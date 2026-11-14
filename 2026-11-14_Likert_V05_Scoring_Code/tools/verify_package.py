#!/usr/bin/env python3
"""Standard-library integrity, source identity and local link verification."""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def verify(root):
    root=Path(root).resolve();errors=[];checked=0;links=0
    manifest=root/'SHA256SUMS'
    if not manifest.exists():raise ValueError('SHA256SUMS is missing')
    for line in manifest.read_text().splitlines():
        h,name=line.split('  ',1);p=root/name
        if not p.resolve().is_relative_to(root):errors.append('unsafe manifest path');continue
        if not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=h:errors.append('SHA mismatch: '+name)
        checked+=1
    for row in csv.DictReader((root/'provenance/SOURCE_MANIFEST.tsv').open(),delimiter='\t'):
        p=root/row['export_path']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=row['export_sha256']:errors.append('export source identity mismatch: '+row['export_path'])
        if row['transformation']=='BYTE_IDENTICAL'and row['original_sha256']!=row['export_sha256']:errors.append('byte-identical assertion mismatch')
    for p in root.rglob('*.md'):
        for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if url.startswith(('https://','http://','#','mailto:')):continue
            path=unquote(url.split('#',1)[0])
            if path and not(p.parent/path).exists():errors.append('broken relative link: '+str(p.relative_to(root))+' -> '+path)
            links+=1
    for p in root.rglob('*.py'):
        if '__pycache__'in p.parts:continue
        try:compile(p.read_text(),str(p.relative_to(root)),'exec')
        except SyntaxError:errors.append('Python syntax error: '+str(p.relative_to(root)))
    forbidden={'aliyun_scoring_api_keys.local.md','apikey.tokenplan.ali1110.txt','response_raw.bin','BUDGET_STATE.json'}
    for p in root.rglob('*'):
        if p.is_symlink():errors.append('unexpected symlink: '+str(p.relative_to(root)))
        if p.name in forbidden:errors.append('private run/credential artifact included: '+p.name)
    result=dict(PASS=not errors,checked_files=checked,relative_links_checked=links,errors=errors,network_calls=0)
    print(json.dumps(result,ensure_ascii=False));return result


if __name__=='__main__':
    r=verify(sys.argv[1]if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
    raise SystemExit(0 if r['PASS']else 1)
