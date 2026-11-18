#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v05ctl — LIKERT V0.5 release runner CLI (bundle-local, self-contained).

Commands: preflight | mock | build-items | start-calibration | status | resume |
stop | export | start-full.

Hard boundaries implemented here (card 03E §7 / CAL32-ONLY node card):
  * stage=CALIBRATION_ONLY: exactly the frozen CALIBRATION_TARGETS.tsv 32 slots;
    auto_full=false; start-full refuses without RELEASE_APPROVAL.json +
    CALIBRATION_RELEASE.json;
  * live sends require: confirmed run config + user confirmation record binding
    its sha + --i-confirm-live-paid-calls + api key env var present (name only);
  * unique run lock (flock); resume uses archive-first/cache/checkpoint
    recovery and never re-buys a received response; REVIEW_PENDING/NE/valid low
    scores are never re-sampled;
  * logs/responses/usage/locks stay in WORK (persistent disk), never in INPUT.
"""
import json, os, subprocess, sys, fcntl, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "f2"))
sys.path.insert(0, str(HERE.parent / "pipeline"))
from common_03a import OUT, RUN_ROOT, VERSION, sha, load, rows
import release_validation as relval
import v05_request_builder as vb
import run_lib as RUN


def work_dir():
    return Path(os.environ.get("LIKERT_V05_WORK_DIR", str(BUNDLE / "work")))


def calib_slots():
    ts = OUT / "targets/CALIBRATION_TARGETS.tsv"
    slots = [r["b_slot_uid"] for r in rows(ts)]
    assert len(slots) == 32 and len(set(slots)) == 32, "calibration list must be exactly 32 unique"
    return slots, sha(ts.read_bytes())


def load_items(slots):
    items = []
    base = OUT / "requests/calibration32"
    for s in slots:
        ctx = load(base / ("CTX_%s.json" % s))
        art = load(base / ("ART_%s.json" % s))
        items.append({"b_slot_uid": s, "case_id": ctx["case_id"], "batch": ctx["batch"],
                      "anonymous_item_id": ctx["anonymous_item_id"],
                      "user_message_sha256": ctx["user_message_sha256"],
                      "identity_echo": ctx["identity_echo"],
                      "ctx": ctx, "artifact": art})
    return items


def full_items():
    base = OUT / "requests/full"
    if not base.is_dir():
        raise SystemExit("full requests not pre-rendered; run build-items first (writes to WORK)")
    slots = [r["b_slot_uid"] for r in rows(OUT / "targets/RATING_TARGETS.tsv")
             if r["send_flag"] == "SEND"]
    items = []
    for s in slots:
        p = base / ("CTX_%s.json" % s)
        if not p.is_file():
            continue  # rendered into WORK copy by build-items; caller merges dirs
        ctx = load(p)
        items.append({"b_slot_uid": s, "case_id": ctx["case_id"], "batch": ctx["batch"],
                      "anonymous_item_id": ctx["anonymous_item_id"],
                      "user_message_sha256": ctx["user_message_sha256"],
                      "identity_echo": ctx["identity_echo"],
                      "ctx": ctx, "artifact": load(base / ("ART_%s.json" % s))})
    return items


def acquire_lock():
    wk = work_dir()
    wk.mkdir(parents=True, exist_ok=True)
    fh = open(wk / "LOCK", "w")
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print(json.dumps({"error": "another run holds the WORK lock; refusing duplicate paid run"}))
        sys.exit(2)
    fh.write(str(os.getpid()))
    fh.flush()
    return fh


def build_runner(cfg_path, run_root, live, slots_sha, scope_name):
    if not live:
        cfg_path = str(OUT.parent / "config/RUN_CONFIG_MOCK.json")
    cfg = vb.load_config(cfg_path)
    conf = None
    p = Path(cfg_path).parent / "F4_USER_CONFIG_CONFIRMATION.json"
    if p.is_file():
        conf = load(p)
    reasons = vb.config_gate(cfg, conf, require_confirmed=live)
    if live:
        if reasons:
            raise SystemExit("live refused: " + "; ".join(reasons))
        if not relval.release_approved():
            raise SystemExit("live refused: RELEASE_APPROVAL.json missing or not bound to MANIFEST sha")
        api_env = (cfg.get("run_boundaries") or {}).get("api_key_env_var_name")
        if not (api_env and not str(api_env).startswith("PENDING") and api_env in os.environ):
            raise SystemExit("live refused: api key env var absent (checked by name only; value never read/logged)")
        transport = RUN.build_live_transport(cfg, lambda c, f, k: RUN.live_gate_reasons(
            c, conf, True, k), True)
        prices = None
    else:
        script = {}
        sp = work_dir() / "MOCK_SCRIPT.json"
        if sp.is_file():
            script = load(sp)
        transport = RUN.MockTransport(script)
    from f2r12_common import sha256_file
    evman = RUN_ROOT / "LIKERT_V04_FULL_SCORING_20261029/F3_EVIDENCE_R1_1/EVIDENCE_MANIFEST_R1_1.json"
    runner = RUN.ScoringRunner(
        cfg, run_root, transport, load(__import__("common_03a").SCHEMA_PATH),
        price_in_per_1m=float((cfg.get("cost") or {}).get("price_basis", {}).get("input_busy_cny_per_1M") or 0.0),
        price_out_per_1m=float((cfg.get("cost") or {}).get("price_basis", {}).get("output_busy_cny_per_1M") or 0.0),
        run_id=RUN_ID(run_root),
        synthetic_test_prices=not live,
        evidence_identity_sha256=sha256_file(evman))
    runner.v05_scope = {"scope": scope_name, "calibration_targets_sha256": slots_sha}
    return runner, live


def RUN_ID(run_root):
    meta = Path(run_root) / "RUN_ID"
    if meta.is_file():
        return meta.read_text().strip()
    rid = os.environ.get("LIKERT_V05_RUN_ID") or ("%s_R_%s" % (VERSION, time.strftime("%Y%m%dT%H%M%S")))
    meta.parent.mkdir(parents=True, exist_ok=True)
    meta.write_text(rid + "\n")
    return rid


def cmd_preflight(a):
    wk = work_dir()
    r = subprocess.run([sys.executable, str(BUNDLE / "preflight/run_offline_battery.py"), "--work", str(wk)],
                       capture_output=True, text=True)
    print(r.stdout[-4000:] or r.stderr[-4000:])
    return r.returncode


def cmd_mock(a):
    wk = work_dir()
    slots, ssha = calib_slots()
    runner, _ = build_runner(str(OUT.parent / "config/RUN_CONFIG_DRAFT.json"), str(wk / "mock_run"), False, ssha, "CALIBRATION_MOCK")
    items = load_items(slots)
    summary = runner.run_items(items)
    print(json.dumps({k: v for k, v in summary.items() if k != "results"}, ensure_ascii=False))
    return 0


def cmd_build_items(a):
    out = a[0] if a else str(work_dir() / "items/full")
    r = subprocess.run([sys.executable, str(HERE / "build_items.py"), "full", out],
                       capture_output=True, text=True)
    print(r.stdout[-2000:] or r.stderr[-4000:])
    return r.returncode


def _start(a, live):
    slots, ssha = calib_slots()
    wk = work_dir()
    lock = acquire_lock()
    stage = wk / "STAGE.json"
    stage.write_text(json.dumps({"stage": "CALIBRATION_ONLY" if live else "CALIBRATION_MOCK",
                                  "auto_full": False, "calibration_targets_sha256": ssha}))
    cfgp = str(OUT.parent / "config/RUN_CONFIG_LIVE.json") if live else str(OUT.parent / "config/RUN_CONFIG_DRAFT.json")
    runner, _ = build_runner(cfgp, str(wk / "run"), live, ssha, "CALIBRATION_ONLY")
    items = load_items(slots)
    summary = runner.run_items(items)
    (wk / "run" / "SUMMARY.json").write_text(json.dumps(
        {k: v for k, v in summary.items() if k != "results"}, ensure_ascii=False, indent=1))
    return 0 if summary["n_failed"] == 0 else 1


def cmd_status(a):
    wk = work_dir()
    out = {"work": str(wk), "lock_pid": (wk / "LOCK").read_text() if (wk / "LOCK").is_file() else None,
           "stage": load(wk / "STAGE.json") if (wk / "STAGE.json").is_file() else None}
    try:
        runner, _ = build_runner(str(OUT.parent / "config/RUN_CONFIG_DRAFT.json"), str(wk / "run"), False, "-", "STATUS")
        out["ledger"] = runner.ledger.snapshot()
        out["checkpoint_committed"] = len(runner.checkpoint.state.get("committed_slots", {}))
    except Exception as e:
        out["checkpoint_raw"] = str(wk / "run/CHECKPOINT.json")
        out["status_error"] = str(e)[:200]
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


def cmd_stop(a):
    wk = work_dir()
    (wk / "STOP_REQUESTED").write_text("stop requested by operator\n")
    lp = wk / "LOCK"
    if lp.is_file():
        pid = lp.read_text().strip()
        try:
            os.kill(int(pid), 15)
            print(json.dumps({"signalled": pid}))
        except Exception as e:
            print(json.dumps({"stop_flag_written": True, "kill_error": str(e)}))
    print(json.dumps({"note": "platform shutdown/billing is the user's arrangement; this only stops THIS worker"}))
    return 0


def cmd_export(a):
    wk = work_dir()
    rid = RUN_ID(wk / "run")
    outp = Path(a[0]) if a else wk
    ts = time.strftime("%Y%m%dT%H%M%S")
    name = "LIKERT_V05_%s_CAL32_%s" % (rid, ts)
    r = subprocess.run(["tar", "-czf", str(outp / (name + ".tar.gz")), "-C", str(wk), "run"],
                       capture_output=True, text=True)
    sha_b = sha((outp / (name + ".tar.gz")).read_bytes())
    (outp / (name + ".tar.gz.sha256")).write_text(sha_b + "  " + name + ".tar.gz\n")
    print(json.dumps({"package": str(outp / (name + ".tar.gz")), "sha256": sha_b}))
    return r.returncode


def cmd_start_full(a):
    print(json.dumps({
        "refused": True,
        "reason": "this bundle ships stage=CALIBRATION_ONLY. start-full requires a separately issued "
                  "RELEASE_APPROVAL.json bound to manifest/MANIFEST.json sha AND a CALIBRATION_RELEASE.json "
                  "from the Astra-reviewed calibration return; both must be placed by the user, "
                  "and the full execution card is issued only after calibration review."}))
    return 3


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    cmd, rest = argv[0], [x for x in argv[1:] if not x.startswith("--i-confirm")]
    flag_live = "--i-confirm-live-paid-calls" in argv
    dispatch = {"preflight": cmd_preflight, "mock": cmd_mock, "build-items": cmd_build_items,
                "start-calibration": lambda a: _start(a, flag_live), "status": cmd_status,
                "resume": lambda a: _start(a, flag_live), "stop": cmd_stop, "export": cmd_export,
                "start-full": cmd_start_full}
    if cmd not in dispatch:
        print("unknown command " + cmd)
        return 1
    return dispatch[cmd](rest)


if __name__ == "__main__":
    raise SystemExit(main())
