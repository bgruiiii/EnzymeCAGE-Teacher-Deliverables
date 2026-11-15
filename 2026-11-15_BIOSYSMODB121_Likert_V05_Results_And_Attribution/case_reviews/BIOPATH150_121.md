# BIOPATH150_121：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：γ-resorcylate degradation II

污染物：2,6-Dihydroxybenzoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 66 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 56.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 68 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 48 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 35 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 32 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`93761f4df114147cb022edfb9ef8b27f66c0fbd4c34a02b43dda95ff40f1f06c`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 路线名与氧条件按题面回显；必答主链前3步及步骤、酶、菌、15项性状字段和证据登记均已交付。额外S4-S6续到β-酮己二酸/TCA，超出gold指定终点Maleylacetate；属范围/表达上的小缺陷而非必需内容缺失。D1按7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

六步主链全部给出，每步含底物/产物英文名与SMILES、一个酶、一个对应微生物；route_scope.chosen_route_name原样填写γ-resorcylate degradation II，oxygen_condition按题面null填写，符合任务参数要求；两个organism_profile各15项性状字段齐全（未知项填null而非编造）。扣分点：S1/S2/S3/S6共4步ec_number为null（题面明确要求EC，且S1/S2/S3正是gold三步，官方编号存在），ORG_001缺ncbi_taxid，S4–S6超出题面/gold终点(Maleylacetate)却以main steps而非范围声明交付。属&#x27;大部分必要内容完整、关联清楚，仅少量遗漏&#x27;，档内取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_121：Frozen gold shows ordered_step_count=3, linear unique, terminal main product Maleylacetate; this is the required main-chain length, not a denominator for extra DAG branches.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_121：Root compound 2,6-Dihydroxybenzoate and terminal Maleylacetate for task-scope conformance.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> S1-S3化学转化与gold相符：2,6-dihydroxybenzoate脱羧到resorcinol+CO2，resorcinol经NADH/O2羟基化为hydroxyquinol，hydroxyquinol经双加氧开环到maleylacetate；方向与主链连续性成立。S4-S6化学上可成立但属指定终点之后的下游，不作为D2主链加分；H+/电荷/立体表示和少量辅因子表述有小缺陷。9-10证据门未满足，7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3与gold三步化学逐一吻合：S1脱羧(2,6-dihydroxybenzoate→resorcinol+CO2，gold S03可逆脱羧)、S2 NADH/O2依赖单加氧羟基化(resorcinol→1,2,4-benzenetriol，gold S02)、S3邻位双加氧开环(hydroxyquinol→maleylacetate，gold S01)，方向均为SUBSTRATE_TO_PRODUCT正方向，环编号与取代位(SMILES)正确，受氢/受氧辅因子在列，无起始步错误、无无依据跳步、无原子明显不守恒。S4–S6(maleylacetate reductase→3-oxoadipate→3-oxoadipyl-CoA→succinyl-CoA+acetyl-CoA)化学亦连续正确，但位于题面/gold终点下游：按P29额外下游不加分、不扣分。主链关键转化获可靠支持，仅辅因子/质子未完全配平(H+未标)，属局部计量简化，不改变主要结论，档内取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：Directed gold reactions for S03/S02/S01 support the required decarboxylation, NADH/O2 hydroxylation and maleylacetate-producing ring cleavage; does not require scoring extra downstream steps.

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 必答S1-S3依次对应gold S03/S02/S01。S3酶名hydroxyquinol 1,2-dioxygenase与accepted集合精确同名；S1的2,6-dihydroxybenzoate decarboxylase是gamma-resorcylate decarboxylase的描述性同义表达，反应正确；S2的resorcinol hydroxylase为较泛名称，但反应含NADH/O2且产物正确，功能对应成立。必答酶EC均为null，未发现显式EC错配；表示/命名/EC未核使9-10与高档证据门不成立，7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

六步酶功能—反应类型对应均正确：脱羧酶(decarboxylase)、NADH依赖单加氧酶(resorcinol hydroxylase)、邻位双加氧酶(hydroxyquinol 1,2-dioxygenase，与gold酶名一致)、maleylacetate reductase、3-oxoadipate CoA-transferase、3-oxoadipyl-CoA thiolase(pcaF)，无EC大类与反应类型矛盾、无&#x27;名称为加氧酶而编号为脱氢酶&#x27;类错配。但EC覆盖不足：仅S4/S5给出EC，gold三步(4.1.1.103、1.14.13.220、1.13.11.37)全部为null，且已给的1.3.1.32、2.8.3.6在E0无冻结记录可核。属&#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：Gold enzyme rows identify gamma-resorcylate decarboxylase, resorcinol 4-hydroxylase (NADH), and hydroxyquinol 1,2-dioxygenase for the three required reactions at curation granularity; this does not verify a specific protein or missing EC.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：Gold directed reactions support substrate/product chemistry for the three required steps; extra S4-S6 are outside this required target set.

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 必答S1-S3全用Rhodococcus opacus 1G；gold对S01（hydroxyquinol开环）列出Rhodococcus opacus物种记录，但S02/S03的gold对应菌为Rhodococcus jostii或Rhizobium sp.等，且1G无TaxID/保藏号/基因组冻结证据。物种级R. opacus与部分步骤相容，菌株级身份及多步催化能力仍未核实；P. putida KT2440身份合理但属下游且无冻结性状事实。属合理候选+部分支持、关键菌株/作用范围待核，5-6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

S3(hydroxyquinol 1,2-dioxygenase)对应菌 Rhodococcus opacus 与gold物种级记录一致(BSY-e00139, taxid 37919)，构成一条可靠物种级对应；S1/S2 gold列 Rhizobium sp. MTP-10005 与 Rhodococcus jostii，答案给 Rhodococcus opacus 1G，gold非穷尽且同属Rhodococcus在场景内合理，E0无法核验菌株1G，故登记UNRESOLVED而非已核实错配；S5/S6用 Pseudomonas putida KT2440 承载β-酮己二酸途径属经典组合，但TaxID 160488在E0无记录(GAP-121-026/027)。身份粒度：声称菌株1G而仅具物种层可核性，且TaxID/保藏号均为null，属&#x27;若干关键身份仍未充分核验&#x27;，未出现已核实的跨属/无关类群或单步菌写成全路径菌的已证明情形，5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_121：Gold step-level organism records include Rhodococcus opacus species for the hydroxyquinol dioxygenase step and other organisms for S02/S03; they do not establish strain 1G identity or its capability for all assigned steps.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> R. opacus 1G的Gram阳性、无运动性等与物种级gold一致；但F7碳源/F9脱羧酶活性等关键能力无冻结证据，且部分性状以属级知识外推到1G。P. putida KT2440的30°C、好氧、革兰氏阴性、杆状、运动、NC_002947/GC 61.5等大多合理，但本案无对应冻结trait记录，不能视为已核实。多项关键性状为null或UNRESOLVED，属部分准确、关键证据不足，5-6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状多为物种/属级常识且与gold物种级观测方向一致：Rhodococcus opacus 不运动(trait_gold presence of motility=false)、革兰氏阳性(gram positive=true)、不产孢与棒杆状属合理但gold为No robust majority；Pseudomonas putida KT2440 革兰氏阴性、直杆菌、极生鞭毛、约30 °C、GC约61.5% 属种级公认值。关键缺口与风险：①ORG_001有7项为null(F2温度/F3 pH/F4盐度/F5保藏/F8/F14基因组/F15)，而gold对 R. opacus 有温度、pH、盐度、基因组观测，属完成度不足(主归D1，此处按适用性扣)；②&#x27;可利用γ-resorcylate作为唯一碳源与能源&#x27;实质支撑目标污染物降解能力(按CG14口径属应用关键声称)，E0无记录(GAP-121-040…044)保持UNRESOLVED；③F5 DSM 6125 与KT2440的对应关系无记录(GAP-121-050/051)，不得凭记忆判定；④&#x27;专性好氧&#x27;相对gold的aerotolerant=true略强。属&#x27;部分性状准确且适用，但关键项证据不足或条件解释需修订&#x27;，5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_121：Species-level representative traits for Rhodococcus opacus include motility=false and gram positive=true; other answer traits and all P. putida KT2440 traits are not covered by this frozen slice.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_121：Marks which Rhodococcus opacus traits are scoreable observed_accuracy versus completeness-only; P. putida rows are absent.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案全部证据条目的source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；决策相关组与核心组只能登记MISSING_SOURCE，无法从答案交付追到可定位条目。没有已核VERIFIED_MIS_CITATION_*，因此不触发错引cap；但重要结论几乎无法外部定位，D5落在1-2档，因仍有claim_scope层面的内部映射而取2。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry共4条(EVID_001–EVID_004)，source_type全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，仅以claim_scope自述支持范围；无任何可定位文献、数据库条目或计算记录，也无法从路径/酶菌/性状追到条目级证据。按六状态：CORE组(CG01/CG02/CG03/CG05/CG07/CG09)与APPLICATION_CRITICAL组(CG08/CG17)及SUPPORTING组均记MISSING_SOURCE——属缺失而非误导，故不触发cap；决策相关组无任何条目级可定位结论，不能进入5–6档；全部组缺失落低分档。同时正向可定位支持(S1–S3化学与R. opacus物种级性状)已登记在事实核验层，不回填来源状态、不上调档位。取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确标注内部知识、把不确定EC与菌株信息置null，uncertainties逐条列出路线未核对、EC不确定、R. opacus 1G性状多为未知、S3产物互变等限制；观测/推断/未知区分总体清楚，未系统性把预测写成实证。少量步骤菌/性状置信度相对其低来源略高，但不构成系统性误导；7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界披露质量高：每个step有uncertainty字段，逐步标注confidence(medium/low/unknown)；uncertainties数组明确写出&#x27;e EC 1.3.1.32为记忆值&#x27;、&#x27;脱羧酶EC未能确定置null&#x27;、&#x27;对应菌来自文献记忆，未核对原始文献&#x27;、&#x27;路线名未与原始数据库核对&#x27;、&#x27;S3开环直接产物为烯醇式并自发互变，本答案合并为一步&#x27;、&#x27;S5/S6可视为替代对应菌&#x27;；未知性状一律null并标unknown而非填满；主动说明氧条件题面为null但路线本身好氧。未见把预测/推断写成实证观测，未见掩盖矛盾。轻微不足：EVID_001以medium置信包装整体记忆性主链、个别物种级性状(如专性好氧)未标注属级外推，属单点过度确信而非系统性误导，档内扣。7–8档取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`31a891b2152bd417df06439d5aff7da47b213e0493f9bfbd494d828d8671ff5c`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> All three required gold main-chain transformations are present in order: S1 decarboxylation of 2,6-dihydroxybenzoate to resorcinol, S2 hydroxylation to hydroxyquinol, S3 ring cleavage to maleylacetate. Route name is correct, each step has an enzyme and organism, and all 15 trait fields are present. Minor issues: S2 EC is null, S4 is an extra downstream step beyond the gold terminal and is not separated as downstream continuation, and the organism has no strain/TaxID. Thus 7–8 band, choose 8; not 9–10 because of the extra out-of-scope step and missing EC.

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的模块均有实质交付：route_scope.chosen_route_name 原样回显“γ-resorcylate degradation II”；4步均给主底物/主产物英文名+SMILES、酶对象与对应微生物；单一生物去重为 ORG_001 并由各步引用；15项性状按展示顺序全部出现（9项填值、6项明确未知，omitted=0）；不确定性字段与模板字段（es验证、error）均已填写。未见格式损坏或范围偏离到其他路线。扣分：只有1个profile被同时标注为完整路径菌（应说明依据）、uncertainties仅1条、结论级来源字段实质未满足（来源问题主要在D5扣分）；S4为题面/gold终点Maleylacetate之外的下游步，按四.2/P29只属范围外延续，不加分也不扣分。综合落在7–8档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_121：Confirms three-step required gold main chain for completeness; it does not require extra branches or additional downstream steps.
- QUESTION_TEXT / QUESTION#BIOPATH150_121：Requires the named route, per-step substrate/product/enzyme/microorganism, and 15 traits; does not authorize unseparated extra downstream steps as required main route.
- ANSWER_TEXT / ANSWER#steps：Shows the three required transformations are present and that S4 is extra; supports completeness observation only.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> The three required transformations are chemically coherent: decarboxylation to resorcinol, hydroxylation to hydroxyquinol, and ring cleavage to maleylacetate. The extra maleylacetate-to-3-oxoadipate step is a plausible downstream reaction but lies beyond the gold terminal. Main-chain cofactors/H+/O2/NADH/H2O are largely omitted, which is a local metering/simplification defect rather than a main-chain break. Representation charge/stereo issues noted by the route diagnosis do not change the named chemistry. Thus 7–8 band, choose 8; not 9–10 because cofactors are not complete and S4 is outside the specified gold endpoint.

<details><summary>V0.4理由与本行变化背景</summary>

主链三步与gold逐步对应、方向一致且连续：S1 2,6-二羟基苯甲酸根脱羧→间苯二酚(+CO2)（对应gold S03 可逆脱羧）；S2 间苯二酚4-羟化→羟基醌(1,2,4-苯三酚)（对应gold S02，gold产物即为1,2,4-Benzenetriol）；S3 羟基醌1,2-二氧合开环→马来酰乙酸（对应gold S01，产物与gold terminal BSY-c12566 相同）。SMILES基本正确：间苯二酚为1,3-二羟基苯，马来酰乙酸与3-氧代己二酸碳数与官能团与gold一致。S4（马来酰乙酸→3-氧代己二酸）位于gold终点之外，属下游延续，按P29/P157不加分不扣分。扣分点：S2/S3/S4 的共底物与辅因子（O2、NADH、H+、NAD+、H2O）全部缺失，字面计量不成立（如间苯二酚→羟基醌需引入来自O2的氧）。按P103/P155 这属局部计量缺陷，D2在7–8档内处理，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：Shows the required decarboxylation, hydroxylation, and ring-cleavage chemistry; supports product/order comparison, not specific protein activity.
- ANSWER_TEXT / ANSWER#steps：Shows named chemistry; extra S4 is downstream of the gold terminal.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 本题必答目标反应为3步：S03入口脱羧、S02中间羟化、S01末端开环至Maleylacetate。答案S1/S2/S3分别覆盖这三步；S4为Maleylacetate下游延续，超出gold终点，不作为D3a目标信用。S01（答案S3）给hydroxyquinol 1,2-dioxygenase/EC 1.13.11.37，与accepted集同名同EC，底物/产物化学等价，可作为唯一较明确可用目标；S02（答案S2）给resorcinol 4-monooxygenase且无EC，accepted为resorcinol 4-hydroxylase (NADH)/1.14.13.220，名称/EC配对未核；S03（答案S1）给2,6-dihydroxybenzoate decarboxylase/4.1.1.98，accepted为gamma-resorcylate decarboxylase/4.1.1.103，显式EC不符且无冻结证据核验。两者均保持U，不自动判F。无已确认F/M/H，亦无已确认KEY失败可触发D-KEY4；但3个目标中仅1个有明确accepted支持，其余2个MAJOR/KEY仍U，属于C05“少数目标可用”，故在&#91;3,4&#93;内取偏低分3而非上沿4。

<details><summary>V0.4理由与本行变化背景</summary>

S3 羟基醌1,2-二氧合酶 EC 1.13.11.37 与gold酶名+EC逐字一致，属可靠对应；S2 仅给名称“Resorcinol 4-monooxygenase”而未给EC（题面允许未知填null，不算编造），其功能类型与gold resorcinol 4-hydroxylase (NADH)（EC 1.14.13.220）一致；S1 脱羧酶功能类型正确，但EC 4.1.1.98 与gold gamma-resorcylate decarboxylase EC 4.1.1.103 冲突，而E0无该EC条目（GAP-121-010），无法核对accepted name/reaction → 按四.5/P66/P73 记UNRESOLVED待核，不cap；S4 马来酰乙酸还原酶 EC 1.3.1.32 在gold终点之外且E0无该EC条目（GAP-121-004），同记待核。整体为“有合理候选与部分支持、若干关键步骤仍缺具体核验”的5–6档，S3有逐字支持的强项，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / S1：声称2,6-dihydroxybenzoate decarboxylase、EC 4.1.1.98用于入口脱羧
- ANSWER_TEXT / S2：声称resorcinol 4-monooxygenase且EC为null用于resorcinol羟化
- ANSWER_TEXT / S3：声称hydroxyquinol 1,2-dioxygenase、EC 1.13.11.37用于开环
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：本题accepted酶行：S01 hydroxyquinol 1,2-dioxygenase/1.13.11.37；S02 resorcinol 4-hydroxylase (NADH)/1.14.13.220；S03 gamma-resorcylate decarboxylase/4.1.1.103
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：定义目标主反应：S03 2,6-Dihydroxybenzoate→Resorcinol+CO2；S02 Resorcinol→1,2,4-Benzenetriol；S01 1,2,4-Benzenetriol→Maleylacetate
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_121：路线BSY-p00861的gold终点主产物为Maleylacetate

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> All steps assign the same organism, Rhizobium radiobacter, with no strain and no TaxID, supported only by EVID_002 (INTERNAL_KNOWLEDGE_ONLY). The complete_pathway_organism_profile_id = ORG_001 also asserts whole-path capability. Gold organism rows include Rhizobium sp. MTP-10005 and Rhodococcus jostii for various steps and a PATHWAY_COMPLETE row for Rhodococcus jostii, but gold is not exhaustive and no frozen evidence proves R. radiobacter cannot do this. The candidate is plausible at genus level but key identity and whole-path capability are unverified, fitting 5–6; choose 5.

<details><summary>V0.4理由与本行变化背景</summary>

答案全链只给一个物种 Rhizobium radiobacter（无株系、无TaxID、无保藏号），并把 ORG_001 标为 complete_pathway_organism_profile_id，等于声称该菌完成整条 γ-resorcylate degradation II 主链。gold各步所列菌为 Rhizobium sp. MTP-10005、Rhodococcus jostii、Paraburkholderia phenoliruptrix、Sphingomonas sp. RW1、Burkholderia sp. AK-5、Rhodococcus opacus、Corynebacterium glutamicum，PATHWAY_COMPLETE 为 Rhodococcus jostii(132919)；答案物种不在其列——但gold非穷尽，按四.5/四.4 不得仅因与gold不同判错。答案侧证据仅 EVID_002(INTERNAL_KNOWLEDGE_ONLY)，E0对 Rhizobium radiobacter 无任何记录；身份定位、反应级能力、完整路径能力三层均缺适用证据（v0.3/P69），且单菌完成整链属强声称而零依据说明。属“有合理候选与部分支持、关键身份与作用范围未充分核验”的5–6档；因缺少株级身份与路径能力依据，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_121：Shows gold-listed organisms and the gold PATHWAY_COMPLETE organism; does not list Rhizobium radiobacter and does not prove it incapable.
- ANSWER_TEXT / ANSWER#steps：Shows the claimed species, absence of strain/TaxID, and whole-path assertion.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> All 15 trait fields are present. Six are explicitly null/unknown and are not treated as errors. Filled values include optimum 28 C, aerobic, motile, rod-shaped, Gram-negative, non-spore-forming, habitat plant/rhizosphere, and F8 degradation of γ-resorcylate/resorcinol/hydroxyquinol. These values lack locatable evidence and are mostly low confidence; F8 is a capability claim on internal EVID_001. No frozen trait record for R. radiobacter is present, so accuracy cannot be verified. Many honest nulls and no shown contradiction keep this out of the lowest band, but key trait evidence is insufficient: 5–6, choose 5.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部按展示顺序出现：9项填值（F2温度optimum 28/嗜中温、F1 aerobic、F6 aerobic/oxygen、F8降解γ-resorcylate/间苯二酚/羟基醌、F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming、F15 soil and rhizosphere; plant pathogen），6项明确未知（F3、F4、F5、F7、F9、F14）。填报值对 Rhizobium radiobacter 的物种级常识而言大体相符，但除F8外 evidence_id 全为 null、置信多为low/unknown；F8 以 EVID_001(INTERNAL_KNOWLEDGE_ONLY) 声称该菌降解目标污染物与其中间体，属把路径能力当性状且无适用证据。E0对 Rhizobium radiobacter 的各性状子字段均登记 NO_TRAIT_RECORD_IN_SNAPSHOT（GAP-121-028~033），全部数值与类别无法核验；F15 亦为无来源的栖息地描述。属“部分性状准确且适用、关键项证据不足”的5–6档；因全部无来源且关键项（温度上下限、pH、盐度、基因组、保藏号）缺失，取5。缺失项按P112主要归D1完成度，D4不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_121：Shows frozen trait scoreability for gold-listed organisms; no R. radiobacter row, which limits verification but is not proof of falsity.
- ANSWER_TEXT / ANSWER#organism_profiles：Shows the filled values, explicit nulls, and confidence labels.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> Only two evidence entries are provided, both source_type INTERNAL_KNOWLEDGE_ONLY, with database/record_id/locator null and only broad claim_scope. Core route, enzyme, organism, and trait conclusions cannot be traced to any locatable source. This is MISSING_SOURCE across decision-relevant groups, not verified mis-citation. D5 1–2 band fits; choose 2 because an evidence registry exists but contains only internal-knowledge labels, not usable citations.

<details><summary>V0.4理由与本行变化背景</summary>

答案的 evidence_registry 只有两条（EVID_001、EVID_002），source_type 均为 INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 全为 null，且同一EVID_001被用于路径、反应、酶与性状——按四.3 属 MISSING_SOURCE（仅有自我声明），不属 GENERIC_SOURCE（连库名/模型名/文献列表都没有）。决策相关组（CG01路线核心步骤、CG02起点、CG03终点、CG05酶-EC、CG07核心菌身份、CG09完整路径能力）全部缺失条目级可定位记录，无任何可核对来源；按P41“全部缺失→低分档（默认不cap）”，且落“几乎无法定位重要结论依据”1–2档。取2（内部是最低档，因答案以结构化 claim_scope 明确了每条证据是什么、并未伪造引用或条目号，略高于1）。无已核实错引：E0为整题EVIDENCE_GAP，按四.6/P51 查不到一律UNRESOLVED，不判虚构、不判CONTRADICTED、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#evidence_registry：Shows both evidence entries are INTERNAL_KNOWLEDGE_ONLY with no database/record/locator; supports MISSING_SOURCE assessment.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer clearly marks many unknowns as null, uses low/unknown confidence for many traits, exposes INTERNAL_KNOWLEDGE_ONLY source_type, and lists one EC uncertainty. However, it also makes broad whole-path and F8 degradation-capability claims at medium confidence with no locatable source and does not closely bound the extra downstream step. Disclosure is partial and some conclusions exceed evidence, but it is not systematic prediction-as-observation. 5–6 band, choose 6 because null/unknown disclosure is relatively clear.

<details><summary>V0.4理由与本行变化背景</summary>

正面：大量未知被如实标出——6项性状 value=null 且 confidence=unknown，F2/F1/F6/F10–F13/F15 标 low，S2 明确写 uncertainty=&#x27;EC number not specified&#x27; 并列入 uncertainties&#91;0&#93;；未编造EC、TaxID、保藏号或数值，符合题面“未知填null”的诚实要求。不足：结论强度多处超过依据——S3 酶-反应以 confidence=high 标注却只指向 INTERNAL_KNOWLEDGE_ONLY；四个步级微生物均 medium 而零来源；complete_pathway_organism_profile_id=ORG_001 的整链能力声称无任何限制说明；未披露“全链单菌、无株级身份、与gold所列菌不一致（Rhizobium sp. MTP-10005 / Rhodococcus jostii 等）”这一主要限制。属“有不确定性说明但过于笼统、部分结论强度仍超过依据”的5–6档；因未知标注覆盖面较广、缺的是主要限制说明而非全面失实，取6。非系统性把预测写成实证，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#uncertainties：Shows explicit unknowns and internal-knowledge labels, but also shows medium-confidence broad claims.

</details>

## Kimi

答案SHA256：`88970ef093e39ec1cae5a70f33c3d95228383db48240359a1ef5ff548a85e2c6`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案返回单个可解析JSON，route_scope.chosen_route_name逐字为γ-resorcylate degradation II；4个step均给出底物/产物英文名、SMILES、酶/EC字段（S2 EC为null但题面允许未知填null）、对应微生物；同一菌Rhizobium sp. MTP-10005以单一ORG_001去重；15项性状全部出现，未知项按null/unknown填写。S4把maleylacetate向下游延伸到3-oxoadipate，超出gold终点Maleylacetate，但题面未显式写终点且任务合同task_conformance=OK，属少量范围扩展而非核心模块缺失或严重偏离，因此不构成D1关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

题面指定路线名γ-resorcylate degradation II原样填写；4步均给底物/产物英文名+SMILES、首选酶与EC、对应微生物；15项性状全部出现；evidence_registry与uncertainties齐备，格式合规。缺口仅属完成度：ncbi_taxid全null、多数gene_or_protein null、5项性状诚实null。属‘大部分必要内容完整、仅少量遗漏’的7–8档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_121：题面要求指定路线名、逐步底物/产物/SMILES、首选酶+EC、对应微生物、同一菌去重及15项性状返回。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_121：本题gold主链为LINEAR_UNIQUE、ordered_step_count=3，任务范围以指定路线主链为界。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_121：路线名为γ-resorcylate degradation II，gold终点主产物为Maleylacetate。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际交付4步主链、单一去重菌profile及15项性状，字段结构完整可读。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链三步有机转化与gold一致：2,6-dihydroxybenzoate脱羧为resorcinol+CO2；resorcinol经O2羟化为hydroxyquinol；hydroxyquinol经O2开环为maleylacetate。方向均为底物到产物，无反向、无第一步核心错误、无原子明显不守恒的无说明跳步。S2未列NADH/NAD+，S3未列H+，S4（超出gold终点）也未列NADH；按P103，主有机物转化正确而辅因子遗漏通常为局部计量缺陷，D2在7–8档处理且不自动cap。S4超出题面gold终点Maleylacetate，属额外下游延续，不据此加重D2；因此给8而非更低或9（程序亦限定D2上限8）。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold三步一致：S1非氧化型脱羧2,6-DHB→resorcinol+CO2（对应gold S03，方向/可逆性一致）；S2 resorcinol单加氧羟化→hydroxyquinol（对应gold S02，NADH作辅因子未列属局部计量缺陷）；S3 hydroxyquinol 1,2-双加氧开环→maleylacetate（对应gold S01）。SMILES与1,3-二羟基苯、1,2,4-苯三酚、maleylacetate、3-oxoadipate一致。S4 maleylacetate→3-oxoadipate为gold终点外下游延续，四.2/P29不加扣分。主链成立、局部辅因子简化，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：gold三步主链方向为2,6-Dihydroxybenzoate→Resorcinol(+CO2)；Resorcinol+NADH+O2+H+→1,2,4-Benzenetriol+NAD++H2O；1,2,4-Benzenetriol+O2→Maleylacetate+H+。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_121：gold终点主产物为Maleylacetate，S4转化为其下游延续。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S1-S3有机主产物与gold一致；S2缺NADH，S3缺H+，S4为额外下游且缺NADH。
- RUBRIC_CLAUSE / P103：主有机物转化正确但辅因子遗漏通常为局部计量缺陷，D2在7–8档处理，不自动cap。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 逐目标步看：gold S01（hydroxyquinol→maleylacetate）在答案S3给出hydroxyquinol 1,2-dioxygenase、EC 1.13.11.37，与accepted集合精确一致，可确认S。gold S02（resorcinol→hydroxyquinol）在答案S2给出resorcinol hydroxylase但EC=null，名称不是accepted全名resorcinol 4-hydroxylase (NADH)，为U。gold S03（2,6-dihydroxybenzoate→resorcinol）在答案S1给出gamma-resorcylate decarboxylase但显式EC 4.1.1.106与accepted的4.1.1.103不一致，显式EC配对未核，按C03记U而非F。故S=1、U=2、无已确认F/M；KEY步为U不触发D-KEY4。主链酶功能有部分适用支持但两个主要/关键步仍未确认，不能进入7–8高档，也不应把U当失败压到3–4；按部分主干支持档取5，未取6因仅1/3目标达到精确S且入口步显式EC配对仍有明确缺口。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶功能与反应类型匹配：S1脱羧酶、S2羟化单加氧酶、S3 hydroxyquinol 1,2-dioxygenase(EC 1.13.11.37，与gold一致)、S4 maleylacetate reductase(EC 1.3.1.32)。S1 EC 4.1.1.106与gold 4.1.1.103存在数字差异，E0=GAP无法核官方accepted name/reaction，按四.5/P66记UNRESOLVED不判错；S2 EC诚实null。主要步骤酶对应成立、少数EC待核，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：accepted酶：S01 hydroxyquinol 1,2-dioxygenase EC 1.13.11.37；S02 resorcinol 4-hydroxylase (NADH) EC 1.14.13.220；S03 gamma-resorcylate decarboxylase EC 4.1.1.103。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：三个必答目标反应及其主底物/主产物方向，用于核对答案酶是否对应目标反应而非旁支。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S3酶与EC精确命中accepted；S2缺EC且名称非accepted全名；S1名称成分对应但显式EC 4.1.1.106与accepted 4.1.1.103不一致。
- RUBRIC_CLAUSE / C05：D3a档内判据：部分主干目标有适用支持、主要/关键待核阻止进入良好档时停在&#91;5,6&#93;下沿。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> Rhizobium sp. MTP-10005 identity is supported by gold (TaxID 267998 in organism_gold), and the organism assignments for the S01 and S03 required steps are supported. However S02 is assigned to Rhizobium although gold S02 organism rows list only Rhodococcus jostii, and complete_pathway_organism_profile_id=ORG_001 claims whole-path capability without direct full-path support. This is partial support with key scope unresolved: 5-6 band, lower half. No verified key error.

<details><summary>V0.4理由与本行变化背景</summary>

核心微生物Rhizobium sp. MTP-10005为gold STEP记录中的真实菌（gold TaxID=267998），S01/S03两步gold即列此菌；身份真实、菌株选择正确，无身份编号编造或跨类群错配。ncbi_taxid诚实null。差异点：第2步resorcinol羟化酶归Rhizobium（gold该步为Rhodococcus jostii），以及整条路径能力归Rhizobium（gold PATHWAY_COMPLETE为Rhodococcus jostii 132919）——E0=GAP无反应级/整路径能力记录，保持未核，未推翻主要微生物推荐。主要身份有可靠支持、少量步级归属与能力待核，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_121：Gold confirms Rhizobium sp. MTP-10005 on S01 and S03, but S02 rows list Rhodococcus jostii and the PATHWAY_COMPLETE row is Rhodococcus jostii (TaxID 132919). Absence of a Rhizobium complete-path row is not proof against Rhizobium.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：Gold enzyme-organism rows support the two Rhizobium step associations but do not establish Rhizobium whole-path completion.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> All 15 trait slots are present: 10 filled, 5 explicit null. Filled traits are mostly genus-level/low-confidence and not strain-specific; gold Rhizobium trait rows are largely UNKNOWN, so they cannot be positively verified. The answer does not present unverified genus-level traits as high-confidence strain observations, and no verified numeric/unit/range contradiction is present. 5-6 band, upper half.

<details><summary>V0.4理由与本行变化背景</summary>

15项全部出现，10项填写、5项诚实null（温度/pH/盐度/保藏/基因组），无编造定量值。已填性状为属水平定性推断（革兰氏阴性、杆状、可运动、不产芽孢、土壤根际），均标low/medium置信并注内部知识来源。关键定量性状（温度/pH/盐度/基因组）全缺，且gold对Rhizobium MTP-10005全项UNKNOWN、E0无官方性状记录，均无法核实数值适用性。属‘部分性状准确且适用，但关键项证据不足’的5–6档，取低5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_121：Gold Rhizobium sp. MTP-10005 trait rows are mostly UNKNOWN; only identity-related TaxID 267998 appears. This does not verify the answer&#x27;s filled traits and does not prove them wrong.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_121：Most Rhizobium traits are completeness_only with no observed value; observed-accuracy scoring is therefore not available for those traits.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer associates claims with evidence IDs and claim scopes, but core sources are a named MetaCyc pathway without a record_id and a vague literature series; many traits rely on INTERNAL_KNOWLEDGE_ONLY. E0 is a case-level EVIDENCE_GAP, so no mis-citation can be verified. Source traceability is partial and not entry-level verifiable: 5-6 band, lower half.

<details><summary>V0.4理由与本行变化背景</summary>

答案对每条主链、酶、菌与性状均给出evidence_id映射（EVID_001 MetaCyc路径名、EVID_002 MTP-10005文献、EVID_003属水平内部知识），实现claim到来源的对应，属‘部分关键结论可定位’。但：EVID_001/002均无record_id、无DOI/确切年份，EVID_003为INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；E0=EVIDENCE_GAP无法核对任何来源实际支持内容，全部记UNRESOLVED，不冒充已证实错引、不判虚构。决策相关组无VERIFIED_MIS_CITATION，severity=NOT_APPLICABLE，不cap。记录指向具体路径与菌株但记录级信息不完整，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Answer delivered database/literature/internal-knowledge locators and claim scopes; D5 evaluates only these delivered records and confirms no verified mis-citation in E0.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_121：Gold confirms the case/pathway identity but does not supply the answer&#x27;s actual source records.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> Uncertainty disclosure is strong: the answer flags route I/II strain-assignment uncertainty, EC 4.1.1.106 uncertainty, unknown resorcinol hydroxylase EC, missing TaxID/genome/physiology values, genus-level trait inferences, and maleylacetate reductase gene-cluster uncertainty. It distinguishes unknown/null from filled content and does not systematically present predictions as observations. 7-8 band, upper half; not 9-10 because some source-confidence claims remain stronger than the case-level evidence gap can support.

<details><summary>V0.4理由与本行变化背景</summary>

答案区分观测/推断/未知较清晰：每步标high/medium/low/unknown置信，uncertainties逐条列出EC归属、TaxID/基因组/温度等未知，厌氧替代分支明确标is_part_of_scored_main_route=false，属水平推断显式注‘属水平推断/内部知识’。主要限制与冲突已披露。轻微问题：EVID_001/002标DATABASE_DIRECT/LITERATURE_DIRECT而record_id null，属单点来源类型包装偏强，但不构成系统性误导、未见掩盖矛盾。属7–8档，取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Answer explicitly lists route/EC/TaxID/trait/gene-cluster uncertainties and labels several traits as genus-level or low confidence.

</details>

## Qwen

答案SHA256：`1edf707e0c2d2ccb80a920336493eb244e06d1133e17d3784793c5223b809a1f`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 题面要求的指定路线名已原样填写，主链步骤、逐步酶与微生物字段均给出；但15项性状全部为null/unknown且无性状来源，属于对必要性状模块的实质占位而非完成，故仅在部分可用档。另有超出终点的下游步骤S4，按P29不额外加分、不因此扣D2范围分，但在D1完整性上也仅属关联可辨。

<details><summary>V0.4理由与本行变化背景</summary>

结构层完成度高：route_scope.chosen_route_name原样回填题面指定路线（未改选）、氧条件null原样保留、4步均给出主底物/主产物英文名与SMILES、每步各1个酶与1个微生物、organism_profiles按物种去重并由step引用、15项性状键齐全、uncertainties与逐step uncertainty齐备。扣分点：唯一profile的15项性状value全为null（明确未知，按P15不计为遗漏或错误，但按P112性状完成度扣分主归D1）、S2酶EC为null、同一物种覆盖全部四步而未给菌株级身份。属“主要模块均有涉及、若干必要内容未实质填充”的5–6档偏上，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_121：题面要求指定路线、逐步主底物/主产物、首选酶/EC、对应微生物，并要求填写15项性状及最强来源。
- ANSWER_TEXT / ANSWER：答案给出4步及逐步酶/菌，但15项性状全部为null/unknown，且无性状来源。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：gold主链为3个必答步，终点主产物为Maleylacetate；用于核对主链覆盖与额外下游步。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 主链关键化学转化与方向基本正确：2,6-DHB脱羧到resorcinol，resorcinol羟基化到hydroxyquinol，hydroxyquinol开环到maleylacetate，符合gold的三步方向与终点。局部问题为S2使用NADPH而gold accepted为NADH依赖的resorcinol 4-hydroxylase，且S3产物未列H+；这些属于局部计量/辅因子层面的问题，按P103在7-8档处理。S4为终点下游延续，按P29不加分也不据此扣分。D2不得9-10。

<details><summary>V0.4理由与本行变化背景</summary>

主链三步化学与冻结gold逐点吻合且顺序/方向正确：S1 2,6-二羟基苯甲酸根(+H+)脱羧→间苯二酚+CO2（原子与电荷配平，与gold S03同向）；S2 间苯二酚经O2/还原力羟化→1,2,4-苯三酚（hydroxyquinol，SMILES与gold BSY-c02714一致）；S3 1,2,4-苯三酚邻位开环→马来酰乙酸（与gold terminal BSY-c12566一致）。S4 马来酰乙酸→3-氧代己二酸超在题面/gold终点之外，按P29属下游延续，不加分也不扣分。局部缺陷：S2/S4用NADPH而gold记录NADH（辅因子替换）、S3产物以二价阴离子书写字面缺2H（答案自述质子化/互变异构未细化），按P103/P104为局部计量与表达问题，不构成不守恒cap。故7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：gold三步反应、方向及S01-S03主底物/主产物；含S02 NADH与S01 H+产物。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_121：gold终点主产物为Maleylacetate，用于判断S4属于终点外下游延续。
- ANSWER_TEXT / ANSWER：答案主链S1-S3化学转化及S4下游延续；S2辅因子为NADPH，S3未列H+。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 三个必答目标反应的酶信息均有交付，酶名在功能类别上大体对应脱羧、羟化与开环；但与accepted集合核对后均不能确认S：S1用EC 4.1.1.68而accepted为gamma-resorcylate decarboxylase EC 4.1.1.103，S2仅写resorcinol hydroxylase且EC null而accepted为resorcinol 4-hydroxylase (NADH) EC 1.14.13.220，S3名称hydroxyquinol 1,2-dioxygenase虽在accepted名称内但EC 1.13.11.29与accepted 1.13.11.37不一致。冻结证据为EVIDENCE_GAP，不能把这些未核配对标为已证伪或已支持，因此均保持U；无已确认KEY失败，不触发D-KEY4上界。按全U实际支持判断为部分目标有功能层线索但仍有实质核验缺口，取5。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶的功能类型与所标注反应类型自洽（脱羧酶/羟化酶/开环双加氧酶/还原酶），EC大类前缀与反应类型不矛盾；S3酶名“hydroxyquinol 1,2-dioxygenase”与gold一致、S2“resorcinol hydroxylase”与gold“resorcinol 4-hydroxylase (NADH)”同族，S1“2,6-dihydroxybenzoate decarboxylase”与gold“gamma-resorcylate decarboxylase”为同一底物的脱羧酶。但具体编号未获支持：S1 EC 4.1.1.68与gold单值4.1.1.103不同、S3 EC 1.13.11.29与gold单值1.13.11.37不同、S2 EC为null、S4在gold范围外。E0无EC条目，按四.5/四.6保留UNRESOLVED、不判错不cap；落在“有合理候选和部分支持，但关键步骤仍缺具体核验”的5–6档，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：列出本题必答步accepted酶名与EC：S03=4.1.1.103；S02=1.14.13.220；S01=1.13.11.37。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：定义三个必答目标反应及其主底物/主产物，用于判断酶名与反应功能的对应。
- ANSWER_TEXT / ANSWER：答案S1-S3显式EC与酶名；S2无EC；S4为非目标下游步。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 档位5–6：单一Cupriavidus gilardii被归属到全部4步（同一ORG_001），无strain、无TaxID、无任何可定位身份/能力记录——E0为EVIDENCE_GAP，答案侧唯一来源EVID_001为INTERNAL_KNOWLEDGE_ONLY；身份定位、步级催化归属、整链能力三层均待核，达不到7–8所需“身份与作用范围有可靠支持”。未显式声称整链能力（complete_pathway_organism_profile_id=null），故不按CG09加重。gold步级菌(Paraburkholderia phenoliruptrix/Rhodococcus jostii/Rhizobium sp. MTP-10005等)与答案不同，但gold非穷尽且无冻结证据可证伪，不登记为错配，故不入3–4档。档内取5：候选合理但零独立支持、零菌株粒度。

<details><summary>V0.4理由与本行变化背景</summary>

微生物层仅有单一物种名Cupriavidus gilardii被指派给全部四步：无strain、无TaxID、无保藏号/基因组号，evidence_id指向的EVID_001为INTERNAL_KNOWLEDGE_ONLY且confidence=low，身份定位、反应级能力、完整路径能力三层（P69/P110）均无任何可核对证据；同时以同一物种承担整条四步主链，等于隐含全路径能力声称而未给全路径或步级能力依据。gold各步菌为Rhizobium sp. MTP-10005、Rhodococcus jostii、Rhodococcus opacus、Corynebacterium glutamicum、Paraburkholderia phenoliruptrix、Sphingomonas sp. RW1等（gold非穷尽，与gold不同不自动判错），但本答案的物种身份与作用范围完全没有适配其粒度的依据，属“多处作用范围/反应能力未成立、身份粒度不足”的3–4档，取4；因E0整题GAP无法核实为错，key_error记UNRESOLVED、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_121：列出gold步级菌与PATHWAY_COMPLETE菌(Rhodococcus jostii 132919)；不支持“答案所选菌错误”，gold非穷尽，也不支持答案菌的能力。
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_121：给出已核物种名映射(如Cupriavidus necator 106590)；不含Cupriavidus gilardii映射，故该名称既未被核成也未可据此判错。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> P44：全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到科学错误。答案organism_profiles&#91;0&#93;.traits的F1–F15全部value=null、raw_text=null、evidence_id=null、confidence=&#x27;unknown&#x27;，即15项全为明确未知(filled=0/explicit_unknown=15/omitted=0)；未发生数值/单位/菌株错配或性状外推，故不按错误档评。

<details><summary>V0.4理由与本行变化背景</summary>

唯一organism_profile（ORG_001）的15项性状（F1–F15）value全部为null、confidence均为unknown、evidence_id均为null，即性状模块未交付任何可评价的数值、单位或适用条件；按P44“全部必需性状均为null/空值时D4按MISSING记1分，不宣称检测到科学错误”处理，故记MISSING=1，并在D1计完成度扣分，两处不重复重扣（P112）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_121：给出可评分性状与待裁子字段清单；用于确认参照存在，不构成答案已交付性状内容，也不回填来源。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_121：含观测/预测性状参照与培养温度≠最适温度等语义；仅判卷参照，不得回填答案缺失的性状或来源。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 全部claim组来源状态=MISSING_SOURCE：唯一evidence_registry条目EVID_001的source_type=INTERNAL_KNOWLEDGE_ONLY、database=null、record_id=null、locator只是路线文字复述，且被复用于4步与ORG_001；15项性状与S2的EC直接null无来源。P34/P41：MISSING_SOURCE落低分档且默认不cap；E0=EVIDENCE_GAP零记录，不能登记任何VERIFIED_MIS_CITATION_*，故无需cap也不判虚构。档内取2：每条结论确有evidence_id映射并统一标low confidence（优于零登记），但无任何可定位外部条目，落1–2档上沿。

<details><summary>V0.4理由与本行变化背景</summary>

全答案仅有1条来源EVID_001：source_type=INTERNAL_KNOWLEDGE_ONLY、database=null、record_id=null、locator只是把路线名与本答案步标（S1–S4/ORG_001）回写一遍，属循环自指，不构成可定位条目。按P34该情形即MISSING_SOURCE；决策相关组CG01/CG02/CG03/CG05/CG07（及CG08）全部仅有内部知识自我声明，按P41“全部缺失→低分档（默认不cap）”落1–2档，取2。无已核实错引（E0整题GAP，不得判虚构或CONTRADICTED），severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不触发关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：证明答案只交付了内部知识自述型来源，无可定位条目；不支持任何具体文献/数据库结论。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：评价侧参考记录，可用于核对酶-反应；属评价者资料，不属答案交付来源，不能回填D5。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 7–8档：证据性质区分总体清楚——每步confidence分档(medium/low)、uncertainties列出4条(氧条件未指定、resorcinol hydroxylase EC未确认、缺菌株与性状来源、下游为中心代谢推断)，central_metabolism_entry与downstream_continuation明确写作推断，未知项诚实null而非编造。未能取8：EC 4.1.1.68与EC 1.13.11.29以medium置信交付，而唯一证据为INTERNAL_KNOWLEDGE_ONLY(low)，置信与依据强度不完全相称，且这两点未逐条披露（P119单点/局部过度确信→档内扣，不cap，也不与D5连坐）。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据强度大体相称：氧条件未指定即声明“无法确认该路线是否严格好氧”；EC未知处填null并单列；明确写出“路线II的代表菌株及15项性状缺乏可核对来源，多数性状填null”；下游β-酮己二酸转化标为推断并放入downstream_continuation/central_metabolism_entry.explanation；source_type如实标INTERNAL_KNOWLEDGE_ONLY、overall confidence=low。扣分点：在无任何来源的情况下仍给S1/S3/S4酶标“medium”置信，且把内部记忆登记为带claim_scope的“证据条目”易被读成可核记录——属单点强度偏高而非系统性误导（P119），故7档而不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：证明答案显式披露氧条件未知、EC未确认、来源缺失与下游推断；不支持任何具体观测已获实证。
- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;.confidence：用于判断置信表达与证据强度是否相称；不证明EC编号对错。

</details>

## Grok

答案SHA256：`d7ec590c3ea4865c77859b26343f79e9b844c4d9cc039597f8060055d89321e9`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定γ-resorcylate degradation II，并要求每步底物/产物+首选酶及EC+一个对应微生物、15项性状。答案只交付路径与酶两个模块：3步中S2/S3无EC；step.microorganism全null、organism_profiles为空，微生物与性状整模块缺失；且程序route_status=DEVIATES（冻结路线为脱羧→resorcinol 4-羟化→双加氧开环至maleylacetate，答案改为脱羧→还原→水解）。按P100/P59属任务参数偏离，按P44属核心模块大部缺失，D1关键错误成立，在&#91;1,4&#93;取2：入口步与不确定性披露是仅有的可用内容，不抬档。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_121#question：支持题面路线锁定、每步酶/EC/微生物要求与15项性状要求；不证明任何具体酶或菌。
- ANSWER_TEXT / BIOPATH150_121#answer：支持答案实际交付的步骤、EC空缺与微生物/性状空缺；不支持其科学正确性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：支持冻结路线三步的定向底物→产物与顺序（S03脱羧→S02羟化→S01双加氧开环至maleylacetate）；不证明其他路线不存在。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所答主链化学自身可成立：S1脱羧与冻结路线一步一致；S2间苯二酚还原为环己烷-1,3-二酮（+2H，但未列电子供体，属P103局部计量缺陷，不cap）；S3环己烷-1,3-二酮水解开环为5-氧代己酸根（C6H8O2+H2O→C6H10O3，方向与计量守恒）。但主链未接至冻结终点maleylacetate，缺少羟化与双加氧两项关键转化，还原/水解两步仅有内部知识来源、缺乏独立支持。取5–6档下沿5：主干部分成立，关键中间体与连接仍需实质修订。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_121#answer：支持答案逐步底物/产物、SMILES与反应类型；不支持其催化真实性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：支持冻结主链的转化序列与主产物身份，用于判断答案中间体是否路线内结构；不证明还原/水解化学本身不存在。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> N=3（冻结三必答步）。逐目标：①入口脱羧目标（gold S03）由答案S1命中，2,6-DHB+H+→resorcinol+CO2、EC 4.1.1.103与accepted gamma-resorcylate decarboxylase/4.1.1.103一致→S；②中间步目标（gold S02, resorcinol 4-hydroxylase/1.14.13.220→hydroxyquinol）被resorcinol reductase→cyclohexane-1,3-dione取代，产物经诊断为路线外结构→F（已核为另一反应）；③终点目标（gold S01, hydroxyquinol 1,2-dioxygenase/1.13.11.37→maleylacetate）主链未交付，仅出现在声明is_part_of_scored_main_route=false的alternative_branches→M。S=1,F=1,M=1,U=0→C=1/3，落&#91;3,4&#93;；KEY终端实证缺失+KEY中间步已核F触发D-KEY4上界4，实际取3：仅少数目标可用，目标主功能严重受损。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：支持三步冻结酶名/EC（S03=4.1.1.103；S02=1.14.13.220；S01=1.13.11.37）与其步骤绑定；不证明具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：支持各步定向底物/产物与主产物身份，用于辨认替代产物为路线外结构；不评价替代路线自身化学价值。
- ANSWER_TEXT / BIOPATH150_121#answer：支持答案实际给出的酶名、EC与产物定位；不支持其已催化目标反应。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求每步一个对应微生物；答案三步的microorganism均为null，organism_profiles为空数组，仅全局声明无可稳定引用菌株。该维对应模块完全未交付，按P44记MISSING=1，不宣称检测到微生物对应错误；诚实声明未知的正面价值归D6，完成度不足归D1，不在此重复重扣。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_121#answer：支持微生物字段与profiles确为空、仅有诚实未知声明；不支持任何物种/菌株身份或能力。
- QUESTION_TEXT / BIOPATH150_121#question：支持每步须绑定一个对应微生物的交付要求。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles为空，15项性状（F1–F15）无任何值、raw_text或evidence_id；答案仅全局声明“15项性状均不编造”。按P44/P112“全部必需性状均为null/空值时D4按MISSING记1分”，不宣称检测到性状错误；缺失的完成度扣分已在D1体现，不重复重扣。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_121#answer：支持15项性状整模块未交付；不支持任何性状数值、单位或来源。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_121：仅说明本题若交付性状存在冻结参照行；不用于给未交付内容补分。

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 交付来源全部为INTERNAL_KNOWLEDGE_ONLY（EVID_001/EVID_002）与MODEL_INFERENCE（EVID_003），按P34属MISSING_SOURCE→低分档；但locator含具体文献题录（Tschech &amp; Schink 1985, Arch Microbiol 143:52-59）与KEGG R03543反应式，并以claim_scope逐条绑定S1–S3，优于纯笼统文献列表；S2/S3无条目级来源。本题E0=EVIDENCE_GAP，无法核验引用，按P40/P51不判错引、不据此cap，仅按已知交付来源事实定档。取3–4档上沿4。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_121#answer：支持来源类型自述、locator具体性与claim_scope映射关系；不支持其内容已被检索或核实。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：仅用于辨识答案所引EC/反应是否与冻结路线一致，不作为答案自身交付来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案逐证据标注source_type（INTERNAL_KNOWLEDGE_ONLY/MODEL_INFERENCE）与confidence，uncertainties明确列出路线名→化学映射未经数据库页面核对、若实为好氧Rhizobium路线应改主链、还原酶EC与电子供体未知、水解酶EC未知、下游发酵未入主链；未知处诚实留null未编造，证据性质与边界基本清楚。扣分点为单点过度确信：S1以记忆来源给high confidence、route_summary以较确定语气称“厌氧发酵主链”，属P119档内扣，非系统性误导。给7–8档上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_121#answer：支持证据类型标注、置信度与不确定性披露的具体内容；不支持这些披露已被外部核实。

</details>

## GPT5.6

答案SHA256：`dbb8825bd31780f84bb54bf31ae2244162945a2d5e70165948633b3d847fd76d`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 1–2档：大部分必要内容缺失；仅入口脱羧步可辨认，缺S02/S01两个主链步、全部微生物和15项性状。路线名与氧条件留空正确，但不能弥补核心交付缺失。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_121：支持本题为3步LINEAR_UNIQUE任务；不证明各步化学或菌株能力。
- ANSWER_TEXT / ANSWER.steps：支持答案只交付一步且未交付微生物/性状；不证明缺失步骤内容。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 5–6档：入口2,6-Dihydroxybenzoate脱羧为resorcinol并释放CO2与gold S03一致，方向与主要产物正确；但只完成1/3主链，关键下游resorcinol→1,2,4-benzenetriol→maleylacetate缺失，连续性严重不足。无已核化学矛盾，故不按D2关键错误cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：支持入口脱羧的底物/产物/CO2；不支持未交付的S02/S01。
- ANSWER_TEXT / ANSWER.steps：支持答案只给出入口步；不证明下游化学。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S03入口酶名gamma-Resorcylate decarboxylase与accepted名称匹配，底物/产物正确；但无EC，S01/S02两个KEY目标未交付。按C04：可判S=1、M=2、N=3，C=1/3落&#91;3,4&#93;；D-KEY4因KEY漏交付触发≤4，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_121：支持S03反应与S01/S02为独立必答步；不支持答案已交付S01/S02。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_121：支持S03名称级酶对应及accepted集合；不支持答案未给出的EC或菌株能力。
- ANSWER_TEXT / ANSWER.steps：支持仅入口名称级交付、无EC、无后续步；不证明缺失步错误。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 微生物模块整体未交付：organism_profiles为空，steps&#91;*&#93;.microorganism均为null，无物种/菌株/TaxID/保藏号或单步/整路能力声称。按MISSING=1，不宣称发现科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：支持微生物模块未交付；不支持任何身份或能力判断。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 性状模块整体未交付：无organism_profiles，因而不存在任何profile的15项性状；回答不确定项说明也未提供逐项null结构。按MISSING=1，不宣称发现科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：支持15项性状整体未交付；不支持具体性状值判断。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5低档：唯一证据EVID_001为INTERNAL_KNOWLEDGE_ONLY，无database/record/locator，无法把入口反应追到条目级来源；CORE路线/酶组均为MISSING_SOURCE。没有已核实错引，故不作D5关键错误cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：支持唯一证据是内部知识且无定位；不支持其为外部可核来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 7–8档：答案明确列出下游、菌株和EC未知，酶confidence=low，来源标为内部知识；没有把未核实蛋白/菌株写成实证。&#x27;可可靠确定&#x27;措辞略强，但整体限制披露具体，非系统性误导，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持答案明确披露下游、菌株、EC未知；不支持这些事实已获外部验证。

</details>
