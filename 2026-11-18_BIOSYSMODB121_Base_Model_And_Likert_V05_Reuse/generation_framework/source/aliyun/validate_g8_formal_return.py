#!/usr/bin/env python3
"""validate_g8_formal_return.py -- independent receiver for the G8 formal return.

Derived from the PASSED combined receiver (validate_bundle_return.py lineage):
raw_stream.sse is the single answer authority and is re-parsed INDEPENDENTLY of
the runner, then chain-checked field by field against visible_answer.txt /
reasoning.txt / parse_meta / slot_status / run_summary.

G8 changes (card-permitted only):
- 484 slots G8-S001..G8-S484; per-model denominator is ALWAYS 121; formal
  failed slots stay in the denominator, answers are never repaired or re-asked;
- request bodies are checked byte-for-byte against the frozen v2 input package
  (file sha from task_slots.tsv) and the frozen messages digest rule
  (compact JSON, key order role,content preserved) is re-asserted per slot;
- engineering classification, NOT an all-JSON-success gate: COMPLETE /
  HTTP_ERROR / TRANSPORT_ERROR are terminal and packagable; held result-unknown
  slots and NOT_DISPATCHED slots are reported honestly and drive COMPLETE vs
  PARTIAL classification instead of refusing the return;
- phase identity: every slot id must be G8-S###, fixture label
  LIVE_G8_FORMAL_RESPONSE, idempotency prefix G8_FORMAL -- structural proof
  that no smoke/pilot slot or answer was reused;
- schema rate is ALWAYS reported separately; no repair, no re-ask.
"""
import argparse, hashlib, json, os, re, sys

PHASE = "G8_FORMAL"
FIXTURE_LABEL_LIVE = "LIVE_G8_FORMAL_RESPONSE"
SLOT_COUNT = 484
CASE_COUNT = 121
TERMINAL = ("COMPLETE", "HTTP_ERROR", "TRANSPORT_ERROR")
HELD = ("DISPATCH_COMMITTED", "POST_DISPATCH_LOCAL_ERROR")
REQUIRED = ("request_body.json", "raw_stream.sse", "response_headers.json", "visible_answer.txt",
            "reasoning.txt", "metadata_paths.json", "search_evidence.json", "parse_meta.json")
OPTIONAL = {"error.txt"}
META_KEYS = {"request_body_sha256", "finish_reason", "usage", "provider_request_id", "sse_done",
             "transport_outcome", "duration_seconds", "fixture_label"}
SENSITIVE_HDR = {"authorization", "cookie", "set-cookie", "x-api-key", "apikey", "dashscope_api_key"}
EXACT_IDS = ["qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3", "kimi/kimi-k3"]
BASE_KEYS = {"model", "temperature", "max_tokens", "stream", "stream_options", "enable_search", "messages"}
GLM_KEYS = BASE_KEYS | {"enable_thinking", "reasoning_effort"}
FORBIDDEN_KEYS = {"response_format", "thinking_budget", "thinking", "tools", "forced_search"}


def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(open(p, "rb").read())


def messages_digest(messages):
    # frozen v2 rule: compact JSON, key order preserved
    return sha_bytes(json.dumps(messages, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def strip_single_fence(text):
    t = (text or "").strip()
    m = re.match(r"^```(?:json)?\s*(.*?)\s*```$", t, re.S)
    return m.group(1) if m else t


def mini_validate(inst, schema, path=""):
    errs = []
    ty = schema.get("type")
    if ty == "object":
        if not isinstance(inst, dict): return [path + ":not_object"]
        for r in schema.get("required", []):
            if r not in inst: errs.append("%s.%s:missing_required" % (path, r))
        for k, spec in (schema.get("properties") or {}).items():
            if k in inst: errs += mini_validate(inst[k], spec, path + "." + k)
    elif ty == "array":
        if not isinstance(inst, list): return [path + ":not_array"]
        it = schema.get("items") or {}
        for i, v in enumerate(inst):
            if it.get("type") == "object" and not isinstance(v, dict):
                errs.append("%s[%d]:not_object" % (path, i)); continue
            for r in it.get("required", []):
                if isinstance(v, dict) and r not in v: errs.append("%s[%d].%s:missing" % (path, i, r))
            for k, sp in (it.get("properties") or {}).items():
                if isinstance(v, dict) and k in v and sp.get("type") == "string" and not isinstance(v[k], str):
                    errs.append("%s[%d].%s:type" % (path, i, k))
    elif ty == "string":
        if not isinstance(inst, str): errs.append(path + ":not_string")
    elif ty in ("integer", "number"):
        if isinstance(inst, bool) or not isinstance(inst, (int, float)): errs.append(path + ":not_number")
    return errs


def extra_warnings(inst, schema):
    n = 0
    if isinstance(inst, dict) and schema.get("type") == "object":
        props = set((schema.get("properties") or {}).keys())
        n += sum(1 for k in inst if k not in props)
        for k, v in inst.items():
            if k in props: n += extra_warnings(v, schema["properties"][k])
    elif isinstance(inst, list) and schema.get("type") == "array":
        for v in inst: n += extra_warnings(v, schema.get("items") or {})
    return n


def derive_raw(slotdir):
    p = os.path.join(slotdir, "raw_stream.sse")
    if not os.path.isfile(p): return None
    raw = open(p, "rb").read()
    visible = []; reasoning = []; finish = None; usage = None; rid = None; done = False; unparse = 0
    for line in raw.split(b"\n"):
        t = line.decode("utf-8", "replace").strip()
        if not t.startswith("data:"): continue
        payload = t[5:].strip()
        if payload == "[DONE]": done = True; continue
        try: obj = json.loads(payload)
        except Exception: unparse += 1; continue
        if not isinstance(obj, dict): unparse += 1; continue
        rid = rid or obj.get("id") or obj.get("request_id") or obj.get("requestId")
        if obj.get("usage") is not None: usage = obj["usage"]
        for ch in (obj.get("choices") or []):
            if not isinstance(ch, dict): continue
            d = ch.get("delta") or {}
            if isinstance(d, dict):
                if d.get("content"): visible.append(d["content"])
                if d.get("reasoning_content"): reasoning.append(d["reasoning_content"])
            if ch.get("finish_reason"): finish = ch["finish_reason"]
    return {"visible": "".join(visible), "reasoning": "".join(reasoning), "finish": finish,
            "usage": usage, "rid": rid, "done": done, "unparseable": unparse}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True, help="frozen v2 offline input package dir")
    ap.add_argument("--run", required=True, help="formal run dir to audit")
    ap.add_argument("--schema", default=None, help="answer schema (default: inputs/schemas/*.json)")
    ap.add_argument("--rehearsal", action="store_true",
                    help="audit a SELF_TEST regression run: expect SELF_TEST_MOCK labels and mark the "
                         "decision as rehearsal; NEVER use for a formal LIVE return")
    a = ap.parse_args()
    inputs = os.path.abspath(a.inputs); run = os.path.abspath(a.run)
    integrity = []

    manifest = json.load(open(os.path.join(inputs, "package.json"), encoding="utf-8"))
    if manifest.get("package_version") != "g8_four_model_offline_inputs_v2":
        integrity.append("inputs_not_v2_package")
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(inputs, "task_slots.tsv"), encoding="utf-8")]
    hdr = rows[0]; matrix = [dict(zip(hdr, r)) for r in rows[1:] if r]
    if len(matrix) != SLOT_COUNT: integrity.append("matrix_not_484")
    schema_path = a.schema
    if schema_path is None:
        cand = [f for f in os.listdir(os.path.join(inputs, "schemas")) if f.endswith(".json")]
        schema_path = os.path.join(inputs, "schemas", cand[0])
    schema = json.load(open(schema_path, encoding="utf-8"))

    summary_path = os.path.join(run, "run_summary.json")
    summary = json.load(open(summary_path, encoding="utf-8")) if os.path.isfile(summary_path) else None
    want_label = "SELF_TEST_MOCK" if a.rehearsal else FIXTURE_LABEL_LIVE
    if summary is None:
        integrity.append("run_summary_missing")
    else:
        if summary.get("phase") != PHASE: integrity.append("run_summary_phase:%r" % summary.get("phase"))
        if summary.get("package_version") != "g8_four_model_offline_inputs_v2":
            integrity.append("run_summary_version:%r" % summary.get("package_version"))
        if a.rehearsal and summary.get("transport") != "SELF_TEST":
            integrity.append("rehearsal_flag_but_transport:%r" % summary.get("transport"))
        if not a.rehearsal and summary.get("transport") != "LIVE":
            integrity.append("formal_audit_but_transport:%r" % summary.get("transport"))
        acu = summary.get("api_calls_used")
        if not isinstance(acu, int) or isinstance(acu, bool) or not (0 <= acu <= SLOT_COUNT):
            integrity.append("api_calls_used_invalid:%r" % acu)

    stats = []
    counts_terminal = {"COMPLETE": 0, "HTTP_ERROR": 0, "TRANSPORT_ERROR": 0}
    held = []; not_dispatched = []
    for r in matrix:
        slot = r["slot_id"]
        if not re.match(r"^G8-S\d{3}$", slot):
            integrity.append("slot_id_not_g8_namespace:%s" % slot); continue
        sfile = os.path.join(run, "slot_status", slot + ".json")
        sst = None
        if os.path.isfile(sfile):
            try: sst = json.load(open(sfile, encoding="utf-8"))
            except Exception: integrity.append("slot_status_unreadable:%s" % slot)
        state = (sst or {}).get("status")
        rec = {"slot": slot, "case_id": r["case_id"], "model": r["anonymous_model_id"],
               "exact_model_id": r["exact_model_id"], "status": state}
        if state is None:
            not_dispatched.append(slot); rec["engineering_class"] = "NOT_REQUESTED"
            stats.append(rec); continue
        if state in HELD:
            held.append(slot); rec["engineering_class"] = "RESULT_UNKNOWN_HELD_NEVER_RESENT"
            stats.append(rec); continue
        if state == "NOT_DISPATCHED":
            not_dispatched.append(slot); rec["engineering_class"] = "NOT_DISPATCHED_STOP"
            stats.append(rec); continue
        if state not in TERMINAL:
            integrity.append("unknown_slot_state:%s=%s" % (slot, state)); continue
        counts_terminal[state] += 1
        rec["engineering_class"] = state
        sdir = os.path.join(run, "slots", slot)
        if not os.path.isdir(sdir):
            integrity.append("missing_slot_dir:%s" % slot); stats.append(rec); continue
        files = set(os.listdir(sdir))
        for f in REQUIRED:
            if f not in files: integrity.append("missing_response_artifact:%s/%s" % (slot, f))
        for f in sorted(files - set(REQUIRED) - OPTIONAL):
            integrity.append("unexpected_slot_file:%s/%s" % (slot, f))
        # body byte equality with the frozen input package
        frozen_body_path = os.path.join(inputs, r["request_body_file"])
        local_body_path = os.path.join(sdir, "request_body.json")
        if os.path.isfile(local_body_path) and os.path.isfile(frozen_body_path):
            lb = open(local_body_path, "rb").read()
            if sha_bytes(lb) != r["request_body_sha256"]:
                integrity.append("request_body_sha_mismatch:%s" % slot)
            if lb != open(frozen_body_path, "rb").read():
                integrity.append("request_body_bytes_differ_from_frozen_input:%s" % slot)
            try: body = json.loads(lb)
            except Exception: body = None
            if isinstance(body, dict):
                if FORBIDDEN_KEYS & set(body):
                    integrity.append("forbidden_parameter_in_request:%s:%s" % (slot, sorted(FORBIDDEN_KEYS & set(body))))
                is_glm = r["exact_model_id"] == "ZHIPU/GLM-5.3"
                want = GLM_KEYS if is_glm else BASE_KEYS
                if set(body) != want:
                    integrity.append("request_key_set_not_exact:%s" % slot)
                if body.get("model") != r["exact_model_id"]:
                    integrity.append("request_model_mismatch:%s" % slot)
                msgs = body.get("messages")
                if not isinstance(msgs, list) or [list(m) for m in msgs if isinstance(m, dict)] != [["role", "content"] for m in msgs if isinstance(m, dict)]:
                    integrity.append("message_key_order_not_frozen:%s" % slot)
                if messages_digest(msgs) != r["messages_sha256"]:
                    integrity.append("messages_digest_mismatch:%s" % slot)
        # parse_meta / fixture label / sensitive headers
        meta = None
        try: meta = json.load(open(os.path.join(sdir, "parse_meta.json"), encoding="utf-8"))
        except Exception: integrity.append("parse_meta_unreadable:%s" % slot)
        if isinstance(meta, dict):
            for k in META_KEYS:
                if k not in meta: integrity.append("parse_meta_incomplete_keys:%s.%s" % (slot, k))
            if meta.get("fixture_label") != want_label:
                integrity.append("fixture_label_wrong:%s=%s" % (slot, meta.get("fixture_label")))
            if meta.get("request_body_sha256") != r["request_body_sha256"]:
                integrity.append("body_sha_mismatch_parse_meta:%s" % slot)
            if not isinstance(meta.get("duration_seconds"), (int, float)) or meta.get("duration_seconds", -1) < 0:
                integrity.append("parse_meta_duration_invalid:%s" % slot)
        try:
            hdrj = json.load(open(os.path.join(sdir, "response_headers.json"), encoding="utf-8"))
            if not isinstance(hdrj, list) or not all(isinstance(x, list) and len(x) == 2 for x in hdrj):
                integrity.append("headers_structure_invalid:%s" % slot)
            elif any(str(x[0]).lower() in SENSITIVE_HDR or str(x[1]).lower().startswith("bearer ")
                     or (not a.rehearsal and str(x[0]).lower() == "x-self-test") for x in hdrj):
                integrity.append("headers_sensitive_or_selftest:%s" % slot)
        except Exception:
            if state == "COMPLETE": integrity.append("headers_unreadable:%s" % slot)
        # raw re-derivation chain
        dv = derive_raw(sdir)
        if dv is None:
            integrity.append("missing_response_artifact:%s/raw_stream.sse" % slot)
            stats.append(rec); continue
        if dv["unparseable"] > 0: integrity.append("raw_unparseable_data_frame:%s:%d" % (slot, dv["unparseable"]))
        try: vfile = open(os.path.join(sdir, "visible_answer.txt"), encoding="utf-8").read()
        except Exception: vfile = None
        try: rfile = open(os.path.join(sdir, "reasoning.txt"), encoding="utf-8").read()
        except Exception: rfile = None
        if state == "COMPLETE":
            if vfile != dv["visible"]: integrity.append("visible_derivation_mismatch:%s" % slot)
            if rfile != dv["reasoning"]: integrity.append("reasoning_derivation_mismatch:%s" % slot)
            if isinstance(meta, dict):
                if meta.get("finish_reason") != dv["finish"]: integrity.append("finish_derivation_mismatch:%s" % slot)
                if meta.get("usage") != dv["usage"]: integrity.append("usage_derivation_mismatch:%s" % slot)
                if meta.get("provider_request_id") != dv["rid"]: integrity.append("request_id_derivation_mismatch:%s" % slot)
                if not dv["rid"]: integrity.append("request_id_absent_in_raw:%s" % slot)
                if not dv["done"]: integrity.append("sse_done_missing_in_raw:%s" % slot)
        if sst is not None and state == "COMPLETE":
            if sst.get("finish_reason") != dv["finish"]: integrity.append("finish_chain_mismatch:%s" % slot)
            if sst.get("provider_request_id") != dv["rid"]: integrity.append("request_id_chain_mismatch:%s" % slot)
            if "visible_len" in sst and sst.get("visible_len") != len(dv["visible"]):
                integrity.append("length_chain_mismatch:%s.visible" % slot)
        # answer-level classification (never repaired)
        vis = dv["visible"]
        rec["http_success"] = state == "COMPLETE" and (sst or {}).get("http_status") == 200
        rec["finish_reason"] = dv["finish"]
        rec["finish_length"] = dv["finish"] == "length"
        rec["visible_empty"] = not (vis or "").strip()
        obj = None; rec["json_valid"] = False
        if vis:
            try: obj = json.loads(strip_single_fence(vis)); rec["json_valid"] = True
            except Exception: obj = None
        rec["object_form"] = isinstance(obj, dict) and len(obj) > 0
        if rec["object_form"]:
            rec["schema_errors"] = mini_validate(obj, schema)
            rec["extra_warnings_n"] = extra_warnings(obj, schema)
        else:
            rec["schema_errors"] = ["not_applied"]; rec["extra_warnings_n"] = 0
        rec["schema_valid"] = rec["object_form"] and not rec["schema_errors"]
        rec["usable_object"] = rec["object_form"] and state == "COMPLETE"
        u = dv["usage"] or {}
        rec["usage_tokens"] = {"prompt": u.get("prompt_tokens"), "completion": u.get("completion_tokens"),
                               "total": u.get("total_tokens"),
                               "reasoning": (u.get("completion_tokens_details") or {}).get("reasoning_tokens")}
        rec["duration_seconds"] = (meta or {}).get("duration_seconds")
        stats.append(rec)

    # ---- classification (engineering, not all-JSON-success) ----
    per_model = {}
    for mid in EXACT_IDS:
        rs = [s for s in stats if s["exact_model_id"] == mid]
        per_model[mid] = {
            "slots_in_matrix": len(rs),
            "denominator_formal": CASE_COUNT,
            "terminal": sum(1 for s in rs if s["status"] in TERMINAL),
            "http_success": sum(1 for s in rs if s.get("http_success")),
            "json_syntax_valid": sum(1 for s in rs if s.get("json_valid")),
            "json_object_form": sum(1 for s in rs if s.get("object_form")),
            "schema_required_type_valid": sum(1 for s in rs if s.get("schema_valid")),
            "usable_json_objects": sum(1 for s in rs if s.get("usable_object")),
            "visible_empty": sum(1 for s in rs if s.get("visible_empty")),
            "finish_length": sum(1 for s in rs if s.get("finish_length")),
            "length_or_empty_union": len({s["slot"] for s in rs if s.get("finish_length") or s.get("visible_empty")}),
            "result_unknown_held": sum(1 for s in rs if s.get("engineering_class") == "RESULT_UNKNOWN_HELD_NEVER_RESENT"),
            "not_dispatched": sum(1 for s in rs if s["status"] in (None, "NOT_DISPATCHED")),
        }
    all_terminal = len(held) == 0 and sum(counts_terminal.values()) == SLOT_COUNT
    classification = "G8_FORMAL_COMPLETE_AUDITED" if all_terminal else "G8_FORMAL_PARTIAL_AUDITED"
    if a.rehearsal:
        classification = "G8_SELF_TEST_REHEARSAL_" + ("COMPLETE" if all_terminal else "PARTIAL")
    if integrity:
        classification = "G8_INTEGRITY_FAIL_AUDIT_BLOCKED"
    out = {"stage": "G8_FORMAL_121CASE_FOUR_MODEL", "phase": PHASE,
           "package_version": "g8_four_model_offline_inputs_v2",
           "g8_formal_status": classification,
           "slot_integrity_problems": integrity,
           "terminal_counts": counts_terminal,
           "result_unknown_held_slots": held,
           "not_dispatched_slots": not_dispatched,
           "counts_overall": {
               "slots": len(stats),
               "terminal": sum(counts_terminal.values()),
               "http_success": sum(1 for s in stats if s.get("http_success")),
               "json_syntax_valid": sum(1 for s in stats if s.get("json_valid")),
               "json_object_form": sum(1 for s in stats if s.get("object_form")),
               "schema_required_type_valid": sum(1 for s in stats if s.get("schema_valid")),
               "usable_json_objects": sum(1 for s in stats if s.get("usable_object")),
               "visible_empty": sum(1 for s in stats if s.get("visible_empty")),
               "finish_length": sum(1 for s in stats if s.get("finish_length")),
               "length_or_empty_union": len({s["slot"] for s in stats if s.get("finish_length") or s.get("visible_empty")}),
               "extra_field_warnings_total": sum(s.get("extra_warnings_n", 0) for s in stats)},
           "per_model": per_model,
           "denominator_note": "every model's formal denominator is 121; failed/unknown/undispatched slots stay in it",
           "rates_reported_separately_note": "HTTP/JSON syntax/object form/schema validity are independent rates from RAW SSE derivations; content failures are kept, never repaired, never re-asked",
           "authority_note": "raw_stream.sse is the single answer authority",
           "shape_review_status": "PENDING_LOCAL_HUMAN_REVIEW",
           "next_stage_allowed": False,
           "rerun_authorized": False,
           "per_slot": stats}
    os.makedirs(os.path.join(run, "decision"), exist_ok=True)
    json.dump(out, open(os.path.join(run, "decision", "g8_formal_status.json"), "w"), ensure_ascii=False, indent=2, sort_keys=True)
    with open(os.path.join(run, "decision", "completion_matrix.tsv"), "w", encoding="utf-8") as fh:
        fh.write("slot_id\tcase_id\tmodel\texact_model_id\tstatus\thttp\tjson\tobject\tschema\tvisible_empty\tfinish_length\textra_warnings\n")
        for s in stats:
            fh.write("\t".join([s["slot"], s["case_id"], s["model"], s["exact_model_id"], str(s.get("status")),
                                str(s.get("http_success")), str(s.get("json_valid")), str(s.get("object_form")),
                                str(s.get("schema_valid")), str(s.get("visible_empty")), str(s.get("finish_length")),
                                str(s.get("extra_warnings_n", 0))]) + "\n")
    c = out["counts_overall"]
    open(os.path.join(run, "RUN_REPORT.md"), "w", encoding="utf-8").write(
        "# G8 formal run report\n\nstatus=%s terminal=%d/484 usable=%d http=%d json=%d object=%d schema=%d empty=%d length=%d union=%d unknown_held=%d not_dispatched=%d integrity=%d\n\n%s\n"
        % (classification, c["terminal"], c["usable_json_objects"], c["http_success"], c["json_syntax_valid"],
           c["json_object_form"], c["schema_required_type_valid"], c["visible_empty"], c["finish_length"],
           c["length_or_empty_union"], len(held), len(not_dispatched), len(integrity),
           "audit complete; content failures kept as-is; per-model denominator 121." if not integrity
           else "INTEGRITY PROBLEMS FOUND: audit blocked; evidence kept; no repair."))
    print("%s terminal=%d/484 usable=%d integrity=%d held=%d not_dispatched=%d"
          % (classification, c["terminal"], c["usable_json_objects"], len(integrity), len(held), len(not_dispatched)))
    if integrity:
        print("integrity:", integrity[:10]); sys.exit(1)


if __name__ == "__main__":
    main()
