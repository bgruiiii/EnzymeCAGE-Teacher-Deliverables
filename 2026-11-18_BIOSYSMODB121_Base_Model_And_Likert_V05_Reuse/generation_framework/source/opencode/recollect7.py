"""GPT 5.6 format recollection round R1: seven authorized second answers, one per case.
Independent ledger/lock/workspace; originals read-only; no touch on the 114 valid first answers.
Card: LOCAL_AI_GPT56_FORMAT_RECOLLECTION7_ONCE_THEN_CLOSEOUT_20261111."""
import csv
import fcntl
import json
import math
import os
import pathlib
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

W=pathlib.Path(__file__).resolve().parents[1]
R=W.parent
W2=R/'FOREIGN_NATIVE_GPT56_LUNA_FULL_REMAINING116_20261110'
REVIEW=R/'04_Local_Review_Audits/FOREIGN_NATIVE_THREE_LINE_FINAL_REVIEW_20261111'
CARD=R/'07_HPC_Prompts/LOCAL_AI_GPT56_FORMAT_RECOLLECTION7_ONCE_THEN_CLOSEOUT_20261111.md'
sys.path.insert(0,str(R/'FOREIGN_NATIVE_GO_PLUS_FIRST10_BATCH_20261109/code'))
import batch as retained
core=retained.core
base=retained.base
prior=retained.prior
load,dump,sha,compact=base.load,base.dump,base.sha,base.compact
MODEL='gpt-5.6-luna'
KEY=pathlib.Path('/home/a/EnzymeCAGE/opencode_luna_api_key.txt')
ENDPOINT='https://opencode.ai/inference/go/openai/v1/responses'
INDEX=R/'BASE_MODEL_EXTENSION_PREP_20261109/FROZEN_QUESTION_INDEX_121.tsv'
SCHEMA=base.INPUT/'schemas/biodegradation_answer_v2.schema.json'
CASES=['BIOPATH150_012','BIOPATH150_013','BIOPATH150_017','BIOPATH150_083','BIOPATH150_098','BIOPATH150_105','BIOPATH150_107']
MAX_POSTS=7
ROUND_CAP=0.75
BASE_56_KNOWN=0.6426708500000006
COMBINED_56_CAP=2.0
REPEAT_FAULT_STOP=5
UA='EnzymeCAGE-Research-Pilot/20261109 (independent scientific question collection)'
USER_VERBATIM='可以，我赞成再收一次。……仅这7题各重答一次，成功的114份不动……做完再收尾，不顺带补Grok或GPT 6。'


def original_for(case):
    l=load(W2/'run/ledger.json')
    s=next(x for x in l['slots'] if x['case_id']==case)
    a=next(x for x in l['attempts'] if x['slot']==s['slot'])
    return l,s,a


def lock():
    path=W/'run/process.lock';path.parent.mkdir(parents=True,exist_ok=True)
    handle=path.open('a');fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
    return handle


def prepare():
    held=lock()
    assert not (W/'run/ledger.json').exists(),'Never reset the recollection ledger'
    rows={r['case_id']:r for r in csv.DictReader(INDEX.open(),delimiter='\t')}
    targets=[]
    for case in CASES:
        l2,s,a=original_for(case)
        d=pathlib.Path(a['result_path']).parent
        raw=(d/'request_body.json').read_bytes()
        row=rows[case];source=R/row['source_message_file'];sraw=source.read_bytes()
        assert sha(sraw)==row['source_file_sha256']
        messages=json.loads(sraw)['messages']
        assert sha(compact(messages))==row['messages_sha256'] and sha(messages[0]['content'].encode())==row['prompt_text_sha256']
        rebuilt=compact(retained.body_for(case,MODEL))
        assert rebuilt==raw==compact(retained.body_for(row['case_id'],MODEL)) and sha(raw)==a['request_sha256']==s['request_sha256'],case
        answer_sha=sha((d/'visible_answer.txt').read_bytes())
        slot=f'RC7-{case[-3:]}'
        rd=W/'run'/slot;rd.mkdir(parents=True,exist_ok=False)
        (rd/'request_body.json').write_bytes(raw)
        targets.append(dict(slot=slot,case_id=case,model=MODEL,status='READY',attempt_ids=[],
            session_id=str(uuid.uuid4()),request_sha256=sha(raw),dedup_key=case+'|'+MODEL+'|recollection_R1',
            original_slot=s['slot'],original_attempt=a['attempt_id'],original_result_path=str(d/'result.json'),
            original_request_sha256=sha(raw),original_answer_sha256=answer_sha,
            original_session=s['session_id'],worst_list_reservation_usd=s['worst_list_reservation_usd'],
            source_version='FORMAT_RECOLLECTION_R1'))
    assert len(targets)==7 and len({t['case_id'] for t in targets})==7
    dump(W/'AUTHORIZATION.json',dict(card=str(CARD),card_sha256=sha(CARD.read_bytes()),user_verbatim=USER_VERBATIM,
        model=MODEL,cases=CASES,post_cap=MAX_POSTS,round_list_cap_usd=ROUND_CAP,combined_56_cap_usd=COMBINED_56_CAP,
        base_56_known_list_usd=BASE_56_KNOWN,source_alias='LUNA_ACCOUNT_B',cash_authorized=False,
        one_attempt_per_case=True,no_third_answer_even_if_format_fail=True,independent_of_dual_model_tech_pool=True,
        excludes=['gpt-6 86 gaps','grok-4.7 BIOPATH150_087/145','original 114 valid answers']))
    dump(W/'run/ledger.json',dict(model=MODEL,posts_committed=0,accounted_usd=0.,unknown_usd=0.,known_list=0.,known_allowance=0.,known_cash=0.,
        stop_reason=None,repeat_fault={},targets=targets,attempts=[]))
    paths=[INDEX,SCHEMA,CARD,pathlib.Path(__file__),REVIEW/'FORMAT_FAILURES.json',REVIEW/'REVIEW_REPORT.json' if (REVIEW/'REVIEW_REPORT.json').exists() else REVIEW/'REVIEW_REPORT.md',W2/'run/ledger.json']
    for t in targets:paths.append(pathlib.Path(t['original_result_path']))
    dump(W/'FROZEN_SOURCES.json',{str(p):sha(p.read_bytes()) for p in paths})
    print(json.dumps(dict(targets=7,round_cap=ROUND_CAP,combined=COMBINED_56_CAP),ensure_ascii=False),flush=True)


def check():
    l=load(W/'run/ledger.json')
    assert len(l['targets'])==7 and len({t['dedup_key'] for t in l['targets']})==7
    for t in l['targets']:
        assert compact(retained.body_for(t['case_id'],MODEL))==(W/'run'/t['slot']/'request_body.json').read_bytes()
        assert sha((W/'run'/t['slot']/'request_body.json').read_bytes())==t['original_request_sha256']==t['request_sha256']

        rr=load(t['original_result_path']);dd=pathlib.Path(t['original_result_path']).parent
        assert sha((dd/'visible_answer.txt').read_bytes())==t['original_answer_sha256']
    assert not any(t['case_id'] not in CASES for t in l['targets'])
    for path,digest in load(W/'FROZEN_SOURCES.json').items():assert sha(pathlib.Path(path).read_bytes())==digest,path
    print('Offline checks PASS: seven identities vs originals, frozen requests, one-attempt scope, 114 originals untouched; no POST.',flush=True)


def can_send(l,t):
    assert t['status']=='READY' and not t['attempt_ids'],'ONE_ATTEMPT_PER_CASE'
    assert l['posts_committed']<MAX_POSTS,'RECOLLECTION_POST_CAP_7'
    assert l['accounted_usd']+t['worst_list_reservation_usd']<=ROUND_CAP,'ROUND_CAP_0_75'
    assert BASE_56_KNOWN+l['accounted_usd']+t['worst_list_reservation_usd']<=COMBINED_56_CAP,'COMBINED_56_CAP_2_0'


def settle(l,a,r):
    l['accounted_usd']+=r['list_cost']-a['reserved_list_usd'];l['unknown_usd']-=a['reserved_list_usd']
    l['known_list']+=r['list_cost'];l['known_allowance']+=r['allowance'];l['known_cash']+=r['cash_cost']


def run(opener=None,key=None):
    held=lock();check();l=load(W/'run/ledger.json')
    if l['stop_reason']:print('Persistent stop:',l['stop_reason']);return
    if any(t['status']=='DISPATCH_COMMITTED' for t in l['targets']):
        offline_recover(l)
        l=load(W/'run/ledger.json')
        if l['stop_reason']:print('recovery stopped:',l['stop_reason']);return
    assert stat.S_IMODE(KEY.stat().st_mode)==0o600
    assert subprocess.run(['git','check-ignore','-q',str(KEY)]).returncode==0
    assert subprocess.run(['git','ls-files','--error-unmatch',str(KEY)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
    key=key or KEY.read_text().strip();assert key and not any(x.isspace() for x in key)
    opener=opener or urllib.request.build_opener(base.NoRedirect)
    for t in l['targets']:
        if l['stop_reason']:break
        if t['status']!='READY':continue
        try:can_send(l,t)
        except AssertionError as e:
            l['stop_reason']=str(e);dump(W/'run/ledger.json',l);break
        raw=(W/'run'/t['slot']/'request_body.json').read_bytes();assert sha(raw)==t['request_sha256']
        aid=t['slot']+'-A01';d=W/'run'/t['slot']/aid;d.mkdir(exist_ok=False)
        (d/'request_body.json').write_bytes(raw)
        req=urllib.request.Request(ENDPOINT,data=raw,method='POST',headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','Accept':'text/event-stream','User-Agent':UA,'x-opencode-session':t['session_id']})
        assert req.full_url==ENDPOINT and req.data==raw and req.get_header('X-opencode-session')==t['session_id']
        dump(d/'safe_request_headers.json',{k:v for k,v in req.header_items() if k.lower() in prior.SAFE_REQUEST})
        a=dict(attempt_id=aid,slot=t['slot'],case_id=t['case_id'],model=MODEL,credential_source='LUNA_ACCOUNT_B',source_version='USER_AUTHORIZED_RECOLLECTION',
            status='DISPATCH_COMMITTED',request_sha256=t['request_sha256'],session_id=t['session_id'],commit_unix=time.time(),reserved_list_usd=t['worst_list_reservation_usd'],
            original_attempt=t['original_attempt'])
        l['attempts'].append(a);t['attempt_ids'].append(aid);t['status']='DISPATCH_COMMITTED';l['posts_committed']+=1
        l['accounted_usd']+=a['reserved_list_usd'];l['unknown_usd']+=a['reserved_list_usd'];dump(W/'run/ledger.json',l)
        life=dict(worker_pid=os.getpid(),request_started_unix=time.time(),phase='WAITING_HEADERS',bytes_received=0,event_count=0,timeout_seconds=1800)
        dump(d/'lifecycle.json',life);(d/'raw_stream.sse').touch();error=None
        print(t['case_id'],'RECOLLECTION COMMITTED',flush=True)
        try:
            with opener.open(req,timeout=1800) as resp:core.receive(resp,d,life)
        except urllib.error.HTTPError as exc:
            error='HTTP_ERROR';life.update(http_status=exc.code,phase='HTTP_ERROR',stream_closed_unix=time.time(),retry_after_raw=(exc.headers.get('Retry-After') if hasattr(exc.headers,'get') else None))
            dump(d/'lifecycle.json',life);(d/'http_error_body.bin').write_bytes(exc.read().replace(key.encode(),b'[REDACTED]'))
        except Exception as exc:
            error=type(exc).__name__;life.update(phase='TRANSPORT_UNKNOWN',exception_class=error,stream_closed_unix=time.time());dump(d/'lifecycle.json',life)
        result=core.materialize(d,t,a,life,error);result['label']='GPT56_FORMAT_RECOLLECTION_R1';dump(d/'result.json',result)
        stop=prior.gate(result,MODEL,life.get('http_status'),error)
        if stop is None:
            assert math.isfinite(result['list_cost']) and math.isfinite(result['allowance'])
            settle(l,a,result)
            if result['list_cost']>a['reserved_list_usd']+1e-8:stop='ACTUAL_COST_EXCEEDS_RESERVATION'
            a.update(status='COMPLETE' if result.get('completed') else 'INCOMPLETE_OR_UNKNOWN',result_path=str(d/'result.json'),stop_reason=stop,list_cost_usd=result['list_cost'],allowance_usd=result['allowance'],cash_usd=result['cash_cost'],schema_status=result.get('schema_status'))
            t.update(status=a['status'],result_path=a['result_path'])
            if stop:l['stop_reason']=stop
        elif life.get('http_status')==429:
            a.update(status='QUOTA_REJECTED',result_path=str(d/'result.json'),stop_reason='ACCOUNT_QUOTA_429_STOP')
            t.update(status='QUOTA_REJECTED',result_path=a['result_path'])
            l['stop_reason']='ACCOUNT_QUOTA_429_STOP'
        elif result.get('terminal') is None or life.get('http_status')!=200 or error:
            category=error or stop
            a.update(status='RESULT_UNKNOWN_LOCAL',result_path=str(d/'result.json'),stop_reason=stop)
            t.update(status='COMMITTED_OR_UNKNOWN',result_path=a['result_path'])
            l['repeat_fault'][category]=l['repeat_fault'].get(category,0)+1
            if l['repeat_fault'][category]>=REPEAT_FAULT_STOP:l['stop_reason']='REPEATED_SERVICE_FAULT'
        else:
            a.update(status='INCOMPLETE_OR_UNKNOWN',result_path=str(d/'result.json'),stop_reason=stop)
            t.update(status='COMMITTED_OR_UNKNOWN',result_path=a['result_path'])
            l['stop_reason']=stop
        dump(W/'run/ledger.json',l);report()
        print(json.dumps({k:result.get(k) for k in ('case_id','completed','schema_status','duration_seconds','list_cost','allowance','cash_cost')},ensure_ascii=False),flush=True)
        if l['stop_reason']:print('STOP',l['stop_reason'],flush=True);break
    check_final()
    leaks=[str(p2.relative_to(W)) for p2 in W.rglob('*') if p2.is_file() and key.encode() in p2.read_bytes()]
    assert not leaks,'Credential leakage detected; do not publish'
    print(json.dumps(report(),ensure_ascii=False,indent=2),flush=True)


def offline_recover(l):
    for t in l['targets']:
        if t['status']!='DISPATCH_COMMITTED':continue
        aid=t['attempt_ids'][-1];d=W/'run'/t['slot']/aid;a=next(x for x in l['attempts'] if x['attempt_id']==aid)
        raw=(d/'raw_stream.sse').read_bytes() if (d/'raw_stream.sse').exists() else b''
        try:r=base.parse(raw)
        except Exception:r=dict(visible_answer='',usage=None,completed=False)
        parsed,js,_tr=base.collector.parse_answer_text(r.get('visible_answer',''))
        val=base.collector.validate_answer(parsed,load(SCHEMA),check=js=='VALID')
        r.update(slot=t['slot'],case_id=t['case_id'],attempt_id=aid,requested_model=MODEL,label='GPT56_FORMAT_RECOLLECTION_R1_OFFLINE',json_status=js,schema_status=val['schema_status'],visible_characters=len(r.get('visible_answer','')),session_id=t['session_id'])
        (d/'visible_answer.txt').write_text(r.pop('visible_answer',''));dump(d/'result.json',r)
        if r.get('completed') and r.get('usage') and r.get('model')==MODEL and r.get('billing_source')=='go-plus' and r.get('cash_cost')==0:
            settle(l,a,r);a.update(status='COMPLETE',result_path=str(d/'result.json'),stop_reason=None,list_cost_usd=r['list_cost'],allowance_usd=r['allowance'],cash_usd=r['cash_cost'],schema_status=val['schema_status'])
            t.update(status='COMPLETE',result_path=a['result_path'])
        else:
            a.update(status='RESULT_UNKNOWN_LOCAL',result_path=str(d/'result.json'),stop_reason='OFFLINE_RECOVERED_UNKNOWN')
            t.update(status='COMMITTED_OR_UNKNOWN',result_path=a['result_path'])
        print('offline replay',aid,'->',t['status'],flush=True)
    dump(W/'run/ledger.json',l)


def check_final():
    l=load(W/'run/ledger.json')
    for pth,digest in load(W/'FROZEN_SOURCES.json').items():
        if str(pth).startswith(str(W2))or pth.endswith('run/ledger.json'):assert sha(pathlib.Path(pth).read_bytes())==digest,pth
    print('final identity check: originals and frozen sources unchanged',flush=True)


def report():
    l=load(W/'run/ledger.json')
    rec=[]
    for t in l['targets']:
        row=dict(case_id=t['case_id'],status=t['status'],source_version='USER_AUTHORIZED_RECOLLECTION',
            original_attempt_id=t['original_attempt'],original_result_path=t['original_result_path'],original_request_sha256=t['original_request_sha256'],original_answer_sha256=t['original_answer_sha256'],
            recollection_attempt_id=(t['attempt_ids'][0] if t['attempt_ids'] else None),recollection_result_path=t.get('result_path'),recollection_session_id=t['session_id'],
            schema_status=None,json_status=None,list_cost=None,allowance=None,cash=None,duration=None)
        if t.get('result_path'):
            r=load(t['result_path'])
            row.update(schema_status=r.get('schema_status'),json_status=r.get('json_status'),list_cost=r.get('list_cost'),allowance=r.get('allowance'),cash=r.get('cash_cost'),duration=r.get('duration_seconds'))
        rec.append(row)
    with (W/'RECOLLECTION_MAP.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rec[0].keys()),delimiter='\t',lineterminator='\n');w.writeheader();[w.writerow(x) for x in rec]
    k=sum(1 for x in rec if x['status']=='COMPLETE' and x['schema_status'] in ('VALID','PASS'))
    summary=dict(model=MODEL,task='GPT56_FORMAT_RECOLLECTION7_R1',targets=7,actual_posts=l['posts_committed'],
        recollection_schema_valid=k,recollection_other=7-k,
        first_baseline_unchanged=dict(total=121,schema_valid=114,format_fail=7),
        usability_view=dict(baseline_valid=114,recaptured_valid=k,recovered_usable_total=114+k,cap_note='max 121 usable; first-attempt rates are not rewritten; no cross-version cherry-picking'),
        known_list_usd_round=l['known_list'],known_allowance_usd_round=l['known_allowance'],known_cash_usd=l['known_cash'],
        combined_56_list_after=BASE_56_KNOWN+l['known_list'],combined_cap=COMBINED_56_CAP,unknown_reservation_usd=l['unknown_usd'],
        stop_reason=l['stop_reason'],repeat_fault=l['repeat_fault'],originals_untouched=True)
    dump(W/'SUMMARY.json',summary)
    view=[]
    l2=load(W2/'run/ledger.json')
    for s in l2['slots']:
        if s['status']=='REUSED_VERIFIED':
            view.append(dict(case_id=s['case_id'],used_source='FIRST5_REUSE',source_version='FIRST_ATTEMPT',result_path=s['source_result_path'],schema='VALID'))
        elif s['case_id'] in CASES:
            m=next(x for x in rec if x['case_id']==s['case_id'])
            if m['status']=='COMPLETE' and m['schema_status'] in ('VALID','PASS'):
                view.append(dict(case_id=s['case_id'],used_source='RECOLLECTION',source_version='USER_AUTHORIZED_RECOLLECTION',result_path=m['recollection_result_path'],schema=m['schema_status']))
            else:
                view.append(dict(case_id=s['case_id'],used_source='FIRST_ATTEMPT_FORMAT_FAIL',source_version='FIRST_ATTEMPT',result_path=s.get('result_path'),schema='INVALID_OR_UNPARSEABLE_KEPT'))
        else:
            rr=load(s['result_path']) if s.get('result_path') else {}
            view.append(dict(case_id=s['case_id'],used_source='FIRST_ATTEMPT',source_version='FIRST_ATTEMPT',result_path=s.get('result_path'),schema=rr.get('schema_status')))
    with (W/'USABILITY_VIEW_121.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(view[0].keys()),delimiter='\t',lineterminator='\n');w.writeheader();[w.writerow(x) for x in view]
    return summary


if __name__=='__main__':{'prepare':prepare,'check':check,'run':run,'report':lambda:print(json.dumps(report(),ensure_ascii=False,indent=2))}[sys.argv[1]]()
