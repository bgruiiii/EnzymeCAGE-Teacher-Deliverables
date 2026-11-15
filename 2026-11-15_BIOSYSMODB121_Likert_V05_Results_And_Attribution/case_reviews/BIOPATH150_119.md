# BIOPATH150_119：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-methylphenol degradation to protocatechuate

污染物：P-Cresol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 64 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 65 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 69.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 64 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 66 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 52 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`cbd9718f0951566ebf9ea2be031b1a9d8e7c5c0a29f375b8159c2bd29ea2ee71`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 题面要求一条主链并要求逐步给出底物/产物、酶/EC与微生物。答案 route_scope 名称原样保留，steps 的底物/产物、酶/EC、微生物及两个 organism_profiles 的15项性状、evidence_registry 基本齐全，JSON可读。但按 task_scope 与 formal_cases，主链为4个必答步；答案只交付3步，并将4-羟基苄醇明确列入 alternative_branches，未作为主链必经中间步交付，属于必答主链的实质遗漏。该遗漏影响完整性，但尚非核心模块大部缺失或改选路线，故D1取5–6档内低分6，不触发D1关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

任务要求的三大模块（路径步骤含底物/产物英文名与SMILES、每步一个首选酶含EC、每步一个对应微生物）与15项性状外壳全部实质交付；route_scope.chosen_route_name逐字保留题面路线名；两条profile按物种+菌株去重（NCIMB 9869与KT2440），steps以organism_profile_id正确引用；每profile 15项性状齐备（13项填写、2项显式null+unknown）。未取9-10档的原因：主链把参考的4步中前两步（4-羟基苄醇中间体）合并为EC 1.17.99.1净反应一步，步骤粒度相对参考略简（已在alternative_branches/uncertainties声明，故不按范围偏离处置）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_119：ordered_step_count=4，LINEAR_UNIQUE，本题主链为4步；可用于完整性核对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：gold主链包含 S04 p-cresol→4-hydroxybenzyl alcohol、S03 4-hydroxybenzyl alcohol→4-hydroxybenzaldehyde、S02 4-hydroxybenzaldehyde→4-hydroxybenzoate、S01 4-hydroxybenzoate→protocatechuate 的连续四步。
- ANSWER_TEXT / ANSWER.steps：答案只给 S1-S3 三步；S1 直接把 p-cresol 写为到 4-hydroxybenzaldehyde，未把4-羟基苄醇作为主链中间步交付。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案主链从对甲酚到原儿茶酸，方向为降解/氧化方向，终点为 protocatechuate，三步净化学均能成立：甲基羟化/氧化到4-羟基苯甲醛、醛氧化到4-羟基苯甲酸、4-羟基苯甲酸3-位羟化到原儿茶酸。与gold四步相比，答案把 S04+S03 合并为 EC 1.17.99.1 的净反应，并把4-羟基苄醇列入alternative_branches；这主要影响完整性，不改变净化学可达性。局部问题包括电子受体泛化、S2用NAD+而gold记录用NADP+、以及未分列中间步；这些属于局部/表述与计量层面，未构成已核核心化学错误或方向反转，故D2取7–8档内较高分8。

<details><summary>V0.4理由与本行变化背景</summary>

三步主链化学成立：S1 4-methylphenol的甲基脱氢羟化净氧化为醛基（Cc1ccc(O)cc1→O=Cc1ccc(O)cc1，4电子氧化、原子守恒）；S2 醛氧化为羧酸（→O=C(O)c1ccc(O)cc1，NAD+依赖）；S3 苯环3位单加氧羟化至原儿茶酸（O=C(O)c1cc(O)c(O)cc1），方向全程forward、无跳步、终点与题面指定protocatechuate一致，辅因子H2O/电子受体/NAD+/O2/NADPH在列。未取9-10档：参考中4-羟基苄醇为独立一步，答案按同一PCMH黄素细胞色素净反应合并（已在uncertainties与alternative_branches声明该中间体并标is_part_of_scored_main_route=false），且S1电子受体仅写“electron acceptor (oxidized)”未落到参考的azurin，属局部表达/计量细节，不构成化学断裂。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：gold显示四步转化、主产物原儿茶酸及S02的NADP+/NADPH记录；可用于比较答案三步净反应与局部辅因子差异。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：S01 accepted EC 1.14.13.2；S02存在多个醛脱氢酶记录，支持醛到酸的化学合理性，同时保留辅因子/酶名差异。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_119：gold终点为3,4-Dihydroxybenzoate/protocatechuate，答案终点一致。
- ANSWER_TEXT / ANSWER.steps：答案给出三步连续净化学并到达protocatechuate；S1为p-cresol→4-hydroxybenzaldehyde，S2→4-hydroxybenzoate，S3→protocatechuate。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> 按4个必答目标逐项看：S01对应答案S3，酶名含 p-hydroxybenzoate hydroxylase，EC 1.14.13.2，与accepted名称-EC配对相符，可记S。S02对应答案S2，答案给4-hydroxybenzaldehyde dehydrogenase并配EC 1.2.1.64；accepted中4-hydroxybenzaldehyde dehydrogenase对应1.2.1.96，而1.2.1.64对应vanillin dehydrogenase，名称与EC不是accepted合法配对，按PAIR_UNVERIFIED记U，不凭未命中直接判F或key_error。S03/S04要求4-羟基苄醇作为独立中间步，答案将直接 p-cresol→4-hydroxybenzaldehyde 作为主链并仅把4-羟基苄醇列入alternative_branches；路线绑定/表示审查未确认其为已核遗漏，故不自动判M/F，按未绑定待核处理。综合S=1、N=4，C=0.25，落入&#91;3,4&#93;；仅少数目标有明确适用支持，取档内低分3。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶-反应对应与冻结参考高度一致：S3的EC 1.14.13.2（4-hydroxybenzoate 3-monooxygenase / p-hydroxybenzoate hydroxylase，PobA）与gold S01四条酶注释的EC完全一致；S2的EC 1.2.1.64落在gold S02多注集合（1.2.1.67/1.2.1.64/1.2.1.7/1.2.1.96）之内，按四.5多注条款不判错；S1的EC 1.17.99.1与gold S03/S04的酶名（alpha subunit of 4-cresol dehydrogenase / 4-methylphenol methylhydroxylase）功能类别吻合，而gold该处ec_number_raw=NOT_OBSERVED。未取9-10档的原因：E0无任何EC官方条目（GAP-119-007/008/015），accepted name、reaction与条目状态均未核；S2名称“4-hydroxybenzaldehyde dehydrogenase (NAD+)”与gold对1.2.1.64的注释名（vanillin dehydrogenase）之间的名称-编号对应未核。无已核实关键错误（无冻结证据可判矛盾）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：S01有EC 1.14.13.2及p-hydroxybenzoate hydroxylase/4-hydroxybenzoate hydroxylase记录；S02记录显示4-hydroxybenzaldehyde dehydrogenase=EC 1.2.1.96，vanillin dehydrogenase=EC 1.2.1.64，支持答案S2名称与EC 1.2.1.64不构成accepted配对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：S03是4-hydroxybenzyl alcohol→4-hydroxybenzaldehyde，S04是p-cresol→4-hydroxybenzyl alcohol；答案未把该独立中间步作为主链交付。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_119：本题主链为4个必答步，作为D3a原N=4的范围依据。
- ANSWER_TEXT / ANSWER.steps：答案S3为p-hydroxybenzoate hydroxylase/EC 1.14.13.2；S2为4-hydroxybenzaldehyde dehydrogenase/EC 1.2.1.64；S1为p-cresol直接到4-hydroxybenzaldehyde。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 物种层对应可靠：P. putida是gold S01–S04的已接受对应菌（organism_gold，taxid 303），答案S1/S2用P. putida NCIMB 9869、S3用P. putida KT2440，物种与gold一致；E0 f3e0:taxid:303核验P. putida学名/lineage为CURRENT。菌株层：NCIMB 9869无E0记录且taxid 303为物种级（STRAIN_TOKEN_NOT_IN_RECORD_NAMES）；KT2440的taxid 160488与NC_002947在E0无记录（GAP-119-001/002/036/037）；S2微生物归属仅INTERNAL_KNOWLEDGE_ONLY(EVID_004)。按D3b身份阶梯①（物种级真实记录支持菌株级声称）档内扣、不cap，取7。

<details><summary>V0.4理由与本行变化背景</summary>

物种级选择与冻结参考一致：gold S01–S04步级微生物均含Pseudomonas putida（TaxID 303），另含P. mendocina/pWWO、P. fluorescens、Pseudomonas sp. CBS3、Sphingomonas sp. SYK6等；答案三步统一用P. putida，属参考集合内的合法候选。步级催化归属（PCMH、醛脱氢、PobA）与gold步级酶名匹配。扣分点：①ORG_001以种级TaxID 303背书菌株级身份NCIMB 9869，E0的303记录为species rank且不含该菌株token（F3R1CLM-004435 UNRESOLVED），按八.D3b身份阶梯①“粒度不足”处理，档内扣、不cap；②ORG_002 KT2440的TaxID 160488与NC_002947在E0无任何记录（GAP-119-001/002），身份与能力待核；③complete_pathway_organism_profile_id=ORG_001的“全路径菌”声称仅由INTERNAL_KNOWLEDGE_ONLY与自由文本文献支撑，未区分身份定位/反应级能力/完整路径能力三层。无已核实身份错配或编造，故不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅核验Pseudomonas putida的官方学名/rank/lineage与CURRENT状态；不支持任何菌株身份、反应级能力或全路径能力
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_119：gold允许P. putida（taxid 303）作为S01–S04的对应菌，属物种级；不代表NCIMB 9869或KT2440任一菌株的能力
- E0_EVIDENCE / f3e0:bacdive:12880：该记录为P. putida mt-2 PaW1(pWWO)，保藏号DSM 3931/ATCC 33015/NCIB 12182/CCUG 2480等；不是NCIMB 9869，不能作为其菌株身份或能力证据

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 两profile均返回15项。可核子项与trait_gold taxid 303物种级观测一致：F10能动、F11杆状、F12革兰氏阴性、F13不产孢、F2偏好中温性、F4非嗜盐；F2/F3/F4数值多填null属完成度（D1口径），不是D4错误；F5的NCIMB 9869与代表记录CCUG 49576不同株，按同物种代表记录条款不判错。待修订项：F1『专性好氧(obligate aerobe)』强于观测aerotolerant=true；F9以基因组pobA推酶活；F14 KT2440数值与F5保藏号无E0记录（U）。主性状可核、仅少量条件/数值问题，取7。

<details><summary>V0.4理由与本行变化背景</summary>

定性性状与冻结种级记录吻合：TaxID 303记录给出运动性true、cell shape=rod-shaped、gram positive=false、sporulation=false、temperature preference=mesophilic、salinity preference=non-halophilic，与答案ORG_001的F10/F11/F12/F13/F2偏好/F4类别一致；数值型性状大量以null+confidence=unknown如实留空（F3、ORG_001的F14），未编造数值。扣分点：①把物种级一般性状直接写成两条菌株级profile（ORG_001几乎所有性状走EVID_010 INTERNAL_KNOWLEDGE_ONLY；ORG_002在160488无任何冻结记录），且未标明其为种级参照；②F1“专性好氧（obligate aerobe，非发酵型）”强于记录（303记录aerotolerant=true、facultative anaerobe=No robust majority），且与“高置信”标签不相称；③ORG_002 F2 optimum 30°C与F14 6181003 bp/GC 61.5%在冻结掩码中分别属completeness_only/待核子字段，无法与gold比对（range policy未冻结）；④未使用四.4同物种代表记录口径标注来源字段。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_119：提供taxid 303/294/72586等物种级观测/预测性状（含F10=true、F11=rod、F12 gram+ false、F13 sporulation false、F2 mesophilic、F4 non-halophilic、F1 aerotolerant=true）；不代表任一答案菌株的菌株级定量性状
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_119：标明哪些性状为observed_accuracy分母、哪些仅completeness_only；不提供答案侧数值
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_119：子字段级可评性（如pH min/max可评、温度端点待老师裁定）；用于避免把不可评子字段当作错误

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案有逐条evidence_registry并把步/酶/菌/性状映射到EVID_001–010，属可核对的结构；但：EC只给EC号、无BRENDA条目/版本locator；两条文献仅作者-年份-刊名（无DOI/卷期页）；EVID_004/010为INTERNAL_KNOWLEDGE_ONLY；TaxID 303种名与CG03终点可在E0/gold条目级核对，TaxID 160488、NC_002947及三个EC均无E0记录。决策相关组以UNRESOLVED_SOURCE为主，CG08/CG09含MISSING_SOURCE；无VERIFIED_MIS_CITATION，不cap。按P41『存在条目级可定位可核对结论→5–6档』取5（决策相关组仍有内部知识缺口）。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记（不压单一总标签）：决策相关组中，路线/酶组给出BRENDA EC条目标识与反应式claim_scope（条目级可定位），身份组给出NCBI Taxonomy 303/160488与RefSeq NC_002947，文献组给出两篇完整引文（Keat &amp; Hopper 1978 Biochem J；Nelson et al. 2002 J Bacteriol）；但E0切片仅含2条记录，全部EC与160488/NC_002947均为EVIDENCE_GAP（查不到），BRENDA条目无URL/locator、文献无PMID/DOI，性状模块大量由INTERNAL_KNOWLEDGE_ONLY（EVID_010/EVID_004）支撑而登记MISSING_SOURCE。按P41合成规则：决策相关组存在条目级可定位结论→5–6档；因核心引用的可核对性与性状来源覆盖均不足，取5。E0无任何经核实错引（taxid:303记录存在且学名吻合，仅菌株token粒度不足），故不cap，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：证明答案引用的TaxID 303在E0存在且种名一致（可核对条目）；不支持EC条目或菌株级引用
- E0_EVIDENCE / f3e0:bacdive:12880：证明E0存在P. putida mt-2 PaW1菌株记录（保藏号/培养温度/底物面板），但不支持答案所引NCIMB 9869
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：用于核对S02名-EC配对是否落在冻结accepted配对；不提供EC条目存在性或内容核验

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> uncertainties具体且与答案对应：净反应vs 4-羟基苄醇中间体、S2基因未知、KT2440基因组为记忆值(medium)、温度/pH/盐度无可靠来源；多处未知填null并给low/medium/unknown，符合『诚实说明未知』。扣分点：F1/F6/F12/F13等以INTERNAL_KNOWLEDGE_ONLY标high、F9由基因组推酶活而未在uncertainties逐条说明，属局部过度确信，非系统性把预测写成实证、无掩盖已知矛盾证据，故不cap，7。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体良好：uncertainties逐条说明S1净反应与4-羟基苄醇中间体的处理、S2基因未知故gene_or_protein=null、ORG_002基因组数值“依据记忆填写（medium）”、温度/pH/盐度缺来源故留空；route_scope.notes主动说明题面氧条件为null而该路线本质好氧（属推断且已标明推断依据）；alternative_branches两条分支均标is_part_of_scored_main_route=false；性状中未知项用null+confidence=unknown。扣分点：多处以high/medium confidence包装INTERNAL_KNOWLEDGE_ONLY来源（F1/F6/F7/F9/F12/F13等），未在字段层标注“内部知识、建议复核”，构成面上偏宽的过度确信；ORG_001菌株级身份以种级TaxID背书未加限定。尚未达到系统性把预测写成实证或掩盖已知矛盾，故不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_119：观测/预测值分栏（OBSERVED/PREDICTED）与UNKNOWN空值，用于判断证据性质标注是否相称；不提供答案侧置信判断
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：G4策展粒度说明功能支持≠蛋白级/实验级，用于核对答案是否把策展当实证；不给出答案置信分

</details>

## DeepSeek

答案SHA256：`072100fee0f4fbb68aba0f499f8bafee5cb764cac9fe4266d1869f908e879f96`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 四步主链、每步底物/产物/酶/微生物及15项性状均给出，route_scope原样填写；S2/S3 EC未定、菌株未指定、来源仅internal，属7–8档少量完成度缺陷，取8。

<details><summary>V0.4理由与本行变化背景</summary>

四步主链完整：每步给出主底物/产物英文名+SMILES、首选酶、对应微生物；route_scope.chosen_route_name 原样填写题面路线名；单一 Pseudomonas putida 去重为一条 profile 且被四步引用；15项性状全部出现。S2/S3 的 EC 为 null，符合题面‘未知填null’要求，非缺失模块。仅酶规格（两处EC缺省）存在少量不完整，属8档偏上。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_119：表明本题为LINEAR_UNIQUE四步主链，用于完整性核对，不证明答案化学正确。
- QUESTION_TEXT / BIOPATH150_119：题面指定路线、每步酶/EC/微生物及15项性状要求。
- ANSWER_TEXT / ANSWER_BIOPATH150_119：答案实际交付四步和15项性状；仅用于定位，不作为科学支持。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 生物顺序p-cresol→4-hydroxybenzyl alcohol→4-hydroxybenzaldehyde→4-hydroxybenzoate→protocatechuate与gold LINEAR_UNIQUE主链一致，方向与碳骨架连续；S01/S02中性/电荷表示差异属notation；未列azurin/NAD(P)+等辅因子，按P103–105为局部计量缺陷，7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与方向正确并与gold一致：p-Cresol→4-羟基苯甲醇→4-羟基苯甲醛→4-羟基苯甲酸→protocatechuate，正向、连接连续、止于题面终端protocatechuate；各步SMILES正确。未列出NADPH/O2等辅因子，属局部计量缺陷，按7–8档处理，不cap；范围声明缺失不额外扣D2。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：给出四步主链方向与主底物/主产物；不支持答案未声称的辅因子或具体酶实验活性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_119：给出题面路线起点p-Cresol与终点3,4-Dihydroxybenzoate/ protocatechuate。
- ANSWER_TEXT / ANSWER_BIOPATH150_119：答案实际化学步骤与SMILES；仅用于定位。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案四步与题面指定主链的化学顺序一致：S1 p-Cresol→4-Hydroxybenzyl alcohol 对应gold S04，S2 alcohol→aldehyde 对应gold S03，S3 aldehyde→4-Hydroxybenzoate 对应gold S02，S4 4-Hydroxybenzoate→Protocatechuate 对应gold S01。逐目标酶对应均被冻结事实登记为MAJOR U：S01/S02受REPRESENTATION_EQ_CHARGE_BLIND路线挂起，S03/S04为非accepted待核；无确认S、F或M，也无可确认KEY失败。已有accepted集合仍可作部分正向对照：S02名称4-Hydroxybenzaldehyde dehydrogenase在accepted名集合中，S01的EC 1.14.13.2与accepted EC一致，S04名称与4-methylphenol methylhydroxylase同义但EC未被冻结记录支持，S2使用4-Hydroxybenzyl alcohol dehydrogenase不在accepted集合且EC为null。整体主链酶名/EC大多合理，待核边界清楚，但四个MAJOR目标均未确认，且存在非accepted与EC缺失，故不能进入7–8档；在&#91;5,6&#93;档内取较高分6。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶功能与反应类型相符（甲基羟化酶/醇脱氢酶/醛脱氢酶/单加氧酶）；S4 EC 1.14.13.2 与gold的4-hydroxybenzoate hydroxylase一致，S1 EC 1.17.99.1 属p-甲酚甲基羟化酶族；S2/S3 EC null为诚实缺省。主要步骤酶对应有支持，但两处EC缺省且1.14.13.2/1.17.99.1在E0无冻结记录，需进一步确认，取7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：冻结gold酶行：S04/S03为4-methylphenol methylhydroxylase/alpha subunit且EC NOT_OBSERVED；S02含4-hydroxybenzaldehyde dehydrogenase及accepted EC；S01含4-hydroxybenzoate hydroxylase且EC 1.14.13.2。支持逐目标酶名/EC对照，不支持具体蛋白实验活性或菌株整路能力。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：冻结gold主链S04→S03→S02→S01的底物-产物方向与端点；支持答案四步化学顺序及题面终点对照，不支持具体酶催化活性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_119：题面路线终点为3,4-Dihydroxybenzoate（protocatechuate）；支持终点名称对照，不支持酶对应。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 各步均用Pseudomonas putida（TaxID 303），与gold organism_gold中P. putida 303步骤条目一致；PATHWAY_COMPLETE行支持P. putida整路。但菌株未指定，S2非gold酶对应的单步归属未独立核实，7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

四步统一归属 Pseudomonas putida（TaxID 303，物种级）。gold organism表中四步均列P. putida为合法菌之一，且species级PATHWAY_COMPLETE=TRUE支撑单一代表菌推荐；TaxID 303与官方学名匹配。仅未给菌株、步级与完整路径能力未逐一核验为保留，取8档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_119：列出各gold步可达微生物及PATHWAY_COMPLETE行；支持P. putida 303物种级身份/整路能力，不证明任意具体菌株或S2非gold酶。
- E0_EVIDENCE / f3e0:taxid:303：支持TaxID 303与Pseudomonas putida的官方名称关联；不支持菌株级能力或具体酶活性。
- ANSWER_TEXT / ANSWER_BIOPATH150_119：答案实际微生物字段；仅用于定位。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> P. putida 303基础性状多数与gold相符（中温偏好、运动、杆状、革兰氏阴性、不产孢、好氧呼吸），但F1写成专性需氧与gold aerotolerant不完全一致；pH/盐度/保藏号/基因组等有gold观测却留null；来源仅internal low，关键定量性状证据不足，定5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

定性性状与gold一致：杆状、革兰氏阴性、不产孢、运动、中温(mesophilic)、需氧呼吸。温/pH/盐度/基因组数值全null为诚实缺省（主归D1完成度）。F1‘专性需氧’与gold aerotolerant=true存在术语差异但非重大错误；F7/F8/F9为概括性描述，属部分可核实。主要性状可核实适用，仅少量条件/数值与来源支持问题，取7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_119：提供P. putida 303已观测性状及UNKNOWN项；不支持答案未填写的值或未记录的鞭毛类型。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_119：标明温度上下限等待裁定、部分性状仅completeness_only；用于避免把未决范围当已核数值。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_119：给出可核子字段与待裁定子字段；用于区分缺失与可评分观测。
- ANSWER_TEXT / ANSWER_BIOPATH150_119：答案实际性状值与confidence；仅用于定位。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry仅两条INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；全部claim组无条目级可定位来源，属MISSING_SOURCE低分档；无已核实错引，不触发cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案仅交付两条来源登记 EVID_001/EVID_002，均为 INTERNAL_KNOWLEDGE_ONLY，无数据库名、record_id、locator或计算记录可与具体结论定位对应，决策相关组（CORE+APPLICATION_CRITICAL）全部为 MISSING_SOURCE。按四.3/P41，全部缺失落低分档；MISSING_SOURCE默认不触发cap。身份 TaxID 303 虽可被官方记录正向支持，但属评价者证据层，不回填系统来源状态。取2分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_119：答案实际交付的来源登记；仅证明其来源状态为internal，不证明结论正确。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案将来源标为INTERNAL_KNOWLEDGE_ONLY并用low/unknown置信度，列出S2/S3 EC未定和菌株未指定；未知字段多填null。但未逐项区分观测/预测，complete_pathway等仍较肯定，D6在7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties明确列出步骤2/3 EC未定、菌株未指定用物种级代表；性状置信多为low/unknown，数值缺省用null，证据性质披露较具体诚实。仅整条路径与菌以medium置信配内部知识、未明示推断性质，属单点过度确信而非系统性误导。取7档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_119：答案实际不确定性标签与说明；仅用于D6披露质量判断。

</details>

## Kimi

答案SHA256：`22372e703510d60efb9beafc0e526a3d7d34ecc113ce585dc205ae92eab2765a`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> Four required steps are delivered with substrate/product names and SMILES, preferred enzyme/EC and a corresponding microorganism; chosen_route_name is the题面 route name. Two organism profiles are separated by species+strain and each contains all 15 trait keys, with nulls marked unknown rather than omitted. Only minor completeness/quality issues remain (some trait values are null, several sources are low/internal), so D1 is high but not perfect.

<details><summary>V0.4理由与本行变化背景</summary>

交付完整性与任务符合度好：route_scope.chosen_route_name逐字为题面指定路线，四步主链每步均给主底物/主产物英文名与SMILES、一个首选酶含EC、一个对应微生物并引用profile；两个同物种异菌株profile按“物种+菌株”未合并、各给全15项性状（13项填写、2项显式null）。扣分点：多项性状仅有内部知识自述来源、第3步菌株归属低置信、部分辅因子SMILES为null，属“大部分必要内容完整、少量关联不清”，落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_119：Gold confirms the task route has four ordered main-chain steps and endpoint protocatechuate; it does not itself prove answer completeness.
- ANSWER_TEXT / ANSWER：Answer text shows the required modules and all 15 trait keys are present; this does not certify scientific correctness.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The four organic transformations follow the gold directed sequence: p-cresol -&gt; 4-hydroxybenzyl alcohol -&gt; 4-hydroxybenzaldehyde -&gt; 4-hydroxybenzoate -&gt; protocatechuate, with correct direction and endpoint. Main structures connect and atom/redox logic is broadly coherent. However S1/S2 omit the azurin electron carrier shown in gold, and S3 uses NAD+/NADH where gold S02 records NADP+/NADPH. These are local redox/cofactor issues, not a broken carbon main chain, so D2 is 8 rather than 9-10.

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步一致：对甲酚→4-羟基苯甲醇→4-羟基苯甲醛→4-羟基苯甲酸→原儿茶酸，方向为SUBSTRATE_TO_PRODUCT、结构与终点（原儿茶酸=gold terminal 3,4-二羟基苯甲酸）正确，S3/S4分别列出NAD+、O2、NADPH与NADH、H2O、NADP+。局部缺陷：S1/S2未列gold反应记录中的氧化型azurin（铜）电子受体，属辅因子遗漏的局部计量缺陷（7–8档，不cap）；S3填NAD+/NADH，而gold该步反应记录为NADP+/NADPH，因缺EC 1.2.1.64官方反应记录不能核实，登记待核而非判错。取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：Gold directed reactions support the main organic sequence and endpoint; they do not certify the answer&#x27;s exact cofactor choices in every step.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_119：Confirms pollutant and terminal product identity; not a complete proof of each reaction step.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> 答案覆盖4个必答目标反应并给出酶名/EC，但逐目标核验后仅1个目标达到可确认支持：answer S4对应gold S01，酶名p-hydroxybenzoate hydroxylase/EC 1.14.13.2与accepted集合精确匹配，记S。answer S3对应gold S02，EC 1.2.1.64虽在accepted EC集合内，但名称4-hydroxybenzaldehyde dehydrogenase在accepted配对中对应1.2.1.96，而1.2.1.64对应vanillin dehydrogenase；名/号配对未核，按C02不记S，记U。answer S2/S1对应gold S03/S04，名称p-cresol methylhydroxylase与accepted名称4-methylphenol methylhydroxylase同义，但显式EC 1.17.99.1在accepted集合为NOT_OBSERVED且冻结证据无EC记录，显式EC配对待核，记U。故S=1、U=3、N=4，C=0.25，落入C04的&#91;3,4&#93;带；因仅1个目标获确认、关键入口步仍为U，选带内下沿3，不取上沿。无已确认F/M，故不触发D-KEY4；key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶名与EC类别自洽、无名称-EC类别矛盾：甲基羟化酶1.17.99.1（黄素细胞色素c）、醛脱氢酶1.2.1.64（NAD(P)+依赖氧化脱氢）、4-羟基苯甲酸3-单加氧酶1.14.13.2（FAD/NADPH）；1.14.13.2与gold酶条目一致，1.2.1.64落在gold该步多注集合(1.2.1.67/1.2.1.64/1.2.1.7/1.2.1.96)内，S2“同一PCMH继续氧化苄醇”与gold S03酶名一致。但EC的官方accepted name/reaction在冻结快照中无记录（GAP-119-006/011/012/014/020/024/025/028），关键步骤酶对应仍有局部未核，故取8而非9–10。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：S01 accepted EC 1.14.13.2；S02 accepted EC集合含1.2.1.64/1.2.1.96等但名称-EC配对按行区分；S03/S04 accepted名称4-methylphenol methylhydroxylase且EC为NOT_OBSERVED。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：四步反应的主底物/主产物、方向与终点protocatechuate；用于确认目标反应序列。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S4&#93;.enzyme：答案实际交付的各步首选酶名称与EC；S4为1.14.13.2，S3为1.2.1.64，S2/S1为1.17.99.1。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Gold organism rows support Pseudomonas putida at the species level for the relevant reaction steps, and the answer consistently uses P. putida. However the answer names NCIMB 9869 for S1-S3 and KT2440 for S4; E0 contains a BacDive record for P. putida mt-2 PaW1/pWWO, not NCIMB 9869, and no frozen TaxID 160488/KT2440 record is supplied. Species-level placement is reliable, but strain-level identity and step capability remain unverified. This is a D3b 7-8 case lowered to 7, not a cross-genus cap.

<details><summary>V0.4理由与本行变化背景</summary>

物种级对应与gold一致：四步均用Pseudomonas putida，gold organism_gold每步均有P. putida（TaxID 303）记录且PATHWAY_COMPLETE(P. putida 303)=TRUE，E0 f3e0:taxid:303亦确认学名。菌株级分配未获冻结记录支持：NCIMB 9869身份与保藏号无记录，KT2440的TaxID 160488无记录（GAP-119-036/037）；第3步pchA归属答案自述按同种途径自NCIMB 9866推断，属身份阶梯①“粒度不足”，档内扣不cap。未见已核实跨类群/异菌株错配，不判关键错误。取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_119：Supports P. putida at species level for these reaction steps; does not verify NCIMB 9869 or KT2440 strain identity/capability.
- E0_EVIDENCE / f3e0:bacdive:12880：A P. putida strain record but not the answer&#x27;s NCIMB 9869; it neither proves nor contradicts the answer&#x27;s strain claim.
- E0_EVIDENCE / f3e0:taxid:303：Species-level identity only; no strain-level identity or full-pathway capability.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> Several species-level P. putida traits are corroborated by gold: pH growth near 7, motility, rod morphology, Gram-negative, non-sporulating, and broad aromatic/phenol degradation. However the answer fills F2 optimum_c 30 for KT2440 from a routine culture-temperature statement, which the trait policy says is not equivalent to an optimum; F4 salinity is left entirely null despite species-level records; p-cresol growth, NCIMB 9869 enzyme purification, and KT2440 genome numbers are not verifiable in E0. Traits are partly accurate and applicable, but key condition interpretation and several strain-level values need substantive revision; D4 6.

<details><summary>V0.4理由与本行变化背景</summary>

可与gold核对的性状一致：运动性+、杆状、革兰氏阴性、不产孢、pH growth 7.0（min5/max8）、温度偏好mesophilic，均落gold物种级代表记录；F4盐度与ORG_001 F14如实null，属诚实未知。扣分：ORG_001多数性状为种水平内部知识（EVID_006 INTERNAL_KNOWLEDGE_ONLY，低置信），按同物种代表口径可参照但非可核记录；ORG_002 F2把raw_text“KT2440常规培养温度为30°C”写成optimum_c=30，属培养温度≠最适温度的测量含义误读；ORG_002 F14基因组数值高置信但无冻结记录（GAP-119-035/049/050/053）。无离谱数值、无把预测冒充实测、无种级观测强推全菌株耐受→7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_119：Supports some species-level trait observations such as motility, morphology, Gram reaction, sporulation, pH, salinity, and broad degradation; does not establish every strain-specific entry or optimum value.
- E0_EVIDENCE / f3e0:bacdive:12880：A strain record with culture temperature; does not establish optimum temperature for NCIMB 9869 or KT2440.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> The answer does provide a structured evidence_registry with specific BRENDA EC identifiers, a MetaCyc pathway locator, an NCBI genome accession, claim scopes and confidence labels. However the E0 slice contains only BacDive 12880 and TaxID 303; none of the BRENDA/MetaCyc/NCBI Genome records or TaxID 160488 are in E0, so key source records are UNRESOLVED_SOURCE rather than verified. Many supportive traits use EVID_006 INTERNAL_KNOWLEDGE_ONLY, which is MISSING_SOURCE. There is no verified mis-citation and no D5 cap; the delivered traceability is partial, giving 5-6 band and score 6.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG08）均给了条目级定位（MetaCyc途径名、BRENDA以EC号为record_id、NCBI RefSeq登录号、profile级TaxID），但统一冻结快照不含这些条目，无法核对引用是否支持结论，只能登记UNRESOLVED_SOURCE；CG14同为UNRESOLVED；CG04与CG10–CG13、CG15、CG16、CG20等性状/条件组仅有INTERNAL_KNOWLEDGE_ONLY或空值，记MISSING_SOURCE。无任何已核实错引→不cap、severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。按P41“存在条目级可定位结论”入5–6档，因无一条可核对、菌株身份来源薄弱，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows what sources the answer actually delivered; it does not prove those records support the claims.
- E0_EVIDENCE / f3e0:bacdive:12880：Only one usable E0 strain record; it does not cover BRENDA EC, MetaCyc pathway, KT2440 genome, or TaxID 160488.
- E0_EVIDENCE / f3e0:taxid:303：Species-level taxonomy only; does not verify strain identities or enzyme records.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The answer generally distinguishes observation, inference and unknown: it supplies explicit uncertainty notes for S2 and S3, says NCIMB 9869 trait data are species-level extrapolations, marks F4/F14 nulls, and explains the oxygen-condition assumption. Some claims are overconfident or unsupported by E0 (high confidence for KT2440 genome and NCIMB enzyme purification; culture temperature treated as optimum), but these are limited and not a systemic prediction-as-observation pattern. D6 8.

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界披露质量好：uncertainties逐条说明S2同酶归属不确定、S3的pchA归属来自NCIMB 9866而非9869、NCIMB 9869系统性状缺乏而按种水平填写、题面氧条件null而按经典好氧途径作答并声明；置信度在high/medium/low间有区分，F4盐度与F14（ORG_001）如实null。扣分：部分未经本快照核实的数据库断言标为high（EVID_001/002、ORG_002 F14），ORG_002 F2把培养温度呈现为最适温度，属单点过度确信而非系统性误导，故档内扣不给cap（不触发D6关键错误）。取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s self-declared uncertainty and confidence; it does not verify the underlying science.

</details>

## Qwen

答案SHA256：`57d776692d2ac26cd03d8f1bc1f6732f0dc1d16eee5f393215cec09edb616f12`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 题面指定路线名原样填写；4步均含底物、产物、SMILES、首选酶及EC、对应微生物；同一菌按profile去重；15项性状全部出现，未知项按题面允许置null；JSON完整。仅有允许的显式未知，无重要任务遗漏或路线改选。

<details><summary>V0.4理由与本行变化背景</summary>

四个步骤均给出主底物/主产物英文名与SMILES、一个首选酶及EC、一个对应微生物，route_scope.chosen_route_name逐字填写题面路线名，predecessor_step_ids成链，15项性状全部出现（11项填写、4项明确null），evidence_registry与claims可对应，无格式缺陷。未达9–10档：温度/pH/盐度/基因组4项关键数值性状未交付，来源仅内部知识，交付完整性仍有缺口。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求指定路线名、4步主链、每步酶/EC/菌、15项性状与null规则。
- ANSWER_TEXT / ANSWER.route_scope+steps+organism_profiles：答案实际交付了路线名、4步、15项性状及JSON结构。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链 p-cresol→4-hydroxybenzyl alcohol→4-hydroxybenzaldehyde→4-hydroxybenzoate→protocatechuate 的方向、顺序和终点均与题面指定路线一致，主要化学转化合理。辅因子、氧/NADPH等未在反应式中完整列出，属局部计量简化，按P103在7–8档内取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步一一对应：P-cresol→4-hydroxybenzyl alcohol→4-hydroxybenzaldehyde→4-hydroxybenzoate→protocatechuate，方向为底物到产物，四个SMILES正确（Cc1ccc(O)cc1 / OCc1ccc(O)cc1 / O=Cc1ccc(O)cc1 / O=C(&#91;O-&#93;)c1ccc(O)cc1 / O=C(&#91;O-&#93;)c1ccc(O)c(O)c1），终点与题面路线终点一致，符合四.2/P29（止于题面终点不扣分）。扣分点仅为主链未列O2、NADPH/NAD+、H2O与电子载体（甲基羟化酶需醌/细胞色素类受体、末步单加氧酶需O2+NADPH），按八.辅因子条款属局部计量缺陷，在7–8档处理，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：gold行显示p-cresol→4-hydroxybenzyl alcohol→4-hydroxybenzaldehyde→4-hydroxybenzoate→3,4-dihydroxybenzoate(protocatechuate)的线性四步方向与终点；不要求答案完整列出所有辅因子。
- ANSWER_TEXT / ANSWER.steps&#91;0..3&#93;：答案四步的底物/产物结构、SMILES和连接顺序可用于化学连续性核对。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按4个必答目标反应逐项看：答案S4对应gold S01，4-hydroxybenzoate 3-monooxygenase / EC 1.14.13.2与accepted集合的4-hydroxybenzoate hydroxylase / EC 1.14.13.2功能与EC一致，计S。答案S1对应gold S04，p-cresol methylhydroxylase名称接近accepted的4-methylphenol methylhydroxylase，但显式EC 1.17.99.1与gold NOT_OBSERVED的EC配对未核，计U。答案S2对应gold S03，aryl-alcohol dehydrogenase / EC 1.1.1.90不在accepted集合，且无冻结证据证明其催化该目标反应，计U。答案S3对应gold S02，aldehyde dehydrogenase / EC 1.2.1.3不在accepted集合（accepted为1.2.1.64/1.2.1.67/1.2.1.7/1.2.1.96等），计U。故S=1、U=3、N=4，C=0.25，落入&#91;3,4&#93;；仅一个目标获得明确accepted支持，其余为支持/配对待核，未达到该带上沿，取3。未发现可核F或已确认KEY失败，不触发D-KEY4上界。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶名与反应类型均自洽：第1步p-cresol methylhydroxylase（与gold的4-methylphenol methylhydroxylase同名族）配1.17.99.1；第2步aryl-alcohol dehydrogenase 1.1.1.90（醇→醛，方向正确）；第3步aldehyde dehydrogenase 1.2.1.3（醛→酸，通用号）；第4步4-hydroxybenzoate 3-monooxygenase 1.14.13.2与gold酶名和EC逐字一致。弱点：第2步用独立醇脱氢酶替代gold中同一甲基羟化酶完成的第二次氧化（合理替代但未声明依据）；第3步用通用1.2.1.3而非gold的1.2.1.96/1.2.1.7/1.2.1.67更具体候选；第1步1.17.99.1为历史/撤转类编号；E0对全部EC均无冻结记录。属“有合理候选和部分支持、关键步骤仍缺具体核验”，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps&#91;0..3&#93;.enzyme：答案四个步骤的酶名与EC：S1 p-cresol methylhydroxylase/1.17.99.1；S2 aryl-alcohol dehydrogenase/1.1.1.90；S3 aldehyde dehydrogenase/1.2.1.3；S4 4-hydroxybenzoate 3-monooxygenase/1.14.13.2。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：Gold酶行显示：S01 accepted EC 1.14.13.2；S02 accepted EC集合1.2.1.64/1.2.1.67/1.2.1.7/1.2.1.96；S03/S04 accepted名称为4-methylphenol methylhydroxylase/alpha subunit of 4-cresol dehydrogenase且EC为NOT_OBSERVED；不证明任意具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：Gold反应方向与主底物/主产物：S04 p-cresol→4-hydroxybenzyl alcohol；S03 4-hydroxybenzyl alcohol→4-hydroxybenzaldehyde；S02 4-hydroxybenzaldehyde→4-hydroxybenzoate；S01 4-hydroxybenzoate→protocatechuate；并显示S01/S02存在电荷表示边界。
- RUBRIC_CLAUSE / C03：D3a逐目标S/F/M/U/H分类及S须显式EC配对已核的规则。
- RUBRIC_CLAUSE / C04：D3a覆盖率分带、U处理及D-KEY4限制规则。
- RUBRIC_CLAUSE / C05：D3a带内整数选择：少数目标可用且边界仅能勉强分清时取低档。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> P. putida种级在gold的S01–S04及PATHWAY_COMPLETE中均有支持；但答案使用NCIMB 9866菌株token，E0 taxid 303仅支持种名，不核实该菌株，BacDive 12880也是mt-2 PaW1/pWWO而非NCIMB 9866。按身份阶梯，种级支持菌株级声称档内扣，取7。

<details><summary>V0.4理由与本行变化背景</summary>

四步微生物均写Pseudomonas putida（TaxID 303），gold organism_gold在S01–S04四行均列出Pseudomonas putida(taxid 303)，且PATHWAY_COMPLETE行对taxid 303标pathway_complete=TRUE，故种级身份、步级归属与整链能力有据；TaxID 303↔Pseudomonas putida种级学名经E0官方记录SUPPORTED。弱点：全部声称绑定菌株“NCIMB 9866”，该菌株token不在E0任何记录名称中（F3R1CLM-004434 UNRESOLVED），bacdive:12880为另一菌株mt-2 PaW1(pWWO)；属D3b身份阶梯①粒度不足——档内扣分（7档附近）、默认不cap；菌株级完整路径能力为种级外推且已在uncertainties披露。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：taxid 303当前记录支持Pseudomonas putida种名/分类；不支持NCIMB 9866菌株token。
- E0_EVIDENCE / f3e0:bacdive:12880：该记录为P. putida mt-2 PaW1/pWWO菌株，含其他保藏号；不能作为NCIMB 9866的菌株级证据。
- GOLD_SLICE / organism_gold.tsv：gold在多个步骤及PATHWAY_COMPLETE中列出P. putida taxid 303；支持种级归属/能力，不核实NCIMB 9866菌株。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 已给性状多为P. putida种级可核：运动性阳性、杆状、革兰氏阴性、不产孢与gold一致；好氧/氧受体描述与303 aerotolerant及无硝酸盐还原背景相容。F5 NCIMB 9866、F15广适性及部分菌株特异性状未逐项核到；F2/F3/F4/F14按题面允许null。主要性状可核但菌株特有条件未充分，取7。

<details><summary>V0.4理由与本行变化背景</summary>

已填11项中运动性阳性、杆状、革兰氏阴性、不产孢与gold对P. putida(taxid 303)的OBSERVED条目一致；F1“好氧”与gold aerotolerant=true/O2呼吸记录方向不矛盾；F6“aerobic respiration/oxygen”与gold nitrate呼吸阴性一致；F8“可降解酚类”有gold degradation: phenol=true(OBSERVED)支持。弱点：F5保藏号NCIMB 9866、F7“可利用对甲酚作碳源和能源”、F9“具有p-cresol methylhydroxylase活性”、F15栖息地广适性在冻结证据中无记录（F7解释层明确153432/12880面板不含对甲酚项，裸名称列表≠阳性碳源清单）；全部性状raw_text=null、evidence仅内部知识、confidence统一medium，且为种级一般知识用于指定菌株（已在uncertainties披露，故不按“预测冒充观测”重判）。整体属“部分性状准确且适用、关键项证据不足”，5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：P. putida 303种级记录支持运动性、杆状、革兰氏阴性、不产孢等；F5列出CCUG 49576，不支持NCIMB 9866；温度/盐度等端点有记录级限制。
- GOLD_SLICE / trait_scoreability_mask.tsv：标明哪些性状有观测值可评、哪些仅为完整性/待裁；菌株级NCIMB 9866不在冻结观测范围内。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry仅有EVID_001/EVID_002，source_type均为INTERNAL_KNOWLEDGE_ONLY，database、record_id、locator全为null；所有决策相关组缺少可定位外部来源，属MISSING_SOURCE低分档。不是已核实错引，不触发cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅两条，source_type均为INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator全为null，按四.3/P34属MISSING_SOURCE；决策相关组（CG01路线核心步骤、CG02起点、CG03终点、CG05酶-EC、CG07核心微生物身份、CG08步级归属、CG09整链能力，以及按应用关键处理的CG14底物利用）全部只有内部知识声明，无任何条目级可定位可核对证据，按P41“全部缺失→低分档（默认不cap）”落入1–2档；给2分而非1分，因答案以evidence_id建立了声称-来源的显式对应、未编造任何数据库条目或文献，且诚实标注confidence=medium；无已核实错引→severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案只登记内部知识条目，无数据库/文献定位。
- RUBRIC_CLAUSE / P34：仅有INTERNAL_KNOWLEDGE_ONLY类自我声明按MISSING_SOURCE低分档处理，默认不触发关键错误cap。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案明确列出氧条件未指定、EC为通用注释、菌株性状未逐项核对，并将温度/pH/盐度/基因组等置unknown/null；不确定性披露具体。但多条内部知识及菌株能力仍以medium confidence呈现，置信表达略强于来源，档内取7。

<details><summary>V0.4理由与本行变化背景</summary>

把F2温度/F3 pH/F4盐度/F14基因组主动置null，uncertainties列出三条具体限制：氧条件未指定而末步单加氧酶需氧、部分EC为通用注释且同工酶因菌株而异、菌株性状基于P. putida一般知识未逐项核对NCIMB 9866原始数据；confidence统一medium、未出现high confidence包装未核实内容，未见把预测写成实证或掩盖矛盾。扣分点：11项性状均以内部知识+medium标签呈现，未逐项标注证据性质（观测/预测/一般知识）与适用边界，属披露充分度不足，7档而非8–9档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties+confidence：答案主动披露氧条件、通用EC及菌株性状未核对等限制，并对多项未知置null。
- RUBRIC_CLAUSE / P119：单点/局部过度确信不自动cap；按披露覆盖范围和证据相称性在档内扣分。

</details>

## Grok

答案SHA256：`173b71af829801d981f273079256083325dda29f386f988937b496f8b518af75`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面指定路线名原样保留；S1–S4每步均给出主底物/主产物、首选酶及EC、对应微生物，且同一菌通过ORG_001去重；15项性状字段全部出现（10项有值、5项明确未知），来源与不确定性字段也交付。完整性高，仅来源/菌株能力问题属其他维度。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION#BIOPATH150_119：题面要求指定路线、每步酶/EC/微生物及15项性状；不支持答案科学正确性。
- ANSWER_TEXT / ANSWER#BIOPATH150_119：显示交付覆盖情况；不证明酶/菌株能力。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链S1–S4为4-甲基苯酚→4-羟基苯甲醇→4-羟基苯甲醛→4-羟基苯甲酸→原儿茶酸，方向、连接与终端均与gold主链一致；关键氧化/羟化化学合理，辅因子多数明确，S1/S2使用泛化电子受体属局部表达问题，不改变主链结论。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：支持四步主链的底物/产物方向与终端；不支持具体蛋白或菌株实验活性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_119：支持题目终端为3,4-二羟基苯甲酸/原儿茶酸；不支持酶学细节。

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a target set N=4. All four required target reactions are delivered with enzyme names/ECs; no confirmed F or M, and no confirmed KEY failure triggers D-KEY4. However the frozen step states remain U for all four: S01/S02 are route-representation hold with accepted name 4-methylphenol methylhydroxylase but EC NOT_OBSERVED, while S03/S04 are MATCH but UNRESOLVED_NONACCEPTED with explicit EC/name pairing unresolved. The answer’s assignments are plausible and step-associated, and the accepted sets give partial name/EC correspondence (e.g. EC 1.14.13.2 for the terminal hydroxylase; EC 1.2.1.64 within the aldehyde-dehydrogenase accepted EC set; p-cresol methylhydroxylase as the accepted methylhydroxylase name), but MAJOR/KEY U prevents the 7–8 band. Score 6 reflects partial usable support with clear reaction-step associations and unresolved EC/representation boundaries, not a default mid-score for unknown.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：Lists accepted enzyme names/ECs for the four gold steps: 4-hydroxybenzoate hydroxylase EC 1.14.13.2 at the terminal step; aldehyde-dehydrogenase accepted EC set including 1.2.1.64/1.2.1.96; 4-methylphenol methylhydroxylase with EC NOT_OBSERVED for the two methylhydroxylase gold steps. Does not by itself verify the answer’s name–EC pairing or specific protein activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：Confirms the directed main-chain reactions p-cresol → 4-hydroxybenzyl alcohol → 4-hydroxybenzaldehyde → 4-hydroxybenzoate → protocatechuate; useful for aligning answer step order and endpoint, not for independently certifying enzyme identity beyond the accepted-set rows.
- ANSWER_TEXT / ANSWER.steps.S1-S4：Answer assigns p-cresol methylhydroxylase EC 1.17.99.1 to S1/S2, 4-hydroxybenzaldehyde dehydrogenase EC 1.2.1.64 to S3, and 4-hydroxybenzoate 3-monooxygenase EC 1.14.13.2 to S4; all four required target steps are present and readable.
- RUBRIC_CLAUSE / C04：D3a uses U for unresolved target/name-EC support; MAJOR/KEY U does not permit the 7–8 band, but all-U is not automatically NE or low if the materials still support a band judgment.

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案所有步骤均归到Pseudomonas mendocina KR1（TaxID 300），并使用单条ORG_001 profile；物种名和属级生理特征合理，但gold organism行列出的是P. mendocina (pWWO/pTOL)、P. putida等，无KR1菌株级记录；TaxID 300为种级，未证明KR1完成整条路径。属合理候选且有部分支持，但关键菌株身份/整路能力仍未充分核验，落5–6档取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_119：显示gold各步可用菌及P. putida PATHWAY_COMPLETE；不列KR1，也不能据此判KR1错误。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段齐全，10项有值、5项明确未知；F1/F6/F10–F13等属P. mendocina/假单胞菌常见物种级特征，具一定合理性。但F7/F8/F9及温度偏好等为INTERNAL_KNOWLEDGE_ONLY且未落到KR1菌株级证据，关键性状的证据与适用性不足；落5–6档取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_119：显示gold中P. putida/P. fluorescens等物种级性状记录；不含KR1，故不能直接核验答案的KR1性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_119：说明多数性状为completeness_only或部分待裁；不支持将未核性状判为已证实。

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案虽有EVID_001–EVID_006及claim_scope映射，但source_type全为INTERNAL_KNOWLEDGE_ONLY；关键路线/酶-EC/菌株身份组均无可核外部来源或生成记录。E0仅含P. putida相关条目，无法核验其ExplorEnz/NCBI声明。无已核实错引，不cap；按MISSING_SOURCE低档，因有结构化定位但与结论关联多为内部自述，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_119：显示答案实际交付的来源登记；不能把内部知识自述视为已核外部来源。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：仅能对照gold酶行；不能验证答案ExplorEnz条目的实际内容。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确区分未知/null、给出confidence，并在uncertainties中说明氧条件推断、KR1基因未核、电子受体未定、TaxID粒度及EC编号可能改分；主要限制披露较好。但部分INTERNAL_KNOWLEDGE_ONLY酶/EC仍标high，KR1整路能力标medium而缺少特异证据，存在局部过强；落7–8档取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_119：显示答案的不确定性/置信度表述；不证明所披露内容为真。

</details>

## GPT5.6

答案SHA256：`689ec4a1b09e0bb707dd2fbacc373e19993b5f052058c4a9947e8be42fb278a2`。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Four-step route, enzyme/EC, microorganism, SMILES and all 15 trait fields are present, but all 15 traits are null/unknown and sources are only internal labels. This is a substantial completeness gap. 5–6 band: main modules present but several necessary contents are placeholders/omissions; choose 6 because path and field structure are clear.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_119：Gold has four ordered required steps; does not make trait nulls complete.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_119：Confirms route name and protocatechuate terminal context.

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The four-step sequence and SMILES match the gold main chain: p-cresol to 4-hydroxybenzyl alcohol, aldehyde, 4-hydroxybenzoate, and protocatechuate. Direction and connectivity are correct. Charge notation differs only (neutral versus &#91;O-&#93;) and cofactors/redox carriers are omitted. Cofactor omission is local per P103, so D2 stays in 7–8; choose 8 because the main chemistry is correct, while 9–10 is blocked by the evidence gate.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：Gold reaction order and structures support the four-step sequence; charge notation only differs.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_119：Confirms p-cresol to 3,4-dihydroxybenzoate route endpoint.

</details>

### D3a 目标反应与酶对应：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四个必答目标步均给出酶名与EC，但冻结材料下仅S4（4-hydroxybenzoate→protocatechuate，EC 1.14.13.2）与accepted集合明确同EC；S1的p-Cresol methylhydroxylase/EC 1.17.99.1名称近同accepted 4-methylphenol methylhydroxylase，但该EC未被冻结记录确认；S2的EC 1.1.1.90与S3的EC 1.2.1.28均不在相应accepted集合，S3与accepted 1.2.1.96/1.2.1.7/1.2.1.64/1.2.1.67存在名称—EC配对悬差。无催化失败证明，不能判F；这些MAJOR目标仍属U。S01/S02还有路线表征电荷盲的UNKNOWN，不能据此升为S。按C04/C05，部分主干有可用对应但多处未核或配对不一致，取5档下沿；不触发KEY失败上界，key_error=N。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_119：列出本题四步参考酶名/EC及accepted范围；支持S4 EC 1.14.13.2与参考4-hydroxybenzoate hydroxylase一致，并显示S2/S3答案EC不在相应参考集合；不证明具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_119：支持四步主底物/主产物及SUBSTRATE_TO_PRODUCT方向；不等同于酶名—EC配对已全部确认。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_119：支持本题为LINEAR_UNIQUE、ordered_step_count=4的主链范围；不直接确认答案各酶EC。

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Each step assigns Pseudomonas putida, and organism_gold has P. putida rows for all four corresponding gold steps, plus a PATHWAY_COMPLETE P. putida record. The identity is species-level only; no strain or TaxID is delivered and no independent strain-level capability evidence is provided, so 9–10 is blocked. 7–8: major microorganism correspondence is reliable, with minor specific identity entries needing confirmation; choose 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_119：Gold step rows include P. putida for each corresponding step and a PATHWAY_COMPLETE P. putida row; species-level only.
- E0_EVIDENCE / f3e0:taxid:303：TaxID 303 is current species Pseudomonas putida; does not support a strain-level identity or experimental capability.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 required traits in the only organism profile are null/unknown. Per P44, D4 is MISSING=1, not a scientific-error score; the missing module is the entire trait-value delivery.

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Every evidence_registry entry is INTERNAL_KNOWLEDGE_ONLY with database/record_id/locator null. Decision-relevant route, enzyme, and organism claims therefore have MISSING_SOURCE. There is no locatable external source and no verified mis-citation; D5 low band 1–2, choose 1 because no external source is delivered at all.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows all evidence entries are INTERNAL_KNOWLEDGE_ONLY with null database, record_id, and locator.

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer explicitly labels source_type INTERNAL_KNOWLEDGE_ONLY, uses low/medium confidence on most steps, lists uncertainties, and fills unknown traits as null. However one enzyme EC is marked high confidence with only internal knowledge, and confidence is not fully aligned with delivered evidence. 7–8: most evidence types and limits are disclosed; choose 7 due the unsupported high-confidence EC.
