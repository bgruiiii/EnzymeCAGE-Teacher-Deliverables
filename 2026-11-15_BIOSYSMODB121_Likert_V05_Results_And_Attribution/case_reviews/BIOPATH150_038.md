# BIOPATH150_038：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-nitrotoluene degradation I

污染物：4-Nitrotoluene；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 64 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 44 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 63 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 48 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 61.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 32 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`509c7ec56e9c9e8d2e56aebbfe55e9c65f24730a4ebb125eb10b51e2195f1e55`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 覆盖了题面指定路线所需的3个主链步骤（4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate），每步均给出底物/产物、酶与微生物，并给出两个organism_profiles及各自15项性状。route_scope名称原样保留；氧条件题面为null，答案在notes中说明按路线I推断aerobic，未改选路线。额外S4–S6属于gold终点4-nitrobenzoate下游，按P29不因此扣D1；但主链表达略超出冻结主链，且部分性状值为null，属少量工程/范围整理问题。

<details><summary>V0.4理由与本行变化背景</summary>

六个交付模块均有实质内容：6步主链（每步底物/产物英文名+SMILES、首选酶+EC或null、对应菌）、2个按物种+菌株去重的profile各含全部15项性状、证据登记与不确定性说明；route_scope.chosen_route_name原样保留题面路线名。扣分点：每个profile有5/15性状诚实null（菌株级定量/保藏/基因组几乎全缺），S4–S6为gold终点(4-nitrobenzoate)之外的延续却直接放入steps主链数组（另设downstream_continuation），氧条件自填aerobic但已在notes披露推理。属&#x27;大部分必要内容完整、少量遗漏&#x27;档，7分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_038：gold为3步LINEAR_UNIQUE、n_required=3；用于核对主链必答范围，不要求下游延续。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_038：gold起点4-Nitrotoluene、终点4-Nitrobenzoate；用于核对交付覆盖，不证明答案科学正确。
- ANSWER_TEXT / ANSWER：显示答案实际交付的steps、profiles、traits与uncertainties；仅用于完整性定位。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> S1–S3的有机主转化、方向与结构连接均正确：4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate，符合gold前3步的有向主链。S1底物/产物与gold一致，但把EC 1.14.15.26的还原型铁氧还蛋白替换为NADH/NAD+，属局部辅因子/计量表达问题；S2用醇脱氢酶/NAD+完成醇→醛，净化学转化成立，但与gold的4-nitrobenzyl alcohol oxidase/EC 1.1.3不同，属局部酶类/辅因子选择问题。S4–S6位于gold终点下游，按P29不进入本题主链覆盖率扣分。7–8档：主链与关键转化有充分依据，少量局部问题不改变主要结论；因上述辅因子/酶类表达问题不给9–10。

<details><summary>V0.4理由与本行变化背景</summary>

主链前三步与冻结gold完全一致（4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate，对应gold S02→S03→S01），方向、碳骨架与官能团变化正确，终点4-nitrobenzoate合规；S4–S6为终点外延续，按P29不进入覆盖率定档。缺陷：S1辅因子写成NADH，而官方EC 1.14.15.26反应式使用还原型铁氧还蛋白（局部辅因子/计量缺陷，按八.辅因子条款不cap）；S2以醇脱氢酶(1.1.1.90, NAD+)替代gold的4-nitrobenzyl alcohol oxidase(EC-1.1.3)，化学可行。7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：gold逐步给出4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate的SUBSTRATE_TO_PRODUCT方向与主产物；用于D2方向/连接核对。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：EC条目支持1.14.15.26的甲基单加氧反应类别；不证明答案用NADH替代铁氧还蛋白仍为同一完整反应式。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> D3a目标N=3（S01/S02/S03）；答案对应S1-S3，S4-S6超出题面终点4-Nitrobenzoate，不计入本条目标N。三个必答目标均未获确认S：S1用EC 1.14.15.26、S3用EC 1.2.1.28，虽落在accepted EC集合，但酶名均不在accepted名称中，名-EC配对仍为UNRESOLVED；S2用EC 1.1.1.90，而accepted步S03为4-nitrobenzyl alcohol oxidase/EC 1.1.3，属未接受的EC不匹配，现仅登记UNRESOLVED，无已确认催化失败证明。全部必答目标均为KEY/MAJOR U，按C05不能给7-8；但有两个目标的EC方向与accepted集合部分吻合，且无已确认F/M，故不进入&#91;1,4&#93;失败锚点，也不因自动未知直接NE。选&#91;5,6&#93;下沿5：存在部分主干目标支持，但所有名-EC配对未核、一个目标EC不在accepted集合，尚无确认的逐反应S支持，不足以上6。

<details><summary>V0.4理由与本行变化背景</summary>

S1 EC 1.14.15.26与gold一致（官方条目ACTIVE；accepted name为toluene methyl-monooxygenase，答案名xylene monooxygenase属家族级别名，名称token未见于记录→UNRESOLVED待核，不判错）；S3 EC 1.2.1.28与gold酶表一致；S2 EC 1.1.1.90在E0无记录（GAP-038-002）→UNRESOLVED；S4/S5按题面要求诚实填null EC并自标low、pnbA/pnbB未核；S6 EC 1.13.11.3无E0记录但为公认标准酶。主要步骤酶-反应对应有合理支持，少量条目待确认→7分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_038：本题必答S01/S02/S03的gold accepted酶/EC行，用于核对答案EC与accepted集合；不证明答案具体蛋白底物谱或实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：本题S02-&gt;S03-&gt;S01的主反应物/产物与方向；仅支持反应映射，不证明答案酶名或EC配对
- E0_EVIDENCE / f3e0:ec:1.14.15.26：EC 1.14.15.26官方条目的accepted name、reaction与ACTIVE状态；支持EC身份核对，不自动支持答案所称xylene monooxygenase名称或4-nitrotoluene特异活性

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 物种层面Pseudomonas putida与TaxID 303的对应有官方分类记录支持；gold步骤微生物也是P. putida/TaxID 303。答案进一步写成P. putida TW3，E0只有BacDive 12880（mt-2 PaW1/pWWO）等别株记录，不能核实TW3；这属于物种级记录支持菌株级声称的粒度不足，按P107通常7档附近档内扣，不cap。答案还把complete_pathway_organism_profile_id指向ORG_001，声称TW3完成全路径；该菌株级全路径能力无冻结证据，保持待核。ORG_002 YH101位于gold终点下游，非本题必答主链，但其菌株身份/能力同样无E0记录，作为额外待核登记。

<details><summary>V0.4理由与本行变化背景</summary>

物种Pseudomonas putida与TaxID 303由官方分类记录精确支持，且与gold步级菌一致；但菌株TW3不在303种级记录名称中（粒度不足，按D3b身份阶梯①档内扣、默认不cap）；YH101无TaxID、无任何冻结记录，其步级归属UNRESOLVED；complete_pathway_organism_profile_id指向ORG_001(TW3)，而S4–S6步级菌却写YH101，完整路径能力归属与步级归属内部不一致。未发现经核实的跨属/无关类群错配，不触发cap；按&#x27;有合理候选和部分支持，但若干关键身份或作用范围仍未充分核验&#x27;取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：官方分类记录支持Pseudomonas putida与TaxID 303的物种级名称对应；不核实TW3菌株或YH101菌株。
- E0_EVIDENCE / f3e0:bacdive:12880：BacDive 12880为P. putida mt-2 PaW1/pWWO菌株记录；不是TW3，不能用于核实答案的TW3身份或能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_038：gold步骤微生物为Pseudomonas putida/TaxID 303物种级；不提供TW3或YH101菌株级证据。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案按任务给出两个profile各15项性状，且对未知项多填null/unknown，诚实性较好。P. putida属级的运动性、杆状、革兰氏阴性、不产芽孢等基础性状与trait_gold观测一致；但关键降解/底物性状存在明显外推：ORG_001声称TW3以4-nitrotoluene为唯一碳源、氮源和能源并完全降解，ORG_002声称YH101以4-nitrobenzoate为碳源并完全矿化，均无冻结菌株级证据；F9把侧链氧化/脱氢酶活性写成TW3已具活性，也超出gold可核粒度。温度、pH、盐度、保藏、基因组等多项为null，属完成度/证据不足，不在D4重复当错误重扣。5–6档：部分性状准确且适用，但关键项证据不足、条件与菌株适用性需实质修订；因基础性状明确正确，取6而非5。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状均为物种/属级定性特征（好氧呼吸+O2、运动性、杆状、革兰氏阴性、不产芽孢、碳源与降解能力描述），与trait_gold taxid 303的OBSERVED记录方向一致；但来源统一为EVID_004（属级内部知识）、raw_text全为null，并被外推到TW3/YH101菌株（物种数据不自动等于菌株级观测）；F1&#x27;专性好氧&#x27;与冻结F1记录(aerotolerant=true、兼性厌氧预测无稳健多数)存在表述张力未核；F15&#x27;分离自土壤&#x27;（TW3）为无来源具体声称；YH101的F15明示为推断。关键定量性状（温度/pH/盐度/保藏号/基因组）全部诚实null，其完成度扣分归D1、不在D4重复重扣。按&#x27;部分性状准确且适用，但关键项证据不足或条件解释需修订&#x27;取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_038：TaxID 303的观测性状支持P. putida运动性、杆状、革兰氏阴性、不产芽孢等属级特征；不提供TW3/YH101菌株级4-nitrotoluene/4-nitrobenzoate碳源或全降解能力。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_038：显示部分性状子字段可评分性与待裁决边界；用于避免把null完成度缺口重复当作已核错误。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 答案虽建立本地evidence_id与claim_scope映射，但EVID_001–EVID_004全部为INTERNAL_KNOWLEDGE_ONLY，EVID_005虽标DATABASE_DIRECT但record_id为null、locator仅为pathway名称，属于无法定位到具体条目的generic来源。关键酶/EC、菌株能力、性状与全路径声称均不能从原交付追到可核对的文献/数据库条目；只有少数属级性状可由冻结trait_gold事后核验，但不能回填为答案原来源。D5 1–2档：重要结论依据几乎不可定位；未发现经统一冻结证据核实的错引，故为MISSING/GENERIC来源低分，不触发CRITICAL/SYSTEMIC cap。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）全部只有INTERNAL_KNOWLEDGE_ONLY自我声明（EVID_001–004）或&#x27;MetaCyc/UniPathway+路线名&#x27;的笼统库名（EVID_005，record_id=null）；无任一条目级可定位可核对记录。按四.3/P41：全部缺失→低分档、默认不cap；全部笼统→3–4档。E0未发现可核实的错引（EC 1.14.15.26条目ACTIVE且名称差异不构成错引；taxid 303学名精确匹配），故无VERIFIED_MIS_CITATION、无cap；未在E0的EC（1.1.1.90/1.13.11.3/1.2.1.28）与YH101/pnbA-pnbB保持UNRESOLVED待核。取3分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：定位答案实际交付的来源类型与locator：EVID_001–004为INTERNAL_KNOWLEDGE_ONLY，EVID_005为无record_id的DATABASE_DIRECT；用于D5来源状态判定。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案较清楚地区分观测、内部记忆、预测与未知：对TW3温度/pH/盐度/保藏/基因组填null，对S4/S5的pnbA/pnbB与YH101身份明确标注内部文献记忆、低置信，对EC归类差异、SMILES立体化学未编码、TW3菌株特异基因未核实均有uncertainties说明；EVID_001–004也标为INTERNAL_KNOWLEDGE_ONLY。仍有个别偏强表述：F7/F8对TW3的“唯一碳源/氮源/能源”“完全降解”给medium且未在uncertainties中同等强调，属单点/局部过度确信，不是系统性把预测写成实证。7–8档：大部分证据性质与主要限制已说明，仅少量强度匹配问题；取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且分层：每步uncertainty说明EC按同类酶归类、菌株特异归类未核；全局uncertainties逐条列出内部记忆依赖、EC缺失、SMILES立体化学未编码；confidence分级（high/medium/low/unknown）大体与证据相称；F15对YH101明示&#x27;推断&#x27;；未知项诚实null而非编造。扣分点：complete_pathway归属TW3与步级YH101的内部矛盾未披露；EVID_005以DATABASE_DIRECT+medium包装无record_id的通用库名（单点过度包装）；F8把含硝基还原段的整条路径能力写给TW3未标为推断。属&#x27;大部分证据性质与边界标注正确、少量单点过度确信&#x27;，7分。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：定位答案对null、内部记忆、低置信、EC归类与立体化学限制的披露；用于评价不确定性表达，不证明其科学内容正确。

</details>

## DeepSeek

答案SHA256：`26c6cc03a7115beb7c211fcd8bf8278634a65581ca1e900b7482b00e4f4fa933`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 题面指定路线名称原样填写；steps S1–S3 覆盖4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate并到达gold终点；每步有酶/菌字段，15项性状结构完整。但必答步S2/S3等EC为null，organism_profiles&#91;0&#93;的15项性状全为null，按P45 D1仍反映完成度不足；下游额外步骤不加分。按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

路径(9步含名称)、每步酶名与微生物均有交付，任务路线名原样回填、氧条件null如实保留；但15项性状全部null、evidence_registry为空、S2–S6缺EC、S7/S8缺主产物SMILES。主要模块有涉及但存在多类必要内容遗漏，属5–6档，因性状与来源两大板块整块落空取低分5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：要求指定路线、每步主底物/产物SMILES、首选酶+EC、对应微生物、15项性状及未知填null
- ANSWER_TEXT / ANSWER_BEGIN：答案S1–S3覆盖必答主链至4-nitrobenzoate；S2/S3 EC为null；15项性状全null
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_038：gold路线终点为4-Nitrobenzoate，用于核对交付终点/范围

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案前三个主链步骤4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate与gold反应方向、主底物/主产物及连接一致，终点合规；后续4-nitrobenzoate下游延伸虽非本题必答，未见明显方向/结构断裂，不改变必答主链结论。主要缺陷是O2、NAD(P)+、铁氧还蛋白等辅因子普遍未列，属P103局部计量缺陷，不cap；按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3与gold三步化学一致（4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate），方向与结构正确、无方向反转或原子不守恒；S4–S9延伸至gentisate/中心代谢为已知路线、原子可守恒。缺陷为各步辅因子(O2/ferredoxin/NAD(P)H)全缺、氧条件一致性未说明，属局部计量/条件缺陷(7–8档)，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：前三个步骤的底物/产物、方向与连接；辅因子未列
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：gold三条必答反应的底物/产物与方向（S02→S03→S01）
- RUBRIC_CLAUSE / P103：辅因子遗漏通常为局部计量缺陷，D2在7–8档内处理，不自动cap

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 逐必答目标：S02（题答S1）给4-nitrotoluene monooxygenase但EC 1.14.13.196不在accepted集且无冻结记录；S03（题答S2）给4-nitrobenzyl alcohol dehydrogenase、无EC，accepted为4-nitrobenzyl alcohol oxidase(1.1.3)；S01（题答S3）给4-nitrobenzaldehyde dehydrogenase、无EC，accepted为benzaldehyde dehydrogenase&#91;multifunctional&#93;(1.2.1.28/1.2.1.29)。三者仅名称层面部分对应，无已核S、无已核实F；按C03/C04全U由裁判依据现有材料定档，取较弱档3，不把未核当已证错。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名与gold 4-nitrotoluene单加氧酶一致、S3与benzaldehyde dehydrogenase(EC1.2.1.28/1.2.1.29)对应；但S2–S6无EC，S1 EC 1.14.13.196、S7 1.13.11.4、S8 5.2.1.4、S9 3.7.1.20均无冻结记录(EVIDENCE_GAP)→UNRESOLVED，不判错也不放行；S2用dehydrogenase而gold为oxidase(EC1.1.3)属档内疑点。合理候选+部分支持而关键步骤缺具体核验，属5–6档，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：三个必答步的enzyme.name/ec_number：S1 EC 1.14.13.196；S2/S3 EC为null
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_038：accepted酶名/EC：S01 1.2.1.28/1.2.1.29；S02 1.14.15/1.14.15.26；S03 1.1.3
- E0_EVIDENCE / f3e0:ec:1.14.15.26：官方EC条目覆盖1.14.15.26，不覆盖答案1.14.13.196；答案EC仍UNRESOLVED

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案所有步骤使用Pseudomonas sp. TW3，无TaxID、保藏号或证据；gold步级微生物为Pseudomonas putida TaxID 303，另有PATHWAY_COMPLETE记录。仅属级Pseudomonas为合理候选，但种/菌株身份与整条路径能力均未核，且complete_pathway_organism_profile_id=ORG_001把同一未核菌写成整路菌，属5–6档低端。

<details><summary>V0.4理由与本行变化背景</summary>

全程单一菌Pseudomonas sp. TW3；属名Pseudomonas与gold P. putida(TaxID 303)相容，但菌株TW3无冻结记录、ncbi_taxid=null，步级与整链能力无任何来源。属粒度不足+能力未核，未构成经核实的菌株错配或跨类群错配，故不cap；合理候选+部分支持而关键身份/作用范围未核，属5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持P. putida物种身份；不支持Pseudomonas sp. TW3的菌株身份或全路径能力。
- E0_EVIDENCE / f3e0:bacdive:12880：支持该P. putida菌株记录；不能回填为TW3身份或能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_038：gold提供P. putida身份与一条PATHWAY_COMPLETE记录；不支持答案TW3。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 答案的organism_profiles&#91;0&#93;.traits中F1-F15全部以value=null、confidence=unknown交付；没有可评价的具体性状值。按P44/四.4，全部必需性状均为null时D4按MISSING=1，不宣称检测到科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状(F1–F15)全部value=null、confidence=unknown，未交付任何可评价性状内容；按四.4/P44“全部必需性状均为null”处理，D4记MISSING=1，不宣称检测到科学错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：支持答案未交付任何可评价性状值；不证明性状错误。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_038：展示gold存在可评分性状参照；不能把答案null回填为已交付。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 答案evidence_registry为空数组，所有step/enzyme/microorganism/trait的evidence_id均为null；没有可定位的文献、数据库条目、计算记录或方法说明。决策相关核心组均只有MISSING_SOURCE，属无来源低档；无已核实错引，不触发CRITICAL/SYSTEMIC cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry为空，全部claim组均为MISSING_SOURCE，无任何可定位文献/条目或计算生成记录→D5落低分档(1–2)，取2；MISSING_SOURCE默认不cap。EC与菌株编号虽交付但均无来源，保持UNRESOLVED待核，不判虚构。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：支持答案未交付任何来源记录；不能据此判引用虚构。

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案对多个未核酶/菌仍给medium confidence：S1 4-nitrotoluene monooxygenase（EC未核）medium；S4-S9多种无EC酶medium；microorganism全步medium。uncertainties为空数组，未说明主要限制或证据性质。虽未把预测直接写成实验观测，且性状诚实null，但多处过度确信、主要限制缺失，落3–4档，不构成系统性D6 cap。

<details><summary>V0.4理由与本行变化背景</summary>

对未知（15性状、S2–S6的EC、菌株TaxID）诚实填null是正面；但route_summary与complete_pathway声称以确定语气陈述未核路线，uncertainties为空、未说明无来源/氧条件一致性等主要限制，多处过度确信→3–4档，取4；属披露不足而非系统性把预测写成实证，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.confidence：展示答案的置信标签与缺失的限制说明；不证明这些标签与证据相称。

</details>

## Kimi

答案SHA256：`729f01babc87afba9aec2b278b85085371d5e667f0b3e8e3d9ce6d22d33e67e7`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 主链S1–S3覆盖gold三步结构，S4为额外下游；步骤、菌与15项性状键均出现，但2/4步缺EC、7/15性状为明确未知，属若干必要内容未实质填写，落5–6档，取6（结构关联清楚且无遗漏键）。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块基本齐备：route_scope.chosen_route_name原样回填题面指定路线，4个step均给出主底物/主产物（含name与SMILES）、首选酶与对应菌，15项性状字段全部出现（8项填写、7项明确null、0遗漏），evidence_registry与uncertainties均已交付。缺陷为S1/S4的EC为null、7项性状未知、S4为gold终点之外的延伸且未显式声明不属于评分主链，属少量遗漏与工程性缺陷，处于7–8档并取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：显示答案交付了4步路径、每步酶名/菌与15项性状字段；显示S1/S4缺EC且多数性状为null。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_038：gold n_required=3、ordered_step_count=3、LINEAR_UNIQUE；不要求全部旁支。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：gold主链为4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate，终点4-Nitrobenzoate。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> S1–S3的底物/产物与gold主链结构、方向一致；S1/S2/S3辅因子未列，S2用脱氢酶而非gold氧化酶但净转化仍为醇到醛；按P103局部计量缺陷不cap，落7–8档取8。S4超出gold终点，按P29不据此加减D2。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3的底物/产物、SMILES、方向与顺序与gold BSY-r02675、BSY-r03240、BSY-r02418逐步一致，主链化学成立、结构书写正确、无方向反转或跳步。S4（4-nitrobenzoate→protocatechuate+nitrite）位于gold终点之外，按P29属额外下游延续，不加分亦不据此扣覆盖率。全部步骤漏写O2/还原型铁氧还蛋白/NAD(P)H等辅因子，属局部计量缺陷（P103），在7–8档内处理，不触发cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：显示各步底物/产物SMILES、方向与连续性；显示辅因子基本未列。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：支持前三步主转化与方向；S01为terminal 4-Nitrobenzoate，S4不在gold终点内。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_038：root=4-Nitrotoluene，terminal=4-Nitrobenzoate；用于界定题面终点，不证明S4化学错误。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 题面锁定3个必答目标步（N=3），答案S1-S3分别对应gold S02/S03/S01，并额外给出S4下游（不计入D3a目标N）。S3酶EC 1.2.1.28落在S01 accepted EC集，但名称—EC配对仍U；S1酶名接近S02 accepted name但无EC，U；S2用4-nitrobenzyl alcohol dehydrogenase EC 1.1.1.90，而accepted为4-nitrobenzyl alcohol oxidase EC 1.1.3，现有材料不能证明其功能不相容，仍记U而非F。三步主底物/主产物方向均对，酶对应有部分适用支持但无确认S，且一处酶类不匹配待核；按C04不因U自动NE或低分，按C05在&#91;5,6&#93;下沿取5。无已确认KEY失败，不触发D-KEY4。

<details><summary>V0.4理由与本行变化背景</summary>

S3 EC 1.2.1.28与gold benzaldehyde dehydrogenase条目一致；S1酶名（4-nitrotoluene monooxygenase）与gold酶名方向一致但EC留null，而E0显示EC 1.14.15.26为active的甲基单加氧酶且gold将其配给该步，属可补而未补；S2以通用芳基醇脱氢酶EC 1.1.1.90替代gold的4-nitrobenzyl alcohol oxidase EC 1.1.3，反应类型上化学可行，但冻结证据无该EC条目；S4 EC为null。未见EC大类别与反应类型冲突、酶名与编号互相矛盾或以家族相关性冒充具体催化证据，故不判关键错误，7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：给出三个必答步的accepted酶/EC：S01为benzaldehyde dehydrogenase EC 1.2.1.28/1.2.1.29；S02为4-nitrotoluene monooxygenase hydroxylase component EC 1.14.15/1.14.15.26；S03为4-nitrobenzyl alcohol oxidase EC 1.1.3。
- GOLD_SLICE / reaction_gold.tsv：给出三个必答步的主底物、主产物、方向及终点为4-Nitrobenzoate；答案S4生成protocatechuate属于超出必答主链的下游延伸，不作为D3a目标反应计入。
- ANSWER_TEXT / steps.S1-S4.enzyme：答案酶声称：S1为4-nitrotoluene monooxygenase（EC null）；S2为4-nitrobenzyl alcohol dehydrogenase（EC 1.1.1.90）；S3为4-nitrobenzaldehyde dehydrogenase（EC 1.2.1.28）；S4为下游额外步。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案给出单一Pseudomonas sp. strain 4NT，并称其为全路径菌；gold步级为Pseudomonas putida TaxID303，pathway_complete另列Pseudomonas sp. NT4(No TaxID)。4NT身份、TaxID及全路径能力在E0无记录，Haigler &amp; Spain 1991为自由文本待核；有合理候选和部分文献线索但关键身份/作用范围未充分核验，落5–6档取6。未发现已核虚构或跨类群错配，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案以单菌株Pseudomonas sp. strain 4NT覆盖四步，与gold路径级菌Pseudomonas sp. NT4（No TaxID）在名称与粒度层面相容，未见与gold步级P. putida（TaxID 303）构成已核实的身份错配（gold步级菌为酶来源菌，路径级菌另列）。但菌株身份无TaxID/保藏号/基因组号，唯一支撑为未解析的自由文本引文（GAP-038-019），属粒度不足与身份、反应级、全路径能力未核实（UNRESOLVED），在7档内扣分，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：显示答案使用Pseudomonas sp. strain 4NT，无TaxID，并声明complete_pathway_organism_profile_id=ORG_001。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_038：步级gold organism为Pseudomonas putida TaxID303/GCA_024508115.1；pathway_complete另有Pseudomonas sp. NT4(No TaxID)；不能直接证明答案的4NT身份或能力。
- E0_EVIDENCE / f3e0:taxid:303：仅证明TaxID303为Pseudomonas putida官方分类记录；不证明Pseudomonas sp. 4NT的身份、菌株能力或全路径能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项键齐全，8项有值、7项明确null；有值项多为属级/internal knowledge（F1/F6/F11/F12/F13）或待核文献（F7/F8/F9），温度/pH/盐度/基因组等关键定量项未给。已给内容未发现明显数值错误，但关键项证据不足且作用对象为未核菌株，落5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状中F1（aerobic）、F6（aerobic respiration/oxygen）、F11（rod-shaped）、F12（Gram-negative）、F13（non-spore-forming）为属级常识，来源为INTERNAL_KNOWLEDGE_ONLY且confidence=low，与gold P. putida种级观测方向相容，但不构成该菌株记录；F7/F8/F9为文献性能力声称，引文未解析。F2/F3/F4/F5/F10/F14/F15共7项为null（诚实未知，完成度扣分归D1，不在此重复重扣）。定量关键性状全缺、可核实项仅属级定性，属&#x27;部分性状准确且适用、关键项证据不足&#x27;的5–6档，取6；未见数值离谱到误导筛选、未见把预测写成观测，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：显示15项性状中8项有值、7项null；有值项confidence多为low/medium，EVID_003为INTERNAL_KNOWLEDGE_ONLY。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_038：gold性状参照主要对应Pseudomonas putida TaxID303；Pseudomonas sp. NT4多为UNKNOWN；不能证明答案4NT的菌株级性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_038：mask显示多个性状子字段为completeness_only或pending adjudication；缺失项不能作数值准确性分母。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出MetaCyc路线名和Haigler &amp; Spain 1991文献引用，核心路线/菌/部分性状可定位；但EVID_001无record_id且claim_scope过宽，EVID_002在E0为自由文本待核，EVID_003为INTERNAL_KNOWLEDGE_ONLY，多个关键组只有笼统/待核来源。无已核实错引，落5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CORE：CG01/CG02/CG03/CG05/CG07/CG09；APPLICATION_CRITICAL：CG08/CG17）中无任何经核实错引，故不触发cap：路线序列可由EVID_001命名的MetaCyc路线定位且与gold前3步吻合（部分条目级可核对），S3 EC 1.2.1.28与gold一致；但菌株身份、全路径能力、EC 1.1.1.90与自由文本引文均为UNRESOLVED待核，性状组多依赖INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）。按P41构成落在5–6档，因最关键的菌株身份与能力证据未核而下取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示EVID_001为MetaCyc路线名无record_id，EVID_002为Haigler &amp; Spain 1991自由文本，EVID_003为INTERNAL_KNOWLEDGE_ONLY。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案用confidence high/medium/low/unknown区分证据，明确列出未确认TaxID/保藏/基因组/温度-pH-盐度，EVID_003标INTERNAL_KNOWLEDGE_ONLY，null纪律较好。仍把4NT全路径能力和部分文献结论以medium呈现，未逐项说明文献未在E0核验，故落7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体较好：未知字段一律null，confidence按medium/low/unknown降级，uncertainties明确列出未确认的TaxID/保藏号/基因组登录号与温度/pH/盐度，EVID_003自述为属级推断只在缺菌株数据处使用，未把预测写成实验观测。缺陷：EVID_001以DATABASE_DIRECT标签包装无record_id的命名路线；&#x27;该甲基羟化酶未见可确认的专属EC&#x27;的否定表述偏强（存在可用的通用EC 1.14.15.26）；complete_pathway能力未附不确定性说明。属少量过度确信而非系统性误导，档内扣至7，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案明确披露氧条件null、TaxID/保藏/基因组/温度-pH-盐度未确认、部分EC未确认。

</details>

## Qwen

答案SHA256：`63146dcd72a68eb0e1fbb049e3ee57b6bb05ba66b7cfc1397160386f33d523d1`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 主要模块均有涉及（路径、步骤、一个微生物、15项性状键、证据登记），但EC全为null、15项性状值全为null/占位、来源仅INTERNAL_KNOWLEDGE_ONLY，属于若干必要内容遗漏/仅占位；按D1 5–6档取6。额外下游S4–S6超出gold终点，不作为加分。

<details><summary>V0.4理由与本行变化背景</summary>

路线名按题面原样回显、6步各含主底物/主产物英文名+SMILES+酶名+菌名，主要模块均有涉及；但每步EC编号全部为null（题面明确要求“一个首选酶及EC”）、15项性状全部null（仅占位）、来源仅一条INTERNAL_KNOWLEDGE_ONLY自述，多处必要内容遗漏或占位，落5–6档取低分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_038：定义3个必答步骤及gold主链；不证明答案额外下游步骤或缺失的EC/性状内容。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 前3步至gold终点4-nitrobenzoate的底物/产物方向与SMILES正确：4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate。辅因子（O2、ferredoxin、NAD+等）遗漏属局部计量缺陷（P103），阻止9–10但不cap；S01仅为电荷表示差异。额外下游S4–S6超出题面终点，不用于加分。按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3与gold主链逐步一致：4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate，方向、结构、SMILES与gold相同；全部步骤未列O2、还原型铁氧还蛋白、NAD+/NADH、H2O2、H+等辅因子，属局部计量缺陷，按八.辅因子条款在7–8档处理；S4–S6位于gold终点(4-Nitrobenzoate)下游，E0无核验记录，登记待核、不进入gold范围外覆盖率扣分。取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：定义S02→S03→S01的有向转化及辅因子；不证明答案额外下游步骤或酶名/EC。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_038：指定终点为4-Nitrobenzoate；不证明额外下游延续。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按三个必答目标逐项核对：答案step S1（对应gold S02）给4-nitrotoluene monooxygenase但EC为null，accepted集要求4-nitrotoluene monooxygenase hydroxylase component/EC 1.14.15.26或1.14.15，支持仍为UNRESOLVED；答案step S2（对应gold S03）给4-nitrobenzyl alcohol dehydrogenase，而accepted为4-nitrobenzyl alcohol oxidase EC 1.1.3，名称/酶类差异尚无催化不相容证明，仍为UNRESOLVED；答案step S3（对应gold S01）给4-nitrobenzaldehyde dehydrogenase但EC为null，accepted为benzaldehyde dehydrogenase EC 1.2.1.28/1.2.1.29，且gold S01存在表示边界HOLD，亦为UNRESOLVED。三步均有可辨认酶名且反应方向与gold主链对应，但无确认S，也无确认F/M；无已核实关键错误。依C04全U由现有材料判断、不自动NE或低分；现有可判信息仅为少数目标名称接近可用、关键EC/配对及S03酶类边界不清，落D3a 3-4档低端，取3。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名“4-nitrotoluene monooxygenase”与gold的4-nitrotoluene monooxygenase hydroxylase component（EC 1.14.15.26）同源；S3“4-nitrobenzaldehyde dehydrogenase”与gold benzaldehyde dehydrogenase（EC 1.2.1.28/1.2.1.29）一致；S2写作脱氢酶而gold为4-nitrobenzyl alcohol oxidase（EC 1.1.3），酶类不一致；全步EC与基因/蛋白均为null，无法按四.6做EC级核验；S4–S6酶名无依据且S6双加氧酶类与所称脱氨反应不匹配。属“合理候选+部分支持、关键步骤缺具体核验”，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.enzyme：答案S1给出4-nitrotoluene monooxygenase，EC为null；对应gold S02反应但无显式EC配对
- ANSWER_TEXT / ANSWER.steps&#91;1&#93;.enzyme：答案S2给出4-nitrobenzyl alcohol dehydrogenase，EC为null；与accepted 4-nitrobenzyl alcohol oxidase EC 1.1.3名称/酶类不一致
- ANSWER_TEXT / ANSWER.steps&#91;2&#93;.enzyme：答案S3给出4-nitrobenzaldehyde dehydrogenase，EC为null；对应gold S01反应但无显式EC配对
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_038：列出本题gold酶名与EC：S02为4-nitrotoluene monooxygenase hydroxylase component EC 1.14.15.26/1.14.15；S03为4-nitrobenzyl alcohol oxidase EC 1.1.3；S01为benzaldehyde dehydrogenase EC 1.2.1.28/1.2.1.29
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：确认三步主反应方向与底物/主产物：S02 4-nitrotoluene→4-nitrobenzyl alcohol；S03 4-nitrobenzyl alcohol→4-nitrobenzaldehyde；S01 4-nitrobenzaldehyde→4-nitrobenzoate
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_038：本题路线终点为4-Nitrobenzoate；用于核对主链终点而非直接证明答案酶对应
- E0_EVIDENCE / f3e0:ec:1.14.15.26：EC 1.14.15.26条目的accepted name为toluene methyl-monooxygenase，reaction为toluene→benzyl alcohol等；不能自动证明答案的具体4-nitrotoluene monooxygenase名称或无EC声称
- RUBRIC_CLAUSE / C04：全U交由裁判依现有材料判断，不自动NE或低分；缺EC不等于没有酶功能，未命中accepted不等于已证伪
- RUBRIC_CLAUSE / C05：D3a 3-4档用于少数目标可用、需实质修订；4档要求已核可用部分与关键边界清楚，本例EC/配对未确认，取低端

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案所有步骤均写Pseudomonas sp. PNT（无TaxID、无独立证据，EVID_001仅INTERNAL_KNOWLEDGE_ONLY）；gold为Pseudomonas putida/TaxID 303。属合理属级候选但菌株身份与逐步能力未核验，且同一菌贯穿全部步骤未给全路径能力证据；按D3b 5–6档取5，不cap（无已核跨类群/异菌株推翻微生物推荐）。

<details><summary>V0.4理由与本行变化背景</summary>

属级Pseudomonas用于硝基芳烃降解合理，与gold的Pseudomonas putida(303)/Pseudomonas sp. NT4同属；但答案为“Pseudomonas sp. PNT”，E0无该菌株记录、未填TaxID、无保藏号，证据仅INTERNAL_KNOWLEDGE_ONLY；同一未核菌株承担全部6步（隐含全路径能力）。属“合理候选+部分支持、关键身份与作用范围未充分核验”，5–6档取6；未核实身份不判错（UNRESOLVED待核）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_038：gold列出步骤与PATHWAY_COMPLETE的Pseudomonas putida/TaxID 303；不支持答案的Pseudomonas sp. PNT或其全路径能力。
- E0_EVIDENCE / f3e0:taxid:303：TaxID 303为Pseudomonas putida物种记录；不核实菌株PNT身份，也不自动支持其反应能力。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 15项性状键均存在，但每一项value均为null、confidence为unknown；按P44，全部必需性状均为null/空值→D4按MISSING记1分，不宣称检测到科学错误。完成度不足已在D1反映。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状（F1–F15）全部为value=null、confidence=unknown，未交付任何可评价的性状取值；按量表P44（v0.3）&#x27;全部必需性状均为null/空值时D4按MISSING记1分&#x27;登记，不宣称检测到科学错误；明确未知的披露质量计入D6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 唯一证据EVID_001为INTERNAL_KNOWLEDGE_ONLY，database/record_id均null，locator仅为路线名；路线、酶、微生物、性状均无可定位的文献/数据库/计算记录。D5 1–2档；因关键结论几乎无法追溯取1。MISSING_SOURCE默认不cap，且无已核实错引。

<details><summary>V0.4理由与本行变化背景</summary>

全案唯一证据条目EVID_001为INTERNAL_KNOWLEDGE_ONLY，database/record_id均为null、locator仅为路线名，无法定位到任何文献/数据库/计算记录；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09/CG17）全部为MISSING_SOURCE，且无任何条目级可核对结论；按四.3，MISSING_SOURCE属缺失而非误导，取低分档且默认不cap；答案未引用E0任一记录，故不存在已核实错引。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案对酶EC/基因、菌株性状、氧条件及替代分支均明确写null/unknown，confidence普遍low/unknown，uncertainties列出主要缺口；诚实未知与证据边界总体清楚。轻微不足：将S4–S6下游仍写入steps而未明确标为超出4-nitrobenzoate终点的continuation；菌株PNT身份未单独声明待核。故7–8档取8，不给9。

<details><summary>V0.4理由与本行变化背景</summary>

答案在route_summary、每步uncertainty与uncertainties列表中明确说明氧条件未指定、EC/基因缺失、全部性状缺来源、下游可能存在替代分支，并把证据标为INTERNAL_KNOWLEDGE_ONLY、置信low/unknown，未把内部知识包装成数据库直查或实验观测；唯S4–S6越出gold终点却仍置于主链且未显式标注为下游推测，属局部披露不足。7–8档取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`cfcd0bfd4dff4749cba1f262fc2c3d44f23f5b9b8d02800bedf0cf72da418e0e`。

### D1 完整性与任务符合度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1–S3覆盖了gold主链的3个必答转化，均给出底物/产物名称与SMILES、酶名和对应微生物；15项性状字段齐备，来源与不确定性有登记。扣分点在于全部EC为null、额外把S4–S5写入主链而超出gold终点、TW3无TaxID；整体属大部分完整但有少量实质缺口。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：答案已交付的步骤、性状、来源与不确定性字段；不证明其科学正确性
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_038：ordered_step_count=3；本题必答主链长度以gold主链为参照，不把全部下游延伸当作必答

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 前3步的有机转化与gold主链一致：4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate，方向、结构与连接清楚。局部问题是S1用NADH而非gold的还原型铁氧还蛋白，S2用脱氢酶而非accepted oxidase；这些属局部酶/辅因子表达问题，不推翻主链。S4–S5位于gold终点之后，作为额外下游不纳入D2主链缺步扣分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：前3步的底物/产物、方向与连接；不证明S2替换酶与accepted oxidase完全等同
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：gold主链三步的底物→产物方向及终点4-Nitrobenzoate

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三个必答目标(S02-&gt;S03-&gt;S01)均以S1-S3交付，主底物/主产物和顺序与gold一致。S1用4-nitrotoluene monooxygenase，可与accepted的4-nitrotoluene monooxygenase hydroxylase component在功能层面对应；S3用4-nitrobenzaldehyde dehydrogenase，可与accepted的benzaldehyde dehydrogenase多功能酶在功能层对应；二者未给EC，不构成显式EC冲突。S2使用4-nitrobenzyl alcohol dehydrogenase/NAD+，而gold目标为4-nitrobenzyl alcohol oxidase EC 1.1.3且使用O2-&gt;H2O2，缺少accepted支持，保留为KEY U。S4-S5位于gold终点4-nitrobenzoate之后，非本题必答目标，不进入D3a目标信用。约2/3目标可支持、1个KEY U，C≈0.67，落&#91;5,6&#93;；支持部分清楚、剩余缺口明确，且无已确认KEY F/M，取6，不进入7-8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_038：列出S01/S02/S03的gold酶名与EC集合：S02为4-nitrotoluene monooxygenase hydroxylase component EC 1.14.15.26/1.14.15；S03为4-nitrobenzyl alcohol oxidase EC 1.1.3；S01为benzaldehyde dehydrogenase EC 1.2.1.28/1.2.1.29。支持目标酶身份，但不支持答案S2的dehydrogenase作为accepted匹配。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：给出S02/S03/S01的有向底物-产物与辅因子行：S03使用O2并生成H2O2，S01使用NAD+并生成NADH；支持目标反应身份及S2与gold在电子受体/酶类型上的差异。不外推到S4-S5。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_038：本题gold终点为4-Nitrobenzoate；据此S4-S5为终点后延伸，不是D3a必答目标。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_038：本题gold为LINEAR_UNIQUE、ordered_step_count=3；支持必答目标数为3，不把额外下游分支并入D3a分母。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：官方EC条目为ACTIVE，accepted names包括toluene methyl-monooxygenase等，反应涉及toluene/xylenes；该条目不自动确认4-nitrotoluene特异活性，也不自动确认答案未给EC的声称。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出Pseudomonas sp. TW3作为逐步对应菌，并把它作为完整路径菌；这是合理的候选，但无TaxID、保藏号或菌株级反应/全路径能力证据。gold步级菌为Pseudomonas putida，PATHWAY_COMPLETE行为Pseudomonas sp. NT4，未直接支持TW3；属有合理候选和部分支持但关键身份/能力未充分核验。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：答案声称的TW3身份与逐步归属；不证明TW3的TaxID或全路径能力
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_038：gold步级菌为Pseudomonas putida；PATHWAY_COMPLETE行含Pseudomonas sp. NT4；不证明TW3完成本题路径
- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida物种身份记录；不把TW3自动归入或确认其菌株身份

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> F11–F13（杆状、革兰氏阴性、不产芽孢）与Pseudomonas属/putida物种的gold记录方向一致；F1/F6及F7/F8/F9等则把TW3的氧需求、碳源利用、降解能力和酶活写成medium，但无TW3菌株级证据。F2/F3/F4/F5/F10/F14/F15多数为null，属于诚实未知而非编造。部分性状可用，但关键性状证据不足，落5档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：答案实际填写的15项性状及null；不证明TW3菌株级准确性
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_038：Pseudomonas putida物种级代表记录支持部分通用性状方向；物种级记录不自动适用于未确认的TW3菌株
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_038：标示若干性状/子字段的可评分性及待裁决字段；不把null自动判错

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 两条evidence_registry均为INTERNAL_KNOWLEDGE_ONLY；EVID_001虽列出作者/年份/期刊题名，但没有DOI、数据库条目或可定位记录，EVID_002为属级常识且明说不是TW3实测。决策相关路线、酶、菌、性状组均缺可定位外部来源，但未见已核实错引，故不触发D5 cap，给低档3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：答案实际交付的来源类型、locator与置信度；不把内部知识升级为外部可定位来源

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确标注证据为INTERNAL_KNOWLEDGE_ONLY，主动披露路线命名不确定、EC未核定、辅酶专一性不确定、TW3缺TaxID与多项性状、文献对TW3种名存在差异，并把alternative branch标为不属于主链；总体证据性质与未知边界披露较好。局部仍把部分TW3/属级性状标为medium，属单点过度确信而非系统性误导，给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：答案对证据类型、未知、冲突和排除分支的披露；不证明其未核内容正确

</details>

## GPT5.6

答案SHA256：`39d86b6dda23b480d6cf6021bc3ac2565cacf5eeb62161ca39ee3ad9abe520b1`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案格式完整，但交付的是另一条两步路线（4-nitrotoluene→4-methylcatechol→2-methylmuconate），不是题面指定路线的主链；缺少终步4-nitrobenzaldehyde→4-nitrobenzoate；15项性状均null。D1适用&#91;1,4&#93;，有结构化两步骤和完整字段，但路线偏离与终步缺失使只能取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：显示题面指定主链应为4-nitrotoluene→4-nitrobenzyl alcohol→4-nitrobenzaldehyde→4-nitrobenzoate；不证明具体酶活。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_038：显示路线名与题面指定终点4-Nitrobenzoate；不扩展支持其他替代路线。
- ANSWER_TEXT / steps：显示答案只给出4-nitrotoluene→4-methylcatechol与4-methylcatechol→2-methylmuconate两步，且无终步。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的两步替代路线在简化层面连续：4-nitrotoluene→4-methylcatechol，再由catechol 1,2-dioxygenase开环到2-methyl-cis,cis-muconate；但未列O2/还原当量，产物SMILES缺失，且止于muconate而非指定终点。作为可成立替代路线最高限&#91;1,6&#93;，取5：主干化学可辨认，但计量和结构细节不足。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：显示指定主链反应，不证明答案替代路线已获实验确认。
- ANSWER_TEXT / steps：显示替代路线的两步底物/产物和内部连续性，也显示产物SMILES缺失。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按Gold逐步核：S02应为4-nitrotoluene→4-nitrobenzyl alcohol，答案S1给4-methylcatechol+nitrite；S03应为4-nitrobenzyl alcohol→4-nitrobenzaldehyde，答案S2用4-methylcatechol→2-methylmuconate；S01终步4-nitrobenzaldehyde→4-nitrobenzoate完全缺失。矩阵保留程序事实UNRESOLVED/MISSING，但按原答与Gold反应记录可判目标反应均未命中或漏交付，S=0，D3a落&#91;1,2&#93;，取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_038：给出S02/S03/S01的目标底物与产物，足以比对答案目标反应是否命中；不证明具体蛋白活性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_038：给出accepted酶名/EC集合；不证明答案替代酶或具体蛋白底物谱。
- ANSWER_TEXT / steps：显示答案两步的底物、产物、酶名与EC，并显示没有终步。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 物种级Pseudomonas putida与Gold/E0的TaxID 303一致，可作为部分身份支持；但答案菌株TW3、TaxID null及complete_pathway_organism_profile_id=ORG_001的整路能力均无E0菌株级记录支持。E0另有P. putida mt-2 PaW1/pWWO记录，不能回填TW3。D3b取5：合理物种候选，但关键菌株身份与整路能力待核。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida物种级分类身份，不支持TW3菌株或整路能力。
- E0_EVIDENCE / f3e0:bacdive:12880：记录的是P. putida mt-2 PaW1/pWWO，不是答案TW3；不能用于回填TW3身份。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_038：支持P. putida/TaxID 303的物种级与全路径条目，不证明答案所用TW3菌株。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段虽全部出现，但filled=0、explicit_unknown=15，所有value均为null/unknown，未交付任何可评价的性状事实。按全null性状模块处理为MISSING=1，不宣称检测到科学错误；完成度问题在D1已体现。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_038：提供P. putida的性状参照行，但不回填答案缺失的性状来源。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_038：显示本题可评分性状集合；不把答案null自动判成错误。
- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：显示15项性状全部null/unknown，模块未实质交付。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案唯一来源EVID_001为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null，且被用于步骤、酶和微生物的宽泛claim；没有可定位外部来源。决策相关核心组均为MISSING_SOURCE，按D5低分档给1；没有外部引用可核，故不登记VERIFIED_MIS_CITATION，也不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：显示EVID_001为INTERNAL_KNOWLEDGE_ONLY，且无database/record_id/locator；不是可定位外部来源。

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确标出首步EC未确认、muconate SMILES未确认、15项性状无来源且填null，证据来源标为internal/low，这些披露具体且诚实。但它把替代路线写成指定route_summary，并设complete_pathway_organism_profile_id=ORG_001，未披露该整路声称缺菌株级支持；属局部过度确信/主要限制未完全说明，取6，不判系统性误导。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：显示答案明确披露EC、SMILES和性状来源未知。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_038：显示P. putida物种级整路记录，不证明答案TW3整路能力；用于判断整路声称披露边界。

</details>
