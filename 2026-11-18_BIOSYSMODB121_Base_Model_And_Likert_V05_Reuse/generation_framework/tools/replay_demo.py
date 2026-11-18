"""Standard-library, synthetic, offline replay using unchanged historical parsers."""
import ast,hashlib,json,re
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def pure_functions(relative,names,extras=None):
 p=ROOT/relative;tree=ast.parse(p.read_text())
 nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in names]
 assert {n.name for n in nodes}==set(names)
 env={'json':json,'re':re};env.update(extras or{})
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),env)
 return env

def main():
 expected=json.loads((ROOT/'examples/expected.json').read_text())
 chat=pure_functions('source/aliyun/g8_formal_runner.py',['flatten','search_evidence','parse_stream'],{'URL_RE':re.compile(r'https?://\S+',re.I)})
 raw=(ROOT/'examples/chat_stream.sse').read_bytes()
 a=chat['parse_stream'](raw.splitlines(keepends=True))
 assert a['visible']==expected['visible_text']and a['usage']==expected['chat_usage']and a['done']
 resp=pure_functions('source/opencode/pilot.py',['events','parse'])
 b=resp['parse']((ROOT/'examples/responses_stream.sse').read_bytes())
 assert b['visible_answer']==expected['visible_text']and b['usage']==expected['responses_usage']and b['completed']
 assert b['visible_answer']!=expected['visible_text']*2,'Do not concatenate delta and completed text twice'
 # A missing final event is a partial stream, not completion.
 incomplete=b'event: response.output_text.delta\ndata: {"type":"response.output_text.delta","delta":"SYNTHETIC partial"}\n\n'
 c=resp['parse'](incomplete);assert not c['completed']and c['usage']is None
 # Pure arithmetic example of the documented overwritten-reservation bug.
 reserved=Decimal('.8');actual=Decimal('.1')
 old_accounted=reserved+actual-actual;old_unknown=reserved-actual
 correct_accounted=reserved+actual-reserved;correct_unknown=reserved-reserved
 assert old_accounted==Decimal('.8')and old_unknown==Decimal('.7')
 assert correct_accounted==Decimal('.1')and correct_unknown==0
 print(json.dumps(dict(PASS=True,label='SYNTHETIC_OFFLINE_ONLY',chat_replay=True,responses_replay=True,no_duplicate_terminal_text=True,incomplete_not_completed=True,reservation_bug_demonstrated=True,network_requests=0,credential_reads=0),ensure_ascii=False))
if __name__=='__main__':main()
