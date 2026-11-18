"""Validation functions exported from the executed S8 modules.

Only import/namespace wiring is adapted. See provenance/SOURCE_MANIFEST.tsv.
"""
import copy
import json
import re
from . import common as N
from .common import sections,canonical

def validate(obj, request):
    """Typed scoring/range/evidence validation; no keyword-based scientific verdict."""
    errors=[];reviews=[]
    if not isinstance(obj,dict):return ['OUTPUT_NOT_OBJECT'],reviews
    if obj.get('schema_id')!='LIKERT_V05_S8_PARTIAL' or obj.get('rater_type')!='AI':errors.append('OUTPUT_IDENTITY')
    if obj.get('identity')!=request['identity']:errors.append('REPAIR_IDENTITY_MISMATCH')
    ds=obj.get('dimensions')
    if not isinstance(ds,dict) or set(ds)!=set(request['wanted']):return errors+['DIMENSIONS_MISMATCH'],reviews
    catbody=next(b for n,b in sections(request['body']['messages'][1]['content'])if n=='REFERENCE_CATALOG')
    cat=json.loads(re.search(r'\{.*\}',catbody,re.S)[0])
    ruletext=request['body']['messages'][0]['content']+'\n'+canonical(request['program'])
    for n,b in sections(request['body']['messages'][1]['content']):
        if n not in ['QUESTION','ANSWER']:ruletext+='\n'+b
    ruletext+='\n'+' '.join('R2-'+n for n in re.findall(r'\[P(\d+)\]',ruletext))
    allowed={'score_status','score','rationale','answer_locator','evidence_refs','rule_ids_cited',
             'key_error','key_error_argument','ne_basis','ne_unverified','missing_basis',
             'root_error_event_ids','unverified_subclaims','route_gate_effect',
             'nine_ten_blocked_by_evidence_gate','na_basis'}
    for d,v in ds.items():
        if not isinstance(v,dict):errors.append(d+':NOT_OBJECT');continue
        if set(v)-allowed:errors.append(d+':UNKNOWN_FIELDS')
        if not isinstance(v.get('rationale'),str)or not v['rationale'].strip():errors.append(d+':RATIONALE')
        if not isinstance(v.get('answer_locator'),str)or not v['answer_locator'].strip():errors.append(d+':LOCATOR')
        st,sc=v.get('score_status'),v.get('score')
        lo,hi=request['program']['allowed_ranges'][d]
        if st=='SCORED':
            if type(sc)is not int or not lo<=sc<=hi:errors.append(d+':SCORE_RANGE')
            if not v.get('evidence_refs'):errors.append(d+':NO_JUDGEMENT_REFERENCE')
        elif st=='NE':
            if sc is not None or not v.get('ne_basis')or not v.get('ne_unverified'):errors.append(d+':NE_BASIS')
            if d=='D3a' and request['program']['d3a_decision_status']in['SCORED','MISSING']:
                errors.append(d+':NE_CONFLICT_WITH_DETERMINED_PROGRAM_DECISION')
            reviews.append(dict(dimension=d,reason='NE requires review of specific scientific gap; not numeric success'))
        elif st=='MISSING':
            if type(sc)is not int or sc!=1 or not v.get('missing_basis'):errors.append(d+':MISSING_BASIS')
            if d=='D3a' and request['program']['d3a_decision_status']!='MISSING':errors.append(d+':MISSING_CONFLICT')
        else:errors.append(d+':STATUS')
        if d=='D3a' and request['program']['d3a_decision_status']=='MISSING'and(st!='MISSING'or sc!=1):
            errors.append(d+':PROGRAM_MISSING_REQUIRED')
        if v.get('key_error')not in['N','Y','UNRESOLVED']:errors.append(d+':KEY_STATUS')
        if v.get('key_error')=='Y':
            arg=v.get('key_error_argument')
            if st!='SCORED'or type(sc)is not int or sc>4:errors.append(d+':KEY_CAP')
            if not isinstance(arg,dict)or not all(arg.get(k)for k in ['dimension_failure','answer_locator','evidence_locator','support_scope']):errors.append(d+':KEY_ARGUMENT')
        refs=v.get('evidence_refs',[])
        if not isinstance(refs,list):errors.append(d+':REFS_NOT_ARRAY');refs=[]
        for ref in refs:
            if not isinstance(ref,dict):errors.append(d+':REF_NOT_OBJECT');continue
            rt,rid=ref.get('ref_type'),ref.get('ref_id')
            if rt not in ['GOLD_SLICE','E0_EVIDENCE','SCOPE_ROW','ANSWER_TEXT','QUESTION_TEXT','RUBRIC_CLAUSE']:errors.append(d+':REF_TYPE')
            if not isinstance(rid,str)or not rid or not ref.get('support_scope'):errors.append(d+':REF_SCOPE')
            if rt in ['GOLD_SLICE','E0_EVIDENCE','SCOPE_ROW']and rid not in cat.get(rt,[]):errors.append(d+':FABRICATED_REFERENCE')
        cited=v.get('rule_ids_cited',[])
        if not isinstance(cited,list):errors.append(d+':RULE_IDS_NOT_ARRAY');cited=[]
        if not cited:reviews.append(dict(dimension=d,reason='rule citations absent'))
        for rid in cited:
            if not isinstance(rid,str)or not rid or rid not in ruletext:errors.append(d+':FABRICATED_RULE')
    return errors,reviews


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


def normalize_response(raw,req):
    obj,view,changes=normalize(raw,req)
    system=req['body']['messages'][0]['content']
    known=set(re.findall(r'\[P(\d+)\]',system))
    aliases={}
    for value in obj.get('dimensions',{}).values():
        for rid in value.get('rule_ids_cited')or[]:
            m=re.fullmatch(r'P(\d+)[-–]P?(\d+)',rid)
            if m and int(m[1])<=int(m[2]) and all(str(n)in known for n in range(int(m[1]),int(m[2])+1)):
                aliases[rid]='exact contiguous range of actual supplied paragraphs'
    if aliases:
        view['body']['messages'][0]['content']+='\nExisting paragraph range aliases:\n'+N.canonical(aliases)
        changes.append(dict(action='recognize_real_paragraph_range_without_rewriting_citation',aliases=aliases))
    return obj,view,changes
