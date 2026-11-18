"""03E item assembly (derived from accepted S0 renderer + 03A/03D example chain).

One render function for every slot. Reuses the reviewed accepted data blocks byte
for byte (question/answer/gold slice/E0 evidence/scope rows come from the same
audited builders); the release changes ONLY the version identity, the compact
release contract (duplicate machine rule JSON removed per card §4), the case
relevant trait overlay, and the frozen branch mapping consumer identity.

Zero API, zero network. Deterministic: same bytes -> same sha anywhere.
"""
import json, re, sys, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "f2"))
from common_03a import (OUT, RUN_ROOT, W, B, S0, F2, SCHEMA_PATH, VERSION, DIMS,
                        BRANCH_MAP, sha, canonical, load, rows, identity)
from rules_03a import decide

_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)
CALIB_CASES = ["BIOPATH150_041", "BIOPATH150_001", "BIOPATH150_006", "BIOPATH150_007",
               "BIOPATH150_020", "BIOPATH150_002", "BIOPATH150_024", "BIOPATH150_018"]
QUARANTINE_SLOTS = {"B480-0201", "B480-0202", "B480-0203", "B480-0204",
                    "B480-0305", "B480-0306", "B480-0307", "B480-0308"}
SCHEMA_ID = "LIKERT_V05_AI_RATING_OUTPUT_SCHEMA_CANDIDATE_R3"  # schema bytes reused verbatim
DIAG_HDR = "gold_step_id\tstep_state\treason_code\tbinding_status\tjac_sub\tjac_prod\tnote"
SEC_HDR = ("gold_step_id\tkey_step_class\troute_step_state\troute_reason_code\tcredit_class"
           "\tfive_state\tstep_conclusion\thighest_support_granularity"
           "\tmissing_for_next_granularity")
ACC_HDR = ("step_occurrence_id\taccepted_enzyme_names\taccepted_ec_normalized_set"
           "\tname_ec_pairs\tec_class\tdisputed_flags\tsupport_scope_statement")
RANGE_HDR = ("D1_task_range\tD2_chemical_range\tD3a_range\td3a_9_10_policyA"
             "\td3a_9_10_policyB\td3a_cap\trule_ids")
R2 = RUN_ROOT / "LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK"
R3 = RUN_ROOT / "LIKERT_V05_REVISION_20261105_R3"


def parse_answer(text):
    try:
        return json.loads(text)
    except Exception:
        return json.loads(_FENCE.sub("", text.strip()).strip())


def load_tables():
    import f2r12_item_builder as LEG
    route = {r["b_slot_uid"]: r for r in rows(R2 / "ROUTE_CASE_RESULTS_480.tsv")}
    align, sec, acc = {}, {}, {}
    for r in rows(R2 / "STEP_ALIGNMENT.tsv"):
        align.setdefault(r["b_slot_uid"], []).append(r)
    for r in rows(R3 / "P2_DISPOSITION_EVIDENCE/STEP_EVIDENCE_STATES_R3.tsv"):
        sec.setdefault(r["b_slot_uid"], []).append(r)
    for r in rows(OUT / "accepted/ACCEPTED_ENZYMES_RELEASE.tsv"):
        acc.setdefault(r["case_id"], []).append(r)
    base = {r["b_slot_uid"]: r for r in rows(R3 / "P3_RULES_TOOLS/BASE_SCORES_AND_REVIEW_FLAGS_R3.tsv")}
    scope = {r["case_id"]: r for r in rows(R2 / "CASE_TASK_SCOPE_120.tsv")}
    qa = {r["case_id"]: r for r in rows(R2 / "REFERENCE_QA_SIGNALS_R2.tsv")}
    mapping = {r["b_slot_uid"]: r for r in rows(BRANCH_MAP)}
    trait = rows(B / "TRAIT_OVERLAY_PROPOSED.tsv")
    return route, align, sec, acc, base, scope, qa, mapping, trait


def section(user, name, drop_intro=False):
    text = re.search(r"===SECTION:" + name + r"_BEGIN===\n(.*?)\n===SECTION:" + name + r"_END===",
                     user, re.S).group(1)
    return text.split("\n", 1)[1] if drop_intro else text


def source_alignment(align_rows, gid):
    return next((x for x in align_rows if x["gold_step_id"] == gid), {})


def has_enzyme_information(step):
    """Answer delivery is separate from automatic scientific acceptance."""
    enzyme = step.get('enzyme') if isinstance(step, dict) else None
    if isinstance(enzyme, dict):
        return any(str(enzyme.get(k) or '').strip() for k in ('name', 'ec_number'))
    return isinstance(enzyme, str) and bool(enzyme.strip())


def derive_contract(ctx, answer, scope_row, mapping_row, traits, reference_hold):
    blocks = ctx["coordination_block_texts"]
    text = blocks["step_evidence"].splitlines()
    hdr = text[0].split("\t")
    source_rows = {d["gold_step_id"]: d for d in (dict(zip(hdr, x.split("\t"))) for x in text[1:] if x.strip())}
    scope = json.loads(blocks["task_scope"])
    complete = (scope["graph_status"] == "LINEAR_UNIQUE" and scope.get("reference_insufficient") == "FALSE")
    targets = []
    for gid, f in ctx["step_facts"].items():
        sr = source_rows[gid]
        alignment = source_alignment(ctx["_align_rows"], gid)
        pred_id = alignment.get("pred_step_id") or alignment.get("pred_step")
        original_step = next((x for x in answer.get("steps", []) if x.get("step_id") == pred_id), None)
        enzyme = original_step.get("enzyme") if original_step else None
        specific_annotation = (enzyme or {}).get("gene_or_protein")
        grain_pending = False  # an annotation string does not assert measured protein/whole-strain activity
        proof = None
        pid = "REAL-ROUTE-" + ctx["b_slot_uid"] + "-" + gid
        registry = load(OUT / "proofs/REAL_PROOF_BINDINGS.json")["records"]
        if pid in registry:
            proof = {"proof_id": pid}
        targets.append({'target_id': gid, **f, 'source_locator': 'SOURCE_STEP_EVIDENCE#' + gid,
                        'delivered': True if original_step is not None or f['route_state'] == 'MATCH' else None,
                        'enzyme_info_present': has_enzyme_information(original_step) if original_step is not None else None,
                        'support_at_claim_granularity': True if f['credit_class'] == 'CONFIRMED_TARGET' and f['five_state'] == 'SUPPORTED' and not grain_pending else None,
                        'explicit_ec_pair_status': 'CONFIRMED' if f['credit_class'] == 'CONFIRMED_TARGET' else 'UNRESOLVED',
                        'importance': 'MAJOR', 'key': complete or sr['key_step_class'].startswith('KEY_'),
                        'reference_or_scope_gap': reference_hold or f['credit_class'] == 'ROUTE_HOLD_REFERENCE',
                        'route_failure_proof': proof, 'catalytic_failure_proof': None,
                        'omission_locator': ('ANSWER.steps[step_id=' + str(pred_id) + '].enzyme (name and EC absent)'
                                             if original_step is not None and not has_enzyme_information(original_step) else ''),
                        'support_scope': 'existing functional target support only; no automatic specific-protein/strain activity certification',
                        'original_key_step_class': sr['key_step_class'],
                        'proposed_key_reason': 'D-KEYDEF-20261110 confirmed: entry/terminal plus mandatory intermediate of the defined required main chain (scope-registry bound)' if complete else 'original ENTRY/TERMINAL role retained; DAG consumption follows frozen mapping BRANCH_PATH_MAPPING_03E + registry runtime gates (03A-4 band/confirmation publication stays NE until key definition complete)'})
        targets[-1].update(function_component_supported=f['credit_class'] == 'CONFIRMED_TARGET',
                           original_pred_step_id=pred_id, gene_or_protein_annotation=specific_annotation,
                           claim_grain_pending=grain_pending,
                           claim_grain_note='function/pair support consumed unchanged; optional gene attribution separately unresolved')
        extra_claims = []
        if specific_annotation:
            extra_claims.append({'claim_id': gid + '#gene_or_protein', 'type': 'ORDINARY_GENE_ANNOTATION',
                                 'value': specific_annotation, 'status': 'UNRESOLVED', 'materiality': 'MINOR',
                                 'applies_to': 'D3a',
                                 'materiality_basis': 'task requires preferred enzyme and EC, not measured activity of a specific protein; this optional identifier alone does not change established target function',
                                 'source_locator': 'ANSWER.steps[step_id=' + str(pred_id) + '].enzyme.gene_or_protein',
                                 'required_support': 'attribution-specific evidence, not inferred from G4 accepted name',
                                 'scientifically_confirmed': False})
        targets[-1]['key_authority_status'] = ('METHOD_CONFIRMED_REGISTRY_BOUND_WHEN_CONSUMED' if complete
                                               else 'INHERITED_OLD_LABEL_OR_FROZEN_BRANCH_MAPPING_PENDING')
        targets[-1]['claim_components'] = {
            'target_function': {'status': 'SUPPORTED' if f['credit_class'] == 'CONFIRMED_TARGET' else 'UNRESOLVED',
                                 'scope': 'target reaction function'},
            'name_explicit_ec_pair': {'status': targets[-1]['explicit_ec_pair_status'],
                                       'explicit_ec': (enzyme or {}).get('ec_number')},
            'gene_or_protein_attribution': {'value': specific_annotation,
                                             'status': 'UNRESOLVED' if specific_annotation else 'NOT_CLAIMED'},
            'experimental_activity_claim': {'statement': None,
                                             'status': 'NOT_IDENTIFIED_AS_MAIN_CLAIM_IN_THESE_EXISTING_RECORDS',
                                             'required_support': 'specific experimental/activity evidence if explicitly claimed'},
            'whole_strain_capability_claim': {'scope': 'separate D3b target, never inferred from gene field',
                                               'required_support': 'strain/pathway capability evidence if claimed'},
            'additional_claims': extra_claims}
    cid = {'b_slot_uid': ctx["b_slot_uid"], 'case_id': ctx["case_id"],
           'answer_sha256': ctx["identity_echo"]["answer_sha256"],
           'current_path_id': (mapping_row.get("current_path_id") or None) if mapping_row else None,
           'identity_source': __import__('os').environ.get('S6_IDENTITY_SOURCE','LIKERT_V04_FULL_SCORING_20261029/F0_INPUT_BASELINE/B_480_ANSWER_INDEX.tsv'),
           'mapping_version': mapping_row.get("mapping_version") if mapping_row else None}
    base_contract = {'original_N': len(targets), 'original_scope_total': int(scope['n_gold_steps_total']),
            'background_count': int(scope['n_background']),
            'target_ids': sorted(ctx['required_gold_step_ids']), 'targets': targets,
            'scope_status': 'REFERENCE_HOLD' if reference_hold else 'DEFINED_CANDIDATE',
            'key_definition_complete': complete,
            'module_delivered': any(has_enzyme_information(step) for step in answer.get('steps', [])),
            'module_delivery_locator': 'ANSWER.steps[*].enzyme.name/ec_number',
            'synthetic': False,
            'independent_key_error': None, 'consumer_identity': cid}
    # --- REF3FIX (isolated-copy narrow change; card POST_REF3_EXISTING_PROGRAM_NE_CLOSEOUT) ---
    # A BRANCHED_DAG slot whose frozen mapping already binds an ADOPTED selected path may
    # have D3a facts consumed over that path's target subset instead of the whole graph.
    # Conditions are ALL existing facts (mapping/catalog/KEY registry/ctx); no new rule,
    # no new selection, no branch-picking. Anything not meeting them returns the base
    # contract verbatim (original PENDING/incomplete behavior preserved).
    if (scope['graph_status'] == 'BRANCHED_DAG' and not reference_hold
            and cid.get('current_path_id') and mapping_row
            and (mapping_row.get('mapping_status') or '') == 'BOUND'):
        sel = cid['current_path_id']
        from registry_03d import _path_index
        cat_idx, _steps_idx = _path_index()
        prow = cat_idx.get(ctx['case_id'], {}).get(sel)
        if prow and prow['adoption_status'] == 'ADOPTED_METHOD_CONFIRMED':
            chain_ids = [x for x in (prow['ordered_step_ids'] or '').split('|') if x]
            reg = load(OUT / 'KEY_DEFINITION_BINDINGS.json')
            conf = reg.get('confirmed_real_keys', {})
            registered = all(
                t in ctx['step_facts'] and t in conf
                and str(conf[t].get('scope_kind', '')).startswith('PATH_CATALOG')
                and sel in [b.get('path_id') for b in (conf[t].get('path_bindings') or [])]
                and not t in reg.get('held_real_keys', {})
                for t in chain_ids)
            if chain_ids and registered:
                subset = [dict(t, key=True, key_authority_status='METHOD_CONFIRMED_REGISTRY_BOUND_WHEN_CONSUMED')
                          for t in targets if t['target_id'] in set(chain_ids)]
                total = base_contract['original_scope_total']
                bc = dict(base_contract)
                bc['target_ids'] = sorted(chain_ids)
                bc['targets'] = subset
                bc['original_N'] = len(subset)
                # closure original_scope_total = N + background_count, preserved with the
                # whole-graph rows outside the selected chain as the non-consumed count
                bc['background_count'] = total - len(subset)
                # KEY applicability: every chain target carries a confirmed D-KEYDEF/D-KEY4
                # PATH_CATALOG registration binding THIS path -> key definition complete.
                bc['key_definition_complete'] = True
                bc['consumed_via'] = {'selected_path_id': sel, 'mapping_status': 'BOUND',
                                      'catalog_row_adoption': 'ADOPTED_METHOD_CONFIRMED',
                                      'chain_steps': chain_ids}
                return bc
    return base_contract


def build_release_envelope(ctx, contract, decision, traits, ar, high):
    case = ctx["case_id"]
    relevant = [t for t in traits if case == "BIOPATH150_020"] if traits else []
    return {
        "release_id": VERSION,
        "review_status": "READY_FOR_RELEASE_REVIEW (RELEASE_APPROVAL.json binding the MANIFEST sha is required before live scoring)",
        "requested_dimensions": DIMS,
        "actual_decision_ids": ["D-M01", "D-KEY4", "D-KEYDEF-20261110", "D-GRAIN-20261110",
                                 "D-BANDS-20261110", "D-TRAITS-20261110", "D-FAST-RUN-20261110",
                                 "D-RATER-SCOPE-20261110"],
        "consumer_identity": contract["consumer_identity"],
        "target_fact_contract": contract,
        "d3a_release_decision": decision,
        "proof_registry_identity_sha256": sha((OUT / "proofs/REGISTRY_IDENTITIES.json").read_bytes()),
        "source_fact_semantics": "original facts untouched; S/F/M/U/H mapping certifies no new chemistry; caps and fixed facts are program-verified and cannot be rewritten by the scorer",
        "required_reply_if_NE": {"score_status": "NE", "score": None, "ne_basis": decision["ne_basis"],
                                  "ne_unverified": decision["ne_unverified"]},
        "NE_transport_range": "HELD sentinel or [1,10] is a transport envelope, never permission to score; the NE gate above controls",
        "trait_overlay_reference": identity(B / "TRAIT_OVERLAY_PROPOSED.tsv"),
        "trait_overlay_case_rows": relevant,
    }


def render_slot(slot, anon, tables, rules, schema, template, system):
    import f2r12_item_builder as LEG
    route, align, sec, acc, base, scope, qa, mapping, traits = tables
    cr = route[slot]
    _, idx = LEG.load_b480_index()
    evman = RUN_ROOT / "LIKERT_V04_FULL_SCORING_20261029/F3_EVIDENCE_R1_1/EVIDENCE_MANIFEST_R1_1.json"
    evidence_binding = {"mode": "F3_R11_CASE_SLICES_V2", "manifest_path": str(evman),
                        "expected_manifest_sha256": sha(evman.read_bytes())}
    payload = LEG.build_item(slot, anon, {}, evidence_binding, S0 / "gold_slices", mode="TEST")
    case = payload["case_id"]
    blocks = {
        "task_scope": json.dumps(scope[case], ensure_ascii=False, sort_keys=True),
        "route_diagnosis": DIAG_HDR + "\n" + "\n".join(
            "\t".join(str(r.get(k, "")) for k in DIAG_HDR.split("\t"))
            for r in sorted(align.get(slot, []), key=lambda x: x["gold_step_id"])),
        "accepted_sets": ACC_HDR + "\n" + "\n".join(
            "\t".join(str(r.get(k, "")) for k in ACC_HDR.split("\t"))
            for r in sorted(acc.get(case, []), key=lambda x: (x.get("step_scope_class", ""), x["step_occurrence_id"]))
            if r.get("step_scope_class") == "REQUIRED"),
        "step_evidence": SEC_HDR + "\n" + "\n".join(
            "\t".join(str(r.get(k, "")) for k in SEC_HDR.split("\t"))
            for r in sorted(sec.get(slot, []), key=lambda x: x["gold_step_id"])),
    }
    body = payload["user_message"]

    def extract(name):
        m = re.search(r"===SECTION:%s_BEGIN===\n(.*?)\n===SECTION:%s_END===" % (name, name), body, re.S)
        assert m, name
        block = m.group(1)
        nl = block.find("\n")
        return block[nl + 1:] if nl > 0 else block
    qtext, atext = extract("QUESTION"), extract("ANSWER")
    rawanswer = LEG.load_answer(idx[slot])
    assert rawanswer == atext.encode("utf-8")
    assert sha(qtext.encode("utf-8")) == idx[slot]["question_rendered_prompt_sha256"]
    reference_hold = False  # 060/094 never reach here (excluded from targets); per-case holds: none current
    visfacts = {}
    lines = blocks["step_evidence"].splitlines()
    h = lines[0].split("\t")
    for l in lines[1:]:
        d = dict(zip(h, l.split("\t")))
        visfacts[d["gold_step_id"]] = {"route_state": d["route_step_state"], "credit_class": d["credit_class"],
                                       "five_state": d["five_state"], "conclusion": d["step_conclusion"]}
    ctx = {"b_slot_uid": slot, "b_slot_uid_coordination_only": slot, "case_id": case,
           "identity_echo": dict(payload["identity_echo"]),
           "batch": "batchB_recovery_inclusive", "anonymous_item_id": anon,
           "route_status": cr["route_status_chemical"], "task_conformance_status": cr["task_conformance_status"],
           "required_gold_step_ids": sorted(visfacts), "step_facts": visfacts,
           "_align_rows": align.get(slot, []), "reference_hold": reference_hold,
           "reference_hold_reason": "", "frozen_record_contradiction": False,
           "coordination_block_texts": blocks}
    contract = derive_contract(ctx, parse_answer(atext), scope[case], mapping.get(slot), traits, reference_hold)
    decision = decide(contract, rules)
    bb = base[slot]
    ar = {"D1": bb["D1_task_range"], "D2": bb["D2_chemical_range"],
          "D3a": ("[" + ",".join(map(str, decision["allowed_range"])) + "]" if decision["allowed_range"]
                  else ("HELD_PENDING_REPRESENTATION_REVIEW" if ctx["route_status"] == "BOUNDARY_REVIEW" else "[1,10]")),
          "D3b": "[1,10]", "D4": "[1,10]", "D5": "[1,10]", "D6": "[1,10]"}
    ctx["allowed_ranges"] = ar
    high = decision["high_tier_eligible"]
    range_rows = RANGE_HDR + "\n" + "\t".join([ar["D1"], ar["D2"], ar["D3a"],
        "ELIGIBLE" if high else "NOT_ELIGIBLE", "NOT_SELECTED",
        ("D3a<=" + str(decision["confirmed_key_failure_cap"]) if decision["user_key_failure_gate"]["applicable"] else "NONE"),
        "R05-EV-02a;SDT-03A-U;RELEASE-" + VERSION])
    envelope = build_release_envelope(ctx, contract, decision, traits, ar, high)
    blocks["base_ranges"] = range_rows + "\n" + canonical(envelope)
    ie = dict(payload["identity_echo"])
    ie["rubric_text_sha256"] = sha(system[system.index("===FULL_RUBRIC_CANDIDATE_BEGIN==="):system.index("===RATING_SCHEMA_VERBATIM_BEGIN===")].encode())
    ie["system_prompt_sha256"] = sha(system.encode())
    ie["item_template_sha256"] = sha(template.encode())
    bs = {k: sha(v.encode()) for k, v in blocks.items()}
    ie["task_scope_sha256"] = bs["task_scope"]
    ie["route_diagnosis_sha256"] = bs["route_diagnosis"]
    ie["accepted_sets_sha256"] = bs["accepted_sets"]
    ie["base_ranges_sha256"] = bs["base_ranges"]
    sub = {
        "{{SCHEMA_ID}}": SCHEMA_ID,
        "{{VERSION_OBJECT_NOTE}}": VERSION + " READY_FOR_RELEASE_REVIEW schema-byte-reused",
        "{{ANONYMOUS_ITEM_ID}}": anon, "{{CASE_ID}}": case,
        "{{QUESTION_FULL_TEXT}}": qtext, "{{ANSWER_FULL_TEXT}}": atext,
        "{{GOLD_SLICE_CONTENT}}": extract("GOLD_SLICE"), "{{SCOPE_ROWS_TSV}}": extract("SCOPE_ROWS"),
        "{{EVIDENCE_ITEMS}}": extract("EVIDENCE"),
        "{{EVIDENCE_STATUS}}": payload["evidence_status"],
        "{{TASK_SCOPE_ROW}}": blocks["task_scope"], "{{ROUTE_DIAGNOSIS_ROWS}}": blocks["route_diagnosis"],
        "{{ROUTE_STATUS}}": ctx["route_status"], "{{TASK_CONFORMANCE}}": ctx["task_conformance_status"],
        "{{ACCEPTED_SETS_ROWS}}": blocks["accepted_sets"], "{{STEP_EVIDENCE_ROWS}}": blocks["step_evidence"],
        "{{BASE_RANGES_ROWS}}": range_rows, "{{RELEASE_CONTRACT_JSON}}": canonical(envelope),
    }
    for k in ie:
        sub["{{" + k.upper() + "}}"] = ie[k]
    # S6 wiring: the release template also carries the REF1 reference-catalog and
    # REF2 exact-table placeholders; filled from the same audited case-level rules
    # (s6_catalog.py reproduces them; equality with every shipped S4 message is an
    # offline-checked invariant, see offline checks).
    import s6_catalog as S6CAT
    cat = S6CAT.build_catalog(case, S6CAT.accepted_rows_for(case),
                              payload["validation_context"]["evidence_ids"])
    sub["{{REFERENCE_CATALOG_JSON}}"] = json.dumps(cat, ensure_ascii=False, indent=1)
    import build_ref2_requests as B2
    sub["{{CG_TRANSCRIPTION_TABLE_JSON}}"] = json.dumps(B2.cg_transcription(ctx), ensure_ascii=False, indent=1)
    sub["{{MATRIX_ECHO_TABLE_JSON}}"] = json.dumps(B2.matrix_table(ctx), ensure_ascii=False, indent=1)
    user = template
    for k, v in sub.items():
        user = user.replace(k, v)
    assert not re.findall(r"\{\{[A-Z_0-9]+\}\}", user), re.findall(r"\{\{[A-Z_0-9]+\}\}", user)[:4]
    ctx.update(identity_echo=ie, coordination_block_texts=blocks,
               user_message_sha256=sha(user.encode()), release_contract=envelope,
               release_decision=decision, c_confirmed=decision["confirmed_target_rate"],
               policy="A", eligibility={"policy_A": high},
               schema=schema, scope_rows=payload["validation_context"]["scope_rows"],
               evidence_ids=payload["validation_context"]["evidence_ids"],
               gold_ref_ids=payload["validation_context"]["gold_ref_ids"],
               scope_row_ref_ids=payload["validation_context"]["scope_row_ref_ids"],
               predef_by_id=payload["validation_context"].get("predef_by_id", {}),
               d2_deviation_cap=(int(re.match(r"\[1,(\d+)\]", bb["D2_chemical_range"]).group(1))
                                 if re.match(r"\[1,\d+\]", bb["D2_chemical_range"]) else 4),
               d2_nine_ten_evidence_ok=False,
               draft_status="READY_FOR_RELEASE_REVIEW")
    del ctx["_align_rows"]
    artifact = {"artifact_kind": "RELEASE_MESSAGES_NOT_SENT_YET", "release_id": VERSION,
                "live_runner": False,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "schema_sha256": sha(SCHEMA_PATH.read_bytes())}
    request = {"model": "FROM_CONFIRMED_RUN_CONFIG", "messages": artifact["messages"],
               "parameters_source": "config/RUN_CONFIG_DRAFT.json (values become frozen only via user confirmation)",
               "response_format": {"type": "json_object"}, "temperature": 0,
               "max_tokens": 65536, "stream": True, "enable_search": False,
               "stream_options": {"include_usage": True}}
    return request, ctx, artifact, decision


def main(argv):
    mode = argv[0] if argv else "calibration"
    outdir_override = argv[1] if len(argv) > 1 else None
    rules = load(OUT / "SCORE_RULES_RELEASE.json")
    schema = load(SCHEMA_PATH)
    template = (OUT / "prompt/USER_TEMPLATE_RELEASE.txt").read_text()
    system = (OUT / "prompt/SYSTEM_PROMPT_RELEASE.txt").read_text()
    tables = load_tables()
    route, align, sec, acc, base, scope, qa, mapping, traits = tables
    import f2r12_item_builder as LEG
    _, idx = LEG.load_b480_index()
    if mode == "calibration":
        calib_models = ["ZHIPU_GLM53_MAX_128K_JSON_OBJECT_CORRECTED", "deepseek-v4.1-flash",
                        "kimi/kimi-k3", "qwen3.8-max"]
        ident = rows(RUN_ROOT / "LIKERT_V05_REVISION_20261105/P0_INPUT_BINDING/B480_IDENTITY.tsv")
        by_cm = {(r["case_id"], r["tested_model_config_id"]): r["b_slot_uid"] for r in ident}
        slots = [by_cm[(c, m)] for c in CALIB_CASES for m in calib_models]
        assert len(slots) == 32 and len(set(slots)) == 32
    else:
        slots = sorted(s for s in idx if s not in QUARANTINE_SLOTS and idx[s]["engineering_class"] == "USABLE")
        assert len(slots) == 472
    outdir = Path(outdir_override) if outdir_override else OUT / ("requests/calibration32" if mode == "calibration" else "requests/full")
    outdir.mkdir(parents=True, exist_ok=True)
    order_map = {}
    results = []
    for i, slot in enumerate(sorted(slots)):
        anon = ("F4I-9%03d" % i) if mode == "calibration" else ("F4I-8%03d" % i)
        if anon in order_map and order_map[anon] != slot:
            raise SystemExit("anon collision")
        order_map[anon] = slot
        request, ctx, artifact, decision = render_slot(slot, anon, tables, rules, schema, template, system)
        (outdir / ("REQ_%s.json" % slot)).write_text(json.dumps(request, ensure_ascii=False, indent=1), encoding="utf-8")
        ctx_pub = {k: v for k, v in ctx.items() if k != "schema"}
        (outdir / ("CTX_%s.json" % slot)).write_text(json.dumps(ctx_pub, ensure_ascii=False, indent=1), encoding="utf-8")
        (outdir / ("ART_%s.json" % slot)).write_text(json.dumps(artifact, ensure_ascii=False, indent=1), encoding="utf-8")
        results.append({"b_slot_uid": slot, "case_id": ctx["case_id"], "anonymous_item_id": anon,
                        "user_message_sha256": ctx["user_message_sha256"],
                        "answer_sha256": ctx["identity_echo"]["answer_sha256"],
                        "score_status": decision["score_status"],
                        "allowed_range": decision["allowed_range"],
                        "high_tier_eligible": decision["high_tier_eligible"],
                        "key_cap": decision["confirmed_key_failure_cap"],
                        "route_status": ctx["route_status"],
                        "current_path_id": ctx["release_contract"]["consumer_identity"]["current_path_id"]})
    cols = ["b_slot_uid", "case_id", "anonymous_item_id", "user_message_sha256", "answer_sha256",
            "score_status", "allowed_range", "high_tier_eligible", "key_cap", "route_status",
            "current_path_id"]
    lines = ["\t".join(cols)]
    for r in results:
        vals = [r["b_slot_uid"], r["case_id"], r["anonymous_item_id"], r["user_message_sha256"],
                r["answer_sha256"], r["score_status"], json.dumps(r["allowed_range"]),
                str(r["high_tier_eligible"]), str(r["key_cap"]), r["route_status"],
                str(r["current_path_id"])]
        lines.append("\t".join(vals))
    (outdir / "RENDER_RESULTS.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"mode": mode, "rendered": len(results),
                      "outdir": str(outdir.relative_to(OUT.parent))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
