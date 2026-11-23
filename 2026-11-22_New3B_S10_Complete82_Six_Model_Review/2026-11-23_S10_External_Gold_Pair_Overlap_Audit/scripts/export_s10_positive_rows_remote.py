#!/usr/bin/env python3
"""Read-only remote export to stdout; no model/GPU imports or remote writes."""
import csv
import gzip
import hashlib
import io
import json
import sys
from pathlib import Path

BASE = Path('/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922/07_splits_reaction_group_20260924')
EXPECTED = {
    'train': ('2c32345c1fe0014cb345d3fdb20eb4c5a17def02b5c641099bc2c74ad19eb575', 604539),
    'valid': ('c0ac099d96253eed57b6222310aac5ba0198478a94d23925a1e1cda25e5bf64a', 75733),
    'test': ('7b3ea8e21a4701aaf3a9fa0378881248bab2fe8c1cd95665016ea9d6146cc805', 75556),
}


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''):
            h.update(b)
    return h.hexdigest()


with gzip.GzipFile(fileobj=sys.stdout.buffer, mode='wb', mtime=0) as compressed:
    with io.TextIOWrapper(compressed, encoding='utf-8') as out:
        def emit(v):
            out.write(json.dumps(v, ensure_ascii=False, separators=(',', ':')) + '\n')
        for split, (expected_sha, expected_n) in EXPECTED.items():
            p = BASE / (split + '.csv')
            start = sha(p)
            assert start == expected_sha, (split, 'SOURCE_SHA_MISMATCH')
            n = positives = 0
            reactions, groups, all_uids, positive_uids = set(), set(), set(), set()
            with p.open(newline='') as f:
                for record_number, r in enumerate(csv.DictReader(f), start=2):
                    n += 1
                    assert r['Label'] in ('0', '1')
                    reaction = r['CANO_RXN_SMILES']
                    left, sep, right = reaction.partition('>>')
                    assert sep and left and right
                    a, b = sorted([reaction, right + '>>' + left])
                    group = 'ISG_' + hashlib.sha256((a + '\n' + b).encode()).hexdigest()
                    assert group == r['INTERNAL_SPLIT_GROUP']
                    reactions.add(reaction)
                    groups.add(group)
                    all_uids.add(r['UniprotID'])
                    if r['Label'] != '1':
                        continue
                    positives += 1
                    positive_uids.add(r['UniprotID'])
                    assert hashlib.sha256(r['sequence'].encode()).hexdigest() == r['sequence_sha256']
                    assert r['UniprotID'] == r['training_carrier_uid']
                    emit({'kind': 'positive', 'split': split,
                          'csv_record_number_including_header': record_number,
                          'uid': r['UniprotID'], 'sequence_sha256': r['sequence_sha256'],
                          'reaction': reaction, 'internal_split_group': group})
            end = sha(p)
            assert end == start and n == expected_n
            emit({'kind': 'source_receipt', 'split': split, 'path': str(p),
                  'sha256_start': start, 'sha256_end': end, 'bytes': p.stat().st_size,
                  'total_rows': n, 'positive_rows': positives,
                  'directed_reactions': len(reactions), 'split_groups': len(groups),
                  'all_label_unique_uids': len(all_uids),
                  'positive_unique_uids': len(positive_uids),
                  'all_stored_group_ids_match_original_s7_function': True,
                  'all_positive_sequence_shas_recomputed': True,
                  'remote_writes': 0})
