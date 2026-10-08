#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score_formal_484.py -- G9 formal scoring adapter over the FROZEN G3 scorer.

API_CALLS=0. The frozen scorer is imported read-only and NEVER modified; no
pre-cleaning, field completion, name substitution or structural rewriting of
any answer is performed. Usable slots: raw visible JSON is json.load'ed
directly and passed to score_answer(case_id, answer, parse_status="VALID").
The 15 non-usable slots call the SAME frozen function's non-dict path
score_answer(case_id, None, parse_status=<reason>); their five science layers
and science total count 0 and stay in the fixed 121 denominator; their
evidence/abstention fields are written NA (never fake zero claims).

Primary science result: per-model macro-case mean over fixed 121 rows.
Layer weights strictly 45/10/20/15/10 (asserted against scorer output).
Usable-only means are reported but are NOT the primary ranking.
"""
import csv
import hashlib
import importlib
import json
import os
import statistics
import sys
from datetime import datetime, timezone

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.abspath(os.path.join(HERE, os.pardir))
EX = os.path.abspath(os.path.join(G9, os.pardir))
G3 = os.path.join(EX, "G3_scorer")
SCORES = os.path.join(G9, "scores")

MODEL_ORDER = ["qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3", "kimi/kimi-k3"]
LAYERS = ["pathway", "smiles", "enzyme", "microbial_identity", "traits"]
WEIGHTS = {"pathway": 45.0, "smiles": 10.0, "enzyme": 20.0,
           "microbial_identity": 15.0, "traits": 10.0}
FIXTURE_LABEL = "FORMAL_FOUR_MODEL_121_20261008"
REASON_VALUES = {"INVALID_JSON", "LENGTH_EMPTY", "RESULT_UNKNOWN_HELD"}

FROZEN_SHA = {
    "scorer.py": "a326eee63258cd0a2706bfd8a1dc6907d6f9fc6aa24b101a7192312c6ed39c61",
    "validators.py": "c302164433e37127854eefdf25c44a5939201375873833d51846c3c127083899",
    "score_recipe.md": "8b79daf906f04e31589ad77bd93998f9a12649575bd4d476447c43028c338392",
    "G3_PREPARATION_MANIFEST.json":
        "24f1004cab0afca4707bbbd34f26f4b7ead074da723651af73f1fe95ad562e8a",
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


def r4(x):
    return "" if x is None else "%.4f" % x


def mean(vals):
    return sum(vals) / len(vals) if vals else None


def pctl(sorted_vals, q):
    """Nearest-rank P90 on a sorted list (documented simple quantile)."""
    if not sorted_vals:
        return None
    idx = max(0, min(len(sorted_vals) - 1,
                     int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[idx]


def main():
    # frozen scorer hard binding, re-asserted at scoring time
    for fname, digest in FROZEN_SHA.items():
        check("frozen_%s_sha" % fname,
              sha256_file(os.path.join(G3, fname)) == digest)
    check("frozen_g1_manifest", sha256_file(os.path.join(
        EX, "G1_gold", "G1_gold.manifest.json")) ==
        "c424763cd4c38fcaac1b178979efb3f18f2b77039369ab6b8c709eab42dce06e")
    check("frozen_g2_manifest", sha256_file(os.path.join(
        EX, "G2_questions", "G2_questions.manifest.json")) ==
        "ae5780e546bb259d0133ba63157ecfe2f3d3071fc37fc2c0050629f7fe575520")
    if FAILURES:
        print("BLOCKED_FROZEN_SCORER")
        return 2

    sys.path.insert(0, G3)
    scorer = importlib.import_module("scorer")
    check("scorer_weight_binding_45_10_20_15_10",
          scorer.LAYERS == {k: WEIGHTS[k] / 100.0 for k in LAYERS},
          scorer.LAYERS)

    with open(os.path.join(G9, "FORMAL_484_SLOT_INDEX.tsv"), encoding="utf-8",
              newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    check("index_rows_484", len(rows) == 484, len(rows))
    check("index_usable_469",
          sum(1 for r in rows if r["engineering_class"] == "USABLE") == 469)

    def score_row(r):
        eclass = r["engineering_class"]
        if eclass == "USABLE":
            path = os.path.join(G9, r["visible_answer_relpath"])
            with open(path, encoding="utf-8") as fh:
                answer = json.load(fh)          # direct json.load, no repair
            res = scorer.score_answer(r["case_id"], answer, parse_status="VALID")
        else:
            check("reason_value_%s" % r["slot"], eclass in REASON_VALUES, eclass)
            res = scorer.score_answer(r["case_id"], None, parse_status=eclass)
        return res

    # ---- staged run: first 3 usable cases per model, structure review ----
    staged = []
    for m in MODEL_ORDER:
        mr = [r for r in rows if r["model_exact_id"] == m
              and r["engineering_class"] == "USABLE"][:3]
        for r in mr:
            res = score_row(r)
            ok = (isinstance(res.get("layers"), dict)
                  and set(res["layers"]) == set(LAYERS)
                  and isinstance(res.get("science_100"), float)
                  and res.get("engineering", {}).get("json_parse_status") == "VALID"
                  and isinstance(res.get("evidence_axis"), dict)
                  and isinstance(res.get("abstention_axis"), dict)
                  and isinstance(res.get("alignment"), dict))
            check("staged_structure_%s_%s" % (m, r["case_id"]), ok)
            w = sum(res["layers"][k] * WEIGHTS[k] for k in LAYERS) / 100.0
            check("staged_weight_math_%s_%s" % (m, r["case_id"]),
                  abs(w - res["science_100"]) < 0.011, "%s vs %s" % (w, res["science_100"]))
            staged.append({"model": m, "case_id": r["case_id"], "slot": r["slot"],
                           "science_100": res["science_100"],
                           "layers": res["layers"]})
    if FAILURES:
        print("STAGED REVIEW FAILED; full run aborted")
        return 2
    with open(os.path.join(G9, "work", "staged_first3_per_model.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(staged, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("[staged] first 3 usable cases per model scored; structure OK")

    # ---- full 484 ----
    os.makedirs(SCORES, exist_ok=True)
    per_slot_path = os.path.join(SCORES, "per_slot_scores.jsonl")
    results = {}
    with open(per_slot_path, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            res = score_row(r)
            eclass = r["engineering_class"]
            if eclass != "USABLE":
                ok = (all(res["layers"][k] == 0.0 for k in LAYERS)
                      and res["science_100"] == 0.0
                      and "evidence_axis" not in res
                      and "abstention_axis" not in res
                      and res["engineering"]["json_parse_status"] == eclass)
                check("nonusable_zero_path_%s" % r["slot"], ok)
            else:
                w = sum(res["layers"][k] * WEIGHTS[k] for k in LAYERS) / 100.0
                check("weight_math_%s" % r["slot"],
                      abs(w - res["science_100"]) < 0.011,
                      "%s vs %s" % (w, res["science_100"]))
            rec = {
                "slot": r["slot"], "case_id": r["case_id"],
                "model_exact_id": r["model_exact_id"],
                "source_package": r["source_package"],
                "source_tar_sha256": r["source_tar_sha256"],
                "engineering_class": eclass,
                "parse_status": res["engineering"]["json_parse_status"],
                "request_body_sha256": r["request_body_sha256"],
                "raw_stream_sha256": r["raw_stream_sha256"],
                "visible_answer_sha256": r["visible_answer_sha256"],
                "science_100": res["science_100"],
                "layers": res["layers"],
                "result": res,
            }
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
            results[(r["case_id"], r["model_exact_id"])] = (r, res)
    check("per_slot_lines_484", len(results) == 484, len(results))

    # ---- per_case_scores.tsv (template columns; scores on scorer-native 0-100) ----
    case_cols = ["case_id", "model_exact_id", "pathway", "smiles", "enzyme",
                 "microbial_identity", "traits", "weighted_total", "json_valid",
                 "schema_valid", "truncated", "evidence_verified_n",
                 "evidence_unverified_n", "overclaim_flags", "recall_macro",
                 "completeness", "abstention_status", "fixture_label",
                 "engineering_class", "slot"]
    g2_cases = []
    with open(os.path.join(EX, "G2_questions", "main_cases.jsonl"),
              encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                g2_cases.append(json.loads(line)["case_id"])
    with open(os.path.join(SCORES, "per_case_scores.tsv"), "w",
              encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=case_cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        for case in g2_cases:
            for m in MODEL_ORDER:
                r, res = results[(case, m)]
                usable = r["engineering_class"] == "USABLE"
                if usable:
                    al = res["alignment"]
                    n_match = len(al["matches"])
                    n_gold = n_match + len(al["missing_gold_steps"])
                    recall = (n_match / n_gold) if n_gold else None
                    td = res.get("traits_detail") or {}
                    comp = td.get("completeness")
                    ev = res["evidence_axis"]
                    ab = res["abstention_axis"]
                    abst = ("NULLS_%d_OVER_%d" % (ab["null_abstentions"],
                                                  ab["overclaims"]))
                    row = {
                        "evidence_verified_n": ev["verified_correct"],
                        "evidence_unverified_n": ev["unverified_correct"],
                        "overclaim_flags": ab["overclaims"],
                        "recall_macro": r4(recall),
                        "completeness": r4(comp) if comp is not None else "NA",
                        "abstention_status": abst,
                    }
                else:
                    row = {
                        "evidence_verified_n": "NA",
                        "evidence_unverified_n": "NA",
                        "overclaim_flags": "NA",
                        "recall_macro": "NA",
                        "completeness": "NA",
                        "abstention_status": "NA_NOT_USABLE",
                    }
                w.writerow({
                    "case_id": case, "model_exact_id": m,
                    "pathway": r4(res["layers"]["pathway"]),
                    "smiles": r4(res["layers"]["smiles"]),
                    "enzyme": r4(res["layers"]["enzyme"]),
                    "microbial_identity": r4(res["layers"]["microbial_identity"]),
                    "traits": r4(res["layers"]["traits"]),
                    "weighted_total": r4(res["science_100"]),
                    "json_valid": "Y" if r["json_valid"] == "True" else "N",
                    "schema_valid": "Y" if r["schema_valid"] == "True" else "N",
                    "truncated": "Y" if r["finish_length"] == "True" else "N",
                    "fixture_label": FIXTURE_LABEL,
                    "engineering_class": r["engineering_class"],
                    "slot": r["slot"],
                    **row})

    # ---- per-model aggregation (fixed 121 denominator = primary) ----
    def agg(rs_pairs):
        out = {}
        for k in LAYERS:
            out["macro_" + k] = mean([res["layers"][k] for _, res in rs_pairs])
        out["macro_weighted_total"] = mean([res["science_100"] for _, res in rs_pairs])
        return out

    summary = {}
    for m in MODEL_ORDER:
        pairs = [results[(c, m)] for c in g2_cases]
        usable_pairs = [(r, res) for r, res in pairs
                        if r["engineering_class"] == "USABLE"]
        s = agg(pairs)
        s["usable_only"] = agg(usable_pairs)
        s["n_cases"] = len(pairs)
        s["usable_n"] = len(usable_pairs)
        s["json_valid_n"] = sum(1 for r, _ in pairs if r["json_valid"] == "True")
        s["schema_valid_n"] = sum(1 for r, _ in pairs if r["schema_valid"] == "True")
        s["truncated_n"] = sum(1 for r, _ in pairs if r["finish_length"] == "True")
        s["invalid_json_n"] = sum(1 for r, _ in pairs
                                  if r["engineering_class"] == "INVALID_JSON")
        s["length_empty_n"] = sum(1 for r, _ in pairs
                                  if r["engineering_class"] == "LENGTH_EMPTY")
        s["held_n"] = sum(1 for r, _ in pairs
                          if r["engineering_class"] == "RESULT_UNKNOWN_HELD")
        summary[m] = s

    sum_cols = (["model_exact_id", "n_cases", "macro_pathway", "macro_smiles",
                 "macro_enzyme", "macro_microbial_identity", "macro_traits",
                 "macro_weighted_total", "micro_weighted_count_note",
                 "json_valid_rate", "schema_valid_rate", "truncation_rate",
                 "main_report_axis", "aux_report_axis", "fixture_label"]
                + ["usable_n", "invalid_json_n", "length_empty_n", "held_n",
                   "usable_only_macro_weighted_total",
                   "usable_only_macro_pathway", "usable_only_macro_smiles",
                   "usable_only_macro_enzyme",
                   "usable_only_macro_microbial_identity",
                   "usable_only_macro_traits"])
    with open(os.path.join(SCORES, "per_model_summary.tsv"), "w",
              encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=sum_cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        for m in MODEL_ORDER:
            s = summary[m]
            w.writerow({
                "model_exact_id": m, "n_cases": s["n_cases"],
                "macro_pathway": r4(s["macro_pathway"]),
                "macro_smiles": r4(s["macro_smiles"]),
                "macro_enzyme": r4(s["macro_enzyme"]),
                "macro_microbial_identity": r4(s["macro_microbial_identity"]),
                "macro_traits": r4(s["macro_traits"]),
                "macro_weighted_total": r4(s["macro_weighted_total"]),
                "micro_weighted_count_note":
                    "micro counts auxiliary only; primary=macro over fixed 121",
                "json_valid_rate": r4(s["json_valid_n"] / 121.0),
                "schema_valid_rate": r4(s["schema_valid_n"] / 121.0),
                "truncation_rate": r4(s["truncated_n"] / 121.0),
                "main_report_axis": "macro_case_average_fixed_121",
                "aux_report_axis": "usable_only_mean_and_micro_counts",
                "fixture_label": FIXTURE_LABEL,
                "usable_n": s["usable_n"],
                "invalid_json_n": s["invalid_json_n"],
                "length_empty_n": s["length_empty_n"],
                "held_n": s["held_n"],
                "usable_only_macro_weighted_total":
                    r4(s["usable_only"]["macro_weighted_total"]),
                "usable_only_macro_pathway": r4(s["usable_only"]["macro_pathway"]),
                "usable_only_macro_smiles": r4(s["usable_only"]["macro_smiles"]),
                "usable_only_macro_enzyme": r4(s["usable_only"]["macro_enzyme"]),
                "usable_only_macro_microbial_identity":
                    r4(s["usable_only"]["macro_microbial_identity"]),
                "usable_only_macro_traits": r4(s["usable_only"]["macro_traits"]),
            })

    # ---- evidence axis (separate; never folded into science) ----
    with open(os.path.join(SCORES, "evidence_axis.tsv"), "w",
              encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["model_exact_id", "citations_verified_n",
                    "citations_unverified_n", "overclaim_n",
                    "f5_accession_illegal_n", "f5_local_lookup_absent_n",
                    "evidence_chain_complete_rate", "evidence_hallucination_n",
                    "ref_missing_n", "internal_knowledge_n", "model_inference_n",
                    "separate_from_science_score", "fixture_label"])
        for m in MODEL_ORDER:
            pairs = [results[(c, m)] for c in g2_cases]
            us = [(r, res) for r, res in pairs if r["engineering_class"] == "USABLE"]
            ver = sum(res["evidence_axis"]["verified_correct"] for _, res in us)
            unv = sum(res["evidence_axis"]["unverified_correct"] for _, res in us)
            over = sum(res["abstention_axis"]["overclaims"] for _, res in us)
            hall = sum(res["evidence_axis"]["evidence_hallucination"] for _, res in us)
            refm = sum(res["evidence_axis"]["ref_missing"] for _, res in us)
            ik = sum(res["evidence_axis"]["internal_knowledge"] for _, res in us)
            mi = sum(res["evidence_axis"]["model_inference"] for _, res in us)
            clean = sum(1 for _, res in us
                        if res["evidence_axis"]["evidence_hallucination"] == 0
                        and res["evidence_axis"]["ref_missing"] == 0)
            w.writerow([m, ver, unv, over,
                        "NA_SCORER_NOT_EMITTED", "NA_SCORER_NOT_EMITTED",
                        r4(clean / len(us)) if us else "NA",
                        hall, refm, ik, mi, "Y", FIXTURE_LABEL])

    # ---- abstention axis (null = recall miss, NEVER overclaim) ----
    with open(os.path.join(SCORES, "abstention_axis.tsv"), "w",
              encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["model_exact_id", "gold_steps_recall_missed_total",
                    "null_abstentions_total", "overclaims_total",
                    "cases_with_null_abstention", "cases_with_overclaim",
                    "mean_recall_macro_usable", "non_usable_slots_NA",
                    "separate_from_science_score", "fixture_label"])
        for m in MODEL_ORDER:
            pairs = [results[(c, m)] for c in g2_cases]
            us = [(r, res) for r, res in pairs if r["engineering_class"] == "USABLE"]
            miss = sum(res["abstention_axis"]["gold_steps_recall_missed"]
                       for _, res in us)
            nulls = sum(res["abstention_axis"]["null_abstentions"] for _, res in us)
            over = sum(res["abstention_axis"]["overclaims"] for _, res in us)
            cn = sum(1 for _, res in us
                     if res["abstention_axis"]["null_abstentions"] > 0)
            co = sum(1 for _, res in us if res["abstention_axis"]["overclaims"] > 0)
            recalls = []
            for _, res in us:
                al = res["alignment"]
                n_gold = len(al["matches"]) + len(al["missing_gold_steps"])
                if n_gold:
                    recalls.append(len(al["matches"]) / n_gold)
            w.writerow([m, miss, nulls, over, cn, co,
                        r4(mean(recalls)) if recalls else "NA",
                        121 - len(us), "Y", FIXTURE_LABEL])

    # ---- engineering axis (tokens/latency from formal parse_meta usage) ----
    with open(os.path.join(SCORES, "engineering_axis.tsv"), "w",
              encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["model_exact_id", "tokens_mean", "tokens_median",
                    "tokens_p90", "tokens_max", "latency_s_mean",
                    "latency_s_median", "latency_s_p90", "latency_s_max",
                    "http_429_n", "http_5xx_n", "timeout_n",
                    "stream_truncation_n", "finish_length_n", "retry_total",
                    "terminal_n_measured", "separate_from_science_score",
                    "fixture_label"])
        for m in MODEL_ORDER:
            pairs = [results[(c, m)] for c in g2_cases]
            toks = sorted(int(r["completion_tokens"]) for r, _ in pairs
                          if r["terminal"] == "True" and r["completion_tokens"])
            durs = sorted(float(r["duration_seconds"]) for r, _ in pairs
                          if r["terminal"] == "True" and r["duration_seconds"])
            http = [int(r["http_status"]) for r, _ in pairs if r["http_status"]]
            flen = sum(1 for r, _ in pairs if r["finish_length"] == "True")
            w.writerow([m,
                        r4(mean(toks)) if toks else "NA",
                        r4(statistics.median(toks)) if toks else "NA",
                        r4(pctl(toks, 0.9)) if toks else "NA",
                        max(toks) if toks else "NA",
                        r4(mean(durs)) if durs else "NA",
                        r4(statistics.median(durs)) if durs else "NA",
                        r4(pctl(durs, 0.9)) if durs else "NA",
                        r4(max(durs)) if durs else "NA",
                        sum(1 for h in http if h == 429),
                        sum(1 for h in http if 500 <= h < 600),
                        0, 0, flen, 0, len(toks), "Y", FIXTURE_LABEL])

    # ---- failure registry (15 rows; kept in 121 denominator, score 0) ----
    with open(os.path.join(SCORES, "failure_registry.tsv"), "w",
              encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["model_exact_id", "case_id", "slot", "engineering_class",
                    "failure_reason", "http_status", "finish_reason",
                    "visible_len", "completion_tokens", "reasoning_tokens",
                    "provider_request_id", "committed_utc",
                    "disposition", "rerun", "fixture_label"])
        n_fail = 0
        for m in MODEL_ORDER:
            for c in g2_cases:
                r, res = results[(c, m)]
                if r["engineering_class"] == "USABLE":
                    continue
                n_fail += 1
                w.writerow([m, c, r["slot"], r["engineering_class"],
                            r["engineering_class"], r["http_status"] or "NA_HELD",
                            r["finish_reason"] or "NA_HELD",
                            r["visible_len"] or "NA_HELD",
                            r["completion_tokens"] or "NA_HELD",
                            r["reasoning_tokens"] or "NA_HELD",
                            r["provider_request_id"], r["committed_utc"],
                            "KEPT_IN_121_DENOMINATOR_SCIENCE_ZERO", "false",
                            FIXTURE_LABEL])
        check("failure_registry_15", n_fail == 15, n_fail)

    # ---- fingerprint summary (terminal slots only; kimi 5 strata; others
    #      NOT_EXPOSED; held slots carry NA_NO_RESPONSE and are disclosed in
    #      the failure registry, never silently merged into a stratum) ----
    with open(os.path.join(SCORES, "fingerprint_summary.tsv"), "w",
              encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["model_exact_id", "system_fingerprint", "n_terminal",
                    "n_usable", "n_non_usable", "completion_tokens_mean",
                    "duration_s_mean", "duration_s_median", "duration_s_p90",
                    "duration_s_max", "fixture_label"])
        strata = {}
        for m in MODEL_ORDER:
            for c in g2_cases:
                r, _ = results[(c, m)]
                if r["terminal"] != "True":
                    continue
                strata.setdefault((m, r["system_fingerprint"]), []).append(r)
        for (m, fp), rs in sorted(strata.items()):
            toks = [int(r["completion_tokens"]) for r in rs
                    if r["completion_tokens"]]
            durs = sorted(float(r["duration_seconds"]) for r in rs
                          if r["duration_seconds"])
            w.writerow([m, fp, len(rs),
                        sum(1 for r in rs if r["engineering_class"] == "USABLE"),
                        sum(1 for r in rs if r["engineering_class"] != "USABLE"),
                        r4(mean(toks)) if toks else "NA",
                        r4(mean(durs)) if durs else "NA",
                        r4(statistics.median(durs)) if durs else "NA",
                        r4(pctl(durs, 0.9)) if durs else "NA",
                        r4(max(durs)) if durs else "NA",
                        FIXTURE_LABEL])
        check("kimi_five_terminal_strata",
              sorted(fp for (m, fp) in strata if m == "kimi/kimi-k3") ==
              ["fpv0_3f6baf1f", "fpv0_c96a51ed", "fpv0_cabe88c9",
               "fpv0_df2f7ec7", "fpv0_e8884bc8"],
              sorted(fp for (m, fp) in strata if m == "kimi/kimi-k3"))
        check("kimi_terminal_strata_counts",
              {fp: len(rs) for (m, fp), rs in strata.items()
               if m == "kimi/kimi-k3"} ==
              {"fpv0_3f6baf1f": 24, "fpv0_c96a51ed": 20, "fpv0_cabe88c9": 30,
               "fpv0_df2f7ec7": 30, "fpv0_e8884bc8": 16})

    # ---- scoring run manifest ----
    man = {
        "task_id": "biosysmodb150_g9_four_model_121_formal_offline_score_20261008",
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "api_calls": 0,
        "fixture_label": FIXTURE_LABEL,
        "scorer_binding": {
            "mode": "FROZEN_READONLY_IMPORT",
            "path": "G3_scorer/scorer.py (in place, unmodified)",
            **{k: sha256_file(os.path.join(G3, k)) for k in FROZEN_SHA},
            "rdkit_version": getattr(scorer, "__version__", None)
            or __import__("rdkit").__version__,
            "call_usable": "score_answer(case_id, json.load(raw_visible), parse_status='VALID')",
            "call_non_usable": "score_answer(case_id, None, parse_status=INVALID_JSON|LENGTH_EMPTY|RESULT_UNKNOWN_HELD)",
        },
        "weights_fixed_pp": WEIGHTS,
        "counts": {
            "rows_scored": len(results),
            "usable": sum(1 for r in rows if r["engineering_class"] == "USABLE"),
            "invalid_json": sum(1 for r in rows
                                if r["engineering_class"] == "INVALID_JSON"),
            "length_empty": sum(1 for r in rows
                                if r["engineering_class"] == "LENGTH_EMPTY"),
            "held": sum(1 for r in rows
                        if r["engineering_class"] == "RESULT_UNKNOWN_HELD"),
        },
        "primary_macro_weighted_total_fixed_121": {
            m: summary[m]["macro_weighted_total"] for m in MODEL_ORDER},
        "aux_usable_only_macro_weighted_total": {
            m: summary[m]["usable_only"]["macro_weighted_total"]
            for m in MODEL_ORDER},
        "checks": CHECKS[0], "failures": len(FAILURES),
        "failure_list": FAILURES,
        "outputs": {},
    }
    if FAILURES:
        print("SCORING RUN: FAIL (%d of %d checks)" % (len(FAILURES), CHECKS[0]))
        return 1
    for fname in ("per_slot_scores.jsonl", "per_case_scores.tsv",
                  "per_model_summary.tsv", "evidence_axis.tsv",
                  "abstention_axis.tsv", "engineering_axis.tsv",
                  "failure_registry.tsv", "fingerprint_summary.tsv"):
        man["outputs"][fname] = sha256_file(os.path.join(SCORES, fname))
    with open(os.path.join(SCORES, "SCORING_RUN_MANIFEST.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print("SCORING RUN: PASS (%d checks, 0 failures)" % CHECKS[0])
    for m in MODEL_ORDER:
        print("  %-24s macro(121)=%.4f  usable-only(%d)=%.4f"
              % (m, summary[m]["macro_weighted_total"], summary[m]["usable_n"],
                 summary[m]["usable_only"]["macro_weighted_total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
