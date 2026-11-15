# BIOPATH150_104：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：(S)-propane-1,2-diol degradation

污染物：S-1,2-Propanediol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 48 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 38.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 48 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 45.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 56.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 41.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`ede71ecedf4c6e8f080236f870a4d811d4276b60f7487255953ad6a268e0db43`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 答案原样回显路线名，但实际主链是(S)-1,2-丙二醇→(S)-乳醛→(S)-乳酸→丙酮酸的氧化路线，而不是冻结任务所要求的pdu/丙酸主链；格式和各模块基本齐全，但任务路线偏离属于D1关键错误，分数受≤4限制，档内取3。

<details><summary>V0.4理由与本行变化背景</summary>

模块结构性完整：3步路径+酶/EC+菌+15项性状+证据登记+不确定性说明，格式合规。但交付的化学主链（经FucO氧化至乳醛、乳酸、丙酮酸）与题面指定路线名&#x27;(S)-propane-1,2-diol degradation&#x27;在gold中对应的主链（S05 B12依赖丙二醇脱水酶→丙醛，再经丙酰-CoA→丙酸）在首步与终点均不同；答案将chosen_route_name原样填写并称&#x27;3步…均有酶学表征&#x27;，属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离，且答案自述路线解释为其最大不确定性，使遵守指定路线这一主要结论失效，按D1关键错误cap≤4取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_104：支持冻结题名与5步分支DAG的任务背景；不证明答案的氧化路线就是题面主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：支持冻结S05入口及S01-S04主链方向；不支持答案把pdu分支列为非评分替代路线。
- ANSWER_TEXT / ANSWER.route_scope/route_summary/steps：定位答案实际交付的氧化主链，用于与任务主链比较。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分4 → V0.5新分6，变化+2。

新裁判理由：

> D2按答案所答化学独立评价。三步醇→醛→酸→丙酮酸转化在化学上连贯，保留(S)构型，列有NAD+/NADH、H+与泛醌等辅因子，终点丙酮酸可进入中心代谢；但这不是冻结pdu/丙酸主链，属于化学可成立的替代路线，按可替代化学上限落在6分档，不能因路线内部自洽而更高。

<details><summary>V0.4理由与本行变化背景</summary>

答案主链首步为FucO(EC1.1.1.77)将(S)-1,2-丙二醇氧化为(S)-乳醛，与gold指定路线首步（B12依赖丙二醇脱水酶EC4.2.1.28将(S)-1,2-丙二醇脱水为丙醛）为不同转化；答案后续乳醛→乳酸→丙酮酸为主链自建途径。主链起始步即偏离该路线，且答案自述路线解释可能全错（&#x27;若数据源所指实为…pdu途径，则主链步骤将不同，此为本答案最大不确定性&#x27;），使D2主链化学连续性主要结论未确立，属主链起始步错误的D2关键错误，cap≤4取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.route_summary; ANSWER.steps S1-S3：定位答案三步氧化转化、辅因子与终点，用于D2化学连续性评价。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：提供冻结主链方向与终点的对照；不要求D2把替代路线回填为目标完成。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> D3a只计目标反应信用。答案主轴没有命中任一冻结必答步：S05关键入口应为B12依赖丙二醇脱水酶EC4.2.1.28生成propionaldehyde，答案主链S1却用FucO EC1.1.1.77生成(S)-乳醛；S01也被替换为乳醛脱氢酶，S02-S04未绑定。替代分支虽提到正确pdu酶，但被明确排除在评分主链外，仅形成有限局部信息；已确认KEY失败使其受≤4限制，档内取2。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶-反应配对在化学上自洽且酶名与EC不矛盾：FucO EC1.1.1.77（醇↔醛）、AldB EC1.2.1.22（醛→酸）、LldD EC1.1.2.3（乳酸→丙酮酸）。但全部证据为INTERNAL_KNOWLEDGE_ONLY，三个EC在冻结证据中均无记录（EVIDENCE_GAP），且这些酶并非指定路线的酶；属&#x27;有合理候选和部分支持但关键步骤缺具体核验&#x27;的第5档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_104：支持冻结S05 accepted酶为B12-dependent propanediol dehydratase EC4.2.1.28；不支持答案主链FucO用于S05。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：支持冻结S05入口反应为S-1,2-Propanediol→Propionaldehyde；不支持答案的lactaldehyde入口。
- ANSWER_TEXT / ANSWER.steps S1-S3; ANSWER.alternative_branches&#91;0&#93;：定位答案主链酶及被排除的pdu替代分支，用于区分主链目标信用与局部信息。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> E. coli K-12 MG1655作为候选微生物合理，所列FucO/AldB/LldD也与E. coli背景相容；但TaxID 511145在E0无冻结记录，且答案用同一菌株承担整条氧化路线并设置complete_pathway_organism_profile_id=ORG_001，而自身又承认外源(S)-1,2-丙二醇生长能力有限。身份可辨但菌株级身份与全路径能力仍支持不足，落在5分档。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份Escherichia coli（K-12 substr. MG1655，taxid 511145）名称本身正确，FucO/AldB/LldD确为大肠杆菌酶，步级酶-菌归属在单步层面成立；但以酶基因存在推断该菌经此途径降解(S)-1,2-丙二醇存在作用范围过度外推（答案亦承认该菌以丙二醇为唯一碳源生长能力有限），且taxid 511145在冻结证据中无记录（EVIDENCE_GAP），身份与作用范围未充分核验，取第5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_104：支持E. coli可作为部分冻结步骤的微生物记录，但PATHWAY_COMPLETE列表不含E. coli；不自动支持K-12 MG1655整路径能力。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;; ANSWER.uncertainties：定位答案的菌株身份、TaxID、整路径声明及对生长能力有限的自述。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 15项性状均已填写。多数定性性状与E. coli物种级冻结记录一致：兼性厌氧、革兰氏阴性、杆状、运动、不产孢，碳源/降解能力描述总体合理。温度上下限、pH、盐度等若干数值子字段在冻结mask中为pending或completeness_only，且答案指向K-12菌株而E0无该菌株记录；F14基因组记录也属未核。主要性状可用、局部数值/条件问题明确，档内取7。

<details><summary>V0.4理由与本行变化背景</summary>

E. coli K-12的15项性状多项与冻结记录一致：F1兼性厌氧、F10有运动性、F11杆状、F12革兰氏阴性、F13不产芽孢均与gold物种级(taxid 562)记录相符；F14基因组NC_000913/4641652 bp/50.8%GC与K-12 MG1655参考基因组吻合；F2/F3/F4数值在性状掩码中为待裁决/仅完整性（不入准确性分母），F5保藏号ATCC 700926与F9酶活为内部知识未核。主要性状可核实且适用，仅少量数值与未核条目，取第7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_104：提供E. coli物种级代表记录，支持兼性厌氧、革兰氏阴性、杆状、运动、不产孢等定性判断；不证明K-12菌株全部数值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_104：标明哪些性状子字段可评分或仅作完整性；温度/pH/盐度部分子字段非精确可评分。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_104：逐子字段标明pending/不可评分状态，用于避免把未核数值当作已证伪。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：定位全部15项性状值与confidence/evidence_id。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D5看实际交付来源。答案的路线、酶、菌和多数性状只登记为INTERNAL_KNOWLEDGE_ONLY，无record_id/locator，属于MISSING_SOURCE；F14虽给NCBI RefSeq NC_000913，但E0无该记录，登记为UNRESOLVED_SOURCE，不能判虚构。决策相关组以缺失来源为主，且无已核错引，故不cap但落1–2档；因有claim_scope/ID映射及一个具体数据库记录线索，取2。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/02/03/05/07/08/09）的路线、酶-EC、菌身份、路径能力等关键结论来源全部为INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；唯一DATABASE_DIRECT（NCBI RefSeq NC_000913, F14）在冻结证据中亦无记录，按UNRESOLVED_SOURCE待核；几无条目级可核对来源，按&#x27;全部缺失→低分档&#x27;取第3档。无已核实错引（不判虚构、不判CONTRADICTED），故不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：定位答案实际交付的证据登记、来源类型与claim_scope。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> D6披露质量较好：多数证据明确标为INTERNAL_KNOWLEDGE_ONLY，给出confidence，并具体列出pdu替代分支、FucO生理方向、LldD EC歧义、AldB注释未逐条核对等限制。残留问题是complete_pathway_organism_profile_id与“均有酶学表征”表述略强于证据，但整体是单点/局部过度确信而非系统性误导，落在7–8档，取8。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties逐条具体诚实：明确路线解释可能全错、FucO生理方向以还原为主且该菌生长能力有限、LldD EC歧义与醌池未细分、AldB底物谱与EC依据来源，并声明未凭记忆填写UniProt登录号以避免编造；各步confidence多为medium/low，INTERNAL_KNOWLEDGE_ONLY如实标注。证据性质与适用边界披露充分，仅主链仍以自建路线作为主链呈现稍显自信，取第8档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; ANSWER.evidence_registry：定位答案对证据性质、未知和限制的披露文本。

</details>

## DeepSeek

答案SHA256：`476228415ae648c7ea8025b008926824bd2c80f8e711e905216d7ff90c2c176c`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> JSON结构完整，3步均给出底物/产物、酶/EC、微生物，并有15项性状；但指定路线为(S)-propane-1,2-diol degradation的B12-dependent propanediol dehydratase主链，答案改走lactaldehyde/lactate/pyruvate氧化支路，未交付propionaldehyde、propanoyl-CoA、propionate/1-propanol等目标主链步骤。属指定路线严重偏离，D1关键错误cap≤4；在受限范围内因结构仍可读、模块有交付取3。

<details><summary>V0.4理由与本行变化背景</summary>

全部任务模块均有实质交付且结构完整（3步含底物/产物英文名与SMILES、每步酶名+EC+微生物、15项性状、evidence_registry），route_scope.chosen_route_name也按题面原样填写；但答案交付的化学主链（丙二醇→乳醛→乳酸→丙酮酸，fucO/aldA，EC 1.1.1.77/1.2.1.22/1.1.1.27）不是题面指定路线（gold BSY-p00755：丙二醇→丙醛→丙醇/丙酰CoA→丙酰磷酸→丙酸，EC 4.2.1.28等）的化学内容，属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离（P100/OBS-D1D2），构成D1关键错误，cap≤4；因模块完整、关联清楚，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：gold主链S05为S-1,2-Propanediol→Propionaldehyde，S01/S02等进入1-Propanol或propionate方向；不支持答案的lactaldehyde/lactate/pyruvate路线作为指定主链。
- ANSWER_TEXT / ANSWER.route_summary：答案自述路线为lactaldehyde/lactate/pyruvate，定位其与指定目标路线的偏离；不等同于目标路线酶学支持。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 仅按答案自身化学评价：S1 (S)-1,2-丙二醇氧化为(S)-乳醛，S2乳醛氧化为(S)-乳酸，S3乳酸氧化为丙酮酸，方向与连接连续，立体化学与氧化态变化基本合理。主要缺陷是NAD+/NADH、H2O等辅因子缺失，属局部计量/表达缺陷，按P103留在7–8档；无核心化学断裂，取8。

<details><summary>V0.4理由与本行变化背景</summary>

三步转化（醇→醛→酸→酮酸）方向一致、底物-产物衔接连续、碳骨架守恒；未列NAD+/NADH属简化，按八.辅因子条款通常为局部计量缺陷、不自动cap。丙二醇→乳醛的氧化方向是否为该酶生理方向、以及该路线是否在该菌株中实际运行，均无冻结核验（仅INTERNAL_KNOWLEDGE_ONLY），合理性证据有限，落5–6档取6。与gold不同不自动判错（P27）；路线偏离已归D1，本维仅评化学质量，不连坐。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：支持答案三步氧化路径的底物-产物连续性与方向；不支持其与指定gold主链的同一性。
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏通常按D2局部计量缺陷处理，不自动cap。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 目标酶-反应对应基本为零：gold S05要求B12-dependent propanediol dehydratase EC 4.2.1.28使(S)-1,2-丙二醇→propionaldehyde，答案S1却用EC 1.1.1.77→(S)-lactaldehyde；gold S01目标为propionaldehyde→1-propanol的alcohol dehydrogenase，答案S2用EC 1.2.1.22→(S)-lactate；S02–S04目标步缺失/未绑定。存在已确认KEY目标失败，D3a受限≤4；因无可用目标催化对应，取1。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名-EC-反应类型内部自洽（醇氧化1.1.1.x、醛氧化1.2.1.22、乳酸氧化1.1.1.27），fucO/aldA为合理候选基因；但三个EC均无冻结记录可核（GAP-104-007/010/019），第三步EC与E. coli常见L-乳酸脱氢酶编号是否一致亦未核，缺具体催化证据，落5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_104：gold S05酶为B12-dependent propanediol dehydratase EC 4.2.1.28；S01接受alcohol dehydrogenase类EC 1.1.1.1/1.1.1.347等；不支持答案的EC 1.1.1.77/1.2.1.22/1.1.1.27作为目标步对应。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：gold S05→propionaldehyde，S01→1-Propanol，S02–S04为propanoyl-CoA/propanoyl phosphate/propionate链；证明答案产物与目标反应不同。
- ANSWER_TEXT / ANSWER.steps.enzyme：定位答案实际交付的酶名/EC及产物；这些是替代路线内部数据，不自动获得目标步信用。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案统一使用Escherichia coli K-12 MG1655（TaxID 511145）并声明complete_pathway_organism_profile_id=ORG_001。E. coli是可合理候选，且gold organism_gold中E. coli出现于部分步；但TaxID 511145在E0无记录，gold PATHWAY_COMPLETE列表为Citrobacter/Klebsiella/Listeria/Salmonella，不含E. coli，答案对同一菌株完成全部三步/整条路径的能力仅有INTERNAL_KNOWLEDGE_ONLY。属有合理候选但关键身份与整路能力未充分核验，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

Escherichia coli K-12 MG1655为合理候选身份，菌名/菌株/TaxID 511145粒度自洽；但TaxID与各步酶归属均无冻结记录（GAP-104-026/027），complete_pathway_organism_profile_id=ORG_001的整条路径能力声称无全路径证据（仅内部知识）；无已核实身份编造或跨类群错配，故不cap，落5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_104：gold列出部分步可用E. coli物种级记录，并列出PATHWAY_COMPLETE为Citrobacter freundii/Klebsiella oxytoca/Listeria innocua/Salmonella enterica；不证明E. coli K-12 MG1655完成整条答案路线。
- ANSWER_TEXT / ANSWER.organism_profiles：定位答案对E. coli K-12 MG1655的菌株身份、TaxID与complete pathway声明；这些声明本身不等于已获外部支持。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 多项性状与E. coli物种级gold/可评分记录相符：F1 facultative anaerobe、F10 motility、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming、F2 mesophilic等；但关键应用性状证据不足：F7/F8声称可降解L-1,2-丙二醇等，gold E. coli F7/F8未给该目标底物能力；F14精确基因组值在E0无记录；F4/F5为null而gold有可观测项；F15 gold为UNKNOWN。部分准确但关键项证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

形态、革兰氏、产孢、运动性、兼性厌氧等性状与gold物种级观测记录一致（四.4允许同物种代表记录，物种级vs菌株级不据此判错）；温度/pH数值子字段多为pending adjudication或仅有培养记录、不能作为最适值核验；盐度与保藏号以null如实标注（完成度扣分归D1）；L-1,2-丙二醇降解能力声称缺证据。主要性状适用但关键项证据不足，落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_104：支持E. coli的motility、rod-shaped、Gram-negative、sporulation=false、温度偏好等；不支持答案关于L-1,2-丙二醇降解及K-12 MG1655精确基因组值的全部声称。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_104：标明E. coli若干性状/子字段的scoreable状态与completeness_only边界，防止把不可评分子字段当已核错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_104：标明温度/pH/盐度等子字段的pending或completeness_only状态，支持保守评分。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：定位答案15项性状的具体值与confidence；不把这些内部填写升级为已验证观测。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> evidence_registry五条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为空，仅用自建EVID_001–EVID_005互指，无法从外部条目、文献DOI或计算记录定位并核对关键路径、酶菌与性状声称。属MISSING_SOURCE低分档；缺失来源默认不cap，但当前可追溯性几乎不成立，取1。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：全部决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）仅有INTERNAL_KNOWLEDGE_ONLY自我声明，无数据库条目/文献/计算记录，无可定位可核对条目→MISSING_SOURCE，落低分档（P34/P41：全部缺失→低分档，默认不cap）。本题无已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION；取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示所有来源类型为INTERNAL_KNOWLEDGE_ONLY且无database/record_id/locator；只支持存在内部标签，不支持外部可定位来源。
- RUBRIC_CLAUSE / P34：MISSING_SOURCE或仅INTERNAL_KNOWLEDGE_ONLY归D5低分档，默认不触发关键错误cap。

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案对多项未核实内容给出medium/high confidence，尤其E. coli K-12 MG1655的精确基因组值、目标底物降解能力与完整路径能力；uncertainties为空，未说明内部知识边界、预测/推断与观测的区别，也未披露主要限制。并非全无置信度区分，但多处结论强度超过依据，属3–4档，取4。

<details><summary>V0.4理由与本行变化背景</summary>

答案把内部知识支撑的酶、菌株与性状（含基因组NC_000913.3、37°C最适、pH 7.0）以high/medium置信包装，uncertainties为空，未区分观测/预测/未知，主要限制未说明；但evidence_registry如实标注source_type=INTERNAL_KNOWLEDGE_ONLY，属部分披露、非明知掩盖，按多处过度确信档内扣，不cap，落3–4档取4。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：定位未核实性状仍标high/medium confidence；不支持这些值已由外部证据确认。
- ANSWER_TEXT / ANSWER.uncertainties：显示uncertainties为空，缺少对主要未知与边界条件的披露；不证明结论正确。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；多处过度确信但未证明系统性掩盖时按档内扣分处理。

</details>

## Kimi

答案SHA256：`5ef8d165b868b0874f86e89ae2ba6f619689df3f00c80d1b3b54dbb331ec4064`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> 题面锁定路线为 (S)-propane-1,2-diol degradation；gold 主链入口为 S-1,2-Propanediol → Propionaldehyde，终点主产物为 1-Propanol/Propionate。答案交付的是另一条 (S)-1,2-丙二醇→(S)-乳酸醛→(S)-乳酸氧化路线，未按锁定路线和终点交付。格式和模块可读，但核心任务路线明显偏离，D1按&#91;1,4&#93;取低档2。

<details><summary>V0.4理由与本行变化背景</summary>

题面明确要求route_scope.chosen_route_name原样填写且&#x27;不得改选其他路线&#x27;；答案虽原样回填路线名，但交付的是fucO/aldA两步氧化（(S)-propanediol→(S)-lactaldehyde→(S)-lactate），并经gold核验题面路线BSY-p00755的冻结化学主链为B12依赖丙二醇脱水酶(EC 4.2.1.28)生成丙醛、续至丙酰CoA/丙酰磷酸/丙酸（并有1-丙醇支路），属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离，按八.D1/P100归D1关键错误、cap≤4。其余完成度良好（两步字段齐全、单一organism_profile、15项性状全列、证据登记与不确定性说明在列），档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_104：gold route name and root/terminal compounds: root S-1,2-Propanediol, terminal 1-Propanol|Propionate; does not by itself prove alternative chemistry impossible.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：gold step sequence includes S05 entry propanediol-&gt;propionaldehyde and S01 propionaldehyde-&gt;1-propanol; supports target route/step expectation, not alternative-route chemistry.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案自身两步氧化在化学上可成立：S-1,2-丙二醇经末端醇氧化到 (S)-乳酸醛，再经醛氧化到 (S)-乳酸，方向与连接清晰，无原子明显不守恒；但未把 NAD+/NADH 作为主底物/产物列出（仅在 reaction_type 说明），且该主链不是题面锁定主链。按本题 D2 允许区间&#91;1,6&#93;取上沿6：主干化学合理，但辅因子/范围证据和任务兼容性仍有缺陷。

<details><summary>V0.4理由与本行变化背景</summary>

交付路线内部化学成立：两步均为NAD+依赖的醇→醛、醛→羧酸氧化，SMILES与氧化态一致（C&#91;C@@H&#93;(CO)O→C&#91;C@@H&#93;(C=O)O→C&#91;C@@H&#93;(C(=O)&#91;O-&#93;)O），方向正确、无跳步、无原子明显不守恒、未一步跳到中心代谢物；终点(S)-lactate为题面未指定终点下的自定边界且已声明，下游氧化为丙酮酸另列不计分，符合四.2/P29。但该路线非gold冻结主链，替代路线的可核证据仅有无record_id的EcoCyc locator（E0无法核对），且fucO生理方向偏还原，属&#x27;主干成立、合理性证据有限&#x27;的5–6档；无错误起始步/无依据跳步/未声明偏离，不触发D2关键错误（四.5第4步），档内取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 5ef8d165b868b0874f86e89ae2ba6f619689df3f00c80d1b3b54dbb331ec4064：quoted answer steps S1-S2, reaction_type and missing NAD+/NADH cofactor listing; does not verify experimental activity.

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分6 → V0.5新分1，变化-5。

新裁判理由：

> D3a只计目标反应酶信用。gold 入口步 S05 为 S-1,2-Propanediol→Propionaldehyde，accepted 为 B12-dependent propanediol dehydratase (EC 4.2.1.28)；S01 为 Propionaldehyde→1-Propanol（alcohol dehydrogenase 等）。答案 S1 用 FucO EC 1.1.1.77 生成 (S)-lactaldehyde，S2 用 AldA EC 1.2.1.22 生成 (S)-lactate，均非目标反应；S02-S04 也未绑定目标步。S=0，入口/终点存在已核目标失败，按D-KEY4上限和C05低档取1；错误路线内部酶自洽不获目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

两步酶-反应类别匹配且无自相矛盾：FucO（L-1,2-propanediol oxidoreductase/lactaldehyde reductase, EC 1.1.1.77, fucO）对应伯醇→醛的NAD(P)依赖氧化还原；AldA（lactaldehyde dehydrogenase, EC 1.2.1.22, aldA）对应醛→羧酸的NAD(P)+氧化。酶名、EC大类与反应类型一致，未出现&#x27;水解酶解释羟化&#x27;或&#x27;加氧酶配脱氢酶号&#x27;式矛盾，也未把广谱家族相关性直接写成具体催化证据（steps&#91;S1&#93;.uncertainty已披露FucO反向活性与AldA广谱背景）。但EC 1.1.1.77与1.2.1.22在E0均无冻结记录（GAP-104-008/011/014/018），accepted name/reaction/条目状态未核，来源仅EcoCyc无record_id locator，属&#x27;合理候选、部分支持、关键步骤缺具体核验&#x27;的5–6档，档内取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_104：accepted target enzyme names/ECs by step; S05 accepted B12-dependent propanediol dehydratase EC 4.2.1.28; S01 alcohol dehydrogenases; does not assess FucO/AldA as target credit.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：target S05 substrate/product S-1,2-Propanediol/Propionaldehyde and S01 Propionaldehyde/1-Propanol; not alternative lactaldehyde/lactate route.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 答案把 E. coli K-12 MG1655（TaxID 511145）作为两步共同菌并声明 complete_pathway_organism_profile_id=ORG_001。E. coli 身份本身合理，且 E. coli 在 gold 的部分目标步（S01/S03/S04）出现过；但 gold 的 PATHWAY_COMPLETE 行未列 E. coli，答案也没有给出该菌完成整条目标路径的独立能力证据；TaxID 511145 在 E0 无冻结记录。故身份候选合理但全路径能力/目标步对应未充分核验，D3b取5（5-6档：合理候选+部分支持，关键范围待核）。

<details><summary>V0.4理由与本行变化背景</summary>

推荐菌为Escherichia coli K-12 MG1655（TaxID 511145，organism_profile_id=ORG_001），与gold种级代表记录(Escherichia coli, taxid 562)同一物种谱系，未使用异菌株或无关类群编号，不构成八.D3b身份阶梯中的②③；步级归属两步同菌且org profile去重，未把单步菌写成整条路径菌；能力声称限于本答案两步反应级（fucO/aldA），未外推到未声称的下游。缺口：TaxID 511145、ATCC 700926与基因存在性在E0均无冻结记录（GAP-104-003/026/027），仅条目级定位未核，故落在&#x27;主要对应与身份有支持、少量具体条目待确认&#x27;的7档；fucO生理还原方向已在uncertainty披露，未伪装成单向降解证据。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_104：lists step organisms and PATHWAY_COMPLETE rows; E. coli appears at some step rows but is not in PATHWAY_COMPLETE rows; absence is not proof of inability.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 15项均填且多数基础性状与 E. coli 物种级 gold 一致：F1兼性厌氧、F10运动、F11杆状、F12革兰氏阴性、F13不产孢；F14的 NC_000913.3/4,641,652 bp/50.8% 与参考基因组常识一致。主要问题：F2把ATCC记录“37°C培养温度”写成 optimum_c=37，gold 只给温度范围/偏好，未给最适值；F5 ATCC 700926、F7/F9/F14 等关键项在E0无冻结记录，不能核实。按5-6档取6：部分性状准确且诚实null，但关键条件解释/若干数值证据不足。

<details><summary>V0.4理由与本行变化背景</summary>

按任务级关键性逐项看：与物种级代表记录一致的关键项有F1兼性厌氧、F10运动性、F11杆状、F12 Gram阴性、F13不产孢，F2偏好&#x27;嗜温&#x27;与gold mesophilic一致，F7/F8/F9的底物-能力描述限定在本人路线；F3 pH、F4盐度以null+unknown诚实标注，按规则只计完成度不判错。扣分项：把常规培养温度37°C回填进optimum_c并标high（培养温度≠最适，证据解释层明确禁止）；F6仅写有氧呼吸/oxygen而未提gold观测的硝酸盐还原-硝酸盐电子受体，属条件解释简化；F5 ATCC 700926与F14 4,641,652 bp/50.8%仅有条目级定位、E0无记录（GAP-104-003/029-031）。整体属&#x27;主要性状可核实且适用，少量数值/条件解释待修&#x27;的7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_104：E. coli species-level trait records: oxygen tolerance, motility, morphology, Gram, sporulation, temperature ranges/preference, etc.; species-level representative, not strain 511145-specific.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_104：E. coli temperature optimum_c has no observed scoreable source; max/min pending teacher adjudication; supports F2 optimum issue.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_104：E. coli F1/F10/F11/F12/F13 observed and scoreable at species level; F2 observed with pending subfields.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案提供了 EVID_001-EVID_004，并逐项挂到 steps/traits；但关键路线/酶-EC 的 EcoCyc 条目 record_id 为空（仅自由文本），BacDive 条目也无 record_id；ATCC 700926、TaxID 511145、EC 1.1.1.77/1.2.1.22 等在本案 E0 均无冻结记录，属于 UNRESOLVED_SOURCE，不能核实支持内容。没有经核实的错引，故不cap；按D5 5-6档取6：部分关键结论可定位到数据库/条目级线索，但核心路线与酶-EC、菌株身份仍未完成可核对映射。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记后：决策相关组（CG01/CG02/CG03/CG05/CG07/CG09为CORE；CG08/CG17与claim级的CG14为APPLICATION_CRITICAL）中，核心路线/酶-EC仅有无record_id的EcoCyc locator（GENERIC_SOURCE），身份与基因组虽有NC_000913.3、ATCC 700926、TaxID 511145等条目级定位，但E0无任何对应冻结记录（UNRESOLVED_SOURCE），无一组达到&#x27;条目级可定位且可核对&#x27;；同时无任何经核实错引（E0与答案声称无claim关联，GAP清单只记&#x27;无记录&#x27;），故不判虚构、不cap。SUPPORTING组的种级正向支持（CG10/CG15）不回填来源状态、不跨档上调。综合为&#x27;部分关键结论可定位、其他模块缺可核映射&#x27;的5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 5ef8d165b868b0874f86e89ae2ba6f619689df3f00c80d1b3b54dbb331ec4064：answer evidence_registry EVID_001-EVID_004 and per-claim evidence_id mapping; shows what was delivered, not whether cited records support claims.
- E0_EVIDENCE / f3e0:bacdive:12880：E0 slice contains only P. putida records; it does not contain the answer&#x27;s cited EcoCyc/ATCC/NCBI/BacDive E. coli records, so those remain UNRESOLVED.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案在 uncertainties 中明确氧条件未指定、说明选择氧化路线而非 Pdu 路线，并承认 FucO/AldA 可逆/广谱；F3/F4 等未知项诚实null。但多处把未有冻结核验的路线、ATCC 37°C、TaxID 511145 等标为 high confidence；F2把培养温度写成最适值；对整条替代路线与目标路线的差异披露不足。属部分披露但若干结论强度超过可核依据，D6取6，未达系统性误导cap。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露较具体：oxygen_condition=null的处理、&#x27;不改选Pdu路线&#x27;的路线边界、FucO可逆性与AldA广谱醛脱氢酶背景均写入route_scope.notes/uncertainty/uncertainties，未知项F3/F4以null+unknown标注，未把预测冒充观测，也未掩盖已知矛盾。扣分项：多处未核内容以DATABASE_DIRECT+high包装（EC 1.1.1.77/1.2.1.22、ATCC 700926、NC_000913.3/基因组数值），温度37°C由培养条件回填仍标high且未在raw_text外声明&#x27;非最适测定&#x27;；属单点过度确信而非系统性误导（同一路线断言多处复用仍按同一根本断言计），未达D6 cap条件，取6档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 5ef8d165b868b0874f86e89ae2ba6f619689df3f00c80d1b3b54dbb331ec4064：uncertainties array and confidence labels; shows disclosure and overconfidence, not external verification.

</details>

## Qwen

答案SHA256：`cbe4c2eed56748c50da3809dd825740b67e9d2b752a1caf5c4e1eea1c7b2d490`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 交付结构完整：路径2步、每步含底物/产物（名称+SMILES）、首选酶+EC、对应菌、单条profile含15项性状、evidence_registry与uncertainties齐备，JSON可解析。但题面锁定路线为(S)-propane-1,2-diol degradation，程序路线诊断已核DEVIATES：入口步S05为NONMATCH（答案给(S)-lactaldehyde，gold r01616产propionaldehyde，OUT_PROVEN_STRUCTURAL），S01为NONMATCH（答案lactaldehyde→lactate，gold r01612为propionaldehyde→1-propanol）；整链被替换为两步氧化到乳酸，且终点非gold终点1-Propanol|Propionate。按D1任务参数偏离属本维关键错误、候选≤4且base_range&#91;1,4&#93;：本维取3——模块齐备、表述清楚，但主链整体替换，可用部分与失效边界仅勉强可辨。

<details><summary>V0.4理由与本行变化背景</summary>

D1关键错误成立（任务参数偏离：回显路线名却交付不同化学路线），cap≤4；cap档内取4：路径/酶/菌/性状/来源/不确定性各模块均有涉及（性状10项填写、5项诚实null），但主链仅2步且止于非gold终点(S)-乳酸，相对gold五步分支链缺S05脱水酶步与S02–S04步。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：支持gold各步定向与结构：S05由(S)-propane-1,2-diol生成propionaldehyde、S01生成1-Propanol、S02生成propanoyl-CoA、S04生成propanoyl phosphate、S03生成Propionate；不支持答案的乳酸氧化路线，也不支持把该替代路线算作本题主链交付。
- SCOPE_ROW / SCOPE#BIOPATH150_104#CG14：仅证明题面污染物与路线范围已锁定为S-1,2-Propanediol/(S)-propane-1,2-diol degradation；不支持任何菌或酶的能力。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分4 → V0.5新分6，变化+2。

新裁判理由：

> 按答案所答化学自身质量独立评价：两步均为NAD+依赖氧化，方向一致、结构正确且衔接连续（C&#91;C@H&#93;(O)CO→C&#91;C@H&#93;(O)C=O→C&#91;C@H&#93;(O)C(=O)&#91;O-&#93;），(S)构型在两步间保持一致；辅因子在列（NAD+/NADH、H2O、H+），无原子明显不守恒（仅H+计量为简化，属局部小缺陷）；终点乳酸可经丙酮酸进入中心代谢，答案亦如此声明。缺点：该链是“化学可成立替换”而否题面指定路线，且仅2步、无来源支持。按C06“化学可成立替换≤6”与base_range&#91;1,6&#93;，取6：化学自洽清楚，但替换属性与证据薄弱阻止进入7以上。

<details><summary>V0.4理由与本行变化背景</summary>

D2关键错误成立（cap≤4），档内取4：所给两步自身氧化还原配平、连接连续（S1 CH3-CH(OH)-CH2OH→CH3-CH(OH)-CHO；S2→CH3-CH(OH)-COO−），但主链首步转化与指定路线不符（gold首步为B12依赖脱水生成丙醛），终点亦不同；按四.5第2/3步未通过（未声明替代、仅内部知识），第4步成立。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 按release d3a_fact_contract：N=5，S=0、F=2、M=0、U=3、H=0，C=0.0（原带C&lt;0.20→&#91;1,2&#93;），且两个已核KEY目标失败（S05入口、S01终点，proof已登记）触发D-KEY4≤4，故在受限&#91;1,4&#93;内取值。C05：无任何已核目标催化对应；两个KEY步为已核结构/转化不符（答案入口产(S)-lactaldehyde、终点产(S)-lactate，均非gold该步主产物），其余三步无对应交付且对齐未确认。答案仍给出可辨认酶名/EC与结构信息（局部可读），但错误路线内部酶自洽不获目标信用，故取2而非1；不足以进入3–4（无少数可用目标，失效/可用边界不可辨）。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档取5：S2醛氧化与EC 1.2.1.22名称-反应类型相符；S1醇氧化类型合理，但&#x27;propane-1,2-diol dehydrogenase&#x27;与EC 1.1.1.7的对应无冻结记录可核（GAP-104-001/002），gene/protein均null，缺具体催化证据；未出现经核实的EC大类/反应类型矛盾，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：支持S05/S01等步的底物-产物结构与定向（S05: (S)-propane-1,2-diol→propionaldehyde；S01: propionaldehyde→1-Propanol），据此判定答案所答转化异于该目标步；不评价具体酶活性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_104：支持各步accepted酶/EC集合（S05=4.2.1.28；S01=1.1.1.1|1.1.1.347等），用于名称-EC对照；不支持答案的1.1.1.7/1.2.1.22属于该步。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 身份层：答案给Pseudomonas putida、strain=null、TaxID 303；E0 f3e0:taxid:303学名精确匹配（物种级）→身份定位成立，且为物种级声称，无“物种级记录冒充菌株”的错配。反应级能力：两步酶在P. putida中的归属无任何对应粒度证据（E0 bacdive:12880为mt-2 PaW1菌株记录，support_scope明确不外推到步骤/底物归属）。整路能力：complete_pathway_organism_profile_id=ORG_001直接宣称该物种完成整链，无证据；gold PATHWAY_COMPLETE名单（546/571/1642/28901）不含P. putida，但gold非穷尽，不作为反证。身份对、能力两层均未核→5–6档下端取5（不因未核判错、不cap）。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档取5：物种身份Pseudomonas putida/TaxID 303经E0核验（种级学名一致，F3R1CLM-004335 SUPPORTED），但无菌株、无反应级或全路径能力证据；complete_pathway_organism_profile_id=ORG_001的全路径声称无支持；未出现经核实的身份错配或跨类群错误，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持TaxID 303的官方学名/rank/lineage与current状态（身份定位层）；不自动支持任何步骤归属或整路能力。
- E0_EVIDENCE / f3e0:bacdive:12880：仅支持P. putida mt-2 PaW1(pWWO)菌株的保藏号与26/30°C培养记录；其support_scope明确不外推底物/酶/整路能力，不能用于支持本答案的步骤归属。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_104：支持gold的步级归属与PATHWAY_COMPLETE名单及对应genome；gold非穷尽，名单缺失不构成对P. putida的能力反证。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项全部出现，5项（F2/F3/F4/F5/F14）为诚实null，未把未知填成数值；已给字符串性状（aerobic、aerobic respiration/O2、motile、rod、Gram-negative、non-spore-forming、F15生境描述）与两处底物/酶活性声称（F7/F8/F9）均以INTERNAL_KNOWLEDGE_ONLY+low标注，未出现预测冒充观测。但：trait_gold与trait_scoreability_mask对TaxID 303均无行，无可核观测可比；关键项F7/F8把物种级书写成可利用并降解目标污染物，属应用关键声称却无证据；亦未给出任何数值/单位条件。按D4“部分性状准确且适用、关键项证据不足”取5（既无已核数值错误，不落3–4；关键项未核阻止6以上）。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档取5：一般性状（好氧、运动、杆状、革兰阴性、不产孢）与物种级常识一致但来源仅INTERNAL_KNOWLEDGE_ONLY且E0未覆盖P. putida性状记录；F7/F8/F9关于目标污染物利用/降解/酶活的声称无支持并与未证实路线绑定；5项数值/条件性状诚实null（完成度扣分归D1，不在此重复重扣）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_104：该切片含4932/562/28901/132919/1773/285及PATHWAY_COMPLETE物种行，但无TaxID 303行；因此不能用于支持或否定P. putida的具体性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_104：仅给出上述物种的observed_accuracy/completeness_only划分，无303行，故D4无法做数值型比对。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 按claim group看决策相关组：CG01/CG02/CG03（路线）仅EVID_001=INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE；CG07/CG08/CG09（身份/步级归属/整路能力）亦仅内部知识→MISSING_SOURCE；CG05（酶-EC）给了ExplorEnz的EC 1.1.1.7/1.2.1.22记录ID，但E0无对应记录（GAP-104-001/002），且EC条目至多支持编号层而非本步归属→UNRESOLVED_SOURCE（未核≠错引）；CG14能力声称同样无来源。无VERIFIED_MIS_CITATION_*，不触发cap（MISSING/GENERIC默认不cap）。按P41：CORE组并非“条目级可定位可核对”，仅少量记录ID形式可定位→3–4档；因关键路线与菌归属全缺失，取3。

<details><summary>V0.4理由与本行变化背景</summary>

低分档取3：决策相关组CG01/CG02/CG03/CG07/CG08/CG09/CG14仅INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE），CG05的ExplorEnz EC条目因E0无冻结记录无法核对（UNRESOLVED_SOURCE）；无可核对条目级证据、无已核实错引，按四.3/八.D5不cap，取低分档上沿。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持身份学名（事实层），不构成答案自行交付的可追溯来源；不能回填D5来源状态。
- E0_EVIDENCE / f3e0:bacdive:12880：仅支持mt-2 PaW1菌株记录；答案未引用该记录，故不能算作原交付证据。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_104：支持gold登记酶/EC作为对照，说明答案的1.1.1.7/1.2.1.22不在该步accepted集合；不用于核对ExplorEnz记录内容。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 证据性质区分做得较实：answer以source_type明确区分INTERNAL_KNOWLEDGE_ONLY（EVID_001/004）与DATABASE_DIRECT（EVID_002/003），每步confidence=low/medium并写明“微生物与反应证据来自内部知识，置信度低”；氧条件未指定如实记录；多数缺失性状诚实null；uncertainties明列三项主要限制，未见把预测伪装成实验观测。唯一超出强度处：complete_pathway_organism_profile_id=ORG_001整路能力断言无任何证据或不确定标注（单点过强，非系统性误导）。按D6 7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档取6：答案标注内部知识来源与low置信度、明确氧条件未指定与证据缺口、未知性状填null，披露较具体；但把自推断路线表述为&#x27;按指定路线名称给出&#x27;而未披露其非指定路线/替代性质，complete_pathway能力声称未加边界，属局部过度确信而非系统性误导，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`d984c036e9c0b9ee4cc60cd5a4231a04df970afd810b38324bd0296d2dc53de1`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1落3–4档且任务偏离触发≤4。答案结构完整，给出了替代好氧氧化路线、酶、菌、15项性状和来源，但没有交付题面锁定的(S)-propane-1,2-diol降解主链：gold主链为5步B12依赖脱水至丙醛，并分向1-丙醇/丙酸；答案明说采用fucO/aldA/lldD路线、不采用钴胺素依赖脱水酶路线，仅3步，缺S02–S04及1-丙醇/丙酸分支。属P100“更换指定路线/自称合规却交付不同路线”的D1关键错误，核心任务符合度失效。因结构完整但仍严重偏离，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_104：gold路线名与终产物，用于核对题面锁定任务。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：gold主链各步方向与中间体；不是要求把全DAG所有旁支强行并成一条。
- QUESTION_TEXT / QUESTION_BIOPATH150_104：题面要求chosen_route_name原样填写且不得改选其他路线。
- ANSWER_TEXT / ANSWER.route_scope.notes；ANSWER.steps：答案明确选择好氧氧化路线而非pdu脱水路线，仅给出3步。

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2允许区间&#91;1,6&#93;；化学可成立替换≤6。所答三步(S)-propane-1,2-diol→(S)-lactaldehyde→(S)-lactate→pyruvate方向、连续性和主结构均合理，辅因子大体给出。局部问题是S3用ubiquinone而EC 1.1.2.3的IUBMB电子受体写细胞色素c，属电子受体/记录不一致，答案自己也披露。因这是对锁定路线的化学可成立替换而非目标主链，按C06封顶在6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：答案三步底物/产物SMILES、方向与辅因子；S1/S2连贯，S3含醌/细胞色素c局部不一致。
- RUBRIC_CLAUSE / C06：化学可成立替换≤6；D2不因路线偏离直接连坐D1，但替代路线不得回填目标完成。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a只计目标反应相应粒度的功能/accepted支持。本题N=5：S05入口脱水、S01丙醛→1-丙醇、S02丙醛→丙酰CoA、S03丙酰磷酸→丙酸、S04丙酰CoA→丙酰磷酸。答案S1把同一入口底物氧化成乳醛，不是S05的丙醛；S2乳醛→乳酸与外源S01不同；S3乳酸→丙酮酸与外源S02–S04不同；S02–S04目标反应未交付。故目标S=0，存在已核目标方向/结构不符与漏交付；错误路线内部酶自洽不得增加目标信用。C04落&#91;1,2&#93;，因无可用目标催化对应取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：gold S05入口脱水及S01–S04目标反应的方向与主要底物/产物。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_104：gold各步accepted酶/EC范围；只作目标反应核对，不外推具体蛋白活性。
- ANSWER_TEXT / ANSWER.steps：答案三步为乳醛/乳酸/丙酮酸替代路线，未给出丙醛、1-丙醇、丙酰CoA、丙酰磷酸或丙酸目标步。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 物种E. coli与菌株K-12 MG1655身份合理；答案为fucO/aldA/lldD三步统一使用该菌，并把整路能力限定为“调控突变后”，没有把野生型直接写成组成型全路菌，符合身份/单步能力/整路能力分层。保留扣分：TaxID 511145与MG1655菌株级全路能力在E0无对应记录，Cocks 1974虽交付但未能在冻结快照核验；属菌株粒度局部待核，未推翻物种级与酶基因层面的主要微生物推荐。7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism；ANSWER.organism_profiles&#91;0&#93;；ANSWER.uncertainties：答案的统一菌株选择、TaxID与整路能力限定。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_104：gold含E. coli物种/部分步记录，但不是511145菌株记录；不能自动支持菌株级身份。

</details>

### D4 性状科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状全部填写。gold E. coli物种记录支持兼性/耐氧、pH范围、非嗜盐、运动、杆状、革兰氏阴性、不产芽孢等主要性状；F14的NC_000913.3/MG1655数值与常见参考一致但E0未给精确记录。少数菌株级/子字段（37°C optimum、ATCC 700926、精确基因组数值、调控后可利用丙二醇）为局部待核，未发现与gold明显矛盾。按7–8档取8：主要性状可核实且适用，仅少量菌株级数值/条件需确认。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_104：E. coli物种级性状记录；支持部分主要性状，不等于所有MG1655菌株级数值均已核实。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_104：标出哪些E. coli性状有可评分观测；温度/盐度部分子字段仍待老师范围政策。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：答案15项性状及其confidence/evidence_id；用于核对具体值。

</details>

### D5 来源与可核查性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案交付了具体PMID、UniProt、NCBI、ATCC定位，核心路线/酶/菌株来源可定位；但E0无E. coli相应记录，均只能登记UNRESOLVED_SOURCE，且大量性状仅EVID_006 INTERNAL_KNOWLEDGE_ONLY，为MISSING_SOURCE；终点丙酮酸与好氧路线选择也缺直接来源。未发现经冻结证据核实的错引，severity_overall=NOT_APPLICABLE。核心可定位、部分模块缺失，落5–6档；因核心locator具体且答案披露不确定性，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry；ANSWER.uncertainties：列出具体来源类型、PMID/UniProt/NCBI/ATCC locator；EVID_006为内部知识。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_104：只说明哪些性状有gold可评分记录，不核对答案引用的PMID/UniProt真实性。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确披露氧条件未指定、当前主链是好氧氧化而非pdu厌氧脱水路线；说明野生型不一定组成型表达该路线；并指出EC 1.1.2.3的IUBMB细胞色素c与生理醌受体的不一致。置信度与来源类型分开给出，未系统性把预测写成实证。扣分点：若干EVID_006内部知识性状仍标high confidence，属局部过度确信，故取8而非9。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties；ANSWER.route_scope.notes；ANSWER.evidence_registry：答案对氧条件、路线选择、野生型表达、EC/受体不一致的披露。
- RUBRIC_CLAUSE / C06：D6按证据性质与不确定性独立评价；单点过度确信与系统性误导分开。

</details>

## GPT5.6

答案SHA256：`68b33faaf857b84cdfd966868f73a544787ca871191effefcd80bcb45178d0a5`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Route name and two steps are delivered, but only the entry S05 and S02 are present; the required main degradation route is not completed to a gold terminal product. One organism profile is given, but all 15 traits are null/unknown and sources are internal-only. This is the 3-4 band: only partial necessary content and multiple missing downstream steps.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：Gold lists five required steps and terminal products Propionate|1-Propanol; the answer only delivers S05-&gt;S02 and stops at propanoyl-CoA.

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The two delivered transformations match gold chemistry: S05 propanediol dehydratase gives propionaldehyde, and S02 CoA/NAD+-dependent propanal dehydrogenase gives propanoyl-CoA with NADH/H+. Continuity between the two steps is correct. However the route stops at propanoyl-CoA and omits downstream terminal conversion, so the main trunk is only partial; 5-6 band.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：Supports the delivered S05 and S02 chemistry and cofactors; does not supply the omitted terminal steps.

</details>

### D3a 目标反应与酶对应：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Judging from the answer text and accepted sets, S05 is supported by propanediol dehydratase/EC 4.2.1.28 and S02 by CoA-dependent propanal dehydrogenase/EC 1.2.1.87. The automatic matrix leaves S02 unbound and S05 candidate-only, but does not rewrite these source facts. The key terminal step S03 and S04/S01 are not delivered, so a confirmed KEY omission applies D-KEY4 and caps D3a at 4; 4 is the upper permitted value, not a full-route claim.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_104：Supports accepted function-level enzyme/EC correspondences for S05 and S02; does not prove PduCDE/PduP specific-protein activity or the omitted steps.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_104：Shows terminal propionate and downstream propanoyl-phosphate steps are absent from the answer.

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The genus/species Salmonella enterica matches gold step organisms and a pathway-complete species. However the answer claims strain LT2 with TaxID 216597 and sets a complete-pathway profile, while frozen gold/E0 supplies only species-level Salmonella enterica 28901 and no verification of LT2/TaxID 216597. Species-level identity supports partial credit; strain-level and whole-path capability remain unverified, so 5-6 band.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_104：Supports Salmonella enterica at species level and pathway-complete status for taxid 28901; does not verify strain LT2 or TaxID 216597.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 required trait fields are present only as null/unknown values; no trait value or source is delivered. Under P44, when all required traits are null/empty, D4 is MISSING=1 rather than an accuracy score.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_104：Shows available gold trait material is not used by the answer; the answer supplies no trait value to compare.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All model-delivered evidence entries are INTERNAL_KNOWLEDGE_ONLY with null database, record_id, and locator. There is no locatable literature, database, or computation record supporting the route, enzymes, or strain. This is MISSING_SOURCE, not verified mis-citation; low band 1-2, assigned 2 because the answer at least groups claims and marks source confidence low.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows all delivered evidence is internal-only with no database/record/locator; supports MISSING_SOURCE, not verified mis-citation.

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer explicitly marks all 15 traits unknown, notes oxygen is unspecified, flags S-isomer evidence as unverified, notes PduP cofactor/direction uncertainty, and states downstream steps were omitted. However it labels step and microorganism confidence medium while all delivered evidence is internal low, and it sets a complete-pathway profile for a partial two-step route. Some confidence exceeds evidence, but this is not systemic prediction-as-observation; 5-6 band, assigned 6.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit disclosure of oxygen, stereochemistry, cofactor/direction, and downstream limitations; also shows medium step confidence against internal low sources.

</details>
