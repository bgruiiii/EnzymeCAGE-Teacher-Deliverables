"""Offline integrity and coverage verification. Does not launch historical code."""
import ast,csv,hashlib,json,re
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
 with p.open(newline='')as h:return list(csv.DictReader(h,delimiter='\t'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 for line in(ROOT/'SHA256SUMS').read_text().splitlines():
  want,rel=line.split('  ',1);p=(ROOT/rel).resolve();assert p.is_relative_to(ROOT)and p.is_file(),rel;assert sha(p)==want,rel
 source=rows(ROOT/'provenance/SOURCE_MANIFEST.tsv')
 for x in source:assert x['export_sha256']==x['source_sha256']==sha(ROOT/x['export_path']),x['export_path']
 cases=[json.loads(x)for x in(ROOT/'questions/main_cases.jsonl').read_text().splitlines()]
 assert len(cases)==len({x['case_id']for x in cases})==121
 for c in cases:
  q=json.loads((ROOT/'questions/original_messages'/f"{c['case_id']}.json").read_text())
  assert q['case_id']==c['case_id']and len(q['messages'])==1 and q['messages'][0]['role']=='user'
 assert len(rows(ROOT/'questions/POLLUTANT_INDEX_121.tsv'))==121
 refs=rows(ROOT/'reference/original_task_contracts/CURRENT_ROUTE_LOCKED_SCOPE_121.tsv');assert len(refs)==len({x['case_id']for x in refs})==121
 gold=rows(ROOT/'reference/gold_121/reaction_gold.tsv');assert len({x['case_id']for x in gold})==121
 answers=rows(ROOT/'existing_outputs/ANSWER_INDEX_PORTABLE_726.tsv')
 assert len(answers)==len({(x['model'],x['case_id'])for x in answers})==726
 for x in answers:assert sha(ROOT/x['answer_file'])==x['answer_sha256'],(x['model'],x['case_id'])
 scores=rows(ROOT/'existing_outputs/likert_results/LIKERT_V05_SCORES_726.tsv');assert len(scores)==726
 assert sum(x['likert_status']=='COMPARABLE'for x in scores)==723
 ratings=[json.loads(x)for x in(ROOT/'existing_outputs/likert_results/LIKERT_V05_RATINGS_723.jsonl').read_text().splitlines()];assert len(ratings)==723
 assert sum(v['score_status']=='NE'for r in ratings for v in r['dimensions'].values())==0
 assert len(rows(ROOT/'examples/ORIGINAL_API_REQUEST_INDEX_6.tsv'))==6
 python=list(ROOT.rglob('*.py'))
 for p in python:ast.parse(p.read_text())
 links=0
 for p in ROOT.rglob('*.md'):
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('https:','http:','#')):continue
   dest=(p.parent/unquote(target.split('#')[0])).resolve()
   assert dest.is_relative_to(ROOT)and dest.exists(),(str(p.relative_to(ROOT)),target)
   links+=1
 for p in ROOT.rglob('*'):
  if p.is_file()and p.suffix in ['.py','.md','.json','.jsonl','.txt','.tsv']:
   assert not re.search(r'\bsk-[A-Za-z0-9_-]{20,}\b',p.read_text()),str(p.relative_to(ROOT))
 print(json.dumps(dict(PASS=True,source_files_verified=len(source),questions=121,answer_positions=726,existing_likert_totals=723,reference_cases=121,python_files_syntax_checked=len(python),documentation_links_checked=links,network_calls=0),ensure_ascii=False))
if __name__=='__main__':main()
