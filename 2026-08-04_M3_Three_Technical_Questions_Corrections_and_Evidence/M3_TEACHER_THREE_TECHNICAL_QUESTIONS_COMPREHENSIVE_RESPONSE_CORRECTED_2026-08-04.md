# M3 给黄老师的三个技术问题综合回复草稿

日期：2026-08-03  
状态：发送前审阅版；本稿把三个问题放在同一份老师可读文档里。  
边界：本稿只解释当前已经回源审计过的链路，不把小试结果写成生产合并结果，不把工具输出写成生物学定论。

## 0. 总结

本轮回答三个问题：

1. 如果候选酶有证据但缺少 EnzymeCAGE D4 资产，是否能按需补资产；
2. EnzymeCAGE 的 0–1 分数是否足够，是否需要额外引入 AutoDock 对接分数；
3. 输入一个底物 SMILES 后，BioTransformer ENVMICRO 模块内部如何得到我们使用的预测产物。

结论如下。

第一，按需补 D4 资产链路已经小试走通，可以做成智能体工具，但要分证据等级、fail-closed、只写入隔离 staged assets，不直接污染正式资产。严格 AlphaFill-transplant 8 Å pocket 路线在困难 100 UID 样本中补回 16/100；AlphaFoldDB-only + P2Rank predicted-pocket fallback 在同一困难样本中补回 45/100，其中 29 个是 strict AlphaFill 路线失败后被救回的 UID。成功 UID 已包含 ESM-2 3B、GVP、pocket-node feature 和 isolated EnzymeCAGE loader validation，可以进入后续酶排序模型的临时测试链路。

第二，EnzymeCAGE 当前输出的 0–1 分数应继续作为主排序分数。它是 raw model logit 经 sigmoid 得到的 reaction-enzyme compatibility score，训练目标是反应-酶正负配对分类，评估目标是 AUC、Top-K、MRR 等排序指标。它不是 docking score、结合自由能或 Km/kcat。AutoDock 更适合作为 Top-K 后的可选辅助证据或解释性检查，不建议现在替代主模型分数，也不建议默认 hard filter。

第三，BioTransformer ENVMICRO 不是深度学习产物生成模型，也不是 Rhea/EC/UniProt 查询。它的内部路线更接近“环境生物转化规则系统”：输入底物 SMILES 后，用 CDK 解析成分子结构对象，检查是否适合 EAWAG-BBD/PPS 类环境微生物预测，然后加载 ENVMICRO 规则库，用 SMARTS 判断底物命中哪些 EAWAG_RULE，用 precedence rules 过滤，再用 SMIRKS 反应模板生成产物结构，最后写出产物 SMILES/InChIKey/Reaction ID/Biosystem 等字段。我们 adapter 后续只做 RDKit 规范化、去重和 Top-10 截断。

## 1. Q1：候选酶缺少 D4 资产时怎么办

### 1.1 问题背景

M3-EXT / EC-Rhea / 相似反应扩展中会出现：

```text
反应证据链找到候选酶 UID
→ 但该 UID 缺少当前 EnzymeCAGE D4 资产
→ 因此不能直接送入 EnzymeCAGE geometric ranking
```

老师关心的是：能否像工具链一样，遇到缺失 UID 时现场补齐该酶的结构、口袋和蛋白特征，而不是等待全量酶池重新构建。

本轮小试验证的是：

```text
输入：UniProt UID
输出：隔离 staged D4 assets + loader validation PASS / blocker report
边界：不修改正式生产资产；不声称该酶一定是目标反应真实正例；只验证能否被 EnzymeCAGE loader 吃进去
```

### 1.2 原 EnzymeCAGE 公开路线

回源代码和 README 后，原 EnzymeCAGE 可公开复现的蛋白资产路线大体是：

```text
UniProt / enzyme list
→ AlphaFoldDB / AlphaFill 结构相关资产
→ AlphaFill 预提取 pocket
→ protein feature 构建
→ EnzymeCAGE dataset / loader / ranking
```

证据点：

- `README.md:22-27` 要求下载数据后用 `feature/main.py` 计算 protein feature，并把 pocket 目录传入；
- `README.md:31-32` 说明作者已经运行 AlphaFill 并预提取 enzyme pockets；
- `feature/download_af2_structures.py:14-23` 是 AlphaFoldDB 结构下载逻辑；
- `feature/extract_pocket.py:16` 固定 pocket 半径为 8 Å；
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

### 1.3 三条补资产路线和结果

我们围绕同一批困难 100 UID 做了三条路线。这个 100 UID 是从 current strict 2026 missing-pocket/missing-D4 metadata 中分层抽样，属于失败富集/困难样本，因此结果应解释为 rescue rate，不是全库覆盖率。

#### 路线 A：严格 AlphaFill-transplant 8 Å pocket

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
| `BLOCKED_SEQUENCE_MISSING` | 4 | 实际是 UniProt fetch timeout/unresolved，不应直接解读为确认无序列 |

资源和时间：

```text
16 个 PASS UID 的平均 full D4 loader-valid 时间：51.31 s/UID
PASS UID 的 ESM-2 3B 平均计算时间：30.67 s/UID
GPU peak allocated：约 11.0–11.24 GB
process max RSS max：约 18.39 GB
```

这个时间包括从 UID 到可以被后续 EnzymeCAGE loader 验证的 staged D4 资产，而不是只下载结构或只跑 pocket。

#### 路线 B：可用 3D 结构 + P2Rank predicted-pocket fallback

链路：

```text
UniProt UID
→ 可用 3D 结构
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

重要边界：该 pilot 多数复用 baseline AlphaFill CIF，少量 AlphaFoldDB，因此它证明的是“有可信 3D 结构时，P2Rank predicted-pocket fallback 可以提高覆盖”，不能写成纯 AlphaFoldDB-only。

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

其中：

```text
BLOCKED_AFDB_P2RANK_NO_POCKET
```

不是“P2Rank 数据库里没有 pocket”。P2Rank 是本地/在线预测器，不是 pocket 数据库查询。这一状态表示 AlphaFoldDB 结构拿到了、P2Rank 跑了，但没有产生可用 top predicted pocket residues。

```text
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED
```

表示 AlphaFoldDB API 和常规 v6/v5/v4 PDB/mmCIF URL 都没有拿到可用结构。

失败案例分析显示，43 个 no-pocket 里有 37 个序列长度 ≤120 aa，均值长度约 97.7 aa，中位数 95 aa。pLDDT 均值/中位数并不低，所以主要不像是 AlphaFold 低置信度造成，而更像是小蛋白/短肽或结构表面不形成 P2Rank 可接受的 ligandable pocket。也就是说，这主要是外部结构/pocket 证据或生物物理形态限制，不是 ESM-2 3B/GVP/loader 后段流程断裂。

资源和时间：

```text
45 个 PASS UID 的 warm/batched 平均 full D4 loader-valid 时间：16.34 s/UID
中位数：11.07 s/UID
最大值：89.58 s/UID
PASS stage mean：AFDB fetch 9.11 s，P2Rank 4.28 s，ESM-2 3B 1.01 s，GVP 0.58 s，loader 1.20 s
GPU peak allocated max：11244 MB
process max RSS max：16723 MB
```

保守给老师的工程估计：

```text
warm/batched 工具运行：约 10–20 s/UID；
cold/single-start 单酶运行：建议按约 40–60 s/UID 估计；
GPU 显存按约 11–12 GB 级别预留；
进程内存按约 17–19 GB 级别预留。
```

### 1.4 建议工具策略

建议把按需补资产工具设计成：

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

## 2. Q2：是否需要额外引入 AutoDock 分数

### 2.1 EnzymeCAGE 0–1 分数是什么

EnzymeCAGE 当前输出的 0–1 分数不是 docking score，而是模型学到的 reaction-enzyme compatibility score。

代码证据（官方公开 EnzymeCAGE commit `255a05e167aabc70f6c0322a00702cdc9d6ebfbc`）：

- `enzymecage/model.py:310-315`：模型拼接特征后通过 MLP 输出一个标量；如果 `sigmoid_readout=True`，直接做 sigmoid；
- `enzymecage/model.py:317-328`：predict 阶段如果模型本身没有 sigmoid readout，则对 raw logit 做 sigmoid；
- `enzymecage/base.py:33-40`：evaluate 阶段同样把 raw logit sigmoid 成 0–1 分数后算指标。

因此：

```text
EnzymeCAGE_score = sigmoid(raw model logit)
```

它可以被称为 probability-like score 或 compatibility score，但不能直接叫物理概率、结合自由能或 docking energy。

### 2.2 训练和评估目标

训练代码证据（官方公开 EnzymeCAGE commit `255a05e167aabc70f6c0322a00702cdc9d6ebfbc`）：

- `train.py:113` 使用 `BCEWithLogitsLoss(reduction='none')`；
- `train.py:128-133` 用 `batch.y` 作为 target，并用模型输出和 target 计算 loss；
- `enzymecage/dataset/geometric.py:170-173,310` 中每行样本的标签来自 `Label` 列，并作为 `data.y`。

监督目标是：

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
实验活性值。
```

评估代码也说明它是排序/分类分数：

- `evaluate.py:31-36` 对同一反应下候选酶按预测分数降序排序；
- `evaluate.py:55-62` 计算 Top-1/3/5/10 success rate；
- `enzymecage/base.py:63-69` 计算 Accuracy、AUC、Precision、Recall、F1。

### 2.3 它是否包含结构/结合相关信息

有，但方式是神经网络特征融合，不是显式 docking。

正式配置证据：

说明：`config/train/pretrain_esm2_3b/seed_42.yaml` 不是官方公开 commit `255a05e167aabc70f6c0322a00702cdc9d6ebfbc` 自带配置；官方公开默认训练配置 `config/train/pretrain/seed_42.yaml:1-10` 使用的是 `ESM-C_600M`。这里引用的是我们本项目在 Chenyu/本地同步的 ESM-2 3B corrected-pocket 正式运行配置，SHA256 为 `83e806341a36bad037aef1af5003b3a01c0ac9a23e5d3699ec605a66d3f0639a`，来源由 2026-07-06 至 2026-07-08 的 ESM-2 3B 配置/迁移审计记录支撑。

- `config/train/pretrain_esm2_3b/seed_42.yaml:1-10`：当前模型为 `EnzymeCAGE`，开启 `geo-enhanced-interaction`、`use_structure=True`、`use_drfp=True`、`use_esm=True`，ESM 模型为 `esm2_t36_3B_UR50D`；
- `config/train/pretrain_esm2_3b/seed_42.yaml:27-33`：使用 reaction DRFP、GVP、ESM-2 3B protein-level、ESM pocket-node、molecule conformation、reaction center 等特征。

模型代码证据：

- `enzymecage/model.py:250-258`：GVP 结构输出和 pocket-node ESM feature 拼接为 enzyme pocket 表示；
- `enzymecage/model.py:267-275`：蛋白节点坐标距离用于 geometry attention bias；
- `enzymecage/model.py:277-285`：底物/产物 reacting center 进入 reaction cross-attention；
- `enzymecage/model.py:291-300`：substrate/reacting-center 与 pocket 的几何 interaction weight 进入 enzyme-compound cross-attention。

所以可以说：

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

### 2.4 AutoDock 的建议定位

建议策略：

```text
主排序：EnzymeCAGE_score
证据来源约束：Rhea/EC/相似反应/实验文献/资产 provenance
可选二级证据：AutoDock-style docking for Top-K
```

不建议当前默认把 AutoDock 作为 hard filter，原因是：

1. EnzymeCAGE 和 AutoDock 回答的是不同问题。EnzymeCAGE 学的是反应-酶配对兼容性；AutoDock 近似评价某个底物 pose/energy；
2. 酶促反应不等于静态结合。底物能结合不代表能催化；
3. docking 需要另行冻结 protocol：结构来源、active-site box、辅因子/金属/水、底物质子化、阈值、融合方式；
4. 按需 D4 小试说明结构/pocket 层本身仍存在覆盖问题；如果 docking 成为默认全量步骤，会引入更重的失败面。

如果老师希望验证 docking 是否值得接入，可以做最小 benchmark：

```text
5–10 个强证据反应；
每个反应取 known positive enzyme、EnzymeCAGE Top-K、低分/negative 候选；
固定 docking protocol；
看 docking 是否能区分 positive/negative、是否改善 Top-K、是否大量 false negative、计算成本是否可接受。
```

## 3. Q3：输入一个底物 SMILES 后，BioTransformer ENVMICRO 内部如何得到预测产物

### 3.1 先明确老师问的不是 wrapper

本问回答的是 BioTransformer ENVMICRO 模块内部机制，不是我们外层怎么运行、怎么打分。

我们外层执行命令是：

```text
java -jar <biotransformer-3.0.0.jar> -k pred -b env -ismi <parent_smiles> -ocsv <case_output_csv> -s 1
```

但老师真正关心的是：

```text
一个 parent SMILES 进入 `-b env` / ENVMICRO 后，BioTransformer 如何生成产物候选？
```

### 3.2 源码身份

源码核查对象：

```text
repository=https://github.com/Wishartlab-openscience/Biotransformer.git
commit=7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
module=BioTransformer 3.0 ENVMICRO / environmental microbial biotransformation
```

该 commit 与我们 HPC 返回包记录的 BioTransformer 3.0 ENVMICRO 工具身份一致。

源码证据：

- `src/main/java/executable/BiotransformerExecutable.java:56-64`：`env` 和 `envmicro` 都映射到 `Biotransformer.bType.ENV`；
- `src/main/java/executable/BiotransformerExecutable.java:957-965`：`bType.ENV` 单分子路径实例化 `EnvMicroBTransformer` 并调用 `simulateEnvMicrobialDegradationAndSaveToCSV(...)`；
- `src/main/java/biotransformer/btransformers/EnvMicroBTransformer.java:243-245`：先调用 `applyEnvMicrobialTransformationsChain(...)`，再保存 CSV。

### 3.3 内部路线总览

老师可读版路线如下：

```text
输入 parent SMILES
→ CDK 解析成 IAtomContainer 分子对象
→ ENVMICRO / PPS-style 有效性检查
→ 加载 ENVMICRO knowledgebase
→ 对底物做结构预处理和 chemical class 标注
→ 遍历 ENVMICRO 的泛化环境细菌 enzyme/reaction set
→ 用 reaction SMARTS 判断底物是否命中某条 EAWAG_RULE
→ 用 excluded SMARTS 排除不适用反应
→ 用 reaction precedence rules 过滤冲突或低优先级规则
→ 对保留规则应用 SMIRKS 结构变换
→ 拆分连通组，去除无意义小分子，规范化和去重
→ 计算产物 InChI / InChIKey / SMILES / metadata
→ 输出 BioTransformer vendor CSV
→ 我们 adapter 再做 RDKit canonicalization、dedup、Top-10
```

一句话解释：

```text
SMARTS 决定“底物哪里能反应”；
SMIRKS 决定“命中后结构怎么改成产物”。
```

### 3.4 有效性检查

ENVMICRO 不是对所有 SMILES 都预测。它先检查输入分子是否适合 EAWAG-BBD/PPS 类环境微生物预测域。

源码证据：

- `EnvMicroBTransformer.java:196-217`：只有 `ChemStructureExplorer.isPpsValid(target)` 通过时才进入环境微生物转化；
- `ChemStructureExplorer.java:1256-1277`：`isPpsValid` 要求分子不是 PPS cofactor、不是 PPS dead-end compound、分子量小于 1000 Da、含碳、不是 mixture，且只包含 H/C/N/O/P/S/F/Cl/Br/I 等允许元素。

这解释了为什么某些输入可能没有预测：不是工具“没想出来”，而是前置规则认为不适合进入该预测域。

### 3.5 ENVMICRO 规则库

`EnvMicroBTransformer()` 构造函数指定 biosystem 为 `ENVMICRO`，并加载 enzyme list 和 reaction list。

源码证据：

- `EnvMicroBTransformer.java:44-49`：`super(BioSystemName.ENVMICRO)`，然后 `setEnzymesList()`、`setReactionsList()`；
- `EnvMicroBTransformer.java:56-79`：从 biosystem 里取有 reaction set 的 enzymes，并把 `bSystem.getReactionsHash()` 放入 ENVMICRO reaction list；
- `BioSystem.java:113-146`：加载 enzymes、metabolic reactions、enzyme-reaction mappings、biosystem enzymes、reaction occurrence ratios、reaction precedence rules。

ENVMICRO 数据库文件包括：

```text
database/ENVMICRO/enzymes.json
database/ENVMICRO/biosystemEnzymes.json
database/ENVMICRO/enzymeReactions.json
database/ENVMICRO/metabolicReactions.json
database/ENVMICRO/biosystemsReactionORatios.json
database/ENVMICRO/reactionPrecedenceRules.json
database/ENVMICRO/pathways.json
```

这些文件头部说明 ENVMICRO 模块使用 EAWAG Biodegradation and Biocatalysis Database / enviPath 相关数据和许可。

重要边界：

```text
ENVMICRO 里实际 biosystem enzyme 是 `UNSPECIFIED_ENVIRONMENTAL_BACTERIAL_ENZYME`。
```

证据：

- `database/ENVMICRO/biosystemEnzymes.json` 中 `ENVMICRO` 只列出 `UNSPECIFIED_ENVIRONMENTAL_BACTERIAL_ENZYME`；
- `database/ENVMICRO/enzymes.json` 中该 enzyme 的 acceptedName 是 `Unspecified environmental bacterial enzyme`，`uniprot_ids` 为空。

因此 BioTransformer 输出 CSV 中的 `Enzyme(s)=Unspecified environmental bacterial enzyme` 不能解释为找到了具体 UniProt 酶，也不能直接作为 EnzymeCAGE 候选酶 UID。

### 3.6 规则匹配和产物生成

进入 `metabolizeWithEnzymes(...)` 后，核心是三件事。

第一，分子预处理：

- `Biotransformer.java:947-962`：如果 `preprocess=true`，调用 `ChemStructureManipulator.preprocessContainer(target)` 并转显式氢；
- `ChemStructureManipulator.java:68-99`：处理原子类型、芳香性、2D 坐标。

第二，reaction SMARTS 约束匹配：

- `Biotransformer.java:1001-1016`：遍历 reaction set；如果 `ChemStructureExplorer.compoundMatchesReactionConstraints(m, starget)` 为真，就加入 matched reactions；
- `ChemStructureExplorer.java:257-299`：检查底物是否匹配该 reaction 的 `reactantsSMARTS`，并且不匹配 `excludedReactantsSMARTS`。

第三，precedence 过滤和 SMIRKS 转换：

- `Biotransformer.java:1021-1029`：`filter=true` 时调用 `MReactionsFilter.filterReactions(...)`；
- `MReactionsFilter.java:87-203`：根据 reaction precedence rules 过滤；
- `MetabolicReaction.java:104-112`：每个 reaction 保存 `smirks`、`reactantsSMARTS`、`excludedReactantsSMARTS`，并解析为 `SMIRKSReaction`；
- `Biotransformer.java:1044-1049`：对 filtered reaction 调用 `generateAllMetabolitesFromAtomContainer(...)`；
- `Biotransformer.java:207-259`：用 `applyTransformationWithSingleCopyForEachPos(...)` 对命中位点应用 SMIRKS，随后拆分连通组、去掉不必要小分子、预处理产物、去重。

所以 BioTransformer ENVMICRO 的“预测”来自：

```text
EAWAG/IUMBBD/enviPath 来源的环境生物转化规则
+ SMARTS/SMIRKS 子结构匹配与反应变换
+ reaction precedence / occurrence ratio 规则
```

不是：

```text
神经网络自由生成；
Rhea/EC/UniProt 查询；
已知路径数据库 exact lookup；
人体 CYP/Phase II 模块。
```

### 3.7 原始输出和我们 adapter 的处理

产物生成后，BioTransformer 把 `Biotransformation` 对象转换成带 transformation metadata 的产物集合，并写 CSV。

源码证据：

- `Biotransformer.java:1424-1747`：为产物补充 InChI、InChIKey、SMILES、理化属性、Reaction、Reaction ID、Enzyme(s)、Biosystem、Precursor 信息；
- `Biotransformer.java:1827-1830`：调用 `extractProductsFromBiotransformationsWithTransformationData(...)` 后写出 CSV。

我们 adapter 只做后处理：

```text
读取 BioTransformer vendor CSV 行
→ RDKit parse
→ canonical SMILES / InChIKey
→ 去重
→ 按 vendor CSV 行顺序保留 rank
→ 最多 Top-10
→ raw_score=null
→ score_semantics=absent
```

因此不能说 BioTransformer 的 rank 是概率，也不能把 `Reaction ID` 或 `Enzyme(s)` 当成真实 Rhea/EC/UniProt 证据。当前它在我们流程中的合理定位是：

```text
污染物 parent SMILES → 一代环境转化产物候选
```

后续如果要找酶，还需要：

```text
parent → product pair
→ Rhea/EC/相似反应/文献证据
→ 候选酶生成
→ EnzymeCAGE ranking
```

## 4. 当前证据文件

### Q1 按需补 D4 资产

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_100UID_COVERAGE_RESOURCE_PROBE_RERUN1_RETURN_LOCAL_AUDIT_2026-08-03.md
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_P2RANK_FALLBACK_COVERAGE_PILOT_RETURN_LOCAL_AUDIT_2026-08-03.md
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_ALPHAFOLDDB_ONLY_P2RANK_CONTROL_RETURN_LOCAL_AUDIT_2026-08-03.md
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_AFDB_ONLY_P2RANK_FAILURE_CASE_ANALYSIS_2026-08-03.md
```

### Q2 分数语义与 AutoDock

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/01_Path_Contract_Objective/M3_EnzymeCAGE_Score_Semantics_And_Docking_Policy_2026-08-03/M3_酶筛选模型0_1评分语义与AutoDock辅助策略分析_2026-08-03.md
```

### Q3 BioTransformer ENVMICRO

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/01_Path_Contract_Objective/M3_Teacher_Three_Technical_Questions_Response_2026-08-03/M3_TEACHER_TECHNICAL_QUESTION_Q3_BIOTRANSFORMER_ENVMICRO_INTERNAL_ROUTE_DRAFT_2026-08-03.md
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/01_Path_Contract_Objective/M3_Teacher_Three_Technical_Questions_Response_2026-08-03/M3_Q3_BIOTRANSFORMER_ENVMICRO_SOURCE_AND_JAR_IDENTITY_EVIDENCE_2026-08-04.md
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_P1_2_1_SMALL_POLLUTANT_STRICT_V0_1_BIOTRANSFORMER_ENVMICRO_RETURN_SCORING_AUDIT_2026-07-29.md
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_P1_2_1_THREE_TOOL_VALID_SINGLE_PARENT_BIOTRANSFORMER_ENVMICRO_PREDICTION_R4_RETURN_LOCAL_AUDIT_2026-07-28.md
```
