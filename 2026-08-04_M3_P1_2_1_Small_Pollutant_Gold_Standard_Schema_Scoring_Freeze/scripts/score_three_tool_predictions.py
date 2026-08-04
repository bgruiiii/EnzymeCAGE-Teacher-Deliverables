#!/usr/bin/env python3
import argparse, csv, json, sys
from collections import defaultdict
from pathlib import Path
try:
    from rdkit import Chem
except Exception:
    sys.stderr.write('M3_P1_2_1_SCORING_BLOCKED_RDKIT_UNAVAILABLE\n')
    raise SystemExit(2)

def canon(smiles):
    mol = Chem.MolFromSmiles(smiles or '')
    if mol is None:
        return '', ''
    return Chem.MolToSmiles(mol, canonical=True), Chem.MolToInchiKey(mol)

def parse_k(text):
    vals=[]
    for part in text.split(','):
        part=part.strip()
        if part:
            vals.append(int(part))
    return sorted(set(vals))

def load_gold(path):
    by_case=defaultdict(list)
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            obj=json.loads(line)
            ik=obj.get('product_inchikey') or canon(obj.get('product_smiles_canonical',''))[1]
            if not ik:
                raise SystemExit('gold product missing InChIKey: '+json.dumps(obj, sort_keys=True))
            obj=dict(obj); obj['product_inchikey']=ik
            by_case[obj['case_id']].append(obj)
    return dict(by_case)

def iter_prediction_rows(path):
    with open(path) as f:
        for line_no,line in enumerate(f,1):
            if not line.strip():
                continue
            obj=json.loads(line)
            if isinstance(obj.get('predictions'), list):
                tool_name=obj.get('tool_id') or obj.get('tool_display_name') or ''
                for p in obj.get('predictions') or []:
                    yield {
                        'tool_name': tool_name,
                        'tool_version': '',
                        'run_id': '',
                        'case_id': obj.get('case_id',''),
                        'parent_smiles': obj.get('input_parent_smiles',''),
                        'prediction_rank': p.get('rank'),
                        'predicted_product_smiles_original': p.get('product_smiles_raw','') or p.get('product_smiles_canonical',''),
                        'predicted_product_smiles_canonical': p.get('product_smiles_canonical',''),
                        'predicted_product_inchikey': p.get('product_inchikey',''),
                        'raw_score': p.get('raw_score',''),
                        'raw_confidence': '',
                        'provenance': 'nested_prediction_package',
                        'raw_output_ref': f'{path}:{line_no}',
                        'normalization_status': p.get('normalization_status','ok'),
                        'normalization_note': p.get('rank_semantics','') or p.get('score_semantics',''),
                    }
            else:
                yield obj

def as_int_rank(v):
    try:
        return int(v)
    except Exception:
        return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--gold-products', required=True)
    ap.add_argument('--predictions', required=True)
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--k', default='1,3,5,10')
    args=ap.parse_args()
    ks=parse_k(args.k)
    max_k=max(ks) if ks else 10
    gold=load_gold(args.gold_products)
    preds_by_case=defaultdict(list)
    for row in iter_prediction_rows(args.predictions):
        case_id=row.get('case_id','')
        rank=as_int_rank(row.get('prediction_rank'))
        if not case_id or rank is None or rank < 1:
            continue
        status=row.get('normalization_status','') or 'ok'
        smi=row.get('predicted_product_smiles_original','') or row.get('predicted_product_smiles_canonical','')
        can=row.get('predicted_product_smiles_canonical','')
        ik=row.get('predicted_product_inchikey','')
        if status != 'invalid_smiles' and (not ik or not can):
            can2, ik2 = canon(smi)
            can = can or can2
            ik = ik or ik2
            if not ik:
                status='invalid_smiles'
        preds_by_case[case_id].append({**row, 'prediction_rank': rank, 'predicted_product_smiles_canonical': can, 'predicted_product_inchikey': ik, 'normalization_status': status})
    out=Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    case_fields=['case_id','case_status','accepted_product_count','prediction_count','first_hit_rank'] + [f'hit_at_{k}' for k in ks] + ['reciprocal_rank_at_10','recovered_product_count_at_10','product_recall_at_10']
    prod_fields=['case_id','product_name','product_inchikey','first_recovered_rank'] + [f'recovered_at_{k}' for k in ks]
    case_rows=[]; product_rows=[]
    for case_id in sorted(gold):
        accepted=gold[case_id]
        accepted_iks={p['product_inchikey'] for p in accepted}
        preds=sorted(preds_by_case.get(case_id, []), key=lambda x:(x['prediction_rank'], x.get('predicted_product_inchikey','')))
        valid_preds=[p for p in preds if p.get('normalization_status') != 'invalid_smiles' and p.get('predicted_product_inchikey')]
        hit_ranks=[p['prediction_rank'] for p in valid_preds if p.get('predicted_product_inchikey') in accepted_iks]
        first_hit=min(hit_ranks) if hit_ranks else ''
        recovered_by_k={k:set() for k in ks}
        first_by_product={ik:'' for ik in accepted_iks}
        for p in valid_preds:
            ik=p.get('predicted_product_inchikey')
            rank=p['prediction_rank']
            if ik in accepted_iks:
                if first_by_product[ik] == '' or rank < first_by_product[ik]:
                    first_by_product[ik]=rank
                for k in ks:
                    if rank <= k:
                        recovered_by_k[k].add(ik)
        recovered_at_10={p.get('predicted_product_inchikey') for p in valid_preds if p['prediction_rank'] <= 10 and p.get('predicted_product_inchikey') in accepted_iks}
        row={'case_id':case_id,'case_status':'ok','accepted_product_count':len(accepted),'prediction_count':len(preds),'first_hit_rank':first_hit}
        for k in ks:
            row[f'hit_at_{k}']=1 if recovered_by_k[k] else 0
        row['reciprocal_rank_at_10']=(1.0/first_hit) if first_hit != '' and first_hit <= 10 else 0.0
        row['recovered_product_count_at_10']=len(recovered_at_10)
        row['product_recall_at_10']=len(recovered_at_10)/len(accepted)
        case_rows.append(row)
        for p in accepted:
            ik=p['product_inchikey']
            prow={'case_id':case_id,'product_name':p.get('product_name',''),'product_inchikey':ik,'first_recovered_rank':first_by_product[ik]}
            for k in ks:
                prow[f'recovered_at_{k}']=1 if ik in recovered_by_k[k] else 0
            product_rows.append(prow)
    with (out/'CASE_LEVEL_SCORING.csv').open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=case_fields); w.writeheader(); w.writerows(case_rows)
    with (out/'PRODUCT_LEVEL_SCORING.csv').open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=prod_fields); w.writeheader(); w.writerows(product_rows)
    n=len(case_rows) or 1
    summary={
        'case_count': len(case_rows),
        'accepted_product_count': sum(int(r['accepted_product_count']) for r in case_rows),
        'prediction_count': sum(int(r['prediction_count']) for r in case_rows),
        'mean_reciprocal_rank_at_10': sum(float(r['reciprocal_rank_at_10']) for r in case_rows)/n,
        'mean_product_recall_at_10': sum(float(r['product_recall_at_10']) for r in case_rows)/n,
        'recovered_product_count_at_10': sum(int(r['recovered_product_count_at_10']) for r in case_rows),
    }
    for k in ks:
        summary[f'hit_at_{k}_count']=sum(int(r[f'hit_at_{k}']) for r in case_rows)
        summary[f'hit_at_{k}_rate']=summary[f'hit_at_{k}_count']/n
    with (out/'SCORING_SUMMARY.json').open('w') as f:
        json.dump(summary, f, indent=2, sort_keys=True); f.write('\n')
if __name__ == '__main__':
    main()
