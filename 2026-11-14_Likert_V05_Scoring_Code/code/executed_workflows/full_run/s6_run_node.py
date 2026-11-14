#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s6_run_node — the single active-budget runner for the combined fixed manifest.

Runs on the Chenyu persistent CPU environment (card: one active executor; local
does assembly only). Two sources per target:
  legacy440 — rendered at runtime from the node's audited frozen tables through
              the S6 runtime render_slot (B480 index path), S4 semantics;
  foreign   — pre-rendered seven-dimension messages under input/requests6/
              (facts built locally from the answer itself; rater message carries
              no model name/old score/old rank).
Output validated by the reviewed S4-flow release_validation (JUDGE_REQUIRED is
judge-work, not a forced NE; caps/whitelists unchanged). One attempt per target,
zero retries; archive-first, cache/checkpoint identity dedup, one work lock.

Usage: python3 -B scripts/s6_run_node.py --deployment . --phase first|resume|status
        --key-file <private key path> --i-confirm-live-paid-calls
"""
import argparse, hashlib, json, os, sys
from pathlib import Path

sys.dont_write_bytecode = True
VERSION = "LIKERT_V05_20261111_S6_COMBINED"
HERE = Path(__file__).resolve().parent
S6 = HERE.parent
ap = argparse.ArgumentParser()
ap.add_argument("--deployment", required=True)
ap.add_argument("--phase", choices=["first", "resume", "status"], required=True)
ap.add_argument("--key-file")
ap.add_argument("--target-file")
ap.add_argument("--i-confirm-live-paid-calls", action="store_true")
A = ap.parse_args()

dep = json.loads((Path(A.deployment) / "DEPLOYMENT.json").read_text())
assert dep["release_id"] == VERSION
inp = Path(dep["input_root"]); work = Path(dep["work_root"]); runtime = Path(dep["runtime_root"])
bundle = Path(dep["base_bundle"])


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


man = json.loads((inp / "manifest/MANIFEST.json").read_text())
for name, d in man["input_files"].items():
    assert sha(inp / name) == d, "S6 input changed: " + name
for name, d in man["runtime_files"].items():
    assert sha(runtime / name) == d, "S6 runtime changed: " + name
cfgp = inp / "config/RUN_CONFIG_LIVE.json"
cfg = json.loads(cfgp.read_text())
conf = json.loads((inp / "config/F4_USER_CONFIG_CONFIRMATION.json").read_text())
appr = json.loads((inp / "approval/RELEASE_APPROVAL.json").read_text())
assert cfg["config_status"] == "USER_CONFIRMED_FROZEN"
assert conf["confirmed_config_sha256"] == sha(cfgp) and conf["confirmed_by"] == "USER" \
    and conf["live_paid_calls_authorized"] is True
assert appr["approved_for"] == "live_scoring" and appr["manifest_sha256"] == sha(inp / "manifest/MANIFEST.json")

import csv as _csv
trows = list(_csv.DictReader((inp / "targets/COMBINED_TARGETS.tsv").open(), delimiter="\t"))
ready = [r for r in trows if r["status"] in ("READY_RENDER_AT_RUN", "READY_RENDERED")]
FIRST = cfg["s6_scope"]["first_target"]
assert [r for r in ready if r["target_id"] == FIRST], "first target must be in READY set"

os.environ["LIKERT_V05_WORK_DIR"] = str(work)
os.environ["LIKERT_V05_RUN_ROOT"] = str(bundle / "data")
os.environ["LIKERT_V05_RELEASE_DIR"] = str(inp / "release")
os.environ["LIKERT_V05_RUN_ID"] = VERSION
if A.key_file:
    kp = Path(A.key_file).resolve()
    assert not (kp.is_relative_to(inp) or kp.is_relative_to(S6)), "credential must stay outside scoring tree"
    os.environ["DASHSCOPE_API_KEY"] = kp.read_text().strip()

sys.path.insert(0, str(runtime / "v05_release"))
sys.path.insert(0, str(runtime / "f2"))
sys.path.insert(0, str(runtime / "pipeline"))
sys.path.insert(0, str(HERE))  # s6_catalog (reference-catalog fill wiring)
import common_03a
common_03a.VERSION = VERSION
import build_items as BI
import release_validation as RV
import v05ctl as control
import v05_request_builder as vb
import run_lib as RUN

lock = control.acquire_lock()
if A.phase == "status":
    print(json.dumps({"targets_ready": len(ready), "first": FIRST,
                      "ledger": json.loads((work / "run/ledger/BUDGET_STATE.json").read_text())
                      ["attempts_used"]}, ensure_ascii=False))
    raise SystemExit(0)
if not A.i_confirm_live_paid_calls:
    raise SystemExit("Explicit --i-confirm-live-paid-calls is required.")
if not os.environ.get("DASHSCOPE_API_KEY"):
    raise SystemExit("DASHSCOPE_API_KEY not configured (value never logged).")

rules = json.loads((inp / "release/SCORE_RULES_RELEASE.json").read_text())
schema = json.loads((inp / "release/schema/RATING_OUTPUT_SCHEMA_RELEASE.json").read_text())
template = (inp / "release/prompt/USER_TEMPLATE_RELEASE.txt").read_text()
system = (inp / "release/prompt/SYSTEM_PROMPT_RELEASE.txt").read_text()
tables = BI.load_tables()

LEGACY_BY_UID = {r["target_id"]: r for r in ready if r["kind"] == "legacy440"}
FOREIGN_BY_UID = {r["target_id"]: r for r in ready if r["kind"] == "foreign"}


ANON_INDEX = {r["target_id"]: i for i,r in enumerate(ready)}

def items_for(selected):
    items = []
    anon_i = 0
    for r in selected:
        tid = r["target_id"]
        if r["kind"] == "foreign":
            ctx = json.loads((inp / ("requests6/CTX_%s.json" % tid)).read_text())
            art = json.loads((inp / ("requests6/ART_%s.json" % tid)).read_text())
            anon = ctx["anonymous_item_id"]
        else:
            # runtime render through the audited frozen tables on the node
            request, ctx, art, decision = BI.render_slot(tid, "F4I-7%03d" % ANON_INDEX[tid], tables, rules, schema, template, system)
            anon = ctx["anonymous_item_id"]
            (work / "run/rendered_legacy").mkdir(parents=True, exist_ok=True)
            for pre, obj in (("CTX", ctx), ("ART", art)):
                (work / "run/rendered_legacy" / ("%s_%s.json" % (pre, tid))).write_text(
                    json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
        anon_i += 1
        items.append({"b_slot_uid": tid, "case_id": ctx["case_id"], "batch": ctx["batch"],
                      "anonymous_item_id": anon, "user_message_sha256": ctx["user_message_sha256"],
                      "identity_echo": ctx["identity_echo"], "ctx": ctx, "artifact": art,
                      "validation_context": {"schema": schema}})
    return items


runner, _ = control.build_runner(str(cfgp), str(work / "run"), True,
                                 sha(inp / "targets/COMBINED_TARGETS.tsv"), "COMBINED_FULL_FIXED_MANIFEST")
selected = [r for r in ready if r["target_id"] == FIRST] if A.phase == "first" else ready
if A.target_file:
    if A.phase != "resume":
        raise SystemExit("--target-file is only allowed in resume phase")
    requested = [r["target_id"] for r in _csv.DictReader(Path(A.target_file).open(), delimiter="\t")]
    if len(set(requested)) != len(requested) or not set(requested) <= {r["target_id"] for r in ready}:
        raise SystemExit("invalid or duplicate subset target list")
    selected = [r for r in ready if r["target_id"] in set(requested)]

if A.phase == "resume":
    ff = work / "S6_FIRST_RESULT.json"
    if not ff.is_file():
        raise SystemExit("no first-target result; do not submit the rest")
    prevres = json.loads(ff.read_text())
    if prevres["config_sha256"] != sha(cfgp) or not prevres["results"] or \
            prevres["results"][0]["system_run_status"] != "OK":
        raise SystemExit("first target did not succeed under this config; stop")
summary = runner.run_items(items_for(selected))
result = {"stage": "COMBINED_FULL_FIXED_MANIFEST", "phase": A.phase, "release_id": VERSION,
          "config_sha256": sha(cfgp), "n_ok": summary["n_ok"], "n_failed": summary["n_failed"],
          "results": [{k: v for k, v in r.items() if k in ("b_slot_uid", "system_run_status",
                      "error_kind", "deduped", "cache_hit", "recovered_from_archive")}
                      for r in summary["results"]],
          "ledger": summary["ledger"], "full_run_started": True,
          "total_estimate_guard_cny": 1000,
          "not_token_plan_verified_cash_charge": True,
          "auto_full": False,
          "note": "NE/REVIEW_PENDING are legal terminal states; technical pass != scientific approval"}
out = (work / "S6_FIRST_RESULT.json") if A.phase == "first" else (work / "S6_RUN_SUMMARY.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ("n_ok", "n_failed", "ledger")}, ensure_ascii=False))
raise SystemExit(0 if result["n_failed"] == 0 else 1)
