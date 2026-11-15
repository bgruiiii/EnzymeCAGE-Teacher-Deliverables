# BIOPATH150_120：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：sulfoquinovose degradation II

污染物：6-Sulfo-d-quinovose；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 56.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 49 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 65.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 69 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 53 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 24.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`cc36d2580bbd78045a10031b85d06699fbb7d44d1087be942c1997905ec40c4d`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 3-4档：答案有完整JSON、路径、酶、菌和15项性状，但目标主链五步中仅S3的3-sulfolactaldehyde dehydrogenase与gold S02终末醛脱氢在名称级可见；S01/S03/S04/S05缺失或不对应，主要必需步骤大部未交付，取3。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖登记：路径4步（每步有主底物/产物英文名与SMILES）、逐步酶与微生物、单一菌株profile含15项性状、3条来源、不确定性段齐全，模块交付形式接近完整。但题面明文规定 chosen_route_name 必须原样填写 given 路线且不得改选其他路线；答案回填正确路线名，交付的主链却是异构酶—醛缩酶型变体（SQ→6-磺酸基-D-果糖→DHAP+3-磺酸基乳醛），与gold该路线入口 sulfoquinovose 1-dehydrogenase（EC 1.1.1.390，SQ+NAD+→6-脱氧-6-磺酸基-D-葡萄糖酸-1,5-内酯）不同。属“自称合规却交付不同化学路线”的任务参数偏离，按P100归D1关键错误，cap≤4；其余模块形式完整，档内取4。披露不构成免扣。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：列出gold S01-S05五步反应、方向与终末产物；不支持答案异构酶主链为完整目标链。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：列出gold S01-S05所需酶与EC；仅S02与答案S3有名称级醛脱氢酶对应。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分4 → V0.5新分8，变化+4。

新裁判理由：

> 7-8档：答案自身S1异构化→S2醛缩裂解→S3 NAD+依赖醛氧化→S4 DHA磷酸化连续，方向降解、碳数/辅因子基本守恒，终末3-sulfolactate；9-10未给，因S3未标立体且替代路线非gold，取8。

<details><summary>V0.4理由与本行变化背景</summary>

交付链内部化学自洽：各步给出结构/连通性一致的SMILES（S2裂解6碳→DHAP+3-磺酸基乳醛，3+3守恒），S3写明NAD+/H2O与NADH辅因子，终点(S)-3-磺酸基乳酸与gold terminal（BSY-c15983）一致。但指定路线主链第一步应为SQ氧化脱氢（EC 1.1.1.390），答案首步改为异构化，其后以醛醇裂解替代gold的内酯水解（3.1.1.99）与脱水（4.2.1.162）步骤，gold主链三个关键中间体（6-脱氧-6-磺酸基-D-葡萄糖酸-1,5-内酯、6-脱氧-6-磺酸基葡萄糖酸、2-脱氢-3,6-二脱氧-6-磺酸基葡萄糖酸）全部缺失。替代变体未按四.5以“替代路线”明确声明并提供可核证据（所引Felux 2015为自由文本，冻结证据无对应记录=UNRESOLVED），第2、3步不满足，第4步偏离使本维“指定路线主链化学正确与连续”的主要结论失效。按四.5与八.D2“主链第一步即错”触发cap≤4；因化学自洽且终点化合物一致，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps.S1-S4：答案自身化学步骤，用于D2方向、连续性、碳数与辅因子评价。
- E0_EVIDENCE / f3e0:ec:5.3.1.31：支持EC 5.3.1.31的accepted name为sulfoquinovose isomerase及其β-sulfoquinovose↔6-deoxy-6-sulfo-D-fructose反应；不证明目标S01或P. putida SQ1全路径。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 本题N=5，gold主链为sulfo-ED型五步：S01 sulfoquinovose 1-dehydrogenase、S03 lactonase、S05 dehydratase、S04 aldolase、S02 3-sulfolactaldehyde dehydrogenase。答案给出的是以sulfoquinovose isomerase、sulfofructose aldolase、DHA kinase为主的另一路线；其S1/S2/S4不对应任何必答目标反应，S01/S03/S04/S05目标步未交付或未绑定。答案S3的酶名与accepted 3-sulfolactaldehyde dehydrogenase一致，但EC为null、立体未标且route_state=UNKNOWN，不能按C04-USER把未知立体/表示升级为已确认S，故该步保留U。于是已确认S=0，且四步目标反应缺失/未绑定；仅存末端酶名的局部可用信息，按C04/C05落入&#91;1,2&#93;，因存在该局部可用信息取2不取1。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名sulfoquinovose isomerase与EC 5.3.1.31经冻结证据核对：官方accepted name与reaction（β-sulfoquinovose = 6-deoxy-6-sulfo-D-fructose）与该步异构化一致（SUPPORTED）。S2（sulfofructose aldolase）、S3（3-sulfolactaldehyde dehydrogenase）给出真实可辨酶名但EC/基因填null，属诚实未知，不计错；S3反应类型（NAD+依赖醛氧化）与酶名一致。S4为通用中心代谢激酶推断步，EC 2.7.1.29 无冻结记录（EVIDENCE_GAP→UNRESOLVED），答案已标注推断且反应证据null。整体为合理候选与部分支持，但途径定义步（S2）与S4缺具体核验，落5–6档取6；无EC大类与反应类型矛盾、无家族相关性冒充具体催化，不判关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：gold必答酶为S01 sulfoquinovose 1-dehydrogenase EC1.1.1.390、S02 3-sulfolactaldehyde dehydrogenase EC1.2.1.97、S03 6-deoxy-6-sulfogluconolactonase EC3.1.1.99、S04 2-dehydro-3,6-dideoxy-6-sulfogluconate aldolase EC4.1.2.58、S05 6-deoxy-D-gluconate 6-sulfonate dehydratase EC4.2.1.162；答案仅S3酶名与S02一致。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：gold主链反应为S01/S03/S05/S04/S02，终点为(2S)-3-sulfolactate；答案S1/S2/S4的反应不是这些目标反应。
- ANSWER_TEXT / steps.S3：答案S3为3-sulfolactaldehyde + NAD+ + H2O -&gt; 3-sulfolactate + NADH，酶名3-sulfolactaldehyde dehydrogenase，ec_number=null，立体未标；可提供末端局部信息但不能确认精确目标匹配。
- ANSWER_TEXT / steps.S1-S2-S4：答案S1/S2/S4给出sulfoquinovose isomerase、sulfofructose aldolase、dihydroxyacetone kinase路线，不对应gold S01/S03/S04/S05目标反应。
- E0_EVIDENCE / f3e0:ec:5.3.1.31：EC 5.3.1.31为sulfoquinovose isomerase（β-sulfoquinovose -&gt; 6-deoxy-6-sulfo-D-fructose），不是gold S01的sulfoquinovose 1-dehydrogenase EC1.1.1.390；支持将答案S1视为非目标替代路线而非S01完成。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 7档：P. putida物种身份由TaxID 303支持；答案用菌株SQ1且TaxID 303为种级记录，菌株token未在记录名中出现，按P107粒度不足档内扣不cap；全路径能力未菌株级核实，保留待核。

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤归属单一菌 Pseudomonas putida SQ1，TaxID 303；E0分类记录学名Pseudomonas putida与TaxID 303精确匹配（SUPPORTED），且与gold各步匹配菌P. putida（TaxID 303）在物种层面一致。菌株标记“SQ1”不在冻结记录的names中（STRAIN_TOKEN_NOT_IN_RECORD_NAMES→UNRESOLVED），属D3b身份阶梯①“粒度不足”（物种级真实记录支持菌株级声称），档内扣、默认不cap。反应级归属（CG08）与全路径能力（CG09，complete_pathway_organism_profile_id=ORG_001）在E0均为UNRESOLVED，但答案未编造TaxID/基因组号、未跨类群错配、未由序列存在性外推整条路径；另答案明确声明菌株级性状无可靠记忆。综合落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持TaxID 303为Pseudomonas putida物种级记录；不证明菌株SQ1身份或SQ1全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_120：gold列P. putida为S01/S03/S04/S05及S02可接受菌之一，PATHWAY_COMPLETE指向P. putida；不证明答案异构酶路线。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 6档：形态、革兰氏、运动、产孢、氧/呼吸等多数与P. putida物种记录相容；但温度/pH/盐度端点、SQ1菌株特有F8/F9路径酶活/降解能力及F15多来自内部知识，F5/F14明确null，关键项证据不足/需修订，取6。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现（filled 13，explicit_unknown 2：F5、F14；omitted 0）。与gold观测一致项：F10运动性=true、F11杆状、F12革兰氏阴性（答案high置信）、F13不产芽孢、F4 category“非嗜盐”对应salinity preference=non-halophilic；F3 optimum 7.0与gold pH growth 7.0记录相容（该性状在评分掩码中为completeness_only）。F2给出中温偏好与30°C最适，与gold观测生长区间25–37°C相容，但min/max端点属pending_teacher_adjudication、optimum无观测源，为局部待核；F4 minimum为可评分子字段（gold=0）而答案填null，属完成度缺口（按P112主要归D1）；F5保藏号与F14基因组全null而gold有CCUG 49576与GCA_024508115.1，属诚实未知而非编造。全部物种典型值以low/medium置信并声明“菌株SQ1无专门报道，按物种典型值”，未把预测包装为观测、未把物种级数据写成菌株普遍性质、无数值离谱。关键项证据不足，落5–6档取6；无D4关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_120：提供P. putida物种级性状观测/预测背景；不证明菌株SQ1特有条目或答案异构酶路径。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_120：标明F2端点等子项待裁定、F3/F15等为completeness_only；不把不可评分端点当确定错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_120：逐子字段标明observed_accuracy或pending；用于避免对未冻结端点猜错。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 3-4档：答案有evidence_registry与claim_scope，但核心路线EVID_001仅有完整引文题名、无DOI/记录号/图表映射且E0为free-text gap；EVID_002为INTERNAL_KNOWLEDGE_ONLY，EVID_003无record_id。决策相关核心组多为UNRESOLVED/MISSING，无法核对支持范围；无已核实错引，不cap，取4。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组无任何已核实错引——E0仅对EC 5.3.1.31（酶名-EC精确匹配）与TaxID 303（学名精确匹配）给出SUPPORTED，与答案一致，无CONTRADICTED；故severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不cap。可追溯性本身偏弱：主链S1–S3仅一条无DOI/PMID的文献引文EVID_001，冻结快照无对应记录→UNRESOLVED_SOURCE；路线名来源EVID_003为无record_id的MetaCyc标签→GENERIC_SOURCE；全部性状与DHA激酶EC仅EVID_002 INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE；S4 reaction_evidence_id=null。仅达“部分关键结论可定位”而未获核对，落3–4档取4。“路线名与化学构成不一致”的引用-声称链嫌疑无法在冻结证据核实，登记UNRESOLVED（key_error=UNRESOLVED），不判虚构、不计已核实关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案实际交付的EVID_001文献题名、EVID_002内部知识、EVID_003 MetaCyc pathway名称；不把这些自报来源升级为已核实支持。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 7-8档：答案区分LITERATURE_DIRECT/INTERNAL_KNOWLEDGE_ONLY/DATABASE_DIRECT，标注low/medium/unknown，明确EC/基因/菌株性状/推断步骤和route ID不确定性；未系统性把预测当观测。因核心路线事实仍有未核与局部过强，取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据强度大体相称：uncertainties明确列出①路线编号构成不确定（若为其他变体则主链不同）②S2/S3的EC与基因未知③菌株级性状无可靠记忆、物种典型值以低置信标注④S4为连接中心代谢的推断步；各步uncertainty与confidence逐项标注（多为medium/low，F5/F14 unknown，F12 high且有gold观测支持）；alternative_branches两条均标is_part_of_scored_main_route=false，范围边界清晰；未把预测/推断写成实证观测，未掩盖已知矛盾。局部过强：部分基于INTERNAL_KNOWLEDGE_ONLY的性状仍标medium（如F1“严格好氧”、F6），且以medium置信把不可核文献支撑的S1–S3当作路线事实；属单点/局部过度确信而非系统性误导，档内扣，落7档；无D6关键错误。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案明确列出路线ID构成、EC/基因缺失、菌株性状缺失及推断步骤等不确定性。
- ANSWER_TEXT / ANSWER.evidence_registry：答案实际标注来源类型与置信度；不证明其科学真实性。

</details>

## DeepSeek

答案SHA256：`f7366a6c3ead70d8046e028bca3afdaacf993c765cab99fb8bae596d33011a07`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 输出为单个可解析JSON，route_scope.chosen_route_name原样填写sulfoquinovose degradation II，steps、organism_profiles、15项性状和evidence_registry均有交付；但主链未完整覆盖gold五个必答步：缺少6-deoxy-6-sulfogluconolactonase（S03）这一步，S1把6-Sulfo-d-quinovose直接写成开链6-Deoxy-6-sulfo-D-gluconate，同时在S5把3-sulfolactate继续裂解为pyruvate+sulfite，越过gold终点(2S)-3-sulfolactate且未标为下游。大部分任务模块已涉及，但必要步骤遗漏与范围越界使D1只能落在5–6档，按问题较多取5。

<details><summary>V0.4理由与本行变化背景</summary>

路线名原样=sulfoquinovose degradation II；交付S1–S5连续主链（同一菌去重为单一ORG_001），每步有底物/产物(name+SMILES)+enzyme(EC)+microorganism；15项性状齐全但F2温度/F3 pH/F4盐度/F5保藏/F14基因组共5项为诚实null，trait_evidence_id多为null。属&#x27;大部分必要内容完整、关联清楚、仅少量遗漏&#x27;，性状完成度不足使取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_120：登记本题ordered_step_count=5且LINEAR_UNIQUE，支持本题有五个必答主链步；不等于要求所有旁支。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：gold反应顺序为S01→S03→S05→S04→S02，终产物为(2S)-3-sulfolactate；支持缺失S03 lactonase步骤和S5越出终点的判断。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：gold五个必答步的酶清单含S03 6-deoxy-6-sulfogluconolactonase EC 3.1.1.99；不证明答案所填EC或菌株。
- ANSWER_TEXT / S1：答案S1将6-Sulfo-d-quinovose直接转为6-Deoxy-6-sulfo-D-gluconate，未列glucono-1,5-lactone中间体。
- ANSWER_TEXT / S5：答案S5在3-Sulfolactate之后继续生成Pyruvate+Sulfite，越出gold终点且未标为downstream/alternative。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 有机主链方向为降解正向，S1氧化、S2脱水、S3醛缩裂解、S4氧化到3-sulfolactate大体连续，S1/S4未列NAD+/NADH按P103属局部计量缺陷，不单独cap；但S1产物写成开链gluconate，而gold首产物是6-deoxy-6-sulfo-D-glucono-1,5-lactone，缺S03 lactonase水解，属关键中间体/转化缺失；S3的3-sulfolactaldehyde与S4的3-sulfolactate未标(2S)立体；S5越出gold终点，不作为主链加分。主干部分成立但关键中间体和结构表达需实质修订，D2落5–6档，按问题较多取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold变换一致：S1 sulfoquinovose→gluconate(dehydrogenase)、S2 gluconate→2-dehydro-3,6-dideoxy-6-sulfo-gluconate(dehydratase)、S3→pyruvate+3-sulfolactaldehyde(aldolase)、S4→3-sulfolactate(dehydrogenase)，题面/gold终点(2S)-3-sulfolactate达成；方向与原子守恒无重大错误。局部：S1把dehydrogenase与lactonase合并（略去6-deoxy-6-sulfo-glucono-1,5-lactone中间体）；S5 sulfolyase超出gold终点（按P29不计）。属&#x27;主链及关键转化有充分依据、少量局部问题&#x27;→7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：gold S01主产物为6-deoxy-6-sulfo-D-glucono-1,5-lactone，S03为lactonase水解，S02终产物为(2S)-3-sulfolactate；支持关键中间体缺失与终点越界的判断。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：gold清单含S03 6-deoxy-6-sulfogluconolactonase EC 3.1.1.99；支持答案未交付该水解步。
- ANSWER_TEXT / S1：答案S1产物SMILES为开链6-Deoxy-6-sulfo-D-gluconate，未表达glucono-1,5-lactone。
- ANSWER_TEXT / S3：答案S3产物3-Sulfolactaldehyde的SMILES未标(2S)立体。
- ANSWER_TEXT / S4：答案S4产物3-Sulfolactate的SMILES未标(2S)立体。
- ANSWER_TEXT / S5：答案S5在3-Sulfolactate之后继续生成Pyruvate+Sulfite，属gold终点之外的下游延续。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> Automatic matching leaves all targets U, but judgeable key failures are present: gold S03 lactonase (EC 3.1.1.99) is absent, S01 product is the acid rather than the gold lactone, and S04 uses EC 4.1.2.55 whose official reaction is phospho-substrate rather than the sulfo-aldolase target. S02/S05 EC pairs remain unverified. Under D-KEY4 this caps D3a at 4; within &#91;1,4&#93;, few usable target correspondences and unclear usable/failed boundary support 3.

<details><summary>V0.4理由与本行变化背景</summary>

五步酶功能/反应类型均对位（dehydrogenase、dehydratase、aldolase、dehydrogenase、sulfolyase），但具体EC与gold accepted EC多处不一致：S1 1.1.1.365(gold 1.1.1.390)、S2 4.2.1.156(gold 4.2.1.162)、S4 1.2.1.89(gold 1.2.1.97)在E0无记录→UNRESOLVED；S3 EC 4.1.2.55的E0官方reaction为2-dehydro-3-deoxy-6-phospho-D-gluconate/galactonate裂解(phospho底物)，与答案sulfo-aldolase对应存在特异性不符；S5 4.4.1.19无记录。属&#x27;合理候选+部分支持、若干关键步骤缺具体核验&#x27;→5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：Gold S01 is sulfoquinovose 1-dehydrogenase EC 1.1.1.390; S03 is 6-deoxy-6-sulfogluconolactonase EC 3.1.1.99; S04 is EC 4.1.2.58.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：Gold S01 product is 6-deoxy-6-sulfo-D-glucono-1,5-lactone; S03 opens the lactone to 6-deoxy-6-sulfo-D-gluconate.
- E0_EVIDENCE / f3e0:ec:4.1.2.55：Official EC 4.1.2.55 reaction uses 2-dehydro-3-deoxy-6-phospho-D-gluconate/phosphogalactonate, not the sulfonated substrate claimed by the answer.

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> The species Pseudomonas putida matches the gold step rows and PATHWAY_COMPLETE. The answer uses one consistent organism profile for all steps and does not invent a conflicting TaxID. Strain SQ1 is not separately verified in the frozen slice, so 9-10 is blocked; within 7-8, mainly correct species-level identity and step association support 8.

<details><summary>V0.4理由与本行变化背景</summary>

微生物Pseudomonas putida与gold每步所赋物种一致（E0 taxid 303=Pseudomonas putida CURRENT；organism_gold五步均列P. putida），五步归属与complete_pathway=ORG_001在种级由gold pathway_complete=TRUE支持。主要不足：菌株SQ1身份/能力无记录(ncbi_taxid=null)，以种级数据用于菌株级声称，S5 sulfolyase能力未核。按八.D3b身份阶梯&#x27;粒度不足、记录真实&#x27;档内扣不cap→6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_120：Pseudomonas putida TaxID 303 is listed for the step reactions and PATHWAY_COMPLETE=TRUE; this does not independently verify strain SQ1.
- E0_EVIDENCE / f3e0:taxid:303：Official taxonomy record supports the species name Pseudomonas putida; not strain SQ1 identity.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> Several given traits align with P. putida species records: motility, rod shape, Gram-negative, non-sporulating. However F2/F3/F4/F5/F14 are null, leaving key quantitative and strain-identity traits absent, and F7/F8/F9/F15 are species-level/internal claims not verified as SQ1-specific. This is a 5-6 profile: partially accurate and applicable, with key evidence gaps; choose 6 because the filled morphology/physiology traits are largely consistent and nulls are honest rather than fabricated.

<details><summary>V0.4理由与本行变化背景</summary>

已填10项中F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating与trait_gold(taxid 303 OBSERVED)一致，F6 aerobic/O2与gold无硝酸盐呼吸一致，F1 &#x27;aerobic&#x27;与gold &#x27;aerotolerant&#x27;基本相符；F7 sulfoquinovose碳源/F8 sulfo-ED降解/F9 sulfo-ED酶活为SQ1菌株特异声称(无官方记录，UNRESOLVED)。关键项F2温度/F3 pH/F4盐度/F5保藏/F14基因组均null（诚实未知、缺证据），构成关键缺口。属&#x27;部分性状准确适用但关键项证据不足&#x27;→6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_120：Supports species-level motility, rod shape, Gram-negative, non-sporulating and other P. putida traits; does not verify SQ1-specific values.
- E0_EVIDENCE / f3e0:taxid:303：Supports species identity Pseudomonas putida only.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> Evidence_registry contains only INTERNAL_KNOWLEDGE_ONLY entries with database=null, record_id=null and generic locators. Decision-relevant claim groups therefore have MISSING_SOURCE; there is no locatable external record to verify. No external identifier is present to support a verified mis-citation, so no D5 cap applies. Within the 1-2 low band, choose 2 because internal claim scopes are at least mapped, but no locatable source is delivered.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry两条(EVID_001/EVID_002)source_type均INTERNAL_KNOWLEDGE_ONLY、database/record_id=null、locator仅为内部描述串；按四.3属MISSING_SOURCE，决策相关组(CG01/02/03/05/07等)全为MISSING_SOURCE→低分档；MISSING_SOURCE为缺失非误导，默认不cap。无经核实错引→severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。故给2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows only internal-knowledge declarations with no database/record locator; does not provide a locatable source.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer honestly sets several traits to null and lists two uncertainty statements, and labels its evidence as internal knowledge only. However it assigns medium confidence to unsupported EC/pathway claims and asserts complete_pathway_organism_profile_id without caveat. This is 5-6: some uncertainty disclosure but important confidence labels exceed the delivered evidence; choose 6 because nulls and source labels show partial calibration without systematic fabrication.

<details><summary>V0.4理由与本行变化背景</summary>

答案给出uncertainties两条（EC不确定、菌株性状非特异可能变化），未知性状诚实null且confidence=unknown，来源标INTERNAL_KNOWLEDGE_ONLY；但披露较笼统，多处step/性状用medium乃至high（如F12/F13 high）而依据仅为内部知识，未明确声明整条路径为模型内部知识需实验核验。属&#x27;有不确定性说明但过于笼统、部分强度超过依据&#x27;→6；非系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows partial uncertainty disclosure, including one EC uncertainty and strain-variation caveat; does not cover all unsupported claims.

</details>

## Kimi

答案SHA256：`19c2d355dff7573cfca297c961aa9e9cc7d0291d0d77e72bb476773a6362574c`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 路线名与氧条件原样处理，四步覆盖主链与微生物，15项性状字段全部出现并含明确unknown；但S01与S03被合并为净步，lactonase未单列，四步EC均为null，4项性状为null，属主要模块均涉及但若干必要内容遗漏或仅明确未知，5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

路径、酶、微生物、性状、来源、不确定性六模块均有实质交付：主链4步（底物/产物英文名+SMILES+酶名+对应菌）齐全，route_scope.chosen_route_name 原样回填，终点止于3-磺基乳酸，下游模块另列；扣分点：四步enzyme.ec_number全为null（题面要求“首选酶及EC”，虽允许未知填null）、15项性状仅11项有值（F3/F4/F5/F14为null），属少量完成度缺口而非模块缺失，故落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION:BIOPATH150_120：题面要求每步主底物/产物+酶/EC+微生物、15性状、路线名原样；不证明答案科学正确。
- ANSWER_TEXT / ANSWER:BIOPATH150_120：答案四步、15性状、来源与不确定性字段；用于完整性定位。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_120：gold ordered_step_count=5；仅作任务范围参考，不把全图旁支当评分分母。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分9 → V0.5新分7，变化-2。

新裁判理由：

> 主链净化学方向正确：S1+S03净氧化/内酯开环至葡萄糖酸，S2脱水至KDSG，S3醛缩生成丙酮酸与3-磺基乳醛，S4氧化至3-磺基乳酸；与gold主链一致。扣分点为S01以净反应合并lactonase、辅因子未列入底物/产物数组、3-磺基乳醛/乳酸立体未指定；属少量局部表示与计量问题，7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

四步化学与gold sulfo-ED主链逐步对应：S1 净脱氢（quinovose→6-deoxy-6-sulfo-gluconate，明确声明可能经1,5-内酯中间体、按净反应合并，对应gold S01+S03）；S2 脱水生成2-dehydro-3,6-dideoxy-6-sulfo-gluconate（gold S05）；S3 retro-aldol生成pyruvate+3-sulfolactaldehyde（gold S04，两个主产物均列）；S4 醛脱氢至3-sulfolactate（gold S02、即gold terminal）。方向、碳骨架与原子收支成立，终点合规，下游3-磺基丙酮酸模块另列并声明不属于评分主链。局部问题：立体化学（(2S)）未标注（答案自注未确认）、辅因子仅文字注明NAD+依赖而未入反应物数组，属局部表达缺陷不改变主链结论；故9档而非10档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：gold S01-S05主链底物/产物/方向；用于化学连续性对照。
- ANSWER_TEXT / ANSWER:BIOPATH150_120：答案S1-S4的SMILES与reaction_type；用于化学判断。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 逐目标看：S01酶名sulfoquinovose 1-dehydrogenase、S02 3-sulfolactaldehyde dehydrogenase、S04 KDSG aldolase、S05 dehydratase均与accepted名称对应；S03 lactonase未单列，被并入S1净步，酶缺失；四步均无EC；S02/S04/S05产物有电荷/立体表示待核。多数主功能有适用支持，但存在MAJOR缺失与表示待核，按5–6档取6，不进入7–8。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶名与gold酶名逐条功能对应：S1 6-sulfo-D-quinovose 1-dehydrogenase（sulfoquinovose dehydrogenase）对应硫代奎诺糖1-脱氢酶；S2 6-deoxy-6-sulfo-D-gluconate dehydratase对应gold 4.2.1.162酶名；S3 2-dehydro-3,6-dideoxy-6-sulfo-D-gluconate aldolase与gold酶名逐字一致；S4 3-sulfolactaldehyde dehydrogenase对应gold 1.2.1.97酶名。未见酶名与反应类型矛盾，也未给出与反应类型不匹配的EC（EC全null，未触发EC错配）。因EC/蛋白标识全缺，功能、EC、身份三要素未齐，不足以进9–10档，落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：gold各步accepted酶名/EC；支持对照，不证明答案具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：gold各步反应方向/产物；用于目标反应对照。
- ANSWER_TEXT / ANSWER:BIOPATH150_120：答案S1-S4酶名/产物；用于逐目标判断。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 全部步骤指向Pseudomonas putida SQ1；物种名与gold organism_gold的P. putida（TaxID 303）一致，且gold PATHWAY_COMPLETE=TRUE；S02的gold也有P. putida可接受。SQ1菌株级身份在E0仅有物种级TaxID 303支持，strain token未核；全路径能力依赖EVID_001自由文本。身份/单步/全路径三层中物种层支持，菌株层局部待核，7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

核心微生物Pseudomonas putida与gold全部步骤菌一致，ncbi_taxid=303经E0核实学名匹配（物种级，SUPPORTED），且答案自注303为物种级、SQ1菌株级TaxID未知；但答案以“SQ1”菌株级身份承载步级归属与完整路径能力：E0仅有物种级taxid:303记录与另一菌株（mt-2 PaW1）的BacDive记录，strain token SQ1不在记录names中，属身份粒度不足（按P107档内扣、默认不cap，不因代表株差异判错）；complete_pathway_organism_profile_id=ORG_001的整路径能力声称在E0为UNRESOLVED（L3能力未核），但与gold PATHWAY_COMPLETE=P. putida方向一致，未见被核实的错误归属或跨类群错配。落5–6档之上、9–10档之下，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_120：gold各步P. putida及PATHWAY_COMPLETE=TRUE；不核验SQ1菌株token。
- E0_EVIDENCE / f3e0:taxid:303：官方TaxID303学名Pseudomonas putida；不支持菌株SQ1或全路径能力。
- ANSWER_TEXT / ANSWER:BIOPATH150_120：答案将全部步骤归P. putida SQ1并声称全路径；用于身份/能力声称定位。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 15项均出现，11项填写、4项明确unknown；F10 motility、F11 rod-shaped、F12 Gram-negative、F13 non-sporulation与trait_gold一致，F2偏好mesophilic一致。扣分点：F1“严格好氧”与gold aerotolerant记录不完全一致；F2 optimum_c=30来自培养温度且原文说非最适；F4/F5/F14等null降低适用性；F7-F9依赖未核全文。部分性状准确，但关键项证据或条件解释需修订，5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

已填11项性状：F10能运动、F11杆状、F12革兰氏阴性、F13不产孢与gold物种级观测记录一致（正向支持登记事实层，不回填来源）；F2 optimum 30°C自注为文献培养温度而非严格最适生长温度，处理符合P113（培养温度≠最适）；F1/F6/F15明确标注“物种层面/低置信”，未把物种级观测冒充菌株级定量观测；F7/F8/F9与gold路径/酶功能方向一致。扣分点：F1“严格好氧”与物种级记录aerotolerant=true存在术语张力且未提示；F2最适值无观测来源（trait_subfield_scoreability_mask记optimum为completeness_only）、pH/盐度端点待老师裁决；F3/F4/F5/F14缺失按P112主归D1不重复重扣。落7–8档取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_120：TaxID303物种级性状记录；不等同SQ1菌株级全部性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_120：性状可评分/待裁定子项；用于D4口径。
- ANSWER_TEXT / ANSWER:BIOPATH150_120：答案11项填写、4项明确unknown；用于性状核对。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 核心路线/酶/微生物声称有具体文献Felux 2015与MetaCyc pathway名可定位；但E0为自由文本gap，无法核对全文，登记UNRESOLVED_SOURCE。多项形态、氧需求、呼吸等性状使用INTERNAL_KNOWLEDGE_ONLY，登记MISSING_SOURCE。无已核实错引，不触发D5 cap。部分关键结论可定位、其他模块缺映射或来源，5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/02/03/05/09）来源为EVID_002“MetaCyc pathway: sulfoquinovose degradation II”（仅路线名、record_id=null）与EVID_001 Felux et al. PNAS 2015;112(31):E4298–E4305完整文献引用（record_id=null）：二者是可定位条目、非笼统库名，故不落GENERIC_SOURCE；但E0将其登记为自由文本缺口（GAP-120-011/013），无法机器核验其支持范围，故记UNRESOLVED_SOURCE。CG07的TaxID 303可核对（学名匹配SUPPORTED）。性状模块（CG10/11/12/13/15）多为EVID_003=INTERNAL_KNOWLEDGE_ONLY或null，记MISSING_SOURCE。无任何经核实错引（无VERIFIED_MIS_CITATION_*），不触发cap，severity=NOT_APPLICABLE。按“部分关键结论可定位并核对、其他模块仍缺映射”落5–6档；因性状模块整体缺可定位来源、核心文献在本快照不可核，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:BIOPATH150_120：答案evidence_registry与uncertainties；用于D5来源定位。
- E0_EVIDENCE / f3e0:taxid:303：官方TaxID303物种名；仅支持物种身份，不支持SQ1菌株或Felux全文。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> uncertainties明确列出EC未确认、菌株保藏/基因组/taxid粒度、内酯中间体、step4收录不确定、立体未定；confidence多数字段与来源相称，主要限制已披露。但F12 high用INTERNAL、F1/F6 medium等仍有一定过度确信。整体非系统性误导，7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界披露具体且与依据相称：四步EC一律null并逐条说明原因；明确声明ncbi_taxid 303为物种级、SQ1菌株级编号未知；声明S1可能经1,5-内酯中间体而按净反应合并；声明S4是否被sulfoquinovose degradation II原样收录存在不确定性并解释纳入依据；声明立体构型未确认；下游模块单列并标注不属于评分主链；性状置信度分级合理（internal knowledge标medium/low）。未发现把预测/推断系统性写成实证观测、也未掩盖已知矛盾。局部扣分：F1以medium给出“严格好氧”而未提示与物种级aerotolerant记录的张力，属单点过度确信（P119档内扣，不cap）。取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:BIOPATH150_120：答案uncertainties与各字段confidence；用于证据性质/边界判断。

</details>

## Qwen

答案SHA256：`6ca5730e5249ca66707b10020f27acfd6d9c56b5b84049e05d52fdb504bab773`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 主链5步、底物/产物、菌与15项性状均有给出；但5步EC全为null，首步内酯产物及S2底物SMILES缺失，若干性状为null。主要模块完整但若干必要字段遗漏，落在5–6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块均有实质涉及：路线名原样回显sulfoquinovose degradation II，5步主链每步给出底物/产物英文名、一个酶与一个菌，单一ORG_001按物种+菌株去重并被各步引用，15项性状外壳齐全（10填/5明确未知/0遗漏）。但题面明确要求“一个首选酶及EC”，五个酶ec_number与gene_or_protein全为null，属必要交付要素系统性缺项；两个内酯SMILES（S1产物、S2底物，同一化合物）为null。属“主要模块均有涉及，但若干必要内容遗漏”，落5–6档，取6（遗漏集中在EC与两个SMILES、非整体缺失）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION#BIOPATH150_120：任务要求每步给出主底物/主产物英文名及SMILES、一个首选酶及EC、一个对应微生物，并填写15项性状。
- ANSWER_TEXT / ANSWER#BIOPATH150_120：答案给出5步主链与15项性状，但EC全为null、部分SMILES为null，部分性状为null；仅支持完整性/符合度判断。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链方向与gold一致：S01氧化内酯化、S03内酯水解、S05脱水、S04醛缩裂解、S02氧化到(2S)-3-sulfolactate；答案顺序S1–S5与gold拓扑对应正确。缺少NAD(P)+/NADH/H2O/H+及部分SMILES未标立体化学，属局部计量/表达缺陷，不推翻主链，7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

5步化学与gold主链逐步吻合：①6-sulfo-D-quinovose氧化为6-deoxy-6-sulfo-D-glucono-1,5-内酯（对应BSY-r02371）；②内酯水解为6-deoxy-D-gluconate 6-sulfonate（BSY-r03447）；③脱水为2-dehydro-3,6-dideoxy-6-sulfogluconate（BSY-r03594）；④醛缩裂解生成pyruvate+(2S)-3-sulfolactaldehyde（BSY-r03484）；⑤氧化为(2S)-3-sulfolactate（BSY-r02478），终点与gold terminal一致。方向、顺序、主链连接均正确，已给SMILES与gold canonical/isosmiles一致。局部缺陷：五步均未列NAD+/NADH/H+/H2O等辅因子（P103属局部计量缺陷，不cap），内酯两处SMILES为null、部分中间体立体化学未注明。落7–8档，取8（主链与关键转化有充分依据）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：提供S01–S05各步方向、主底物/主产物与辅因子；不支持将答案的缺失EC或菌株能力视为已支持。
- ANSWER_TEXT / ANSWER#BIOPATH150_120：支持答案主链转化顺序与终产物声称；辅因子和立体化学缺失需在档内扣分。

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 五步酶名与accepted集合的功能方向逐一对应（sulfoquinovose dehydrogenase、lactonase、dehydratase、aldolase、sulfolactaldehyde dehydrogenase），但显式EC全缺，自动对齐未绑定且S01/S03为MISSING、S02/S04/S05为表示等价待裁；按功能判断主要对应可靠，仍不足以进9–10，7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

五个酶的功能名与gold酶名逐步语义对应：sulfoquinovose 1-dehydrogenase→“6-sulfo-D-quinovose dehydrogenase”；6-deoxy-6-sulfogluconolactonase→“…quinovonolactonase”；6-deoxy-D-gluconate 6-sulfonate dehydratase→“…gluconate dehydratase”；2-dehydro-3,6-dideoxy-6-sulfogluconate aldolase→“…aldolase”；3-sulfolactaldehyde dehydrogenase→“sulfolactaldehyde dehydrogenase”（与gold同名词）。未出现EC大类与反应类型相矛盾、酶名与EC互斥等关键错误。但EC编号与gene/protein五步全缺，来源仅为不可定位的通路名，故“若干关键步骤仍缺具体核验”，落5–6档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：提供各必答步accepted酶名与EC；支持功能级名称对应判断，不证明答案任意具体蛋白底物谱或实验活性。
- ANSWER_TEXT / ANSWER#BIOPATH150_120：答案给出五步酶名但未给EC；支持功能级比对并暴露显式EC缺失。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 所有步骤使用Pseudomonas putida SQ1；金标各步均含P. putida（TaxID 303，种级），种级步骤归属有支持。但TaxID 303为种级，strain SQ1与完整路径菌能力未由题内证据绑定；按身份阶梯为粒度不足/待确认，档内扣，取7。

<details><summary>V0.4理由与本行变化背景</summary>

五步统一推荐Pseudomonas putida（strain SQ1，ncbi_taxid=303），与gold organism_gold中S01–S05的物种级归属完全一致（P. putida为各步EXACT匹配菌，S02为三种可选菌之一，选P. putida不判错）。TaxID 303经E0核验为Pseudomonas putida（species rank、CURRENT），学名-编号关联成立。遗留问题：strain记号SQ1在冻结证据中无对应（f3e0:taxid:303为species级，bacdive:12880为mt-2 PaW1(pWWO)另一菌株），属“物种级记录支持菌株级声称”的粒度不足，按D3b身份阶梯①档内扣、默认不cap；未出现跨属/无关类群错配，也无由序列存在性直接推整条路径的实验性外推（路径能力另有物种级PATHWAY_COMPLETE支持）。落7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_120：支持各步P. putida物种级归属；PATHWAY_COMPLETE行仍为TaxID303种级，不支持SQ1菌株级身份或该菌株全路径能力。
- E0_EVIDENCE / f3e0:taxid:303：TaxID303官方记录为Pseudomonas putida种级；不支持菌株SQ1身份，也不支持完整路径能力。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> P. putida的motile、rod-shaped、Gram-negative、non-spore-forming与金标观察一致；F1/F6/F7–F9/F15多为内部知识或通路级推断，温度、pH、盐度、保藏、基因组等关键定量项为诚实null。主要已给性状可核，少量条件解释和关键缺口，落在7档。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全，10项填写、5项诚实null（F2温度/F3 pH/F4盐度/F5保藏/F14基因组），无编造痕迹。已给项中可核的定性性状全部与gold观测一致：F10 motility=motile（observed true）、F11 rod-shaped、F12 Gram-negative（gram positive=false）、F13 non-spore-forming（sporulation=false）；F6（aerobic respiration/O2）、F7（6-sulfo-D-quinovose）、F8（sulfoquinovose degradation）、F9（sulfoquinovose dehydrogenase activity）方向合理但仅有通路级/内部知识支撑；F1填“aerobic”而gold观测记录为aerotolerant=true，类目映射存在偏差风险；F15为泛化描述。关键定量性状（温度/pH/盐度/基因组）全缺，且已给项来源为INTERNAL_KNOWLEDGE_ONLY、无raw_text与record定位，属“关键项证据不足”，落5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_120：支持P. putida的motility、rod-shaped、Gram-negative、sporulation等观察，并提供温度/pH/盐度等参考；不支持将内部知识或通路级推断直接判为已观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_120：标明F2/F3/F4等子字段的可评分边界；支持区分诚实null与已给性状的适用性判断。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> EVID_001仅给MetaCyc通路名，无record_id/版本，属通路级/待核来源，但将路线、酶名和P. putida步骤归属关联到同一通路；EVID_002为INTERNAL_KNOWLEDGE_ONLY，一般性状无可定位来源；F7–F9部分靠EVID_001。部分关键结论可定位，其他模块缺映射，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付两条来源：EVID_001为DATABASE_DIRECT/MetaCyc，但record_id=null、locator仅为通路名“pathway: sulfoquinovose degradation II”，无条目ID、版本或段内定位，属GENERIC_SOURCE（且该自由文本引文在E0中登记为GAP-120-016不可解析为可查询标识符，故并记UNRESOLVED_SOURCE）；EVID_002为INTERNAL_KNOWLEDGE_ONLY，按P34属MISSING_SOURCE。决策相关组（CG01/CG02/CG03路线与CG05酶-EC）全部仅有笼统来源；但CG07侧交付了可定位可核对的编号TaxID 303，经E0核验学名一致（正向可定位支持登记于事实核验层），构成“决策相关组存在部分可定位可核对条目级证据”，按P35/P41进入5–6档，取5（多数核心结论仍缺映射）。无任何已核实错引（查不到≠虚构），不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_120：支持登记EVID_001为MetaCyc通路名且无record_id、EVID_002为INTERNAL_KNOWLEDGE_ONLY；不支持将这些记录核验为已定位条目。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案有逐步uncertainty、总体uncertainties及低/中confidence，明确EC/基因/蛋白、内酯环位置、辅因子、保藏号、基因组和内部知识等未知；主要限制披露较充分。但SQ1菌株完整路径能力未特别标注为待核，且部分低置信性状仍给出具体值，档内取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案区分了证据性质与未知：uncertainties列6条具体限制（氧条件未指定、EC与基因未确认、内酯环位置未确认、辅因子未列、菌株保藏/基因组/定量性状缺失、物种级性状来自内部知识且置信低），并在字段层用confidence=medium/low/unknown与evidence.source_type=DATABASE_DIRECT/INTERNAL_KNOWLEDGE_ONLY做了标注，未见“预测冒充观测”或掩盖矛盾。缺口：把complete_pathway_organism_profile_id直接指向ORG_001而未标明这是L3（完整路径能力）声称、且未提示菌株级身份未核；各步medium置信的通路归属只在uncertainties中笼统说明。属“大部分观测/预测/未知被正确标注，主要限制已说明”，落7档，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_120：支持答案对缺口、辅因子、EC、菌株保藏/基因组及内部知识低置信的披露；也显示SQ1全路径能力未单独标为待核。

</details>

## Grok

答案SHA256：`1bbc8e57abb28998c075759d77aaa2c8f6b8726d697b7fd776294f2f543459c2`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 覆盖5步主链、逐步底物/产物、菌与15项性状字段，交付结构完整；但每步均未提供EC，且来源与部分关键性状仅以内部知识或null承载，故在D1允许区间&#91;1,4&#93;取上沿。

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> sulfo-ED五步化学顺序、方向与主要产物总体连贯，终点( S )-3-磺基乳酸与gold一致；但S1入口底物SMILES与gold根结构存在明确立体冲突（route diagnosis: STEREO_CONFLICT_SPECIFIED），按显式立体冲突候选上限≤5，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_120：gold根与末端结构；用于核对S1立体表示及末端( S )-3-磺基乳酸，不自动扩展到其他未声称内容。

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 五个酶名与accepted集合在功能/名称层面基本对应：sulfoquinovose dehydrogenase、lactonase、dehydratase、aldolase、3-sulfolactaldehyde dehydrogenase；但所有步骤EC均null，且S1目标反应有立体冲突，9–10证据门不成立，故在&#91;1,8&#93;内取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：gold列出各步接受酶名/EC；仅支持功能级酶-反应对应，不证明具体蛋白底物谱或实验活性。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 各步均对应Pseudomonas putida，物种与gold STEP行一致，PATHWAY_COMPLETE行也支持P. putida完成该路线；但答案使用菌株SQ1并以物种级TaxID 303承载菌株身份，属物种级记录支持菌株级声称的粒度不足，按D3b身份阶梯档内扣、不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida物种级TaxID 303；不支持菌株SQ1的独立菌株级身份。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_120：gold在全部STEP行列出Pseudomonas putida，并有PATHWAY_COMPLETE行；支持物种级路线能力，不替代菌株SQ1级验证。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已给性状中杆状、革兰氏阴性、不产芽孢与gold物种级观测一致；F7/F8/F9与路线/酶功能方向相符；但F1写作“专性好氧”而gold F1观测为aerotolerant，且F6/F7/F9多为internal knowledge或物种级外推，多个关键环境性状为null，故取5–6档的6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_120：gold物种级性状记录支持杆状、Gram阴性、不产芽孢，并给出aerotolerant等观测；不支持将物种级记录自动扩展为SQ1菌株级实测。

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 关键结论主要依赖EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY记录；EVID_001给出Felux et al. 2015标题但自述未重新检索，EVID_002为物种共识。无条目级数据库记录或可核生成记录；无已核实错引，故不cap，按3–4档取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅核对TaxID 303为P. putida物种级；不证明答案来源交付充分，也不支持SQ1菌株级记录。
- E0_EVIDENCE / f3e0:bacdive:12880：BacDive 12880为P. putida mt-2 PaW1/pWWO菌株记录，不是SQ1；不能回填SQ1身份或性状。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> uncertainties明确列出EC/基因null、TaxID为物种级、SQ1性状缺精确记录、SMILES未逐条核对等限制，证据类型总体标注为internal/medium；但F7/F8等以high confidence承载未外部核验的路径能力，存在局部过度确信，故取7。

## GPT5.6

答案SHA256：`51017e537846fcab70a63f95e72e2998de09cf3ad1845b28dfc82fe2e7b620ae`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Only two of five required main-chain steps are delivered. The answer echoes the route name but substitutes an alternative isomerase/aldolase two-step route for the specified sulfoquinovose degradation II chain; S03-S05 are absent, one organism is reused, and all 15 traits are null. This is the 1-2 band: most necessary content missing and severe task deviation; 2 is given only for identifiable JSON and partial pathway material.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：Establishes the specified five-step S01-S05 main chain and terminal product; does not establish that the answer&#x27;s alternative route is experimentally impossible.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_120：Establishes ordered_step_count=5 and LINEAR_UNIQUE for the specified route; not a requirement that every gold DAG branch be delivered.

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The two delivered transformations are internally connected and chemically plausible for an alternative sulfo-ED-type route, but the specified route begins with sulfoquinovose 1-dehydrogenase to the lactone, not isomerization to 6-deoxy-6-sulfo-D-fructose, and the required terminal (2S)-3-sulfolactate is absent. D2 is held to the &#91;1,4&#93; range by route/direction substitution; 3 reflects local plausibility but a major mismatch and incompleteness.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_120：Shows the specified first step, intermediates, and terminal (2S)-3-sulfolactate; does not evaluate the alternative route&#x27;s own experimental validity.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Supports a real sulfoquinovose isomerase reaction to 6-deoxy-6-sulfo-D-fructose; does not support that reaction as the gold S01 dehydrogenase step or the specified route.

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> No required target enzyme-reaction pair is delivered. The answer gives sulfoquinovose isomerase and sulfofructose aldolase, which belong to an alternative route, while the accepted S01-S05 enzymes are absent; S03-S05 have no enzyme at all. With essentially no usable target catalytic correspondence, the &#91;1,2&#93; low band applies and 1 is selected.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_120：Lists the accepted enzyme names/EC for S01-S05; does not establish that no other enzyme can act on alternative substrates.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Supports the answer&#x27;s isomerase reaction as a local alternative-route function; does not support it as the required S01 accepted enzyme or give target credit.

</details>

### D3b 微生物身份与能力：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Escherichia coli K-12 substr. MG1655 and TaxID 511145 are offered for both steps and as the complete-pathway organism, but the frozen gold organism rows assign the specified route to Pseudomonas putida and other organisms, and no E0 record supports E. coli route capability. One organism is reused across all steps, and complete_pathway_organism_profile_id=ORG_001 exceeds the two-step support. This is the 3-4 band: multiple organism/capability mismatches and whole-path overreach, but not a verified unrelated-taxon fabrication.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_120：Shows gold step organisms and PATHWAY_COMPLETE for the specified route; not exhaustive proof that E. coli cannot use any alternative route.
- E0_EVIDENCE / f3e0:taxid:303：Supports Pseudomonas putida TaxID 303 identity; does not support E. coli K-12 or its route capability.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer returns all 15 trait slots but every value is null or null-subfield with confidence unknown and no evidence_id. Under the all-required-traits-null rule, D4 is MISSING=1 rather than a scientific-error score.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_120：Shows trait references exist for gold organisms; does not supply traits for the answer&#x27;s E. coli profile or fill the answer&#x27;s missing trait delivery.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All decision-relevant claim groups rely only on INTERNAL_KNOWLEDGE_ONLY evidence_registry entries with database, record_id, and locator null. There is no external source or traceable generation record for route, enzymes, organism, or traits. This is MISSING_SOURCE; no verified mis-citation is present. D5 1-2 applies because important conclusions are essentially not traceable; 1 is selected.

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Uncertainty disclosure is relatively specific: EC numbers are said to be unconfirmed, SMILES stereochemistry unconfirmed, oxygen unspecified, and strain-step mapping is marked low confidence; evidence entries consistently say INTERNAL_KNOWLEDGE_ONLY/low. However complete_pathway_organism_profile_id=ORG_001 is stated without an equally explicit caveat despite only two steps. This is not systemic prediction-as-observation; 7-8 band, 7 for the residual overclaim.
