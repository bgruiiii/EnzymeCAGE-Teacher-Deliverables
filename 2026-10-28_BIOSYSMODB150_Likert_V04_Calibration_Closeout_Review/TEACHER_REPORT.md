# 申请确认v0.4并尽快启动四模型全量评分

- 日期：2026-10-28；整理材料已通过Astra独立复核，可供用户提交；量表仍未正式冻结。
- 本稿不声明M5/M6全部通过，不声明V0.4_FROZEN，不替老师作最终决定

黄老师您好：

## 本次核心申请：若v0.4可用，请授权尽快全量出分

师姐已经在催促出分。结合您此前“别加新东西、把已有任务收口”的意见，我们希望本轮不再停留于反复校准细节，而是尽快完成现有四模型评价。

**若您认可当前v0.4及已披露限制可用于本期评价，恳请同步确认量表适用版本，并授权立即推进批次B共同120题×4模型＝480份冻结答案的全量AI辅助Likert评分和评价侧证据核验，同时整理离线程序评分主表。**

**人工抽查请您统筹安排**：样本量、人员、时间以及是否与全量出分并行，由您决定，我们不自行新增一轮人评作为启动前置。若有不能豁免的人工前置，烦请一次明确最小范围；其他抽查建议并行或随后补充，避免长期等待。未完成人工验证的条目如实标注，不声称已人审。

申请的是对已经收集的答案全量评分，不重采样模型、不补写模型答案。150题中的29条隔离题不纳入；正式121题中B共同集排除持续失败BIOPATH150_023后为120题。全量指480行评分/状态覆盖，不强迫未核事实填成确定分数。**这是本轮执行申请，尚未视作您已批准付费调用或正式评分。**

[详细执行范围与人工抽查安排请示](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/FULL_SCORING_AUTHORIZATION_REQUEST_20261028.md)

## 在线审阅入口与本次交付范围

- 沿用此前给老师共享材料的仓库：https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables
- **本轮完整审阅入口：https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review**
- [材料目录及阅读顺序](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/README.md)
- [老师要求—本轮交付逐项对照](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/TEACHER_REQUIREMENT_DELIVERY_MATRIX.tsv)
- [完整v0.4候选量表Word](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/rubric/LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1.docx)与[同内容纯文本](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/rubric/LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1_TEXT_EXTRACT.txt)
- [全部文件SHA清单](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/MANIFEST.sha256)；[可下载的整体审阅包](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/archives/LIKERT_V04_PUBLIC_TEACHER_REVIEW_20261028.tar.gz)

**不是只提交这一篇MD。** 本轮提供量表、32份匿名原题/原答、A原始评分及逐题理由、B收到的原始汇总、224维对照、30项第三人裁决与修订、证据登记、逐维统计、可复算脚本和审计依据。老师可以直接在GitHub分层阅读，也可下载整体包；不依赖学生电脑上的本地路径。

这里的“整体”指**当前小样本校准/定稿阶段的完整可审阅材料**，不是把尚未执行的120题×4模型全量评分、程序主表和老师待安排的人工抽查写成已交付。公开版不包含API密钥、原始通信/确认日志、私有模型身份映射、完整gold原表、模型权重、HPC巨型raw以及许可未确认的第三方网页/全文快照；出处、摘要级支持范围与哈希保留，具体公开/未公开清单见[材料边界说明](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/CONTENTS_AND_ACCESS_BOUNDARIES.md)。

按您10月15日方法文件、10月16日批复及后续收口意见，小样本收尾材料已经形成并核对。以下保留完整进展、数据和限制，核心请求是一次确认v0.4适用范围与全量评分启动安排，尽快得到可复核主表。

## 一、为什么做这件事（白话）

此前17项争议由我人工逐项确认，暴露出光靠gold字符串或评分AI的记忆会漏掉真问题：有真实编号不等于支持所写功能，菌株身份、单步能力和完整路径能力是三回事。所以按您批准的方向修订了v0.4候选量表，先用小规模材料验证"评价侧查证机制+评分条款"能不能被实际执行——查证工具只当"判卷的显微镜"，从不递给被测模型，也不回填成模型原有引用。

## 二、做了什么、结果如何

**已完成（实物在案）**：M1–M4——v0.4候选量表R2、五库证据核验原型（30次请求39条规范化记录、离线可重放）、3题窄复核+150题只读初筛、A/B两份32答案匿名校准包。这不是150题科学事实全量认证，也不是全量API评分。

**本轮收尾整理（全部离线、原分未动）**：

1. **原始对照**：A冻结32份与B提交32份意见按答案SHA一一配对，8题×4份=32对、224个维度项；A侧状态SCORED=211、MISSING=8、NE=5，可数值配对219项。与既有对照表交叉复验零失配。
2. **逐维描述性统计**（A提交 vs B提交意见，方法=预登记的线性加权kappa w=1−|i−j|/9，固定1–10刻度；下表为原32份主口径，USABLE28敏感性另列于附件表）：

| 维度 | 有效n | exact | within-1 | MAE | 加权kappa | KE分歧 |
|---|---|---|---|---|---|---|
| D1 | 32 | 46.9% | 93.8% | 0.594 | 0.680 | 3 |
| D2 | 31 | 48.4% | 80.6% | 0.903 | 0.513 | 5 |
| D3a | 31 | 54.8% | 87.1% | 0.581 | 0.597 | 5 |
| D3b | 29 | 44.8% | 75.9% | 0.966 | 0.401 | 0 |
| D4 | 32 | 31.3% | 81.3% | 0.906 | 0.361 | 0 |
| D5 | 32 | 81.3% | 93.8% | 0.250 | 0.796 | 3 |
| D6 | 32 | 31.3% | 87.5% | 0.875 | 0.403 | 5 |

   D1任务符合度、D2路径、D3a酶、D3b微生物、D4性状、D5来源、D6不确定性。USABLE28敏感性中，D3b的kappa为0.169、D4为0.257，进一步提示这些边界仍需关注，不能只摘全样本较高值宣布校准通过。

   这是**已收评分之间的数学描述**，未设通过阈值；不是协商后结果，也没有把第三人分数回填进A/B再报"一致性提高"。
3. **定点裁决收口**：触发复核的30个维度/15份答案（差≥3共9、KE分歧21、A整维NE对B数值5，原因有重叠）已由第三评价者裁决；其确认回复明示修订10行，其中3项分数、2项关键错误判定改变，整合后KE=是9/否11/待核10。原A/B分数与裁决值并列保存，未生成"最终32份评分"。其余194项只是本轮未触发，不等于已被确认正确。
4. **补证证据分层**：第三人新增证据76条（25份原文快照已在本地按SHA核对并可本地离线读取；51条仅URL/引文，不声称已全部独立核验；公开仓库发布来源、必要引文和哈希，不重发许可未确认的第三方全文/商业网页）；协调端另做4次官方核验单独登记。原共同冻结证据与新增证据分开，补证后意见不倒填成补证前独立评分。

## 三、限制（如实说明，不暗示已达标）

原批准流程要求两位未看过既往AI分数的评价者独立评分。实际留档：A（学生本人）此前参与17项裁决——那是用户人工逐项确认、作为修订依据，不能替代双人独立校准，本轮流程偏离已如实登记；B方汇总文件仍自述"AI预评分、非独立H1"，按师兄转交意见接收；第三评价者已声明不兼任原A/B，签署与日期栏占位保留、未代签。因此我们**不声称**材料已证明完全满足原严格双盲H1条件。请您决定在这些限制如实披露的情况下，v0.4能否用于本期正式全量评价；如仍有不可豁免前置，请一次列出最小范围。我们不自行新增整套重评，也不把记录说明等非实质修补无限延长为出分前置。

## 四、希望您一次确认的启动事项

1. **v0.4适用与全量评分授权**：若当前候选及已披露限制可以接受，请确认本期适用版本，并授权对B共同120题/480份冻结答案开展全量AI辅助评分和必要证据核验，离线程序主表同步推进。评分AI的版本、固定提示词、结构化输出、费用上限、并发与有限重试在执行卡中锁定，未获确认前不实际调用。
2. **人工抽查由您安排，尽量不阻塞主表**：原方法中的约50–60份分层人工安排是否沿用、调整或并行，请您统筹。我们不自行取消原方案，也不默认追加一轮新的人工任务；希望允许先滚动产出带证据/人审状态的全量主表，抽查和争议裁决按您安排补充。若必须先完成某项人审，请明确最小不可豁免范围。
3. **保留单项，不拖整批**：B001-D2机理依据请生物侧针对性确认，其3/Y裁决值和科学保留分别留档，暂不当作已核实通用负例；请求您确认能否带保留继续其他条目全量评分。D5身份/引用、D6锚点弹性等解释在定稿说明集中统一，不因个别文字/字段/打包问题反复重开整轮评价。确实影响规则、公平性或分数正确性的实质问题仍单列处理。

## 五、获准后以出分为主线推进

- **先锁一次执行合同**：确认量表、所选gold、评分AI/版本/提示词、证据快照、费用上限和恢复策略；不根据得分高低调提示词，不重采样原模型。
- **只做必要通路检查**：复用现有32份和已验API原型检查输入、输出格式、计数、公式、证据定位与缓存，最小必要适配后进入全量，不先开发大而全平台或扩展研究分支。
- **全量评分与程序表并行**：形成480行全覆盖的评分/状态主表，原程序科学轴、v0.4评价轴、证据轴和弃答轴并列；旧G9/G10不被覆盖，新gold版本不混算。
- **人工抽查按您安排并行/随后进行**：明确哪些是AI评价、哪些已人审、哪些待核，不能把未完成抽查标成已通过，也不让未明确的人工新轮次长期阻塞整批结果。
- **区分实质问题和小修**：题目/答案错配、规则版本混用、分数计算错误、数据漂移、密钥和预算风险等必须处理；文案、目录、说明、格式等集中留痕修订，不触发模型重跑或全批重评。
- **逐批汇报、保留边界**：先交可复核的全量阶段表和数据，单项疑难留队列，必要时附影响分析；最终排名与论文结论标明证据/人审覆盖，不把阶段出分冒称所有科学问题已解决。

本申请是为落实已有任务尽快收口，不增加新模型训练、新题集或额外原生采样。人工抽查的具体工作量和时点完全请您安排。

## 六、随稿附件

原始32份/224维对应表与逐维统计表（含方法与有效n）、30项裁决层与10行修订日志、原值/裁决值并列表、证据版本与限制表（88行分层）、政策定稿矩阵（19行）、B001单项保留说明、定稿备忘、人员与流程边界说明、全部输入SHA与只读核验结果。

## 七、老师原要求与本轮材料对应

您10月15日方法文件第六节要求的是：批次A最终轴系表、批次B共同题集主表及恢复敏感性、人工评价包（抽样框/原始评分/一致性/分歧归因）、汇总报告和全部产物SHA清单；不是规定“只交单个MD”。10月16日又明确了候选量表和核验资料先冻结、同8题人工校准、原始一致性与第三人复核、送您确认后冻结的顺序。

本次着重提交后一个校准/定稿阶段，包含以下可直接检查的材料：

| 要核对什么 | GitHub内位置 | 能据此判断什么／不能据此判断什么 |
| --- | --- | --- |
| 实际使用的评分标准 | [rubric/](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/rubric) | 完整候选正文、任务关键性与条件表；不是已冻结正式量表 |
| 这8题如何构成32份材料 | [32份对应表](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/tables/ORIGINAL_32_ITEM_PAIRING.tsv)、[匿名原题与原答](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/answers) | 每case4份、原文未润色；历史固定校准样本，不替换为后来恢复答案 |
| A实际提交的分数和理由 | [A冻结评分](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/inputs/A/ratings_initial_frozen.tsv)、[32份逐题理由](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/inputs/A/case_reviews) | 保留NE、MISSING、覆盖与KE；个人实际流程/既往经历按方法说明解释 |
| B方收到的评分意见 | [原始汇总](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/inputs/B/SUMMARY_PREREVIEW.md) | 来源自述原样保留；不补造缺少的逐维status、理由或人工确认 |
| 为什么只筛30个维度项 | [224维原始对照](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/tables/ORIGINAL_224_DIMENSION_PAIRS.tsv)、[触发清单](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/tables/DISPUTE_TRIGGER_REGISTER.tsv) | 差≥3、KE分歧和NE对数值逐项可追；同分不同KE也保留 |
| 第三人最终给了什么、改了什么 | [30项裁决](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/tables/ADJUDICATION_30_DECISIONS.tsv)、[修订日志](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/tables/ADJUDICATION_CHANGELOG.tsv)、[确认回复公开副本](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/third_review/CONFIRMATION_RESPONSE_PUBLIC.md) | 原分、v2、确认后值分开；不能把裁决后趋同当作原始一致性 |
| 原始意见差距有多大 | [逐维统计](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/tables/DESCRIPTIVE_AGREEMENT_BY_DIMENSION.tsv)、[方法与来源](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/METHOD_AND_RECORD_PROVENANCE.md) | 有效n、exact、within-1、MAE、有向差、线性加权kappa；含USABLE敏感性、无通过阈值 |
| 新证据具体支持到哪里 | [证据登记](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/evidence/ADDED_EVIDENCE_REGISTER_76_NORMALIZED.tsv)、[快照核对索引](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/evidence/SNAPSHOT_INTEGRITY_INDEX.tsv) | 身份/反应/全路径/性状范围、原文定位与局限；覆盖不等于支持，负检索不判不存在 |
| AI具体参与了什么 | [AI辅助溯源说明](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/AI_ASSISTANCE_PROVENANCE.md) | 预审、导航、检索、转录分层；未记录的模型版本/实际提示词明确未知，不猜填 |
| 量表哪些条款还待定 | [政策矩阵](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/tables/POLICY_FINALIZATION_MATRIX.tsv)、[定稿备忘](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/V04_FINALIZATION_MEMO_CANDIDATE.md) | 已决、待确认、仅技术整理分开，不重开已决事项、不擅自增加阈值 |
| B001为什么暂不作通用负例 | [单项保留说明](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/B001_D2_SCIENTIFIC_RESERVATION.md) | 3/Y作为提交裁决保留、硫记账不作机理证明，未删样本或自动改分 |
| 整理过程是否算对、改过原始值 | [独立审计](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/audits/ASTRA_CLOSEOUT_AUDIT_20261028.md)、[公开数据复算脚本](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/scripts/verify_public_statistics.py) | 统计和修订可从公开输入复算；这不是所有科学事实全量认证 |
| 后续正式四模型报告还有什么 | [老师要求交付对照表](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/TEACHER_REQUIREMENT_DELIVERY_MATRIX.tsv) | 本轮申请120/480全量AI评分与程序主表；人工抽查范围/时点请您安排，未执行内容不写成已完成 |

## 八、希望本轮反馈直接落到执行安排

1. 已有候选量表、原型、初筛、校准数据、第三人裁决和离线统计作为依据，全部可审阅；这些工作不是再开启一轮校准的理由。
2. 现有记录来源、10项KE待核与B001科学保留继续如实披露，不以赶进度掩盖，也不自动改成已核实。
3. **核心请示是：认可v0.4后，同步授权尽快开始480份全量AI辅助评分与证据核验，不只继续等待小样本细节；人工抽查由您统筹，尽可能并行、不重复扩大。**
4. 若确有不能豁免的前置，请一次列明最小范围及安排；其他单项保留和非实质小修随结果集中处理，不让整批分数长期不出。
5. 全量评分费用、并发、版本及输出合同在执行卡中固定，经确认再运行；本请求不冒称已经获准或已产生正式分数。

详细材料已在GitHub日期目录，原32份与全部冻结结果仍保留。仓库现行入口将同步本次全量评分申请，历史版本可由commit追溯。

学生 陈浩然侧（评测线）敬上

附件是独立复核通过的冻结整理快照，包内DRAFT字样保留构建时状态。通过的是整理、统计和反馈材料，不是严格独立H1条件或v0.4正式冻结。
