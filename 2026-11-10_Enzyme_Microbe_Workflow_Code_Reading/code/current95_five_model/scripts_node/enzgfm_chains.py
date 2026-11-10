#!/usr/bin/env python3
"""R4 shared EnzGFM consumption chains — the EXACT chain topology verified by
verify_enzgfm_arms.py, factored for reuse by the scoring adapter so that the
consumer proof and the scorer consume identical objects.

Chains (first-wins, source-tagged):
  pocket(uid): BASE_V6_MERGED -> R1_MERGED_{MAIN,SUPP,SUPP2} -> RESCUE_R4_TASK
               -> RESCUE_LANE_OLDR3 -> RESCUE_LANE_S5
  global(seq): BASE_V6_MERGED -> R1_MERGED_* -> RESCUE_R4_TASK (exact-seq keys)
               -> lane {seq_sha}.npy dirs (RESCUE_LANE_*)
  gvp(uid):    FLAT_JULY -> S3_SEPT -> R1_SEPT -> RESCUE_R3D (this round's
               gvp_rescue overlay) -> BUNDLE_DIRECT (registered lane files)
  E0 lane:     frozen p2_assets views (BASE+P1 delta, FORMAL_GVP, P0 universe)
Reaction assets are bound separately by the caller (R3 merged per-ctx, the
unified five-arm representation of this round).
"""
import csv, glob, hashlib, json, os, pickle, sys
from collections.abc import Mapping

import numpy as np
import pandas as pd
import torch

_NEWROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PKG = _NEWROOT + "/current95_five_model_complete_prep_20261103"
if _PKG + "/sources" not in sys.path:
    sys.path.insert(0, _PKG + "/sources")
import r3_paths as P

TRAIN = "/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922"
E0RUN = "/usrdata/EnzymeCAGE_data/training_runs/enzymecage_enzgfm_old_formal_plus_brenda_20260928"
W2CODE = E0RUN + "/02_fasttrack_p2_p4_typed_exclusion_training_20260929/code"
WR = TRAIN + "/s11_r1_self_included_four_model_20260927"
INV = _NEWROOT + "/runtime/enzgfm_inventory"
EXTR = _NEWROOT + "/runtime/enzgfm_extraction/shard_000_of_001"
sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()


def build_task_overlay():
    task_pocket, task_global, task_src = {}, {}, {}
    for cp in sorted(glob.glob(EXTR + "/chunks/chunk_*.pt")):
        obj = torch.load(cp, map_location="cpu", weights_only=False)
        assert obj.get("__format__") == "enzgfm650m_feature_chunk_v1"
        for uid, e in obj["entries"].items():
            task_pocket[uid] = e["pocket_feature"]
            task_global[e["sequence"]] = e["global_feature"]
            task_src[uid] = {"chunk": os.path.basename(cp), "seq_sha": e["sequence_sha256"],
                             "indices_n": len(e["pocket_indices_1based"]), "pocket_source": e.get("pocket_source", "")}
        del obj
    man_sha = hashlib.sha256(open(EXTR + "/RUN_MANIFEST.json", "rb").read()).hexdigest()
    return task_pocket, task_global, task_src, man_sha


def build_lane_maps():
    lane_receipts = {}
    with open(INV + "/ENZGFM_LANE_RECEIPTS.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            lane_receipts.setdefault(r["uid"], r)
    lane_pocket, lane_global = {}, {}
    for lname, ovl in (("OLDR3", P.OLDR3 + "/overlay"), ("S5", P.S5 + "/overlay")):
        tag = "RESCUE_LANE_" + lname
        for fn in os.listdir(ovl + "/pocket/new_enzgfm650m"):
            if fn.endswith(".npy") and "__" in fn:
                sha64, uid = fn[:-4].split("__", 1)
                lane_pocket.setdefault(uid, (os.path.join(ovl, "pocket/new_enzgfm650m", fn), tag, sha64))
        for fn in os.listdir(ovl + "/global/new_enzgfm650m"):
            if fn.endswith(".npy"):
                lane_global.setdefault(fn[:-4], (os.path.join(ovl, "global/new_enzgfm650m", fn), tag))
    return lane_receipts, lane_pocket, lane_global


class R1Chains:
    def __init__(self, lsm, load_gvp):
        os.environ.setdefault("ENZYMECAGE_SHARD_CACHE_SIZE", "all")
        self.task_pocket, self.task_global, self.task_src, self.task_manifest_sha = build_task_overlay()
        self.lane_receipts, self.lane_pocket, self.lane_global = build_lane_maps()
        self.base_p = lsm(TRAIN + "/04_plm_assets/enzgfm/merged/pocket_node_feature/enzgfm_node_feature.torch.pt")
        self.wr_p = [lsm(WR + f"/assets/enzgfm/{r}/pocket_node_feature/enzgfm_node_feature.torch.pt")
                     for r in ("merged_main", "merged_supp", "merged_supp2")]
        self.base_g = pickle.load(open(TRAIN + "/04_plm_assets/enzgfm/merged/protein_level/seq2feature.pkl", "rb"))
        self.wr_g = [pickle.load(open(WR + f"/assets/enzgfm/{r}/protein_level/seq2feature.pkl", "rb"))
                     for r in ("merged_main", "merged_supp", "merged_supp2")]
        self.POCKET_STORES = [self.base_p] + self.wr_p + [self.task_pocket]
        self.POCKET_TAGS = ["BASE_V6_MERGED", "R1_MERGED_MAIN", "R1_MERGED_SUPP", "R1_MERGED_SUPP2", "RESCUE_R4_TASK"]
        self.GLOBAL_STORES = [self.base_g] + self.wr_g + [self.task_global]
        self.GLOBAL_TAGS = ["BASE_V6_MERGED", "R1_MERGED_MAIN", "R1_MERGED_SUPP", "R1_MERGED_SUPP2", "RESCUE_R4_TASK"]
        self.gvp_flat = load_gvp(P.STORES["gvp_flat"])
        self.gvp_s3 = torch.load(P.STORES["gvp_s3_new"], map_location="cpu", weights_only=False)
        self.gvp_r1 = torch.load(P.STORES["gvp_r1_overlay"], map_location="cpu", weights_only=False)
        self.gvp_rescue = pickle.load(open(_NEWROOT + "/overlay/gvp_rescue.pkl", "rb"))
        self.bundle_files = {}
        for root in (P.R3 + "/overlays/gvp_r3d", P.OLDR3 + "/overlay/gvp", P.S5 + "/overlay/gvp",
                     P.WS + "/runtime/main/R3_task/R3_structure_protein/overlay/gvp",
                     P.WS + "/runtime/delta15/R3_task/R3_structure_protein/overlay/gvp"):
            if not os.path.isdir(root): continue
            for fn in os.listdir(root):
                if fn.endswith(".gvp.pt"):
                    self.bundle_files.setdefault(fn[:-7].split("_", 1)[1], os.path.join(root, fn))
        self.GVP_CHAIN = [("FLAT_JULY", self.gvp_flat), ("S3_SEPT", self.gvp_s3),
                          ("R1_SEPT", self.gvp_r1), ("RESCUE_R3D", self.gvp_rescue)]
        # route tables (R1_score_cd VERBATIM sources)
        self.cseq = pd.read_parquet(P.CARRIER_PARQUET).drop_duplicates("UniprotID").set_index("UniprotID")
        routing = pd.read_parquet(TRAIN + "/08_loader_code_smoke_20260924/feature_routes/FEATURE_SOURCE_ROUTING.parquet").astype(str)
        self.sha2route = {}
        for r in routing.itertuples():
            self.sha2route.setdefault(r.sequence_sha256, r.UniprotID)
        self.r1seq = {}
        for f_ in glob.glob(WR + "/assets/CARRIER_*.csv"):
            d = pd.read_csv(f_, dtype=str)
            for r in d.itertuples():
                self.r1seq[r.UniprotID] = r.sequence

    def pocket_get(self, uid):
        for st, tag in zip(self.POCKET_STORES, self.POCKET_TAGS):
            if uid in st:
                return np.asarray(st[uid], dtype=np.float32), tag
        lp = self.lane_pocket.get(uid)
        if lp:
            return np.load(lp[0]).astype(np.float32), lp[1]
        return None, None

    def global_get(self, seq):
        for st, tag in zip(self.GLOBAL_STORES, self.GLOBAL_TAGS):
            if seq in st:
                return np.asarray(st[seq], dtype=np.float32), tag, "TEXT"
        lg = self.lane_global.get(sha_text(seq))
        if lg:
            return np.load(lg[0]).astype(np.float32), lg[1], "SHA"
        return None, None, None

    def gvp_get(self, uid):
        for tag, st in self.GVP_CHAIN:
            if uid in st:
                v = st[uid]
                return (tuple(v) if not isinstance(v, tuple) else v), tag
        bf = self.bundle_files.get(uid)
        if bf:
            v = torch.load(bf, map_location="cpu", weights_only=False)
            v = v[uid] if isinstance(v, dict) and uid in v else v
            return tuple(v), "BUNDLE_DIRECT"
        return None, None

    def route_uid(self, uid, sh):
        """audited substitution: sha2route + carrier/r1 sequence-sha binding."""
        ru = self.sha2route.get(sh)
        if ru and ru != uid:
            cseqv = self.cseq.loc[ru, "sequence"] if ru in self.cseq.index else self.r1seq.get(ru)
            if cseqv is not None and sha_text(str(cseqv)) == sh:
                return ru
        return None

    def inventory(self):
        return {"task_uids": len(self.task_pocket), "task_manifest_sha256": self.task_manifest_sha,
                "lane_receipts": len(self.lane_receipts), "lane_pocket_uids": len(self.lane_pocket),
                "lane_global_shas": len(self.lane_global),
                "gvp_layers": {"FLAT_JULY": len(list(self.gvp_flat.keys())), "S3_SEPT": len(self.gvp_s3),
                                "R1_SEPT": len(self.gvp_r1), "RESCUE_R3D": len(self.gvp_rescue),
                                "BUNDLE_DIRECT": len(self.bundle_files)}}


def build_e0_lane():
    if W2CODE not in sys.path:
        sys.path.insert(0, W2CODE)
    import p2_assets as A
    st = A.load_p2_stores()
    views, uni = A.build_views(st)
    closure = A.e0_required_closure(views, uni)
    uni_seq = dict(zip(uni.uid, uni.sequence))
    uni_sha = dict(zip(uni.uid, uni.sequence_sha256))
    return views, uni_seq, uni_sha, closure


def tensor_ok(a, dim):
    a = np.asarray(a, dtype=np.float64)
    if not np.isfinite(a).all(): return False, "nonfinite"
    if a.ndim == 1 and a.shape[0] != dim: return False, "dim"
    if a.ndim == 2 and a.shape[1] != dim: return False, "dim"
    if float(np.abs(a).max()) == 0.0: return False, "allzero"
    return True, ""
