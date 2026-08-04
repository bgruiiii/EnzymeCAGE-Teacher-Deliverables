# M3 给黄老师的技术问题回复草稿：Q1 缺酶资产补齐链路；Q2 EnzymeCAGE 分数与 AutoDock 关系

日期：2026-08-03  
状态：draft；当前先回答前两个问题，第三个 BioTransformer 路径问题另行补入同一目录下的综合版。

## 0. 先给老师看的简短结论

本轮先回答两个问题。

第一，如果 Rhea/EC/相似反应扩展找到了候选酶，但该 UniProt UID 缺少当前 EnzymeCAGE D4 资产，我们已经完成了 UID-only 的按需补资产小试。结论是：这条链路可以做成智能体工具，但必须 fail-closed，并且要把 pocket 来源分成证据等级。严格 AlphaFill-transplant 8 Å pocket 路线在困难 100 UID 样本上补回 16/100；AlphaFoldDB-only + P2Rank predicted-pocket fallback 在同一困难样本上补回 45/100，其中 29 个是严格 AlphaFill 路线失败后被救回的 UID。生成成功的 UID 已经能通过 isolated EnzymeCAGE loader validation，可以进入后续酶排序模型的“临时/隔离资产”测试；但这不等于已经合并进正式生产资产，也不等于该酶一定是目标反应的真实正例。

第二，EnzymeCAGE 当前输出的 0–1 分数应作为主排序分数。这个分数是模型 raw logit 经 sigmoid 得到的 reaction-enzyme compatibility score，训练目标是反应-酶正负配对分类，评估目标也是 AUC、Top-K、MRR 等排序指标。它不是 AutoDock docking score，也不是结合自由能或 Km/kcat。AutoDock 更适合作为 Top-K 之后的可选二级证据、解释性检查或 soft rerank，不建议现在直接替代主模型分数，也不建议默认作为 hard filter。

## 1. Q1：如果候选酶缺少 EnzymeCAGE D4 资产，怎么办？

### 1.1 问题背景

在 M3-EXT / EC-Rhea 扩展里，会出现这种情况：

```text
反应证据链可以找到候选酶 UID
→ 但该 UID 不在当前 EnzymeCAGE 可直接打分的 D4 资产池里
→ 因此即使候选酶有实验或数据库证据，也不能直接送入 EnzymeCAGE geometric ranking
```

老师关心的是：是否可以像工具链一样，遇到缺失 UID 时现场补齐该酶的结构、口袋和蛋白特征，而不是等待全量酶池重新构建。

我们目前验证的是：

```text
输入：UniProt UID
输出：隔离 staged D4 assets + loader validation PASS / blocker report
边界：不修改正式生产资产；不声称生物学正例；只验证能否被 EnzymeCAGE loader 吃进去
```

### 1.2 原始 EnzymeCAGE 资产路线是什么

回源代码和 README 后，原始 EnzymeCAGE 可公开复现的蛋白资产路线大体是：

```text
UniProt / enzyme list
→ AlphaFoldDB / AlphaFill 结构相关资产
→ AlphaFill 预提取 pocket
→ protein feature 构建
→ EnzymeCAGE dataset / loader / ranking
```

证据点：

- `README.md:22-27` 要求下载数据后用 `feature/main.py` 计算 protein feature，并把 pocket 目录传入。
- `README.md:31-32` 明确说作者已经运行 AlphaFill 并预提取 enzyme pockets。
- `feature/download_af2_structures.py:14-23` 是 AlphaFoldDB 结构下载逻辑。
- `feature/extract_pocket.py:16` 固定 pocket 半径为 8 Å。
- `feature/extract_pocket.py:214-308` 从 AlphaFill JSON/结构中选 ligand/cofactor transplant 相关链，并保留 ligand 周围 8 Å 残基作为 pocket。

更正说明（2026-08-04，按老师 2026-08-03 反馈修复）：此前本稿写“当前公开仓库没有完整 P2Rank 生成脚本”不成立。以官方公开仓库 commit `255a05e167aabc70f6c0322a00702cdc9d6ebfbc` 为准，`scripts/` 下存在完整 P2Rank 脚本链：

```text
scripts/extract_p2rank_pockets.py（325 行）：
  写 P2Rank dataset → 调用 `prank predict -c alphafold`
  → 解析 prediction → 残基筛选 → 输出 pocket PDB / pocket_info

scripts/run_mining_pipeline.py：
  以 `--p2rank_home` / `--skip_p2rank` 控制 P2Rank 步骤，
  未 skip 时调用 `scripts/extract_p2rank_pockets.py`
```

因此，本轮路线 C 中：

```text
AlphaFoldDB protein-only structure → P2Rank 2.5.1 `prank predict -c alphafold` → predicted pocket
```

应表述为“官方公开 P2Rank pocket 生成流程的复现”；在本项目证据分级中，它可作为 lower-evidence predicted-pocket fallback / 对照，而不是仅仅“方向一致的 fallback 对照”。同时仍需保留证据等级边界：P2Rank predicted pocket 与 AlphaFill ligand-neighbor pocket 不是同一种证据，不能伪装成 strict AlphaFill transplant pocket。

`mix-af-p2rank` 的出处也已核正：该字符串见官方公开仓库 commit `255a05e167...` 的 `config/infer/Enzyme-405.yaml`、`config/infer/Orphan-335.yaml` 和 `config/infer/case-study/glutarate.yaml`，对应 `gvp_protein_feature_mix-af-p2rank.pt` 与 `esm_node_feature_mix-af-p2rank.pt` 等资产文件名。

### 1.3 我们测试了哪些补资产路线

我们围绕同一批困难 100 UID 做了三条路线。这个 100 UID 不是全库随机样本，而是从 current strict 2026 missing-pocket/missing-D4 metadata 中分层抽样，属于“失败富集/困难样本”，因此结果应解释为 rescue rate，不是全库覆盖率。

#### 路线 A：严格 AlphaFill-transplant 8 Å pocket 路线

链路：

```text
UniProt UID
→ UniProt sequence
→ public AlphaFill CIF/JSON
→ AlphaFill ligand/cofactor transplant metadata
→ 原 EnzymeCAGE 8 Å pocket extraction
→ corrected ESM-2 3B
→ GVP
→ isolated EnzymeCAGE loader validation
```

结果：

```text
16 / 100 PASS_FULL_D4_LOADER
```

主要 blocker：

| 状态 | 数量 | 含义 |
|---|---:|---|
| `PASS_FULL_D4_LOADER` | 16 | 严格 AlphaFill-transplant pocket 路线完整走通，并通过 isolated loader |
| `BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY` | 43 | AlphaFill 可访问，但没有可用 ligand/cofactor transplant metadata |
| `BLOCKED_ALPHAFILL_404` | 20 | 当前 public AlphaFill endpoint 没有该 UID 条目 |
| `BLOCKED_POCKET_EXTRACTION_EMPTY_OR_INVALID` | 17 | transplant metadata 存在，但原 EnzymeCAGE pocket extraction 没有生成有效 pocket |
| `BLOCKED_SEQUENCE_MISSING` | 4 | 实际是 UniProt fetch timeout/unresolved，不应解读为确认无序列 |

资源和时间：

```text
16 个 PASS UID 的平均 full D4 loader-valid 时间：51.31 s/UID
PASS UID 的 ESM-2 3B 平均计算时间：30.67 s/UID
GPU peak allocated：约 11.0–11.24 GB
process max RSS max：约 18.39 GB
```

这个时间包括从 UID 到可以被后续 EnzymeCAGE loader 验证的 staged D4 资产，而不是只下载结构或只跑 pocket。也就是包含 sequence、structure/pocket、ESM-2 3B、GVP 和 loader validation。

#### 路线 B：可用 3D 结构 + P2Rank predicted-pocket fallback

链路：

```text
UniProt UID
→ 可用 3D 结构（该 pilot 中多数复用 baseline AlphaFill CIF，少量 AlphaFoldDB）
→ P2Rank 2.5.1 predicted pocket
→ pocket PDB / pocket_info
→ corrected ESM-2 3B
→ GVP
→ isolated EnzymeCAGE loader validation
```

结果：

```text
42 / 100 PASS_PREDICTED_POCKET_D4_LOADER
其中 26 / 100 是严格 AlphaFill 路线失败后被 rescued
```

重要边界：

```text
这不是纯 AlphaFoldDB-only 对照；
该 pilot 主要证明“有可信 3D 结构时，P2Rank predicted-pocket fallback 可以明显提高覆盖”；
不能把 predicted-pocket PASS 混写成 strict AlphaFill-transplant PASS。
```

#### 路线 C：AlphaFoldDB-only + P2Rank predicted-pocket 对照

链路：

```text
UniProt UID
→ AlphaFoldDB protein-only 3D structure
→ P2Rank 2.5.1 `prank predict -c alphafold`
→ top predicted pocket residues
→ pocket PDB / pocket_info
→ corrected ESM-2 3B
→ GVP
→ isolated EnzymeCAGE loader validation
```

结果：

```text
45 / 100 PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER
29 / 100 是严格 AlphaFill 路线失败后被 rescued
88 / 100 AlphaFoldDB structure fetch PASS
43 / 100 BLOCKED_AFDB_P2RANK_NO_POCKET
12 / 100 BLOCKED_AFDB_STRUCTURE_FETCH_FAILED
```

这条路线是目前覆盖率最高、边界最清楚的一条 predicted-pocket fallback。关键解释是：

```text
BLOCKED_AFDB_P2RANK_NO_POCKET
不是“P2Rank 数据库里没有 pocket”。
P2Rank 不是数据库查询，而是本地/在线预测器。
它的含义是：AlphaFoldDB 结构拿到了、P2Rank 跑了，但没有产生可用 top predicted pocket residues。
```

```text
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED
表示 AlphaFoldDB API 和常规 v6/v5/v4 PDB/mmCIF URL 都没有拿到可用结构。
```

失败案例分析显示，43 个 no-pocket 里有 37 个序列长度 ≤120 aa；均值长度约 97.7 aa，中位数 95 aa。pLDDT 均值/中位数并不低，所以主要不像是 AlphaFold 低置信度造成，而更像是小蛋白/短肽或结构表面不形成 P2Rank 可接受的 ligandable pocket。也就是说，这主要是外部结构/pocket 证据或生物物理形态限制，不是 ESM-2 3B/GVP/loader 流程断裂。

资源和时间：

```text
45 个 PASS UID 的 warm/batched 平均 full D4 loader-valid 时间：16.34 s/UID
中位数：11.07 s/UID
最大值：89.58 s/UID
PASS stage mean：AFDB fetch 9.11 s，P2Rank 4.28 s，ESM-2 3B 1.01 s，GVP 0.58 s，loader 1.20 s
GPU peak allocated max：11244 MB
process max RSS max：16723 MB
```

这个 16.34 s/UID 是 warm/batched 状态下的实际运行观察值。因为 ESM-2 3B 模型加载和缓存会显著影响单酶耗时，不能把它直接说成冷启动单酶成本。结合严格 AlphaFill 路线和早期 P0A434 单酶测试，保守表述应为：

```text
warm/batched 工具运行：约 10–20 s/UID；
cold/single-start 单酶运行：建议按约 40–60 s/UID 估计；
GPU 显存按约 11–12 GB 级别预留；
进程内存按约 17–19 GB 级别预留。
```

### 1.4 为什么不能只用 AlphaFill，为什么要加入 P2Rank fallback

严格 AlphaFill 路线证据等级最高，因为 pocket 是从 ligand/cofactor transplant 上下文里定义的，和原 EnzymeCAGE 可公开复现路线最接近。

但在困难 100 UID 样本里，严格路线只有 16/100 走通，失败主要集中在：

```text
AlphaFill 无可用 transplant metadata；
AlphaFill 404；
原 pocket extractor 不能生成有效 pocket。
```

P2Rank fallback 的作用不是证明“预测 pocket 一定正确”，而是在 AlphaFill 没有 ligand/cofactor transplant 或 strict extractor 失败时，利用已有 3D 结构预测一个可用 pocket，使候选酶至少能进入模型侧的 lower-evidence ranking 试验。AlphaFoldDB-only + P2Rank 在同一困难样本中达到 45/100，说明它对覆盖率有实际帮助。

同时，P2Rank pocket 和 strict AlphaFill pocket 不能混为同一个证据等级。对 16 个 strict PASS control 比较：

```text
mixed-structure P2Rank vs strict AlphaFill pocket Jaccard mean ≈ 0.451
AlphaFoldDB-only P2Rank vs strict AlphaFill pocket Jaccard mean ≈ 0.340
```

这说明 predicted pocket 与 ligand-neighbor pocket 有重叠，但不完全一致，甚至可能有较大语义漂移。因此必须分层披露。

### 1.5 建议给智能体实现的正式策略

建议把按需补资产工具设计成分层、非破坏、fail-closed 的工具：

```text
Tool: EnzymeCAGE_OnDemand_D4_Backfill
Input: UniProt UID 或 UID 列表
Output: per-UID PASS/blocker status、staged asset paths、timing/resource、provenance、formal_assets_mutated=false
```

推荐层级：

| Tier | 路线 | 证据等级 | 是否建议进入后续 ranking |
|---|---|---|---|
| Tier 1 | AlphaFill transplant + original 8 Å pocket | 最高；最接近原 EnzymeCAGE 公开路线 | 可以作为 strict staged D4 |
| Tier 2 | AlphaFoldDB + P2Rank predicted pocket | 覆盖更好，但 pocket 是预测来的 | 可以作为 lower-evidence / predicted-pocket staged D4 |
| Tier 3 | old-pocket revalidation 或其他可信结构源 | 需另行授权和验证 | 暂不默认合并 |

工具必须避免：

```text
不允许凭空造 pocket；
不允许 whole-protein 或固定 residue 当作 pocket；
不允许把 P2Rank predicted-pocket 伪装成 AlphaFill transplant pocket；
不允许未经授权合并到正式生产资产；
不允许把资产可构建性等同于生物学正确性。
```

建议状态字段：

```text
PASS_FULL_D4_LOADER
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER
BLOCKED_SEQUENCE_FETCH_TIMEOUT
BLOCKED_SEQUENCE_MISSING_OR_UNRESOLVED
BLOCKED_ALPHAFILL_404
BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY
BLOCKED_ALPHAFILL_HAS_TRANSPLANTS_BUT_POCKET_EXTRACTION_EMPTY_OR_INVALID
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED
BLOCKED_AFDB_P2RANK_NO_POCKET
BLOCKED_ESM3B_FAILED
BLOCKED_GVP_FAILED
BLOCKED_LOADER_VALIDATION_FAILED
```

### 1.6 Q1 当前可给老师的结论

可以这样回复：

```text
我们已经把“缺少候选酶资产时能否按需补 D4”的链路做了小试。结论是可行，但应按证据等级分层。

严格复用原 EnzymeCAGE AlphaFill-transplant 8 Å pocket 逻辑时，在困难 100 UID 样本上有 16/100 能补到 isolated loader-valid D4 资产，PASS UID 平均约 51.31 s/UID，ESM-2 3B 是主要耗时，GPU 峰值约 11–12 GB。

如果允许 lower-evidence predicted-pocket fallback，则 AlphaFoldDB-only + P2Rank 在同一困难样本上补到 45/100，其中 29 个是 strict AlphaFill 失败后被救回的 UID。成功样本已包含 ESM-2 3B、GVP、pocket-node feature 和 isolated EnzymeCAGE loader validation；warm/batched 运行平均约 16.34 s/UID，但冷启动单酶建议保守按 40–60 s/UID 估计。

失败主要是外部结构/pocket 证据不可用或蛋白本身太短/无可用 predicted pocket，不是 ESM/GVP/loader 后段流程失败。建议后续智能体采用 Tier 1 strict AlphaFill + Tier 2 AlphaFoldDB/P2Rank fallback 的非破坏式按需补资产工具，所有结果带 blocker 和 provenance，不直接合并生产资产。
```

## 2. Q2：EnzymeCAGE 0–1 分数是否足够？需不需要加 AutoDock？

### 2.1 0–1 分数是什么

EnzymeCAGE 当前输出的 0–1 分数不是 docking score，而是模型学到的 reaction-enzyme compatibility score。

代码证据（官方公开 EnzymeCAGE commit `255a05e167aabc70f6c0322a00702cdc9d6ebfbc`）：

- `enzymecage/model.py:310-315`：模型拼接特征后通过 MLP 输出一个标量；如果 `sigmoid_readout=True`，直接做 sigmoid。
- `enzymecage/model.py:317-328`：predict 阶段如果模型本身没有 sigmoid readout，则对 raw logit 做 sigmoid。
- `enzymecage/base.py:33-40`：evaluate 阶段同样把 raw logit sigmoid 成 0–1 分数后算指标。

所以：

```text
EnzymeCAGE_score = sigmoid(raw model logit)
```

它可以被称为 probability-like score 或 compatibility score，但不能直接叫物理概率、结合自由能或 docking energy。

### 2.2 这个分数是怎么训练出来的

训练代码证据（官方公开 EnzymeCAGE commit `255a05e167aabc70f6c0322a00702cdc9d6ebfbc`）：

- `train.py:113` 使用 `BCEWithLogitsLoss(reduction='none')`。
- `train.py:128-133` 用 `batch.y` 作为 target，并用模型输出和 target 计算 loss。
- `enzymecage/dataset/geometric.py:170-173,310` 中每行样本的标签来自 `Label` 列，并作为 `data.y`。

因此监督目标是：

```text
这个 reaction-enzyme pair 是否像训练数据里的正例配对。
```

不是：

```text
docking energy；
结合自由能；
Km；
kcat；
kcat/Km；
实验活性值；
过渡态稳定化能。
```

评估代码也说明它是排序/分类分数：

- `evaluate.py:31-36` 对同一反应下候选酶按预测分数降序排序。
- `evaluate.py:55-62` 计算 Top-1/3/5/10 success rate。
- `enzymecage/base.py:63-69` 计算 Accuracy、AUC、Precision、Recall、F1。

### 2.3 它有没有包含结构和结合相关信息

有，但方式是神经网络特征融合，不是显式 docking。

正式配置证据：

说明：`config/train/pretrain_esm2_3b/seed_42.yaml` 不是官方公开 commit `255a05e167aabc70f6c0322a00702cdc9d6ebfbc` 自带配置；官方公开默认训练配置 `config/train/pretrain/seed_42.yaml:1-10` 使用的是 `ESM-C_600M`。这里引用的是我们本项目在 Chenyu/本地同步的 ESM-2 3B corrected-pocket 正式运行配置，SHA256 为 `83e806341a36bad037aef1af5003b3a01c0ac9a23e5d3699ec605a66d3f0639a`，来源由 2026-07-06 至 2026-07-08 的 ESM-2 3B 配置/迁移审计记录支撑。

- `config/train/pretrain_esm2_3b/seed_42.yaml:1-10`：当前模型为 `EnzymeCAGE`，开启 `geo-enhanced-interaction`、`use_structure=True`、`use_drfp=True`、`use_esm=True`，ESM 模型为 `esm2_t36_3B_UR50D`。
- `config/train/pretrain_esm2_3b/seed_42.yaml:27-33`：使用 reaction DRFP、GVP、ESM-2 3B protein-level、ESM pocket-node、molecule conformation、reaction center 等特征。

模型代码证据：

- `enzymecage/model.py:250-258`：GVP 结构输出和 pocket-node ESM feature 拼接为 enzyme pocket 表示。
- `enzymecage/model.py:267-275`：蛋白节点坐标距离用于 geometry attention bias。
- `enzymecage/model.py:277-285`：底物/产物 reacting center 进入 reaction cross-attention。
- `enzymecage/model.py:291-300`：substrate/reacting-center 与 pocket 的几何 interaction weight 进入 enzyme-compound cross-attention。

因此可以说：

```text
EnzymeCAGE 分数间接包含 pocket/结构/底物/反应中心的兼容性信号。
```

但不能说：

```text
EnzymeCAGE 已经完成了底物 docking；
EnzymeCAGE 直接输出结合难易程度；
EnzymeCAGE 直接输出 kcal/mol 级结合能；
EnzymeCAGE 直接评价 Km/kcat。
```

更准确的中文定义是：

```text
它评价的是“该反应-酶组合像不像训练集中已知可催化组合”的学习型兼容性分数；其中可能间接学习到部分结合、口袋和反应类型匹配信号，但不是显式物理对接分数。
```

### 2.4 AutoDock 应该怎么放

会议纪要/计划里 AutoDock 的定位本来也是辅助项：

- `ENZYMECAGE_LUCAPCYCLE_MEETING_MINUTES_2026-07-03.md:23`：docking score 可作为判断某个酶-底物反应是否可能发生的辅助阈值之一，可用于过滤或降低候选酶排序。
- `ENZYMECAGE_LUCAPCYCLE_MEETING_MINUTES_2026-07-03.md:31`：由模型给出酶促反应发生概率排序，同时可以结合 AutoDock 等对接工具打分作为辅助标准。
- `ENZYMECAGE_ESM3B_REVISED_EXECUTION_PLAN_2026-07-03.md:700-711`：当前工作是 reaction-to-enzyme ranking，AutoDock-style docking scores 是 optional auxiliary feasibility threshold。

建议策略：

```text
主排序：EnzymeCAGE_score
证据来源约束：Rhea/EC/相似反应/实验文献/资产 provenance
可选二级证据：AutoDock-style docking for Top-K
```

不建议当前默认把 AutoDock 作为 hard filter，原因是：

1. EnzymeCAGE 和 AutoDock 回答的是不同问题。EnzymeCAGE 学的是反应-酶配对兼容性；AutoDock 近似评价某个底物 pose/energy。
2. 酶促反应不等于静态结合。底物能结合不代表能催化；docking 分数差也可能是结构、辅因子、金属、水、质子化状态、柔性 pocket 或过渡态没有处理好。
3. docking 需要另行冻结 protocol：结构来源、active-site box、辅因子/金属/水、底物质子化、阈值、融合方式。这些都需要老师/生物化学侧裁定。
4. 我们刚做的按需 D4 小试说明结构/pocket 层本身仍存在覆盖问题；如果 docking 成为默认全量步骤，会引入比 EnzymeCAGE ranking 更重的失败面。

### 2.5 推荐给老师的方案

建议采用三阶段策略：

| 阶段 | 做法 | 说明 |
|---|---|---|
| 默认主线 | `final_score = EnzymeCAGE_score` | 用于大规模候选酶排序，和当前训练/评估目标一致 |
| 可解释增强 | 对 Top-K 做 AutoDock-style docking 注释 | docking score 单列披露，不默认改排名 |
| 谨慎 rerank | 若后续验证 docking 有增益，再作为 soft modifier | 需要老师先批准 protocol 和融合规则 |

暂不建议：

```text
用 AutoDock 替代 EnzymeCAGE；
把 docking score 直接当主分数；
把 docking 差的候选默认 hard delete。
```

如果老师希望验证 docking 是否值得接入，可以做最小 benchmark：

```text
5–10 个强证据反应；
每个反应取 known positive enzyme、EnzymeCAGE Top-K、低分/negative 候选；
固定 docking protocol；
看 docking 是否能区分 positive/negative、是否改善 Top-K、是否大量 false negative、计算成本是否可接受。
```

### 2.6 Q2 当前可给老师的结论

可以这样回复：

```text
EnzymeCAGE 当前 0–1 分数来自 raw logit 的 sigmoid，训练目标是 reaction-enzyme 正负配对分类，评估目标是 AUC/Top-K/MRR 等排序指标。因此它应作为当前反应找酶任务的主排序分数。

这个分数不是 docking score，也不是结合自由能或 Km/kcat；但模型输入包含反应特征、reaction center、酶 pocket-node ESM、GVP 结构特征和几何 interaction，因此可以间接学习到底物/口袋/反应类型兼容性信号。

AutoDock 更适合放在 Top-K 之后作为辅助证据或解释性检查。现阶段不建议直接替代 EnzymeCAGE_score，也不建议默认 hard filter。若老师希望接入 docking，建议先做 5–10 个强证据反应的小 benchmark，冻结 docking protocol 后验证它是否真的提高 Top-K 或减少假阳性。
```

## 3. 当前证据文件

### Q1 按需补 D4 资产

严格 AlphaFill 100 UID 审计：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_100UID_COVERAGE_RESOURCE_PROBE_RERUN1_RETURN_LOCAL_AUDIT_2026-08-03.md
```

P2Rank fallback 审计：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_P2RANK_FALLBACK_COVERAGE_PILOT_RETURN_LOCAL_AUDIT_2026-08-03.md
```

AlphaFoldDB-only + P2Rank 审计：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_ALPHAFOLDDB_ONLY_P2RANK_CONTROL_RETURN_LOCAL_AUDIT_2026-08-03.md
```

失败案例剖析：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_AFDB_ONLY_P2RANK_FAILURE_CASE_ANALYSIS_2026-08-03.md
```

### Q2 分数语义与 AutoDock

详细分析：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/01_Path_Contract_Objective/M3_EnzymeCAGE_Score_Semantics_And_Docking_Policy_2026-08-03/M3_酶筛选模型0_1评分语义与AutoDock辅助策略分析_2026-08-03.md
```

## 4. 仍待补入第三问

第三问 BioTransformer 路径还需要单独回源检查后再写，尤其要把：

```text
输入是什么；
BioTransformer ENVMICRO 如何生成产物；
每个底物输出候选数是否固定；
如何和已知降解路径答案评分；
它与 enviFormer / 弓师兄模型的测试边界如何区分。
```

写成老师能看懂的流程说明，而不是只写函数名或 runner 名。
