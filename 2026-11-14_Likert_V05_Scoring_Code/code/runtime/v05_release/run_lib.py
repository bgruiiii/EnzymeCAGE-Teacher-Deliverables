"""F2 R1 scoring runner (audit F2-P1-01/03/04/05 fixes integrated).

Pipeline per target: run-identity check → cache (revalidated) → checkpoint
dedup (IDENTITY-VERIFIED) → per-slot persistent quota → budget reserve
(per-attempt, actual body size) → send → FULL wire archive → transport-level
settlement (usage-first, rating validity irrelevant) → parse+validate →
canonical record (shared totals contract) → commit.

Wire: LiveTransport (f2r12_transport) implements the frozen stream=true SSE
protocol ported from the production-proven collector, plus a non-stream path;
the HTTP session is injectable so the REAL parse path is tested offline with
fake responses. MockTransport remains for pipeline-level tests and returns
WireOutcome-shaped dicts.

Live gate (unchanged in spirit, hardened): USER_CONFIRMED_FROZEN config +
user confirmation record binding its sha + CLI flag + API key env existence +
E0 evidence bound + prices ONLY from the confirmed config (no CLI price
override on the live path).

Offline: importing performs no network I/O; `requests` imported only inside
LiveTransport construction without an injected session, under the gate.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (F2_DIR, read_json, sha256_file, sha256_bytes,
                         canonical_json, utc_now_iso, totals_contract)
import v05_request_builder as rb
import release_validation as rv
from f2r12_budget_ledger import (BudgetLedger, BudgetStop, AttemptCapReached,
                                SlotAttemptQuotaExceeded, AuthStop,
                                usage_cost_cny)
from f2r12_cache_checkpoint import (ResponseCache, Checkpoint, AttemptArchive,
                                    IdentityDriftError, load_canonical_jsonl,
                                    repair_canonical)

LIVE_FLAG = "--i-confirm-live-paid-calls"
RETRYABLE_KINDS = {"RATE_LIMIT", "SERVER_5XX", "TIMEOUT", "INVALID_JSON",
                   "SCHEMA_FAIL", "NO_CONTENT_BLOCK", "NO_TERMINAL_MARKER",
                   "CHUNK_PARSE_ERRORS", "READ_ERROR",
                   "SSE_PARSE_EXCEPTION", "MOCK_SCRIPT_EXHAUSTED"}
# R1.1: connection-loss kinds carry a dynamic suffix (exception type) —
# matched by prefix in the retry decision
RETRYABLE_KIND_PREFIXES = ("CONNECTION_LOST_UNKNOWN_STAGE",)
NEUTRAL_RETRY_NOTE = ("\n\n[技术重试附注] 上一次响应无法作为符合schema的合法JSON评分对象被接受"
                      "（技术原因）。请重新只输出一个符合RATING_OUTPUT_SCHEMA的JSON对象，"
                      "不含任何其他文本。本附注不涉及任何评分内容。")


class LiveGateError(RuntimeError):
    pass


class ModelDriftStop(RuntimeError):
    pass


# ---------------------------------------------------------------- transports

class MockTransport:
    """Pipeline-level test double. Script maps slot_uid → [WireOutcome dicts].
    Outcomes use the SAME shape as f2r12_transport.WireOutcome (raw bytes via
    raw_response_bytes or legacy raw_text)."""

    def __init__(self, script):
        self.script = script
        self.calls = []
        self._lock = threading.Lock()

    def send(self, request: dict, timeout: int):
        ident = request["item_identity"]
        uid = ident["b_slot_uid"]
        with self._lock:
            n = sum(1 for c in self.calls if c["b_slot_uid"] == uid)
            self.calls.append({"b_slot_uid": uid, "attempt_index": n,
                               "model": request["body"]["model"],
                               "approx_input_tokens": request["approx_input_tokens"],
                               "user_message_sha256": ident["user_message_sha256"],
                               "request_body_sha256": sha256_bytes(
                                   json.dumps(request["body"], ensure_ascii=False).encode("utf-8"))})
            outcomes = self.script.get(uid) or []
            if n >= len(outcomes):
                return {"http_status": 500, "raw_response_bytes": None, "raw_text": None,
                        "usage": None, "error_kind": "MOCK_SCRIPT_EXHAUSTED",
                        "may_have_billed": False, "response_received": False}
            return outcomes[n]


def build_live_transport(cfg: dict, reasons_checker, live_flag_given: bool):
    """Construct the REAL transport under the full live gate. `requests` is
    imported inside f2r12_transport only when session=None."""
    from f2r12_transport import LiveTransport
    api_env = (cfg.get("run_boundaries") or {}).get("api_key_env_var_name")
    key_present = bool(api_env and not str(api_env).startswith("PENDING")
                       and api_env in os.environ)
    reasons = reasons_checker(cfg, live_flag_given, key_present)
    if reasons:
        raise LiveGateError("; ".join(reasons))
    key = os.environ.get(api_env)  # value used only in-memory for the header;
    # never logged, never persisted (archive stores authorization_stored=False)
    endpoint = cfg["scoring_ai"]["recommended"]["endpoint"]
    stream = bool((cfg["model_parameters"].get("stream") or {}).get("value", True))
    return LiveTransport(endpoint, key, session=None, stream=stream)


def live_gate_reasons(cfg: dict, confirmation, live_flag_given: bool,
                      api_key_present: bool) -> list:
    reasons = list(rb.config_gate(cfg, confirmation, require_confirmed=True))
    if not live_flag_given:
        reasons.append(f"CLI flag {LIVE_FLAG} not given")
    if not api_key_present:
        reasons.append("API key env var does not exist (checked by name only)")
    ev = (cfg.get("content_identity") or {}).get("evidence_snapshot_sha256")
    if not ev or "PENDING" in str(ev):
        reasons.append(f"evidence not bound: {ev!r} (F3 E0 package required before live scoring)")
    return reasons


def load_confirmation(cfg: dict):
    from common_03a import OUT as _ROUT
    p = cfg.get("_confirmation_path") or (_ROUT.parent / "config/F4_USER_CONFIG_CONFIRMATION.json")
    if os.path.exists(p):
        return read_json(p)
    return None


# -------------------------------------------------------------------- runner

class ScoringRunner:
    def __init__(self, cfg: dict, run_root, transport, schema: dict,
                 price_in_per_1m: float, price_out_per_1m: float,
                 run_id: str | None = None,
                 synthetic_test_prices: bool = False,
                 evidence_identity_sha256: str = "PENDING_F3_E0_BINDING"):
        # --- prices: live runs take them ONLY from the confirmed config ---
        self.synthetic_test_prices = bool(synthetic_test_prices)
        if not self.synthetic_test_prices:
            cfg_prices = _confirmed_prices(cfg)
            if cfg_prices is None:
                raise LiveGateError(
                    "prices not confirmed in config — live runs may not use CLI/injected prices")
            price_in_per_1m, price_out_per_1m = cfg_prices
        self.price_in = float(price_in_per_1m)
        self.price_out = float(price_out_per_1m)

        self.cfg = cfg
        self.run_id = run_id or f"F4_RUN_{utc_now_iso().replace(':', '').replace('-', '')}"
        self.root = str(run_root)
        os.makedirs(self.root, exist_ok=True)
        self.transport = transport
        self.schema = schema
        sched = cfg.get("scheduling") or {}
        est = (cfg.get("cost") or {}).get("estimates_cny") or {}
        hard_cap = _first_number(est, "hard_cap_total_cny")
        reserve = _first_number(est, "per_call_worst_case_reservation_busy")
        attempt_cap = _int_or(sched.get("global_attempt_cap"), "value", 960)
        if hard_cap is None or reserve is None:
            raise LiveGateError("hard_cap / per-call reserve not numeric — config not confirmed")
        self.max_retries = _int_or(sched.get("retry_policy"),
                                   "max_technical_retries_per_target", 1)
        self.ledger = BudgetLedger(os.path.join(self.root, "ledger"), hard_cap,
                                   attempt_cap, reserve,
                                   max_transfers_per_target=1 + self.max_retries)
        self.cache = ResponseCache(os.path.join(self.root, "cache"))
        self.checkpoint = Checkpoint(os.path.join(self.root, "CHECKPOINT.json"))
        self.archive = AttemptArchive(os.path.join(self.root, "attempts"))
        self.canonical_path = os.path.join(self.root, "RATINGS_CANONICAL.jsonl")
        self.timeout = _int_or(sched.get("per_request_timeout_seconds"), "value", 1800)
        self.concurrency = _int_or(sched.get("max_concurrency"), "value", 2)
        self.backoff = (sched.get("retry_policy") or {}).get("backoff_seconds") or {}
        self._canon_lock = threading.Lock()
        self.quarantine_path = os.path.join(self.root, "QUARANTINE_DUAL_RESULTS.jsonl")
        # R1.2 (F2R11-P1-02): repair the canonical file BEFORE anything reads
        # it — binary-safe: torn tail (incl. mid-UTF-8) preserved as evidence
        # and removed from the active file; mid-file damage quarantined; a
        # complete final line missing its newline is KEPT (normalized).
        self.canonical_repair_report = repair_canonical(self.canonical_path,
                                                        repair_log_dir=self.root)
        # R1.2 (F2R11-P1-01): the ORIGINAL PROVIDER ARCHIVE is the primary
        # recovery source; index it once at startup.
        self.archive_index = self.archive.index_by_slot()
        # R1.1 (F2R1-P1-02): index existing canonical OK records at startup so
        # a crash between canonical write and checkpoint commit can be
        # completed IDEMPOTENTLY (never a second OK record)
        self._ok_index = {}   # uid → {"transfer_id", "response_sha256", "record"}
        self._quarantined_slots = set()
        if os.path.exists(self.canonical_path):
            prior, problems = load_canonical_jsonl(self.canonical_path)
            if problems:
                # post-repair this must be empty; if not, quarantine loudly —
                # never silently skip damaged lines
                self._quarantine_dual("<canonical-load>", None, None,
                                      f"UNPARSEABLE_LINES_AFTER_REPAIR:{problems[:3]}")
            for rec in prior:
                if rec.get("system_run_status") == "OK":
                    uid0 = rec.get("b_slot_uid")
                    prev0 = self._ok_index.get(uid0)
                    if prev0 and prev0["response_sha256"] != rec.get("response_sha256"):
                        # TRUE dual result: quarantine both refs, block the
                        # slot — never pick a side, never re-transfer
                        self._quarantine_dual(uid0, prev0["record"], rec,
                                              "PREEXISTING_DUAL_OK_AT_STARTUP")
                        self._ok_index.pop(uid0, None)
                        self._quarantined_slots.add(uid0)
                    elif uid0 not in self._quarantined_slots:
                        self._ok_index[uid0] = {
                            "transfer_id": rec.get("transfer_id"),
                            "response_sha256": rec.get("response_sha256"),
                            "record": rec}
        self.stop_all = threading.Event()

        # --- F2-P1-04: bind FULL run identity before any dedup/commit, and
        # reconcile possibly-billed inflight reservations from a dead process
        ci = cfg.get("content_identity") or {}
        self.run_identity = {
            "run_id": self.run_id,
            "config_sha256": cfg.get("_config_sha256") or "UNBOUND",
            "schema_sha256": sha256_bytes(canonical_json(schema).encode("utf-8")),
            "system_prompt_sha256": ci.get("system_prompt_sha256", "UNBOUND"),
            "item_template_sha256": ci.get("item_template_sha256", "UNBOUND"),
            "f0_manifest_sha256": ci.get("f0_input_baseline_manifest_sha256", "UNBOUND"),
            "b480_index_sha256": ci.get("b480_answer_index_sha256", "UNBOUND"),
            "evidence_identity_sha256": evidence_identity_sha256,
        }
        self.checkpoint.set_run_identity(self.run_identity)
        self.reconciled_inflight = self.ledger.reconcile_on_startup()

    # -- public entry --
    def run_items(self, item_payloads: list, batch_index: int = 0) -> dict:
        results = []
        with ThreadPoolExecutor(max_workers=max(1, self.concurrency)) as ex:
            futs = {ex.submit(self.process_item, it, batch_index): it for it in item_payloads}
            for fut, it in futs.items():
                results.append(fut.result())
        ok = sum(1 for r in results if r["system_run_status"] == "OK")
        return {"run_id": self.run_id, "batch_index": batch_index,
                "n_items": len(results), "n_ok": ok,
                "n_failed": len(results) - ok, "results": results,
                "reconciled_inflight_on_startup": self.reconciled_inflight,
                "ledger": self.ledger.snapshot()}

    def process_item(self, item: dict, batch_index: int) -> dict:
        uid = item["b_slot_uid"]
        anon = item["anonymous_item_id"]
        if uid in self._quarantined_slots:
            return {"b_slot_uid": uid, "anonymous_item_id": anon,
                    "system_run_status": "FAILED_DUAL_RESULT_QUARANTINED",
                    "detail": "preexisting contradictory OK records quarantined at startup; human review required"}
        digest = Checkpoint.slot_identity_digest(
            item, self.run_identity["config_sha256"], self.run_identity["schema_sha256"])
        # 1) identity-verified dedup (F2-P1-04: never return an old OK under a
        #    changed evidence/config/run identity)
        try:
            prev = self.checkpoint.committed_slot(uid, identity_digest=digest)
        except IdentityDriftError as e:
            self._write_canonical(item, f"{self.run_id}#{uid}#DRIFT", -1, None, None,
                                  "FAILED_INPUT_IDENTITY_MISMATCH", None,
                                  {"detail": str(e)})
            return {"b_slot_uid": uid, "anonymous_item_id": anon,
                    "system_run_status": "FAILED_INPUT_IDENTITY_MISMATCH",
                    "detail": str(e)}
        if prev and prev.get("validation_status") == "VALID":
            return {"b_slot_uid": uid, "anonymous_item_id": anon,
                    "system_run_status": "OK", "deduped": True,
                    "transfer_id": prev["transfer_id"]}
        # 1b) R1.1 crash-window recovery (F2R1-P1-02 repro A): an OK canonical
        #     record exists but the checkpoint commit never landed. Verify
        #     identity + original archive + revalidate under the CURRENT
        #     schema/context, then complete the commit IDEMPOTENTLY — never a
        #     second OK record, never a new transfer.
        rec_ok = self._ok_index.get(uid)
        if rec_ok is not None:
            rec = rec_ok["record"]
            same_identity = (rec.get("run_identity", {}).get("config_sha256")
                             == self.run_identity["config_sha256"]
                             and rec.get("run_identity", {}).get("schema_sha256")
                             == self.run_identity["schema_sha256"]
                             and rec.get("run_identity", {}).get("evidence_identity_sha256")
                             == self.run_identity["evidence_identity_sha256"]
                             and rec.get("answer_sha256") == item["identity_echo"]["answer_sha256"])
            tid = rec.get("transfer_id") or ""
            archive_ok = os.path.exists(os.path.join(
                self.root, "attempts", tid.replace("/", "_").replace("#", "__")))
            rating = rec.get("rating")
            revalid = False
            if same_identity and archive_ok and isinstance(rating, dict):
                revalid = rv.validate_rating(rating, item["validation_context"],
                                             self.schema).valid
            if same_identity and archive_ok and revalid:
                self.checkpoint.commit_slot(uid, tid, "VALID",
                                            self.ledger.snapshot(), batch_index,
                                            identity_digest=digest)
                return {"b_slot_uid": uid, "anonymous_item_id": anon,
                        "system_run_status": "OK", "deduped": True,
                        "recovered_after_crash": True, "transfer_id": tid}
            # inconsistent recovery material → quarantine, never auto-choose
            self._quarantine_dual(uid, rec, None,
                                  "RECOVERY_INCONSISTENT"
                                  f"(same_identity={same_identity},archive_ok={archive_ok},"
                                  f"revalid={revalid})")
            self._ok_index.pop(uid, None)
            return {"b_slot_uid": uid, "anonymous_item_id": anon,
                    "system_run_status": "FAILED_DUAL_RESULT_QUARANTINED",
                    "detail": "uncommitted OK record failed recovery verification; quarantined for review"}
        # 1c) R1.2 ARCHIVE-FIRST recovery (F2R11-P1-01): a complete, valid
        #     provider response may already be archived (original wire +
        #     settled usage) even though cache/canonical/checkpoint never got
        #     written. Replay it through the CURRENT parser/validator under
        #     full identity checks and complete the derived layers idempotently
        #     — a valid archived rating is NEVER re-sampled.
        arch = self._recover_from_archive(item, digest, batch_index)
        if arch is not None:
            return arch
        # 2) cache lookup with revalidation against current schema+context
        key = rb.cache_key(item, self.cfg)

        def _revalidate(entry):
            try:
                rating = rv.parse(entry["raw_response_text"])
            except ValueError:
                return False
            return rv.validate_rating(rating, item, self.schema).valid

        cached = self.cache.get_valid(key, revalidate=_revalidate)
        if cached is not None:
            served = self._cache_serve(item, cached, batch_index, digest)
            if not served:
                return {"b_slot_uid": uid, "anonymous_item_id": anon,
                        "system_run_status": "FAILED_DUAL_RESULT_QUARANTINED",
                        "error_kind": "DUAL_RESULT_QUARANTINED"}
            return {"b_slot_uid": uid, "anonymous_item_id": anon,
                    "system_run_status": "OK", "cache_hit": True}
        # 3) build request (gate enforced for live; mock bypasses confirmation
        #    but never touches the network)
        require_confirmed = self._is_live()
        request = rb.build_request_body(item, self.cfg,
                                        load_confirmation(self.cfg) if require_confirmed else None,
                                        require_confirmed=require_confirmed)
        # 4) attempt loop with PERSISTENT per-slot quota (restart-safe)
        attempt = 0
        last = None
        while attempt <= self.max_retries and not self.stop_all.is_set():
            if self.ledger.slot_attempts_used(uid) >= 1 + self.max_retries:
                last = {"system_run_status": "FAILED_HTTP_429_EXHAUSTED",
                        "error_kind": "SLOT_QUOTA_PERSISTENT"}
                break
            transfer_id = self._next_transfer_id(uid, attempt)
            outcome = self._one_transfer(item, request, transfer_id, attempt,
                                         batch_index, digest)
            last = outcome
            if outcome["system_run_status"] == "OK":
                return {"b_slot_uid": uid, "anonymous_item_id": anon,
                        "system_run_status": "OK", "transfer_id": transfer_id,
                        "attempts_used": attempt + 1}
            kind = outcome.get("error_kind")
            if kind in ("AUTH", "MODEL_DRIFT"):
                if kind == "AUTH":
                    self.ledger.stop_branch("HTTP_401_403_ON_SCORING_ENDPOINT")
                self.stop_all.set()
                return {"b_slot_uid": uid, "anonymous_item_id": anon,
                        "system_run_status": outcome["system_run_status"],
                        "error_kind": kind,
                        "transfer_id": transfer_id}
            if kind in ("BUDGET_STOP", "ATTEMPT_CAP", "SLOT_QUOTA_PERSISTENT"):
                self.stop_all.set()
                return {"b_slot_uid": uid, "anonymous_item_id": anon,
                        "system_run_status": outcome["system_run_status"],
                        "transfer_id": transfer_id}
            retryable = (kind in RETRYABLE_KINDS) or (
                isinstance(kind, str)
                and any(kind.startswith(p) for p in RETRYABLE_KIND_PREFIXES))
            if not retryable or attempt == self.max_retries:
                break
            if outcome.get("system_run_status") == "UNKNOWN_INFLIGHT" and \
                    self.ledger.slot_attempts_used(uid) >= 1 + self.max_retries:
                break
            wait = self.backoff.get(kind, 0) or 0
            if wait:
                time.sleep(min(wait, 0.2) if isinstance(self.transport, MockTransport) else wait)
            # neutral technical note; per-attempt body → per-attempt reserve
            request = dict(request)
            request["body"] = dict(request["body"])
            request["body"]["messages"] = [
                m if m["role"] != "user" else
                {"role": "user", "content": m["content"] + NEUTRAL_RETRY_NOTE}
                for m in request["body"]["messages"]]
            request["approx_input_tokens"] = rb._approx_token_count(request["body"]["messages"])
            attempt += 1
        status = (last or {}).get("system_run_status", "NOT_RUN")
        return {"b_slot_uid": uid, "anonymous_item_id": anon,
                "system_run_status": status, "attempts_used": attempt + 1,
                "error_kind": (last or {}).get("error_kind")}

    def _is_live(self) -> bool:
        from f2r12_transport import LiveTransport
        return isinstance(self.transport, LiveTransport) and self.transport._session is not None \
            and not hasattr(self.transport._session, "posted")

    def _next_transfer_id(self, uid: str, attempt: int) -> str:
        # R1.1 (F2R1-P1-02 repro B): sequence comes from the PERSISTENT ledger
        # counter — a restarted process can never re-mint an old transfer_id
        n = self.ledger.next_transfer_seq()
        return f"{self.run_id}#{uid}#a{attempt}#t{n}"

    def _quarantine_dual(self, uid: str, rec_a, rec_b, reason: str):
        """True dual/contradictory results are isolated for review — never
        silently resolved by picking one (repair card §3)."""
        entry = {"b_slot_uid": uid, "reason": reason, "utc": utc_now_iso(),
                 "record_a": {"transfer_id": (rec_a or {}).get("transfer_id"),
                              "response_sha256": (rec_a or {}).get("response_sha256"),
                              "system_run_status": (rec_a or {}).get("system_run_status")},
                 "record_b": ({"transfer_id": rec_b.get("transfer_id"),
                               "response_sha256": rec_b.get("response_sha256"),
                               "system_run_status": rec_b.get("system_run_status")}
                              if rec_b else None)}
        with self._canon_lock:
            with open(self.quarantine_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False, allow_nan=False) + "\n")

    def _one_transfer(self, item, request, transfer_id, attempt, batch_index,
                      digest) -> dict:
        uid = item["b_slot_uid"]
        # per-attempt reserve from the ACTUAL current body size (retry bodies
        # carry the neutral note → slightly larger; audited F2-P1-03)
        max_out = _int_or(self.cfg.get("model_parameters"), "max_tokens", 65536)
        per_reserve = (request["approx_input_tokens"] * self.price_in
                       + max_out * self.price_out) / 1_000_000.0
        try:
            self.ledger.reserve(transfer_id, uid, reserve_cny=per_reserve)
        except BudgetStop as e:
            self._write_canonical(item, transfer_id, attempt, None, None,
                                  "FAILED_BUDGET_STOP", None, {"detail": str(e)})
            return {"system_run_status": "FAILED_BUDGET_STOP", "error_kind": "BUDGET_STOP",
                    "detail": str(e)}
        except AttemptCapReached as e:
            self._write_canonical(item, transfer_id, attempt, None, None,
                                  "FAILED_HTTP_429_EXHAUSTED", None, {"detail": str(e)})
            return {"system_run_status": "FAILED_HTTP_429_EXHAUSTED",
                    "error_kind": "ATTEMPT_CAP", "detail": str(e)}
        except SlotAttemptQuotaExceeded as e:
            self._write_canonical(item, transfer_id, attempt, None, None,
                                  "FAILED_HTTP_429_EXHAUSTED", None, {"detail": str(e)})
            return {"system_run_status": "FAILED_HTTP_429_EXHAUSTED",
                    "error_kind": "SLOT_QUOTA_PERSISTENT", "detail": str(e)}
        except AuthStop as e:
            self._write_canonical(item, transfer_id, attempt, None, None,
                                  "FAILED_HTTP_AUTH_401_403", None, {"detail": str(e)})
            return {"system_run_status": "FAILED_HTTP_AUTH_401_403", "error_kind": "AUTH",
                    "detail": str(e)}

        wire = self.transport.send(request, self.timeout)
        wire = dict(wire)
        # normalize legacy mock fields
        if wire.get("raw_response_bytes") is None and wire.get("raw_text") is not None:
            wire["raw_response_bytes"] = wire["raw_text"].encode("utf-8")
        request_body_bytes = json.dumps(request["body"], ensure_ascii=False).encode("utf-8")
        # FULL wire archive FIRST (originals preserved regardless of outcome)
        self.archive.store(transfer_id, wire, request_body_bytes,
                           request["item_identity"],
                           run_identity=self.run_identity,
                           attempt_index=attempt)
        self.checkpoint.record_slot_attempt(uid, transfer_id,
                                            wire.get("error_kind") or "RESPONSE_RECEIVED")

        # --- transport-level settlement BEFORE rating validity (F2-P1-03) ---
        self.ledger.settle_by_transport(transfer_id, {
            "usage": wire.get("usage"),
            "http_status": wire.get("http_status"),
            "response_received": wire.get("raw_response_bytes") is not None,
            "may_have_billed": wire.get("may_have_billed", False),
            "error_kind": wire.get("error_kind"),
        }, self.price_in, self.price_out)

        kind = wire.get("error_kind")
        # transport-level classification (billing already settled above):
        # interrupted/unknown streams are UNKNOWN_INFLIGHT (possibly billed,
        # content unreliable); clean refusals map to their frozen statuses.
        transport_status = {
            "AUTH": "FAILED_HTTP_AUTH_401_403",
            "RATE_LIMIT": "FAILED_HTTP_429_EXHAUSTED",
            "SERVER_5XX": "FAILED_HTTP_5XX_EXHAUSTED",
            "TIMEOUT": "UNKNOWN_INFLIGHT",
            "READ_ERROR": "UNKNOWN_INFLIGHT",
            "NO_TERMINAL_MARKER": "UNKNOWN_INFLIGHT",
            "CHUNK_PARSE_ERRORS": "UNKNOWN_INFLIGHT",
            "SSE_PARSE_EXCEPTION": "UNKNOWN_INFLIGHT",
            "INVALID_JSON": "FAILED_INVALID_JSON",
            "NO_CONTENT_BLOCK": "FAILED_INVALID_JSON",
        }.get(kind)
        if transport_status is None and kind is not None:
            transport_status = ("UNKNOWN_INFLIGHT" if wire.get("may_have_billed")
                                else "FAILED_HTTP_OTHER")
        if transport_status is not None:
            self._write_canonical(item, transfer_id, attempt, None, None,
                                  transport_status, wire.get("usage"), wire)
            return {"system_run_status": transport_status, "error_kind": kind}

        content = wire.get("content_text")
        if content is None:
            content = wire.get("raw_text")
        if content is None:
            raw_b = wire.get("raw_response_bytes")
            content = raw_b.decode("utf-8", "replace") if raw_b else None
        if content is None:
            self._write_canonical(item, transfer_id, attempt, None, None,
                                  "FAILED_INVALID_JSON", wire.get("usage"), wire)
            return {"system_run_status": "FAILED_INVALID_JSON", "error_kind": kind or "NO_CONTENT"}

        # model identity drift (no silent switch) — billing already settled
        model_expected = self.cfg["scoring_ai"]["recommended"]["exact_model_id"]
        model_returned = wire.get("model_returned")
        if model_returned is not None and model_returned != model_expected:
            self.stop_all.set()
            self._write_canonical(item, transfer_id, attempt, None, None,
                                  "FAILED_MODEL_DRIFT", wire.get("usage"), wire)
            return {"system_run_status": "FAILED_MODEL_DRIFT", "error_kind": "MODEL_DRIFT",
                    "detail": f"returned model {model_returned!r} != frozen {model_expected!r}"}

        # parse + validate (rating validity NEVER affects billing above)
        try:
            rating = rv.parse(content)
        except ValueError as e:
            self._write_canonical(item, transfer_id, attempt, None, None,
                                  "FAILED_INVALID_JSON", wire.get("usage"), wire)
            return {"system_run_status": "FAILED_INVALID_JSON", "error_kind": "INVALID_JSON",
                    "detail": str(e)[:200]}
        vres = rv.validate_rating(rating, item, self.schema)
        if not vres.valid:
            self._write_canonical(item, transfer_id, attempt, rating, vres,
                                  "FAILED_SCHEMA_VALIDATION", wire.get("usage"), wire)
            return {"system_run_status": "FAILED_SCHEMA_VALIDATION",
                    "error_kind": "SCHEMA_FAIL", "n_errors": len(vres.errors)}
        # success
        self.cache.put(rb.cache_key(item, self.cfg), content, wire.get("usage"),
                       "VALID", request["item_identity"], transfer_id=transfer_id)
        wrote = self._write_canonical(item, transfer_id, attempt, rating, vres, "OK",
                                      wire.get("usage"), wire)
        if wrote == "QUARANTINED_DUAL":
            return {"system_run_status": "FAILED_DUAL_RESULT_QUARANTINED",
                    "error_kind": "DUAL_RESULT_QUARANTINED"}
        # WRITTEN or SKIPPED_IDEMPOTENT → commit (idempotent under lock)
        self.checkpoint.commit_slot(uid, transfer_id, "VALID",
                                    self.ledger.snapshot(), batch_index,
                                    identity_digest=digest)
        cost = usage_cost_cny(wire.get("usage"), self.price_in, self.price_out)
        return {"system_run_status": "OK", "error_kind": None, "cost_cny": cost}

    def _recover_from_archive(self, item, digest, batch_index):
        """R1.2 (F2R11-P1-01): the ORIGINAL PROVIDER ARCHIVE is the primary
        recovery source. For each archived attempt of this slot, verify the
        FULL chain — request body sha, raw wire sha, meta completeness, run
        identity, item identity echo, transport-level success — then REPLAY
        the raw bytes through the current parser and revalidate under the
        current schema/context. Exactly one recoverable valid result →
        complete cache/canonical/checkpoint idempotently under the ORIGINAL
        transfer id (never a -CACHED pseudonym), with ledger reconciliation
        (settled → no double bill; inflight → settle from archived usage;
        unknown reserve → resolve only with verifiable archived usage).
        Multiple DIFFERENT recoverable results → quarantine, never pick one.
        Unrecoverable archives (incomplete/invalid/identity-mismatched) stay
        untouched as failure history; normal frozen-quota logic proceeds."""
        uid = item["b_slot_uid"]
        anon = item["anonymous_item_id"]
        metas = self.archive_index.get(uid) or []
        if not metas:
            return None
        from f2r12_transport import (parse_sse_bytes, parse_non_stream_bytes,
                                     new_stream_state)
        recoverable = []
        for meta in metas:
            try:
                d = meta.get("_dir")
                raw_p = os.path.join(d, "response_raw.bin")
                req_p = os.path.join(d, "request_body.json")
                if not (os.path.exists(raw_p) and os.path.exists(req_p)):
                    continue
                raw = open(raw_p, "rb").read()
                req_bytes = open(req_p, "rb").read()
                if sha256_bytes(raw) != meta.get("response_raw_sha256"):
                    continue   # archived wire integrity broken → not a source
                if sha256_bytes(req_bytes) != meta.get("request_body_sha256"):
                    continue
                if meta.get("http_status") != 200 or meta.get("error_kind") is not None:
                    continue   # transport-level failure: nothing to recover
                if meta.get("stream_status") != "COMPLETE":
                    continue   # incomplete wire is never forced into a success
                # run identity must match CURRENT frozen versions (run_id may
                # differ across restarts; content identities may not).
                # R1.2.1 HOTFIX (F2 R1.2 reaudit §一): the seven-key comparison
                # is ONE whole-candidate gate — any mismatched OR missing key
                # rejects THIS ARCHIVE (continue targets the outer candidate
                # loop). The R1.2 code had `continue` inside the key loop,
                # which skipped only to the next key and never rejected the
                # candidate. Unknown/absent run_identity never counts as a
                # match; values are never backfilled from the current config.
                arch_ri = meta.get("run_identity") or {}
                identity_keys = ("config_sha256", "schema_sha256",
                                 "system_prompt_sha256", "item_template_sha256",
                                 "f0_manifest_sha256", "b480_index_sha256",
                                 "evidence_identity_sha256")
                if any(arch_ri.get(k) != self.run_identity.get(k)
                       for k in identity_keys):
                    continue   # ← outer candidate loop: this archive is refused
                req_ident = meta.get("request_identity") or {}
                if req_ident.get("user_message_sha256") != item.get("user_message_sha256"):
                    continue
                if (req_ident.get("identity_echo") or {}) != item.get("identity_echo"):
                    continue
                # model drift: a drifted response was already a failure; a
                # missing provider model field stays NOT_PROVIDED (disclosed,
                # never backfilled) and remains recoverable per P2-02 policy
                model_expected = self.cfg["scoring_ai"]["recommended"]["exact_model_id"]
                mr = meta.get("model_returned")
                if mr is not None and mr != model_expected:
                    continue
                # replay the ORIGINAL bytes through the CURRENT parser
                req_body = json.loads(req_bytes.decode("utf-8"))
                state = new_stream_state()
                if req_body.get("stream"):
                    content = parse_sse_bytes(raw, state)
                    if state["chunk_parse_errors"] or not state["terminal_seen"]:
                        continue
                else:
                    try:
                        content = parse_non_stream_bytes(raw, state)
                    except ValueError:
                        continue
                if not content:
                    continue
                rating = rv.parse(content)
                vres = rv.validate_rating(rating, item, self.schema)
                if not vres.valid:
                    continue   # schema-invalid archives are failure history
                recoverable.append((meta, content, rating, vres))
            except (ValueError, OSError, KeyError, UnicodeDecodeError):
                continue
        if not recoverable:
            return None
        distinct = {}
        for meta, content, rating, vres in recoverable:
            distinct.setdefault(sha256_bytes(content.encode("utf-8")),
                                (meta, content, rating, vres))
        if len(distinct) > 1:
            first = next(iter(distinct.values()))[0]
            second = list(distinct.values())[1][0]
            self._quarantine_dual(uid, {"transfer_id": first.get("transfer_id"),
                                        "response_sha256": first.get("response_raw_sha256")},
                                  {"transfer_id": second.get("transfer_id"),
                                   "response_sha256": second.get("response_raw_sha256")},
                                  "MULTIPLE_VALID_ARCHIVED_RESULTS")
            self._quarantined_slots.add(uid)
            return {"b_slot_uid": uid, "anonymous_item_id": anon,
                    "system_run_status": "FAILED_DUAL_RESULT_QUARANTINED",
                    "detail": "multiple different valid archived results; quarantined, no side picked"}
        meta, content, rating, vres = next(iter(distinct.values()))
        transfer_id = meta["transfer_id"]
        # ledger reconciliation — idempotent, never a double bill, never a
        # guessed cost: unknown reserves resolve ONLY via archived usage
        wire_for_settle = {"usage": meta.get("usage"), "http_status": 200,
                           "response_received": True, "may_have_billed": False,
                           "error_kind": None}
        try:
            self.ledger.settle_inflight_from_archive(transfer_id, wire_for_settle,
                                                     self.price_in, self.price_out)
        except KeyError:
            pass  # transfer never reserved here (foreign root) — leave accounting untouched
        # complete the derived layers under the ORIGINAL transfer identity
        self.cache.put(rb.cache_key(item, self.cfg), content, meta.get("usage"),
                       "VALID", meta.get("request_identity") or {},
                       transfer_id=transfer_id)
        wire = dict(meta)
        wire["recovery_source"] = "ARCHIVE_REPLAY"
        wrote = self._write_canonical(item, transfer_id,
                                      meta.get("attempt_index", 0), rating, vres,
                                      "OK", meta.get("usage"), wire)
        if wrote == "QUARANTINED_DUAL":
            return {"b_slot_uid": uid, "anonymous_item_id": anon,
                    "system_run_status": "FAILED_DUAL_RESULT_QUARANTINED",
                    "error_kind": "DUAL_RESULT_QUARANTINED"}
        self.checkpoint.commit_slot(uid, transfer_id, "VALID",
                                    self.ledger.snapshot(), batch_index,
                                    identity_digest=digest)
        return {"b_slot_uid": uid, "anonymous_item_id": anon,
                "system_run_status": "OK", "recovered_from_archive": True,
                "transfer_id": transfer_id, "new_transfers": 0}

    def _cache_serve(self, item, cached, batch_index, digest):
        # R1.2: the cache is a DERIVED accelerator — it must reference the
        # real provider archive and keep the ORIGINAL transfer id (no
        # -CACHED pseudonym overwriting the original identity).
        transfer_id = cached.get("transfer_id")
        archive_dir = None
        if transfer_id:
            candidate = os.path.join(
                self.root, "attempts",
                transfer_id.replace("/", "_").replace("#", "__"))
            if os.path.isdir(candidate):
                archive_dir = candidate
        if archive_dir is None:
            # cache entry without provider archive: provenance broken — do not
            # serve it as a transfer, do not fabricate identity; log and fall
            # through to quota logic (or quarantine upstream if canonical OK)
            self._quarantine_dual(item["b_slot_uid"], None,
                                  {"transfer_id": transfer_id,
                                   "response_sha256": cached.get("raw_response_sha256")},
                                  "CACHE_ENTRY_WITHOUT_PROVIDER_ARCHIVE")
            return False
        raw = cached["raw_response_text"]
        rating = rv.parse(raw)
        vres = rv.validate_rating(rating, item, self.schema)
        # R1.1: a cache hit must NEVER create a second OK canonical record
        # when an uncommitted OK from an interrupted run already exists —
        # _write_canonical's guard handles idempotency/quarantine.
        wrote = self._write_canonical(item, transfer_id, 0, rating, vres, "OK",
                                      cached.get("usage"),
                                      {"recovery_source": "CACHE_DERIVED",
                                       "archive_dir": archive_dir})
        if wrote == "QUARANTINED_DUAL":
            return False
        self.checkpoint.commit_slot(item["b_slot_uid"], transfer_id, "VALID",
                                    self.ledger.snapshot(), batch_index,
                                    identity_digest=digest)
        return True

    def _write_canonical(self, item, transfer_id, attempt, rating, vres,
                         system_run_status, usage, wire):
        """Append one canonical record. R1.1 guard (F2R1-P1-02): at most ONE
        OK record per slot —
          - same transfer_id + same response sha as an existing OK record →
            idempotent replay: SKIP the write (recovery completion, not a
            second result);
          - a DIFFERENT OK result for the same slot → quarantine both refs,
            refuse the write, never pick a side.
        Returns "WRITTEN" | "SKIPPED_IDEMPOTENT" | "QUARANTINED_DUAL"."""
        uid = item["b_slot_uid"]
        response_sha = (sha256_bytes(json.dumps(rating, ensure_ascii=False,
                                                sort_keys=True).encode("utf-8"))
                        if rating else None)
        if system_run_status == "OK":
            with self._canon_lock:
                existing = self._ok_index.get(uid)
                if existing is not None:
                    if (existing["transfer_id"] == transfer_id
                            and existing["response_sha256"] == response_sha):
                        return "SKIPPED_IDEMPOTENT"
                    self._quarantine_dual(uid, existing["record"],
                                          {"transfer_id": transfer_id,
                                           "response_sha256": response_sha,
                                           "system_run_status": "OK"},
                                          "SECOND_DIFFERENT_OK_RESULT")
                    return "QUARANTINED_DUAL"
        ie = item["identity_echo"]
        wire = wire if isinstance(wire, dict) else {}
        model_returned = wire.get("model_returned")
        model_frozen = (self.cfg.get("scoring_ai") or {}).get("recommended", {}).get("exact_model_id")
        if model_returned is None:
            model_verification = "NOT_PROVIDED_BY_PROVIDER"   # P2-02: unknown stays unknown
        elif model_returned == model_frozen:
            model_verification = "VERIFIED_MATCH"
        else:
            model_verification = "DRIFT"
        rec = {
            "scoring_run_id": self.run_id,
            "run_identity": self.run_identity,
            "anonymous_item_id": item["anonymous_item_id"],
            "batch": item["batch"],
            "case_id": item["case_id"],
            "b_slot_uid": uid,
            "input_manifest_sha": ie["input_manifest_sha"],
            "question_rendered_prompt_sha256": ie["question_rendered_prompt_sha256"],
            "answer_sha256": ie["answer_sha256"],
            "rubric_text_sha256": ie["rubric_text_sha256"],
            "gold_slice_manifest_sha256": ie["gold_slice_manifest_sha256"],
            "scope_rows_sha256": ie["scope_rows_sha256"],
            "evidence_snapshot_sha": ie["evidence_snapshot_sha"],
            "evidence_case_slice_sha256": ie.get("evidence_case_slice_sha256"),
            "system_prompt_sha256": ie["system_prompt_sha256"],
            "item_template_sha256": ie["item_template_sha256"],
            "rating_schema_sha256": sha256_bytes(canonical_json(self.schema).encode("utf-8")),
            "run_config_sha256": self.cfg.get("_config_sha256"),
            "transfer_id": transfer_id,
            "request_id": wire.get("provider_request_id"),
            "provider": (self.cfg.get("scoring_ai") or {}).get("recommended", {}).get("provider"),
            "model_frozen": model_frozen,
            "model_returned": model_returned,
            "model_identity": wire.get("model_identity"),
            "model_identity_verification": model_verification,
            "http_status": wire.get("http_status"),
            "stream_status": wire.get("stream_status"),
            "finish_reason": wire.get("finish_reason"),
            "read_error": wire.get("read_error"),
            "raw_truncated": wire.get("raw_truncated", False),
            "raw_response_sha256": (sha256_bytes(wire["raw_response_bytes"])
                                    if wire.get("raw_response_bytes") else None),
            "attempt_index": attempt,
            "utc": utc_now_iso(),
            "usage": usage,
            "cost_cny": usage_cost_cny(usage, self.price_in, self.price_out),
            "response_sha256": response_sha,
            "system_run_status": system_run_status,
            "recovery_source": wire.get("recovery_source"),
            "validation": vres.to_dict() if vres is not None else None,
            "rating": rating if system_run_status == "OK" else None,
            "rating_raw_preserved_on_failure": system_run_status != "OK",
            "rater_type": "AI",
        }
        # shared totals contract (F2-P1-05: MISSING participates; validator,
        # canonical and projection all use f2r12_common.totals_contract)
        if rating:
            tc = totals_contract(rating.get("dimensions") or {})
            if tc["status"] == "COMPARABLE":
                rec["recomputed_weighted_total"] = tc["weighted_total"]
                rec["recomputed_scientific_subscore"] = tc["scientific_subscore"]
                rec["model_weighted_total"] = rating.get("weighted_total")
                rec["model_scientific_subscore"] = rating.get("scientific_subscore")
                rec["total_correction_applied"] = (
                    not isinstance(rating.get("weighted_total"), (int, float))
                    or abs(rating["weighted_total"] - tc["weighted_total"]) > 0.01)
            else:
                rec["recomputed_weighted_total"] = "NOT_COMPARABLE"
                rec["recomputed_scientific_subscore"] = "NOT_COMPARABLE"
                rec["total_status_contract"] = tc["status"]
        with self._canon_lock:
            with open(self.canonical_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False, allow_nan=False) + "\n")
            if system_run_status == "OK":
                self._ok_index[uid] = {"transfer_id": transfer_id,
                                       "response_sha256": response_sha,
                                       "record": rec}
        return "WRITTEN"


# ------------------------------------------------------------------- helpers

def _confirmed_prices(cfg: dict):
    """Extract confirmed busy prices from the frozen config. Returns None when
    unconfirmed/pending → live construction refused (no CLI bypass)."""
    pb = ((cfg.get("cost") or {}).get("price_basis") or {})
    pin, pout = pb.get("input_busy_cny_per_1M"), pb.get("output_busy_cny_per_1M")
    if (isinstance(pin, (int, float)) and not isinstance(pin, bool)
            and isinstance(pout, (int, float)) and not isinstance(pout, bool)
            and str((cfg.get("cost") or {}).get("price_status", "")).startswith("CONFIRMED")):
        return float(pin), float(pout)
    return None


def _file_sha_or(d: dict, key: str) -> str:
    v = d.get(key)
    return v if isinstance(v, str) and len(v) == 64 else "UNBOUND"


def _int_or(d, key, default):
    v = d.get(key) if isinstance(d, dict) else None
    if isinstance(v, dict):
        v = v.get("value")
    return v if isinstance(v, int) and not isinstance(v, bool) else default


def _first_number(d, key):
    v = d.get(key)
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    return None


# ------------------------------------------------------------------ CLI main

def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["validate-config", "mock", "live"],
                    default="validate-config")
    ap.add_argument("--items-dir", default=None)
    ap.add_argument("--run-root", default=None)
    ap.add_argument("--mock-script", default=None)
    ap.add_argument(LIVE_FLAG, action="store_true")
    # NOTE: no --price-in/--price-out on the live path (audit F2-P1-03:
    # prices come only from the confirmed config). Mock runs use explicitly
    # labeled synthetic test prices via ScoringRunner(synthetic_test_prices=True).
    a = ap.parse_args(argv)

    cfg = rb.load_config()
    if a.mode == "validate-config":
        conf = load_confirmation(cfg)
        reasons = rb.config_gate(cfg, conf, require_confirmed=True)
        print(json.dumps({"mode": "validate-config",
                          "config_sha256": cfg.get("_config_sha256"),
                          "config_status": cfg.get("config_status"),
                          "live_gate_blocking_reasons": reasons,
                          "gate_open": not reasons}, ensure_ascii=False, indent=1))
        return 0
    if a.mode == "live":
        transport = build_live_transport(
            cfg, lambda c, flag, keyp: live_gate_reasons(c, load_confirmation(c), flag, keyp),
            a.i_confirm_live_paid_calls)
    else:
        script = json.load(open(a.mock_script, encoding="utf-8")) if a.mock_script else {}
        transport = MockTransport(script)

    items = []
    if a.items_dir:
        for name in sorted(os.listdir(a.items_dir)):
            if name.endswith(".json"):
                items.append(read_json(os.path.join(a.items_dir, name)))
    est = (cfg.get("cost") or {}).get("estimates_cny") or {}
    runner = ScoringRunner(
        cfg, a.run_root or os.path.join(str(F2_DIR), "logs", "mock_run"),
        transport, rv.load_schema(),
        price_in_per_1m=9.0, price_out_per_1m=27.0,
        synthetic_test_prices=(a.mode != "live"))
    summary = runner.run_items(items)
    print(json.dumps({k: v for k, v in summary.items() if k != "results"},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
