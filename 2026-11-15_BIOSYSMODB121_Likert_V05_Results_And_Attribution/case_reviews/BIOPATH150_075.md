# BIOPATH150_075：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-chlorobenzoate degradation

污染物：4-Chlorobenzoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 65 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 59 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 59.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 44.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 60.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 44 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`c8a8976851effd1f3a2c4e853177d50e64d3cce7436a0a828d00e4d346c29e58`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 题面指定的路线名称原样保留，答案给出10步，每步均含底物/产物、酶/EC与对应微生物；S1-S4对应gold四步主链并在S4到达3,4-二羟基苯甲酸（protocatechuate），两个菌株profile各含15项性状。主要不足是若按题面‘每步主底物/主产物均给SMILES’严格执行，S1产物、S2底物与产物、S3底物等CoA中间体SMILES为null，另有若干下游步骤SMILES缺失；下游β-酮己二酸延伸超出gold四步终点，但按P29不因此扣D1。总体大部分必要内容完整、关联清楚，属7-8档，取8。

<details><summary>V0.4理由与本行变化背景</summary>

8档：主要模块均有实质交付——10步主链、每步酶与微生物、两个profile各15项性状、route_scope、evidence_registry、uncertainties齐备，route名称原样回填。扣分点：多个主产物SMILES为null（4-chlorobenzoyl-CoA、4-hydroxybenzoyl-CoA、4-carboxymuconolactone、3-oxoadipyl-CoA、succinyl-CoA、acetyl-CoA），CBS3的TaxID为null；属字段级遗漏而非模块缺失，故不进入9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：gold四步主链及终点3,4-Dihydroxybenzoate，用于核对必答步覆盖和范围；不表示答案额外下游步骤均必答
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：本题路线根物4-Chlorobenzoate与gold终点3,4-Dihydroxybenzoate的身份范围
- ANSWER_TEXT / ANSWER：答案实际交付的10步、2个菌株profile及15项性状字段

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> S1-S4与gold主链的方向和化学一致：4-chlorobenzoate→4-chlorobenzoyl-CoA（EC 6.2.1.33），水解脱氯→4-hydroxybenzoyl-CoA（EC 3.8.1.7），硫酯水解→4-hydroxybenzoate（EC 3.1.2.23），羟化→protocatechuate（EC 1.14.13.2）。主链原子关系和辅因子基本合理；S5-S10的β-酮己二酸延伸化学上连续，S4后超出本题gold终点，按P29不额外加分也不扣D2。局部H+/CoA currency省略、个别SMILES为null属于小问题，不改变主要结论。程序allowed_ranges.D2=&#91;1,8&#93;且nine_ten_eligible=false，故取7-8档中的8。

<details><summary>V0.4理由与本行变化背景</summary>

9档：S1-S4与gold的fcb主链逐步一致（4-chlorobenzoate→4-chlorobenzoyl-CoA→4-hydroxybenzoyl-CoA→4-hydroxybenzoate→protocatechuate）；S5-S10为标准β-酮己二酸途径延续，方向、连接与主碳流合理，辅因子多数在列。S6/S7的SMILES为null不构成化学断裂；答案延伸至TCA超出gold终点但题面未指定终点，按量表四.2不因此扣D2覆盖率。少量H+等小项未列，不影响主结论。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：gold S01-S04的底物/产物、方向与主链连接，用于核对S1-S4化学对应；不把额外下游步骤纳入必答主链
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：gold接受EC 1.14.13.2、3.1.2.23、6.2.1.33、3.8.1.7；不证明具体蛋白实验活性或下游额外酶
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：路线根物4-Chlorobenzoate与gold终点3,4-Dihydroxybenzoate，用于界定主链终点

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 四个必答步的酶名/EC 可人工对齐 accepted sets：S1 6.2.1.33、S2 3.8.1.7、S3 3.1.2.23、S4 1.14.13.2；无已核 KEY 失败。程序事实仍为 ROUTE_HOLD_REPRESENTATION/UNRESOLVED，显式 EC 官方记录和 S01/S03 表示等价未获 E0 核验，故在允许区间 &#91;1,8&#93; 取 7，而非 8–10。

<details><summary>V0.4理由与本行变化背景</summary>

8档：S1-S10的酶名、EC与反应类型总体对应正确；S1-S4的EC（6.2.1.33、3.8.1.7、3.1.2.23、1.14.13.2）由gold直接支持；S5-S10为标准β-酮己二酸酶系。S10 EC 2.3.1.174答案自述未经数据库核对，且本案E0无对应记录，故若干EC仍需确认，取8而非9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：支持 four required enzyme names/ECs 的 G4 参考对应；不证明具体蛋白实验活性或官方 EC 核验。
- GOLD_SLICE / reaction_gold.tsv：支持目标反应方向/参与者的参考记录；S01/S03 表示边界仍未裁决。
- ANSWER_TEXT / ANSWER：答案交付的酶名/EC；用于与 accepted sets 对比，不等于外部来源已核。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> CBS3 与 gold STEP 的 S02/S03/S04 名称/菌株一致，且 organism_gold 的 PATHWAY_COMPLETE 含 72586；S4 的 P. putida 与 gold S01 的物种级 P. putida 对齐，但答案使用 KT2440/TaxID 160488 的 strain 级身份未在 E0 核实。无跨属/无关类群或编造身份证据，按物种级支持 strain 级声称的粒度不足在 7 档内扣，不 cap。

<details><summary>V0.4理由与本行变化背景</summary>

7档：S1-S3的Pseudomonas sp. CBS3在gold中为EXACT匹配，身份与单步能力可靠；S4-S10使用Pseudomonas putida KT2440，gold有P. putida物种级记录支持该物种的4-hydroxybenzoate hydroxylase与β-酮己二酸途径，但KT2440菌株级TaxID/能力属菌株级声称，存在物种级记录支持菌株级声称的粒度不足（D3b身份阶梯①），按通常7档处理，不cap。CBS3的TaxID留null属完整性不足，不是经核实身份错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：支持 CBS3 在 S02/S03/S04 的 STEP 身份及 72586 的 PATHWAY_COMPLETE 行；P. putida 仅到物种级 303，不核验 KT2440/160488。
- GOLD_SLICE / trait_gold.tsv：支持部分 P. putida 物种级性状；CBS3 多数性状为 UNKNOWN，不能支持 strain 级具体值。
- ANSWER_TEXT / ANSWER：答案交付的身份/菌株声称；不自动证明 TaxID 或完整能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 两个 profile 都返回了 15 项性状。P. putida 的杆状、革兰氏阴性、可运动、不产芽孢及部分底物/降解相关性状与 gold 物种级观察相容；但 CBS3 多个 F1/F6–F13 值来自内部知识/属级推测，KT2440 的 F2 最适 30°C、F5 DSM 6125、F14 NC_002947 等 strain 级值未在 E0 核实。部分准确且适用，但关键项证据不足，取 5–6 档中的 6。

<details><summary>V0.4理由与本行变化背景</summary>

8档：ORG_002（KT2440）的主要性状与gold P. putida物种级代表记录/标准菌株知识一致——好氧、O2为末端受体、可运动、杆状、革兰氏阴性、不产芽孢、芳香族降解、pca酶系、基因组NC_002947（对KT2440常见）；ORG_001（CBS3）的关键降解性状（以4-氯苯甲酸为碳源、具fcbA/B/C、可进一步矿化）与gold路径步骤相容，若干形态/运动性明确标为属级推测。F5 DSM 6125、F14 NC_002947及部分CBS3性状无E0记录，故取8而非9；缺失的pH/盐度等按D1完整性处理，不在D4重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：支持 P. putida 部分物种级性状；CBS3 多数性状为 UNKNOWN，不支持答案填写的 strain 级值。
- GOLD_SLICE / trait_scoreability_mask.tsv：标明哪些性状为 observed_accuracy 或 completeness_only；CBS3 多为 completeness_only。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv：标明 pH/salinity/temperature 等多值/参考待裁决子字段；支持局部未核登记。
- ANSWER_TEXT / ANSWER：答案交付的性状值与 confidence；不能把 internal knowledge 回填为观测。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry 四条全部为 INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 均为空；核心路线、酶-EC、微生物身份、性状、基因组编号均无可定位的外部来源。答案内部 claim_scope 映射存在，但无法沿文献/数据库条目核查，属 MISSING_SOURCE 低分档；MISSING_SOURCE 默认不触发 cap。

<details><summary>V0.4理由与本行变化背景</summary>

2档：evidence_registry四条全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，无法沿文献、数据库条目或计算记录定位到具体结论；按六状态属MISSING_SOURCE。MISSING_SOURCE默认不触发关键错误cap，且无经核实错引，故D5低分但不判KE。给2而非1，是因为答案仍用EVID_001-EVID_004把内部声称与步骤做了结构化映射。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明模型交付的是内部知识型来源且无外部定位；不支持外部可追溯性。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 答案有专门 uncertainties 列表，明确 null SMILES、未核 EC/DSM/TaxID/genome、全部证据为 INTERNAL_KNOWLEDGE_ONLY；多数未知和低置信项有标注。仍有若干酶证据被标 high confidence，而来源仅为内部知识，属局部过度确信；但未系统性掩盖矛盾或把预测写成实证，取 7。

<details><summary>V0.4理由与本行变化背景</summary>

8档：答案明确披露全部证据为INTERNAL_KNOWLEDGE_ONLY，uncertainties列出SMILES未定、CBS3性状无来源、KT2440 DSM/TaxID/genome未核对、S10 EC未核对；属级推测标low confidence，未知项填null，未系统性把预测写成实证。少量过度确信：EVID_001/EVID_002对核心步骤给high confidence但仅为内部知识，属单点过度确信，不构成系统性误导cap，故取8。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：支持答案对未知、内部知识和待核点的披露，也显示局部 high confidence 与内部来源不完全相称。

</details>

## DeepSeek

答案SHA256：`6b1ae0745595c64d454cc2756bc1844fd167e77155bfd51a11ab0d5c1492bdb6`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 题面要求的四个必答主链步骤均已出现，route_scope 路线名原样填写，酶/EC、微生物及15项性状模块均有覆盖；但若干必答化学字段缺失：S1 主产物4-Chlorobenzoyl-CoA的SMILES为null，S2主底物与主产物SMILES均为null，S3主底物4-Hydroxybenzoyl-CoA的SMILES为null，属于必要内容遗漏。S5-S10为终点点后的额外下游延续，按P29不额外加分也不据此扣D2；D1只按必答主链与交付字段完整性评为5。

<details><summary>V0.4理由与本行变化背景</summary>

五个模块均有实质交付：10步主链（4-氯苯甲酸→4-氯苯甲酰-CoA→4-羟基苯甲酰-CoA→4-羟基苯甲酸→原儿茶酸→β-酮己二酸途径→乙酰辅酶A/琥珀酰辅酶A）、每步一个首选酶含EC、每步绑定一个菌并按物种+菌株去重为单一profile、15项性状字段齐全（10项填入+5项明确未知）、chosen_route_name原样回填。遗漏项：多数CoA类主底物/主产物SMILES为null（S2、S6、S7、S10主对全缺，S1/S3/S5/S8/S9部分缺）；ncbi_taxid为null；题面要求的&#x27;各项最强来源&#x27;仅以一条INTERNAL_KNOWLEDGE_ONLY占位。属&#x27;大部分必要内容完整、少量遗漏&#x27;档，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_075：gold 必答主链 ordered_step_count=4，终点为3,4-Dihydroxybenzoate；用作D1必答范围边界
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：路线名称为4-chlorobenzoate degradation，终点化合物为3,4-Dihydroxybenzoate
- ANSWER_TEXT / 6b1ae0745595c64d454cc2756bc1844fd167e77155bfd51a11ab0d5c1492bdb6：答案S1-S4存在若干主底物/主产物SMILES为null，S5-S10为额外下游延续

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 必答四步化学方向与gold一致：S1 CoA连接生成4-chlorobenzoyl-CoA，S2水解脱氯生成4-hydroxybenzoyl-CoA，S3硫酯水解生成4-hydroxybenzoate，S4羟化生成protocatechuate（3,4-dihydroxybenzoate）；底物到产物方向正确，未发现主链反转、明显原子不守恒或无依据跳跃。S5-S10继续β-酮己二酸下游且化学上连贯，但超出gold终点；按P29额外下游不额外加分也不据此扣D2。因D2最高允许为8且无9-10证据门，取7-8档上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与连续性成立：S1 CoA活化（4-氯苯甲酸+CoA+ATP→4-氯苯甲酰-CoA+AMP+PPi）、S2 水解脱卤（→4-羟基苯甲酰-CoA+Cl-）、S3 硫酯水解（→4-羟基苯甲酸+CoA）、S4 4-羟基苯甲酸3-单加氧酶羟化（+NADPH+O2→原儿茶酸）与gold四步（BSY-r01960→BSY-r01961→BSY-r00117→BSY-r00094）方向、结构、顺序一致；S5–S10为标准β-酮己二酸（原儿茶酸intradiol开环）下游，连接与原子计量自洽，无起始步错误、无无依据跳步、无方向反转。仅个别H+/H2O未列，属局部计量缺陷（辅因子条款7–8档）；主链辅因子（ATP/CoA/NADPH/O2/琥珀酰-CoA）已列出。gold终点为3,4-二羟基苯甲酸而答案延续至中心代谢物，按题面未指定终点处理，不作覆盖率扣分、也不加分。取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：gold S01-S04 的目标反应、方向及主底物/主产物；支持S1-S4反应对应判断
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：gold终点为3,4-Dihydroxybenzoate，用于区分必答主链与额外下游延续
- ANSWER_TEXT / 6b1ae0745595c64d454cc2756bc1844fd167e77155bfd51a11ab0d5c1492bdb6：答案给出S1-S10连续转化及反应类型；S1-S4覆盖必答主链，S5-S10为额外下游

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 四个必答目标反应均有可对应的酶名与显式EC：gold S03（4-chlorobenzoate:CoA ligase，6.2.1.33）对应答案S1；gold S04（4-chlorobenzoate-CoA dehalogenase，3.8.1.7）对应答案S2；gold S02（4-hydroxybenzoyl-CoA thioesterase，3.1.2.23）对应答案S3；gold S01（4-hydroxybenzoate hydroxylase，1.14.13.2）对应答案S4。答案酶名/EC落在accepted sets范围内，未发现EC类别与反应类型冲突。fcbA/fcbB/fcbC等基因归属为可选MINOR附加声称且未核，不足以压过主导功能对应；S5-S10额外下游酶不在本题N=4的目标信用内。因D3a最高允许为8且无9-10证据门，取7-8档上沿8；key_error为N。

<details><summary>V0.4理由与本行变化背景</summary>

10步酶名与EC逐条自洽且与反应类型匹配：S1 6.2.1.33（4-氯苯甲酸:CoA连接酶，fcbA）、S2 3.8.1.7（4-氯苯甲酰-CoA脱卤酶，fcbB）、S3 3.1.2.23（4-羟基苯甲酰-CoA硫酯酶，fcbC）、S4 1.14.13.2（4-羟基苯甲酸3-单加氧酶）与enzyme_gold四行EC逐字一致；S5 1.13.11.3、S6 5.5.1.2、S7 4.1.1.44、S8 3.1.1.24、S9 2.8.3.6、S10 2.3.1.174与β-酮己二酸途径各步酶功能对应，未见EC大类别与反应类型矛盾、未见酶名与EC互斥。扣分点为下游6个EC在E0中无冻结记录（UNRESOLVED），且仅3步给出基因名。取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：gold必答步accepted酶名/EC：S01=1.14.13.2，S02=3.1.2.23，S03=6.2.1.33，S04=3.8.1.7；支持答案四个目标酶对应判断
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：gold各必答步的反应类型/方向，用于核对答案酶对应的目标反应而非仅名称相似
- ANSWER_TEXT / 6b1ae0745595c64d454cc2756bc1844fd167e77155bfd51a11ab0d5c1492bdb6：答案S1-S4给出目标酶名与EC，S5-S10为额外下游酶，不计入本题必答目标信用

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案各步统一使用Pseudomonas sp. CBS3（strain CBS3，TaxID留null未编造），并在complete_pathway_organism_profile_id声称ORG_001可完成整条路径。冻结organism_gold在S01–S04四步均将Pseudomonas sp. CBS3列为EXACT匹配（TaxID 72586），且PATHWAY_COMPLETE行含72586 pathway_complete=TRUE，身份定位、步级归属与整路径能力均有记录级依据；仅缺TaxID/保藏号等更细粒度定位，取7–8带上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份有gold支持：Pseudomonas sp. CBS3在organism_gold中于S01–S04四步均EXACT匹配（taxid 72586），且PATHWAY_COMPLETE行显示72586的pathway_complete=TRUE，可支撑&#x27;整条（gold定义的4步）路径菌&#x27;身份；答案对ncbi_taxid留null，属如实缺失而非错配。扣分点：S5–S10各步归属同一菌株的能力声称超出gold的4步路径，答案未给反应级或全路径证据（证据仅一条内部知识），属身份定位≠反应级能力≠完整路径能力中后两层证据不足；未见跨属/异菌株错配等已核实身份错误。取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_075：支持Pseudomonas sp. CBS3（72586）在S01–S04为EXACT匹配微生物，且72586在PATHWAY_COMPLETE行为pathway_complete=TRUE；属记录级支持，不等于独立实验复核，也不核验答案自附来源。
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism：仅支持答案交付的菌名/菌株与归属声明，不构成身份或能力证据。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项性状齐备（10填、5明确null、0遗漏）：F2温度/F3 pH/F4盐度/F5保藏/F14基因组关键定量项诚实留null；已填F1好氧、F6好氧呼吸/氧、F7底物利用、F8降解能力、F9酶活、F10运动性、F11杆状、F12革兰氏阴性、F13不产孢、F15土壤/废水，均为泛Pseudomonas属性且全部仅署名EVID_001=INTERNAL_KNOWLEDGE_ONLY。冻结trait_gold对CBS3（72586）除F14 TaxID外全为UNKNOWN/complete_only，既不能证实也无已核矛盾；故按“部分性状合理但关键项证据不足、菌株级适用性未核”取5–6带下沿5，不以诚实null重复重扣（完成度归D1）。

<details><summary>V0.4理由与本行变化背景</summary>

10项填入性状均为定性、属级常见特征（F1好氧、F6好氧呼吸/氧为末端电子受体、F10运动、F11杆状、F12革兰阴性、F13不产孢、F15土壤与废水），与Pseudomonas属通行特征一致；F7/F8/F9与gold中CBS3的降解路线及fcbA/fcbB/fcbC酶活归属相容。但trait_gold对72586的F1–F13、F15全部为UNKNOWN，故这些性状既无独立核验、也无矛盾；全部以单一INTERNAL_KNOWLEDGE_ONLY证据＋medium置信承载，未标注为推断/预测，也未给菌株级适用条件；5项（温度/pH/盐度/保藏/基因组）明确null属诚实未知，其完成度扣分归D1不重复重扣（P112）。属&#x27;部分性状准确且适用、关键项证据不足&#x27;的5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_075：显示CBS3（72586）除F14外均为completeness_only/不可核验；可作为不判错、不判对的依据，不支持任何性状数值。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_075：72586的F1–F15除F14 TaxID外均UNKNOWN；只能证明无观测记录，不能否证答案填写内容。
- ANSWER_TEXT / ANSWER.evidence_registry&#91;EVID_001&#93;：仅表明性状署名为INTERNAL_KNOWLEDGE_ONLY、无database/record_id/locator，不构成性状支持。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案仅交付一条EVID_001：source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator均null，claim_scope覆盖“4-chlorobenzoate degradation pathway”与“Pseudomonas sp. CBS3 traits”。按P34，INTERNAL_KNOWLEDGE_ONLY属MISSING_SOURCE（缺失而非误导），全部决策相关claim组均无可定位来源→1–2低分档，默认不cap；因如实声明内部知识、未编造引用，取带内2。

<details><summary>V0.4理由与本行变化背景</summary>

全篇仅一条evidence_registry（EVID_001）：source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator全为null，claim_scope仅泛写&#x27;4-chlorobenzoate degradation pathway&#x27;&#x27;Pseudomonas sp. CBS3 traits&#x27;。按四.3，&#x27;完全无引用或仅有INTERNAL_KNOWLEDGE_ONLY类自我声明&#x27;＝MISSING_SOURCE；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）与支持组均无条目级可定位可核对来源，故落低分档（1–2）。本案E0为EVIDENCE_GAP，任何编号类声称（EC/ TaxID/登录号）只能UNRESOLVED，不判虚构、不判CONTRADICTED、不计已核实关键错误，因此不触发cap（P34/P40/P51）。取2：答案至少以单一来源类型统一披露、未伪造具体条目。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;EVID_001&#93;：仅证明来源类型为INTERNAL_KNOWLEDGE_ONLY且定位字段为空，不支持任何结论可追查性。
- RUBRIC_CLAUSE / P34：规定INTERNAL_KNOWLEDGE_ONLY记MISSING_SOURCE并按低分档、默认不触发关键错误cap。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 答案在evidence_registry显式标注INTERNAL_KNOWLEDGE_ONLY、统一用medium而非high、并对F2/F3/F4/F5/F14诚实留null，uncertainties亦承认下游酶菌株归属与EC“未逐一核实”；但该说明仅一句且只覆盖下游，主链四步的酶/EC、fcbA/fcbB/fcbC基因归属与CBS3全部已填性状均未披露为记忆值/未核，仍以medium置信呈现，属“有不确定性说明但过于笼统、部分结论强度超过依据”的5–6带，非系统性误导，不cap，取5。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露有实质内容：5项性状明确填null（温度/pH/盐度/保藏/基因组），uncertainties明确写出&#x27;下游酶的具体菌株归属和EC编号基于一般知识，未逐一核实&#x27;，即对最大风险点（下游EC与菌株归属）作了具体而非笼统的限定；未把预测包装成数据库直查观测。不足：所有步级酶/菌与全部性状统一用medium置信＋单一INTERNAL_KNOWLEDGE_ONLY证据承载，未逐项区分&#x27;观测/推断/未知&#x27;；F7–F9实际由路线反推却按独立性状呈现；未说明氧条件未指定时&#x27;好氧&#x27;标注的依据边界。属单点/局部置信与证据不相称而未掩盖主要限制，档内扣分不cap（P119），取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：仅证明答案给出了一句范围有限的不确定性说明，不代表其余未核结论已披露。
- RUBRIC_CLAUSE / P119：区分单点过度确信（档内扣）与系统性误导（cap候选），本维按前者处理。

</details>

## Kimi

答案SHA256：`c02715b98c8b459e75e7bff3bcac44bb78635f95545445fc531ad6dc0daa9e81`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 5-6 band: main modules are present (route text, three enzyme steps, one microorganism, 15 trait fields, source and uncertainty), but one of four required main-chain steps is missing and the answer terminates at 4-hydroxybenzoate instead of the gold terminal 3,4-dihydroxybenzoate; 12/15 traits are explicitly unknown. Within band choose 5 because the omitted terminal step is a KEY_TERMINAL omission.

<details><summary>V0.4理由与本行变化背景</summary>

主模块齐备：3步均给主底物/主产物（含SMILES与role=main/cofactor/byproduct）、首选酶+EC、对应菌；单一organism_profile按物种+菌株去重，步引用自洽；15项性状槽位全部出现（3项有值、12项诚实null）；route_scope.chosen_route_name原样回填题面路线名；来源与不确定性各有登记。缺口：主链止于4-hydroxybenzoate，比gold线性4步少4-hydroxybenzoate hydroxylase一步（答案已在route_scope.notes与central_metabolism_entry显式声明边界，属完成度不足而非任务参数偏离）；12/15性状为null（P45：诚实null仍反映完成度不足）。落7–8档，档内取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：Gold terminal is 3,4-Dihydroxybenzoate; answer stops at 4-hydroxybenzoate.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：Gold required S01 is 4-hydroxybenzoate hydroxylase converting 4-hydroxybenzoate to 3,4-dihydroxybenzoate; answer does not deliver it.
- ANSWER_TEXT / ANSWER：Shows delivered three steps and 12 null/unknown trait fields.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 5-6 band: the three delivered transformations are chemically coherent (ATP-dependent CoA ligation, hydrolytic dehalogenation, thioester hydrolysis) with correct direction and explicit cofactors; however the main chain stops at 4-hydroxybenzoate and omits the required terminal hydroxylation to 3,4-dihydroxybenzoate. Delivered steps show no atom imbalance or direction reversal, but the missing terminal conversion prevents 7-8.

<details><summary>V0.4理由与本行变化背景</summary>

三步化学与gold线性步逐一对应：S1为ATP依赖CoA连接（4-chlorobenzoate+ATP+CoA→4-chlorobenzoyl-CoA+AMP+diphosphate），S2为水解脱氯（4-chlorobenzoyl-CoA+H2O→4-hydroxybenzoyl-CoA+Cl−），S3为硫酯水解（4-hydroxybenzoyl-CoA+H2O→4-hydroxybenzoate+CoA）；方向均为forward、主链角色标注正确、未见原子明显不守恒，辅因子/副产物在列。未给9–10：相对gold还差S01羟化步（4-hydroxybenzoate→3,4-dihydroxybenzoate），虽按P29/P28题面未指定终点时该下游缺口不进入D2覆盖率扣分，但&#x27;关键转化均获可靠支持&#x27;的把握受限；脱卤酶EC问题归D3a另行待核。主链及关键转化有充分依据、少量局部问题→8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：Gold main chain includes S01 hydroxylation to 3,4-dihydroxybenzoate; answer covers S03/S04/S02 transformations but not S01.
- ANSWER_TEXT / ANSWER：Shows the three delivered chemical transformations and the 4-hydroxybenzoate endpoint.

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 按C03/C04/C05：答案仅交付三步，且止于4-hydroxybenzoate。S1的4-chlorobenzoate-CoA ligase/EC 6.2.1.33与accepted S03一致；S3的4-hydroxybenzoyl-CoA thioesterase/EC 3.1.2.23与accepted S02一致；S2的dehalogenase名称接近，但EC 3.8.1.6与accepted S04的3.8.1.7不一致，且三步在程序状态中均为ROUTE_HOLD_REPRESENTATION/U，不能按已确认S计。Gold必答S01为4-hydroxybenzoate hydroxylase（EC 1.14.13.2），将4-hydroxybenzoate转为3,4-dihydroxybenzoate；答案缺失该KEY_TERMINAL步，按D-KEY4将D3a限制在≤4。受限范围内，两步有accepted名称/EC明确匹配，一步EC待核，可用部分与关键缺失边界清楚，取4而非更低；但不足以进入5–6档。

<details><summary>V0.4理由与本行变化背景</summary>

4-chlorobenzoate-CoA ligase EC 6.2.1.33与4-hydroxybenzoyl-CoA thioesterase EC 3.1.2.23与gold一致；4-chlorobenzoyl-CoA dehalogenase名称与gold一致，但EC写作3.8.1.6，而gold为3.8.1.7。E0无官方EC条目（item gap GAP-075-009: EC:3.8.1.6；GAP-075-015: EC:6.2.1.33待派发），按四.5/四.6保持UNRESOLVED待核，不判错、不cap；fcbA/fcbB/fcbC基因归属无冻结证据可核。主要步骤酶-反应对应有可靠支持、仅少量条目需确认→7–8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：S01为4-hydroxybenzoate hydroxylase/EC 1.14.13.2；S02为4-hydroxybenzoyl-CoA thioesterase/EC 3.1.2.23；S03为4-chlorobenzoate:CoA ligase/EC 6.2.1.33；S04为4-chlorobenzoate-CoA dehalogenase/EC 3.8.1.7。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：S01为4-hydroxybenzoate→3,4-dihydroxybenzoate的末端羟基化；S02生成4-hydroxybenzoate；S03为4-chlorobenzoate→4-chlorobenzoyl-CoA；S04为4-chlorobenzoyl-CoA→4-hydroxybenzoyl-CoA。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_075：BIOPATH150_075为LINEAR_UNIQUE，ordered_step_count=4。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：Gold终点主产物为3,4-Dihydroxybenzoate；答案止于4-hydroxybenzoate，未达该终点。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 7-8 band: Pseudomonas sp. CBS-3 matches the gold organism rows for the pathway steps, and gold pathway-complete data include TaxID 72586; the answer consistently assigns ORG_001 to all delivered steps. The missing TaxID and lack of a separate capability source are minor omissions, not an identity error. The missing terminal step is handled under D1/D2/D3a, not as a microbe identity failure.

<details><summary>V0.4理由与本行变化背景</summary>

身份层：答案单菌Pseudomonas sp. strain CBS-3与gold organism_gold的Pseudomonas sp. CBS3为EXACT匹配（TaxID 72586），粒度合法；步级归属层：gold在S02/S03/S04均将CBS3列为对应菌，与答案三步归属一致；完整路径能力层：gold PATHWAY_COMPLETE行72586 pathway_complete=TRUE，支持其对BSY-p00582的能力归属。答案ncbi_taxid留null属诚实未知，不构成身份错配；未出现由基因组/序列存在性外推整条路径的情形。仅文献内容本身E0不可核（见D5）与TaxID缺填，7–8档内取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_075：Gold matches the species/strain name and lists pathway-complete capability; it does not certify every enzyme step in the answer, and answer did not deliver a TaxID.
- ANSWER_TEXT / ANSWER：Shows the single strain used for all steps and the complete-pathway profile id.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 5-6 band: only F7/F8/F9 are filled; F7-F9 are relevant to the dehalogenase pathway but rely on one source and are not machine-verified in E0. The 12 key quantitative/physiological traits (temperature, pH, salinity, oxygen, etc.) are honestly null/unknown. Partial traits are plausible and applicable, but key trait evidence is insufficient, so 5-6; choose 6 for clear null handling and relevant filled traits.

<details><summary>V0.4理由与本行变化背景</summary>

15项齐全：F7/F8/F9三项有值并指向EVID_001，其余12项value=null+confidence=unknown（诚实未知，不计为遗漏/错误）。gold对CBS3（72586）F1–F13与F15均为UNKNOWN、仅F14有TaxID记录，trait_scoreability_mask显示72586全部性状无观测值可评分→既不能证其错，也不能证其准；F8/F9把脱卤酶体系文献外推为整菌降解能力/酶活，作用范围表述尚可但缺独立观测支持；F14留null而未使用gold可得的TaxID 72586（属完成度问题而非错误）。部分性状合理但关键项证据不足→5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_075：Gold trait rows for Pseudomonas sp. CBS3 are UNKNOWN; gold neither confirms nor contradicts the answer&#x27;s filled F7-F9, and cannot verify the source.
- ANSWER_TEXT / ANSWER：Shows the three filled traits and twelve explicit unknown/null traits.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 5-6 band: one specific literature citation (Chang et al., Biochemistry 1992) is provided and claim_scope covers the three enzymes and F7-F9, but the same citation is reused for all claims, the terminal boundary claim lacks a direct source, and E0 is EVIDENCE_GAP so actual support cannot be verified. No verified mis-citation, so no cap; score 6 for partial traceability.

<details><summary>V0.4理由与本行变化背景</summary>

仅有单一来源EVID_001：一个具体文献条目（作者/期刊/卷期页齐全），claim_scope覆盖三酶主链与F7/F8/F9；全部步、酶、菌与三项性状共用该来源，无逐claim独立来源或计算记录。E0为EVIDENCE_GAP，文献内容、书目与全部编号均无法核验→相关组登记UNRESOLVED_SOURCE，不判虚构、不判CONTRADICTED、不cap；无已核实错引（severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION）。决策相关组有可定位的条目级来源（非GENERIC），但内容不可核对且单源复用覆盖全部核心结论，落5–6档（部分关键结论可定位、其余记录不足）取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Provides the full citation and claim_scope; does not contain a DOI and cannot be verified in E0.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：Gold terminal is 3,4-Dihydroxybenzoate; the answer&#x27;s source does not establish the stated 4-hydroxybenzoate terminal boundary.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 7-8 band: the answer is unusually explicit about nulls and limits: oxygen condition null, TaxID absent, 12 traits unknown, and uncertainty notes explain the CoA chemistry and unresolved identity. However it assigns high confidence to all three enzymes, the microbe and F7-F9 from one unverified source, and incorrectly asserts that the downstream hydroxylation is outside the specified main chain. No systematic prediction-as-observation, so no cap; choose 7.

<details><summary>V0.4理由与本行变化背景</summary>

正面：uncertainties明确披露题面氧条件未指定、CBS-3未解析到可核验物种名/TaxID/保藏号与完整生理性状；route_scope.notes与central_metabolism_entry声明终点边界、下游不属评分主链；全部未知项一律null+unknown，未把预测/推断写成观测。扣分：所有已填事实与编号统一标high confidence，包括与gold不一致且不可核的脱卤酶EC 3.8.1.6、以及由酶纯化文献外推的F8/F9整菌能力/酶活，对这些未核实点零披露——属单点/少数条目过度确信而非系统性误导，5–6档取6，不cap。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows honest null disclosures and overconfident high-confidence labels; also shows the incorrect terminal-boundary explanation.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：Gold terminal is 3,4-Dihydroxybenzoate, so the answer&#x27;s boundary explanation is not supported.

</details>

## Qwen

答案SHA256：`870229bb7e5dad4a090c7896d5938ecbb95098908ed6d6ae78831a2a48a19e7c`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 结构上覆盖了路径、逐步酶/菌和15项性状字段，route_scope.chosen_route_name逐字保留；但15项性状全部为null且无来源，构成D1完成度不足（P45），且所交付主链未清晰对应gold的四步CoA主链（S03 ligase→S04 dehalogenase→S02 thioesterase→S01 hydroxylase）。当前route alignment为BOUNDARY_REVIEW/ROUTE_HOLD_REPRESENTATION，不能确认任务路线符合也不能据此cap。按主要模块有涉及但必要内容/关联不足，取5–6档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

六步均给出主底物/产物英文名、酶名+EC与对应微生物，route_scope.chosen_route_name原样回填“4-chlorobenzoate degradation”，steps/organism_profiles/evidence_registry结构完整可读；但两个profile的15项性状全部null（仅结构占位、无实质内容），3-carboxy-cis,cis-muconate、4-carboxymuconolactone、maleylacetate等中间体SMILES为null，属“主要模块均有涉及但若干必要内容遗漏/仅占位”的5–6档，档内取6（结构关联清楚、无路线名偏离，但性状模块完成度极低）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案包含6步路径、逐步酶与微生物、两个organism_profile及15项性状字段；所有性状value/evidence_id为null
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_075：gold formal case记录ordered_step_count=4；该数字是全图材料数，不单独作为所有旁支的缺步分母
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：gold主链酶记录包含6.2.1.33、3.8.1.7、3.1.2.23、1.14.13.2；仅表示数据库策展的酶-反应粒度，不证明具体蛋白实验活性
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：gold终点主产物为3,4-Dihydroxybenzoate

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 所答至3,4-DHB的主干（4-chlorobenzoate→4-hydroxybenzoate→3,4-DHB）化学上可成立；S2与gold S01的4-hydroxybenzoate 3-monooxygenase反应一致。但相对于题面锁定的gold CoA主链，S1用直接水解脱氯替代CoA ligase/dehalogenase/thioesterase路线，按C06化学可成立替换≤6。继续延伸到3-oxoadipate的S5把4-carboxymuconolactone decarboxylation产物写成maleylacetate（未给SMILES，且与S6 maleylacetate reductase连用），关键中间体与连接仍待核/可能为替代，不能进入7–8；无已核核心化学矛盾，故不cap，取6。

<details><summary>V0.4理由与本行变化背景</summary>

以gold为参照：题面范围内主链（4-chlorobenzoate→4-hydroxybenzoate→3,4-dihydroxybenzoate）化学成立——S1水解脱卤反应式C7H4ClO2-+H2O→C7H5O3-+Cl-+H+原子与电荷守恒；S2与gold S01一致（4-Hydroxybenzoate+NADPH+H++O2→3,4-Dihydroxybenzoate+NADP++H2O，EC 1.14.13.2）；S3邻位开环、S4环化化学成立。缺陷：S5把4-carboxymuconolactone脱羧产物写成maleylacetate(+CO2)，β-酮己二酸支路的正确连接应为3-oxoadipate enol-lactone随后经内酯水解酶开环，S6以maleylacetate reductase(EC 1.3.1.4，属氯代儿茶酚支路)生成3-oxoadipate，下游连接不成立。该缺陷位于gold终点之外的下游延伸，按四.2/P29不进入覆盖率定档，按“主干成立但关键中间体/连接需修订、合理性证据有限”取5–6档、档内6；未触发cap（起始步与方向合理、无原子明显不守恒、未一步跳入中心代谢）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案给出S1直接水解脱氯、S2 4-羟基苯甲酸羟化至3,4-二羟基苯甲酸，以及S5–S6至3-氧代己二酸的延伸步骤；S5产物maleylacetate未给SMILES
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：gold S01反应为4-hydroxybenzoate + O2 + NADPH + H+ → 3,4-Dihydroxybenzoate + H2O + NADP+；与答案S2的主转化一致
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：gold主链包含4-chlorobenzoate:CoA ligase（6.2.1.33）、4-chlorobenzoyl-CoA dehalogenase（3.8.1.7）、4-hydroxybenzoyl-CoA thioesterase（3.1.2.23）和4-hydroxybenzoate hydroxylase（1.14.13.2）；用于对照答案S1的路线替换
- RUBRIC_CLAUSE / C06：D2对化学可成立替换候选设≤6上限，且需独立化学依据

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> C04计数带为&#91;3,4&#93;：仅S01目标反应匹配（S=1/4），S03关键入口不是gold的CoA连接酶，S04/S02缺失。D-KEY4上限4适用；因仅少数目标可用且关键入口失败，取3而非默认上沿4。

<details><summary>V0.4理由与本行变化背景</summary>

六步酶名与EC大类均与反应类型相容（3.8.1脱卤、1.14.13.2单加氧、1.13.11开环双加氧、5.5.1环异构、4.1.1脱羧、1.3.1还原），未出现已核实的“EC大类与反应类型不匹配”或“酶名与EC互相矛盾”；S2的EC 1.14.13.2由gold enzyme_gold直接支持（4-hydroxybenzoate hydroxylase）。不足：S1以EC 3.8.1.2支撑4-chlorobenzoate dehalogenase的名称—编号对应无E0记录可核（答案自述该EC归属不确定、confidence low），S3–S6的EC亦无冻结记录核实，属“有合理候选和部分支持、若干关键步骤缺具体核验”的5–6档、档内6；按四.6不得凭记忆放行，故不判错也不给高分。key_error=UNRESOLVED（S1 EC疑似特异性不符但冻结证据不足，不cap、不计已核实KE）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：gold酶记录定义S01 EC1.14.13.2、S02 EC3.1.2.23、S03 EC6.2.1.33、S04 EC3.8.1.7；不支持无CoA中间体的4-氯苯甲酸直接脱卤入口。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：gold反应记录给出CoA介导四步有向主链及终点3,4-dihydroxybenzoate。
- ANSWER_TEXT / BIOPATH150_075#answer：答案S2为4-hydroxybenzoate-&gt;3,4-dihydroxybenzoate EC1.14.13.2；S1为直接脱卤且缺少4-chlorobenzoyl-CoA/4-hydroxybenzoyl-CoA步骤。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> gold organism行支持Pseudomonas putida在S01羟基化步骤；Pseudomonas sp. CBS3身份真实（gold TaxID 72586），但答案把它用于gold不支持的直接脱卤步骤，且P. putida无strain/TaxID。部分支持、若干能力未核，取5–6档上沿6；疑似能力错配在E0缺口下记UNRESOLVED，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

两个profile的菌名均能在gold organism_gold中找到：Pseudomonas sp. CBS3（taxid 72586，S01–S04行）与Pseudomonas putida（taxid 303，S01行），属真实步级微生物身份，不存在跨属/异菌株错配或编造；答案未填TaxID/保藏号，粒度较低但未冒充菌株级（strain仅CBS3，与gold 72586对应）。不足：把P. putida同一物种用于S2–S6五步、CBS3用于S1水解脱卤，均为反应级/多步能力声称，无E0记录核实（身份定位≠反应级能力≠完整路径能力）；complete_pathway_organism_profile_id=null，未声称全路径菌。按“有合理候选和部分支持、若干关键作用范围未充分核验”取5–6档、档内6；按身份阶梯不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_075：gold organism行支持P. putida用于S01，支持CBS3用于CoA介导S02/S03/S04；不支持CBS3直接脱卤。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 两个organism_profile的15项性状全部value=null、confidence=unknown；按P44全部必需性状为null/空值时D4记MISSING=1，不宣称检测到科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

两个organism_profiles（ORG_001 Pseudomonas sp. CBS3、ORG_002 Pseudomonas putida）的F1–F15全部为value null、confidence unknown、evidence_id null，未交付任何可评价的性状值；按P44“全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到科学错误”。诚实null的完成度后果已在D1反映、披露质量在D6正面体现，D4无内容可评分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_075#answer：答案提供性状键但所有性状值均为null/unknown。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 所有evidence_registry条目均为INTERNAL_KNOWLEDGE_ONLY，database/record_id为null，决策相关结论不可外部定位；属MISSING_SOURCE低分档。无已核实错引，默认不cap；有结构化claim_scope自映射，故取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

六条EVID均source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id为null、locator为自由文本，按P34属MISSING_SOURCE而非GENERIC_SOURCE；decision-relevant组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）全部MISSING_SOURCE，SUPPORTING组亦无条目级定位；无任何经核实的VERIFIED_MIS_CITATION（E0=EVIDENCE_GAP，不判虚构、不判CONTRADICTED），故severity=NOT_APPLICABLE、不cap；按P41“全部缺失→低分档”取2（答案对各步标注confidence low/unknown并在uncertainties说明未附外部记录，略优于完全无说明，但无一条可核对）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_075#answer：证据登记仅为内部知识，无数据库条目、DOI或可定位记录。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案持续使用low/unknown置信，列出氧条件、EC归属、菌株活性等限制，未知性状填null；无系统性把预测写成实证。但它仍把替代直脱卤路线写成单条连续主路线而未标明替代性，故取7而非8/9。

<details><summary>V0.4理由与本行变化背景</summary>

答案在uncertainties与每步uncertainty中具体披露：氧条件未指定、EC编号归属不确定、具体菌株活性未逐项验证、性状因缺来源填null；并将全部条目confidence标为low/unknown、source_type标为INTERNAL_KNOWLEDGE_ONLY，未把内部知识包装为DATABASE_DIRECT或观测，证据性质与置信度大体相称，属7–8档。不足：未披露S5中间体归属（maleylacetate vs 3-oxoadipate enol-lactone）的不确定性，也未说明S1水解脱卤与gold CoA路径的替代关系，故档内取7而非8–9；属披露不足而非系统性误导，不cap（八.D6/P119）。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_075#answer：答案披露了不确定性与低置信，但未声明其路线为相对指定CoA路线的替代路线。

</details>

## Grok

答案SHA256：`a5d8fa326421b7cc4f9f0839632d97e022642cf5dd150fc37b67f26b3d6978f5`。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出S1-S3三步主链，起点、方向与字段结构基本完整，但缺少任务必答末端S01（4-hydroxybenzoate→3,4-dihydroxybenzoate），并在route_summary中把4-hydroxybenzoate之后内容排除出评分主链；15项性状仅5项有值、10项明确未知。按5-6档取6：主要模块均有涉及，但必要末端步骤与大量性状信息遗漏。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：gold终点为3,4-Dihydroxybenzoate，支持判断答案缺少末端步；不证明具体蛋白实验活性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_075：本题主链登记4步；不代表所有DAG旁支都必答。
- ANSWER_TEXT / steps S1-S3：答案仅交付三个step；S01未作为step交付。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已交付S1-S3三步化学上连续且方向正确：4-chlorobenzoate经CoA连接活化、4-chlorobenzoyl-CoA水解脱氯、4-hydroxybenzoyl-CoA硫酯水解；主要辅因子与产物基本列出，无原子/方向性核心冲突。缺少S01末端羟化主要按D1/D3a目标完成与缺步处理，不以覆盖率硬换D2；未达9-10因任务主链终点未在答案主链中闭合。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：支持S03→S04→S02三步化学转化与方向；不扩展到未交付的S01。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：支持对应酶名/EC与反应类型；不证明具体蛋白实验活性。
- ANSWER_TEXT / steps S1-S3：答案已交付的化学步骤可逐项核对；不包含S01。

</details>

### D3a 目标反应与酶对应：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1、S2、S3分别与gold S03（6.2.1.33）、S04（3.8.1.7）、S02（3.1.2.23）的accepted酶名/EC匹配，功能级支持清楚；但必答末端S01（4-hydroxybenzoate hydroxylase，EC 1.14.13.2）未作为step交付，属于KEY_TERMINAL目标缺失，触发D-KEY4的≤4上界。受限&#91;1,4&#93;内取4：三个已交付目标支持明确、关键失败边界清楚；不是默认4，而是多数成功不豁免KEY上界。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：支持四步accepted酶名/EC；S01为1.14.13.2，答案未交付。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：支持终点为3,4-Dihydroxybenzoate；不支持具体蛋白活性。
- ANSWER_TEXT / steps S1-S3：答案仅交付三个酶的step；S01缺失。

</details>

### D3b 微生物身份与能力：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案在S1-S3均指向Pseudomonas sp. CBS3；gold organism_gold对S01-S04均给出该菌EXACT匹配，并对TaxID 72586登记PATHWAY_COMPLETE=TRUE，支持其身份、步级归属和整条路径能力声称。TaxID留null属诚实未知，未编造；缺少S01的微生物行是路线缺步后果，不是D3b身份/能力错误。按9-10档取9：关键微生物对应与全路径能力有充分适用支持，仅身份编号留空。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_075：支持CBS3在四步均有EXACT organism匹配及PATHWAY_COMPLETE；不证明具体蛋白实验活性。
- ANSWER_TEXT / microorganism fields：答案使用CBS3并声明全路径profile；未填TaxID。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项字段全部出现，5项有值、10项明确未知；有值项F1/F6/F7/F8/F9与路线能力大体相容，未见与gold直接冲突的数值。但CBS3在冻结trait_gold中除F14 TaxID外均为UNKNOWN，答案的有值性状只有INTERNAL_KNOWLEDGE_ONLY来源，温度/pH/盐度/保藏/基因组等关键项缺失。按5-6档取5：部分性状可理解且诚实未知，但关键项证据不足、适用性不能核验。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_075：CBS3多数性状为UNKNOWN，F14仅TaxID 72586 observed；不支持答案有值性状的定量观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_075：CBS3多数性状为completeness_only；不能把未知回填为已观测。
- ANSWER_TEXT / traits：答案显式返回15项，5项有值、10项unknown；支持D6诚实披露但不等于D4已核。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> answer的evidence_registry三条均为INTERNAL_KNOWLEDGE_ONLY，无database、record_id或可定位外部条目；IUBMB EC与fcbABC描述只是内部知识说明，不能作为可核来源。按六状态属MISSING_SOURCE，决策相关claim group整体不可外部追查；无已核实错引，故不cap，但D5只能落1-2档。取2：有claim_scope分区和描述性locator，较完全无来源略好。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：三条均为INTERNAL_KNOWLEDGE_ONLY，无外部记录ID；支持D5低档，不证明科学错误。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确列出uncertainties：TaxID/保藏/基因组未核实、多项性状无原文不按属级猜测、SMILES为近似、氧条件为路线典型好氧而非实测、fcb基因对应未重新检索；大量字段用null/unknown。证据类型总体标注为INTERNAL_KNOWLEDGE_ONLY，未把预测写成实验观测。仍有高confidence内部知识项及全路径profile声称略强，故不取9-10；按7-8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：支持其已披露主要未知与证据边界；不把内部知识升级为外部证据。
- ANSWER_TEXT / evidence_registry：明确标为INTERNAL_KNOWLEDGE_ONLY，有助于D6；不弥补D5可追溯性。

</details>

## GPT5.6

答案SHA256：`c6acab3836ca2ed9c670796cc37246d57c3a3d4c2bfb0687be94421a7035a5c6`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案原样填写 chosen_route_name，并给出3步主链及每步的底物/产物名、首选酶/EC和对应微生物，路径模块、酶模块、微生物模块均有可辨认内容；但15项性状全部为 null/unknown，没有任何性状值或最强来源，等于性状模块仅占位；同时与冻结gold的4步主链相比，答案未提供S02/S03/S04对应的CoA连接、CoA脱卤和硫酯酶转化。路线状态为BOUNDARY_REVIEW，故不把替代路线单独改判为已确认路线失败，但完整性按实际交付和题面15性状要求仍应落在5–6档下沿。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_075#question：要求主链每步给出底物/产物英文名及SMILES、首选酶及EC、对应微生物；同一菌去重；每个profile一次返回15项性状及最强来源。
- ANSWER_TEXT / BIOPATH150_075#answer：steps仅交付3步；organism_profiles&#91;0&#93;的15项性状value均为null，confidence为unknown，evidence_id均为null。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_075：冻结主链 ordered_step_count=4、LINEAR_UNIQUE；仅作完整性参照，不自动把替代路线判错。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：gold四个必答步及方向；答案只部分对应，S02/S03/S04未绑定。

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主有机转化到gold终点protocatechuate的部分合理：4-hydroxybenzoate经EC 1.14.13.2羟化为protocatechuate与gold/accepted一致；protocatechuate 3,4-dioxygenase开环也化学合理，但已超出gold终点，按P29不因额外下游加减分。主要问题是S1用4-chlorobenzoate直接水解脱氯到4-hydroxybenzoate，替代gold的CoA连接/CoA脱卤/硫酯酶三步，缺少CoA中间体，且该直接转化未被冻结gold确认；S1未列H2O/H+，S2未列O2/NADPH/H+，S3产物SMILES为null。按D2 5–6档：主干部分成立但关键首转化/中间体需修订、合理性证据有限，取6；未达到7–8档的“关键转化有充分依据、仅少量局部问题”。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_075#answer：S1以4-Chlorobenzoate dehalogenase EC 3.8.1.2直接生成4-Hydroxybenzoate和chloride，未列H2O/H+；S2以EC 1.14.13.2生成protocatechuate，未列O2/NADPH/H+；S3产物3-Carboxy-cis,cis-muconate的SMILES为null。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_075：gold终点为3,4-Dihydroxybenzoate（protocatechuate）。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：gold主链为4-chlorobenzoate经4-chlorobenzoyl-CoA、4-hydroxybenzoyl-CoA、4-hydroxybenzoate到3,4-dihydroxybenzoate；答案S1直接水解脱氯不在该gold主链中。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：gold accepted酶包括EC 6.2.1.33、3.8.1.7、3.1.2.23、1.14.13.2；答案S1的EC 3.8.1.2不在gold酶行中，不能据gold确认。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> N=4. Manual alignment: answer S2 matches gold S01 (4-hydroxybenzoate -&gt; protocatechuate; 4-hydroxybenzoate 3-monooxygenase EC 1.14.13.2; accepted function-level G4) =&gt; S=1. Gold S02 (4-hydroxybenzoyl-CoA thioesterase EC 3.1.2.23), S03 (4-chlorobenzoate:CoA ligase EC 6.2.1.33), and S04 (4-chlorobenzoyl-CoA dehalogenase EC 3.8.1.7) are not delivered; answer uses a direct dehalogenase and ring-cleavage step instead =&gt; M=3. C=1/4=0.25, band &#91;3,4&#93;; KEY_ENTRY S03 missing and other main-chain targets missing; D-KEY4 caps at 4. Choose 3: only one of four required target reactions is usable and the key entry plus two other required steps are absent.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_075：Lists accepted gold enzymes for S01-S04; supports EC 1.14.13.2 on S01 only at function level.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_075：Defines directed gold reactions S01-S04; supports the missing-step check.
- ANSWER_TEXT / ANSWER：Shows S2 matches S01, while S1/S3 are different reactions and S02-S04 are absent.

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Pseudomonas sp. CBS3 name/strain is gold-supported (TaxID 72586) and is a supported organism for gold S01 hydroxylase, which answer S2 matches. No complete-pathway organism claim is made (complete_pathway_organism_profile_id null). However step-level capability for the answer&#x27;s direct dehalogenase S1 and protocatechuate dioxygenase S3 is not supported in the supplied gold/E0; two of three step-level associations remain unresolved. 5-6 band; choose 6 because identity is reliable and one core step is supported, but several step-level capabilities need confirmation.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_075：Lists Pseudomonas sp. CBS3 exact organism rows for gold S01-S04; supports identity/strain and S01 step-level association, not every answer step.
- ANSWER_TEXT / ANSWER：Shows CBS3 used for all three answer steps; used to locate supported and unresolved step-level claims.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 required traits in ORG_001 are present only as null/unknown; no trait value is delivered. Under P44, all required traits null/empty =&gt; D4 MISSING=1.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows every trait value is null/unknown; supports MISSING, not a scientific error finding.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_075：Shows the frozen trait slice; for CBS3 many trait rows are UNKNOWN, but this does not supply answer trait values.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All answer evidence entries are INTERNAL_KNOWLEDGE_ONLY with database, record_id, and locator null. These are MISSING_SOURCE under D5; decision-relevant route/enzyme/organism claims are not locatable. No verified mis-citation is present, so no cap; source traceability is in the 1-2 band. Choose 2 because the answer does provide structured claim scopes but no actual locatable sources.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows only internal-knowledge declarations and no locatable external sources; supports low D5.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer is generally honest about uncertainty: multiple nulls, low/unknown confidence, explicit uncertainties, and INTERNAL_KNOWLEDGE_ONLY source labels. It does not systematically present predictions as observations. Minor overstatement exists in route_summary and medium confidence on S1, but main limits and unknowns are disclosed. 7-8 band; choose 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows explicit uncertainty labels and null handling; supports high but not perfect D6.

</details>
