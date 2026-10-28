# v0.4小样本评价进展与定稿边界请示

- 日期：2026-10-28；整理材料已通过Astra独立复核，可供用户提交；量表仍未正式冻结。
- 本稿不声明M5/M6全部通过，不声明V0.4_FROZEN，不替老师作最终决定

黄老师您好：

## 在线审阅入口与本次交付范围

- 沿用此前给老师共享材料的仓库：https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables
- **本轮完整审阅入口：https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review**
- [材料目录及阅读顺序](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/README.md)
- [老师要求—本轮交付逐项对照](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/TEACHER_REQUIREMENT_DELIVERY_MATRIX.tsv)
- [完整v0.4候选量表Word](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/rubric/LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1.docx)与[同内容纯文本](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/rubric/LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1_TEXT_EXTRACT.txt)
- [全部文件SHA清单](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/MANIFEST.sha256)；[可下载的整体审阅包](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/archives/LIKERT_V04_PUBLIC_TEACHER_REVIEW_20261028.tar.gz)

**不是只提交这一篇MD。** 本轮提供量表、32份匿名原题/原答、A原始评分及逐题理由、B收到的原始汇总、224维对照、30项第三人裁决与修订、证据登记、逐维统计、可复算脚本和审计依据。老师可以直接在GitHub分层阅读，也可下载整体包；不依赖学生电脑上的本地路径。

这里的“整体”指**当前小样本校准/定稿阶段的完整可审阅材料**，不是把后续尚未执行的120题×4模型正式主表和正式50–60份人工抽样也写成已交付。公开版不包含API密钥、原始通信/确认日志、私有模型身份映射、完整gold原表、模型权重、HPC巨型raw以及许可未确认的第三方网页/全文快照；出处、摘要级支持范围与哈希保留，具体公开/未公开清单见[材料边界说明](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/CONTENTS_AND_ACCESS_BOUNDARIES.md)。

按您10月15日方法文件和10月16日批复，小样本校准的收尾整理已完成，现用白话汇报进展、结果和限制，最后是三件请您决定的事。

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

原批准流程要求两位未看过既往AI分数的评价者独立评分。实际留档：A（学生本人）此前参与17项裁决——那是用户人工逐项确认、作为修订依据，不能替代双人独立校准，本轮流程偏离已如实登记；B方汇总文件仍自述"AI预评分、非独立H1"，按师兄转交意见接收；第三评价者已声明不兼任原A/B，签署与日期栏占位保留、未代签。因此我们**不声称**材料已证明完全满足原严格双盲H1条件，也不据此停工、不要求师兄整套重评——现有材料是否够用、缺多少，正是请您决定的第一件事。

## 四、请您决定的三件事（其余技术细节在附件矩阵，不逐条打扰）

1. **材料用途**：现有A/B原始对照+30项裁决+描述性统计，可否作为本期量表规则验证/定稿的依据？如仍需补足严格独立校准，请明确最小补充范围（我们不自行扩大、不默认重做全部32份）。kappa通过阈值您此前未指定，本轮报告未设任何阈值，是否指定由您决定。
2. **B001-D2单项科学保留**：该答案把磺酸糖一步"水解"成葡萄糖+亚硫酸盐，第三人维持3分并判关键错误，补充了"至少三段必需化学"论证；但形式氧化数核对显示硫两侧均为+4，已知加氧路线也不自动排除所有单步可能——我们保留其裁决值，同时不把这段论证标成已核实科学事实。请生物侧只确认这一条机理依据（不是请您替代化学专家逐题打分）；可否在保留该个案限制下继续量表定稿，请您决定。不删样本、不整轮重做。
3. **定稿口径统一**：D5"身份字段错误"与"引用错引"的编码区分、D6锚点"通常5–6档"保留弹性（7–8为个案裁量）、"UNRESOLVED事实/局部待核/整维NE"三层区分等，附件矩阵已给出建议说明——确认后即可写入定稿说明，不改规则文字、权重或阈值。

## 五、下一步（按既有安排，不新增授权）

待您确认用途与冻结边界后：正式核验工具生产化（M7）、共同题集120题/480份程序主表（P1，阶段表中尚未启动，现有G9/G10程序分保留可用）、约50–60份正式分层人工评价（M8）。本轮不重跑模型、不修改gold、不发布模型排名。

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
| 后续正式四模型报告还有什么 | [老师要求交付对照表](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-10-28_BIOSYSMODB150_Likert_V04_Calibration_Closeout_Review/TEACHER_REQUIREMENT_DELIVERY_MATRIX.tsv) | 批次B120/480主表、恢复敏感性、正式分层人工评价等明确仍待执行/核对，不用本轮32份替代 |

## 八、本轮结论与建议的推进顺序

1. **现在可以确认的**：候选量表、原型、初筛、评分包、意见对照和裁决收尾材料均已形成；离线整理统计经独立复核没有发现数值或转录错误。
2. **仍不能直接写的**：严格独立双人H1达标、76条证据全部独立认证、150题gold全部正确、B001机理证明完整、v0.4已经正式冻结，或当前四模型最终排名已产生。
3. **请您决定的范围**：现有材料作规则验证/定稿依据是否足够；B001留作单项保留时能否继续整体定稿；定稿解释矩阵哪些可采纳。不是请您重新打30项分，也不是重新申请已批准的原型开发。
4. **确认之后再执行**：按确认范围完善最终量表与必要最小补充，再做正式核验工具、明确gold版本的共同题集程序评价和正式分层人工抽样；不重复采样原模型，不把恢复输出回填批次A。

为避免把材料分散在聊天里，本轮以GitHub日期目录及SHA清单为完整入口。仓库首页与00_CURRENT_TEACHER_REVIEW_ENTRYPOINT会同时指向本日期目录，历史版本只作为历史保留。

学生 陈浩然侧（评测线）敬上

附件是独立复核通过的冻结整理快照，包内DRAFT字样保留构建时状态。通过的是整理、统计和反馈材料，不是严格独立H1条件或v0.4正式冻结。
