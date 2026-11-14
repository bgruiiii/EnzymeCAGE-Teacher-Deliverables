"""Lossless output compatibility, with all original scientific gates retained.

Never changes a score, status, rationale, evidence reference or scientific
claim. All mappings are recorded. Citation IDs are preserved verbatim.
"""
import copy
import re


def normalize_output(rating, ctx):
    out = copy.deepcopy(rating)
    changes = []
    if not isinstance(out, dict):
        return out, changes
    # A misplaced whole top-level object is recoverable only when the original
    # value exists in the wrong container and its actual destination is absent.
    top_keys = {'d5_registry','fact_verification_register','root_error_events','confidence','confidence_reason',
                'weighted_total','total_status','scientific_subscore','scientific_shortfall','review_queue',
                'best_content','most_needed_revision','route_alignment_echo','step_evidence_matrix',
                'high_tier_gate_attestation','accepted_set_binding_echo','base_range_compliance'}
    for container_name in ['dimensions','review_queue']:
        container = out.get(container_name)
        if not isinstance(container, dict):
            continue
        for key in sorted(top_keys & set(container)):
            if key == container_name or key in out:
                continue
            out[key] = container.pop(key)
            changes.append({'path':container_name+'.'+key,'action':'move_existing_object_to_top_level','destination':key})
    dr = out.get('d5_registry') or {}
    if isinstance(dr, dict):
        for i, row in enumerate(dr.get('claim_groups') or []):
            if not isinstance(row,dict):
                continue
            if 'condition_note' in row and row['condition_note'] is None:
                row.pop('condition_note')
                changes.append({'path':f'd5_registry.claim_groups[{i}].condition_note',
                                'action':'remove_null_extra_field'})
            code = row.get('claim_group')
            if not isinstance(code,str) or not re.match(r'^CG\d{2}(?:$|_)', code):
                continue
            gid=code[:4]
            predef = (ctx.get('predef_by_id') or {}).get(gid)
            if not isinstance(predef,dict):
                continue
            scope = next((x for x in ctx.get('scope_rows') or [] if x['claim_group'][:4]==gid), None)
            name = scope['claim_group'] if scope else predef.get('name')
            variants={gid}
            for variant in [name,predef.get('name')]:
                if variant:
                    variants.add(variant.split('（',1)[0])
            if name and code in variants and code!=name:
                row['claim_group'] = name
                changes.append({'path':f'd5_registry.claim_groups[{i}].claim_group','action':'unique_frozen_group_alias','from':code,'to':name})
    for dim, obj in (out.get('dimensions') or {}).items():
        if dim not in ['D1','D2','D3a','D3b','D4','D5','D6'] or not isinstance(obj,dict):
            continue
        for alias in ['root_event_ids','root_error_events']:
            value = obj.get(alias)
            if alias in obj and isinstance(value,list) and all(isinstance(x,str)for x in value):
                if 'root_error_event_ids' not in obj:
                    obj['root_error_event_ids'] = obj.pop(alias)
                    changes.append({'path':f'dimensions.{dim}.{alias}','action':'unambiguous_field_alias','to':'root_error_event_ids'})
                elif value == obj['root_error_event_ids']:
                    obj.pop(alias)
                    changes.append({'path':f'dimensions.{dim}.{alias}','action':'remove_exact_duplicate_alias'})
        # Preserve already supplied pending-claim explanations, merely echoing
        # the same model text in the redundant paired fields required by legacy.
        pending=obj.get('unverified_subclaims') or []
        if dim=='D3a' and obj.get('score_status')=='SCORED' and pending and all(
                isinstance(x,dict) and all(x.get(k) for k in ['claim','reason_unverified','why_dim_still_scorable'])
                for x in pending):
            for field, value in [
                ('ne_basis','; '.join(x['why_dim_still_scorable'] for x in pending)),
                ('ne_unverified','; '.join(x['claim']+': '+x['reason_unverified'] for x in pending))]:
                if not obj.get(field):
                    obj[field]=value
                    changes.append({'path':f'dimensions.{dim}.{field}','action':'echo_existing_pending_claim_text','source':'unverified_subclaims'})
        for i, sub in enumerate(obj.get('unverified_subclaims') or []):
            if not isinstance(sub,dict):
                continue
            for key in ['ne_basis','ne_unverified']:
                if key in sub and sub[key] is None:
                    sub.pop(key)
                    changes.append({'path':f'dimensions.{dim}.unverified_subclaims[{i}].{key}','action':'remove_null_extra_field'})
        if obj.get('score_status')=='NE' and obj.get('route_gate_effect')=='HELD_PENDING_REPRESENTATION_REVIEW':
            obj['route_gate_effect']='HELD_BOUNDARY'
            changes.append({'path':f'dimensions.{dim}.route_gate_effect','action':'existing_enum_alias','from':'HELD_PENDING_REPRESENTATION_REVIEW','to':'HELD_BOUNDARY'})
    if isinstance(out.get('dimensions'),dict) and out['dimensions'].get('D5ALT',False) is None:
        out['dimensions'].pop('D5ALT')
        changes.append({'path':'dimensions.D5ALT','action':'remove_null_extra_field'})
    for i, rec in enumerate(out.get('fact_verification_register') or []):
        if not isinstance(rec,dict):
            continue
        if rec.get('claim_links')==[]:
            rec.pop('claim_links')
            changes.append({'path':f'fact_verification_register[{i}].claim_links','action':'remove_empty_extra_field'})
        if 'note' in rec and rec['note'] is None:
            rec['note']=''
            changes.append({'path':f'fact_verification_register[{i}].note','action':'null_optional_note_to_empty_string'})
    # Duplicated nested top-level fields are harmless only if values are equal.
    for container_name in ['dimensions','review_queue']:
        container=out.get(container_name)
        if isinstance(container,dict):
            for key in list(top_keys & set(container)):
                if key!=container_name and key in out and container[key]==out[key]:
                    container.pop(key)
                    changes.append({'path':container_name+'.'+key,'action':'remove_exact_duplicate_top_level_object'})
    # The actual wire and intrinsic answer/question identities bind the return.
    # Redundant diagnostic hashes may be copied back from that same request;
    # never repair an answer, question, rubric or principal item identity.
    echo=out.get('input_identity_echo')
    expected=ctx.get('identity_echo') or {}
    # A single deleted character in the redundant template-hash echo is
    # recoverable only when every other identity hash and principal ID match.
    # Never repair answer/question hashes or substitute an unrelated template.
    if isinstance(echo,dict):
        key='item_template_sha256'
        got,want=echo.get(key),expected.get(key)
        if (isinstance(got,str) and isinstance(want,str) and len(got)==63 and len(want)==64
                and re.fullmatch('[0-9a-f]{63}',got)
                and any(want[:i]+want[i+1:]==got for i in range(64))
                and all(echo.get(k)==v for k,v in expected.items() if k!=key)
                and all(out.get(k)==ctx.get(k) for k in ['case_id','anonymous_item_id','batch'])):
            echo[key]=want
            changes.append({'path':'input_identity_echo.'+key,
                            'action':'restore_single_deleted_char_in_redundant_template_echo',
                            'from':got,'to':want})
    intrinsic=['answer_sha256','question_rendered_prompt_sha256','rubric_text_sha256',
               'system_prompt_sha256','item_template_sha256']
    if (isinstance(echo,dict) and all(echo.get(k)==expected.get(k) for k in intrinsic)
            and all(out.get(k)==ctx.get(k) for k in ['case_id','anonymous_item_id','batch'])):
        for key in ['base_ranges_sha256','evidence_case_slice_sha256']:
            if expected.get(key) and echo.get(key)!=expected[key]:
                before=echo.get(key);echo[key]=expected[key]
                changes.append({'path':'input_identity_echo.'+key,'action':'copy_non_scientific_echo_from_bound_request',
                                'from':before,'to':expected[key]})
    return out, changes


def compatible_schema(schema, artifact):
    """Allow R2-103 ONLY if actual supplied rubric contains P103. No ID rewrite."""
    copied = copy.deepcopy(schema)
    supplied = '\n'.join(m['content'] for m in artifact['messages'] if m['role']=='system')
    paragraphs = sorted(set(re.findall(r'\[P(\d{3})\]',supplied)),key=int)
    cited_pattern = copied['definitions']['dimension']['properties']['rule_ids_cited']['items']
    other_ids=sorted(set(re.findall(r'(?<![A-Z0-9-])(F\d{2}[A-Z]-\d{2})(?![A-Z0-9-])',supplied)))
    if paragraphs or other_ids:
        original = cited_pattern['pattern']
        assert original.endswith(')$')
        extra=(['R2-(?:'+'|'.join(paragraphs)+')'] if paragraphs else [])+[re.escape(x) for x in other_ids]
        cited_pattern['pattern'] = original[:-2]+'|'+'|'.join(extra)+')$'
    return copied, ['R2-'+p for p in paragraphs]+other_ids


def apply_existing_program_caps(rating,ctx):
    """Existing numeric ceilings, separately logged; never a format repair."""
    changes=[]
    dims=rating.get('dimensions') or {}
    decision=(ctx.get('release_contract') or {}).get('d3a_release_decision') or {}
    for dim,obj in dims.items():
        if not isinstance(obj,dict) or obj.get('score_status')!='SCORED' or type(obj.get('score'))is not int:
            continue
        maximum=None;reason=None
        if dim=='D1' and (ctx.get('route_status')=='DEVIATES' or ctx.get('task_conformance_status')=='VIOLATED'):
            maximum,reason=4,'existing task-deviation D1 ceiling'
        if dim=='D2':
            if ctx.get('route_status')=='DEVIATES':
                maximum,reason=ctx.get('d2_deviation_cap',4),'existing deviation-specific D2 ceiling'
            if not ctx.get('d2_nine_ten_evidence_ok',False) and (maximum is None or maximum>8):
                maximum,reason=8,'existing D2 9–10 evidence gate is not met'
        if dim=='D3a' and decision.get('confirmed_key_failure_cap') is not None:
            maximum,reason=decision['confirmed_key_failure_cap'],'existing source-bound confirmed KEY failure ceiling'
        if maximum is not None and obj['score']>maximum:
            before=obj['score'];obj['score']=maximum
            changes.append({'dimension':dim,'raw_model_score':before,'effective_score':maximum,
                            'action':'PROGRAM_CAP_DERIVATIVE','basis':reason})
    if changes:
        from f2r12_common import totals_contract
        total=totals_contract(dims)
        rating['weighted_total']=total['weighted_total'] if total['status']=='COMPARABLE' else 'NOT_COMPARABLE'
        rating['scientific_subscore']=total['scientific_subscore'] if total['status']=='COMPARABLE' else 'NOT_COMPARABLE'
        rating['total_status']=total['status']
        sf=rating.get('scientific_shortfall')
        if isinstance(sf,dict):
            sf['dims']=sorted(d for d in ['D2','D3a','D3b','D4'] if
                              (dims.get(d)or{}).get('score_status') in ['SCORED','MISSING'] and
                              type((dims.get(d)or{}).get('score'))is int and dims[d]['score']<5)
            sf['flag']=bool(sf['dims'])
    return changes


def validate_compatible(rating, item, schema, original_validate, apply_caps=False):
    normalized, changes = normalize_output(rating,item['ctx'])
    caps=apply_existing_program_caps(normalized,item['ctx']) if apply_caps else []
    effective_schema, allowed_three_digit_ids = compatible_schema(schema,item['artifact'])
    result = original_validate(normalized,item,effective_schema)
    # The old soft flag's regex predates the schema; suppress only a supplied,
    # exact existing paragraph citation that is now legally accepted.
    result.review_flags = [flag for flag in result.review_flags if not (
        flag.get('gate')=='V05-S5' and any(flag.get('message','').endswith('未知规则ID：'+rid) for rid in allowed_three_digit_ids))]
    if changes or allowed_three_digit_ids:
        result.projection = dict(result.projection)
        result.projection['output_format_compatibility'] = {
            'normalizations':changes,'existing_three_digit_paragraph_ids_accepted':allowed_three_digit_ids,
            'scores_statuses_rationales_and_evidence_refs_unchanged':not bool(caps)}
    if caps:
        result.projection=dict(result.projection)
        result.projection['program_score_caps']=caps
    return result, normalized, changes
