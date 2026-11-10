"""Final asset gate: all original target steps, identical candidates in five arms.

CLI --package PKG --ledger verified_consumer_rows.tsv --out OUT
Ledger rows cover EVERY original candidate x five arms. Every row refers to
an actual CPU consumer proof JSON and its SHA; missing background can only be
uniformly excluded after a recorded attempt. No model scores are inputs.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ARMS = ('legacy_esm2_3b', 'legacy_esmc600m', 'new_esmc600m', 'current_e0_enzgfm650m', 'new_enzgfm650m')
DIMS = dict(zip(ARMS, (2560, 1152, 1152, 2048, 2048)))


def freeze(package, ledger):
    package = Path(package)
    expected = {}
    parent = {}
    labels = {}
    sequences = {}
    for ctx in ('main', 'delta15'):
        steps = json.loads((package / f'inputs/{ctx}/THREE_B_VERIFIED_PARENT_POOL.json').read_text())
        with (package / f'inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv').open() as f:
            for r in csv.DictReader(f, delimiter='\t'):
                if hashlib.sha256(r['sequence'].encode()).hexdigest() != r['sequence_sha256']:
                    raise ValueError('RUNTIME_SEQUENCE_SHA_MISMATCH')
                sequences[ctx, r['runtime_uid'], r['sequence_sha256']] = r['sequence']
        with (package / f'inputs/{ctx}/EVAL_LABELS_PARENT.tsv').open() as f:
            labels[ctx] = {(r['step_occurrence_id'], r['sequence_sha256']): r['gold_flag'] == 'TRUE'
                           for r in csv.DictReader(f, delimiter='\t')}
        for s in steps:
            parent[ctx, s['step_id']] = s
            for pos, (u, sh) in enumerate(zip(s['pool_uids'], s['pool_shas'])):
                for arm in ARMS:
                    expected[ctx, s['step_id'], pos, arm] = (u, sh)
    seen = {}
    proofs = {}
    with open(ledger) as f:
        for r in csv.DictReader(f, delimiter='\t'):
            key = r['ctx'], r['step_id'], int(r['position']), r['arm']
            if key not in expected or key in seen:
                raise ValueError('LEDGER_DUPLICATE_OR_EXTRA:' + str(key))
            if (r['runtime_uid'], r['sequence_sha256']) != expected[key]:
                raise ValueError('SCIENTIFIC_IDENTITY_MISMATCH:' + str(key))
            p = Path(r['proof_file'])
            if not p.is_absolute():
                p = Path(ledger).parent / p
            raw = p.read_bytes()
            if hashlib.sha256(raw).hexdigest() != r['proof_sha256']:
                raise ValueError('CONSUMER_PROOF_DRIFT:' + str(key))
            proof = json.loads(raw)
            if any(proof.get(k) != r[k] for k in ('arm', 'runtime_uid', 'sequence_sha256')):
                raise ValueError('CONSUMER_PROOF_IDENTITY:' + str(key))
            ok = r['consumable'] == 'TRUE'
            if proof.get('consumable') is not ok:
                raise ValueError('CONSUMER_PROOF_VERDICT:' + str(key))
            if ok:
                if not (proof.get('plm_dim') == DIMS[r['arm']] and proof.get('rows', 0) > 0
                        and proof.get('gvp_rows') == proof.get('rows') and proof.get('finite') is True
                        and proof.get('pairing_verified') is True and proof.get('body_sha_verified') is True
                        and proof.get('real_consumer_pass') is True and proof.get('recipe_identity')):
                    raise ValueError('CONSUMER_PROOF_NOT_COMPLETE:' + str(key))
            elif not (proof.get('attempted_repair') is True and proof.get('typed_reason')):
                raise ValueError('UNATTEMPTED_ASSET_GAP:' + str(key))
            seen[key] = ok
            proofs[key] = proof
    if set(seen) != set(expected):
        raise ValueError('CONSUMER_LEDGER_INCOMPLETE:' + str(len(set(expected) - set(seen))))
    out = defaultdict(list)
    unresolved = []
    for (ctx, sid), s in parent.items():
        keep = [i for i in range(len(s['pool_uids'])) if all(seen[ctx, sid, i, arm] for arm in ARMS)]
        gold = [labels[ctx][sid, s['pool_shas'][i]] for i in keep]
        if not any(gold):
            unresolved.append(sid)
            continue
        entry = {**s, 'pool_uids': [s['pool_uids'][i] for i in keep],
                 'pool_shas': [s['pool_shas'][i] for i in keep], 'gold_flags': gold,
                 'n_gold': sum(gold), 'n_background': len(gold) - sum(gold),
                 'no_discrimination': all(gold)}
        entry['pool_seqs'] = [sequences[ctx, s['pool_uids'][i], s['pool_shas'][i]] for i in keep]
        for arm, field in zip(ARMS, ('asset_uids_3b', 'asset_uids_legacy', 'asset_uids_new', 'asset_uids_e0', 'asset_uids_new_enzgfm')):
            entry[field] = [proofs[ctx, sid, i, arm].get('asset_uid', s['pool_uids'][i]) for i in keep]
        entry['today_batch_flags'] = [any(proofs[ctx, sid, i, arm].get('generated_in_this_round', False) for arm in ARMS) for i in keep]
        entry['rescue_dependent'] = any(g and new for g, new in zip(gold, entry['today_batch_flags']))
        out[ctx].append(entry)
    if unresolved:
        raise ValueError('TARGET_STEPS_NOT_READY:' + ';'.join(unresolved))
    return dict(out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--package', required=True)
    ap.add_argument('--ledger', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = Path(a.out)
    # Revoke stale gate before validating any changed ledger.
    if (out / 'ALL_MODELS_ASSETS_READY.json').exists():
        (out / 'ALL_MODELS_ASSETS_READY.json').unlink()
    tables = freeze(a.package, a.ledger)
    out.mkdir(parents=True, exist_ok=True)
    for ctx, steps in tables.items():
        (out / f'UNIFIED_STEP_TABLE_{ctx}.json').write_text(json.dumps(steps))
    receipt = {'status': 'ALL_MODELS_ASSETS_READY', 'arms': ARMS,
               'steps': sum(len(v) for v in tables.values()),
               'consumer_ledger_path': str(Path(a.ledger).resolve()),
               'consumer_ledger_sha256': hashlib.sha256(Path(a.ledger).read_bytes()).hexdigest(),
               'step_table_sha256': {ctx: hashlib.sha256((out / f'UNIFIED_STEP_TABLE_{ctx}.json').read_bytes()).hexdigest() for ctx in tables},
               'scope': 'ASSET_READINESS_ONLY_NUMERICAL_CONTROLS_SEPARATE', 'model_forward_executed_by_gate': False}
    (out / 'ALL_MODELS_ASSETS_READY.json').write_text(json.dumps(receipt, indent=2))
    print(json.dumps(receipt))
