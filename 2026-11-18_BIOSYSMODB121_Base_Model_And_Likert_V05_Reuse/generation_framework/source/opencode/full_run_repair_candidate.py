"""Foreign full continuation. Supplement 2026-11-10 (AUTONOMOUS_TRANSIENT_RECOVERY_AND_QUEUE_CONTINUE):
bounded automatic backoff for explicit service-capacity rejects; a single local unknown freezes only itself
and the queue continues independent unsubmitted targets; account-quota/cost/identity anomalies still global
save-exit awaiting the user. Original questions/models/science/budget caps unchanged (35 USD list cap;
phase POSTs <=246 incl. shared technical-replacement pool <=24; cumulative commits <=270)."""
import copy,csv,fcntl,json,os,pathlib,stat,subprocess,sys,threading,time,traceback,urllib.request,urllib.error,uuid
from email.utils import parsedate_to_datetime
W=pathlib.Path(__file__).resolve().parents[1];R=W.parent
BATCH=R/'FOREIGN_NATIVE_GO_PLUS_FIRST10_BATCH_20261109'
RESUME=R/'FOREIGN_NATIVE_GO_PLUS_FIRST10_RESUME_20261109'
RETRY=R/'FOREIGN_NATIVE_GO_PLUS_FIRST10_USER_RETRY_20261109'
NETFIX=R/'FOREIGN_NATIVE_GO_PLUS_FIRST10_NETFIX_20261109'
sys.path.insert(0,str(BATCH/'code'));import batch as engine
base=engine.base;core=engine.core;prior=engine.prior
load,dump,sha,compact=base.load,base.dump,base.sha,base.compact
CARD=R/'07_HPC_Prompts/LOCAL_AI_FOREIGN_NATIVE_GO_PLUS_FULL_REMAINING111_QUOTA_AWARE_EXECUTOR_ONLY_20261109.md'
SUPPLEMENT=R/'07_HPC_Prompts/LOCAL_AI_FOREIGN_NATIVE_GO_PLUS_AUTONOMOUS_TRANSIENT_RECOVERY_AND_QUEUE_CONTINUE_20261110.md'
REVIEW=R/'04_Local_Review_Audits/FOREIGN_NATIVE_GO_PLUS_CAPACITY_AND_QUEUE_REVIEW_20261110/REVIEW.md'
INDEX=R/'BASE_MODEL_EXTENSION_PREP_20261109/FROZEN_QUESTION_INDEX_121.tsv'
INDEX_ROWS=list(csv.DictReader(INDEX.open(),delimiter='\t'))
CASE_IDS=[r['case_id'] for r in INDEX_ROWS];CASE_ID_SET=set(CASE_IDS)
TASK_ID='FOREIGN_NATIVE_GO_PLUS_FULL_REMAINING111_QUOTA_AWARE'
DISPATCH_ORDER=['grok-4.7','gpt-6-luna']
CAP_COMMITS_TOTAL=270;CAP_PHASE_POSTS=246;CAP_TECH_POOL=24;CAP_CAPACITY_PER_TARGET=3;CAP_QUOTA_PER_TARGET=1;CAP_LIST_USD=35.0
CAPACITY_BACKOFF_SECONDS=[120,300,600];GLOBAL_COOLDOWN_SECONDS=900;STREAK_COOLDOWN=5;STREAK_EXIT=10;UNKNOWN_STREAK_EXIT=10
CARRY_COMMITS=24;CARRY_ACCOUNTED=3.3921622399999993;CARRY_UNKNOWN=1.8213977
CARRY_KNOWN_LIST=1.57076454;CARRY_KNOWN_ALLOWANCE=6.2830580000000005;CARRY_KNOWN_CASH=0
CHECKPOINT_EVERY=10;CUM30_NEW_TARGETS=40
# Concurrency per explicit user instruction 2026-11-10 15:0x ('能不能并发4个'); after first account-quota 429 at 15:15 the user set '继续2个试试 2个应该没问题吧 或者三个' -> total 2 in-flight. Science/dedup/budget/stop gates unchanged.
CONCURRENCY=5;MAX_INFLIGHT_PER_MODEL={'grok-4.7':4,'gpt-6-luna':1}
# Luna per-minute token rate limit observed 2026-11-10 (HTTP429 'Token rate limit exceeded', 46ms edge reject, zero tokens): pace Luna commits and cap Luna in-flight at 1. Account windows were healthy (rolling 22%).
LUNA_MIN_INTERVAL_SECONDS=60
def luna_paced(l):return NOW()-l.get('last_commit_unix',{}).get('gpt-6-luna',0)<LUNA_MIN_INTERVAL_SECONDS
_IDCHECK={'bucket':-1,'val':None}
def inputs_unchanged(l):
 # full source-identity hash verified at worker start and re-verified every 10 commits (per-dispatch hashing starves the loop)
 b=l['commits_total']//10
 if _IDCHECK['bucket']!=b:
  _IDCHECK['val']=base.identities()==load(W/'INPUT_OUTPUT_IDENTITIES.json')['sources_before'];_IDCHECK['bucket']=b
 return _IDCHECK['val']
def stop_requested():return (W/'STOP_REQUEST').exists()
KEY2=pathlib.Path('/home/a/EnzymeCAGE/opencode_luna_api_key.txt')
SOURCE_A='ORIGINAL_ACCOUNT_A';SOURCE_B='LUNA_ACCOUNT_B'
def luna_key_available():return KEY2.exists() and KEY2.read_text().strip()!=''
def luna_key():
 return KEY2.read_text().strip() if luna_key_available() else None
def external_hold(s):return (W/'EXTERNAL_LUNA_HOLD').exists() and s['model']=='gpt-6-luna'
def NOW():return time.time()
QUOTA_PATTERNS=['quota','rate limit','rate_limit','too many requests','throttl','insufficient','exhaust','usage limit','limit reached','allowance','out of funds','billing','payment']
CAPACITY_PATTERNS=['at capacity','high demand','overloaded','currently at capacity']

def manifests():
 out=engine.manifests()
 entries={}
 for line in (BATCH/'SHA256SUMS').read_text().splitlines():
  h,rel=line.split('  ',1);assert sha((BATCH/rel).read_bytes())==h,rel;entries[rel]=h
 assert len(entries)==117;out[BATCH.name]=entries
 entries={}
 for line in (NETFIX/'SHA256SUMS').read_text().splitlines():
  h,rel=line.split('  ',1);assert sha((NETFIX/rel).read_bytes())==h,rel;entries[rel]=h
 assert len(entries)==125;out[NETFIX.name]=entries
 for folder,hashes in [(RETRY,load(NETFIX/'CARRY_IN.json')['resume_source_hashes']),(RESUME,load(RETRY/'CARRY_IN.json')['resume_source_hashes'])]:
  entries={}
  for rel,h in hashes.items():assert sha((folder/rel).read_bytes())==h,folder.name+'/'+rel;entries[rel]=h
  out[folder.name]=entries
 identities_now=base.identities()
 for snapshot in [NETFIX/'INPUT_OUTPUT_IDENTITIES.json',NETFIX/'INPUT_OUTPUT_IDENTITIES_FINAL.json']:
  s=load(snapshot)
  assert identities_now==s['sources_before'] and identities_now==s.get('sources_after',s['sources_before']),snapshot
 return out

def locks():
 held=[]
 for folder in [prior.PREV,core.R1,engine.R2,BATCH,RESUME,RETRY,NETFIX,W]:
  f=folder/'run/process.lock';h=f.open('a' if folder==W else 'r');fcntl.flock(h,fcntl.LOCK_EX|fcntl.LOCK_NB);held.append(h)
 return held

def body_for(case,model):return engine.body_for(case,model)
def science(case,model,body):return engine.science(case,model,body)

def request(s):
 raw=(W/'run'/s['slot']/'request_body.json').read_bytes();body=json.loads(raw)
 assert s['model'] in base.MODELS and body['model']==s['model'],'SEND_BOUNDARY_MODEL_WHITELIST'
 assert base.ENDPOINT=='https://opencode.ai/inference/go/openai/v1/responses','SEND_BOUNDARY_ENDPOINT'
 assert sha(raw)==s['request_sha256'] and sha(compact(science(s['case_id'],s['model'],body)))==s['scientific_request_config_sha256']
 assert s['session_id'].strip(),'SESSION_REQUIRED_BEFORE_POST'
 return raw

def can_send(l,s):
 assert not l['stop_reason'],'PERSISTENT_STOP'
 assert s['case_id'] in CASE_ID_SET and s['model'] in base.MODELS,'OUT_OF_FROZEN_SCOPE'
 if s.get('quota_pending'):
  assert s['status']=='QUOTA_REJECTED','QUOTA_REPLACEMENT_STATE'
  assert s['quota_replacements_used']<CAP_QUOTA_PER_TARGET,'QUOTA_REPLACEMENT_ALREADY_USED'
  assert l['quota_recovery_posts']<CAP_TECH_POOL,'TECH_REPLACEMENT_POOL_24'
 elif s['status']=='DEFERRED_CAPACITY':
  # CAP_CAPACITY_PER_TARGET=3 replacements => at most 4 POSTs (initial + 3); attempts counts rejections so far.
  assert s['capacity_attempts']<CAP_CAPACITY_PER_TARGET+1,'CAPACITY_ATTEMPTS_EXHAUSTED'
  assert NOW()>=s['next_eligible_at_unix'],'CAPACITY_BACKOFF_NOT_ELAPSED'
  assert l['quota_recovery_posts']<CAP_TECH_POOL,'TECH_REPLACEMENT_POOL_24'
 else:
  assert s['status']=='ELIGIBLE_UNSUBMITTED' and not s['attempt_ids'],'DEDUP_ALREADY_SUBMITTED_OR_REUSED'
 assert l['commits_total']<CAP_COMMITS_TOTAL,'COMMIT_CAP_270'
 assert l['phase_posts']<CAP_PHASE_POSTS,'PHASE_POST_CAP_246'
 assert l['accounted_usd']+l.get('sourceB_accounted_usd',0.0)+s['worst_list_reservation_usd']<=CAP_LIST_USD,'LIST_BUDGET_CAP_35'

def retry_after_unix(raw):
 if raw is None:return None
 try:return NOW()+float(raw)
 except ValueError:
  try:return parsedate_to_datetime(raw).timestamp()
  except Exception:return None

ACCOUNT_PATTERNS=['quota','plan','billing','payment','insufficient','allowance','out of funds','usage limit','credit']
MODEL_RATE_BACKOFF_SECONDS=[1800,3600,7200]
def classify_reject(r,life,error,d,http_body):
 # A 'service_capacity' requires: HTTP200 in-stream error frame or HTTP503, explicit upstream capacity wording, and NO reasoning/body/tool/refusal/nonempty output/terminal/positive usage.
 raw=(d/'raw_stream.sse').read_bytes() if (d/'raw_stream.sse').exists() else b''
 low=raw.lower()
 has_progress=bool(r.get('terminal') or r.get('usage') or r.get('visible_characters') or r.get('tool_call_detected') or b'reasoning' in low)
 http=life.get('http_status')
 if http==403:return 'account_quota'
 if http==429:
  t429=(http_body or '').lower()
  if any(k in t429 for k in ACCOUNT_PATTERNS):return 'account_quota'
  if ('rate limit' in t429 or 'too_many_requests' in t429) and not (r.get('terminal') or r.get('usage') or r.get('visible_characters')):return 'model_rate_limit'
  return 'account_quota'
 text=(http_body or '').lower()
 if http==503 and not has_progress and any(k in text for k in CAPACITY_PATTERNS):return 'service_capacity'
 if http==200 and error is None and not has_progress:
  evs=[]
  try:evs=[e for e in base.events(raw)]
  except Exception:pass
  msg=' '.join(str(e.get('message','')) for e in evs if e.get('type')=='error').lower()
  if msg and any(k in msg for k in CAPACITY_PATTERNS):return 'service_capacity'
  if msg and any(k in msg for k in QUOTA_PATTERNS):return 'account_quota'
 return None

LOCAL_STOPS={'HTTP_SERVICE_ERROR','TRANSPORT_UNKNOWN','SERVICE_FAILED_OR_TERMINAL_UNKNOWN'}
def dispatch_commit(l,s,key,source=SOURCE_A):
 # Durable commit-before-send; caller holds the ledger lock in parallel mode.
 can_send(l,s);raw=request(s)
 req=urllib.request.Request(base.ENDPOINT,data=raw,method='POST',headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','Accept':'text/event-stream','User-Agent':prior.UA,'x-opencode-session':s['session_id']})
 assert req.get_header('X-opencode-session') and req.data==raw and req.full_url==base.ENDPOINT
 aid=s['slot']+('-A%02d'%(len(s['attempt_ids'])+1));d=W/'run'/s['slot']/aid;d.mkdir(exist_ok=False);(d/'request_body.json').write_bytes(raw)
 dump(d/'safe_request_headers.json',{k:v for k,v in req.header_items() if k.lower() in prior.SAFE_REQUEST})
 kind='capacity_technical_replacement' if s['status']=='DEFERRED_CAPACITY' else ('quota_technical_replacement' if s.get('quota_pending') else 'regular')
 a={'attempt_id':aid,'slot':s['slot'],'case_id':s['case_id'],'model':s['model'],'dedup_key':s['dedup_key'],'status':'DISPATCH_COMMITTED','commit_unix':NOW(),'request_sha256':sha(raw),'session_id':s['session_id'],'list_accounted':s['worst_list_reservation_usd'],'allowance_accounted':s['allowance_reservation_usd'],'reservation_state':'UNKNOWN','kind':kind,'credential_source':source,'account_label':source}
 s['status']='DISPATCH_COMMITTED';s['attempt_ids'].append(aid);l['new_attempts'].append(a)
 l['phase_posts']+=1;l['commits_total']+=1
 if source==SOURCE_B:
  l['sourceB_accounted_usd']=l.get('sourceB_accounted_usd',0.0)+a['list_accounted'];l['sourceB_unknown_usd']=l.get('sourceB_unknown_usd',0.0)+a['list_accounted']
 else:
  l['accounted_usd']+=a['list_accounted'];l['unknown_usd']+=a['list_accounted']
 l['phase_allowance_accounted'][s['model']]+=a['allowance_accounted']
 if kind in ('capacity_technical_replacement','quota_technical_replacement'):l['quota_recovery_posts']+=1;s['quota_replacements_used']=s.get('quota_replacements_used',0)+(1 if kind=='quota_technical_replacement' else 0)
 l.setdefault('last_commit_unix',{})[s['model']]=NOW()
 dump(W/'run/ledger.json',l)
 life={'worker_pid':os.getpid(),'thread':threading.current_thread().name,'request_started_unix':NOW(),'phase':'WAITING_HEADERS','bytes_received':0,'event_count':0,'timeout_seconds':1800,'timeout_kind':'socket operation'};dump(d/'lifecycle.json',life);(d/'raw_stream.sse').touch()
 print(aid,s['case_id'],s['model'],kind.upper(),'COMMITTED',flush=True)
 return a,d,req,life

def dispatch_stream(d,req,key,opener,life):
 error=None;error_body_text=None
 try:
  with opener.open(req,timeout=1800) as resp:core.receive(resp,d,life)
 except urllib.error.HTTPError as e:
  error='HTTP_ERROR';red=e.read().replace(key.encode(),b'[REDACTED]');error_body_text=red.decode('utf-8','replace')
  life.update({'http_status':e.code,'safe_headers':{k:v for k,v in e.headers.items() if k.lower() in prior.SAFE_RESPONSE},'retry_after_raw':(e.headers.get('Retry-After') if hasattr(e.headers,'get') else None),'headers_received_unix':NOW(),'stream_closed_unix':NOW(),'phase':'HTTP_ERROR'});dump(d/'lifecycle.json',life);(d/'http_error_body.bin').write_bytes(red)
 except Exception as e:error=type(e).__name__;life.update({'exception_class':error,'phase':'TRANSPORT_UNKNOWN','stream_closed_unix':NOW()});dump(d/'lifecycle.json',life)
 return error,error_body_text

def dispatch(l,s,key,opener,source=SOURCE_A):
 a,d,req,life=dispatch_commit(l,s,key,source)
 error,error_body_text=dispatch_stream(d,req,key,opener,life)
 r=core.materialize(d,s,a,life,error);r['label']='FULL_CONTINUATION_NEW';dump(d/'result.json',r)
 return finalize(l,s,a,life,error,d,r,error_body_text)

def settle_success(l,s,a,r):
 src=a.get('credential_source',SOURCE_A)
 reserved_list=a['list_accounted'];reserved_allowance=a['allowance_accounted']
 l['phase_allowance_accounted'][s['model']]+=r['allowance']-reserved_allowance
 a.update({'list_accounted':r['list_cost'],'allowance_accounted':r['allowance'],'reservation_state':'KNOWN','returned_billing_source':r.get('billing_source'),'returned_cash_cost':r.get('cash_cost')})
 if src==SOURCE_B:
  l['sourceB_accounted_usd']=l.get('sourceB_accounted_usd',0.0)+r['list_cost']-reserved_list;l['sourceB_unknown_usd']=l.get('sourceB_unknown_usd',0.0)-reserved_list
  for k,name in [('list_cost','sourceB_known_list'),('allowance','sourceB_known_allowance'),('cash_cost','sourceB_known_cash')]:l[name]=l.get(name,0.0)+r[k]
 else:
  l['accounted_usd']+=r['list_cost']-reserved_list;l['unknown_usd']-=reserved_list
 l['cumulative_known_list']+=r['list_cost'];l['cumulative_known_allowance']+=r['allowance'];l['cumulative_known_cash']+=r['cash_cost']
 for k,name in [('list_cost','phase_known_list'),('allowance','phase_known_allowance'),('cash_cost','phase_known_cash')]:l[name][s['model']]+=r[k]
 # Card section 4: the ~4x ratio is a prediction, not a stop gate; changed multipliers are recorded, answers are kept.
 if r['list_cost']>0:l['multiplier_observations']+=1;l['multiplier_last']=r['allowance']/r['list_cost'];l['multiplier_max']=max(l['multiplier_max'] or 0.0,l['multiplier_last'])
 s['quota_pending']=False;l['capacity_streak']=0;l['unknown_streak']=0

def finalize(l,s,a,life,error,d,r,error_body_text):
 # Shared by live dispatch and offline recovery: classifies rejection, settles or freezes additively. Returns a disposition string.
 cls=classify_reject(r,life,error,d,error_body_text)
 if a.get('credential_source')==SOURCE_B and cls is not None:
  a.update({'status':'SOURCE_B_REJECTED_HOLD','result_path':str(d/'result.json'),'http_status':life.get('http_status'),'rejection_class':cls,'stop_reason':'LUNA_SOURCE_REJECTED'})
  s.update({'status':'SOURCE_B_REJECTED_HOLD','result_path':str(d/'result.json'),'quota_pending':False})
  l['luna_source_stop']={'unix':NOW(),'reason':cls,'attempt_id':a['attempt_id'],'http_status':life.get('http_status')}
  dump(W/'run/ledger.json',l);print(a['attempt_id'],'LUNA_SOURCE_HELD; Grok queue unchanged',flush=True);return 'luna_source_held'
 if cls=='account_quota':
  a.update({'status':'QUOTA_REJECTED','result_path':str(d/'result.json'),'http_status':life.get('http_status'),'rejection_class':cls,'stop_reason':'QUOTA_AWAITING_USER_RESUME'})
  s.update({'status':'QUOTA_REJECTED','result_path':str(d/'result.json'),'quota_pending':True})
  if a.get('credential_source')==SOURCE_B:
   l['luna_source_stop']={'unix':NOW(),'reason':'new source LUNA_ACCOUNT_B returned 429; source stopped per card section 4, no fallback to old key','error_body_sha256':sha((d/'http_error_body.bin').read_bytes()) if (d/'http_error_body.bin').exists() else None}
  else:
   l['stop_reason']='QUOTA_AWAITING_USER_RESUME'
  next_at=retry_after_unix(life.get('retry_after_raw'))
  dump(W/'QUOTA_STATE.json',{'slot':s['slot'],'case_id':s['case_id'],'model':s['model'],'attempt_id':a['attempt_id'],'rejection_class':cls,'http_status':life.get('http_status'),'error_evidence':str(d/'http_error_body.bin' if (d/'http_error_body.bin').exists() else d/'raw_stream.sse'),'error_body_sha256':sha((d/'http_error_body.bin').read_bytes()) if (d/'http_error_body.bin').exists() else sha((d/'raw_stream.sse').read_bytes()),'retry_after_raw':life.get('retry_after_raw'),'next_eligible_at_unix':next_at,'next_eligible_observable':next_at is not None,'session_id':s['session_id'],'reservation_state':'UNKNOWN_UNRELEASED','user_action_required':'explicit resume authorization after quota recovery; see card section 3','recorded_unix':NOW()})
  dump(W/'run/ledger.json',l);print(a['attempt_id'],'ACCOUNT_QUOTA_SAVE_EXIT no automatic waiting',flush=True);return 'account_quota'
 if cls=='model_rate_limit':
  # Model-scoped token-rate throttle (e.g. Luna TPM): defer this target and cool the whole model; other models keep dispatching. Account-window wording still global-stops above.
  a.update({'status':'MODEL_RATE_REJECT','result_path':str(d/'result.json'),'http_status':life.get('http_status'),'rejection_class':cls,'stop_reason':'MODEL_RATE_DEFERRED'})
  s['capacity_attempts']=s.get('capacity_attempts',0)+1
  wait=MODEL_RATE_BACKOFF_SECONDS[min(s['capacity_attempts']-1,len(MODEL_RATE_BACKOFF_SECONDS)-1)]
  nxt=NOW()+wait
  if s['capacity_attempts']<=CAP_CAPACITY_PER_TARGET:
   s.update({'status':'DEFERRED_CAPACITY','next_eligible_at_unix':nxt,'next_eligible_observable':False,'last_rejection_evidence':str(d/'http_error_body.bin' if (d/'http_error_body.bin').exists() else d/'raw_stream.sse')})
  else:
   s.update({'status':'DEFERRED_SERVICE_CAPACITY','next_eligible_at_unix':nxt,'last_rejection_evidence':str(d/'http_error_body.bin' if (d/'http_error_body.bin').exists() else d/'raw_stream.sse')})
  l.setdefault('model_rate_cooldown',{})[s['model']]=nxt
  l.setdefault('model_rate_events',[]).append({'unix':NOW(),'slot':s['slot'],'model':s['model'],'attempt':a['attempt_id'],'cooldown_until':nxt})
  dump(W/'run/ledger.json',l);print(a['attempt_id'],'MODEL_RATE_LIMIT',s['model'],'model cooled until',nxt,'queue continues',flush=True);return 'model_rate_limit'
 if cls=='service_capacity':
  a.update({'status':'SERVICE_CAPACITY_REJECT','result_path':str(d/'result.json'),'http_status':life.get('http_status'),'rejection_class':cls,'stop_reason':'DEFERRED_PENDING_BACKOFF'})
  s['capacity_attempts']=s.get('capacity_attempts',0)+1
  if s['capacity_attempts']<=CAP_CAPACITY_PER_TARGET:
   ra=retry_after_unix(life.get('retry_after_raw'));nxt=NOW()+CAPACITY_BACKOFF_SECONDS[s['capacity_attempts']-1]
   if ra and ra>nxt:nxt=ra
   s.update({'status':'DEFERRED_CAPACITY','next_eligible_at_unix':nxt,'next_eligible_observable':ra is not None,'last_rejection_evidence':str(d/'raw_stream.sse')})
  else:s['status']='DEFERRED_SERVICE_CAPACITY'
  if a.get('credential_source')==SOURCE_B:
   l['luna_source_stop']={'unix':NOW(),'reason':'new source LUNA_ACCOUNT_B rate-limited (429 token rate); source stopped per card section 4','error_body_sha256':sha((d/'http_error_body.bin').read_bytes()) if (d/'http_error_body.bin').exists() else None}
  l['capacity_streak']+=1;l['unknown_streak']=0
  if l['capacity_streak']>=STREAK_COOLDOWN and not l['cooldown_done']:
   l['cooldown_done']=True;l['cooldown_until_unix']=NOW()+GLOBAL_COOLDOWN_SECONDS;print('COOLDOWN 15min after 5 consecutive capacity rejects',flush=True)
  if l['capacity_streak']>=STREAK_EXIT:l['stop_reason']='STOPPED_TRANSIENT_SERVICE_OUTAGE'
  dump(W/'run/ledger.json',l);print(a['attempt_id'],'SERVICE_CAPACITY_REJECT streak',l['capacity_streak'],'slot',s['status'],flush=True);return 'service_capacity'
 stop=prior.gate(r,s['model'],life.get('http_status'),error)
 if stop and (stop in LOCAL_STOPS or (stop=='MODEL_MISMATCH_OR_MISSING' and not r.get('terminal'))):
  # A stream break or transport loss without settlement evidence: no final result exists; freeze THIS target, keep reservation unknown, and continue the rest.
  a.update({'status':'RESULT_UNKNOWN_LOCAL','result_path':str(d/'result.json'),'http_status':life.get('http_status'),'stop_reason':stop})
  s.update({'status':'COMMITTED_OR_UNKNOWN','result_path':str(d/'result.json')})
  if a.get('credential_source')==SOURCE_B:
   l['luna_source_stop']={'unix':NOW(),'reason':stop,'attempt_id':a['attempt_id']}
  else:
   l['unknown_streak']+=1
   if l['unknown_streak']>=UNKNOWN_STREAK_EXIT:l['stop_reason']='STOPPED_LOCAL_UNKNOWN_OUTAGE'
  dump(W/'run/ledger.json',l);print(a['attempt_id'],'LOCAL_UNKNOWN_FREEZE',stop,'queue continues',flush=True);return 'unknown_local'
 if stop is None and (r['list_cost']>s['worst_list_reservation_usd']+1e-8 or r['allowance']>s['allowance_reservation_usd']+1e-7):stop='USAGE_EXCEEDS_RESERVATION'
 if stop is None:settle_success(l,s,a,r)
 a.update({'status':'COMPLETE' if r.get('completed') else 'INCOMPLETE_OR_ERROR','result_path':str(d/'result.json'),'stop_reason':stop,**{k:r.get(k) for k in ['http_status','list_cost','allowance','cash_cost','billing_source']}});s.update({'status':a['status'],'result_path':a['result_path']})
 if stop:
  if a.get('credential_source')==SOURCE_B and stop!='USAGE_EXCEEDS_RESERVATION':
   l['luna_source_stop']={'unix':NOW(),'reason':stop,'attempt_id':a['attempt_id']}
  else:l['stop_reason']=stop
 dump(W/'run/ledger.json',l);print(a['attempt_id'],a['status'],'list',r.get('list_cost'),'allowance',r.get('allowance'),'cash',r.get('cash_cost'),'STOP',stop,flush=True);return 'settled' if not stop else 'stopped'

def progress(l):
 settled=sum(1 for s in l['slots'] if s['status'] in ['COMPLETE','INCOMPLETE_OR_ERROR','COMMITTED_OR_UNKNOWN','DEFERRED_SERVICE_CAPACITY'] and not s.get('carried_verified'))
 if settled==l['last_progress_settled']:return
 l['last_progress_settled']=settled
 if settled%CHECKPOINT_EVERY==0:
  dump(W/'PROGRESS_CHECKPOINTS'/('CHECKPOINT_%03d.json'%settled),{'settled_new_targets':settled,'unix':NOW(),'phase_posts':l['phase_posts'],'commits_total':l['commits_total'],'accounted_usd':l['accounted_usd'],'unknown_usd':l['unknown_usd'],'cumulative_known_list':l['cumulative_known_list'],'cumulative_known_allowance':l['cumulative_known_allowance'],'cumulative_known_cash':l['cumulative_known_cash'],'capacity_streak':l['capacity_streak'],'unknown_streak':l['unknown_streak'],'multiplier':{k:l['multiplier_'+k] for k in ['observations','last','max']}})
 if settled==CUM30_NEW_TARGETS and not l['cum30_written']:
  est={}
  for m in base.MODELS:
   n=sum(1 for s in l['slots'] if s['status'] in ['COMPLETE','INCOMPLETE_OR_ERROR'] and s['model']==m and not s.get('carried_verified'));known=l['phase_known_list'][m]
   est[m]={'settled_new':n,'phase_list_mean':(known/n if n else None)}
  dump(W/'CUMULATIVE30_CHECKPOINT.json',{'unix':NOW(),'note':'one-time estimate update at cumulative 30 questions; no stop required, remaining authorized targets continue','new_target_estimates':est,'cumulative_known_list':l['cumulative_known_list'],'cumulative_known_allowance':l['cumulative_known_allowance']});l['cum30_written']=True
 dump(W/'run/ledger.json',l)

def preflight(l):
 manifests();assert load(W/'EXTRA_USAGE_CONFIRMATION.json')['carried_confirmed_disabled']
 for rel,h in load(W/'PRE_DISPATCH_FREEZE.json').items():assert sha((W/rel).read_bytes())==h,rel
 dump(W/'logs/worker.json',{'pid':os.getpid(),'start_unix':NOW(),'locks':'all prior generations process.lock held','restart':False,'task_id':TASK_ID})
 assert stat.S_IMODE(base.KEY.stat().st_mode)==0o600
 assert subprocess.run(['git','check-ignore','-q',str(base.KEY)]).returncode==0
 assert subprocess.run(['git','ls-files','--error-unmatch',str(base.KEY)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
 if KEY2.exists():
  assert stat.S_IMODE(KEY2.stat().st_mode)==0o600
  assert subprocess.run(['git','check-ignore','-q',str(KEY2)]).returncode==0
  assert subprocess.run(['git','ls-files','--error-unmatch',str(KEY2)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0

def offline_recover_commit(l):
 # A committed slot without result: replay the durable raw stream offline. Full terminal frame settles; otherwise freeze as unknown. Never re-POST here.
 for s in l['slots']:
  if s['status']!='DISPATCH_COMMITTED':continue
  aid=s['attempt_ids'][-1];d=W/'run'/s['slot']/aid;a=next(x for x in (l['new_attempts']+l['historical_attempts']) if x['attempt_id']==aid)
  life=load(d/'lifecycle.json') if (d/'lifecycle.json').exists() else {'worker_pid':None,'request_started_unix':a.get('commit_unix',NOW()),'phase':'RECOVERED','bytes_received':0,'event_count':0,'http_status':200}
  raw=(d/'raw_stream.sse').read_bytes() if (d/'raw_stream.sse').exists() else b''
  try:r=base.parse(raw)
  except Exception:r={'visible_answer':'','usage':None,'completed':False}
  parsed,js,_tr=base.collector.parse_answer_text(r.get('visible_answer',''));validation=base.collector.validate_answer(parsed,load(base.INPUT/'schemas/biodegradation_answer_v2.schema.json'),check=js=='VALID')
  r.update({'slot':s['slot'],'case_id':s['case_id'],'attempt_id':aid,'requested_model':s['model'],'label':'FULL_CONTINUATION_OFFLINE_RECOVERED','json_status':js,'schema_status':validation['schema_status'],'visible_characters':len(r.get('visible_answer','')),'session_id':s['session_id'],'sent_request_sha256':a.get('request_sha256')})
  (d/'visible_answer.txt').write_text(r.pop('visible_answer') if 'visible_answer' in r else '');dump(d/'result.json',r);dump(d/'schema_validation.json',validation)
  life.setdefault('stream_closed_unix',NOW())
  finalize(l,s,a,life,'PROCESS_LOSS_OFFLINE_RECOVERY' if not r.get('completed') else None,d,r,None)
  print('offline replay of',aid,'->',s['status'],flush=True)
 dump(W/'run/ledger.json',l)

def wait_for_work(l):
 # local timer only: naps until the earliest capacity backoff, global cooldown or Luna pace deadline; never polls an LLM, never wakes the account quota.
 waiting=[s for s in l['slots'] if s['status']=='DEFERRED_CAPACITY']
 targets=[s['next_eligible_at_unix'] for s in waiting]
 if l.get('cooldown_until_unix') and l['cooldown_until_unix']>NOW():targets.append(l['cooldown_until_unix'])
 pending_models={s['model'] for s in l['slots'] if s['status']=='ELIGIBLE_UNSUBMITTED' or (s.get('quota_pending') and s['status']=='QUOTA_REJECTED')}
 for m,until in (l.get('model_rate_cooldown') or {}).items():
  if m in pending_models and until>NOW():targets.append(until)
 if 'gpt-6-luna' in pending_models and luna_paced(l):targets.append(l.get('last_commit_unix',{}).get('gpt-6-luna',0)+LUNA_MIN_INTERVAL_SECONDS)
 if not targets:return False
 target=min(targets)
 nap=target-NOW()
 if nap>0:
  dump(W/'logs/worker.json',{'pid':os.getpid(),'unix':NOW(),'state':'CAPACITY_BACKOFF_SLEEP','sleep_seconds':min(nap,60),'deferred_targets':len(waiting)})
  time.sleep(min(nap,60));return True
 return True

def run_queue(l):
 key=base.KEY.read_text().strip();assert key;opener=urllib.request.build_opener(base.NoRedirect)
 kB=luna_key();opB=urllib.request.build_opener(base.NoRedirect) if kB else None
 while not l['stop_reason']:
  did=False
  if stop_requested():l['stop_reason']='USER_STOP_REQUESTED';dump(W/'run/ledger.json',l);break
  if l.get('cooldown_until_unix') and NOW()<l['cooldown_until_unix']:
   dump(W/'logs/worker.json',{'pid':os.getpid(),'unix':NOW(),'state':'GLOBAL_CAPACITY_COOLDOWN','sleep_seconds':min(l['cooldown_until_unix']-NOW(),60)})
   time.sleep(min(l['cooldown_until_unix']-NOW(),60));continue
  for s in l['slots']:
   if l['stop_reason']:break
   if stop_requested():l['stop_reason']='USER_STOP_REQUESTED';dump(W/'run/ledger.json',l);break
   ready=ready_slot(l,s) and not external_hold(s)
   if ready and s['model']=='gpt-6-luna' and luna_paced(l):ready=False
   if not ready:continue
   assert inputs_unchanged(l)
   try:can_send(l,s)
   except AssertionError as e:
    if str(e) in ('CAPACITY_BACKOFF_NOT_ELAPSED','TECH_REPLACEMENT_POOL_24','CAPACITY_ATTEMPTS_EXHAUSTED'):continue
    if str(e)=='QUOTA_REPLACEMENT_ALREADY_USED':
     s['quota_pending']=False;s['status']='QUOTA_REJECTED_EXHAUSTED';dump(W/'run/ledger.json',l);continue
    l['stop_reason']=str(e);dump(W/'run/ledger.json',l);break
   if s['model']=='gpt-6-luna':
    if not kB or l.get('luna_source_stop'):continue
    dispatch(l,s,kB,opB,SOURCE_B)
   else:dispatch(l,s,key,opener)
   did=True;progress(l)
  if l['stop_reason']:break
  pending=any(s['status']=='ELIGIBLE_UNSUBMITTED' and not external_hold(s) for s in l['slots'])
  deferred=any(s['status']=='DEFERRED_CAPACITY' and not external_hold(s) for s in l['slots'])
  if not pending and not deferred:break
  if did:continue
  if not wait_for_work(l):l['stop_reason']='RUNLOOP_NO_PROGRESS';dump(W/'run/ledger.json',l);break
 credential_sweep([key,kB])

def ready_slot(l,s):
 if l.get('model_rate_cooldown',{}).get(s['model'],0)>NOW():return False
 return s['status']=='ELIGIBLE_UNSUBMITTED' or (s.get('quota_pending') and s['status']=='QUOTA_REJECTED') or (s['status']=='DEFERRED_CAPACITY' and NOW()>=s['next_eligible_at_unix'] and s['capacity_attempts']<CAP_CAPACITY_PER_TARGET+1)

def parallel_queue(l,key,opener,threads=None,caps=None,lock=None,keyB=None,openerB=None):
 # Grok pool plus a dedicated serial Luna dispatcher: Luna readiness must never wait for long Grok streams to join.
 threads=threads or MAX_INFLIGHT_PER_MODEL['grok-4.7'];caps=caps or MAX_INFLIGHT_PER_MODEL;lock=lock or threading.RLock()
 SKIP={'CAPACITY_BACKOFF_NOT_ELAPSED','TECH_REPLACEMENT_POOL_24','CAPACITY_ATTEMPTS_EXHAUSTED'}
 def s_of(a):return next(x for x in l['slots'] if x['slot']==a['slot'])
 def pick_commit(model_filter,keyx,source):
  with lock:
   if l['stop_reason']:return None
   if stop_requested():l['stop_reason']='USER_STOP_REQUESTED';dump(W/'run/ledger.json',l);return None
   if l.get('cooldown_until_unix') and NOW()<l['cooldown_until_unix']:return 'cooldown'
   inflight={}
   for s in l['slots']:
    if s['status']=='DISPATCH_COMMITTED':inflight[s['model']]=inflight.get(s['model'],0)+1
   for s in l['slots']:
    if s['model']!=model_filter:continue
    if not ready_slot(l,s) or external_hold(s) or inflight.get(s['model'],0)>=caps.get(s['model'],1):continue
    if s['model']=='gpt-6-luna' and (luna_paced(l) or l.get('luna_source_stop')):continue
    try:can_send(l,s)
    except AssertionError as e:
     if str(e) in SKIP:continue
     if str(e)=='QUOTA_REPLACEMENT_ALREADY_USED':
      s['quota_pending']=False;s['status']='QUOTA_REJECTED_EXHAUSTED';dump(W/'run/ledger.json',l);continue
     l['stop_reason']=str(e);dump(W/'run/ledger.json',l);return None
    assert inputs_unchanged(l)
    return (dispatch_commit(l,s,keyx,source),keyx,source)
 def make_body(model_filter,keyx,source,openerx):
  def body():
   while True:
    with lock:
     if l['stop_reason']:return
     if model_filter=='gpt-6-luna' and l.get('luna_source_stop'):return
    try:item=pick_commit(model_filter,keyx,source)
    except Exception:
     with lock:traceback.print_exc();l['stop_reason']='PARALLEL_PICK_FAULT';dump(W/'run/ledger.json',l);return
    if item is None:
     with lock:
      future=not l['stop_reason'] and not (model_filter=='gpt-6-luna' and l.get('luna_source_stop')) and any(s['model']==model_filter and not external_hold(s) and (s['status']=='ELIGIBLE_UNSUBMITTED' or (s['status']=='DEFERRED_CAPACITY' and s.get('capacity_attempts',0)<CAP_CAPACITY_PER_TARGET+1)) for s in l['slots'])
     if not future:return
     time.sleep(1);continue
    if item=='cooldown':time.sleep(15);continue
    (a,d,req,life),kx,src=item
    try:
     error,ebt=dispatch_stream(d,req,kx,openerx,life)
     r=core.materialize(d,s_of(a),a,life,error);r['label']='FULL_CONTINUATION_NEW';dump(d/'result.json',r)
     with lock:finalize(l,s_of(a),a,life,error,d,r,ebt);progress(l)
    except Exception:
     with lock:traceback.print_exc();l['stop_reason']='PARALLEL_DISPATCH_FAULT';dump(W/'run/ledger.json',l);return
  return body
 while True:
  ts=[threading.Thread(target=make_body('grok-4.7',key,SOURCE_A,opener),name='grok-%d'%i,daemon=True) for i in range(threads)]
  if keyB and openerB and not l.get('luna_source_stop'):
   ts.append(threading.Thread(target=make_body('gpt-6-luna',keyB,SOURCE_B,openerB),name='luna-0',daemon=True))
  elif not keyB and any(s['status']=='ELIGIBLE_UNSUBMITTED' and s['model']=='gpt-6-luna' for s in l['slots']):
   l.setdefault('flags',{})['LUNA_CREDENTIAL_PENDING']=True
  for t in ts:t.start()
  for t in ts:t.join()
  with lock:
   if l['stop_reason']:break
   def live(m):return any((s['status']=='ELIGIBLE_UNSUBMITTED' or s['status']=='DEFERRED_CAPACITY') and s['model']==m and not external_hold(s) and not (m=='gpt-6-luna' and (not keyB or l.get('luna_source_stop'))) for s in l['slots'])
   if not live('grok-4.7') and not live('gpt-6-luna'):break
   if not wait_for_work(l):l['stop_reason']='RUNLOOP_NO_PROGRESS';dump(W/'run/ledger.json',l);break

def credential_sweep(keys):
 leaks=[]
 for f2 in W.rglob('*'):
  if not f2.is_file():continue
  blob=f2.read_bytes()
  for k in keys:
   if k and k.encode() in blob:leaks.append(str(f2.relative_to(W)))
 dump(W/'logs/CREDENTIAL_HANDLING.json',{'note':'designated key files only, in-memory','mode_600_untracked_ignored':True,'leak_check_passed':not leaks,'key_or_digest_recorded':False});assert not leaks

def worker_par():
 held=locks();l=load(W/'run/ledger.json')
 if l['stop_reason']:print('Persistent global stop, zero new POST:',l['stop_reason']);return
 if any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']):
  offline_recover_commit(l)
  if l['stop_reason']:print('recovery stopped queue:',l['stop_reason']);return
 preflight(l)
 key=base.KEY.read_text().strip();assert key;opener=urllib.request.build_opener(base.NoRedirect)
 kB=luna_key();opB=urllib.request.build_opener(base.NoRedirect) if kB else None
 if kB is None:l.setdefault('flags',{})['LUNA_CREDENTIAL_PENDING']=True
 parallel_queue(l,key,opener,keyB=kB,openerB=opB)
 credential_sweep([key,kB])

def worker():
 held=locks();l=load(W/'run/ledger.json')
 if l['stop_reason']:print('Persistent global stop, zero new POST:',l['stop_reason']);return
 if any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']):
  offline_recover_commit(l)
  if l['stop_reason']:print('recovery stopped queue:',l['stop_reason']);return
 preflight(l);run_queue(l)

def slot_of(l,slot):return next(s for s in l['slots'] if s['slot']==slot)

def resume_core(l):
 assert l['stop_reason']=='QUOTA_AWAITING_USER_RESUME','NOT_A_QUOTA_PAUSE'
 assert (W/'RESUME_AUTHORIZATION.json').exists(),'USER AUTHORIZATION FILE REQUIRED'
 auth=load(W/'RESUME_AUTHORIZATION.json')
 assert auth['task_id']==TASK_ID and auth['stop_reason_registered']=='QUOTA_AWAITING_USER_RESUME'
 assert auth['user_reply_verbatim'].strip(),'USER INSTRUCTION REQUIRED'
 q=load(W/'QUOTA_STATE.json');assert not any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']),'IN_FLIGHT_REQUESTS'
 if auth.get('scope')=='queue_only':
  s=slot_of(l,q['slot']);s['quota_pending']=False;s['status']='QUOTA_REJECTED_EXHAUSTED'
  l['stop_reason']=None;l['resume_events'].append({'unix':NOW(),'kind':'queue_only','user_reply_verbatim':auth['user_reply_verbatim'],'recorded_unix':auth['recorded_unix'],'slot':q['slot']})
 else:
  assert auth['slot']==q['slot'],'RESUME_SLOT_MISMATCH'
  s=slot_of(l,q['slot']);assert s['status']=='QUOTA_REJECTED' and s['quota_replacements_used']<CAP_QUOTA_PER_TARGET,'QUOTA_REPLACEMENT_ALREADY_USED'
  if q.get('next_eligible_at_unix') is not None:assert NOW()>=q['next_eligible_at_unix'],'RETRY_AFTER_NOT_ELAPSED'
  assert sha((W/'run'/s['slot']/'request_body.json').read_bytes())==s['request_sha256'],'FROZEN_BYTES_DRIFT'
  s['quota_pending']=True
  l['resume_events'].append({'unix':NOW(),'kind':'quota_technical_replacement','user_reply_verbatim':auth['user_reply_verbatim'],'recorded_unix':auth['recorded_unix'],'slot':q['slot'],'next_eligible_at_unix':q.get('next_eligible_at_unix')})
 l['stop_reason']=None;dump(W/'run/ledger.json',l)

def resume():
 held=locks();l=load(W/'run/ledger.json')
 resume_core(l);preflight(l);run_queue(l)

def resume_par():
 held=locks();l=load(W/'run/ledger.json')
 resume_core(l);preflight(l)
 key=base.KEY.read_text().strip();assert key;opener=urllib.request.build_opener(base.NoRedirect)
 kB=luna_key();opB=urllib.request.build_opener(base.NoRedirect) if kB else None
 parallel_queue(l,key,opener,keyB=kB,openerB=opB)
 credential_sweep([key,kB])

def recover():
 held=locks();l=load(W/'run/ledger.json')
 if not any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']):print('nothing committed in flight');return
 offline_recover_commit(l);dump(W/'run/ledger.json',l);print('offline recovery done; committed targets never auto-resent',l['stop_reason'])

def freeze():
 rels=['code/full_run.py','code/test_full_run.py','AUTHORIZATION_SCOPE.json','CARRY_IN.json','FROZEN_TARGETS.json','INPUT_OUTPUT_IDENTITIES.json','PILOT_CONFIG.json','EXTRA_USAGE_CONFIRMATION.json','SUPERVISOR_CONFIG.json','EFFECTIVE_RUNTIME_CONFIG.json','logs/OFFLINE_TEST_RESULTS.json']
 # logs/REPAIR_RECORD.json excluded from freeze: append-only engineering ledger, not a dispatch input
 rels+=[str((p.relative_to(W))) for p in (W/'run').glob('*/request_body.json')]
 dump(W/'PRE_DISPATCH_FREEZE.json',{rel:sha((W/rel).read_bytes()) for rel in rels})

def status():
 l=load(W/'run/ledger.json')
 from collections import Counter
 print(json.dumps({'TASK_ID':TASK_ID,'commits_total':l['commits_total'],'phase_posts':l['phase_posts'],'quota_recovery_posts':l['quota_recovery_posts'],'accounted_usd':l['accounted_usd'],'unknown_usd':l['unknown_usd'],'cumulative_known_list':l['cumulative_known_list'],'cumulative_known_allowance':l['cumulative_known_allowance'],'cumulative_known_cash':l['cumulative_known_cash'],'stop_reason':l['stop_reason'],'capacity_streak':l['capacity_streak'],'unknown_streak':l['unknown_streak'],'slot_statuses':dict(Counter(s['status'] for s in l['slots'])),'multiplier':{k:l['multiplier_'+k] for k in ['observations','last','max']}},ensure_ascii=False,indent=2))

def prepare():
 assert not (W/'run/ledger.json').exists(),'Never reset an existing ledger'
 held=locks();old=manifests();sources=base.identities()
 nl=load(NETFIX/'run/ledger.json');nd=load(NETFIX/'SHARED_DEDUP_INDEX.json')
 assert nl['posts_committed']==CARRY_COMMITS and abs(nl['accounted_usd']-CARRY_ACCOUNTED)<1e-12 and abs(nl['unknown_usd']-CARRY_UNKNOWN)<1e-12
 assert nl['stop_reason'] is None and len(nl['slots'])==20 and len(nd)==20
 nindex={(i['case_id'],i['exact_model_id']):i for i in nd}
 sys.path.insert(0,str(prior.PREV/'code'));import replay
 SCHEMA=base.INPUT/'schemas/biodegradation_answer_v2.schema.json'
 metadata=load(engine.R2/'PILOT_CONFIG.json')['metadata']
 carried={'complete':0,'reused':0,'unknown':0}
 slots=[]
 for case in CASE_IDS:
  for model in DISPATCH_ORDER:
   body=body_for(case,model);raw=compact(body);cfg=science(case,model,body);digest=sha(compact(cfg));key=case+'|'+model+'|'+digest
   slot='FULL-%03d'%(len(slots)+1);nrow=nindex.get((case,model));ns=next((x for x in nl['slots'] if x['case_id']==case and x['model']==model),None) if nrow else None
   s={'slot':slot,'case_id':case,'model':model,'scientific_request_config_sha256':digest,'dedup_key':key,'scientific_config':cfg,'request_sha256':sha(raw),'session_id':ns['session_id'] if nrow else str(uuid.uuid4()),'attempt_ids':copy.deepcopy(ns['attempt_ids']) if nrow else [],'quota_replacements_used':0}
   if nrow:
    assert nrow['status']==ns['status'] and ns['dedup_key']==key and ns['scientific_request_config_sha256']==digest,'NETFIX_CONFIG_DRIFT'
    path=ns.get('result_path',ns.get('source_result_path'));assert path
    rr=load(path);d=pathlib.Path(path).parent;actual=load(d/'request_body.json');assert science(case,model,actual)==cfg
    v=replay.replay((d/'raw_stream.sse').read_bytes());assert v['visible_answer']==(d/'visible_answer.txt').read_text() and v['usage']==rr.get('usage') and v['terminal']==rr.get('terminal')
    parsed,js,_tr=base.collector.parse_answer_text(v['visible_answer']);val=base.collector.validate_answer(parsed,load(SCHEMA),check=js=='VALID');assert val['schema_status']==rr['schema_status']
    s.update({'source_result_path':path,'source_attempt':nrow['attempt_ids'][-1]})
    if ns['status'] in ['COMPLETE','PILOT_REUSED']:s['status']='REUSED_VERIFIED';s['carried_verified']=True;carried['complete']+=(ns['status']=='COMPLETE');carried['reused']+=(ns['status']=='PILOT_REUSED')
    else:assert ns['status']=='HISTORICAL_UNKNOWN_FROZEN';s['status']='LEGACY_UNKNOWN_HOLD';carried['unknown']+=1
   else:
    d=W/'run'/slot;d.mkdir(parents=True,exist_ok=True);(d/'request_body.json').write_bytes(raw)
    upper=len(body['input'][0]['content'].encode())+4096;prices=metadata[model]['cost']['text'];ip=max(prices['input']['price'],prices['input'].get('cache',{}).get('write',0));context=upper+65536
    assert context<(200000 if model=='grok-4.7' else 272000),'CONTEXT_LIMIT'
    reserve=(upper*ip+65536*prices['output']['price'])/1e6
    s.update({'input_token_upper':upper,'context_upper':context,'worst_list_reservation_usd':reserve,'allowance_reservation_usd':4*reserve,'status':'ELIGIBLE_UNSUBMITTED'})
   slots.append(s)
 eligible=[s for s in slots if s['status']=='ELIGIBLE_UNSUBMITTED']
 assert len(slots)==242 and len(eligible)==222 and carried['complete']+carried['reused']==19 and carried['unknown']==1
 assert len(set(s['dedup_key'] for s in slots))==242 and len(set(s['session_id'] for s in slots))==242
 ledger={'TASK_ID':TASK_ID,'commits_carry':CARRY_COMMITS,'commits_total':CARRY_COMMITS,'proven_pre_http_transport_commits':1,'phase_posts':0,'quota_recovery_posts':0,'accounted_usd':CARRY_ACCOUNTED,'unknown_usd':CARRY_UNKNOWN,'cumulative_known_list':CARRY_KNOWN_LIST,'cumulative_known_allowance':CARRY_KNOWN_ALLOWANCE,'cumulative_known_cash':CARRY_KNOWN_CASH,'phase_allowance_accounted':{m:0 for m in base.MODELS},'phase_known_list':{m:0 for m in base.MODELS},'phase_known_allowance':{m:0 for m in base.MODELS},'phase_known_cash':{m:0 for m in base.MODELS},'multiplier_observations':0,'multiplier_last':None,'multiplier_max':None,'stop_reason':None,'last_progress_settled':0,'cum30_written':False,'capacity_streak':0,'unknown_streak':0,'cooldown_done':False,'cooldown_until_unix':None,'resume_events':[],'slots':slots,'historical_attempts':nl['historical_attempts']+nl['new_attempts'],'new_attempts':[]}
 dump(W/'CARRY_IN.json',{'netfix_ledger':nl,'netfix_dedup_index':nd,'netfix_attempt_history':load(NETFIX/'SHARED_ATTEMPT_HISTORY.json'),'manifests':old,'carry_commits':CARRY_COMMITS,'carry_generation_posts':23,'carry_accounted_usd':CARRY_ACCOUNTED,'carry_unknown_usd':CARRY_UNKNOWN,'carry_known_list':CARRY_KNOWN_LIST,'carry_known_allowance':CARRY_KNOWN_ALLOWANCE,'resume_source_hashes':{rel:sha((NETFIX/rel).read_bytes()) for rel in ['run/ledger.json','SHARED_DEDUP_INDEX.json','SHARED_ATTEMPT_HISTORY.json','TARGET_RESULTS.json','FINAL_STATUS.json','AUTHORIZATION_SCOPE.json']}})
 dump(W/'FROZEN_TARGETS.json',slots);dump(W/'run/ledger.json',ledger)
 dump(W/'INPUT_OUTPUT_IDENTITIES.json',{'sources_before':sources,'netfix_final_sources_after':load(NETFIX/'INPUT_OUTPUT_IDENTITIES_FINAL.json')['sources_after']})
 dump(W/'AUTHORIZATION_SCOPE.json',{'task_id':TASK_ID,'card':str(CARD),'card_sha256':sha(CARD.read_bytes()),'user_handoff':True,'scope':'222 eligible unsubmitted targets x two exact models; first-10 statuses carried; no Likert; no GitHub upload','cumulative_list_cap_usd':CAP_LIST_USD,'cumulative_commit_hard_cap':CAP_COMMITS_TOTAL,'phase_new_post_cap':CAP_PHASE_POSTS,'quota_recovery_post_cap':CAP_TECH_POOL,'quota_replacement_per_target_cap':CAP_QUOTA_PER_TARGET,'cash_authorized':False,'extra_usage':'carried user-confirmed off; executor never changes settings','full_run_authorized':True,'historical_unknown_resend_authorized':False,'stop_on_limit':'save persistent state and exit; resume only on explicit user authorization','automatic_waiting_or_polling':'forbidden'})
 dump(W/'EXTRA_USAGE_CONFIRMATION.json',{'source':'carried from NETFIX batch confirmation; no known settings change observed or performed by executor','user_reply':'已查看，Extra Usage 已关闭','carried_confirmed_disabled':True,'settings_modified_by_executor':False,'confirmed_unix_carry':1794214800,'recorded_unix':NOW()})
 dump(W/'PILOT_CONFIG.json',{'endpoint':base.ENDPOINT,'timeout_seconds':1800,'timeout_kind':'socket operation; no visible-text deadline; continuous reasoning is not a hang','concurrency':1,'worker_restarts':0,'metadata':metadata,'case_order':CASE_IDS,'model_dispatch_order':DISPATCH_ORDER,'model_order':base.MODELS,'limits':load(W/'AUTHORIZATION_SCOPE.json'),'checkpoint_every_targets':CHECKPOINT_EVERY,'estimate_is_not_guarantee':True})
 dump(W/'SUPERVISOR_CONFIG.json',{'unit':'enzyme-go-fullcont-20261109','Restart':'no','WorkingDirectory':'/home/a/EnzymeCAGE','network_env':'inherit standard proxy/certificate variables from working execution environment; no values in logs; no credentials in proxy URLs','socket_timeout':1800,'worker_restart':False})
 dump(W/'EFFECTIVE_RUNTIME_CONFIG.json',{'recorded_unix':NOW(),'runtime_budget_authority':'AUTHORIZATION_SCOPE.json (frozen before dispatch)','effective_cumulative_list_cap_usd':CAP_LIST_USD,'effective_commit_cap':CAP_COMMITS_TOTAL,'effective_phase_post_cap':CAP_PHASE_POSTS,'cash_authorized':False,'allowance_multiplier_stop_replaced_by':'record-only per card section 4; conservative list reservation still gates'})
 print('242 targets frozen: 19 reused verified, 1 legacy unknown, 222 eligible; caps 35 USD / 270 commits / 246 phase posts / tech pool 24')

def supervise(mode='worker'):
 # Regression guard for the 2026-11-09 incident: the shared r2 monitor must be pointed at this workspace before use.
 core.W=W;core.supervise([sys.executable,'-B',str(pathlib.Path(__file__).resolve()),mode])

if __name__=='__main__':
 {'prepare':prepare,'worker':worker,'worker_par':worker_par,'resume':resume,'resume_par':resume_par,'recover':recover,'freeze':freeze,'status':status,'supervise':lambda:supervise(sys.argv[2] if len(sys.argv)>2 else 'worker')}[sys.argv[1]]()
