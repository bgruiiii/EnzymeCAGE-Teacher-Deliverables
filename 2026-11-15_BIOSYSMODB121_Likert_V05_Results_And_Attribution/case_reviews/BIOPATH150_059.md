# BIOPATH150_059：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：L-tryptophan degradation to 2-amino-3-carboxymuconate semialdehyde

污染物：Tryptophan；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 47 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 59.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 73.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 62 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 71 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 44.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`aba504988019c643e2b38089782389a256c3326949b753e04713d64f90513c2e`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分9 → V0.5新分4，变化-5。

新裁判理由：

> All major requested modules are present: five steps with substrates, products, enzymes, ECs, microorganisms, three organism profiles with 15 trait fields each, an evidence registry, and route scope. However the frozen route diagnosis marks route_status=DEVIATES and the terminal product is not accepted as the specified terminal; the allowed D1 range is &#91;1,4&#93;. Within that cap, 4 reflects strong completeness but a task/endpoint conformity failure.

<details><summary>V0.4理由与本行变化背景</summary>

覆盖5步主链、每步底物/产物/SMILES、酶/EC、对应菌及3个organism profile的15项性状；route_scope.chosen_route_name原样填写题面路线名，氧条件保持null；未见路线改选或核心模块缺失。少量性状以显式null/unknown交付，属完成度内可接受。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：Gold terminal product and step order; does not by itself evaluate nonterminal answer content
- ANSWER_TEXT / ANSWER.steps&#91;4&#93;.products&#91;0&#93;：Answer terminal product as delivered; used only for terminal conformity comparison

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分9 → V0.5新分5，变化-4。

新裁判理由：

> The four sequential nonterminal kynurenine transformations are chemically coherent in direction and continuity, and the answer includes O2/NADPH/H2O cofactors. The terminal product representation/identity is not accepted by the frozen route diagnosis, so the specified endpoint chemistry is not fully successful; no first-step reversal or gross atom-accounting failure warrants a lower D2 key cap. Score 5 within the allowed &#91;1,6&#93; range.

<details><summary>V0.4理由与本行变化背景</summary>

五步为经典犬尿氨酸途径：Trp→N-formyl-L-kynurenine→L-kynurenine→3-hydroxy-L-kynurenine→3-hydroxyanthranilate→ACMS；起点、方向、主链顺序与题面终点、gold主链一致，关键加氧/水解/裂解步骤与辅因子标注基本完整；SMILES个别写法非规范但化学连接与gold一致，未见反转、无依据跳步或原子明显不守恒。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：Gold reaction direction and continuity; terminal product comparison only

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分9 → V0.5新分3，变化-6。

新裁判理由：

> Frozen target counts are S=1, F=1, U=3, M=0, H=0 over N=5. The single support is the entry step S05; the confirmed failure is the KEY terminal S01, so D3a is capped at 4. One supported target plus a key terminal failure and three unresolved internal alignments places the answer among few usable targets with a serious key failure, not the top of the restricted range.

<details><summary>V0.4理由与本行变化背景</summary>

五步EC与gold enzyme_gold逐项一致：1.13.11.11、3.5.1.9、1.14.13.9、3.7.1.3、1.13.11.6；酶名与反应类型匹配，未见EC大类、酶名或反应类型矛盾。基因/蛋白名多为常见标注，但E0未逐条核验，属次要未核项。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：Gold target reactions for terminal failure and entry support; other target alignments remain under representation holds
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：Enzyme/EC accepted-set pairs only; does not establish specific strain activity

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> The organism choices are plausible and partly aligned: P. fluorescens TaxID 294 identity is supported in E0; S. cerevisiae is the gold species-level organism for KMO and HAAO. However PAO1 and S288C strain-level records are absent from E0, P. aeruginosa is not in the gold organism rows for TDO/formamidase, and the P. fluorescens whole-pathway degradation wording exceeds the single-step evidence. No identity contradiction or cross-kingdom error is verified, so no D3b cap; 5-6 band with score 6.

<details><summary>V0.4理由与本行变化背景</summary>

S3/S5用S. cerevisiae与gold step organisms一致；S4的P. fluorescens物种身份由E0 TaxID 294记录支持；S1/S2的P. aeruginosa PAO1及S4步级催化能力缺乏冻结记录，但属合理候选，且答案未声称单一菌完成整条路径（complete_pathway_organism_profile_id=null），并在uncertainties中限定P. aeruginosa主要走向分支。主要身份与作用范围未见已核实错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：Supports only Pseudomonas fluorescens TaxID 294 identity/rank/lineage; does not support kynureninase or whole-pathway capability
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_059：Gold organism associations for the listed steps; not an exhaustive organism list

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> All three profiles return the 15 trait shells. P. fluorescens morphology, Gram-negative, non-sporulating and motile traits align with observed gold rows, and several other values are plausible. However many strain-level values for PAO1/S288C are unverified, some P. fluorescens observed fields are left null, and whole-pathway tryptophan-degradation wording is broader than the single-step support. Explicit nulls are not treated as false; 5-6 band, score 6.

<details><summary>V0.4理由与本行变化背景</summary>

已给性状总体为常见且与gold/通行知识不冲突；P. fluorescens的运动、杆状、革兰阴性、不产孢与gold一致；PAO1与S288C的形态/染色/温度/基因组数值大体合理。不足在于多个性状仅INTERNAL_KNOWLEDGE_ONLY或未在E0核验，P. fluorescens的pH、盐度、保藏号、基因组缺失，S. cerevisiae多数性状无冻结记录；未见已核实的关键性状错误或把预测冒充观测的明确证据。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_059：Observed trait records for reference organisms; species-level records do not automatically prove answer strain-level values
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_059：Identifies which observed trait subfields are scoreable; missing/unknown fields remain completeness rather than scientific error

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> The answer provides an evidence registry with per-step and per-trait mappings, but the core route and enzyme claims rely on EVID_001/EVID_003/EVID_005/EVID_006/EVID_007 INTERNAL_KNOWLEDGE_ONLY or generic literature lists. E0 supplies only the TaxID 294 identity record. Thus important conclusions are mostly not traceable to item-level verifiable sources; no verified mis-citation is established, so no cap, but D5 falls in the low/generic-source band.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关核心组（路线、起点/终点、酶-EC、核心菌身份、步级归属）主要依赖EVID_001/003/005/006/007的INTERNAL_KNOWLEDGE_ONLY或笼统KEGG/教材/BRENDA/SGD表述，没有可定位条目级记录；仅少数基因组文献和TaxID 294记录可定位/支持，不能覆盖核心路径与酶菌结论。无已核实错引，MISSING/GENERIC默认不cap，按低分档3分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：Supports only TaxID 294 identity; does not support EC, route, or trait claims
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：Gold enzyme/EC reference rows; not equivalent to answer-delivered locatable sources

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer gives specific uncertainties, explicit nulls, alternative branches marked not part of the scored route, and evidence source_type labels. However the core route is largely EVID_001 INTERNAL_KNOWLEDGE_ONLY but rated high confidence, and the terminal product mismatch is not disclosed. This is limited overconfidence rather than systemic misrepresentation; 5-6 band, score 6.

<details><summary>V0.4理由与本行变化背景</summary>

答案有uncertainties与多处null/unknown，明确P. aeruginosa不完成整链、P. fluorescens菌株未知、盐度等缺来源，具备部分不确定性说明；但大量仅内部常识的酶/性状仍标high或medium，未系统区分观测、知识推断与预测，部分置信强度超过可核依据。属部分披露但强度偏高，未达系统性把预测写成实证的cap程度。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows the answer&#x27;s own disclosure text; not an external verification of the claims

</details>

## DeepSeek

答案SHA256：`378b0efbf7097aae8eaca5a54854b5fc28c108280b502c29637d40fff0cb67a4`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案按题面指定路线给出5步主链，route_scope.chosen_route_name与题面逐字一致，并覆盖至指定终点；每步均有底物/产物名称与SMILES、酶及EC、对应微生物。organism_profiles提供全部15项性状字段，但其中7项为明确null/unknown，题面允许未知项填null，故不按缺失处理，但对D1完成度只构成部分不足；无改选路线、无缺步或模块级遗漏。因此落在7–8档，取8。

<details><summary>V0.4理由与本行变化背景</summary>

5步主链、起点与题面终点、每步底物/产物SMILES、首选酶+EC、对应微生物、15项性状外壳、evidence_registry与uncertainties均按v2结构实质交付；route_scope.chosen_route_name逐字复用题面路线名，未改选路线。扣分点：15项性状中7项为null（F2温度/F3 pH/F4盐度/F5保藏/F7碳源/F9酶活/F14基因组），其中F5、F14及F2在冻结gold中本有物种级记录，属完成度损失（不判科学错误）；辅因子字段未列但题面未强制要求。档位7–8，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_059：支持题面路线名称、起始物和终点化合物身份；不证明答案每一步化学正确性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_059：支持本题在冻结材料中为5步线性主链、ordered_step_count=5；不直接支持答案文本本身。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：支持冻结主链的逐步连接和终点范围；不把gold下游或旁支自动当作D1必答分母。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 五个有机主转化与冻结gold顺序一致：L-tryptophan→N-formyl-L-kynurenine→L-kynurenine→3-hydroxy-L-kynurenine→3-hydroxyanthranilate→2-amino-3-carboxymuconate semialdehyde；方向为降解正向，关键中间体、步骤连接和终点正确，未见主链化学错误或断裂。主要缺陷是S1/S3/S5未列O2/NADPH等辅因子，S2/S4未列H2O/H+，多步字面计量不完整；按P103属局部计量缺陷，应在7–8档处理而非关键错误。故取8。

<details><summary>V0.4理由与本行变化背景</summary>

五步化学与冻结gold逐行吻合：Trp→N-formyl-L-kynurenine→L-kynurenine(+formate)→3-hydroxy-L-kynurenine→3-hydroxyanthranilate(+alanine)→2-amino-3-carboxymuconate semialdehyde；方向、原子连接与题面指定终点一致，核对ACMS的SMILES与gold canonical结构一致，3-hydroxyanthranilate、3-hydroxykynurenine亦一致。不足：双加氧酶缺O2、单加氧酶缺NADPH等辅因子与计量标注，属局部计量缺陷（八.辅因子条款），不构成关键错误；档位7–8，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：支持五步主链的底物/产物、方向、关键中间体、步骤连接、辅因子角色和终点；不扩展到未声称的下游或旁支。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_059：支持题面路线终点2-amino-3-carboxymuconate semialdehyde的化合物身份；不证明中间步骤的酶活或菌株能力。

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 五步答案的酶名+EC与accepted sets逐字对应：Trp→N-formylkynurenine用tryptophan 2,3-dioxygenase EC 1.13.11.11；formamidase EC 3.5.1.9；kynurenine 3-monooxygenase EC 1.14.13.9；kynureninase EC 3.7.1.3；3-hydroxyanthranilate 3,4-dioxygenase EC 1.13.11.6，均属G4策展级功能支持。故主要目标催化对应可靠；但全部目标均为ROUTE_HOLD_REPRESENTATION/UNRESOLVED、target credit=HOLD，且D3a允许区间上限为&#91;1,8&#93;、9–10 policyA=NOT_ELIGIBLE，故取良好带下沿7，不取8/9。

<details><summary>V0.4理由与本行变化背景</summary>

五步酶-反应对应与gold enzyme_gold逐行一致：tryptophan 2,3-dioxygenase EC 1.13.11.11（gold该步为1.13.11.11|1.13.11.52多注）、kynurenine formamidase EC 3.5.1.9、kynurenine 3-monooxygenase EC 1.14.13.9、kynureninase EC 3.7.1.3、3-hydroxyanthranilate 3,4-dioxygenase EC 1.13.11.6；酶名、EC大类与反应类型匹配，未出现名号矛盾。扣分点：gene_or_protein全为null、trace到具体蛋白身份不清，且EC官方accepted name/reaction未在E0核验（GAP-059-002/003/004/006/007），未达9–10的“身份与作用范围清楚”。档位7–8，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：提供五步accepted酶名/EC行；仅支持数据库策展粒度G4，不证明具体蛋白实验活性
- ANSWER_TEXT / BIOPATH150_059.answer.steps&#91;&#93;.enzyme：答案填写的酶名与EC，仅作逐字对照来源

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Pseudomonas fluorescens（TaxID 294）身份由E0核实为种级记录；在organism_gold中该菌仅列于S01（3-hydroxyanthranilate 3,4-dioxygenase）一步，答案却把它用于全部五步并设complete_pathway_organism_profile_id=ORG_001，属以单步/内部知识支持整条路径能力。CG08/CG09均UNRESOLVED；gold非穷尽，不能把“未列”当已证伪，故不是已核实关键错误，取5–6带下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份层成立：Pseudomonas fluorescens、TaxID 294经E0核实为种级官方记录（名称对应SUPPORTED），且答案未声称菌株与保藏号，与“物种级声称”粒度一致。问题在能力层：同一物种被指派为全部5步的唯一执行菌，并以complete_pathway_organism_profile_id=ORG_001声称其完成整条路径，而答案证据仅INTERNAL_KNOWLEDGE_ONLY，无步级或全路径能力记录；gold中294仅作为3-hydroxyanthranilate 3,4-dioxygenase步骤四株备选之一出现，gold不穷尽、且不自动否定，故不判已核实错误，仅登记未核。身份定位≠反应级能力≠完整路径能力三层不得互替（P69）。档位5–6（合理候选、身份有支持、作用范围未核验），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：仅支持TaxID 294对应Pseudomonas fluorescens、rank=species与lineage；不支持任何单步催化或全路径能力
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_059：展示P. fluorescens(294)仅出现在S01一步；PATHWAY_COMPLETE行为S. cerevisiae与B. cenocepacia，非穷尽

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 已给性状中，F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating与gold对TaxID 294的OBSERVED记录一致；F1“aerobic”相对gold“aerotolerant=true”属简化；F8“degrades L-tryptophan…”在gold中无对应记录，F15 habitat在gold为UNKNOWN；F2/F3/F4/F5/F7/F9/F14虽有gold可评数据但答案留null。关键任务相关F8证据不足，属部分性状准确、关键项证据不足的5–6带，取5。

<details><summary>V0.4理由与本行变化背景</summary>

已填8项（F1/F6/F8/F10/F11/F12/F13/F15）：F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating与gold种级观测一致；F1“aerobic”与gold aerotolerant=true、facultative anaerobe=false方向一致但无直接需氧记录；F15栖息地广适性为未核实的一般性表述（gold F15=UNKNOWN）；F8把“经犬尿氨酸途径降解色氨酸至ACMS”写为物种广义降解能力，屬未核实能力声称，接近把路径推断当作物种性状。7项定量/身份性状（温度、pH、盐度、保藏号、碳源、酶活、基因组）为null明确未知，gold中多有物种级记录，完成度损失已主记D1，此处不重复重扣。档位5–6（部分性状准确但关键项证据不足），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_059：提供TaxID 294的OBSERVED性状（motility、cell shape、gram、sporulation等）；不含tryptophan降解记录
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_059：标明TaxID 294各性状observed/scoreable状态，用于区分完整性缺口与可评缺失

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> evidence_registry三条（EVID_001/002/003）source_type全为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，无法定位到任何条目；按MISSING_SOURCE规则属确实无引用/仅自我声明，低分档评定；这是来源缺失而非已核实错引，默认不cap。取2。

<details><summary>V0.4理由与本行变化背景</summary>

答案三条证据（EVID_001菌性状、EVID_002路线、EVID_003酶EC）全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，按四.3逐组登记MISSING_SOURCE——这是缺失而非误导，默认不触发cap；无任何已核实错引，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。可定位可核项仅身份层：交付TaxID 294经E0核实为P. fluorescens种级记录（与声称粒度一致，SUPPORTED），五步EC号与gold一致但E0无EC条目（UNRESOLVED，不判虚构）。因其餘决策相关组（路线、酶、菌、性状）结论整体不可追查，属“全部缺失”低分档；考虑身份条目实际可定位并已核实，取低分档上限3而非1–2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_059.answer.evidence_registry：证明答案仅交付INTERNAL_KNOWLEDGE_ONLY条目；不支持任何可定位来源

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 答案在uncertainties中明确列出“氧条件未指定、部分性状未提供具体数值、酶与菌种基于通用知识缺乏数据库直接记录”，对未知性状也标unknown，属诚实披露；但五步与全路径能力、F8降解声称仍以medium confidence呈现，未区分预测与观测，也未限定P. fluorescens能力范围，属“有不确定性说明但过于笼统、部分结论强度超过依据”的5–6带，取5。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties具体列出“氧条件未指定/部分性状无具体数值/酶与菌种基于通用知识、缺乏数据库直接记录”，并逐项给confidence标签，未知性状统一null+unknown，属诚实披露；未见把预测伪装成数据库直查的表述。不足：未核实的整条路径能力与步级归属仍统一标medium，F8能力表述接近观测口径，未对本答案最关键的“单一物种全路径能力未核”做点对点限制；属主要限制已说明但个别结论强度略超依据，档位7–8取7。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_059.answer.uncertainties：仅支持披露文本观察；不证明置信度与证据相称

</details>

## Kimi

答案SHA256：`74aaedd3bd3b3aa551d9c3172bc42d79036b6a011c0912380c256fb968960b27`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 答案完整交付了题面指定的5步主链，route_scope.chosen_route_name逐字保留题面路线名，氧条件按题面保留null；S1–S5均给出主底物/主产物英文名与SMILES、一个首选酶名/EC和一个对应微生物；两个“物种+菌株”profile去重且各自填齐15项性状。仅有个别性状值缺少可定位来源或置信度较低，属局部缺陷，不构成重要任务模块遗漏或路线偏离，故在9–10档取9。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的全部模块均实质交付：5步主链每步都给出主底物/主产物英文名与SMILES、首选酶+EC、对应微生物与organism_profile_id；两份profile各15项性状；evidence_registry 7条并逐条绑定claim_scope；uncertainties 4条。route_scope.chosen_route_name原样照抄题面路线名，未改选路线、未改氧条件（保留null并在notes说明实际依赖O2），无空模板照抄。局部缺陷（step3产物端未列NADP+/H2O、部分性状无来源）属内容层问题，已在D2/D4/D5分轴处理，不重复扣完整性。9档取低分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_059：gold formal case records ordered_step_count=5 and LINEAR_UNIQUE; used only to confirm the task&#x27;s five-step main-route scope, not to import gold as answer content.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_059：defines root Tryptophan and terminal 2-Azaniumyl-3-(3-oxoprop-1-enyl)but-2-enedioate; used to check route/endpoint task scope.
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：answer text contains five sequential steps, two deduplicated species+strain organism profiles, and 15 traits per profile; used as completeness locator.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 五步化学转化与gold主链一致：L-tryptophan→N-formyl-L-kynurenine→L-kynurenine→3-hydroxy-L-kynurenine→3-hydroxyanthranilate→2-amino-3-carboxymuconate semialdehyde；反应方向为底物到产物，关键开环、脱甲酰、羟化、裂解及终点连接连续。局部存在辅因子/副产物标注简化（如S3未列NADP+与水，S2/S4未列H+），按P103–P105属局部计量或简化表达，不改变主链结论；按本题程序D2上限为8，取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步一致：L-Trp+O2→N-甲酰-L-犬尿氨酸（吡咯环氧化开环）→水解去甲酰基生成L-犬尿氨酸+甲酸→KMO羟化生成3-羟基-L-犬尿氨酸→犬尿氨酸酶裂解生成3-羟基邻氨基苯甲酸+L-丙氨酸→3-HAA双加氧开环生成题面指定终点ACMS。方向、结构连通性、SMILES与终产物均与gold（BSY-r03862/r02255/r02091/r02023/r01725、终点BSY-c18177）吻合，符合四.2“止于题面终点即为完整交付”。扣分点：step3仅列O2/NADPH为底物，产物端未列NADP+/H2O，字面计量不完整，属八.辅因子条款的局部计量缺陷，按7–8档处理、不cap；鉴于仅此一处且其余辅因子（O2/H2O/NADPH、甲酸/L-丙氨酸副产物）均已列出，8档取高分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：gold reaction rows give the directed substrate-to-product participants and five-step chemistry; used to compare main-chain chemistry and continuity, not to require undisplayed branches.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：accepted enzyme names/ECs for the five target reactions; used at reaction-class level only, not as proof of specific protein experimental activity.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_059：defines the terminal ACMS product identity; used to check endpoint chemistry.
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：answer text provides the five-step chemistry and local cofactor omissions; used for D2 chemistry locator.

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 按JUDGE_REQUIRED审阅：答案五步酶名/EC与本题accepted sets逐项对应（S1 TDO 1.13.11.11↔S05；S2 formamidase 3.5.1.9↔S04；S3 KMO 1.14.13.9↔S03；S4 kynureninase 3.7.1.3↔S02；S5 3HA dioxygenase 1.13.11.6↔S01），目标催化对应充分；S01–S04结构表示等价边界仍待裁定，9–10证据门关闭，故在&#91;7,8&#93;取8。

<details><summary>V0.4理由与本行变化背景</summary>

五步酶名/EC与gold冻结酶表逐一对应：tryptophan 2,3-dioxygenase EC 1.13.11.11（gold该步为多注集合1.13.11.11|1.13.11.52，按四.5多注条款答案选集内号不扣）、kynurenine formamidase EC 3.5.1.9、kynurenine 3-monooxygenase EC 1.14.13.9、kynureninase EC 3.7.1.3、3-hydroxyanthranilate 3,4-dioxygenase EC 1.13.11.6。酶功能类型（heme双加氧/酰胺水解/FAD单加氧/PLP裂解/非血红素Fe(II)双加氧）与EC大类一致，无“名称为加氧酶而编号为脱氢酶”类矛盾。gene_or_protein（kynA/kynB/BNA4/BNA5/BNA1）与对应酶一致。E0无EC条目（GAP-059-002/003/004/006/007等），官方accepted name/reaction属局部待核，不影响本维整体可评。9档取中。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：Gold accepted enzyme names/EC per step; does not prove specific protein substrate specificity or experimental activity.
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.enzyme：Answer enzyme names/EC are being compared to accepted sets; representation alignment remains local pending.

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> S. cerevisiae S288c覆盖S3–S5，organism_gold对S. cerevisiae有species-level exact步骤支持且PATHWAY_COMPLETE为真，但未核实S288c菌株级；S1–S2使用P. aeruginosa PAO1，未出现在organism_gold，E0亦无该TaxID记录，答案仅以Kurnasov文献并以uncertainty承认其体内主走anthranilate支路。属合理候选+部分支持、关键微生物归属仍欠核验，取&#91;5,6&#93;上沿6；未核实不等于已证伪，key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

分轴判断：①S3–S5以Saccharomyces cerevisiae S288c为代表，与gold的酶-菌归属（S01/S02/S03/S04/S05均登记S. cerevisiae）一致，且gold PATHWAY_COMPLETE行登记S. cerevisiae（TaxID 4932）为本通路完整菌，答案“酵母含完整BNA途径”的整路径声称有gold物种级支持，未把单步菌写成整路径菌（complete_pathway_organism_profile_id只给ORG_002）；②S1–S2改用Pseudomonas aeruginosa PAO1（KynA/KynB），该菌不在gold本case菌表内——gold非穷尽，不据此判错，但E0亦无该菌反应级记录（GAP-059-039/040等），其反应级能力未核；答案已自述PAO1体内主要走anthranilate支路，属披露性限制，未过度外推；③TaxID 208964/559292为菌株级编号，E0无TaxID记录，无法按四.6核ScientificName/rank/lineage，按身份阶梯①/②的“粒度与支持范围待核”处理，不判cap。综合：主要菌（酵母）与gold一致、身份要素完整，但前两步代表菌与两个菌株级编号仍未充分核验，落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_059：Gold supports S. cerevisiae at species level for the five reactions and records pathway_complete TRUE for taxid 4932; does not verify S288c strain or P. aeruginosa PAO1.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 两个profile均一次给出15项性状，完整性好；但trait_scoreability_mask显示S. cerevisiae仅F14有observed_accuracy，P. aeruginosa PAO1无对应observed行，多数性状为completeness_only或INTERNAL_KNOWLEDGE_ONLY。部分基因组/保藏号数值具体且来源定位清楚，但关键性状整体仍缺可核验观测，取&#91;5,6&#93;上沿6；未核不判错。

<details><summary>V0.4理由与本行变化背景</summary>

两份profile各15项齐备，关键可核项基本正确且适用于所指对象：PAO1保藏号ATCC 15692、基因组NC_002516.2/6,264,403 bp/66.6% GC，S288c保藏号ATCC 204508、基因组GCA_000146045.2/12,157,105 bp/38.3% GC，均为该菌株的标准参考值；革兰氏阴性/不产芽孢/杆状/有鞭毛（PAO1）与无运动性/卵圆酵母/子囊孢子（S288c）等定性性状方向正确；温度最适37°C/30°C合理；F4盐度两项均以null明确未知（不冒充观测）。扣分点：F3 pH最适（7.0/5.0）无evidence_id且非null，违反“无来源填null”的交付纪律；部分性状仅INTERNAL_KNOWLEDGE_ONLY（EVID_007）低置信；E0对208964/559292的F14等子字段为EVIDENCE_GAP_TRAIT_SUBFIELD，无法逐值核验。无“预测冒充观测”“数值离谱到误导筛选”“物种级观测推广为全菌株性质”的情形。落7档（主要性状可核实且适用，少量条件/来源问题）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_059：Mask shows most traits completeness_only; only limited F14 observed_accuracy for S. cerevisiae and no P. aeruginosa rows.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_059：Subfield mask identifies only scattered scoreable observed scalars; range/multi-value and internal-only traits are not accuracy denominators.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案给每一步都挂了 reaction_evidence_id，并给酶/菌和大量性状填了 evidence_id；evidence_registry 也列了 source_type/database/locator/claim_scope，主链步骤和酶菌结论可沿 EVID_001–EVID_003 等条目核对。但关键条目质量不齐：EVID_001 仅是 MetaCyc pathway 名称且无 record_id，EVID_002/EVID_003/EVID_006 缺 DOI/PMID 或记录号，EVID_001/002/003/006 的定位粒度偏粗；更明显的是 S. cerevisiae 的 F2/F3/F6/F7/F10/F11/F12/F13/F15 等多项性状仅引 EVID_007=INTERNAL_KNOWLEDGE_ONLY，P. aeruginosa F8 亦为 internal，无法追到可定位文献/条目；个别性状引 EVID_003（NAD 代谢论文）支持范围过宽。因此属于“部分关键结论可定位并核对，其他模块仍缺映射或必要来源记录”的 5–6 档，给 6 分。未见已核实的 VERIFIED_MIS_CITATION_CRITICAL/SYSTEMIC，故不记 key_error=Y。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group合成：决策相关组CG01/CG02/CG03（路线）主要挂EVID_001（MetaCyc通路名，record_id=null，属通路级而非条目级稳定标识）与EVID_002；CG05（酶-EC）挂EVID_002/003/006；CG07（菌株身份）TaxID 208964/559292无专属来源，仅由步骤EVID_002/003间接背书；CG08步级菌归属同源；CG09整路径声称挂EVID_003/006。全部引用在E0中无核验记录（EC/TaxID/文献均列EVIDENCE_GAP），故一律UNRESOLVED_SOURCE，不判虚构、不判CONTRADICTED。但引用可定位到条目层级（3篇具体作者-年份-期刊-题名文献、BacDive记录DSM 22644、SGD参考株R64/GCA_000146045.2），非“仅库名/模型名”全笼统；CG12/CG13及部分性状为无来源或明确未知（MISSING_SOURCE），按缺失处理不cap。无经核实错引→不触发LOCAL/CRITICAL/SYSTEMIC。综合落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：列出本题各步已接受的酶名/EC，可用于核对答案所给酶与EC是否可对照；不证明答案所引 EVID_001–EVID_003 的文献具体支持每个酶/菌结论。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_059：说明官方性状切片对 S. cerevisiae 多数性状并无可用记录；因此答案以 INTERNAL_KNOWLEDGE_ONLY 填写的多项性状无法借该切片得到外部条目核验。不支持将其直接判为错引或虚构。
- SCOPE_ROW / SCOPE#BIOPATH150_059#CG14：标记底物利用性状在承担目标污染物能力论证时为 APPLICATION_CRITICAL；仅提供条件/关键性上下文，不提供具体性状来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确标注route_scope.oxygen_condition=null并说明实际为需氧过程；uncertainties列出P. aeruginosa anthranilate支路、S. cerevisiae代表性与部分性状缺源；各性状confidence多为medium/low/unknown，INTERNAL_KNOWLEDGE_ONLY用低置信。未见系统性把预测写成实证或掩盖主要矛盾。按披露具体、边界较清楚，取&#91;7,8&#93;上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界表述总体诚实具体：uncertainties&#91;0&#93;指出题面氧条件null但路线实际依赖O2（区分题面限制与路线性质）；&#91;1&#93;披露3–5步用真核代表、细菌同源途径证据较弱；&#91;2&#93;披露PAO1体内主走anthranilate支路、kynA/kynB属注释与体外证据；&#91;3&#93;说明盐度/最适pH缺源，已null或INTERNAL_KNOWLEDGE_ONLY低置信。confidence分级与依据大体相称（酶与文献支撑为high，内部知识为low/unknown），未把预测写成实证，未掩盖替代支路（另列两条is_part_of_scored_main_route=false的分支）。扣分点：F3 pH最适与部分性状在无来源情况下给出数值（仅以low标注），个别基因组/保藏号以high/medium包装而E0不可核，属单点过度确信而非系统性误导（不cap）。8档取中。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties/confidence：Answer&#x27;s own uncertainty and confidence labels are evaluated for disclosure quality; not external truth.

</details>

## Qwen

答案SHA256：`41c0f016ad163b1fdcb63b4632015f9816313422d8426b8ca3dd1f7a755611c8`。

### D1 完整性与任务符合度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> JSON完整；路线名原样照填，5步均给出底物、产物、酶和对应微生物，15项性状字段齐全。10项有值、5项明确unknown/null（温度、pH、盐度、保藏、基因组），且未给菌株，完整性虽良好但未达9–10。按7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

全部必答模块均实质交付：5步主链每步给出主底物/主产物英文名与SMILES、一个首选酶+EC、一个对应菌；15项性状齐备（10项填写、5项null且confidence=unknown，按明确未知登记，不计为遗漏）；route_scope.chosen_route_name逐字照抄题面指定路线名，未改选路线；单菌按物种去重为一条profile，符合格式要求。扣分点：5项性状（温度/pH/盐度/保藏/基因组）在gold中本有可参照记录却留空，NADPH/NADP+辅因子SMILES为null，菌未给株级身份、酶未给gene/protein标识；属少量遗漏与字段级缺陷，未达7档以下。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 主链与gold五步一致：L-Trp→N-formyl-L-kynurenine→L-kynurenine→3-hydroxy-L-kynurenine→3-hydroxyanthranilate+L-alanine→2-amino-3-carboxymuconate semialdehyde；方向、结构、连接正确，O2/NADPH/H2O等主要辅因子在列。S2/S4未写H+，且四步与gold有电荷表示差异，属局部表示/计量问题，不改变主链结论。按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐行等价：S1 L-tryptophan+O2→N-formyl-L-kynurenine（双加氧，方向forward）、S2→L-kynurenine+formate（水解）、S3 L-kynurenine+O2+NADPH+H+→3-hydroxy-L-kynurenine+NADP++H2O（单加氧，辅因子完整）、S4→3-hydroxyanthranilate+L-alanine（水解裂解）、S5+O2→2-amino-3-carboxymuconate semialdehyde（双加氧）；止于题面指定终点，无无依据跳步、无方向反转、无原子明显不守恒。残留缺陷仅为局部计量/字段级：S2未列H+、NADPH/NADP+的SMILES为null（答案自述并在uncertainties披露），按八.辅因子与简化反应式条款留在9档内，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：支持五步主链的反应方向、主产物与步骤连接；不支持具体菌株能力或答案来源交付。

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 五步酶名/EC分别对应accepted S05/S04/S03/S02/S01：tryptophan 2,3-dioxygenase EC 1.13.11.11、formamidase EC 3.5.1.9、kynurenine 3-monooxygenase EC 1.14.13.9、kynureninase EC 3.7.1.3、3-hydroxyanthranilate 3,4-dioxygenase EC 1.13.11.6；EC与accepted集合精确匹配。四步程序仍ROUTE_HOLD_REPRESENTATION，故不满足9–10正式门；按功能层给8。

<details><summary>V0.4理由与本行变化背景</summary>

五步酶-EC与gold步级酶表逐一吻合：tryptophan 2,3-dioxygenase 1.13.11.11、formamidase(arylformamidase) 3.5.1.9、kynurenine 3-monooxygenase 1.14.13.9、kynureninase 3.7.1.3、3-hydroxyanthranilate 3,4-dioxygenase 1.13.11.6；酶名与反应类型（双加氧/水解/单加氧/裂解/双加氧）自洽，未出现EC大类别与反应类型不匹配。gold在tryptophan dioxygenase步为多注1.13.11.11|1.13.11.52，答案取集合内编号，按四.5保守条款不扣分。未进入9–10档的原因：未给gene/protein或序列标识，且五步EC在E0无冻结条目记录（仅gold步级映射可核），官方accepted name/reaction核验待补；支持性质为内部知识（INTERNAL_KNOWLEDGE_ONLY），故按7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：支持各目标反应的accepted酶名/EC范围；不支持具体蛋白底物谱或实验活性。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Pseudomonas fluorescens TaxID 294身份可核；但仅终端S01有organism_gold步级记录，S1–S4的P. fluorescens催化归属均无适用冻结记录。答案又将P. fluorescens标为complete_pathway ORG_001，gold PATHWAY_COMPLETE未列该菌，但gold非穷尽，不能判假。属合理候选+部分支持、若干关键步级与全路径能力未充分核验，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

身份层正确、能力层未核，落在5–6档（有合理候选和部分支持，但关键身份作用范围未充分核验），档内取5：①菌名与TaxID 294经E0核实为Pseudomonas fluorescens（种级名-身份对应SUPPORTED），无身份编造；②但S1–S5五步全部归属同一菌，并设complete_pathway_organism_profile_id=ORG_001，构成“全路径能力”与步级催化归属的实质声称，其唯一来源为INTERNAL_KNOWLEDGE_ONLY、confidence=low；③gold organism_gold对S02–S05列出的是其他菌（S. cerevisiae/C. metallidurans/S. parvulus/D. acidovorans等），但该表由酶源行衍生、非穷尽菌谱，不能据此判P. fluorescens不能催化；④E0对CG08（步级归属）与CG09（全路径能力）均登记UNRESOLVED，冻结证据既不能证实也不能推翻，按“疑似但证据不足”处理：key_error=UNRESOLVED、不cap；⑤答案主动写明“微生物归属证据强度有限”，属如实披露，不足以弥补粒度与能力外推的缺口。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：支持TaxID 294官方对应Pseudomonas fluorescens、rank=species；不支持任何步级催化或全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_059：列示各步参考菌；P. fluorescens仅出现在S01终端步，PATHWAY_COMPLETE行未列P. fluorescens（非穷尽）。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 10/15性状有值；F10运动、F11杆状、F12革兰氏阴性、F13不产孢有trait_gold支持。F7色氨酸作碳源、F8广谱降解、F9五步酶活、F15广栖息地及F1/F6氧相关主要为内部知识或未核；温度、pH、盐度、保藏、基因组关键项为null。部分性状准确且适用，但关键证据不足，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

已填10项性状中，低权重表型项与gold观测一致：F10“有鞭毛，能运动”(motility=true)、F11“杆状”(cell shape=rod-shaped)、F12“革兰氏阴性”(gram positive=false)、F13“不产孢”(sporulation=false)、F1“好氧”(aerotolerant=true，粗粒度相符)；F6“有氧呼吸/末端受体氧”与gold呼吸/反硝化观测不矛盾但无直接条目。关键项（任务用途相关）证据不足：F9把路径五酶整体写成该菌酶活、F7把“色氨酸作碳源”写成一般性状、F8“可降解色氨酸等芳香族氨基酸”、F15“土壤/水体/根际广布”均无来源，且F7/F8/F9属由路径预测向菌株能力的反向外推（四.4/D4条款禁止的“预测冒充观测”式表述，虽已标low confidence）；F2/F3/F4/F5/F14留空。按性状重要度加权（而非填写比例），落在“部分性状准确且适用，但关键项证据不足”档，无与gold相矛盾的数值，档内取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_059：支持P. fluorescens运动、杆状、革兰氏阴性、不产孢等观测；不支持未给出的温度/pH/盐度、色氨酸碳源、五步酶活等具体声称。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> EVID_001与EVID_002均为INTERNAL_KNOWLEDGE_ONLY，无database、record_id、locator或raw_text；决策相关路线/酶/菌/性状均无法沿外部条目或计算记录核查。无已核实错引，不触发D5 cap。属MISSING_SOURCE低档；有局部evidence_id映射，取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

答案只交付两条evidence_registry条目（EVID_001、EVID_002），source_type均为INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator全为null，仅有自我声明的claim_scope清单，无法定位到任何文献、数据库条目或计算记录——按四.3属MISSING_SOURCE（“完全无引用，或仅有INTERNAL_KNOWLEDGE_ONLY类自我声明”）。决策相关组（CORE的CG01/CG02/CG03/CG05/CG07与APPLICATION_CRITICAL的CG08、CORE的CG09）全部缺失，按P41“全部缺失→低分档（默认不cap）”定档；本单元不存在已核实错引（唯一编号类声称TaxID 294经E0核实SUPPORTED），故不触发cap、severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。低分档内取2而非1：答案至少给出了claim_scope级映射并自标low confidence，可看出每条结论依赖哪条自我声明，但仍无任何可定位来源。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确标注内部知识、低置信、氧条件未指定、部分辅因子SMILES不完整、终产物SMILES为结构推断，5项未知性状置null；未系统把预测写成实证。个别全路径/酶活声称仍有低置信和限制说明覆盖，按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体诚实且具体：全文confidence取low/unknown，evidence source_type自标INTERNAL_KNOWLEDGE_ONLY（未冒充数据库直查），uncertainties列出4条实质限制（氧条件未指定；微生物归属与性状缺外部证据、主要按内部知识低置信填写；部分辅因子SMILES未完整；终产物SMILES为结构推断），并在每步uncertainty重复提示菌归属证据有限——未见把预测系统性写成实证观测、未见掩盖已知矛盾。扣分点：F7/F8/F9与complete_pathway_organism_profile_id仍以断言式value文本表述能力（强度略超“内部知识”依据），属个别结论强度超证据而非系统性误导，按8.D6单点过度确信/披露不完美处理在7档，不cap。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`9526dc25b181473193641dc7955bb5fef690a9d7ce3e58041120cb2fa8d401b1`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出完整五步主链、题面指定路线名、终点、每步主底物/产物、首选酶与EC、对应微生物，并返回15项性状；额外分支明确标为非评分主链。未见必要模块缺失或任务范围偏离，仅存在待复核的representation/base-range标记，故置于9-10带下沿。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_059：确认题面路线名、起点Tryptophan与终点2-aminomuconate semialdehyde，不替代答案正确性判断。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_059：确认该案为LINEAR_UNIQUE、ordered_step_count=5，支持完整性分母按五步主链核验。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链为经典犬尿氨酸/BNA途径：Trp→N-formyl-L-kynurenine→L-kynurenine→3-hydroxy-L-kynurenine→3-hydroxyanthranilate→ACMS。五步方向、主产物、O2/NADPH/H2O等辅因子与反应连接和gold reaction切片一致；仅SMILES电荷/立体表示有轻微表达问题，不改变主链化学。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：支持五步主链的底物/产物、方向和反应连接；不证明答案的具体蛋白或菌株实验活性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_059：支持路线起点与指定终点结构身份，不扩展到未声称的下游。

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的五个酶/EC与accepted sets逐项对应：S1 tryptophan 2,3-dioxygenase EC 1.13.11.11（gold S05）；S2 kynurenine formamidase EC 3.5.1.9（S04）；S3 kynurenine 3-monooxygenase EC 1.14.13.9（S03）；S4 kynureninase EC 3.7.1.3（S02）；S5 3-hydroxyanthranilate 3,4-dioxygenase EC 1.13.11.6（S01）。程序矩阵对S01-S04仍为UNKNOWN/UNRESOLVED（charge/stereo representation），但名称与显式EC已由accepted sets支持；剩余基因归属BNA1/BNA2/BNA4/BNA5为MINOR U。无已确认KEY失败，9-10受representation/high-tier门限制，故取7-8带上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：支持五步相应酶名/EC与gold/accepted集合对应；不证明具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：支持每步反应方向与底物/产物对应；不自动核验具体基因归属。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S5&#93;.enzyme：定位答案实际交付的酶名、EC与基因字段；答案自述不等于已核验。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 五步均使用Saccharomyces cerevisiae S288C，与organism_gold中五步的S. cerevisiae物种级记录及PATHWAY_COMPLETE 4932行一致；但答案交付菌株级TaxID 559292，E0无该TaxID记录，菌株级身份和全路径能力只由物种级记录支持，属粒度不足，按身份阶梯通常7档附近且不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_059：支持五步均有S. cerevisiae物种级记录及4932的PATHWAY_COMPLETE；不支持S288C/559292菌株级身份或菌株级能力。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;：定位答案交付的菌名、菌株、TaxID与complete_pathway_organism_profile_id；答案自述不等于已核验。

</details>

### D4 性状科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段全部返回，F3 pH以null+unknown如实表示，其余温度、氧、盐度、保藏、呼吸、碳源、酶活、运动、形态、革兰、产孢、基因组和栖息地均有值；这些与S. cerevisiae/S288C常见性状总体相符。但trait_gold对4932多数性状为UNKNOWN，F14仅支持TaxID层面，S288C菌株级性状多未在E0核验，故按7-8带取8而非9-10。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_059：支持4932的F14 TaxID观测及多数性状为UNKNOWN；不能把UNKNOWN反推为答案错误，也不支持S288C菌株级全部性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_059：显示4932多数性状为completeness_only、F14为observed_accuracy；用于区分完整性与可核验准确性。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_059：显示4932各性状子字段没有可评分观测值；不把未核验当作错误。

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的evidence_registry六条均为INTERNAL_KNOWLEDGE_ONLY；虽给出KEGG map00380、SGD BNA pathway、NCBI 4932、ATCC 204508、GCF_000146045.2等名称/编号，但未交付可定位外部条目、DOI/URL或条目内容核验。decision-relevant的路线/酶/身份组因此均为MISSING_SOURCE，属3-4低档；无已核实错引，不cap，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示所有证据条目source_type=INTERNAL_KNOWLEDGE_ONLY；不能作为已交付外部来源或已核验引用。

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案列出了EC替代号、未填基因符号、其他菌株证据不足、立体化学未指定、null未用近似值等具体不确定性，且F3 pH明确unknown；但同时把大量仅INTERNAL_KNOWLEDGE_ONLY支持的酶/性状标为high/medium，未在正文中清楚区分观测、内部知识与预测。属部分披露但结论强度局部超过依据，按5-6带取6，非系统性误导，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：定位答案实际披露的限制与未知；不证明其全部置信标签与证据强度相称。
- ANSWER_TEXT / ANSWER.evidence_registry：显示来源类型为内部知识；用于判断预测/推断/观测是否清楚区分，不把缺失当虚构。

</details>

## GPT5.6

答案SHA256：`79263b7283ff93edc6179705632df48a13f87ca4e58cf6bb21636b25bb8845e0`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面指定路线名已原样填写；5步均给出主底物/主产物名称与SMILES、首选酶名+EC、对应微生物，且同一菌去重为一个organism_profile。主要缺陷是15项性状全部为null/unknown，仅占位，未实质完成性状模块；按D1 5–6档（主要模块涉及但必要内容仅占位/遗漏）取5，因全性状模块缺失不属于少量遗漏。科学正确性另归D2。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：题面要求指定路线主链、每步主底物/主产物英文名及SMILES、一个首选酶及EC、一个对应微生物，并填写15项性状及来源；不确定项可null。
- ANSWER_TEXT / ANSWER.route_scope：chosen_route_name逐字为L-tryptophan degradation to 2-amino-3-carboxymuconate semialdehyde。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S5&#93;：5步均含substrates/products的name+smiles、enzyme.name+ec_number、microorganism；覆盖路径、酶、菌三个模块。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：15项性状全部为value:null/confidence:unknown，没有任何已填写性状值或来源，仅登记为未知。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_059：本题为LINEAR_UNIQUE，ordered_step_count=5，n_required=5；用于核对题面要求的必答主链规模，不作为旁支缺步分母。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_059：本题确有15项性状字段集合；该表说明部分字段可评分/部分仅完整性，不改变答案全部null导致性状模块未实质完成的事实。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链顺序与方向整体对应该case的5步kynurenine路径，终点名称正确；但关键中间体结构有实质问题：S1产物SMILES把甲酰基放在α-氨基上，而gold的N&#x27;-formylkynurenine是在芳环氨基上成甲酰；S3产物SMILES的羟基位置与3-hydroxy-L-kynurenine不符，S4又使用同一S3底物却生成3-hydroxyanthranilate，形成中间体结构不一致；O2、NADPH、H2O及formate/alanine等辅因子/副产物未列。主链仍可辨认，属5–6档“主干部分成立，但关键中间体/连接需实质修订”，因多处关键中间体问题取5；未达cap≤4，key_error=N。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_059：冻结gold给出5步主链的底物/主产物及方向：S05 tryptophan→N&#x27;-formylkynurenine；S04 N&#x27;-formylkynurenine→L-kynurenine+formate；S03 L-kynurenine→3-hydroxy-L-kynurenine（含O2/NADPH）；S02 3-hydroxy-L-kynurenine→3-hydroxyanthranilate+L-alanine；S01 3-hydroxyanthranilate+O2→2-amino-3-carboxymuconate semialdehyde。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_059：题面终点化合物2-amino-3-carboxymuconate semialdehyde对应gold terminal compound 2-Azaniumyl-3-(3-oxoprop-1-enyl)but-2-enedioate。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S5&#93;.substrates/products.smiles：答案S1产物SMILES为α-N-甲酰异构体，不是gold N&#x27;-formylkynurenine；S3产物SMILES的芳环羟基位置与3-hydroxy-L-kynurenine不符；S4沿用同一S3底物却给出3-hydroxyanthranilate，结构连续性不一致；各步未列O2/NADPH/H2O/formate/alanine。
- ANSWER_TEXT / ANSWER.route_summary：答案自述为kynurenine pathway主链，方向为降解至指定终点，可用于核对主链方向；不取代结构核验。

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按反应而非位置step_id映射：S1 TDO EC1.13.11.11对应gold S05，S2 formamidase EC3.5.1.9对应S04，S3 kynurenine 3-monooxygenase EC1.14.13.9对应S03，S4 kynureninase名称对应S02，S5 3-hydroxyanthranilate 3,4-dioxygenase EC1.13.11.6对应S01。四步名称/EC与accepted一致，主催化对应可靠；S4显式EC 4.2.1.21与accepted kynureninase EC 3.7.1.3未对齐，是局部配对问题，阻止9–10但不使整维NE。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_059：支持各目标反应的accepted酶名/EC集合；不证明具体蛋白底物谱或实验活性。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Pseudomonas fluorescens为真实物种，E0 TaxID 294支持种级身份；但答案未给菌株、TaxID或证据，却把同一物种用于全部五步并设置complete_pathway_organism_profile_id=ORG_001。种级身份有支持，单步反应能力与全路径能力未核，故为部分支持5分，不判身份错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：支持Pseudomonas fluorescens种级身份；不支持菌株身份、单步催化或整条路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_059：gold列出部分步骤的菌种关联和全路径菌；gold非穷尽，不能自动否定未列出的P. fluorescens全路径能力。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段均存在但所有value均为null/空，属全部必需性状null/空值；按P44该模块D4记MISSING=1，不宣称检测到科学错误。

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry五条均为INTERNAL_KNOWLEDGE_ONLY，database/record/locator均为null；按六状态属MISSING_SOURCE。虽本地EVID_00x可把声称与局部ID关联，但无法定位到外部条目或原文，D5低分1–2档取2；无已核实错引，不cap。

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> uncertainties明确写出氧条件未指定、微生物仅种级低置信、SMILES/终产物表示可能有差异；各酶confidence多为medium、菌为low、性状unknown，未把内部知识包装成实验观测。轻微问题是内部知识来源却给酶medium置信，但总体披露与边界清楚，按7–8档取8。
