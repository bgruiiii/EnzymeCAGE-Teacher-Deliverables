# CLAIM_GROUP_CRITICALITY_PREDEFINITION_R2 伴随说明（NOTES）

- 日期：2026-10-26；阶段：M4校准候选R2配套。
- 本表状态：**已按用户2026-10-26任务条件式口径确认用于本校准候选**
  （DECISION_CRITICALITY=CONFIRMED_TASK_CONDITIONAL_POLICY，用户决定记录SHA256=41ac596c07bfe1dac9a7c4e38fac4aa8b48350189c5f6ff7ad273cb5cb6153e1）；
  **正式冻结（M6）前仍需生物侧复核**；逐行确认状态见review_status列。
- R1版本首行的`#`注释已移入本说明；R2数据文件为标准TSV（首行即列名表头），
  读取方仍应使用comment-aware方式兼容历史R1文件（M1 R1最终审计§四.2互操作要求）。
- condition_type枚举：
  - UNCONDITIONAL：关键性不依赖题面条件，按criticality_when_condition_met列执行；
  - TASK_CONDITIONAL：按题面条件是否成立取met/unmet列值；条件成立性在评分前
    逐题登记于CASE_CLAIM_GROUP_SCOPE.tsv（仅读题面字段，不读答案）；
  - CLAIM_CONDITIONAL：分组条件文本在评分前按题面登记，具体声称是否落入关键组
    在评分时按该声称实际用途判定（不得按答案整体表现倒推分组）。
- 任务条件式口径（用户确认原文要旨）：氧条件在题面明确要求好氧/厌氧时属关键筛选
  依据；温度/pH/盐度仅在题面明确限定相应环境条件时为应用关键，未限定时默认辅助；
  底物利用仅在实际承担目标污染物降解能力论证时关键，普通碳源偏好为辅助。
- 关键组身份不自动封顶：只有经核实的错误实际使相应主要推荐/适用性结论失效，才按
  该维度既有关键错误规则处理；局部错误档内扣；证据不足待核（UNRESOLVED）。
- 同物种代表记录口径（用户2026-10-26决定）：物种级profile的性状参照可来自同物种
  代表菌株记录；这不改变答案侧声称的粒度匹配要求，也不宣称同物种各菌株性状相同。
- review_status枚举：USER_CONFIRMED_TASK_CONDITIONAL_20261026（用户确认的条件式分组行）；
  CARRIED_FROM_R1_FOR_CALIBRATION_CANDIDATE（沿承R1、用于校准候选、M6前生物侧复核）；
  PENDING_BIOLOGICAL_REVIEW_M6（生物侧复核保留至冻结门）。
- 未决联动：UPD-02（处置=RESOLVED_BY_USER_TASK_CONDITIONAL_POLICY，生物侧复核移至M6）、
  UPD-03/UPD-09（边界案例与合成参数仍OPEN，M5校准实证）。
