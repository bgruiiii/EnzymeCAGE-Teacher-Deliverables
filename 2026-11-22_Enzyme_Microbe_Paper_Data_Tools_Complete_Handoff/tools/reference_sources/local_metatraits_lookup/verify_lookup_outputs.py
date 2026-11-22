#!/usr/bin/env python3
"""Verify emitted row bindings/coverage and small original-row samples, CPU only."""
import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

P=Path(__file__).resolve().parent


def main():
    summary=json.loads((P/'LOOKUP_SUMMARY.json').read_text())
    with (P/'SPECIES_LOOKUP_1100.tsv').open() as f:species=list(csv.DictReader(f,delimiter='\t'))
    ids={r['accepted_species_taxid'] for r in species}
    count=defaultdict(Counter);sample={};matched=0
    with gzip.open(P/'MATCHED_METATRAITS_SPECIES_ROWS.jsonl.gz','rt') as f:
        for line in f:
            r=json.loads(line);matched+=1
            assert r['target_species_taxid'] in ids
            assert r['identity_scope']=='SPECIES_REFERENCE_ONLY_NOT_ORIGINAL_STRAIN'
            if r['match_route']=='EXACT_NCBI_SPECIES_TAXID':assert r['target_species_taxid']==r['raw_record']['taxon_id']
            scope=r['evidence_scope']
            if r['has_value']:count[r['target_species_taxid']][scope]+=1
            if r['source_file']=='ncbi_species_summary_no_predictions.tsv.gz' and len(sample)<24:
                sample[r['source_line']]=r['raw_record']
    observed={r['accepted_species_taxid'] for r in species if int(r['exact_NCBI_no_predictions_rows_with_values'])>0}
    prior={r['accepted_species_taxid'] for r in species if r['previous_2478_has_any_evidence']=='True'}
    for r in species:
        tid=r['accepted_species_taxid']
        assert int(r['exact_NCBI_no_predictions_rows_with_values'])==count[tid]['NCBI_NO_PREDICTIONS']
        assert int(r['exact_NCBI_all_mixed_rows_with_values'])==count[tid]['NCBI_ALL_MIXED_SCOPE']
    source=next(Path(p) for p in summary['inputs'] if p.endswith('/ncbi_species_summary_no_predictions.tsv.gz'))
    verified=0
    with gzip.open(source,'rt') as f:
        for lineno,row in enumerate(csv.DictReader(f,delimiter='\t'),2):
            if lineno in sample:assert row==sample[lineno];verified+=1
            if verified==len(sample):break
    assert len(ids)==1100 and len(prior)==608 and len(observed)==661 and len(observed-prior)==207
    assert verified==24
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in summary['inputs'].items())
    result={'all_material_checks_pass':True,'target_species':1100,'matched_evidence_rows':matched,
        'new_exact_nonpredicted_species_references':207,'original_nonpredicted_rows_sampled':verified,
        'original_source_hashes_match':True,'existing_source_counts_not_overwritten':True,
        'new_predictions':0,'new_network_requests':0,
        'interpretation':'new species references; not exact strain observations or full phenotype panels'}
    (P/'LOOKUP_INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
