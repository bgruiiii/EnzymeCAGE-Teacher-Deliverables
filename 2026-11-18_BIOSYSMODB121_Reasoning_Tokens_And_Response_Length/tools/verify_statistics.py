"""Portable verification of published per-case observations and summary tables."""
import csv,hashlib,json,re
from pathlib import Path
from decimal import Decimal
from collections import Counter
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
def read(name):
 with(ROOT/name).open(newline='')as h:return list(csv.DictReader(h,delimiter='\t'))
def quant(values,p):
 v=sorted(values);x=Decimal(len(v)-1)*p;i=int(x)
 return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(x-i)
def close(a,b):assert abs(Decimal(a)-b)<Decimal('0.00000001'),(a,str(b))
def main():
 for line in(ROOT/'SHA256SUMS').read_text().splitlines():
  want,rel=line.split('  ',1);p=(ROOT/rel).resolve();assert p.is_relative_to(ROOT)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==want,rel
 rs=read('PER_CASE_LENGTH_AND_TOKENS_847.tsv');summaries=read('MODEL_SUMMARY.tsv')
 assert len(rs)==len({(r['cohort'],r['model'],r['case_id'])for r in rs})==847
 assert set(Counter((x['cohort'],x['model'])for x in rs).values())=={121}
 assert len(summaries)==14
 keys=['input_tokens','total_output_tokens','actual_reasoning_tokens','output_minus_reasoning_tokens','body_chars','body_nonspace_chars','body_han_chars','body_utf8_bytes']
 for r in rs:
  assert r['explicit_thinking_budget']==''
  if r['output_minus_reasoning_tokens']!='':close(r['output_minus_reasoning_tokens'],Decimal(r['total_output_tokens'])-Decimal(r['actual_reasoning_tokens']))
  if r['body_chars']!='':assert Decimal(r['body_han_chars'])<=Decimal(r['body_nonspace_chars'])<=Decimal(r['body_chars'])
 for m in summaries:
  group=[r for r in rs if r['cohort']==m['cohort']and r['model']==m['model']and(m['subset']=='ALL_POSITIONS_OBSERVED_ONLY'or r['complete_and_schema_valid']=='True')]
  assert len(group)==int(m['subset_n'])
  for key in keys:
   values=[Decimal(r[key])for r in group if r[key]!=''];assert len(values)==int(m[key+'_n'])
   if not values:assert m[key+'_mean']=='';continue
   close(m[key+'_mean'],sum(values)/len(values));close(m[key+'_median'],quant(values,Decimal('.5')));close(m[key+'_p90'],quant(values,Decimal('.9')));close(m[key+'_p95'],quant(values,Decimal('.95')));close(m[key+'_min'],min(values));close(m[key+'_max'],max(values))
 links=0
 for p in ROOT.glob('*.md'):
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('http:','https:','#')):continue
   dest=(p.parent/unquote(target.split('#')[0])).resolve()
   if dest.is_relative_to(ROOT):assert dest.exists(),target
   links+=1
 print(json.dumps(dict(PASS=True,observations=847,summary_rows=14,groups=7,statistics='Decimal means and interpolated percentiles',links_checked=links,API_calls=0),ensure_ascii=False))
if __name__=='__main__':main()
