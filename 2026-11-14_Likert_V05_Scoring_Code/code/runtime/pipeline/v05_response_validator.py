#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v05_response_validator.py -- V0.5评分返回独立validator（R1候选实现，可运行）。

F10：不再是说明书。硬门应拒即拒（返回errors），软门转人工（review_flags）。
所有门读取与评分输入同源SHA绑定的机器表值（route_status/必答步集合/允许区间/
矛盾绑定/HELD名单），validator与评分者不得各持一套事实。
枚举与VOCABULARY_V05.json一致（构造时校验）。
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB_PATH = os.path.join(HERE, os.pardir, "schema_prompt", "VOCABULARY_V05.json")

_RANGE_RE = re.compile(r"^\[(\d+),(\d+)\]$")

GATE_IDS = ["V05-G1", "V05-G2", "V05-G3", "V05-G4", "V05-G5", "V05-G6", "V05-G7",
            "V05-G8", "V05-S1", "V05-S2", "V05-S3", "V05-S4", "V05-S5", "V05-S6"]


def load_vocabulary(path=None):
    with open(path or VOCAB_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _range_ok(score, allowed):
    if allowed.startswith("NE_HELD") or allowed.startswith("HELD"):
        return None   # HELD槽不应有分（G8处理）
    m = _RANGE_RE.match(allowed)
    if not m:
        return None
    lo, hi = int(m.group(1)), int(m.group(2))
    return lo <= score <= hi


def validate_rating(rating, inputs, vocab=None):
    """rating: 评分返回JSON（V05候选schema实例）。
    inputs: 同源事实包：
      route_status, task_conformance_status, required_gold_step_ids(list),
      allowed_ranges {D1,D2,D3a,D3b,D4,D5,D6}, held(bool), held_reason,
      frozen_record_contradiction(bool), policy("A"/"B"),
      eligibility {"policy_A": bool, "policy_B": bool},
      input_shas {...}, prior_rating_material_present(bool, 必须False)
    返回 (ok, errors, review_flags)。"""
    vocab = vocab or load_vocabulary()
    errors, review = [], []

    def err(gate, msg):
        errors.append({"gate": gate, "message": msg})

    # ---- 泄漏门（F05：评分输入不得携带旧分/旧key_error/模型身份） ----
    if inputs.get("prior_rating_material_present"):
        err("V05-G0", "评分输入携带旧评分材料（旧分/旧key_error/模型身份）——必须剥离")

    # ---- G8 HELD槽不得有评分返回 ----
    if inputs.get("held"):
        err("V05-G8", "HELD槽(%s)不应被发送/接受评分返回" % inputs.get("held_reason", ""))
        return False, errors, review

    # ---- G6 身份回显 ----
    echo = rating.get("route_alignment_echo") or {}
    if echo.get("route_status") != inputs["route_status"]:
        err("V05-G6", "route_alignment_echo.route_status(%s)≠输入(%s)" % (
            echo.get("route_status"), inputs["route_status"]))
    for k, v in (inputs.get("input_shas") or {}).items():
        if str(rating.get("input_identity_echo", {}).get(k, "")) != v and \
           str(echo.get(k, "")) != v:
            err("V05-G6", "输入SHA回显缺失/不符：%s" % k)

    # ---- G2 矩阵完整性 ----
    matrix = rating.get("step_evidence_matrix") or []
    got_ids = {row.get("gold_step_id") for row in matrix}
    want_ids = set(inputs["required_gold_step_ids"])
    if got_ids != want_ids:
        err("V05-G2", "step_evidence_matrix行集≠必答步集（缺%s，多%s）" % (
            sorted(want_ids - got_ids)[:3], sorted(got_ids - want_ids)[:3]))
    for row in matrix:
        if row.get("step_conclusion_7class") not in vocab["step_conclusion_classes"]:
            err("V05-G2", "矩阵行结论枚举非法：%s" % row.get("step_conclusion_7class"))
        if row.get("evidence_five_state") not in vocab["evidence_five_state"]:
            err("V05-G2", "矩阵行五态枚举非法：%s" % row.get("evidence_five_state"))
        if row.get("target_credit_usable") not in ("YES", "NO_ROUTE_BLOCKED",
                                                   "NO_EVIDENCE",
                                                   "HOLD_PENDING_REPRESENTATION_REVIEW"):
            err("V05-G2", "target_credit_usable枚举非法：%s" % row.get("target_credit_usable"))

    dims = rating.get("dimensions") or {}

    # ---- G1 路线门按轴执行（F07：不再D1/D2一律双cap；轴依据见allowed_ranges来源表） ----
    if inputs["route_status"] == "DEVIATES":
        d1 = (dims.get("D1") or {}).get("score")
        if isinstance(d1, int) and d1 > 4:
            err("V05-G1", "确认路线偏离：D1任务轴不得超过4（得分%d）" % d1)
        d2 = (dims.get("D2") or {}).get("score")
        d2cap = inputs.get("d2_deviation_cap", 4)   # 由决策表按偏离类型给出（方向4/替换6/立体5）
        if isinstance(d2, int) and d2 > d2cap:
            err("V05-G1", "偏离类型对应D2化学轴上界%d（得分%d）；轴依据必须由决策表提供" % (d2cap, d2))
    if inputs.get("task_conformance_status") == "VIOLATED":
        d1 = (dims.get("D1") or {}).get("score")
        if isinstance(d1, int) and d1 > 4:
            err("V05-G1", "任务条件违背：D1不得超过4（得分%d）" % d1)

    # ---- G7 错路线步不得计目标信用 ----
    for row in matrix:
        if row.get("structure_match_and_direction") in ("NONMATCH", "MISSING") and \
           row.get("target_credit_usable") == "YES":
            err("V05-G7", "步%s路线未通过却target_credit_usable=YES" % row.get("gold_step_id"))

    # ---- G3 高档门（F04：按维度作用域；D1/D6永不受催化证据门限制） ----
    policy = inputs.get("policy", "A")
    elig = (inputs.get("eligibility") or {}).get("policy_%s" % policy)
    d3a = (dims.get("D3a") or {}).get("score")
    if isinstance(d3a, int) and d3a >= 9 and not elig:
        err("V05-G3", "D3a=9/10但政策%s资格不成立（计算值，非硬编码）" % policy)
    d2 = (dims.get("D2") or {}).get("score")
    if isinstance(d2, int) and d2 >= 9 and not inputs.get("d2_nine_ten_evidence_ok", False):
        err("V05-G3", "D2=9/10需关键转化获可靠支持（科学支持高档门仅作用D2/D3a相关声称）")
    gate = rating.get("high_tier_gate_attestation") or {}
    if (isinstance(d3a, int) and d3a >= 9) and not gate.get("nine_ten_eligible"):
        err("V05-G3", "9-10缺high_tier_gate_attestation自证或自证为false")

    # ---- G5 冻结记录矛盾cap（仅独立绑定；旧AI标签不构成） ----
    if inputs.get("frozen_record_contradiction"):
        if isinstance(d3a, int) and d3a > 4:
            err("V05-G5", "冻结官方记录独立反驳绑定声称：D3a cap≤4（得分%d）" % d3a)

    # ---- G4 区间门（各轴allowed range；越区间必须显式REVIEW_REQUESTED） ----
    brc = rating.get("base_range_compliance") or {}
    for dim in ("D1", "D2", "D3a", "D3b", "D4", "D5", "D6"):
        allowed = (inputs.get("allowed_ranges") or {}).get(dim, "")
        sc = (dims.get(dim) or {}).get("score")
        st = (dims.get(dim) or {}).get("score_status")
        if st in ("NE", "NA") or sc is None:
            continue
        r = _range_ok(sc, allowed)
        if r is False:
            if brc.get("within_range_or_review") == "REVIEW_REQUESTED_OUT_OF_RANGE":
                review.append({"gate": "V05-S1", "dim": dim,
                               "message": "区间外申请复核：%s=%d 允许%s" % (dim, sc, allowed)})
            else:
                err("V05-G4", "%s=%d超出允许区间%s且未申请复核" % (dim, sc, allowed))

    # ---- S3 高分低命中异常 ----
    try:
        c_conf = inputs.get("c_confirmed", 0.0)
        if isinstance(d3a, int) and d3a >= 7 and c_conf < 0.5:
            review.append({"gate": "V05-S3",
                           "message": "D3a≥7但C_confirmed=%.2f<0.5（高分低命中异常）" % c_conf})
    except TypeError:
        pass

    # ---- S5 规则ID引用 ----
    for dim, dv in dims.items():
        if isinstance(dv, dict) and dv.get("score_status") == "SCORED":
            ids = dv.get("rule_ids_cited") or []
            if not ids:
                review.append({"gate": "V05-S5", "message": "%s缺rule_ids_cited" % dim})
            for rid in ids:
                if not re.match(r"^(R05-[A-Z]{2}-[0-9]{2}[a-z]?|SDT-[A-Z0-9-]+|R2-[0-9]{2}|F[0-9]{2})$", str(rid)):
                    review.append({"gate": "V05-S5",
                                   "message": "%s引用未知规则ID：%s" % (dim, rid)})

    # ---- S6 同根事件一致性 ----
    caps = [d for d in ("D1", "D2", "D3a", "D3b", "D4", "D5", "D6")
            if (dims.get(d) or {}).get("key_error") == "Y"]
    if len(caps) > 1:
        flat = {tuple(sorted((dims.get(d) or {}).get("root_error_event_ids") or []))
                for d in caps}
        if len(flat) > 1:
            review.append({"gate": "V05-S6",
                           "message": "多维cap但ROOT_ERROR_EVENT_ID不一致（不连坐纪律复核）"})

    # ---- S2 争议 ----
    dispute = echo.get("dispute")
    # Invalid shapes are rejected by schema validation; do not crash the batch.
    if isinstance(dispute, dict) and dispute.get("has_dispute"):
        review.append({"gate": "V05-S2", "message": "评分者对路线诊断提出异议：入人工复核，程序状态不变"})

    # ---- S4 key_error=Y但对应维未cap（继承V0.4同型门） ----
    for dim, dv in dims.items():
        if isinstance(dv, dict) and dv.get("key_error") == "Y" and \
           isinstance(dv.get("score"), int) and dv["score"] > 4:
            err("V05-S4", "%s key_error=Y但score=%d>4" % (dim, dv["score"]))

    ok = not errors
    return ok, errors, review


def paid_run_gate(run_config):
    """F10/RUN_CONFIG：任何PENDING字段存在→拒绝付费运行（默认拒绝）。"""
    blockers = []
    if run_config.get("status", "").startswith("DRAFT"):
        blockers.append("config_status_draft")
    for f in run_config.get("pending_fields_summary", []):
        blockers.append(f)
    if run_config.get("freeze_record_status") != "FROZEN":
        blockers.append("freeze_record_not_frozen")
    return (not blockers), blockers
