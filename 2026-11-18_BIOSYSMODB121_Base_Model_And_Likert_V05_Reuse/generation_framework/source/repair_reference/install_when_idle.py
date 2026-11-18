"""Install a byte-identified repair only with all locks idle. Does not launch or send."""
import copy
import fcntl
import hashlib
import json
import pathlib
import shutil
import time

HERE=pathlib.Path(__file__).resolve().parent
R=HERE.parents[1]
W=R/'FOREIGN_NATIVE_GO_PLUS_FULL_CONTINUATION_20261109'
BASELINE='e94f8a210b60e5f7671107dfdde1174dd742e6af41bb3be6119f077a6523f122'
PATCHED='2950ae9b71e917545c8df788393510bdf645e93978513ff4369c075d84c54f59'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text())
def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def main():
    assert read(HERE/'FOCUSED_TEST_RESULTS.json')['passed']
    assert sha(W/'code/full_run.py')==BASELINE,'Current source changed: do not overwrite another executor edit'
    assert sha(W/'code/full_run_repaired.py')==PATCHED
    handles=[]
    try:
        for name in ('run/process.lock','run/supervisor.lock'):
            handle=(W/name).open('a');fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB);handles.append(handle)
        l=read(W/'run/ledger.json')
        assert not any(s['status']=='DISPATCH_COMMITTED' for s in l['slots']),'In-flight requests: leave running worker untouched'
        assert not (W/'STOP_REQUEST').exists(),'Resolve latest user stop explicitly; this installer never deletes it'
        assert l['stop_reason'] in (None,'USER_STOP_REQUESTED'),'Unresolved budget/account/identity stop'
        snapshot=HERE/('install_backup_'+str(time.time_ns()));snapshot.mkdir()
        for name in ('code/full_run.py','run/ledger.json','PRE_DISPATCH_FREEZE.json'):
            shutil.copyfile(W/name,snapshot/pathlib.Path(name).name)
        before=copy.deepcopy(l)
        carry=read(W/'CARRY_IN.json')
        attempts=l['new_attempts']
        A=[a for a in attempts if a.get('credential_source','ORIGINAL_ACCOUNT_A')!='LUNA_ACCOUNT_B']
        B=[a for a in attempts if a.get('credential_source')=='LUNA_ACCOUNT_B']
        known=lambda a:a.get('reservation_state')=='KNOWN'
        l['accounted_usd']=carry['carry_accounted_usd']+sum(a['list_accounted'] for a in A)
        l['unknown_usd']=carry['carry_unknown_usd']+sum(a['list_accounted'] for a in A if not known(a))
        l['sourceB_accounted_usd']=sum(a['list_accounted'] for a in B)
        l['sourceB_unknown_usd']=sum(a['list_accounted'] for a in B if not known(a))
        for field,carry_key in (('list','carry_known_list'),('allowance','carry_known_allowance'),('cash','carry_known_cash')):
            key={'list':'list_cost','allowance':'allowance','cash':'cash_cost'}[field]
            carried=carry.get(carry_key,0.) if field=='cash' else carry[carry_key]
            l['cumulative_known_'+field]=carried+sum(a[key] for a in attempts if known(a))
            l['sourceB_known_'+field]=sum(a[key] for a in B if known(a))
            for model in l['phase_known_list']:
                l['phase_known_'+{'list':'list','allowance':'allowance','cash':'cash'}[field]][model]=sum(a[key] for a in attempts if known(a) and a['model']==model)
        for model in l['phase_allowance_accounted']:
            l['phase_allowance_accounted'][model]=sum(a['allowance_accounted'] for a in attempts if a['model']==model)
        rejects=[a for a in B if a.get('http_status')==429]
        if rejects:
            a=rejects[-1];slot=next(s for s in l['slots'] if s['slot']==a['slot'])
            if slot['status'] not in ('COMPLETE','REUSED_VERIFIED'):
                slot.update(status='SOURCE_B_REJECTED_HOLD',quota_pending=False)
            l['luna_source_stop']={'unix':time.time(),'reason':'Existing source-B HTTP429; no new test call',
                                   'attempt_id':a['attempt_id'],'http_status':429}
        if l['stop_reason']=='USER_STOP_REQUESTED':l['stop_reason']=None
        assert l['commits_total']==before['commits_total'] and l['phase_posts']==before['phase_posts']
        assert l['accounted_usd']+l['sourceB_accounted_usd']<=35,'Corrected cumulative budget already exhausted'
        event={'unix':time.time(),'action':'install tested isolated repair; reconcile arithmetic from existing attempts only',
               'user_authorization':'你修好了让他去启动 然后就让他监控了',
               'old_code_sha256':BASELINE,'new_code_sha256':PATCHED,'backup':str(snapshot),
               'original_attempts_unchanged':l['new_attempts']==before['new_attempts'],
               'no_new_posts':True,'Luna_hold_does_not_pause_Grok':True,
               'money_before':{k:before.get(k) for k in ('accounted_usd','unknown_usd','sourceB_accounted_usd','sourceB_unknown_usd')},
               'money_after':{k:l.get(k) for k in ('accounted_usd','unknown_usd','sourceB_accounted_usd','sourceB_unknown_usd')}}
        l.setdefault('engineering_resume_events',[]).append(event)
        shutil.copyfile(W/'code/full_run_repaired.py',W/'code/full_run.py')
        write(W/'run/ledger.json',l)
        write(W/'logs/DUAL_SOURCE_REPAIR.json',event)
        shutil.copyfile(HERE/'FOCUSED_TEST_RESULTS.json',W/'logs/DUAL_SOURCE_FOCUSED_TEST_RESULTS.json')
        frozen=read(W/'PRE_DISPATCH_FREEZE.json')
        for name in list(frozen)+['logs/DUAL_SOURCE_FOCUSED_TEST_RESULTS.json']:
            frozen[name]=sha(W/name)
        write(W/'PRE_DISPATCH_FREEZE.json',frozen)
        write(HERE/'INSTALLATION_RECORD.json',event)
        print('Installed and frozen. No worker started, no API POST. Executor may start worker_par once locks are released.')
    finally:
        for handle in reversed(handles):handle.close()


if __name__=='__main__':main()
