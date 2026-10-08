#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_formal_484_slot_index.py -- G9 offline merge index builder (READ-ONLY on sources).

TASK_ID: biosysmodb150_g9_four_model_121_formal_offline_score_20261008
API_CALLS=0. Reads only the two extracted formal return packages plus the frozen
G2 case list; never modifies scorer, gold, masks, or model answers; never copies
pilot/smoke/probe answers; never repairs JSON; never extracts answers from reasoning.

Outputs (written only under the G9 directory):
  FORMAL_484_SLOT_INDEX.tsv
  FORMAL_MERGE_MANIFEST.json
"""
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.abspath(os.path.join(HERE, os.pardir))
EX = os.path.abspath(os.path.join(G9, os.pardir))
BASE = os.path.abspath(os.path.join(EX, os.pardir))

TM_ROOT = os.path.join(G9, "source", "three_model")
KM_ROOT = os.path.join(G9, "source", "kimi")
TM_RUN = os.path.join(TM_ROOT, "formal_run")
KM_RUN = os.path.join(KM_ROOT, "kimi_run")

# Hard identities (execution card section 1). Verified before use.
SOURCE_IDENTITY = {
    "three_model": {
        "tar_name": "biosysmodb150_g6r3_glm_low_then_g8p1_three_model_return_20261007T015420Z.tar.gz",
        "bytes": 95804898,
        "sha256": "76a45fac8b54a3e5b6be549245cd7927233f4adbd9082766a886bf6bdf68b8ec",
        "audit_md": "BIOSYSMODB150_G6R3_GLM_LOW_G8P1_THREE_MODEL_FORMAL_RETURN_LOCAL_AUDIT_20261007.md",
        "audit_sha256": "4ede4adafe84901d322151e2500a246e0cb99a49f30c9f784658e5741305e3a6",
    },
    "kimi": {
        "tar_name": "biosysmodb150_g8p2_kimi_k3_121_formal_return_20261007T141621Z.tar.gz",
        "bytes": 117802093,
        "sha256": "e17504af6c2927e9ba37c9f31eb0ec75aa346bfdc1ac28badd213fbcdf31e34c",
        "audit_md": "BIOSYSMODB150_G8P2_KIMI_K3_121_FORMAL_RETURN_LOCAL_AUDIT_20261008.md",
        "audit_sha256": "4fbc0a029d551689c4e4d6c8986f785492d4fe85a40b1b366cac5915c758544e",
    },
}
AUTHORITY_MD = "BIOSYSMODB150_FOUR_MODEL_121_FORMAL_API_COLLECTION_CLOSURE_20261008.md"
AUTHORITY_SHA = "73314ebc41af42225f32aab2b2d7bb69b85c8b7d8a6efaed124e66b176da42bd"

# Embedded four-model input package bound by both stages (authority closure file).
INPUT_PACKAGE_SHA = "48a7e6835fe65994c14b293f4d4ead36aa616835c8727a82abc3f84c559fb222"
# Per-package dispatch matrix (what run_summary.matrix_sha256 actually binds).
DISPATCH_MATRIX_RELPATH = {
    "three_model": "derived_package/phase_inputs/formal.tsv",
    "kimi": "derived_package/inputs/task_slots.tsv",
}
RELEASE_RELPATH = {
    "three_model": "release/G8P1_FORMAL_STAGE_RELEASE.json",
    "kimi": "release/G8P2_FORMAL_RELEASE.json",
}

# Frozen scorer binding (execution card section 2; all asserted in gate step).
SCORER_BINDING = {
    "g1_gold_manifest_sha256": "c424763cd4c38fcaac1b178979efb3f18f2b77039369ab6b8c709eab42dce06e",
    "g2_questions_manifest_sha256": "ae5780e546bb259d0133ba63157ecfe2f3d3071fc37fc2c0050629f7fe575520",
    "g3_gate_sha256": "32c155201a360db8de229e40a9d9cb14bd152993fd0356fd8b0eb8c9001ccaa2",
    "g3_manifest_sha256": "24f1004cab0afca4707bbbd34f26f4b7ead074da723651af73f1fe95ad562e8a",
    "scorer_sha256": "a326eee63258cd0a2706bfd8a1dc6907d6f9fc6aa24b101a7192312c6ed39c61",
    "score_recipe_sha256": "8b79daf906f04e31589ad77bd93998f9a12649575bd4d476447c43028c338392",
    "validators_sha256": "c302164433e37127854eefdf25c44a5939201375873833d51846c3c127083899",
    "teacher_approval_sha256": "1fa908f5ff1caad1f0cb475e820309f0b6431be4e613d51a8548088399c1a5d0",
    "rdkit_version": "2026.03.5",
}

MODEL_ORDER = ["qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3", "kimi/kimi-k3"]

EXPECTED_FAILURES = {
    ("qwen3.8-max", "RESULT_UNKNOWN_HELD"): ["BIOPATH150_084"],
    ("deepseek-v4.1-flash", "LENGTH_EMPTY"): ["BIOPATH150_125"],
    ("ZHIPU/GLM-5.3", "INVALID_JSON"): [
        "BIOPATH150_021", "BIOPATH150_077", "BIOPATH150_092", "BIOPATH150_114",
        "BIOPATH150_119", "BIOPATH150_123", "BIOPATH150_125", "BIOPATH150_127",
        "BIOPATH150_132", "BIOPATH150_138", "BIOPATH150_146"],
    ("kimi/kimi-k3", "RESULT_UNKNOWN_HELD"): ["BIOPATH150_050"],
    ("kimi/kimi-k3", "LENGTH_EMPTY"): ["BIOPATH150_128"],
}
EXPECTED_USABLE = {"qwen3.8-max": 120, "deepseek-v4.1-flash": 120,
                   "ZHIPU/GLM-5.3": 110, "kimi/kimi-k3": 119}

# Kimi fingerprint terminal counts per local audit F2.
EXPECTED_KIMI_FP_TERMINAL = {
    "fpv0_3f6baf1f": 24, "fpv0_c96a51ed": 20, "fpv0_cabe88c9": 30,
    "fpv0_df2f7ec7": 30, "fpv0_e8884bc8": 16,
}

FAILURES = []
CHECKS = [0]


def check(name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILURES.append({"check": name, "detail": str(detail)[:300]})
        print("  [FAIL] %s :: %s" % (name, str(detail)[:200]))
    return ok


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sha256_file_or_none(path):
    return sha256_file(path) if os.path.isfile(path) else None


def read_slot_status(run_root, slot):
    with open(os.path.join(run_root, "slot_status", slot + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def read_matrix(run_root):
    rows = {}
    with open(os.path.join(run_root, "decision", "completion_matrix.tsv"),
              encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rows[row["slot"]] = row
    return rows


def bool_s(v):
    return v == "True"


def classify(status, mrow):
    if status == "DISPATCH_COMMITTED":
        return "RESULT_UNKNOWN_HELD"
    if bool_s(mrow["pass_all"]):
        return "USABLE"
    if bool_s(mrow["finish_length"]) or bool_s(mrow["visible_empty"]):
        return "LENGTH_EMPTY"
    if not bool_s(mrow["json"]):
        return "INVALID_JSON"
    return "OTHER_CONTENT_FAILURE"


def read_dispatch_matrix(pkg_root, pkg_key):
    path = os.path.join(pkg_root, DISPATCH_MATRIX_RELPATH[pkg_key])
    rows = {}
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rows[row["slot_id"]] = row
    return rows, path


def collect_package(pkg_key, pkg_root, run_root, models):
    """Build per-slot records for one return package (read-only)."""
    matrix = read_matrix(run_root)
    dispatch, dispatch_path = read_dispatch_matrix(pkg_root, pkg_key)
    with open(os.path.join(run_root, "run_summary.json"), encoding="utf-8") as fh:
        run_summary = json.load(fh)
    with open(os.path.join(run_root, "decision",
                           "g6r3_formal_status.json" if pkg_key == "three_model"
                           else "g8p2_kimi_status.json"), encoding="utf-8") as fh:
        decision = json.load(fh)
    with open(os.path.join(pkg_root, RELEASE_RELPATH[pkg_key]), encoding="utf-8") as fh:
        release = json.load(fh)

    tar_path = os.path.join(BASE, "03_HPC_Returned_Result_Summaries",
                            SOURCE_IDENTITY[pkg_key]["tar_name"])
    check("%s_tar_sha" % pkg_key, sha256_file(tar_path) == SOURCE_IDENTITY[pkg_key]["sha256"])
    check("%s_tar_bytes" % pkg_key,
          os.path.getsize(tar_path) == SOURCE_IDENTITY[pkg_key]["bytes"])
    audit_path = os.path.join(BASE, "04_Local_Review_Audits",
                              SOURCE_IDENTITY[pkg_key]["audit_md"])
    check("%s_audit_sha" % pkg_key,
          sha256_file(audit_path) == SOURCE_IDENTITY[pkg_key]["audit_sha256"])

    # run_summary.matrix_sha256 binds the INPUT dispatch matrix, not the decision output
    check("%s_matrix_sha_binding" % pkg_key,
          sha256_file(dispatch_path) == run_summary["matrix_sha256"],
          run_summary["matrix_sha256"])
    check("%s_input_package_binding" % pkg_key,
          release.get("input_package_sha256") == INPUT_PACKAGE_SHA,
          release.get("input_package_sha256"))
    check("%s_not_dispatched_zero" % pkg_key, run_summary["not_dispatched_slots"] == [])

    slot_ids = sorted(f[:-5] for f in os.listdir(os.path.join(run_root, "slot_status"))
                      if f.endswith(".json"))
    slots_dir = set(os.listdir(os.path.join(run_root, "slots")))
    check("%s_slot_status_matrix_same_set" % pkg_key, set(slot_ids) == set(matrix))
    check("%s_slot_dirs_subset" % pkg_key, slots_dir <= set(slot_ids),
          sorted(slots_dir - set(slot_ids))[:5])

    records = []
    request_ids = {}
    msg_sha_by_case = {}
    for slot in slot_ids:
        st = read_slot_status(run_root, slot)
        mrow = matrix.get(slot)
        if mrow is None:
            check("%s_matrix_row_%s" % (pkg_key, slot), False, "missing")
            continue
        model = st["model_exact_id"]
        check("%s_model_in_expected_%s" % (pkg_key, slot), model in models, model)
        check("%s_matrix_model_match_%s" % (pkg_key, slot), mrow["model"] == model)
        check("%s_matrix_case_match_%s" % (pkg_key, slot), mrow["case"] == st["case_id"])
        status = st["status"]
        terminal = status == "COMPLETE"
        if not terminal:
            check("%s_held_status_%s" % (pkg_key, slot), status == "DISPATCH_COMMITTED", status)
        if "attempt" in st:
            check("%s_attempt_one_%s" % (pkg_key, slot), st["attempt"] == 1)
        eclass = classify(status, mrow)

        slot_dir = os.path.join(run_root, "slots", slot)
        body_path = os.path.join(slot_dir, "request_body.json")
        raw_path = os.path.join(slot_dir, "raw_stream.sse")
        vis_path = os.path.join(slot_dir, "visible_answer.txt")
        meta_path = os.path.join(slot_dir, "parse_meta.json")

        body_sha = sha256_file_or_none(body_path)
        check("%s_body_sha_present_%s" % (pkg_key, slot), body_sha is not None)
        check("%s_body_sha_match_%s" % (pkg_key, slot),
              body_sha == st["request_body_sha256"],
              "%s vs %s" % (body_sha, st.get("request_body_sha256")))
        drow = dispatch.get(slot)
        check("%s_dispatch_row_%s" % (pkg_key, slot), drow is not None)
        if drow is not None:
            check("%s_dispatch_case_%s" % (pkg_key, slot), drow["case_id"] == st["case_id"])
            check("%s_dispatch_model_%s" % (pkg_key, slot),
                  drow["exact_model_id"] == model)
            check("%s_dispatch_body_sha_%s" % (pkg_key, slot),
                  drow["request_body_sha256"] == st["request_body_sha256"],
                  drow["request_body_sha256"])
            check("%s_dispatch_body_file_sha_%s" % (pkg_key, slot),
                  sha256_file_or_none(os.path.join(pkg_root, "derived_package",
                                                   drow["request_body_file"])) == body_sha)
            msg_sha_by_case.setdefault(st["case_id"], set()).add(drow["messages_sha256"])

        raw_sha = sha256_file_or_none(raw_path)
        vis_sha = sha256_file_or_none(vis_path)
        meta = None
        if os.path.isfile(meta_path):
            with open(meta_path, encoding="utf-8") as fh:
                meta = json.load(fh)
        if terminal:
            check("%s_terminal_has_raw_meta_%s" % (pkg_key, slot),
                  raw_sha is not None and meta is not None)
            check("%s_fixture_live_%s" % (pkg_key, slot),
                  meta is not None and meta["fixture_label"] in
                  ("LIVE_G8P1_THREE_MODEL", "LIVE_G8P2_KIMI_RESPONSE"),
                  meta and meta.get("fixture_label"))
            check("%s_meta_body_sha_%s" % (pkg_key, slot),
                  meta is not None and meta["request_body_sha256"] == st["request_body_sha256"])
            check("%s_meta_request_id_%s" % (pkg_key, slot),
                  meta is not None and meta["provider_request_id"] == st["provider_request_id"])
        else:
            check("%s_held_only_body_%s" % (pkg_key, slot),
                  raw_sha is None and vis_sha is None and meta is None,
                  "held slot must carry only the request body")

        rid = st.get("provider_request_id")
        if rid is not None:
            check("%s_request_id_unique_%s" % (pkg_key, slot),
                  rid not in request_ids, rid)
            request_ids[rid] = slot

        usage = (meta or {}).get("usage") or {}
        cdet = usage.get("completion_tokens_details") or {}
        rec = {
            "source_package": pkg_key,
            "source_tar_sha256": SOURCE_IDENTITY[pkg_key]["sha256"],
            "slot": slot,
            "case_id": st["case_id"],
            "model_exact_id": model,
            "phase": st["phase"],
            "status": status,
            "terminal": terminal,
            "engineering_class": eclass,
            "failure_reason": "" if eclass == "USABLE" else eclass,
            "http_status": st.get("http_status", ""),
            "finish_reason": st.get("finish_reason", ""),
            "json_valid": bool_s(mrow["json"]),
            "object_form": bool_s(mrow["object"]),
            "schema_valid": bool_s(mrow["schema"]),
            "pass_all": bool_s(mrow["pass_all"]),
            "degenerate": bool_s(mrow["degenerate"]),
            "visible_empty": bool_s(mrow["visible_empty"]),
            "finish_length": bool_s(mrow["finish_length"]),
            "repeat": bool_s(mrow["repeat"]),
            "extra_warnings": int(mrow["extra"]),
            "request_body_sha256": st["request_body_sha256"],
            "raw_stream_sha256": raw_sha if raw_sha is not None else "null",
            "visible_answer_sha256": vis_sha if vis_sha is not None else "null",
            "prompt_tokens": usage.get("prompt_tokens", ""),
            "completion_tokens": usage.get("completion_tokens", ""),
            "reasoning_tokens": cdet.get("reasoning_tokens", ""),
            "total_tokens": usage.get("total_tokens", ""),
            "duration_seconds": (meta or {}).get("duration_seconds", ""),
            "provider_request_id": rid if rid is not None else "null",
            "committed_utc": st["committed_utc"],
            # held slots never received a response: no fingerprint exists.
            "system_fingerprint": (st["system_fingerprint"] if terminal
                                   else "NA_NO_RESPONSE"),
            "response_model_field": st.get("response_model_field", ""),
            "reasoning_len": st.get("reasoning_len", ""),
            "visible_len": st.get("visible_len", ""),
            "visible_answer_relpath": (
                os.path.relpath(vis_path, G9).replace(os.sep, "/")
                if vis_sha is not None else "null"),
        }
        records.append(rec)

    # decision-count cross-check
    dec_counts = decision["counts"]
    n_terminal = sum(1 for r in records if r["terminal"])
    n_usable = sum(1 for r in records if r["engineering_class"] == "USABLE")
    n_held = sum(1 for r in records if r["engineering_class"] == "RESULT_UNKNOWN_HELD")
    check("%s_terminal_matches_decision" % pkg_key, n_terminal == dec_counts["terminal"],
          "%s vs %s" % (n_terminal, dec_counts["terminal"]))
    check("%s_usable_matches_decision" % pkg_key, n_usable == dec_counts["usable"],
          "%s vs %s" % (n_usable, dec_counts["usable"]))
    check("%s_slots_matches_decision" % pkg_key, len(records) == dec_counts["slots"])
    for model, pm in decision["per_model"].items():
        mr = [r for r in records if r["model_exact_id"] == model]
        check("%s_%s_slot_count" % (pkg_key, model), len(mr) == pm["slots"] == 121)
        check("%s_%s_usable" % (pkg_key, model),
              sum(1 for r in mr if r["engineering_class"] == "USABLE") == pm["usable"])
        check("%s_%s_held" % (pkg_key, model),
              sum(1 for r in mr if r["engineering_class"] == "RESULT_UNKNOWN_HELD") == pm["held"])
        check("%s_%s_terminal" % (pkg_key, model),
              sum(1 for r in mr if r["terminal"]) == pm["terminal"])
    held_list = run_summary["result_unknown_slots_held"]
    check("%s_held_list_match" % pkg_key,
          sorted(r["slot"] for r in records
                 if r["engineering_class"] == "RESULT_UNKNOWN_HELD") == sorted(held_list),
          held_list)
    return records, decision, run_summary, msg_sha_by_case


def main():
    tm_models = {"qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3"}
    tm_records, tm_decision, tm_summary, tm_msgs = collect_package(
        "three_model", TM_ROOT, TM_RUN, tm_models)
    km_records, km_decision, km_summary, km_msgs = collect_package(
        "kimi", KM_ROOT, KM_RUN, {"kimi/kimi-k3"})
    records = tm_records + km_records

    # same frozen question per case across all four models (messages digest unique)
    merged_msgs = {}
    for d in (tm_msgs, km_msgs):
        for case, shas in d.items():
            merged_msgs.setdefault(case, set()).update(shas)
    check("messages_cover_121_cases", len(merged_msgs) == 121, len(merged_msgs))
    bad = sorted(c for c, s in merged_msgs.items() if len(s) != 1)
    check("messages_sha_unique_per_case_across_models", not bad, bad[:5])

    # ---- canonical case order from frozen G2 ----
    g2_cases = []
    with open(os.path.join(EX, "G2_questions", "main_cases.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                g2_cases.append(json.loads(line)["case_id"])
    check("g2_case_count_121", len(g2_cases) == 121 and len(set(g2_cases)) == 121)

    # ---- hard merge assertions ----
    check("total_rows_484", len(records) == 484, len(records))
    keys = [(r["case_id"], r["model_exact_id"]) for r in records]
    check("unique_keys_484", len(set(keys)) == 484)
    per_model_cases = {}
    for m in MODEL_ORDER:
        cs = sorted({r["case_id"] for r in records if r["model_exact_id"] == m})
        per_model_cases[m] = cs
        check("model_%s_121_cases" % m, len(cs) == 121)
        check("model_%s_case_set_equals_g2" % m, cs == sorted(g2_cases))
    check("case_order_identical_across_models",
          all(per_model_cases[m] == per_model_cases[MODEL_ORDER[0]] for m in MODEL_ORDER))

    # per-model case sequence in dispatch order must match G2 canonical order
    for m in MODEL_ORDER:
        seq = [r["case_id"] for r in records if r["model_exact_id"] == m]
        seq_sorted_by_slot = [c for _, c in sorted(
            (r["slot"], r["case_id"]) for r in records if r["model_exact_id"] == m)]
        check("model_%s_slot_order_is_canonical" % m, seq_sorted_by_slot == g2_cases,
              "first diffs: %s" % [
                  (a, b) for a, b in zip(seq_sorted_by_slot, g2_cases) if a != b][:3])

    n_committed = len(records)
    n_terminal = sum(1 for r in records if r["terminal"])
    n_usable = sum(1 for r in records if r["engineering_class"] == "USABLE")
    n_held = sum(1 for r in records if r["engineering_class"] == "RESULT_UNKNOWN_HELD")
    n_invalid = sum(1 for r in records if r["engineering_class"] == "INVALID_JSON")
    n_lenempty = sum(1 for r in records if r["engineering_class"] == "LENGTH_EMPTY")
    n_other = sum(1 for r in records if r["engineering_class"] == "OTHER_CONTENT_FAILURE")
    content_fail = n_invalid + n_lenempty + n_other
    check("committed_484", n_committed == 484)
    check("terminal_482", n_terminal == 482, n_terminal)
    check("usable_469", n_usable == 469, n_usable)
    check("content_failures_13", content_fail == 13, content_fail)
    check("held_2", n_held == 2, n_held)
    check("invalid_json_11", n_invalid == 11, n_invalid)
    check("length_empty_2", n_lenempty == 2, n_lenempty)
    check("other_content_0", n_other == 0, n_other)
    check("not_dispatched_0",
          tm_summary["not_dispatched_slots"] == [] and km_summary["not_dispatched_slots"] == [])

    for m in MODEL_ORDER:
        mr = [r for r in records if r["model_exact_id"] == m]
        check("usable_%s_%d" % (m.replace("/", "_"), EXPECTED_USABLE[m]),
              sum(1 for r in mr if r["engineering_class"] == "USABLE") == EXPECTED_USABLE[m])
    for (m, eclass), cases in EXPECTED_FAILURES.items():
        got = sorted(r["case_id"] for r in records
                     if r["model_exact_id"] == m and r["engineering_class"] == eclass)
        check("failure_list_%s_%s" % (m.replace("/", "_"), eclass), got == sorted(cases),
              "%s vs %s" % (got, sorted(cases)))

    # usable slots: raw visible must directly json.load into a dict (no repair anywhere)
    n_json_ok = 0
    for r in records:
        if r["engineering_class"] != "USABLE":
            continue
        path = os.path.join(G9, r["visible_answer_relpath"])
        try:
            with open(path, encoding="utf-8") as fh:
                obj = json.load(fh)
            ok = isinstance(obj, dict)
        except ValueError:
            ok = False
        if not check("usable_direct_json_%s_%s" % (r["model_exact_id"], r["case_id"]), ok):
            break
        n_json_ok += 1
    check("usable_json_count_469", n_json_ok == 469, n_json_ok)

    # fingerprints: three models never exposed; kimi exactly five groups
    check("three_model_fingerprint_not_exposed",
          all(r["system_fingerprint"] == "NOT_EXPOSED"
              for r in tm_records if r["terminal"]))
    check("held_fingerprint_na_no_response",
          all(r["system_fingerprint"] == "NA_NO_RESPONSE"
              for r in records if not r["terminal"]))
    fp_term = {}
    fp_usable = {}
    for r in km_records:
        fp = r["system_fingerprint"]
        if r["terminal"]:
            fp_term[fp] = fp_term.get(fp, 0) + 1
        if r["engineering_class"] == "USABLE":
            fp_usable[fp] = fp_usable.get(fp, 0) + 1
    check("kimi_five_fingerprints", set(fp_term) == set(EXPECTED_KIMI_FP_TERMINAL), fp_term)
    for fp, n in EXPECTED_KIMI_FP_TERMINAL.items():
        check("kimi_fp_terminal_%s" % fp, fp_term.get(fp) == n, fp_term.get(fp))
    check("kimi_held_fingerprint_absent",
          all(r["system_fingerprint"] in EXPECTED_KIMI_FP_TERMINAL
              for r in km_records if r["terminal"]))

    # committed_utc well-formed ISO UTC everywhere
    for r in records:
        try:
            datetime.strptime(r["committed_utc"], "%Y-%m-%dT%H:%M:%SZ")
            ok = True
        except ValueError:
            ok = False
        if not check("committed_utc_iso_%s" % r["slot"], ok, r["committed_utc"]):
            break

    if FAILURES:
        print("MERGE INDEX BUILD: FAIL (%d failures of %d checks)" % (len(FAILURES), CHECKS[0]))
        json.dump({"status": "FAIL", "checks": CHECKS[0], "failures": FAILURES},
                  open(os.path.join(G9, "work", "merge_index_failures.json"), "w"),
                  ensure_ascii=False, indent=2)
        return 1

    # ---- write index (case-canonical order, model order fixed) ----
    by_key = {(r["case_id"], r["model_exact_id"]): r for r in records}
    cols = ["source_package", "source_tar_sha256", "slot", "case_id", "model_exact_id",
            "phase", "status", "terminal", "engineering_class", "failure_reason",
            "http_status", "finish_reason", "json_valid", "object_form", "schema_valid",
            "pass_all", "degenerate", "visible_empty", "finish_length", "repeat",
            "extra_warnings", "request_body_sha256", "raw_stream_sha256",
            "visible_answer_sha256", "prompt_tokens", "completion_tokens",
            "reasoning_tokens", "total_tokens", "duration_seconds",
            "provider_request_id", "committed_utc", "system_fingerprint",
            "response_model_field", "reasoning_len", "visible_len",
            "visible_answer_relpath"]
    index_path = os.path.join(G9, "FORMAL_484_SLOT_INDEX.tsv")
    with open(index_path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n",
                           extrasaction="ignore")
        w.writeheader()
        for case in g2_cases:
            for m in MODEL_ORDER:
                row = dict(by_key[(case, m)])
                row["terminal"] = str(row["terminal"])
                for k in ("json_valid", "object_form", "schema_valid", "pass_all",
                          "degenerate", "visible_empty", "finish_length", "repeat"):
                    row[k] = str(row[k])
                w.writerow(row)

    # ---- merge manifest ----
    per_model = {}
    for m in MODEL_ORDER:
        mr = [r for r in records if r["model_exact_id"] == m]
        per_model[m] = {
            "slots": len(mr),
            "committed": len(mr),
            "terminal": sum(1 for r in mr if r["terminal"]),
            "usable": sum(1 for r in mr if r["engineering_class"] == "USABLE"),
            "invalid_json": sorted(r["case_id"] for r in mr
                                   if r["engineering_class"] == "INVALID_JSON"),
            "length_empty": sorted(r["case_id"] for r in mr
                                   if r["engineering_class"] == "LENGTH_EMPTY"),
            "result_unknown_held": sorted(r["case_id"] for r in mr
                                          if r["engineering_class"] == "RESULT_UNKNOWN_HELD"),
        }
    manifest = {
        "task_id": "biosysmodb150_g9_four_model_121_formal_offline_score_20261008",
        "built_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "api_calls": 0,
        "mode": "OFFLINE_READONLY_MERGE",
        "source_identity": SOURCE_IDENTITY,
        "authority_closure": {"path": "00_Authority_Teacher_Plan/" + AUTHORITY_MD,
                              "sha256": AUTHORITY_SHA},
        "scorer_binding": SCORER_BINDING,
        "case_order_source": {
            "path": "G2_questions/main_cases.jsonl",
            "n_cases": 121,
            "sha256": sha256_file(os.path.join(EX, "G2_questions", "main_cases.jsonl")),
        },
        "dispatch_matrices": {
            pkg: {
                "path": "source/%s/%s" % (pkg, DISPATCH_MATRIX_RELPATH[pkg]),
                "sha256": sha256_file(os.path.join(
                    TM_ROOT if pkg == "three_model" else KM_ROOT,
                    DISPATCH_MATRIX_RELPATH[pkg])),
            } for pkg in ("three_model", "kimi")},
        "embedded_input_package_sha256": INPUT_PACKAGE_SHA,
        "messages_sha256_per_case": {
            c: sorted(s)[0] for c, s in sorted(merged_msgs.items())},
        "model_order": MODEL_ORDER,
        "counts": {
            "rows": len(records),
            "committed": n_committed,
            "terminal": n_terminal,
            "usable": n_usable,
            "content_failures": content_fail,
            "invalid_json": n_invalid,
            "length_empty": n_lenempty,
            "result_unknown_held": n_held,
            "not_dispatched": 0,
            "formal_retries": 0,
        },
        "per_model": per_model,
        "kimi_fingerprint_strata": {
            fp: {"terminal": fp_term.get(fp, 0), "usable": fp_usable.get(fp, 0)}
            for fp in sorted(EXPECTED_KIMI_FP_TERMINAL)},
        "ledger_authority": {
            "three_model": {
                "path": "source/three_model/ledger/global_calls.json",
                "sha256": sha256_file(os.path.join(TM_ROOT, "ledger", "global_calls.json")),
                "total_committed": 377, "spent_cny_est": 184.780276,
                "held_reserve_cny": 2.479296, "held_slot": "G8P1-S208",
                "ignored_runtime_files": ["global_calls.json.tmp", "global_calls.json.lock",
                                          "formal_run/.runner.lock"]},
            "kimi": {
                "path": "source/kimi/ledger/kimi_calls.json",
                "sha256": sha256_file(os.path.join(KM_ROOT, "ledger", "kimi_calls.json")),
                "total_committed": 121, "spent_cny_est": 435.86014,
                "held_reserve_cny": 6.7536, "held_slot": "G8P2-K042",
                "ignored_runtime_files": ["kimi_calls.json.tmp", "kimi_calls.json.lock",
                                          "kimi_run/.runner.lock"]},
        },
        "unit_price_cny_per_1M": {
            "qwen3.8-max": {"input": 12, "output": 36},
            "deepseek-v4.1-flash": {"input": 2, "output": 8},
            "ZHIPU/GLM-5.3": {"input": 8, "output": 28},
            "kimi/kimi-k3": {"input": 20, "output": 100},
            "basis": "frozen budget guard configs: three_model release/G8P1_FORMAL_STAGE_RELEASE.json, kimi release/G8P2_FORMAL_RELEASE.json; held settled at worst-case reserve (PROMPT_BOUND*in + 65536*out)/1e6",
        },
        "builder_checks": {"checks": CHECKS[0], "failures": 0},
        "index_file": {
            "path": "FORMAL_484_SLOT_INDEX.tsv",
            "sha256": sha256_file(index_path),
            "rows": 484,
        },
        "no_pilot_smoke_probe_answers": True,
        "no_json_repair": True,
        "no_reasoning_extraction": True,
    }
    man_path = os.path.join(G9, "FORMAL_MERGE_MANIFEST.json")
    with open(man_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print("MERGE INDEX BUILD: PASS (%d checks, 0 failures); rows=484 usable=%d"
          % (CHECKS[0], n_usable))
    return 0


if __name__ == "__main__":
    sys.exit(main())
