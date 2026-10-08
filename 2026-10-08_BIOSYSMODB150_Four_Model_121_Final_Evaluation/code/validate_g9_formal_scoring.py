#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_g9_formal_scoring.py -- INDEPENDENT validator for the G9 offline
four-model formal scoring round. Does NOT import the merge builder or the
scoring wrapper; all expectations are re-derived from constants below and the
read-only sources. API_CALLS=0.

Recomputes at minimum:
  1. both source tar bytes+SHA256 and the two audit + authority SHAs
  2. 484 unique (case_id, model) keys; 4x121 denominators; canonical case order
  3. 469 usable / 13 content failures / 2 held / 0 not-dispatched / 0 retries
  4. exact failure lists per model
  5. per-slot request-body, raw-stream and visible-answer SHA256 recomputed
     from the source packages; canonical formal slot paths only (no pilot/
     smoke/probe answer can be substituted without detection)
  6. scores JSON<->TSV consistency; non-usable slots scored via the frozen
     non-dict path (layers 0, science 0, NA evidence/abstention)
  7. science weights 45/10/20/15/10 recomputed on every usable slot
  8. all 10 sensitivity variants: rule regeneration, sum==100, macro
     recomputation from per-slot layers (scorer NOT re-run)
  9. kimi fingerprint strata (24/20/30/30/16 terminal; 15 usable in e8884bc8)
 10. shape-review sampling reproducibility from seed 20261006 and byte-exact
     export SHAs
 11. api_calls==0 recorded in every produced manifest

Usage: validate_g9_formal_scoring.py [--g9 DIR] [--ex DIR] [--base DIR]
       [--out FINAL_VALIDATION.json]
"""
import argparse
import csv
import hashlib
import json
import os
import random
import re
import sys
from datetime import datetime, timezone

# ---- standalone constants (deliberately duplicated, never imported) ----
MODEL_ORDER = ["qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3", "kimi/kimi-k3"]
LAYERS = ["pathway", "smiles", "enzyme", "microbial_identity", "traits"]
WEIGHTS = {"pathway": 45.0, "smiles": 10.0, "enzyme": 20.0,
           "microbial_identity": 15.0, "traits": 10.0}
SEED = 20261006

TARS = {
    "three_model": ("biosysmodb150_g6r3_glm_low_then_g8p1_three_model_return_20261007T015420Z.tar.gz",
                    95804898,
                    "76a45fac8b54a3e5b6be549245cd7927233f4adbd9082766a886bf6bdf68b8ec"),
    "kimi": ("biosysmodb150_g8p2_kimi_k3_121_formal_return_20261007T141621Z.tar.gz",
             117802093,
             "e17504af6c2927e9ba37c9f31eb0ec75aa346bfdc1ac28badd213fbcdf31e34c"),
}
AUDITS = {
    "BIOSYSMODB150_G6R3_GLM_LOW_G8P1_THREE_MODEL_FORMAL_RETURN_LOCAL_AUDIT_20261007.md":
        "4ede4adafe84901d322151e2500a246e0cb99a49f30c9f784658e5741305e3a6",
    "BIOSYSMODB150_G8P2_KIMI_K3_121_FORMAL_RETURN_LOCAL_AUDIT_20261008.md":
        "4fbc0a029d551689c4e4d6c8986f785492d4fe85a40b1b366cac5915c758544e",
}
AUTHORITY = ("BIOSYSMODB150_FOUR_MODEL_121_FORMAL_API_COLLECTION_CLOSURE_20261008.md",
             "73314ebc41af42225f32aab2b2d7bb69b85c8b7d8a6efaed124e66b176da42bd")
FROZEN = {
    "G1_gold/G1_gold.manifest.json":
        "c424763cd4c38fcaac1b178979efb3f18f2b77039369ab6b8c709eab42dce06e",
    "G2_questions/G2_questions.manifest.json":
        "ae5780e546bb259d0133ba63157ecfe2f3d3071fc37fc2c0050629f7fe575520",
    "gates/G3_scorer.stage_gate.json":
        "32c155201a360db8de229e40a9d9cb14bd152993fd0356fd8b0eb8c9001ccaa2",
    "G3_scorer/G3_PREPARATION_MANIFEST.json":
        "24f1004cab0afca4707bbbd34f26f4b7ead074da723651af73f1fe95ad562e8a",
    "G3_scorer/scorer.py":
        "a326eee63258cd0a2706bfd8a1dc6907d6f9fc6aa24b101a7192312c6ed39c61",
    "G3_scorer/score_recipe.md":
        "8b79daf906f04e31589ad77bd93998f9a12649575bd4d476447c43028c338392",
    "G3_scorer/validators.py":
        "c302164433e37127854eefdf25c44a5939201375873833d51846c3c127083899",
    "00_Authority_Teacher_Plan/TEACHER_REPLY_BIOSYSMODB150_G2_G3_SIGNOFF_2026-09-28(1).md":
        "1fa908f5ff1caad1f0cb475e820309f0b6431be4e613d51a8548088399c1a5d0",
}
USABLE_EXPECT = {"qwen3.8-max": 120, "deepseek-v4.1-flash": 120,
                 "ZHIPU/GLM-5.3": 110, "kimi/kimi-k3": 119}
FAIL_EXPECT = {
    ("qwen3.8-max", "RESULT_UNKNOWN_HELD"): ["BIOPATH150_084"],
    ("deepseek-v4.1-flash", "LENGTH_EMPTY"): ["BIOPATH150_125"],
    ("ZHIPU/GLM-5.3", "INVALID_JSON"): [
        "BIOPATH150_021", "BIOPATH150_077", "BIOPATH150_092", "BIOPATH150_114",
        "BIOPATH150_119", "BIOPATH150_123", "BIOPATH150_125", "BIOPATH150_127",
        "BIOPATH150_132", "BIOPATH150_138", "BIOPATH150_146"],
    ("kimi/kimi-k3", "RESULT_UNKNOWN_HELD"): ["BIOPATH150_050"],
    ("kimi/kimi-k3", "LENGTH_EMPTY"): ["BIOPATH150_128"],
}
KIMI_FP = {"fpv0_3f6baf1f": (24, 24), "fpv0_c96a51ed": (20, 20),
           "fpv0_cabe88c9": (30, 30), "fpv0_df2f7ec7": (30, 30),
           "fpv0_e8884bc8": (16, 15)}
CANONICAL_VISIBLE = {
    "three_model": "source/three_model/formal_run/slots/{slot}/visible_answer.txt",
    "kimi": "source/kimi/kimi_run/slots/{slot}/visible_answer.txt",
}
CANONICAL_RAW = {
    "three_model": "source/three_model/formal_run/slots/{slot}/raw_stream.sse",
    "kimi": "source/kimi/kimi_run/slots/{slot}/raw_stream.sse",
}
CANONICAL_BODY = {
    "three_model": "source/three_model/formal_run/slots/{slot}/request_body.json",
    "kimi": "source/kimi/kimi_run/slots/{slot}/request_body.json",
}
SLOT_RE = {"three_model": re.compile(r"^G8P1-S\d{3}$"),
           "kimi": re.compile(r"^G8P2-K\d{3}$")}

CHECKS = [0]
FAILURES = []


def check(section, name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILURES.append({"section": section, "check": name,
                         "detail": str(detail)[:300]})
        print("  [FAIL][%s] %s :: %s" % (section, name, str(detail)[:200]))
    return ok


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def variant_weights(base, layer, delta):
    w = dict(base)
    w[layer] = base[layer] + delta
    rest = 100.0 - w[layer]
    others = sum(base[k] for k in LAYERS if k != layer)
    for k in LAYERS:
        if k != layer:
            w[k] = base[k] * rest / others
    return w


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--g9", default=None)
    ap.add_argument("--ex", default=None)
    ap.add_argument("--base", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    here = os.path.dirname(os.path.abspath(__file__))
    g9 = os.path.abspath(args.g9 or os.path.join(here, os.pardir))
    ex = os.path.abspath(args.ex or os.path.join(g9, os.pardir))
    base = os.path.abspath(args.base or os.path.join(ex, os.pardir))
    sections = {}

    def sec(name):
        sections.setdefault(name, {"checks": 0, "failures": 0})
        return name

    def c(section, name, ok, detail=""):
        before = len(FAILURES)
        r = check(section, name, ok, detail)
        sections.setdefault(section, {"checks": 0, "failures": 0})
        sections[section]["checks"] += 1
        if len(FAILURES) > before:
            sections[section]["failures"] += 1
        return r

    # ============ S1 source identities ============
    s = sec("S1_source_identity")
    for pkg, (name, nbytes, digest) in TARS.items():
        p = os.path.join(base, "03_HPC_Returned_Result_Summaries", name)
        c(s, "%s_tar_exists" % pkg, os.path.isfile(p))
        if os.path.isfile(p):
            c(s, "%s_tar_bytes" % pkg, os.path.getsize(p) == nbytes)
            c(s, "%s_tar_sha" % pkg, sha256_file(p) == digest)
    for name, digest in AUDITS.items():
        p = os.path.join(base, "04_Local_Review_Audits", name)
        c(s, "audit_sha_" + name[:24], os.path.isfile(p)
          and sha256_file(p) == digest)
    p = os.path.join(base, "00_Authority_Teacher_Plan", AUTHORITY[0])
    c(s, "authority_sha", os.path.isfile(p) and sha256_file(p) == AUTHORITY[1])

    # ============ S2 frozen scorer ============
    s = sec("S2_frozen_scorer")
    for rel, digest in FROZEN.items():
        # teacher approval lives under BASE/00_Authority_Teacher_Plan, the rest
        # under the execution dir
        root = base if rel.startswith("00_Authority_Teacher_Plan") else ex
        p = os.path.join(root, rel)
        c(s, "frozen_" + os.path.basename(rel),
          os.path.isfile(p) and sha256_file(p) == digest)
    import rdkit
    c(s, "rdkit_2026_03_5", rdkit.__version__ == "2026.03.5", rdkit.__version__)

    # ============ S3 index integrity ============
    s = sec("S3_index_integrity")
    index_path = os.path.join(g9, "FORMAL_484_SLOT_INDEX.tsv")
    c(s, "index_exists", os.path.isfile(index_path))
    if not os.path.isfile(index_path):
        return finish(sections, args, g9)
    with open(index_path, encoding="utf-8", newline="") as fh:
        idx = list(csv.DictReader(fh, delimiter="\t"))
    c(s, "rows_484", len(idx) == 484, len(idx))
    keys = [(r["case_id"], r["model_exact_id"]) for r in idx]
    c(s, "unique_keys", len(set(keys)) == len(keys) == 484)
    g2_cases = []
    with open(os.path.join(ex, "G2_questions", "main_cases.jsonl"),
              encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                g2_cases.append(json.loads(line)["case_id"])
    c(s, "g2_cases_121", len(g2_cases) == 121)
    for m in MODEL_ORDER:
        mr = [r for r in idx if r["model_exact_id"] == m]
        c(s, "model_121_%s" % m, len(mr) == 121, len(mr))
        c(s, "model_case_set_%s" % m,
          sorted(r["case_id"] for r in mr) == sorted(g2_cases))
        seq = [cid for _, cid in sorted((r["slot"], r["case_id"]) for r in mr)]
        c(s, "model_case_order_%s" % m, seq == g2_cases)
        c(s, "model_slot_pattern_%s" % m,
          all(SLOT_RE[r["source_package"]].match(r["slot"]) for r in mr))
    n_term = sum(1 for r in idx if r["terminal"] == "True")
    n_usable = sum(1 for r in idx if r["engineering_class"] == "USABLE")
    n_inv = sum(1 for r in idx if r["engineering_class"] == "INVALID_JSON")
    n_len = sum(1 for r in idx if r["engineering_class"] == "LENGTH_EMPTY")
    n_held = sum(1 for r in idx if r["engineering_class"] == "RESULT_UNKNOWN_HELD")
    c(s, "terminal_482", n_term == 482, n_term)
    c(s, "usable_469", n_usable == 469, n_usable)
    c(s, "invalid_11", n_inv == 11, n_inv)
    c(s, "length_2", n_len == 2, n_len)
    c(s, "held_2", n_held == 2, n_held)
    c(s, "content_failures_13", n_inv + n_len == 13)
    for m, n in USABLE_EXPECT.items():
        c(s, "usable_%s" % m,
          sum(1 for r in idx if r["model_exact_id"] == m
              and r["engineering_class"] == "USABLE") == n)
    for (m, cls), cases in FAIL_EXPECT.items():
        got = sorted(r["case_id"] for r in idx
                     if r["model_exact_id"] == m and r["engineering_class"] == cls)
        c(s, "faillist_%s_%s" % (m, cls), got == sorted(cases), got)
    # per-slot SHA recomputation from canonical formal paths only
    rid_seen = {}
    for r in idx:
        pkg, slot = r["source_package"], r["slot"]
        body_p = os.path.join(g9, CANONICAL_BODY[pkg].format(slot=slot))
        c(s, "body_file_%s" % slot, os.path.isfile(body_p)
          and sha256_file(body_p) == r["request_body_sha256"])
        vis_expect = CANONICAL_VISIBLE[pkg].format(slot=slot)
        if r["terminal"] == "True":
            raw_p = os.path.join(g9, CANONICAL_RAW[pkg].format(slot=slot))
            c(s, "raw_sha_%s" % slot, os.path.isfile(raw_p)
              and sha256_file(raw_p) == r["raw_stream_sha256"])
            c(s, "vis_sha_%s" % slot,
              r["visible_answer_relpath"] == vis_expect
              and sha256_file(os.path.join(g9, vis_expect))
              == r["visible_answer_sha256"])
            rid = r["provider_request_id"]
            c(s, "rid_present_%s" % slot, rid not in ("", "null"))
            c(s, "rid_unique_%s" % slot, rid not in rid_seen, rid)
            rid_seen[rid] = slot
            try:
                datetime.strptime(r["committed_utc"], "%Y-%m-%dT%H:%M:%SZ")
                ok = True
            except ValueError:
                ok = False
            c(s, "utc_iso_%s" % slot, ok)
        else:
            c(s, "held_no_raw_%s" % slot, r["raw_stream_sha256"] == "null")
            c(s, "held_no_visible_%s" % slot, r["visible_answer_sha256"] == "null"
              and r["visible_answer_relpath"] == "null")
            c(s, "held_rid_null_%s" % slot, r["provider_request_id"] == "null")
            c(s, "held_fp_na_%s" % slot, r["system_fingerprint"] == "NA_NO_RESPONSE")
        if r["engineering_class"] == "USABLE":
            try:
                obj = json.load(open(os.path.join(g9, vis_expect),
                                     encoding="utf-8"))
                ok = isinstance(obj, dict)
            except (ValueError, OSError):
                ok = False
            c(s, "usable_json_dict_%s" % slot, ok)
    c(s, "terminal_rids_482", len(rid_seen) == 482, len(rid_seen))
    # kimi fingerprint strata
    fp = {}
    for r in idx:
        if r["model_exact_id"] == "kimi/kimi-k3" and r["terminal"] == "True":
            t, u = fp.get(r["system_fingerprint"], (0, 0))
            fp[r["system_fingerprint"]] = (
                t + 1, u + (1 if r["engineering_class"] == "USABLE" else 0))
    c(s, "kimi_fp_strata", fp == KIMI_FP, fp)
    c(s, "three_model_fp_not_exposed",
      all(r["system_fingerprint"] == "NOT_EXPOSED" for r in idx
          if r["source_package"] == "three_model" and r["terminal"] == "True"))

    # ============ S4 scores consistency ============
    s = sec("S4_scores_consistency")
    slots_path = os.path.join(g9, "scores", "per_slot_scores.jsonl")
    c(s, "jsonl_exists", os.path.isfile(slots_path))
    if not os.path.isfile(slots_path):
        return finish(sections, args, g9)
    js = {}
    with open(slots_path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rec = json.loads(line)
                js[(rec["case_id"], rec["model_exact_id"])] = rec
    c(s, "jsonl_484", len(js) == 484, len(js))
    idx_by_key = {(r["case_id"], r["model_exact_id"]): r for r in idx}
    for k, rec in js.items():
        r = idx_by_key.get(k)
        if r is None:
            c(s, "jsonl_key_in_index_%s" % (k,), False)
            continue
        c(s, "class_match_%s" % rec["slot"],
          rec["engineering_class"] == r["engineering_class"])
        res = rec["result"]
        if r["engineering_class"] == "USABLE":
            c(s, "parse_valid_%s" % rec["slot"],
              rec["parse_status"] == "VALID"
              and res["engineering"]["json_parse_status"] == "VALID")
            w = sum(float(res["layers"][x]) * WEIGHTS[x] for x in LAYERS) / 100.0
            # frozen scorer rounds each layer AND science_100 to 2 decimals:
            # legitimate deviation from re-weighted rounded layers is <= 0.01
            c(s, "weight_math_%s" % rec["slot"],
              abs(w - float(res["science_100"])) <= 0.011,
              "%s vs %s" % (w, res["science_100"]))
            c(s, "evidence_axis_present_%s" % rec["slot"],
              isinstance(res.get("evidence_axis"), dict)
              and isinstance(res.get("abstention_axis"), dict))
        else:
            c(s, "parse_reason_%s" % rec["slot"],
              rec["parse_status"] == r["engineering_class"]
              and res["engineering"]["json_parse_status"] == r["engineering_class"])
            c(s, "zero_science_%s" % rec["slot"],
              all(float(res["layers"][x]) == 0.0 for x in LAYERS)
              and float(res["science_100"]) == 0.0)
            c(s, "no_evidence_claim_%s" % rec["slot"],
              "evidence_axis" not in res and "abstention_axis" not in res)
        c(s, "binding_sha_%s" % rec["slot"],
          rec["visible_answer_sha256"] == r["visible_answer_sha256"]
          and rec["request_body_sha256"] == r["request_body_sha256"])
    # per_case_scores.tsv <-> jsonl
    pc_path = os.path.join(g9, "scores", "per_case_scores.tsv")
    with open(pc_path, encoding="utf-8", newline="") as fh:
        pc = list(csv.DictReader(fh, delimiter="\t"))
    c(s, "per_case_rows_484", len(pc) == 484, len(pc))
    for row in pc:
        k = (row["case_id"], row["model_exact_id"])
        rec = js.get(k)
        if rec is None:
            c(s, "pc_key_%s" % (k,), False)
            continue
        res = rec["result"]
        for x in LAYERS:
            c(s, "pc_layer_%s_%s" % (x, rec["slot"]),
              abs(float(row[x]) - round(float(res["layers"][x]), 4)) < 1e-9,
              row[x])
        c(s, "pc_total_%s" % rec["slot"],
          abs(float(row["weighted_total"]) - round(float(res["science_100"]), 4)) < 1e-9)
        if rec["engineering_class"] != "USABLE":
            c(s, "pc_na_%s" % rec["slot"],
              row["evidence_verified_n"] == "NA"
              and row["evidence_unverified_n"] == "NA"
              and row["overclaim_flags"] == "NA"
              and row["recall_macro"] == "NA"
              and row["abstention_status"] == "NA_NOT_USABLE")
    # per_model_summary macros recomputed over fixed 121
    with open(os.path.join(g9, "scores", "per_model_summary.tsv"),
              encoding="utf-8", newline="") as fh:
        pms = {row["model_exact_id"]: row
               for row in csv.DictReader(fh, delimiter="\t")}
    c(s, "pms_models_4", sorted(pms) == sorted(MODEL_ORDER))
    for m in MODEL_ORDER:
        row = pms.get(m)
        if row is None:
            continue
        c(s, "pms_n121_%s" % m, int(row["n_cases"]) == 121)
        for x in LAYERS + ["weighted_total"]:
            key = "macro_" + x
            if x == "weighted_total":
                vals = [float(js[(cid, m)]["result"]["science_100"])
                        for cid in g2_cases]
            else:
                vals = [float(js[(cid, m)]["result"]["layers"][x])
                        for cid in g2_cases]
            c(s, "pms_%s_%s" % (key, m),
              abs(float(row[key]) - sum(vals) / 121.0) < 1e-4,
              "%s vs %s" % (row[key], sum(vals) / 121.0))
        c(s, "pms_usable_n_%s" % m,
          int(row["usable_n"]) == USABLE_EXPECT[m])

    # scoring run manifest must bind the REAL frozen scorer hashes
    srm_path = os.path.join(g9, "scores", "SCORING_RUN_MANIFEST.json")
    c(s, "scoring_manifest_exists", os.path.isfile(srm_path))
    if os.path.isfile(srm_path):
        srm = load_json(srm_path)
        binding = srm.get("scorer_binding", {})
        for fname, key in (("scorer.py", "scorer.py"),
                           ("validators.py", "validators.py"),
                           ("score_recipe.md", "score_recipe.md"),
                           ("G3_PREPARATION_MANIFEST.json",
                            "G3_PREPARATION_MANIFEST.json")):
            real = sha256_file(os.path.join(ex, "G3_scorer", fname))
            c(s, "srm_binding_%s" % key, binding.get(key) == real,
              "%s vs %s" % (binding.get(key), real))
        c(s, "srm_rdkit", binding.get("rdkit_version") == "2026.03.5",
          binding.get("rdkit_version"))
        c(s, "srm_weights", srm.get("weights_fixed_pp") == WEIGHTS)
        c(s, "srm_counts", srm.get("counts", {}).get("rows_scored") == 484
          and srm.get("counts", {}).get("usable") == 469
          and srm.get("counts", {}).get("invalid_json") == 11
          and srm.get("counts", {}).get("length_empty") == 2
          and srm.get("counts", {}).get("held") == 2,
          srm.get("counts"))
        c(s, "srm_zero_failures", srm.get("failures") == 0)

    # ============ S5 sensitivity ============
    s = sec("S5_sensitivity")
    bound_path = os.path.join(g9, "scores", "sensitivity_spec_bound.json")
    c(s, "bound_exists", os.path.isfile(bound_path))
    if os.path.isfile(bound_path):
        bound = load_json(bound_path)
        c(s, "bound_scorer_sha", bound.get("scorer_binding", {}).get(
            "scorer_sha256") == FROZEN["G3_scorer/scorer.py"])
        c(s, "bound_model_set", bound.get("model_set") == MODEL_ORDER)
        c(s, "bound_base_weights",
          bound.get("variants") is not None
          and all(abs(sum(w.values()) - 100.0) < 1e-9
                  for w in bound["variants"].values()))
        c(s, "bound_no_synthetic",
          "SYNTHETIC" not in json.dumps(bound.get("copied", ""))
          and bound.get("fixture_label") != "SYNTHETIC_OFFLINE_FIXTURE")
        regen = {}
        for layer in LAYERS:
            for d in (+5.0, -5.0):
                regen["%s%+dpp" % (layer, int(d))] = variant_weights(
                    dict(WEIGHTS), layer, d)
        for name, w in regen.items():
            gw = bound.get("variants", {}).get(name)
            c(s, "variant_rule_%s" % name, gw is not None
              and all(abs(gw[k] - w[k]) < 1e-9 for k in LAYERS))
        with open(os.path.join(g9, "scores", "sensitivity_results.tsv"),
                  encoding="utf-8", newline="") as fh:
            srows = list(csv.DictReader(fh, delimiter="\t"))
        c(s, "sens_rows_40", len(srows) == 40, len(srows))
        per_model_layers = {m: [] for m in MODEL_ORDER}
        for cid in g2_cases:
            for m in MODEL_ORDER:
                per_model_layers[m].append(
                    {k: float(js[(cid, m)]["result"]["layers"][k])
                     for k in LAYERS})
        for row in srows:
            w = {k: float(row["weights_" + k]) for k in LAYERS}
            c(s, "sens_row_sum100_%s_%s" % (row["variant"], row["model_exact_id"]),
              abs(sum(w.values()) - 100.0) < 1e-9)
            name = row["variant"]
            c(s, "sens_row_rule_%s_%s" % (name, row["model_exact_id"]),
              name in regen
              and all(abs(w[k] - regen[name][k]) < 1e-9 for k in LAYERS))
            vals = [sum(lv[k] * w[k] for k in LAYERS) / 100.0
                    for lv in per_model_layers[row["model_exact_id"]]]
            c(s, "sens_row_macro_%s_%s" % (name, row["model_exact_id"]),
              abs(float(row["macro_weighted_total"]) - sum(vals) / len(vals)) < 1e-4,
              row["macro_weighted_total"])

    # ============ S6 sampling reproducibility ============
    s = sec("S6_sampling")
    sm_path = os.path.join(g9, "shape_review", "sampling_manifest.json")
    c(s, "sampling_manifest_exists", os.path.isfile(sm_path))
    if os.path.isfile(sm_path):
        sm = load_json(sm_path)
        c(s, "seed_20261006", sm.get("seed") == SEED)
        rng = random.Random(SEED)
        sorted_cases = sorted(g2_cases)
        expect = {m: rng.sample(sorted_cases, 2) for m in MODEL_ORDER}
        c(s, "sample_reproducible", sm.get("sampled") == expect,
          "%s vs %s" % (sm.get("sampled"), expect))
        c(s, "sample_order", sm.get("model_order") == MODEL_ORDER)
        # exports byte-exact against source
        sums_path = os.path.join(g9, "shape_review", "SHA256SUMS")
        c(s, "shape_sums_exists", os.path.isfile(sums_path))
        n_exports = 0
        for m in MODEL_ORDER:
            for cid in sm.get("sampled", {}).get(m, []):
                r = idx_by_key.get((cid, m))
                if r is None or r["engineering_class"] != "USABLE":
                    continue
                n_exports += 1
                stem = "%s__%s__%s.visible_answer.txt" % (
                    m.replace("/", "_"), cid, r["slot"])
                p = os.path.join(g9, "shape_review", "samples", stem)
                c(s, "export_exists_%s" % stem, os.path.isfile(p))
                if os.path.isfile(p):
                    c(s, "export_sha_%s" % stem,
                      sha256_file(p) == r["visible_answer_sha256"])
        c(s, "export_count_%d" % n_exports, n_exports >= 1)

    # ============ S7 api_calls = 0 ============
    s = sec("S7_api_zero")
    for rel in ("FORMAL_MERGE_MANIFEST.json", "scores/SCORING_RUN_MANIFEST.json",
                "scores/sensitivity_spec_bound.json",
                "scores/usage_cost_summary.json",
                "shape_review/sampling_manifest.json"):
        p = os.path.join(g9, rel)
        if os.path.isfile(p):
            d = load_json(p)
            c(s, "api_calls_zero_" + rel, d.get("api_calls") == 0,
              d.get("api_calls"))
        else:
            c(s, "api_calls_zero_" + rel, False, "missing")

    return finish(sections, args, g9)


def finish(sections, args, g9):
    overall = "FAIL" if FAILURES else "PASS"
    report = {
        "validator": "validate_g9_formal_scoring.py (independent; does not "
                     "import the merge builder or scoring wrapper)",
        "validated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "g9_root": g9,
        "api_calls": 0,
        "overall": overall,
        "total_checks": CHECKS[0],
        "total_failures": len(FAILURES),
        "sections": sections,
        "failures": FAILURES,
    }
    out = args.out or os.path.join(g9, "FINAL_VALIDATION.json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print("G9 VALIDATION: %s (%d checks, %d failures) -> %s"
          % (overall, CHECKS[0], len(FAILURES), out))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
