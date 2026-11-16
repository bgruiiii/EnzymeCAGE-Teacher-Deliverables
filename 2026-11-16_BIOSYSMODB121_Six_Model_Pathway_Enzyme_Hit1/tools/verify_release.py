"""Independent arithmetic, raw-source, linkage and edge-case verification."""
import collections,csv,hashlib,json,re,sys
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]

def rows(name):
 with(ROOT/name).open(newline='')as h:return list(csv.DictReader(h,delimiter='\t'))
def require_close(value,n,d):
 assert abs(Decimal(value)-Decimal(n)*100/Decimal(d))<Decimal('1e-10'),(value,n,d)
def main():
 manifest=ROOT/'SHA256SUMS'
 if manifest.exists():
  for line in manifest.read_text().splitlines():
   want,rel=line.split('  ',1);p=(ROOT/rel).resolve();assert p.is_relative_to(ROOT)
   assert hashlib.sha256(p.read_bytes()).hexdigest()==want,rel
 idx=rows('inputs/ANSWERS_726.tsv');cc=rows('results/PER_CASE_726.tsv');ss=rows('results/PER_GOLD_STEP.tsv');summary=rows('results/SIX_MODEL_HIT1_SUMMARY.tsv')
 assert len(idx)==len(cc)==len({(x['model'],x['case_id'])for x in cc})==726
 assert set(collections.Counter(x['model']for x in cc).values())=={121}
 for x in idx:
  p=ROOT/x['answer_file'];assert p.is_file()
  assert hashlib.sha256(p.read_bytes()).hexdigest()==x['answer_sha256']
 for x in ss:
  if x['enzyme_ec_hit1']=='1':
   assert x['ec_reference_scoreable']=='1'
   assert re.fullmatch(r'\d+\.\d+\.\d+\.\d+',x['pred_ec'])
   assert x['pred_ec']in x['gold_accepted_complete_ecs'].split('|')
   assert x['target_binding_method']in('REACTION_EXACT','UNIQUE_SUBSTRATE_ANCHOR')
  if not x['pred_ec']:assert x['enzyme_ec_hit1']=='0'
  assert int(x['reaction_and_enzyme_ec_hit1'])==int(x['reaction_hit1_strict'])*int(x['enzyme_ec_hit1'])
 for m in summary:
  chosen=[x for x in cc if x['model']==m['model']and x['route_evaluable']=='True'and(m['cohort'].startswith('ALL')or x['common118']=='True')]
  assert len(chosen)==int(m['pathway_hit1_denominator'])
  assert sum(int(x['pathway_hit1_strict'])for x in chosen)==int(m['pathway_hit1_hits'])
  n=sum(int(x['n_gold_target_steps'])for x in chosen);hits=sum(int(x['reaction_hits_strict'])for x in chosen)
  assert n==int(m['reaction_hit1_denominator'])and hits==int(m['reaction_hit1_hits'])
  en=sum(int(x['enzyme_ec_scoreable_targets'])for x in chosen);eh=sum(int(x['enzyme_ec_hits'])for x in chosen)
  assert en==int(m['enzyme_ec_hit1_denominator'])and eh==int(m['enzyme_ec_hit1_hits'])
  for field,a,b in [('pathway_hit1_pct',int(m['pathway_hit1_hits']),len(chosen)),('reaction_hit1_micro_pct',hits,n),('enzyme_ec_hit1_pct',eh,en)]:require_close(m[field],a,b)
 assert len([x for x in ss if x['enzyme_ec_hit_with_reaction_miss']=='1'])>0
 # Behavioral probes of the actual extracted frozen alignment definitions.
 sys.path.insert(0,str(ROOT/'tools'));import compute_hit1 as c
 s=c.load_scorer(ROOT)
 def comp(smiles,name):return dict(iso=s.CHEM.canon(smiles),achiral=None,names={name})
 gold={'T1':dict(order=1,preds=set(),subs=[comp('CCO','ethanol')],prods=[comp('CC=O','acetaldehyde')])}
 wrong=dict(order=1,substrates=[dict(smiles='CCO',name='ethanol',role='main')],products=[dict(smiles='CC(=O)O',name='acetate',role='main')],enzyme=dict(ec_number='1.1.1.1'))
 assert s.align_steps(gold,[wrong],threshold=1.0)['matches']==[]
 mapping,method=c.standalone_mapping(s,gold,[wrong],{},True)
 assert mapping=={'T1':0}and method['T1']=='UNIQUE_SUBSTRATE_ANCHOR'
 rev=dict(substrates=[dict(smiles='CC=O',role='main')],products=[dict(smiles='CCO',role='main')])
 assert not s.align_steps(gold,[rev],threshold=1.0)['matches']
 repeat=dict(substrates=[dict(name='ethanol',role='main')],products=[dict(name='acetaldehyde',role='main')])
 assert not s.align_steps(gold,[repeat],frozenset({'ethanol','acetaldehyde'}),threshold=1.0)['matches']
 correct=dict(substrates=[dict(smiles='CCO',role='main')],products=[dict(smiles='CC=O',role='main')])
 duplicate={'T1':gold['T1'],'T2':dict(gold['T1'],order=2)}
 assert len(s.align_steps(duplicate,[correct],threshold=1.0)['matches'])==1
 good=dict(correct,order=1)
 assert c.route_hit([['T1']],{'T1':0},[good],gold)
 assert not c.route_hit([['T1']],{'T1':0},[good,good],gold)
 # An equivalent reference branch must not lose its only prediction to
 # another branch's stable-id tie-break.
 assert c.route_hit_alternatives(s,[['T2']],[good],duplicate,frozenset(),1.0)
 # Only valid local links are checked. The parent historical release is a
 # sibling after publication and is intentionally allowed outside this bundle.
 nlinks=0
 for p in ROOT.rglob('*.md'):
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('http:','https:','#')):continue
   dest=(p.parent/unquote(target.split('#')[0])).resolve()
   if dest.is_relative_to(ROOT):assert dest.exists(),(p.name,target)
   nlinks+=1
 for p in ROOT.rglob('*'):
  if p.is_file()and p.suffix in {'.py','.tsv','.json','.md','.txt'}:
   text=p.read_text()
   assert not re.search(r'/home/[a-zA-Z0-9_.-]+/',text),p.relative_to(ROOT)
   assert not re.search(r'(?i)(?:sk-[a-z0-9_-]{20,}|Bearer\s+[a-z0-9._-]{24,})',text),p.relative_to(ROOT)
 print(json.dumps(dict(PASS=True,positions=726,step_rows=len(ss),summary_rows=len(summary),raw_file_sha_verified=len(idx),behavioral_probes=7,links_verified=nlinks,api_calls=0),ensure_ascii=False))
if __name__=='__main__':main()
