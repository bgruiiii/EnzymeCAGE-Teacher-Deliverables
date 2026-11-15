"""Independent standard-library verification of the public numerical release."""
import csv
import hashlib
import json
import re
from collections import Counter,defaultdict
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
WEIGHTS=dict(D1=15,D2=25,D3a=10,D3b=10,D4=15,D5=15,D6=10)


def read(name):
    with(ROOT/'data'/name).open(newline='')as f:return list(csv.DictReader(f,delimiter='\t'))


def close(a,b):return abs(Decimal(str(a))-Decimal(str(b)))<Decimal('0.00000001')


def main():
    for line in(ROOT/'SHA256SUMS').read_text().splitlines():
        expected,relative=line.split('  ',1);p=(ROOT/relative).resolve()
        assert p.is_relative_to(ROOT)
        assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,relative
    scores=read('LIKERT_V05_SCORES_726.tsv')
    assert len(scores)==len({(x['model'],x['case_id'])for x in scores})==726
    assert set(Counter(x['model']for x in scores).values())=={121}
    assert sum(x['likert_status']=='COMPARABLE'for x in scores)==723
    for row in scores:
        if row['likert_status']=='COMPARABLE':
            assert close(sum(Decimal(row[d+'_score'])*w/10 for d,w in WEIGHTS.items()),row['likert_total'])
        else:
            assert row['likert_total']==''
        p=sum(Decimal(row['program_'+k])*w for k,w in zip(
            ['pathway','smiles','enzyme','microbial_identity','traits'],map(Decimal,['.45','.10','.20','.15','.10'])))
        assert abs(p-Decimal(row['program_weighted_total_100']))<=Decimal('.011')
        if row['program_binding_status']=='SAME_ANSWER_SHA':assert row['program_answer_sha256']==row['answer_sha256']
    common=read('COMMON118_SCORES_708.tsv')
    assert len(common)==708 and len({x['case_id']for x in common})==118
    assert set(Counter(x['case_id']for x in common).values())=={6}
    for row in read('SIX_MODEL_COMMON118_SUMMARY.tsv'):
        group=[x for x in common if x['model']==row['model']]
        assert len(group)==118
        assert close(sum(Decimal(x['likert_total'])for x in group)/118,row['mean_likert_total'])
        assert close(sum(Decimal(x['program_weighted_total_100'])for x in group)/118,row['mean_program_total_100'])
        assert all(row[k]for k in ['gateway','exact_id','search_status','temperature','reasoning','output_budget'])
    ratings=[json.loads(x)for x in(ROOT/'data/LIKERT_V05_RATINGS_723.jsonl').read_text().splitlines()]
    assert len(ratings)==723
    status=Counter(v['score_status']for x in ratings for v in x['dimensions'].values())
    assert status=={'SCORED':4823,'MISSING':238}
    rowmap={x['slot']:x for x in scores}
    for r in ratings:
        assert r['scoring_model']=='deepseek-v4.1-flash-1017'
        row=rowmap[r['slot']];assert r['answer_sha256']==row['answer_sha256']
        for d,v in r['dimensions'].items():
            assert v['score_status']==row[d+'_status']and v['score']==int(row[d+'_score'])
    dims=read('V04_V05_DIMENSION_CHANGE_3360.tsv')
    assert len(dims)==len({(x['slot'],x['dimension'])for x in dims})==3360
    assert sum(x['approved_reference_scope_changed']=='True'for x in dims)==56
    sums=defaultdict(Decimal)
    for d in dims:
        difference=Decimal(d['v05_score'])-Decimal(d['v04_score'])
        assert close(difference,d['delta_score'])
        weighted=difference*WEIGHTS[d['dimension']]/10
        assert close(weighted,d['weighted_total_delta_contribution'])
        sums[d['slot']]+=weighted
        assert int(d['v05_score'])==int(rowmap[d['slot']][d['dimension']+'_score'])
    cases=read('V04_V05_CASE_CHANGE_480.tsv');assert len(cases)==480
    for row in cases:
        assert close(Decimal(row['v05_total'])-Decimal(row['v04_total']),row['delta_total'])
        assert close(sums[row['slot']],row['delta_total'])
    for row in read('FOUR_MODEL_FULL120_AND_CORE118.tsv'):
        group=[x for x in cases if x['model']==row['model']];assert len(group)==120
        assert close(sum(Decimal(x['v04_total'])for x in group)/120,row['old_original120_mean'])
        assert close(sum(Decimal(x['v05_total'])for x in group)/120,row['new_repaired120_mean'])
    for row in read('FOUR_MODEL_DIMENSION_CHANGE_28.tsv'):
        g=[x for x in dims if x['model']==row['model']and x['dimension']==row['dimension']];assert len(g)==120
        assert close(sum(Decimal(x['delta_score'])for x in g)/120,row['mean_delta'])
    assert len(read('UNSCORED_POSITIONS_3.tsv'))==3
    costs=read('SCORING_COST_BY_PHASE.tsv')
    assert sum(int(x['attempts'])for x in costs)==1142
    assert sum(int(x['usage_settled'])for x in costs)==1119
    assert sum(int(x['current_unknown_reservations'])for x in costs)==23
    assert close(sum(Decimal(x['known_price_estimate_cny'])for x in costs),'567.042456')
    pages=list((ROOT/'case_reviews').glob('BIOPATH150_*.md'))
    assert len(pages)==121 and all(p.stat().st_size<500000 for p in pages)
    linked=0
    for p in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('https:','http:','#')):continue
            dest=(p.parent/unquote(target.split('#')[0])).resolve()
            assert dest.exists(),(str(p.relative_to(ROOT)),target);linked+=1
    # Published text must not contain real local paths or internal blind IDs.
    for p in ROOT.rglob('*'):
        if p.suffix.lower()in ['.md','.tsv','.json','.jsonl','.txt','.py']:
            content=p.read_text()
            assert not re.search(r'/home/[A-Za-z0-9_./-]+',content),str(p)
            assert not re.search(r'\bF4I-[A-Za-z0-9-]+\b',content),str(p)
    print(json.dumps(dict(PASS=True,positions=726,scored=723,common_cases=118,
        native_dimension_pairs=3360,NE=0,links_verified=linked,
        arithmetic='independent Decimal recomputation',network_calls=0)))


if __name__=='__main__':main()
