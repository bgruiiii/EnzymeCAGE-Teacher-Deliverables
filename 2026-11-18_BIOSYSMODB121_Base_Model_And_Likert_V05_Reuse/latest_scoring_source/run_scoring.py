"""One paid request per new approved-scope answer; two workers, one ledger."""
import copy
import csv
import fcntl
import hashlib
import io
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
W=HERE.parent
S9=W/'S9_121X6_COVERAGE_COMPLETION_20261115'
sys.path.insert(0,str(S9))
import score_readable_failure as E
N,RC,RUN=E.N,E.RC,E.RUN
PREFIX='S12_APPROVED_SCOPE_20261115'
LOCK=threading.RLock()
STOP=threading.Event()


def log(**values):
    with LOCK:print(json.dumps(values,ensure_ascii=False),flush=True)


def targets():
    with(HERE/'TARGETS_12.tsv').open()as f:return list(csv.DictReader(f,delimiter='\t'))


def build(row):
    case=row['case_id'];ref=HERE/'references'/case
    manifest=N.load(ref/'MANIFEST.json');assert manifest['decision']['actor']=='USER'
    data=Path(row['answer_path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['answer_sha256']
    answer=json.loads(data)
    scope=RC.load_scope(str(ref/'CASE_TASK_SCOPE.tsv'))[case]
    gold=RC.load_gold_steps(str(ref/'reaction_gold.tsv'))
    facts=RC.align_case(scope,gold[case],answer,frozenset(),RC.build_cross_route_index(gold),case_id=case)
    profile_names={str(x.get('organism_name')or'').strip().lower()for x in answer.get('organism_profiles',[])}
    sections=[];ids=[]
    for f in manifest['files']:
        p=ref/f['file'];assert N.file_sha(p)==f['sha256']
        with p.open()as h:
            rd=csv.DictReader(h,delimiter='\t');fields=rd.fieldnames;rs=list(rd)
        if f['file'].startswith('trait_'):
            rs=[x for x in rs if x.get('organism_name','').strip().lower()in profile_names]
        buff=io.StringIO();wr=csv.DictWriter(buff,fields,delimiter='\t',lineterminator='\n');wr.writeheader();wr.writerows(rs)
        sections.append('--- FILE: '+f['file']+' ---\n'+buff.getvalue())
        ids += [f['file'],f['file']+'#case:'+case]
    for name in ['source_pathway_annotations.tsv','source_reaction_records.tsv','SCOPE_ROLES.tsv']:
        sections.append('--- FILE: '+name+' ---\n'+(ref/name).read_text());ids += [name,name+'#case:'+case]
    all_missing=not any(isinstance(s.get('enzyme'),dict)and(s['enzyme'].get('name')or s['enzyme'].get('ec_number'))for s in answer.get('steps',[]))
    # C06 retains independent D2 anchors. Incomplete coverage is descriptive,
    # not a new mechanical score formula. Confirmed task deviation constrains
    # D1; actual directional contradiction constrains D2 separately.
    d1=[1,4]if facts['task_conformance_status']=='VIOLATED'or facts['route_status']=='DEVIATES'else[1,6]if facts['route_status']=='INCOMPLETE'else[1,10]if facts['route_status']=='BOUNDARY_REVIEW'else[5,10]
    d2=[1,4]if facts['flipped_strict_nonrev']or facts['flipped_strict_rev']or facts['chain_reversal_confirmed']else[1,5]if facts['stereo_conflict']else[1,8]
    program=dict(allowed_ranges={d:d1 if d=='D1'else d2 if d=='D2'else([1,1]if all_missing else[1,8])if d=='D3a'else[1,10]for d in N.DIMS},
        d3a_decision_status='MISSING'if all_missing else'JUDGE_REQUIRED',confirmed_key_failure_cap=None,
        source_route_status=facts['route_status'],source_task_conformance_status=facts['task_conformance_status'],route_facts=facts,
        approved_required_reactions=manifest['required_reactions'],background_not_required=manifest['background_reactions'],
        key_roles_source='SCOPE_ROLES.tsv: existing ENTRY/TERMINAL task roles; no invented confirmed-failure proof',
        note='只读本答案事实。自动表示/EC待核不要求整维NE；不把未命中accepted自动判错。D1与D2独立。'+
             'D3a逐目标功能/酶候选按现有C03-C05阅读给定参考判断，KEY失败须有实际已核错误或遗漏定位，不代造证明。'+
             '未提供新的高档催化证明，按既有科学证据门D2/D3a上界8；不能扩展给D1/D6。')
    catalogue=dict(GOLD_SLICE=ids,SCOPE_ROW=[case],E0_EVIDENCE=[])
    user='\n'.join(f'===SECTION:{k}_BEGIN===\n{v}\n===SECTION:{k}_END==='for k,v in[
        ('QUESTION',(ref/'QUESTION.txt').read_text()),('ANSWER',data.decode()),
        ('GOLD_SLICE','\n'.join(sections)),('TASK_SCOPE',N.canonical(scope)),('REFERENCE_CATALOG',N.canonical(catalogue))])
    user+='\n===CURRENT_PROGRAM_JUDGEMENT===\n'+N.canonical(program)
    user+='\n本轮仅评价既有原答案。用户已明确确认修正范围：060必答四步至题名终点；094必答雄酮至雄烯二酮的两步，睾酮入口是背景，未答背景不扣分。'+\
          '旧三步参考的错误终点不能继续用于094；060原题名一直要求完整终点，现补齐参考末步。不给预设分数。'+\
          'source_pathway_annotations是旧路径级标签，不自动证明修正后全链能力；organism_gold的STEP是原始策展关联，按声明粒度判断。'+\
          '同物种性状行可来自冻结其他case，source_reference_case_id保留；物种代表记录不自动证明每个菌株及条件，培养温度不当最适温度。'+\
          '没有本轮逐声称外部新核验，不编核验记录；没有材料不等于已核错误。D5评价原答案来源交付，不将评分方资料回填成模型证据。'+\
          '只按既有量表出分，不研究替代方案；规则引用用实际System的C00-C08/Pxxx。\n'
    system=N.rubric()+'\n'+N.OUTPUT
    number=next(i for i,x in enumerate(targets(),1)if x['slot']==row['slot'])
    anon=f'F4I-S12-{number:04d}'
    identity=dict(repair_version=PREFIX,repair_item_id=anon,anonymous_item_id=anon,case_id=case,
        batch='S12_USER_APPROVED_SCOPE_NEW_RATINGS',answer_sha256=row['answer_sha256'],requested_dimensions=N.DIMS,
        source_artifact_sha256=N.file_sha(ref/'MANIFEST.json'),rubric_sha256=hashlib.sha256(system.encode()).hexdigest(),
        program_and_materials_sha256=hashlib.sha256(user.encode()).hexdigest())
    identity['repair_identity_sha256']=N.digest(identity)
    user+='\n===REPAIR_IDENTITY===\n'+N.canonical(identity)
    assert dict(N.sections(user))['ANSWER'].encode()==data
    assert not any(name in user for name in ['grok-4.7','gpt-5.6-luna','deepseek-v4.1-flash','kimi/kimi-k3','qwen3.8-max'])
    body=dict(model=N.MODEL,messages=[dict(role='system',content=system),dict(role='user',content=user)],
        temperature=0,stream=True,max_tokens=65536,enable_thinking=True,response_format={'type':'json_object'},
        stream_options={'include_usage':True},enable_search=False)
    return dict(slot=row['slot'],wanted=N.DIMS,program=program,identity=identity,body=body,body_sha256=N.digest(body))


def prepare():
    plan=[]
    assert N.load(HERE/'REFERENCE_CHECKS.json')['PASS']
    for row in targets():
        req=build(row);out=HERE/'scoring'/req['identity']['anonymous_item_id'];out.mkdir(parents=True,exist_ok=True)
        p=out/'REQUEST.json'
        if p.exists():assert N.load(p)==req,'bound request drift'
        else:p.write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n')
        plan.append(dict(slot=row['slot'],case_id=row['case_id'],directory=str(out),body_sha256=req['body_sha256'],
                         route_status=req['program']['source_route_status'],required=req['program']['route_facts']['n_required']))
    assert len(plan)==12 and sum(x['required']for x in plan)==36
    (HERE/'REQUEST_MANIFEST.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    log(event='PREPARED',targets=12,model=N.MODEL,paid_calls=0)
    return plan


def export():
    base={x['slot']:x for x in map(json.loads,(S9/'CURRENT_RATINGS.jsonl').read_text().splitlines())}
    finals=copy.deepcopy(base)
    with(S9/'CURRENT_SCORES_ALL_726.tsv').open()as f:rows=list(csv.DictReader(f,delimiter='\t'))
    byslot={x['slot']:x for x in rows};outcomes=Counter()
    for p in sorted((HERE/'scoring').glob('*/RESULT.json')):
        recovered=p.with_name('RECOVERED_RESULT.json')
        if recovered.exists():p=recovered
        rec=N.load(p);outcomes[rec['status']]+=1
        if rec['status']!='OK':continue
        slot=rec['slot'];assert slot not in base
        finals[slot]=rec['rating'];r=byslot[slot];t=rec['rating']['totals']
        r.update(coverage_status='SCORED_APPROVED_REFERENCE_REPAIR',total_status=t['status'],weighted_total=t['weighted_total'],
                 scientific_subscore=t['scientific_subscore'],scoring_cohort='S12_USER_APPROVED_REFERENCE_SCOPE',
                 next_action='REUSE_UNCHANGED',review_note=rec['rating']['note'],
                 supplement_request_status='OK',supplement_transfer_id=rec['transfer_id'],supplement_result_path=str(p))
        for d,v in rec['rating']['dimensions'].items():r[d+'_status']=v['score_status'];r[d+'_score']=v.get('score')
    for slot,v in base.items():assert finals[slot]==v
    with(HERE/'CURRENT_RATINGS.jsonl').open('w')as f:
        for _,v in sorted(finals.items()):f.write(json.dumps(v,ensure_ascii=False)+'\n')
    for name,selected in [('CURRENT_SCORES_ALL_726.tsv',rows),('CURRENT_UNSCORED_POSITIONS.tsv',[x for x in rows if x['slot']not in finals])]:
        with(HERE/name).open('w',newline='')as f:
            wr=csv.DictWriter(f,list(rows[0]),delimiter='\t',lineterminator='\n');wr.writeheader();wr.writerows(selected)
    led=N.load(RUN.LEDGER/'BUDGET_STATE.json')
    common=Counter(x['case_id']for x in rows if x['total_status']=='COMPARABLE')
    statuses=Counter(v['score_status']for x in finals.values()for v in x['dimensions'].values())
    report=dict(positions=726,ratings=len(finals),comparable=sum(x['total_status']=='COMPARABLE'for x in rows),
        newly_adopted=len(finals)-len(base),remaining_unscored=726-len(finals),
        common_comparable_cases=sum(v==6 for v in common.values()),dimension_statuses=dict(statuses),
        outcomes=dict(outcomes),attempts=led['attempts_used'],known_price_estimate_cny=led['committed_spend_cny'],
        unknown_reserves=len(led['unknown_reserves']),inflight=len(led['inflight']),old711_unchanged=True)
    (HERE/'PROGRESS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report


def main():
    mode=sys.argv[1]if len(sys.argv)>1 else'prepare'
    if mode=='export':log(**export());return
    plan=prepare()
    if mode!='run':return
    assert N.load(HERE/'OFFLINE_CHECKS.json')['PASS']
    lock=open(RUN.S6/'work/LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    initial=N.load(RUN.LEDGER/'BUDGET_STATE.json');assert not initial['inflight']
    snapshot=HERE/'LEDGER_BEFORE.json'
    if not snapshot.exists():snapshot.write_text(json.dumps(initial,ensure_ascii=False,indent=2)+'\n')
    ledger=RUN.BudgetLedger(str(RUN.LEDGER),1000,1200,2.0,max_transfers_per_target=20)
    credentials=RUN.CRE.load_credentials(expected_model=N.MODEL)
    cfg=N.load(RUN.S6/'input/config/RUN_CONFIG_LIVE.json')
    for c in credentials:c['endpoint']=c['endpoint']or cfg['scoring_ai']['recommended']['endpoint']
    def job(entry):
        out=Path(entry['directory']);rp=out/'RESULT.json'
        if rp.exists():
            effective=out/'RECOVERED_RESULT.json'if(out/'RECOVERED_RESULT.json').exists()else rp
            log(event='DEDUP_OR_HOLD',slot=entry['slot'],status=N.load(effective)['status']);return
        prefix=PREFIX+'#'+entry['slot']+'#'
        state=N.load(RUN.LEDGER/'BUDGET_STATE.json')
        if any(isinstance(t,str)and t.startswith(prefix)for k in ['settlements','unknown_reserves','inflight']for t in state[k]):
            log(event='PERSISTED_ATTEMPT_HOLD_NO_CALL',slot=entry['slot']);return
        if STOP.is_set():return
        req=N.load(out/'REQUEST.json');assert req['body_sha256']==entry['body_sha256']
        archive=RUN.AttemptArchive(str(out/'work/attempts'))
        for c in credentials:
            tid=prefix+'t'+str(ledger.next_transfer_seq());ledger.reserve(tid,entry['slot'],reserve_cny=2.0)
            log(event='DISPATCH',slot=entry['slot'],transfer=tid,alias=c['alias'])
            wire=RUN.LiveTransport(c['endpoint'],c['key'],session=None,stream=True).send(
                dict(endpoint=c['endpoint'],body=req['body'],item_identity=req['identity']),1800)
            archive.store(tid,wire,json.dumps(req['body'],ensure_ascii=False).encode(),req['identity'],run_identity=PREFIX,attempt_index=0)
            settle=ledger.settle_by_transport(tid,dict(usage=wire.get('usage'),http_status=wire.get('http_status'),
                response_received=wire.get('raw_response_bytes')is not None,may_have_billed=wire.get('may_have_billed',False),error_kind=wire.get('error_kind')),2.,8.)
            rec=dict(slot=entry['slot'],transfer_id=tid,alias=c['alias'],http_status=wire.get('http_status'),
                stream_status=wire.get('stream_status'),settlement=settle,request_body_sha256=req['body_sha256'],
                status='TECHNICAL_FAILURE_OR_UNKNOWN')
            if wire.get('http_status')==200 and wire.get('stream_status')=='COMPLETE':
                try:
                    if wire.get('model_returned')!=N.MODEL:
                        STOP.set();raise ValueError('MODEL_IDENTITY_MISMATCH')
                    raw=json.loads(wire['content_text']);obj,view,changes=E.normalize_for_request(raw,req)
                    errors,reviews=N.validate(obj,view)
                    rec.update(status='REJECTED'if errors else'OK',response=obj,errors=errors,reviews=reviews,normalizations=changes)
                    if not errors:
                        rec['rating']=dict(slot=entry['slot'],kind='S12_APPROVED_REFERENCE_SCOPE_NEW_RATING',dimensions=obj['dimensions'],
                            totals=E.totals_contract(obj['dimensions']),
                            per_dimension_provenance={d:dict(source=tid,answer_sha256=req['identity']['answer_sha256'],
                                request_body_sha256=req['body_sha256'],reference_manifest_sha256=req['identity']['source_artifact_sha256'])for d in N.DIMS},
                            note='用户2026-11-15明确确认060四步/094两步范围后首次评分；采用独立修正参考版本，原题与原答未改。')
                except Exception as exc:rec.update(status='RESPONSE_PARSE_OR_PROTOCOL_FAILURE',error_type=type(exc).__name__)
            rp.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
            log(event='RESULT',slot=entry['slot'],transfer=tid,status=rec['status'],errors=rec.get('errors',[]))
            with LOCK:export()
            if wire.get('http_status')!=200 and RUN.CRE.classify(wire)=='SWITCH':continue
            break
    with ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(job,plan))
    with LOCK:log(event='BATCH_COMPLETE',**export())


if __name__=='__main__':main()
