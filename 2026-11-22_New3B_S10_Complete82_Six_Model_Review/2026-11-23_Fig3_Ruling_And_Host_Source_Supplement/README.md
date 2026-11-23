# 图3裁定与酶/宿主线追加请求：完整补件

2026-11-23。**R1已独立复审通过，按A–E一次集中交付。** 图3数值前轮已独立复算，本轮未重算；字段修正16项检查通过。

先读[给师姐的统一反馈](REPLY_TO_SISTER_UNIFIED.md)。

| 需要的内容 | 本目录入口 |
|---|---|
| A：V6名单剔除掩码与保留数 | [掩码](approved_numeric/SIXTH_RULE_MASKS.json)、[12步匹配清单](approved_numeric/V6_MATCHED_REACTIONS_12.tsv)；原382/338保留370/326，主228不变 |
| B：应使用哪列判断来源物种 | [7468行派生表](UID_SPECIES_TRACE_7468_R1.tsv)、[精确字段定义](SPECIES_FIELD_DICTIONARY_AND_JOIN_PROTOCOL_R1.tsv)；采用identified_microbe_source_for_followup，5579是候选UID数 |
| C：是否接线、授权和排期 | [统一反馈C](REPLY_TO_SISTER_UNIFIED.md#c-接线与排期措辞收口)；隔离接入分支由黄老师授权，接口/资源齐备后约2工作日为估计，未开始接线或部署 |
| D：逐步导出的字段与已有能力 | [三轴映射](CASE_EXPORT_PROTOCOL_FIELDS_R1.tsv)、[运行设计契约](CASE_EXPORT_RUN_CONTRACT_R1.json)、[SCHEMA_ONLY示例](CASE_EXPORT_EXAMPLE_SCHEMA_ONLY_R1.json) |
| E：原数值限制确认 | [统一反馈E](REPLY_TO_SISTER_UNIFIED.md#e-逐臂数值限制定稿确认)、[Q66Q78确认](LIMITATIONS_CONFIRMATION_Q66Q78_R1.json) |
| 图3a/3b：旧3B基准差值及绝对区间 | [差值森林数据](approved_numeric/FIG3A_OLD3B_REFERENCE_PAIRED_CI.tsv)、[绝对性能数据](approved_numeric/FIG3B_ABSOLUTE_PERFORMANCE_CI.tsv)；228/262分列，路径cluster、10000次 |

**B的三层不能互换：** 来源记录可追7430 UID、范围已接受5607 UID、两者相交5601 UID；其中22 UID为Unknown/uncultured来源标签，单列后5579 UID符合后续来源证据工作定义。以上都不是独立物种数，不证明可培养、可购买或整链功能。候选排序表按科学UID与序列SHA连接该列后，师姐自行计算每步Top-k覆盖率。

`approved_numeric/NONGOLD_SPECIES_COVERAGE_*.tsv`仅为旧版广义来源追溯对照，包含非微生物与占位来源，**不要用作最终判定B覆盖率**。原始值保留；分母表、前五规则、覆盖率等由师姐接手，本轮不重复计算。

D所列run_id、Gold annotation与R1派生字段接入为导出层契约，不代表新代码已接main。真实完整案例还依赖C；两个不同路径的R4评分步不能拼成同一整链。当前在线配置继续标未获维护者书面确认。

[独立采用报告](evidence/R1_ADOPTION_REPORT.md) · [机器复核](evidence/R1_INDEPENDENT_CHECKS.json) · [数值与附录来源](APPROVED_ARTIFACTS_REGISTER.tsv) · [文件清单](MANIFEST.tsv)
