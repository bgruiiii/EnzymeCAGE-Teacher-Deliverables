#!/usr/bin/env python3
"""Offline species-reference lookup, preserving raw MetaTraits rows and scope.
Does not reassign strain traits, modify previous counts, or run predictors.
"""
import ast
import csv
import gzip
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

OUT=Path(__file__).resolve().parent
R=OUT.parent
REPO=R.parents[3]
DATA=REPO/'data/metatraits'
TARGET=R/'ENZYME_HOST_PAPER_CLOSEOUT_20261122/COMPLETE82_SPECIES_TRAIT_COVERAGE_1100.tsv'
PATTERN_SOURCE=REPO/'custom/github_upload/EnzymeCAGE-Enzyme-Microbe-Workflow_20261110/code/metatraits_etl/run_metatraits_c7_1_mapping.py'
EXPECTED={
 'ncbi_species_summary_no_predictions.tsv.gz':'9e16ca57b94819fa591f32bc1cf194c82eae85b0dbbc454a3c1a449257a33873',
 'ncbi_species_summary_all.tsv.gz':'9118379f800c5f2d8f0d0787ffd3045cbe3bb84a592657b06723252c13799bcd',
 'gtdb_species_summary_no_predictions.tsv.gz':'e676d4cd8c9244ffde60cc5968b3806d8a5fb3ada5a505d53c22b27e1e1e3df7',
 'NCBI2GTDB.tsv.gz':'761d5537a7edb4b0133e88e7bbc85570cf3cb6f2555b9f9ce6cca3e1056a0ddd',
 'GTDB2NCBI.tsv.gz':'892ecf0410091e3f2b4c88e5e129cae3cc43117613b1745aa73f95ccdcfbb9e3'}


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(x):return re.sub(r'\s+',' ',x.strip()).casefold()
def nonmissing(x):return str(x).strip().lower() not in ['', 'na', 'nan', 'none', 'null', 'no robust majority']
def has_value(r):
    return any(nonmissing(r.get(k,'')) for k in ['consensus_value','minimum','median','mean','maximum','discrete_values'])


def main():
    OUT.mkdir(exist_ok=True)
    assert DATA.is_dir(),DATA
    with TARGET.open() as f:targets=list(csv.DictReader(f,delimiter='\t'))
    assert len(targets)==1100 and len({r['accepted_species_taxid'] for r in targets})==1100
    ts={r['accepted_species_taxid']:r for r in targets}
    names=defaultdict(set)
    for taxid,r in ts.items():
        for n in r['species_names'].split(';'):
            if n.strip():names[norm(n)].add(taxid)
    # Recover only the accepted literal mapping rules; never execute old script.
    tree=ast.parse(PATTERN_SOURCE.read_text());patterns=None
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='F_PATTERNS' for t in node.targets):
            patterns=ast.literal_eval(node.value)
    assert patterns and not patterns['F5']
    def panels(r):
        return [fid for fid,rules in patterns.items() if any(word in r.get(field,'').lower() for field,word in rules)]
    inputs={str(TARGET):digest(TARGET),str(PATTERN_SOURCE):digest(PATTERN_SOURCE)}
    for name,want in EXPECTED.items():
        p=DATA/name;h=digest(p);assert h==want,(name,h);inputs[str(p)]=h
    stats=defaultdict(lambda:defaultdict(int));scanned={};crosswalk=[]
    # Mapping rows are evidence only. No majority-fraction guess is promoted to exact identity.
    with gzip.open(DATA/'NCBI2GTDB.tsv.gz','rt') as f:
        for lineno,r in enumerate(csv.DictReader(f,delimiter='\t'),2):
            tid=r['taxonID NCBI']
            if tid in ts:
                crosswalk.append({'accepted_species_taxid':tid,'gtdb_taxid':r['taxonID GTDB'],
                    'majority_fraction':r['majority fraction'],'ncbi_species_name':r['species (NCBI)'],
                    'gtdb_species_name':r['species (GTDB)'],'source_line':lineno,
                    'mapping_scope':'NCBI_TO_GTDB_REFERENCE_NOT_EXACT_STRAIN'})
    gtdb_to_targets=defaultdict(set)
    for r in crosswalk:gtdb_to_targets[r['gtdb_taxid']].add(r['accepted_species_taxid'])
    outputs=OUT/'MATCHED_METATRAITS_SPECIES_ROWS.jsonl.gz'
    with outputs.open('wb') as rawout, gzip.GzipFile(filename='',fileobj=rawout,mode='wb',mtime=0) as gz:
        def emit(tid,route,name,lineno,row,scope):
            ids=panels(row);value=has_value(row)
            stats[tid][scope+'_rows']+=1
            if value:stats[tid][scope+'_value_rows']+=1
            if value and set(ids)&{'F1','F2','F3','F4'}:stats[tid][scope+'_environment_value_rows']+=1
            rec={'target_species_taxid':tid,'target_species_names':ts[tid]['species_names'],
                'match_route':route,'identity_scope':'SPECIES_REFERENCE_ONLY_NOT_ORIGINAL_STRAIN',
                'evidence_scope':scope,'source_file':name,'source_file_sha256':EXPECTED[name],
                'source_line':lineno,'has_value':value,'C7_panel_ids':ids,'raw_record':row}
            gz.write((json.dumps(rec,ensure_ascii=False,allow_nan=False)+'\n').encode())
        for name in ['ncbi_species_summary_no_predictions.tsv.gz','ncbi_species_summary_all.tsv.gz','gtdb_species_summary_no_predictions.tsv.gz']:
            count=0
            with gzip.open(DATA/name,'rt') as f:
                for lineno,row in enumerate(csv.DictReader(f,delimiter='\t'),2):
                    count+=1;tid=row['taxon_id']
                    if name.startswith('gtdb'):
                        for targetid in sorted(gtdb_to_targets.get(tid,())):
                            emit(targetid,'DOCUMENTED_NCBI_TO_GTDB',name,lineno,row,'GTDB_NO_PREDICTIONS_REFERENCE')
                        continue
                    hit={tid} if tid in ts else set()
                    route='EXACT_NCBI_SPECIES_TAXID'
                    if not hit:
                        hit=names.get(norm(row['taxon_name']),set());route='EXACT_NAME_DIFFERENT_TAXID_REFERENCE'
                    if not hit:continue
                    for targetid in sorted(hit):
                        if name.endswith('_no_predictions.tsv.gz'):
                            scope='NCBI_NO_PREDICTIONS'
                        else:
                            # 'all' rows mix sources: never call all-minus-no observed.
                            scope='NCBI_ALL_MIXED_SCOPE'
                        if route!='EXACT_NCBI_SPECIES_TAXID':scope+='__NAME_REFERENCE'
                        emit(targetid,route,name,lineno,row,scope)
            scanned[name]=count
    resultrows=[]
    for tid,t in ts.items():
        s=stats[tid]
        no=s.get('NCBI_NO_PREDICTIONS_value_rows',0)
        mix=s.get('NCBI_ALL_MIXED_SCOPE_value_rows',0)
        gtdb=s.get('GTDB_NO_PREDICTIONS_REFERENCE_value_rows',0)
        name_ref=sum(v for k,v in s.items() if '__NAME_REFERENCE_value_rows' in k)
        resultrows.append({'accepted_species_taxid':tid,'species_names':t['species_names'],
            'previous_2478_has_any_evidence':t['has_any_usable_trait_evidence'],
            'exact_NCBI_no_predictions_rows_with_values':no,
            'exact_NCBI_no_predictions_environment_rows_with_values':s.get('NCBI_NO_PREDICTIONS_environment_value_rows',0),
            'exact_NCBI_all_mixed_rows_with_values':mix,
            'GTDB_crosswalk_no_predictions_reference_rows_with_values':gtdb,
            'exact_name_other_taxid_reference_rows_with_values':name_ref,
            'lookup_result':'EXACT_SPECIES_NONPREDICTED_REFERENCE' if no else 'EXACT_SPECIES_MIXED_SCOPE_REFERENCE' if mix else 'MAPPED_OR_NAME_SPECIES_REFERENCE' if gtdb or name_ref else 'NO_MATCH_IN_LOCAL_SPECIES_TABLES',
            'scope':'species-reference evidence only; no source strain identity upgrade',
            'new_prediction_run':False})
    def wt(name,rows):
        with (OUT/name).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    wt('SPECIES_LOOKUP_1100.tsv',resultrows)
    if crosswalk:wt('NCBI_GTDB_MAPPING_REFERENCES.tsv',crosswalk)
    prior_gap=[r for r in resultrows if r['previous_2478_has_any_evidence']=='False']
    summary={'target_species':1100,'prior_2478_with_any_evidence':608,'prior_gap_species':len(prior_gap),
        'exact_NCBI_nonpredicted_species_with_values':sum(r['exact_NCBI_no_predictions_rows_with_values']>0 for r in resultrows),
        'exact_NCBI_nonpredicted_environment_species':sum(r['exact_NCBI_no_predictions_environment_rows_with_values']>0 for r in resultrows),
        'prior_gap_exact_NCBI_nonpredicted_with_values':sum(r['exact_NCBI_no_predictions_rows_with_values']>0 for r in prior_gap),
        'prior_gap_exact_NCBI_all_mixed_with_values':sum(r['exact_NCBI_all_mixed_rows_with_values']>0 for r in prior_gap),
        'result_distribution':dict(Counter(r['lookup_result'] for r in resultrows)),
        'scanned_rows':scanned,'inputs':inputs,'new_database_requests':0,'new_predictions':0,
        'previous_source_level_counts_modified':False,
        'note':'raw species table lookup is broader than curated2478/source-key join; all table is mixed, mapped/name routes are reference only'}
    assert len(resultrows)==1100 and len(prior_gap)==492
    assert all(digest(Path(p))==h for p,h in inputs.items())
    (OUT/'LOOKUP_SUMMARY.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='inputs'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
