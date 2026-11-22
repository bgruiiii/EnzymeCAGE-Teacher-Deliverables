#!/usr/bin/env python3
"""R3 consumer integration: overlay-chained asset indices for all three arms +
named rescue routes (no free mixing). Extends the R2 task-local lib; the R2
files are NOT modified (thin extension per prompt: 算法源沿R2 task-local薄扩展).

Route bundles (per-UID identity receipts recorded at slice time):
  NEW600 named routes (pocket, gvp, global):
    JULY_RANK1   = (CORRECTED_JULY, FLAT_JULY, FORMAL_JULY)
    S10_RANK2    = (S10_SEPT, S3_SEPT, S10_SEPT)
    S11_RANK3    = (S11_SEPT, R1_SEPT, S11_SEPT)
    RESCUE_R3D   = (RESCUE_R3D, RESCUE_R3D, any-registered-global)
      — pocket and GVP MUST come from the SAME rescue receipt bundle
        (same ordered indices; rows==len(indices) verified at slice time);
        global is sequence-level (no residue pairing) and follows the route
        priority FORMAL_JULY > S10 > S11 > RESCUE_S10CONTRACT.
  LEGACY named routes:
    L_NATIVE       = (NATIVE_JULY, FLAT_JULY, FORMAL_NATIVE)
    L_SEPT_UNION   = (SEPT_UNION_GENERATED, SEPT_UNION_GENERATED,
                      {FORMAL_NATIVE | SEPT_UNION_GENERATED})
      — union values proven value-identical to native on 1,899 shared keys
        (R2 bridge 60/60 exact); union is native-first merge.
    L_RESCUE_R3D   = (RESCUE_GENERATED_0713, RESCUE_R3D,
                      {FORMAL_NATIVE | RESCUE_GENERATED_0713})
      — legacy pocket sliced via the REAL legacy_indices() compact/BOS contract
        (recipe empirically confirmed vs September union in LEGACY_RECIPE_CONTROL);
        labeled generated, NEVER native.
  3B: R3 merged materialized stores per context (A109-proven consumer path),
      C95AssetIndex extension with the parent runtime map.
"""
import json, os, pickle, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_paths as P
import r2_lib as L2
from r2_lib import Multi, SourcedMulti, RouteSeq, SourcedRouteSeq, ThrowingGlobalView, sha_text, log


class OverlayChain(SourcedMulti):
    """First-wins Mapping over ordered layers with source tags (each loaded once)."""
    pass


def load_overlays():
    ovl = P.NEWROOT + "/overlay"
    out = {}
    for name in ("new600_pocket_rescue", "new600_global_rescue", "legacy_pocket_rescue",
                 "legacy_global_rescue", "gvp_rescue"):
        p = f"{ovl}/{name}.pkl"
        if os.path.exists(p):
            with open(p, "rb") as f:
                out[name] = pickle.load(f)
        else:
            out[name] = {}
    man = f"{ovl}/OVERLAY_MANIFEST.json"
    out["_manifest"] = json.load(open(man)) if os.path.exists(man) else {}
    return out


def load_sept_union():
    sys.path.insert(0, P.REPO_OLD)
    from enzymecage.dataset.sharded_protein import load_pocket_node_feature_data, load_protein_gvp_data
    up = load_pocket_node_feature_data(P.P291_ASSETS + "/esm_node_feature_600m_union.pt")
    ug = load_protein_gvp_data(P.P291_ASSETS + "/gvp_union.pt")
    with open(P.P291_ASSETS + "/seq2feature_600m_union.pkl", "rb") as f:
        uglob = pickle.load(f)
    return up, ug, uglob


# ---------------- NEW ARM v3 ----------------
NEW_GEN_COMPAT = {
    ("CORRECTED_JULY", "FLAT_JULY", "FORMAL_JULY"),
    ("S10_SEPT", "S3_SEPT", "S10_SEPT"),
    ("S11_SEPT", "R1_SEPT", "S11_SEPT"),
    # rescue bundle: pocket+gvp from SAME receipt; global any registered seq-level route
    ("RESCUE_R3D", "RESCUE_R3D", "RESCUE_S10CONTRACT"),
    ("RESCUE_R3D", "RESCUE_R3D", "FORMAL_JULY"),
    ("RESCUE_R3D", "RESCUE_R3D", "S10_SEPT"),
    ("RESCUE_R3D", "RESCUE_R3D", "S11_SEPT"),
}


class NewArmIndexV3(L2.NewArmIndex):
    """NewArmIndex with rescue overlays appended to each chain (gap-fillers only)."""
    def __init__(self, ctx, pd, torch, overlays):
        super().__init__(ctx, pd, torch)
        ov_p = overlays["new600_pocket_rescue"]; ov_g = overlays["new600_global_rescue"]; ov_v = overlays["gvp_rescue"]
        if ov_p:
            self.pocket_store = SourcedMulti(list(self.pocket_store.stores) + [ov_p],
                                             list(self.pocket_store.tags) + ["RESCUE_R3D"])
        if ov_g:
            self.global_store = SourcedMulti(list(self.global_store.stores) + [ov_g],
                                             list(self.global_store.tags) + ["RESCUE_S10CONTRACT"])
        if ov_v:
            self.gvp_store = SourcedMulti(list(self.gvp_store.stores) + [ov_v],
                                          list(self.gvp_store.tags) + ["RESCUE_R3D"])
        self.pocket_node = self.pocket_store
        self.gvp = self.gvp_store
        self.overlays = overlays


def new_arm_check_v3(idx, asset_uid, seq, sha):
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
    if (p_src, g_src, src["global"]) not in NEW_GEN_COMPAT:
        return False, "ROUTE_GENERATION_MIXED_QUARANTINED", src
    if p_src == "RESCUE_R3D" and g_src != "RESCUE_R3D":
        return False, "RESCUE_BUNDLE_MISMATCH", src
    try:
        n = int(idx.gvp_store[asset_uid][0].shape[0])
        pr = idx.pocket_store[asset_uid]
        p = int(pr.shape[0]); dim = int(pr.shape[1])
    except (AttributeError, IndexError, TypeError):
        return False, "TENSOR_SHAPE_UNREADABLE", src
    if dim != 1152: return False, f"POCKET_DIM_NOT_1152_{dim}", src
    if not (0 < n == p <= len(seq)):
        return False, f"ROW_PAIRING_MISMATCH_gvp{n}_pocket{p}_seqlen{len(seq)}", src
    return True, "OK", src


# ---------------- LEGACY ARM v3 ----------------
LEGACY_GEN_COMPAT = {
    ("NATIVE_JULY", "FLAT_JULY", "FORMAL_NATIVE"),
    ("SEPT_UNION_GENERATED", "SEPT_UNION_GENERATED", "FORMAL_NATIVE"),
    ("SEPT_UNION_GENERATED", "SEPT_UNION_GENERATED", "SEPT_UNION_GENERATED"),
    ("NATIVE_JULY", "FLAT_JULY", "SEPT_UNION_GENERATED"),  # union global == native on overlap (bridge-proven)
    ("RESCUE_GENERATED_0713", "RESCUE_R3D", "FORMAL_NATIVE"),
    ("RESCUE_GENERATED_0713", "RESCUE_R3D", "RESCUE_GENERATED_0713"),
    # R4 task-copy extension (LEGACY_COMPAT_EXT_20261103, typed + scoped):
    # rescue pocket (sliced from the receipt-bound node at the bundle indices)
    # + RESCUE_R3D bundle GVP (byte-identical to the value the original 3B
    # merge consumed — MERGE_MANIFEST value_sha256 verified) + September union
    # global (native-first merge; union==native value class bridge-proven on
    # 1,899 shared keys, R2 bridge 60/60 exact). This keeps the same-receipt
    # bundle rule for pocket+GVP and conservatively consumes the EARLIER
    # union global instead of today's rescue global. Affected uids (complete
    # enumeration): A0A224AUZ2 (gold), B6HQT0, G8BHG6.
    ("RESCUE_GENERATED_0713", "RESCUE_R3D", "SEPT_UNION_GENERATED"),
}


class LegacyArmIndexV3:
    """PrecomputedAssetIndex-compatible interface over overlay chains:
    pocket: native -> sept union -> rescue(generated 0713)
    gvp:    flat   -> sept union -> rescue(r3d bundle)
    global (seq-keyed): formal native -> union -> rescue generated
    reaction assets from the R3 per-context merged reaction store.
    uid_to_sequence/ambiguous from the old splits (C95AssetIndex extends)."""
    def __init__(self, pd, torch_mod):
        sys.path.insert(0, P.REPO_OLD)
        from enzymecage.dataset.sharded_protein import load_pocket_node_feature_data, load_protein_gvp_data
        native_pocket = load_pocket_node_feature_data(P.STORES["legacy_pocket_native"])
        flat_gvp = load_protein_gvp_data(P.STORES["gvp_flat"])
        with open(P.STORES["legacy_global_formal"], "rb") as f:
            formal = pickle.load(f)
        up, ug, uglob = load_sept_union()
        ov = load_overlays()
        self.pocket_node = OverlayChain([native_pocket, up, ov["legacy_pocket_rescue"]],
                                        ["NATIVE_JULY", "SEPT_UNION_GENERATED", "RESCUE_GENERATED_0713"])
        self.gvp = OverlayChain([flat_gvp, ug, ov["gvp_rescue"]],
                                ["FLAT_JULY", "SEPT_UNION_GENERATED", "RESCUE_R3D"])
        gchain = OverlayChain([formal, uglob, ov["legacy_global_rescue"]],
                              ["FORMAL_NATIVE", "SEPT_UNION_GENERATED", "RESCUE_GENERATED_0713"])
        self.sequence_esm = _ThrowingSourced(gchain)
        self._gchain = gchain
        from r2_lib import split_uid_map
        self.uid_to_sequence, self.ambiguous_uids = split_uid_map(pd)
        self.overlays = ov
        self.rxn_fp = None

    def bind_reaction(self, ctx, pd, torch_mod):
        import pickle as pk
        from pathlib import Path
        rx = P.RXN[ctx]
        with open(rx + "/rxn2fp_merged.pkl", "rb") as f: self.rxn_fp = pk.load(f)
        with open(rx + "/reacting_center_merged.pkl", "rb") as f: self.reaction_centers = pk.load(f)
        mdir = Path(rx + "/mol_conformation")
        mtab = pd.read_csv(mdir / "mol2id.csv")
        self.molecule_index = frozenset(mtab["SMILES"].astype(str))
        self.molecule_graphs = torch_mod.load(mdir / "mol_graph_dict.pt", map_location="cpu", weights_only=False)
        if not self.molecule_index.issubset(self.molecule_graphs.keys()):
            raise RuntimeError(f"mol graph cache incomplete ctx={ctx}")
        self.ctx = ctx

    @staticmethod
    def _molecules(rxn):
        if rxn.count(">>") != 1: return []
        return [v.replace("*", "C") for side in rxn.split(">>") for v in side.split(".") if v and v != "[*H2]"]

    def missing_assets(self, rxn):
        missing = []
        if rxn not in self.rxn_fp: missing.append("DRFP reaction fingerprint")
        mols = self._molecules(rxn)
        if not mols or any(m not in self.molecule_index or m not in self.molecule_graphs for m in mols):
            missing.append("molecule-conformation graph")
        return missing

    def global_source_of(self, seq):
        return self._gchain.source_of(seq)

    def inventory(self):
        return {"arm": "legacy_esmc600m_v3",
                "pocket_layers": {t: len(s) for s, t in zip(self.pocket_node.stores, self.pocket_node.tags)},
                "gvp_layers": {t: len(s) for s, t in zip(self.gvp.stores, self.gvp.tags)},
                "global_layers": {t: len(s) for s, t in zip(self._gchain.stores, self._gchain.tags)}}


class _ThrowingSourced(ThrowingGlobalView):
    """Throwing view over an OverlayChain; source_of passthrough."""
    def source_of(self, k):
        return self.b.source_of(k) if hasattr(self.b, "source_of") else None


def legacy_arm_check_v3(idx, uid, seq):
    if uid in idx.ambiguous_uids:
        return False, "AMBIGUOUS_UID_IN_SPLITS", {}
    p_src = idx.pocket_node.source_of(uid)
    g_src = idx.gvp.source_of(uid)
    gl_src = idx.global_source_of(seq) if seq in idx.sequence_esm else None
    if p_src is None: return False, "LEGACY_POCKET_MISSING_ALL_ROUTES", {}
    if g_src is None: return False, "LEGACY_GVP_MISSING_ALL_ROUTES", {}
    if gl_src is None: return False, "LEGACY_GLOBAL_MISSING_ALL_ROUTES", {"pocket": p_src, "gvp": g_src}
    src = {"pocket": p_src, "gvp": g_src, "global": gl_src}
    if (p_src, g_src, gl_src) not in LEGACY_GEN_COMPAT:
        return False, "LEGACY_ROUTE_BUNDLE_MIXED_QUARANTINED", src
    try:
        n = int(idx.gvp[uid][0].shape[0])
        pr = idx.pocket_node[uid]
        p = int(pr.shape[0]); dim = int(pr.shape[1])
    except (AttributeError, IndexError, TypeError):
        return False, "TENSOR_SHAPE_UNREADABLE", src
    if dim != 1152: return False, f"POCKET_DIM_NOT_1152_{dim}", src
    if not (0 < n == p <= len(seq)):
        return False, f"ROW_PAIRING_MISMATCH_gvp{n}_pocket{p}_seqlen{len(seq)}", src
    return True, "OK", src
