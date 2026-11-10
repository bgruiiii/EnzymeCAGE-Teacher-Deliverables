#!/usr/bin/env python3
"""R4 five-way unified-pool comparison + 95-path coverage + formal 411/95.

Five-arm extension of sources/r3_compare_unified.py (structure VERBATIM; arm
set extended to the gated five; tags b3/leg/new/e0enz/newenz; winner = tied-tag
join). Inputs: eval/{arm}/{ctx}/{ENSEMBLE_REPORT.json,
PER_STEP_METRICS_SEQ_LEVEL.tsv.gz}, runtime/pool/{UNIFIED_STEP_TABLE_*,
STEP_RETENTION_AUDIT.tsv, FREEZE_SUMMARY.json}, R2 corrected 411 inventory.
Capability denominator = INCLUDED steps (NO_DISCRIMINATION excluded), asserted
IDENTICAL across all five arms (drift gate). Path-complete rule calibrated on
the 3B parent (must reproduce 82 policy-complete paths; stereo9+transport6
policy exemptions, unique rule per R3 brute-force).
Outputs: runtime/compare/{FIVE_WAY_COMPARISON.json, PER_STEP_FIVE_WAY.tsv.gz,
PATH_COVERAGE_95_FIVE.json, PATH_CASES_*.json, STEP_STATUS_411_FORMAL_R4.tsv,
CASE_95_FORMAL_R4.tsv}
"""
import csv, gzip, json, os, sys
from collections import defaultdict
from pathlib import Path
_NEWROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, _NEWROOT + "/current95_five_model_complete_prep_20261103/sources")
import r3_paths as P
assert P.NEWROOT == _NEWROOT

OUT = P.NEWROOT + "/runtime/compare"; os.makedirs(OUT, exist_ok=True)
POOL = P.NEWROOT + "/runtime/pool"
gate = json.load(open(f"{POOL}/ALL_MODELS_ASSETS_READY.json"))
assert gate["status"] == "ALL_MODELS_ASSETS_READY" and gate["steps"] == 382
ARMS = list(gate["arms"])
assert len(ARMS) == 5
TAGS = {"legacy_esm2_3b": "b3", "legacy_esmc600m": "leg", "new_esmc600m": "new",
        "current_e0_enzgfm650m": "e0enz", "new_enzgfm650m": "newenz"}

def read_metrics(arm, ctx):
    p = f"{P.NEWROOT}/eval/{arm}/{ctx}/PER_STEP_METRICS_SEQ_LEVEL.tsv.gz"
    out = {}
    if os.path.exists(p):
        with gzip.open(p, "rt") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                out[r["step_id"]] = r
    return out

metrics = {arm: {} for arm in ARMS}
reports = {}
for arm in ARMS:
    for ctx in P.CTXS:
        metrics[arm].update(read_metrics(arm, ctx))
        rp = f"{P.NEWROOT}/eval/{arm}/{ctx}/ENSEMBLE_REPORT.json"
        if os.path.exists(rp):
            reports[(arm, ctx)] = json.load(open(rp))
for arm in ARMS:
    assert metrics[arm], f"NO METRICS for {arm} — run evaluator first"

steps = {}
for ctx in P.CTXS:
    for s in json.load(open(f"{POOL}/UNIFIED_STEP_TABLE_{ctx}.json")):
        steps[s["step_id"]] = (ctx, s)

# denominator drift gate (five arms)
den = {arm: {sid for sid, m in metrics[arm].items() if m["capability_denominator"] == "INCLUDED"} for arm in ARMS}
base = den[ARMS[0]]
for arm in ARMS[1:]:
    assert den[arm] == base, f"CAPABILITY_DENOMINATOR_DRIFT {arm}: +{len(den[arm]-base)} -{len(base-den[arm])}"

rows = []
for sid, (ctx, s) in sorted(steps.items()):
    row = {"step_id": sid, "ctx": ctx, "case_id": sid.split("__")[0],
           "n_candidates": len(s["pool_uids"]), "n_gold": s["n_gold"],
           "no_discrimination": str(bool(s["no_discrimination"])).upper(),
           "rescue_dependent": str(bool(s["rescue_dependent"])).upper(),
           "capability": metrics[ARMS[0]].get(sid, {}).get("capability_denominator", "NOT_FORMAL")}
    for arm in ARMS:
        tag = TAGS[arm]
        m = metrics[arm].get(sid)
        row[f"{tag}_formal"] = str(m is not None)
        row[f"{tag}_best_gold_rank"] = (m.get("best_gold_rank", "") if m else "")
        row[f"{tag}_hit_at_1"] = (m.get("hit_at_1", "") if m else "")
        row[f"{tag}_hit_at_3"] = (m.get("hit_at_3", "") if m else "")
    if row["capability"] == "INCLUDED":
        ranks = []
        for arm in ARMS:
            r = metrics[arm][sid].get("best_gold_rank")
            ranks.append(int(r) if r not in ("", None) else 10**9)
        for arm, rk in zip(ARMS, ranks):
            row["best_rank_" + TAGS[arm]] = rk
        best = min(ranks)
        row["winner"] = ",".join(TAGS[a] for a, r in zip(ARMS, ranks) if r == best)
    rows.append(row)

def agg(arm, subset=None):
    sel = [r for r in rows if r["capability"] == "INCLUDED" and (subset is None or subset(r))]
    n = len(sel)
    m_all = [metrics[arm][r["step_id"]] for r in sel]
    out = {"capability_steps": n}
    for k in ("hit_at_1", "hit_at_3", "hit_at_5", "hit_at_10"):
        out[k] = sum(int(m[k]) for m in m_all)
        out[k + "_pct"] = round(100 * out[k] / n, 2) if n else None
    out["mrr_mean"] = round(sum(float(m["mrr_seq_level"]) for m in m_all) / n, 5) if n else None
    out["mrr_at_10_mean"] = round(sum(float(m["mrr_at_10"]) for m in m_all) / n, 5) if n else None
    return out

non_rescue = lambda r: r["rescue_dependent"] == "FALSE"
win_combos = defaultdict(int)
for r in rows:
    if r["capability"] == "INCLUDED" and r.get("winner"):
        win_combos[r["winner"]] += 1
comparison = {
    "pool": "R4_FIVE_MODEL_UNIFIED (gate-generated five-arm consumer-accepted tables of the 3B-verified parent pool, order-preserved, 382 steps)",
    "gate_ledger_sha256": gate["consumer_ledger_sha256"],
    "steps_scored_total": len(rows),
    "capability_steps": len(base),
    "no_discrimination_steps": sum(1 for r in rows if r["no_discrimination"] == "TRUE"),
    "rescue_dependent_steps": sum(1 for r in rows if r["rescue_dependent"] == "TRUE"),
    "arms": {arm: agg(arm) for arm in ARMS},
    "sensitivity_store_only_steps": {arm: agg(arm, non_rescue) for arm in ARMS},
    "per_step_wins": dict(sorted(win_combos.items(), key=lambda kv: -kv[1])),
    "reports": {f"{arm}/{ctx}": {k: reports[(arm, ctx)].get(k) for k in ("steps_total", "steps_formal", "steps_partial", "contract_violations_n")}
                for arm in ARMS for ctx in P.CTXS if (arm, ctx) in reports},
}
json.dump(comparison, open(f"{OUT}/FIVE_WAY_COMPARISON.json", "w"), indent=1)
cols = list(rows[0].keys())
with gzip.open(f"{OUT}/PER_STEP_FIVE_WAY.tsv.gz", "wt") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter="\t"); w.writeheader()
    for r in rows: w.writerow(r)

# ---------- 95-path coverage (calibrated on 3B parent) ----------
inv411 = list(csv.DictReader(open(P.R2 + "/inventory_r2/corrected/STEP_INVENTORY_411_CONTEXT_CORRECTED.tsv"), delimiter="\t"))
assert len(inv411) == 411
case_steps = defaultdict(list)
for r in inv411:
    case_steps[r["case_id"]].append(r)
policy_excluded = {r["step_occurrence_id"] for r in inv411
                   if r["stereo_omitted_9"] == "True" or r["status_class"].startswith("TRANSPORT")}
parent382 = set()
for ctx in P.CTXS:
    for s in json.load(open(f"{P.PKG}/inputs/{ctx}/THREE_B_VERIFIED_PARENT_POOL.json")):
        parent382.add(s["step_id"])
unified_ids = set(steps.keys())
formal_set = {arm: set(metrics[arm]) for arm in ARMS}

def paths_complete(scored_set):
    n = 0; cases = []
    for case, rs in sorted(case_steps.items()):
        all_ids = {r["step_occurrence_id"] for r in rs}
        need = all_ids - policy_excluded
        complete = need <= scored_set
        n += complete
        cases.append({"case_id": case, "steps": len(all_ids), "policy_excluded": len(all_ids & policy_excluded),
                      "required": len(need), "scored": len(need & scored_set), "complete": complete})
    return n, cases

calib, _ = paths_complete(parent382)
cov = {"calibration_3b_parent_paths_complete": calib, "calibration_expected": 82,
       "calibration_pass": calib == 82,
       "calibration_rule": "complete = every case step except stereo9+transport6 formally scored; unique rule reproducing 82 (R3 brute-force: stereo-only 79 / stereo+blocked 83 / all-exempt 87)"}
assert calib == 82, f"calibration failed: {calib} != 82"
for arm in ARMS:
    name = arm + "_this_round"
    n, cases = paths_complete(formal_set[arm])
    cov[name] = {"paths_complete": n, "steps_formal": len(formal_set[arm])}
    json.dump(cases, open(f"{OUT}/PATH_CASES_{name}.json", "w"), indent=1)
inter = set(unified_ids)
for arm in ARMS:
    inter &= formal_set[arm]
n, cases = paths_complete(inter)
cov["five_way_common"] = {"paths_complete": n, "steps_formal": len(inter)}
json.dump(cases, open(f"{OUT}/PATH_CASES_five_way_common.json", "w"), indent=1)
json.dump(cov, open(f"{OUT}/PATH_COVERAGE_95_FIVE.json", "w"), indent=1)

# ---------- formal 411/95 ----------
audit = {}
with open(f"{POOL}/STEP_RETENTION_AUDIT.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        audit[r["step_id"]] = r
out411 = []
for r in inv411:
    sid = r["step_occurrence_id"]
    o = dict(r)
    a = audit.get(sid)
    o["r4_unified_retained"] = (a["state"] if a else "NOT_IN_PARENT_382")
    o["r4_n_retained"] = a["n_retained"] if a else "0"
    o["r4_n_gold_retained"] = a["n_gold_retained"] if a else "0"
    o["r4_rescue_dependent"] = a["rescue_dependent"] if a else ""
    for arm in ARMS:
        tag = TAGS[arm]
        m = metrics[arm].get(sid)
        o[f"{tag}_formal_scored_r4"] = str(m is not None)
        o[f"{tag}_capability_r4"] = m["capability_denominator"] if m else ""
        o[f"{tag}_best_gold_rank_r4"] = (m.get("best_gold_rank", "") if m else "")
        o[f"{tag}_hit_at_1_r4"] = (m.get("hit_at_1", "") if m else "")
    scored_all = all(o[f"{TAGS[a]}_formal_scored_r4"] == "True" for a in ARMS)
    if scored_all:
        o["r4_formal_status"] = "FORMAL_SCORED_FIVE_MODEL_UNIFIED_POOL"
    elif a and a["state"] == "RETAINED":
        miss = [TAGS[a] for a in ARMS if o[f"{TAGS[a]}_formal_scored_r4"] != "True"]
        o["r4_formal_status"] = "RETAINED_NOT_FORMAL_" + "+".join(miss)
    elif r["stereo_omitted_9"] == "True":
        o["r4_formal_status"] = "OMITTED_STEREO_ONLY_USER_POLICY"
    elif r["status_class"].startswith("BLOCKED"):
        o["r4_formal_status"] = "BLOCKED_SCIENCE_NOT_SCORED"
    elif r["status_class"].startswith("TRANSPORT"):
        o["r4_formal_status"] = "TRANSPORT_SEPARATE_SCOPE_NOT_SCORED"
    elif sid in parent382:
        o["r4_formal_status"] = "IN_PARENT_NOT_ADMITTED_" + (a["typed_reason"] if a else "GATE_GAP")
    else:
        o["r4_formal_status"] = "NOT_IN_PARENT_382_NO_CONSUMABLE_GOLD_OR_POLICY"
    o["evidence_level_r4"] = "FORMAL_SCORER_REBUILT_UNIFIED_FIVE" if scored_all else o.get("evidence_level", "")
    out411.append(o)
p411 = f"{OUT}/STEP_STATUS_411_FORMAL_R4.tsv"
with open(p411, "w") as f:
    w = csv.DictWriter(f, fieldnames=list(out411[0].keys()), delimiter="\t"); w.writeheader(); w.writerows(out411)

cases95 = defaultdict(lambda: defaultdict(int))
for o in out411:
    c = cases95[o["case_id"]]
    c["steps"] += 1
    c["five_model_formal"] += o["r4_formal_status"] == "FORMAL_SCORED_FIVE_MODEL_UNIFIED_POOL"
    c["unified_retained"] += o["r4_unified_retained"] == "RETAINED"
    c["policy_excluded"] += o["stereo_omitted_9"] == "True" or o["status_class"].startswith(("BLOCKED", "TRANSPORT"))
    c["parent382"] += o["step_occurrence_id"] in parent382
ccols = ["case_id", "steps", "five_model_formal", "unified_retained", "parent382", "policy_excluded", "path_complete_five_way"]
p95 = f"{OUT}/CASE_95_FORMAL_R4.tsv"
uni_complete = {c["case_id"]: c["complete"] for c in json.load(open(f"{OUT}/PATH_CASES_five_way_common.json"))}
with open(p95, "w") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(ccols)
    for case in sorted(cases95):
        c = cases95[case]
        w.writerow([case, c["steps"], c["five_model_formal"], c["unified_retained"], c["parent382"], c["policy_excluded"], uni_complete.get(case, False)])
for p in (p411, p95):
    rr = list(csv.DictReader(open(p), delimiter="\t"))
    assert all(None not in x.values() for x in rr), f"non-rectangular {p}"
print(json.dumps({"comparison": {k: comparison[k] for k in ("steps_scored_total", "capability_steps", "no_discrimination_steps", "rescue_dependent_steps")},
                  "arms": comparison["arms"], "wins": comparison["per_step_wins"],
                  "path_coverage": cov,
                  "formal_411_status_counts": {k: sum(1 for o in out411 if o["r4_formal_status"] == k) for k in sorted({o["r4_formal_status"] for o in out411})}}, indent=1))
