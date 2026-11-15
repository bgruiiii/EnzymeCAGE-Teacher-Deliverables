# BIOPATH150_014：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：2-nitrobenzoate degradation II

污染物：2-Nitrobenzoate；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 45.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 33 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 55 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 44.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 54.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 35 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`cf8d970da63e67d35154d875c4da3e6360a1d9ce12b6e33a817d0c3f1612c4da`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分3 → V0.5新分4，变化+1。

新裁判理由：

> 结构化输出完整，steps、酶、微生物和15项性状均已给出；但主链按2-hydroxylaminobenzoate→3-hydroxyanthranilate→pyruvate/acetaldehyde延伸，未遵循题面冻结路线要求的anthranilate→catechol主链。任务路线偏离属D1关键错误，允许范围&#91;1,4&#93;；因格式与模块覆盖较完整，取4。

<details><summary>V0.4理由与本行变化背景</summary>

题面明确指定路线名并要求不得改选其他路线；冻结gold的2-nitrobenzoate degradation II为三步线性链（2-nitrobenzoate→2-hydroxylaminobenzoate→anthranilate→catechol，终点catechol）。答案在route_scope.chosen_route_name原样填写路线名并自称“按题面指定路线名称作答”，但主链自S2起改为2-hydroxylaminobenzoate经Bamberger重排生成3-hydroxyanthranilate并延伸至pyruvate+acetaldehyde，未包含gold路线II的anthranilate与catechol两个关键节点，属“自称合规却交付不同化学路线”的任务参数偏离（P100），构成D1关键错误。模块层面（10步、酶、菌、15性状字段、来源与不确定性）交付较完整，故cap档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：显示冻结主链为2-nitrobenzoate→2-hydroxylaminobenzoate→anthranilate→catechol；支持D1路线偏离判断，不评价答案替代化学本身。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案替代路线的多数化学步骤（硝基还原、3-hydroxyanthranilate开环、aminomuconate代谢至pyruvate/acetaldehyde）在形式与方向上连贯，辅因子多处列明；关键问题在S2：2-hydroxylaminobenzoate经Bamberger型重排到3-hydroxyanthranilate缺少EC和可核证据，且为路线分叉核心。D2允许范围&#91;1,6&#93;，主链部分成立但关键连接需实质核验，取6。

<details><summary>V0.4理由与本行变化背景</summary>

就答案实际交付的主链本身看：硝基→羟氨基4电子还原计量正确；Bamberger重排生成3-hydroxyanthranilate与已知经3-hydroxyanthranilate的2-硝基苯甲酸代谢一致；3,4-开环、脱羧、醛脱氢、脱氨、互变异构、脱羧、水合、醛醇裂解至pyruvate+acetaldehyde的转化方向、碳数与官能团连接逐级自洽，末段oxalocrotonate支线与教科书序列一致。扣分点：该路线并非题面指定路线，且其证据仅为内部知识、无可核来源（四.5第3步：无可核证据→按未证实登记，不自动判错也不给高分）；S1产物侧漏写H2O（属局部计量缺陷，P103）；S2的“mutase”归属与中间体立体化学未定。落5–6档“主干部分成立、合理性证据有限”。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：仅作冻结参考主链定位；D2对答案替代路线的化学连续性独立评价。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 程序事实为S=0、F=1、U=2、H=0、M=0；S03为已确认KEY失败，触发D-KEY4上界≤4，允许范围&#91;1,4&#93;。答案在入口步骤附近有局部可用信息，但没有已确认目标信用，且关键中间步被替代，目标主推荐不可用；因此在&#91;1,4&#93;内取2，不机械取4。

<details><summary>V0.4理由与本行变化背景</summary>

酶名与反应类型逐步骤功能相符：硝基还原酶（硝基→羟氨基）、3-hydroxyanthranilate 3,4-dioxygenase（开环双加氧）、ACMS脱羧酶（脱羧）、氨基粘康酸半醛脱氢酶（醛→酸）、2-aminomuconate deaminase（水解脱氨）、4-oxalocrotonate tautomerase（互变异构）、4-oxalocrotonate decarboxylase（β-酮酸脱羧）、水合酶、醛缩酶。但仅4步给出EC且全部无冻结记录可核（E0 GAP→UNRESOLVED），6步EC为null；S2“mutase”是否为真实酶催化无法核实。属“有合理候选和部分支持，若干关键步骤仍缺具体核验”的5–6档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：S03目标为2-hydroxylaminobenzoate→anthranilate；答案产物3-hydroxyanthranilate不支持该目标反应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_014：S03 accepted enzyme为2-hydroxylaminobenzoate reductase；答案S2为mutase且无EC，不能获得目标信用。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案将全部10步归给同一Pseudomonas sp.，无strain、TaxID或菌株级证据，并声明complete_pathway_organism_profile_id=ORG_001。gold中S02可涉及Pseudomonas fluorescens，但S01/S03使用其他菌，且PATHWAY_COMPLETE未列Pseudomonas sp.。属身份粒度不足与整路能力过度声称，但未有E0证据证明所给菌名/能力为已核实错误，故不触发已核实cap；按多步骤归属与能力范围问题取4。

<details><summary>V0.4理由与本行变化背景</summary>

全部10步与complete_pathway_organism_profile_id共用单一“Pseudomonas sp.”（strain、TaxID均null），即以属级身份承担“单菌完成整条路径”的能力声称，且唯一依据是INTERNAL_KNOWLEDGE_ONLY、confidence medium/low，属身份粒度不足+作用范围外推。属级选择本身合理（gold路线II的S02硝基还原酶亦列出Pseudomonas fluorescens），故不判已核实错误、不cap；落5–6档“有合理候选和部分支持，关键身份或作用范围仍未充分核验”，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_014：显示各gold步的已知菌与完整路径菌；不能证明Pseudomonas sp.绝不能降解，故仅支持粒度/匹配不足与未核状态。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项性状均出现：10项填写、5项明确未知。氧耐受、革兰氏阴性、不产孢、杆状、运动性等属Pseudomonas属级合理描述；但F7称以2-nitrobenzoate为唯一碳源/氮源、F8称矿化，以及F9酶活，均绑定到未定菌株的Pseudomonas sp.且无来源，属关键项证据不足与过度推广。定量性状多为null，未编造；D4取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现：10项填写（F1、F6、F7、F8、F9、F10、F11、F12、F13、F15），5项明确未知（F2温度、F3 pH、F4盐度、F5保藏、F14基因组）。填写项多为属级一般性状（革兰氏阴性、不产芽孢、杆状、可运动）与好氧属性，与Pseudomonas属相符，且氧需求与题面好氧条件（CG10 APPLICATION_CRITICAL）一致；但F7“以2-nitrobenzoate为唯一碳源、氮源与能源”与F8“矿化为CO2与H2O”等菌株级能力被写成事实，身份却仅到属、无定位来源，且F8与其自身末产物（pyruvate/acetaldehyde）不完全一致。属“部分性状准确且适用，关键项证据不足”，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_014：展示gold菌株可评分性状；未含Pseudomonas sp.，故不能支持答案菌株级性状。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案evidence_registry的EVID_001–EVID_003全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；关键路线、酶、微生物和性状结论均无可定位外部来源，属MISSING_SOURCE。因其仍提供局部evidence_id到claim_scope的映射并诚实标注内部知识，取低档2而非1；来源缺失本身不触发D5 cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅3条，source_type全为INTERNAL_KNOWLEDGE_ONLY，无任何可定位的数据库条目、文献DOI或计算记录；decision-relevant组（CG01/02/03/05/07/08/09/04/10）全部为MISSING_SOURCE，SUPPORTING组同。按四.3与八.D5：MISSING_SOURCE按低分档、默认不触发cap；因连笼统库名/文献列表都没有，落1–2档“几乎无法定位重要结论依据”。答案对每条证据给出claim_scope并如实声明无外部来源，属缺失而非误导，故不判错引、不cap；无已核实错引，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案明确标注所有证据为内部知识，列出路线名称歧义、菌株/TaxID缺失、多个EC为记忆性记录、立体化学未指定等；缺失项多填null，证据性质披露较强。但仍有若干中等置信的功能/整路能力表述，尤其Pseudomonas sp. complete pathway与F7/F8较易读成实证或整路结论，故未给9-10；取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案的uncertainties具体且非模板化：路线名歧义（若II实指anthranilate路线则第2步及下游需改）、菌株/TaxID不可核实故为null、6步EC未定、中间体立体化学未定、4个EC为记忆值、全部证据为内部知识。未知项以null如实表达，未编造字段。扣分点：F7/F8等属级能力以medium confidence陈述而全无来源，route_summary/complete_pathway把单菌全路径能力当作既成事实，F8“矿化为CO2与H2O”与其自身末产物略冲突——属“部分结论强度仍超过依据”的单点过度确信，未达系统性误导，D6不cap。取6。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`7a14db4a90e55022adb27b81d41e4e052254c92ba3726c8eb08ca7284a45f548`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D1档1–2：答案格式完整且给出8步、酶、菌与性状框架，但实际主链替换为2-nitrobenzoate→2-nitrophenol→catechol→β-酮己二酸，未按题面锁定的2-nitrobenzoate degradation II（2-nitrobenzoate→2-hydroxylaminobenzoate→anthranilate→catechol）交付；15项性状全为null/unknown。属严重任务路线偏离，任务符合度低。

<details><summary>V0.4理由与本行变化背景</summary>

题目要求指定路线2-nitrobenzoate degradation II，并要求完整路径、酶、微生物及15项性状。答案虽返回8步路径、酶和微生物，但S1/S2采用2-nitrobenzoate 2-monooxygenase/2-nitrophenol 2-monooxygenase经2-nitrophenol到catechol的路线，与gold路线II的nitroreduction→2-hydroxylaminobenzoate→anthranilate→catechol入口不同，却在route_scope自称路线II；同时两个profile的15项性状全部为null。按P100，自称合规却交付不同化学路线属D1关键错误；路径/酶/菌模块存在但路线偏离且性状模块未交付，取3分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_014：gold根/终点身份为2-Nitrobenzoate到Catechol，路线BSY-p00161；不证明答案替代路线。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：gold指定主链为2-nitrobenzoate→2-hydroxylaminobenzoate→anthranilate→catechol；不支持2-nitrophenol分支。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_014：gold S02为nitroreductase、S01为anthranilate dioxygenase；不证明答案单加氧酶路线。
- ANSWER_TEXT / ANSWER.steps：显示答案实际经2-nitrophenol和β-酮己二酸延伸；不表示该路线符合题面指定路线。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> D2档5–6：所答2-nitrobenzoate→2-nitrophenol→catechol→β-酮己二酸方向一致、步骤连接基本合理，属已知替代降解逻辑；但首两步辅因子/副产物（O2、NADPH、CO2、nitrite等）未列，部分产物SMILES为null，局部计量与证据不足；按base range &#91;1,6&#93;取6。任务路线偏离不在D2重复扣分。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付的2-nitrobenzoate→2-nitrophenol→catechol→β-ketoadipate路线在宽泛化学轮廓上连贯，S3-S8的β-ketoadipate步骤基本合理；但相对题目指定路线II，缺失nitroreduction/2-hydroxylaminobenzoate/anthranilate入口，S1/S2未列CO2/nitrite及O2/NADPH等辅因子，且全部为内部知识、无外部依据。关键中间体与入口转化仍需修订、合理性证据有限，落在5-6档低端，取5分；路线名称/任务符合度偏离已在D1处理，D2不因同一任务参数问题再cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：提供gold反应方向与辅因子示例；不证明答案替代路线已获实验支持。
- ANSWER_TEXT / ANSWER.steps：显示答案主链、方向、产物与缺失SMILES/辅因子；不表示化工细节完整。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> D3a确认S=0、F=1、U=2；S02为D-KEY4确认的KEY_ENTRY目标失败：答案S1为2-nitrobenzoate→2-nitrophenol（EC 1.14.13.166），目标S02要求2-nitrobenzoate→2-hydroxylaminobenzoate（nitroreductase，EC 1.7.1.-/NOT_OBSERVED）。无已核目标成功，S01/S03仅未对齐；按D-KEY4上界≤4及C05低档取2。不把U当成功或失败。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶名与EC大类同所写反应类型基本自洽（monooxygenase、dioxygenase、isomerase、lactonase、CoA-transferase、thiolase），但S1/S2采用的1.14.13.166/1.14.13.167不是gold路线II的nitroreductase/anthranilate dioxygenase体系，且无gene/protein标识；全部EC均为INTERNAL_KNOWLEDGE_ONLY，E0为EVIDENCE_GAP，无法核accepted name/reaction与条目状态。属有合理候选但若干关键步骤缺具体核验，取5-6档的6分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_014：gold S02目标为2-nitrobenzoate nitroreductase/nitrobenzoate nitroreductase，EC 1.7.1.-或NOT_OBSERVED；不证明答案EC 1.14.13.166可催化该目标。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：目标S02产物为o-Hydroxylaminobenzoic acid；不支持答案产物2-nitrophenol。
- ANSWER_TEXT / ANSWER.steps：显示答案S1为2-nitrobenzoate→2-nitrophenol、S2为2-nitrophenol→catechol；不显示目标S02 nitroreductase步骤。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> D3b档5–6：答案给出P. fluorescens KU-7与P. putida KT2440（TaxID 160488）；KU-7在organism_gold中作为本案S02菌株出现，KT2440为常用菌株且TaxID常见，属合理候选并有部分对应。但S01/S03目标菌未按gold给出，KU-7对S1/S2单加氧酶、KT2440对S3-S8多步能力未在冻结证据中核验，若干关键作用范围未充分核验，取5。无编造物种/TaxID或把单步写成完整路径的证据，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案使用真实感较强的菌名/菌株：P. fluorescens KU-7与P. putida KT2440；未声称complete_pathway_organism_profile_id，避免把单步菌直接写成全路径菌。但S1/S2及KT2440的步级归属与gold路线II的S01-S03菌谱不一致，KU-7未给TaxID，KT2440 TaxID 160488无法在E0核验，且所有证据仅为内部知识。属有合理候选但关键身份/能力未充分核验，取5-6档的6分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_014：gold列出本案S02可含Pseudomonas fluorescens KU-7，以及S01/S03的Acinetobacter/Burkholderia/Arthrobacter等；不支持KT2440下游逐步能力。
- ANSWER_TEXT / ANSWER.steps：显示答案将KU-7用于S1-S2、KT2440用于S3-S8；不证明这些逐项反应能力。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> D4：两个organism_profiles的15项性状全部为null/unknown，未提供数值、单位、条件或来源；按P44全部必需性状null/空值时D4 MISSING=1，不宣称检测到科学错误，完成度问题主归D1。

<details><summary>V0.4理由与本行变化背景</summary>

两个organism_profile均把15项性状填为value=null/confidence=unknown，没有任何性状数值、单位或条件值。按P44，全部必需性状均为null时D4记MISSING=1，不宣称检测到科学错误；完成度缺失主要由D1反映。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_014：冻结trait表含部分目标菌观测性状；答案未交付任何对应值。
- ANSWER_TEXT / ANSWER.organism_profiles：显示所有15项性状均为null且confidence=unknown；不显示任何可评价性状值。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> D5低档：全部证据条目source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，无任何可定位文献、数据库条目或计算记录与结论建立对应关系；属MISSING_SOURCE。无已核实错引，不触发错引cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry的EVID_001-EVID_008全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，没有任何可定位文献、数据库条目或计算记录；关键路径、酶、菌与性状结论均无法沿外部记录核查。属MISSING_SOURCE，按低分档取2分；单纯来源缺失默认不cap。E0为EVIDENCE_GAP，也无可核实错引，故不判CRITICAL/SYSTEMIC。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示所有来源均为INTERNAL_KNOWLEDGE_ONLY且无database/record_id/locator；不建立可定位来源。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D6档5–6：答案在uncertainties中承认酶EC/菌株信息基于内部知识可能有偏差，且未知性状填null，体现部分诚实；但大量步骤/酶/菌株以high/medium confidence呈现，证据均为INTERNAL_KNOWLEDGE_ONLY，未逐条区分观测、预测、推断与未知，置信与证据强度不完全相称。属有不确定性说明但偏笼统，档内取5。非系统性把预测写成实证，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案把evidence_registry统一标为INTERNAL_KNOWLEDGE_ONLY，并在uncertainties中笼统提示EC编号和菌株信息可能偏差；性状全null也体现未知。但步骤级confidence多为medium/high，仍以内部知识支撑路线II主链，且未披露route_scope路线名与实际monooxygenase入口路线不一致这一主要限制。属“有不确定性说明但过于笼统、部分结论强度超过依据”，取5-6档的5分；非系统性把预测写成实证，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示仅一条泛化不确定性声明；不证明逐条置信校准充分。
- ANSWER_TEXT / ANSWER.evidence_registry：显示来源均为内部知识；不证明high/medium置信有外部证据支撑。

</details>

## Kimi

答案SHA256：`48bae9a1a694583b96f31ee4e0a65341d82363f78ff20da8b5f516d82442d033`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 题面指定route II；gold主链为S02→S03→S01（2-nitrobenzoate→2-hydroxylaminobenzoate→anthranilate→Catechol）。答案仅首步2-nitrobenzoate→2-hydroxylaminobenzoate与S02相符，随后转入3-hydroxyanthranilate/2-aminomuconate分支，未交付S03 anthranilate与S01 Catechol终点。所有输出模块和15项性状均出现，但指定路线/终点偏离属D1关键错误，cap≤4；因模块齐全且首步可辨，取4。

<details><summary>V0.4理由与本行变化背景</summary>

七类模块均实质交付：5步主链、每步首选酶与对应菌、15项性状（9项填写/6项明确未知/0遗漏）、7条证据登记、4条不确定性；chosen_route_name与oxygen_condition按题面原样回显，未改选路线名。扣分点：S3–S5开链中间体SMILES为null、S1酶EC为null（均按题面null纪律诚实置空，但属必要子信息缺失）；5步复用同一菌株代表（题面允许，但弱化步级对应）。路线化学分支与冻结gold主链不一致所形成的任务符合度疑点登记review_queue，不据此作D1关键错误（任务参数偏离与路线化学质量分轴见八.D1/D2边界）。落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_014：gold路线II终点为Catechol；不支持答案以2-aminomuconate为终点。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：支持gold S02→S03→S01主链及S01产生Catechol；不评价答案替代分支的化学质量。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 按化学自身质量评：nitroreduction→Bamberger型重排→3-hydroxyanthranilate开环→脱羧→醛氧化至2-aminomuconate，方向为降解、步骤连接连续，主链化学总体可成立。局部缺陷明显：S1/S3/S5未列NADPH/O2/NAD+等辅因子，S3–S5开链中间体SMILES为null；且这是替代分支而非gold路线，按D2独立化学分不因路线偏离自动重罚。7–8档中取7，因多处局部计量/结构表达缺失阻止进入9–10。

<details><summary>V0.4理由与本行变化背景</summary>

化学主干内部自洽：S1硝基→羟胺还原方向正确；S2分子内重排到3-羟基邻氨基苯甲酸；S3 3,4-双加氧开环；S4脱羧并显式给出CO2副产物；S5醛脱氢到2-氨基粘康酸，产物/底物逐级衔接，无起始步错误、无方向反转、无无说明跳步。缺陷：NADPH/O2/NAD+等辅因子未列入反应式（属局部计量缺陷，按八.辅因子条款不cap）；S3–S5开链中间体SMILES为null，结构核对受限；S2之后与冻结gold分支（羟氨基苯甲酸→anthranilate→catechol）分离，替代分支无条目级可核证据（EVID_001仅路线名），按四.5第3步“按未证实登记，不自动判错也不给高分”。落5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：提供gold路线反应方向和终点作为对照；不证明答案替代分支每一步都被实验确认。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 逐目标步：S02（2-nitrobenzoate→2-hydroxylaminobenzoate，nitroreductase）有gold enzyme/reaction支持，记S；S03要求2-hydroxylaminobenzoate reductase→anthranilate，答案改为mutase→3-hydroxyanthranilate，记F；S01要求anthranilate dioxygenase→Catechol，答案未给该酶/反应，改走开环脱羧分支，记F。S=1,F=2,N=3，C=1/3落&#91;3,4&#93;；S01为KEY_TERMINAL、S03为必经中间步缺失，D-KEY4上界4适用。因仅1/3目标反应可用且关键终点缺失，取3；未另认定独立EC错配，故key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

五步各给一首选酶且酶名与反应类型相符（硝基还原酶/分子内重排酶/3,4-双加氧酶/脱羧酶/醛脱氢酶）；EC大类与反应类型未见矛盾（1.13双加氧、4.1.1脱羧、1.2.1醛脱氢、5.4.4分子内转移）。但S1硝基还原酶EC=null（gold该步为通配EC 1.7.1.-，答案未给出，属信息不足非错误）；EC 1.13.11.6/4.1.1.45/1.2.1.32/5.4.4.1在E0均无冻结记录（GAP-014-001~004），无法核accepted name/reaction/条目状态，按未证实登记。属“有合理候选和部分支持、若干关键步骤仍缺具体核验”，落5–6档取6；不因引用问题按D3a关键错误处理（OBS-D3A-D5）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_014：支持gold S02 nitroreductase、S03 hydroxylaminobenzoate reductase、S01 anthranilate dioxygenase；不证明替代mutase/开环分支用于目标credit。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：支持S02→S03→S01目标反应方向与产物；不扩展到3-hydroxyanthranilate替代分支。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 身份层：Arthrobacter protophormiae RKJ100在gold S02 organism行有EXACT记录（No TaxID），首步菌株关联可支持；但答案把RKJ100写成全五步代表菌并设置complete_pathway_organism_profile_id=ORG_001。gold的PATHWAY_COMPLETE仅见A. protophormiae 37930等物种级记录，未见RKJ100菌株级全路径证据；替代步骤S2–S5的菌株催化能力无冻结记录。属合理候选+部分支持，但多个单步/整路能力未核，5–6档取5，不触发身份cap。

<details><summary>V0.4理由与本行变化背景</summary>

菌名与菌株token在冻结gold中存在（Arthrobacter protophormiae，TaxID 37930；“Arthrobacter protophormiae RKJ100”，No TaxID），身份定位不属编造；答案诚实标注现名可能为Glutamicibacter protophormiae、TaxID/保藏号未知。问题：①粒度不足——gold的PATHWAY_COMPLETE记录属物种37930，RKJ100无菌株级完成路径记录，答案以complete_pathway_organism_profile_id=ORG_001把整条路径能力绑到RKJ100（八.D3b①档内扣，默认不cap）；②S3–S5步级归属与酶学能力无任何可核证据（EVID_002无标识）；③gold的S01对应菌为Acinetobacter baylyi/Burkholderia cepacia/Burkholderia terrae，与答案分支不同，不据此判身份错误。落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_014：支持S02 exact RKJ100身份及部分物种级PATHWAY_COMPLETE；不支持RKJ100在替代分支各步或整条替代路径的能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 15项均出现，6项明确null，无把预测写成观测的数值捏造。已填性状多为物种/属级低中置信描述：Gram阳性、杆状—球状、非产孢与A. protophormiae物种记录大体相容；但RKJ100菌株级性状在gold全为UNKNOWN，F6好氧呼吸/O2、F7底物利用、F8/F9降解与酶活等缺少菌株级适用证据，F1又借路线氧条件而非菌株耐氧记录。属部分准确+关键项证据不足，5–6档取6，因null诚实且无离谱数值/系统性外推。

<details><summary>V0.4理由与本行变化背景</summary>

15项一次返回：9项填写、6项明确未知（F2/F3/F4/F10/F14及F5空保藏号），无编造，符合题面null纪律。已填项以物种级一般性状为主，与冻结gold物种记录方向一致（gram positive=true、cell shape=rod-shaped为OBSERVED；sporulation=false为PREDICTED）；但F1“好氧”、F6“好氧呼吸/O2”与gold的aerotolerant=true语义不完全对应且引路线条目EVID_001；F7“可利用2-nitrobenzoate”在trait_gold无物种级记录；F8“本路线确证”措辞偏强；F9把路线酶活写成菌株活性；F15诚实写“证据不足”属正面。数值型关键性状（温度/pH/盐度/基因组）全为明确未知，其完成度缺口归D1不重复重扣（八.D4）。属“部分性状准确且适用、关键项证据不足”，落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_014：物种37930的Gram阳性/杆状等记录可作物种级参照；RKJ100菌株级记录为UNKNOWN，不支持把物种值写成菌株实测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_014：显示RKJ100多数性状subfield为completeness_only；不能作为菌株级精确观测分母。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 答案有EVID_001–EVID_007登记：路线仅给MetaCyc pathway name无record_id；菌株来源为PubMed无标识文献；一般性状为INTERNAL_KNOWLEDGE_ONLY；EC 5.4.4.1/1.13.11.6/4.1.1.45/1.2.1.32给ExplorEnz record_id但E0无记录。决策相关组中路线/终点/菌株来源偏笼统，部分酶-EC给到条目级标识但无法核验。无已核实错引，不能判CRITICAL/SYSTEMIC；5–6档取5，因关键路线/终点与菌株仍缺可核对映射。

<details><summary>V0.4理由与本行变化背景</summary>

按6个条件组+核心组登记后，决策相关组（CORE+APPLICATION_CRITICAL）没有任何“条目级可定位且可核对”的证据：CG01/02/03仅有MetaCyc路线名（record_id=null）；CG07/08/09依赖无标识PubMed报告；CG10把路线条目EVID_001用于氧性状（超出其自述claim_scope）；CG14目标污染物能力声称证据不可定位；CG17无登录号（诚实null）。CG05给出ExplorEnz EC条目指针，但E0无冻结记录（GAP-014-001~004等），只能UNRESOLVED。无已核实错引→不cap，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。按P41合成规则，决策相关组以笼统/待核来源为主→3–4档；因存在部分EC级指针且来源结构自洽，取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：仅用于登记答案实际交付来源；不把其内容回填为已核实证据。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案总体明确区分未知：EC未确认、TaxID/保藏/基因组号null、开链SMILES null、菌名可能异名、nitroso中间体合并均写明；confidence多为medium/low，未把预测写成实验。主要缺陷是未披露其S2后主链与题面route II的anthranilate/Catechol方向不一致，且个别EC标high confidence却无E0核验。属大部分不确定性与限制已标注、但主要路线冲突未清楚说明，7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体：EC未确认、现名可能变更为Glutamicibacter protophormiae、开链中间体SMILES未断言、2-nitrosobenzoate可能单列等4条列明；null与unknown标签使用规范；F15明确写“证据不足”属正面做法。但置信标签多处超出依据：F7以不可定位文献给high；F8用“本路线确证”；F9/F1/F6以路线条目作性状/酶活证据仍标medium；EVID_001标DATABASE_DIRECT但record_id=null，EVID_002标LITERATURE_DIRECT但无标识。属多点过度确信与证据类型标注不严，未达系统性把预测写成实证或掩盖矛盾的程度（不cap）。落5–6档取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_014：gold终点Catechol；用于说明答案未披露路线II终点冲突，不要求D6替代D1任务判断。

</details>

## Qwen

答案SHA256：`627ab1a19d2e58b037b7ca4c489a246e7fc82d45181f53fb651f55b599513a02`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> The answer is structurally complete: route name/oxygen are echoed, four steps have substrates/products, enzyme/microorganism objects, and all 15 trait slots exist. However it replaces the specified 2-nitrobenzoate degradation II main chain with a 3-hydroxy-2-nitrobenzoate/3-hydroxyanthranilate route and omits the gold terminal anthranilate-&gt;catechol step. Route deviation makes this a D1 task-conformance key error capped at 4; score 4 reflects complete delivery but major task nonconformance.

<details><summary>V0.4理由与本行变化背景</summary>

档位判定：主要模块均有涉及，但必要内容多处缺失（3/4步未给EC、S4主产物SMILES缺失、15项性状仅5项填写、微生物仅属级&#x27;Pseudomonas sp.&#x27;），本应对应5–6档；又因任务参数偏离——题面限定route_scope.chosen_route_name原样填写&#x27;2-nitrobenzoate degradation II&#x27;且禁止改选，答案自述&#x27;按题面指定路线填写&#x27;但交付3-羟基化-硝基还原-开环支路——按八.D1/D2边界条款属D1关键错误，封顶后取档上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_014：Supports the gold route name, root 2-nitrobenzoate, and terminal catechol; does not by itself establish the answer chemistry.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：Supports the required gold orientation S02-&gt;S03-&gt;S01 and the terminal catechol-producing S01 reaction.
- ANSWER_TEXT / steps：Shows the answer uses S1 2-nitrobenzoate 3-hydroxylation and a 3-hydroxyanthranilate ring-cleavage chain rather than the gold S02/S03/S01 route.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分4 → V0.5新分6，变化+2。

新裁判理由：

> As a chemical sequence independent of target-route credit, the proposed route is internally coherent: aromatic 3-hydroxylation, nitro reduction to hydroxylamine, reduction to 3-hydroxyanthranilate, and 3-hydroxyanthranilate 3,4-dioxygenase ring cleavage. But it is a substituted route rather than the specified route, cofactors/electron donors and stoichiometry are omitted, and the final product SMILES is missing. This places D2 in the partial/alternative-route band, not high tier.

<details><summary>V0.4理由与本行变化背景</summary>

档位判定：答案自身支路的化学类型、方向与连接自洽（3-羟基化→硝基还原→羟氨基还原→3-羟基邻氨基苯甲酸3,4-开环），无方向反转、无一步跳中心代谢物，辅因子/电子供体全缺但已在每步uncertainty披露（属局部计量缺陷）；若仅看内部化学可达7–8档。但按四.5四步判断：题面已指定路线（第1步成立）；答案未声明替代路线或范围边界而是声称合规（第2步不成立）；所用支路无可核证据（EVID_001仅INTERNAL_KNOWLEDGE_ONLY，第3步不成立）；该偏离使D2&#x27;题面指定路线主链&#x27;结论失效（首步转化即不同、终点未声明地由catechol改为2-amino-3-carboxymuconate semialdehyde，第4步成立）→按P62触发D2关键错误，取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：Supports the specified gold chemistry and orientation; the answer&#x27;s route is a different substitution.
- ANSWER_TEXT / steps：Shows the alternative 3-hydroxy route, omitted cofactors/stoichiometry, and S4 product with null SMILES.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> Target-level facts: gold S02 and S03 are confirmed KEY failures and S01 is unbound/missing; there is no target S. The answer&#x27;s enzyme annotations belong to a different 3-hydroxy route. Under D-KEY4 the confirmed KEY failures cap D3a at 4; because no target reaction is supported and only some local enzyme-class information is useful, score 2 is appropriate.

<details><summary>V0.4理由与本行变化背景</summary>

酶功能与所指反应类型一致：S1单加氧酶对芳环羟基化、S2硝基还原酶将硝基还原为羟氨基、S3羟氨基还原酶还原为氨基、S4 3-羟基邻氨基苯甲酸3,4-双加氧酶开环，且EC 1.13.11.6与酶名（双加氧酶）自洽。不足：3/4步无EC、无基因/蛋白标识，支撑仅EVID_001（INTERNAL_KNOWLEDGE_ONLY）；EC 1.13.11.6在E0无冻结记录（GAP-014-006/022）不可核实。属5–6档&#x27;有合理候选和部分支持，若干关键步骤缺具体核验&#x27;，取5；KE=UNRESOLVED（不cap），并保留成对局部待核。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_014：Supports gold step enzymes: anthranilate dioxygenase for S01, 2-nitrobenzoate nitroreductase for S02, 2-hydroxylaminobenzoate reductase for S03.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：Supports the gold directed reactions and the S02/S03 entry/midroute connectivity.
- ANSWER_TEXT / steps：Shows the answer&#x27;s S1-S4 use a different 3-hydroxy route and omit the gold S01 anthranilate dioxygenase step.

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> The answer uses one genus-level Pseudomonas sp. profile for all four steps, with no strain, TaxID, or step-level source. It also sets complete_pathway_organism_profile_id ORG_001 and claims broad degradation/enzyme activity from internal knowledge only. A genus-level candidate is not enough for step-specific identity or whole-path capability; this overextends one profile to a complete path, so D3b is in the weak partial band.

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份仅&#x27;Pseudomonas sp.&#x27;（strain=null、ncbi_taxid=null、无保藏号/基因组号），四种步骤与complete_pathway_organism_profile_id均归同一属级条目ORG_001；无任何反应级或全路径能力证据，来源仅EVID_001（INTERNAL_KNOWLEDGE_ONLY）。身份粒度不足（属级真实类群范围内）叠加&#x27;无单步证据即写全路径能力&#x27;的外推，属3–4档取4；疑似的身份-能力外推因E0无记录不能核实，KE=UNRESOLVED，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_014：Supports gold step-specific organisms and pathway-complete organisms; does not support a single unidentified Pseudomonas sp. for all steps.
- ANSWER_TEXT / microorganism：Shows all steps use Pseudomonas sp. ORG_001 with no strain, TaxID, or step-level evidence.

</details>

### D4 性状科学性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> All 15 trait keys are present, but only 5 are filled and 10 are explicit unknown. The filled oxygen/respiration traits are plausible at a generic Pseudomonas level, but the target carbon-utilization, broad-degradation, and 2-nitrobenzoate 3-monooxygenase activity values are asserted for an unidentified Pseudomonas sp. with internal-only support. No numeric temperature/pH/salinity data or strain-specific applicability are supplied. D4 is therefore partial but key evidence is insufficient.

<details><summary>V0.4理由与本行变化背景</summary>

15项中仅5项填写（F1好氧、F6有氧呼吸/O2、F7可利用2-硝基苯甲酸根作碳源能源、F8可降解2-硝基苯甲酸根、F9具2-nitrobenzoate 3-monooxygenase活性），其余10项为null且confidence=unknown（诚实未知，完成度扣分归D1，不在此重复重扣）。F1/F6为属级合理且与题面好氧一致；F7/F8/F9是对目标污染物的属级能力/酶活声称，无种/菌株级或可核证据（GAP-014-055~062），但均标low并披露身份未知。未出现数值/单位/菌株错配或把观测冒充实测数值。属5–6档&#x27;部分性状准确且适用，关键项证据不足&#x27;，取5；KE=N。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：Shows 5 filled traits and 10 explicit unknowns; F7/F8/F9 assert target degradation/activity with internal evidence only.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_014：Shows which gold traits for named organisms are observed/scoreable; the answer&#x27;s genus-level profile is not a substitute for those identities.

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> Traceability is weak. Route steps, S1-S3 enzymes, the single Pseudomonas sp. profile, and target trait claims cite EVID_001 INTERNAL_KNOWLEDGE_ONLY; EVID_003 is also internal-only. Only S4 enzyme EC 1.13.11.6 has a specific IUBMB record (EVID_002), and E0 cannot independently verify it. Decision-relevant groups are therefore dominated by MISSING_SOURCE with one UNRESOLVED_SOURCE; no verified mis-citation is present, so no D5 cap applies. Score 3 reflects very limited mapping between main conclusions and locatable sources.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07为CORE；CG04/CG08/CG10/CG14为APPLICATION_CRITICAL或条件关键）几乎全部仅有INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；仅CG05另有一条EC 1.13.11.6引IUBMB酶命名（含database/record_id/locator），但E0无该记录（GAP-014-006/022）→UNRESOLVED_SOURCE。无经核对实的条目级结论，亦无已核实错引（severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION），按&#x27;全部缺失→低分档、默认不cap&#x27;取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：Shows EVID_001/EVID_003 are INTERNAL_KNOWLEDGE_ONLY and EVID_002 is a specific IUBMB record for EC 1.13.11.6.
- ANSWER_TEXT / steps：Shows most step-level evidence ids point to EVID_001, not to external locatable records.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> The answer discloses many limits: unconfirmed EC numbers, omitted cofactors/electron donors, unknown species/strain/TaxID, missing final product SMILES, and mostly low/unknown confidence. This is substantially better than hiding uncertainty. It still sets complete_pathway_organism_profile_id and asserts some target trait/enzyme values for a genus-level Pseudomonas sp. from internal knowledge, so it is not top-tier, but this is not systematic misrepresentation.

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且逐条：各步注明辅因子/化学计量未列、EC未确认；uncertainties列出EC未确认、仅属级身份、辅因子缺失、S4产物SMILES缺失；confidence总体low/unknown，未把预测写成实测观测。不足：未披露其主链与题面指定路线/参照终点的偏离（反而自述合规），complete_pathway对属级菌的能力声称未标注外推性质，EC 1.13.11.6以DATABASE_DIRECT/high呈现但E0不可核、未附待复核提示。属&#x27;有不确定性说明但部分结论强度超过依据&#x27;的5–6档，取6；非系统性误导，KE=N。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：Lists unconfirmed ECs, unknown strain/TaxID/genome, omitted cofactors, and missing product SMILES.
- ANSWER_TEXT / steps：Shows per-step uncertainty and low confidence for most enzyme/microorganism claims.

</details>

## Grok

答案SHA256：`089ca9a0d6337eb4d99d0bfca81d16d891438cdd673ae0496afab5a8f911e6ec`。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 表单与主要模块齐全：route_scope原样写2-nitrobenzoate degradation II、aerobic；steps给出底物/产物/酶/菌；15项性状均出现；evidence_registry有局部记录。但必需主链未完整：gold为S02 2-nitrobenzoate→2-hydroxylaminobenzoate→S03 anthranilate→S01 catechol三步；答案S1直接写2-nitrobenzoate→2-aminobenzoate，未给2-hydroxylaminobenzoate中间步，S2才对应gold S01；catechol后S3-S8为下游续写，按P29不作为必需完成加分。性状7项null，按P45只反映完成度不足。故主要模块涉及但若干必要内容遗漏，落5-6档，取6。未确认路线改选/条件违背，不判D1 key error。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：gold S02 2-nitrobenzoate→2-hydroxylaminobenzoate、S03→anthranilate、S01 anthranilate→catechol三步；终点catechol
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_014：ordered_step_count=3；LINEAR_UNIQUE；主链材料为三步
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：S1为2-nitrobenzoate→2-aminobenzoate，未交付2-hydroxylaminobenzoate中间步
- ANSWER_TEXT / ANSWER.steps&#91;1&#93;：S2为2-aminobenzoate→catechol，对应gold S01
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：15项性状字段齐全，但F2/F3/F4/F5/F10/F14/F15等多项为null，完成度受限
- SCOPE_ROW / SCOPE#BIOPATH150_014#CG04：题面氧条件aerobic为任务条件

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 方向为好氧降解、前向；S2 anthranilate/2-aminobenzoate→catechol（EC 1.14.12.1）、S3 catechol→cis,cis-muconate（1.13.11.1）及S4-S8 β-酮己二酸步骤基本正确且连续。主要问题是S1把六电子硝基还原压成一步2-nitrobenzoate→2-aminobenzoate，只写一个NADPH和water，未给/未配平2-hydroxylaminobenzoate关键中间体，与指定路线II的partial reduction不完全一致；属关键中间体/计量需修订，未到整链方向反转或核心化学断裂。按5-6档取6；S3-S8超出catechol终点的下游按P29不另扣D2，也不加分。key_error=N。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：gold S02为2-nitrobenzoate部分还原到2-hydroxylaminobenzoate，S03再由还原酶到anthranilate，S01 anthranilate→catechol；答案S1缺少该中间步
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_014：本题为aerobic，gold终点主产物为Catechol
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：S1净写2-nitrobenzoate→2-aminobenzoate，仅列一个NADPH、water，未给2-hydroxylaminobenzoate中间体
- ANSWER_TEXT / ANSWER.steps&#91;1&#93;：S2 anthranilate 1,2-dioxygenase EC 1.14.12.1转化2-aminobenzoate→catechol，化学上基本正确
- ANSWER_TEXT / ANSWER.steps&#91;2&#93;：S3 catechol 1,2-dioxygenase EC 1.13.11.1生成cis,cis-muconate，基本正确
- ANSWER_TEXT / ANSWER.steps&#91;3-7&#93;：S4-S8为β-酮己二酸途径标准步骤，连接连续，化学基本合理
- RUBRIC_CLAUSE / P103：主有机物转化正确但辅因子遗漏通常属局部计量缺陷，不自动cap；本案仍需按关键中间体缺失修订
- QUESTION_TEXT / QUESTION.route_scope：题面指定2-nitrobenzoate degradation II与aerobic

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> N=3 required gold steps. S01 (anthranilate dioxygenase, anthranilate→catechol) is supported at name/EC level; S02 is not delivered as 2-nitrobenzoate→2-hydroxylaminobenzoate because the answer instead gives direct 2-aminobenzoate; S03 (2-hydroxylaminobenzoate reductase) is absent. S=1, F=1, M=1 gives C=1/3 → &#91;3,4&#93;. The key entry/mandatory intermediate failure keeps D3a within D-KEY4 ≤4; within band 3 because only one target is usable and the reduction segment fails.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_014：gold enzyme names/EC for S01 anthranilate dioxygenase, S02 nitroreductase, S03 2-hydroxylaminobenzoate reductase; supports target function/EC at curated level, not specific protein activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：gold directed reactions: S02 produces 2-hydroxylaminobenzoate; S03 produces anthranilate; S01 produces catechol.
- ANSWER_TEXT / ANSWER：answer S1 uses nitroreductase but products 2-aminobenzoate, not 2-hydroxylaminobenzoate; no S03 enzyme/reaction is present; answer S2 matches anthranilate→catechol.

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Arthrobacter protophormiae RKJ100 is a real strain and is supported for the nitroreductase step in gold. However the answer assigns RKJ100 to all S01/S03/S4-S8 and sets complete_pathway_organism_profile_id without a PATHWAY_COMPLETE row for RKJ100; whole-path and several step-level capabilities remain partially supported/unresolved. Identity is not fabricated and no verified key mismatch is established. 5-6 band, upper 6.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_014：gold lists Arthrobacter protophormiae RKJ100 for S02 nitroreductase; PATHWAY_COMPLETE rows are for 37930/311230/37919, not RKJ100. Supports identity for S02 but not whole-path capability.
- ANSWER_TEXT / ANSWER：answer assigns RKJ100 to every step and to complete_pathway_organism_profile_id; downstream steps are labeled low-confidence inference.

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Many required traits are null; non-null values are largely genus/species-level for A. protophormiae (Gram-positive, aerobic, non-sporeforming, rod-sphere) and plausible. The key strain-specific F7/F8/F9 claims are internal-knowledge based and F8 asserts a 2-aminobenzoate intermediate not confirmed by frozen RKJ100 trait rows. Honest nulls and labels support 5-6 band, upper 6.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_014：gold RKJ100 trait rows are UNKNOWN; species 37930 has Gram-positive, aerotolerant, rod-shaped, non-sporulating records. Species-level support does not verify RKJ100 strain-specific F7/F8/F9.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_014：identifies scoreable vs completeness-only traits; RKJ100 mostly completeness-only and predicted/unknown.
- ANSWER_TEXT / ANSWER：answer fills 8 traits, leaves 7 null, and labels genus-level values medium/low with internal evidence.

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Decision-relevant route/enzyme/microbe claims rely only on INTERNAL_KNOWLEDGE_ONLY or MODEL_INFERENCE; no locatable database entries/DOIs are delivered, and EVID_001 is a literature memory not opened. Under D5 this is MISSING_SOURCE low band; the structured evidence registry and specific citation memory justify 3 rather than 1-2. E0 gap prevents verified mis-citation or cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：evidence_registry entries are INTERNAL_KNOWLEDGE_ONLY/MODEL_INFERENCE; EVID_001 cites a paper by memory but no DOI/page and says not opened.
- RUBRIC_CLAUSE / P34：INTERNAL_KNOWLEDGE_ONLY is MISSING_SOURCE, low band, not a verified mis-citation.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer&#x27;s uncertainties and confidence labels clearly distinguish internal knowledge, model inference, low-confidence downstream inference, honest nulls, route I/II mapping risk, taxonomy reclassification risk, and stoichiometric limitations. There is some overconfidence in medium labels for internal claims, but not systemic. 7-8 band, upper 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：uncertainties section lists route-number risk, missing EC/enzymes, downstream inference, null traits, and reclassification disclaimer; evidence_registry marks internal/model inference.

</details>

## GPT5.6

答案SHA256：`8836be04e0473ae2c75e9287c35a87406f88a30411b4868d5d84008717175e1a`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定路线为2-nitrobenzoate degradation II，冻结任务合同要求3个必答步（S02 2-nitrobenzoate→2-hydroxylaminobenzoate；S03→anthranilate；S01 anthranilate→catechol+CO2+NH4），终点为Catechol。答案只给两步：S1直接把2-Nitrobenzoate写成2-Aminobenzoate，S2把2-Aminobenzoate写成2-Aminomuconate semialdehyde，未给S03、S01及终点catechol；按逐目标映射仅S02有候选步且为SUBSTITUTION_SUSPECTED_IDENTITY_UNRESOLVED，S01/S03缺失。酶/菌/15项性状字段有涉及，故非完全不可辨认，但核心主链大部缺失且明显偏离指定路线，D1关键错误成立，落1–2档取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：支持锁定主链S02→S03→S01的底物/产物及S01产物为catechol+CO2+NH4；不证明答案两步的具体酶或菌活性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_014：支持本题为LINEAR_UNIQUE、ordered_step_count=3；不表示答案已交付全部3步。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_014：支持路线名2-nitrobenzoate degradation II及terminal_compound_names=Catechol。
- ANSWER_TEXT / ANSWER_TEXT：支持答案实际只交付两步且终点为2-Aminomuconate semialdehyde而非Catechol。
- SCOPE_ROW / SCOPE#BIOPATH150_014#CG04：题面氧条件aerobic为任务条件；答案declared aerobic不替代主链交付。

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2按所答化学与目标主链评价。S1将2-nitrobenzoate直接写成2-aminobenzoate，跳过冻结主链的2-hydroxylaminobenzoate中间体；S2以anthranilate 1,2-dioxygenase将anthranilate转为2-aminomuconate semialdehyde，而冻结S01 accepted反应为anthranilate→catechol+CO2+NH4，终点catechol缺失。两步概念上有硝基还原与芳环开环痕迹，但关键中间体、核心开环产物和终点均与指定主链不符，构成主链核心转化错误/严重断裂，D2关键错误成立，落3–4档取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：支持S02产物2-hydroxylaminobenzoate、S03产物anthranilate、S01产物catechol+CO2+NH4；不证明具体蛋白底物谱。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_014：支持S01 accepted酶名为anthranilate dioxygenase、EC 1.14.12.1；不证明答案所称具体蛋白活性。
- ANSWER_TEXT / ANSWER_TEXT：支持答案写S1产物2-Aminobenzoate、S2产物2-Aminomuconate semialdehyde及S2酶名anthranilate 1,2-dioxygenase。
- SCOPE_ROW / SCOPE#BIOPATH150_014#CG04：题面aerobic为任务条件；不对答案内部化学正确性作背书。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Allowed range &#91;1,8&#93;. The delivered two steps do not supply the three target reactions: the entry target product is 2-hydroxylaminobenzoate but the answer gives 2-aminobenzoate; the terminal target is catechol but the answer gives 2-aminomuconate semialdehyde; the S03 hydroxylaminobenzoate-reductase step is absent. No target step reaches S; substrate and some enzyme names remain usable, so the low band is 2 rather than 1.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_014：Defines target products for S02 and S01 and the three-step direction; not a general proof about all possible alternative routes.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_014：Gives accepted enzyme names/EC context for the target steps; does not certify specific protein activity.

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer uses Pseudomonas putida KT2440 (TaxID 160488) for both steps and as complete_pathway_organism_profile_id, but supplies only MODEL_INFERENCE evidence and no step-level or whole-path capability record. The named strain is a plausible aromatic-degrader candidate, yet target-step attribution and whole-path capability remain unverified; 5-6 band, low end.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_014：Gold lists other organisms for these target steps; absence does not prove P. putida KT2440 incapable, but it does not support the answer&#x27;s strain attribution.

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The profile supplies all 15 trait fields, with 7 filled and 8 explicit unknown. The filled values are broad (aerobic, Gram-negative, aromatic-degradation capacity, oxygen acceptor) and plausible in outline, but have no locatable source and no numeric values are fabricated. This is partial applicable content with key evidence gaps; 5-6 band, low end.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_014：No P. putida KT2440 trait rows are present in this slice; absence does not contradict the answer but cannot verify the filled traits.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All evidence_registry rows are MODEL_INFERENCE with null database, record_id and locator. Internal evidence IDs map claims but do not provide locatable literature/database/computational records. This is MISSING_SOURCE for decision-relevant groups, not a verified mis-citation; traceability is near-absent, so 1-2 band, upper end.

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer generally labels its evidence as low confidence, uses explicit nulls for unknown traits, and lists uncertainties for missing EC numbers, strain-level evidence and downstream steps. It does not systematically present inference as observation. Some route/organism assertions remain stronger than the model-inference source, so 7-8 band, lower end.
