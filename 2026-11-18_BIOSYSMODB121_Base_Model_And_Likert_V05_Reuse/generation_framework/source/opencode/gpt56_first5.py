"""Five original cases on GPT 5.6 Luna. Reuse audited receiver/parser; no retries."""
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
METADATA=R/'FOREIGN_NATIVE_GO_PLUS_PILOT_R1_20261109/docs/models_public.json'
SCHEMA=base.INPUT/'schemas/biodegradation_answer_v2.schema.json'
CAP_POSTS=5
CAP_LIST=.5
UA='EnzymeCAGE-Research-Pilot/20261109 (independent scientific question collection)'


def selected_rows():
    rows=list(csv.DictReader(INDEX.open(),delimiter='\t'))
    assert len(rows)==121
    return rows[:5]


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
    assert 'reasoning' not in body and 'temperature' not in body and body['tools']==[]
    return body


def lock():
    path=W/'run/process.lock';path.parent.mkdir(parents=True,exist_ok=True)
    handle=path.open('a');fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
    return handle


def prepare():
    held=lock()
    assert not (W/'run/ledger.json').exists(),'Never reset five-case ledger'
    rows=selected_rows()
    metadata=next(m for m in load(METADATA)['data'] if m['id']==MODEL)
    costs=metadata['cost']['text']
    slots=[]
    for i,row in enumerate(rows,1):
        body=body_for(row);raw=compact(body)
        slot=f'GPT56-FIRST5-{i:03d}'
        source=R/row['source_message_file']
        upper=len(body['input'][0]['content'].encode())+4096
        assert upper+65536<272000 and 65536<=metadata['limit']['output']
        reserve=(upper*max(costs['input']['price'],costs['input'].get('cache',{}).get('write',0))+65536*costs['output']['price'])/1e6
        cfg=retained.science(row['case_id'],MODEL,body)
        config_sha=sha(compact(cfg))
        entry=dict(slot=slot,case_id=row['case_id'],model=MODEL,status='READY',attempt_ids=[],
                   session_id=str(uuid.uuid4()),source_message_file=row['source_message_file'],source_file_sha256=row['source_file_sha256'],
                   messages_sha256=row['messages_sha256'],prompt_sha256=row['prompt_text_sha256'],
                   request_sha256=sha(raw),scientific_config_sha256=config_sha,
                   dedup_key=row['case_id']+'|'+MODEL+'|'+config_sha,worst_list_reservation_usd=reserve)
        d=W/'run'/slot;d.mkdir(parents=True,exist_ok=False);(d/'request_body.json').write_bytes(raw)
        slots.append(entry)
    assert sum(s['worst_list_reservation_usd'] for s in slots)<CAP_LIST
    dump(W/'AUTHORIZATION.json',dict(user_request='你试一下5.6 采集五道题 看看时间 价格 我再决定',
             model=MODEL,cases=[r['case_id'] for r in rows],post_cap=5,list_cap_usd=CAP_LIST,
             full_run_authorized=False,existing_GPT6_answers_unchanged=True,grok_shared_ledger_untouched=True,
             source_alias='LUNA_ACCOUNT_B',cash_authorized=False,retries=0,
             reasoning='NOT_SENT_EFFECTIVE_DEFAULT; not the none-effort connectivity probe',
             question_selection='first five in the original frozen 121-case order; not a representative random sample'))
    dump(W/'run/ledger.json',dict(model=MODEL,posts_committed=0,accounted_usd=0.,unknown_usd=0.,
             known_list=0.,known_allowance=0.,known_cash=0.,stop_reason=None,slots=slots,attempts=[]))
    paths=[INDEX,SCHEMA,METADATA,pathlib.Path(__file__),
           R/'FOREIGN_NATIVE_GO_PLUS_FIRST10_BATCH_20261109/code/batch.py',
           R/'FOREIGN_NATIVE_GO_PLUS_PILOT_R2_20261109/code/r2.py',
           R/'FOREIGN_NATIVE_GO_PLUS_PILOT_R1_20261109/code/r1_runner.py',
           R/'FOREIGN_NATIVE_GO_PLUS_PILOT_20261109/code/pilot.py']+[R/r['source_message_file'] for r in rows]
    dump(W/'FROZEN_SOURCES.json',{str(p):sha(p.read_bytes()) for p in paths})
    print(json.dumps({'prepared_cases':[s['case_id'] for s in slots],'worst_list_reservation_total':sum(s['worst_list_reservation_usd'] for s in slots),'post_cap':5}),flush=True)


def check():
    l=load(W/'run/ledger.json');rows=selected_rows()
    assert len(l['slots'])==5 and len({s['dedup_key'] for s in l['slots']})==5
    for row,s in zip(rows,l['slots']):
        assert s['model']==MODEL and s['case_id']==row['case_id']
        assert compact(body_for(row))==(W/'run'/s['slot']/'request_body.json').read_bytes()
        assert s['request_sha256']==sha(compact(body_for(row)))
    for path,digest in load(W/'FROZEN_SOURCES.json').items():assert sha(pathlib.Path(path).read_bytes())==digest,path
    print('Offline checks PASS: five identities, original G2/G8 messages, exact model, frozen request bytes; no POST.',flush=True)


def report(l):
    results=[load(a['result_path']) for a in l['attempts'] if a.get('result_path')]
    good=[r for r in results if r.get('completed') and r.get('schema_status')=='VALID']
    # Old schema validator may use PASS as its success token; count it explicitly.
    good=[r for r in results if r.get('completed') and r.get('schema_status') in ('VALID','PASS')]
    durations=[r['duration_seconds'] for r in results if r.get('completed')]
    summary=dict(model=MODEL,targets=5,actual_posts=l['posts_committed'],completed=sum(bool(r.get('completed')) for r in results),
                 schema_statuses={r['case_id']:r.get('schema_status') for r in results},
                 completed_and_schema_valid=len(good),known_list_usd=l['known_list'],known_allowance_usd=l['known_allowance'],
                 known_cash_usd=l['known_cash'],unknown_list_reservation_usd=l['unknown_usd'],stop_reason=l['stop_reason'],
                 full_run_authorized=False,reuse_successes_in_future=True,scientific_correctness_reviewed=False)
    if durations:
        summary['duration_seconds']=dict(mean=statistics.mean(durations),median=statistics.median(durations),minimum=min(durations),maximum=max(durations),sum=sum(durations))
    if len(results)==5 and all(r.get('list_cost') is not None for r in results):
        summary['linear_121_estimate']=dict(total_list_usd=l['known_list']/5*121,remaining_116_list_usd=l['known_list']/5*116,
            total_allowance_usd=l['known_allowance']/5*121,remaining_116_allowance_usd=l['known_allowance']/5*116,
            total_serial_minutes=statistics.mean(durations)*121/60 if len(durations)==5 else None,
            caveat='First-five sample; not a guarantee or account quota observation. Reuse these five, do not recollect them.')
    dump(W/'SUMMARY.json',summary)
    fields=['case_id','model','http_status','completed','schema_status','duration_seconds','first_visible_seconds','visible_characters','input_tokens','output_tokens','reasoning_tokens','list_cost','allowance','cash_cost']
    with (W/'RESULTS.tsv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');writer.writeheader()
        for r in results:
            row={k:r.get(k) for k in fields};row['input_tokens']=(r.get('usage') or {}).get('input_tokens');row['output_tokens']=(r.get('usage') or {}).get('output_tokens');writer.writerow(row)
    return summary


def run():
    held=lock();check();l=load(W/'run/ledger.json')
    assert l['stop_reason'] is None
    assert not any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']),'Never resend an unknown committed request'
    assert stat.S_IMODE(KEY.stat().st_mode)==0o600
    assert subprocess.run(['git','check-ignore','-q',str(KEY)]).returncode==0
    assert subprocess.run(['git','ls-files','--error-unmatch',str(KEY)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
    key=KEY.read_text().strip();assert key and not any(x.isspace() for x in key)
    opener=urllib.request.build_opener(base.NoRedirect)
    for s in l['slots']:
        if s['status']!='READY':continue
        assert l['posts_committed']<CAP_POSTS and not s['attempt_ids']
        assert l['accounted_usd']+s['worst_list_reservation_usd']<=CAP_LIST
        source=R/s['source_message_file'];assert sha(source.read_bytes())==s['source_file_sha256']
        raw=(W/'run'/s['slot']/'request_body.json').read_bytes();assert sha(raw)==s['request_sha256']
        aid=s['slot']+'-A01';d=W/'run'/s['slot']/aid;d.mkdir(exist_ok=False)
        (d/'request_body.json').write_bytes(raw)
        req=urllib.request.Request(ENDPOINT,data=raw,method='POST',headers={'Authorization':'Bearer '+key,
             'Content-Type':'application/json','Accept':'text/event-stream','User-Agent':UA,'x-opencode-session':s['session_id']})
        dump(d/'safe_request_headers.json',{k:v for k,v in req.header_items() if k.lower() in prior.SAFE_REQUEST})
        a=dict(attempt_id=aid,slot=s['slot'],model=MODEL,credential_source='LUNA_ACCOUNT_B',status='DISPATCH_COMMITTED',
               request_sha256=s['request_sha256'],commit_unix=time.time(),reserved_list_usd=s['worst_list_reservation_usd'])
        l['attempts'].append(a);s['attempt_ids'].append(aid);s['status']='DISPATCH_COMMITTED';l['posts_committed']+=1
        l['accounted_usd']+=a['reserved_list_usd'];l['unknown_usd']+=a['reserved_list_usd'];dump(W/'run/ledger.json',l)
        life=dict(worker_pid=os.getpid(),request_started_unix=time.time(),phase='WAITING_HEADERS',bytes_received=0,event_count=0,timeout_seconds=1800)
        dump(d/'lifecycle.json',life);(d/'raw_stream.sse').touch();error=None
        print(s['case_id'],'COMMITTED',flush=True)
        try:
            with opener.open(req,timeout=1800) as resp:core.receive(resp,d,life)
        except urllib.error.HTTPError as exc:
            error='HTTP_ERROR';life.update(http_status=exc.code,phase='HTTP_ERROR',stream_closed_unix=time.time())
            dump(d/'lifecycle.json',life);(d/'http_error_body.bin').write_bytes(exc.read().replace(key.encode(),b'[REDACTED]'))
        except Exception as exc:
            error=type(exc).__name__;life.update(phase='TRANSPORT_UNKNOWN',exception_class=error,stream_closed_unix=time.time());dump(d/'lifecycle.json',life)
        result=core.materialize(d,s,a,life,error);result['label']='GPT56_FIRST5_FORMAL_REUSABLE';dump(d/'result.json',result)
        stop=prior.gate(result,MODEL,life.get('http_status'),error)
        if stop is None:
            assert math.isfinite(result['list_cost']) and math.isfinite(result['allowance'])
            l['accounted_usd']+=result['list_cost']-a['reserved_list_usd'];l['unknown_usd']-=a['reserved_list_usd']
            l['known_list']+=result['list_cost'];l['known_allowance']+=result['allowance'];l['known_cash']+=result['cash_cost']
            if result['list_cost']>a['reserved_list_usd']+1e-8 or l['accounted_usd']>CAP_LIST:stop='ACTUAL_COST_EXCEEDS_RESERVATION'
        a.update(status='COMPLETE' if result.get('completed') else 'INCOMPLETE_OR_UNKNOWN',result_path=str(d/'result.json'),stop_reason=stop)
        s.update(status=a['status'],result_path=a['result_path'])
        if stop:l['stop_reason']=stop
        dump(W/'run/ledger.json',l);report(l)
        print(json.dumps({k:result.get(k) for k in ('case_id','completed','schema_status','duration_seconds','list_cost','allowance','cash_cost')},ensure_ascii=False),flush=True)
        if stop:print('STOP',stop,flush=True);break
    check()
    leaks=[str(p.relative_to(W)) for p in W.rglob('*') if p.is_file() and key.encode() in p.read_bytes()]
    assert not leaks,'Credential leakage detected; do not publish'
    dump(W/'KEY_HANDLING.json',dict(designated_file_only=True,mode_600=True,no_key_or_digest_recorded=True,leak_check_passed=True))
    print(json.dumps(report(l),ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':{'prepare':prepare,'check':check,'run':run,'report':lambda:print(json.dumps(report(load(W/'run/ledger.json')),ensure_ascii=False,indent=2))}[sys.argv[1]]()
