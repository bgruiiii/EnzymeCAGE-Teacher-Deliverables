# 新3B-S10与82路径六模型比较：统一交付

## 11月23日更新：外测与训练正样本配对审计已完成

**训练配对重叠为120/382（31.41%）、110/338（32.54%），均超过预先约定的20%。主结果改用配对排除后的228步，原338/382全量降为补充。**

[新增审计完整入口](2026-11-23_S10_External_Gold_Pair_Overlap_Audit/README.md)：RDKit反应判等、Gold配对、正样本UID membership、原S7家族占比、冻结剔除名单和六臂离线重算均已交。更保守的精确序列别名口径保留227步，也一并提供。没有重训、重新评分或改候选池；228步不再等于82条完整路径。

日期：2026年11月22日。**请先读[给师姐的完整报告](REPORT_FOR_SISTER.md)。** 本目录为酶排序器训练与外测资料，不是通用大语言模型参数测试。

报告重点：新3B用了什么数据、怎样训练、与旧五组如何比较；121→95→82的筛选条件；反应/酶资产依赖；本轮工程问题和科学证据限制。不预定新模型赢、不把82写成全部预测正确、不把所有缺口归为上游缺陷。

## 数据与结果

| 文件 | 内容 |
|---|---|
| [训练数据划分](TRAINING_SPLITS_S10.tsv) | 三split数量、反应/组数及CSV SHA |
| [新3B训练配置](TRAINING_CONFIG_NEW3B.json) | 固定蛋白特征、五seed、优化/选模规则 |
| [内部test逐seed](INTERNAL_TEST_PER_SEED_5.tsv) | 修正后实际指标、best轮次、test-open次数 |
| [内部集成与best身份](INTERNAL_ENSEMBLE_AND_BEST_IDENTITIES.json) | 内部580反应分母、五best SHA；不是338步外测 |
| [六组身份](MODEL_IDENTITY_6.tsv) | encoder/维度/原formal或S10/五seed |
| [原82路径338步全量汇总](SIX_MODEL_COMPLETE82_STEP338.tsv) | 原全量补充口径，6行；主口径见新增228步表 |
| [全382步六组汇总](SIX_MODEL_ALL382.tsv) | 补充视图，分母不可与338互抄 |
| [六组逐步结果](SIX_MODEL_STEP_RESULTS_2292.tsv) | 2292模型×步的参考rank、Hit/MRR，非原始答卷 |
| [路径级Top-k诊断汇总](PATH_TOPK_DIAGNOSTIC_6.tsv) | 一条路径每个required步骤均命中时的路径数 |
| [路径级492行明细](PATH_TOPK_DETAIL_492.tsv) | 六组×82路径，不代表湿实验成功 |
| [路径cluster配对区间](PAIRED_PATH_BOOTSTRAP_60.tsv) | 10000次，seed20261120，两视图60区间 |

## 筛选与边界

| 文件 | 内容 |
|---|---|
| [各阶段分母总表](COHORT_COUNTS.tsv) | 121/95/82路径、533/411/349原步骤与required/scored |
| [121到82逐路径去向](PATH_SCOPE_121_TO_82.tsv) | 26条参考缺口，95条中的13条required受阻 |
| [95路径411步状态](STEP_SCOPE_411.tsv) | required396、scored382、82子集338分列 |
| [14个未评分必需步骤](MISSING_REQUIRED_STEPS_14.tsv) | 6化学表示+8可消费参考资产等待，不推定全因缺3D |
| [15个政策豁免步骤](EXEMPT_STEPS_15.tsv) | 9立体-only+6运输；82中实际包含11个 |
| [资产与原因归属](ASSET_DEPENDENCIES_AND_ATTRIBUTION.md) | 方法依赖、数据/科学证据、评价规则与本轮工程责任分开 |
| [审计限制说明](AUDIT_LIMITS.md) | 成绩已核与最新CPU补件待独立复审不混同 |
| [机器审计状态](AUDIT_STATUS.json) | 验证计数、来源缺口与发布限制 |
| [来源身份](SOURCE_IDENTITIES.tsv) | 已用结果/证据的文件名、SHA与角色，无私有路径 |
| [引用和使用边界](CITATIONS_AND_REUSE.md) | 采用已核文献，不重新授予权重/数据许可 |
| [BibTeX](CITATIONS_VERIFIED.bib) | 已有引用复核结果 |
| [校验清单](SHA256SUMS) | 本目录公开文件SHA256 |

## 阅读结论

- 原全量338步Hit@10=77.51%与30/82路径诊断保留为补充；新主口径228步Hit@10=73.25%，不再称82条完整路径。
- S10有755828标记样本，不是755828个酶；训练的是下游ranker，非3B全参微调。
- 数据/训练/口袋recipe/消费者协议存在交叉变化，不能把差值单独归因于模型大小。
- 最新CPU补件只验证了归档身份，7603检查为执行方报告，未冒称全部来源已获独立无条件验收。
- 本次只整理与复算已存在结果，零模型调用、零训练、零新GPU；不含Key、完整训练数据/序列Gold、原始权重或大特征。
