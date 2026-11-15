# BIOPATH150_122：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：γ-resorcylate degradation I

污染物：2,6-Dihydroxybenzoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 63 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 44.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 53 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 47 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 68.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 32.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`1fee4a76836808cc0850f6b065f223106aa24fd28c7ace468b97c94f2c1e8de0`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 任务要求的路线名、逐步底物/产物、酶与微生物、以及每个profile的15项性状均已交付；路线名原样，三份profile按物种+菌株去重，S3/S4复用ORG_003。主要扣分点是S1/S2未给EC且S4被同时写成主链步骤和downstream_continuation，属少量完整性/范围表达缺陷，不构成关键任务偏离。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块实质齐全：4步主链每步给底物/产物英文名与SMILES、酶名（EC未确认处如实null）、对应菌；3个菌各返回15项性状并逐项绑定evidence_id；证据登记与不确定性说明均存在。route_scope.chosen_route_name原样填写题面路线名，无任务参数偏离。档位7–8（大部分必要内容完整、关联清楚，少量遗漏），取8：步骤1–2的EC为null（指令允许未知填null）、S4为gold终点下游延续（按P29不加分不扣分）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_122_question：题面要求指定路线、逐步底物/产物、首选酶及EC、对应微生物、15项性状与最强来源；未知项填null。
- ANSWER_TEXT / ANSWER.steps：答案给出4步、每步底物/产物/酶/微生物，3个profile各15项性状，并登记内部证据ID。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_122：gold主链为LINEAR_UNIQUE，n_required=3；全图ordered_step_count仅材料数，不要求交付所有旁支。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_122：题面路线γ-resorcylate degradation I的起点为2,6-Dihydroxybenzoate，gold终点为Maleylacetate。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链有机转化与gold顺序一致：S1 2,6-dihydroxybenzoate脱羧到resorcinol+CO2；S2 resorcinol羟化为hydroxyquinol；S3 hydroxyquinol开环到maleylacetate；S4延续到3-oxoadipate也属合理下游。未发现方向反转、原子明显不守恒或无依据跳步。主要局部问题是S2写NADH而非gold的FADH2、S1/S3 SMILES的电荷/立体表示未完全规范化，因此落7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学正确且连续：S1 2,6-二羟基苯甲酸脱羧→间苯二酚+CO2（方向、原子正确）；S2 间苯二酚羟化→1,2,4-三羟基苯（hydroxyquinol）；S3 邻位开环→maleylacetate；S4 maleylacetate还原→3-oxoadipate。前3步与gold逐步一致，S4为正确的β-酮己二酸下游延续。局部问题：S2以NADH替代gold的FADH2（就Trichosporon羟化酶语境可接受）、H+等小无机物普遍省略——按八.辅因子条款属局部计量缺陷（7–8档内），不改变主要结论。档位7–8，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：gold逐步方向与主有机转化：2,6-dihydroxybenzoate→resorcinol+CO2，resorcinol→1,2,4-benzenetriol，1,2,4-benzenetriol→maleylacetate。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_122：支持gold各步酶名/EC与反应对应；不证明答案S2的NADH机制或具体菌株活性。
- ANSWER_TEXT / ANSWER.steps：答案逐步骤给出底物、产物、反应类型及S1-S4连接关系。
- RUBRIC_CLAUSE / R2-62：与gold不同不自动错误；任务方向/主链失败才影响D2。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 本题D3a目标N=3。答案S1（入口脱羧）、S2（中间羟化）、S3（末端开环）均交付了对应酶；S4为gold终点maleylacetate之后的额外下游，不计入本题D3a目标N。S1酶名gamma-resorcylate decarboxylase与S3酶名+EC 1.13.11.37与accepted集合相符，S2 resorcinol hydroxylase未命中accepted的resorcinol 4-hydroxylase (FADH2)/EC 1.14.14.27且EC为null。由于S1/S3仍受表示等价挂起、S2为未入accepted的待核，三目标均不能确认S，也无已核失败F、漏答M或已确认KEY失败，故不触发D-KEY4上界；按C05部分主干有适用支持且关键MAJOR仍U，不能进入7分以上，取5分。

<details><summary>V0.4理由与本行变化背景</summary>

酶-反应对应科学正确：S1 γ-resorcylate decarboxylase（对应gold S03的gamma-resorcylate decarboxylase）、S2 resorcinol hydroxylase（对应gold S02的resorcinol 4-hydroxylase）、S3 hydroxyquinol 1,2-dioxygenase EC 1.13.11.37（与gold一致，PnpC）、S4 maleylacetate reductase EC 1.3.1.32（PnpD）功能类别均匹配，无EC大类/反应类型矛盾。扣分：S1、S2的EC为null（gold对应4.1.1.103、1.14.14.27未填）；已填两个EC在E0无冻结记录（GAP-122-002/005），核验态为UNRESOLVED。档位7–8，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;S1-S3&#93;.enzyme：答案实际交付的三个目标酶字段：S1 gamma-resorcylate decarboxylase（EC null）；S2 resorcinol hydroxylase（EC null）；S3 hydroxyquinol 1,2-dioxygenase（EC 1.13.11.37）。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_122：本题accepted酶行：S03 gamma-resorcylate decarboxylase EC 4.1.1.103；S02 resorcinol 4-hydroxylase (FADH2) EC 1.14.14.27；S01 hydroxyquinol 1,2-dioxygenase EC 1.13.11.37。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：目标反应与终点：S03 2,6-dihydroxybenzoate→resorcinol+CO2；S02 resorcinol+FADH2+O2→1,2,4-benzenetriol；S01 1,2,4-benzenetriol+O2→maleylacetate，gold终点为Maleylacetate。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 微生物候选总体合理但身份粒度/证据不足：S1用Rhizobium sp.且TaxID 354无冻结记录；S2用Trichosporon cutaneum且无TaxID/记录；S3/S4用P. putida DLL-E4，E0的TaxID 303只支持Pseudomonas putida物种名，不包含DLL-E4菌株。未发现跨kingdom或明显编造身份，故不cap；但若干关键身份/作用范围仍未充分核验，落5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

菌-步对应总体合理：S1 Rhizobium 对应γ-resorcylate decarboxylase（gold该酶来源即Rhizobium sp. MTP-10005，属级正确）；S2 Trichosporon cutaneum 为经典resorcinol hydroxylase来源（gold未收，属合理替代）；S3/S4 Pseudomonas putida DLL-E4 的PnpC/PnpD为真实单步能力来源。答案未把单步菌写成全路径菌（complete_pathway_organism_profile_id=null，逐步骤独立给菌），避免了八.D3b所禁的“单步=全路径”外推。身份缺口：Rhizobium仅到属并给TaxID 354（E0无记录，GAP-122-018，UNRESOLVED）；P. putida TaxID 303学名SUPPORTED，但菌株DLL-E4未在记录names中出现（菌株级UNRESOLVED）；Trichosporon未给TaxID。按身份阶梯①粒度不足档内扣，不cap。档位5–6，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_122：gold Step微生物包括Rhizobium sp. MTP-10005、Sphingomonas sp. RW1、Rhodococcus等；不等于答案所用的Rhizobium sp. TaxID 354、Trichosporon cutaneum或P. putida DLL-E4已获支持。
- E0_EVIDENCE / f3e0:taxid:303：TaxID 303记录支持Pseudomonas putida物种学名与当前分类状态；不支持菌株DLL-E4身份或该菌株完成整条路径能力。
- ANSWER_TEXT / ANSWER.organism_profiles：答案给出Rhizobium sp.、Trichosporon cutaneum、P. putida DLL-E4及TaxID字段；用于核对身份粒度与step归属。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 每个profile均给15项，未知项多按null/unknown如实处理；P. putida的革兰氏阴性、杆状、好氧等一般性状合理。主要问题是关键数值/条件多缺证据，Rhizobium F7把脱羧酶活性外推为可利用γ-resorcylate/间苯二酚生长，Trichosporon F12写“革兰氏阳性”对真菌包膜表述不够准确；故属部分性状准确但关键项证据不足、条件解释需修订，取6。

<details><summary>V0.4理由与本行变化背景</summary>

性状按属/种水平一般知识填写，数值型关键性状（温度区间、pH、盐度、保藏号、基因组）多诚实null，未见编造离谱数值，也未见把物种级耐受数值硬写成全物种普遍耐受范围。问题：几乎所有已填性状（尤其Rhizobium sp.、Trichosporon cutaneum）在冻结证据中无对应记录，核验态UNRESOLVED；P. putida的多项为种级知识套用于菌株DLL-E4；F7/F8有由单酶活性外推底物利用/降解能力之处（虽已标low/medium并写明“推断”）。档位5–6（部分性状准确且适用，但关键项证据不足），取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_122：gold性状记录集中于Paraburkholderia、Sphingomonas、Burkholderia、Rhizobium MTP-10005、Rhodococcus、Corynebacterium；不覆盖答案Rhizobium sp. 354、Trichosporon cutaneum或P. putida DLL-E4。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_122：指出许多性状子字段在冻结输入中不可观测或仅completeness_only；答案大量null不应当作科学错误。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;&#93;.traits：用于核对答案实际填写值、null/unknown声明和条件外推；不把内部知识来源当作观测证据。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案的evidence_registry全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为空，无法沿具体路径、酶菌或性状追到可定位文献/数据库条目。虽建立了局部EVID_00x与claim_scope的映射并诚实披露内部知识限制，但这仍属MISSING_SOURCE而非可核对来源；无已核实错引，故不触发D5 cap，落1–2档取2。

<details><summary>V0.4理由与本行变化背景</summary>

全部结论证据均为INTERNAL_KNOWLEDGE_ONLY自我声明：evidence_registry EVID_001–007的database/record_id/locator全为null，无数据库条目或文献可定位支持具体结论，符合MISSING_SOURCE定义。按四.3/MISSING_SOURCE属缺失而非误导，默认不cap；无已核实错引（编号类声称EC 1.13.11.37/1.3.1.32、TaxID 354均UNRESOLVED，TaxID 303仅学名部分SUPPORTED，无CONTRADICTED）。档位取低分档，因答案虽自行标注内部知识且给出可追的酶名/EC/基因/菌名，但无任何可定位记录，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：所有证据source_type均为INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator，不能定位外部记录。
- ANSWER_TEXT / ANSWER.uncertainties：答案承认全部证据为内部知识、未能提供数据库记录编号或文献定位；提高D6诚实性，但不回填D5来源。
- E0_EVIDENCE / f3e0:taxid:303：E0可核对TaxID 303的物种名，但答案未把它作为该步来源登记；且该记录不支持DLL-E4菌株。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案较清楚地披露了内部知识、未知EC/菌株、路线I/II变体可能差异、以及大量性状null；把预测/内部推断与未知分开，未系统性把预测写成实证。局部问题是S3/S4酶EC及P. putida若干一般性状用了high confidence，而其来源仅为内部知识，置信表述略强；但整体限制、冲突和待验证点已说明，属良好档取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体而非笼统：uncertainties明确声明全部证据为内部知识、路线I/II变体划分可能出入、EC与菌株未确认、数值性状缺来源，并把evidence_registry的source_type统一标为INTERNAL_KNOWLEDGE_ONLY。扣分：多处性状（如P. putida F1/F6/F11/F12/F13、Rhizobium F12）在仅有内部知识支撑下仍标confidence=high，个别结论强度略超依据，属单点/多点过度确信而非系统性误导，不cap。档位5–6，取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：明确说明全部证据为内部知识、路线I/II变体可能差异、EC/菌株未确认、性状多为null。
- ANSWER_TEXT / ANSWER.steps&#91;&#93;.uncertainty：逐步披露酶EC、菌株、PnpC/PnpD背景及风险；部分酶confidence=high与内部知识来源略不相称。
- RUBRIC_CLAUSE / R2-45：诚实null与编造严格区分；D6可因准确披露未知获得较高分。

</details>

## DeepSeek

答案SHA256：`b0c3b040ce9c0cccd5ed9e6990b653047c8924c4f96d4a8feff7fc8b09845874`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案结构完整，给出4步、酶、菌与15项性状；但题面锁定γ-resorcylate degradation I，答案S1-S2实际走2,6-dihydroxybenzoate 3-monooxygenase→2,3,6-trihydroxybenzoate→1,2,4-trihydroxybenzene，未交付gold S03 gamma-resorcylate decarboxylase（2,6-Dihydroxybenzoate→Resorcinol+CO2）和S02 resorcinol 4-hydroxylase（Resorcinol→1,2,4-Benzenetriol）。属严重偏离指定路线，D1关键错误成立，cap≤4；因模块形式完整、可读，取4。

<details><summary>V0.4理由与本行变化背景</summary>

七项模块齐备：4步主链、每步酶与EC（S2 EC填null）、每步微生物（同一P. putida去重引用ORG_001）、15项性状外壳齐全、route_scope.chosen_route_name原样填“γ-resorcylate degradation I”。完整度高（近7-8档），但主链化学与题面指定路线的canonical顺序不符：本题路线为脱羧先行（2,6-DHB→resorcinol→1,2,4-Benzenetriol→Maleylacetate），答案改为羟化先行（经2,3,6-三羟基苯甲酸），且未声明为替代路线——属任务符合度扣分而非模块缺失，综合6档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：S03行支持2,6-Dihydroxybenzoate→Resorcinol+CO2经gamma-resorcylate decarboxylase EC 4.1.1.103；S02行支持Resorcinol→1,2,4-Benzenetriol经resorcinol 4-hydroxylase EC 1.14.14.27；不扩展到答案替代路线。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_122：支持该题gold主链为LINEAR_UNIQUE、ordered_step_count=3。
- ANSWER_TEXT / ANSWER_BEGIN：答案实际交付S1-S2为3-monooxygenase/decarboxylase替代路线。
- QUESTION_TEXT / QUESTION_BEGIN：题面route_scope.chosen_route_name为γ-resorcylate degradation I且不得改选。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分5 → V0.5新分7，变化+2。

新裁判理由：

> D2按所答化学质量独立评价，不把替代路线回填目标完成。答案S1羟化、S2脱羧、S3开环、S4还原总体连贯，S3与gold终点开环一致；但S1/S3/S4未列O2/NADH/FADH2等辅因子，S2未列CO2副产物，属局部计量缺陷；额外S4下游依P29不扣分。主链关键转化可辨认，少量局部问题不改变主要化学结论，故7。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学内部自洽：羟化→脱羧→双加氧开环→还原，方向与计量无明显违背（2,3,6-三羟基苯甲酸去羧基计为1,2,4-苯三酚，结构可对应）；S3开环 1,2,4-benzenetriol→Maleylacetate 用 hydroxyquinol 1,2-dioxygenase EC 1.13.11.37，与gold S01精确一致。但入口两步与题面指定路线canonical顺序（脱羧先行）不同，且S1(EC 1.14.13.111)与S2(EC null)缺核验依据；S4延伸至3-oxoadipate超出gold终点属额外交付（不扣覆盖）。按四.5‘与gold不同不自动判错’办理，未证实部分登记待核→5档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：S01/S02/S03行支持gold各步底物、产物、方向与酶反应类型，用于对照答案化学连续性；不自动判定答案替代路线错误。
- ANSWER_TEXT / ANSWER_BEGIN：答案实际给出S1-S4的底物/产物/反应类型与酶，用于评价所答化学质量。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_122：支持根物2,6-Dihydroxybenzoate与gold terminal main product Maleylacetate。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 按目标反应逐项核对：answer S3（1,2,4-trihydroxybenzene→maleylacetate，hydroxyquinol 1,2-dioxygenase，EC 1.13.11.37）与accepted S01名称/EC/产物对齐，可判S=1；S02（resorcinol 4-hydroxylase, EC 1.14.14.27）和S03（gamma-resorcylate decarboxylase, EC 4.1.1.103）在答案中无对应反应/酶，判M=2。N=3，C=1/3，落&#91;3,4&#93;；两项KEY目标M触发D-KEY4上界4，带内取3：仅少数目标可用且关键入口/中间步缺失，主功能严重受损。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶名与反应类型一致（monooxygenase/decarboxylase/dioxygenase/reductase），无EC大类与反应矛盾；S3 hydroxyquinol 1,2-dioxygenase EC 1.13.11.37 与gold精确一致（gold支持）。但S1 EC 1.14.13.111、S4 EC 1.3.1.32 在E0无冻结记录（GAP-122-004/010/005/013→UNRESOLVED），S2 EC为null。合理候选+部分支持、多关键步缺具体核验→5档；无已核实酶-反应错配，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_122：列出S01-S03 accepted酶名/EC；S01支持hydroxyquinol 1,2-dioxygenase/EC 1.13.11.37，S02/S03 enzymatic targets未在答案中交付。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：给出各步底物/产物与方向；支持S01目标产物Maleylacetate，同时显示答案缺少S02/S03目标反应。
- ANSWER_TEXT / ANSWER.steps S1-S4：显示answer S3可对应S01；S1/S2为不同上游路线，不获得S02/S03目标信用。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> P. putida与TaxID 303仅支持物种名身份；答案无strain，且把同一物种用于全部步骤并设置complete_pathway_organism_profile_id=ORG_001，构成无strain/无步骤能力证据的整路径能力声称。gold步骤菌为其他菌株，但不据此证明P. putida不能；分数落在3–4档，取4因身份本身有效、错误边界清楚，但步骤级与整路径能力仍实质缺失。

<details><summary>V0.4理由与本行变化背景</summary>

全4步统一推荐 Pseudomonas putida（无菌株、TaxID 303）。身份层：TaxID 303 学名与官方记录匹配（SUPPORTED, f3e0:taxid:303）；但gold本题各步微生物为Paraburkholderia/Sphingomonas/Rhizobium/Rhodococcus/Corynebacterium等，未含P. putida；P. putida对各步的催化归属(CG08)与整条路径能力(CG09)均UNRESOLVED（E0无反应级/路径级证据）；且仅种级、无保藏号/菌株，以同一菌覆盖整条路径。属合理属级候选但作用范围与整路径能力未核→5档；能力未核登记UNRESOLVED，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida的官方分类名/物种身份，不支持任何菌株、单步催化或整路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_122：gold列出S01-S03的步骤相关菌；未列P. putida不等于已证明P. putida不能，但答案没有给出相应步骤证据。
- ANSWER_TEXT / ANSWER.microorganism+complete_pathway：显示答案使用同一物种并明确声称整路径profile ORG_001，但没有strain或步骤能力依据。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项字段齐全，部分通用性状（如Gram-negative、rod-shaped、motile、non-spore-forming、aerobic respiration）可作为部分可用信息；但F2给出4/30/37°C并称中温菌，E0仅见BacDive 12880菌株培养记录26/30°C，不能支持最小/最适/最大；F8/F9还给出未定位的芳香物降解与通路酶活。多项关键数值/能力仍超出证据，落5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状均给出外壳；P. putida种级多项为教科书可核事实（Gram-negative、rod-shaped、polar flagella运动、非产孢、专性需氧、化能异养）方向正确；F4/F3/F5/F14诚实填null(unknown)。但F2温度min4/opt30/max37无冻结记录佐证，BacDive 12880仅见26/30°C培养记录（培养温度≠最适/上下限，解释层明示），max37属外推；F8/F9把未核实的降解/酶能力重述为性状（无证据）。部分性状准确、关键项证据不足+个别外推→5档；无‘预测冒充观测/数值离谱/物种级滥推全菌株’的已核实关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：仅支持P. putida菌株mt-2 PaW1的保藏号与26/30°C培养温度记录；不支持物种级温度上下限/最适值，也不支持F8/F9能力。
- E0_EVIDENCE / f3e0:taxid:303：仅支持物种名，不支持性状数值。
- ANSWER_TEXT / ANSWER.traits：显示15项已填、4项显式unknown；同时显示多个数值/能力以medium confidence给出但无相应定位来源。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> evidence_registry仅有EVID_001/EVID_002，二者source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null；路径、酶、菌、性状结论均无条目级可定位来源。按D5 1–2档取1。因MISSING_SOURCE默认不作为已核实错引cap，key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅2条，source_type均 INTERNAL_KNOWLEDGE_ONLY（EVID_001/002），database/record_id/locator均null，无可定位条目。按P34→全部MISSING_SOURCE；决策相关组（CORE/APPLICATION_CRITICAL）均MISSING_SOURCE→低分档（P41/P98），默认不cap。无已核实错引（无可核对象，查不到≠虚构）→severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，key_error=N。低分档取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示答案仅交付内部知识声明，无数据库条目、文献 DOI/定位或计算记录可核对。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案有confidence字段、null与一条uncertainties说明，但多数内部知识声称仍以medium confidence呈现，complete_pathway ORG_001、精确温度与F8/F9能力未明确标为推断/待核；不确定性说明过于笼统，部分结论强度超过依据。落5–6档取5，未达系统性误导cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案以confidence标签（medium/low/high/unknown）与INTERNAL_KNOWLEDGE_ONLY来源类型标注证据性质；F4/F3/F5/F14等未知诚实置null，uncertainties列出‘部分酶EC、菌株身份、多项性状未确定’。但说明较笼统，且对未核实的整条路径与P. putida路径能力仍给medium置信，结论强度超过依据。属披露存在但笼统、部分过度确信，非系统性把预测写成实证→5档，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.confidence+uncertainties：显示答案使用了confidence与unknown/null，但也显示关键能力/数值以medium confidence给出且限制说明笼统。
- E0_EVIDENCE / f3e0:taxid:303：仅支持P. putida名称；不能为整路径能力或精确性状提供观测级支持。

</details>

## Kimi

答案SHA256：`9c4a715c2f591f1e3007c5d587a489148f4562fa4b6fb10fa2437452c6d180e6`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> 答案覆盖路径、酶、菌、15项性状与来源模块，但按锁定路线γ-resorcylate degradation I核对，gold必需三步为S03 2,6-DHB→resorcinol、S02 resorcinol→hydroxyquinol、S01 hydroxyquinol→maleylacetate；答案S1把前两步合并为直接2,6-DHB→hydroxyquinol，缺失resorcinol中间体与对应酶步，S3又延伸到gold终点Maleylacetate之后。只命中1/3必需主链步，属核心任务模块大部缺失/严重不完整，D1关键错误成立，在&#91;1,4&#93;内取3。

<details><summary>V0.4理由与本行变化背景</summary>

8分：题面指定的γ-resorcylate degradation I被原样填写，steps、organism_profiles、15项性状字段和evidence_registry均已交付；每步给出底物/产物、酶与微生物，性状均有字段外壳。不足在于第3步把3-oxoadipate作为主链延伸、若干性状为null，完整性未到9–10档，但主要模块均实质回应。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：冻结gold要求S03 2,6-DHB→resorcinol、S02 resorcinol→hydroxyquinol、S01 hydroxyquinol→maleylacetate；不支持答案S1直接生成hydroxyquinol或S3作为评分主链终点。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_122：支持路线名γ-resorcylate degradation I与gold终点Maleylacetate；不支持把3-oxoadipate作为本题主链终点。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分3 → V0.5新分5，变化+2。

新裁判理由：

> 答案自身三步连续，辅因子多数有列（O2、NADH），S3 maleylacetate reductase步骤化学上可成立；但S1把gold的脱羧→羟基化两步合并为直接单加氧反应，关键中间体resorcinol及连续转化被省略，属关键中间体/连接需实质修订。未发现可据冻结证据判定的原子不守恒或方向反转，故不另立D2关键错误。按base_ranges D2允许范围&#91;2,5&#93;，取5。

<details><summary>V0.4理由与本行变化背景</summary>

3分：主链首步错误。gold首步为2,6-Dihydroxybenzoate经γ-resorcylate decarboxylase脱羧生成Resorcinol+CO2；答案S1却把2,6-DHB直接经单加氧酶生成2-Hydroxyhydroquinone并释放CO2，跳过Resorcinol中间体。S2 hydroxyquinol→maleylacetate与S3 maleylacetate→3-oxoadipate本身方向基本合理，但不能弥补首步错误；符合首步错误的关键错误cap≤4，档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：gold显示2,6-DHB→resorcinol→hydroxyquinol的连续转化；不支持把两步合并为直接2,6-DHB→hydroxyquinol作为等价主链。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 按目标反应逐项核：S01目标hydroxyquinol→maleylacetate可由答案S2的hydroxyquinol 1,2-dioxygenase EC 1.13.11.37对应，accepted集明确接受该酶/EC，记1个可用目标。S03目标2,6-DHB→resorcinol（gamma-resorcylate decarboxylase, EC 4.1.1.103）未交付，答案S1改为直接单加氧生成hydroxyquinol；S02目标resorcinol→hydroxyquinol（resorcinol 4-hydroxylase, EC 1.14.14.27）也未交付。N=3，已核可用S=1，M/F=2，C≈0.333落入&#91;3,4&#93;；其中S03为KEY_ENTRY且缺失，D-KEY4上界4不改变本带。档内取3：仅一个目标酶步可用，关键入口/中间步失效边界清楚。

<details><summary>V0.4理由与本行变化背景</summary>

4分：S1核心酶功能与gold不符：答案给“2,6-dihydroxybenzoate monooxygenase (GraB)”，EC null；gold首步为gamma-resorcylate decarboxylase EC 4.1.1.103，并另有resorcinol 4-hydroxylase EC 1.14.14.27。答案漏掉后者。S2的hydroxyquinol 1,2-dioxygenase EC 1.13.11.37与gold一致，S3 maleylacetate reductase EC 1.3.1.32为合理下游候选，但首步核心酶-反应对应错误使主要推荐失效，cap≤4档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_122：支持S01答案S2的酶/EC匹配；同时显示S02/S03目标酶未被答案交付，不支持答案S1作为S03替代。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：支持目标反应方向与底物/产物；不证明答案S1直接单加氧为本题目标反应。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案统一使用Rhizobium sp. strain MTP-10005，与gold organism_gold中S01/S02/S03的菌株及PATHWAY_COMPLETE=TRUE一致；身份定位与整路径能力声称有适用gold支持，且同一菌去重。扣分点是答案把该菌用于S1直接GraB反应，该具体替代步的菌株级单步能力未在冻结材料中单独核验；但未推翻主要微生物推荐。按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

8分：答案的Rhizobium sp. strain MTP-10005与gold organism_gold中多个步骤的EXACT匹配记录一致，gold并有267998的PATHWAY_COMPLETE=TRUE，支持其整条路径能力；TaxID填null属于诚实未知，不据此判错。未见菌株级反应层额外证据或身份错配，取8分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_122：支持Rhizobium sp. MTP-10005参与gold三步且pathway_complete=TRUE；不单独验证答案S1的GraB替代反应。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案按要求返回15项性状，7项填写、8项明确null/unknown，未编造数值。Rhizobium MTP-10005的trait_gold除TaxID外基本为UNKNOWN，因此F1/F6/F7/F8/F9/F12/F15的定性值不能在冻结材料中确认或否证；答案多数标low/medium并写明推断，但部分性状仅给EVID_001而raw_text缺失，关键定量性状仍为null。按5–6档“部分性状可适用但关键项证据不足/条件解释需修订”取6。

<details><summary>V0.4理由与本行变化背景</summary>

5分：15项字段齐全，但仅7项有值、8项明确未知；有值项中F1、F6、F12明确标为推断且无菌株级直接来源，F7/F8/F9/F15依赖同一未核文献，F9还重复了D3a的首步错误酶功能。官方trait快照对Rhizobium MTP-10005几乎全为UNKNOWN，关键性状证据不足；按D4条款，缺失本身主要归D1，不重复重扣，故在5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_122：显示Rhizobium MTP-10005的trait记录基本为UNKNOWN/无观测值；不能确认答案填写值，也不能据此判其错误。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_122：支持多数性状为completeness_only或无观测值，不能把未核验值当已观测事实。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分4 → V0.5新分6，变化+2。

新裁判理由：

> 答案交付了可定位的文献引文EVID_001（作者/刊/卷期页）以及BRENDA EC条目EVID_002/EVID_003和MetaCyc路线名EVID_004，主要路线/酶/菌声称有来源ID映射，不是完全无来源。但EVID_001为自由文本引文且未在冻结E0解析核验，EVID_004缺record_id且仅路线名，部分性状仅笼统挂EVID_001或无raw_text；无已核实错引，不能判CRITICAL/SYSTEMIC。按“部分关键结论可定位并核对，其他模块仍缺映射或必要生成记录”的5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

4分：答案给出了具体文献与EC数据库指针，但E0无对应记录可核对：EC 1.13.11.37与1.3.1.32均为EVIDENCE_GAP，Yoshida等2007与MetaCyc项均未解析/未核；E0仅有的两条记录属于Pseudomonas putida，不能支持Rhizobium或本题EC。故关键来源只能登记UNRESOLVED_SOURCE，保留低分与待核标记；无已核实错引，不触发D5 cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案较清楚地区分未知与推断：15项中性状大量null，F1/F6/F12等明示推断，uncertainties列出EC缺失、TaxID/保藏/基因组未知、氧条件未指定及maleylacetate表述差异。扣分点是S2/S3酶与菌株confidence标high、route_summary对gra基因簇表述较强，且未披露其S1直接单加氧与gold两步主链的路线差异；属局部过度确信，不是系统性误导。按7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

7分：答案较清楚地标出多处unknown/null，F1/F6/F12明确写“推断”，uncertainties列出EC缺失、TaxID/保藏号/基因组缺失、氧条件null及maleylacetate互变异构问题；主要限制有披露。不足是EVID_001整体标high、F8/F9等文献性主张未进一步核验，且首步科学冲突未被披露为限制；属局部过度确信而非系统性误导，取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：展示答案实际披露的未知/推断与置信标签；不验证其科学真值。

</details>

## Qwen

答案SHA256：`61feb7898c28c3dff599cddb238c1918134de2a723a0356ce36916b1ca99af4e`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 必要主链步骤和酶/微生物字段基本给出，但15项性状全部为null/unknown，且多个EC/SMILES缺失，属于主要模块涉及但存在实质占位与遗漏，落5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6偏下取5：路线模块完整（4步、每步底物-产物-酶-菌绑定、order与前驱清楚），route_scope.chosen_route_name原样回显题面指定路线&#x27;γ-resorcylate degradation I&#x27;、氧条件按题面null填写，无任务参数偏离。但必要内容多处遗漏：15项性状全部未给出数值（仅显式unknown）、S1/S2未给EC、maleylacetate与3-oxoadipate的SMILES缺失、全部菌株与TaxID为null、来源仅有内部自述。属&#x27;主要模块均有涉及但若干必要内容遗漏&#x27;，按完成度不足取5，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：answer shows four steps, enzyme fields, one organism profile, and all 15 traits null/unknown
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_122：gold main chain is linear unique with three required steps; not a basis for requiring every DAG branch

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> S1-S3 core chemistry follows the gold direction: decarboxylation, hydroxylation, and ring cleavage to maleylacetate. FADH2/O2 cofactor omissions are local stoichiometric gaps under P103; S4 is downstream beyond the specified terminal and is not required. 7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

7–8档取7：S1脱羧（2,6-Dihydroxybenzoate→resorcinol+CO2）、S2羟化（resorcinol→1,2,4-三羟基苯）、S3 1,2-双加氧开环（→maleylacetate）与gold BSY-r02866→BSY-r00202→BSY-r00201的转化节点、方向（SUBSTRATE_TO_PRODUCT forward）与顺序（linear order 1→2→3）一致，无起始步错误、无方向反转、无无依据跳步；S4（maleylacetate→3-oxoadipate）位于gold终点Maleylacetate下游，按P29不进入评分范围，额外延续不加分、未延续不扣分。扣分点为局部计量/结构缺陷：S2缺O2与FADH2、S3缺O2、S4缺还原当量且辅因子未列，maleylacetate与3-oxoadipate的SMILES为null。按P103辅因子遗漏属7–8档局部缺陷，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：gold shows the directed three-step main chain ending at Maleylacetate; cofactor participants are listed but not the only acceptable simplified expression
- ANSWER_TEXT / ANSWER：answer gives the three core conversions plus one extra downstream reduction

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> D3a按C03-C05评三个必答目标反应。S1（对应gold S03）2,6-二羟基苯甲酸脱羧→间苯二酚/CO2，酶名2,6-dihydroxybenzoate decarboxylase可视为gamma-resorcylate decarboxylase的功能同义，缺EC但功能可判，记S。S2（gold S02）反应结构匹配，但resorcinol hydroxylase未达到accepted resorcinol 4-hydroxylase (FADH2)/EC 1.14.14.27，记U。S3（gold S01，KEY_TERMINAL）名称hydroxyquinol 1,2-dioxygenase在accepted集，但显式EC 1.13.11.22与accepted 1.13.11.37不一致，E0无1.13.11.22记录，不能判F，记U。S4为终端下游，不计目标信用。S=1,N=3，仅少数目标已核可用；无已证关键失败，按受限档给4。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档取6：各步酶的功能类别与反应类型相符——S1脱羧酶（对应gold gamma-resorcylate decarboxylase EC 4.1.1.103）、S2羟化酶（对应gold resorcinol 4-hydroxylase (FADH2) EC 1.14.14.27）、S3羟喹醇1,2-双加氧酶（gold同名酶记录对应EC 1.13.11.37）、S4 maleylacetate reductase（下游步，功能为还原）。但S1/S2的EC为null，S3所给EC 1.13.11.22与S4所给EC 1.3.1.32在冻结证据中无记录（EVIDENCE_GAP_NO_RECORD），按四.6/P66保持UNRESOLVED，不得据数据库记忆判为错或对；&#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;取6，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：答案S1-S4酶名/EC及底物产物；S3 EC=1.13.11.22，S1/S2 EC=null
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_122：gold accepted enzyme/EC for required steps: S03 4.1.1.103; S02 1.14.14.27; S01 1.13.11.37 (hydroxyquinol 1,2-dioxygenase)
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：target reaction substrate/product/direction；S03 entry decarboxylation, S02 hydroxylation, S01 ring cleavage to Maleylacetate terminal

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案对全部步骤使用同一Cupriavidus metallivorans profile，无strain/TaxID，也无步骤级反应能力或全路径能力证据；该菌未见于gold organism行，但gold非穷尽，不能据此证明其错误。身份与能力均未核验，落3–4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档取5：四步均归属同一物种 Cupriavidus metallivorans（strain=null、ncbi_taxid=null、confidence=low），未提供任何支持该菌具备脱羧/羟化/开环/还原反应级能力或整链能力的实验或条目证据，等同于以单一步级归属叠加出整链能力声称而无证据；身份粒度仅为物种、无株与TaxID。另一方面，该菌名与能力在冻结证据中无记录（E0两条记录均属Pseudomonas putida；verified_species_name_crosswalk仅含Cupriavidus necator=106590），无法核实其为错，按未证实处理，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_122：gold lists organisms for the required steps; it is non-exhaustive and does not prove Cupriavidus metallivorans incapable
- ANSWER_TEXT / ANSWER：answer uses one Cupriavidus metallivorans profile for all steps with no strain or TaxID

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 所有15项性状均为null/unknown，没有交付任何性状值；按P44/P45记MISSING=1，不宣称检测到科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

按四.4/P44记MISSING=1：任务要求&#x27;填写15项性状及各项最强来源&#x27;，答案唯一profile ORG_001的F1–F15全部为 value=null、evidence_id=null、confidence=unknown，未交付任何性状数值/单位/条件，故无可评性状内容；此状态表示&#x27;未提供可评价结果&#x27;，不宣称检测到科学错误，完成度扣分已在D1计入，不在此重复重扣（P112）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：all required trait fields are present but every value is null/unknown

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 决策相关claim groups均仅见INTERNAL_KNOWLEDGE_ONLY的EVID_001/EVID_002，database/record_id/locator均为null，无法定位到外部条目；属MISSING_SOURCE，不是已核实错引。D5落1–2档取2。

<details><summary>V0.4理由与本行变化背景</summary>

1–2档取2：evidence_registry仅两条，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null，claim_scope只覆盖S1–S4与ORG_001，无法定位任何条目、文献或计算记录；决策相关组CG01/CG02/CG03/CG05/CG07/CG08与支持组CG04/CG10–CG14/CG20全部为MISSING_SOURCE。按P34/P41&#x27;全部缺失→低分档&#x27;，MISSING_SOURCE默认不cap；EC缺口属UNRESOLVED而非已核实错引，故无CRITICAL/SYSTEMIC。取2而非1：答案以结构化registry明确把证据标为内部知识并给low，未伪造不存在的条目或编号。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：evidence_registry entries are internal-knowledge-only and contain no database record or locator

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确将confidence标为low/unknown，列出氧条件未指定、EC/SMILES/性状/辅因子缺失等限制，未把预测包装成实验观测；披露具体且与证据强度相称，落7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

7–8档取7：答案系统性标注证据性质与置信——所有酶/菌字段confidence=low，两条证据均标INTERNAL_KNOWLEDGE_ONLY，uncertainties明确列出氧条件未指定、EC/SMILES/性状缺乏可靠来源按null处理、辅因子与化学计量未展开；未把预测/推断写成实验观测，未知以null显式登记。扣分点为单点过度确信与说明不足：route_summary与central_metabolism_entry以陈述句给出通路及中心代谢解释而就地未标注证据性质；菌名具体到种（Cupriavidus metallivorans）却未说明身份粒度与来源缺失（零披露）。按P119属单点过度确信、非系统性误导，档内扣分、不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：answer explicitly lists uncertainties and marks missing fields as null/unknown

</details>

## Grok

答案SHA256：`fbd380d896436babf07d91df1928da01cdce8b7ef3523176ebfb284df63886c2`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 覆盖全部3个必答主链步（对应gold S03/S02/S01），每步给出主底物/主产物名称与SMILES、一个首选酶、一个微生物；route_scope.chosen_route_name逐字为γ-resorcylate degradation I；organism_profiles按物种+菌株单条去重且被各步引用；15项性状按模板全列（6填9个诚实null）；evidence_registry与uncertainties齐备。轻微问题：S2未给EC（题面允许未知填null但属要求项未满）、S4（maleylacetate→3-oxoadipate）一步超出gold终点Maleylacetate且被同时标注为main与downstream、氧条件题面null而答案填aerobic（已在notes披露为推断）。落7–8档，因仅少量遗漏/边界问题取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION#BIOPATH150_122：题面要求逐步给主底物/主产物英文名与SMILES、一个首选酶及EC、一个对应微生物、15项性状及最强来源；未指定氧条件与终点token；未知项填null。
- ANSWER_TEXT / ANSWER#BIOPATH150_122：仅证明上述内容已交付及字段完整性，不证明其科学正确性。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步必答化学与gold一致且顺序/方向正确：脱羧（2,6-dihydroxybenzoate→resorcinol+CO2，原子与电荷配平）、单加氧羟化（resorcinol→hydroxyquinol=1,2,4-benzenetriol）、1,2-双加氧开环（hydroxyquinol→maleylacetate），主链SMILES与gold在电荷记法差异内同一结构，无反向、无无依据跳步、无一步跳到中心代谢物。局部问题：S2以NADH/NAD+替代gold的FADH2/FAD（辅因子-计量局部缺陷，按P103在7–8档内处理，不cap）；S3产物未列H+（次要）。S4 3-oxoadipate为真实下游反应且已单列downstream，不计入必答终点亦不扣分。取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：支持三步主链的底物/产物结构与方向、终点Maleylacetate；并显示S02以FADH2为辅底物、FAD为副产物，不支持NADH为该步辅因子。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_122：支持入口化合物2,6-Dihydroxybenzoate与终点Maleylacetate的身份；不涉及下游3-oxoadipate化学。

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> N=3逐目标判：①gold S01（KEY_TERMINAL，1,2,4-benzenetriol+O2→maleylacetate）由答案S3命中，hydroxyquinol 1,2-dioxygenase EC 1.13.11.37与accepted set精确同名同EC→S；②gold S02（resorcinol 4-hydroxylase (FADH2) EC 1.14.14.27）由答案S2以名称为&#x27;resorcinol hydroxylase&#x27;、EC=null给出，反应resorcinol→hydroxyquinol与gold主产物同结构，属名称/功能层可支持但未完成显式名号配对→按S计并保留局部待核；③gold S03（KEY_ENTRY，gamma-resorcylate decarboxylase EC 4.1.1.103）由答案S1以&#x27;2,6-dihydroxybenzoate decarboxylase&#x27;EC 4.1.1.103给出，EC精确一致、名称属同一活性同义名，入口底物差异仅为电荷记法（REPRESENTATION_EQ_CHARGE_BLIND）→判S。故S=3、U=0、F=M=H=0，C=1.0；但d3a 9–10不可用（policyA NOT_ELIGIBLE；KEY入口步仍在表示复核、S02缺显式EC、S02辅因子另有局部缺陷），落&#91;7,8&#93;；因局部对应与支持边界尚需少量修订取7，不取8。未命中accepted本身未作为证伪依据。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_122：支持三个必答步的accepted酶名/EC（G4参考策展粒度）；不证明任意具体蛋白底物谱、实验活性或菌株能力。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：支持三步主底物/主产物身份与方向（含S02的FADH2辅底物），说明答案S2的NADH为局部辅因子偏差而非酶-反应错配。
- ANSWER_TEXT / ANSWER#BIOPATH150_122：仅定位答案实际给出的酶名/EC与反应式，不证明其正确。

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步一致归属Rhizobium sp. MTP-10005；organism_gold对该菌株在S01（BSY-e00137）、S02（BSY-e00142）、S03（BSY-e02507）三步均有EXACT记录（gold TaxID 267998），身份（名称+菌株）与步级归属均与冻结记录一致；complete_pathway_organism_profile_id=ORG_001与PATHWAY_COMPLETE=TRUE行相符，未把单步支持冒充全路径能力。不足：TaxID/基因组留null（诚实缺省但少一项身份要素）、未交付菌株级能力证据（来源问题归D5）、菌株级性状值未核（归D4）。落7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_122：支持Rhizobium sp. MTP-10005的三步步级归属及pathway_complete=TRUE；不支持菌株级性状值、具体蛋白活性或TaxID在答案中的交付。

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状全部出现，9项以value=null、confidence=unknown诚实留空（与gold对该菌株除TaxID外全UNKNOWN的状态相容，未编造数值/单位/保藏号/基因组号）。填入的6项（F1好氧、F6好氧呼吸/分子氧、F7利用2,6-二羟基苯甲酸、F8降解能力、F9脱羧酶活性、F12革兰氏阴性）均为属级/通路级推断，自述来源EVID_003为INTERNAL_KNOWLEDGE_ONLY、confidence=medium/low、raw_text=null，未见与任何冻结记录冲突的数值或跨株外推（无温度/pH/盐度被写成菌株实测）；但均缺MTP-10005菌株级证据，故不能给8以上。落5–6与7–8之间取7（诚实null与合理标注占优，关键项证据不足为主要失分点）。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_122：显示该菌株仅F14的TaxID为OBSERVED，其余性状均UNKNOWN；不提供任何可判答案对错的菌株级性状观测，故填入项只能UNRESOLVED。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_122：确认该菌株除F14外无observed_accuracy分母，性状只能按完整性与诚实性评价，不能据无记录判答案错误。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部决策相关组（路线/步骤、酶-EC、核心菌株身份、性状）仅以INTERNAL_KNOWLEDGE_ONLY自述交付：evidence_registry两条的database/record_id=null、locator为&#x27;文献记忆、本次未实时检索、无原文摘录&#x27;，无DOI/条目号/反应ID/基因组号等可定位锚点，属MISSING_SOURCE而非GENERIC可定位；按P34低分档。无任何已核实错引（没有可核引用对象），故不cap、severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION；SUPPORTING组也无条目级证据可上调。落1–2档，因确实点名了MetaCyc途径名与菌株名（极弱可指向性）取2而非1。

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / P34：MISSING_SOURCE（完全无引用或仅INTERNAL_KNOWLEDGE_ONLY自我声明）按低分档评定，默认不触发关键错误cap。
- RUBRIC_CLAUSE / P41：按claim group合成：决策相关组全部缺失→低分档；未核来源单独登记，不与错引严重度混算。
- ANSWER_TEXT / ANSWER#BIOPATH150_122：证明交付来源形态为内部记忆自述，非可定位条目。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 证据性质与边界披露质量高：evidence_registry明确标注source_type=INTERNAL_KNOWLEDGE_ONLY并声明&#x27;本次未实时检索数据库、无原文摘录&#x27;；uncertainties逐条列出S2缺EC、S4辅因子偏好未核、TaxID/保藏号/基因组号/温度pH盐度等无数值来源、主链止于3-oxoadipate且β-酮己二酸途径不计入、基因符号未确认；9项性状value=null且confidence=unknown，未见把预测写成实测观测。扣分点：两个记忆来源的酶EC仍标confidence=high（与证据类型轻度不相称），F8把至3-oxoadipate的通路能力以medium直述、未标注为推断；属单点/局部过度确信，非系统性误导，故在7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_122：支持&#x27;已披露未知与限制&#x27;的判定；不证明所披露内容科学正确。
- RUBRIC_CLAUSE / P119：单点过度确信（强标签包装未核内容）与系统性误导分开：前者档内扣分，后者才是cap候选。

</details>

## GPT5.6

答案SHA256：`93458880da3393a8f9a9aa144e01ee0cedb6aec63ad9f754673265209eef36c3`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 任务结构表面完整，但路线在首步脱羧后偏离题面指定的γ-resorcylate degradation I：后续为resorcinol还原/水解开环至3-oxopimelate，未交付gold的1,2,4-benzenetriol与终点maleylacetate；15项性状全为null。按D1任务偏离关键错误落在3档：有可辨认步骤和字段，但主要路线不符合题面，必要终点缺失。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：gold主链为S03 2,6-Dihydroxybenzoate→Resorcinol+CO2，S02 Resorcinol→1,2,4-Benzenetriol，S01 1,2,4-Benzenetriol→Maleylacetate；支持指定路线与终点，不支持答案的还原/水解开环替代路线。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_122：题面指定route_name与terminal main product为γ-resorcylate degradation I、Maleylacetate；用于D1任务符合度，不外推到其他路线。
- ANSWER_TEXT / ANSWER.route_scope;ANSWER.steps;ANSWER.organism_profiles：被测答案自报路线、三步反应、酶/菌与15项null性状；用于完整性和任务偏离定位。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1脱羧生成resorcinol+CO2化学上可成立且与gold入口步对应；但S2将resorcinol还原为dihydroresorcinol，S3给dihydroresorcinol水解开环至3-oxopimelate，名称与SMILES存在不一致（dihydroresorcinol/3-oxopimelate结构表述与碳数/氧化还原计量不清），且未连接至gold的1,2,4-benzenetriol→maleylacetate主链。仅首步可靠，后续关键转化需实质修订，落3–4档，取4因首步和步骤顺序表达仍可辨。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：gold S03/S02/S01反应、辅因子与方向用于比较答案化学连续性；D2仍按答案自身化学独立评价，不将“与gold不同”本身自动判错。
- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;.substrates/products/smiles：答案给出的三步底物/产物和SMILES；支持结构/名称/计量问题定位，不证明替代路线在外部实验中成立。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按目标反应核：entry target S03（2,6-Dihydroxybenzoate→Resorcinol+CO2）由答案S1给出且与accepted gamma-resorcylate decarboxylase功能相符，可作S；S02目标（Resorcinol→1,2,4-Benzenetriol）答案改为resorcinol还原为dihydroresorcinol，未交付目标产物，按目标失败F；S01目标（1,2,4-Benzenetriol→Maleylacetate）完全缺失，按M。N=3，S=1，C=0.333，落&#91;3,4&#93;；仅一个目标可用且关键terminal缺失、midroute被替换，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_122：gold三步目标反应与产物；用于逐目标判断答案是否交付S03/S02/S01。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_122：accepted酶名/EC：S01 1.13.11.37，S02 1.14.14.27，S03 4.1.1.103；支持S1脱羧功能对应，不证明答案S2/S3替代酶功能。
- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;.enzyme/substrates/products：答案实际交付的酶名、底物和产物；用于逐目标mapping。

</details>

### D3b 微生物身份与能力：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案三步均归Thauera aromatica K172，未给TaxID、保藏号或菌株级实验记录，唯一证据为INTERNAL_KNOWLEDGE_ONLY；gold organism行对应的是其他菌株（如Rhizobium sp. MTP-10005等）。该菌名可作为候选，但多步反应级能力与整路径能力均无适用支持，且把同一菌用于全部替代步骤，落3–4档，取4因身份名称本身未被证明为伪。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_122：gold给出各步匹配菌株及TaxID/基因组；用于说明答案Thauera K172缺少对应gold记录，不将“不在gold”自动判为错误。
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism;ANSWER.organism_profiles&#91;0&#93;：答案自报Thauera aromatica K172与同一profile；支持“多步归属同一菌且无来源”的定位。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段均存在但全部value为null、confidence=unknown，未交付任何可评价的性状观测/预测值或适用来源。按P44，全部必需性状为null/空值时D4记MISSING=1，不宣称检测到具体科学错误；诚实unknown的披露另在D6体现。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：答案15项性状均为null/unknown；支持D4 MISSING定位，不支持任何性状正确性判断。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案仅登记EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；路线、酶、菌和性状无任何可定位数据库条目、文献或计算记录可核对。按D5六状态为MISSING_SOURCE，决策相关组全部缺失，落1–2档取1；无已核实错引，不触发cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：唯一证据条目为INTERNAL_KNOWLEDGE_ONLY，且无database/record/locator；支持MISSING_SOURCE，不支持任何具体结论的可追溯性。
- RUBRIC_CLAUSE / P34_MISSING_SOURCE：MISSING_SOURCE包括完全无引用或仅INTERNAL_KNOWLEDGE_ONLY；默认低分且不自动cap。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案总体明确区分未知与低置信：所有酶/菌步骤标low，trait全unknown，uncertainties列出氧条件未指定、EC/基因/菌株证据不足、dihydroresorcinol与3-oxopimelate结构异构体不确定；evidence_registry自标INTERNAL_KNOWLEDGE_ONLY。主要限制披露较充分，仅complete_pathway_organism_profile_id仍显过度但非系统性误导，落7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties;ANSWER.evidence_registry&#91;0&#93;：答案自述不确定性、低置信和INTERNAL_KNOWLEDGE_ONLY；支持D6披露质量评价。
- RUBRIC_CLAUSE / P119_P121：单点过度确信与系统性误导分开；D5来源缺失不自动使D6 cap。

</details>
