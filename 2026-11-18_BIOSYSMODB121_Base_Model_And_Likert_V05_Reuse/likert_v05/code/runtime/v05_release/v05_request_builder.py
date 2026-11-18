"""V0.5 request builder over the reviewed config gate.

Same gate semantics as the audited f2r12_request_builder (PENDING fields block;
live requires USER_CONFIRMED_FROZEN + user confirmation binding the config sha);
only the body assembly changes: messages come from the pre-rendered release
artifact, never from V0.4 template re-rendering.
"""
import json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "f2"))
from common_03a import OUT, SCHEMA_PATH, VERSION, sha
import f2r12_request_builder as RB

_approx_token_count = RB._approx_token_count
ConfigNotConfirmed = RB.ConfigNotConfirmed
RequestBuildError = RB.RequestBuildError
PENDING_RE = RB.PENDING_RE


def load_config(path=None, bind_sha=True):
    path = path or (OUT.parent / "config/RUN_CONFIG_LIVE.json")
    cfg = json.loads(Path(path).read_text())
    if bind_sha:
        cfg["_config_sha256"] = sha(Path(path).read_bytes())
    return cfg


def config_gate(cfg, confirmation, require_confirmed):
    return RB.config_gate(cfg, confirmation, require_confirmed)


def model_config_canonical_sha(cfg):
    return RB.model_config_canonical_sha(cfg)


def build_request_body(item_payload, cfg, confirmation=None, require_confirmed=True):
    reasons = config_gate(cfg, confirmation, require_confirmed)
    if require_confirmed and reasons:
        raise RB.ConfigNotConfirmed("; ".join(reasons))
    ai = cfg["scoring_ai"]["recommended"]
    mp = cfg["model_parameters"]

    def pval(name):
        v = mp.get(name)
        return v.get("value") if isinstance(v, dict) else v

    model_id = ai.get("exact_model_id")
    endpoint = ai.get("endpoint")
    import re
    if not model_id or re.search(RB.PENDING_RE, str(model_id)):
        raise RB.RequestBuildError("exact_model_id not confirmed: %r" % (model_id,))
    if not endpoint or not str(endpoint).startswith("https://"):
        raise RB.RequestBuildError("endpoint must be HTTPS and confirmed")
    ctx = item_payload["ctx"]
    messages = item_payload["artifact"]["messages"]
    body = {"model": model_id, "messages": messages, "stream": bool(pval("stream"))}
    for key in ("temperature", "max_tokens", "response_format", "enable_thinking", "stream_options"):
        val = pval(key)
        if val == "OMIT" or val is None:
            continue
        body[key] = val
    rt = pval("reasoning_effort")
    if rt not in (None, "OMIT"):
        body["reasoning_effort"] = rt
    es = pval("enable_search")
    if es is False:
        body["enable_search"] = False
    bound = pval("max_input_tokens_bound") or 200000
    approx = RB._approx_token_count(messages)
    if approx > bound:
        raise RB.RequestBuildError("item %s: approx input tokens %d > bound %d" %
                                   (ctx["anonymous_item_id"], approx, bound))
    return {"endpoint": endpoint, "body": body, "approx_input_tokens": approx,
            "model_config_canonical_sha256": model_config_canonical_sha(cfg),
            "config_sha256": cfg.get("_config_sha256"),
            "item_identity": {"b_slot_uid": ctx["b_slot_uid"],
                              "anonymous_item_id": ctx["anonymous_item_id"],
                              "case_id": ctx["case_id"],
                              "user_message_sha256": ctx["user_message_sha256"],
                              "identity_echo": ctx["identity_echo"],
                              "release_id": VERSION}}


def cache_key(item_payload, cfg):
    ctx = item_payload["ctx"]
    ie = ctx["identity_echo"]
    components = {"release_id": VERSION, "b_slot_uid": ctx["b_slot_uid"],
                  "answer_sha256": ie["answer_sha256"],
                  "question_rendered_prompt_sha256": ie["question_rendered_prompt_sha256"],
                  "user_message_sha256": ctx["user_message_sha256"]}
    for k, v in sorted(ie.items()):
        components[k] = v
    components["rating_schema_sha256"] = sha(SCHEMA_PATH.read_bytes())
    components["model_config_canonical_sha256"] = model_config_canonical_sha(cfg)
    components["run_config_version_sha256"] = cfg.get("_config_sha256")
    import hashlib
    return hashlib.sha256(json.dumps(components, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
