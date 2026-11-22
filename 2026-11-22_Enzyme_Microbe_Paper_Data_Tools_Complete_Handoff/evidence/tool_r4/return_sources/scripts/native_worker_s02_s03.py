#!/usr/bin/env python3
"""R4 node worker: one formal retained real call for each of the two fixed steps.

Task: today's closeout card, item 3. Single process; holds the SAME task GPU
lock as the 2026-11-21 numeric-control job (non-blocking; on contention the
worker STOPS without touching the GPU). Order: lock -> GPU idle check ->
CPU identity/ledger/pool verification -> native C95 index build (merged
stores, read-only) + per-UID asset availability check -> load five 3B
checkpoints (SHA-verified) -> exactly one wrapper-backend whole-step call per
step (S02 then S03, frozen pool order, no candidate dropped, no second
sigmoid: trace values are per-seed probabilities, averaged once by the
wrapper) -> raw persisted immediately per call -> end receipts.

Writes only under its own fresh OUT dir on the node. Never overwrites a
previous attempt. Technical failure: record and exit; no retry-until-pass.
"""
import fcntl, hashlib, json, math, os, subprocess, sys, time, traceback
from pathlib import Path

BASE = Path("/usrdata/EnzymeCAGE_data/workspaces/current95_ngpu32g_20261031")
OLD5 = BASE / "old_five_numeric_control_20261121"          # 11/21 GPU task root (lock holder)
OLD = BASE / "five_model_complete_20261103"
PKG = OLD / "current95_five_model_complete_prep_20261103"
A109 = BASE / "a109_admission_resume_20261102_run"
R3 = BASE / "asset_repair_r3_20261101/output"
REPO = Path("/usrdata/EnzymeCAGE_data/EnzymeCAGE-master")
WRAP_PKG = REPO / "HPC_Returned_Result_Summaries/d4b1a_wrapper_hash_relative_path_final_package_correction_20260716"
SRC_SNAP = Path("/usrdata/EnzymeCAGE_data/workspaces/path_enzyme_microbe_code_review_20261110/review_payload/src_snapshot")
V1 = REPO / "HPC_Returned_Result_Summaries/enzymecage_v1_20260714"
R4TOOL = Path(os.environ["R4_TOOL"])
EXPECTED = json.loads(Path(os.environ["R4_EXPECTED"]).read_text())  # driver-staged copy of scripts/expected_identities.json
LEDGER = json.loads(Path(os.environ["R4_LEDGER"]).read_text())
ARCHIVE = Path(os.environ["R4_ARCHIVE"])  # = $OLD (for gf_out evidence)
CTX = "main"

def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(8 << 20), b""):
            h.update(blk)
    return h.hexdigest()

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def query(args):
    return subprocess.run(["nvidia-smi"] + args, capture_output=True, text=True, check=True).stdout.strip()

def main():
    # never overwrite: attempt dir chosen by driver via env R4_ATTEMPT_DIR (must not exist)
    AT = Path(os.environ["R4_ATTEMPT_DIR"])
    assert not AT.exists(), f"ATTEMPT_DIR_EXISTS {AT}"
    AT.mkdir(parents=True)
    def w(name, obj):
        (AT / name).write_text(json.dumps(obj, indent=1, default=vars, allow_nan=False))

    lock_path = OLD5 / "gpu.lock"
    fd = os.open(lock_path, os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("GPU_LOCK_HELD_BY_OTHER_TASK: not contending, not waiting, aborting")
        return 3
    w("LOCK_ACQUIRED.json", {"lock": str(lock_path), "utc": now(),
                             "mode": "same-task non-blocking exclusive lock as 2026-11-21 job"})
    gpus = query(["--query-gpu=index,uuid,memory.used,utilization.gpu", "--format=csv,noheader"])
    procs = query(["--query-compute-apps=pid,gpu_uuid,used_memory", "--format=csv,noheader"])
    assert procs == "", f"FOREIGN_GPU_PROCESS: {procs}"
    visible = os.environ.get("CUDA_VISIBLE_DEVICES")
    print("GPU_STATE", gpus.replace("\n", " | "), flush=True)

    # ---- CPU: source & checkpoint identity ----
    mod_roots = {"wrapper_predictor": SRC_SNAP / "wrapper/predictor.py",
                 "enzymecage_model": REPO / "enzymecage/model.py",
                 "enzymecage_dataset_geometric": REPO / "enzymecage/dataset/geometric.py",
                 "c95_asset_index_ext": PKG / "historical/a109/c95_asset_index_ext.py",
                 "recovery_helpers": PKG / "scripts/recovery_helpers.py",
                 "r3_gf_unified": PKG / "sources/r3_gf_unified.py",
                 "enzymecage_wrapper_asset_index": WRAP_PKG / "enzymecage_wrapper/asset_index.py"}
    ids = {k: sha_file(p) for k, p in mod_roots.items()}
    drift = {k: (v, EXPECTED["modules"].get(k)) for k, v in ids.items() if EXPECTED["modules"].get(k) and EXPECTED["modules"][k] != v}
    assert not drift, f"MODULE_SHA_DRIFT {drift}"
    ck = {}
    for seed, want in EXPECTED["checkpoints"].items():
        p = V1 / f"3b_ensemble/seed_{seed}/best_model.pth"
        got = sha_file(p); assert got == want, f"CKPT_SHA_MISMATCH seed{seed}"
        ck[seed] = {"path": str(p), "sha256": got, "bytes": p.stat().st_size}

    # ---- CPU: gate + ledger vs frozen pool + archive raw identity ----
    sys.path.insert(0, str(R4TOOL)); sys.path.insert(0, str(PKG / "scripts"))
    import recovery_helpers as RH
    gate = RH.require_scoring_gate(str(OLD / "runtime/pool"))
    st = OLD / "runtime/pool/UNIFIED_STEP_TABLE_main.json"
    assert sha_file(st) == EXPECTED["step_table_main_sha256"] == gate["step_table_sha256"][CTX], "STEP_TABLE_SHA"
    steps = {s["step_id"]: s for s in json.loads(st.read_text())}
    for sid, led in LEDGER["steps"].items():
        m = steps[sid]
        assert m["pool_uids"] == led["pool_uids"] and m["pool_shas"] == led["pool_shas"], sid
        assert m["model_reaction"] == led["model_reaction"] and m["model_key_sha256"] == led["model_key_sha256"], sid
        assert hashlib.sha256(m["model_reaction"].encode()).hexdigest() == m["model_key_sha256"]
        # 11/4 raw-logits original on the node (same bytes as the returned archive member)
        node_raw = OLD / "gf_out" / EXPECTED["evidence_members"][sid]
        assert sha_file(node_raw) == led["raw_evidence_sha256"], f"EVIDENCE_RAW_SHA {sid}"
        j = json.loads(node_raw.read_text())
        assert j["pool_uids"] == led["pool_uids"] and j["pool_shas"] == led["pool_shas"] and j["model_key_sha256"] == led["model_key_sha256"]
        assert set(j["seed_identities"]) == {"40", "41", "42", "43", "44"}

    # ---- CPU: native C95 index (merged stores) + per-UID availability ----
    from enzyme_host_tool import native_c95_assets as NC
    nb = {"pkg": str(PKG), "a109": str(A109), "c95_dir": str(PKG / "historical/a109"), "wrap_pkg_root": str(WRAP_PKG), "rh_dir": str(PKG / "scripts"),
          "enzymecage_source_root": str(REPO),
          "merged_cfg": {CTX: str(R3 / f"materialize_{CTX}/cfg/c95_3b_merged_config.yaml")},
          "module_shas": {k: {"path": str(p), "sha256": EXPECTED["modules"].get(k)} for k, p in mod_roots.items()}}
    t0 = time.time()
    idx = NC.build_native_c95_index(nb, CTX)
    avail = {}
    for sid, led in LEDGER["steps"].items():
        a = {u: bool(idx.has_enzyme(u)) for u in led["pool_uids"]}
        miss = idx.missing_assets(led["model_reaction"])
        avail[sid] = {"available": sum(a.values()), "n": len(a), "missing_assets_for_query": miss}
    w("CPU_PREFLIGHT.json", {"utc": now(), "index_build_sec": round(time.time() - t0, 1),
                             "inventory": {k: (v if isinstance(v, (int, str)) else None) for k, v in idx.inventory().items() if isinstance(v, (int, str))},
                             "availability": avail, "gate": gate["status"], "module_ids": ids,
                             "pool_order_verified": True, "checkpoint_receipts": ck})

    # ---- GPU: one runtime, one formal call per step ----
    from enzyme_host_tool.config import ScoringCfg
    from enzyme_host_tool.scoring_backends import EnzymeCAGEWrapperNativeC95Backend
    cfg = ScoringCfg(backend="enzyme_cage_wrapper_native_c95", wrapper_code_root=str(SRC_SNAP),
                     enzymecage_source_root=str(REPO), weights_package_root=str(V1), top_k=10, return_ci=True,
                     native_binding={"paths": nb, "ctx": CTX})
    be = EnzymeCAGEWrapperNativeC95Backend(cfg)
    # inject prebuilt index path: build runtime via adapter with prebuilt_idx
    be._runtime_factory = lambda: NC.make_native_runtime(cfg, nb, CTX, prebuilt_idx=idx)
    start = {"utc": now(), "gpu": gpus, "operation": "one formal retained whole-step real call per fixed step",
             "steps_order": list(LEDGER["steps"])}
    w("START.json", start)
    results = {}
    for sid, led in LEDGER["steps"].items():
        t0 = time.time()
        out = be.score(led["model_reaction"], list(zip(led["pool_uids"], led["pool_shas"])))
        rt = be._rt
        trace = dict(rt.last_trace or {})
        payload = {"step_id": sid, "utc_after_call": now(), "sec": round(time.time() - t0, 1),
                   "status": out.status, "query": led["model_reaction"], "model_key_sha256": led["model_key_sha256"],
                   "pool_uids_frozen_order": led["pool_uids"], "score_outcome": out, "last_trace": trace,
                   "trace_semantics": "PER_SEED_PROBABILITIES_FROM_MODEL_EVALUATE; averaged ONCE by wrapper; no second sigmoid applied anywhere",
                   "protocol": "WHOLE_STEP (differs from C2 bounded16; value-equality not required and not asserted)"}
        (AT / f"RAW_{sid}.json").write_text(json.dumps(payload, indent=1, default=vars, allow_nan=False))
        # ---- post-call accounting asserts (after raw is on disk) ----
        valid = trace.get("valid_uids", []) or []
        vs = trace.get("per_seed_scores", []) or []
        ne = {x.uid for x in out.not_evaluated}
        assert out.status == "OK", f"STATUS_NOT_OK {sid}: {out.status}"
        assert len(vs) == 5 and all(len(v) == len(valid) for v in vs)
        assert all(all(isinstance(x, (int, float)) and math.isfinite(x) and 0.0 <= x <= 1.0 for x in v) for v in vs)
        assert set(valid) | ne == set(led["pool_uids"]) and not (set(valid) & ne)
        means = {u: sum(v[i] for v in vs) / 5.0 for i, u in enumerate(valid)}
        order = sorted(valid, key=lambda u: (-means[u], u))
        assert [c.uid for c in out.all_scored] == order and len(order) == len(valid)
        assert all(abs(c.score - means[c.uid]) < 1e-15 for c in out.all_scored)
        assert [c.display_rank for c in out.all_scored[:10]] == list(range(1, 11))
        results[sid] = {"scored": len(out.all_scored), "typed_missing": len(out.not_evaluated),
                        "complete_all_candidates": len(ne) == 0,
                        "top1": (out.all_scored[0].uid, out.all_scored[0].score) if out.all_scored else None,
                        "mean_c2_note": "C2 protocol differs (bounded16 lane + frozen ranks); value equality NOT asserted",
                        "sec": round(time.time() - t0, 1)}
        print(f"CALL_DONE {sid} scored={len(out.all_scored)} ne={len(out.not_evaluated)}", flush=True)
    end = {"utc": now(), "gpu_after": query(["--query-gpu=index,memory.used,utilization.gpu", "--format=csv,noheader"]),
           "compute_apps_after": query(["--query-compute-apps=pid,used_memory", "--format=csv,noheader"]),
           "api_successful_requests": getattr(be._rt, "forward_call_count", None),
           "models_loaded": 5, "seeds": [40, 41, 42, 43, 44],
           "source_shas_end": {k: sha_file(p) for k, p in mod_roots.items()},
           "checkpoint_shas_end": {s: sha_file(V1 / f"3b_ensemble/seed_{s}/best_model.pth") for s in EXPECTED["checkpoints"]},
           "pool_sha_end": sha_file(st)}
    assert end["source_shas_end"] == ids and end["checkpoint_shas_end"] == {s: c["sha256"] for s, c in ck.items()}
    assert end["pool_sha_end"] == EXPECTED["step_table_main_sha256"]
    w("END.json", end)
    w("RESULT.json", {"kind": "TOOL_R4_S02_S03_REAL_NATIVE_C95_CALLS", "start": start, "per_step": results,
                      "end": end, "all_candidates_accounted": all(v["scored"] + v["typed_missing"] == LEDGER["steps"][k]["n_candidates"] for k, v in results.items())})
    print("AUDIT_RESULT=" + json.dumps({"results": results, "end_utc": end["utc"]}, default=vars))
    return 0

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    try:
        rc = main()
    except Exception:
        print("WORKER_FAILED:\n" + traceback.format_exc(), flush=True)
        try:
            Path(os.environ["R4_ATTEMPT_DIR"]).mkdir(parents=True, exist_ok=True)
            (Path(os.environ["R4_ATTEMPT_DIR"]) / "FAIL.json").write_text(traceback.format_exc())
        except Exception:
            pass
        rc = 1
    sys.exit(rc)
