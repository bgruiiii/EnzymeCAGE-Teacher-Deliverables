#!/usr/bin/env python3
"""R3 three-model GF scoring on the UNIFIED three-way pool.

Adapted from R2 r2_gf_dual600m.py (v3) which adapts BUNDLE/historical/a109/
GF_DUAL_RUN_C95.py (audited). Complete change list vs R2 GF v3:
 1. third arm legacy_esm2_3b: old stack, esm_model from the R3 merged cfg
    (esm2_t36_3B_UR50D -> 2560), PLAIN state_dict strict, index =
    C95AssetIndex(PrecomputedAssetIndex(R3 materialize_{ctx} merged cfg),
    parent runtime map) — the A109-proven consumer path; bounded16 protocol
    (invariance-gated on this node in A109).
 2. legacy_esmc600m: LegacyArmIndexV3 overlay chain (native -> sept-union ->
    rescue-generated-0713) with named-bundle rule; whole_step original protocol
    (bounded16 invariance gate failed at 1.9e-4 in R2 — typed, retained).
 3. new_esmc600m: NewArmIndexV3 (R2 chain + rescue overlays) bounded16.
 4. step table = UNIFIED_STEP_TABLE_{ctx}; per-arm asset uid columns; dim
    asserted from ACTUAL store tensors (2560/1152); rescue/today-batch
    dependency counts bound into COMMON context.
 5. locked checkpoint matrices from the bundled MODEL_IDENTITIES_27 (all three
    arms), asserted per seed load with full file sha.
Unchanged: raw contract (sigmoid_readout=False asserted per seed), finite+len
asserts, frozen COMMON context + per-seed identities, pre-forward conflict
scan, identical-identity resume, atomic writes, typed FORWARD_FAILURES with no
candidate dropping, real invariance/determinism smokes per seed.
"""
import argparse, hashlib, json, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_paths as P
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "scripts"))
import recovery_helpers as RH
import r2_lib as L2
import r3_consumer as C3

ap = argparse.ArgumentParser()
ap.add_argument("--arm", required=True, choices=list(P.ARMS3))
ap.add_argument("--seeds", default=",".join(map(str, P.SEEDS)))
ap.add_argument("--contexts", default="main,delta15")
a = ap.parse_args()
ARM = a.arm
SEEDS = [int(x) for x in a.seeds.split(",")]
CTXS = a.contexts.split(",")
assert SEEDS == P.SEEDS
RH.require_scoring_gate(P.NEWROOT + "/runtime/pool")

DIM = {"legacy_esm2_3b": 2560, "legacy_esmc600m": 1152, "new_esmc600m": 1152}[ARM]
PROTOCOL = {"legacy_esm2_3b": "bounded16", "legacy_esmc600m": "whole_step", "new_esmc600m": "bounded16"}[ARM]

if ARM == "new_esmc600m":
    STACK_ROOT = P.S8CODE
else:
    STACK_ROOT = P.REPO_OLD
    sys.path.insert(0, P.WRAP)
sys.path.insert(0, STACK_ROOT)
sys.path.insert(0, P.BUNDLE + "/historical/a109")
os.environ.setdefault("ENZYMECAGE_SHARD_CACHE_SIZE", "all")
import torch, yaml
import enzymecage.model as _emodel
import enzymecage.dataset.geometric as geom
import torch_geometric.data as pyg_data
from torch_geometric.loader import DataLoader
from enzymecage.model import EnzymeCAGE
from c95_bounded_forward import forward_dataset, real_invariance_smoke
import pandas as pd

sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()
t0 = time.time()
def log(*m): print(f"[{time.time()-t0:7.1f}s][{ARM}]", *m, flush=True)

# locked matrix (bundled identities, cross-checked vs R1 node verification for 600M arms)
LOCKED = {}
import csv as _csv
with open(P.PKG + "/MODEL_IDENTITIES_27.tsv") as f:
    for r in _csv.DictReader(f, delimiter="\t"):
        if r["arm"] == ARM:
            LOCKED[int(r["seed"])] = (r["path"], r["sha256"], int(r["bytes"]))
assert sorted(LOCKED) == P.SEEDS

dev = torch.device("cuda:0")
FOLLOW = ["protein", "reaction_feature", "esm_feature", "substrates", "products"]
POOL = P.NEWROOT + "/runtime/pool"

# ---- index construction (heavy stores once per process) ----
if ARM == "legacy_esm2_3b":
    from enzymecage_wrapper.asset_index import PrecomputedAssetIndex
    from c95_asset_index_ext import C95AssetIndex
    def bind_ctx(ctx):
        cfg = yaml.safe_load(open(f"{P.R3}/materialize_{ctx}/cfg/c95_3b_merged_config.yaml"))
        idx = RH.build_3b_index(P, ctx, cfg, PrecomputedAssetIndex, C95AssetIndex)
        return idx, cfg
elif ARM == "legacy_esmc600m":
    from c95_asset_index_ext import C95AssetIndex
    core = C3.LegacyArmIndexV3(pd, torch)
    log("legacy v3 chain:", json.dumps(core.inventory(), default=str)[:300])
    def bind_ctx(ctx):
        core.bind_reaction(ctx, pd, torch)
        idx = C95AssetIndex(core, f"{P.PKG}/inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv")
        # extend uid map with parent runtime rows (C95 does this itself); nothing else needed
        return idx, None
else:
    overlays = C3.load_overlays()
    NEWIDX = C3.NewArmIndexV3("main", pd, torch, overlays)
    log("new v3 index built; overlays:", {k: len(v) for k, v in overlays.items() if k != "_manifest"})
    def bind_ctx(ctx):
        import pickle
        from pathlib import Path
        rx = P.RXN[ctx]
        with open(rx + "/rxn2fp_merged.pkl", "rb") as f: NEWIDX.rxn_fp = pickle.load(f)
        with open(rx + "/reacting_center_merged.pkl", "rb") as f: NEWIDX.reaction_centers = pickle.load(f)
        mdir = Path(rx + "/mol_conformation")
        mtab = pd.read_csv(mdir / "mol2id.csv")
        NEWIDX.molecule_index = frozenset(mtab["SMILES"].astype(str))
        NEWIDX.molecule_graphs = torch.load(mdir / "mol_graph_dict.pt", map_location="cpu", weights_only=False)
        if not NEWIDX.molecule_index.issubset(NEWIDX.molecule_graphs.keys()):
            raise RuntimeError(f"mol graph cache incomplete ctx={ctx}")
        NEWIDX.ctx = ctx
        return NEWIDX, None

AUID_COL = {"legacy_esm2_3b": "asset_uids_3b", "legacy_esmc600m": "asset_uids_legacy", "new_esmc600m": "asset_uids_new"}[ARM]

def build(idx, rxn, uids, seqs):
    if ARM == "legacy_esmc600m":
        for u, s in zip(uids, seqs):
            assert idx.sequence_for(u) == s, f"sequence_for mismatch {u}"
    fr = geom.pd.DataFrame({"UniprotID": uids, "CANO_RXN_SMILES": [rxn] * len(uids),
                            "sequence": list(seqs), "Label": [0] * len(uids)})
    ds = geom.GeometricDataset.__new__(geom.GeometricDataset); pyg_data.Dataset.__init__(ds)
    ds.df_data = fr; ds.pocket_node_feature = idx.pocket_node; ds.esm_dim = DIM
    ds.protein_dict = idx.gvp; ds.esm_feat_dict = idx.sequence_esm; ds.rxn_feat_dict = idx.rxn_fp
    ds.uniprot_ids = list(uids); ds.rxns = [rxn] * len(uids); ds.targets = [0] * len(uids)
    ds.seqs = list(seqs); ds.weights = torch.ones(len(uids))
    if ARM == "new_esmc600m":
        m2i = pd.read_csv(P.RXN[NEWIDX.ctx] + "/mol_conformation/mol2id.csv")
        ds.mol_to_index = dict(zip(m2i.SMILES.astype(str), m2i.ID))
    else:
        ds.mol_to_index = {k: i for i, k in enumerate(idx.molecule_index)}
    ds.mol_to_data = idx.molecule_graphs
    ds.reacting_center_map = idx.reaction_centers
    return ds

def make_model(seed, cfg3b=None):
    p, want, nb = LOCKED[seed]
    assert os.path.getsize(p) == nb, f"ckpt size drift {p}"
    h = L2.sha_file(p)
    assert h == want, f"CKPT SHA MISMATCH {ARM} seed{seed}"
    if ARM == "legacy_esm2_3b":
        m = EnzymeCAGE(use_esm=cfg3b["use_esm"], use_structure=cfg3b["use_structure"], use_drfp=cfg3b["use_drfp"],
                       use_prods_info=cfg3b["use_prods_info"], esm_model=cfg3b["esm_model"],
                       interaction_method=cfg3b["interaction_method"],
                       rxn_inner_interaction=cfg3b["rxn_inner_interaction"],
                       pocket_inner_interaction=cfg3b["pocket_inner_interaction"], device=str(dev))
        m.load_state_dict(torch.load(p, map_location="cpu", weights_only=False), strict=True)
    elif ARM == "legacy_esmc600m":
        m = EnzymeCAGE(use_esm=True, use_structure=True, use_drfp=True, use_prods_info=False,
                       esm_model="ESM-C_600M", interaction_method="geo-enhanced-interaction",
                       rxn_inner_interaction=True, pocket_inner_interaction=True, device=str(dev))
        m.load_state_dict(torch.load(p, map_location="cpu", weights_only=False), strict=True)
    else:
        m = EnzymeCAGE(use_esm=True, use_structure=True, use_drfp=True, use_prods_info=False,
                       plm_model="esmc600m", plm_dim=1152,
                       interaction_method="geo-enhanced-interaction", rxn_inner_interaction=True,
                       pocket_inner_interaction=True, device=str(dev))
        ck = torch.load(p, map_location="cpu", weights_only=False)
        m.load_state_dict(ck["model_state_dict"], strict=True)
    m = m.to(dev).eval()
    assert getattr(m, "sigmoid_readout", None) is False, "RAW contract requires sigmoid_readout=False"
    assert int(m.esm_dim) == DIM, f"model esm_dim {m.esm_dim} != {DIM}"
    return m, p, want

OUTPUT_SEMANTICS = "RAW_LOGIT_FORWARD_SIGMOID_READOUT_FALSE"

def run_context(ctx):
    log(f"===== context {ctx} =====")
    idx, cfg3b = bind_ctx(ctx)
    steps = json.load(open(f"{POOL}/UNIFIED_STEP_TABLE_{ctx}.json"))
    if not steps:
        log("no unified steps; skip"); return
    if ARM == "new_esmc600m":
        idx.set_sha_map([(sq, sh) for s in steps for sq, sh in zip(s["pool_seqs"], s["pool_shas"])])
    out_root = f"{P.NEWROOT}/gf_out/{ARM}/{ctx}"
    OUT = out_root + f"/raw_logits_{ARM}"
    os.makedirs(OUT, exist_ok=True)

    # dim from ACTUAL store tensor
    s0 = steps[0]
    probe = idx.pocket_node[s0[AUID_COL][0]]
    dim_actual = int(np.asarray(probe).shape[1])
    assert dim_actual == DIM, f"actual dim {dim_actual} != {DIM}"
    log("actual store dim verified:", dim_actual)

    freeze_summ_sha = L2.sha_file(f"{POOL}/FREEZE_SUMMARY.json")
    admission_sha = L2.sha_file(P.NEWROOT + "/runtime/pc_genimpact/ADMISSION_DECISION.json")
    ovl_manifest = P.NEWROOT + "/overlay/OVERLAY_MANIFEST.json"
    COMMON_CONTEXT = {
        "arm": ARM, "context": ctx, "lane": "R3_UNIFIED_THREE_MODEL",
        "context_inputs": {"a109_overlay_identity": RH.a109_identity(P, ctx) if ARM == "legacy_esm2_3b" else None,
            "unified_step_table_sha256": sha(open(f"{POOL}/UNIFIED_STEP_TABLE_{ctx}.json", "rb").read()),
            "runtime_map_sha256": L2.sha_file(f"{P.PKG}/inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv"),
            "eval_labels_parent_sha256": L2.sha_file(f"{P.PKG}/inputs/{ctx}/EVAL_LABELS_PARENT.tsv"),
            "freeze_summary_sha256": freeze_summ_sha,
            "admission_decision_sha256": admission_sha,
            "overlay_manifest_sha256": L2.sha_file(ovl_manifest) if os.path.exists(ovl_manifest) else "",
            "reaction_identity": {f: L2.sha_file(f"{P.RXN[ctx]}/{f}") for f in ("rxn2fp_merged.pkl", "reacting_center_merged.pkl")},
        },
        "assets": {"chain": {"legacy_esm2_3b": "R3 merged materialized stores (A109-proven)",
                             "legacy_esmc600m": "native_july -> sept_union_generated -> rescue_generated_0713 (named bundles only)",
                             "new_esmc600m": "corrected/S10/S11 + rescue_r3d overlays (named bundles only)"}[ARM],
                   "rescue_batch_label": "RESCUE_GENERATED_NODE_20261103 (RTX4080S Ada vGPU; weights 8ef856e1…; esm 3.1.1; verbatim recipe; admitted with batch-effect disclosure)"},
        "rescue_dependency": {"steps_rescue_dependent": sum(1 for s in steps if s["rescue_dependent"]),
                              "rows_today_batch": sum(sum(1 for f in s["today_batch_flags"] if f) for s in steps)},
        "sources": {"gf_script_sha256": L2.sha_file(os.path.abspath(__file__)),
                    "r3_consumer_sha256": L2.sha_file(os.path.dirname(os.path.abspath(__file__)) + "/r3_consumer.py"),
                    "r2_lib_sha256": L2.sha_file(os.path.dirname(os.path.abspath(__file__)) + "/r2_lib.py"),
                    "bounded_helper_sha256": L2.sha_file(P.BUNDLE + "/historical/a109/c95_bounded_forward.py"),
                    "stack_root": STACK_ROOT,
                    "model_source_sha256": sha(open(_emodel.__file__, "rb").read()),
                    "geometric_source_sha256": sha(open(geom.__file__, "rb").read())},
        "batch_contract": ({"max_candidate_batch_size": 16, "padding": "FROZEN_WHOLE_STEP_MAXIMA", "protocol": "BOUNDED16_INVARIANCE_GATED"}
                           if PROTOCOL == "bounded16" else
                           {"protocol": "WHOLE_STEP_PURE_BATCH", "padding": "NATURAL_WHOLE_STEP",
                            "protocol_reason": "R2 legacy bounded16 invariance 1.9e-4>1e-5 typed; whole-step is the PC-verified original protocol"}),
        "weights": {"locked_ckpt_shas": {str(s): LOCKED[s][1] for s in P.SEEDS}},
        "output_contract": {"output_semantics": OUTPUT_SEMANTICS,
                            "sigmoid_readout_evidence": "asserted False on the deployed model object per seed; finite+len asserts; no range guessing"},
    }
    COMMON_SHA = sha(json.dumps(COMMON_CONTEXT, sort_keys=True, separators=(",", ":")))
    json.dump({"common_context": COMMON_CONTEXT, "common_context_sha256": COMMON_SHA},
              open(f"{out_root}/COMMON_CONTEXT.json", "w"), indent=1)
    log(f"common_context_sha256={COMMON_SHA[:16]}…")

    # ---- prescan with the REAL per-arm predicate ----
    ready, incomplete = [], []
    for s in steps:
        rxn = s["model_reaction"]
        miss = idx.missing_assets(rxn)
        c = idx.reaction_centers.get(rxn)
        if not isinstance(c, (tuple, list)) or len(c) != 2 or len(c[0]) == 0 or len(c[1]) == 0:
            miss = miss + ["reacting-center typed key/side"]
        miss_uids = []
        for u, sq, sh in zip(s[AUID_COL], s["pool_seqs"], s["pool_shas"]):
            if ARM == "new_esmc600m":
                ok, reason, _ = C3.new_arm_check_v3(idx, u, sq, sh)
            elif ARM == "legacy_esmc600m":
                ok, reason, _ = C3.legacy_arm_check_v3(core, u, sq)
                ok = ok and idx.has_enzyme(u)
            else:
                ok = idx.has_enzyme(u); reason = "" if ok else "3B_HAS_ENZYME_FALSE"
            if not ok: miss_uids.append(f"{u}:{reason}")
        if miss or miss_uids:
            incomplete.append({"step_id": s["step_id"], "missing_reaction_assets": miss,
                               "missing_candidate_uids_n": len(miss_uids),
                               "missing_candidate_uids_sample": miss_uids[:5],
                               "status": "INCOMPLETE_POOL_NOT_FORWARDED"})
        else:
            ready.append(s)
    json.dump({"arm": ARM, "ctx": ctx, "total_steps": len(steps), "ready": len(ready), "incomplete": len(incomplete),
               "incomplete_steps": incomplete, "common_context_sha256": COMMON_SHA},
              open(f"{out_root}/GF_PRESCAN_REPORT.json", "w"), indent=1)
    log(f"prescan ready={len(ready)} incomplete={len(incomplete)}")
    if not ready:
        log("GF_STOP no ready steps"); return

    existing, conflicts = {}, []
    for s in ready:
        f = os.path.join(OUT, f"{s['step_id']}.json")
        if not os.path.exists(f): continue
        d = json.load(open(f)); existing[s["step_id"]] = d
        if d.get("common_context_sha256") != COMMON_SHA:
            conflicts.append({"step_id": s["step_id"], "reason": "COMMON_CONTEXT_MISMATCH"})
        elif d.get("pool_uids") != s["pool_uids"] or d.get("pool_shas") != s["pool_shas"]:
            conflicts.append({"step_id": s["step_id"], "reason": "MEMBERSHIP_CONFLICT"})
    if conflicts:
        json.dump(conflicts, open(f"{out_root}/GF_CONTEXT_CONFLICTS.json", "w"), indent=1)
        raise SystemExit(f"GF_CONTEXT_CONFLICT {len(conflicts)}")

    def forward_whole_step(m, ds):
        b = next(iter(DataLoader(ds, batch_size=len(ds.uniprot_ids), shuffle=False, follow_batch=FOLLOW))).to(dev)
        with torch.no_grad():
            o = m.forward(b)
        if isinstance(o, tuple): o = o[0]
        raw = o.detach().cpu().to(torch.float64).numpy().reshape(-1)
        if not np.isfinite(raw).all(): raise RuntimeError("NON_FINITE_RAW_LOGIT")
        return raw

    max_pool = max(len(s["pool_uids"]) for s in ready)
    log(f"frozen max pool={max_pool}; protocol={PROTOCOL}")
    timing = {"arm": ARM, "ctx": ctx, "protocol": PROTOCOL, "steps": len(ready), "per_seed": {}, "representative_batches": []}
    failed = set()
    for seed in SEEDS:
        m, p, ck_sha = make_model(seed, cfg3b)
        smoke = max(ready, key=lambda s: len(s["pool_uids"]))
        sauids = smoke[AUID_COL]
        if PROTOCOL == "bounded16":
            real_invariance_smoke(m, lambda rxn, uids: build(idx, rxn, uids,
                                  [smoke["pool_seqs"][sauids.index(u)] for u in uids]),
                                  {**smoke, "pool_uids": sauids}, DataLoader, FOLLOW, dev, _emodel,
                                  f"{out_root}/REAL_BATCH_INVARIANCE_seed_{seed}.json")
        else:
            r1 = forward_whole_step(m, build(idx, smoke["model_reaction"], sauids, smoke["pool_seqs"]))
            r2 = forward_whole_step(m, build(idx, smoke["model_reaction"], sauids, smoke["pool_seqs"]))
            dd = float(np.max(np.abs(r1 - r2)))
            json.dump({"step_id": smoke["step_id"], "protocol": "WHOLE_STEP_PURE_BATCH", "candidates": len(sauids),
                       "run1_vs_run2_max_abs_delta": dd, "gpu_mem_alloc_mb": round(torch.cuda.max_memory_allocated()/1e6, 1),
                       "sanity_gate": "<=1e-3 disclosed", "pass": bool(dd <= 1e-3)},
                      open(f"{out_root}/REAL_WHOLE_STEP_DETERMINISM_seed_{seed}.json", "w"), indent=1)
            assert dd <= 1e-3, f"WHOLE_STEP_DETERMINISM_SANITY_FAILED {dd}"
        n = reused = 0; ts = time.time()
        for s in ready:
            sid = s["step_id"]; auids = s[AUID_COL]
            if sid in failed: continue
            d0 = existing.get(sid)
            if d0 and str(seed) in d0.get("seeds", {}):
                si = d0.get("seed_identities", {}).get(str(seed), {})
                saved = d0.get("raw_logits", {}).get(str(seed))
                ok_saved = (isinstance(saved, list) and len(saved) == len(auids)
                            and all(isinstance(x, (int, float)) and np.isfinite(x) for x in saved))
                if si.get("common_context_sha256") == COMMON_SHA and si.get("ckpt_sha256") == ck_sha and ok_saved:
                    reused += 1; continue
            try:
                tb = time.time()
                if PROTOCOL == "bounded16":
                    Lg = forward_dataset(m, build(idx, s["model_reaction"], auids, s["pool_seqs"]), DataLoader, FOLLOW, dev, _emodel, max_candidates=16)
                else:
                    Lg = forward_whole_step(m, build(idx, s["model_reaction"], auids, s["pool_seqs"]))
                dt = time.time() - tb
            except (RuntimeError, KeyError, ValueError, IndexError) as exc:
                with open(f"{out_root}/FORWARD_FAILURES.jsonl", "a") as fl:
                    fl.write(json.dumps({"step_id": sid, "seed": seed, "status": "FORWARD_FAILED_TYPED_NO_CANDIDATE_DROPPED",
                                         "error": type(exc).__name__ + ": " + str(exc)[:300], "pool_size": len(auids)}) + "\n")
                failed.add(sid); torch.cuda.empty_cache(); continue
            assert np.isfinite(Lg).all(), sid
            assert len(Lg) == len(auids), f"{sid}: len {len(Lg)} != {len(auids)}"
            if seed == SEEDS[0] and len(timing["representative_batches"]) < 8:
                timing["representative_batches"].append({"step_id": sid, "pool": len(auids), "forward_sec": round(dt, 3),
                                                         "gpu_mem_alloc_mb": round(torch.cuda.max_memory_allocated()/1e6, 1)})
            f = os.path.join(OUT, f"{sid}.json")
            d = json.load(open(f)) if os.path.exists(f) else {
                "step_id": sid, "model_cano_rxn_smiles": s["model_reaction"], "model_key_sha256": s["model_key_sha256"],
                "no_discrimination": bool(s.get("no_discrimination")),
                "pool_uids": s["pool_uids"], "pool_shas": s["pool_shas"], "asset_uids": auids,
                "arm": ARM, "ctx": ctx, "lane": "R3_UNIFIED_THREE_MODEL",
                "rescue_dependent": bool(s.get("rescue_dependent")),
                "seeds": {}, "raw_logits": {}, "seed_identities": {},
                "common_context_sha256": COMMON_SHA, "common_context": COMMON_CONTEXT,
                "output_semantics": OUTPUT_SEMANTICS}
            assert d["pool_uids"] == s["pool_uids"] and d["pool_shas"] == s["pool_shas"], f"{sid}: drift"
            assert d.get("common_context_sha256") == COMMON_SHA and d.get("model_key_sha256") == s["model_key_sha256"]
            d["seeds"][str(seed)] = True; d["raw_logits"][str(seed)] = Lg.tolist()
            d.setdefault("seed_identities", {})[str(seed)] = {
                "common_context_sha256": COMMON_SHA, "ckpt_path": p, "ckpt_sha256": ck_sha,
                "forward_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            tmpf = f + ".tmp"; json.dump(d, open(tmpf, "w")); os.replace(tmpf, f)
            n += 1
            if n % 60 == 0: log(f"s{seed} {n}/{len(ready)} ({time.time()-ts:.0f}s)")
        timing["per_seed"][str(seed)] = {"forwarded": n, "reused": reused, "wall_sec": round(time.time()-ts, 1), "failed_steps": sorted(failed)}
        log(f"seed {seed} done forwarded={n} reused={reused} wall={time.time()-ts:.0f}s")
        del m; torch.cuda.empty_cache()
    json.dump(timing, open(f"{out_root}/GF_TIMING.json", "w"), indent=1)
    log(f"GF DONE {ARM}/{ctx}")

for ctx in CTXS:
    run_context(ctx)
log("GF_ALL_DONE", ARM)
