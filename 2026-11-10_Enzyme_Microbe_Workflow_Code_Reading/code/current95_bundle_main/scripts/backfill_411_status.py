#!/usr/bin/env python3
"""N7 real backfill entry: current-step GF/ensemble results -> the accepted
411 step-occurrence status table, plus the read-only overlap-mask report
against the TRUE train/valid/test splits (old masks/splits are never written;
the curated pool is never treated as training data).

Per-step backfill_status vocabulary (typed, no silent buckets):
  FORMAL_SCORED_FIVE_SEED        in ensemble formal_steps
  PARTIAL_<reason>               in ensemble partial list (four-seed means are
                                 never presented as five-seed)
  CONTRACT_VIOLATION_<reason>    ensemble contract violations (exit 30 class)
  INCOMPLETE_POOL_NOT_FORWARDED  GF prescan typed (candidates never dropped)
  NOT_RUN_NO_RESULT              READY but no GF output at all (typed)
  PRESERVED_TYPED_BLOCKED        21 blocked steps — untouched, never scored
  PRESERVED_TYPED_TRANSPORT      6 transport steps — untouched
NO_DISCRIMINATION flags (9) are carried through verbatim.

Denominator guarantees (hard asserts, exit 3 on violation):
  * output rows == input 411 rows (step occurrence identity preserved)
  * status_class counts identical to the accepted table (384 READY / 21 / 6)
  * candidate denominator: sum of READY pool sizes recomputed from the frozen
    step table (36,105) and reported; rankings rows must equal scored pools.

Mask section (--train/--valid/--test + --eval-labels): counts gold sequence
shas overlapping each true split (sequence-level, sha256 over exact text).
Read-only; without the split paths the section is typed
MASK_DEFERRED_NODE_SPLITS (never guessed locally).
"""
import argparse
import csv
import gzip
import hashlib
import json
import os
import sys

sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()
EXIT_OK, EXIT_CONFIG, EXIT_DENOM = 0, 2, 3


def read_tsv(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt", newline="") as f:
        header = f.readline(); f.seek(0)
        return list(csv.DictReader(f, delimiter="\t" if "\t" in header else ","))


def write_tsv_gz(path, rows, cols):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path, "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step-status-411", required=True, help="accepted STEP_POOL_STATUS_411.tsv (read-only)")
    ap.add_argument("--step-table", required=True, help="gen/gf/c95_step_table.json (384 READY)")
    ap.add_argument("--prescan", default=None, help="GF_PRESCAN_REPORT.json")
    ap.add_argument("--ensemble-report", default=None, help="ENSEMBLE_REPORT.json")
    ap.add_argument("--rankings", default=None, help="RANKINGS_FULL.tsv.gz")
    ap.add_argument("--eval-labels", default=None)
    ap.add_argument("--train", default=None)
    ap.add_argument("--valid", default=None)
    ap.add_argument("--test", default=None)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    base_rows = read_tsv(a.step_status_411)
    steps = {s["step_id"]: s for s in json.load(open(a.step_table))}
    prescan = json.load(open(a.prescan)) if a.prescan else {"incomplete_steps": []}
    rep = json.load(open(a.ensemble_report)) if a.ensemble_report else None
    formal = set()
    partial_reason, violation_reason = {}, {}
    if rep:
        # formal step ids are recoverable from the report only via rankings; the
        # report itself stores counts — take ids from RANKINGS_FULL when given
        for p in rep.get("partial", []):
            partial_reason[p["step_id"]] = p.get("reason", "PARTIAL")
        for v in rep.get("contract_violations", []):
            violation_reason[v["step_id"]] = v.get("reason", "CONTRACT_VIOLATION")
    if a.rankings and os.path.isfile(a.rankings):
        formal = {r["step_id"] for r in read_tsv(a.rankings)}
    incomplete = {r["step_id"]: r for r in prescan.get("incomplete_steps", [])}

    out_rows = []
    counts = {}
    for r in base_rows:
        sid = r["step_occurrence_id"]
        row = dict(r)
        sc = r.get("status_class", "")
        if sc == "READY":
            if sid in violation_reason:
                bs = "CONTRACT_VIOLATION_" + str(violation_reason[sid]).split()[0]
            elif sid in partial_reason:
                bs = "PARTIAL_" + str(partial_reason[sid]).split()[0]
            elif sid in formal:
                bs = "FORMAL_SCORED_FIVE_SEED"
            elif sid in incomplete:
                bs = "INCOMPLETE_POOL_NOT_FORWARDED"
            elif rep is None and not a.rankings:
                bs = "NOT_RUN_NO_GF_INPUTS_PROVIDED"
            else:
                bs = "NOT_RUN_NO_RESULT"
        elif "BLOCK" in sc.upper():
            bs = "PRESERVED_TYPED_BLOCKED"
        elif "TRANSPORT" in sc.upper():
            bs = "PRESERVED_TYPED_TRANSPORT"
        else:
            bs = "PRESERVED_TYPED_" + sc.replace(" ", "_")
        row["backfill_status"] = bs
        row["backfill_detail"] = json.dumps({
            "missing_reaction_assets": incomplete.get(sid, {}).get("missing_reaction_assets"),
            "missing_candidate_uids_n": incomplete.get(sid, {}).get("missing_candidate_uids_n"),
        }) if sid in incomplete else ""
        out_rows.append(row)
        counts[bs] = counts.get(bs, 0) + 1

    # ---- denominator guarantees -------------------------------------------
    base_counts = {}
    for r in base_rows:
        base_counts[r.get("status_class", "")] = base_counts.get(r.get("status_class", ""), 0) + 1
    errs = []
    if len(out_rows) != len(base_rows):
        errs.append(f"row count drift {len(out_rows)} != {len(base_rows)}")
    ready_ids = [r["step_occurrence_id"] for r in base_rows if r.get("status_class") == "READY"]
    if sorted(ready_ids) != sorted(steps.keys()):
        errs.append(f"READY set != step table set ({len(ready_ids)} vs {len(steps)})")
    pool_rows = sum(len(s["pool_uids"]) for s in steps.values())
    nd = sum(1 for s in steps.values() if s.get("no_discrimination"))
    scored_rows = None
    if a.rankings and os.path.isfile(a.rankings):
        rrows = read_tsv(a.rankings)
        scored_rows = len(rrows)
        exp = sum(len(steps[sid]["pool_uids"]) for sid in formal)
        if scored_rows != exp:
            errs.append(f"rankings rows {scored_rows} != scored pool sizes {exp}")
    if errs:
        print("DENOMINATOR_VIOLATION: " + "; ".join(errs), file=sys.stderr)
        return EXIT_DENOM

    cols = sorted({k for r in out_rows for k in r})
    cols = [c for c in ["step_occurrence_id", "status_class", "pool_status", "no_discrimination"] if c in cols] + \
           [c for c in cols if c not in ("step_occurrence_id", "status_class", "pool_status", "no_discrimination")]
    write_tsv_gz(os.path.join(a.out_dir, "STEP_POOL_STATUS_411_BACKFILL.tsv.gz"), out_rows, cols)

    # ---- overlap mask report (read-only; true splits only) -----------------
    mask = {"status": "MASK_DEFERRED_NODE_SPLITS"}
    if a.train and a.valid and a.test and a.eval_labels:
        gold_shas = {r["sequence_sha256"] for r in read_tsv(a.eval_labels) if r.get("gold_flag") == "TRUE"}
        mask = {"status": "COMPUTED_READ_ONLY", "gold_shas": len(gold_shas), "splits": {}}
        for name, p in (("train", a.train), ("valid", a.valid), ("test", a.test)):
            shas = set()
            for r in read_tsv(p):
                seq = r.get("sequence", "")
                if seq:
                    shas.add(sha_text(seq))
            mask["splits"][name] = {"rows": len(shas), "gold_overlap_shas": len(gold_shas & shas)}
        mask["policy"] = ("true train/valid/test read-only; curated pool never used as training "
                          "data; counts only, no row-level export of split contents")
    json.dump(mask, open(os.path.join(a.out_dir, "OVERLAP_MASK_REPORT.json"), "w"), indent=1)

    report = {"rows_total": len(out_rows), "base_status_class_counts": base_counts,
              "backfill_status_counts": counts,
              "ready_steps": len(steps), "ready_pool_rows": pool_rows,
              "no_discrimination_steps": nd,
              "formal_scored_steps": len(formal),
              "rankings_rows": scored_rows,
              "preserved": {"blocked": base_counts.get("BLOCKED", 0),
                            "transport": base_counts.get("TRANSPORT", 0),
                            "policy": "Input context status classes and all candidate members preserved; "
                                      "mainline and Rescue15 denominators reported separately"},
              "mask": mask}
    json.dump(report, open(os.path.join(a.out_dir, "BACKFILL_REPORT.json"), "w"), indent=1)
    print(json.dumps({k: report[k] for k in ("rows_total", "backfill_status_counts",
                                             "ready_pool_rows", "formal_scored_steps")}, indent=1))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
