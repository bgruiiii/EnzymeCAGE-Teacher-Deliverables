#!/usr/bin/env python3
"""Bounded session-header repair. Original frozen package is read-only."""
import csv, difflib, fcntl, importlib.util, json, os, pathlib, stat, subprocess, sys, time, urllib.request, urllib.error, uuid
W=pathlib.Path(__file__).resolve().parents[1]; R=W.parent
PREV=R/'FOREIGN_NATIVE_GO_PLUS_PILOT_20261109'
spec=importlib.util.spec_from_file_location('previous_pilot',PREV/'code/pilot.py'); base=importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
load,dump,sha,compact=base.load,base.dump,base.sha,base.compact
CARD=R/'07_HPC_Prompts/LOCAL_AI_FOREIGN_NATIVE_GO_PLUS_PILOT_R1_SESSION_REPAIR_AND_BOUNDED_RESUME_20261109.md'
UA='EnzymeCAGE-Research-Pilot/20261109 (independent scientific question collection)'
SAFE_REQUEST={'content-type','accept','user-agent','x-opencode-session'}
SAFE_RESPONSE={'content-type','date','x-request-id','request-id','retry-after'}

def verify_old():
    entries={}
    for line in (PREV/'SHA256SUMS').read_text().splitlines():
        digest,rel=line.split('  ',1); assert sha((PREV/rel).read_bytes())==digest,rel; entries[rel]=digest
    assert len(entries)==38
    assert base.identities()==load(PREV/'INPUT_OUTPUT_IDENTITIES.json')['sources_before']
    return entries

def prepare():
    assert not (W/'run/ledger.json').exists(),'Never reset an existing R1 ledger'
    old=verify_old(); oldledger=load(PREV/'run/ledger.json'); error=load(PREV/'run/GO-P001/http_error_body.bin')
    assert oldledger['posts_committed']==1 and oldledger['stop_reason']=='HTTP_SERVICE_ERROR'
    assert error['error']['type']=='MissingSessionID'
    oldresult=load(PREV/'run/GO-P001/result.json'); assert oldresult['http_status']==400 and oldresult['usage'] is None
    assert (PREV/'run/GO-P001/raw_stream.sse').read_bytes()==b''
    carry=oldledger['slots'][0]['worst_list_cost_usd']; assert abs(carry-0.0354297)<1e-12
    original=load(PREV/'FROZEN_SLOTS.json'); slots=[]
    for row in original:
        s=dict(row); s.update({'status':'READY','session_id':str(uuid.uuid4()),'attempt_ids':(['R0-GO-P001-A01'] if s['slot']=='GO-P001' else []),'has_model_result':False})
        d=W/'run'/s['slot']; d.mkdir(parents=True,exist_ok=True)
        raw=(PREV/'run'/s['slot']/'request_body.json').read_bytes(); assert sha(raw)==s['request_sha256']
        (d/'request_body.json').write_bytes(raw); slots.append(s)
    attempt={'attempt_id':'R0-GO-P001-A01','slot':'GO-P001','status':'HTTP_ERROR','http_status':400,'error_type':'MissingSessionID','source':str(PREV/'run/GO-P001'),'is_model_result':False,'worst_reservation_usd':carry,'list_cost':None,'cash_cost':None,'allowance':None,'reservation_state':'UNKNOWN','accounted_usd':carry,'session_id':None,'note':'Original omitted session header; no prior ID exists. R1 assigns once, persists across any technical replacement/restart.'}
    dump(W/'CARRY_IN.json',{'old_manifest_sha256':sha((PREV/'SHA256SUMS').read_bytes()),'old_38_files':old,'old_ledger':oldledger,'old_post_count':1,'old_unknown_reservation_usd':carry,'old_error':error})
    dump(W/'CONTINUATION_AUTHORIZATION.json',{'source':'User handed off R1 card in current conversation and authorized autonomous bounded technical fixes','card_path':str(CARD),'card_sha256':sha(CARD.read_bytes()),'specific_override':'Only old GO-P001 HTTP400 MissingSessionID may be technically replaced; no blanket stop bypass','old_error_sha256':sha((PREV/'run/GO-P001/http_error_body.bin').read_bytes()),'old_ledger_sha256':sha((PREV/'run/ledger.json').read_bytes()),'post_cap_cumulative':6,'list_cost_cap_cumulative_usd':2,'full_run_authorized':False,'independent_audit_pass':False})
    dump(W/'FROZEN_SLOTS.json',slots)
    cfg=load(PREV/'PILOT_CONFIG.json'); cfg.update({'post_cap':6,'new_post_cap':5,'carry_in_posts':1,'carry_in_unknown_usd':carry,'total_regular_worst_with_carry_usd':carry+sum(s['worst_list_cost_usd'] for s in slots),'technical_margin_max':1,'retries':'bounded explicit protocol replacements only; no content/unknown retry','repair':'x-opencode-session only; bodies byte-identical','metadata_source':str(PREV/'docs/models_public.json')})
    assert cfg['total_regular_worst_with_carry_usd']<=2
    dump(W/'PILOT_CONFIG.json',cfg)
    dump(W/'INPUT_OUTPUT_IDENTITIES.json',{'sources_before':base.identities(),'old_package_before':old})
    dump(W/'run/ledger.json',{'posts_committed':1,'new_posts_committed':0,'accounted_usd':carry,'unknown_reservation_usd':carry,'stop_reason':None,'slots':slots,'attempts':[attempt],'technical_errors_seen':['MissingSessionID'],'technical_margin_used':0})
    print('R1 prepared: old POST=1; carry unknown USD',carry,'regular worst + carry',cfg['total_regular_worst_with_carry_usd'])

def request_bytes(s):
    original=(PREV/'run'/s['slot']/'request_body.json').read_bytes()
    assert sha(original)==s['request_sha256'],'FROZEN_ORIGINAL_DRIFT'
    repair=load(W/'PROTOCOL_REPAIR.json') if (W/'PROTOCOL_REPAIR.json').exists() else {}
    variant=repair.get('variants',{}).get(s['slot'])
    if not variant:return original
    assert s['model']=='grok-4.7' and repair['error_signature']=='EMPTY_TOOLS_TOOL_CHOICE_REJECTED'
    assert sha((W/repair['error_path']).read_bytes())==repair['error_sha256']
    assert sha((W/'docs/xai_openapi.json').read_bytes())==repair['documentation_sha256']
    body=json.loads(original); assert body.pop('tool_choice')=='none' and body['tools']==[]
    expected=compact(body); assert sha(expected)==variant['new_body_sha256']
    assert (W/variant['path']).read_bytes()==expected
    return expected

def build_request(s,raw,key):
    sid=s.get('session_id'); assert isinstance(sid,str) and sid.strip(),'SESSION_REQUIRED_BEFORE_POST'
    assert raw==request_bytes(s),'BODY_DRIFT'
    req=urllib.request.Request(base.ENDPOINT,data=raw,method='POST',headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','Accept':'text/event-stream','User-Agent':UA,'x-opencode-session':sid})
    assert req.get_header('X-opencode-session')==sid
    assert req.full_url==base.ENDPOINT and req.data==raw and req.method=='POST'
    return req

def next_attempt(ledger,s):
    assert not ledger['stop_reason'],'PERSISTENT_STOP'
    assert s['status']=='READY' and not s['has_model_result'],'NO_RESEND_OF_COMMITTED_OR_MODEL_RESULT'
    repair=load(W/'PROTOCOL_REPAIR.json') if (W/'PROTOCOL_REPAIR.json').exists() else {}
    def authorized_protocol_replacement(a):
        return (a['attempt_id']==repair.get('replaces_attempt_id') and a.get('http_status')==400
                and not a.get('is_model_result') and a.get('cash_cost') is None
                and a.get('protocol_error_classification')=='EMPTY_TOOLS_TOOL_CHOICE_REJECTED'
                and ledger['technical_margin_used']==1)
    assert not any(a['slot']==s['slot'] and a['reservation_state']=='UNKNOWN'
                   and a['attempt_id']!='R0-GO-P001-A01' and not authorized_protocol_replacement(a)
                   for a in ledger['attempts']),'UNKNOWN_NO_RETRY'
    assert ledger['posts_committed']<6 and ledger['new_posts_committed']<5,'POST_CAP'
    assert ledger['accounted_usd']+s['worst_list_cost_usd']<=2,'BUDGET_CAP'
    return f"R1-{s['slot']}-A{len(s['attempt_ids'])+1:02d}"

def commit(ledger,s,attempt_id):
    assert attempt_id==next_attempt(ledger,s)
    a={'attempt_id':attempt_id,'slot':s['slot'],'status':'DISPATCH_COMMITTED','session_id':s['session_id'],'request_sha256':s['request_sha256'],'worst_reservation_usd':s['worst_list_cost_usd'],'accounted_usd':s['worst_list_cost_usd'],'reservation_state':'UNKNOWN','commit_unix':time.time(),'is_model_result':False}
    s['status']='DISPATCH_COMMITTED'; s['attempt_ids'].append(attempt_id)
    ledger['attempts'].append(a); ledger['posts_committed']+=1; ledger['new_posts_committed']+=1
    ledger['accounted_usd']+=a['accounted_usd']; ledger['unknown_reservation_usd']+=a['accounted_usd']
    return a

def gate(r,model,http,error=None):
    if http!=200:return 'HTTP_SERVICE_ERROR'
    if error:return 'TRANSPORT_UNKNOWN'
    if r.get('model')!=model:return 'MODEL_MISMATCH_OR_MISSING'
    if r.get('tool_call_detected'):return 'TOOL_CALL_DETECTED'
    if r.get('billing_source')!='go-plus':return 'BILLING_SOURCE_NOT_VERIFIED_GO_PLUS'
    if r.get('cash_cost')!=0:return 'CASH_COST_NONZERO_OR_UNKNOWN'
    u=r.get('usage') or {}
    if not all(isinstance(u.get(k),(int,float)) and not isinstance(u[k],bool) and u[k]>=0 for k in ['input_tokens','output_tokens']):return 'USAGE_UNKNOWN'
    if not all(isinstance(r.get(k),(int,float)) and not isinstance(r[k],bool) and r[k]>=0 for k in ['allowance','list_cost']):return 'BILLING_UNKNOWN'
    if r.get('terminal') not in ['response.completed','response.incomplete']:return 'SERVICE_FAILED_OR_TERMINAL_UNKNOWN'
    # Known, closed incomplete/empty/schema failure is a model result, never regenerated.
    return None

def technical_retry_eligible(ledger,a,error_type):
    # Called only after documented repair + offline tests, never automatically on HTTP failure.
    return (ledger['technical_margin_used']<1 and ledger['posts_committed']<6
            and a.get('http_status')==400 and not a.get('is_model_result')
            and a.get('error_type')==error_type and error_type not in ledger['technical_errors_seen']
            and error_type in ['MissingSessionID'] and a.get('cash_cost') in [None,0])

def acquire_locks():
    old=(PREV/'run/process.lock').open('r'); fcntl.flock(old,fcntl.LOCK_EX|fcntl.LOCK_NB)
    new=(W/'run/process.lock').open('a'); fcntl.flock(new,fcntl.LOCK_EX|fcntl.LOCK_NB)
    return old,new

def dispatch(ledger,s,key,opener):
    raw=request_bytes(s)
    req=build_request(s,raw,key)  # actual send path; invalid header refuses BEFORE durable commit/POST
    aid=next_attempt(ledger,s); d=W/'run'/s['slot']/aid; d.mkdir(parents=True,exist_ok=False)
    (d/'request_body.json').write_bytes(raw)
    safe={k:v for k,v in req.header_items() if k.lower() in SAFE_REQUEST}
    dump(d/'safe_request_headers.json',safe)
    a=commit(ledger,s,aid); a['request_sha256']=sha(req.data); dump(W/'run/ledger.json',ledger)
    http=None; headers={}; error=None; first=None; start=time.time(); mono=time.monotonic()
    print(aid,'committed; POST starting',flush=True)
    with (d/'raw_stream.sse').open('wb') as out:
        try:
            with opener.open(req,timeout=1800) as resp:
                http=resp.status; headers={k:v for k,v in resp.headers.items() if k.lower() in SAFE_RESPONSE}
                for line in resp:
                    out.write(line); out.flush(); os.fsync(out.fileno())
                    if first is None and b'response.output_text.delta' in line:
                        try:
                            e=json.loads(line.split(b'data:',1)[1])
                            if e.get('delta'):first=time.monotonic()-mono
                        except (ValueError,IndexError):pass
        except urllib.error.HTTPError as e:
            http=e.code; (d/'http_error_body.bin').write_bytes(e.read().replace(key.encode(),b'[REDACTED]'))
            headers={k:v for k,v in e.headers.items() if k.lower() in SAFE_RESPONSE}; error='HTTP_ERROR'
        except Exception as e:error=type(e).__name__
    raw_sse=(d/'raw_stream.sse').read_bytes()
    try:r=base.parse(raw_sse)
    except Exception as e:r={'visible_answer':'','usage':None,'completed':False,'parse_error':type(e).__name__}
    parsed,jstatus,transform=base.collector.parse_answer_text(r['visible_answer'])
    validation=base.collector.validate_answer(parsed,load(base.INPUT/'schemas/biodegradation_answer_v2.schema.json'),check=jstatus=='VALID')
    r.update({'slot':s['slot'],'attempt_id':aid,'case_id':s['case_id'],'requested_model':s['model'],'label':'PILOT_R1','http_status':http,'transport_error':error,'started_unix':start,'ended_unix':time.time(),'duration_seconds':time.monotonic()-mono,'first_visible_seconds':first,'json_status':jstatus,'parser_transform':transform,'schema_status':validation['schema_status'],'visible_characters':len(r['visible_answer']),'sent_request_sha256':sha(req.data),'session_id':s['session_id']})
    (d/'visible_answer.txt').write_text(r.pop('visible_answer'))
    dump(d/'schema_validation.json',validation); dump(d/'safe_response_headers.json',headers); dump(d/'result.json',r)
    stop=gate(r,s['model'],http,error)
    is_model=(http==200 and bool(raw_sse) and any(e.get('type','').startswith('response.') for e in base.events(raw_sse))) if 'parse_error' not in r else bool(raw_sse)
    a.update({'status':'COMPLETE' if r.get('completed') else 'HTTP_ERROR' if http and http!=200 else 'INCOMPLETE_OR_FAILED','http_status':http,'is_model_result':is_model,'result_path':str((d/'result.json').relative_to(W)),'stop_reason':stop,'list_cost':r.get('list_cost'),'cash_cost':r.get('cash_cost'),'allowance':r.get('allowance'),'billing_source':r.get('billing_source')})
    if (d/'http_error_body.bin').exists():
        try:
            error_doc=load(d/'http_error_body.bin'); detail=error_doc.get('error')
            a['error_type']=detail.get('type','UNCLASSIFIED') if isinstance(detail,dict) else 'UNCLASSIFIED'
            if detail=='Invalid request content: A tool_choice was set on the request but no tools were specified.':a['error_type']='EMPTY_TOOLS_TOOL_CHOICE_REJECTED'
        except (ValueError,KeyError,TypeError,AttributeError):a['error_type']='UNCLASSIFIED'
    if stop is None:
        # Verified provider list_cost, not allowance and not cash cost, settles worst reservation.
        ledger['accounted_usd']+=r['list_cost']-a['accounted_usd']; ledger['unknown_reservation_usd']-=a['accounted_usd']
        a['accounted_usd']=r['list_cost']; a['reservation_state']='KNOWN_LIST_COST'
        if r['list_cost']>a['worst_reservation_usd']+1e-9 or ledger['accounted_usd']>2:stop='ACTUAL_COST_EXCEEDS_RESERVATION_OR_CAP'
    if a.get('error_type') in ledger['technical_errors_seen']:stop='SAME_TECHNICAL_ERROR_RECURRED'
    s.update({'status':a['status'],'has_model_result':is_model,'latest_attempt_id':aid,'result_path':a['result_path']})
    if stop:ledger['stop_reason']=stop; a['stop_reason']=stop
    dump(W/'run/ledger.json',ledger)
    print(aid,a['status'],'billing',r.get('billing_source'),'allowance',r.get('allowance'),'list_cost',r.get('list_cost'),'cash',r.get('cash_cost'),'stop',stop,flush=True)
    return r

def run():
    locks=acquire_locks(); ledger=load(W/'run/ledger.json')
    if ledger['stop_reason']:print('Persistent stop:',ledger['stop_reason']); return
    if any(s['status']=='DISPATCH_COMMITTED' for s in ledger['slots']):
        ledger['stop_reason']='COMMITTED_RESULT_UNKNOWN_NO_RESEND'; dump(W/'run/ledger.json',ledger); return
    verify_old()
    assert load(W/'logs/OFFLINE_TEST_RESULTS.json')['passed']
    for rel,digest in load(W/'PRE_DISPATCH_FREEZE.json').items():assert sha((W/rel).read_bytes())==digest,rel
    assert base.identities()==load(W/'INPUT_OUTPUT_IDENTITIES.json')['sources_before']
    keyfile=base.KEY; assert stat.S_IMODE(keyfile.stat().st_mode)==0o600
    assert subprocess.run(['git','ls-files','--error-unmatch',str(keyfile)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
    assert subprocess.run(['git','check-ignore','-q',str(keyfile)]).returncode==0
    key=keyfile.read_text().strip(); assert key
    dump(W/'logs/KEY_HANDLING.json',{'note':'已读取指定密钥文件','mode':'600','git_untracked':True,'local_ignore_hit':True})
    opener=urllib.request.build_opener(base.NoRedirect)
    for s in ledger['slots']:
        if s['status']!='READY':continue
        # Check full original input identities immediately before each new send.
        assert base.identities()==load(W/'INPUT_OUTPUT_IDENTITIES.json')['sources_before']
        dispatch(ledger,s,key,opener)
        if ledger['stop_reason']:break
    # Leak check in the sole process that holds the credential; no digest/prefix is logged.
    leaks=[str(f.relative_to(W)) for f in W.rglob('*') if f.is_file() and key.encode() in f.read_bytes()]
    dump(W/'logs/CREDENTIAL_LEAK_CHECK.json',{'passed':not leaks,'leaking_files':leaks,'secret_or_digest_recorded':False})
    assert not leaks,'Credential found: do not package'

if __name__=='__main__':{'prepare':prepare,'run':run}[sys.argv[1]]()
