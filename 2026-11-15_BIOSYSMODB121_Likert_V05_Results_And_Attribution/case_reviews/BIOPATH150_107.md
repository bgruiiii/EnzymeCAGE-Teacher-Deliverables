# BIOPATH150_107：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：nicotinate degradation I

污染物：Nicotinate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 67.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 49.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 76.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 44 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 73 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 52.5 | COMPARABLE | USER_AUTHORIZED_RECOLLECTION_R1 |

## GLM

答案SHA256：`b1fa67757161e7ca1197c485f7ee1316ec380aba97be1cfaafd87657cba6b31f`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 6个必答主链步骤齐全，终点为fumarate；每步均给出主底物/主产物、SMILES、酶和菌，15项性状均出现，route_scope原样保留。少量完成度缺口：4步EC为null、部分性状子值为null，但任务允许未知填null，故属少量遗漏，7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

六个模块均有实质交付：6步主链（steps S1–S6，order=1–6）各给主底物/主产物英文名与SMILES、一个首选酶与一个对应微生物；route_scope.chosen_route_name原样为&quot;nicotinate degradation I&quot;，未改选路线；organism_profiles仅一条ORG_001（物种+菌株去重）并被六步引用；15项性状全部填写（filled=15, omitted=0）；evidence_registry与uncertainties均给出。4步EC按题面第5条填null属规则允许的诚实未知，不计为遗漏。仅少量定位/字段粒度不足，落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv：本题为6步线性唯一主链、终点Fumarate；只要求一条主链的6个必要步，不是要求覆盖全部分支。
- GOLD_SLICE / case_root_identity.tsv：题面指定nicotinate degradation I，根Nicotinate，终点Fumarate。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 6步主链顺序与gold一致：nicotinate→6-hydroxynicotinate→2,5-dihydroxypyridine→N-formylmaleamate→maleamate→maleate→fumarate。局部问题：S1用NAD+而非cytochrome，S2称“水解脱羧”并漏O2/NADH，辅因子与机制表达不完整；但主底物/主产物、方向与步骤连接未被推翻，属7–8档局部计量/机制缺陷，取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链六步方向与主产物逐步与冻结gold一致：nicotinate→6-hydroxynicotinate→2,5-dihydroxypyridine→N-formylmaleamate→maleamate→maleate→fumarate，终点fumarate即gold terminal（CORE CG03），无起始步错误、无方向反转、无一步跳到中心代谢物、无未声明的严重偏离，故不触发D2关键错误。扣分点为S2：答案把6-羟基烟酸→2,5-二羟基吡啶写成&quot;水解脱羧&quot;、仅列water为共底物，而gold该反应(reaction_gold row 1848)以dioxygen与NADH为底物、NAD+/CO2/H2O为产物；答案字面H与电荷不守恒且机理表述不同。该缺口属局部计量/机理缺陷（P103、P62），不cap，7–8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：逐步给出S04 nicotinate→6-hydroxynicotinate、S03→2,5-dihydroxypyridine、S01→N-formylmaleamate、S02→maleamate、S05→maleate、S06→fumarate；并显示S03需O2/NADH、S04用cytochrome。
- GOLD_SLICE / case_root_identity.tsv：路线终点为Fumarate。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> S3–S6的酶名/EC与accepted集合一致或名称精确命中（S3 2,5-dihydroxypyridine 5,6-dioxygenase、S4 N-formylmaleamate deformylase、S5 maleamate amidohydrolase、S6 maleate cis-trans isomerase EC 5.2.1.1），可给功能信用。S1为入口步，答案给EC 1.17.1.5而accepted为nicotinate dehydrogenase (cytochrome) EC 1.17.2.1；S2“6-hydroxynicotinate decarboxylase”不在accepted集合且漏O2/NADH。二者是key/MAJOR待核，未获官方记录不能判F，亦不能进7–8；按部分主干支持取5。

<details><summary>V0.4理由与本行变化背景</summary>

S3 2,5-dihydroxypyridine 5,6-dioxygenase、S4 N-formylmaleamate deformylase、S5 maleamate amidohydrolase、S6 maleate cis-trans isomerase(EC 5.2.1.1)四个酶名/EC与gold一致；S1酶名nicotinate dehydrogenase方向正确。不足：(a) S2把gold的6-hydroxynicotinate 3-monooxygenase(EC 1.14.13.114)写成&quot;6-hydroxynicotinate decarboxylase&quot;，酶类别与反应类型不符（FV-02）；(b) S1给EC 1.17.1.5，gold为nicotinate dehydrogenase (cytochrome) EC 1.17.2.1，但E0无EC 1.17.1.5冻结记录（GAP-107-010），按四.5/P66记UNRESOLVED待核、不判错、不cap；(c) S3–S5 EC按题面规则null。核心推荐未被推翻，属&quot;有合理候选和部分支持、若干步骤缺具体核验&quot;，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：各必答步accepted酶名/EC：S04 nicotinate dehydrogenase (cytochrome) EC 1.17.2.1；S03 6-hydroxynicotinate 3-monooxygenase EC 1.14.13.114；S01 2,5-dihydroxypyridine 5,6-dioxygenase EC 1.13.11.9；S02 N-formylmaleamate deformylase EC 3.5.1.106；S05 maleamate amidohydrolase EC 3.5.1.107；S06 maleate cis-trans isomerase EC 5.2.1.1。仅支持策展功能，不证明具体蛋白活性。
- GOLD_SLICE / reaction_gold.tsv：S03/S04的辅因子与反应方向；用于核对答案S1/S2的酶与辅因子。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 物种级Pseudomonas putida在organism_gold中多步出现并列为PATHWAY_COMPLETE，支持物种可关联该路线。但答案具体到KT2440，TaxID 160482在E0中无冻结记录，whole-pathway能力又仅以物种级记录支撑；菌株级身份/能力尚未充分核验。属5–6档“合理候选与部分支持，但关键身份或作用范围未充分核验”，取6。

<details><summary>V0.4理由与本行变化背景</summary>

六步均归Pseudomonas putida，gold organism_gold对本题六步反应均存在Pseudomonas putida的EXACT步级记录（并另有P. fluorescens/Alcaligenes faecalis可选），菌属选择有依据；complete_pathway_organism_profile_id=ORG_001的种级全路径能力由gold PATHWAY_COMPLETE（TaxID 303, pathway_complete=TRUE）支持，未出现&quot;由序列存在直接推断整条路径&quot;式无依据外推。不足为身份粒度：答案以种级可支持的身份配菌株KT2440与TaxID 160482，160482在E0无冻结记录（GAP-107-001/045/047），属D3b身份阶梯①&quot;粒度不足&quot;——记录真实且同lineage、菌株能力声称为物种级证据所覆盖，档内扣分、默认不cap，7档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：P. putida TaxID 303出现在多步STEP并列为PATHWAY_COMPLETE；支持物种级P. putida可关联该路线，不自动证明KT2440菌株级TaxID或所有菌株能力。

</details>

### D4 性状科学性：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 多数性状与P. putida observed记录相符：运动、杆状、革兰氏阴性、不产孢、非嗜盐、pH约7、可利用多种碳源、基因组大小/GC在物种范围内；F14用KT2440的NC_002947也合理。少量问题：F2最适30°C、F9“完整酶系活性”等偏记忆/偏强，但无明确关键性状矛盾，7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

与gold种级代表记录一致、按四.4同物种代表记录条款不因菌株不同判错的项目：F1 aerotolerant、F2 preference=mesophilic/温度生长区间25–37℃、F3 pH growth 7.0（与答案optimum 7.0吻合）、F4 non-halophilic、F10 motility=true、F11 rod-shaped、F12 gram-negative、F13 sporulation=false。问题项：F2 optimum_c=30无观测来源（该子字段completeness_only）；F9把&quot;具备完整烟酸降解途径酶系活性&quot;写成既有事实，属由通路/基因组存在向观测酶活外推（P115）；F7声称&quot;以烟酸作为唯一碳源、氮源和能量来源&quot;，gold种级F7记录未含nicotinate；F14基因组数值、F5 DSM 6125在E0无记录。无经核实的错误数值（如嗜冷菌写80℃一类误导筛选的离谱值），不触发D4关键错误；属&quot;部分性状准确且适用、关键项证据不足&quot;5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：P. putida TaxID 303的观测性状：温度25–37°C、pH growth 7.0/min5/max8、非嗜盐、运动、杆状、革兰氏阴性、产孢false、可利用多种碳源等；物种代表性记录，不证明KT2440所有性状相同。
- GOLD_SLICE / trait_scoreability_mask.tsv：标示F2 optimum等子字段为completeness_only或pending，不能把未观测子字段当已核实观测。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> evidence_registry全部为INTERNAL_KNOWLEDGE_ONLY：EVID_001只有MetaCyc路线名、record_id null；EVID_002无database/record_id/locator却覆盖多数性状；EVID_003–005虽给NC_002947、DSM 6125、160482，但仍是内部知识且无locator/无原文，不能核对其实际支持内容。结论与来源关联很弱，属3–4档，取3。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG09、CG08、CG17）均无条目级可定位可核对的来源：EVID_001–EVID_005的source_type全部为INTERNAL_KNOWLEDGE_ONLY，record_id/locator多处为null，答案在uncertainties中自述&quot;全部证据均为模型内部知识，未进行实时数据库检索&quot;，按P34属MISSING_SOURCE类自我声明；路线组另给库名MetaCyc+路线名（GENERIC_SOURCE），编号类声称（EC 1.17.1.5/5.2.1.1、TaxID 160482、NC_002947、DSM 6125）在E0均无冻结记录→UNRESOLVED_SOURCE待核。E0唯一记录为TaxID 294（P. fluorescens），与本答案声称无关联，不能提供任何正向支持。按P41：决策相关组全部缺失/笼统→3–4档；因EVID_001的claim_scope对S1–S6与F9映射清楚、错误未被核实（UNRESOLVED≠虚构），档内取4。无已核实错引，不触发D5关键错误，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / EVID_001：答案将EVID_001标为INTERNAL_KNOWLEDGE_ONLY，database=MetaCyc但record_id=null；只能算内部知识声明。
- ANSWER_TEXT / EVID_002：EVID_002无database、无record_id、无locator，覆盖多数性状；无法定位到条目核验。
- ANSWER_TEXT / EVID_003：EVID_003虽给NCBI RefSeq record_id=NC_002947，但source_type仍为INTERNAL_KNOWLEDGE_ONLY、locator=null。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> uncertainties明确披露全部证据为内部知识、EC/基因组/保藏号为记忆值、raw_text为null；证据类型没有系统性伪装成观测，主要限制已说明。个别字段给high confidence但属教科书性状，且未掩盖未知；7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且诚实：uncertainties逐条列出EC 1.17.1.5与5.2.1.1为记忆值、其余EC未能确证已填null、基因名未核、开环产物与三步水解酶名基于路线记忆、基因组数值与DSM保藏号为记忆值、raw_text全null且未做实时检索；route_scope.notes正确区分题面氧条件null与所选好氧路线的关系，未把路线属性写成题面条件。扣分点：F1/F6/F12/F13以high置信包装无来源的种级性状、S2机理差异零披露、F9通路酶活以既成事实表述——属单点过度确信与证据类型轻度越位，非系统性误导、无掩盖已知矛盾，档内扣，不cap。7档取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：答案不确定性列表明确全部证据为内部知识、EC/基因组/保藏号为记忆值、raw_text为null。
- ANSWER_TEXT / confidence：部分字段标high/medium confidence，需与证据类型相称。

</details>

## DeepSeek

答案SHA256：`f1d5d0d82739bc78a9d68c491611b99e6237bb8c364a8e6ad3b99dbb65825e16`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 题面route_scope.chosen_route_name被原样回显（nicotinate degradation I），6步均给出底物/产物英文名+SMILES、一个首选酶+EC、一个对应微生物；单一profile按物种+菌株去重；15项性状齐全；JSON完整。程序route_status=DEVIATES，task_conformance_status=OK仅表示路线名锁定字段回显一致，而第6步用maleate hydratase（EC 4.2.1.31）把该路线终止转化maleate→fumarate（EC 5.2.1.1）替换为maleate→(S)-malate，属“自称路线合规却交付不同化学路线”的任务偏离，按D1关键错误封顶，在&#91;1,4&#93;内取4：其余模块完整、偏离边界清楚，但关键任务偏离不许进入5分以上。

<details><summary>V0.4理由与本行变化背景</summary>

六步主链齐全，每步含底物/产物(name+SMILES)、酶+EC、微生物；同一菌去重为单一profile(ORG_001)供各步引用；15项性状全部返回(14填、1明确未知)，交付格式合规。范围偏离：题面路线nicotinate degradation I的gold终点为fumarate，答案止于(S)-malate(第6步改maleate水合)，属终点范围偏离，扣分但不构成核心模块缺失。7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_107：支持答案第6步给出的是maleate水合而非maleate异构化；不支持该步属于指定路线终止转化。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：支持gold终止步为maleate⇌fumarate；不支持答案的maleate→(S)-malate属该锁定路线。
- QUESTION_TEXT / QUESTION#BIOPATH150_107：支持本题路线被锁定；不支持把终止步替换为路线外化学仍算任务合规。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 前5步的底物/产物配对与顺序逐条对应gold链路（nicotinate→6-hydroxynicotinate→2,5-dihydroxypyridine→N-formylmaleamate→maleamate→maleate），方向均为底物→产物，charge notation差异不改变结构对应；主要缺口是第6步：gold终止步为maleate⇌fumarate（异构化），答案给出maleate→(S)-malate（水合），即终止转化/终点与指定路线不一致，属“主干部分成立但关键转化需修订”。辅因子（氧化型细胞色素、NADH/H+/O2）普遍未列，按P103只作局部计量缺陷，不另cap。D2允许区间&#91;1,6&#93;，档内取6：已支持部分的逐反应关联清楚、待修点单一明确，但终止转化缺口足以阻止进入7分以上。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S5化学与gold一致(nicotinate→6-hydroxynicotinate→2,5-dihydroxypyridine→N-formylmaleamate→maleamate(+formate)→maleate(+ammonium))，方向与连接正确；第6步偏离：以maleate hydratase(EC 4.2.1.31)把maleate水合为(S)-malate，而gold nicotinate degradation I为maleate cis-trans isomerase(EC 5.2.1.1)异构为fumarate，终点不同且未声明为替代分支；辅因子(O2/NADH/H2O等)全缺属局部计量缺陷(7–8档口径，不cap)。主干成立但终点关键转化需修订，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：支持前5步的主要底物/产物与主链顺序；支持S06为maleate⇌fumarate；不支持终止步为malate水合。
- ANSWER_TEXT / ANSWER#BIOPATH150_107：支持答案给出的化学转化序列与方向；不支持其终止步属于锁定路线。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> N=6；程序已确认KEY终止步BIOPATH150_107__S06__BSY-r03834为F（NONMATCH，proof REAL-ROUTE-B480-0350-BIOPATH150_107__S06__BSY-r03834），其余5步自动对齐未确认（U），S=0，C=0.0；触发D-KEY4（上界4），允许区间&#91;1,4&#93;。带内取3：可用部分（前5步酶名与gold链路一致，其中1.13.11.9与3.5.1.107与accepted set完全相同）与关键失败边界（终止步被替换）可分，但已核支持为零、其余EC与accepted set不一致且E0无记录可核、表示等价待裁，依据不足以支撑受限范围上沿4；无已确认漏答，故不按M处理。

<details><summary>V0.4理由与本行变化背景</summary>

酶名与反应类型基本匹配：S3 2,5-dihydroxypyridine 5,6-dioxygenase(EC 1.13.11.9)与S5 maleamate amidase(EC 3.5.1.107)与gold吻合；S1 nicotinate dehydrogenase(1.17.99.1 vs gold 1.17.2.1)、S2 6-hydroxynicotinate 3-monooxygenase(1.14.13.163 vs gold 1.14.13.114)、S4 N-formylmaleamate deformylase(3.5.1.105 vs gold 3.5.1.106)编号与gold不符且E0无记录→UNRESOLVED，非确认错误；未见EC大类与反应类型矛盾。部分支持但若干关键步骤EC缺核验，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：支持六步目标反应及S06为maleate⇌fumarate；不支持答案S6的maleate水合为终止目标反应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_107：支持accepted set的酶名/EC；不支持答案给出的1.17.99.1、1.14.13.163、3.5.1.105、4.2.1.31为已核正确。
- ANSWER_TEXT / ANSWER#BIOPATH150_107：支持答案实际交付的EC号与酶名；不支持这些EC已获冻结证据核验。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案六步统一用Pseudomonas putida KT2440（TaxID 160488），并以complete_pathway_organism_profile_id声称为整条路径菌。gold在S01–S06六步均有P. putida（TaxID 303）物种级STEP行，且PATHWAY_COMPLETE含TaxID 303，故物种层面身份与路径能力有支持；但E0无160488记录（GAP-107-046/048），1853菌株级身份、菌株级步归属与菌株级全路径能力未核，属“物种级记录支持菌株级声称”的粒度不足，按身份阶梯档内扣分（7档），不cap；未核不等于错误。

<details><summary>V0.4理由与本行变化背景</summary>

全步使用Pseudomonas putida KT2440(TaxID 160488)作整条路径菌。P. putida在gold PATHWAY_COMPLETE中列为整条路径菌(物种级,TaxID 303)，菌种选择合理；但以单一菌株KT2440承担全部6步整条路径能力，属物种级→菌株级外推，KT2440(160488)菌株级能力无冻结记录(GAP-107-046/048)→UNRESOLVED；身份编号正确性未核验。身份定位≠反应级能力≠完整路径能力。5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_107：支持P. putida在物种层面出现在六步并与整条路径能力相关联；不支持KT2440/160488菌株级身份或菌株级能力。
- ANSWER_TEXT / ANSWER#BIOPATH150_107：支持答案的菌株级身份与整路径菌声称；不支持该声称已有冻结记录核验。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 15项性状齐全，F4为明确null（诚实未知）；F10–F13（有运动性、杆状、革兰氏阴性、不产芽孢）与gold 303观测一致，F2 preference=mesophilic一致，F6需氧呼吸/O2与物种记录方向一致。不可核部分：F2 optimum_c、F3 pH optimum在gold 303为completeness_only（无观测源）；F5保藏号ATCC 47054、F14 NC_002947.4/6,181,873 bp/61.5% GC、F7/F8碳源与广谱降解声称在E0无160488记录，不能核验（按代表记录条款也不判错）。主要性状方向适用、局部未核，取7档；F2上下限、pH上下限、F4缺失主要计D1完成度，不在此重复重扣。

<details><summary>V0.4理由与本行变化背景</summary>

性状多与P. putida物种级(303)记录一致：F1需氧、F10运动性、F11杆状、F12革兰氏阴性、F13不产芽孢与gold OBSERVED一致；F2最适30/中温与303温度25–37区间相符；F4盐度如实null、F3 min/max null，诚实披露。KT2440菌株级数值(ATCC 47054、NC_002947.4、6,181,873 bp、GC61.5%)概念合理但E0无163/160488记录→未核；同物种代表记录口径下不因菌株不同判错。主要性状适用，关键项存在未核，7–8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_107：支持物种级303的观测记录用于代表记录比对；不支持菌株级160488数值，也不把range端点当最适值。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_107：支持哪些子字段可作精度分母；不支持把非scoreable子字段判错。
- ANSWER_TEXT / ANSWER#BIOPATH150_107：支持答案实际填写的性状值；不支持这些数值已被冻结证据核验为真。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> evidence_registry两条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null；步骤反应、酶-EC、微生物身份、性状、基因组登录号等全部关键决策组只挂自建EVID_001/EVID_002，无任何可定位条目或计算记录，属MISSING_SOURCE（完全无外部可核查来源），落入1–2档；无已核实错引（不存在可核对的被引条目），按P34默认不cap；取2：registry具备claim_scope映射和证据类型自述，略优于完全空白，但可追溯性实质为零。

<details><summary>V0.4理由与本行变化背景</summary>

全部结论仅INTERNAL_KNOWLEDGE_ONLY(EVID_001/EVID_002)，无database/record_id/locator/DOI，无可定位外部来源→MISSING_SOURCE，低分档；无伪造DOI，非错引，不cap。ATCC 47054、TaxID 160488、各EC编号等编号类声称无冻结记录→UNRESOLVED。取3(低分档偏上，因有claim_scope结构化登记但来源本身不可定位)。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_107：支持答案未交付可定位来源；不支持任何结论可被外部条目核对。
- RUBRIC_CLAUSE / P34：支持MISSING_SOURCE（含仅INTERNAL_KNOWLEDGE_ONLY）按低分档且默认不触发关键错误cap。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 正面：证据类型在registry中统一标为INTERNAL_KNOWLEDGE_ONLY（未冒充数据库/实验观测），F4等未知项如实null；负面：steps&#91;*&#93;.enzyme/microorganism及多数性状confidence=high，uncertainties为空数组，未说明“仅有内部知识、无外部支持”，也未披露菌株级身份未核、终止步与路线不符等主要限制，属“有不确定性说明但过于笼统、部分结论强度仍超过依据”的5–6档；未达到系统性把预测写成实证观测，故不cap；取5。

<details><summary>V0.4理由与本行变化背景</summary>

有部分不确定性标注：F4盐度null、F3 min/max null、若干性状medium/low/unknown置信，体现未知如实；但路径6步的酶/菌全部标high置信、来源为INTERNAL_KNOWLEDGE_ONLY，uncertainties为空，未声明这些为内部记忆/待核，也未提示第6步终点与canonical fumarate不一致或EC编号待核。部分结论强度超过依据、证据类型区分不足；因有诚实null且非明知掩盖，不作系统性误导cap，属多点过度确信，5–6档取5。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_107：支持答案未给出限制/冲突说明且置信偏高；不支持其高置信有对应证据强度。
- RUBRIC_CLAUSE / P119：支持单点/多处过度确信与系统性误导分档处理，前者档内扣不cap。

</details>

## Kimi

答案SHA256：`ac269c414b73181b7a213d2096c2427d748bb70314e21a2c4cd07f9ada2b5e2d`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 题面指定 nicotinate degradation I；答案按6步主链完整给出底物/产物英文名与SMILES、首选酶及EC、对应微生物，并提交15项性状及来源登记。route_scope.chosen_route_name逐字为题面路线，终点为fumarate；仅存在少量局部来源/未知字段与工程性表达问题，不构成重要模块缺失或路线偏离。

<details><summary>V0.4理由与本行变化背景</summary>

全部必答模块实质交付：6步主链均含底物/产物英文名与SMILES、首选酶与EC、对应微生物与profile_id；route_scope.chosen_route_name与题面路线名逐字一致；单一菌株去重为一条profile并返回全部15项性状（14项填写+1项明确未知null）；5条证据条目与不确定性说明均在。仅性状证据粒度与F4一处明确未知属轻微缺陷，无模块缺失或范围偏离，落9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ac269c414b73181b7a213d2096c2427d748bb70314e21a2c4cd07f9ada2b5e2d：答案正文包含6步路线、各步底物/产物、酶/EC、微生物及15项性状与来源字段
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_107：正式案例记录显示本题为6步线性主链、终点主产物为fumarate
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：gold反应序列给出题面指定路线的6个必答目标步及主底物/主产物顺序；不表示任何答案正确

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主有机碳骨架与方向连续且与gold一致：nicotinate→6-hydroxynicotinate→2,5-dihydroxypyridine→N-formylmaleamate→maleamate+formate→maleate+NH4+→fumarate，终点为fumarate，无反向主链或跳步。若干步骤省略H2O、cytochrome、NADH/H+等辅因子或配平细节（尤其S1/S2/S4/S5），并存在羟吡啶/吡啶酮互变异构SMILES表达；按P103属局部计量/表达缺陷，不推翻主链化学结论。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步吻合：nicotinate→6-hydroxynicotinate→2,5-dihydroxypyridine→N-formylmaleamate→maleamate→maleate→fumarate，方向正确、终点与gold terminal(Fumarate)一致、SMILES与gold canonical同构（羟基吡啶/吡啶酮互变异构表达差异不判错）。缺陷是辅因子/氧化还原载体计量不全（S1缺细胞色素与水、S2缺NADH/NAD+与H2O、S4/S5缺H2O/H+），属局部计量缺陷，按八.辅因子条款落7–8档，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ac269c414b73181b7a213d2096c2427d748bb70314e21a2c4cd07f9ada2b5e2d：答案逐步给出主底物/主产物、方向与主要转化类型
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：gold逐步反应方向、主底物/主产物与线性顺序；用于核对主链化学连续性，不扩展到未声称的辅因子细节
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_107：本题根化合物为Nicotinate，terminal主产物为Fumarate

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 多数目标步的酶/EC与accepted功能粒度为S或可合理可核：S3 NicD 1.13.11.9、S4 N-formylmaleamate deformylase 3.5.1.106、S2 NicC 1.14.13.114、S5 maleamate amidase/hydrolase 3.5.1.107、S6 maleate isomerase 5.2.1.1均有对应accepted集合支持。关键进入步S1仍为U：答案给nicotinate dehydrogenase (NicAB) EC 1.5.1.13，而本题accepted集合登记为nicotinate dehydrogenase (cytochrome) EC 1.17.2.1；冻结材料无记录可确认1.5.1.13与1.17.2.1在本任务功能层的等价性。该U为KEY U，按C05不得进入7-8，但并非已核F，故给5-6档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

六步酶名与反应类型均与gold对应（6-hydroxynicotinate 3-monooxygenase、2,5-dihydroxypyridine 5,6-dioxygenase、N-formylmaleamate deformylase、maleamate amidase、maleate cis-trans isomerase），其中5步EC（1.14.13.114、1.13.11.9、3.5.1.106、3.5.1.107、5.2.1.1）与enzyme_gold逐字一致；首步EC 1.5.1.13与gold 1.17.2.1不一致且E0无该EC冻结条目，按四.5/四.6记UNRESOLVED待核、档内扣分不cap，落8档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ac269c414b73181b7a213d2096c2427d748bb70314e21a2c4cd07f9ada2b5e2d：答案各步酶名、EC与gene_or_protein字段；不扩展为具体蛋白实验活性证明
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_107：本题accepted酶/EC rows：包括S04 nicotinate dehydrogenase (cytochrome) EC-1.17.2.1、S06 maleate cis-trans isomerase EC-5.2.1.1等；只支持功能层对应，不证明任意具体蛋白底物谱或实验活性

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 各步均用P. putida KT2440。Gold organism_gold在六步均列P. putida（TaxID 303），且PATHWAY_COMPLETE也列P. putida，因此物种级微生物对应可靠。KT2440菌株/TaxID 160488及菌株级全路径能力在E0无冻结记录，只能作局部待核；未见身份矛盾或把单步写成全路径的错误。按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

六步均归属Pseudomonas putida（ORG_001），organism_gold对六个反应步均有P. putida的EXACT种级记录，且PATHWAY_COMPLETE行（taxid 303）支持该种整条路径能力，故反应级与整路径能力声称有gold支持；但菌株级身份（KT2440、TaxID 160488、ATCC 47054）超出冻结记录粒度且E0无法核验，按D3b身份阶梯①粒度不足档内扣分（7档附近），不cap；身份定位/反应级能力/整路径能力三层分别登记。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_107：支持P. putida species taxid 303出现在各步及PATHWAY_COMPLETE；不核实KT2440 strain/TaxID 160488。
- ANSWER_TEXT / ANSWER：答案各步绑定P. putida KT2440并声明complete_pathway_organism_profile_id=ORG_001。

</details>

### D4 性状科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 15项中14项填写、F4盐度明确null。P. putida物种级gold支持革兰氏阴性、杆状、运动、不产孢、pH生长约7、中温菌及基因组范围；答案多数相符。局部问题：F1“严格好氧/专性好氧”强于gold的aerotolerant记录；F2 optimum 30 °C、F5 ATCC 47054、F7烟酸根唯一碳源、F14 NC_002947为KT2440特异且E0未核；F4未填但如实unknown。无关键性状被已核推翻，按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

主要性状与同物种代表记录（P. putida种级trait_gold）一致：温度生长25–37℃、中温偏好；pH生长7、min5/max8；革兰阴性、杆状、有运动性、不产芽孢；基因组大小与GC落在种内观测区间。问题：F2把培养温度30℃写成optimum（培养温度不等于最适值）、F5 ATCC 47054与F14 NC_002947数值无冻结记录待核、F4盐度整体null（完成度归D1）。总体属少量条件/数值与证据粒度问题，落7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_107：P. putida taxid 303物种级性状；按同物种代表记录口径可用于参照，不等于KT2440菌株全部性状相同。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_107：标示F2 min/max等子字段待裁定、部分性状仅completeness_only；不把未核字段当已错。
- ANSWER_TEXT / ANSWER：答案15项性状原文及confidence/evidence_id。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 每步/每性状均有evidence_id并映射到evidence_registry；CORE路线/酶/身份声称指向MetaCyc pathway、Jiménez等文献、RefSeq NC_002947和ATCC 47054。但EVID_002缺年份/卷期/DOI，EVID_005为无record_id的BacDive strain datasheet，E0对多数引用为GAP，不能核对其实际支持内容；状态应为UNRESOLVED_SOURCE/GENERIC_SOURCE，非已核实错引。属部分关键结论可定位但未核，按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出逐组可定位线索：EVID_001 MetaCyc路线名、EVID_002完整题录、EVID_003 NCBI登录号、EVID_004 ATCC保藏号，并逐步绑定evidence_id；但E0本题切片仅1条P. fluorescens记录，全部EC/TaxID/登录号/保藏号/文献条目均无法核验（GAP-107-002/003/005/007/013/017/019/021/040/041/042/046），性状来源EVID_005无record_id属笼统来源。按四.3：决策相关组登记UNRESOLVED_SOURCE低分+待核，不判虚构、不计已核实关键错误、不cap；结构上强于纯笼统列表，落5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：E0仅提供TaxID 294 P. fluorescens官方记录；不支持答案KT2440、EC 1.5.1.13、ATCC 47054或NC_002947。
- ANSWER_TEXT / ANSWER：答案交付的五个证据条目及claim_scope；用于评价可追溯性，不证明引用内容真实。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案明确披露题面氧条件null及采用好氧KT2440路线、首步酶命名歧义、末端异构化基因未指定；对F4盐度填null，confidence字段多为medium/low用于未核项。主要限制与未知已说明，未见系统性把预测冒充观测或掩盖矛盾。个别性状高置信（严格好氧、烟酸根唯一碳源）属局部过强，非系统性误导；按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案有具体不确定性披露：氧条件为null故采用好氧nic途径的说明、NicAB命名与EC层面对应的说明、末端马来酸异构化基因未指定的说明；pH标low、盐度填null/unknown，部分体现诚实。但多条性状以high置信包装在无record_id的EVID_005与未核验的EVID_003上，证据粒度与置信标签不相称；未把预测系统性写成实证、未见掩盖主要矛盾，属若干/单点过度确信（5–6档），不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案uncertainties、confidence与null使用；用于评价披露质量，不证明科学内容正确。

</details>

## Qwen

答案SHA256：`1a89d13eb189d9447dd4dd36954828f3f527f69f0c6565763fda2c1e46b63a79`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> Route name is correct and five main-chain transformations plus enzyme/microbe per step are readable, but gold S06/maleate isomerase is omitted, the maleate intermediate is skipped, and only 3/15 traits are filled. Within the allowed D1 range &#91;1,4&#93;, 4 rather than 3 because most route modules are present.

<details><summary>V0.4理由与本行变化背景</summary>

档7–8：题面必需模块均有实质回应——route_scope.chosen_route_name原样填‘nicotinate degradation I’；steps S1–S5每步给主底物/主产物英文名+SMILES、一个酶+EC、一个微生物；organism_profiles按物种+菌株去重为1条并含全部15项性状字段；evidence_registry与uncertainties均交付。扣分点：gold主链为6步，答案把maleamate→maleate→fumarate并为S5一步（少交付一个独立步骤的酶，主要化学后果在D2评）；15项性状中12项为显式null（P15：明确未知≠遗漏≠错误，但仍反映完成度不足）。档内取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_107_question：Requires nicotinate degradation I main route and 15 traits.
- ANSWER_TEXT / ANSWER.steps/organism_profiles：Shows five steps and only three non-null trait values.

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> First four transformations broadly follow nicotinate-&gt;6-hydroxynicotinate-&gt;2,5-dihydroxypyridine-&gt;N-formylmaleamate-&gt;maleamate, but answer S5 directly writes maleamate-&gt;fumarate+ammonia, merging gold S05 (maleamate-&gt;maleate) and S06 (maleate-&gt;fumarate) and skipping the maleate intermediate/isomerase. This is an unsupported jump to central metabolite fumarate; 4 in 3-4 band.

<details><summary>V0.4理由与本行变化背景</summary>

档7–8：主链方向与化学成立——nicotinate→6-hydroxynicotinate→2,5-dihydroxypyridine(+CO2)→N-formylmaleamate→maleamate→fumarate；终点与题面/gold终产物fumarate一致；关键化合物SMILES与gold对应条目一致（如6-hydroxynicotinate、2,5-dihydroxypyridine、N-formylmaleamate、maleamate、fumarate）。局部缺陷：S5把maleamate→maleate（gold S05，EC 3.5.1.107）与maleate→fumarate（gold S06，EC 5.2.1.1）并为一步，未单列maleate中间体，并把顺反异构并入‘水解酶’；O2/NADH/细胞色素等辅因子未列（P103属局部计量缺陷，不cap）。既有错误未推翻主链主要结论→按四.5第4步档内扣分，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：Gold S05 gives maleamate-&gt;maleate; gold S06 separately gives maleate-&gt;fumarate; no direct one-step maleamate-&gt;fumarate.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> Five target steps are not confirmed as accepted (U); S05 is confirmed nonmatch (maleamate-&gt;fumarate instead of maleate) and S06 is missing. The confirmed KEY failure and terminal omission cap D3a &lt;=4. Available path/enzyme content is only partially usable and several ECs do not match accepted sets; 3 rather than 4 because no confirmed target success and the failure/omission boundary is only partly compensated by plausible first four transformations.

<details><summary>V0.4理由与本行变化背景</summary>

档5–6：酶名与反应类型大体匹配（羟化/双加氧开环/脱甲酰/水解），S3的EC 1.13.11.9与gold一致；但S1 EC 1.17.1.6（gold 1.17.2.1）、S2 EC 1.14.14.18（gold 1.14.13.114）、S4 EC 3.5.1.103（gold 3.5.1.106）、S5 EC 3.5.1.104（gold 3.5.1.107）与gold不一致，且缺maleate isomerase（EC 5.2.1.1）这一步。E0对上述EC均无条目（GAP-107-006/009/011/014/015），按P66/P73无法核验记UNRESOLVED，保留低分与待核标记、不cap；S5把异构反应归给‘maleamate hydrolase’属功能范围不匹配，但其水解酶活性本身正确，未推翻主要酶推荐。档内取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_107：Accepted enzyme/EC sets for required steps; used for EC comparison.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：Gold reaction sequence and terminal step evidence.

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> TaxID 294 identity as Pseudomonas fluorescens is supported by E0, and organism_gold PATHWAY_COMPLETE includes TaxID 294, supporting species-level whole-path capability. The answer uses species-only, no strain, and step-level P. fluorescens attribution is not separately listed for S01/S02/S05; 8 not 9.

<details><summary>V0.4理由与本行变化背景</summary>

档7–8：物种级身份Pseudomonas fluorescens / TaxID 294经E0核对SUPPORTED（ScientificName=Pseudomonas fluorescens、rank=species、lineage为Bacteria）；gold organism_gold记294为BSY-p00781的PATHWAY_COMPLETE菌，并在S03/S04/S06列P. fluorescens，为物种级微生物推荐与整路径能力提供正向支持。答案未给菌株（species级声称与其粒度一致，不得仅因未到菌株判错）；S01/S02/S05的步级归属在gold中记为P. putida/Alcaligenes等，答案未区分逐级证据（P69三层：身份≠步级能力≠全路径能力），属局部待确认。无已核实身份编造或跨类群错配→不cap；档内取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：Supports TaxID 294 = Pseudomonas fluorescens species identity; does not support strain-level or step-level activity.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_107：PATHWAY_COMPLETE row for TaxID 294 supports whole-path capability at species level; STEP rows do not list P. fluorescens for every answer step.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Only F7/F8/F9 are filled: F7 nicotinate, F8 nicotinate degradation, F9 nicotinate dehydrogenase. F9 has species-level step support, but F7/F8 lack official trait records in the snapshot (GAP-107-087/088/089) and all three use generic EVID_001. Other 12 traits are explicit unknown/null. D1 carries completeness; D4 5 for partial qualitative traits with insufficient key evidence.

<details><summary>V0.4理由与本行变化背景</summary>

档5–6：15项字段齐备，12项为显式null（诚实未知，完成度问题归D1，不在D4重复重扣）；填入的F7‘nicotinate’、F8‘nicotinate degradation’、F9‘nicotinate dehydrogenase activity’与路线能力方向一致，但均为与路线绑定的定性描述，不是物种/菌株级性状观测值；E0无对应性状记录（GAP-107-087/088/089），只能算证据不足的推断性填写（confidence=medium）。未见离谱数值、单位或条件错误，未见把物种级观测推广为全菌株性质。档内取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_107：P. fluorescens trait records; no official F7/F8 nicotinate trait record found.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_107：Shows pending/absent trait subfield scoreability, including F7/F8/F9 gaps.

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> Only one generic MetaCyc pathway locator (record_id null) is reused for all steps, enzymes, microbe and traits; no item-level or record-level citation is delivered. Decision-relevant groups are generic/unresolved. Score 3 in the 3-4 band: only a generic library/pathway name with weak mapping.

<details><summary>V0.4理由与本行变化背景</summary>

档3–4：全部结论只挂一条EVID_001（MetaCyc，record_id=null，locator仅路线名‘pathway: nicotinate degradation I’），却声明覆盖steps S1-S5、enzyme assignments、microorganism association与F7/F8/F9性状。决策相关组（CG01/CG02/CG03/CG05、CG08/CG09、以及claim-level为APPLICATION_CRITICAL的CG14）均无条目级可定位可核对证据；E0又无该路线/EC/性状记录（GAP-107-043等），故只能记GENERIC_SOURCE/UNRESOLVED_SOURCE，按P41属3–4档，‘部分关键结论可定位并核对’的5–6档条件不成立。疑似的来源-声称范围越界（路线记录用于性状）冻结证据无法核实，按P51/P56记UNRESOLVED、不判虚构不判CONTRADICTED、不cap；档内取4（claim_scope映射清楚故取高档）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：Shows EVID_001 is a generic MetaCyc pathway locator with no record_id.

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> The answer discloses oxygen null and many traits unknown, and uses medium confidence, but does not disclose that several EC numbers are mismatched/unverified, that EVID_001 is a generic pathway locator, or that maleamate-&gt;fumarate merges S05/S06. Some uncertainty is present but key limitations/conflicts are not clearly marked; 5 in 5-6 band.

<details><summary>V0.4理由与本行变化背景</summary>

档5–6：披露有实质内容——route_scope.oxygen_condition按题面保留null并说明；uncertainties明确P. fluorescens菌株与多数生理性状缺可核对来源故置null，未把预测写成实证观测。但证据性质标注过强：唯一来源标DATABASE_DIRECT/medium而record_id为空、无条目级定位；5步EC号与三项性状均以medium呈现，未标注‘与官方记录待核’；S5一步实为两个反应的合并也未披露。属有限/单点式过度确信而非系统性误导（P119）→档内扣分，不cap。档内取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows two uncertainty notes: oxygen null and missing P. fluorescens strain/traits.

</details>

## Grok

答案SHA256：`039aba3bf9cf32db9a4d1a8253219becaa8509aba7b3da562404cabad2bafc44`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案覆盖本题6个必答主链步，逐步给出底物/产物、酶/EC与微生物，并以fumarate为终点；15项性状全部出现，内部引用自洽，任务符合性程序为OK。主要模块完整、对应清楚；仅见题面氧条件为null而答案自设为aerobic等轻微表述/范围假设，未造成必要内容缺失，故留在9分档而非10分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_107：支持本案为LINEAR_UNIQUE、ordered_step_count=6、s4r2_order_pass=TRUE；用于核对完成6步主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_107：支持route_name=nicotinate degradation I、终端主产物=Fumarate；不支持答案任何未声称内容。
- SCOPE_ROW / SCOPE#BIOPATH150_107#CG04：题面氧条件为null（未指定），答案自设aerobic属轻微任务表述假设；未据此认定任务核心偏离。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 六步主链方向与顺序与gold一致：nicotinate→6-hydroxynicotinate→2,5-dihydroxypyridine→N-formylmaleamate→maleamate→maleate→fumarate，终点fumarate正确。关键转化和连接成立；S1电子受体/EC式表达、S3/S4缺H+、S5用ammonia而非ammonium等属局部计量/表达问题，P103下不改变主结论，且D2 9-10门未放行，故给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：支持六步主底物/主产物、有向顺序及关键转化；用于核对答案主链化学与连接，不证明具体酶蛋白实验活性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_107：支持终端主产物为Fumarate；不支持答案未声称的额外下游内容。

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 逐目标步核对：S02/S05/S06（答案S4/S5/S6）为已支持功能匹配；S01/S03/S04（答案S3/S2/S1）仍为ROUTE_HOLD_REPRESENTATION/UNRESOLVED，不按F或M计，也不把未命中accepted自动判错。当前可判S=3/6=0.50，落在C04的&#91;5,6&#93;；已支持步名/EC/反应对应清楚，未核步边界明确，故取6而非5；无已确认KEY失败，D-KEY4不触发，9-10门未放行。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_107：列出六步accepted酶名/EC及G4功能级支持粒度；支持功能/配对的参考范围，不支持具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：支持六步反应底物/产物与主链顺序；用于判断已支持步和U步的边界，不把表示待核自动判为错误。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 六步均填Pseudomonas putida KT2440。金标organism rows在物种级支持P. putida参与各步，PATHWAY_COMPLETE亦支持P. putida物种完成整条路线；但冻结E0/金标切片列的是P. putida taxid 303，未列KT2440/taxid 160488，故属物种级记录支持菌株级/全路径菌株声明的粒度不足（身份阶梯①），档内扣至7，不构成已核身份错误或cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_107：物种级P. putida对六步及PATHWAY_COMPLETE有支持；不支持KT2440/taxid 160488的菌株级身份或菌株级全路径能力。
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism：显示答案将六步统一绑定到P. putida KT2440/taxid 160488，并声称完整路径菌。

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P. putida物种级性状金标支持mesophilic偏好、non-halophilic、运动、杆状、革兰氏阴性、不产芽孢及基因组范围；答案15项填14项，F3_pH诚实null。若干KT2440菌株级或路径特异值（ATCC 47054、AE015451/6181863/61.6、F7烟酸根唯一碳氮源、F9 nic簇酶活）不在冻结记录中，F1“专性好氧”亦非金标直接字段；未发现已核矛盾，按同物种代表记录口径不因菌株不同直接判错，档内取7并保留局部未核。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_107：物种级P. putida支持温度偏好、盐度偏好、运动性、形态、革兰氏、产孢等观测；不提供KT2440菌株级ATCC/基因组/烟酸根唯一碳氮源精确核验。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_107：显示P. putida若干性状子字段可评/待裁范围；不把未核预测或范围端点升级为已观测精确值。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：显示答案填写的15项性状、null项与内部知识/文献来源标签。

</details>

### D5 来源与可核查性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案交付了EVID_001-EVID_006，并将步骤、酶、菌与性状逐项挂接；核心路线/酶/菌使用具体文献或数据库locator，不是纯GENERIC或全MISSING。但E0对EVID_001/002/003/004/005及EC/ATCC/AE015451无claim关联核验记录，多个性状仅EVID_006 INTERNAL_KNOWLEDGE_ONLY；未见已核错引或CRITICAL/SYSTEMIC。故落5-6档并取6：来源可定位但关键支持内容未能实际核对，且部分模块来源弱。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示实际交付的六条证据、来源类型、locator与claim_scope；不等于这些来源已在E0获事实核验。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_107：可核对S04 accepted EC为1.17.2.1；不能证明答案EVID_001或EC 1.17.1.5不存在/错引。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案uncertainties明确披露EC电子受体差异、6-羟基/6-氧代互变异构、温度/pH/盐度数值缺失及后续EC编号归属；F3_pH用null且confidence=unknown，符合诚实未知。扣分点在于KT2440菌株级身份/全路径能力、ATCC/基因组与部分性状仍以high/medium呈现，未充分标明其相对物种级记录的支持边界；但不确定性披露具体，非系统性把预测写成实证，故7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案主动披露的EC、互变异构与null数值限制；不证明其余high/medium标签均与证据强度相称。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_107：显示物种级P. putida支持，不提供KT2440菌株级身份；用于判断答案菌株级高置信披露边界。

</details>

## GPT5.6

答案SHA256：`8d488e240a5f6313eadd26f5f9207eb29d05b5c5eafcc564465331ae9b02a28e`。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案覆盖6步主链，逐步骤给出底物/产物名称、SMILES、酶名及同一P. putida KT2440 profile，route_scope原样填写nicotinate degradation I且终点为Fumarate。但仅第1步填写EC，其余5步EC为null；15项性状全部为null且无性状来源；evidence_registry仅一条INTERNAL_KNOWLEDGE_ONLY覆盖整条主链；程序路线诊断中gold S01仍为MISSING/NO_BOUND_RELATION。主要模块均有涉及，但若干必要内容遗漏或仅占位，落5–6档；主链和关联大体可读，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_107：ordered_step_count=6、LINEAR_UNIQUE；仅支持本题主链长度/形态，不要求全图旁支
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：gold六步主链及终点Fumarate；用于检查步骤覆盖和终点，不用于D1科学正确性加分
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_107：题面路径root=Nicotinate，terminal=Fumarate
- ANSWER_TEXT / 8d488e240a5f6313eadd26f5f9207eb29d05b5c5eafcc564465331ae9b02a28e：答案六步结构存在；第2–6步EC为null，全部15项性状为null，evidence_registry仅一条INTERNAL_KNOWLEDGE_ONLY

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 六步主链化学顺序与gold一致：Nicotinate→6-Hydroxynicotinate→2,5-Dihydroxypyridine→N-Formylmaleamate→Maleamate→Maleate→Fumarate；方向为降解正向，步骤间产物/底物连续，终点符合题面/gold的Fumarate。主要问题是多步缺失辅因子或副产物（如O2、NADH、细胞色素、H2O、CO2、H+）及部分计量简化，属P103所述局部计量缺陷，未出现首步错误、方向反转、主链断裂或跳至中心代谢物等关键错误；D2 nine_ten门为false，故取8档上限。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：支持六步主链的有机底物/产物、方向和连续性；不证明答案的辅因子完整性或酶EC配对
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_107：支持指定路线终点为Fumarate
- ANSWER_TEXT / 8d488e240a5f6313eadd26f5f9207eb29d05b5c5eafcc564465331ae9b02a28e：答案逐步给出主底物/主产物并保持链内连续；同时可见多步辅因子/副产物未列

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 六个目标反应中，S2-S6 的酶名与 accepted set 在 G4 策展粒度上可对应（缺 EC 不自动否定已支持功能）；S1 的底物/产物正确，但显式 EC 1.17.99.1 与 accepted EC 1.17.2.1 不同且无冻结记录，按 U 而非 F。因一个 KEY/MAJOR 的显式 EC 对仍未核，不能进入 7-8 或 9-10；支持部分清楚、缺口局部，取 5-6 档上沿 6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_107：给出六步 accepted enzyme names/EC；支持功能级匹配，不证明任意具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_107：给出各步底物/产物方向；用于核对答案主反应与 accepted 酶对应的化学步骤。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案把六步都归给 Pseudomonas putida KT2440（TaxID 160488）。Gold 有 P. putida TaxID 303 的步级记录及 PATHWAY_COMPLETE，但 E0 无 160488/KT2440 记录；物种级支持不能核实菌株级身份和步级能力。这是同物种菌株粒度/错配风险，未达到已核关键错误，故不 cap；5-6 档取 5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_107：Gold 列出 P. putida TaxID 303 的步级归属及 PATHWAY_COMPLETE；不支持 KT2440/TaxID 160488 的菌株级步骤能力。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部 15 项必需性状均以 null/unknown 返回，没有可评价的观测值或预测值。按 P44，全部必需性状为 null/空值时 D4 记 MISSING=1，不宣称检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_107：说明本题 15 项性状字段及可评分性结构；不把答案的 null 性状回填为观测值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部关键结论仅由 EVID_001 INTERNAL_KNOWLEDGE_ONLY 支撑，无 database、record_id、locator，无法定位到具体条目或文献。按 D5 六状态属 MISSING_SOURCE，不是已核实错引；1-2 档中取 2，因为答案至少显式登记了一条内部知识证据及其 claim_scope，并披露未核。

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案把酶/菌/反应归为低置信或内部知识，逐步给出 uncertainty，并在 uncertainties 中明确数据库记录、EC、菌株特异性证据未核；性状均显式 null/unknown，没有把预测写成实证观测。无系统性过度确信；仅缺少逐项 EC/菌株限制的完全展开，故 7-8 档取 8。
