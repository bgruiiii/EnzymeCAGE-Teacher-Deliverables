# BIOPATH150_083：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：quinate degradation II

污染物：(-)-Quinate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 61 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 34 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 49 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 56 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 56 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 46.5 | COMPARABLE | USER_AUTHORIZED_RECOLLECTION_R1 |

## GLM

答案SHA256：`41c1771d0d66b08169d127a761faf4196dc9c518809cc0ebb119196fb0c25fed`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> JSON完整，route_scope.chosen_route_name原样为quinate degradation II；steps均给出底物/产物（含英文名与SMILES或允许的null）、首选酶与EC、对应微生物；15项性状齐全，且同一菌仅用ORG_001去重。前3步覆盖本题冻结3步主链，S4-S9延伸至β-酮己二酸途径属于超出冻结终点的范围延伸，但已在uncertainties中披露，未造成必答模块缺失或明显格式缺陷。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块齐全：9步主链、每步酶/EC/微生物、15项性状、证据与不确定性均有交付；路线名按题面原样填写，JSON结构可读。仅少量SMILES、保藏号、基因组大小明确null，属允许未知，无重要模块缺失或范围偏离。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_083：本题主线为LINEAR_UNIQUE、ordered_step_count=3，冻结必答主链为3步
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_083：冻结根化合物为(-)-Quinate，终点为3,4-Dihydroxybenzoate；支持判断答案额外下游超越终点
- SCOPE_ROW / SCOPE#BIOPATH150_083#CG04：题面氧条件为null，答案route_scope.oxygen_condition=null与题面一致
- ANSWER_TEXT / 41c1771d0d66b08169d127a761faf4196dc9c518809cc0ebb119196fb0c25fed：答案确实交付9步、1个去重菌株profile及15项性状；不表示所述科学内容均正确

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 前3步主链化学方向与连接基本正确：S1由(-)-quinate氧化为3-dehydroquinate，S2脱水为3-dehydroshikimate，S3芳构化为protocatechuate；S4-S9的β-酮己二酸途径在化学上也连续，但超出冻结终点，只作额外延伸。主要缺陷是多个步骤缺失氧化还原/脱水辅因子或水（S1缺NAD(P)+/醌类受体，S2/S3缺H2O），属局部计量与表达不完整，按P103不自动cap；D2达本请求允许上界8，不因额外下游覆盖加分。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3与gold化学一致：quinate→3-dehydroquinate→3-dehydroshikimate→protocatechuate；S4–S9为β-酮己二酸下游，化学上连贯但gold未覆盖。题面未明确终点，额外下游不按覆盖率扣分；未见起始步错误、方向反转或原子明显不守恒。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：冻结S01-S03主链反应为quinate→3-dehydroquinate→3-dehydroshikimate→3,4-Dihydroxybenzoate，并列出S01氧化还原载体与S02/S03的H2O；不要求下游β-酮己二酸步骤
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_083：终点为3,4-Dihydroxybenzoate，支持S3之后为额外下游的判断
- ANSWER_TEXT / 41c1771d0d66b08169d127a761faf4196dc9c518809cc0ebb119196fb0c25fed：答案逐步反应、缺失辅因子/水及额外下游的实际文本位置

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> S2的酶名3-dehydroquinate dehydratase与EC 4.2.1.10和冻结accepted集合完全一致；S1酶名quinate dehydrogenase与accepted名称同族，但显式EC 1.1.5.6并非冻结accepted的1.1.1.282；S3酶名3-dehydroshikimate dehydratase与accepted名称一致，但显式EC 4.2.1.51并非冻结accepted的4.2.1.118。三者反应本身未见已核催化矛盾，故不判F；但仅S2在名称+EC层面完全可核，S1/S3的显式EC配对仍待核，不能当S，D3a只能按少量/部分目标可用并需实质EC核验处理。

<details><summary>V0.4理由与本行变化背景</summary>

S1/S2及S4–S8酶名-反应基本对应；S1用EC 1.1.5.6为醌依赖变体，gold列1.1.1.282，未核实；S3 EC 4.2.1.51与gold 4.2.1.118冲突且E0无记录，保持UNRESOLVED；S9 EC 2.3.1.174凭记忆。多数关键步骤有合理候选，少量关键EC待核，取7分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_083：冻结accepted酶名/EC：S01 quinate dehydrogenase=1.1.1.282；S02 3-dehydroquinate dehydratase=4.2.1.10；S03 3-dehydroshikimate dehydratase=4.2.1.118；不证明答案的1.1.5.6与4.2.1.51错误，但表明其不在本accepted集合内
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：冻结S01-S03目标反应及主链方向；支持三个必答目标步的化学上下文，不单独核验答案具体EC
- ANSWER_TEXT / 41c1771d0d66b08169d127a761faf4196dc9c518809cc0ebb119196fb0c25fed：答案实际填写的S1-S3酶名、EC及不确定性披露位置

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案把所有步骤及complete_pathway_organism_profile_id都归到P. putida KT2440（TaxID 160492）。E0只有P. putida物种TaxID 303及mt-2菌株记录，未提供KT2440菌株级身份、单步归属或完整路径能力证据；属于合理候选但关键粒度未核，落在5–6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤推荐P. putida KT2440，物种/菌株选择与β-酮己二酸途径相符；但TaxID 160492无E0记录，E0仅有P. putida species 303；完整路径能力无独立证据，gold complete-pathway名单不含P. putida但gold非穷尽。属合理候选、部分支持，取6分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持P. putida物种级名；不核验KT2440菌株或TaxID 160492。
- E0_EVIDENCE / f3e0:bacdive:12880：记录为P. putida mt-2/Paw1菌株及26/30°C培养记录；不是KT2440，也不能外推其全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_083：gold列出其他菌的步级归属和部分PATHWAY_COMPLETE；absence of P. putida不构成已证伪，但也不支持答案的KT2440全路径声称。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项性状字段齐全，部分通用性状（革兰氏阴性、杆状、不产孢、运动性等）与P. putida一般特征相容；但数值项（最适30°C、pH 7、GC 61.5%）及菌株特异性性状缺少KT2440的冻结记录支持，且有若干内部知识填充。关键项证据不足，落5–6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全，Gram阴性/杆状/运动/不产孢/GC 61.5等与P. putida常识相符；但KT2440无E0性状记录，F2最适30℃仅由培养温度推得（培养温度≠最适），pH/盐度/底物谱多为种级或内部知识，关键项证据不足。取6分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：提供P. putida mt-2的培养温度记录与保藏号；不能回填KT2440的数值或保藏信息。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_083：gold性状行针对其他菌；没有P. putida KT2440行，absence不等于已证伪，但不能支持答案的具体数值。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 路线、步骤、酶、微生物和多数性状均以INTERNAL_KNOWLEDGE_ONLY登记，没有可定位的数据库条目、DOI或计算记录；EVID_004虽有文献题名但明确为记忆引用、未逐条核对，且E0无对应记录。属于决策相关组来源缺失为主，按MISSING_SOURCE低分档，给2；无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

核心组CG01/CG02/CG03/CG05/CG07及CG08/CG09均只有INTERNAL_KNOWLEDGE_ONLY或无可定位条目；EVID_004为凭记忆文献且无DOI/record_id，free-text未解析。无已核实错引，MISSING_SOURCE低分档不cap；决策相关组无条目级可核对证据，取2分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / P34：仅有INTERNAL_KNOWLEDGE_ONLY或完全无引用按MISSING_SOURCE处理；默认低分且不自动cap。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确把多数来源标为INTERNAL_KNOWLEDGE_ONLY，列出EC/SMILES/菌株保藏/路线解释等不确定性，CoA SMILES未知处填null，整体证据性质披露较好；但部分性状和路由解释仍以medium confidence呈现且来源不具体，未达9–10的全面边界核验，取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案明确披露EC凭记忆、CoA SMILES缺失、路线范围不确定、保藏号/pH/盐度/基因组大小未知；source_type标为INTERNAL_KNOWLEDGE_ONLY，未把预测冒充观测。但部分步骤仍给high/medium置信且核心身份/性状缺独立支持，披露较好但非充分，取7分。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：仅证明答案自身有内部知识/未知/置信度披露，不证明外部科学内容正确。

</details>

## DeepSeek

答案SHA256：`75b489f123813a0bfda8b60c65bebd60a45353b52a5b41ba6070487ea618d192`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> D1: The answer supplies 9 steps, enzymes, one organism, and all 15 trait slots, but the required S01-S03 route structures are program-marked NONMATCH due stereo conflict, so task route conformance is materially compromised. The D1 cap applies; 4 is the top of the capped range given otherwise complete module coverage.

<details><summary>V0.4理由与本行变化背景</summary>

9步主链、每步酶名+EC、每步微生物、15项性状、chosen_route_name原样为quinate degradation II，主要模块均有涉及；但题面明文要求每步给出主底物与主产物的英文名及SMILES，实际S5/S8/S9两步或全部的SMILES均为null、S4/S6/S7部分为null（仅S1–S3成对完整），且“各项最强来源”仅用INTERNAL_KNOWLEDGE_ONLY占位、无record_id/locator，属若干必要内容遗漏与占位，落5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：Defines the required directed S01-S03 substrate/product structures and stereochemistry; the answer&#x27;s steps are program-marked NONMATCH.
- QUESTION_TEXT / question：Specifies route_scope.chosen_route_name must be quinate degradation II and asks for main route steps.
- ANSWER_TEXT / answer：Answer route_scope name and S1-S3 structures/SMILES; module fields are complete but structures differ.

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> D2: Main transformations (quinate oxidation, dehydroquinate dehydration, dehydroshikimate dehydration) are chemically plausible and the downstream beta-ketoadipate steps are continuous, but the required S01-S03 structures have explicit stereo conflict/NONMATCH; within the allowed D2 range &#91;1,5&#93;, 4 reflects multiple required-step structural errors.

<details><summary>V0.4理由与本行变化背景</summary>

主链前三步与gold反应行逐行吻合：(-)-Quinate→3-Dehydroquinate（氧化，forward）→3-Dehydroshikimate（脱水，reversible）→3,4-Dihydroxybenzoate/protocatechuate（脱水），产物身份与方向一致；其后S04–S09的β-酮己二酸步骤化学上连续且方向合理（开环→环异构→脱羧→内酯水解→CoA转移→硫解），但落在gold题面范围外（gold终点为protocatechuate），按四.2/P29不进入覆盖率加分或扣分；辅因子缺失（S1未列电子受体、S8未列succinyl-CoA）属局部计量缺陷（P102–P105），不cap。落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：Required S01-S03 directed structures and stereochemistry; answer structures differ.
- ANSWER_TEXT / answer：Answer S1-S9 SMILES and reaction types; transformations are plausible but required stereochemistry is not matched.

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分7 → V0.5新分1，变化-6。

新裁判理由：

> D3a: All three required target steps are confirmed F/ROUTE_BLOCKED_NONMATCH with KEY failure cap; S=0. Although S2/S3 ECs match accepted sets, target credit is blocked by the route stereo conflict, and S1 EC 1.1.99.25 is not the accepted 1.1.1.282. Under the full-F case, score 1 reflects no usable target catalytic credit.

<details><summary>V0.4理由与本行变化背景</summary>

S2（3-dehydroquinate dehydratase, EC 4.2.1.10）与S3（3-dehydroshikimate dehydratase, EC 4.2.1.118）的酶-EC与enzyme_gold完全一致；S1给出PQQ型quinate dehydrogenase EC 1.1.99.25，与gold酶条目EC 1.1.1.282（NAD(P)+型）不同，E0无EC条目（GAP-083-004/018），按四.5“无法核验→UNRESOLVED、保留待核、不判错不cap”处理；下游各步酶名与EC大类自洽（1.13.11.3加氧酶、5.5.1.2异构酶、4.1.1.44脱羧酶、3.1.1.24水解酶、2.8.3.6转移酶、2.3.1.174硫解酶），但E0亦无条目核验。落7–8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_083：Accepted enzyme/EC rows: S01 1.1.1.282; S02 4.2.1.10; S03 4.2.1.118.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：Required directed reactions; answer&#x27;s S01-S03 are NONMATCH due stereo conflict.
- ANSWER_TEXT / answer：Answer S1 EC 1.1.99.25; S2 EC 4.2.1.10; S3 EC 4.2.1.118.

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> D3b: A. baylyi name is consistent with S02/S03 step records, but the answer uses strain ADP1/taxid 53438 for all steps and claims whole-pathway degradation; frozen organism_gold has A. baylyi only as STEP for S02/S03, no PATHWAY_COMPLETE row, and no S01 A. baylyi support. Whole-pathway overclaim is a D3b key error; 4 is the capped upper bound with species-level step support for two steps.

<details><summary>V0.4理由与本行变化背景</summary>

答案统一推荐Acinetobacter baylyi ADP1（物种+菌株去重为单条profile，符合题面要求）；gold在S02/S03步即以Acinetobacter baylyi（种级taxid 202950）为步级菌，物种级身份对应成立；gold的S01步归属为Aspergillus nidulans、S03另有C. glutamicum/G. oxydans/N. crassa等，属gold多来源映射，答案以A. baylyi单菌承担全链并附PQQ型酶说明，属合理替代而非错配。未核点：TaxID 53438无E0记录（GAP-083-045），gold种级ID为202950；单菌完成整条路径（complete_pathway_organism_profile_id=ORG_001）在冻结证据中无全路径能力记录（gold pathway_complete未对A. baylyi标TRUE），按v0.3身份定位/反应级能力/全路径能力三层分离登记待核，未构成已核实关键错误。落7–8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_083：Lists A. baylyi only as STEP for S02/S03; PATHWAY_COMPLETE rows are other organisms, not A. baylyi.
- ANSWER_TEXT / answer：route_summary and complete_pathway_organism_profile_id/step microorganism fields claim A. baylyi ADP1 across the route.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> D4: Several traits match species-level A. baylyi records (non-motile, Gram-negative, non-spore-forming, genome size/GC range), but many key traits (F6/F7/F8/F9/F11/F15, and F14 accession) lack frozen support for the claimed ADP1 strain and are stated with high/medium confidence. Partially usable; substantial revision needed. No D4 key error because no absurd numerical value or explicit species-to-all-strains generalization is verified.

<details><summary>V0.4理由与本行变化背景</summary>

可核关键性状与gold种级代表记录一致：F12 Gram-negative（gold gram positive=false, OBSERVED）、F13 non-spore-forming（gold sporulation=false）、F10 non-motile（gold motility=false）、F14 gc_percent=40.3落在gold 40.1–40.5%、genome_size_bp=3,598,621落在gold观测区间；F3/F4/F5以value全null+confidence unknown诚实标注，不计为错误；F2 optimum 30°C（gold仅给出28–37°C生长记录，最适子字段不可评分）、F7/F8/F9/F11/F15无E0观测条目，F14登录号NC_005966.1无E0记录，均登记待核。未发现预测冒充观测、数值离谱或把种级观测硬说成株级定量。落7–8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_083：Species-level A. baylyi records for taxid 202950; supports some traits and marks others unknown or no robust majority.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_083：Marks observed-accuracy vs completeness-only traits; some traits are not scoreable for accuracy.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_083：Shows pending/unscoreable subfields, including temperature endpoints and salinity maximum.
- ANSWER_TEXT / answer：Answer trait values and confidence labels for the claimed ADP1 profile.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> D5: Both evidence_registry entries are INTERNAL_KNOWLEDGE_ONLY with null database, record_id, and locator; no locatable literature/database/computational record. This is MISSING_SOURCE across claims; no verified mis-citation. D5 low band 1-2; 1 because no important conclusion is traceable to an external source.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅有EVID_001/EVID_002两条，source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null，路径、酶、菌、性状全部claim group均为MISSING_SOURCE，无任何可定位条目级证据可核对（落1–2档的“几乎无法定位重要结论依据”）；但通篇未编造文献/DOI/访问号，未出现已核实错引，按P34/P41“全部缺失→低分档、默认不cap”，取2分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer：Evidence registry has only INTERNAL_KNOWLEDGE_ONLY entries with no database, record_id, or locator.
- RUBRIC_CLAUSE / P34：MISSING_SOURCE includes only INTERNAL_KNOWLEDGE_ONLY self-declaration and defaults not to a critical-error cap.

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> D6: Answer uses high/medium confidence and presents unsupported trait/pathway claims without limitations or uncertainties; however it marks evidence source_type INTERNAL_KNOWLEDGE_ONLY and leaves several traits explicitly unknown/null. This is multiple overconfidence/evidence-type confusion without verified systemic masking; D6 3-4, score 4.

<details><summary>V0.4理由与本行变化背景</summary>

答案对来源类型作了诚实标注（全部INTERNAL_KNOWLEDGE_ONLY）、未知项以null+confidence unknown标出，属部分不确定性说明；但uncertainties数组为空、无任何限制/冲突/待验证点陈述，且F1/F6/F10/F11/F12/F13以confidence=high包装仅有内部知识的条目，route_summary以确定语气声称整条路径，属多字段过度确信而非系统性掩盖，按P119落5–6档取5。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer：Confidence labels and source_type INTERNAL_KNOWLEDGE_ONLY; empty uncertainties array.
- RUBRIC_CLAUSE / P119：Single-point overconfidence vs systemic misleading; D6 cap only for systemic misleading.

</details>

## Kimi

答案SHA256：`19406916dacfc145c7c524c7099554d9eb0b245b3e42587babad01e89edb0175`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分9 → V0.5新分4，变化-5。

新裁判理由：

> 题目要求的3步主链、逐步酶/EC、微生物、15项性状字段均已实质交付，route_scope.chosen_route_name原样为quinate degradation II；但路线诊断为DEVIATES，且D1_task_range为&#91;1,4&#93;，故在该允许范围上沿取4，不把化学正确性重复计入D1。

<details><summary>V0.4理由与本行变化背景</summary>

三步骤（S1–S3）齐备：每步给出主底物与主产物英文名+SMILES，绑定一个首选酶（含EC）与一个对应微生物；route_scope.chosen_route_name原样填写quinate degradation II；同一菌按物种+菌株去重为单一ORG_001 profile；15项性状全部出现（12填、3项诚实null、0遗漏）。仅证据条目record_id多为null、性状3项为空值属完整度轻微缺口，未造成模块缺失或关联不清，故取9档高位而非10档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_083：支持gold为3步LINEAR_UNIQUE主链与题面主链范围；不证明答案化学结构正确。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分9 → V0.5新分5，变化-4。

新裁判理由：

> 按名称与方向，quinate→3-dehydroquinate→3-dehydroshikimate→protocatechuate与gold主链一致，S1含NAD+/NADH/H+，S2/S3为脱水；但程序诊断S01/S02未绑定、S03存在STEREO_CONFLICT_SPECIFIED（另有电荷记法），关键中间体/结构表示需修订，受D2允许上限&#91;1,5&#93;限制取5。

<details><summary>V0.4理由与本行变化背景</summary>

化学链与gold反应链S01–S03逐步对应：(-)-quinate→3-dehydroquinate（NAD+依赖氧化）→3-dehydroshikimate（脱水）→protocatechuate（脱水芳构化）。方向均为底物→产物、无反转；S1写出NAD+→NADH+H+，S2/S3写出H2O，氧化还原与脱水计量闭合；终点与gold terminal（3,4-Dihydroxybenzoate=原儿茶酸）一致，未向题定终点以下延伸；各步SMILES与gold isosmiles连接性一致，无起始步错误、无无依据跳步。档内取9：已主动声明路线边界（不向中心代谢延伸），未列下游continuation不扣分（四.2/P29）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：支持gold三步主链方向、底物/产物与S03终点；不证明答案所填SMILES/立体化学均正确。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_083：支持题面终点化合物为3,4-Dihydroxybenzoate/protocatechuate。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 程序D3a计数S=0,F=1,U=2；S03（KEY_TERMINAL）已确认目标失败并触发D-KEY4硬上限4。S01/S02仅ALIGNMENT_NOT_CONFIRMED，不判S也不判F；无可确认S，仅S02/S03酶名/EC与accepted有表面对应，终端关键失败使目标主功能严重受损，故在&#91;1,4&#93;内取3，不机械取4。

<details><summary>V0.4理由与本行变化背景</summary>

S2酶3-dehydroquinate dehydratase EC 4.2.1.10、S3酶3-dehydroshikimate dehydratase EC 4.2.1.118与gold逐字一致，酶名与反应类型（脱水/脱水芳构化）匹配；S1酶名quinate dehydrogenase与反应类型（NAD+依赖氧化）匹配，但EC 1.1.1.24与gold 1.1.1.282不一致，E0无相应EC冻结记录（GAP-083-001/010/011/015/030/033），无法核accepted name/reaction与active/transferred状态，按四.5保守条款保留待核、不cap；基因名QuiA/QuiB/QuiC无冻结记录。7–8档内取7：主要步骤酶对应有可靠支持，S1编号一项需进一步确认。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_083：支持accepted S01 EC1.1.1.282、S02 EC4.2.1.10、S03 EC4.2.1.118；不把EC一致扩展为具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：支持S03为KEY_TERMINAL及gold终点3,4-Dihydroxybenzoate；程序诊断为NONMATCH/STEREO_CONFLICT_SPECIFIED。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> Acinetobacter baylyi/ADP1身份在物种层面合理，S02/S03与gold的Acinetobacter baylyi步级记录同种；但TaxID 62977在E0无记录，S01的A. baylyi关联无gold步级支持，完整路径能力仅为注释/查询级，未充分核验。属部分支持、若干关键身份/范围未核，取5-6档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

全链条使用单一菌Acinetobacter baylyi ADP1：物种身份真实且与题定路线相符；gold在S02、S03步骤级列出Acinetobacter baylyi（EC 4.2.1.10 catabolic型、EC 4.2.1.118），与答案S02/S03归属一致；S01步骤级gold仅列Aspergillus nidulans，答案S01归属无gold支持，但gold非穷尽不据此判错。TaxID 62977为菌株级粒度，与声称粒度一致（物种级202950与菌株级62977可并存，P67），但E0无TAXID:62977记录（GAP-083-046/049）→UNRESOLVED；complete_pathway_organism_profile_id=ORG_001的整条路径能力声称不在gold PATHWAY_COMPLETE名单内，亦无独立能力记录。身份定位/反应级能力/全路径能力三层未全部核实（P69），故5–6档取6；无经核实的关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_083：支持gold S02/S03含Acinetobacter baylyi物种级步级记录；不等于ADP1菌株身份或全路径能力已核。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_083：支持本题主链为3步线性；不证明任何单一菌完成全路径。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 15项均返回，3项为显式unknown；F10不运动、F12革兰氏阴性、F13不产孢与gold物种级观测一致，F14基因组数值落入gold物种范围；但F2把DSMZ培养温度30°C写作optimum_c，F1严格好氧与gold aerotolerant记录不一致/需核，F7/F8/F9以路径/查询证据承担性状且多属未核，F11无robust majority；属部分准确但关键项证据/条件需修订，取6。

<details><summary>V0.4理由与本行变化背景</summary>

15项齐全、3项诚实null（F3/F4/F15），无编造填满。与同物种代表记录（taxid 202950）对照：F10不运动、F12革兰氏阴性、F13不产芽孢均获OBSERVED一致；F14 3,598,621 bp与GC 40.3%落于gold物种参考区间（2,250,030–3,746,897 bp；40.1–40.5%）；F2以DSMZ培养温度30 °C填optimum并明确声明“培养温度为依据、未获可靠上下限”，符合四.4“培养温度≠最适值”口径，且30 °C在观测生长范围28–37 °C内。不足：F5 DSM 24193与ADP1的菌株级对应、F11短杆状至球杆状（gold为No robust majority）、F14登录号NC_005966.1/GCF_000005825.1均无可核对记录（GAP-083-073..080）；F7/F9由路径成员关系推导酶活与碳源利用，非直接观测；F8由基因组潜力外推但已用“代谢潜力”限定。属“部分性状准确且适用、关键项证据不足”，5–6档取6；无经核实的关键科学错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_083：支持A. baylyi物种级代表记录中的部分性状（motility/gram/sporulation/genome范围等）；不自动覆盖ADP1菌株全部性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_083：标明部分性状仅completeness_only、部分温度/盐度子字段待裁定；不把不可评子字段当已知准确值。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出6条evidence_registry（MetaCyc/UniProt/NCBI/DSMZ/两篇DOI）并映射到步骤和性状，但多数为查询式/自由文本定位，E0无对应记录可核；未见已核实错引，故不cap。决策相关组部分有具体记录（GCF、DSM 24193、DOI），部分为查询级/缺映射，取5-6档下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出6条证据并把step/enzyme/microorganism/每项性状绑定到evidence_id，claim_scope书写清楚，属有结构的来源交付；EVID_003（GCF_000005825.1）、EVID_004（DSM 24193）与EVID_005/EVID_006（DOI）为条目级定位，但E0中均无冻结记录可核；EVID_001/EVID_002仅有检索式URL且record_id=null，属库级/检索式定位，决策相关组（CG01/02/03/05/07/08/09）的关键结论只能追到此类定位。无任何经核实的错引（E0对EC/TaxID/登录号/DOI全为EVIDENCE_GAP，按纪律保持UNRESOLVED、不判虚构、不判CONTRADICTED），故不cap。按P41：存在部分条目级可定位结论→5–6档，取5（关键组定位不足、无一条可对照冻结记录核对）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：仅支持答案实际交付了这些来源登记与映射；不证明其内容真实或充分支持对应结论。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案使用confidence与raw_text并显式null，但uncertainties为空且无限制说明；对未核TaxID、酶-EC、完整路径及多条性状给high/medium，属部分不确定性说明但部分结论强度超过E0可核范围，非系统性把预测写成观测，取5。

<details><summary>V0.4理由与本行变化背景</summary>

正面：F3/F4/F15明确null且confidence=unknown，F2明确写出“以DSMZ培养温度30 °C为依据；未获得可靠上下限”，正确区分培养温度与最适/上下限（四.4）；central_metabolism_entry声明题定终点边界，不把推断写成观测；F8以“代谢潜力”限定而非观测断言。不足：uncertainties为空数组、三步uncertainty=null，EC 1.1.1.24（与gold 1.1.1.282不符）、TaxID 62977、DSM 24193、NC_005966.1等未核实要素统一以confidence=high与DATABASE_DIRECT/LITERATURE_DIRECT标签呈现且零披露，属多点过度确信；但错误集中于同一批身份/编号断言、无系统性把预测写成实证、无已知矛盾被掩盖。按单点/多点过度确信非系统性误导口径，5–6档取6。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.confidence_fields_and_uncertainties：支持答案确有confidence/raw_text/显式null的登记；不证明这些置信声明与E0证据相称。

</details>

## Qwen

答案SHA256：`64434eb68adfa57aff03ac655a317203abdae1df1820ccd26ff74d7f35b6a311`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 题面要求的主链三步全部实质交付：S1 (-)-Quinate→3-Dehydroquinate、S2→3-Dehydroshikimate、S3→Protocatechuate，每步均给出英文名+SMILES、一个首选酶及EC、一个对应微生物；route_scope.chosen_route_name 原样填写“quinate degradation II”，未改选路线；organism_profiles 仅一条 ORG_001 并按 species+strain 去重后由三步共同引用，符合“同菌去重”。15项性状键齐全（F2/F3/F4/F5/F14 值为 null、其余10项有值），符合题面“不确定项为null”的交付约定，故 null 本身按诚实未知处理而非缺字段。扣分点为局部性而非结构性：S1 辅因子写作泛化占位名“acceptor”（SMILES为null）、微生物仅有种级 TaxID 303 而无菌株、gene_or_protein 全 null、evidence_registry 仅两条 INTERNAL_KNOWLEDGE_ONLY（来源质量另在D5评）。整体属“大部分必要内容完整、关联清楚、少量遗漏/工程性占位”，未达9–10所需的全部要素精确无缺。

<details><summary>V0.4理由与本行变化背景</summary>

三个步骤齐备，每步均给出主底物/主产物英文名与SMILES、单个首选酶与EC、一个对应微生物并做profile去重；route_scope.chosen_route_name按题面原样填quinate degradation II，未改选其他路线；15项性状一次返回且与身份区一致；证据登记与不确定性说明均在。仅剩局部完整度瑕疵（strain全null、S1氧化还原载体只写泛称acceptor未命名），未构成必要模块缺失或范围偏离，落9–10档取9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_083：任务要求：指定路线 quinate degradation II 的主链、每步底物/产物名+SMILES+一个首选酶及EC+一个对应微生物、15项性状、route_scope 原样填写路线名
- ANSWER_TEXT / S1：第1步主底物/主产物、酶 quinate dehydrogenase (quinone) 1.1.5.8、微生物 Pseudomonas putida 均已交付；辅因子仅为泛化 acceptor（smiles=null）
- ANSWER_TEXT / S2：第2步已交付 3-Dehydroquinate→3-Dehydroshikimate、酶与EC、菌
- ANSWER_TEXT / S3：第3步已交付 →Protocatechuate、酶 4.2.1.118、菌；非漏答
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_083：本题为 LINEAR_UNIQUE、ordered_step_count=3，与题面任务范围一致；该计数为全图材料数，本评只按本题3步必答主链计完整性

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 主链化学骨架成立：方向为降解型（quinate→…→protocatechuate），三步反应类型（氧化、脱水、脱水/芳构化）与gold一致，终点产物 Protocatechuate（3,4-dihydroxybenzoate，SMILES O=C(O)c1cc(O)c(O)cc1）与题面/金标终点一致，S1 底物与产物结构正确。但存在实质缺陷：S2 产物“3-Dehydroshikimate”所给 SMILES O=C(O)C1=CC(O)C(O)C(O)C1 环上为三个羟基且无酮基，实为莽草酸式连接（gold 为 C1C(C(C(=O)C=C1C(=O)&#91;O-&#93;)O)O），属名称—结构冲突的关键中间体错误；因此按字面写作的 S2（C7H10O6→C7H10O5+H2O）与 S3（C7H10O5→C7H6O4+H2O）氢原子不守恒，多出2H未说明。另有 S1 氧化还原载体未被具体写出（以“acceptor/reduced acceptor”占位、SMILES为null，与EC 1.1.5.8的醌型受体不相称）、立体化学整体缺省（表示层问题）。这些不推翻主链主要结论（名称、顺序、酶与终点正确，换成正确脱氢莽草酸结构后两步脱水即配平），故不构成D2关键错误，但“关键中间体仍需修订”对应5–6档，取该档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

主链方向与三步转化类型正确（醌依赖型氧化→脱水→脱水），起点(-)-Quinate、终点protocatechuate与gold S01–S03及terminal逐一对齐，且明确止于题面路线范围、无无依据跳步或方向反转。但S2主产物标为3-Dehydroshikimate，所给SMILES却是三羟基环己烯羧酸（无酮羰基，相当于C7H10O5），与dehydroquinate(C7H10O6)脱水生成dehydroshikimate(C7H8O5)的计量不符，S3沿用同一结构又生成C7H6O4+H2O，使S2/S3氢原子不守恒且未作说明；该缺陷落在关键中间体的结构表达，属需实质修订，未推翻主链结论，按5–6档取6，不触发cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：逐步主底物/主产物身份与正确结构：S1 (-)-Quinate→3-Dehydroquinate（含NAD(P)+/NAD(P)H/H+载体）、S2 3-Dehydroquinate→3-Dehydroshikimic acid（canonical SMILES含酮基与一个C=C）、S3 3-Dehydroshikimic acid→3,4-Dihydroxybenzoate+H2O；可用于核对所给SMILES是否与名称一致
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_083：本题终点化合物为 3,4-Dihydroxybenzoate，用于核对答案终点未越界也未错位
- ANSWER_TEXT / S2：答案自述第2步脱水产物结构，可与金标脱氢莽草酸结构逐原子比较（实测无酮基、三个羟基→名实不符）
- ANSWER_TEXT / S3：第3步沿用同一错误中间体结构作为底物，导致该步按字面亦不配平；产物本身为正确的原儿茶酸

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 第1步：答案给“quinate dehydrogenase (quinone)” EC 1.1.5.8，与accepted集合的 quinate dehydrogenase / EC 1.1.1.282 为同一底物同一转化的不同电子受体酶，不构成已核催化不相容；但冻结证据无该EC记录（GAP-083-003/017），名—号配对与相应粒度支持仍不可判，按U（支持/配对待核）而非F。第2步 EC 4.2.1.10 名称“3-dehydroquinate dehydratase”与accepted酶名/EC逐字一致；第3步 EC 4.2.1.118 名称“3-dehydroshikimate dehydratase”亦与accepted一致，两步在G4策展粒度上获得可核功能支持（accepted集合声明“该反应可由这些酶名/EC催化”，不外推具体蛋白活性）。但程序路线诊断为 BOUNDARY_REVIEW：S01/S02 为 UNRESOLVED（表示/身份边界未裁定）、S03 NO_BOUND_RELATION，均非MATCH，故不能据C03赋S；同一事实的中间体结构错误已在D2计，不在此双计。三个目标均为KEY/MAJOR且有U，按C05不得进入7–8档；亦无任何已核催化失败或实证漏答（catalytic_failure_proof=null，KEY4不触发）。综合：多数目标（2/3）的酶名—EC在accepted集合内、边界清楚，剩余部分为可信但未核的替代EC加表示层缺陷，取5–6档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名与EC内部自洽且反应类型匹配：S2 3-dehydroquinate dehydratase/EC 4.2.1.10、S3 3-dehydroshikimate dehydratase/EC 4.2.1.118与gold完全一致；S1给quinate dehydrogenase (quinone)/EC 1.1.5.8，与gold的1.1.1.282（NAD(P)+型）为同一反应的另一合法酶型，E0对该EC无冻结记录，按四.5保守条款登记UNRESOLVED、不判错。三步均只标confidence low且仅内部知识来源，故取7而不上探更高档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_083：本题各必答步的受支持酶名与EC：S01 quinate dehydrogenase / 1.1.1.282；S02 4.2.1.10（多个同工酶名均属同一步）；S03 4.2.1.118；为数据库策展粒度（G4），不支持任意具体蛋白底物谱或实验活性
- ANSWER_TEXT / S1：第1步实际给出的酶名与EC（1.1.5.8）——可与accepted集合比对，属同一转化但不同EC、不在accepted集合内
- ANSWER_TEXT / S2：第2步酶名与EC与accepted逐字一致（4.2.1.10），功能级支持成立；其产物结构问题属D2，不在此重复计入酶对应
- ANSWER_TEXT / S3：第3步酶名与EC与accepted逐字一致（4.2.1.118）；该步目标绑定为NO_BOUND_RELATION，故按U登记而非S
- E0_EVIDENCE / f3e0:bacdive:12880：仅陈述 Pseudomonas putida mt-2 PaW1(pWWO) 菌株记录与保藏号、培养温度26/30°C等事实，不含EC或酶-反应支持；不能用于证实或否证本答案任一步的酶-反应对应

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> P. putida物种身份与TaxID 303有E0分类记录支持，但答案未给菌株，且三步单步归属与complete_pathway_organism_profile_id所声称的全路径能力没有对应反应/全路径证据。无已核身份矛盾或跨类群错配，故不cap；按5–6档取6：有合理候选和部分身份支持，但关键作用范围/全路径能力仍充分未核。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份合理：Pseudomonas putida与TaxID 303的官方名称关联在E0中核为SUPPORTED（F3R1CLM-004335），未编造菌株或保藏号（strain/collection均null，符合题面null纪律）。但答案把该物种同时指派为全部三步的催化者并设complete_pathway_organism_profile_id=ORG_001，等于声称整条路径能力，却无步级归属或全路径能力证据（F3R1CLM-003992/000207为UNRESOLVED）；与gold步级菌（真菌与放线菌等）不同，gold非穷尽故不据此判错。身份真实≠反应级能力≠完整路径能力，落5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持TaxID 303与P. putida名称关联；不支持任何单步催化或全路径能力。
- E0_EVIDENCE / f3e0:bacdive:12880：支持该菌株记录存在；不支持quinate降解或各步酶归属。
- ANSWER_TEXT / ANSWER_TEXT：支持答案声称同一物种承担三步与全路径；不证明能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项性状均出现，10项有值、5项明确null，null处理诚实。多数有值性状仅为低置信定性描述，无locatable来源；F7声称可利用quinate为碳源/能源未被E0 12880底物面板支持，F8把quinate称为芳香族化合物存在表述错误。无已核数值离谱或物种级推广到菌株级的关键错误，按5–6档取5：部分性状合理，但关键证据不足且局部解释需修订。

<details><summary>V0.4理由与本行变化背景</summary>

10项性状已填：F1好氧、F6有氧呼吸/末端受体氧气、F7可利用(-)-quinate、F8、F9、F10可运动、F11杆状、F12革兰氏阴性、F13不产芽孢、F15土壤/水体/根际；5项null并标confidence unknown（F2/F3/F4/F5/F14），按题面诚实null处理，不与遗漏或错误等同。物种级定性描述总体与Pseudomonas putida常识相符，但raw_text全为null、证据仅INTERNAL_KNOWLEDGE_ONLY，无任何数值、单位与观测条件，关键项不可核；F8把quinate写作芳香族化合物属解释瑕疵。落5–6档取6（缺失的完成度扣分归D1，不在此重复重扣）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持该P. putida菌株的部分表型记录；面板未列quinate，不能支持F7/F8。
- ANSWER_TEXT / ANSWER_TEXT：支持答案填写了哪些性状值与null；不证明这些性状已获来源支持。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 答案的证据登记EVID_001/EVID_002均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为null；步骤、酶、菌与性状的关键结论无法追到可定位文献/数据库条目/计算记录。属MISSING_SOURCE低分档，且不是已核实错引，默认不触发cap。按1–2档取1：重要结论依据几乎无法定位。

<details><summary>V0.4理由与本行变化背景</summary>

全部结论只由EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY自我声明支撑（database/record_id/locator全为null，raw_text全空），路线、酶-EC、微生物身份与性状均无可定位的文献条目、数据库记录或计算记录；按四.3六状态全组登记MISSING_SOURCE，属来源缺失而非误导，默认不触发cap。E0中TaxID 303名称关联虽为SUPPORTED，但按OBS-POS-LOCATABLE只登记在事实层，不回填为答案来源或提升来源状态。无任何可追溯条目，落1–2档取2；答案未编造引用这一正面因素在D6计，不在D5加分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：支持答案只交付了内部知识标签；不提供任何可定位外部来源。
- E0_EVIDENCE / f3e0:taxid:303：可支持P. putida名称身份，但不由答案交付，也不支持路线/酶/性状来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案把已填酶/菌/性状全部标为low confidence，未填项用null并说明氧条件、辅因子、菌株、下游归属不确定性；没有把内部推断系统写成观测实证。主要限制披露较具体，仅全路径菌能力未单独标注不确定，属轻微披露缺口，按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界披露总体到位：两条证据均标INTERNAL_KNOWLEDGE_ONLY、全部confidence为low/unknown，5项性状null并明确标unknown，uncertainties列出氧条件未指定、初始脱氢酶电子受体/辅因子未细化、菌株与保藏信息未知、下游裂解是否属指定路线未确认，并声明主链止于题面终点、下游另列不计入；未把预测包装成观测，无掩盖已知冲突。扣分点：整条路线与全路径菌能力仅以低置信呈现而未作“记忆值、建议复核”的显式声明，S2中间体名称与SMILES不一致未披露；属单点/局部过度确信而非系统性误导，落7–8档取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：支持答案对未知、低置信和路线边界有明确披露；不证明披露内容本身科学正确。

</details>

## Grok

答案SHA256：`0755fad5e8edeb64b0fafea81866cd1d101a145ff6a0a0173653c350e1547615`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All requested modules are present and structured: 3-step main route ending at protocatechuate, enzyme/EC and organism per step, one deduplicated organism profile with all 15 traits, evidence registry, and uncertainty notes. However the frozen route diagnosis is DEVIATES, with S1/S2 NONMATCH owing to specified stereochemical conflict; within the allowed D1 range &#91;1,4&#93;, this otherwise complete delivery is limited to 4 rather than a higher completeness score.

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：Sets route quinate degradation II and required main-route output; does not prove answer chemistry.
- ANSWER_TEXT / ANSWER：Shows delivered modules and structures; does not by itself verify them.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：Gold substrate/product structures and endpoint; used only for structural comparison, not enzyme activity.

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The named transformations are the expected oxidation-dehydration-aromatization sequence to protocatechuate, and S1 includes NAD+/NADH while S2/S3 include H2O. But the frozen route diagnosis marks S1/S2 NONMATCH owing to STEREO_CONFLICT_SPECIFIED and S3 UNKNOWN/charge-blind. An explicit stereo conflict permits at most 5; because two of three core steps are affected and S3 remains unresolved, choose 4 within the allowed &#91;1,5&#93; range.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：Gold reaction direction, substrate/product identities, and endpoint; not a proof of answer enzyme activity.
- ANSWER_TEXT / ANSWER：Shows answer chemistry and cofactor representation; used for comparison only.

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按D3a只审目标反应的酶功能/accepted支持：S1 quinate/shikimate dehydrogenase EC 1.1.1.282、S2 3-dehydroquinate dehydratase EC 4.2.1.10、S3 3-dehydroshikimate dehydratase EC 4.2.1.118，均与本题accepted集合中的目标酶/EC对应。qsuD/qsuB/qsuC仅为普通基因/蛋白归属附加项，题面要求首选酶与EC而非特定蛋白实测，其未核不推翻已支持的目标功能。路线诊断中的表示/立体疑点不单独改写D3a酶功能结论，且无已核催化不相容或关键酶失败。因程序不允许D3a 9–10且仍有轻微名称同义/附加归属待核边界，取&#91;7,8&#93;带内上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_083：支持S01 quinate dehydrogenase EC 1.1.1.282、S02 3-dehydroquinate dehydratase EC 4.2.1.10、S03 3-dehydroshikimate dehydratase EC 4.2.1.118的G4功能级 accepted 酶/EC 对应；不证明任意具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：支持S01-&gt;S02-&gt;S03的目标主链反应方向及主底物/主产物身份，用于核对酶所对应的目标反应；不提供酶活实验证明。
- ANSWER_TEXT / 0755fad5e8edeb64b0fafea81866cd1d101a145ff6a0a0173653c350e1547615：答案实际交付三个目标步骤的酶名/EC：1.1.1.282、4.2.1.10、4.2.1.118；同时给出qsuD/qsuB/qsuC作为可选基因/蛋白归属。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All three steps are assigned to Corynebacterium glutamicum ATCC 13032. The gold organism table supports C. glutamicum at S2/S3, and the PATHWAY_COMPLETE row supports C. glutamicum as a quinate-degrading organism. The strain-level TaxID 196627 and ATCC 13032 identity are not independently verified in the provided E0/gold, so species-level support cannot fully certify the strain; no contradicting strain identity is shown. Choose 7 in the 7-8 band because the core microbial recommendation is supported but the strain granularity remains unresolved.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_083：Gold lists C. glutamicum species and pathway-complete status; does not verify strain TaxID 196627.
- ANSWER_TEXT / ANSWER：Shows claimed C. glutamicum ATCC 13032 assignment.

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Several provided traits are qualitatively consistent with the gold species representative: Gram-positive, non-motile, non-sporulating, rod-shaped, oxygen/respiration context, and temperature 30 C within the observed 28-37 C growth record and mesophilic preference. However several numeric subfields are null where gold has observed scalars (pH min/max, salinity numeric, genome size/GC), and F8/F15 contain broader downstream/habitat claims beyond the frozen main route. These are local issues rather than a dimension-invalidating error; choose 7 in the 7-8 band.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_083：Species-level representative traits; not all fields are strain-specific and some are UNKNOWN.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_083：Indicates which trait fields are scoreable versus completeness-only; does not set the score.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_083：Subfield scoreability and pending range-policy flags; used to avoid treating non-scoreable categories as numeric errors.
- ANSWER_TEXT / ANSWER：Shows delivered trait values, evidence IDs, and confidence.

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Core route/enzyme/microbe claims are tied to a specific literature locator in EVID_001, and some carbon/enzyme traits also use it. However the paper is not present in the E0 snapshot, so exact support cannot be verified; many other traits use EVID_002 INTERNAL_KNOWLEDGE_ONLY, which is a missing-source status. The claim-group registry therefore has core groups as UNRESOLVED_SOURCE and many trait groups as MISSING_SOURCE, with no verified mis-citation. This is partial locatability with substantial source gaps, so choose 5 in the 5-6 band.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows delivered source records and internal-only declarations; not external verification.

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer explicitly lists uncertainties about route I/II boundary, an alternative quinone-dependent route, cofactor choice, and missing numeric values, and it leaves unknown numeric fields null rather than inventing them. It also labels evidence source types and confidence. Some high-confidence labels on internal-knowledge traits are overconfident, and possible stereochemical representation risk is not disclosed, but the issue is local rather than systemic. Choose 7 in the 7-8 band.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows uncertainty disclosures and confidence labels.
- QUESTION_TEXT / QUESTION：Shows task allows null/unknown and requires uncertainty disclosure; not scientific evidence.

</details>

## GPT5.6

答案SHA256：`994cfed83fe76467c340154c38d1956720f06775e1792d58ac89eee298cf406e`。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步主链、每步酶/EC与对应微生物均有给出，主要模块在场；但S2产物与S3底物SMILES为null，S1底物/产物SMILES结构有误，且15项性状全为null（明确未知），完整性只到5–6档上沿，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;：答案交付三步主链及每步酶/EC/菌；部分SMILES缺失或结构错误，性状全null
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：gold三步有向反应及主底物/主产物；支持任务范围与终点，不证明答案SMILES正确
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_083：gold性状记录多为UNKNOWN；不用于回填答案缺失性状

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按名称与方向，三步主链为quinate→3-dehydroquinate→3-dehydroshikimate→protocatechuate，与gold顺序一致；但S1底物与产物SMILES均多一个羟基，结构不等同quinate/3-dehydroquinate，S2产物与S3底物SMILES缺失。关键转化名称成立而结构表达多处不可靠，落入3–4档，取上沿4；未判单一关键错误cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;：答案给出三步名称/方向，但S1 SMILES含额外羟基、S2产物/S3底物SMILES缺失
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_083：gold canonical SMILES与有向反应；用于比较结构，不自动扩展到未声称内容

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步酶名/EC均与accepted集合对应：S01 quinate dehydrogenase/1.1.1.282，S02 3-dehydroquinase/4.2.1.10（accepted dehydratase同EC），S03 3-dehydroshikimate dehydratase/4.2.1.118；功能级G4支持成立。S2名称属同义表达但EC一致，按&#91;7,8&#93;取8；9–10受release base range与high-tier policy限制不启用。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;.enzyme：答案三步酶名与EC
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_083：gold各步accepted酶名/EC；G4策展粒度，不证明具体蛋白实验活性

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S01 organism_gold对Aspergillus nidulans为EXACT；PATHWAY_COMPLETE行taxid 162425（Aspergillus nidulans）为TRUE，支持全路径能力。S02/S03步级organism_gold未列该菌，但全路径完整行可支持；taxid/strain为null属交付缺失而非已核错误。主要微生物对应可靠，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;.microorganism; ANSWER.organism_profiles&#91;0&#93;：答案三步均用A. nidulans，未给菌株/TaxID
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_083：S01 exact A. nidulans；PATHWAY_COMPLETE taxid 162425 A. nidulans=TRUE；不扩展到具体菌株实验

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P44：全部必需性状均为null/空值时D4按MISSING=1，不宣称检测到科学错误；D1已记完成度不足。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：15项性状均未交付可评价值
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_083：gold性状记录多为UNKNOWN；不能回填答案缺失来源

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry全部source_type=INTERNAL_KNOWLEDGE_ONLY，仅自述MetaCyc record_id/locator，未交付可定位外部记录；核心路线/酶/身份组均MISSING_SOURCE。按D5低档&#91;1,2&#93;取2（有结构化自述但不可核验）。未核实错引，不触发cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;*&#93;：全部来源为INTERNAL_KNOWLEDGE_ONLY，无外部可核记录

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确披露菌株/TaxID/15性状无可靠单一来源、S2 SMILES未确认，并将性状标unknown；主要限制已说明。但核心酶/菌仍以medium confidence呈现，且S1 SMILES结构错误未披露；属单点过度确信/披露不完整，未达系统性误导，按&#91;7,8&#93;取7，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; confidence fields：答案披露部分未知与限制，但核心步骤仍medium confidence

</details>
