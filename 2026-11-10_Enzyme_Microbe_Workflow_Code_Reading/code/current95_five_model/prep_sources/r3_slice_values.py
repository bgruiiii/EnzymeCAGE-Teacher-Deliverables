#!/usr/bin/env python3
"""R3 dual-recipe CPU slicing of generated/cached raw nodes into per-arm overlay
stores with FULL per-UID identity receipts.

Recipes (never shared values, separately labeled):
  NEW600 : pocket = node[1-based biological untrimmed indices]  (S10/S11 contract,
           verbatim R1_esmc_bulk2 formula), global = node.mean(0) float32.
           Label: RESCUE_R3D_* / RESCUE_S10CONTRACT_GLOBAL.
  LEGACY : pocket = node[legacy compact indices] via the REAL legacy_indices()
           contract (pocket-only PDB + derived pocket_info; BOS-once/EOS-never
           defect preserved; status must be OK — no shortcut), global =
           node.mean(0). Labels: LEGACY_GENERATED_R3D_RESCUE (0713 weights),
           never native.
  GVP    : rescue overlay files reused READ-ONLY from registered roots; rows
           verified against indices count at slice time (real check, not receipt
           text only).

RECIPE CONTROL (gates legacy rescue): for UIDs present in the September union
pocket AND with a p291 seq_nodes raw cache, verify union_pocket[uid] ==
node_cache[0:rows] EXACTLY (float32). This empirically confirms the
full-sequence-node + compact-prefix-slice recipe against the September
VERIFIED generated route before applying it to rescue UIDs. Control failure
=> legacy rescue suspended (typed), new600 unaffected.

Outputs: NEWROOT/overlay/{new600_pocket_rescue,new600_global_rescue,
legacy_pocket_rescue,legacy_global_rescue,gvp_rescue}.pkl (atomic),
SLICE_RECEIPTS.jsonl (per-UID full identity), SLICE_SUMMARY.json.
Resume: receipts with verified outputs skip re-slicing (identity-checked).
"""
import csv, glob, hashlib, json, os, pickle, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_paths as P
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "scripts"))
import recovery_helpers as RH
sys.path.insert(0, P.BUNDLE + "/historical/legacy")
from legacy_index_lib import legacy_indices, STD

t0 = time.time()
def log(*a): print(f"[{time.time()-t0:6.1f}s]", *a, flush=True)
EXT = P.NEWROOT + "/runtime/extraction"
CACHE = EXT + "/cache_nodes"
OVL = P.NEWROOT + "/overlay"; os.makedirs(OVL, exist_ok=True)
RECEIPTS = OVL + "/SLICE_RECEIPTS.jsonl"
sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()
arr_sha = lambda a: hashlib.sha256(np.ascontiguousarray(a, dtype=np.float32).tobytes()).hexdigest()

# ---------- load state + worklists ----------
uid_state = {}
import gzip
with gzip.open(P.NEWROOT + "/runtime/ledger/UID_ASSET_STATE.tsv.gz", "rt") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        uid_state[r["uid"]] = r
log("uid states:", len(uid_state))

# sequences
sha2seq = {}
for ctx in P.CTXS:
    with open(f"{P.PKG}/inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            sha2seq[r["sequence_sha256"]] = r["sequence"]

# node receipts (verified generations)
node_rec = {}
if os.path.exists(EXT + "/NODE_RECEIPTS.jsonl"):
    with open(EXT + "/NODE_RECEIPTS.jsonl") as f:
        for line in f:
            if line.strip():
                r = json.loads(line); node_rec[r["seq_sha256"]] = r
log("node receipts:", len(node_rec))

# indices sources: pocket_ok scans + carrier + corrected jsonl
indices = {}   # uid -> dict(indices, source, seq_sha, structure_sha, pocket_pdb_sha, pdb_path)
def scan_pocket_ok(rootdir, tag, cluster_pattern):
    n = 0
    for p in glob.glob(rootdir + "/*/pocket_ok.json"):
        try:
            j = json.load(open(p))
            u = j.get("uid") or os.path.basename(os.path.dirname(p))
            idx = j.get("untrimmed_indices")
            if not u or not idx or u in indices: continue
            d = os.path.dirname(p)
            # R4 adaptation (PDB_BINDING_20261103): source-aware pdb binding.
            # The pocket_ok receipt records its producer: P2Rank_* -> the lane's
            # {uid}_p2rank_cluster.pdb (R3D-proven legacy contract input);
            # ALPHAFILL_* -> the pocketw extraction pdb (OLDR3-manifest-proven).
            # cluster_pattern may be a single pattern or ordered candidates.
            pats = cluster_pattern if isinstance(cluster_pattern, (list, tuple)) else \
                ([cluster_pattern] if cluster_pattern else [])
            _src = str(j.get("source", ""))
            if _src.startswith("P2Rank"):
                pats = sorted(pats, key=lambda x: 0 if "p2rank" in x else 1)
            elif _src.startswith("ALPHAFILL"):
                pats = sorted(pats, key=lambda x: 0 if "pocketw" in x else 1)
            pdb = None
            for pat in pats:
                c = pat.format(dir=d, uid=u)
                if os.path.exists(c):
                    pdb = c
                    break
            indices[u] = {"indices": [int(x) for x in idx], "source": tag,
                          "seq_sha": j.get("structure_sha256", "") and j.get("sequence_sha256", "") or j.get("sequence_sha256", ""),
                          "structure_sha": j.get("structure_sha256", ""),
                          "pocket_pdb_sha": j.get("pocket_pdb_sha256", ""),
                          "pdb_path": pdb}
            n += 1
        except Exception:
            pass
    return n
n1 = scan_pocket_ok(P.R3 + "/struct_r3d/work/struct", "R3D_P2RANK_20261101", "{dir}/{uid}_p2rank_cluster.pdb")
n2 = scan_pocket_ok(P.OLDR3 + "/struct_lane/work/struct", "OLDR3_STRUCT_LANE_20261008",
                    ["{dir}/pocketw/pocket/{uid}.pdb", "{dir}/{uid}_p2rank_cluster.pdb"])
n3 = scan_pocket_ok(P.S5 + "/struct_lane/work/struct", "S5_STRUCT_LANE_20261006",
                    ["{dir}/pocketw/pocket/{uid}.pdb", "{dir}/{uid}_p2rank_cluster.pdb"])
# --- R4 source recovery (task-copy adaptation SOURCE_RECOVERY_20261103) -------
# Original-3B merge-manifest lanes missing from the R3 scan set (see ledger
# patch of the same name): task_r3_overlay_new struct lane, S5 historical
# recheck receipts, R3C pair-adjudicated evidence indices.
n4 = scan_pocket_ok(P.WS + "/runtime/main/R3_task/R3_structure_protein/struct_lane/work/struct",
                    "R3_TASK_NEW_MAIN", "{dir}/pocketw/pocket/{uid}.pdb")
n5 = scan_pocket_ok(P.WS + "/runtime/delta15/R3_task/R3_structure_protein/struct_lane/work/struct",
                    "R3_TASK_NEW_DELTA15", "{dir}/pocketw/pocket/{uid}.pdb")
n6 = 0
for _p in glob.glob(P.S5 + "/struct_lane/work/struct/*/pocket_ok_hist.json"):
    try:
        _j = json.load(open(_p))
        _u = _j.get("uid") or os.path.basename(os.path.dirname(_p))
        _idx = _j.get("untrimmed_indices")
        if not _u or not _idx or _u in indices: continue
        _d = os.path.dirname(_p)
        _pdb = _d + "/" + _u + "_hist.pdb"
        indices[_u] = {"indices": [int(x) for x in _idx], "source": "S5_HIST_RECHECK",
                       "seq_sha": _j.get("sequence_sha256", ""), "structure_sha": _j.get("structure_sha256", ""),
                       "pocket_pdb_sha": _j.get("pocket_pdb_sha256", ""),
                       "pdb_path": _pdb if os.path.exists(_pdb) else None}
        n6 += 1
    except Exception:
        pass
n7 = 0
_r3c_wl = P.R3 + "/pair_adjudications/PAIR_REPAIR_WORKLIST.tsv"
if os.path.isfile(_r3c_wl):
    with open(_r3c_wl) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            _u = r.get("uid", "")
            if not _u or _u in indices: continue
            if not str(r.get("verdict", "")).startswith("PASS"): continue
            _evp = r.get("evidence_file", "")
            if not _evp or not os.path.isfile(_evp): continue
            try:
                _ev = json.load(open(_evp))
                _idx = [int(x) for x in _ev["mapped_1based_indices"]]
                if hashlib.sha256(json.dumps(_idx).encode()).hexdigest() != _ev.get("indices_sha256"): continue
                _pdb = _ev.get("pdb_path", "")
                if not _pdb or not os.path.isfile(_pdb): continue
                if hashlib.sha256(open(_pdb, "rb").read()).hexdigest() != _ev.get("pdb_sha256"): continue
                indices[_u] = {"indices": _idx, "source": "R3C_PAIR_ADJUDICATED",
                               "seq_sha": r.get("sequence_sha256", ""), "structure_sha": _ev.get("pdb_sha256", ""),
                               "pocket_pdb_sha": _ev.get("pdb_sha256", ""), "pdb_path": _pdb}
                n7 += 1
            except Exception:
                pass
# historical-recheck receipts (pocket_ok_hist.json) in OLDR3 / R3_task lanes;
# pdb = {uid}_hist.pdb beside the receipt (Q8KN40: hist pdb sha == S5 GVP
# manifest recorded pdb — same-structure entity proof)
n8 = 0
for _root, _tag in ((P.OLDR3 + "/struct_lane/work/struct", "OLDR3_HIST_RECHECK"),
                    (P.WS + "/runtime/main/R3_task/R3_structure_protein/struct_lane/work/struct", "R3_TASK_NEW_HIST_MAIN"),
                    (P.WS + "/runtime/delta15/R3_task/R3_structure_protein/struct_lane/work/struct", "R3_TASK_NEW_HIST_DELTA15")):
    for _p in glob.glob(_root + "/*/pocket_ok_hist.json"):
        try:
            _j = json.load(open(_p))
            _u = _j.get("uid") or os.path.basename(os.path.dirname(_p))
            _idx = _j.get("untrimmed_indices")
            if not _u or not _idx or _u in indices: continue
            _d = os.path.dirname(_p)
            _pdb = _d + "/" + _u + "_hist.pdb"
            indices[_u] = {"indices": [int(x) for x in _idx], "source": _tag,
                           "seq_sha": _j.get("sequence_sha256", ""), "structure_sha": _j.get("structure_sha256", ""),
                           "pocket_pdb_sha": _j.get("pocket_pdb_sha256", ""),
                           "pdb_path": _pdb if os.path.exists(_pdb) else None}
            n8 += 1
        except Exception:
            pass
# oldR3/S5 manifest pdb paths
try:
    dm = json.load(open(P.OLDR3 + "/GVP_DELTA_MANIFEST.json"))
    for k, v in dm.items():
        if v.get("status") == "SUCCESS" and "|" in k:
            u = k.split("|", 1)[1]
            if u in indices and not indices[u]["pdb_path"] and v.get("pdb") and os.path.exists(v["pdb"]):
                indices[u]["pdb_path"] = v["pdb"]
                indices[u]["pdb_sha256_manifest"] = v.get("pdb_sha256", "")
except Exception as e: log("oldr3 manifest:", e)
try:
    sm = json.load(open(P.S5 + "/gvp_manifests/GVP_MANIFEST_full.json"))
    for k, v in sm.items():
        if v.get("status") == "SUCCESS" and "|" in k:
            u = k.split("|", 1)[1]
            if u in indices and not indices[u]["pdb_path"] and v.get("pdb") and os.path.exists(v["pdb"]):
                indices[u]["pdb_path"] = v["pdb"]
except Exception as e: log("s5 manifest:", e)
# R4 source recovery: R3_task lane GVP delta manifests (pdb path binding)
for _ctx in ("main", "delta15"):
    try:
        tm = json.load(open(P.WS + f"/runtime/{_ctx}/R3_task/R3_structure_protein/GVP_DELTA_MANIFEST.json"))
        for k, v in tm.items():
            if v.get("status") == "SUCCESS" and "|" in k:
                u = k.split("|", 1)[1]
                if u in indices and not indices[u]["pdb_path"] and v.get("pdb") and os.path.exists(v["pdb"]):
                    indices[u]["pdb_path"] = v["pdb"]
                    indices[u]["pdb_sha256_manifest"] = v.get("pdb_sha256", "")
    except Exception as e: log("r3_task manifest:", _ctx, e)
log("indices receipts: r3d", n1, "oldr3", n2, "s5", n3, "r3_task", n4 + n5,
    "s5_hist", n6, "r3c", n7, "hist_oldr3_r3task", n8, "total", len(indices))
import pandas as pd
cdf = pd.read_parquet(P.CARRIER_PARQUET)
carrier_idx = {}
for r in cdf.itertuples(index=False):
    carrier_idx.setdefault(str(r.UniprotID), [int(x) for x in str(r.pocket_indices_1based).split(",") if x != ""])
corr_idx = {}
with open(P.CORR_JSONL) as f:
    for line in f:
        if line.strip():
            j = json.loads(line); corr_idx[j["UniprotID"]] = [int(x) for x in j["corrected_untrimmed_indices"]]
log("carrier:", len(carrier_idx), "corrected:", len(corr_idx))

# gvp overlay files
gvp_files = {}
for root, tag in ((P.R3 + "/overlays/gvp_r3d", "GVP_R3D"),
                  (P.OLDR3 + "/overlay/gvp", "GVP_OLDR3"),
                  (P.S5 + "/overlay/gvp", "GVP_S5"),
                  # R4 source recovery: task_r3_overlay_new producer lane
                  (P.WS + "/runtime/main/R3_task/R3_structure_protein/overlay/gvp", "GVP_R3_TASK_NEW"),
                  (P.WS + "/runtime/delta15/R3_task/R3_structure_protein/overlay/gvp", "GVP_R3_TASK_NEW")):
    if not os.path.isdir(root): continue
    for fn in os.listdir(root):
        if fn.endswith(".gvp.pt"):
            u = fn[:-7].split("_", 1)[1]
            gvp_files.setdefault(u, (os.path.join(root, fn), tag))
log("gvp overlay files:", len(gvp_files))

import torch
_real_gvp_cache = {}
# R4 adaptation (NODE_FIX_20261103): the bundled patch imports the repo loader
# for store-fallback GVP rows; REPO_OLD must be on sys.path first (the ledger
# script does the same).
if P.REPO_OLD not in sys.path:
    sys.path.insert(0, P.REPO_OLD)
from enzymecage.dataset.sharded_protein import load_protein_gvp_data
for _uid, _b in RH.recovery_bundles(P.PKG).items():
    indices[_uid] = {"indices": _b["indices"], "source": "A109_VERIFIED_RECOVERY", "seq_sha": _b["seq_sha256"],
                     "structure_sha": _b["structure_sha256"], "pocket_pdb_sha": _b["pdb_sha256"], "pdb_path": _b["pdb"]}
    gvp_files[_uid] = (_b["gvp"], "A109_VERIFIED_RECOVERY")
def load_gvp(uid):
    fp = gvp_files.get(uid)
    if not fp:
        src = uid_state.get(uid, {}).get("gvp_rescue_source")
        if src in ("FLAT_JULY", "S3_SEPT", "R1_SEPT"):
            val, rows, filename = RH.actual_gvp(uid, src, P, torch, load_protein_gvp_data, _real_gvp_cache)
            return val, (filename, src)
        return None, None
    v = torch.load(fp[0], map_location="cpu", weights_only=False)
    if isinstance(v, dict) and uid in v: v = v[uid]
    return v, fp

# Preserve the already-generated R3 nodes instead of re-extracting them.
_previous_node_receipts = {}
_previous_receipt_file = P.PREVROOT + "/runtime/extraction/NODE_RECEIPTS.jsonl"
if os.path.isfile(_previous_receipt_file):
    for _line in open(_previous_receipt_file):
        if _line.strip():
            _rec = json.loads(_line)
            _previous_node_receipts[_rec["seq_sha256"]] = _rec
# p291 seq_nodes cache
seq_nodes_dir = P.P291 + "/assets/seq_nodes"

def get_node(sha, seqlen):
    """verified node: generated receipt first, then p291 seq_nodes cache (identity-gated)."""
    p = f"{CACHE}/{sha}.npy"
    r = node_rec.get(sha)
    if r and os.path.exists(p):
        n = np.load(p)
        if n.shape == (seqlen + 2, 1152) and np.isfinite(n).all() and r.get("seqlen") == seqlen:
            return n, "GENERATED_R3", r
    prior = P.PREVROOT + f"/runtime/extraction/cache_nodes/{sha}.npy"
    prior_receipt = _previous_node_receipts.get(sha)
    if prior_receipt and os.path.isfile(prior):
        n = np.load(prior)
        if (prior_receipt.get("weight_sha256") == P.ESMC_WEIGHTS_SHA and n.shape == (seqlen + 2, 1152)
                and np.isfinite(n).all() and arr_sha(n) == prior_receipt.get("node_value_sha256")):
            return n, "GENERATED_R3", prior_receipt
    cp = f"{seq_nodes_dir}/{sha}.npz"
    if os.path.exists(cp):
        try:
            z = np.load(cp)
            n = z["node"].astype(np.float32)
            if n.shape == (seqlen + 2, 1152) and np.isfinite(n).all():
                rec = {"source": "P291_SEQ_NODES_CACHE", "file_sha256": hashlib.sha256(open(cp, 'rb').read()).hexdigest()}
                return n, "P291_SEQ_NODES_CACHE_RESLICE", rec
        except Exception:
            pass
    return None, "NODE_UNAVAILABLE", None

# ---------- RECIPE CONTROL: union pocket == node_cache[0:rows] ----------
log("recipe control: September union vs raw-node-cache prefix slice ...")
union_pocket = None
control = {"checked": 0, "exact_equal": 0, "mismatch_examples": [], "verdict": ""}
try:
    sys.path.insert(0, P.REPO_OLD)
    from enzymecage.dataset.sharded_protein import load_pocket_node_feature_data
    union_pocket = load_pocket_node_feature_data(P.P291_ASSETS + "/esm_node_feature_600m_union.pt")
    n_checked = 0
    for u in sorted(union_pocket.keys()):
        if n_checked >= 20: break
        stt = uid_state.get(u)
        seq = None
        sha = None
        # union uid may not be in parent universe; find its sequence via splits-independent sources: p291 u2s not registered here -> use carrier/cseq or runtime map
        if stt:
            sha = stt["seq_sha"]; seq = sha2seq.get(sha)
        if seq is None:
            if u in carrier_idx:
                row = cdf[cdf.UniprotID == u]
                if len(row): seq = str(row.iloc[0]["sequence"]); sha = str(row.iloc[0]["sequence_sha256"])
        if seq is None: continue
        cp = f"{seq_nodes_dir}/{sha}.npz"
        if not os.path.exists(cp): continue
        z = np.load(cp); node = z["node"].astype(np.float32)
        pv = np.asarray(union_pocket[u], dtype=np.float32)
        rows = pv.shape[0]
        if node.shape[0] < rows: continue
        prefix = node[0:rows]
        eq = prefix.shape == pv.shape and np.array_equal(prefix, pv)
        control["checked"] += 1
        control["exact_equal"] += int(eq)
        if not eq and len(control["mismatch_examples"]) < 5:
            control["mismatch_examples"].append({"uid": u, "rows": rows,
                                                 "max_abs_delta": float(np.max(np.abs(prefix - pv))) if prefix.shape == pv.shape else None})
        n_checked += 1
    control["verdict"] = ("RECIPE_CONFIRMED_union_pocket_equals_node_prefix" if control["checked"] >= 5 and control["exact_equal"] == control["checked"]
                          else "RECIPE_CONTROL_INCONCLUSIVE_OR_FAILED")
except Exception as e:
    control["verdict"] = "RECIPE_CONTROL_ERROR"
    control["error"] = repr(e)[:300]
json.dump(control, open(OVL + "/LEGACY_RECIPE_CONTROL.json", "w"), indent=1)
log("recipe control:", control["verdict"], control["checked"], "checked,", control["exact_equal"], "equal")
LEGACY_RESCUE_ALLOWED = control["verdict"].startswith("RECIPE_CONFIRMED")

# ---------- resume state ----------
sliced = {}
if os.path.exists(RECEIPTS):
    os.replace(RECEIPTS, RECEIPTS + ".run1")
if os.path.exists(RECEIPTS):
    with open(RECEIPTS) as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                if r.get("status") == "SLICED_OK": sliced[r["uid"]] = r

# ---------- main slicing ----------
def _previous_overlay(name):
    p = P.PREVROOT + "/overlay/" + name + ".pkl"
    return pickle.load(open(p, "rb")) if os.path.isfile(p) else {}
new_pocket = _previous_overlay("new600_pocket_rescue")
new_global = _previous_overlay("new600_global_rescue")
leg_pocket = _previous_overlay("legacy_pocket_rescue")
leg_global = _previous_overlay("legacy_global_rescue")
gvp_merged = _previous_overlay("gvp_rescue")
summary = {"uids_processed": 0, "new600_pocket": 0, "new600_global": 0, "legacy_pocket": 0, "legacy_global": 0,
           "gvp_merged": 0, "typed": {}}
def typed(k): summary["typed"][k] = summary["typed"].get(k, 0) + 1

# tier ordering
def tier_of(u):
    t = uid_state.get(u, {}).get("priority_tier", "T9")
    try: return (int(t[1]), int(t.split("_")[-1]) if t.startswith("T1") else 0)
    except Exception: return (9, 0)

# need = uids whose repair actions explicitly require SLICING work
# (NEW_RESCUE_SLICE_* or LEGACY_RESCUE_GENERATION_*). Uids covered by
# sept-union reuse / store-ready / blocked-typed are NOT slice targets
# (the first run over-included them, producing spurious NODE_UNAVAILABLE types).
need = []
for u, st in uid_state.items():
    acts = st.get("repair_actions", "")
    if "NEW_RESCUE_SLICE" in acts or "LEGACY_RESCUE_GENERATION" in acts:
        need.append(u)
need.sort(key=tier_of)
log("rescue candidates:", len(need))

typed_rows = []
rec_f = open(RECEIPTS, "a")
for u in need:
    st = uid_state[u]
    sha = st["seq_sha"]; seq = sha2seq.get(sha)
    if seq is None:
        typed("NO_SEQUENCE_IN_PARENT_MAP"); typed_rows.append([u, "NO_SEQUENCE_IN_PARENT_MAP"]); continue
    if u in sliced:
        # restore from previous run receipts if outputs still hold (rebuild below anyway from caches)
        pass
    idx_entry = indices.get(u)
    idxs = idx_entry["indices"] if idx_entry else carrier_idx.get(u)
    idx_src = idx_entry["source"] if idx_entry else ("CARRIER_S10" if u in carrier_idx else None)
    if idxs is None:
        # corrected indices (July cohort) as last registered source
        if u in corr_idx: idxs, idx_src = corr_idx[u], "CORRECTED_JULY"
    if idxs is None:
        typed("NO_ORDERED_INDICES_ANY_SOURCE"); typed_rows.append([u, "NO_ORDERED_INDICES_ANY_SOURCE"]); continue
    node, node_src, nrec = get_node(sha, len(seq))
    if node is None:
        _t = "NODE_UNAVAILABLE_" + ("T1" if tier_of(u)[0] == 1 else "LATER")
        typed(_t); typed_rows.append([u, _t + f"|sha={sha}|actions={uid_state[u].get('repair_actions','')}"]); continue
    # GVP real rows check
    gvp_val, gfp = load_gvp(u)
    gvp_rows = None; gvp_src = st.get("gvp_rescue_source", "")
    if gvp_val is not None:
        try: gvp_rows = int(gvp_val[0].shape[0])
        except Exception: gvp_rows = None
    if gvp_rows is None:
        typed("GVP_VALUE_UNREADABLE"); typed_rows.append([u, "GVP_VALUE_UNREADABLE"]); continue
    if gvp_rows != len(idxs):
        typed(f"GVP_ROWS_{gvp_rows}_NE_INDICES_{len(idxs)}"); typed_rows.append([u, f"GVP_ROWS_{gvp_rows}_NE_INDICES_{len(idxs)}|idx_src={idx_src}|gvp_src={gfp[1] if gfp else gvp_src}"]); continue
    maxidx = max(idxs)
    if maxidx > len(seq) or min(idxs) < 1:
        typed("INDICES_OUT_OF_RANGE"); typed_rows.append([u, f"INDICES_OUT_OF_RANGE|n={len(idxs)}|seqlen={len(seq)}|src={idx_src}"]); continue
    rec = {"uid": u, "seq_sha256": sha, "seqlen": len(seq), "node_source": node_src,
           "node_receipt": (nrec.get("node_value_sha256") if nrec and "node_value_sha256" in nrec else nrec.get("file_sha256", "") if nrec else ""),
           "indices_source": idx_src, "indices_n": len(idxs), "indices_sha256": sha_text(json.dumps(idxs)),
           "gvp_source": gfp[1] if gfp else gvp_src, "gvp_file": gfp[0] if gfp else "",
           "gvp_rows": gvp_rows,
           "structure_sha256": idx_entry.get("structure_sha", "") if idx_entry else "",
           "pocket_pdb_sha256": idx_entry.get("pocket_pdb_sha", "") if idx_entry else "",
           "weight_sha256": P.ESMC_WEIGHTS_SHA if node_src == "GENERATED_R3" else "P291_CACHE_ORIGINAL_WEIGHTS_PER_RECEIPT",
           "tier": st.get("priority_tier", "")}
    # ---- NEW600 slice (biological 1-based direct) ----
    pk_new = np.ascontiguousarray(node[list(idxs)], dtype=np.float32)
    assert pk_new.shape == (len(idxs), 1152) and np.isfinite(pk_new).all()
    new_pocket[u] = pk_new
    new_global[sha] = np.ascontiguousarray(node.mean(0), dtype=np.float32)
    rec["new600_pocket_value_sha256"] = arr_sha(pk_new)
    rec["new600_recipe"] = "RESCUE_BIO_1BASED_DIRECT_SLICE_S10CONTRACT"
    summary["new600_pocket"] += 1; summary["new600_global"] += 1
    gvp_merged[u] = tuple(x if isinstance(x, str) else torch.as_tensor(x).clone() for x in gvp_val) if gfp else None
    if gvp_merged[u] is not None: summary["gvp_merged"] += 1
    rec["gvp_value_sha256"] = hashlib.sha256(np.ascontiguousarray(np.asarray(gvp_val[0], dtype=np.float32)).tobytes()).hexdigest()
    # ---- LEGACY slice (real contract via legacy_indices; prefix recipe control-confirmed) ----
    if LEGACY_RESCUE_ALLOWED:
        pdb = idx_entry.get("pdb_path") if idx_entry else None
        leg_ok = False; leg_reason = "NO_POCKET_PDB_FOR_CONTRACT"
        if pdb:
            try:
                # derive pocket_info from the ordered indices (residue numbers == 1-based sequence positions)
                import tempfile
                with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tf:
                    tf.write("UniprotID,pocket_residues\n")
                    tf.write(f"{u},\"{','.join(str(x) for x in idxs)}\"\n")
                    pinfo = tf.name
                li, status = legacy_indices(pdb, pinfo, u)
                os.unlink(pinfo)
                if status == "OK" and li == list(range(len(idxs))):
                    pk_leg = np.ascontiguousarray(node[li], dtype=np.float32)
                    assert pk_leg.shape == (len(idxs), 1152) and np.isfinite(pk_leg).all()
                    leg_pocket[u] = pk_leg
                    leg_global[seq] = np.ascontiguousarray(node.mean(0), dtype=np.float32)
                    rec["legacy_pocket_value_sha256"] = arr_sha(pk_leg)
                    rec["legacy_recipe"] = "LEGACY_COMPACT_BOS_ONCE_PREFIX_SLICE_GENERATED_0713_WEIGHTS_CONTRACT_VERIFIED_VS_SEPT_UNION"
                    rec["legacy_pdb_path"] = pdb
                    summary["legacy_pocket"] += 1; summary["legacy_global"] += 1
                    leg_ok = True
                else:
                    leg_reason = f"LEGACY_CONTRACT_STATUS_{status}"
            except Exception as e:
                leg_reason = "LEGACY_CONTRACT_ERROR_" + type(e).__name__
        if not leg_ok:
            rec["legacy_typed"] = leg_reason
            typed(leg_reason); typed_rows.append([u, "LEGACY_" + leg_reason])
    else:
        rec["legacy_typed"] = "LEGACY_RESCUE_SUSPENDED_RECIPE_CONTROL"
        typed("LEGACY_RESCUE_SUSPENDED_RECIPE_CONTROL")
    rec["status"] = "SLICED_OK"
    rec_f.write(json.dumps(rec) + "\n"); rec_f.flush()
    summary["uids_processed"] += 1
    if summary["uids_processed"] % 200 == 0:
        log("sliced", summary["uids_processed"], "new_p", summary["new600_pocket"], "leg_p", summary["legacy_pocket"])
rec_f.close()
with open(OVL + "/TYPED_FAILURES_SLICE.tsv", "w") as f:
    f.write("uid\ttyped_reason\n")
    for u, r in typed_rows: f.write(f"{u}\t{r}\n")

# ---------- atomic overlay materialization ----------
def dump_atomic(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f: pickle.dump(obj, f, protocol=4)
    os.replace(tmp, path)
    return {"path": path, "entries": len(obj), "bytes": os.path.getsize(path),
            "file_sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()}

manifest = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "recipe_control": control, "summary": summary, "overlays": {}}
if new_pocket: manifest["overlays"]["new600_pocket_rescue"] = dump_atomic(new_pocket, f"{OVL}/new600_pocket_rescue.pkl")
if new_global: manifest["overlays"]["new600_global_rescue"] = dump_atomic(new_global, f"{OVL}/new600_global_rescue.pkl")
if leg_pocket: manifest["overlays"]["legacy_pocket_rescue"] = dump_atomic(leg_pocket, f"{OVL}/legacy_pocket_rescue.pkl")
if leg_global: manifest["overlays"]["legacy_global_rescue"] = dump_atomic(leg_global, f"{OVL}/legacy_global_rescue.pkl")
if gvp_merged: manifest["overlays"]["gvp_rescue"] = dump_atomic({k: v for k, v in gvp_merged.items() if v is not None}, f"{OVL}/gvp_rescue.pkl")
json.dump(manifest, open(f"{OVL}/OVERLAY_MANIFEST.json", "w"), indent=1)
log("SLICE DONE", json.dumps(summary["typed"], indent=1)[:800])
log("overlays:", {k: v["entries"] for k, v in manifest["overlays"].items()})
