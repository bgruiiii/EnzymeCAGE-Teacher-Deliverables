"""Thin adapter for one supplied request; dry-run by default, no automatic retries.
Does not choose tasks, edit prompts, score answers, or manage batch billing.
"""
import argparse,ast,hashlib,json,os,re,time,uuid,urllib.error,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ENDPOINTS={'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions':'chat-completions','https://opencode.ai/inference/go/openai/v1/chat/completions':'chat-completions','https://opencode.ai/inference/go/openai/v1/responses':'responses'}
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):return None

def dump(p,value):
 tmp=p.with_suffix('.tmp')
 with tmp.open('w')as h:json.dump(value,h,ensure_ascii=False,indent=2);h.write('\n');h.flush();os.fsync(h.fileno())
 os.replace(tmp,p)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def pure(file,names,extra=None):
 path=ROOT/'generation_framework'/file
 nodes=[n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef)and n.name in names]
 assert {n.name for n in nodes}==set(names)
 env={'json':json,'re':re};env.update(extra or{})
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),env);return env

def replay(raw,protocol):
 if protocol=='responses':
  d=pure('source/opencode/pilot.py',['events','parse'])['parse'](raw)
  return dict(complete=d['completed'],content=d['visible_answer'],model=d.get('model'),finish=d.get('terminal'),usage=d.get('usage'))
 d=pure('source/aliyun/g8_formal_runner.py',['flatten','search_evidence','parse_stream'],{'URL_RE':re.compile(r'https?://\S+',re.I)})['parse_stream'](raw.splitlines(keepends=True))
 return dict(complete=d['done']and d['finish']=='stop',content=d['visible'],model=None if d['response_model_field']=='NOT_EXPOSED'else d['response_model_field'],finish=d['finish'],usage=d['usage'])

def execute(body,cfg,out,live=False,opener=None):
 endpoint=cfg.get('endpoint');protocol=cfg.get('protocol')
 if endpoint not in ENDPOINTS or ENDPOINTS[endpoint]!=protocol:raise ValueError('endpoint/protocol not reviewed')
 if not isinstance(body,dict)or body.get('model')!=cfg.get('model'):raise ValueError('explicit model equality required')
 field='input'if protocol=='responses'else'messages'
 if not isinstance(body.get(field),list)or not body[field]or body.get('stream')is not True:raise ValueError('explicit messages and stream=true required')
 cap=body.get('max_output_tokens'if protocol=='responses'else'max_tokens')
 if type(cap)is not int or cap<=0:raise ValueError('explicit positive output limit required')
 wire=json.dumps(body,ensure_ascii=False,separators=(',',':')).encode();identity=digest(endpoint.encode()+b'\0'+wire)
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 import fcntl
 lock=(out/'WORK.lock').open('a+')
 try:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);statepath=out/'state.json'
  if statepath.exists():
   state=json.loads(statepath.read_text())
   if state['identity']!=identity:raise ValueError('work directory belongs to a different request')
   if state['status']!='PREPARED':return dict(deduped=True,state=state)
  else:
   state=dict(identity=identity,endpoint=endpoint,protocol=protocol,model_requested=body['model'],wire_sha256=digest(wire),session_id=str(uuid.uuid4()),status='PREPARED')
   (out/'request_body.json').write_bytes(wire);dump(statepath,state)
  if not live:return dict(dry_run=True,state=state)
  if cfg.get('live_authorized')is not True:raise ValueError('live_authorized=true and --live both required')
  secret=os.environ.get(cfg.get('api_key_env','BASE_MODEL_API_KEY'))
  if not secret:raise ValueError('configured key environment variable absent; value never logged')
  headers={'Content-Type':'application/json','Accept':'text/event-stream','Authorization':'Bearer '+secret,'User-Agent':'Research-Single-Request-Adapter/20261118'}
  if 'opencode.ai'in endpoint:headers['x-opencode-session']=state['session_id']
  req=urllib.request.Request(endpoint,data=wire,headers=headers,method='POST')
  state.update(status='DISPATCH_COMMITTED',started_unix=time.time(),billing_status='UNKNOWN');dump(statepath,state)
  client=opener or urllib.request.build_opener(NoRedirect());http=None;error=None
  with(out/'raw_stream.sse').open('wb')as h:
   try:
    with client.open(req,timeout=int(cfg.get('timeout_seconds',1800)))as response:
     http=response.status
     for chunk in response:h.write(chunk);h.flush();os.fsync(h.fileno())
   except urllib.error.HTTPError as e:http=e.code;error='HTTP_ERROR';(out/'http_error_body.bin').write_bytes(e.read().replace(secret.encode(),b'[REDACTED]'))
   except Exception as e:error=type(e).__name__
  raw=(out/'raw_stream.sse').read_bytes()
  try:d=replay(raw,protocol)
  except Exception as e:d=dict(complete=False,content='',model=None,usage=None,finish=None,parse_error=type(e).__name__)
  (out/'visible_answer.txt').write_text(d['content']or'')
  usage=d['usage'];oc=(usage or{}).get('opencode',{});model=d['model']
  match=model in([cfg['model']]+cfg.get('accepted_returned_model_ids',[]))if model else None
  try:json.loads(d['content']or'');js='JSON_READABLE'
  except ValueError:js='NOT_JSON'
  result=dict(status='COMPLETE'if d['complete']and match is True and error is None else'HELD_REVIEW',http_status=http,transport_error=error,model_requested=body['model'],model_returned=model,model_matches=match,finish_reason=d['finish'],usage=usage,billing_status='PROVIDER_USAGE_RECORDED'if usage else'UNKNOWN',opencode_billing_source=oc.get('billing_source'),opencode_list_cost=oc.get('list_cost'),opencode_allowance=oc.get('allowance'),opencode_cash_cost=(usage or{}).get('cost'),json_parse_status=js,schema_validation='NOT_PERFORMED',scientific_correctness='NOT_EVALUATED',raw_sha256=digest(raw),identity=identity)
  dump(out/'result.json',result);state.update(status=result['status'],ended_unix=time.time(),billing_status=result['billing_status']);dump(statepath,state);return result
 finally:fcntl.flock(lock,fcntl.LOCK_UN);lock.close()

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--request',type=Path,required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--live',action='store_true');a=p.parse_args()
 obj=json.loads(a.request.read_text());print(json.dumps(execute(obj.get('body',obj),json.loads(a.config.read_text()),a.out,a.live),ensure_ascii=False))
if __name__=='__main__':main()
