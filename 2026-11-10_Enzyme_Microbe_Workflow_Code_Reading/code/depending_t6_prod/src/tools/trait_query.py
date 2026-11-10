# src/tools/trait_query.py
# T5B: C8 只读性状注释 adapter（替换旧 M4b 空实现）。
#
# 确定性链:
#   enzyme UID -> 权威 UID CSV 精确等值 -> source_signature
#   -> C8-1 (source_signature, trait_id) 精确匹配 -> 每 source_signature 恰好 F1-F15
#   -> HostTraitAnnotation (G-SCHEMA trait 镜像) + 兼容 TraitRecord
#
# 红线: 无在线 API、无名称/TaxID 模糊匹配、无 PREDICTED、无排序/过滤/打分、
#       无 confidence / trait_score / total_score / reranked_rank。

import csv
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from src.schemas.evidence import HostTraitAnnotation, TraitEvidence, TraitRecord

logger = logging.getLogger(__name__)

F_TRAITS = [f"F{i}" for i in range(1, 16)]
SOURCE_TOOL = "c8_trait_annotation_readonly"


class C8AssetError(RuntimeError):
    """C8-1 / UID CSV 资产身份或完整性失败（fail-closed）。"""


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _evidence_hash(trait_id: str, evidence_class: str, value_norm: str,
                   source_record_id: str, resolution: str) -> str:
    payload = "\n".join([str(x) for x in (trait_id, evidence_class, value_norm,
                                          source_record_id, resolution, SOURCE_TOOL)])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class C8TraitAdapter:
    """只读 adapter：一次流式扫描 UID CSV + 一次加载 37,170 行 C8 lookup 索引。"""

    def __init__(self, lookup_root: str, uid_map_path: str):
        self.lookup_root = Path(lookup_root)
        self.uid_map_path = Path(uid_map_path)
        self.lookup_root_sha = ""
        self.uid_map_sha = ""
        self.uid_to_sources: Dict[str, List[dict]] = {}
        self.lookup_index: Dict[Tuple[str, str], dict] = {}
        self._load()

    def _load(self):
        lookup_root = self.lookup_root
        uid_map = self.uid_map_path
        if not lookup_root.is_dir():
            raise C8AssetError("C8_LOOKUP_ROOT missing or not a directory")
        if uid_map.is_symlink() or lookup_root.is_symlink():
            raise C8AssetError("C8 asset path must not be a symlink")
        if not uid_map.is_file():
            raise C8AssetError("C8_UID_SOURCE_MAP_PATH missing or not a regular file")
        index_jsonl = lookup_root / "C8_METATRAITS_LOOKUP_INDEX.jsonl"
        if not index_jsonl.is_file() or index_jsonl.is_symlink():
            raise C8AssetError("C8_METATRAITS_LOOKUP_INDEX.jsonl missing inside C8_LOOKUP_ROOT")
        # ── 固定资产 SHA/bytes 门（先于内容读取）──
        EXPECT_UID_BYTES = 104025134
        EXPECT_UID_SHA = "7b92e8e625cb73f070c8e902687ea5bbdbf749f04a19828e550e3fe205684fe6"
        EXPECT_LOOKUP_SHA = "d51a540db2f9798d65e25b46f22960ba29ae2d4b288be218c83c299f24f5d5af"
        if uid_map.stat().st_size != EXPECT_UID_BYTES:
            raise C8AssetError(f"UID map bytes != {EXPECT_UID_BYTES}")
        measured_uid_sha = _sha256_file(uid_map)
        if measured_uid_sha != EXPECT_UID_SHA:
            raise C8AssetError(f"UID map SHA256 != expected {EXPECT_UID_SHA[:16]}...")
        measured_lookup_sha = _sha256_file(index_jsonl)
        if measured_lookup_sha != EXPECT_LOOKUP_SHA:
            raise C8AssetError(f"lookup index SHA256 != expected {EXPECT_LOOKUP_SHA[:16]}...")
        # 一次加载 lookup 索引；校验 37,170 行与 (sig,trait) 唯一性
        n = 0
        pairs = set()
        group_by_sig_traits: Dict[str, set] = {}
        with open(index_jsonl, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                n += 1
                row = json.loads(line)
                sig = row.get("source_signature", "")
                tid = row.get("trait_id", "")
                if not sig or not tid:
                    raise C8AssetError("lookup row missing source_signature/trait_id")
                pair = (sig, tid)
                if pair in pairs:
                    raise C8AssetError(f"lookup (source_signature, trait_id) not unique: {pair}")
                pairs.add(pair)
                self.lookup_index[pair] = row
                group_by_sig_traits.setdefault(sig, set()).add(tid)
        if n != 37170:
            raise C8AssetError(f"lookup rows != 37170 (got {n})")
        for sig, tids in group_by_sig_traits.items():
            if tids != set(F_TRAITS):
                raise C8AssetError(f"source_signature {sig[:40]} has trait set {sorted(tids)}")
        # 一次流式扫描 UID CSV；只收集与请求相关的行在 query 阶段按需过滤，
        # 但为校验完整性这里记录总行数门槛（本实现扫描一次并在查询时复用内存行）。
        self._uid_rows: Dict[str, List[dict]] = {}
        n_uid = 0
        self.uid_header_ok = False
        with open(uid_map, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.uid_header_ok = reader.fieldnames is not None and reader.fieldnames == [
                "UniprotID","TaxID","organism_name","lineage","reviewed","gene_primary",
                "proteome_raw","proteome_id_list","proteome_id","proteome_count",
                "proteome_organism","proteome_organism_id","proteome_strain_name","strain_name",
                "proteome_type","genome_assembly_from_proteome","genome_assembly_level",
                "genome_assembly_source","source_signature","source_resolution_level",
                "is_ambiguous","source_db","mapping_confidence","query_status",
                "taxonomy_group","keep_bacteria_fungi_archaea",
            ]
            for row in reader:
                n_uid += 1
                uid = (row.get("UniprotID") or "").strip()
                if not uid:
                    raise C8AssetError("UID CSV row with empty UniprotID")
                self._uid_rows.setdefault(uid, []).append(dict(row))
        if not self.uid_header_ok:
            raise C8AssetError("UID CSV header mismatch (expected 26-column authority header)")
        if n_uid != 168335:
            raise C8AssetError(f"UID CSV rows != 168335 (got {n_uid})")

    # ── 查询入口 ──
    def annotate(self, organism_candidates) -> Tuple[List[HostTraitAnnotation], Dict]:
        """从 organism_candidates 的 supporting_enzymes[].uid 构建注释。

        Returns (annotations, evidence_meta)。不改变、不排序任何候选。
        """
        seen_uids: List[str] = []
        seen_set = set()
        uid_to_hosts: Dict[str, List[dict]] = {}
        for cand in organism_candidates or []:
            for sup in cand.supporting_enzymes:
                uid = sup.uid
                if uid not in seen_set:
                    seen_set.add(uid)
                    seen_uids.append(uid)
                has_reviewed = False
                for prov in (cand.per_enzyme_source_provenance or []):
                    if prov.enzyme_uid == uid and prov.uniprot_reviewed is not None:
                        has_reviewed = True
                        break
                uid_to_hosts.setdefault(uid, []).append({
                    "organism_uid": cand.organism_uid,
                    "tax_id": cand.ncbi_taxon_id,
                    "organism_name": cand.organism_name,
                    "reviewed": has_reviewed,
                })
        annotations: List[HostTraitAnnotation] = []
        not_mapped: List[str] = []
        mult_source_uids: List[str] = []
        mapped_sigs = set()
        for uid in seen_uids:
            rows = self._uid_rows.get(uid, [])
            if not rows:
                not_mapped.append(uid)
                annotations.append(_unresolved_annotation(uid))
                continue
            if len(rows) > 1:
                mult_source_uids.append(uid)
            for row in rows:
                sig = (row.get("source_signature") or "").strip()
                mapped_sigs.add(sig if sig else f"EMPTY_{uid}")
                annotations.append(self._annotate_one(uid, row, uid_to_hosts.get(uid, [])))
        evidence_meta = {
            "unique_enzyme_uids": len(seen_uids),
            "mapped_uids": len(seen_uids) - len(not_mapped),
            "not_mapped_uids": not_mapped,
            "multi_source_uids": mult_source_uids,
            "unique_source_signatures": len({a.source_signature for a in annotations if a.source_signature != "NOT_MAPPED"}),
            "asset_hashes": {
                "uid_map_sha256": _sha256_file(self.uid_map_path),
                "lookup_index_sha256": _sha256_file(self.lookup_root / "C8_METATRAITS_LOOKUP_INDEX.jsonl"),
            },
        }
        return annotations, evidence_meta

    def _annotate_one(self, uid: str, row: dict, hosts: List[dict]) -> HostTraitAnnotation:
        sig = (row.get("source_signature") or "").strip()
        strain = (row.get("strain_name") or "").strip() or (row.get("proteome_strain_name") or "").strip()
        taxid_raw = (row.get("TaxID") or "").strip()
        taxid: Optional[int] = None
        if taxid_raw.isdigit() and int(taxid_raw) > 0:
            taxid = int(taxid_raw)
        org = (row.get("organism_name") or "").strip() or (row.get("species_name_or_guess") or "").strip()
        # host resolution 保守转换
        if strain:
            resolution = "EXACT_STRAIN"
        elif taxid and org:
            resolution = "SPECIES"
        else:
            resolution = "UNRESOLVED"
        traits: Dict[str, TraitEvidence] = {}
        warnings: List[str] = []
        taxonomy_group = (row.get("taxonomy_group") or "").strip() or None
        for tid in F_TRAITS:
            lrow = self.lookup_index.get((sig, tid))
            if lrow is None:
                raise C8AssetError(f"lookup missing ({sig[:40]}, {tid})")
            traits[tid] = self._trait_evidence(sig, lrow, warnings, resolution, taxonomy_group)
        host_ref = hosts[0] if hosts else {}
        reviewed_any = host_ref.get("reviewed", False)
        # frozen host evidence source enum: only UNIPROT_REVIEWED when the source candidate
        # really carries UniProt reviewed host provenance; otherwise UNRESOLVED (never guessed).
        host_evidence_sources = ["UNIPROT_REVIEWED"] if reviewed_any else ["UNRESOLVED"]
        return HostTraitAnnotation(
            enzyme_uid=uid,
            source_signature=sig,
            host_taxid=taxid,
            host_name=org or None,
            host_resolution=resolution,
            host_taxonomy_group=taxonomy_group,
            host_evidence_sources=host_evidence_sources,
            traits=traits,
            warnings=warnings,
        )

    def _trait_evidence(self, sig: str, lrow: dict, warnings: List[str],
                        host_resolution: str, taxonomy_group) -> TraitEvidence:
        tid = lrow["trait_id"]
        taxonomy = lrow.get("taxonomy_group", "")
        observed_available = bool(lrow.get("observed_available"))
        matched = ((lrow.get("matched_observed_examples") or "").strip())
        warning_list: List[str] = []
        if bool(lrow.get("predicted_soft_fill_candidate_available")):
            warning_list.append("predicted_candidate_present_but_not_activated")
            warnings.append(f"{tid}:predicted_candidate_present_but_not_activated")
        if taxonomy == "target_fungi":
            evidence_class = "IDENTITY_ONLY"
            value = None
            trait_resolution = "IDENTITY_ONLY"
        elif observed_available:
            parsed = _conservative_structured_value(matched)
            if not parsed:
                # conservative semantics: observed flag set but no parseable content -> MISSING + warning
                evidence_class = "MISSING"
                value = None
                warning_list.append("observed_available_flag_set_but_no_parseable_content")
            else:
                evidence_class = "OBSERVED"
                value = parsed
            # non-fungi mapped: resolution never above host resolution
            trait_resolution = host_resolution if host_resolution in ("EXACT_STRAIN", "SPECIES") else "UNRESOLVED"
        else:
            evidence_class = "MISSING"
            value = None
            trait_resolution = host_resolution if host_resolution in ("EXACT_STRAIN", "SPECIES") else "UNRESOLVED"
        value_norm = json.dumps(value, sort_keys=True, ensure_ascii=False) if value is not None else "<null>"
        return TraitEvidence(
            trait_id=tid,
            trait_value=value,
            trait_evidence_class=evidence_class,
            trait_resolution=trait_resolution,
            trait_source=lrow.get("source_type_preview") or "c8_1_lookup",
            source_record_id=f"{sig}|{tid}",
            source_tool=SOURCE_TOOL,
            model_version=None,
            evidence_hash=_evidence_hash(tid, evidence_class, value_norm, f"{sig}|{tid}",
                                         trait_resolution),
            used_for_hard_filtering=False,
            used_for_ranking=False,
            direct_target_degradation_claim=False,
            trait_warning=warning_list,
        )


def _conservative_structured_value(matched: str):
    """matched_observed_examples 仅按实际分号分隔；trim、去空、首见去重。
    逗号不是分隔符，不得把逗号当分隔符。"""
    if not matched:
        return []
    parts = [p.strip() for p in matched.split(";") if p.strip()]
    return list(dict.fromkeys(parts))


def _unresolved_annotation(uid: str) -> HostTraitAnnotation:
    traits = {}
    for tid in F_TRAITS:
        traits[tid] = TraitEvidence(
            trait_id=tid, trait_value=None, trait_evidence_class="MISSING",
            trait_resolution="UNRESOLVED", trait_source="uid_to_source_keep_bacteria_fungi_archaea",
            source_record_id=f"NOT_MAPPED:{uid}", source_tool=SOURCE_TOOL,
            evidence_hash=_evidence_hash(tid, "MISSING", "<null>", f"NOT_MAPPED:{uid}", "UNRESOLVED"),
            trait_warning=[],
        )
    return HostTraitAnnotation(
        enzyme_uid=uid, source_signature="NOT_MAPPED",
        host_resolution="UNRESOLVED",
        host_evidence_sources=["UNRESOLVED"],
        traits=traits,
        warnings=["NOT_MAPPED: enzyme UID has no row in authority UID CSV; explicit UNRESOLVED, not silently dropped"],
    )


# ── 兼容壳（旧函数名保留，但语义已替代为 T5B 只读注释；不再有 allowlist/TaxID 模糊查询）──

def _assets_from_env() -> C8TraitAdapter:
    from config.settings import C8_LOOKUP_PATH, C8_UID_SOURCE_MAP_PATH
    return C8TraitAdapter(C8_LOOKUP_PATH, C8_UID_SOURCE_MAP_PATH)


def query_traits(tax_ids=None, traits=None):
    raise NotImplementedError(
        "query_traits(TaxID fuzzy) has been superseded by T5B c8_trait_annotation_readonly: "
        "use C8TraitAdapter.annotate(organism_candidates) with the authority UID CSV exact match. "
        "No online API / name matching / TaxID approximation is permitted.")


def apply_soft_filter(trait_records, candidates):
    # 保留 soft 语义：T5B 决策同样不做硬过滤，仅由注释携带状态。
    return candidates


def build_trait_annotations(organism_candidates, c8_lookup_root=None, uid_map_path=None):
    """便捷入口：从候选立即构建注释；资产路径可显式传入，否则读环境变量。"""
    if c8_lookup_root is None or uid_map_path is None:
        adapter = _assets_from_env()
    else:
        adapter = C8TraitAdapter(c8_lookup_root, uid_map_path)
    return adapter.annotate(organism_candidates)


def validate_host_evidence_sources(sources: list) -> List[str]:
    """生产同源 host 层 predicate：非空、唯一、仅允许冻结四枚举。"""
    problems: List[str] = []
    if not isinstance(sources, list) or not sources:
        problems.append("host_evidence_sources empty or not array")
    if len(set(sources)) != len(sources):
        problems.append("host_evidence_sources not unique")
    for s in sources:
        if s not in ("UNIPROT_REVIEWED", "KEGG_SUPPLEMENT", "BACDIVE_OBSERVED", "UNRESOLVED"):
            problems.append(f"unknown host evidence source {s}")
    if "uid_to_source_keep_bacteria_fungi_archaea" in sources:
        problems.append("uid map filename must not be used as host evidence source")
    return problems


def validate_annotation_semantics(ann) -> List[str]:
    """生产同源语义门（mutation harness 与 final validator 共用）。返回问题列表，空则为通过。"""
    problems: List[str] = validate_host_evidence_sources(ann.host_evidence_sources)
    if list(ann.traits.keys()) != F_TRAITS:
        problems.append("F1-F15 keys incomplete")
    if ann.traits.get("F5") and ann.traits["F5"].trait_evidence_class == "PREDICTED":
        problems.append("F5 predicted")
    if ann.traits.get("F8") and (ann.traits["F8"].direct_target_degradation_claim
                                 or ann.traits["F8"].used_for_ranking):
        problems.append("F8 direct claim or ranking")
    if ann.traits.get("F15") and ann.traits["F15"].used_for_ranking:
        problems.append("F15 used for ranking")
    for ev in ann.traits.values():
        if ev.used_for_hard_filtering:
            problems.append("hard filtering flag")
        if not isinstance(ev.trait_warning, list):
            problems.append("trait_warning not array")
        if ev.trait_resolution not in ("EXACT_STRAIN","SPECIES","REPRESENTATIVE_STRAIN","IDENTITY_ONLY","UNRESOLVED"):
            problems.append(f"bad trait_resolution {ev.trait_resolution}")
    if ann.host_taxonomy_group == "target_fungi":
        for ev in ann.traits.values():
            if ev.trait_evidence_class != "IDENTITY_ONLY" or ev.trait_resolution != "IDENTITY_ONLY":
                problems.append("fungi must be IDENTITY_ONLY")
    else:
        for ev in ann.traits.values():
            if ev.trait_resolution not in (ann.host_resolution, "UNRESOLVED", "IDENTITY_ONLY"):
                problems.append(f"trait resolution {ev.trait_resolution} above host {ann.host_resolution}")
    return problems


def trait_records_from_annotations(annotations) -> List[TraitRecord]:
    """从同一确定性注释生成兼容 trait_records（同源，不得一真一假）。"""
    records: List[TraitRecord] = []
    for ann in annotations:
        for tid in F_TRAITS:
            ev = ann.traits.get(tid)
            if ann.source_signature == "NOT_MAPPED":
                continue
            records.append(TraitRecord(
                trait_name=tid,
                value=ev.trait_value,
                is_ai=False,
                majority_label=ev.trait_evidence_class,
                source_database="C8_METATRAITS_LOOKUP_INDEX",
                source_url=None,
                tax_id=ann.host_taxid,
            ))
    return records
