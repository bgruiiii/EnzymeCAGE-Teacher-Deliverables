"""GPT 5.6 Luna full continuation: reuse the audited five, collect the remaining 116 original cases.
Independent workspace/ledger/lock; never touches the Grok four-way queue or the old dual-model ledger.
Card: LOCAL_AI_GPT56_LUNA_FULL_REMAINING116_REUSE5_EXECUTOR_ONLY_20261110."""
import csv
import fcntl
import json
import math
import os
import pathlib
import stat
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

W=pathlib.Path(__file__).resolve().parents[1]
R=W.parent
F=R/'FOREIGN_NATIVE_GPT56_LUNA_FIRST5_20261110'
sys.path.insert(0,str(R/'FOREIGN_NATIVE_GO_PLUS_FIRST10_BATCH_20261109/code'))
import batch as retained
core=retained.core
base=retained.base
prior=retained.prior
sys.path.insert(0,str(R/'FOREIGN_NATIVE_GO_PLUS_PILOT_20261109/code'))
import replay
load,dump,sha,compact=base.load,base.dump,base.sha,base.compact
MODEL='gpt-5.6-luna'
KEY=pathlib.Path('/home/a/EnzymeCAGE/opencode_luna_api_key.txt')
ENDPOINT='https://opencode.ai/inference/go/openai/v1/responses'
INDEX=R/'BASE_MODEL_EXTENSION_PREP_20261109/FROZEN_QUESTION_INDEX_121.tsv'
METADATA=R/'FOREIGN_NATIVE_GO_PLUS_PILOT_R1_20261109/docs/models_public.json'
SCHEMA=base.INPUT/'schemas/biodegradation_answer_v2.schema.json'
REUSE_CASES=['BIOPATH150_001','BIOPATH150_002','BIOPATH150_004','BIOPATH150_005','BIOPATH150_006']
CAP_NEW_POSTS=116
CAP_CUM_POSTS=121
CAP_LIST=2.0  # cumulative 5.6 formal batch list-price cap incl. carried five, unknowns and in-flight worst reservations
CHECKPOINT_EVERY=10
REPEAT_FAULT_STOP=5
UA='EnzymeCAGE-Research-Pilot/20261109 (independent scientific question collection)'


def all_rows():
    rows=list(csv.DictReader(INDEX.open(),delimiter='\t'))
    assert len(rows)==121
    return rows


def body_for(row):
    source=R/row['source_message_file']
    raw=source.read_bytes()
    assert sha(raw)==row['source_file_sha256']
    messages=json.loads(raw)['messages']
    assert sha(compact(messages))==row['messages_sha256']
    assert len(messages)==1 and messages[0]['role']=='user'
    assert sha(messages[0]['content'].encode())==row['prompt_text_sha256']
    assert (base.INPUT/'messages'/source.name).read_bytes()==raw
    body=retained.body_for(row['case_id'],MODEL)
    assert body['input']==messages and body['max_output_tokens']==65536
    assert 'reasoning' not in body and 'temperature' not in body and body['tools']==[] and body['tool_choice']=='none'
    return body


def lock():
    path=W/'run/process.lock';path.parent.mkdir(parents=True,exist_ok=True)
    handle=path.open('a');fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
    return handle


def prepare():
    held=lock()
    assert not (W/'run/ledger.json').exists(),'Never reset an existing 5.6 ledger'
    rows=all_rows()
    fl=load(F/'run/ledger.json')
    fattempt={a["slot"]:a for a in fl["attempts"]}
    assert fl['posts_committed']==5 and sum(1 for a in fl['attempts'] if a['status']=='COMPLETE')==5
    metadata=next(m for m in load(METADATA)['data'] if m['id']==MODEL)
    costs=metadata['cost']['text']
    slots=[];carry_list=0.0
    for i,row in enumerate(rows,1):
        body=body_for(row);raw=compact(body)
        slot=f'GPT56-FULL-{i:03d}'
        cfg=retained.science(row['case_id'],MODEL,body)
        config_sha=sha(compact(cfg))
        entry=dict(slot=slot,case_id=row['case_id'],model=MODEL,attempt_ids=[],
                   session_id=str(uuid.uuid4()),source_message_file=row['source_message_file'],source_file_sha256=row['source_file_sha256'],
                   messages_sha256=row['messages_sha256'],prompt_sha256=row['prompt_text_sha256'],
                   request_sha256=sha(raw),scientific_config_sha256=config_sha,
                   dedup_key=row['case_id']+'|'+MODEL+'|'+config_sha)
        if row['case_id'] in REUSE_CASES:
            fa=fattempt[next(s for s in fl['slots'] if s['case_id']==row['case_id'])['slot']]
            rd=pathlib.Path(fa['result_path'])
            entry.update(status='REUSED_VERIFIED',source_result_path=str(rd),source_attempt=fa['attempt_id'],
                         source_request_sha256=fa['request_sha256'],carry_verified=True)
            carry_list+=load(rd)['list_cost']
        else:
            upper=len(body['input'][0]['content'].encode())+4096
            assert upper+65536<272000 and 65536<=metadata['limit']['output']
            entry.update(status='READY',worst_list_reservation_usd=(upper*max(costs['input']['price'],costs['input'].get('cache',{}).get('write',0))+65536*costs['output']['price'])/1e6)
            d=W/'run'/slot;d.mkdir(parents=True,exist_ok=False);(d/'request_body.json').write_bytes(raw)
        slots.append(entry)
    assert sum(1 for s in slots if s['status']=='REUSED_VERIFIED')==5
    assert sum(1 for s in slots if s['status']=='READY')==116
    assert len({s['dedup_key'] for s in slots})==121
    dump(W/'AUTHORIZATION.json',dict(card=str(R/'07_HPC_Prompts/LOCAL_AI_GPT56_LUNA_FULL_REMAINING116_REUSE5_EXECUTOR_ONLY_20261110.md'),
         card_sha256=sha((R/'07_HPC_Prompts/LOCAL_AI_GPT56_LUNA_FULL_REMAINING116_REUSE5_EXECUTOR_ONLY_20261110.md').read_bytes()),
         user_request='那就让它全量用5.6吧。你写个提示词，我去执行，把剩下的跑完。',model=MODEL,
         reuse_cases=REUSE_CASES,new_post_cap=CAP_NEW_POSTS,cum_post_cap=CAP_CUM_POSTS,list_cap_usd=CAP_LIST,
         source_alias='LUNA_ACCOUNT_B',cash_authorized=False,grok_queue_untouched=True,
         retries='none for success/unknown; single-target faults freeze and continue',full_run_authorized=True))
    dump(W/'run/ledger.json',dict(model=MODEL,posts_committed=5,new_posts=0,accounted_usd=carry_list,unknown_usd=0.,
         known_list=carry_list,known_allowance=load(F/'SUMMARY.json')['known_allowance_usd'],known_cash=0.,
         stop_reason=None,repeat_fault={},settled_count=0,slots=slots,attempts=[]))
    paths=[INDEX,SCHEMA,METADATA,pathlib.Path(__file__),
           R/'FOREIGN_NATIVE_GO_PLUS_FIRST10_BATCH_20261109/code/batch.py',
           R/'FOREIGN_NATIVE_GO_PLUS_PILOT_R2_20261109/code/r2.py',
           R/'FOREIGN_NATIVE_GO_PLUS_PILOT_R1_20261109/code/r1_runner.py',
           R/'FOREIGN_NATIVE_GO_PLUS_PILOT_20261109/code/pilot.py',
           F/'run/ledger.json',F/'SUMMARY.json']+[R/r['source_message_file'] for r in rows]
    dump(W/'FROZEN_SOURCES.json',{str(p):sha(p.read_bytes()) for p in paths})
    print(json.dumps({'reused':5,'ready':116,'carry_list_usd':carry_list,'cum_post_cap':CAP_CUM_POSTS,'list_cap':CAP_LIST}),flush=True)


def check():
    l=load(W/'run/ledger.json');rows=all_rows()
    assert len(l['slots'])==121 and len({s['dedup_key'] for s in l['slots']})==121
    for row,s in zip(rows,l['slots']):
        assert s['model']==MODEL and s['case_id']==row['case_id']
        if s['status']=='READY':
            assert compact(body_for(row))==(W/'run'/s['slot']/'request_body.json').read_bytes()
            assert s['request_sha256']==sha(compact(body_for(row)))
        elif s.get('carry_verified'):
            rd=pathlib.Path(s['source_result_path']);dd=rd.parent
            v=replay.replay((dd/'raw_stream.sse').read_bytes())
            rr=load(rd)
            assert v['usage']==rr.get('usage') and v['terminal']==rr.get('terminal') and v['visible_answer']==(dd/'visible_answer.txt').read_text()
            assert sha((dd/'request_body.json').read_bytes())==s['source_request_sha256']
    for path,digest in load(W/'FROZEN_SOURCES.json').items():assert sha(pathlib.Path(path).read_bytes())==digest,path
    print('Offline checks PASS: 121 identities, five reused raw streams replay-equal, exact model, frozen request bytes; no POST.',flush=True)


def can_dispatch(l,s):
    assert s['status']=='READY' and not s['attempt_ids'],'DEDUP_ALREADY_SUBMITTED_OR_REUSED'
    assert l['new_posts']<CAP_NEW_POSTS,'NEW_POST_CAP_116'
    assert l['posts_committed']<CAP_CUM_POSTS,'CUM_POST_CAP_121'
    assert l['accounted_usd']+s['worst_list_reservation_usd']<=CAP_LIST,'LIST_CAP_2_0'


def settle(l,s,a,result):
    l['accounted_usd']+=result['list_cost']-a['reserved_list_usd'];l['unknown_usd']-=a['reserved_list_usd']
    l['known_list']+=result['list_cost'];l['known_allowance']+=result['allowance'];l['known_cash']+=result['cash_cost']


def run(opener=None,key=None,now=None):
    now=now or time.time
    held=lock();check();l=load(W/'run/ledger.json')
    if l['stop_reason']:print('Persistent stop:',l['stop_reason']);return
    if any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']):
        offline_recover(l,now)
        l=load(W/'run/ledger.json')
        if l['stop_reason']:print('recovery stopped worker:',l['stop_reason']);return
    assert stat.S_IMODE(KEY.stat().st_mode)==0o600
    assert subprocess.run(['git','check-ignore','-q',str(KEY)]).returncode==0
    assert subprocess.run(['git','ls-files','--error-unmatch',str(KEY)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
    key=key or KEY.read_text().strip();assert key and not any(x.isspace() for x in key)
    opener=opener or urllib.request.build_opener(base.NoRedirect)
    for s in l['slots']:
        if l['stop_reason']:break
        if s['status']!='READY':continue
        try:can_dispatch(l,s)
        except AssertionError as e:
            l['stop_reason']=str(e);dump(W/'run/ledger.json',l);break
        source=R/s['source_message_file'];assert sha(source.read_bytes())==s['source_file_sha256']
        raw=(W/'run'/s['slot']/'request_body.json').read_bytes();assert sha(raw)==s['request_sha256']
        aid=s['slot']+'-A01';d=W/'run'/s['slot']/aid;d.mkdir(exist_ok=False)
        (d/'request_body.json').write_bytes(raw)
        req=urllib.request.Request(ENDPOINT,data=raw,method='POST',headers={'Authorization':'Bearer '+key,
             'Content-Type':'application/json','Accept':'text/event-stream','User-Agent':UA,'x-opencode-session':s['session_id']})
        assert req.full_url==ENDPOINT and req.data==raw
        dump(d/'safe_request_headers.json',{k:v for k,v in req.header_items() if k.lower() in prior.SAFE_REQUEST})
        a=dict(attempt_id=aid,slot=s['slot'],case_id=s['case_id'],model=MODEL,credential_source='LUNA_ACCOUNT_B',status='DISPATCH_COMMITTED',
               request_sha256=s['request_sha256'],session_id=s['session_id'],commit_unix=now(),reserved_list_usd=s['worst_list_reservation_usd'])
        l['attempts'].append(a);s['attempt_ids'].append(aid);s['status']='DISPATCH_COMMITTED';l['posts_committed']+=1;l['new_posts']+=1
        l['accounted_usd']+=a['reserved_list_usd'];l['unknown_usd']+=a['reserved_list_usd'];dump(W/'run/ledger.json',l)
        life=dict(worker_pid=os.getpid(),request_started_unix=now(),phase='WAITING_HEADERS',bytes_received=0,event_count=0,timeout_seconds=1800)
        dump(d/'lifecycle.json',life);(d/'raw_stream.sse').touch();error=None
        print(s['case_id'],'COMMITTED',flush=True)
        try:
            with opener.open(req,timeout=1800) as resp:core.receive(resp,d,life)
        except urllib.error.HTTPError as exc:
            error='HTTP_ERROR';life.update(http_status=exc.code,phase='HTTP_ERROR',stream_closed_unix=now(),safe_headers={k:v for k,v in exc.headers.items() if k.lower() in prior.SAFE_RESPONSE},retry_after_raw=(exc.headers.get('Retry-After') if hasattr(exc.headers,'get') else None))
            dump(d/'lifecycle.json',life);(d/'http_error_body.bin').write_bytes(exc.read().replace(key.encode(),b'[REDACTED]'))
        except Exception as exc:
            error=type(exc).__name__;life.update(phase='TRANSPORT_UNKNOWN',exception_class=error,stream_closed_unix=now());dump(d/'lifecycle.json',life)
        result=core.materialize(d,s,a,life,error);result['label']='GPT56_FULL_FORMAL';dump(d/'result.json',result)
        stop=prior.gate(result,MODEL,life.get('http_status'),error)
        if stop is None:
            assert math.isfinite(result['list_cost']) and math.isfinite(result['allowance'])
            settle(l,s,a,result)
            if result['list_cost']>a['reserved_list_usd']+1e-8:stop='ACTUAL_COST_EXCEEDS_RESERVATION'
            a.update(status='COMPLETE' if result.get('completed') else 'INCOMPLETE_OR_UNKNOWN',result_path=str(d/'result.json'),stop_reason=stop,
                     list_cost_usd=result['list_cost'],allowance_usd=result['allowance'],cash_usd=result['cash_cost'])
            s.update(status=a['status'],result_path=a['result_path'])
            l['settled_count']+=1;l['repeat_fault']={}
            if l['settled_count']%CHECKPOINT_EVERY==0:
                dump(W/'PROGRESS_CHECKPOINTS'/('CHECKPOINT_%03d.json'%l['settled_count']),dict(unix=now(),settled=l['settled_count'],new_posts=l['new_posts'],known_list=l['known_list'],known_allowance=l['known_allowance'],known_cash=l['known_cash'],unknown=l['unknown_usd'],accounted=l['accounted_usd']))
            if stop:l['stop_reason']=stop
        elif life.get('http_status')==429:
            a.update(status='QUOTA_REJECTED',result_path=str(d/'result.json'),stop_reason='ACCOUNT_QUOTA_429_STOP')
            s.update(status='QUOTA_REJECTED',result_path=a['result_path'])
            l['stop_reason']='ACCOUNT_QUOTA_429_STOP'
        elif result.get('terminal') is None or life.get('http_status')!=200 or error:
            category=error or stop
            a.update(status='RESULT_UNKNOWN_LOCAL',result_path=str(d/'result.json'),stop_reason=stop)
            s.update(status='COMMITTED_OR_UNKNOWN',result_path=a['result_path'])
            l['settled_count']+=1
            l['repeat_fault'][category]=l['repeat_fault'].get(category,0)+1
            if l['repeat_fault'][category]>=REPEAT_FAULT_STOP:l['stop_reason']='REPEATED_SERVICE_FAULT'
        else:
            a.update(status='INCOMPLETE_OR_UNKNOWN',result_path=str(d/'result.json'),stop_reason=stop)
            s.update(status='COMMITTED_OR_UNKNOWN',result_path=a['result_path'])
            l['stop_reason']=stop
        dump(W/'run/ledger.json',l);report(l)
        print(json.dumps({k:result.get(k) for k in ('case_id','completed','schema_status','duration_seconds','list_cost','allowance','cash_cost')},ensure_ascii=False),flush=True)
        if l['stop_reason']:print('STOP',l['stop_reason'],flush=True);break
    check()
    leaks=[str(p.relative_to(W)) for p in W.rglob('*') if p.is_file() and key.encode() in p.read_bytes()]
    assert not leaks,'Credential leakage detected; do not publish'
    dump(W/'KEY_HANDLING.json',dict(designated_file_only=True,mode_600=True,no_key_or_digest_recorded=True,leak_check_passed=True))
    print(json.dumps(report(l),ensure_ascii=False,indent=2),flush=True)


def offline_recover(l,now=None):
    now=now or time.time
    for s in l['slots']:
        if s['status']!='DISPATCH_COMMITTED':continue
        aid=s['attempt_ids'][-1];d=W/'run'/s['slot']/aid;a=next(x for x in l['attempts'] if x['attempt_id']==aid)
        life=load(d/'lifecycle.json') if (d/'lifecycle.json').exists() else dict(request_started_unix=a['commit_unix'],http_status=200,phase='RECOVERED')
        raw=(d/'raw_stream.sse').read_bytes() if (d/'raw_stream.sse').exists() else b''
        try:r=base.parse(raw)
        except Exception:r=dict(visible_answer='',usage=None,completed=False)
        parsed,js,_tr=base.collector.parse_answer_text(r.get('visible_answer',''))
        validation=base.collector.validate_answer(parsed,load(SCHEMA),check=js=='VALID')
        r.update(slot=s['slot'],case_id=s['case_id'],attempt_id=aid,requested_model=MODEL,label='GPT56_FULL_OFFLINE_RECOVERED',
                 json_status=js,schema_status=validation['schema_status'],visible_characters=len(r.get('visible_answer','')),session_id=s['session_id'])
        (d/'visible_answer.txt').write_text(r.pop('visible_answer',''));dump(d/'result.json',r);dump(d/'schema_validation.json',validation)
        life.setdefault('stream_closed_unix',now())
        if r.get('completed') and r.get('usage') and r.get('model')==MODEL and r.get('billing_source')=='go-plus' and r.get('cash_cost')==0:
            settle(l,s,a,r);a.update(status='COMPLETE',result_path=str(d/'result.json'),stop_reason=None,list_cost_usd=r['list_cost'],allowance_usd=r['allowance'],cash_usd=r['cash_cost'])
            s.update(status='COMPLETE',result_path=a['result_path']);l['settled_count']+=1
        else:
            a.update(status='RESULT_UNKNOWN_LOCAL',result_path=str(d/'result.json'),stop_reason='OFFLINE_RECOVERED_UNKNOWN')
            s.update(status='COMMITTED_OR_UNKNOWN',result_path=a['result_path']);l['settled_count']+=1
        print('offline replay',aid,'->',s['status'],flush=True)
    dump(W/'run/ledger.json',l)


def report(l):
    results=[load(a['result_path']) for a in l['attempts'] if a.get('result_path')]
    good=[r for r in results if r.get('completed') and r.get('schema_status') in ('VALID','PASS')]
    format_fail=[r for r in results if r.get('completed') and r.get('schema_status') not in ('VALID','PASS')]
    unknowns=[s for s in l['slots'] if s['status']=='COMMITTED_OR_UNKNOWN']
    durations=[r['duration_seconds'] for r in results if r.get('completed')]
    summary=dict(model=MODEL,targets_total=121,reused_verified=5,new_posts=l['new_posts'],cum_posts=l['posts_committed'],
                 completed=sum(bool(r.get('completed')) for r in results),completed_and_schema_valid=len(good),
                 completed_format_fail=len(format_fail),unknown_or_partial=len(unknowns),
                 unsubmitted=sum(1 for s in l['slots'] if s['status']=='READY'),
                 quota_rejected=sum(1 for s in l['slots'] if s['status']=='QUOTA_REJECTED'),
                 known_list_usd=l['known_list'],known_allowance_usd=l['known_allowance'],known_cash_usd=l['known_cash'],
                 unknown_list_reservation_usd=l['unknown_usd'],accounted_usd=l['accounted_usd'],cap_list_usd=CAP_LIST,
                 stop_reason=l['stop_reason'],repeat_fault=l['repeat_fault'],scientific_correctness_reviewed=False)
    if durations:
        summary['duration_seconds']=dict(mean=statistics.mean(durations),median=statistics.median(durations),minimum=min(durations),maximum=max(durations),sum=sum(durations))
    dump(W/'SUMMARY.json',summary)
    fields=['case_id','model','http_status','completed','schema_status','duration_seconds','first_visible_seconds','visible_characters','input_tokens','output_tokens','reasoning_tokens','list_cost','allowance','cash_cost']
    with (W/'RESULTS.tsv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');writer.writeheader()
        for r in results:
            row={k:r.get(k) for k in fields};row['input_tokens']=(r.get('usage') or {}).get('input_tokens');row['output_tokens']=(r.get('usage') or {}).get('output_tokens');writer.writerow(row)
    return summary


def supervise():
    core.W=W
    core.supervise([sys.executable,'-B',str(pathlib.Path(__file__).resolve()),'run'])


if __name__=='__main__':{'prepare':prepare,'check':check,'run':run,'report':lambda:print(json.dumps(report(load(W/'run/ledger.json')),ensure_ascii=False,indent=2)),'supervise':supervise}[sys.argv[1]]()
