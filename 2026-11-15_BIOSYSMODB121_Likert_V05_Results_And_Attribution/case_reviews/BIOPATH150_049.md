# BIOPATH150_049：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：glycerol degradation I

污染物：Glycerol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 65.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 58 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 66 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 63.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 64 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 46.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`ae006fec5512b58ccf1872344418d87f6448891aef2ff12d2a350283a4f0eaaf`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 答案JSON可读，route_scope.chosen_route_name与题面一致，S1/S2分别给出甘油激酶和甘油-3-磷酸脱氢酶、EC、E. coli及15项性状；但按本题任务与gold，主链必答含S03甘油facilitator（S03→S01）且终点为glycerone phosphate，答案未交付S03，另把DHAP→D-GAP的TPI作为S3主链步延伸到gold终点之后。属主要模块已涉及但必要主链步骤缺失/范围偏移，需实质修订，按D1 5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

三步主链、每步 main substrate/product+SMILES、首选酶+EC、对应微生物均实质交付；route_scope.chosen_route_name 原样填写题面给定路线名；15项性状全部填写。仅 S2 泛醌/泛醇 SMILES 为 null、未涉及 gold 中的甘油转运步骤，属少量工程/范围缺陷，7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：本题为LINEAR_UNIQUE，ordered_step_count=3，路径名为glycerol degradation I。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：gold任务主链显示S03甘油facilitator在S01之前、S01→S02；S02终产物为glycerone phosphate；未将TPI列为该主链步。该gold不穷尽，不能据此自动证明TPI化学错误。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_049：本题gold终点化合物为Glycerone phosphate(2-)。
- ANSWER_TEXT / ANSWER_BEGIN：答案交付S1-S3三步及逐步酶/EC/微生物，并交付ORG_001的15项性状与evidence_registry；其中没有与gold S03对应的甘油跨膜facilitator步骤。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> S1甘油经甘油激酶磷酸化为sn-glycerol 3-phosphate并生成ADP，S2以醌为电子受体将sn-glycerol 3-phosphate氧化为glycerone phosphate，方向、主产物与gold S01/S02的化学转化一致；S3 DHAP↔D-GAP为化学上成立的糖酵解下游反应。未见方向反转、原子明显不守恒或基本化学约束违反。ubiquinone/ubiquinol未给SMILES、终点后延伸及电荷/立体表示未定属局部问题，不改变主链化学结论；D2 9–10门未开且程序允许上界为8，故取8。

<details><summary>V0.4理由与本行变化背景</summary>

甘油→sn-甘油-3-磷酸→磷酸二羟丙酮→D-甘油醛-3-磷酸的转化方向、结构与连接合理；S1（激酶磷酸化，ATP/ADP 在列）与 S2（醌依赖脱氢，泛醌/泛醇在列但SMILES null）与 gold 前两步一致；S3 tpiA 异构化为化学自洽的下游延伸，答案在 uncertainty 中声明部分数据库以 DHAP 为终点。题面未指定终点，按 P29 下游延续不加分亦不扣覆盖率；H+ 未列与泛醌 SMILES 缺失属局部计量/表达缺陷，7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：支持本题gold S01为glycerol→sn-glycerol 3-phosphate、S02为sn-glycerol 3-phosphate→glycerone phosphate的SUBSTRATE_TO_PRODUCT方向；S03为甘油facilitator；S02为gold终点步。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_049：本题gold终点产物为Glycerone phosphate(2-)，答案S2产物与之一致；答案另列的D-GAP属终点后延伸。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：本题路径为线性唯一，gold ordered_step_count=3；该材料不穷尽，不能反推所有未列反应均错误。
- ANSWER_TEXT / ANSWER_BEGIN：答案S1-S3给出主底物/主产物SMILES、ADP/ATP与ubiquinone/ubiquinol角色及连续步骤；S3为DHAP到D-GAP的异构化，化学上成立但在gold终点之后。

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> S1 glycerol kinase EC 2.7.1.30 and S2 glycerol-3-phosphate dehydrogenase EC 1.1.5.3 match the accepted enzyme/EC sets. The required KEY_ENTRY S03 glycerol facilitator is absent; answer step S3 is the extra downstream triose-phosphate isomerase reaction (DHAP to D-GAP). With two supported targets and one key entry target missing, the KEY4 cap restricts D3a to &#91;1,4&#93;; score 4 because the supported part and key failure boundary are clear.

<details><summary>V0.4理由与本行变化背景</summary>

S1 glycerol kinase EC 2.7.1.30 与 S2 glycerol-3-phosphate dehydrogenase EC 1.1.5.3 分别与 gold enzyme_gold 记录的酶名/EC 一致，酶类别与反应类型自洽；S3 triose-phosphate isomerase EC 5.3.1.1 属公认异构酶且与酮-醛异构反应类型一致，但冻结证据无该步骤记录，登记局部待核，不推翻关键步骤酶对应可靠的整体判断。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_049：Supports S01 glycerol kinase EC 2.7.1.30 and S02 glycerol-3-phosphate dehydrogenase EC 1.1.5.3; S03 accepted enzyme is glycerol facilitator.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：Shows S03 gold reaction is glycerol&#91;out&#93; to glycerol&#91;in&#93;, not DHAP to D-GAP.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> The answer uses Escherichia coli K-12 substr. MG1655, TaxID 511145, consistently. Gold supports E. coli species-level identity and PATHWAY_COMPLETE for TaxID 562, but the strain-level TaxID and strain-level whole-path claim are not independently verified. This is a granularity/identity-strength issue (species-level support for strain-level claim), normally 7档附近 and not a cap.

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份为 Escherichia coli K-12 substr. MG1655，物种层与 gold organism_gold 的 Escherichia coli（TaxID 562、pathway_complete=TRUE）一致，与路线酶（glpK/glpD）自洽；答案给菌株级 TaxID 511145，声称粒度与所填 ID 粒度匹配，但 E0 无该 ID 冻结记录（UNRESOLVED，非 CONTRADICTED）。菌株级能力依赖物种级记录，属粒度不足档内扣（7档附近），未推翻主要微生物推荐，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_049：Supports E. coli TaxID 562 for S01/S03 and PATHWAY_COMPLETE E. coli true; does not directly verify TaxID 511145 or the strain-level whole-path claim.

</details>

### D4 性状科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> Most scoreable E. coli traits match frozen gold observations or species-level representative values: mesophilic preference, non-halophilic category, motility, rod morphology, Gram-negative, non-sporulating, glycerol growth, and broad heterotrophy. Several subfields are unscoreable or unresolved (temperature/pH/salinity endpoints, ATCC number, genome accession), but no major trait is shown wrong; the band is 7-8, taking 8 because the supported traits and limitations are clear.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部填写；多项与 gold trait_gold 物种级记录一致：兼性厌氧/耐氧、pH optimum 7.0 落在 gold pH growth 7.0–8.5、非嗜盐（non-halophilic）、可运动、杆状、革兰氏阴性、不产孢、降解谱非芳香/非烃；温度上下限、pH 上下限、盐度数值诚实填 null。F5 保藏号 ATCC 47076 与 gold 记录 DSM 4599 不同、F14 基因组 NC_000913.3/4641652 bp/50.78% 与 gold Genome ID GCA_003018455.1 不同，均因 E0 GAP 无法核验（UNRESOLVED）；F9 用甘油代谢酶代替标准酶活面板属解读偏差。主要性状可核实适用、少量记录与条件待核，7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_049：Species-level E. coli trait observations support broad traits such as non-halophilic, motility, rod shape, Gram-negative, non-sporulating, and glycerol growth prediction; not all strain-specific values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_049：Shows which trait fields are scoreable and which are completeness-only or pending teacher adjudication.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_049：Shows temperature/pH/salinity endpoints are pending or unscoreable; prevents treating unverified numeric endpoints as a proven error.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> Delivered traceability is partial. The route and enzyme claims name MetaCyc/EcoCyc entries with pathway/gene locators, and genome/collection claims give RefSeq/ATCC accessions, but most route/enzyme records lack stable record_id values, and many trait claims rely only on INTERNAL_KNOWLEDGE_ONLY. E0 is EVIDENCE_GAP, so no source is verified or contradicted; D5 is scored on delivered source form, leaving it in the 5-6 band at 5.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CORE: CG01/02/03/05/07；APPLICATION_CRITICAL: CG08/17）中，路线与酶-EC 依赖 EVID_001 MetaCyc &quot;pathway name&quot; 与 EVID_002 EcoCyc 基因注释（record_id 均为 null，GENERIC_SOURCE），性状类 CG10–13/CG15/CG16 依赖 EVID_005 INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；仅 EVID_003 RefSeq NC_000913.3、EVID_004 ATCC 47076 属条目级 record_id，但 E0 整题 EVIDENCE_GAP 无法核对（UNRESOLVED_SOURCE）。按 P41，决策相关组不存在条目级可定位且可核对的结论，落3–4档；无已核实错引，不触发cap，取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer includes a specific uncertainty section for the null oxygen condition, anaerobic alternative, endpoint ambiguity, null numeric limits, and cofactor SMILES. However many general traits are backed by INTERNAL_KNOWLEDGE_ONLY yet carry high or medium confidence, with limited in-field labeling of evidence type. This is overconfidence and partial labeling rather than systemic misleading; 5-6 band, taking 6 because the main limitations are disclosed.

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties 数组具体列明：氧条件未指定下好氧 GlpD 与厌氧 glpABC 的取舍、S3 终点与部分数据库记载的差异、温度/pH/盐度上下限无可靠来源故填 null、泛醌 SMILES 未给；诚实null与范围声明质量较好。但多项仅由 EVID_005 INTERNAL_KNOWLEDGE_ONLY 支撑的性状（F1/F2/F6/F11/F12/F13）标 high confidence，置信与证据强度不相称，属多点过度确信而非系统性把预测写成实证观测，档内扣至6档，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`c519e6f2449486aa836fc54ebaf798af977fd8fcfbac8497b8b74d9189ab1c2c`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 5–6档，取6。答案正确填写route_scope名称并给出S1甘油激酶、S2甘油-3-磷酸脱氢酶两步及辅因子，但完全缺少必答的S03甘油 facilitator/转运步（3个必答步只交付2个）；无改选路线问题，主要模块均在，但关键入口步遗漏和来源占位使完整性不能进入7–8。

<details><summary>V0.4理由与本行变化背景</summary>

各模块均有实质交付：路线名原样回填glycerol degradation I、两步有序主链（含SMILES、酶+EC、对应菌）、15项性状、evidence_registry、uncertainties；JSON完整可读，无自述或题面复读。缺陷：gold主链为3步（S03甘油转运/易化步，linear_display_order=1、拓扑层级0位于首步），答案只给S01、S02两步且未以范围声明说明省略转运/摄取步，属少量必要内容遗漏但关联清楚，落7–8档，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：证明本题任务要求3个必答步；不证明答案已交付全部步骤。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：gold含S03转运步；该行是任务完整性参照，不是D2化学转化评分。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 7–8档，取8。S1甘油经甘油激酶磷酸化为甘油-3-磷酸并带ATP/ADP，S2甘油-3-磷酸经醌依赖脱氢酶生成二羟基丙酮磷酸并带泛醌/泛醇，方向、主产物和连续性正确；缺少S03转运步主要归D1/D3a完整性，且G3P/DHAP的电荷/立体表示待representation review，故不进入9–10，但主链化学可靠性足以取8。

<details><summary>V0.4理由与本行变化背景</summary>

两步化学转化与gold逐行吻合：S1甘油+ATP→甘油-3-磷酸+ADP（磷酸化，方向正确，结构SMILES与gold共识一致）；S2甘油-3-磷酸+电子传递醌→二羟基丙酮磷酸+醌醇（氧化，方向正确）。终点二羟基丙酮磷酸即gold terminal Glycerone phosphate(2-)，止于题面终点，无未声明的下游越界；辅因子（ATP/ADP、醌/醌醇）在列，仅在H+等小项上简化，属局部计量缺陷（八.辅因子条款7–8档）。未表示转运步属化学外部环节，不影响主链化学正确性。落7–8档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：支持两步主转化和辅因子方向；不支持具体蛋白实测活性；电荷/立体表示另有review。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_049：支持起点/终点主化合物身份；不代表答案已完成所有必答步。

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> D-KEY4受限&#91;1,4&#93;，取4。S1 glycerol kinase/EC 2.7.1.30与S2 glycerol-3-phosphate dehydrogenase/EC 1.1.5.3均与accepted set的G4酶名/EC一致；但S03 glycerol facilitator/转运反应为预定义KEY_ENTRY且答案完全未交付，属KEY实证遗漏，D3a不能超过4。4为上限而非默认：两个可用KEY步支持边界清楚，S03缺失使主链不完整。

<details><summary>V0.4理由与本行变化背景</summary>

两步酶-EC对应均与gold一致且无自相矛盾：glycerol kinase / EC 2.7.1.30（gold S01，GLYCEROL-KIN-CPLX）、glycerol-3-phosphate dehydrogenase (quinone) / EC 1.1.5.3（gold S02 aerobic glycerol-3-phosphate dehydrogenase），反应类型（磷酸化/氧化）与EC大类匹配，未出现酶名与EC互斥或家族相关性冒充催化证据的情形。基因glpK/glpD属合理补充但E0无核验记录。gold S03（glycerol facilitator，EC=NOT_OBSERVED）非酶学核心，未给不构成D3a关键错误。落8档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_049：支持S1/S2酶名-EC与目标反应在G4策展粒度匹配；不支持具体蛋白活性或任意菌株能力。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：支持S03为必答转运反应；答案未交付该步，触发D-KEY4遗漏上界。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 7档。E. coli物种身份在S01与gold完全命中，gold亦记录E. coli pathway_complete=TRUE，支持物种级甘油降解能力；K-12 MG1655/TaxID 511145与S02步级E. coli归属不在冻结step organism行中，且S03微生物未交付。按身份阶梯，物种级真实记录支持菌株级声称属档内扣、不cap，取7。

<details><summary>V0.4理由与本行变化背景</summary>

身份层：两步均指向Escherichia coli K-12 substr. MG1655（TaxID 511145），与gold S01匹配菌Escherichia coli（taxid 562）同lineage，species/菌株粒度自洽；两步同菌并按要求去重（单一profile ORG_001被两step引用）。能力层：gold PATHWAY_COMPLETE列出taxid 562对BSY-p00432的pathway_complete=TRUE，提供物种级整路径能力正向参考；但S02步gold匹配菌为Pseudomonas putida/Saccharomyces cerevisiae，答案改用E. coli需独立反应级证据（E0未见），TaxID 511145在E0无记录（GAP-049-028/030）。未出现跨属/无关类群、亦未把单步菌写成整条路径菌。属&#x27;主要对应有可靠支持、少量条目待确认&#x27;，7–8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_049：支持E. coli物种身份和物种级完整路径能力；不支持K-12 MG1655菌株级TaxID或S02步级E. coli归属。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 7档。主要性状与E. coli物种级gold一致或合理：F1 facultative anaerobe与预测一致，F2 mesophilic与gold偏好一致，F10 motility、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating均有物种级gold支持，F14 size/GC落在物种范围；F3/F4显式unknown，F5 ATCC 47076、F14 NC_000913.3及F15广适栖息地未在冻结记录中直接核实。按同物种代表记录口径档内取7。

<details><summary>V0.4理由与本行变化背景</summary>

与gold可比对的性状多数成立：F1氧耐受与gold观测aerotolerant一致；F2 preference嗜温与gold观测mesophilic一致；F10 motility、F11 rod-shaped、F12 Gram-negative（gram positive=false）、F13 non-sporulating均与gold物种级观测一致；F7的甘油生长与gold预测growth: glycerol=true一致。但关键缺口明显：F3 pH、F4盐度整项null（gold该taxid有pH/盐度记录，虽pH子字段为completeness_only、盐度端点pending teacher adjudication）；F2 optimum 37°C在gold无optimum子字段（mask标completeness_only）；F5 ATCC 47076与gold物种级代表记录DSM 4599不同株（按四.4不判错，但未经核验）；F14基因组数值与F15栖息地无冻结证据。整体落&#x27;部分性状准确且适用，但关键项证据不足或条件解释需修订&#x27;5–6档，取6。未把任何性状写成整菌降解能力，未出现数值离谱或物种观测硬推全菌株的表述。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_049：支持E. coli物种级氧耐受、温度偏好、运动性、形态、Gram、产孢及基因组范围；不支持K-12菌株特异F5/F14或F15。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_049：标明pH/habitat不是观测准确性子字段；不能据此把unknown判错。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 1–2档，取1。全部evidence_registry条目EVID_001–EVID_005均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；路径、酶-EC、微生物、性状和基因组关键结论均无法追到可定位文献/数据库条目或计算记录。属MISSING_SOURCE缺失，不是已核实错引，按P34低分且默认不cap；因关键结论完全不可外部定位，取低档下沿1。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 5条全部为INTERNAL_KNOWLEDGE_ONLY：database/record_id/locator均为null，claim_scope只是文字描述，无任何可定位可核对的条目、文献或计算记录。决策相关组（CG01路线核心、CG02起点、CG03终点、CG05酶-EC、CG07核心菌株身份、CG09整路径能力）全部为MISSING_SOURCE，无条目级证据可进入5–6档；SUPPORTING组同样缺失。按四.3/P34，MISSING_SOURCE为缺失而非误导，默认不触发关键错误cap；整体落&#x27;几乎无法定位重要结论依据&#x27;1–2档，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示答案实际交付来源为internal-only；不能作为外部可定位来源。
- RUBRIC_CLAUSE / P34：MISSING_SOURCE/INTERNAL_KNOWLEDGE_ONLY按低分档，默认不触发cap。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 5–6档，取6。答案把全部证据标为INTERNAL_KNOWLEDGE_ONLY，F3/F4明确unknown，并给出氧条件未指定、可能使用其他同工酶的uncertainty，这些是正面披露；但酶/EC、微生物TaxID及多个性状仍以high/medium confidence呈现而无外部支持，部分结论强度超过依据。属局部过度确信而非系统性把预测写成观测，取6。

<details><summary>V0.4理由与本行变化背景</summary>

正面：F3、F4以value整体null+confidence=unknown显式声明未知，F2 min/max留null而非编造；uncertainties明示题面氧条件未指定且厌氧可能改用其他同工酶；每条evidence均标注source_type=INTERNAL_KNOWLEDGE_ONLY，属对来源性质的诚实声明而非把预测写成观测。不足：EC、革兰氏、产孢、基因组等仅凭内部知识的结论标confidence=high，证据强度与置信标签不相称；未说明同一菌株粒度的证据边界与替代分支。属多处单点过度确信而非系统性误导（无掩盖已知矛盾、无把预测冒充实证观测），落5–6档取6。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry/uncertainties：显示internal-only披露、unknown标注及氧条件/同工酶提示；也显示部分high confidence缺乏外部依据。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；D6按披露质量独立定档。

</details>

## Kimi

答案SHA256：`d8e8f8d30dff58e8ddf219450fe15254f9b5004af48802c9fe7de9ebc66c8729`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 路线名按题面原样填写；交付了S1、S2两步及15项性状、1个菌profile，模块关联总体清楚。但本题任务范围登记的必答主链含S03 glycerol facilitator入口步，原答steps仅有S1/S2，无S03转运步，属必要内容遗漏；故选D1 5–6档内的6分，不认定D1关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

题面指定路线名原样回填（glycerol degradation I，未改选）、两步核心转化、每步一个首选酶+EC+一个对应菌、15项性状全部返回、来源与不确定性均有交付，主模块对应清楚；相对gold三步（含S03 glycerol facilitator 转运步）缺转运步与辅因子参与者字段，属少量遗漏，落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：本案正式主链为LINEAR_UNIQUE、ordered_step_count=3；仅作路线任务上下文，不等同于要求交付全图所有旁支
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：gold反应行显示S03 glycerol facilitator为甘油入口转运步并连接到S01；支持S03属于本案任务范围内需处理的入口步，不扩展到其他未交付旁支
- ANSWER_TEXT / ANSWER.steps：原答只给出S1甘油激酶和S2 GlpD两步，未给出S03 glycerol facilitator/转运步；同时organism_profiles含全部15项性状

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> S1甘油经ATP依赖甘油激酶生成sn-glycerol 3-phosphate；S2由aerobic glycerol-3-phosphate dehydrogenase（GlpD, EC 1.1.5.3）氧化为glycerone phosphate/DHAP，方向正确，主链连续，并止于题面/gold终点DHAP。局部缺陷为：ATP/ADP、醌/醌醇未列入substrates/products；产物SMILES的电荷/立体表示与gold表示不同；未展开S03转运。按P103辅因子遗漏属局部计量缺陷，不自动cap；D2取7–8档内的7分，无关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

S1 ATP依赖磷酸化 甘油→sn-glycerol 3-phosphate、S2 醌依赖氧化 sn-glycerol 3-phosphate→glycerone phosphate，方向、顺序、起点与终点均与gold S01/S02及terminal一致，无起始步错误、无跳步、无方向反转；但答案只列主底物/主产物，未把ATP/ADP、醌/醌醇列入participants，属局部计量缺失（八.辅因子条款P103），不cap，7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_049：本题根化合物为Glycerol，终点主产物为Glycerone phosphate(2-)；支持D2终点边界，不支持其他未声称化学
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：gold S01显示甘油经ATP/ADP相关磷酸化到sn-glycerol 3-phosphate；S02显示醌依赖氧化到glycerone phosphate；支持主转化和辅因子为局部缺失，不证明具体蛋白实验活性
- ANSWER_TEXT / ANSWER.steps：原答S1/S2主底物与主产物、方向和酶EC与主链化学一致；未列ATP/ADP、醌/醌醇为底物/产物，且未给S03转运步
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏通常按局部计量缺陷在7–8档处理，非自动cap；仅在任务明确要求完整配平并使主要结论失效时才另评

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分9 → V0.5新分5，变化-4。

新裁判理由：

> N=3（S01、S02、S03）。S01/S02原答给出glycerol kinase EC 2.7.1.30与aerobic glycerol-3-phosphate dehydrogenase EC 1.1.5.3，名称和EC与gold/accepted集合一致，具有适用功能支持；但E0为整题证据缺口，显式名称—EC配对、表示等价与具体记录仍UNRESOLVED，按C03应记U而非冒充S。S03为KEY_ENTRY glycerol facilitator，原答未提供该步，按实际缺步记M（缺失定位：steps仅有S1/S2）。因此无已确认S，两个目标有适用功能支持但待核，一个关键入口步缺失，阻止进入7–8；按C05 5–6档取5分。该缺步按D3a目标M计入，不另按D3a关键错误清单或未经确认的D-KEY4 proof判key_error。

<details><summary>V0.4理由与本行变化背景</summary>

两步首选酶glycerol kinase(EC 2.7.1.30, glpK)与aerobic glycerol-3-phosphate dehydrogenase(EC 1.1.5.3, glpD)的酶名、EC与基因标识与gold S01/S02逐项一致，反应类型（磷酸化/醌依赖脱氢）与EC大类匹配，未见酶名-EC互斥或家族相关性冒充具体催化；EC/UniProt条目本体在E0中无记录，作局部待核登记，不影响酶-反应对应判定，9档取9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_049：S01 accepted为glycerol kinase EC 2.7.1.30；S02 accepted含aerobic glycerol-3-phosphate dehydrogenase EC 1.1.5.3；S03为glycerol facilitator且无EC。仅支持数据库策展粒度功能/名称，不证明具体蛋白实验活性或显式EC配对已核
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：S01/S02目标反应分别为甘油磷酸化与sn-glycerol 3-phosphate氧化到glycerone phosphate；S03为甘油入口转运步。支持目标反应与缺步判断，不扩展到未声称内容
- ANSWER_TEXT / ANSWER.steps：原答S1/S2的酶名与EC与accepted/gold名称—EC一致，但S03缺失；显式EC配对在E0无冻结记录时保持UNRESOLVED
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：案件正式主链为3步线性；用于N=3上下文，不把全图其他内容自动当主链缺步分母

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> Species-level E. coli is supported by the S01 gold organism record and by a PATHWAY_COMPLETE E. coli record, and the answer&#x27;s identity fields are internally coherent. However it uses strain K-12 MG1655 TaxID 511145, while frozen gold organism records use TaxID 562 or other step organisms, and S02 is attributed to E. coli although gold step rows list other organisms. This is a strain-level/granularity and step-attribution issue, not a verified contradiction, so 7.

<details><summary>V0.4理由与本行变化背景</summary>

两步均归属Escherichia coli K-12 MG1655，与gold S01/S03的E. coli(562)一致、且gold PATHWAY_COMPLETE含taxid 562，菌株选择与整条路线能力不矛盾；gold S02步级菌为P. putida/S. cerevisiae属gold非穷尽，E. coli glpD催化该步有独立条目级引用支撑，不因与gold不同判错；TaxID 511145与菌株级身份未在E0核验，按局部待核登记，8档取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_049：Supports E. coli at S01 and species-level PATHWAY_COMPLETE for TaxID 562; does not verify strain 511145 or all step-level attributions.

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> Most 15 traits align with E. coli species-level gold/representative data: facultative/anaerobic, mesophilic, non-halophilic, rod-shaped, Gram-negative, non-sporulating, motile, and glycerol-growth support. Local issues remain: 37C optimum is extrapolated from routine growth rather than an optimum measurement; ATCC 700926 and strain-specific genome NC_000913.3/TaxID 511145 are not in frozen records; exact pH/genome values need verification. These are local condition/granularity issues, not a verified key failure, so 7.

<details><summary>V0.4理由与本行变化背景</summary>

15项全填且多数与gold taxid 562观测一致（F1兼性厌氧/耐氧、F4非嗜盐、F10有运动、F11杆状、F12革兰阴性、F13不产孢），F8/F10/F15主动限定适用范围、诚实标注低置信；扣分点：F2把ATCC\&quot;常规培养37°C\&quot;表述为\&quot;最适约37°C\&quot;（培养温度≠最适温度，P52/P113），F3最适pH 7、F5 ATCC 700926、F14 NC_000913.3/4,641,652 bp/50.8%均为E0未核的条目级数值，按局部待核登记；落7–8档取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_049：Species-level E. coli trait observations; does not verify strain-specific ATCC/genome values or optimum from routine growth.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_049：Shows many temperature/pH/salinity range subfields are pending or completeness-only; not a numeric exact-match basis.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> The answer supplies a mapped evidence_registry with specific locators for enzymes, TaxID, genome and ATCC, but E0 is EVIDENCE_GAP so no citation can be verified. Core route evidence EVID_001 is a generic MetaCyc pathway page, many traits use INTERNAL_KNOWLEDGE_ONLY, and whole-path capability lacks a dedicated source. Some decision-relevant claims have entry-level locators, so this is a 5-6 case; no verified mis-citation and no cap, select 6 because mapping is clear but key verification is pending.

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组中CG05（UniProt P0A6F3/P13035）、CG07（NCBI Taxonomy 511145）、CG17（RefSeq NC_000913.3）为条目级可定位引用，CG01/CG03仅有MetaCyc\&quot;pathway page\&quot;且record_id=null的笼统来源；支持组CG10/CG12/CG13/CG15多依赖INTERNAL_KNOWLEDGE_ONLY(EVID_007)→MISSING_SOURCE。E0本题为EVIDENCE_GAP（entries=0），全部条目内容与claim_scope的匹配无从核验→UNRESOLVED_SOURCE，不判虚构、不计已核实错引、不cap；按P41\&quot;部分关键结论可定位可核对、其他模块缺映射\&quot;落5–6档，取低端5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows delivered source registry and locators; does not itself verify the citations.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_049：Shows accepted enzyme/step context; not a citation-verification record for the answer&#x27;s UniProt IDs.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The answer clearly flags that oxygen was unspecified and that GlpD&#x27;s terminal electron acceptor was not expanded, and it labels confidence including an explicitly INTERNAL_KNOWLEDGE_ONLY evidence source. Some unverified identifiers carry high confidence, but they are tied to specific database locators and there is no systematic prediction-as-observation or hidden contradiction. Local overconfidence/labeling gaps keep this at 8 rather than 9.

<details><summary>V0.4理由与本行变化背景</summary>

逐项confidence分级（high/medium/low）与source_type如实标注，EVID_007自陈INTERNAL_KNOWLEDGE_ONLY；uncertainties明确列出氧条件未指定、GlpD末端电子受体未展开；F8/F10/F15主动限定范围并降低置信。不足：F5/F7/F14对E0未核的编号/表型给high confidence（单点过度确信，P119），未见系统性把预测写成实证或掩盖矛盾，落7–8档取8。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit caveats for oxygen condition and GlpD electron acceptor; does not verify the identifiers.

</details>

## Qwen

答案SHA256：`7a6f497461a4a0c5491178905b5293ecb3f28bc93c2a345f2158c2842e5f61e2`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 题面指定的 route_name 原样填写；两个已给步骤均含底物/产物、主要SMILES、首选酶/EC、对应微生物，且同一菌只建一个 profile，15项性状键齐全。但任务合同要求3个必答步，答案仅交付S1/S2，缺少gold的S03 glycerol facilitator（glycerol&#91;out&#93;→glycerol&#91;in&#93;）入口步骤，route_summary也只覆盖两步化学反应；属必要内容遗漏，不是全部适用要求均被实质回应。无核心任务模块大部缺失、无严重偏离指定路线、输出可读，故D1不触发关键错误；按5–6档，遗漏一项但其余模块清楚，取6。

<details><summary>V0.4理由与本行变化背景</summary>

主要模块齐备：route_scope逐字回填题面路线名，route_summary、2步主链（底物/产物英文名+SMILES、首选酶+EC、对应微生物）、15项性状结构、evidence_registry与uncertainties均实质交付；关联清楚。不足：未包含gold的S03甘油转运步；F3/F4/F5/F8/F10五项为明确未知（如实登记但完成度不足）；辅因子ATP/ADP的SMILES为null。属7–8档中取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：Gold显示S03 glycerol facilitator为glycerol&#91;out&#93;→glycerol&#91;in&#93;的入口步骤，位于S01之前；S01/S02为后续化学步骤。支持任务主链包含S03，不能把全图材料数当旁支分母。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：ordered_step_count=3、LINEAR_UNIQUE，支持本题必答主链为3步而非2步；不是要求全部旁支。
- ANSWER_TEXT / ANSWER.steps：答案实际只交付S1/S2两步，缺少S03入口运输步；不能据此声称全部必答步已实质回应。
- ANSWER_TEXT / ANSWER.organism_profiles.ORG_001.traits：15项性状字段均出现且同一菌仅一个profile；字段存在不等于每项内容均非null，但不支持D1整模块缺失。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> S1甘油激酶磷酸化（glycerol+ATP→glycerol 3-phosphate+ADP）与gold S01方向、主产物一致；S2甘油-3-磷酸脱氢酶氧化为dihydroxyacetone phosphate（glycerone phosphate）与gold S02主转化及终点一致，S1产物作为S2底物，连续性成立。S2以泛化acceptor/reduced acceptor表示电子载体，未写具体电子传递醌，属局部计量/表达简化；缺S03运输步影响入口完整性，但核心化学转化未反转、无主链第一步错误、无原子明显不守恒或无依据跳步，故不触发D2关键错误。按7–8档，核心化学主链充分成立但有局部缺口，因程序已限定9–10不可用且现存问题不改变主要化学结论，取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链两步化学成立且连续：S1甘油经ATP依赖磷酸化生成sn-glycerol 3-phosphate（与gold r01889一致）；S2以醌型电子受体氧化为二羟丙酮磷酸（与gold r03030一致），方向、官能团转化与连接正确，终点与gold terminal Glycerone phosphate(2-)一致；主产物/主底物SMILES合理，辅因子在列。局部问题：电子受体泛写为acceptor、有氧/厌氧酶系未定（题面氧条件null）；未含S03转运步（非碳骨架转化）。7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：S01为ATP依赖的甘油激酶反应，S02为电子传递醌依赖的甘油-3-磷酸脱氢酶反应，主产物为Sn-glycerol 3-phosphate与Glycerone phosphate；方向为substrate→product。支持答案两步核心化学对应gold S01/S02。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_049：terminal_compound_names=Glycerone phosphate(2-)，与答案dihydroxyacetone phosphate终点一致。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_049：S01 accepted EC为2.7.1.30，S02 accepted EC为1.1.5.3；答案的EC与对应反应匹配。具体蛋白实验活性不由此自动证明。
- ANSWER_TEXT / ANSWER.steps.S2：答案S2用泛化acceptor/reduced acceptor而非具体电子传递醌，支持这是简化表达/局部计量问题，不单独构成D2关键错误。
- SCOPE_ROW / SCOPE#BIOPATH150_049#CG04：题面氧条件为null，条件不成立；不能据氧条件强制要求特定好氧/厌氧路线。D2按已有化学步骤本身评价。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> S1 glycerol kinase EC 2.7.1.30 and S2 glycerol-3-phosphate dehydrogenase EC 1.1.5.3 match the accepted enzyme names/EC sets at G4 curation granularity. S03 glycerol facilitator/uptake is not delivered and is marked UNBOUND; because the program key gate is not applicable for an UNBOUND step, I do not apply the D-KEY4 cap. Coverage therefore falls in the partial band &#91;5,6&#93;; I choose 5 because the missing entry/uptake step is a substantive required gap.

<details><summary>V0.4理由与本行变化背景</summary>

两步酶与gold enzyme_gold逐字一致：glycerol kinase EC 2.7.1.30（S01）、glycerol-3-phosphate dehydrogenase EC 1.1.5.3（S02），酶功能类型（激酶/脱氢酶）与所催化反应匹配，未把家族相关性当具体催化证据，并给出glpK/glpD。未核部分：EC accepted name/active状态与基因-蛋白标识因E0无条目未能机器核验（四.6）。8档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_049：S01 accepted glycerol kinase EC 2.7.1.30 and S02 accepted glycerol-3-phosphate dehydrogenase EC 1.1.5.3; does not establish specific protein or strain activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：Gold reactions support the S01/S02 target transformations; S03 transport remains a separate required step and is not bound in the diagnosis.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> The answer uses Escherichia coli K-12 substr. MG1655 for both steps. Species-level E. coli identity and an E. coli complete-pathway gold row support the main organism choice, and the S01 organism is directly present in gold. The strain-level TaxID 511145 is over-specific relative to the frozen species-level record, and S02 step-level gold lists other organisms; these are within-band attribution gaps rather than a verified key identity failure.

<details><summary>V0.4理由与本行变化背景</summary>

物种身份Escherichia coli与gold organism_gold一致（taxid 562），gold PATHWAY_COMPLETE行taxid 562 pathway_complete=TRUE支持其整条路径能力；S01菌归属与gold一致。不足：S02步级菌用E. coli，而gold步级记录为Pseudomonas putida(303)/Saccharomyces cerevisiae(4932)——E. coli glpD确具EC 1.1.5.3活性、属合理步级选择，未构成经核实错误，但缺步级证据；菌株级TaxID 511145无法核验。7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_049：S01 E. coli species and PATHWAY_COMPLETE E. coli taxid 562 true; does not verify strain K-12 MG1655 taxid 511145 or every step-level E. coli attribution.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> All 15 trait slots are present, with 10 filled and 5 explicit null. Core morphology, Gram reaction and sporulation match species-level E. coli gold, and oxygen/glycerol-use claims are plausible. However several key items are unsupported or over-specific: temperature optimum 37 C is not an observed optimum, genome NC_000913.3 and exact size/GC are unverified, F15 is unsupported, and some respiration/enzyme claims rely on internal knowledge. This is a partial 5–6 profile; I choose 6 because the core cell-envelope/morphology traits are correct and the remaining issues are mostly evidence or specificity gaps.

<details><summary>V0.4理由与本行变化背景</summary>

已填10项中性状与gold观测/预测一致：F1兼性厌氧（aerotolerant真/兼性厌氧预测真）、F11杆状、F12革兰氏阴性、F13不产孢、F7可生长于甘油（预测）、F14为K-12 MG1655的基因组量级（4.64 Mb、GC≈50.8%）、F2最适37℃落在gold生长区间0–42℃内且偏好mesophilic。不足：F6末端电子受体只写oxygen（gold另有nitrate reduction=true与electron acceptor: nitrate预测真），表述不完整而非反证；F2 optimum、F14具体登录号无冻结观测源；F3/F4/F5/F8/F10为明确未知（完成度归D1，此处不重复重扣）。7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_049：E. coli species-level observed traits include rod-shaped, Gram-negative, non-sporulating, aerotolerant/facultative, and temperature/salinity ranges; does not verify K-12 MG1655-specific values.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_049：Marks temperature range endpoints pending teacher adjudication, optimum completeness-only, and other subfield scoreability limits.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D5 is partial. The core route/enzyme claims point to EVID_001 MetaCyc &#x27;glycerol degradation I&#x27; but give no record_id, which is only generic route-level source support. EVID_002 TaxID 511145 and EVID_003 NC_000913.3 are exact-looking NCBI identifiers but the case E0 is EVIDENCE_GAP and they remain UNRESOLVED, not verified and not contradicted. Many traits use EVID_004 INTERNAL_KNOWLEDGE_ONLY. There is no verified mis-citation, so no D5 cap; the 5–6 band applies, and I choose 5 because core source mapping is generic and several decision-relevant traits lack delivered sources.

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：核心化学链与酶（CG01/CG02/CG03/CG05）仅由EVID_001（MetaCyc，record_id为空、locator仅路径名）支撑→GENERIC_SOURCE；身份/基因组（CG07/CG17）给出可定位条目号（TaxID 511145、NC_000913.3）但E0为EVIDENCE_GAP无法核对→UNRESOLVED_SOURCE；性状（CG10–CG16）主要依赖EVID_004 INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE。决策相关组存在部分条目级可定位记录（另有EVID_002/003），故不入3–4档；但核心化学与酶链缺条目级定位，取5–6档中较低值5。无经核实错引，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows delivered source records and claim_scope; EVID_001 lacks record_id, EVID_004 is internal knowledge only.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_049：Shows some species-level trait records exist in gold but were not delivered as sources by the answer; does not turn the answer&#x27;s source status into verified.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer does disclose oxygen-condition uncertainty, possible electron-acceptor/enzyme differences, and that some traits rely on internal knowledge; it also uses nulls for many unknown traits. However it assigns high confidence to unverified TaxID/genome claims, gives a specific temperature optimum without a source, and makes a complete-pathway organism claim without strain-level caveat. This is better than systematic overclaiming but still has local overconfidence, so 5–6 band with 6.

<details><summary>V0.4理由与本行变化背景</summary>

有不确定性披露且具体可查：uncertainties明确写出氧条件未指定导致电子受体/酶系不确定、部分性状基于内部知识无原始文献；F3/F4/F5/F8/F10明确置null并标confidence=unknown，未编造填空。不足：EVID_001以DATABASE_DIRECT+high置信包装一个无record_id的路径名来源；F7等预测性性状以事实口吻陈述、未标预测；内部知识性状统一medium置信。属单点/局部过度确信而非系统性误导，不cap，5–6档取6。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit uncertainty for oxygen condition and internal trait knowledge; does not disclose E0 verification gaps for TaxID/genome.
- ANSWER_TEXT / ANSWER.evidence_registry：Shows confidence labels and source types; EVID_004 is openly internal, while EVID_002/EVID_003 are marked high without E0 verification.

</details>

## Grok

答案SHA256：`6ad3212423155c29c5cb8d78a63f48c07ae0557a786ccb1f3297fe580bf91177`。

### D1 完整性与任务符合度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 7: answer supplies a coherent main route with two chemical steps, correct chosen_route_name, oxygen null, one organism profile with 15 trait entries, and evidence registry. It omits the gold S03 glycerol facilitator/entry transport step required by the 3-step task scope. Most required modules are present, but one necessary entry step is missing.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：States ordered_step_count=3 for the frozen case, supporting that S03 is within the required main-chain set; does not by itself prove answer chemistry.
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_049：Shows answer delivered only two steps and supplied 15 trait entries; does not show S03 transport.

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 8: S1 glycerol kinase phosphorylation and S2 quinone-dependent GlpD oxidation are directionally and stoichiometrically plausible, include ATP/ADP and quinone/quinol cofactors, and reach the gold terminal product DHAP. The missing S03 entry transport creates an entry/continuity gap; charge/stereo representation differences prevent 9-10.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：Supports directed conversions S01 and S02 and the terminal glycerone phosphate; does not cover the omitted S03 transport step.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_049：Supports glycerol as root and glycerone phosphate as terminal; does not prove answer&#x27;s cofactor specificity.
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_049：Shows the delivered two-step chemistry and cofactors; does not include S03.

</details>

### D3a 目标反应与酶对应：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 4: S1 glycerol kinase EC 2.7.1.30 and S2 aerobic glycerol-3-phosphate dehydrogenase EC 1.1.5.3 match accepted enzyme name/EC pairs at G4 curation granularity. The S03 KEY_ENTRY glycerol facilitator/entry step is absent from the answer, so D-KEY4 caps D3a at 4. glpK/glpD gene attributions remain minor unresolved claims.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_049：Supports accepted enzyme names/EC for S01/S02 and the S03 glycerol facilitator entry step; does not prove specific protein activity.
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_049：Shows S1/S2 enzyme names/EC and absence of S03; does not supply missing S03 enzyme/function.

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 7: the core organism is E. coli, and gold has E. coli species-level PATHWAY_COMPLETE support. The answer asserts strain K-12 MG1655/TaxID 511145 and assigns S02 to E. coli while the gold step organism row lists P. putida/S. cerevisiae. Species-level E. coli records support the strain-level claim only with a granularity gap; no verified contradiction, so no cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_049：Supports E. coli at species level for S01/S03 and PATHWAY_COMPLETE for E. coli 562; does not verify K-12 MG1655 strain-level TaxID 511145 or S02 step-level E. coli attribution.
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_049：Shows E. coli K-12 MG1655 used for both steps and complete_pathway claim; does not provide independent strain capability evidence.

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 7: many traits agree with E. coli species-level gold, including motility, rod morphology, Gram-negative, non-sporulation, non-halophilic salinity category, and oxygen tolerance. Temperature optimum 37 C, ATCC 700926, U00096, and several strain-specific numeric/genome subfields are not in frozen gold/E0; pH and genome size/GC are honestly null. No verified contradiction, but enough unresolved trait specifics to keep this at 7.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_049：Supports several E. coli species-level categorical traits; does not verify K-12 MG1655 strain-specific culture collection, genome accession, or optimum 37 C.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_049：Shows which E. coli trait fields are observed/scoreable vs completeness-only; does not turn unverified strain values into errors.
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_049：Shows the delivered 15 traits and explicit nulls; does not supply source records for unverified strain-specific values.

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 4: evidence_registry exists, but key pathway/enzyme groups rely on INTERNAL_KNOWLEDGE_ONLY entries with no record IDs (MISSING_SOURCE). TaxID 511145, ATCC 700926, and U00096 are identifier-level locators, but E0 is an evidence gap, so they remain UNRESOLVED_SOURCE rather than verified. No verified mis-citation, so no cap; traceability is weak but not absent.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_049：Shows delivered source types, database names, and locators; does not provide frozen records proving the claimed support.

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 6: the answer discloses several uncertainties and nulls (oxygen unspecified, stereochemistry not encoded, missing cofactor SMILES, missing numeric/genome data, no MetaCyc record ID). However many pathway/enzyme/trait claims rest on INTERNAL_KNOWLEDGE_ONLY evidence yet carry high confidence, so confidence partly exceeds evidence. Not systematic misrepresentation; no cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_049：Shows uncertainty disclosure and confidence labels; does not supply independent evidence for high-confidence internal-knowledge-only claims.

</details>

## GPT5.6

答案SHA256：`267474ed61c85a8ba5b9ae4ae18aea1b0fac0c09ea56213d5aaa318725a21141`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> route_scope.chosen_route_name 原样填写 glycerol degradation I，且 S1/S2 给出底物、产物、酶/EC 与微生物；但任务必答主链为 3 步，答案只交付 2 步，缺少 S03 甘油 facilitator/uptake 入口步。15 项性状虽按字段全部出现，但全部为 null/unknown 的占位，未提供实质性状内容。整体属于主要模块涉及但若干必要内容遗漏/仅占位，落在 5–6 档；因缺少一个关键入口步且性状模块无实质内容，取 5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：本题 ordered_step_count=3、LINEAR_UNIQUE，任务主链长度 3；不是要求全部旁支。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：必答步包含 S03 甘油 facilitator/uptake 入口步，且 S03-&gt;S01；答案未交付该步。
- ANSWER_TEXT / steps&#91;S1,S2&#93;; organism_profiles&#91;0&#93;.traits：答案实际只交付 S1/S2；15项性状字段存在但均为 null/unknown 占位。
- RUBRIC_CLAUSE / P45：诚实填写 null/unknown 仍反映完成度不足，D1 按完成度评定。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1 甘油经甘油激酶生成 sn-glycerol 3-phosphate，S2 sn-glycerol 3-phosphate 经 glycerol-3-phosphate dehydrogenase (quinone) 生成 dihydroxyacetone phosphate，主有机转化、方向与题面终点（glycerone phosphate/DHAP）一致，未见核心化学反转、原子明显不守恒或无依据跳步。主要缺陷是未列 ATP/ADP 与 quinone/quinol 辅因子，且电荷/立体表示简化；按 P103 属局部计量/表达缺陷，D2 保持在 7–8 档。S03 转运入口缺失已在 D1/D3a 处理，不另作 D2 化学错误。取 8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：S01 甘油-&gt;sn-glycerol 3-phosphate；S02 sn-glycerol 3-phosphate-&gt;glycerone phosphate；方向为 substrate_to_product。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_049：终点为 Glycerone phosphate(2-)；答案产物 DHAP 对应同一终点。
- ANSWER_TEXT / steps&#91;S1,S2&#93;：答案化学主链两步；未列辅因子。
- RUBRIC_CLAUSE / P103：主有机物转化正确但辅因子遗漏通常属局部计量缺陷，D2 在 7–8 档内处理，不自动 cap。

</details>

### D3a 目标反应与酶对应：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1 glycerol kinase / EC 2.7.1.30 与 S2 glycerol-3-phosphate dehydrogenase (quinone) / EC 1.1.5.3 均与本题 accepted 酶名/EC 集合在 G4 功能粒度上匹配；glpK/glpD 仅为可选 gene 归属，按 MINOR 未核处理，不推翻已匹配的目标功能。关键问题是必答 KEY_ENTRY 步 S03（glycerol facilitator/uptake）完全未交付，target S03=MISSING。按 C04/D-KEY4，已确认 KEY 的实证交付缺失触发 4 分上界；两个已交付酶对应清楚且正确，支持取受限范围上沿 4，不再升高。此处 4 是 D-KEY4 遗漏上界，不是已签署的 D3a 酶名/EC 矛盾 key_error。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_049：S01 glycerol kinase EC 2.7.1.30；S02 EC 1.1.5.3 的 accepted 酶行；仅支持功能/EC 粒度，不证明具体蛋白实验活性或整路菌能力。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_049：S03 为甘油 facilitator/uptake 入口步；答案无该步交付。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_049：必答主链 ordered_step_count=3，S03 为任务范围一部分。
- ANSWER_TEXT / steps&#91;S1,S2&#93;：答案仅提交两个酶步；S03 目标缺失。
- RUBRIC_CLAUSE / D-KEY4：已确认 KEY 的合法已核 F 或实证交付 M 触发 D3a 4 分上界；上界不代签 key_error=Y。
- RUBRIC_CLAUSE / C04：KEY 实证遗漏保留 4 分上限；U/表示待核不自动抹去已确认漏答。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> E. coli species identity is compatible with the gold S01 E. coli row and PATHWAY_COMPLETE E. coli=true. The answer uses one E. coli K-12 MG1655 profile for all steps; strain-level TaxID 511145 and S02 step-level E. coli are not directly present in the frozen slice, so within-grade deduction gives 7 rather than cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_049：Supports E. coli 562 at S01 and whole-pathway E. coli=true; does not contain TaxID 511145/K-12 MG1655 or an S02 E. coli step row.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 required traits are present only as null/unknown with no trait evidence. Under P44/D4 missing rule, this is D4=MISSING=1, not a scored scientific-error judgment.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：Shows all 15 trait slots are null/unknown with no delivered trait values or trait sources.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All evidence_registry entries are source_type INTERNAL_KNOWLEDGE_ONLY with null database, record_id, and locator. This is MISSING_SOURCE, not verified mis-citation; the low 1-2 band applies and 1 is chosen because no important conclusion has a locatable delivered source.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows all delivered source records are INTERNAL_KNOWLEDGE_ONLY with no database/record/locator, so claims are not independently traceable.

</details>

### D6 不确定性与诚实度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer discloses that oxygen was unspecified and that trait sources were not provided, which is honest. However, enzyme and organism claims carry high confidence while all evidence is INTERNAL_KNOWLEDGE_ONLY; uncertainty disclosure is present but insufficiently calibrated, placing it in the 5-6 band and taking 5.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows limited uncertainty disclosure: oxygen unspecified and trait sources absent; does not calibrate high-confidence internal-only enzyme/organism claims.

</details>
