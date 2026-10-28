#!/usr/bin/env python3
"""Verify the published anonymous calibration data without local workspace access or network."""
import argparse
import csv
import hashlib
import io
import json
import re
import tarfile
from collections import Counter
from fractions import Fraction
from pathlib import Path

DIMS = ["D1", "D2", "D3a", "D3b", "D4", "D5", "D6"]


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--skip-hashes", action="store_true", help="Only for pre-manifest construction checks.")
    args = ap.parse_args()
    base = args.base.resolve()
    a = {x["item_id"]: x for x in rows(base / "inputs/A/ratings_initial_frozen.tsv")}
    b = {}
    for line in (base / "inputs/B/SUMMARY_PREREVIEW.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("| V04-B-"):
            continue
        values = [x.strip() for x in next(csv.reader([line], delimiter="|"))][1:-1]
        assert len(values) == 13
        b[values[0]] = dict(zip(["item_id", "case_id", "engineering_class"] + DIMS + ["total", "science", "ke"], values))
    pairs = rows(base / "tables/ORIGINAL_32_ITEM_PAIRING.tsv")
    assert len(a) == len(b) == len(pairs) == 32
    raw, triggers, sources = [], [], []
    for p in pairs:
        x, y = a[p["a_item_id"]], b[p["b_item_id"]]
        assert x["case_id"] == y["case_id"] == p["case_id"]
        assert hash_file(base / "answers" / p["b_item_id"] / "visible_answer.txt") == p["visible_answer_sha256"]
        ka, kb = set(x["key_error_dims"].split(";")) - {""}, set(y["ke"].split(";")) - {"", "无"}
        for d in DIMS:
            av = int(x[d]) if x[d] else None
            bv = int(y[d])
            t = []
            if av is not None and abs(av - bv) >= 3:
                t.append("GAP_GE3")
            if (d in ka) != (d in kb):
                t.append("KE_DISAGREEMENT")
            if x["score_status_" + d] in {"NE", "NA"}:
                t.append("NE_VS_NUMERIC")
            raw.append((d, av, bv, p["engineering_class"]))
            if t:
                triggers.append((p["b_item_id"], d, t))
    assert len(raw) == 224 and sum(x[1] is not None for x in raw) == 219
    assert len(triggers) == 30 and len({x[0] for x in triggers}) == 15
    reported = {(x["basis"], x["dimension"]): x for x in rows(base / "tables/DESCRIPTIVE_AGREEMENT_BY_DIMENSION.tsv")}
    checks = []
    for basis in ["ORIGINAL_32", "USABLE28"]:
        for d in DIMS:
            cohort = [(av, bv) for dim, av, bv, eng in raw if dim == d
                      and av is not None and (basis == "ORIGINAL_32" or eng == "USABLE")]
            n = len(cohort)
            ca, cb = Counter(x for x, y in cohort), Counter(y for x, y in cohort)
            observed = Fraction(sum(abs(x-y) for x,y in cohort), n)
            expected = sum(Fraction(nx*cb[y]*abs(x-y),n*n) for x,nx in ca.items() for y in cb)
            kap = 1 - observed/expected if expected else None
            actual = {"n_valid_numeric_pairs": n, "exact_count": sum(x==y for x,y in cohort),
                      "within1_count": sum(abs(x-y)<=1 for x,y in cohort),
                      "mae":float(observed),
                      "weighted_kappa_linear":float(kap) if kap is not None else None}
            item = reported[(basis,d)]
            for key,val in actual.items():
                if val is None:
                    assert item[key] == "UNDEFINED"
                else:
                    assert abs(float(item[key])-val) <= 0.000051,(basis,d,key)
            checks.append({"basis":basis,"dimension":d,"n":n,"kappa":actual["weighted_kappa_linear"]})
    c = rows(base / "tables/ADJUDICATION_30_DECISIONS.tsv")
    assert len(c)==30 and Counter(x["key_error_decision"] for x in c)=={"Y":9,"N":11,"UNRESOLVED":10}
    changes=rows(base / "tables/ADJUDICATION_CHANGELOG.tsv")
    assert len(changes)==10 and sum(x["score_changed"]=="Y" for x in changes)==3
    assert sum(x["ke_changed"]=="Y" for x in changes)==2
    evidence=rows(base / "evidence/ADDED_EVIDENCE_REGISTER_76_NORMALIZED.tsv")
    assert len(evidence)==76 and len({x["evidence_id"] for x in evidence})==76
    snapshot=rows(base / "evidence/SNAPSHOT_INTEGRITY_INDEX.tsv")
    assert Counter(x["status"] for x in snapshot)=={"HASH_MATCH":25,"URL_QUOTE_ONLY_NO_RETURNED_RAW":51}
    hash_entries=0
    if not args.skip_hashes:
        manifest=base/"PAYLOAD_SHA256SUMS"
        assert manifest.is_file()
        for line in manifest.read_text().splitlines():
            h,rel=line.split("  ",1)
            assert not Path(rel).is_absolute() and ".." not in Path(rel).parts
            assert hash_file(base/rel)==h,rel
            hash_entries+=1
        top=base/"MANIFEST.sha256"
        if top.exists():
            for line in top.read_text().splitlines():
                h,rel=line.split("  ",1)
                assert hash_file(base/rel)==h,rel
    print(json.dumps({"status":"PASS_PUBLIC_CALIBRATION_REVIEW_DATA",
                      "paired_answers":32,"dimensions":224,"numeric_pairs":219,
                      "targeted_dimensions":30,"targeted_answers":15,
                      "statistics_verified":checks,"adjudications":30,
                      "evidence_registry_rows":76,"provided_snapshot_hash_matches":25,
                      "source_raw_snapshots_republished":False,
                      "hash_entries_checked":hash_entries,
                      "network_calls":0,"strict_two_human_H1_declared_met":False,
                      "v04_frozen":False},ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
