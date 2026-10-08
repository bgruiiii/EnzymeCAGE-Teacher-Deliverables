#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""export_shape_review.py -- export the 8 frozen-sample raw visibles (byte-exact
copies; failed/held slots would export a status note instead) and build the
objective shape checklist. Sample was fixed BEFORE any answer content was read
(sampling_manifest.json). Raw exports are copies for human review only; scoring
always reads the in-package originals.

Checklist fields are objective and script-computed:
  json_load_ok            direct json.load of raw visible bytes
  schema_errors/warnings  frozen G3 validators.schema_validate (read-only)
  n_steps/n_profiles/n_evidence
  traits_15F_profiles     profiles whose traits dict has exactly the 15 F keys
  null_leaf_ratio         null leaves / all leaves in the answer JSON
  question_echo_chunks    200-char question chunks (step 100) found verbatim
  template_shell_suspect  heuristic degenerate-shell flag (+ receiver flag)
"""
import csv
import hashlib
import importlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.abspath(os.path.join(HERE, os.pardir))
EX = os.path.abspath(os.path.join(G9, os.pardir))
G3 = os.path.join(EX, "G3_scorer")
SR = os.path.join(G9, "shape_review")

MODEL_ORDER = ["qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3", "kimi/kimi-k3"]
TRAIT_KEYS = {"F1_oxygen_tolerance", "F2_temperature", "F3_pH", "F4_salinity",
              "F5_culture_collection", "F6_respiration_electron_acceptor",
              "F7_carbon_substrate_utilization", "F8_degradation_capacity_broad",
              "F9_enzyme_activity", "F10_motility", "F11_cell_morphology",
              "F12_gram_cell_envelope", "F13_sporulation", "F14_genome_basic",
              "F15_habitat_generalism"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def leaf_stats(node):
    leaves = 0
    nulls = 0
    stack = [node]
    while stack:
        n = stack.pop()
        if isinstance(n, dict):
            stack.extend(n.values())
        elif isinstance(n, list):
            stack.extend(n)
        else:
            leaves += 1
            if n is None:
                nulls += 1
    return leaves, nulls


def question_text(case):
    path = os.path.join(G9, "source", "three_model", "derived_package",
                        "inputs", "messages", case + ".json")
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    assert doc["case_id"] == case
    return "\n".join(m.get("content") or "" for m in doc["messages"])


def echo_chunks(qtext, atext, size=200, step=100):
    hits = 0
    total = 0
    for i in range(0, max(1, len(qtext) - size + 1), step):
        chunk = qtext[i:i + size]
        total += 1
        if chunk in atext:
            hits += 1
    return hits, total


def main():
    sys.path.insert(0, G3)
    validators = importlib.import_module("validators")

    with open(os.path.join(SR, "sampling_manifest.json"), encoding="utf-8") as fh:
        sampling = json.load(fh)
    with open(os.path.join(G9, "FORMAL_484_SLOT_INDEX.tsv"), encoding="utf-8",
              newline="") as fh:
        index = {(r["model_exact_id"], r["case_id"]): r
                 for r in csv.DictReader(fh, delimiter="\t")}

    os.makedirs(os.path.join(SR, "samples"), exist_ok=True)
    rows = []
    sums = []
    for m in MODEL_ORDER:
        for case in sampling["sampled"][m]:
            r = index[(m, case)]
            safe_model = m.replace("/", "_")
            stem = "%s__%s__%s" % (safe_model, case, r["slot"])
            if r["engineering_class"] != "USABLE":
                note = ("%s STATUS NOTE: sampled slot %s (%s / %s) is "
                        "engineering_class=%s; per frozen contract the sample is "
                        "NOT replaced and no answer content exists to review."
                        % (datetime.now(timezone.utc).strftime("%FT%TZ"),
                           r["slot"], m, case, r["engineering_class"]))
                npath = os.path.join(SR, "samples", stem + ".STATUS_NOTE.txt")
                with open(npath, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(note + "\n")
                sums.append("%s  %s" % (sha256_file(npath),
                                        os.path.basename(npath)))
                rows.append({"model_exact_id": m, "case_id": case,
                             "slot": r["slot"],
                             "engineering_class": r["engineering_class"],
                             "exported": "STATUS_NOTE",
                             "export_sha256": sha256_file(npath)})
                continue
            src = os.path.join(G9, r["visible_answer_relpath"])
            dst = os.path.join(SR, "samples", stem + ".visible_answer.txt")
            shutil.copyfile(src, dst)  # byte-exact copy, no transformation
            xsha = sha256_file(dst)
            assert xsha == r["visible_answer_sha256"] == sha256_file(src)
            sums.append("%s  %s" % (xsha, os.path.basename(dst)))
            with open(dst, "rb") as fh:
                raw = fh.read()
            text = raw.decode("utf-8")
            try:
                answer = json.loads(text)
                jok = isinstance(answer, dict)
            except ValueError:
                answer, jok = None, False
            errs, warns = ([], []) if not jok else validators.schema_validate(answer)
            if jok:
                steps = answer.get("steps") or []
                profiles = answer.get("organism_profiles") or []
                evid = answer.get("evidence_registry") or []
                t15 = sum(1 for p in profiles
                          if isinstance(p.get("traits"), dict)
                          and set(p["traits"]) == TRAIT_KEYS)
                leaves, nulls = leaf_stats(answer)
                hits, total = echo_chunks(question_text(case), text)
                shell = ("N" if (len(steps) > 0 and len(profiles) > 0
                                 and len(evid) > 0
                                 and (nulls / leaves if leaves else 1) < 0.9)
                         else "Y")
            rows.append({
                "model_exact_id": m, "case_id": case, "slot": r["slot"],
                "engineering_class": r["engineering_class"],
                "exported": "RAW_VISIBLE",
                "export_file": os.path.basename(dst),
                "export_sha256": xsha,
                "visible_bytes": len(raw),
                "json_load_ok": "Y" if jok else "N",
                "schema_errors_n": len(errs) if jok else "NA",
                "schema_warnings_n": len(warns) if jok else "NA",
                "n_steps": len(answer.get("steps") or []) if jok else "NA",
                "n_organism_profiles":
                    len(answer.get("organism_profiles") or []) if jok else "NA",
                "n_evidence_registry":
                    len(answer.get("evidence_registry") or []) if jok else "NA",
                "traits_15F_profiles": t15 if jok else "NA",
                "null_leaf_ratio": ("%.4f" % (nulls / leaves)) if jok and leaves else "NA",
                "question_echo_chunks": ("%d/%d" % (hits, total)) if jok else "NA",
                "template_shell_suspect": shell if jok else "NA",
                "receiver_degenerate_flag": r["degenerate"],
                "receiver_schema_flag": r["schema_valid"],
            })
    cols = ["model_exact_id", "case_id", "slot", "engineering_class", "exported",
            "export_file", "export_sha256", "visible_bytes", "json_load_ok",
            "schema_errors_n", "schema_warnings_n", "n_steps",
            "n_organism_profiles", "n_evidence_registry", "traits_15F_profiles",
            "null_leaf_ratio", "question_echo_chunks", "template_shell_suspect",
            "receiver_degenerate_flag", "receiver_schema_flag"]
    with open(os.path.join(SR, "checklist.tsv"), "w", encoding="utf-8",
              newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    with open(os.path.join(SR, "SHA256SUMS"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("\n".join(sums) + "\n")
        fh.write("%s  %s\n" % (sha256_file(os.path.join(SR, "checklist.tsv")),
                               "checklist.tsv"))
        fh.write("%s  %s\n" % (sha256_file(os.path.join(SR, "sampling_manifest.json")),
                               "sampling_manifest.json"))
    print("EXPORTED %d samples (%d raw, %d status notes)"
          % (len(rows), sum(1 for r in rows if r["exported"] == "RAW_VISIBLE"),
             sum(1 for r in rows if r["exported"] == "STATUS_NOTE")))
    for r in rows:
        print("  %-22s %s %s json=%s steps=%s prof=%s evid=%s 15F=%s null=%s echo=%s shell=%s"
              % (r["model_exact_id"], r["case_id"], r["slot"],
                 r.get("json_load_ok"), r.get("n_steps"),
                 r.get("n_organism_profiles"), r.get("n_evidence_registry"),
                 r.get("traits_15F_profiles"), r.get("null_leaf_ratio"),
                 r.get("question_echo_chunks"), r.get("template_shell_suspect")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
