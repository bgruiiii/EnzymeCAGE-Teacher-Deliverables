"""S8 scope_r1 batch: 293 remaining old-NE answers with credential rotation.

Thin continuation of the pilot runner: same F2 transport/archive/budget
components, the SAME live ledger (execution/work/ledger), the original S8
validator and merger, and scoped_ne_repair.build for input path-scope wiring.
Keys rotate ONLY on provably-not-billed auth/quota refusals; scored or
unknown-billed attempts are never re-bought; scoring-side rejection stops the
slot but not the batch. Logs and archives contain alias IDs only, never keys.
"""
import csv
import fcntl
import hashlib
import json
import os
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
S8 = HERE.parent
REL = S8.parent
Q = S8 / 'scope_fix_20261114'
S6 = REL / 'S6_COMBINED_V05_SCORING_20261111'
sys.path[:0] = [str(S6 / 'runtime/v05_release'), str(S6 / 'runtime/f2'),
                str(S6 / 'runtime/pipeline'), str(S8), str(Q)]
import ne_repair as BASE
import scoped_ne_repair as SC
import s8_credentials as CRE
from f2r12_common import utc_now_iso, totals_contract
from f2r12_budget_ledger import BudgetLedger
from f2r12_transport import LiveTransport
from f2r12_cache_checkpoint import AttemptArchive

load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
OUT = HERE / 'scope_r1'
LEDGER = HERE / 'work' / 'ledger'
PREFIX = 'S8R1_20261114'
VERSION = SC.VERSION
MODEL = BASE.MODEL
PILOT_EXCLUDE = set(BASE.PILOT)
BILLABLE_SETTLE = {'ACTUAL_USAGE', 'UNKNOWN_KEPT'}


def log(**ev):
    print(json.dumps(ev, ensure_ascii=False), flush=True)


def load_plan():
    rows = list(csv.DictReader((Q / 'REMAINING_NE_TARGETS.tsv').open(), delimiter='\t'))
    assert len(rows) == 293 and sum(len(r['requested_dimensions'].split(',')) for r in rows) == 546
    assert not (set(r['slot'] for r in rows) & PILOT_EXCLUDE), 'PILOT_IN_PLAN'
    return rows


def preflight():
    binding = load(Q / 'INPUT_SCOPE_FIX_BINDING.json')
    assert binding['repair_version'] == VERSION
    assert binding['remaining_answer_targets'] == 293 and binding['remaining_NE_dimensions'] == 546
    assert sha(S8 / 'ne_repair.py') == binding['source_module_sha256'], 'NE_REPAIR_DRIFT'
    assert sha(S8 / 'execution' / 'work' / 'RESULTS.jsonl') == binding['pilot_result_sha256'], 'PILOT_RESULTS_DRIFT'
    checks = load(Q / 'OFFLINE_SCOPE_CHECKS.json')
    assert checks.get('PASS') is True, 'OFFLINE_CHECKS_FAIL'
    led = load(LEDGER / 'BUDGET_STATE.json')
    assert led['attempts_used'] >= 808 and not led['inflight'], 'LEDGER_PRECONDITION'
    man = {r['slot']: r for r in binding['requests']}
    assert len(man) == 293
    kinds = {'true': None, 'false': None}
    for s in man.values():
        k = str(s['branch_scope_attached']).lower()
        if kinds[k] is None:
            kinds[k] = s
        if kinds['true'] and kinds['false']:
            break
    samples = [x for x in kinds.values() if x]
    for s in samples:
        req = SC.build(s['slot'], s['wanted'])
        assert req['body_sha256'] == s['request_sha256'], f"MANIFEST_DRIFT_{s['slot']}"
        assert req['identity']['repair_identity_sha256'] == s['identity_sha256'], f"IDENTITY_DRIFT_{s['slot']}"
    return binding, man, samples


def round_state():
    by = {}
    p = OUT / 'RESULTS.jsonl'
    if p.exists():
        for x in map(json.loads, p.read_text().splitlines()):
            rec = by.setdefault(x['slot'], dict(ok=False, billable=False, aliases=set()))
            rec['aliases'].add(x.get('alias'))
            if x.get('status') == 'OK':
                rec['ok'] = True
            if x.get('settle_mode') in BILLABLE_SETTLE or (x.get('http_status') == 200):
                rec['billable'] = True
    return by


def attempt_slot(slot, wanted, req, man_row, creds, transports, ledger, archive, secrets, bad):
    """Send at most once per usable alias (429 gets one backoff retry each);
    global send cap 6. Returns (scored, global_stop_reason)."""
    if req['body_sha256'] != man_row['request_sha256']:
        _record(dict(slot=slot, status='PRECHECK_FAIL', dims=wanted, alias=None,
                     note='rebuilt request differs from binding manifest', utc=utc_now_iso()))
        log(event='PRECHECK_FAIL', slot=slot)
        return False, None
    sends = 0
    for cred in creds:
        alias = cred['alias']
        if alias in bad:
            continue
        for backoff in range(2):
            if sends >= 6:
                break
            sends += 1
            seq = ledger.next_transfer_seq()
            tid = f'{PREFIX}#{slot}#t{seq}'
            ledger.reserve(tid, slot, reserve_cny=2.0)
            log(event='DISPATCH', slot=slot, dims=wanted, transfer=tid, alias=alias,
                body_sha=req['body_sha256'][:16], backoff=backoff, utc=utc_now_iso())
            wire = transports[alias].send(dict(endpoint=cred['endpoint'], body=req['body'],
                                               item_identity=req['identity']), 1800)
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
            usable_response = (wire.get('http_status') == 200
                               and wire.get('stream_status') == 'COMPLETE')
            if usable_response:
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
                                   totals=merged['totals'], residual_NE=merged['residual_NE_dimensions'])
                        _record(rec)
                        return True, None
                    rec.update(status='VALIDATION_REJECTED', errors=errors, reviews=reviews,
                               raw_excerpt=CRE.scrub(json.dumps(obj, ensure_ascii=False)[:1500], secrets))
                    _record(rec)
                    log(event='SLOT_REJECTED_NO_REBUY', slot=slot, alias=alias, errors=errors)
                    return False, None  # scoring-side issue: never a key-switch or rebuy reason
                except Exception as exc:
                    rec.update(status='RESPONSE_PROTOCOL_FAIL',
                               error=f'{type(exc).__name__}: {exc}')
                    _record(rec)
                    return False, None  # streamed response billed-ish; hold, no rotation
            cls = CRE.classify(wire)
            if cls == 'SWITCH':
                rec.update(status='CREDENTIAL_REFUSED', fail_class=cls,
                           excerpt=CRE.scrub(wire.get('raw_response_bytes'), secrets))
                _record(rec)
                bad.add(alias)
                _save_bad(bad, alias, rec['excerpt'])
                log(event='ALIAS_UNAVAILABLE', slot=slot, alias=alias)
                break  # next alias
            if cls == 'BACKOFF':
                rec.update(status='RATE_LIMIT', fail_class=cls)
                _record(rec)
                if backoff == 0:
                    time.sleep(90)
                    continue
                break  # give up this alias for this slot; try next
            if cls == 'PRE_DISPATCH':
                rec.update(status='PRE_DISPATCH_FAIL', fail_class=cls)
                _record(rec)
                break  # next alias once; systemic net failure surfaces across slots
            rec.update(status='UNKNOWN_BILLED_HOLD', fail_class=cls)
            _record(rec)
            log(event='SLOT_HOLD_UNKNOWN', slot=slot, alias=alias)
            return False, None  # possible-billing outcome: keep reserve, no blind rotation
    if len(bad) >= len(creds):
        return False, 'ALL_CREDENTIALS_UNAVAILABLE'
    return False, None


def _record(rec):
    with (OUT / 'RESULTS.jsonl').open('a') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        f.flush()
        os.fsync(f.fileno())


def _save_bad(bad, alias, excerpt):
    p = OUT / 'CREDENTIAL_STATE.json'
    old = load(p) if p.exists() else {}
    old['round_bad'] = sorted(bad)
    old.setdefault('detail', {})[alias] = dict(excerpt=excerpt, utc=utc_now_iso())
    p.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n')


def _progress(plan):
    state = round_state()
    led = load(LEDGER / 'BUDGET_STATE.json')
    ok = sum(1 for r in plan if state.get(r['slot'], {}).get('ok'))
    attempted = sum(1 for r in plan if r['slot'] in state)
    return dict(done=ok, ok=ok, failed_or_held=attempted - ok, remaining=len(plan) - ok,
                ledger=dict(attempts_used=led['attempts_used'],
                            committed_spend_cny=led['committed_spend_cny'],
                            unknown_reserves=len(led['unknown_reserves']),
                            inflight=len(led['inflight'])))


def main():
    mode = sys.argv[-1] if len(sys.argv) > 1 else 'run'
    creds = CRE.load_credentials(expected_model=MODEL)
    assert creds, 'NO_CREDENTIALS'
    secrets = [c['key'] for c in creds]
    if mode == 'selfcheck':
        binding, man, samples = preflight()
        led = load(LEDGER / 'BUDGET_STATE.json')
        log(event='SELFCHECK_OK', aliases=[c['alias'] for c in creds],
            hosts=sorted({(c['endpoint'] or 'RUN_CONFIG').split('//')[-1].split('/')[0] for c in creds}),
            sample_slots=[s['slot'] for s in samples], attempts_now=led['attempts_used'],
            spend_now=led['committed_spend_cny'])
        return
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'logs').mkdir(exist_ok=True)
    lock = open(S6 / 'work/LOCK', 'a+')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log(event='ABORT', reason='S6 work lock held elsewhere')
        sys.exit(2)
    (HERE / 'ACTIVE_RUN.json').write_text(json.dumps(dict(
        pid=os.getpid(), script=str(Path(__file__)), mode=mode, round=VERSION,
        prefix=PREFIX, log=str(OUT / 'logs/RUN.log'), automatic_retries=False), indent=2) + '\n')
    binding, man, _ = preflight()
    cfg = load(S6 / 'input/config/RUN_CONFIG_LIVE.json')
    default_endpoint = cfg['scoring_ai']['recommended']['endpoint']
    ledger = BudgetLedger(str(LEDGER), 1000, 1200, 2.0, max_transfers_per_target=20)
    ledger.reconcile_on_startup()
    archive = AttemptArchive(str(OUT / 'work/attempts'))
    transports = {}
    for c in creds:
        c['endpoint'] = c['endpoint'] or default_endpoint
        transports[c['alias']] = LiveTransport(c['endpoint'], c['key'], session=None, stream=True)
    (OUT / 'RUN_MANIFEST.json').write_text(json.dumps(dict(
        version=VERSION, prefix=PREFIX, aliases=[c['alias'] for c in creds],
        endpoints={c['alias']: c['endpoint'].split('//')[-1].split('/')[0] for c in creds},
        gates=dict(money_cny=1000, attempts=1200), pilot_excluded=sorted(PILOT_EXCLUDE),
        binding_sha=sha(Q / 'INPUT_SCOPE_FIX_BINDING.json'), started=utc_now_iso()), indent=2) + '\n')

    plan = load_plan()
    state = round_state()
    bad = set()
    p = OUT / 'CREDENTIAL_STATE.json'
    if p.exists():
        bad = set(load(p).get('round_bad', []))
    global_stop = None
    for row in plan:
        slot = row['slot']
        st = state.get(slot, {})
        if st.get('ok') or st.get('billable'):
            continue
        wanted = row['requested_dimensions'].split(',')
        req = SC.build(slot, wanted)
        scored, gstop = attempt_slot(slot, wanted, req, man[slot], creds, transports,
                                     ledger, archive, secrets, bad)
        if gstop:
            global_stop = gstop
            break
        prog = _progress(plan)
        log(event='SLOT_DONE', slot=slot, ok=scored, done=prog['done'],
            remaining=prog['remaining'], attempts=prog['ledger']['attempts_used'],
            spend=round(prog['ledger']['committed_spend_cny'], 4), round_bad=sorted(bad))
        (OUT / 'PROGRESS.json').write_text(json.dumps(prog, ensure_ascii=False, indent=2) + '\n')
    prog = _progress(plan)
    prog['stop_reason'] = global_stop
    prog['finished_utc'] = utc_now_iso()
    (OUT / 'PROGRESS.json').write_text(json.dumps(prog, ensure_ascii=False, indent=2) + '\n')
    log(event='RUN_STOP', done=prog['done'], ok=prog['ok'], failed_or_held=prog['failed_or_held'],
        remaining=prog['remaining'], stop_reason=global_stop,
        attempts=prog['ledger']['attempts_used'], spend=prog['ledger']['committed_spend_cny'])


if __name__ == '__main__':
    main()
