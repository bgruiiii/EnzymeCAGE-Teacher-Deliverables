# BIOPATH150_036：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：resorcinol degradation

污染物：Resorcinol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 76.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 55 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 77 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 56.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 69 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 35 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`62d69c7531a5cee6973090348bfcb5348d3326d9dc0bdd75ef75ef2c4aef3b71`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案覆盖了题面要求的路径、逐步酶/EC、对应微生物、3个organism_profiles的15项性状及证据登记；chosen_route_name原样填写，JSON可解析。额外下游步骤属补充，不构成遗漏；仅少量范围说明可再收紧。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖5步主链、每步酶与对应微生物、3个organism profile各15项性状、来源登记与不确定性说明，route_scope.chosen_route_name原样填写。主要缺项是S4主产物3-oxoadipyl-CoA、S5主底物3-oxoadipyl-CoA及S5主产物succinyl-CoA/acetyl-CoA的SMILES均为null，未满足“每一步主底物与主产物均给SMILES”的字段要求；此外部分性状为显式null或仅内部知识来源。整体大部分必要内容完整，属少量遗漏，定8档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_036：本题gold为LINEAR_UNIQUE、ordered_step_count=3；仅支持任务范围核对，不要求交付全图旁支。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_036：支持resorcinol降解路线名与终点主线范围；不证明答案每一步科学正确。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 主链三步化学转化方向与骨架基本正确：resorcinol羟化为hydroxyquinol，邻位开环为maleylacetate，再还原为3-oxoadipate；后续β-ketoadipate延伸步骤也化学连贯。首步酶EC与gold accepted入口酶不同，但反应式本身成立，属局部需核，不构成主链断裂或方向反转；额外下游不扣D2。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold一致：resorcinol→1,2,4-benzenetriol（hydroxyquinol）→maleylacetate→3-oxoadipate，方向、芳环羟化、邻位开环、还原与后续CoA转移/硫解连续；S1把O2/NADPH列入，S2列O2，S3列NADH，S4列succinyl-CoA，S5列CoA，未见原子明显不守恒或无说明跳步。S4/S5为gold终点3-oxoadipate下游延续，按P29不进入覆盖率扣分；故给9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：给出参考的主底物/主产物与方向：resorcinol→1,2,4-Benzenetriol→Maleylacetate→3-Oxoadipate；仅支持参考反应骨架，不证明具体酶活性。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 仅评3个必答目标反应。答案S2=hydroxyquinol 1,2-dioxygenase EC 1.13.11.37对应gold S01，答案S3=maleylacetate reductase EC 1.3.1.32对应gold S03，二者与accepted集合名称/EC逐字一致；但程序对这两步因电荷/表示等价未裁定而保持ROUTE_HOLD_REPRESENTATION，不能据此确认S。答案S1目标为resorcinol→1,2,4-benzenetriol，使用phenol 2-monooxygenase EC 1.14.13.7，而gold S02 accepted为resorcinol 4-hydroxylase (NADPH) EC 1.14.13.219，属UNRESOLVED_NONACCEPTED；无已核催化矛盾，不判F。故三目标均为KEY/MAJOR U，7分以上受KEY/MAJOR U限制；模块已交付、无确认KEY失败，D-KEY4不触发，不整维NE。两步有精确accepted支持且逐反应用清楚，但入口EC/表示待核仍阻止进入良好档，按5–6带取6。答案S4/S5位于gold终点3-Oxoadipate之后，属于额外下游，不用作D3a目标信用加分。

<details><summary>V0.4理由与本行变化背景</summary>

S2 EC1.13.11.37（hydroxyquinol 1,2-dioxygenase）与S3 EC1.3.1.32（maleylacetate reductase）与gold一致；S4 EC2.8.3.6、S5 EC2.3.1.16为3-oxoadipate下游经典酶，合理但不在gold切片。S1给出resorcinol hydroxylase/phenol 2-monooxygenase EC1.14.13.7，而gold首步为resorcinol 4-hydroxylase (NADPH) EC1.14.13.219；E0无EC1.14.13.7条目，无法核实该替代酶对resorcinol的具体催化，按待核扣分，不判关键错误。主要步骤酶对应有支持，首步需修订，定7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：列出必答目标步可接受酶名与EC：S01/hydroxyquinol 1,2-dioxygenase EC 1.13.11.37，S02/resorcinol 4-hydroxylase (NADPH) EC 1.14.13.219，S03/maleylacetate reductase EC 1.3.1.32；不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：支持三条必答目标反应的底物/产物与方向：S01 1,2,4-benzenetriol→maleylacetate；S02 resorcinol→1,2,4-benzenetriol；S03 maleylacetate→3-oxoadipate。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_036：支持本题主链为3步、LINEAR_UNIQUE，D3a目标分母为3；不把终点后下游并入必答目标。
- ANSWER_TEXT / 62d69c7531a5cee6973090348bfcb5348d3326d9dc0bdd75ef75ef2c4aef3b71：定位答案各步的酶名/EC与目标反应声称，用于与accepted集合逐反应用比对。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> required步的微生物归属（T. cutaneum、S. japonicum UT26、P. putida KT2440）与相应步骤催化功能大体相符；答案明确complete_pathway_organism_profile_id=null，未把单步菌写成整条路径菌。KT2440使用TaxID 303为种级记录、非菌株级，属粒度不足待核；但该步为额外下游，且主要微生物推荐未因此被推翻。

<details><summary>V0.4理由与本行变化背景</summary>

P. putida KT2440的物种身份有E0 taxid303支持；但303为种级记录，不能单独核实KT2440菌株，ATCC47054/NC_002947未在E0冻结，属粒度不足档内扣。T. cutaneum与S. japonicum UT26的身份/步级能力仅有自由文本文献或内部知识，E0未核；S. japonicum UT26的LinE/LinF用于非氯化hydroxyquinol/maleylacetate步骤需限定作用范围。未发现跨属/无关类群或把单步写成整条路径能力的系统性错误，主要微生物推荐部分有支持，定7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_036：参考步级微生物归属覆盖多个类群；不把某一条参考菌等同于唯一答案，也不证明答案所选菌的具体反应能力。
- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida种名与TaxID 303的官方分类对应；不支持P. putida KT2440菌株级同一性。

</details>

### D4 性状科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 15项性状均按profile返回；已填定性性状与所指对象的常见特征大体相符，KT2440的保藏号与基因组基础信息也接近常见记录。关键定量项多明确填null/unknown，未被冒充为观测值；少量内部知识性状未逐条核验，属局部问题。

<details><summary>V0.4理由与本行变化背景</summary>

每个profile均给出15项性状，关键项大体合理：P. putida KT2440最适30°C、ATCC47054、NC_002947约6.18 Mb/GC61.5%与已知KT2440信息一致；S. japonicum UT26革兰氏阴性/鞘脂外膜、LinE/LinF、γ-HCH降解能力合理；T. cutaneum酵母形态、好氧、酚类利用合理。但多数性状仅INTERNAL_KNOWLEDGE_ONLY，E0无对应记录；T. cutaneum温度、S. japonicum温度/盐度等关键项为显式null，已给内容的可核实性有限。未发现数值离谱到误导筛选或把预测冒充观测的关键错误，定7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_036：给出本题可评分性状与completeness_only子项；支持按已给内容评D4，不要求把null当错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_036：逐子字段标记observed/ pending/ completeness_only；仅用于判断哪些子项可核，不自动证明答案数值正确。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 主链/酶/微生物有具体文献或数据库条目及claim_scope，但E0对EC与自由文本引文均无可核记录，核心组只能登记UNRESOLVED_SOURCE；多个性状证据为INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE。按D5六状态合成，决策相关组部分可定位、部分缺失，处5–6档；无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案证据登记有结构：路线/酶/菌身份使用EVID_001/002/004具体文献或EVID_003数据库条目，性状多数使用EVID_005/006/007（INTERNAL_KNOWLEDGE_ONLY）。问题在于：三条文献为自由文本未解析、EC与NC_002947均无E0冻结记录，无法实际核对；T. cutaneum/S. japonicum UT26性状及多数P. putida KT2440性状无可用外部来源，属MISSING_SOURCE；P. putida KT2440菌株身份仅种级TaxID支持，粒度不足。无经核实错引，不触发cap；按5–6档下沿取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：支持参考酶/EC的accepted范围；不自动核验答案EVID_001/002/004的具体文献支持范围。
- E0_EVIDENCE / f3e0:bacdive:12880：仅给出P. putida mt-2 PaW1(pWWO)菌株记录及部分保藏号/培养温度；不支持KT2440 ATCC 47054或答案中全部性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_036：显示大量性状子字段为completeness_only或无观测记录；支持把内部知识性状登记为缺失来源而非虚构错引。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案区分了文献、数据库、内部知识、未知/null与confidence，列出EC记忆值、文献待核、菌名新组合、异构体表述及未确认全链等限制；多数未核项以low/medium/unknown保留。个别INTERNAL_KNOWLEDGE_ONLY性状仍标medium，属局部过度确信，但未系统性把预测写成实证，也未掩盖主要矛盾。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties列出7项具体限制：首步酶物种差异、EC号记忆待核、硫解酶EC异名、未能确认单一菌株完成全链、UT26新组合名、马来酰乙酸互变异构、各菌性状来自内部知识未逐条核对；多处confidence=low/medium，未知项填null，并明确厌氧分支不属于评分主链。未见系统性把预测写成观测或掩盖主要矛盾；个别内部知识性状仍标medium，属档内扣分，定8档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`ed3ab034acf295593ab651c7f4810adb90045c1290ea82221d7df5dc441bf8e7`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 题面要求的resorcinol degradation主链前3步均有交付，步骤含底物/产物、酶与微生物，route_scope.chosen_route_name原样填写；15项性状字段齐备并保留unknown/null。额外给出S4–S5下游步骤且部分CoA类SMILES为null，属于非主要完整性问题，故在良好档取8而非9。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的模块均有实质回应：5步主链（S1–S5）每步给出主底物/产物英文名、酶名+EC、对应微生物与profile引用；route_scope.chosen_route_name原样回显&quot;resorcinol degradation&quot;；15项性状字段全部出现；evidence_registry 7条内部引用闭合。缺陷为字段级遗漏：S4/S5的Succinyl-CoA、3-Oxoadipyl-CoA、Acetyl-CoA等smiles为null（题面要求给SMILES），且首两步未列O2/NADPH。属7–8档&quot;大部分必要内容完整、少量遗漏&quot;，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ed3ab034acf295593ab651c7f4810adb90045c1290ea82221d7df5dc441bf8e7：显示答案含5步、逐步酶与微生物、15项性状及route_scope填写；部分下游CoA SMILES为null
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_036：本题冻结通路名为resorcinol degradation，ordered_step_count=3
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_036：冻结终点主产物为3-Oxoadipate；不直接评价答案额外下游步骤的科学正确性

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 必需主链三步的有机转化与连接成立：resorcinol→hydroxyquinol→maleylacetate→3-oxoadipate，终点产物为3-oxoadipate。主要缺陷是S1缺O2/NADPH、S2缺O2、S3缺NAD(P)H等辅因子/计量标注，S4–S5为额外下游且S5缺CoA底物；这些属局部计量与表达问题，按P103在7–8档取7，不触发cap。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步吻合且方向正确：Resorcinol→1,2,4-Benzenetriol(Hydroxyquinol)（4-羟化）→Maleylacetate（1,2-开环）→3-Oxoadipate（还原，方向与gold反向补全一致）；SMILES与gold结构对应（苯三酚Oc1ccc(O)c(O)c1、maleylacetate与gold同一分子）。题面未指定终点，答案覆盖到gold终点3-oxoadipate，其后S4（CoA转移，含succinyl-CoA作cofactor、succinate作byproduct）与S5（硫解生成acetyl-CoA/succinyl-CoA）化学正确，按四.2/P29额外下游延续不加分亦不扣分。缺陷：首两步未标注O2/NADPH等辅因子，字面计量不完整，按八.辅因子条款属局部计量缺陷，定档7–8，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ed3ab034acf295593ab651c7f4810adb90045c1290ea82221d7df5dc441bf8e7：显示S1–S3底物/产物与方向；显示辅因子未列入及S4–S5额外下游
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：冻结主链方向为Resorcinol→1,2,4-Benzenetriol→Maleylacetate→3-Oxoadipate，并给出参与者角色
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_036：冻结终点为3-Oxoadipate；额外下游不进入必需主链评分范围

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 3个必需目标反应均有酶信息交付，但均未成为已确认S：S01、S03因表示/路线对齐挂起为U；S02为accepted EC非匹配待核U。S2的hydroxyquinol 1,2-dioxygenase/EC 1.13.11.37与accepted集合精确对应，但目标对齐仍U；S1的resorcinol 4-hydroxylase/EC 1.14.13.166与accepted EC 1.14.13.219不符，S3的maleylacetate reductase/EC 1.3.1.45与accepted EC 1.3.1.32不符，均因无冻结EC记录保持U而非已验证F。故为部分目标有适用支持的低档，取5；无已确认KEY失败，不适用KEY4上界。

<details><summary>V0.4理由与本行变化背景</summary>

5个酶名与所在步反应类型自洽（羟化酶/开环双加氧酶/还原酶/CoA转移酶/硫解酶），S2的EC 1.13.11.37与hydroxyquinol 1,2-dioxygenase在酶gold中一致（SUPPORTED）。但S1标EC 1.14.13.166，而本题gold冻结酶记录为resorcinol 4-hydroxylase (NADPH) EC 1.14.13.219；S3标EC 1.3.1.45，而gold为maleylacetate reductase EC 1.3.1.32——冻结证据中这两个EC均无条目（GAP-036-005/GAP-036-008），按四.6/P66记UNRESOLVED，保留低分与待核标记、不判CONTRADICTED、不cap。关键步骤酶-EC对应仍有2处待核，属5–6档&quot;有合理候选和部分支持、若干关键步骤缺具体核验&quot;，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ed3ab034acf295593ab651c7f4810adb90045c1290ea82221d7df5dc441bf8e7：显示三个目标步的酶名与EC交付
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：冻结accepted酶记录：resorcinol 4-hydroxylase (NADPH)=1.14.13.219；hydroxyquinol 1,2-dioxygenase=1.13.11.37；maleylacetate reductase=1.3.1.32；不证明具体蛋白实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：冻结三步目标反应及方向，用于目标步映射；不自动补足EC记录

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> TaxID 303 is supported for Pseudomonas putida name identity, and the answer uses one deduplicated species-level profile. However there is no step-level reaction capability evidence and no evidence for complete_pathway_organism_profile_id=ORG_001. This fits the 5-6 band: plausible candidate and partial identity support, but key reaction/pathway capability remains unverified.

<details><summary>V0.4理由与本行变化背景</summary>

身份侧：5步统一给物种级Pseudomonas putida、ncbi_taxid=303、未声明菌株（strain=null），声称粒度与证据粒度匹配，且官方分类记录中303的学名与Pseudomonas putida精确匹配（SUPPORTED），不构成身份错配或跨类群错引。能力侧：全部5步归属同一菌并声明complete_pathway_organism_profile_id=ORG_001，等于把整条路径能力系于单一物种，但冻结证据仅有身份记录存在、步级归属（L2）与全路径能力（L3）均语义未核（UNRESOLVED）；gold各步列出多个不同宿主（Corynebacterium glutamicum、Paraburkholderia、Sphingobium等），gold非穷尽故不据此判错。身份正确但作用范围与整路径能力未获反应级证据，属5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Official taxonomy record supports Pseudomonas putida name/TaxID 303 identity only; it does not support strain-level identity, step catalysis, or complete pathway capability.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> All 15 trait fields are present, with explicit nulls for F3/F4/F5/F14 and filled generic species-level values for others. However most filled values rely on EVID_007 INTERNAL_KNOWLEDGE_ONLY with no raw_text or locatable database record. Some values are plausible for P. putida, but key traits are not source-verified; 5-6 band fits partial applicability with material evidence gaps.

<details><summary>V0.4理由与本行变化背景</summary>

已给的11项性状中，氧需求（aerobic）、呼吸方式（O2为末端受体）、细胞形态（rod-shaped）、革兰氏（Gram-negative）、产孢（non-spore-forming）、运动性（polar flagella）、栖息地（土壤/水体/根际）与种级Pseudomonas putida的通行特征一致，未出现数值离谱或把物种观测写成全菌株普适的越级外推；温度项只给preference=mesophilic、数值留null，符合&quot;培养温度≠最适值&quot;的约束。关键缺口：温度/pH/盐度定量值、保藏号、基因组信息均null或unknown（P. putida mt-2记录实际含DSM 3931等保藏号与26/30°C培养温度，答案未用，评价者也不得回填），F7/F9/F15描述较笼统、无raw_text原文；冻结证据无该物种的观测性状卡可核。属5–6档&quot;部分性状准确适用但关键项证据不足&quot;，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> All evidence entries EVID_001-EVID_007 are INTERNAL_KNOWLEDGE_ONLY with database, record_id, and locator null. No path, enzyme, organism, or trait conclusion can be traced to a locatable external source. This is MISSING_SOURCE, not verified mis-citation, so it is a low-band D5 score without cap; 2 reflects that a structured claim-to-evidence registry exists but is non-locatable.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 7条全部source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，仅以局部标签与claim_scope（step:S1…、organism:…、traits:…）自关联。按四.3/P34，&quot;完全无引用或仅有INTERNAL_KNOWLEDGE_ONLY类自我声明&quot;归MISSING_SOURCE；本题决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）与支持组全部为MISSING_SOURCE，无一条条目级可定位可核对证据，故按P41&quot;全部缺失→低分档（默认不cap）&quot;落入1–2档，取2。不存在已核实错引（无外部编号/文献被引用），severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> The answer uses medium confidence widely and gives explicit nulls for some unknown traits, but it does not explain limitations, does not provide uncertainties, and treats internal knowledge as medium-confidence support. This is not a systemic prediction-as-observation cap, but confidence strength exceeds disclosed evidence; 5-6 band.

<details><summary>V0.4理由与本行变化背景</summary>

正面：4项完全未知性状以value=null+confidence=unknown如实标注，未编造数值；evidence_registry显式把全部来源标为INTERNAL_KNOWLEDGE_ONLY，没有把内部知识包装成数据库直查，属于对证据性质的诚实标注。负面：uncertainties数组为空，route_summary与steps以断言口吻给出主链，酶、菌身份、降解能力一律confidence=medium且零披露&quot;记忆值/建议复核&quot;，也未说明&quot;未核EC/未核全路径能力&quot;等主要待验证点，结论强度超过依据。属&quot;有不确定性说明但笼统、部分结论强度超过依据&quot;的单点/多点过度确信而非系统性把预测写成实证，5–6档取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`32101f2045d73fce1228f6fa7e1653e5abe6ce4fd7987f7264b97826c8ef3598`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 必答主链S1–S3均在且顺序正确，3-oxoadipate到达；S4/S5为额外下游，不是漏答；15性状字段齐全，明确未知有标注。扣分点为S1 EC缺省、部分CoA酯SMILES为null、额外下游混入steps，故为良好档上沿但非满分。

<details><summary>V0.4理由与本行变化背景</summary>

五步主链、每步底物/产物（含SMILES）、对应酶与微生物、15项性状、来源登记与不确定性均已实质交付，chosen_route_name原样回填为resorcinol degradation；ORG_001去重后由各步引用，符合去重要求。不足：S1酶未给EC（题面要求每步给EC），若干辅因子/CoA酯SMILES留空——属少量遗漏，落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_036：确认本题共同主链为3步线性路线，额外下游不构成必答分母
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_036：确认题面路线名与终点为resorcinol degradation至3-Oxoadipate

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> S1–S3主链化学转化、方向与终点正确：resorcinol→hydroxyquinol→maleylacetate→3-oxoadipate；S1/S3辅因子已列，S4/S5额外下游化学上合理。局部表达缺陷为CoA酯SMILES null、S1/S3电荷表示边界未自动确认；主链化学无已核失败，取8。

<details><summary>V0.4理由与本行变化背景</summary>

前3步与gold逐一对上：S1 resorcinol→1,2,4-benzenetriol（羟化，O2+NAD(P)H，生成H2O/NAD(P)+）、S2 hydroxyquinol邻位开环→maleylacetate、S3→3-oxoadipate；方向、碳数与结构成立，辅因子在列。S4/S5为gold终点下游的β-酮己二酸公共步（CoA转移、硫解），化学正确且题面未指定终点，按四.2不扣覆盖率；厌氧/反硝化替代路线已声明不属于评分主链。未达10仅因NAD(P)H与CoA酯SMILES留空、戊糖计量未逐式配平。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：支持S02→S01→S03主链方向与主产物；不证明额外CoA步骤为必答

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 三必答目标反应均有可辨认酶/功能且主反应匹配：S2为hydroxyquinol 1,2-dioxygenase EC 1.13.11.37，S3为maleylacetate reductase EC 1.3.1.32，均命中accepted；S1点名resorcinol hydroxylase并给出resorcinol→hydroxyquinol，EC null仅阻止精确名称—EC配对与9–10高档，不构成KEY失败。按judge-required与base range&#91;1,8&#93;取8。

<details><summary>V0.4理由与本行变化背景</summary>

S2 EC1.13.11.37（hydroxyquinol 1,2-dioxygenase）与S3 EC1.3.1.32（maleylacetate reductase）与gold酶表一致，反应类型与酶名相称；S4 2.8.3.6、S5 2.3.1.174与β-酮己二酸公共步匹配。S1仅给“resorcinol hydroxylase”且EC=null并自述无权威EC，而gold该步有1.14.13.219——属少量条目待补，落7–8档取8；EC官方条目在E0无冻结记录，按UNRESOLVED登记，不判错。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：accepted set支持1.13.11.37、1.3.1.32及resorcinol 4-hydroxylase功能；不证明S1蛋白级活性或任意具体蛋白底物谱
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：支持三步底物/产物与方向

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 所有必答步均归属Corynebacterium glutamicum；organism_gold确认TaxID 1718在S01/S02/S03均有对应，且PATHWAY_COMPLETE为TRUE。ATCC 13032菌株级精确身份/基因链接未在E0确认，属局部U；物种身份、步级归属和完整路径能力已支持，故不cap，取8。

<details><summary>V0.4理由与本行变化背景</summary>

各步统一归属Corynebacterium glutamicum（TaxID 1718），与gold STEP行（S01/S02/S03均含1718）及PATHWAY_COMPLETE行（taxid 1718，pathway_complete=TRUE）一致，未出现异菌株编号或跨类群错配，未把单步菌写成整路径菌。但gold侧1718为物种级记录，答案的菌株级身份（ATCC 13032）与“整条路径能力”仅由自由文本文献EVID_001支撑，属八.D3b①粒度不足，档内扣取7，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_036：支持C. glutamicum TaxID 1718在三个必答步的EXACT归属及PATHWAY_COMPLETE；不单独确认ATCC 13032菌株级档案

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 主要形态/染色/运动/产孢、温度偏好中温等与trait_gold 1718一致；F14大小与GC落入种级范围。未支持点包括把30°C、pH7.0写成最适值，F8宽泛芳香物清单与F15栖息地广适性外推，ATCC 13032菌株级档案未核。CG11–13条件为FALSE属辅助，CG14所支撑的目标resorcinol能力有PATHWAY_COMPLETE支持；无关键性状被推翻，取7。

<details><summary>V0.4理由与本行变化背景</summary>

关键性状与gold观测对得上：F10无运动性、F12革兰氏阳性、F13不产孢、F11棒状、F14 GC 53.8%且在2.1–3.43Mb范围内，身份一致。问题：F2只给optimum 30°C（源自BacDive培养/生长温度，不是最适证据，且未附raw_text）；F4盐度直接留null；F6仅列O2为末端受体（gold观测到reduction: nitrate=true）；F8广谱芳香族降解仅凭内部知识且confidence=medium。整体属“主要性状可核实、少量条件与数值解释需修订”，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_036：支持1718多种形态/染色/运动/产孢与部分温度、基因组范围；不确认任意菌株最适值或F15
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_036：显示1718温度/pH optimal子字段无observed scalar，不能作为已证最适值

</details>

### D5 来源与可核查性：7 / SCORED

V0.4旧分5 → V0.5新分7，变化+2。

新裁判理由：

> 核心路线有EVID_001文献题录及EVID_002/3/4数据库EC/reaction定位，S1–S3、菌株、基因组和多数性状均能追到具体记录；但E0不能核验这些来源，F3/F6/F8/F15使用INTERNAL_KNOWLEDGE_ONLY，ATCC/NC_003450存在E0 gap。无经核实错引，不cap；交付记录部分可定位、部分内部/待核，取7。

<details><summary>V0.4理由与本行变化背景</summary>

8条证据登记均具条目级定位形式（文献题录、KEGG/BRENDA EC号及反应式、NCBI登录号NC_003450、BacDive DSM 20300、EAWAG-BBD链接），且逐条挂到具体步骤/性状，非仅库名；但决策相关组（CG01/CG02/CG03/CG05/CG07/CG09）的条目在本案E0均无冻结记录可核，只能登记UNRESOLVED_SOURCE；F3/F6/F8/F15为INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）。无任何已核实错引，故不cap。按P41“存在条目级可定位结论→5–6档”，因可核对部分极有限取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：核对accepted EC/酶名存在性；不核验答案所引文献正文或E0记录
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_036：用于核对部分性状事实；不把种级记录回填为答案原始来源

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> uncertainties明确说明氧条件null、S1 EC/基因未知、全路径证据有限、基因组/性状参考值需复核，并将厌氧替代路线标为不计分主链；多数confidence与来源强度相称。局部仍有把30°C/pH7.0写成最适值的过强表达，但非系统性预测冒充观测，无已核矛盾掩盖，取8。

<details><summary>V0.4理由与本行变化背景</summary>

题面氧条件为null，答案明确声明按经典好氧路线给主链、把厌氧与反硝化路线列入alternative_branches并标is_part_of_scored_main_route=false；uncertainties逐条给出S1缺EC、S2互变异构处理、酶学确证有限、基因组/性状建议复核，证据性质区分较好。扣分点：F8/F15等内部知识值仍标medium且无raw_text，F2把培养温度当optimum，属单点过度确信而非系统性误导，未掩盖主要矛盾——落7–8档取8。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Qwen

答案SHA256：`f03866f63d7a16482048d3be49cbf66b8d02887e5ac73d6314b22d29b848c10d`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 题面指定路线名原样保留，输出为3步连续主链，每一步均有酶名与对应微生物，15项性状槽位齐全，JSON可解析；但所有步骤EC均为null，maleylacetate与beta-ketoadipate等结构SMILES缺失，性状多数为null或仅INTERNAL_KNOWLEDGE_ONLY低置信来源，属于主要模块均涉及但若干必要内容遗漏、仅低证据占位，故落5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

全部模块均实质涉及：3步主链、每步绑定酶名与菌、15项性状全部出现、证据与不确定性登记齐备；route_scope.chosen_route_name 原样填 &#x27;resorcinol degradation&#x27; 符合题面。档内取7：三酶EC全null、两中间体SMILES null，酶/结构字段完整度受限（均按任务允许的null如实填写，非编造）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / f03866f63d7a16482048d3be49cbf66b8d02887e5ac73d6314b22d29b848c10d：显示3步主链、1个organism_profile及15项性状槽位；所有enzyme.ec_number为null，maleylacetate与beta-ketoadipate的SMILES为null，证据仅INTERNAL_KNOWLEDGE_ONLY。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_036：冻结formal case为resorcinol degradation、LINEAR_UNIQUE、ordered_step_count=3；支持路线名与3步主链长度，不支持把全图旁支当缺步分母。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_036：根化合物Resorcinol，终点3-Oxoadipate；支持题面路线与终点参照。
- RUBRIC_CLAUSE / P45：诚实填写未知/null反映D1完成度不足，不能与编造等同。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链方向与核心转化合理：resorcinol→hydroxyquinol（1,2,4-benzenetriol同义）→maleylacetate→beta-ketoadipate（3-oxoadipate同义），步骤连续且包含开环与还原。与gold相比首步使用NADH而gold为NADPH，属局部辅因子/氧化还原计量问题；缺陷在于部分中间体SMILES未给出，但名称转化本身未见主链级化学错误，故7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

三步化学与gold BSY-p00342 主链一致：resorcinol→hydroxyquinol（羟化）→maleylacetate（邻位开环）→β-ketoadipate（还原），方向、步骤顺序与终点(3-oxoadipate)均正确，连续无跳步。档内取8：S1辅因子用NADH（gold为NADPH）、S2/S3中间体SMILES null等局部计量/结构缺陷，不改变主链结论。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / f03866f63d7a16482048d3be49cbf66b8d02887e5ac73d6314b22d29b848c10d：答案给出resorcinol→hydroxyquinol→maleylacetate→beta-ketoadipate三步，首步列O2/NADH，第三步列NADH/NAD+；maleylacetate与beta-ketoadipate未给SMILES。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：gold反应切片显示resorcinol+NADPH+O2→1,2,4-Benzenetriol；1,2,4-Benzenetriol+O2→Maleylacetate；maleylacetate+NAD(P)H+H+→3-Oxoadipate及方向；支持主转化与终点，不支持答案具体NADH选择。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_036：终点化合物为3-Oxoadipate；支持将beta-ketoadipate按同义终点理解，但不额外延伸下游评分。
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏/局部计量问题通常在D2的7–8档处理，不自动cap。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> N=3。S02路线为STRICT_MATCH，但酶名“resorcinol hydroxylase”不在accepted“resorcinol 4-hydroxylase (NADPH)/EC 1.14.13.219”集合且EC为null，故为U；S01路线为NAME_ONLY_UNRESOLVED/UNKNOWN，属表示边界未决，不能判S；S03诊断MISSING/UNBOUND，但原答实际含maleylacetate reductase与beta-ketoadipate（3-oxoadipate同义），属对齐/同义未绑定而非确证漏答，按C03保留U。因而S=0、U=3、无已核F/M；部分酶功能与accepted集有对应，但无EC/名称配对核验且全部主目标仍U，不能进7–8档，故5。

<details><summary>V0.4理由与本行变化背景</summary>

三酶名均与gold accepted名对应：hydroxyquinol 1,2-dioxygenase(=EC1.13.11.37)、maleylacetate reductase(=EC1.3.1.32)、resorcinol 4-hydroxylase(=EC1.14.13.219)，功能-反应类型匹配正确。档内取6：三酶EC全null、无基因/蛋白、来源仅内部知识，属&#x27;有合理候选和部分支持、关键步骤缺具体核验&#x27;。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / f03866f63d7a16482048d3be49cbf66b8d02887e5ac73d6314b22d29b848c10d：三个目标步均给出酶名但ec_number全为null；S2为hydroxyquinol 1,2-dioxygenase，S3为maleylacetate reductase，S1为resorcinol hydroxylase。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：accepted/ gold enzyme rows：S01含hydroxyquinol 1,2-dioxygenase与EC 1.13.11.37；S02为resorcinol 4-hydroxylase (NADPH) EC 1.14.13.219；S03为maleylacetate reductase EC 1.3.1.32；支持酶名/EC目标，不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：支持三步目标反应的方向和主底物/产物，包括S02 strict match及S01/S03的表示/绑定待核事实。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_036：确认本题为3步LINEAR_UNIQUE主链，N=3；不把全图旁支当作D3a缺步分母。
- RUBRIC_CLAUSE / C03：U包括对齐/实体/名称—EC配对/相应粒度支持尚不可确定；对齐未绑定不等于漏答。
- RUBRIC_CLAUSE / C04：全U由裁判依现有材料判断，不自动NE或低分；高U比例阻止7–8档，但不自动判错。
- RUBRIC_CLAUSE / C05：5分适用于部分主干目标有适用支持但仍有局部表达或关联问题、不能进良好档。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案仅给Acinetobacter calcoaceticus名称、无strain/TaxID/保藏号，且E0/gold无该菌记录；同一未支持菌被用于全部三步并支持整路能力。未发现已核身份矛盾，故不cap；按‘合理候选但关键身份/作用范围未充分核验’取5。

<details><summary>V0.4理由与本行变化背景</summary>

全程唯一菌Acinetobacter calcoaceticus为真实种名且属已知芳香族降解菌，但不在本题gold organism清单，被赋予完成整条三步路径（全路径能力）却零条目级证据、confidence=low。属&#x27;合理候选、作用范围（全路径）未充分核验&#x27;；未核实不判虚构、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_036：gold step organisms为Paraburkholderia/Sphingomonas/Rhizobium/Rhodococcus/Corynebacterium等，未列A. calcoaceticus；不证明其不能降解。
- E0_EVIDENCE / f3e0:bacdive:12880：该记录为Pseudomonas putida mt-2 PaW1，不支持A. calcoaceticus身份或能力。
- E0_EVIDENCE / f3e0:taxid:303：TaxID 303为Pseudomonas putida分类记录，不适用于A. calcoaceticus。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项性状齐全，但A. calcoaceticus无E0/gold性状记录；F2/F3/F4/F5/F14为null，其余多为low confidence且关键降解性状F7/F8/F9无来源。未发现已核数值/单位/菌株矛盾，按‘部分性状可作低置信候选、关键项证据不足’取5。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状多为Acinetobacter属一致、正确的一般性状（革兰氏阴性、球杆菌、不运动、不产孢、需氧、有氧呼吸）；但应用关键的F7(利用间苯二酚)、F8(降解能力)、F9(羟化酶/双加氧酶活性)是对未经核实路径声称的重述、无来源（EVID_002=内部知识）；F2/F3/F4/F5/F14为null。属&#x27;部分性状准确适用、关键项证据不足&#x27;。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_036：gold traits覆盖其他step organisms，无A. calcoaceticus记录；不验证本题性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_036：列出各gold organism性状可评分性；A. calcoaceticus行仅有证据缺口登记，无观测值。
- E0_EVIDENCE / f3e0:bacdive:12880：P. putida记录不能回填为A. calcoaceticus性状来源。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> EVID_001/EVID_002均source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null；无任何可定位条目支持路线、酶、菌或性状。属MISSING_SOURCE低档，不是已核实错引，默认不cap；给2而非1因仍有内部证据标签和claim_scope登记。

<details><summary>V0.4理由与本行变化背景</summary>

两项证据均source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator全null，无法定位任何条目或文献→决策相关组（CG01/CG02/CG03/CG05/CG07）全部MISSING_SOURCE。按MISSING_SOURCE低分档评2；属缺失非误导，默认不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：冻结快照仅有P. putida记录；不能支持答案的A. calcoaceticus或路线claim。
- E0_EVIDENCE / f3e0:taxid:303：TaxID303为P. putida；不定位答案任何来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案明确列出氧条件未指定、EC未填、菌株/生理性状缺来源、SMILES未确认，并把多数性状标low/unknown；不确定性披露具体，未系统把预测写成实证。但路线/菌仍以低置信陈述给出且无来源，故取7而非8–10。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露诚实具体：route_scope.notes声明&#x27;氧条件未指定、按常见好氧主链填写&#x27;；uncertainties列出EC未填/SMILES未确认/菌株与生理性状缺来源；各步uncertainty与confidence=low一致；未见把预测包装成观测的系统性误导。档内取7：缺少观测vs预测的结构化区分，且F7/F8/F9降解能力声称未标注为对路径声称的重述。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：E0仅有P. putida分类记录，不能支持A. calcoaceticus；答案对此未完全展开。

</details>

## Grok

答案SHA256：`fce33d8a867e291d1392aba500d700dd656e7a99ff03e2130fc3b6ea39f855c5`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求的 resorcinol degradation 主链、逐步酶/微生物和15项性状均有实质回应；答案覆盖gold三步主链并另列下游β-酮己二酸延续，额外下游按P29不额外加分亦不扣分；仅有少量SMILES/EC为null或物种级代表菌的完整性限制。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_036_question：题面指定 route_scope.chosen_route_name=resorcinol degradation，氧条件null，要求每步底物/产物、酶/EC、微生物及15项性状。
- ANSWER_TEXT / ANSWER.steps;ANSWER.organism_profiles：答案交付5步、1个ORG_001 profile及15项性状；额外下游步骤不用于提高主链完成度。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_036：gold ordered_step_count=3、LINEAR_UNIQUE；答案覆盖S01-S03主链并额外延伸S4/S5。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链 resorcinol→hydroxyquinol→maleylacetate→3-oxoadipate 的方向、开环/还原及β-酮己二酸延伸在化学上连贯；辅因子细节有省略或NADH/NADPH不确定性，若干CoA化合物SMILES为null，属局部计量/表达缺陷，不推翻主链。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps.S1-S5：答案给出主链及额外下游的底物、产物、反应类型和连接。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：gold支持S02 resorcinol→hydroxyquinol、S01 hydroxyquinol→maleylacetate、S03 maleylacetate→3-oxoadipate的方向与主要转化；不覆盖答案额外S4/S5。

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S2 hydroxyquinol 1,2-dioxygenase EC 1.13.11.37 与S3 maleylacetate reductase EC 1.3.1.32 均与accepted集合精确对应；S1以generic resorcinol hydroxylase覆盖resorcinol→hydroxyquinol功能，但EC null且NADH/NADPH与accepted 1.14.13.219不完全对齐，阻止9–10，按&#91;7,8&#93;取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps.S1-S3.enzyme：S1 resorcinol hydroxylase EC null；S2 hydroxyquinol 1,2-dioxygenase EC1.13.11.37；S3 maleylacetate reductase EC1.3.1.32。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：gold列出S01 hydroxyquinol 1,2-dioxygenase EC1.13.11.37、S02 resorcinol 4-hydroxylase (NADPH) EC1.14.13.219、S03 maleylacetate reductase EC1.3.1.32；支持策展粒度酶-反应对应，不证明具体蛋白实测。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：gold反应行支持三步主链的底物/产物方向；S01/S03的charge-blind表示问题不改变产物层面对应。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Pseudomonas putida种级TaxID 303身份可由E0支持，但答案无指定菌株、对每一步均使用同一种级代表并声称完整路径能力；gold步骤菌并不包含P. putida，且无P. putida完成该resorcinol全路径的对应证据，属身份可定位而能力/粒度未充分核验的5–6档。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：官方分类记录支持Pseudomonas putida种级TaxID 303身份；不支持具体菌株或全路径能力。
- E0_EVIDENCE / f3e0:bacdive:12880：记录为P. putida mt-2 PaW1菌株事实及培养温度/底物面板；不支持答案未指定菌株的resorcinol全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_036：gold步骤菌列出来源不同菌株；未列P. putida不自动判错，但说明答案菌种选择未被gold步骤直接交叉支持。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Gram阴性、杆菌、运动、不产芽孢、好氧等基础性状与P. putida常识相符；但温度定量、盐度、resorcinol利用及F9路径酶活均无逐条支持，且把种级/代表菌性状用于全路径能力论证，属部分性状可用但关键项证据不足的5–6档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles.ORG_001.traits：答案给出15项性状，其中12项filled、3项显式null；多项性状evidence为INTERNAL_KNOWLEDGE_ONLY。
- E0_EVIDENCE / f3e0:bacdive:12880：记录仅支持该菌株培养温度26/30°C阳性及底物面板等局部事实；不支持答案的4°C/41°C表述、resorcinol利用或F9路径酶活。

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 关键路线、酶、菌和性状均主要依赖EVID_001/EVID_002的INTERNAL_KNOWLEDGE_ONLY，locator只笼统提及KEGG/EAWAG-BBD，无具体条目、DOI、record_id或可核对记录；属MISSING/GENERIC来源低档。无经核实错引，故不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：EVID_001/002均source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id为null，locator仅泛称KEGG/EAWAG-BBD；不能定位到具体条目。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确标注evidence_registry为INTERNAL_KNOWLEDGE_ONLY，列出氧条件未指定、EC缺失、代表菌无 strain、β-酮己二酸连接推断、辅因子歧义及性状raw_text缺失等限制；不确定性与证据性质总体相称，仅部分F8/F9仍偏强。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties;ANSWER.evidence_registry：答案披露INTERNAL_KNOWLEDGE_ONLY、EC缺失、菌株未定、推断连接、辅因子和性状null等限制。

</details>

## GPT5.6

答案SHA256：`bf44aa08664ed4c5c5c5477e07c43b72ef50b582debbf1bbd76fa344d8eb5d3b`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1基础区间&#91;1,4&#93;。答案只交付两步，缺少题面主链终点3-Oxoadipate；两步酶均无EC；唯一organism_profile的15项性状全部为null/明确未知。它覆盖了路线名、部分步骤与部分酶菌关联，因此不取1；但关键主链步骤和性状模块均明显不完整，落在较低档，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_036：本题参考主链为3步，不是2步；仅证明所需步数，不证明答案其他内容。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_036：题面路线终产物为3-Oxoadipate；不证明S1/S2的具体反应产物。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2基础区间&#91;1,6&#93;。第一步resorcinol羟化为1,2,4-benzenetriol与参考S02一致；但第二步把1,2,4-benzenetriol开环产物写成2-hydroxymuconic semialdehyde，而参考S01为maleylacetate，属于主链关键转化/产物错误；随后又缺3-Oxoadipate终点。因关键化学转化已错，D2按关键错误压制在≤4内，取4（保留第一步正确与边界清楚）。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：支持S01目标开环产物为maleylacetate；不支持2-hydroxymuconic semialdehyde。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：支持S01酶名/EC与1,2,4-trihydroxybenzene开环相关；不证明答案给出的错误产物。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按JUDGE_REQUIRED与给定accepted/gold判读可见交付：S02目标resorcinol 4-hydroxylase对应resorcinol-&gt;1,2,4-benzenetriol，可算作一个可用目标；S01目标要求1,2,4-benzenetriol-&gt;maleylacetate，而答案给成2-hydroxymuconic semialdehyde，不能按目标步支持；S03终点maleylacetate-&gt;3-oxoadipate完全未交付。以可见主链计，3个目标中仅1个有可用功能对应，S/N≈0.33，落&#91;C04 3,4&#93;带，取3。程序target mapping仍为UNRESOLVED且current_path_id为空，故不宣称已确认KEY正式失败或D-KEY4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_036：支持S02第一步匹配及S01目标产物；不支持答案S2产物。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_036：支持各步酶-EC参考集合；不证明答案未给的EC或未交付的S03。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出Pseudomonas putida KT2440（TaxID 160488）并用于两步，但仅EVID_002 INTERNAL_KNOWLEDGE_ONLY，未给菌株级来源或反应级能力证据；冻结gold本案步级微生物行未列该菌株，E0仅有P. putida物种/其他菌株记录。身份看似合理、候选可辨认，但反应能力与作用范围未核，因此落5-6档，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_036：列出参考步级相关微生物；不证明P. putida KT2440具有这些反应能力，且gold非穷尽。
- E0_EVIDENCE / f3e0:taxid:303：仅支持P. putida物种级分类名；不支持KT2440菌株身份或任何步骤催化能力。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 唯一organism_profile的15项性状均以value null/confidence unknown返回；虽有字段外壳但没有任何已填性状值或可核来源。按P44，全部必需性状均为null/空值时D4按MISSING=1处理，不宣称检测到具体性状科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示15项性状均为null/unknown；不提供任何性状数值或来源。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_036：说明本题存在可用性状参照/可评分字段；不证明答案已交付性状。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案仅登记EVID_001与EVID_002，二者source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null，无法沿条目定位或核对支持内容。按D5六状态，所有决策相关组为MISSING_SOURCE，落低档&#91;1,2&#93;；因答案至少显式标注internal和low confidence并给出claim_scope，取2而非1。无已核实错引，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示仅有内部知识声明，无可定位数据库/文献记录；不证明任何外部来源存在。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案把酶/菌confidence标为low，并在step uncertainty和uncertainties中明确说明EC、酶学命名、菌株直接证据及氧条件未指定等限制；性状全部null而非编造。主要证据性质和边界披露较好，符合7-8档；不足是未明确指出S2产物与参考maleylacetate冲突，因此不取9-10，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案对EC、菌株证据、氧条件等作不确定性披露；不证明其科学结论正确。

</details>
