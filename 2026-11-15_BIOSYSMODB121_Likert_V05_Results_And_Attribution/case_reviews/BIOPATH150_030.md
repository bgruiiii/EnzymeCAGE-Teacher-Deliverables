# BIOPATH150_030：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：D-galactonate degradation

污染物：D-galactonate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 47 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 67 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 76 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 72 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 69 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 37 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`25c9fad0a6f9baa2fe070fef1883471b6056faa1fa293291fa6001b98732df7d`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 交付完整：3步、1个去重菌profile、15项性状、证据与不确定项均已给出，且route_scope.chosen_route_name原样填写。但答案把冻结线性主链替换为非磷酸化dgo变体，S2先醛醇裂解、S3再用D-glyceraldehyde kinase，未按gold S01激酶→S03磷酸化醛醇裂解交付；属任务路线偏离。按D1任务偏离cap≤4，结合完整度取4。

<details><summary>V0.4理由与本行变化背景</summary>

全部必需模块交付：3步齐备，每步含主底物/主产物英文名+SMILES、首选酶名+EC、对应微生物；route_scope.chosen_route_name原样填&#x27;D-galactonate degradation&#x27;未改选；organism_profiles按物种+菌株去重为1条(E. coli K-12);15项性状全部出现；evidence_registry与uncertainties均交付。扣分点：题面要求&#x27;各项最强来源&#x27;，但来源全部为INTERNAL_KNOWLEDGE_ONLY、无外部可定位记录，来源子项未实质满足。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：显示gold主链为S02脱水、S01激酶、S03磷酸化醛醇裂解的有向顺序；支持答案路线顺序与gold不同，不单独证明替代化学全部不可行。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：显示S01为2-dehydro-3-deoxygalactonokinase、S03为2-dehydro-3-deoxy-6-phosphogalactonate aldolase；支持目标酶步与答案S2/S3不同。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 首步D-galactonate脱水生成2-dehydro-3-deoxy-D-galactonate与gold S02一致，主有机物可连到pyruvate/G3P。但答案先以EC 4.1.2.21醛醇裂解非磷酸化中间体生成pyruvate+D-glyceraldehyde，再用EC 2.7.1.28磷酸化D-glyceraldehyde，未按gold S01激酶→S03磷酸化醛醇裂解；关键中间体6-phosphate和酶步顺序需实质修订。属5-6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

化学转化在名称/酶/逻辑层面成立：脱水(D-galactonate→2-dehydro-3-deoxy-D-galactonate+H2O)、醛醇裂解(→pyruvate+D-glyceraldehyde)、甘油醛+ATP磷酸化(→D-glyceraldehyde-3-phosphate+ADP)，反应类型与方向正确，终点与gold terminal(pyruvate+G3P)一致；属E. coli真实非磷酸化dgo分支，答案主动声明路线边界(§4.5第3步有声明但无可核外部证据，按&#x27;不判错也不给高分&#x27;处理)。但关键中间体&#x27;2-dehydro-3-deoxy-D-galactonate&#x27;的SMILES(OC&#91;C@@H&#93;(O)&#91;C@H&#93;(O)CC(=O)&#91;O-&#93;)经核对为5碳且缺C2酮基，与其名称(C6)及S2产物(C3+C3=C6)碳数不自洽，关键中间体结构需修订。落5–6档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：gold S02支持D-galactonate→2-dehydro-3-deoxy-D-galactonate；gold S01/S03显示答案缺少6-phosphate中间体和对应醛醇裂解产物。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：gold S01激酶EC 2.7.1.178与S03醛醇裂解EC 4.1.2.55|4.1.2.21支持目标酶步；不自动证明答案替代酶在E. coli K-12中负责该步。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：官方EC 4.1.2.55反应为2-dehydro-3-deoxy-6-phospho-D-galactonate→pyruvate+D-glyceraldehyde 3-phosphate；不支持答案S2用非磷酸化底物生成D-glyceraldehyde。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> 程序事实为S=0、F=1、U=2；S01为已确认KEY失败，D-KEY4上限4。目标S01激酶步被S2醛醇裂解替代，S03磷酸化醛醇裂解未交付；S1脱水反应虽与gold S02化学相近，但S02/S03仍为UNKNOWN/ALIGNMENT_NOT_CONFIRMED，不能计S。核心目标主链失效，仅少量局部信息有用，取2。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名-EC-反应类型互相一致：D-galactonate dehydratase/DgoD=EC4.2.1.6(裂合脱水)、2-dehydro-3-deoxy-D-galactonate aldolase/DgoA=EC4.1.2.21(裂合醛缩)、D-glyceraldehyde kinase/DgoK=EC2.7.1.28(转移酶磷酸化)，无EC大类与反应类型错配(§八.D3a)；EC4.2.1.6与gold脱水酶一致。EC4.1.2.21官方accepted name为2-dehydro-3-deoxy-D-gluconate aldolase(葡糖酸型)，用于半乳糖酸型醛缩酶存底物构型疑点，但答案已在uncertainties如实披露、非隐瞒；EC2.7.1.28自述凭内部知识。三EC在E0均无冻结记录(GAP-030-010/012/013)保持UNRESOLVED，不判错不判虚构。档内取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：S01目标酶为2-dehydro-3-deoxygalactonokinase EC 2.7.1.178；S03为2-dehydro-3-deoxy-6-phosphogalactonate aldolase EC 4.1.2.55|4.1.2.21；支持答案未命中S01/S03关键目标酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：S01要求2-dehydro-3-deoxy-D-galactonate+ATP→6-phosphate；S03要求6-phosphogalactonate→pyruvate+G3P；支持答案S2/S3目标反应缺失或替代。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：EC 4.1.2.55官方反应使用6-磷酸半乳糖酸型底物；不支持答案S2在非磷酸化中间体上使用醛醇裂解作为目标S03反应。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> gold organism_gold对S01/S02/S03均列Escherichia coli，且PATHWAY_COMPLETE对E. coli为TRUE；答案用E. coli K-12 MG1655并统一到一个profile。物种级与全路径推荐有支持，主要微生物推荐未被推翻。但菌株级TaxID 511145/NC_000913未在gold/E0直接核验，且S2 EC 4.1.2.21、S3 EC 2.7.1.28在E. coli K-12中的单步能力无冻结证据；属合理候选+部分支持、若干关键条目待核，5-6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份E. coli与gold一致：gold organism_gold对S02/S03步均为Escherichia coli(TaxID562)，且PATHWAY_COMPLETE(E. coli,562,TRUE)支持E. coli完成半乳糖酸整条降解的能力；答案三步均归E. coli、complete_pathway_organism_profile_id=ORG_001，与gold种级身份及路径能力一致。但答案用菌株级K-12 MG1655/TaxID511145/ATCC700926，E0无菌株级冻结记录(仅种级562)，属物种级记录支持菌株级声称的粒度不足档(§八.D3b①)，档内扣、默认不cap；未用无关类群或异菌株，不构成身份错配。取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_030：gold列出E. coli TaxID 562覆盖S01/S02/S03，并PATHWAY_COMPLETE TRUE；支持E. coli物种级/全路径主推荐，不支持K-12 MG1655菌株级身份或替代酶步能力。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：提供E. coli物种级性状背景；不支持菌株K-12 MG1655的TaxID 511145/NC_000913核验。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 多数性状与gold E. coli物种级记录一致：F1兼性厌氧、F4非嗜盐、F10运动、F11杆状、F12革兰阴性、F13不产孢均有支持；F2偏好中温、F3 pH与F7碳源利用大体合理。局部问题：F2最适37°C、F5 ATCC 700926、F14 NC_000913/4,641,652 bp/50.8%、F15栖息地概括缺少冻结记录直接核验；F9把DgoK写成D-glyceraldehyde kinase存在局部科学问题。按局部未核不改主要7分带。

<details><summary>V0.4理由与本行变化背景</summary>

性状与gold种级E. coli记录多项吻合(trait_gold对照)：F1兼性厌氧(facultative anaerobe=true)、F12革兰氏阴性(gram positive=false/gram negative=true)、F11杆状(rod-shaped)、F13不产孢(sporulation=false)、F10可运动(motility=true)均SUPPORTED；F4非嗜盐(non-halophilic)一致；F8缺广谱污染物降解能力与gold(degradation aromatic/hydrocarbon=false)一致。但F5(ATCC700926)、F14(NC_000913/4,641,652bp/50.8%GC)、F2最适37℃、F3最适pH7.0等菌株级/定量值为内部知识、E0无对应冻结记录(GAP-030-029至039)未核验，仅可判为对E. coli生物学的合理值。主要性状可核实且适用，局部定量/菌株级值待核，档内取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：支持E. coli物种级F1/F4/F10/F11/F12/F13等分类性状；不直接核验K-12 MG1655的F2最适值、F5 ATCC号、F14 NC_000913或F15概括。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_030：标明E. coli F2 min/max、F3 pH、F4 salinity等子字段存在待裁定/完整度口径；支持D4按局部字段谨慎处理，不把字段填写率机械换分。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_030：显示E. coli F2/F3/F4部分端点属pending_teacher_adjudication或completeness_only；支持不将未裁定端点作为已核实数值。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> EVID_001、EVID_002、EVID_003均登记为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为null；核心路线、酶-EC、微生物身份、性状等决策相关组均为MISSING_SOURCE。答案有内部evidence_id与claim_scope，但无法定位到外部记录或文献；未发现已核实错引，不触发D5 cap。可追溯性几乎不可定位，按低分档给2。

<details><summary>V0.4理由与本行变化背景</summary>

来源全部为INTERNAL_KNOWLEDGE_ONLY自声明：evidence_registry三条(EVID_001/002/003)的source_type=INTERNAL_KNOWLEDGE_ONLY、database与record_id均null、locator null，无任何可定位文献/数据库条目/计算记录，核心结论无法追溯，属§4.3 MISSING_SOURCE低分档。这是缺失而非误导，无任何已核实错引，默认不cap。答案的EC4.2.1.6/4.1.2.21/2.7.1.28、TaxID511145、基因组NC_000913等在E0无记录(GAP-030-006/010/012/026/029-039)，保持UNRESOLVED待核，不判虚构、不判CONTRADICTED。取2档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案明确标注INTERNAL_KNOWLEDGE_ONLY，列出DgoA/DgoK EC待核、ATCC/NC_000913未核、氧条件null，并给出多条具体不确定性，未把全部内容伪装成实验观测。但部分内部知识仍标high confidence（S1、菌株归因、F11-F13等），属单点过度确信而非系统性误导；主要限制已说明，给7。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties与各步uncertainty具体诚实：明确指出EC4.1.2.21底物构型(葡糖酸型vs半乳糖酸型)疑点、EC2.7.1.28凭内部知识未核、全部证据为内部知识且无记录号/文献定位、氧条件null对路线适用范围的影响，属具体披露(§八.D6正面)。但多处步级/性状confidence标&#x27;high&#x27;(如S1酶、F1/F6/F11/F12/F13性状)与&#x27;仅内部知识、无外部核验&#x27;的证据强度不完全相称，属单点过度确信而非系统性误导(§八.D6)，档内扣、不cap。取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`cab7508f607e7e5296500e114903ff6763ceaa2eee3ea03efd31e7570f207971`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案按题面指定的 D-galactonate degradation 主链给出3步，逐步包含主底物/主产物英文名与SMILES、首选酶及EC、对应微生物；同一菌 Escherichia coli K-12 substr. MG1655 去重为单一profile，15项性状均按展示顺序出现。未发现指定路线改选或必须模块缺失；少量性状为显式null/unknown（如F10、F4盐度），但题面允许未知填null，属轻微完整度问题，故9而非10。

<details><summary>V0.4理由与本行变化背景</summary>

全部要求模块均已实质交付：三步主链、逐步主底物/产物含SMILES、每步一酶+EC、一微生物、15项性状槽位齐备、证据登记表就位；chosen_route_name原样回显题面。仅F4盐度、F10运动性为诚实null（任务明示不确定填null），属少量遗漏，无范围偏离或路线改选。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_030：支持路线名称为D-galactonate degradation、终点为pyruvate与D-glyceraldehyde 3-phosphate；不证明答案所有细节正确
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_030：冻结案例为LINEAR_UNIQUE、ordered_step_count=3；用于核对主链必要步数为3，不把旁支并入分母
- ANSWER_TEXT / cab7508f607e7e5296500e114903ff6763ceaa2eee3ea03efd31e7570f207971：答案实际交付3步、单一去重profile及15项性状字段

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 三步主转化与冻结gold主链一致：D-galactonate脱水生成2-dehydro-3-deoxy-D-galactonate；ATP依赖磷酸化生成2-dehydro-3-deoxy-D-galactonate 6-phosphate；醛缩裂解生成pyruvate与D-glyceraldehyde 3-phosphate。方向均为底物到产物并到达题面/gold终点。局部问题为S1未列H2O、S2未列H+，以及SMILES未表达立体化学；按P103/P104属局部计量/表示缺陷，不推翻主链，故7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

三步化学与gold reaction一致：S1 D-galactonate脱水→2-dehydro-3-deoxy-D-galactonate；S2 ATP依赖磷酸化→6-磷酸+ADP（正确纳入ATP/ADP辅因子）；S3醛缩裂解→pyruvate+D-glyceraldehyde 3-phosphate，方向与连接正确、终点合规。仅S1未列H2O、SMILES未标立体化学（属简化表达，非计量失衡），据辅因子/简化条款为局部小缺陷，不改主链结论。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：支持gold主链三步的底物、产物、方向与连接；不自动支持答案省略的辅因子/立体化学细节
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_030：支持题面路线终点为Pyruvate与D-glyceraldehyde 3-phosphate(2-)
- ANSWER_TEXT / cab7508f607e7e5296500e114903ff6763ceaa2eee3ea03efd31e7570f207971：答案实际给出的三步化学转化、方向与SMILES
- RUBRIC_CLAUSE / P103：主有机物转化正确但辅因子遗漏通常按局部计量缺陷在7–8档处理，不自动cap

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 三步首选酶与accepted集合基本对应：S1 D-galactonate dehydratase/EC 4.2.1.6，S2 2-dehydro-3-deoxygalactonokinase/EC 2.7.1.58，S3 2-dehydro-3-deoxygalactonate 6-phosphate aldolase/EC 4.1.2.55。enzyme_gold/accepted集合覆盖这些名称与EC；E0对EC 4.1.2.55的accepted name/reaction支持S3功能级对应。未发现已核目标失败或漏答；但EC 4.2.1.6、2.7.1.58官方冻结记录缺口、表示等价(stereo blind)待裁定及dgoD/dgoK/dgoA基因归属待核，使名称—显式EC配对与支持范围尚未达到8档的充分清楚，故7。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名-EC-功能与gold一致：S1 D-galactonate dehydratase EC 4.2.1.6(dgoD)、S2 2-dehydro-3-deoxygalactonokinase EC 2.7.1.58(dgoK)、S3 6-磷酸醛缩酶 EC 4.1.2.55(dgoA)，均落在gold对应步骤EC多注集合内；S3的EC 4.1.2.55经E0核实accepted name与reaction相符。S1/S2的EC在E0无冻结记录，属局部未核（不判错、不降整维）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：列出目标步的accepted酶名与EC（含4.2.1.6、2.7.1.58、4.1.2.55等）；仅支持功能级酶—反应对应，不证明具体蛋白实验活性或菌株能力
- E0_EVIDENCE / f3e0:ec:4.1.2.55：EC 4.1.2.55的accepted name/reaction含2-dehydro-3-deoxy-6-phospho-D-galactonate = pyruvate + D-glyceraldehyde 3-phosphate，支持S3功能级对应；不外推具体蛋白或菌株能力
- ANSWER_TEXT / cab7508f607e7e5296500e114903ff6763ceaa2eee3ea03efd31e7570f207971：答案实际给出的酶名、EC与可选基因归属
- RUBRIC_CLAUSE / C05：7–8档内选择：主要目标催化对应可靠但名号配对/支持边界尚需局部修订时取7

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> gold三步步级记录均以Escherichia coli物种级条目支持；答案统一用E. coli K-12 MG1655并给出TaxID 511145，E0无511145记录，按D3b身份阶梯①物种级支持菌株级声称，档内扣不cap；完整路径能力有E. coli PATHWAY_COMPLETE物种级支持但菌株级待核。

<details><summary>V0.4理由与本行变化背景</summary>

推荐菌Escherichia coli（K-12）与该路径三步骤归属一致；gold为E. coli(562)在S01/S02/S03均有匹配酶记录且PATHWAY_COMPLETE=TRUE，支持其为完整路径菌，未把单步菌写成整条路径菌。身份采用菌株级TaxID 511145，与所声称菌株K-12 MG1655粒度一致（物种级与菌株级不冲突），但E0无该TaxID记录，属局部未核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_030：三步步级记录支持Escherichia coli物种级归属及PATHWAY_COMPLETE=true；不核实K-12 MG1655菌株级TaxID 511145。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_030：支持该路径为LINEAR_UNIQUE且E. coli可作路径菌的物种级参照；不支持所有具体菌株。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> F1/F11/F12/F13等有E. coli物种级观测支持；F2 optimum 37、F3 optimum 7.0、F5 ATCC 47076、F14 U00096.2、F15栖息地描述未在E0直接核验。按同物种代表记录口径，不因答案菌株与代表株不同自动判错；关键项多数可支持，部分菌株级/最适值待核，取7档。

<details><summary>V0.4理由与本行变化背景</summary>

关键定性性状与gold一致且适用：F1兼性厌氧、F11杆状、F12革兰氏阴性、F13不产芽孢、F2温度偏好嗜中温，均可由trait_gold代表记录支持；F7/F8称可利用并降解D-半乳糖酸与gold完整路径一致。F5保藏号(ATCC 47076)、F14基因组(U00096.2/4641652bp/50.8%)、F2最适37℃、F3最适pH7.0等数值/身份项在E0无记录，属局部未核；F4盐度、F10运动性为诚实null（完整度缺口，非错误）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：E. coli 562物种级记录支持兼性厌氧、杆状、革兰氏阴性、不产孢、运动性及多类碳源/酶活；不直接核实K-12 MG1655菌株级F2/F3/F5/F14/F15。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_030：标明E. coli若干性状可评分及子字段边界；不把物种级记录升级为菌株级观测。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_030：标明F2/F3/F4等子字段待裁定或仅完整性，不用于数值精度强制。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> 核心步骤、酶/EC、微生物归属的EVID_001-EVID_004均为INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE；仅EVID_005/006为DATABASE_DIRECT但E0未核。重要结论几乎不能沿外部条目核查，落D5低档。无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（路线CG01/02/03、酶CG05、菌身份CG07、整路径CG09）的支撑几乎全部为INTERNAL_KNOWLEDGE_ONLY（EVID_001–004）=MISSING_SOURCE，核心结论无法从答案自身追到可定位条目；仅基因组U00096.2(EVID_005)与ATCC 47076(EVID_006)给出DATABASE_DIRECT记录ID，但E0无法核其内容=UNRESOLVED_SOURCE。无已核实错引（无CONTRADICTED），按P41决策相关组缺失/待核→低分档、默认不cap，档内取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：gold可作酶名/EC参照，但不能回填答案原交付来源，不能提升D5。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_030：gold可作E. coli物种级身份参照，但不证明答案已交付可定位来源。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：可核部分物种级性状，但答案核心路径来源仍缺。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：仅一条EC官方事实，不能覆盖三步路径、菌株与性状来源。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案用INTERNAL_KNOWLEDGE_ONLY标示部分证据性质，并对F4/F10等未知填null；但多处菌株级/最适值/来源字段用medium或high confidence包装，uncertainties为空，未系统说明表示边界与待核点。属部分披露、仍有过度确信，取6档，不判系统性误导。

<details><summary>V0.4理由与本行变化背景</summary>

字段级confidence存在（酶/菌medium、null项unknown，2项诚实null），有一定不确定性标注；但多项纯INTERNAL_KNOWLEDGE_ONLY的性状（F1/F6/F11/F12/F13）标high，且uncertainties数组为空、全篇无限制或观测/预测/未知的显式说明，部分结论强度超过依据。属单点/多点过度确信而非系统性把预测写成实证、无掩盖已知矛盾，故档内扣不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：可核对答案自报的confidence、source_type与uncertainties字段。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：对照物种级性状支持范围，判断答案披露是否与证据强度相称；不回填答案来源。

</details>

## Kimi

答案SHA256：`d5eca0df54df4bea18deaf1be6333e775af831e1c0fc51d7f261c8bdc60f0bd8`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案结构完整且可解析；主链三步覆盖D-galactonate→2-dehydro-3-deoxy-D-galactonate→6-phosphate→pyruvate+D-glyceraldehyde 3-phosphate，每一步给出主底物/主产物、SMILES、首选酶/EC和对应E. coli；同一菌只保留一个organism_profile；route_scope.chosen_route_name原样为D-galactonate degradation；15项性状全部出现。少量性状子字段为null/未知，但按题面属于允许的明确未知，不构成模块遗漏，故D1取9。

<details><summary>V0.4理由与本行变化背景</summary>

主链3步全部实质作答（每步均给底物/产物英文名+SMILES、首选酶名+EC、对应菌），route_scope.chosen_route_name逐字填写题面路线名&#x27;D-galactonate degradation&#x27;，未改选路线；同一菌（E. coli K-12 MG1655）三步去重为单条ORG_001，15项性状全部出现且带raw_text/evidence_id/confidence；JSON完整可解析。扣分点：S2为ATP依赖磷酸化，但substrates/products数组未按题面第8条把ATP/ADP（及脱水步H2O）作为cofactor/byproduct返回，属交付字段局部遗漏（P105），不是科学错误，不据篇幅或术语加分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求指定路线下3步主链、每步主底物/产物英文名与SMILES、一个首选酶及EC、一个对应微生物；并填写15项性状及最强来源。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_030：gold正式案显示本题为LINEAR_UNIQUE、ordered_step_count=3，支持必答主链边界为3步；不表示全DAG所有旁支均须交付。
- ANSWER_TEXT / ANSWER_BEGIN：答案实际交付3步、1个E. coli profile、15项性状及证据登记；不证明其科学内容正确。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链方向和化学连续性成立：S1脱水生成2-dehydro-3-deoxy-D-galactonate，S2在C6磷酸化生成6-phosphate，S3醛裂解为pyruvate与D-glyceraldehyde 3-phosphate；底物/产物SMILES与这些转化相容，方向为substrate→product，未见主链第一步错、方向反转或明显原子/氧化还原断裂。S2只列主有机底物/产物而未列ATP/ADP，属于局部辅因子/计量信息省略；按辅因子条款通常落在7–8档而非cap，故取8而非9–10。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步一致：S1 D-galactonate→2-dehydro-3-deoxy-D-galactonate（脱水，方向forward，与gold order1/S02一致）；S2→2-dehydro-3-deoxy-D-galactonate 6-phosphate（激酶磷酸化，与gold order2/S01一致）；S3醛裂解为pyruvate+D-glyceraldehyde 3-phosphate，与case_root_identity的terminal两产物完全一致，止于题面指定终点，无多余下游延续。所给SMILES连通性与gold canonical结构一致（C6羧酸骨架、C3脱氧、C6磷酸）。局部缺陷：未把ATP/ADP/H2O列入反应参与者，属辅因子遗漏的局部计量缺陷（P103，7–8档内处理），不构成关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：逐金标反应给出S02 D-galactonate→2-dehydro-3-deoxy-D-galactonate、S01→6-phosphate、S03 6-phosphate→pyruvate+D-glyceraldehyde 3-phosphate的有向主链；支持主链方向与终点，不证明答案全部辅因子已列全。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：gold酶行列出脱水酶、激酶和醛缩酶对应的反应/酶条目；支持反应类型，不自动证明具体蛋白实验活性。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：官方EC条目记录2-dehydro-3-deoxy-6-phospho-D-galactonate→pyruvate+D-glyceraldehyde 3-phosphate的醛裂解反应；支持S3反应方向/产物，不扩展到未声称的菌株或实验活性。

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 按答案步骤与必答目标反应对齐：S1的D-galactonate dehydratase/EC 4.2.1.6命中目标S02的accepted name/EC集合；S2的2-dehydro-3-deoxygalactonate kinase/EC 2.7.1.58命中目标S01的accepted name/EC集合；S3的2-dehydro-3-deoxy-6-phosphogalactonate aldolase/EC 4.1.2.21命中目标S03的accepted name/EC集合。三者均为G4策展/接受集合粒度，功能级目标反应可支持；dgoD/dgoK/dgoA仅为可选基因归属且未核，属MINOR局部未核，不改变目标功能信用。受本题D3a允许范围&#91;1,8&#93;及高档次门限制，取8。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名与EC均落在gold多注集合内：4.2.1.6∈{4.2.1.140,4.2.1.6}（S02）、2.7.1.58∈{2.7.1.178,2.7.1.58}（S01）、4.1.2.21∈{4.1.2.55,4.1.2.21}（S03），且基因名dgoD/dgoK/dgoA与E. coli对应关系与酶功能一致；按四.5多注条款，选集内编号不扣分。E0仅含EC 4.1.2.55条目，其accepted name与reaction已覆盖&#x27;2-dehydro-3-deoxy-6-phospho-D-galactonate = pyruvate + D-glyceraldehyde 3-phosphate&#x27;的醛裂解反应，支持该步反应类型；但答案所写4.1.2.21及4.2.1.6、2.7.1.58的条目状态在冻结证据中无记录（GAP-030-009/012/007），故以局部未核登记、不据此降为NE。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：gold酶行包含S01 2.7.1.58、S02 4.2.1.6、S03 4.1.2.21等accepted/同工酶条目；支持酶名—EC与目标反应的功能级匹配，不证明具体蛋白实测活性。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：EC 4.1.2.55条目的reaction明确包括2-dehydro-3-deoxy-6-phospho-D-galactonate→pyruvate+D-glyceraldehyde 3-phosphate；支持S3醛缩酶反应功能，不把该条目自动扩展为EC 4.1.2.21的完整官方身份核验。
- ANSWER_TEXT / ANSWER_BEGIN：答案逐酶交付name、EC和可选gene_or_protein；支持定位所评的具体酶/EC声称，不证明所有来源支持关系均已在E0核实。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 答案三步均用Escherichia coli K-12 substr. MG1655，物种E. coli与gold organism_gold的E. coli主链一致，且gold对E. coli给出PATHWAY_COMPLETE=TRUE，可支持E. coli物种级主链归属。但答案进一步声称K-12 MG1655（TaxID 511145）为该路径的完整路径菌，gold organism_gold只给到E. coli物种/562级，E0对511145为GAP，未核；这属于物种级/真实同lineage记录支持菌株级或全路径能力声称，按D3b身份阶梯档内扣至7，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

Escherichia coli 在organism_gold中同时对应S01、S02、S03三步酶，并有PATHWAY_COMPLETE=TRUE（taxid 562）记录，故物种级身份、步级归属与整条路径能力均有gold支持，不属于跨类群/编造。加分上限未取9–10的原因：答案把全部步骤与性状绑定到菌株K-12 substr. MG1655，其ncbi_taxid 511145与ATCC 700926在冻结证据中无记录（GAP-030-002/003/026），性状又以BacDive DSM 30083（species/type strain）代表记录支撑——属&#x27;物种级/代表记录支持菌株级声称&#x27;的粒度问题（P107①，档内扣、默认不cap），且菌株级能力本身尚待核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_030：gold逐步骤列出E. coli作为S01/S02/S03对应微生物，且PATHWAY_COMPLETE行显示E. coli 562 pathway_complete=TRUE；支持E. coli物种级主链归属，不直接核验K-12 MG1655菌株级身份/能力。
- ANSWER_TEXT / ANSWER_BEGIN：答案实际把同一E. coli K-12 MG1655 profile绑定到三步并声明complete_pathway_organism_profile_id；支持定位被评的菌株级/全路径能力声称。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 多数性状与gold E. coli物种/代表记录相容：F1兼性厌氧、F4非嗜盐类别、F10运动、F11杆状、F12革兰氏阴性、F13不产芽孢、F14基因组大小/GC落在E. coli范围。主要问题是解释/粒度：F2把ATCC的growth temperature 37°C写成optimum_c=37，按D-TRAITS培养温度不等于最适温度；F3把pH 7.0列为optimum而非已核范围；F15的广适栖息地描述在gold F15为UNKNOWN且E0未核。多数性状可用但存在数个条件/解释问题，落在7–8档下沿，取7。

<details><summary>V0.4理由与本行变化背景</summary>

性状与gold物种级观测总体一致：F1兼性厌氧（aerotolerant/facultative anaerobe=true）、F10可运动、F11杆状、F12革兰氏阴性、F13不产芽孢、F4非嗜盐（salinity preference=non-halophilic）、F3 pH 7.0落在gold pH growth 7.0–8.5内、F14 4,641,652 bp与GC 50.8%落在gold物种级范围（1.22–7.62 Mb、40.2–63.0%）内，无被反驳的离谱值；盐度数值与pH端点为诚实null。扣分项：F2把&#x27;Growth conditions: temperature 37 °C&#x27;（培养温度）直接填为optimum_c并给high置信，违反测量语义纪律（P113：培养温度不等于最适温度；该子字段在mask中为completeness_only/无观测源）；F5 ATCC 700926、F14菌株级数值与TaxID均无冻结记录，且多项high置信建立在species/type strain代表记录上，未区分&#x27;代表株推断&#x27;与&#x27;菌株级观测&#x27;。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：gold E. coli性状行支持兼性厌氧、运动、杆状、革兰氏阴性、不产芽孢、非嗜盐类别及基因组大小/GC范围等；不提供K-12 MG1655菌株特异数值，也不把培养温度自动当作最适温度。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_030：列出E. coli温度/pH/盐度等子字段的可评分性与待裁决状态；支持区分observed_accuracy与completeness_only，不把未冻结范围策略当作已核数值。
- ANSWER_TEXT / ANSWER_BEGIN：答案逐项给出15项性状、raw_text、evidence_id和confidence；支持定位F2/F3/F14/F15等具体声称。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案确实交付了evidence_registry并为步骤/性状逐项绑定evidence_id：路线用MetaCyc pathway名，酶用EcoCyc dgoD/dgoK/dgoA记录，身份用NCBI Taxonomy 511145，基因组用GCF_000005845.2/NC_000913.3，性状多用BacDive DSM 30083。部分关键结论有可定位数据库名/locator/record_id，能达到5–6档；但EVID_001/EVID_002无稳定record_id，EVID_003/004/005/006虽有条目但不在E0冻结记录中，且EVID_006为DSM 30083代表记录，不能完整支持K-12 MG1655所有菌株级性状。未发现已核实错引，故不cap；因多个决策相关组仍为UNRESOLVED_SOURCE，不能进入7–8档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付6条DATABASE_DIRECT证据并与claim_scope逐条映射，其中身份/保藏/基因组/生理四类给出可定位记录号（TaxID 511145、ATCC 700926、BacDive DSM 30083、GCF_000005845.2/NC_000913.3），优于&#x27;只给库名&#x27;；但决策相关组仍有缺口：路线（CG01–CG03）只给MetaCyc通路名、酶-EC（CG05）只给dgoD/dgoK/dgoA基因名描述，均无record_id，且全部关键引用在冻结证据中无记录（GAP-030-002/003/004/007/009/012/024），引用-声称链一律UNRESOLVED，无法核对实际支持内容；F4盐度类别无来源（MISSING_SOURCE）。E0唯一相关条目为EC 4.1.2.55，答案并未引用该编号，只能支持该步反应类型存在。按四.3/P41：无已核实错引，条目级可定位与笼统并存→5档；不因内容正确而抬档，也不因未核判为错引或cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：答案实际交付6条evidence_registry及逐项evidence_id绑定；支持评价其来源交付形态，不证明被引记录真实支持全部声称。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：E0仅含EC 4.1.2.55一条官方事实；其余EVID_001-EVID_006所涉TaxID 511145、ATCC 700926、BacDive DSM 30083及多个EC在E0为GAP或未提供，不能据此判支持。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：gold性状行可作为部分E. coli物种级性状的事实核验参照，但不等于答案所引EVID_006条目已被E0冻结；不回填为答案原来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案有专门uncertainties说明：氧条件题面未指定，主链按E. coli代表性磷酸化路线；盐度/pH生长上下限缺乏菌株特异强来源，故只填可支持的最适/类别或留空。逐性状confidence有high/medium/low区分，F4用low且未冒充观测，F6/F15用medium，未系统性把预测写成实证。存在少量单点过强：F2把growth temperature写成optimum并标high，F5/F14等菌株级记录confidence=high但E0未核；这属于档内扣分而非系统性误导，故D6取8。

<details><summary>V0.4理由与本行变化背景</summary>

有不确定性披露但偏薄：uncertainties仅两条（氧条件未指定、盐度/pH上下限缺菌株特异来源），且逐项性状带confidence与raw_text、F4以low+null诚实留空，这些是正向要素；扣分在于证据性质标注不足——酶/通路以high置信包装但引用条目在冻结证据中均不可核，F2把培养温度当最适值仍标high，代表株记录被用于菌株级性状而未说明&#x27;代表记录/推断&#x27;性质，属单点（多项同源）过度确信而非系统性掩盖矛盾（未见已知矛盾被掩盖，亦未把预测写成实证观测）。按P119档内扣分、不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：答案交付uncertainties数组及逐项confidence/raw_text，支持评价其证据性质与不确定性披露质量。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：gold显示E. coli温度/pH/盐度等为范围或多来源性状，且F15为UNKNOWN；支持检查答案是否把培养温度/代表记录过度确认为最适值或菌株级观测。

</details>

## Qwen

答案SHA256：`24ddea3e814f2f9833aad396292176a608d7585e9b155d1c3fbf5a0e91762bd1`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> All three required steps are present with substrate/product names, SMILES for main species, enzyme/EC and microorganism mapping; route_scope.chosen_route_name is exact; all 15 trait fields are present, with two explicit null/unknown entries. Minor omissions are limited to cofactor SMILES and honest null traits.

<details><summary>V0.4理由与本行变化背景</summary>

任务参数无偏离：route_scope.chosen_route_name 原样为“D-galactonate degradation”、oxygen_condition=null 与题面一致；3步均给出主底物/主产物英文名与SMILES、首选酶含EC、对应微生物并去重为1条ORG_001 profile；15项性状全数在场（13填写+2明确unknown，未把null计为遗漏）；evidence_registry与uncertainties齐备。扣分点仅为“各项最强来源”多以INTERNAL_KNOWLEDGE_ONLY占位、以及盐度在种级记录存在的情况下留null（完成度小缺口），故取7–8档内偏上。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows completeness and field presence; does not by itself establish scientific correctness or source quality.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_030：Gold declares a three-step required main-chain scope; it does not prove the answer chemistry.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> The main route order and terminal products match gold at name/connectivity level: D-galactonate -&gt; 2-dehydro-3-deoxy-D-galactonate -&gt; 6-phosphate -&gt; pyruvate + D-glyceraldehyde 3-phosphate. Direction and aldol cleavage are correct. Minor defects: simplified SMILES, unspecified stereo/charge, and null ATP/ADP SMILES prevent the top band; no direction or conservation cap.

<details><summary>V0.4理由与本行变化背景</summary>

三步化学与gold主链逐步一致且方向正确：S1 脱水（D-galactonate→2-dehydro-3-deoxy-D-galactonate+H2O，对应gold BSY-r02710）、S2 ATP依赖磷酸化（→2-dehydro-3-deoxy-D-galactonate 6-phosphate+ADP，对应gold BSY-r01882，ATP已作cofactor在列）、S3 醛缩裂解（→pyruvate+D-glyceraldehyde 3-phosphate，对应gold BSY-r03487）；起点与题面/gold根化合物一致、终点与gold terminal(BSY-c06675|BSY-c15179)一致，步骤连接无跳步、无方向反转，脱水/裂解原子收支成立。仅有非立体开链SMILES与ATP/ADP SMILES为null的局部表达缺陷（已在uncertainty声明），按SC3属9档而非7–8档的辅因子全缺情形，取9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：Shows gold reaction names, order and terminal products; representation/stereo equivalence is not established.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_030：Supports root and terminal identity at name level; not exact SMILES representation.

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 按C03逐一核验3个必答目标：答案S1的D-galactonate dehydratase/4.2.1.6与S2的2-dehydro-3-deoxygalactonokinase/2.7.1.58分别命中accepted名称与EC集合；S3的酶名与目标反应相近，但显式EC 4.1.2.29不在accepted集合（4.1.2.55/4.1.2.21），E0仅核到4.1.2.55且无4.1.2.29记录，故S3为局部U而非F。S=2,U=1,N=3，C≈0.67，按C04落&#91;5,6&#93;；S3为KEY_TERMINAL U，不能进入7–8，但两步已支持反应关联清楚、待核点明确，按C05取6。

<details><summary>V0.4理由与本行变化背景</summary>

S1 EC 4.2.1.6（D-galactonate dehydratase）与S2 EC 2.7.1.58（2-dehydro-3-deoxygalactonokinase）均落在gold多注集合内（4.2.1.140|4.2.1.6；2.7.1.178|2.7.1.58），酶名与反应类型一致；S3酶名2-dehydro-3-deoxy-D-galactonate-6-phosphate aldolase与gold酶名及E0中EC 4.1.2.55的accepted name/reaction（2-dehydro-3-deoxy-6-phospho-D-galactonate=pyruvate+D-glyceraldehyde 3-phosphate）一致，但所给EC 4.1.2.29不在gold多注集合{4.1.2.55,4.1.2.21}内且冻结证据无该号记录（GAP-030-011/018）。按四.5“选集外号先核官方条目；无法核验→UNRESOLVED，保留低分与待核标记，不cap”处理：主链酶对应大体成立、EC大类(4.1.2.x)与裂解反应类型不矛盾，故不触发D3a关键错误，档内取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：给出S01-S03的accepted酶名与EC集合；S03接受EC为4.1.2.55|4.1.2.21，不含答案S3的4.1.2.29；不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：给出必答三步的反应物、产物及有向主链关系，用于核对答案S1-S3的催化顺序；不外推未声称内容。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：官方EC 4.1.2.55条目反应包含2-dehydro-3-deoxy-6-phospho-D-galactonate = pyruvate + D-glyceraldehyde 3-phosphate；未核验答案S3的EC 4.1.2.29，亦不自动支持或反驳其他声称。
- ANSWER_TEXT / steps.S1-S3.enzyme：答案交付的酶名/EC为：S1 D-galactonate dehydratase/4.2.1.6，S2 2-dehydro-3-deoxygalactonokinase/2.7.1.58，S3 2-dehydro-3-deoxy-D-galactonate-6-phosphate aldolase/4.1.2.29。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> E. coli is an accepted organism for all three gold steps, and gold PATHWAY_COMPLETE marks E. coli species-level pathway capability true. The answer uses a real-looking strain label K-12 substr. MG1655 with TaxID 511145, but that strain-level identity/capability is not in the frozen E0 records. Species-level correspondence is strong; strain-level granularity remains a minor unverified point.

<details><summary>V0.4理由与本行变化背景</summary>

gold organism_gold对三步均给出Escherichia coli（EXACT，taxid 562）且PATHWAY_COMPLETE=TRUE，答案的物种身份与“可完成整条D-galactonate降解”的能力声称在种级获支持，未把单步菌写成全路径菌。问题在粒度：答案以菌株级K-12 substr. MG1655与TaxID 511145交付，冻结证据无TAXID:511145记录（GAP-030-026/028），属D3b身份阶梯①“物种级真实记录支持菌株级声称（记录真实且同lineage）”→档内扣分（7档附近）、默认不cap；能力声称有gold种级独立依据，不因身份粒度问题推翻主要微生物推荐。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_030：Supports E. coli at species level for the steps and pathway_complete; does not verify strain K-12 MG1655 TaxID 511145.

</details>

### D4 性状科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> Most given traits align with species-level E. coli gold: facultative anaerobic/aerotolerant, mesophilic preference and broad temperature range, pH range including 7.0, rod-shaped, Gram-negative, non-sporulating. Honest nulls are present for salinity and motility. Strain-specific ATCC and genome accession claims, plus exact optimum values, are not verified in E0; minor rather than major error.

<details><summary>V0.4理由与本行变化背景</summary>

按trait_scoreability_mask/trait_subfield_scoreability_mask，E. coli(562)可评分观测项中：F1“兼性厌氧”与gold facultative anaerobe=true/aerotolerant=true一致；F11“杆状”、F12“革兰氏阴性”、F13“不产孢”与gold观测一致；F7/F8/F9关于D-galactonate利用与garD/garK/garL活性与gold途径/酶一致；F14数值(4,641,652 bp、GC 50.8%)落在种级观测区间（1.22–7.62 Mb、40.2–63.0%）内未被反驳。待核/偏弱处：F2最适37°C与F3最适pH 7.0无观测可评分（min/max多为pending_teacher_adjudication，非scoreable）、F5 ATCC 47076与F14登录号NC_000913.3在快照不可核、F15栖息地描述gold为UNKNOWN、F4盐度种级记录存在而答案留null（完整性缺口主记D1，D4按已给内容评定不重复重扣）。主要性状可核实且适用，仅少量条目待核，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：Species-level trait observations/predictions for E. coli; does not verify strain K-12 MG1655 ATCC 47076 or NC_000913.3.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_030：Identifies which trait subfields are scoreable; does not fill unverified strain-specific values.

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> Core route, enzyme and microorganism claims rely on EVID_001/EVID_003, both INTERNAL_KNOWLEDGE_ONLY, which is MISSING_SOURCE. EVID_002 (NC_000913.3) and EVID_004 (ATCC 47076) give specific database records but cannot be verified in E0 and are UNRESOLVED_SOURCE. There is no verified mis-citation. The 3-4 band applies; score 3 because the core source chain is largely absent.

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09，及承担目标物降解能力论证的CG14）来源状态以MISSING_SOURCE为主——路径/酶/菌/多项性状均引EVID_001/EVID_003的INTERNAL_KNOWLEDGE_ONLY自我声明；CG17（NC_000913.3）与CG07内保藏号（ATCC 47076）虽标DATABASE_DIRECT，但冻结快照查无对应记录→UNRESOLVED_SOURCE待核。全案无经核实错引（无VERIFIED_MIS_CITATION_*），不触发cap（四.3：MISSING_SOURCE默认不cap；UNRESOLVED不计已核实关键错误）。决策相关组缺条目级可定位可核对证据、无外部证据支撑，属“全部缺失/不可核对”的低分档，档内取3（答案确有结构化evidence_registry与claim_scope映射，高于完全无引用）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows exactly what source types/IDs the answer delivered; does not verify external records absent from E0.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> The answer explicitly discloses oxygen-condition uncertainty, simplified SMILES/stereochemistry, and unverified traits; confidence labels are present and many unknowns are honest nulls. However, some specific accession/collection claims are marked high/medium without caveat. Overall main limitations are clear; single-point overconfidence is minor, not systemic.

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体良好：evidence_registry逐条标注source_type（明确自标INTERNAL_KNOWLEDGE_ONLY），逐项给confidence，2项未知（F4/F10）以null+unknown诚实填写而非编造，每步带uncertainty，总 uncertainties列出氧条件未定、SMILES简化、性状未逐项核验原始文献；未把预测包装成实证观测，也未见掩盖矛盾。扣分点：F14以DATABASE_DIRECT/high包装快照不可核的登录号、F5同标DATABASE_DIRECT（均属单点过度确信而非系统性），且未提示性状值为物种级参照外推到菌株K-12 MG1655的粒度边界。按D6严重度条款属档内扣（5–6至7档之间），取7。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s own uncertainty/confidence disclosures; does not verify the underlying claims.

</details>

## Grok

答案SHA256：`bfcdc775779878d1302783a073d6a35e9fa91b30361b3114f2154f9e5f0c4e5a`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步主链、每步底物/产物/酶/EC/微生物、15项性状、来源登记和不确定性均已交付；route_scope路线名原样填写，氧条件按题面保持null；仅有部分性状子字段以null保留，属允许的诚实未知，整体无重要模块缺失。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_030：证明本题gold为3步LINEAR_UNIQUE路线，用于核对交付步数与主链范围；不证明答案所有性状子字段均已核验。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_030：证明题面路线名、起点与终点身份；不替代答案对15项性状的来源核验。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链三步化学转化与gold方向、端点一致：脱水生成2-dehydro-3-deoxy-D-galactonate，ATP依赖磷酸化生成6-磷酸产物，醛缩裂解生成pyruvate与D-glyceraldehyde 3-phosphate。第2步未列H+且ATP/ADP电荷表达简化，属局部计量/表达问题，不推翻主链；未给9-10。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：支持三步反应的底物/产物、方向与主链顺序；不支持答案未交付的H+或具体蛋白实验活性。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：官方EC 4.1.2.55反应式支持2-dehydro-3-deoxy-6-phospho-D-galactonate裂解为pyruvate与D-glyceraldehyde 3-phosphate；不直接核验答案所用EC 4.1.2.21的具体蛋白归属。

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三个必答目标反应的酶名/EC均落在本题accepted sets内：S1 dgoD/4.2.1.6对应脱水酶，S2 dgoK/2.7.1.58对应激酶，S3 dgoA/4.1.2.21对应醛缩酶；无已确认KEY失败。dgoD/dgoK/dgoA基因归属为MINOR待核，且release的D3a高分门未放行9-10，故给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：gold酶行支持S02 4.2.1.6、S01 2.7.1.58、S03 4.1.2.21分别属于对应反应；不证明dgoD/dgoK/dgoA具体基因归属或实验活性。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：官方EC条目支持同一醛缩酶反应的accepted reaction；不自动支持4.1.2.21的具体蛋白底物谱。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> E. coli在organism_gold中逐step出现且PATHWAY_COMPLETE为真，支持物种级身份与路径能力；答案进一步指定K-12 substr. MG1655/TaxID 511145，属菌株级身份，但冻结记录只有E. coli物种级与GCA_003018455.1，未单独核验511145，按身份阶梯属粒度不足、档内扣分，不构成key error。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_030：支持Escherichia coli作为S01/S02/S03对应微生物及E. coli PATHWAY_COMPLETE=true；不支持K-12 substr. MG1655/TaxID 511145的菌株级独立记录。

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 多数可核性状与gold相符：兼性厌氧、运动性、杆状、革兰氏阴性、不产芽孢、非嗜盐类别、D-半乳糖酸降解与dgo酶活；但37°C与pH 7.0被写成最适值，而gold只有生长范围/偏好，最适未知；ATCC 700926、NC_000913.3、F15栖息地等菌株级/生态声称在冻结记录中未核。属多处局部条件与证据问题，给7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_030：支持E. coli的兼性厌氧、运动性、杆状、Gram阴性、不产芽孢、非嗜盐偏好、碳源利用与路径表型；不支持37°C/pH 7.0为最适值，也不支持菌株级ATCC/NCBI登录号。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_030：显示E. coli F2/F3/F4多个子字段为completeness_only或pending_teacher_adjudication；用于说明最适/极限值不可作为已观测精确值加分。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_030：逐子字段标明optimum无观测来源、温度/pH/盐度端点待裁定；不支持把生长温度点直接当作最适值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的evidence_registry全部source_type=INTERNAL_KNOWLEDGE_ONLY，即使给出EcoCyc/ATCC/NCBI名称和局部record_id，也属于自我声明记忆而非可定位的外部交付来源；核心路线、酶、菌和性状均无法按原交付追到可核条目。没有已核实的错引，故不cap，但D5低档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：只证明答案实际交付了内部知识来源登记；不证明这些来源真实存在、可定位或支持相应声称。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确披露未联机复核、EcoCyc编号来自记忆、用K-12测序株代表dgo途径、SMILES未联机核对、若干数值子字段留空；这些是具体诚实披露。但 pathway/酶仍以high confidence呈现内部知识，37°C与pH 7.0等最适值未标为推断，属局部过度确信，未达系统性误导。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持答案确实披露了未联机核验、菌株代表性与SMILES未核对等限制；不证明其所有high confidence判断与证据强度相称。

</details>

## GPT5.6

答案SHA256：`1a5a0e9d3aa9d4fcf6f33c4b761c55567feac3640f71fec8d4041fec81bb0d08`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出两步主链及对应酶/EC和E. coli菌株，但缺少指定的2-dehydro-3-deoxy-D-galactonate磷酸化步骤，末端也由G3P变为glyceraldehyde；15项性状虽全部出现但均为null/unknown，来源仅内部知识。主模块均有涉及但必要内容有实质遗漏，落5分档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：支持三道必答步及S03末端产物；不表示答案已交付全部步骤。
- ANSWER_TEXT / ANSWER：支持答案实际只给两步、15项性状全为null/unknown的覆盖登记。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 第一步D-galactonate脱水生成2-dehydro-3-deoxy-D-galactonate在化学上成立；但第二步直接以非磷酸化底物裂解为pyruvate+glyceraldehyde，跳过了指定主链的磷酸化/6-磷酸底物转化，不能延续到规定末端G3P。仅一步可靠、关键连接不符合指定路径，且D2允许区间为&#91;1,4&#93;，取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：支持指定主链S02脱水、S01磷酸化、S03 6-磷酸底物裂解的顺序；不支持非磷酸化直接裂解作为指定S03。
- ANSWER_TEXT / ANSWER：显示答案第二步使用非磷酸化2-keto-3-deoxy-D-galactonate并产出glyceraldehyde。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S02（D-galactonate dehydratase EC 4.2.1.6）与答案第一步一致，可支持；S01激酶步骤未交付；S03为KEY_TERMINAL，答案以非磷酸化底物和EC 4.1.2.20裂解为glyceraldehyde，而既定S03要求6-磷酸底物到pyruvate+D-glyceraldehyde 3-phosphate，故关键末端不成立。S=1,F=1,M=1，C=0.333落&#91;3,4&#93;；KEY末端失败使主功能严重受损，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_030：支持S02可接受D-galactonate dehydratase EC 4.2.1.6，且S03可接受aldolase为EC 4.1.2.55/4.1.2.21；不支持EC 4.1.2.20作为S03。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_030：支持S03底物为2-dehydro-3-deoxy-D-galactonate 6-phosphate、产物为pyruvate+D-glyceraldehyde 3-phosphate；不支持非磷酸化底物和glyceraldehyde。
- E0_EVIDENCE / f3e0:ec:4.1.2.55：官方EC 4.1.2.55反应使用2-dehydro-3-deoxy-6-phospho-D-galactonate生成pyruvate+D-glyceraldehyde 3-phosphate；不扩展到EC 4.1.2.20。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> E. coli在gold中支持S01/S02/S03步级归属且PATHWAY_COMPLETE为TRUE，答案选用E. coli方向正确。但答案把身份细化为K-12 MG1655/TaxID 511145，E0无该TaxID冻结记录，属于物种级记录支持更细菌株声明的粒度不足；不推翻主要微生物推荐，按D3b身份阶梯取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_030：支持E. coli物种级可对应三步并具PATHWAY_COMPLETE；不等于已核实K-12 MG1655/TaxID 511145菌株级身份。
- ANSWER_TEXT / ANSWER：显示答案使用Escherichia coli K-12 MG1655/TaxID 511145并声称完整路径。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的15项性状全部为null/unknown，没有交付任何可评价的性状值。按P44，全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示15项性状均为null或unknown，无实际数值/文本值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的EVID_001/EVID_002均为INTERNAL_KNOWLEDGE_ONLY且无record/locator；EVID_003虽写NCBI Taxonomy与TaxID 511145，但source_type仍是INTERNAL_KNOWLEDGE_ONLY且E0无该TaxID记录。决定相关组均为MISSING_SOURCE，无法从原交付定位可核对外部来源；无已核实错引，不cap，按低分档取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示三条证据均为INTERNAL_KNOWLEDGE_ONLY，反应/酶无record/locator，身份记录为TaxID 511145。

</details>

### D6 不确定性与诚实度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案把证据标为INTERNAL_KNOWLEDGE_ONLY，并对底物立体化学与下游延续作了有限不确定性说明；但同时对完整路径、具体酶/EC和E. coli K-12 MG1655给出medium confidence，且未披露缺失磷酸化步骤/非磷酸化替代分支这一主要限制，部分结论强度仍超过依据。按5–6档取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示证据性质标为内部知识、部分字段有局限说明，但主要路径限制未充分披露。

</details>
