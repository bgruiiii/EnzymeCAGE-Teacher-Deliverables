"""Portable I/O adapter; score validation and totals come from actual run code.

Inputs must already bind the task/reference facts. This module never claims
to infer scientific truth from a raw answer, or to replace expert review.
"""
import copy
import json
from .common import ROOT,DIMS,MODEL,canonical,digest,totals_contract
from .validation import validate,normalize_response


def prepare(item,requested=None):
    wanted=requested or list(DIMS)
    if not wanted or len(set(wanted))!=len(wanted) or not set(wanted)<=set(DIMS):raise ValueError('invalid requested dimensions')
    for k in ['item_id','case_id','anonymous_item_id','batch','question_text','answer_text','program','materials','reference_catalog']:
        if k not in item:raise ValueError('missing prepared-item field: '+k)
    if any(k in item for k in ['old_scores','model_ranking','old_rationale']):raise ValueError('old scores/rankings are not scoring input')
    program=copy.deepcopy(item['program'])
    if set(wanted)-set(program.get('allowed_ranges',{})):raise ValueError('explicit program range required for each requested dimension')
    if 'd3a_decision_status'not in program:raise ValueError('frozen D3a decision required')
    if 'D3a'in wanted:
        cap=program.get('confirmed_key_failure_cap')
        if cap is not None:
            lo,hi=program['allowed_ranges']['D3a']
            program['allowed_ranges']['D3a']=[lo,min(hi,cap)]
    for d in wanted:
        r=program['allowed_ranges'][d]
        if not isinstance(r,list)or len(r)!=2 or not all(type(x)is int for x in r)or not 1<=r[0]<=r[1]<=10:
            raise ValueError('invalid frozen score range: '+d)
    if item['materials'].get('MAIN_CHAIN_SCOPE'):
        program['main_chain_scope']=item['materials']['MAIN_CHAIN_SCOPE']
    system=(ROOT/'rubric/SYSTEM_RUBRIC_USED_S8.txt').read_text(encoding='utf-8')+'\n'+(ROOT/'schemas/PARTIAL_OUTPUT_INSTRUCTIONS.txt').read_text(encoding='utf-8')
    material={'QUESTION':item['question_text'],'ANSWER':item['answer_text']}
    material.update(copy.deepcopy(item['materials']))
    if 'BASE_RANGES'in material or 'RELEASE_CONTRACT'in material:raise ValueError('do not reintroduce obsolete all-graph/automatic-NE envelopes')
    material['REFERENCE_CATALOG']=item['reference_catalog']
    user='\n'.join(f'===SECTION:{k}_BEGIN===\n'+(v if isinstance(v,str)else canonical(v))+f'\n===SECTION:{k}_END==='for k,v in material.items())
    user+='\n===CURRENT_PROGRAM_JUDGEMENT===\n'+canonical(program)
    identity=dict(repair_version='LIKERT_V05_CODE_EXPORT_20261114',repair_item_id=item['item_id'],
        anonymous_item_id=item['anonymous_item_id'],case_id=item['case_id'],batch=item['batch'],
        answer_sha256=__import__('hashlib').sha256(item['answer_text'].encode()).hexdigest(),
        requested_dimensions=wanted,program_and_materials_sha256=__import__('hashlib').sha256(user.encode()).hexdigest(),
        rubric_sha256=__import__('hashlib').sha256(system.encode()).hexdigest())
    identity['repair_identity_sha256']=digest(identity)
    user+='\n===REPAIR_IDENTITY===\n'+canonical(identity)
    body=dict(model=MODEL,messages=[dict(role='system',content=system),dict(role='user',content=user)],
        temperature=0,stream=True,max_tokens=65536,enable_thinking=True,
        response_format={'type':'json_object'},stream_options={'include_usage':True},enable_search=False)
    return dict(slot=item['item_id'],wanted=wanted,identity=identity,program=program,body=body,
                body_sha256=digest(body),synthetic=bool(item.get('synthetic')))


def validate_return(response,request):
    normalized,view,changes=normalize_response(response,request)
    errors,reviews=validate(normalized,view)
    return dict(valid=not errors,errors=errors,reviews=reviews,
                normalized_response=normalized,normalizations=changes,
                actual_request_sha256=request['body_sha256'])


def merge(response,request,baseline=None):
    result=validate_return(response,request)
    if not result['valid']:raise ValueError(result['errors'])
    rated=result['normalized_response']['dimensions']
    if baseline is None:
        if set(rated)!=set(DIMS):raise ValueError('partial output requires a seven-dimension baseline')
        dims=copy.deepcopy(rated)
    else:
        dims=copy.deepcopy(baseline['dimensions'])
        for d in request['wanted']:
            if dims[d]['score_status']!='NE':raise ValueError('repair cannot overwrite previously numerical/MISSING dimension: '+d)
            dims[d]=copy.deepcopy(rated[d])
        assert all(dims[d]==baseline['dimensions'][d]for d in DIMS if d not in request['wanted'])
    return dict(item_id=request['slot'],dimensions=dims,totals=totals_contract(dims),
                replaced_dimensions=request['wanted'],source_request_sha256=request['body_sha256'],
                review_flags=result['reviews'],normalizations=result['normalizations'],
                human_external_validity='PENDING_NOT_REPLACED_BY_AI')
