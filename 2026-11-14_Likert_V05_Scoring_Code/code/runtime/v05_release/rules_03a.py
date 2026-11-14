"""Small offline candidate decision layer. No network, live runner or stored model scores."""
from collections import Counter
from fractions import Fraction
import re
from common_03a import OUT, load,sha

from proofs_03a_r1 import resolve_proof
from registry_03d import verify_real_key_record, branch_gate

def classify(row, synthetic=False, current=None):
 required={'target_id','route_state','credit_class','five_state','conclusion','delivered','enzyme_info_present',
           'support_at_claim_granularity','explicit_ec_pair_status','importance','key','source_locator',
           'reference_or_scope_gap','route_failure_proof','catalytic_failure_proof','omission_locator'}
 missing=required-set(row)
 if missing: raise ValueError('missing target fields: '+','.join(sorted(missing)))
 for k in ['key','reference_or_scope_gap']:
  if type(row[k]) is not bool:raise ValueError(k+' must be bool')
 for k in ['delivered','enzyme_info_present','support_at_claim_granularity']:
  if row[k] is not None and type(row[k]) is not bool:raise ValueError(k+' must be boolean or null')
 if not row['target_id'] or not row['source_locator']:raise ValueError('target/source empty')
 if row['importance'] not in ['MAJOR','MINOR'] or (row['key'] and row['importance']!='MAJOR'):raise ValueError('bad importance')
 if row['explicit_ec_pair_status'] not in ['CONFIRMED','UNRESOLVED','ABSENT']:raise ValueError('bad EC pair')
 for field,conclusion in [('route_failure_proof','TARGET_FAILURE'),('catalytic_failure_proof','CATALYTIC_FAILURE')]:
  if row[field] is not None:resolve_proof(row[field],row,synthetic,conclusion,current)
 if row['reference_or_scope_gap']:return 'H','REFERENCE_OR_SCOPE'
 if row['route_failure_proof'] is not None:
  resolve_proof(row['route_failure_proof'],row,synthetic,'TARGET_FAILURE',current)
  return 'F','CONFIRMED_TARGET_FAILURE'
 if row['delivered'] is False:
  if not row['omission_locator']:raise ValueError('missing omission locator')
  return 'M','DELIVERY_OMISSION'
 if row['enzyme_info_present'] is False:
  if not row['omission_locator']:raise ValueError('missing enzyme omission locator')
  return 'M','ENZYME_INFO_ABSENT'
 if row['route_state']!='MATCH':return 'U','ALIGNMENT_NOT_CONFIRMED'
 if row['catalytic_failure_proof'] is not None:
  resolve_proof(row['catalytic_failure_proof'],row,synthetic,'CATALYTIC_FAILURE',current)
  return 'F','CONFIRMED_CATALYTIC_INCOMPATIBILITY'
 if (row['delivered'] is True and row['enzyme_info_present'] is True
     and row['credit_class']=='CONFIRMED_TARGET' and row['five_state']=='SUPPORTED'
     and row['support_at_claim_granularity'] is True and row['explicit_ec_pair_status']!='UNRESOLVED'):
  return 'S','TARGET_SUPPORT_CONFIRMED'
 return 'U', ('PAIR_UNVERIFIED' if row['explicit_ec_pair_status']=='UNRESOLVED' else
               'CANDIDATE' if row['credit_class']=='CANDIDATE_ONLY' else 'SUPPORT_GAP')

def band(s,n,rules,high=False):
 c=Fraction(s,n)
 for b in rules['d3a']['bands']:
  if c < Fraction(b['upper_exclusive']):return b['allowed_range']
 return rules['d3a']['all_supported_range'] if high else rules['d3a']['all_supported_but_gate_blocked_range']

def user_key_cap(contract,mapped,rules):
 """Method confirmed; actual KEY identities still require their own predefinition."""
 registry=load(OUT/'KEY_DEFINITION_BINDINGS.json')
 if sha((OUT/'KEY_DEFINITION_BINDINGS.json').read_bytes())!=rules['key_definition_registry_sha256']:raise ValueError('KEY definition registry identity mismatch')
 triggers=[];pending=[]
 for source,m in zip(contract['targets'],mapped):
  if not m['key'] or m['class'] not in ['F','M']:continue
  if contract['synthetic']:
   predef=registry['synthetic_predefined_keys'].get(m['target_id'])
   if predef is None:raise ValueError('synthetic KEY has no predeclared fixture target')
  else:
   predef=registry['confirmed_real_keys'].get(m['target_id'])
   if predef is None:
    pending.append({'target_id':m['target_id'],'fact_class':m['class'],
      'reason': registry.get('held_real_keys',{}).get(m['target_id'],{})
        .get('hold_reason','no METHOD_CONFIRMED KEY record for this composite identity (HELD/BACKGROUND/quarantined or unadopted scope)')})
    continue
   ident=contract.get('consumer_identity') or {}
   if str(predef.get('scope_kind','')).startswith('PATH_CATALOG'):
    # F03D-01 runtime gate: without the current selected adopted main chain the record is
    # PENDING and never triggers the cap; branch-union KEY failure is forbidden here.
    sel=ident.get('current_path_id')
    if not sel:
     # A proven omission on a step shared by EVERY adopted chain does not
     # depend on selecting one branch; verify each existing path binding.
     from registry_03d import _path_index
     catalog,_ = _path_index()
     paths=[p for p in catalog.get(ident.get('case_id'),{}).values()
            if p['adoption_status']=='ADOPTED_METHOD_CONFIRMED']
     if paths and all(m['target_id'] in p['ordered_step_ids'].split('|') for p in paths):
      for path in paths:
       verify_real_key_record(predef,registry,m['target_id'],mode='runtime',
         current={'case_id':ident.get('case_id'),'selected_path_id':path['path_id']})
     else:
      pending.append({'target_id':m['target_id'],'fact_class':m['class'],
        'reason':'unbound branch; failed step is not established as common to every adopted main chain'})
      continue
    else:
     verify_real_key_record(predef,registry,m['target_id'],mode='runtime',
       current={'case_id':ident.get('case_id'),'selected_path_id':sel})
   else:
    verify_real_key_record(predef,registry,m['target_id'],mode='runtime',
      current={'case_id':ident.get('case_id')})
  triggers.append({'target_id':m['target_id'],'fact_class':m['class'],'key_definition':predef,
      'failure_proof':source['route_failure_proof'] or source['catalytic_failure_proof'],
      'omission_locator':source['omission_locator'],'decision_id':'D-KEY4'})
 return {'applicable':bool(triggers),'confirmed_key_failure_cap':rules['d3a']['key_failure_cap'] if triggers else None,
         'triggers':triggers,'key_applicability_pending':pending,'key_registry_sha256':__import__('common_03a').sha((OUT/'KEY_DEFINITION_BINDINGS.json').read_bytes())}

def enforce_user_cap(score,cap):
 """Independent numeric hard gate; key_error=N or NE cannot erase a retained cap."""
 if cap['applicable'] and score is not None and (type(score) is not int or score>cap['confirmed_key_failure_cap']):
  raise ValueError('D-KEY4: numeric D3a must be <=4; critical-error flag cannot bypass user upper bound')

def decide(contract, rules=None):
 rules=rules or load(OUT/'SCORE_RULES_CANDIDATE.json')
 required={'original_N','original_scope_total','background_count','target_ids','targets','scope_status','key_definition_complete',
           'module_delivered','synthetic','independent_key_error'}
 if not isinstance(contract,dict) or required-set(contract):raise ValueError('candidate contract missing fields')
 n=contract['original_N']; rr=contract['targets']
 if type(n) is not int or n<=0 or type(contract['background_count']) is not int or contract['background_count']<0:raise ValueError('invalid denominator')
 if type(contract['original_scope_total']) is not int or contract['original_scope_total']!=n+contract['background_count']:raise ValueError('original target/background scope closure')
 if any(type(contract[k]) is not bool for k in ['key_definition_complete','module_delivered','synthetic']):raise ValueError('bad contract boolean')
 if contract['scope_status'] not in ['DEFINED_CANDIDATE','UNDEFINED','REFERENCE_HOLD']:raise ValueError('bad scope')
 ids=[x['target_id'] for x in rr]
 if len(rr)!=n or len(set(ids))!=n or set(ids)!=set(contract['target_ids']):raise ValueError('target/N closure or duplicate')
 current=None
 if not contract['synthetic']:
  # F03D-02: real consumption must state which frozen answer/case is being judged; missing or
  # cross-case identity fails closed (never falls back to comparing four class labels).
  ci=contract.get('consumer_identity')
  if not isinstance(ci,dict) or not all(ci.get(k) for k in ('b_slot_uid','case_id','answer_sha256')):
   raise ValueError('real contract missing consumer identity (slot/case/answer_sha)')
  if any(not t.startswith(ci['case_id']+'__') for t in ids):
   raise ValueError('consumer identity case does not cover contract targets')
  current=dict(ci)
  _bstat,_brsn=branch_gate(ci['case_id'],ci.get('current_path_id'))
 else:
  _bstat,_brsn='NONE',None
 mapped=[]
 for x in rr:
  c,sub=classify(x,contract['synthetic'],current);mapped.append({'target_id':x['target_id'],'class':c,'subtype':sub,'key':x['key'],'importance':x['importance']})
 counts={c:0 for c in 'SFMUH'};counts.update(Counter(x['class'] for x in mapped));assert sum(counts.values())==n
 keycap=user_key_cap(contract,mapped,rules)
 s,u,h=counts['S'],counts['U'],counts['H']
 key_all_supported=all(x['class']=='S' for x in mapped if x['key']) and any(x['key'] for x in mapped)
 high=(s==n and contract['key_definition_complete'] and key_all_supported and not any(a['status']!='SUPPORTED' and a.get('applies_to','D3a')=='D3a' for x in rr for a in x.get('claim_components',{}).get('additional_claims',[])))
 result={'status':'CANDIDATE_RANGE','score_status':'SCORED','allowed_range':None,'counts':counts,'original_N':n,
         'background_count':contract['background_count'],'original_scope_total':contract['original_scope_total'],'scope_status':contract['scope_status'],
         'confirmed_target_rate':s/n,'sensitivity_boundary':[s/n,(s+u)/n],
         'sensitivity_is_probability':False,'high_tier_eligible':high,'target_mapping':mapped,
         'reason':'','ne_basis':None,'ne_unverified':None,'counts_as_formal':False,'candidate_only':True,
         'user_key_failure_gate':keycap,'confirmed_key_failure_cap':keycap['confirmed_key_failure_cap']}
 def held(reason):
  result.update(status='REVIEW_PENDING',score_status='NE',allowed_range=None,high_tier_eligible=False,
                reason=reason,ne_basis=reason,ne_unverified=';'.join(x['target_id']+':'+x['subtype'] for x in mapped if x['class'] in 'UH') or reason)
  return result
 def judge_required(reason):
  # U is an automatic match result, not proof that the judge cannot evaluate
  # the actual answer using the supplied rubric and evidence.
  ceiling = rules['d3a']['major_failure_cap'] if any(
      x['importance']=='MAJOR' and x['class'] in ['F','M'] for x in mapped) else 8
  result.update(status='JUDGE_REQUIRED',score_status='JUDGE_REQUIRED',
                allowed_range=[1,ceiling],high_tier_eligible=False,reason=reason,
                ne_basis=None,ne_unverified=None,automatic_matching_only=True,
                unresolved_target_ids=[x['target_id'] for x in mapped if x['class'] in 'UH'])
  return result
 # Whole-module omission is established by the frozen answer, not by a
 # successful reference match or a selected branch.
 if not contract['module_delivered']:
  result.update(status='CANDIDATE_MISSING',score_status='MISSING',allowed_range=[1,1],
                reason='entire enzyme module not delivered; missing_basis required',
                module_delivery_locator=contract.get('module_delivery_locator','ANSWER.steps[*].enzyme'))
  return result
 # A verified KEY failure establishes a low scoring ceiling. Other automatic
 # unknowns are retained and cannot erase that already established failure.
 if keycap['applicable'] and not h and contract['scope_status']=='DEFINED_CANDIDATE':
  result.update(status='CANDIDATE_RANGE',score_status='SCORED',
                allowed_range=[1,keycap['confirmed_key_failure_cap']],high_tier_eligible=False,
                reason='confirmed KEY error/located omission: score within [1,4]; other automatic unknowns do not erase the known failure',
                ne_unverified=';'.join(x['target_id']+':'+x['subtype'] for x in mapped if x['class']=='U') or None,
                ne_basis='local unresolved claims retained; no supported credit inferred' if u else None)
  return result
 # MP-DAG-EXIT: top-level exit gate for branch scope, BEFORE any band/confirmation-rate/high-tier
 # publication. Covers S/F/M/U/H and whole-module states; never only the nested KEY F/M loop.
 if _bstat=='PENDING':return judge_required('reference branch not automatically bound; judge the task against adopted paths, never the graph union; genuine undecidable scope remains NE')
 if h or contract['scope_status']!='DEFINED_CANDIDATE':return held('reference/scope affects assessment; retain original N and H')
 if not contract['key_definition_complete']:return judge_required('automatic KEY applicability incomplete; assess the supplied task/evidence before deciding whether scientific uncertainty requires NE')
 if u:
  options={tuple(band(s+i,n,rules,high=False)) for i in range(u+1)}
  result['sensitivity_possible_current_bands']=[list(b) for b in sorted(options)]
  if any(x['class']=='U' and (x['key'] or x['importance']=='MAJOR') for x in mapped):return judge_required('automatic pair/alignment match unresolved; judge enzyme function and explicit EC using supplied evidence; genuine key uncertainty remains NE')
  if Fraction(u,n)>Fraction(str(rules['d3a']['max_minor_unknown_rate'])):return judge_required('automatic unknown proportion is not a scientific verdict; assess supplied evidence and retain genuine uncertainty')
  if len(options)!=1:return judge_required('automatic matches alone do not determine a band; judge supplied evidence without treating unmatched as false')
  result['allowed_range']=list(next(iter(options)))
  # For a good/high band, every predeclared major target must really be S.
  if result['allowed_range'][0]>=7 and any(x['importance']=='MAJOR' and x['class']!='S' for x in mapped):return held('major not fully supported for good band')
  result.update(reason='minor unknown cannot change restricted band; keep paired local ne fields',
                ne_basis='all permitted completions stay within same non-high band',
                ne_unverified=';'.join(x['target_id'] for x in mapped if x['class']=='U'))
 else:
  result['allowed_range']=band(s,n,rules,high=high)
  result['reason']='sufficiently determined target facts; interval only, integer requires cited judgement'
 major_failed=any(x['importance']=='MAJOR' and x['class'] in ['F','M'] for x in mapped)
 if major_failed and result['allowed_range'][1]>rules['d3a']['major_failure_cap']:
  result['allowed_range']=[min(result['allowed_range'][0],rules['d3a']['major_failure_range'][0]),rules['d3a']['major_failure_cap']]
  result['high_tier_eligible']=False
  result['reason']+='; predeclared KEY/MAJOR failure or material omission limits candidate band, not key_error attestation'
 supplementary=[a for x in rr for a in x.get('claim_components',{}).get('additional_claims',[]) if a['status']!='SUPPORTED' and a.get('applies_to','D3a')=='D3a']
 if any(a['materiality']=='MAJOR' for a in supplementary):return held('material experimental/protein/whole-strain claim unresolved; function component retained')
 if supplementary:
  cap=rules['d3a']['minor_annotation_pending_cap']
  result['allowed_range']=[min(result['allowed_range'][0],rules['d3a']['all_supported_but_gate_blocked_range'][0]),min(result['allowed_range'][1],cap)]
  result['high_tier_eligible']=False
  result['ne_basis']='supported target function/pair unchanged; predefined supplementary annotation cannot negate it, but high-band scope not fully closed'
  result['ne_unverified']=';'.join(a['claim_id']+':'+a['status'] for a in supplementary)
  result['reason']+='; supplementary attribution pending separately'
 result['supplementary_claims_pending']=supplementary
 result['cross_dimension_component_reviews']=[a for x in rr for a in x.get('claim_components',{}).get('additional_claims',[]) if a.get('applies_to','D3a')!='D3a' and a['status']!='SUPPORTED']
 if keycap['applicable']:
  lo,hi=result['allowed_range'];ceiling=keycap['confirmed_key_failure_cap']
  result['allowed_range']=[lo,min(hi,ceiling)] if lo<=ceiling else [1,ceiling]
  result['high_tier_eligible']=False
  result['reason']+='; USER_CONFIRMED D-KEY4 upper bound; high conflicting candidate band replaced by [1,4], not a fixed score'
 ke=contract['independent_key_error']
 if ke is not None:
  if not isinstance(ke,dict) or not all(ke.get(k) for k in ['dimension_failure','answer_locator','evidence_locator','support_scope']):raise ValueError('key error missing four elements')
  lo,hi=result['allowed_range']
  if lo>4:return held('independent main-failure finding conflicts with count band; review, no forced score')
  result['allowed_range']=[lo,min(hi,4)]
 return result

def dag_status(scope,submitted):
 """Synthetic/predeclared path checking only; not a new real route classifier."""
 if not scope.get('defined'):return 'BOUNDARY_REVIEW'
 nodes=submitted['nodes']; transitions=submitted['transitions']
 if not nodes:return 'MISSING'
 if nodes[0] not in scope['starts'] or nodes[-1] not in scope['ends']:return 'INCOMPLETE'
 if any((a,b) not in map(tuple,scope['edges']) for a,b in zip(nodes,nodes[1:])):return 'DISCONNECTED_OR_FOREIGN'
 if len(transitions)!=len(nodes)-1:return 'DISCONNECTED_OR_FOREIGN'
 actual=[scope['edge_transitions'][a+'->'+b] for a,b in zip(nodes,nodes[1:])]
 if transitions!=actual:return 'DISCONNECTED_OR_FOREIGN'
 if not set(scope['required_transitions'])<=set(actual):return 'MISSING_REQUIRED_TRANSFORMATION'
 return 'ALLOWED_MAIN_ROUTE'

def accepted_match(name,ec,pairs,pair_verified):
 """Frozen candidate set membership; never expands accepted or certifies chemistry."""
 hits=[p for p in pairs if p['name']==name and (ec is None or p['ec']==ec)]
 if hits and (ec is None or pair_verified):return 'SUPPORTED_MEMBERSHIP_AT_DECLARED_SCOPE'
 if any(p['name']==name for p in pairs) and ec is not None and not pair_verified:return 'PAIR_UNVERIFIED'
 return 'UNRESOLVED_NONACCEPTED'
