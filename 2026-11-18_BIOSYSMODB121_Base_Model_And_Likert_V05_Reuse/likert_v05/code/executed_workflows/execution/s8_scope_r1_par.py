"""S8 scope_r1 PARALLEL batch: same contracts, K concurrent slots.

Threaded dispatcher over the same 293-row plan. Ledger, archive, RESULTS and
credential-state mutations stay serialized under one in-process lock; only
HTTP streaming runs concurrently, so request COUNT is identical to serial —
parallelism buys wall-clock time, never extra purchases.

Restart-orphan policy: inflight transfers left by the killed serial runner
are reconciled by the ledger into kept unknown reserves; each affected slot
gets exactly ONE documented retry (its stream was cut by our restart, so no
recoverable response exists; the orphan reserve itself is never erased).
Any OTHER ledger-unknown slot without a recorded attempt is held, not re-bought.
Key rotation only on provably not-billed auth/quota refusals; 429 gets one
same-alias backoff; scoring-side rejection never re-buys or rotates.
"""
import fcntl
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s8_scope_r1_run as ORIG
import s8_credentials as CRE
import ne_repair as BASE
import scoped_ne_repair as SC
from f2r12_common import utc_now_iso, totals_contract
from f2r12_budget_ledger import BudgetLedger
from f2r12_transport import LiveTransport
from f2r12_cache_checkpoint import AttemptArchive

OUT = ORIG.OUT
LEDGER_DIR = ORIG.LEDGER
PREFIX = ORIG.PREFIX
VERSION = ORIG.VERSION
MODEL = ORIG.MODEL
STATE = threading.Lock()
_tls = threading.local()
log = ORIG.log


def transport_for(cred):
    cache = _tls.__dict__.setdefault('transports', {})
    key = (cred['alias'], cred['endpoint'])
    if key not in cache:
        cache[key] = LiveTransport(cred['endpoint'], cred['key'], session=None, stream=True)
    return cache[key]


def _persist_bad(bad, alias, excerpt):
    p = OUT / 'CREDENTIAL_STATE.json'
    old = json.loads(p.read_text()) if p.exists() else {}
    old['round_bad'] = sorted(bad)
    old.setdefault('detail', {})[alias] = dict(excerpt=excerpt, utc=utc_now_iso())
    p.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n')


def process_slot(row, man, creds, ledger, archive, secrets, bad):
    slot = row['slot']
    wanted = row['requested_dimensions'].split(',')
    try:
        req = SC.build(slot, wanted)
    except Exception as exc:
        ORIG._record(dict(slot=slot, status='BUILD_FAIL', dims=wanted,
                          error=f'{type(exc).__name__}: {exc}', utc=utc_now_iso()))
        return False, slot
    if req['body_sha256'] != man[slot]['request_sha256']:
        ORIG._record(dict(slot=slot, status='PRECHECK_FAIL', dims=wanted,
                          note='rebuilt request differs from binding manifest', utc=utc_now_iso()))
        return False, slot
    sends = 0
    for cred in creds:
        alias = cred['alias']
        with STATE:
            if alias in bad:
                continue
        backoff_wait = False
        for attempt in range(2):
            if sends >= 6 or backoff_wait:
                if backoff_wait:
                    backoff_wait = False
                    time.sleep(90)
                else:
                    break
            with STATE:
                seq = ledger.next_transfer_seq()
                tid = f'{PREFIX}#{slot}#t{seq}'
                ledger.reserve(tid, slot, reserve_cny=2.0)
                log(event='DISPATCH', slot=slot, dims=wanted, transfer=tid, alias=alias,
                    body_sha=req['body_sha256'][:16], attempt=attempt, utc=utc_now_iso())
            wire = transport_for(cred).send(dict(endpoint=cred['endpoint'], body=req['body'],
                                                 item_identity=req['identity']), 1800)
            with STATE:
                sends += 1
                archive.store(tid, wire, json.dumps(req['body'], ensure_ascii=False).encode(),
                              req['identity'], run_identity=VERSION, attempt_index=0)
                settle = ledger.settle_by_transport(tid, dict(
                    usage=wire.get('usage'), http_status=wire.get('http_status'),
                    response_received=wire.get('raw_response_bytes') is not None,
                    may_have_billed=wire.get('may_have_billed', False),
                    error_kind=wire.get('error_kind')), 2., 8.)
                rec = dict(slot=slot, transfer_id=tid, alias=alias, dims=wanted,
                           body_sha256=req['body_sha256'], status='TECHNICAL_FAILURE',
                           http_status=wire.get('http_status'), stream_status=wire.get('stream_status'),
                           error_kind=wire.get('error_kind'), usage=wire.get('usage'),
                           settle_mode=settle.get('mode'), utc=utc_now_iso())
                usable = (wire.get('http_status') == 200
                          and wire.get('stream_status') == 'COMPLETE')
                if usable:
                    try:
                        if wire.get('model_returned') not in (None, MODEL):
                            raise RuntimeError('MODEL_DRIFT')
                        obj = json.loads(wire.get('content_text') or '')
                        if set(obj.get('dimensions') or {}) != set(wanted):
                            raise ValueError('unexpected requested dimensions')
                        errors, reviews = BASE.validate(obj, req)
                        if not errors:
                            merged = BASE.merge_validated(obj, req, tid, totals_contract)
                            (OUT / 'merged').mkdir(exist_ok=True)
                            (OUT / 'responses').mkdir(exist_ok=True)
                            (OUT / 'merged' / f'MERGED_{slot}.json').write_text(
                                json.dumps(merged, ensure_ascii=False, indent=2) + '\n')
                            (OUT / 'responses' / f'RESPONSE_{slot}.json').write_text(
                                json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
                            rec.update(status='OK', errors=[], reviews=reviews,
                                       totals=merged['totals'],
                                       residual_NE=merged['residual_NE_dimensions'])
                            ORIG._record(rec)
                            return True, slot
                        rec.update(status='VALIDATION_REJECTED', errors=errors, reviews=reviews,
                                   raw_excerpt=CRE.scrub(json.dumps(obj, ensure_ascii=False)[:1500], secrets))
                        ORIG._record(rec)
                        return False, slot
                    except Exception as exc:
                        rec.update(status='RESPONSE_PROTOCOL_FAIL',
                                   error=f'{type(exc).__name__}: {exc}')
                        ORIG._record(rec)
                        return False, slot
                cls = CRE.classify(wire)
                if cls == 'SWITCH':
                    rec.update(status='CREDENTIAL_REFUSED', fail_class=cls,
                               excerpt=CRE.scrub(wire.get('raw_response_bytes'), secrets))
                    ORIG._record(rec)
                    bad.add(alias)
                    _persist_bad(bad, alias, rec['excerpt'])
                    log(event='ALIAS_UNAVAILABLE', slot=slot, alias=alias)
                    break  # outer: next alias
                if cls == 'BACKOFF':
                    rec.update(status='RATE_LIMIT', fail_class=cls)
                    ORIG._record(rec)
                    if attempt == 0:
                        backoff_wait = True  # sleep+retry SAME alias once
                        continue
                    break  # still limited: next alias
                if cls == 'PRE_DISPATCH':
                    rec.update(status='PRE_DISPATCH_FAIL', fail_class=cls)
                    ORIG._record(rec)
                    break  # next alias once; systemic failure surfaces across slots
                rec.update(status='UNKNOWN_BILLED_HOLD', fail_class=cls)
                ORIG._record(rec)
                log(event='SLOT_HOLD_UNKNOWN', slot=slot, alias=alias)
                return False, slot
        if sends >= 6:
            break
    if len(bad) >= len(creds):
        log(event='ALL_CREDENTIALS_UNAVAILABLE', slot=slot)
    return False, slot


def main():
    mode = sys.argv[-1] if len(sys.argv) > 1 else '4'
    if mode == 'selfcheck':
        ORIG.main()
        return
    K = int(mode) if mode.isdigit() else 4
    creds = CRE.load_credentials(expected_model=MODEL)
    assert creds, 'NO_CREDENTIALS'
    secrets = [c['key'] for c in creds]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'logs').mkdir(exist_ok=True)
    lock = open(ORIG.S6 / 'work/LOCK', 'a+')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log(event='ABORT', reason='S6 work lock held elsewhere')
        sys.exit(2)
    (HERE / 'ACTIVE_RUN.json').write_text(json.dumps(dict(
        pid=os.getpid(), script=str(Path(__file__)), mode=f'parallel-{K}', round=VERSION,
        prefix=PREFIX, log=str(OUT / 'logs/RUN.log'), automatic_retries=False), indent=2) + '\n')
    cfg = json.loads((ORIG.S6 / 'input/config/RUN_CONFIG_LIVE.json').read_text())
    default_endpoint = cfg['scoring_ai']['recommended']['endpoint']
    for c in creds:
        c['endpoint'] = c['endpoint'] or default_endpoint
    ledger = BudgetLedger(str(LEDGER_DIR), 1000, 1200, 2.0, max_transfers_per_target=20)
    # reconcile first: the killed serial runner may have left one inflight
    # transfer, which preflight's no-inflight assertion would refuse.
    if ledger.reconcile_on_startup():
        st = json.loads((LEDGER_DIR / 'BUDGET_STATE.json').read_text())
        for tid, v in st['unknown_reserves'].items():
            if tid.startswith(PREFIX + '#') and v.get('reason') == 'RECONCILED_AFTER_RESTART_UNKNOWN_INFLIGHT':
                ORIG._record(dict(slot=v['slot_uid'], transfer_id=tid, alias='orphan', dims=None,
                                  status='RESTART_ORPHAN_UNKNOWN', orphan=True,
                                  note='serial runner killed mid-stream; reserve kept; one retry allowed',
                                  utc=utc_now_iso()))
                log(event='ORPHAN_RECORDED', slot=v['slot_uid'], transfer=tid)
    binding, man, _ = ORIG.preflight()
    archive = AttemptArchive(str(OUT / 'work/attempts'))
    plan = ORIG.load_plan()
    state = ORIG.round_state()
    led = json.loads((LEDGER_DIR / 'BUDGET_STATE.json').read_text())
    orphan_allowed = {v['slot_uid'] for k, v in led['unknown_reserves'].items()
                      if k.startswith(PREFIX + '#') and v.get('reason') == 'RECONCILED_AFTER_RESTART_UNKNOWN_INFLIGHT'}
    unknown_slots = {v['slot_uid'] for k, v in led['unknown_reserves'].items() if k.startswith(PREFIX + '#')}
    bad = set()
    p = OUT / 'CREDENTIAL_STATE.json'
    if p.exists():
        bad = set(json.loads(p.read_text()).get('round_bad', []))
    todo = []
    for row in plan:
        slot = row['slot']
        st = state.get(slot, {})
        if st.get('ok') or st.get('billable'):
            continue
        if slot in unknown_slots and slot not in orphan_allowed:
            ORIG._record(dict(slot=slot, status='LEDGER_UNKNOWN_HOLD',
                              note='unknown-billed transfer without attempt record; held, not re-bought',
                              utc=utc_now_iso()))
            log(event='LEDGER_UNKNOWN_HOLD', slot=slot)
            continue
        todo.append(row)
    log(event='PARALLEL_START', K=K, todo=len(todo), round_bad=sorted(bad))
    done = 0
    results = []

    def safe(r):
        try:
            return process_slot(r, man, creds, ledger, archive, secrets, bad)
        except Exception as exc:
            with STATE:
                ORIG._record(dict(slot=r['slot'], status='TASK_EXCEPTION',
                                  error=f'{type(exc).__name__}: {exc}', utc=utc_now_iso()))
            return False, r['slot']

    with ThreadPoolExecutor(max_workers=K) as pool:
        for ok, slot in pool.map(safe, todo):
            done += 1
            prog = ORIG._progress(plan)
            (OUT / 'PROGRESS.json').write_text(json.dumps(prog, ensure_ascii=False, indent=2) + '\n')
            log(event='SLOT_DONE', slot=slot, ok=ok, seq=done, of=len(todo),
                done=prog['done'], remaining=prog['remaining'],
                attempts=prog['ledger']['attempts_used'],
                spend=round(prog['ledger']['committed_spend_cny'], 4), round_bad=sorted(bad))
            results.append(ok)
    prog = ORIG._progress(plan)
    prog['finished_utc'] = utc_now_iso()
    (OUT / 'PROGRESS.json').write_text(json.dumps(prog, ensure_ascii=False, indent=2) + '\n')
    log(event='RUN_STOP', done=prog['done'], ok=prog['ok'], failed_or_held=prog['failed_or_held'],
        remaining=prog['remaining'], attempts=prog['ledger']['attempts_used'],
        spend=prog['ledger']['committed_spend_cny'])


if __name__ == '__main__':
    main()
