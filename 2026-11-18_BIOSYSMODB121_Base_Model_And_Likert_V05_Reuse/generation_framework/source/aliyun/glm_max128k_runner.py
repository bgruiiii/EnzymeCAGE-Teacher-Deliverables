#!/usr/bin/env python3
"""glm_max128k_runner.py -- ZHIPU/GLM-5.3 default-max + 128K + json_object
FORMAL 121-case runner (configuration ZHIPU_GLM53_MAX_128K_JSON_OBJECT_CORRECTED).

Narrow derivation; NOTHING is invented wholesale:
- from the audited G6-R3/G8 formal runner lineage (g6r3_runner.py, three-model
  return 76a45fac..., local audit 4ede4ada...): commit-before-transport with
  fsync+rename, at-most-once COMMITTED_STATES never re-sent, resume sends only
  NOT_DISPATCHED, single-instance flock, raw SSE byte-verbatim + sanitized
  headers + search-evidence rules + parse_meta/idempotency, budget
  reserve/refund/settle with hard-cap stop, checkpoints, self-test mock mode
  that can never touch formal ledgers or be packaged as formal, run_summary
  with held/not-dispatched accounting;
- from the audited GLM T1 R2-R2 runner lineage (PROVIDER_ERROR fix):
  HTTP 200 + SSE top-level error is classified PROVIDER_ERROR and NEVER
  COMPLETE; provider_error.json + raw-derived evidence; effective-status
  extraction <NNN>.

Card-specified changes vs the two ancestors (authorized by the 2026-10-11
teacher decision 4ae7fe6ab73cbb4b2ccfc8563ac6f035b34a6bc5bd04cdb26d2145f78c5d1fa):
- single model ZHIPU/GLM-5.3, 121 slots GLM128K-F001..F121, concurrency=1
  (serial dispatch loop; no ThreadPoolExecutor);
- MAX_TOKENS=131072; shared contract additionally requires response_format
  json_object PRESENT, reasoning_effort ABSENT (default max),
  enable_thinking REMOVED (R1: bodies now carry exactly the T1
-  verified successful parameter contract; see inputs/REQUEST_BODY_DIFF_PROOFS.json
-  t1_contract_match); the frozen parent bodies remain untouched
- price basis 8/28 CNY per 1M (input/output), worst reserve per slot
  (10000*8+131072*28)/1e6 = 3.750016, total 453.751936, hard cap 600;
  guard re-computes these programmatically and refuses on drift;
- error policy per this card: ANY 401/403 (HTTP or SSE effective) -> immediate
  stop of new dispatch; provider/HTTP 400, JSON/schema/length/empty-visible ->
  slot terminal failure KEPT IN THE 121 DENOMINATOR, continue next case;
  429/5xx/transport/unknown-provider -> zero retry, terminal or HELD, 5
  consecutive service-class failures stop new dispatch; identity/budget/matrix/
  endpoint drift -> refusal before any transport; commits/HELD never re-sent;
- receiver (card section 3) runs per slot on the PERSISTED raw stream, never on
  in-process memory: rebuild visible/reasoning/usage/error, check DONE, finish,
  direct json.loads (no fence stripping, no repair, no reasoning extraction),
  top-level object, frozen Draft-07 schema (jsonschema import guarded; missing
  library yields null, never true), non-empty shell, integrity re-hash.
Self-test: zero network; SELF_TEST labels; scratch rehearsal ledger only.
"""
import argparse, fcntl, hashlib, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
WORK = os.path.abspath(os.path.join(ROOT, os.pardir))
TERMINAL = ("COMPLETE", "HTTP_ERROR", "TRANSPORT_ERROR", "PROVIDER_ERROR")
COMMITTED_STATES = ("DISPATCH_COMMITTED", "POST_DISPATCH_LOCAL_ERROR",
                    "COMPLETE", "HTTP_ERROR", "TRANSPORT_ERROR", "PROVIDER_ERROR")
TASK = "biosysmodb150_glm53_zhipu_max128k_121_formal_r1_20261011"
SCOPE = "LIVE_GLM53_MAX128K_121_FORMAL_R1"
CONFIGURATION_ID = "ZHIPU_GLM53_MAX_128K_JSON_OBJECT_CORRECTED"
MODEL = "ZHIPU/GLM-5.3"
ENDPOINT = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
MATRIX_SHA = "321b0ccbc51e9a77b24a70c122dfb825e8eac1b18db57599f71084ee60f64e56"
PROOFS_SHA = "c0fd450fae3ef67153dfd18c3237490266d2c2a0603cced15a6d502932f53a7f"
CONFIG_SHA = "28d9a19f401a12861dea9928f0ce8b2c685e1140066f6abc8952bdc42161c1be"
SCHEMA_SHA = "ebf2d47fd4737d7bdb020910b269b9245990d6e9a3e5b37570d8c572ac3bb9ae"
TEACHER_AUTHORITY_SHA = "4ae7fe6ab73cbb4b2ccfc8563ac6f035b34a6bc5bd0d4cdb26d2145f78c5d1fa"
N_SLOTS = 121
GLOBAL_CAP = 121
PROMPT_BOUND = 10000
MAX_TOKENS = 131072
PRICE_IN_PER_1M = 8.0
PRICE_OUT_PER_1M = 28.0
EXPECTED_RESERVE_PER_SLOT = 3.750016
EXPECTED_RESERVE_TOTAL = 453.751936
EXPECTED_HARD_CAP = 600.0
# exact successful T1 channel-control parameter contract (messages excluded);
# cross-checked against the 3/3 ZHIPU/GLM-5.3 probe bodies at the same time
T1_REF_PARAMS = {"model": "ZHIPU/GLM-5.3", "temperature": 0, "max_tokens": 131072,
                 "enable_search": False, "response_format": {"type": "json_object"},
                 "stream": True, "stream_options": {"include_usage": True}}
def params_without_messages(body):
    d = dict(body); d.pop("messages", None); return d
IMMEDIATE_STOP_HTTP = {401, 403}
SERVICE_RUN_LIMIT = 5
SERVICE_RUN_HTTP = {429} | set(range(500, 600))
CHECKPOINT_EVERY = 20
EFFECTIVE_STATUS_RE = re.compile(r"\s*<(\d{3})>")
STOP_MARKER_FILE = "formal_stop_markers.json"
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(open(p, "rb").read())
def utcnow(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def _atomic_write(path, obj):
    tmp = "%s.tmp.%d" % (path, os.getpid())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)
def _locked_update(path, fn):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            st = {}
            if os.path.exists(path):
                try: st = json.load(open(path, encoding="utf-8"))
                except Exception: st = {}
            st = fn(st); _atomic_write(path, st)
        finally:
            fcntl.flock(lk, fcntl.LOCK_UN)
    return st

# ---------------- SSE parse (G6-R3 rules + T1 provider-error capture) ----------------
def parse_stream(raw_lines):
    visible = []; reasoning = []; finish = None; usage = None; rid = None
    model_fp = None; sys_fp = "NOT_EXPOSED"; done = False
    provider_errors = []
    unknown = set()
    KNOWN_TOP = {"choices", "object", "created", "model", "id", "usage",
                 "system_fingerprint", "request_id", "requestId", "error"}
    KNOWN_DELTA = {"content", "reasoning_content", "role", "function_call", "tool_calls"}
    for b in raw_lines:
        line = b.decode("utf-8", "replace").strip()
        if not line.startswith("data:"): continue
        payload = line[5:].strip()
        if payload == "[DONE]": done = True; continue
        try: obj = json.loads(payload)
        except Exception: unknown.add("UNPARSEABLE_DATA_FRAME"); continue
        for k in obj.keys():
            if k not in KNOWN_TOP: unknown.add("top." + k)
        rid = rid or obj.get("id") or obj.get("request_id") or obj.get("requestId")
        model_fp = model_fp or obj.get("model")
        if obj.get("system_fingerprint"): sys_fp = obj["system_fingerprint"]
        if obj.get("usage"): usage = obj["usage"]
        if isinstance(obj.get("error"), dict): provider_errors.append(obj["error"])
        for ch in (obj.get("choices") or []):
            d = ch.get("delta") or {}
            for k in d.keys():
                if k not in KNOWN_DELTA: unknown.add("delta." + k)
            if d.get("content"): visible.append(d["content"])
            if d.get("reasoning_content"): reasoning.append(d["reasoning_content"])
            if ch.get("finish_reason"): finish = ch["finish_reason"]
    return dict(visible="".join(visible), reasoning="".join(reasoning),
                finish=finish, usage=usage, rid=rid, done=done,
                provider_errors=provider_errors, unknown=sorted(unknown),
                response_model_field=model_fp or "NOT_EXPOSED",
                system_fingerprint=sys_fp)

def provider_error_summary(err_obj):
    msg = str((err_obj or {}).get("message") or "")
    m = EFFECTIVE_STATUS_RE.match(msg)
    return {"code": (err_obj or {}).get("code"),
            "type": (err_obj or {}).get("type"),
            "effective_status": int(m.group(1)) if m else None,
            "message": msg[:800]}

# ---------------- budget guard (prices frozen by this card) ----------------
RESERVE_PER_SLOT = (PROMPT_BOUND * PRICE_IN_PER_1M + MAX_TOKENS * PRICE_OUT_PER_1M) / 1e6
def budget_selfcheck():
    ok = (abs(RESERVE_PER_SLOT - EXPECTED_RESERVE_PER_SLOT) < 1e-9
          and abs(RESERVE_PER_SLOT * N_SLOTS - EXPECTED_RESERVE_TOTAL) < 1e-6)
    if not ok: raise SystemExit("BUDGET_CONST_DRIFT")
    return ok
class BudgetGuard:
    def __init__(self, cfg, ledger_path, enabled=True):
        self.enabled = enabled; self.stopped = False; self.stop_reason = None
        if not enabled: return
        if cfg.get("approved") is not True: raise SystemExit("budget requires approved=true")
        self.hard_cap = float(cfg["hard_cap_cny"])
        if self.hard_cap > EXPECTED_HARD_CAP: raise SystemExit("BUDGET_REFUSED: hard cap above 600 card bound")
        if abs(self.hard_cap - EXPECTED_HARD_CAP) > 1e-9: raise SystemExit("BUDGET_REFUSED: hard cap must be exactly 600")
        p = cfg.get("unit_price_cny_per_1M", {}).get(MODEL, {})
        if float(p.get("input")) != PRICE_IN_PER_1M or float(p.get("output")) != PRICE_OUT_PER_1M:
            raise SystemExit("BUDGET_REFUSED: unit prices must be the frozen T1-observed 8/28 per 1M")
        budget_selfcheck()
        self.ledger = ledger_path
    def try_reserve(self, slot):
        if not self.enabled: return True
        cost = RESERVE_PER_SLOT
        def upd(st):
            spent = float(st.get("spent_cny_est", 0.0))
            outst = float(st.get("reserved_outstanding_cny", 0.0))
            if spent + outst + cost > self.hard_cap + 1e-9:
                st["cap_hit"] = True; return st
            st["reserved_outstanding_cny"] = outst + cost
            st.setdefault("reservations", {})[slot] = cost
            return st
        st = _locked_update(self.ledger, upd)
        if st.get("cap_hit"):
            self.stopped = True; self.stop_reason = "BUDGET_HARD_CAP_REACHED_600"; return False
        return True
    def refund(self, slot):
        if not self.enabled: return
        def upd(st):
            res = float((st.get("reservations") or {}).pop(slot, 0.0))
            st["reserved_outstanding_cny"] = max(0.0, float(st.get("reserved_outstanding_cny", 0.0)) - res)
            return st
        _locked_update(self.ledger, upd)
    def settle(self, slot, usage):
        if not self.enabled: return
        def upd(st):
            res = float((st.get("reservations") or {}).pop(slot, 0.0))
            st["reserved_outstanding_cny"] = max(0.0, float(st.get("reserved_outstanding_cny", 0.0)) - res)
            if isinstance(usage, dict) and usage.get("prompt_tokens") is not None and usage.get("completion_tokens") is not None:
                st["spent_cny_est"] = float(st.get("spent_cny_est", 0.0)) + (usage["prompt_tokens"] * PRICE_IN_PER_1M + usage["completion_tokens"] * PRICE_OUT_PER_1M) / 1e6
            else:
                st["spent_cny_est"] = float(st.get("spent_cny_est", 0.0)) + res
            return st
        _locked_update(self.ledger, upd)
    def state(self):
        if not self.enabled: return {"enabled": False}
        st = json.load(open(self.ledger, encoding="utf-8")) if os.path.exists(self.ledger) else {}
        return {"enabled": True, "hard_cap_cny": self.hard_cap,
                "reserve_per_slot_cny": round(RESERVE_PER_SLOT, 6),
                "spent_cny_est": round(float(st.get("spent_cny_est", 0)), 6),
                "reserved_outstanding_cny": round(float(st.get("reserved_outstanding_cny", 0)), 6),
                "stopped": self.stopped, "stop_reason": self.stop_reason}

# ---------------- authorization ----------------
def check_authorization(path):
    if not path: raise SystemExit("LIVE dispatch requires --authorization; nothing dispatched")
    au = json.load(open(path, encoding="utf-8"))
    checks = [
        au.get("release_allowed") is True,
        au.get("scope") == SCOPE,
        au.get("task_id") == TASK,
        au.get("authority_sha256") == TEACHER_AUTHORITY_SHA,
        au.get("matrix_sha256") == MATRIX_SHA,
        au.get("diff_proofs_sha256") == PROOFS_SHA,
        au.get("config_sha256") == CONFIG_SHA,
        au.get("max_calls") == N_SLOTS,
        au.get("retries") == 0,
        au.get("configuration_id") == CONFIGURATION_ID,
        au.get("model_exact_id") == MODEL,
        au.get("endpoint") == ENDPOINT,
        (au.get("budget") or {}).get("approved") is True,
    ]
    if not all(checks):
        bad = [i for i, c in enumerate(checks) if not c]
        raise SystemExit("AUTHORIZATION_REFUSED: exact contract mismatch at %s" % bad)
    return au

# ---------------- matrix + frozen contract validation ----------------
def load_matrix():
    path = os.path.join(ROOT, "inputs/MATRIX.json")
    if sha_file(path) != MATRIX_SHA: raise SystemExit("IDENTITY_REFUSED: matrix sha drift")
    mx = json.load(open(path, encoding="utf-8"))
    slots = mx["slots"]
    if (mx["max_calls"] != N_SLOTS or mx["retries"] != 0 or mx["concurrency"] != 1
        or len(slots) != N_SLOTS or [s["slot"] for s in slots] != mx["dispatch_order_slots"]):
        raise SystemExit("IDENTITY_REFUSED: matrix header drift")
    cases = [s["case_id"] for s in slots]
    if len(set(cases)) != N_SLOTS: raise SystemExit("CASE_SET_INVALID: duplicate cases")
    proofs_path = os.path.join(ROOT, "inputs/REQUEST_BODY_DIFF_PROOFS.json")
    if sha_file(proofs_path) != PROOFS_SHA: raise SystemExit("IDENTITY_REFUSED: proofs sha drift")
    proofs = {p["case_id"]: p for p in json.load(open(proofs_path, encoding="utf-8"))["proofs"]}
    schema_path = os.path.join(ROOT, "inputs/schemas/biodegradation_answer_v2.schema.json")
    if sha_file(schema_path) != SCHEMA_SHA: raise SystemExit("IDENTITY_REFUSED: schema drift")
    seen_cases = set()
    for s in slots:
        case = s["case_id"]
        if s["status"] != "NOT_DISPATCHED" or s["model_exact_id"] != MODEL \
           or s["configuration_id"] != CONFIGURATION_ID:
            raise SystemExit("matrix row wrong: %s" % s["slot"])
        if case in seen_cases: raise SystemExit("CASE_SET_INVALID: %s" % case)
        seen_cases.add(case)
        bp = os.path.join(ROOT, s["body_path"])
        if sha_file(bp) != s["body_sha256"]: raise SystemExit("body sha mismatch %s" % s["slot"])
        pb = os.path.join(ROOT, s["parent_body_path"])
        if sha_file(pb) != s["parent_body_sha256"]: raise SystemExit("parent body sha mismatch %s" % s["slot"])
        mp = os.path.join(ROOT, s["messages_path"])
        mlist = json.load(open(mp, encoding="utf-8"))["messages"]
        if sha_bytes(json.dumps(mlist, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) != s["messages_sha256"]:
            raise SystemExit("messages digest mismatch %s" % s["slot"])
        body = json.load(open(bp, encoding="utf-8"))
        parent = json.load(open(pb, encoding="utf-8"))
        # frozen shared contract + allowed-diff-only proof vs parent
        if body.get("model") != MODEL or body.get("max_tokens") != MAX_TOKENS \
           or body.get("temperature") != 0 or body.get("enable_search") is not False \
           or body.get("stream") is not True or body.get("stream_options") != {"include_usage": True} \
           or body.get("response_format") != {"type": "json_object"} \
           or "enable_thinking" in body:
            raise SystemExit("BODY_CONTRACT_VIOLATION %s" % s["slot"])
        if "reasoning_effort" in body: raise SystemExit("REASONING_EFFORT_FORBIDDEN %s" % s["slot"])
        if params_without_messages(body) != T1_REF_PARAMS:
            raise SystemExit("T1_CONTRACT_MISMATCH %s" % s["slot"])
        check = dict(body)
        check["max_tokens"] = 65536; check.pop("response_format")
        check["reasoning_effort"] = "low"; check["enable_thinking"] = True
        if check != parent: raise SystemExit("UNALLOWED_BODY_DIFF %s" % s["slot"])
        if set(body) != set(parent) - {"reasoning_effort", "enable_thinking"} | {"response_format"}:
            raise SystemExit("ALLOWED_DIFF_KEYSET_FAIL %s" % s["slot"])
        pf = proofs.get(case)
        if not pf or pf["new_body_sha256"] != s["body_sha256"] or pf["old_body_sha256"] != s["parent_body_sha256"] \
           or pf["messages_sha256"] != s["messages_sha256"] or pf["no_other_diff"] is not True:
            raise SystemExit("PROOF_BINDING_FAIL %s" % case)
    if len(seen_cases) != N_SLOTS: raise SystemExit("CASE_SET_INVALID: not 121")
    return slots, schema_path

# ---------------- receiver (card section 3): independent from persisted raw ----------------
def receiver_check(rundir, slot, schema_path):
    sdir = os.path.join(rundir, "slots", slot)
    rawp = os.path.join(sdir, "raw_stream.sse")
    out = {"slot": slot, "receiver_utc": utcnow(),
           "raw_present": os.path.isfile(rawp)}
    if not out["raw_present"]:
        out.update(dict(status_source="MISSING_RAW", done=False, finish=None,
                        json_valid=False, object_form=False, schema_valid=None,
                        non_empty_shell=False, integrity_findings=["MISSING_RAW"],
                        slot_pass=False, engineering_class="HELD_NO_RAW"))
        return out
    raw = open(rawp, "rb").read()
    pr = parse_stream(raw.split(b"\n"))
    vis_file = os.path.join(sdir, "visible_answer.txt")
    rea_file = os.path.join(sdir, "reasoning.txt")
    findings = []
    if os.path.isfile(vis_file) and open(vis_file, encoding="utf-8").read() != pr["visible"]:
        findings.append("VISIBLE_RAW_MISMATCH")
    if os.path.isfile(rea_file) and open(rea_file, encoding="utf-8").read() != pr["reasoning"]:
        findings.append("REASONING_RAW_MISMATCH")
    if pr["provider_errors"]:
        pe = provider_error_summary(pr["provider_errors"][0])
        pp = os.path.join(sdir, "provider_error.json")
        if os.path.isfile(pp):
            disk = json.load(open(pp, encoding="utf-8"))
            if sha_bytes(json.dumps(disk, sort_keys=True).encode()) != sha_bytes(json.dumps(pr["provider_errors"][0], sort_keys=True).encode()):
                findings.append("PROVIDER_ERROR_FILE_MISMATCH")
        else:
            findings.append("PROVIDER_ERROR_NOT_PERSISTED")
    else:
        pe = None
    if pr["response_model_field"].lower() not in (MODEL.lower(), "zhipu/glm-5.3"):
        findings.append("RESPONSE_MODEL_MISMATCH")
    json_valid = False; object_form = False; schema_valid = None; shell = False
    try:
        ans = json.loads(pr["visible"]) if pr["visible"] else None
        json_valid = ans is not None
        object_form = isinstance(ans, dict)
        if object_form:
            try:
                import jsonschema
                errs = [e.message for e in jsonschema.Draft7Validator(
                    json.load(open(schema_path, encoding="utf-8"))).iter_errors(ans)]
                schema_valid = (len(errs) == 0)
            except ImportError:
                schema_valid = None
                findings.append("SCHEMA_VALIDATOR_UNAVAILABLE_NULL")
            if object_form and ans.get("case_id") and isinstance(ans.get("steps"), list) and len(ans["steps"]) > 0 \
               and isinstance(ans.get("evidence_registry"), list):
                shell = True
    except Exception:
        json_valid = False; object_form = False; schema_valid = False
    done = pr["done"]; finish = pr["finish"]
    if pr["unknown"]: findings.append("UNKNOWN_FRAME_KEYS:" + ",".join(pr["unknown"])[:120])
    if pr["provider_errors"]: eng = "PROVIDER_ERROR"
    elif finish == "length": eng = "FINISH_LENGTH"
    elif not pr["visible"]: eng = "VISIBLE_EMPTY"
    elif not json_valid: eng = "JSON_INVALID"
    elif not object_form: eng = "NON_OBJECT"
    elif schema_valid is False: eng = "SCHEMA_INVALID"
    elif not done: eng = "NO_DONE"
    elif finish != "stop": eng = "FINISH_" + str(finish).upper()
    elif not shell: eng = "EMPTY_SHELL"
    else: eng = "USABLE"
    critical = [f for f in findings if not f.startswith("SCHEMA_VALIDATOR")
                and not f.startswith("UNKNOWN_FRAME_KEYS")]
    slot_pass = (eng == "USABLE" and schema_valid is True
                 and pr["usage"] is not None and not critical)
    return dict(slot=slot, receiver_utc=utcnow(), raw_present=True,
                raw_sha256=sha_bytes(raw), done=done, finish=finish,
                provider_error=pe, visible_len=len(pr["visible"]),
                reasoning_len=len(pr["reasoning"]), usage=pr["usage"],
                rid=pr["rid"], response_model_field=pr["response_model_field"],
                json_valid=bool(json_valid), object_form=bool(object_form),
                schema_valid=schema_valid, non_empty_shell=shell,
                integrity_findings=findings, engineering_class=eng,
                slot_pass=bool(slot_pass))

# ---------------- transports ----------------
class HttpTransport:
    name = "LIVE"
    def __init__(self, key, endpoint): self.key = key; self.endpoint = endpoint
    def stream(self, body, timeout=3600):
        import urllib.request, urllib.error
        req = urllib.request.Request(self.endpoint,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + self.key,
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
    name = "SELF_TEST"
    def __init__(self, fixtures_dir, fixture="default.sse"): self.d = fixtures_dir; self.f = fixture
    def stream(self, body, timeout=3600):
        slot = body["messages"][0]["content"].split("case_id: ")[1].split("\n")[0]
        he = os.path.join(self.d, slot + ".http_error")
        if os.path.exists(he):
            code = int(open(he, encoding="utf-8").read().strip() or "429")
            eb = os.path.join(self.d, slot + ".errbody")
            err = open(eb, "rb").read() if os.path.exists(eb) else b'{"error":"mock"}'
            return "HTTP_ERROR", code, err, [], []
        if os.path.exists(os.path.join(self.d, slot + ".transport_error")):
            return "TRANSPORT_ERROR", None, b"mock transport failure", [], []
        f = os.path.join(self.d, slot + ".sse")
        if not os.path.exists(f): f = os.path.join(self.d, self.f)
        lines = [l.encode() + b"\n" for l in open(f, encoding="utf-8").read().splitlines()]
        return "OK", 200, b"", lines, [("x-self-test", "1")]

# ---------------- main loop ----------------
def write_stop_marker(ledger_dir, kind, record):
    def upd(st):
        st.setdefault("markers", {})[kind] = record
        return st
    _locked_update(os.path.join(ledger_dir, STOP_MARKER_FILE), upd)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--authorization", default=None)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--fixtures-dir", default=None)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--preflight", action="store_true")
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--endpoint", default=ENDPOINT)
    a = ap.parse_args()
    slots, schema_path = load_matrix()
    budget_selfcheck()
    if a.preflight:
        print("PREFLIGHT_PASS task=%s model=%s configuration=%s slots=%d "
              "max_calls=%d retries=0 concurrency=1 max_tokens=%d effort=OMITTED_DEFAULT_MAX "
              "response_format=json_object enable_thinking=OMITTED reserve_per_slot=%.6f total=%.6f hard_cap=%.1f network_calls=0"
              % (TASK, MODEL, CONFIGURATION_ID, len(slots), N_SLOTS, MAX_TOKENS,
                 RESERVE_PER_SLOT, RESERVE_PER_SLOT * N_SLOTS, EXPECTED_HARD_CAP))
        return 0
    rundir = os.path.join(WORK, "formal_run")
    if not a.self_test and a.endpoint != ENDPOINT:
        raise SystemExit("refusing: public PAYG endpoint only")
    if a.self_test:
        if not a.fixtures_dir or not os.path.isdir(a.fixtures_dir): raise SystemExit("--self-test requires --fixtures-dir")
        transport = MockTransport(a.fixtures_dir)
        ledger_path = a.ledger or os.path.join(rundir, ".rehearsal_ledger.json")
        budget = BudgetGuard(None, ledger_path, enabled=False)
    else:
        au = check_authorization(a.authorization)
        k = os.environ.get("DASHSCOPE_API_KEY", "").strip()
        if not k: raise SystemExit("BLOCKED_MISSING_PAYG_API_KEY / nothing dispatched")
        transport = HttpTransport(k, a.endpoint)
        ledger_path = a.ledger or os.path.join(WORK, "ledger", "glm128k_formal_calls.json")
        budget = BudgetGuard(au["budget"], ledger_path, enabled=True)
    os.makedirs(rundir, exist_ok=True)
    lk = open(os.path.join(rundir, ".runner.lock"), "w")
    try: fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: raise SystemExit("single instance: another runner holds the lock")
    lk.write(str(os.getpid())); lk.flush()
    ss = os.path.join(rundir, "slot_status")
    if not a.resume:
        if os.path.isdir(ss) and os.listdir(ss): raise SystemExit("run dir has slots; use --resume (never overwrite)")
    state = {"used": 0, "new": 0, "authorized": N_SLOTS, "terminal_new": 0,
             "last_ck": 0, "stop_new_dispatch": False, "stop_reason": None,
             "service_run": 0}
    committed_before = 0
    for s in slots:
        p = os.path.join(ss, s["slot"] + ".json")
        if os.path.exists(p):
            try:
                if json.load(open(p, encoding="utf-8")).get("status") in COMMITTED_STATES: committed_before += 1
            except Exception: pass
    state["used"] = committed_before
    results = []
    for s in slots:
        slot = s["slot"]; sfile = os.path.join(ss, slot + ".json")
        if os.path.exists(sfile):
            try: prev = json.load(open(sfile, encoding="utf-8"))
            except Exception: prev = None
            if prev and prev.get("status") in COMMITTED_STATES:
                results.append(dict(prev, resumed_skipped=True)); continue
        if state["stop_new_dispatch"]:
            results.append({"slot": slot, "status": "NOT_DISPATCHED", "note": "stop: " + str(state["stop_reason"])}); continue
        if state["used"] >= state["authorized"]:
            results.append({"slot": slot, "status": "REFUSED_OVER_PHASE_CAP"}); continue
        if not budget.try_reserve(slot):
            state["stop_new_dispatch"] = True
            state["stop_reason"] = budget.stop_reason or "BUDGET"
            write_stop_marker(os.path.dirname(ledger_path), "BUDGET_HARD_CAP_REACHED_600", {"utc": utcnow(), "slot": slot})
            results.append({"slot": slot, "status": "NOT_DISPATCHED", "note": "budget refused"}); continue
        state["used"] += 1; state["new"] += 1
        body_bytes = open(os.path.join(ROOT, s["body_path"]), "rb").read()
        body = json.loads(body_bytes)
        body_sha = s["body_sha256"]
        idem = sha_bytes(("%s|%s|%s|%s" % (TASK, slot, s["case_id"], body_sha)).encode())
        committed = {"slot": slot, "task": TASK, "case_id": s["case_id"],
                     "model_exact_id": MODEL, "configuration_id": CONFIGURATION_ID,
                     "status": "DISPATCH_COMMITTED", "attempt": 1,
                     "request_body_sha256": body_sha, "idempotency_key": idem,
                     "committed_utc": utcnow(),
                     "transport_name": transport.name,
                     "fixture_label": "SELF_TEST_MOCK" if transport.name == "SELF_TEST" else "LIVE_GLM53_MAX128K_121_FORMAL_R1"}
        _atomic_write(sfile, committed)
        sdir = os.path.join(rundir, "slots", slot)
        os.makedirs(sdir, exist_ok=True)
        open(os.path.join(sdir, "request_body.json"), "wb").write(body_bytes)
        t0 = time.time()
        try:
            outcome, status, err, blines, headers = transport.stream(body)
        except Exception as e:
            budget.settle(slot, None)
            _atomic_write(sfile, {"slot": slot, "status": "POST_DISPATCH_LOCAL_ERROR",
                                  "error": str(e)[:200], "request_body_sha256": body_sha,
                                  "idempotency_key": idem, "committed_utc": committed["committed_utc"],
                                  "note": "commit existed; result unknown; never re-dispatched"})
            state["terminal_new"] += 1
            _checkpoint(rundir, state, budget)
            results.append(json.load(open(sfile, encoding="utf-8"))); continue
        dur = time.time() - t0
        open(os.path.join(sdir, "raw_stream.sse"), "wb").write(b"".join(blines))
        if err: open(os.path.join(sdir, "error.txt"), "wb").write(err if isinstance(err, bytes) else str(err).encode())
        json.dump([[k, v] for k, v in headers if k.lower() not in ("authorization", "cookie", "set-cookie")],
                  open(os.path.join(sdir, "response_headers.json"), "w"), ensure_ascii=False)
        pr = parse_stream(blines)
        open(os.path.join(sdir, "visible_answer.txt"), "w", encoding="utf-8").write(pr["visible"])
        open(os.path.join(sdir, "reasoning.txt"), "w", encoding="utf-8").write(pr["reasoning"])
        if pr["provider_errors"]:
            _atomic_write(os.path.join(sdir, "provider_error.json"), pr["provider_errors"][0])
        budget.settle(slot, pr["usage"])
        rc = receiver_check(rundir, slot, schema_path)
        _atomic_write(os.path.join(sdir, "receiver.json"), rc)
        status_class = ("COMPLETE" if outcome == "OK" and not pr["provider_errors"] else
                        "PROVIDER_ERROR" if pr["provider_errors"] else
                        "HTTP_ERROR" if outcome == "HTTP_ERROR" else "TRANSPORT_ERROR")
        st = {"slot": slot, "case_id": s["case_id"], "model_exact_id": MODEL,
              "configuration_id": CONFIGURATION_ID,
              "status": status_class, "http_status": status,
              "provider_request_id": pr["rid"], "finish_reason": pr["finish"],
              "sse_done": pr["done"],
              "provider_effective_status": (provider_error_summary(pr["provider_errors"][0])["effective_status"]
                                            if pr["provider_errors"] else None),
              "engineering_class": rc["engineering_class"], "slot_pass": rc["slot_pass"],
              "visible_len": len(pr["visible"]), "reasoning_len": len(pr["reasoning"]),
              "usage": pr["usage"], "response_model_field": pr["response_model_field"],
              "duration_seconds": round(dur, 3),
              "committed_utc": committed["committed_utc"],
              "request_body_sha256": body_sha, "idempotency_key": idem}
        _atomic_write(sfile, st)
        results.append(st)
        state["terminal_new"] += 1
        eff = st["provider_effective_status"]
        imm = (status_class == "HTTP_ERROR" and status in IMMEDIATE_STOP_HTTP) or \
              (status_class == "PROVIDER_ERROR" and eff in IMMEDIATE_STOP_HTTP)
        svc = ((status_class == "HTTP_ERROR" and (status in SERVICE_RUN_HTTP)) or
               (status_class == "TRANSPORT_ERROR") or
               (status_class == "PROVIDER_ERROR" and eff is not None and
                (eff in SERVICE_RUN_HTTP or eff not in (400,))))
        if imm:
            state["stop_new_dispatch"] = True
            state["stop_reason"] = "AUTH_%s_IMMEDIATE_STOP" % (eff if eff is not None else status)
            write_stop_marker(os.path.dirname(ledger_path), "AUTH_IMMEDIATE_STOP",
                              {"utc": utcnow(), "slot": slot, "http_or_effective": status or eff})
        elif svc:
            state["service_run"] += 1
            if state["service_run"] >= SERVICE_RUN_LIMIT:
                state["stop_new_dispatch"] = True
                state["stop_reason"] = "PERSISTENT_SERVICE_FAILURE_RUN_%d" % state["service_run"]
                write_stop_marker(os.path.dirname(ledger_path), "SERVICE_RUN_STOP",
                                  {"utc": utcnow(), "slot": slot, "streak": state["service_run"]})
        else:
            state["service_run"] = 0
        _checkpoint(rundir, state, budget)
    held = [s["slot"] for s in slots
            if os.path.exists(os.path.join(ss, s["slot"] + ".json"))
            and json.load(open(os.path.join(ss, s["slot"] + ".json"), encoding="utf-8")).get("status")
            in ("DISPATCH_COMMITTED", "POST_DISPATCH_LOCAL_ERROR")]
    nd = [r["slot"] for r in results if r.get("status") == "NOT_DISPATCHED"]
    terminal_states = [json.load(open(os.path.join(ss, x["slot"] + ".json"), encoding="utf-8"))
                       for x in slots if os.path.exists(os.path.join(ss, x["slot"] + ".json"))
                       and json.load(open(os.path.join(ss, x["slot"] + ".json"), encoding="utf-8")).get("status") in TERMINAL]
    passes = sum(1 for x in terminal_states if x.get("slot_pass"))
    os.makedirs(os.path.join(rundir, "decision"), exist_ok=True)
    rows = ["slot\tcase_id\tstatus\thttp_status\tprovider_effective_status\tfinish_reason\tsse_done\tengineering_class\tslot_pass\tvisible_len\treasoning_len\tprompt_tokens\tcompletion_tokens\treasoning_tokens\trequest_body_sha256\tprovider_request_id"]
    for x in terminal_states:
        u = x.get("usage") or {}
        rt = ((u.get("completion_tokens_details") or {}).get("reasoning_tokens"))
        rows.append("\t".join(str(v) for v in [x["slot"], x["case_id"], x["status"], x.get("http_status"), x.get("provider_effective_status"),
                    x.get("finish_reason"), x.get("sse_done"), x.get("engineering_class"), x.get("slot_pass"),
                    x.get("visible_len"), x.get("reasoning_len"), u.get("prompt_tokens"), u.get("completion_tokens"), rt,
                    x.get("request_body_sha256"), x.get("provider_request_id")]))
    open(os.path.join(rundir, "decision/completion_matrix.tsv"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    summary = {"transport": transport.name, "task": TASK,
               "configuration_id": CONFIGURATION_ID, "model_exact_id": MODEL,
               "slot_count": N_SLOTS, "api_calls_used": state["used"],
               "api_calls_new_this_process": state["new"],
               "slot_pass": passes, "terminal": len(terminal_states),
               "held": len(held), "not_dispatched": len(nd),
               "stop_new_dispatch": state["stop_new_dispatch"],
               "stop_reason": state["stop_reason"],
               "held_slots": held, "not_dispatched_slots": nd,
               "budget": budget.state(),
               "matrix_sha256": MATRIX_SHA, "diff_proofs_sha256": PROOFS_SHA,
               "run_utc": utcnow(),
               "retries": 0, "concurrency": 1,
               "scientific_denominator": N_SLOTS}
    _atomic_write(os.path.join(rundir, "run_summary.json"), summary)
    print("task=%s dispatched %d new (cumulative %d/121) terminal=%d slot_pass=%d held=%d not_dispatched=%d stop=%s self_test=%s"
          % (TASK, state["new"], state["used"], len(terminal_states), passes, len(held), len(nd),
             state["stop_reason"], transport.name == "SELF_TEST"))

def _checkpoint(rundir, state, budget):
    if state["terminal_new"] - state["last_ck"] >= CHECKPOINT_EVERY or state["stop_new_dispatch"]:
        _atomic_write(os.path.join(rundir, "checkpoint.json"),
            {"utc": utcnow(), "task": TASK,
             "terminal_new_this_process": state["terminal_new"],
             "api_calls_used_cumulative": state["used"],
             "stop_new_dispatch": state["stop_new_dispatch"],
             "stop_reason": state["stop_reason"],
             "budget": budget.state(), "retries": 0})
        state["last_ck"] = state["terminal_new"]

if __name__ == "__main__": main()
