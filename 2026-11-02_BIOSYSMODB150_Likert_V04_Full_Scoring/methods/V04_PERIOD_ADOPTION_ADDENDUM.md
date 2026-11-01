# V04本期规则采用Addendum（F0封存）

- 任务：F0（LIKERT_V04_FULL_SCORING_20261029_R0 总合同 §5）。
- 日期：2026-10-29（北京时间）。执行器：用户派发的本地F0执行窗口。
- 性质：本期（480份全量AI辅助评分+人类锚点外部效度验证）规则采用与身份封存文件。
  本文件不重写任何科学条文，不修改任何已冻结规则字节，只登记"本期适用什么、以哪个字节为准、
  哪些语义问题仍然开放"。
- 权威链：老师10-28批复（SHA256=7c0b82092d20ea54a4f1db3c591313f29c55f33c5403f8f730242339e01322ef，
  2824字节）→ 总合同（SHA256=73dfc012d902f9223cb887fdaaedca22d55860c968572a6d7d65351e203f5844，
  38465字节）→ 本addendum。机器可读绑定见同目录 RULES_MANIFEST_V04_PERIOD.json。

## 一、本期规范正文与"候选"页眉处置

1. 老师10-28批复§二已确认v0.4量表条款**可用于本期评价**（有条件）。据此，下列R2净化版正文
   为本期规范基础，其历史页眉中的"CANDIDATE/候选"字样由本期授权覆盖——即：页眉状态字样不再
   表示"未获批"，但**科学正文一个字节不改**：
   - 评分者净化版Word：LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1.docx
     SHA256=2e4a5f048807d2201e6a3beb0c2d22c40b4d380bfa4a5245706377dd67f81d6e（60855字节）
     ——与总合同§3.3指定的Word SHA一致。
   - 其既有可读导出：LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1_TEXT_EXTRACT.txt
     SHA256=bcf78065c6a56b02e4647de61db20c02ee17526ac4913c40cdaa2b6bca8ca283（61541字节）。
     该导出是既有人读版本；本期**不新做**"去除候选字样"的改写导出，避免因改页眉触碰科学条文。
   - 协调完整版（ normative 正文与净化版一致，含协调侧附注）：
     LIKERT_v0_4_CANDIDATE_R2_COORDINATOR_FULL.docx
     SHA256=747a02f86d96a7e66a73a14529845b8b3ff226ed3e4de2e181607865ba288e7b（66756字节）；
     LIKERT_v0_4_CANDIDATE_R2_COORDINATOR_FULL_TEXT_EXTRACT.txt
     SHA256=333e23bcf3e396400717614335c825fa4f42ad8ff2ad49c83b746f190af7aea4（73787字节）。
   - 唯一主位置：R/56_BIODEGRADATION_LIKERT_V04_M4_HUMAN_CALIBRATION_PACKAGES_R2_20261026/
     stage_A/LIKERT_V04_M4_RATER_A_PACKAGE/rubric/（协调完整版在同目录树coordinator/下）。
     各包内字节一致 copies 由该目录树SHA256SUMS（461项，F0复验通过）绑定。
2. 配套规则文件（同rubric目录，字节冻结）：
   - CLAIM_GROUP_CRITICALITY_PREDEFINITION_R2.tsv
     SHA256=c4558b47776ce750a133fe23ec566561c493aa764890d6b1751ff5ada9cd2095（8759字节，CG01–CG20）；
   - CLAIM_GROUP_CRITICALITY_PREDEFINITION_R2_NOTES.md
     SHA256=de1615b63c0a10c47f3542f686d8a9678dcea6923fbfeaa63906aadd05b0f0e3（2466字节）；
   - 历史8题条件登记：CASE_CLAIM_GROUP_SCOPE.tsv
     SHA256=16a84c878082c9c51631dc697dd09e3919f58e28e6f0f2456c985b528a9a2abe（12240字节，48行）。
     **该8题表不得冒充120题覆盖**；本期120题覆盖由F0新生成的CASE_CLAIM_GROUP_SCOPE_120.tsv
     （720行=120题×6条件组，题面-only生成，与8题冻结表交叉核验48/48逐字节一致）承担。
3. 条件式关键性口径：用户2026-10-26确认（DECISION_CRITICALITY=CONFIRMED_TASK_CONDITIONAL_POLICY，
   决定记录SHA256=41ac596c07bfe1dac9a7c4e38fac4aa8b48350189c5f6ff7ad273cb5cb6153e1）。
   TASK_CONDITIONAL组的条件成立性在评分前逐题登记（仅读题面字段，不读答案）；
   CLAIM_CONDITIONAL组登记条件文本，逐声称判定在评分时按实际用途进行，不得按答案整体表现倒推分组。

## 二、维度、权重与数值规则（照已批条文执行，不新设）

1. 七维：D1/D2/D3a/D3b/D4/D5/D6，1–10整数；权重15/25/10/10/15/15/10。
   全可评时加权总分=1.5·D1+2.5·D2+D3a+D3b+1.5·D4+1.5·D5+D6；以程序复算为准。
2. 程序评分五层权重45/10/20/15/10属另一测量体系，与Likert七维**不互相换算**。
3. SYSTEMIC仍cap≤4且按构成要素定档，**不自设默认分/默认档区间**（UPD-11仍OPEN）。
4. D6"单点过度确信通常5–6档"保持弹性文字，**不变成一律5–6**；保留的高档个案（7/7/8）
   只作锚点/解释边界案例。
5. 老师未给kappa通过阈值，本期**不得新设**；人类锚点统计只报描述性一致性指标。
6. MISSING=1须确为答案未交付模块；NE/NA为空数值并带依据；模型调用失败是system_run_status
   失败而不是被测答案MISSING；任一整维NE/未约定NA→total_status=NOT_COMPARABLE，不重归一。
7. KE=Y必须有逐维失效论证与可定位核验证据，且对应分≤4；一个引用错误不自动连坐酶/菌/路径各维。
8. D5沿用既有六状态与集合语义（按CG组记录状态集合，不生成单一"最坏来源状态"替代集合）；
   正向可定位支持登记在事实核验层，不新增来源状态、不回填原交付状态。
9. B023型"身份字段不一致"不因旧编码字样自动判"已核实错引"；身份字段错误、引用是否支持该字段、
   其余引用待核三者分开（术语统一随UPD-01，仍OPEN）。
10. 已批条文能覆盖的照原文执行；确实不能定数值/定档的具体维度保留NE/UNRESOLVED并入队
    （F0_UNRESOLVED_QUEUE.tsv），不暂停全部480份，不由执行器发明分档。

## 三、锚点与校准材料使用边界

1. 保留合成教学锚点；**不向AI评分者或新人类包放入真实32份的分数/裁决锚点**。
2. B001（=V04-A-007=CANON-032=BIOPATH150_146）不得作已核实通用负例：3/Y裁决值与科学保留
   分别留档；生物侧单项核查按批复§三.4进行，不阻塞整批。F0已核实本case四个B槽均为
   batchA原生输出（非恢复文本），历史映射定位的是同一批答案字节；绑定见
   GOLD_AND_SCOPE_FREEZE_RECORD.json#b001_historical_mapping。
3. AI评分者看匿名ID、完整题面和原答；不看被测模型名、程序分、历史A/B/第三人分或先前排名。
   私有映射仅协调侧保存。

## 四、本期必须携带的披露（进F6不确定性章，不掩盖）

1. 旧M5一致性证据为**混合一致性**（A为学生本人且有17项既往裁决暴露、B为AI预评分汇总），
   STRICT_OLD_TWO_HUMAN_H1_MET=false，永久披露；不得改称"严格双人H1 PASS"。
2. 弱一致维度：D4=0.361、D3b=0.401、D6=0.403；USABLE28敏感性D3b=0.169、D4=0.257。
   这三维分数解读区间宽于其他维度；不添加凭空置信区间，不只报0.80掩盖低值。
3. 未完成外部人类验证的维度一律标"人类效度验证进行中"，不得标"已通过人工验证"。
4. 回顾性评价事实不变：可称"本次评分前冻结执行方案"，不能称"在原模型生成前预注册"。
5. 选择性恢复非随机：20份恢复输出的敏感性分析必须双视图交付（合同§6.6/§11.1）。

## 五、政策矩阵本期处置

19行旧政策矩阵（POLICY_FINALIZATION_MATRIX.tsv，
SHA256=1047e595cf9b560ba17f37cb962793232f5f93d3475b2fec399f774667a40ae8，15090字节）
另派生本期处置列：POLICY_DISPOSITION_FOR_PERIOD.tsv（同目录）。原则：
- 授权已解决的**适用性/流程门**不再OPEN（如"v0.4能否用于本期""是否要补做旧双人H1才能评分"
  "B001是否阻塞整批""格式小修是否重开整轮"）；
- 老师没有逐项裁决的**语义问题**不得一键RESOLVED（UPD-01/03/06/07/08/09/11及OBS系列语义项
  保持开放，按上表operational规则执行并入队）；
- 全部19行均不阻塞480份评分（blocks_480_scoring=FALSE），阻塞点只保留合同定义的三个交接门。

## 六、F0新登记开放项（不在19行矩阵内）

- F0-UQ-001-BIOPATH150_013：题面氧条件=mixed（兼性），CG04/CG10任务条件成立性无先例裁决。
  已批文本两处口径覆盖不一致（NOTES用户要旨"明确要求好氧/厌氧时关键" vs R2 task_condition列
  "以氧条件限定路线/环境"）。登记UNRESOLVED_NO_APPROVED_PRECEDENT并入队，待老师/生物侧裁决；
  仅影响该case两行关键性判定，不阻塞其余119 case；化学合理性仍由D2自身判据评价。
  详见F0_UNRESOLVED_QUEUE.tsv与CASE_CLAIM_GROUP_SCOPE_120.tsv对应行。

## 七、批次与版本纪律（本addendum自身）

- 本addendum为F0新建文件，不修改任何历史文件；旧Word/旧表保持字节（BEFORE/AFTER哈希见
  identity/READONLY_SOURCE_HASH_REGISTRY_*.tsv）。
- 提示词科学规则或证据实质改变→新run/version与影响评估（合同§13）；文案格式小修集中留痕。
- 本文件与RULES_MANIFEST_V04_PERIOD.json、POLICY_DISPOSITION_FOR_PERIOD.tsv、
  TEACHER_REPLY_ACCEPTANCE_MAPPING.tsv共同构成EXECUTION_RULE_PACKAGE的F0封存层；
  总合同状态EXECUTION_RULE_PACKAGE=TO_BE_SEALED_BY_F0由本组文件落实，待独立复核。
