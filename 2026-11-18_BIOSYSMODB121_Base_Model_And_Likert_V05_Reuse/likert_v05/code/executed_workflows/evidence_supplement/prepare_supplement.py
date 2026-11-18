"""Freeze already downloaded public records for the remaining exact gaps."""
import csv
import hashlib
import json
import re
import sys
from html import unescape
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import recover_format as R
N=R.N
E=HERE/'evidence'
load=N.load
canon=N.canonical


def plain(html):
    html=re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',html,flags=re.S|re.I)
    return ' '.join(unescape(re.sub('<[^>]+>',' ',html)).split())


def prepare():
    manifests=[]
    for p in E.glob('*MANIFEST.json'):
        d=load(p);manifests.extend(d if isinstance(d,list)else[d])
    by_id={x['id']:x for x in manifests if x.get('status')==200}
    records={}
    def add(rid,source,content,note):
        meta=by_id[source]
        assert hashlib.sha256(Path(meta['file']).read_bytes()).hexdigest()==meta['sha256']
        records[rid]=dict(ref_id=rid,source_url=meta['url'],raw_sha256=meta['sha256'],
                          frozen_retrieval_date='2026-11-14',content=content,support_scope=note)
    # Exact EC records; do not infer that family activity proves a given strain.
    enz={}
    for block in (E/'enzyme_dat.raw').read_text().split('//\n'):
        m=re.search(r'^ID\s+(\S+)',block,re.M)
        if m:enz[m[1]]=block
    wanted_ec=['1.6.99.7','1.5.1.34','1.14.13.186','1.14.15.34','1.14.15.3',
        '1.1.1.1','1.2.1.3','1.14.13.230','1.1.2.9','1.14.13.7','1.13.11.2',
        '1.14.13.44','3.7.1.8','1.13.11.39','3.5.1.105','3.5.1.107','3.5.1.108',
        '3.5.4.45','4.4.1.12','4.4.1.24','1.13.11.74',
        '1.1.1.337','4.1.1.79','2.3.1.234','2.3.1.8']
    for ec in wanted_ec:
        if ec in enz:
            content='\n'.join(x for x in enz[ec].splitlines()if x[:2]in['ID','DE','AN','CA','CC'])
            add('SUPP:ENZYME:'+ec,'enzyme_dat',content,
                'Official ENZYME name/reaction/status only. Transfers are followed with their actual target record; broad class reactions do not certify specific substrate/protein/strain activity.')
    for tax in ['1833','62977','290398','28380','272943','1060','266834','290633']:
        d=load(E/f'taxonomy_{tax}.raw')
        content={k:v for k,v in d.items()if k in['scientificName','taxonId','rank','active','synonyms','otherNames','parent']}
        add('SUPP:TAX:'+tax,'taxonomy_'+tax,content,
            'Official taxonomic identity, rank and aliases. Historical names listed as aliases are not errors. Taxonomy alone does not prove step activity, pathway capability or all strain traits.')
    for dsm in ['3043','3503','158','43188']:
        text=plain((E/f'dsm_{dsm}.raw').read_text())
        start=text.find('Name:',text.find('DSM '+dsm))
        end=text.find('Risk group:',start)
        add('SUPP:DSM:'+dsm,'dsm_'+dsm,text[start:end],
            'DSMZ exact-strain catalogue identifiers and observed cultivation conditions. A culture temperature is not an optimum/minimum/maximum; a different strain cannot stand in for the answer strain.')
    x=load(E/'uniprot_petn.raw')
    for protein in x.get('results',[]):
        add('SUPP:UNIPROT:'+protein['primaryAccession'],'uniprot_petn',
            dict(accession=protein['primaryAccession'],organism=protein.get('organism'),
                 proteinDescription=protein.get('proteinDescription'),
                 comments=[c for c in protein.get('comments',[])if c['commentType']in['FUNCTION','CATALYTIC ACTIVITY']]),
            'Reviewed annotation with cited primary experiments. Inspect exact nitroglycerin reactions; do not extend first denitration to every downstream denitration without support.')
    literature_ids={}
    for source in ['primary_petn_old','primary_adp1','primary_sulfolactate','primary_harder',
                   'primary_gluconobacter','primary_canavanine','primary_ca3','primary_3hp',
                   'primary_ap1','pub_rhodococcus_quinaldine']:
        if source not in by_id:continue
        ds=load(Path(by_id[source]['file'])).get('resultList',{}).get('result',[])
        kept=[]
        for d in ds:
            if d.get('source')!='MED' or not d.get('abstractText'):continue
            rid='SUPP:PMID:'+d['id']
            content={k:d.get(k)for k in ['id','source','title','authorString','pubYear','doi','pmcid']}
            content['abstract']=plain(d['abstractText'])
            add(rid,source,content,
                'Primary bibliographic record and supplied abstract only; not a full-text inspection. Check exact organism, strain, substrate and stated methods. A search hit is not confirmation, and absence is not disproof.')
            kept.append(rid)
        literature_ids[source]=kept
    def ec(*ids):return ['SUPP:ENZYME:'+x for x in ids if 'SUPP:ENZYME:'+x in records]
    mapping={
        'B480-0042':['SUPP:UNIPROT:P71278']+literature_ids.get('primary_petn_old',[]),
        'B480-0043':['SUPP:UNIPROT:P71278']+ec('1.6.99.7','1.5.1.34')+literature_ids.get('primary_petn_old',[]),
        'B480-0090':ec('1.14.13.186','1.14.15.34'),
        'B480-0412':ec('1.14.15.3','1.1.1.1','1.2.1.3','1.14.13.230','1.1.2.9'),
        'GRK47__BIOPATH150_126':ec('1.14.13.230','1.1.1.1','1.1.2.9','1.2.1.3'),
        'GRK47__BIOPATH150_102':ec('1.14.13.7','1.13.11.2','1.14.13.44','3.7.1.8','1.13.11.39'),
        'GPT56L__BIOPATH150_053':ec('3.5.1.105','3.5.1.107','3.5.1.108','3.5.4.45'),
        'B480-0064':['SUPP:TAX:1833','SUPP:DSM:43188']+literature_ids.get('pub_rhodococcus_quinaldine',[]),
        'B480-0138':['SUPP:TAX:62977']+literature_ids.get('primary_adp1',[]),
        'B480-0240':ec('1.13.11.74')+literature_ids.get('primary_ap1',[]),
        'B480-0287':['SUPP:TAX:290398','SUPP:DSM:3043']+ec('1.1.1.337','4.1.1.79','2.3.1.234','2.3.1.8')+literature_ids.get('primary_sulfolactate',[]),
        'B480-0347':literature_ids.get('primary_harder',[]),
        'B480-0415':['SUPP:TAX:290633','SUPP:DSM:3503']+literature_ids.get('primary_gluconobacter',[]),
        'B480-0439':['SUPP:TAX:1060']+ec('4.4.1.12','4.4.1.24'),
        'B480-0474':['SUPP:TAX:266834']+literature_ids.get('primary_canavanine',[]),
        'GPT56L__BIOPATH150_090':['SUPP:TAX:28380']+literature_ids.get('pub_thauera_k172',[]),
        'GPT56L__BIOPATH150_093':literature_ids.get('primary_ca3',[]),
        'GRK47__BIOPATH150_082':['SUPP:TAX:272943','SUPP:DSM:158']+literature_ids.get('primary_3hp',[]),
    }
    assert len(mapping)==18
    for uid,ids in mapping.items():
        mapping[uid]=list(dict.fromkeys(x for x in ids if x in records))
        assert mapping[uid],uid
    grouped={}
    for row in csv.DictReader((HERE.parent/'RESIDUAL_NE_26.tsv').open(),delimiter='\t'):
        if row['slot']=='B480-0162':continue
        grouped.setdefault(row['slot'],[]).append(row['dimension'])
    assert set(grouped)==set(mapping)and sum(map(len,grouped.values()))==24
    output=dict(version='S8_REMAINING_TARGETED_EVIDENCE_20261114',
        records=records,slot_evidence=mapping,slot_dimensions=grouped,
        old_gold_and_accepted_sets_unchanged=True,
        evaluator_supplement_not_model_source=True,
        limitations='Fresh taxonomy nomenclature is evaluated with historical aliases; official identity/reaction records and abstracts do not prove every whole-pathway or strain-specific activity.',
        supplemental_record_count=len(records))
    (HERE/'EVIDENCE_SUPPLEMENT.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(target_slots=len(grouped),target_dimensions=24,records=len(records),new_score_calls=0)))
    return output


if __name__=='__main__':prepare()
