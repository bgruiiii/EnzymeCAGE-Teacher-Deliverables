"""03D-R1 real KEY registry loader (F03D-01 close-out).
Static registration verification checks each record against the ACTUAL sources: scope-row
membership (required vs background vs quarantine), role re-derived from the fixed graph,
DAG bindings resolved against THIS case's PATH_CATALOG/PATH_STEPS, non-empty role-aware
method basis. Runtime consumption additionally requires the current case/selected path.
Fail closed with concrete row locators. Nothing here re-derives chemistry."""
from pathlib import Path
from common_03a import OUT, R, load, sha

SCOPE = 'LIKERT_V05_REVISION_20261105_R2/P1_ROUTE_CHECK/CASE_TASK_SCOPE_120.tsv'
CATALOG = OUT/'PATH_CATALOG_03D.tsv'; STEPS = OUT/'PATH_STEPS_03D.tsv'
QUARANTINE = {'BIOPATH150_060', 'BIOPATH150_094'}
KEYDEF = 'D-KEYDEF-20261110'

_scope_cache = None
def _scope():
    global _scope_cache
    if _scope_cache is None:
        lines = (R/SCOPE).read_text().splitlines()
        hdr = lines[0].split('\t'); ix = {k:i for i,k in enumerate(hdr)}
        _scope_cache = {}
        for l in lines[1:]:
            f = l.split('\t'); cid = f[ix['case_id']]
            _scope_cache[cid] = {'required': [x for x in f[ix['required_step_ids']].split('|') if x],
                                 'background': [x for x in f[ix['background_step_ids']].split('|') if x],
                                 'graph_status': f[ix['graph_status']],
                                 'disposition': f[ix['disposition_status']],
                                 'row_sha': sha(l.encode())}
    return _scope_cache

_graph_cache = {}
def _graph(case_id):
    if case_id not in _graph_cache:
        p = R/('LIKERT_V05_RELEASE_20261108/S0_INTEGRATION/gold_slices/'+case_id+'/reaction_gold.tsv')
        lines = p.read_text().splitlines(); hdr = lines[0].split('\t')
        ix = {k:i for i,k in enumerate(hdr)}
        per = {}
        for l in lines[1:]:
            f = l.split('\t'); sid = f[ix['step_occurrence_id']]
            e = per.setdefault(sid, {'raw': [], 'succ': set(), 'pred': set(), 'orient': f[ix['gold_orientation']]})
            e['raw'].append(l)
            e['succ'] |= {x for x in f[ix['successor_step_ids']].split('|') if x}
            e['pred'] |= {x for x in f[ix['predecessor_step_ids']].split('|') if x}
        _graph_cache[case_id] = per
    return _graph_cache[case_id]

def _linear_role(case_id, full_id):
    sc = _scope()[case_id]; inscope = {x.split('__')[1] for x in sc['required']}
    g = _graph(case_id)[full_id]
    if not [x for x in g['pred'] if x.split('__')[1] in inscope]: return 'ENTRY'
    if not [x for x in g['succ'] if x.split('__')[1] in inscope]: return 'TERMINAL'
    return 'MANDATORY_INTERMEDIATE_IN_MAIN_CHAIN'

def _rows(path):
    lines = Path(path).read_text().splitlines(); hdr = lines[0].split('\t')
    return [dict(zip(hdr, l.split('\t'))) for l in lines[1:]]

_cat_cache = _step_cache = None
def _path_index():
    global _cat_cache, _step_cache
    if _cat_cache is None:
        _cat_cache = {}
        for r in _rows(CATALOG):
            _cat_cache.setdefault(r['case_id'], {})[r['path_id']] = r
        _step_cache = {}
        for r in _rows(STEPS):
            _step_cache.setdefault((r['case_id'], r['path_id']), {})[r['gold_step_id']] = r
    return _cat_cache, _step_cache

def branch_gate(case_id, selected_path_id):
    """MP-DAG-EXIT top-level state gate used by decide() for real contracts.
    Returns ('PENDING', reason) when a branch case has no current selected main chain bound;
    raises for an invalid/HELD/wrong-case selected path (invalid contract, fail closed);
    ('NONE', None) for linear cases. Scope truth comes from the pinned CASE_TASK_SCOPE_120 row,
    never from a caller-reported scope_status claim."""
    sc = _scope().get(case_id)
    if sc is None:
        raise ValueError('case absent from pinned scope table: '+case_id)
    if sc['graph_status'] != 'BRANCHED_DAG':
        return ('NONE', None)
    if not selected_path_id:
        return ('PENDING', 'branch case: current selected main chain not bound (pinned scope graph_status=BRANCHED_DAG); D3a target-set mapping pending; no union-based M/confirmation-rate/high-tier')
    cat_idx, _ = _path_index()
    paths = cat_idx.get(case_id, {})
    if selected_path_id not in paths:
        raise ValueError('selected path '+selected_path_id+' is not a path of case '+case_id)
    if paths[selected_path_id]['adoption_status'] != 'ADOPTED_METHOD_CONFIRMED':
        raise ValueError('selected path '+selected_path_id+' not adopted for case '+case_id+' (HELD paths are not consumable)')
    return ('OK', None)

def verify_real_key_record(rec, registry, target_id, mode='static', current=None):
    """Raises ValueError with the failing locator; returns rec when fully bound.
    mode='static': registration applicability (no answer involved).
    mode='runtime': additionally requires the running contract's current binding dict
    (case for linear; case + selected adopted path for DAG)."""
    if rec.get('status') != 'METHOD_CONFIRMED_SCOPE_BOUND':
        raise ValueError('KEY record '+target_id+' not consumable (status '+str(rec.get('status'))+')')
    for k in ('case_id','gold_step_id','gold_short','gold_reaction_id','gold_direction',
              'scope_row_sha256','role','decision_ids','scope_source','graph_source'):
        if k not in rec: raise ValueError('KEY record '+target_id+' missing field '+k)
    if target_id != '%s__%s__%s'%(rec['case_id'],rec['gold_short'],rec['gold_reaction_id']):
        raise ValueError('KEY record composite identity mismatch at '+target_id)
    if registry.get('confirmed_real_keys', {}).get(target_id) != rec:
        raise ValueError('KEY record not registered under this exact composite key at '+target_id)
    if target_id in registry.get('held_real_keys', {}):
        raise ValueError('target present in held register contradicts confirmed at '+target_id)
    ledger = registry['decision_ledger']
    if not rec['decision_ids']:
        raise ValueError('empty method basis on '+target_id)
    for dec in rec['decision_ids']:
        if dec not in ledger: raise ValueError('unregistered decision '+dec+' on '+target_id)
        ent = ledger[dec]; p = R/ent['path']
        if not p.is_file() or sha(p.read_bytes()) != ent['sha256']:
            raise ValueError('decision source absent/changed '+dec+' for '+target_id)
    # Method basis must be complete: D-KEYDEF defines the KEY scope (incl. intermediates),
    # D-KEY4 is the consumption rule; both must be bound on every consumable record.
    for need in (KEYDEF, 'D-KEY4'):
        if need not in rec['decision_ids']:
            raise ValueError('KEY record missing required method basis '+need+' at '+target_id)
    if rec['case_id'] in QUARANTINE:
        raise ValueError('quarantined case cannot confirm KEY at '+target_id)
    sc = _scope().get(rec['case_id'])
    if sc is None: raise ValueError('case absent from pinned scope table: '+rec['case_id'])
    if target_id in sc['background']:
        raise ValueError('background step registered as consumable KEY at '+target_id+' (scope row is authoritative)')
    if target_id not in sc['required']:
        raise ValueError('step outside pinned required scope at '+target_id)
    if sc['row_sha'] != rec['scope_row_sha256']:
        raise ValueError('scope row sha mismatch '+target_id)
    st = registry['scope_table']; p = R/st['path']
    if sha(p.read_bytes()) != st['sha256']: raise ValueError('scope table changed '+target_id)
    g = rec['graph_source']; gp = R/g['path']
    if not gp.is_file() or sha(gp.read_bytes()) != g['file_sha256']:
        raise ValueError('graph source absent/changed '+target_id+' ('+g['path']+')')
    if ('/'+rec['case_id']+'/') not in ('/'+g['path']):
        raise ValueError('graph file belongs to a different case at '+target_id)
    if rec['scope_source'].get('case', rec['case_id']) != rec['case_id']:
        raise ValueError('scope_source case mismatch '+target_id)
    if sc['graph_status'] == 'BRANCHED_DAG':
        if not rec.get('scope_kind','').startswith('PATH_CATALOG'):
            raise ValueError('branch case record must bind adopted path catalog at '+target_id)
        pb = rec.get('path_bindings') or []
        if not pb: raise ValueError('DAG KEY record without adopted-path binding '+target_id)
        src_sha=rec.get('scope_source',{}).get('path_sha256')
        catf=C.OUT/rel_cat if False else OUT/'PATH_CATALOG_03D.tsv'
        if src_sha != sha(catf.read_bytes()):
            raise ValueError('catalog file sha not bound in scope_source at '+target_id)
        cat_idx, step_idx = _path_index()
        roles = set()
        for b in pb:
            paths = cat_idx.get(rec['case_id'], {})
            if b['path_id'] not in paths:
                raise ValueError('path '+b['path_id']+' is not a path of case '+rec['case_id']+' (binding '+target_id+')')
            prow = paths[b['path_id']]
            if prow['adoption_status'] != 'ADOPTED_METHOD_CONFIRMED':
                raise ValueError('bound path not adopted at '+target_id+' ('+b['path_id']+')')
            srow = step_idx.get((rec['case_id'], b['path_id']), {}).get(target_id)
            if srow is None:
                raise ValueError('target step not contained in bound path '+b['path_id']+' of case '+rec['case_id'])
            if b.get('step_row_sha256') != srow['step_row_sha256']:
                raise ValueError('path step row sha mismatch '+target_id+' on '+b['path_id'])
            if b.get('role_in_path') != srow['role_in_path']:
                raise ValueError('path role differs from catalog '+target_id+' on '+b['path_id'])
            if srow['gold_orientation'] and srow['gold_orientation'] != rec['gold_direction']:
                raise ValueError('path direction differs from record at '+target_id)
            roles.add(srow['role_in_path'])
        expected_role = next(iter(roles)) if len(roles) == 1 else 'MULTI_ROLE:'+'+'.join(sorted(roles))
        if rec['role'] != expected_role:
            raise ValueError('DAG role not re-derivable from THIS case catalog at '+target_id+' (record '+rec['role']+', catalog '+expected_role+')')
        if mode == 'runtime':
            if not current or not current.get('selected_path_id'):
                raise ValueError('runtime DAG consumption requires current selected path '+target_id)
            if current.get('case_id') != rec['case_id']:
                raise ValueError('runtime DAG case mismatch '+target_id)
            if current['selected_path_id'] not in [b['path_id'] for b in pb]:
                raise ValueError('selected path '+current['selected_path_id']+' not among record bindings '+target_id)
    else:
        if rec.get('scope_kind','').startswith('LINEAR'):
            if 'gold_row_sha256' not in rec:
                raise ValueError('linear KEY record without slice row hash '+target_id)
            matched = [l for l in _slice_lines(g['path']) if l.split('\t')[2] == target_id]
            if not matched: raise ValueError('step row absent in bound graph file '+target_id)
            if sha('\n'.join(matched).encode()) != rec['gold_row_sha256']:
                raise ValueError('graph step row changed '+target_id)
            if any(l.split('\t')[9] != rec['gold_direction'] for l in matched):
                raise ValueError('graph orientation differs from KEY record '+target_id)
            derived = _linear_role(rec['case_id'], target_id)
            if rec['role'] != derived:
                raise ValueError('role not re-derivable from fixed graph at '+target_id+' (record '+rec['role']+', graph '+derived+')')
            if mode == 'runtime':
                if not current or current.get('case_id') != rec['case_id']:
                    raise ValueError('runtime consumption requires current case binding '+target_id)
        else:
            raise ValueError('non-branch record must use LINEAR scope kind at '+target_id)
    return rec

_slice_cache = {}
def _slice_lines(path):
    if path not in _slice_cache:
        _slice_cache[path] = (R/path).read_text().splitlines()[1:]
    return _slice_cache[path]
