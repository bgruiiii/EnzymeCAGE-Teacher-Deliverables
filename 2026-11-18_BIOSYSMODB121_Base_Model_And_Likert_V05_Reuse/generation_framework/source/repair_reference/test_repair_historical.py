"""Focused offline tests of AST-extracted functions; no business imports or keys."""
import ast
import copy
import json
import pathlib
import tempfile
import threading
import types
import unittest

HERE=pathlib.Path(__file__).resolve().parent
R=HERE.parents[1]
CANDIDATE=R/'FOREIGN_NATIVE_GO_PLUS_FULL_CONTINUATION_20261109/code/full_run_repaired.py'


def module_functions(root):
    tree=ast.parse(CANDIDATE.read_text())
    wanted={'can_send','classify_reject','settle_success','finalize','ready_slot','parallel_queue'}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
    ns=dict(W=root,SOURCE_A='ORIGINAL_ACCOUNT_A',SOURCE_B='LUNA_ACCOUNT_B',NOW=lambda:100.0,
            CASE_ID_SET={'CASE_TEST'},CAP_COMMITS_TOTAL=270,CAP_PHASE_POSTS=246,
            CAP_TECH_POOL=24,CAP_CAPACITY_PER_TARGET=3,CAP_QUOTA_PER_TARGET=1,CAP_LIST_USD=35.0,
            MAX_INFLIGHT_PER_MODEL={'grok-4.7':4,'gpt-6-luna':1},
            ACCOUNT_PATTERNS=['quota','plan','billing'],CAPACITY_PATTERNS=['at capacity'],
            LOCAL_STOPS={'HTTP_SERVICE_ERROR','TRANSPORT_UNKNOWN','SERVICE_FAILED_OR_TERMINAL_UNKNOWN'},
            UNKNOWN_STREAK_EXIT=10,MODEL_RATE_BACKOFF_SECONDS=[1800,3600,7200],
            threading=threading,traceback=__import__('traceback'),
            dump=lambda p,v:None,external_hold=lambda s:False,stop_requested=lambda:False,
            luna_paced=lambda l:False,inputs_unchanged=lambda l:True,progress=lambda l:None,
            prior=types.SimpleNamespace(gate=lambda *a:None),base=types.SimpleNamespace(MODELS=('gpt-6-luna','grok-4.7')))
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(CANDIDATE),'exec'),ns)
    return ns


def ledger():
    return dict(stop_reason=None,commits_total=120,phase_posts=96,quota_recovery_posts=2,
                accounted_usd=10.,unknown_usd=1.,sourceB_accounted_usd=.5,sourceB_unknown_usd=.5,
                cumulative_known_list=9.,cumulative_known_allowance=36.,cumulative_known_cash=0.,
                phase_allowance_accounted={'grok-4.7':4.,'gpt-6-luna':2.},
                phase_known_list={'grok-4.7':0.,'gpt-6-luna':0.},
                phase_known_allowance={'grok-4.7':0.,'gpt-6-luna':0.},
                phase_known_cash={'grok-4.7':0.,'gpt-6-luna':0.},
                multiplier_observations=0,multiplier_last=None,multiplier_max=None,
                unknown_streak=0,capacity_streak=0,slots=[])


class Repair(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name)
        self.m=module_functions(self.root)

    def tearDown(self):self.tmp.cleanup()

    def test_A_settlement_uses_original_reservation(self):
        l=ledger();a=dict(list_accounted=1.,allowance_accounted=4.)
        s={'model':'grok-4.7'};r=dict(list_cost=.2,allowance=.8,cash_cost=0.,billing_source='go-plus')
        self.m['settle_success'](l,s,a,r)
        self.assertAlmostEqual(l['accounted_usd'],9.2);self.assertAlmostEqual(l['unknown_usd'],0.)
        self.assertAlmostEqual(l['cumulative_known_list'],9.2);self.assertEqual(a['list_accounted'],.2)

    def test_B_settlement_separate_and_cumulative(self):
        l=ledger();a=dict(list_accounted=.5,allowance_accounted=2.,credential_source='LUNA_ACCOUNT_B')
        s={'model':'gpt-6-luna'};r=dict(list_cost=.1,allowance=.4,cash_cost=0.,billing_source='go-plus')
        self.m['settle_success'](l,s,a,r)
        self.assertAlmostEqual(l['sourceB_accounted_usd'],.1);self.assertAlmostEqual(l['sourceB_unknown_usd'],0.)
        self.assertAlmostEqual(l['accounted_usd'],10.);self.assertAlmostEqual(l['cumulative_known_list'],9.1)

    def test_B_429_holds_only_Luna(self):
        l=ledger();s={'slot':'TEST','model':'gpt-6-luna'};a={'attempt_id':'TEST-A01','credential_source':'LUNA_ACCOUNT_B'}
        r={'terminal':None,'usage':None,'visible_characters':0};life={'http_status':429}
        result=self.m['finalize'](l,s,a,life,'HTTP_ERROR',self.root,r,'Token rate limit exceeded')
        self.assertEqual(result,'luna_source_held');self.assertIsNone(l['stop_reason'])
        self.assertIn('luna_source_stop',l);self.assertEqual(s['status'],'SOURCE_B_REJECTED_HOLD')
        self.assertNotIn('model_rate_cooldown',l)

    def test_B_cash_gate_not_spoofed(self):
        observed=[]
        def gate(r,*args):observed.append(r['cash_cost']);return 'NONZERO_CASH'
        self.m['prior']=types.SimpleNamespace(gate=gate)
        l=ledger();s={'model':'gpt-6-luna'};a={'attempt_id':'TEST-A01','credential_source':'LUNA_ACCOUNT_B'}
        r=dict(completed=True,cash_cost=1.,billing_source='unexpected',http_status=200)
        self.m['finalize'](l,s,a,{'http_status':200},None,self.root,r,None)
        self.assertEqual(observed,[1.]);self.assertIsNone(l['stop_reason']);self.assertIn('luna_source_stop',l)

    def test_budget_includes_both_accounts_for_Luna(self):
        l=ledger();l['accounted_usd']=34.5;l['sourceB_accounted_usd']=.4
        s=dict(case_id='CASE_TEST',model='gpt-6-luna',status='ELIGIBLE_UNSUBMITTED',attempt_ids=[],worst_list_reservation_usd=.2)
        with self.assertRaisesRegex(AssertionError,'LIST_BUDGET_CAP_35'):self.m['can_send'](l,s)

    def test_already_successful_never_sent_again(self):
        l=ledger();s=dict(case_id='CASE_TEST',model='gpt-6-luna',status='COMPLETE',attempt_ids=['OLD'],worst_list_reservation_usd=.2)
        with self.assertRaisesRegex(AssertionError,'DEDUP_ALREADY_SUBMITTED_OR_REUSED'):self.m['can_send'](l,s)

    def test_Grok_request_shape_unchanged(self):
        original=CANDIDATE.with_name('full_run.py')
        def funcs(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)}
        old,new=funcs(original),funcs(CANDIDATE)
        for name in ('body_for','science','request','dispatch_stream','worker','worker_par'):
            self.assertEqual(old[name],new[name],name)

    def scheduler_fixture(self,with_key=True,hold=False):
        l=ledger();l['slots']=[dict(slot='G',model='grok-4.7',status='ELIGIBLE_UNSUBMITTED'),dict(slot='L',model='gpt-6-luna',status='ELIGIBLE_UNSUBMITTED')]
        clock={'now':0.};l['model_rate_cooldown']={'gpt-6-luna':1.}
        started=threading.Event();luna_done=threading.Event();sent=[];lock=threading.Lock()
        self.m['NOW']=lambda:clock['now'];self.m['can_send']=lambda *a:None
        def commit(l,s,key,source):
            s['status']='DISPATCH_COMMITTED';sent.append((s['model'],source))
            return ({'slot':s['slot']},self.root,None,{})
        def stream(d,req,key,op,life):
            if key=='FIXTURE_G':
                started.set()
                if with_key and not hold:assert luna_done.wait(1.),'Luna was blocked by Grok join'
            else:
                assert started.wait(1.);luna_done.set()
            return None,None
        def finalize(l,s,*args):s['status']='COMPLETE'
        def sleep(_):
            clock['now']+=1.
            started.wait(.001)
        self.m.update(dispatch_commit=commit,dispatch_stream=stream,finalize=finalize,
                      core=types.SimpleNamespace(materialize=lambda *a:{}),time=types.SimpleNamespace(sleep=sleep),
                      wait_for_work=lambda l:False)
        if hold:l['luna_source_stop']={'reason':'existing rejection'}
        self.m['parallel_queue'](l,'FIXTURE_G',None,threads=1,lock=lock,
                                 keyB='FIXTURE_L' if with_key else None,openerB=object() if with_key else None)
        self.assertIsNone(l['stop_reason']);return l,sent

    def test_Luna_readiness_does_not_wait_for_Grok(self):
        l,sent=self.scheduler_fixture();self.assertEqual(len(sent),2)
        self.assertTrue(all(s['status']=='COMPLETE' for s in l['slots']))

    def test_missing_Luna_key_does_not_stop_Grok(self):
        l,sent=self.scheduler_fixture(with_key=False);self.assertEqual(sent,[('grok-4.7','ORIGINAL_ACCOUNT_A')])

    def test_held_Luna_does_not_stop_Grok(self):
        l,sent=self.scheduler_fixture(hold=True);self.assertEqual(sent,[('grok-4.7','ORIGINAL_ACCOUNT_A')])


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Repair))
    (HERE/'FOCUSED_TEST_RESULTS.json').write_text(json.dumps(dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful(),business_imports=0,network_posts=0,credential_reads=0),indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
