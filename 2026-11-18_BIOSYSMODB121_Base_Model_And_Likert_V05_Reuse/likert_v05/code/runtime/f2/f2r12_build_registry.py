"""Build R1.2.1 input identity registry (BEFORE/AFTER closure per hotfix card).

Registers every read-only input the R1.2 recovery-only repair consumes and
VERIFIES the R1.1 baseline (50-item SUMS + the 32 F4-R1.1-card artifact
bindings) as required by the card. Scientific artifacts (prompt/template/
schema) and the F3 R1.1 evidence binding are asserted BYTE-IDENTICAL to
R1.1 — this round changes recovery code only.

Usage:
  python3 f2r12_build_registry.py BEFORE|AFTER

Offline: no network, no model API. Env var VALUES never read (existence only).
"""
from __future__ import annotations

import json
import os
import platform
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (R, F2_DIR, sha256_file, atomic_write_json, utc_now_iso,
                          F0_INPUT_BASELINE_MANIFEST_SHA, MASTER_CONTRACT_SHA,
                          TEACHER_REPLY_SHA)

BASE = R / "LIKERT_V04_FULL_SCORING_20261029"
R0_DIR = BASE / "F2_SCORER_BUILD"
R1_DIR = BASE / "F2_SCORER_BUILD_R1"
R11_DIR = BASE / "F2_SCORER_BUILD_R1_1"
R12_DIR = F2_DIR
F0_DIR = BASE / "F0_INPUT_BASELINE"
F3R11_DIR = BASE / "F3_EVIDENCE_R1_1"
REAUDIT = R / "04_Local_Review_Audits" / "LIKERT_V04_FULL_SCORING_20261029" / "F2_R1_1_INDEPENDENT_REAUDIT_20261030"
R12_DIR_PREV = BASE / "F2_SCORER_BUILD_R1_2"
REAUDIT_R12 = R / "04_Local_Review_Audits" / "LIKERT_V04_FULL_SCORING_20261029" / "F2_R1_2_INDEPENDENT_RECOVERY_REAUDIT_20261030"
AUTH = R / "00_Authority_Teacher_Plan"
PROMPTS = R / "07_HPC_Prompts"

IMMUTABLE_INPUTS = [
    # hotfix authority (R1.2.1)
    ("r1_2_1_hotfix_card", PROMPTS / "LOCAL_AI_LIKERT_V04_F2_R1_2_1_ARCHIVE_IDENTITY_GATE_HOTFIX_EXECUTOR_ONLY_20261030.md",
     "adadcf0f4a356ce6d45cdc2d2163cad93a66726e0bae422cdecac6332b444aa0"),
    ("r1_2_recovery_reaudit_report", REAUDIT_R12 / "F2_R1_2_INDEPENDENT_RECOVERY_REAUDIT_REPORT.md",
     "bce7caf2306f910fc443a9d279b59ac03275a1ca69f6afa237d7086b28f1d085"),
    ("r1_2_recovery_reaudit_results", REAUDIT_R12 / "AUDIT_RESULTS.json", None),
    ("r1_2_cross_config_repro", REAUDIT_R12 / "CROSS_CONFIG_ARCHIVE_REPRO.json", None),
    ("r1_2_reaudit_script_main", REAUDIT_R12 / "audit_f2_r1_2.py", None),
    ("r1_2_reaudit_script_crosscfg", REAUDIT_R12 / "audit_cross_config_archive.py", None),
    # previous round authority (R1.2)
    ("r1_2_repair_card", PROMPTS / "LOCAL_AI_LIKERT_V04_F2_R1_2_ARCHIVE_AND_TRUNCATED_TAIL_RECOVERY_ONLY_EXECUTOR_ONLY_20261030.md",
     "e7380f61263c1692d399c0b9530466bb9fb9d1d9a70cf9a9303713191e2c0461"),
    ("r1_2_repair_report", R12_DIR_PREV / "F2_R1_2_RECOVERY_REPAIR_REPORT.md", None),
    ("r1_2_f4_card", PROMPTS / "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_2_20261030.md",
     "69cc205d105109cc91469f723bd9bbd034b0d153a2c6b02fa38d343925c92fb6"),
    # R1.1 authority
    ("r1_1_repair_card", PROMPTS / "LOCAL_AI_LIKERT_V04_F2_R1_1_RUNTIME_CLOSURE_AND_APPROVED_E0_REBIND_EXECUTOR_ONLY_20261029.md",
     "d5580989a5c02787c65ec137c6f2b59315e5f480c468efeb23cc511422ebaded"),
    ("r1_1_reaudit_report", REAUDIT / "F2_R1_1_INDEPENDENT_REAUDIT_REPORT.md",
     "d610c625c4e9c328b7b70596cd72afb3c81daa690b64de79b0c27f6f84e5465a"),
    ("r1_1_reaudit_results", REAUDIT / "AUDIT_RESULTS.json", None),
    ("r1_1_reaudit_wire_repro", REAUDIT / "COMPLETE_WIRE_RECOVERY_REPRO.json",
     "63403031e81d77ca42c5bf16f3e81083aaa5852d34f7a9990b9c250db12bc6b6"),
    ("r1_1_reaudit_script_main", REAUDIT / "audit_f2_r1_1.py", None),
    ("r1_1_reaudit_script_wire", REAUDIT / "audit_complete_wire_recovery.py", None),
    # upper authority
    ("master_contract", AUTH / "MASTER_CONTRACT_LIKERT_V04_FULL_SCORING_AND_HUMAN_ANCHORS_20261029.md",
     MASTER_CONTRACT_SHA),
    ("teacher_reply_1028", AUTH / "TEACHER_REPLY_LIKERT_V04_FULL_SCORING_AUTHORIZATION_2026-10-28.md",
     TEACHER_REPLY_SHA),
    ("f0_input_baseline_manifest", F0_DIR / "INPUT_BASELINE_MANIFEST.json",
     F0_INPUT_BASELINE_MANIFEST_SHA),
    # previous F2 rounds (read-only)
    ("r1_1_repair_report", R11_DIR / "F2_R1_1_REPAIR_REPORT.md", None),
    ("r1_1_f4_card", PROMPTS / "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_1_20261029.md",
     "014e9132ef1e32f9d64735c09c7093f1e1b5a765857d3a441902374f921bca98"),
    # R1.1 scientific artifacts — must be BYTE-IDENTICAL in R1.2 (card §1)
    ("r1_1_system_prompt", R11_DIR / "SCORING_SYSTEM_PROMPT.txt",
     "0829ae541b6e0c089e4d7bcf92f927f43507ee7230c244cb467c1faf98956dea"),
    ("r1_1_item_template", R11_DIR / "ITEM_MESSAGE_TEMPLATE.txt",
     "4534bda6f8177cca958ccaf09fe4cdab52e8b4ae50bad14e7dbf364adcc009a6"),
    ("r1_1_rating_schema", R11_DIR / "RATING_OUTPUT_SCHEMA.json",
     "c387ba77e9958306babb94078a1fb57cc96246a00d2dcfc658cf6b1a6349a0f9"),
    # audited F3 R1.1 evidence package (binding unchanged this round)
    ("f3_r1_1_manifest", F3R11_DIR / "EVIDENCE_MANIFEST_R1_1.json",
     "7e54df82ea49a54916ad523bea924b82d44576691d2ad35448947ae6021af95e"),
    ("f3_r1_1_case_evidence_manifest", F3R11_DIR / "CASE_EVIDENCE_MANIFEST.json",
     "1615849e26361ba1b274aa33025382688116c7d184c189880725a2416cef327d"),
    ("f3_r1_1_interface_doc", F3R11_DIR / "F3_TO_F2_INTERFACE.md", None),
]


def verify_sums(root, sums_name="SHA256SUMS") -> dict:
    sums_path = os.path.join(str(root), sums_name)
    n_ok = n_bad = 0
    bad = []
    with open(sums_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            sha, _, rel = line.split(" ", 2)
            rel = rel.lstrip("*")
            p = os.path.join(str(root), rel)
            if os.path.exists(p) and sha256_file(p) == sha:
                n_ok += 1
            else:
                n_bad += 1
                bad.append(rel)
    return {"entries": n_ok + n_bad, "ok": n_ok, "mismatch": n_bad, "bad": bad[:10]}


def verify_r11_card_bindings() -> dict:
    idp = PROMPTS / "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_1_20261029.md.identity.json"
    ident = json.load(open(idp, encoding="utf-8"))
    n_ok = n_bad = 0
    for label, info in ident["bound_r1_1_artifacts"].items():
        rel = label.split("(")[0]
        p = os.path.join(str(R11_DIR), rel)
        if rel == "RULE_TO_VALIDATOR_MATRIX.tsv":
            p = os.path.join(str(R0_DIR), rel)
        if os.path.exists(p) and sha256_file(p) == info["sha256"]:
            n_ok += 1
        else:
            n_bad += 1
    return {"bindings": n_ok + n_bad, "ok": n_ok, "mismatch": n_bad}


def verify_science_byte_identity() -> dict:
    """Hotfix card §3: prompt/template/schema byte-identical to R1.2 AND R1.1."""
    out = {}
    for name in ("SCORING_SYSTEM_PROMPT.txt", "ITEM_MESSAGE_TEMPLATE.txt",
                 "RATING_OUTPUT_SCHEMA.json"):
        a = sha256_file(R12_DIR / name)
        b = sha256_file(R12_DIR_PREV / name)
        c = sha256_file(R11_DIR / name)
        out[name] = {"r1_2_1_sha256": a, "r1_2_sha256": b, "r1_1_sha256": c,
                     "identical": a == b == c}
    return out


def verify_r12_card_bindings() -> dict:
    idp = PROMPTS / "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_2_20261030.md.identity.json"
    ident = json.load(open(idp, encoding="utf-8"))
    n_ok = n_bad = 0
    for label, info in ident["bound_r1_2_artifacts"].items():
        rel = label.split("(")[0]
        p = os.path.join(str(R12_DIR_PREV), rel)
        if rel == "RULE_TO_VALIDATOR_MATRIX.tsv":
            p = os.path.join(str(R0_DIR), rel)
        elif rel.startswith("COST_AND_CALL_PLAN_R1_1.md") or rel.startswith("E0_INTERFACE_CONTRACT_R1_1.md"):
            p = os.path.join(str(R11_DIR), rel)
        if os.path.exists(p) and sha256_file(p) == info["sha256"]:
            n_ok += 1
        else:
            n_bad += 1
    return {"bindings": n_ok + n_bad, "ok": n_ok, "mismatch": n_bad}


def main(phase: str) -> int:
    assert phase in ("BEFORE", "AFTER")
    entries = []
    mismatch = []
    for role, path, exp in IMMUTABLE_INPUTS:
        e = {"role": role, "path": str(path)}
        if not os.path.exists(path):
            e["exists"] = False
            mismatch.append({"role": role, "problem": "MISSING"})
            entries.append(e)
            continue
        sha = sha256_file(path)
        e.update({"exists": True, "sha256": sha, "bytes": os.path.getsize(path)})
        if exp and sha != exp:
            e["expected_sha256"] = exp
            mismatch.append({"role": role, "problem": "SHA_MISMATCH", "actual": sha})
        entries.append(e)

    env_names = ["DASHSCOPE_API_KEY", "BAILIAN_API_KEY", "OPENAI_API_KEY",
                 "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "MOONSHOT_API_KEY",
                 "ZHIPU_API_KEY"]
    env_existence = {n: (n in os.environ) for n in env_names}

    science = verify_science_byte_identity()
    r12_sums = verify_sums(R12_DIR_PREV)
    r12_cards = verify_r12_card_bindings()
    r11_sums = verify_sums(R11_DIR)
    r11_cards = verify_r11_card_bindings()
    r1_sums = verify_sums(R1_DIR)
    r0_sums = verify_sums(R0_DIR)
    f0_sums = verify_sums(F0_DIR)

    reg = {
        "task_id": "F2_R1_2_1",
        "registry": f"R1_2_1_INPUT_IDENTITY_REGISTRY_{phase}",
        "phase": phase,
        "period": "LIKERT_V04_FULL_SCORING_20261029_R0",
        "generated_utc": utc_now_iso(),
        "repair_authority": {
            "card": "LOCAL_AI_LIKERT_V04_F2_R1_2_ARCHIVE_AND_TRUNCATED_TAIL_RECOVERY_ONLY_EXECUTOR_ONLY_20261030.md",
            "reaudit_status_consumed": "EVIDENCE_AND_PREVIOUS_FIXES_VERIFIED_TWO_RECOVERY_WINDOWS_REMAIN; F4仍LOCKED",
            "writable_scope": ["LIKERT_V04_FULL_SCORING_20261029/F2_SCORER_BUILD_R1_2_1/",
                               "07_HPC_Prompts/LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_2_20261030.md(+identity)"],
            "readonly_confirmed": "R0/R1/R1.1的F2目录、F0、F1、F3三代包、审计目录、合同、rubric、gold全部只读消费",
        },
        "executor_environment": {"python": platform.python_version(),
                                 "platform": platform.platform()},
        "immutable_inputs": entries,
        "science_byte_identity_vs_r1_1": science,
        "baseline_verification": {
            "r1_2_sums": r12_sums,
            "r1_2_f4_card_artifact_bindings": r12_cards,
            "r1_1_sums": r11_sums,
            "r1_1_f4_card_artifact_bindings": r11_cards,
            "r1_sums": r1_sums,
            "r0_sums": r0_sums,
            "f0_sums": f0_sums,
        },
        "api_key_environment_check": {
            "policy": "仅存在性,不读取值",
            "vars_checked_names_only": env_existence,
            "any_present": any(env_existence.values()),
        },
        "network_and_api": {"NETWORK_ATTEMPTS": 0, "MODEL_API_ATTEMPTS": 0},
        "mismatches": mismatch,
    }
    ok = (not mismatch
          and all(v["identical"] for v in science.values())
          and r12_sums["mismatch"] == 0 and r12_cards["mismatch"] == 0
          and r11_sums["mismatch"] == 0 and r11_cards["mismatch"] == 0
          and r1_sums["mismatch"] == 0 and r0_sums["mismatch"] == 0
          and f0_sums["mismatch"] == 0)
    reg["identity_check_overall"] = "PASS" if ok else "FAIL_SEE_DETAILS"
    out = R12_DIR / f"R1_2_1_INPUT_IDENTITY_REGISTRY_{phase}.json"
    atomic_write_json(out, reg)
    print(f"written: {out}")
    print(f"immutable inputs: {len(entries)}; mismatches: {len(mismatch)}")
    print(f"science byte-identity vs R1.1: {all(v['identical'] for v in science.values())}")
    print(f"R1.2 SUMS: {r12_sums['ok']}/{r12_sums['entries']}; R1.2 card bindings: {r12_cards['ok']}/{r12_cards['bindings']}")
    print(f"R1.1 SUMS: {r11_sums['ok']}/{r11_sums['entries']}; R1.1 card bindings: {r11_cards['ok']}/{r11_cards['bindings']}")
    print(f"R1 SUMS: {r1_sums['ok']}/{r1_sums['entries']}; R0 SUMS: {r0_sums['ok']}/{r0_sums['entries']}; F0 SUMS: {f0_sums['ok']}/{f0_sums['mismatch']} mismatch")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "BEFORE"))
