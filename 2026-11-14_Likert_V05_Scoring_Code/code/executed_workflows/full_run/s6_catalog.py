#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s6_catalog — reconstruct the REF1 reference-catalog JSON exactly as shipped.

Case-level audited rules (no new material):
  E0_EVIDENCE: the case's frozen F3 evidence ids (empty when EVIDENCE_GAP);
  GOLD_SLICE : every shipped slice tsv, file + file#case:<id>;
  SCOPE_ROW  : SCOPE#<case>#<CGxx> from the frozen 120-case claim-group scope table;
  matrix     : ACCSET:<required step ids> + SCOPE ids + GOLD ids (that order).
The S6 offline check verifies byte equality of the reconstruction against all
8 shipped S4 calibration messages before any foreign render uses it.
"""
import csv, json, os
from pathlib import Path

_R = Path(os.environ["LIKERT_V05_RUN_ROOT"]) if "LIKERT_V05_RUN_ROOT" in os.environ else     Path("/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/LIKERT_V05_RELEASE_20261108/S2_CHENYU_RELEASE_03E/bundle/data")
_OUT = Path(os.environ["LIKERT_V05_RELEASE_DIR"])
SLICES = _R / "LIKERT_V05_RELEASE_20261108/S0_INTEGRATION/gold_slices"
F0SCOPE = _R / "LIKERT_V04_FULL_SCORING_20261029/F0_INPUT_BASELINE/CASE_CLAIM_GROUP_SCOPE_120.tsv"
ACCEPTED = _OUT / "accepted/ACCEPTED_ENZYMES_RELEASE.tsv"
_scope_cache = {}
_acc_cache = {}


def scope_row_ids(case):
    if case not in _scope_cache:
        out = ["SCOPE#%s#%s" % (case, r["claim_group"][:4])
               for r in csv.DictReader(F0SCOPE.open(), delimiter="\t") if r["case_id"] == case]
        _scope_cache[case] = sorted(out)
    return _scope_cache[case]


def accepted_rows_for(case):
    if case not in _acc_cache:
        _acc_cache[case] = [r for r in csv.DictReader(ACCEPTED.open(), delimiter="\t")
                            if r["case_id"] == case]
    return _acc_cache[case]


def gold_ids(case):
    files = sorted(f.name for f in (SLICES / case).iterdir() if f.is_file()
                   and f.name != "GOLD_SLICE_MANIFEST.json")
    out = []
    for f in files:
        out += [f, "%s#case:%s" % (f, case)]
    return out


def build_catalog(case, accepted_rows, evidence_ids):
    gold = gold_ids(case)
    scope = scope_row_ids(case)
    req = sorted((r for r in accepted_rows if r.get("step_scope_class") == "REQUIRED"),
                 key=lambda r: r["step_occurrence_id"])
    accset = ["ACCSET:" + r["step_occurrence_id"] for r in req]
    return {"E0_EVIDENCE": sorted(evidence_ids), "GOLD_SLICE": gold, "SCOPE_ROW": scope,
            "matrix_evidence_entry_and_version": sorted(accset + scope + list(evidence_ids) + gold)}
