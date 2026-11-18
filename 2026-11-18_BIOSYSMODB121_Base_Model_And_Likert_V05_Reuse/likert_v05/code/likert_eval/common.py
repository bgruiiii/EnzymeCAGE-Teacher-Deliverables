import hashlib
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/runtime/f2'))
from f2r12_common import totals_contract

DIMS=['D1','D2','D3a','D3b','D4','D5','D6']
MODEL='deepseek-v4.1-flash-1017'
canonical=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
digest=lambda x:hashlib.sha256(canonical(x).encode()).hexdigest()
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))


def sections(text):
    return [(m[1],m[2])for m in re.finditer(r'===SECTION:([A-Z_0-9]+)_BEGIN===\n(.*?)\n===SECTION:\1_END===',text,re.S)]
