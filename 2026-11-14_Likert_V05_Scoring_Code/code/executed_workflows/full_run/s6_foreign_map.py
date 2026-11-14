#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s6_foreign_map — per-foreign-answer branch mapping using the SAME frozen
deterministic rule as LIKERT_V05_03E_BRANCHMAP_V1 (branch_path_map_03e.py):
exactly one ADOPTED path fully covered, in order, by the answer's own
main-chain MATCH bindings -> BOUND; otherwise null (PENDING / ambiguous / no
adoption). Consumes S6 STEP_ALIGNMENT (answer-specific) + 03D
PATH_CATALOG/PATH_STEPS. No score-based tie-breaking, no chemistry re-derivation.
"""
import csv, json, sys
from pathlib import Path

sys.dont_write_bytecode = True
R = Path("/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01")
S6 = R / "LIKERT_V05_RELEASE_20261108/S6_COMBINED_V05_SCORING_20261111"
REL = R / "LIKERT_V05_RELEASE_20261108/S4_SCORING_FLOW_FIX_20261111/input/release"
_FENCE = None
import re
_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.M)
csv.field_size_limit(1 << 27)


def parse(text):
    try:
        return json.loads(text)
    except Exception:
        pass
    s = _FENCE.sub("", text.strip()).strip()
    try:
        return json.loads(s)
    except Exception:
        return None


def main():
    scope = {r["b_slot_uid"]: r for r in csv.DictReader((S6 / "out/facts/ROUTE_CASE_RESULTS_S6.tsv").open(), delimiter="\t")}
    cat = list(csv.DictReader((REL / "PATH_CATALOG_03D.tsv").open(), delimiter="\t"))
    steps = list(csv.DictReader((REL / "PATH_STEPS_03D.tsv").open(), delimiter="\t"))
    adopted, path_steps = {}, {}
    for r in cat:
        if r["adoption_status"] == "ADOPTED_METHOD_CONFIRMED":
            adopted.setdefault(r["case_id"], set()).add(r["path_id"])
        else:
            adopted.setdefault(r["case_id"], set())
    for r in steps:
        path_steps.setdefault((r["case_id"], r["path_id"]), []).append(r)
    align = {}
    for r in csv.DictReader((S6 / "out/facts/STEP_ALIGNMENT_S6.tsv").open(), delimiter="\t"):
        align.setdefault(r["b_slot_uid"], []).append(r)
    routes = scope  # keyed by b_slot_uid (= scoring item id)
    out_rows = []
    rows = list(csv.DictReader((R / "07_HPC_Prompts/LIKERT_V05_FULL_PLUS_GROK_GPT56_20261111/FOREIGN_TWO_MODELS_242_VERIFIED.tsv").open(), delimiter="\t"))
    from collections import defaultdict
    sc = {r["case_id"]: r for r in csv.DictReader((R / "LIKERT_V05_RELEASE_20261108/S2_CHENYU_RELEASE_03E/bundle/data/LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK/CASE_TASK_SCOPE_120.tsv").open(), delimiter="\t")}
    for row in rows:
        item = row["scoring_item_id"]
        case = row["case_id"]
        if item not in routes:
            continue  # skipped positions keep their status; no mapping fabricated
        main_ids, alt_ids = set(), set()
        obj = parse(Path(row["answer_path"]).read_text(encoding="utf-8"))
        if isinstance(obj, dict):
            for st in obj.get("steps") or []:
                if isinstance(st, dict) and isinstance(st.get("step_id"), str):
                    main_ids.add(st["step_id"])
            for br in obj.get("alternative_branches") or []:
                if isinstance(br, dict):
                    for st in br.get("steps") or []:
                        if isinstance(st, dict) and isinstance(st.get("step_id"), str):
                            alt_ids.add(st["step_id"])
        match_by_gold = {}
        for a in align.get(item, []):
            if a["step_state"] == "MATCH" and a["pred_step_id"]:
                match_by_gold.setdefault(a["gold_step_id"], []).append(a)
        covered = []
        for path_id in sorted(adopted.get(case, set())):
            prow = sorted(path_steps.get((case, path_id), []), key=lambda x: int(x["order_index"]))
            need = [x["gold_step_id"] for x in prow]
            ok_main, orders = True, []
            for gid in need:
                in_main = [c for c in match_by_gold.get(gid, []) if c["pred_step_id"] in main_ids]
                if not in_main:
                    ok_main = False
                    break
                orders.append(min(int(c["pred_order"]) for c in in_main if c["pred_order"]))
            if ok_main:
                covered.append(path_id if orders == sorted(orders) else path_id + "#ORDER_MISMATCH")
        if len(covered) == 1 and not covered[0].endswith("#ORDER_MISMATCH"):
            cid, basis, status = covered[0], ("UNIQUE_COVER: exactly one adopted path of %s is fully covered by the "
                "answer main-chain MATCH bindings in order; direct bind (D-M01/D-KEYDEF). Adopted paths checked: %s."
                % (case, ",".join(sorted(adopted.get(case, set()))))), "BOUND"
        elif covered:
            cid, basis, status = "", ("AMBIGUOUS_MULTIPLE_COVER: %s" % covered), "PENDING_MULTIPLE"
        elif not adopted.get(case):
            cid, basis, status = "", ("NO_ADOPTED_PATH: case scope graph_status=%s (linear or none); consumer identity stays null"
                % sc.get(case, {}).get("graph_status", "?")), "NOT_BRANCH"
        else:
            cid, basis, status = "", ("NO_COVER: no adopted path fully covered by main-chain MATCH bindings in order; "
                "adopted paths: %s" % ",".join(sorted(adopted.get(case, set())))), "PENDING"
        out_rows.append({"b_slot_uid": item, "case_id": case,
                         "tested_model_config_id": row["model_config_id"],
                         "answer_sha256": row["answer_sha256"], "parse_state": "OK" if obj is not None else "FAIL",
                         "main_step_ids": "|".join(sorted(main_ids)),
                         "alternative_step_ids": "|".join(sorted(alt_ids)),
                         "adopted_paths": "|".join(sorted(adopted.get(case, set()))),
                         "covered_paths": "|".join(covered),
                         "current_path_id": cid,
                         "mapping_status": status, "mapping_basis": basis,
                         "mapping_version": "S6_FOREIGN_BRANCHMAP_V1"})
    with (S6 / "out/facts/BRANCH_MAPPING_S6.tsv").open("w", newline="") as f:
        w = csv.DictWriter(f, list(out_rows[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(out_rows)
    print(json.dumps({"mapped": len(out_rows),
                      "BOUND": sum(1 for r in out_rows if r["mapping_status"] == "BOUND"),
                      "PENDING": sum(1 for r in out_rows if r["mapping_status"] in ("PENDING", "PENDING_MULTIPLE")),
                      "NOT_BRANCH": sum(1 for r in out_rows if r["mapping_status"] == "NOT_BRANCH")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
