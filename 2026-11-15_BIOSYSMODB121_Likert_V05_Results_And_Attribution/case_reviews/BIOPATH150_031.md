# BIOPATH150_031：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：D-galacturonate degradation I

污染物：aldehydo-D-galacturonate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 41.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 68 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 65.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 72 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 76 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 40 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`c1aabb907eee9e12c976776bfe9ba7db8d1c94fd852fd219c828f0cc0c1a6a9d`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> 题面锁定D-galacturonate degradation I；答案虽回显路线名，却给出L-半乳糖酸还原型真菌四步路线，与冻结gold的S05→S03→S04→S01→S02主链步骤、方向和终点不一致。任务路线偏离属D1关键错误；模块虽大体齐全，但任务符合度失败，在&#91;1,4&#93;内取2。

<details><summary>V0.4理由与本行变化背景</summary>

交付完整：S1–S4均给出主底物/主产物（含SMILES）、首选酶（1个EC+3个如实null并说明原因）、每一步步级菌；两个organism_profiles各15项性状；evidence_registry与uncertainties齐备；route_scope.chosen_route_name逐字为题面路线名、氧条件null；JSON必填字段齐备。扣分：主链化学为丝状真菌L-半乳糖酸还原途径，与冻结gold BSY-p00289（细菌D-塔格糖酮酸/D-阿卓糖酸，5步，止于pyruvate+D-glyceraldehyde 3-phosphate）不同；题面仅给路线名而无pathway ID，名称→化学对应在冻结证据中不可核，答案未以&#x27;替代路线&#x27;名义显式声明范围偏离（仅uncertainties承认路线定义凭记忆）。故落7档（大部分必要内容完整、关联清楚），不能给9–10（存在范围偏离待核风险）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_031#question：题面锁定路线名称并要求在该路线下给出主链；不支持改选另一条化学路线。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：冻结gold目标主链的方向、步骤和终点；不支持答案的L-半乳糖酸真菌路线。
- ANSWER_TEXT / ANSWER.steps：答案实际交付的四步替代路线；不支持目标主链完成。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> D2按答案自身化学质量评价：其给出已知真菌还原型D-半乳糖醛酸路线，四步底物/产物、辅因子与方向基本连续；S1 NADPH还原、S2脱水、S3 retro-aldol裂解、S4 NADPH还原甘油，主链化学可成立。但它不是题面冻结目标路线，且部分立体化学未核，故在允许&#91;1,5&#93;内取上限5。

<details><summary>V0.4理由与本行变化背景</summary>

四步化学内部成立：S1醛基NADPH还原（D-galacturonate reductase，伴NADPH/NADP+成对）→L-galactonate；S2 C2-H/C3-OH脱水→2-dehydro-3-deoxy-L-galactonate（+H2O）；S3 retro-aldol裂解C3–C4→pyruvate+L-glyceraldehyde；S4 L-glyceraldehyde经NADPH还原→glycerol。方向一致、原子/电荷与SMILES相符、步骤连接无跳步，辅因子在列（不适用辅因子遗漏条款）。但整链与gold S01–S05（异构酶起始，经tagaturonate/altronate/KDG/KDPG）不同，属未证实替代路线：无条目级证据（EVID_001笼统、EVID_002凭记忆），按四.5第3步登记为未证实，不判错也不给高分；故6档（主干部分成立、合理性证据有限），不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：答案替代路线的底物、产物、辅因子和方向；不支持目标路线完成。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分6 → V0.5新分1，变化-5。

新裁判理由：

> 目标五步中S=0；S01/S03/S04为已确认KEY目标失败，S02/S05为未绑定/未确认（U），答案整体走L-半乳糖酸真菌路线，未交付目标S05异构酶、S03 tagaturonate reductase、S04 altronate dehydratase、S01激酶、S02醛缩酶。按D-KEY4在&#91;1,4&#93;内评分；无任何目标反应支持，取1。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名D-galacturonate reductase+EC 1.1.1.365+gaaA与&#x27;醛基→伯醇&#x27;还原反应类型相符；S2脱水酶对应脱水、S3醛缩酶对应retro-aldol裂解、S4 L-glyceraldehyde reductase对应醛还原，均无EC大类与反应类型矛盾，也无名称-编号互斥；3个无正式EC的酶如实填null并说明，符合任务的null纪律。但EC 1.1.1.365与gaaA/gaaB/gaaC均无冻结记录可核（整题GAP），其余三步无EC/条目级支持——属&#x27;有合理候选和部分支持、关键步骤仍缺具体核验&#x27;的5–6档，取6；不cap（无已核实酶-反应错配）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：冻结目标必需步及其方向；不支持答案替代酶路线。
- ANSWER_TEXT / ANSWER.steps：答案实际酶模块内容；不显示目标反应匹配。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出A. niger（TaxID 5061）和T. reesei（TaxID 51453），物种名称与TaxID是合理候选，且与所答真菌路线相配；但所有步骤微生物归属仅凭internal knowledge/vague literature，单步催化与整路能力无冻结证据，且不是gold目标细菌路线。按5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

步级归属清楚：S1–S3=Aspergillus niger（TaxID 5061，未给菌株）、S4=Trichoderma reesei（TaxID 51453，未给菌株），物种级粒度与其声称粒度基本匹配，未见跨属/跨kingdom或明显编造迹象；A. niger为文献中该真菌途径的模式菌，属&#x27;合理候选&#x27;。但：①TaxID与物种身份无冻结记录可核（GAP-031-039/041），②各步催化能力属反应级声称、整条路径能力属全路径声称，均无对应证据（P69三层不得互相冒充），③complete_pathway_organism_profile_id=ORG_002(T. reesei)与S1–S3归属A. niger不一致（该字段本轮不评分，作一致性瑕疵记录）。故5档（合理候选、关键身份与作用范围未充分核验），不cap（无可核实身份错配）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：答案声明的微生物身份与步骤归属；不支持其催化能力已核。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_031：冻结gold目标路线微生物为细菌；不支持答案真菌身份或能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 两份profile均填15项，若干通用性状（好氧、中温、不运动、真菌细胞壁、A. niger/T. reesei形态）与常识相符，且pH/保藏/基因组件诚实置null；但关键数值与物种级性状无冻结证据，E0对5061/51453无trait records，只能判部分可用、关键项证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

两profile均一次返回15项（ORG_001/ORG_002同为filled 12、explicit_unknown 3、omitted 0：F3_pH、F5、F14为诚实unknown/null）。定量字段（温度/pH/盐度/基因组）一律null，符合&#x27;不确定项为null&#x27;纪律，未编造数值；定性性状（专性好氧、中温偏好、非嗜盐、有氧呼吸O2、可利用D-半乳糖醛酸、植物多糖降解、不运动、有隔菌丝与分生孢子、真菌包膜不适用革兰氏、产孢方式、栖息地广适）与普通真菌学常识一致，未见离谱数值、未见把物种级观测硬写成菌株级定量。扣分：全部性状仅以INTERNAL_KNOWLEDGE_ONLY（EVID_003/004）或笼统文献为据，冻结gold只含细菌物种（Dickeya/E. coli/Pectobacterium等），真菌物种无记录可核（GAP-031-044~051/090~097）；F9对T. reesei的&#x27;Lga1&#x27;活性无来源。故6档（部分性状准确适用但关键项证据不足），不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：答案填写的15项性状及null；不支持其数值已被外部核验。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_031：冻结trait记录覆盖目标细菌TaxID，无5061/51453记录；不能用于确认答案真菌性状。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> EVID_001为无DOI/PMID的泛化文献列表，EVID_002为MetaCyc记忆，EVID_003/004为普通真菌学常识；无条目级可定位记录。决策相关路线/酶/身份组仅有GENERIC/MISSING来源，按D5 3–4档取下沿3。E0 EVIDENCE_GAP，不能把未核当错引/虚构，故不cap。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：EVID_001标LITERATURE_DIRECT但locator只有作者+约年份+基因名，自承&#x27;具体卷期无法核实&#x27;且无DOI/record_id→GENERIC_SOURCE；EVID_002（MetaCyc凭记忆）、EVID_003/EVID_004（普通真菌学常识）为INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE。决策相关组（CORE：CG01/02/03/05/07/09；APPLICATION_CRITICAL：CG08/17及claim级APPLICATION_CRITICAL的CG14）没有任何条目级可定位可核对证据；E0为EVIDENCE_GAP（entries=0），无可核实错引，故severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION、不cap。按P41/P35：决策相关组全部笼统/缺失→3–4档，取3（无任一条目级定位，结论-来源关联很弱）；SUPPORTING组（CG15/16/18/19/20）单独登记，不跨档上调。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案实际交付的来源记录；显示泛化文献与internal knowledge，无条目级定位。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案在uncertainties中明确MetaCyc路线为记忆、S4边界不确定、EC/基因/TaxID未实时核对、性状无来源、SMILES立体可能误差，并区分INTERNAL_KNOWLEDGE_ONLY与低置信；主要限制披露具体诚实。个别高/中置信标签仍略强于来源，故取8而非9–10。

<details><summary>V0.4理由与本行变化背景</summary>

正面：uncertainties逐条说明路线定义凭记忆、S4是否属该途径边界、三个酶无正式EC故null、EC/TaxID/基因名均未实时核对、性状缺可引来源、SMILES立体化学可能误差；多数酶/菌/性状confidence=medium，未知项如实置null/unknown，未发现把预测当观测的系统性表述或掩盖矛盾。扣分：S1酶confidence=high却同时自述&#x27;EC 1.1.1.365与gaaA未实时核对&#x27;；EVID_001把凭记忆的文献列表标为LITERATURE_DIRECT（来源类型轻度膨胀）；route_summary以确定语气陈述路线身份（其不确定性放在别处）。属单点过度确信+局部证据类型膨胀，非系统性误导，档内扣。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案对记忆、边界、未核编号、SMILES和性状来源限制的披露；支持D6主要限制已说明。

</details>

## DeepSeek

答案SHA256：`01a5bb0b9f2420b5905538e3d9a04e4c6337c7733ccf2648367fc368e645ab9d`。

### D1 完整性与任务符合度：10 / SCORED

V0.4旧分8 → V0.5新分10，变化+2。

新裁判理由：

> 题面指定路线与终点；答案给出5步完整主链，逐步含底物/产物英文名与SMILES、首选酶及EC、对应微生物；仅一个E. coli K-12 MG1655 profile并去重引用；15项性状字段齐全，未知项按null/unknown处理；JSON结构与交付格式符合要求。无重要遗漏或范围偏离，D1取9–10档上沿10。

<details><summary>V0.4理由与本行变化背景</summary>

五步主链均含主底物/产物英文名+SMILES、酶名+EC+gene、微生物三件套；15项性状全出现（13填+2诚实null）；route_scope.chosen_route_name原样填题面指定路线名。结构完整、模块齐全，属7–8档较好水平；扣分点在于任务说明第6条要求无可靠来源时填null并将confidence置low/unknown，答案却以INTERNAL_KNOWLEDGE_ONLY作为evidence_id并在核心步骤标high confidence，交付合规略有偏离。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 01a5bb0b9f2420b5905538e3d9a04e4c6337c7733ccf2648367fc368e645ab9d：答案包含5个步骤，每步有底物/产物、首选酶及EC、对应微生物；只有一个去重后的ORG_001 profile且15项性状字段均出现（部分未知按null/unknown）。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_031：该gold案例为LINEAR_UNIQUE且ordered_step_count=5；仅用于核对本题主链长度与案例身份，不要求交付全图旁支。
- SCOPE_ROW / SCOPE#BIOPATH150_031#CG04：题面氧条件为null（未指定）；D1不因未指定氧条件判定任务偏离。
- RUBRIC_CLAUSE / P17：档内选分原则：按实际完成度取档内高分，不因篇幅或术语额外加分。
- RUBRIC_CLAUSE / P100：D1评价任务模块完成度、路线/条件遵守与交付完整性；D2另评化学正确性。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 主链五步与gold方向、顺序一致：S1醛式-D-半乳糖醛酸→D-tagaturonate异构化；S2 D-tagaturonate+NADH→D-altronate+NAD+还原；S3 D-altronate→2-dehydro-3-deoxy-D-gluconate+H2O脱水；S4加ATP磷酸化→6-磷酸；S5 KDPG醛缩酶裂解→pyruvate+D-甘油醛-3-磷酸。关键转化、方向、连接和终点均成立，辅因子基本在列；SMILES未完整标注立体化学/电荷为局部表示问题，不推翻主链。因程序允许D2最高&#91;1,8&#93;且nine_ten=false，取7–8档上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

五步主链化学正确且与gold反应序列一致：醛糖→酮糖异构化(S1)、NADH依赖还原(S2)、脱水生成2-脱氢-3-脱氧-D-葡萄糖酸(S3)、ATP磷酸化(S4)、KDPG醛缩裂解为丙酮酸+3-磷酸甘油醛(S5)，方向正确、C数守恒、连接连续，终点与gold terminal（pyruvate+D-glyceraldehyde 3-phosphate）吻合。辅因子NADH/NAD+、ATP/ADP已在列，仅H+未显式配平属局部计量缺陷（7–8档级，不cap）；主链与终点完整故取9档而非10（氧化还原计量未完全写全）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 01a5bb0b9f2420b5905538e3d9a04e4c6337c7733ccf2648367fc368e645ab9d：答案五步链：aldehydo-D-galacturonate→D-tagaturonate→D-altronate→2-dehydro-3-deoxy-D-gluconate→6-磷酸→pyruvate+D-glyceraldehyde 3-phosphate；含NADH/NAD+、H2O、ATP/ADP，主成员有SMILES。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：gold反应行显示同一组五步有向转化：S05入口异构化、S03还原、S04脱水、S01磷酸化、S02醛缩裂解；用于核对化学方向与连续性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：accepted酶集合与答案所列异构酶、还原酶、脱水酶、激酶、醛缩酶家族/EC相符；不用于证明具体蛋白实测活性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_031：gold根为aldehydo-D-galacturonate，terminal主产物为Pyruvate与D-glyceraldehyde 3-phosphate；答案到达相同终点。
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏通常属局部计量缺陷；本答案主要辅因子已在列，不触发cap。
- RUBRIC_CLAUSE / P100：D2评价反应化学本身（转化、方向、守恒、连续性），与D1任务符合度分轴。
- RUBRIC_CLAUSE / P17：档内选分原则：先定档再按实际表现取档内分，不因文字量加分。

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 五个必答步的显式EC/酶名均能在给定accepted集合中找到对应：S1(5.3.1.12)、S2(1.1.1.58)、S3(4.2.1.7)、S4(2.7.1.45)、S5(4.1.2.14)，对应gold S05/S03/S04/S01/S02的已接受酶行，达到G4功能/EC级支持。故给&#91;7,8&#93;带上沿8；但表示等价仍为ROUTE_HOLD_REPRESENTATION，且gene_or_protein与TaxID附加声称未核，9-10证据门不成立。

<details><summary>V0.4理由与本行变化背景</summary>

五步酶-反应对应与EC均与gold enzyme_gold相符：S1 5.3.1.12(D-glucoronate/D-galacturonate isomerase)、S2 1.1.1.58(tagaturonate reductase)、S3 4.2.1.7(D-altronate dehydratase)、S4 2.7.1.45(∈gold多注集合{2.7.1.178,2.7.1.45})、S5 4.1.2.14(∈gold多注集合{4.1.2.55,4.1.2.14})；酶名与EC一致、功能类型匹配。gold为多注集合时答案选集内号按四.5保守条款接受。gene标识(uxaC/uxaB/uxaA/kdgK/eda)为附加标注，冻结gold未列，作待核不降主判。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：支持五步酶名/EC属于已列accepted酶行；不证明任意具体蛋白实验活性或SMILES表示等价。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：支持五步反应名称/方向与主链顺序；不证明答案未指定立体/电荷的SMILES与gold精确同构。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> gold organism_gold显示Escherichia coli（TaxID 562）可对应全部五步反应，并作为PATHWAY_COMPLETE出现；答案使用E. coli的菌株K-12 substr. MG1655/TaxID 511145，属同物种更细粒度声称。物种级身份/路径能力有支持，但菌株级TaxID与具体菌株能力记录在EVIDENCE_GAP中不可核，按身份阶梯的粒度不足档内扣，给7。

<details><summary>V0.4理由与本行变化背景</summary>

每步微生物均为Escherichia coli：gold organism_gold的5个STEP均含Escherichia coli，且E. coli(taxid 562)在PATHWAY_COMPLETE中，故物种级身份与步级归属有可靠依据、整路径能力在物种层面成立。不足在于答案进一步声称菌株K-12 substr. MG1655 / TaxID 511145，属菌株级粒度声称，冻结证据无该菌株级记录（GAP-031-040），按D3b身份阶梯①粒度不足处理——物种级真实记录支持菌株级声称，档内扣、不cap；主要微生物推荐未被推翻。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_031：支持E. coli物种级对五步反应及PATHWAY_COMPLETE的对应；不支持K-12 MG1655菌株级TaxID 511145或该菌株专属能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> E. coli物种级gold支持若干性状：facultative anaerobe(F1预测)、rod-shaped(F11)、Gram-negative(F12)、non-sporulating(F13)。但答案针对K-12 MG1655填写的F2 optimum 37、F3 optimum 7.0、F5 ATCC 47076、F7 D-galacturonate/D-glucuronate利用、F8/F9路径相关能力、F14具体NC_000913.3数值与F15栖息地，在本案EVIDENCE_GAP/物种级gold中不能核验；存在部分准确但关键项证据不足与条件解释需修订，按5-6档给6。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状多为E. coli口径且方向正确：F1 facultative anaerobe、F6兼性厌氧+氧受体、F11杆状、F12革兰阴性、F13不产孢与trait_gold物种级一致；F2嗜温/37℃、F3 pH 7.0、F5 ATCC 47076、F7利用半乳糖醛酸/葡萄糖醛酸、F14 NC_000913.3/4641652bp/50.8%合理；F8/F9/F15表述合理。F4盐度与F10运动性为诚实null（完整性归D1，不重复重扣）。弱点：多数性状来自INTERNAL_KNOWLEDGE_ONLY，菌株级未核，部分数值为物种级推广，按四.4同物种代表记录条款可接受但不回填来源。取7档（主要性状可核实且适用，存在少量待核与条件解释问题）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_031：支持E. coli物种级F1/F11/F12/F13等observed/predicted性状；不代表K-12 MG1655菌株所有数值，不把培养温度范围当最适值。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_031：说明温度/pH等子字段多为范围或pending，不能作为精确optimum的已核支持。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 核心路线、酶、微生物与多数性状的evidence_registry使用EVID_001/EVID_003的INTERNAL_KNOWLEDGE_ONLY且无locator，属MISSING_SOURCE；仅F14给出NCBI NC_000913.3这一具体记录，但EVIDENCE_GAP无法核验，属UNRESOLVED_SOURCE。决策相关核心组几乎无可定位来源，落1-2档；因仍有一个基因组定位符，取2而非1。无已核实错引，不触发D5 cap。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关核心组（CG01路线步骤/CG02起点/CG03终点/CG05酶-EC/CG07核心微生物身份）在答案侧的证据均指向EVID_001=INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE；性状组同为EVID_003=INTERNAL_KNOWLEDGE_ONLY。仅F14基因组有EVID_002=DATABASE_DIRECT(NCBI NC_000913.3)可定位，属个别可核对条目。核心结论几乎无法沿答案交付记录追查，落入1–2档低分段；MISSING_SOURCE默认不触发关键错误cap，故不判KE。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示EVID_001/EVID_003为INTERNAL_KNOWLEDGE_ONLY、EVID_002为NCBI NC_000913.3；该定位符本身尚未在冻结快照中核验。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案明确写出两条不确定性：SMILES未标立体、部分表型来自内部知识未逐项附原始文献；对F4/F10等也标null/unknown，具备一定披露。但五个核心步骤的酶/微生物仍以high confidence配INTERNAL_KNOWLEDGE_ONLY，多个菌株级性状以medium/high置信度填写而未被识别为未核，关键表示/K-12身份限制未充分披露；属“有不确定性说明但部分结论强度超过依据”，5-6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

答案有uncertainties披露（SMILES未标立体化学、部分表型性状来自内部知识未逐项附原始文献），且来源类型诚实标为INTERNAL_KNOWLEDGE_ONLY而非伪装数据库，属正面披露；但全部步骤酶/微生物confidence标high、性状多为medium/high，而其依据为内部知识/未核，结论强度整体超过证据，属&#x27;部分结论强度仍超过依据&#x27;的5–6档情形，档内扣分，未构成系统性把预测写成实证的误导（不cap）。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持答案已披露SMILES立体缺失与部分性状仅内部知识；不支持其所有high/medium置信度均与证据相称。

</details>

## Kimi

答案SHA256：`bbd87e77438a8739522438c51c25deade05e0594182413fcda18371af2934bbe`。

### D1 完整性与任务符合度：10 / SCORED

V0.4旧分9 → V0.5新分10，变化+1。

新裁判理由：

> 五步主链完整交付，route_scope.chosen_route_name原样为D-galacturonate degradation I，每步均有底物/产物英文名与SMILES、首选酶及EC、对应微生物；同一物种+菌株的单一ORG_001 profile去重复用，15项性状全部出现。未发现必要模块遗漏或交付格式偏离。

<details><summary>V0.4理由与本行变化背景</summary>

五步主链齐全（S1–S5），每步给出主底物/主产物英文名与SMILES、首选酶含EC与基因名、对应微生物含菌株与TaxID；15项性状全部填写；evidence_registry（5条）与uncertainties（4条）均交付；route_scope.chosen_route_name与题面给定的&#x27;D-galacturonate degradation I&#x27;逐字一致，未改选路线；氧条件null如实保留并在notes说明。无必要模块缺失、无占位或复读；少量字段质量缺陷（SMILES碳数、部分性状数值）归D2/D4，不在此重复扣分。故判9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：题面锁定D-galacturonate degradation I，要求主链、每步底物/产物英文名与SMILES、首选酶及EC、对应微生物、15项性状
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_031：ordered_step_count=5、LINEAR_UNIQUE、n_required=5，支持单条主链完整性核验
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_031：root=aldehydo-D-galacturonate，terminal=Pyruvate|D-glyceraldehyde 3-phosphate
- ANSWER_TEXT / ANSWER.steps&#91;1-5&#93;：五步均列出底物/产物name与smiles、enzyme.name/ec_number、microorganism，并用ORG_001复用
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：单一E. coli K-12 MG1655 profile包含全部15项性状

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 主链名称顺序、反应方向、酶/EC及终点大体正确，但结构SMILES出现多步实质错误：S1底物比gold root多一个CH2（7C vs 6C）；S2产物D-altronate为7C且末端写为醛，而gold D-altronate为6C并含CH2OH；S3以7C D-altronate生成6C KDG+water，未说明碳损失，构成明显原子不守恒。按D2关键错误上限≤4；因名称级主链仍可辨认，取4而非3。D2九到十分门false，不进入9–10。

<details><summary>V0.4理由与本行变化背景</summary>

主干与gold BSY-p00289五步一一对应且顺序正确：S1 isomerase（aldehyde-D-galacturonate→D-tagaturonate，对应gold S05）→S2 reductase（D-taguronate→D-altronate，gold S03）→S3 dehydratase（D-altronate→KDG，gold S04）→S4 kinase（KDG→KDG-6-P，gold S01）→S5 aldolase（KDG-6-P→pyruvate+D-glyceraldehyde 3-phosphate，gold S02）；终点与gold terminal完全一致；NADH/NAD+、ATP/ADP辅因子与H2O副产物在列，方向无反转。扣分点：S1底物、S1产物D-taguronate、S3底物D-altronate三处SMILES按原子计数均为7碳（gold root与中间体为6碳），在S3形成7C→6C+H2O的碳不守恒；但化合物名称、转化类型与连接顺序仍正确，主链主要结论未被推翻，属局部结构表达缺陷（7–8档取低）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_031：gold root isosmiles为6碳aldehydo-D-galacturonate；terminal为pyruvate与D-glyceraldehyde 3-phosphate
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：S05 isomerase: aldehydo-D-galacturonate(6C)-&gt;D-tagaturonate(6C); S03: D-tagaturonate+NADH-&gt;D-altronate+NAD+; S04: D-altronate(6C)-&gt;KDG(6C)+H2O; S01: KDG+ATP-&gt;KDG-6P+ADP; S02: KDG-6P-&gt;pyruvate+G3P
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：accepted enzyme/EC sets include 5.3.1.12,1.1.1.58,4.2.1.7,2.7.1.45/2.7.1.178,4.1.2.14/4.1.2.55
- ANSWER_TEXT / ANSWER.steps&#91;S1-S3&#93;：S1底物SMILES含额外CH2（7C）而gold root为6C；S2产物D-altronate为7C/末端醛而gold D-altronate为6C/CH2OH；S3底物7C-&gt;KDG6C+H2O，碳不守恒

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> Manual mapping: answer S1/S2/S3/S4/S5 correspond to gold S05/S03/S04/S01/S02. All five explicit ECs (5.3.1.12, 1.1.1.58, 4.2.1.7, 2.7.1.45, 4.1.2.14) and enzyme names match the accepted sets at function level. Score 8 is within the allowed &#91;1,8&#93;; 9-10 is blocked by representation/E0 gaps.

<details><summary>V0.4理由与本行变化背景</summary>

五个EC与gold多注集合逐一对上：S1 5.3.1.12（gold S05，UXAC-MONOMER）、S2 1.1.1.58（gold S03）、S3 4.2.1.7（gold S04）、S4 2.7.1.45（gold S01集合{2.7.1.178,2.7.1.45}内，按四.5多注集合条款选集内号不扣分）、S5 4.1.2.14（gold S02集合{4.1.2.55,4.1.2.14}内）；酶名与反应类型（异构/酮基还原/脱水/磷酸化/醛缩）自洽，基因uxaC/uxaB/uxaA/kdgK/eda与EC的对应与gold gene-enzyme定位一致，无EC大类与反应类型错配。E0整题无EC条目（GAP-031-006/008/010/013/016），accepted name/条目状态未能机器核验，属局部未核而非错误，故不给满分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：Gold lists the accepted enzyme names and ECs for the five required steps; supports function-level matching, not specific protein activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：Gold gives directed reactions; supports mapping answer steps to the required chain, with S01/S02 stereo unresolved.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Gold supports E. coli species-level identity and pathway-complete status (taxid 562). The answer uses E. coli K-12 MG1655 taxid 511145 for all steps. Species-level records support the species claim but not the strain-level taxid/whole-pathway claim, so this is a within-grade deduction under the D3b identity ladder, not a cap; no cross-species or unrelated-taxon error is present.

<details><summary>V0.4理由与本行变化背景</summary>

五步统一推荐Escherichia coli K-12 MG1655（TaxID 511145），gold organism_gold对S01/S02/S03/S04/S05均有E. coli（taxid 562）物种级记录，且PATHWAY_COMPLETE含E. coli，物种选择有据，未把单步菌写成跨物种全路径菌，也未出现跨属/无关类群身份。但答案交付的是菌株级身份与菌株级TaxID，gold仅有物种级（562）记录，属D3b身份阶梯①粒度不足——档内扣分（约7档），默认不cap；TaxID 511145本身在E0无冻结记录（GAP-031-040/042），只能记UNRESOLVED待核，未核≠错，故不按②③档处理。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_031：Gold lists E. coli species taxid 562 for relevant step enzymes and PATHWAY_COMPLETE; it does not verify strain K-12 MG1655 taxid 511145.

</details>

### D4 性状科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> All 15 traits are filled. Most match E. coli species-level gold: facultative anaerobe, motility, rod morphology, Gram-negative, non-sporulating, mesophilic preference, pH/salinity ranges, and carbon-source utilization. Exact K-12 MG1655 ATCC/genome and several optima are unverified under E0, but not contradicted; same-species representative trait use is allowed. Score 8 reflects strong trait coverage with local unverified exact values.

<details><summary>V0.4理由与本行变化背景</summary>

可核性状与gold 562观察记录一致：F1兼性厌氧（aerotolerant=true/facultative anaerobe=true）、F10有运动性（motility=true）、F11直杆状（rod-shaped）、F12革兰氏阴性（gram positive=false）、F13不产芽孢（sporulation=false）、F7/F8葡萄糖等糖利用与降解（degradation: glucose=true）；F6兼性厌氧与O2末端受体与gold兼性厌氧一致。数值项F2最适37℃、F3最适7.0、F4最适0.5% NaCl在gold仅有range/端点记录且子字段待老师冻结range政策，不能判错也不能默认正确，答案已对盐度标low；F5 ATCC 700926、F14 NC_000913.3/4641652bp/50.8%在E0无记录（GAP-031-002/003）→UNRESOLVED；F9把途径酶（UxaC/UxaB/UxaA/KdgK/Eda）当作&#x27;酶活&#x27;性状属轻度类别混用；F15低置信、gold该字段UNKNOWN（不构成矛盾）。主要性状适用、关键缺口集中于不可核数值→7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_031：Gold gives E. coli species-level trait observations/predictions; supports species-level comparisons, not strain-specific exact ATCC/genome/optimum values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_031：Masks indicate which trait fields are observed-accuracy versus completeness-only; helps avoid treating unscoreable subfields as errors.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> Core route, enzyme and identity claims cite MetaCyc/EcoCyc/BacDive pathway or gene lists without record IDs; some modules provide exact NC_000913.3 and ATCC 700926, but E0 is EVIDENCE_GAP and cannot verify them. No verified mis-citation is present. This fits the 5-6 partial-traceability band; choose 5 because decision-relevant core groups are mostly generic or unresolved and lack official verification.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09/CG17）中，路径与酶组仅给数据库名+途径名/基因名，EVID_001（MetaCyc）、EVID_002（EcoCyc）、EVID_003（BacDive）的record_id均为null，答案自述&#x27;MetaCyc/EcoCyc途径的内部记录号未引用具体ID，以途径名称定位&#x27;→GENERIC_SOURCE；CG17（NC_000913.3）与CG07（ATCC 700926、TaxID 511145）虽有条目级编号，但E0整题EVIDENCE_GAP无法核对→UNRESOLVED_SOURCE。按四.3/P41：决策相关组全部仅有笼统来源、无条目级可核对结论→3–4档；无经核实错引（未核≠虚构，不判CONTRADICTED），不触发cap，取4档（因给出具体途径名、五个基因名与两个条目号，可追溯性明显强于纯库名，取本档上限）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Answer supplies database names, pathway/gene locators, exact NCBI accession and ATCC number; does not supply record IDs for core MetaCyc/EcoCyc/BacDive claims.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> The answer lists specific uncertainties: open-chain versus pyranose balance, omitted NADH/NAD+ SMILES, low-confidence salinity optimum, and missing internal record IDs. However many enzyme/taxid/genome claims are marked high confidence while resting on generic database locators or E0-gap records. This is single-point overconfidence, not systemic prediction-as-observation, so 6 within the 5-6 band.

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且诚实：uncertainties四条分别说明开链/吡喃环平衡、NADH/NAD+ SMILES缺失及其原因、盐度最适值为常用培养近似（已标low）、并主动承认MetaCyc/EcoCyc未引用record_id只以途径名称定位；置信度有分层（盐度/栖息地low，数值项medium，酶/菌high），未把预测写成实验观测，未掩盖与gold的差异（替代分支标注is_part_of_scored_main_route=false）。不足：TaxID 511145、ATCC 700926、NC_000913.3等不可核身份/基因组字段统一标high且未声明其为待核数据库直查；多数step.uncertainty为null，披露集中于全局数组。属单点过度确信（多处仍有具体披露），非系统性误导，按D6严重度条款档内扣、不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Answer provides concrete uncertainty notes and confidence labels; high-confidence labels on unresolved exact identifiers remain overconfident.

</details>

## Qwen

答案SHA256：`9b6ae874dbf4b7a91bf14d2f90ed8787e8aa3dc0e86604063b557fbc9565586b`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 题面要求的五个主链步骤、每步底物/产物/酶/EC/微生物、同一菌去重profile及15项性状外壳均已回应，route_scope.chosen_route_name原样填写；11项性状有值、4项按题面允许显式unknown，0遗漏。完成度良好，但4项性状未知及D1/D2表征边界hold使其不到9–10。

<details><summary>V0.4理由与本行变化背景</summary>

五个必答模块均实质交付：steps共5步，每步含主底物/主产物英文名与SMILES、一个首选酶含EC、一个对应微生物；organism_profiles按物种+菌株去重为1条并含全部15项性状（11项填写、F3/F4/F5/F10为明确未知null，按P15明确未知不计遗漏）；evidence_registry 4条、uncertainties 3条；route_scope.chosen_route_name原样为“D-galacturonate degradation I”，未改选路线。扣分点仅局部：4项性状来源空缺、S4磷酸化未列H+产物的计量字段、部分证据仅为内部知识自称。属9档（全部适用要求实质回应、对应明确、无重要遗漏或范围偏离），未取10因局部字段完整性有瑕疵。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案实际交付的步骤、酶、微生物、性状外壳与未知/null声明；不证明其科学正确性。
- QUESTION_TEXT / QUESTION_BEGIN：支持题面对五步主链、每步酶/EC/微生物及15项性状的交付要求。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_031：支持本题为线性唯一、5个必答步；不作为旁支全图覆盖率分母。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 主链方向与顺序正确：醛式-D-半乳糖醛酸→D-塔格糖醛酸→D-阿卓糖酸→KDG→KDG-6-P→丙酮酸+D-甘油醛-3-磷酸；S2补NADH/H+/NAD+，S4补ATP/ADP，S3列H2O副产物，终点与gold terminal一致。局部缺陷是SMILES多未标立体化学、部分为简化非异构表示，结构表征处于representation boundary hold；主链化学与连续性仍成立，故7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold五步一致：aldehydo-D-galacturonate→D-tagaturonate（异构，EC 5.3.1.12）→D-altronate（NADH/H+还原，EC 1.1.1.58）→2-dehydro-3-deoxy-D-gluconate（脱水，副产物水）→6-磷酸（ATP磷酸化）→pyruvate + D-glyceraldehyde 3-phosphate（醛裂解）；顺序、方向、碳数与末端化合物均与gold（terminal=Pyruvate|D-glyceraldehyde 3-phosphate(2-)）吻合，SMILES主链与gold canonical结构一致。S2列NADH/H+→NAD+、S4列ATP→ADP、S3列水，属辅因子大体在列；局部计量缺陷（S4未列H+、立体化学未标注且已在uncertainties披露）按P103/P105不超过7–8档逻辑，本维主结论不受影响，取9档（终点合规、辅子基本在列、另列下游）；未取10因氧化还原/电荷计量不完整。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案实际给出的底物/产物、辅因子、方向与终点；不支持未给出的立体化学细节。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：支持gold主链定向反应、主底物/主产物和终点；不自动证明答案SMILES的立体化学完整。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_031：支持根底物aldehydo-D-galacturonate与终点Pyruvate/D-glyceraldehyde 3-phosphate。

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 按accepted sets与enzyme_gold核：S1 uronate isomerase/EC5.3.1.12、S2 tagaturonate reductase/EC1.1.1.58、S4 KDG kinase/EC2.7.1.45、S5 KDPG aldolase/EC4.1.2.14的酶名/EC与gold/accepted相符；S3 altronate dehydratase的EC写作4.2.1.8，而accepted/gold为4.2.1.7，构成一个已核酶-EC配对错误。整体不是全错，主酶名与反应方向大体成立，按&#91;1,8&#93;内7分；不触发KEY4硬上限，因为目标反应本身已交付且酶名正确，错误集中在EC编号。

<details><summary>V0.4理由与本行变化背景</summary>

五个步骤的酶-反应类型均匹配：异构酶EC 5.3.1.12、还原酶EC 1.1.1.58、脱水酶4.2.1.-、激酶EC 2.7.1.45（gold多注集合含2.7.1.45）、醛裂解酶EC 4.1.2.14（gold多注集合含4.1.2.14），无“EC大类与反应类型不匹配”或“酶名与EC互相矛盾”情形。唯一实质待核点：S3把altronate dehydratase标为EC 4.2.1.8，而gold同一酶（BSY-e02250 D-altronate dehydratase）为EC 4.2.1.7；E0无官方EC accepted name/reaction记录，按P66/P71不得据gold数字不等直接判错，登记UNRESOLVED待核。综合取7档（主要步骤酶对应有可靠支持，少量条目需进一步确认），不cap、不连坐D5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案五个酶名/EC的实际交付文本。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：支持gold各步酶名/EC；S04明确为D-altronate dehydratase EC4.2.1.7，不支持EC4.2.1.8。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：支持各步定向反应与主底物/主产物；用于判断所答酶是否对应该反应，不证明具体蛋白实测活性。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案所有步骤使用同一Escherichia coli K-12 substr. MG1655（TaxID 511145）profile；gold在物种级E. coli（TaxID 562）对五步酶均给出EXACT organism，并有PATHWAY_COMPLETE行，支持“E. coli可走该路径”的物种级身份/能力。缺陷是答案把声称下沉到K-12 MG1655菌株级（511145）和整路径能力，冻结材料没有该菌株级记录；按D3b身份阶梯的粒度不足处理，档内取7，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

五步均归属Escherichia coli K-12 substr. MG1655，且gold对五个步骤均有Escherichia coli（TaxID 562）物种级酶-菌记录，gold PATHWAY_COMPLETE亦含E. coli（562，pathway_complete=TRUE），故“E. coli可走该路线”的物种级推荐有可靠支持。但答案给的是菌株级身份（TaxID 511145）与“单一菌株完成整条路径”的能力声称；gold仅提供物种级代表记录，菌株级511145在E0无冻结记录（GAP-031-001/040/043），按P52同物种代表记录口径与D3b身份阶梯①（粒度不足、记录真实且同lineage）→档内扣、默认不cap；未发现跨属/无关类群错配迹象，也不得据记忆放行菌株级身份。取7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案把同一菌株用于五步并声称complete pathway。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_031：支持E. coli（562）在五步均为EXACT organism且有PATHWAY_COMPLETE行；不支持TaxID511145菌株级等同。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_031：支持本题为线性唯一5步主链；不证明任一具体菌株完成整路径。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 已填性状中F1兼性厌氧、F6有氧呼吸兼厌氧发酵且末端受体oxygen、F11杆状、F12革兰氏阴性、F13不产孢与gold物种级E. coli观测相容；F2温度偏好中温、F14 K-12 MG1655的U00096.3/4641652 bp/50.8%及F7/F8/F9/F15的菌株级表述缺冻结菌株级证据。F3/F4/F5/F10为显式null，按题面允许，完成度已归D1。主要性状可核，关键项存在菌株级未核，7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

已填11项性状多数与gold E. coli物种级代表记录相容：F1“兼性厌氧”（gold 562 facultative anaerobe=true、aerotolerant=true）、F11杆状、F12革兰氏阴性（gram positive=false）、F13不产孢（sporulation=false）；F2 optimum 37℃/中温与gold 562温度范围0–42℃、mesophilic一致（gold未给最适值，按“培养/观测温度≠最适”口径不作定量核对）；F6“有氧呼吸兼厌氧发酵/末端受体oxygen”与gold兼性厌氧及硝酸盐还原背景不矛盾；F7/F8/F9围绕半乳糖醛酸/葡萄糖醛酸降解与相应酶活，与gold物种级代谢背景相容。F3/F4/F5/F10为明确未知null，按P15不与错误等同。主要扣分点：F14以“DATABASE_DIRECT/high”给出菌株级U00096.3、4641652 bp、GC 50.8%，E0无该条目（GAP-031-069…074及TAXID:511145缺口），菌株级数值待核；F15栖息地描述gold 562为UNKNOWN，属未核实一般性陈述。取7档（主要性状可核实且适用于物种对象，少量条件/粒度问题），不作预测冒充观测的系统性判定。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案实际填写的15项外壳、11项有值/4项显式null及confidence/evidence_id。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_031：支持E. coli物种级F1/F6/F11/F12/F13等观测；不提供K-12 MG1655菌株级U00096.3记录。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_031：支持温度/盐度等子字段中哪些仅有范围或待裁决；说明不能把范围端点自动当最适/极限。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案交付了来源层：EVID_001 MetaCyc路线名、EVID_002 NCBI Taxonomy 511145、EVID_003 RefSeq U00096.3、EVID_004 INTERNAL_KNOWLEDGE_ONLY。部分关键结论有可定位指向（TaxID/Genome ID/路线名），但EVID_001缺record_id且被复用于酶/traits，EVID_004仅内部知识，E0为整题EVIDENCE_GAP，无法核对条目内容。无已核实错引或虚构，故不cap；按部分关键结论可定位、其他模块缺映射，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付4条证据登记，且与结论映射明确：EVID_001（MetaCyc“D-galacturonate degradation I”，claim_scope含route/steps/enzymes/碳源/降解能力/酶活）、EVID_002（NCBI Taxonomy 511145，仅身份/ncbi_taxid）、EVID_003（RefSeq U00096.3，仅F14）、EVID_004（INTERNAL_KNOWLEDGE_ONLY，覆盖7项性状）。决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09/CG17）为“命名具体但当前冻结证据无法核对”的UNRESOLVED_SOURCE；性状相关组（CG10–CG16）主源为内部知识自称，登记MISSING_SOURCE；不存在已核实错引，故severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION、不cap。因来源与结论关联明确（非纯笼统库名）但均不可核对，且决策相关组无条目级已核实支持，取5档（部分关键结论可定位、其余缺映射与可核对记录）；不取3–4档因非“仅笼统库名/文献列表”情形。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案实际交付的数据库名、record_id、locator、claim_scope、confidence和内部知识声明。
- SCOPE_ROW / SCOPE#BIOPATH150_031#CG04：支持本题氧条件条件组登记为FALSE/SUPPORTING；不等同于来源已核验。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：可作为来源核验对照，但不回填为答案原交付来源，也不替代E0缺口。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> uncertainties明确写出氧条件未指定、部分酶/菌株表型未逐项核实、SMILES未标立体化学；多数未知性状显式null，evidence_registry区分DATABASE_DIRECT与INTERNAL_KNOWLEDGE_ONLY，confidence以medium/low/unknown为主，F14标high。存在F14/F7/F8/F9等菌株级声称偏强，但并非系统性把预测写成实证或掩盖已知矛盾；7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案提供了不确定性披露（uncertainties：氧条件未指定、部分酶基因与菌株表型未逐项核实、SMILES未标注立体化学），并在证据层区分DATABASE_DIRECT与INTERNAL_KNOWLEDGE_ONLY、逐条标confidence，未把预测说成实验观测，也未掩盖与自己结论冲突的已知信息——属部分诚实披露。不足：披露偏笼统，未逐字段列出待核项；F14以“数据库直查+high”包装菌株级具体数值，而E0无对应记录，构成单点过度确信（按P119档内扣、不cap）；性状多处medium置信但来源为内部知识。综合取6档（有不确定性说明但笼统，部分结论强度略超依据），不作系统性误导判定。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案对未知、null、证据类型和confidence的实际表述。
- QUESTION_TEXT / QUESTION_BEGIN：支持题面允许不确定项填null、要求区分未知与编造。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_031：用于判断哪些性状有观测/预测背景；不把未核菌株级声称升级为已证。

</details>

## Grok

答案SHA256：`262ccddf3acf759ed9befe267f5f475448466867bba918ec2e829ffbd541022f`。

### D1 完整性与任务符合度：10 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Answer delivers a complete five-step JSON main route with substrate/product names and SMILES, one enzyme name and EC per step, and a de-duplicated organism profile for all steps. route_scope.chosen_route_name exactly matches D-galacturonate degradation I and oxygen_condition null is preserved. All 15 traits are present. Optional branches are explicitly marked as not part of the scored main route. No material task or format omission observed.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_031：Gold shows 5 ordered required steps for this case; not a provenance source for the answer.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_031：Gold root/route identity matches the question route name; does not verify all answer details.
- ANSWER_TEXT / answer.steps&#91;1-5&#93;：Confirms delivery of the five requested steps, enzyme/EC fields, microorganism fields and 15 traits.

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The five transformations are in correct degradative order and match gold directed chemistry: isomerization to D-taguronate, NADH-dependent reduction to D-altronate, dehydration to 2-dehydro-3-deoxy-D-gluconate, ATP-dependent phosphorylation to the 6-phospho intermediate, and aldol cleavage to pyruvate plus D-glyceraldehyde 3-phosphate. Cofactors and byproducts are represented, the terminal products match the gold endpoint, and alternative branches are clearly excluded from the scored route. No chemistry cap is present.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：Supports gold reaction direction, main substrates/products, and terminal products; does not prove specific protein activity.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_031：Confirms the gold terminal compounds pyruvate and D-glyceraldehyde 3-phosphate.
- ANSWER_TEXT / answer.steps&#91;1-5&#93;.reaction_type：Shows the answer&#x27;s delivered chemical sequence and cofactor handling.

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All five target reactions have answer enzyme name/EC pairs matching the supplied accepted sets at G4 curation granularity: EC 5.3.1.12 for the entry isomerase, EC 1.1.1.58 for tagaturonate reductase, EC 4.2.1.7 for altronate dehydratase, EC 2.7.1.45 for the kinase, and EC 4.1.2.14 for the aldolase. Thus the major target functions are supported; the remaining unresolved items are MINOR optional gene/protein annotations uxaC/uxaB/uxaA/kdgK/eda. Because D3a is capped at &#91;1,8&#93; here and 9–10 lacks experimental/protein-specific and optional-gene confirmation, 8 is the appropriate upper-band score.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：Shows accepted enzyme names and ECs at reaction-function curation level; does not certify specific protein activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：Connects the accepted enzyme/EC fields to the directed gold reactions.
- ANSWER_TEXT / answer.steps&#91;1-5&#93;.enzyme：Shows the actual delivered enzyme names, EC numbers and optional gene annotations.

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Every step is assigned to Escherichia coli, and gold organism rows include E. coli at species level for the relevant reactions and a PATHWAY_COMPLETE record for E. coli 562. The answer&#x27;s exact strain claim, E. coli K-12 substr. MG1655 (taxid 511145), and its strain-level complete-pathway claim lack a frozen strain-specific record. Under the D3b identity ladder this is species-level support for a strain-level claim: within-grade deduction, not a cap. Score 7.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_031：Supports E. coli at species/reaction level and E. coli species-level PATHWAY_COMPLETE records; does not verify strain K-12 MG1655 taxid 511145.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_031：Confirms the case is a defined linear pathway case; not a strain-level identity record.
- ANSWER_TEXT / answer.organism_profiles&#91;ORG_001&#93;：Shows the delivered species, strain, taxid and complete-pathway claim.

</details>

### D4 性状科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Most major traits match the frozen E. coli species-level trait records: facultative anaerobe, non-halophilic, pH 7 within the recorded growth range, motile, rod-shaped, Gram-negative, non-sporulating, and use of D-glucose plus the D-galacturonate pathway context. The main uncertainty is strain-specific granularity: optimum 37 C, ATCC 700926, NC_000913.3, genome size/GC and the F15 habitat statement are not directly verified in the frozen slice. These are local unverified items rather than proven errors, so 8 is appropriate.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_031：Supports E. coli species-level traits such as facultative anaerobe, non-halophilic, motility, morphology, Gram reaction, sporulation and several carbon-source observations; does not verify strain-specific K-12 MG1655 values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_031：Identifies which E. coli 562 trait fields are scoreable and which are completeness-only.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_031：Shows that several temperature/pH/salinity subfields are completeness-only or pending range policy, so exact strain-specific optimum/endpoint claims cannot be fully verified.
- ANSWER_TEXT / answer.organism_profiles&#91;ORG_001&#93;.traits：Shows the delivered trait values, including strain-specific ATCC, genome and habitat claims.

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer does provide a structured evidence_registry mapping route, enzymes, organism and traits to EVID_001-EVID_004, with some database names and record locators. However every entry is source_type=INTERNAL_KNOWLEDGE_ONLY, and the answer itself discloses no live database retrieval. The frozen slice is an EVIDENCE_GAP with no claim-linked records, so the delivered citations cannot be verified and are registered as unresolved, not as verified mis-citations. This fits the low source-delivery band: some mapping exists but actual external support cannot be checked. No cap applies because no fabricated or contradicted citation is verified.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.evidence_registry：Shows that all delivered evidence entries are INTERNAL_KNOWLEDGE_ONLY with database/record-like locators, not actual verified external records.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer clearly labels evidence sources as INTERNAL_KNOWLEDGE_ONLY and includes an uncertainties list disclosing no live retrieval, unchecked SMILES, omitted cofactor SMILES, missing numeric limits, and alternative organisms not used. It also distinguishes null/unknown values. The main weakness is that several strain-specific trait and identifier claims are marked high confidence despite internal-only support, but this is a limited overconfidence issue rather than systemic misleading. Score 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.uncertainties：Shows explicit uncertainty disclosures and the internal-knowledge provenance label.
- ANSWER_TEXT / answer.evidence_registry&#91;&#93;.confidence：Shows where high confidence is assigned to internal-knowledge evidence, especially strain-specific traits.

</details>

## GPT5.6

答案SHA256：`de2216597c2e26ca3cc1a4bd0a5be69c6ecda9fedbdc1deef1de04891c4db188`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1任务符合度：route_scope名称回显正确，但实际给出非磷酸化旁路S1-S4，漏掉gold S01激酶步（KDG→KDG-6P），终端为D-glyceraldehyde而非D-glyceraldehyde 3-phosphate；route诊断DEVIATES。JSON/字段完整、四步均有酶与菌，但路线锁定任务的主要符合性失效；15项性状全部显式unknown。按3-4档取下沿3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows answer echoes route name but delivers four nonphosphorylated steps with terminal D-glyceraldehyde and all traits null.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：Gold requires KDG→KDG-6P→pyruvate + D-glyceraldehyde 3-phosphate; does not support direct nonphosphorylated bypass.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：Supports kinase and phospho-aldolase enzymes for the required gold steps; does not support omission of the kinase step.

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1-S3的异构化、还原、脱水顺序在化学上基本连贯；S4直接以非磷酸化KDG醛缩裂解为pyruvate + D-glyceraldehyde，绕过S01激酶和6-磷酸中间体，终端与gold G3P不符；还原步未标NADH，SMILES电荷/立体表示有冲突。主干部分成立但关键连接需实质修订；按5-6档取下沿5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the delivered four-step nonphosphorylated route and terminal D-glyceraldehyde.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：Supports the expected phosphorylated intermediate and G3P terminal; does not support the answer&#x27;s nonphosphorylated terminal step.

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按目标五步计，未见任何一步达到C03的S：S01所需激酶未交付，S02终端产物应为D-glyceraldehyde 3-phosphate而答案为D-glyceraldehyde，S03与S05的显式EC分别为1.1.1.158、5.3.1.7，不在对应accepted set（1.1.1.58、5.3.1.12）中；S04的酶名/EC 4.2.1.7与accepted set一致，但路线诊断为表示/立体冲突UNRESOLVED，不能按S计，只作局部可用信息。核心目标酶对应仍失效；C04覆盖率落&#91;1,2&#93;，C05取2：少量局部的酶名/EC可用，但核心目标推荐不可用。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_031：列出本例目标S01-S05的冻结合格酶名/EC集合：S01为2.7.1.178/2.7.1.45等激酶，S02为4.1.2.55/4.1.2.14等醛缩酶，S03为1.1.1.58，S04为4.2.1.7，S05为5.3.1.12；仅支持目标反应可由这些酶/EC催化，不证明具体蛋白实测活性，也不支持答案S1的5.3.1.7或S2的1.1.1.158。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_031：显示目标S02底物为2-dehydro-3-deoxy-6-phospho-D-gluconate，产物含D-glyceraldehyde 3-phosphate与pyruvate；支持判断答案S4产物D-glyceraldehyde缺少3-磷酸，且目标S01应为加磷酸的激酶步骤；不扩展到未声称的旁支。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_031：确认该formal case为LINEAR_UNIQUE、ordered_step_count=5，用于目标主链步数背景；不把全图旁支当作额外缺步分母。
- ANSWER_TEXT / ANSWER：定位答案实际交付的S1-S4酶、EC和产物字段；仅证明答案文本如此声称，不证明其科学正确性。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> E. coli在gold organism行中按物种级支持各目标步，PATHWAY_COMPLETE E. coli 562也支持物种级全路径能力。答案统一使用E. coli K-12 MG1655/TaxID 511145；该菌株级身份和全路径能力未在E0中冻结，属物种→菌株粒度不足，不是无关类群或已证伪。按7-8档取下沿7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all steps assigned to Escherichia coli K-12 MG1655, TaxID 511145, and whole-path profile ORG_001.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_031：Supports E. coli species-level occurrence for each step and species-level PATHWAY_COMPLETE E. coli; does not provide frozen strain-level 511145 capability.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4按P44：全部必需15项性状均为null/空值，D4记MISSING=1，不宣称检测到科学错误；完成度不足已在D1反映。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all 15 trait values null/unknown with confidence unknown and no trait evidence ids.

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry仅有1条通路级MetaCyc记录覆盖全部路线/酶/EC/基因声称，以及1条NCBI TaxID记录；无逐步locator、无版本/URL、无性状来源。E0为EVIDENCE_GAP，来源内容属待核而非已证伪；决策相关组为generic/unresolved，但存在条目级记录而非全缺失。按5-6档取下沿5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows one pathway-level MetaCyc record and one NCBI Taxonomy record; no per-step or trait sources.

</details>

### D6 不确定性与诚实度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 性状全部诚实null/unknown是正面披露；但路线酶与菌均以DATABASE_DIRECT/high confidence呈现，来源仅为一条通路级记录和一条TaxID记录，未列uncertainties、替代路线或主要限制，多个EC/终端声称强于交付证据。属档内过度确信而非已证系统性虚构；按5-6档取下沿5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows high confidence for route enzymes/organism with no uncertainty list, while traits are explicitly unknown.

</details>
