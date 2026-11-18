"""R2: reuse R1 protocol, new supervised lifecycle; no worker retries."""
import copy,fcntl,json,os,pathlib,signal,stat,subprocess,sys,time,urllib.request,urllib.error
W=pathlib.Path(__file__).resolve().parents[1]; R=W.parent; R1=R/'FOREIGN_NATIVE_GO_PLUS_PILOT_R1_20261109'
sys.path.insert(0,str(R1/'code')); import r1_runner as prior
base=prior.base; load,dump,sha=prior.load,prior.dump,prior.sha
CARD=R/'07_HPC_Prompts/LOCAL_AI_FOREIGN_NATIVE_GO_PLUS_PILOT_R2_FAST_REPAIR_AND_REMAINING2_EXECUTE_20261109.md'
def manifests():
    out={}
    for folder,n in [(prior.PREV,38),(R1,81)]:
        entries={}
        for line in (folder/'SHA256SUMS').read_text().splitlines():
            h,rel=line.split('  ',1); assert sha((folder/rel).read_bytes())==h,rel; entries[rel]=h
        assert len(entries)==n;out[folder.name]=entries
    assert base.identities()==load(R1/'INPUT_OUTPUT_IDENTITIES.json')['sources_before']
    return out

def locks():
    handles=[]
    for f in [prior.PREV/'run/process.lock',R1/'run/process.lock',W/'run/process.lock']:
        h=f.open('a' if f.parent.parent==W else 'r'); fcntl.flock(h,fcntl.LOCK_EX|fcntl.LOCK_NB); handles.append(h)
    return handles

def prepare():
    assert not (W/'run/ledger.json').exists()
    held=locks(); before=manifests(); l=load(R1/'run/ledger.json')
    assert l['posts_committed']==4 and abs(l['unknown_reservation_usd']-0.9283297)<1e-10
    dump(W/'CARRY_IN.json',{'ledger':l,'manifests':before,'known_list_cost_usd':0.00173155,'unknown_usd':0.9283297,'old_stop_preserved':l['stop_reason']})
    l=copy.deepcopy(l);l['r2_posts']=0;l['stop_reason']=None;l['r2_allowed_slots']=['GO-P003','GO-P004']
    for a in l['attempts']:
        if a.get('result_path'):a['result_path']=str(R1/a['result_path'])
    for s in l['slots']:
        if s.get('result_path'):s['result_path']=str(R1/s['result_path'])
        if s['slot'] in l['r2_allowed_slots']:
            assert s['status']=='READY' and not s['attempt_ids'];d=W/'run'/s['slot'];d.mkdir(parents=True,exist_ok=True)
            raw=prior.request_bytes(s);(d/'request_body.json').write_bytes(raw)
            s['r2_request_sha256']=sha(raw)
    dump(W/'run/ledger.json',l)
    dump(W/'AUTHORIZATION_SCOPE.json',{'task_id':'FOREIGN_NATIVE_GO_PLUS_PILOT_R2_FAST_REPAIR_AND_REMAINING2','card':str(CARD),'card_sha256':sha(CARD.read_bytes()),'actual_user_handoff':True,'only_slots':['GO-P003','GO-P004'],'old_stop':load(R1/'run/ledger.json')['stop_reason'],'specific_continuation':True,'post_cap':6,'new_post_cap':2,'list_cap_usd':2,'cash_authorized':False,'full_run_authorized':False})
    dump(W/'PILOT_CONFIG.json',{'endpoint':base.ENDPOINT,'timeout_seconds':1800,'timeout_kind':'urllib socket operations timeout, not a no-visible-output deadline; continuous data may extend total duration','worker_restarts':0,'supervisor_poll_seconds':2,'progress_seconds':5,'post_cap':6,'new_post_cap':2,'list_cap_usd':2,'all_session_ids':{s['slot']:s['session_id'] for s in l['slots']},'metadata':load(R1/'PILOT_CONFIG.json')['metadata'],'regular_worst_including_carry_usd':l['accounted_usd']+sum(s['worst_list_cost_usd'] for s in l['slots'] if s['slot'] in l['r2_allowed_slots'])})
    dump(W/'INPUT_OUTPUT_IDENTITIES.json',{'sources_before':base.identities(),'previous_manifests':before})
    print('Prepared R2; carry POST4, unknown 0.9283297; two targets only')

def can_commit(l,s):
    assert s['slot'] in ['GO-P003','GO-P004'] and s['status']=='READY' and not s['attempt_ids'],'NO_REENTRY'
    assert not l['stop_reason'] and l['posts_committed']<6 and l['r2_posts']<2,'POST_CAP_OR_STOP'
    assert l['accounted_usd']+s['worst_list_cost_usd']<=2,'USD_CAP'

def receive(resp,d,life):
    life.update({'http_status':resp.status,'safe_headers':{k:v for k,v in resp.headers.items() if k.lower() in prior.SAFE_RESPONSE},'headers_received_unix':time.time(),'phase':'WAITING_EVENTS'})
    dump(d/'lifecycle.json',life)
    data=[];last_save=0;terminal=False;first=None
    with (d/'raw_stream.sse').open('wb') as f:
        for line in resp:
            f.write(line);f.flush();os.fsync(f.fileno());now=time.time()
            life['bytes_received']=life.get('bytes_received',0)+len(line);life['last_byte_unix']=now
            stripped=line.rstrip(b'\r\n')
            if stripped.startswith(b'data:'):data.append(stripped[5:].lstrip(b' '))
            if not stripped and data:
                payload=b'\n'.join(data);data=[]
                if payload!=b'[DONE]':
                    try:e=json.loads(payload)
                    except ValueError:e={}
                    typ=e.get('type','');life['event_count']=life.get('event_count',0)+1
                    if typ=='response.created':
                        r=e.get('response',{});life.update({'response_id':r.get('id'),'response_model':r.get('model'),'response_created_unix':now});dump(d/'response_created.json',e)
                    if 'reasoning' in typ:life['phase']='REASONING'
                    if typ=='response.output_text.delta' and e.get('delta'):
                        life['phase']='VISIBLE_OUTPUT'
                        if first is None:first=now-life['request_started_unix'];life['first_visible_seconds']=first
                    if typ in ['response.completed','response.incomplete','response.failed']:
                        terminal=True;life['phase']=typ;life['terminal_received_unix']=now
                        dump(d/'terminal_event.json',e) # persist final usage immediately
                    if typ=='response.created' or terminal:dump(d/'lifecycle.json',life)
            if now-last_save>=5:
                dump(d/'lifecycle.json',life);last_save=now
    life['stream_closed_unix']=time.time();dump(d/'lifecycle.json',life)
    return first

def materialize(d,s,a,life,error):
    raw=(d/'raw_stream.sse').read_bytes() if (d/'raw_stream.sse').exists() else b''
    try:r=base.parse(raw)
    except Exception as e:r={'visible_answer':'','usage':None,'completed':False,'parse_error':type(e).__name__}
    parsed,js,transform=base.collector.parse_answer_text(r['visible_answer'])
    validation=base.collector.validate_answer(parsed,load(base.INPUT/'schemas/biodegradation_answer_v2.schema.json'),check=js=='VALID')
    r.update({'slot':s['slot'],'case_id':s['case_id'],'attempt_id':a['attempt_id'],'requested_model':s['model'],'label':'PILOT_R2','http_status':life.get('http_status'),'transport_error':error,'started_unix':life['request_started_unix'],'ended_unix':life.get('stream_closed_unix'),'duration_seconds':life.get('stream_closed_unix',time.time())-life['request_started_unix'],'first_visible_seconds':life.get('first_visible_seconds'),'json_status':js,'schema_status':validation['schema_status'],'parser_transform':transform,'visible_characters':len(r['visible_answer']),'session_id':s['session_id'],'sent_request_sha256':a['request_sha256']})
    (d/'visible_answer.txt').write_text(r.pop('visible_answer'));dump(d/'result.json',r);dump(d/'schema_validation.json',validation)
    return r

def dispatch(l,s,key,opener):
    can_commit(l,s);raw=(W/'run'/s['slot']/'request_body.json').read_bytes()
    assert sha(raw)==s['r2_request_sha256'] and raw==prior.request_bytes(s)
    req=prior.build_request(s,raw,key)
    aid='R2-'+s['slot']+'-A01';d=W/'run'/s['slot']/aid;d.mkdir(exist_ok=False)
    (d/'request_body.json').write_bytes(raw);dump(d/'safe_request_headers.json',{k:v for k,v in req.header_items() if k.lower() in prior.SAFE_REQUEST})
    a={'attempt_id':aid,'slot':s['slot'],'status':'DISPATCH_COMMITTED','request_sha256':sha(raw),'session_id':s['session_id'],'worst_reservation_usd':s['worst_list_cost_usd'],'accounted_usd':s['worst_list_cost_usd'],'reservation_state':'UNKNOWN','commit_unix':time.time()}
    s['status']='DISPATCH_COMMITTED';s['attempt_ids'].append(aid);l['attempts'].append(a);l['posts_committed']+=1;l['r2_posts']+=1;l['accounted_usd']+=a['accounted_usd'];l['unknown_reservation_usd']+=a['accounted_usd'];dump(W/'run/ledger.json',l)
    life={'worker_pid':os.getpid(),'request_started_unix':time.time(),'phase':'WAITING_HEADERS','bytes_received':0,'event_count':0,'timeout_seconds':1800,'timeout_kind':'socket operation'};dump(d/'lifecycle.json',life)
    (d/'raw_stream.sse').touch();error=None
    print(aid,'COMMITTED',flush=True)
    try:
        with opener.open(req,timeout=1800) as resp:receive(resp,d,life)
    except urllib.error.HTTPError as e:
        error='HTTP_ERROR';life.update({'http_status':e.code,'headers_received_unix':time.time(),'safe_headers':{k:v for k,v in e.headers.items() if k.lower() in prior.SAFE_RESPONSE},'phase':'HTTP_ERROR','stream_closed_unix':time.time()})
        dump(d/'lifecycle.json',life);(d/'http_error_body.bin').write_bytes(e.read().replace(key.encode(),b'[REDACTED]'))
    except Exception as e:
        error=type(e).__name__;life.update({'phase':'TRANSPORT_UNKNOWN','exception_class':error,'stream_closed_unix':time.time()});dump(d/'lifecycle.json',life)
    r=materialize(d,s,a,life,error);stop=prior.gate(r,s['model'],life.get('http_status'),error)
    if stop is None:
        l['accounted_usd']+=r['list_cost']-a['accounted_usd'];l['unknown_reservation_usd']-=a['accounted_usd'];a['accounted_usd']=r['list_cost'];a['reservation_state']='KNOWN_LIST_COST'
        if r['list_cost']>a['worst_reservation_usd']+1e-9:stop='RESERVATION_EXCEEDED'
    a.update({'status':'COMPLETE' if r.get('completed') else 'INCOMPLETE_OR_ERROR','result_path':str(d/'result.json'),'stop_reason':stop,**{k:r.get(k) for k in ['list_cost','cash_cost','allowance','billing_source','http_status']}})
    s.update({'status':a['status'],'result_path':a['result_path'],'has_model_result':r.get('terminal') is not None})
    if stop:l['stop_reason']=stop
    dump(W/'run/ledger.json',l);print(aid,a['status'],r.get('billing_source'),r.get('list_cost'),r.get('allowance'),r.get('cash_cost'),'STOP',stop,flush=True)

def worker():
    held=locks();l=load(W/'run/ledger.json')
    if l['stop_reason']:return
    assert not any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']),'Never replay committed request'
    assert load(W/'logs/OFFLINE_TEST_RESULTS.json')['passed']
    for rel,h in load(W/'PRE_DISPATCH_FREEZE.json').items():assert sha((W/rel).read_bytes())==h,rel
    manifests();dump(W/'logs/worker.json',{'pid':os.getpid(),'start_unix':time.time(),'lock_paths':[str(prior.PREV/'run/process.lock'),str(R1/'run/process.lock'),str(W/'run/process.lock')],'automatic_restart':False})
    assert stat.S_IMODE(base.KEY.stat().st_mode)==0o600
    assert subprocess.run(['git','check-ignore','-q',str(base.KEY)]).returncode==0
    assert subprocess.run(['git','ls-files','--error-unmatch',str(base.KEY)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
    key=base.KEY.read_text().strip();assert key
    opener=urllib.request.build_opener(base.NoRedirect)
    for s in l['slots']:
        if s['slot'] not in l['r2_allowed_slots'] or s['status']!='READY':continue
        assert base.identities()==load(W/'INPUT_OUTPUT_IDENTITIES.json')['sources_before']
        dispatch(l,s,key,opener)
        if l['stop_reason']:break
    leaks=[str(f.relative_to(W)) for f in W.rglob('*') if f.is_file() and key.encode() in f.read_bytes()]
    dump(W/'logs/CREDENTIAL_HANDLING.json',{'note':'已读取指定密钥文件','mode_600_untracked_ignored':True,'leak_check_passed':not leaks,'key_or_digest_recorded':False});assert not leaks

def supervise(command=None):
    # A separate session-owned monitor survives loss of a tool wait handle. Never restarts the worker.
    lock=(W/'run/supervisor.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    info={'pid':os.getpid(),'start_unix':time.time(),'worker_restarts':0,'status':'RUNNING'}
    with (W/'logs/worker.stdout.log').open('ab') as out:
        proc=subprocess.Popen(command or [sys.executable,'-B',str(pathlib.Path(__file__).resolve()),'worker'],stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
        info['worker_pid']=proc.pid;dump(W/'logs/supervisor.json',info)
        while proc.poll() is None:
            info['last_monitor_unix']=time.time();dump(W/'logs/supervisor.json',info);time.sleep(2)
        info.update({'status':'EXITED','returncode':proc.returncode,'signal':-proc.returncode if proc.returncode<0 else None,'end_unix':time.time()})
        stages={}
        for f in W.glob('run/*/*/lifecycle.json'):stages[str(f.relative_to(W))]=load(f)
        info['final_lifecycles']=stages;dump(W/'logs/supervisor.json',info)

if __name__=='__main__':{'prepare':prepare,'worker':worker,'supervise':supervise}[sys.argv[1]]()
