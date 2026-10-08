#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compute_usage_costs.py -- per-model usage/duration stats and formal cost
recomputed from parse_meta usage (read-only), with basis disclosure and
cross-checks against the authoritative ledgers and local audits.

Accounting basis (identical to the frozen runners' budget guard):
  per terminal call: (prompt_tokens*in_price + completion_tokens*out_price)/1e6
  held slot (no response): settled at worst-case reserve
    (PROMPT_BOUND(10000)*in_price + MAX_TOKENS(65536)*out_price)/1e6
  unit prices CNY per 1M tokens: qwen3.8-max 12/36, deepseek-v4.1-flash 2/8,
    ZHIPU/GLM-5.3 8/28 (release/G8P1_FORMAL_STAGE_RELEASE.json budget guard);
    kimi/kimi-k3 20/100 (release/G8P2_FORMAL_RELEASE.json).
  Probe/smoke/pilot are engineering costs, NOT part of the formal total and
  NOT deducted from it. .tmp/.lock ledger snapshots are ignored; only the
  authoritative global_calls.json / kimi_calls.json are read.
"""
import csv
import hashlib
import json
import os
import statistics
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.abspath(os.path.join(HERE, os.pardir))
SCORES = os.path.join(G9, "scores")

MODEL_ORDER = ["qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3", "kimi/kimi-k3"]
PRICES = {"qwen3.8-max": (12.0, 36.0), "deepseek-v4.1-flash": (2.0, 8.0),
          "ZHIPU/GLM-5.3": (8.0, 28.0), "kimi/kimi-k3": (20.0, 100.0)}
HELD_RESERVE = {("qwen3.8-max", "G8P1-S208"): 2.479296,
                ("kimi/kimi-k3", "G8P2-K042"): 6.7536}
# Local-audit reference values for cross-check (formal terminal usage cost).
AUDIT_REF = {"qwen3.8-max": 136.3089, "deepseek-v4.1-flash": 25.9615,
             "ZHIPU/GLM-5.3": 17.7004}
AUDIT_REF_KIMI_TOTAL_INCL_HELD = 435.86014
AUDIT_REF_TOTAL_APPROX = 618.31
LEDGER_REF = {"three_model_spent": 184.780276, "three_model_committed": 377,
              "kimi_spent": 435.86014, "kimi_committed": 121}

FAILURES = []
CHECKS = [0]


def check(name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILURES.append({"check": name, "detail": str(detail)[:300]})
        print("  [FAIL] %s :: %s" % (name, str(detail)[:200]))
    return ok


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def pctl(sorted_vals, q):
    if not sorted_vals:
        return None
    idx = max(0, min(len(sorted_vals) - 1, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[idx]


def stats(vals):
    if not vals:
        return {k: None for k in ("mean", "median", "p90", "max", "n")}
    sv = sorted(vals)
    return {"n": len(sv), "mean": sum(sv) / len(sv),
            "median": statistics.median(sv), "p90": pctl(sv, 0.9), "max": sv[-1]}


def main():
    with open(os.path.join(G9, "FORMAL_484_SLOT_INDEX.tsv"), encoding="utf-8",
              newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    check("rows_484", len(rows) == 484)

    # authoritative ledgers only; .tmp/.lock ignored by construction
    tm_ledger = json.load(open(os.path.join(
        G9, "source", "three_model", "ledger", "global_calls.json"),
        encoding="utf-8"))
    km_ledger = json.load(open(os.path.join(
        G9, "source", "kimi", "ledger", "kimi_calls.json"), encoding="utf-8"))
    check("ledger_three_model", tm_ledger["total_committed"] == 377
          and abs(tm_ledger["spent_cny_est"] - 184.780276) < 1e-6)
    check("ledger_kimi", km_ledger["total_committed"] == 121
          and abs(km_ledger["spent_cny_est"] - 435.86014) < 1e-6)
    check("ledger_held_reserves",
          tm_ledger["reconciled_held"][0]["charged_reserve_cny"] == 2.479296
          and km_ledger["reconciled_held"][0]["charged_reserve_cny"] == 6.7536)

    out_rows = []
    totals = {}
    for m in MODEL_ORDER:
        mr = [r for r in rows if r["model_exact_id"] == m]
        usable = sum(1 for r in mr if r["engineering_class"] == "USABLE")
        inv = sum(1 for r in mr if r["engineering_class"] == "INVALID_JSON")
        le = sum(1 for r in mr if r["engineering_class"] == "LENGTH_EMPTY")
        held = sum(1 for r in mr if r["engineering_class"] == "RESULT_UNKNOWN_HELD")
        term = [r for r in mr if r["terminal"] == "True"]
        toks = stats([int(r["completion_tokens"]) for r in term])
        ptoks = stats([int(r["prompt_tokens"]) for r in term])
        durs = stats([float(r["duration_seconds"]) for r in term])
        ip, op = PRICES[m]
        usage_cost = sum((int(r["prompt_tokens"]) * ip
                          + int(r["completion_tokens"]) * op) / 1e6 for r in term)
        held_cost = sum(v for (mm, _), v in HELD_RESERVE.items() if mm == m)
        total = usage_cost + held_cost
        totals[m] = {"usage_cost": usage_cost, "held_reserve": held_cost,
                     "total": total}
        out_rows.append({
            "model_exact_id": m, "slots": len(mr), "usable": usable,
            "invalid_json": inv, "length_empty": le, "held": held,
            "terminal_measured_n": toks["n"],
            "completion_tokens_mean": toks["mean"],
            "completion_tokens_median": toks["median"],
            "completion_tokens_p90": toks["p90"],
            "completion_tokens_max": toks["max"],
            "prompt_tokens_mean": ptoks["mean"],
            "duration_s_mean": durs["mean"], "duration_s_median": durs["median"],
            "duration_s_p90": durs["p90"], "duration_s_max": durs["max"],
            "unit_price_cny_per_1M_in_out": "%g/%g" % (ip, op),
            "formal_usage_cost_cny": usage_cost,
            "held_reserve_cny": held_cost,
            "formal_total_cost_cny": total,
        })

    # cross-checks against audits
    for m, ref in AUDIT_REF.items():
        check("audit_cost_%s" % m, abs(totals[m]["usage_cost"] - ref) < 0.002,
              "%s vs audit %s" % (totals[m]["usage_cost"], ref))
    check("audit_kimi_total",
          abs(totals["kimi/kimi-k3"]["total"] - AUDIT_REF_KIMI_TOTAL_INCL_HELD) < 0.002,
          totals["kimi/kimi-k3"]["total"])
    grand = sum(t["total"] for t in totals.values())
    check("audit_grand_total_618_31", abs(grand - AUDIT_REF_TOTAL_APPROX) < 0.02,
          grand)

    def f4(v):
        return "" if v is None else "%.4f" % v

    tsv_path = os.path.join(SCORES, "usage_cost_summary.tsv")
    with open(tsv_path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0]), delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        for r in out_rows:
            rr = dict(r)
            for k in list(rr):
                if isinstance(rr[k], float):
                    rr[k] = f4(rr[k])
            w.writerow(rr)

    summary = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "api_calls": 0,
        "basis": {
            "formula": "terminal: (prompt*in + completion*out)/1e6; held: worst-case reserve (10000*in + 65536*out)/1e6",
            "unit_price_cny_per_1M": {m: {"input": PRICES[m][0], "output": PRICES[m][1]}
                                      for m in MODEL_ORDER},
            "price_source": [
                "source/three_model/release/G8P1_FORMAL_STAGE_RELEASE.json budget.unit_price_cny_per_1M",
                "source/kimi/release/G8P2_FORMAL_RELEASE.json budget.unit_price_cny_per_1M"],
            "held_reserves_cny": {"G8P1-S208": 2.479296, "G8P2-K042": 6.7536},
            "excluded": "probe/smoke/pilot engineering calls are excluded from the formal total and not deducted",
            "ignored_runtime_files": ["global_calls.json.tmp", "global_calls.json.lock",
                                      "kimi_calls.json.tmp", "kimi_calls.json.lock",
                                      ".runner.lock files"],
            "quantile_method": "nearest-rank on sorted terminal values (p90 index = round(0.9*(n-1)))",
        },
        "per_model": {r["model_exact_id"]: r for r in out_rows},
        "formal_grand_total_cny": grand,
        "ledger_cross_check": {
            "three_model_ledger_spent_cny": tm_ledger["spent_cny_est"],
            "three_model_formal_portion_cny":
                totals["qwen3.8-max"]["total"] + totals["deepseek-v4.1-flash"]["total"]
                + totals["ZHIPU/GLM-5.3"]["total"],
            "three_model_nonformal_engineering_cny":
                tm_ledger["spent_cny_est"] - (
                    totals["qwen3.8-max"]["total"]
                    + totals["deepseek-v4.1-flash"]["total"]
                    + totals["ZHIPU/GLM-5.3"]["total"]),
            "kimi_ledger_spent_cny": km_ledger["spent_cny_est"],
            "kimi_recomputed_total_cny": totals["kimi/kimi-k3"]["total"],
            "ledger_sha256": {
                "global_calls.json": sha256_file(os.path.join(
                    G9, "source", "three_model", "ledger", "global_calls.json")),
                "kimi_calls.json": sha256_file(os.path.join(
                    G9, "source", "kimi", "ledger", "kimi_calls.json"))},
        },
        "audit_reference_match": {
            "qwen_136.3089": abs(totals["qwen3.8-max"]["usage_cost"] - 136.3089) < 0.002,
            "deepseek_25.9615": abs(totals["deepseek-v4.1-flash"]["usage_cost"] - 25.9615) < 0.002,
            "glm_17.7004": abs(totals["ZHIPU/GLM-5.3"]["usage_cost"] - 17.7004) < 0.002,
            "kimi_435.86014_incl_held": abs(totals["kimi/kimi-k3"]["total"] - 435.86014) < 0.002,
            "grand_approx_618.31": abs(grand - 618.31) < 0.02,
        },
        "checks": CHECKS[0], "failures": len(FAILURES), "failure_list": FAILURES,
    }
    if FAILURES:
        print("USAGE/COST: FAIL (%d of %d)" % (len(FAILURES), CHECKS[0]))
        return 1
    with open(os.path.join(SCORES, "usage_cost_summary.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print("USAGE/COST: PASS (%d checks); formal grand total = %.4f CNY" %
          (CHECKS[0], grand))
    for m in MODEL_ORDER:
        t = totals[m]
        print("  %-24s usage=%.4f held=%.6f total=%.4f"
              % (m, t["usage_cost"], t["held_reserve"], t["total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
