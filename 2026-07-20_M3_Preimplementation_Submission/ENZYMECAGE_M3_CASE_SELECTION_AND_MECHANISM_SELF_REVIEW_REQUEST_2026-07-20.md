# EnzymeCAGE M3 三案例选择与机理自审确认申请

日期：2026-07-20

回复老师文件：

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_P0_ADJUDICATION_AND_IMPLEMENTATION_CONTRACT_2026-07-17.md
```

当前状态：M3-P0 已通过；本文件只提交三个待确认案例及学生机理自审。三个案例尚未冻结，M3-P1 代码尚未编写，M3-P2/P3/P4 尚未启动。

## 一、申请老师确认的组合

| Case | 角色 | Reaction SHA256 | Rhea / EC | B pool / 命中 | C pool / 命中 | 按裁定实际路线 |
|---|---|---|---|---:|---:|---|
| 1 | strong 污水 plausible | `240655c6546e987d720edcb3f4467e2076ac97245172d81343831e7dfc97f3a8` | 40543 / 1.14.15.33 | 1 / 1 | 5 / 1 | B-primary |
| 2 | medium 非污水 | `19fe5b26e16a1a8ca60628be8718d3162cabded0299e2276a8503aec787bcf15` | 11532 / 1.4.3.19 | 10 / 3 | 17 / 3 | B-primary |
| 3 | weak 非污水技术边界 | `03900c0cd72deb2cdbdc826defd03e694d0ac53cd1ec8fbba509845fe1b92152` | 24292 / 2.3.1.1 | 0 / 0 | 79 / 0 | C-fallback |

三个案例的 B、C 独立 pool 均不超过 100。Case 1 和 case 2 两路均召回正确 UID；case 3 两路均未召回正确 UID，具体边界在第四节如实说明，请老师明确确认是否接受其作为 weak 技术边界。

本次 pool 证据来自 M3-P0B1：B 和 C 均全局排除 451 个 P0 query 反应；B 只用固定 Rhea 140 与 formal Label=1 行中的显式完整 EC；C 使用原版 top-10 相似反应召回。已知正确 UID 只用于事后评价，没有参与候选构造或路线选择。

## 二、Case 1：strong 污水 plausible

### 2.1 固定身份与反应

```yaml
reaction_sha256: 240655c6546e987d720edcb3f4467e2076ac97245172d81343831e7dfc97f3a8
rhea_master_id: 40543
ec: 1.14.15.33
difficulty_tier: STRONG_TOP_5
best_positive_rank: 1
wastewater_status: SUPPORTED_PLAUSIBLE_REQUIRES_REVIEW
```

Rhea 140 官方反应：

```text
10-deoxymethymycin + 2 reduced [2Fe-2S]-[ferredoxin] + O2 + 2 H(+)
= neomethymycin + 2 oxidized [2Fe-2S]-[ferredoxin] + H2O
```

Canonical reaction SMILES：

```text
CC[C@H]1OC(=O)[C@H](C)[C@@H](O[C@@H]2O[C@H](C)C[C@H](N(C)C)[C@H]2O)[C@@H](C)C[C@@H](C)C(=O)/C=C/[C@H]1C.O=O.S1[Fe]S[Fe+]1.S1[Fe]S[Fe+]1>>C[C@@H]1C[C@H](N(C)C)[C@@H](O)[C@H](O[C@H]2[C@@H](C)C[C@@H](C)C(=O)/C=C/[C@@H](C)[C@@H]([C@@H](C)O)OC(=O)[C@@H]2C)O1.O.S1[Fe+]S[Fe+]1.S1[Fe+]S[Fe+]1
```

### 2.2 学生机理自审

底物到产物发生含氧官能团引入；O2、两个还原型 [2Fe-2S]-ferredoxin 和质子参与，产物侧生成水及氧化型 ferredoxin。该计量关系与 EC 1.14.15.33 的 ferredoxin-dependent oxygenase 氧化/羟化类型一致。Rhea master、EC、反应 SMILES 和唯一已知 UID O87605 相互一致，未发现机理方向或辅因子矛盾。

污水证据边界：10-deoxymethymycin 在项目底物表中被标为“广义新污染物-抗生素”，来源记录为 `WW_7226bd3b19a6e4a3`。这只支持将本案例列作污水/新污染物 plausible 场景，不证明该反应已在污水体系中验证，也不证明产物更易降解。

### 2.3 B/C 完整候选结果

已知正例及冻结 D4 rank：

```text
O87605: 1
```

B query-excluded pool（实际采用）：

```text
O87605
```

C original-top10 pool：

```text
D5E3H2, O87605, Q00441, Q9KIZ4, Q9ZHQ1
```

两路均包含 O87605。B 非空，依老师裁定采用 B-primary；C 只保留为独立 provenance，不做并集。

## 三、Case 2：medium 非污水

### 3.1 固定身份与反应

```yaml
reaction_sha256: 19fe5b26e16a1a8ca60628be8718d3162cabded0299e2276a8503aec787bcf15
rhea_master_id: 11532
ec: 1.4.3.19
difficulty_tier: MEDIUM_6_TO_30
best_positive_rank: 8
wastewater_status: NOT_ESTABLISHED
```

Rhea 140 官方反应：

```text
glycine + O2 + H2O = glyoxylate + H2O2 + NH4(+)
```

Canonical reaction SMILES：

```text
NCC(=O)O.O.O=O>>N.O=CC(=O)O.OO
```

### 3.2 选择理由与学生机理自审

老师指出两个污水 medium 候选的正确 UID 均未入池，并允许从 P0 非污水 `MEDIUM_6_TO_30` 中选择 B 或 C 能召回正确 UID 的反应。Rhea:11532 的 best rank=8，难度标签真实为 medium；B=10、C=17，且两路各召回 3 个正确 UID，因此不需要人为调整难度，也不需要虚构污水关联。

反应把 glycine 氧化为 glyoxylate，同时释放 NH4(+) 并将 O2 还原为 H2O2，符合 EC 1.4.3.19 的以氧为受体的氨基酸氧化脱氨类型。Rhea、EC、SMILES 的反应物和产物一致，未发现方向或计量冲突。

### 3.3 B/C 完整候选结果

已知正例及冻结 D4 ranks：

```text
S5FMM4:8, Q5L2C2:9, O31616:10, Q55710:17,
Q3M859:21, Q8YRC9:25, P33642:33, Q88Q83:34
```

B query-excluded pool（实际采用）：

```text
A0A095C6S0, A0A499UB99, C4R4G9, O31616, P80324,
Q5L2C2, Q7X2D3, Q99042, Q9Y7N4, S5FMM4
```

C original-top10 pool：

```text
A0A095C6S0, A0A499UB99, C4R4G9, C4R6B0, J9VRT1,
O31616, P80324, Q1AYM8, Q5L2C2, Q75WF1, Q7X2D3,
Q8VPD4, Q99042, Q9X7P6, Q9Y7N4, S4S6Z0, S5FMM4
```

两路共同召回 O31616、Q5L2C2、S5FMM4。B 非空，依老师裁定采用 B-primary；其余 5 个已知正例没有进入公平 B 或 C pool，不能写成 8/8 召回。

## 四、Case 3：weak 非污水技术边界

### 4.1 固定身份与反应

```yaml
reaction_sha256: 03900c0cd72deb2cdbdc826defd03e694d0ac53cd1ec8fbba509845fe1b92152
rhea_master_id: 24292
ec: 2.3.1.1
difficulty_tier: WEAK_OVER_100
best_positive_rank: 644
wastewater_status: NOT_ESTABLISHED
```

Rhea 140 官方反应：

```text
L-glutamate + acetyl-CoA = N-acetyl-L-glutamate + CoA + H(+)
```

Canonical reaction SMILES：

```text
CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1OP(=O)(O)O.N[C@@H](CCC(=O)O)C(=O)O>>CC(=O)N[C@@H](CCC(=O)O)C(=O)O.CC(C)(COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1OP(=O)(O)O)[C@@H](O)C(=O)NCCC(=O)NCCS
```

### 4.2 学生机理自审

反应从 acetyl-CoA 向 L-glutamate 氨基转移乙酰基，生成 N-acetyl-L-glutamate、CoA 和 H(+)，与 EC 2.3.1.1 的 amino-acid N-acetyltransferase 类型一致。官方式、EC 和 canonical SMILES 未见反应物、产物或方向矛盾。

### 4.3 B/C 完整候选结果与失败边界

该反应有 295 个 D4-valid 已知正例，冻结 D4 最佳 rank 为 644。公平 B pool 为空：

```text
[]
```

B 为空后按裁定使用 C-fallback。C pool 共 79 个 UID：

```text
A0A120HUS7, A0A1D3PCK2, A6VCX3, A8F961, B0VH76,
C3MPM7, C3MYM1, C3N5A3, C3NDV7, C3NHU6, C4KGW9,
D2Z028, E9P8D2, O27667, O34350, O59390, O87198, O94225,
P05342, P05345, P0A9D4, P0A9D5, P0A9D6, P0A9D7, P16426,
P21861, P29847, P31668, P32003, P43886, P46854, P48570,
P54951, P57162, P58637, P58967, P67764, P67765, P67766,
P70728, P71043, P71405, P74089, P76112, P77985, P95231,
Q00852, Q00853, Q01181, Q06750, Q07179, Q09927, Q12122,
Q12726, Q44290, Q47884, Q4J989, Q52070, Q56002, Q57146,
Q57926, Q59967, Q5HIE6, Q5HRM4, Q65PC9, Q6GBV9, Q6GJE0,
Q89B11, Q8CTU2, Q8TKQ6, Q8TW28, Q8ZPD3, Q971S5, Q97ZE0,
Q9HUU7, Q9US33, Q9V1J1, Q9Y823, Q9ZK14
```

这 79 个 UID 与 295 个已知正例的交集为 0。因此该 case 不是“正确酶已入池但模型排到 644”，而是候选召回阶段已经失败，M3 v1 后续排序没有机会找到正确酶。

独立复算 21 个 `WEAK_OVER_100` query：

```text
B pool <=100 且 C pool <=100：1 个
上述集合中 B 或 C 至少召回一个正确 UID：0 个
```

所以 Rhea:24292 是唯一满足老师两池上限的 weak 候选，但它展示的是检索失败边界。请老师明确裁定：

```text
M3C3-A：接受 Rhea:24292 作为 weak 技术边界，明确预期结果为候选召回 fail closed；
M3C3-B：不接受零正确 UID 入池的 weak case，并重新定义或放宽 weak case 条件后再选。
```

在老师确认前，本地不把 case 3 冻结为正式配置。

## 五、与老师合同的完整对照

| 要求 | 本次结果 |
|---|---|
| strong 污水 plausible | Rhea:40543，规则支持但仍需人工审核 |
| medium | 污水 medium 不可用后，按授权选择非污水 Rhea:11532 |
| weak 非污水技术边界 | 提交唯一两池合规的 Rhea:24292，并披露两路零召回 |
| 三个案例 B/C 均 <=100 | 1/5、10/17、0/79，全部满足 |
| 保存两路完整 UID 与 provenance | 本文件列出完整 UID；底层 B1 证据保存完整来源 |
| B-primary/C-fallback | case 1/2 用 B，case 3 因 B 空使用 C |
| 不做 B+C 并集 | 满足 |
| D4 冻结资产域 | 所有候选均来自 D4-valid domain；未补资产 |
| 定量结果逐 case 披露 | 已披露 pool、recover、已知正例与历史 rank |
| 三层资产框架只作后续引用 | 当前 demo 只覆盖 `d4_computable_asset_pool` 子集，不在 M3 实现资产补齐 |
| 学生自审后老师复核 | 本文件为学生自审，等待老师确认 |

## 六、老师要求的八项逐 case 记录状态

本文件处于案例冻结前，不把尚未运行的 M3 stage、schema 或 batch-context
测试写成完成。八项记录当前状态如下，冻结后继续沿用同一口径：

| # | 老师要求 | Case 1 | Case 2 | Case 3 |
|---|---|---|---|---|
| 1 | 每一 stage 与 schema | 仅案例选择/机理自审完成；M3-P1 未启动，无 live schema 结果 | 同左 | 同左 |
| 2 | 反应、Rhea/EC 或邻居 provenance | Rhea:40543、EC 1.14.15.33；B/C 完整底层 provenance 已保存在 B1 | Rhea:11532、EC 1.4.3.19；B/C provenance 已保存 | Rhea:24292、EC 2.3.1.1；B/C provenance 已保存 |
| 3 | pool 路线、大小、正确 UID 入池 | B-primary；B=1/1，C=5/1 | B-primary；B=10/3，C=17/3 | C-fallback；B=0/0，C=79/0，明确未召回 |
| 4 | EnzymeCAGE rank、Top-10/Top-50 | 历史 rank=1；Top-10=1/1，Top-50=1/1 | 历史 ranks=8,9,10,17,21,25,33,34；Top-10=3/8，Top-50=8/8 | 历史 best rank=644；Top-10=0/295，Top-50=0/295；且当前候选 pool 已先 miss |
| 5 | EC class、机理、污水判断 | 氧化/羟化；污水 plausible，需复核 | 氧化脱氨；非污水 | 乙酰基转移；非污水技术边界 |
| 6 | 不确定性、batch context、资产域 | 污水证据仅规则匹配；本次未运行新 batch-context 测试；候选限 D4 冻结资产域 | 非污水；本次未运行新 batch-context 测试；候选限 D4 冻结资产域 | 两路零召回；本次未运行新 batch-context 测试；候选限 D4 冻结资产域 |
| 7 | 不把 rank 1 写成现实世界最优酶 | 未作该表述；rank 只表示冻结评估排序 | 同左 | 同左 |
| 8 | 学生/老师/外部专家审核 | 学生自审完成；老师待确认；外部专家未审核且不是当前硬门槛 | 同左 | 学生自审完成但零召回边界待老师明示；外部专家未审核 |

这里的 Top-10/Top-50 是 A1A 冻结历史排名统计，不是本次重新推理结果。Case 3
的 rank=644 也不能移植到当前 C=79 pool；因为正确 UID 不在该 pool 中，当前
路线只能 fail closed。

## 七、证据来源与解释边界

本文件的 Rhea master、官方反应式和 EC 来自固定下载到本地的 Rhea 140
`rhea-directions.tsv`、`rhea2ec.tsv`、`rhea-reactions.txt.gz` 和
`rhea-reaction-smiles.tsv` 离线连接，不是在线逐条 API 查询，也不是大模型
生成。难度与历史 rank 来自已接受 A1A 固定五 seed 预测证据；B/C pool 与 UID
成员来自已接受 B1 公平 query-excluded 证据。

本次没有重新运行模型。文中的 pool rank 不存在，因为 B/C pool 是 UID 集合；
所列 rank 是冻结 D4 评估中的 EnzymeCAGE 历史 rank。候选入池、模型排序和真实
生物学有效性是三个不同层次，本文没有把它们互相替代。

## 八、请求老师确认

请老师确认：

1. case 1 Rhea:40543 是否可冻结为 strong 污水 plausible case；
2. case 2 Rhea:11532 是否可冻结为 medium 非污水 case；
3. case 3 是否接受 `M3C3-A` 的“候选召回失败型 weak 技术边界”。

老师确认后，学生再生成三个正式 case YAML/JSON；在此之前不写 M3-P1 Agent 代码。
