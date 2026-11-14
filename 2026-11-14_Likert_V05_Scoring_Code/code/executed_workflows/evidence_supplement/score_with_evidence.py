"""One targeted scoring round for the 24 remaining evidence-gap dimensions.

Same rubric/judge/totals; evaluator-side supplements are frozen separately.
No answer generation, no wholesale rescoring, no automatic paid retries.
"""
import copy
import csv
import fcntl
import hashlib
import json
import os
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
CLOSE=HERE.parent
S8=CLOSE.parent
sys.path[:0]=[str(S8/'execution'),str(CLOSE),str(HERE)]
import s8_scope_r1_run as RUN
import recover_format as REC
from f2r12_common import totals_contract
N=REC.N
SUPP=HERE/'EVIDENCE_SUPPLEMENT.json'
OUT=HERE/'targeted_scoring'
IO=threading.RLock()


def normalize_response(raw,req):
    obj,view,changes=REC.normalize(raw,req)
    system=req['body']['messages'][0]['content']
    known=set(re.findall(r'\[P(\d+)\]',system))
    aliases={}
    for value in obj.get('dimensions',{}).values():
        for rid in value.get('rule_ids_cited')or[]:
            m=re.fullmatch(r'P(\d+)[-–]P?(\d+)',rid)
            if m and int(m[1])<=int(m[2]) and all(str(n)in known for n in range(int(m[1]),int(m[2])+1)):
                aliases[rid]='exact contiguous range of actual supplied paragraphs'
    if aliases:
        view['body']['messages'][0]['content']+='\nExisting paragraph range aliases:\n'+N.canonical(aliases)
        changes.append(dict(action='recognize_real_paragraph_range_without_rewriting_citation',aliases=aliases))
    return obj,view,changes


def build(slot,wanted):
    ctx,art,cp,ap=N.item_for(slot)
    assert all(N.dimensions(N.source_records()[slot])[d]['score_status']=='NE'for d in wanted)
    if set(wanted)<=set(['D1','D2','D3a']):
        req=RUN.SC.build(slot,wanted)
    else:
        kept=[(n,b if n in['QUESTION','ANSWER']else b.replace(slot,ctx['anonymous_item_id']))
              for n,b in N.sections(art['messages'][1]['content'])
              if n not in['BASE_RANGES','RELEASE_CONTRACT','SCORING_FLOW_FIX']and'SCHEMA'not in n and'OUTPUT'not in n]
        decision=ctx['release_contract']['d3a_release_decision']
        program=dict(allowed_ranges=N.ranges_for(ctx,wanted),d3a_decision_status=decision['score_status'],
                     confirmed_key_failure_cap=decision.get('confirmed_key_failure_cap'),
                     source_route_status=ctx['route_status'],
                     scope_note='Use existing task and reference for this dimension only; do not apply another dimension cap.')
        sysmsg=N.rubric()+'\n'+N.OUTPUT
        user='\n'.join(f'===SECTION:{n}_BEGIN===\n{b}\n===SECTION:{n}_END==='for n,b in kept)
        user+='\n===CURRENT_PROGRAM_JUDGEMENT===\n'+N.canonical(program)
        ident=dict(repair_version='S8_TARGETED_EVIDENCE_20261114',repair_item_id=ctx['anonymous_item_id'],
            anonymous_item_id=ctx['anonymous_item_id'],case_id=ctx['case_id'],batch=ctx['batch'],
            answer_sha256=ctx['identity_echo']['answer_sha256'],requested_dimensions=wanted,
            source_context_sha256=N.file_sha(cp),source_artifact_sha256=N.file_sha(ap))
        req=dict(slot=slot,wanted=wanted,program=program,identity=ident,
            body=dict(model=N.MODEL,messages=[dict(role='system',content=sysmsg),dict(role='user',content=user)],
                temperature=0,stream=True,max_tokens=65536,enable_thinking=True,
                response_format={'type':'json_object'},stream_options={'include_usage':True},enable_search=False))
    supplement=N.load(SUPP)
    ids=supplement['slot_evidence'][slot]
    records=[supplement['records'][rid]for rid in ids]
    user=req['body']['messages'][1]['content'].split('\n===REPAIR_IDENTITY===\n')[0]
    oldcat=next(b for n,b in N.sections(user)if n=='REFERENCE_CATALOG')
    m=re.search(r'\{.*\}',oldcat,re.S);cat=json.loads(m[0])
    cat['E0_EVIDENCE']=list(dict.fromkeys(cat.get('E0_EVIDENCE',[])+ids))
    newcat=oldcat[:m.start()]+N.canonical(cat)+oldcat[m.end():]
    user=user.replace('===SECTION:REFERENCE_CATALOG_BEGIN===\n'+oldcat+'\n===SECTION:REFERENCE_CATALOG_END===',
                      '===SECTION:REFERENCE_CATALOG_BEGIN===\n'+newcat+'\n===SECTION:REFERENCE_CATALOG_END===',1)
    user+='\n===SECTION:EVALUATOR_SUPPLEMENT_BEGIN===\n'+N.canonical(records)+'\n===SECTION:EVALUATOR_SUPPLEMENT_END==='
    user+='\n以上补充仅用于评价冻结原答案，原E0缺记录说明不再代表这些新增记录也不存在。按现有量表判断对应维度，引用使用SUPP精确ID；别名/转移条目要读实际条目。身份记录不自动证明全路径或全部性状；培养温度不是最适温度。新命名按历史别名核对，不因更名扣分。补证不是模型原来提供的来源，不能回填模型的证据交付。不增加accepted集合，不把搜索无结果当错，也不研究替代方案。确实仍缺关键事实才保留NE并指出具体缺口。\n'
    ident=copy.deepcopy(req['identity']);ident.pop('repair_identity_sha256',None)
    ident.update(repair_version='S8_TARGETED_EVIDENCE_20261114',
        evaluator_supplement_sha256=N.file_sha(SUPP),
        rubric_sha256=hashlib.sha256(req['body']['messages'][0]['content'].encode()).hexdigest(),
        program_and_materials_sha256=hashlib.sha256(user.encode()).hexdigest())
    ident['repair_identity_sha256']=N.digest(ident)
    req['body']['messages'][1]['content']=user+'\n===REPAIR_IDENTITY===\n'+N.canonical(ident)
    req.update(identity=ident,body_sha256=N.digest(req['body']))
    return req


def export():
    finals={x['slot']:x for x in map(json.loads,(CLOSE/'FINAL_RATINGS_REVIEWED.jsonl').read_text().splitlines())}
    single=HERE/'single_0162/RECOVERY_RESULT.json'
    overlays=[]
    if single.exists()and N.load(single).get('status')=='OK':overlays.append(N.load(single))
    overlays += [N.load(p)for p in sorted((OUT/'adopted').glob('*.json'))]
    for result in overlays:
        uid=result['slot'];obj=result['response']
        for d,v in obj['dimensions'].items():
            assert finals[uid]['dimensions'][d]['score_status']=='NE'
            finals[uid]['dimensions'][d]=copy.deepcopy(v)
            finals[uid]['per_dimension_provenance'][d]=dict(source=result['transfer_id'],
                request_sha256=result['actual_request_sha256'],raw_response_sha256=result['raw_response_sha256'],
                evaluator_supplement_sha256=result.get('evaluator_supplement_sha256'))
        finals[uid]['kind']='S8_TARGETED_REMAINDER_RECOVERY'
    states={d:{}for d in N.DIMS};comparable=0;residual=[]
    with(OUT/'FINAL_RATINGS.jsonl').open('w')as f,(OUT/'FINAL_SCORES.tsv').open('w')as table:
        fields=['slot','total_status','weighted_total']+[d+'_'+k for d in N.DIMS for k in ['status','score']]
        wr=csv.DictWriter(table,fieldnames=fields,delimiter='\t',lineterminator='\n');wr.writeheader()
        for uid,r in sorted(finals.items()):
            r['totals']=totals_contract(r['dimensions']);t=r['totals'];comparable+=t['status']=='COMPARABLE'
            row=dict(slot=uid,total_status=t['status'],weighted_total=t['weighted_total'])
            for d,v in r['dimensions'].items():
                st=v['score_status'];states[d][st]=states[d].get(st,0)+1
                row[d+'_status']=st;row[d+'_score']=v.get('score')
                if st=='NE':residual.append(dict(slot=uid,dimension=d,basis=v.get('ne_basis'),unverified=v.get('ne_unverified')))
            wr.writerow(row);f.write(json.dumps(r,ensure_ascii=False)+'\n')
    ledger=N.load(RUN.LEDGER/'BUDGET_STATE.json')
    report=dict(positions=len(finals),comparable=comparable,not_comparable=len(finals)-comparable,
        adopted_requests=len(overlays),residual_NE_dimensions=len(residual),dimension_counts=states,
        residual=residual,attempts=ledger['attempts_used'],historical_price_estimate_cny=ledger['committed_spend_cny'],
        unknown_reserves=len(ledger['unknown_reserves']),inflight=len(ledger['inflight']),updated=RUN.utc_now_iso())
    (OUT/'PROGRESS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report


def prepare():
    supplement=N.load(SUPP)
    manifest=[]
    for uid,wanted in supplement['slot_dimensions'].items():
        req=build(uid,wanted);ctx,art,_,_=N.item_for(uid)
        assert req['body']['messages'][0]['content']==N.rubric()+'\n'+N.OUTPUT
        oldblocks=dict(N.sections(art['messages'][1]['content']));newblocks=dict(N.sections(req['body']['messages'][1]['content']))
        assert all(oldblocks[k]==newblocks[k]for k in ['QUESTION','ANSWER','GOLD_SLICE','ACCEPTED_SETS'])
        manifest.append(dict(slot=uid,wanted=wanted,request_sha256=req['body_sha256']))
    assert len(manifest)==18 and sum(len(x['wanted'])for x in manifest)==24
    OUT.mkdir(exist_ok=True);(OUT/'adopted').mkdir(exist_ok=True)
    (OUT/'REQUEST_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(offline_prepared=18,dimensions=24,model=N.MODEL,rubric_unchanged=True,answers_and_gold_unchanged=True),ensure_ascii=False))
    return manifest


def main():
    if sys.argv[-1]=='prepare':prepare();return
    if sys.argv[-1]=='export':print(json.dumps({k:v for k,v in export().items()if k not in ['residual','dimension_counts']}));return
    lock=open(RUN.S6/'work/LOCK','a+')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    manifest=N.load(OUT/'REQUEST_MANIFEST.json')
    RUN.OUT=OUT;RUN.PREFIX='S8R3_EVIDENCE_20261114'
    original_record=RUN._record
    def locked_record(record):
        with IO:original_record(record)
    RUN._record=locked_record
    state=N.load(RUN.LEDGER/'BUDGET_STATE.json');assert not state['inflight']
    ledger=RUN.BudgetLedger(str(RUN.LEDGER),1000,1200,2.0,max_transfers_per_target=20)
    creds=RUN.CRE.load_credentials(expected_model=N.MODEL);cfg=N.load(RUN.S6/'input/config/RUN_CONFIG_LIVE.json')
    for c in creds:c['endpoint']=c['endpoint']or cfg['scoring_ai']['recommended']['endpoint']
    archive=RUN.AttemptArchive(str(OUT/'work/attempts'));secrets=[c['key']for c in creds];bad=set()
    def job(row):
        uid=row['slot'];wanted=row['wanted']
        known=N.load(RUN.LEDGER/'BUDGET_STATE.json')
        prefix=RUN.PREFIX+'#'+uid+'#'
        if any(isinstance(t,str)and t.startswith(prefix)for t in known['settlements'])or any(t.startswith(prefix)for t in known['unknown_reserves']):
            return
        req=build(uid,wanted);assert req['body_sha256']==row['request_sha256']
        transports={c['alias']:RUN.LiveTransport(c['endpoint'],c['key'],session=None,stream=True)for c in creds}
        RUN.attempt_slot(uid,wanted,req,row,creds,transports,ledger,archive,secrets,bad)
        try:
            with IO:
                records=[json.loads(x)for x in(OUT/'RESULTS.jsonl').read_text().splitlines()]
            rec=next(x for x in reversed(records)if x['slot']==uid and x.get('http_status')==200)
            ad=OUT/'work/attempts'/rec['transfer_id'].replace('#','__');meta=N.load(ad/'response_meta.json')
            assert meta['stream_status']=='COMPLETE'
            assert meta.get('model_returned')in(None,N.MODEL)
            raw=json.loads(REC.parse_sse_bytes((ad/'response_raw.bin').read_bytes(),REC.new_stream_state()))
            obj,view,changes=normalize_response(raw,req);errors,reviews=N.validate(obj,view)
            result=dict(slot=uid,transfer_id=rec['transfer_id'],response=obj,errors=errors,reviews=reviews,
                normalizations=changes,actual_request_sha256=req['body_sha256'],
                raw_response_sha256=REC.sha(ad/'response_raw.bin'),evaluator_supplement_sha256=N.file_sha(SUPP),
                status='OK'if not errors else'REJECTED')
            with IO:
                if not errors:(OUT/'adopted'/f'{uid}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
                (OUT/'review').mkdir(exist_ok=True)
                (OUT/'review'/f'{uid}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
                report=export()
            RUN.log(event='MERGED',slot=uid,status=result['status'],comparable=report['comparable'],residual_NE=report['residual_NE_dimensions'])
        except Exception as exc:
            RUN.log(event='REMAINS_UNRESOLVED',slot=uid,reason=type(exc).__name__)
    # Direct identifier/reaction contradictions first; all tasks remain one
    # explicit attempt each, without a new calibration batch or extra calls.
    priority=['GPT56L__BIOPATH150_053','GPT56L__BIOPATH150_090']
    manifest.sort(key=lambda r:(priority.index(r['slot']) if r['slot']in priority else 2,r['slot']))
    with ThreadPoolExecutor(max_workers=2)as executor:list(executor.map(job,manifest))
    with IO:report=export()
    RUN.log(event='ROUND_COMPLETE',comparable=report['comparable'],residual_NE=report['residual_NE_dimensions'])


if __name__=='__main__':main()
