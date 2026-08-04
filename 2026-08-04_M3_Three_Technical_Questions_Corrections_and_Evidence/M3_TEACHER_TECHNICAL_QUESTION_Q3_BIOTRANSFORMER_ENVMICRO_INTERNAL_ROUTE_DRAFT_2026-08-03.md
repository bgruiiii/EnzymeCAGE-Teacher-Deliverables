# M3 给黄老师的技术问题回复草稿 Q3：BioTransformer ENVMICRO 内部产物生成路线

日期：2026-08-03  
状态：draft；本稿回答“输入一个底物 SMILES 后，在 BioTransformer ENVMICRO 模块内部经历什么，最终得到我们使用的预测产物输出”。  
源码核查对象：`Wishartlab-openscience/Biotransformer`，commit `7149f7ec6b2f32f9f789bab53aa4a71db49e59e2`，与我们 HPC 返回包记录的 `BioTransformer 3.0 ENVMICRO` 工具身份一致。

## 0. 先说结论

BioTransformer ENVMICRO 这一路不是深度学习产物预测模型，也不是先去数据库查“这个底物已有哪个路径”。它更准确地说是：

```text
输入 SMILES
→ CDK 解析成分子对象
→ 检查是否适合 EAWAG-BBD/PPS 环境微生物预测
→ 加载 ENVMICRO 规则库
→ 用规则库里的 SMARTS 判断哪些 EAWAG_RULE 可作用于该底物
→ 用反应优先级规则过滤
→ 用对应 SMIRKS 反应变换生成产物结构
→ 计算产物 InChI/InChIKey/SMILES/理化属性
→ 写出 BioTransformer vendor CSV
→ 我们的 adapter 再 RDKit 规范化、去重、最多保留 Top-10
```

所以它的“预测”主要来自：

```text
EAWAG/IUMBBD/enviPath 来源的环境生物转化规则 + SMARTS/SMIRKS 子结构匹配与反应变换 + reaction precedence / occurrence ratio 规则
```

而不是：

```text
神经网络从训练集自由生成；
Rhea/EC/UniProt 查询；
已知路径数据库 exact lookup；
人体 CYP/Phase II 模块。
```

## 1. CLI 怎么进入 ENVMICRO 模块

我们执行的命令固定为：

```text
java -jar <biotransformer-3.0.0.jar> -k pred -b env -ismi <parent_smiles> -ocsv <case_output_csv> -s 1
```

源码证据：

- `src/main/java/executable/BiotransformerExecutable.java:56-64` 中，`env` 和 `envmicro` 都映射到 `Biotransformer.bType.ENV`。
- `src/main/java/executable/BiotransformerExecutable.java:957-965` 中，如果 `bType.ENV` 且输入是单个分子，则实例化 `EnvMicroBTransformer`，并调用：

```java
ebt.simulateEnvMicrobialDegradationAndSaveToCSV(singleInput, true, true, nrOfSteps, scoreThreshold, outputF, annotate);
```

我们本轮的 `-s 1` 对应 `nrOfSteps=1`，因此只做一代转化，不展开多步完整路径。

## 2. 输入 SMILES 首先变成什么

`-ismi <parent_smiles>` 进入 BioTransformer CLI 后，会被解析成 CDK 的 `IAtomContainer` 分子对象。后续所有判断和反应变换都不再是字符串层面直接拼接，而是在 CDK/SMIRKS 结构对象上做。

在 ENVMICRO 单分子 CSV 输出路径里，调用链是：

```text
BiotransformerExecutable
→ EnvMicroBTransformer()
→ simulateEnvMicrobialDegradationAndSaveToCSV(...)
→ applyEnvMicrobialTransformationsChain(...)
→ metabolizeWithEnzymesBreadthFirst(...)
→ metabolizeWithEnzymes(...)
→ generateAllMetabolitesFromAtomContainer(...)
→ saveBioTransformationProductsToCSV(...)
```

源码证据：

- `EnvMicroBTransformer.java:243-245`：`simulateEnvMicrobialDegradationAndSaveToCSV` 先调用 `applyEnvMicrobialTransformationsChain`，再保存 CSV。
- `EnvMicroBTransformer.java:191-207`：`applyEnvMicrobialTransformationsChain` 对输入分子做有效性判断，通过后调用 `metabolizeWithEnzymesBreadthFirst`。

## 3. ENVMICRO 会先做“可预测性/有效性”检查

ENVMICRO 不是对所有 SMILES 都预测。它先检查输入分子是否符合 EAWAG-BBD/PPS 类环境微生物预测条件。

源码证据：

- `EnvMicroBTransformer.java:196-217`：只有 `ChemStructureExplorer.isPpsValid(target)` 通过时才进入环境微生物转化；否则报错说明该化合物必须是有机物、非混合物、非 cofactor/dead-end compound、分子量不超过 1000 Da 等。
- `ChemStructureExplorer.java:1256-1277`：`isPpsValid` 的条件包括：

```text
不是 PPS cofactor；
不是 PPS dead-end compound；
natural exact mass < 1000；
含碳；
不是 mixture；
只包含 H/C/N/O/P/S/F/Cl/Br/I 等允许原子集合。
```

这解释了为什么某些输入可能没有预测：不是工具“没想出来”，而是前置规则认为不适合进入该环境微生物预测域。

## 4. ENVMICRO 构造时加载了哪些规则资产

`EnvMicroBTransformer()` 构造函数会指定 biosystem 为 `ENVMICRO`，然后建立 enzyme list 和 reaction list。

源码证据：

- `EnvMicroBTransformer.java:44-49`：`super(BioSystemName.ENVMICRO)`，然后 `setEnzymesList()`、`setReactionsList()`。
- `EnvMicroBTransformer.java:56-79`：从 biosystem 里取有 reaction set 的 enzymes，并把 `bSystem.getReactionsHash()` 放入 ENVMICRO reaction list。
- `BioSystem.java:113-146`：加载 biosystem-specific knowledgebase，包括 enzymes、metabolic reactions、enzyme-reaction mappings、biosystem enzymes、reaction occurrence ratios、reaction precedence rules。

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

非常重要的边界：

```text
ENVMICRO 里实际 biosystem enzyme 是 `UNSPECIFIED_ENVIRONMENTAL_BACTERIAL_ENZYME`。
```

证据：

- `database/ENVMICRO/biosystemEnzymes.json` 中 `ENVMICRO` 只列出 `UNSPECIFIED_ENVIRONMENTAL_BACTERIAL_ENZYME`。
- `database/ENVMICRO/enzymes.json` 中该 enzyme 的 acceptedName 是 `Unspecified environmental bacterial enzyme`，`uniprot_ids` 为空。

因此 BioTransformer 输出 CSV 里的：

```text
Enzyme(s)=Unspecified environmental bacterial enzyme
Biosystem=ENVMICRO
```

不能解释为找到了具体 UniProt 酶，也不能直接作为 EnzymeCAGE 候选酶 UID。它只是规则库里的泛化环境细菌酶/规则组标签。

## 5. 它怎么判断哪些反应规则适用于这个底物

进入 `metabolizeWithEnzymes(...)` 后，大致做三层筛选。

### 5.1 分子预处理

源码证据：

- `Biotransformer.java:947-962`：如果 `preprocess=true`，会调用 `ChemStructureManipulator.preprocessContainer(target)`，并转显式氢。
- `ChemStructureManipulator.java:68-99`：`preprocessContainer` 会感知原子类型、处理芳香性、生成 2D 坐标。

### 5.2 enzyme/substrate specificity 粗筛

源码证据：

- `Biotransformer.java:983-989`：先给底物分配 chemical classes，然后对每个 enzyme 调用 `esspredictor.isValidSubstrate(...)`。
- `ESSpecificityPredictor.java:154-182`：对 CYP 等人体酶会有专门逻辑；但对其他一般 enzyme，当前逻辑返回 `validSubstrate=true`。

对于 ENVMICRO，因为主要 enzyme 是 `UNSPECIFIED_ENVIRONMENTAL_BACTERIAL_ENZYME`，这一步基本不是机器学习筛选；主要实质筛选在下一步 reaction SMARTS/SMIRKS 规则匹配。

### 5.3 reaction SMARTS 约束匹配

源码证据：

- `Biotransformer.java:1001-1016`：对通过 enzyme 粗筛的 enzyme，遍历其 reaction set；如果 `ChemStructureExplorer.compoundMatchesReactionConstraints(m, starget)` 为真，就把该反应加入 matched reactions。
- `ChemStructureExplorer.java:257-299`：`compoundMatchesReactionConstraints` 会检查：

```text
底物是否匹配该 reaction 的 reactantsSMARTS；
如果该 reaction 有 excludedReactantsSMARTS，底物不能匹配这些排除模式。
```

这一步是核心：输入底物的子结构如果命中某条 EAWAG_RULE 的 SMARTS 条件，就认为这条规则有资格作用于该底物。

## 6. 匹配到的反应还会被 precedence rules 过滤

匹配到很多反应后，如果 `filter=true`，BioTransformer 会调用 `MReactionsFilter.filterReactions(...)`。

源码证据：

- `Biotransformer.java:1021-1029`：`filter=true` 时使用 `this.mRFilter.filterReactions(matchedReactions)`。
- `MReactionsFilter.java:87-203`：根据 reaction precedence rules 过滤 reaction。
- `BioSystem.java:367-390`：从 `reactionPrecedenceRules.json` 里加载 ENVMICRO 的 `relative` 和 `strict` precedence rules。

老师可读解释：

```text
如果一个底物同时匹配多条环境转化规则，BioTransformer 不一定全部保留；
它会用 ENVMICRO 的 reaction precedence rules 去保留更优先/更合适的规则，避免低优先级规则和高优先级规则重复或冲突。
```

这也是为什么同一个底物输出的产物数量不固定。

## 7. 它怎么由“反应规则”生成“产物结构”

对过滤后的每条 reaction，BioTransformer 用该 reaction 的 SMIRKS 做化学结构变换。

源码证据：

- `MetabolicReaction.java:104-112`：每个 `MetabolicReaction` 包含 `smirks`、`reactantsSMARTS`、`excludedReactantsSMARTS`，并把 reactionSMIRKS 解析成 `SMIRKSReaction`。
- `Biotransformer.java:1044-1049`：对每个 filtered reaction，调用 `generateAllMetabolitesFromAtomContainer(...)`。
- `Biotransformer.java:182-190`：`generateAllMetabolitesFromAtomContainer(molecule, MetabolicReaction, ...)` 实际取 `mReaction.getSmirksReaction()`。
- `Biotransformer.java:207-259`：用 `smrkMan.applyTransformationWithSingleCopyForEachPos(...)` 对反应位点应用 SMIRKS，生成候选产物；随后拆分连通组、去掉不必要小分子、预处理产物、去重。

简化说：

```text
SMARTS 决定“这个底物哪里能反应”；
SMIRKS 决定“命中后结构怎么改成产物”。
```

例如 ENVMICRO 的 `metabolicReactions.json` 中每条 `EAWAG_RULE_BT...` 都有：

```text
smirks
smarts
excludedReactantSmarts
btmrID
```

因此 BioTransformer 是按规则库里的反应模板生成产物，而不是从语言模型或神经网络里直接吐出 SMILES。

## 8. score / rank 在 BioTransformer 原始输出里的含义

对每个成功生成产物的 reaction，BioTransformer 会计算一个 score。

源码证据：

- `Biotransformer.java:1060-1065`：如果底物本身已有 `Score`，则乘以该 reaction 在 biosystem 中的 occurrence ratio；否则 score 等于 `bSystem.getReactionsORatios().get(j.name)`。
- `BioSystem.java:328-345`：reaction occurrence ratios 来自 `biosystemsReactionORatios.json`。

但需要注意：我们最终 normalized JSONL 里没有使用 BioTransformer score 作为置信度。

我们这轮 adapter 的规范化策略是：

```text
读取 BioTransformer vendor CSV 行；
RDKit parse；
canonical SMILES / InChIKey；
去重；
按 vendor CSV 行顺序保留 rank；
最多 Top-10；
raw_score=null；
score_semantics=absent；
rank_semantics=vendor_csv_row_order_deduplicated_adapter_rank_not_native_confidence。
```

所以给老师不能说：

```text
BioTransformer rank 1 的概率最高。
```

更准确是：

```text
我们按 BioTransformer vendor CSV 输出顺序，经 adapter 规范化和去重后形成 Top-K 产物候选；当前没有可解释为概率的原生置信度分数进入评分。
```

## 9. 输出 CSV 是怎么写出来的

产物生成后，BioTransformer 把 `Biotransformation` 对象转换为带 transformation metadata 的产物集合，再写 CSV。

源码证据：

- `EnvMicroBTransformer.java:243-245`：`simulateEnvMicrobialDegradationAndSaveToCSV` 调用 `saveBioTransformationProductsToCSV`。
- `Biotransformer.java:1424-1747`：`extractProductsFromBiotransformationsWithTransformationData` 为产物补充 InChI、InChIKey、SMILES、理化属性、Reaction、Reaction ID、Enzyme(s)、Biosystem、Precursor 信息。
- `Biotransformer.java:1827-1830`：`saveBioTransformationProductsToCSV` 调用 `extractProductsFromBiotransformationsWithTransformationData`，再用 `FileUtilities.saveAtomContainerSetToCSV(...)` 写出。

因此我们看到的 BioTransformer vendor CSV 字段：

```text
SMILES
InChIKey
Reaction
Reaction ID
Enzyme(s)
Biosystem
Precursor SMILES
Precursor InChIKey
```

就是在这一阶段被写出的。

## 10. 用一条最小链路给老师解释

可以这样给老师讲：

```text
BioTransformer ENVMICRO 输入一个污染物 SMILES 后，首先用 CDK 把 SMILES 解析为分子结构对象，并检查该分子是否适合环境微生物 PPS/EAWAG-BBD 类预测。通过后，模块加载 ENVMICRO 规则库：其中包括 EAWAG_RULE 的 SMARTS/SMIRKS 反应模板、反应排除 SMARTS、反应优先级规则和 occurrence ratio。

随后程序遍历 ENVMICRO 中的泛化环境细菌 enzyme/reaction set。对每条规则，先用 SMARTS 判断底物是否有可反应子结构，并排除 excluded SMARTS 命中的情况；如果多条规则同时命中，再用 reaction precedence rules 做过滤。保留下来的规则用 SMIRKS 在所有可反应位点生成产物结构，生成后去掉无意义小分子、拆分连通组、规范化并去重，最后写出产物 SMILES/InChIKey/Reaction ID/Biosystem 等字段。

所以 BioTransformer ENVMICRO 的结果不是 Rhea/EC/UniProt 查询结果，也不是具体酶 UID 预测，而是基于 EAWAG-BBD/enviPath 来源环境生物转化规则的结构模板预测。我们后处理时只取产物结构做 RDKit 规范化、去重和 Top-10 评分。
```

## 11. 这对我们项目意味着什么

对我们来说，BioTransformer ENVMICRO 的合理定位是：

```text
污染物 parent SMILES → 一代环境转化产物候选
```

它适合作为后续反应找酶链路的上游：

```text
parent pollutant
→ BioTransformer ENVMICRO 预测 product candidates
→ 形成 parent → product pseudo-reaction / candidate reaction
→ 再做 Rhea/EC/相似反应/候选酶生成
→ EnzymeCAGE ranking
```

但它本身不能替代：

```text
反应证据回源；
Rhea/EC 归属；
候选酶 UID 生成；
EnzymeCAGE 反应找酶评分。
```

## 12. 证据文件和源码定位

本轮执行证据：

```text
04_Local_Review_Audits/ENZYMECAGE_M3_P1_2_1_SMALL_POLLUTANT_STRICT_V0_1_BIOTRANSFORMER_ENVMICRO_RETURN_SCORING_AUDIT_2026-07-29.md
04_Local_Review_Audits/ENZYMECAGE_M3_P1_2_1_THREE_TOOL_VALID_SINGLE_PARENT_BIOTRANSFORMER_ENVMICRO_PREDICTION_R4_RETURN_LOCAL_AUDIT_2026-07-28.md
```

源码定位，commit `7149f7ec6b2f32f9f789bab53aa4a71db49e59e2`：

```text
src/main/java/executable/BiotransformerExecutable.java
src/main/java/biotransformer/btransformers/EnvMicroBTransformer.java
src/main/java/biotransformer/btransformers/Biotransformer.java
src/main/java/biotransformer/biosystems/BioSystem.java
src/main/java/biotransformer/transformation/MetabolicReaction.java
src/main/java/biotransformer/transformation/MReactionsFilter.java
src/main/java/biotransformer/utils/ChemStructureExplorer.java
src/main/java/biotransformer/utils/ChemStructureManipulator.java
src/main/java/biotransformer/esaprediction/ESSpecificityPredictor.java
database/ENVMICRO/*.json
```

