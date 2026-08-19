# 污染物转化产物预测路线阶段性评估报告

日期：2026-08-19  
范围：污染物一代转化产物预测 / 已知路径检索路线评估  
不包含：微生物性状 MetaTraits/BacDive 专题；酶侧 M4 acceptance；生产 D4 写入。

## 1. 一句话结论

当前最稳妥的路线不是“单一模型替代所有工具”，而是分层使用：

```text
已知 parent/pathway 在 enviPath 中存在
→ 优先用 enviPath 本地快照做已知路径检索

未知 parent 需要 blind prediction
→ 当前以 BioTransformer ENVMICRO 作为主预测基线

ECLIPSE PREDEC
→ 作为补充候选生成器 / 后续改进对象，而不是现在替代 BioTransformer
```

这个结论来自三类证据：

1. BBD83 已知污染物路径集上的多工具比较；
2. BBD-finetuned ECLIPSE 在 BBD83 上的 all-fold / OOF 审计；
3. Soil/Sludge 转移评估和 enviPath 本地快照 lookup 补充审计。

## 2. 为什么要做这轮评估

我们前期已经有 83 个 BBD/enviPath-lineage 的污染物母体，以及 148 条可接受的一代转化产物标签。这个测试集适合比较不同工具的“一步转化产物预测能力”，但它也有明显边界：它和 BBD/enviPath 数据源关系很近，不能单独支撑“泛化到所有非 BBD 文献污染物”的结论。

因此后续又做了两步：

1. 对 ECLIPSE 做 BBD fine-tune，并检查 EC 条件是否有帮助；
2. 用 enviPath Soil/Sludge 数据做一个跨数据集转移测试，看 BBD-only ECLIPSE、BioTransformer 和 enviPath lookup 各自能做什么。

## 3. 三条主要路线分别是什么

### 3.1 BioTransformer ENVMICRO

BioTransformer 是当前最稳定的 blind prediction 基线。它不依赖我们的训练，也不需要答案表作为输入。对未知底物，它可以直接给出环境微生物转化候选。

它的优势是：

- 在 BBD83 上整体最好；
- 在 Soil/Sludge 转移集上 Hit@3/5/10 仍然最好；
- 不会大量输出 unchanged parent 作为候选。

它的限制是：

- 对某些 parent 会 empty/error；
- 规则覆盖不到的化学空间仍会漏；
- 它不是数据库查询，因此不能保证已知路径全部找回。

### 3.2 Chem-ECLIPSE / ECLIPSE product model

这里的 ECLIPSE 有两个口径：

```text
ECLIPSE NoEC:
  底物 SMILES → product model → 产物
  不提供 EC 条件。

ECLIPSE PREDEC:
  底物 SMILES → 先预测 EC → 带 EC 条件的 product model → 产物
```

注意：ECLIPSE NoEC 不是 enviFormer。它只是 Chem-ECLIPSE product model 的无 EC baseline；enviFormer 是另一套外部模型。

本轮结果显示：

- 初始 ECMap/USPTO 配置在 BBD83 上很弱；
- BBD fine-tune 后，PREDEC 明显优于 NoEC；
- 但在保守 OOF 和 Soil/Sludge 转移测试里，PREDEC 还没有超过 BioTransformer；
- ECLIPSE 仍有较明显 unchanged-parent 输出问题，需要 parent filtering。

### 3.3 enviPath

enviPath 要分成两种完全不同的能力：

```text
enviPath BBD Rules prediction:
  用规则/setting 进行一步预测，属于 prediction。

enviPath local snapshot lookup:
  从本地 BBD/Soil/Sludge 已知路径表里检索 parent → known products，
  属于已知路径查询，不是 blind prediction。
```

这点非常重要。Soil/Sludge lookup 得到 100% 找回，是因为评估对象本身来自 Soil/Sludge enviPath 快照；这证明 lookup 层完整可用，但不能写成“enviPath 预测准确率 100%”。

## 4. BBD83 已知污染物路径集结果

### 4.1 早期四路线比较

BBD83 / 148 accepted product labels 上，早期四路线比较的核心结果如下：

| Route | Any prediction | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product labels recovered@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 76/83 | 28/83 | 40/83 | 50/83 | 50/83 | 0.428 | 60/148 |
| enviPath BBD Rules prediction | 79/83 | 20/83 | 35/83 | 42/83 | 43/83 | 0.343 | 60/148 |
| enviFormer latest-current | 82/83 | 1/83 | 1/83 | 2/83 | 3/83 | 0.016 | 4/148 |

当时结论：

- BioTransformer 是主线；
- enviPath BBD Rules prediction 有补充价值；
- 当前可获得的 enviFormer checkpoint 不适合做主线。

答案表自检：

```text
BBD83 restricted accepted-products table:
rows = 148
unique cases = 83
RDKit-canonical parent == accepted product rows = 0
```

因此 BBD83 的分数不是靠“答案本身就是底物”抬高的。

### 4.2 ECLIPSE 初始两阶段配置

ECMap H-ECLIPSE + USPTO-pretrained product transformer 在 BBD83 上没有形成有效提升：

| Route | Valid cases | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product labels recovered@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ECLIPSE NoEC product | 80/83 | 3/83 | 4/83 | 4/83 | 4/83 | 0.042 | 5/148 |
| ECLIPSE PredEC product | 83/83 | 2/83 | 2/83 | 2/83 | 2/83 | 0.024 | 3/148 |
| BioTransformer ENVMICRO baseline | - | 28/83 | 40/83 | 50/83 | 50/83 | 0.428 | 60/148 |

原因主要是 EC 预测和污染物降解任务不匹配：EC3 Hit@10 只有 9/82。

### 4.3 BBD-finetuned ECLIPSE

后来做了 BBD fine-tune。这个结果比初始配置明显好：

| Route | Cases | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product recovery@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| NoEC all-fold parent-filtered | 83 | 25/83 | 43/83 | 45/83 | 47/83 | 0.408 | 59/148 |
| PREDEC all-fold parent-filtered | 83 | 37/83 | 60/83 | 66/83 | 66/83 | 0.589 | 87/148 |
| NoEC OOF parent-filtered | 81 | 15/81 | 26/81 | 26/81 | 26/81 | 0.251 | 28/145 |
| PREDEC OOF parent-filtered | 81 | 26/81 | 38/81 | 38/81 | 38/81 | 0.389 | 45/145 |

解释：

- all-fold 结果说明 BBD fine-tuning 和 EC 条件确实有信号；
- 但 all-fold 可能包含训练/测试接近带来的乐观因素；
- OOF-only 更保守，PREDEC 仍优于 NoEC，但低于 BioTransformer BBD83 baseline 的 Hit@10 50/83、MRR@10 0.428。

因此 ECLIPSE PREDEC 可以保留为补充候选源，但现在不适合直接替代 BioTransformer。

## 5. Soil/Sludge 转移测试结果

### 5.1 测试集

输入来自已下载的 enviPath 数据：

| Dataset | Raw rows |
|---|---:|
| Soil | 2584 |
| Sludge | 497 |
| Soil + Sludge | 3081 |

清洗后：

| Item | Count |
|---|---:|
| unique parents | 1788 |
| accepted parent-product labels | 2924 |
| BBD-overlap parents | 57 |
| BBD-parent-excluded denominator | 1731 |

这不是严格外部文献 benchmark，而是 Soil/Sludge 跨数据集转移评估。

答案表自检：

```text
Soil/Sludge unique-parent answer key:
rows = 2924
unique parents = 1788
RDKit-canonical parent == accepted product rows = 0

Soil/Sludge parent-product dedup table:
rows = 2924
RDKit-canonical parent == product rows = 0
```

所以 Soil/Sludge 评估也没有把“底物本身”当成正确转化产物计分。

### 5.2 Blind prediction 指标

combined all-valid / parent-filtered：

| Route | Valid non-empty coverage | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 |
|---|---:|---:|---:|---:|---:|---:|
| ECLIPSE NoEC | 1781/1788 | 10.91% | 18.85% | 22.15% | 23.15% | 0.154 |
| ECLIPSE PREDEC | 1785/1788 | 11.35% | 20.81% | 25.11% | 26.51% | 0.167 |
| BioTransformer ENVMICRO | 1679/1788 | 10.63% | 21.48% | 27.52% | 30.93% | 0.172 |

BBD-parent-excluded / parent-filtered：

| Route | Valid non-empty coverage | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 |
|---|---:|---:|---:|---:|---:|---:|
| ECLIPSE NoEC | 1724/1731 | 10.75% | 18.49% | 21.72% | 22.76% | 0.151 |
| ECLIPSE PREDEC | 1728/1731 | 11.15% | 20.34% | 24.67% | 26.00% | 0.164 |
| BioTransformer ENVMICRO | 1628/1731 | 10.40% | 21.14% | 27.21% | 30.73% | 0.170 |

解释：

- PREDEC 相比 NoEC 稳定提升；
- BioTransformer 在 Hit@3/5/10 和 product-label recovery 上仍更强；
- BioTransformer 有 109 个 combined all-valid empty/error parent，这些在全分母指标中保留为 miss。

### 5.3 enviPath lookup 指标

对同一批 Soil/Sludge-derived parent，enviPath 本地快照 lookup：

| Scope | Parents found | Product labels recovered | Product recall |
|---|---:|---:|---:|
| combined | 1788/1788 | 2924/2924 | 100.0% |
| soil | 1521/1521 | 2454/2454 | 100.0% |
| sludge | 276/276 | 501/501 | 100.0% |
| bbd_parent_excluded | 1731/1731 | 2834/2834 | 100.0% |

官方 API 也做了 bounded sanity check：

```text
sample_size=80
HTTP 200 = 80/80
errors = 0
```

解释：

- 这证明本地 enviPath Soil/Sludge 快照可作为完整 known-pathway retrieval layer；
- 不能把它当作 blind prediction 分数。

## 6. 三个工具整体能力比较

| 工具/路线 | 最适合做什么 | 当前证据 | 优点 | 风险/限制 | 当前定位 |
|---|---|---|---|---|---|
| BioTransformer ENVMICRO | 未知底物 blind prediction | BBD83 Hit@10 50/83；Soil/Sludge Hit@10 30.93% | 当前最稳；不依赖我们训练；parent-copy 问题少 | 有 empty/error；规则覆盖有限 | 主预测基线 |
| enviPath | 已知路径查询；BBD Rules 可作补充预测 | Soil/Sludge lookup 1788/1788 parent、2924/2924 product；BBD Rules BBD83 Hit@10 43/83 | 已知路径检索强；可补 BioTransformer 漏例 | lookup 不是 prediction；外部未知底物仍需预测工具 | 已知路径优先检索层 + 规则补充 |
| BBD-finetuned ECLIPSE PREDEC | 补充候选生成；研究 EC 条件帮助 | Soil/Sludge Hit@10 26.51%；BBD83 OOF parent-filtered Hit@10 38/81 | 比 NoEC 明显好；说明 EC 条件有信号 | 仍低于 BioTransformer；parent-copy；泛化需外部验证 | 补充候选源 / 后续优化对象 |

补充：当前可获得的 enviFormer checkpoint 在 BBD83 上表现很弱，且 enviFormer 不是 ECLIPSE NoEC。因此本报告不把 enviFormer 作为最终三路线之一。

## 7. 推荐使用策略

建议后续系统路线写成：

```text
输入 parent SMILES
  ↓
先查 enviPath 本地快照 / 已知路径库
  ├─ 若找到：返回 known pathway products，并标注 retrieval / observed evidence
  └─ 若找不到：进入 blind prediction
          ↓
      BioTransformer ENVMICRO 作为主预测
          ↓
      ECLIPSE PREDEC 作为补充候选源
          ↓
      合并、去 unchanged-parent、去重、按来源与证据等级排序
```

其中：

- enviPath lookup 结果应标注为“已知路径检索/数据库证据”；
- BioTransformer 和 ECLIPSE 结果应标注为“模型预测候选”；
- 不应把 lookup 结果和 prediction Hit@K 混成一个准确率。

## 8. 还不能声称什么

目前不能声称：

```text
ECLIPSE 已经超过 BioTransformer。
enviPath 对 Soil/Sludge 的预测准确率是 100%。
这已经是严格非 BBD 外部 benchmark。
```

可以声称：

```text
BioTransformer 仍是当前最稳的 blind prediction baseline。
BBD-finetuned ECLIPSE PREDEC 比 NoEC 有稳定提升，但目前更适合补充候选。
enviPath local snapshot lookup 对已知 Soil/Sludge parent/pathway 完整可用，应作为已知路径检索层。
```

## 9. 后续建议

短期建议：

1. 先把本报告作为阶段性结论交付；
2. 系统设计采用“enviPath lookup first + BioTransformer prediction + ECLIPSE PREDEC supplement”；
3. 如果要继续研究，优先构建严格非 BBD、非 enviPath-lineage 的外部小测试集。

中期可做：

1. BBD + Soil + Sludge 联合训练 ECLIPSE，但必须留出外部测试集；
2. 做 BioTransformer / ECLIPSE candidate-level complementarity；
3. 对 ECLIPSE parent-copy 做标准过滤和重排；
4. 如果能拿到更好环境降解 EC predictor，再重新评估 PREDEC。

## 10. 本报告对应证据

关键入口：

```text
EVIDENCE_INDEX_2026-08-19.md
../01_Key_Tables/tool_capability_comparison_2026-08-19.md
../01_Key_Tables/soil_sludge_metrics_summary_v2.csv
../01_Key_Tables/envipath_lookup_summary_metrics.csv
```

关键本地审计：

```text
../03_Local_Audits/CHEM_ECLIPSE_BBD_FINETUNE_SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_RETURN_LOCAL_AUDIT_2026-08-19.md
../03_Local_Audits/ENVIPATH_SOIL_SLUDGE_KNOWN_PATHWAY_LOOKUP_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-19.md
../03_Local_Audits/CHEM_ECLIPSE_BBD83_OOF_PARENTFILTER_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-18.md
../03_Local_Audits/ENZYMECAGE_M3_P1_2_1_BBD_KNOWN_PATHWAY_V0_2_FOUR_ROUTE_RERUN1_RETURN_SCORING_AUDIT_2026-08-05.md
```
