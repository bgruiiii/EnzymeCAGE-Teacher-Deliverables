#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r2p_pipeline.py -- 01R2补丁MP-1：在R2门源码基础上只修predef单条目绕过（不重建、不扩展）。

MP-1修正（复审R2 §MP-1，r2_pipeline.py:145–148）：
 * predef_by_id条目非dict（null/[]/字符串）不再静默continue：明确REJECTED、不抛异常；
 * 其余逻辑与R2门完全一致（冻结20组绑定/类型先于枚举/R3 schema枚举/S0加硬层+R3完整链）。

原R2修正（复审R1 §3）保持：
 1) predef_by_id绑定旧F2冻结表：load_predef_attrs()自带SHA校验；
    空表/缺组/多组/篡改CORE属性一律REJECTED——CG01等无条件组不再可绕过；
 2) 所有值检查先类型后枚举：allowed_ranges非字符串、step_facts字段非字符串
    （如five_state={}）明确REJECTED，不再以TypeError崩溃；
 3) route_state/credit_class/five_state/conclusion枚举改读R3候选schema
    step_evidence_matrix.items.properties（CONTRADICTED/CREDIT_CONTRADICTED等
    量表合法值不再因当前底表未出现而被误拒）；结构层接受≠真实矛盾确认；
 4) 其余同R1：缺字段≠默认值；HELD哨兵仅边界/隔离槽；底层仍S0加硬层+R3完整链。
"""
import csv
import json
import os
import re
import sys

import v05_paths as _vp
R = _vp.RUN_ROOT
S0 = os.path.join(R, "LIKERT_V05_RELEASE_20261108", "S0_INTEGRATION")
R3 = os.path.join(R, "LIKERT_V05_REVISION_20261105_R3")
V4 = os.path.join(R, "LIKERT_V04_FULL_SCORING_20261029")
sys.path.insert(0, str(_vp.PIPELINE))
sys.path.insert(0, _vp.F2)
import s0_pipeline as S0P  # noqa: E402
import f2r12_item_builder as LEG  # noqa: E402

csv.field_size_limit(1 << 27)
DIMS = ["D1", "D2", "D3a", "D3b", "D4", "D5", "D6"]
RANGE_RE = re.compile(r"^\[(\d{1,2}),(\d{1,2})\]$")
POLICY_ENUM = {"A", "B"}
HELD_SENTINEL = "HELD_PENDING_REPRESENTATION_REVIEW"

# 冻结预定义表（旧入口自带SHA校验；不手写影子词表）
PREDEF_FROZEN = LEG.load_predef_attrs()
PREDEF_SOURCE = {"path": str(LEG.CG_PREDEF_PATH), "content_sha256": str(LEG.CG_PREDEF_SHA)}

# 枚举来自R3候选schema（单一来源）
_schema = json.load(open(os.path.join(
    R3, "P3_RULES_TOOLS", "schema_prompt",
    "RATING_OUTPUT_SCHEMA_V05_CANDIDATE_R3.json"), encoding="utf-8"))
_mat = _schema["properties"]["step_evidence_matrix"]["items"]["properties"]
ENUM = {
    "route_state": set(_mat["structure_match_and_direction"]["enum"]),
    "credit_class": set(_mat["credit_class"]["enum"]),
    "five_state": set(_mat["evidence_five_state"]["enum"]),
    "conclusion": set(_mat["step_conclusion_7class"]["enum"]),
}
ENUM_SOURCE = os.path.relpath(os.path.join(
    R3, "P3_RULES_TOOLS", "schema_prompt",
    "RATING_OUTPUT_SCHEMA_V05_CANDIDATE_R3.json"), R)


def _isstr(v):
    return isinstance(v, str)


def contract_errors(ctx):
    errs = []

    def bad(field, msg):
        errs.append({"gate": "R2-CTX-STRUCT", "field": field, "message": msg})

    if not isinstance(ctx, dict):
        return [{"gate": "R2-CTX-STRUCT", "field": "*", "message": "ctx非dict"}]
    # 身份
    if not (_isstr(ctx.get("case_id")) and
            re.match(r"^BIOPATH150_\d{3}$", ctx.get("case_id") or "")):
        bad("case_id", "缺失/非法case标识")
    if not (_isstr(ctx.get("anonymous_item_id")) and ctx.get("anonymous_item_id")):
        bad("anonymous_item_id", "缺失/空")
    if "schema" not in ctx or not isinstance(ctx["schema"], dict):
        bad("schema", "缺失或非对象")
    for k in ("route_status", "task_conformance_status"):
        if k not in ctx:
            bad(k, "字段缺失（不得默认）")
        elif not _isstr(ctx[k]):
            bad(k, "须为字符串")
    # 政策与资格
    if ctx.get("policy") not in POLICY_ENUM:
        bad("policy", "非法/缺失政策枚举：%r" % (ctx.get("policy"),))
    elig = ctx.get("eligibility")
    if not isinstance(elig, dict):
        bad("eligibility", "缺失/非对象")
    elif ctx.get("policy") in POLICY_ENUM:
        need = "policy_%s" % ctx["policy"]
        if need not in elig:
            bad("eligibility", "缺少所选政策%s的资格键" % need)
        elif not isinstance(elig[need], bool):
            bad("eligibility", "%s须为boolean" % need)
    # allowed_ranges：先类型后正则
    ar = ctx.get("allowed_ranges")
    if not isinstance(ar, dict):
        bad("allowed_ranges", "缺失/非对象")
    else:
        miss = [d for d in DIMS if d not in ar]
        if miss:
            bad("allowed_ranges", "缺必需维度范围：%s" % "|".join(miss))
        held_ok = (ctx.get("route_status") == "BOUNDARY_REVIEW" or
                   ctx.get("reference_hold") is True)
        for d, v in ar.items():
            if not _isstr(v):
                bad("allowed_ranges", "%s范围须为字符串，得到%s" % (d, type(v).__name__))
                continue
            if v == HELD_SENTINEL:
                if not held_ok:
                    bad("allowed_ranges", "%s=HELD哨兵仅BOUNDARY_REVIEW/隔离槽合法" % d)
                continue
            m = RANGE_RE.match(v)
            if not m or not (1 <= int(m.group(1)) <= int(m.group(2)) <= 10):
                bad("allowed_ranges", "%s范围非法:%r" % (d, v))
    # 白名单（EVIDENCE_GAP合法空；缺失≠空）
    for k in ("evidence_ids", "gold_ref_ids", "scope_row_ref_ids"):
        v = ctx.get(k, "MISSING")
        if v == "MISSING":
            bad(k, "字段缺失（合法空=空列表，缺失≠空）")
        elif not isinstance(v, list) or not all(_isstr(x) for x in v):
            bad(k, "须为字符串列表")
    # scope_rows
    sr = ctx.get("scope_rows")
    if not isinstance(sr, list) or not sr:
        bad("scope_rows", "缺失/空列表")
    else:
        for i, row in enumerate(sr):
            if not isinstance(row, dict) or not {"claim_group", "condition_met",
                                                 "active_criticality"} <= set(row):
                bad("scope_rows", "第%d行缺必需键" % i)
            elif not all(_isstr(row.get(k)) and (row.get(k) or "").strip()
                         for k in ("claim_group", "condition_met", "active_criticality")):
                bad("scope_rows", "第%d行必需键须为非空字符串" % i)
    # predef_by_id：绑定冻结表（空表/缺组/篡改一律拒）
    pf = ctx.get("predef_by_id")
    if "predef_by_id" not in ctx or not isinstance(pf, dict):
        bad("predef_by_id", "字段缺失/非对象（不得默认无预定义）")
    else:
        missing_groups = sorted(set(PREDEF_FROZEN) - set(pf))
        extra_groups = sorted(set(pf) - set(PREDEF_FROZEN))
        if missing_groups:
            bad("predef_by_id", "缺冻结表必需组:%s" % "|".join(missing_groups))
        if extra_groups:
            bad("predef_by_id", "含冻结表外影子组:%s" % "|".join(extra_groups))
        for gid, v in pf.items():
            fz = PREDEF_FROZEN.get(gid)
            if fz is None:
                continue  # 影子组已由extra_groups报错
            if not isinstance(v, dict):
                # MP-1：非对象条目（null/[]/字符串等）明确拒绝，不得静默跳过
                bad("predef_by_id",
                    "%s条目须为对象（得到%s）：空值/列表/字符串不能绕过冻结属性比较"
                    % (gid, type(v).__name__))
                continue
            if v.get("name") != fz["name"]:
                bad("predef_by_id", "%s name与冻结表不一致" % gid)
            if v.get("condition_type") != fz["condition_type"]:
                bad("predef_by_id", "%s condition_type与冻结表不一致" % gid)
            if fz["condition_type"] == "UNCONDITIONAL" and \
                    v.get("criticality_unconditional") != fz["criticality_unconditional"]:
                bad("predef_by_id",
                    "%s criticality篡改/缺失（冻结=%r，ctx=%r）"
                    % (gid, fz["criticality_unconditional"],
                       v.get("criticality_unconditional")))
    # 必答步与逐步事实：先类型后枚举
    rg = ctx.get("required_gold_step_ids")
    if not isinstance(rg, list) or not rg:
        bad("required_gold_step_ids", "缺失/空")
    elif not all(_isstr(x) and x.count("__") >= 2 for x in rg):
        bad("required_gold_step_ids", "ID格式非法")
    sf = ctx.get("step_facts")
    if not isinstance(sf, dict) or not sf:
        bad("step_facts", "缺失/空")
    else:
        if isinstance(rg, list):
            for gid in rg:
                if gid not in sf:
                    bad("step_facts", "必答步缺事实行:%s" % gid)
        need = {"route_state", "credit_class", "five_state", "conclusion"}
        for gid, f in sf.items():
            if not isinstance(f, dict):
                bad("step_facts", "%s非对象" % gid)
                continue
            miss = need - set(f)
            if miss:
                bad("step_facts", "%s缺必需字段:%s" % (gid, "|".join(sorted(miss))))
                continue
            for fld in ("route_state", "credit_class", "five_state", "conclusion"):
                if not _isstr(f[fld]):
                    bad("step_facts", "%s.%s须为字符串，得到%s"
                        % (gid, fld, type(f[fld]).__name__))
                elif f[fld] not in ENUM[fld]:
                    bad("step_facts", "%s.%s不在schema枚举:%r" % (gid, fld, f[fld]))
    # 隔离/矛盾/高档/cap/覆盖
    for k, typ in (("reference_hold", bool), ("frozen_record_contradiction", bool),
                   ("d2_nine_ten_evidence_ok", bool)):
        if k not in ctx:
            bad(k, "字段缺失（不得默认False）")
        elif not isinstance(ctx[k], typ):
            bad(k, "须为boolean")
    if ctx.get("reference_hold") is True and not (
            _isstr(ctx.get("reference_hold_reason")) and ctx["reference_hold_reason"].strip()):
        bad("reference_hold_reason", "reference_hold=true必须带非空reason")
    if "reference_hold" in ctx and ctx.get("reference_hold") is False and \
            "reference_hold_reason" not in ctx:
        bad("reference_hold_reason", "字段缺失（false时可空，但键必须在）")
    if "d2_deviation_cap" not in ctx:
        bad("d2_deviation_cap", "字段缺失（不得默认4）")
    elif isinstance(ctx["d2_deviation_cap"], bool) or \
            not isinstance(ctx["d2_deviation_cap"], int) or \
            not 1 <= ctx["d2_deviation_cap"] <= 10:
        bad("d2_deviation_cap", "非法:%r" % (ctx["d2_deviation_cap"],))
    if "c_confirmed" not in ctx:
        bad("c_confirmed", "字段缺失（不得默认0）")
    elif isinstance(ctx["c_confirmed"], bool) or \
            not isinstance(ctx["c_confirmed"], (int, float)) or \
            not 0 <= ctx["c_confirmed"] <= 1:
        bad("c_confirmed", "须为0..1数值")
    cb = ctx.get("coordination_block_texts")
    if not isinstance(cb, dict) or not cb or \
            not all(_isstr(k) and _isstr(v) for k, v in cb.items()):
        bad("coordination_block_texts", "缺失/空/类型非法")
    return errs


def process_rating(rating, ctx):
    errs = contract_errors(ctx)
    if errs:
        return {"status": "REJECTED", "errors": errs, "corrections": [], "review_flags": [],
                "projection": {"counts_as_formal": False, "stage": "R2-CTX-STRUCT"}}
    return S0P.process_rating(rating, ctx)


if __name__ == "__main__":
    print("r2 pipeline module; use process_rating(rating, ctx)")
