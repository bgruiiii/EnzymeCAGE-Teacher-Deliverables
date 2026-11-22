# 酶与微生物线：师姐问题逐项答复与数据/工具

2026-11-22完整交付。**原始数据、方法、性状库、工具、关键复审与两份反馈集中在本目录。** 本目录内即可读答复、下载表格、查看代码与关键验证，无需跳回项目的其它本地目录。

发布前已对照[师姐原任务书逐项核对](docs/TASK_COMPLETION_REVIEW.md)。陌生微生物先查现有库，仍缺再按需预测的[实际脚本与环境入口](tools/TRAIT_QUERY_AND_PREDICTION.md)已集中提供。

| 师姐的问题 | 已完成什么 | 从哪里看 |
|---|---|---|
| C1 用了哪组模型、真跑过吗 | 历史3B-v1五seed装载与真实运行已核；当前在线装载未确认 | [模型与方法](docs/MODELS_AND_METHODS.md) |
| C2 原始成绩在哪里，能否复算 | 三张原始表及主要汇总可复算，原数值限制保留 | [原始成绩与复算说明](docs/RESULTS_AND_LIMITS.md)、[数据目录](data/ranking/) |
| B1 排序酶与菌证据如何接起来 | 7468UID逐条来源表、旧412对应、现有性状记录覆盖已整理 | [微生物对应说明](docs/MICROBES_AND_TRAITS.md)、[逐UID表](data/hosts/MICROBE_UID_EVIDENCE_FOR_PAPER_7468.tsv.gz) |
| A1 性状有没有做、如何使用 | 总库2478来源；已有查询和412来源预测，先查本地库，仍缺再按需独立预测 | [性状库与用法](docs/MICROBES_AND_TRAITS.md)、[库与来源索引](data/traits/) |
| A2 候选酶怎么召回 | 指定集成B优先/C兜底与Top10方法分层说明，未做通道消融 | [模型与方法](docs/MODELS_AND_METHODS.md) |
| A3 拆步、串联、缺资产怎么办 | R4复用既有资产，S02=13/13、S03=31/31全候选真实评分；真缺件补建工具独立按需 | [工具及接入状态](docs/TOOLS_AND_MAIN_INTEGRATION.md)、[代码](tools/) |
| C3 参考关联、模型身份、引用 | 阶段账本、身份与引用已整理；非关键历史留存项备注 | [模型与方法](docs/MODELS_AND_METHODS.md)、[参考文献](references/) |
| D/E 湿实验与消融 | 湿实验立项前冻结名单；通道消融按原任务不立项 | [任务状态](docs/TASK_STATUS.md) |

**[给师姐的完整反馈](docs/REPLY_TO_SISTER.md)**；**给黄老师的工程反馈另列：[问题、已备工具与main接入决定](maintainer/REPLY_TO_HUANG.md)。** 我们提供独立工具、库和验证依据，没有权限也没有擅自修改depending main，是否采用/合并/部署由黄老师决定。

读数要点：7468是酶UID，2478和412是不同范围的来源记录；642只是旧412与当前候选的交集。来源登记、性状观测、模型预测、酶分数和菌株功能验证各有含义，不互相代替。

[包内检查](PACKAGE_CHECKS.json)与[逐文件来源](provenance/SOURCES.tsv)用于定位资料；文件完整性通过不等于全部工程或科学问题清零。[发布状态](PUBLICATION_STATUS.json)明确当前是否上传。重型模型权重/外部原数据库不重复放入本包，运行依赖与资产根由工具配置提供。
