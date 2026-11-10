"""R3 FIXED retrieval engine.
Frozen scoring core (Morgan r=8 + BulkTanimoto + getRSim greedy + max(S1,S2))
is invoked verbatim from copied_old_pipeline (== retrieve.py functions).

CRITICAL reproduction detail: the frozen getRSim greedy tie-break depends on the
candidate-molecule id strings and the `list(set(cand_smiles))` enumeration order
that retrieve.py's get_mol_simi_dict uses. To reproduce retrieve.py bit-for-bit
the engine mirrors get_mol_simi_dict EXACTLY: same MOL_i ids, same set()
enumeration (deterministic under the fixed PYTHONHASHSEED=0 used everywhere),
and cpd_simi_dict rebuilt per query.

FIX 1: for every query molecule (whether or not it appears among candidates) the
       fingerprint is computed and BulkTanimoto-compared against ALL candidate
       molecule fingerprints -> sim[query_molecule][candidate_id] = score.
FIX 2: strict mode enum {PRODUCTION_INCLUDE_EXACT, BENCHMARK_QUERY_EXCLUDED};
       unknown mode raises; BENCHMARK excludes exact directional repr AND
       reverse/undirected-equal chemistry; PRODUCTION keeps exact matches at 1.0.
Ranking: (-score, sha256(canonical_directional))."""
import hashlib
from collections import Counter, defaultdict

from copied_old_pipeline import (neutralize_atoms, get_morgan_fp, bulkTani, getRSim,
                                 remove_redundent_from_rxn, filter_unwanted_rxn,
                                 neutralize_rxn, cano_rxn)

MODES = ("PRODUCTION_INCLUDE_EXACT", "BENCHMARK_QUERY_EXCLUDED")

def query_retrieval_repr(rxn_smiles):
    r = remove_redundent_from_rxn(rxn_smiles)
    if r: r = filter_unwanted_rxn(r)
    if r: r = neutralize_rxn(r)
    return cano_rxn(r) if r else None

def sha256s(x): return hashlib.sha256(x.encode()).hexdigest()

class FixedIndex:
    """Candidate universe + structures built EXACTLY like retrieve.py's
    get_mol_simi_dict, so getRSim tie-breaks identically."""
    def __init__(self, name, reactions, rxn_to_enzymes):
        # reactions: list of dicts {canonical_directional, retrieval_repr, undirected_key}
        self.name = name
        self.reactions = reactions
        self.rxn_to_enzymes = rxn_to_enzymes or {}
        self.rx_repr = {r["canonical_directional"]: r["retrieval_repr"] for r in reactions}
        self.by_repr = defaultdict(list)
        self.by_uk = defaultdict(list)
        for r in reactions:
            self.by_repr[r["retrieval_repr"]].append(r["canonical_directional"])
            if r.get("undirected_key"):
                self.by_uk[r["undirected_key"]].append(r["canonical_directional"])
        # --- candidate molecule universe, EXACTLY as get_mol_simi_dict ---
        cand_smiles_list = []
        for rxn in self.rx_repr.values():
            cand_smiles_list += rxn.split(">>")[0].split(".") + rxn.split(">>")[1].split(".")
        cand_smiles = list(set(cand_smiles_list))
        self.cand_mol_ids = [f"MOL_{i}" for i, _ in enumerate(cand_smiles)]
        self.cand_mol_to_id_dict = dict(zip(cand_smiles, self.cand_mol_ids))
        self.cand_fp_list = []
        self._cand_fp_ok = set()
        for smi in cand_smiles:
            s2 = neutralize_atoms(smi)
            try:
                self.cand_fp_list.append(get_morgan_fp(s2)[0])
            except Exception:
                self.cand_fp_list.append(None)
        # candidate rct/prod id-counters per reaction (as run_retrieval builds them)
        self.rxn_rct_ids, self.rxn_pro_ids = {}, {}
        for cd, rxn in self.rx_repr.items():
            self.rxn_rct_ids[cd] = Counter([self.cand_mol_to_id_dict.get(s) for s in rxn.split(">>")[0].split(".")])
            self.rxn_pro_ids[cd] = Counter([self.cand_mol_to_id_dict.get(s) for s in rxn.split(">>")[1].split(".")])
        self.cds = list(self.rx_repr.keys())

    def molecules(self): return len(self.cand_mol_ids)
    def reactions_n(self): return len(self.reactions)

def _query_sim(index, q_repr):
    """FIX 1: fingerprint of EVERY query molecule vs ALL candidate fingerprints."""
    q_smiles = q_repr.split(">>")[0].split(".") + q_repr.split(">>")[1].split(".")
    sim = {}
    for smi in set(q_smiles):
        try:
            fp_target = get_morgan_fp(neutralize_atoms(smi))[0]
            sim[smi] = bulkTani(fp_target, index.cand_fp_list, index.cand_mol_ids)
        except Exception:
            pass
    return sim

def retrieve(index, q_repr, mode, q_uk=None, topk=None):
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode!r}; allowed: {MODES}")
    exact_cd = set(index.by_repr.get(q_repr, []))
    if q_uk:
        exact_cd |= set(index.by_uk.get(q_uk, []))
    cand = index.cds
    if mode == "BENCHMARK_QUERY_EXCLUDED":
        cand = [c for c in cand if c not in exact_cd]
    sim = _query_sim(index, q_repr)
    rcts = Counter(q_repr.split(">>")[0].split("."))
    pros = Counter(q_repr.split(">>")[1].split("."))
    out = []
    for cd in cand:
        if cd in exact_cd:          # PRODUCTION mode only
            out.append((cd, 1.0)); continue
        S1, S2, _ = getRSim(rcts, pros, index.rxn_rct_ids[cd], index.rxn_pro_ids[cd], sim)
        out.append((cd, max(S1, S2)))
    out.sort(key=lambda t: (-t[1], sha256s(t[0])))
    return out[:topk] if topk else out

def build_index_from_pairs(name, pairs, master, tiers):
    """Production index membership: ONLY pairs with production_retrieval_eligible
    = true and evidence_tier in `tiers`. Unresolved / weak-tier never index."""
    ok = pairs["production_retrieval_eligible"] & pairs["evidence_tier"].isin(tiers)
    ep = pairs[ok]
    rxn_keys = set(ep["reaction_key"])
    sub = master[master["canonical_directional"].isin(rxn_keys) &
                 (master["retrieval_repr"].str.len() > 0)]
    seen, reactions = set(), []
    for row in sub.itertuples():
        if row.canonical_directional in seen: continue
        seen.add(row.canonical_directional)
        reactions.append({"canonical_directional": row.canonical_directional,
                          "retrieval_repr": row.retrieval_repr,
                          "undirected_key": row.chemistry_equivalence_undirected_key,
                          "reaction_id_internal": row.reaction_id_internal})
    r2e = defaultdict(set)
    for row in ep.itertuples():
        if row.reaction_key in seen:
            r2e[row.reaction_key].add((row.canonical_protein_id, row.sequence_sha256))
    return FixedIndex(name, reactions, dict(r2e))
