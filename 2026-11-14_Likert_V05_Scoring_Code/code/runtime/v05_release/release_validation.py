"""03E release validator — thin adapter over the accepted PATCH chain.

Replaces the V0.4 global rv.validate_rating/SCHEMA_ID use (no version pollution:
this module never calls the old SCHEMA_ID path; the legacy audited validators are
still invoked through the same reviewed pipeline r2p/s0/R3 chain).

Returns a ValidationResult-shaped object. Technical failure != scientific NE:
a received-but-NE/REVIEW_PENDING result is valid for transport purposes (never
re-sampled) but counts_as_formal stays False until RELEASE_APPROVAL.json exists.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "f2"))
sys.path.insert(0, str(HERE.parent / "pipeline"))
from common_03a import OUT, SCHEMA_PATH, VERSION, DIMS, sha, load, canonical
from rules_03a import decide, enforce_user_cap
import r2p_pipeline as PATCH_PIPE
from f2r12_common import totals_contract

parse_rating_json = None  # set below to avoid binding the old V0.4 schema id


class VRes:
    def __init__(self, valid, status, errors, corrections, review_flags, projection):
        self.valid = bool(valid)
        self.status = status
        self.errors = errors
        self.corrections = corrections
        self.review_flags = review_flags
        self.projection = projection

    def to_dict(self):
        return {"valid": self.valid, "status": self.status, "errors": self.errors,
                "corrections": self.corrections, "review_flags": self.review_flags,
                "projection": self.projection}


def _section(user, name, drop_intro=False):
    m = re.search(r"===SECTION:" + name + r"_BEGIN===\n(.*?)\n===SECTION:" + name + r"_END===", user, re.S)
    if not m:
        raise KeyError("section " + name)
    text = m.group(1)
    return text.split("\n", 1)[1] if drop_intro else text


def release_approved():
    p = OUT.parent / "approval/RELEASE_APPROVAL.json"
    if not p.is_file():
        return False
    try:
        rec = json.loads(p.read_text())
    except Exception:
        return False
    man = OUT.parent / "manifest/MANIFEST.json"
    if not man.is_file():
        return False
    return rec.get("manifest_sha256") == sha(man.read_bytes()) and rec.get("approved_for") == "live_scoring"


def verify_visible(item):
    """Recompute every program fact from visible bytes; raise ValueError on drift."""
    ctx, artifact = item["ctx"], item["artifact"]
    if artifact.get("release_id") != VERSION or artifact.get("live_runner") is not False:
        raise ValueError("release artifact identity mismatch")
    system, user = [x["content"] for x in artifact["messages"]]
    if len(artifact["messages"]) != 2:
        raise ValueError("two messages required")
    ie = ctx["identity_echo"]
    if sha(system.encode()) != ie["system_prompt_sha256"]:
        raise ValueError("system identity mismatch")
    if sha(user.encode()) != ctx["user_message_sha256"]:
        raise ValueError("user identity mismatch")
    vis = dict(re.findall(r"^- ([a-z_0-9]+)=([0-9a-f]{64})$", user, re.M))
    if vis != ie or len(vis) != 14:
        raise ValueError("14 identity mismatch")
    if sha(_section(user, "QUESTION", True).encode()) != ie["question_rendered_prompt_sha256"]:
        raise ValueError("question identity")
    if sha(_section(user, "ANSWER", True).encode()) != ie["answer_sha256"]:
        raise ValueError("answer identity")
    env = json.loads(_section(user, "RELEASE_CONTRACT", True))
    if env != ctx["release_contract"]:
        raise ValueError("release contract mismatch")
    ci = env["target_fact_contract"].get("consumer_identity")
    if (not isinstance(ci, dict) or ci.get("b_slot_uid") != ctx["b_slot_uid"]
            or ci.get("case_id") != ctx["case_id"]
            or ci.get("answer_sha256") != ie["answer_sha256"]):
        raise ValueError("contract consumer identity not bound to this frozen answer")
    blocks = ctx["coordination_block_texts"]
    for key, name in [("task_scope", "TASK_SCOPE"), ("route_diagnosis", "ROUTE_DIAGNOSIS"),
                      ("accepted_sets", "ACCEPTED_SETS"), ("step_evidence", "EVIDENCE_FIVE_STATE")]:
        if _section(user, name, True) != blocks[key]:
            raise ValueError("message/ctx " + key)
    for field, k in [("task_scope_sha256", "task_scope"), ("route_diagnosis_sha256", "route_diagnosis"),
                     ("accepted_sets_sha256", "accepted_sets")]:
        if sha(blocks[k].encode()) != ie[field]:
            raise ValueError("object " + field)
    base = _section(user, "BASE_RANGES", True) + "\n" + canonical(env)
    if base != blocks["base_ranges"] or sha(base.encode()) != ie["base_ranges_sha256"]:
        raise ValueError("base/candidate digest mismatch")
    rules = load(OUT / "SCORE_RULES_RELEASE.json")
    actual = decide(env["target_fact_contract"], rules)
    if actual != env["d3a_release_decision"]:
        raise ValueError("decision not derived from visible facts")
    if env["proof_registry_identity_sha256"] != sha((OUT / "proofs/REGISTRY_IDENTITIES.json").read_bytes()):
        raise ValueError("proof registry identity mismatch")
    if env["release_id"] != VERSION or ctx.get("policy") != "A" \
            or ctx["eligibility"] != {"policy_A": actual["high_tier_eligible"]} \
            or ctx["c_confirmed"] != actual["confirmed_target_rate"]:
        raise ValueError("release policy/eligibility/count mismatch")
    ff = {}
    lines = blocks["step_evidence"].splitlines()
    hdr = lines[0].split("\t")
    for row in lines[1:]:
        x = dict(zip(hdr, row.split("\t")))
        ff[x["gold_step_id"]] = {"route_state": x["route_step_state"], "credit_class": x["credit_class"],
                                 "five_state": x["five_state"], "conclusion": x["step_conclusion"]}
    if ff != ctx["step_facts"] or set(ff) != set(ctx["required_gold_step_ids"]):
        raise ValueError("visible fact/target set differs from ctx")
    return actual


def validate_rating(rating, item, schema):
    """item = {"ctx":CTX, "artifact":ART} (plus runner fields)."""
    ctx = item["ctx"]
    try:
        decision = verify_visible(item)
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        return VRes(False, "REJECTED", [{"gate": "03E-CONTRACT", "message": str(e)}], [], [],
                    {"counts_as_formal": False, "stage": "03E-CONTRACT"})
    upstream = PATCH_PIPE.process_rating(rating, dict(ctx, schema=schema))
    errors = list(upstream["errors"])
    d3 = (rating.get("dimensions") or {}).get("D3a") or {}
    try:
        enforce_user_cap(d3.get("score"), decision["user_key_failure_gate"])
    except ValueError as e:
        errors.append({"gate": "03E-USER-KEY4", "message": str(e)})
    if decision["score_status"] == "NE":
        if d3.get("score_status") != "NE" or d3.get("score") is not None \
                or not d3.get("ne_basis") or not d3.get("ne_unverified"):
            errors.append({"gate": "03E-UNKNOWN",
                           "message": "undetermined band/key requires NE/null and paired bases; no guessed score"})
    elif decision["score_status"] == "MISSING":
        if d3.get("score_status") != "MISSING" or d3.get("score") != 1 or not d3.get("missing_basis"):
            errors.append({"gate": "03E-MISSING",
                           "message": "whole-module missing requires MISSING=1 with basis"})
    elif decision["score_status"] == "JUDGE_REQUIRED":
        if d3.get('score_status') == 'SCORED':
            score = d3.get('score')
            lo, hi = decision['allowed_range']
            if type(score) is not int or not lo <= score <= hi:
                errors.append({'gate':'03E-RANGE','message':'judge-assessed score exceeds the existing evidence/known-failure ceiling'})
            if not d3.get('rationale') or not d3.get('evidence_refs'):
                errors.append({'gate':'03E-JUDGEMENT','message':'numeric judgement requires a rubric rationale and supplied references'})
        elif d3.get('score_status') == 'NE':
            if d3.get('score') is not None or not d3.get('ne_basis') or not d3.get('ne_unverified'):
                errors.append({'gate':'03E-UNKNOWN','message':'genuine uncertainty requires NE/null and specific paired bases'})
        else:
            errors.append({'gate':'03E-STATUS','message':'automatic matcher pending needs actual SCORED or specifically justified NE judgement'})
    elif d3.get("score_status") == "SCORED":
        sc = d3.get("score")
        lo, hi = decision["allowed_range"]
        if type(sc) is not int or not lo <= sc <= hi:
            errors.append({"gate": "03E-RANGE", "message": "release D3a band mismatch"})
        if decision.get("ne_unverified") and not (d3.get("ne_basis") and d3.get("ne_unverified")):
            errors.append({"gate": "03E-LOCAL-U", "message": "local U requires paired fields"})
    elif d3.get("score_status") != "NE":
        errors.append({"gate": "03E-STATUS", "message": "assessable module cannot claim missing/not applicable"})
    approved = release_approved()
    if errors:
        status, valid = "REJECTED", False
    elif decision["score_status"] == "NE" or upstream["status"] == "REVIEW_PENDING":
        status, valid = "REVIEW_PENDING", True
    elif upstream["status"] == "ACCEPTED":
        status, valid = ("ACCEPTED" if approved else "PENDING_RELEASE_APPROVAL"), True
    else:
        status, valid = ("CORRECTED" if approved else "PENDING_RELEASE_APPROVAL"), True
    proj = dict(upstream["projection"])
    proj["counts_as_formal"] = bool(proj.get("counts_as_formal")) and approved and valid \
        and status in ("ACCEPTED", "CORRECTED")
    proj["release_id"] = VERSION
    proj["release_approved"] = approved
    proj["formal_scoring_gated"] = not approved
    return VRes(valid, status, errors, upstream["corrections"], upstream["review_flags"], proj)


def parse(content):
    from f2r12_response_validator import parse_rating_json as _p
    return _p(content)


# Output compatibility amendment 2026-11-12: requests and scientific rules unchanged.
_strict_validate_before_format_compat = validate_rating
def validate_rating(rating, item, schema):
    from format_compat import validate_compatible
    original_scores = {d: obj.get("score") for d,obj in (rating.get("dimensions") or {}).items()
                       if isinstance(obj,dict)}
    result, effective, mappings = validate_compatible(
        rating, item, schema, _strict_validate_before_format_compat, apply_caps=True)
    if result.valid:
        caps = result.projection.get("program_score_caps") or []
        if mappings or caps:
            result.projection["raw_model_dimension_scores"] = original_scores
            result.projection["effective_rating_is_derived_from_preserved_wire"] = True
            rating.clear()
            rating.update(effective)
        for cap in caps:
            result.corrections.append({"field":"dimensions."+cap["dimension"]+".score",
                "reported":cap["raw_model_score"],"program_value":cap["effective_score"],
                "action":"PROGRAM_CAPPED_EXISTING_RULE","basis":cap["basis"]})
        if caps and result.status in ("ACCEPTED","CORRECTED"):
            result.status="CORRECTED"
    return result
