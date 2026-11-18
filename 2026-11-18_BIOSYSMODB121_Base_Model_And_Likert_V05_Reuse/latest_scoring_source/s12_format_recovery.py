"""Accept exact names of supplied rubric rows; never rewrite scores/citations."""
import copy
import csv
import io
import json
import re
from pathlib import Path

import run_scoring as S

HERE=Path(__file__).resolve().parent


def normalize(raw,req):
    obj,view,changes=S.E.normalize_for_request(raw,req)
    text=req['body']['messages'][0]['content'];aliases={}
    mapping=dict(D1=1,D2=2,D3a=3,D3b=4,D4=5,D5=6,D6=7)
    for v in obj.get('dimensions',{}).values():
        for rid in v.get('rule_ids_cited',[]):
            m=re.fullmatch(r'TABLE0[-_.](D[1-6](?:a|b)?)',rid)
            if m and m[1]in mapping:
                row=mapping[m[1]]
                if '[TABLE 0]'in text and re.search(r'^\s*R'+str(row)+r':\s*'+re.escape(m[1])+r'\b',text,re.M):
                    aliases[rid]='exact existing TABLE 0 R'+str(row)+' '+m[1]
    if aliases:
        view['body']['messages'][0]['content']+='\nExisting exact dimension names of supplied TABLE 0 rows:\n'+S.N.canonical(aliases)
        changes.append(dict(action='recognize_existing_table_row_by_exact_dimension_name',
                            validation_view_only=True,aliases=aliases,citations_not_rewritten=True))
    sections=dict(S.N.sections(req['body']['messages'][1]['content']))
    case=req['identity']['case_id']
    task=json.loads(sections['TASK_SCOPE'])
    assert task['case_id']==case
    roles_match=re.search(r'--- FILE: SCOPE_ROLES.tsv ---\n(.*?)(?=\n--- FILE:|$)',sections['GOLD_SLICE'],re.S)
    supplied_roles=list(csv.DictReader(io.StringIO(roles_match[1]),delimiter='\t'))if roles_match else[]
    role_aliases={}
    for value in obj.get('dimensions',{}).values():
        for rid in value.get('rule_ids_cited',[]):
            m=re.fullmatch(r'SCOPE_ROLES\.tsv:(ENTRY|TERMINAL|MAJOR|NONE|REQUIRED|BACKGROUND_NOT_REQUIRED)',rid)
            if m and any(m[1]in [r.get('key_role'),r.get('task_role')]for r in supplied_roles):
                role_aliases[rid]='existing supplied scope-data role anchor, cited in rule field; not an additional scientific rule'
    if role_aliases:
        view['body']['messages'][0]['content']+='\nExisting supplied scope-data anchors referenced in rule field:\n'+S.N.canonical(role_aliases)
        changes.append(dict(action='recognize_exact_existing_scope_data_anchor_in_rule_field',
                            validation_view_only=True,anchors=role_aliases,citations_not_rewritten=True))
    view_sections=dict(S.N.sections(view['body']['messages'][1]['content']))
    cat=json.loads(view_sections['REFERENCE_CATALOG']);scope_aliases=[]
    for value in obj.get('dimensions',{}).values():
        for ref in value.get('evidence_refs',[]):
            rid=ref.get('ref_id')
            if ref.get('ref_type')!='SCOPE_ROW'or rid in cat['SCOPE_ROW']:continue
            exact_case_alias=rid=='SCOPE_ROW#'+case
            exact_roles_file=(rid in ['SCOPE_ROLES.tsv','SCOPE_ROLES.tsv#case:'+case]
                              and rid in cat['GOLD_SLICE']and'--- FILE: SCOPE_ROLES.tsv ---'in sections['GOLD_SLICE'])
            if exact_case_alias or exact_roles_file:
                cat['SCOPE_ROW'].append(rid);scope_aliases.append(rid)
    if scope_aliases:
        old='===SECTION:REFERENCE_CATALOG_BEGIN===\n'+view_sections['REFERENCE_CATALOG']+'\n===SECTION:REFERENCE_CATALOG_END==='
        new='===SECTION:REFERENCE_CATALOG_BEGIN===\n'+S.N.canonical(cat)+'\n===SECTION:REFERENCE_CATALOG_END==='
        view['body']['messages'][1]['content']=view['body']['messages'][1]['content'].replace(old,new,1)
        changes.append(dict(action='recognize_exact_existing_scope_case_and_roles_file',validation_view_only=True,
                            references=scope_aliases,citations_not_rewritten=True))
    return obj,view,changes


def main():
    recovered=[]
    for p in sorted((HERE/'scoring').glob('*/RESULT.json')):
        rec=S.N.load(p)
        if rec['status']!='REJECTED':continue
        req=S.N.load(p.parent/'REQUEST.json');raw=rec['response']
        obj,view,changes=normalize(raw,req);errors,reviews=S.N.validate(obj,view)
        if errors:continue
        assert obj==raw,'this recovery must leave the complete response unchanged'
        result=copy.deepcopy(rec);result.update(status='OK',errors=[],reviews=reviews,
            normalizations=rec.get('normalizations',[])+changes,
            recovery_kind='OFFLINE_EXACT_EXISTING_ANCHOR_ALIAS_NO_NEW_CALL',original_result_sha256=S.N.file_sha(p),
            scores_statuses_rationales_citations_unchanged=True)
        result['rating']=dict(slot=rec['slot'],kind='S12_APPROVED_REFERENCE_SCOPE_NEW_RATING',
            dimensions=obj['dimensions'],totals=S.E.totals_contract(obj['dimensions']),
            per_dimension_provenance={d:dict(source=rec['transfer_id'],answer_sha256=req['identity']['answer_sha256'],
                request_body_sha256=req['body_sha256'],reference_manifest_sha256=req['identity']['source_artifact_sha256'],
                offline_derivative='exact_existing_table_row_alias')for d in S.N.DIMS},
            note='用户确认060四步/094两步后首次评分；原引用TABLE0维度名离线对应既有行，模型原分/理由/引用未改。')
        (p.parent/'RECOVERED_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        recovered.append(rec['slot'])
    print(json.dumps(dict(recovered=recovered,new_calls=0),ensure_ascii=False))


if __name__=='__main__':main()
