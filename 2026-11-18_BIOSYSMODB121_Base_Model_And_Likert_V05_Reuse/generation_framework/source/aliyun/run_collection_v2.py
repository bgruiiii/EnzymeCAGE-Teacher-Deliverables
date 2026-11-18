#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_collection_v2.py  --  BIOSYSMOdb150 five-LLM answer collector, v2.

Authority
---------
* 07_HPC_Prompts/LOCAL_AI_BIOSYSMODB150_COLLECTION_V2_PAYLOAD_BUILDER_EXECUTOR_ONLY_20260926.md
  sections 3 (deliverables), 4 (offline tests), 6 (packaging whitelist).
* 00_Authority_Teacher_Plan/BIOSYSMODB150_API_ANSWER_COLLECTION_EXECUTION_PLAN_2026-09-26.md
  sections 6 (blank template), 7 (dispatch), 8 (receiver), 9 (status model),
  10 (parameters/budget), 11 (parsing and layout), 12 (mock scenarios),
  13 (packaging), 14 (evidence).

This file is BOTH the CLI entry point and the only importable library of the v2
collector: the payload whitelist allows exactly three scripts, so
``summarize_collection_v2.py``, ``validate_collection_artifacts_v2.py`` and
``tests/`` all load this module with
``importlib.util.spec_from_file_location()``.

Engineering boundaries enforced in code (not merely documented)
---------------------------------------------------------------
1. Importing this module reads no API key, no env file, performs no network I/O
   and writes nothing.  ``requests`` and ``jsonschema`` are optional imports;
   a missing ``jsonschema`` degrades ``schema_status`` to ``NOT_CHECKED``
   instead of aborting the collection.
2. Raw SSE events are appended and flushed one line at a time, so a killed
   process still leaves a replayable transcript.
3. ``delta.content`` and ``delta.reasoning_content`` are accumulated into
   separate buffers and separate files.  Reasoning text is never promoted into
   the visible answer and is never parsed as if it were the answer.
4. The six status dimensions stay separate.  A schema failure, a JSON failure
   or a truncation is recorded as an observation.  Nothing in this module
   compares an answer against gold, judges scientific correctness, deletes or
   rewrites a non-conforming answer, or re-questions a model about content.
5. Retries are transport-level only (429 / 5xx / network / read timeout /
   deadline), capped, backoff-respecting, and never content-based.
6. Old attempt directories are never cleared before a retry: every attempt is
   an independent ``attempt_NNN/`` directory that survives.

Status vocabulary (execution plan section 9)
--------------------------------------------
transport_status : NOT_SENT | HTTP_ERROR | HTTP_200 | NETWORK_ERROR
stream_status    : NOT_STARTED | COMPLETE | INTERRUPTED | PARSE_ERROR | UNKNOWN
terminal_reason / finish_reason : stop | length | content_filter | tool_calls
                                  | other | null
json_parse_status: VALID | INVALID | EMPTY
schema_status    : VALID | INVALID | NOT_CHECKED
collection_status: RESPONSE_CAPTURED | RESPONSE_CAPTURED_TRUNCATED
                   | PARTIAL_STREAM_CAPTURED | NO_RESPONSE

``finish_reason`` is the provider's own ``choices[0].finish_reason`` (never
invented).  ``terminal_reason`` is why the collector stopped reading: equal to
``finish_reason`` when the provider supplied one, ``other`` when the stream
ended without one (bare ``[DONE]``, read timeout, deadline, transport error,
EOF), and ``null`` when the stream never started.

``stream_status`` is ``COMPLETE`` only when a terminal marker (``[DONE]``) or a
``finish_reason`` was observed AND no read-stream error and no chunk parse
error occurred.  Having received chunks is never sufficient.

Leak-scan policy
----------------
The collector's own secret is never tolerated anywhere: the loaded key value is
a hard block in every artifact.  ``Bearer `` and ``sk-`` are hard blocks in
collector-generated files (request/status/timing/validation/manifest/normalized
/results/SHA256SUMS).  In verbatim model-output files (answer_text.txt,
reasoning_content.txt, parsed_answer.json, raw_events.jsonl) those two patterns
are *reported* but not blocked, because censoring or discarding model-authored
bytes would destroy the raw answer this run exists to preserve.
"""

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import threading
import time

try:  # optional at import time: a dry run and the whole test suite need neither
    import requests
except ImportError:  # pragma: no cover - depends on the target machine
    requests = None

try:
    import jsonschema
except ImportError:  # pragma: no cover - depends on the target machine
    jsonschema = None


# --------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------

RECORD_VERSION = "collection_record_v2"
ANSWER_SCHEMA_VERSION = "biodegradation_answer_v2"
DEFAULT_RUN_ID = "biosysmodb150_bailian_collection_v2_20260926"

# --- teacher-aligned staging (execution plan section 5, G gates) -------------
# phase enters BOTH the run directory layout and the idempotency key, so a
# formal attempt can never reuse a smoke/pilot terminal record.
PHASES = ("smoke", "pilot", "formal", "exploratory")
ROUTE_MODES = ("main", "exploratory")
DEFAULT_EXPERIMENT_VERSION = "teacher_aligned_D0"
DEFAULT_PHASE = "smoke"
# upstream stage gates that must be PASS before the phase may go live
PHASE_UPSTREAM_GATES = {
    "smoke": ("G1_gold", "G2_questions", "G3_scorer", "G4_search"),
    "pilot": ("G1_gold", "G2_questions", "G3_scorer", "G4_search", "G5_smoke"),
    "formal": ("G1_gold", "G2_questions", "G3_scorer", "G4_search", "G5_smoke",
               "G6_pilot", "G7_budget"),
    "exploratory": ("G1_gold", "G2_questions", "G3_scorer", "G4_search"),
}
GATE_FILE_SUFFIXES = (".stage_gate.json", ".json")
SEARCH_DECISIONS = ("ALL_PASS", "ANY_NOT_PASS", "UNDECIDED")
# enable_search is derived ONLY from the G4 symmetry decision (section 12):
# all five models pass -> true; any failure -> false; no decision -> dispatch refused.
SEARCH_DECISION_TO_ENABLE = {"ALL_PASS": True, "ANY_NOT_PASS": False}

PROMPT_BASENAMES = {
    "main": "unified_collection_v2.txt",
    "exploratory": "unified_collection_v2_exploratory.txt",
}

LIVE_GATE_STATUSES = ("PREPARING", "READY_FOR_REVIEW", "PASS", "FAIL", "INVALIDATED")

ROUTE_SCOPE_MISSING_ERROR = "NOT_SENT_ROUTE_SCOPE_MISSING_IN_MAIN_MODE"
SEARCH_UNDECIDED_ERROR = "NOT_SENT_SEARCH_DECISION_UNDECIDED"
LIVE_GATE_ERROR = "NOT_SENT_LIVE_GATE_REFUSED"


TRANSPORT_STATUSES = ("NOT_SENT", "HTTP_ERROR", "HTTP_200", "NETWORK_ERROR")
STREAM_STATUSES = ("NOT_STARTED", "COMPLETE", "INTERRUPTED", "PARSE_ERROR", "UNKNOWN")
TERMINAL_VOCABULARY = ("stop", "length", "content_filter", "tool_calls", "other", None)
JSON_PARSE_STATUSES = ("VALID", "INVALID", "EMPTY")
SCHEMA_STATUSES = ("VALID", "INVALID", "NOT_CHECKED")
COLLECTION_STATUSES = (
    "RESPONSE_CAPTURED",
    "RESPONSE_CAPTURED_TRUNCATED",
    "PARTIAL_STREAM_CAPTURED",
    "NO_RESPONSE",
)

EVENT_KINDS = (
    "DATA",
    "DONE",
    "HTTP_ERROR",
    "CHUNK_PARSE_ERROR",
    "READ_TIMEOUT",
    "DEADLINE_EXCEEDED",
    "TRANSPORT_ERROR",
    "EOF",
    "TERMINAL_OBSERVED",
    "STREAM_CLOSED",
)

# the eight per-attempt artifacts, in the mandated order
ARTIFACT_NAMES = (
    "request",
    "raw_events",
    "answer_text",
    "reasoning_content",
    "parsed_answer",
    "validation",
    "timing",
    "status",
)
ARTIFACT_FILENAMES = {
    "request": "request.json",
    "raw_events": "raw_events.jsonl",
    "answer_text": "answer_text.txt",
    "reasoning_content": "reasoning_content.txt",
    "parsed_answer": "parsed_answer.json",
    "validation": "validation.json",
    "timing": "timing.json",
    "status": "status.json",
}

MAX_DISPLAYED_VALIDATION_ERRORS = 200
MAX_ERROR_MESSAGE_CHARS = 2000
MAX_HTTP_ERROR_BODY_CHARS = 2000

OXYGEN_GLOSS = {
    "aerobic": "好氧",
    "anaerobic": "厌氧",
    "mixed": "兼性",
    "unknown": "未知",
}

DEFAULT_LIMITS = {
    "connect_timeout_seconds": 20,
    "read_idle_timeout_seconds": 120,
    "attempt_deadline_seconds": 1800,
    "max_transport_retries": 2,
    "backoff_base_seconds": 5,
    "backoff_cap_seconds": 30,
    "honor_retry_after": True,
    "retryable_http_status": [429, 500, 502, 503, 504],
    "fatal_http_status": [400, 401, 403, 404],
    "per_model_concurrency": 1,
    "global_concurrency": 5,
    "tier2_allowed_only_when_documented_higher_cap": True,
    "tier2_max_attempts_per_model": 1,
    # The old "total_new_api_request_cap: 15" live shortcut (toluene engineering
    # smoke) is REMOVED: task counts now come from the phase's frozen case list
    # (5 x n). live authorization is a separate, explicit gate.
    "live_disabled": True,
    "authorized_new_api_requests": 0,
    # teacher-approved envelope (G1 approval 2026-09-27): G4<=15, G5=15, G6=50,
    # hard total 80. No global cap: phase gates + this envelope replace the old
    # toluene 15-request shortcut.
    "phase_api_request_caps": {"G4_search": 15, "G5_smoke": 15, "G6_pilot": 50},
    "phase_api_total_cap": 80,
    "no_content_based_retry": True,
    "no_science_requestion": True,
    "resume_policy": "SKIP_TERMINAL_HOLD_INTERRUPTED",
    "raw_events_flush_per_event": True,
}

# Explicit per-file whitelist for a run directory. Filenames are matched, never
# directories: a directory that happens to contain a SHA256SUMS is still walked
# (skipping it whole was the v1 summarize.py defect).
RUN_ROOT_FILES = ("run_manifest.json", "SHA256SUMS", "VALIDATION_REPORT.json")
NORMALIZED_AGGREGATE_FILES = ("all_models.jsonl", "all_attempts.jsonl")
PER_MODEL_JSONL_RE = re.compile(r"^model_m[0-9]+\.jsonl$")
RESULT_FILENAME_RE = re.compile(r"^BIOPATH150_[0-9]{3}__[A-Za-z0-9._-]+__[A-Za-z0-9._-]+\.json$")

ATTEMPT_DIR_RE = re.compile(r"^attempt_(\d{3})$")
CASE_ID_RE = re.compile(r"^BIOPATH150_[0-9]{3}$")
SINGLE_FENCE_RE = re.compile(r"^```[^\n]*\n(.*?)\n?```$", re.DOTALL)
SK_KEY_RE = re.compile(r"sk-[A-Za-z0-9_\-]{8,}")


# --------------------------------------------------------------------------
# hashing and atomic IO (house style: 23_.../scripts/s4r2_manifest.py)
# --------------------------------------------------------------------------

def sha256_bytes(data):
    """SHA256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_text(text):
    """SHA256 hex digest of UTF-8 encoded text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path):
    """SHA256 hex digest of a file, streamed in 1 MiB blocks."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dir(path):
    if path and not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return path


def atomic_write_bytes(path, data):
    """Write bytes via tempfile + os.replace so a kill cannot leave a torn file."""
    ensure_dir(os.path.dirname(path))
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".cv2tmp_")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return path


def atomic_write_text(path, text):
    return atomic_write_bytes(path, text.encode("utf-8"))


def atomic_write_json(path, obj, indent=2):
    text = json.dumps(obj, indent=indent, ensure_ascii=False, sort_keys=False)
    return atomic_write_text(path, text + "\n")


def atomic_write_jsonl(path, records):
    """One json.dumps per line; never pretty JSON concatenated together."""
    lines = [json.dumps(r, ensure_ascii=False, sort_keys=False) for r in records]
    text = "".join(line + "\n" for line in lines)
    return atomic_write_text(path, text)


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def read_text(path):
    return read_bytes(path).decode("utf-8")


def utc_stamp(at=None):
    """UTC audit stamp. Wall clock is for auditing only; durations use monotonic."""
    dt = at if at is not None else datetime.datetime.utcnow()
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (dt.microsecond // 1000)


def compact_json(obj):
    """Compact, non-ASCII-preserving JSON text (used for the prompt schema block)."""
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False, sort_keys=False)


def sanitize_model_id(name):
    """Filesystem slug for an exact model id. The exact id is never replaced."""
    return name.replace("/", "_")


def sanitize_filename_component(name):
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


def load_json_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_jsonl_file(path):
    """Parse a JSONL file; every line must independently parse."""
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except ValueError as exc:
                raise ValueError("%s:%d not independently parsable: %s" % (path, lineno, exc))
    return rows


# --------------------------------------------------------------------------
# prompt / body rendering (execution plan sections 6 and 7)
# --------------------------------------------------------------------------

def build_case_metadata_block(case, route_mode="main"):
    """The per-case metadata lines inserted at {{CASE_METADATA_BLOCK}}.

    Contains only dispatch metadata. Gold step counts, endpoints, organisms and
    enzymes are never part of a case line and therefore never appear here.

    route_mode="main" (teacher's primary experiment): the route is always
    specified by the question; a null route_scope never degrades into a
    free-choice instruction here -- such a case is refused upstream and goes to
    pending review instead of being silently re-interpreted.
    route_mode="exploratory": null route_scope is the expected input and the
    free-choice wording is shown, matching the separate exploratory prompt.
    """
    oxygen = case.get("oxygen_condition")
    route = case.get("route_scope")
    if oxygen is None:
        oxygen_text = "null（未指定）"
    else:
        gloss = OXYGEN_GLOSS.get(oxygen)
        oxygen_text = "%s（%s）" % (oxygen, gloss) if gloss else str(oxygen)
    if route is None:
        if route_mode == "exploratory":
            route_text = "null（不限定路线：由你选择该氧条件下的主链，并在 route_scope.chosen_route_name 中写明）"
        else:
            route_text = "null（未指定）"
    else:
        route_text = str(route)
    return "\n".join([
        "case_id: %s" % case.get("case_id"),
        "污染物中文名: %s" % case.get("pollutant_name_zh"),
        "污染物英文名: %s" % case.get("pollutant_name_en"),
        "氧条件: %s" % oxygen_text,
        "路线范围: %s" % route_text,
    ])


def render_blank_template(template_text, case):
    """Substitute the five case placeholders of the blank template.

    A null value replaces the whole quoted placeholder with a JSON null so the
    rendered template stays valid JSON. The rendered text is re-parsed as a
    hard assertion: a template that renders to invalid JSON must never be sent.
    """
    out = template_text
    pairs = (
        ("{{CASE_ID}}", case.get("case_id")),
        ("{{POLLUTANT_NAME_ZH}}", case.get("pollutant_name_zh")),
        ("{{POLLUTANT_NAME_EN}}", case.get("pollutant_name_en")),
        ("{{OXYGEN_CONDITION}}", case.get("oxygen_condition")),
        ("{{ROUTE_SCOPE}}", case.get("route_scope")),
    )
    for token, value in pairs:
        if value is None:
            out = out.replace('"%s"' % token, "null")
            out = out.replace(token, "")
        else:
            text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
            out = out.replace(token, text)
    json.loads(out)  # hard assertion
    return out


def render_prompt(prompt_template_text, case, rendered_template_text, compact_schema_text,
                  route_mode="main"):
    """Render the single user-message body. Byte-identical for all five models."""
    out = prompt_template_text
    out = out.replace("{{CASE_METADATA_BLOCK}}",
                      build_case_metadata_block(case, route_mode))
    out = out.replace("{{BLANK_TEMPLATE_JSON}}", rendered_template_text)
    out = out.replace("{{COMPACT_SCHEMA_JSON}}", compact_schema_text)
    for token in re.findall(r"\{\{[A-Z_]+\}\}", out):
        raise ValueError("unrendered prompt placeholder remains: %s" % token)
    return out


def build_messages(prompt_text):
    """One user message only, as proven byte-for-byte by the 2026-09-24 smoke.

    No system message and no tool message: introducing several unknown provider
    capabilities at once is what execution plan section 7 warns against.
    """
    return [{"role": "user", "content": prompt_text}]


def messages_sha256(messages):
    return sha256_text(compact_json(messages))


def build_request_body(exact_model_id, messages, max_tokens, shared_parameters,
                       enable_search):
    """Body shape verified by the 2026-09-24 smoke run.

    tier1 never carries enable_thinking / reasoning_effort / thinking_budget /
    response_format: each model keeps its native reasoning behaviour.

    ``enable_search`` is NOT read from the models config: the collector derives
    it only from the G4 search-efficacy symmetry decision (ALL_PASS -> true,
    ANY_NOT_PASS -> false) and writes the frozen policy into every body, so no
    model can silently keep search on. A None decision is refused upstream and
    never reaches this function for a live request.
    """
    if enable_search is None:
        raise ValueError("enable_search is undecided: the G4 search symmetry "
                         "decision must produce ALL_PASS or ANY_NOT_PASS before "
                         "any request body is built")
    body = {"model": exact_model_id, "messages": messages}
    for key in sorted(shared_parameters):
        if key == "enable_search":
            continue  # ignored on purpose: the G4 decision owns this parameter
        body[key] = shared_parameters[key]
    body["max_tokens"] = max_tokens
    body["enable_search"] = bool(enable_search)
    ordered = {"model": body.pop("model"), "messages": body.pop("messages")}
    for key in ("temperature", "max_tokens", "stream", "stream_options", "enable_search"):
        if key in body:
            ordered[key] = body.pop(key)
    for key in sorted(body):
        ordered[key] = body[key]
    return ordered


def request_body_sha256(body):
    """sha256 over the exact serialized request body (model+messages+parameters)."""
    return sha256_text(compact_json(body))


def idempotency_key(phase, experiment_version, case_id, model_id, body_sha):
    """sha256 over the five contracted identity atoms (execution plan section 10).

    phase + experiment_version + case_id + model_id + request_body_sha. A formal
    phase can therefore never reuse a smoke/pilot terminal record, and a body
    change (template/schema/parameter regeneration) invalidates the key.
    """
    return sha256_text(compact_json({
        "phase": phase,
        "experiment_version": experiment_version,
        "case_id": case_id,
        "model_id": model_id,
        "request_body_sha": body_sha,
    }))


def request_parameter_snapshot(body):
    """The body parameters actually sent, minus the (large) messages array."""
    return {k: v for k, v in body.items() if k != "messages"}


# --------------------------------------------------------------------------
# key handling (README_SECURITY_AND_SETUP.md section 5)
# --------------------------------------------------------------------------

class KeyLoadError(Exception):
    pass


def check_key_env_file_permissions(path):
    """Refuse a key file readable by group or other. Returns the octal mode."""
    mode = stat.S_IMODE(os.stat(path).st_mode)
    if mode & 0o077:
        raise KeyLoadError(
            "refusing to read key env file with group/other permissions "
            "(mode=%s); fix with: chmod 600 %s" % (oct(mode), path)
        )
    return mode


def load_api_key(key_env_file, env_var="DASHSCOPE_API_KEY"):
    """Read exactly one variable from an external, chmod-600 file.

    Never reads os.environ, never prints the value, its length, a prefix or a
    suffix. Callers may only report PRESENT / MISSING.
    """
    if not key_env_file:
        raise KeyLoadError("--key-env-file is required for a real (non --dry-run) collection")
    path = os.path.abspath(key_env_file)
    if not os.path.isfile(path):
        raise KeyLoadError("key env file not found: %s" % path)
    check_key_env_file_permissions(path)
    key = None
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("export "):
                line = line[len("export "):].strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith(env_var + "="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        raise KeyLoadError("%s not found in key env file" % env_var)
    return key


def build_headers(api_key):
    """In-memory only. Never written to request.json or any other artifact."""
    return {
        "Authorization": "Bearer %s" % api_key,
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }


LEAK_PATTERNS_HARD_EVERYWHERE = ("__KEY_VALUE__",)
LEAK_PATTERNS_GENERATED = ("Bearer ", "sk-", "DASHSCOPE_API_KEY=", ".env")
MODEL_OUTPUT_ARTIFACTS = (
    "answer_text.txt",
    "reasoning_content.txt",
    "parsed_answer.json",
    "raw_events.jsonl",
)


def scan_text_for_leaks(text, key_value=None):
    """Return a list of finding dicts. Never returns the secret itself."""
    findings = []
    if key_value and key_value in text:
        findings.append({"pattern": "api_key_value", "severity": "HARD", "count": text.count(key_value)})
    bearer = text.count("Bearer ")
    if bearer:
        findings.append({"pattern": "Bearer ", "severity": "CONTEXT", "count": bearer})
    sk = len(SK_KEY_RE.findall(text))
    if sk:
        findings.append({"pattern": "sk-<key-shaped>", "severity": "CONTEXT", "count": sk})
    if "DASHSCOPE_API_KEY=" in text:
        findings.append({"pattern": "DASHSCOPE_API_KEY=", "severity": "CONTEXT",
                         "count": text.count("DASHSCOPE_API_KEY=")})
    return findings


def scan_artifacts_for_leaks(paths, key_value=None):
    """Scan artifacts; hard-block on the key value and on generated-file patterns."""
    hard = []
    reported = []
    for path in paths:
        if not os.path.isfile(path):
            continue
        try:
            text = read_bytes(path).decode("utf-8", "replace")
        except OSError:
            continue
        basename = os.path.basename(path)
        is_model_output = basename in MODEL_OUTPUT_ARTIFACTS
        for finding in scan_text_for_leaks(text, key_value):
            item = dict(finding)
            item["path"] = path
            if finding["pattern"] == "api_key_value":
                hard.append(item)
            elif is_model_output:
                reported.append(item)
            else:
                if finding["pattern"] in LEAK_PATTERNS_GENERATED:
                    hard.append(item)
                else:
                    reported.append(item)
    return {"hard_failures": hard, "reported_findings": reported}


# --------------------------------------------------------------------------
# answer parsing (execution plan section 11) -- no LLM repair, no guessing
# --------------------------------------------------------------------------

def strip_single_fence(text):
    """Remove exactly one surrounding JSON fence, or return None.

    Only the whole-text-single-fence case is handled. Extracting a JSON-looking
    slice out of a longer prose body is deliberately not implemented.
    """
    if not text.startswith("```"):
        return None
    if text.count("```") != 2:
        return None
    match = SINGLE_FENCE_RE.match(text)
    if not match:
        return None
    return match.group(1).strip()


def parse_answer_text(text):
    """Return (parsed_value, json_parse_status, parser_transform).

    Rules, in order:
      * empty / whitespace-only body -> (None, EMPTY, NONE); never {} as a fake
      * whole-text json.loads succeeds -> (value, VALID, NONE)
      * whole text is one fenced block -> strip that fence and parse again,
        parser_transform = STRIP_SINGLE_FENCE
      * otherwise -> (None, INVALID, NONE). No slice extraction, no quote
        substitution, no bracket repair, no model-assisted repair.

    A legal JSON array or JSON null is preserved as the parsed value with
    json_parse_status = VALID; the schema layer then reports INVALID. Data is
    never discarded and never replaced by an empty object.
    """
    if text is None:
        return None, "EMPTY", "NONE"
    stripped = text.strip()
    if not stripped:
        return None, "EMPTY", "NONE"
    try:
        return json.loads(stripped), "VALID", "NONE"
    except ValueError:
        pass
    unfenced = strip_single_fence(stripped)
    if unfenced is not None:
        try:
            return json.loads(unfenced), "VALID", "STRIP_SINGLE_FENCE"
        except ValueError:
            return None, "INVALID", "STRIP_SINGLE_FENCE"
    return None, "INVALID", "NONE"


def error_path_of(error):
    parts = [str(p) for p in getattr(error, "absolute_path", [])]
    return "/".join(parts) if parts else "$"


def _resolve_schema_node(node, schema_root, depth=0):
    """Follow $ref chains so the walker sees the real object definitions."""
    seen = 0
    while isinstance(node, dict) and "$ref" in node and seen < 32:
        ref = node["$ref"]
        if not ref.startswith("#/"):
            return None  # external ref: never traversed, never a warning source
        target = schema_root
        for part in ref[2:].split("/"):
            if not isinstance(target, dict) or part not in target:
                return None
            target = target[part]
        node = target
        seen += 1
    return node


def collect_extra_field_warnings(instance, schema, path="$", out=None, schema_root=None):
    """Independent walker: unknown keys at ANY nesting level become warnings.

    Teacher contract section 8: extra fields are recorded as warnings only --
    never a FAIL, never a hard error, never deleted from the parsed answer.
    The answer schema deliberately carries no additionalProperties:false any
    more, so jsonschema no longer flags them; this walker reports them without
    touching the instance.
    """
    if out is None:
        out = []
    if schema_root is None:
        schema_root = schema if isinstance(schema, dict) else None
    node = _resolve_schema_node(schema, schema_root)
    if node is None:
        return out
    schema = node
    if "anyOf" in schema:
        for sub in schema["anyOf"]:
            collect_extra_field_warnings(instance, sub, path, out, schema_root)
        return out
    if "allOf" in schema:
        for sub in schema["allOf"]:
            collect_extra_field_warnings(instance, sub, path, out, schema_root)
        return out
    if "oneOf" in schema:
        for sub in schema["oneOf"]:
            collect_extra_field_warnings(instance, sub, path, out, schema_root)
        return out
    if isinstance(instance, dict):
        props = schema.get("properties")
        if isinstance(props, dict) and props:
            for key in instance:
                if key not in props:
                    out.append({"path": path, "unexpected_key": key})
                else:
                    collect_extra_field_warnings(
                        instance[key], props[key], "%s/%s" % (path, key), out,
                        schema_root)
    elif isinstance(instance, list):
        items = schema.get("items")
        if items is not None:
            for index, value in enumerate(instance):
                collect_extra_field_warnings(value, items, "%s/%d" % (path, index),
                                             out, schema_root)
    return out


def validate_answer(parsed, schema_obj, check=True):
    """Validate the parsed answer. Returns a dict, never raises.

    The FULL error count is always reported in ``total``; the displayed list is
    capped at MAX_DISPLAYED_VALIDATION_ERRORS with ``truncated`` set. Counting
    uses ``list(Draft7Validator(schema).iter_errors(instance))``, which is the
    same traversal the frozen 2026-09-26 audit used to obtain 150 / 145 errors
    (against the v1 schema, which still fails on extra fields).

    Teacher alignment: extra fields at any nesting level are warnings collected
    by the independent walker ``collect_extra_field_warnings``; they never enter
    ``total`` and never flip schema_status. Hard errors are required / type /
    enum / structural violations only. JSON syntax validity and schema status
    stay separate axes.
    """
    result = {
        "schema_status": "NOT_CHECKED",
        "errors": [],
        "total": 0,
        "truncated": False,
        "warnings": [],
        "warnings_total": 0,
        "note": None,
        "answer_schema_version": ANSWER_SCHEMA_VERSION,
        "validator": None,
    }
    if not check:
        result["note"] = "NOT_CHECKED_no_parsable_body"
        return result
    if jsonschema is None:
        result["note"] = "NOT_CHECKED_jsonschema_unavailable"
        return result
    if schema_obj is None:
        result["note"] = "NOT_CHECKED_schema_unavailable"
        return result
    try:
        validator = jsonschema.Draft7Validator(schema_obj)
    except Exception as exc:  # a broken schema must not kill a collection run
        result["note"] = "NOT_CHECKED_schema_unusable:%s" % type(exc).__name__
        return result
    result["validator"] = "jsonschema.Draft7Validator/%s" % getattr(jsonschema, "__version__", "unknown")
    try:
        errors = list(validator.iter_errors(parsed))
    except Exception as exc:
        result["note"] = "NOT_CHECKED_validation_raised:%s" % type(exc).__name__
        return result
    total = len(errors)
    shown = []
    for err in errors[:MAX_DISPLAYED_VALIDATION_ERRORS]:
        message = err.message if isinstance(err.message, str) else str(err.message)
        if len(message) > MAX_ERROR_MESSAGE_CHARS:
            message = message[:MAX_ERROR_MESSAGE_CHARS] + "...[truncated]"
        shown.append({
            "path": error_path_of(err),
            "message": message,
            "validator": str(err.validator),
        })
    result["schema_status"] = "VALID" if total == 0 else "INVALID"
    result["errors"] = shown
    result["total"] = total
    result["truncated"] = total > len(shown)
    if isinstance(parsed, dict):
        warnings = collect_extra_field_warnings(parsed, schema_obj)
        result["warnings"] = warnings[:MAX_DISPLAYED_VALIDATION_ERRORS]
        result["warnings_total"] = len(warnings)
    return result


# --------------------------------------------------------------------------
# transport seam (the only place HTTP exists; tests inject a fake)
# --------------------------------------------------------------------------

class TransportError(Exception):
    """Normalized transport failure so callers never import requests."""

    def __init__(self, message, kind="NETWORK"):
        Exception.__init__(self, message)
        self.kind = kind
        self.message = message


class StreamHandle(object):
    """Minimal response contract shared by the real and the fake transport."""

    status_code = None
    headers = {}

    def iter_lines(self):
        raise NotImplementedError

    def read_text(self, limit=MAX_HTTP_ERROR_BODY_CHARS):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class Transport(object):
    """Abstract transport. open_stream() must not be called at import time."""

    name = "abstract"

    def open_stream(self, endpoint, body, timeout, headers):
        raise NotImplementedError


def classify_exception(exc):
    """Map an exception onto READ_TIMEOUT / CONNECT / NETWORK by class name.

    Class-name matching keeps this module independent of the requests package,
    which may be absent on the machine that only runs the offline tests.
    """
    name = type(exc).__name__
    if name in ("ReadTimeout", "ReadTimeoutError", "SocketTimeout"):
        return "READ_TIMEOUT"
    if name in ("ConnectTimeout", "ConnectTimeoutError"):
        return "CONNECT"
    return "NETWORK"


class RequestsStreamHandle(StreamHandle):
    def __init__(self, response):
        self._response = response
        self.status_code = response.status_code
        try:
            self.headers = {str(k).lower(): v for k, v in response.headers.items()}
        except Exception:  # pragma: no cover - defensive
            self.headers = {}

    def iter_lines(self):
        # decode_unicode=False on purpose: requests derives the encoding from
        # Content-Type and would silently pick ISO-8859-1 for text/event-stream,
        # mangling UTF-8 Chinese. Lines are decoded as UTF-8 by the collector.
        return self._response.iter_lines(decode_unicode=False)

    def read_text(self, limit=MAX_HTTP_ERROR_BODY_CHARS):
        try:
            data = self._response.content
        except Exception as exc:
            return "<unreadable error body: %s>" % type(exc).__name__
        if isinstance(data, bytes):
            data = data.decode("utf-8", "replace")
        return data[:limit]

    def close(self):
        try:
            self._response.close()
        except Exception:  # pragma: no cover - defensive
            pass


class RequestsTransport(Transport):
    """The only real HTTP implementation. Requires requests at call time only."""

    name = "requests"

    def open_stream(self, endpoint, body, timeout, headers):
        if requests is None:
            raise TransportError("the requests library is not installed", kind="NETWORK")
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                data=payload,
                stream=True,
                timeout=timeout,
            )
        except Exception as exc:
            raise TransportError(
                "%s: %s" % (type(exc).__name__, exc), kind=classify_exception(exc)
            )
        return RequestsStreamHandle(response)


# --------------------------------------------------------------------------
# raw event writer: append + flush per event
# --------------------------------------------------------------------------

class RawEventWriter(object):
    """Appends one JSON object per SSE event and flushes immediately.

    Memory stays flat: no chunk object is retained, only counters and the two
    text buffers owned by the caller. Safe for a 393k-token output.
    """

    def __init__(self, path, t0_mono):
        self.path = path
        self.t0 = t0_mono
        self.seq = 0
        self.counts = {}
        self._fh = None
        ensure_dir(os.path.dirname(path))
        if not os.path.exists(path):
            # create eagerly so the artifact always exists, even for NOT_SENT
            open(path, "a", encoding="utf-8", newline="\n").close()

    def _open(self):
        if self._fh is None:
            self._fh = open(self.path, "a", encoding="utf-8", newline="\n")
        return self._fh

    def emit(self, kind, raw_line=None, **extra):
        if kind not in EVENT_KINDS:
            raise ValueError("unknown event_kind: %s" % kind)
        fh = self._open()
        self.seq += 1
        event = {
            "seq": self.seq,
            "recv_utc": utc_stamp(),
            "mono_offset_ms": int(round((time.monotonic() - self.t0) * 1000)),
            "event_kind": kind,
        }
        if raw_line is not None:
            event["raw_line"] = raw_line
        for key in sorted(extra):
            if extra[key] is not None:
                event[key] = extra[key]
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
        fh.flush()
        self.counts[kind] = self.counts.get(kind, 0) + 1
        return self.seq

    def count(self, kind):
        return self.counts.get(kind, 0)

    def close(self):
        if self._fh is not None:
            try:
                self._fh.flush()
            finally:
                self._fh.close()
                self._fh = None


# --------------------------------------------------------------------------
# streaming chunk absorption (shared by the live loop and by local replay)
# --------------------------------------------------------------------------

def normalize_finish_reason(value):
    if value is None:
        return None
    if not isinstance(value, str):
        return "other"
    return value if value in ("stop", "length", "content_filter", "tool_calls") else "other"


def new_stream_state():
    """Per-attempt accumulator. Flat by design: no chunk object is retained."""
    return {
        "answer_parts": [],
        "reasoning_parts": [],
        "chunk_count": 0,
        "parse_error_count": 0,
        "done_seen": False,
        "terminal_seen": False,
        "finish_reason": None,
        "finish_reason_raw": None,
        "usage_raw": None,
        "provider_request_id": None,
        "saw_visible_content": False,
        "saw_reasoning": False,
        "read_error": False,
        "deadline_exceeded": False,
        "first_event_seconds": None,
        "first_reasoning_seconds": None,
        "first_visible_content_seconds": None,
        "blank_line_count": 0,
        "sse_control_line_count": 0,
        "decode_replaced_count": 0,
        "http_error_event": False,
        "transport_error_event": False,
        "error": None,
        "http_status": None,
        "retry_after_seconds_observed": None,
    }


def absorb_chunk(chunk, state):
    """Fold one provider chunk into the accumulator.

    delta.content and delta.reasoning_content go to separate buffers. Reasoning
    text is never appended to the visible answer and is never treated as an
    answer candidate. usage is kept verbatim; no token field is derived from it
    and no provider-specific field is used to estimate the visible-text volume.
    """
    if not isinstance(chunk, dict):
        return
    if state.get("provider_request_id") is None:
        rid = chunk.get("id")
        if isinstance(rid, str) and rid:
            state["provider_request_id"] = rid
    usage = chunk.get("usage")
    if usage is not None:
        state["usage_raw"] = usage
    choices = chunk.get("choices")
    if not isinstance(choices, list):
        return
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        delta = choice.get("delta")
        if not isinstance(delta, dict):
            delta = {}
        content = delta.get("content")
        if isinstance(content, str) and content:
            state["saw_visible_content"] = True
            state["answer_parts"].append(content)
        reasoning = delta.get("reasoning_content")
        if isinstance(reasoning, str) and reasoning:
            state["saw_reasoning"] = True
            state["reasoning_parts"].append(reasoning)
        finish = choice.get("finish_reason")
        if finish is not None and state.get("finish_reason_raw") is None:
            state["finish_reason_raw"] = finish
            state["finish_reason"] = normalize_finish_reason(finish)
            state["terminal_seen"] = True


def parse_retry_after(value):
    if value is None:
        return None
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def rebuild_from_raw_events(path):
    """Replay our own transcript. Used only to complete an INTERRUPTED marker.

    This is the local-replay capability required by execution plan section 5:
    it re-derives content, reasoning, chunk_count, finish_reason and terminal
    evidence from the lines we flushed while receiving. It never fabricates an
    event that was not recorded.
    """
    state = new_stream_state()
    state["event_count"] = 0
    state["malformed_event_lines"] = 0
    state["event_kind_counts"] = {}
    if not os.path.isfile(path):
        state["answer_text"] = ""
        state["reasoning_text"] = ""
        return state
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            state["event_count"] += 1
            try:
                event = json.loads(line)
            except ValueError:
                state["malformed_event_lines"] += 1
                continue
            kind = event.get("event_kind")
            state["event_kind_counts"][kind] = state["event_kind_counts"].get(kind, 0) + 1
            if kind == "DATA":
                state["chunk_count"] += 1
                raw = event.get("raw_line")
                if isinstance(raw, str):
                    payload = raw.strip()
                    if payload.startswith("data:"):
                        payload = payload[5:].strip()
                    try:
                        absorb_chunk(json.loads(payload), state)
                    except ValueError:
                        continue
            elif kind == "DONE":
                state["done_seen"] = True
                state["terminal_seen"] = True
            elif kind == "CHUNK_PARSE_ERROR":
                state["parse_error_count"] += 1
            elif kind == "READ_TIMEOUT":
                state["read_error"] = True
            elif kind == "DEADLINE_EXCEEDED":
                state["deadline_exceeded"] = True
            elif kind == "TRANSPORT_ERROR":
                state["transport_error_event"] = True
            elif kind == "HTTP_ERROR":
                state["http_error_event"] = True
            elif kind == "TERMINAL_OBSERVED":
                state["terminal_seen"] = True
            if event.get("http_status") is not None and state["http_status"] is None:
                state["http_status"] = event["http_status"]
    state["answer_text"] = "".join(state["answer_parts"])
    state["reasoning_text"] = "".join(state["reasoning_parts"])
    return state


# --------------------------------------------------------------------------
# status derivation
# --------------------------------------------------------------------------

def compute_stream_status(state, transport_status):
    """COMPLETE requires terminal evidence AND a clean read stream."""
    if transport_status in ("NOT_SENT", "HTTP_ERROR", "NETWORK_ERROR"):
        return "NOT_STARTED"
    if state["parse_error_count"] > 0:
        return "PARSE_ERROR"
    if state["terminal_seen"] and not state["read_error"] and not state["deadline_exceeded"]:
        return "COMPLETE"
    if (state["chunk_count"] > 0 or state["read_error"] or state["deadline_exceeded"]
            or state["done_seen"]):
        return "INTERRUPTED"
    return "UNKNOWN"


def compute_collection_status(stream_status, finish_reason, captured_anything):
    if stream_status == "NOT_STARTED":
        return "NO_RESPONSE"
    if stream_status == "COMPLETE":
        return "RESPONSE_CAPTURED_TRUNCATED" if finish_reason == "length" else "RESPONSE_CAPTURED"
    return "PARTIAL_STREAM_CAPTURED" if captured_anything else "NO_RESPONSE"


def compute_terminal_reason(state, transport_status):
    if transport_status != "HTTP_200":
        return None
    return state["finish_reason"] or "other"


def decide_retry(meta, limits, attempts_made):
    """Transport-level retry decision only. Never content-based.

    A visible answer that is already on disk is never re-requested because of a
    format violation or a factual disagreement, and finish_reason=length is an
    observation to record, not a transport failure.
    """
    rec = meta["record"]
    max_retries = int(limits.get("max_transport_retries", 2))
    transport = rec.get("transport_status")
    if transport == "NOT_SENT":
        return False, "NOT_SENT_NO_RETRY"
    if transport == "HTTP_ERROR":
        status = meta.get("http_status")
        if status in list(limits.get("fatal_http_status", [])):
            return False, "FATAL_HTTP_STATUS_NO_RETRY"
        if status in list(limits.get("retryable_http_status", [])):
            if attempts_made > max_retries:
                return False, "MAX_TRANSPORT_RETRIES_REACHED"
            return True, "RETRYABLE_HTTP_STATUS"
        return False, "NON_RETRYABLE_HTTP_STATUS"
    if transport == "NETWORK_ERROR":
        if attempts_made > max_retries:
            return False, "MAX_TRANSPORT_RETRIES_REACHED"
        return True, "NETWORK_ERROR_RETRY"
    stream = rec.get("stream_status")
    if stream == "COMPLETE":
        return False, "TERMINAL_RESPONSE_CAPTURED"
    if stream == "PARSE_ERROR":
        return False, "CHUNK_PARSE_ERROR_NO_CONTENT_BASED_RETRY"
    if rec.get("visible_answer_present") or rec.get("reasoning_text_present"):
        return False, "CONTENT_ALREADY_CAPTURED_NO_CONTENT_BASED_RETRY"
    if attempts_made > max_retries:
        return False, "MAX_TRANSPORT_RETRIES_REACHED"
    return True, "EMPTY_INTERRUPTED_STREAM_TRANSPORT_RETRY"


def backoff_seconds(limits, attempts_made, retry_after):
    base = float(limits.get("backoff_base_seconds", 5))
    cap = float(limits.get("backoff_cap_seconds", 30))
    delay = min(cap, base * (2 ** max(0, attempts_made - 1)))
    if limits.get("honor_retry_after", True) and retry_after is not None:
        delay = max(delay, float(retry_after))
    return delay


# --------------------------------------------------------------------------
# attempt layout, base record, artifact writing
# --------------------------------------------------------------------------

def attempt_layout(run_root, anonymous_model_id, case_id, attempt_id):
    rel_dir = "models/%s/%s/%s" % (anonymous_model_id, case_id, attempt_id)
    abs_dir = os.path.join(run_root, rel_dir)
    rel = dict((k, "%s/%s" % (rel_dir, ARTIFACT_FILENAMES[k])) for k in ARTIFACT_NAMES)
    absolute = dict((k, os.path.join(run_root, v)) for k, v in rel.items())
    return rel_dir, abs_dir, rel, absolute


def empty_timing(limits, retry_index=0):
    return {
        "start_utc": None,
        "end_utc": None,
        "wall_seconds": None,
        "first_event_seconds": None,
        "first_reasoning_seconds": None,
        "first_visible_content_seconds": None,
        "connect_timeout_seconds": limits.get("connect_timeout_seconds"),
        "read_idle_timeout_seconds": limits.get("read_idle_timeout_seconds"),
        "attempt_deadline_seconds": limits.get("attempt_deadline_seconds"),
        "retry_index": retry_index,
    }


def base_record(ctx, model_cfg, case, attempt_id, rel_paths):
    """A record that already satisfies collection_record_v2 before enrichment."""
    return {
        "record_version": RECORD_VERSION,
        "run_id": ctx.run_id,
        "phase": ctx.phase,
        "experiment_version": ctx.experiment_version,
        "route_mode": ctx.route_mode,
        "case_id": case.get("case_id"),
        "pollutant_name_zh": case.get("pollutant_name_zh") or "",
        "pollutant_name_en": case.get("pollutant_name_en") or "",
        "anonymous_model_id": model_cfg.get("anonymous_model_id"),
        "model_id": model_cfg.get("exact_model_id"),
        "idempotency_key": None,
        "request_body_sha256": None,
        "search_policy": ctx.search_policy_snapshot(),
        "prompt_sha256": ctx.prompt_template_sha256,
        "template_sha256": ctx.blank_template_sha256,
        "schema_sha256": ctx.answer_schema_sha256,
        "attempt_id": attempt_id,
        "transport_status": "NOT_SENT",
        "stream_status": "NOT_STARTED",
        "terminal_reason": None,
        "finish_reason": None,
        "visible_answer_present": False,
        "json_parse_status": "EMPTY",
        "schema_status": "NOT_CHECKED",
        "collection_status": "NO_RESPONSE",
        "answer_text": "",
        "answer_text_sha256": sha256_bytes(b""),
        "reasoning_text_present": False,
        "parsed_answer": None,
        "parser_transform": "NONE",
        "validation_errors_total": 0,
        "validation_errors": [],
        "validation_warnings": [],
        "validation_warnings_total": 0,
        "usage_raw": None,
        "timing": empty_timing(ctx.limits),
        "artifact_paths": dict(rel_paths),
        "identity_mismatch": False,
        "error": None,
        "retry_after_seconds_observed": None,
        "request_parameter_snapshot": None,
        "provider_request_id": None,
    }


DRY_RUN_ERROR = "DRY_RUN_RENDER_ONLY"
BUDGET_ERROR = "NOT_SENT_NEW_REQUEST_BUDGET_EXHAUSTED"


def is_terminal_record(rec):
    """True when this attempt reached a definitive outcome and must not be re-billed."""
    if rec.get("interrupted_marker"):
        return False
    return rec.get("transport_status") != "NOT_SENT"


def write_attempt_artifacts(ctx, rec, state, abs_paths, timing_doc, validation_doc,
                            parsed, answer_bytes, reasoning_bytes):
    atomic_write_bytes(abs_paths["answer_text"], answer_bytes)
    atomic_write_bytes(abs_paths["reasoning_content"], reasoning_bytes)
    atomic_write_text(
        abs_paths["parsed_answer"],
        json.dumps(parsed, indent=2, ensure_ascii=False) + "\n",
    )
    atomic_write_json(abs_paths["validation"], validation_doc)
    atomic_write_json(abs_paths["timing"], timing_doc)
    atomic_write_json(abs_paths["status"], rec)


def build_validation_document(ctx, rec, json_status, transform, validation_result, parsed):
    model_case_id = parsed.get("case_id") if isinstance(parsed, dict) else None
    return {
        "json_parse_status": json_status,
        "parser_transform": transform,
        "schema_status": validation_result["schema_status"],
        "validation_errors_total": validation_result["total"],
        "validation_errors_displayed": len(validation_result["errors"]),
        "validation_errors_truncated": validation_result["truncated"],
        "max_displayed_validation_errors": MAX_DISPLAYED_VALIDATION_ERRORS,
        "validation_errors": validation_result["errors"],
        "validation_warnings_total": validation_result.get("warnings_total", 0),
        "validation_warnings": validation_result.get("warnings", []),
        "extra_field_policy": ("extra fields at any nesting level are warnings only: "
                               "never a hard error, never a FAIL, never deleted"),
        "note": validation_result["note"],
        "validator": validation_result["validator"],
        "answer_schema_version": ANSWER_SCHEMA_VERSION,
        "answer_schema_sha256": ctx.answer_schema_sha256,
        "parsed_answer_present": parsed is not None,
        "dispatched_case_id": rec["case_id"],
        "model_returned_case_id": model_case_id,
        "identity_mismatch": bool(rec.get("identity_mismatch")),
        "policy": ("schema failure is recorded only: the answer is never deleted, "
                   "rewritten, repaired by a model, or re-questioned"),
    }


def build_timing_document(ctx, rec, state, t_start_mono, retry_index, tier, max_tokens,
                          answer_bytes, reasoning_bytes, event_writer=None):
    timing = dict(rec["timing"])
    doc = dict(timing)
    doc.update({
        "retry_index": retry_index,
        "tier": tier,
        "max_tokens": max_tokens,
        "http_status": state.get("http_status"),
        "chunk_count": state.get("chunk_count", 0),
        "data_event_count": state.get("chunk_count", 0),
        "chunk_parse_error_count": state.get("parse_error_count", 0),
        "done_seen": bool(state.get("done_seen")),
        "terminal_seen": bool(state.get("terminal_seen")),
        "read_error": bool(state.get("read_error")),
        "deadline_exceeded": bool(state.get("deadline_exceeded")),
        "blank_line_count": state.get("blank_line_count", 0),
        "sse_control_line_count": state.get("sse_control_line_count", 0),
        "decode_replaced_count": state.get("decode_replaced_count", 0),
        "finish_reason_raw": state.get("finish_reason_raw"),
        "answer_text_bytes": len(answer_bytes),
        "reasoning_text_bytes": len(reasoning_bytes),
        "reasoning_text_sha256": sha256_bytes(reasoning_bytes),
        "provider_request_id": state.get("provider_request_id"),
        "raw_event_line_count": (event_writer.seq if event_writer is not None
                                 else state.get("event_count", 0)),
        "event_kind_counts": dict(event_writer.counts if event_writer is not None
                                  else state.get("event_kind_counts", {})),
        "terminal_evidence": {
            "done_marker_observed": bool(state.get("done_seen")),
            "finish_reason_observed": state.get("finish_reason"),
            "terminal_observed_event": bool(
                (event_writer.count("TERMINAL_OBSERVED") if event_writer is not None
                 else state.get("event_kind_counts", {}).get("TERMINAL_OBSERVED", 0)) > 0),
        },
        "monotonic_vs_utc_note": ("*_seconds are monotonic differences; *_utc are wall-clock "
                                  "audit stamps only"),
        "started_monotonic": t_start_mono,
    })
    return doc


def write_not_sent_record(ctx, model_cfg, case, attempt_index, reason):
    """A definitive status line for a task that was never billed."""
    attempt_id = "attempt_%03d" % attempt_index
    anon = model_cfg.get("anonymous_model_id")
    case_id = case.get("case_id")
    _rel_dir, abs_dir, rel_paths, abs_paths = attempt_layout(ctx.run_root, anon, case_id, attempt_id)
    ensure_dir(abs_dir)
    rec = base_record(ctx, model_cfg, case, attempt_id, rel_paths)
    rec["transport_status"] = "NOT_SENT"
    rec["stream_status"] = "NOT_STARTED"
    rec["collection_status"] = "NO_RESPONSE"
    rec["json_parse_status"] = "EMPTY"
    rec["schema_status"] = "NOT_CHECKED"
    rec["error"] = reason
    state = new_stream_state()
    answer_bytes = b""
    reasoning_bytes = b""
    parsed, json_status, transform = None, "EMPTY", "NONE"
    validation_result = validate_answer(None, ctx.answer_schema, check=False)
    validation_doc = build_validation_document(ctx, rec, json_status, transform,
                                               validation_result, parsed)
    timing_doc = build_timing_document(ctx, rec, state, None, 0, 1, None,
                                       answer_bytes, reasoning_bytes)
    atomic_write_json(abs_paths["request"], {
        "endpoint": ctx.endpoint,
        "method": "POST",
        "body": None,
        "messages_sha256": None,
        "note": "NOT_SENT: %s" % reason,
    })
    if not os.path.exists(abs_paths["raw_events"]):
        atomic_write_bytes(abs_paths["raw_events"], b"")
    write_attempt_artifacts(ctx, rec, state, abs_paths, timing_doc, validation_doc,
                            parsed, answer_bytes, reasoning_bytes)
    return rec


def write_interrupted_marker(ctx, model_cfg, case, attempt_id, reason):
    """Complete an attempt directory whose process died before status.json.

    Written on the restart sweep so a killed run is visible instead of being
    silently re-billed. Content is reconstructed only from our own flushed
    transcript; no event is invented.
    """
    anon = model_cfg.get("anonymous_model_id")
    case_id = case.get("case_id")
    _rel_dir, abs_dir, rel_paths, abs_paths = attempt_layout(ctx.run_root, anon, case_id, attempt_id)
    ensure_dir(abs_dir)
    state = rebuild_from_raw_events(abs_paths["raw_events"])
    rec = base_record(ctx, model_cfg, case, attempt_id, rel_paths)

    request_exists = os.path.isfile(abs_paths["request"])
    if not request_exists:
        atomic_write_json(abs_paths["request"], {
            "endpoint": ctx.endpoint,
            "method": "POST",
            "body": None,
            "messages_sha256": None,
            "note": "INTERRUPTED_UNKNOWN: request.json was never written",
        })
    has_stream_evidence = (state["chunk_count"] > 0 or state["done_seen"]
                           or state["terminal_seen"])
    if has_stream_evidence:
        rec["transport_status"] = "HTTP_200"
    elif state["http_error_event"]:
        rec["transport_status"] = "HTTP_ERROR"
    elif request_exists or state["transport_error_event"] or state["event_count"] > 0:
        rec["transport_status"] = "NETWORK_ERROR"
    else:
        rec["transport_status"] = "NOT_SENT"

    captured_anything = bool(state["answer_text"]) or bool(state["reasoning_text"])
    rec["stream_status"] = "INTERRUPTED" if rec["transport_status"] != "NOT_SENT" else "NOT_STARTED"
    rec["terminal_reason"] = None
    rec["finish_reason"] = state["finish_reason"]
    if rec["finish_reason"] and not state["read_error"] and not state["deadline_exceeded"] \
            and state["parse_error_count"] == 0 and state["terminal_seen"]:
        rec["stream_status"] = "COMPLETE"
        rec["terminal_reason"] = rec["finish_reason"]
    rec["visible_answer_present"] = bool(state["answer_text"])
    rec["reasoning_text_present"] = bool(state["reasoning_text"])
    rec["collection_status"] = compute_collection_status(
        rec["stream_status"], rec["finish_reason"], captured_anything)
    rec["answer_text"] = state["answer_text"]
    rec["usage_raw"] = state["usage_raw"]
    rec["provider_request_id"] = state["provider_request_id"]
    rec["interrupted_marker"] = True
    rec["error"] = "INTERRUPTED_UNKNOWN: %s" % reason

    parsed, json_status, transform = parse_answer_text(state["answer_text"])
    validation_result = validate_answer(parsed, ctx.answer_schema, check=(json_status == "VALID"))
    rec["json_parse_status"] = json_status
    rec["parser_transform"] = transform
    rec["parsed_answer"] = parsed
    rec["schema_status"] = validation_result["schema_status"]
    rec["validation_errors_total"] = validation_result["total"]
    rec["validation_errors"] = validation_result["errors"]
    rec["validation_warnings_total"] = validation_result.get("warnings_total", 0)
    rec["validation_warnings"] = validation_result.get("warnings", [])
    if isinstance(parsed, dict):
        model_case_id = parsed.get("case_id")
        if model_case_id is not None and model_case_id != rec["case_id"]:
            rec["identity_mismatch"] = True

    answer_bytes = state["answer_text"].encode("utf-8")
    reasoning_bytes = state["reasoning_text"].encode("utf-8")
    if os.path.isfile(abs_paths["answer_text"]):
        answer_bytes = read_bytes(abs_paths["answer_text"])
    if os.path.isfile(abs_paths["reasoning_content"]):
        reasoning_bytes = read_bytes(abs_paths["reasoning_content"])
    rec["answer_text"] = answer_bytes.decode("utf-8", "replace")
    rec["answer_text_sha256"] = sha256_bytes(answer_bytes)

    validation_doc = build_validation_document(ctx, rec, json_status, transform,
                                               validation_result, parsed)
    timing_doc = build_timing_document(ctx, rec, state, None, 0, None, None,
                                       answer_bytes, reasoning_bytes)
    timing_doc["reconstructed_from_raw_events"] = True
    timing_doc["malformed_event_lines"] = state.get("malformed_event_lines", 0)
    write_attempt_artifacts(ctx, rec, state, abs_paths, timing_doc, validation_doc,
                            parsed, answer_bytes, reasoning_bytes)
    return rec


# --------------------------------------------------------------------------
# one attempt
# --------------------------------------------------------------------------

def stream_attempt(ctx, rec, state, abs_paths, body, api_key, limits, event_writer, t0_mono):
    """Open the stream and consume it, appending and flushing every event."""
    handle = None
    deadline = t0_mono + float(limits["attempt_deadline_seconds"])
    try:
        headers = build_headers(api_key) if api_key is not None else {}
        timeout = (limits["connect_timeout_seconds"], limits["read_idle_timeout_seconds"])
        try:
            handle = ctx.transport.open_stream(ctx.endpoint, body, timeout, headers)
        except TransportError as exc:
            event_writer.emit("TRANSPORT_ERROR", error=exc.message, transport_kind=exc.kind)
            state["transport_error_event"] = True
            rec["transport_status"] = "NETWORK_ERROR"
            state["error"] = "TRANSPORT_%s: %s" % (exc.kind, exc.message)
            return
        except Exception as exc:
            event_writer.emit("TRANSPORT_ERROR", error="%s: %s" % (type(exc).__name__, exc))
            state["transport_error_event"] = True
            rec["transport_status"] = "NETWORK_ERROR"
            state["error"] = "%s: %s" % (type(exc).__name__, exc)
            return

        status = getattr(handle, "status_code", None)
        state["http_status"] = status
        try:
            headers_in = dict(getattr(handle, "headers", None) or {})
        except Exception:  # pragma: no cover - defensive
            headers_in = {}
        request_id = headers_in.get("x-request-id") or headers_in.get("X-Request-Id")
        if isinstance(request_id, str) and request_id and state["provider_request_id"] is None:
            state["provider_request_id"] = request_id
        retry_after = parse_retry_after(headers_in.get("retry-after")
                                       or headers_in.get("Retry-After"))
        if retry_after is not None:
            state["retry_after_seconds_observed"] = retry_after

        if status != 200:
            try:
                error_body = handle.read_text(MAX_HTTP_ERROR_BODY_CHARS)
            except Exception as exc:
                error_body = "<unreadable error body: %s>" % type(exc).__name__
            error_body = (error_body or "")[:MAX_HTTP_ERROR_BODY_CHARS]
            event_writer.emit("HTTP_ERROR", http_status=status, error_body=error_body,
                              retry_after=retry_after)
            state["http_error_event"] = True
            rec["transport_status"] = "HTTP_ERROR"
            state["error"] = "HTTP %s: %s" % (status, error_body)
            return

        rec["transport_status"] = "HTTP_200"
        try:
            for raw_line in handle.iter_lines():
                now = time.monotonic()
                if now > deadline:
                    event_writer.emit("DEADLINE_EXCEEDED",
                                      attempt_deadline_seconds=limits["attempt_deadline_seconds"])
                    state["deadline_exceeded"] = True
                    state["error"] = state["error"] or "attempt_deadline_seconds exceeded"
                    break
                if isinstance(raw_line, bytes):
                    try:
                        line = raw_line.decode("utf-8")
                    except UnicodeDecodeError:
                        line = raw_line.decode("utf-8", "replace")
                        state["decode_replaced_count"] += 1
                elif isinstance(raw_line, str):
                    line = raw_line
                else:
                    line = str(raw_line)
                stripped = line.strip()
                if not stripped:
                    state["blank_line_count"] += 1
                    continue
                if state["first_event_seconds"] is None:
                    state["first_event_seconds"] = round(now - t0_mono, 6)
                if not stripped.startswith("data:"):
                    # SSE field/comment lines carry no payload; counted, not stored
                    state["sse_control_line_count"] += 1
                    continue
                payload = stripped[5:].strip()
                if payload == "[DONE]":
                    event_writer.emit("DONE", raw_line=line)
                    state["done_seen"] = True
                    state["terminal_seen"] = True
                    # [DONE] is the SSE terminator; stop instead of blocking on
                    # a server that keeps the connection open until read timeout.
                    break
                try:
                    chunk = json.loads(payload)
                except ValueError as exc:
                    state["parse_error_count"] += 1
                    event_writer.emit("CHUNK_PARSE_ERROR", raw_line=line, error=str(exc))
                    continue
                event_writer.emit("DATA", raw_line=line)
                state["chunk_count"] += 1
                had_content = state["saw_visible_content"]
                had_reasoning = state["saw_reasoning"]
                had_finish = state["finish_reason"]
                absorb_chunk(chunk, state)
                elapsed = round(time.monotonic() - t0_mono, 6)
                if state["saw_reasoning"] and not had_reasoning \
                        and state["first_reasoning_seconds"] is None:
                    state["first_reasoning_seconds"] = elapsed
                if state["saw_visible_content"] and not had_content \
                        and state["first_visible_content_seconds"] is None:
                    state["first_visible_content_seconds"] = elapsed
                if state["finish_reason"] and not had_finish:
                    event_writer.emit("TERMINAL_OBSERVED", finish_reason=state["finish_reason"])
        except Exception as exc:
            kind = "READ_TIMEOUT" if classify_exception(exc) == "READ_TIMEOUT" else "TRANSPORT_ERROR"
            event_writer.emit(kind, error="%s: %s" % (type(exc).__name__, exc))
            state["read_error"] = True
            state["error"] = "%s: %s" % (type(exc).__name__, exc)
        else:
            if not state["done_seen"] and not state["deadline_exceeded"]:
                event_writer.emit("EOF")
    finally:
        if handle is not None:
            try:
                handle.close()
            except Exception:  # pragma: no cover - defensive
                pass
        event_writer.emit("STREAM_CLOSED")
        event_writer.close()


def run_attempt(ctx, model_cfg, case, attempt_index, tier, max_tokens, api_key, retry_index=0):
    """Execute (or render, when dry) one attempt and return its outcome meta."""
    anon = model_cfg.get("anonymous_model_id")
    exact = model_cfg.get("exact_model_id")
    case_id = case.get("case_id")
    attempt_id = "attempt_%03d" % attempt_index
    _rel_dir, abs_dir, rel_paths, abs_paths = attempt_layout(ctx.run_root, anon, case_id, attempt_id)
    ensure_dir(abs_dir)

    rendered = ctx.prompt_for(case)
    messages = rendered["messages"]
    body = build_request_body(exact, messages, max_tokens, ctx.shared_request_parameters,
                              ctx.search_enable())
    body_sha = request_body_sha256(body)
    key = idempotency_key(ctx.phase, ctx.experiment_version, case_id, exact, body_sha)
    request_doc = {
        "endpoint": ctx.endpoint,
        "method": "POST",
        "body": body,
        "body_sha256": body_sha,
        "idempotency_key": key,
        "phase": ctx.phase,
        "experiment_version": ctx.experiment_version,
        "route_mode": ctx.route_mode,
        "messages_sha256": rendered["messages_sha256"],
        "rendered_prompt_sha256": rendered["rendered_prompt_sha256"],
        "prompt_sha256": ctx.prompt_template_sha256,
        "template_sha256": ctx.blank_template_sha256,
        "answer_schema_sha256": ctx.answer_schema_sha256,
        "record_schema_sha256": ctx.record_schema_sha256,
        "search_policy": ctx.search_policy_snapshot(),
        "tier": tier,
        "max_tokens": max_tokens,
        "model_id_exact": exact,
        "model_id_slug": sanitize_model_id(exact),
        "note": "Authorization header intentionally not stored",
    }
    atomic_write_json(abs_paths["request"], request_doc)

    rec = base_record(ctx, model_cfg, case, attempt_id, rel_paths)
    rec["request_body_sha256"] = body_sha
    rec["idempotency_key"] = key
    rec["request_parameter_snapshot"] = request_parameter_snapshot(body)
    state = new_stream_state()
    t_start_mono = time.monotonic()
    rec["timing"]["start_utc"] = utc_stamp()
    rec["timing"]["retry_index"] = retry_index

    if ctx.dry_run:
        rec["transport_status"] = "NOT_SENT"
        rec["stream_status"] = "NOT_STARTED"
        rec["collection_status"] = "NO_RESPONSE"
        rec["error"] = DRY_RUN_ERROR
        rec["timing"]["end_utc"] = utc_stamp()
        rec["timing"]["wall_seconds"] = 0.0
        answer_bytes = b""
        reasoning_bytes = b""
        parsed, json_status, transform = None, "EMPTY", "NONE"
        validation_result = validate_answer(None, ctx.answer_schema, check=False)
        validation_result["note"] = "NOT_CHECKED_dry_run_no_request_sent"
        if not os.path.exists(abs_paths["raw_events"]):
            atomic_write_bytes(abs_paths["raw_events"], b"")
        validation_doc = build_validation_document(ctx, rec, json_status, transform,
                                                   validation_result, parsed)
        timing_doc = build_timing_document(ctx, rec, state, t_start_mono, retry_index, tier,
                                           max_tokens, answer_bytes, reasoning_bytes)
        timing_doc["dry_run"] = True
        write_attempt_artifacts(ctx, rec, state, abs_paths, timing_doc, validation_doc,
                                parsed, answer_bytes, reasoning_bytes)
        return {"record": rec, "http_status": None, "retryable": False,
                "retry_reason": "DRY_RUN", "retry_after": None, "tier": tier}

    event_writer = RawEventWriter(abs_paths["raw_events"], t_start_mono)
    try:
        stream_attempt(ctx, rec, state, abs_paths, body, api_key, ctx.limits,
                       event_writer, t_start_mono)
    finally:
        event_writer.close()

    answer_text = "".join(state["answer_parts"])
    reasoning_text = "".join(state["reasoning_parts"])
    answer_bytes = answer_text.encode("utf-8")
    reasoning_bytes = reasoning_text.encode("utf-8")

    rec["stream_status"] = compute_stream_status(state, rec["transport_status"])
    rec["terminal_reason"] = compute_terminal_reason(state, rec["transport_status"])
    rec["finish_reason"] = state["finish_reason"]
    rec["visible_answer_present"] = bool(answer_text)
    rec["reasoning_text_present"] = bool(reasoning_text)
    captured_anything = bool(answer_text) or bool(reasoning_text)
    rec["collection_status"] = compute_collection_status(
        rec["stream_status"], rec["finish_reason"], captured_anything)
    rec["answer_text"] = answer_text
    rec["answer_text_sha256"] = sha256_bytes(answer_bytes)
    rec["usage_raw"] = state["usage_raw"]
    rec["provider_request_id"] = state["provider_request_id"]
    rec["retry_after_seconds_observed"] = state["retry_after_seconds_observed"]
    if state["error"]:
        rec["error"] = state["error"]

    parsed, json_status, transform = parse_answer_text(answer_text)
    validation_result = validate_answer(parsed, ctx.answer_schema, check=(json_status == "VALID"))
    rec["json_parse_status"] = json_status
    rec["parser_transform"] = transform
    rec["parsed_answer"] = parsed
    rec["schema_status"] = validation_result["schema_status"]
    rec["validation_errors_total"] = validation_result["total"]
    rec["validation_errors"] = validation_result["errors"]
    rec["validation_warnings_total"] = validation_result.get("warnings_total", 0)
    rec["validation_warnings"] = validation_result.get("warnings", [])
    if isinstance(parsed, dict):
        model_case_id = parsed.get("case_id")
        if model_case_id is not None and model_case_id != rec["case_id"]:
            # the dispatched id stays outside, the model's own value stays inside
            rec["identity_mismatch"] = True

    rec["timing"]["end_utc"] = utc_stamp()
    rec["timing"]["wall_seconds"] = round(time.monotonic() - t_start_mono, 6)
    rec["timing"]["first_event_seconds"] = state["first_event_seconds"]
    rec["timing"]["first_reasoning_seconds"] = state["first_reasoning_seconds"]
    rec["timing"]["first_visible_content_seconds"] = state["first_visible_content_seconds"]

    validation_doc = build_validation_document(ctx, rec, json_status, transform,
                                               validation_result, parsed)
    timing_doc = build_timing_document(ctx, rec, state, t_start_mono, retry_index, tier,
                                       max_tokens, answer_bytes, reasoning_bytes, event_writer)
    write_attempt_artifacts(ctx, rec, state, abs_paths, timing_doc, validation_doc,
                            parsed, answer_bytes, reasoning_bytes)

    retryable, retry_reason = decide_retry({"record": rec, "http_status": state["http_status"]},
                                           ctx.limits, retry_index + 1)
    return {"record": rec, "http_status": state["http_status"], "retryable": retryable,
            "retry_reason": retry_reason, "retry_after": state["retry_after_seconds_observed"],
            "tier": tier}


# --------------------------------------------------------------------------
# attempt selection -- pre-declared rule, never content-based
# --------------------------------------------------------------------------

SELECTION_RULE_COMPLETE = "FIRST_COMPLETE_STREAM_BY_ATTEMPT_ORDER"
SELECTION_RULE_CAPTURED = "FIRST_CAPTURED_RESPONSE_BY_ATTEMPT_ORDER"
SELECTION_RULE_FIRST = "FIRST_ATTEMPT_BY_ATTEMPT_ORDER"


def select_attempt(records):
    """Pick the first attempt that reached a terminal response.

    The rule looks only at transport/stream/collection dimensions. It never
    prefers a schema-valid, JSON-valid or otherwise better-looking answer, and
    a truncated, refused or malformed response is selected exactly like a clean
    one when it is the first terminal response.
    """
    ordered = sorted(records, key=lambda r: (r.get("attempt_id") or ""))
    if not ordered:
        return None, None
    # An INTERRUPTED_UNKNOWN marker reconstructs an attempt whose process died;
    # the contracted rule is "the first *normally terminated* response", so a
    # marker is only selectable when it is all this task has.
    candidates = [r for r in ordered if not r.get("interrupted_marker")] or ordered
    for rec in candidates:
        if rec.get("stream_status") == "COMPLETE":
            return rec, SELECTION_RULE_COMPLETE
    for rec in candidates:
        if rec.get("collection_status") != "NO_RESPONSE":
            return rec, SELECTION_RULE_CAPTURED
    return candidates[0], SELECTION_RULE_FIRST


def scan_task_attempts(ctx, model_cfg, case):
    """Return (records, next_attempt_index, held_interrupted_attempt_ids)."""
    anon = model_cfg.get("anonymous_model_id")
    case_id = case.get("case_id")
    abs_dir = os.path.join(ctx.run_root, "models", str(anon), str(case_id))
    records = []
    held = []
    next_index = 1
    if not os.path.isdir(abs_dir):
        return records, next_index, held
    for name in sorted(os.listdir(abs_dir)):
        match = ATTEMPT_DIR_RE.match(name)
        if not match:
            continue
        index = int(match.group(1))
        next_index = max(next_index, index + 1)
        attempt_id = "attempt_%03d" % index
        status_path = os.path.join(abs_dir, name, ARTIFACT_FILENAMES["status"])
        if os.path.isfile(status_path):
            try:
                rec = load_json_file(status_path)
            except ValueError:
                rec = write_interrupted_marker(
                    ctx, model_cfg, case, attempt_id, "status.json exists but is not parsable")
                records.append(rec)
                held.append(attempt_id)
                continue
            if rec.get("interrupted_marker"):
                held.append(attempt_id)
            records.append(rec)
        else:
            rec = write_interrupted_marker(
                ctx, model_cfg, case, attempt_id,
                "no terminal status.json (process exited mid-attempt)")
            records.append(rec)
            held.append(attempt_id)
    return records, next_index, held


# --------------------------------------------------------------------------
# run context
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# G4 search decision + G1..G7 stage gates + live authorization (D0 alignment)
# --------------------------------------------------------------------------

class LiveGateError(Exception):
    """Raised when a live request would be issued without the contracted gates."""


def load_search_decision(search_decision_path=None, inline=None):
    """Load the G4 search-symmetry decision. Never invents a value.

    Accepts either a path to a decision document (e.g.
    G4_search/search_symmetry_decision.json, carrying {"decision": ...}) or an
    already-loaded dict (test seam). Missing/undecided -> decision UNDECIDED
    with enable_search None, which the dispatcher refuses.
    """
    snapshot = {
        "decision": None,
        "decision_source": None,
        "decision_sha256": None,
        "enable_search": None,
    }
    data = None
    if inline is not None:
        data = inline
        snapshot["decision_source"] = "inline"
    elif search_decision_path is not None and os.path.isfile(search_decision_path):
        data = load_json_file(search_decision_path)
        snapshot["decision_source"] = os.path.abspath(search_decision_path)
        snapshot["decision_sha256"] = sha256_file(search_decision_path)
    if isinstance(data, dict):
        decision = data.get("decision")
        decided_at = data.get("decided_at") or data.get("timestamp")
        if decision in SEARCH_DECISIONS:
            snapshot["decision"] = decision
            snapshot["decided_at"] = decided_at
            snapshot["enable_search"] = SEARCH_DECISION_TO_ENABLE.get(decision)
        elif decision is not None:
            snapshot["decision"] = "UNDECIDED"
            snapshot["decision_note"] = "unrecognized decision value: %r" % (decision,)
    if snapshot["decision"] is None:
        snapshot["decision"] = "UNDECIDED"
        snapshot["decision_note"] = ("no G4 search symmetry decision supplied; "
                                     "enable_search must not be defaulted")
    return snapshot


def find_stage_gate_file(stage_gate_dir, gate_name):
    if not stage_gate_dir or not os.path.isdir(stage_gate_dir):
        return None
    for suffix in GATE_FILE_SUFFIXES:
        candidate = os.path.join(stage_gate_dir, gate_name + suffix)
        if os.path.isfile(candidate):
            return candidate
    return None


def load_stage_gates(stage_gate_dir, required_gates):
    """Load the required upstream stage_gate.json documents, in gate order.

    Each returned entry carries the gate's own fields plus a chain check
    result: gate[i].input_manifest_sha must equal gate[i-1].output_manifest_sha,
    which is how "wrong upstream hash" is detected before a live request.
    """
    entries = []
    previous_output_sha = None
    for gate_name in required_gates:
        path = find_stage_gate_file(stage_gate_dir, gate_name)
        entry = {"gate": gate_name, "path": path, "status": None,
                 "input_manifest_sha": None, "output_manifest_sha": None,
                 "chain_ok": None, "error": None}
        if path is None:
            entry["error"] = "STAGE_GATE_MISSING"
            entries.append(entry)
            previous_output_sha = None
            continue
        try:
            doc = load_json_file(path)
        except ValueError as exc:
            entry["error"] = "STAGE_GATE_UNREADABLE:%s" % exc
            entries.append(entry)
            previous_output_sha = None
            continue
        entry["status"] = doc.get("status")
        entry["input_manifest_sha"] = doc.get("input_manifest_sha")
        entry["output_manifest_sha"] = doc.get("output_manifest_sha")
        entry["stage_field"] = doc.get("stage")
        entry["reviewer"] = doc.get("reviewer")
        entry["approval_source"] = doc.get("approval_source")
        entry["timestamp"] = doc.get("timestamp")
        if entry["status"] not in LIVE_GATE_STATUSES or entry["status"] != "PASS":
            if entry["error"] is None:
                entry["error"] = "STAGE_GATE_NOT_PASS"
        if previous_output_sha is not None:
            entry["chain_ok"] = (entry["input_manifest_sha"] == previous_output_sha)
            if not entry["chain_ok"] and entry["error"] is None:
                entry["error"] = "STAGE_GATE_HASH_CHAIN_BROKEN"
        if entry["stage_field"] is not None and entry["stage_field"] != gate_name:
            if entry["error"] is None:
                entry["error"] = "STAGE_GATE_NAME_MISMATCH"
        entries.append(entry)
        previous_output_sha = entry["output_manifest_sha"]
    return entries


def evaluate_live_authorization(ctx):
    """Decide whether live API requests are authorized for this context.

    Refusal reasons (never silently ignored):
      * LIVE_DISABLED_BY_RUN_LIMITS -- the D0 package states live_disabled=true;
      * AUTHORIZED_NEW_API_REQUESTS_NOT_POSITIVE -- D0 authorizes 0 new requests;
      * SEARCH_DECISION_UNDECIDED -- enable_search must come from a G4 decision;
      * STAGE_GATE_* -- a required upstream gate is missing / not PASS / its
        input-output hash chain is broken (wrong upstream hash).
    Offline (dry-run / mock) PASS is NEVER live authorization.
    """
    refusals = []
    if ctx.limits.get("live_disabled", True):
        refusals.append({"code": "LIVE_DISABLED_BY_RUN_LIMITS",
                         "detail": "run_limits.json states live_disabled=true"})
    authorized = ctx.limits.get("authorized_new_api_requests", 0)
    if not isinstance(authorized, int) or isinstance(authorized, bool) or authorized <= 0:
        refusals.append({"code": "AUTHORIZED_NEW_API_REQUESTS_NOT_POSITIVE",
                         "detail": "authorized_new_api_requests=%r" % (authorized,)})
    # teacher-approved phase envelope: the authorization may not exceed the
    # phase's own cap, and the total envelope (80) bounds every phase package
    caps = ctx.limits.get("phase_api_request_caps") or {}
    # the caps use the teacher's stage names; map the collector phase to them
    stage_key = {"smoke": "G5_smoke", "pilot": "G6_pilot"}.get(ctx.phase)
    phase_cap = caps.get(stage_key) if stage_key else None
    if phase_cap is not None and isinstance(authorized, int) \
            and not isinstance(authorized, bool) and authorized > phase_cap:
        refusals.append({"code": "AUTHORIZED_EXCEEDS_PHASE_CAP",
                         "detail": "phase=%s authorized=%d exceeds the teacher-"
                                   "approved phase cap %d" % (ctx.phase, authorized,
                                                              phase_cap)})
    total_cap = ctx.limits.get("phase_api_total_cap")
    if isinstance(total_cap, int) and isinstance(authorized, int) \
            and not isinstance(authorized, bool) and authorized > total_cap:
        refusals.append({"code": "AUTHORIZED_EXCEEDS_TOTAL_ENVELOPE",
                         "detail": "authorized=%d exceeds the teacher-approved "
                                   "total envelope %d" % (authorized, total_cap)})
    if ctx.search_policy.get("decision") not in SEARCH_DECISION_TO_ENABLE:
        refusals.append({"code": "SEARCH_DECISION_UNDECIDED",
                         "detail": "G4 search symmetry decision is %r; enable_search "
                                   "must not be defaulted" % (ctx.search_policy.get("decision"),)})
    required_gates = list(PHASE_UPSTREAM_GATES.get(ctx.phase, ()))
    gates = load_stage_gates(ctx.stage_gate_dir, required_gates)
    for entry in gates:
        if entry.get("error"):
            refusals.append({"code": entry["error"], "gate": entry["gate"],
                             "detail": "gate file=%s status=%s input=%s output=%s"
                                       % (entry.get("path"), entry.get("status"),
                                          entry.get("input_manifest_sha"),
                                          entry.get("output_manifest_sha"))})
    return {
        "phase": ctx.phase,
        "live_requested": bool(ctx.live),
        "authorized": not refusals,
        "refusals": refusals,
        "required_gates": required_gates,
        "gate_evidence": gates,
        "search_policy": ctx.search_policy_snapshot(),
        "authorized_new_api_requests": authorized if isinstance(authorized, int)
                                       and not isinstance(authorized, bool) else 0,
        "note": "offline mock PASS is never live authorization",
    }


class RunContext(object):
    """Everything one run needs. Constructed explicitly; never at import time."""

    def __init__(self, root, run_id=None, output_root=None, cases_path=None,
                 models_config_path=None, limits_path=None, prompt_path=None,
                 template_path=None, schema_path=None, record_schema_path=None,
                 transport=None, dry_run=False, max_tier=1, resume=False,
                 resume_interrupted=False, only_models=None, only_cases=None,
                 max_new_requests=None, sleeper=None, api_key=None,
                 phase=DEFAULT_PHASE, experiment_version=DEFAULT_EXPERIMENT_VERSION,
                 route_mode="main", search_decision_path=None, search_decision=None,
                 stage_gate_dir=None, live=False):
        self.root = os.path.abspath(root)
        self.phase = str(phase)
        if self.phase not in PHASES:
            raise ValueError("phase must be one of %s: %r" % (list(PHASES), phase))
        self.experiment_version = str(experiment_version or DEFAULT_EXPERIMENT_VERSION)
        self.route_mode = str(route_mode)
        if self.route_mode not in ROUTE_MODES:
            raise ValueError("route_mode must be one of %s: %r"
                             % (list(ROUTE_MODES), route_mode))
        self.live = bool(live)
        self.stage_gate_dir = (os.path.abspath(stage_gate_dir)
                               if stage_gate_dir else None)
        self.search_policy = load_search_decision(search_decision_path,
                                                  inline=search_decision)

        self.cases_path = os.path.abspath(cases_path or os.path.join(
            self.root, "cases", "toluene_engineering_smoke.jsonl"))
        self.models_config_path = os.path.abspath(models_config_path or os.path.join(
            self.root, "config", "models.collection_v2.json"))
        self.limits_path = os.path.abspath(limits_path or os.path.join(
            self.root, "config", "run_limits.json"))
        self.prompt_path = os.path.abspath(prompt_path or os.path.join(
            self.root, "prompts", PROMPT_BASENAMES[self.route_mode]))
        self.template_path = os.path.abspath(template_path or os.path.join(
            self.root, "templates", "biodegradation_answer_v2.blank.template.json"))
        self.schema_path = os.path.abspath(schema_path or os.path.join(
            self.root, "schemas", "biodegradation_answer_v2.schema.json"))
        self.record_schema_path = os.path.abspath(record_schema_path or os.path.join(
            self.root, "schemas", "collection_record_v2.schema.json"))

        self.models_config = load_json_file(self.models_config_path)
        self.limits = dict(DEFAULT_LIMITS)
        if os.path.isfile(self.limits_path):
            self.limits.update(load_json_file(self.limits_path))
        # The old toluene shortcut key is dead: reject it loudly if a stale
        # config still carries it, so no live run can inherit the 15-request cap.
        if "total_new_api_request_cap" in self.limits:
            raise ValueError("run_limits.json still carries the removed "
                             "total_new_api_request_cap shortcut; teacher-aligned "
                             "staging authorizes requests per phase instead")

        self.run_id = run_id or self.models_config.get("run_id_default") or DEFAULT_RUN_ID
        self.phase_run_id = "%s__%s__%s" % (
            self.run_id, self.phase, sanitize_filename_component(self.experiment_version))
        self.output_root = os.path.abspath(output_root or os.path.join(self.root, "runs"))
        self.run_root = os.path.join(self.output_root, self.phase_run_id)

        self.endpoint = self.models_config.get("endpoint")
        self.api_key_env = self.models_config.get("api_key_env", "DASHSCOPE_API_KEY")
        self.shared_request_parameters = dict(self.models_config.get("shared_request_parameters") or {})
        self.shared_request_parameters.pop("enable_search", None)
        self.tier1_forbidden_parameters = list(self.models_config.get("tier1_forbidden_parameters") or [])

        self.models = list(self.models_config.get("models") or [])
        slugs = [sanitize_model_id(m.get("exact_model_id", "")) for m in self.models]
        if len(set(slugs)) != len(slugs):
            raise ValueError("model id slugs are not pairwise distinct: %s" % sorted(slugs))
        anon_ids = [m.get("anonymous_model_id") for m in self.models]
        if len(set(anon_ids)) != len(anon_ids):
            raise ValueError("anonymous_model_id values are not pairwise distinct: %s" % anon_ids)

        self.prompt_template_text = read_text(self.prompt_path)
        self.blank_template_text = read_text(self.template_path)
        self.answer_schema = load_json_file(self.schema_path)
        self.record_schema = (load_json_file(self.record_schema_path)
                              if os.path.isfile(self.record_schema_path) else None)
        self.prompt_template_sha256 = sha256_file(self.prompt_path)
        self.blank_template_sha256 = sha256_file(self.template_path)
        self.answer_schema_sha256 = sha256_file(self.schema_path)
        self.record_schema_sha256 = (sha256_file(self.record_schema_path)
                                     if os.path.isfile(self.record_schema_path) else None)
        self.cases = load_jsonl_file(self.cases_path)
        self.cases_sha256 = sha256_file(self.cases_path)
        for case in self.cases:
            if not CASE_ID_RE.match(str(case.get("case_id"))):
                raise ValueError("case_id does not match %s: %r"
                                 % (CASE_ID_RE.pattern, case.get("case_id")))
        if self.route_mode == "main":
            # Main experiment questions must carry a specified route. Cases that
            # do not are NOT silently reinterpreted as free-route questions:
            # they surface at dispatch time as pending-review NOT_SENT records.
            self.route_unspecified_case_ids = sorted(
                str(c.get("case_id")) for c in self.cases if c.get("route_scope") is None)
        else:
            self.route_unspecified_case_ids = []

        self.only_models = set(only_models or [])
        self.only_cases = set(only_cases or [])
        self.dry_run = bool(dry_run)
        self.max_tier = int(max_tier)
        self.resume = bool(resume)
        self.resume_interrupted = bool(resume_interrupted)
        self.transport = transport
        self.api_key = api_key
        self.sleeper = sleeper or time.sleep
        # In-process belt only (None = unlimited); production authorization is
        # the separate live gate, never this counter.
        self.max_new_requests = (int(max_new_requests)
                                 if max_new_requests is not None else None)

        self._lock = threading.RLock()
        self._prompt_cache = {}
        self.new_api_requests_issued = 0
        self.budget_exhausted_skips = 0
        self.task_outcomes = {}

    # -- helpers -----------------------------------------------------------

    def search_policy_snapshot(self):
        return {
            "decision": self.search_policy.get("decision"),
            "decision_source": self.search_policy.get("decision_source"),
            "decision_sha256": self.search_policy.get("decision_sha256"),
            "enable_search": self.search_policy.get("enable_search"),
        }

    def search_enable(self):
        return self.search_policy.get("enable_search")

    def prepare(self):
        for sub in ("models", "results", "normalized"):
            ensure_dir(os.path.join(self.run_root, sub))
        return self.run_root

    def tier_max_tokens(self, model_cfg, tier):
        tiers = model_cfg.get("output_budget_tiers") or {}
        value = tiers.get("tier%d_max_tokens" % int(tier))
        if value is None:
            return None if int(tier) != 1 else 16384
        return int(value)

    def take_budget_slot(self):
        with self._lock:
            if self.max_new_requests is not None and \
                    self.new_api_requests_issued >= self.max_new_requests:
                self.budget_exhausted_skips += 1
                return False
            self.new_api_requests_issued += 1
            return True

    def prompt_for(self, case):
        """Rendered prompt + messages for a case. Identical bytes for all models."""
        case_id = case.get("case_id")
        with self._lock:
            cached = self._prompt_cache.get(case_id)
        if cached is not None:
            return cached
        rendered_template = render_blank_template(self.blank_template_text, case)
        prompt_text = render_prompt(self.prompt_template_text, case, rendered_template,
                                    compact_json(self.answer_schema),
                                    route_mode=self.route_mode)
        messages = build_messages(prompt_text)
        entry = {
            "rendered_template_text": rendered_template,
            "prompt_text": prompt_text,
            "rendered_prompt_sha256": sha256_text(prompt_text),
            "messages": messages,
            "messages_sha256": messages_sha256(messages),
        }
        with self._lock:
            self._prompt_cache[case_id] = entry
        return entry

    def prospective_body_and_key(self, model_cfg, case, max_tokens):
        """The request body (and its idempotency key) a tier-1 attempt would send.

        Refuses before any bytes move when the G4 search decision is undecided:
        enable_search must never be defaulted.
        """
        rendered = self.prompt_for(case)
        body = build_request_body(model_cfg.get("exact_model_id"), rendered["messages"],
                                  max_tokens, self.shared_request_parameters,
                                  self.search_enable())
        body_sha = request_body_sha256(body)
        key = idempotency_key(self.phase, self.experiment_version, case.get("case_id"),
                              model_cfg.get("exact_model_id"), body_sha)
        return body, body_sha, key

    def validate_record(self, record):
        """Self-check against collection_record_v2. Returns a list of errors."""
        return validate_answer(record, self.record_schema, check=True)["errors"]


def build_tasks(ctx):
    tasks = []
    for model_cfg in ctx.models:
        if not model_cfg.get("enabled", True):
            continue
        anon = model_cfg.get("anonymous_model_id")
        if ctx.only_models and anon not in ctx.only_models:
            continue
        for case in ctx.cases:
            case_id = case.get("case_id")
            if ctx.only_cases and case_id not in ctx.only_cases:
                continue
            tasks.append((model_cfg, case))
    tasks.sort(key=lambda t: (t[0].get("anonymous_model_id") or "", t[1].get("case_id") or ""))
    return tasks


# --------------------------------------------------------------------------
# task execution (retry loop + gated tier2 escalation)
# --------------------------------------------------------------------------

def execute_task(ctx, model_cfg, case):
    """Run one (model, case) task. Returns {"records": [...], "outcome": str}."""
    records, next_index, held = scan_task_attempts(ctx, model_cfg, case)

    # Route policy (teacher section 1/7): the MAIN experiment prompt always
    # carries a specified route. A null route_scope never silently degrades
    # into a free-route question: the case goes to pending review, unsent.
    if ctx.route_mode == "main" and case.get("route_scope") is None:
        if any(r.get("error") == ROUTE_SCOPE_MISSING_ERROR for r in records):
            return {"records": records, "outcome": "SKIPPED_ROUTE_SCOPE_PENDING_REVIEW",
                    "held": held}
        rec = write_not_sent_record(ctx, model_cfg, case, next_index,
                                    ROUTE_SCOPE_MISSING_ERROR)
        records.append(rec)
        return {"records": records, "outcome": "PENDING_REVIEW_ROUTE_SCOPE", "held": held}

    # Search policy (teacher section 4): enable_search exists only through a G4
    # symmetry decision. No decision -> nothing is dispatched, nothing defaulted.
    if ctx.search_enable() is None:
        if any(r.get("error") == SEARCH_UNDECIDED_ERROR for r in records):
            return {"records": records, "outcome": "SKIPPED_SEARCH_UNDECIDED", "held": held}
        if any(is_terminal_record(r) for r in records):
            return {"records": records, "outcome": "SKIPPED_TERMINAL_EXISTING", "held": held}
        rec = write_not_sent_record(ctx, model_cfg, case, next_index,
                                    SEARCH_UNDECIDED_ERROR)
        records.append(rec)
        return {"records": records, "outcome": "NOT_SENT_SEARCH_UNDECIDED", "held": held}

    tier = 1
    max_tokens = ctx.tier_max_tokens(model_cfg, tier)
    _body, _body_sha, prospective_key = ctx.prospective_body_and_key(model_cfg, case,
                                                                     max_tokens)
    # Idempotency (teacher section 8.1): skip only a terminal record whose
    # idempotency key matches this phase + experiment version + body. A smoke
    # or pilot terminal record therefore never satisfies a formal run.
    if any(is_terminal_record(r) and r.get("idempotency_key") == prospective_key
           for r in records):
        return {"records": records, "outcome": "SKIPPED_TERMINAL_EXISTING", "held": held}
    if held and not ctx.resume_interrupted:
        return {"records": records, "outcome": "HELD_INTERRUPTED", "held": held}
    if ctx.dry_run and any(r.get("error") == DRY_RUN_ERROR for r in records):
        return {"records": records, "outcome": "SKIPPED_DRY_RUN_ALREADY_RENDERED", "held": held}

    api_key = None if ctx.dry_run else ctx.api_key
    attempts_made = 0
    index = next_index
    retry_trace = []
    while True:
        if not ctx.dry_run and not ctx.take_budget_slot():
            records.append(write_not_sent_record(ctx, model_cfg, case, index, BUDGET_ERROR))
            retry_trace.append({"attempt_index": index, "decision": "BUDGET_EXHAUSTED"})
            break
        meta = run_attempt(ctx, model_cfg, case, index, tier, max_tokens, api_key,
                           retry_index=attempts_made)
        records.append(meta["record"])
        retry_trace.append({
            "attempt_index": index,
            "tier": tier,
            "attempt_id": meta["record"].get("attempt_id"),
            "idempotency_key": meta["record"].get("idempotency_key"),
            "transport_status": meta["record"].get("transport_status"),
            "stream_status": meta["record"].get("stream_status"),
            "http_status": meta.get("http_status"),
            "retryable": bool(meta.get("retryable")),
            "retry_reason": meta.get("retry_reason"),
        })
        index += 1
        attempts_made += 1
        if ctx.dry_run or not meta.get("retryable"):
            break
        delay = backoff_seconds(ctx.limits, attempts_made, meta.get("retry_after"))
        ctx.sleeper(delay)

    if not ctx.dry_run and ctx.max_tier >= 2:
        tier2_tokens = ctx.tier_max_tokens(model_cfg, 2)
        gate_ok = bool(ctx.limits.get("tier2_allowed_only_when_documented_higher_cap", True))
        allowed_per_model = int(ctx.limits.get("tier2_max_attempts_per_model", 1))
        selected, _rule = select_attempt(records)
        if (tier2_tokens and gate_ok and allowed_per_model > 0 and tier2_tokens > (max_tokens or 0)
                and selected is not None and selected.get("finish_reason") == "length"
                and ctx.take_budget_slot()):
            meta = run_attempt(ctx, model_cfg, case, index, 2, tier2_tokens, api_key,
                               retry_index=attempts_made)
            records.append(meta["record"])
            retry_trace.append({
                "attempt_index": index, "tier": 2,
                "attempt_id": meta["record"].get("attempt_id"),
                "transport_status": meta["record"].get("transport_status"),
                "stream_status": meta["record"].get("stream_status"),
                "http_status": meta.get("http_status"),
                "retryable": False, "retry_reason": "TIER2_ESCALATION",
            })
    return {"records": records, "outcome": "EXECUTED", "held": held,
            "attempt_trace": retry_trace}


def run_all(ctx):
    """Execute every task with a global thread pool and a per-model lock."""
    ctx.prepare()
    tasks = build_tasks(ctx)
    results = {}
    if not tasks:
        return results
    if not ctx.dry_run and ctx.api_key is None:
        raise KeyLoadError("no API key loaded; a real run requires --key-env-file")
    if not ctx.dry_run and ctx.transport is None:
        # Production path: this module would install the REAL HTTP transport by
        # itself, so live authorization is checked here as a hard guard. Offline
        # mock tests inject a transport through the seam and never hit this.
        gate = evaluate_live_authorization(ctx)
        if not gate["authorized"]:
            raise LiveGateError(
                "live API requests are not authorized (phase=%s): %s"
                % (ctx.phase, json.dumps(gate["refusals"], ensure_ascii=False)))
        ctx.live_gate = gate
        ctx.transport = RequestsTransport()

    per_model_locks = dict((m.get("anonymous_model_id"), threading.Lock()) for m in ctx.models)

    def work(task):
        model_cfg, case = task
        lock = per_model_locks.get(model_cfg.get("anonymous_model_id"))
        if lock is None:
            lock = threading.Lock()
            per_model_locks[model_cfg.get("anonymous_model_id")] = lock
        with lock:  # per_model_concurrency = 1
            return task, execute_task(ctx, model_cfg, case)

    workers = max(1, min(int(ctx.limits.get("global_concurrency", 5)), len(tasks)))
    if workers <= 1 or len(tasks) <= 1:
        for task in tasks:
            _task, outcome = work(task)
            results[(task[0].get("anonymous_model_id"), task[1].get("case_id"))] = outcome
        return results
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(work, task) for task in tasks]
        for future in concurrent.futures.as_completed(futures):
            task, outcome = future.result()
            results[(task[0].get("anonymous_model_id"), task[1].get("case_id"))] = outcome
    return results


# --------------------------------------------------------------------------
# results / normalized / manifest / SHA256SUMS
# --------------------------------------------------------------------------

def result_filename(case, model_cfg):
    return "%s__%s__%s.json" % (
        sanitize_filename_component(str(case.get("case_id"))),
        sanitize_filename_component(str(case.get("pollutant_name_en") or "unknown")),
        sanitize_filename_component(sanitize_model_id(str(model_cfg.get("exact_model_id")))),
    )


def write_results_and_normalized(ctx, tasks, results):
    """Selected record per task into results/ and normalized/*.jsonl.

    Every task gets exactly one line in all_models.jsonl, including tasks that
    were never sent: 750 terminal records are not the same claim as 750
    complete answers, and the missing ones must be visible.
    """
    results_dir = os.path.join(ctx.run_root, "results")
    normalized_dir = os.path.join(ctx.run_root, "normalized")
    ensure_dir(results_dir)
    ensure_dir(normalized_dir)

    per_model_selected = dict((m.get("anonymous_model_id"), []) for m in ctx.models)
    all_selected = []
    all_attempts = []
    selected_rows = []

    for model_cfg, case in tasks:
        anon = model_cfg.get("anonymous_model_id")
        case_id = case.get("case_id")
        outcome = results.get((anon, case_id)) or {"records": [], "outcome": "TASK_MISSING"}
        records = list(outcome.get("records") or [])
        all_attempts.extend(records)
        if records:
            selected, rule = select_attempt(records)
        else:
            selected = write_not_sent_record(ctx, model_cfg, case, 1, "TASK_MISSING_NO_ATTEMPT")
            all_attempts.append(selected)
            rule = "SYNTHESIZED_STATUS_LINE_FOR_MISSING_TASK"
        row = dict(selected)
        row["selected_attempt"] = selected.get("attempt_id")
        row["selection_rule"] = rule
        results_path = os.path.join(results_dir, result_filename(case, model_cfg))
        atomic_write_json(results_path, row)
        per_model_selected.setdefault(anon, []).append(row)
        all_selected.append(row)
        selected_rows.append(row)
        with ctx._lock:
            ctx.task_outcomes[outcome.get("outcome", "UNKNOWN")] = \
                ctx.task_outcomes.get(outcome.get("outcome", "UNKNOWN"), 0) + 1

    for anon in sorted(per_model_selected):
        rows = sorted(per_model_selected[anon], key=lambda r: (r.get("case_id") or ""))
        atomic_write_jsonl(os.path.join(normalized_dir, "model_%s.jsonl" % anon), rows)
    atomic_write_jsonl(
        os.path.join(normalized_dir, "all_models.jsonl"),
        sorted(all_selected, key=lambda r: (r.get("anonymous_model_id") or "",
                                            r.get("case_id") or "")))
    atomic_write_jsonl(
        os.path.join(normalized_dir, "all_attempts.jsonl"),
        sorted(all_attempts, key=lambda r: (r.get("anonymous_model_id") or "",
                                            r.get("case_id") or "",
                                            r.get("attempt_id") or "")))
    return {"selected": selected_rows, "attempts": all_attempts}


def status_counts(records):
    counts = {
        "records": len(records),
        "RESPONSE_CAPTURED": 0,
        "RESPONSE_CAPTURED_TRUNCATED": 0,
        "PARTIAL_STREAM_CAPTURED": 0,
        "NO_RESPONSE": 0,
        "visible_answer_present": 0,
        "json_parse_VALID": 0,
        "json_parse_INVALID": 0,
        "json_parse_EMPTY": 0,
        "schema_VALID": 0,
        "schema_INVALID": 0,
        "schema_NOT_CHECKED": 0,
        "stream_COMPLETE": 0,
        "stream_not_COMPLETE": 0,
    }
    for rec in records:
        cs = rec.get("collection_status")
        if cs in counts:
            counts[cs] += 1
        if rec.get("visible_answer_present"):
            counts["visible_answer_present"] += 1
        jp = rec.get("json_parse_status")
        if jp in JSON_PARSE_STATUSES:
            counts["json_parse_%s" % jp] += 1
        ss = rec.get("schema_status")
        if ss in SCHEMA_STATUSES:
            counts["schema_%s" % ss] += 1
        if rec.get("stream_status") == "COMPLETE":
            counts["stream_COMPLETE"] += 1
        else:
            counts["stream_not_COMPLETE"] += 1
    return counts


def write_run_manifest(ctx, tasks, selected, attempts):
    models = []
    for model_cfg in ctx.models:
        exact = model_cfg.get("exact_model_id")
        models.append({
            "anonymous_model_id": model_cfg.get("anonymous_model_id"),
            "exact_model_id": exact,
            "filesystem_slug": sanitize_model_id(exact),
            "enabled": bool(model_cfg.get("enabled", True)),
            "per_model_concurrency": model_cfg.get("per_model_concurrency", 1),
            "tier1_max_tokens": ctx.tier_max_tokens(model_cfg, 1),
            "tier2_max_tokens": ctx.tier_max_tokens(model_cfg, 2),
            "parameter_contract_evidence_status":
                model_cfg.get("parameter_contract_evidence_status"),
        })
    if ctx.models and ctx.search_enable() is not None:
        body_sample = build_request_body("<exact_model_id>",
                                         [{"role": "user", "content": "<prompt>"}],
                                         ctx.tier_max_tokens(ctx.models[0], 1),
                                         ctx.shared_request_parameters,
                                         ctx.search_enable())
    elif ctx.models:
        body_sample = {"note": "no frozen body: G4 search decision is UNDECIDED"}
    else:
        body_sample = {}
    manifest = {
        "run_id": ctx.run_id,
        "phase_run_id": ctx.phase_run_id,
        "phase": ctx.phase,
        "experiment_version": ctx.experiment_version,
        "route_mode": ctx.route_mode,
        "live_authorized": bool(getattr(ctx, "live_gate", {}).get("authorized", False))
                           if not ctx.dry_run else False,
        "live_gate": getattr(ctx, "live_gate", None),
        "search_policy": ctx.search_policy_snapshot(),
        "generated_utc": utc_stamp(),
        "dry_run": bool(ctx.dry_run),
        "max_tier": ctx.max_tier,
        "endpoint": ctx.endpoint,
        "api_key_env": ctx.api_key_env,
        "api_key_value": "NEVER_STORED",
        "artifacts": {
            "prompt_template": {"path": ctx.prompt_path, "sha256": ctx.prompt_template_sha256,
                                "route_mode": ctx.route_mode},
            "blank_template": {"path": ctx.template_path, "sha256": ctx.blank_template_sha256},
            "answer_schema": {"path": ctx.schema_path, "sha256": ctx.answer_schema_sha256},
            "record_schema": {"path": ctx.record_schema_path, "sha256": ctx.record_schema_sha256},
            "cases": {"path": ctx.cases_path, "sha256": ctx.cases_sha256,
                      "count": len(ctx.cases),
                      "route_unspecified_case_ids": ctx.route_unspecified_case_ids},
            "models_config": {"path": ctx.models_config_path,
                              "sha256": sha256_file(ctx.models_config_path)},
            "limits_config": {"path": ctx.limits_path,
                              "sha256": (sha256_file(ctx.limits_path)
                                         if os.path.isfile(ctx.limits_path) else None)},
        },
        "models": models,
        "slug_uniqueness": {
            "count": len(models),
            "distinct": len(set(m["filesystem_slug"] for m in models)) == len(models),
        },
        "shared_request_parameters": ctx.shared_request_parameters,
        "request_body_key_order_sample": list(body_sample.keys()),
        "tier1_forbidden_parameters": ctx.tier1_forbidden_parameters,
        "limits": ctx.limits,
        "requests": {
            "planned_tasks": len(tasks),
            "new_api_requests_issued": ctx.new_api_requests_issued,
            "in_process_request_belt": ctx.max_new_requests,
            "authorized_new_api_requests": ctx.limits.get("authorized_new_api_requests"),
            "budget_exhausted_skips": ctx.budget_exhausted_skips,
            "attempt_records_total": len(attempts),
            "selected_records_total": len(selected),
            # What this invocation actually dispatched. "models" above documents
            # the frozen five-model contract; --only-models / --only-cases make
            # the dispatched subset smaller, and the validator must compare
            # against the subset, not against the contract.
            "dispatched_anonymous_model_ids": sorted(set(
                str(m.get("anonymous_model_id")) for m, _c in tasks
                if m.get("anonymous_model_id"))),
            "dispatched_case_ids": sorted(set(
                str(c.get("case_id")) for _m, c in tasks if c.get("case_id"))),
        },
        "task_outcomes": dict(sorted(ctx.task_outcomes.items())),
        "status_counts_selected": status_counts(selected),
        "status_counts_all_attempts": status_counts(attempts),
        "unit_price_cny": "UNKNOWN",
        "cost_cny": "UNKNOWN",
        "selection_rule_vocabulary": [
            SELECTION_RULE_COMPLETE, SELECTION_RULE_CAPTURED, SELECTION_RULE_FIRST],
        "policy_notes": [
            "format conformance is an observation, never a scoring or deletion gate",
            "no gold comparison, no scientific judgement, no content-based retry, no re-question",
            "reasoning_content is stored separately and is never promoted into answer_text",
            "usage_raw is preserved verbatim; no token field is derived from it",
            "extra fields at any nesting level are warnings only, never deleted",
            "enable_search is frozen from the G4 symmetry decision, never defaulted true",
            "phase + experiment_version + case + model + request body hash form the idempotency key",
            "offline mock PASS is never live authorization",
        ],
    }
    atomic_write_json(os.path.join(ctx.run_root, "run_manifest.json"), manifest)
    return manifest


def is_allowed_run_relpath(rel):
    """True when rel is one of the explicitly whitelisted run artifacts."""
    parts = rel.split("/")
    top = parts[0]
    base = parts[-1]
    if len(parts) == 1:
        return base in RUN_ROOT_FILES
    if top == "models":
        # models/<anonymous_model_id>/<CASE_ID>/attempt_NNN/<artifact>
        return len(parts) == 5 and base in ARTIFACT_FILENAMES.values()
    if top == "results":
        return len(parts) == 2 and bool(RESULT_FILENAME_RE.match(base))
    if top == "normalized":
        if len(parts) != 2 or not base.endswith(".jsonl"):
            return False
        return base in NORMALIZED_AGGREGATE_FILES or bool(PER_MODEL_JSONL_RE.match(base))
    if top == "summaries":
        return len(parts) == 2 and base.endswith(".tsv")
    return False


def collect_run_files(root):
    """Sorted (relpath, abspath) for every regular file under root.

    Walks everything: a directory that happens to contain a SHA256SUMS is never
    skipped as a whole, which was the v1 summarize.py defect.
    """
    items = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            absolute = os.path.join(dirpath, name)
            if os.path.islink(absolute) or not os.path.isfile(absolute):
                continue
            rel = os.path.relpath(absolute, root).replace(os.sep, "/")
            items.append((rel, absolute))
    items.sort(key=lambda item: item[0])
    return items


def write_sha256sums(root):
    """Sorted, one line per file, only SHA256SUMS itself excluded."""
    lines = []
    for rel, absolute in collect_run_files(root):
        if rel == "SHA256SUMS":
            continue
        lines.append("%s  %s" % (sha256_file(absolute), rel))
    atomic_write_text(os.path.join(root, "SHA256SUMS"), "".join(line + "\n" for line in lines))
    return len(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def parse_csv(value):
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def build_arg_parser(default_root=None):
    if default_root is None:
        default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(
        prog="run_collection_v2.py",
        description="BIOSYSMOdb150 five-LLM answer collector v2 (engineering capture only; "
                    "no gold comparison, no scientific judgement, no content-based retry).",
    )
    parser.add_argument("--root", default=default_root,
                        help="collector root (default: parent of the scripts directory)")
    parser.add_argument("--cases", default=None, help="cases JSONL (default: <root>/cases/...)")
    parser.add_argument("--models-config", default=None)
    parser.add_argument("--limits-config", default=None)
    parser.add_argument("--prompt", default=None)
    parser.add_argument("--template", default=None)
    parser.add_argument("--schema", default=None, help="answer schema (biodegradation_answer_v2)")
    parser.add_argument("--record-schema", default=None, help="collection_record_v2 schema")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output-root", default=None, help="default: <root>/runs")
    parser.add_argument("--tier", type=int, choices=(1, 2), default=1,
                        help="maximum output-budget tier allowed (2 enables gated escalation)")
    parser.add_argument("--phase", default=DEFAULT_PHASE, choices=PHASES,
                        help="staging phase: enters the run directory layout AND the "
                             "idempotency key, so formal never reuses smoke/pilot records")
    parser.add_argument("--experiment-version", default=DEFAULT_EXPERIMENT_VERSION,
                        help="frozen experiment version (template/schema/parameter "
                             "generation); part of the idempotency key")
    parser.add_argument("--route-mode", default="main", choices=ROUTE_MODES,
                        help="main = route specified by the question (primary "
                             "experiment); exploratory = separate free-route "
                             "experiment with its own prompt and hash")
    parser.add_argument("--search-decision", default=None,
                        help="path to the G4 search-symmetry decision document "
                             "(decision: ALL_PASS -> enable_search true, ANY_NOT_PASS "
                             "-> false); without it live dispatch is refused")
    parser.add_argument("--stage-gate-dir", default=None,
                        help="directory holding <Gate>.stage_gate.json PASS files for "
                             "this phase's upstream gates (G1..G7 per phase)")
    parser.add_argument("--live", action="store_true",
                        help="authorize live API requests for this phase; requires the "
                             "run limits NOT to disable live, a positive authorized "
                             "request count, a decided search policy and PASS upstream "
                             "gates. D0 packages ship live_disabled=true.")
    parser.add_argument("--dry-run", action="store_true",
                        help="render requests and SHAs only: no key is loaded, nothing is sent")
    parser.add_argument("--resume", action="store_true",
                        help="continue an existing run directory without re-billing terminal tasks")
    parser.add_argument("--resume-interrupted", action="store_true",
                        help="also issue a new attempt for directories held as INTERRUPTED_UNKNOWN")
    parser.add_argument("--key-env-file", default=None,
                        help="external chmod-600 file holding DASHSCOPE_API_KEY")
    parser.add_argument("--only-models", default=None, help="comma-separated anonymous ids")
    parser.add_argument("--only-cases", default=None, help="comma-separated case ids")
    parser.add_argument("--max-new-requests", type=int, default=None,
                        help="cap on newly billed requests for this invocation")
    parser.add_argument("--quiet", action="store_true")
    return parser


def build_run_context_from_args(args, transport=None):
    return RunContext(
        root=args.root,
        run_id=args.run_id,
        output_root=args.output_root,
        cases_path=args.cases,
        models_config_path=args.models_config,
        limits_path=args.limits_config,
        prompt_path=args.prompt,
        template_path=args.template,
        schema_path=args.schema,
        record_schema_path=args.record_schema,
        transport=transport,
        dry_run=args.dry_run,
        max_tier=args.tier,
        resume=args.resume,
        resume_interrupted=args.resume_interrupted,
        only_models=parse_csv(args.only_models),
        only_cases=parse_csv(args.only_cases),
        max_new_requests=args.max_new_requests,
        phase=args.phase,
        experiment_version=args.experiment_version,
        route_mode=args.route_mode,
        search_decision_path=args.search_decision,
        stage_gate_dir=args.stage_gate_dir,
        live=args.live,
    )


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    ctx = build_run_context_from_args(args)

    if ctx.dry_run:
        print("api_key: NOT_LOADED (--dry-run never reads a key)")
        print("phase=%s experiment_version=%s route_mode=%s"
              % (ctx.phase, ctx.experiment_version, ctx.route_mode))
        print("search_policy: %s" % json.dumps(ctx.search_policy_snapshot(),
                                               ensure_ascii=False))
        ctx.transport = _NullTransport()
    else:
        # Live authorization is checked BEFORE any key is loaded and BEFORE any
        # transport exists: a refused run touches no secret and no network.
        if not args.live:
            print("LIVE_REFUSED: %s" % "live requests require --live (this D0 package "
                                       "authorizes 0 new API requests)")
            return 2
        gate = evaluate_live_authorization(ctx)
        if not gate["authorized"]:
            print("LIVE_REFUSED: phase=%s" % ctx.phase)
            for refusal in gate["refusals"]:
                print("  %s %s" % (refusal.get("code"), refusal.get("detail", "")))
            return 2
        ctx.live_gate = gate
        if args.max_new_requests is not None:
            authorized = gate["authorized_new_api_requests"]
            if args.max_new_requests > authorized:
                print("LIVE_REFUSED: --max-new-requests=%d exceeds authorized_new_"
                      "api_requests=%d" % (args.max_new_requests, authorized))
                return 2
        try:
            ctx.api_key = load_api_key(args.key_env_file, ctx.api_key_env)
        except KeyLoadError as exc:
            print("api_key: MISSING (%s)" % exc)
            return 3
        print("api_key: PRESENT")
        print("phase=%s experiment_version=%s route_mode=%s live_authorized=true"
              % (ctx.phase, ctx.experiment_version, ctx.route_mode))
        print("search_policy: %s" % json.dumps(ctx.search_policy_snapshot(),
                                               ensure_ascii=False))
        ctx.transport = RequestsTransport()

    ctx.prepare()
    tasks = build_tasks(ctx)
    print("run_id=%s phase_run_id=%s tasks=%d models=%d cases=%d dry_run=%s max_tier=%d"
          % (ctx.run_id, ctx.phase_run_id, len(tasks), len(ctx.models), len(ctx.cases),
             ctx.dry_run, ctx.max_tier))

    results = run_all(ctx)
    written = write_results_and_normalized(ctx, tasks, results)
    manifest = write_run_manifest(ctx, tasks, written["selected"], written["attempts"])
    sums_rows = write_sha256sums(ctx.run_root)

    unknown = [rel for rel, _abs in collect_run_files(ctx.run_root)
               if not is_allowed_run_relpath(rel)]
    if unknown:
        print("UNEXPECTED_RUN_FILES=%s" % unknown)

    scan = scan_artifacts_for_leaks(
        [abs_path for _rel, abs_path in collect_run_files(ctx.run_root)], ctx.api_key)
    if scan["hard_failures"]:
        print("LEAK_SCAN: FAIL %d hard finding(s)" % len(scan["hard_failures"]))
        for finding in scan["hard_failures"]:
            print("  %s pattern=%s count=%s" % (finding["path"], finding["pattern"],
                                                finding["count"]))
        return 2
    print("LEAK_SCAN: PASS (reported_findings=%d)" % len(scan["reported_findings"]))

    if not args.quiet:
        print("task_outcomes=%s" % json.dumps(manifest["task_outcomes"], ensure_ascii=False))
        print("status_counts_selected=%s"
              % json.dumps(manifest["status_counts_selected"], ensure_ascii=False))
        print("new_api_requests_issued=%d in_process_belt=%s budget_exhausted_skips=%d"
              % (ctx.new_api_requests_issued, ctx.max_new_requests,
                 ctx.budget_exhausted_skips))
        print("SHA256SUMS rows=%d" % sums_rows)
        print("run_root=%s" % ctx.run_root)
    return 0


class _NullTransport(Transport):
    """Guards --dry-run: any attempt to open a stream is a hard programming error."""

    name = "null"

    def open_stream(self, endpoint, body, timeout, headers):
        raise AssertionError("--dry-run must never open a stream")


if __name__ == "__main__":
    sys.exit(main())
