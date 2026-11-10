# src/tools/microbe_recommender.py
# M5: 微生物推荐工具（严格镜像学生 microbe_crew.tools.enzyme2organism_tool）
#
# 职责：把酶 UID 映射到 reviewed UniProt 宿主（主证据）+ 独立 KEGG multiplicity（交叉证据），
#       产出 EnzymeSourceProvenance（原始证据维度透传），供 OrganismAggregator 聚合。
#
# 纪律：
# - MT-D1：v1 仅纳入 UniProt reviewed (Swiss-Prot) 宿主；unreviewed(TrEMBL) 记为 SourceError 排除。
# - MT-D2：透传原始维度（reviewed 状态 / annotation score / protein existence / KEGG multiplicity），
#          不合成 organism_confidence float、不把 reviewed/unreviewed 映射成 0-1。
# - 不做 metaTraits 性状判定 / 污水适配打分（M4b，未立项）。habitat_match 一律留空并诚实标注。
#
# T6-R3A-R2A（§5—§8）追加纪律：
# - 宿主证据解析路由三态且互不冒充：
#     LIVE_UNIPROT_REVIEWED            —— live UniProt reviewed response（真实 URL/entryType/response SHA）
#     FROZEN_REVIEWED_UID_MAP_FALLBACK —— live 失败/非 reviewed 时改用冻结 reviewed UID map 行
#     （两者均失败）                     —— 诚实 UNRESOLVED，不伪造宿主
# - 冻结 map 行绝不写入 UniProtReviewedHostEvidence（该模型语义 = live response）。
# - source_signature 表达**宿主身份**（map 审计签名或确定性 taxon|organism 构造），
#   accession / URL / response SHA / map 行号只作为 evidence record identity。
# - map 部署路径复用既有 C8_UID_SOURCE_MAP_PATH 环境变量；不硬编码主机目录、不复制大表。

import csv
import hashlib
import json
import logging
import os
import stat
from typing import Any, Dict, List, Optional, Tuple

import httpx

from src.schemas.evidence import (
    EnzymeSourceProvenance,
    EvidenceRecord,
    HostEvidenceRecord,
    KEGGSupplementEvidence,
    MicrobeCandidate,
    OrganismCandidate,
    SourceError,
    UniProtReviewedHostEvidence,
    host_signature_is_enzyme_uid_shaped,
)

logger = logging.getLogger(__name__)

UNIPROT_ENTRY_TYPE = "UniProtKB reviewed (Swiss-Prot)"
_HTTP_TIMEOUT = 20.0
_USER_AGENT = "EnzymeCAGE-Crew-Enzyme2Organism/1.0"
_HEADERS = {"User-Agent": _USER_AGENT, "Accept": "application/json, text/plain"}


def _uniprot_url(uid: str) -> str:
    return f"https://rest.uniprot.org/uniprotkb/{uid}.json"


def _kegg_url(uid: str) -> str:
    return f"https://rest.kegg.jp/conv/genes/uniprot:{uid}"


def _request_bytes(url: str) -> bytes:
    resp = httpx.get(url, headers=_HEADERS, timeout=_HTTP_TIMEOUT)
    resp.raise_for_status()
    return bytes(resp.content)


def _request_error(source: str, url: str, exc: Exception) -> SourceError:
    return SourceError(
        source_database=source,
        source_url=url,
        error_type=type(exc).__name__,
        message=str(exc),
    )



# ═══════════════════════════════════════════════════════════════════════════
# G4-R2A §6：冻结 reviewed UID map（live 失败时的第二来源）进程级 lazy loader
# ═══════════════════════════════════════════════════════════════════════════
# 复用项目既有部署约定：C8_UID_SOURCE_MAP_PATH 指向权威 CSV 绝对路径（T5B 起沿用）。
# 不新造第二张大表、不把 104MB 表复制进仓库/交付包、不在源码里硬编码主机绝对路径。
FROZEN_UID_MAP_ENV_VAR = "C8_UID_SOURCE_MAP_PATH"
FROZEN_UID_MAP_BASENAME = "uid_to_source_keep_bacteria_fungi_archaea.csv"
FROZEN_UID_MAP_BYTES = 104025134
FROZEN_UID_MAP_SHA256 = (
    "7b92e8e625cb73f070c8e902687ea5bbdbf749f04a19828e550e3fe205684fe6"
)
FROZEN_UID_MAP_REQUIRED_COLUMNS = (
    "UniprotID",
    "TaxID",
    "organism_name",
    "reviewed",
    "source_signature",
    "source_resolution_level",
    "mapping_confidence",
    "is_ambiguous",
    "source_db",
)
# 该表 reviewed 列实测唯一取值（小写字面量），非此值即不得当作 reviewed fallback
FROZEN_UID_MAP_REVIEWED_VALUE = "reviewed"
# source_resolution_level → 四项 identity-resolution 中的 resolved 值。
# REPRESENTATIVE_STRAIN 不启用：无 map 级菌株权威时不声称该分辨率。
FROZEN_UID_MAP_RESOLUTION_BY_LEVEL = {
    "proteome": "EXACT_STRAIN",      # 唯一 proteome id → 菌株/组装级
    "taxon_organism": "SPECIES",     # 仅 TaxID + organism name → 种级
}
# §5 确定性构造规则（对外可复算；不是 map 审计签名，不得冒充）
HOST_SIGNATURE_CONSTRUCTION_RULE = (
    "taxon:<positive_ncbi_taxid>|organism:<scientific_name stripped, "
    "internal whitespace collapsed to single ASCII spaces, casefolded>"
)

# 进程级缓存：整表只流式扫描一次，只留「UID → 原始行字节定位」紧凑索引；之后任意 UID
# 都用 os.pread 回读那一行（不再扫描 104MB 表，§6 第 7 条）。已解析行 identity 与
# UID 级错误（含缺行）同样进程级永久缓存 ⇒ 同批重复查询零 I/O。
_FROZEN_MAP_INDEX: Dict[str, Tuple[Tuple[int, int, int], ...]] = {}
_FROZEN_MAP_HEADER: Optional[List[str]] = None
_FROZEN_MAP_ROWS: Dict[str, Dict[str, Any]] = {}
_FROZEN_MAP_UID_ERRORS: Dict[str, str] = {}
_FROZEN_MAP_SEEN_UIDS: set = set()
_FROZEN_MAP_FULL_SCAN_DONE = False
_FROZEN_MAP_SCAN_COUNT = 0
_FROZEN_MAP_OPEN_COUNT = 0
_FROZEN_MAP_LINE_READ_COUNT = 0
_FROZEN_MAP_GATE_ERROR: Optional[str] = None
_FROZEN_MAP_TABLE_SHA256: Optional[str] = None
_FROZEN_MAP_PATH: Optional[str] = None
_FROZEN_MAP_FH: Optional[Any] = None


def frozen_map_cache_stats() -> Dict[str, Any]:
    """只读观测面：开表/全表扫描/行回读次数与已核身份（§6「不重复扫描」的实证）。"""
    return {
        "env_var": FROZEN_UID_MAP_ENV_VAR,
        "env_configured": bool((os.environ.get(FROZEN_UID_MAP_ENV_VAR) or "").strip()),
        "gate_error": _FROZEN_MAP_GATE_ERROR,
        "table_sha256": _FROZEN_MAP_TABLE_SHA256,
        "open_count": _FROZEN_MAP_OPEN_COUNT,
        "scan_count": _FROZEN_MAP_SCAN_COUNT,
        "full_scan_done": _FROZEN_MAP_FULL_SCAN_DONE,
        "indexed_uids": len(_FROZEN_MAP_INDEX),
        "line_read_count": _FROZEN_MAP_LINE_READ_COUNT,
        "cached_row_uids": len(_FROZEN_MAP_ROWS),
        "cached_queried_uids": len(_FROZEN_MAP_SEEN_UIDS),
    }


def _frozen_map_file_sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _frozen_map_identity_error(path: str) -> Optional[str]:
    """开表前的身份门（§6 顺序：路径 → regular/非 symlink → bytes → 固定 SHA）。"""
    if not path:
        return (
            f"{FROZEN_UID_MAP_ENV_VAR} is not configured: frozen reviewed UID map "
            "unavailable (no silent online/name-matching/TaxID-approximation fallback)"
        )
    if not os.path.isabs(path):
        return f"{FROZEN_UID_MAP_ENV_VAR} must be an absolute path, got {path!r}"
    try:
        st = os.lstat(path)
    except OSError as exc:
        return f"frozen reviewed UID map missing/unreadable at configured path: {type(exc).__name__}: {exc}"
    if stat.S_ISLNK(st.st_mode):
        return f"frozen reviewed UID map path is a symlink (refused): {path}"
    if not stat.S_ISREG(st.st_mode):
        return f"frozen reviewed UID map path is not a regular file: {path}"
    if st.st_size != FROZEN_UID_MAP_BYTES:
        return (
            "frozen reviewed UID map byte size mismatch: "
            f"observed {st.st_size}, frozen {FROZEN_UID_MAP_BYTES}"
        )
    digest = _frozen_map_file_sha256(path)
    if digest != FROZEN_UID_MAP_SHA256:
        return (
            "frozen reviewed UID map sha256 mismatch: "
            f"observed {digest}, frozen {FROZEN_UID_MAP_SHA256}"
        )
    if os.path.basename(path) != FROZEN_UID_MAP_BASENAME:
        return (
            "frozen reviewed UID map filename identity mismatch (possible wrong table): "
            f"observed {os.path.basename(path)!r}, expected {FROZEN_UID_MAP_BASENAME!r}"
        )
    return None


def _frozen_map_gate() -> Tuple[Optional[str], Optional[str]]:
    """首次真正需要 map 时才核身份（lazy）；结果与错误都在进程内缓存，不重复核。"""
    global _FROZEN_MAP_GATE_ERROR, _FROZEN_MAP_PATH, _FROZEN_MAP_TABLE_SHA256
    if _FROZEN_MAP_GATE_ERROR is not None:
        return None, _FROZEN_MAP_GATE_ERROR
    if _FROZEN_MAP_PATH is not None:
        return _FROZEN_MAP_PATH, None
    path = (os.environ.get(FROZEN_UID_MAP_ENV_VAR) or "").strip()
    err = _frozen_map_identity_error(path)
    if err is not None:
        _FROZEN_MAP_GATE_ERROR = err
        logger.warning("[microbe_recommender] frozen reviewed UID map unavailable: %s", err)
        return None, err
    _FROZEN_MAP_TABLE_SHA256 = FROZEN_UID_MAP_SHA256
    _FROZEN_MAP_PATH = path
    return path, None


def _frozen_map_validate_row(line_no: int, header: List[str], cols: Dict[str, str]) -> Tuple[
    Optional[Dict[str, Any]], Optional[str]
]:
    """单行合法性（§6：只接受 UID 精确匹配 + reviewed 合法行；身份不明即显式错误）。"""
    uid = cols.get("UniprotID", "").strip()
    if not uid:
        return None, f"frozen map line {line_no} has an empty UniprotID"
    if cols.get("reviewed", "").strip() != FROZEN_UID_MAP_REVIEWED_VALUE:
        return None, (
            f"frozen map line {line_no} (uid {uid}) is not a reviewed row "
            f"(reviewed={cols.get('reviewed', '')!r}); refusing to use it as reviewed fallback"
        )
    if cols.get("is_ambiguous", "").strip() not in ("", "0"):
        return None, (
            f"frozen map line {line_no} (uid {uid}) is flagged ambiguous "
            f"(is_ambiguous={cols.get('is_ambiguous')!r}); refusing to pick a host"
        )
    raw_taxid = cols.get("TaxID", "").strip()
    try:
        taxid = int(raw_taxid)
    except ValueError:
        return None, f"frozen map line {line_no} (uid {uid}) has non-integer TaxID {raw_taxid!r}"
    if taxid <= 0:
        return None, f"frozen map line {line_no} (uid {uid}) has non-positive TaxID {taxid}"
    name = cols.get("organism_name", "").strip()
    if not name:
        return None, f"frozen map line {line_no} (uid {uid}) has an empty organism_name"
    signature = cols.get("source_signature", "").strip()
    if not signature:
        return None, f"frozen map line {line_no} (uid {uid}) has an empty source_signature"
    if host_signature_is_enzyme_uid_shaped(uid, signature):
        return None, (
            f"frozen map line {line_no} source_signature {signature!r} is enzyme-UID-shaped, "
            "not a host identity (T6-R3A-R2A §5 root cause C)"
        )
    level = cols.get("source_resolution_level", "").strip()
    resolution = FROZEN_UID_MAP_RESOLUTION_BY_LEVEL.get(level)
    if resolution is None:
        return None, (
            f"frozen map line {line_no} (uid {uid}) has unknown source_resolution_level "
            f"{level!r}; no defensible host identity resolution (not guessing SPECIES/STRAIN)"
        )
    return {
        "uid": uid,
        "line": line_no,
        "taxid": taxid,
        "organism_name": name,
        "source_signature": signature,
        "resolution_level": level,
        "host_resolution": resolution,
        "mapping_confidence": cols.get("mapping_confidence", "").strip(),
        "source_db": cols.get("source_db", "").strip(),
        "reviewed": cols.get("reviewed", "").strip(),
        "header_columns": len(header),
    }, None


def _frozen_map_scan(path: str) -> None:
    """全表只流式扫描一次，建 UID → 原始行定位（1-based 行号, 字节偏移, 字节长度）索引。

    只留定长定位信息、不缓存任何行内容 ⇒ 104MB 表在本进程内被完整读取的次数恒为 1，
    后续任意批次的新 UID 都走索引 + os.pread 回读（§6 第 7 条）。UniprotID 是首列且
    实测无引号包裹，故用廉价的「首个逗号前字段」建索引键；行内容合法性仍在回读时由
    csv 解析 + `_frozen_map_validate_row` 逐行判定，并要求 UniprotID 与查询 UID 全等
    （索引只是加速器，不作为匹配依据）。
    """
    global _FROZEN_MAP_SCAN_COUNT, _FROZEN_MAP_OPEN_COUNT
    global _FROZEN_MAP_GATE_ERROR, _FROZEN_MAP_HEADER
    global _FROZEN_MAP_FULL_SCAN_DONE, _FROZEN_MAP_FH
    _FROZEN_MAP_SCAN_COUNT += 1
    _FROZEN_MAP_OPEN_COUNT += 1
    header: Optional[List[str]] = None
    index: Dict[str, List[Tuple[int, int, int]]] = {}
    fh = open(path, "rb")
    try:
        offset = 0
        for line_no, raw in enumerate(fh, start=1):
            length = len(raw)
            if line_no == 1:
                try:
                    header = next(csv.reader([raw.decode("utf-8")]))
                except UnicodeDecodeError as exc:
                    _FROZEN_MAP_GATE_ERROR = (
                        f"frozen reviewed UID map header is not valid UTF-8: {exc}"
                    )
                    fh.close()
                    return
                missing = [c for c in FROZEN_UID_MAP_REQUIRED_COLUMNS if c not in header]
                if missing:
                    _FROZEN_MAP_GATE_ERROR = (
                        "frozen reviewed UID map CSV schema mismatch, missing columns: "
                        + ", ".join(missing)
                    )
                    fh.close()
                    return
                offset += length
                continue
            first = raw.split(b",", 1)[0].decode("ascii", "ignore").strip()
            if first:
                index.setdefault(first, []).append((line_no, offset, length))
            offset += length
    except BaseException:
        fh.close()
        raise
    # 扫描成功 → 同一句柄保留给后续 os.pread 行回读（本进程不再第二次开表/扫描）
    _FROZEN_MAP_FH = fh
    _FROZEN_MAP_HEADER = header
    _FROZEN_MAP_INDEX.clear()
    for uid, locations in index.items():
        _FROZEN_MAP_INDEX[uid] = tuple(locations)
    _FROZEN_MAP_FULL_SCAN_DONE = True


def _frozen_map_read_row(
    path: str, uid: str
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """按索引回读单 UID 的原始行 bytes：同一 bytes 既做 csv 解析又做行 SHA256（§6 第 5 条）。

    返回 (identity, 不可用原因)。同 UID 多行：identity 全等 → 取首条并把其余行号记入
    duplicate_rows；有差异 → 显式冲突错误（不猜、不择优选一条）。缺行 → 显式「无行」
    错误（精确匹配，不做前缀/模糊/Name 匹配）。
    """
    global _FROZEN_MAP_LINE_READ_COUNT
    locations = _FROZEN_MAP_INDEX.get(uid)
    if not locations:
        return None, (
            "uid has no row in the frozen reviewed UID map "
            "(no ambiguous/prefix/Name matching performed)"
        )
    header = _FROZEN_MAP_HEADER or []
    transient_fd: Optional[int] = None
    if _FROZEN_MAP_FH is not None:
        fd = _FROZEN_MAP_FH.fileno()
    else:
        transient_fd = os.open(path, os.O_RDONLY)
        fd = transient_fd
    identities: List[Dict[str, Any]] = []
    failures: List[str] = []
    try:
        for line_no, offset, length in locations:
            _FROZEN_MAP_LINE_READ_COUNT += 1
            raw = os.pread(fd, length, offset)
            if len(raw) != length:
                failures.append(
                    f"frozen map line {line_no} could not be fully re-read "
                    f"({len(raw)} of {length} bytes)"
                )
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                failures.append(f"frozen map line {line_no} is not valid UTF-8: {exc}")
                continue
            row = next(csv.reader([text]))
            cols = {
                name: (row[i].strip() if i < len(row) else "")
                for i, name in enumerate(header)
            }
            identity, err = _frozen_map_validate_row(line_no, header, cols)
            if err is not None:
                failures.append(err)
                continue
            assert identity is not None
            if identity["uid"] != uid:
                failures.append(
                    "frozen map line " + str(line_no) + " row uid "
                    + repr(identity["uid"]) + " does not exactly match queried uid "
                    + repr(uid)
                )
                continue
            identity = dict(identity)
            identity["file"] = os.path.basename(path)
            identity["table_sha256"] = _FROZEN_MAP_TABLE_SHA256 or FROZEN_UID_MAP_SHA256
            identity["row_sha256"] = hashlib.sha256(raw).hexdigest()
            identities.append(identity)
    finally:
        if transient_fd is not None:
            os.close(transient_fd)
    if not identities:
        return None, " | ".join(failures)
    distinct = {
        (i["source_signature"], i["taxid"], i["organism_name"], i["host_resolution"])
        for i in identities
    }
    if len(distinct) > 1:
        return None, (
            f"uid {uid} has {len(distinct)} conflicting host identity rows in the frozen "
            "reviewed UID map (lines "
            + ", ".join(str(i["line"]) for i in identities)
            + "); refusing to pick one"
        )
    if len(identities) > 1:
        identities[0]["duplicate_rows"] = [i["line"] for i in identities[1:]]
    return identities[0], None


def frozen_map_host_identity(
    uids: List[str],
) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, str], Optional[str]]:
    """按需解析冻结 map 宿主身份。返回 ({uid: row_identity}, {uid: 不可用原因}, 全局错误)。

    全局错误非 None 即整表不可用（未配置 / 非 regular / symlink / bytes / SHA / 文件名 /
    CSV schema / header 非法编码）；单 UID 错误表示该行缺失或非 reviewed / ambiguous /
    身份冲突 / resolution level 未知。两种情况都**不会**伪造宿主，也不降级为 live。

    缓存语义（§6 第 7 条）：首次真正需要 map 才开表并流式扫描一次；此后任意批次的新 UID
    仅查索引 + os.pread 回读该行（不重复扫描），已解析 identity 与缺行/坏行错误均永久
    缓存，同批重复 UID 直接命中缓存。
    """
    path, gate_err = _frozen_map_gate()
    if gate_err is not None or path is None:
        return {}, {}, gate_err or "frozen reviewed UID map unavailable"
    if _FROZEN_MAP_GATE_ERROR is not None:
        return {}, {}, _FROZEN_MAP_GATE_ERROR
    if not _FROZEN_MAP_FULL_SCAN_DONE:
        _frozen_map_scan(path)
        if _FROZEN_MAP_GATE_ERROR is not None:
            return {}, {}, _FROZEN_MAP_GATE_ERROR
    rows: Dict[str, Dict[str, Any]] = {}
    errors: Dict[str, str] = {}
    for uid in dict.fromkeys(uids):
        if uid not in _FROZEN_MAP_SEEN_UIDS:
            _FROZEN_MAP_SEEN_UIDS.add(uid)
            identity, err = _frozen_map_read_row(path, uid)
            if err is not None:
                _FROZEN_MAP_UID_ERRORS[uid] = err
            else:
                assert identity is not None
                _FROZEN_MAP_ROWS[uid] = identity
        if uid in _FROZEN_MAP_ROWS:
            rows[uid] = _FROZEN_MAP_ROWS[uid]
        elif uid in _FROZEN_MAP_UID_ERRORS:
            errors[uid] = _FROZEN_MAP_UID_ERRORS[uid]
    return rows, errors, None


def resolve_host_identity(
    uid: str,
    uniprot: Optional[UniProtReviewedHostEvidence],
    live_failure: Optional[str],
) -> Dict[str, Any]:
    """§5/§7：为单酶产出「宿主 identity」字段包（EnzymeSourceProvenance 的关键字参数）。

    路由优先级（严格，不互相冒充）：
      1. live UniProt reviewed 命中  → route=LIVE_UNIPROT_REVIEWED（证据事实取 live response）；
         宿主**签名**优先取冻结 map 已审计签名（§5 本任务四 UID 的权威宿主 identity）；
         map 不可用/无行/TaxID 与 live 不一致 → 改用 §5 确定性构造并留痕（不因此降级 UNRESOLVED）。
      2. live 失败或非 reviewed      → 若冻结 map 有合法 reviewed 行：route=FROZEN_REVIEWED_UID_MAP_FALLBACK
         （不写 UniProtReviewedHostEvidence、不声称 live URL/response SHA）。
      3. 两者皆失败                  → route=None（下游强制 UNRESOLVED），并记 frozen_map_error。
    本函数纯计算：不访问网络；map 读取由 §6 lazy loader 一次性完成。
    """
    rows, uid_errors, gate_err = frozen_map_host_identity([uid])
    row = rows.get(uid)
    warnings: List[str] = []
    kwargs: Dict[str, Any] = {
        "resolution_route": None,
        "host_identity_source": None,
        "host_identity_source_signature": None,
        "host_resolution": None,
        "host_taxid": None,
        "host_name": None,
        "frozen_map_file": None,
        "frozen_map_line": None,
        "frozen_map_row_sha256": None,
        "frozen_map_table_sha256": None,
        "frozen_map_error": None,
        "mapping_confidence_raw": None,
        "warnings": warnings,
    }
    if uniprot is not None:
        kwargs["resolution_route"] = "LIVE_UNIPROT_REVIEWED"
        warnings.append("resolution_route=LIVE_UNIPROT_REVIEWED")
        taxid, name = int(uniprot.ncbi_taxon_id), uniprot.scientific_organism_name
        if row is not None and row["taxid"] == taxid:
            kwargs["host_identity_source"] = "FROZEN_REVIEWED_UID_MAP"
            kwargs["host_identity_source_signature"] = row["source_signature"]
            kwargs["host_resolution"] = row["host_resolution"]
            kwargs["frozen_map_file"] = row["file"]
            kwargs["frozen_map_line"] = row["line"]
            kwargs["frozen_map_row_sha256"] = row["row_sha256"]
            kwargs["frozen_map_table_sha256"] = row["table_sha256"]
            kwargs["mapping_confidence_raw"] = row["mapping_confidence"]
            warnings.append(
                "host_identity_source=FROZEN_REVIEWED_UID_MAP: audited host signature taken "
                f"from frozen reviewed UID map {row['file']}:line={row['line']} "
                f"(source_resolution_level={row['resolution_level']}); host evidence itself "
                "remains the live UniProt reviewed response"
            )
            if " ".join(str(name).split()).casefold() != " ".join(
                    str(row["organism_name"]).split()).casefold():
                warnings.append(
                    "host_name_differs_live_vs_frozen_map: names remain different under the "
                    "declared normalization; TaxID matches; map contains an additional "
                    "parenthetical historical name; live observed name remains unchanged; "
                    "map signature/name remains unchanged; no synonym equivalence is "
                    f"adjudicated by this task; live={name!r} map={row['organism_name']!r}"
                )
        else:
            reason = (
                "frozen map row TaxID "
                f"{row['taxid']} disagrees with live UniProt TaxID {taxid}: refusing to mix "
                "two host identity sources"
                if row is not None else
                (gate_err or uid_errors.get(uid) or "no frozen map row")
            )
            kwargs["host_identity_source"] = "CONSTRUCTED_TAXON_ORGANISM"
            kwargs["host_identity_source_signature"] = _constructed_host_signature(taxid, name)
            kwargs["host_resolution"] = "SPECIES"
            if row is None:
                kwargs["frozen_map_error"] = reason
            warnings.append(
                f"host identity via §5 deterministic construction (not a frozen-map signature): {reason}"
            )
            warnings.append(
                f"construction_rule={HOST_SIGNATURE_CONSTRUCTION_RULE}; "
                f"original live scientific organism name={name!r}; "
                "host_resolution kept at SPECIES without map-level strain authority"
            )
        kwargs["host_taxid"] = taxid
        kwargs["host_name"] = name
        if live_failure:
            warnings.append(f"live_uniprot_notes: {live_failure}")
        return kwargs
    if row is not None:
        kwargs["resolution_route"] = "FROZEN_REVIEWED_UID_MAP_FALLBACK"
        kwargs["host_identity_source"] = "FROZEN_REVIEWED_UID_MAP"
        kwargs["host_identity_source_signature"] = row["source_signature"]
        kwargs["host_resolution"] = row["host_resolution"]
        kwargs["host_taxid"] = row["taxid"]
        kwargs["host_name"] = row["organism_name"]
        kwargs["frozen_map_file"] = row["file"]
        kwargs["frozen_map_line"] = row["line"]
        kwargs["frozen_map_row_sha256"] = row["row_sha256"]
        kwargs["frozen_map_table_sha256"] = row["table_sha256"]
        kwargs["mapping_confidence_raw"] = row["mapping_confidence"]
        warnings.extend([
            "resolution_route=FROZEN_REVIEWED_UID_MAP_FALLBACK",
            "live_uniprot_failure: " + (live_failure or "no reviewed UniProt evidence returned"),
            "frozen_map_identity: " + f"{row['file']}:line={row['line']} "
            + f"row_sha256={row['row_sha256']} table_sha256={row['table_sha256']} "
            + f"source_db={row['source_db']} reviewed={row['reviewed']}",
            "the frozen reviewed UID map row is mapping evidence, NOT a live UniProt response: "
            "no live URL / entryType / response SHA is claimed for this record",
            "mapping_confidence_raw="
            + f"{row['mapping_confidence']!r} (source_resolution_level={row['resolution_level']}) "
            "recorded verbatim; never converted into a confidence/score (MT-D2)",
        ])
        if row.get("duplicate_rows"):
            warnings.append(
                "frozen map duplicate identical-identity rows ignored: "
                + ", ".join(str(n) for n in row["duplicate_rows"])
            )
        return kwargs
    # 路由 3：live 与冻结 map 均未命中 → 交给下游强制 UNRESOLVED（不伪造宿主）
    map_reason = gate_err or uid_errors.get(uid) or "no usable frozen reviewed UID map row"
    kwargs["frozen_map_error"] = map_reason
    warnings.extend([
        "resolution_route=UNRESOLVED (no live reviewed UniProt evidence and no usable "
        "frozen reviewed UID map row)",
        "live_uniprot_failure: " + (live_failure or "no reviewed UniProt evidence returned"),
        "frozen_map_unavailable: " + map_reason,
    ])
    return kwargs


def _constructed_host_signature(taxon_id: int, organism_name: str) -> str:
    """§5 确定性构造：规则见 HOST_SIGNATURE_CONSTRUCTION_RULE（可复算，不冒充 map 签名）。"""
    normalized = " ".join(str(organism_name).split()).casefold()
    return f"taxon:{int(taxon_id)}|organism:{normalized}"


def query_uniprot_reviewed(
    uid: str,
) -> Tuple[Optional[UniProtReviewedHostEvidence], Optional[SourceError]]:
    """查询 reviewed UniProt 宿主证据；unreviewed / 校验失败返回 (None, SourceError)。"""
    url = _uniprot_url(uid)
    body = _request_bytes(url)
    digest = hashlib.sha256(body).hexdigest()
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, SourceError(
            source_database="UniProtKB", source_url=url,
            error_type="malformed_response", message=f"invalid UTF-8 JSON: {exc}",
        )

    if not isinstance(payload, dict):
        return None, SourceError(
            source_database="UniProtKB", source_url=url,
            error_type="malformed_response", message="top-level UniProt response is not an object",
        )
    if payload.get("primaryAccession") != uid:
        return None, SourceError(
            source_database="UniProtKB", source_url=url,
            error_type="primary_accession_mismatch",
            message="primaryAccession does not exactly match the requested UID",
        )
    if payload.get("entryType") != UNIPROT_ENTRY_TYPE:
        return None, SourceError(
            source_database="UniProtKB", source_url=url,
            error_type="unreviewed_or_unsupported_entry",
            message="entryType is not UniProtKB reviewed (Swiss-Prot)",
        )

    organism = payload.get("organism")
    if not isinstance(organism, dict):
        organism = {}
    name = organism.get("scientificName")
    taxon_id = organism.get("taxonId")
    if not isinstance(name, str) or not name.strip():
        return None, SourceError(
            source_database="UniProtKB", source_url=url,
            error_type="missing_reviewed_host",
            message="reviewed record lacks a scientific organism name",
        )
    if isinstance(taxon_id, bool) or not isinstance(taxon_id, int) or taxon_id <= 0:
        return None, SourceError(
            source_database="UniProtKB", source_url=url,
            error_type="missing_reviewed_host",
            message="reviewed record lacks a positive integer NCBI taxon ID",
        )

    try:
        evidence = UniProtReviewedHostEvidence(
            source_url=url,
            response_sha256=digest,
            primary_accession=payload["primaryAccession"],
            entry_type=payload["entryType"],
            reviewed=True,
            scientific_organism_name=name,
            ncbi_taxon_id=taxon_id,
            lineage=organism.get("lineage", []),
            annotation_score=payload["annotationScore"],
            protein_existence=payload["proteinExistence"],
        )
    except (KeyError, TypeError, ValueError) as exc:
        return None, SourceError(
            source_database="UniProtKB", source_url=url,
            error_type="malformed_response",
            message=f"reviewed evidence fields are malformed: {exc}",
        )
    return evidence, None


def query_kegg(uid: str) -> KEGGSupplementEvidence:
    """查询 KEGG 基因映射并保留 multiplicity 原样（解析异常时向上抛出，由调用方转 SourceError）。"""
    url = _kegg_url(uid)
    body = _request_bytes(url)
    digest = hashlib.sha256(body).hexdigest()
    text = body.decode("utf-8")
    expected_left = f"up:{uid}"
    gene_ids: List[str] = []
    seen: set = set()
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip():
            continue
        fields = raw_line.split("\t")
        if len(fields) != 2 or fields[0] != expected_left or not fields[1] or ":" not in fields[1]:
            raise ValueError(f"invalid KEGG conversion row {line_number}")
        gene_id = fields[1]
        if gene_id not in seen:
            seen.add(gene_id)
            gene_ids.append(gene_id)
    multiplicity = len(gene_ids)
    state = "missing" if multiplicity == 0 else "single" if multiplicity == 1 else "multiple"
    return KEGGSupplementEvidence(
        source_url=url, response_sha256=digest,
        gene_ids=gene_ids, multiplicity=multiplicity, state=state,
    )


def _map_one(uid: str) -> EnzymeSourceProvenance:
    errors: List[SourceError] = []
    uniprot: Optional[UniProtReviewedHostEvidence] = None
    kegg: Optional[KEGGSupplementEvidence] = None
    try:
        uniprot, exclusion = query_uniprot_reviewed(uid)
        if exclusion is not None:
            errors.append(exclusion)
    except httpx.HTTPError as exc:
        errors.append(_request_error("UniProtKB", _uniprot_url(uid), exc))
    try:
        kegg = query_kegg(uid)
    except (httpx.HTTPError, ValueError, UnicodeDecodeError) as exc:
        errors.append(_request_error("KEGG", _kegg_url(uid), exc))
    # G4-R2A §7：live reviewed 未命中时不直接判死，先查冻结 reviewed UID map（fallback），
    # 两者均失败才留 route=None（下游强制 UNRESOLVED）。KEGG 仍是独立补充，不参与宿主身份。
    live_failure = "; ".join(
        f"{e.source_database}:{e.error_type}" for e in errors if e.source_database == "UniProtKB"
    ) or None
    host_identity = resolve_host_identity(uid, uniprot, live_failure)
    return EnzymeSourceProvenance(
        enzyme_uid=uid,
        uniprot_reviewed=uniprot,
        kegg=kegg,
        source_errors=errors,
        **host_identity,
    )


def map_enzyme_hosts(enzyme_uids: List[str]) -> Dict[str, EnzymeSourceProvenance]:
    """给定酶 UID 列表，映射到 reviewed UniProt 宿主 + KEGG multiplicity（首见去重顺序）。

    Returns:
        {enzyme_uid: EnzymeSourceProvenance}。网络不可用时各源记 SourceError，不编造。
    """
    # G4-R2A §6：一次性预热本批 UID 的冻结 map 身份 → 后续 _map_one 全部命中进程缓存，
    # 整批至多一次开表/扫描（不逐 UID 重复扫 104MB 表）。
    unique_uids = list(dict.fromkeys(enzyme_uids))
    frozen_map_host_identity(unique_uids)
    provenance: Dict[str, EnzymeSourceProvenance] = {}
    for uid in unique_uids:
        provenance[uid] = _map_one(uid)
    live = sum(1 for p in provenance.values() if p.resolution_route == "LIVE_UNIPROT_REVIEWED")
    fallback = sum(
        1 for p in provenance.values()
        if p.resolution_route == "FROZEN_REVIEWED_UID_MAP_FALLBACK"
    )
    unresolved = len(provenance) - live - fallback
    logger.info(
        f"[microbe_recommender] 映射 {len(provenance)} 个酶 UID → live reviewed {live} 个 / "
        f"冻结 map fallback {fallback} 个 / 未解析 {unresolved} 个"
    )
    return provenance


def microbe_candidates_from_provenance(
    provenance: Dict[str, EnzymeSourceProvenance],
    order: List[str],
    environment: str = "wastewater",
) -> List[MicrobeCandidate]:
    """从 provenance 派生 MicrobeCandidate（仅 reviewed 宿主），供展示/证据链使用。

    MT-D1：仅 reviewed 宿主成为候选；两条合法 reviewed 路由都进候选（互不冒充，由
    resolution_route 区分）——live UniProt reviewed response，或冻结 reviewed UID map 行。
    未解析（含 unreviewed / 两源均失败）不进候选，排除留痕在 provenance。
    """
    candidates: List[MicrobeCandidate] = []
    for uid in order:
        prov = provenance.get(uid)
        if prov is None:
            continue
        route = prov.resolution_route
        kegg_note = ""
        if prov.kegg is not None:
            kegg_note = f"；KEGG multiplicity={prov.kegg.multiplicity}({prov.kegg.state})"
        if route == "LIVE_UNIPROT_REVIEWED" and prov.uniprot_reviewed is not None:
            up = prov.uniprot_reviewed
            organism_name, tax_id = up.scientific_organism_name, up.ncbi_taxon_id
            rationale = (
                f"UniProt reviewed 宿主（annotation_score={up.annotation_score}, "
                f"protein_existence={up.protein_existence}{kegg_note}）；"
                f"宿主 identity={prov.host_identity_source_signature}"
                f"（host_identity_source={prov.host_identity_source}）；"
                f"目标环境 {environment} 未做性状适配评估，待 M4b metaTraits 集成"
            )
        elif (
            route == "FROZEN_REVIEWED_UID_MAP_FALLBACK"
            and prov.host_taxid is not None and prov.host_name
        ):
            organism_name, tax_id = prov.host_name, prov.host_taxid
            rationale = (
                f"live UniProt 未取得 reviewed 证据，改用冻结 reviewed UID map 第 "
                f"{prov.frozen_map_file}:line={prov.frozen_map_line} 行"
                f"（host_resolution={prov.host_resolution}, mapping_confidence 原值="
                f"{prov.mapping_confidence_raw}；非 live response，不声称 annotation_score）"
                f"{kegg_note}；宿主 identity={prov.host_identity_source_signature}；"
                f"目标环境 {environment} 未做性状适配评估，待 M4b metaTraits 集成"
            )
        else:
            continue  # MT-D1/§7：未解析宿主不进候选，不伪造
        candidates.append(
            MicrobeCandidate(
                organism_name=organism_name,
                tax_id=tax_id,
                enzyme_uid=uid,
                habitat_match=None,  # M4b 未立项，不做污水适配评估
                growth_conditions=None,
                source_db="UniProt",
                evidence_level="reviewed",
                rationale=rationale,
                resolution_route=route,
                host_identity_source_signature=prov.host_identity_source_signature,
            )
        )
    return candidates


def recommend_microbes(
    enzyme_uids: List[str],
    environment: str = "wastewater",
    top_k: int = 5,
) -> List[MicrobeCandidate]:
    """便捷入口：映射 + 派生 MicrobeCandidate（reviewed-only）。

    保留此函数以兼容既有调用；内部走 map_enzyme_hosts 单次网络查询。
    """
    uids = enzyme_uids[:top_k] if top_k else enzyme_uids
    provenance = map_enzyme_hosts(uids)
    candidates = microbe_candidates_from_provenance(provenance, uids, environment)
    if not candidates:
        logger.warning(
            "[microbe_recommender] 未获得任何 reviewed organism 映射（网络不可用或全部 unreviewed），返回空列表"
        )
    return candidates


def build_host_evidence_record(
    enzyme_uid: str,
    provenance: EnzymeSourceProvenance,
    host_resolution: Optional[str] = None,
    warnings: Optional[List[str]] = None,
) -> HostEvidenceRecord:
    """把单酶 EnzymeSourceProvenance 转换为 production HostEvidenceRecord（G4-R1 真实接线）。

    纪律（T6-R3A-R1 §7 八条最小修正 + T6-R3A-R2A §5/§6 修正）：
    - host_resolution 必须是三合法 resolved 值之一；已解析宿主不得降级 UNRESOLVED；
      取值优先用节点/provenance 携带的宿主 identity resolution，调用方显式值不得与之冲突。
    - **R2A §5 根因 C**：source_signature 表达宿主身份（冻结 map 审计签名或 §5 确定性
      taxon|organism 构造），不再写 ``uniprotkb_reviewed:<enzyme_uid>``；accession 属于
      evidence record identity，仍留在 source_record_id。
    - **R2A §6**：fallback 记录 source_record_id=<map basename>:line=<1-based>、
      evidence_hash=该 CSV 原始行 bytes 的 SHA256（表 SHA 记在 provenance），
      host_evidence_source 仍为 [UNIPROT_REVIEWED]（该表 reviewed-only），warnings 显式
      记 resolution_route / live 失败原因 / map 行身份，并声明这不是 live response。
    - 两源均失败：强制 UNRESOLVED + UNRESOLVED source 独占 + 身份字段全 None；
      evidence_hash 为 unresolved 决策材料的 SHA256（warnings 注明非数据 hash）。
    - KEGG 只作独立补充（保留在 provenance.kegg），不并入 host_evidence_source、
      不产生伪造 UniProt reviewed；无 confidence、无 trait_score。
    """
    out_warnings = list(warnings) if warnings else []
    route = provenance.resolution_route
    carried_sig = provenance.host_identity_source_signature
    if carried_sig is not None and host_signature_is_enzyme_uid_shaped(enzyme_uid, carried_sig):
        raise ValueError(
            f"provenance carries an enzyme-UID-shaped host signature {carried_sig!r} for uid "
            f"{enzyme_uid!r}; refusing to emit it as host identity (T6-R3A-R2A §5 root cause C)"
        )
    if route == "FROZEN_REVIEWED_UID_MAP_FALLBACK":
        if provenance.uniprot_reviewed is not None:
            raise ValueError(
                f"uid {enzyme_uid!r}: resolution_route=FROZEN_REVIEWED_UID_MAP_FALLBACK must "
                "not carry a live UniProtReviewedHostEvidence (task section 6)"
            )
        resolution = provenance.host_resolution
        if host_resolution not in (None, resolution):
            raise ValueError(
                f"uid {enzyme_uid!r}: caller-supplied host_resolution {host_resolution!r} "
                f"conflicts with the frozen-map host identity resolution {resolution!r}"
            )
        if resolution not in ("EXACT_STRAIN", "SPECIES", "REPRESENTATIVE_STRAIN"):
            raise ValueError(
                f"uid {enzyme_uid!r}: frozen-map fallback has no defensible resolved "
                f"host_resolution (got {resolution!r})"
            )
        signature = carried_sig or provenance.host_identity_source_signature
        if not (signature and provenance.host_taxid and provenance.host_name):
            raise ValueError(
                f"uid {enzyme_uid!r}: frozen-map fallback lacks host identity "
                "signature/taxid/name"
            )
        return HostEvidenceRecord(
            enzyme_uid=enzyme_uid,
            source_signature=signature,
            host_taxid=provenance.host_taxid,
            host_name=provenance.host_name,
            host_resolution=resolution,
            host_evidence_source=["UNIPROT_REVIEWED"],
            source_record_id=(
                f"{provenance.frozen_map_file}:line={provenance.frozen_map_line}"
            ),
            evidence_hash=str(provenance.frozen_map_row_sha256),
            warnings=_record_warnings(out_warnings, provenance, route),
            resolution_route=route,
            host_identity_source=provenance.host_identity_source,
        )
    up = provenance.uniprot_reviewed
    if up is not None:
        resolution = host_resolution or provenance.host_resolution
        if resolution not in ("EXACT_STRAIN", "SPECIES", "REPRESENTATIVE_STRAIN"):
            raise ValueError(
                f"reviewed UniProt host evidence for uid {enzyme_uid!r} must resolve to "
                f"EXACT_STRAIN/SPECIES/REPRESENTATIVE_STRAIN; got {resolution!r} "
                f"(explicit={host_resolution!r}, carried={provenance.host_resolution!r}); "
                f"reviewed evidence must not be downgraded to UNRESOLVED"
            )
        signature = carried_sig
        identity_source = provenance.host_identity_source
        if not signature:
            # §8 末段：节点输出只携带原始 provenance、未带宿主签名时，转换层按 §5 规则从
            # **已携带字段**确定性补齐，并显式记录输入字段来源（不要求 task 脚本手填）。
            # 转换层刻意不二次打开冻结 map：map identity resolver 的权威生效点在 production
            # 节点侧（§5/§6），其结论已随 state 现有承载键到达下游。
            signature = _constructed_host_signature(
                up.ncbi_taxon_id, up.scientific_organism_name
            )
            identity_source = identity_source or "CONSTRUCTED_TAXON_ORGANISM"
            out_warnings.append(
                "host_identity_supplemented_at_conversion=CONSTRUCTED_TAXON_ORGANISM over "
                f"carried reviewed UniProt host fields (input_fields=ncbi_taxon_id="
                f"{up.ncbi_taxon_id}, scientific_organism_name="
                f"{up.scientific_organism_name!r}); "
                f"construction_rule={HOST_SIGNATURE_CONSTRUCTION_RULE}; "
                "carried host_identity_source_signature absent -> frozen-map authority is "
                "applied in the production node path (task sections 5-6), the conversion "
                "layer deliberately does not re-open the map; "
                "source_record_id stays the UniProt accession "
                + repr(up.primary_accession)
                + " (evidence record identity, not host identity); "
                "no field was hand-filled by a task script"
            )
        identity_source = identity_source or "CONSTRUCTED_TAXON_ORGANISM"
        return HostEvidenceRecord(
            enzyme_uid=enzyme_uid,
            source_signature=signature,
            host_taxid=up.ncbi_taxon_id,
            host_name=up.scientific_organism_name,
            host_resolution=resolution,
            host_evidence_source=["UNIPROT_REVIEWED"],
            source_record_id=up.primary_accession,
            evidence_hash=up.response_sha256,
            warnings=_record_warnings(out_warnings, provenance, route),
            resolution_route=route or "LIVE_UNIPROT_REVIEWED",
            host_identity_source=identity_source,
        )
    # 无 reviewed 分支：强制 UNRESOLVED（含 KEGG 存在时——KEGG 不产生伪造 reviewed）
    if host_resolution not in (None, "UNRESOLVED"):
        raise ValueError(
            f"no reviewed UniProt host evidence for uid {enzyme_uid!r}; "
            f"host_resolution must be UNRESOLVED, got {host_resolution!r}"
        )
    decision_material = (
        f"UNRESOLVED|uid={enzyme_uid}|uniprot_reviewed=absent|"
        f"kegg={'present' if provenance.kegg is not None else 'absent'}"
    )
    out_warnings.append(
        "uniprot_reviewed_absent: resolved as UNRESOLVED; "
        "evidence_hash is the SHA256 of the decision material, not of a data response"
    )
    if provenance.frozen_map_error:
        out_warnings.append(
            "frozen_map_unavailable: " + str(provenance.frozen_map_error)
        )
    return HostEvidenceRecord(
        enzyme_uid=enzyme_uid,
        source_signature=None,
        host_taxid=None,
        host_name=None,
        host_resolution="UNRESOLVED",
        host_evidence_source=["UNRESOLVED"],
        source_record_id=enzyme_uid,
        evidence_hash=hashlib.sha256(decision_material.encode("utf-8")).hexdigest(),
        warnings=_record_warnings(out_warnings, provenance, "UNRESOLVED"),
        resolution_route=None,
        host_identity_source=None,
    )

# ═══════════════════════════════════════════════════════════════════════════
# G4-R2A §8：下游 host evidence 只消费 microbe_selection_node 的输出
# ═══════════════════════════════════════════════════════════════════════════
def _record_warnings(
    caller_warnings: List[str],
    provenance: EnzymeSourceProvenance,
    route: Optional[str],
) -> List[str]:
    """合并 caller warnings 与 provenance 携带的 warnings（去重、caller 在前），并保证
    冻结 G-SCHEMA hostEvidence.warnings 一定含显式 resolution_route token（schema 只允许
    九个字段，因此路由留痕走 warnings，生产侧对象另有 exclude 字段）。
    """
    merged = list(caller_warnings)
    for item in provenance.warnings:
        if item and item not in merged:
            merged.append(item)
    token = f"resolution_route={route or 'UNRESOLVED'}"
    if token not in merged:
        merged.append(token)
    return merged


def host_evidence_records_from_node_output(
    microbe_candidates: List[MicrobeCandidate],
    organism_candidates: List[OrganismCandidate],
    evidence_records: Optional[List[EvidenceRecord]] = None,
) -> List[HostEvidenceRecord]:
    """把**节点输出**转换为 production host evidence（T6-R3A-R2A §8 唯一合法下游入口）。

    输入全部来自 microbe_selection_node 返回 dict 的现有承载键：
    - microbe_candidates：宿主 identity 路由 + 签名（顺序即 top_uids 内的解析顺序）；
    - organism_candidates[*].per_enzyme_source_provenance：原始证据 + 宿主 identity 字段；
    - evidence_records（state.evidence_chain 中 stage=="microbe" 的记录）：UNRESOLVED ledger。

    纪律：本函数**不**调用 map_enzyme_hosts / query_uniprot_reviewed / _request_bytes，
    也**不**接受另行重查的 provenance map 参数；缺携带事实即显式报错，不回退去再查一次。
    """
    provenance_by_uid: Dict[str, EnzymeSourceProvenance] = {}
    for org in organism_candidates:
        for prov in org.per_enzyme_source_provenance:
            provenance_by_uid.setdefault(prov.enzyme_uid, prov)

    records: List[HostEvidenceRecord] = []
    emitted: set = set()
    for cand in microbe_candidates:
        uid = cand.enzyme_uid
        prov = provenance_by_uid.get(uid)
        if prov is None:
            raise ValueError(
                f"microbe candidate uid {uid!r} carries no provenance in "
                "organism_candidates[*].per_enzyme_source_provenance; refusing to re-query the "
                "mapper (T6-R3A-R2A §8: downstream must consume node output only)"
            )
        if cand.resolution_route != prov.resolution_route:
            raise ValueError(
                f"uid {uid!r}: node self-contradiction, microbe_candidates resolution_route "
                f"{cand.resolution_route!r} != provenance resolution_route "
                f"{prov.resolution_route!r}"
            )
        if (cand.host_identity_source_signature is not None
                and cand.host_identity_source_signature != prov.host_identity_source_signature):
            raise ValueError(
                f"uid {uid!r}: node self-contradiction between microbe_candidates and "
                "per_enzyme_source_provenance host identity signatures"
            )
        records.append(build_host_evidence_record(
            uid, prov, None,
            [f"host_evidence_converted_from=microbe_selection_node output (uid {uid})"],
        ))
        emitted.add(uid)

    # 节点携带但候选列表未列出的已解析 provenance：不静默丢（防御性补全，仍只用节点输出）
    for uid, prov in provenance_by_uid.items():
        if uid in emitted or prov.resolution_route is None:
            continue
        records.append(build_host_evidence_record(
            uid, prov, None,
            [f"host_evidence_converted_from=microbe_selection_node organism_candidates (uid {uid})"],
        ))
        emitted.add(uid)

    for ev in evidence_records or []:
        if ev.stage != "microbe":
            continue
        ledger = (ev.data or {}).get("unresolved_host_ledger")
        if not isinstance(ledger, list):
            continue
        for entry in ledger:
            if not isinstance(entry, dict):
                continue
            uid = str(entry.get("enzyme_uid") or "").strip()
            if not uid or uid in emitted:
                continue
            reasons = [str(r) for r in (entry.get("reasons") or []) if str(r).strip()]
            if not reasons:
                reasons = ["no_reviewed_evidence_and_no_frozen_map_hit"]
            material = (
                f"UNRESOLVED|uid={uid}|source=microbe_selection_node_unresolved_ledger|"
                + "|".join(reasons)
            )
            ledger_warnings = [
                "unresolved_host_ledger consumed from microbe_selection_node output for uid "
                + uid + ": " + ", ".join(reasons),
                "host_resolution=UNRESOLVED: evidence_hash is the SHA256 of the honest "
                "decision material, not of a data response",
                "neither live reviewed UniProt nor the frozen reviewed UID map produced a host "
                "identity; no host fabricated (T6-R3A-R2A §7 Path U)",
            ]
            if entry.get("frozen_map_error"):
                ledger_warnings.append(
                    "frozen_map_unavailable: " + str(entry["frozen_map_error"])
                )
            records.append(HostEvidenceRecord(
                enzyme_uid=uid,
                source_signature=None,
                host_taxid=None,
                host_name=None,
                host_resolution="UNRESOLVED",
                host_evidence_source=["UNRESOLVED"],
                source_record_id=uid,
                evidence_hash=hashlib.sha256(material.encode("utf-8")).hexdigest(),
                warnings=ledger_warnings,
            ))
            emitted.add(uid)
    return records
