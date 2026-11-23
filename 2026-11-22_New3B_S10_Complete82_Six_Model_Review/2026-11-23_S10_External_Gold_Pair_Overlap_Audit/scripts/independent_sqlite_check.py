#!/usr/bin/env python3
"""Independent graph normalization + SQLite EXISTS counts + rank-only metrics."""
import csv
import gzip
import hashlib
import json
import math
import sqlite3
from functools import lru_cache
from pathlib import Path

from rdkit import Chem, RDLogger

RDLogger.DisableLog('rdApp.*')
ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT.parent
PUB = ROOT / 'public'


def rows(p):
    with p.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def side_key(side, strip=False):
    # Unlike the producer, parse a whole disconnected side, then use RDKit
    # connected-component extraction rather than splitting text at dots.
    m = Chem.MolFromSmiles(side)
    assert m is not None
    for atom in m.GetAtoms():
        atom.SetAtomMapNum(0)
    m = Chem.RemoveHs(m)
    if strip:
        Chem.RemoveStereochemistry(m)
    fragments = Chem.GetMolFrags(m, asMols=True, sanitizeFrags=True)
    return '.'.join(sorted(Chem.MolToSmiles(f, canonical=True, isomericSmiles=True) for f in fragments))


@lru_cache(maxsize=None)
def canon(rxn, strip=False):
    a, b = rxn.split('>>')
    return side_key(a, strip) + '>>' + side_key(b, strip)


def group(rxn):
    a, b = rxn.split('>>')
    forward, reverse = sorted((rxn, b + '>>' + a))
    return 'ISG_' + hashlib.sha256((forward + '\n' + reverse).encode()).hexdigest()


def main():
    checks = {}
    def check(key, ok, detail):
        checks[key] = {'pass': bool(ok), 'detail': detail}
        assert ok, (key, detail)
    seal = json.loads((PUB / 'MASKS_SEALED_BEFORE_METRICS.json').read_text())
    check('protocol_and_match_seal_unchanged', sha(ROOT / 'PROTOCOL_FROZEN_BEFORE_COUNTS.json') == seal['protocol_sha256']
          and all(sha(PUB / p) == h for p, h in seal['files'].items()), len(seal['files']))
    db = sqlite3.connect(':memory:')
    db.executescript('CREATE TABLE pos(split, rxn, ns, uid, seqsha, family, record);'
                     'CREATE TABLE ext(step PRIMARY KEY, view82 INTEGER, rxn, ns, family);'
                     'CREATE TABLE gold(step, uid, seqsha);CREATE TABLE candidate(step, uid);')
    positives, receipts = [], []
    with gzip.open(ROOT / 'private_inputs/S10_POSITIVE_ROWS_SOURCE_BOUND.jsonl.gz', 'rt') as f:
        for line in f:
            r = json.loads(line)
            if r['kind'] == 'source_receipt':
                receipts.append(r)
                continue
            assert group(r['reaction']) == r['internal_split_group']
            positives.append((r['split'], canon(r['reaction']), canon(r['reaction'], True),
                              r['uid'], r['sequence_sha256'], r['internal_split_group'],
                              r['csv_record_number_including_header']))
    db.executemany('INSERT INTO pos VALUES (?,?,?,?,?,?,?)', positives)
    db.executescript('CREATE INDEX p_rxn ON pos(split,rxn);CREATE INDEX p_ns ON pos(split,ns);'
                     'CREATE INDEX p_uid ON pos(split,uid);CREATE INDEX p_family ON pos(split,family);'
                     'CREATE INDEX p_uidpair ON pos(split,rxn,uid);CREATE INDEX p_seqpair ON pos(split,rxn,seqsha);')
    ext, gold, candidate = {}, [], []
    with gzip.open(RUN / 'ENZYME_HOST_C2_C3_EXPORT_20261118/STEP_CANDIDATE_RANKINGS.tsv.gz', 'rt') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['arm'] != 'legacy_esm2_3b':
                continue
            sid = r['step_id']
            ext[sid] = (sid, int(r['in_complete82'] == 'True'), canon(r['model_reaction']),
                        canon(r['model_reaction'], True), group(r['model_reaction']))
            candidate.append((sid, r['scientific_uid']))
            if r['gold_flag'] == 'TRUE':
                gold.append((sid, r['scientific_uid'], r['sequence_sha256']))
    db.executemany('INSERT INTO ext VALUES (?,?,?,?,?)', ext.values())
    db.executemany('INSERT INTO gold VALUES (?,?,?)', gold)
    db.executemany('INSERT INTO candidate VALUES (?,?)', candidate)
    check('source_and_external_denominators', len(positives) == 112245 and len(ext) == 382
          and len(gold) == 841 and len(candidate) == 16448,
          {'positive_rows': len(positives), 'steps': len(ext), 'gold': len(gold), 'associations': len(candidate)})
    norm = rows(PUB / 'EXTERNAL_REACTION_NORMALIZATION_382.tsv')
    check('independent_graph_normalization_matches_every_target', all(
        ext[r['step_id']][2:4] == (r['rdkit_canonical_stereo_preserved'], r['rdkit_canonical_stereo_removed'])
        for r in norm), len(norm))
    summaries = rows(PUB / 'OVERLAP_SUMMARY_2VIEWS_3SPLITS.tsv')
    for r in summaries:
        sp, v = r['split'], r['view']
        where = 'e.view82=1' if v == 'COMPLETE82_STEP338' else '1'
        scalar = lambda sql: db.execute(sql, (sp,)).fetchone()[0]
        results = {
            'reaction_match_steps': scalar(f'SELECT count(*) FROM ext e WHERE {where} AND EXISTS(SELECT 1 FROM pos p WHERE p.split=? AND p.rxn=e.rxn)'),
            'reaction_match_ignore_stereo_steps': scalar(f'SELECT count(*) FROM ext e WHERE {where} AND EXISTS(SELECT 1 FROM pos p WHERE p.split=? AND p.ns=e.ns)'),
            'original_s7_family_match_steps': scalar(f'SELECT count(*) FROM ext e WHERE {where} AND EXISTS(SELECT 1 FROM pos p WHERE p.split=? AND p.family=e.family)'),
            'any_gold_uid_pair_match_steps': scalar(f'SELECT count(DISTINCT e.step) FROM ext e JOIN gold g USING(step) WHERE {where} AND EXISTS(SELECT 1 FROM pos p WHERE p.split=? AND p.rxn=e.rxn AND p.uid=g.uid)'),
            'any_gold_sequence_pair_match_steps': scalar(f'SELECT count(DISTINCT e.step) FROM ext e JOIN gold g USING(step) WHERE {where} AND EXISTS(SELECT 1 FROM pos p WHERE p.split=? AND p.rxn=e.rxn AND p.seqsha=g.seqsha)'),
            'matched_gold_uid_associations': scalar(f'SELECT count(*) FROM ext e JOIN gold g USING(step) WHERE {where} AND EXISTS(SELECT 1 FROM pos p WHERE p.split=? AND p.rxn=e.rxn AND p.uid=g.uid)'),
            'matched_gold_sequence_associations': scalar(f'SELECT count(*) FROM ext e JOIN gold g USING(step) WHERE {where} AND EXISTS(SELECT 1 FROM pos p WHERE p.split=? AND p.rxn=e.rxn AND p.seqsha=g.seqsha)'),
            'positive_uid_membership_count': scalar(f'SELECT count(DISTINCT c.uid) FROM candidate c JOIN ext e USING(step) WHERE {where} AND EXISTS(SELECT 1 FROM pos p WHERE p.split=? AND p.uid=c.uid)'),
        }
        check(v + ':' + sp + ':independent_sql_counts', all(int(r[k]) == value for k, value in results.items()), results)
    # Exact correspondence of every published positive match, not a sample.
    pairrows = rows(PUB / 'GOLD_PAIR_MATCHES_2523.tsv')
    bad = []
    for r in pairrows:
        ck = ext[r['step_id']][2]
        uid_seen = db.execute('SELECT EXISTS(SELECT 1 FROM pos WHERE split=? AND rxn=? AND uid=?)',
                             (r['split'], ck, r['gold_uid'])).fetchone()[0]
        seq_seen = db.execute('SELECT EXISTS(SELECT 1 FROM pos WHERE split=? AND rxn=? AND seqsha=?)',
                             (r['split'], ck, r['gold_sequence_sha256'])).fetchone()[0]
        if bool(uid_seen) != (r['exact_uid_pair_positive_match'] == 'True') or bool(seq_seen) != (r['exact_sequence_pair_positive_match'] == 'True'):
            bad.append([r['step_id'], r['split'], r['gold_uid']])
    check('all_2523_Gold_pair_flags_independently_joined', not bad, {'rows': len(pairrows), 'bad': bad})
    metric_source = RUN / 'NEW3B_S10_SISTER_DELIVERY_20261122/NEW3B_S10_COMPLETE82_SIX_MODEL_REVIEW/SIX_MODEL_STEP_RESULTS_2292.tsv'
    old = rows(metric_source)
    check('existing_metrics_identity_unchanged', sha(metric_source) == seal['metrics_file_sha256_pre_read'], len(old))
    masks = json.loads((PUB / 'STEP_MASKS_FROZEN.json').read_text())
    output = rows(PUB / 'SIX_ARM_FILTERED_RECOMPUTATION_60.tsv')
    bad = []
    for r in output:
        sets = masks[r['view']][r['mask']]
        base = [x for x in old if x['arm'] == r['arm'] and (r['view'] == 'ALL_SCORED382' or x['in_complete82'] == 'True')]
        kept = [x for x in base if x['step_id'] in sets['kept']]
        assert len(kept) == int(r['kept_steps'])
        for field, k in [('hit_at_1', 1), ('hit_at_3', 3), ('hit_at_5', 5), ('hit_at_10', 10)]:
            value = sum(int(x['best_reference_rank']) <= k for x in kept) / len(kept)
            if abs(value - float(r['kept_' + field])) > 1e-12:
                bad.append([r['arm'], r['view'], r['mask'], field])
        for field in ['mrr', 'mrr_at_10']:
            value = math.fsum(1 / int(x['best_reference_rank']) if field == 'mrr' or int(x['best_reference_rank']) <= 10 else 0 for x in kept) / len(kept)
            if abs(value - float(r['kept_' + field])) > 1e-12:
                bad.append([r['arm'], r['view'], r['mask'], field])
    check('all_60_filtered_rows_recomputed_from_integer_reference_ranks', not bad, {'rows': len(output), 'bad': bad})
    for sp, rec in ((r['split'], r) for r in receipts):
        check(sp + ':source_receipt_and_positive_rowcount', rec['sha256_start'] == rec['sha256_end']
              and db.execute('SELECT count(*) FROM pos WHERE split=?', (sp,)).fetchone()[0] == rec['positive_rows'],
              {'sha256': rec['sha256_end'], 'positive_rows': rec['positive_rows']})
    result = {'all_independent_checks_pass': all(c['pass'] for c in checks.values()), 'checks': checks,
              'implementation': 'whole-side RDKit graph parsing + GetMolFrags; SQLite EXISTS joins; integer-rank metrics',
              'models_or_GPU_calls': 0}
    (PUB / 'INDEPENDENT_CHECKS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'all_independent_checks_pass': result['all_independent_checks_pass'], 'checks': len(checks)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
