#!/usr/bin/env python3
"""package_g8_formal_return.py -- formal return packager (complete OR partial).

Derived from the PASSED R2 V1.2 packager lineage. G8 changes (card-permitted):
- a return is packagable in ANY terminal combination (COMPLETE / HTTP_ERROR /
  TRANSPORT_ERROR); "all 484 JSON success" is NOT a return condition;
- PARTIAL returns are first-class: budget-stop / service-failure-stop /
  drift-stop runs package with NOT_DISPATCHED and RESULT_UNKNOWN_HELD slots
  listed explicitly and honestly in the identity (unknown-result slots are
  never re-sent and never presented as un-requested);
- LIVE transport required; every SELF_TEST marker is refused;
- run/SHA256SUMS + recursive audit/SHA256SUMS (dual SHA) and a detached
  replay_package that re-runs the receiver without the source package;
- raw evidence may be large: the packager emits a volume manifest
  (path/bytes/sha256 per raw_stream.sse) bound into the identity so raw can be
  shipped as separate volumes while staying hash-bound.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def refuse(msg):
    sys.stderr.write("REFUSE: " + msg + "\n"); sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exec-package", required=True, help="formal exec package root (contains inputs/ and scripts/)")
    ap.add_argument("--run", required=True, help="formal run dir to package")
    ap.add_argument("--out-dir", default=None, help="output dir (default: exec package root)")
    ap.add_argument("--allow-partial", action="store_true",
                    help="required to package a run that is not 484/484 terminal")
    ap.add_argument("--rehearsal-mode", action="store_true",
                    help="package a SELF_TEST run as a clearly-marked SELF_TEST_REHEARSAL artifact "
                         "(regression evidence; NEVER a formal return)")
    a = ap.parse_args()
    pkgroot = os.path.abspath(a.exec_package)
    run = os.path.abspath(a.run)
    if run != os.path.join(pkgroot, "run"):
        refuse("--run must be exactly <exec-package>/run (tar members are pkgroot-relative, lineage contract)")
    out_dir = os.path.abspath(a.out_dir or pkgroot)
    inputs = os.path.join(pkgroot, "inputs")
    if not os.path.isdir(inputs): refuse("inputs/ missing in exec package")
    if not os.path.isfile(os.path.join(run, "run_summary.json")): refuse("no run to return")
    for need in ("decision/g8_formal_status.json", "decision/completion_matrix.tsv", "RUN_REPORT.md"):
        if not os.path.exists(os.path.join(run, need)):
            refuse("receiver output missing (%s): run validate_g8_formal_return.py first" % need)

    rs = json.load(open(os.path.join(run, "run_summary.json"), encoding="utf-8"))
    rehearsal = False
    if rs.get("transport") == "LIVE":
        rehearsal = False
    elif rs.get("transport") == "SELF_TEST" and a.rehearsal_mode:
        rehearsal = True
    else:
        refuse("formal return requires LIVE transport, got %r (SELF_TEST packagable only with --rehearsal-mode)"
               % rs.get("transport"))
    dec = json.load(open(os.path.join(run, "decision", "g8_formal_status.json"), encoding="utf-8"))
    if dec.get("g8_formal_status") == "G8_INTEGRITY_FAIL_AUDIT_BLOCKED":
        refuse("integrity-blocked runs are not formal-packagable; fix the audit path first (evidence kept)")
    tc = dec["terminal_counts"]; n_terminal = sum(tc.values())
    held = dec.get("result_unknown_held_slots") or []
    undis = dec.get("not_dispatched_slots") or []
    partial = n_terminal < 484 or held or undis
    if partial and not a.allow_partial:
        refuse("run is PARTIAL (terminal=%d held=%d not_dispatched=%d); rerun with --allow-partial to package honestly"
               % (n_terminal, len(held), len(undis)))
    acu = rs.get("api_calls_used")
    if not isinstance(acu, int) or isinstance(acu, bool) or not (0 <= acu <= 484):
        refuse("api_calls_used invalid: %r" % acu)

    # self-test marker sweep over the whole run tree (formal path only)
    if not rehearsal:
        for dp, dns, fns in os.walk(run):
            for f in fns:
                if not f.endswith((".json", ".txt", ".md", ".tsv")): continue
                body = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
                for marker in ("SELF_TEST_MOCK", "x-self-test", "SELF_TEST"):
                    if marker in body:
                        refuse("self-test marker %r found in run/%s" % (marker, os.path.relpath(os.path.join(dp, f), run)))
    for dp, dns, fns in os.walk(run):
        if any("self_test" in f.lower() or f.startswith("st_") for f in fns):
            refuse("run/ contains self-test artifact under %s" % dp)
    # every terminal slot must carry the transport-consistent label
    live_labels = 0
    want_label = "SELF_TEST_MOCK" if rehearsal else "LIVE_G8_FORMAL_RESPONSE"
    for e in rs.get("slots", []):
        if e.get("status") in ("COMPLETE", "HTTP_ERROR", "TRANSPORT_ERROR"):
            pm_path = os.path.join(run, "slots", e["slot"], "parse_meta.json")
            if not os.path.isfile(pm_path): refuse("terminal slot without parse_meta: %s" % e["slot"])
            pm = json.load(open(pm_path, encoding="utf-8"))
            if pm.get("fixture_label") != want_label:
                refuse("fixture_label not %r in %s: %r" % (want_label, e["slot"], pm.get("fixture_label")))
            live_labels += 1
    if live_labels != n_terminal:
        refuse("live label count %d != terminal count %d" % (live_labels, n_terminal))

    # ---- outputs only after all checks pass ----
    run_files = sorted(os.path.relpath(os.path.join(dp, f), run)
                       for dp, dns, fns in os.walk(run) for f in fns
                       if f not in ("SHA256SUMS", ".runner.lock") and not f.endswith(".pyc") and "__pycache__" not in dp)
    with open(os.path.join(run, "SHA256SUMS"), "w", encoding="utf-8") as fh:
        for f in run_files: fh.write("%s  run/%s\n" % (sha(os.path.join(run, f)), f))

    raw_volumes = []
    for f in run_files:
        if f.endswith("raw_stream.sse"):
            p = os.path.join(run, f)
            raw_volumes.append({"path": "run/" + f, "bytes": os.path.getsize(p), "sha256": sha(p)})

    audit = os.path.join(pkgroot, "audit")
    rp = os.path.join(audit, "replay_package")
    shutil.rmtree(audit, ignore_errors=True)
    os.makedirs(os.path.join(rp, "scripts"), exist_ok=True)
    # replay package: receiver + minimal frozen inputs needed to re-run it detached
    shutil.copy2(os.path.join(HERE, "validate_g8_formal_return.py"), os.path.join(rp, "scripts", "validate_g8_formal_return.py"))
    for sub in ("schemas",):
        os.makedirs(os.path.join(rp, "inputs", sub), exist_ok=True)
    for f in ("package.json", "task_slots.tsv", "SHA256SUMS"):
        shutil.copy2(os.path.join(inputs, f), os.path.join(rp, "inputs", f))
    for f in os.listdir(os.path.join(inputs, "schemas")):
        shutil.copy2(os.path.join(inputs, "schemas", f), os.path.join(rp, "inputs", "schemas", f))
    # request bodies are needed for byte-equality chain checks
    os.makedirs(os.path.join(rp, "inputs", "request_bodies"), exist_ok=True)
    for f in os.listdir(os.path.join(inputs, "request_bodies")):
        shutil.copy2(os.path.join(inputs, "request_bodies", f), os.path.join(rp, "inputs", "request_bodies", f))
    open(os.path.join(audit, "README_DETACHED_REPLAY.md"), "w", encoding="utf-8").write(
        "# 脱离源包的确定性复算（不修改原始 run/ 证据）\n"
        "在 return tar 解包根目录执行：\n```bash\n"
        'REPLAY=$(mktemp -d)/replay_package\ncp -r audit/replay_package "$REPLAY"\ncp -r run "$REPLAY/run"\n'
        'python3 "$REPLAY/scripts/validate_g8_formal_return.py" --inputs "$REPLAY/inputs" --run "$REPLAY/run"\n'
        'cmp run/decision/g8_formal_status.json "$REPLAY/run/decision/g8_formal_status.json"\n'
        'cmp run/decision/completion_matrix.tsv "$REPLAY/run/decision/completion_matrix.tsv"\n'
        'cmp run/RUN_REPORT.md "$REPLAY/run/RUN_REPORT.md"\nsha256sum -c run/SHA256SUMS\n```\n'
        "所有 cmp 与 sha256sum -c 必须通过。receiver 输出工程分类：COMPLETE/HTTP_ERROR/TRANSPORT_ERROR\n"
        "任意组合可回包；PARTIAL 如实标注；每模型分母恒为121；失败槽不删除、不修复、不补问。\n")
    asums = []
    for dp, dns, fns in os.walk(audit):
        for f in sorted(fns):
            rel = os.path.relpath(os.path.join(dp, f), audit)
            if rel == "SHA256SUMS": continue
            asums.append((rel, sha(os.path.join(dp, f))))
    with open(os.path.join(audit, "SHA256SUMS"), "w", encoding="utf-8") as fh:
        for rel, d in sorted(asums): fh.write("%s  audit/%s\n" % (d, rel))

    members = ["run/" + f for f in run_files + ["SHA256SUMS"]] + ["audit/" + rel for rel, _ in asums] + ["audit/SHA256SUMS"]
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    kind = "complete" if not partial else "partial"
    if rehearsal:
        tar = os.path.join(out_dir, "biosysmodb150_g8_SELF_TEST_REHEARSAL_return_%s_%s.tar.gz" % (kind, ts))
    else:
        tar = os.path.join(out_dir, "biosysmodb150_g8_formal_return_%s_%s.tar.gz" % (kind, ts))
    subprocess.run(["tar", "--sort=name", "--mtime=1970-01-01 00:00:00 UTC", "--owner=0", "--group=0",
                    "-czf", tar] + members, cwd=pkgroot, check=True)
    ident = {"return_package_version": "g8_formal_return_v1", "file": os.path.basename(tar),
             "mode": ("SELF_TEST_REHEARSAL" if rehearsal else "FORMAL"),
             "bytes": os.path.getsize(tar), "sha256": sha(tar),
             "return_kind": ("COMPLETE_484" if not partial else "PARTIAL_HONEST"),
             "run_sha256sums_sha256": sha(os.path.join(run, "SHA256SUMS")),
             "audit_sha256sums_sha256": sha(os.path.join(audit, "SHA256SUMS")),
             "g8_formal_status": dec.get("g8_formal_status"),
             "terminal_counts": tc, "usable_json_objects": dec["counts_overall"]["usable_json_objects"],
             "length_or_empty_union": dec["counts_overall"]["length_or_empty_union"],
             "result_unknown_held_slots": held, "not_dispatched_count": len(undis),
             "api_calls_committed_total": acu,
             "budget_state": rs.get("budget"), "stop_reason": rs.get("stop_reason"),
             "raw_volume_manifest_entries": len(raw_volumes),
             "raw_volume_manifest_sha256": None,
             "contains_key": False, "contains_self_test": False, "run_transport": "LIVE",
             "per_model_denominator": 121,
             "detached_replay": "see audit/README_DETACHED_REPLAY.md"}
    vm_path = tar + ".raw_volumes.json"
    json.dump(raw_volumes, open(vm_path, "w"), ensure_ascii=False, indent=1, sort_keys=True)
    ident["raw_volume_manifest_sha256"] = sha(vm_path)
    json.dump(ident, open(tar + ".identity.txt", "w"), ensure_ascii=False, indent=2, sort_keys=True)
    open(tar + ".identity.txt", "a").write("\n")
    print("return package:", os.path.basename(tar), os.path.getsize(tar), "bytes", sha(tar)[:16],
          "| kind:", ident["return_kind"], "| terminal:", n_terminal, "| held:", len(held), "| undispatched:", len(undis))


if __name__ == "__main__":
    main()
