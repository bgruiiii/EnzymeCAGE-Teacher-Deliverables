"""F2 shared utilities: hashing, canonical JSON, atomic writes, paths.

Task: F2 (LIKERT_V04_FULL_SCORING_20261029_R0, master contract §7).
This module is offline-only: it performs no network I/O and never reads
environment variable VALUES (only existence checks are allowed, and those
live in the registry builder, not here).
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

# R root per master contract §2
R = Path(os.environ.get("LIKERT_V05_RUN_ROOT", str(Path(__file__).resolve().parents[2] / "data")))
F2_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F2_SCORER_BUILD_R1_2_1"
F0_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F0_INPUT_BASELINE"

# Frozen upstream identities consumed by F2 (values verified at registry build)
F0_INPUT_BASELINE_MANIFEST_SHA = "2771361134b763b28556c7b803801c98f0e0fff8e27064da2b1efee9da3eff65"
MASTER_CONTRACT_SHA = "73dfc012d902f9223cb887fdaaedca22d55860c968572a6d7d65351e203f5844"
TEACHER_REPLY_SHA = "7c0b82092d20ea54a4f1db3c591313f29c55f33c5403f8f730242339e01322ef"
F2_CARD_SHA = "a2d74aeb4cdc7f83143eb4f319f73cc1114529e4d45e43a87c9a8b6d1b62fc2d"
RUBRIC_RATER_CLEAN_TEXT_SHA = "bcf78065c6a56b02e4647de61db20c02ee17526ac4913c40cdaa2b6bca8ca283"
RUBRIC_RATER_CLEAN_DOCX_SHA = "2e4a5f048807d2201e6a3beb0c2d22c40b4d380bfa4a5245706377dd67f81d6e"
SCOPE120_SHA = "4d8c7eab5823695d0a2fe8ac2c263fc1130bc4beb3e308d0ddc92078351cdfeb"
B480_INDEX_SHA = "40c875d9ea945225f6a37d711753321aaf3a9bca0139a38d22ced95d8905d9e3"

# F0-N1 erratum (audit dir): the three stale generator-identity fields in the
# original manifest/rules-manifest/generation-log point at 680847ff…/16256B;
# the actual final frozen script is:
ERRATUM_FINAL_SCOPE_SCRIPT_SHA = "2dce890a528ca61ea32e220e57023d30950d55f5d15db743367ca2315d6024a7"
ERRATUM_SUPERSEDED_SCRIPT_SHA = "680847ff1c38ce797d817afa4ba2d2a8e3b3924a421f113e54fe8b3a715a802c"

DIMENSIONS = ["D1", "D2", "D3a", "D3b", "D4", "D5", "D6"]
WEIGHTS = {"D1": 15, "D2": 25, "D3a": 10, "D3b": 10, "D4": 15, "D5": 15, "D6": 10}
SCORE_STATUS_ENUM = ["SCORED", "MISSING", "NE", "NA"]
D5_SIX_STATES = [
    "MISSING_SOURCE",
    "GENERIC_SOURCE",
    "UNRESOLVED_SOURCE",
    "VERIFIED_MIS_CITATION_LOCAL",
    "VERIFIED_MIS_CITATION_CRITICAL",
    "VERIFIED_MIS_CITATION_SYSTEMIC",
]
D5_SEVERITY_ENUM = [
    "NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION",
    "NA",
    "LOCAL",
    "CRITICAL",
    "SYSTEMIC",
]
# Mis-citation severity ordering is ONLY defined among these four (rubric R15:
# the NA<LOCAL<CRITICAL<SYSTEMIC order applies to mis-citation severity alone;
# the six source states have no total order).
MISCITATION_SEVERITY_ORDER = {"LOCAL": 1, "CRITICAL": 2, "SYSTEMIC": 3}
FACT_STATUS_ENUM = ["SUPPORTED", "CONTRADICTED", "UNRESOLVED"]
COVERAGE_MAIN_ENUM = ["已给出", "部分给出", "明确未知", "未提供", "任务不要求"]
COVERAGE_SOURCE_ENUM = ["已给出", "部分给出", "未提供"]
CONFIDENCE_ENUM = ["高", "中", "低"]
KEY_ERROR_ENUM = ["Y", "N", "UNRESOLVED"]
SYSTEM_RUN_STATUS_ENUM = [
    "OK",
    "NOT_RUN",
    "FAILED_HTTP_AUTH_401_403",
    "FAILED_HTTP_429_EXHAUSTED",
    "FAILED_HTTP_5XX_EXHAUSTED",
    "FAILED_HTTP_OTHER",
    "FAILED_TIMEOUT",
    "FAILED_INVALID_JSON",
    "FAILED_SCHEMA_VALIDATION",
    "FAILED_MODEL_DRIFT",
    "FAILED_BUDGET_STOP",
    "FAILED_INPUT_IDENTITY_MISMATCH",
    "FAILED_DUAL_RESULT_QUARANTINED",
    "UNKNOWN_INFLIGHT",
]
TRAITS_REQUIRED_COUNT = 15  # answer schema v2 definitions/traits required F1..F15

CG_PREDEFINITION_GROUPS = [
    "CG01_路线核心步骤（主链转化序列与顺序）",
    "CG02_路线起点（入口底物与首步转化）",
    "CG03_路线终点（题面指定终点）",
    "CG04_氧与氧化还原条件（路线条件体系）",
    "CG05_酶-反应对应与关键EC（核心步骤酶）",
    "CG06_非核心步骤酶候选与家族级标注",
    "CG07_核心微生物身份（菌名/菌株/保藏号/TaxID三件套）",
    "CG08_步级微生物归属（单步催化剂归属）",
    "CG09_完整路径能力声称（PATHWAY_COMPLETE/全路径菌）",
    "CG10_性状：氧需求",
    "CG11_性状：温度（最适/范围）",
    "CG12_性状：pH",
    "CG13_性状：盐度",
    "CG14_性状：底物利用谱/碳源",
    "CG15_一般形态/分类性状（革兰氏、产孢、运动性、形态）",
    "CG16_栖息地/生态来源描述",
    "CG17_基因组/序列登录号",
    "CG18_文献书目信息（作者/年份/期刊/卷期页/DOI）",
    "CG19_非核心子声称（方法说明、背景、数据库版本声明）",
    "CG20_不确定性与置信度标签",
]
CG_ID_PATTERN_LEN = 4  # "CGnn"

# Case-level unresolved registration (F0-UQ-001): BIOPATH150_013 CG04/CG10 stay
# UNRESOLVED; downstream must not coerce to TRUE/FALSE or drop the case.
UNRESOLVED_SCOPE_CASE = "BIOPATH150_013"
UNRESOLVED_SCOPE_CGS = {"CG04", "CG10"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj) -> str:
    """Deterministic JSON serialization used for all identity hashes."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def sha256_canonical(obj) -> str:
    return sha256_bytes(canonical_json(obj).encode("utf-8"))


def atomic_write_bytes(path, data: bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_f2_")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, str(path))
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def atomic_write_text(path, text: str) -> None:
    atomic_write_bytes(path, text.encode("utf-8"))


def atomic_write_json(path, obj) -> None:
    atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=2,
                                       allow_nan=False) + "\n")


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def utc_now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def is_pure_int(v) -> bool:
    """True only for real integers. Rejects bool, float (even 7.0), str '7',
    NaN/Inf — the truthy-string / numeric-leak counterexamples from contract
    §6 acceptance and §7.3 numeric rules."""
    return isinstance(v, int) and not isinstance(v, bool)

# ---------------------------------------------------------------------------
# R1 additions (audit F2-P1-05 / F2-P2-01)

SCHEMA_ID_R1 = "LIKERT_V04_AI_RATING_OUTPUT_SCHEMA_R1"

# F3 E0 interface (E0_INTERFACE_CONTRACT_R1.md): files the adapter consumes
# from an F3 evidence package, with required columns for schema-compat checks.
F3_REQUIRED_FILES = {
    "NORMALIZED_RECORDS.jsonl": None,  # jsonl; required record keys below
    "CLAIM_REGISTRY.tsv": ["claim_id", "case_ids"],
    "VERIFICATION_RESULTS.tsv": ["claim_id", "official_record_ids"],
}
F3_RECORD_REQUIRED_KEYS = ["record_id", "record_class", "record_type",
                           "canonical_identifier", "source_files"]
# Optional-but-expected annotation keys; absence is disclosed per record in
# the slice (never silently rewritten, never a whole-package rejection):
F3_RECORD_DISCLOSED_OPTIONAL_KEYS = ["support_scope_note", "record_status"]
# Keys that must never appear in rater-facing evidence records (leak defense;
# F3 manifest declares NORMALIZED_RECORDS as the sanitized rater-facing layer)
F3_FORBIDDEN_RECORD_KEYS = {"model_config", "tested_model", "model_identity",
                            "program_score", "historical_score", "ranking",
                            "key_error", "ke_verdict", "third_person_score",
                            "adjudication", "rater_id", "human_attestation"}


def totals_contract(dims: dict) -> dict:
    """SINGLE lossless totals contract shared by validator, runner canonical
    records and TSV projection (audit F2-P1-05: all three layers must use the
    same algorithm; MISSING=1 participates with weight retained, rubric 五/P78;
    NE/NA → NOT_COMPARABLE, never renormalized).

    Returns dict:
      status: COMPARABLE | NOT_COMPARABLE | INCOMPLETE
      values: {dim: int} for SCORED/MISSING dims (MISSING contributes 1)
      ne_na_dims: [dims with NE/NA]
      incomplete_dims: [dims missing/illegal status or score]
      weighted_total / scientific_subscore: float when COMPARABLE else None
    """
    values = {}
    ne_na = []
    incomplete = []
    for d in DIMENSIONS:
        dim = dims.get(d) if isinstance(dims, dict) else None
        if not isinstance(dim, dict):
            incomplete.append(d)
            continue
        st = dim.get("score_status")
        sc = dim.get("score")
        if st == "SCORED":
            if is_pure_int(sc) and 1 <= sc <= 10:
                values[d] = sc
            else:
                incomplete.append(d)
        elif st == "MISSING":
            if sc == 1 and is_pure_int(sc):
                values[d] = 1
            else:
                incomplete.append(d)
        elif st in ("NE", "NA"):
            ne_na.append(d)
        else:
            incomplete.append(d)
    out = {"values": values, "ne_na_dims": ne_na, "incomplete_dims": incomplete,
           "weighted_total": None, "scientific_subscore": None}
    if incomplete:
        out["status"] = "INCOMPLETE"
        return out
    if ne_na:
        out["status"] = "NOT_COMPARABLE"
        return out
    out["status"] = "COMPARABLE"
    out["weighted_total"] = round(
        1.5 * values["D1"] + 2.5 * values["D2"] + values["D3a"] + values["D3b"]
        + 1.5 * values["D4"] + 1.5 * values["D5"] + values["D6"], 10)
    out["scientific_subscore"] = round(
        (25 * values["D2"] + 10 * values["D3a"] + 10 * values["D3b"]
         + 15 * values["D4"]) / 60.0, 10)
    return out
