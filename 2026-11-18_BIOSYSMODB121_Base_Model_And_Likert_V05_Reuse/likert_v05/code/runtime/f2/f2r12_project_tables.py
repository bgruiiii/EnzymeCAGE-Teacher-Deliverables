"""F2 projection tools: RATINGS_CANONICAL.jsonl is the ONE normative
structured rating source; RATINGS_480.tsv and RATING_DIMENSIONS_3360.tsv are
projections of it (contract §7.3: 只生成一个规范结构化评分源，TSV/展示MD由它
投影; no second independently-edited record may diverge — projection
consistency is enforced here, mirroring the M4 R2 FIELD_PROJECTION_CONTRACT
discipline).

Rules:
  - projections are regenerated from the canonical JSONL only;
  - if a projection file exists and does NOT match the regeneration, the
    tool REFUSES (dual-record contradiction counterexample T15) instead of
    silently overwriting either side;
  - failed/NOT_RUN slots appear in RATINGS_480.tsv with their frozen
    system_run_status and EMPTY dimension fields (480-row coverage ≠ 480
    successful ratings);
  - weighted_total column = PROGRAM RECOMPUTE (authoritative); the model's
    original value is kept in model_weighted_total + correction flag.

Offline: no network.
"""
from __future__ import annotations

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import DIMENSIONS, atomic_write_text, totals_contract
from f2r12_cache_checkpoint import load_canonical_jsonl

R480_COLUMNS = [
    "b_slot_uid", "anonymous_item_id", "batch", "case_id",
    "system_run_status", "validation_status", "attempt_index", "transfer_id",
    "model_frozen", "model_returned", "http_status", "stream_status",
    "finish_reason", "utc",
    "prompt_tokens", "completion_tokens", "cost_cny",
] + [f"{d}_score_status" for d in DIMENSIONS] \
    + [f"{d}_score" for d in DIMENSIONS] \
    + [f"{d}_key_error" for d in DIMENSIONS] + [
    "weighted_total_program", "weighted_total_model", "total_correction_applied",
    "total_status", "scientific_subscore_program", "scientific_subscore_model",
    "d5_severity_overall",
    "confidence", "review_queue_flag", "evidence_snapshot_sha",
    "evidence_case_slice_sha256",
    "input_manifest_sha", "answer_sha256", "question_rendered_prompt_sha256",
    "rubric_text_sha256", "gold_slice_manifest_sha256", "scope_rows_sha256",
    "system_prompt_sha256", "rating_schema_sha256", "run_config_sha256",
    "rater_type",
]

DIM3360_COLUMNS = [
    "b_slot_uid", "anonymous_item_id", "case_id", "dimension",
    "score_status", "score", "key_error", "root_error_event_ids",
    "rationale", "answer_locator", "ne_basis", "ne_unverified", "na_basis",
    "missing_basis", "n_unverified_subclaims", "n_evidence_refs",
    "system_run_status",
]


def _program_totals(dims: dict):
    """Projection uses the SAME shared lossless contract as validator and
    canonical records (audit F2-P1-05): SCORED and MISSING=1 both participate;
    NE/NA → NOT_COMPARABLE."""
    tc = totals_contract(dims or {})
    if tc["status"] == "COMPARABLE":
        return tc["weighted_total"], tc["scientific_subscore"]
    return "NOT_COMPARABLE", "NOT_COMPARABLE"


def project(canonical_path: str, out_dir: str, expected_slots: int | None = None,
            expected_committed_uids=None):
    """R1.2 (F2R11-P1-02): unparseable canonical lines are a HARD error —
    the projector must never 'warn, emit 0 rows and still report success'.
    Run the startup repair (repair_canonical) first; it preserves the torn
    tail bytes as evidence and leaves a parseable active file.
    expected_committed_uids: checkpoint VALID slot set — every one of them
    MUST appear in the projection (consistency check, not just an upper
    bound); unexecuted slots stay honestly absent/NOT_RUN elsewhere."""
    recs, problems = load_canonical_jsonl(canonical_path)
    if problems:
        raise RuntimeError(
            f"canonical file has {len(problems)} unparseable line(s) "
            f"(first: {problems[0]}): refusing to project — run startup repair "
            "(f2r12_cache_checkpoint.repair_canonical) which preserves the "
            "damaged bytes as evidence; never project a silently-lossy table")
    # last record per slot wins for status, but ALL attempts remain in the
    # archive/ledger; duplicates with two VALID records = contradiction
    by_slot = {}
    for r in recs:
        uid = r["b_slot_uid"]
        prev = by_slot.get(uid)
        if prev and prev.get("system_run_status") == "OK" and r.get("system_run_status") == "OK":
            raise RuntimeError(
                f"dual VALID canonical records for {uid} — single normative source violated; "
                "refusing to project (list both, choose neither automatically)")
        if prev is None or prev.get("system_run_status") != "OK":
            # OK wins; among failures the LATEST record reflects the final state
            by_slot[uid] = r
    if expected_slots is not None and len(by_slot) > expected_slots:
        raise RuntimeError(f"more unique slots ({len(by_slot)}) than expected ({expected_slots})")
    if expected_committed_uids:
        missing = [u for u in expected_committed_uids if u not in by_slot]
        if missing:
            raise RuntimeError(
                f"checkpoint marks {len(missing)} slot(s) VALID but canonical/projection "
                f"lack them (e.g. {missing[:3]}) — checkpoint/canonical/projection must be "
                "consistent; refusing to emit a table that hides completed ratings")

    r480 = [R480_COLUMNS]
    d3360 = [DIM3360_COLUMNS]
    for uid in sorted(by_slot):
        r = by_slot[uid]
        rating = r.get("rating") or {}
        dims = rating.get("dimensions") or {}
        usage = r.get("usage") or {}
        prog_total, prog_sub = _program_totals(dims) if dims else ("", "")
        row = {
            "b_slot_uid": uid,
            "anonymous_item_id": r.get("anonymous_item_id"),
            "batch": r.get("batch"),
            "case_id": r.get("case_id"),
            "system_run_status": r.get("system_run_status"),
            "validation_status": (r.get("validation") or {}).get("status"),
            "attempt_index": r.get("attempt_index"),
            "transfer_id": r.get("transfer_id"),
            "model_frozen": r.get("model_frozen"),
            "model_returned": r.get("model_returned"),
            "http_status": r.get("http_status", ""),
            "stream_status": r.get("stream_status", ""),
            "finish_reason": r.get("finish_reason", ""),
            "utc": r.get("utc"),
            "prompt_tokens": usage.get("prompt_tokens", ""),
            "completion_tokens": usage.get("completion_tokens", ""),
            "cost_cny": r.get("cost_cny") if r.get("cost_cny") is not None else "",
            "weighted_total_program": (r.get("recomputed_weighted_total")
                                       if r.get("recomputed_weighted_total") is not None else prog_total),
            "weighted_total_model": r.get("model_weighted_total", ""),
            "total_correction_applied": r.get("total_correction_applied", ""),
            "total_status": rating.get("total_status", ""),
            "scientific_subscore_program": (r.get("recomputed_scientific_subscore")
                                            if r.get("recomputed_scientific_subscore") is not None else prog_sub),
            "scientific_subscore_model": r.get("model_scientific_subscore", ""),
            "d5_severity_overall": (rating.get("d5_registry") or {}).get("severity_overall", ""),
            "confidence": rating.get("confidence", ""),
            "review_queue_flag": (rating.get("review_queue") or {}).get("flag", ""),
            "evidence_snapshot_sha": r.get("evidence_snapshot_sha", ""),
            "evidence_case_slice_sha256": r.get("evidence_case_slice_sha256", ""),
            "input_manifest_sha": r.get("input_manifest_sha", ""),
            "answer_sha256": r.get("answer_sha256", ""),
            "question_rendered_prompt_sha256": r.get("question_rendered_prompt_sha256", ""),
            "rubric_text_sha256": r.get("rubric_text_sha256", ""),
            "gold_slice_manifest_sha256": r.get("gold_slice_manifest_sha256", ""),
            "scope_rows_sha256": r.get("scope_rows_sha256", ""),
            "system_prompt_sha256": r.get("system_prompt_sha256", ""),
            "rating_schema_sha256": r.get("rating_schema_sha256", ""),
            "run_config_sha256": r.get("run_config_sha256", ""),
            "rater_type": r.get("rater_type", "AI"),
        }
        for d in DIMENSIONS:
            dim = dims.get(d) or {}
            row[f"{d}_score_status"] = dim.get("score_status", "")
            # failed calls: dimension score fields stay EMPTY (never 0)
            row[f"{d}_score"] = dim.get("score") if dim.get("score") is not None else ""
            row[f"{d}_key_error"] = dim.get("key_error", "")
            d3360.append([
                uid, r.get("anonymous_item_id"), r.get("case_id"), d,
                dim.get("score_status", ""), 
                dim.get("score") if dim.get("score") is not None else "",
                dim.get("key_error", ""),
                ";".join(dim.get("root_error_event_ids") or []),
                dim.get("rationale", ""), dim.get("answer_locator", ""),
                dim.get("ne_basis") or "", dim.get("ne_unverified") or "",
                dim.get("na_basis") or "", dim.get("missing_basis") or "",
                len(dim.get("unverified_subclaims") or []),
                len(dim.get("evidence_refs") or []),
                r.get("system_run_status"),
            ])
        r480.append([row[c] for c in R480_COLUMNS])

    def _tsv(rows):
        return "\n".join("\t".join(_cell(x) for x in row) for row in rows) + "\n"

    def _cell(v):
        if v is None:
            return ""
        s = str(v)
        if "\t" in s or "\n" in s:
            s = s.replace("\t", " ").replace("\n", "\\n")
        return s

    outputs = {}
    for name, rows in [("RATINGS_480.tsv", r480), ("RATING_DIMENSIONS_3360.tsv", d3360)]:
        text = _tsv(rows)
        p = os.path.join(out_dir, name)
        if os.path.exists(p):
            existing = open(p, encoding="utf-8").read()
            if existing != text:
                raise RuntimeError(
                    f"projection {name} exists and DIFFERS from canonical regeneration — "
                    "dual-record contradiction; refusing to overwrite either side "
                    "(resolve by correcting the canonical source or archiving the projection explicitly)")
        atomic_write_text(p, text)
        outputs[name] = {"path": p, "data_rows": len(rows) - 1}
    return outputs


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical_jsonl")
    ap.add_argument("out_dir")
    ap.add_argument("--expected-slots", type=int, default=None)
    a = ap.parse_args()
    print(json.dumps(project(a.canonical_jsonl, a.out_dir, a.expected_slots),
                     ensure_ascii=False, indent=1))
