#!/usr/bin/env python3
"""R2 shared library: paths, identities, arm index construction.

Provenance: adapts (does not modify) the audited historical entries shipped in
the R1 bundle (BUNDLE/historical/...):
  * legacy arm  — R1_replay_legacy.py + A109 GF_DUAL_RUN_C95.py pattern
                  (PrecomputedAssetIndex + C95AssetIndex, old stack, plain sd)
  * new arm     — R1_score_cd.py load_arm()/Multi/RouteSeq/seqfor() VERBATIM
                  assembly, S8 code stack, wrapped state_dict
  * bounded fwd — c95_bounded_forward.py used unmodified (copied into adapted/)
Reaction assets: R3 materialize_{main,delta15}/merged/reaction per context.
R2 hardening over key-only inventory (per R2 prompt §A):
  * ThrowingGlobalView: missing global raises KeyError (old geometric.get_esm_feat
    silently zero-fills — forbidden; acceptance guarantees membership anyway).
  * route-generation consistency for the new arm: pocket/GVP/global must come
    from the SAME generation bundle (JULY rank1: corrected+flat+formal-seq;
    S10 rank2: s10 out shards+s3; S11 rank3: gen2 shards+r1 overlay).
    any(pocket from X) + any(gvp from Y) mixing is typed-quarantined.
  * audited asset-route UID substitution (FEATURE_SOURCE_ROUTING) only with
    exact sequence-sha identity, explicitly logged (uid_route_log).
"""
import hashlib
import json
import os
import pickle
import sys
import time
from collections.abc import Mapping

sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()

def sha_file(p, sample=False):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        if not sample:
            for b in iter(lambda: f.read(8 << 20), b""):
                h.update(b)
        else:
            size = os.path.getsize(p)
            h.update(f.read(1 << 16))
            if size > (1 << 17):
                f.seek(size - (1 << 16))
                h.update(f.read(1 << 16))
            h.update(str(size).encode())
    return h.hexdigest()

# ---------------- registered paths (no全盘考古) ----------------
WS   = "/usrdata/EnzymeCAGE_data/workspaces/current95_ngpu32g_20261031"
R1   = WS + "/current95_dual600m_fasttrack_r1_20261102"
BUNDLE = R1 + "/current95_600m_dual_fasttrack_r1_20261102"
R2   = WS + "/current95_dual600m_r2_scoring_20261102"
R2P  = R2 + "/current95_dual600m_r2_cpu_prep_20261102"
PREP = R2P + "/prepared_common_inputs"
A109 = WS + "/a109_admission_resume_20261102_run"
R3   = WS + "/asset_repair_r3_20261101/output"
RETURN_ROOT = "/usrdata/EnzymeCAGE_data/EnzymeCAGE-master/HPC_Returned_Result_Summaries/CURRENT95_DUAL600M_R2_SCORING_20261102"

TRAIN = "/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922"
S10  = TRAIN + "/10_full_training_enzgfm_then_esmc_continuation_r1_20260926"
S8CODE = TRAIN + "/08_loader_code_smoke_20260924/code"
WR   = TRAIN + "/s11_r1_self_included_four_model_20260927"
FEAT = "/usrdata/EnzymeCAGE_data/feature/protein"

REPO_OLD  = "/usrdata/EnzymeCAGE_data/EnzymeCAGE-master"          # == /root/projects/EnzymeCAGE-master (byte-identical model.py/geometric.py, verified)
REPO_LEGACY_SYS = "/root/projects/EnzymeCAGE-master"              # historical sys.path of R1_replay_legacy (PC fidelity)
WRAP   = REPO_OLD + "/HPC_Returned_Result_Summaries/d4b1a_wrapper_hash_relative_path_final_package_correction_20260716"

P291   = "/usrdata/EnzymeCAGE_data/workspaces/p291_legacy600m_20260922"
P291_NEW_CFG = P291 + "/runtime/NEW/config.yaml"
P291_ASSETS  = P291 + "/runtime/assets"
WTC    = "/usrdata/EnzymeCAGE_data/workspaces/p298_tc_20260922"
LEGACY_FROZEN_RAW = WR + "/inputs/legacy/pollutant291_p2rank_legacy600m_model_matched_dual5seed_rerun_20260922/results/raw_logits_600m"
LEGACY_ASSET_UNION_TSV = WR + "/inputs/legacy/pollutant291_p2rank_legacy600m_model_matched_dual5seed_rerun_20260922/assets/FULL_3557_UID_ASSET_UNION.tsv"

CKPT_LEGACY_TPL = REPO_OLD + "/HPC_Returned_Result_Summaries/enzymecage_v1_20260714/600m_ensemble/seed_{seed}/best_model.pth"
CKPT_NEW_TPL    = S10 + "/esmc600m/seed_{seed}/best_model.pth"

STORES = {
    "legacy_global_formal": FEAT + "/ESM-C_600M_baseline_1152_round1_20260708/protein_level/seq2feature.pkl",
    "legacy_pocket_native": FEAT + "/ESM-C_600M_baseline_1152_round1_20260708/pocket_node_feature/esm_node_feature.torch.pt",
    "gvp_flat":             FEAT + "/gvp/gvp_protein_feature_flat.pt",
    "corrected_pocket":     FEAT + "/esmc600m_corrected_pocket_107705_20260713/pocket_node_feature/esm_node_feature.torch.pt",
    "gvp_s3_new":           TRAIN + "/03_gvp_assets/gvp_protein_feature_s3_new.pt",
    "gvp_r1_overlay":       WR + "/assets/gvp_r1_overlay.pt",
    "s10_out":              TRAIN + "/04_plm_assets/esmc/out",
    "s11_gen2_out":         WR + "/assets/esmc_gen2/out",
}
RXN = {ctx: R3 + f"/materialize_{ctx}/merged/reaction" for ctx in ("main", "delta15")}
SPLITS = {k: f"/usrdata/EnzymeCAGE_data/pollutant298_original_only_dual_3b_600m_4gpu_20260921/runtime/splits/{k}.csv"
          for k in ("train", "valid", "test")}
ROUTING_PARQUET = TRAIN + "/08_loader_code_smoke_20260924/feature_routes/FEATURE_SOURCE_ROUTING.parquet"
CARRIER_PARQUET = TRAIN + "/02_carrier_uid_and_pocket/SEQUENCE_TO_CARRIER_UID_ALL.parquet"

SEEDS = [40, 41, 42, 43, 44]
ARMS = ("legacy_esmc600m", "new_esmc600m")
CTXS = ("main", "delta15")

def locked_ckpt_table():
    """arm -> seed -> (path, sha256, bytes) from the bundled identity matrix."""
    import csv as _csv
    out = {a: {} for a in ARMS}
    with open(BUNDLE + "/inventory/MODEL_IDENTITIES_27.tsv") as f:
        for r in _csv.DictReader(f, delimiter="\t"):
            if r["arm"] in out:
                out[r["arm"]][int(r["seed"])] = (r["path"], r["sha256"], int(r["bytes"]))
    for a in ARMS:
        assert sorted(out[a]) == SEEDS, f"locked matrix incomplete for {a}"
        assert all(v[1] == v[1] and out[a][s][1] for s in SEEDS for v in [out[a][s]])
    # cross-check against R1 node-side verification
    verified = {}
    with open(R1 + "/work/logs/checkpoint_verify_600m.tsv") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 4:
                verified[(p[0], int(p[1]))] = (p[2], p[3])
    for a in ARMS:
        for s in SEEDS:
            st, sh = verified[(a, s)]
            assert st == "OK" and sh == out[a][s][1], f"R1 verify mismatch {a} seed{s}"
    return out

def store_identity(name, path, n_keys=None, value_sample=None, full_sha=False):
    st = os.stat(path)
    rec = {"name": name, "path": path, "bytes": st.st_size,
           "mtime_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st.st_mtime)),
           "sha256": sha_file(path, sample=not full_sha),
           "sha256_level": "FULL" if full_sha else "SAMPLED_HEAD64K_TAIL64K_SIZE"}
    if n_keys is not None:
        rec["n_keys"] = int(n_keys)
    if value_sample is not None:
        rec["value_sample"] = value_sample
    return rec

# ---------------- no-zero-fill view ----------------
class ThrowingGlobalView(Mapping):
    """Wrap a plain dict so geometric.get_esm_feat cannot silently zero-fill."""
    def __init__(self, base, tag=""):
        self.b = base; self.tag = tag
    def __getitem__(self, k):
        if k in self.b: return self.b[k]
        raise KeyError(f"MISSING_GLOBAL_PLM_FEATURE[{self.tag}]:" + sha_text(str(k))[:16])
    def __contains__(self, k): return k in self.b
    def __iter__(self): return iter(self.b)
    def __len__(self): return len(self.b)

# ---------------- Multi / RouteSeq (VERBATIM from R1_score_cd.py) ----------
class Multi(Mapping):
    def __init__(self, stores): self.stores = stores
    def __getitem__(self, k):
        for st in self.stores:
            if k in st: return st[k]
        raise KeyError(k)
    def __contains__(self, k): return any(k in st for st in self.stores)
    def __iter__(self):
        seen = set()
        for st in self.stores:
            for k in st:
                if k not in seen: seen.add(k); yield k
    def __len__(self): return len(list(iter(self)))

class SourcedMulti(Multi):
    """Multi with per-key source tagging for route-generation consistency."""
    def __init__(self, stores, tags):
        super().__init__(stores); self.tags = tags
    def source_of(self, k):
        for st, tag in zip(self.stores, self.tags):
            if k in st: return tag
        return None

class RouteSeq(Mapping):
    """global view: key = sequence text; NEW stores keyed by sha -> map seq->sha first."""
    def __init__(self, base, sha_map): self.b = base; self.m = sha_map
    def _try(self, k):
        v = self.b.get(k, None)
        if v is not None: return v
        s = self.m.get(k)
        if not s: return None
        # R2 fix vs VERBATIM source: original R1_score_cd RouteSeq raised KeyError
        # here when a mapped sha was absent from every store; the acceptance
        # predicate requires a None return so the miss becomes a TYPED reason
        # (NEW_GLOBAL_MISSING_ALL_ROUTES) instead of a crash. Value semantics
        # for present keys are unchanged.
        try: return self.b[s]
        except KeyError: return None
    def __getitem__(self, k):
        v = self._try(k)
        if v is None: raise KeyError(str(k)[:12])
        return v
    def __contains__(self, k): return self._try(k) is not None
    def __iter__(self): return iter(self.b)
    def __len__(self): return len(self.b)

class SourcedRouteSeq(RouteSeq):
    """RouteSeq over a SourcedMulti base with generation attribution."""
    def source_of(self, seq):
        base = self.b
        stores = base.stores if isinstance(base, SourcedMulti) else [base]
        tags = base.tags if isinstance(base, SourcedMulti) else ["FORMAL"]
        for st, tag in zip(stores, tags):
            if seq in st: return tag
        s = self.m.get(seq)
        if s:
            for st, tag in zip(stores, tags):
                if s in st: return tag
        return None

# ---------------- split-based uid map (PrecomputedAssetIndex pattern) ------
def split_uid_map(pd):
    from collections import defaultdict
    uid_sequences = defaultdict(set)
    for key in ("train", "valid", "test"):
        frame = pd.read_csv(SPLITS[key], usecols=["UniprotID", "sequence"], dtype=str, keep_default_na=False)
        for uid, sequence in frame.itertuples(index=False, name=None):
            uid_sequences[uid].add(sequence)
    ambiguous = frozenset(u for u, s in uid_sequences.items() if len(s) != 1)
    uid_to_sequence = {u: next(iter(s)) for u, s in uid_sequences.items() if len(s) == 1}
    return uid_to_sequence, ambiguous

# ---------------- legacy arm index ------------------------------------------
def build_legacy_index(repo_root, wrapper_root, cfg_path, runtime_map_path, a109_dir):
    """PrecomputedAssetIndex(task cfg) + C95AssetIndex(runtime map), A109 pattern."""
    for p in (repo_root, wrapper_root, a109_dir):
        if p not in sys.path: sys.path.insert(0, p)
    import yaml
    from enzymecage_wrapper.asset_index import PrecomputedAssetIndex
    from c95_asset_index_ext import C95AssetIndex
    cfg = yaml.safe_load(open(cfg_path))
    inner = PrecomputedAssetIndex(cfg)
    inner.sequence_esm = ThrowingGlobalView(inner.sequence_esm, "legacy_formal")
    idx = C95AssetIndex(inner, runtime_map_path)
    return cfg, idx

# ---------------- new arm index ---------------------------------------------
class NewArmIndex:
    """Exposes the PrecomputedAssetIndex interface expected by C95AssetIndex,
    backed by the R1_score_cd.py load_arm('new_esmc600m') assembly (VERBATIM
    store order) + R3 reaction assets + S8 routing tables."""
    def __init__(self, ctx, pd, torch, env_all_cache=True):
        if env_all_cache:
            os.environ.setdefault("ENZYMECAGE_SHARD_CACHE_SIZE", "all")
        from enzymecage.dataset.sharded_protein import _load_sharded_mapping, load_protein_gvp_data
        # ---- protein side (load_arm VERBATIM, with source tags) ----
        self.pocket_store = SourcedMulti(
            [_load_sharded_mapping(STORES["corrected_pocket"]),
             dict((k, v) for i in range(4) for k, v in pickle.load(open(STORES["s10_out"] + f"/esmc_pocket_shard{i}.pkl", "rb")).items()),
             dict((k, v) for i in range(4) for k, v in pickle.load(open(STORES["s11_gen2_out"] + f"/esmc_pocket_shard{i}.pkl", "rb")).items())],
            ["CORRECTED_JULY", "S10_SEPT", "S11_SEPT"])
        formal = pickle.load(open(STORES["legacy_global_formal"], "rb"))
        s10g = dict((k, v) for i in range(4) for k, v in pickle.load(open(STORES["s10_out"] + f"/esmc_global_shard{i}.pkl", "rb")).items())
        s11g = dict((k, v) for i in range(4) for k, v in pickle.load(open(STORES["s11_gen2_out"] + f"/esmc_global_shard{i}.pkl", "rb")).items())
        self.global_store = SourcedMulti([formal, s10g, s11g], ["FORMAL_JULY", "S10_SEPT", "S11_SEPT"])
        self.gvp_store = SourcedMulti(
            [load_protein_gvp_data(STORES["gvp_flat"]),
             load_protein_gvp_data(STORES["gvp_s3_new"]),
             torch.load(STORES["gvp_r1_overlay"], map_location="cpu", weights_only=False)],
            ["FLAT_JULY", "S3_SEPT", "R1_SEPT"])
        self.pocket_node = self.pocket_store
        self.gvp = self.gvp_store
        # RouteSeq view is created per-frame once sha_map is known (set_sha_map)
        self.sequence_esm = ThrowingGlobalView(formal, "new_formal_placeholder")
        self._formal_n = len(formal); self._s10g = s10g; self._s11g = s11g
        # ---- reaction side (R3 per context) ----
        rx = RXN[ctx]
        with open(rx + "/rxn2fp_merged.pkl", "rb") as f: self.rxn_fp = pickle.load(f)
        with open(rx + "/reacting_center_merged.pkl", "rb") as f: self.reaction_centers = pickle.load(f)
        from pathlib import Path
        mdir = Path(rx + "/mol_conformation")
        mtab = pd.read_csv(mdir / "mol2id.csv")
        self.molecule_index = frozenset(mtab["SMILES"].astype(str))
        self.molecule_graphs = torch.load(mdir / "mol_graph_dict.pt", map_location="cpu", weights_only=False)
        if not self.molecule_index.issubset(self.molecule_graphs.keys()):
            raise RuntimeError("molecule graph cache is incomplete; refusing any asset repair")
        # ---- uid map base (splits) ----
        self.uid_to_sequence, self.ambiguous_uids = split_uid_map(pd)
        # ---- S8 routing tables (VERBATIM R1_score_cd) ----
        cseq = pd.read_parquet(CARRIER_PARQUET).drop_duplicates("UniprotID").set_index("UniprotID")
        routing = pd.read_parquet(ROUTING_PARQUET).astype(str)
        self.sha2route = {}
        for r in routing.itertuples():
            self.sha2route.setdefault(r.sequence_sha256, r.UniprotID)
        self.cseq = cseq
        self.ctx = ctx

    def set_sha_map(self, pairs):
        """pairs: list of (sequence_text, sha) for the current frame."""
        self.sequence_esm = SourcedRouteSeq(self.global_store, {s: sh for s, sh in pairs})

    def global_source_of(self, seq):
        v = self.sequence_esm
        return v.source_of(seq) if isinstance(v, SourcedRouteSeq) else None

    # PrecomputedAssetIndex-compatible reaction predicates (VERBATIM math)
    @staticmethod
    def _molecules(reaction_smiles):
        if reaction_smiles.count(">>") != 1: return []
        sides = reaction_smiles.split(">>")
        return [value.replace("*", "C") for side in sides for value in side.split(".") if value and value != "[*H2]"]

    def missing_assets(self, reaction_smiles):
        missing = []
        if reaction_smiles not in self.rxn_fp: missing.append("DRFP reaction fingerprint")
        molecules = self._molecules(reaction_smiles)
        if not molecules or any(m not in self.molecule_index or m not in self.molecule_graphs for m in molecules):
            missing.append("molecule-conformation graph")
        return missing

    def has_reaction(self, reaction_smiles): return not self.missing_assets(reaction_smiles)

    def inventory(self):
        return {"arm": "new_esmc600m", "ctx": self.ctx,
                "pocket_sources": dict(zip(self.pocket_store.tags, [len(s) for s in self.pocket_store.stores])),
                "global_sources": {"FORMAL_JULY": self._formal_n, "S10_SEPT": len(self._s10g), "S11_SEPT": len(self._s11g)},
                "gvp_sources": dict(zip(self.gvp_store.tags, [len(s) for s in self.gvp_store.stores])),
                "drfp_reaction_count": len(self.rxn_fp),
                "molecule_index_count": len(self.molecule_index),
                "molecule_graph_count": len(self.molecule_graphs),
                "query_methods_read_only": True}

GEN_COMPAT = {("CORRECTED_JULY", "FLAT_JULY", "FORMAL_JULY"),
              ("S10_SEPT", "S3_SEPT", "S10_SEPT"),
              ("S11_SEPT", "R1_SEPT", "S11_SEPT"),
              # July pocket/global with Sept GVP or vice versa is NOT allowed.
              }

def new_arm_check(idx, asset_uid, seq, sha):
    """Strict per-row consumer predicate for the new arm.
    Returns (ok: bool, reason: str, sources: dict)."""
    src = {}
    if asset_uid in idx.ambiguous_uids:
        return False, "AMBIGUOUS_UID_IN_SPLITS", src
    p_src = idx.pocket_store.source_of(asset_uid)
    g_src = idx.gvp_store.source_of(asset_uid)
    if p_src is None: return False, "NEW_POCKET_MISSING_ALL_ROUTES", src
    if g_src is None: return False, "NEW_GVP_MISSING_ALL_ROUTES", src
    src = {"pocket": p_src, "gvp": g_src}
    if seq not in idx.sequence_esm:
        return False, "NEW_GLOBAL_MISSING_ALL_ROUTES", src
    src["global"] = idx.global_source_of(seq)
    if (p_src, g_src, src["global"]) not in GEN_COMPAT:
        return False, "ROUTE_GENERATION_MIXED_QUARANTINED", src
    # row pairing closure (C95AssetIndex math): gvp rows == pocket rows <= len(seq)
    try:
        n = int(idx.gvp_store[asset_uid][0].shape[0])
        pr = idx.pocket_store[asset_uid]
        p = int(pr.shape[0]); dim = int(pr.shape[1])
    except (AttributeError, IndexError, TypeError):
        return False, "TENSOR_SHAPE_UNREADABLE", src
    if dim != 1152:
        return False, f"POCKET_DIM_NOT_1152_{dim}", src
    if not (0 < n == p <= len(seq)):
        return False, f"ROW_PAIRING_MISMATCH_gvp{n}_pocket{p}_seqlen{len(seq)}", src
    return True, "OK", src

def legacy_arm_check(idx, uid, seq):
    """Strict per-row consumer predicate for the legacy arm (native July bundle)."""
    if uid in idx.ambiguous_uids:
        return False, "AMBIGUOUS_UID_IN_SPLITS"
    if uid not in idx.gvp: return False, "GVP_FLAT_MISSING"
    if uid not in idx.pocket_node: return False, "LEGACY_POCKET_NATIVE_MISSING"
    if seq not in idx.sequence_esm: return False, "LEGACY_GLOBAL_FORMAL_MISSING"
    try:
        n = int(idx.gvp[uid][0].shape[0])
        pr = idx.pocket_node[uid]
        p = int(pr.shape[0]); dim = int(pr.shape[1])
    except (AttributeError, IndexError, TypeError):
        return False, "TENSOR_SHAPE_UNREADABLE"
    if dim != 1152: return False, f"POCKET_DIM_NOT_1152_{dim}"
    if not (0 < n == p <= len(seq)):
        return False, f"ROW_PAIRING_MISMATCH_gvp{n}_pocket{p}_seqlen{len(seq)}"
    return True, "OK"

def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)
