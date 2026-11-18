"""Export existing reference data for one case. Does not decide a new task scope."""
import argparse,csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
 with p.open(newline='')as h:
  r=csv.DictReader(h,delimiter='\t');return r.fieldnames,list(r)
def export(case,out):
 metadata={x['case_id']:x for x in map(json.loads,(ROOT/'questions/main_cases.jsonl').read_text().splitlines())}
 if case not in metadata:raise ValueError('case not in original 121')
 if out.exists():raise FileExistsError('use a new output directory')
 out.mkdir(parents=True)
 (out/'ORIGINAL_QUESTION.json').write_bytes((ROOT/'questions/original_messages'/f'{case}.json').read_bytes())
 scope=next(x for x in rows(ROOT/'reference/original_task_contracts/CURRENT_ROUTE_LOCKED_SCOPE_121.tsv')[1]if x['case_id']==case)
 (out/'ORIGINAL_TASK_SCOPE.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n')
 counts={}
 for src in list((ROOT/'reference/gold_121').glob('*.tsv'))+[ROOT/'reference/original_task_contracts/ACCEPTED_ENZYMES_RELEASE.tsv']:
  fields,rs=rows(src)
  filtered=[x for x in rs if x['case_id']==case]if'case_id'in fields else rs
  with(out/src.name).open('w',newline='')as h:
   wr=csv.DictWriter(h,fields,delimiter='\t',lineterminator='\n');wr.writeheader();wr.writerows(filtered)
  counts[src.name]=len(filtered)
 overrides=ROOT/'reference/case_overrides'/case
 if overrides.exists():
  import shutil
  shutil.copytree(overrides,out/'case_overrides')
 info=dict(case_id=case,metadata=metadata[case],exported_rows=counts,reference_purpose='ORIGINAL_ROUTE_LOCKED_TASK_REFERENCE_NOT_NEW_ANSWER_FACTS',warning='Original scope is not a new pollutant-only task contract. Empty release-accepted slice does not mean no enzyme evidence: consult enzyme_gold/case overrides. No old answer alignment or score is assigned to a new answer.')
 (out/'REFERENCE_INFO.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n');return info
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();print(json.dumps(export(a.case,a.out),ensure_ascii=False))
