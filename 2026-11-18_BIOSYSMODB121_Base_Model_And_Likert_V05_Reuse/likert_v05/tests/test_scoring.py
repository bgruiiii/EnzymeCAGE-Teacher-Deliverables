"""Meaningful contract regression checks, using SYNTHETIC data only."""
import copy
import json
import socket
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
from likert_eval.common import load,DIMS,totals_contract
from likert_eval.pipeline import prepare,validate_return,merge
from likert_eval.runner import run
from f2r12_budget_ledger import BudgetLedger,SlotAttemptQuotaExceeded
from f2r12_transport import parse_sse_bytes,new_stream_state


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.item=load(ROOT/'examples/synthetic_item.json')
        self.req=prepare(self.item)
        self.response=load(ROOT/'examples/synthetic_response.json')

    def test_actual_full_seven_dimension_validation(self):
        self.assertTrue(validate_return(self.response,self.req)['valid'])
        self.assertEqual(set(self.response['dimensions']),set(DIMS))

    def test_deterministic_prepared_request_identity(self):
        self.assertEqual(self.req,load(ROOT/'examples/synthetic_request.json'))

    def test_original_totals_formula_and_missing_weight(self):
        result=merge(self.response,self.req)
        self.assertEqual(result['totals']['weighted_total'],4*1.5+5*2.5+3+6+1*1.5+2*1.5+7)
        self.assertEqual(result['dimensions']['D4']['score_status'],'MISSING')

    def test_known_cap_cannot_be_bypassed_by_key_error_n(self):
        bad=copy.deepcopy(self.response);bad['dimensions']['D3a']['score']=5
        self.assertIn('D3a:SCORE_RANGE',validate_return(bad,self.req)['errors'])

    def test_wrong_answer_identity_rejected(self):
        bad=copy.deepcopy(self.response);bad['identity']['answer_sha256']='0'*64
        self.assertIn('REPAIR_IDENTITY_MISMATCH',validate_return(bad,self.req)['errors'])

    def test_fake_reference_rejected(self):
        bad=copy.deepcopy(self.response);bad['dimensions']['D1']['evidence_refs'][0]['ref_id']='UNPROVIDED_RECORD'
        self.assertIn('D1:FABRICATED_REFERENCE',validate_return(bad,self.req)['errors'])

    def test_boolean_float_and_string_are_not_scores(self):
        for value in [True,3.0,'3']:
            bad=copy.deepcopy(self.response);bad['dimensions']['D3a']['score']=value
            self.assertIn('D3a:SCORE_RANGE',validate_return(bad,self.req)['errors'])

    def test_ne_does_not_erase_determined_numeric_decision(self):
        bad=copy.deepcopy(self.response)
        bad['dimensions']['D3a'].update(score_status='NE',score=None,ne_basis='SYNTHETIC automatic uncertainty',ne_unverified='SYNTHETIC pending matcher')
        self.assertIn('D3a:NE_CONFLICT_WITH_DETERMINED_PROGRAM_DECISION',validate_return(bad,self.req)['errors'])

    def test_genuine_ne_preserved_and_total_not_reweighted(self):
        item=copy.deepcopy(self.item);item['program']['d3a_decision_status']='JUDGE_REQUIRED'
        req=prepare(item);response=copy.deepcopy(self.response);response['identity']=req['identity']
        response['dimensions']['D3a'].update(score_status='NE',score=None,
            ne_basis='SYNTHETIC critical fact has no supplied reference',ne_unverified='SYNTHETIC exact missing target record')
        result=merge(response,req)
        self.assertEqual(result['totals']['status'],'NOT_COMPARABLE')
        self.assertIsNone(result['totals']['weighted_total'])

    def test_partial_repair_preserves_other_six_dimensions(self):
        req=load(ROOT/'examples/synthetic_repair_request.json')
        response=load(ROOT/'examples/synthetic_repair_response.json')
        baseline=load(ROOT/'examples/synthetic_repair_baseline.json')
        result=merge(response,req,baseline)
        for d in DIMS:
            if d!='D3a':self.assertEqual(result['dimensions'][d],baseline['dimensions'][d])

    def test_partial_repair_cannot_replace_existing_numeric_score(self):
        req=load(ROOT/'examples/synthetic_repair_request.json');response=load(ROOT/'examples/synthetic_repair_response.json')
        with self.assertRaises(ValueError):merge(response,req,{'dimensions':self.response['dimensions']})

    def test_no_extra_dimension(self):
        req=load(ROOT/'examples/synthetic_repair_request.json');response=load(ROOT/'examples/synthetic_repair_response.json')
        response['dimensions']['D1']=copy.deepcopy(self.response['dimensions']['D1'])
        self.assertIn('DIMENSIONS_MISMATCH',validate_return(response,req)['errors'])

    def test_default_config_and_synthetic_input_cannot_trigger_paid_call(self):
        config=load(ROOT/'config_templates/scoring.example.json')
        with tempfile.TemporaryDirectory()as d:
            with self.assertRaises(ValueError):run(self.req,config,d,False)
            config['live_authorized']=True
            with self.assertRaisesRegex(ValueError,'SYNTHETIC'):run(self.req,config,d,True)
            self.assertFalse((Path(d)/'ledger').exists())

    def test_unknown_charge_is_retained_and_not_rebought(self):
        with tempfile.TemporaryDirectory()as d:
            ledger=BudgetLedger(d,10,3,2,max_transfers_per_target=1)
            ledger.reserve('SYNTHETIC#t1','request_1',2)
            self.assertEqual(ledger.reconcile_on_startup(),1)
            state=load(Path(d)/'BUDGET_STATE.json')
            self.assertEqual(state['unknown_reserves']['SYNTHETIC#t1']['reserve_cny'],2)
            with self.assertRaises(SlotAttemptQuotaExceeded):ledger.reserve('SYNTHETIC#t2','request_1',2)

    def test_production_sse_parser_reads_complete_json(self):
        text=json.dumps(self.response,ensure_ascii=False)
        packets=[dict(model='deepseek-v4.1-flash-1017',choices=[dict(delta=dict(content=text),finish_reason=None)]),
                 dict(model='deepseek-v4.1-flash-1017',choices=[dict(delta={},finish_reason='stop')],usage=dict(prompt_tokens=1,completion_tokens=1,total_tokens=2))]
        raw=(''.join('data: '+json.dumps(p,ensure_ascii=False)+'\n\n'for p in packets)+'data: [DONE]\n\n').encode()
        state=new_stream_state();parsed=parse_sse_bytes(raw,state)
        self.assertEqual(json.loads(parsed),self.response);self.assertTrue(state['done_seen'])


if __name__=='__main__':
    # A test accidentally trying network fails instead of reaching a service.
    socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError('offline tests must not connect'))
    unittest.main(verbosity=2)
