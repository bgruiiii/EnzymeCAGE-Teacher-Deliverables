# Method note — MG-Structural@K adapted evaluation for BBD full-route

协议名：`ENVIFORMER_MG_STRUCTURAL_AT_K_ADAPTED_BBD_FULL_ROUTE`
日期：2026-08-26

---

## 1. 协议定位与边界

本评价是 **enviFormer Multi-Generation 的结构化适配版**，灵感来自 Brydon et al. (2025) 与 Aukema et al. (2021) 的 pathway 级加权评价，但做了以下关键简化/适配：

| 维度 | enviFormer official | 本适配版 |
|---|---|---|
| 分支保留 | beam=5 + 累积概率阈值剪枝 | 固定每步 TopK（K=1/3/5/10） |
| 概率 | LogSoftmax log-probability，阈值扫描 | 不使用概率阈值；rank 字段为权威排序 |
| 输出 | PR curve + AUPRC | weighted Precision / Recall / Jaccard（无 AUPRC） |
| 跨工具 | 同模型概率可比 | BioTransformer/enviPath/ECLIPSE 概率尺度不同，故用固定 candidate budget |

**不声称**：official enviFormer MG、probability-based MG AUPRC、calibrated probability comparison、complete mineralization、biologically confirmed full degradation。

**允许声称**：fixed-budget, graph-structural, enviFormer-style adapted MG evaluation: MG-Structural@1 / @3 / @5 / optional @10。

## 2. 输入

### 2.1 Restricted answer graph（本地评分资产，不进 teacher-facing 文件夹）

- `BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_REACTION_EDGES.csv`（710 条 scoreable 边）
- `BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_COMPOUND_NODES.csv`
- `BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_PARENT_ROUTE_SUMMARY.csv`（93 case）
- `BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_ROUTE_PATHS_PARENT_TO_TERMINAL.csv`

### 2.2 预测输出

- 主预测包：`bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz`
  - sha256 = `ee8e06fffe76bec29825702c18deb1211e33b7c4609ff3132be8428179fe83cf`
- QC 参考：`bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_v2_cleanup_supplement_20260826.tar.gz`
  - sha256 = `13107f9fa6b376327e817b64373bd58e6c0db635dc563de848c156dd49e6a592`
- 使用每个工具的 `PREDICTED_ROUTE_EDGES.jsonl`：
  - `biotransformer_envmicro_multistep`（tool_id = biotransformer_envmicro，no_score）
  - `envipath_bbd_rules_multistep`（tool_id = envipath_prediction，multi_generation_edge_probability）
  - `eclipse_predec_bbd_finetuned_10fold_multistep`（tool_id = eclipse_predec，log-likelihood）
  - `eclipse_noec_bbd_finetuned_10fold_multistep_optional`（optional，partial depth 4）

## 3. 标准化

- 主评分 key：**non-isomeric RDKit canonical SMILES**（`Chem.MolToSmiles(mol, isomericSmiles=False)`）。
- 选择理由：BBD 答案常不指定立体化学，而 ECLIPSE 可能输出立体特异产物；非同构匹配是之前 local audit 的稳健主比较 key。
- canonicalization_mode = `non_isomeric_rdkit_canonical`
- rdkit_available = true
- invalid_reference_smiles_count = 0
- invalid_prediction_row_count：按工具分别记录（biotransformer 565；其余 0）。

## 4. 评分范围

- 93 total parent cases
- 92 evaluable route cases
- 1 excluded zero-route-edge case：`FR-BBD3-CAND-c0105`（Chlorobenzene，route_edge_count=0）

## 5. 真实图构造

对每个 `full_route_case_id`：
1. 从 parent_route_summary 取 `parent_canonical_smiles` 作为 root（重新非同构标准化）。
2. 取该 case 的 `source_pathway_abbrs`（可能多个，pipe 分隔）。
3. 收集这些 pathway 的所有 `scoreable_by_structure == true` 反应边，构作有向图 `source_canonical → target_canonical`。
4. BFS 从 root 计算 shortest directed depth。
5. root 不计分；不可达真实节点记录在 QC 并排除出该 case 的 scoring denominator。

注意：少数 pathway_abbr（ctc / caa / cpr）被多个 case 共享；每个 case 的真实图只取从自身 root 可达的子图，因此共享 pathway 不会串分。

## 6. 预测图构造（每工具 × 每 case × 每 K）

1. 只保留 `normalization_status == ok` 的预测边。
2. 移除 parent-copy / self-loop 行：`target_is_original_parent_copy`、`target_is_source_copy`、`source == target`。
3. 对 source/target 做非同构标准化。
4. 按 `(full_route_case_id, tool_id, source_key)` 分组出边。
5. 组内排序：
   - `edge_rank_from_source` 升序（权威）
   - `edge_rank_global_within_case_depth` 升序（权威）
   - `local_edge_score_raw` 降序（仅 tie-breaker；对 ECLIPSE log-likelihood，数值大者更好）
   - 注：`edge_rank_from_source == -1` 视为未排序，映射为大值排末尾。
6. 每个 source 只保留 TopK 个 **unique target** 节点。
7. 从 root 出发 BFS 遍历保留边，到 max_depth = 6。
8. 防无限循环：BFS visited 集合；不展开自环；单 case 节点上限 1000，命中则报告 cap_hit。

## 7. CO2 策略

- `exclude_CO2_from_main_node_scoring = true`
- 构图阶段即跳过 target == CO2（`O=C=O`）的边，CO2 不进入真实图也不进入预测图。
- 真实图中有 10 条以 CO2 为 target 的边，均被排除。

## 8. 深度加权

- `weight(depth) = 1 / 2^depth`
- root depth=0 不计分（weight=0）。
- TP 用 **真实深度** 权重；FN 用 **真实深度** 权重；FP 用 **预测深度** 权重。

## 9. 中间体（intermediate metabolite）处理

- `intermediate_handling = true`（基础版实现）
- 识别条件：预测节点 X 不在真实图中，且存在真实边 U→V，U 与 V 同时在真实图与预测图中，且 X 位于预测图中 U→V 最短路径的内部节点上。
- 中间体 weight = 0，不计为 FP。
- `downstream_depth_correction = false`：未实现 downstream 节点深度因中间体而校正的完整逻辑（已在 validation report 与 audit 中标注此限制，不冒充完整 official intermediate 行为）。
- 中间体逐条明细见 `MG_STRUCTURAL_AT_K_INTERMEDIATE_NODES_2026-08-26.csv`。

## 10. 指标公式

对每条 pathway（case）：
```
weighted_precision = weighted_tp / (weighted_tp + weighted_fp)   # 分母 0 → 0
weighted_recall    = weighted_tp / (weighted_tp + weighted_fn)    # 分母 0 → 0
weighted_jaccard   = weighted_tp / (weighted_tp + weighted_fp + weighted_fn)  # 分母 0 → 0
```
- macro：对 scored case 的指标做算术平均。
- micro：先汇总所有 case 的 weighted_tp/fp/fn，再算指标（作补充，不与 official 数值混用）。

## 11. Toy tests（真实评分前强制通过）

| # | 场景 | 期望 | 结果 |
|---|---|---|---|
| 1 | 精确链 A→B→C | P=R=J=1 | PASS |
| 2 | 多一个 FP A→X | P=0.5 R=1 J=0.5 | PASS |
| 3 | 缺下游 A→B（真 A→B→C） | P=1 R=2/3 J=2/3 | PASS |
| 4 | root 不计分 | root 不在 nodes、TP=0.5 | PASS |
| 5 | 深度加权：depth1 FP 比 depth3 FP 惩罚更重 | P_depth3fp > P_depth1fp | PASS |
| 6 | 中间体 A→X→B（真 A→B） | X 零权重、不计 FP、P=R=J=1 | PASS |

全部 PASS 后才进行真实评分。

## 12. 主要参数一览

```
protocol_name        = ENVIFORMER_MG_STRUCTURAL_AT_K_ADAPTED_BBD_FULL_ROUTE
K_values             = 1, 3, 5, 10   (主结论聚焦 1/3/5；10 为 wider exploratory)
max_depth            = 6
max_pred_nodes/case  = 1000
canonicalization     = non_isomeric_rdkit_canonical
exclude_co2          = true
intermediate_handling= true (基础版)
downstream_depth_correction = false
depth_weight         = 1 / 2^depth
root_excluded        = true
aggregation          = all92_inclusive_macro (主表) + scored_only_macro (补充)
```

## 12b. 聚合层级：all-92 主表 vs scored-only 补充

本评价产出两套工具级汇总：

| 汇总表 | 文件 | 分母 | 用途 |
|---|---|---|---|
| **all-92 inclusive macro/micro** | `MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv` | 全部 92 个 evaluable case；NO_PREDICTION 按 0 分保留 | **teacher-facing 主表** |
| scored-only macro/micro | `MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv` | 只在有预测的 SCORED case 上平均 | coverage-conditional 补充 |

选择 all-92 作为主表的原因：scored-only 会让有 NO_PREDICTION case 的工具（BioTransformer 8 个、enviPath 5 个）分数偏乐观。all-92 把这些工具的未覆盖 case 按 0 分保留在分母中，使跨工具比较更公平。

两套表的 NO_PREDICTION case 行均为零分（weighted_tp=fp=precision=recall=jaccard=0, weighted_fn>0），仅分母处理方式不同。

## 13. 已知限制

1. **bounded depth≤6 scoring（重要限制）**：真实图在与返回的 bounded 预测图相同的 depth 窗口内评分。15 个 evaluable BBD route 的最大深度超过 6（最深 13），因此本补充不应描述为对每条 route 的全深度终点路线恢复。这不影响结果有效性，因为预测生成本身也 bounded 到 depth 6，但必须描述为 bounded-depth 结构评价。
   - 超过 depth 6 的 15 个 case：Gallate(9), Benzoate(13), 2,4-D(8), p-Cymene(8), Fluorene(7), Bromoxynil(7), Limonene(7), 2,4-Dichlorotoluene(7), Cyclohexane(10), Citronellol(12), Isooctane(13), Isoniazid(7), Asulam(7), Malathion(7), gamma-HCH(7)。
2. 非同构匹配会令 cis/trans 异构体（如 cpr / caa 两条 case）映射到同一 key，其真实图与评分在非同构层等价——这是稳健主比较的已知取舍，与之前 local audit 一致。
3. downstream depth correction 未实现，FP 深度可能略偏高，但对跨工具相对排序影响小。
4. 无概率阈值 / 无 AUPRC：本协议不产生 PR curve，故不能替代 enviFormer official probability-based MG。
5. ECLIPSE NoEC 为 optional 且原始生成为 partial depth 4，K 宽放后 recall 上限受此约束。
