"""Offline revalidation of already paid S8 returns; never sends requests."""
import copy
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
S8=HERE.parent
SRC=S8/'execution/scope_r1'
sys.path[:0]=[str(S8/'scope_fix_20261114'),str(S8.parent/'S6_COMBINED_V05_SCORING_20261111/runtime/f2')]
import scoped_ne_repair as F
from f2r12_transport import parse_sse_bytes,new_stream_state
from f2r12_common import totals_contract
N=F.BASE
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def normalize(obj,req):
    out=copy.deepcopy(obj);changes=[]
    ident=out.get('identity')or{}
    expected=req['identity']
    diff=[k for k in expected if expected[k]!=ident.get(k)]
    diagnostic={'rubric_sha256','source_artifact_sha256','program_and_materials_sha256'}
    # Only a single typo in a redundant diagnostic echo, with every other
    # identity field (including answer and repair digest) exactly matching.
    if len(diff)==1 and diff[0]in diagnostic and set(ident)==set(expected):
        key=diff[0];got,want=ident[key],expected[key]
        one_edit=(isinstance(got,str)and len(got)==63 and any(want[:i]+want[i+1:]==got for i in range(64)))or(
            isinstance(got,str)and len(got)==64 and sum(a!=b for a,b in zip(got,want))==1)
        if one_edit and re.fullmatch('[0-9a-f]+',got):
            ident[key]=want;changes.append(dict(path='identity.'+key,action='restore_single_typo_in_redundant_echo',old=got,new=want))
    user=req['body']['messages'][1]['content']
    catsection=next(b for n,b in N.sections(user)if n=='REFERENCE_CATALOG')
    cat=json.loads(re.search(r'\{.*\}',catsection,re.S)[0])
    sysmsg=req['body']['messages'][0]['content']
    aliases={}
    for d,v in out.get('dimensions',{}).items():
        arg=v.get('key_error_argument')
        if isinstance(arg,str):
            matches=list(re.finditer(r'(?<![A-Za-z_])(dimension_failure|answer_locator|evidence_locator|support_scope)\s*[:=：]',arg))
            if len(matches)==4 and {m[1]for m in matches}=={'dimension_failure','answer_locator','evidence_locator','support_scope'}:
                fields={m[1]:arg[m.end():matches[i+1].start()if i+1<len(matches)else len(arg)].strip()for i,m in enumerate(matches)}
                if all(fields.values()):
                    v['key_error_argument']=fields
                    changes.append(dict(path=d+'.key_error_argument',action='parse_existing_four_labelled_fields',original_text=arg))
        for i,ref in enumerate(v.get('evidence_refs')or[]):
            if ref.get('ref_type')=='FORMAL_CASES'and ref.get('ref_id')in cat.get('GOLD_SLICE',[])and ref['ref_id'].startswith('formal_cases.tsv'):
                ref['ref_type']='GOLD_SLICE';changes.append(dict(path=f'{d}.evidence_refs.{i}.ref_type',action='exact_frozen_file_type_alias',old='FORMAL_CASES',new='GOLD_SLICE'))
        for rid in v.get('rule_ids_cited')or[]:
            table=re.fullmatch(r'TABLE0[-_]([RD])(\d+)',rid)
            para=re.fullmatch(r'C04\.(\d+)',rid)
            generic=re.fullmatch(r'TABLE(\d+)',rid)
            if table:
                row=int(table[2])
                if table[1]=='D':row={'1':1,'2':2}.get(table[2],-1)
                if '[TABLE 0]'in sysmsg and re.search(r'^  R'+str(row)+r':',sysmsg,re.M):aliases[rid]=f'TABLE 0 row R{row}'
            elif para:
                block=sysmsg[sysmsg.index('## C04 '):sysmsg.index('## C05 ')]
                if re.search(r'^'+para[1]+r'\. ',block,re.M):aliases[rid]='C04 paragraph '+para[1]
            elif generic and '[TABLE '+generic[1]+']'in sysmsg:aliases[rid]='TABLE '+generic[1]
    # Citation IDs stay as written. The validation-only view recognizes exact
    # aliases of actual supplied table/paragraph anchors; it is never sent.
    view=copy.deepcopy(req)
    if aliases:
        view['body']['messages'][0]['content']+='\nExisting anchor aliases for offline validation only:\n'+N.canonical(aliases)
        changes.append(dict(action='recognize_existing_anchor_aliases_without_rewriting_citations',aliases=aliases))
    return out,view,changes


def main():
    (HERE/'recovered').mkdir(exist_ok=True)
    missing=list(csv.DictReader((SRC/'UNRESOLVED_SLOTS.tsv').open(),delimiter='\t'))
    recovered=[];remaining=[]
    for row in missing:
        uid=row['slot'];wanted=row['requested_dimensions'].split(',');req=F.build(uid,wanted)
        archive=Path(row['archive']);meta=N.load(archive/'response_meta.json')
        assert sha(archive/'response_raw.bin')==meta['response_raw_sha256']
        posted=N.load(archive/'request_body.json');assert posted==req['body'],uid
        state=new_stream_state()
        try:raw=json.loads(parse_sse_bytes((archive/'response_raw.bin').read_bytes(),state))
        except ValueError as exc:
            remaining.append(dict(slot=uid,dimensions=wanted,reason='INCOMPLETE_JSON',detail=str(exc),source_transfer_id=row['transfer_id']));continue
        assert meta['stream_status']=='COMPLETE'and state['done_seen']
        normalized,view,changes=normalize(raw,req)
        errors,reviews=N.validate(normalized,view)
        if errors:
            remaining.append(dict(slot=uid,dimensions=wanted,reason='STILL_REJECTED',errors=errors,source_transfer_id=row['transfer_id']));continue
        assert all(raw['dimensions'][d]['score']==normalized['dimensions'][d]['score']and
                   raw['dimensions'][d]['score_status']==normalized['dimensions'][d]['score_status']and
                   raw['dimensions'][d]['rationale']==normalized['dimensions'][d]['rationale']for d in wanted)
        derivative=dict(slot=uid,source_transfer_id=row['transfer_id'],raw_response_sha256=meta['response_raw_sha256'],
            actual_request_sha256=req['body_sha256'],kind='OFFLINE_FORMAT_DERIVATIVE_NOT_NEW_GENERATION',
            response=normalized,normalizations=changes,model_scores_statuses_rationales_unchanged=True,
            merged=N.merge_validated(normalized,view,row['transfer_id'],totals_contract),new_api_calls=0)
        (HERE/'recovered'/f'RECOVERED_{uid}.json').write_text(json.dumps(derivative,ensure_ascii=False,indent=2)+'\n')
        recovered.append(derivative)
    # Compose a new version; do not overwrite the execution team's originals.
    finals={x['slot']:x for x in map(json.loads,(SRC/'FINAL_RATINGS_S8.jsonl').read_text().splitlines())}
    for rec in recovered:
        old=copy.deepcopy(finals[rec['slot']]);merged=rec['merged'];wanted=merged['replaced_dimensions']
        for d in wanted:
            assert old['dimensions'][d]['score_status']=='NE'
            finals[rec['slot']]['dimensions'][d]=copy.deepcopy(merged['dimensions'][d])
            finals[rec['slot']]['per_dimension_provenance'][d]=dict(source=rec['source_transfer_id'],derivative=f'recovered/RECOVERED_{rec["slot"]}.json',request_sha256=rec['actual_request_sha256'])
        assert all(finals[rec['slot']]['dimensions'][d]==old['dimensions'][d]for d in N.DIMS if d not in wanted)
        finals[rec['slot']]['kind']='S8_COORDINATOR_OFFLINE_FORMAT_RECOVERY'
    states={d:Counter()for d in N.DIMS};comparable=0
    with(HERE/'FINAL_RATINGS_REVIEWED.jsonl').open('w')as f, (HERE/'FINAL_SCORES_REVIEWED.tsv').open('w')as table:
        fields=['slot','total_status','weighted_total']+[d+'_'+k for d in N.DIMS for k in ['status','score']]
        wr=csv.DictWriter(table,fieldnames=fields,delimiter='\t',lineterminator='\n');wr.writeheader()
        for uid,r in sorted(finals.items()):
            r['totals']=totals_contract(r['dimensions']);t=r['totals'];comparable+=t['status']=='COMPARABLE'
            row=dict(slot=uid,total_status=t['status'],weighted_total=t['weighted_total'])
            for d,v in r['dimensions'].items():states[d][v['score_status']]+=1;row[d+'_status']=v['score_status'];row[d+'_score']=v.get('score')
            wr.writerow(row);f.write(json.dumps(r,ensure_ascii=False)+'\n')
    ledpath=S8/'execution/work/ledger/BUDGET_STATE.json';ledger=N.load(ledpath)
    report=dict(positions=len(finals),zero_cost_recovered_slots=len(recovered),recovered_slots=[x['slot']for x in recovered],
        still_unresolved=remaining,comparable_totals=comparable,not_comparable_totals=len(finals)-comparable,
        residual_NE_dimensions=sum(v.get('NE',0)for v in states.values()),dimension_counts={d:dict(v)for d,v in states.items()},
        paid_calls_by_review=0,ledger_sha256=sha(ledpath),attempts=ledger['attempts_used'],estimated_cny=ledger['committed_spend_cny'])
    (HERE/'RECOVERY_REVIEW_COUNTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
