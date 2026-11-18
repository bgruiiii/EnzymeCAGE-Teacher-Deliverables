"""F2 response validator: strict structural + semantic validation of AI rating
JSON against RATING_OUTPUT_SCHEMA.json and the period rule set.

Layers:
  L1 strict JSON parse (NaN/Infinity rejected — json.loads accepts them by
     default, so parse_constant raises),
  L2 JSON Schema draft-07 (jsonschema),
  L3 semantic rules (contract §7.3 numeric rules, rubric v0.4 clauses, F0
     policy dispositions). Each rule id appears in RULE_TO_VALIDATOR_MATRIX.tsv.

The validator NEVER modifies dimension scores. weighted_total /
scientific_subscore mismatches produce CORRECTION records (program recompute
is authoritative; the model's original output is preserved verbatim in the
raw response file).

Offline: no network, no model API.
"""
from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (DIMENSIONS, WEIGHTS, TRAITS_REQUIRED_COUNT,
                         CG_PREDEFINITION_GROUPS, UNRESOLVED_SCOPE_CASE,
                         UNRESOLVED_SCOPE_CGS, is_pure_int, sha256_bytes,
                         canonical_json, totals_contract)

SCHEMA_ID = "LIKERT_V04_AI_RATING_OUTPUT_SCHEMA_R1"

# Keys that must never appear anywhere in an AI rating output
# (rater_type=AI; no forged human attestation; no model identity / historical
# score / ranking leakage fields).
FORBIDDEN_KEYS = {
    "human_attestation", "attestation", "signature", "rater_id",
    "tested_model", "tested_model_config_id", "model_name", "model_identity",
    "program_score", "program_total", "historical_score", "history_score",
    "ranking", "rank", "grade_label", "grade", "third_person_score",
    "adjudication", "adjudicated_score",
}
FORBIDDEN_STRING_VALUES = {
    # rater identity forgery
    '"rater_type": "human"', '"rater_type":"human"', '"rater_type": "HUMAN"',
}

MISCIT_SEV_FROM_STATUS = {
    "VERIFIED_MIS_CITATION_LOCAL": "LOCAL",
    "VERIFIED_MIS_CITATION_CRITICAL": "CRITICAL",
    "VERIFIED_MIS_CITATION_SYSTEMIC": "SYSTEMIC",
}
SEV_RANK = {"LOCAL": 1, "CRITICAL": 2, "SYSTEMIC": 3}
DECISION_RELEVANT_CRITICALITY_TOKENS = ("CORE", "APPLICATION_CRITICAL")


def _reject_nan(token):
    raise ValueError(f"NaN/Infinity not allowed in rating JSON: {token}")


def parse_rating_json(text: str):
    """L1: strict parse. Raises ValueError on NaN/Inf/invalid JSON."""
    return json.loads(text, parse_constant=_reject_nan)


class ValidationResult:
    def __init__(self):
        self.errors = []      # rule violations → response invalid
        self.corrections = []  # program-recompute differences (non-invalidating)
        self.review_flags = []  # route-to-review-queue findings (non-invalidating)

    def err(self, code, msg):
        self.errors.append({"code": code, "message": msg})

    def correction(self, field, model_value, recomputed):
        self.corrections.append({"field": field, "model_value": model_value,
                                 "recomputed_value": recomputed})

    def review(self, code, msg):
        self.review_flags.append({"code": code, "message": msg})

    @property
    def valid(self):
        return not self.errors

    def to_dict(self):
        return {"status": "VALID" if self.valid else "INVALID",
                "errors": self.errors, "corrections": self.corrections,
                "review_flags": self.review_flags}


def _walk_strings(obj, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def _walk_keys(obj, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield f"{path}.{k}", k
            yield from _walk_keys(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_keys(v, f"{path}[{i}]")


def _all_numbers(obj, path="$"):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _all_numbers(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _all_numbers(v, f"{path}[{i}]")


def validate_schema_structure(rating: dict, schema: dict, res: ValidationResult):
    """L2: JSON Schema draft-07."""
    try:
        import jsonschema
    except ImportError:
        res.err("V02_SCHEMA_LIB_MISSING", "jsonschema not installed")
        return
    v = jsonschema.Draft7Validator(schema)
    for e in sorted(v.iter_errors(rating), key=lambda e: list(e.path)):
        loc = "$." + ".".join(str(p) for p in e.path) if e.path else "$"
        res.err("V02_SCHEMA", f"{loc}: {e.message[:300]}")


def validate_rating(rating: dict, ctx: dict, schema: dict) -> ValidationResult:
    """Full validation.

    ctx (request-side context, built by f2r12_request_builder/item_builder):
      case_id, anonymous_item_id,
      identity_echo: {field: expected_sha}  (9 fields),
      scope_rows: [{claim_group, condition_met, active_criticality}]  (6 rows),
      evidence_ids: [str]  (E0 ids provided in request; may be empty in tests),
      gold_ref_ids: [str]  (gold slice file names / row ids provided),
      scope_row_ref_ids: [str],
    """
    res = ValidationResult()
    if not isinstance(rating, dict):
        res.err("V00_NOT_OBJECT", "rating is not a JSON object")
        return res

    validate_schema_structure(rating, schema, res)

    # V20: every JSON number finite (NaN/Inf rejection beyond parser)
    for path, num in _all_numbers(rating):
        if isinstance(num, float) and not math.isfinite(num):
            res.err("V20_NON_FINITE", f"{path}: non-finite number {num}")

    # V17: forbidden keys / identity-forgery strings anywhere
    for path, key in _walk_keys(rating):
        if key.lower() in FORBIDDEN_KEYS:
            res.err("V17_FORBIDDEN_KEY", f"{path}: forbidden key '{key}'")
    for path, s in _walk_strings(rating):
        for bad in FORBIDDEN_STRING_VALUES:
            if bad in s:
                res.err("V17_FORBIDDEN_VALUE", f"{path}: rater identity forgery")

    # V01: identity echo + item/case ids must equal request-injected values
    echo = rating.get("input_identity_echo")
    if isinstance(echo, dict):
        for field, expected in (ctx.get("identity_echo") or {}).items():
            got = echo.get(field)
            if got != expected:
                res.err("V01_IDENTITY_ECHO",
                        f"input_identity_echo.{field}={got!r} != request {expected!r}")
    if rating.get("case_id") != ctx.get("case_id"):
        res.err("V01_CASE_ID", f"case_id {rating.get('case_id')!r} != {ctx.get('case_id')!r}")
    if rating.get("anonymous_item_id") != ctx.get("anonymous_item_id"):
        res.err("V01_ITEM_ID",
                f"anonymous_item_id {rating.get('anonymous_item_id')!r} != {ctx.get('anonymous_item_id')!r}")
    if rating.get("rater_type") != "AI":
        res.err("V17_RATER_TYPE", f"rater_type must be 'AI', got {rating.get('rater_type')!r}")
    if rating.get("schema_id") != SCHEMA_ID:
        res.err("V22_SCHEMA_ID", f"schema_id must be {SCHEMA_ID}")

    dims = rating.get("dimensions")
    dims = dims if isinstance(dims, dict) else {}

    # V03/V04: per-dimension status↔score↔basis linkage; strict integers
    scored_values = {}
    ne_na_dims = []
    for d in DIMENSIONS:
        dim = dims.get(d)
        if not isinstance(dim, dict):
            res.err("V03_DIM_MISSING", f"dimensions.{d} missing/not object")
            continue
        st = dim.get("score_status")
        sc = dim.get("score")
        if st == "SCORED":
            if not is_pure_int(sc):
                res.err("V04_NOT_PURE_INT",
                        f"{d}: SCORED score must be strict int 1-10, got {sc!r} ({type(sc).__name__})")
            elif not (1 <= sc <= 10):
                res.err("V04_RANGE", f"{d}: score {sc} outside 1-10")
            else:
                scored_values[d] = sc
            # F2-P2-01 (rubric 四.4/P48): local-unverified coexists with a
            # numeric score — SCORED may carry the PAIRED ne_basis+ne_unverified
            # fields (lossless mapping of 局部待核); one-without-the-other is broken.
            nb, nu = dim.get("ne_basis"), dim.get("ne_unverified")
            if (nb is None) != (nu is None):
                res.err("V03_LOCAL_UNVERIFIED_PAIR",
                        f"{d}: SCORED local-unverified fields must be paired "
                        "(ne_basis and ne_unverified both present or both null)")
            if nb is not None and not (str(nb).strip() and str(nu).strip()):
                res.err("V03_LOCAL_UNVERIFIED_PAIR",
                        f"{d}: SCORED local-unverified pair must be non-empty strings")
            for f in ("na_basis", "missing_basis"):
                if dim.get(f) is not None:
                    res.err("V03_BASIS_CROSS", f"{d}: SCORED but {f} non-null")
            if not (dim.get("rationale") or "").strip():
                res.err("V16_RATIONALE", f"{d}: SCORED requires non-empty rationale")
            if not (dim.get("answer_locator") or "").strip():
                res.err("V16_LOCATOR", f"{d}: SCORED requires answer_locator")
        elif st == "MISSING":
            # V19: MISSING must be exactly 1 and truly an undelivered module.
            # MISSING counts as score 1 in the weighted totals (weights kept,
            # rubric 五/P78: 缺失模块按规则保留权重，不能删除后使总分升高).
            if sc != 1 or not is_pure_int(sc):
                res.err("V19_MISSING_NOT_1", f"{d}: MISSING requires score==1, got {sc!r}")
            else:
                scored_values[d] = 1
            if not (dim.get("missing_basis") or "").strip():
                res.err("V03_MISSING_BASIS", f"{d}: MISSING requires missing_basis")
            for f in ("ne_basis", "ne_unverified", "na_basis"):
                if dim.get(f) is not None:
                    res.err("V03_BASIS_CROSS", f"{d}: MISSING but {f} non-null")
        elif st == "NE":
            # V18: NE must be null numeric, never 0, with paired basis fields
            if sc is not None:
                res.err("V18_NE_NOT_NULL", f"{d}: NE requires score=null, got {sc!r}")
            if not (dim.get("ne_basis") or "").strip() or not (dim.get("ne_unverified") or "").strip():
                res.err("V03_NE_PAIR", f"{d}: NE requires ne_basis AND ne_unverified paired non-empty")
            ne_na_dims.append(d)
        elif st == "NA":
            if sc is not None:
                res.err("V18_NA_NOT_NULL", f"{d}: NA requires score=null, got {sc!r}")
            if not (dim.get("na_basis") or "").strip():
                res.err("V03_NA_BASIS", f"{d}: NA requires na_basis")
            ne_na_dims.append(d)
        else:
            res.err("V07_ILLEGAL_STATUS", f"{d}: illegal score_status {st!r}")

    # V05: KE=Y → argument present, score ≤4, dim SCORED; KE=UNRESOLVED → review
    ke_y_dims = []
    for d in DIMENSIONS:
        dim = dims.get(d)
        if not isinstance(dim, dict):
            continue
        ke = dim.get("key_error")
        if ke not in ("Y", "N", "UNRESOLVED"):
            res.err("V05_KE_ENUM", f"{d}: key_error {ke!r} not in Y/N/UNRESOLVED")
        if ke == "Y":
            ke_y_dims.append(d)
            arg = dim.get("key_error_argument")
            if not isinstance(arg, dict):
                res.err("V05_KE_NO_ARG", f"{d}: key_error=Y requires key_error_argument")
            else:
                if not (arg.get("invalidation_argument") or "").strip():
                    res.err("V05_KE_ARG_EMPTY", f"{d}: invalidation_argument empty")
                if not arg.get("verification_evidence"):
                    res.err("V05_KE_NO_EVIDENCE", f"{d}: KE=Y requires locatable verified evidence refs")
                if not (arg.get("support_scope") or "").strip():
                    res.err("V05_KE_NO_SCOPE", f"{d}: KE=Y requires support_scope")
                if arg.get("capped") is not True:
                    res.err("V05_KE_NOT_CAPPED", f"{d}: KE=Y requires capped=true")
            st = dim.get("score_status")
            sc = dim.get("score")
            if st != "SCORED":
                res.err("V05_KE_STATUS", f"{d}: KE=Y requires score_status=SCORED (got {st!r}); "
                        "a call failure is system_run_status, an undelivered module is MISSING(1) — neither is KE")
            elif is_pure_int(sc) and sc > 4:
                res.err("V05_KE_GT4", f"{d}: KE=Y requires score<=4, got {sc}")
        else:
            if dim.get("key_error_argument") is not None:
                res.err("V05_KE_ARG_UNEXPECTED", f"{d}: key_error_argument present but key_error={ke!r}")
        if ke == "UNRESOLVED":
            res.review("V05_KE_UNRESOLVED", f"{d}: key_error=UNRESOLVED → review queue (not counted as verified KE, no cap)")

    # V06: same-root events — dims sharing an event must have distinct arguments
    events = rating.get("root_error_events")
    events = events if isinstance(events, list) else []
    event_ids = set()
    for ev in events:
        if isinstance(ev, dict):
            eid = ev.get("event_id")
            if eid in event_ids:
                res.err("V07_EVENT_DUP", f"duplicate root event id {eid}")
            event_ids.add(eid)
            for d in ev.get("affected_dims") or []:
                dim = dims.get(d)
                if isinstance(dim, dict):
                    refs = dim.get("root_error_event_ids") or []
                    if eid not in refs:
                        res.err("V07_EVENT_DIM_BACKREF",
                                f"event {eid} lists {d} but {d}.root_error_event_ids lacks it")
    for d in DIMENSIONS:
        dim = dims.get(d)
        if isinstance(dim, dict):
            for eid in dim.get("root_error_event_ids") or []:
                if eid not in event_ids:
                    res.err("V07_EVENT_MISSING", f"{d}: references unregistered event {eid}")
    ke_args_by_dim = {}
    for d in ke_y_dims:
        arg = (dims.get(d) or {}).get("key_error_argument") or {}
        ke_args_by_dim[d] = arg.get("invalidation_argument") or ""
    for ev in events:
        if not isinstance(ev, dict):
            continue
        shared = [d for d in (ev.get("affected_dims") or []) if d in ke_args_by_dim]
        for i in range(len(shared)):
            for j in range(i + 1, len(shared)):
                a, b = ke_args_by_dim[shared[i]], ke_args_by_dim[shared[j]]
                if a and a == b:
                    res.err("V06_NO_INDEPENDENT_ARG",
                            f"{shared[i]}/{shared[j]} share event {ev.get('event_id')} with byte-identical "
                            "invalidation_argument — per-dimension independent argument required (no guilt by association)")

    # V08: D5 registry
    reg = rating.get("d5_registry")
    reg = reg if isinstance(reg, dict) else {}
    groups = reg.get("claim_groups")
    groups = groups if isinstance(groups, list) else []
    # F2-P1-05 fix: ALL scope/echo checks are keyed by CGnn id — a permitted
    # long (predefinition) or short (scope120) name variant can never bypass
    # the frozen condition/criticality echo or the 013 UNRESOLVED rule.
    scope_rows_by_id = {r["claim_group"][:4]: r for r in (ctx.get("scope_rows") or [])}
    # F0 scope120 uses abbreviated CG names for some groups (e.g.
    # "CG11_性状：温度" vs predefinition "CG11_性状：温度（最适/范围）").
    # Both namings are frozen upstream; accept a name when it equals the
    # predefinition name OR the scope120 name for the same CG id. Alignment
    # is by CGnn id, never by fuzzy text.
    predef_by_id = {name[:4]: name for name in CG_PREDEFINITION_GROUPS}
    scope_name_by_id = {cid: r["claim_group"] for cid, r in scope_rows_by_id.items()}
    # frozen predefinition attributes supplied by the item builder from
    # CLAIM_GROUP_CRITICALITY_PREDEFINITION_R2.tsv (sha-verified):
    # {CGnn: {"condition_type": ..., "criticality_unconditional": ...}}
    predef_attrs = ctx.get("predef_by_id") or {}
    seen_groups = set()
    seen_cg_ids = set()
    group_sev = []
    for g in groups:
        if not isinstance(g, dict):
            res.err("V08_GROUP_NOT_OBJ", "claim_groups entry not object")
            continue
        cg = g.get("claim_group") or ""
        cg_id = cg[:4]
        if not (len(cg) >= 4 and cg_id.startswith("CG") and cg_id[2:].isdigit()):
            res.err("V08_CG_FORMAT", f"claim_group {cg!r} not CGnn-prefixed")
            continue
        known_names = {predef_by_id.get(cg_id), scope_name_by_id.get(cg_id)} - {None}
        if cg not in known_names:
            res.err("V08_CG_UNKNOWN",
                    f"claim_group {cg!r} matches neither the CG01–CG20 predefinition name "
                    f"nor the frozen scope120 name for {cg_id} ({sorted(known_names)})")
        if cg_id in seen_cg_ids:
            res.err("V28_GROUP_DUP", f"duplicate claim group id {cg_id}")
        seen_cg_ids.add(cg_id)
        if cg in seen_groups:
            res.err("V28_GROUP_DUP", f"duplicate claim_group entry {cg_id}")
        seen_groups.add(cg)
        # echo fidelity vs frozen scope registration — BY ID (alias-proof)
        if cg_id in scope_rows_by_id:
            row = scope_rows_by_id[cg_id]
            if g.get("condition_met_echo") != row["condition_met"]:
                res.err("V08_COND_ECHO",
                        f"{cg_id}: condition_met_echo {g.get('condition_met_echo')!r} != frozen scope {row['condition_met']!r} (name variant does not bypass)")
            if g.get("criticality") != row["active_criticality"]:
                res.err("V08_CRIT_ECHO",
                        f"{cg_id}: criticality {g.get('criticality')!r} != frozen scope {row['active_criticality']!r} (name variant does not bypass)")
            # F0-UQ-001: 013 CG04/CG10 stay UNRESOLVED, never coerced
            if (ctx.get("case_id") == UNRESOLVED_SCOPE_CASE
                    and cg_id in UNRESOLVED_SCOPE_CGS):
                if g.get("condition_met_echo") in ("TRUE", "FALSE"):
                    res.err("V08_013_COERCED",
                            f"{UNRESOLVED_SCOPE_CASE} {cg_id}: condition_met coerced to "
                            f"{g.get('condition_met_echo')!r}; must stay UNRESOLVED_NO_APPROVED_PRECEDENT (F0-UQ-001)")
                ss = set(g.get("source_status_set") or [])
                if "VERIFIED_MIS_CITATION_CRITICAL" in ss or "VERIFIED_MIS_CITATION_SYSTEMIC" in ss:
                    res.review("V08_013_ROUTE_TEACHER",
                               f"{UNRESOLVED_SCOPE_CASE} {cg_id}: mis-citation CRITICAL/SYSTEMIC while task condition "
                               "UNRESOLVED → route to teacher/bio adjudication via review queue; no auto-KE")
        else:
            # group outside the per-case frozen scope rows: enforce the frozen
            # predefinition attributes (CORE fixed attribute per approved text;
            # no invented defaults)
            attrs = predef_attrs.get(cg_id) or {}
            if attrs.get("condition_type") == "UNCONDITIONAL":
                if g.get("condition_met_echo") != "NOT_APPLICABLE_UNCONDITIONAL":
                    res.err("V08_UNCOND_ECHO",
                            f"{cg_id}: UNCONDITIONAL predefinition group requires "
                            f"condition_met_echo=NOT_APPLICABLE_UNCONDITIONAL, got {g.get('condition_met_echo')!r}")
                expected_crit = attrs.get("criticality_unconditional")
                if expected_crit and g.get("criticality") != expected_crit:
                    res.err("V08_UNCOND_CRIT",
                            f"{cg_id}: criticality {g.get('criticality')!r} != frozen predefinition {expected_crit!r}")
        # status set / severity consistency
        ss = g.get("source_status_set")
        if not isinstance(ss, list) or not ss:
            res.err("V08_STATUS_SET_EMPTY", f"{cg_id}: source_status_set empty/invalid")
            ss = []
        mis_sevs = [MISCIT_SEV_FROM_STATUS[s] for s in ss if s in MISCIT_SEV_FROM_STATUS]
        sev = g.get("severity")
        if mis_sevs:
            expected = max(mis_sevs, key=lambda s: SEV_RANK[s])
            if sev != expected:
                res.err("V08_SEV_MISMATCH",
                        f"{cg_id}: severity {sev!r} != highest mis-citation level {expected!r} in status set")
            group_sev.append(expected)
        else:
            if sev not in ("NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION", "NA"):
                res.err("V08_SEV_WITHOUT_MISCIT",
                        f"{cg_id}: severity {sev!r} but no VERIFIED_MIS_CITATION_* in status set")
        if not (g.get("basis") or "").strip():
            res.err("V08_BASIS_EMPTY", f"{cg_id}: basis empty")
        # V15: evidence refs in group entries
        _check_refs(g.get("evidence_refs") or [], ctx, res, f"d5.{cg_id}")

    # required coverage: the 6 scope-registered groups + core unconditional
    # groups, compared at CG-id level (name variants handled above)
    required_ids = set(scope_name_by_id.keys()) | {"CG01", "CG02", "CG03", "CG05", "CG07"}
    missing_ids = required_ids - seen_cg_ids
    if missing_ids:
        res.err("V08_GROUP_COVERAGE",
                f"claim_groups missing required entries: {sorted(missing_ids)}")

    sev_overall = reg.get("severity_overall")
    expected_overall = (max(group_sev, key=lambda s: SEV_RANK[s]) if group_sev
                        else "NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION")
    if sev_overall != expected_overall:
        res.err("V08_SEV_OVERALL",
                f"severity_overall {sev_overall!r} != highest group mis-citation severity {expected_overall!r}")
    d5 = dims.get("D5") if isinstance(dims.get("D5"), dict) else {}
    if sev_overall in ("CRITICAL", "SYSTEMIC"):
        sc5 = d5.get("score")
        if d5.get("score_status") == "SCORED" and is_pure_int(sc5) and sc5 > 4:
            res.err("V08_CAP_BREACH", f"D5 score {sc5} >4 despite severity_overall={sev_overall} (cap≤4)")
        if d5.get("key_error") != "Y":
            res.err("V08_CAP_KE", f"severity_overall={sev_overall} triggers D5 key error; D5.key_error must be Y")
    # soft band checks (review flags, not rejections — UPD-09: no invented parameters)
    if sev_overall == "NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION" and "D5" in ke_y_dims:
        res.review("V08_KE_WITHOUT_MISCIT",
                   "D5 KE=Y without verified mis-citation — allowed only under '完全不可追查' clause; needs human review")
    dr_all_generic = False
    if groups and scope_rows_by_id:
        dr = [g for g in groups if isinstance(g, dict) and
              any(tok in (g.get("criticality") or "") for tok in DECISION_RELEVANT_CRITICALITY_TOKENS)]
        dr_all_generic = bool(dr) and all(
            set(g.get("source_status_set") or []) <= {"GENERIC_SOURCE"} for g in dr)
    if dr_all_generic and d5.get("score_status") == "SCORED" and is_pure_int(d5.get("score")) and d5["score"] > 6:
        res.review("V08_GENERIC_BAND",
                   f"all DECISION_RELEVANT groups GENERIC_SOURCE but D5={d5['score']} (>6); rubric usual band 3–4 — review")

    # V09: fact verification register
    fv = rating.get("fact_verification_register")
    fv = fv if isinstance(fv, list) else []
    fv_ids = set()
    for item in fv:
        if not isinstance(item, dict):
            res.err("V09_FV_NOT_OBJ", "fact_verification_register entry not object")
            continue
        cid = item.get("claim_id")
        if cid in fv_ids:
            res.err("V09_FV_DUP", f"duplicate claim_id {cid}")
        fv_ids.add(cid)
        stt = item.get("status")
        refs = item.get("evidence_refs") or []
        if stt in ("SUPPORTED", "CONTRADICTED"):
            hard = [r for r in refs if isinstance(r, dict)
                    and r.get("ref_type") in ("E0_EVIDENCE", "GOLD_SLICE")]
            if not hard:
                res.err("V09_VERDICT_NO_FROZEN_EVIDENCE",
                        f"{cid}: status={stt} requires ≥1 E0_EVIDENCE/GOLD_SLICE ref "
                        "(fact verdicts only from frozen evidence, never from model memory)")
        _check_refs(refs, ctx, res, f"fv.{cid}")

    # V15: dimension-level evidence refs
    for d in DIMENSIONS:
        dim = dims.get(d)
        if isinstance(dim, dict):
            _check_refs(dim.get("evidence_refs") or [], ctx, res, d)
            arg = dim.get("key_error_argument")
            if isinstance(arg, dict):
                _check_refs(arg.get("verification_evidence") or [], ctx, res, f"{d}.ke")

    # V10/V11: totals linkage + recompute via the SINGLE shared contract
    # (f2r12_common.totals_contract — validator/canonical/projection identical;
    # audit F2-P1-05: MISSING=1 participates with weight retained)
    wt = rating.get("weighted_total")
    ss_total = rating.get("scientific_subscore")
    ts = rating.get("total_status")
    tc = totals_contract(dims)
    if tc["status"] == "NOT_COMPARABLE":
        if wt != "NOT_COMPARABLE":
            res.err("V10_NE_RENORMALIZED",
                    f"dims {tc['ne_na_dims']} are NE/NA but weighted_total={wt!r}; must be NOT_COMPARABLE, no renormalization")
        if ss_total != "NOT_COMPARABLE":
            res.err("V11_SUB_RENORMALIZED",
                    f"dims {tc['ne_na_dims']} are NE/NA but scientific_subscore={ss_total!r}; must be NOT_COMPARABLE")
        if ts != "NOT_COMPARABLE":
            res.err("V10_TOTAL_STATUS", f"total_status must be NOT_COMPARABLE when any dim NE/NA, got {ts!r}")
    elif tc["status"] == "COMPARABLE":
        recomputed = tc["weighted_total"]
        if not (isinstance(wt, (int, float)) and not isinstance(wt, bool) and math.isfinite(wt)):
            res.err("V10_TOTAL_TYPE", f"weighted_total must be finite number when all dims SCORED/MISSING, got {wt!r}")
        elif abs(wt - recomputed) > 0.01:
            res.correction("weighted_total", wt, recomputed)
        if ts != "COMPARABLE":
            res.err("V10_TOTAL_STATUS", f"all dims SCORED/MISSING but total_status={ts!r} (expected COMPARABLE)")
        sub_recomputed = tc["scientific_subscore"]
        if not (isinstance(ss_total, (int, float)) and not isinstance(ss_total, bool)
                and math.isfinite(ss_total)):
            res.err("V11_SUB_TYPE", f"scientific_subscore must be finite number, got {ss_total!r}")
        elif abs(ss_total - sub_recomputed) > 0.01:
            res.correction("scientific_subscore", ss_total, sub_recomputed)
    else:
        res.err("V03_STATUS_INCOMPLETE",
                f"dims {tc['incomplete_dims']} lack a legal status/score combination — every dim must have one")

    # V12: traits counts closure
    cov = rating.get("coverage")
    if isinstance(cov, dict):
        tc = cov.get("traits_counts")
        if isinstance(tc, dict):
            req, f_, u, o = (tc.get("required"), tc.get("filled"),
                             tc.get("explicit_unknown"), tc.get("omitted"))
            if req != TRAITS_REQUIRED_COUNT:
                res.err("V12_TRAITS_REQUIRED", f"traits_counts.required={req!r} != {TRAITS_REQUIRED_COUNT}")
            if all(is_pure_int(x) for x in (f_, u, o)):
                if f_ + u + o != TRAITS_REQUIRED_COUNT:
                    res.err("V12_TRAITS_SUM", f"filled({f_})+explicit_unknown({u})+omitted({o}) != {TRAITS_REQUIRED_COUNT}")
            else:
                res.err("V12_TRAITS_TYPE", "traits_counts fields must be strict integers")

    # V13: scientific shortfall linkage
    sf = rating.get("scientific_shortfall")
    if isinstance(sf, dict):
        expected_short = sorted(d for d in ("D2", "D3a", "D3b", "D4")
                                if d in scored_values and scored_values[d] < 5)
        got = sorted(sf.get("dims") or [])
        if got != expected_short:
            res.err("V13_SHORTFALL_DIMS",
                    f"scientific_shortfall.dims {got} != required {expected_short} (SCORED and <5)")
        if bool(sf.get("flag")) != bool(expected_short):
            res.err("V13_SHORTFALL_FLAG",
                    f"scientific_shortfall.flag={sf.get('flag')!r} inconsistent with dims {expected_short}")

    # V26: review queue internal consistency
    rq = rating.get("review_queue")
    if isinstance(rq, dict):
        reasons = rq.get("reasons") or []
        if bool(rq.get("flag")) != bool(reasons) and not (rq.get("flag") and not reasons):
            # flag=true with empty reasons is allowed only if validator injected flags later;
            # flag=false with non-empty reasons is a contradiction
            if not rq.get("flag") and reasons:
                res.err("V26_REVIEW_INCONSISTENT", "review_queue.flag=false but reasons non-empty")

    return res


def _check_refs(refs, ctx, res: ValidationResult, where: str):
    """V15: fabricated citation / scope check — E0 evidence ids must exist in
    the request-provided list; GOLD_SLICE refs must exist in the slice;
    locator-bearing types need non-empty locator or support_scope."""
    ev_ids = set(ctx.get("evidence_ids") or [])
    gold_ids = set(ctx.get("gold_ref_ids") or [])
    scope_ids = set(ctx.get("scope_row_ref_ids") or [])
    for r in refs:
        if not isinstance(r, dict):
            res.err("V15_REF_NOT_OBJ", f"{where}: evidence ref not object")
            continue
        rt, rid = r.get("ref_type"), r.get("ref_id")
        if not (r.get("support_scope") or "").strip():
            res.err("V15_NO_SUPPORT_SCOPE", f"{where}: ref {rid!r} lacks support_scope (支持什么/不支持什么)")
        if rt == "E0_EVIDENCE":
            if ev_ids and rid not in ev_ids:
                res.err("V15_FABRICATED_EVIDENCE",
                        f"{where}: evidence_id {rid!r} not in frozen E0 list provided in request")
        elif rt == "GOLD_SLICE":
            if gold_ids and rid not in gold_ids:
                res.err("V15_FABRICATED_GOLD_REF",
                        f"{where}: gold ref {rid!r} not in provided gold slice")
        elif rt == "SCOPE_ROW":
            if scope_ids and rid not in scope_ids:
                res.err("V15_FABRICATED_SCOPE_REF",
                        f"{where}: scope ref {rid!r} not in provided scope rows")
        elif rt not in ("QUESTION_TEXT", "ANSWER_TEXT", "RUBRIC_CLAUSE"):
            res.err("V15_REF_TYPE", f"{where}: illegal ref_type {rt!r}")


def load_schema(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "RATING_OUTPUT_SCHEMA.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # CLI: validate one rating JSON file against a request-context JSON file
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("rating_json")
    ap.add_argument("ctx_json")
    ap.add_argument("--schema", default=None)
    a = ap.parse_args()
    with open(a.rating_json, encoding="utf-8") as f:
        raw = f.read()
    ctx = json.load(open(a.ctx_json, encoding="utf-8"))
    schema = load_schema(a.schema)
    try:
        rating = parse_rating_json(raw)
    except ValueError as e:
        print(json.dumps({"status": "INVALID", "errors": [{"code": "V20_PARSE", "message": str(e)}],
                          "corrections": [], "review_flags": []}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    out = validate_rating(rating, ctx, schema).to_dict()
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if out["status"] == "VALID" else 1)
