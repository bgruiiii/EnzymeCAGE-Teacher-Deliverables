"""F2 R1 cache + checkpoint (audit F2-P1-04 fixes; contract §7.4).

Changes over R0:
  - Checkpoint read-modify-write is protected by a real transaction lock
    (O_CREAT|O_EXCL lock file, single-writer discipline). R0's lockless
    read-modify-write lost one of two concurrent commits silently; R1 keeps
    both (tested with real threads).
  - Identity binding BEFORE dedup: the checkpoint stores the run identity
    (run/config/schema/prompt/template/evidence/F0 manifests) and a per-slot
    identity digest. A resume that presents a DIFFERENT identity (new
    evidence, new run, changed config) is REFUSED for reuse — old slots are
    never returned as OK under a new version (audit repro: changed evidence
    sha + new run_id returned deduped OK on R0).
  - Cache entries are re-verified on read: stored raw text must match its
    stored sha AND revalidate against the current schema+context; tampered or
    stale entries are quarantined (renamed, logged) and treated as a miss —
    a cache hit can never launder modified content.
  - AttemptArchive stores the FULL original wire material: request body
    bytes (sha-bound; Authorization never persisted), response raw bytes
    (complete SSE stream or JSON envelope), safe headers, provider id, UTC,
    usage, model, finish_reason, stream_status. Parsed content is derived.
  - canonical JSONL loader tolerates a crash-truncated tail: the incomplete
    line is preserved to RATINGS_CANONICAL.jsonl.corrupt_tail (never silently
    dropped) and a RECONCILE event is reported.

Offline: pure local file I/O; no network.
"""
from __future__ import annotations

import errno
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (atomic_write_json, atomic_write_text, atomic_write_bytes,
                         read_json, utc_now_iso, sha256_bytes, sha256_file,
                         sha256_canonical)


class IdentityDriftError(RuntimeError):
    pass


class _FileLock:
    """Single-writer transaction lock (lock file with O_CREAT|O_EXCL)."""

    def __init__(self, path, timeout=30.0):
        self.path = path
        self.timeout = timeout

    def __enter__(self):
        deadline = time.time() + self.timeout
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                if time.time() > deadline:
                    raise TimeoutError(f"checkpoint lock contention > {self.timeout}s")
                try:
                    if time.time() - os.path.getmtime(self.path) > 3600 * 2:
                        os.unlink(self.path)
                except OSError:
                    pass
                time.sleep(0.02)

    def __exit__(self, *a):
        try:
            os.unlink(self.path)
        except OSError:
            pass


class ResponseCache:
    def __init__(self, root):
        self.root = str(root)
        os.makedirs(self.root, exist_ok=True)
        self.quarantine_dir = os.path.join(self.root, "_quarantine")

    def _path(self, key: str) -> str:
        if not (isinstance(key, str) and len(key) == 64
                and all(c in "0123456789abcdef" for c in key)):
            raise ValueError(f"illegal cache key: {key!r}")
        return os.path.join(self.root, key[:2], key + ".json")

    def get_valid(self, key: str, revalidate=None):
        """Return the entry only when: stored sha matches stored text AND
        (revalidate is None OR revalidate(entry) is True). Tampered/failed
        entries are quarantined and reported as a miss."""
        p = self._path(key)
        if not os.path.exists(p):
            return None
        entry = read_json(p)
        raw = entry.get("raw_response_text")
        if not isinstance(raw, str) or sha256_bytes(raw.encode("utf-8")) != entry.get("raw_response_sha256"):
            self._quarantine(key, p, "STORED_SHA_MISMATCH(content tampered)")
            return None
        if entry.get("validation_status") != "VALID":
            return None  # failed entries archived, never reused as success
        if revalidate is not None and not revalidate(entry):
            self._quarantine(key, p, "REVALIDATION_FAILED(current schema/context)")
            return None
        return entry

    def _quarantine(self, key, p, reason):
        os.makedirs(self.quarantine_dir, exist_ok=True)
        dst = os.path.join(self.quarantine_dir, f"{key}.{int(time.time())}.json")
        try:
            os.replace(p, dst)
        except OSError:
            return
        atomic_write_json(dst + ".reason", {"cache_key": key, "reason": reason,
                                            "quarantined_utc": utc_now_iso(),
                                            "quarantined_path": dst})

    def put(self, key: str, raw_response_text: str, usage, validation_status: str,
            request_identity: dict, transfer_id: str = ""):
        p = self._path(key)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.exists(p):
            existing = read_json(p)
            if existing.get("raw_response_sha256") != sha256_bytes(raw_response_text.encode("utf-8")):
                raise RuntimeError(
                    f"cache key collision with different content for {key} — refusing to overwrite "
                    "(previous responses are never replaced)")
            return
        entry = {"cache_key_sha256": key, "raw_response_text": raw_response_text,
                 "raw_response_sha256": sha256_bytes(raw_response_text.encode("utf-8")),
                 "usage": usage, "validation_status": validation_status,
                 "transfer_id": transfer_id,
                 "request_identity": request_identity, "stored_utc": utc_now_iso()}
        atomic_write_json(p, entry)


class Checkpoint:
    """Transaction-locked, identity-bound resume state."""

    def __init__(self, path):
        self.path = str(path)
        self.lock = _FileLock(self.path + ".lock")
        if not os.path.exists(self.path):
            atomic_write_json(self.path, {
                "checkpoint_version": 2, "run_identity": None, "batches": [],
                "committed_slots": {}, "cumulative_cost": None,
                "updated_utc": utc_now_iso()})

    def read(self) -> dict:
        with self.lock:
            return read_json(self.path)

    def set_run_identity(self, identity: dict):
        """Bind/verify the FULL run identity. Refuses a checkpoint that
        already carries a different identity (no silent cross-version reuse).
        identity must include: run_id, config_sha256, schema_sha256,
        system_prompt_sha256, item_template_sha256, f0_manifest_sha256,
        b480_index_sha256, evidence_identity_sha256 (or explicit PENDING)."""
        required = ("run_id", "config_sha256", "schema_sha256",
                    "system_prompt_sha256", "item_template_sha256",
                    "f0_manifest_sha256", "b480_index_sha256",
                    "evidence_identity_sha256")
        missing = [k for k in required if k not in identity]
        if missing:
            raise IdentityDriftError(f"run identity incomplete: missing {missing}")
        with self.lock:
            st = read_json(self.path)
            prev = st.get("run_identity")
            if prev is None:
                st["run_identity"] = identity
                st["updated_utc"] = utc_now_iso()
                atomic_write_json(self.path, st)
                return
            drift = {k: (prev.get(k), identity.get(k)) for k in required
                     if prev.get(k) != identity.get(k) and k != "run_id"}
            if drift:
                raise IdentityDriftError(
                    f"checkpoint identity drift — refusing cross-version reuse: {drift}; "
                    "a new evidence/config/run requires a NEW run root or explicit user-approved rebind")
            if prev.get("run_id") != identity.get("run_id"):
                # same content identity, different run label: allowed only as
                # an explicit resume of the same frozen inputs; record it
                st.setdefault("run_id_aliases", []).append(identity["run_id"])
                st["updated_utc"] = utc_now_iso()
                atomic_write_json(self.path, st)

    @staticmethod
    def slot_identity_digest(item_payload: dict, config_sha: str, schema_sha: str) -> str:
        ie = item_payload.get("identity_echo") or {}
        return sha256_canonical({"slot": item_payload.get("b_slot_uid"),
                                 "identity_echo": ie,
                                 "config_sha256": config_sha,
                                 "schema_sha256": schema_sha})

    def committed_slot(self, b_slot_uid: str, identity_digest: str | None = None):
        """Dedup lookup WITH identity verification (audit F2-P1-04): a commit
        is reusable only when its recorded identity digest matches. Mismatch
        → IdentityDriftError (never returned as OK)."""
        with self.lock:
            st = read_json(self.path)
        entry = st["committed_slots"].get(b_slot_uid)
        if entry is None:
            return None
        if entry.get("validation_status") != "VALID":
            return entry  # failed slots: caller decides retry within quota
        if identity_digest is not None and entry.get("identity_digest") != identity_digest:
            raise IdentityDriftError(
                f"slot {b_slot_uid} committed under a different input/config identity "
                f"({entry.get('identity_digest','?')[:12]}… vs {identity_digest[:12]}…) — "
                "refusing to return the old result as OK for the new version")
        return entry

    def is_committed(self, b_slot_uid: str, identity_digest: str | None = None) -> bool:
        entry = self.committed_slot(b_slot_uid, identity_digest)
        return bool(entry and entry.get("validation_status") == "VALID")

    def commit_slot(self, b_slot_uid: str, transfer_id: str, validation_status: str,
                    cost_snapshot: dict, batch_index: int, identity_digest: str = ""):
        with self.lock:
            st = read_json(self.path)
            if st.get("run_identity") is None:
                raise IdentityDriftError("checkpoint identity not bound before commit")
            prev = st["committed_slots"].get(b_slot_uid)
            if prev and prev["validation_status"] == "VALID" and validation_status == "VALID":
                raise RuntimeError(
                    f"duplicate VALID commit for {b_slot_uid} (transfer {transfer_id}) — "
                    "refusing double submission")
            st["committed_slots"][b_slot_uid] = {
                "transfer_id": transfer_id, "validation_status": validation_status,
                "batch_index": batch_index, "identity_digest": identity_digest,
                "utc": utc_now_iso()}
            st["cumulative_cost"] = cost_snapshot
            if batch_index not in [b["batch_index"] for b in st["batches"]]:
                st["batches"].append({"batch_index": batch_index, "started_utc": utc_now_iso()})
            st["updated_utc"] = utc_now_iso()
            atomic_write_json(self.path, st)

    def record_slot_attempt(self, b_slot_uid: str, transfer_id: str, status: str):
        """Persistent per-slot attempt history (survives restarts; quota is
        ALSO enforced inside the ledger — double safety)."""
        with self.lock:
            st = read_json(self.path)
            hist = st.setdefault("slot_attempt_history", {}).setdefault(b_slot_uid, [])
            hist.append({"transfer_id": transfer_id, "status": status, "utc": utc_now_iso()})
            st["updated_utc"] = utc_now_iso()
            atomic_write_json(self.path, st)


class AttemptArchive:
    """Append-only FULL wire archive (audit F2-P1-01: originals, not hashes).

    Per transfer directory:
      request_body.json        — exact bytes posted (Authorization NEVER stored)
      response_raw.bin         — complete SSE stream or JSON envelope bytes
      response_meta.json       — http status, safe headers, provider id, utc,
                                 usage, model, finish_reason, stream_status,
                                 derived content sha, error kind
    Nothing is ever overwritten; a repeated transfer_id is refused.
    """

    def __init__(self, root):
        self.root = str(root)
        os.makedirs(self.root, exist_ok=True)

    def store(self, transfer_id: str, wire: dict, request_body_bytes: bytes | None,
              request_identity: dict, run_identity: dict | None = None,
              attempt_index: int | None = None):
        safe_tid = transfer_id.replace("/", "_").replace("#", "__")
        d = os.path.join(self.root, safe_tid)
        if os.path.exists(d):
            raise RuntimeError(f"attempt {transfer_id} already archived — refusing overwrite")
        os.makedirs(d)
        raw = wire.get("raw_response_bytes")
        if raw is None and wire.get("raw_text") is not None:
            raw = wire["raw_text"].encode("utf-8")
        if raw is not None:
            atomic_write_bytes(os.path.join(d, "response_raw.bin"), raw)
        if request_body_bytes is not None:
            atomic_write_bytes(os.path.join(d, "request_body.json"), request_body_bytes)
        meta = {k: wire.get(k) for k in
                ("http_status", "safe_headers", "provider_request_id", "model_returned",
                 "model_identity", "usage", "finish_reason", "stream_status",
                 "error_kind", "may_have_billed",
                 "started_utc", "ended_utc", "request_body_sha256", "chunk_parse_errors",
                 "read_error", "raw_truncated", "raw_full_length")}
        meta["transfer_id"] = transfer_id
        meta["response_raw_sha256"] = sha256_bytes(raw) if raw is not None else None
        meta["response_raw_bytes_len"] = len(raw) if raw is not None else None
        meta["derived_content_text_sha256"] = (
            sha256_bytes(wire["content_text"].encode("utf-8"))
            if isinstance(wire.get("content_text"), str) else None)
        meta["request_identity"] = request_identity
        # R1.2: run identity travels with the archive so recovery can verify
        # the archived response was produced under the CURRENT frozen versions
        meta["run_identity"] = run_identity
        meta["attempt_index"] = attempt_index
        meta["authorization_stored"] = False
        meta["archived_utc"] = utc_now_iso()
        atomic_write_json(os.path.join(d, "response_meta.json"), meta)
        return d

    def index_by_slot(self) -> dict:
        """R1.2 (F2R11-P1-01): scan the archive once → {b_slot_uid: [meta,…]}
        in archived order. The ARCHIVE (original provider wire) is the primary
        recovery source; cache is only a derived accelerator."""
        index = {}
        if not os.path.isdir(self.root):
            return index
        for name in sorted(os.listdir(self.root)):
            meta_p = os.path.join(self.root, name, "response_meta.json")
            if not os.path.isfile(meta_p):
                continue
            try:
                with open(meta_p, encoding="utf-8") as f:
                    meta = json.load(f)
            except (ValueError, UnicodeDecodeError):
                continue  # unreadable meta: surfaced by validator I-checks, not fatal here
            meta["_dir"] = os.path.join(self.root, name)
            uid = (meta.get("request_identity") or {}).get("b_slot_uid")
            if uid:
                index.setdefault(uid, []).append(meta)
        return index


# ---------------------------------------------------------------------------
# R1.2 (F2R11-P1-02): binary-safe canonical loading + startup repair
# ---------------------------------------------------------------------------

def _try_record(line_bytes: bytes):
    """Parse one JSONL line from BYTES (mid-UTF-8 truncation safe).
    Returns (record, None) or (None, reason)."""
    try:
        text = line_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        return None, f"UTF8_DECODE_ERROR({e.start}:{e.end})"
    try:
        return json.loads(text), None
    except ValueError as e:
        return None, f"JSON_PARSE_ERROR({e})"


def load_canonical_jsonl(path):
    """Binary-safe loader. Returns (records, problems) where problems lists
    {"line_no", "reason", "sha256"} for every non-empty line that fails to
    parse — mid-file damage AND torn tails are both surfaced, never silently
    skipped. Does NOT modify the file (repair_canonical does)."""
    records, problems = [], []
    if not os.path.exists(path):
        return records, None
    with open(path, "rb") as f:
        raw = f.read()
    for i, line in enumerate(raw.split(b"\n"), 1):
        if not line.strip():
            continue
        rec, reason = _try_record(line)
        if rec is None:
            problems.append({"line_no": i, "reason": reason,
                             "sha256": sha256_bytes(line)})
        else:
            records.append(rec)
    return records, problems


def repair_canonical(path, repair_log_dir=None):
    """Startup repair of RATINGS_CANONICAL.jsonl (F2R11-P1-02).

    Distinguishes three situations and NEVER loses evidence:
      1. complete valid lines            → kept in the active file;
      2. a final line WITHOUT newline:
           - valid JSON  → COMPLETE_MISSING_FINAL_NEWLINE: kept (normalized
             by appending the newline) — a complete record must not be lost;
           - invalid     → TRUNCATED_TAIL: raw bytes moved to
             <path>.truncated_tail_<utc> (sha recorded), removed from the
             active file so later appends start on a clean boundary;
      3. newline-terminated but unparsable lines in the MIDDLE → true
         mid-file damage: raw bytes preserved in CORRUPT_RECORDS_QUARANTINE
         (with line numbers + shas), removed from the active file, flagged
         for human review (never silently skipped).
    The pre-repair file is backed up whole (<path>.pre_repair_backup_<utc>,
    never overwriting an existing backup); every action is appended to
    CANONICAL_REPAIR_LOG.jsonl. Idempotent: a clean file is untouched.
    Returns a report dict (repaired flag + actions + evidence paths).
    """
    report = {"path": str(path), "repaired": False, "actions": [],
              "backup_path": None, "tail_evidence": None,
              "quarantine_evidence": None, "records_valid": 0}
    if not os.path.exists(path):
        return report
    with open(path, "rb") as f:
        raw = f.read()
    original_sha = sha256_bytes(raw)
    segments = raw.split(b"\n")
    trailing = segments[-1]          # bytes after the last \n (b"" if ends with \n)
    complete_lines = segments[:-1]

    valid_lines = []       # bytes of lines that stay in the active file
    mid_corrupt = []       # (line_no, bytes, reason)
    for i, line in enumerate(complete_lines, 1):
        if not line.strip():
            continue
        rec, reason = _try_record(line)
        if rec is None:
            mid_corrupt.append((i, line, reason))
        else:
            valid_lines.append(line)

    tail_action = None
    if trailing.strip():
        rec, reason = _try_record(trailing)
        if rec is None:
            tail_action = ("TRUNCATED_TAIL", reason)
        else:
            tail_action = ("COMPLETE_MISSING_FINAL_NEWLINE", None)
            valid_lines.append(trailing)

    needs_repair = bool(mid_corrupt) or tail_action is not None
    report["records_valid"] = len(valid_lines)
    if not needs_repair:
        return report

    log_dir = repair_log_dir or os.path.dirname(os.path.abspath(path))
    os.makedirs(log_dir, exist_ok=True)
    stamp = utc_now_iso().replace(":", "").replace("-", "")

    # 1) whole-file backup (evidence; never overwrite an existing backup)
    backup = f"{path}.pre_repair_backup_{stamp}"
    n = 0
    while os.path.exists(backup):
        n += 1
        backup = f"{path}.pre_repair_backup_{stamp}_{n}"
    atomic_write_bytes(backup, raw)
    report["backup_path"] = backup
    report["actions"].append({"action": "BACKUP_WHOLE_FILE", "path": backup,
                              "original_sha256": original_sha,
                              "original_bytes": len(raw)})

    # 2) truncated tail → evidence file (append-style, timestamped, never
    #    overwriting historical tail evidence)
    if tail_action and tail_action[0] == "TRUNCATED_TAIL":
        tail_path = f"{path}.truncated_tail_{stamp}"
        atomic_write_bytes(tail_path, trailing)
        report["tail_evidence"] = tail_path
        report["actions"].append({
            "action": "TRUNCATED_TAIL_PRESERVED", "path": tail_path,
            "tail_bytes": len(trailing),
            "tail_sha256": sha256_bytes(trailing),
            "reason": tail_action[1],
            "note": "unfinished record removed from active file; the slot is recovered from cache/archive, never re-paid blindly"})
    elif tail_action:
        report["actions"].append({
            "action": "COMPLETE_MISSING_FINAL_NEWLINE_NORMALIZED",
            "line_sha256": sha256_bytes(trailing),
            "note": "complete valid record kept; newline appended"})

    # 3) mid-file corrupt lines → quarantine (explicit, never silent)
    if mid_corrupt:
        q_path = os.path.join(log_dir, "CORRUPT_RECORDS_QUARANTINE.jsonl")
        with open(q_path, "a", encoding="utf-8") as f:
            for line_no, line, reason in mid_corrupt:
                entry = {"source_path": str(path), "line_no": line_no,
                         "reason": reason, "line_sha256": sha256_bytes(line),
                         "line_bytes_b64": __import__("base64").b64encode(line).decode("ascii"),
                         "quarantined_utc": utc_now_iso(),
                         "original_file_backup": backup}
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        report["quarantine_evidence"] = q_path
        report["actions"].append({
            "action": "MIDFILE_CORRUPT_QUARANTINED", "count": len(mid_corrupt),
            "line_nos": [m[0] for m in mid_corrupt], "path": q_path,
            "note": "true mid-file damage isolated for human review; valid records around it are kept"})

    # 4) rewrite the active file atomically = valid prefix/lines + newline end
    new_raw = b"".join(l + b"\n" for l in valid_lines)
    atomic_write_bytes(path, new_raw)
    report["repaired"] = True
    report["actions"].append({
        "action": "ACTIVE_FILE_REWRITTEN",
        "new_sha256": sha256_bytes(new_raw), "new_bytes": len(new_raw),
        "records_kept": len(valid_lines)})

    # 5) repair log (append-only)
    log_path = os.path.join(log_dir, "CANONICAL_REPAIR_LOG.jsonl")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"utc": utc_now_iso(), "report": report},
                           ensure_ascii=False) + "\n")
    return report
