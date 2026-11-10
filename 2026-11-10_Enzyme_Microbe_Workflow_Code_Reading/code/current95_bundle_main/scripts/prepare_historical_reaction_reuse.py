"""Exact-key views over all three accepted historical reaction-asset routes.
Uses the old 422-key route/strict tables and OLD86 per-store locators; no new
asset generation, no copying old large stores, no overwrite of old files.
"""
import argparse,csv,hashlib,json,pickle
from pathlib import Path
import numpy as np

def table(p):
    with open(p) as f:return list(csv.DictReader(f,delimiter='\t'))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--step-table',required=True);ap.add_argument('--frozen',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    frozen=Path(a.frozen);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    wanted={s['model_key_sha256']:s['model_reaction'] for s in json.loads(Path(a.step_table).read_text())}
    strict={r['model_key_sha256'] for r in table(frozen/'R1R1_FINAL_REACTION_ASSET_STATUS_422.tsv') if r['final_strict_ready']=='TRUE'}
    route={r['model_key_sha256']:r for r in table(frozen/'R1R1_REACTION_ASSET_ROUTE_422.tsv')}
    old86={r['model_key_sha256']:r for r in table(frozen/'R1R1_OLD86_VERIFY.tsv')}
    cache={};molecule_maps={};ledger=[]
    def mapping(p):
        p=str(p)
        if p not in cache:cache[p]=pickle.load(open(p,'rb'))
        return cache[p]
    for key,rxn in sorted(wanted.items()):
        if key not in strict:continue
        r=route[key];fp=ct=mol=None
        if r['route']=='OLD_STORE:r1':
            z=old86[key];fp=Path(z['drfp_source'].split(':',1)[1]);ct=Path(z['center_source'].split(':',1)[1]);mol=Path(z['mol_conf_dir'])
        else:
            result=Path(r['s1_result'])
            if result.exists():
                if r['route']=='VERIFIED65_BUNDLE':
                    base=Path(json.loads(result.read_text())['R1R1_FINAL_SELECTED_RESULT']['bundle'])
                else:base=result.parent
                fp=base/'drfp/rxn2fp.pkl';ct=base/'reacting_center/reacting_center.pkl';mol=base/'molecule_conformation'
        if not fp or not fp.is_file() or not ct.is_file() or not (mol/'mol2id.csv').is_file():
            ledger.append({'key':key,'route':r['route'],'status':'REGISTERED_SOURCE_NOT_VISIBLE'});continue
        try:
            fv=mapping(fp)[rxn];cv=mapping(ct)[rxn]
            arr=np.asarray(fv)
            if arr.shape!=(2048,) or not np.isfinite(arr).all() or not arr.any() or len(cv)!=2 or not len(cv[0]) or not len(cv[1]):raise ValueError('FIELD_SHAPE_OR_FINITE')
            if str(mol) not in molecule_maps:
                with (mol/'mol2id.csv').open() as f:molecule_maps[str(mol)]={x['SMILES']:x['ID'] for x in csv.DictReader(f)}
            mm=molecule_maps[str(mol)];components=sorted({x.replace('*','C') for side in rxn.split('>>') for x in side.split('.') if x and x!='[*H2]'})
            if not all(x in mm and (mol/(str(mm[x])+'.sdf')).is_file() for x in components):raise ValueError('EXACT_COMPONENT_SDF_MISSING')
            dst=out/('RXASSET_'+key)
            for part in ('drfp','reacting_center','molecule_conformation'):(dst/part).mkdir(parents=True,exist_ok=True)
            (dst/'drfp/rxn2fp.pkl').write_bytes(pickle.dumps({rxn:fv}));(dst/'reacting_center/reacting_center.pkl').write_bytes(pickle.dumps({rxn:cv}))
            with (dst/'molecule_conformation/mol2id.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,['SMILES','ID']);w.writeheader()
                for i,x in enumerate(components,1):
                    w.writerow({'SMILES':x,'ID':i});link=dst/f'molecule_conformation/{i}.sdf'
                    if link.is_symlink() or link.exists():link.unlink()
                    link.symlink_to((mol/(str(mm[x])+'.sdf')).resolve())
            note={'model_key_sha256':key,'R1R1_FINAL_SELECTED_RESULT':{'status':'SUCCESS'},'reuse_only':True,'historical_route':r['route'],'fp_source':str(fp),'center_source':str(ct),'mol_source':str(mol),'fresh_tensor_graph_check':'PENDING_NODE_CONSUMER'}
            (dst/'R1R1_FINAL_ASSET_RESULT.json').write_text(json.dumps(note,indent=2)+'\n')
            ledger.append({'key':key,'route':r['route'],'status':'EXACT_EXISTING_VALUES_REUSED_NO_GENERATION'})
        except (KeyError,ValueError,TypeError,IndexError) as e:
            ledger.append({'key':key,'route':r['route'],'status':'SOURCE_NOT_REUSABLE','reason':str(e)})
    (out/'HISTORICAL_REUSE_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
    print(json.dumps({'reused':sum(x['status']=='EXACT_EXISTING_VALUES_REUSED_NO_GENERATION' for x in ledger),'source_records':len(ledger)}))
if __name__=='__main__':main()
