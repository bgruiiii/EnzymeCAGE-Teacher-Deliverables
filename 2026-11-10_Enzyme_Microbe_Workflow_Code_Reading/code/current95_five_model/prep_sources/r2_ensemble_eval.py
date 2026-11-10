#!/usr/bin/env python3
"""R2 ensemble + evaluation — adapted from BUNDLE/historical/a109/c95_ensemble_eval.py
(audited formula). Changes (complete):
 1. locked five-weight matrix parameterized per arm (--arm; values from the
    bundled MODEL_IDENTITIES_27 matrix cross-checked vs R1 node verification).
 2. metrics ADD hit_at_3 and mrr_at_10 as separately named columns; the
    documented formula (float64 sigmoid EXACTLY ONCE per seed logit; mean of
    5 seed probs equal weight 0.2; rank desc; sha256(uid) tie-break only on
    genuine float64 equality) and ALL completeness/contract gates are VERBATIM
    (seed set exactness, pool identity vs step table, output_semantics contract,
    per-seed common-context + locked ckpt binding, finite/length, PARTIAL vs
    formal separation, NO_DISCRIMINATION excluded from capability denominator).
 3. step table = R2 effective (consumer-accepted) table; labels joined by
    (step, sha) from the prepared per-context eval labels.
"""
import argparse, csv, gzip, hashlib, json, math, os, sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2_lib as L

sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()
sha_file = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
EXIT_OK, EXIT_PARTIAL, EXIT_CONTRACT = 0, 20, 30
EXPECTED_SEMANTICS = "RAW_LOGIT_FORWARD_SIGMOID_READOUT_FALSE"

def read_tsv(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def write_tsv_gz(path, rows, cols):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path, "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows: w.writerow({c: r.get(c, "") for c in cols})

def sigmoid64(x): return 1.0 / (1.0 + math.exp(-x))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True)
    ap.add_argument("--raw-logits-dir", required=True)
    ap.add_argument("--step-table", required=True)
    ap.add_argument("--runtime-map", required=True)
    ap.add_argument("--eval-labels", required=True)
    ap.add_argument("--seeds", default="40,41,42,43,44")
    ap.add_argument("--expected-context", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--locked-shas-json", default=None,
                    help="optional {seed: sha256} override (for arms outside r2_lib.locked_ckpt_table, e.g. legacy_esm2_3b)")
    a = ap.parse_args()
    seeds = a.seeds.split(",")
    if a.locked_shas_json:
        EXP = {int(k): v for k, v in json.load(open(a.locked_shas_json)).items()}
    else:
        EXP = {s: v[1] for s, v in L.locked_ckpt_table()[a.arm].items()}
    os.makedirs(a.out_dir, exist_ok=True)
    steps = json.load(open(a.step_table))
    exp_ctx = json.load(open(a.expected_context))
    expected_common_sha = exp_ctx["common_context_sha256"]
    recomputed = sha_text(json.dumps(exp_ctx["common_context"], sort_keys=True, separators=(",", ":")))
    if recomputed != expected_common_sha:
        print("CONTRACT_VIOLATION: expected-context internally inconsistent", file=sys.stderr)
        return EXIT_CONTRACT
    labels = {}
    for r in read_tsv(a.eval_labels):
        labels[(r["step_occurrence_id"], r["sequence_sha256"])] = r

    rankings, partial, violations, formal_steps = [], [], [], []
    for s in steps:
        sid = s["step_id"]
        p = os.path.join(a.raw_logits_dir, f"{sid}.json")
        if not os.path.isfile(p):
            partial.append({"step_id": sid, "reason": "RAW_LOGITS_FILE_MISSING"}); continue
        d = json.load(open(p))
        if d.get("pool_uids") != s["pool_uids"] or d.get("pool_shas") != s["pool_shas"]:
            partial.append({"step_id": sid, "reason": "POOL_IDENTITY_MISMATCH_VS_STEP_TABLE"}); continue
        if set(d.get("seeds", {})) != set(seeds):
            partial.append({"step_id": sid, "reason": "SEED_SET_NOT_EXACT",
                            "present": sorted(d.get("seeds", {})), "required": seeds}); continue
        sem = d.get("output_semantics")
        if sem != EXPECTED_SEMANTICS:
            violations.append({"step_id": sid, "reason": (
                f"PROBABILITY_ROUTE_CONTRACT_REJECTED (declared {sem!r})" if sem
                else "OUTPUT_CONTRACT_FIELD_MISSING")}); continue
        if d.get("common_context_sha256") != expected_common_sha:
            violations.append({"step_id": sid, "reason": "COMMON_CONTEXT_MISMATCH_VS_EXPECTED",
                               "stored": d.get("common_context_sha256"), "expected": expected_common_sha}); continue
        seed_ids = d.get("seed_identities", {})
        vio = None
        for sd in seeds:
            si = seed_ids.get(str(sd))
            if not si: vio = f"SEED_IDENTITY_MISSING seed={sd}"; break
            if si.get("common_context_sha256") != expected_common_sha:
                vio = f"PER_SEED_CONTEXT_MISMATCH seed={sd}"; break
            if si.get("ckpt_sha256") != EXP.get(int(sd)):
                vio = f"PER_SEED_CKPT_SHA_MISMATCH seed={sd}"; break
        if vio:
            violations.append({"step_id": sid, "reason": vio}); continue
        n = len(s["pool_uids"])
        acc = [0.0] * n
        bad = None
        for sd in seeds:
            Lg = d["raw_logits"].get(str(sd))
            if Lg is None or len(Lg) != n: bad = f"LOGIT_LENGTH seed={sd}"; break
            for i, x in enumerate(Lg):
                if not math.isfinite(x): bad = f"NON_FINITE seed={sd} idx={i}"; break
            if bad: break
            for i, x in enumerate(Lg):
                acc[i] += sigmoid64(float(x))
        if bad:
            partial.append({"step_id": sid, "reason": bad}); continue
        ens = [v / len(seeds) for v in acc]
        order = sorted(range(n), key=lambda i: (-ens[i], sha_text(s["pool_uids"][i])))
        formal_steps.append(sid)
        for rank, i in enumerate(order, start=1):
            uid = s["pool_uids"][i]; sh = s["pool_shas"][i]
            lab = labels.get((sid, sh), {})
            rankings.append({"step_id": sid, "rank": rank, "runtime_uid": uid, "sequence_sha256": sh,
                             "ensemble_prob_float64": repr(ens[i]),
                             "gold_flag": lab.get("gold_flag", ""),
                             "label_class": lab.get("label_class", "UNLABELED_CANDIDATE"),
                             "no_discrimination": str(bool(s.get("no_discrimination"))).upper()})

    metrics, by_step = [], {}
    for r in rankings: by_step.setdefault(r["step_id"], []).append(r)
    for sid in formal_steps:
        rows = by_step[sid]
        nd = rows[0]["no_discrimination"] == "TRUE"
        gold_ranks = [r["rank"] for r in rows if r["gold_flag"] == "TRUE"]
        n_non_gold = sum(1 for r in rows if r["gold_flag"] != "TRUE")
        if nd or n_non_gold == 0 or len(rows) <= 1:
            metrics.append({"step_id": sid, "capability_denominator": "NO_DISCRIMINATION",
                            "n_candidates": len(rows), "gold_ranks": ";".join(map(str, gold_ranks))}); continue
        best = min(gold_ranks) if gold_ranks else None
        metrics.append({"step_id": sid, "capability_denominator": "INCLUDED",
                        "n_candidates": len(rows), "gold_ranks": ";".join(map(str, gold_ranks)),
                        "best_gold_rank": best if best is not None else "",
                        "hit_at_1": int(best == 1) if best else 0,
                        "hit_at_3": int(best is not None and best <= 3),
                        "hit_at_5": int(best is not None and best <= 5),
                        "hit_at_10": int(best is not None and best <= 10),
                        "mrr_seq_level": (1.0 / best) if best else 0.0,
                        "mrr_at_10": ((1.0 / best) if (best and best <= 10) else 0.0),
                        "metric_naming": "BEST_GOLD_SEQUENCE_LEVEL_DIAGNOSTIC (component hits never count as complete-enzyme success)"})
    write_tsv_gz(os.path.join(a.out_dir, "RANKINGS_FULL.tsv.gz"), rankings,
                 ["step_id", "rank", "runtime_uid", "sequence_sha256", "ensemble_prob_float64",
                  "gold_flag", "label_class", "no_discrimination"])
    write_tsv_gz(os.path.join(a.out_dir, "PER_STEP_METRICS_SEQ_LEVEL.tsv.gz"), metrics,
                 ["step_id", "capability_denominator", "n_candidates", "gold_ranks", "best_gold_rank",
                  "hit_at_1", "hit_at_3", "hit_at_5", "hit_at_10", "mrr_seq_level", "mrr_at_10", "metric_naming"])
    inc = [m for m in metrics if m["capability_denominator"] == "INCLUDED"]
    report = {
        "utc": datetime.now(timezone.utc).isoformat(), "arm": a.arm,
        "formula": "prob=1/(1+exp(-float64 logit)) once; mean of 5 seed probs (equal weight 0.2); rank desc; sha256(uid) tie-break on exact float64 equality (GF documented contract)",
        "requested_seeds": seeds,
        "steps_total": len(steps), "steps_formal": len(formal_steps), "steps_partial": len(partial),
        "partial": partial[:50], "contract_violations_n": len(violations), "contract_violations": violations[:50],
        "expected_common_context_sha256": expected_common_sha,
        "locked_ckpt_matrix": EXP,
        "capability_steps": len(inc),
        "no_discrimination_steps": sum(1 for m in metrics if m["capability_denominator"] == "NO_DISCRIMINATION"),
        "seq_level_summary": {
            "hit_at_1": sum(m["hit_at_1"] for m in inc), "hit_at_3": sum(m["hit_at_3"] for m in inc),
            "hit_at_5": sum(m["hit_at_5"] for m in inc), "hit_at_10": sum(m["hit_at_10"] for m in inc),
            "mrr_mean": (sum(m["mrr_seq_level"] for m in inc) / len(inc)) if inc else None,
            "mrr_at_10_mean": (sum(m["mrr_at_10"] for m in inc) / len(inc)) if inc else None,
            "denominator_note": "capability denominator excludes NO_DISCRIMINATION steps"},
        "input_identities": {"step_table_sha256": sha_file(a.step_table), "runtime_map_sha256": sha_file(a.runtime_map),
                             "eval_labels_sha256": sha_file(a.eval_labels), "expected_context_sha256": sha_file(a.expected_context),
                             "raw_logits_dir_files": len(os.listdir(a.raw_logits_dir)),
                             "script_sha256": sha_file(os.path.abspath(__file__)),
                             "source_script": "historical/a109/c95_ensemble_eval.py",
                             "source_sha256": sha_file(L.BUNDLE + "/historical/a109/c95_ensemble_eval.py")},
    }
    with open(os.path.join(a.out_dir, "ENSEMBLE_REPORT.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps({k: report[k] for k in ("arm", "steps_total", "steps_formal", "steps_partial",
                                             "contract_violations_n", "capability_steps", "no_discrimination_steps")}, indent=1))
    print(json.dumps(report["seq_level_summary"], indent=1))
    if violations: return EXIT_CONTRACT
    if partial: return EXIT_PARTIAL
    return EXIT_OK

if __name__ == "__main__":
    sys.exit(main())
