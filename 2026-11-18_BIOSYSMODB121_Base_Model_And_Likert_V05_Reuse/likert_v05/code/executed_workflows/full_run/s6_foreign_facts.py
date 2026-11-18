#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s6_foreign_facts — deterministic per-answer facts for the two foreign models.

Consumes FOREIGN_TWO_MODELS_242_VERIFIED.tsv (identity/shas already verified by
INPUT_REVIEW.json; re-verified here per row). For every READY row (except
060/094 reference holds and the two 023 scope-pending rows) it runs the SAME
frozen deterministic analysis components used to build B480 tables:
  * P1 route_checker.align_case (threshold 0.5 primary) on the case's V05 frozen
    gold slice + CASE_TASK_SCOPE_120 row -> step alignment + case route facts;
  * P2 disposition credit/five-state rules (accepted name/EC/pair hits;
    EC family prefix; missing-enzyme; UNKNOWN representation hold), minus the
    F3/D3A-audit ledger enrichment that does not exist for foreign answers:
    claims list stays empty, no verified-contradiction override. The result is
    this answer's OWN facts; nothing is copied from any other model's rows, and
    unconfirmed automatic matches stay UNRESOLVED/CANDIDATE for the judge —
    never fabricated MATCH-support (F) or whole-dimension NE.
key_step_class is task-level (case, gold_step) and taken from the audited R3
table after verifying per-case consistency, so it does not depend on any answer.

Outputs under S6 out/facts/: STEP_ALIGNMENT_S6.tsv, ROUTE_CASE_RESULTS_S6.tsv,
STEP_EVIDENCE_STATES_S6.tsv, FACTS_SUMMARY.json (per-row status).
Zero network. Read-only sources.
"""
import csv, hashlib, json, os, re, sys
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
R = Path("/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01")
S6 = R / "LIKERT_V05_RELEASE_20261108/S6_COMBINED_V05_SCORING_20261111"
CARD = R / "07_HPC_Prompts/LIKERT_V05_FULL_PLUS_GROK_GPT56_20261111"
BUNDLE_DATA = R / "LIKERT_V05_RELEASE_20261108/S2_CHENYU_RELEASE_03E/bundle/data"
P1 = BUNDLE_DATA / "LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK"
G1 = R / "LIKERT_V04_FULL_SCORING_20261029/F1_PROGRAM_TABLES/work/adapter_stage"
P2D = R / "LIKERT_V05_REVISION_20261105/P2_DISPOSITION_EVIDENCE"
R3D = BUNDLE_DATA / "LIKERT_V05_REVISION_20261105_R3/P2_DISPOSITION_EVIDENCE"
SLICES = BUNDLE_DATA / "LIKERT_V05_RELEASE_20261108/S0_INTEGRATION/gold_slices"  # noqa (kept for docs)
CTRL = G1 / "G2_questions/controlled_input_scoring_mask.tsv"
V05REL = R / "LIKERT_V05_RELEASE_20261108/S4_SCORING_FLOW_FIX_20261111/input/release"
sys.path.insert(0, str(R / "LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK"))
import route_checker_r2 as rc

csv.field_size_limit(1 << 27)
_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.M)
OUTF = S6 / "out/facts"
OUTF.mkdir(parents=True, exist_ok=True)


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def parse_answer_text(text):
    try:
        return json.loads(text), "OK"
    except Exception:
        pass
    stripped = _FENCE.sub("", text.strip()).strip()
    try:
        return json.loads(stripped), "OK_AFTER_CODEFENCE_STRIP"
    except Exception:
        return None, "JSON_PARSE_FAILURE"


def main():
    rows = list(csv.DictReader((CARD / "FOREIGN_TWO_MODELS_242_VERIFIED.tsv").open(), delimiter="\t"))
    assert len(rows) == 242
    scope = rc.load_scope(str(P1 / "CASE_TASK_SCOPE_120.tsv"))
        # same reference the audited R2 chain used (G1_gold identity-corrected, 121 cases;
    # V05 scope still gates which cases are scorable: 023 has no CASE_TASK_SCOPE_120 row)
    gold_all = rc.load_gold_steps(str(G1 / "G1_gold/reaction_gold.tsv"))
    cross_index = rc.build_cross_route_index(gold_all)
    controlled = rc.load_controlled_mask(str(CTRL))
    # accepted sets per (case, short)
    acc_steps = {}
    with (P2D / "ACCEPTED_ENZYME_SETS.tsv").open() as f:
        for r in csv.DictReader(f, delimiter="\t"):
            acc_steps[(r["case_id"], r["step_occurrence_id"].split("__")[1])] = r
    # key_step_class task-level from audited R3; verify per-case consistency
    r3 = list(csv.DictReader((R3D / "STEP_EVIDENCE_STATES_R3.tsv").open(), delimiter="\t"))
    kc_by_case_step, kc_conflict = {}, []
    for r in r3:
        k = (r["case_id"], r["gold_step_id"])
        if k in kc_by_case_step and kc_by_case_step[k] != r["key_step_class"]:
            kc_conflict.append(k)
        kc_by_case_step[k] = r["key_step_class"]
    assert not kc_conflict, kc_conflict[:4]
    # gold slice manifest sha per case (identity for judge-facing slice)
    import hashlib
    scope_sha = hashlib.sha256((P1/'CASE_TASK_SCOPE_120.tsv').read_bytes()).hexdigest()
    align_out, route_out, step_out, summary = [], [], [], []
    ready = skipped = 0
    for row in rows:
        item = row["scoring_item_id"]
        case = row["case_id"]
        status = row["integration_status"]
        if status != "READY_FOR_ANSWER_SPECIFIC_SCORING_ADAPTER":
            summary.append({"item": item, "case": case, "status": status or row["input_readiness"],
                            "facts": "NOT_GENERATED_KEEP_STATE"})
            skipped += 1
            continue
        ah = hashlib.sha256(Path(row["answer_path"]).read_bytes()).hexdigest()
        assert ah == row["answer_sha256"], (item, ah[:10])
        if case not in scope or case not in gold_all:
            summary.append({"item": item, "case": case,
                            "status": "REFERENCE_SCOPE_PENDING_023" if case == "BIOPATH150_023" else "CASE_NOT_IN_V05_SLICES",
                            "facts": "NOT_GENERATED_KEEP_STATE"})
            skipped += 1
            continue
        answer, pstate = parse_answer_text(Path(row["answer_path"]).read_text(encoding="utf-8"))
        sco = scope[case]
        ctrl = frozenset(controlled.get(case, ()))
        res = rc.align_case(sco, gold_all[case], answer, ctrl, cross_index, threshold=0.5, case_id=case)
        if pstate == "OK_AFTER_CODEFENCE_STRIP":
            res["answer_state"] = "OK"
            res["route_flags"] = sorted(set(res["route_flags"]) | {"PARSE_REQUIRED_CODEFENCE_STRIP"})
        elif pstate != "OK":
            res["answer_state"] = pstate
        sens = {t: rc.align_case(sco, gold_all[case], answer, ctrl, cross_index, threshold=t, case_id=case)
                for t in (0.4, 0.6)}
        # EXACTLY the audited R2 column set so the R3 base-score rules run on
        # foreign rows with zero logic change
        route_out.append({
            "b_slot_uid": item, "case_id": case, "tested_model_config_id": row["model_config_id"],
            "recovered": "FALSE", "answer_sha256": row["answer_sha256"], "answer_parse_state": pstate,
            "n_required": res["n_required"], "n_background_scope": res["n_background"],
            "matched": res["matched"], "coverage": res["coverage"],
            "flipped_strict": res["flipped_strict"], "flipped_strict_nonrev": res["flipped_strict_nonrev"],
            "flipped_strict_rev": res["flipped_strict_rev"],
            "reversal_candidates_two_sided": res["reversal_candidates_two_sided"],
            "substituted_confirmed": res["substituted_confirmed"], "stereo_conflict": res["stereo_conflict"],
            "boundary_unknown": res["boundary_unknown"], "nonmatch_confirmed": res["nonmatch_confirmed"],
            "missing": res["missing"],
            "chain_reversal_confirmed": "TRUE" if res["chain_reversal_confirmed"] else "FALSE",
            "chain_reversal_candidate_strong": "TRUE" if res["chain_reversal_candidate_strong"] else "FALSE",
            "endpoint_flow_swap": res["endpoint_flow_swap"], "extra_background": res["extra_background"],
            "extra_downstream": res["extra_downstream"], "extra_other_route_clue": res["extra_other_route_clue"],
            "extra_unmatched": res["extra_unmatched"], "edge_total": res["edge_total"],
            "edge_concordant": res["edge_concordant"], "edge_discordant_hard": res["edge_discordant_hard"],
            "edge_discordant_soft": res["edge_discordant_soft"], "endpoint_reached": res["endpoint_reached"],
            "endpoint_token_check": res["endpoint_token_check"],
            "split_merge_suspected": res["split_merge_suspected"],
            "n_alt_branches_declared": res.get("n_alt_branches_declared", ""),
            "n_downstream_continuation": res.get("n_downstream_continuation", ""),
            "controlled_repetitions": res["controlled_repetitions"],
            "controlled_excluded": res["controlled_excluded"],
            "task_conformance_status": res["task_conformance_status"],
            "task_violations": ";".join(res["task_violations"]),
            "route_status_chemical": res["route_status"],
            "task_and_route_status": res["task_and_route_status"],
            "route_status_t05_primary": res["route_status"],
            "route_status_t04_record_only": sens[0.4]["route_status"],
            "route_status_t06_record_only": sens[0.6]["route_status"],
            "threshold_sensitive": "TRUE" if not (sens[0.4]["route_status"] == res["route_status"] == sens[0.6]["route_status"]) else "FALSE",
            "route_flags": ";".join(res["route_flags"]),
            "result_class": "S6_ANSWER_SPECIFIC_R2_RULES_FOREIGN",
            "reference_gold_version": "G1_gold_identity_corrected_20261026",
            "scope_version_sha256": scope_sha,
            "checker_version": "route_checker_r2(F01/F02/F07/F08)"})
        # answer enzymes per pred step
        enz_by_step = {}
        for s in (answer or {}).get("steps", []):
            e = s.get("enzyme") or {}
            enz_by_step[s.get("step_id")] = {
                "enzyme_present": bool(e) and (e.get("name") or e.get("ec_number")),
                "name": e.get("name") or "", "ec": e.get("ec_number") or ""}
        for ar in res["step_rows"]:
            gsid = ar["gold_step_id"]
            short = gsid.split("__")[1]
            align_out.append({"b_slot_uid": item, "case_id": case,
                              "tested_model_config_id": row["model_config_id"],
                              "gold_step_id": gsid, "gold_short": short,
                              "gold_reaction_id": ar.get("gold_reaction_id", gsid.split("__")[2]),
                              "gold_order": ar.get("gold_order", ""), "gold_arrow_class": ar.get("gold_arrow_class", ""),
                              "pred_step_id": ar.get("pred_step_id", ""), "pred_order": ar.get("pred_order", ""),
                              "step_state": ar["step_state"], "reason_code": ar.get("reason_code", ""),
                              "binding_status": ar.get("binding_status", ""),
                              "binding_status": ar.get("binding_status", ""),
                              "jac_sub": ar.get("jac_sub", ""), "jac_prod": ar.get("jac_prod", ""),
                              "threshold": "0.5", "note": ar.get("note", ""),
                              "result_class": "S6_ANSWER_SPECIFIC_DRAFT_MATCHING"})
            # ---- disposition per P2 rules (no F3/D3A audit) ----
            acc = acc_steps.get((case, short), {})
            acc_names = {norm(x) for x in (acc.get("accepted_enzyme_names", "") or "").split("|") if x}
            acc_ecs = {norm(x) for x in (acc.get("accepted_ec_normalized_set", "") or "").split("|")
                       if x and x != "not_observed"}
            acc_pairs = set()
            for p in (acc.get("name_ec_pairs", "") or "").split("|"):
                if p and "=" in p:
                    nm_, ec_ = p.split("=", 1)
                    acc_pairs.add(norm(nm_ + "=" + ec_.replace("EC-", "").replace("ec-", "")))
            not_obs_only = acc.get("has_not_observed_only_ec") == "TRUE"
            route_state, route_reason = ar["step_state"], ar.get("reason_code", "")
            pred_sid = ar.get("pred_step_id", "")
            nearest_unrelated = ""
            if route_state == "MISSING" and pred_sid:
                nearest_unrelated = pred_sid
                pred_sid_for_enz = ""
            else:
                pred_sid_for_enz = pred_sid
            ez = (enz_by_step.get(pred_sid_for_enz) or {}) if pred_sid_for_enz else {}
            e_name, e_ec = ez.get("name", ""), ez.get("ec", "")
            ec_fmt = ("ABSENT_ENZYME" if not pred_sid or not ez.get("enzyme_present") else
                      "NULL_EC" if not e_ec else
                      "EXPLICIT_COMPLETE" if e_ec and e_ec.count(".") == 3 and not e_ec.endswith("-")
                      and "-" not in e_ec.split(".")[-1] else "INCOMPLETE_OR_FAMILY")
            name_hit = "YES" if e_name and norm(e_name) in acc_names else "NO"
            ec_hit = "YES" if e_ec and norm(e_ec) in acc_ecs else "NO"
            if ec_hit == "NO" and e_ec and e_ec.count(".") < 3:
                pref = e_ec.rstrip(".-")
                if any(x.startswith(norm(pref)) for x in acc_ecs):
                    ec_hit = "FAMILY_PREFIX"
            pair_hit = "NO"
            if e_name and e_ec:
                pair_hit = "YES" if norm("%s=%s" % (e_name, e_ec)) in acc_pairs else "NO"
            elif name_hit == "YES" and not e_ec and not_obs_only:
                pair_hit = "NAME_ONLY_NOT_OBSERVED_EC_OK"
            keyc = kc_by_case_step.get((case, gsid), "STANDARD")
            if route_state == "MATCH":
                if pair_hit == "YES" or (ec_hit == "YES" and (not e_name or name_hit == "YES")):
                    concl, five = "VERIFIED_FUNCTION_MATCH", "SUPPORTED"
                elif name_hit == "YES" and ec_fmt in ("NULL_EC",):
                    concl, five = "VERIFIED_FUNCTION_MATCH", "SUPPORTED"
                elif ec_hit == "FAMILY_PREFIX" or (e_ec and ec_fmt == "INCOMPLETE_OR_FAMILY"):
                    concl, five = "INCOMPLETE_EC", "CANDIDATE"
                elif e_ec and ec_hit == "NO":
                    concl, five = "REFERENCE_EC_NONMATCH_UNRESOLVED", "UNRESOLVED"
                elif not ez.get("enzyme_present") or (not e_name and not e_ec):
                    concl, five = "MISSING_ENZYME", "MISSING"
                elif e_name and name_hit == "NO" and not e_ec:
                    concl, five = "REFERENCE_EC_NONMATCH_UNRESOLVED", "UNRESOLVED"
                else:
                    concl, five = "CANDIDATE_ONLY", "CANDIDATE"
                if ec_fmt == "ABSENT_ENZYME":
                    concl, five = "MISSING_ENZYME", "MISSING"
                elif ec_fmt == "NULL_EC" and name_hit == "NO" and e_name:
                    concl, five = "REFERENCE_EC_NONMATCH_UNRESOLVED", "UNRESOLVED"
                usable = "YES" if five in ("SUPPORTED", "CANDIDATE") else "NO_EVIDENCE_%s" % five
            elif route_state == "UNKNOWN":
                concl, five, usable = "REFERENCE_OR_EVIDENCE_UNAVAILABLE", "UNRESOLVED", "HOLD_PENDING_REPRESENTATION_REVIEW"
            else:
                concl = "REACTION_MISSING_OR_WRONG"
                five = "MISSING" if (not pred_sid or not ez.get("enzyme_present")) else \
                    ("UNRESOLVED" if route_state == "MISSING" else
                     ("CONTRADICTED" if route_reason in ("STEREO_CONFLICT",) else "UNRESOLVED"))
                usable = "NO_ROUTE_BLOCKED"
            credit = {"SUPPORTED": "CONFIRMED_TARGET", "CANDIDATE": "CANDIDATE_ONLY",
                      "MISSING": ("MISSING_ENZYME_INFO" if route_state == "MATCH" else "ROUTE_BLOCKED_MISSING"),
                      "UNRESOLVED": ("UNRESOLVED_NONACCEPTED" if route_state == "MATCH" else
                                     ("ROUTE_HOLD_REPRESENTATION" if route_state == "UNKNOWN"
                                      else "ROUTE_BLOCKED_NONMATCH"))}[five]
            step_out.append({"b_slot_uid": item, "case_id": case,
                             "tested_model_config_id": row["model_config_id"],
                             "gold_step_id": gsid, "gold_short": short,
                             "key_step_class": keyc, "route_step_state": route_state,
                             "route_reason_code": route_reason,
                             "pred_step_id": pred_sid, "pred_enzyme_name": e_name, "pred_ec": e_ec,
                             "ec_format": ec_fmt, "accepted_name_hit": name_hit,
                             "accepted_ec_hit": ec_hit, "accepted_pair_hit": pair_hit,
                             "credit_class": credit,
                             "confirmed_target_credit": "YES" if five == "SUPPORTED" else "NO",
                             "candidate_present": "YES" if (e_name or e_ec) else "NO",
                             "reference_match": "HIT" if (name_hit == "YES" or ec_hit != "NO") else "NO",
                             "five_state": five, "step_conclusion": concl,
                             "highest_support_granularity":
                                 ("G4_REFERENCE_CURATED_REACTION_FUNCTION" if five == "SUPPORTED"
                                  else "G3_NAME_LEVEL" if (name_hit == "YES" or ec_hit != "NO") and route_state == "MATCH"
                                  else "G0_NONE"),
                             "missing_for_next_granularity": (
                                 "目标步未给出：缺步按MISSING登记" if five == "MISSING" else
                                 "路线门未过；酶声称本身按UNRESOLVED登记（不判错不判对）" if route_state in ("MISSING", "NONMATCH", "UNKNOWN") else
                                 "参考已接受=数据库策展粒度(G4)：不证明具体蛋白底物谱或实验活性" if five == "SUPPORTED" else
                                 "具体催化实验确认缺；候选不自动升级为已确认" if five == "CANDIDATE" else
                                 "与参考不匹配或未命中accepted：待核"),
                             "frozen_record_contradiction": "FALSE",
                             "f3_claims_bound_n": "0", "f3_claim_five_states": "",
                             "eligible_9_10_policy_A_inputs": "NO", "eligible_9_10_policy_B_inputs": "NO",
                             "result_class": "S6_ANSWER_SPECIFIC_P2_RULES_NO_F3",
                             "notes": (nearest_unrelated and ("最近无关预测步%s的酶信息不归属本目标步" % nearest_unrelated)) or ""})
        summary.append({"item": item, "case": case, "status": "FACTS_BUILT",
                        "answer_sha256": ah[:12], "route_status": res.get("route_status"),
                        "n_match": sum(1 for a in res["step_rows"] if a["step_state"] == "MATCH"),
                        "n_steps": len(res["step_rows"])})
        ready += 1

    def write(p, rows_, cols):
        with p.open("w", newline="") as f:
            w = csv.DictWriter(f, cols, delimiter="\t", lineterminator="\n", extrasaction="ignore")
            w.writeheader(); w.writerows(rows_)
    write(OUTF / "STEP_ALIGNMENT_S6.tsv", align_out, list(align_out[0].keys()))
    write(OUTF / "ROUTE_CASE_RESULTS_S6.tsv", route_out, list(route_out[0].keys()))
    write(OUTF / "STEP_EVIDENCE_STATES_S6.tsv", step_out, list(step_out[0].keys()))
    (OUTF / "FACTS_SUMMARY.json").write_text(json.dumps(
        {"ready_facts_built": ready, "skipped_kept_state": skipped,
         "status_counts": {s: sum(1 for x in summary if x["status"] == s) for s in
                           sorted({x["status"] for x in summary})},
         "detail": summary}, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"ready_facts_built": ready, "skipped": skipped,
                      "align_rows": len(align_out), "step_rows": len(step_out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
