# BIOPATH150_064：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-sulfocatechol degradation

污染物：3,4-Dihydroxybenzenesulfonate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 64 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 35 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 67.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 49 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 81 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 29 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`41ca62697a6ce3f0715fedbe01c3de4ecdb13bed9dc8c402760c0b86da4fc265`。

### D1 完整性与任务符合度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 题面路线名原样填写，给出4步主链、每步主底物/主产物英文名与SMILES、酶名和对应微生物；15项性状字段全部出现。主要不足是4步中3步EC为null，TaxID/基因组及若干性状值为null，按诚实未知登记但完成度不足，落在7–8档内取7。

<details><summary>V0.4理由与本行变化背景</summary>

四步主链、每步酶(名称)与对应菌、15项性状(10填5标unknown)、来源与不确定性均登记，主要模块涉及完整、关联清楚。缺口：3/4步EC未给、5项性状诚实置null、来源全为INTERNAL_KNOWLEDGE_ONLY无可定位记录。属5-6档(主要模块均有涉及但若干必要内容遗漏)，档内取较高6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_064：题面路线名4-sulfocatechol degradation、起点3,4-Dihydroxybenzenesulfonate与终点3-Oxoadipate，用于核对路线范围和终点。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_064：本案为LINEAR_UNIQUE、ordered_step_count=4；用于核对必需主链步数，不表示全部旁支都必须交付。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：冻结的四步有序反应及主底物/主产物角色；用于核对步骤覆盖和连接。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 四步化学主链连续：4-sulfocatechol双加氧开环产生3-sulfomuconate；随后内酯化为4-sulfomuconolactone；水解脱磺生成maleylacetate并释放sulfite；NADH依赖还原为3-oxoadipate，终点与gold一致。局部问题为H+及部分氧化还原计量未写全、S1/S2立体化学未明确，但未见主链方向、核心转化或连续性断裂；受本案9–10门限制，取8。

<details><summary>V0.4理由与本行变化背景</summary>

四步主链化学与gold reaction_gold一致：邻位双加氧开环→3-sulfomuconate→4-sulfomuconolactone→maleylacetate+亚硫酸盐→3-oxoadipate；辅因子O2/H2O/NADH在列，终点3-oxoadipate与gold terminal一致。局部问题：S1产物标&#x27;cis,cis&#x27;而gold为(2E,4Z)、SMILES未标立体化学(答案已如实披露)，S2内酯SMILES表示略有差异。7-8档(主链及关键转化充分，少量局部问题不改主要结论)，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：四步有向主链、主产物/副产物与方向；S01/S02仅表示等价/立体未定，不是已证化学失败。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_064：终点为3-Oxoadipate，用于核对D2主链终点和范围。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 4个必答目标中，S03 4-sulfomuconolactone hydrolase与S04 maleylacetate reductase/EC 1.3.1.32有相应名称/功能支持，计S=2；S01 entry与S02因表示/立体等价及酶名—EC待核，计U=2，未形成已核F或M。C=S/N=2/4=0.50，按C04落入&#91;5,6&#93;。因KEY_ENTRY S01及S02仍待核，只有后半段明确支持，选择下沿5；9–10不适用，KEY4未因已确认KEY失败触发。

<details><summary>V0.4理由与本行变化背景</summary>

酶-反应对应总体正确：S3&#x27;4-sulfomuconolactone hydrolase&#x27;与gold同名(EC应为3.1.1.92)，S4&#x27;maleylacetate reductase&#x27;EC 1.3.1.32与gold完全一致；S1&#x27;4-sulfocatechol 1,2-dioxygenase&#x27;与S2&#x27;3-sulfomuconate cycloisomerase&#x27;为功能正确的描述，与gold的EC注释名(protocatechuate 3,4-dioxygenase typeII / 3-carboxymuconate lactonizing enzyme type2)为命名/注释差异，无EC-反应类型矛盾。缺口：3/4步EC未给，全部内部知识无外部核验(EC 1.3.1.32在E0无冻结记录)。5-6档(合理候选和部分支持但关键步骤缺具体核验)，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_064：冻结accepted enzyme名称/EC集合：S03=4-sulfomuconolactone hydrolase/EC 3.1.1.92，S04=maleylacetate reductase/EC 1.3.1.32；S01/S02的答案酶名与accepted名称不同且存在表示待核，不足以判已核失败；不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：目标反应S01–S04的步骤与主产物；S03/S04功能级匹配，S01/S02因表示/立体等价待核而非已证错误。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> H. intermedia在organism_gold中为S01-S04的EXACT物种匹配，且PATHWAY_COMPLETE行含TaxID 65786并pathway_complete=TRUE；主要微生物推荐有物种级与全路径支持。但答案把同一物种写成菌株S1并给出complete_pathway_organism_profile_id，却没有TaxID/保藏号/基因组号支持该菌株级身份；按D3b身份阶梯属物种级记录支持菌株级声称的粒度不足，档内取7、不cap。

<details><summary>V0.4理由与本行变化背景</summary>

选用Hydrogenophaga intermedia，与gold organism_gold四步均EXACT匹配(taxid 65786)，且该物种在gold PATHWAY_COMPLETE=TRUE，单菌完成整条路径获gold支持；物种身份正确。strain&#x27;S1&#x27;为株级声称，gold仅物种级记录，TaxID与保藏号如实null。按身份阶梯①粒度不足：物种级真实记录支持株级声称，档内扣、不cap(通常7档附近)。取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_064：支持Hydrogenophaga intermedia为S01-S04的物种级匹配，且TaxID 65786有PATHWAY_COMPLETE=TRUE；不证明菌株S1身份。
- ANSWER_TEXT / 41ca62697a6ce3f0715fedbe01c3de4ecdb13bed9dc8c402760c0b86da4fc265：显示答案实际声称H. intermedia S1并赋予全路径能力；该菌株级身份无TaxID/保藏号。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 多项关键形态/生理性状与gold物种级记录一致：F1好氧/专性需氧、F10运动、F11杆状、F12革兰氏阴性、F13不产孢，F9所列途径酶与organism_gold的H. intermedia四步酶系一致；缺乏观测的F2/F3/F4/F5/F14以null明确未知，完成度主要归D1。扣分点在于F7/F8/F15把磺化芳烃利用、较广降解谱和生境广适性写成较强结论，trait_gold缺少直接逐项支持，且菌株S1特异性未核；故在7档内取7。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状多与gold观测一致：革兰氏阴性(gold gram positive=false)、杆状(gold rod-shaped)、可运动(gold motility=true)、不产芽孢(gold预测sporulation=false)、好氧(gold obligate aerobe)——核心形态/生理性状正确适用。缺口：温度/F5保藏号/F14基因组诚实置null但gold有观测值(F2生长25-28℃/max41、F5 DSM 5680等、F14 GCA_005938115.1)，属完成度缺口；F7磺胺酸利用、F8降解谱、F15栖息地广适为未核功能声称。5-6档(部分性状准确且适用但关键项证据不足)，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_064：支持H. intermedia的物种级好氧、运动、杆状、革兰氏阴性及部分生理/基因组记录；不直接支持S1菌株特异F7/F8/F15强声称。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_064：标明F1/F10/F11/F12等为可评分观测项，F3/F4/F6/F8等多为completeness_only或预测背景；用于避免把缺失当科学错误。
- ANSWER_TEXT / 41ca62697a6ce3f0715fedbe01c3de4ecdb13bed9dc8c402760c0b86da4fc265：显示F7/F8/F15的具体主张与low/medium置信；这些主张缺少外部定位。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 答案的evidence_registry三条全部为INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator；按D5六状态，决策相关声称均无外部可定位来源，属MISSING_SOURCE低分档。虽部分结论可由gold物种级/酶级记录侧面支持，但D5只评价系统实际交付的来源记录，不能用评价者gold回填。无已核实错引，不触发cap，故在1-2档取2。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry三条均INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator，无DOI或条目可定位，属MISSING_SOURCE低分档(P34)，默认不触发关键错误cap。答案诚实标注内部知识与低/中置信、claim_scope有登记但无外部可核记录；E0仅含Pseudomonas putida条目，与本案Hydrogenophaga答案无关，相关声称保持UNRESOLVED。低分档取3(考虑到claim_scope登记与诚实披露，不取1-2)。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 41ca62697a6ce3f0715fedbe01c3de4ecdb13bed9dc8c402760c0b86da4fc265：显示所有来源仅为内部知识，无外部定位；不能作为可追溯外部证据。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_064：Gold可支持部分酶-反应事实，但属于评价侧参考，不回填为答案原交付来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确把证据登记为INTERNAL_KNOWLEDGE_ONLY，并对EC未确认、SMILES立体未定、TaxID/保藏号/基因组/温度pH盐度等填null，uncertainties集中披露了主要限制；多数未知与低置信标签相符。仅少数性状（F6/F9/F13等）以medium置信给出、但来源仍为内部知识，属轻微披露强度问题。整体在7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露详实具体：明确EC未确认置null、立体化学未确认、TaxID/保藏号/基因组无可靠来源置null、文献出处无法回忆故全部登记INTERNAL_KNOWLEDGE_ONLY并置低/中置信、NADH SMILES省略以免误写；证据类型标注与置信强弱相称，未把预测/推断冒充观测，无系统性误导，不cap。8档(证据性质与限制标注清楚，未逐条讨论替代路线/冲突略扣)。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 41ca62697a6ce3f0715fedbe01c3de4ecdb13bed9dc8c402760c0b86da4fc265：显示答案主动披露未知、内部知识性质与多项待核限制；不证明所述科学内容为真。

</details>

## DeepSeek

答案SHA256：`20c9a6c253fb28b9ee7bcd5eacea86138eda521bbd7d4d83024a805011ca9a56`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 答案回显了题面路线名并给出4个步骤、酶与菌，但其实际化学主链在S02即偏离gold的4-sulfomuconolactone路线，S03/S04转向非gold的3-sulfolactate支路并止于pyruvate/sulfite；同时15项性状全部为null、evidence_registry为空。任务模块形式存在但主链交付不符合题面锁定路线，按D1任务偏离与完整性不足定3分。

<details><summary>V0.4理由与本行变化背景</summary>

四步主链（底物/产物英文名+SMILES）、逐步酶（4步均有酶名，3步有EC）、逐步微生物均已实质交付，route_scope.chosen_route_name按题面原样回填为&#x27;4-sulfocatechol degradation&#x27;；但性状模块15项全部null、evidence_registry为空，两处必要模块实质缺失（明确未知不等于遗漏，但完成度仍不足）。属&#x27;主要模块均有涉及、若干必要内容遗漏&#x27;档（5–6），取5。JSON可解析、字段齐全，工程完好不额外扣科学分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：仅用于核对题面锁定路线的必需主链与终点，不证明所有替代路线均无科学价值。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_064：仅支持本题gold终点为3-oxoadipate，不扩展到其他案例或替代终点。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> S1底物3,4-DHB到3-sulfomuconate与gold S01一致；但S2把3-sulfomuconate转为4-Sulfolactone，而非gold的4-sulfomuconolactone，核心环化产物分叉；S3/S4继续走向3-sulfolactate→pyruvate/sulfite，未沿gold到达3-oxoadipate。仅首步和局部反应类型可辨，核心转化断裂，按3-4档取4分。

<details><summary>V0.4理由与本行变化背景</summary>

四步判断走查：题面已指定路线名（第1步成立）；答案未声明其下游走向与常规4-磺基邻苯二酚分支不同（第2步不成立）；下游分支无可核证据（第3步按未证实登记）；第4步——S3把C6的4-Sulfolactone（SMILES计6个碳）以&#x27;reaction_type=hydrolysis&#x27;转为C3的3-Sulfolactate（SMILES计3个碳），3个碳无去向、无副产物、无说明，且S4完全建立在该C3中间体上，主链自S2之后无法成立。该碳骨架不守恒属本维自身的关键错误条件（原子明显不守恒且无说明），故cap≤4；因S1双加氧开环与S2环异构化两步化学与gold一致，档内取上限4。S1未把O2列为辅因子本属局部计量缺陷（单独按7–8档处理），不单独构成cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：仅支持gold主链的底物、产物、方向与终点；不评价答案替代支路的所有化学可行性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_064：仅支持本题终点为3-oxoadipate，不证明其他终点在别的任务中不可接受。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> S02已被程序绑定为必答KEY中间步，且gold产物4-sulfomuconolactone与答案4-Sulfolactone结构性不符，触发D-KEY4，D3a只能落在&#91;1,4&#93;。S01的EC/酶对齐、S03/S04目标对齐仍为局部未核；S=0、F=1、U=3，几乎没有可计入目标反应的已支持酶信用，仅S1底物-产物线索有局部参考价值，故取2分。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶的功能类别（双加氧酶/环异构酶/水解酶/磺基裂解酶）与答案自报的反应类型大体对应，S3在EC未知时如实置null而非编造，属正向做法；但EC 1.13.11.51、5.5.1.7、4.4.1.19在冻结证据中均无条目（GAP-064-004/007/008/010/015/016），与gold相应步骤酶（1.13.11.3/1.13.11.-、5.5.1.2、3.1.1.92、1.3.1.32）不同且无法核验，按四.5&#x27;无法核验→UNRESOLVED，保留低分与待核标记，不cap&#x27;处理；另有S3酶名（4-sulfolactone hydrolase）与其实际交付的C6→C3转化不相称（该化学问题已在D2独立计错，本维不重复计）。属&#x27;有合理候选与部分支持、若干关键步骤缺具体核验&#x27;档（5–6），取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：仅支持S02 gold产物身份与答案产物不同，不推断S01/S03/S04所有酶均无效。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_064：仅支持accepted酶名/EC集合与gold步骤归属；不证明具体蛋白底物谱或实验活性。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案全程使用Hydrogenophaga intermedia，gold organism行显示该物种覆盖S01-S04，且PATHWAY_COMPLETE记录支持其完成gold 4-sulfocatechol路线；物种级身份与全路径能力有可靠支持。但答案写strain S1、无TaxID，并把该菌配到非gold的S02-S04替代反应上，菌株级身份及这些具体步骤能力未核，故取7档而非9-10。

<details><summary>V0.4理由与本行变化背景</summary>

答案推荐的物种Hydrogenophaga intermedia与gold的步级菌一致（S01–S04均列出该种，taxid 65786），且gold对该种登记PATHWAY_COMPLETE=TRUE（genome GCA_005938115.1），因此主要微生物推荐与&#x27;整条路径能力&#x27;在物种层获得可靠支持；不足处：菌株标签&#x27;S1&#x27;与TaxID均无冻结记录，属物种级记录支持菌株级声称的粒度不足（身份阶梯①：档内扣分、默认不cap），且答案未交付任何证据（归D5）。四步均用同一物种亦符合题面&#x27;每步写该步对应的菌&#x27;的要求。定档7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_064：仅支持H. intermedia在gold路线中的物种级与全路径能力；不证明strain S1或答案替代步骤的菌株级能力。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 不是判性状数值错误，而是性状模块没有可评价内容：15项全部以value=null交付，confidence均为unknown，filled=0。按P44全部必需性状均为null/空值时D4记MISSING=1。

<details><summary>V0.4理由与本行变化背景</summary>

唯一的organism_profile中15项性状（F1–F15）全部为value=null、raw_text=null、evidence_id=null、confidence=&#x27;unknown&#x27;，没有任何可评价的性状数值或适用范围；按四.4&#x27;全部必需性状均为null/空值时D4按MISSING记1分，不宣称检测到科学错误&#x27;处理。明确未知体现信息不足，不与遗漏或错误等同，故不在D4另扣，其完成度后果已在D1反映。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry为空，所有step、enzyme、microorganism与trait的evidence_id均为null；仅有“inferred from literature”式自述，无法定位到具体条目。决策相关组全部为MISSING_SOURCE，路径、酶、菌、性状均无法沿来源记录核查；无已核实错引，不触发cap，按D5低档取2。

<details><summary>V0.4理由与本行变化背景</summary>

答案evidence_registry为空数组，各步reaction_evidence_id/trait_evidence_id、enzyme.evidence_id、microorganism.evidence_id全为null，仅在uncertainty中写&#x27;inferred from literature; exact source not verified&#x27;（属INTERNAL_KNOWLEDGE_ONLY/MISSING_SOURCE）；决策相关组（CG01/CG02/CG03/CG05/CG07/CG09）全部无可定位条目，属&#x27;几乎无法定位重要结论依据&#x27;低分档（1–2）。无任何引用即不存在已核实错引，按四.3/P34 MISSING_SOURCE默认不触发cap，取2（保留1分余量因答案如实自述来源未核）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案对全部步骤酶标confidence=low，对15项性状全部null且confidence=unknown，并在uncertainties中说明EC/菌株为推断、性状未核，未系统性把预测冒充实证；这些是正面披露。但route_summary仍以确定语气陈述整条路径，且未说明与指定gold主链的偏离或S02产物冲突，故取7档而非更高。

<details><summary>V0.4理由与本行变化背景</summary>

正向：四步confidence一律&#x27;low&#x27;，未知性状一律null而非填占位；uncertainties明确写出&#x27;EC编号与菌株归属为文献推断、未核实来源&#x27;与&#x27;性状未经原始来源核实&#x27;，并把未知留白——属大部分证据性质被正确标注、未把预测写成实证。不足：披露较笼统（同一句重复于多步），route_summary以确定语气陈述S3&#x27;水解为3-磺基乳酸&#x27;，未提示该下游走向与常规4-磺基邻苯二酚（maleylacetate分支）不同、也未提示SMILES层面碳数不连续，部分结论强度略超依据。属泛化披露不足与单点过度确信，非系统性误导，档内处理（5–6），取6，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`1fbe89521b18c6e8682a39f0988e5b0d8aa54f0496f1f3f36fe6d4d282df9c6d`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案给出4步主链、每步酶与微生物、15项性状字段，路线名原样保留，氧条件null未擅改，主模块齐全；少数性状为null及来源绑定有限，未达无重要遗漏的9-10档。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块总体齐备：四步主链、每步底物/产物英文名+SMILES、每步首选酶与对应微生物、单一菌株profile的15项性状、evidence_registry与uncertainties均交付；chosen_route_name原样为&quot;4-sulfocatechol degradation&quot;，未改路线、未擅改氧条件（保留null）。扣分：15项性状中6项为null/全null（F2/F3/F4/F5/F10/F14），其中温度、保藏号、运动性、基因组在gold有可定位记录，属完成度不足；S2/S3未给EC（S3在gold已有EC 3.1.1.92，属可补未补）。档位7–8，取7（大部分必要内容完整，存在若干可补遗漏）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_064：金标本case为LINEAR_UNIQUE、ordered_step_count=4；只支持四步主链存在，不证明答案科学正确。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_064：指定路线名4-sulfocatechol degradation与终点3-Oxoadipate；不扩展到未声称的下游。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链与金标四步一致：S1正位开环、S2内酯化、S3水解脱亚硫酸根、S4还原到3-oxoadipate；方向与终点正确，辅因子多数列出。S2/S3精确立体表示仍有表示边界复核，故落7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

四步主链与gold S01–S04逐一对应：4-sulfocatechol正位双加氧裂解→3-磺基黏康酸→4-磺基黏康酸内酯→maleylacetate+亚硫酸根→3-oxoadipate；起点与gold根化合物一致，终点=gold terminal 3-oxoadipate，方向、主要原子收支与步骤连接成立，首步含O2共底物、S3含H2O、S4含NADH/NAD+。扣分：S1/S3/S4未列H+产物（局部计量简化，按P103在档内处理，不cap）；S2内酯SMILES答案自述按黏康酸内酯类比给出、待与权威化合物记录核对；S1产物以cis,cis命名，与gold (2E,4Z)立体表述不一致且未说明。档位7–8，取8（主链与关键转化有充分依据，少量局部问题不改变主要结论）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：S01-S04主链化合物、方向与终点；不支持未列出的酶/菌身份。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> D3a按四个必答目标逐步核酶名/EC：S04的maleylacetate reductase + EC 1.3.1.32与accepted集合精确匹配；S03的4-sulfomuconolactone hydrolase名称与accepted匹配，未填EC不自动判错。S01所答3,4-dihydroxybenzenesulfonate 3,4-dioxygenase/EC 1.13.11.14不在本题accepted集合且无冻结EC记录，S02所答sulfomuconate cycloisomerase/EC null亦未匹配accepted的3-carboxymuconate lactonizing enzyme type 2/EC 5.5.1.2，二者保持U。两个目标有适用支持、两个待核，按C04覆盖带落在&#91;5,6&#93;；因关键入口S01仍待核且仅约半数目标获支持，取档内低分5。未达到已核关键错误条件，不触发KEY4≤4。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶功能类型均与反应类型匹配：S1为双加氧酶（intradiol cleavage，与4-sulfocatechol正位裂解一致）、S2为磺基黏康酸环化异构酶、S3为4-sulfomuconolactone hydrolase（名称与gold一致）、S4为maleylacetate reductase EC 1.3.1.32（与gold一致）。扣分：S1所给EC 1.13.11.14与gold的1.13.11.3/通配1.13.11.-属同家族但具体号不同，E0无该EC记录（GAP-064-001），无法核accepted name/reaction，按P64/P66登记UNRESOLVED不判错；S2未给EC，S3未给EC（gold已有3.1.1.92）；S2/S3仅引无定位文献。档位7–8，取7（主要步骤酶对应有合理支持，若干条目需进一步确认）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：仅支持S03与S04的accepted酶名/EC配对：4-sulfomuconolactone hydrolase EC 3.1.1.92；maleylacetate reductase EC 1.3.1.32；不证明具体蛋白实验活性或整路能力
- GOLD_SLICE / reaction_gold.tsv：仅支持S03/S04目标反应名称、方向与主产物对应：4-sulfomuconolactone→maleylacetate+sulfite；maleylacetate→3-oxoadipate；不扩展到其他目标或菌株能力
- GOLD_SLICE / enzyme_gold.tsv：仅列S01/S02 accepted集合：protocatechuate 3,4-dioxygenase type II EC 1.13.11.3/1.13.11.-；3-carboxymuconate lactonizing enzyme type 2 EC 5.5.1.2；不足以确认答案的EC 1.13.11.14或sulfomuconate cycloisomerase
- ANSWER_TEXT / ANSWER.steps.S1-S4.enzyme：答案实际交付的酶名与EC声称：S1 1.13.11.14；S2无EC；S3无EC；S4 1.3.1.32

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Hydrogenophaga intermedia在S1-S4均属gold物种且PATHWAY_COMPLETE为TRUE，物种级主要微生物对应成立；但答案给的菌株S1、TaxID null及菌株级全路径能力未获冻结证据支持，落7档。

<details><summary>V0.4理由与本行变化背景</summary>

核心微生物推荐为Hydrogenophaga intermedia，该物种在gold organism_gold中为EXACT匹配（TaxID 65786，基因组GCA_005938115.1），并出现在S01–S04及PATHWAY_COMPLETE行，物种级选择正确、与目标路线相容。扣分：答案给出菌株标签&quot;S1&quot;但无任何菌株级记录/保藏号/TaxID（ncbi_taxid为null），属“物种级真实记录支持菌株级声称”的粒度不足（身份阶梯①：档内扣、默认不cap）；单步与整条路径能力均只作种级归因。档位7–8，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_064：支持Hydrogenophaga intermedia物种及PATHWAY_COMPLETE TRUE；不列S1菌株，不支持菌株级身份或菌株级全路径能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> F1好氧、F11杆状、F12革兰氏阴性、F13不产孢与trait_gold观测一致；但F7/F8/F9/F15多由通路推断，trait_gold无观测或仅predicted/UNKNOWN，且F5/F10/F14等可用观测留空。部分性状准确但关键项证据不足，落5-6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状中可核实且适用的部分：F1“好氧”与种级代表记录obligate aerobe一致；F12革兰氏阴性、F11杆状与种级观测记录一致；F6好氧呼吸/氧气与好氧双加氧路线相容（但无观测记录）。问题：F7碳源/底物利用、F8广义降解能力、F9酶活三项实为路径/文献推断，却以medium置信与具体raw_text当作性状值交付，属“推断充作性状证据/证据强度超过依据”；F15栖息地陈述带限定但仍无记录支撑；F13仅有种级预测级记录。F2/F3/F4/F5/F10/F14以null或全null返回，属诚实未知（完成度扣分已计D1，不在此重复重扣）。档位5–6，取6（部分性状准确适用，关键项证据不足、条件解释需修订）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_064：F1/F11/F12/F13等观测支持；F7裸名称列表非阳性清单，F8等有predicted背景，不能当观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_064：F6/F7/F8/F9/F15等为completeness_only或predicted background；不能把预测当观测。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> S1/S4给出具体EC数据库名、record_id与URL，属可定位条目；但E0无对应记录，无法核对支持内容。S2/S3、微生物身份和多数性状仅EVID_003（PubMed无record_id/locator），属泛称来源。未见经核实错引，不cap；按部分关键结论可定位、其他模块缺映射的5-6档取下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记后：决策相关组中，酶-EC组（CG05）有ExplorEnz条目号+URL的条目级定位（1.13.11.14、1.3.1.32），但E0无对应EC记录（GAP-064-001/002），只能记UNRESOLVED_SOURCE；核心菌身份（CG07）、步级归属（CG08）、全路径能力（CG09）以及多数性状（CG10/CG14/CG15/CG16）仅引EVID_003——PubMed但record_id与locator均为null，属GENERIC_SOURCE，无法定位条目；路线S2/S3反应同样只挂该笼统来源。不存在经核实的错引（查不到≠虚构≠矛盾），不触发cap。按P41“决策相关组存在部分可定位可核对条目→5–6档”，取5（部分关键结论（酶-EC）可定位，但核心身份/步级归属/性状仍缺映射）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_064：accepted EC/名称可用于检验来源支持范围；不核验答案EVID_001/002是否真实存在。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_064：只支持Hydrogenophaga intermedia物种级身份；不核验EVID_003 PubMed条目。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> uncertainties明确列出S2/S3 EC未定、H. intermedia S1保藏号/TaxID/基因组及温度/pH/盐度未核、氧条件null未擅改；confidence多标medium/low。部分通路推断性状（F7/F8/F9）未明确标为预测，complete_pathway字段也未单独限制；主要限制已披露，落7档。

<details><summary>V0.4理由与本行变化背景</summary>

正面：uncertainties三条具体（S2/S3酶EC未定、TaxID/基因组/温度pH盐度未核、氧条件null未擅自改写），各字段confidence分档使用（high/medium/low/unknown），F11/F13/F15的raw_text明示属/种级推断与未核实，未把主要未知掩盖。扣分：F7/F8/F9等以路径或属级推断得出的性状值未标注为“推断/预测”，却给medium置信并挂在无定位的EVID_003上，属多处结论强度超过依据；但错误集中于同一类推断，非系统性把预测写成实证、无明知掩盖证据，故档内扣不cap。档位5–6，取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_064：用于对照答案是否把predicted/UNKNOWN写成观测；不改变D6披露质量评分。

</details>

## Qwen

答案SHA256：`8e7d5b41bd16f87dd989fd395bdb13f26f0f19d47f03d869bd41c964ccfd0a55`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案以合法JSON交付指定路线名，包含4个主链步骤、每步底物/产物名称、首选酶与对应微生物，并以ORG_001去重；organism_profile的15项性状字段齐全。存在少量完整性缺口：4-sulfomuconolactone、3-sulfomuconolactone等中间体SMILES为null，trait raw_text多为null，部分中间体结构信息不足；但未出现整模块缺失或明显任务范围偏离，按D1的7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

四步主链齐备，每步均绑定 substrate/product/enzyme/microorganism，chosen_route_name 原样回填题面给定路线名，15 项性状全部出现（11 项有值、4 项明确 null），来源与不确定性均有登记。缺陷为 S2 与 S3 的底物或产物 SMILES 为 null、S2/S3 无 EC，属若干必要内容遗漏、部分字段仅占位，落 5–6 档取 6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案包含4个step、每步底物/产物/首选酶/微生物、1个organism_profile的15项性状及evidence_registry；用于D1完整性与格式核对。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_064：冻结任务材料显示本题为4-sulfocatechol degradation、LINEAR_UNIQUE、ordered_step_count=4；用于核对D1路线范围与主链步数框架，不替代答案内容。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> D2主链化学存在已核关键错误：S1声明为intradiol ring-cleavage dioxygenation，却直接把3,4-Dihydroxybenzenesulfonate转为4-sulfomuconolactone，跳过了gold S01主产物3-sulfomuconate；冻结反应行显示S01应生成(2E,4Z)-3-sulfonatohexa-2,4-dienedioate（3-sulfomuconate），再由S02转为4-sulfomuconolactone。答案S2又写成4-sulfomuconolactone→3-sulfomuconolactone，与gold S02的3-sulfomuconate→4-sulfomuconolactone不符。S3/S4向maleylacetate与3-oxoadipate的后续方向大体可接续，但入口转化和S1-S2连接已错，触发D2关键错误cap≤4；鉴于S3/S4尚可接续且终点可达，在受限范围内取4。

<details><summary>V0.4理由与本行变化背景</summary>

起点 3,4-Dihydroxybenzenesulfonate 与终点 3-oxoadipate 与 gold 记录一致，O2 参与的双加氧开环方向、脱磺与还原方向正确，S4 与 gold 完全对应。但 S1 把开环与内酯化合并、主产物直接写成 4-sulfomuconolactone，省略 gold 记录的 3-sulfomuconate 开环二烯酸中间体；S2 插入 gold 主链无对应的内酯异构步；S3 以 3-sulfomuconolactone（gold 为 4-sulfomuconolactone）为水解底物。主干成立但关键中间体与连接需实质修订、合理性证据有限，落 5–6 档取 5；未达起始步错误、方向反转、明显不守恒或跳到中心代谢物的 cap 条件。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：S01底物3,4-Dihydroxybenzenesulfonate加O2的MAIN_PRODUCT为BSY-c12591 (2E,4Z)-3-sulfonatohexa-2,4-dienedioate（3-sulfomuconate）；S02将3-sulfomuconate转为4-sulfomuconolactone；S03 4-sulfomuconolactone+水生成maleylacetate+sulfite；S04 maleylacetate还原为3-oxoadipate。
- ANSWER_TEXT / ANSWER：答案S1把4-sulfomuconolactone直接列为3,4-Dihydroxybenzenesulfonate的产物；S2把4-sulfomuconolactone转为3-sulfomuconolactone；用于核对D2连接与中间体。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 逐目标步核对accepted酶集合：S04的maleylacetate reductase/EC 1.3.1.32与accepted一致，可确认支持；S01的3,4-dihydroxybenzenesulfonate 3,4-dioxygenase/EC 1.13.11.8不在accepted名/EC集合（accepted为protocatechuate 3,4-dioxygenase type II/EC 1.13.11.3或1.13.11.-），S02 sulfomuconolactone isomerase无EC且与accepted 3-carboxymuconate lactonizing enzyme type 2/EC 5.5.1.2不对应，S03 3-sulfomuconolactone hydrolase无EC且与accepted 4-sulfomuconolactone hydrolase/EC 3.1.1.92名称粒度不一致；这些按U待核，不判F。仅1/4目标可确认支持，属少量目标可用，D3a按3分。无确认KEY失败，不触发D-KEY4。

<details><summary>V0.4理由与本行变化背景</summary>

S4 的 maleylacetate reductase、EC 1.3.1.32 与 gold 的酶-反应对应完全一致，可直接核对。S1 给出 1.13.11.8，与 gold 的 protocatechuate 3,4-dioxygenase type II（1.13.11.3/1.13.11.-）不一致，但 E0 无 EC:1.13.11.8 的冻结记录，按四.5/四.6 保守条款保持 UNRESOLVED 待核、不判错；S2 的 sulfomuconolactone isomerase 与 S3 的 3-sulfomuconolactone hydrolase 均无 EC、无冻结记录。有合理候选与部分支持、若干关键步骤缺具体核验，落 5–6 档取 5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_064：逐S01-S04列出可接受酶名与EC：S01 protocatechuate 3,4-dioxygenase type II/EC 1.13.11.3或1.13.11.-；S02 3-carboxymuconate lactonizing enzyme type 2/EC 5.5.1.2；S03 4-sulfomuconolactone hydrolase/EC 3.1.1.92；S04 maleylacetate reductase/EC 1.3.1.32。为反应级策展支持，不证明具体蛋白底物谱或实验活性。
- ANSWER_TEXT / ANSWER：答案S01=3,4-dihydroxybenzenesulfonate 3,4-dioxygenase/EC 1.13.11.8；S02=sulfomuconolactone isomerase/EC null；S03=3-sulfomuconolactone hydrolase/EC null；S04=maleylacetate reductase/EC 1.3.1.32。用于与accepted集合逐步比对。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> P. putida NCBI TaxID 303的物种级身份可由E0 taxid:303核对，属于合理候选；但答案用同一物种覆盖S1-S4，且complete_pathway_organism_profile_id=ORG_001声称整条路径能力，EVID_001 claim_scope只覆盖organism_name/ncbi_taxid，无反应级或全路径能力证据。按D3b 5–6档：有合理身份和部分支持，但关键作用范围未核验；取低半5分。

<details><summary>V0.4理由与本行变化背景</summary>

TaxID 303 与 Pseudomonas putida 的官方记录匹配（E0 核实为 SUPPORTED），身份定位层成立，物种作为芳香化合物降解菌也属合理候选。但四步全部归同一菌、complete_pathway_organism_profile_id=ORG_001，步级催化能力（L2）与完整路径能力（L3）仅有 INTERNAL_KNOWLEDGE_ONLY 支持，gold 的本题步级菌列表中亦无该菌。身份真实但关键能力未核验、作用范围未限定，落 5–6 档取 5；无已核实错误，不 cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida物种级学名与TaxID；不支持菌株级身份、单步催化或全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_064：列出gold步骤菌与全路径菌记录；gold非穷尽，不自动判答案菌错误，但可用于核对作用范围证据是否匹配。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项外壳齐全，F4/F3/F5/F14以null明确未知，未把缺失伪造成观测；F1/F6/F10/F11/F12/F13/F15等一般性状对P. putida属种水平大致合理。但F7可利用4-磺基儿茶酚、F8可降解磺化儿茶酚类、F9具有3,4-二羟基苯磺酸3,4-双加氧酶活性均引用EVID_002 INTERNAL_KNOWLEDGE_ONLY，无条目级证据；F2仅给嗜温偏好无数值。按D4 5–6档：部分性状适用但关键项证据不足，取低半5分。

<details><summary>V0.4理由与本行变化背景</summary>

P. putida 的杆状、革兰氏阴性、不产孢、可运动、好氧、嗜温与土壤/淡水广适性描述属可靠一般性状；F3/F4/F5/F14 明确置 null（诚实未知，不计为错误）。但 F7（可利用 4-磺基儿茶酚为碳源）、F8（可降解磺化儿茶酚类）、F9（具有该 3,4-双加氧酶活性）把降解相关性状写成已知值，仅有 INTERNAL_KNOWLEDGE_ONLY 支持，E0 的 12880 面板不包含本题污染物。部分性状准确适用、关键项证据不足，落 5–6 档取 6；明确未知与低置信标注未按编造处理。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：仅支持该菌株记录中的培养温度26/30°C与保藏号集合等；不是答案未指定菌株的4-sulfocatechol性状证据，培养温度也不等于最适值。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_064：提供冻结性状参照；未覆盖或不同不自动判错，关键降解性状仍需对应粒度证据。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> D5按claim group登记：CG07身份有EVID_001 NCBI Taxonomy 303且E0 taxid:303可核对；但路线核心步骤、起点、终点、酶-反应/EC、步级微生物归属、全路径能力、性状均主要依赖EVID_002/EVID_003 INTERNAL_KNOWLEDGE_ONLY，无条目级可定位来源。决策相关组多数为MISSING_SOURCE，仅身份一处可定位；按D5 3–4档取低半3分。未发现经核实的错引，故不触发cap。

<details><summary>V0.4理由与本行变化背景</summary>

证据登记 3 条：EVID_001 为 NCBI Taxonomy record 303（条目级可定位，E0 核对学名匹配、SUPPORTED）；EVID_002/EVID_003 均为 INTERNAL_KNOWLEDGE_ONLY，路线、酶、步级菌与性状无可定位条目。决策相关组中仅 CG07 存在条目级可定位可核对结论，其余为 MISSING_SOURCE，CG05/CG06 另记 UNRESOLVED_SOURCE（EC/酶名无冻结记录）。无任何已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不 cap；按四.3/P41&#x27;存在条目级可定位可核对结论→5–6 档&#x27;并结合多数核心组缺失，取 5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida物种名与TaxID；不支持路线、酶-反应、步级归属或性状来源。
- E0_EVIDENCE / f3e0:bacdive:12880：为另一菌株记录，含培养温度/保藏号等；不支撑答案未指定菌株的4-sulfocatechol路线或性状来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案将EVID_002/EVID_003标为INTERNAL_KNOWLEDGE_ONLY并给low/medium，uncertainties列出氧条件未定、内酯异构/水解酶EC不确定、未指定菌株导致性状为种级推断、辅因子化学计量未确认；整体未把内部推断系统性包装成实验观测。仍有少量过强处：S1酶给medium、microorganism给medium且complete_pathway profile存在，但其不确定性披露基本具体。按D6 7–8档取低半7分。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties 具体列出氧条件未指定、内酯化/异构/水解命名与 EC 不确定、未指定菌株故性状为物种水平低置信推断、辅因子计量与立体化学未确认；证据条目均标 INTERNAL_KNOWLEDGE_ONLY，多数性状 confidence=low，明确未知项置 null。但 S1–S4 的 enzyme/microorganism confidence=medium 而所引 EVID_002 为 low，且 complete_pathway_organism_profile_id 与 F7/F8/F9 具体值未声明为推断，属单点过度确信。披露整体较好、部分结论强度超出依据，落 5–6 档取 6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`ef696b20d466626e83baecd350dce8cd0f0e5573a49b649f70d436da1b90f7d7`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 输出按题面指定路线名填写4-sulfocatechol degradation，并给出4个主链步骤，覆盖底物/产物名称与SMILES、酶名及可给EC或显式null、对应微生物；同一菌去重为ORG_001，15项性状字段齐全，下游延续另列而未混入主链。主要不完整处是S2/S3无EC、若干性状为null，且题面氧条件原本未指定而答案将其记为aerobic但有说明；这些属于7–8档的少量/局部缺陷，未使任务模块大部缺失或路线偏离。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：题面指定route_scope.chosen_route_name必须原样填写4-sulfocatechol degradation；要求每步底物/产物、酶及EC、微生物；要求同一菌去重并填写15项性状，未知可null；氧条件为null（未指定）。
- ANSWER_TEXT / ANSWER.route_scope;ANSWER.steps;ANSWER.organism_profiles：答案填写了指定路线名、4个步骤、每步酶与微生物、1个去重菌株档案及15项性状字段；S2/S3的EC为null，若干性状为null，氧条件写为aerobic并在notes说明。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_064：本题路径名称为4-sulfocatechol degradation，起点为3,4-Dihydroxybenzenesulfonate，终点为3-Oxoadipate。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_064：冻结案例为LINEAR_UNIQUE，ordered_step_count=4，可作为4步主链完整性核对材料。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_064：冻结性状材料显示Hydrogenophaga intermedia存在部分可观测性状记录；这支持指出答案若干性状null与可核记录之间的完成度差距，但不把未知null直接判为科学错误。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案4步化学主链与本题4-sulfocatechol降解主链一致：S1双加氧邻位开环生成3-sulfomuconate，S2内酯化为4-sulfomuconolactone，S3水解脱亚硫酸盐生成maleylacetate与sulfite，S4还原为3-oxoadipate并止于gold终点。方向、顺序、终点和主要转化均正确，辅因子在S1/S3/S4有列出，S2无需辅因子。局部问题包括SMILES/名称的立体化学未充分标明、S4以NADH简写NAD(P)H、S2/S3酶EC缺失，但不推翻主链化学结论；按当前D2可评上界为8，给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：冻结反应切片给出S01-S04的底物/产物、方向及主链连接：S01 3,4-Dihydroxybenzenesulfonate+O2→3-sulfomuconate；S02→4-sulfomuconolactone；S03→maleylacetate+sulfite；S04→3-oxoadipate。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_064：本题终点化合物为3-Oxoadipate，答案S4主产物与终点一致。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_064：冻结酶材料显示S01可为protocatechuate 3,4-dioxygenase EC 1.13.11.3/1.13.11.-，S03为4-sulfomuconolactone hydrolase EC 3.1.1.92，S04为maleylacetate reductase EC 1.3.1.32；用于核对答案酶及EC对应，不要求具体蛋白实验级支持。
- ANSWER_TEXT / ANSWER.steps.S1-S4：答案逐步骤给出主底物/主产物与SMILES、反应类型、酶和微生物；化学路线可辨认，S4止于3-oxoadipate；存在立体化学表达和NADH/NAD(P)H简写等局部问题。

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a允许范围为&#91;1,8&#93;，policyA=NOT_ELIGIBLE，9–10被阻断。S01 EC 1.13.11.3与S04 EC 1.3.1.32匹配accepted sets；S03使用精确accepted酶名“4-sulfomuconolactone hydrolase”但省略EC；S02用“3-sulfomuconate cycloisomerase”并置EC null，与accepted的“3-carboxymuconate lactonizing enzyme type 2/EC 5.5.1.2”仅部分对齐。主催化方向与四步对应大体可靠，但EC/名称配对和S02名称边界仍有局部未决，故在&#91;7,8&#93;带取低分7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_064：Gold/accepted酶集合支持S01–S04的反应-酶候选；不支持把S02不同名称与null EC自动当作S03式精确accepted配对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：支持四步主链反应方向与主产物；不解决S02/S03的具体EC配对。

</details>

### D3b 微生物身份与能力：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步均绑定Hydrogenophaga intermedia S1；organism_gold对S01–S04均出现Hydrogenophaga intermedia（TaxID 65786）且PATHWAY_COMPLETE=TRUE。物种/菌株身份与整条路径能力对应良好；S04菌株链接在答案中标注为MODEL_INFERENCE/medium，但gold独立列有H. intermedia S04记录，未构成已核身份错误。未给TaxID/genome不是本题必填，且不影响主要微生物推荐，故9而非10。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_064：支持H. intermedia S1在S01–S04的菌株级对应及PATHWAY_COMPLETE=TRUE；不把答案未交付的TaxID/基因组字段回填为答案证据。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_064：支持本案为4步LINEAR_UNIQUE路径，不把全DAG旁支作为微生物对应分母。

</details>

### D4 性状科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案交付10项有值性状、5项诚实null。F1好氧、F5 DSM 5680、F10运动、F11杆状、F12革兰氏阴性、F13不产芽孢、F8/F9路径与酶活均有trait_gold支持或与gold一致；F6仅由好氧/专性好氧间接支持，F7“4-氨基苯磺酸盐作为碳源”未在冻结F7面板中明确出现。F2/F3/F4/F14/F15为null，主要缺口属完整性而非编造。已给内容多数准确，故8分；F6/F7局部未核使9–10不成立。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_064：支持F1、F5、F10–F13及部分F7/F8/F9的观测/预测记录；不支持把F6呼吸方式与F7 4-氨基苯磺酸盐利用直接当作已观测值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_064：支持若干性状子字段的scoreable/completeness_only分层；不把缺失性状自动判为科学错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_064：支持温度/盐度等子字段的可评分与待裁决状态；不用于把答案null回填为已填值。

</details>

### D5 来源与可核查性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案提交了7条evidence_registry并逐步映射：EVID_001–004为LITERATURE_DIRECT，EVID_005为DATABASE_DIRECT，EVID_006明确标MODEL_INFERENCE，EVID_007明确标INTERNAL_KNOWLEDGE_ONLY。关键路线、酶、菌株和多数性状均有locator；但E0不包含这些文献/数据库记录，无法独立核验其存在或支持范围，故登记UNRESOLVED_SOURCE而非错引；S02/S03缺EC、S04菌株链接为模型推断，使D5不能取9–10。无VERIFIED_MIS_CITATION，不触发cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_064：Gold支持部分酶-反应候选，但不核验答案EVID_001–EVID_005的文献/数据库存在性。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_064：Gold支持H. intermedia的菌株/路径事实；不等同于核验答案所交付文献的原文内容。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_064：Gold支持若干性状观测；不把答案EVID_004/EVID_007回填为已核来源。

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案清楚区分LITERATURE_DIRECT、DATABASE_DIRECT、MODEL_INFERENCE、INTERNAL_KNOWLEDGE_ONLY；对S02/S03无确认EC、S04菌株链接仅模型推断、TaxID/基因组/温度/pH/盐度未核、SMILES立体未强制等均作了披露。未见系统性把预测写成实证或掩盖主要矛盾；仅F6/F7等个别confidence可再收紧，故9而非10。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_064：用于对照答案对性状缺失/不确定的披露；不把gold记录回填为答案自己交付的证据。

</details>

## GPT5.6

答案SHA256：`c303024a68d5b9ea899b1026b033277cf5001b256595bd24db9f41b260d42e4e`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面指定4-sulfocatechol degradation主链，gold必答4步；答案只有S1/S2两步，止于cis,cis-muconate，未交付4-sulfomuconolactone水解和maleylacetate还原到3-oxoadipate的S03/S04；15项性状全为null/unknown。路线名正确且两步字段齐全，但主链半截和性状模块缺失，按D1 3–4档取下沿3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：shows only two delivered steps and no S03/S04; does not support a complete four-step main route.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：defines the four-step linear gold main route and terminal 3-oxoadipate; does not support the truncated two-step route.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_064：records four ordered steps for the case; not a full-route content support for the answer.

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1底物/产物与gold S01一致；但S2把3-sulfomuconate直接写成经3-sulfomuconate desulfonase生成cis,cis-muconate+sulfite，跳过gold S02的4-sulfomuconolactone及S03水解、S04还原，并提前进入中心代谢物，未到题面/gold终点3-oxoadipate。主链在中间断裂，属无依据跳跃/核心转化错误，D2关键错误cap≤4；S1部分可用使其高于1–2，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：shows the claimed direct desulfonation to cis,cis-muconate and early termination; does not show the required S03/S04 conversions.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_064：gold S02 product is 4-sulfomuconolactone and S03/S04 lead to 3-oxoadipate; does not support direct cis,cis-muconate as the specified main route.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_064：identifies the case terminal product as 3-oxoadipate; does not support termination at cis,cis-muconate.

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> N=4（S01–S04）。S01交付了3,4-Dihydroxybenzenesulfonate→3-Sulfomuconate及4-Sulfocatechol 1,2-dioxygenase/EC 1.13.11.3，但名称—目标功能及显式EC配对在给定accepted/E0材料中仍为UNRESOLVED，按U处理，不计为S。S02交付3-Sulfomuconate→cis,cis-Muconate+ Sulfite及3-sulfomuconate desulfonase，产物与gold S02目标产物4-sulfomuconolactone不符，程序路线诊断为NONMATCH/SUBSTITUTED_MIDROUTE_FOREIGN，按已核目标反应不符记F。S03、S04未交付，按M记。故S=0、F=1、M=2、U=1，C=S/N=0，落入C04的C&lt;0.20→&#91;1,2&#93;候选带。没有已确认的目标功能支持；仅有一个待核入口步，另一步为不同反应、两步缺失，主推荐不可用，按C05取1而非2。整个酶模块并非未交付，故不记MISSING；已有明确F/M使本维可判，不因S01待核整维NE。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：本题S01–S04的accepted酶名/EC材料：S01 protocatechuate 3,4-dioxygenase type II（1.13.11.3/1.13.11.-）；S02 3-carboxymuconate lactonizing enzyme type 2（5.5.1.2/NOT_OBSERVED）；S03 4-sulfomuconolactone hydrolase（3.1.1.92）；S04 maleylacetate reductase类（1.3.1.32）。仅支持目标酶对应核对，不证明任意具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv：目标主链反应序列与方向：S01 3,4-Dihydroxybenzenesulfonate→3-sulfomuconate；S02 3-sulfomuconate→4-sulfomuconolactone；S03 4-sulfomuconolactone→Maleylacetate；S04 Maleylacetate→3-Oxoadipate。用于核对答案S02产物是否为目标反应产物以及S03/S04是否缺失。
- GOLD_SLICE / formal_cases.tsv：本题为LINEAR_UNIQUE、ordered_step_count=4；仅用于确认本题主链目标步数为4，不把全图旁支当作缺步分母。
- GOLD_SLICE / case_root_identity.tsv：题面指定路线名4-sulfocatechol degradation及gold终端3-Oxoadipate；用于确认目标终点，不用于把答案的替代脱磺酸路线回填为目标完成。
- ANSWER_TEXT / c303024a68d5b9ea899b1026b033277cf5001b256595bd24db9f41b260d42e4e：答案只交付S1–S2；S2主产物为cis,cis-Muconate与Sulfite，并非S02目标4-sulfomuconolactone；S3/S4未见。用于D3a目标交付/缺失与S02产物不符的定位。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Hydrogenophaga intermedia is an exact gold species for all step rows and pathway_complete=TRUE; species-level identity and pathway capability are supported. However the answer adds strain &#x27;S1&#x27; and no TaxID, so it makes a strain-level identity claim with only species-level support (D3b identity ladder ①粒度不足, usually 7-band, no cap). It also uses the same profile for a non-gold S02 reaction, whose step-level capability is unverified. Main correspondence reliable, minor/specific identity items need confirmation -&gt; 7.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：shows the species, an unverified strain token, and no TaxID; does not establish strain-level identity.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_064：supports species Hydrogenophaga intermedia (TaxID 65786) and pathway_complete TRUE; does not provide a strain S1 record.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles&#91;0&#93;.traits的15项全部value=null、confidence=unknown，未交付任何可评价的性状值；按P44/P112全部必需性状为空时D4记MISSING=1，不宣称科学错误；完成度扣分归D1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：shows all 15 required trait values are null/unknown; no trait observation to score.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 唯一证据EVID_001为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null；steps、organism_profiles、route_summary、complete_pathway均引同一内部条目。决策相关组CG01/CG02/CG03/CG05/CG07/CG09全部MISSING_SOURCE，无条目级可定位来源；无已核实错引。按D5 MISSING_SOURCE低分档，重要结论几乎无法定位外部依据，取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：shows only INTERNAL_KNOWLEDGE_ONLY with no database/record/locator; does not provide a locatable source.

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案多处标low/unknown，uncertainties列出氧条件、3-sulfomuconate结构/SMILES、脱磺酸酶EC、菌株/步骤证据、15项性状来源缺口，未把内部知识写成实测。但它把ORG_001设为complete_pathway_organism_profile_id并给出完整路径口吻，和自身仅2步/证据不足相矛盾，部分结论强度超过依据；属局部/单点过度确信而非系统性cap，5–6档取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：shows explicit unknowns and low confidence; does not support the complete_pathway organism flag.

</details>
