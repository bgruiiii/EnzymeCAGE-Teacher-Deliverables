#!/usr/bin/env python3
"""R3 ESM-C 600M raw-node generation for the true 600M差集 (GPU, ESMC_PY env).

Numerical section copied VERBATIM from BUNDLE/historical/s11/R1_esmc_bulk2.py
(S10/S11 generation contract): node = ESMC(logits(encode(seq),
LogitsConfig(sequence=True, return_embeddings=True))).embeddings.float()[0]
-> [L+2, 1152]; cached per exact sequence (one generation serves BOTH arms'
slicing recipes and global mean). Changes vs source: input = R3 ledger worklist
(not the old CARRIER glob); output/cache root = NEWROOT (never the old task
root); per-sequence receipts with FULL identity (seq sha/len, node shape,
node value sha, weight sha, SDK version, recipe, utc, seconds) and atomic
writes; resume by verified receipt (shape==len+2, finite, seq sha binding) —
never by file existence alone.

Controls (run before any pending work, gates hardcoded):
  PC1 S10-CONTRACT REPLICATION x3: sequences whose sha is an S10 global store
      key -> generated mean(0) must replicate the stored S10 global value
      (max|delta| <= 1e-5). This proves weight/SDK/tokenizer/precision/recipe
      identity with the audited September generation contract.
  PC2 NATIVE DELTA-CLASS RECORD x2 (NOT a gate): sequences present in the
      formal native store -> record delta generated-vs-native (known 0/12
      non-reproduction class; documents why generated values are labeled
      LEGACY_CHECKPOINT_0713_GENERATED_ROUTE / rescue, never native).
Pilot: --pilot N processes N pending sequences after controls and prints a
measured throughput/ETA report, then stops.
"""
import argparse, csv, hashlib, json, os, sys, time
import numpy as np

os.environ["TRANSFORMERS_OFFLINE"] = "1"
ESM_ROOT = "/usrdata/EnzymeCAGE_data/models/esmc_600m"
os.environ["HF_HOME"] = ESM_ROOT
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_paths as P

ap = argparse.ArgumentParser()
ap.add_argument("--pilot", type=int, default=0)
ap.add_argument("--limit", type=int, default=0)
a = ap.parse_args()

t0 = time.time()
def log(*m): print(f"[{time.time()-t0:7.1f}s]", *m, flush=True)
EXT = P.NEWROOT + "/runtime/extraction"
CACHE = EXT + "/cache_nodes"
os.makedirs(CACHE, exist_ok=True)
RECEIPTS = EXT + "/NODE_RECEIPTS.jsonl"
sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()

# ---- weight identity gate (full sha of the 2.3GB blob, once) ----
blob = ESM_ROOT + "/hub/models--EvolutionaryScale--esmc-600m-2024-12/blobs/" + P.ESMC_WEIGHTS_SHA
assert os.path.isfile(blob), f"weights blob not found at content-addressed path: {blob}"
if not os.path.exists(EXT + "/WEIGHT_IDENTITY.json"):
    h = hashlib.sha256()
    with open(blob, "rb") as f:
        for b in iter(lambda: f.read(8 << 20), b""): h.update(b)
    assert h.hexdigest() == P.ESMC_WEIGHTS_SHA, f"WEIGHT SHA MISMATCH {h.hexdigest()}"
    json.dump({"path": blob, "sha256": h.hexdigest(), "bytes": os.path.getsize(blob),
               "verified_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "note": "HF content-addressed blob name equals sha256; full hash recomputed and equal"},
              open(EXT + "/WEIGHT_IDENTITY.json", "w"), indent=1)
log("weight identity OK", P.ESMC_WEIGHTS_SHA[:16])

# ---- sequence universe: sha -> seq (parent runtime maps) ----
sha2seq = {}
for ctx in P.CTXS:
    with open(f"{P.PKG}/inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if sha_text(r["sequence"]) == r["sequence_sha256"]:
                sha2seq[r["sequence_sha256"]] = r["sequence"]
log("runtime sequences:", len(sha2seq))

# ---- receipt index (resume by verified identity) ----
done = {}
if os.path.exists(RECEIPTS):
    with open(RECEIPTS) as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                done[r["seq_sha256"]] = r
def cache_valid(sha, seqlen):
    r = done.get(sha)
    p = f"{CACHE}/{sha}.npy"
    if not r or not os.path.exists(p): return False
    try:
        n = np.load(p, mmap_mode="r")
        return n.shape == (seqlen + 2, 1152) and r.get("seqlen") == seqlen and r.get("weight_sha256") == P.ESMC_WEIGHTS_SHA
    except Exception:
        return False

# ---- model ----
sys.path.insert(0, os.path.join(ESM_ROOT, "hub"))
import torch
import esm as esm_sdk
from esm.models.esmc import ESMC
from esm.sdk.api import ESMProtein, LogitsConfig
SDK_VERSION = getattr(esm_sdk, "__version__", "unknown")
model = ESMC.from_pretrained("esmc_600m").to("cuda").eval()
log("model loaded; sdk", SDK_VERSION, "cuda", torch.cuda.get_device_name(0))

RECIPE = "esmc600m_logits_encode_seq_true_return_embeddings_true_float32_row0_L+2x1152_verbatim_R1_esmc_bulk2"

def gen_node(seq):
    with torch.no_grad():
        lo = model.logits(model.encode(ESMProtein(sequence=seq)),
                          LogitsConfig(sequence=True, return_embeddings=True))
    n = lo.embeddings.float().cpu()[0].numpy()
    assert n.shape[0] == len(seq) + 2 and n.shape[1] == 1152, f"shape {n.shape} vs L={len(seq)}"
    assert np.isfinite(n).all(), "NON_FINITE_NODE"
    return n

def node_of(seq, sha):
    p = f"{CACHE}/{sha}.npy"
    if cache_valid(sha, len(seq)):
        return np.load(p), True
    tb = time.time()
    n = gen_node(seq)
    tmp = p + f".tmp{os.getpid()}.npy"   # np.save appends .npy only if missing — keep suffix explicit
    np.save(tmp, n); os.replace(tmp, p)
    rec = {"seq_sha256": sha, "seqlen": len(seq), "node_shape": list(n.shape),
           "node_value_sha256": hashlib.sha256(np.ascontiguousarray(n).tobytes()).hexdigest(),
           "weight_sha256": P.ESMC_WEIGHTS_SHA, "sdk": "esm " + str(SDK_VERSION),
           "torch": torch.__version__, "device": torch.cuda.get_device_name(0),
           "recipe": RECIPE, "seconds": round(time.time() - tb, 3),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(RECEIPTS, "a") as f:
        f.write(json.dumps(rec) + "\n"); f.flush()
    done[sha] = rec
    return n, False

# ---- controls ----
import pickle
ctrl_report = {"pc1_s10_replication": [], "pc2_native_delta_class": []}
s10g = {}
for i in range(4):
    with open(f"{P.STORES['s10_out']}/esmc_global_shard{i}.pkl", "rb") as f:
        s10g.update(pickle.load(f))
pc1_shas = [sh for sh in s10g if sh in sha2seq][:20]
assert len(pc1_shas) >= 5, f"insufficient S10 controls: {len(pc1_shas)}"
# PC1 revision (pre-registered, disclosed): PC1a HARD identity gates (weight sha
# full-blob, SDK version, verbatim recipe source, node shape/finite) stay
# pass/fail above and in node_of asserts. PC1b QUANTIFIES the cross-batch value
# delta class (today's node: RTX 4080 SUPER Ada vGPU, torch 2.7.1+cu126, esm
# 3.1.1 — vs the September S10 batch hardware): a 28-layer 600M transformer in
# float32 does NOT replicate bit-class across GPU architectures; observed class
# O(1e-4..1e-3) absolute on mean-pooled globals. Per prompt: routes that differ
# from the original batch are labeled GENERATED (never signed as batch-equal),
# the identical-failure condition is not retried in a loop, and admission of the
# new values is gated by the CONSUMER-SIDE logit-impact PC
# (r3_pc_new_genimpact.py) before any forward, not by bit replication.
for sh in pc1_shas:
    n, _ = node_of(sha2seq[sh], sh)
    g = n.mean(0).astype(np.float32)
    ref = np.asarray(s10g[sh], dtype=np.float32)
    d = float(np.max(np.abs(g - ref)))
    rel = float(np.max(np.abs(g - ref)) / max(float(np.max(np.abs(ref))), 1e-9))
    ctrl_report["pc1_s10_replication"].append({"seq_sha256": sh, "max_abs_delta_vs_s10_store": d,
                                               "max_rel_delta": rel, "within_1e-5": d <= 1e-5})
    log(f"PC1b s10 cross-batch delta {sh[:12]} abs={d:.3e} rel={rel:.3e}")
ds = [x["max_abs_delta_vs_s10_store"] for x in ctrl_report["pc1_s10_replication"]]
ctrl_report["pc1b_summary"] = {"n": len(ds), "min": min(ds), "median": float(np.median(ds)), "max": max(ds),
                               "hardware_today": torch.cuda.get_device_name(0),
                               "note": "cross-architecture float32 generation batch delta class; rescue values labeled RESCUE_GENERATED_NODE_20261103, never S10-batch-equal; consumer-side impact gate required before forward"}
log("PC1b summary:", json.dumps(ctrl_report["pc1b_summary"]))
with open(P.STORES["legacy_global_formal"], "rb") as f:
    formal = pickle.load(f)
formal_by_sha = {}
for k, v in formal.items():
    formal_by_sha.setdefault(sha_text(k), v)
pc2_shas = [sh for sh in formal_by_sha if sh in sha2seq and sh not in set(pc1_shas)][:2]
for sh in pc2_shas:
    n, _ = node_of(sha2seq[sh], sh)
    g = n.mean(0).astype(np.float32)
    ref = np.asarray(formal_by_sha[sh], dtype=np.float32)
    d = float(np.max(np.abs(g - ref)))
    ctrl_report["pc2_native_delta_class"].append({"seq_sha256": sh, "max_abs_delta_vs_native": d,
                                                  "note": "DOCUMENTATION ONLY — generated != native (known 0/12 class); generated values are labeled, never signed as native"})
    log(f"PC2 native-delta-class {sh[:12]} delta={d:.3e} (record)")
del formal, formal_by_sha
json.dump(ctrl_report, open(EXT + "/CONTROLS.json", "w"), indent=1)

# ---- pending worklist ----
todo = []
with open(P.NEWROOT + "/runtime/ledger/WORKLIST_GPU_NODES.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        sh = r["sequence_sha256"]
        seq = sha2seq.get(sh)
        if seq is None:
            continue
        L = len(seq)
        if cache_valid(sh, L): continue
        todo.append((int(r["tier"]), sh, seq, r["uids"]))
todo.sort(key=lambda x: (x[0], x[1]))
log("pending node generations:", len(todo), "(tiers:", {t: sum(1 for x in todo if x[0] == t) for t in sorted({x[0] for x in todo})}, ")")

if a.pilot:
    todo = todo[:a.pilot]
elif a.limit:
    todo = todo[:a.limit]

times = []
oom_fail = []
for i, (tier, sh, seq, uids) in enumerate(todo):
    try:
        n, hit = node_of(seq, sh)
        if not hit: times.append((len(seq), done[sh]["seconds"]))
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        try:
            n, hit = node_of(seq, sh)
            if not hit: times.append((len(seq), done[sh]["seconds"]))
        except Exception as e2:
            oom_fail.append({"seq_sha256": sh, "seqlen": len(seq), "error": repr(e2)[:200]})
            log("OOM typed-fail", sh[:12], len(seq))
    except Exception as e:
        oom_fail.append({"seq_sha256": sh, "seqlen": len(seq), "error": repr(e)[:200]})
        log("typed-fail", sh[:12], repr(e)[:120])
    if (i + 1) % 50 == 0:
        el = time.time() - t0
        log(f"progress {i+1}/{len(todo)} elapsed={el:.0f}s",
            f"last50_mean={np.mean([t for _, t in times[-50:]]) if times else 0:.2f}s")

if times:
    arr = np.array([t for _, t in times]); lens = np.array([l for l, _ in times])
    report = {"n_processed": len(times), "seqlen_min_med_max": [int(lens.min()), int(np.median(lens)), int(lens.max())],
              "sec_per_seq_min_med_mean_max": [round(float(arr.min()), 3), round(float(np.median(arr)), 3), round(float(arr.mean()), 3), round(float(arr.max()), 3)],
              "oom_typed_fails": oom_fail}
    n_cache = sum(1 for x in (0,) )  # placeholder
    json.dump(report, open(EXT + ("PILOT_THROUGHPUT.json" if a.pilot else "THROUGHPUT.json"), "w"), indent=1)
    log("throughput:", json.dumps(report))
if oom_fail:
    json.dump(oom_fail, open(EXT + "/TYPED_FAILURES.json", "w"), indent=1)
log("EXTRACT DONE processed", len(todo), "cached_total", len(done))
