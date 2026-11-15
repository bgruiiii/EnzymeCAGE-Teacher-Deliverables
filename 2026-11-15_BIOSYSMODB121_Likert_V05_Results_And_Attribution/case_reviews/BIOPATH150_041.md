# BIOPATH150_041：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：propanoyl CoA degradation I

污染物：succinyl-CoA；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 44 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 39 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 52.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 44 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 50 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 28.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`27a690d99f29733a0d447062939b38d4c1cfc9c37006643a44db59c921d2634f`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案结构完整，steps、enzyme、microorganism、15项性状与evidence_registry均有交付，三目标步模块也未整体缺失；但主链按 propanoyl-CoA→succinyl-CoA 方向组织，未按题面污染物 succinyl-CoA 的降解主链方向交付，任务符合度受实质影响，故在5–6档取低分5。D1不将方向反转另判为本维key_error，方向科学问题归D2独立评价。

<details><summary>V0.4理由与本行变化背景</summary>

六个模块均实质交付：三步主链（底物/产物/SMILES）、每步酶与EC、1个对应菌、15项性状、3条证据、不确定性说明，route_scope.chosen_route_name与题面一致，格式完整。但主链自 propanoyl-CoA 起、止于 succinyl-CoA，题面要求的&#x27;污染物 succinyl-CoA 的降解&#x27;方向未在完整性层面得到实质对应；该方向问题的化学判据在D2另判，D1仅按任务符合度/范围偏离档内扣分。按5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：本题污染源为 succinyl-CoA，gold 终点主产物为 propanoyl-CoA 与 bicarbonate，支持任务降解方向应由 succinyl-CoA 向 propanoyl-CoA；不证明答案反向链符合任务。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：S03/S02/S01 的 directed rows 显示任务主链为 succinyl-CoA→(R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate；用于核对主链方向，不将答案反向链当作任务完成。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_041：线段为 LINEAR_UNIQUE、ordered_step_count=3，可支持本题主链长度为3步及模块完整性的分母；不表示反向顺序可接受。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> gold定向步骤为 succinyl-CoA→(R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate；答案给出的是完全相反的 propanoyl-CoA→(S)-methylmalonyl-CoA→(R)-methylmalonyl-CoA→succinyl-CoA。三步转化化学本身可辨认且辅因子有列，但相对题面降解主链整体方向反转，属于D2关键错误“反应方向反转”，cap≤4；因方向错误覆盖全主链，取3而非上限4。

<details><summary>V0.4理由与本行变化背景</summary>

答案为 propanoyl-CoA→(S)-methylmalonyl-CoA→(R)-methylmalonyl-CoA→succinyl-CoA，与题面污染物 succinyl-CoA 的降解方向相反（冻结gold：root=succinyl-CoA、terminal=propanoyl-CoA+bicarbonate，三步顺序 S03→S02→S01）。&#x27;反应方向反转&#x27;属八.R2关键错误，cap≤4；但逐步化学（羧化/差向异构/B12依赖骨架重排）正确、ATP/CO2/ADP/Pi辅因子与主副产物分列清楚，档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：root_compound=succinyl-CoA，terminal_compound=propanoyl-CoA|Bicarbonate，支持任务主链从 succinyl-CoA 向 propanoyl-CoA/bicarbonate 降解。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：S03 directed row: succinyl-CoA→(R)-methylmalonyl-CoA；S02: (R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA；S01: (S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate。直接支持答案方向相反。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：S01–S03 accepted enzyme/EC sets支持相应酶功能与编号粒度，但不支持把反向顺序作为本题主链方向。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分8 → V0.5新分2，变化-6。

新裁判理由：

> 目标主链方向整体反向。gold/题面任务方向为 succinyl-CoA → (R)-methylmalonyl-CoA → (S)-methylmalonyl-CoA → propanoyl-CoA + bicarbonate（S03→S02→S01），而原答案给出 propanoyl-CoA → (S)-methylmalonyl-CoA → (R)-methylmalonyl-CoA → succinyl-CoA（S1→S3），并在 uncertainties 中明确把 succinyl-CoA 当作末端产物。三个目标反应的酶名/EC 基本对应（6.4.1.3、5.1.99.1、5.4.99.2），但每一步均按相反方向交付，不能算目标步完成；核心主推荐失效。正确 EC/名称仅构成局部可用信息，故在&#91;1,2&#93;内取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶-反应对应良好：EC 6.4.1.3（生物素依赖羧化）、EC 5.1.99.1（差向异构）、EC 5.4.99.2（B12依赖重排）与gold enzyme_gold三步EC逐一一致，酶名与反应类型相符；基因/蛋白仅mutA/mutB并注明凭记忆。按7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：支持gold有向主链为 succinyl-CoA → (R)-methylmalonyl-CoA → (S)-methylmalonyl-CoA → propanoyl-CoA + bicarbonate；不支持答案的反向链作为目标完成。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：支持答案三步的酶名/EC与accepted集合基本对应，但这些局部身份不能把反方向步骤升为目标完成。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：支持从污染物 succinyl-CoA 出发、到 propanoyl-CoA/bicarbonate 的任务方向；答案把起点终点对调。
- RUBRIC_CLAUSE / C00：要求按有向任务评价；不能因甲基丙二酰-CoA 变位酶/差向异构酶可逆而把反方向链算作目标完成。
- RUBRIC_CLAUSE / C03：支持把三个反方向目标步登记为F而非S或单纯U。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案给出单一微生物Mycobacterium tuberculosis H37Rv（TaxID 83332）并声称其完成三步；身份候选合理、菌株明确，但全路径能力、TaxID/基因组/保藏号均无E0冻结记录，且gold受试菌列表不含Mtb（gold非穷尽，不能据此判错）。按“合理候选但关键身份/作用范围未充分核验”取5分。

<details><summary>V0.4理由与本行变化背景</summary>

以单一菌 Mycobacterium tuberculosis H37Rv（TaxID 83332）承担三步；该物种具备甲基丙二酰-CoA通路的候选合理、无证据反驳，但菌株级完整路径能力仅由记忆型文献EVID_002支撑、TaxID 83332无冻结记录，身份与能力属部分支持。按5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_041：Gold列出的STEP菌为Cereibacter sphaeroides、Propionibacterium freudenreichii、Escherichia coli；gold非穷尽，不能证明M. tuberculosis H37Rv无能力。
- ANSWER_TEXT / ANSWER#BIOPATH150_041：答案声称M. tuberculosis H37Rv可完成propanoyl-CoA→succinyl-CoA三步，并给出EVID_002文献记忆性来源。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 原答案给出 M. tuberculosis H37Rv（taxid 83332）完整15项性状；身份与多项基本性状（ATCC 27294、NC_000962、约4.41 Mb/65.6% GC、革兰氏阳性/抗酸、杆状、无运动、不产孢、好氧等）与常见知识一致，且未知项如盐度/pH以null保留。但冻结trait切片仅覆盖1063/1744/562，没有taxid 83332的官方性状记录；答案几乎全部性状引用EVID_003 INTERNAL_KNOWLEDGE_ONLY且raw_text为null，菌种保藏号、基因组精确数值和酶活等关键项缺独立核验。因此主要性状大体适用，但关键证据不足，不能进入7–8档；按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐备（13项填写、F3/F4两项如实null），数值/单位/结构与所指菌株相符（最适37℃、ATCC 27294、NC_000962/4,411,532 bp/GC 65.6%、革兰氏阳性抗酸、无运动、不产孢等），F15栖息地描述符合&#x27;非广适&#x27;含义；但全部以EVID_003内部知识标注且多项标high，E0无该菌性状记录，真值待核。按7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：显示原答案提供了15项性状，但多数高/中置信度数值没有可定位原始来源，属于内部知识声称而非外部核验。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_041：支持本案冻结trait切片没有 M. tuberculosis/taxid 83332 的官方性状行；不能据此核验 ORG_001 的菌种保藏号、基因组数值和酶活。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_041：支持 taxid 83332 在本切片中无性状可评分记录，D4应保留证据不足限制而非按填满率给高分。
- RUBRIC_CLAUSE / C06：支持对大体适用但关键项未独立核验的性状集取5–6档而非7–8档。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案交付了evidence_registry并逐项挂接evidence_id，但决策相关组来源普遍笼统或缺失：EVID_001为无record_id的MetaCyc pathway页面（GENERIC）；EVID_002为自述凭记忆、未核验的文献（UNRESOLVED）；EVID_003为INTERNAL_KNOWLEDGE_ONLY（MISSING），覆盖多数性状/身份/基因组。核心酶EC可在gold enzyme_gold得到G4接受事实，但答案自身来源仍非条目级；E0无法核验，不能判已核实错引。按3-4档“仅笼统来源/主要模块缺映射”取4。

<details><summary>V0.4理由与本行变化背景</summary>

证据注册3条：EVID_001仅MetaCyc pathway页名、无record_id（笼统）；EVID_002为记忆型文献自由文本、不可解析；EVID_003为INTERNAL_KNOWLEDGE_ONLY。决策相关组（CG01/02/03/05为GENERIC_SOURCE；CG07/08/09为UNRESOLVED_SOURCE；CG17为MISSING_SOURCE）无任何条目级可定位可核对结论，按P41落3–4档取4；E0整题GAP，无已核实错引，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_041：EVID_001无record_id；EVID_002自述记忆未核；EVID_003为内部知识；多数traits指向EVID_003。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：仅支持S01/S02/S03的accepted EC/酶名G4事实，不使答案自身来源升级为条目级可核记录。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案在uncertainties、notes与各step.uncertainty中较具体地区分记忆性文献、内部知识、SMILES立体未标注、基因座位未核实与null；主要限制和方向边界有披露。问题在于部分高置信标签用于EVID_003内部知识或未核EC/性状，存在局部过度确信，但未达到系统性把预测写成实证或掩盖矛盾。按7-8档“大部分证据性质/限制已标注，少量问题”取7。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体：注明SMILES未标立体中心、mutA/mutB凭记忆、MetaCyc record ID/基因座/精确基因组大小未核，并说明污染物为路线末端产物的范围边界，符合&#x27;区分已知/推断/未知&#x27;。但多项内部知识性状标high、Mtb全路径能力以&#x27;文献记载&#x27;陈述且来源不可核，存在轻度过度确信。按7档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_041：答案明确写出succinyl-CoA为末端产物、SMILES未标立体、文献记忆未核、基因与部分数值留null。

</details>

## DeepSeek

答案SHA256：`bbe770029a8e29adfc8acc453660ef1d28447191129022c717390366e905ef23`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> JSON结构完整，3个主链步骤均给出enzyme/EC与microorganism，route_scope.chosen_route_name也按要求原样填写；但所有底物/产物的SMILES均为null，15项性状全部value=null、evidence_id=null、confidence=unknown，任务要求的SMILES与性状实质内容缺失。明确未知可减轻但不能等同于已完成，属主要模块均有涉及但若干必要内容遗漏/仅占位，需实质修订，取5分。

<details><summary>V0.4理由与本行变化背景</summary>

主要模块（3步路径、每步酶与菌）均有涉及，但主链化合物SMILES全部为null、15项性状全部未交付（仅null/unknown）、菌株未指定；属必要内容多处遗漏，按5–6档取低端5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / P15：明确未知体现信息不足，不能与遗漏或错误等同；但D1完成度仍按实际填写/未知记录反映。
- RUBRIC_CLAUSE / P45：诚实填写未知/null：D1反映完成度不足。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_041：本题冻结gold ordered_step_count=3，题面要求主链步级交付。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 主碳骨架与整体方向（succinyl-CoA→propanoyl-CoA）成立，但关键中间体立体化学与末端转化需实质修订：gold为succinyl-CoA→(R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate，S01为propionyl-CoA carboxylase EC 6.4.1.3反向；答案写L-methylmalonyl-CoA→D-methylmalonyl-CoA，并用EC 4.1.1.41脱羧生成CO2。按C06，显式立体冲突候选≤5；虽然脱羧替换本身可化学成立，但核心中间体与末端酶/产物组合未与指定主链可靠对齐，取5分。

<details><summary>V0.4理由与本行变化背景</summary>

三步主链化学与gold方向一致：succinyl-CoA→甲基丙二酰-CoA→差向异构化为另一甲基丙二酰-CoA→脱羧/羧化反向生成propanoyl-CoA，碳架与脱羧计量成立。辅因子（B12、ATP/ADP/Pi等）未列属局部计量缺陷，按7–8档取8；无关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：gold步级方向显示S03 succinyl-CoA→(R)-methylmalonyl-CoA、S02 (R)→(S)-methylmalonyl-CoA、S01 (S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate；答案使用L/D并接EC 4.1.1.41脱羧，关键中间体/末端转化需修订。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：gold S01 accepted enzyme为propionyl-CoA carboxylase EC 6.4.1.3，而非EC 4.1.1.41；用于D2化学比较，不代替D3a判定。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：gold terminal主产物为Bicarbonate|propanoyl-CoA；答案末端主产物为propanoyl-CoA+CO2 byproduct。
- RUBRIC_CLAUSE / C06：D2显式立体冲突候选≤5；化学可成立替换候选≤6。

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案的 S1/S2 使用 methylmalonyl-CoA mutase EC 5.4.99.2 与 methylmalonyl-CoA epimerase EC 5.1.99.1，分别与 accepted S03/S02 的酶身份对应；但 S3 使用 methylmalonyl-CoA decarboxylase EC 4.1.1.41，将 D-methylmalonyl-CoA 转为 propanoyl-CoA + CO2，而 accepted KEY_TERMINAL S01 要求 propionyl-CoA carboxylase alpha/beta EC 6.4.1.3 作用于 (S)-methylmalonyl-CoA 生成 propanoyl-CoA + bicarbonate。末端关键目标未按指定反应完成，应受 KEY4 上界约束；中间体 L/D 与 gold R/S 顺序也不完全一致，故只能给受限上沿 4。

<details><summary>V0.4理由与本行变化背景</summary>

酶名与EC类别内部一致；5.4.99.2变位酶、5.1.99.1差向异构酶与gold酶表吻合；第三步用4.1.1.41甲基丙二酰-CoA脱羧酶，gold对应步骤为6.4.1.3丙酰-CoA羧化酶反向，属未核替代/不同酶选择。E0无EC记录，关键步骤仍缺具体核验，按5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：确认 accepted EC：S01 为 6.4.1.3，S02 为 5.1.99.1，S03 为 5.4.99.2；S01 未列 EC 4.1.1.41
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：确认目标方向/结构：S03 succinyl-CoA -&gt; (R)-methylmalonyl-CoA；S02 (R) -&gt; (S)；S01 (S)-methylmalonyl-CoA -&gt; propanoyl-CoA + bicarbonate；答案末端用 decarboxylase/CO2，且 L/D 顺序不同
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_041：确认本题为三步线性主链，不能把旁支或替代路线回填为目标步骤

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 7-8 band at lower edge: Propionibacterium freudenreichii TaxID 1744 matches gold organism rows exactly and PATHWAY_COMPLETE is TRUE, supporting species-level identity and whole-path capability. No strain is given and no step-specific strain-level capability evidence is delivered, so lower-edge 7 rather than higher.

<details><summary>V0.4理由与本行变化背景</summary>

Propionibacterium freudenreichii/TaxID 1744与gold organism_gold一致，gold PATHWAY_COMPLETE=TRUE支持物种级完整路径；未给菌株，属物种级身份。S01步级在gold另有Cereibacter记录，但pathway_complete不推翻该物种推荐。E0无TaxID官方记录、来源仅内部知识，按7–8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_041：Exact species name and TaxID 1744 with PATHWAY_COMPLETE TRUE; supports species-level identity and whole-path capability, not strain-level identity or specific step enzyme activity.
- ANSWER_TEXT / ANSWER：Answer claims Propionibacterium freudenreichii, strain null, TaxID 1744, and reuses ORG_001 for all steps.

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> All 15 required traits are present as fields but every value is null with confidence unknown; no evaluable trait content is delivered. Per P44 this is D4 MISSING=1, not a claim of detected scientific error.

<details><summary>V0.4理由与本行变化背景</summary>

organism_profiles&#91;0&#93;.traits的F1–F15全部value=null、confidence=unknown，未交付任何性状；按P44全部必需性状null→D4 MISSING=1，不宣称检测到科学错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：All 15 traits are null/unknown; no evaluable trait values were delivered.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 1-2 band: all key conclusions rely on INTERNAL_KNOWLEDGE_ONLY evidence_registry entries with null database, record_id, and locator; no locatable external sources are delivered. No verified mis-citation is established, so no cap applies.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry三条均为INTERNAL_KNOWLEDGE_ONLY，无database、record_id、locator；全部关键结论无法定位到外部条目。按四.3 MISSING_SOURCE低分档（1–2）取2；无已核实错引，默认不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Only internal-knowledge labels are provided; no database entry, stable locator, or external record is delivered.

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 5-6 band at lower edge: the answer lists a few unknowns and marks all traits unknown, but enzyme steps carry high confidence while grounded only in INTERNAL_KNOWLEDGE_ONLY evidence; evidence type and support scope are not clearly separated, so some conclusions exceed the stated basis. Not systemic misleading evidence.

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties列出SMILES未提供、菌株未指定、氧条件未指定，且15项性状标unknown，属有不确定性说明；但酶confidence=high与INTERNAL_KNOWLEDGE_ONLY来源不相称，未披露EC/TaxID未核及第三步酶替代/辅因子差异，说明偏笼统、部分结论强度超过依据。按5–6档取6，非系统性误导，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows partial uncertainty disclosure, but high-confidence enzyme claims are not tied to locatable evidence or explicit evidence-type limits.

</details>

## Kimi

答案SHA256：`78a18dd0aee0880dc4f288651fe40dbd8d54df7730f19fcf35e453ff7699da95`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> 结构上覆盖3步、酶、微生物与15项性状，但题面要求的是succinyl-CoA在propanoyl CoA degradation I下向propanoyl-CoA/bicarbonate的降解；答案把主链写成propanoyl-CoA -&gt; succinyl-CoA，并把succinyl-CoA作为末端产物，主任务方向反了。给3：模块齐全与可读性保留，但任务符合度核心失败。

<details><summary>V0.4理由与本行变化背景</summary>

六类输出模块均实质交付：三步主链（英文名+SMILES双端、每步一酶一EC、每步一菌且按物种+菌株去重）、两条菌株profile各15项性状、证据登记、不确定性说明；chosen_route_name原样回填，氧条件按null处理，格式完整。扣分点：题面要求‘所述物质(succinyl-CoA)的降解主链’，答案却以propanoyl-CoA为首步底物、把succinyl-CoA放在末步产物位置，属任务范围/方向层面的偏离（答案已在route_scope.notes与S3.uncertainty主动声明），不构成模块缺失。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：固化gold根为succinyl-CoA，终产物为Bicarbonate|propanoyl-CoA；仅支持题面主链方向与终点，不证明全部替代路线不存在。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：用于核对S03-&gt;S02-&gt;S01的有向主链；不支持把反向发酵路线算作题面降解完成。
- ANSWER_TEXT / ANSWER.steps：答案实际逐步方向为propanoyl-CoA羧化生成succinyl-CoA，不是succinyl-CoA起始降解。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 三步反应在反向/可逆意义上可写出，辅因子和连续性较清楚；但与题面有向主链相反：答案从propanoyl-CoA走到succinyl-CoA，且S02用(S)-&gt;(R)甲基丙二酰-CoA，与gold任务方向(R)-&gt;(S)不符。方向冲突属D2关键错误，cap后给4：化学表达较完整，但方向/终点核心失效。

<details><summary>V0.4理由与本行变化背景</summary>

三步化学本身正确且连续：S1丙酰-CoA羧化（ATP+碳酸氢盐→ADP+磷酸，生物素依赖酰基-CoA羧化酶）、S2甲基丙二酰-CoA差向异构（S→R）、S3腺苷钴胺依赖变位生成succinyl-CoA；方向、原子与主链连接无跳跃，反应节点（propanoyl-CoA→(S)-甲基丙二酰-CoA→(R)-甲基丙二酰-CoA→succinyl-CoA）与gold三步反应（BSY-r01768/r03821/r03869）的化学一一对应，辅因子在列且计量交代清楚。局部问题：整条链按‘propanoyl-CoA→succinyl-CoA’书写（即题面污染物的生成方向），与题面‘所述物质降解主链’及gold根/终点口径相反；答案已在route_scope与S3.uncertainty明确声明succinyl-CoA是该路线末端产物，属已声明的方向处置，不按未声明偏离处理、不触发cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：支持S03 succinyl-CoA -&gt; (R)-methylmalonyl-CoA、S02 (R)-&gt;(S)、S01 (S)-methylmalonyl-CoA -&gt; propanoyl-CoA/bicarbonate的有向关系；不证明反向酶学不可能。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：支持题面终点为propanoyl-CoA/bicarbonate；不用于排除所有反向发酵化学。
- ANSWER_TEXT / ANSWER.steps：答案实际方向与gold有向步骤相反，且S02的R/S方向不符。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分9 → V0.5新分2，变化-7。

新裁判理由：

> 本题要求从琥珀酰-CoA 出发沿 propanoyl CoA degradation I 主链到 propanoyl-CoA + bicarbonate；gold 方向为 succinyl-CoA→(R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate。答案给出的是完全反向的链：propanoyl-CoA→(S)-methylmalonyl-CoA→(R)-methylmalonyl-CoA→succinyl-CoA。三个目标酶的酶名/EC虽与 accepted 集合对应，但均在反向方程中使用，未完成所需方向的目标反应；只有局部正确酶身份可资利用，核心目标主推荐失效，故为2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶-反应对应正确且与gold酶条目逐条一致：S1 propionyl-CoA carboxylase EC 6.4.1.3（α/β亚基，accA1/pccB）、S2 methylmalonyl-CoA epimerase EC 5.1.99.1、S3 methylmalonyl-CoA mutase EC 5.4.99.2；酶名、EC大类与反应类型（羧化/差向异构/B12变位）互不矛盾，作用范围限定到具体步骤，未见把家族相关性当催化证据。仅因E0无法核对EC accepted name/reaction与条目状态，登记局部待核，不降档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：支持本题主链应从 succinyl-CoA 起始并以 Bicarbonate/propanoyl-CoA 为终点；不支持答案的反向整链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：给出逐目标反应的有向底物/产物方向；答案三步均为相反方向。不单独证明具体蛋白实验活性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：支持答案的酶名/EC与 accepted 目标酶对应；不支持反向目标反应完成。
- RUBRIC_CLAUSE / C03：用于判定反向方程不按S计而属目标方向失败。
- RUBRIC_CLAUSE / C05：用于在&#91;1,2&#93;内选择2分而非1分。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> P. freudenreichii在S2/S3与gold的物种级微生物行相符；S1用S. coelicolor A3(2) M145有具体文献指向acyl-CoA carboxylase，但E0无机器事实可核，TaxID/株级催化不能确认。未发现已核实身份矛盾；给7：主要微生物对应有合理支持，但S1与株级能力仍属局部待核。

<details><summary>V0.4理由与本行变化背景</summary>

步骤菌与gold步骤菌口径相容：S2/S3使用Propionibacterium freudenreichii subsp. shermanii CIRM-BIA1，与gold S02/S03步骤菌Propionibacterium freudenreichii（TaxID 1744）同种且该物种属gold PATHWAY_COMPLETE集合；S1使用Streptomyces coelicolor A3(2) M145（TaxID 100226），gold该步虽登记Cereibacter sphaeroides，但gold非穷尽，替代菌不因与gold不同判错。身份层级处理基本清楚：菌名/菌株/保藏号一致，CIRM-BIA1的TaxID诚实留null；S1菌的羧化酶归属有具体文献指向。扣分点：S2/S3的菌株级反应能力由经典P. shermanii研究外推（属身份阶梯①粒度不足，档内扣分不cap），答案已明确披露；S. coelicolor属未经gold覆盖的替代菌，本快照无法核其反应级证据。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_041：支持P. freudenreichii出现在S2/S3的gold微生物行，及C. sphaeroides等替代对应；不证明S. coelicolor不能作为替代菌。
- ANSWER_TEXT / ANSWER.evidence_registry：答案交付EVID_003/EVID_007等来源映射；支持其可追溯性声称，不自动证明株级实验活性。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> P. freudenreichii的F10无运动性、F12革兰氏阳性、F13不产孢及F14基因组大小/GC等与gold冻结性状一致或相容；S. coelicolor性状多数为常见物种描述但无gold/E0条目可核。温度项以培养温度写optimum_c并标low，存在条件解释风险但已标注。给7：主要性状有支持，局部待核与条件解释需修订。

<details><summary>V0.4理由与本行变化背景</summary>

两条profile的15项性状齐备，明确未知用null（pH、盐度、ORG_001保藏号）而非编造；可与本地物种级记录比对的关键性状一致：P. freudenreichii（1744）革兰氏阳性、不产孢、无运动性、杆状与trait_gold物种级观测吻合，F14（FN806773，2,616,384 bp，67.3% G+C）落在gold物种级区间（1.2–2.7 Mb、66.6–67.6%）内且与所引基因组文献数值自洽；ORG_001的F14（NC_003888，8,667,507 bp，72.1%）为A3(2)标准基因组值。扣分点：ORG_001 F2以‘常规培养30°C’填optimum_c=30，属培养温度≠最适温度的误读（P52/P113）；若干性状（F7/F8/F9/F15）依赖代表记录或定性推断、raw_text缺失；S. coelicolor各性状在本地无官方记录，无法核验；温度min/max按scoreability mask为pending_teacher_adjudication，答案留null属诚实。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_041：支持P. freudenreichii的F10=false、F12=true、F13=false及F14基因组统计范围；不支持外推到未列出的S. coelicolor性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_041：给出P. freudenreichii与S. coelicolor各性状的可评分/complete-only状态；不把无观测项当错误。
- ANSWER_TEXT / ANSWER.traits：答案实际交付15项/株，并给部分性状raw_text与confidence；用于D4档位判断。

</details>

### D5 来源与可核查性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案给EVID_001-EVID_008并将route、酶/EC、微生物、性状与部分genome/evidence字段映射到具体KEGG模块、文献或内部知识；结构上可追溯。EVID_002缺record_id、EVID_004书目较旧/不完整、EVID_008为内部知识，且E0为EVIDENCE_GAP，不能机器核验引用内容；按未核不判错引，给7：大部分关键结论有可定位交付记录，少量记录不完整。

<details><summary>V0.4理由与本行变化背景</summary>

来源结构完整：每条反应、酶、菌与大部分性状均绑定evidence_id；EVID_001为KEGG模块M00741的条目级记录，EVID_003–EVID_007为含作者/年/刊/卷期页的可定位文献，EVID_006/EVID_007与其所支撑的基因组/身份声称对应关系清楚，属于决策相关组存在条目级可定位结论，落入5–6档。未达7–8档的原因：统一冻结证据为EVIDENCE_GAP（entries=0），引用内容是否实际支持claim_scope无法核对，相关组统一登记UNRESOLVED_SOURCE；另有EVID_002（MetaCyc，record_id=null）与EVID_004（书目仅‘1960s’，缺卷期页）为笼统来源，ORG_001温度/运动性仅INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）。全部为未核或缺失，无任何已核实错引→不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：列出答案实际交付的来源ID、数据库/文献定位与claim_scope；不证明这些来源内容已被E0核验。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：仅用于比对酶/EC记录定位；不作为D5已核实错引或不支持结论的证据。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案有route_scope.notes、逐步uncertainty、confidence与uncertainties数组，明确区分未知、文献外推与株级未实测；EVID_008内部知识也标low。主要问题是仍以high/medium包装部分未机器核验的文献与菌株能力，但整体披露具体，不是系统性把预测写成实证。给8。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界披露具体且与依据大体相称：uncertainties列出MetaCyc pathway ID未确认、S2/S3酶学来自经典P. shermanii非CIRM-BIA1实测、株TaxID不确定、氧条件未指定及丙酸发酵中路线反向运行；逐步骤uncertainty字段说明机制性书写与路线终点；明确未知用null（pH、盐度、TaxID、保藏号）；预测/外推处（株归属、ORG_002低置信性状）标注low/medium。未见系统性把预测当实证、未见掩盖主要矛盾。扣分点：ORG_001 F2把培养温度写成optimum且仍给数值；ORG_001部分性状（F11/F12/F13）标high但本地无记录可核；属单点/局部强度偏高，非系统性误导。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案主动披露MetaCyc ID未确认、P. shermanii株级外推、TaxID null及氧条件未指定；支持D6披露质量判断。

</details>

## Qwen

答案SHA256：`8f430e8edf06ecea42acd22845da2d7e98764a0660ebd9cdee6d256fb0322309`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案覆盖路径、酶、微生物、15项性状、来源与不确定性等模块，但主链方向反转：题面污染物为succinyl-CoA，gold要求succinyl-CoA→propanoyl-CoA+bicarbonate，答案却从propanoyl-CoA生成succinyl-CoA并续到succinate。属D1任务路线/方向偏离关键错误，按C06候选≤4；因其余交付模块较完整，取4。

<details><summary>V0.4理由与本行变化背景</summary>

路径、酶、微生物、性状、来源、不确定性六模块均有实质交付，steps逐项给出底物/产物/SMILES、酶+EC、对应微生物，15项性状全部出现（11项有值、4项明确unknown/null），关联清楚。但主链入口为propanoyl-CoA，题面污染物succinyl-CoA仅在S3作为产物出现、S4才被消耗，与“降解succinyl-CoA”存在实质范围偏离；该方向张力属题面路线名与污染物之间的冲突，登记review_queue，不据此单独判关键错误。主要模块均在、仅入口/方向与性状完整性需实质修订，判5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：gold定向步骤显示succinyl-CoA→(R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate；不支持答案的反向主链作为目标完成。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：该题root为succinyl-CoA、terminal main products为Bicarbonate|propanoyl-CoA；仅支持任务边界，不支持反向路线。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 答案所用三个核心酶/EC与gold步骤名称层面相符，但把gold主链整体反向：propanoyl-CoA→(S)-methylmalonyl-CoA→(R)-methylmalonyl-CoA→succinyl-CoA，并额外到succinate；而任务要求succinyl-CoA→propanoyl-CoA+bicarbonate。方向冲突贯穿全部必答步骤，属D2方向反转关键错误，按C06≤4；因所有核心步骤均反向，取3。

<details><summary>V0.4理由与本行变化背景</summary>

S1羧化（propanoyl-CoA→(S)-methylmalonyl-CoA）、S2差向异构（(S)→(R)-methylmalonyl-CoA）、S3变位（(R)-methylmalonyl-CoA→succinyl-CoA）三步化学转化正确，酶/EC与gold enzyme_gold的S01–S03完全对应，链连接连续；S4 succinyl-CoA→succinate为真实中心代谢步骤但不在gold路线内，答案自述低置信。主要限制是整条主链取丙酰-CoA→琥珀酰-CoA的正向（生物合成）方向，与题面要求降解succinyl-CoA及gold方向相反，主链首步不是succinyl-CoA的转化；该方向张力属题面/gold冲突，按四.5四步判断登记而非直接cap。化学本身成立、方向/入口需实质修订，判5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：gold定向行支持succinyl-CoA→(R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate；不支持将反向往succinyl-CoA的路线作为目标主链。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分8 → V0.5新分1，变化-7。

新裁判理由：

> 题面与gold定向为succinyl-CoA经S03→S02→S01生成propanoyl-CoA与bicarbonate；答案的route_summary及S1–S3整体反向：propanoyl-CoA→(S)-methylmalonyl-CoA→(R)-methylmalonyl-CoA→succinyl-CoA，并把succinyl-CoA进一步转为succinate。三个必答目标均按反向路线交付，属于已核方向错误，全部为F，无目标S。虽然酶名/EC与accepted集合一致，但化学可逆不取消有向任务，错误路线的酶自洽不能增加目标信用；全F且无正确方向目标完成，主推荐失效，取&#91;1,2&#93;下沿1。

<details><summary>V0.4理由与本行变化背景</summary>

S1 propionyl-CoA carboxylase（EC 6.4.1.3）、S2 methylmalonyl-CoA epimerase（EC 5.1.99.1）、S3 methylmalonyl-CoA mutase（EC 5.4.99.2）与gold enzyme_gold的酶名/EC逐条对应，功能与反应类型一致；S4 succinyl-CoA synthetase（EC 6.2.1.5）为真实中心代谢酶但不在gold路线内，答案已标low置信。gene_or_protein均为null，题面只要求酶+EC，不构成D3a缺陷。关键步骤酶对应有可靠支持，仅S4与身份细节需进一步确认，判7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：显示gold方向为succinyl-CoA→(R)-methylmalonyl-CoA（S03）、(R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA（S02）、(S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate（S01）；不支持答案的反向顺序。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：题面根物为succinyl-CoA，终端主产物为Bicarbonate|propanoyl-CoA；支持降解方向为succinyl-CoA至propanoyl-CoA，而非propanoyl-CoA至succinyl-CoA。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：accepted酶名/EC可用于这些目标反应，但不证明反向路线完成目标，也不改变方向性任务要求。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_041：本题为单一线性三步必答链，不能用另选分支或反向解释替代目标主链。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案使用Propionibacterium freudenreichii并声明为complete_pathway profile；gold物种级/ pathway-complete行支持P. freudenreichii（taxid 1744）具完整路径能力，但答案TaxID 1748在E0无记录，且S01的菌-步归属未由gold organism行直接支持。身份/能力部分可用但关键身份字段与步级归属待核，属5–6档，取6；未核实身份错配不cap。

<details><summary>V0.4理由与本行变化背景</summary>

四步均归Propionibacterium freudenreichii（ORG_001，strain null，ncbi_taxid 1748）。gold organism_gold将该物种（taxid 1744，GCA_900087655.1）标为PATHWAY_COMPLETE=TRUE，且S02/S03步骤归属P. freudenreichii 1744，物种层面支持其可完成该甲基丙二酰-CoA路径；答案的taxid 1748在E0无冻结记录、与gold的1744不一致，属未核身份差异，不判虚构、不cap。物种名正确且路径能力有gold物种级支持，身份编号待核、strain粒度不足，判6–7档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_041：gold列出P. freudenreichii taxid 1744及PATHWAY_COMPLETE行；不验证答案taxid 1748，也不自动证明答案每一步的菌-步归属。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案返回全部15项性状，部分关键项与gold同物种记录一致或相容（mesophilic、non-motile、Gram-positive、non-spore-forming）；但F1氧耐受写aerotolerant anaerobe而gold为No robust majority，F8把途径描述当作广义降解能力，F9用methylmalonyl-CoA mutase活性作一般酶活，且多数性状仅INTERNAL_KNOWLEDGE_ONLY、E0无法核验。属部分准确但关键项证据不足/解释需修订的5–6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状与P. freudenreichii的物种级合理值基本相符：non-motile、Gram-positive、non-spore-forming、mesophilic、fermentative、dairy/fermented foods，与gold 1744的motility=false、gram positive=true、sporulation=false、temperature preference=mesophilic一致；F2仅给preference未给数值、F6末端电子受体null、F3/F4/F5/F14明确null。主要缺陷是所有性状仅标EVID_003 INTERNAL_KNOWLEDGE_ONLY、confidence low，无原始记录；taxid 1748与gold 1744不一致未核；关键项（pH/盐度/保藏/基因组）缺失。部分性状准确且适用但关键项证据不足、条件解释需修订，判5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_041：gold对P. freudenreichii taxid 1744给出部分观测/预测性状；支持若干性状核对，但不支持答案全部内部知识值，也不验证taxid 1748。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_041：标明哪些性状/子字段可评分或仅完整性；不支持把不可评分/仅预测项当作已观测事实。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 答案给出EVID_001 MetaCyc pathway级定位、EVID_002 NCBI Taxonomy record_id 1748，以及EVID_003/EVID_005 internal knowledge；路径/酶结论可部分沿pathway名定位，但无逐步记录ID，性状无外部来源，TaxID 1748在E0无记录。属部分关键结论可定位、其他模块仍缺映射的5–6档，取5；E0 gap使声称保持UNRESOLVED，不判错引、不cap。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/02/03/05/07/08/09）无一条目级可定位可核对证据：EVID_001仅给MetaCyc pathway名、record_id=null（GENERIC_SOURCE）；EVID_002的taxid 1748在E0无记录且与gold 1744不一致（UNRESOLVED_SOURCE）；EVID_003/EVID_005为INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）。SUPPORTING组同样以内部知识为主。无经核实的VERIFIED_MIS_CITATION，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION；按“全部仅有笼统来源→3–4档”取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry.EVID_001：提供MetaCyc pathway名与pathway级locator，claim_scope覆盖steps/enzymes/EC/representative organism；无record_id，不足以逐条支持全部酶-反应/菌归属。
- ANSWER_TEXT / evidence_registry.EVID_002：提供NCBI Taxonomy record_id 1748与P. freudenreichii名称；E0无该记录，TaxID 1748保持UNRESOLVED，不能确认也不能判虚构。
- ANSWER_TEXT / evidence_registry.EVID_003：性状来源为INTERNAL_KNOWLEDGE_ONLY，未交付可定位外部条目；只支持“作者知晓/推断”，不支持数据库观测。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案多处confidence为medium/low/unknown，uncertainties明确披露污染物-路线底物不匹配、SMILES简化、性状多来自内部知识；未把多数预测系统性写成实验观测。但TaxID 1748标high且complete_pathway声明边界说明不足，属单点过度确信/局部边界问题，不构成系统性误导；落7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

答案逐step给出uncertainty，证据按DATABASE_DIRECT/INTERNAL_KNOWLEDGE_ONLY分型，confidence多为low/medium，uncertainties明列题面污染物succinyl-CoA与路线常规底物propanoyl-CoA的张力、SMILES简化非立体、性状来自内部知识；S4自述可能不属于路线本体并标low置信。观测/预测/内部知识/未知有基本区分，限制与待核点具体，未系统性把内部知识包装成实证。唯route_summary与complete_pathway表述较肯定、taxid 1748未标待核，属局部过度确信而非系统性误导，判7–8档取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：答案主动披露路线底物不匹配、SMILES简化与性状内部知识限制；支持D6正面评价。
- ANSWER_TEXT / evidence_registry.EVID_002：TaxID 1748以high confidence标注；E0 gap显示该身份记录未核实，构成单点过度确信材料。

</details>

## Grok

答案SHA256：`46a6b63051fefb76f9940c4b9a85d97884a0172f5af9865d58ee9403d28adf54`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 输出格式完整，steps、enzyme、microorganism、15项性状和uncertainty均有实质交付；但主链方向与题面污染物的降解方向相反：答案明确以琥珀酰-CoA为终产物、以丙酰-CoA为起点，按D1任务偏离档与&#91;1,4&#93;范围取4，不因模块齐全抹去路线方向错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：标明root为succinyl-CoA、terminal为Bicarbonate|propanoyl-CoA；支持任务方向，不支持答案反向主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：给出主链逐步方向；支持gold方向，不支持答案的反向方向。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案三步化学在反向方向上内部连贯，但指定任务要求的是琥珀酰-CoA向丙酰-CoA/碳酸氢盐的降解方向；答案将三步全部反向，主链方向反转属于D2关键方向冲突，按&#91;1,5&#93;范围并在反向链可辨认的前提下取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：显示S01-S03的gold主底物/主产物方向；不支持答案S1-S3的反向顺序。

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三个目标步的酶名与EC均能在accepted set/酶gold中找到对应：6.4.1.3、5.1.99.1、5.4.99.2；D3a主要酶-反应对应可靠。因路线方向与立体SMILES表示仍有未决局部问题，且release上限为8、9-10不开放，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：列出各步accepted酶名与EC；仅支持酶-EC身份，不证明具体蛋白实验活性或答案反应方向。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Propionibacterium freudenreichii物种级身份和完整路径能力在organism_gold中有支持（taxid 1744，PATHWAY_COMPLETE TRUE），S02/S03也有步级关联；但答案写subsp. shermanii且无TaxID，S01步级归属没有直接步级记录。主要物种/全路径对应可靠，仅菌株粒度与个别步级归属待核，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_041：支持P. freudenreichii物种级全路径能力及S02/S03步级关联；不支持subsp. shermanii菌株级身份或S01直接步级归属。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 部分性状与gold直接相符：不运动、革兰氏阳性、杆状、不产芽孢。但若干填报项缺乏直接观测支持或与弱预测/无多数记录不符：F1耐氧厌氧、F2 optimum 30、F6延胡索酸末端受体、F7乳酸/葡萄糖/甘油、F8/F9途径酶活动与F15低栖息地广适性。按5-6档取6：有可用部分，但关键项证据不足、条件解释需修订。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_041：支持部分P. freudenreichii物种级观测性状；不支持未出现的菌株级/具体数值或把预测当观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_041：区分observed_accuracy与completeness/predicted背景；限制用预测或范围记录替代观测。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry中EVID_001-EVID_004全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；核心路线、酶、微生物、性状等决策相关组均为MISSING_SOURCE，无法沿可定位来源核查。因至少登记了局部证据ID和来源类型，未达完全空白，按D5低档&#91;1,2&#93;取2；MISSING_SOURCE默认不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示所有来源均为INTERNAL_KNOWLEDGE_ONLY且无数据库记录/定位；仅支持D5缺失来源判断。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案整体清楚标注INTERNAL_KNOWLEDGE_ONLY，列出路线方向不确定、P. freudenreichii方向性不确定、SMILES立体表示问题及TaxID/保藏号/基因组号未核；未知项多填null。减分点是部分内部知识仍标high confidence且若干性状无来源。按7-8档取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持D6对证据性质与限制披露的评价；不能回填为外部证据。

</details>

## GPT5.6

答案SHA256：`b08972cd04675976a7f3d9fb8da0e3e7f122614c2038eea5028549d09a3d8432`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面指定路线为 propanoyl CoA degradation I（succinyl-CoA→(R)-methylmalonyl-CoA→(S)-methylmalonyl-CoA→propanoyl-CoA+bicarbonate）；答案给出的是TCA片段 succinyl-CoA→succinate→fumarate→L-malate→oxaloacetate，全部三个必答目标步均未交付，属D1任务路线偏离关键错误。结构虽完整，但核心任务不符，取3–4档下沿3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_041：题面路线根为succinyl-CoA，gold终点主产物为Bicarbonate|propanoyl-CoA，不支持答案的oxaloacetate终点。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：给出本题必答三步S01-S03的目标反应与方向；不支持把答案的TCA步骤算作指定路线交付。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案四个TCA转化各自在化学上可成立，但主链不是题面指定降解路线，起始方向、中间体和终点均不匹配；同时省略ATP/ADP、CoA、醌、NAD+等辅因子。D1任务偏离另计，D2只评所答化学；按本题允许区间&#91;1,4&#93;及局部化学正确取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_041：显示指定路线目标方向与中间体；不支持答案TCA片段作为目标主链。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 目标S01-S03的accepted酶/EC分别为6.4.1.3、5.1.99.1、5.4.99.2；答案给的6.2.1.5、1.3.5.1、4.2.1.2、1.1.1.37均对应TCA步骤，不能获得目标反应信用。错误路线内部酶自洽不获D3a目标信用；按C04目标对应几乎全无，取1–2档下沿1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_041：列出指定路线S01-S03的accepted酶与EC；不支持答案TCA酶作为目标步对应。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案统一使用Escherichia coli K-12 MG1655/TaxID 511145。Gold有E. coli物种级（TaxID 562）pathway_complete及S03 step-level记录，但无该菌株级511145记录，且答案把该菌用于TCA而非目标甲基丙二酰-CoA步骤。物种候选合理、有部分支持，但菌株级身份及目标步归属/全路径能力未充分核验，取5–6档上沿6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_041：Gold有E. coli物种级pathway_complete（562）及S03 step-level记录；不支持答案所用菌株511145的菌株级全路径能力，也不支持把E. coli用于全部TCA步作为目标路线对应。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> answer的15项性状全部为null或子字段null、confidence=unknown，未提供任何可评价的性状数值、条件或来源。按P44，全部必需性状均为null/空值时D4作MISSING=1，不宣称检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_041：显示gold参考菌株存在可评分性状记录；答案侧无任何性状值，不能用于准确度评分。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_041：gold性状记录仅用于核验参考；不得回填答案缺失的性状来源或数值。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry EVID_001-EVID_006全部为INTERNAL_KNOWLEDGE_ONLY，database、record_id、locator均为空；路线、酶-EC、菌株身份、全路径能力等关键结论均无可定位外部来源，属MISSING_SOURCE低档。按P34默认不触发已核实错引cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / P34：MISSING_SOURCE/INTERNAL_KNOWLEDGE_ONLY按低分档处理，默认不触发已核实错引cap。

</details>

### D6 不确定性与诚实度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确标注internal knowledge、氧条件未指定、辅因子省略、性状null/unknown，有部分不确定性披露；但多个酶、菌株和全路径结论给high/medium confidence且无可定位来源，并把TCA路线称为“按指定路线”，未披露主要路线偏离及范围限制，属多处过度确信且主要限制未说明，按3–4档取4；非系统性误导，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / P119：单点/多处过度确信通常档内扣分；系统性把预测写成实证或掩盖主要矛盾才作D6 cap候选。

</details>
