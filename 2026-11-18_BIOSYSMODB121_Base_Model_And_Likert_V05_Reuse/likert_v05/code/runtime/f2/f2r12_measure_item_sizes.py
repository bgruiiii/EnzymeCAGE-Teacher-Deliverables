"""R1.1 item size measurement with the AUDITED F3 R1.1 evidence package
(f3r11_case_slice_v2, incl. real F7 interpretation-layer text; repair card §2:
re-register request sizes and cost estimates with real E0; the R0 60KB
placeholder estimate must not be reused as if measured).

Assembles, per slot: R1 system prompt (rubric + full schema embedded) +
question + frozen answer bytes + per-case gold slice (same algorithm as the
slicer, single pass) + R1 template overhead + REAL per-case E0 slice text
from the adapter. Token estimate = same conservative heuristic as the request
builder. Output: logs/ITEM_SIZE_MEASUREMENTS_R1_2_1.json.

Offline: reads only; no network, no model API.
"""
from __future__ import annotations

import csv
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import R, F0_DIR, F2_DIR, atomic_write_json, utc_now_iso
import f2r12_gold_slicer
import f2r12_evidence_adapter as ea

F3_MANIFEST = R / "LIKERT_V04_FULL_SCORING_20261029" / "F3_EVIDENCE_R1_1" / "EVIDENCE_MANIFEST_R1_1.json"
F3_MANIFEST_SHA = "7e54df82ea49a54916ad523bea924b82d44576691d2ad35448947ae6021af95e"
TEMPLATE_OVERHEAD_BYTES = 8_000  # R1 template (measured file + fixed text)


def approx_tokens_from_mixed(text_bytes: int, cjk_ratio: float) -> int:
    cjk = int(text_bytes * cjk_ratio / 3)
    other = text_bytes - cjk * 3
    return cjk + other // 3


def slice_bytes_per_case() -> dict:
    totals = {}
    for name in f2r12_gold_slicer.CASE_SCOPED_TABLES:
        path = f2r12_gold_slicer.GOLD_DIR / name
        raw = open(path, "rb").read()
        lines = raw.decode("utf-8").splitlines(keepends=True)
        cols = lines[0].rstrip("\r\n").split("\t")
        idx = cols.index("case_id")
        hb = len(lines[0].encode("utf-8"))
        per = {}
        for line in lines[1:]:
            fields = line.rstrip("\r\n").split("\t")
            if len(fields) > idx:
                per[fields[idx]] = per.get(fields[idx], 0) + len(line.encode("utf-8"))
        for cid, b in per.items():
            totals[cid] = totals.get(cid, 0) + hb + b
    for name in f2r12_gold_slicer.WHOLE_TABLES:
        b = os.path.getsize(f2r12_gold_slicer.GOLD_DIR / name)
        for cid in totals:
            totals[cid] += b
    for cid, doc in f2r12_gold_slicer.CASE_SCOPE_DOCS.items():
        if cid in totals:
            totals[cid] += os.path.getsize(doc)
    return totals


def main() -> int:
    pkg = ea.load_package_from_binding(
        {"mode": "F3_R11_CASE_SLICES_V2", "manifest_path": str(F3_MANIFEST),
         "expected_manifest_sha256": F3_MANIFEST_SHA})

    rows = list(csv.DictReader(open(F0_DIR / "B_480_ANSWER_INDEX.tsv", encoding="utf-8"),
                               delimiter="\t"))
    qdir = R / "25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26" / "G2_questions" / "rendered_messages"
    qsize = {}
    for cid in {r["case_id"] for r in rows}:
        d = json.load(open(qdir / f"{cid}.json", encoding="utf-8"))
        qsize[cid] = len(d["messages"][0]["content"].encode("utf-8"))
    gold = slice_bytes_per_case()
    sp_bytes = os.path.getsize(F2_DIR / "SCORING_SYSTEM_PROMPT.txt")

    s = open(F2_DIR / "SCORING_SYSTEM_PROMPT.txt", encoding="utf-8").read()
    cjk = sum(1 for ch in s if "\u4e00" <= ch <= "\u9fff" or "\u3000" <= ch <= "\u303f")
    probe_ratio = cjk * 3 / max(len(s.encode("utf-8")), 1)

    per_slot = []
    for r in rows:
        cid = r["case_id"]
        uid = r["b_slot_uid"]
        ev = pkg.build_item_evidence(cid, uid)
        ev_bytes = ev["block_bytes"]
        total = (sp_bytes + qsize[cid] + int(r["answer_bytes"]) + gold.get(cid, 0)
                 + TEMPLATE_OVERHEAD_BYTES + ev_bytes)
        tok_prompt = approx_tokens_from_mixed(sp_bytes + qsize[cid], probe_ratio)
        tok_data = approx_tokens_from_mixed(
            int(r["answer_bytes"]) + gold.get(cid, 0) + TEMPLATE_OVERHEAD_BYTES + ev_bytes,
            probe_ratio * 0.6)
        per_slot.append({"b_slot_uid": uid, "case_id": cid,
                         "tested_model_config_id": r["tested_model_config_id"],
                         "assembled_bytes_real_e0r11": total,
                         "e0r11_block_bytes": ev_bytes,
                         "evidence_status": ev["status"],
                         "approx_input_tokens": tok_prompt + tok_data,
                         "gold_slice_bytes": gold.get(cid, 0)})

    toks = sorted(s["approx_input_tokens"] for s in per_slot)
    n = len(toks)
    summary = {
        "measurement": "R1_2_1_REAL_F3R1_1_E0_V2",
        "evidence_package": {"manifest_sha256": pkg.manifest_sha256,
                             "baseline_id": pkg.baseline_id,
                             "interface": pkg.identity()["interface"],
                             "case_manifest_sha256": pkg.case_manifest_sha256,
                             "records": len(pkg.record_ids),
                             "cases_bound": len(pkg.case_bindings)},
        "n_slots": n,
        "approx_input_tokens": {
            "mean": round(statistics.mean(toks), 1), "median": toks[n // 2],
            "p90": toks[int(n * 0.9)], "p99": toks[int(n * 0.99)],
            "max": toks[-1], "min": toks[0]},
        "e0r11_block_bytes_stats": {
            "mean": round(statistics.mean([s["e0r11_block_bytes"] for s in per_slot]), 1),
            "max": max(s["e0r11_block_bytes"] for s in per_slot)},
        "system_prompt_bytes": sp_bytes,
        "cjk_ratio_probe": round(probe_ratio, 4),
        "token_heuristic": "CJK≈1token/char; other≈1token/3bytes; conservative over-estimate",
        "max_input_tokens_bound_in_config": 400000,
        "bound_headroom_vs_measured_max": 400000 - toks[-1],
        "replaces": "R0 60KB占位估算与R1旧包测量均作废；本表为已审F3 R1.1（含F7全文）真实装配实测",
    }
    out = F2_DIR / "logs" / "ITEM_SIZE_MEASUREMENTS_R1_2_1.json"
    atomic_write_json(out, {"generated_utc": utc_now_iso(), "summary": summary,
                            "per_slot": per_slot})
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
