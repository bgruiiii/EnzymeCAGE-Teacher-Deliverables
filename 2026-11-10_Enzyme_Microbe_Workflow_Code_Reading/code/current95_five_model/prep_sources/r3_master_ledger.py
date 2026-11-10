#!/usr/bin/env python3
"""R3 checkpoint-2 master ledger: per-context / per-candidate-row / per-model
asset accounting over the 3B-verified parent pool (382 steps / 16,472 rows /
7,480 entities), plus repair worklists.

Records SEPARATELY: key presence vs consumer conclusion (checkpoint-2 rule).
Sources wired (registered locations only): R3 MERGE_MANIFEST (3B), native July
stores (legacy), corrected/S10/S11 stores + gvp trio (new, R2 route rules),
p291 September union + seq_nodes raw-node cache (legacy generated route),
r3d/oldR3/S5 pocket_ok.json ordered indices + GVP overlay files + manifests,
A109 registry receipts, S10/S11 CARRIER indices.
Outputs under NEWROOT/runtime/ledger: LEDGER_PARENT_ROWS.tsv.gz,
UID_ASSET_STATE.tsv.gz, STEP_STATE_382.tsv, LEDGER_SUMMARY.json,
WORKLIST_{GPU_NODES,CPU_RESLICE,SEPT_UNION,GVP_PAIRING,BLOCKED}.tsv
(per-context row ledgers appended then merged — fixes the R2 single-list defect).
"""
import csv, glob, hashlib, json, os, pickle, sys, time
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_paths as P
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "scripts"))
import recovery_helpers as RH

t0 = time.time()
def log(*a): print(f"[{time.time()-t0:6.1f}s]", *a, flush=True)
OUT = P.NEWROOT + "/runtime/ledger"; os.makedirs(OUT, exist_ok=True)
sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()

# ---------------- package inputs ----------------
pool = {}   # ctx -> step list
for ctx in P.CTXS:
    pool[ctx] = json.load(open(f"{P.PKG}/inputs/{ctx}/THREE_B_VERIFIED_PARENT_POOL.json"))
uid2 = {}   # ctx -> uid -> (sha, seq)
for ctx in P.CTXS:
    uid2[ctx] = {}
    with open(f"{P.PKG}/inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            uid2[ctx][r["runtime_uid"]] = (r["sequence_sha256"], r["sequence"])
gold = {}
for ctx in P.CTXS:
    with open(f"{P.PKG}/inputs/{ctx}/EVAL_LABELS_PARENT.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["gold_flag"] == "TRUE":
                gold[(ctx, r["step_occurrence_id"], r["sequence_sha256"])] = r.get("gold_accessions", "")
rows_total = sum(len(s["pool_uids"]) for c in pool for s in pool[c])
log("parent pool steps:", {c: len(pool[c]) for c in pool}, "rows:", rows_total, "gold labels:", len(gold))

q123 = {}
with open(f"{P.PKG}/PRIORITY_COVER_CANDIDATES_123.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        q123[r["runtime_uid"]] = int(r["priority_order"])
opt184 = set()
with open(f"{P.PKG}/GOLD_OPTIONS_FOR_UNCOVERED_STEPS_184.tsv") as f:
    opt184 = {r["runtime_uid"] for r in csv.DictReader(f, delimiter="\t")}
g562 = {}
with open(f"{P.PKG}/GOLD_ENTITY_QUEUE_ALL_562.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        g562[r["runtime_uid"]] = r
log("queues: 123 =", len(q123), "184 =", len(opt184), "562 =", len(g562))

# ---------------- key sets ----------------
# 3B merged manifests
man3b = {}
for ctx in P.CTXS:
    g, p_, v = set(), set(), set()
    with open(f"{P.R3}/materialize_{ctx}/MERGE_MANIFEST.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if not r["status"].startswith("MERGED"): continue
            (g if r["family"] == "global" else p_ if r["family"] == "pocket" else v if r["family"] == "gvp" else g).add(r["key"])
    man3b[ctx] = {"global_sha": g, "pocket_uid": p_, "gvp_uid": v}
    log(f"3B manifest {ctx}: global {len(g)} pocket {len(p_)} gvp {len(v)}")

# legacy native
formal_global_shas = set()
with open(P.STORES["legacy_global_formal"], "rb") as f:
    for k in pickle.load(f).keys(): formal_global_shas.add(sha_text(k))
log("formal global seqs:", len(formal_global_shas))
sys.path.insert(0, P.REPO_OLD)
from enzymecage.dataset.sharded_protein import load_pocket_node_feature_data, load_protein_gvp_data
legacy_pocket_uids = set(load_pocket_node_feature_data(P.STORES["legacy_pocket_native"]).keys())
gvp_flat_uids = set(load_protein_gvp_data(P.STORES["gvp_flat"]).keys())
assert legacy_pocket_uids and gvp_flat_uids, "R1 key caches missing — reload required"
log("legacy pocket:", len(legacy_pocket_uids), "gvp flat:", len(gvp_flat_uids))

# new arm stores
corr_rows = {}
with open(P.CORR_JSONL) as f:
    for line in f:
        if line.strip():
            j = json.loads(line); corr_rows[j["UniprotID"]] = len(j["corrected_untrimmed_indices"])
s10g, s10p, s11g, s11p = set(), set(), set(), set()
for i in range(4):
    with open(f"{P.STORES['s10_out']}/esmc_global_shard{i}.pkl", "rb") as f: s10g.update(pickle.load(f).keys())
    with open(f"{P.STORES['s10_out']}/esmc_pocket_shard{i}.pkl", "rb") as f: s10p.update(pickle.load(f).keys())
    with open(f"{P.STORES['s11_gen2_out']}/esmc_global_shard{i}.pkl", "rb") as f: s11g.update(pickle.load(f).keys())
    with open(f"{P.STORES['s11_gen2_out']}/esmc_pocket_shard{i}.pkl", "rb") as f: s11p.update(pickle.load(f).keys())
import torch
gvp_s3 = set(torch.load(P.STORES["gvp_s3_new"], map_location="cpu", weights_only=False).keys())
gvp_r1 = set(torch.load(P.STORES["gvp_r1_overlay"], map_location="cpu", weights_only=False).keys())
log("corrected:", len(corr_rows), "s10:", len(s10g), len(s10p), "s11:", len(s11g), len(s11p), "s3:", len(gvp_s3), "r1:", len(gvp_r1))

# september union + raw node cache (legacy generated route)
sys.path.insert(0, P.REPO_OLD)
from enzymecage.dataset.sharded_protein import load_pocket_node_feature_data, load_protein_gvp_data
union_pocket = set(load_pocket_node_feature_data(P.P291_ASSETS + "/esm_node_feature_600m_union.pt").keys())
union_gvp = set(load_protein_gvp_data(P.P291_ASSETS + "/gvp_union.pt").keys())
with open(P.P291_ASSETS + "/seq2feature_600m_union.pkl", "rb") as f:
    union_global_shas = {sha_text(k) for k in pickle.load(f).keys()}
seq_nodes = {x[:-4] for x in os.listdir(P.P291 + "/assets/seq_nodes") if x.endswith(".npz")}
log("sept union p/g/gl:", len(union_pocket), len(union_gvp), len(union_global_shas), "seq_nodes:", len(seq_nodes))

# carrier indices (S10 route)
import pandas as pd
carrier_idx = {}
cdf = pd.read_parquet(P.CARRIER_PARQUET)
for r in cdf.itertuples(index=False):
    carrier_idx.setdefault(str(r.UniprotID), (str(r.sequence_sha256), str(r.pocket_indices_1based)))
log("carrier uids:", len(carrier_idx))

# rescue receipts: pocket_ok.json across three registered roots + manifests
indices_src = {}   # uid -> dict(indices, n, source, seq_sha, structure_sha, pocket_pdb_sha, root)
def scan_pocket_ok(root_dirs, tag):
    n = 0
    for d in root_dirs:
        for p in glob.glob(d + "/*/pocket_ok.json"):
            try:
                j = json.load(open(p))
                u = j.get("uid") or os.path.basename(os.path.dirname(p))
                idx = j.get("untrimmed_indices")
                if not u or not idx: continue
                if u in indices_src: continue  # first-registered wins; collisions recorded
                indices_src[u] = {"indices": [int(x) for x in idx], "n": len(idx), "source": tag,
                                  "seq_sha": j.get("sequence_sha256", j.get("seq_sha", "")),
                                  "structure_sha": j.get("structure_sha256", ""),
                                  "pocket_pdb_sha": j.get("pocket_pdb_sha256", ""),
                                  "path": p}
                n += 1
            except Exception:
                pass
    return n
n1 = scan_pocket_ok([P.R3 + "/struct_r3d/work/struct"], "R3D_P2RANK_20261101")
n2 = scan_pocket_ok([P.OLDR3 + "/struct_lane/work/struct"], "OLDR3_STRUCT_LANE_20261008")
n3 = scan_pocket_ok([P.S5 + "/struct_lane/work/struct"], "S5_STRUCT_LANE_20261006")
# --- R4 source recovery (task-copy adaptation SOURCE_RECOVERY_20261103) -------
# Lanes named by the original 3B MERGE_MANIFEST sources that the R3 scan set
# did not cover: task_r3_overlay_new (R3_task struct lane pocket_ok receipts),
# s5_overlay historical recheck (pocket_ok_hist.json), task_r3c_pair_repair
# (adjudicated evidence mapped_1based_indices). GVP values for the traced gold
# UIDs verified value_bytes_sha-equal to the merge manifest value_sha256.
n4 = scan_pocket_ok([P.WS + "/runtime/main/R3_task/R3_structure_protein/struct_lane/work/struct"], "R3_TASK_NEW_MAIN")
n5 = scan_pocket_ok([P.WS + "/runtime/delta15/R3_task/R3_structure_protein/struct_lane/work/struct"], "R3_TASK_NEW_DELTA15")
n6 = 0
for _p in glob.glob(P.S5 + "/struct_lane/work/struct/*/pocket_ok_hist.json"):
    try:
        _j = json.load(open(_p))
        _u = _j.get("uid") or os.path.basename(os.path.dirname(_p))
        _idx = _j.get("untrimmed_indices")
        if not _u or not _idx or _u in indices_src: continue
        indices_src[_u] = {"indices": [int(x) for x in _idx], "n": len(_idx), "source": "S5_HIST_RECHECK",
                           "seq_sha": _j.get("sequence_sha256", _j.get("seq_sha", "")),
                           "structure_sha": _j.get("structure_sha256", ""),
                           "pocket_pdb_sha": _j.get("pocket_pdb_sha256", ""),
                           "path": _p}
        n6 += 1
    except Exception:
        pass
n7 = 0
_r3c_wl = P.R3 + "/pair_adjudications/PAIR_REPAIR_WORKLIST.tsv"
if os.path.isfile(_r3c_wl):
    with open(_r3c_wl) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            _u = r.get("uid", "")
            if not _u or _u in indices_src: continue
            if not str(r.get("verdict", "")).startswith("PASS"): continue
            _evp = r.get("evidence_file", "")
            if not _evp or not os.path.isfile(_evp): continue
            try:
                _ev = json.load(open(_evp))
                _idx = [int(x) for x in _ev["mapped_1based_indices"]]
                if hashlib.sha256(json.dumps(_idx).encode()).hexdigest() != _ev.get("indices_sha256"): continue
                indices_src[_u] = {"indices": _idx, "n": len(_idx), "source": "R3C_PAIR_ADJUDICATED",
                                   "seq_sha": r.get("sequence_sha256", ""),
                                   "structure_sha": _ev.get("pdb_sha256", ""),
                                   "pocket_pdb_sha": _ev.get("pdb_sha256", ""),
                                   "path": _evp}
                n7 += 1
            except Exception:
                pass
# historical-recheck receipts (pocket_ok_hist.json) in OLDR3 / R3_task lanes
# (S5 hist handled above). Q8KN40-class gold: OLDR3 hist PDB sha256 equals the
# pdb recorded in the S5 GVP manifest — same-structure entity proof.
n8 = 0
for _root, _tag in ((P.OLDR3 + "/struct_lane/work/struct", "OLDR3_HIST_RECHECK"),
                    (P.WS + "/runtime/main/R3_task/R3_structure_protein/struct_lane/work/struct", "R3_TASK_NEW_HIST_MAIN"),
                    (P.WS + "/runtime/delta15/R3_task/R3_structure_protein/struct_lane/work/struct", "R3_TASK_NEW_HIST_DELTA15")):
    for _p in glob.glob(_root + "/*/pocket_ok_hist.json"):
        try:
            _j = json.load(open(_p))
            _u = _j.get("uid") or os.path.basename(os.path.dirname(_p))
            _idx = _j.get("untrimmed_indices")
            if not _u or not _idx or _u in indices_src: continue
            indices_src[_u] = {"indices": [int(x) for x in _idx], "n": len(_idx), "source": _tag,
                               "seq_sha": _j.get("sequence_sha256", _j.get("seq_sha", "")),
                               "structure_sha": _j.get("structure_sha256", ""),
                               "pocket_pdb_sha": _j.get("pocket_pdb_sha256", ""),
                               "path": _p}
            n8 += 1
        except Exception:
            pass
log("pocket_ok receipts: r3d", n1, "oldr3", n2, "s5", n3, "r3_task", n4 + n5,
    "s5_hist", n6, "r3c", n7, "hist_oldr3_r3task", n8, "total", len(indices_src))

# gvp overlay files per uid (filename {sha32}_{uid}.gvp.pt)
gvp_files = {}   # uid -> (path, source_tag)
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
# manifests with rows
gvp_rows_receipt = {}
try:
    dm = json.load(open(P.OLDR3 + "/GVP_DELTA_MANIFEST.json"))
    for k, v in dm.items():
        if v.get("status") == "SUCCESS":
            u = k.split("|", 1)[1]
            gvp_rows_receipt[u] = {"rows": int(v["rows"]), "file": v.get("file", ""), "pdb_sha256": v.get("pdb_sha256", ""), "feat_sha256": v.get("feat_sha256", ""), "manifest": "OLDR3_GVP_DELTA"}
except Exception as e: log("oldr3 manifest err", e)
try:
    sm = json.load(open(P.S5 + "/gvp_manifests/GVP_MANIFEST_full.json"))
    for k, v in sm.items():
        if v.get("status") == "SUCCESS" and "|" in k:
            u = k.split("|", 1)[1]
            gvp_rows_receipt.setdefault(u, {"rows": int(v.get("rows", -1)), "file": v.get("file", ""), "manifest": "S5_GVP_FULL"})
except Exception as e: log("s5 manifest err", e)
# R4 source recovery: R3_task lane GVP delta manifests (rows + pdb receipts)
for _ctx in P.CTXS:
    try:
        tm = json.load(open(P.WS + f"/runtime/{_ctx}/R3_task/R3_structure_protein/GVP_DELTA_MANIFEST.json"))
        for k, v in tm.items():
            if v.get("status") == "SUCCESS" and "|" in k:
                u = k.split("|", 1)[1]
                gvp_rows_receipt.setdefault(u, {"rows": int(v["rows"]), "file": v.get("file", ""),
                                                "pdb_sha256": v.get("pdb_sha256", ""), "feat_sha256": v.get("feat_sha256", ""),
                                                "manifest": "R3_TASK_NEW_GVP_DELTA_" + _ctx.upper()})
    except Exception as e: log("r3_task manifest err", _ctx, e)
a109reg = json.load(open(P.A109 + "/REGISTRY.json")).get("entities", {})
log("gvp rows receipts:", len(gvp_rows_receipt), "a109 registry:", len(a109reg))
# r3d pair manifest rows
r3d_pair = {}
with open(P.R3 + "/overlays/pocket_r3d/PAIR_MANIFEST_R3D.jsonl") as f:
    for line in f:
        j = json.loads(line)
        r3d_pair[j["uid"]] = j
log("r3d pair manifest:", len(r3d_pair))

# ---------------- per-UID state ----------------
# universe of uids in parent pools
uni = {}
for ctx in P.CTXS:
    for s in pool[ctx]:
        for u, sh in zip(s["pool_uids"], s["pool_shas"]):
            e = uid2[ctx].get(u)
            if e and e[0] == sh:
                uni.setdefault(u, (ctx, sh, e[1]))
log("universe uids:", len(uni))

# Verified source capsule takes precedence for the SAME accepted 109 pockets.
for _uid, _b in RH.recovery_bundles(P.PKG).items():
    indices_src[_uid] = {"indices": _b["indices"], "n": _b["rows"], "source": "A109_VERIFIED_RECOVERY",
                         "seq_sha": _b["seq_sha256"], "structure_sha": _b["structure_sha256"],
                         "pocket_pdb_sha": _b["pdb_sha256"]}
    gvp_files[_uid] = (_b["gvp"], "A109_VERIFIED_RECOVERY")
    gvp_rows_receipt[_uid] = {"rows": _b["rows"]}
RH_RECOVERY_UIDS = set(RH.recovery_bundles(P.PKG))
_real_gvp_cache = {}
def _real_store_rows(uid, tag):
    return RH.actual_gvp(uid, tag, P, torch, load_protein_gvp_data, _real_gvp_cache)[1]
def gvp_located(u):
    """returns (source_tag, rows_or_None, file_or_None)

    R4 precedence fix (SOURCE_RECOVERY_20261103): a registered structural-lane
    GVP bundle file wins over the generic stores, because the same lane's
    ordered-indices receipt pairs with the lane's GVP (same-receipt bundle rule
    of the RESCUE_* named routes) and r3_slice_values.load_gvp has always
    consumed the bundle file first — ledger classification must match the real
    consumption route. Store lookup (real-value rows) is the fallback when no
    bundle file is registered for the UID."""
    if u in gvp_files:
        value = torch.load(gvp_files[u][0], map_location="cpu", weights_only=False)
        value = value[u] if isinstance(value, dict) and u in value else value
        rows = int(value[0].shape[0])
        if rows is None and u in r3d_pair: rows = int(r3d_pair[u].get("gvp_rows", -1)) or None
        if rows is None and u in a109reg: rows = a109reg[u].get("rows")
        return (gvp_files[u][1], rows, gvp_files[u][0])
    if u in gvp_flat_uids and u not in RH_RECOVERY_UIDS: return ("FLAT_JULY", _real_store_rows(u, "FLAT_JULY"), None)
    if u in gvp_s3 and u not in RH_RECOVERY_UIDS: return ("S3_SEPT", _real_store_rows(u, "S3_SEPT"), None)
    if u in gvp_r1 and u not in RH_RECOVERY_UIDS: return ("R1_SEPT", _real_store_rows(u, "R1_SEPT"), None)
    if u in a109reg:
        return ("A109_REGISTRY", a109reg[u].get("rows"), None)
    return (None, None, None)

uid_state = {}
for u, (ctx, sh, seq) in uni.items():
    st = {"uid": u, "ctx_first": ctx, "seq_sha": sh, "seqlen": len(seq)}
    # --- 3B key presence (manifest, per row's own ctx; uid may span ctxs) ---
    def tb_present(c):
        return sh in man3b[c]["global_sha"] and u in man3b[c]["pocket_uid"] and u in man3b[c]["gvp_uid"]
    st["three_b_key_by_ctx"] = {c: tb_present(c) for c in P.CTXS}
    st["three_b_key"] = "PRESENT" if st["three_b_key_by_ctx"][ctx] else ("PRESENT_OTHER_CTX" if any(st["three_b_key_by_ctx"].values()) else "MISSING")
    st["three_b_consumer"] = "VERIFIED_BY_A109_PARENT_POOL" if st["three_b_key"] == "PRESENT" else "KEY_MISSING_IN_ROW_CTX"
    # --- legacy ---
    leg_g = sh in formal_global_shas
    leg_p = u in legacy_pocket_uids
    leg_v = u in gvp_flat_uids
    st["legacy_key"] = "NATIVE_READY" if (leg_g and leg_p and leg_v) else "NATIVE_MISSING"
    st["legacy_missing_parts"] = "|".join(x for x, ok in (("global", leg_g), ("pocket", leg_p), ("gvp_flat", leg_v)) if not ok)
    # rescue ladder for legacy
    in_union = (u in union_pocket and u in union_gvp) or (sh in union_global_shas and u in union_pocket)
    st["legacy_sept_union"] = bool(u in union_pocket and u in union_gvp)
    st["legacy_node_cache"] = sh in seq_nodes
    # --- new ---
    new_g = sh in formal_global_shas or sh in s10g or sh in s11g
    new_p = u in corr_rows or u in s10p or u in s11p
    new_v = leg_v or (u in gvp_s3) or (u in gvp_r1)
    st["new_key"] = "STORE_READY" if (new_g and new_p and new_v) else "STORE_MISSING"
    st["new_missing_parts"] = "|".join(x for x, ok in (("global", new_g), ("pocket", new_p), ("gvp", new_v)) if not ok)
    # --- rescue classification (shared node economy) ---
    gsrc, grows, gfile = gvp_located(u)
    st["gvp_rescue_source"] = gsrc or ""
    st["gvp_rescue_rows"] = grows if grows is not None else ""
    st["gvp_rescue_file"] = gfile or ""
    isr = indices_src.get(u)
    st["indices_source"] = isr["source"] if isr else ("" if u not in carrier_idx else "CARRIER_S10")
    if isr:
        st["indices_n"] = isr["n"]
        st["indices_sha"] = sha_text(json.dumps(isr["indices"]))
        st["structure_sha"] = isr["structure_sha"]
        st["pocket_pdb_sha"] = isr["pocket_pdb_sha"]
    elif u in carrier_idx:
        idxs = [int(x) for x in carrier_idx[u][1].split(",") if x != ""]
        st["indices_n"] = len(idxs)
        st["indices_sha"] = sha_text(json.dumps(idxs))
        st["structure_sha"] = ""; st["pocket_pdb_sha"] = ""
    else:
        st["indices_n"] = ""; st["indices_sha"] = ""; st["structure_sha"] = ""; st["pocket_pdb_sha"] = ""
    rows_match = (grows is not None and st["indices_n"] != "" and int(grows) == int(st["indices_n"]))
    st["gvp_indices_rows_match"] = str(rows_match) if (gsrc and st["indices_n"] != "") else ""
    # repair actions
    acts = []
    if st["new_key"] != "STORE_READY":
        if gsrc and st["indices_n"] != "" and rows_match:
            acts.append("NEW_RESCUE_SLICE_" + ("NODE_CACHED" if st["legacy_node_cache"] else "NODE_GPU"))
        elif gsrc and st["indices_n"] == "":
            acts.append("NEW_BLOCKED_NO_INDICES")
        elif not gsrc:
            acts.append("NEW_BLOCKED_NO_GVP_STRUCTURAL")
        else:
            acts.append("NEW_BLOCKED_ROWS_MISMATCH_gvp%s_idx%s" % (grows, st["indices_n"]))
    if st["legacy_key"] != "NATIVE_READY":
        if st["legacy_sept_union"]:
            acts.append("LEGACY_SEPT_UNION_REUSE")
        elif gsrc and st["indices_n"] != "" and rows_match:
            acts.append("LEGACY_RESCUE_GENERATION_" + ("NODE_CACHED" if st["legacy_node_cache"] else "NODE_GPU") + "_CONTRACT_CHECK_PENDING")
        elif not gsrc:
            acts.append("LEGACY_BLOCKED_NO_GVP_STRUCTURAL")
        else:
            acts.append("LEGACY_BLOCKED_NO_INDICES_OR_ROWS")
    st["repair_actions"] = ";".join(acts) if acts else "NONE_NEEDED"
    st["priority_tier"] = ("T1_123QUEUE_%d" % q123[u]) if u in q123 else ("T2_184OPTIONS" if u in opt184 else ("T3_GOLD562" if u in g562 else "T4_BACKGROUND"))
    uid_state[u] = st
log("uid states built:", len(uid_state))

# ---------------- per-row ledger (per-ctx files then merged — R2 defect fix) ----------------
row_files = []
for ctx in P.CTXS:
    p = f"{OUT}/LEDGER_ROWS_{ctx}.tsv.gz"
    import gzip as gz
    with gz.open(p, "wt") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["ctx", "step_id", "pool_position", "runtime_uid", "sequence_sha256", "gold_flag",
                    "three_b_key_present", "three_b_consumer", "legacy_key_state", "legacy_missing_parts",
                    "new_key_state", "new_missing_parts", "repair_actions", "priority_tier",
                    "gvp_rescue_source", "gvp_rescue_rows", "indices_source", "indices_n", "gvp_indices_rows_match"])
        for s in pool[ctx]:
            for pos, (u, sh) in enumerate(zip(s["pool_uids"], s["pool_shas"])):
                st = uid_state.get(u)
                gflag = (ctx, s["step_id"], sh) in gold
                if st is None:
                    w.writerow([ctx, s["step_id"], pos, u, sh, gflag, "UID_NOT_IN_RUNTIME_MAP", "", "", "", "", "", "BLOCKED_NO_SEQUENCE", "", "", "", "", "", ""])
                    continue
                w.writerow([ctx, s["step_id"], pos, u, sh, gflag,
                            st["three_b_key"], st["three_b_consumer"], st["legacy_key"], st["legacy_missing_parts"],
                            st["new_key"], st["new_missing_parts"], st["repair_actions"], st["priority_tier"],
                            st["gvp_rescue_source"], st["gvp_rescue_rows"], st["indices_source"], st["indices_n"],
                            st["gvp_indices_rows_match"]])
    row_files.append(p)
    log("row ledger", ctx, "written")

# ---------------- per-step state ----------------
step_rows = []
for ctx in P.CTXS:
    for s in pool[ctx]:
        n3 = nleg = nnew = ncommon_now = 0
        ncommon_pot = 0
        gnow = gpot = 0
        for u, sh in zip(s["pool_uids"], s["pool_shas"]):
            st = uid_state.get(u)
            if not st: continue
            t3 = st["three_b_key_by_ctx"].get(ctx, False)
            leg = st["legacy_key"] == "NATIVE_READY" or "LEGACY_SEPT_UNION_REUSE" in st["repair_actions"] or "LEGACY_RESCUE_GENERATION" in st["repair_actions"]
            new = st["new_key"] == "STORE_READY" or "NEW_RESCUE_SLICE" in st["repair_actions"]
            n3 += t3
            leg_now = st["legacy_key"] == "NATIVE_READY"
            new_now = st["new_key"] == "STORE_READY"
            nleg += leg_now; nnew += new_now
            g = (ctx, s["step_id"], sh) in gold
            if t3 and leg_now and new_now:
                ncommon_now += 1; gnow += g
            if t3 and leg and new:
                ncommon_pot += 1; gpot += g
        step_rows.append([ctx, s["step_id"], len(s["pool_uids"]), s.get("frozen_n_golds", ""),
                          n3, nleg, nnew, ncommon_now, gnow, ncommon_pot, gpot,
                          "ADMITTED_NOW" if gnow >= 1 else ("ADMITTED_POTENTIAL" if gpot >= 1 else "NO_COMMON_GOLD")])
with open(f"{OUT}/STEP_STATE_382.tsv", "w") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["ctx", "step_id", "parent_n", "frozen_n_golds", "three_b_present", "legacy_ready_now", "new_ready_now",
                "common_rows_now", "common_gold_now", "common_rows_potential", "common_gold_potential", "admission_state"])
    w.writerows(step_rows)
adm_now = sum(1 for r in step_rows if r[11] == "ADMITTED_NOW")
adm_pot = sum(1 for r in step_rows if r[11] in ("ADMITTED_NOW", "ADMITTED_POTENTIAL"))
log("steps admitted now:", adm_now, "potential after repair:", adm_pot, "of", len(step_rows))

# ---------------- worklists ----------------
# W1 GPU nodes: unique sequences needing generation
need_node = {}
for u, st in uid_state.items():
    if "NODE_GPU" in st["repair_actions"] and not st["legacy_node_cache"]:
        need_node.setdefault(st["seq_sha"], {"uids": [], "tier": 999, "seq": None})
        need_node[st["seq_sha"]]["uids"].append(u)
        need_node[st["seq_sha"]]["tier"] = min(need_node[st["seq_sha"]]["tier"],
                                                int(st["priority_tier"].split("_")[0][1:]) if st["priority_tier"][0] == "T" else 9)
for ctx in P.CTXS:
    for u, (sh, sq) in uid2[ctx].items():
        if sh in need_node and need_node[sh]["seq"] is None:
            need_node[sh]["seq"] = sq
with open(f"{OUT}/WORKLIST_GPU_NODES.tsv", "w") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["tier", "sequence_sha256", "n_uids", "uids", "seqlen"])
    for sh, d in sorted(need_node.items(), key=lambda kv: (kv[1]["tier"], kv[0])):
        w.writerow([d["tier"], sh, len(d["uids"]), ";".join(sorted(d["uids"])), len(d["seq"] or "")])
log("W1 gpu node sequences:", len(need_node), "tiers:", {t: sum(1 for d in need_node.values() if d['tier']==t) for t in sorted({d['tier'] for d in need_node.values()})})

# W2 CPU reslice candidates
with open(f"{OUT}/WORKLIST_CPU_RESLICE.tsv", "w") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["sequence_sha256", "uids", "cache_path", "tier"])
    n2_ = 0
    for u, st in uid_state.items():
        if st["legacy_node_cache"] and ("NODE_CACHED" in st["repair_actions"]):
            w.writerow([st["seq_sha"], u, f"{P.P291}/assets/seq_nodes/{st['seq_sha']}.npz", st["priority_tier"]]); n2_ += 1
log("W2 cpu reslice rows:", n2_)

# W3 sept union reuse (legacy)
with open(f"{OUT}/WORKLIST_SEPT_UNION.tsv", "w") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["runtime_uid", "seq_sha", "union_pocket", "union_gvp", "union_global", "tier"])
    n3_ = 0
    for u, st in uid_state.items():
        if "LEGACY_SEPT_UNION_REUSE" in st["repair_actions"]:
            w.writerow([u, st["seq_sha"], u in union_pocket, u in union_gvp, st["seq_sha"] in union_global_shas, st["priority_tier"]]); n3_ += 1
log("W3 sept union rows:", n3_)

# W4 gvp pairing plan
with open(f"{OUT}/WORKLIST_GVP_PAIRING.tsv", "w") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["runtime_uid", "gvp_source", "gvp_file", "gvp_rows_receipt", "indices_source", "indices_n", "indices_sha256", "rows_match", "structure_sha256", "pocket_pdb_sha256", "tier"])
    n4 = 0
    for u, st in uid_state.items():
        if st["gvp_rescue_source"] and st["gvp_rescue_source"] not in ("FLAT_JULY", "S3_SEPT", "R1_SEPT"):
            w.writerow([u, st["gvp_rescue_source"], st["gvp_rescue_file"], st["gvp_rescue_rows"], st["indices_source"],
                        st["indices_n"], st["indices_sha"], st["gvp_indices_rows_match"], st["structure_sha"], st["pocket_pdb_sha"], st["priority_tier"]]); n4 += 1
log("W4 gvp pairing rows:", n4)

# W5 blocked typed
with open(f"{OUT}/WORKLIST_BLOCKED.tsv", "w") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["runtime_uid", "seq_sha", "blocked_reason", "tier"])
    n5 = 0
    for u, st in uid_state.items():
        bl = [a for a in st["repair_actions"].split(";") if "BLOCKED" in a]
        if bl:
            w.writerow([u, st["seq_sha"], ";".join(bl), st["priority_tier"]]); n5 += 1
log("W5 blocked rows:", n5)

# uid state dump
import gzip as _gz2
with _gz2.open(f"{OUT}/UID_ASSET_STATE.tsv.gz", "wt") as f:
    w = csv.DictWriter(f, fieldnames=list(next(iter(uid_state.values())).keys()), delimiter="\t")
    w.writeheader()
    for u in sorted(uid_state): w.writerow(uid_state[u])

# ---------------- summary ----------------
from collections import Counter
sumry = {
    "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "parent_pool": {"steps": sum(len(pool[c]) for c in pool), "rows": rows_total, "uids": len(uni), "gold_links": len(gold)},
    "steps_admitted_common_now": adm_now, "steps_admitted_common_potential": adm_pot,
    "uid_states": {
        "three_b_key_present_first_ctx": sum(1 for s in uid_state.values() if s["three_b_key"] == "PRESENT"),
        "legacy_native_ready": sum(1 for s in uid_state.values() if s["legacy_key"] == "NATIVE_READY"),
        "legacy_sept_union_rescue": sum(1 for s in uid_state.values() if "LEGACY_SEPT_UNION_REUSE" in s["repair_actions"]),
        "legacy_rescue_generation": sum(1 for s in uid_state.values() if "LEGACY_RESCUE_GENERATION" in s["repair_actions"]),
        "legacy_blocked": sum(1 for s in uid_state.values() if "LEGACY_BLOCKED" in s["repair_actions"]),
        "new_store_ready": sum(1 for s in uid_state.values() if s["new_key"] == "STORE_READY"),
        "new_rescue_slice": sum(1 for s in uid_state.values() if "NEW_RESCUE_SLICE" in s["repair_actions"]),
        "new_blocked": sum(1 for s in uid_state.values() if "NEW_BLOCKED" in s["repair_actions"]),
    },
    "worklists": {"gpu_node_sequences": len(need_node), "cpu_reslice_rows": n2_, "sept_union_rows": n3_,
                  "gvp_pairing_rows": n4, "blocked_rows": n5},
    "gpu_node_tiers": {str(t): sum(1 for d in need_node.values() if d["tier"] == t) for t in sorted({d["tier"] for d in need_node.values()})},
    "elapsed_sec": round(time.time() - t0, 1),
}
json.dump(sumry, open(f"{OUT}/LEDGER_SUMMARY.json", "w"), indent=1)
log("SUMMARY", json.dumps(sumry["uid_states"], indent=1))
log("LEDGER DONE")
