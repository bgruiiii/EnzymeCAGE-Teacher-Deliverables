"""Synthetic protocol/identity checks. No real key or network."""
import os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from collect_one import execute,ROOT
class Response:
 status=200
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def __iter__(self):return iter((ROOT/'generation_framework/examples/responses_stream.sse').read_bytes().splitlines(keepends=True))
class Fake:
 def __init__(self):self.calls=0
 def open(self,request,timeout):self.calls+=1;return Response()
class Tests(unittest.TestCase):
 def setUp(self):
  self.body={'model':'SYNTHETIC_RESPONSES_MODEL','input':[{'role':'user','content':'SYNTHETIC'}],'max_output_tokens':256,'stream':True}
  self.cfg={'model':self.body['model'],'protocol':'responses','endpoint':'https://opencode.ai/inference/go/openai/v1/responses','live_authorized':True,'api_key_env':'SYNTHETIC_BASE_MODEL_TEST_KEY'}
 def test_dry_run_neither_reads_key_nor_sends(self):
  with tempfile.TemporaryDirectory()as d:
   f=Fake()
   with patch.dict(os.environ,{},clear=True):a=execute(self.body,self.cfg,d,False,f)
   self.assertTrue(a['dry_run']);self.assertEqual(f.calls,0)
 def test_one_send_and_resume_dedup(self):
  with tempfile.TemporaryDirectory()as d,patch.dict(os.environ,{'SYNTHETIC_BASE_MODEL_TEST_KEY':'SYNTHETIC_NOT_A_REAL_CREDENTIAL'}):
   f=Fake();a=execute(self.body,self.cfg,d,True,f);b=execute(self.body,self.cfg,d,True,f)
   self.assertEqual(a['status'],'COMPLETE');self.assertTrue(b['deduped']);self.assertEqual(f.calls,1)
   self.assertEqual((Path(d)/'raw_stream.sse').read_bytes(),(ROOT/'generation_framework/examples/responses_stream.sse').read_bytes())
 def test_unknown_not_resent(self):
  class Broken(Fake):
   def open(self,*a,**kw):self.calls+=1;raise TimeoutError()
  with tempfile.TemporaryDirectory()as d,patch.dict(os.environ,{'SYNTHETIC_BASE_MODEL_TEST_KEY':'SYNTHETIC_NOT_A_REAL_CREDENTIAL'}):
   f=Broken();a=execute(self.body,self.cfg,d,True,f);b=execute(self.body,self.cfg,d,True,f)
   self.assertEqual(a['billing_status'],'UNKNOWN');self.assertTrue(b['deduped']);self.assertEqual(f.calls,1)
 def test_request_drift_refused(self):
  with tempfile.TemporaryDirectory()as d:
   execute(self.body,self.cfg,d)
   with self.assertRaises(ValueError):execute(dict(self.body,max_output_tokens=128),self.cfg,d)
 def test_double_live_gate(self):
  with tempfile.TemporaryDirectory()as d:
   with self.assertRaises(ValueError):execute(self.body,dict(self.cfg,live_authorized=False),d,True,Fake())
if __name__=='__main__':unittest.main()
