# BBD full-route 污染物降解路线工具评估整理包

整理日期：2026-08-26  
用途：整理 BBD 已知降解路径测试集上 BioTransformer / enviPath / ECLIPSE 的一步产物预测、多步路线图预测、simple-path 清理，以及更严格的多步结构相似度评分结果，供黄老师/师姐快速查看。  
当前状态：GitHub teacher-facing 证据包已整理；包内不包含 restricted answer key 原始文件。

---

## 1. 最新一句话结论

这轮结果不能只用一句“哪个工具最好”概括，应该分成两层：

```text
如果看“覆盖能力”，ECLIPSE PREDEC 最强：
它最容易在多步扩展中摸到 BBD 真实下游节点。

如果看“结构精确度”，BioTransformer 最稳：
在固定每步候选数、并惩罚错误分支后，它的整体路线结构相似度最高。
```

白话解释：

```text
ECLIPSE PREDEC 更会“找得到”，但也更会“乱分支”；
BioTransformer 没那么会撒网，但生成路线更干净。
```

所以本包建议的汇报口径是：

```text
ECLIPSE PREDEC 适合做高召回候选生成主线；
BioTransformer 适合作为更保守、错误分支较少的结构参考；
enviPath BBD Rules 可解释性强，适合作为规则证据/辅助对照。
```

重要边界：

```text
当前评估限于 BBD-local 已知路径范围和 depth≤6 的 bounded 多步路线图。
不能表述为完整矿化到 CO2/H2O，也不能表述为真实环境完整降解已经被证明。
```

---

## 2. 测试集是什么

本轮使用：

```text
BBD full-route v0.3/v3.1 strict blind 输入
```

测试集规模：

```text
93 个 parent 污染物 / 外源化合物
其中 83 个兼容原 BBD83，一并加入 10 个 v0.3 candidate
```

本地评分时有 1 个 case 在 restricted answer graph 中是 zero-route-edge：

```text
FR-BBD3-CAND-c0105 Chlorobenzene
```

所以 answer-based 主评分分母是：

```text
92 个可评价 case
```

污染物类别大致包括：

```text
含卤代污染物、多环芳烃、芳香族外源污染物、农药/除草剂、
三嗪类除草剂、氨基甲酸酯类农药、有机磷农药、硝基芳香族污染物、
药物/个人护理品相关分子、塑化剂/阻燃剂/内分泌干扰物，
以及其他 EAWAG-BBD 外源化合物。
```

关键文件：

```text
00_testset_blind/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_1_BLIND_PARENT_INPUTS_FOR_PREDICTION_STRICT.csv
03_summary_tables/TESTSET_OVERVIEW_2026-08-26.csv
```

---

## 3. 盲测和答案边界

本轮执行边界：

```text
HPC/chenyu 只拿到 strict blind parent 输入；
HPC/chenyu 不读 restricted answer；
HPC/chenyu 不做答案评分；
预测结果返回后，全部在本地用 restricted answer 做审计和评分。
```

包内只包含可外发/可展示材料和聚合评分结果，不包含 restricted answer key 原始文件。

---

## 4. 一步产物预测结果

一步预测只看：

```text
污染物 parent → 第一代产物
```

主结果使用 parent-filtered 口径，即排除“把底物本身当产物”的候选。

| 工具 | Hit@1 | Hit@3 | Hit@5 | Hit@10 | 简单解释 |
|---|---:|---:|---:|---:|---|
| ECLIPSE PREDEC | 33/92 = 35.9% | 62/92 = 67.4% | 70/92 = 76.1% | 74/92 = 80.4% | 第一步预测最强 |
| BioTransformer ENVMICRO | 31/92 = 33.7% | 43/92 = 46.7% | 52/92 = 56.5% | 52/92 = 56.5% | 中等 |
| ECLIPSE NoEC | 29/92 = 31.5% | 47/92 = 51.1% | 50/92 = 54.3% | 52/92 = 56.5% | 去掉 EC 后下降 |
| enviPath BBD Rules | 24/92 = 26.1% | 42/92 = 45.7% | 45/92 = 48.9% | 45/92 = 48.9% | 可解释但偏弱 |

一句话解释：

```text
如果只问“第一步能不能猜到 BBD 里记录的真实第一代产物”，ECLIPSE PREDEC 明显最好，Top10 达到 80.4%。
```

对应文件：

```text
03_summary_tables/ONE_STEP_GENERATION1_SCORE_SUMMARY_2026-08-26.csv
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_THREE_TOOL_BLIND_PREDICTIONS_RETURN_LOCAL_AUDIT_2026-08-25.md
```

---

## 5. 多步路线图第一层结果：覆盖能力

多步预测不是只看第一步，而是把工具预测出的产物继续往下扩展，形成 bounded route graph。

本轮设置：

```text
max_depth = 6
frontier cap = 10
child cap = 10
```

这一层评分主要问：

```text
工具生成的大路线图里，有没有碰到 BBD 真实路线里的节点/边？
```

结果：

| 工具 | 第一步 case 命中 | 任意下游节点命中 | BBD-local 终点节点命中 | 精确边 case 命中 | 简单解释 |
|---|---:|---:|---:|---:|---|
| ECLIPSE PREDEC | 81/92 = 88.0% | 89/92 = 96.7% | 67/92 = 72.8% | 80/92 = 87.0% | 覆盖能力最强 |
| ECLIPSE NoEC | 70/92 = 76.1% | 80/92 = 87.0% | 52/92 = 56.5% | 62/92 = 67.4% | 无 EC 也有能力，但弱于 PREDEC |
| BioTransformer ENVMICRO | 59/92 = 64.1% | 71/92 = 77.2% | 44/92 = 47.8% | 60/92 = 65.2% | 多步后能找到更多下游节点 |
| enviPath BBD Rules | 53/92 = 57.6% | 62/92 = 67.4% | 30/92 = 32.6% | 52/92 = 56.5% | 规则法覆盖偏弱 |

这一层说明：

```text
ECLIPSE PREDEC 很容易在多步扩展中摸到真实路线里的下游产物。
```

但这一层也有局限：

```text
如果工具每一步都生成很多候选，路线图会变大；
图越大，越容易“碰巧包含答案”。
所以这层结果适合说明覆盖能力，不适合单独说明路线结构预测质量。
```

对应文件：

```text
03_summary_tables/MULTISTEP_GRAPH_LOCAL_SCORE_SUMMARY_2026-08-26.csv
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_BOUNDED_MULTISTEP_ROUTE_EXPANSION_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-26.md
```

---

## 6. 多步路线图第二层结果：更严格的结构相似度

为了避免“大图撒网导致结果虚高”，我们补做了更严格的多步结构评分。

参考思想来自 enviFormer / multi-generation pathway evaluation：

```text
不能只看单步 Top1，也不能只看大图里有没有碰到答案；
应该比较整张预测路线图和真实路线图的结构重合，
并惩罚多预测出来的错误分支。
```

但我们没有直接照搬 enviFormer 原版概率评分，因为三个工具的分数不是同一种概率：

```text
ECLIPSE 有模型分数；
BioTransformer 没有可比较概率；
enviPath BBD Rules 是规则命中，也不是可比较概率。
```

所以本轮采用固定分支预算：

```text
K=1：每一步只保留第 1 个候选继续走，最严格。
K=3：每一步保留前 3 个候选继续走。
K=5：每一步保留前 5 个候选继续走。
K=10：宽松补充，不作为主结论。
```

结构相似度的直白公式：

```text
路线结构相似度 =
预测对的部分 / (预测对的部分 + 漏掉的真实部分 + 多预测的错误部分)
```

也就是：

```text
Jaccard = TP / (TP + FP + FN)
```

其中：

```text
TP：预测对了的真实路线节点
FP：工具多预测出来、真实路线里没有的节点
FN：真实路线里有、工具漏掉的节点
```

并且前几步权重更大：

```text
第 1 步权重 1/2；
第 2 步权重 1/4；
第 3 步权重 1/8；
越往后权重越小；
起始污染物本身不计分。
```

主表使用 all-92 inclusive macro：

```text
92 个可评分 case 全部入分母；
NO_PREDICTION case 按 0 分保留。
```

结果：

| 工具 | K=1 结构相似度 | K=3 结构相似度 | K=5 结构相似度 | 简单解释 |
|---|---:|---:|---:|---|
| BioTransformer ENVMICRO | 0.197 | 0.154 | 0.152 | 综合结构最干净 |
| enviPath BBD Rules | 0.116 | 0.136 | 0.140 | 规则法中等偏弱 |
| ECLIPSE PREDEC | 0.178 | 0.106 | 0.070 | 覆盖高，但错误分支多 |
| ECLIPSE NoEC | 0.155 | 0.100 | 0.065 | 不带 EC 后整体弱一些 |

正确解释：

```text
BioTransformer K=1 的 0.197 不是“19.7% 的污染物完全预测对”，
而是 92 个污染物的路线图平均加权重合程度约为 19.7%。

BioTransformer K=1 下，只有 1/92 个 case 达到完全结构匹配：
Cyclohexane。
```

这一层结论：

```text
BioTransformer 在 K=1/3/5 的综合结构相似度最高；
ECLIPSE PREDEC 的 recall 最高，说明它最容易覆盖真实节点；
但 PREDEC 随 K 增大产生大量错误分支，precision/Jaccard 明显下降。
```

对应文件：

```text
07_enviformer_style_mg_structural_at_k/README.md
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_REPORTING_SUPPLEMENT_2026-08-26.md
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_MG_STRUCTURAL_AT_K_ALL92_SUPPLEMENT_CODEX_FINAL_AUDIT_2026-08-26.md
```

---

## 7. simple-path 路径层是否修好了

第一次多步包里，ECLIPSE 的 `PREDICTED_ROUTE_PATHS` 有很多重复节点/重复边，所以不能直接当成干净路线展示。

后面做了两次修复：

```text
repair v1：清掉重复节点/重复边。
repair v2：再删除 root-only zero-edge 占位 path，并修正 coverage summary。
```

v2 审计结论：

```text
PASS
PASS_FOR_TEACHER_FACING_PATH_LAYER
```

v2 清理后：

| 工具 | 保留 simple path 行数 | 删除零边占位行 | 有非空 simple path 的 case |
|---|---:|---:|---:|
| BioTransformer ENVMICRO | 779 | 8 | 85/93 |
| enviPath BBD Rules | 745 | 5 | 88/93 |
| ECLIPSE PREDEC | 930 | 0 | 93/93 |
| ECLIPSE NoEC | 930 | 0 | 93/93 |

所有保留路径均满足：

```text
path_depth >= 1
edge_id_path 非空
无重复 node
无重复 SMILES
无重复 edge
无 parent-copy / self-loop 占位路径
每个 case 最多 10 条路径
```

对应文件：

```text
03_summary_tables/SIMPLE_PATH_V2_COVERAGE_SUMMARY_2026-08-26.csv
04_path_layer_v2_summary/
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_V2_CLEANUP_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-26.md
```

---

## 8. EC 条件有没有用

有用。

ECLIPSE PREDEC 明显优于 ECLIPSE NoEC：

```text
一步 Top10：
PREDEC 74/92 = 80.4%
NoEC   52/92 = 56.5%

多步任意下游节点：
PREDEC 89/92 = 96.7%
NoEC   80/92 = 87.0%

多步 BBD-local 终点节点：
PREDEC 67/92 = 72.8%
NoEC   52/92 = 56.5%
```

所以可以比较稳地说：

```text
给模型提供 EC 条件，对污染物降解产物/路线候选生成是有帮助的。
```

---

## 9. 这次结果不能怎么说

不要这样表述：

```text
已经预测出了完整矿化路线。
已经预测到 CO2/H2O。
已经证明真实环境里一定这样降解。
ECLIPSE 完全不行。
BioTransformer 能完整预测大多数污染物路线。
```

推荐这样表述：

```text
这次是在 BBD 已知路径范围内，做 depth≤6 的多步路线预测和结构评分。
ECLIPSE PREDEC 覆盖真实下游产物能力最强；
BioTransformer 在惩罚错误分支后的综合结构相似度最高；
EC 条件对 ECLIPSE 有明显帮助；
但完整路线拓扑和终点矿化仍需要后续继续验证。
```

---

## 10. 当前限制

### 10.1 不是完整矿化

很多 BBD 路线走到：

```text
邻苯二酚、丙酮酸、乙酰辅酶A、乙醛酸、苯甲酸、琥珀酸、草酰乙酸等
```

就停了。

这通常表示污染物已经进入更常见的代谢网络，但不等于数据库继续记录到 CO2/H2O。

### 10.2 只评价 depth≤6

本轮预测图最多生成到：

```text
depth = 6
```

有 15 个真实 BBD route 的最大深度超过 6，所以这些 case 只评价 depth≤6 内的结构恢复。

### 10.3 结构评分不是原版 enviFormer 概率评分

本轮结构评分借鉴了 enviFormer 多步评价思想，但不是 official probability-threshold Multi-Generation / AUPRC。

原因是不同工具的分数不能直接当作同一种概率比较。

---

## 11. 包内文件夹说明

```text
00_testset_blind/
```

盲测输入，只含 parent 信息，不含答案。

```text
01_hpc_return_identities/
```

HPC 返回包 identity sidecar，用于证明每次返回包身份。

```text
02_local_audits/
```

本地审计报告。已包含 strict blind、一步预测、多步扩展、simple-path v2、MG-Structural@K、all-92 supplement 和 Codex final audit。

```text
03_summary_tables/
```

一步预测、多步覆盖、simple-path 和测试集概况汇总表。

```text
04_path_layer_v2_summary/
```

v2 simple-path 清理结果。包含 corrected coverage、重复检查、删除零边占位行清单等。

```text
05_hpc_prompts/
```

发给 chenyu 的执行提示词，记录执行边界和要求。

```text
06_return_archives/
```

非 restricted 的 HPC 返回 tar.gz 原包，便于复核。

```text
07_enviformer_style_mg_structural_at_k/
```

更严格的多步结构评分补充。推荐优先看：

```text
07_enviformer_style_mg_structural_at_k/README.md
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv
```

```text
SISTER_READABLE_BBD_FULL_ROUTE_MULTISTEP_PREDICTION_REPORT_2026-08-26.md
```

给师姐/线下讨论看的中文说明版，尽量用白话解释整个流程和结果。

```text
PACKAGE_COMPLETENESS_CHECK_2026-08-26.md
```

上传前包完整性检查，说明本包已经包含哪些证据层、哪些审计、推荐阅读顺序，以及不能过度表述的边界。

---

## 12. 建议给老师的汇报口径

可以这样说：

```text
黄老师您好，我们把原 BBD83 的第一步产物测试扩展成了 BBD full-route v0.3/v3.1 的 93 个 parent 盲测集合，并比较了 BioTransformer、enviPath BBD Rules、ECLIPSE PREDEC/NoEC 的一步产物预测和 bounded 多步路线图预测。

结果分两层：如果看覆盖能力，ECLIPSE PREDEC 最强，一步产物 Top10 为 74/92 = 80.4%，多步任意下游节点 case hit 为 89/92 = 96.7%，BBD-local 终点节点 case hit 为 67/92 = 72.8%。对比 NoEC 版本，EC 条件明显提升预测效果。

同时我们补做了更严格的多步结构相似度评分：92 个可评分 case 全部入分母，NO_PREDICTION 按 0 分保留，并惩罚错误分支。该口径下 BioTransformer 的 K=1/3/5 综合结构相似度最高；ECLIPSE PREDEC 的 recall 最高但 precision/Jaccard 随 K 增大明显下降，说明其优势更多体现在候选覆盖而非干净拓扑复原。

目前 simple-path 层已完成 v2 清理审计，保留路径均为非空 simple path，无重复节点/SMILES/edge，也没有 parent-copy/self-loop 占位路径。

需要说明的是，目前结论仍限于 BBD-local 已知路径范围和 depth≤6 的 bounded predicted route graph，不声明完整矿化或真实环境完整降解。后续如果老师认可，可以继续做中心代谢图承接或外部非 BBD 路线验证。
```

---

## 13. 后续建议

当前这个包已经足够支撑一次阶段汇报。后续建议不是继续在同一批 BBD 结果上反复榨指标，而是进入两个更有价值的方向：

```text
1. 中心代谢图承接：
   把 BBD-local 路线断点继续接到公共中心代谢网络，
   但需要单独定义边界，不能混同于本轮 BBD-local 评价。

2. 外部非 BBD 路线验证：
   构建高质量、非 BBD 来源的小型完整路线测试集，
   检验 ECLIPSE PREDEC / BioTransformer / enviPath 的泛化能力。
```
