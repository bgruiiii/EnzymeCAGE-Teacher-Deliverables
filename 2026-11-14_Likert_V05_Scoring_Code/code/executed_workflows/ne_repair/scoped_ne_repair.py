"""Input-only path-scope repair. Reuses S8 rubric, score validator and merger.

No new route inference, score thresholds, evidence acquisition or API calls.
"""
import copy
import csv
import hashlib
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
S8=HERE.parent
sys.path.insert(0,str(S8))
import ne_repair as BASE

VERSION='LIKERT_V05_S8_INPUT_PATH_SCOPE_R1_20261114'
CATALOG=BASE.S6/'input/release/PATH_CATALOG_03D.tsv'
STEPS=BASE.S6/'input/release/PATH_STEPS_03D.tsv'
validate=BASE.validate
merge_validated=BASE.merge_validated


@lru_cache(maxsize=1)
def catalogs():
    return (list(csv.DictReader(CATALOG.open(),delimiter='\t')),
            list(csv.DictReader(STEPS.open(),delimiter='\t')))


def build(slot,wanted):
    request=BASE.build(slot,wanted)
    ctx,_,_,_=BASE.item_for(slot)
    body=request['body']
    user=body['messages'][1]['content']
    material,tail=user.split('\n===CURRENT_PROGRAM_JUDGEMENT===\n',1)
    program_text,_=tail.split('\n===REPAIR_IDENTITY===\n',1)
    program=json.loads(program_text)
    task=dict(BASE.sections(material))['TASK_SCOPE']
    scope=json.loads(re.search(r'\{.*\}',task,re.S)[0])
    if scope.get('graph_status')=='BRANCHED_DAG':
        cats,steps=catalogs()
        paths=[copy.deepcopy(x)for x in cats if x['case_id']==ctx['case_id']and x['adoption_status']=='ADOPTED_METHOD_CONFIRMED']
        pathids={x['path_id']for x in paths}
        pathsteps=[copy.deepcopy(x)for x in steps if x['case_id']==ctx['case_id']and x['path_id']in pathids]
        for path in paths:
            listed=sorted([x for x in pathsteps if x['path_id']==path['path_id']],key=lambda x:int(x['order_index']))
            assert len(listed)==int(path['n_steps'])
            assert [x['gold_step_id']for x in listed]==path['ordered_step_ids'].split('|')
        # Relabel the old graph union as background; never pretend it is a
        # selected chain. Keep its facts, order and evidence unchanged.
        for key in ['required_step_ids','n_required','gold_terminal_step_ids']:
            if key in scope:scope['graph_reference_'+key]=scope.pop(key)
        scope['required_scope_source']='D-M01_ONE_ADOPTED_MAIN_CHAIN'
        scope['scope_decision_ref']='D-M01;existing PATH_CATALOG_03D and PATH_STEPS_03D'
        replacement='题面与全图参考元数据：graph_reference字段只供定位，不是答卷必须完成全部分支。\n'+BASE.canonical(scope)
        material=material.replace('===SECTION:TASK_SCOPE_BEGIN===\n'+task+'\n===SECTION:TASK_SCOPE_END===',
                                  '===SECTION:TASK_SCOPE_BEGIN===\n'+replacement+'\n===SECTION:TASK_SCOPE_END===',1)
        target=program.pop('target_fact_contract')
        program['full_graph_reference_observations']=target
        program['graph_observations_are_not_required_chain_denominator']=True
        program['main_chain_scope']=dict(case_id=ctx['case_id'],
            catalog_sha256=BASE.file_sha(CATALOG),steps_sha256=BASE.file_sha(STEPS),
            source_selected_path_id=target.get('consumer_identity',{}).get('current_path_id'),
            adopted_paths=paths,adopted_path_steps=pathsteps,
            scope_rule='D-M01: assess one adopted main chain; unselected branches do not count as omissions')
        material+='\n===SECTION:MAIN_CHAIN_SCOPE_BEGIN===\n'+BASE.canonical(program['main_chain_scope'])+'\n===SECTION:MAIN_CHAIN_SCOPE_END===' 
        material+='\n评分范围说明：按上面已认可主链及答案判断本次目标维度，在已有理由里简记所评主链。全图MISSING/未命中不能直接作为所评主链漏答；未选分支不扣缺步。不自建路线，不因多条认可链而自动NE；确实缺少可判范围时保留具体缺口。\n'
    user_material=material+'\n===CURRENT_PROGRAM_JUDGEMENT===\n'+BASE.canonical(program)
    ident=copy.deepcopy(request['identity'])
    ident.pop('repair_identity_sha256')
    ident['repair_version']=VERSION
    ident['program_and_materials_sha256']=hashlib.sha256(user_material.encode()).hexdigest()
    ident['repair_identity_sha256']=BASE.digest(ident)
    body['messages'][1]['content']=user_material+'\n===REPAIR_IDENTITY===\n'+BASE.canonical(ident)
    request.update(identity=ident,program=program,body_sha256=BASE.digest(body))
    return request


def prepare():
    plans=list(csv.DictReader((S8/'AFFECTED_NE_TARGETS.tsv').open(),delimiter='\t'))
    pilot=[json.loads(x)for x in (S8/'execution/work/RESULTS.jsonl').read_text().splitlines()]
    done={x['slot']:x for x in pilot if x['status']=='OK'}
    assert set(done)==set(BASE.PILOT)
    rows=[]
    for row in plans:
        if row['slot']in done:continue
        ds=row['requested_dimensions'].split(',')
        assert all(BASE.dimensions(BASE.source_records()[row['slot']])[d]['score_status']=='NE'for d in ds)
        rows.append(dict(slot=row['slot'],requested_dimensions=','.join(ds),reason='ONLY_PREVIOUSLY_AFFECTED_NE;PILOT_ALREADY_PAID_EXCLUDED'))
    assert len(rows)==293 and sum(len(x['requested_dimensions'].split(','))for x in rows)==546
    with(HERE/'REMAINING_NE_TARGETS.tsv').open('w')as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    count=0
    manifest=[]
    for row in rows:
        req=build(row['slot'],row['requested_dimensions'].split(','))
        branch='main_chain_scope'in req['program']
        count+=branch
        manifest.append(dict(slot=row['slot'],wanted=req['wanted'],request_sha256=req['body_sha256'],
                             identity_sha256=req['identity']['repair_identity_sha256'],branch_scope_attached=branch))
    record=dict(repair_version=VERSION,rubric_unchanged_from_S8=True,
        rubric_sha256=hashlib.sha256(BASE.rubric().encode()).hexdigest(),
        source_module_sha256=BASE.file_sha(S8/'ne_repair.py'),
        catalog_sha256=BASE.file_sha(CATALOG),path_steps_sha256=BASE.file_sha(STEPS),
        pilot_result_sha256=BASE.file_sha(S8/'execution/work/RESULTS.jsonl'),
        baseline_binding=BASE.load(S8/'REPAIR_INPUT_BINDING.json'),
        pilot_rebought=False,remaining_answer_targets=len(rows),remaining_NE_dimensions=546,
        branch_answer_targets=count,requests=manifest,new_api_calls=0)
    (HERE/'INPUT_SCOPE_FIX_BINDING.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    return record


if __name__=='__main__':
    r=prepare()
    print(json.dumps({k:v for k,v in r.items()if k not in ['requests','baseline_binding']},ensure_ascii=False))
