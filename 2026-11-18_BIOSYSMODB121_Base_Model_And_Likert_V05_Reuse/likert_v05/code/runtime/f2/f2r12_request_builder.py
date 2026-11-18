"""F2 request builder: assemble the provider request body for one item and
enforce the configuration gate.

Gate (contract §7.2 / F2 card stop position): a live request body is only
built when SCORING_RUN_CONFIG.json carries config_status=USER_CONFIRMED_FROZEN,
a matching user confirmation record binds its sha256, and NO required field
still contains a PENDING_* placeholder or null. Otherwise the builder raises
ConfigNotConfirmed — this is the "无配置即调用" counterexample rejection
(test T12), and it is why F2 itself can never emit a live call.

Offline: no network, no model API.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (F2_DIR, read_json, sha256_file, sha256_bytes,
                       canonical_json, sha256_canonical)

PENDING_RE = re.compile(r"PENDING_|待确认|待绑定", re.IGNORECASE)


class ConfigNotConfirmed(RuntimeError):
    pass


class RequestBuildError(RuntimeError):
    pass


def _scan_pending(obj, path="$"):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            hits += _scan_pending(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += _scan_pending(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if PENDING_RE.search(obj):
            hits.append((path, obj))
    return hits


def config_gate(cfg: dict, confirmation: dict | None, require_confirmed: bool):
    """Enforce the confirmation gate. Returns list of blocking reasons
    (empty = gate open)."""
    reasons = []
    status = cfg.get("config_status")
    if require_confirmed:
        if status != "USER_CONFIRMED_FROZEN":
            reasons.append(f"config_status={status!r} != USER_CONFIRMED_FROZEN")
        if not confirmation:
            reasons.append("user confirmation record missing (F4_USER_CONFIG_CONFIRMATION.json)")
        else:
            if confirmation.get("confirmed_config_sha256") != cfg.get("_config_sha256"):
                reasons.append("confirmation does not bind this config sha256")
            if confirmation.get("confirmed_by") != "USER":
                reasons.append("confirmation not by USER (executor/Astra/model cannot self-confirm)")
            if confirmation.get("live_paid_calls_authorized") is not True:
                reasons.append("live_paid_calls_authorized != true in confirmation record")
    # Required-field pending scan (always, regardless of mode)
    required_groups = ["scoring_ai.recommended", "model_parameters", "cost",
                       "scheduling", "run_boundaries"]
    flat = _flatten(cfg)
    for path, val in flat.items():
        if not any(path.startswith("$." + g) for g in required_groups):
            continue
        if isinstance(val, str) and PENDING_RE.search(val):
            # alternative-option fields and disclosure notes may legitimately
            # contain PENDING markers; only *value-bearing* fields block:
            if _is_value_field(path):
                reasons.append(f"required field still pending: {path}={val[:80]!r}")
    return reasons


VALUE_FIELD_KEYS = {"status", "value", "hard_cap_total_cny", "endpoint",
                    "exact_model_id", "provider", "api_key_env_var_name",
                    "per_call_worst_case_reservation_busy", "expected_mean_total_480",
                    "worst_case_total_incl_retries_960", "smoke_sub_budget_cny",
                    "price_status", "evidence_snapshot_sha256"}


def _is_value_field(path: str) -> bool:
    leaf = path.rsplit(".", 1)[-1]
    leaf = re.sub(r"\[\d+\]$", "", leaf)
    if leaf in VALUE_FIELD_KEYS:
        return True
    return False


def _flatten(obj, path="$"):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(_flatten(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(_flatten(v, f"{path}[{i}]"))
    else:
        out[path] = obj
    return out


def model_config_canonical_sha(cfg: dict) -> str:
    """Canonical identity of the model-parameter block (cache key component;
    any parameter change = new identity = no cross-version cache hit)."""
    mp = cfg.get("model_parameters") or {}
    frozen = {k: (v.get("value") if isinstance(v, dict) else v) for k, v in mp.items()}
    frozen["_model_id"] = (cfg.get("scoring_ai") or {}).get("recommended", {}).get("exact_model_id")
    frozen["_endpoint"] = (cfg.get("scoring_ai") or {}).get("recommended", {}).get("endpoint")
    return sha256_canonical(frozen)


def build_request_body(item_payload: dict, cfg: dict, confirmation: dict | None = None,
                       require_confirmed: bool = True) -> dict:
    """Build the OpenAI-compatible request body for one item.

    Raises ConfigNotConfirmed when the gate is closed (this is the desired
    F2 behaviour: zero live calls possible without user confirmation).
    """
    reasons = config_gate(cfg, confirmation, require_confirmed)
    if require_confirmed and reasons:
        raise ConfigNotConfirmed("; ".join(reasons))

    ai = cfg["scoring_ai"]["recommended"]
    mp = cfg["model_parameters"]

    def pval(name):
        v = mp.get(name)
        return v.get("value") if isinstance(v, dict) else v

    model_id = ai.get("exact_model_id")
    endpoint = ai.get("endpoint")
    if not model_id or PENDING_RE.search(str(model_id)):
        raise RequestBuildError(f"exact_model_id not confirmed: {model_id!r}")
    if not endpoint or not str(endpoint).startswith("https://"):
        raise RequestBuildError(f"endpoint must be HTTPS and confirmed: {endpoint!r}")

    messages = [
        {"role": "system", "content": _read(item_payload["system_prompt_path"])},
        {"role": "user", "content": item_payload["user_message"]},
    ]
    body = {"model": model_id, "messages": messages, "stream": bool(pval("stream"))}
    for key, param in [("temperature", "temperature"), ("max_tokens", "max_tokens"),
                       ("response_format", "response_format"),
                       ("enable_thinking", "enable_thinking"),
                       ("stream_options", "stream_options")]:
        val = pval(param)
        if val == "OMIT" or val is None:
            continue  # explicit OMIT per contract §7.2
        body[key] = val
    rt = pval("reasoning_effort")
    if rt not in (None, "OMIT"):
        body["reasoning_effort"] = rt
    # enable_search: never defaulted true; only sent when explicitly False-supported
    es = pval("enable_search")
    if es is False:
        body["enable_search"] = False

    # input size guard: refuse oversize instead of silent truncation
    bound = pval("max_input_tokens_bound") or 200000
    approx_tokens = _approx_token_count(messages)
    if approx_tokens > bound:
        raise RequestBuildError(
            f"item {item_payload['anonymous_item_id']}: approx input tokens {approx_tokens} > "
            f"bound {bound}; refusing (no silent truncation / summarization of frozen Q&A)")

    return {
        "endpoint": endpoint,
        "body": body,
        "approx_input_tokens": approx_tokens,
        "model_config_canonical_sha256": model_config_canonical_sha(cfg),
        "config_sha256": cfg.get("_config_sha256"),
        "item_identity": {
            "b_slot_uid": item_payload["b_slot_uid"],
            "anonymous_item_id": item_payload["anonymous_item_id"],
            "case_id": item_payload["case_id"],
            "user_message_sha256": item_payload["user_message_sha256"],
            "identity_echo": item_payload["identity_echo"],
        },
    }


def _read(path) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def _approx_token_count(messages) -> int:
    """Conservative offline estimate: CJK chars ≈ 1 token each, other bytes
    ≈ 1 token per 3 bytes; used only for the oversize guard and budget
    reservation. Actual usage comes from the provider response."""
    total = 0
    for m in messages:
        s = m["content"]
        cjk = sum(1 for ch in s if "\u4e00" <= ch <= "\u9fff" or "\u3000" <= ch <= "\u303f")
        other_bytes = len(s.encode("utf-8")) - cjk * 3
        total += cjk + max(other_bytes, 0) // 3 + 8
    return total


def cache_key(item_payload: dict, cfg: dict) -> str:
    """Cache key per contract §7.4: logical slot + frozen inputs + prompt +
    model config + schema + run-config version. Any component change → miss."""
    ie = item_payload["identity_echo"]
    components = {
        "b_slot_uid": item_payload["b_slot_uid"],
        "answer_sha256": ie["answer_sha256"],
        "question_rendered_prompt_sha256": ie["question_rendered_prompt_sha256"],
        "rubric_text_sha256": ie["rubric_text_sha256"],
        "system_prompt_sha256": ie["system_prompt_sha256"],
        "item_template_sha256": ie["item_template_sha256"],
        "gold_slice_manifest_sha256": ie["gold_slice_manifest_sha256"],
        "scope_rows_sha256": ie["scope_rows_sha256"],
        "evidence_snapshot_sha256": ie["evidence_snapshot_sha"],
        "evidence_case_slice_sha256": ie.get("evidence_case_slice_sha256"),
        "rating_schema_sha256": sha256_file(F2_DIR / "RATING_OUTPUT_SCHEMA.json"),
        "model_config_canonical_sha256": model_config_canonical_sha(cfg),
        "run_config_version_sha256": cfg.get("_config_sha256"),
    }
    return sha256_canonical(components)


def load_config(path=None, bind_sha: bool = True) -> dict:
    path = path or (F2_DIR / "SCORING_RUN_CONFIG.json")
    cfg = read_json(path)
    if bind_sha:
        cfg["_config_sha256"] = sha256_file(path)
    return cfg


if __name__ == "__main__":
    # CLI: demonstrate the gate — building against the R0 draft MUST fail.
    cfg = load_config()
    try:
        build_request_body({"system_prompt_path": str(F2_DIR / "SCORING_SYSTEM_PROMPT.txt"),
                            "user_message": "x", "b_slot_uid": "B480-0001",
                            "anonymous_item_id": "F4I-0001", "case_id": "BIOPATH150_001",
                            "user_message_sha256": "0" * 64,
                            "identity_echo": {}}, cfg)
        print("UNEXPECTED: gate open on draft config")
        raise SystemExit(1)
    except ConfigNotConfirmed as e:
        print(f"gate CLOSED as required on draft config: {str(e)[:400]}")
        raise SystemExit(0)
