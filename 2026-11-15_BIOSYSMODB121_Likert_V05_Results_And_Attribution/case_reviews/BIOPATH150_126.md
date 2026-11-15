# BIOPATH150_126：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：butane degradation

污染物：Butane；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 44 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 59.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 64.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 54 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 72 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 60 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`567099291d8cac09ddb0d215ed05478de1bfbab12463ab99dbec81ae2b82594d`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> SCORED within D1 allowed range &#91;1,4&#93; because the program route diagnosis marks DEVIATES. The JSON is complete and readable, with steps, enzymes, one organism profile and all 15 trait fields present. However the delivered main chain is a subterminal 2-butanol/2-butanone/ethyl acetate route rather than the gold butane→1-butanol→butanal→butyrate chain, so this is a central task-route deviation rather than a minor format defect.

<details><summary>V0.4理由与本行变化背景</summary>

覆盖路径(7步)、每步酶与微生物、15项性状字段与uncertainties模块均实质交付；chosen_route_name按题面原样填butane degradation，未改选路线名；部分EC与多数定量性状为诚实null(信息不足非遗漏)；未发现重大范围或格式偏离，故取8档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：Gold S01/S02 directed reactions show butane→1-butanol and 1-butanol→butyraldehyde; does not support the answer&#x27;s 2-butanol route.
- ANSWER_TEXT / ANSWER：Answer route_summary and steps show a complete but different 2-butanol/2-butanone route.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> SCORED at the upper end of D2 allowed range &#91;1,6&#93;. The alternative subterminal route is chemically coherent and mostly continuous: butane→2-butanol→2-butanone→ethyl acetate→ethanol+acetate→acetaldehyde→acetate→acetyl-CoA, with cofactors generally represented. It is a valid chemical substitution but not the gold route, so D2 cannot enter the 7-10 band; no confirmed internal chemical contradiction was found.

<details><summary>V0.4理由与本行变化背景</summary>

亚末端氧化主链(丁烷→2-丁醇→2-丁酮→乙酸乙酯→乙醇+乙酸→乙醛→乙酸→乙酰辅酶A)各步方向、碳数守恒与连接自洽，未见明显化学错误；但整条路线属于与gold末端氧化(→丁酸)不同的替代路线，且S3 BVMO生成乙酸乙酯为推定步骤、答案无任何可定位证据支撑，按四.5“合理替代路线无证据→登记未证实、不给高分”落入5–6档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：Provides the gold directed route for comparison; does not establish the answer&#x27;s alternative route as task-correct.
- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s step chemistry and continuity.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> SCORED within D3a release range &#91;1,4&#93;. Fixed counts are S=0, F=2, U=2; confirmed KEY entry failure at S02. The answer supplies no gold target reaction and instead gives a different butane activation product (2-butanol) and downstream route. Some local butane-monooxygenase-like chemistry is present, so score 2 rather than 1, but the core target recommendations fail and the confirmed KEY failure caps the dimension.

<details><summary>V0.4理由与本行变化背景</summary>

S4–S7酶名与EC类别匹配(羧酸酯酶3.1.1.1、醇脱氢酶1.1.1.1、醛脱氢酶1.2.1.3、乙酰辅酶A合成酶6.2.1.1)，未见名称与EC矛盾；S1–S3(丁烷单加氧酶/仲醇脱氢酶/BVMO)为合理候选但均无EC、无基因/蛋白标识、无可核证据，若干关键步骤缺具体核验，落5–6档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_126：Gold S02 lists soluble butane monooxygenase EC 1.14.13.230 for butane→1-butanol; does not support butane→2-butanol.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：Gold directed reactions define S01-S04 target substrate/product pairs.
- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s delivered enzyme/reaction pairs.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> SCORED in the partial band. The answer gives one species-level candidate, Pseudomonas butanovora, for all steps and claims complete-pathway capability via ORG_001. Gold gives Thauera butanivorans (TaxID 86174) with pathway_complete TRUE. P. butanovora may be an old synonym, but that synonymy and the answer&#x27;s route-specific whole-pathway capability are not verified in the provided E0/crosswalk; no strain or TaxID is supplied. Reasonable candidate but key identity/capability remains unverified, so 5.

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份&#x27;Pseudomonas butanovora&#x27;即gold所用Thauera butanivorans的旧名同物，答案亦自陈可能重分类，物种层面身份基本正确；gold PATHWAY_COMPLETE=TRUE支持该菌具完整丁烷降解能力；但未给菌株/TaxID，且S3 BVMO等分步催化归属无独立证据，落5–6档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_126：Gold organism is Thauera butanivorans TaxID 86174 with pathway_complete TRUE; does not automatically verify P. butanovora synonymy or the answer&#x27;s route.
- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s organism identity and complete-pathway claim.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> SCORED in the partial band. All 15 trait fields are present: 8 filled and 7 explicit unknown, with no omitted fields. Gold supports rod-shaped morphology, Gram-negative, and non-sporulating; those match. Other filled traits (oxygen tolerance, O2 respiration, butane/intermediate carbon source, TCE/MTBE co-metabolism, BMO activity) are internal only and not verified. Key observed traits such as motility and genome size are left null. Partial accuracy/applicability with key evidence gaps fits 5.

<details><summary>V0.4理由与本行变化背景</summary>

定性性状(杆状、革兰氏阴性、不产芽孢、好氧、醇脱氢酶EC1.1.1.1活性)与gold观察记录一致；但温/pH/盐度/基因组等定量性状全为null(信息不足，主归D1)，F7底物谱与F8 TCE/MTBE共代谢为无定位证据的较宽声称，部分关键项证据不足，落5–6档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_126：Provides observed/predicted trait rows for Thauera butanivorans; supports some morphology/Gram/sporulation comparisons and shows other fields are null in the answer.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_126：Marks which trait subfields are observed-accuracy versus completeness-only; does not make predicted background values observed facts.
- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s filled and null trait values.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> SCORED low. The answer&#x27;s evidence_registry labels EVID_001-EVID_008 as INTERNAL_KNOWLEDGE_ONLY, with database, record_id and locator null. That is MISSING_SOURCE under the rubric, not a verified mis-citation. No key conclusion can be traced to a locatable literature or database record. Score 2 because evidence labels and uncertainty exist, but there is essentially no traceable source.

<details><summary>V0.4理由与本行变化背景</summary>

全部evidence_registry条目source_type=INTERNAL_KNOWLEDGE_ONLY，无DOI/数据库条目/计算记录等可定位来源，无任一claim可沿记录核到外部条目；属MISSING_SOURCE情形，按低分档评定、默认不cap；无经核实错引，severity=NOT_APPLICABLE。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all evidence entries are INTERNAL_KNOWLEDGE_ONLY with null database/record/locator.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> SCORED in the good band. The answer explicitly marks many unknowns and limitations: null ECs, null strain/TaxID, uncertain synonymy, unverified trait values, and a separate uncertainties list. It distinguishes internal knowledge from observations reasonably well. It still uses medium confidence for route steps without locatable sources and makes some broad statements such as literature-supported aerobic route, so 7 rather than 8.

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties逐条给出(氧条件null但路线需氧、分类归属可能改为Thauera、EC/基因未核实、S5–S7通用酶、多数性状null)，未知以null诚实标注，观测/推断/未知大体区分；但将仅内部知识的S7乙酰辅酶A合成酶标high、多个内部知识标medium，局部置信与证据不完全相称，档内扣分至7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s explicit uncertainty and confidence labeling.

</details>

## DeepSeek

答案SHA256：`df33f7034d0d3dc075edc7ddbf602977127422356c50f0e69ae94f9b3031c574`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> All main modules are delivered: route_scope, eight steps with substrates/products/SMILES, enzyme and microorganism fields, all 15 trait slots, evidence registry, and uncertainties. One enzyme EC is null, five traits are explicit unknown, and sources are internal-only, but those are permitted or mainly D5 issues. Extra downstream beta-oxidation steps do not create a required-step omission. 7-8 band; score 8 for near-complete fields with minor null/source limitations.

<details><summary>V0.4理由与本行变化背景</summary>

8档：六模块（路线、酶、微生物、性状、来源、不确定性）均有实质交付，route_scope.chosen_route_name原样为butane degradation；15项性状齐全（10填、5未知、0遗漏），JSON完整可解析。少量遗漏：S1酶EC为null、ncbi_taxid为null、温度/pH/盐度/基因组/栖息地5项null；均属诚实未知而非占位。大部分必要内容完整、关联清楚，仅少量遗漏，定8档取中。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：Requires main route with per-step substrate/product/SMILES, enzyme/EC, microorganism, 15 traits and strongest source.
- ANSWER_TEXT / ANSWER.steps/organism_profiles/evidence_registry：Shows delivered fields, null EC at S1, and explicit unknown trait slots.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The main route butane-&gt;1-butanol-&gt;butanal-&gt;butyrate and the downstream beta-oxidation to acetyl-CoA are chemically continuous and directionally consistent. Substrate/product SMILES generally match; the butyrate neutral-acid vs anion difference is charge-notation only. Cofactors are omitted and not required by the task, so this is a local stoichiometric/representation limitation. 7-8 band; score 8 for correct main chain with local cofactor/charge omissions.

<details><summary>V0.4理由与本行变化背景</summary>

8档：butane→1-butanol→butanal→butyrate核心段转化方向、结构与gold化学一致（SMILES正确、连续、原子守恒），随后β-氧化至acetyl-CoA为教科书标准化学且逐级连接合理；全链辅因子（O2/NADH/FAD/CoA/ATP）未列，属主有机物转化正确而辅因子遗漏的局部计量缺陷（辅因子条款7–8档，不cap）；答案超出gold终点butyrate延续至acetyl-CoA，题面未显式指定终点，按P28/P29不作覆盖率扣分。主链及关键转化有充分依据，少量局部问题不改主要结论。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：Shows gold S02 butane-&gt;1-butanol, S01/S04 1-butanol-&gt;butanal, S03 butanal-&gt;butyrate, with redox carriers and oxygen/NADH cofactors.
- ANSWER_TEXT / ANSWER.steps S1-S8：Shows answer pathway and omitted cofactors/charge notation.

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> The answer follows the recognized butane-&gt;1-butanol-&gt;butanal-&gt;butyrate branch (S02-S01-S03) with plausible enzyme families, but target enzyme correspondence is not confirmed at accepted granularity: S02 has no EC and only a generic butane monooxygenase name; S01 uses EC 1.1.1.1 versus accepted 1.1.2.9/1.1.5.11; S03 uses EC 1.2.1.3 versus accepted butanal monooxygenase EC 1.14.13; S03 representation is charge-blind held. No target enzyme correspondence is confirmed as S. 3-4 band; score 4 for clear main transformations but limited/nonaccepted enzyme support and key unresolved acceptance.

<details><summary>V0.4理由与本行变化背景</summary>

6档：各步酶的功能类别与所指反应基本匹配（丁烷单加氧酶、醇/醛脱氢、butyrate-CoA连接、酰基CoA脱氢、烯酰CoA水合、3-羟酰CoA脱氢、硫解酶），但E0为EVIDENCE_GAP，7个EC号均无冻结记录核验；S2用EC1.1.1.1、S3用EC1.2.1.3，与gold指定1-丁醇脱氢酶(1.1.2.9/1.1.5.11)、丁醛单加氧酶(1.14.13)不同，属gold多注集合外号，须核官方条目→UNRESOLVED（不判错、不cap）；S1 EC为null属诚实未知。合理候选+部分支持、若干关键步骤缺具体核验，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_126：Gold accepted enzymes include soluble butane monooxygenase EC 1.14.13.230 for S02, 1-butanol dehydrogenase EC 1.1.2.9/1.1.5.11 for S01/S04, and butanal monooxygenase EC 1.14.13 for S03.
- ANSWER_TEXT / ANSWER.steps S1-S3 enzyme fields：Answer gives generic butane monooxygenase with null EC, alcohol dehydrogenase EC 1.1.1.1, and aldehyde dehydrogenase EC 1.2.1.3.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> The answer uses one organism, Pseudomonas butanovora ATCC 43655, consistently for all steps and claims a complete-pathway profile. Gold uses Thauera butanivorans TaxID 86174; the names are plausibly synonyms and the strain token is plausible, but no frozen crosswalk/E0 record confirms the synonym or TaxID, and ncbi_taxid is null (allowed). Identity is consistent and not confirmed cross-genus; 7-8 band; score 7 pending synonym/TaxID confirmation.

<details><summary>V0.4理由与本行变化背景</summary>

6档：核心菌Pseudomonas butanovora ATCC 43655为经典丁烷降解菌，单步丁烷单加氧酶能力有合理依据；但E0 gap无身份记录核验、ncbi_taxid为null，且与gold规范化名Thauera butanivorans(TaxID 86174)疑为同物异名(basonym)，冻结verified_species_name_crosswalk未含该映射；complete_pathway_organism_profile_id=ORG_001把整条路径能力归于单一菌未限定作用范围。合理候选+部分支持，关键身份与整条路径能力未充分核验，5–6档取6（不cap：未核实身份错配，非编造）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_126：Gold step and PATHWAY_COMPLETE organism is Thauera butanivorans TaxID 86174; does not by itself confirm the Pseudomonas butanovora synonym.
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism：Answer claims Pseudomonas butanovora ATCC 43655 for all steps and complete pathway.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Basic phenotypes (Gram-negative, rod-shaped, non-sporulating, motile) align broadly with gold. However key quantitative traits temperature, pH, salinity, and genome are null/unknown despite gold observed values, and F6 oxygen respiration, F7/F8 short-chain alkane utilization, and F10 polar flagella are internal-knowledge or genus-level extrapolations. 5-6 band; score 5 for partial accurate traits with key gaps and overbroad claims.

<details><summary>V0.4理由与本行变化背景</summary>

6档：已填性状中方向与gold代表物种记录一致的（F10 presence of motility=true、F11 rod-shaped、F12 gram negative、F13 sporulation=false）可对上，F1&#x27;aerobic&#x27;与gold&#x27;aerotolerant&#x27;相近；但温度/pH/盐度/基因组/栖息地5项为null，关键培养条件缺口大；F6末端受体写oxygen，而gold对同种仅有预测性硝酸盐呼吸/反硝化（predicted background, scoreable=FALSE，仅作提示不作准确度分母）。已填性状多为内部知识medium/high置信、缺外部核验。部分性状准确且适用但关键项证据不足，5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_126：Gold contains observed temperature min/max, salinity min/max, genome size/GC, rod-shaped, Gram-negative, motility, and predicted nitrate/denitrification rows for Thauera butanivorans.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_126：Shows which trait subfields are scoreable versus completeness-only in the frozen trait reference.
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：Shows answer trait values, nulls, and internal evidence links.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> All decision-relevant claims (route, enzymes, organism, traits) point only to EVID_001-EVID_005, all source_type INTERNAL_KNOWLEDGE_ONLY with null database, record_id, and locator. This is MISSING_SOURCE under D5; no verified mis-citation is present. 1-2 band; score 2 for structured claim mapping but no locatable external source.

<details><summary>V0.4理由与本行变化背景</summary>

2档：evidence_registry五条全部source_type=INTERNAL_KNOWLEDGE_ONLY，无任何可定位外部条目/文献/计算记录；决策相关组（路线、酶-EC、菌株身份、底物利用等）整体为MISSING_SOURCE。按六状态合成规则MISSING_SOURCE属低分档、为缺失而非误导、默认不cap；虽有自洽的内部claim映射，但不构成可追溯，1–2档取2。key_error=N（缺失非虚构，E0无已核实错引，不cap）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows all five evidence entries are internal-only with no external locator or record identifier.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer labels evidence source_type as INTERNAL_KNOWLEDGE_ONLY and lists several uncertainties/null traits, which supports D6. But it assigns medium/high confidence to internal-only pathway, organism, and several traits, and does not discuss key limitations or conflicts such as enzyme EC nonmatches, organism synonym uncertainty, and missing quantitative traits. 5-6 band; score 6 for explicit unknowns and source-type labels, not higher due overconfidence and missing conflict discussion.

<details><summary>V0.4理由与本行变化背景</summary>

6档：已用INTERNAL_KNOWLEDGE_ONLY如实标注来源性质，uncertainties显式列出EC未定、TaxID/基因组未定、培养条件未定，未知项填null，F1氧需求标medium、F10运动性标low；但多项内部知识型结论给medium/high置信（F12/F13为high），complete-pathway主张未加范围限定，β-氧化延伸未标注为推断，缺替代路线与冲突讨论。不确定性有说明但部分结论强度超过依据，5–6档取6（单点过度确信，非系统性误导，不cap）。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties and confidence labels：Shows disclosed unknown EC/TaxID/traits and internal-only confidence labels, but not discussion of EC nonmatches or synonym uncertainty.

</details>

## Kimi

答案SHA256：`5d2bb2815aa8bb11c33d83b05ba00727f299921c41ad0e7768d4a93999f68cdd`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分9 → V0.5新分6，变化-3。

新裁判理由：

> 所选主链S02→S01→S03均有对应步骤，路线名、酶、菌及15项性状壳均交付；但答案把丁酸后的β-氧化续写为主链，且未交付S04旁支，完整性/任务边界存在实质瑕疵，按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

9档：题面要求的路径+每步酶/EC+每步对应菌+15项性状+来源+不确定性均被实质回应；route_scope.chosen_route_name逐字回填“butane degradation”，氧条件null如实保留；单一物种profile去重符合“同一菌去重”要求；F3/F4/F5/F14按题面“不确定填null”规则为明确未知而非遗漏。仅S1的EC空缺与部分辅因子未列为局部缺陷，无重要遗漏或范围偏离。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_126：确认该案为BRANCHED_DAG、ordered_step_count=4；不表示所有旁支都必答。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：给出S01–S04的底物/产物与方向；用于核对主链覆盖，不自动要求全部旁支。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S8&#93;：答案实际交付8步、1个菌profile与15项性状壳。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 主链化学方向基本正确：丁烷→1-丁醇→丁醛→丁酸及β-氧化到乙酰辅酶A；但S4 CoA活化未列ATP/AMP等辅因子，S8硫解只列1分子乙酰辅酶A，且把题面终点丁酸后的下游续写为主链，属局部计量与边界问题，按3–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

8档：主链化学正确、方向与连接成立——S1末端单加氧（列O2与水）、S2/S3醇/醛氧化、S4 AMP型CoA活化、S5–S8 β-氧化四步至乙酰CoA；碳骨架与氧化还原方向与gold四步（丁烷→1-丁醇→丁醛→丁酸）上游一致。扣分点：S5/S7的FAD/NAD+与S4的ATP等辅因子未列，属局部计量缺陷（P103，7–8档处理不cap）；题面未指定终点，答案延伸至乙酰CoA按P29不进入覆盖率扣分，S8硫解生成2分子乙酰CoA以“代表产物”简化并已披露。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：给出S01–S04的底物、产物和方向；用于核对主链化学连续性。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S8&#93;：答案逐步给出丁烷氧化、CoA活化与β-氧化转化。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 按已选主链P126_1（Butane→1-butanol→butyraldehyde→butyrate，N=3）评价。三步均已交付且底物/产物方向与目标匹配，但三目标的功能/accepted酶对应均未确认：S1用butane monooxygenase而ec_number为null，gold对应soluble butane monooxygenase/1.14.13.230；S2用alcohol dehydrogenase EC 1.1.1.1，与gold 1-butanol dehydrogenase (cytochrome c)/1.1.2.9不同；S3用aldehyde dehydrogenase EC 1.2.1.3，与gold butanal monooxygenase/1.14.13不同。现有材料没有已核催化矛盾，不能判F；但也没有已确认S，且KEY/MAJOR U尚存，不能进入7–8。仅部分目标具有可用功能相似性，需实质核对酶名/EC、电子受体与氧依赖，故取部分可用档下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

7档：S1酶名“soluble diiron monooxygenase (sBMO)”与gold soluble butane monooxygenase同指；S4 6.2.1.2、S5 1.3.8.1、S6 4.2.1.17、S7 1.1.1.35、S8 2.3.1.9均为对应反应的标准编号且酶名与EC自洽。扣分：答案称sBMO“无专属四位EC编号”，与gold EC 1.14.13.230矛盾（FV-01）；S2给EC 1.1.1.1、S3给EC 1.2.1.3，与gold该步记录的1.1.2.9/1.1.5.11与1.14.13不同，且答案自陈缺菌株级确证、官方条目核对不可得→待核。上述问题不推翻“丁烷经醇/醛氧化至丁酸”的酶学主结论，故不构成关键错误，仅档内扣分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 5d2bb2815aa8bb11c33d83b05ba00727f299921c41ad0e7768d4a93999f68cdd：支持答案S1–S3所交酶名与EC字段；不支持其已获得accepted目标匹配
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_126：gold目标步S01–S03的accepted酶名/EC：1.1.2.9、1.14.13.230、1.14.13；仅用于比对，不自动证明答案错误
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：S01–S03目标反应的主底物/主产物方向；仅定位目标反应，不作额外支持外推
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_126：全图4步/BRANCHED_DAG仅作定位；已选P126_1主链为3步，未选分支不计入D3a目标N

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 所选主链S02/S01/S03对应菌均为Thauera butanivorans，与gold organism_gold的EXACT身份一致；菌株/TaxID未填按任务允许null，整路径能力与PATHWAY_COMPLETE=TRUE相符。下游β-氧化菌归属仅内部推断，故7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

7档：种级身份Thauera butanivorans（原Pseudomonas butanovora）与gold物种名EXACT一致（TaxID 86174，Bacteria），声称粒度（种级、strain null）与gold种级记录粒度匹配，未用他菌株编号冒充；S1–S3步级归属有gold步级菌记录支撑；S4–S8归属基于生长表型/内部知识并明确披露“尚无该菌逐步骤酶学实验确证”，无跨属/跨kingdom错配，也未仅凭序列存在性断言整条路径能力。扣分：strain/TaxID留空、β-氧化段菌株级能力证据不足。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_126：S01–S04 organism_name_normalized=Thauera butanivorans且match EXACT；PATHWAY_COMPLETE行pathway_complete=TRUE。
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism：答案在所有步骤复用同一种Thauera butanivorans，并声明complete_pathway_organism_profile_id。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 可评分观测性状中F1、F7、F8、F9、F10、F11、F12、F14有gold行；答案F10运动性、F11杆状、F12革兰氏阴性、F13不产芽孢与gold一致，F2 optimum 30°C落在gold生长温度28–30附近。但F3/F4/F5/F14为null，F8 TCE共代谢、F15栖息地广适性为低置信推断，故7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

7档：已给性状多数与gold观察一致——运动性true、杆状、革兰氏阴性、不产芽孢（预测阴性）、温度optimum 30℃落在gold观察生长28–30℃区间内。扣分：F1“好氧”与gold F1观察值aerotolerant语义不完全等同（局部）；关键缺口F4盐度（gold观察0–2 %NaCl）、F14基因组大小/GC、F2的min 10/max 41未填；除F9外性状来源为INTERNAL_KNOWLEDGE_ONLY低/中置信，未标观察/预测。按P112缺失的完成度扣分主归D1，本维按已给内容质量与适用性定7档，不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_126：给出T. butanivorans的观测/预测性状行，包括运动性、杆状、革兰氏阴性、温度范围、盐度范围等。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_126：标明各性状是否可作observed_accuracy或completeness_only；不把预测背景当观测。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_126：给出F2/F4可评分标量子字段及gold值；不把null缺失当错误。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案给出EVID_001 KEGG map00650、EVID_002具体文献、EVID_003 EAWAG-BBD条目，核心路线/酶-EC有可定位条目；但S2–S8菌归属多依赖EVID_004 INTERNAL_KNOWLEDGE_ONLY，且E0为EVIDENCE_GAP无法核验引用实际支持范围，按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

5档：决策相关组中多个关键结论有具体可定位条目（KEGG map00650记录号+URL、EAWAG-BBD butane map URL、Dubbels 2007全文引文），且claim_scope逐条写明对应步骤与EC，明显优于“仅笼统库名”；但E0为EVIDENCE_GAP（entries=0），各条目的实际支持内容无法核对，只能登记UNRESOLVED_SOURCE；步级菌归属S2–S8与多数性状仅INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）。属“部分关键结论可定位但支持未核、其他模块缺映射”，取5；无经核实错引，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案实际交付KEGG map00650、Dubbels 2007文献、EAWAG-BBD URL及EVID_004内部知识声明。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确列出氧条件未指定、sBMO无专属EC、S2–S3脱氢酶为通用归属、S4–S8为KEGG推断、菌株/TaxID未确认，并给low/unknown；未把推断系统性写成观测。局部TCE共代谢/栖息地广适性仍偏推断，故7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

8档：uncertainties五条具体诚实（sBMO无四位EC、S2–S3通用酶归属缺菌株证据、S4–S8为KEGG推断、题面未指定氧条件故取好氧、strain/保藏号/TaxID未确认），逐字段confidence标注（S2–S8菌归属low、UNKNOWN项显式null），INTERNAL_KNOWLEDGE_ONLY来源被明示。扣分：“sBMO目前无专属四位EC编号”以确定语气给出，实为可核事实错误（单点过度确信）；性状值未区分观察/预测。属单点问题而非系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案明确披露sBMO无EC、S2–S3通用酶归属、S4–S8推断、菌株/TaxID未确认。

</details>

## Qwen

答案SHA256：`8cab9320d0c442bd206b1320d0d93b1718bbfc653b62a5c0abf92a55b42cfa92`。

### D1 完整性与任务符合度：7 / SCORED

V0.4旧分5 → V0.5新分7，变化+2。

新裁判理由：

> 按D-M01选定主链P126_1（butane→1-butanol→butyraldehyde→butyrate）检查：答案S1-S3覆盖该主链起点、中间体和丁酸终点，并逐步给出底物/产物、酶、菌；15项性状字段齐全但全部为null（诚实未知），S4-S8额外下游中butanoyl-CoA等SMILES缺失；无整模块缺失或路线名改选。按P29额外下游不按未选分支扣D1，但性状全未知及额外步骤表达缺口使D1为7分。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档：路径（8步至acetyl-CoA）、逐步酶/EC、对应微生物三模块均实质覆盖，chosen_route_name按题面原样填写且JSON结构可读；但15项性状全部为null（仅占位）、S4–S8五个主产物SMILES为null，性状模块实质未交付，符合“主要模块均有涉及，但若干必要内容遗漏、仅占位”，档内因遗漏面大取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：实际交付了8步主链、酶、菌及15项性状字段；主链前三步含SMILES，S4-S8部分CoA中间体SMILES为null
- QUESTION_TEXT / QUESTION：题面要求主链每步底物/产物英文名与SMILES、酶/EC、对应微生物，并要求15项性状；未知项允许null
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_126：本题gold根底物Butane、终端主产物Butyrate；用于定位所评主链终点

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 按P126_1主链，S1 butane→1-butanol、S2 1-butanol→butanal、S3 butanal→butanoate的底物/产物、方向与碳骨架连续，终点丁酸与gold terminal Butyrate一致；缺少O2/NADH等辅因子按P103/P104为局部计量表达简化，未使主链氧化还原/电荷主要结论失效。S4-S8额外下游非主链必需，不据此扣D2；在D2最高8分范围内，主链化学成立，仅余辅因子/表达简化问题。

<details><summary>V0.4理由与本行变化背景</summary>

7–8档：主链化学正确、方向正确——butane→1-butanol→butanal→butanoate与gold前段（S02/S01或S04/S03）一致，后续butanoyl-CoA→crotonoyl-CoA→(S)-3-hydroxybutanoyl-CoA→acetoacetyl-CoA→acetyl-CoA为规范β-氧化；无起始步错误、无方向反转、无原子明显不守恒。O2、NAD+/NADH、FAD、CoA、ATP等辅因子与化学计量全部未标注，属局部计量缺陷（P103/SC3），不cap，档内取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：S1 butane→1-butanol，S2 1-butanol→butanal，S3 butanal→butanoate，方向与主链一致；未展开辅因子
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：列出S02 butane→1-butanol、S01 1-butanol→butyraldehyde、S03 butyraldehyde→butyrate的有向反应及主产物；不证明额外下游步骤
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_126：终端主产物Butyrate，支持所评主链终点

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 所评主链为P126_1（butane→1-butanol→butanal→butyrate，3步）。答案S1-S3的底物/产物方向与主链一致，且所给酶名/EC均为官方条目可核（1.14.15.3、1.1.1.1、1.2.1.3），但均非accepted集合中的目标酶（1.14.13.230、1.1.2.9、1.14.13）；官方反应只支持广谱烷烃单加氧酶/醇脱氢酶/醛脱氢酶类别，未证明对丁烷、1-丁醇、丁醛的目标底物作用；S1关键入口亦未确认。因此目标酶对应整体为U而非S/F，主链化学转化可用但酶学对应需实质核验/修订，按C04/C05取5分（部分主干可用，不能因未知给1或NE）。S4-S8为butyrate下游β-氧化，不作为D3a目标步加分。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档：每步均给出酶名+EC，且酶功能与反应类型相符（单加氧、醇脱氢、醛脱氢、CoA连接、β-氧化四酶），未见EC大类别与反应类型明显矛盾；但全部confidence=low、唯一证据EVID_001为INTERNAL_KNOWLEDGE_ONLY，无任何条目级支持，且EC与gold所列酶（1.14.13.230、1.1.2.9、1.14.13）不同，E0无EC记录可核（GAP-126-001/003/004/006/009/010/013/017等），属“有合理候选和部分支持、关键步骤仍缺具体核验”，取档内5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_126：列出本题accepted酶：S02 soluble butane monooxygenase 1.14.13.230；S01 1-butanol dehydrogenase (cytochrome c) 1.1.2.9；S03 butanal monooxygenase 1.14.13。用于对比答案酶非accepted。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：定义S02/S01/S03的底物-产物方向：butane→1-butanol→butanal→butyrate；仅支持目标转化，不证明答案酶。
- E0_EVIDENCE / SUPP:ENZYME:1.14.15.3：官方ENZYME条目：alkane 1-monooxygenase，反应示例为octane→octan-1-ol；仅支持烷烃1-单加氧酶类别，不证明丁烷底物或菌株活性。
- E0_EVIDENCE / SUPP:ENZYME:1.1.1.1：官方ENZYME条目：alcohol dehydrogenase，可作用于primary/secondary alcohols；仅支持醇脱氢酶类别，不证明1-丁醇具体底物/菌株活性。
- E0_EVIDENCE / SUPP:ENZYME:1.2.1.3：官方ENZYME条目：aldehyde dehydrogenase (NAD+)，醛→羧酸；仅支持醛脱氢酶类别，不证明丁醛具体底物/菌株活性。
- E0_EVIDENCE / SUPP:ENZYME:1.14.13.230：官方ENZYME条目：soluble butane monooxygenase，明确butane→butan-1-ol，是gold accepted S02酶；用于说明答案S1未采用该已接受酶。
- E0_EVIDENCE / SUPP:ENZYME:1.1.2.9：官方ENZYME条目：1-butanol dehydrogenase (cytochrome c)，butan-1-ol→butanal，是gold accepted S01酶；用于对比答案S2。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S3&#93;：答案给出的三步底物/产物与酶名/EC；S1-S3覆盖目标主链到butyrate，S4-S8为butyrate下游β-氧化，不作为D3a目标步加分。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案给出Pseudomonas butanovora作为各步对应菌，并在complete_pathway_organism_profile_id声明全路径能力；但无TaxID/菌株，且gold为Thauera butanivorans，异名关系和全路径能力未在E0核实。属合理候选但关键身份/能力未充分核验，落5–6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档：给出可辨认的物种级候选Pseudomonas butanovora并在8步中一致归属，无跨属/无关类群记录，也未编造菌株号或TaxID；但无strain、TaxID、保藏号，无反应级或全路径能力证据，complete_pathway_organism_profile_id=ORG_001把丁烷至acetyl-CoA整链能力归于一菌；与gold物种Thauera butanivorans（TaxID 86174）的关系无法由冻结证据核实（E0 GAP，crosswalk未含），保持UNRESOLVED、不判编造不判错，属“合理候选和部分支持、关键身份与作用范围未充分核验”，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_126：gold列出Thauera butanivorans TaxID 86174及PATHWAY_COMPLETE=TRUE；不支持直接核实Pseudomonas butanovora的异名、菌株身份或答案的整路径能力。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 任务要求15项性状；答案organism_profiles&#91;0&#93;.traits中15项value全部为null且confidence=unknown，未交付任何可评性状值。按P44，全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

按P44：题目要求15项性状，organism_profiles&#91;0&#93;.traits的F1–F15全部为null/空值（confidence=unknown），构成该维对应模块完全未交付可评价结果，D4记MISSING=1，不宣称检测到科学错误；完成度不足已在D1反映，不重复重扣（P112）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_126：列出本题15项性状的可评分掩码与observed/predicted背景；用于确认性状字段集合，不用于给null值补分。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 全答案仅evidence_registry EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，locator为 pathway文字说明，database/record_id均为null。decision-relevant组均只能是MISSING_SOURCE；无已核实错引，不触发cap。D5落1–2档，因仍有内部记录但完全不可外部定位，取2。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组CG01/CG02/CG03/CG05/CG07（及CG08/CG09）全部只有EVID_001一条INTERNAL_KNOWLEDGE_ONLY自我声明，record_id=null、无数据库/文献条目，无可定位可核对结论，符合MISSING_SOURCE“完全无引用或仅内部知识自我声明”的低分档；无经核实的错引，默认不cap，按1–2档“几乎无法定位重要结论依据”取2。题面条件组CG04/CG10–CG13登记FALSE且相应性状为null，CG14仅声称级登记；SUPPORTING状态不能跨档上调。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.evidence_registry&#91;0&#93;：仅证明答案登记了一个internal-knowledge来源；不支持存在可定位文献/数据库条目。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确把来源标为INTERNAL_KNOWLEDGE_ONLY、多数酶/菌confidence=low，16项性状置null/unknown，并列出未指定氧条件、辅因子未展开、2-丁醇支路等不确定性；未把预测写成实证。因complete_pathway_organism_profile_id及部分EC仍较强呈现而未充分限定，取8而非9–10。

<details><summary>V0.4理由与本行变化背景</summary>

7–8档：所有酶与菌confidence=low、EVID_001明确标为INTERNAL_KNOWLEDGE_ONLY、15项性状以null+unknown如实登记，uncertainties具体列出氧条件未指定、菌株/保藏/基因组与多数生理性状未核实、辅因子与电子受体/化学计量未展开、可能存在2-丁醇支路；未见把预测写成实证或掩盖已知矛盾。扣分点：未显式声明EC/路径属记忆推断待复核，未讨论物种名与gold菌名可能的关系，故取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.uncertainties：证明答案主动披露了氧条件、菌株/性状未核实、辅因子未展开及2-丁醇支路；不证明其科学内容正确。

</details>

## Grok

答案SHA256：`fdb9102e8489fe4e6926157cf76ca1a3e4099e82ae67dc2058643700f1115603`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所选P126_1主链的S02/S01/S03均有对应步骤、酶、微生物、证据条目和15项性状外壳；额外β-氧化超出gold终点Butyrate，按P29不额外加分，也不作为缺步扣分。任务范围基本完整，仅有氧条件题面未指定而答案自行选定好氧这一处需说明。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_126：支持本题路线名butane degradation、终点Butyrate及污染物身份；不证明答案所有步骤正确。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_126：支持本题为BRANCHED_DAG、ordered_step_count=4；不要求交付全部旁支。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 丁烷末端氧化至丁酸及后续一轮β-氧化的方向、碳骨架和步骤连接总体连贯：丁烷→1-丁醇→丁醛→丁酸，再到丁酰CoA、巴豆酰CoA、3-羟丁酰CoA、乙酰乙酰CoA和乙酰CoA。辅因子多数列出，但S1/S3有H+等局部计量省略，S8只列一个乙酰CoA产物并在uncertainty说明两分子；属局部修订级问题，不构成方向反转或主链断裂。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：支持gold前段丁烷→1-丁醇→丁醛→丁酸的反应方向与主要底物/产物；不支持答案超出终点的β-氧化步骤作为必需步。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_126：支持gold前段酶名/EC与反应类型；不证明答案所用替代EC或具体蛋白活性。

</details>

### D3a 目标反应与酶对应：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按已认可主链P126_1（S02→S01→S03；丁烷→1-丁醇→丁醛→丁酸）评D3a，原N=3。S1丁烷单加氧酶功能与SUPP:ENZYME:1.14.13.230相符，但答案称无专用EC并填null，而该酶已有EC 1.14.13.230；S2用EC 1.1.1.1，官方条目只支持广谱伯醇→醛，未确认其为目标1-丁醇脱氢酶(cytochrome c) EC 1.1.2.9；S3用EC 1.2.1.3，官方条目支持醛→羧酸，但目标接受酶为butanal monooxygenase EC 1.14.13且含O2/NADH反应语境，未确认二者等价。三项均为MAJOR；无已核F/M，KEY4不触发，故不是低分失败锚点或封顶；但两项MAJOR酶-EC对应仍未落到accepted支持，不能进入7–8高档。属于部分主干目标有适用支持、主要酶-EC对应仍需实质核验，取&#91;5,6&#93;下沿5。S4–S8为丁酸下游延伸，超出本主链终点，不作为D3a目标步计分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_126：本题adopted主链目标酶记录：S02 soluble butane monooxygenase EC 1.14.13.230；S01 1-butanol dehydrogenase (cytochrome c) EC 1.1.2.9；S03 butanal monooxygenase EC 1.14.13。仅支持这些参考接受项，不自动认证答案中的替代EC等同。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：adopted主链目标反应的主底物/主产物与辅因子语境：butane→1-butanol、1-butanol→butanal、butanal→butyrate；支持反应方向与主产物，不证明答案所用替代酶为参考接受酶。
- E0_EVIDENCE / SUPP:ENZYME:1.14.13.230：官方条目：butane monooxygenase (soluble)，反应butane + NADH + O2 + H+ = butan-1-ol + NAD+ + H2O；支持S1的酶名/功能，也说明答案“无专用EC”不准确；不证明bmoX归属或具体蛋白实验活性。
- E0_EVIDENCE / SUPP:ENZYME:1.1.1.1：官方条目：alcohol dehydrogenase，广谱伯醇/仲醇 + NAD+ → 醛/酮；支持S2的通用醇脱氢功能，不证明其为Thauera butanivorans目标cytochrome c型1-丁醇脱氢酶EC 1.1.2.9。
- E0_EVIDENCE / SUPP:ENZYME:1.2.1.3：官方条目：aldehyde dehydrogenase (NAD(+))，醛 + NAD+ + H2O → 羧酸 + NADH + 2H+；支持S3的通用醛脱氢功能，不证明其等同于gold butanal monooxygenase EC 1.14.13或含O2/NADH的目标反应。
- ANSWER_TEXT / steps S1-S3：答案实际交付：S1 butane monooxygenase，ec_number=null，gene=bmoX；S2 alcohol dehydrogenase，EC 1.1.1.1；S3 aldehyde dehydrogenase，EC 1.2.1.3。

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 核心微生物身份为Thauera butanivorans ATCC 43655，与gold organism行的Thauera butanivorans完全对应，且gold PATHWAY_COMPLETE=TRUE支持整条路径能力。答案未填TaxID，且S4-S8的β-氧化归属为推断性扩展；核心身份正确、路径能力有支持，但有少量身份/归属待核，故为良好档而非满档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_126：支持Thauera butanivorans为S01-S04对应菌，TaxID 86174，PATHWAY_COMPLETE=TRUE；不证明未列出的ATCC 43655菌株号或β-氧化延伸各步归属。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已填性状中F11杆状、F12革兰氏阴性、F13不产芽孢与gold一致，F1/F6/F7/F8/F9方向大致合理；但F2温度、F4盐度、F10运动性、F14基因组在gold中有可评分观测而答案置null，F5保藏号及F6/F7/F8/F9的多项具体表述在E0缺口下无法核验。诚实null不按编造处理，但关键性状证据不足且多个可观测项未填，定在部分可用需实质修订档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_126：支持F11杆状、F12革兰氏阴性、F13不产芽孢，以及F2/F4/F10/F14等存在可评分观测；不支持答案F5/F6/F7/F8/F9的全部具体表述。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_126：界定各性状的observed_accuracy与completeness_only角色；F2/F4等不是以预测背景作主要正确性分母。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_126：支持F2 min/max、F4 min/max等子字段的可评分观测；不把未填子字段自动判为错误。

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案逐步/逐性状建立了evidence_id映射，EVID_006列出IUBMB EC号，EVID_001/002/003/005给出论文作者与年份，属于部分关键结论可定位；但所有来源均为INTERNAL_KNOWLEDGE_ONLY，record_id/DOI/稳定链接缺失，且E0为本案级EVIDENCE_GAP，无法核对引用实际支持内容。存在可定位映射但整体来源较弱，定5分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_126：仅用于比对答案来源声称所对应的accepted酶/EC；不核验答案的文献引用是否存在或支持其断言。

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案在route_scope.notes、各step.uncertainty和uncertainties中明确区分题面未指定氧条件、EC缺失、后四步β-氧化为途径推断、部分辅酶A硫酯不填SMILES、TaxID/温度/pH/盐度等无可靠来源置null；证据类型标注为INTERNAL_KNOWLEDGE_ONLY，未把内部推断系统性写成实验观测。个别高置信标签略强，但不构成系统性误导。

## GPT5.6

答案SHA256：`453617f2b4f16c1601810d7bfbbf729ec82a77f9bc37c75ee1502f4631b4c518`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求的主链、每步底物/产物/酶/微生物、15项性状均已实质出现；route_scope.chosen_route_name原样为butane degradation；同一菌去重为ORG_001并由各步引用；15项性状字段齐全，未知项填null，符合题面允许。S4为butyrate下游至acetyl-CoA的额外概括步骤，已在uncertainty披露简化，按P29额外下游不作为缺步扣D1，仅属少量范围/表达瑕疵。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 453617f2b4f16c1601810d7bfbbf729ec82a77f9bc37c75ee1502f4631b4c518：答案的route_scope、steps、organism_profiles与15项性状均完整出现
- QUESTION_TEXT / question.json messages&#91;0&#93;.content：题面要求主链、每步底物/产物/酶/微生物、15项性状及route_scope名称
- RUBRIC_CLAUSE / P29：题面终点外额外下游延续不加分、不扣分

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按一条认可主链P126_1/P126_2评至butyrate：S1丁烷末端羟化生成1-butanol、S2 1-butanol氧化为butanal、S3 butanal氧化为butanoic acid，方向、主碳骨架和步骤连续性成立；S1列O2/水，S2/S3缺NAD+/NADH等辅因子，属局部计量缺陷（P103），不cap。S4为butyrate下游至acetyl-CoA的概括，超出gold terminal，按P29额外下游不加分、不扣分；其简化已在uncertainty披露，不作为主链关键错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 453617f2b4f16c1601810d7bfbbf729ec82a77f9bc37c75ee1502f4631b4c518：S1-S3的底物/产物/方向/连续性；S4为butyrate下游概括并披露简化
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：gold主链方向为Butane→1-Butanol→Butyraldehyde→Butyrate，S03为terminal
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_126：本案gold terminal主产物为Butyrate
- RUBRIC_CLAUSE / P29：题面终点外额外下游延续不加分、不扣分
- RUBRIC_CLAUSE / P103：辅因子遗漏通常属局部计量缺陷，不自动cap

</details>

### D3a 目标反应与酶对应：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按一条认可主链评（P126_1或P126_2，未选分支S04不另计缺步）。答案各步均给出可辨认酶名/EC，反应类型与方向大体合理；但与accepted集合逐项未命中：S02为1.14.15.3 vs accepted 1.14.13.230，S01/S04为1.1.1.1 vs accepted 1.1.2.9/1.1.5.11，S03为1.2.1.3 vs accepted 1.14.13；E0无冻结核验记录，均登记U，不能判S，也不因未命中accepted自动判F。无已确认KEY失败，D-KEY4不触发。部分功能型对应可读但需实质核对/修订，故给5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 453617f2b4f16c1601810d7bfbbf729ec82a77f9bc37c75ee1502f4631b4c518：答案各步酶名/EC及reaction_evidence_id
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_126：本案各目标步accepted酶名/EC记录
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_126：各目标步反应底物/产物/方向
- RUBRIC_CLAUSE / C03：S/F/M/U/H分类；未命中accepted不等于已证伪
- RUBRIC_CLAUSE / C04：U存在时由裁判按实际支持和错误评分，不自动NE或低分
- RUBRIC_CLAUSE / C05：1–10档内锚点；5分为部分可用、需实质修订

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> A plausible named organism/strain is supplied for every step, but the answer gives no TaxID and no synonym/crosswalk support linking Pseudomonas butanovora ATCC 43655 to gold Thauera butanivorans TaxID 86174; it also asserts whole-path capability via complete_pathway_organism_profile_id without external capability evidence. This fits the 5-6 band at the lower side, not a verified identity error.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_126：Gold step organism is Thauera butanivorans TaxID 86174; answer names Pseudomonas butanovora ATCC 43655 and gives no TaxID, so identity/synonym match is unverified.
- ANSWER_TEXT / ANSWER_SECTION_BIOPATH150_126：Answer assigns ORG_001 to all steps and sets complete_pathway_organism_profile_id=ORG_001, asserting whole-path capability without external evidence.

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer returns all 15 trait fields and honestly nulls 11 of them, which is better than fabrication, but only F5/F7/F8/F9 are non-null; those values lack raw_text and independent frozen phenotype support for the named organism. This fits the 5-6 band at the lower side.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_126：Gold trait records are for Thauera butanivorans 86174, not directly verified for the answer&#x27;s named Pseudomonas butanovora; observed and predicted values are distinguished in gold.
- ANSWER_TEXT / ANSWER_SECTION_BIOPATH150_126：Answer returns all 15 traits, 11 explicit unknown/null, 4 non-null values; F7/F8/F9 rely on internal evidence and no raw_text.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All evidence_registry entries EVID_001-EVID_005 are INTERNAL_KNOWLEDGE_ONLY with null database, record_id, and locator. Decision-relevant route, enzyme, microbe, and trait claims therefore have MISSING_SOURCE rather than verified mis-citation; this is a low 1-2 band, with 2 because internal claim mapping is at least explicit.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_SECTION_BIOPATH150_126：evidence_registry entries EVID_001-EVID_005 are all INTERNAL_KNOWLEDGE_ONLY with null database/record/locator; no locatable source is delivered.

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer discloses oxygen unspecified, missing TaxID/genome information, and simplified beta-oxidation intermediates, and it nulls many unknowns. However, several internal-only enzyme/route claims carry medium confidence, so the 5-6 band is more appropriate than 7-8.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_SECTION_BIOPATH150_126：uncertainties array and confidence fields disclose oxygen unspecified, missing TaxID/genome, and simplified beta-oxidation, but some internal-only claims use medium confidence.

</details>
