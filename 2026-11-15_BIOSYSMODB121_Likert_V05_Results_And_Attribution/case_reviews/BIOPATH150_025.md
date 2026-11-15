# BIOPATH150_025：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-toluenecarboxylate degradation

污染物：p-Toluate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 47.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 56.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 52.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 48.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 40.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 30 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`b224ae2414bb1e48c98c1b2ea0f5c8088490acbaccd98b44d56ea5559e8e8ad0`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> 答案以P. putida mt-2的TOL质粒间位裂解途径替代题面锁定的4-toluenecarboxylate侧链氧化主链；S1起即生成二氢二醇而非gold的4-Carboxybenzyl alcohol，整条主链与指定路线不同。输出形式完整但任务路线明显偏离，按D1关键错误在&#91;1,4&#93;内取2。

<details><summary>V0.4理由与本行变化背景</summary>

六步主链、逐步酶+EC+对应菌、单菌去重(ORG_001)、15项性状全部出现、evidence_registry与uncertainties均交付，结构完整且符合任务格式；route_scope.chosen_route_name原样填&#x27;4-toluenecarboxylate degradation&#x27;。扣分点：题面要求&#x27;各项最强来源&#x27;，而答案全部为INTERNAL_KNOWLEDGE_ONLY且confidence多为medium/high，来源强度不达标；所交付的TOL间位裂解化学路线与gold BSY-p00243指定路线不同，属路线定位/命题歧义（已登记复核，非模块缺失）。综合7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：Gold主链为p-Toluate→4-Carboxybenzyl alcohol→4-Formylbenzoate→Terephthalate；不支持TOL间位裂解步骤。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：题面路线范围与gold终点为Terephthalate；不表示TOL途径可替代指定路线。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S6&#93;：答案实际交付TOL间位裂解六步，不是题面指定路线的S01-S03。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 答案给出的TOL间位裂解化学序列内部连续，六步均有底物/产物、SMILES与主要辅因子，方向为降解方向；S1双加氧、S2脱羧芳构化、S3间位开环、S4水解、S5水合、S6逆醛醇裂解在TOL途径内可成立。它不是题面指定路线，但D2按所答化学自身质量评价；化学可成立替换允许至6，取6。

<details><summary>V0.4理由与本行变化背景</summary>

TOL质粒间位裂解主链化学连续、方向正确：S1芳环cis-双加氧(p-toluate→cis-二氢二醇，含O2/NADH)，S2脱氢脱羧芳构化(→4-甲基儿茶酚+CO2+NADH)，S3儿茶酚2,3-间位开环(→5-甲基-2-羟基粘康酸半醛)，S4 C-C水解(→2-羟基己-2,4-二烯酸+甲酸)，S5水合(→4-羟基-2-氧代己酸)，S6逆醛醇(→丙酮酸+丙醛)。步骤连接与辅因子(S1 NADH/O2、S2 NAD+)基本守恒，属经典好氧间位裂解合理替代路线且明确声明。S5/S6对6碳甲基底物酶特异性为延展推断(中等置信、已披露)，故8档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;S1-S6&#93;：答案化学序列、辅因子与SMILES；用于评价替代路线自身连续性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：仅用于说明gold路线与答案路线不同；不作为TOL步骤的正面支持。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分7 → V0.5新分1，变化-6。

新裁判理由：

> 目标S01/S02为已确认目标失败：答案S1/S2是TOL间位裂解反应，不是gold的侧链氧化步骤；目标S03缺失/未绑定，答案S3为catechol 2,3-dioxygenase而非TsaD。S=0、F=2、U=1；已确认KEY失败适用D3a≤4且程序给定&#91;1,4&#93;。没有可用的目标步支持，按C05取1。

<details><summary>V0.4理由与本行变化背景</summary>

六步酶-反应类型对应一致：双加氧1.14.12.10/1.13.11.2、脱氢1.3.1.25、C-C水解3.7.1.9、水合4.2.1.80、醛缩4.1.3.39，EC大类与反应类型匹配，未见酶名与EC互相矛盾；答案区分了S2/S5/S6的推断性与家族/具体证据。但全部EC在冻结证据无记录，未能逐条核accepted name/reaction/状态，故7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：gold目标反应S01-S03；答案S1-S3产物/转化不同，不能获得目标信用。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_025：gold接受酶为4-toluene-sulfonate monooxygenase、4-sulfobenzyl alcohol dehydrogenase、TsaD；不支持答案的TOL酶对应。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S3&#93;：答案实际酶/EC与转化；S1-S3不匹配目标S01-S03。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案使用P. putida mt-2，身份在物种/菌株记录层可支持：TaxID 303为P. putida种级记录，BacDive 12880有mt-2 PaW1(pWWO)菌株记录。TaxID 303用于菌株声称属种级粒度；整条路径能力与逐步菌归属仍待核，但无已证伪。按身份阶梯为档内扣分，取7。

<details><summary>V0.4理由与本行变化背景</summary>

各步统一对应P. putida mt-2(TaxID 303)：物种级学名经E0核验(SUPPORTED)，bacdive 12880存在mt-2 PaW1(pWWO)菌株记录；菌株级身份用种级TaxID属粒度不足，答案已诚实披露；步级催化归属(CG08)与完整路径能力(CG09)冻结证据为UNRESOLVED待核。无跨类群/编造，按身份阶梯①粒度不足约7档、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持P. putida mt-2/pWWO菌株记录与26/30 °C培养记录；不支持完整p-toluate降解路径能力。
- E0_EVIDENCE / f3e0:taxid:303：支持P. putida种级TaxID 303的学名；不自动支持mt-2菌株级TaxID关联。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 15项性状均出现，F5为明确未知；多数性状对P. putida mt-2合理（革兰氏阴性、杆状、运动、不产孢、好氧、中温、非嗜盐、TOL底物利用等）。F2最适30 °C并非E0直接观测值（仅有26/30 °C生长记录）；F14使用KT2440的NC_002947代表mt-2，菌株来源需说明；其余多为内部知识。按主要性状可用、少量数值/来源问题取7。

<details><summary>V0.4理由与本行变化背景</summary>

性状针对P. putida mt-2：革兰氏阴性、直杆菌、运动、专性好氧、不产芽孢、TOL底物谱等属教科书正确；F14用KT2440(NC_002947, 6,181,873bp, GC61.5%)并诚实注明为mt-2质粒消除衍生株。但多数P. putida性状在冻结证据(gold为Comamonas testosteroni)无可核记录，F2最适30°C、F3 pH7.0属由记录外推(已标medium)，F5保藏填null(未利用可得记录)。无离谱值、无预测冒充高置信观测，5-6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持mt-2菌株记录、26/30 °C生长记录与保藏号集合；不支持最适温度或完整性状谱。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：答案15项性状原文与置信标签。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案的evidence_registry五条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；没有可定位的文献、数据库条目或计算记录。按D5六状态属MISSING_SOURCE低分档，未发现已核实虚构或错引，不cap。取2。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry EVID_001-005全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为空，无DOI/数据库条目/计算记录，按四.3为MISSING_SOURCE低分档；虽交付TaxID303、NC_002947、xyl基因与EC等可定位标识符，但不构成系统交付的来源记录，且以medium/high confidence包装内部知识。MISSING_SOURCE默认不cap(P34)。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案交付的来源记录均为内部知识声明，无外部可定位条目。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确标注证据来源为INTERNAL_KNOWLEDGE_ONLY，逐项给出confidence，并在uncertainties中说明未引用外部记录、S5/S6 EC不确定、F14为KT2440衍生株、TaxID为种级、代谢物同义名等。未把预测系统性写成实验观测，也未掩盖主要限制；仅部分高置信路线声称缺少外部来源，属局部扣分，取8。

<details><summary>V0.4理由与本行变化背景</summary>

D6为答案最强项：uncertainties逐条列明未引用外部记录、S5/S6 EC未确证、F14取自KT2440非mt-2、TaxID为种级、命名同义；每步对推断标medium并说明依据；alternative_branches明确is_part_of_scored_main_route=false，区分观测/推断、披露限制充分。仅个别性状值(最适30°C)略强于记录支持，8档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案对内部知识、EC不确定、F14菌株来源和TaxID粒度的披露。

</details>

## DeepSeek

答案SHA256：`43ff67a1b335cd6b60708229f2e970d00f950a212b43cd7fa4814edd288bfbc1`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 题面指定路线名已原样填写，S1–S3覆盖p-Toluate至Terephthalate的必答主链，steps、organism_profiles、15项性状和证据登记均存在；主要扣分为S2/S3未给EC、若干下游额外步骤SMILES为null，且答案把超出必答终点的下游延续也列入主链而未单独标明边界，因此落在7–8档，取8。

<details><summary>V0.4理由与本行变化背景</summary>

10步主模块齐全，每步有底物/产物名、酶、菌，15项性状均出现；但S7/S8/S9/S10多个SMILES为null、S2/S3缺EC、F4/F14显式未知，属若干必要字段遗漏，按6档（主要模块涉及但若干必要内容遗漏）取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / question：题面要求指定路线、每步底物/产物/酶/微生物及15项性状。
- ANSWER_TEXT / answer：答案覆盖必答三步并给出15项性状，但S2/S3的EC为null；超出终点的下游步骤有若干SMILES为null。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_025：冻结gold显示本题为LINEAR_UNIQUE、ordered_step_count=3，必答主链至Terephthalate。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 必答主链S1–S3的有机转化、方向与顺序和gold一致：p-Toluate→4-Carboxybenzyl alcohol（答案名4-(hydroxymethyl)benzoate）→4-Formylbenzoate→Terephthalate；未见方向反转或主链断裂。主要缺陷是S1未写O2/NADH、S2/S3未写NAD(H)等辅因子，属局部计量/表达不完整，按7–8档取8；额外下游不用于抬高D3a目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

S1-S3与gold主链一致：p-Toluate→4-(hydroxymethyl)benzoate→4-Formylbenzoate→Terephthalate，方向与结构正确；S4-S10为gold未覆盖的下游β-酮己二酸延伸，化学上连贯，但S4缺CO2、若干辅因子未列，按8档（主链可靠、局部计量/表达问题）取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：冻结gold逐步给出p-Toluate→4-Carboxybenzyl alcohol→4-Formylbenzoate→Terephthalate及反应方向。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_025：gold显示S01–S03的参考酶记录；不自动证明答案给出的不同酶名/EC。
- ANSWER_TEXT / answer：答案S1–S3的有机底物/产物与gold结构对应；辅因子未写入。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 按本题N=3必答目标S1-S3评价；S4-S10位于题面终点Terephthalate之后，属下游延续，不计入D3a目标信用。S1为KEY_ENTRY，答4-toluenecarboxylate methylhydroxylase/EC 1.14.13.186；官方ENZYME条目显示1.14.13.186已转至1.14.15.34，而1.14.15.34为tylosin生物合成P450，不能支持p-Toluate甲基羟化，构成酶名-EC矛盾及关键入口步错误。S2答4-(hydroxymethyl)benzoate dehydrogenase无EC，S3答4-formylbenzoate dehydrogenase无EC；二者功能名与目标反应方向相符，但均未落入accepted酶名/EC集合，也无独立证据确认，按C03保持U，不能计S。综合为少数功能线索可用、关键入口步存在已核矛盾、可用与失效边界只能部分区分，落C05 3分档。

<details><summary>V0.4理由与本行变化背景</summary>

S1-S3酶功能与gold步骤对应（S1单加氧/甲基羟化，S2醇脱氢，S3醛脱氢），名称基本合理；S2/S3缺EC，S1具体EC 1.14.13.186及下游EC在E0均无冻结记录，按7档（主要步骤有支持、若干条目待确认）取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps&#91;0&#93;.enzyme：答案S1将4-toluenecarboxylate methylhydroxylase与EC 1.14.13.186配对。
- E0_EVIDENCE / SUPP:ENZYME:1.14.13.186：官方条目：EC 1.14.13.186为transferred entry，指向1.14.15.34；不证明p-Toluate甲基羟化活性。
- E0_EVIDENCE / SUPP:ENZYME:1.14.15.34：官方条目：1.14.15.34为20-oxo-5-O-mycaminosyltylactone 23-monooxygenase（tylosin生物合成），非p-Toluate甲基羟化酶。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_025：本题accepted酶集合：S01为4-toluene-sulfonate monooxygenase/EC 1.14.99；S02为4-sulfobenzyl alcohol dehydrogenase/EC 1.1.1.257或1.1.1.M5；S03为TsaD/EC 1.2.1或1.2.1.62；用于核对答案酶名/EC是否落入accepted。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：必答三步反应底物/产物与方向；答案S1-S3产物与方向匹配，但D3a仅据此不能确认酶名/EC。
- ANSWER_TEXT / steps&#91;1&#93;.enzyme / steps&#91;2&#93;.enzyme：S2/S3未给EC，酶名分别为4-(hydroxymethyl)benzoate dehydrogenase和4-formylbenzoate dehydrogenase，均不在accepted名称集合内。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案推荐的核心微生物为Comamonas testosteroni，与gold的C. testosteroni物种身份（TaxID 285）一致，且gold PATHWAY_COMPLETE支持该物种完成相关路径；但答案额外指定菌株T-2，该菌株身份及菌株级能力在冻结证据中未获确认。主物种推荐可靠、仅具体菌株条目待核，落在7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

答案统一用Comamonas testosteroni T-2，物种与gold C. testosteroni（TaxID 285）一致，S1-S3物种级有gold支持；但T-2菌株、TaxID null、F5 DSMZ 6577及S4-S10全路径能力无E0/gold记录，按6档（合理候选、若干关键身份/作用范围未充分核验）取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_025：gold逐步微生物均为Comamonas testosteroni，TaxID 285，并登记PATHWAY_COMPLETE；未列出T-2菌株特异性。
- ANSWER_TEXT / answer：答案使用Comamonas testosteroni T-2并声称完整路径；物种名匹配，但T-2无冻结证据确认。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 基础分类性状中F10运动性true、F11 rod-shaped、F12 Gram-negative、F13非产孢与gold一致，支持部分性状可靠；但F2只填optimum 30、遗漏gold可观测的minimum 10/maximum 37，F4盐度全null而gold有0–2%观测，F14基因组全null而gold有GCA_016599875.1及GC/大小记录；F5 DSMZ 6577与gold JCM 6233不同且未核。总体为部分性状准确、关键数值/来源证据不足，落在5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全，F10-F13与gold物种级观测一致（运动、杆状、革兰阴性、不产孢），F2偏好mesophilic、F3 7.0等大体合理；F4/F14诚实null，F2 min/max与F5/F9等菌株级数值/活性缺E0或gold直接支持，按7档（主要性状可核实、少量条件/数值待确认）取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_025：提供C. testosteroni的观测/预测性状；F2观测min/max、F4盐度、F14基因组及F10–F13基础性状可核对。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_025：F2 minimum_c=10、maximum_c=37可计观测准确度，optimum_c无观测来源；F4 minimum=0、maximum=2可计观测准确度。
- ANSWER_TEXT / answer：答案F2 optimum=30但min/max为null；F4全null；F14全null；F5给DSMZ 6577。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案的evidence_registry只有EVID_001与EVID_002，二者source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；路径、酶、菌、性状的关键结论均无法追到可定位外部条目。按D5六状态，这属于MISSING_SOURCE；不是已核错引，默认不cap，但可追溯性极低，落在1–2档取2。

<details><summary>V0.4理由与本行变化背景</summary>

答案仅登记EVID_001/EVID_002，source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null；所有决策相关组均无可定位条目级来源，按MISSING_SOURCE低分档取2；这是缺失而非已核实错引，默认不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer：答案证据登记仅INTERNAL_KNOWLEDGE_ONLY，无外部数据库记录、DOI或可定位locator。

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案虽在evidence_registry标明INTERNAL_KNOWLEDGE_ONLY，但大量路径步骤和性状仍以medium/high confidence呈现，uncertainties为空数组，未说明预测/内部知识与可验证观测的边界，也未写明主要限制；属于多处过度确信、证据类型区分不足，但尚未达到系统性伪造观测的cap程度，取3–4档中的4。

<details><summary>V0.4理由与本行变化背景</summary>

答案在evidence_registry把全部来源标为INTERNAL_KNOWLEDGE_ONLY，形式上未冒充数据库直查；但无uncertainties说明，S4-S10及多项性状仍给high/medium置信，未披露T-2菌株/EC/下游能力等主要限制，属多处过度确信、主要限制未说明，按3-4档取4；未达系统性把预测写成实证的程度，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer：答案全部外部证据为INTERNAL_KNOWLEDGE_ONLY，但confidence多为medium/high，uncertainties为空。

</details>

## Kimi

答案SHA256：`8c3d86cc650df9a5c9a25ff8fb4753547671fb7503abab32301fd1a8b96977cd`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 题面指定路线为 4-toluenecarboxylate degradation，gold 主链为 p-Toluate→4-Carboxybenzyl alcohol→4-Formylbenzoate→Terephthalate；答案交付的是 P. putida mt-2 TOL 间位裂解路线，终点为 propionyl-CoA，未交付指定主链与终点。虽然 JSON 结构、7 步、酶菌和 15 项性状基本齐全，但核心任务路线严重偏离，按 D1 关键错误档取 3。

<details><summary>V0.4理由与本行变化背景</summary>

路线（7步，含主底物/主产物英文名与SMILES）、每步一个首选酶（名称+EC+基因）、每步对应微生物（同一菌株ORM_001去重合规）、15项性状（12项填写+3项明确未知+0项遗漏）、证据登记6条与不确定性4条均已实质交付，各模块对应清楚，格式完整。未给高分的理由：所交付路线的化学终点（pyruvate/propanal）与gold切片终点（terephthalate，3步主链）不一致，而题面只给路线名，形成题面/gold疑似冲突（已登记review_queue），任务符合度不能判为完全成立；此不确定性不归责答案，但也不宜给9–10档。取7–8档下沿。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / question_rendered_prompt_sha256：题面要求 route_scope.chosen_route_name 原样填写 4-toluenecarboxylate degradation，并给出该路线主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：本题 gold 终点为 Terephthalate，不是 propionyl-CoA。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：gold 主链三步为 p-Toluate→4-Carboxybenzyl alcohol→4-Formylbenzoate→Terephthalate；不支持答案的 TOL 间位裂解步骤作为本题主链。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案给出的 TOL 间位裂解路线在化学上基本连续，方向为 p-Toluate 向 propionyl-CoA 降解，主有机转化可成立；但存在 O2、NADH、H2O、CoA 等辅因子遗漏，S4–S7 对甲基化同系物的酶名/EC 适用范围有局部不确定，且该路线是题面指定路线之外的化学可成立替换，按 C06 限于 &#91;1,6&#93;。取 6：主链化学框架较完整，但辅因子与局部酶适用范围仍需修订。

<details><summary>V0.4理由与本行变化背景</summary>

主链7步化学连续且自洽，与TOL质粒间位裂解已知路径一致：双加氧（引入O2成顺式二氢二醇）→脱氢并脱羧芳构化（释CO2）→间位环裂解→水解断裂释甲酸→水合→醛醇裂解生成pyruvate+propanal→醛氧化酰化为propionyl-CoA；逐步核对碳数与氧化还原计量成立（如S4：C7H8O4+H2O→C6H8O3+CH2O2；S6：C6H10O4→C3H4O3+C3H6O），未见方向反转、起始步错误或无依据跳步。扣分理由：首步未列O2/NADH、末步未列CoA/NAD+，属局部计量缺陷（按P103不cap，7–8档内处理）；且该路线与题面路线名的对应关系无冻结证据可核（登记待核）。取7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;S1-S7&#93;：答案自述的 TOL 主链、步骤方向与产物。
- RUBRIC_CLAUSE / P103：主有机物转化正确但辅因子遗漏通常为局部计量缺陷；本题仍受指定路线替换的 &#91;1,6&#93; 范围限制。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分7 → V0.5新分1，变化-6。

新裁判理由：

> 程序事实为 S01/S02 已确认目标失败、S03 对齐未确认/缺失，S=0、F=2、U=1；S01/S02 为 KEY，命中 D-KEY4 上界 4。目标 S01 的 accepted 反应是 p-Toluate→4-Carboxybenzyl alcohol，S02 是 4-Carboxybenzyl alcohol→4-Formylbenzoate，而答案给的是 TOL 双加氧/间位裂解酶，不对应目标反应。错误路线内部酶自洽不获目标信用；几乎无可用目标催化对应，故取 1。

<details><summary>V0.4理由与本行变化背景</summary>

步骤酶与xyl基因/EC体系基本相符：xylE（EC 1.13.11.2 catechol 2,3-dioxygenase）、xylG（EC 3.7.1.9）、xylJ（EC 4.2.1.80）、xylK（EC 4.1.3.39）、xylQ（EC 1.2.1.10）与公认酶功能一致，未见酶名与EC大类互相矛盾（无水解酶解释羟化等错配），且答案对4个下游酶自标medium。扣分理由：全部EC在冻结快照中均无记录（GAP-025-002/005/009/011/015/018/020），无法按四.6核对accepted name/reaction/状态；S2的EC 1.3.1.67与自拟名&#x27;cis-Toluate dihydrodiol dehydrogenase&#x27;为待核项。取7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_025：目标 S01 接受 4-toluene-sulfonate monooxygenase 组分，S02 接受 4-sulfobenzyl alcohol dehydrogenase，S03 接受 TsaD。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：目标反应为 p-Toluate→4-Carboxybenzyl alcohol→4-Formylbenzoate→Terephthalate；不支持答案的 TOL 步骤。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案核心微生物为 Pseudomonas putida mt-2 / ATCC 33015，E0 的 BacDive 12880 支持 mt-2 PaW1(pWWO) 菌株身份及 ATCC 33015 保藏号；TOL 质粒与甲基苯甲酸代谢有答案所引 Williams &amp; Murray 1974 文献线索。未填 TaxID，未编造保藏号；但整条 TOL 路径能力未在 E0 机器核验。身份层可靠、能力层局部待核，取 7。

<details><summary>V0.4理由与本行变化背景</summary>

身份层面有冻结证据正向支持：f3e0:bacdive:12880为Pseudomonas putida mt-2 PaW1(pWWO)菌株记录，保藏号集合含ATCC 33015，与答案organism_name/strain/F5保藏号一致；f3e0:taxid:303为P. putida种级记录（答案ncbi_taxid留null，未编造）。全7步由同一菌株承担，符合TOL质粒xyl体系，未被写成&#x27;跨物种拼盘&#x27;。扣分理由：步级催化与全路径能力仅由无法核验的文献/数据库条目支撑（GAP-025-048/049），未达&#x27;关键步骤微生物身份、菌株、催化范围及整条路径能力均有充分且适用支持&#x27;的9–10档；gold菌为Comamonas testosteroni，属题面/gold冲突登记，不作菌株错配扣分。取7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持 mt-2 PaW1(pWWO) 菌株记录及 ATCC 33015 等保藏号；不自动支持整路径降解能力。
- ANSWER_TEXT / ANSWER.evidence_registry&#91;EVID_002&#93;：答案引用的 Williams &amp; Murray 1974 文献线索；未在 E0 中解析核验。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> F5 ATCC 33015 有 E0 支持；F3/F4/F14 如实填 null。F2 把 BacDive 的常规培养温度 30°C 写成 optimum_c=30，属于培养温度与最适值语义混淆；F1/F10–F13/F15 的 EVID_006 来源未在 E0 摘要中核验；F7/F8/F9 的 TOL 相关性状合理但未在 E0 核验。部分性状准确适用，但关键温度条件解释需修订、若干性状待核，取 6。

<details><summary>V0.4理由与本行变化背景</summary>

可核实部分：F5（ATCC 33015）与E0的mt-2记录保藏号集合一致；F8所述携带pWW0与E0的strain_designation &#x27;mt-2 PaW1, pWWO&#x27;相容。多数性状（F1好氧、F12革兰氏阴性、F10运动、F11杆状、F13不产孢）与该物种常识一致但快照无对应字段（GAP-025-063至072），按UNRESOLVED待核、不判错；F3/F4/F14如实置null（明确未知≠错误）。实质扣分点：F2把ATCC记录的常规培养温度30°C填入optimum_c（P113：培养温度≠最适温度；答案raw_text虽自述&#x27;未见可引用上下限&#x27;，结构字段仍误置），F15为低置信度叙述且无定位支持。故落5–6档上沿，取6分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持 ATCC 33015 与 26/30°C 生长阳性记录；培养温度不等于最适温度。
- RUBRIC_CLAUSE / P113：培养温度记录不等于最适温度；性状应按原测量语义解释。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案提供了 EVID_001–EVID_006 的证据注册与逐步映射，形式上可追溯；但 E0 仅核验 P. putida mt-2 身份/ATCC 33015 与培养温度，路线、酶-EC、整路径能力及多数性状来源均为自由文本且未解析，登记为 UNRESOLVED_SOURCE。F2 把培养温度 30°C 写成 optimum_c，来源只支持生长温度，按 CG11 LOCAL 错引登记；无 CRITICAL/SYSTEMIC，不 cap，取 6。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group逐组登记：决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）中，MetaCyc仅给路线标题无条目ID、UniProt仅给xyl基因名无登录号、PubMed仅书目、BacDive无record_id，均无可条目级核对的冻结记录→UNRESOLVED_SOURCE/GENERIC_SOURCE；CG07的保藏号与菌株记录在E0中获得正向支持（ATCC 33015、mt-2/pWWO），属&#x27;部分关键结论可定位并核对，其他模块仍缺映射&#x27;，落入5–6档；未发现经核实的不存在或不支持结论的引用，故severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不触发cap；F3/F4/F14等null项为MISSING_SOURCE。取5分（5–6档下沿）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持 mt-2 PaW1 菌株身份、ATCC 33015 与 26/30°C 生长记录；不支持将 30°C 解释为最适温度。
- E0_EVIDENCE / f3e0:taxid:303：支持 Pseudomonas putida 官方分类记录；不自动支持菌株级身份或能力。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案对未知性状填 null，给出 confidence、raw_text、uncertainties，并单列 alternative_branches 与下游延续，说明氧条件 null 与 XylG 水解支路选择；大部分预测/未知与推断边界有标注。但 F2 将培养温度写成最适值、部分 high/medium 置信声称超出现有 E0 核验，属局部过强而非系统性误导。取 7。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量较好：uncertainties明确写出题面氧条件null但TOL主链需分子氧、环裂解后水解支路与氧化支路择一并将XylF–XylH–XylI标为不属于评分主链、F3/F4/F14如实null的理由、XylQ以乙醛为经典底物对丙醛属延伸解释；步级confidence对4个下游酶标medium，下游延续另列并声明超出主链。扣分理由：EVID_001/002/004在无可定位记录的情况下整体标high（单点过度确信倾向，P119档内扣而非cap）；未披露&#x27;所走路线与题面路线名对应关系&#x27;这一主要不确定性。取7档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案自述的氧条件、支路选择、null 性状与 XylQ 置信限制。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；前者档内扣分，后者才是 cap 候选。

</details>

## Qwen

答案SHA256：`3938029cd3906b9d1ebe69f52931630bcfdd396b02c640ff84c5f85816a98fc0`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> 题面锁定 4-toluenecarboxylate degradation；答案实际给出 TOL 间位裂解替代路线，未交付 p-toluate→4-carboxybenzyl alcohol→4-formylbenzoate→terephthalate。任务偏离属D1关键错误；结构虽大体可读，但主任务符合性失效，取2。

<details><summary>V0.4理由与本行变化背景</summary>

D1评完整性与任务符合度。答案步骤结构（底物/产物名+SMILES、首选酶、对应菌）、15项性状、证据登记与不确定性说明均已交付，字段层面覆盖齐全；但答案在route_scope.chosen_route_name原样回填『4-toluenecarboxylate degradation』的同时，交付的是TOL型间位裂解化学（p-toluate→4-methylcatechol→开环→4-methyl-2-oxopent-4-enoate），与题面指定路线的化学主链不同，属任务参数偏离（P100：自称合规却交付不同化学路线），D1关键错误成立，cap≤4。档内取4：其余模块完整、未知项如实null、未见编造占位。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：支持目标终点为Terephthalate；不评价替代路线化学。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_025：支持本题目标主链为3步线性主链；不代表全部DAG旁支都必答。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：显示目标主链逐步反应；用于与答案S1-S3对照。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分4 → V0.5新分6，变化+2。

新裁判理由：

> 按D2独立化学质量评价：S1 p-toluate双加氧脱羧到4-methylcatechol、S2 2,3-开环、S3水解到4-methyl-2-oxopent-4-enoate+formate，方向与辅因子基本连贯；但中间体SMILES缺失、部分产物名称需核，且为替代路线，最高只能到6。

<details><summary>V0.4理由与本行变化背景</summary>

按合理替代路线四步判断：①题面已指定路线；②答案未声明替代路线，直接以该路线名承载不同化学；③替代路线无条目级可核证据（EVID_001为自由文本定位，GAP-025-045未解析，UNRESOLVED）；④偏离使主链结论失效，且首步化学本身有缺陷——1,2-双加氧酶只能完成去芳构化，不能同时完成所声称的脱羧，答案把双加氧酶与后续脱氢酶两步合并为一步并以同一酶承担，同时NADH/NAD+计入了本应抵消的净反应。主链止于4-methyl-2-oxopent-4-enoate，未达指定路线终点。D2关键错误成立，cap≤4；因S2开环、S3水解的化学与连接合理、辅因子列出、下游留白有说明，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：gold目标化学用于对照；答案替代化学按D2独立评价，不将替代内容回填目标完成。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：显示答案终点与gold终点不同；不单独据此判D2化学错误。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> S01为KEY_ENTRY且已核NONMATCH（答案p-toluate→4-methylcatechol，非目标4-carboxybenzyl alcohol）；S02/S03无目标credit；无S，confirmed_target_rate=0。D-KEY4确认KEY失败上限4；按C05选1（几乎无可用目标催化对应，核心已核失败使主推荐不可用）。

<details><summary>V0.4理由与本行变化背景</summary>

S2 catechol 2,3-dioxygenase 与『ring-cleavage dioxygenation』反应类型自洽（EC 1.13.11.2 在E0无冻结记录，只作UNRESOLVED待核）；S3『2-hydroxy-4-methylmuconate-semialdehyde hydrolase』功能与水解反应相符（EC如实null）；S1『toluate/benzoate 1,2-dioxygenase』作为候选酶合理，但不能单独完成所声称的脱羧，酶-反应对应不完整。属『有合理候选和部分支持，若干关键步骤仍缺具体核验』档（5–6），取5；无经核实的关键错误，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_025：支持目标逐步酶集合；不证明答案替代酶错误，但用于判断目标credit缺失。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：支持S01目标产物为4-Carboxybenzyl alcohol；答案S1产物为4-methylcatechol。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：支持目标终点；答案未交付该终点。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> P. putida mt-2身份有物种级TaxID 303与BacDive菌株记录支持，ATCC 33015在记录中；但目标菌为Comamonas testosteroni 285，且答案将同一菌写成全路径能力，路径能力未获冻结证据确认，属合理候选但关键身份/作用范围未充分核验，取5。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份 Pseudomonas putida 与官方记录相符（f3e0:taxid:303，record_status=CURRENT，species级）；f3e0:bacdive:12880为mt-2 PaW1(pWWO)菌株记录，支持菌株token与保藏号集合。但：答案自身只以EVID_001自由文本承载菌源；TaxID记录不含菌株token（F3R1CLM-004443 UNRESOLVED）；步级催化归属（F3R1CLM-004037）与整条路径能力（F3R1CLM-000244，complete_pathway_organism_profile_id=ORG_001）均无条目级证据。属『有合理候选和部分支持，若干关键作用范围未充分核验』档（5–6），取6；身份/能力三层分别核验，未见编造或跨类群错配，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持TaxID 303为Pseudomonas putida物种级记录；不支持菌株能力或全路径能力。
- E0_EVIDENCE / f3e0:bacdive:12880：支持P. putida mt-2菌株记录及ATCC 33015等保藏号；不支持目标Comamonas身份或TOL路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_025：支持gold目标菌为Comamonas testosteroni；不据此机械判P. putida在别的路线中不可能。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案15项性状均出现（12填、3明确unknown）；F5 ATCC 33015由BacDive 12880支持；F1/F6/F10-F13等P. putida分类/生理性状合理；F7-F9 TOL相关为低置信推断。主要性状与所指P. putida mt-2对应，无关键数值/单位错误，取7。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全，未知项（F3_pH、F4_salinity、F14_genome_basic）如实null，且F2只写偏好『中温』而把数值留null，未把培养温度26/30°C换算成最适或上下限，符合证据解释层纪律。可核部分：F5 ATCC 33015与f3e0:bacdive:12880保藏号集合一致（事实层SUPPORTED，不据此回填为答案来源）。其余性状（F1/F6/F7/F8/F9/F15）为种级通用知识，来源为INTERNAL_KNOWLEDGE_ONLY（EVID_002），芳香底物利用在12880面板中未被测试（裸名称列表≠阳性清单），无法核实。属『部分性状准确且适用，但关键项证据不足』档（5–6），取6；无预测冒充观测、无数值离谱或跨菌株外推的已核实错误，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持ATCC 33015等保藏号及26/30°C培养记录；不支持全部性状或路径能力。
- E0_EVIDENCE / f3e0:taxid:303：支持物种名；不支持具体生理/底物性状。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分3 → V0.5新分4，变化+1。

新裁判理由：

> EVID_001为MetaCyc自由文本locator、record_id为null，EVID_002为INTERNAL_KNOWLEDGE_ONLY；核心步骤/酶/菌均映射到同一粗粒度来源，F5等多项无条目级可核来源。E0无对应MetaCyc记录，属UNRESOLVED/GENERIC而非已核错引；D5取4（3-4档上沿）。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记来源状态：决策相关组（CG01/CG02/CG03/CG05/CG07/CG08）仅有EVID_001（MetaCyc自由文本定位，无record_id，GAP-025-045未解析）与EVID_002（INTERNAL_KNOWLEDGE_ONLY），无任何条目级可定位可核对结论；性状类组（CG10–CG13/CG15）仅有内部知识，属MISSING_SOURCE；CG09全路径声称无任何引用。E0未提供CONTRADICTED事实，EC与自由文本引文属EVIDENCE_GAP/UNRESOLVED，不判虚构、不计已核实关键错误，故不cap。决策相关组全部笼统/未核→3–4档，因单一自由文本源承载全部步骤与酶菌且性状全为内部知识，档内取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：E0仅含该菌株记录；不能核对EVID_001的MetaCyc记录。
- E0_EVIDENCE / f3e0:taxid:303：仅支持物种分类；不能核对路径/酶/性状来源链。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案多处标low/unknown，uncertainties列出EC、下游、氧条件等限制，未系统把预测当观测；主要缺点是EVID_001仍标DATABASE_DIRECT但为自由文本，且未明确声明路线偏离，故取8而非9-10。

<details><summary>V0.4理由与本行变化背景</summary>

答案不确定性披露较具体：route_summary点明中间体命名/酶编号/下游终产物不确定，每步有uncertainty字段，uncertainties列三条，central_metabolism_entry留空并说明理由，未知EC与性状填null，confidence多为low——未见把预测系统性写成实证观测。扣分点：EVID_001标为DATABASE_DIRECT却无record_id（单点强化证据类型），EVID_002用引文式raw_text包装内部知识，且未披露『所交付化学路线与题面路线名所指路线不一致』这一主要冲突。属单点/局部过度确信而非系统性误导，5–6档取6，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`ef144fcb2aeee5cc96eb6dc06620ab9fab6010ca4abc186b02e949b27224587d`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Task route lock is not met. The answer names the requested route but delivers a TOL meta-cleavage route (p-toluate -&gt; dihydrodiol -&gt; 4-methylcatechol -&gt; ring cleavage -&gt; pyruvate/propanal), while the required target is p-toluate -&gt; 4-carboxybenzyl alcohol -&gt; 4-formylbenzoate -&gt; terephthalate. The target terminal and both target intermediates are absent. D1 1-2 band: clearly deviates from task despite a complete-looking JSON; score 2 rather than 1 because the answer is readable and structurally complete.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：Shows the target S01-S03 chemistry and terminal terephthalate; does not support the answer&#x27;s TOL meta-cleavage steps.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：Shows the case pathway and terminal compound identity; not a full experimental proof.
- ANSWER_TEXT / ANSWER.steps：Answer&#x27;s delivered step sequence and products; used only to locate the task deviation.

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出的是TOL质粒meta-裂解替代路线（p-toluate→二氢二醇→4-甲基儿茶酚→开环→丙酮酸/丙醛），不是gold的甲基氧化主链（p-toluate→4-carboxybenzyl alcohol→4-formylbenzoate→terephthalate）。按替代化学独立评价，主链名称与多数转化方向、连续性大体成立，但S6产物SMILES“CC=CC(=O)C(=O)&#91;O-&#93;”仅5个碳，与名称2-oxohex-4-enoate（C6）不符；S7又以同一C5底物生成C6产物，造成原子守恒/连续性断点。该缺陷落在关键中间体与连接处，且替代路线按C06至多&#91;1,6&#93;；综合取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：本题gold终点为Terephthalate；仅说明目标路线终点，不支持答案meta-裂解路线。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：gold S01–S03为p-Toluate→4-Carboxybenzyl alcohol→4-Formylbenzoate→Terephthalate；不覆盖答案的TOL meta-裂解步骤。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S8&#93;：用于核对答案所给主链、底物/产物名称与SMILES；显示S6产物为C5而名称为C6，S7以其为C5底物生成C6产物。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> No target S01-S03 enzyme reaction is supported. S01 target is 4-toluene-sulfonate monooxygenase/EC 1.14.99, but the answer gives toluate 1,2-dioxygenase EC 1.14.12.10 and a dihydrodiol product. S02 target is 4-sulfobenzyl alcohol dehydrogenase, but the answer gives a dihydrodiol dehydrogenase. S03 target 4-formylbenzoate -&gt; terephthalate is absent. C04 gives C=0/3, C&lt;0.20 -&gt; &#91;1,2&#93;; score 1 because there is essentially no target catalytic credit and the core target recommendation fails. Alternative-route enzyme self-consistency does not earn target credit.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_025：Target S01-S03 enzyme rows and ECs; does not validate answer&#x27;s TOL enzymes as target enzymes.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：Target reaction direction and substrates/products.
- ANSWER_TEXT / ANSWER.steps：Answer&#x27;s delivered enzymes and reactions; used for target-credit comparison.

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Pseudomonas putida mt-2 identity is plausibly supported: E0 f3e0:bacdive:12880 records the mt-2 PaW1(pWWO) strain and includes ATCC 33015, and TaxID 303 is the correct species-level record. However the answer uses species-level TaxID 303 for a strain-level claim, assigns this organism as the whole-path organism for a foreign TOL route, and gives no E0 pathway-capability record. The target route&#x27;s gold organism is Comamonas testosteroni, so target-step microbial correspondence is not established. D3b 5-6 band: reasonable candidate and partial identity support, but key scope/capability remains unverified; score 5.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：Supports P. putida mt-2 strain record and ATCC 33015/CCUG 2480 collection numbers; does not prove whole-path capability or target-route membership.
- E0_EVIDENCE / f3e0:taxid:303：Supports species-level Pseudomonas putida TaxID 303; does not establish a strain-level TaxID or pathway capability.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_025：Target-step organism rows are Comamonas testosteroni; not a validation of P. putida for the target route.
- ANSWER_TEXT / ANSWER.organism_profiles：Answer&#x27;s identity and whole-path organism claim.

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 trait fields are present: 12 filled and 3 explicitly unknown (F3 pH, F4 salinity, F14 genome). The F5 ATCC 33015 entry is supported by E0 f3e0:bacdive:12880. Many general traits (rod, Gram-negative, motile, non-sporulating, aerobic, TOL degradation) are plausible for P. putida mt-2, but the quantitative temperature range, pH, salinity, and genome fields are missing or generic, and most trait values are species-level internal knowledge rather than strain-verified. D4 5-6 band: some traits accurate/applicable, key evidence and quantitative conditions insufficient; score 6.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：Supports mt-2 strain record, ATCC 33015 collection number, and 26/30 C culture records; does not establish all traits or optima.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_025：Gold traits are for Comamonas testosteroni 285, not the answer&#x27;s P. putida mt-2; used only to avoid misapplying target-organism traits to P. putida.
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：Answer&#x27;s delivered 15 trait fields and explicit nulls.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 is low because all decision-relevant groups rely on EVID_001-EVID_003, all labeled INTERNAL_KNOWLEDGE_ONLY. EVID_001 gives only a recalled KEGG map00622 and explicitly says it is not a real-time retrieval; EVID_002 and EVID_003 give no database/record. E0 can support only the P. putida mt-2 strain record and species TaxID, not the route, enzyme functions, or traits. This is MISSING_SOURCE across key groups, not verified mis-citation. D5 1-2 band: important conclusions are not traceably located; score 2.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：Supports only the mt-2 strain/collection record; cannot verify answer&#x27;s route, enzyme, or trait citations.
- E0_EVIDENCE / f3e0:taxid:303：Supports only species-level P. putida taxonomy; cannot verify TOL pathway or traits.
- ANSWER_TEXT / ANSWER.evidence_registry：Shows the answer delivered only internal-knowledge evidence entries.

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer is unusually explicit about uncertainty: it states the oxygen condition was null and that it interpreted the route as aerobic TOL meta-cleavage; it flags EC-number ambiguity, non-methyl official substrates, missing stereochemistry, species-level TaxID, unverified ATCC correspondence, and missing numeric traits. The evidence registry labels sources as INTERNAL_KNOWLEDGE_ONLY. Some high-confidence claims still rest on species-level memory, and it presents the TOL route as the main route without discussing the target side-chain alternative, so it is not 9-10. D6 7-8 band: most limitations are disclosed; score 7.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows the answer&#x27;s disclosed limitations and unknowns.
- ANSWER_TEXT / ANSWER.evidence_registry：Shows evidence-type labeling and confidence declarations.

</details>

## GPT5.6

答案SHA256：`2aefc2c7c5138b60b58c5b369433f4583509881c3902e558da9c8b65a363e9e2`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1主要看任务模块完成度、路线/条件遵守与交付完整性。答案虽原样回填了route_scope.chosen_route_name，但route_summary与两步实际化学给出的是CoA连接/厌氧脱芳构化路线，不是题面锁定route下的金标三步主链；缺少通向Terephthalate的终点步骤；15项性状全部为null，仅占位未提供可评价内容。覆盖了部分路径、酶和微生物，但核心终点与性状模块大部缺失，且存在明显路线偏离，属较弱档；因任务符合性关键失败，D1≤4，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_025_QUESTION：题面要求给出指定路线4-toluenecarboxylate degradation下的主链，并填写15项性状及来源；题面锁定路线，不得改选其他路线。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：金标主链为S01→S02→S03三步，S03生成Terephthalate；答案仅给出两步且未连到该终点。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：本题终点主产物为Terephthalate；答案止于2,5-Dihydro-4-methylbenzoyl-CoA，未交付该终点。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_025：本题ordered_step_count=3，支持金标主链为三步；答案仅两步且未覆盖终点。
- ANSWER_TEXT / ANSWER：答案实际交付两步、单一Thauera aromatica K172 profile，15项性状均为null；route_summary自述为CoA连接与厌氧脱芳构化。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2按实际交付化学独立评价。S1为对甲苯甲酸根经CoA连接生成4-methylbenzoyl-CoA并释放AMP/PPi，基本可辨认；S2为4-methylbenzoyl-CoA的还原脱芳构化，但电子载体未指明、主产物SMILES为null，且链止于2,5-Dihydro-4-methylbenzoyl-CoA，未继续到题面/金标主链的Terephthalate终点。该两步与金标三步氧化路线不同，但D2不把替代路线回填目标完成；未见已核原子明显不守恒或方向反转，因此不触发D2关键错误。主干部分成立但关键连接、终点和证据不足，属5–6档，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案S1为CoA连接、S2为脱芳构化还原，均只到第二步；S2使用未指明的Reduced electron carrier，产物SMILES缺失。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：金标主链为三步：p-Toluate→4-Carboxybenzyl alcohol→4-Formylbenzoate→Terephthalate；答案实际给出的是不同的CoA/脱芳构化两步，并停在中途。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_025：本题终点主产物为Terephthalate；答案未到达该终点。
- QUESTION_TEXT / BIOPATH150_025_QUESTION：题面氧条件未指定；路线名称锁定为4-toluenecarboxylate degradation。该信息用于判断D2实际化学连续性与终点，不用于把替代路线回填目标完成。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> N=3。S01/S02答案分别为EC6.2.1.25与EC1.3.7.8，产物为4-Methylbenzoyl-CoA与2,5-Dihydro-4-methylbenzoyl-CoA，和gold目标反应/产物不同，按已核目标反应不符记F；S03无酶信息记M。故S=0,F=2,M=1,U=0,C=0，C04落&#91;1,2&#93;；所有KEY/MAJOR目标酶对应失败或缺失，无目标催化信用，取1。错误路线内部酶自洽不获目标信用。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_025：S01 accepted为4-toluene-sulfonate monooxygenase EC1.14.99；S02为4-sulfobenzyl alcohol dehydrogenase EC1.1.1.257/1.1.1.M5；S03为TsaD EC1.2.1/1.2.1.62。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_025：S01 p-Toluate→4-Carboxybenzyl alcohol；S02→4-Formylbenzoate；S03→Terephthalate。
- ANSWER_TEXT / ANSWER：答案S1/S2给出不同反应/产物，S3缺失；仅证明交付内容，不证明目标酶对应。

</details>

### D3b 微生物身份与能力：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> gold三步对应菌均为Comamonas testosteroni（TaxID 285，GCA_016599875.1）。答案S1/S2均用Thauera aromatica K172，TaxID null、无基因组/步级能力证据，S3无菌；目标微生物身份与步级对应未建立，且与gold目标菌不一致。属多处物种/能力不匹配、缺少适用支持，落3-4档，取3。Thauera能力未核，不据此判已证伪。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_025：gold步级菌均为Comamonas testosteroni TaxID285，genome GCA_016599875.1，PATHWAY_COMPLETE=TRUE；不支持Thauera。
- ANSWER_TEXT / ANSWER：答案给出Thauera aromatica K172，TaxID null，无基因组编号；S3无微生物。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案organism_profiles&#91;0&#93;.traits的15项全为null且confidence=unknown；没有可评价的性状数值/对象值，按P44全null性状记D4 MISSING=1，不宣称已检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明15项性状全部未填写实质值，仅占位null。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；结论无法追到可定位文献/条目/计算记录，按MISSING_SOURCE低分档取1。无已核实错引，不触发D5 cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明答案实际交付来源仅为内部知识声明，无外部可定位记录；不证明结论真假。

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案有明确unknown/null、uncertainties与INTERNAL_KNOWLEDGE_ONLY/low标签，部分披露不确定性；但核心酶与微生物仍标medium，route_summary以“已知代表性主链”陈述替代路线，未清楚标为推断/替代，且未说明与目标主链边界。属部分披露但强度与依据不完全相称，落5-6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明答案有不确定性字段和内部知识标签，也在核心声称使用medium；不证明科学正确性。

</details>
