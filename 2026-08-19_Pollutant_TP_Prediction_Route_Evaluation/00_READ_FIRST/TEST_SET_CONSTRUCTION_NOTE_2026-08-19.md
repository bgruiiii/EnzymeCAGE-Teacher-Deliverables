# 测试集构建说明 — 污染物转化产物预测路线评估

日期：2026-08-19  
用途：说明本交付包中 BBD83 与 Soil/Sludge 两类评估集的来源、清洗口径和使用边界。

## 1. 本交付包用了哪几类测试集

本阶段实际用于结论汇总的测试集有两类：

| 测试集 | 用途 | 是否 blind prediction | 当前定位 |
|---|---|---|---|
| BBD83 已知污染物路径集 | 比较 BioTransformer、enviPath BBD Rules、enviFormer、ECLIPSE 在 83 个 parent 上的一步产物预测能力 | 是，预测端只看 parent，不看答案 | 早期主比较集，但与 BBD/enviPath 数据源关系较近 |
| enviPath Soil/Sludge 转移集 | 检查 BBD-only ECLIPSE 与 BioTransformer 在 Soil/Sludge parent 上的跨数据集表现；同时验证 enviPath 本地 known-pathway lookup | prediction 部分是；lookup 部分不是 | 阶段性转移评估，不等同于严格外部文献 benchmark |

另有一个严格非 BBD / 非 enviPath-lineage 的外部文献测试集正在构建中，但还没有达到冻结预测标准，因此本交付包只记录其当前状态，不把它作为最终指标来源。

## 2. BBD83 是怎么来的

BBD83 来自前期整理的 BBD / enviPath-lineage 已知污染物一代转化路径。

核心口径：

```text
parent cases = 83
accepted one-step product labels = 148
```

预测评估时，执行端只能读取 blind parent input；答案表用于本地评分与审计，不提供给预测工具。

本交付包保留了以下证据：

```text
../02_Return_Packages/enzymecage_m3_p1_2_1_bbd_known_pathway_v0_2_four_route_blind_rerun1_20260805.tar.gz
../02_Return_Packages/enzymecage_m3_p1_2_1_bbd83_eclipse_two_stage_ec_conditioned_product_pilot_20260817.tar.gz
../02_Return_Packages/chem_eclipse_bbd_fullfold_bbd83_oof_parentfilter_supplement_20260817.tar.gz
../03_Local_Audits/ENZYMECAGE_M3_P1_2_1_BBD_KNOWN_PATHWAY_V0_2_FOUR_ROUTE_RERUN1_RETURN_SCORING_AUDIT_2026-08-05.md
../03_Local_Audits/ECLIPSE_TWO_STAGE_EC_CONDITIONED_PRODUCT_BBD83_RETURN_LOCAL_AUDIT_2026-08-17.md
../03_Local_Audits/CHEM_ECLIPSE_BBD83_OOF_PARENTFILTER_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-18.md
```

本地 RDKit canonical 自检确认：

```text
BBD83 accepted-products table:
rows = 148
unique cases = 83
parent == accepted product rows = 0
```

因此 BBD83 的得分不是靠“预测出底物本身”抬高的。

## 3. Soil/Sludge 转移集是怎么来的

Soil/Sludge 转移集来自 chenyu 侧下载并整理的 enviPath 数据。

原始资产记录：

| Dataset | Raw reactions / processed rows context |
|---|---:|
| BBD | 1480 reactions；processed table 中 BBD 1549 rows |
| Soil | 2445 reactions；processed table 中 Soil 2584 rows |
| Sludge | 494 reactions；processed table 中 Sludge 497 rows |

本阶段用于 Soil/Sludge 评估的是清洗后的 unique-parent answer key：

```text
unique parents = 1788
accepted parent-product labels = 2924
BBD-overlap parents = 57
BBD-parent-excluded denominator = 1731
```

本交付包同时报告两个口径：

1. combined all-valid parent-filtered：1788 个 parent；
2. BBD-parent-excluded parent-filtered：排除 57 个 BBD-overlap parent 后的 1731 个 parent。

这样做的目的是防止 BBD fine-tuned ECLIPSE 因为训练数据相近而被过度乐观评价。

本地 RDKit canonical 自检确认：

```text
Soil/Sludge unique-parent answer key:
rows = 2924
unique parents = 1788
parent == accepted product rows = 0

Soil/Sludge parent-product dedup table:
rows = 2924
parent == product rows = 0
```

因此 Soil/Sludge 的预测分数也不是靠 unchanged parent 抬高的。

## 4. 哪些是预测，哪些是查询

这个边界是本阶段最重要的解释点。

| Route | 属于什么 | 能不能当预测准确率 |
|---|---|---|
| BioTransformer ENVMICRO | blind prediction | 可以 |
| ECLIPSE NoEC / PREDEC | blind prediction | 可以 |
| enviFormer latest-current | blind prediction | 可以，但当前分数很低 |
| enviPath BBD Rules prediction | rule-based prediction | 可以，但只在 BBD83 里作为预测路线比较 |
| enviPath local snapshot lookup | known-pathway lookup / database retrieval | 不可以当作 blind prediction accuracy |

所以 Soil/Sludge 中 enviPath lookup 的 1788/1788 parent 和 2924/2924 product 找回，只能说明：

```text
本地 enviPath Soil/Sludge 快照作为已知路径检索层完整可用。
```

不能写成：

```text
enviPath 对 Soil/Sludge 的预测准确率是 100%。
```

## 5. 为什么严格外部文献集还没放进最终指标

我们已经启动了非 BBD / 非 enviPath-lineage 的外部文献测试集构建，但 V0/V1 审计显示还不能直接用于最终预测：

1. V0 primary 过度集中在 PFAS / PAP / fluorotelomer 等少数化学类别；
2. 一些候选证据来源属于 abiotic、plasma、vague environmental 或 human-mixed，不适合作为微生物/环境降解主测试；
3. V1 clean primary 太小，reserve pool 仍需人工筛选和 enviPath overlap 排查；
4. 因此当前只记录“构建中”，不把它混进已完成指标。

对应状态审计：

```text
../03_Local_Audits/NON_BBD_EXTERNAL_TP_CURRENT_STATE_AND_SOIL_SLUDGE_SIDE_TEST_DECISION_2026-08-18.md
```

## 6. 最终结论使用边界

本交付包可以支持：

```text
BioTransformer 是当前最稳的 blind prediction baseline。
BBD-finetuned ECLIPSE PREDEC 比 ECLIPSE NoEC 有稳定提升，但目前更适合作为补充候选源。
enviPath local snapshot lookup 对已知 Soil/Sludge parent/pathway 完整可用，应作为已知路径检索层。
```

本交付包不能支持：

```text
ECLIPSE 已经全面超过 BioTransformer。
enviPath Soil/Sludge lookup 代表 100% blind prediction accuracy。
当前已经完成严格非 BBD 外部文献泛化验证。
```
