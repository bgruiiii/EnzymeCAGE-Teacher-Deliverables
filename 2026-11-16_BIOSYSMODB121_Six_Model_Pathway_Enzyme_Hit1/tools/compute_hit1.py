"""Offline top-one integrated-answer evaluation. See REPORT.md for definitions."""
import argparse,ast,collections,csv,hashlib,io,json,re,statistics,sys,types,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
csv.field_size_limit(1<<27)
ROOT=Path(__file__).resolve().parents[1]
EC_RE=re.compile(r'^\d+\.\d+\.\d+\.\d+$')

def read(p):
 with Path(p).open(newline='',encoding='utf-8')as h:return list(csv.DictReader(h,delimiter='\t'))
def write(p,rs):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8')as h:
  w=csv.DictWriter(h,list(rs[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rs)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pct(a,b):return 100*a/b if b else None
def clean_ec(v):
 if v is None:return ''
 return re.sub(r'^EC[\s:\-]*','',str(v).strip(),flags=re.I)
def preferred(p):
 e=p.get('enzyme')
 # The schema is a single object. A list is not a top-k candidate search.
 if not isinstance(e,dict):return {},'NONOBJECT_OR_ABSENT'
 return e,'SINGLE_PREFERRED_OBJECT'
def load_scorer(root):
 # Load ONLY the unchanged normalization/alignment definitions, not unrelated
 # trait, evidence or CSV lookup machinery from the historical scorer.
 p=root/'reference/G3_scorer/scorer.py'
 tree=ast.parse(p.read_text())
 wanted={'norm','Chem','comp_key','jac','_gold_side','_pred_side','align_steps'}
 selected=[node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))and node.name in wanted]
 assert {node.name for node in selected}==wanted
 namespace={'json':json};exec(compile(ast.Module(body=selected,type_ignores=[]),str(p),'exec'),namespace)
 s=types.SimpleNamespace(**{k:namespace[k]for k in wanted})
 s.CHEM=s.Chem();namespace['CHEM']=s.CHEM
 if s.CHEM.version=='UNAVAILABLE':raise RuntimeError('RDKit required; never substitute names silently')
 from rdkit import RDLogger
 RDLogger.DisableLog('rdApp.*')
 original=s.CHEM.canon;cache={}
 def canon(x,achiral=False):
  key=(x,achiral)
  if key not in cache:cache[key]=original(x,achiral)
  return cache[key]
 s.CHEM.canon=canon
 ref=json.loads((root/'reference/TARGET_REFERENCE.json').read_text())
 steps={}
 for case,gs in ref['steps'].items():
  steps[case]={}
  for sid,g in gs.items():
   g['preds']=set(g['preds'])
   for side in ['subs','prods']:
    for c in g[side]:c['names']=set(c['names'])
   steps[case][sid]=g
 s.GOLD=types.SimpleNamespace(steps=steps)
 s.CONTROLLED={case:set(names)for case,names in ref['controlled'].items()}
 s.reference=ref
 return s

def pred_order(p,i):
 try:return float(p.get('order'))
 except(TypeError,ValueError):return i+1

def route_hit(paths,match,ps,gold):
 for path in paths:
  if len(path)!=len(ps)or any(g not in match for g in path):continue
  # Directed gold dependencies must occur in the correct output order.
  pos={sid:pred_order(ps[match[sid]],match[sid])for sid in path}
  if any(pos[a]>=pos[b]for a,b in zip(path,path[1:])):continue
  if any(pos[p]>=pos[g]for g in path for p in gold[g]['preds']if p in pos):continue
  if len(set(pos.values()))!=len(pos):continue
  return True
 return False

def route_hit_alternatives(s,paths,ps,gold,controlled,threshold):
 # Alternatives are accepted references, not additional model guesses.
 # Align each allowed path on its own so a chemically identical step in a
 # different gold branch cannot consume the only matching prediction.
 for path in paths:
  if len(path)!=len(ps):continue
  subset={g:gold[g]for g in path}
  result=s.align_steps(subset,ps,controlled,threshold=threshold)
  mapping={x['gold_step']:x['pred_index']for x in result['matches']}
  if route_hit([path],mapping,ps,subset):return True
 return False

def standalone_mapping(s,gs,ps,matched,is_linear):
 """Fix target identity without inspecting enzyme/EC or requiring product success."""
 mapping=dict(matched);methods={g:'REACTION_EXACT'for g in mapping}
 used=set(mapping.values());unmapped=set(gs)-set(mapping)
 # Unique same-side substrate identity can bind a failed product to its target.
 # Name aliases come only from gold itself. Valid structure has authority.
 def substrate_keys(g,p):
  gold=gs[g]['subs'];pred=[x for x in(p.get('substrates')or[])if isinstance(x,dict)and s.norm(x.get('role'))in('','main')]
  pk={s.CHEM.canon(x.get('smiles'))for x in pred if s.CHEM.canon(x.get('smiles'))}
  gk={x['iso']for x in gold if x['iso']}
  if pk and gk:return pk==gk
  pn={s.norm(x.get('name'))for x in pred if x.get('name')}
  return bool(pn)and len(pred)==len(gold)and all(any(n in c['names']for n in pn)for c in gold)and all(any(n in c['names']for c in gold)for n in pn)
 candidates={g:[i for i,p in enumerate(ps)if i not in used and substrate_keys(g,p)]for g in unmapped}
 reverse=collections.Counter(i for v in candidates.values()for i in v)
 for g,idxs in candidates.items():
  if len(idxs)==1 and reverse[idxs[0]]==1:
   mapping[g]=idxs[0];methods[g]='UNIQUE_SUBSTRATE_ANCHOR';used.add(idxs[0])
 # Positional assignment is permitted only for a reference-linear, equal-length
 # answer and when EVERY already proven anchor agrees with that position.
 ordered=sorted(gs,key=lambda k:(gs[k]['order'],k))
 pi=sorted(range(len(ps)),key=lambda i:(pred_order(ps[i],i),i))
 expected=dict(zip(ordered,pi))
 if is_linear and len(ps)==len(gs)and len({pred_order(p,i)for i,p in enumerate(ps)})==len(ps)and all(expected[g]==i for g,i in mapping.items()):
  for g in ordered:
   if g not in mapping:mapping[g]=expected[g];methods[g]='LINEAR_EQUAL_LENGTH_ORDER'
 assert len(set(mapping.values()))==len(mapping)
 return mapping,methods

def calculate(root):
 s=load_scorer(root)
 idx=read(root/'inputs/ANSWERS_726.tsv');assert len(idx)==726
 formal={x['case_id']:x for x in s.reference['formal_cases']}
 scopes={x['case_id']:x for x in read(root/'inputs/TASK_SCOPES.tsv')}
 catalog=read(root/'inputs/PATH_CATALOG.tsv')
 allowed=collections.defaultdict(list)
 for x in catalog:
  if x['adoption_status']=='ADOPTED_METHOD_CONFIRMED':allowed[x['case_id']].append(x['ordered_step_ids'].split('|'))
 ecrows=collections.defaultdict(list)
 for x in s.reference['enzymes']:ecrows[(x['case_id'],x['step_occurrence_id'])].append(x)
 common={x['case_id']for x in read(root/'inputs/COMMON118.tsv')}
 cases=[];steps=[];reference=[];source_status=collections.Counter()
 for case,gs_all in sorted(s.GOLD.steps.items()):
  scope=scopes.get(case,{})
  required=set(filter(None,scope.get('required_step_ids','').split('|')))or set(gs_all)
  required &=set(gs_all)
  # Corrected 060/094 are already materialized as required-only reference tables.
  if case in ['BIOPATH150_060','BIOPATH150_094']:
   paths=[sorted(required,key=lambda g:(gs_all[g]['order'],g))];policy='USER_APPROVED_REFERENCE_REPAIR'
  elif case in allowed:
   paths=allowed[case];required={g for p in paths for g in p};policy='EXISTING_ADOPTED_MAIN_CHAIN_ALTERNATIVES'
  elif formal[case]['final_graph_status']=='LINEAR_UNIQUE':
   paths=[sorted(required,key=lambda g:(gs_all[g]['order'],g))];policy='REFERENCE_LINEAR_TASK_SCOPE'
  else:paths=[];policy='MAIN_CHAIN_SCOPE_UNRESOLVED'
  assert required and required<=set(gs_all)
  reference.append(dict(case_id=case,pathway_name=formal[case]['pathway_name'],graph_status=formal[case]['final_graph_status'],scope_policy=policy,route_evaluable=bool(paths),target_steps=len(required),allowed_path_count=len(paths),allowed_paths_json=json.dumps(paths,ensure_ascii=False),target_step_ids='|'.join(sorted(required)),background_step_ids=scope.get('background_step_ids','')))
 ref={x['case_id']:x for x in reference}
 for row in idx:
  case=row['case_id'];mod=row['model'];rr=ref[case];gs={g:s.GOLD.steps[case][g]for g in rr['target_step_ids'].split('|')};ps=[];a=None
  if row['answer_file']:
   p=root/row['answer_file'];assert sha(p)==row['answer_sha256'],(mod,case)
   try:a=json.loads(p.read_text())
   except json.JSONDecodeError:a=None
  if isinstance(a,dict):
   assert a.get('case_id')==case,(mod,case,a.get('case_id'))
   ps=[p for p in(a.get('steps')or[])if isinstance(p,dict)]
  if not isinstance(a,dict):state='NO_READABLE_ORIGINAL_ANSWER'
  elif row['coverage_status']=='READABLE_SCHEMA_FAILURE':state='READABLE_SCHEMA_FAILURE_CONTENT_RETAINED'
  else:state='READABLE_SELECTED_ANSWER'
  # Scientific content is scored whenever readable, regardless of formatting.
  source_status[state]+=1
  controlled=frozenset(s.CONTROLLED.get(case,set()))
  exact=s.align_steps(gs,ps,controlled,threshold=1.0)
  loose=s.align_steps(gs,ps,controlled,threshold=.5)
  em={x['gold_step']:x['pred_index']for x in exact['matches']}
  lm={x['gold_step']:x['pred_index']for x in loose['matches']}
  paths=json.loads(rr['allowed_paths_json'])
  linear=len(paths)==1 and(formal[case]['final_graph_status']=='LINEAR_UNIQUE'or case in ['BIOPATH150_060','BIOPATH150_094'])
  mapping,methods=standalone_mapping(s,gs,ps,em,linear)
  local=[]
  for sid,g in sorted(gs.items()):
   accepted=ecrows[(case,sid)];ecs={clean_ec(x['ec_number_normalized'])for x in accepted if EC_RE.fullmatch(clean_ec(x['ec_number_normalized']))}
   names={s.norm(x['enzyme_name'])for x in accepted if x['enzyme_name'].strip()}
   pi=mapping.get(sid);p=ps[pi]if pi is not None else {};enz,shape=preferred(p)
   ec=clean_ec(enz.get('ec_number'));name=s.norm(enz.get('name'))
   ec_order_hit=bool(ecs)and bool(ec)and ec in ecs
   anchored=methods.get(sid)in ('REACTION_EXACT','UNIQUE_SUBSTRATE_ANCHOR')
   ec_hit=ec_order_hit and anchored
   name_hit=bool(name)and name in names and anchored
   same_pair=bool(ecs)and anchored and any(name and name==s.norm(x['enzyme_name'])and ec and ec==clean_ec(x['ec_number_normalized'])for x in accepted)
   # Joint metric takes the enzyme attached to the exact reaction, not a
   # separately chosen object. Mapping above uses the same exact match first.
   eh=bool(sid in em and ec_hit)
   status=('NO_REFERENCE_COMPLETE_EC'if not ecs else'NO_OR_UNALIGNED_RECOMMENDATION'if pi is None else'ORDER_ONLY_MAPPING_SENSITIVITY'if not anchored else'NO_COMPLETE_PREDICTED_EC'if not EC_RE.fullmatch(ec)else'EC_HIT'if ec_hit else'EC_NONMATCH')
   out=dict(model=mod,case_id=case,gold_step_id=sid,gold_reaction_id=sid.rsplit('__',1)[-1],scope_evaluable=rr['route_evaluable'],gold_order=g['order'],reaction_hit1_strict=int(sid in em),reaction_hit1_frozen05=int(sid in lm),pred_index=pi if pi is not None else '',pred_step_id=p.get('step_id',''),target_binding_method=methods.get(sid,'UNRESOLVED_OR_MISSING'),pred_enzyme_name=enz.get('name')or'',pred_ec=ec,gold_accepted_complete_ecs='|'.join(sorted(ecs)),gold_accepted_names='|'.join(sorted(names)),ec_reference_scoreable=int(bool(ecs)),enzyme_ec_hit1=int(ec_hit),enzyme_ec_hit1_order_sensitivity=int(ec_order_hit),enzyme_name_hit1=int(name_hit),enzyme_name_ec_same_record_hit1=int(same_pair),reaction_and_enzyme_ec_hit1=int(eh),enzyme_ec_hit_with_reaction_miss=int(ec_hit and sid not in em),ec_status=status,answer_sha256=row['answer_sha256'],answer_file=row['answer_file'])
   local.append(out);steps.append(out)
  n=len(gs);ecden=sum(x['ec_reference_scoreable']for x in local);ech=sum(x['enzyme_ec_hit1']for x in local)
  cases.append(dict(model=mod,case_id=case,pathway_name=rr['pathway_name'],source_state=state,answer_source_version=row['answer_source_version'],answer_sha256=row['answer_sha256'],answer_file=row['answer_file'],scope_policy=rr['scope_policy'],route_evaluable=rr['route_evaluable'],common118=case in common,n_gold_target_steps=n,n_predicted_steps=len(ps),pathway_hit1_strict=int(route_hit_alternatives(s,paths,ps,gs,controlled,1.0))if paths else '',pathway_hit1_frozen05=int(route_hit_alternatives(s,paths,ps,gs,controlled,.5))if paths else '',reaction_hits_strict=len(em),reaction_hits_frozen05=len(lm),reaction_micro_component_pct=pct(len(em),n),enzyme_ec_scoreable_targets=ecden,enzyme_ec_hits=ech,enzyme_ec_order_sensitivity_hits=sum(x['enzyme_ec_hit1_order_sensitivity']for x in local),enzyme_ec_component_pct=pct(ech,ecden),enzyme_name_hits=sum(x['enzyme_name_hit1']for x in local),enzyme_pair_hits=sum(x['enzyme_name_ec_same_record_hit1']for x in local),joint_reaction_enzyme_ec_hits=sum(x['reaction_and_enzyme_ec_hit1']for x in local),enzyme_ec_hits_reaction_miss=sum(x['enzyme_ec_hit_with_reaction_miss']for x in local),binding_unresolved=sum(x['target_binding_method']not in ('REACTION_EXACT','UNIQUE_SUBSTRATE_ANCHOR')for x in local),predicted_enzyme_objects=sum(isinstance(p.get('enzyme'),dict)for p in ps),predicted_trait_profiles=len((a or{}).get('organism_profiles')or[])))
 summaries=[]
 for cohort in ['ALL121_SCOPED120','COMMON118_SCOPED117']:
  for mod in sorted({x['model']for x in cases}):
   allc=[x for x in cases if x['model']==mod and(cohort.startswith('ALL')or x['common118'])]
   cc=[x for x in allc if x['route_evaluable']]
   selected={x['case_id']for x in cc};ss=[x for x in steps if x['model']==mod and x['case_id']in selected]
   n=sum(x['n_gold_target_steps']for x in cc);ecden=sum(x['enzyme_ec_scoreable_targets']for x in cc)
   ecbind=sum(x['ec_reference_scoreable']and x['target_binding_method']in ('REACTION_EXACT','UNIQUE_SUBSTRATE_ANCHOR')for x in ss)
   h=sum(x['pathway_hit1_strict']for x in cc);rh=sum(x['reaction_hits_strict']for x in cc);eh=sum(x['enzyme_ec_hits']for x in cc)
   summaries.append(dict(cohort=cohort,model=mod,case_positions=len(allc),scope_evaluable_cases=len(cc),scope_held_cases=len(allc)-len(cc),readable_answers=sum(x['source_state']!='NO_READABLE_ORIGINAL_ANSWER'for x in allc),pathway_hit1_hits=h,pathway_hit1_denominator=len(cc),pathway_hit1_pct=pct(h,len(cc)),reaction_hit1_hits=rh,reaction_hit1_denominator=n,reaction_hit1_micro_pct=pct(rh,n),reaction_hit1_macro_pct=statistics.mean(x['reaction_micro_component_pct']for x in cc),enzyme_ec_hit1_hits=eh,enzyme_ec_hit1_denominator=ecden,enzyme_ec_hit1_pct=pct(eh,ecden),enzyme_ec_hit1_order_sensitivity_pct=pct(sum(x['enzyme_ec_order_sensitivity_hits']for x in cc),ecden),enzyme_ec_reference_targets_without_complete_ec=n-ecden,enzyme_ec_target_binding_coverage_pct=pct(ecbind,ecden),enzyme_name_hit1_hits=sum(x['enzyme_name_hits']for x in cc),enzyme_name_hit1_pct=pct(sum(x['enzyme_name_hits']for x in cc),n),enzyme_name_ec_pair_hit1_pct=pct(sum(x['enzyme_pair_hits']for x in cc),ecden),joint_reaction_enzyme_ec_hit1_pct=pct(sum(x['joint_reaction_enzyme_ec_hits']for x in cc),ecden),enzyme_ec_hits_with_reaction_miss=sum(x['enzyme_ec_hits_reaction_miss']for x in cc),frozen05_pathway_hit1_pct=pct(sum(x['pathway_hit1_frozen05']for x in cc),len(cc)),frozen05_reaction_hit1_micro_pct=pct(sum(x['reaction_hits_frozen05']for x in cc),n),unresolved_or_missing_target_bindings=sum(x['binding_unresolved']for x in cc)))
 result=root/'results'
 write(result/'SIX_MODEL_HIT1_SUMMARY.tsv',summaries)
 write(result/'PER_CASE_726.tsv',cases)
 write(result/'PER_GOLD_STEP.tsv',steps)
 write(result/'REFERENCE_SCOPE_121.tsv',reference)
 coverage=[]
 for mod in sorted({x['model']for x in cases}):
  group=[x for x in cases if x['model']==mod]
  coverage.append(dict(model=mod,positions=121,readable_original_answers=sum(x['source_state']!='NO_READABLE_ORIGINAL_ANSWER'for x in group),readable_schema_failure=sum(x['source_state']=='READABLE_SCHEMA_FAILURE_CONTENT_RETAINED'for x in group),no_readable_original=sum(x['source_state']=='NO_READABLE_ORIGINAL_ANSWER'for x in group),total_predicted_steps=sum(x['n_predicted_steps']for x in group),total_preferred_enzyme_objects=sum(x['predicted_enzyme_objects']for x in group),answer_files_index='inputs/ANSWERS_726.tsv'))
 write(result/'OUTPUT_COVERAGE.tsv',coverage)
 checks=dict(PASS=True,positions=len(cases),unique_positions=len({(x['model'],x['case_id'])for x in cases}),selected_raw_answers=sum(bool(x['answer_file'])for x in idx),reference_cases=len(reference),scope_held_cases=[x['case_id']for x in reference if not x['route_evaluable']],step_rows=len(steps),rdkit_version=s.CHEM.version,frozen_scorer_sha256=sha(root/'reference/G3_scorer/scorer.py'),api_calls=0,no_hits_from_empty_ec=True,wrong_reaction_correct_ec_examples=sum(x['enzyme_ec_hit_with_reaction_miss']for x in steps))
 assert len(cases)==len({(x['model'],x['case_id'])for x in cases})==726
 assert len(reference)==121 and len(common)==118
 assert all(x['pathway_hit1_denominator']==(120 if x['cohort'].startswith('ALL')else 117)for x in summaries)
 assert all(not x['enzyme_ec_hit1']or x['pred_ec']and x['pred_ec']in x['gold_accepted_complete_ecs'].split('|')for x in steps)
 assert all(x['enzyme_ec_hit1']<=x['ec_reference_scoreable']for x in steps)
 assert all(not x['reaction_and_enzyme_ec_hit1']or x['reaction_hit1_strict']and x['enzyme_ec_hit1']for x in steps)
 (result/'VALIDATION.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 try:workbook(root,summaries,cases,steps,coverage,reference)
 except ImportError:print('openpyxl unavailable: TSV complete; Excel skipped',file=sys.stderr)
 print(json.dumps(checks,ensure_ascii=False));print(json.dumps([x for x in summaries if x['cohort'].startswith('ALL')],ensure_ascii=False))

def workbook(root,*groups):
 from openpyxl import Workbook
 from openpyxl.styles import Font,PatternFill,Alignment
 from openpyxl.utils import get_column_letter
 wb=Workbook();wb.remove(wb.active)
 for name,rs in zip(['六模型Hit1','逐题726','逐步Gold目标','输出覆盖','参考范围'],groups):
  ws=wb.create_sheet(name);cols=list(rs[0]);ws.append(cols)
  for r in rs:ws.append([r[k]for k in cols])
  ws.freeze_panes='C2';ws.auto_filter.ref=ws.dimensions
  for c in ws[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='24476A')
  for i,k in enumerate(cols,1):ws.column_dimensions[get_column_letter(i)].width=28 if k not in ['pathway_name','gold_step_id']else 48
  for row in ws.iter_rows(min_row=2):
   for c in row:
    if isinstance(c.value,float):c.number_format='0.0000'
 target=root/'六模型路径与酶_Hit1.xlsx'
 wb.save(target)
 # Fix document/ZIP metadata so offline recomputation preserves SHA256SUMS.
 original=target.read_bytes();buf=io.BytesIO()
 with zipfile.ZipFile(io.BytesIO(original))as zi,zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED)as zo:
  for entry in zi.infolist():
   data=zi.read(entry.filename)
   if entry.filename=='docProps/core.xml':
    data=re.sub(rb'(<dcterms:(?:created|modified)[^>]*>)[^<]+',rb'\g<1>2026-11-16T00:00:00Z',data)
   entry.date_time=(2026,11,16,0,0,0);entry.compress_type=zipfile.ZIP_DEFLATED
   zo.writestr(entry,data)
 target.write_bytes(buf.getvalue())

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT);args=parser.parse_args();calculate(args.root.resolve())
if __name__=='__main__':main()
