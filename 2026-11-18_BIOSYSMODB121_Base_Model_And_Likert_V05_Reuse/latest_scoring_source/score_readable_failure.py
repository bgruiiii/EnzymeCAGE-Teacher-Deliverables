"""Score the existing Grok-145 body once, retaining its schema-failure status.

Uses the executed S8 rubric, validator, transport/archive and current ledger.
Only case-shared reference blocks are reused; no other answer's facts/ranges.
"""
import csv
import fcntl
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = HERE.parent
R = W.parent
S8 = W / 'S8_NE_REVIEW_20261113'
sys.path[:0] = [str(S8 / 'execution'), str(S8), str(R / 'LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK'),
               str(S8 / 'coordinator_closeout_20261114/remaining_rescue')]
import s8_scope_r1_run as RUN
import ne_repair as N
import route_checker_r2 as RC
from score_with_evidence import normalize_response
from f2r12_common import totals_contract

SLOT = 'GRK47__BIOPATH150_145'
PREFIX = 'S9_READABLE_20261115'
OUT = HERE / 'readable_failure_145'


def normalize_for_request(raw, req):
    obj, view, changes = normalize_response(raw, req)
    blocks = dict(N.sections(req['body']['messages'][1]['content']))
    if 'TASK_SCOPE' in blocks:
        match = re.search(r'\{.*\}', blocks['TASK_SCOPE'], re.S)
        scope = json.loads(match[0]) if match else {}
        case = scope.get('case_id')
        refs = [r for v in obj.get('dimensions',{}).values() for r in v.get('evidence_refs',[])]
        if case == req['identity']['case_id'] and any(r.get('ref_type')=='SCOPE_ROW'and r.get('ref_id')==case for r in refs):
            vblocks = dict(N.sections(view['body']['messages'][1]['content']))
            cat = json.loads(re.search(r'\{.*\}', vblocks['REFERENCE_CATALOG'], re.S)[0])
            if case not in cat.get('SCOPE_ROW',[]):
                cat.setdefault('SCOPE_ROW',[]).append(case)
                old='===SECTION:REFERENCE_CATALOG_BEGIN===\n'+vblocks['REFERENCE_CATALOG']+'\n===SECTION:REFERENCE_CATALOG_END==='
                new='===SECTION:REFERENCE_CATALOG_BEGIN===\n'+N.canonical(cat)+'\n===SECTION:REFERENCE_CATALOG_END==='
                view['body']['messages'][1]['content']=view['body']['messages'][1]['content'].replace(old,new,1)
                changes.append(dict(action='recognize_exact_case_id_of_existing_supplied_TASK_SCOPE_row',
                                    ref_type='SCOPE_ROW',ref_id=case,validation_view_only=True))
    return obj, view, changes


def build():
    index = R / '04_Local_Review_Audits/FOREIGN_MODEL_COMPARISON_PREPARATION_20261111/CANDIDATE_INPUTS_MAIN6_726.tsv'
    row = next(x for x in csv.DictReader(index.open(), delimiter='\t')
               if x['model_config_id']=='grok-4.7' and x['case_id']=='BIOPATH150_145')
    data = Path(row['answer_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['answer_sha256']
    answer = json.loads(data)
    assert answer['case_id'] == 'BIOPATH150_145'
    assert answer['steps'] and all(s.get('enzyme') is None and s.get('microorganism') is None for s in answer['steps'])
    assert not answer['organism_profiles']
    # Same-case reference carrier only. All answer-specific blocks are excluded.
    _, art, _, ap = N.item_for('GPT56L__BIOPATH150_145')
    blocks = dict(N.sections(art['messages'][1]['content']))
    matches = list(re.finditer(r'--- FILE: ([^ ]+) ', blocks['GOLD_SLICE']))
    core = ['case_root_identity.tsv','enzyme_gold.tsv','formal_cases.tsv','organism_gold.tsv','reaction_gold.tsv']
    gold = blocks['GOLD_SLICE'][:matches[0].start()]
    for i, m in enumerate(matches):
        if m[1] in core:
            gold += blocks['GOLD_SLICE'][m.start():matches[i+1].start() if i+1<len(matches) else len(blocks['GOLD_SLICE'])]
    # Trait tables are irrelevant because the scored answer supplies no organism
    # profiles. They are omitted with disclosure, never represented as empty Gold.
    scope = RC.load_scope(str(R/'LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK/CASE_TASK_SCOPE_120.tsv'))['BIOPATH150_145']
    goldsteps = RC.load_gold_steps(str(R/'LIKERT_V04_FULL_SCORING_20261029/F1_PROGRAM_TABLES/work/adapter_stage/G1_gold/reaction_gold.tsv'), cases={'BIOPATH150_145'})
    facts = RC.align_case(scope, goldsteps['BIOPATH150_145'], answer, frozenset(),
                          RC.build_cross_route_index(goldsteps), case_id='BIOPATH150_145')
    assert facts['route_status']=='INCOMPLETE' and facts['missing']==7 and facts['coverage']==0
    cat = dict(GOLD_SLICE=[x for name in core for x in [name,name+'#case:BIOPATH150_145']],
               SCOPE_ROW=[], E0_EVIDENCE=[])
    program = dict(allowed_ranges={d:([1,6] if d=='D1' else [1,4] if d=='D2' else [1,1] if d=='D3a' else [1,10]) for d in N.DIMS},
                   d3a_decision_status='MISSING', confirmed_key_failure_cap=None,
                   source_route_status=facts['route_status'], route_facts=facts,
                   range_source='executed R3 INCOMPLETE D1=[1,6], cov_band(0) D2=[1,4]; C08 no enzyme MISSING=1',
                   own_answer_missing_enzyme=True, own_answer_organism_profiles_empty=True,
                   engineering_schema_failure_retained=True,
                   note='原正文不改；结构失败与科学评分分列。替代路线明确不属主链，不拿替代酶或菌算目标推荐。')
    kept = [('QUESTION',blocks['QUESTION']),('ANSWER',data.decode()),('GOLD_SLICE',gold),
            ('TASK_SCOPE',blocks['TASK_SCOPE']),('REFERENCE_CATALOG',N.canonical(cat))]
    user = '\n'.join(f'===SECTION:{k}_BEGIN===\n{v}\n===SECTION:{k}_END===' for k,v in kept)
    user += '\n===CURRENT_PROGRAM_JUDGEMENT===\n'+N.canonical(program)
    user += '\n本次评价完整原始正文，不补写模型答案。该JSON存在原采集schema不合，保留工程失败状态；但内容仍可按既有量表评分。'+ \
            '其主链产品、反应类型、酶、对应菌均未交付；不要把模型不会回答误写成评价方缺参考NE。'+ \
            '无任何organism_profiles，故不装载无关的大型性状表；这是材料裁剪，不是Gold原本为空。'+ \
            '不要联网。规则引用可直接用System实际[Pxxx]编号；不造规则编号。按各维原有条款独立打分。\n'
    system = N.rubric()+'\n'+N.OUTPUT
    ident = dict(repair_version=PREFIX, repair_item_id='F4I-S9-0145', anonymous_item_id='F4I-S9-0145',
                 case_id='BIOPATH150_145', batch='S9_EXISTING_BODY', answer_sha256=row['answer_sha256'],
                 requested_dimensions=N.DIMS, source_artifact_sha256=N.file_sha(ap),
                 rubric_sha256=hashlib.sha256(system.encode()).hexdigest(),
                 program_and_materials_sha256=hashlib.sha256(user.encode()).hexdigest())
    ident['repair_identity_sha256'] = N.digest(ident)
    user += '\n===REPAIR_IDENTITY===\n'+N.canonical(ident)
    body = dict(model=N.MODEL,messages=[dict(role='system',content=system),dict(role='user',content=user)],
                temperature=0, stream=True, max_tokens=65536, enable_thinking=True,
                response_format={'type':'json_object'}, stream_options={'include_usage':True}, enable_search=False)
    req = dict(slot=SLOT,wanted=N.DIMS,program=program,identity=ident,body=body,body_sha256=N.digest(body))
    assert dict(N.sections(user))['ANSWER'].encode()==data
    assert not any(x in user for x in ['gpt-5.6-luna','grok-4.7','GPT56L__','GRK47__'])
    assert not any(x in dict(N.sections(user)) for x in ['ROUTE_DIAGNOSIS','EVIDENCE_FIVE_STATE','BASE_RANGES','RELEASE_CONTRACT'])
    return req


def main():
    OUT.mkdir(exist_ok=True)
    req=build()
    binding=OUT/'REQUEST.json'
    if binding.exists():
        assert N.load(binding)==req, 'bound request changed'
    else:
        binding.write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n')
    if len(sys.argv)<2 or sys.argv[1]!='run':
        print(json.dumps(dict(prepared=True, model=N.MODEL,body_sha256=req['body_sha256'],
                             prompt_characters=sum(len(x['content'])for x in req['body']['messages']),paid_calls=0)))
        return
    existing=OUT/('RECOVERED_RESULT.json'if(OUT/'RECOVERED_RESULT.json').exists()else'RESULT.json')
    if existing.exists():
        known=N.load(existing)
        print(json.dumps(dict(event='DEDUP_NO_CALL'if known['status']=='OK'else'HOLD_EXISTING_ATTEMPT_NO_CALL',
                              slot=SLOT,status=known['status'])),flush=True)
        return
    lock=open(RUN.S6/'work/LOCK','a+')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    state=N.load(RUN.LEDGER/'BUDGET_STATE.json')
    prefix=PREFIX+'#'+SLOT+'#'
    keys=list(state['settlements'])+list(state['unknown_reserves'])+list(state['inflight'])
    assert not any(isinstance(t,str)and t.startswith(prefix)for t in keys), 'already attempted; offline review only'
    assert not state['inflight'], 'another inflight request exists'
    ledger=RUN.BudgetLedger(str(RUN.LEDGER),1000,1200,2.0,max_transfers_per_target=20)
    creds=RUN.CRE.load_credentials(expected_model=N.MODEL)
    cfg=N.load(RUN.S6/'input/config/RUN_CONFIG_LIVE.json')
    archive=RUN.AttemptArchive(str(OUT/'work/attempts'))
    for c in creds:
        endpoint=c['endpoint']or cfg['scoring_ai']['recommended']['endpoint']
        tid=prefix+'t'+str(ledger.next_transfer_seq())
        ledger.reserve(tid,SLOT,reserve_cny=2.0)
        print(json.dumps(dict(event='DISPATCH',slot=SLOT,transfer=tid,alias=c['alias'])),flush=True)
        wire=RUN.LiveTransport(endpoint,c['key'],session=None,stream=True).send(dict(endpoint=endpoint,body=req['body'],item_identity=req['identity']),1800)
        archive.store(tid,wire,json.dumps(req['body'],ensure_ascii=False).encode(),req['identity'],run_identity=PREFIX,attempt_index=0)
        settle=ledger.settle_by_transport(tid,dict(usage=wire.get('usage'),http_status=wire.get('http_status'),
                  response_received=wire.get('raw_response_bytes')is not None,may_have_billed=wire.get('may_have_billed',False),error_kind=wire.get('error_kind')),2.,8.)
        rec=dict(slot=SLOT,transfer_id=tid,alias=c['alias'],http_status=wire.get('http_status'),
                 stream_status=wire.get('stream_status'),settlement=settle,request_body_sha256=req['body_sha256'])
        if wire.get('http_status')==200 and wire.get('stream_status')=='COMPLETE':
            assert wire.get('model_returned') in (None,N.MODEL), 'model changed'
            raw=json.loads(wire['content_text'])
            obj,view,changes=normalize_for_request(raw,req)
            errors,reviews=N.validate(obj,view)
            rec.update(status='OK'if not errors else 'REJECTED',response=obj,errors=errors,reviews=reviews,normalizations=changes)
            if not errors:
                schema_failure=req['program'].get('engineering_schema_failure_retained',False)
                rec['rating']=dict(slot=SLOT,kind='S9_NEW_SCORE_EXISTING_SCHEMA_FAILURE'if schema_failure else'S9_CASE023_REFERENCE_INTERFACE_EXTENSION',dimensions=obj['dimensions'],
                    totals=totals_contract(obj['dimensions']),original_engineering_status='INVALID_SCHEMA_RETAINED'if schema_failure else'ORIGINAL_READY',
                    per_dimension_provenance={d:dict(source=tid,answer_sha256=req['identity']['answer_sha256'],request_body_sha256=req['body_sha256'])for d in N.DIMS},
                    note='原采集格式失败保留；只评价原有正文，没有补写答案。'if schema_failure else'接入原有023题参考材料；只评价现成正文，没有补采答案。')
        else:
            rec['status']='TECHNICAL_FAILURE_OR_UNKNOWN'
        (OUT/'RESULT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in rec.items()if k not in ['response','rating']},ensure_ascii=False),flush=True)
        if wire.get('http_status')!=200 and RUN.CRE.classify(wire)=='SWITCH':
            continue  # credential refusal only; never rotate for scored/unknown results
        break


if __name__=='__main__':
    main()
