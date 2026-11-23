#!/usr/bin/env python3
"""Reuse original path-cluster estimator on already-frozen filtered masks."""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / 'public'
SOURCE = ROOT.parent / 'NEW3B_S10_SISTER_DELIVERY_20261122/NEW3B_S10_COMPLETE82_SIX_MODEL_REVIEW/SIX_MODEL_STEP_RESULTS_2292.tsv'
with SOURCE.open() as f:
    old = list(csv.DictReader(f, delimiter='\t'))
masks = json.loads((PUB / 'STEP_MASKS_FROZEN.json').read_text())
fields = ['hit_at_1', 'hit_at_3', 'hit_at_5', 'hit_at_10', 'mrr', 'mrr_at_10']
new_arm = 'new_esm2_3b_s10'
arms = sorted({r['arm'] for r in old} - {new_arm})
rng = np.random.default_rng(20261120)
output = []
checks = []
for view, sets in masks.items():
    # Primary and exact-sequence alias sensitivity are both pre-frozen masks.
    for mask in ['PRIMARY_DROP_TRAIN_GOLD_UID_PAIR', 'SENSITIVITY_DROP_TRAIN_GOLD_SEQUENCE_PAIR']:
        keep = set(sets[mask]['kept'])
        selected = [r for r in old if r['step_id'] in keep]
        paths = sorted({r['case_id'] for r in selected})
        for arm in arms:
            aa = {r['step_id']: r for r in selected if r['arm'] == new_arm}
            bb = {r['step_id']: r for r in selected if r['arm'] == arm}
            assert set(aa) == set(bb) == keep
            counts = np.array([sum(x['case_id'] == p for x in aa.values()) for p in paths], dtype=np.int64)
            numerators = np.array([[sum(float(aa[s][m]) - float(bb[s][m])
                                       for s in keep if aa[s]['case_id'] == p) for m in fields] for p in paths])
            draw = rng.integers(0, len(paths), size=(10000, len(paths)))
            weights = np.zeros((10000, len(paths)), dtype=np.int64)
            for i, d in enumerate(draw):
                weights[i] = np.bincount(d, minlength=len(paths))
            denominators = weights @ counts
            boot = (weights @ numerators) / denominators[:, None]
            # Independent direct expansion of 10 draws validates weighted reduction.
            err = 0.0
            bypath = {p: [s for s in keep if aa[s]['case_id'] == p] for p in paths}
            for i in range(10):
                expanded = [s for j in draw[i] for s in bypath[paths[j]]]
                direct = np.array([sum(float(aa[s][m]) - float(bb[s][m]) for s in expanded) / len(expanded) for m in fields])
                err = max(err, float(np.max(np.abs(direct - boot[i]))))
            assert err < 1e-12
            checks.append({'view': view, 'mask': mask, 'pair': arm, 'direct_draws_checked': 10, 'max_error': err})
            lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
            point = numerators.sum(axis=0) / counts.sum()
            for k, metric in enumerate(fields):
                output.append({'view': view, 'mask': mask, 'pair': new_arm + '-vs-' + arm, 'metric': metric,
                    'paired_diff': float(point[k]), 'ci95_low': float(lo[k]), 'ci95_high': float(hi[k]),
                    'n_steps': len(keep), 'n_cluster_paths': len(paths), 'resamples': 10000,
                    'seed': 20261120, 'multiplicity_adjusted': False,
                    'note': 'resample paths containing retained steps; all retained steps within drawn path, same draw for both arms; step-macro point estimates; not whole-path success or equivalence proof'})
assert len(output) == 120
with (PUB / 'FILTERED_PATH_CLUSTER_PAIRED_CI_120.tsv').open('w') as f:
    w = csv.DictWriter(f, fieldnames=list(output[0]), delimiter='\t', lineterminator='\n')
    w.writeheader()
    w.writerows(output)
(PUB / 'BOOTSTRAP_REDUCTION_CHECKS.json').write_text(json.dumps({
    'all_pass': True, 'checks': checks, 'mask_file_sha256': hashlib.sha256((PUB / 'STEP_MASKS_FROZEN.json').read_bytes()).hexdigest(),
    'source_metrics_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'no_model_calls': True}, indent=2) + '\n')
print(json.dumps({'CI_rows': len(output), 'direct_draw_reduction_checks': len(checks), 'all_pass': True}))
