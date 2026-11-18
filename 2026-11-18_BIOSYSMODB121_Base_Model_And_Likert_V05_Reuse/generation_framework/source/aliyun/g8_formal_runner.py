#!/usr/bin/env python3
"""g8_formal_runner.py -- G8 formal 121-case x four-model runner (484 slots).

Narrow derivation from the PASSED combined lineage (R2 V1.2 runner, which the
G5-R8/G6-R1 combined bundle runner itself narrowly derived from). Inherited
unchanged: commit-before-transport at-most-once dispatch, raw SSE verbatim
preservation, cumulative cross-process accounting, per-model concurrency 1 with
total concurrency 4, sanitized headers, zero auto retry, answers never repaired
or re-asked.

Card-permitted changes only: phase G8_FORMAL; 121 cases / 484 slots G8-S001..
G8-S484 taken verbatim from the v2 offline input package (request bodies are
used byte-for-byte as packaged, never rebuilt); budget guard with per-request
worst-case reservation and hard-cap stop; checkpoint every 20 new terminal
slots; persistent-service-failure circuit breaker; partial-return capable;
cross-process single-instance flock; resume dispatches only NOT_DISPATCHED
slots and NEVER re-sends committed ones (result-unknown slots stay held as
RESULT_UNKNOWN, counted in the ledger, not treated as un-requested).

LIVE dispatch is refused unless an authorization file (READINESS.json) carries
release_allowed=true, an approved budget with a numeric hard cap, and the exact
sha256 of the v2 input package tar. Self-test mode is labeled SELF_TEST and can
never be packaged as a formal return.
"""
import argparse, fcntl, hashlib, json, os, re, stat, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

TERMINAL = ("COMPLETE", "HTTP_ERROR", "TRANSPORT_ERROR")
COMMITTED_STATES = ("DISPATCH_COMMITTED", "POST_DISPATCH_LOCAL_ERROR", "COMPLETE", "HTTP_ERROR", "TRANSPORT_ERROR")
PHASE = "G8_FORMAL"
STAGE = "G8_FORMAL_121CASE_FOUR_MODEL"
FIXTURE_LABEL_LIVE = "LIVE_G8_FORMAL_RESPONSE"
EXPECTED_INPUT_VERSION = "g8_four_model_offline_inputs_v2"
SLOT_COUNT = 484
CASE_COUNT = 121
MODEL_COUNT = 4
MAX_TOKENS = 65536
CHECKPOINT_EVERY = 20
SERVICE_FAILURE_RUN_LIMIT = 5  # consecutive cross-model HTTP/transport failures -> stop new dispatch
SERVICE_FAILURE_HTTP = {401, 403, 429} | set(range(500, 600))


def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(open(p, "rb").read())


def _atomic_write(path, obj):
    tmp = "%s.tmp.%d" % (path, os.getpid())
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)


# ---------------- evidence parsing (inherited V1.6/V2 rules) ----------------
URL_RE = re.compile(r"https?://\S+", re.I)

def flatten(obj, prefix="", out=None, depth=0):
    if out is None: out = {}
    if depth > 12: return out
    if isinstance(obj, dict):
        if not obj: out[prefix + "(empty_dict)"] = True
        for k, v in obj.items(): flatten(v, f"{prefix}.{k}" if prefix else str(k), out, depth + 1)
    elif isinstance(obj, list):
        if not obj: out[prefix + "(empty_list)"] = True
        for i, v in enumerate(obj[:50]): flatten(v, f"{prefix}[{i}]", out, depth + 1)
    else:
        out[prefix] = obj if not isinstance(obj, dict) else str(obj)[:500]
    return out

def search_evidence(paths):
    hits = []; detail = {}
    def num(v):
        try: return float(v)
        except Exception: return None
    sres = [k for k in paths if re.match(r"search_info\.search_results(\[|$|\.)", k)]
    urls_in = [k for k in sres if isinstance(paths[k], str) and URL_RE.search(paths[k])]
    if urls_in: hits.append("R1_search_info_urls")
    detail["R1"] = {"keys": len(sres), "with_urls": len(urls_in)}
    for k, v in paths.items():
        if re.search(r"usage\.plugins\.search\.count$", k) and (num(v) or 0) > 0:
            hits.append("R2_usage_plugins_search_count"); detail["R2"] = v; break
    for k, v in paths.items():
        if re.search(r"usage\.x_tools\.web_search\.count$", k) and (num(v) or 0) > 0:
            hits.append("R3_usage_x_tools_web_search_count"); detail["R3"] = v; break
    for k, v in paths.items():
        if (re.search(r"(web_search_call|action\.sources)", k) or k.endswith("tool_calls[*].type")) \
           and isinstance(v, str) and URL_RE.search(v):
            hits.append("R4_web_search_action_sources"); detail["R4"] = k; break
    for k, v in paths.items():
        if re.search(r"tool_calls", k) and isinstance(v, (str, int, float, list)) and re.search(r"search|web", str(v), re.I) \
           and str(v).strip() not in ("", "None", "0"):
            hits.append("R5_tool_calls_search"); detail["R5"] = k; break
    return hits, bool(hits), detail

def parse_stream(raw_lines):
    visible = []; reasoning = []; finish = None; usage = None; rid = None
    model_fp = None; sys_fp = "NOT_EXPOSED"; done = False
    frames = []; unknown = set(); all_paths = {}
    KNOWN_TOP = {"choices", "object", "created", "model", "id", "usage", "system_fingerprint", "request_id", "requestId"}
    KNOWN_DELTA = {"content", "reasoning_content", "role", "function_call", "tool_calls"}
    for b in raw_lines:
        line = b.decode("utf-8", "replace").strip()
        if not line.startswith("data:"): continue
        payload = line[5:].strip()
        if payload == "[DONE]": done = True; continue
        try: obj = json.loads(payload)
        except Exception: unknown.add("UNPARSEABLE_DATA_FRAME"); continue
        frames.append(obj)
        for k in obj.keys():
            if k not in KNOWN_TOP: unknown.add(k)
        rid = rid or obj.get("id") or obj.get("request_id") or obj.get("requestId")
        model_fp = model_fp or obj.get("model")
        if obj.get("system_fingerprint"): sys_fp = obj["system_fingerprint"]
        if obj.get("usage"): usage = obj["usage"]
        for ch in (obj.get("choices") or []):
            d = ch.get("delta") or {}
            for k in d.keys():
                if k not in KNOWN_DELTA: unknown.add("delta." + k)
            if d.get("content"): visible.append(d["content"])
            if d.get("reasoning_content"): reasoning.append(d["reasoning_content"])
            if ch.get("finish_reason"): finish = ch["finish_reason"]
    for i, fr in enumerate(frames):
        for p, v in flatten(fr).items(): all_paths.setdefault(f"frame[{i}].{p}", v)
    hits, has, detail = search_evidence({k.split(".", 1)[1]: v for k, v in all_paths.items()})
    return dict(visible="".join(visible), reasoning="".join(reasoning), finish=finish, usage=usage,
                rid=rid, done=done, unknown=sorted(unknown), paths=all_paths,
                evidence_rules=hits, evidence=has, evidence_detail=detail,
                response_model_field=model_fp or "NOT_EXPOSED", system_fingerprint=sys_fp)


# ---------------- transports ----------------
class HttpTransport:
    name = "LIVE"
    def __init__(self, key, endpoint): self.key = key; self.endpoint = endpoint
    def stream(self, body, timeout=1800, slot=None):
        import urllib.request, urllib.error
        req = urllib.request.Request(self.endpoint,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": "Bearer " + self.key,
                     "Accept": "text/event-stream"}, method="POST")
        raw = []
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                for line in r: raw.append(line)
        except urllib.error.HTTPError as e:
            return "HTTP_ERROR", e.code, (e.read() or b""), raw, [(k, v) for k, v in e.headers.items()]
        except Exception as e:
            return "TRANSPORT_ERROR", None, str(e).encode("utf-8"), raw, []
        return "OK", 200, b"", raw, []

class MockTransport:
    """Self-test transport. Per-slot side-effect files enable offline regression:
    <slot>.http_error (content = HTTP code) -> HTTP_ERROR terminal;
    <slot>.transport_error -> TRANSPORT_ERROR terminal;
    <slot>.local_error -> exception inside stream (POST_DISPATCH_LOCAL_ERROR)."""
    name = "SELF_TEST"
    def __init__(self, fixtures_dir, fixture="default.sse"): self.d = fixtures_dir; self.f = fixture
    def stream(self, body, timeout=1800, slot=None):
        if slot:
            he = os.path.join(self.d, slot + ".http_error")
            if os.path.exists(he):
                try: code = int(open(he, encoding="utf-8").read().strip() or "429")
                except ValueError: code = 429
                eb = os.path.join(self.d, slot + ".errbody")
                err = open(eb, "rb").read() if os.path.exists(eb) else b'{"error":"mock"}'
                return "HTTP_ERROR", code, err, [], []
            if os.path.exists(os.path.join(self.d, slot + ".transport_error")):
                return "TRANSPORT_ERROR", None, b"mock transport failure", [], []
            if os.path.exists(os.path.join(self.d, slot + ".local_error")):
                raise RuntimeError("mock local error injected for %s" % slot)
        f = os.path.join(self.d, slot + ".sse") if slot else None
        if not f or not os.path.exists(f): f = os.path.join(self.d, self.f)
        lines = [l.encode() + b"\n" for l in open(f, encoding="utf-8").read().splitlines()]
        return "OK", 200, b"", lines, [("x-self-test", "1")]


# ---------------- input package ----------------
class InputPackage:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        bad = self.verify_sums()
        if bad: raise SystemExit("input package integrity FAILED: %s" % bad[:5])
        self.manifest = json.load(open(os.path.join(self.root, "package.json"), encoding="utf-8"))
        if self.manifest.get("package_version") != EXPECTED_INPUT_VERSION:
            raise SystemExit("input package_version must be %s, got %r" % (EXPECTED_INPUT_VERSION, self.manifest.get("package_version")))
        if self.manifest.get("case_count") != CASE_COUNT or self.manifest.get("model_count") != MODEL_COUNT or self.manifest.get("slot_count") != SLOT_COUNT:
            raise SystemExit("input package shape wrong (need 121/4/484)")
        if self.manifest.get("contains_gold_tables") is not False or self.manifest.get("contains_credentials") is not False:
            raise SystemExit("input package must not contain gold/credentials")
        rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(self.root, "task_slots.tsv"), encoding="utf-8")]
        hdr = rows[0]; self.slots = [dict(zip(hdr, r)) for r in rows[1:] if r]
        if len(self.slots) != SLOT_COUNT:
            raise SystemExit("task_slots.tsv must carry exactly 484 rows")
        expected_ids = ["G8-S%03d" % i for i in range(1, SLOT_COUNT + 1)]
        if [s["slot_id"] for s in self.slots] != expected_ids:
            raise SystemExit("slot id set/order wrong")
        if any(s["status"] != "NOT_DISPATCHED" or s["phase"] != "G8" for s in self.slots):
            raise SystemExit("input matrix must be all G8/NOT_DISPATCHED")
        for s in self.slots:
            bp = os.path.join(self.root, s["request_body_file"])
            if not os.path.isfile(bp): raise SystemExit("missing body file: %s" % s["request_body_file"])
            if sha_file(bp) != s["request_body_sha256"]: raise SystemExit("body sha mismatch: %s" % s["slot_id"])
            s["body_path"] = bp
            s["body_bytes"] = open(bp, "rb").read()

    def verify_sums(self):
        bad = []
        for line in open(os.path.join(self.root, "SHA256SUMS"), encoding="utf-8"):
            if not line.strip(): continue
            dg, rel = line.rstrip("\n").split("  ", 1)
            p = os.path.join(self.root, rel)
            if not os.path.exists(p) or sha_file(p) != dg: bad.append(rel)
        return bad


# ---------------- budget guard ----------------
class BudgetGuard:
    """Worst-case reservation per dispatch; hard-cap stop; spend from real usage."""
    def __init__(self, cfg, enabled=True):
        self.enabled = enabled
        self.lock = threading.Lock()
        self.stopped = False
        self.stop_reason = None
        self.reserved = 0.0
        self.spent = 0.0
        self.reservations = {}
        if not enabled:
            return
        self.hard_cap = float(cfg["hard_cap_cny"])
        self.prices = {m: (float(p["input"]), float(p["output"])) for m, p in cfg["unit_price_cny_per_1M"].items()}
        self.prompt_bound = int(cfg.get("prompt_token_bound", 7000))
        if cfg.get("approved") is not True:
            raise SystemExit("budget guard requires approved=true in the authorization budget block")

    def reserve_cost(self, exact_model_id):
        pin, pout = self.prices[exact_model_id]
        return (self.prompt_bound * pin + MAX_TOKENS * pout) / 1e6

    def try_reserve(self, slot, exact_model_id):
        if not self.enabled: return True
        cost = self.reserve_cost(exact_model_id)
        with self.lock:
            if self.stopped: return False
            if self.spent + self.reserved + cost > self.hard_cap:
                self.stopped = True
                self.stop_reason = "BUDGET_HARD_CAP_REACHED"
                return False
            self.reservations[slot] = cost
            self.reserved += cost
            return True

    def settle(self, slot, usage, exact_model_id):
        if not self.enabled: return
        pin, pout = self.prices[exact_model_id]
        with self.lock:
            res = self.reservations.pop(slot, None)
            if res is not None: self.reserved -= res
            if isinstance(usage, dict) and usage.get("prompt_tokens") is not None and usage.get("completion_tokens") is not None:
                # completion already includes reasoning tokens; never billed twice
                cost = (usage["prompt_tokens"] * pin + usage["completion_tokens"] * pout) / 1e6
            else:
                cost = res if res is not None else self.reserve_cost(exact_model_id)
            self.spent += cost

    def state(self):
        with self.lock:
            return {"enabled": self.enabled, "hard_cap_cny": getattr(self, "hard_cap", None),
                    "spent_cny_estimated": round(self.spent, 4), "reserved_cny": round(self.reserved, 4),
                    "stopped": self.stopped, "stop_reason": self.stop_reason}


# ---------------- slot execution ----------------
def run_slot(transport, run_dir, slot_row, budget, state, lock):
    slot = slot_row["slot_id"]
    sdir = os.path.join(run_dir, "slots", slot)
    sfile = os.path.join(run_dir, "slot_status", slot + ".json")
    os.makedirs(os.path.join(run_dir, "slot_status"), exist_ok=True)
    with lock:
        if os.path.exists(sfile):
            try: prev = json.load(open(sfile, encoding="utf-8"))
            except Exception: prev = None
            if prev and prev.get("status") in COMMITTED_STATES:
                return dict(prev, resumed_skipped=True)
        if state["stop_new_dispatch"]:
            return {"slot": slot, "status": "NOT_DISPATCHED", "http_status": None,
                    "note": "new dispatch stopped: %s" % state["stop_reason"]}
        if state["used"] >= state["authorized"]:
            return {"slot": slot, "status": "REFUSED_OVER_AUTHORIZED_BUDGET", "http_status": None}
        if not budget.try_reserve(slot, slot_row["exact_model_id"]):
            state["stop_new_dispatch"] = True
            state["stop_reason"] = state["stop_reason"] or budget.stop_reason or "BUDGET_HARD_CAP_REACHED"
            return {"slot": slot, "status": "NOT_DISPATCHED", "http_status": None,
                    "note": "budget reservation refused: %s" % state["stop_reason"]}
        state["used"] += 1
        state["new"] += 1
        body_bytes = slot_row["body_bytes"]
        body = json.loads(body_bytes)
        body_sha = slot_row["request_body_sha256"]  # file-bytes sha, bound in the frozen matrix
        idem = sha_bytes(("%s|%s|%s|%s|%s" % (PHASE, slot, slot_row["case_id"], slot_row["exact_model_id"], body_sha)).encode())
        committed = {"slot": slot, "phase": PHASE, "case_id": slot_row["case_id"],
                     "model_exact_id": slot_row["exact_model_id"],
                     "anonymous_model_id": slot_row["anonymous_model_id"],
                     "status": "DISPATCH_COMMITTED", "attempt": 1,
                     "request_body_sha256": body_sha, "idempotency_key": idem,
                     "committed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                     "transport_name": transport.name,
                     "fixture_label": "SELF_TEST_MOCK" if transport.name == "SELF_TEST" else FIXTURE_LABEL_LIVE}
        _atomic_write(sfile, committed)  # persisted BEFORE any transport call
    os.makedirs(sdir, exist_ok=True)
    try:
        with open(os.path.join(sdir, "request_body.json"), "wb") as fh:
            fh.write(body_bytes)  # byte-identical to the frozen input package body
    except Exception:
        pass
    t0 = time.time()
    try:
        outcome, status, err, body_lines, headers = transport.stream(body, slot=slot)
    except Exception as e:
        st = {"slot": slot, "phase": PHASE, "status": "POST_DISPATCH_LOCAL_ERROR", "error": str(e)[:200],
              "request_body_sha256": body_sha, "idempotency_key": idem,
              "note": "commit existed; result unknown; never re-dispatched"}
        _atomic_write(sfile, st)
        with lock:
            state["service_failure_run"] += 1
            _maybe_service_stop(state)
            _checkpoint(run_dir, state, budget)
        return st
    dur = time.time() - t0
    try:
        open(os.path.join(sdir, "raw_stream.sse"), "wb").write(b"".join(body_lines))
        if err: open(os.path.join(sdir, "error.txt"), "wb").write(err if isinstance(err, bytes) else str(err).encode())
        json.dump([[k, v] for k, v in headers if k.lower() not in ("authorization", "cookie", "set-cookie")],
                  open(os.path.join(sdir, "response_headers.json"), "w"), ensure_ascii=False)
        pr = parse_stream(body_lines)
        open(os.path.join(sdir, "visible_answer.txt"), "w", encoding="utf-8").write(pr["visible"])
        open(os.path.join(sdir, "reasoning.txt"), "w", encoding="utf-8").write(pr["reasoning"])
        json.dump(pr["paths"], open(os.path.join(sdir, "metadata_paths.json"), "w"), ensure_ascii=False, indent=1, sort_keys=True, default=str)
        json.dump({"rules_hit": pr["evidence_rules"], "has_real_search_evidence": pr["evidence"],
                   "detail": pr["evidence_detail"], "unknown_top_keys": pr["unknown"],
                   "evidence_keys_present": [k for k in pr["paths"] if re.search(r"search_info|plugins|x_tools|tool_calls|web_search|action\.sources", k)]},
                  open(os.path.join(sdir, "search_evidence.json"), "w"), ensure_ascii=False, indent=1, sort_keys=True)
        json.dump({"usage": pr["usage"], "finish_reason": pr["finish"], "provider_request_id": pr["rid"],
                   "sse_done": pr["done"], "transport_outcome": outcome, "slot_status": status,
                   "idempotency_key": idem, "request_body_sha256": body_sha, "duration_seconds": round(dur, 3),
                   "response_model_field": pr["response_model_field"], "system_fingerprint": pr["system_fingerprint"],
                   "fixture_label": "SELF_TEST_MOCK" if transport.name == "SELF_TEST" else FIXTURE_LABEL_LIVE},
                  open(os.path.join(sdir, "parse_meta.json"), "w"), ensure_ascii=False, indent=1, sort_keys=True)
        st = {"slot": slot, "phase": PHASE, "case_id": slot_row["case_id"],
              "model_exact_id": slot_row["exact_model_id"],
              "status": ("COMPLETE" if outcome == "OK" else ("HTTP_ERROR" if outcome == "HTTP_ERROR" else "TRANSPORT_ERROR")),
              "http_status": status, "provider_request_id": pr["rid"], "finish_reason": pr["finish"],
              "visible_len": len(pr["visible"]), "reasoning_len": len(pr["reasoning"]),
              "search_evidence_rules": pr["evidence_rules"], "has_real_search_evidence": pr["evidence"],
              "response_model_field": pr["response_model_field"], "system_fingerprint": pr["system_fingerprint"],
              "committed_utc": committed["committed_utc"],
              "request_body_sha256": body_sha}
    except Exception as e:
        st = {"slot": slot, "phase": PHASE, "status": "POST_DISPATCH_LOCAL_ERROR", "error": str(e)[:200],
              "post_processing": True, "request_body_sha256": body_sha, "idempotency_key": idem}
    _atomic_write(sfile, st)
    budget.settle(slot, (json.load(open(os.path.join(sdir, "parse_meta.json"), encoding="utf-8")).get("usage")
                         if os.path.exists(os.path.join(sdir, "parse_meta.json")) else None),
                  slot_row["exact_model_id"])
    with lock:
        state["terminal_new"] += 1
        svc_fail = st["status"] in ("HTTP_ERROR", "TRANSPORT_ERROR") and (
            st["status"] == "TRANSPORT_ERROR" or st.get("http_status") in SERVICE_FAILURE_HTTP)
        state["service_failure_run"] = state["service_failure_run"] + 1 if svc_fail else 0
        _maybe_service_stop(state)
        _checkpoint(run_dir, state, budget)
    return st


def _maybe_service_stop(state):
    if not state["stop_new_dispatch"] and state["service_failure_run"] >= SERVICE_FAILURE_RUN_LIMIT:
        state["stop_new_dispatch"] = True
        state["stop_reason"] = "PERSISTENT_SERVICE_FAILURE_RUN_%d" % state["service_failure_run"]


def _checkpoint(run_dir, state, budget):
    if state["terminal_new"] - state["last_checkpoint_at"] >= CHECKPOINT_EVERY or state["stop_new_dispatch"]:
        _atomic_write(os.path.join(run_dir, "checkpoint.json"),
                      {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                       "terminal_new_this_process": state["terminal_new"],
                       "api_calls_used_cumulative": state["used"],
                       "stop_new_dispatch": state["stop_new_dispatch"],
                       "stop_reason": state["stop_reason"],
                       "budget": budget.state()})
        state["last_checkpoint_at"] = state["terminal_new"]


# ---------------- launch gates ----------------
def read_key(key_file=None):
    k = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not k and key_file:
        stt = os.stat(key_file)
        if stat.S_IMODE(stt.st_mode) & 0o077: raise SystemExit("refusing key file not 0600")
        rawk = open(key_file, encoding="utf-8").read().strip()
        if "=" in rawk or "\n" in rawk.strip():
            raise SystemExit("key file looks like dotenv; source it and use env DASHSCOPE_API_KEY")
        k = rawk
    if not k: raise SystemExit("no API key: nothing dispatched")
    return k


def check_authorization(path, inputs_tar_sha):
    auth = json.load(open(path, encoding="utf-8"))
    if auth.get("release_allowed") is not True:
        raise SystemExit("AUTHORIZATION REFUSED: READINESS release_allowed != true (open gaps: %s)"
                         % auth.get("open_gaps"))
    if auth.get("input_package_sha256") != inputs_tar_sha:
        raise SystemExit("AUTHORIZATION REFUSED: input_package_sha256 mismatch")
    b = auth.get("budget") or {}
    if b.get("approved") is not True or not isinstance(b.get("hard_cap_cny"), (int, float)):
        raise SystemExit("AUTHORIZATION REFUSED: budget not approved or hard cap not numeric")
    return auth


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True, help="unpacked v2 offline input package directory (read-only)")
    ap.add_argument("--inputs-tar-sha256", default=None, help="sha256 of the v2 input tar recorded in READINESS")
    ap.add_argument("--run-dir", default=None, help="live run dir (default: ./run next to inputs); fixed per task")
    ap.add_argument("--authorization", default=None, help="READINESS.json path; REQUIRED for LIVE")
    ap.add_argument("--key-file", default=None)
    ap.add_argument("--endpoint", default="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
    ap.add_argument("--self-test", action="store_true", help="mock transport, zero network, SELF_TEST labels")
    ap.add_argument("--fixtures-dir", default=None)
    ap.add_argument("--self-test-budget", default=None,
                    help="budget JSON (approved/hard_cap_cny/unit_price_cny_per_1M) to exercise the "
                         "budget guard offline in --self-test; regression use only")
    ap.add_argument("--resume", action="store_true")
    a = ap.parse_args()

    pkg = InputPackage(a.inputs)
    run_dir = os.path.abspath(a.run_dir or os.path.join(os.getcwd(), "run"))

    if a.self_test:
        if not a.fixtures_dir or not os.path.isdir(a.fixtures_dir):
            raise SystemExit("--self-test requires --fixtures-dir")
        transport = MockTransport(a.fixtures_dir)
        if a.self_test_budget:
            budget = BudgetGuard(json.load(open(a.self_test_budget, encoding="utf-8")), enabled=True)
        else:
            budget = BudgetGuard(None, enabled=False)
    else:
        if not a.authorization:
            raise SystemExit("LIVE dispatch requires --authorization READINESS.json; nothing dispatched")
        auth = check_authorization(a.authorization, a.inputs_tar_sha256)
        transport = HttpTransport(read_key(a.key_file), a.endpoint)
        budget = BudgetGuard(auth["budget"], enabled=True)

    os.makedirs(run_dir, exist_ok=True)
    lock_path = os.path.join(run_dir, ".runner.lock")
    lock_fh = open(lock_path, "w")
    try:
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise SystemExit("another runner instance holds %s; single-instance enforced" % lock_path)
    lock_fh.write(str(os.getpid())); lock_fh.flush()

    if not a.resume:
        existing = os.path.join(run_dir, "slot_status")
        if os.path.isdir(existing) and os.listdir(existing):
            raise SystemExit("run dir has committed slots; use --resume (never overwrite evidence)")

    # cumulative accounting across processes
    committed_before = 0
    for s in pkg.slots:
        sf = os.path.join(run_dir, "slot_status", s["slot_id"] + ".json")
        if os.path.exists(sf):
            try: stt = json.load(open(sf, encoding="utf-8")).get("status")
            except Exception: stt = None
            if stt in COMMITTED_STATES: committed_before += 1
    state = {"used": committed_before, "new": 0, "authorized": SLOT_COUNT,
             "terminal_new": 0, "last_checkpoint_at": 0,
             "stop_new_dispatch": False, "stop_reason": None, "service_failure_run": 0}
    lock = threading.Lock()
    models = sorted({s["exact_model_id"] for s in pkg.slots})
    pmlocks = {m: threading.Lock() for m in models}

    def one(row):
        with pmlocks[row["exact_model_id"]]:
            return run_slot(transport, run_dir, row, budget, state, lock)

    results = []
    with ThreadPoolExecutor(max_workers=MODEL_COUNT) as ex:
        for r in ex.map(one, pkg.slots):
            results.append(r)
            if state["stop_new_dispatch"]:
                pass  # map continues; run_slot returns NOT_DISPATCHED for the rest without transport

    unknown = [s["slot_id"] for s in pkg.slots
               if (lambda p: os.path.exists(p) and json.load(open(p, encoding="utf-8")).get("status")
                   in ("DISPATCH_COMMITTED", "POST_DISPATCH_LOCAL_ERROR"))
                  (os.path.join(run_dir, "slot_status", s["slot_id"] + ".json"))]
    not_dispatched = [r["slot"] for r in results if r.get("status") == "NOT_DISPATCHED"]
    summary = {"transport": transport.name, "phase": PHASE, "stage": STAGE,
               "package_version": EXPECTED_INPUT_VERSION,
               "slots": results, "api_calls_used": state["used"],
               "api_calls_new_this_process": state["new"], "authorized": state["authorized"],
               "stop_new_dispatch": state["stop_new_dispatch"], "stop_reason": state["stop_reason"],
               "result_unknown_slots_held": unknown, "not_dispatched_slots": not_dispatched,
               "budget": budget.state(),
               "run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    _atomic_write(os.path.join(run_dir, "run_summary.json"), summary)
    print("dispatched %d new of %d authorized (cumulative %d, self_test=%s, stop=%s, unknown_held=%d, not_dispatched=%d)"
          % (state["new"], state["authorized"], state["used"], a.self_test, state["stop_reason"], len(unknown), len(not_dispatched)))
    print("runner finished; run validate_g8_formal_return.py then package_g8_formal_return.py; content failures are kept, never repaired.")


if __name__ == "__main__":
    main()
