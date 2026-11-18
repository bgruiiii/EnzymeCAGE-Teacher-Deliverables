#!/usr/bin/env python3
"""PILOT only. No retry. New Responses envelope; frozen G8 sources stay read-only."""
import csv, fcntl, hashlib, importlib.util, json, os, pathlib, stat, sys, time
import urllib.request, urllib.error
W=pathlib.Path(__file__).resolve().parents[1]
R=W.parent
G=R/'25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26'
OLD=G/'G8_formal_execution_prepare_20261006/code/scripts'
INPUT=G/'G8_formal_execution_prepare_20261006/package_src/biosysmodb150_g8_formal_four_model_exec_20261006/inputs'
ENDPOINT='https://opencode.ai/inference/go/openai/v1/responses'
KEY=pathlib.Path('/home/a/EnzymeCAGE/opencode_api_key.txt')
CARD=R/'07_HPC_Prompts/LOCAL_AI_FOREIGN_NATIVE_GO_PLUS_2MODEL_4CALL_PILOT_EXECUTOR_ONLY_20261109.md'
MODELS=['gpt-6-luna','grok-4.7']
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(pathlib.Path(p).read_text())
def dump(p,d):
    p=pathlib.Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.tmp')
    with tmp.open('w') as f:
        json.dump(d,f,ensure_ascii=False,indent=2); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,p)
    fd=os.open(str(p.parent),os.O_RDONLY); os.fsync(fd); os.close(fd)
def compact(d): return json.dumps(d,ensure_ascii=False,separators=(',',':')).encode()
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
legacy=module('legacy_g8',OLD/'g8_formal_runner.py')
collector=module('legacy_collection',R/'24_BIOSYSMODB150_FIVE_LLM_API_ORCHESTRATOR_2026-09-24/scripts/run_collection_v2.py')
def identities():
    rows=list(csv.DictReader((R/'BASE_MODEL_EXTENSION_PREP_20261109/FROZEN_QUESTION_INDEX_121.tsv').open(),delimiter='\t'))
    assert len(rows)==121
    paths={}
    for row in rows:
        p=R/row['source_message_file']; raw=p.read_bytes(); d=json.loads(raw); msg=d['messages']
        assert sha(raw)==row['source_file_sha256']
        assert sha(compact(msg))==row['messages_sha256']
        assert len(msg)==1 and msg[0]['role']=='user' and set(msg[0])=={'role','content'}
        assert sha(msg[0]['content'].encode())==row['prompt_text_sha256']
        cp=INPUT/'messages'/p.name; assert cp.read_bytes()==raw
        paths[str(p.relative_to(R))]=sha(raw); paths[str(cp.relative_to(R))]=sha(raw)
    for b in load(R/'BASE_MODEL_EXTENSION_PREP_20261109/SOURCE_BINDINGS.json'):
        p=R/b['path']; assert sha(p.read_bytes())==b['sha256'],b['path']; paths[b['path']]=b['sha256']
    for p in list(OLD.glob('*.py'))+list(INPUT.rglob('*'))+[CARD,R/'BASE_MODEL_EXTENSION_PREP_20261109/FROZEN_QUESTION_INDEX_121.tsv']:
        if p.is_file(): paths[str(p.relative_to(R))]=sha(p.read_bytes())
    return paths

def prepare():
    assert not (W/'run/ledger.json').exists(),'Existing ledger: do not reset'
    before=identities(); dump(W/'INPUT_OUTPUT_IDENTITIES.json',{'sources_before':before})
    metadata={m['id']:m for m in load(W/'docs/models_public.json')['data'] if m['id'] in MODELS}
    assert set(metadata)==set(MODELS)
    slots=[]
    for i,(case,model) in enumerate([(c,m) for c in ['BIOPATH150_001','BIOPATH150_002'] for m in MODELS],1):
        msgs=load(INPUT/'messages'/f'{case}.json')['messages']
        body={'model':model,'input':msgs,'stream':True,'max_output_tokens':65536,'tools':[],'tool_choice':'none'}
        if model=='grok-4.7': body['temperature']=0
        raw=compact(body); slot=f'GO-P{i:03}'; d=W/'run'/slot; d.mkdir(parents=True,exist_ok=True)
        p=d/'request_body.json'; assert not p.exists(); p.write_bytes(raw)
        assert json.loads(p.read_bytes())['input']==msgs
        # Byte-level vocabulary upper bound plus generous envelope/token overhead; no cache assumption.
        upper=sum(len(m['content'].encode()) for m in msgs)+4096
        meta=metadata[model]; cost=meta['cost']['text']; context=upper+65536
        assert context < min(x['when']['context']['gt'] for v in cost.values() for x in v.get('overrides',[]))
        assert context<meta['limit']['context'] and 65536<=meta['limit']['output']
        reserve=(upper*cost['input']['price']+65536*cost['output']['price'])/1e6
        slots.append({'slot':slot,'case_id':case,'model':model,'label':'PILOT','request_sha256':sha(raw),'prompt_sha256':sha(msgs[0]['content'].encode()),'input_token_upper':upper,'max_output_tokens':65536,'worst_list_cost_usd':reserve,'context_upper':context,'status':'NOT_DISPATCHED'})
    total=sum(s['worst_list_cost_usd'] for s in slots); assert total<=2
    dump(W/'PILOT_CONFIG.json',{'endpoint':ENDPOINT,'post_cap':4,'list_cost_cap_usd':2,'total_worst_reservation_usd':total,'metadata':metadata,'sampling':{'gpt-6-luna':{'temperature':'unsupported/not_sent'},'grok-4.7':{'temperature':0},'top_p':'not_sent','reasoning.effort':'not_sent; effective default unobservable'},'tools':[],'tool_choice':'none','extra_format_contract':False,'retries':0,'concurrency':1})
    dump(W/'AUTHORIZATION_SCOPE.json',{'task_id':'FOREIGN_NATIVE_GO_PLUS_2MODEL_4CALL_PILOT','source':'User actually handed off the following execution card in this conversation','user_message':'按照这个来执行一下;'+str(CARD),'card_sha256':sha(CARD.read_bytes()),'full_run_authorized':False,'independent_audit_pass':False,'cap_origin':'execution card safety cap, not a quote of user numerical approval'})
    dump(W/'FROZEN_SLOTS.json',slots); dump(W/'run/ledger.json',{'posts_committed':0,'reserved_usd':0,'stop_reason':None,'slots':slots})
    print('Prepared 121 verified identities; 4 slots; worst reservation USD',total)

def events(raw):
    # SSE spec: concatenate multi-line data, accept CRLF and only complete blank-line frames.
    lines=raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n').split('\n'); data=[]
    for line in lines:
        if not line:
            if data:
                payload='\n'.join(data); data=[]
                if payload!='[DONE]': yield json.loads(payload)
        elif line.startswith('data:'):
            v=line[5:]; data.append(v[1:] if v.startswith(' ') else v)

def parse(raw):
    ev=list(events(raw)); delta=''; terminal=None; response={}; tool=False
    for e in ev:
        typ=e.get('type','')
        if typ=='response.output_text.delta': delta+=e.get('delta','')
        if typ in ['response.completed','response.failed','response.incomplete']:
            terminal=typ; response=e.get('response',{})
        item=e.get('item',{})
        if 'call' in typ or (item and item.get('type') not in ['message','reasoning']): tool=True
    text=''.join(c.get('text','') for o in response.get('output',[]) if o.get('type')=='message' for c in o.get('content',[]) if c.get('type')=='output_text')
    for o in response.get('output',[]):
        if o.get('type') not in ['message','reasoning']: tool=True
    usage=response.get('usage'); oc=(usage or {}).get('opencode',{})
    return {'visible_answer':text if text else delta,'terminal':terminal,'response_status':response.get('status'),'model':response.get('model'),'usage':usage,'reasoning_tokens':(usage or {}).get('output_tokens_details',{}).get('reasoning_tokens'),'cached_tokens':(usage or {}).get('input_tokens_details',{}).get('cached_tokens'),'billing_source':oc.get('billing_source'),'allowance':oc.get('allowance'),'list_cost':oc.get('list_cost'),'cash_cost':(usage or {}).get('cost'),'tool_call_detected':tool,'completed':terminal=='response.completed' and response.get('status')=='completed','truncated':terminal=='response.incomplete','event_count':len(ev)}

def gate(result,model,http):
    if http!=200:return 'HTTP_SERVICE_ERROR'
    if result.get('model')!=model:return 'MODEL_MISMATCH_OR_MISSING'
    if result.get('tool_call_detected'):return 'TOOL_CALL_DETECTED'
    if result.get('billing_source')!='go-plus':return 'BILLING_SOURCE_NOT_VERIFIED_GO_PLUS'
    if result.get('cash_cost')!=0:return 'CASH_COST_NONZERO_OR_UNKNOWN'
    u=result.get('usage') or {}
    if not all(isinstance(u.get(k),(int,float)) for k in ['input_tokens','output_tokens']):return 'USAGE_UNKNOWN'
    if not all(isinstance(result.get(k),(int,float)) for k in ['allowance','list_cost']):return 'BILLING_USAGE_UNKNOWN'
    if not result.get('completed'):return 'TERMINAL_NOT_COMPLETED'
    return None

def commit(ledger,s):
    assert s['status']=='NOT_DISPATCHED','At-most-once: already committed'
    assert ledger['posts_committed']<4 and ledger['reserved_usd']+s['worst_list_cost_usd']<=2
    ledger['posts_committed']+=1; ledger['reserved_usd']+=s['worst_list_cost_usd']
    s['status']='DISPATCH_COMMITTED'; s['commit_time_unix']=time.time()

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def run():
    lock=(W/'run/process.lock').open('a'); fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    ledger=load(W/'run/ledger.json')
    if ledger['stop_reason']: print('Persistent stop:',ledger['stop_reason']); return
    if any(s['status']=='DISPATCH_COMMITTED' for s in ledger['slots']):
        ledger['stop_reason']='COMMITTED_RESULT_UNKNOWN_NO_RESEND'; dump(W/'run/ledger.json',ledger); return
    assert load(W/'logs/OFFLINE_TEST_RESULTS.json')['passed']
    assert identities()==load(W/'INPUT_OUTPUT_IDENTITIES.json')['sources_before']
    for rel,digest in load(W/'PRE_DISPATCH_FREEZE.json').items():
        assert sha((W/rel).read_bytes())==digest,rel
    cfg=load(W/'PILOT_CONFIG.json')
    assert cfg['total_worst_reservation_usd']<=2
    assert stat.S_IMODE(KEY.stat().st_mode)==0o600
    import subprocess
    assert subprocess.run(['git','ls-files','--error-unmatch',str(KEY)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
    assert subprocess.run(['git','check-ignore','-q',str(KEY)]).returncode==0
    key=KEY.read_text().strip(); assert key
    dump(W/'logs/KEY_HANDLING.json',{'note':'已读取指定密钥文件','mode':'600','git_untracked':True,'local_ignore_hit':True})
    opener=urllib.request.build_opener(NoRedirect)
    for s in ledger['slots']:
        if s['status']!='NOT_DISPATCHED': continue
        d=W/'run'/s['slot']; raw=(d/'request_body.json').read_bytes()
        assert sha(raw)==s['request_sha256']
        body=json.loads(raw); original=load(INPUT/'messages'/f"{s['case_id']}.json")['messages']
        assert body['input']==original and sha(body['input'][0]['content'].encode())==s['prompt_sha256']
        assert set(body)==({'model','input','stream','max_output_tokens','tools','tool_choice'}|({'temperature'} if s['model']=='grok-4.7' else set()))
        commit(ledger,s); dump(W/'run/ledger.json',ledger)  # durable commit BEFORE any transport
        started=time.time(); mono=time.monotonic(); http=None; first=None; error=None; headers={}
        req=urllib.request.Request(ENDPOINT,data=raw,method='POST',headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','Accept':'text/event-stream','User-Agent':'EnzymeCAGE-Research-Pilot/20261109 (independent scientific question collection)'})
        print(s['slot'],'committed; POST starting',flush=True)
        with (d/'raw_stream.sse').open('wb') as out:
            try:
                with opener.open(req,timeout=1800) as resp:
                    http=resp.status
                    headers={k:v for k,v in resp.headers.items() if k.lower() in ['content-type','date','x-request-id','request-id','retry-after']}
                    for line in resp:
                        out.write(line); out.flush(); os.fsync(out.fileno())
                        if first is None and b'response.output_text.delta' in line:
                            try:
                                e=json.loads(line.split(b'data:',1)[1]); visible=e.get('delta','')
                                if visible:first=time.monotonic()-mono
                            except (ValueError,IndexError):pass
            except urllib.error.HTTPError as e:
                http=e.code; err=e.read(); (d/'http_error_body.bin').write_bytes(err.replace(key.encode(),b'[REDACTED]'))
                headers={k:v for k,v in e.headers.items() if k.lower() in ['content-type','date','x-request-id','retry-after']}; error='HTTP_ERROR'
            except Exception as e:
                error=type(e).__name__  # no exception text/headers/key exposure
        try: result=parse((d/'raw_stream.sse').read_bytes())
        except Exception as e: result={'completed':False,'parse_error':type(e).__name__,'visible_answer':'','usage':None}
        parsed,jstatus,transform=collector.parse_answer_text(result['visible_answer'])
        validation=collector.validate_answer(parsed,load(INPUT/'schemas/biodegradation_answer_v2.schema.json'),check=jstatus=='VALID')
        result.update({'slot':s['slot'],'case_id':s['case_id'],'requested_model':s['model'],'label':'PILOT','http_status':http,'transport_error':error,'started_unix':started,'ended_unix':time.time(),'duration_seconds':time.monotonic()-mono,'first_visible_seconds':first,'json_status':jstatus,'parser_transform':transform,'schema_status':validation['schema_status'],'visible_characters':len(result['visible_answer']),'sent_request_sha256':sha(raw)})
        (d/'visible_answer.txt').write_text(result.pop('visible_answer'))
        dump(d/'schema_validation.json',validation); dump(d/'safe_headers.json',headers); dump(d/'result.json',result)
        stop=gate(result,s['model'],http)
        s['status']='COMPLETE' if result['completed'] else ('HTTP_ERROR' if http and http!=200 else 'RESULT_UNKNOWN_OR_FAILED')
        s['result_path']=str((d/'result.json').relative_to(W)); s['stop_reason']=stop
        if stop:ledger['stop_reason']=stop
        dump(W/'run/ledger.json',ledger)
        print(s['slot'],s['status'],'billing',result.get('billing_source'),'cash',result.get('cash_cost'),'stop',stop,flush=True)
        if stop: break

if __name__=='__main__':
    {'prepare':prepare,'run':run}[sys.argv[1]]()
