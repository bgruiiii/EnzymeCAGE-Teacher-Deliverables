# M3-P1-2.1 Reaction Predictor Route Adjudication Package

日期：2026-07-26  
状态：**PILOT SCORED / FINAL ROUTE NOT SELECTED / IMPLEMENTATION LOCKED**

## 主入口

请先读仓库根目录：

```text
M3_P1_2_1_REACTION_PREDICTOR_ROUTE_ADJUDICATION_REQUEST_2026-07-26.md
```

该文件给出：

- 老师 §2.1 的原始合同要求；
- 三路线小试结果与科学边界；
- 学生侧分层方案建议；
- 需要刘老师 / 老师裁定的三个最小问题；
- 裁定前保持锁定的事项。

## 证据目录

`evidence/` 按审查顺序包含：

1. `P1_2_1_REACTION_PREDICTOR_THREE_ROUTE_PREAUDIT_AND_UNIFIED_PILOT_CONTRACT.md`
   — 答案解锁前冻结的三路线合同与边界。
2. `UNIFIED_PILOT_INPUTS.json`
   — 三路线统一输入。
3. `UNIFIED_PILOT_ANSWER_KEY.json`
   — 门禁通过后才解锁的答案钥匙。
4. `M3_P1_2_1_ANSWER_KEY_UNLOCK_AND_SCORING_POLICY_FREEZE_2026-07-26.json`
   — 解锁前冻结的评分政策。
5. `M3_P1_2_1_REACTION_PREDICTOR_PILOT_EVIDENCE_REGISTRY.json`
   — 证据身份注册表。
6. `ENZYMECAGE_M3_P1_2_1_ANSWER_KEY_UNLOCK_GATE_AND_SCORING_POLICY_FREEZE_LOCAL_AUDIT_2026-07-26.md`
   — 25/25 门禁审计。
7. 三份 A/B/C HPC 返回本地审计。
8. `ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_ANSWER_KEY_UNLOCK_AND_TARGET_SCORING_LOCAL_AUDIT_2026-07-26.md`
   — 人类可读总评分。
9. `ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_TARGET_SCORING_MACHINE_REPORT_2026-07-26.json`
   — 机器评分。
10. `ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_TARGET_SCORING_INDEPENDENT_VALIDATOR_REPORT_2026-07-26.json`
    — 43/43 独立重算与 6/6 反向测试结果。

## 完整性文件

```text
DELIVERABLE_SHA256SUMS.txt
M3_P1_2_1_REACTION_PREDICTOR_ROUTE_ADJUDICATION_PRESUBMISSION_INDEPENDENT_AUDIT_2026-07-26.md
```

SHA256 清单覆盖根目录主入口、此 README、独立提交前审计和全部证据文件；
仅清单自身因避免循环校验而不纳入。独立审计单独核对清单、JSON 可解析性、
源文件字节一致性和边界措辞。

## 明确未交付

本包没有：

- 选择最终生产路线；
- 修改 `reaction_prediction_node`；
- 把 B 的 product-only 输出包装为完整反应；
- 把 C-exact 的已知反应查表结果包装为未知反应泛化；
- 启动 M4b/M4c；
- 启动 M3-EXT 补资产或模型运行。
