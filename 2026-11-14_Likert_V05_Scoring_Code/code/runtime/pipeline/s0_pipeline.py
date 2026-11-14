#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
s0_pipeline.py -- 01卡B：组合入口加硬版。复用R3组合链（旧validator全门+双向同源+分区泄漏），
本层只补"ctx关键运行字段不得缺省"：route_status/task_conformance_status必须存在且属枚举、
identity_echo恰14项且与请求对象一致、reference_hold必带reason——缺任何一项=REJECTED
（不得默认CONFORMS）。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
import v05_paths as _vp
R = _vp.RUN_ROOT
sys.path.insert(0, str(_vp.PIPELINE))
sys.path.insert(0, HERE)
import v05_rating_pipeline_r3 as PR3  # noqa: E402

ROUTE_ENUM = {"CONFORMS", "DEVIATES", "INCOMPLETE", "BOUNDARY_REVIEW", "REFERENCE_HOLD"}
TASK_ENUM = {"OK", "VIOLATED"}
ECHO14 = set(PR3.REQUIRED_CTX)  # placeholder replaced below
IDENTITY_KEYS = {
    "input_manifest_sha", "question_rendered_prompt_sha256", "answer_sha256",
    "rubric_text_sha256", "gold_slice_manifest_sha256", "scope_rows_sha256",
    "evidence_snapshot_sha", "system_prompt_sha256", "item_template_sha256",
    "evidence_case_slice_sha256", "task_scope_sha256", "route_diagnosis_sha256",
    "accepted_sets_sha256", "base_ranges_sha256"}


def process_rating(rating, ctx):
    # 加硬的输入合同：缺关键运行字段=fail-closed，绝不默认
    if ctx.get("route_status") not in ROUTE_ENUM:
        return {"status": "REJECTED",
                "errors": [{"gate": "S0-CTX-HARD",
                            "message": "ctx.route_status缺失/非法（不得默认CONFORMS）：%r"
                                       % ctx.get("route_status")}],
                "corrections": [], "review_flags": [],
                "projection": {"counts_as_formal": False}}
    if ctx.get("task_conformance_status") not in TASK_ENUM:
        return {"status": "REJECTED",
                "errors": [{"gate": "S0-CTX-HARD",
                            "message": "ctx.task_conformance_status缺失/非法：%r"
                                       % ctx.get("task_conformance_status")}],
                "corrections": [], "review_flags": [],
                "projection": {"counts_as_formal": False}}
    ie = ctx.get("identity_echo")
    if not isinstance(ie, dict) or set(ie) != IDENTITY_KEYS:
        return {"status": "REJECTED",
                "errors": [{"gate": "S0-CTX-HARD",
                            "message": "identity_echo必须恰为14项（少/多/占位均拒）"}],
                "corrections": [], "review_flags": [],
                "projection": {"counts_as_formal": False}}
    for k, v in ie.items():
        if not isinstance(v, str) or len(v) != 64 or v in ("0" * 64, "1" * 64):
            return {"status": "REJECTED",
                    "errors": [{"gate": "S0-CTX-HARD",
                                "message": "身份字段非法(长度/占位0/1)：%s" % k}],
                    "corrections": [], "review_flags": [],
                    "projection": {"counts_as_formal": False}}
    if ctx.get("reference_hold") and not ctx.get("reference_hold_reason"):
        return {"status": "REJECTED",
                "errors": [{"gate": "S0-CTX-HARD", "message": "reference_hold必须带reason"}],
                "corrections": [], "review_flags": [],
                "projection": {"counts_as_formal": False}}
    return PR3.process_rating(rating, ctx)
