# BIOPATH150_146：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：sulfoquinovose degradation VI

污染物：6-sulfo-beta-D-quinovose；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 57 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 39.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 50.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 21 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 18 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 27.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`dcce8b3ce4fc09736d69700b5869e0de6033dffc4c1b5a0a9c6c38a78b504e4c`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 题面要求的路线名已原样保留，steps/organism_profiles/traits/evidence_registry 等主要模块均有实质内容，15项性状全部出现，工程结构完整。主要不足是：题面要求每一步给首选酶及EC，但四个step的enzyme.ec_number全部为null；gold主链含S04 3-sulfolactate exporter步骤，答案只有四个转化步骤，未单列该输出步骤。因此属于“主要模块均有涉及，但若干必要内容遗漏”的5–6档；因EC系统性缺失并缺一个必要步骤，档内取低分5。

<details><summary>V0.4理由与本行变化背景</summary>

四步化学主链齐备（每步底物/产物英文名+SMILES、一个酶、一个对应菌与 profile 引用），15 项性状全部填写，route_scope.chosen_route_name 原样填 &#x27;sulfoquinovose degradation VI&#x27;，未改选路线，模块对应清楚（7–8 档，取 8）。扣分点：四步 EC 全为 null（模板允许未知填 null，但题面要求首选酶及 EC）；gold S04 的 3-sulfolactate 外排步未单列为 step，仅在外排叙述与 downstream_continuation 提及，未越过题面终点。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：gold主链有S01–S05五个必答步骤，其中S04__BSY-r03670为3-sulfolactate exporter；答案未单列该步骤。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_146：gold各步有酶及EC记录（如2.7.1.184、1.2.1.97、4.1.2.57、5.3.1.31）；答案四步EC均为null，形成必要字段缺失。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_146：本题gold终点为(2S)-3-sulfolactate；答案化学终点一致，但输出步骤未覆盖。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案给出的化学主链为SQ异构化→6-sulfo-D-fructose→ATP依赖磷酸化→6-sulfo-D-fructose-1-phosphate→醛缩裂解生成DHAP与sulfolactaldehyde→NAD+依赖氧化生成3-sulfolactate。方向为降解方向，步骤连续，主碳骨架与硫载体到gold终点(2S)-3-sulfolactate一致；ATP/NAD+辅因子已列出，未见主链首步错误、方向反转或明显原子不守恒。局部问题主要是sulfolactaldehyde/3-sulfolactate立体化学未标注、S1产物以开链形式表达，以及与gold环状/立体表示存在差异；这些属于局部表达/立体问题，未推翻主链化学结论，故在7–8档取8。程序允许D2至8且9–10门未开，不取9。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与 gold reaction_gold 的 S05→S01→S03→S02 逐步一致：SQ 异构→ATP 依赖磷酸化→C3–C4 醛缩裂解（DHAP+sulfolactaldehyde）→NAD(P)+ 依赖醛氧化，方向全部正向，终点 (2S)-3-sulfolactate 与 gold terminal 一致，碳骨架与硫原子在列。局部缺陷：H+/H2O 与立体构型（(2S)）未标注、NAD(P)+ 写为 NAD+（集合内成员），按八.辅因子条款属局部计量/表达缺陷，在 7–8 档处理，不 cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：gold主链化学顺序为S05异构、S01磷酸化、S03醛缩、S02氧化生成(2S)-3-sulfolactate；答案S1–S4在化学转化顺序上对应，仅缺少S04 exporter输出步骤。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_146：gold终点为(2S)-3-sulfolactate；答案S4产物为3-sulfolactate，化学终点一致。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：gold S03醛缩产物包括glycerone phosphate(DHAP)与(2S)-3-sulfolactaldehyde；答案S3给出DHAP+sulfolactaldehyde，主产物对应。

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> Four chemical enzyme steps match accepted gold names at name/function level: sulfoquinovose isomerase, sulfofructose kinase, sulfofructosephosphate-type aldolase, and 3-sulfolactaldehyde dehydrogenase; EC is null throughout. However S04 3-sulfolactate exporter is a pre-defined KEY_TERMINAL step and is not delivered as a structured step with enzyme/microorganism, only mentioned in route_summary as secretion. D-KEY4 therefore caps D3a at ≤4; within the restricted range the four supported steps and the missing-key boundary are clear, so 4. This cap is not signed as key_error=Y.

<details><summary>V0.4理由与本行变化背景</summary>

四个酶名分别与 gold enzyme_gold 的 accepted names 对应：sulfoquinovose isomerase（5.3.1.31）、sulfofructokinase（2.7.1.184）、sulfofructose-1-phosphate aldolase（4.1.2.57）、3-sulfolactaldehyde dehydrogenase（1.2.1.97），功能类型与反应类型匹配；yihS/yihT 基因标注与文献一致，其余基因名候选均填 null。扣分点：EC 全为 null，无法按四.6 做具体 EC 核验（非错引，仅为未给号）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_146：Accepted enzyme names for S01/S02/S03/S05; supports name-level matching only, not protein-specific substrate/activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：Directed gold reactions and S04 exporter row; supports the key-terminal exporter distinction.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> Species-level E. coli is gold-supported for S05/S01/S03, but the answer uses strain K-12 MG1655 (TaxID 511145) for all steps and claims complete_pathway_organism_profile_id=ORG_001. Gold organism rows do not list E. coli for S02/S04, and PATHWAY_COMPLETE is only Alkalicoccus urumqiensis. The claim is not proven false because gold is non-exhaustive, but strain identity and whole-path capability are unverified, and the S02/S04 attribution lacks gold support. Fits 5-6 partial-support band; lower 5 because several key identity/capability items remain open.

<details><summary>V0.4理由与本行变化背景</summary>

全部四步归 E. coli K-12（单一 profile，符合&#x27;同一菌去重&#x27;要求）。gold organism_gold 在 S05（异构酶，BSY-e03761）、S01（激酶，BSY-e01498）、S03（醛缩酶，BSY-e02747）均列 Escherichia coli，支持 3/4 步归属；S02 脱氢酶步 gold 仅列 Bacillus aryabhattai/Pseudomonas putida/Alkalicoccus urumqiensis，答案的 E. coli 归属无切片支持但 gold 非穷尽、E. coli 磺酸糖酵解途径存在，故不判错、仅档内扣。菌株级 TaxID 511145 在 E0 无冻结记录（GAP-146-006/007），身份粒度为真实菌株级声称但未核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_146：Gold step organisms; E. coli appears for S05/S01/S03 but not S02/S04; PATHWAY_COMPLETE only Alkalicoccus urumqiensis.

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Key qualitative E. coli traits are supported at species level: oxygen tolerance/facultative prediction, motility, rod shape, Gram-negative, non-sporulating, non-halophilic and mesophilic. Numeric temperature/pH/salinity fields are partly pending or not scoreable in the frozen mask, and strain-specific ATCC/genome values lack E0 records. No observed trait is clearly contradicted. Main traits are verifiable; remaining issues are numerical/strain-level and unresolved, so 7 lower good band.

<details><summary>V0.4理由与本行变化背景</summary>

15 项性状全部填写。与 gold trait_gold 可核对者一致：F1 兼性厌氧、F10 运动性 true、F11 杆状、F12 革兰阴性（gram positive=false）、F13 不产孢、F4 非嗜盐（salinity preference=non-halophilic）、F7 糖类/甘油利用；F5 ATCC 700926、F14 NC_000913.3/4641652 bp/50.8% 为 MG1655 常见值但 E0 无冻结记录。差距项：F2 max 45 / min 10 与 gold observed 35–41 / 4–35、F3 min 4.4 与 gold 6.0–7.0 不同，但相应子字段在 trait_subfield_scoreability_mask 为 pending_teacher_adjudication 或 completeness_only，不能据此判错；F15 gold 为 UNKNOWN。按&#x27;主要性状可核实、少量数值问题&#x27;取 7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_146：Species-level E. coli traits: motility true, rod-shaped, Gram-positive false, sporulation false, salinity preference non-halophilic, temperature preference mesophilic; not strain-specific numeric validation.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_146：Marks F3 pH and F15 habitat generalism completeness-only/not scoreable and several F2/F4 endpoints pending teacher adjudication.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> The answer&#x27;s evidence_registry relies on EVID_001 and EVID_003 as INTERNAL_KNOWLEDGE_ONLY with no database/record/locator for route, enzymes, organism attribution, carbon-source and physiology claims. EVID_002 declares NCBI RefSeq NC_000913.3, but E0 has an explicit gap for that accession, so it remains UNRESOLVED_SOURCE rather than verified. Decision-relevant core groups are mostly MISSING_SOURCE; only one genome accession is even nominally locatable. This is 1-2 band; 2 because one database accession is at least named. No verified mis-citation, so no cap and key_error=N.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）来源全部为 INTERNAL_KNOWLEDGE_ONLY（EVID_001/EVID_003），按四.3 即 MISSING_SOURCE：无任何可定位文献/数据库条目与路径、酶、菌结论对应；仅 CG17 给出 NCBI RefSeq/NC_000913.3 条目级指针（EVID_002 DATABASE_DIRECT），但 E0 无冻结记录（GAP-146-001），核不了→UNRESOLVED_SOURCE。无经核实错引、无虚构引用，MISSING_SOURCE 默认不 cap，按低分档取 2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / dcce8b3ce4fc09736d69700b5869e0de6033dffc4c1b5a0a9c6c38a78b504e4c：Answer&#x27;s own evidence_registry and per-trait evidence_id fields; used to judge delivered source locatability, not to verify external facts.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> The answer distinguishes INTERNAL_KNOWLEDGE_ONLY from DATABASE_DIRECT in evidence_registry, uses null for EC and uncertain genes, and lists specific uncertainties about route-number VI, EC, gene assignments, stereochemistry, exporter/terminal continuation, ATCC/TaxID and trait values. However several traits are still given high confidence on internal knowledge, and route completeness/exporter boundary is not fully disclosed as a step gap. Most major limitations are labeled, with some overconfidence and incompleteness, so 7 lower good band rather than 8-10.

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据相称：所有 EC 无法核实时填 null 未臆造号，基因名候选（yihR/yihP）明确标不确定，主动披露 &#x27;I–VI 变体映射无法外部核实&#x27;、立体构型未核、性状数值为内部知识/近似典型值、外排与跨种互养不属主链等。扣分点：多项仅 INTERNAL_KNOWLEDGE_ONLY 的性状仍标 confidence=high（F1/F10–F13），且 raw_text 全为 null 缺少原文可核层，属单点/局部过度确信而非系统性误导，档内扣。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / dcce8b3ce4fc09736d69700b5869e0de6033dffc4c1b5a0a9c6c38a78b504e4c：Answer&#x27;s uncertainty statements, evidence-type labels and confidence fields; used to judge disclosure quality, not external truth.

</details>

## DeepSeek

答案SHA256：`49e39e5109a1b1e445bd4181069d0a22c88ac642a391ee7af92f7bc0aa8613ee`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> Answer is complete as a JSON answer and covers steps, enzymes, one organism and 15 trait fields, but it substitutes a different sulfoquinovose route for the specified route VI: the gold route orders S05-&gt;S01-&gt;S03-&gt;S02-&gt;S04 and ends at 3-sulfolactate export, while the answer gives an S1-S6 SQ dehydrogenase/gluconate/dehydratase/aldolase/sulfolactate route. This is a task-route deviation, not merely a chemical imperfection. Within the task-deviation cap &#91;1,4&#93;, 3 reflects complete formatting but central route nonconformity.

<details><summary>V0.4理由与本行变化背景</summary>

结构完整（6步、每步酶+菌、15性状、证据registry），但交付化学路线与题面指定 sulfoquinovose degradation VI 完全不同：gold VI 为 SQ→6-deoxy-6-sulfo-D-fructose(异构酶5.3.1.31)→磺基果糖-1-P(激酶2.7.1.184)→磺基乳醛+DHAP(醛缩酶4.1.2.57)→磺基乳酸(脱氢酶1.2.1.97)→外排；答案为 sulfo-ED 型(SQ→磺基葡萄糖酸内酯→…)，且 route_scope.chosen_route_name 仍填 &#x27;sulfoquinovose degradation VI&#x27; 自称合规——属任务参数偏离/自称合规却交付不同路线，D1关键错误；模块齐全故档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：Gold main-chain ordering and terminal S04 export; supports that the answer sequence/terminal differs from route VI. Does not itself score D2 chemistry of the alternative chain.
- ANSWER_TEXT / steps：Shows the answer&#x27;s actual S1-S6 transformations and its route_summary claim to route VI.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分4 → V0.5新分6，变化+2。

新裁判理由：

> Evaluated independently of target route credit, the answer presents a chemically continuous sulfo-ED-like alternative chain: SQ oxidation to lactone, hydrolysis to gluconate, dehydration, KDSG-type aldol cleavage, sulfolactaldehyde oxidation, and sulfolactate desulfonation. The sequence is plausible and connected, but oxidation steps omit NAD(P)+/NAD(P)H, some intermediate naming/representation issues remain, and the chain continues beyond the specified terminal. Within the allowed chemical range &#91;1,6&#93;, 6 is the upper side for a largely coherent but materially non-target chain with local stoichiometric/representational gaps.

<details><summary>V0.4理由与本行变化背景</summary>

交付主链在化学上自洽(sulfo-ED：SQ→磺基葡萄糖酸内酯→磺基葡萄糖酸→KDSG→丙酮酸+磺基乳醛→磺基乳酸→丙酮酸+亚硫酸)，连接/方向/原子基本合理；但它不是题面指定路线 VI(起点为脱氢酶而非异构酶，异构酶/激酶/4.1.2.57 步骤缺失)，且未声明为替代路线→未声明地严重偏离指定路线、错误起始步，D2主链结论失效，cap≤4；因交付路线本身是真实且连贯的生化解途径，取cap档上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps：Shows the answer&#x27;s main-chain transformations and continuity.
- E0_EVIDENCE / f3e0:tp:EV146-08：Supports that EC 4.1.2.58 is associated with KDSG-type aldol cleavage to pyruvate and 3-sulfolactaldehyde; does not validate the whole answer route or all EC assignments.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> Target-enzyme credit is low. No target step is confirmed as S; four target steps remain alignment-unresolved, and the confirmed KEY terminal S04 (3-sulfolactate export) is not delivered. The answer&#x27;s S5 has the target S02 substrate/product names locally, but its EC 1.2.1.83 is not the accepted target EC 1.2.1.97 and the pair remains unresolved. Other EC/name pairs are contradicted by E0 records. The D-KEY4 confirmed KEY failure keeps D3a within &#91;1,4&#93;; 2 recognizes only limited local target-adjacent information, not wrong-route internal enzyme coherence.

<details><summary>V0.4理由与本行变化背景</summary>

6个酶中4个 EC 与官方 accepted name/reaction 明确错配：1.1.1.375 官方=L-2-hydroxycarboxylate dehydrogenase(非sulfoquinovose dehydrogenase)；4.2.1.155 官方=(methylthio)acryloyl-CoA hydratase(非6-sulfo-D-gluconate dehydratase)；1.2.1.83 官方=3-succinoylsemialdehyde-pyridine dehydrogenase(非3-sulfolactaldehyde dehydrogenase)；4.4.1.23 官方=2-hydroxypropyl-CoM lyase(非3-sulfolactate sulfolyase，官方近4.4.1.24)。仅4.1.2.58(KDSG aldolase)与3.1.1.17(gluconolactonase,泛底物)较符。多处酶-EC矛盾，核心步骤酶对应失效，D3a关键错误，档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：Gold target steps and S04 terminal export; shows the required target reaction order/terminal.
- E0_EVIDENCE / f3e0:tp:EV146-09：Official EC 1.2.1.83 is not 3-sulfolactaldehyde dehydrogenase; supports EC/name mismatch for answer S5, not all unresolved steps.
- E0_EVIDENCE / f3e0:tp:EV146-04：Official EC 1.1.1.375 is L-2-hydroxycarboxylate dehydrogenase, not sulfoquinovose dehydrogenase; supports mismatch for answer S1.
- E0_EVIDENCE / f3e0:tp:EV146-10：Official EC 4.4.1.23 is 2-hydroxypropyl-CoM lyase, not a 3-sulfolactate sulfolyase; supports mismatch for answer S6.
- ANSWER_TEXT / steps：Shows answer enzyme/EC assignments and substrate/product pairs.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The strain identity is supported: TaxID 226186 is B. thetaiotaomicron VPI-5482 and ATCC 29148 is its valid culture collection number. However, the answer assigns every step and complete-pathway capability to ORG_001 using only INTERNAL_KNOWLEDGE_ONLY evidence; E0 annotations keep CG08 step-organism attribution and CG09 complete-pathway capability UNRESOLVED. No verified contradiction exists, and gold is non-exhaustive, so this is a partial-support/overbroad-capability case rather than a verified key error. Band 5-6, score 5.

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份 B. thetaiotaomicron VPI-5482 (TaxID 226186) 经E0核实SUPPORTED(学名含VPI-5482、rank、lineage)，身份三件套正确；但&#x27;该菌执行本6步/独立完成整条路线&#x27;的反应级(CG08)与全路径(CG09)能力在E0为UNRESOLVED，答案把整条sulfo-ED路线归给单一菌而无步级证据。身份正确+作用范围/能力未核→5档。未核≠错误，不cap(UNRESOLVED)。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:226186：Supports B. thetaiotaomicron VPI-5482 identity/TaxID record; does not support step catalysis or complete pathway capability.
- E0_EVIDENCE / f3e0:tp:EV146-02：Supports formal name/strain and lineage; does not support degradation capability.
- E0_EVIDENCE / f3e0:tp:EV146-03：Supports ATCC 29148 as B. thetaiotaomicron VPI 5482; does not support sulfoquinovose degradation.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_146：Shows gold step organisms and full-pathway organism; gold is non-exhaustive and is not used to declare B. theta automatically wrong.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> All 15 trait fields are present; F5 ATCC 29148 and F14 accession NC_004663.1 are identity/accession facts supported by E0. Many other values are plausible standard B. theta traits, but the local trait snapshot has no official B. theta trait rows, and F2/F3/F4/F6/F7/F8/F9/F14 size-GC/F15 remain unverified. The answer also gives medium/high confidence without raw text. This fits partial applicability with key evidence gaps, band 5-6; score 5.

<details><summary>V0.4理由与本行变化背景</summary>

B. thetaiotaomicron 15项性状生物学上大体合理(F1专性厌氧、F10非运动、F11杆状、F12革兰阴性、F13不产孢)；F5 ATCC 29148 与 F14 NC_004663.1 经E0支持；F4_salinity 诚实填 null。但本轮该物种无 trait gold(item_gaps: NO_TRAIT_RECORD_IN_SNAPSHOT)，多数性状无据可核，且以medium/high confidence标注无来源；F9&#x27;sulfoquinovose dehydrogenase&#x27;随错误酶。部分性状合理且有少量支持、关键项证据不足→6。不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-03：Supports ATCC 29148 identity; does not support most trait values.
- E0_EVIDENCE / f3e0:accession:NC_004663.1：Supports accession record existence/status only; not genome size or GC values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_146：Shows local trait scoreability for other organisms; does not provide verified B. thetaiotaomicron trait values.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分3 → V0.5新分1，变化-2。

新裁判理由：

> The evidence_registry contains only EVID_001 and EVID_002, both INTERNAL_KNOWLEDGE_ONLY with null database, null record_id and null locator. No locatable literature, database entry or computational record is delivered for the route, enzyme/EC, organism or traits. This is MISSING_SOURCE behavior and falls in the low D5 band. There is no verified mis-citation, so no D5 cap or key_error is asserted.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 仅 EVID_001/EVID_002，均 INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator 全null→MISSING_SOURCE(P34)。答案未交付可定位文献/数据库/计算记录；身份/ATCC/基因组虽可由E0核实，但属评价者核验、不回填为答案来源(P51)。EC官方错配为事实层CONTRADICTED，但答案未引用官方EC条目(来源指向内部知识)，按P40/OBS-D3A-D5不计已核实误引、不cap。全部缺失→低分档，取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：Shows only two internal-knowledge source entries with no locatable database/record/locator.
- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：Shows trait evidence_ids pointing to the same internal-only registry; no external locator is supplied.

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> The answer does distinguish some uncertainty with confidence values and labels both evidence entries as INTERNAL_KNOWLEDGE_ONLY, and it leaves salinity null. But uncertainties is empty, raw_text is null for most traits, and many unverified organism/physiological claims are presented with medium or high confidence without limitations. This is more than a single isolated overconfidence issue but not a systematic prediction-as-observation cap case. Band 3-4; score 4.

<details><summary>V0.4理由与本行变化背景</summary>

有confidence分级(部分low，如F3/F6)，但organism各步&#x27;high&#x27;、酶&#x27;medium&#x27;均基于INTERNAL_KNOWLEDGE_ONLY且无来源；uncertainties数组为空，未披露路线与gold不符、EC不确定等主要限制；结论强度高于依据。属多处过度确信、主要限制未说明(3-4档)，取4；仍有low标注与分区、未凭空把观测冒充，且非全程系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：Shows INTERNAL_KNOWLEDGE_ONLY source_type and medium confidence, providing some disclosure of evidence nature.
- ANSWER_TEXT / uncertainties：Shows the uncertainties array is empty despite many unverified claims.

</details>

## Kimi

答案SHA256：`3a38d647c60be92f0a55d038b1cc9d4506e0ce0ade141e21a5ecb2afbf27f890`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 答案覆盖4步并给出每步酶/菌及15项性状，但所交主链终点为2,3-dihydroxypropane-1-sulfonate而非题面路线VI的(2S)-3-sulfolactate，且缺S04 exporter等必要步，属任务路线/终点严重偏离；D1关键错误成立，按cap≤4取4（结构较完整但任务符合度受限）。

<details><summary>V0.4理由与本行变化背景</summary>

四个必需模块（主链、酶、微生物、性状）均实质交付：4步均含底物/产物英文名、首选酶与EC（S4按题面允许填null）、对应菌；路线名原样回显、氧条件如实null；15项性状一次返回且2项诚实null。扣分点：S1/S2/S3复用同一括号不闭合的SMILES（必需结构字段的工程缺陷，共4处）、ATP/ADP无SMILES、S4终点与题面路线在gold中的终点不一致（该化学/来源问题分别在D2、D5独立判定，此处不双计）。属7–8档（大部分完整、少量工程缺陷），档内取低。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_146：gold root=6-sulfo-beta-D-quinovose，terminal=(2S)-3-sulfolactate；仅支持任务终点事实，不评价替代化学自身质量。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：gold五步有向主链及S04磺基乳酸外排终点；不扩展到答案未声称内容。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 所答从6-sulfo-beta-D-quinovose经异构化、ATP磷酸化、醛缩裂解至3-sulfolactaldehyde，再还原为DHPS，步骤顺序与主有机物转化连续；但作为指定路线VI的替代化学，按C06上限≤6，且S4未列电子供体/辅因子、部分SMILES为开链表达，取6。

<details><summary>V0.4理由与本行变化背景</summary>

S1醛糖-酮糖异构化、S2 ATP依赖的1-磷酸化、S3逆羟醛裂解三步的方向、主产物与gold反应序列一致（gold S05→S01→S03），ATP/ADP作为辅因子已在列，未出现起始步错误、方向反转或原子明显不守恒。主要问题在末端：S4把3-sulfolactaldehyde还原为2,3-dihydroxypropane-1-sulfonate并止于此，而gold该路线的下一步是脱氢生成(2S)-3-sulfolactate（EC 1.2.1.97）并导出，答案为未被冻结证据核实的替代末端（EVID_002仅INTERNAL_KNOWLEDGE_ONLY），按四.5第3步登记为未证实，不自动判错亦不给高分；S4电子供体缺失虽已声明，仍属计量信息不完整；S1/S2/S3的SMILES不闭合使结构表达不可机读（工程性，已计入D1）。综合属5–6档（主干部分成立但关键转化/连接仍需修订），档内取低。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：gold的S01/S03等中间体可作部分转化对照；不证明替代还原终点或具体酶。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> S=0、F=1（S04 KEY terminal confirmed failure）、U=4；显式EC 5.3.1.34/2.7.1.106/4.1.2.55与官方accepted名称/反应不符，S1-S3功能未获目标支持；按D-KEY4在&#91;1,4&#93;内取2：核心目标推荐失效，仅少量局部信息（步骤类型/中间体名）有用。

<details><summary>V0.4理由与本行变化背景</summary>

三个核心步骤给出的EC编号经E0官方条目逐项比对均与其所称酶-反应不符：EC 5.3.1.34的accepted name为D-erythrulose 4-phosphate isomerase（D-erythrulose-4-phosphate=D-erythrose 4-phosphate），非sulfoquinovose异构酶（gold为5.3.1.31）；EC 2.7.1.106为glucose-1,6-bisphosphate synthase（3-phospho-D-glyceroyl phosphate+α-D-glucose 1-phosphate），非ATP依赖的sulfo-fructose激酶（gold为2.7.1.184）；EC 4.1.2.55为KDPG/KDGal醛缩酶，非6-sulfo-D-fructose-1-phosphate醛缩酶（gold为4.1.2.57）。这属“多处反应与酶不匹配、酶名与EC互相矛盾”，使该维主要结论（关键步骤的酶对应）失效。正向因素：反应类型（异构酶/激酶/醛缩酶）方向正确、gene_or_protein未编造、S4 EC诚实null。按关键错误cap≤4，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.34：官方EC 5.3.1.34为D-erythrulose 4-phosphate isomerase，不支持答案所写6-sulfo-D-quinovose isomerase。
- E0_EVIDENCE / f3e0:ec:2.7.1.106：官方EC 2.7.1.106为glucose-1,6-bisphosphate synthase，不支持答案所写6-sulfo-D-fructose kinase。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：官方EC 4.1.2.55为KDG aldolase，不支持答案所写6-sulfo-D-fructose-1-phosphate aldolase。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_146：gold accepted酶为2.7.1.184、1.2.1.97、4.1.2.57、5.3.1.31；仅支持accepted对应，不证明答案蛋白活性。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 所有步归属Bacteroides thetaiotaomicron VPI-5482；TaxID 226186/ATCC 29148身份可定位，但E0明确不支持降解能力，步级催化与完整路径能力均无适用证据；身份正确不豁免能力核验，故5（部分支持、关键能力待核）。

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份三件套核验成立：TaxID 226186官方学名含菌株词VPI-5482（rank=no rank）、ATCC 29148确为该菌株、NC_004663.1记录存在，无跨属/异菌株错配，故不触发身份阶梯cap。不足在于能力层：4步全部归属同一菌且complete_pathway_organism_profile_id=ORG_001，隐含整条路径能力，但步级催化归属（E0标注ORGANISM_STEP_ROLE=L2 UNRESOLVED）与全路径能力（COMPLETE_PATHWAY_CAPABILITY_L3 UNRESOLVED）均无冻结证据支持；S4归属仅靠内部知识。属“身份有可靠支持、关键作用范围未充分核验”的5–6档，因身份要素全部核实取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:226186：仅支持TaxID 226186对应B. thetaiotaomicron VPI-5482身份；不支持任何降解能力。
- E0_EVIDENCE / f3e0:tp:EV146-03：支持ATCC 29148为B. thetaiotaomicron VPI-5482有效保藏号；不支持sulfoquinovose降解能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_146：gold步级菌为E. coli、Alkalicoccus、Bacillus、Pseudomonas、Clostridium；仅作对照，不证明答案菌能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 15项全部出现（13填值、2明确unknown），B. thetaiotaomicron/VPI-5482的F5 ATCC 29148、F12革兰氏阴性、F13不产孢等大体合理；但F1/F2/F14等多项无E0原始性状记录，F14数值仅有accession存在性，未达充分核验；按5-6档取6（部分准确适用但关键项证据不足）。

<details><summary>V0.4理由与本行变化背景</summary>

15项齐备、2项诚实null、单位与结构外壳规范；F5(ATCC 29148)与F14基因组登录号有可定位记录支持身份/存在性；F1/F10/F11/F12/F13等为B. thetaiotaomicron的常规性状，彼此自洽且未见与常识冲突的数值。不足：冻结快照对taxid 226186无任何性状记录（NO_TRAIT_RECORD_IN_SNAPSHOT，trait_scoreability_mask对全部性状为completeness_only），F2的optimum 37°C实际来自“常规培养温度”语境（非最适观测，答案preference已如实写为培养温度）、F7/F9把sulfoquinovose利用与磺基糖酵解酶活写入性状，实质承担目标污染物能力论证却无可核证据、F14的6,260,361 bp/42.8%GC未在冻结卡字段内。属“部分性状准确且适用、关键项证据不足”的5–6档，因无已核实数值错误、多项为物种级标准性状取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-03：仅支持ATCC 29148身份/保藏事实；不支持温度、氧、基因组数值或降解能力。
- E0_EVIDENCE / f3e0:accession:NC_004663.1：仅支持NC_004663.1存在及状态；不支持答案所填genome size/GC数值。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 决策相关组部分可定位：CG07身份TaxID/ATCC/RefSeq可核；但CG01/CG05/CG09主要依赖MetaCyc路线名（无record_id，GENERIC_SOURCE）和INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE），关键步骤/酶/能力链缺映射；无已核实错引，按5-6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组中出现条目级可定位可核对证据的有CG07（TaxID 226186、ATCC 29148）与CG17（NC_004663.1存在），且核验成立；但CORE的CG01/CG02/CG03/CG05/CG09只有无record_id的MetaCyc路线名（GENERIC）与INTERNAL_KNOWLEDGE_ONLY（MISSING），关键路径/酶/全路径能力结论无法沿条目追查，CG08步级归属亦为GENERIC+MISSING。答案未交付任何“存在但不支持结论”的可核实被引条目（EVID_001的record_id=null，路线名属自由文本，E0 gap GAP-146-004），故不登记已核实错引、不cap；三个EC与官方条目的矛盾按四.3/P40在事实层登记为CONTRADICTED并计入D3a，D5保持UNRESOLVED/ GENERIC来源状态。按四.3合成规则“决策相关组存在部分条目级可核对证据→5–6档”，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:226186：支持身份记录存在；不支持降解能力或步骤来源。
- E0_EVIDENCE / f3e0:tp:EV146-03：支持ATCC保藏事实；不支持路线/酶/性状来源。
- E0_EVIDENCE / f3e0:accession:NC_004663.1：支持核酸记录存在性；不支持所填genome数值。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案逐项列出氧条件未指定、MetaCyc无record_id、S4还原酶EC/电子供体不确定、ATP/ADP SMILES null等，区分confidence；但F1/F5/F12/F14等多项标high/medium且无原始摘录，部分强度超过依据；属单点/多点过度确信而非系统性误导，取6。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出了具体、非模板化的不确定性披露：题面氧条件null不改选路线、MetaCyc仅有路线名locator故EC置medium、S4还原酶EC/基因/电子供体未定（confidence=low）、核苷酸SMILES未填；未知性状用null+confidence=unknown，未把预测包装成观测，未掩盖已知矛盾。扣分点：F1“严格厌氧”、F12革兰阴性等仅凭INTERNAL_KNOWLEDGE_ONLY却标high（单点过度确信）；F2把ATCC保藏页当37°C的最适温度依据而未说明“培养温度≠最适”；末端由3-sulfolactate改为DHPS的偏离未作为替代路线/边界声明，使读者可能误以为该终点即题面路线终点。属单点过度确信+边界披露不足，非系统性误导，5–6档取6。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：列出答案自述不确定性；不证明相关性状已获外部核验。

</details>

## Qwen

答案SHA256：`f7b22338a952528e078e785a08d95eaee48e37b354fed2f8b21ca7613e4b54ec`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D1 1-2档：只交付了1步，目标主链要求5步，且15项性状全部为null；虽然路线名回显正确，但内容是一次水解脱硫到D-glucose与sulfite，不是题面指定路线的主链。存在可解析的步骤与profile，因此不取1，但核心完整性失败，取2。

<details><summary>V0.4理由与本行变化背景</summary>

题面指定路线名原样填写且notes声明不改动；但route_summary与steps&#91;0&#93;交付的是6-磺酸基-β-D-奎诺糖水解脱硫生成D-葡萄糖+亚硫酸盐的单步路线，与route VI的5步主链（异构酶→激酶→醛缩酶→脱氢酶→外排）不同，属自称合规却交付不同路线的任务参数偏离（P100），D1关键错误成立cap≤4；因仍有1步+酶名+菌+不确定性且格式可读，档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：冻结gold显示本题目标主链为S01-S05五步；不包含答案中的单步水解脱硫路径。
- ANSWER_TEXT / ANSWER：答案只含一个step，organism profile 的15项性状均为null。

</details>

### D2 反应化学科学性：1 / SCORED

V0.4旧分3 → V0.5新分1，变化-2。

新裁判理由：

> D2 1-2档：唯一反应把目标路线的入口异构化/磷酸化-醛缩酶-脱氢酶序列替换为水解脱硫生成D-glucose与sulfite，没有给出6-deoxy-6-sulfo-D-fructose、其1-磷酸、3-sulfolactaldehyde或3-sulfolactate等目标中间体，主链核心转化在第一步即偏离，无法构成题面指定路线的可信连续路径。取1。

<details><summary>V0.4理由与本行变化背景</summary>

答案主链仅一步：SQ+H2O→D-葡萄糖+亚硫酸盐，随后声明D-葡萄糖进入中心碳代谢，等于一步直达中心代谢物；route VI首步为sulfoquinovose isomerase(EC 5.3.1.31)生成6-deoxy-6-sulfo-D-fructose，其后经激酶/醛缩酶/脱氢酶至(2S)-3-sulfolactate。按合理替代路线四步判断：题面已指定路线（是）→未声明为替代路线（否）→无可核证据（EVID_001仅INTERNAL_KNOWLEDGE_ONLY）→偏离使主链化学与连续性结论失效，D2关键错误成立cap≤4；单步水解本身化学可辨，档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：gold显示目标路线S05入口为sulfoquinovose isomerase，S01为kinase，S03为aldolase，S02为dehydrogenase，S04为exporter；不支持答案的单步水解路径。
- ANSWER_TEXT / ANSWER：答案只给出一个水解步骤，没有目标中间体或连接关系。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> C04目标层：五个必答目标反应全部为ROUTE_BLOCKED_MISSING/REACTION_MISSING_OR_WRONG，答案未交付任何目标步骤的酶或EC。唯一酶sulfoquinovose sulfohydrolase没有EC，也不在accepted目标酶集合中，属于错误路线内容，不能获得目标信用。由于酶模块并非完全为空，按SCORED失败锚点评，不判整维MISSING；取1。

<details><summary>V0.4理由与本行变化背景</summary>

唯一酶名“sulfoquinovose sulfohydrolase”与其自称的“hydrolytic desulfonation”反应类型相容（水解酶切C–S键），名实不矛盾；但ec_number与gene_or_protein均为null，证据仅INTERNAL_KNOWLEDGE_ONLY，未提供可核的酶-反应对应，且非route VI所用的sulfoquinovose isomerase(EC 5.3.1.31)。属“有合理候选和部分支持、关键步骤缺具体核验”（5–6档），取5；无EC/酶名类别冲突，不构成D3a关键错误，引用问题归D5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_146：gold列出S01-S05的accepted目标酶；答案酶名不在其中。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：gold列出五步目标反应；答案未交付这些反应。
- ANSWER_TEXT / ANSWER：答案仅一个离路线的酶与步骤，且explicit EC为null。

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> D3b 3-4档：答案只给出Pseudomonas fluorescens，TaxID 294。物种级身份有E0支持，但该菌不是本题任何目标步骤的gold对应菌，且没有反应级证据支持其催化sulfoquinovose sulfohydrolase步骤或目标路线。身份本身可核，但作用范围/步骤归属不匹配，主要微生物推荐对目标主链不可用；取3。

<details><summary>V0.4理由与本行变化背景</summary>

Pseudomonas fluorescens 种级身份与TaxID 294经E0核验一致（名称-TaxID关联SUPPORTED），属真实物种、非无关类群、非异菌株错配；但答案以该菌承担该步催化并列为complete_pathway_organism_profile_id=ORG_001，步级能力与整条路径能力均无可核依据（仅INTERNAL_KNOWLEDGE_ONLY），E0对应claim为UNRESOLVED。属“有合理候选、关键身份作用范围未充分核验”（5–6档），取5，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：仅支持TaxID 294对应Pseudomonas fluorescens的物种级身份；不支持该菌的sulfoquinovose降解或所声称步骤能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_146：gold目标步骤的对应菌为E. coli、Alkalicoccus urumqiensis、Bacillus aryabhattai、Pseudomonas putida、Clostridium sp. MSTE9；不含P. fluorescens。
- ANSWER_TEXT / ANSWER：答案把P. fluorescens绑定到唯一一个离路线的步骤。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> D4按MISSING处理：任务要求15项性状，答案的ORG_001中15项性状全部为null，confidence均为unknown；没有可评价的性状数值或明确观测。按P44及C04，D4=MISSING=1，不宣称检测到科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

任务要求每个organism_profile一次返回全部15项性状及各项最强来源；答案organism_profiles&#91;0&#93;.traits的F1–F15全部value=null、raw_text=null、evidence_id=null、confidence=unknown，未交付任何性状数值或观测。按P44“全部必需性状均为null/空值→D4按MISSING记1分，不宣称检测到科学错误”；完成度不足另在D1反映，不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案中15项性状全部为空，支持MISSING判定。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_146：gold提供可核性状记录；本处只用于确认性状模块应有内容，不将未交付内容回填为答案证据。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> D5 1-2档：route/step/enzyme/microorganism的已交付声称只指向EVID_001，其source_type=INTERNAL_KNOWLEDGE_ONLY，database与record_id均为null，locator是自由文本短语，无法定位到可核对条目。按六状态属MISSING_SOURCE；这是缺失而非已核实错引，不触发错引cap。答案有低置信度标注，但无可追溯外部来源，取2。

<details><summary>V0.4理由与本行变化背景</summary>

答案唯一来源EVID_001的source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均无可用定位记录，claim_scope覆盖route/step/enzyme/microorganism；无任何可定位文献、数据库条目或计算记录。按四.3属MISSING_SOURCE（缺失而非误导），决策相关组（CG01/02/03/05/07/08/09）全部缺失→低分档，默认不触发cap；档内取2。评价者核验到的TaxID 294正向事实属事实核验层，不回填为答案交付来源。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案唯一证据条目为内部知识型，无数据库记录或可定位文献。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> D6 7-8档：答案把唯一证据标为INTERNAL_KNOWLEDGE_ONLY/low，酶与微生物confidence为low，EC、菌株与15项性状均填null/unknown，并明确说明EC、菌株与性状来源不足及SMILES仅为近似表达；没有把预测写成实验观测。轻微不足是route_summary对水解转化使用了较事实化的陈述，未显式标为推断。取7。

<details><summary>V0.4理由与本行变化背景</summary>

答案对未知处理诚实：EC、菌株号、15项性状均明确置null，全部confidence=low/unknown，uncertainties具体列出“EC/菌株证据不足”“SMILES为结构近似、未保证质子化与立体化学”，未把预测写成实证观测；主要限制已说明。唯一实质边界问题是把水解脱硫路线标注为route VI并声明“按题面指定路线填写”，未披露与route VI主链不同——属范围表述失实，但非系统性把预测当实证；综合披露质量档内取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案明确标注内部知识、低置信度、未知字段与SMILES近似性，支持D6证据性质披露判断。

</details>

## Grok

答案SHA256：`84aee6cc7b62b6a657e633e2a9aa8e0fffeb68655336f828dad3de5c9a96b611`。

### D1 完整性与任务符合度：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 1–2档：主链转化、每步酶/EC、对应微生物及15项性状等核心任务模块基本未交付；仅有一个底物和“unresolved product”占位，且明确拒绝填写VI路线。按D1完整性锚点取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_146：Shows the main chain, enzyme, microorganism, and traits are not delivered; does not support scientific correctness.
- QUESTION_TEXT / QUESTION_TEXT#BIOPATH150_146：Defines required deliverables only.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_146：Confirms a five-step linear task exists; does not make other branches required and does not establish answer correctness.

</details>

### D2 反应化学科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2按缺失处理：题面要求的主链反应未交付，答案只有底物和“unresolved product”，没有任何可评价的降解转化、方向、连续性或守恒内容；按MISSING=1，不宣称检测到具体化学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_146：Shows no degradative reaction sequence was delivered.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：Locates the frozen main-chain chemistry for comparison; does not support any answer-provided chemistry, because none was delivered.

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a按C04/P44与release contract处理：整个酶模块未交付，steps&#91;0&#93;.enzyme=null且全链无任何酶名或EC；按MISSING=1，U计数不转换为科学错误，也不给0/中分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_146：Shows the enzyme module is absent; does not support any enzyme function.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_146：Locates accepted enzyme records for the case; does not imply the answer delivered them.
- RUBRIC_CLAUSE / C04：Supplies the missing-module handling rule only.

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b按缺失处理：答案未给任何微生物身份、菌株、TaxID、保藏号或单步/整路能力声称，organism_profiles为空；按MISSING=1，不宣称检测到身份或能力错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_146：Shows no microorganism module was delivered.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_146：Locates reference organism rows; does not support any answer-provided organism because none was delivered.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4按缺失处理：organism_profiles为空，因而没有任何profile可承载任务要求的15项性状；按P44，全部必需性状未交付时D4=MISSING=1，不把缺失等同于编造或错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_146：Shows no organism profile or trait object was delivered.
- QUESTION_TEXT / QUESTION_TEXT#BIOPATH150_146：Defines required trait deliverable only.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 1–2档：evidence_registry为空，主链、酶、微生物和性状均无任何可定位来源或生成记录；没有可核对条目，MISSING_SOURCE默认不构成已核实错引，但可追溯性几乎为零，取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_146：Shows no delivered source records to trace; does not show fabricated citations.

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6高档：答案明确把路线VI、酶、微生物、性状和氧条件标为未知，拒绝编造；不确定性列表具体，并区分底物SMILES与途径其余代谢物是否解析。证据边界与置信表达一致；无正面结果不因诚实null自动扣D6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_146：Shows explicit uncertainty and non-fabrication statements; does not establish the underlying route facts.

</details>

## GPT5.6

答案SHA256：`c5626059f2dcafa9c2f2bb18d02ed7552166f06d266a5b9b16d243e4469155e3`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求给出指定路线主链、每步首选酶/EC、对应微生物，并填写15项性状及来源；答案仅交付3步路径，steps&#91;*&#93;.enzyme与microorganism全为null，organism_profiles为空，核心任务模块大部缺失。按D1 3–4档“仅覆盖少数必要模块”取3；因核心模块缺失构成D1关键错误，封顶≤4。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案仅3步，steps&#91;*&#93;.enzyme/microorganism为null，organism_profiles为空。
- QUESTION_TEXT / QUESTION_BEGIN：题面要求每步给出首选酶/EC、对应微生物及15项性状。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_146：该案gold为LINEAR_UNIQUE 5步主链；只用于完整性参照，不自动判替代路线错误。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出3步替代性推定路线：C1氧化为6-deoxy-6-sulfo-D-gluconate、脱水为2-keto-3-deoxy-6-sulfo-D-gluconate、醛缩裂解为pyruvate与sulfolactaldehyde；反应类型与连接大体自洽，但无证据支持，未形成到达题面指定终点(2S)-3-sulfolactate的连续主链，中间体命名与官方KDSG底物名称也不完全一致。按D2 3–4档“多个重要连接/终点仍需修订、合理性证据有限”取上沿4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_146：gold主链为S05→S01→S03→S02→S04；只作参照，不自动否定替代化学。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_146：gold终点为(2S)-3-sulfolactate。
- E0_EVIDENCE / f3e0:tp:EV146-08：EC 4.1.2.58产物侧与答案S3一致；官方底物名与答案中间体名不完全一致。

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 整个酶模块未交付：steps&#91;*&#93;.enzyme全为null，未给任何首选酶、EC或可辨认功能信息。按C04/P44记MISSING=1，不宣称检测到酶科学错误；D-KEY4不适用。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：steps&#91;*&#93;.enzyme均为null。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_146：gold每必答步有酶/EC记录；仅作参考，不替代答案缺失。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 微生物模块完全未交付：steps&#91;*&#93;.microorganism全为null，organism_profiles为空。按P44记MISSING=1，不宣称检测到微生物身份或能力错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：steps&#91;*&#93;.microorganism均为null，organism_profiles为空。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_146：gold含逐步微生物记录；仅作参考，不替代答案缺失。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 性状模块完全未交付：organism_profiles为空，未填写任何15项性状、单位/条件或来源。按P44记MISSING=1，不宣称检测到性状科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：organism_profiles为空，未填写任何性状。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_146：gold含可评分性状参照；仅作参考，不替代答案缺失。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry为空，所有reaction_evidence_id、enzyme.evidence_id、microorganism.evidence_id均为null；route_summary与steps没有可定位来源。属MISSING_SOURCE低分档（D5 1–2），无已核实错引，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示evidence_registry为空且各evidence_id为null。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确把route_summary标为“推定主链”，逐步uncertainty说明酶/EC/微生物未核实，organism_profiles留空，并列出缺少直接来源；未把预测写成观测，也未掩盖未知。扣分点：未给出更细的逐声称置信标签/证据类型，部分主链仍以“主链”口吻呈现，故取7–8档偏上8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案明确标注推定、未核实与未知。

</details>
