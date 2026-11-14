#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v05_rating_pipeline_r3.py -- R3-B：唯一组合评分返回入口。

= 旧受审计语义链（f2r12_response_validator.validate_rating，导入后仅以模块属性覆盖
  SCHEMA_ID为V0.5候选ID——不改旧文件）+ V0.5新增门（R2 validator）+ R3新门：
  * 矩阵与ctx事实**双向全字段**同源（structure/credit_class/five_state/conclusion；
    YES仅当事实CONFIRMED；事实CONFIRMED而输出降级也拒——不允许两侧互相矛盾）；
  * 引用白名单来自本请求实际提供对象（E0/gold slice/scope rows/ACCSET:<gold_step_id>），
    废止"GOLD:"前缀无条件放行；
  * 泄漏扫描按ctx.coordination_block_texts分区（协调端装配块）执行；规范正文与冻结数据
    文本不再触发G0误拒（复审B3修复）；同时真实请求整体作为回归正例通过；
  * 政策字段（policy/allowed_ranges/eligibility/reference_hold/step_facts/scope_rows/
  identity_echo/whitelists）缺失=fail-closed REJECTED；
  * 合法REVIEW_REQUESTED/边界/HELD→REVIEW_PENDING（不计正式）；legacy corrections→CORRECTED。
"""

import importlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import v05_paths as _vp
R = _vp.RUN_ROOT
F2CODE = _vp.F2
sys.path.insert(0, F2CODE)

import f2r12_response_validator as LEG  # noqa: E402  旧入口只读复用
import v05_response_validator as V5  # noqa: E402  R2 validator（V0.5门）

V05_SCHEMA_ID = "LIKERT_V05_AI_RATING_OUTPUT_SCHEMA_CANDIDATE_R3"
LEG.SCHEMA_ID = V05_SCHEMA_ID  # 模块属性适配（不改旧文件本体）

COORD_LEAK_PATTERNS = [
    re.compile(r"v04[_ ]?(D[1-6]|score|total)", re.IGNORECASE),
    re.compile(r"(weighted_total|scientific_subscore)[^,}]*?(=|:)\s*[0-9]"),
    re.compile(r"(ZHIPU_GLM53|GLM-5\.3|kimi/kimi|qwen3\.8|deepseek-v4)", re.IGNORECASE),
    re.compile(r"R21_ORIGINAL_ACCEPTED|TARGETED5_TECHNICAL"),
    re.compile(r"PRIOR_AI_RATING_CLUE|key_error=Y(?!须|要求)"),
]

REQUIRED_CTX = {
    # key → 是否允许空值（EVIDENCE_GAP案的evidence_ids合法为空；其余必填非空）
    "schema": False, "identity_echo": False, "step_facts": False,
    "allowed_ranges": False, "scope_rows": False, "required_gold_step_ids": False,
    "evidence_ids": True, "gold_ref_ids": True, "scope_row_ref_ids": True,
    "coordination_block_texts": False, "policy": False, "eligibility": False,
}


def _err(code, msg):
    return {"gate": code, "message": msg}


def process_rating(rating, ctx):
    errors, corrections = [], []
    for k, allow_empty in REQUIRED_CTX.items():
        v = ctx.get(k)
        missing = v is None or (not allow_empty and v in ("", {}, []))
        if k not in ctx or missing:
            return {"status": "REJECTED",
                    "errors": [_err("V05-P0", "缺少必需ctx字段:%s" % k)],
                    "corrections": [], "review_flags": [],
                    "projection": {"counts_as_formal": False}}
    review_flags = []

    # ---------- 1. 旧受审计语义链（完整调用） ----------
    legacy_ctx = {
        "case_id": ctx.get("case_id"), "anonymous_item_id": ctx.get("anonymous_item_id"),
        "identity_echo": ctx["identity_echo"], "scope_rows": ctx["scope_rows"],
        "evidence_ids": ctx["evidence_ids"], "gold_ref_ids": ctx["gold_ref_ids"],
        "scope_row_ref_ids": ctx["scope_row_ref_ids"],
        "predef_by_id": ctx.get("predef_by_id", {}),
    }
    lres = LEG.validate_rating(rating, legacy_ctx, ctx["schema"])
    for e in lres.errors:
        errors.append({"gate": "LEGACY:" + e.get("code", "V??"),
                       "message": str(e.get("message", ""))[:200]})
    corrections += [{"field": c.get("field"), "reported": c.get("model_value"),
                     "program_value": c.get("recomputed_value"), "action": "PROGRAM_RECOMPUTED"}
                    for c in lres.corrections]
    for r_ in getattr(lres, "review_flags", []) or []:
        review_flags.append({"gate": "LEGACY:" + str(r_.get("code") if isinstance(r_, dict) else r_),
                             "message": str(r_)[:160]})

    # ---------- 2. V0.5门（R2 validator；ctx_to_inputs复用其route/credit/矩阵输入侧检查） ----------
    ok5, errs5, rev5 = V5.validate_rating(rating, {
        "route_status": ctx.get("route_status", "CONFORMS"),
        "task_conformance_status": ctx.get("task_conformance_status", "OK"),
        "required_gold_step_ids": ctx["required_gold_step_ids"],
        "allowed_ranges": ctx["allowed_ranges"],
        "held": bool(ctx.get("reference_hold")),
        "held_reason": ctx.get("reference_hold_reason", ""),
        "frozen_record_contradiction": bool(ctx.get("frozen_record_contradiction")),
        "policy": ctx.get("policy", "A"),
        "eligibility": ctx["eligibility"],
        "input_shas": {}, "prior_rating_material_present": False,
        "d2_deviation_cap": ctx.get("d2_deviation_cap", 4),
        "d2_nine_ten_evidence_ok": bool(ctx.get("d2_nine_ten_evidence_ok")),
        "c_confirmed": ctx.get("c_confirmed", 0.0)})
    for e in errs5:
        if e["gate"] == "V05-G0":
            continue  # G0改由分区扫描（见4），避免以手填开关代实扫
        errors.append(e)
    review_flags += rev5

    # ---------- 3. 矩阵↔事实双向全字段 + 白名单 ----------
    whitelist = set(ctx["evidence_ids"]) | set(ctx["gold_ref_ids"]) | \
        set(ctx["scope_row_ref_ids"]) | {"ACCSET:" + g for g in ctx["required_gold_step_ids"]}
    matrix = rating.get("step_evidence_matrix") or []
    facts = ctx["step_facts"]
    seen = []
    for r_ in matrix:
        gid = r_.get("gold_step_id")
        seen.append(gid)
        f = facts.get(gid)
        if f is None:
            errors.append(_err("V05-G2", "矩阵引用ctx外目标步:%s" % gid))
            continue
        for field, factkey in (("structure_match_and_direction", "route_state"),
                               ("credit_class", "credit_class"),
                               ("evidence_five_state", "five_state"),
                               ("step_conclusion_7class", "conclusion")):
            got = r_.get(field)
            if got is not None and got != f[factkey]:
                errors.append(_err("V05-G2", "%s.%s=%r与事实%r不一致(双向同源)" %
                                   (gid, field, got, f[factkey])))
        if r_.get("target_credit_usable") == "YES" and f["credit_class"] != "CONFIRMED_TARGET":
            errors.append(_err("V05-G7", "%s 事实=%s不得成功用信用" % (gid, f["credit_class"])))
        if f["credit_class"] == "CONFIRMED_TARGET" and r_.get("target_credit_usable") != "YES" \
                and r_.get("structure_match_and_direction") == "MATCH":
            errors.append(_err("V05-G7", "%s 事实CONFIRMED但输出擅自取消信用(双向)" % gid))
        ev = r_.get("evidence_entry_and_version")
        if ev and ev not in whitelist:
            errors.append(_err("V05-G2", "%s 引用不在本请求对象白名单:%s" % (gid, str(ev)[:50])))
    if sorted(seen) != sorted(set(seen)):
        errors.append(_err("V05-G2", "矩阵存在重复gold_step_id"))
    if set(seen) != set(ctx["required_gold_step_ids"]):
        errors.append(_err("V05-G2", "矩阵ID集合≠必答集合"))

    # ---------- 4. 按来源分区泄漏扫描（真实装配块内容） ----------
    for bname, btext in (ctx.get("coordination_block_texts") or {}).items():
        for pat in COORD_LEAK_PATTERNS:
            mm = pat.search(btext or "")
            if mm:
                errors.append(_err("V05-G0", "协调装配块%s含禁用内容:%r" % (bname, mm.group(0)[:40])))

    # ---------- 5. 状态投影 ----------
    rc_ = rating.get("base_range_compliance") or {}
    if errors:
        status = "REJECTED"
    elif ctx.get("reference_hold") or ctx.get("route_status") == "BOUNDARY_REVIEW" or \
            rc_.get("within_range_or_review") == "REVIEW_REQUESTED_OUT_OF_RANGE" or review_flags:
        status = "REVIEW_PENDING"
    elif corrections:
        status = "CORRECTED"
    else:
        status = "ACCEPTED"
    dims = rating.get("dimensions") or {}
    prog = {"legacy_valid": bool(lres.valid),
            "program_values": {c["field"]: c["program_value"] for c in corrections},
            "counts_as_formal": status in ("ACCEPTED", "CORRECTED"),
            "dims_scored": sorted(d for d, v in dims.items()
                                  if isinstance(v, dict) and v.get("score_status") == "SCORED")}
    return {"status": status, "errors": errors, "corrections": corrections,
            "review_flags": review_flags, "projection": prog}


if __name__ == "__main__":
    print("pipeline module; use process_rating(rating, ctx)")
