#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_mutation_tests.py -- adversarial mutation battery for the independent
validator. Each mutation is applied to a THROWAWAY copy tree of the G9
artifacts (sources are symlinked read-only; real artifacts are never touched).
Expected: control PASSes; every mutated tree FAILs validation.

Mutations (execution card section 7):
  M1 duplicate_key        duplicate one (case, model) index row
  M2 replaced_failure     consistently flip GLM BIOPATH150_021 INVALID_JSON
                          slot to a fabricated USABLE score across index +
                          jsonl + per_case TSV (caught only by source truth)
  M3 pilot_contamination  repoint a formal row's visible answer to a pilot
                          slot answer (path + sha both consistent)
  M4 denominator_120      drop one kimi case row (120 denominator)
  M5 weights_changed      tamper per_model_summary macro and one sensitivity
                          variant weight
  M6 scorer_sha_changed   tamper recorded scorer binding SHA
  M7 swapped_review_sample replace the frozen-seed sample picks
"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.abspath(os.path.join(HERE, os.pardir))
EX = os.path.abspath(os.path.join(G9, os.pardir))
BASE = os.path.abspath(os.path.join(EX, os.pardir))
MUT_ROOT = os.path.join(G9, "work", "mutations")
VALIDATOR = os.path.join(HERE, "validate_g9_formal_scoring.py")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def build_tree(name):
    tree = os.path.join(MUT_ROOT, name, "g9tree")
    if os.path.exists(os.path.join(MUT_ROOT, name)):
        shutil.rmtree(os.path.join(MUT_ROOT, name))
    os.makedirs(tree)
    os.makedirs(os.path.join(tree, "shape_review"))
    shutil.copyfile(os.path.join(G9, "FORMAL_484_SLOT_INDEX.tsv"),
                    os.path.join(tree, "FORMAL_484_SLOT_INDEX.tsv"))
    shutil.copyfile(os.path.join(G9, "FORMAL_MERGE_MANIFEST.json"),
                    os.path.join(tree, "FORMAL_MERGE_MANIFEST.json"))
    shutil.copytree(os.path.join(G9, "scores"), os.path.join(tree, "scores"))
    for f in ("sampling_manifest.json", "checklist.tsv", "SHA256SUMS"):
        shutil.copyfile(os.path.join(G9, "shape_review", f),
                        os.path.join(tree, "shape_review", f))
    os.symlink(os.path.join(G9, "source"), os.path.join(tree, "source"))
    os.symlink(os.path.join(G9, "shape_review", "samples"),
               os.path.join(tree, "shape_review", "samples"))
    return tree


def read_index(tree):
    with open(os.path.join(tree, "FORMAL_484_SLOT_INDEX.tsv"),
              encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        return list(rd), rd.fieldnames


def write_index(tree, rows, cols):
    with open(os.path.join(tree, "FORMAL_484_SLOT_INDEX.tsv"), "w",
              encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def mut_duplicate_key(tree):
    rows, cols = read_index(tree)
    rows.append(dict(rows[0]))
    write_index(tree, rows, cols)


def mut_replaced_failure(tree):
    rows, cols = read_index(tree)
    for r in rows:
        if r["case_id"] == "BIOPATH150_021" and r["model_exact_id"] == "ZHIPU/GLM-5.3":
            r["engineering_class"] = "USABLE"
            r["failure_reason"] = ""
            r["json_valid"] = r["object_form"] = r["schema_valid"] = "True"
            r["pass_all"] = "True"
    write_index(tree, rows, cols)
    fake_layers = {"pathway": 60.0, "smiles": 0.0, "enzyme": 0.0,
                   "microbial_identity": 0.0, "traits": 0.0}
    fake_science = 27.0
    p = os.path.join(tree, "scores", "per_slot_scores.jsonl")
    recs = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    for rec in recs:
        if rec["case_id"] == "BIOPATH150_021" and rec["model_exact_id"] == "ZHIPU/GLM-5.3":
            rec["engineering_class"] = "USABLE"
            rec["parse_status"] = "VALID"
            rec["science_100"] = fake_science
            rec["layers"] = dict(fake_layers)
            rec["result"]["layers"] = dict(fake_layers)
            rec["result"]["science_100"] = fake_science
            rec["result"]["engineering"]["json_parse_status"] = "VALID"
            rec["result"]["evidence_axis"] = {"verified_correct": 1,
                                              "unverified_correct": 0,
                                              "internal_knowledge": 0,
                                              "model_inference": 0,
                                              "evidence_hallucination": 0,
                                              "ref_missing": 0}
            rec["result"]["abstention_axis"] = {"gold_steps_recall_missed": 0,
                                                "null_abstentions": 0,
                                                "overclaims": 0}
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        for rec in recs:
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
    pc = os.path.join(tree, "scores", "per_case_scores.tsv")
    with open(pc, encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        prows, pcols = list(rd), rd.fieldnames
    for r in prows:
        if r["case_id"] == "BIOPATH150_021" and r["model_exact_id"] == "ZHIPU/GLM-5.3":
            r["engineering_class"] = "USABLE"
            r["pathway"] = "60.0000"
            r["weighted_total"] = "27.0000"
            r["json_valid"] = "Y"
            r["schema_valid"] = "Y"
            r["evidence_verified_n"] = "1"
            r["evidence_unverified_n"] = "0"
            r["overclaim_flags"] = "0"
            r["recall_macro"] = "1.0000"
            r["abstention_status"] = "NULLS_0_OVER_0"
    with open(pc, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=pcols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(prows)


def mut_pilot_contamination(tree):
    pilot_root = os.path.join(G9, "source", "three_model", "glm_pilot_run", "slots")
    pilot_slot = sorted(os.listdir(pilot_root))[0]
    pilot_vis = os.path.join(pilot_root, pilot_slot, "visible_answer.txt")
    rel = "source/three_model/glm_pilot_run/slots/%s/visible_answer.txt" % pilot_slot
    rows, cols = read_index(tree)
    for r in rows:
        if r["case_id"] == "BIOPATH150_001" and r["model_exact_id"] == "qwen3.8-max":
            r["visible_answer_relpath"] = rel
            r["visible_answer_sha256"] = sha256_file(pilot_vis)
    write_index(tree, rows, cols)


def mut_denominator_120(tree):
    rows, cols = read_index(tree)
    rows = [r for r in rows
            if not (r["case_id"] == "BIOPATH150_028"
                    and r["model_exact_id"] == "kimi/kimi-k3")]
    write_index(tree, rows, cols)


def mut_weights_changed(tree):
    p = os.path.join(tree, "scores", "per_model_summary.tsv")
    with open(p, encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        rows, cols = list(rd), rd.fieldnames
    for r in rows:
        if r["model_exact_id"] == "qwen3.8-max":
            r["macro_weighted_total"] = "%.4f" % (float(r["macro_weighted_total"]) + 1.0)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    b = os.path.join(tree, "scores", "sensitivity_spec_bound.json")
    d = json.load(open(b, encoding="utf-8"))
    d["variants"]["pathway+5pp"]["pathway"] = 52.0
    json.dump(d, open(b, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=2, sort_keys=True)


def mut_scorer_sha_changed(tree):
    p = os.path.join(tree, "scores", "SCORING_RUN_MANIFEST.json")
    d = json.load(open(p, encoding="utf-8"))
    d["scorer_binding"]["scorer.py"] = "0" * 64
    json.dump(d, open(p, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=2, sort_keys=True)


def mut_swapped_review_sample(tree):
    p = os.path.join(tree, "shape_review", "sampling_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    d["sampled"]["qwen3.8-max"] = ["BIOPATH150_001", "BIOPATH150_002"]
    json.dump(d, open(p, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=2, sort_keys=True)


MUTATIONS = [
    ("control_no_mutation", None, "PASS"),
    ("M1_duplicate_key", mut_duplicate_key, "FAIL"),
    ("M2_replaced_failure_answer", mut_replaced_failure, "FAIL"),
    ("M3_pilot_contamination", mut_pilot_contamination, "FAIL"),
    ("M4_denominator_120", mut_denominator_120, "FAIL"),
    ("M5_weights_changed", mut_weights_changed, "FAIL"),
    ("M6_scorer_sha_changed", mut_scorer_sha_changed, "FAIL"),
    ("M7_swapped_review_sample", mut_swapped_review_sample, "FAIL"),
]


def run_validator(tree):
    out = os.path.join(tree, "FINAL_VALIDATION.json")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, VALIDATOR, "--g9", tree, "--ex", EX, "--base", BASE,
         "--out", out],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    report = json.load(open(out, encoding="utf-8")) if os.path.isfile(out) else {}
    return proc.returncode, report


def main():
    os.makedirs(MUT_ROOT, exist_ok=True)
    results = []
    all_ok = True
    for name, fn, expect in MUTATIONS:
        tree = build_tree(name)
        if fn is not None:
            fn(tree)
        rc, report = run_validator(tree)
        got = report.get("overall", "NO_REPORT")
        ok = (got == expect) and (rc == 0 if expect == "PASS" else rc != 0)
        all_ok = all_ok and ok
        failed_checks = [f["check"] for f in report.get("failures", [])][:6]
        results.append({
            "mutation": name, "expected": expect, "got": got,
            "validator_exit": rc, "verdict": "DETECTED" if ok else "ESCAPED",
            "total_checks": report.get("total_checks"),
            "total_failures": report.get("total_failures"),
            "sample_failed_checks": failed_checks,
        })
        print("%-28s expected=%s got=%s exit=%s -> %s  %s"
              % (name, expect, got, rc, "DETECTED" if ok else "ESCAPED",
                 failed_checks[:3]))
        if name != "control_no_mutation":
            shutil.rmtree(tree, ignore_errors=True)  # keep control for audit
    report = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "api_calls": 0,
        "validator": os.path.relpath(VALIDATOR, G9),
        "all_mutations_detected": all_ok,
        "results": results,
    }
    with open(os.path.join(G9, "work", "mutation_results.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("MUTATION BATTERY: %s (%d/%d detected)"
          % ("PASS" if all_ok else "FAIL",
             sum(1 for r in results if r["verdict"] == "DETECTED") - 1,
             len(MUTATIONS) - 1))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
