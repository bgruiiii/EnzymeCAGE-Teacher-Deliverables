"""Explicitly gated single-item API execution using the production F2 modules."""
import fcntl
import json
import os
from pathlib import Path
from .common import MODEL,canonical,digest,load
from .pipeline import validate_return
from f2r12_budget_ledger import BudgetLedger
from f2r12_cache_checkpoint import AttemptArchive
from f2r12_transport import LiveTransport


def run(request,config,work,confirm_live=False):
    if not confirm_live or config.get('live_authorized')is not True:raise ValueError('live calls require config live_authorized=true and explicit CLI confirmation')
    if request.get('synthetic'):raise ValueError('SYNTHETIC example is offline-only; do not purchase a judge call for it')
    if request['body'].get('model')!=MODEL or config.get('model')!=MODEL:raise ValueError('exact judge model mismatch')
    if digest(request['body'])!=request['body_sha256']:raise ValueError('request changed after preparation')
    key=os.environ.get(config.get('api_key_env','ALIYUN_SCORING_API_KEY'))
    if not key:raise ValueError('configured API key environment variable is absent; values never printed')
    endpoint=config['endpoint']
    if not endpoint.startswith('https://'):raise ValueError('HTTPS endpoint required')
    root=Path(work);root.mkdir(parents=True,exist_ok=True)
    lock=(root/'WORK.lock').open('a+')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise ValueError('another scoring worker owns this work directory')
    # Keep the lock file open for the entire request/settlement/validation.
    try:
        ledger=BudgetLedger(str(root/'ledger'),float(config['hard_cap_cny']),
            int(config['global_attempt_cap']),float(config['reserve_per_request_cny']),max_transfers_per_target=1)
        ledger.reconcile_on_startup()
        run_key=digest(dict(identity=request['identity'],body=request['body'],model=MODEL,endpoint=endpoint))
        prior=root/'results'/f'{run_key}.json'
        state=load(root/'ledger/BUDGET_STATE.json')
        if prior.exists():return dict(deduped=True,result=load(prior))
        if state['slot_attempts'].get(run_key,0):raise ValueError('this request was already attempted or may be billed; inspect archive/ledger, do not blindly resend')
        seq=ledger.next_transfer_seq();tid=f'LIKERT_CODE_EXPORT#{run_key[:20]}#t{seq}'
        ledger.reserve(tid,run_key,reserve_cny=float(config['reserve_per_request_cny']))
        transport=LiveTransport(endpoint,key,session=None,stream=True)
        wire=transport.send(dict(endpoint=endpoint,body=request['body'],item_identity=request['identity']),int(config.get('timeout_seconds',1800)))
        archive=AttemptArchive(str(root/'attempts'))
        archive.store(tid,wire,json.dumps(request['body'],ensure_ascii=False).encode(),request['identity'],run_identity='LIKERT_V05_CODE_EXPORT_20261114',attempt_index=0)
        price=config['historical_price_basis_cny_per_million']
        settlement=ledger.settle_by_transport(tid,dict(usage=wire.get('usage'),http_status=wire.get('http_status'),
            response_received=wire.get('raw_response_bytes')is not None,may_have_billed=wire.get('may_have_billed',False),error_kind=wire.get('error_kind')),float(price['input']),float(price['output']))
        record=dict(transfer_id=tid,item_id=request['slot'],request_sha256=request['body_sha256'],
            endpoint=endpoint,run_config_sha256=digest(config),
            model_requested=MODEL,model_returned=wire.get('model_returned'),http_status=wire.get('http_status'),
            stream_status=wire.get('stream_status'),usage=wire.get('usage'),settlement=settlement,
            status='TECHNICAL_FAILURE',price_basis_not_verified_cash_charge=True)
        try:
            if wire.get('stream_status')!='COMPLETE':raise ValueError('incomplete response; billing uncertainty preserved')
            if wire.get('model_returned')not in(None,MODEL):raise ValueError('judge model drift')
            obj=json.loads(wire.get('content_text')or'')
            result=validate_return(obj,request)
            record.update(validation=result,response=obj,status='OK'if result['valid']else'REJECTED')
        except Exception as exc:record['error']=f'{type(exc).__name__}: {exc}'
        prior.parent.mkdir(exist_ok=True);prior.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        return record
    finally:
        fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
