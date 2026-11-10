# -*- coding: utf-8 -*-
"""B2 part A: freeze R0 index representation/canonical crosswalk, then run the
frozen r3 retrieval (Morgan r=8 sparse + BulkTanimoto + getRSim greedy +
max(same,reverse)) for every FULL query model key.
PRODUCTION_INCLUDE_EXACT: exact same-direction identity keeps score 1.0 and
deterministic rank1 (sort key (-score, sha256(canonical_directional))).
Same/reverse duplicate groups (chemistry undirected key) are collapsed to the
first-ranked member; ALL group members are stored as reference provenance.
Requires PYTHONHASHSEED=0 (set ordering feeds the frozen getRSim tie-break).
CPU-only; per-query shards are immutable and resumable.
"""
import gzip, hashlib, json, os, sys, time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b121_common as C

W = C.WORK
R3S = os.path.join(W, "tools/r3_retrieval/expanded_reaction_enzyme_phase1_r3_retrieval_dbp_20260914", "scripts")
R0 = os.path.join(W, "tools/r0_census/enzymecage_pollutant_biodegradation_category_capacity_census_r0_20260920")
B2 = os.path.join(W, "B2")
OUTQ = os.path.join(B2, "retrieval")
os.makedirs(OUTQ, exist_ok=True)
sys.path.insert(0, R3S)

import pandas as pd
import fixed_retrieval_engine as FRE
from copied_old_pipeline import (remove_redundent_from_rxn, filter_unwanted_rxn,
                                 neutralize_rxn, cano_rxn)

sha256s = FRE.sha256s


def qrepr(cd):
    r = remove_redundent_from_rxn(cd)
    if r:
        r = filter_unwanted_rxn(r)
    if r:
        r = neutralize_rxn(r)
    return cano_rxn(r) if r else None


def main():
    if os.environ.get("PYTHONHASHSEED", None) != "0":
        C.die("PYTHONHASHSEED must be 0 for frozen tie-break semantics")
    if os.environ.get("CUDA_VISIBLE_DEVICES", None) != "":
        C.die("CUDA_VISIBLE_DEVICES must be ''")
    t0 = time.time()
    mp = pd.read_parquet(os.path.join(R0, "01_funnel", "REACTION_MASTER_POOL.parquet"))
    ps = pd.read_parquet(os.path.join(R0, "01_funnel", "ALL_SCIENTIFIC_PAIRS.parquet"))
    assert len(mp) == 29061 and len(ps) == 292582

    pr = ps[["canonical_directional", "retrieval_repr"]].dropna(subset=["retrieval_repr"])
    first = {}
    multi = set()
    for cd, rep in zip(pr.canonical_directional, pr.retrieval_repr):
        if cd not in first:
            first[cd] = rep
        elif first[cd] != rep:
            multi.add(cd)
    uk = dict(zip(mp.canonical_directional, mp.chemistry_equivalence_undirected_key))
    reactions = []
    fix_up = 0
    for cd in mp.canonical_directional:
        rep = first.get(cd)
        if rep is None or cd in multi or ">>" not in (rep or ""):
            got = qrepr(cd)
            rep = got if got else cd
            fix_up += 1
        u = uk.get(cd)
        reactions.append({"canonical_directional": cd, "retrieval_repr": rep,
                          "undirected_key": u if isinstance(u, str) else None})
    uk_by_repr = {}
    for r in reactions:
        uk_by_repr.setdefault(r["retrieval_repr"], r["undirected_key"])
    C.write_json(os.path.join(B2, "INDEX_FREEZE.json"), {
        "library_reactions": len(reactions),
        "repr_from_pairs_frozen": len(reactions) - fix_up,
        "repr_recomputed_or_fallback": fix_up,
        "multi_repr_collisions": len(multi),
        "pair_rows": len(ps),
        "master_sha256": C.sha256_file(os.path.join(R0, "01_funnel", "REACTION_MASTER_POOL.parquet")),
        "pairs_sha256": C.sha256_file(os.path.join(R0, "01_funnel", "ALL_SCIENTIFIC_PAIRS.parquet")),
        "engine": "r3 fixed_retrieval_engine (Morgan r=8 sparse + BulkTanimoto + getRSim + max(same,reverse))",
        "mode": "PRODUCTION_INCLUDE_EXACT",
        "pythonhashseed": "0",
    })

    idx = FRE.FixedIndex("R0_29061", reactions, {})
    members_uk = defaultdict(set)
    members_repr = defaultdict(set)
    for r in reactions:
        members_repr[r["retrieval_repr"]].add(r["canonical_directional"])
        if r["undirected_key"]:
            members_uk[r["undirected_key"]].add(r["canonical_directional"])
    uk_of = {r["canonical_directional"]: r["undirected_key"] for r in reactions}
    repr_of = {r["canonical_directional"]: r["retrieval_repr"] for r in reactions}
    print(f"index built r={idx.reactions_n()} mol={idx.molecules()} {time.time()-t0:.0f}s", flush=True)

    sq = C.read_tsv(os.path.join(W, "B1", "step_queries.tsv"))
    queries = defaultdict(list)
    for q in sq:
        if q["model_cleaned_full"]:
            queries[q["model_cleaned_full"]].append([q["case_id"], q["step_occurrence_id"]])
    print("unique FULL queries:", len(queries), flush=True)

    n = 0
    for k, keys in sorted(queries.items()):
        fn = os.path.join(OUTQ, sha256s(k)[:40] + ".json.gz")
        if os.path.isfile(fn):
            n += 1
            continue
        q_repr = qrepr(k)
        rec = {"model_key": k, "steps": keys, "q_repr": q_repr}
        if q_repr is None:
            rec["status"] = "QUERY_REPRESENTATION_FAILED"
        else:
            ranked = FRE.retrieve(idx, q_repr, "PRODUCTION_INCLUDE_EXACT",
                                  q_uk=uk_by_repr.get(q_repr))
            exact = set(idx.by_repr.get(q_repr, []))
            seen, refs = set(), []
            for cd, score in ranked:
                g = uk_of.get(cd) if uk_of.get(cd) else ("CD:" + cd)
                if g in seen:
                    continue
                seen.add(g)
                grp = set(members_uk.get(g, [])) | members_repr.get(repr_of[cd], {cd}) | {cd}
                refs.append({"cd": cd, "score": round(float(score), 12),
                             "uk": uk_of.get(cd) or "", "group_cds": sorted(grp),
                             "exact_same_direction": cd in exact})
                if len(refs) == 10:
                    break
            rec["exact_in_library"] = bool(exact)
            rec["exact_sha_sorted_representatives"] = sorted(exact)
            rec["references"] = refs
            rec["raw_top20"] = [[cd, round(float(s), 12)] for cd, s in ranked[:20]]
        with gzip.open(fn, "wt", encoding="utf-8") as f:
            json.dump(rec, f)
        n += 1
        if n % 25 == 0:
            print(f"queries {n}/{len(queries)} {time.time()-t0:.0f}s", flush=True)
    print("RETRIEVAL DONE", n, f"{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
