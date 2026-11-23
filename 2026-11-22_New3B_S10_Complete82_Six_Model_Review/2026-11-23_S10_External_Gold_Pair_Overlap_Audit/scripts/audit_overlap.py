#!/usr/bin/env python3
"""Two explicitly separated stages: match/seal masks, then reuse old metrics."""
import argparse
import ast
import csv
import gzip
import hashlib
import json
import math
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

from rdkit import Chem, RDLogger, rdBase

RDLogger.DisableLog('rdApp.*')
ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT.parent
PUB = ROOT / 'public'
SPLITS = ('train', 'valid', 'test')
VIEWS = ('ALL_SCORED382', 'COMPLETE82_STEP338')
EXPECTED_PROTOCOL = '7140c11269fe0138c66dfbfefc8180383a6edc744ffd5551f44c51fd8833c34d'
C2 = RUN / 'ENZYME_HOST_C2_C3_EXPORT_20261118/STEP_CANDIDATE_RANKINGS.tsv.gz'
METRICS = RUN / 'NEW3B_S10_SISTER_DELIVERY_20261122/NEW3B_S10_COMPLETE82_SIX_MODEL_REVIEW/SIX_MODEL_STEP_RESULTS_2292.tsv'
LEDGER = RUN / 'ENZYME_HOST_C3_METHODS_STAGE_ACCOUNTING_CLOSEOUT_20261120/reviewed_20261120/STEP_MEMBERSHIP_LEDGER_411.tsv'
EXPORT = ROOT / 'private_inputs/S10_POSITIVE_ROWS_SOURCE_BOUND.jsonl.gz'
FIELDS = ('hit_at_1', 'hit_at_3', 'hit_at_5', 'hit_at_10', 'mrr', 'mrr_at_10')


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''):
            h.update(b)
    return h.hexdigest()


def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def table(p, rows):
    assert rows
    with p.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def readtable(p):
    op = gzip.open if p.suffix == '.gz' else open
    with op(p, 'rt') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def original_s7_group(reaction):
    left, _, right = reaction.partition('>>')
    a, b = sorted([reaction, right + '>>' + left])
    return 'ISG_' + hashlib.sha256((a + '\n' + b).encode('utf-8')).hexdigest()


@lru_cache(maxsize=None)
def component_key(smiles, strip_stereo=False):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        raise ValueError('RDKit parse/sanitize failed')
    for a in m.GetAtoms():
        a.SetAtomMapNum(0)
    m = Chem.RemoveHs(m)
    if strip_stereo:
        Chem.RemoveStereochemistry(m)
    return Chem.MolToSmiles(m, canonical=True, isomericSmiles=True)


@lru_cache(maxsize=None)
def canonical(reaction, strip_stereo=False):
    sides = reaction.split('>>')
    if len(sides) != 2 or not all(sides):
        raise ValueError('expected two nonempty reaction sides separated by >>')
    return '>>'.join('.'.join(sorted(component_key(x, strip_stereo) for x in side.split('.')))
                     for side in sides)


def normalization_controls():
    checks = {
        'same_graph_different_spelling': canonical('C(C)O>>CC=O') == canonical('CCO>>O=CC'),
        'component_order_ignored': canonical('O.CCO>>O.CC=O') == canonical('CCO.O>>CC=O.O'),
        'atom_maps_ignored': canonical('[CH3:4][OH:2]>>[CH2:4]=[O:2]') == canonical('CO>>C=O'),
        'direction_preserved': canonical('CCO>>CC=O') != canonical('CC=O>>CCO'),
        'specified_stereochemistry_preserved': canonical('N[C@H](C)C(=O)O>>CC') != canonical('N[C@@H](C)C(=O)O>>CC'),
        'stereo_secondary_only': canonical('N[C@H](C)C(=O)O>>CC', True) == canonical('N[C@@H](C)C(=O)O>>CC', True),
        'unspecified_not_equated_to_specified': canonical('NC(C)C(=O)O>>CC') != canonical('N[C@H](C)C(=O)O>>CC'),
        'multiplicity_preserved': canonical('O.O>>O') != canonical('O>>O'),
        'charge_preserved': canonical('C[O-]>>C=O') != canonical('CO>>C=O'),
        'isotopes_preserved': canonical('[13CH3]O>>C=O') != canonical('CO>>C=O'),
        'tautomers_not_collapsed': canonical('CC=O>>CC') != canonical('C=CO>>CC'),
        'dummy_preserved_without_substructure_expansion': canonical('*C>>CO') != canonical('CC>>CO'),
        'family_reverse_same': original_s7_group('CCO>>CC=O') == original_s7_group('CC=O>>CCO'),
    }
    for bad in ('not-a-reaction', 'invalid>>CC'):
        try:
            canonical(bad)
        except ValueError:
            checks['parse_failure_rejected:' + bad] = True
        else:
            checks['parse_failure_rejected:' + bad] = False
    tree = ast.parse((ROOT / 'evidence/s7_reaction_group_split.py').read_text())
    fn = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'isg')
    scope = {'hashlib': hashlib}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), '<original-isg-function-only>', 'exec'), scope)
    checks['original_s7_function_matches'] = all(original_s7_group(x) == scope['isg'](x)
        for x in ['CCO>>CC=O', 'O.CCO>>O.CC=O', 'N[C@H](C)C(=O)O>>CC'])
    assert all(checks.values()), checks
    return checks


def external_identity():
    steps = {}
    uid_steps = defaultdict(set)
    with gzip.open(C2, 'rt') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['arm'] != 'legacy_esm2_3b':
                continue
            sid = r['step_id']
            s = steps.setdefault(sid, {'step_id': sid, 'case_id': r['case_id'], 'ctx': r['ctx'],
                'reaction': r['model_reaction'], 'model_key_sha256': r['model_key_sha256'],
                'in_complete82': r['in_complete82'] == 'True', 'candidates': {}, 'gold': {}})
            assert s['reaction'] == r['model_reaction'] and s['case_id'] == r['case_id']
            assert hashlib.sha256(s['reaction'].encode()).hexdigest() == s['model_key_sha256']
            assert r['scientific_uid'] not in s['candidates']
            s['candidates'][r['scientific_uid']] = r['sequence_sha256']
            uid_steps[r['scientific_uid']].add(sid)
            if r['gold_flag'] == 'TRUE':
                s['gold'][r['scientific_uid']] = r['sequence_sha256']
    assert len(steps) == 382 and sum(s['in_complete82'] for s in steps.values()) == 338
    assert len(uid_steps) == 7468 and sum(len(s['candidates']) for s in steps.values()) == 16448
    assert sum(len(s['gold']) for s in steps.values()) == 841
    assert sum(len(s['gold']) for s in steps.values() if s['in_complete82']) == 739
    lm = {x['step_id']: x for x in readtable(LEDGER)}
    assert {k for k, s in lm.items() if s['scored'] == 'True'} == set(steps)
    assert {k for k, s in lm.items() if s['in_scored338'] == 'True'} == {k for k, s in steps.items() if s['in_complete82']}
    return steps, uid_steps


def match():
    assert sha(ROOT / 'PROTOCOL_FROZEN_BEFORE_COUNTS.json') == EXPECTED_PROTOCOL
    assert not (PUB / 'MASKS_SEALED_BEFORE_METRICS.json').exists(), 'Never overwrite an existing mask seal'
    controls = normalization_controls()
    steps, uid_steps = external_identity()
    receipts = {}
    indices = {s: {'rxn': set(), 'nostereo': set(), 'groups': set(), 'uids': set(),
                   'uidpairs': defaultdict(list), 'seqpairs': defaultdict(list),
                   'uidpairs_nostereo': set(), 'seqpairs_nostereo': set()} for s in SPLITS}
    errors = []
    source_rows = 0
    with gzip.open(EXPORT, 'rt') as f:
        for line in f:
            r = json.loads(line)
            sp = r['split']
            if r['kind'] == 'source_receipt':
                assert sp not in receipts
                receipts[sp] = r
                continue
            assert r['kind'] == 'positive'
            source_rows += 1
            idx = indices[sp]
            assert original_s7_group(r['reaction']) == r['internal_split_group']
            try:
                ck, ns = canonical(r['reaction']), canonical(r['reaction'], True)
            except ValueError as exc:
                errors.append({'source': sp, 'record': r['csv_record_number_including_header'], 'error': str(exc)})
                continue
            idx['rxn'].add(ck)
            idx['nostereo'].add(ns)
            idx['groups'].add(r['internal_split_group'])
            idx['uids'].add(r['uid'])
            witness = {'record': r['csv_record_number_including_header'], 'uid': r['uid'],
                       'sequence_sha256': r['sequence_sha256'], 'raw_reaction': r['reaction']}
            idx['uidpairs'][ck, r['uid']].append(witness)
            idx['seqpairs'][ck, r['sequence_sha256']].append(witness)
            idx['uidpairs_nostereo'].add((ns, r['uid']))
            idx['seqpairs_nostereo'].add((ns, r['sequence_sha256']))
    assert set(receipts) == set(SPLITS) and source_rows == 112245
    counts = {x['split']: x for x in readtable(RUN / 'NEW3B_S10_SISTER_DELIVERY_20261122/NEW3B_S10_COMPLETE82_SIX_MODEL_REVIEW/TRAINING_SPLITS_S10.tsv')}
    for sp, r in receipts.items():
        assert r['sha256_start'] == r['sha256_end'] == counts[sp]['csv_sha256']
        assert r['total_rows'] == int(counts[sp]['rows'])
        assert r['positive_unique_uids'] == len(indices[sp]['uids'])
    norm_rows, step_rows, pair_rows = [], [], []
    for sid, s in sorted(steps.items()):
        try:
            ck, ns = canonical(s['reaction']), canonical(s['reaction'], True)
        except ValueError as exc:
            errors.append({'source': 'external', 'step_id': sid, 'error': str(exc)})
            continue
        family = original_s7_group(s['reaction'])
        norm_rows.append({'step_id': sid, 'case_id': s['case_id'], 'in_complete82': s['in_complete82'],
            'original_model_reaction': s['reaction'], 'model_key_sha256': s['model_key_sha256'],
            'rdkit_canonical_stereo_preserved': ck, 'rdkit_canonical_stereo_removed': ns,
            'original_s7_exact_forward_reverse_group': family, 'normalization_status': 'OK'})
        row = {'step_id': sid, 'case_id': s['case_id'], 'in_complete82': s['in_complete82'],
               'n_candidates': len(s['candidates']), 'n_gold_uid_pairs': len(s['gold'])}
        reverse = '>>'.join(ck.split('>>')[::-1])
        for sp in SPLITS:
            idx = indices[sp]
            uidn = seqn = uidns = seqns = 0
            for uid, seqsha in sorted(s['gold'].items()):
                uw, sw = idx['uidpairs'].get((ck, uid), []), idx['seqpairs'].get((ck, seqsha), [])
                uidn += bool(uw)
                seqn += bool(sw)
                uidns += (ns, uid) in idx['uidpairs_nostereo']
                seqns += (ns, seqsha) in idx['seqpairs_nostereo']
                pair_rows.append({'step_id': sid, 'case_id': s['case_id'], 'in_complete82': s['in_complete82'],
                    'split': sp, 'gold_uid': uid, 'gold_sequence_sha256': seqsha,
                    'canonical_reaction_sha256': hashlib.sha256(ck.encode()).hexdigest(),
                    'exact_uid_pair_positive_match': bool(uw), 'exact_sequence_pair_positive_match': bool(sw),
                    'stereo_removed_uid_pair_match': (ns, uid) in idx['uidpairs_nostereo'],
                    'stereo_removed_sequence_pair_match': (ns, seqsha) in idx['seqpairs_nostereo'],
                    'uid_match_csv_records': json.dumps([x['record'] for x in uw]),
                    'sequence_match_csv_records': json.dumps([x['record'] for x in sw]),
                    'sequence_match_training_uids': json.dumps(sorted({x['uid'] for x in sw})),
                    'uid_match_sequence_sha_conflict': any(x['sequence_sha256'] != seqsha for x in uw)})
            row.update({sp + '_reaction_match': ck in idx['rxn'],
                        sp + '_reaction_match_ignore_stereo': ns in idx['nostereo'],
                        sp + '_reverse_only_reaction_match': ck not in idx['rxn'] and reverse in idx['rxn'],
                        sp + '_original_s7_family_match': family in idx['groups'],
                        sp + '_gold_uid_pairs_matched': uidn, sp + '_gold_sequence_pairs_matched': seqn,
                        sp + '_any_gold_uid_pair_match': uidn > 0,
                        sp + '_any_gold_sequence_pair_match': seqn > 0,
                        sp + '_all_gold_uid_pairs_match': uidn == len(s['gold']),
                        sp + '_all_gold_sequence_pairs_match': seqn == len(s['gold']),
                        sp + '_any_gold_uid_pair_ignore_stereo': uidns > 0,
                        sp + '_any_gold_sequence_pair_ignore_stereo': seqns > 0})
        step_rows.append(row)
    dump(ROOT / 'evidence/PARSE_FAILURES.json', errors)
    assert not errors, 'UNKNOWN parsing rows recorded; cannot silently count as no overlap'
    assert len(step_rows) == 382 and len(pair_rows) == 841 * 3
    table(PUB / 'EXTERNAL_REACTION_NORMALIZATION_382.tsv', norm_rows)
    table(PUB / 'STEP_OVERLAP_382.tsv', step_rows)
    table(PUB / 'GOLD_PAIR_MATCHES_2523.tsv', pair_rows)
    membership = []
    for uid, sids in sorted(uid_steps.items()):
        s82 = {sid for sid in sids if steps[sid]['in_complete82']}
        membership.append({'candidate_uid': uid, 'in_all382': True, 'in_complete82': bool(s82),
            'associations_all382': len(sids), 'associations_complete82': len(s82),
            **{sp + '_positive_uid_match': uid in indices[sp]['uids'] for sp in SPLITS}})
    table(PUB / 'CANDIDATE_UID_MEMBERSHIP_7468.tsv', membership)
    summary, masks = [], {}
    for view in VIEWS:
        ss = [r for r in step_rows if view == VIEWS[0] or r['in_complete82']]
        assert len(ss) == (382 if view == VIEWS[0] else 338)
        ids = {r['step_id'] for r in ss}
        unique_uids = {uid for sid in ids for uid in steps[sid]['candidates']}
        assert len(unique_uids) == (7468 if view == VIEWS[0] else 7056)
        for sp in SPLITS:
            result = {'view': view, 'split': sp, 'n_external_steps': len(ss),
                'n_external_distinct_targets': len({steps[r['step_id']]['reaction'] for r in ss}),
                'n_external_gold_uid_associations': sum(r['n_gold_uid_pairs'] for r in ss),
                'n_unique_candidate_uids': len(unique_uids),
                'n_step_candidate_associations': sum(r['n_candidates'] for r in ss)}
            for field in ['reaction_match', 'reaction_match_ignore_stereo', 'reverse_only_reaction_match',
                          'original_s7_family_match', 'any_gold_uid_pair_match', 'any_gold_sequence_pair_match',
                          'all_gold_uid_pairs_match', 'all_gold_sequence_pairs_match',
                          'any_gold_uid_pair_ignore_stereo', 'any_gold_sequence_pair_ignore_stereo']:
                n = sum(r[sp + '_' + field] for r in ss)
                result[field + '_steps'] = n
                result[field + '_step_percent'] = n / len(ss) * 100
            result['matched_gold_uid_associations'] = sum(r[sp + '_gold_uid_pairs_matched'] for r in ss)
            result['matched_gold_sequence_associations'] = sum(r[sp + '_gold_sequence_pairs_matched'] for r in ss)
            result['positive_uid_membership_count'] = len(unique_uids & indices[sp]['uids'])
            result['positive_uid_membership_percent'] = result['positive_uid_membership_count'] / len(unique_uids) * 100
            result['positive_uid_association_membership_count'] = sum(
                uid in indices[sp]['uids'] for sid in ids for uid in steps[sid]['candidates'])
            result['positive_uid_association_membership_percent'] = result['positive_uid_association_membership_count'] / result['n_step_candidate_associations'] * 100
            summary.append(result)
        definitions = {
            'PRIMARY_DROP_TRAIN_GOLD_UID_PAIR': lambda r: r['train_any_gold_uid_pair_match'],
            'SENSITIVITY_DROP_TRAIN_GOLD_SEQUENCE_PAIR': lambda r: r['train_any_gold_sequence_pair_match'],
            'SENSITIVITY_DROP_TRAIN_REACTION': lambda r: r['train_reaction_match'],
            'SENSITIVITY_DROP_TRAIN_FAMILY': lambda r: r['train_original_s7_family_match'],
            'SENSITIVITY_DROP_ANY_SPLIT_GOLD_UID_PAIR': lambda r: any(r[sp + '_any_gold_uid_pair_match'] for sp in SPLITS),
        }
        masks[view] = {name: {'kept': sorted(r['step_id'] for r in ss if not pred(r)),
                              'dropped': sorted(r['step_id'] for r in ss if pred(r))}
                       for name, pred in definitions.items()}
    table(PUB / 'OVERLAP_SUMMARY_2VIEWS_3SPLITS.tsv', summary)
    dump(PUB / 'S10_SOURCE_RECEIPTS.json', receipts)
    dump(PUB / 'GENERIC_REACTION_DISCLOSURE.json', {
        'rule': 'Valid RDKit dummy/wildcard atoms remain literal graph nodes; no substructure expansion or replacement. A generic reaction is not declared chemically equivalent to an instantiated reaction.',
        'training_distinct_reactions_with_dummy_by_split': {sp: sum('*' in ck for ck in indices[sp]['rxn']) for sp in SPLITS},
        'external_steps_with_dummy': [r['step_id'] for r in norm_rows if '*' in r['rdkit_canonical_stereo_preserved']],
        'implementation_note_sha256': sha(ROOT / 'evidence/CANONICALIZATION_IMPLEMENTATION_NOTE.json')})
    dump(ROOT / 'evidence/NORMALIZATION_CONTROLS.json', {'rdkit_version': rdBase.rdkitVersion, 'checks': controls})
    mask_p = PUB / 'STEP_MASKS_FROZEN.json'
    dump(mask_p, masks)
    source = {str(p): {'sha256': sha(p), 'bytes': p.stat().st_size}
              for p in [C2, LEDGER, EXPORT, METRICS, ROOT / 'evidence/s7_reaction_group_split.py']}
    dump(ROOT / 'evidence/INPUT_IDENTITIES_PRIVATE.json', source)
    sealed_files = [x for x in PUB.glob('*') if x.is_file()]
    dump(PUB / 'MASKS_SEALED_BEFORE_METRICS.json', {
        'protocol_sha256': EXPECTED_PROTOCOL,
        'stage': 'MATCHING_COMPLETE_AND_MASKS_FROZEN; filtered metric file not read in this stage',
        'files': {p.name: sha(p) for p in sorted(sealed_files)},
        'metrics_file_sha256_pre_read': sha(METRICS), 'rdkit_version': rdBase.rdkitVersion})
    print(json.dumps({'matching_complete': True, 'parse_errors': len(errors),
                      'summary': [{k: r[k] for k in ['view', 'split', 'reaction_match_steps',
                        'any_gold_uid_pair_match_steps', 'any_gold_sequence_pair_match_steps',
                        'original_s7_family_match_steps', 'positive_uid_membership_count']} for r in summary]}, ensure_ascii=False))


def metrics():
    seal = json.loads((PUB / 'MASKS_SEALED_BEFORE_METRICS.json').read_text())
    assert sha(ROOT / 'PROTOCOL_FROZEN_BEFORE_COUNTS.json') == seal['protocol_sha256'] == EXPECTED_PROTOCOL
    assert sha(METRICS) == seal['metrics_file_sha256_pre_read']
    assert all(sha(PUB / p) == h for p, h in seal['files'].items())
    masks = json.loads((PUB / 'STEP_MASKS_FROZEN.json').read_text())
    old = readtable(METRICS)
    assert len(old) == 2292 and len({r['arm'] for r in old}) == 6
    outputs = []
    for view in VIEWS:
        original = [r for r in old if view == VIEWS[0] or r['in_complete82'] == 'True']
        arms = sorted({r['arm'] for r in original})
        for name, sets in masks[view].items():
            kept = set(sets['kept'])
            for arm in arms:
                full = [r for r in original if r['arm'] == arm]
                subset = [r for r in full if r['step_id'] in kept]
                assert len(subset) == len(kept) and len(full) == len(kept) + len(sets['dropped'])
                out = {'view': view, 'mask': name, 'arm': arm, 'full_steps': len(full),
                    'excluded_steps': len(sets['dropped']), 'kept_steps': len(subset),
                    'full_paths': len({r['case_id'] for r in full}),
                    'paths_with_kept_steps': len({r['case_id'] for r in subset}),
                    'paths_retaining_all_original_scored_steps': sum(
                        {r['step_id'] for r in full if r['case_id'] == cid} <= kept
                        for cid in {r['case_id'] for r in full}),
                    'candidates_or_ranks_changed': False}
                for field in FIELDS:
                    baseline = math.fsum(float(r[field]) for r in full) / len(full)
                    value = math.fsum(float(r[field]) for r in subset) / len(subset) if subset else None
                    out['full_' + field] = baseline
                    out['kept_' + field] = value
                    out['delta_' + field + ('_percentage_points' if field.startswith('hit') else '')] = (
                        (value - baseline) * (100 if field.startswith('hit') else 1) if value is not None else '')
                outputs.append(out)
    assert len(outputs) == 2 * 5 * 6
    table(PUB / 'SIX_ARM_FILTERED_RECOMPUTATION_60.tsv', outputs)
    dump(PUB / 'METRIC_RECOMPUTATION_RECEIPT.json', {
        'frozen_mask_seal_sha256': sha(PUB / 'MASKS_SEALED_BEFORE_METRICS.json'),
        'original_metric_file_sha256': sha(METRICS),
        'rows': len(outputs), 'model_forwards': 0, 'retraining': 0,
        'same_mask_for_all_six_arms': True, 'reranking': False,
        'only_offline_step_averages': True})
    primary = [r for r in outputs if r['mask'] == 'PRIMARY_DROP_TRAIN_GOLD_UID_PAIR']
    print(json.dumps({'offline_metrics_complete': True, 'primary': primary}, ensure_ascii=False))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('stage', choices=['match', 'metrics'])
    args = p.parse_args()
    (match if args.stage == 'match' else metrics)()
