"""F2 gold slicer: build per-case gold slices from the frozen corrected gold
(G1_gold_identity_corrected_20261026, READ-ONLY), mirroring the M4 R2
8-case slice approach (GOLD_SLICE_MANIFEST with per-file sha256 +
source_sha256 + rows).

Deterministic: same case + same gold bytes → byte-identical slice files.
Slices are written to an output directory chosen by the caller (F4 prep or
test area); this tool never writes into the gold source tree.

Case-scope documents bound by F0 GOLD_AND_SCOPE_FREEZE_RECORD are attached
when applicable: SCOPE_ADDENDUM_BIOPATH150_016 (DECISION_016=A),
PROTOCOL_DISCLOSURE_BIOPATH150_006 (DECISION_006=D).

Offline: no network, no model API.
"""
from __future__ import annotations

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (R, sha256_file, sha256_bytes, atomic_write_bytes,
                       atomic_write_json)

GOLD_DIR = R / "25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26" / "G1_gold_identity_corrected_20261026"
GOLD_MANIFEST_SHA = "30257bde8f76f0afbafcbb84c9b0bd58ae1fcd19e73f0c7b5ee01f3a947f9d58"

CASE_SCOPED_TABLES = [
    "formal_cases.tsv",
    "enzyme_gold.tsv",
    "organism_gold.tsv",
    "reaction_gold.tsv",
    "trait_gold.tsv",
    "trait_scoreability_mask.tsv",
    "trait_subfield_scoreability_mask.tsv",
    "case_root_identity.tsv",
]
WHOLE_TABLES = [
    "verified_species_name_crosswalk.tsv",  # small; whole file (M4 pattern)
]
CASE_SCOPE_DOCS = {
    "BIOPATH150_016": R / "56_BIODEGRADATION_LIKERT_V04_M4_HUMAN_CALIBRATION_PACKAGES_20261026" / "staging_shared" / "gold" / "SCOPE_ADDENDUM_BIOPATH150_016.md",
    "BIOPATH150_006": R / "56_BIODEGRADATION_LIKERT_V04_M4_HUMAN_CALIBRATION_PACKAGES_20261026" / "staging_shared" / "gold" / "PROTOCOL_DISCLOSURE_BIOPATH150_006.md",
}


def _filter_rows(path, case_id: str) -> tuple[bytes, int]:
    """Filter TSV rows by the column NAMED case_id (its position differs per
    table: organism_gold.tsv has scope first)."""
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    lines = text.splitlines(keepends=True)
    if not lines:
        return b"", 0
    header = lines[0]
    cols = header.rstrip("\r\n").split("\t")
    if "case_id" not in cols:
        raise RuntimeError(f"{path}: no case_id column in header")
    idx = cols.index("case_id")
    out = [header]
    n = 0
    for line in lines[1:]:
        fields = line.rstrip("\r\n").split("\t")
        if len(fields) > idx and fields[idx] == case_id:
            out.append(line)
            n += 1
    data = "".join(out).encode("utf-8")
    return data, n


def build_case_slice(case_id: str, out_dir) -> dict:
    """Build gold slice for one case. Returns manifest dict (also written to
    out_dir/GOLD_SLICE_MANIFEST.json). Raises on missing source or zero-row
    core tables (a case with no gold rows is an identity problem, not silence)."""
    out_dir = str(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    if sha256_file(GOLD_DIR / "G1_gold.manifest.json") != GOLD_MANIFEST_SHA:
        raise RuntimeError(f"gold manifest sha mismatch — refusing to slice: {GOLD_DIR}")
    files = {}
    for name in CASE_SCOPED_TABLES:
        src = GOLD_DIR / name
        data, rows = _filter_rows(src, case_id)
        if rows == 0 and name in ("formal_cases.tsv", "case_root_identity.tsv"):
            raise RuntimeError(f"{case_id}: zero rows in required table {name}")
        atomic_write_bytes(os.path.join(out_dir, name), data)
        files[name] = {"rows": rows, "sha256": sha256_bytes(data),
                       "source_sha256": sha256_file(src),
                       "source_bytes": os.path.getsize(src)}
    for name in WHOLE_TABLES:
        src = GOLD_DIR / name
        data = open(src, "rb").read()
        rows = max(len(data.decode("utf-8").splitlines()) - 1, 0)
        atomic_write_bytes(os.path.join(out_dir, name), data)
        files[name] = {"rows": rows, "sha256": sha256_bytes(data),
                       "source_sha256": sha256_file(src),
                       "source_bytes": len(data)}
    if case_id in CASE_SCOPE_DOCS:
        doc = CASE_SCOPE_DOCS[case_id]
        data = open(doc, "rb").read()
        name = os.path.basename(str(doc))
        atomic_write_bytes(os.path.join(out_dir, name), data)
        files[name] = {"rows": None, "sha256": sha256_bytes(data),
                       "source_sha256": sha256_file(doc),
                       "source_bytes": len(data)}
    manifest = {
        "manifest": "GOLD_SLICE_MANIFEST_F2",
        "case_id": case_id,
        "gold_directory": str(GOLD_DIR),
        "gold_label": "G1_gold_identity_corrected_20261026",
        "gold_manifest_sha256": GOLD_MANIFEST_SHA,
        "gold_is_not_exhaustive": True,
        "note": "gold是核查基线与正确性参照，不是唯一允许答案；与gold不同不自动等于错误（量表四.2/四.5）",
        "files": files,
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=1,
                                 sort_keys=True) + "\n").encode("utf-8")
    atomic_write_bytes(os.path.join(out_dir, "GOLD_SLICE_MANIFEST.json"), manifest_bytes)
    manifest["manifest_file_sha256"] = sha256_bytes(manifest_bytes)
    return manifest


def slice_ref_ids(manifest: dict, case_id: str) -> list:
    """Reference ids accepted by the validator for ref_type=GOLD_SLICE:
    '<file>#case:<case_id>' for case-scoped tables, '<file>' for whole files,
    plus row-level ids are free-form within a file — validator only checks the
    file-level id set provided here (row locators live in support_scope)."""
    ids = []
    for name in manifest["files"]:
        ids.append(name)
        ids.append(f"{name}#case:{case_id}")
    return ids


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("case_id")
    ap.add_argument("out_dir")
    a = ap.parse_args()
    m = build_case_slice(a.case_id, a.out_dir)
    print(json.dumps({"case_id": a.case_id, "out_dir": a.out_dir,
                      "manifest_file_sha256": m["manifest_file_sha256"],
                      "files": {k: v["rows"] for k, v in m["files"].items()}},
                     ensure_ascii=False, indent=1))
