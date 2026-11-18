"""Build isolated references for the two explicitly user-approved scopes."""
import copy
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

csv.field_size_limit(1 << 27)

HERE=Path(__file__).resolve().parent
W=HERE.parent
R=W.parent
S9=W/'S9_121X6_COVERAGE_COMPLETION_20261115'
G=R/'LIKERT_V04_FULL_SCORING_20261029/F1_PROGRAM_TABLES/work/adapter_stage/G1_gold'
DB=R/'00_Authority_Teacher_Plan/BIOSYSMOdb v2'
ORDER={'BIOPATH150_060':['BSY-r01724','BSY-r01723','BSY-r02822','BSY-r01726'],
       'BIOPATH150_094':['BSY-r02482','BSY-r03042']}
PINS={}


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p,delimiter='\t'):
    p=Path(p);PINS[str(p)]=sha(p)
    with p.open(encoding='utf-8-sig',newline='')as f:
        rd=csv.DictReader(f,delimiter=delimiter);return list(rd.fieldnames),list(rd)


def put(p,obj):
    Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def write(p,fields,rows):
    with Path(p).open('w',newline='')as f:
        wr=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n');wr.writeheader();wr.writerows(rows)


def main():
    decisions=json.loads((S9/'CASE_SCOPE_USER_DECISIONS.json').read_text())
    assert decisions['BIOPATH150_060']['status']=='USER_APPROVED_FOUR_STEP_SCOPE'
    assert decisions['BIOPATH150_094']['status']=='USER_APPROVED_TWO_STEP_SCOPE'
    for d in decisions.values():PINS[d['decision_document']]=sha(d['decision_document'])
    _,coverage=read(S9/'CURRENT_SCORES_ALL_726.tsv')
    targets=[x for x in coverage if x['case_id']in ORDER]
    assert len(targets)==12 and all(x['total_status']=='UNSCORED'for x in targets)
    requested_names=defaultdict(set)
    for t in targets:
        p=Path(t['answer_path']);assert sha(p)==t['answer_sha256'];PINS[str(p)]=sha(p)
        answer=json.loads(p.read_text());assert answer['case_id']==t['case_id']
        requested_names[t['case_id']].update(str(x.get('organism_name')or'').strip().lower()for x in answer.get('organism_profiles',[]))
    names=['case_root_identity.tsv','formal_cases.tsv','reaction_gold.tsv','enzyme_gold.tsv',
           'organism_gold.tsv','trait_gold.tsv','trait_scoreability_mask.tsv',
           'trait_subfield_scoreability_mask.tsv','verified_species_name_crosswalk.tsv']
    data={name:read(G/name)for name in names}
    _,rawreactions=read(DB/'BIOSYSMOdb_Reactions_v1.0.csv',',')
    reactions={x['Reaction unique ID']:x for x in rawreactions}
    _,rawenzymes=read(DB/'BIOSYSMOdb_Enzymes_v1.0.csv',',')
    _,rawcompounds=read(DB/'BIOSYSMOdb_Compounds_chemical_info_v1.0.csv',',')
    compounds={x['BIOSYSMO ID']:x for x in rawcompounds}
    scope_fields,_=read(R/'LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK/CASE_TASK_SCOPE_120.tsv')
    approvals=[]
    for case,required in ORDER.items():
        out=HERE/'references'/case;out.mkdir(parents=True,exist_ok=True)
        selected={name:[copy.deepcopy(x)for x in rows if x.get('case_id')==case]if 'case_id'in fields else copy.deepcopy(rows)
                  for name,(fields,rows)in data.items()}
        original=copy.deepcopy(selected)
        path=selected['formal_cases.tsv'][0]['pathway_id']
        steps={x['reaction_id']:x['step_occurrence_id']for x in selected['reaction_gold.tsv']}
        if case=='BIOPATH150_060':
            steps['BSY-r01726']=case+'__S04__BSY-r01726'
            # Intrinsic reaction/enzyme/step-organism annotations already exist
            # in frozen G1 for this same reaction under case055. Reuse them
            # with explicit source locators, never its pathway-complete claim.
            for name in ['reaction_gold.tsv','enzyme_gold.tsv','organism_gold.tsv']:
                extra=[copy.deepcopy(x)for x in data[name][1]if x.get('case_id')=='BIOPATH150_055'and x.get('reaction_id')=='BSY-r01726']
                assert extra,name
                for x in extra:
                    assert name!='organism_gold.tsv'or x['scope']=='STEP'
                    x.update(case_id=case,pathway_id=path,step_occurrence_id=steps['BSY-r01726'])
                selected[name].extend(extra)
            raw=next(x for x in rawenzymes if x['Enzyme-ID']=='BSY-e00862')
            assert 'BSY-r01726'in raw['Reactions catalyzed'].split('|')and'4.1.1.77'in raw['EC number']
            assert reactions['BSY-r01726']['Substrate 1 ID Biosysmo']=='BSY-c15577'
            assert reactions['BSY-r01726']['Product 1 ID Biosysmo']=='BSY-c16542'
            terminal='BSY-c16542'
        else:
            terminal='BSY-c01562'
            # Restore the reversible background entry using actual source
            # sides; it is not a required continuation of the androsterone path.
            raw=reactions['BSY-r00968']
            subs={raw[f'Substrate {i} ID Biosysmo']for i in range(1,5)}-{''}
            prods={raw[f'Product {i} ID Biosysmo']for i in range(1,5)}-{''}
            for x in selected['reaction_gold.tsv']:
                if x['reaction_id']!='BSY-r00968':continue
                cid=x['compound_id'];assert(cid in subs)!=(cid in prods)
                side='SUBSTRATE'if cid in subs else'PRODUCT'
                x.update(participant_side=side,participant_source_side=side,gold_orientation='SUBSTRATE_TO_PRODUCT',
                         arrow_class='reversible',predecessor_step_ids='',successor_step_ids='',topological_level='0')
                if x['role_label']in ['MAIN_SUBSTRATE','MAIN_PRODUCT']:
                    x['role_label']='MAIN_SUBSTRATE'if side=='SUBSTRATE'else'MAIN_PRODUCT'
            selected['formal_cases.tsv'][0]['final_graph_status']='BRANCHED_DAG'
        required_ids=[steps[r]for r in required]
        for x in selected['reaction_gold.tsv']:
            if x['reaction_id']not in required:continue
            n=required.index(x['reaction_id'])
            x.update(linear_display_order=str(n+1),topological_level=str(n),branch_id='1',
                     predecessor_step_ids=required_ids[n-1]if n else'',
                     successor_step_ids=required_ids[n+1]if n+1<len(required_ids)else'')
        if case=='BIOPATH150_060':
            selected['formal_cases.tsv'][0]['ordered_step_count']='4'
        root=selected['case_root_identity.tsv'][0]
        cmp=compounds[terminal]
        root.update(terminal_compound_ids=terminal,terminal_compound_names=cmp['cmpdname'],
                    terminal_isosmiles=cmp['isosmiles'],terminal_canonicalsmiles=cmp['canonicalsmiles'])
        # Preserve old pathway-level annotations separately. They do not
        # automatically certify the corrected four-step/two-step task scope.
        annotations=[x for x in selected['organism_gold.tsv']if x['scope']=='PATHWAY_COMPLETE']
        selected['organism_gold.tsv']=[x for x in selected['organism_gold.tsv']if x['scope']!='PATHWAY_COMPLETE']
        write(out/'source_pathway_annotations.tsv',data['organism_gold.tsv'][0],annotations)
        # Frozen same-species trait observations may be reused across cases,
        # preserving strain/measurement/source fields and the original case.
        # Only organisms actually recommended in the six immutable answers
        # are added. This is evaluator-side reference lookup, not a claim
        # that the recommended strain has every representative observation.
        for name in ['trait_gold.tsv','trait_scoreability_mask.tsv','trait_subfield_scoreability_mask.tsv']:
            known={json.dumps({k:v for k,v in x.items()if k!='case_id'},sort_keys=True)for x in selected[name]}
            for source in data[name][1]:
                if source.get('organism_name','').strip().lower()not in requested_names[case]:continue
                signature=json.dumps({k:v for k,v in source.items()if k!='case_id'},sort_keys=True)
                if signature in known:continue
                known.add(signature);x=copy.deepcopy(source);x['source_reference_case_id']=x['case_id'];x['case_id']=case;selected[name].append(x)
        manifests=[]
        for name in names:
            fields=list(data[name][0])
            if any('source_reference_case_id'in x for x in selected[name]):fields.append('source_reference_case_id')
            write(out/name,fields,selected[name])
            manifests.append(dict(file=name,sha256=sha(out/name),rows=len(selected[name]),source=str(G/name),source_sha256=PINS[str(G/name)]))
        rawfields=list(rawreactions[0])
        source_rxns=[reactions[x]for x in required+(['BSY-r00968']if case=='BIOPATH150_094'else[])]
        write(out/'source_reaction_records.tsv',rawfields,source_rxns)
        question=R/f'25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26/G2_questions/rendered_messages/{case}.json'
        PINS[str(question)]=sha(question);q=json.loads(question.read_text());meta=q['case_metadata']
        (out/'QUESTION.txt').write_text(next(x['content']for x in reversed(q['messages'])if x['role']=='user'))
        background=[steps['BSY-r00968']]if case=='BIOPATH150_094'else[]
        scope={k:''for k in scope_fields}
        scope.update(case_id=case,pathway_id=path,pathway_name=meta['pathway_name'],route_name_question=meta['route_scope'],
            route_qualifier=meta['route_scope'],pollutant_en=meta['pollutant_name_en'],pollutant_zh=meta['pollutant_name_zh'],
            oxygen=meta['oxygen_condition']or'',graph_status='LINEAR_UNIQUE',ordered_step_count=str(len(required)+len(background)),
            n_gold_steps_total=str(len(required)+len(background)),required_step_ids='|'.join(required_ids),
            background_step_ids='|'.join(background),n_required=str(len(required)),n_background=str(len(background)),
            gold_terminal_step_ids=required_ids[-1],gold_terminal_main_products=cmp['cmpdname'],
            required_scope_source='USER_EXPLICIT_SCOPE_DECISION_20261115',
            direction_policy='USER_APPROVED_START_TO_NAMED_ENDPOINT;BACKGROUND_ENTRY_NOT_REQUIRED',
            edge_list=';'.join(a.split('__')[1]+'->'+b.split('__')[1]for a,b in zip(required_ids,required_ids[1:])),
            reference_insufficient='FALSE',route_uniqueness_validated='USER_SELECTED_EXISTING_SOURCE_ROUTE',
            content_deviation_requires_human_review='FALSE',disposition_status='USER_APPROVED_REFERENCE_REPAIR',
            notes='保留原题。060必答4步；094雄酮出发必答2步，睾酮入口仅背景。原PATHWAY_COMPLETE标签不自动证明修正范围能力；不得因背景未答扣分。')
        write(out/'CASE_TASK_SCOPE.tsv',scope_fields,[scope])
        write(out/'SCOPE_ROLES.tsv',['step_id','reaction_id','task_role','key_role'],[
            dict(step_id=sid,reaction_id=rid,task_role='REQUIRED',key_role='ENTRY'if n==0 else'TERMINAL'if n==len(required)-1 else'MAJOR')
            for n,(sid,rid)in enumerate(zip(required_ids,required))]+[
            dict(step_id=sid,reaction_id='BSY-r00968',task_role='BACKGROUND_NOT_REQUIRED',key_role='NONE')for sid in background])
        # Validate the carbon skeleton against the adopted source reaction
        # chain, using actual main-substrate/product rows, never S-number order.
        mainpairs={}
        for rid in required:
            rs=[x for x in selected['reaction_gold.tsv']if x['reaction_id']==rid]
            a={x['compound_id']for x in rs if x['role_label']=='MAIN_SUBSTRATE'}
            b={x['compound_id']for x in rs if x['role_label']=='MAIN_PRODUCT'}
            mainpairs[rid]=(a,b)
        assert all(mainpairs[a][1]&mainpairs[b][0]for a,b in zip(required,required[1:]))
        assert terminal in mainpairs[required[-1]][1]
        if background:
            rs=[x for x in selected['reaction_gold.tsv']if x['reaction_id']=='BSY-r00968']
            assert any(x['compound_id']=='BSY-c01530'and x['role_label']=='MAIN_SUBSTRATE'for x in rs)
            assert any(x['compound_id']=='BSY-c01562'and x['role_label']=='MAIN_PRODUCT'for x in rs)
        manifest=dict(case_id=case,version='S12_USER_APPROVED_REFERENCE_REPAIR_20261115',
            decision=decisions[case],files=manifests,required_reactions=required,background_reactions=['BSY-r00968']if background else[],
            source_pathway_annotations_sha256=sha(out/'source_pathway_annotations.tsv'),
            source_reaction_records_sha256=sha(out/'source_reaction_records.tsv'),
            scope_sha256=sha(out/'CASE_TASK_SCOPE.tsv'),scope_roles_sha256=sha(out/'SCOPE_ROLES.tsv'),
            question_sha256=sha(out/'QUESTION.txt'),base_source_Gold_modified=False,
            pathways_annotations_not_upgraded_to_full_route_proof=True,
            trait_reference_reuse='frozen same-species observations only; strain/source/measurement fields retained',
            transformations=['060 adds existing r01726 reaction/enzyme/STEP annotations from frozen same-reaction records',
                             '094 restores source direction of r00968 as background; only r02482/r03042 required',
                             'graph/root-terminal metadata updated; original complete-pathway annotations separated',
                             'same-species frozen trait lookup for recommended profile names'])
        put(out/'MANIFEST.json',manifest);approvals.append(dict(case_id=case,required=len(required),background=len(background),manifest_sha256=sha(out/'MANIFEST.json')))
    write(HERE/'TARGETS_12.tsv',list(targets[0]),targets)
    put(HERE/'REFERENCE_CHECKS.json',dict(PASS=True,cases=approvals,targets=12,all_original_answer_sha_verified=True,
        original_reference_sources_unchanged=all(sha(p)==s for p,s in PINS.items()),new_calls=0))
    put(HERE/'INPUT_MANIFEST.json',dict(files=[dict(path=p,sha256=s)for p,s in sorted(PINS.items())]))
    assert all(sha(p)==s for p,s in PINS.items())
    print(json.dumps(dict(prepared_cases=approvals,targets=12,paid_calls=0),ensure_ascii=False))


if __name__=='__main__':main()
