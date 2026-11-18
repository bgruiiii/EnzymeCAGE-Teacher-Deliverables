"""Score only the five existing readable case-023 answers, never recollect."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
import score_readable_failure as ENGINE
N,RC=ENGINE.N,ENGINE.RC
REF=HERE/'case023_reference'
PREFIX='S9_CASE023_20261115'


def targets():
    return [x for x in csv.DictReader((HERE/'SUPPLEMENT_18_EXISTING_ANSWERS.tsv').open(),delimiter='\t')
            if x['case_id']=='BIOPATH150_023']


def build(row):
    data=Path(row['answer_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==row['answer_sha256']
    answer=json.loads(data)
    scope=RC.load_scope(str(REF/'CASE_TASK_SCOPE.tsv'))['BIOPATH150_023']
    goldsteps=RC.load_gold_steps(str(REF/'reaction_gold.tsv'))
    facts=RC.align_case(scope,goldsteps['BIOPATH150_023'],answer,frozenset(),RC.build_cross_route_index(goldsteps),case_id='BIOPATH150_023')
    profile_names={str(x.get('organism_name')or'').strip().lower()for x in answer.get('organism_profiles',[])}
    files=json.loads((REF/'MANIFEST.json').read_text())['files']
    blocks=[];ids=[];kept_rows={}
    for f in files:
        name=f['file'];p=REF/name
        assert N.file_sha(p)==f['output_sha256']
        with p.open()as h:
            rd=csv.DictReader(h,delimiter='\t');fields=rd.fieldnames;rs=list(rd)
        if name.startswith('trait_'):
            rs=[x for x in rs if x.get('organism_name','').strip().lower()in profile_names]
        buf=io.StringIO();wr=csv.DictWriter(buf,fields,delimiter='\t',lineterminator='\n');wr.writeheader();wr.writerows(rs)
        blocks.append('--- FILE: '+name+' ---\n'+buf.getvalue());ids += [name,name+'#case:BIOPATH150_023']
        kept_rows[name]=len(rs)
    route=facts['route_status']
    if route=='DEVIATES':
        d1=[1,4]
        d2=[1,4]if facts['flipped_strict_nonrev']or facts['flipped_strict_rev']or facts['chain_reversal_confirmed']else[1,5]if facts['stereo_conflict']else[1,6]
    elif route=='INCOMPLETE':
        d1=[1,6];c=float(facts['coverage']);d2=[5,8]if c>=.8 else[3,6]if c>=.5 else[2,5]if c>=.2 else[1,4]
    else:
        d1=[1,10]if route=='BOUNDARY_REVIEW'else[5,10]
        d2=[1,8]if route=='BOUNDARY_REVIEW'else[5,8]
    program=dict(allowed_ranges={d:d1 if d=='D1'else d2 if d=='D2'else[1,8]if d=='D3a'else[1,10]for d in N.DIMS},
                 d3a_decision_status='JUDGE_REQUIRED',confirmed_key_failure_cap=None,source_route_status=route,
                 source_task_conformance_status=facts['task_conformance_status'],route_facts=facts,
                 note='只装配原有023题及原Gold行，未变更科学评分锚点。自动匹配/表示边界不挂起整维；逐条读原反应与配对材料判断。'+
                      'Gold不是穷尽真理，未命中不直接当错。原始enzyme_gold行是原有功能候选参照，不把宽泛/多注候选自动升格为精确底物活性证据。'+
                      '本题未新增高档KEY证据证明，按既有科学证据门D2/D3a最高8，D1/D6独立。')
    cat=dict(GOLD_SLICE=ids,SCOPE_ROW=[],E0_EVIDENCE=[])
    user='\n'.join(f'===SECTION:{k}_BEGIN===\n{v}\n===SECTION:{k}_END==='for k,v in[
        ('QUESTION',(REF/'QUESTION.txt').read_text()),('ANSWER',data.decode()),
        ('GOLD_SLICE','\n'.join(blocks)),('TASK_SCOPE',N.canonical(scope)),('REFERENCE_CATALOG',N.canonical(cat))])
    user+='\n===CURRENT_PROGRAM_JUDGEMENT===\n'+N.canonical(program)
    user+='\n性状行仅过滤为该答案organism_profiles中已推荐的物种；原有行值、identity层级、来源与mask均不改。'+\
          '材料未覆盖的菌株/具体性状如实区分未知和已核错误；已知漏答照量表计分，不退回NE。'+\
          '原Gold文件内字段定义、F2温度语义及F7测试类型按System既有条款读，不把生长温度当最适温度。'+\
          '无本轮F3逐声称额外核验，不能编造核验记录。规则引用直接用System实际[Pxxx]，不造编号。\n'
    system=N.rubric()+'\n'+N.OUTPUT
    number=next(i for i,x in enumerate(targets(),1)if x['slot']==row['slot'])
    anonymous='F4I-S9-023-'+str(number)
    ident=dict(repair_version=PREFIX,repair_item_id=anonymous,anonymous_item_id=anonymous,
               case_id='BIOPATH150_023',batch='S9_CASE023_EXISTING_ANSWERS',answer_sha256=row['answer_sha256'],
               requested_dimensions=N.DIMS,reference_extension_sha256=N.file_sha(REF/'MANIFEST.json'),
               rubric_sha256=hashlib.sha256(system.encode()).hexdigest(),
               program_and_materials_sha256=hashlib.sha256(user.encode()).hexdigest())
    ident['repair_identity_sha256']=N.digest(ident)
    user+='\n===REPAIR_IDENTITY===\n'+N.canonical(ident)
    assert dict(N.sections(user))['ANSWER'].encode()==data
    assert all(s not in user for s in ['grok-4.7','gpt-5.6-luna','deepseek-v4.1-flash','kimi/kimi-k3','qwen3.8-max'])
    body=dict(model=N.MODEL,messages=[dict(role='system',content=system),dict(role='user',content=user)],
              temperature=0,stream=True,max_tokens=65536,enable_thinking=True,
              response_format={'type':'json_object'},stream_options={'include_usage':True},enable_search=False)
    return dict(slot=row['slot'],wanted=N.DIMS,program=program,identity=ident,body=body,body_sha256=N.digest(body))


def main():
    mode=sys.argv[1]if len(sys.argv)>1 else'prepare'
    selected=targets();assert len(selected)==5
    manifest=[]
    for row in selected:
        req=build(row);out=HERE/'case023_scoring'/req['identity']['anonymous_item_id'];out.mkdir(parents=True,exist_ok=True)
        p=out/'REQUEST.json'
        if p.exists():assert N.load(p)==req
        else:p.write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n')
        manifest.append(dict(slot=row['slot'],anonymous=req['identity']['anonymous_item_id'],request_sha256=req['body_sha256'],
                             prompt_characters=sum(len(x['content'])for x in req['body']['messages']),
                             route_status=req['program']['source_route_status']))
        if mode=='run':
            ENGINE.OUT=out;ENGINE.SLOT=row['slot'];ENGINE.PREFIX=PREFIX;ENGINE.build=lambda:req
            original_argv=sys.argv;sys.argv=[__file__,'run']
            try:ENGINE.main()
            finally:sys.argv=original_argv
            result=N.load(out/('RECOVERED_RESULT.json'if(out/'RECOVERED_RESULT.json').exists()else'RESULT.json'))
            if result['status']!='OK':
                print(json.dumps(dict(event='STOP_AFTER_FIRST_NONOK',slot=row['slot'],reason=result['status'])),flush=True)
                break
    (HERE/'CASE023_REQUEST_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(mode=mode,prepared=len(manifest),requests=manifest),ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
