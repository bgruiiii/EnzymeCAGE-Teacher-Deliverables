"""Narrow proof receipts. 03D-R1: REAL consumption must bind the CURRENT answer sheet,
case, audited answer identity and current predicted step; synthetic fixtures stay isolated."""
from common_03a import OUT,R,load,sha,jsha,rows
FACT_KEYS=('route_state','credit_class','five_state','conclusion')
ALIGNMENT='LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK/STEP_ALIGNMENT.tsv'
R3EV='LIKERT_V05_REVISION_20261105_R3/P2_DISPOSITION_EVIDENCE/STEP_EVIDENCE_STATES_R3.tsv'
F0IDX='LIKERT_V04_FULL_SCORING_20261029/F0_INPUT_BASELINE/B_480_ANSWER_INDEX.tsv'
_f0cache={}
def F0_ROW(slot):
 if not _f0cache:
  for x in rows(R/F0IDX):
   _f0cache.setdefault(x['b_slot_uid'],x)
 return _f0cache.get(slot)
_r3cache={}
def R3_FACTS(slot,gid):
 if not _r3cache:
  for x in rows(R/R3EV):
   _r3cache[(x['b_slot_uid'],x['gold_step_id'])]=(x['route_step_state'],x['credit_class'],x['five_state'],x['step_conclusion'])
 return _r3cache.get((slot,gid))

def resolve_proof(ref,row,synthetic,expected_conclusion,current=None):
 if not isinstance(ref,dict) or set(ref)!={'proof_id'} or not isinstance(ref['proof_id'],str):
  raise ValueError('failure proof must be registered proof_id only; supplied metadata is not evidence')
 mode='SYNTHETIC' if synthetic else 'REAL'
 index=load(OUT/'proofs/REGISTRY_IDENTITIES.json')
 p=OUT/index[mode]['path']
 if sha(p.read_bytes())!=index[mode]['sha256']:raise ValueError('proof registry identity mismatch')
 registry=load(p)
 if registry['mode']!=mode:raise ValueError('proof registry mode mismatch')
 rec=registry['records'].get(ref['proof_id'])
 if rec is None:raise ValueError('unregistered proof_id in '+mode)
 if rec['mode']!=mode or rec['target_id']!=row['target_id'] or rec['verified_conclusion']!=expected_conclusion:
  raise ValueError('proof target/type/conclusion mismatch')
 if any(row[k]!=rec['expected_input_facts'][k] for k in FACT_KEYS):
  raise ValueError('failure proof conflicts with current route/credit/support facts')
 if mode=='REAL':
  if rec['proof_type']!='DETERMINISTIC_ROUTE_PROOF' or rec['source_path_rel_R']!=ALIGNMENT:
   raise ValueError('unapproved scientific/AI proof source; no chemical replies registered')
  # Pin the allowed source to the pre-work, reviewed source identity, not a caller supplied hash.
  before={x['path_rel_R']:x['sha256'] for x in load(OUT/'UPSTREAM_BEFORE.json')}
  _add=OUT/'proofs/RELEASE_CTX_ADDITIONS.json'
  if _add.is_file():
   before.update({x['path_rel_R']:x['sha256'] for x in load(_add)['records']})
  if rec['source_sha256']!=before.get(ALIGNMENT):raise ValueError('source not bound to reviewed input')
  source=R/ALIGNMENT
  if not source.is_file() or sha(source.read_bytes())!=rec['source_sha256']:raise ValueError('proof source absent or changed')
  matches=[x for x in rows(source) if x['b_slot_uid']==rec['source_key']['b_slot_uid'] and x['gold_step_id']==rec['target_id']]
  if len(matches)!=1:raise ValueError('proof record not uniquely found')
  actual=matches[0]
  if jsha(actual)!=rec['source_record_sha256']:raise ValueError('proof source record changed')
  if actual['step_state']!='NONMATCH' or actual['reason_code']!=rec['reason_code'] or actual['binding_status']!=rec['binding_status']:
   raise ValueError('route record does not support registered failure')
  if not actual['reason_code'].startswith(('SUBSTITUTED_','DIRECTION_FLIPPED_STRICT','STEREO_CONFLICT_SPECIFIED','ORDER_')):
   raise ValueError('unconfirmed route reason')
  if {k:actual[k] for k in ['gold_reaction_id','gold_arrow_class','pred_step_id']}!=rec['reaction_binding']:
   raise ValueError('target reaction/direction/prediction binding mismatch')
  # F03D-02 (03D-R1): the proof is bound to the CURRENT answer sheet, case, audited answer
  # identity and the current target's own predicted step. Proof_id prefix alone never suffices,
  # four matching class labels never authorize cross-answer reuse, and identity is not optional.
  if current is None:raise ValueError('real proof consumption requires current answer binding')
  for k in ('b_slot_uid','case_id','answer_sha256'):
   if not current.get(k):raise ValueError('current answer binding missing '+k)
  if current['b_slot_uid']!=rec['source_key']['b_slot_uid']:
   raise ValueError('proof belongs to slot '+rec['source_key']['b_slot_uid']+', current answer is '+current['b_slot_uid'])
  if current['case_id']!=rec.get('case_id') or current['case_id']!=row['target_id'].split('__')[0]:
   raise ValueError('current case does not match proof target')
  if current['answer_sha256']!=rec.get('answer_sha256'):
   raise ValueError('current answer identity differs from frozen proof binding')
  srci=rec['answer_identity_source']; f0=R/srci['path']
  if sha(f0.read_bytes())!=srci['sha256']:raise ValueError('answer identity source absent/changed')
  fr=F0_ROW(current['b_slot_uid'])
  if fr is None or fr['answer_sha256_recomputed']!=rec['answer_sha256'] or fr['case_id']!=current['case_id']:
   raise ValueError('audited F0 baseline does not confirm current answer identity for proof slot')
  cur_pred=row.get('original_pred_step_id')
  if cur_pred!=rec['reaction_binding']['pred_step_id']:
   raise ValueError('current predicted step '+str(cur_pred)+' != proof source prediction '+rec['reaction_binding']['pred_step_id'])
  # Also bind the exact target's current R3 terminal-state four facts (03D: proof extension is
  # independent of the KEY list and covers all deterministic route failures, not only three examples).
  r3p=R/rec['r3_source']['path']
  if not r3p.is_file() or sha(r3p.read_bytes())!=rec['r3_source']['sha256']:raise ValueError('R3 evidence source absent/changed')
  add=load(OUT/'UPSTREAM_03D_ADDITIONS.json')
  if rec['r3_source']['sha256']!=add['pins'].get(rec['r3_source']['path'],{}).get('sha256'):raise ValueError('R3 source not bound to reviewed 03D snapshot')
  facts=R3_FACTS(rec['source_key']['b_slot_uid'],row['target_id'])
  if facts!=tuple(rec['expected_input_facts'][k] for k in FACT_KEYS):raise ValueError('proof conflicts with current R3 four facts')
  # Where a landed coordination ctx exists, its echoed facts must agree too (never a weaker check).
  if 'ctx_path_rel_R' in rec:
   ctxpath=R/rec['ctx_path_rel_R']
   if not ctxpath.is_file() or sha(ctxpath.read_bytes())!=before.get(rec['ctx_path_rel_R']):raise ValueError('original ctx source changed')
   if load(ctxpath)['step_facts'].get(row['target_id'])!=rec['expected_input_facts']:raise ValueError('source ctx facts do not support proof')
 else:
  if rec['proof_type']!='SYNTHETIC_FIXTURE' or rec['source_path']!='proofs/SYNTHETIC_FACT_FIXTURES.json':raise ValueError('synthetic provenance mismatch')
  source=OUT/rec['source_path']
  if not source.is_file() or sha(source.read_bytes())!=rec['source_sha256']:raise ValueError('synthetic fixture source absent/changed')
  fixture=load(source)['records'].get(rec['source_record_id'])
  if fixture is None or jsha(fixture)!=rec['source_record_sha256']:raise ValueError('synthetic record absent/changed')
  if fixture['target_id']!=row['target_id'] or fixture['verified_conclusion']!=expected_conclusion or fixture['expected_input_facts']!=rec['expected_input_facts']:
   raise ValueError('synthetic target/conclusion mismatch')
 return rec
