"""F2 R1 budget ledger (audit F2-P1-03 / F2-P1-04 fixes).

Changes over R0:
  - USAGE-FIRST settlement: a transfer is settled from the TRANSPORT outcome
    (usage / response received / may-have-billed) BEFORE and INDEPENDENT of
    whether the rating JSON parses or validates. A billable HTTP 200 with
    invalid JSON and usage {1000,100} at test prices 9/27 MUST book 0.0117 —
    R0 released it to 0. Malformed/negative/NaN usage on a received response
    is an UNKNOWN charge, never 0.
  - actual cost may exceed the reservation (real usage > heuristic estimate):
    commit the actual and log OVER_RESERVE_SETTLEMENT — the heuristic is an
    estimate with a documented stopping mechanism (hard cap over
    committed+inflight+unknown), NOT a claimed strict billing upper bound.
  - persistent PER-SLOT attempt counts (slot_attempts): the "first + 1
    technical retry" quota survives process restarts; reserve() refuses when
    the slot quota or the global attempt cap is exhausted.
  - reconcile_on_startup(): inflight reservations left by a dead process
    become UNKNOWN_INFLIGHT charges (possibly billed; never zeroed), with a
    RECONCILED_AFTER_RESTART ledger event — restart cannot erase exposure.
  - duplicate settlement / duplicate reserve of the same transfer is refused.
  - prices come ONLY from the frozen confirmed config at runtime; the ledger
    validates them per call (finite, >= 0). CLI overrides are not accepted.

Offline: pure local file accounting; no network.
"""
from __future__ import annotations

import errno
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import atomic_write_json, utc_now_iso, is_pure_int


class BudgetStop(Exception):
    pass


class AttemptCapReached(Exception):
    pass


class SlotAttemptQuotaExceeded(Exception):
    pass


class AuthStop(Exception):
    pass


def usage_cost_cny(usage, price_in_per_1m, price_out_per_1m):
    """Cost from a provider usage block. Returns None when usage is absent or
    malformed (missing/non-integer/negative/NaN/Inf) — caller MUST treat None
    as UNKNOWN (never 0). Prices validated finite and >= 0."""
    for p in (price_in_per_1m, price_out_per_1m):
        if not (isinstance(p, (int, float)) and not isinstance(p, bool)
                and math.isfinite(p) and p >= 0):
            raise ValueError(f"illegal price {p!r} (must be finite >= 0; "
                             "prices come only from the frozen confirmed config)")
    if not isinstance(usage, dict):
        return None
    pt = usage.get("prompt_tokens")
    ct = usage.get("completion_tokens")
    if not (is_pure_int(pt) and is_pure_int(ct)):
        return None
    if pt < 0 or ct < 0:
        return None
    cost = (pt * price_in_per_1m + ct * price_out_per_1m) / 1_000_000.0
    if not math.isfinite(cost) or cost < 0:
        return None
    return cost


class BudgetLedger:
    def __init__(self, root, hard_cap_cny: float, global_attempt_cap: int,
                 default_reserve_cny: float, max_transfers_per_target: int = 2):
        if not (isinstance(hard_cap_cny, (int, float)) and hard_cap_cny > 0):
            raise ValueError("hard_cap_cny must be a positive number from the confirmed config")
        self.root = str(root)
        os.makedirs(self.root, exist_ok=True)
        self.state_path = os.path.join(self.root, "BUDGET_STATE.json")
        self.log_path = os.path.join(self.root, "ATTEMPT_LEDGER.jsonl")
        self.lock_path = os.path.join(self.root, ".ledger.lock")
        self.hard_cap = hard_cap_cny
        self.attempt_cap = global_attempt_cap
        self.default_reserve = default_reserve_cny
        self.max_transfers_per_target = max_transfers_per_target
        if not os.path.exists(self.state_path):
            atomic_write_json(self.state_path, self._empty_state())

    def _empty_state(self):
        return {"committed_spend_cny": 0.0, "inflight": {}, "unknown_reserves": {},
                "attempts_used": 0, "slot_attempts": {}, "stopped": None,
                "settlements": [], "updated_utc": utc_now_iso()}

    # -- locking (single-writer transaction discipline) --
    def _lock(self):
        deadline = time.time() + 30
        while True:
            try:
                fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                if time.time() > deadline:
                    raise TimeoutError("ledger lock contention > 30s")
                try:
                    if time.time() - os.path.getmtime(self.lock_path) > 3600 * 2:
                        os.unlink(self.lock_path)  # stale lock from a dead process
                except OSError:
                    pass
                time.sleep(0.02)

    def _unlock(self):
        try:
            os.unlink(self.lock_path)
        except OSError:
            pass

    def _read(self):
        with open(self.state_path, encoding="utf-8") as f:
            return json.load(f)

    def _log(self, event: dict):
        event = dict(event)
        event["utc"] = utc_now_iso()
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")

    # -- startup reconciliation (restart-safe exposure) --
    def reconcile_on_startup(self) -> int:
        """Inflight entries from a previous (dead) process → unknown charges.
        Returns the number reconciled. Called once at runner init."""
        self._lock()
        try:
            st = self._read()
            n = 0
            for tid, entry in list(st["inflight"].items()):
                st["unknown_reserves"][tid] = {
                    "slot_uid": entry["slot_uid"], "reserve_cny": entry["reserve_cny"],
                    "reason": "RECONCILED_AFTER_RESTART_UNKNOWN_INFLIGHT"}
                del st["inflight"][tid]
                self._log({"event": "RECONCILED_AFTER_RESTART", "transfer_id": tid,
                           "kept_reserve_cny": entry["reserve_cny"]})
                n += 1
            if n:
                st["updated_utc"] = utc_now_iso()
                atomic_write_json(self.state_path, st)
            return n
        finally:
            self._unlock()

    # -- dispatch gate --
    def reserve(self, transfer_id: str, slot_uid: str, reserve_cny: float | None = None) -> float:
        reserve = self.default_reserve if reserve_cny is None else reserve_cny
        if not (isinstance(reserve, (int, float)) and not isinstance(reserve, bool)
                and math.isfinite(reserve) and reserve > 0):
            raise ValueError(f"reserve must be finite > 0 (unknown is never 0): {reserve!r}")
        self._lock()
        try:
            st = self._read()
            if st["stopped"]:
                raise AuthStop(f"ledger stopped: {st['stopped']}")
            if transfer_id in st["inflight"] or transfer_id in st.get("settlements", []):
                self._log({"event": "DUPLICATE_RESERVE_REFUSED", "transfer_id": transfer_id})
                raise KeyError(f"transfer {transfer_id} already reserved/settled — duplicate dispatch refused")
            if st["attempts_used"] >= self.attempt_cap:
                self._log({"event": "ATTEMPT_CAP_REFUSAL", "transfer_id": transfer_id,
                           "attempts_used": st["attempts_used"], "cap": self.attempt_cap})
                raise AttemptCapReached(f"attempts_used {st['attempts_used']} >= cap {self.attempt_cap}")
            slot_n = st["slot_attempts"].get(slot_uid, 0)
            if slot_n >= self.max_transfers_per_target:
                self._log({"event": "SLOT_QUOTA_REFUSAL", "transfer_id": transfer_id,
                           "slot_uid": slot_uid, "slot_attempts": slot_n,
                           "quota": self.max_transfers_per_target})
                raise SlotAttemptQuotaExceeded(
                    f"slot {slot_uid} already used {slot_n}/{self.max_transfers_per_target} transfers "
                    "(persistent quota; restart does not reset it)")
            inflight_sum = sum(v["reserve_cny"] for v in st["inflight"].values())
            unknown_sum = sum(v["reserve_cny"] for v in st["unknown_reserves"].values())
            projected = st["committed_spend_cny"] + inflight_sum + unknown_sum + reserve
            if projected > self.hard_cap + 1e-9:
                self._log({"event": "BUDGET_STOP_REFUSAL", "transfer_id": transfer_id,
                           "committed": st["committed_spend_cny"], "inflight": inflight_sum,
                           "unknown": unknown_sum, "reserve": reserve,
                           "projected": projected, "hard_cap": self.hard_cap})
                raise BudgetStop(
                    f"projected {projected:.4f} > hard_cap {self.hard_cap:.4f} "
                    f"(committed={st['committed_spend_cny']:.4f}, inflight={inflight_sum:.4f}, "
                    f"unknown={unknown_sum:.4f}, this_reserve={reserve:.4f})")
            st["inflight"][transfer_id] = {"slot_uid": slot_uid, "reserve_cny": reserve,
                                           "started_utc": utc_now_iso()}
            st["attempts_used"] += 1
            st["slot_attempts"][slot_uid] = slot_n + 1
            st["updated_utc"] = utc_now_iso()
            atomic_write_json(self.state_path, st)
            self._log({"event": "RESERVE", "transfer_id": transfer_id, "slot_uid": slot_uid,
                       "reserve_cny": reserve, "attempts_used": st["attempts_used"],
                       "slot_attempts": slot_n + 1})
            return reserve
        finally:
            self._unlock()

    def slot_attempts_used(self, slot_uid: str) -> int:
        self._lock()
        try:
            return self._read()["slot_attempts"].get(slot_uid, 0)
        finally:
            self._unlock()

    def next_transfer_seq(self) -> int:
        """PERSISTENT monotonic transfer sequence (F2R1-P1-02): survives
        process restarts, so a resumed run can never re-mint an old
        transfer_id (duplicate-dispatch guard would refuse it, blocking the
        remaining legal retry quota)."""
        self._lock()
        try:
            st = self._read()
            st["transfer_seq"] = int(st.get("transfer_seq", 0)) + 1
            st["updated_utc"] = utc_now_iso()
            atomic_write_json(self.state_path, st)
            return st["transfer_seq"]
        finally:
            self._unlock()

    # -- settlement: TRANSPORT-outcome first, rating validity irrelevant --
    def settle_by_transport(self, transfer_id: str, wire: dict,
                            price_in_per_1m: float, price_out_per_1m: float) -> dict:
        """wire keys used: usage, http_status, response_received(bool),
        may_have_billed(bool), error_kind. Returns the settlement record.

        Precedence:
          1. valid usage → commit ACTUAL cost (even if > reserve → flagged);
          2. no valid usage but a response was received (HTTP status present
             or bytes arrived) or may_have_billed → keep reserve as UNKNOWN;
          3. clean pre-response failure (connection error before any byte,
             auth/rate-limit refusal without generation) → release reserve.
        Rating JSON parse/schema validity is NEVER an input to this decision.
        """
        usage = wire.get("usage")
        cost = usage_cost_cny(usage, price_in_per_1m, price_out_per_1m)
        response_received = bool(wire.get("response_received")) or wire.get("http_status") is not None
        may_have_billed = bool(wire.get("may_have_billed"))
        self._lock()
        try:
            st = self._read()
            entry = st["inflight"].pop(transfer_id, None)
            if entry is None:
                self._log({"event": "DUPLICATE_SETTLEMENT_REFUSED", "transfer_id": transfer_id})
                raise KeyError(f"transfer {transfer_id} not inflight (duplicate settlement refused)")
            if cost is not None:
                st["committed_spend_cny"] += cost
                over = cost > entry["reserve_cny"] + 1e-12
                rec = {"transfer_id": transfer_id, "mode": "ACTUAL_USAGE",
                       "cost_cny": cost, "reserve_cny": entry["reserve_cny"],
                       "over_reserve": over, "usage": usage}
                self._log({"event": "SETTLE_ACTUAL", **rec,
                           **({"note": "actual usage exceeded heuristic reservation; committed at actual; "
                                       "hard cap governs via committed+inflight+unknown"} if over else {})})
            elif response_received or may_have_billed:
                reason = ("USAGE_MISSING_RESPONSE_RECEIVED" if response_received
                          else "UNKNOWN_INFLIGHT_MAY_HAVE_BILLED")
                st["unknown_reserves"][transfer_id] = {
                    "slot_uid": entry["slot_uid"], "reserve_cny": entry["reserve_cny"],
                    "reason": reason, "error_kind": wire.get("error_kind")}
                rec = {"transfer_id": transfer_id, "mode": "UNKNOWN_KEPT",
                       "kept_reserve_cny": entry["reserve_cny"], "reason": reason}
                self._log({"event": "SETTLE_UNKNOWN", **rec})
            else:
                rec = {"transfer_id": transfer_id, "mode": "RELEASED",
                       "released_cny": entry["reserve_cny"],
                       "error_kind": wire.get("error_kind")}
                self._log({"event": "RELEASE_RESERVE", **rec})
            st.setdefault("settlements", []).append(transfer_id)
            st["updated_utc"] = utc_now_iso()
            atomic_write_json(self.state_path, st)
            return rec
        finally:
            self._unlock()

    # -- R1.2 (F2R11-P1-01): idempotent reconciliation against the archive --

    def transfer_state(self, transfer_id: str) -> str:
        """SETTLED | INFLIGHT | UNKNOWN_RESERVED | UNSEEN — recovery uses this
        to avoid double-billing an already-settled transfer."""
        self._lock()
        try:
            st = self._read()
            if transfer_id in st.get("settlements", []):
                return "SETTLED"
            if transfer_id in st.get("inflight", {}):
                return "INFLIGHT"
            if transfer_id in st.get("unknown_reserves", {}):
                return "UNKNOWN_RESERVED"
            return "UNSEEN"
        finally:
            self._unlock()

    def settle_inflight_from_archive(self, transfer_id: str, wire: dict,
                                     price_in_per_1m: float,
                                     price_out_per_1m: float):
        """Crash happened after archive but before settlement: settle now from
        the ARCHIVED wire (verifiable original usage). Idempotent via
        transfer_state; a settled transfer is never billed twice."""
        state = self.transfer_state(transfer_id)
        if state == "SETTLED":
            return {"mode": "ALREADY_SETTLED_NO_DOUBLE_BILL", "transfer_id": transfer_id}
        if state == "INFLIGHT":
            rec = self.settle_by_transport(transfer_id, wire,
                                           price_in_per_1m, price_out_per_1m)
            rec["settled_from"] = "ARCHIVE_REPLAY"
            self._log({"event": "SETTLED_FROM_ARCHIVE", "transfer_id": transfer_id,
                       "mode": rec["mode"], "cost_cny": rec.get("cost_cny")})
            return rec
        if state == "UNKNOWN_RESERVED":
            return self.resolve_unknown_with_archive(transfer_id, wire,
                                                     price_in_per_1m,
                                                     price_out_per_1m)
        raise KeyError(f"transfer {transfer_id} never reserved in this ledger — "
                       "archive/ledger mismatch, refusing to invent accounting")

    def resolve_unknown_with_archive(self, transfer_id: str, wire: dict,
                                     price_in_per_1m: float,
                                     price_out_per_1m: float):
        """An unknown-charge reserve can be resolved ONLY by verifiable
        original usage from the archive; without usage the unknown risk
        stays (never guessed, never zero-filled)."""
        usage = wire.get("usage")
        cost = usage_cost_cny(usage, price_in_per_1m, price_out_per_1m)
        self._lock()
        try:
            st = self._read()
            entry = st.get("unknown_reserves", {}).get(transfer_id)
            if entry is None:
                raise KeyError(f"transfer {transfer_id} not in unknown_reserves")
            if cost is None:
                self._log({"event": "UNKNOWN_RESERVE_KEPT_NO_VERIFIABLE_USAGE",
                           "transfer_id": transfer_id})
                return {"mode": "UNKNOWN_KEPT", "transfer_id": transfer_id,
                        "kept_reserve_cny": entry["reserve_cny"]}
            del st["unknown_reserves"][transfer_id]
            st["committed_spend_cny"] += cost
            st.setdefault("settlements", []).append(transfer_id)
            st["updated_utc"] = utc_now_iso()
            atomic_write_json(self.state_path, st)
            self._log({"event": "UNKNOWN_RESOLVED_WITH_ARCHIVED_USAGE",
                       "transfer_id": transfer_id, "cost_cny": cost,
                       "released_reserve_cny": entry["reserve_cny"],
                       "usage": usage})
            return {"mode": "RESOLVED_FROM_ARCHIVE", "transfer_id": transfer_id,
                    "cost_cny": cost}
        finally:
            self._unlock()

    def stop_branch(self, reason: str):
        self._lock()
        try:
            st = self._read()
            st["stopped"] = reason
            st["updated_utc"] = utc_now_iso()
            atomic_write_json(self.state_path, st)
            self._log({"event": "BRANCH_STOP", "reason": reason})
        finally:
            self._unlock()

    def snapshot(self) -> dict:
        self._lock()
        try:
            st = self._read()
            inflight_sum = sum(v["reserve_cny"] for v in st["inflight"].values())
            unknown_sum = sum(v["reserve_cny"] for v in st["unknown_reserves"].values())
            return {"committed_spend_cny": st["committed_spend_cny"],
                    "inflight_reserve_cny": inflight_sum,
                    "unknown_reserve_cny": unknown_sum,
                    "projected_total_cny": st["committed_spend_cny"] + inflight_sum + unknown_sum,
                    "hard_cap_cny": self.hard_cap,
                    "attempts_used": st["attempts_used"],
                    "attempt_cap": self.attempt_cap,
                    "slot_attempts": dict(st["slot_attempts"]),
                    "stopped": st["stopped"]}
        finally:
            self._unlock()
