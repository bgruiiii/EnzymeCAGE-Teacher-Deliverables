"""Verify source SHA, Python syntax, local documentation links and package contents."""
import ast,csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 for line in(ROOT/'SHA256SUMS').read_text().splitlines():
  want,relative=line.split('  ',1);p=(ROOT/relative).resolve()
  assert p.is_relative_to(ROOT)and p.is_file(),relative
  assert hashlib.sha256(p.read_bytes()).hexdigest()==want,relative
 sources=list(csv.DictReader((ROOT/'provenance/SOURCE_MANIFEST.tsv').open(),delimiter='\t'))
 for x in sources:
  assert x['source_sha256']==x['export_sha256']==hashlib.sha256((ROOT/x['export_path']).read_bytes()).hexdigest(),x['export_path']
 py=list(ROOT.rglob('*.py'))
 for p in py:ast.parse(p.read_text())
 links=0
 for p in ROOT.rglob('*.md'):
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('https:','http:','#')):continue
   path=(p.parent/target.split('#')[0]).resolve()
   assert path.is_relative_to(ROOT)and path.exists(),(p.relative_to(ROOT),target)
   links+=1
 for p in ROOT.rglob('*'):
  if not p.is_file():continue
  assert p.name not in ['.env','opencode_api_key.txt','opencode_luna_api_key.txt','config.local.json']
  if p.suffix in ['.json','.md','.py','.txt','.tsv','.sse']:
   text=p.read_text()
   assert not re.search(r'\bsk-[A-Za-z0-9_-]{20,}\b',text),p.relative_to(ROOT)
 print(json.dumps(dict(PASS=True,source_files_sha_verified=len(sources),python_files_syntax_checked=len(py),documentation_links_verified=links,network_requests=0),ensure_ascii=False))
if __name__=='__main__':main()
