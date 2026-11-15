# BIOPATH150_004：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：Caffeine (fungal) pathway

污染物：Caffeine；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

**Qwen/B480-0012的D3a范围复审标记仍OPEN；另有同删该题后的敏感性视图。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 52.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 56 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 60 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 52 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 69.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 66.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`4078e770cb5cba9bf3a3a271598f90777476331e793f20e948ac07cf7e645afb`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 覆盖题面指定的Caffeine (fungal) pathway与好氧条件，给出8步、3个按种去重的organism_profile、每profile 15项性状、来源与不确定性；所选主链S1–S3（咖啡因→茶碱→3-甲基黄嘌呤→黄嘌呤）齐全。但5个酶EC为null、所有菌均无菌株、A. tamarii多项性状null，来源多为内部知识，且答案把链延伸到指定终点之外、主链边界未声明；属主要模块均有涉及但若干必要内容缺失/关联不清，按5–6档取6（受base range &#91;1,6&#93;上限）。

<details><summary>V0.4理由与本行变化背景</summary>

七类模块实质交付：8步主链每步给出底物/产物英文名与SMILES并绑定一个首选酶与一个对应菌；3个按物种去重的profile各含全部15项性状字段；8条evidence_registry逐条带claim_scope；6条uncertainties。chosen_route_name逐字为&#x27;Caffeine (fungal) pathway&#x27;，oxygen_condition=aerobic。未给9–10的原因：F3 pH、F4盐度、F14基因组在三个profile全部为null，S1–S3与S7–S8的ec_number为null，A. tamarii未给TaxID——属诚实未知（P45），但仍是完成度不足。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:BIOPATH150_004：用于核对交付模块、字段完整性与主链边界表述
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_004：确认本题为BRANCHED_DAG、全图11步；仅作全图材料数，不作单条认可主链的缺步分母
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：用于定位所选主链S07/S08/S10与其余分支步，不据此要求交付全部旁支

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 所选主链三步转化、方向与主产物与gold S07/S08/S10逐字一致：咖啡因N7-脱甲基→茶碱、茶碱N1-脱甲基→3-甲基黄嘌呤、3-甲基黄嘌呤N3-脱甲基→黄嘌呤，甲醛作副产物正确；下游尿酸→尿囊素→尿囊酸→尿基乙酸→乙醛酸化学上可成立。但辅因子/氧还配平（O2、NAD(P)H、H+）未列，把分支DAG表述为单一线性链，并越过指定终点延伸到嘌呤分解代谢，连接与边界说明需修订，合理性多为内部知识；按5–6档并受base range &#91;2,5&#93;上限取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链前三步与gold分支化学一致：咖啡因→茶碱（gold S07）、茶碱→3-甲基黄嘌呤（S08）、3-甲基黄嘌呤→黄嘌呤（S10），方向为forward、无跳步、无一步跳到中心代谢物；S4–S8（黄嘌呤→尿酸→尿囊素→尿囊酸→(S)-尿基乙酸→乙醛酸）是真菌嘌呤分解代谢的合理延续，但超出gold终点（Xanthine|Formaldehyde），按P28/P29既不计覆盖扣分也不加分。档内取7而非8–9的依据：各步只写主有机物与甲醛/尿素等副产物，未列O2、NADPH/NAD+与H2O（S1–S3氧化性脱甲基缺氧化剂使甲醛生成字面不守恒；S5尿酸氧化缺O2与H2O），按P102–P103属局部计量缺陷，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：S07/S08/S10底物、主产物与方向；不扩展到未声称的辅因子或下游步骤
- ANSWER_TEXT / ANSWER:BIOPATH150_004：核对每步化学式、副产物与步骤连接

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分5 → V0.5新分7，变化+2。

新裁判理由：

> 三个必答目标S07/S08/S10的酶功能与accepted G4及gold反应一致：S1「caffeine N7-demethylase」对应咖啡因→茶碱、S2「theophylline N1-demethylase」对应茶碱→3-甲基黄嘌呤、S3「3-methylxanthine N3-demethylase」对应3-甲基黄嘌呤→黄嘌呤，产物与方向均对。但三步显式EC全为null、酶名为描述性而非registry精确名，名—EC配对及条目级身份未获E0核验；9–10不适用（release policy A NOT_ELIGIBLE / policy B NOT_SELECTED），在&#91;1,8&#93;内因已核名号配对不足取7。

<details><summary>V0.4理由与本行变化背景</summary>

S4黄嘌呤脱氢酶(1.17.1.4)、S6尿囊素酶(3.5.2.5)+DAL1、S5尿酸氧化酶uaZ等，酶名与反应类型自洽，属合理候选；但最具特征性的S1–S3咖啡因/甲基黄嘌呤N-脱甲基步骤只有描述性名称，ec_number与gene均为null、置信low，核心步骤缺任何可核验的酶身份；S5所填EC 1.7.3.0在E0无记录，accepted name/reaction无法核对，按四.6记UNRESOLVED（疑似与&#x27;urate oxidase&#x27;名称不匹配，需复核），不判错、不cap。整体落5–6档，取5因缺失恰在核心脱甲基步。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：S07为caffeine demethylase（1.13.12.-/1.14.13.178）、S08为7-methylxanthine/theophylline demethylase（1.14.13.128/1.13.12.-）、S10为methylxanthine N3-demethylase（1.14.13.179）；支持功能名/EC家族，不支持具体蛋白实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：S07咖啡因→茶碱、S08茶碱→3-甲基黄嘌呤、S10 3-甲基黄嘌呤→黄嘌呤的底物/产物/方向
- ANSWER_TEXT / ANSWER:BIOPATH150_004：核对三步所给酶名与EC（均为null）

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> A. tamarii（种级，无TaxID/菌株）有organism_gold PATHWAY_COMPLETE=TRUE的整路径支持；但S1–S3的真菌单步归属在gold步级未给（S07步级物种为细菌），S4–S5归A. nidulans、S6–S8归S. cerevisiae仅有内部知识，TaxID 162425/4932未获E0核验且无来源条目。属合理候选+部分支持，关键身份与作用范围未充分核验，取5。

<details><summary>V0.4理由与本行变化背景</summary>

A. tamarii作为S1–S3降解菌，与gold把Aspergillus tamarii(41984, Fungi)列为PATHWAY_COMPLETE=TRUE、并在S08（茶碱→3-甲基黄嘌呤）列该菌的方向一致；A. nidulans(162425)与S. cerevisiae(4932)承担gold终点之后的嘌呤分解步，属经典模式菌但E0无记录。三profile均为物种级、strain留null，complete_pathway_organism_profile_id=null，未把单步支持写成整条路径能力；无跨类群/异菌株编号错配。扣分：步级归属（尤其S1、S3的A. tamarii）无条目级证据，S4–S8归属完全在gold范围外待核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_004：A. tamarii PATHWAY_COMPLETE=TRUE（物种级整路径能力）；S07步级物种行为细菌，不等于真菌单步归属；不扩展到A. nidulans/S. cerevisiae
- ANSWER_TEXT / ANSWER:BIOPATH150_004：核对各步微生物与profile身份字段

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 三个profile均返回15项结构，未知项以null/unknown如实标注；但A. tamarii多项关键数值（温度/pH/盐度/保藏/基因组）为null，所填性状（A. nidulans约37 °C、FGSC A4，S. cerevisiae 28–30 °C、兼性厌氧等）多为常识性内部知识，trait_gold对A. tamarii多为UNKNOWN、对A. nidulans/S. cerevisiae无本案记录，E0无法核验。部分性状合理适用但关键项证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状以常见物种一般性描述为主（丝状真菌、专性好氧、非运动、分生孢子、几丁质-葡聚糖细胞壁；酵母兼性厌氧、出芽、子囊孢子），方向合理；但来源均为EVID_006/007/008的INTERNAL_KNOWLEDGE_ONLY、raw_text全null，F2最适温度（37 °C/30 °C）与F5 FGSC A4等定量/编号项以medium置信给出，而E0与gold对这些物种无对应观测（item_gaps GAP-004-060…086；gold中A. tamarii性状全为UNKNOWN）；F3/F4/F14全部null属诚实未知（完成度已在D1扣）。未出现预测冒充观测，也未把单菌株观测推广为全物种（全部物种级、无strain级定量）。落5–6档，取5因关键定量项证据不足。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_004：A. tamarii性状多为UNKNOWN；A. nidulans/S. cerevisiae无本案性状记录；不扩展到未观测的菌株性质
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_004：标出哪些子字段在本案不可评分/仅完整性，避免把未核数值当作已核实
- ANSWER_TEXT / ANSWER:BIOPATH150_004：核对15项是否齐全、未知是否如实标注及来源指向

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 决策相关组（路线CG01/02/03、关键酶CG05、核心菌CG07）来源仅为INTERNAL_KNOWLEDGE_ONLY或「记忆性文献」（EVID_002无条目号、EVID_005 PubChem无record_id），无条目级可定位可核对来源；所选主链S07/S08/S10反应虽可由gold切片核对，但模型未交付对应可定位来源。按3–4档取3；无已核实错引，不触发cap。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07；CG04/CG08/CG10；CG14按claim条件）均无条目级可定位可核对记录：主链、酶、身份来源为EVID_001/003/004/006/007/008的INTERNAL_KNOWLEDGE_ONLY自述；唯一外部指向EVID_002（PubMed但record_id=null，且自述&#x27;记忆性文献依据…未能给出确切文献条目编号&#x27;）与EVID_005（PubChem无record_id），属笼统来源；编号类（EC 1.17.1.4/1.7.3.0/3.5.2.5、TaxID 162425/4932）处EVIDENCE_GAP→UNRESOLVED_SOURCE。按四.3/P41，决策相关组全部缺失或笼统→3–4档；无经核实错引（MISSING/GENERIC默认不cap），故不触发关键错误；因registry逐条带claim_scope、来源类型与记忆性有明确声明，取该档上限4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:BIOPATH150_004：核对实际交付的来源类型与可定位性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：说明哪些反应事实本可被gold核对，但模型未交付对应来源

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> uncertainties逐条列出首步N7/N1歧义、真菌脱甲基酶未纯化/EC与基因未知、Hakil文献为记忆性、尿囊酸分解路径差异、S7/S8 EC null及多数性状缺失；confidence多用low/medium，evidence_registry以INTERNAL_KNOWLEDGE_ONLY如实标注。主要限制与冲突已说明，个别性状以medium呈现但未系统性误导，取7。

<details><summary>V0.4理由与本行变化背景</summary>

披露整体扎实：6条uncertainties逐项列出首步产物选择分歧（茶碱vs可可碱）、脱甲基酶未被纯化鉴定、Hakil文献为记忆性且无编号、尿囊酸分解路线分歧、S7/S8 EC留null不猜、性状大量null；alternative_branches明确把细菌路线标为is_part_of_scored_main_route=false，未混入主链；置信多为low/medium且与内部知识来源基本相称。档内扣分：把记忆性文献写成source_type=LITERATURE_DIRECT（应为内部知识类），且37/30 °C最适、FGSC A4、酵母&#x27;革兰阳性着色&#x27;等未核实项给medium置信，属单点过度确信/证据类型标注不严，但已披露、非系统性误导。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:BIOPATH150_004：核对观测/推断/未知的标注与限制披露

</details>

## DeepSeek

答案SHA256：`3645d2a5b6c187cfa4aa2237440decc37d02a5509d8c3eab5855f7723553a8fc`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 按D-M01只评一条已认可主链。答案S1-S3对应P004_5：S07 caffeine→theophylline、S09 theophylline→1-methylxanthine、S11 1-methylxanthine→xanthine，起终点和咖啡因真菌N-去甲基化主链一致。route_scope名称与好氧条件正确；steps、enzyme、microorganism、organism_profiles、15项traits、evidence_registry均已给出，未见核心模块缺失。S1-S3的EC为null，但题面允许未知填null；S4-S8属黄嘌呤下游嘌呤分解，超出该已认可主链终点，作为主链steps呈现属于轻微范围/放置问题，不构成D1关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

主链（8步）、每步底物/产物英文名+SMILES、微生物归属、15项性状均已交付，chosen_route_name原样为Caffeine (fungal) pathway，交付完整度较高。但S1–S3三个主链去甲基化步骤enzyme.ec_number为null，未满足‘一个首选酶及EC’的必填要求（关键步骤EC缺失）；去甲基化未列formaldehyde副产物；S4–S8为超出题面终点xanthine的下游延续（按P29不加分不扣分）。故落5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际包含route_scope、8个steps、1个organism_profile及15项traits、4条evidence_registry；用于核对交付结构。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：支持P004_5主链三步：S07 caffeine→theophylline、S09 theophylline→1-methylxanthine、S11 1-methylxanthine→xanthine；不证明下游S4-S8属于该gold主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_004：支持题面路线名为Caffeine (fungal) pathway、好氧及gold终点主产物含Xanthine/Formaldehyde；用于判断答案主链范围。
- SCOPE_ROW / SCOPE#BIOPATH150_004#CG04：题面明确aerobic（好氧），答案route_scope.oxygen_condition=aerobic与题面一致。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 化学主链S1-S3方向与顺序正确并匹配P004_5：S1 caffeine N7-demethylation→theophylline，S2 N3-demethylation→1-methylxanthine，S3 N1-demethylation→xanthine，连接连续。S4-S8为xanthine→uric acid→allantoin→allantoic acid→ureidoglycolic acid→glyoxylic acid+urea，整体嘌呤分解方向与所列酶类型合理。主要缺陷是多个步骤只列主产物，省略N-去甲基化释放的formaldehyde及氧化/氧化酶步骤的O2、CO2、H2O2等辅因子或副产物，属局部计量与简化表达问题，按P103/P104处理，不推翻主链；S4-S8又在gold终点之外，仅按化学自身质量评价，故不入9-10。

<details><summary>V0.4理由与本行变化背景</summary>

主链S1 caffeine→theophylline(N7)、S2 theophylline→1-methylxanthine(N3)、S3 1-methylxanthine→xanthine(N1)方向与化学连接正确，且与gold支路S07→S09→S11一致，并到达题面终点xanthine。局部缺陷：去甲基化未列O2/NAD(P)H与formaldehyde（辅因子/副产物简化，属局部计量缺陷，按P102/P103在7–8档处理，不自动cap）；S4–S8为超题面终点下游，按P29不进入覆盖评分。故7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：支持答案前三个目标转化的gold反应与方向：S07 caffeine→theophylline、S09 theophylline→1-methylxanthine、S11 1-methylxanthine→xanthine；不支持S4-S8作为gold主链步骤。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_004：gold终点主产物含Xanthine/Formaldehyde；答案S3已到xanthine，S4-S8为下游延续，不能作为该gold主链继续给分。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案声称的底物/产物、SMILES、反应类型与酶EC；用于核对主链方向、连接及省略辅因子/副产物情况。
- SCOPE_ROW / SCOPE#BIOPATH150_004#CG04：题面限定aerobic（好氧），答案route_scope为aerobic；用于判断化学路径是否与题面氧条件一致。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 在可判范围内，答案给出了caffeine→theophylline→1-methylxanthine→xanthine这一可对应accepted caffeine/theophylline/N1-demethylase功能的候选分支，首三步酶名与S07/S09/S11的家族功能相符；但前三步无EC且精确名号配对未核，目标绑定仍为U，额外下游嘌呤步骤不用于提高目标信用。D3a允许区间&#91;1,8&#93;且9–10不成立，按部分主干可用、需实质核验取6。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3酶名（caffeine N7-demethylase / theophylline N3-demethylase / 1-methylxanthine N1-demethylase）与所标反应类型功能一致，未见酶名与EC相互矛盾；但三个主链关键步骤EC为null，缺具体EC核验。S4–S8给出EC（1.17.1.4/1.7.3.3/3.5.2.5/3.5.3.4/4.3.2.3）与标准嘌呤分解酶对应，属合理候选，但E0无EC记录无法核实。综合为‘合理候选+部分支持、关键步骤缺具体核验’，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：列出caffeine demethylase、theophylline demethylase、methylxanthine N1/N3-demethylase等accepted名称/EC；只支持家族级目标功能，不证明答案无EC的精确N7/N3/N1命名或具体蛋白活性。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案以Aspergillus niger（TaxID 5061）作为全部步骤微生物，并声明complete_pathway_organism_profile_id=ORG_001。EVID_004最多只对应TaxID身份，且E0无该TaxID记录；没有任何冻结的反应级或全路径能力证据。gold真菌记录为Aspergillus tamarii/Penicillium commune等，不含A. niger，但缺记录不等于已证伪。按仅身份性候选、整路能力被过度外推，给4。

<details><summary>V0.4理由与本行变化背景</summary>

答案以单一Aspergillus niger（TaxID 5061）承担全部8步，并设complete_pathway_organism_profile_id=ORG_001（整条路径能力声称）。身份层面A. niger/5061在常识上可对应，但gold step级菌为A. tamarii/P. commune及多种细菌，A. niger不在gold菌列表（gold非穷尽，失配≠错误）；关键是步级反应能力与整条路径能力仅由INTERNAL_KNOWLEDGE_ONLY支撑，E0无记录可核，属‘身份定位≠反应级能力≠完整路径能力’的过度外推。未见经核实的身份错配（不cap），但作用范围未充分核验，5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_004：给出本题gold涉及的微生物与部分全路径记录；不包含A. niger，不能把缺失自动当作A. niger错误的证明。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案提供全部15项性状，10项有值、5项明确unknown/null；明确null本身是诚实披露。非空性状集中在A. niger的氧需求、呼吸、形态、产孢和一般碳源描述，均为内部知识来源；E0无A. niger性状记录，trait_gold也无A. niger行。多项性状表面合理但关键证据不足，且把部分一般性状用于整路能力论证，按部分可用、需实质核验给5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐备（filled=10，explicit_unknown=5，omitted=0）。有值项（obligate aerobe、aerobic respiration/O2、非运动、丝状菌丝、几丁质壁非革兰染色、产分生孢子、广谱碳源、降解caffeine、若干酶活、腐生栖息地）对A. niger在常识层面大致正确且与所选物种匹配（物种级profile，按P52同物种粒度可接受）；但全部来源为INTERNAL_KNOWLEDGE_ONLY、无独立可核依据，且温度/pH/盐度/保藏号/基因组等关键定量项为null（诚实未知，完成度问题主要归D1）。按P46不默认正确、不判错，属‘部分性状准确适用但关键项证据不足’5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_004：本题trait gold不包含TaxID 5061/A. niger的性状行；不能据此判定答案性状正确或错误。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_004：显示本案可评分性状主要针对gold列出的其他微生物；A. niger无对应可评分记录。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D5只评价实际交付来源。答案的路线、酶、性状关键结论主要由EVID_001–EVID_003支持，而这些均标为INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE；EVID_004为NCBI Taxonomy记录，但locator为null且E0无冻结记录，TaxID 5061只能登记UNRESOLVED_SOURCE。没有可定位文献/数据库条目支撑关键结论，也未核实为错引；按几乎无法定位重要依据给2。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出evidence_registry并逐段绑定EVID_001–EVID_004，但EVID_001/002/003均为INTERNAL_KNOWLEDGE_ONLY（按P34归MISSING_SOURCE），仅EVID_004为DATABASE_DIRECT(NCBI Taxonomy, record 5061)且只支持taxid身份、E0无法核实。决策相关组（CG01/02/03/05/07/08/09等CORE与APPLICATION_CRITICAL）几乎全为MISSING_SOURCE，路径/酶/性状主要结论无法追到可定位文献或条目；无已核实错引（E0 GAP不能判虚构/错引），MISSING_SOURCE默认不cap，取低分档3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案对多数酶用low、对TaxID用medium、对未知性状显式null，并标明INTERNAL_KNOWLEDGE_ONLY，说明并非系统性把预测写成实证；但uncertainties为空，route_summary与complete_pathway_organism_profile_id表述过强，未具体说明主链绑定、A. niger整路能力、SMILES/EC核验等限制。按有多处不确定性提示但过于笼统、部分结论强度超过依据给6。

<details><summary>V0.4理由与本行变化背景</summary>

答案通过evidence.source_type=INTERNAL_KNOWLEDGE_ONLY与confidence(medium/low/unknown)对证据性质做了部分披露，未把内部知识伪装成DATABASE_DIRECT（除taxid），具一定诚实度；但route_summary与complete_pathway_organism_profile_id=ORG_001以肯定语气陈述全路径能力、steps.uncertainty全为null、uncertainties为空数组，未显式区分预测/推断与观测、未列主要限制。属‘有不确定性说明但过于笼统、部分结论强度超过依据’，5档；未达系统性误导cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`4211d198563932bee07bc91d6d272a9318c669c3c93fffe2b02f5bf9bbf870ea`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案给出指定真菌好氧路线、8个步骤、每步底物/产物/酶/菌，以及两个organism_profile各15项性状；所选P004_2主链S03/S04/S02由答案S1-S3对应交付。按base_range&#91;1,6&#93;取6：主模块齐全且关联清楚，但前三步EC为null、若干性状仅低置信内部知识，且下游延伸超出主链终点，均属完整性/表达上的实质保留，不进入更高档。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8：路径、酶、微生物、性状、来源、不确定性六个模块均有实质交付；8步均给出底物/产物英文名与SMILES、酶与菌；organism_profiles按物种去重为2条（A. tamarii、A. nidulans FGSC A4），每条15项性状齐全。取7而非8：题面明确要求“一个首选酶及EC”，而S1–S3的ec_number与gene_or_protein全为null（自述未表征，属诚实未知但仍构成完成度缺口）；A. tamarii的strain/TaxID/基因组全null；两个profile各有4项性状为明确未知；此外S1产物SMILES误用咖啡因字符串（RE-01，表示层缺陷）。S4–S8越过gold终点（xanthine）属额外下游延续，按四.2/P29不加分亦不据此扣覆盖率。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：支持答案交付了8步主链、酶与对应微生物；不证明各酶-反应已被官方证据确认。
- ANSWER_TEXT / ANSWER.organism_profiles：支持两个菌profile及15项性状字段已给出；不证明性状数值均经外部核验。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_004：支持题面路线名为Caffeine (fungal) pathway、好氧与终点背景；不支持答案中未交付内容。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_004：支持本题为BRANCHED_DAG、ordered_step_count=11；该全图行数不作为单条主链缺步分母。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 所选P004_2的S03/S04/S02三步在答案S1-S3中方向正确：Caffeine→paraxanthine→7-methylxanthine→xanthine，底物/产物结构匹配，N-脱甲基顺序与产物一致。下游嘌呤链总体合理，但S5将5-hydroxyisourate/OHCU中间体合并并给H2O2，S7-S8辅因子与计量有简化，属于主干成立但局部转化/计量需修订；按base_range&#91;2,5&#93;取5。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8，取7。成立之处：S1–S3的转化身份与顺序与gold第二支逐字吻合（caffeine→1,7-dimethylxanthine→7-methylxanthine→xanthine），S1–S3列O2为辅底物、formaldehyde为副产物，与gold参与者一致；S4–S8为教科书式嘌呤降解链，方向正确、碳/氮骨架大体守恒。扣分理由：(a)S1产物paraxanthine的SMILES与咖啡因SMILES完全相同（RE-01），字面上该步未发生去甲基，结构表示与名称矛盾；(b)脱甲基三步缺NAD(P)H/H+、S4缺NAD+，按八.辅因子条款属局部计量缺陷，7–8档内处理，不cap；(c)S5把HIU/OHCU合并已明确声明，S7把allantoicase（生成ureidoglycolate）与后续lyase步合并为allantoate→urea+glyoxylate且未标出ureidoglycolate。以上均为局部问题，未推翻“主链为真菌N-脱甲基后接嘌呤降解”的主要结论，故不判关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：支持所选三步的金标方向与主底物/主产物；不支持把下游所有分支并入评分主链。
- ANSWER_TEXT / ANSWER.steps.S1-S3：支持答案三步的底物、产物、SMILES与顺序；不能证明辅因子完整配平。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：支持这些步骤的酶类/EC参考类别；不支持答案未给出的显式EC。

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 程序将S02/S03/S04标为U，但人工对照accepted sets可见三步底物/产物均MATCH，且酶名可对应：S3“7-methylxanthine demethylase”与accepted名一致；S2“1,7-dimethylxanthine N1-demethylase”为paraxanthine demethylase别名；S1“caffeine N3-demethylase”与caffeine demethylase同类且产物paraxanthine一致。三酶均无显式EC，但题目允许未知EC填null，不能据此判错。因名-EC配对未充分显式、E0无记录，取&#91;7,8&#93;下沿7而非8；未发现催化矛盾，不触发KEY4。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6，取6。5步给出EC：1.17.1.4（黄嘌呤脱氢酶）、1.7.3.3（尿酸氧化酶）、3.5.2.5（尿囊素酶）、3.5.1.5（脲酶）与其标注的反应类型相符；S7写作“allantoicase (allantoate amidohydrolase)”并配EC 3.5.3.4，名称括注所指酶与EC所指酶不一致，且产物列为urea+glyoxylate（allantoicase自体反应产物为ureidoglycolate），酶名-EC-产物三者不协调。路径定义性的S1–S3 N-脱甲基酶只给功能名，EC与基因全为null并自述未表征；gold对这些步提供1.14.13.178/1.13.12.-候选，答案既未采用也未说明与真菌酶的对应关系，故核心步骤酶对应仍缺具体核验。综合取6：有合理候选与部分支持，若干关键步骤未获核验。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：支持这些目标反应可由accepted酶名/EC类别催化；不支持任意具体蛋白实验活性。
- ANSWER_TEXT / ANSWER.steps.S1-S3.enzyme：支持答案给出的酶名与EC null；不能证明缺失EC已被补足。
- RUBRIC_CLAUSE / C04.4：用于说明局部U/关键性判断与9–10门；不替代科学事实核验。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> A. tamarii为Gold organism表中真实出现且PATHWAY_COMPLETE=TRUE的咖啡因降解真菌，物种身份可靠；A. nidulans FGSC A4的TaxID 227321与FGSC A4保藏号有答案引用，身份层面合理。第一步和第三步把A. tamarii写成单步酶归属，Gold单步行不直接支持，属于步骤级待核；但未把单步支持冒充为已逐酶实验确认，且complete_pathway字段为null，未过度声称整条路径。因此取7档上沿偏保守。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8，取7。A. tamarii与Aspergillus nidulans FGSC A4都是与本题真菌路线相容的选择，且gold在paraxanthine/theophylline demethylase等步确实列有A. tamarii，身份方向一致；身份层未出现跨属/跨kingdom或异菌株错配：A. nidulans给出菌株与TaxID，A. tamarii的菌株、TaxID诚实留null。答案显式区分“步级能力”与“整条路径能力”（complete_pathway_organism_profile_id=null，并在uncertainties声明真菌体内嘌呤降解能力未经逐一实验确认），未由基因组/注释存在直接推断整条路径。扣分：S1（caffeine→paraxanthine）在gold该步仅列细菌，答案仅以一篇文献（EVID_002）支撑真菌承担，属支持粒度待确认；A. nidulans的TaxID 227321与hxA/uaZ归属在本案无冻结记录。故7档取7：主要微生物身份对应可靠，少量具体条目待确认。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_004：支持A. tamarii为已收录的咖啡因降解真菌及部分步骤归属；不支持所有单步酶归属。
- ANSWER_TEXT / ANSWER.organism_profiles：支持两个菌的物种/菌株/TaxID声称；不证明其所有单步催化均已实验确认。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_004：支持A. tamarii身份及部分记录；不支持A. nidulans的本地性状/酶记录。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 两个profile均返回15项性状，未知项多填null，未用编造数值填满；A. nidulans F5 FGSC A4有较高置信引用，A. tamarii的咖啡因利用/降解/酶活与EVID_002一致。但温度、pH、盐度、基因组等关键定量项大量缺失；多数一般性状仅EVID_006内部知识且低置信，A. nidulans又无本地记录。按D4“部分性状准确且适用，但关键项证据不足”取6，而非7–8。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8，取7。性状全部为定性/物种级描述，数值子字段（F2的min/opt/max、F3、F4）一律填null而未编造；未把培养温度或生长观测点写成耐受极限，未把单菌株观测推广为全物种，也未把酶活观测外推为整菌生长（F8/F9均限定在嘌呤/咖啡因降解语境并标medium）。好氧、非运动、分隔菌丝、分生孢子、几丁质-葡聚糖壁等与曲霉属生物学一致，逐项标low/unknown并注明EVID_006为内部知识。扣分：两个profile各4项性状全null（完成度缺口归D1，此处不重复重扣）；F5把“FGSC A4”拆为collection=FGSC、accession=A4并以high置信+DATABASE_DIRECT呈现，属把菌株代号当保藏编号的单点过度包装；关键数值性状全缺，无法在本案核验。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_004：支持A. tamarii多项性状在Gold中为UNKNOWN、部分F14/身份记录可查；不支持答案所有一般性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_004：支持哪些性状属于可观测准确率计数、哪些仅完整度/待裁决；不把不可评分项当错误。
- ANSWER_TEXT / ANSWER.organism_profiles.traits：支持答案已返回全部15项及低/unknown置信标签；不证明数值全部正确。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出逐步骤/逐性状的 evidence_id 并登记 EVID_001–EVID_007，S4–S8 的 Aspergillus nidulans 酶名/EC 及 FGSC A4 保藏号有较具体来源，可部分追溯；但 S1–S3 关键上游脱甲基酶仅有文献/图谱级或推定证据（EVID_002/EVID_001），酶名与 N3/N1 区域化学未在 claim_scope 中明确支持且无 EC；EVID_004 为 AspGD/FungiDB 主页式登记，缺具体条目号；大量性状（尤其 ORG_001 与 ORG_002 的 F1/F2/F6/F10–F13/F15）仅指 EVID_006 INTERNAL_KNOWLEDGE_ONLY 且 raw_text 为 null，无法核到可定位记录。整体为部分关键结论可定位、其他模块缺可核记录，属5分档。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（部分关键结论可定位，其他模块仍缺映射或必要生成记录），取5。可定位之处：路线三步有EAWAG-BBD咖啡因映射页URL（EVID_001）、完整文献题录Hakil et al. 1998（EVID_002）与MetaCyc途径名（EVID_003）；核心菌身份给出NCBI Taxonomy记录227321（EVID_005）与FGSC A4（EVID_007）。不足：CG05对S1–S3核心脱甲基酶完全无来源（EC/基因null，仅功能名），其余酶仅AspGD/FungiDB首页级笼统来源（无entry ID）；CG10/CG11–CG16性状与氧需求几乎全部依赖EVID_006 INTERNAL_KNOWLEDGE_ONLY。本案E0为EVIDENCE_GAP（entries=0），任何引用-声称支持均无法机器核对，故不判虚构、不判错引，全部按UNRESOLVED待核；同一单元未出现已核实错引，不执行cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：列出目标步可接受的酶名/EC条目；用于核对答案 S1-S3 推定酶名和缺失 EC 未能逐条对应到可接受条目，不证明答案引用内容为假。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_004：列出目标步的策展微生物记录；支持答案下游 A. nidulans 与 FGSC A4 相关身份/保藏信息有可核记录，但不支持 S1-S3 所有 A. tamarii 酶名/EC 均为具体条目支持。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确把S1-S3酶标为推定/未表征，说明无EC；S5说明合并HIU/OHCU中间体；下游A. nidulans被限定为代表性酶学注释而非逐一实验确认；A. tamarii菌株/TaxID/基因组未知处填null；alternative_branches明确标为不属于评分主链。主要限制、未知和证据性质披露较充分，仅少数一般性状为低置信内部知识且部分raw_text为null，取8而非9。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8，取7。正面：uncertainties五条与逐步confidence把推定单加氧酶无EC、HIU/OHCU中间体合并、allantoicase与allantoate amidohydrolase分支差异、A. tamarii菌株/TaxID缺失、模式菌酶学注释代表物种能力等限制逐项写明，并明确“具体菌-酶对应未经逐一实验确认”；酶未知处如实置null而非猜测EC；未把计算/数据库注释写成实验观测。扣分：EVID_002/EVID_005标high、F5以DATABASE_DIRECT+high包装无法核对的保藏信息，属单点过度确信（按八.D6档内扣分，不cap）；未声明S4–S8已越过本题路线在gold中的终点xanthine；S1产物SMILES与底物相同的内部矛盾未在uncertainties中披露。整体披露质量高、无系统性误导，故7档取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持答案明确披露推定酶、缺失EC、合并步骤、代表菌限制及null值；不证明这些披露本身已外部核验。
- ANSWER_TEXT / ANSWER.steps.*.uncertainty：支持逐步不确定性标注；不能替代D2/D3的科学证据。
- ANSWER_TEXT / ANSWER.alternative_branches：支持答案把细菌路线明确排除在评分主链外；不把替代路线计入目标完成。

</details>

## Qwen

答案SHA256：`d275d2749fcc5e5dfa47620b7516aaf07af0fbee4a328778451386d04fe9ce5d`。

复审/来源说明：REVIEW_SCOPE_REQUIRED on D3a (see S8/README and 20261114 card): branch-scope rationale not yet human-confirmed

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 路线名称与好氧条件已原样回显，交付了5个主链步骤、底物/产物英文名与SMILES、酶名和对应微生物，且15项性状键均出现。但S1–S3的ec_number均缺失，题干要求的每步首选酶及EC未完整落实；多个性状为null/unknown；对本题预先认可主链的必要步覆盖仍有限。属主要模块均有涉及但若干必要内容遗漏，故在5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

结构层面完成、必需模块均有交付：route_scope.chosen_route_name 原样填写 &#x27;Caffeine (fungal) pathway&#x27;，oxygen_condition=aerobic；S1–S5 均给出主底物/产物英文名与 SMILES、一个首选酶与一个对应微生物；单一 ORG_001 profile 含全部 15 个性状槽位。但实质完成度有限：S1–S3 缺 EC 与基因/蛋白、无 strain 与 TaxID、6/15 性状为 null（诚实未知，按 P45 反映完成度而非错误）、来源全部为 INTERNAL_KNOWLEDGE_ONLY。按 &#x27;主要模块均有涉及，但若干必要内容遗漏&#x27; 取 6 档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;：交付5步，含底物/产物、SMILES、酶名、微生物；S1-S3的ec_number为null
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：15项性状键均出现，多项value为null/unknown
- QUESTION_TEXT / QUESTION.route_scope：题面固定路线名、好氧条件及每步酶/EC/微生物字段要求
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_004：本题gold终点主产物含Formaldehyde|Xanthine；不能把全图各分支直接当作D1唯一缺步分母

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案主链为咖啡因逐步N-去甲基化至黄嘌呤，并继续黄嘌呤→尿酸→尿囊素；方向均为底物到产物，关键中间体连接总体可辨认，黄嘌呤氧化酶/尿酸氧化酶步给出O2、H2O与H2O2，化学上大体合理。存在局部问题：S1–S3的N-去甲基化未列O2/NAD(P)H等辅因子，字面计量不完整；theobromine→7-methylxanthine为未在gold该分支直接列出的替代连接，但其化学上并非明显不可能；黄嘌呤后继续下游不额外加分也不按未延续下游扣分。按P103辅因子遗漏通常为局部缺陷，不触发关键错误，故在7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

起点与核心转化化学成立：S1 caffeine→theobromine 与 gold S01 一致，S3 7-methylxanthine→xanthine 与 gold S02 一致；caffeine/theobromine/7-methylxanthine/xanthine 的 SMILES 与 gold canonical 一致，甲醛作为氧化去甲基副产物化学正确。S2 theobromine→7-methylxanthine 为 gold 未收录的合理 N-去甲基化分支（gold S05 走 theobromine→3-methylxanthine），未以 alternative_branches 声明属替代支路，按合理替代路线四步判断作档内扣分、不 cap。S1–S3 未列 O2/NAD(P)H 属辅因子简化（P103 局部计量缺陷）。S4 xanthine→uric acid、S5 uric acid→allantoin(+CO2+H2O2) 化学与计量成立，但位于 gold 终点 xanthine 之外，按 P29 属额外下游，不加分亦不扣 D2 覆盖分。取 7 档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;：S1-S5的底物/产物、方向与连接；S1-S3缺辅因子标注
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：用于比对目标反应底物/产物和终点xanthine；gold为分支图，不能据此要求全部旁支
- RUBRIC_CLAUSE / P103：主有机物转化正确但辅因子遗漏通常为局部计量缺陷，不自动cap

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 仅按目标反应相应粒度的酶/功能支持计分：S01咖啡因→可可碱的caffeine demethylase与S02 7-methylxanthine→xanthine的7-methylxanthine demethylase可按accepted名称/功能支持为S；S04处于ROUTE_HOLD_REPRESENTATION/UNRESOLVED，答案theobromine→7-methylxanthine不能作为S04 paraxanthine demethylase目标反应；其余多个目标步在给定五态表中为MISSING。能确认的目标功能很少，核心目标酶对应链基本未建立，故落在1–2档并取2。S4–S5尿酸盐/尿囊素步超出gold终点xanthine，不作为本题目标反应加分。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3 酶名（caffeine demethylase / theobromine demethylase / 7-methylxanthine demethylase）与 gold 同一步的酶名属同一家族、反应类型（氧化去甲基）方向正确；但 S1–S3 的 ec_number 与 gene_or_protein 均为 null，仅家族级候选、缺具体催化身份与编号核验。S4 xanthine oxidase EC 1.17.3.2、S5 urate oxidase EC 1.7.3.3 数值上与通行对应一致，但 E0 为整题 EVIDENCE_GAP，按四.6 保持 UNRESOLVED、不判错也不判虚构。未见 EC 大类与反应类型互相矛盾（无水解酶解释羟化等错配）。按 &#x27;合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27; 取 6 档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.enzyme：S1 caffeine demethylase EC null；S2 theobromine demethylase EC null；S3 7-methylxanthine demethylase EC null；S4/S5为下游酶
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：accepted酶名/EC用于S01、S02等目标反应；只支持数据库策展功能粒度，不证明具体蛋白实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：目标反应的底物/产物与方向；S02产物为xanthine；S04/S05底物或产物与答案S2不完全对应
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_004：gold终点主产物含Formaldehyde|Xanthine；尿酸/尿囊素属下游，不是本题目标反应

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案将全部步骤归于Aspergillus sydowii，物种层面是合理真菌候选且与好氧真菌路线类型相符；但无strain、TaxID、菌株级能力或反应级证据，冻结gold亦未列A. sydowii。未发现可核实身份矛盾，故按D3b中档5：有合理候选但关键反应级能力未充分核验，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

5 步全部归属同一物种 Aspergillus sydowii，仅物种级名称，strain 与 ncbi_taxid 均为 null，证据仅 INTERNAL_KNOWLEDGE_ONLY（EVID_001/EVID_003）。该属与 gold 真菌步骤菌（Aspergillus tamarii 41984、Penicillium commune 36653）同生态位但非同种记录；gold 未覆盖不自动判错。按 P69 三层核验：身份定位（物种名真实但未给菌株级/编号）、单步反应级能力（无独立证据）、完整路径能力（complete_pathway_organism_profile_id=null，未作全路径菌声称，未越级）。因 &#x27;合理候选和部分支持，但若干关键身份与作用范围未充分核验&#x27; 且把同一未核物种写成 5 步催化剂，取 5 档；无已核实身份错配或编造，不触发身份阶梯 cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_004：gold列出各步真菌/细菌归属（如A. tamarii、P. commune等），未列A. sydowii；未列不等于已证伪。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项外壳齐全，9项有值、6项明确null；氧耐受/呼吸方式/形态/产孢/栖息地等定性描述较合理，但A. sydowii无冻结trait记录，F7/F8/F9的碳源/降解/酶活声称缺外部定位来源。无已核实数值或单位矛盾，按D4中档5：部分性状可用但关键证据不足，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

单一 profile 15 项中 9 项有值、6 项诚实 null（F2/F3/F4/F5/F10/F14），无数值编造。已给性状以属级泛化陈述为主：F11 filamentous fungus、F12 fungal cell wall/Gram stain not applicable、F13 produces conidia、F15 soil and plant-associated fungus，与真菌一般特征相符但非菌株级观测；F7/F8/F9 实质复述本答案的降解能力声称，缺独立证据（有循环论证风险）；F1 aerobic、F6 aerobic respiration/O2 与题面氧条件一致但仅内部知识。A. sydowii 在 trait_gold 中全部性状为 UNKNOWN/无观测（item GAP-004-042~047），故无已核实数值错误、无 &#x27;预测冒充观测&#x27;、未把特定观测推广为全物种耐受范围。按 &#x27;部分性状准确且适用，但关键项证据不足&#x27; 取 5 档；关键定量性状缺失的完成度问题按 P112 归 D1，不在此重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_004：冻结trait表未含A. sydowii行，不能支持已填性状；缺失不是已证矛盾。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_004：提供其他gold菌株的可评分/不可评分字段，不适用于未列A. sydowii的性状核验。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> evidence_registry三条均为INTERNAL_KNOWLEDGE_ONLY，无database、record_id或可定位locator；决定相关组只能登记MISSING_SOURCE。因答案仍提供内部claim_scope绑定，不是零结构，取低档2；无经核实的LOCAL/CRITICAL/SYSTEMIC错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

按六状态逐组登记：全部 claim group 仅有 INTERNAL_KNOWLEDGE_ONLY 自我声明（EVID_001–003），属 MISSING_SOURCE（P34）；决策相关组（CG01/CG02/CG03/CG05/CG07 与任务条件成立的 CG04/CG10、声称级 CG14）均无任何条目级可定位可核对来源，SUPPORTING 组同样缺失，故落低分档。E0 为整题 EVIDENCE_GAP：EC 1.17.3.2/1.7.3.3、A. sydowii 身份与性状声称保持 UNRESOLVED（P40/P51），不计已核实错引、不判虚构。MISSING_SOURCE 属缺失而非误导，默认不触发 cap（P34/P35），故 severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。档内取 3：EVID 到步骤/性状的映射与 claim_scope 清楚、诚实自标内部知识，但无一条结论可外部追溯。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案多处明确标注内部知识、low/medium confidence、未知EC/辅因子，并说明黄嘌呤氧化酶可能由脱氢酶替代；null与不确定性字段较诚实，未系统性把预测写成实证。少数EC以medium confidence给出且无外部来源，故列8不列9；不cap。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体较好：uncertainties 明确列出初始三步缺 EC/基因/辅因子、Aspergillus sydowii 与菌株信息仅内部知识且置信低、真菌中可能由黄嘌呤脱氢酶替代、尿囊素后步骤未纳入主链；S1 uncertainty 明确声明甲醛为 &#x27;按一般氧化去甲基化推断&#x27;；confidence 全篇以 low/medium/unknown 标注，未把推断写成实测。扣分点：S4/S5 的 EC 以 &#x27;medium&#x27; 包装但证据同为 INTERNAL_KNOWLEDGE_ONLY（虽已披露脱氢酶替代，属单点过度确信、非系统性误导，P119 档内扣）；S2 theobromine→7-methylxanthine 这一非 gold 分支未标注为替代/待核。取 7 档。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`fd8591d6311ad8417bc877ca753c5bd80e181b66b4c76b214b12c70087c97242`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所评主链取已认可P004_4（Caffeine→Theophylline→3-Methylxanthine→Xanthine）。答案route_scope原样填写Caffeine (fungal) pathway与aerobic，3步主链逐步给出底物/产物/SMILES/酶/微生物，15项性状字段齐全且以null显式标未知，单一ORG_001去重，符合主链范围且未把未选分支计为缺步。全步EC为null、7项性状为null使完成度未达满分；这些是显式未知而非缺失字段或格式失败。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION#BIOPATH150_004：题面指定Caffeine (fungal) pathway与aerobic，并要求每步底物/产物/SMILES、酶及EC、微生物和15项性状
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_004：支持路线名Caffeine (fungal) pathway、起始物Caffeine、终产物Xanthine/Formaldehyde及好氧条件
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：支持P004_4的三步主链反应S07/S08/S10及其主底物/主产物对应；未选旁支不计缺步
- SCOPE_ROW / SCOPE#BIOPATH150_004#CG04：题面氧条件aerobic已冻结为关键任务条件
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_004：全图为11步分支DAG，但不是要求全部旁支；D1按单条认可主链评价

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所评主链P004_4的三步化学转化与已认可主链一致：Caffeine经N7-去甲基生成Theophylline，Theophylline经N1-去甲基生成3-Methylxanthine，3-Methylxanthine经N3-去甲基生成Xanthine；方向均为底物到产物，连续性无断裂，主产物及SMILES总体对应。主要不足是各步未列出O2/NAD(P)H等辅因子与甲醛副产物，且答案明示未核实；按P103属局部计量/副产物表达问题，不推翻主链结论，故在7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：支持S07 Caffeine→Theophylline、S08 Theophylline→3-Methylxanthine、S10 3-Methylxanthine→Xanthine的主产物与正向连接；Formaldehyde在相应反应中为byproduct
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：支持去甲基化酶功能与相关反应步骤的已接受酶名/EC集合；具体EC配对仍需逐项核验
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_004：支持终点包含Xanthine与Formaldehyde，P004_4以Xanthine为末端主产物
- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;：答案实际交付的三步底物、产物、SMILES、反应类型及不确定性说明

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案显式给出咖啡因→茶碱→3-甲基黄嘌呤→黄嘌呤的连续分支，对应金标S07→S08→S10并到黄嘌呤终点；三步功能名分别与accepted集合的caffeine demethylase、theophylline/methylxanthine N1-demethylase、methylxanthine N3-demethylase在功能粒度上相符。没有显式EC，KEY定义/高分门未完成，因此不进入9–10；D3a允许范围&#91;1,8&#93;内取7：主要功能对应可靠，但酶编号与关键性绑定仍有局部缺口。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：支持S07咖啡因→茶碱、S08茶碱→3-甲基黄嘌呤、S10 3-甲基黄嘌呤→黄嘌呤的底物/产物方向；不证明具体蛋白或实验活性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：提供这些步骤的accepted功能名/EC集合；答案未给EC，仅可作功能级对应，不自动等于具体蛋白催化证据。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案将各步统一归到Aspergillus tamarii，未给菌株、TaxID或基因组号；金标organism_gold中A. tamarii（TaxID 41984，Fungi）带PATHWAY_COMPLETE=TRUE，可在物种/整路径能力层支持主要微生物选择。该支持不等于每一具体步骤的菌株级归属均已逐条列出，且答案来源仅为内部知识，故取7而非更高。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_004：支持Aspergillus tamarii为物种级PATHWAY_COMPLETE=TRUE的真菌；不支持答案未给出的菌株身份，也不自动逐条支持S07/S10的菌株级归属。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案按15项性状返回，8项填写、7项明确null、0项遗漏；null项符合诚实未知，不应与错误等同。已填写项多为A. tamarii的泛真菌/属级性状（好氧、O2呼吸、不运动、有隔菌丝、真菌细胞壁、分生孢子）及咖啡因降解/N-去甲基活性，方向合理但主要依赖内部知识；金标trait_gold中A. tamarii除TaxID外大多为UNKNOWN，关键定性/定量性状缺少冻结观测支持，故落5–6档取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_004：A. tamarii行除TaxID 41984外基本为UNKNOWN；不能把答案的属级常识回填成已观测菌株性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_004：显示A. tamarii多数性状为completeness_only/不可评分观测；支持D4低档而非判错。

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 路线/步骤可追到EVID_001这一条具体文献题录，属于条目级可定位记录；但E0为证据缺口，无法核对其是否支持所声称的具体酶名和分支。微生物、步骤归属和多数性状依赖EVID_002/EVID_003的INTERNAL_KNOWLEDGE_ONLY，按D5属MISSING_SOURCE类，不是已核实错引。整体为部分关键结论可定位、其他模块缺条目级来源，落5–6档取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：记录答案实际交付的来源：EVID_001为具体文献题录；EVID_002/EVID_003为INTERNAL_KNOWLEDGE_ONLY。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_004：证明A. tamarii多数性状在冻结trait_gold中为UNKNOWN；不能回填为答案来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案较清楚地标注了未知：酶EC/基因/辅因子/一碳副产物未核实、菌株与TaxID未核实、温度/pH/盐度等缺菌株级数据、黄嘌呤下游不计入主链、可可碱支路明确标为非评分主链。证据类型也在evidence_registry中分开标注。主要不足是EVID_002/EVID_003为内部知识却仍用于若干性状/微生物声称，置信度标注为medium/low，存在轻度过度包装但有披露，故取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案对EC、基因、菌株、性状缺口、下游边界和替代支路的披露内容。

</details>

## GPT5.6

答案SHA256：`fad3fc2ab7f16e48164652f47801add01b02bde93755ae543679dd3dd1649be7`。

### D1 完整性与任务符合度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 7档：题面要求的路径、酶、微生物、15项性状与来源框架均有实质回答，route_name 原样；但所选主链与全 gold 主链的绑定处于 BOUNDARY_REVIEW，答案又把 xanthine→uric acid 作为主链一步并放在 gold 终点 xanthine 之外，另有多项显式 unknown，故仅少量到中等遗漏。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / question.json messages&#91;0&#93;.content：题面锁定 Caffeine (fungal) pathway、aerobic、要求每步给主底物/主产物、酶/EC、微生物及15项性状。
- ANSWER_TEXT / ANSWER.steps：答案给出4步连续咖啡因去甲基化/氧化路径及对应微生物；不证明全 gold 主链绑定。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 7–8档：Caffeine→Theophylline→3-Methylxanthine→Xanthine 的 N-去甲基化方向与结构连续，Xanthine→Uric acid 的氧化在化学上成立；主链无方向反转或明显守恒错误。去甲基化步骤未列甲醛副产物/O2/NAD(P)H 等辅因子，按局部计量缺陷处理；uric acid 是 gold 终点 xanthine 之外的额外下游，但化学本身未引入关键错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：给出 gold 主链各步底物/产物与方向，支持评估已交付的各步化学连续性；不把 gold 全部旁支当作必答分母。
- ANSWER_TEXT / ANSWER.steps：答案给出四步底物/产物 SMILES 与反应类型，可核对主转化方向与连续性。

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a 5–6档：答案给出的前三个去甲基化功能名与 gold 中 caffeine demethylase、theophylline demethylase/methylxanthine N1-demethylase、methylxanthine N3-demethylase 的功能级 accepted 记录方向一致，但这些步骤均未给 EC；第4步 EC 1.17.3.2 在 E0 无冻结记录。全 gold 主链未自动绑定（BOUNDARY_REVIEW），缺失其他 gold 目标步不能作为已证实错误，但也阻止进入7–8档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_004：给出本案各 gold 步 accepted 酶名/EC 的功能级集合；不证明具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_004：支持核对答案已交付步骤的底物—产物方向；不自动补齐未绑定分支的必答性。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b 7–8档：物种名 Aspergillus tamarii 与 gold 的物种级身份一致，organism_gold 的 PATHWAY_COMPLETE 行对该物种给出完整路径能力 TRUE，支持“整条路径菌”的物种级声称；但 answer 未给 TaxID/菌株号，且除 Theophylline→3-Methylxanthine 外，逐步归属没有逐条 A. tamarii 记录可核，故取7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_004：支持 Aspergillus tamarii 物种级身份及 PATHWAY_COMPLETE TRUE；不支持未给出的菌株号/具体菌株级能力。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4 5–6档：15项外壳齐全，但7项为显式unknown/null；有值的氧耐受、呼吸方式、底物利用、降解能力、N-去甲基化活性、丝状形态、分生孢子等只有部分 EVID_001 或完全无来源，且 A. tamarii 的 gold 性状大多为 UNKNOWN，无法核实到物种/菌株级观测。无离谱数值或单位错误，但关键氧性状与多个一般性状证据不足，故为部分可用。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_004：本案 A. tamarii 的绝大多数性状为 UNKNOWN，不能为答案的有值性状提供观测支持，也不能把一般真菌常识当物种/菌株观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_004：显示 A. tamarii 多个性状无可评分观测；支持按证据不足而非数值错误处理。

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 3–4档：决策相关结论主要依赖 EVID_001 的泛化文献声明（无作者/DOI/条目定位）和大量无来源字段；EVID_002 仅给 EC 记录号 1.17.3.2，但在 E0 无冻结记录，EVIDENCE_GAP 下登记 UNRESOLVED_SOURCE，不判虚构。根据六状态条款，决策相关组多数仅有笼统/缺失来源，未达到5–6档“部分关键结论可定位并核对”。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示 EVID_001 无 locator，EVID_002 仅给 EC 记录号；不能证明具体关键结论已被可定位来源支持。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 7–8档：答案明确把多个酶/EC、菌株、TaxID、保藏号、基因组信息标为未知，uncertainties 具体列出 A. tamarii 菌株/ TaxID 未定、N-去甲基化酶 EC 未定、尿酸步骤连续性未确认；未把预测系统性写成实证。仍有若干一般性状（好氧、丝状、分生孢子）无来源但标 low/unknown，属于轻度证据边界不足，故取8档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案对菌株、TaxID、具体酶/EC 及尿酸连接的不确定性有具体披露；不代表所有性状均已核验。

</details>
