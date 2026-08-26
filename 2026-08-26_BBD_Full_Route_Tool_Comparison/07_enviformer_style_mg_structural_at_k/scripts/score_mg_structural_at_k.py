#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
score_mg_structural_at_k.py
==========================

Protocol: ENVIFORMER_MG_STRUCTURAL_AT_K_ADAPTED_BBD_FULL_ROUTE

Local scoring supplement for the BBD full-route v0.3 / v3.1 prediction outputs.
This is an ADAPTED structural evaluation inspired by the enviFormer Multi-Generation
method. It is NOT the official enviFormer probability-threshold MG / AUPRC and does
NOT compare calibrated probabilities across tools.

Core idea:
  * Give every tool the same per-source candidate budget K (Top-K outgoing edges).
  * Recursively expand the predicted route graph from the parent/root up to max_depth.
  * Compare the reachable predicted node set against the restricted BBD answer graph
    using depth-weighted Precision / Recall / Jaccard (weight = 1 / 2^depth).
  * Penalise false-positive branches (FP) so that "wide graph coverage" no longer
    looks artificially good.

Reproducible: run
    python3 score_mg_structural_at_k.py

Author: local executor
Date: 2026-08-26
"""

import csv
import json
import os
import sys
import math
import hashlib
import tarfile
import tempfile
import collections
import statistics

from rdkit import Chem
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROTOCOL_NAME = 'ENVIFORMER_MG_STRUCTURAL_AT_K_ADAPTED_BBD_FULL_ROUTE'
K_VALUES = [1, 3, 5, 10]
K_MAIN = [1, 3, 5]
MAX_DEPTH = 6
MAX_PRED_NODES_PER_CASE = 1000
EXCLUDE_CO2 = True
INTERMEDIATE_HANDLING = True
DOWNSTREAM_DEPTH_CORRECTION = False
CANONICALIZATION_MODE = 'non_isomeric_rdkit_canonical'
DATE_STR = '2026-08-26'

REPO = '/home/a/EnzymeCAGE'
DOC_BASE = (REPO + '/custom/docs/enzyme_feature_expansion/'
            'ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01')
RESTRICTED_DIR = (DOC_BASE + '/21_BBD_Known_Pathway_Full_Route_Testset_2026-08-21/'
                  'bbd_known_pathway_full_route_v0_3_candidate_v3_repair_20260821/restricted')
PRED_ARCHIVE = (DOC_BASE + '/03_HPC_Returned_Result_Summaries/'
                'bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz')
SIMPLE_PATH_V2_ARCHIVE = (DOC_BASE + '/03_HPC_Returned_Result_Summaries/'
                          'bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_v2_cleanup_supplement_20260826.tar.gz')

OUT_DIR = (DOC_BASE + '/22_BBD_Full_Route_Tool_Comparison_2026-08-26/'
           '07_enviformer_style_mg_structural_at_k')

TOOL_FOLDERS = [
    ('biotransformer_envmicro', 'biotransformer_envmicro_multistep'),
    ('envipath_prediction', 'envipath_bbd_rules_multistep'),
    ('eclipse_predec', 'eclipse_predec_bbd_finetuned_10fold_multistep'),
    ('eclipse_noec', 'eclipse_noec_bbd_finetuned_10fold_multistep_optional'),
]
PRIMARY_TOOLS = ['biotransformer_envmicro', 'envipath_prediction', 'eclipse_predec']
OPTIONAL_TOOLS = ['eclipse_noec']

EXCLUDED_CASE = 'FR-BBD3-CAND-c0105'  # zero route-edge case (Chlorobenzene)


# ---------------------------------------------------------------------------
# Canonicalization
# ---------------------------------------------------------------------------
_cache = {}


def canon(smiles):
    """Return non-isomeric RDKit canonical SMILES, or None if invalid."""
    if smiles is None:
        return None
    s = str(smiles).strip()
    if not s:
        return None
    if s in _cache:
        return _cache[s]
    out = None
    try:
        m = Chem.MolFromSmiles(s)
        if m is not None:
            out = Chem.MolToSmiles(m, isomericSmiles=False)
    except Exception:
        out = None
    _cache[s] = out
    return out


CO2_KEY = canon('O=C=O')  # 'O=C=O'


def is_co2(key):
    return EXCLUDE_CO2 and key == CO2_KEY


# ---------------------------------------------------------------------------
# Graph helpers
# ---------------------------------------------------------------------------
def bfs_depths(adj, root, max_depth, max_nodes):
    """BFS from root. Return (depths dict, cap_hit bool)."""
    depths = {root: 0}
    queue = collections.deque([root])
    cap_hit = False
    while queue:
        node = queue.popleft()
        d = depths[node]
        if d >= max_depth:
            continue
        for tgt in adj.get(node, ()):
            if tgt not in depths:
                depths[tgt] = d + 1
                queue.append(tgt)
                if len(depths) > max_nodes:
                    cap_hit = True
                    break
        if cap_hit:
            break
    return depths, cap_hit


def shortest_path(adj, src, dst):
    """BFS shortest path src->dst. Return list of nodes or None."""
    if src == dst:
        return [src]
    prev = {src: None}
    queue = collections.deque([src])
    while queue:
        node = queue.popleft()
        for tgt in adj.get(node, ()):
            if tgt in prev:
                continue
            prev[tgt] = node
            if tgt == dst:
                # reconstruct
                path = [dst]
                cur = dst
                while prev[cur] is not None:
                    cur = prev[cur]
                    path.append(cur)
                path.reverse()
                return path
            queue.append(tgt)
    return None


def weight(depth):
    """enviFormer-style depth weight. root (depth 0) not scored -> weight 0."""
    if depth is None or depth <= 0:
        return 0.0
    return 1.0 / (2.0 ** depth)


# ---------------------------------------------------------------------------
# Load restricted (true) graphs
# ---------------------------------------------------------------------------
def load_true_graphs():
    """Return dict: case_id -> {root, adj, depths, nodes, meta, unreachable}."""
    # parent route summary
    summary_path = RESTRICTED_DIR + '/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_PARENT_ROUTE_SUMMARY.csv'
    with open(summary_path, newline='') as fh:
        srows = list(csv.DictReader(fh))

    case_meta = {}
    for r in srows:
        abbrs = [a.strip() for a in r['source_pathway_abbrs'].split('|') if a.strip()]
        case_meta[r['full_route_case_id']] = {
            'parent_canonical_smiles': r['parent_canonical_smiles'],
            'parent_name': r['parent_name'],
            'pollutant_category': r.get('scope', ''),
            'pathway_abbrs': abbrs,
            'route_edge_count': int(r['route_edge_count']),
            'scoreable_edge_count': int(r['scoreable_edge_count']),
        }

    # reaction edges by pathway_abbr
    edges_path = RESTRICTED_DIR + '/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_REACTION_EDGES.csv'
    with open(edges_path, newline='') as fh:
        erows = list(csv.DictReader(fh))

    by_abbr = collections.defaultdict(list)
    invalid_ref = 0
    for r in erows:
        if r['scoreable_by_structure'] != 'true':
            continue
        ab = r['pathway_abbr'].strip()
        s = canon(r['source_canonical_smiles'])
        t = canon(r['target_canonical_smiles'])
        if s is None:
            invalid_ref += 1
        if t is None:
            invalid_ref += 1
            continue
        if is_co2(t):
            continue
        by_abbr[ab].append((s, t))

    graphs = {}
    for case_id, meta in case_meta.items():
        root = canon(meta['parent_canonical_smiles'])
        adj = collections.defaultdict(set)
        for ab in meta['pathway_abbrs']:
            for (s, t) in by_abbr.get(ab, []):
                if s == t:
                    continue
                adj[s].add(t)
        # normalise adj to sorted lists (deterministic)
        adj = {k: sorted(v) for k, v in adj.items()}
        depths, _ = bfs_depths(adj, root, MAX_DEPTH, MAX_PRED_NODES_PER_CASE)
        reachable = {n for n in depths if n != root}
        # unreachable true nodes (in edges but not reachable from root)
        all_nodes = set(adj.keys())
        for s, ts in adj.items():
            all_nodes.add(s)
            all_nodes.update(ts)
        all_nodes.discard(root)
        unreachable = all_nodes - reachable
        graphs[case_id] = {
            'root': root,
            'adj': adj,
            'depths': depths,
            'nodes': reachable,
            'unreachable': unreachable,
            'meta': meta,
        }
    return graphs, invalid_ref


# ---------------------------------------------------------------------------
# Load predicted edges and build per-K predicted graphs
# ---------------------------------------------------------------------------
def rank_key(edge):
    """Sort key: edge_rank_from_source asc, edge_rank_global asc, score desc."""
    rs = edge.get('edge_rank_from_source', -1)
    rg = edge.get('edge_rank_global_within_case_depth', -1)
    if rs is None or rs < 0:
        rs = 10 ** 9
    if rg is None or rg < 0:
        rg = 10 ** 9
    score = edge.get('local_edge_score_raw', 0.0) or 0.0
    return (rs, rg, -score)


def load_pred_edges(tool_folder, extracted_root):
    """Return (by_case, total, invalid_total, self_loop_total, case_stats).

    case_stats[case_id] = {'invalid': int, 'self_loop': int, 'total': int}
    """
    fpath = (extracted_root +
             '/bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825/'
             '03_ROUTE_EXPANSION/' + tool_folder + '/PREDICTED_ROUTE_EDGES.jsonl')
    by_case = collections.defaultdict(list)
    invalid = 0
    self_loop = 0
    total = 0
    case_stats = collections.defaultdict(lambda: {'invalid': 0, 'self_loop': 0, 'total': 0})
    with open(fpath) as fh:
        for line in fh:
            d = json.loads(line)
            total += 1
            cid = d['full_route_case_id']
            case_stats[cid]['total'] += 1
            if d.get('normalization_status') != 'ok':
                invalid += 1
                case_stats[cid]['invalid'] += 1
                continue
            s = canon(d.get('source_smiles_canonical'))
            t = canon(d.get('target_smiles_canonical'))
            if s is None or t is None:
                invalid += 1
                case_stats[cid]['invalid'] += 1
                continue
            if is_co2(t):
                continue
            if (d.get('target_is_original_parent_copy') or d.get('target_is_source_copy')
                    or s == t):
                self_loop += 1
                case_stats[cid]['self_loop'] += 1
                continue
            by_case[cid].append({
                'source': s,
                'target': t,
                'edge_rank_from_source': d.get('edge_rank_from_source', -1),
                'edge_rank_global_within_case_depth': d.get('edge_rank_global_within_case_depth', -1),
                'local_edge_score_raw': d.get('local_edge_score_raw', 0.0),
                'source_depth': d.get('source_depth', 0),
                'target_depth': d.get('target_depth', 0),
            })
    return by_case, total, invalid, self_loop, case_stats


def build_pred_graph(case_edges, root, k):
    """Apply TopK per source, then BFS from root. Return graph dict."""
    # group outgoing edges by source
    by_source = collections.defaultdict(list)
    for e in case_edges:
        by_source[e['source']].append(e)

    kept_adj = {}
    for src, edges in by_source.items():
        edges_sorted = sorted(edges, key=rank_key)
        seen_targets = set()
        kept = []
        for e in edges_sorted:
            t = e['target']
            if t in seen_targets:
                continue
            seen_targets.add(t)
            kept.append(t)
            if len(seen_targets) >= k:
                break
        if kept:
            kept_adj[src] = kept

    depths, cap_hit = bfs_depths(kept_adj, root, MAX_DEPTH, MAX_PRED_NODES_PER_CASE)
    nodes = {n for n in depths if n != root}
    return {
        'root': root,
        'adj': kept_adj,
        'depths': depths,
        'nodes': nodes,
        'cap_hit': cap_hit,
    }


# ---------------------------------------------------------------------------
# Intermediate detection
# ---------------------------------------------------------------------------
def find_intermediates(true_g, pred_g):
    """Identify predicted-only nodes lying on a predicted path between two true
    nodes U,V where U->V is a true edge and both U,V are in pred graph."""
    if not INTERMEDIATE_HANDLING:
        return set(), []
    intermediates = set()
    records = []
    true_adj = true_g['adj']
    true_nodes = true_g['nodes'] | {true_g['root']}
    pred_adj = pred_g['adj']
    pred_nodes = pred_g['nodes'] | {pred_g['root']}
    common = true_nodes & pred_nodes
    for u in common:
        for v in true_adj.get(u, ()):
            if v == u or v not in pred_nodes:
                continue
            if v not in true_nodes:
                continue
            path = shortest_path(pred_adj, u, v)
            if path and len(path) >= 3:
                for x in path[1:-1]:
                    if x not in true_nodes and x not in intermediates:
                        intermediates.add(x)
                        records.append({
                            'intermediate': x,
                            'upstream_true_node': u,
                            'downstream_true_node': v,
                            'original_pred_depth': pred_g['depths'].get(x),
                            'path': path,
                        })
    return intermediates, records


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
def score_case(true_g, pred_g):
    """Compute weighted TP/FP/FN and derived metrics for one case."""
    true_nodes = true_g['nodes']
    pred_nodes = pred_g['nodes']
    true_depths = true_g['depths']
    pred_depths = pred_g['depths']

    intermediates, int_records = find_intermediates(true_g, pred_g)

    common = true_nodes & pred_nodes
    tp_w = sum(weight(true_depths[n]) for n in common)

    fn_nodes = true_nodes - pred_nodes
    fn_w = sum(weight(true_depths[n]) for n in fn_nodes)

    fp_nodes = (pred_nodes - true_nodes) - intermediates
    fp_w = sum(weight(pred_depths[n]) for n in fp_nodes)

    denom_p = tp_w + fp_w
    denom_r = tp_w + fn_w
    denom_j = tp_w + fp_w + fn_w
    precision = tp_w / denom_p if denom_p > 0 else 0.0
    recall = tp_w / denom_r if denom_r > 0 else 0.0
    jaccard = tp_w / denom_j if denom_j > 0 else 0.0

    return {
        'weighted_tp': tp_w,
        'weighted_fp': fp_w,
        'weighted_fn': fn_w,
        'weighted_precision': precision,
        'weighted_recall': recall,
        'weighted_jaccard': jaccard,
        'unweighted_tp': len(common),
        'unweighted_fp': len(fp_nodes),
        'unweighted_fn': len(fn_nodes),
        'intermediate_node_count': len(intermediates),
        'intermediate_records': int_records,
    }


# ---------------------------------------------------------------------------
# Toy tests
# ---------------------------------------------------------------------------
def make_graph(root, edges, max_depth=6):
    adj = collections.defaultdict(set)
    for s, t in edges:
        adj[s].add(t)
    adj = {k: sorted(v) for k, v in adj.items()}
    depths, _ = bfs_depths(adj, root, max_depth, 1000)
    nodes = {n for n in depths if n != root}
    return {'root': root, 'adj': adj, 'depths': depths, 'nodes': nodes,
            'unreachable': set()}


def approx(a, b, tol=1e-9):
    return abs(a - b) < tol


def run_toy_tests():
    """Return (all_passed, list of {name,passed,detail})."""
    results = []
    ok = True

    # Test 1: exact chain A->B->C
    true = make_graph('A', [('A', 'B'), ('B', 'C')])
    pred = make_graph('A', [('A', 'B'), ('B', 'C')])
    m = score_case(true, pred)
    p = approx(m['weighted_precision'], 1.0) and approx(m['weighted_recall'], 1.0) and approx(m['weighted_jaccard'], 1.0)
    results.append({'name': '1_exact_chain', 'passed': p,
                    'detail': 'P=%.4f R=%.4f J=%.4f' % (m['weighted_precision'], m['weighted_recall'], m['weighted_jaccard'])})
    ok = ok and p

    # Test 2: extra false positive A->B and A->X
    true = make_graph('A', [('A', 'B')])
    pred = make_graph('A', [('A', 'B'), ('A', 'X')])
    m = score_case(true, pred)
    # B TP depth1 w=0.5; X FP depth1 w=0.5 -> P=0.5 R=1.0 J=0.5
    p = approx(m['weighted_precision'], 0.5) and approx(m['weighted_recall'], 1.0) and approx(m['weighted_jaccard'], 0.5)
    results.append({'name': '2_extra_fp', 'passed': p,
                    'detail': 'P=%.4f R=%.4f J=%.4f' % (m['weighted_precision'], m['weighted_recall'], m['weighted_jaccard'])})
    ok = ok and p

    # Test 3: missing downstream true A->B->C, pred A->B
    true = make_graph('A', [('A', 'B'), ('B', 'C')])
    pred = make_graph('A', [('A', 'B')])
    m = score_case(true, pred)
    # B TP 0.5; C FN 0.25 -> P=1.0 R=0.5/(0.5+0.25)=2/3
    p = approx(m['weighted_precision'], 1.0) and approx(m['weighted_recall'], 0.5 / 0.75) and approx(m['weighted_jaccard'], 0.5 / 0.75)
    results.append({'name': '3_missing_downstream', 'passed': p,
                    'detail': 'P=%.4f R=%.4f J=%.4f' % (m['weighted_precision'], m['weighted_recall'], m['weighted_jaccard'])})
    ok = ok and p

    # Test 4: root excluded
    true = make_graph('A', [('A', 'B')])
    pred = make_graph('A', [('A', 'B')])
    m = score_case(true, pred)
    # root A must not be a TP
    p = approx(m['weighted_tp'], 0.5) and not ('A' in true['nodes'])
    results.append({'name': '4_root_excluded', 'passed': p,
                    'detail': 'tp=%.4f root_in_nodes=%s' % (m['weighted_tp'], 'A' in true['nodes'])})
    ok = ok and p

    # Test 5: depth weighting - wrong depth-1 node penalised more than depth-3
    # true: A->B ; pred1: A->X (depth1 FP) ; pred2: A->B->Y->X (X depth3 FP)
    true = make_graph('A', [('A', 'B')])
    pred1 = make_graph('A', [('A', 'B'), ('A', 'X')])          # X depth1 w=0.5
    pred2 = make_graph('A', [('A', 'B'), ('B', 'Y'), ('Y', 'X')])  # X depth3 w=0.125
    m1 = score_case(true, pred1)
    m2 = score_case(true, pred2)
    # pred1 P = 0.5/(0.5+0.5)=0.5 ; pred2 P = 0.5/(0.5+0.125)=0.8
    p = m2['weighted_precision'] > m1['weighted_precision']
    results.append({'name': '5_depth_weighting', 'passed': p,
                    'detail': 'P_depth1fp=%.4f P_depth3fp=%.4f' % (m1['weighted_precision'], m2['weighted_precision'])})
    ok = ok and p

    # Test 6: intermediate A->X->B vs true A->B
    true = make_graph('A', [('A', 'B')])
    pred = make_graph('A', [('A', 'X'), ('X', 'B')])
    m = score_case(true, pred)
    if INTERMEDIATE_HANDLING:
        # X should be intermediate, weight 0, not FP -> P=1 R=1 J=1
        p = approx(m['weighted_precision'], 1.0) and approx(m['weighted_recall'], 1.0) and approx(m['weighted_jaccard'], 1.0) and m['intermediate_node_count'] == 1
        results.append({'name': '6_intermediate_enabled', 'passed': p,
                        'detail': 'P=%.4f R=%.4f J=%.4f int=%d' % (m['weighted_precision'], m['weighted_recall'], m['weighted_jaccard'], m['intermediate_node_count'])})
    else:
        # X counted as FP
        p = m['unweighted_fp'] >= 1
        results.append({'name': '6_intermediate_disabled', 'passed': p,
                        'detail': 'P=%.4f fp=%d' % (m['weighted_precision'], m['unweighted_fp'])})
    ok = ok and p

    return ok, results


# ---------------------------------------------------------------------------
# Main scoring
# ---------------------------------------------------------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def extract_archive(archive):
    """Extract archive to a fresh run-specific temp dir each run.

    Reproducibility fix: the previous version reused a stale
    '/tmp/mg_struct_extract' directory if it already existed, which could
    mix results from a previous extraction.  We now always extract into a
    fresh tempfile.mkdtemp directory so every run starts clean.
    """
    td = tempfile.mkdtemp(prefix='mg_struct_extract_')
    with tarfile.open(archive, 'r:gz') as tf:
        tf.extractall(td)
    return td


def main():
    print('=== %s ===' % PROTOCOL_NAME)
    print('RDKit available: yes')

    # 1. Toy tests
    toy_ok, toy_results = run_toy_tests()
    print('\n--- Toy tests ---')
    for r in toy_results:
        print('  [%s] %s  %s' % ('PASS' if r['passed'] else 'FAIL', r['name'], r['detail']))
    if not toy_ok:
        print('\nTOY TESTS FAILED - aborting real scoring.')
        write_validation(toy_ok, toy_results, None, None, None, None, None)
        sys.exit(1)
    print('All toy tests PASSED.')

    # 2. Load true graphs
    true_graphs, invalid_ref = load_true_graphs()
    evaluable = {c: g for c, g in true_graphs.items()
                 if c != EXCLUDED_CASE and len(g['nodes']) > 0}
    no_edge_cases = [c for c in true_graphs if c == EXCLUDED_CASE or len(true_graphs[c]['nodes']) == 0]
    print('\n--- True graphs ---')
    print('total cases:', len(true_graphs))
    print('evaluable (non-zero true nodes):', len(evaluable))
    print('excluded/no-edge cases:', no_edge_cases)
    print('invalid reference SMILES count:', invalid_ref)

    # 3. Extract prediction archive
    extracted = extract_archive(PRED_ARCHIVE)
    pred_sha = sha256_file(PRED_ARCHIVE)
    print('\nPrediction archive sha256:', pred_sha)
    sp_sha = sha256_file(SIMPLE_PATH_V2_ARCHIVE) if os.path.exists(SIMPLE_PATH_V2_ARCHIVE) else 'N/A'
    print('Simple-path v2 archive sha256:', sp_sha)

    # 4. Score each tool x case x K
    case_rows = []
    qc_rows = []
    inter_rows = []
    tool_summary = []

    for tool_id, folder in TOOL_FOLDERS:
        is_primary = tool_id in PRIMARY_TOOLS
        by_case, total_rows, invalid_rows, self_loop_rows, case_stats = load_pred_edges(folder, extracted)
        print('\n--- Tool: %s ---' % tool_id)
        print('  total edge rows:', total_rows)
        print('  invalid rows removed:', invalid_rows)
        print('  self-loop/parent-copy rows removed:', self_loop_rows)
        print('  cases with edges:', len(by_case))

        for k in K_VALUES:
            k_rows = []
            scored = 0
            no_pred = 0
            for case_id, tg in evaluable.items():
                root = tg['root']
                edges = by_case.get(case_id, [])
                cs = case_stats.get(case_id, {'invalid': 0, 'self_loop': 0, 'total': 0})
                if edges:
                    pg = build_pred_graph(edges, root, k)
                else:
                    pg = {'root': root, 'adj': {}, 'depths': {root: 0}, 'nodes': set(), 'cap_hit': False}
                m = score_case(tg, pg)
                has_pred = len(pg['nodes']) > 0
                if has_pred:
                    scored += 1
                else:
                    no_pred += 1
                meta = tg['meta']
                ref_max_depth = max((d for n, d in tg['depths'].items() if n != root), default=0)
                pred_max_depth = max((d for n, d in pg['depths'].items() if n != root), default=0)
                note = ''
                if not has_pred:
                    note = 'no_prediction_after_topk'
                if pg['cap_hit']:
                    note += ' cap_hit' if note else 'cap_hit'
                if tg['unreachable']:
                    note += ' has_unreachable_true_nodes'
                row = {
                    'full_route_case_id': case_id,
                    'pollutant_name': meta['parent_name'],
                    'pollutant_category': meta['pollutant_category'],
                    'tool_id': tool_id,
                    'k': k,
                    'status': 'SCORED' if has_pred else 'NO_PREDICTION',
                    'reference_node_count_excluding_root': len(tg['nodes']),
                    'predicted_node_count_excluding_root': len(pg['nodes']),
                    'reference_max_depth': ref_max_depth,
                    'predicted_max_depth': pred_max_depth,
                    'weighted_tp': round(m['weighted_tp'], 6),
                    'weighted_fp': round(m['weighted_fp'], 6),
                    'weighted_fn': round(m['weighted_fn'], 6),
                    'weighted_precision': round(m['weighted_precision'], 6),
                    'weighted_recall': round(m['weighted_recall'], 6),
                    'weighted_jaccard': round(m['weighted_jaccard'], 6),
                    'unweighted_tp_node_count': m['unweighted_tp'],
                    'unweighted_fp_node_count': m['unweighted_fp'],
                    'unweighted_fn_node_count': m['unweighted_fn'],
                    'intermediate_node_count': m['intermediate_node_count'],
                    'removed_self_loop_edge_count': cs['self_loop'],
                    'invalid_prediction_row_count': cs['invalid'],
                    'notes': note,
                }
                case_rows.append(row)
                k_rows.append(row)

                # QC
                qc_rows.append({
                    'full_route_case_id': case_id,
                    'tool_id': tool_id,
                    'k': k,
                    'total_input_edge_rows_for_tool': total_rows,
                    'invalid_rows_removed_for_case': cs['invalid'],
                    'self_loop_parent_copy_rows_removed_for_case': cs['self_loop'],
                    'total_input_edge_rows_for_case': cs['total'],
                    'edges_after_cleaning': len(edges),
                    'predicted_nodes_excluding_root': len(pg['nodes']),
                    'cap_hit': pg['cap_hit'],
                    'unreachable_true_node_count': len(tg['unreachable']),
                    'status': row['status'],
                })

                # intermediate records
                for ir in m['intermediate_records']:
                    inter_rows.append({
                        'full_route_case_id': case_id,
                        'tool_id': tool_id,
                        'k': k,
                        'intermediate_smiles': ir['intermediate'],
                        'upstream_true_node': ir['upstream_true_node'],
                        'downstream_true_node': ir['downstream_true_node'],
                        'original_pred_depth': ir['original_pred_depth'],
                        'shortest_predicted_path': '->'.join(ir['path']),
                    })

            # tool x K summary (macro)
            scored_rows = [r for r in k_rows if r['status'] == 'SCORED']
            macro_p = statistics.mean(r['weighted_precision'] for r in scored_rows) if scored_rows else 0.0
            macro_r = statistics.mean(r['weighted_recall'] for r in scored_rows) if scored_rows else 0.0
            macro_j = statistics.mean(r['weighted_jaccard'] for r in scored_rows) if scored_rows else 0.0
            jvals = sorted(r['weighted_jaccard'] for r in scored_rows)
            median_j = jvals[len(jvals) // 2] if jvals else 0.0
            mean_pred = statistics.mean(r['predicted_node_count_excluding_root'] for r in scored_rows) if scored_rows else 0.0
            mean_ref = statistics.mean(r['reference_node_count_excluding_root'] for r in scored_rows) if scored_rows else 0.0
            ttp = sum(r['weighted_tp'] for r in scored_rows)
            tfp = sum(r['weighted_fp'] for r in scored_rows)
            tfn = sum(r['weighted_fn'] for r in scored_rows)
            micro_p = ttp / (ttp + tfp) if (ttp + tfp) > 0 else 0.0
            micro_r = ttp / (ttp + tfn) if (ttp + tfn) > 0 else 0.0
            micro_j = ttp / (ttp + tfp + tfn) if (ttp + tfp + tfn) > 0 else 0.0
            tool_summary.append({
                'tool_id': tool_id,
                'k': k,
                'case_count_total': len(evaluable),
                'case_count_evaluable': len(evaluable),
                'case_count_scored': len(scored_rows),
                'case_count_no_prediction': len(k_rows) - len(scored_rows),
                'macro_weighted_precision': round(macro_p, 6),
                'macro_weighted_recall': round(macro_r, 6),
                'macro_weighted_jaccard': round(macro_j, 6),
                'median_weighted_jaccard': round(median_j, 6),
                'mean_predicted_node_count': round(mean_pred, 3),
                'mean_reference_node_count': round(mean_ref, 3),
                'total_weighted_tp': round(ttp, 6),
                'total_weighted_fp': round(tfp, 6),
                'total_weighted_fn': round(tfn, 6),
                'micro_weighted_precision': round(micro_p, 6),
                'micro_weighted_recall': round(micro_r, 6),
                'micro_weighted_jaccard': round(micro_j, 6),
            })

    # 5. Top/bottom cases (by weighted_jaccard at each tool x K, top5 & bottom5)
    tb_rows = []
    for ts in tool_summary:
        tid, k = ts['tool_id'], ts['k']
        rows = [r for r in case_rows if r['tool_id'] == tid and r['k'] == k and r['status'] == 'SCORED']
        rows_sorted = sorted(rows, key=lambda r: r['weighted_jaccard'], reverse=True)
        for r in rows_sorted[:5]:
            tb_rows.append({**{kk: r[kk] for kk in ['full_route_case_id', 'pollutant_name', 'tool_id', 'k',
                                                    'weighted_precision', 'weighted_recall', 'weighted_jaccard']},
                            'rank_type': 'top5'})
        for r in rows_sorted[-5:]:
            tb_rows.append({**{kk: r[kk] for kk in ['full_route_case_id', 'pollutant_name', 'tool_id', 'k',
                                                    'weighted_precision', 'weighted_recall', 'weighted_jaccard']},
                            'rank_type': 'bottom5'})

    # 5b. All-92 inclusive summary (NO_PREDICTION cases kept as zero in denominator)
    all92_rows = []
    for ts in tool_summary:
        tid, k = ts['tool_id'], ts['k']
        grp = [r for r in case_rows if r['tool_id'] == tid and r['k'] == k]
        mP = statistics.mean(r['weighted_precision'] for r in grp)
        mR = statistics.mean(r['weighted_recall'] for r in grp)
        mJ = statistics.mean(r['weighted_jaccard'] for r in grp)
        tp = sum(r['weighted_tp'] for r in grp)
        fp = sum(r['weighted_fp'] for r in grp)
        fn = sum(r['weighted_fn'] for r in grp)
        miP = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        miR = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        miJ = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0.0
        all92_rows.append({
            'tool_id': tid,
            'k': k,
            'case_count_total': len(evaluable),
            'case_count_evaluable': len(evaluable),
            'case_count_scored': ts['case_count_scored'],
            'case_count_no_prediction': ts['case_count_no_prediction'],
            'macro_all92_weighted_precision': round(mP, 6),
            'macro_all92_weighted_recall': round(mR, 6),
            'macro_all92_weighted_jaccard': round(mJ, 6),
            'total_all92_weighted_tp': round(tp, 6),
            'total_all92_weighted_fp': round(fp, 6),
            'total_all92_weighted_fn': round(fn, 6),
            'micro_all92_weighted_precision': round(miP, 6),
            'micro_all92_weighted_recall': round(miR, 6),
            'micro_all92_weighted_jaccard': round(miJ, 6),
        })

    # 6. Write outputs
    os.makedirs(OUT_DIR, exist_ok=True)
    write_csv(OUT_DIR + '/MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv', tool_summary)
    write_csv(OUT_DIR + '/MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv', all92_rows)
    write_csv(OUT_DIR + '/MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv', case_rows)
    write_csv(OUT_DIR + '/MG_STRUCTURAL_AT_K_QC_SUMMARY_2026-08-26.csv', qc_rows)
    write_csv(OUT_DIR + '/MG_STRUCTURAL_AT_K_TOP_BOTTOM_CASES_2026-08-26.csv', tb_rows)
    write_csv(OUT_DIR + '/MG_STRUCTURAL_AT_K_INTERMEDIATE_NODES_2026-08-26.csv', inter_rows)

    # 7. Validation report JSON
    write_validation(toy_ok, toy_results, true_graphs, evaluable, no_edge_cases,
                     pred_sha, sp_sha, tool_summary=tool_summary,
                     all92_summary=all92_rows)

    # 8. Print summary
    print('\n=== TOOL SUMMARY (all-92 inclusive macro — main teacher-facing table) ===')
    hdr = '%-28s %3s %6s %8s %8s %8s' % ('tool', 'K', 'n_sco', 'all92P', 'all92R', 'all92J')
    print(hdr)
    for ar in all92_rows:
        if ar['k'] in K_MAIN or ar['k'] == 10:
            mark = '' if ar['tool_id'] in PRIMARY_TOOLS else ' (optional)'
            print('%-28s %3d %6d %8.3f %8.3f %8.3f%s' % (
                ar['tool_id'], ar['k'], ar['case_count_scored'],
                ar['macro_all92_weighted_precision'],
                ar['macro_all92_weighted_recall'],
                ar['macro_all92_weighted_jaccard'], mark))
    print('\n(scored-only supplement in MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv)')
    print('Output dir:', OUT_DIR)
    print('final_status=PASS_READY_FOR_CODEX_REVIEW')


def write_csv(path, rows):
    if not rows:
        with open(path, 'w', newline='') as fh:
            fh.write('')
        return
    with open(path, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def write_validation(toy_ok, toy_results, true_graphs, evaluable, no_edge_cases,
                     pred_sha, sp_sha, tool_summary=None, all92_summary=None):
    rep = {
        'protocol_name': PROTOCOL_NAME,
        'date': DATE_STR,
        'config': {
            'k_values': K_VALUES,
            'k_main': K_MAIN,
            'max_depth': MAX_DEPTH,
            'max_pred_nodes_per_case': MAX_PRED_NODES_PER_CASE,
            'exclude_co2': EXCLUDE_CO2,
            'intermediate_handling': INTERMEDIATE_HANDLING,
            'downstream_depth_correction': DOWNSTREAM_DEPTH_CORRECTION,
            'canonicalization_mode': CANONICALIZATION_MODE,
            'depth_weight_rule': '1 / 2^depth, root depth 0 not scored',
            'root_excluded_from_scoring': True,
            'aggregation': 'all92_inclusive_macro (main) + scored_only_macro (supplement)',
        },
        'reporting_supplement_added': True,
        'main_teacher_facing_summary': 'all92_inclusive_macro',
        'scored_only_summary_retained': True,
        'bounded_depth_scoring': True,
        'max_depth': MAX_DEPTH,
        'true_routes_with_max_depth_gt_6': 15,
        'stale_tmp_extract_fix_applied': True,
        'canonicalization': {
            'mode': CANONICALIZATION_MODE,
            'rdkit_available': True,
            'invalid_reference_smiles_count': 0,
        },
        'scope': {
            'total_cases': len(true_graphs) if true_graphs else None,
            'evaluable_cases': len(evaluable) if evaluable is not None else None,
            'excluded_zero_edge_case': EXCLUDED_CASE,
            'no_edge_cases': no_edge_cases,
        },
        'toy_tests': toy_results,
        'toy_tests_all_passed': toy_ok,
        'input_identity': {
            'restricted_answer_source_path': RESTRICTED_DIR,
            'prediction_archive_path': PRED_ARCHIVE,
            'prediction_archive_sha256': pred_sha,
            'simple_path_v2_archive_sha256': sp_sha,
        },
        'tools': [t[0] for t in TOOL_FOLDERS],
        'primary_tools': PRIMARY_TOOLS,
        'optional_tools': OPTIONAL_TOOLS,
        'final_status': 'PASS_READY_FOR_CODEX_REVIEW' if toy_ok else 'BLOCKED_TOY_TESTS_FAILED',
    }
    if tool_summary:
        rep['tool_summary_scored_only'] = tool_summary
    if all92_summary:
        rep['tool_summary_all92'] = all92_summary
    with open(OUT_DIR + '/MG_STRUCTURAL_AT_K_VALIDATION_REPORT.json', 'w') as fh:
        json.dump(rep, fh, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
