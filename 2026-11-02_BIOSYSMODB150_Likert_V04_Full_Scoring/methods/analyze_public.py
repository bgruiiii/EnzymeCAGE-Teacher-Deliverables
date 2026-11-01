#!/usr/bin/env python3
"""Reproduce all statistics/figures from this package's public input tables."""
import argparse
import csv
import itertools
import json
import math
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.stats import mannwhitneyu
import statsmodels
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint

DIMS = ['D1', 'D2', 'D3a', 'D3b', 'D4', 'D5', 'D6']
LAYERS = ['layer_pathway', 'layer_smiles', 'layer_enzyme', 'layer_microbial_identity', 'layer_traits']
TOTAL = 'science_weighted_total_100'
SEED, REPS = 20261029, 2000
LABELS = {'qwen3.8-max': 'Qwen', 'deepseek-v4.1-flash': 'DeepSeek', 'kimi/kimi-k3': 'Kimi',
          'ZHIPU_GLM53_MAX_128K_JSON_OBJECT_CORRECTED': 'GLM-128K'}


def read(p):
    with Path(p).open(encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write(p, rows, fields=None):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0])
    with p.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def number(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (ValueError, TypeError):
        return None


def bootstrap(values):
    values = np.asarray(values, dtype=float)
    if not len(values):
        return None, None
    rng = np.random.default_rng(SEED)
    means = values[rng.integers(0, len(values), (REPS, len(values)))].mean(axis=1)
    return [float(x) for x in np.quantile(means, [.025, .975])]


def describe(values):
    a = np.asarray(values, dtype=float)
    if not len(a):
        return dict(n=0, mean='', median='', q1='', q3='', mean_ci_low='', mean_ci_high='')
    lo, hi = bootstrap(a)
    return dict(n=len(a), mean=float(a.mean()), median=float(np.median(a)),
                q1=float(np.quantile(a, .25)), q3=float(np.quantile(a, .75)), mean_ci_low=lo, mean_ci_high=hi)


def analyze(root):
    root = Path(root)
    data, out = root / 'data', root / 'statistics'
    b = read(data / 'batchB_recovery_inclusive_PROGRAM_480.tsv')
    a = read(data / 'batchA_native_single_shot_FINAL_AXES.tsv')
    rates = read(data / 'batchB_LIKERT_480.tsv')
    dims = read(data / 'batchB_LIKERT_DIMENSIONS_3360.tsv')
    assert len(a) == 484 and len(b) == len(rates) == 480 and len(dims) == 3360
    models = sorted({x['tested_model_config_id'] for x in b})
    bmap = {x['b_slot_uid']: x for x in b}
    allcases = sorted({x['case_id'] for x in b})
    native = [c for c in allcases if all(x['recovered'] == 'FALSE' for x in b if x['case_id'] == c)]
    assert len(allcases) == 120 and len(native) == 100
    program, lk = [], []
    for view, cases in [('COMMON120_RECOVERY_INCLUSIVE', allcases), ('COMMON100_ALL4_NATIVE', native)]:
        for m in models:
            bb = [x for x in b if x['tested_model_config_id'] == m and x['case_id'] in cases]
            for key in LAYERS + [TOTAL]:
                program.append(dict(batch='batchB_recovery_inclusive', view=view, model=m, endpoint=key,
                                    **describe([float(x[key]) for x in bb])))
            for d in DIMS:
                rr = [x for x in dims if x['tested_model_config_id'] == m and x['dimension'] == d and x['case_id'] in cases]
                nums = [number(x['score']) for x in rr if x['score_status'] in ('SCORED', 'MISSING')]
                nums = [v for v in nums if v is not None]
                nk = sum(x['key_error'] == 'Y' for x in rr)
                ci = proportion_confint(nk, len(rr), alpha=.05, method='wilson')
                lk.append(dict(batch='batchB_recovery_inclusive', view=view, model=m, dimension=d,
                               **describe(nums), denominator=len(rr),
                               scored=sum(x['score_status'] == 'SCORED' for x in rr),
                               missing=sum(x['score_status'] == 'MISSING' for x in rr),
                               ne=sum(x['score_status'] == 'NE' for x in rr), na=sum(x['score_status'] == 'NA' for x in rr),
                               failed=sum(not x['score_status'] for x in rr), key_error_y=nk,
                               key_error_unresolved=sum(x['key_error'] == 'UNRESOLVED' for x in rr),
                               key_error_rate=nk / len(rr), key_error_wilson_low=float(ci[0]), key_error_wilson_high=float(ci[1]),
                               human_validity='PENDING'))
    write(out / 'B_PROGRAM_SUMMARY.tsv', program)
    write(out / 'B_LIKERT_DIMENSION_SUMMARY.tsv', lk)
    axes=[]
    for m in models:
        bb=[x for x in b if x['tested_model_config_id']==m]
        keys=['evidence_verified_n','evidence_unverified_n','evidence_hallucination_n','evidence_ref_missing_n',
              'evidence_internal_knowledge_n','evidence_model_inference_n','abstention_nulls_n','abstention_overclaims_n','gold_steps_recall_missed']
        row=dict(batch='batchB_recovery_inclusive',model=m,n=120)
        for key in keys:
            row[key+'_sum']=sum(float(x[key]) for x in bb)
            row[key+'_mean']=row[key+'_sum']/120
        row['evidence_chain_complete_rate']='NOT_ESTIMABLE_FROM_FROZEN_G3_F1_EXPORT'
        row['scope_note']='LOOKUP program proxy; not official fact verification. Trait completeness is not evidence-chain completeness.'
        axes.append(row)
    write(out/'B_EVIDENCE_ABSTENTION_SAME_PAGE.tsv',axes)
    eng = []
    for m in models:
        rows = [x for x in a if x['model_config_id'] == m]
        n = len(rows)
        assert n == 121
        good = sum(x['engineering_class'] == 'USABLE' for x in rows)
        ci = proportion_confint(good, n, alpha=.05, method='wilson')
        e = dict(batch='batchA_native_single_shot', model=m, denominator=n, usable=good,
                 usable_rate=good/n, usable_wilson_low=float(ci[0]), usable_wilson_high=float(ci[1]),
                 truncated=sum(x['truncated_finish_length'].lower() == 'true' for x in rows),
                 json_valid=sum(x['json_valid'].lower() == 'true' for x in rows))
        for key in ['usage_cost_cny_formal_basis', 'duration_seconds', 'prompt_tokens', 'completion_tokens', 'reasoning_tokens']:
            vals = [number(x[key]) for x in rows]
            vals = [v for v in vals if v is not None]
            e[key + '_observed_n'] = len(vals)
            e[key + '_sum'] = sum(vals)
            e[key + '_mean_observed'] = float(np.mean(vals)) if vals else ''
        for key in LAYERS + [TOTAL]:
            e[key + '_oldgold_primary_mean_121'] = float(np.mean([float(x['oldgold_' + key]) for x in rows]))
            e[key + '_newgold_sensitivity_mean_121'] = float(np.mean([float(x['newgold_' + key]) for x in rows]))
        for key in ['evidence_verified_n','evidence_unverified_n','evidence_hallucination_n','abstention_nulls_n','abstention_overclaims_n']:
            vals=[number(x['oldgold_'+key]) for x in rows]
            e[key+'_observed_n']=sum(v is not None for v in vals)
            e[key+'_sum_observed']=sum(v for v in vals if v is not None)
        eng.append(e)
    write(out / 'A_ENGINEERING_SCIENCE_SUMMARY.tsv', eng)
    rec = []
    for m in models:
        for key in LAYERS + [TOTAL]:
            r = [float(x[key]) for x in b if x['tested_model_config_id'] == m and x['recovered'] == 'TRUE']
            n = [float(x[key]) for x in b if x['tested_model_config_id'] == m and x['recovered'] == 'FALSE']
            eligible = min(len(r), len(n)) >= 2
            p = float(mannwhitneyu(r, n, alternative='two-sided', method='auto').pvalue) if eligible else None
            rec.append(dict(model=m, endpoint=key, recovered_n=len(r), non_recovered_n=len(n),
                            recovered_mean=float(np.mean(r)), non_recovered_mean=float(np.mean(n)),
                            recovered_median=float(np.median(r)), non_recovered_median=float(np.median(n)),
                            p_raw=p if p is not None else '', p_holm='',
                            status='ESTIMABLE' if eligible else 'NOT_ESTIMABLE_N_LT_2',
                            family_planned=24, causal_interpretation='NOT_ALLOWED'))
    eligible = [x for x in rec if x['p_raw'] != '']
    _, adjusted, _, _ = multipletests([x['p_raw'] for x in eligible], method='holm')
    for x, p in zip(eligible, adjusted):
        x['p_holm'] = float(p)
    write(out / 'RECOVERY_MWU_HOLM_24_PLANNED.tsv', rec)
    pairs = []
    for m1, m2 in itertools.combinations(models, 2):
        for kind, table, mkey, endpoint in [('PROGRAM_B_PRIMARY', b, 'tested_model_config_id', TOTAL),
                                           ('AI_LIKERT_EXPLORATORY', rates, 'tested_model_config_id', 'weighted_total_program')]:
            l = {x['case_id']: number(x[endpoint]) for x in table if x[mkey] == m1}
            r = {x['case_id']: number(x[endpoint]) for x in table if x[mkey] == m2}
            cases = sorted(c for c in set(l) & set(r) if l[c] is not None and r[c] is not None)
            diff = [l[c] - r[c] for c in cases]
            values = describe(diff)
            word = ('INDISTINGUISHABLE_ONE_QUESTION_SCALE' if kind == 'PROGRAM_B_PRIMARY'
                    and abs(values['mean']) < 100 / len(cases) else 'DESCRIPTIVE_DIFFERENCE_NOT_A_SIGNIFICANCE_CLAIM')
            pairs.append(dict(analysis=kind, model_left=m1, model_right=m2, **values,
                              wording=word, statistical_unit='CASE_PAIRED', p_value='NOT_COMPUTED_NO_TEST_ADDED'))
    write(out / 'PAIRED_CASE_BOOTSTRAP_2000.tsv', pairs)
    comparison = []
    for x in rates:
        p = bmap[x['b_slot_uid']]
        comparison.append(dict(b_slot_uid=x['b_slot_uid'], case_id=x['case_id'], model=x['tested_model_config_id'],
                               program_total=p[TOTAL], likert_total=x['weighted_total_program'],
                               program_gold_limited='TRUE', likert_human_validity='PENDING',
                               scientific_shortfall=x['scientific_shortfall_flag'],
                               **{k:p[k] for k in LAYERS},
                               **{d:x[d + '_score'] for d in DIMS},
                               review_reason='Gold-scope program and AI rubric measure different constructs; review individual rationale, not replace scores.'))
    write(out / 'PROGRAM_AI_ALL480_COMPARISON.tsv', comparison)
    figures(root, models, program, lk, eng, comparison)
    status = {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
              'statsmodels': statsmodels.__version__, 'bootstrap_replicates': REPS, 'bootstrap_seed': SEED,
              'bootstrap_unit': 'case; paired differences resampled together', 'human_scores_used': 0,
              'recovery_tests_planned': 24, 'recovery_tests_estimable': len(eligible),
              'recovery_holm_any_below_05': any(x['p_holm'] < .05 for x in eligible),
              'likert_valid': sum(x['system_run_status'] == 'OK' for x in rates),
              'likert_total_comparable': sum(number(x['weighted_total_program']) is not None for x in rates),
              'common_all4_native_cases': len(native),
              'all_dimensions_human_validity': '人类效度验证进行中',
              'claim_limits': 'No new significance test chosen; paired CIs are descriptive, no causal recovery claim.'}
    (out / 'ANALYSIS_STATUS.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return status


def figures(root, models, program, lk, eng, comparison):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    d = root / 'figures'
    d.mkdir(exist_ok=True)
    labels = [LABELS.get(m, m) for m in models]
    fig, ax = plt.subplots(figsize=(9, 4.4), constrained_layout=True)
    values = np.array([[next(x['mean'] for x in program if x['model']==m and x['endpoint']==e and x['view'].startswith('COMMON120')) for e in LAYERS] for m in models])
    im = ax.imshow(values, vmin=0, vmax=100, cmap='YlGnBu', aspect='auto')
    ax.set_xticks(range(5), ['Pathway', 'SMILES', 'Enzyme', 'Organism', 'Traits'])
    ax.set_yticks(range(4), labels)
    for i in range(4):
        for j in range(5):
            ax.text(j,i,f'{values[i,j]:.1f}',ha='center',va='center',color='black' if values[i,j]<55 else 'white')
    ax.set_title('Batch B: gold-limited program layers (120 paired cases)')
    fig.colorbar(im,ax=ax,label='Program layer score (0-100)')
    fig.savefig(d/'B_PROGRAM_FIVE_LAYERS.png',dpi=160);plt.close(fig)
    fig, ax = plt.subplots(figsize=(10,4.7),constrained_layout=True)
    for i,m in enumerate(models):
        vals=[next(x['median'] for x in lk if x['model']==m and x['dimension']==dim and x['view'].startswith('COMMON120')) for dim in DIMS]
        ax.plot(DIMS,vals,marker='o',label=LABELS.get(m,m))
    ax.set_ylim(.5,10.5);ax.set_ylabel('Median AI-assisted Likert (1-10)')
    ax.set_title('Batch B: seven dimensions; human validity pending')
    ax.legend(ncol=4,loc='lower center');ax.grid(axis='y',alpha=.2)
    fig.savefig(d/'B_AI_LIKERT_SEVEN_DIMENSIONS.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8.5,4.6),constrained_layout=True)
    for m in models:
        rows=[x for x in comparison if x['model']==m and number(x['likert_total']) is not None]
        ax.scatter([float(x['program_total']) for x in rows],[float(x['likert_total']) for x in rows],s=13,alpha=.45,label=LABELS.get(m,m))
    ax.set_xlabel('Gold-limited program total (0-100)');ax.set_ylabel('AI rubric total (10-100)')
    ax.set_title('Different constructs: paired by case; not interchangeable')
    ax.legend();ax.grid(alpha=.15)
    fig.savefig(d/'PROGRAM_VS_AI_SCATTER.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8.5,4.6),constrained_layout=True)
    ordered=[next(x for x in eng if x['model']==m) for m in models]
    means=np.array([x['usable_rate'] for x in ordered])
    lo=np.array([x['usable_wilson_low'] for x in ordered]);hi=np.array([x['usable_wilson_high'] for x in ordered])
    ax.bar(labels,means,color=['#258477','#ad594b','#6b63a8','#5484a6'])
    ax.errorbar(range(4),means,yerr=[means-lo,hi-means],fmt='none',color='black',capsize=5)
    ax.set_ylim(0,1.08);ax.set_ylabel('Usable fraction, Wilson 95% CI')
    ax.set_title('Batch A: native single shot, fixed 121 per model')
    fig.savefig(d/'A_NATIVE_RELIABILITY.png',dpi=160);plt.close(fig)


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('package',type=Path)
    print(json.dumps(analyze(p.parse_args().package),ensure_ascii=False,indent=2))
