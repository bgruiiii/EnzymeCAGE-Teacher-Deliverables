#!/usr/bin/env python3
import argparse, csv, json, subprocess, sys, tempfile
from pathlib import Path
try:
    from rdkit import Chem
except Exception:
    sys.stderr.write('M3_P1_2_1_SCORING_BLOCKED_RDKIT_UNAVAILABLE\n')
    raise SystemExit(2)

def ok_smiles(s):
    return Chem.MolFromSmiles(s or '') is not None

def write_reports(root, status, checks, errors):
    report={'status':status,'checks':checks,'errors':errors}
    vdir=root/'validation'; vdir.mkdir(exist_ok=True)
    (vdir/'VALIDATION_REPORT.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    lines=['# Validation Report','',f'Status: `{status}`','']
    for name,val in checks.items():
        lines.append(f'- {name}: {val}')
    if errors:
        lines += ['','## Errors'] + [f'- {e}' for e in errors]
    (vdir/'VALIDATION_REPORT.md').write_text('\n'.join(lines)+'\n')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--package-root', default=str(Path(__file__).resolve().parents[1]))
    args=ap.parse_args(); root=Path(args.package_root)
    errors=[]; checks={}
    cases_csv=root/'gold_standard/SMALL_POLLUTANT_STRICT_V0_1_CASES.csv'
    reactions_csv=root/'gold_standard/SMALL_POLLUTANT_STRICT_V0_1_GOLD_STANDARD_REACTIONS.csv'
    products_jsonl=root/'gold_standard/SMALL_POLLUTANT_STRICT_V0_1_GOLD_STANDARD_PRODUCTS.jsonl'
    blind_csv=root/'gold_standard/SMALL_POLLUTANT_STRICT_V0_1_BLIND_PARENT_INPUTS.csv'
    schema_json=root/'schema/THREE_TOOL_PREDICTION_NORMALIZED_SCHEMA.json'
    score_script=root/'scripts/score_three_tool_predictions.py'
    cases=list(csv.DictReader(cases_csv.open()))
    reactions=list(csv.DictReader(reactions_csv.open()))
    products=[json.loads(line) for line in products_jsonl.open() if line.strip()]
    checks['case_count']=len(cases)
    if len(cases)!=18: errors.append('expected exactly 18 parent cases')
    checks['reaction_row_count']=len(reactions)
    checks['product_jsonl_count']=len(products)
    if not reactions or len(reactions)!=len(products): errors.append('reaction row count must be nonzero and match product jsonl count')
    for row in cases:
        if int(row.get('accepted_product_count','0')) < 1: errors.append('case has no accepted product: '+row.get('case_id',''))
        if not ok_smiles(row.get('parent_smiles_canonical','')): errors.append('invalid parent smiles: '+row.get('case_id',''))
    for row in reactions:
        if not ok_smiles(row.get('parent_smiles_canonical','')): errors.append('invalid parent smiles in reaction: '+row.get('case_id',''))
        if not ok_smiles(row.get('product_smiles_canonical','')): errors.append('invalid product smiles in reaction: '+row.get('case_id',''))
        if not row.get('product_inchikey',''): errors.append('empty product inchikey: '+row.get('case_id',''))
    blind_header=next(csv.reader(blind_csv.open()))
    checks['blind_columns']=blind_header
    leak_terms=['product','reaction','answer','evidence']
    leaked=[c for c in blind_header if any(t in c.lower() for t in leak_terms)]
    if leaked: errors.append('blind input leakage columns: '+','.join(leaked))
    try:
        json.loads(schema_json.read_text()); checks['schema_json_parseable']=True
    except Exception as e:
        checks['schema_json_parseable']=False; errors.append('schema JSON not parseable: '+repr(e))
    try:
        with tempfile.TemporaryDirectory() as td:
            td=Path(td)
            syn=td/'synthetic_predictions.jsonl'
            hit_case=cases[0]; miss_case=cases[1]
            first_prod=next(p for p in products if p['case_id']==hit_case['case_id'])
            rows=[
                {'tool_name':'synthetic','tool_version':'test','run_id':'validation','case_id':hit_case['case_id'],'parent_smiles':hit_case['parent_smiles_canonical'],'prediction_rank':1,'predicted_product_smiles_original':first_prod['product_smiles_canonical'],'predicted_product_smiles_canonical':first_prod['product_smiles_canonical'],'predicted_product_inchikey':first_prod['product_inchikey'],'raw_score':'','raw_confidence':'','provenance':'validation','raw_output_ref':'synthetic','normalization_status':'ok','normalization_note':'hit'},
                {'tool_name':'synthetic','tool_version':'test','run_id':'validation','case_id':miss_case['case_id'],'parent_smiles':miss_case['parent_smiles_canonical'],'prediction_rank':1,'predicted_product_smiles_original':'C','predicted_product_smiles_canonical':'C','predicted_product_inchikey':'VNWKTOKETHGBQD-UHFFFAOYSA-N','raw_score':'','raw_confidence':'','provenance':'validation','raw_output_ref':'synthetic','normalization_status':'ok','normalization_note':'miss'},
            ]
            syn.write_text(''.join(json.dumps(r, sort_keys=True)+'\n' for r in rows))
            out=td/'score'
            subprocess.run([sys.executable, str(score_script), '--gold-products', str(products_jsonl), '--predictions', str(syn), '--out-dir', str(out), '--k', '1,3,5,10'], check=True)
            checks['synthetic_scoring_runs']=True
    except Exception as e:
        checks['synthetic_scoring_runs']=False; errors.append('synthetic scoring failed: '+repr(e))
    for tool in ['biotransformer_envmicro','enviformer_latest']:
        rdir=root/'replay'/tool
        summ=rdir/'SCORING_SUMMARY.json'
        if summ.exists():
            data=json.loads(summ.read_text())
            checks[f'{tool}_replay_case_count']=data.get('case_count')
            if data.get('case_count') != 18: errors.append(tool+' replay case_count != 18')
            case_rows=list(csv.DictReader((rdir/'CASE_LEVEL_SCORING.csv').open()))
            if len(case_rows) != data.get('case_count'): errors.append(tool+' replay summary/case csv mismatch')
        elif (rdir/'REPLAY_UNAVAILABLE.json').exists():
            checks[f'{tool}_replay']='unavailable'
        else:
            errors.append(tool+' replay outputs missing')
    status='PASS' if not errors else 'FAIL'
    write_reports(root, status, checks, errors)
    if errors:
        raise SystemExit(1)
if __name__ == '__main__':
    main()
