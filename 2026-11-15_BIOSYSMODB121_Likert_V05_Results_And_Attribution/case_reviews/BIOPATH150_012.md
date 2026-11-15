# BIOPATH150_012：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：Nitroglycerin degradation pathway

污染物：Nitroglycerin；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 61 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 52.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 65.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 47 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 54.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 38 | COMPARABLE | USER_AUTHORIZED_RECOLLECTION_R1 |

## GLM

答案SHA256：`ddf4894a5fa7b3eb2d5642def86ba3a4a88d58aecdc47a32c51f69c725b94922`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分7 → V0.5新分9，变化+2。

新裁判理由：

> 按D-M01取答案最接近的认可主链P012_1（S01→S06→S04）评。答案完整返回route_scope（路线名与好氧条件原样）、3步主链、每步底物/产物/酶/微生物、3条organism_profiles各15项性状及evidence_registry；未提供EC但题面允许未知填null，字段集合完整，模块关联清楚。仅EC全为null及主链把1,2/1,3异构体合并表示，属少量局部缺陷，不构成重要遗漏或范围偏离。

<details><summary>V0.4理由与本行变化背景</summary>

结构完整：三步主链各带底物/产物英文名+SMILES、首选酶、对应微生物；三条物种+菌株去重profile各含15项性状；证据登记与uncertainties齐备。主要扣分点为全部酶EC与gene以null交付（题面要求EC，虽属如实未知）、多个关键数值性状为null，故落7–8档取下7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- SCOPE_ROW / SCOPE#BIOPATH150_012#CG04：题面冻结好氧条件，用于核对oxygen_condition原样填写
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_012：路线名称与终点甘油，用于核对route_scope及主链终点
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_012：图状态为BRANCHED_DAG及7步全图材料；按D-M01仅作定位，不作单链缺步分母

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 所选主链P012_1的化学转化与gold反应一致：GTN经NADPH依赖还原脱硝生成GDN并释放亚硝酸根，GDN继续脱硝生成GMN，GMN脱硝生成甘油；方向为底物→产物，终点甘油，包含1,2-/1,3-GDN与1-/2-GMN异构体处理，辅因子NADPH/NADP+在列。仅一步同时列两种异构体属浓缩表示，不改变主链化学正确性。D2九十分门未开，故最高8。

<details><summary>V0.4理由与本行变化背景</summary>

GTN→1,2-/1,3-GDN→1-/2-GMN→甘油，还原脱硝、NAD(P)H→NAD(P)+、每步释放亚硝酸根，方向为forward、终点为甘油，与gold(BSY-p00143，S01–S07，terminal=Glycerol)逐转化一致；把1,2/1,3与1-/2-并列异构体并入同一母步属合理简化，未改变化学结论，辅因子在列。落9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：S01/S06/S04等反应的方向、主底物/主产物、亚硝酸根副产物及NAD(P)H/NAD(P)+载体
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_012：污染物硝化甘油与终点产物甘油
- SCOPE_ROW / SCOPE#BIOPATH150_012#CG04：题面指定好氧条件，用于核对路线环境条件

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 按D-M01取答案最接近的认可主链P012_1（S01→S06→S04）评。三步均交付酶名，但S01的PETN reductase不在S01 accepted酶名集且EC=null；S06/S04为功能级 nitrate ester reductase/OYE-family描述，亦未给出accepted名或EC。程序事实：S01/S06为ROUTE_HOLD_REPRESENTATION(UNRESOLVED)，S04为UNRESOLVED_NONACCEPTED。无已确认S，也无已核实F/M；属全U/表示待核。答案的功能方向（NAD(P)H依赖硝酸酯还原脱硝）与accepted xenobiotic reductase家族相符，但按C02不能以家族相似代替精确配对，故不能进7-8。取5：部分功能合理可用，但关键酶名/EC配对未确认，需实质核验。

<details><summary>V0.4理由与本行变化背景</summary>

S1首选PETN还原酶(Enterobacter cloacae PB2来源)对硝化甘油还原有实质文献级功能支持；S2/S3仅为功能级“硝酸酯还原酶”描述，EC/gene/protein均null，关键步酶-EC未具体核验；未见酶名与EC大类别相矛盾（EC全缺）。落5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_012：S01/S06/S04的accepted酶名与EC集合；用于核对答案酶名/EC是否命中，不证明任意具体蛋白活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：对应目标反应的底物/产物方向，用于核对答案酶所绑定的反应
- E0_EVIDENCE / f3e0:taxid:303：P. putida TaxID 303的官方分类记录；仅身份/分类事实，不自动支持具体酶反应或菌株能力

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> D3b 5-6档：P. putida物种身份有E0 TaxID303名称关联及gold PATHWAY_COMPLETE支持；E. cloacae PB2的TaxID550为E0 gap，A. radiobacter NBA10无TaxID/冻结记录，且其完全脱硝能力仅内部声明。若干关键身份/能力未充分核验，取5。

<details><summary>V0.4理由与本行变化背景</summary>

E. cloacae PB2、P. putida(303)、A. radiobacter NBA10均为已知/合理的硝化甘油还原脱硝相关菌；但PB2以种级TaxID 550支持菌株级身份（E0无550记录→UNRESOLVED，属粒度不足档内扣）、NBA10菌株号与TaxID null；taxid 303与P. putida种名在E0精确匹配SUPPORTED；未见跨类群/编造。落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida TaxID303的官方名称/分类关联；不支持步级GTN/GDN脱硝能力，也不支持菌株级身份。
- GOLD_SLICE / organism_gold.tsv：gold PATHWAY_COMPLETE行含P. putida 303/A. tumefaciens 358等；不包含A. radiobacter NBA10完全脱硝的冻结记录。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> D4 5-6档：P. putida的Gram阴性、杆状、运动、不产芽孢、中温性及部分碳源/glycerol利用与gold可核记录一致；但温度/pH/盐度/保藏号/基因组数值大量null，E. cloacae PB2与A. radiobacter NBA10性状无冻结记录，A. radiobacter完全脱硝能力亦未核。部分性状准确适用，关键项证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状多为属/种级定性描述，其中与E0/gold一致者（P. putida革兰阴性、杆状、有运动性、不产孢、偏好中温）方向正确；但P. putida本可有观测的温度/pH/盐度区间等关键定量性状多数null，E. cloacae PB2与A. radiobacter NBA10在E0无性状记录→UNRESOLVED；未见离谱数值或把预测冒充观测。落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：gold仅对P. putida 303有较完整F1-F14观测/预测记录；不支持E. cloacae PB2或A. radiobacter NBA10的性状。
- GOLD_SLICE / trait_scoreability_mask.tsv：P. putida 303多数字段为observed_accuracy或completeness_only；F2 min/max等仍待温度范围政策裁定。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D5低档：全部关键结论的来源为INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator；仅P. putida TaxID303有官方名称关联，不能追到步级酶、菌株能力或性状结论。无已核实错引，不触发cap；按MISSING_SOURCE低档取2。

<details><summary>V0.4理由与本行变化背景</summary>

全部证据为INTERNAL_KNOWLEDGE_ONLY(EVID_001–007)，决策相关组(CG01/02/03/05/07/04/10等)关键结论无可定位外部记录→MISSING_SOURCE；仅taxid 303经E0核为SUPPORTED、taxid 550无记录UNRESOLVED；无经核实错引，severity=NOT_APPLICABLE不触发cap。按MISSING_SOURCE低分档给3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅官方名称/分类关联；不支持答案步级酶、菌株能力或性状来源，也不能替代答案原交付来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> D6 7-8档：答案明确把来源标为INTERNAL_KNOWLEDGE_ONLY，逐项列出EC/基因、菌株、TaxID、异构体比例和NADPH SMILES等未知，未把预测冒充观测；但部分内部知识仍标high/medium，置信强度略高于可外部核验程度，故取7。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露充分且具体：明确EC/基因未知、全部证据为内部知识、TaxID null、菌株级不确定、异构体比例不定，无隐瞒矛盾；扣分点为对内部知识核心化学(EVID_001/002)标confidence=high，置信强度与证据类型略不相称，属单点过度确信档内扣，未见系统性误导。落7档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`5ec0c41bd9f2a794be8d8c31c3f108217510254ea832a431c2099ac76a8f5e37`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> Selected path P012_2 has three required steps (S01/S07/S05); the answer covers all three with substrate/product names and SMILES, an enzyme name, a microorganism, and all 15 trait fields. EC is null for every step, so enzyme/EC delivery is only partial. Score kept at the provided D1 upper bound 6.

<details><summary>V0.4理由与本行变化背景</summary>

3步主链（Nitroglycerin→1,2-Dinitroglycerin→1-Mononitroglycerin→Glycerol）实质回应了题面的路径、逐步酶、菌与性状要求，route_scope.chosen_route_name与题面路线名逐字一致，三对底物/产物均含英文名与SMILES，15项性状全部出现。扣分点：三步酶的ec_number与gene_or_protein全部为null（模板允许未知填null，但“首选酶及EC”的交付完整性不足）；未列NAD(P)H/NAD(P)+辅因子；4项性状为整体null。归7–8档（大部分必要内容完整、少量遗漏），取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;; ANSWER.organism_profiles&#91;0&#93;.traits：Shows the delivered three steps, enzyme names with null EC, microorganism, and full 15-trait block.
- QUESTION_TEXT / QUESTION：Requires main route steps with substrate/product, enzyme and EC, microorganism, and 15 traits.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：Shows selected-path reactions S01/S07/S05 for coverage checking, not the full DAG branch set as denominator.

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> The three-step reductive denitration sequence matches selected gold path S01-&gt;S07-&gt;S05 and ends at glycerol. Main chemical defect is omission of NAD(P)H/NAD(P)+ redox carriers and implied stoichiometry; under P103 this is a local cofactor/stoichiometry defect, not a main-chain error. Score 7 in the 7-8 band; the provided base range &#91;2,5&#93; conflicts with this chemistry judgment, so review is requested.

<details><summary>V0.4理由与本行变化背景</summary>

三步化学与gold主链逐行吻合：S1对应gold S01（Nitroglycerin+NAD(P)H→1,2-dinitroglycerol+nitrite）、S2对应gold S07（1,2-dinitroglycerol→1-mononitroglycerin+nitrite）、S3对应gold S05（1-mononitroglycerin→Glycerol+nitrite）；方向为SUBSTRATE_TO_PRODUCT正向，末端为gold terminal甘油，SMILES与gold canonical一致，无起始步错误、无无依据跳步。唯一缺陷是NAD(P)H/NAD(P)+全缺，按P102–P103属局部计量缺陷，7–8档处理、不cap。取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;：Shows the claimed nitroglycerin -&gt; 1,2-dinitroglycerin -&gt; 1-mononitroglycerin -&gt; glycerol sequence and omitted redox carriers.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：Supports the selected S01/S07/S05 substrate-product transformations and shows NAD(P)H/NAD(P)+ carriers absent from the answer.

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 按已认可主链P012_2评S01、S07、S05三个目标：答案S1-S3均用Pentaerythritol tetranitrate reductase且EC=null。S01目标反应有SUPP:UNIPROT:P71278的官方推荐名及精确催化反应nitroglycerin+NADPH=1,2-dinitroglycerol+nitrite+NADP+直证，可记S；S07（1,2-dinitroglycerin→1-mononitroglycerin）和S05（1-mononitroglycerin→glycerol）在accepted集内未列出该酶名，且P71278的support_scope明确不应把首次脱硝外推到全部下游脱硝，故保持U而非F。S+F+M+U+H=1+0+0+2+0=3，无已核关键失败/漏交付，无D-KEY4上界。两处关键下游U阻止进入7–8；但U不是已证错误，不能仅按未核压成失败带。按C05取5–6下沿5：已有入口目标适用支持，但下游关联与所需EC仍未核，属部分可用、需实质修订。

<details><summary>V0.4理由与本行变化背景</summary>

三步统一写作Pentaerythritol tetranitrate reductase，ec_number与gene_or_protein均为null。该酶名与Enterobacter cloacae PB2的硝酸酯还原酶活性（gold侧对应xenobiotic reductase EC 1.6.99.1 / nitroglycerin reductase EC 1.7.1等硝酸酯还原类）在功能层面自洽，属合理候选而非明显错误；但三步均无EC、无蛋白标识，E0快照无该酶任何条目，关键步骤的酶-EC对应无法核验，也未见对“同一酶催化三级脱硝”的专门说明。归5–6档（有合理候选和部分支持，关键步骤仍缺具体核验），取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps&#91;0-2&#93;.enzyme.name：答案三步均声称同一PETN reductase且未给EC，用于核对酶名与目标步骤的对应关系。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_012：给出S01/S07/S05各步accepted酶名与EC集合；S01含nitroglycerin reductase等，S07含1,2-dinitroglycerin reductase及xenobiotic reductase，S05仅xenobiotic reductase；均未直接列出Pentaerythritol tetranitrate reductase。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：给出P012_2主链S01/S07/S05的目标反应、方向与主产物，用于逐目标核对D3a功能对应。
- E0_EVIDENCE / SUPP:UNIPROT:P71278：官方推荐名Pentaerythritol tetranitrate reductase，来源Enterobacter cloacae，并直接列出nitroglycerin+NADPH=1,2-dinitroglycerol+nitrite+NADP+等反应；支持S01的酶名与目标功能，但support_scope明确不得把首次脱硝外推到全部下游脱硝，故不直接支持S07/S05。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Enterobacter cloacae/taxid 550 is a plausible species-level identity, but strain PB2 identity, step-level attribution, and whole-pathway capability are unsupported by frozen evidence. The answer assigns the same organism to every step and declares complete_pathway_organism_profile_id=ORG_001 without locatable capability evidence. This fits the 5-6 partial-support band; lower 5 because the whole-pathway claim is central.

<details><summary>V0.4理由与本行变化背景</summary>

推荐单一菌Enterobacter cloacae PB2（TaxID 550）承担全部三步，并通过complete_pathway_organism_profile_id=ORG_001隐含“单株完成整条路径”的能力声称。PB2是文献中已知的硝酸酯降解菌，TaxID 550与E. cloacae物种级身份一致，菌名/菌株写法自洽，属合理候选；但E0无TAXID:550记录（GAP-012-010/011）、无该菌任何性状记录，身份定位、反应级能力、全路径能力三层均未核实，且全路径声称只有内部知识支撑。未出现跨属/无关类群或异菌株冒用等可核实身份错配，不cap。归5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;.microorganism; ANSWER.complete_pathway_organism_profile_id：Shows one E. cloacae PB2 profile used for all steps and a whole-pathway capability declaration.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_012：Lists gold organisms for the pathway; does not supply evidence for E. cloacae PB2, but absence from gold is not treated as proof of error.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> All 15 traits are present and nulls are explicit. Filled values are mostly plausible species-level E. cloacae traits, but key strain-specific claims such as F8 degradation capacity and F9 PETN/nitrate-ester reductase activity, plus several F1/F2/F6/F7 values, lack applicable strain-level evidence and are generalized to PB2. This fits 5-6 partial applicability; score 6.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现；11项给出值（optimum_c=37/中温菌、兼性厌氧、兼性厌氧+氧气末端受体、多种碳水化合物与有机酸、降解硝化甘油与PETN、PETN/硝酸酯还原酶活性、周生鞭毛、杆状、革兰氏阴性、不产芽孢、土壤水肠道生境广泛），4项（F3/F4/F5/F14）以null或全null子键+confidence=unknown明确未知，属诚实null而非编造，符合P112、P44。所填值与该物种的一般表型常识相符，但全部指向INTERNAL_KNOWLEDGE_ONLY的EVID_002，E0快照无E. cloacae PB2任何性状记录，无法核实；把物种级常识以high/medium置信度直接用于菌株PB2，作用粒度与条件说明不足。归5–6档（部分性状准确且适用，关键项证据不足），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：Shows all 15 trait fields, filled values, explicit nulls, and internal evidence links.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> Both evidence entries are INTERNAL_KNOWLEDGE_ONLY with null database, record_id, and locator. All decision-relevant claim groups are MISSING_SOURCE; no verified mis-citation exists, so no cap applies. D5 is in the 1-2 band; score 2 because the answer at least maps claims to local evidence IDs.

<details><summary>V0.4理由与本行变化背景</summary>

答案的evidence_registry仅两条（EVID_001、EVID_002），source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null，无任何可定位条目、文献或计算记录；按P34属MISSING_SOURCE（缺失而非误导），按P41“全部缺失→低分档（默认不cap）”。无已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。因答案仍保留了带claim_scope的证据登记结构并如实标注“内部知识”，略高于最低档，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows both evidence entries are INTERNAL_KNOWLEDGE_ONLY with no locatable database record or locator.

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> The evidence registry labels sources as INTERNAL_KNOWLEDGE_ONLY, but the answer presents a complete pathway and many traits with medium/high confidence, has an empty uncertainties array, and states no limitations or conflicts. This is multiple overconfident claims with missing boundary disclosure; 3-4 band, score 4.

<details><summary>V0.4理由与本行变化背景</summary>

正面：两类证据都如实标为INTERNAL_KNOWLEDGE_ONLY，未把内部知识包装成DATABASE_DIRECT，证据类型未被混淆；F3/F4/F5/F14也以null+unknown如实标未知。不足：F1/F11/F12/F13以high、F2/F6/F7等以medium置信度包装内部知识，而EVID_002自身confidence仅medium，出现置信标签强于证据的情况；uncertainties为空、route_scope.notes为null，主要限制与待核点未说明。属多点过度确信而非系统性把预测写成实证观测（无已核实矛盾被掩盖），按P119归5–6档，取5。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; ANSWER.organism_profiles&#91;0&#93;.traits&#91;*&#93;.confidence; ANSWER.evidence_registry&#91;*&#93;.source_type：Shows empty uncertainties, multiple medium/high confidence labels, and internal-knowledge-only source type.

</details>

## Kimi

答案SHA256：`252501aafba4fa292ccbe1672aefdb09298319421b0f58e2369eb3e57c0565cd`。

### D1 完整性与任务符合度：10 / SCORED

V0.4旧分8 → V0.5新分10，变化+2。

新裁判理由：

> 题面指定 Nitroglycerin degradation pathway、aerobic、main route；答案 route_scope 原样填写，3步连续至 glycerol，每步底物/产物/酶/EC/菌及15项性状均交付，异构体支路明确排除。按D-M01只评当前P012_1主链S01/S06/S04，未要求全DAG旁支，D1完整无重要遗漏。

<details><summary>V0.4理由与本行变化背景</summary>

结构完整：3步主链每步给出底物/产物英文名与SMILES、一个首选酶+EC、一个对应微生物；route_scope.chosen_route_name逐字填&#x27;Nitroglycerin degradation pathway&#x27;、oxygen_condition=aerobic，未改选路线；单一profile一次返回全部15项性状且每项含evidence_id与confidence；1,3-GDN/1-GMN异构支路列入alternative_branches并声明is_part_of_scored_main_route=false；下游矿化明确不纳入评分主链。扣分点仅：F3/F4/F5/F14为null（诚实未知，非遗漏），gene_or_protein全null。档位7–8（大部分必要内容完整、关联清楚），无重要遗漏或范围偏离，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv：确认题面路线为 Nitroglycerin degradation pathway、终点为 Glycerol；支持D1路线/终点匹配，不支持酶或菌株正确性。
- GOLD_SLICE / formal_cases.tsv：确认该案为BRANCHED_DAG、7步全图；不等于单条主链必答7步，D-M01下不将未选分支作为D1缺步分母。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链三步有机转化、方向、SMILES与gold S01/S06/S04一致，终点glycerol；连续性完整，1,3-GDN/1-GMN异构体支路已明确排除。各步未列NADPH/NADP+辅因子，属P103局部计量缺陷，不cap，按7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

三步均为NADPH依赖的还原脱硝（硝酸酯→亚硝酸盐），方向正确：nitroglycerin → glyceryl 1,2-dinitrate → glyceryl 2-mononitrate → glycerol，与gold线性主链S01(BSY-r00035)→S06(BSY-r00789)→S04(BSY-r00038)逐步一致，终点甘油=gold terminal BSY-c00203，副产物nitrite与gold BYPRODUCT一致；四个化学体的SMILES与gold isosmiles/canonicalsmiles为同一连接性（硝基以电荷分离式书写）。缺陷：NAD(P)H/NAD(P)+未作为cofactor/产物列出、反应式未配平，按八.辅因子与简化反应式条款属局部计量缺陷，D2按7–8档处理、不cap。档内取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Gold S01/S06/S04 支持答案三步的主底物/主产物和正向脱硝化学；不证明答案酶EC或菌株。
- GOLD_SLICE / case_root_identity.tsv：支持终点Glycerol；不支持辅因子完整性。

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 按已认可主链P012_1评三步（S01 nitroglycerin→glyceryl 1,2-dinitrate；S06 glyceryl 1,2-dinitrate→glycerol-2-nitrate/2-mononitroglycerol；S04 glycerol-2-nitrate→glycerol）。答案的底物/产物顺序与这三步反应结构基本对应，但三步均把酶标为pentaerythritol tetranitrate reductase + EC 1.6.99.7。SUPP:ENZYME:1.6.99.7显示该EC已转移至1.5.1.34（6,7-dihydropteridine reductase），与所写硝酸酯还原酶名称/功能矛盾；SUPP:UNIPROT:P71278给PB2 PETN reductase的推荐EC为1.7.1.-，并明确支持nitroglycerin首步脱硝至1,2-/1,3-dinitroglycerol与nitrite释放，但未支持同一酶完成后续1,2-DN→2-MN→glycerol两步。Gold accepted EC集合为1.7.1/1.6.99.1，不含1.6.99.7。故路线化学对应可用，但酶名—EC配对构成D3a关键错误，主要酶对应结论失效，cap≤4；考虑首步酶名有实验支持、三步反应结构/终点正确，取受限范围内4。

<details><summary>V0.4理由与本行变化背景</summary>

酶名pentaerythritol tetranitrate reductase与EC 1.6.99.7类别自洽（NADPH依赖氧化还原酶、作用于硝酸酯），不存在“水解酶解释羟化/名称为加氧酶而EC为脱氢酶”式内部矛盾；但EC 1.6.99.7在E0无冻结记录（GAP-012-002/003/004/005），无法核对其accepted name、reaction与active/transferred状态，按四.6记UNRESOLVED，不判错、不cap；gold同路径给1.7.1与1.6.99.1（其中EC-1.7.1为类级、非完整号），属集合/版本差异，按P64/P66不凭数字不同判错。三步归一为同一酶属外推，答案已在uncertainties自陈“后续脱硝是否完全由同一酶承担，文献表述可能存在差异”。档位5–6（有合理候选、关键步骤缺具体核验），取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / SUPP:ENZYME:1.6.99.7：官方ENZYME条目显示1.6.99.7为已转移条目，转移至1.5.1.34；不支持将1.6.99.7作为当前PETN reductase的EC。
- E0_EVIDENCE / SUPP:ENZYME:1.5.1.34：官方ENZYME条目为6,7-dihydropteridine reductase，说明1.6.99.7的转移目标身份；该酶不是所写硝酸酯还原酶。
- E0_EVIDENCE / SUPP:UNIPROT:P71278：Reviewed annotation：Enterobacter cloacae PB2 PETN reductase推荐EC 1.7.1.-；支持NADPH依赖的nitroglycerin首步脱硝至1,2-/1,3-dinitroglycerol并释放nitrite；不证明同一酶完成下游1,2-DN→2-MN→glycerol。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_012：已认可主链S01/S06/S04的accepted酶/EC包含1.7.1和/或1.6.99.1，不含答案所用的1.6.99.7；支持EC非匹配判断。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：P012_1的S01/S06/S04底物与主产物（nitroglycerin→glyceryl 1,2-dinitrate→glycerol-2-nitrate→glycerol，nitrite副产物）与答案反应顺序基本对应；不证明答案EC正确。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Enterobacter cloacae PB2及TaxID 550为具体候选，但E0无TAXID:550记录；全路径能力仅由complete_pathway_organism_profile_id=ORG_001声明，无冻结全路径证据；答案自身对株级未核有披露；未发现已核不匹配。按5-6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

身份三件套为Enterobacter cloacae + PB2 + ncbi_taxid 550：若550为种级TaxID而声称到菌株PB2，属八.D3b阶梯①粒度不足（档内扣、默认不cap）；E0无TaxID 550与PB2菌株级记录（GAP-012-001/010/011），身份与反应级/整路径能力均UNRESOLVED。完整路径能力声称（complete_pathway_organism_profile_id=ORG_001、三步同菌）实际由单酶证据外推，答案已在uncertainties标注该不确定性；gold的步级宿主为Pseudomonas fluorescens I-C / Agrobacterium tumefaciens / Pseudomonas putida II-B，与答案不同但gold非穷尽，不构成已核实错配，不触发cap。档位5–6（有合理候选、关键身份与作用范围未充分核验），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：Gold逐步菌为Pseudomonas fluorescens I-C、Agrobacterium tumefaciens、Pseudomonas putida II-B及PATHWAY_COMPLETE 303/358；无Enterobacter cloacae PB2记录；gold非穷尽，缺失不证明错误。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项性状均出现，但F2/F1/F6/F7/F8/F9/F10/F11/F12/F13/F15或为种级内部知识、或引用非性状证据；F3/F4/F5/F14为null。关键株级定量/适用性未核，部分性状合理但证据不足，按5-6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

已填11项均为种级定性性状（兼性厌氧、以氧为末端电子受体、周生鞭毛运动、杆状、Gram-negative、不产孢、中温性偏好、异养、硝酸酯类降解、PETN还原酶活、环境广适），方向与Enterobacter cloacae的物种性状相符，且对PB2株级多处标low并注明“株级未核实”；F3/F4/F5/F14为null属诚实未知（完成度在D1侧计，不重复重扣）。扣分点：全部性状唯一来源EVID_004为INTERNAL_KNOWLEDGE_ONLY，无条目级来源；温度/pH/盐度/基因组等关键应用性状无任何实测数值；F9以high置信标注未核实酶活。档位5–6（部分性状准确且适用、关键项证据不足），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Gold性状行覆盖Pseudomonas/Agrobacterium等，无Enterobacter cloacae PB2；不能据缺失判错，也不能支持其性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv：显示本题可评分性状子字段与待裁决范围；未覆盖Enterobacter PB2。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 关键组CG01/02/03/05/07/08/09的交付来源多为EAWAG-BBD/BRENDA/NCBI库名或描述性locator，EVID_002/005的EC/TaxID在E0无记录；EVID_004为INTERNAL_KNOWLEDGE_ONLY；无已验证错引，故不cap，但关键结论无法沿冻结记录核对，3-4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记来源：路线三组（CG01/CG02/CG03）仅有库名EAWAG-BBD/UM-BBD、PubChem与路径级描述、无条目ID（GENERIC）且E0无对应条目可核（UNRESOLVED）；酶-EC组与核心菌株身份组给出record_id（EC 1.6.99.7、TaxID 550）但E0无记录（UNRESOLVED，GAP-012-001/002～005/010/011）；氧需求与形态/栖息地等性状组仅INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；pH/盐度/基因组为null、未声称。全案无任何经核实错引，故不判CRITICAL/SYSTEMIC、不cap，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。按P41：决策相关组存在条目级可定位线索但均未核对、且部分决策相关性状模块仅有内部声明，落在5–6档下沿，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：用于核对答案EC 1.6.99.7是否在accepted集合；不在集合且E0无记录，保持UNRESOLVED，不判虚构。
- GOLD_SLICE / organism_gold.tsv：用于核对Enterobacter cloacae PB2是否在gold逐步菌/PATHWAY_COMPLETE记录；无记录，保持UNRESOLVED。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案用confidence与uncertainties明确标注异构体、株级未核、同酶承担后续步骤不确定，并对F2/F10/F15等低置信；但F9高置信、EVID_002/005中等置信在E0无记录，属单点过度确信，非系统性误导；按7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质分栏清楚：evidence_registry逐条标source_type，性状主体明确标为INTERNAL_KNOWLEDGE_ONLY并在locator写明“种级性状、PB2数据未核实”；uncertainties列出异构体归属、PB2保藏号/基因组/盐度/pH/温度未核、S2/S3是否同一酶承担三点；未知项一律null并配confidence=unknown；alternative_branches声明不属评分主链；未把预测/推断写成观测。扣分点：F9（PETN还原酶活）与F12（Gram-negative）以high置信包装无条目核实的内部知识，属单点过度确信，档内扣、非系统性误导，不cap。档位7–8，取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Qwen

答案SHA256：`a47971e63debcd78383e025879b48b40554b85827f5873433499932fb1743e56`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> D1 5-6：选定P012_2三步主链、菌、15项性状字段均有交付，路线名/好氧条件正确；但每步EC全null、无strain/TaxID、8项性状显式未知且来源仅内部知识，属主要模块有涉及但必要内容不全，按允许区间&#91;1,6&#93;取6。

<details><summary>V0.4理由与本行变化背景</summary>

路线名与氧条件按题面原样回填；给出3步，每步含底物/产物英文名与SMILES、每步酶（EC按题面允许填null）与对应菌，单一profile列出全部15项性状（7填8空，闭合=15）。无模块缺失，格式完整可解析。仅酶EC全null、菌为物种级无株号/TaxID，属少量不完整；未达9-10档‘全部要求实质回应且身份信息完整’，取7-8档高分段8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;：答案交付三步主链、一个菌profile和15项性状字段；EC与strain/TaxID多为null。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：支持选定链S01/S07/S05的核心转化与终点甘油；不代表全DAG旁支必答。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> D2 5：三步还原脱硝方向与选定S01/S07/S05核心转化一致，终点甘油；但NAD(P)H/NAD(P)+辅因子全缺、无配平、三步复用同一酶名且无机制/来源，合理性证据有限，按允许&#91;2,5&#93;取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链三步均为还原脱硝、方向正向无反转：硝化甘油→1,2-甘油二硝酸酯→1-甘油单硝酸酯→甘油，对应gold反应步r00035→r00790→r00039，终点glycerol等于gold terminal。底物/产物SMILES与gold一致。辅因子NAD(P)H/NAD(P)+未纳入（答案在uncertainties明示），按P103属局部计量缺陷、7-8档内处理不cap；1,3-DNG支路已声明is_part_of_scored_main_route=false，不构成未声明偏离。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：S01/S07/S05主转化和方向；行内NAD(P)H/NAD(P)+显示氧化还原载体，答案未列。
- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;：答案三步化学与终点；辅因子、计量和酶机制未交付。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按已认可主链P012_2（S01→S07→S05）评D3a：答案steps&#91;0&#93;对应S01，给出nitroglycerin reductase（EC null），该名在S01 accepted集内且无显式EC，按功能级支持记S；steps&#91;1&#93;对应S07、steps&#91;2&#93;对应S05，二者均复用nitroglycerin reductase且EC null，但该名不在S07/S05 accepted集内，亦无EC可核，按U待核处理，不能自动判F。故S=1、U=2、N=3，C=1/3，落入0.20≤C&lt;0.50的弱档&#91;3,4&#93;；仅一个目标步有accepted功能支持，两个KEY/MAJOR目标步仍为未确认支持，取低档3。无已核关键失败，不触发KEY4；不因U直接整维NE。

<details><summary>V0.4理由与本行变化背景</summary>

酶功能类别（硝酸酯还原酶）与各步还原脱硝相符；步骤1酶名nitroglycerin reductase与gold酶BSY-e00016(EC 1.7.1)同名，但答案EC=null且无基因/蛋白；步骤2-3复用同一酶，而gold对应步为1,2-dinitroglycerin reductase(e00015)与xenobiotic reductase(1.6.99.1)，答案亦自标该步酶不确定。属‘有合理候选和部分支持、关键步骤缺具体核验’，5-6档取中段6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / a47971e63debcd78383e025879b48b40554b85827f5873433499932fb1743e56：答案三个步骤均使用nitroglycerin reductase且ec_number为null；steps&#91;0&#93;产物为1,2-glyceryl dinitrate，steps&#91;1&#93;产物为1-glyceryl mononitrate，steps&#91;2&#93;产物为Glycerol。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_012：列出S01/S07/S05的gold酶名与EC；S01含nitroglycerin reductase，S05仅列xenobiotic reductase，S07列1,2-dinitroglycerin reductase与xenobiotic reductase；未列nitroglycerin reductase作为S05/S07 accepted名。该slice的缺失只支持登记U，不单独证明该酶绝对不能催化。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：支持所选主链P012_2的S01→S07→S05底物/产物身份与方向，用于核对答案S1-S3的化学连接；不证明答案酶名在S07/S05具有催化功能。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_012：该案为BRANCHED_DAG且题面指定Nitroglycerin degradation pathway；仅用于确认按一条认可主链评，不将全图分支作为缺步分母。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> D3b 3-4：仅给Agrobacterium radiobacter种名，无strain/TaxID；该种不在gold organism set，且三步同一菌无步级/全路径能力证据，只有内部知识；身份部分可辨但反应级能力未支持，取4。

<details><summary>V0.4理由与本行变化背景</summary>

单一物种Agrobacterium radiobacter用于全部3步，无株号/TaxID/保藏号；该种属真实（crosswalk：A. radiobacter=362），与gold对应菌A. tumefaciens(358)同属异种，非编造；但E0无A. radiobacter记录，反应级与全路径能力均未核，答案自标low且INTERNAL_KNOWLEDGE_ONLY。属‘合理候选+部分支持、关键身份或作用范围未充分核验’，5-6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_012：gold步级菌为P. fluorescens I-C、A. tumefaciens、P. putida II-B；无A. radiobacter步级能力。
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_012：确认Agrobacterium radiobacter为有效种名/TaxID 362；不证明其降解硝化甘油能力。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：答案将A. radiobacter用于全部步骤，证据为INTERNAL_KNOWLEDGE_ONLY。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D4 5-6：15项字段齐全，8项显式未知是诚实的；但已填F8/F9降解/酶活关键性状仅内部知识，A. radiobacter无trait_gold行，F1/F6/F11/F12/F13亦无来源；部分性状合理但关键证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项中7项填写（F1好氧、F6好氧呼吸/oxygen、F8广谱降解、F9硝酸酯还原酶活性、F11杆状、F12革兰阴性、F13不产芽孢），8项诚实null；已填项均confidence=low且evidence=INTERNAL_KNOWLEDGE_ONLY，E0对A. radiobacter相应子字段为EVIDENCE_GAP。形态/革兰/产孢属常见性状但无来源；F8/F9把未核的降解/酶活能力当性状陈述，属‘部分性状可信但关键项证据不足’，5-6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_012：trait_gold覆盖P. fluorescens I-C、A. tumefaciens、P. putida；无A. radiobacter性状行。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：7项填写、8项null；F8/F9等关键项为内部知识且低置信度。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> D5 1-2：两个evidence条目均INTERNAL_KNOWLEDGE_ONLY，database/record/locator全null；核心路线、酶、菌、性状无可定位条目级来源；无已核实错引，按MISSING_SOURCE低档，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅2条INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null，决策相关组(CG01/02/03/05/07/08/09)均为MISSING_SOURCE。虽用claim_scope建立内部映射，但无任何可定位外部条目，属‘几乎无法定位重要结论依据’低分档。MISSING_SOURCE为缺失非误导，默认不cap；无已核实错引，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：EVID_001/EVID_002均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> D6 7-8：答案明确标注EC/基因未知、分支可能、菌株性状基于一般知识无文献、辅因子未纳入；多数未知/low confidence标注清楚；仅F8/F9等个别能力声称仍偏强但低置信度，取8。

<details><summary>V0.4理由与本行变化背景</summary>

全篇confidence=low/unknown，EC与未知性状填null，uncertainties列明辅因子省略、1,2/1,3分支、菌株性状来源、EC缺等，正确区分未知与预测，未把猜测写成实证。8档要求主要限制与冲突更具体、且无单点强包装；此处置信标签略笼统、F8/F9能力声称仅以low包装，取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; ANSWER.steps&#91;*&#93;.uncertainty：明确披露EC未知、分支不确定性、菌株性状一般知识、辅因子省略。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits&#91;*&#93;.confidence：多数未填性状为unknown，已填项low；非系统性把预测写成实证。

</details>

## Grok

答案SHA256：`49af6466ab264fc135081ca073286c7f739e6ea6ef14e7119b462310fe944576`。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面路线名与好氧条件原样遵守；按已选主链P012_3给出连续三步、终点glycerol，每步底物/产物/SMILES、酶名和菌均有；15项性状字段齐全，4项显式null，EC均null但题面允许未知。受D1_task_range&#91;1,6&#93;限制，给6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_012：确认本题为7步BRANCHED_DAG、Aerobic；不直接证明答案完整性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_012：支持起点Nitroglycerin与终点Glycerol的题面/gold范围核对。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1 nitroglycerin→1,3-DNG、S2 1,3-DNG→1-MNG、S3 1-MNG→glycerol与选定主链S02/S03/S05的主底物、主产物与方向一致；NADPH/H+与nitrite副产物在列，1,2-DNG明确标为副产物/替代分支。化学主链可成立，但受D2_chemical_range&#91;2,5&#93;限制，给5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：支持选定S02/S03/S05的底物→主产物方向、nitrite与NAD(P)H/NAD(P)+角色；不证明具体酶身份。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_012：支持终点为Glycerol。

</details>

### D3a 目标反应与酶对应：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按已认可主链P012_3（S02→S03→S05）评。答案三步的底物/产物顺序与目标反应化学对应：nitroglycerin→1,3-dinitroglycerin→1-mononitroglycerin→glycerol，模块已交付，未发现已确认F或漏答。但三步酶均写“glycerol trinitrate reductase”且EC=null，未与本题accepted酶名/EC集合直接确认，三个MAJOR目标的酶对应均仍为U；依C04全U不自动判低或NE，按实际材料只能判为部分可用、需实质核验/补EC，不能进入7–8或9–10。取5，不取上限或中点。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：S02/S03/S05行支持主链底物/产物化学：nitroglycerin→1,3-dinitroglycerin→1-mononitroglycerin→glycerol；本身不确认答案的酶身份。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_012：列出该步accepted/curated酶名与EC标签（如nitroglycerin reductase、xenobiotic reductase）；答案确切名称“glycerol trinitrate reductase”配EC=null未在其中直接匹配，故酶支持仍为UNRESOLVED。
- ANSWER_TEXT / 49af6466ab264fc135081ca073286c7f739e6ea6ef14e7119b462310fe944576：显示三步均使用同一酶名且EC为null；支持U/支持缺口分类，不构成已确认正确。
- RUBRIC_CLAUSE / C04：全U案件应由裁判按实际支持与错误判断，不自动NE或低分；U不直接转S或F。
- RUBRIC_CLAUSE / C05：5–6档要求部分主干可用但仍有实质缺口；7–8要求主要目标酶对应可靠且仅少量预定次要U。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案统一使用Agrobacterium radiobacter并写ncbi_taxid=358；但冻结crosswalk将Agrobacterium radiobacter映射到362，358对应Agrobacterium tumefaciens，存在名称—TaxID身份错配。选定S02的gold菌可为A. tumefaciens 358，但S03/S05 organism_gold列出Pseudomonas，未给同一Agrobacterium完成全步的独立支持。属合理候选但身份与作用范围需实质核验，给5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_012：S02可见A. tumefaciens 358；S03/S05列出Pseudomonas等，不支持同一A. radiobacter全步能力。
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_012：Agrobacterium radiobacter→362，Agrobacterium tumefaciens→358；不支持radiobacter+358的组合。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段齐全，但F3/F4/F5/F14为null；F5 ST027079与F14 GCA_003667905.1在taxid 358的gold中有记录而未返回。F1/F6/F7/F10/F11/F12/F13/F15主要依赖EVID_003 INTERNAL_KNOWLEDGE_ONLY；基本形态/革兰/运动性等看似合理，但关键项证据不足且身份对应存在错配。按部分性状可用但需实质修订给5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_012：taxid 358有F5 ST027079与F14 GCA_003667905.1记录；其余多数性状为UNKNOWN。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_012：区分observed_accuracy与completeness_only；不把未知性状自动判错。
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_012：提示radiobacter与358身份错配会影响性状归属解释。

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> EVID_001/002给出可定位的具体文献题名/作者/年份/期刊，但E0快照无相应记录，无法核验；EVID_003为INTERNAL_KNOWLEDGE_ONLY，承担多种性状。核心路线/酶/身份有来源形态但多数为UNRESOLVED_SOURCE，性状来源为MISSING_SOURCE；未发现E0可核实的错引，故不cap，按部分关键结论可定位、其他仍缺核验给5。

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> uncertainties明确列出EC无可靠IUBMB号、辅因子SMILES省略、性状无来源置null、种级性状不等同脱硝分离株实测、S3同酶证据弱；EVID_003标为内部知识，confidence有low/medium区分。披露较诚实，仅部分内部知识性状仍给medium/high，属单点偏强而非系统性误导，给8。

## GPT5.6

答案SHA256：`f07b5a1a2800cec13baf466f4e6c941ec3d662bcd896e0be4d7d15082edc17d7`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> JSON delivered and route name/oxygen are correct; three steps and one organism profile cover main modules, but all EC fields are null, all 15 traits are null/unknown, and only one organism profile is used. Main modules are present but substantive completeness is limited, so mid band 5.

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT：Requires main route, per-step enzyme/EC/microorganism, 15 traits, and correct route name.
- ANSWER_TEXT / ANSWER_TEXT：Answer contains 3 steps, EC null, one organism profile, and all 15 traits null/unknown.

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Nitrate ester denitration sequence and glycerol endpoint are chemically coherent; however S1 product is named 1,2-Dinitroglycerin while its SMILES is the 1,3 isomer (gold S02), and all reductive steps omit NAD(P)H/NAD(P)+/H+. Key intermediate nomenclature/redox balance needs revision, so 5.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Answer claims sequential denitration to glycerol but gives mismatched dinitro name/SMILES and omits redox cofactors.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：Gold S02 names the same dinitro SMILES as 1,3-DNG; S02-S05 define the denitration branch to glycerol.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_012：Gold terminal main product is Glycerol.

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按已选主链P012_3（目标S02/S03/S05，N=3）评价D3a：S02由accepted nitroglycerin reductase（EC-1.7.1）在G4功能粒度支持，答案S1的Nitroglycerin reductase（ec_number=null）与该目标功能相容；S03与S05的答案同为Nitroglycerin reductase且无EC，但这两种逐步accepted集合分别只列1,2-dinitroglycerin reductase/xenobiotic reductase和xenobiotic reductase，未命中不能自动判错，按U计。S=1、U=2，C=1/3≈0.333，落C04的&#91;3,4&#93;带；只有少数目标可用，且两个关键MAJOR步骤待核，不取上沿，取3。无已核KEY失败，D-KEY4不触发。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_012：支持S02/S03/S05目标反应及P012_3主链的底物/产物方向；不证明具体酶蛋白活性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_012：S02 accepted含nitroglycerin reductase（EC-1.7.1），支持答案S1的功能级匹配；S03/S05 accepted集合未列单独的Nitroglycerin reductase且答案无EC，支持其维持UNRESOLVED而非已证失败。
- ANSWER_TEXT / ANSWER：答案三步均填写enzyme name=&#x27;Nitroglycerin reductase&#x27;、ec_number=null；用于核对逐步酶声称。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Organism is a named strain but lacks TaxID/collection/genome and any external support; it is not in gold organism rows (gold non-exhaustive) and the complete-pathway capability claim is based only on internal knowledge. Candidate is plausible but key identity/capability unresolved, so 5.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Answer assigns Mycobacterium sp. GP1 to all steps, TaxID null, and claims complete pathway for ORG_001.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_012：Gold lists other organisms for S02/S03/S05; absence of Mycobacterium GP1 is not a contradiction.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 traits are present only as null/unknown values; per P44/MISSING rule, D4 is MISSING=1, not a science-error score.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：All 15 trait entries have null values and confidence unknown.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Only evidence is EVID_001 with source_type INTERNAL_KNOWLEDGE_ONLY and no database/record/locator; all decision-relevant groups are MISSING_SOURCE. No external traceability, no verified mis-citation; D5 low band 1.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Evidence registry contains one internal-knowledge-only entry with null database/record/locator; all claims point to it.

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Answer clearly labels internal-knowledge-only evidence, low enzyme confidence, and lists unknown EC/protein, isomer ambiguity, missing TaxID/collection/genome; but it still uses medium confidence for organism and asserts complete-pathway strain capability without explicit caveat. Most limitations are disclosed; 7.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Answer includes explicit uncertainty list and low/unknown confidence for key unknown facts.

</details>
