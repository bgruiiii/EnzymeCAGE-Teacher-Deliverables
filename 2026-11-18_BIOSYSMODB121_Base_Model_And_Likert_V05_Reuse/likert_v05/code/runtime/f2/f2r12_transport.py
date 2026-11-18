"""F2 R1.1 transport (audit F2R1-P1-03 + P2-01 + P2-02 fixes on top of the
R1 SSE receiver).

Fixes over R1:
  - RAW BYTE FIDELITY (P2-01): the stream path accumulates the ACTUAL arrived
    bytes via iter_content (CRLF preserved exactly; no line re-joining, no
    locally-injected markers inside the provider payload). SSE parsing works
    on a COPY of the raw bytes; read errors are recorded in meta only. Error
    bodies are length-capped with an explicit truncated flag + full length.
  - CONNECTION-LOSS ACCOUNTING (P1-03): once session.post has been entered,
    the request may already be uploaded; only exceptions that provably occur
    BEFORE any byte is sent (invalid URL/missing schema — raised during
    request construction) release the reservation. ConnectionError /
    RemoteDisconnected / Timeout / ChunkedEncoding / anything else →
    may_have_billed=True (UNKNOWN_INFLIGHT); we never assume "not a Timeout
    ⇒ not billed".
  - MODEL IDENTITY HONESTY (P2-02): a missing provider `model` field yields
    model_returned=None + model_identity="NOT_PROVIDED_BY_PROVIDER"; the
    requested model is NEVER copied into the actual field; the runner records
    the verification state and the F4 first-batch gate must observe real
    provider behaviour and freeze the disclosure policy.

Testability: injectable session (FakeSession/FakeResponse with iter_content
support) drives the REAL send/parse path offline. `requests` is imported only
when no session is injected (under the runner's live gate).

Offline: importing this module performs no network I/O.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import sha256_bytes, utc_now_iso

SAFE_HEADER_ALLOWLIST = ("content-type", "x-request-id", "x-dashscope-osshsa",
                         "retry-after", "x-ratelimit-limit-requests",
                         "x-ratelimit-remaining-requests", "date", "server")
MAX_ERROR_BODY_BYTES = 64 * 1024
# Exception type names provably raised BEFORE any byte hits the wire
# (request-construction errors in the requests library):
PRE_DISPATCH_ERROR_NAMES = {"InvalidURL", "MissingSchema", "InvalidSchema",
                            "URLRequired", "InvalidHeader"}
_LINE_SPLIT = re.compile(rb"\r\n|\r|\n")


def _safe_headers(headers) -> dict:
    out = {}
    try:
        items = headers.items()
    except AttributeError:
        return out
    for k, v in items:
        kl = str(k).lower()
        if kl in SAFE_HEADER_ALLOWLIST:
            out[kl] = str(v)
    return out


def new_stream_state() -> dict:
    return {
        "content_parts": [], "reasoning_parts": [],
        "usage_raw": None, "finish_reason_raw": None,
        "provider_request_id": None, "model_returned": None,
        "chunk_count": 0, "chunk_parse_errors": 0,
        "done_seen": False, "terminal_seen": False,
        "read_error": None, "blank_line_count": 0, "sse_control_line_count": 0,
    }


def absorb_chunk(chunk, state: dict):
    """Ported from run_collection_v2.absorb_chunk (484 real calls)."""
    if not isinstance(chunk, dict):
        return
    if state.get("provider_request_id") is None:
        rid = chunk.get("id")
        if isinstance(rid, str) and rid:
            state["provider_request_id"] = rid
    if state.get("model_returned") is None:
        mdl = chunk.get("model")
        if isinstance(mdl, str) and mdl:
            state["model_returned"] = mdl
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
            state["content_parts"].append(content)
        reasoning = delta.get("reasoning_content")
        if isinstance(reasoning, str) and reasoning:
            state["reasoning_parts"].append(reasoning)
        finish = choice.get("finish_reason")
        if finish is not None and state.get("finish_reason_raw") is None:
            state["finish_reason_raw"] = finish
            state["terminal_seen"] = True


def parse_sse_bytes(raw: bytes, state: dict) -> str:
    """Parse SSE from a COPY of the exact arrived bytes (universal newline
    split for parsing only — the archived raw stays byte-exact incl. CRLF)."""
    for line in _LINE_SPLIT.split(raw):
        stripped = line.strip()
        if not stripped:
            state["blank_line_count"] += 1
            continue
        if not stripped.startswith(b"data:"):
            state["sse_control_line_count"] += 1
            continue
        payload = stripped[5:].strip()
        if payload == b"[DONE]":
            state["done_seen"] = True
            state["terminal_seen"] = True
            break
        try:
            chunk = json.loads(payload.decode("utf-8", "replace"),
                               parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c)))
        except (ValueError, UnicodeDecodeError):
            state["chunk_parse_errors"] += 1
            continue
        state["chunk_count"] += 1
        absorb_chunk(chunk, state)
    return "".join(state["content_parts"])


def parse_non_stream_bytes(raw: bytes, state: dict):
    text = raw.decode("utf-8", "replace")
    env = json.loads(text,
                     parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c)))
    if not isinstance(env, dict):
        raise ValueError("envelope is not a JSON object")
    state["provider_request_id"] = env.get("id")
    state["model_returned"] = env.get("model")
    state["usage_raw"] = env.get("usage")
    state["chunk_count"] = 1
    choices = env.get("choices")
    content = None
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        msg = choices[0].get("message") or {}
        content = msg.get("content")
        state["finish_reason_raw"] = choices[0].get("finish_reason")
        if state["finish_reason_raw"] is not None:
            state["terminal_seen"] = True
        reasoning = msg.get("reasoning_content")
        if isinstance(reasoning, str) and reasoning:
            state["reasoning_parts"].append(reasoning)
    if isinstance(content, str):
        state["content_parts"].append(content)
        return content
    return None


class WireOutcome(dict):
    """Transport result. R1.1 additions:
      model_identity: PROVIDED | NOT_PROVIDED_BY_PROVIDER
      raw_truncated: bool + raw_full_length (error-body cap disclosure)
      read_error: str|None (meta only — NEVER injected into raw bytes)
    """


class LiveTransport:
    def __init__(self, endpoint: str, api_key: str | None, session=None,
                 stream: bool = True):
        self.endpoint = endpoint
        self.stream = stream
        self._session = session
        if session is None:
            if not api_key:
                raise RuntimeError("api_key required when no session injected")
            import requests  # only here, under the runner's live gate
            self._session = requests.Session()
            self._session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"})

    def send(self, request: dict, timeout: int) -> WireOutcome:
        body = dict(request["body"])
        body["stream"] = bool(self.stream)
        if self.stream:
            body.setdefault("stream_options", {"include_usage": True})
        body_bytes = json.dumps(body, ensure_ascii=False).encode("utf-8")
        out = WireOutcome(http_status=None, raw_response_bytes=None,
                          raw_response_sha256=None, raw_truncated=False,
                          raw_full_length=None, safe_headers={},
                          provider_request_id=None, model_returned=None,
                          model_identity="NOT_PROVIDED_BY_PROVIDER",
                          usage=None, finish_reason=None,
                          stream_status="NOT_STARTED", content_text=None,
                          error_kind=None, may_have_billed=False,
                          read_error=None,
                          started_utc=utc_now_iso(), ended_utc=None,
                          request_body_sha256=sha256_bytes(body_bytes),
                          request_body_bytes_len=len(body_bytes))
        state = new_stream_state()
        try:
            resp = self._session.post(self.endpoint, data=body_bytes,
                                      timeout=timeout, stream=self.stream)
        except Exception as e:
            name = type(e).__name__
            # P1-03: only provable pre-dispatch construction errors release;
            # everything else may have happened AFTER the upload started.
            if name in PRE_DISPATCH_ERROR_NAMES:
                out["error_kind"] = f"PRE_DISPATCH_{name.upper()}"
                out["may_have_billed"] = False
                out["stream_status"] = "NOT_STARTED"
            else:
                is_timeout = "Timeout" in name or "timeout" in str(e).lower()
                out["error_kind"] = "TIMEOUT" if is_timeout \
                    else f"CONNECTION_LOST_UNKNOWN_STAGE:{name}"
                out["may_have_billed"] = True   # uploaded-then-dropped is possible
                out["stream_status"] = "UNKNOWN"
            out["ended_utc"] = utc_now_iso()
            return out
        try:
            out["http_status"] = resp.status_code
            out["safe_headers"] = _safe_headers(getattr(resp, "headers", {}) or {})
            status = resp.status_code
            if status in (401, 403):
                out["error_kind"] = "AUTH"
                self._capture_error_body(resp, out)
                out["stream_status"] = "NOT_STARTED"
                out["ended_utc"] = utc_now_iso()
                return out
            if status == 429:
                out["error_kind"] = "RATE_LIMIT"
                self._capture_error_body(resp, out)
                out["stream_status"] = "NOT_STARTED"
                out["ended_utc"] = utc_now_iso()
                return out
            if status >= 500:
                out["error_kind"] = "SERVER_5XX"
                out["may_have_billed"] = True
                self._capture_error_body(resp, out)
                out["stream_status"] = "NOT_STARTED"
                out["ended_utc"] = utc_now_iso()
                return out
            if status != 200:
                out["error_kind"] = f"HTTP_{status}"
                self._capture_error_body(resp, out)
                out["stream_status"] = "NOT_STARTED"
                out["ended_utc"] = utc_now_iso()
                return out
            # --- HTTP 200: real wire parsing ---
            if self.stream:
                raw, read_error = self._read_stream_bytes(resp)
                out["raw_response_bytes"] = raw
                out["raw_response_sha256"] = sha256_bytes(raw)
                out["read_error"] = read_error
                try:
                    content = parse_sse_bytes(raw, state)
                except Exception as e:
                    out["error_kind"] = f"SSE_PARSE_EXCEPTION:{type(e).__name__}"
                    out["stream_status"] = "PARSE_ERROR"
                    out["may_have_billed"] = True
                    self._finalize_ids(out, state)
                    out["ended_utc"] = utc_now_iso()
                    return out
                if read_error:
                    out["stream_status"] = "INTERRUPTED"
                    out["error_kind"] = "READ_ERROR"
                    out["may_have_billed"] = True
                elif state["chunk_parse_errors"]:
                    out["stream_status"] = "PARSE_ERROR"
                    out["error_kind"] = "CHUNK_PARSE_ERRORS"
                    out["may_have_billed"] = True
                elif state["terminal_seen"]:
                    out["stream_status"] = "COMPLETE"
                else:
                    out["stream_status"] = "INTERRUPTED"
                    out["error_kind"] = "NO_TERMINAL_MARKER"
                    out["may_have_billed"] = True
                out["content_text"] = content if content else None
                if not content and out["error_kind"] is None:
                    out["error_kind"] = "NO_CONTENT_BLOCK"
            else:
                raw = self._read_body(resp)
                out["raw_response_bytes"] = raw
                out["raw_response_sha256"] = sha256_bytes(raw)
                try:
                    content = parse_non_stream_bytes(raw, state)
                except ValueError:
                    out["error_kind"] = "INVALID_JSON"
                    out["stream_status"] = "PARSE_ERROR"
                    out["may_have_billed"] = True
                    self._finalize_ids(out, state)
                    out["ended_utc"] = utc_now_iso()
                    return out
                out["stream_status"] = "COMPLETE" if state["terminal_seen"] else "UNKNOWN"
                out["content_text"] = content if content else None
                if not content and out["error_kind"] is None:
                    out["error_kind"] = "NO_CONTENT_BLOCK"
            self._finalize_ids(out, state)
            out["ended_utc"] = utc_now_iso()
            return out
        finally:
            close = getattr(resp, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass

    def _finalize_ids(self, out, state):
        out["provider_request_id"] = state.get("provider_request_id") \
            or out["safe_headers"].get("x-request-id")
        out["model_returned"] = state.get("model_returned")
        # P2-02: never backfill from the requested model
        out["model_identity"] = ("PROVIDED" if state.get("model_returned")
                                 else "NOT_PROVIDED_BY_PROVIDER")
        out["usage"] = state.get("usage_raw")
        out["finish_reason"] = state.get("finish_reason_raw")
        out["chunk_parse_errors"] = state["chunk_parse_errors"]
        out["reasoning_text_sha256"] = (
            sha256_bytes("".join(state["reasoning_parts"]).encode("utf-8"))
            if state["reasoning_parts"] else None)
        if out["raw_response_bytes"] is not None and out["raw_response_sha256"] is None:
            out["raw_response_sha256"] = sha256_bytes(out["raw_response_bytes"])

    def _capture_error_body(self, resp, out):
        """Error bodies are length-capped; truncation is explicitly flagged
        with the full length (P2-01: no silent truncation masquerading as
        complete wire)."""
        body = self._read_body(resp)
        out["raw_full_length"] = len(body)
        if len(body) > MAX_ERROR_BODY_BYTES:
            body = body[:MAX_ERROR_BODY_BYTES]
            out["raw_truncated"] = True
        out["raw_response_bytes"] = body
        out["raw_response_sha256"] = sha256_bytes(body)

    def _read_body(self, resp) -> bytes:
        data = getattr(resp, "content", None)
        if isinstance(data, bytes):
            return data
        text = getattr(resp, "text", "") or ""
        return text.encode("utf-8", "replace")

    def _read_stream_bytes(self, resp):
        """Accumulate EXACT arrived bytes via iter_content (P2-01). Read
        errors are returned for meta only — never injected into the raw."""
        chunks = []
        read_error = None
        it = getattr(resp, "iter_content", None)
        if callable(it):
            try:
                for chunk in it(8192):
                    if isinstance(chunk, bytes):
                        chunks.append(chunk)
                    else:
                        chunks.append(str(chunk).encode("utf-8"))
            except Exception as e:
                read_error = f"{type(e).__name__}: {e}"
        else:
            chunks.append(self._read_body(resp))
        return b"".join(chunks), read_error


# --------------------------------------------------------------------------
# Offline fake-HTTP doubles (drive the REAL send/parse path)

class FakeResponse:
    def __init__(self, status_code=200, content=b"", chunks=None, headers=None,
                 iter_content_error=None):
        self.status_code = status_code
        self.content = content
        self._chunks = chunks
        self.headers = headers or {"content-type": "text/event-stream",
                                   "x-request-id": "FAKE-REQ-ID"}
        self.text = content.decode("utf-8", "replace")
        self._iter_content_error = iter_content_error
        self.closed = False

    def iter_content(self, chunk_size=8192):
        if self._iter_content_error:
            n = 0
            for ch in (self._chunks if self._chunks is not None else [self.content]):
                if self._iter_content_error[0] == n:
                    raise self._iter_content_error[1]
                yield ch
                n += 1
            return
        if self._chunks is not None:
            for ch in self._chunks:
                yield ch
        else:
            for i in range(0, max(len(self.content), 1), chunk_size):
                piece = self.content[i:i + chunk_size]
                if piece:
                    yield piece

    def iter_lines(self):  # legacy shim (transport no longer uses it)
        for line in self.content.splitlines():
            yield line

    def close(self):
        self.closed = True


class FakeSession:
    """Injectable session double: records posted bodies, replays scripted
    responses. NEVER touches the network."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.posted = []

    def post(self, url, data=None, timeout=None, stream=None, **kw):
        self.posted.append({"url": url, "body_bytes": data,
                            "body_sha256": sha256_bytes(data or b""),
                            "timeout": timeout, "stream": stream})
        if not self.responses:
            raise AssertionError("FakeSession exhausted")
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def sse_bytes(frames: list, done: bool = True, crlf: bool = False) -> bytes:
    """Build a real-format SSE wire payload; crlf=True emits CRLF line
    endings to test byte-exact preservation."""
    nl = b"\r\n" if crlf else b"\n"
    out = []
    for f in frames:
        out.append(b"data: " + json.dumps(f, ensure_ascii=False).encode("utf-8") + nl + nl)
    if done:
        out.append(b"data: [DONE]" + nl + nl)
    return b"".join(out)


def _split_contiguous(s: str, n: int) -> list:
    if n <= 1:
        return [s]
    size = max(1, -(-len(s) // n))
    return [s[i:i + size] for i in range(0, len(s), size)]


def stream_frames(content: str, usage=None, model="deepseek-v4-pro-0813",
                  rid="fake-rid-1", finish="stop", n_content=1,
                  reasoning=None):
    frames = []
    if reasoning:
        frames.append({"id": rid, "model": model,
                       "choices": [{"delta": {"reasoning_content": reasoning}}]})
    pieces = _split_contiguous(content, n_content)
    for i, p in enumerate(pieces):
        last = (i == len(pieces) - 1)
        frames.append({"id": rid, "model": model,
                       "choices": [{"delta": {"content": p},
                                    "finish_reason": finish if last else None}]})
    if usage is not None:
        frames.append({"id": rid, "model": model, "usage": usage, "choices": []})
    return frames
