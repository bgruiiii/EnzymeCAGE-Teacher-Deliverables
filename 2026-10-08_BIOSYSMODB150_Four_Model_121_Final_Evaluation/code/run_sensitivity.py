#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_sensitivity.py -- +/-5pp weight sensitivity for the FORMAL four-model run.

Copies ONLY the math rule from G9_reporting_preflight/sensitivity_spec.json
(base weights, renormalization rule, the 10 variant weight vectors). Does NOT
copy any SYNTHETIC score or the five-model lineup. Rebinds:
  scorer_binding -> actual frozen G3 SHAs
  model set      -> this round's four formal models
Recomputes per-model macro weighted totals from the SAME 484 per-slot layer
scores (per_slot_scores.jsonl); the scorer is NOT re-run.
"""
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.abspath(os.path.join(HERE, os.pardir))
EX = os.path.abspath(os.path.join(G9, os.pardir))
SPEC = os.path.join(EX, "G9_reporting_preflight", "sensitivity_spec.json")
SCORES = os.path.join(G9, "scores")

MODEL_ORDER = ["qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3", "kimi/kimi-k3"]
LAYERS = ["pathway", "smiles", "enzyme", "microbial_identity", "traits"]
FROZEN_G3 = {
    "g3_gate_sha256": "32c155201a360db8de229e40a9d9cb14bd152993fd0356fd8b0eb8c9001ccaa2",
    "g3_manifest_sha256": "24f1004cab0afca4707bbbd34f26f4b7ead074da723651af73f1fe95ad562e8a",
    "scorer_sha256": "a326eee63258cd0a2706bfd8a1dc6907d6f9fc6aa24b101a7192312c6ed39c61",
    "score_recipe_sha256": "8b79daf906f04e31589ad77bd93998f9a12649575bd4d476447c43028c338392",
    "validators_sha256": "c302164433e37127854eefdf25c44a5939201375873833d51846c3c127083899",
}

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


def variant_weights(base, layer, delta):
    """Regenerate the spec rule: w_layer += delta; remaining four scaled
    proportionally so the sum is exactly 100."""
    w = dict(base)
    w[layer] = base[layer] + delta
    rest = 100.0 - w[layer]
    others_sum = sum(base[k] for k in LAYERS if k != layer)
    for k in LAYERS:
        if k != layer:
            w[k] = base[k] * rest / others_sum
    return w


def main():
    spec = json.load(open(SPEC, encoding="utf-8"))
    base = spec["base_weights_pp"]
    check("base_weights_45_10_20_15_10",
          base == {"pathway": 45.0, "smiles": 10.0, "enzyme": 20.0,
                   "microbial_identity": 15.0, "traits": 10.0}, base)

    # regenerate all 10 variants from the rule and compare to spec table
    regen = {}
    for layer in LAYERS:
        for delta in (+5.0, -5.0):
            name = "%s%+dpp" % (layer, int(delta))
            regen[name] = variant_weights(base, layer, delta)
    check("variants_10", len(regen) == 10)
    for name, w in regen.items():
        check("variant_sum_100_%s" % name, abs(sum(w.values()) - 100.0) < 1e-9,
              sum(w.values()))
        for k in LAYERS:
            check("variant_match_spec_%s_%s" % (name, k),
                  abs(w[k] - spec["variants"][name][k]) < 1e-9,
                  "%s: %s vs %s" % (k, w[k], spec["variants"][name][k]))

    # per-slot layer scores from the frozen-scorer run (no scorer re-run)
    slots = []
    with open(os.path.join(SCORES, "per_slot_scores.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                slots.append(json.loads(line))
    check("slots_484", len(slots) == 484, len(slots))
    per_model_layers = {m: [] for m in MODEL_ORDER}
    for s in slots:
        per_model_layers[s["model_exact_id"]].append(
            {k: float(s["layers"][k]) for k in LAYERS})
    for m in MODEL_ORDER:
        check("model_rows_121_%s" % m, len(per_model_layers[m]) == 121)

    def macro(weights, m):
        vals = [sum(lv[k] * weights[k] for k in LAYERS) / 100.0
                for lv in per_model_layers[m]]
        return sum(vals) / len(vals)

    base_macro = {m: macro(base, m) for m in MODEL_ORDER}
    base_rank = {m: i + 1 for i, m in enumerate(
        sorted(MODEL_ORDER, key=lambda x: -base_macro[x]))}

    # sanity: base recomputation must equal the scored science_100 macro
    # within the frozen scorer's 2-decimal rounding of layers/science
    scored_macro = {}
    for s in slots:
        scored_macro.setdefault(s["model_exact_id"], []).append(s["science_100"])
    for m in MODEL_ORDER:
        check("base_equals_scored_%s" % m,
              abs(base_macro[m] - sum(scored_macro[m]) / 121.0) < 0.005,
              "%s vs %s" % (base_macro[m], sum(scored_macro[m]) / 121.0))

    rows_out = []
    for name in sorted(regen):
        w = regen[name]
        vm = {m: macro(w, m) for m in MODEL_ORDER}
        vrank = {m: i + 1 for i, m in enumerate(
            sorted(MODEL_ORDER, key=lambda x: -vm[x]))}
        for m in MODEL_ORDER:
            rows_out.append({
                "variant": name, "model_exact_id": m,
                "weights_pathway": w["pathway"], "weights_smiles": w["smiles"],
                "weights_enzyme": w["enzyme"],
                "weights_microbial_identity": w["microbial_identity"],
                "weights_traits": w["traits"],
                "macro_weighted_total": vm[m],
                "rank_in_variant": vrank[m], "rank_at_base": base_rank[m],
                "delta_vs_base": vm[m] - base_macro[m],
                "rank_changed": "Y" if vrank[m] != base_rank[m] else "N",
            })
    rows_out.sort(key=lambda r: (r["variant"], r["model_exact_id"]))
    out_path = os.path.join(SCORES, "sensitivity_results.tsv")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        wcsv = csv.DictWriter(fh, fieldnames=list(rows_out[0]), delimiter="\t",
                              lineterminator="\n")
        wcsv.writeheader()
        for r in rows_out:
            rr = dict(r)
            rr["macro_weighted_total"] = "%.4f" % rr["macro_weighted_total"]
            rr["delta_vs_base"] = "%+.4f" % rr["delta_vs_base"]
            wcsv.writerow(rr)

    n_changed = sum(1 for r in rows_out if r["rank_changed"] == "Y")
    stability = "STABLE_ALL_10_VARIANTS" if n_changed == 0 else (
        "RANK_CHANGES_IN_%d_OF_40_MODEL_VARIANT_CELLS" % n_changed)

    bound = {
        "derived_from": "G9_reporting_preflight/sensitivity_spec.json (math rule only)",
        "spec_sha256": sha256_file(SPEC),
        "copied": ["base_weights_pp", "renorm rule", "10 variant weight vectors"],
        "not_copied": ["SYNTHETIC scores", "five-model lineup",
                       "fixture_label SYNTHETIC_OFFLINE_FIXTURE"],
        "scorer_binding": FROZEN_G3,
        "model_set": MODEL_ORDER,
        "rule": spec["rule"],
        "renorm": spec["renorm"],
        "variants": regen,
        "fixture_label": "FORMAL_FOUR_MODEL_121_20261008",
        "api_calls": 0,
        "scorer_rerun": False,
        "layer_score_source": {
            "path": "scores/per_slot_scores.jsonl",
            "sha256": sha256_file(os.path.join(SCORES, "per_slot_scores.jsonl")),
        },
        "base_macro_weighted_total": base_macro,
        "base_ranking": base_rank,
        "ranking_stability": stability,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": CHECKS[0], "failures": len(FAILURES), "failure_list": FAILURES,
    }
    if FAILURES:
        print("SENSITIVITY: FAIL (%d of %d)" % (len(FAILURES), CHECKS[0]))
        return 1
    with open(os.path.join(SCORES, "sensitivity_spec_bound.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(bound, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print("SENSITIVITY: PASS (%d checks); base ranking %s; stability=%s"
          % (CHECKS[0],
             " > ".join("%s(%.4f)" % (m, base_macro[m])
                        for m in sorted(MODEL_ORDER, key=lambda x: -base_macro[x])),
             stability))
    return 0


if __name__ == "__main__":
    sys.exit(main())
