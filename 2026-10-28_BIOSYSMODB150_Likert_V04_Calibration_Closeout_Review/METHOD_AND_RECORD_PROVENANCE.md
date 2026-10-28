# 方法与记录溯源（METHOD_AND_RECORD_PROVENANCE）

- 日期：2026-10-28；构建：离线整理执行器；状态：`DRAFT_PENDING_ASTRA_AUDIT`
- 全程 `NETWORK_CALLS=0`、`MODEL_API_CALLS=0`、`MODEL_RERUNS=0`、`ORIGINAL_SCORES_MODIFIED=false`。
- 统计标签（每表每行携带）：`comparison_basis=A_SUBMISSION_VS_B_SUBMITTED_OPINIONS_DESCRIPTIVE`

## 1. 记录分层与性质（先钉死性质，再谈统计）

| 层 | 记录 | 性质声明（原文依据） |
|---|---|---|
| A原始冻结 | ratings_initial_frozen.tsv（32行）+ case_reviews/32份 + confirmation_log.jsonl + human_attestation.txt | 本人声明人工判断、AI转录；A既往参与17项争议裁决、自行阅读/批量确认的流程偏离已登记（RATER_EXPOSURE_AND_PROTOCOL_DEVIATION.md、attestation原文）。不改写为"仅AI整理"，也不声称无历史接触 |
| B提交汇总 | SUMMARY_PREREVIEW.md（32行markdown表） | 原文自述"AI预评分、非独立H1"；按师兄转交意见接收；只有数值分+KE列，无逐维status/完整理由；缺失status登记为NOT_PROVIDED_NUMERIC_ONLY，**不补为SCORED** |
| 第三人v2 | v2 ZIP（收到值经审阅目录SHA256SUMS核验）+ ADDED_EVIDENCE 76条 | 30个指定维度，与原A/B不是同一评分轮；补证后意见不倒填为补证前独立评分 |
| 裁决派生层 | ADJUDICATION_30_CONFIRMED_DERIVED.tsv + 确认回复10行修订 | 实际评价者声明不兼任原A/B；签署/日期占位保留、未代签；派生层不是原始独立H1 |

严格双人独立H1条件是否满足：**不由执行器宣布**（`STRICT_TWO_HUMAN_H1_CONDITION_DECLARED_MET=false`）。

## 2. 配对方法（任务A）

- 连接键：canonical_id（A/B两份私有映射），并逐对核验 `visible_answer_sha256`、`original_question_sha256`、`case_id`、`engineering_class` 四项A/B一致；**不按同号相减**（V04-A-001≠V04-B-001所指答案）、**不按case_id独连**（每case有4份，case连接会产生16对多对多）。
- 32对×7维=224维项；A分值/状态取自冻结TSV原行，B分值/KE取自markdown表原行（解析时记录行号作引用定位）。
- 触发原因独立重算（差≥3、KE分歧、A整维NE对B数值），排序约定与既有表一致（SCORE_GAP_GE3;KEY_ERROR_DISAGREEMENT;A_NE_NA_VS_B_NUMERIC）；与ALL_224_DIMENSION_COMPARISONS.tsv逐单元交叉复验（224行×13字段+KE两列），**零失配**；与ALIGNED_32_ANSWER_PAIRS.tsv交叉复验（32行×5字段），零失配。数字不是从旧报告复制自证。

## 3. 统计方法（任务B）

- 指标：逐维 exact、within-1、MAE、平均有向差（A−B）、线性加权Cohen's kappa。
- kappa：**线性权重 w(i,j)=1−|i−j|/9，固定1–10全刻度**（POST_RATING_AUDIT_PROTOCOL.md预登记的报告方法，非通过阈值）。实现：混淆矩阵公式 κ=(po−pe)/(1−pe)，po=Σw·conf/n，pe=Σw·row·col；**手写实现**——sklearn未安装且禁止联网安装（本机Python 3.10.12、numpy 2.2.6、pytest 9.1.0）。
- 独立小例验算（构建时自检+tests/固化）：
  - 手算例 [(1,1),(2,3)]：po=17/18、pe=8/9 → κ=0.5（精确）；
  - 完全一致且边缘分布非退化 [(1,1),(1,1),(2,2),(2,2)] → κ=1.0；
  - 零方差 [(5,5),(5,5)]：pe=1 → **UNDEFINED**（不填0、不吞NaN）；
  - n=0 → **UNDEFINED**。
- NE处理：A整维NE（5项：V04-A-005/D3b、V04-A-007/D2·D3a·D3b、V04-A-015/D3b）无数值，成对排除、逐维分别列有效n（32/31/31/29/32/32/32），不填0/1/5或中间分；有效配对合计219=224−5。
- MISSING处理：A侧8个MISSING格（V04-A-014全7维、V04-A-007/D4）保留原1分入数值比较，`a_missing_included_count`单列；解释为交付缺失，不与科学能力混同。
- KE分歧计数分母为该口径全部行（含NE行，KE比较不依赖数值），原32口径逐维3/5/5/0/0/3/5、合计21，与触发登记一致。
- 双口径：主口径=原32份；敏感性=USABLE28（剔V04-B-016/B-023/B-028=INVALID_JSON、V04-B-026=LENGTH_EMPTY，剔除对象在表中点名不隐去）。
- 禁止事项自查：无第三人值回填后再报"原始一致性提高"；统计覆盖全部32份而非只筛30争议项；NE未当中间分；空答案未丢分母；未设任何通过阈值；未生成"协商后A/B评分"。

## 4. 裁决收口方法（任务C）

- 确认回复markdown的10行修订表**程序化解析**（剥离加粗标记与全角括注、按"→"拆分），与EXPLICIT_10_ROW_AMENDMENTS.tsv、ADJUDICATION_30_CONFIRMED_DERIVED.tsv三方逐字段核对一致；分数改变=3、KE改变=2、其余20项v2原值未动；KE计数9/11/10复算一致。
- 30项的原A/B值**从原始记录重建**（A冻结TSV+B汇总markdown，经canonical配对），与ORIGINAL_A_B_V2_AND_RESPONSE_COMPARISON.tsv全字段比对：30/30 MATCH。未生成"最终32份评分"。
- RETAIN 3项（B010-D3b、B011-D3b、B032-D2）：基线草案版本不明的字段原样保留，明确v2数值作候选值，不推断等于B原分。

## 5. 证据分层方法（任务C）

EVIDENCE_VERSION_AND_LIMITATIONS.tsv 共88行、5层，逐行带layer与source_ref：

1. `ORIGINAL_FROZEN_EVIDENCE_SNAPSHOT_20261026`（1行引用）：原共同冻结证据快照 b8b44d55…（A冻结manifest登记），与新增证据分开；
2. `THIRD_PARTY_ADDED_EVIDENCE_20261028`（76行）：25行HASH_MATCH（快照SHA与归一化表一致，可离线读取）、51行URL_QUOTE_ONLY（不可离线重放，不冒充已独立核验）；
3. `COORDINATOR_INDEPENDENT_OFFICIAL_CHECK_20261028`（4行）：ec_4.5.1.1、ec_1.1.1.160、ec_3.1.1.31、pmid_16996055，raw/meta已归档；登记为协调端补充核验，不冒充第三人当时留存文件；本卡未重发请求；
4. `EVIDENCE_COLUMN_NORMALIZATION_LOG`（4行）：EV007-05/EV007-16/EV029-17/EV029-18列错位归一化，scientific_fact_changed=NO，原文未改；
5. `GLOBAL_CAVEAT`（3行）：51条无raw限制、二次引用不计独立实验、负检索不判不存在。

## 6. 输入闭包与完整性

- 23个只读输入锁+执行卡本体：开工前逐项SHA256核验通过（INPUT_IDENTITIES_BEFORE.tsv）；A冻结目录内部SUMS、v2审阅目录SUMS全项OK；收尾后复核（INPUT_IDENTITIES_AFTER.tsv）须与BEFORE一致。
- 扩展闭包（实读但不在23锁内的文件：A的32份case_reviews、confirmation_log.jsonl、ALIGNED_32_ANSWER_PAIRS.tsv、ORIGINAL_A_B_V2_AND_RESPONSE_COMPARISON.tsv、ADDED_EVIDENCE_NORMALIZED_DERIVED.tsv、EVIDENCE_SNAPSHOT_CHECKS.tsv、EVIDENCE_COLUMN_NORMALIZATIONS.tsv、V2_RECEIPT_AND_CHECKS.json、independent_official_raw/8文件、RATER_EXPOSURE_AND_PROTOCOL_DEVIATION.md、POST_RATING_AUDIT_PROTOCOL.md、量表全文提取等）：路径/字节/SHA/用途逐项登记于同一TSV的EXT行。
- 未读取SOURCE_MODEL_PROVENANCE.tsv等模型身份映射；本目录材料不发给尚在独立评分的评价者；未生成任何模型排名。
- 历史脚本红线：未运行inspect_v2.py（含4次官方查询）及任何会写回源目录/联网的脚本；对A冻结文件未重跑冻结器。

## 7. 复算入口

`scripts/`内构建器全部离线确定性：build_task_a.py（配对/224维/触发）、build_task_b.py（统计，含kappa自检）、build_task_c.py（裁决/证据）、build_task_d.py（政策矩阵+B001链核验）；validate_closeout.py为独立验证器（从实物重算，不用报告自证）；tests/为合成反例测试（全部合成评分只在TemporaryDirectory）。
