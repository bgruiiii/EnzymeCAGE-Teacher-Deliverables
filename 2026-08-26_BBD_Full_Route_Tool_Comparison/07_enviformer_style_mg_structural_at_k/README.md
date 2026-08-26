# MG-Structural@K — enviFormer-style adapted structural evaluation for BBD full-route

协议名：`ENVIFORMER_MG_STRUCTURAL_AT_K_ADAPTED_BBD_FULL_ROUTE`
日期：2026-08-26
评价范围：BBD full-route v0.3 / v3.1，93 个 parent case，92 个可评分 case（排除 `FR-BBD3-CAND-c0105` Chlorobenzene 零边 case）

---

## 1. 为什么要做这个补充

之前的 bounded-multistep "大图 coverage" 诊断偏宽松：它只统计"真实产物节点是否在某处被预测到"，不惩罚错误分支。
ECLIPSE PREDEC 生成了约 29,530 条预测边（含大量自环 / 重复 / 见过即标记），天然覆盖率高，看起来最强，
但这种"强"很大程度上是图变大带来的，而不是路径结构恢复质量高。

本次补充加入 **FP 惩罚**：每个工具在同样的每步 Top-K 分支预算下递归构图，再用深度加权 Precision / Recall / Jaccard 比较，
这样"乱分支"会拉低 Precision，使评价更科学。

## 2. 这次评价是什么

- 给每个工具同样的分支预算：每个 source node 每一步最多保留 TopK 个候选（K = 1, 3, 5；补充 K = 10）。
- 从 parent/root 出发，递归展开预测 route graph 到 max_depth = 6。
- 与 BBD restricted answer graph 做 **weighted structural comparison**：
  - 深度权重 `weight(depth) = 1 / 2^depth`（depth 1 = 0.5, depth 2 = 0.25, …；root 不计分）。
  - TP 用真实深度权重，FN 用真实深度权重，FP 用预测深度权重。
  - 中间体（intermediate metabolite）识别：预测中位于两个真实节点之间的、真实图中不存在的节点，零权重、不计 FP。
- 指标：weighted Precision / Recall / Jaccard，以及 macro（按 case 平均）与 micro（按节点汇总）两套。

## 3. 这次评价不是什么

- **不是** enviFormer official probability-threshold Multi-Generation / AUPRC。
- **不比较**跨工具的校准概率（BioTransformer 无概率、enviPath 是规则概率、ECLIPSE 是 log-likelihood，尺度不可直接比）。
- 因此跨工具比较用固定 candidate budget（TopK），而不是概率阈值。
- **不是**所有 BBD case 的全深度终点矿化评分：评价范围为 bounded depth≤6 route graph，因为预测图本身生成到 depth 6。15 个真实 BBD route 的最大深度超过 6，这些 case 只评价 depth≤6 内的结构恢复。

## 4. 主跨工具比较表（all-92 inclusive macro — 推荐主表）

**主表**：`MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv`
92 个可评分 case 全部入分母，NO_PREDICTION 按 0 分保留。

| tool | K | all-92 macro P | all-92 macro R | all-92 macro J | n_scored |
|---|---:|---:|---:|---:|---:|
| biotransformer_envmicro | 1 | 0.329 | 0.242 | **0.197** | 84 |
| biotransformer_envmicro | 3 | 0.203 | 0.396 | **0.154** | 84 |
| biotransformer_envmicro | 5 | 0.195 | 0.467 | **0.152** | 84 |
| envipath_prediction | 1 | 0.257 | 0.133 | 0.116 | 87 |
| envipath_prediction | 3 | 0.208 | 0.327 | 0.136 | 87 |
| envipath_prediction | 5 | 0.197 | 0.384 | 0.140 | 87 |
| eclipse_predec | 1 | 0.315 | 0.220 | 0.178 | 92 |
| eclipse_predec | 3 | 0.122 | 0.510 | 0.106 | 92 |
| eclipse_predec | 5 | 0.074 | 0.645 | 0.070 | 92 |
| eclipse_noec *(optional)* | 1 | 0.278 | 0.188 | 0.155 | 92 |
| eclipse_noec *(optional)* | 5 | 0.069 | 0.512 | 0.065 | 92 |

原 scored-only / coverage-conditional 补充表保留为：`MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv`（只在 SCORED case 上平均，偏乐观，不作主表）。

其他文件：
- 每 case × tool × K 明细：[`MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv`](MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv)
- 报告补充说明：[`MG_STRUCTURAL_AT_K_REPORTING_SUPPLEMENT_2026-08-26.md`](MG_STRUCTURAL_AT_K_REPORTING_SUPPLEMENT_2026-08-26.md)
- 方法说明：[`MG_STRUCTURAL_AT_K_METHOD_NOTE_2026-08-26.md`](MG_STRUCTURAL_AT_K_METHOD_NOTE_2026-08-26.md)
- QC：[`MG_STRUCTURAL_AT_K_QC_SUMMARY_2026-08-26.csv`](MG_STRUCTURAL_AT_K_QC_SUMMARY_2026-08-26.csv)
- Top/Bottom case：[`MG_STRUCTURAL_AT_K_TOP_BOTTOM_CASES_2026-08-26.csv`](MG_STRUCTURAL_AT_K_TOP_BOTTOM_CASES_2026-08-26.csv)
- 中间体明细：[`MG_STRUCTURAL_AT_K_INTERMEDIATE_NODES_2026-08-26.csv`](MG_STRUCTURAL_AT_K_INTERMEDIATE_NODES_2026-08-26.csv)
- 验证报告：[`MG_STRUCTURAL_AT_K_VALIDATION_REPORT.json`](MG_STRUCTURAL_AT_K_VALIDATION_REPORT.json)

## 5. 如何解释

- **Precision 低** → 乱分支多（生成的 FP 节点多）。ECLIPSE PREDEC 在 K=5 时 all-92 precision 仅 0.074，说明它虽覆盖广，但大量分支是错的。
- **Recall 高** → 覆盖真实路线多。ECLIPSE PREDEC @5 recall 0.645 最高，但代价是 precision 崩塌。
- **Jaccard** → 整体重合度（TP / (TP+FP+FN)），综合衡量"既不漏也不乱"。

一句话结论：在固定 TopK 分支预算下，**BioTransformer 在 all-92 的 MG-Structural@1/@3/@5 综合 Jaccard 最高**；
ECLIPSE PREDEC 的 recall 最高，说明它最容易覆盖到真实节点；
但 PREDEC 随 K 增大产生大量 FP 分支，precision/Jaccard 明显下降；
因此这次更科学的结论不是"谁撒网最大"，而是区分"覆盖能力"和"结构精确度"。

## 6. bounded depth≤6 限制

评价范围为 bounded depth≤6 route graph，因为预测图本身生成到 depth 6。15 个真实 BBD route 的最大深度超过 6（最深 13），这些 case 只评价 depth≤6 内的结构恢复，不应描述为全深度终点路线恢复。详见方法说明 §13。

## 7. 可复现脚本

[`scripts/score_mg_structural_at_k.py`](scripts/score_mg_structural_at_k.py)
（已修复 stale tmp extraction 问题：每次运行使用 `tempfile.mkdtemp` 全新解压目录）
