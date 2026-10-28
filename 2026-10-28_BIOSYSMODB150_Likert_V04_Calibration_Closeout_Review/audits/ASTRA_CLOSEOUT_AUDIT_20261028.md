# v0.4校准收尾整理包：最终本地审计

- 日期：2026-10-28；审计者：Codex/Astra。
- 对象：M5_CLOSEOUT_M6_PREPARATION_20261028。
- 结论：`PASS_FOR_TEACHER_PROGRESS_SUBMISSION`。
- 范围：离线整理、描述性统计、裁决修订转录、证据分层和教师进度/决策材料，可以提交。
- 不代表：严格双人独立H1条件已满足、全部科学争议已解决、M5/M6整体通过或v0.4正式冻结。

## 1. 独立复核结果

本次没有调用执行器的构建/验证入口重写收尾包；使用独立脚本读取原A冻结、B原Markdown、canonical映射和确认后的裁决层。

1. A/B按canonical与原答案SHA一一对应，32份、224维；219个可数值对，NE5保持无数值。
2. 原始争议触发独立复算：30维/15份，差≥3为9、KE分歧21、NE对数值5；重叠不重复计争议。
3. 用标准库Fraction按距离形式独立计算线性加权kappa，不复用执行器common.py，也不依赖其numpy验证函数。
4. 逐维n、exact、within-1、MAE、有向差、kappa、KE分歧及分母共14行，全部与交付表四位小数容差内一致，无差异。
5. 30项裁决数值/KE与已锁定整合源一致；10行变更中3项分数、2项KE改变，最终KE=9Y/11N/10UNRESOLVED。
6. 重新运行16项合成测试（python -B，关闭pytest缓存），16/16 PASS；临时测试没有改动真实评分。
7. 输入表78条数据记录：76条文件哈希记录、2条目录SUMS结果。全部复核一致，BEFORE/AFTER相同。内部A冻结37项、v2审阅66项SHA全过。
8. 冻结交付物SUMS全过，tar单根29个普通文件成员，其中28个payload由内部SUMS覆盖；无重名、链接、危险路径，归档内文件和磁盘一致。
9. 独立构造TarInfo及gzip重新封装冻结内容，得到与交付tar逐字节相同的结果。
10. 审计与测试前后，原收尾目录全树SHA相同。网络/模型API/模型重跑均0。

## 2. 已复算的主要统计

下列是已收A记录与B提交意见的数学描述，不是已经验证的双人独立专家一致性：

| 维度 | 原32有效n | 原32线性加权kappa | USABLE28有效n | USABLE28 kappa |
| --- | --- | --- | --- | --- |
| D1 | 32 | 0.6803 | 28 | 0.5978 |
| D2 | 31 | 0.5129 | 27 | 0.4059 |
| D3a | 31 | 0.5974 | 27 | 0.5535 |
| D3b | 29 | 0.4012 | 25 | 0.1686 |
| D4 | 32 | 0.3609 | 28 | 0.2571 |
| D5 | 32 | 0.7959 | 28 | 0.7612 |
| D6 | 32 | 0.4035 | 28 | 0.3000 |

交付表与教师稿已经明确：B原文自述AI预评分/非独立H1，A既往17项裁决及流程偏离留档；无自设通过阈值。
未以第三人值替换A/B后报“原始一致性提高”，未把只评争议的子集冒充全样本。
不能只摘最高kappa当作已通过校准，尤其USABLE敏感性下部分维度明显更弱。

## 3. 科学与方法边界是否如实保留

已检查教师主文、短消息、方法说明、政策矩阵和B001 dossier：
- 人员与记录来源边界明确，没有把第三人或AI辅助层伪装为最初独立H1。
- B001对应V04-B-001=V04-A-007=CANON-032=BIOPATH150_146；A原NE、B原2与第三人3/Y并列，未改分、删样本。
- 硫+4→+4仅作为形式记账，未声称证明一步水解可行；必要机理仍保留，暂不作已核实通用负例。
- D5身份不一致/引用错引、D6“通常5–6”的弹性、正向支持编码及局部待核/整维NE等，均为候选定稿说明，不擅改规则或关闭全部OPEN。
- 原76条补证、25份快照、51条无raw、额外4次协调核验来源层分开，不声称全部证据独立认证。
- 当前提交是请老师确认材料用途与定稿边界，不要求老师替代生物专家逐题判断，也不启动M7/M8或重新运行模型。

## 4. 非阻塞技术观察

- INPUT_IDENTITIES表的两条SUMS结果把entries_ok/entries_bad存入哈希列，属于混合记录类型，不是对应文件被改；已按SUMS角色独立解析并复核37/66项。后续可增加record_type与专门计数字段，避免自动审计误读。
- CLOSEOUT_VALIDATION.json包含ran_utc，且在tar内。本次冻结内容可逐字节重建，已经独立证明；但若重跑验证生成新的UTC，再重建流水线，不能保证归档相同。后续版本应把运行时UTC日志移出确定性摘要。此项不影响本次统计或提交进度材料，不为此重做科学数据或修改已封存包。
- 输入表共78条数据行、含表头79行；“79 rows”需注明口径，避免误解为79个独立输入文件。
- 教师稿含DRAFT_PENDING_ASTRA_AUDIT为构建时状态。冻结稿不回写；可发送展示版另建，引用本审计解除“待核后才能提交”的停止线。展示放行不等于量表冻结。

## 5. 归档身份及复现证据

- tar：LIKERT_V04_CLOSEOUT_FOR_TEACHER_DRAFT_20261028.tar.gz。
- SHA256：5e555d631e655108eda77d56af89804788088eeff220ca37e327f37bd9d920c5。
- bytes：120781。
- 独立审计脚本：本目录LIKERT_V04_CLOSEOUT_INDEPENDENT_AUDIT_20261028.py。
- 机器记录：同名.json，含原件重算结果、逐维精确值、测试输出、归档重建和不变性检查。
- 复现不重跑原构建器；原始A/B及收尾包均保留。本次未发送任何内容给老师。

## 6. 放行与后续

允许由用户向黄老师发送进度反馈、定稿边界请示和附件。建议只问三项：当前材料用途/如需最小补充、B001科学保留处理、定稿解释口径。
后续老师和生物侧确认后，再决定量表最终冻结及正式工具/评价阶段；本审计不替代其决策。

```text
AUDIT_STATUS=PASS_FOR_TEACHER_PROGRESS_SUBMISSION
CLOSEOUT_DATA_AND_STATISTICS_VERIFIED=true
INDEPENDENT_STATISTIC_ROWS=14
SYNTHETIC_TESTS=16/16_PASS
ORIGINAL_SCORES_MODIFIED=false
FROZEN_CLOSEOUT_PACKAGE_MODIFIED=false
NETWORK_CALLS=0
MODEL_API_CALLS=0
TEACHER_REPORT_SENT=false
STRICT_TWO_HUMAN_H1_DECLARED_MET=false
B001_SCIENTIFIC_RESERVATION_RETAINED=true
V04_FROZEN=false
NEXT_ACTION=用户发送已审计反馈材料，等待老师对用途与定稿边界的决定
```
