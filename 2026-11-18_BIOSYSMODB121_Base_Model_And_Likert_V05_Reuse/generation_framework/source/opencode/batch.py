"""First10 deduplicated batch. Reuses frozen R2 receiver, validator and supervisor."""
import copy,csv,fcntl,json,os,pathlib,stat,subprocess,sys,time,urllib.request,urllib.error,uuid
W=pathlib.Path(__file__).resolve().parents[1];R=W.parent;R2=R/'FOREIGN_NATIVE_GO_PLUS_PILOT_R2_20261109'
sys.path.insert(0,str(R2/'code'));import r2 as core
prior=core.prior;base=core.base;load,dump,sha,compact=prior.load,prior.dump,prior.sha,prior.compact
CARD=R/'07_HPC_Prompts/LOCAL_AI_FOREIGN_NATIVE_GO_PLUS_FIRST10_DEDUP_BATCH_EXECUTOR_ONLY_20261109.md'
CASES=['BIOPATH150_'+f'{n:03}' for n in [1,2,4,5,6,7,8,9,10,11]]
SCHEMA=base.INPUT/'schemas/biodegradation_answer_v2.schema.json'

def manifests():
 out=core.manifests();entries={}
 for line in (R2/'SHA256SUMS').read_text().splitlines():
  h,rel=line.split('  ',1);assert sha((R2/rel).read_bytes())==h,rel;entries[rel]=h
 assert len(entries)==50;out[R2.name]=entries;return out

def locks():
 held=[]
 for folder in [prior.PREV,core.R1,R2,W]:
  f=folder/'run/process.lock';h=f.open('a' if folder==W else 'r');fcntl.flock(h,fcntl.LOCK_EX|fcntl.LOCK_NB);held.append(h)
 return held

def body_for(case,model):
 msgs=load(base.INPUT/'messages'/f'{case}.json')['messages']
 body={'model':model,'input':msgs,'stream':True,'max_output_tokens':65536,'tools':[]}
 if model=='grok-4.7':body['temperature']=0
 else:body['tool_choice']='none'
 return body

def science(case,model,body):
 assert body==body_for(case,model),'SCIENTIFIC_CONFIGURATION_DRIFT'
 return {'endpoint':base.ENDPOINT,'provider_protocol':'Responses streaming','model':model,'messages':body['input'],'prompt_sha256':sha(body['input'][0]['content'].encode()),'schema_sha256':sha(SCHEMA.read_bytes()),'max_output_tokens':65536,'temperature':body.get('temperature','UNSUPPORTED_NOT_SENT'),'top_p':'NOT_SENT','reasoning.effort':'NOT_SENT_EFFECTIVE_DEFAULT_UNOBSERVABLE','tools':[],'tool_choice':body.get('tool_choice','NOT_SENT_EMPTY_TOOLS_DEFAULT_NONE'),'structured_output':'NOT_SENT','system_developer':'NONE'}

def prepare():
 assert not (W/'run/ledger.json').exists(),'Never reset existing ledger'
 held=locks();old=manifests();sources=base.identities();oldledger=load(R2/'run/ledger.json')
 assert oldledger['posts_committed']==6 and abs(oldledger['unknown_reservation_usd']-0.9283297)<1e-10
 sys.path.insert(0,str(prior.PREV/'code'));import replay
 old_by={(s['case_id'],s['model']):s for s in oldledger['slots']}
 slots=[];metadata=load(R2/'PILOT_CONFIG.json')['metadata']
 for case in CASES:
  for model in base.MODELS:
   body=body_for(case,model);raw=compact(body);cfg=science(case,model,body);digest=sha(compact(cfg));key=case+'|'+model+'|'+digest
   oldslot=old_by.get((case,model));slot=f'FIRST10-{len(slots)+1:03}'
   s={'slot':slot,'case_id':case,'model':model,'scientific_request_config_sha256':digest,'dedup_key':key,'scientific_config':cfg,'request_sha256':sha(raw),'session_id':oldslot['session_id'] if oldslot else str(uuid.uuid4()),'attempt_ids':copy.deepcopy(oldslot['attempt_ids']) if oldslot else [],'status':'NEW_UNSUBMITTED'}
   if oldslot:
    r=load(oldslot['result_path']);d=pathlib.Path(oldslot['result_path']).parent;actual=load(d/'request_body.json');assert science(case,model,actual)==cfg
    v=replay.replay((d/'raw_stream.sse').read_bytes());assert v['usage']==r['usage'] and v['terminal']==r['terminal'] and v['visible_answer']==(d/'visible_answer.txt').read_text()
    s['source_result_path']=oldslot['result_path'];s['source_attempt']=oldslot['attempt_ids'][-1]
    if oldslot['status']=='COMPLETE':
     assert v['terminal']=='response.completed' and r['model']==model and prior.gate(r,model,200) is None
     parsed,js,tr=base.collector.parse_answer_text(v['visible_answer']);val=base.collector.validate_answer(parsed,load(SCHEMA),check=js=='VALID');assert val['schema_status']==r['schema_status']
     s['status']='PILOT_REUSED'
    else:assert oldslot['status']=='RESULT_UNKNOWN';s['status']='HISTORICAL_UNKNOWN_FROZEN'
   else:
    d=W/'run'/slot;d.mkdir(parents=True,exist_ok=True);(d/'request_body.json').write_bytes(raw)
    upper=len(body['input'][0]['content'].encode())+4096;prices=metadata[model]['cost']['text'];ip=max(prices['input']['price'],prices['input'].get('cache',{}).get('write',0));context=upper+65536
    assert context<(200000 if model=='grok-4.7' else 272000)
    s.update({'input_token_upper':upper,'context_upper':context,'worst_list_reservation_usd':(upper*ip+65536*prices['output']['price'])/1e6})
    s['allowance_reservation_usd']=4*s['worst_list_reservation_usd']
   slots.append(s)
 assert sum(s['status']=='PILOT_REUSED' for s in slots)==3 and sum(s['status']=='HISTORICAL_UNKNOWN_FROZEN' for s in slots)==1
 ledger={'posts_committed':6,'new_posts':0,'accounted_usd':oldledger['accounted_usd'],'unknown_usd':oldledger['unknown_reservation_usd'],'stage_allowance_accounted':{m:0 for m in base.MODELS},'stage_known_list':{m:0 for m in base.MODELS},'stage_known_allowance':{m:0 for m in base.MODELS},'stage_known_cash':{m:0 for m in base.MODELS},'stop_reason':None,'slots':slots,'historical_attempts':oldledger['attempts'],'new_attempts':[]}
 dump(W/'CARRY_IN.json',{'old_ledger':oldledger,'manifests':old,'posts':6,'known_list_cost':0.07785298,'known_allowance':0.3114119,'known_cash':0,'unknown_list_reservation':0.9283297,'unknown_allowance_and_cash':'unknown'})
 dump(W/'FROZEN_TARGETS.json',slots);dump(W/'run/ledger.json',ledger);dump(W/'INPUT_OUTPUT_IDENTITIES.json',{'sources_before':sources,'manifests':old})
 dump(W/'EXTRA_USAGE_CONFIRMATION.json',{'source':'actual user reply to execution window question','user_reply':'已查看，Extra Usage 已关闭','observed_by':'user; not independently read via API','recorded_unix':time.time(),'confirmed_disabled':True,'settings_modified_by_executor':False})
 dump(W/'AUTHORIZATION_SCOPE.json',{'card':str(CARD),'card_sha256':sha(CARD.read_bytes()),'user_handoff':True,'new_post_cap':16,'cumulative_post_cap':22,'list_cap_usd':6,'stage_allowance_cap_per_model_usd':4,'allowance_reservation_multiplier_assumption':4,'cash_authorized':False,'full_run_authorized':False})
 dump(W/'PILOT_CONFIG.json',{'endpoint':base.ENDPOINT,'timeout_seconds':1800,'timeout_kind':'socket operation; no visible-text deadline','concurrency':1,'worker_restarts':0,'metadata':metadata,'case_order':CASES,'model_order':base.MODELS,'limits':load(W/'AUTHORIZATION_SCOPE.json'),'estimate_is_not_guarantee':True})
 print('20 targets frozen: 3 reused,1 unknown frozen,16 new; Extra Usage user confirmed off')

def request(s):
 raw=(W/'run'/s['slot']/'request_body.json').read_bytes();body=json.loads(raw)
 assert sha(raw)==s['request_sha256'] and sha(compact(science(s['case_id'],s['model'],body)))==s['scientific_request_config_sha256']
 assert s['session_id'].strip()
 return raw

def can_send(l,s):
 assert s['status']=='NEW_UNSUBMITTED' and not s['attempt_ids'],'DEDUP_ALREADY_SUBMITTED_OR_REUSED'
 assert not l['stop_reason'] and l['posts_committed']<22 and l['new_posts']<16,'POST_CAP_OR_STOP'
 assert l['accounted_usd']+s['worst_list_reservation_usd']<=6,'LIST_BUDGET_CAP'
 assert l['stage_allowance_accounted'][s['model']]+s['allowance_reservation_usd']<=4,'MODEL_STAGE_ALLOWANCE_CAP'

def dispatch(l,s,key,opener):
 can_send(l,s);raw=request(s)
 req=urllib.request.Request(base.ENDPOINT,data=raw,method='POST',headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','Accept':'text/event-stream','User-Agent':prior.UA,'x-opencode-session':s['session_id']})
 assert req.get_header('X-opencode-session') and req.data==raw
 aid=s['slot']+'-A01';d=W/'run'/s['slot']/aid;d.mkdir(exist_ok=False);(d/'request_body.json').write_bytes(raw)
 dump(d/'safe_request_headers.json',{k:v for k,v in req.header_items() if k.lower() in prior.SAFE_REQUEST})
 a={'attempt_id':aid,'slot':s['slot'],'case_id':s['case_id'],'model':s['model'],'dedup_key':s['dedup_key'],'status':'DISPATCH_COMMITTED','commit_unix':time.time(),'request_sha256':sha(raw),'session_id':s['session_id'],'list_accounted':s['worst_list_reservation_usd'],'allowance_accounted':s['allowance_reservation_usd'],'reservation_state':'UNKNOWN'}
 s['status']='DISPATCH_COMMITTED';s['attempt_ids'].append(aid);l['new_attempts'].append(a);l['posts_committed']+=1;l['new_posts']+=1;l['accounted_usd']+=a['list_accounted'];l['unknown_usd']+=a['list_accounted'];l['stage_allowance_accounted'][s['model']]+=a['allowance_accounted'];dump(W/'run/ledger.json',l)
 life={'worker_pid':os.getpid(),'request_started_unix':time.time(),'phase':'WAITING_HEADERS','bytes_received':0,'event_count':0,'timeout_seconds':1800,'timeout_kind':'socket operation'};dump(d/'lifecycle.json',life);(d/'raw_stream.sse').touch();error=None
 print(aid,s['case_id'],s['model'],'COMMITTED',flush=True)
 try:
  with opener.open(req,timeout=1800) as resp:core.receive(resp,d,life)
 except urllib.error.HTTPError as e:
  error='HTTP_ERROR';life.update({'http_status':e.code,'safe_headers':{k:v for k,v in e.headers.items() if k.lower() in prior.SAFE_RESPONSE},'headers_received_unix':time.time(),'stream_closed_unix':time.time(),'phase':'HTTP_ERROR'});dump(d/'lifecycle.json',life);(d/'http_error_body.bin').write_bytes(e.read().replace(key.encode(),b'[REDACTED]'))
 except Exception as e:error=type(e).__name__;life.update({'exception_class':error,'phase':'TRANSPORT_UNKNOWN','stream_closed_unix':time.time()});dump(d/'lifecycle.json',life)
 r=core.materialize(d,s,a,life,error);r['label']='FIRST10_DEDUP_NEW';dump(d/'result.json',r);stop=prior.gate(r,s['model'],life.get('http_status'),error)
 if stop is None:
  if r['list_cost']>s['worst_list_reservation_usd']+1e-8 or r['allowance']>s['allowance_reservation_usd']+1e-7 or r['allowance']>r['list_cost']*4+max(1e-7,r['list_cost']*0.0001):stop='USAGE_OR_MULTIPLIER_EXCEEDS_RESERVATION'
  l['accounted_usd']+=r['list_cost']-a['list_accounted'];l['unknown_usd']-=a['list_accounted'];l['stage_allowance_accounted'][s['model']]+=r['allowance']-a['allowance_accounted']
  a.update({'list_accounted':r['list_cost'],'allowance_accounted':r['allowance'],'reservation_state':'KNOWN'})
  for k,name in [('list_cost','stage_known_list'),('allowance','stage_known_allowance'),('cash_cost','stage_known_cash')]:l[name][s['model']]+=r[k]
 a.update({'status':'COMPLETE' if r.get('completed') else 'INCOMPLETE_OR_ERROR','result_path':str(d/'result.json'),'stop_reason':stop,**{k:r.get(k) for k in ['http_status','list_cost','allowance','cash_cost','billing_source']}});s.update({'status':a['status'],'result_path':a['result_path']})
 if stop:l['stop_reason']=stop
 dump(W/'run/ledger.json',l);print(aid,a['status'],'list',r.get('list_cost'),'allowance',r.get('allowance'),'cash',r.get('cash_cost'),'STOP',stop,flush=True)

def worker():
 held=locks();l=load(W/'run/ledger.json')
 if l['stop_reason']:return
 if any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']):l['stop_reason']='COMMITTED_RESULT_UNKNOWN_NO_RESEND';dump(W/'run/ledger.json',l);return
 manifests();assert load(W/'EXTRA_USAGE_CONFIRMATION.json')['confirmed_disabled'];assert load(W/'logs/OFFLINE_TEST_RESULTS.json')['passed']
 for rel,h in load(W/'PRE_DISPATCH_FREEZE.json').items():assert sha((W/rel).read_bytes())==h,rel
 dump(W/'logs/worker.json',{'pid':os.getpid(),'start_unix':time.time(),'locks':'R0,R1,R2,FIRST10 process.lock held','restart':False})
 assert stat.S_IMODE(base.KEY.stat().st_mode)==0o600
 assert subprocess.run(['git','check-ignore','-q',str(base.KEY)]).returncode==0
 assert subprocess.run(['git','ls-files','--error-unmatch',str(base.KEY)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
 key=base.KEY.read_text().strip();assert key;opener=urllib.request.build_opener(base.NoRedirect)
 for s in l['slots']:
  if s['status']!='NEW_UNSUBMITTED':continue
  assert base.identities()==load(W/'INPUT_OUTPUT_IDENTITIES.json')['sources_before']
  try:can_send(l,s)
  except AssertionError as e:l['stop_reason']=str(e);dump(W/'run/ledger.json',l);break
  dispatch(l,s,key,opener)
  if l['stop_reason']:break
 leaks=[str(f.relative_to(W)) for f in W.rglob('*') if f.is_file() and key.encode() in f.read_bytes()]
 dump(W/'logs/CREDENTIAL_HANDLING.json',{'note':'已读取指定密钥文件','mode_600_untracked_ignored':True,'leak_check_passed':not leaks,'key_or_digest_recorded':False});assert not leaks

def supervise():
 core.W=W;core.supervise([sys.executable,'-B',str(pathlib.Path(__file__).resolve()),'worker'])
if __name__=='__main__':{'prepare':prepare,'worker':worker,'supervise':supervise}[sys.argv[1]]()
