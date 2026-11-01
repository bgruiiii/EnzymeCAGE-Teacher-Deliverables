#!/usr/bin/env python3
"""Portable standard-library validation of the public teacher deliverable."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import tarfile


def read(p):
    with p.open(encoding='utf-8') as f:
        return list(csv.DictReader(f,delimiter='\t'))


def verify(root, hashes=True):
    root=Path(root)
    checks={}
    b=read(root/'data/batchB_recovery_inclusive_PROGRAM_480.tsv')
    a=read(root/'data/batchA_native_single_shot_FINAL_AXES.tsv')
    r=read(root/'data/batchB_LIKERT_480.tsv')
    d=read(root/'data/batchB_LIKERT_DIMENSIONS_3360.tsv')
    checks['A484_B480_R480_D3360']=len(a)==484 and len(b)==len(r)==480 and len(d)==3360
    bmap={x['b_slot_uid']:x for x in b};rmap={x['b_slot_uid']:x for x in r}
    checks['unique480_and_same_input_identity']=len(bmap)==len(rmap)==480 and set(bmap)==set(rmap) and all(
        x['case_id']==bmap[u]['case_id'] and x['answer_sha256']==bmap[u]['answer_sha256'] for u,x in rmap.items())
    checks['B120x4']=len({x['case_id'] for x in b})==120 and len({x['tested_model_config_id'] for x in b})==4
    checks['A_fixed121_each']=all(sum(x['model_config_id']==m for x in a)==121 for m in {x['model_config_id'] for x in a})
    checks['batch_isolation']=all(x['batch']=='batchA_native_single_shot' for x in a) and all(x['batch']=='batchB_recovery_inclusive' for x in b+r+d)
    checks['recovery20_native460']=sum(x['recovered']=='TRUE' for x in b)==20 and sum(x['recovered']=='FALSE' for x in b)==460
    checks['all480_valid_not_failure_totals']=all(x['system_run_status']=='OK' and x['validation_status']=='VALID' for x in r)
    program_weights={'layer_pathway':.45,'layer_smiles':.1,'layer_enzyme':.2,'layer_microbial_identity':.15,'layer_traits':.1}
    checks['program_five_layer_weight_math']=all(abs(float(x['science_weighted_total_100'])-sum(float(x[k])*w for k,w in program_weights.items()))<.011 for x in b)
    weights=dict(zip(['D1','D2','D3a','D3b','D4','D5','D6'],[1.5,2.5,1,1,1.5,1.5,1]))
    dm={(x['b_slot_uid'],x['dimension']):x for x in d}
    checks['unique3360_dimensions']=len(dm)==3360
    checks['all_verified_KE_caps']=all(x['key_error']!='Y' or (x['score']!='' and int(x['score'])<=4) for x in d)
    arithmetic=[]
    for u,x in rmap.items():
        numeric=True;total=0
        for dim,w in weights.items():
            z=dm[u,dim];s=z['score_status'];score=z['score']
            if s in ['SCORED','MISSING']:
                n=int(score);assert 1<=n<=10
                if s=='MISSING':assert n==1
                total+=w*n
            elif s in ['NE','NA']:
                assert score=='';numeric=False
            else:raise AssertionError('Invalid score status')
        arithmetic.append(abs(float(x['weighted_total_program'])-total)<1e-7 if numeric else x['weighted_total_program']=='')
    checks['all_weighted_totals_and_NE_MISSING']=all(arithmetic)
    costs=read(root/'data/ALL_CALLS_COST_AND_RETRY_HISTORY.tsv')
    known=[x for x in costs if x['cost_cny']!='']
    checks['usage_price_recomputed']=all(abs(float(x['cost_cny'])-(2*int(x['prompt_tokens'])+8*int(x['completion_tokens']))/1e6)<1e-9 for x in known)
    checks['unknown_not_zero_filled']=sum(x['accounting_status']=='UNKNOWN_RESERVE_RETAINED_NOT_ZERO_COST' and x['cost_cny']=='' for x in costs)==1
    checks['no_false_human_validation']=all(x['human_validity']=='PENDING' for x in r)
    checks['475_original_plus5_versioned_rescue']=sum(x['rating_version']=='R21_ORIGINAL_ACCEPTED475' for x in r)==475 and sum(x['rating_version']=='TARGETED5_TECHNICAL_CONTRACT_20261102' for x in r)==5
    hashed=0
    if hashes:
        manifest=root/'MANIFEST.sha256'
        if not manifest.exists():manifest=root/'PAYLOAD.sha256'
        assert manifest.exists(), 'Missing manifest'
        for line in manifest.read_text().splitlines():
            wanted,name=line.split(None,1);p=PurePosixPath(name)
            assert not p.is_absolute() and '..' not in p.parts
            assert hashlib.sha256((root/name).read_bytes()).hexdigest()==wanted,name
            hashed+=1
        checks['manifest_all_hashes']=True
    for archive in (root/'archives').glob('*.tar.gz') if (root/'archives').exists() else []:
        with tarfile.open(archive,'r:gz') as t:
            names=[]
            for m in t.getmembers():
                p=PurePosixPath(m.name)
                assert not p.is_absolute() and '..' not in p.parts and m.isfile() and not m.issym() and not m.islnk()
                names.append(m.name)
            assert len(names)==len(set(names))
        checks['tar_regular_unique_relative_members']=True
    assert all(checks.values()),checks
    return dict(checks=checks,hash_entries_verified=hashed,known_cost_cny=round(sum(float(x['cost_cny']) for x in known),6),calls=len(costs),valid480=len(r),dimensions=len(d))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--without-manifest',action='store_true')
    a=p.parse_args()
    print(json.dumps(verify(a.root,not a.without_manifest),ensure_ascii=False,indent=2))
