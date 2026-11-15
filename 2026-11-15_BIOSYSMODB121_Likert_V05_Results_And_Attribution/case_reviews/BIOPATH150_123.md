# BIOPATH150_123：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：propane degradation I

污染物：Propane；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 48.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 42 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 48.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 36.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 45.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 33.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`ea78525c943cad13bed3b1479efdfabb1ea399126af4a8f6c136b7cddeb37e8c`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案输出了完整JSON、7步主链、3个菌株profile及15项性状，工程完整性较好；但主链内容把题面指定的 propane degradation I 替换为丙烷末端氧化至琥珀酰-CoA，而gold/route diagnosis显示本题主链为丙烷→丙-2-醇→丙酮→乙酸甲酯→乙酸/甲醇。按D1任务路线偏离关键错误cap≤4，因交付结构完整取4。

<details><summary>V0.4理由与本行变化背景</summary>

输出结构完整，路径、酶、微生物、15项性状与证据登记均交付；但题面明确限定route_scope为propane degradation I并要求原样不改选，答案虽填写该名称，却交付丙烷末端氧化经丙-1-醇/丙酸/甲基丙二酰-CoA至琥珀酰-CoA的主链，与冻结gold中该路线（丙烷→丙-2-醇→丙酮→乙酸甲酯→乙酸/甲醇，4步）不同，属自称合规却交付不同化学路线的任务参数偏离，D1主要结论失效，cap≤4；因各模块均已实质填写，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_123_question：题面将路线范围限定为 propane degradation I，并要求不得改选其他路线；不提供具体化学事实。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_123：显示本题gold为4步、LINEAR_UNIQUE的propane degradation I；不表示其他丙烷路线在自然界不存在。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：显示gold主链S03/S02/S04/S01的有向反应与底物/产物；只支持本题目标主链，不扩展到答案的末端氧化路线。
- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_123：显示答案实际交付的是丙烷→丙-1-醇→丙醛→丙酸→丙酰-CoA→甲基丙二酰-CoA→琥珀酰-CoA的替代路线。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> D2按答案所答路线的化学质量独立评价：S1–S7主有机物转化连续，醇/醛氧化、CoA活化、羧化、差向异构与变位重排均基本合理，辅因子多数列出；存在H+或B12等局部计量/表达简写。由于这是与题面指定路线不同的替代路线，按C06化学可成立替代路线最高&#91;1,6&#93;取6，不将替代路线回填目标完成。

<details><summary>V0.4理由与本行变化背景</summary>

按D1/D2边界，路线名称/任务参数偏离归D1；D2只看交付反应化学。S1–S7碳骨架连续、方向正确，主产物与底物连接合理，主要辅因子（O2、NADH/NAD+、ATP/CoA、HCO3-）在位，无起始步错误、无依据跳步或明显原子不守恒。S1末端羟化与gold亚末端路线不同，但作为独立化学路线可成立；因部分酶机制/辅因子细节未经E0核验，取8而非更高。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_123：显示答案自身S1–S7的底物、产物、方向与辅因子；支持评价其内部连续性，不支持其等同gold主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：用于确认题面指定路线与答案路线不同；不作为D2替代路线化学合理性的唯一判据。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分8 → V0.5新分2，变化-6。

新裁判理由：

> 逐目标映射为S=0、F=2、U=2。已绑定KEY步S03和S02为确认目标失败：答案S1为propane→propan-1-ol而gold S03为propane→propan-2-ol；答案S2为propan-1-ol→propanal而gold S02为propan-2-ol→acetone。S01/S04仍为alignment未确认，不给予支持信用。已确认KEY失败触发D-KEY4上界&#91;1,4&#93;；本题无任何目标S支持，核心目标反应对应失效，按C05取2。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶名与反应类型大体匹配：S1丙烷单加氧酶（无正式EC，已如实null）；S2醇脱氢酶EC 1.1.1.1、S3醛脱氢酶EC 1.2.1.3为通用NAD+依赖酶；S4丙酰-CoA合成酶EC 6.2.1.17、S5丙酰-CoA羧化酶EC 6.4.1.3、S6甲基丙二酰-CoA差向异构酶EC 5.1.99.1、S7甲基丙二酰-CoA变位酶EC 5.4.99.2与相应反应类型一致。E0无法核验EC accepted name/reaction，故局部待核，但未见酶名与EC类别互相矛盾。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：显示gold S03为propane→propan-2-ol、S02为propan-2-ol→acetone、S04为acetone→methyl acetate、S01为methyl acetate→acetate+methanol；只支持这些目标反应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_123：显示gold各目标步的首选酶/EC；不支持把答案的末端氧化酶直接当作目标酶。
- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_123：显示答案S1/S2选择的是丙烷末端氧化及通用醇脱氢酶，不是gold S03/S02的目标反应。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案给出的菌名/菌株多为真实候选，但多处与本题目标路线步骤不对应：S1–S3使用Rhodococcus sp. BCP1的末端氧化设定，S4以Salmonella LT2的PrpE作模型，S5–S7以Propionibacterium freudenreichii的Wood-Werkman酶系作模型；答案自述S5–S7并非丙烷降解菌，且complete_pathway_organism_profile_id仍指向ORG_001，形成步级归属与整路能力的不一致。多项菌-步能力与TaxID/保藏/基因组无E0核验，按D3b 3–4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3用Rhodococcus sp. BCP1，作为已知丙烷/丁烷降解菌，步级身份合理；但S4用Salmonella enterica Typhimurium LT2、S5–S7用Propionibacterium freudenreichii，答案自述二者无烷烃降解能力，却将其作为丙烷主链对应微生物，步级归属与“丙烷降解主链微生物”匹配较弱；complete_pathway_organism_profile_id=ORG_001也缺少S4–S7在红球菌中的全路径证据。未达到编造身份或跨类群cap程度，按5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_123：显示各步菌名、菌株、ORC profile及作者自述的模型菌局限；支持评价步级归属，不支持证明其目标路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_123：显示gold目标步对应的Gordonia sp. TY-5、Mycolicibacterium smegmatis、Mycobacterium goodii等；不证明其他菌绝对不能催化单步反应。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 三个profile均一次返回15项性状，未知项多用null/unknown，符合诚实空值方向；但关键数值与一般性状大量依赖INTERNAL_KNOWLEDGE_ONLY、无raw_text，Salmonella/Propionibacterium的37°C、pH、ATCC、GC等无法在E0核验，Rhodococcus BCP1多数关键性状为空。按D4 5–6档“部分性状可解释、关键证据不足”取5。

<details><summary>V0.4理由与本行变化背景</summary>

三个profile均返回15项性状，未填项多以null+unknown诚实披露；已填性状多为一般微生物学常识且与身份大体相符，如Salmonella LT2的Gram阴性、兼性厌氧、运动性、NC_003197与GC 52.2%等。但关键数值/条件缺可定位来源，P. freudenreichii的盐度、末端电子受体等证据弱，且所用菌并非gold路线菌；按5–6档“部分性状准确且适用，但关键项证据不足”取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_123：只含gold菌株的冻结性状记录；不直接核验答案所用Rhodococcus BCP1、Salmonella LT2、Propionibacterium的性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_123：显示gold菌株哪些性状可计分；不支持把gold菌株值回填给答案菌株。
- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_123：显示答案实际填写的15项性状、null与confidence；支持评价完整性和证据外显程度。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> D5按实际交付来源登记。决策相关组中，路线/酶主要依赖EVID_001的MetaCyc页面名与EVID_002–EVID_004的文献系列概述，缺record_id/DOI；EVID_005–EVID_007为INTERNAL_KNOWLEDGE_ONLY；仅EVID_008有NC_003197具体登录号但仍无法在E0核对。整体达到“笼统来源/缺映射”的3–4档，未达到可核对关键结论的5–6档；因E0为EVIDENCE_GAP，不判已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry逐step有EVID映射，但核心路线、酶-EC与核心菌身份主要依赖无DOI/record_id的文献系列、MetaCyc页面名或INTERNAL_KNOWLEDGE_ONLY；仅EVID_008给出NC_003197具体accession，且E0为EVIDENCE_GAP无法核验。决策相关组整体未达到“条目级可定位可核对”，落入3–4档；无已核实错引，不触发cap，因证据登记结构尚完整取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_123：显示答案实际交付的8条来源、其source_type、locator、record_id及claim_scope；支持按交付粒度评D5，不回填评价者新增证据。
- RUBRIC_CLAUSE / C08：支持D5来源状态与总分/NE处理规则；不替代具体来源核验。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确给出uncertainties，区分null/未知/中等confidence，披露数据库路线未逐条核验、丙烷单加氧酶无正式EC、BCP1身份信息为null、S4/S5–S7使用模型菌且非丙烷降解菌等主要限制；替代分支也标注不属评分主链。局部存在把INTERNAL_KNOWLEDGE_ONLY性状标为high confidence的单点过度确信，但整体披露具体且非系统性误导，按D6 7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案有具体不确定性披露：路线数据库定义未逐条核验、S1无正式EC、S4与S5–S7使用非丙烷降解模式菌、多项性状null及近似记忆未填。整体未把预测系统性写成实证，主要限制有说明；但部分步级菌/酶标high confidence，与笼统来源不完全相称，属单点过度确信，档内扣至7而非更高。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_123：显示答案对未知、预测、模型菌局限和路线未核验的披露；支持D6证据性质判断，不证明科学内容本身正确。
- RUBRIC_CLAUSE / C06：支持D6区分单点过度确信与系统性误导的锚点；不新增证据。

</details>

## DeepSeek

答案SHA256：`1b9e86df5ec47552dcf50349cd7131b18dc110c14a1eff91d539a32db3f8608e`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> The task requires the frozen propane degradation I main chain. The answer copies the route name but delivers a different 7-step propane-&gt;1-propanol-&gt;...-&gt;succinyl-CoA route, omitting the gold S01-S04 main-chain steps and terminal acetate/methanol. This is a D1 task-compliance key error; range &#91;1,4&#93;, score 3 because all output modules are present and readable but the required route is not delivered.

<details><summary>V0.4理由与本行变化背景</summary>

题面明确要求chosen_route_name=&#x27;propane degradation I&#x27;且不得改选其他路线。答案route_scope虽填该名，但交付的S1–S7是经1-丙醇→丙醛→丙酸→丙酰-CoA→(S/R)-甲基丙二酰-CoA→琥珀酰-CoA的末端氧化/甲基丙二酰-CoA路线，与gold的propane degradation I（经2-丙醇→丙酮→乙酸甲酯→乙酸+甲醇）为不同路线，属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离（P100），D1关键错误成立，cap≤4。输出结构完整（7步、15项性状字段齐全、evidence_registry齐全），档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv：Gold pathway is propane degradation I with four ordered required steps; this does not authorize a different main chain.
- GOLD_SLICE / reaction_gold.tsv：Gold main chain is propane -&gt; propan-2-ol -&gt; acetone -&gt; methyl acetate -&gt; acetate + methanol; it does not support the answer&#x27;s 1-propanol/succinyl-CoA route.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> Alternative route chemistry is largely coherent: terminal hydroxylation, alcohol/aldehyde oxidation, CoA activation, and methylmalonyl-CoA pathway to succinyl-CoA have connected steps and no obvious reversed direction or atom break. Cofactors are mostly omitted and the endpoint differs from gold acetate/methanol; under the D2 allowed range &#91;1,6&#93;, 6 reflects a chemically plausible alternative with local omissions, not target credit.

<details><summary>V0.4理由与本行变化背景</summary>

交付主链每一步化学转化（单加氧→醇脱氢→醛脱氢→CoA连接→羧化→差向异构→变位酶）化学上成立、方向正确、计量基本守恒、步骤连续，属已知丙烷末端氧化/甲基丙二酰-CoA途径。但该路线并非题面指定的propane degradation I，且为未声明的替代路线、无外部证据。按合理替代路线四步判断：未声明+无证据→不自动判错也不给高分；交付路线无&#x27;起始步错误/无依据跳步/原子不守恒&#x27;，路线替换属D1范畴（P100），故不构成D2关键错误。综合&#x27;主干化学成立但合理性证据有限且不挑战任务条件符合性&#x27;，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Provides the gold reaction chemistry and terminal products for comparison; does not itself prove the answer&#x27;s alternative route wrong.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> No accepted gold target step is completed. S02 and S03 are confirmed KEY target failures; S01 and S04 have no bound relation/alignment not confirmed. Counts S=0, F=2, U=2; D-KEY4 keeps the score within &#91;1,4&#93;. Score 2 reflects no supported target credit, with only local alternative-enzyme information; not 1 because a complete enzyme module is present.

<details><summary>V0.4理由与本行变化背景</summary>

七步酶-反应对应总体合理：alcohol dehydrogenase(1.1.1.1)、aldehyde dehydrogenase(1.2.1.3)、propionate--CoA ligase(6.2.1.17)、propionyl-CoA carboxylase(6.4.1.3)、methylmalonyl-CoA epimerase(5.1.99.1)、methylmalonyl-CoA mutase(5.4.99.2)与各步反应类型匹配；首步propane 1-monooxygenase(1.14.13.229)区域选择性/归属有不确定。全部EC为编号类声称，E0为EVIDENCE_GAP无法核实→UNRESOLVED待核，不判错；无酶名与EC明显矛盾；gene/protein均为null。取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：Gold accepted enzymes are methyl acetate hydrolase, secondary alcohol dehydrogenase, propane 2-monooxygenase, and acetone monooxygenase; does not support the answer&#x27;s target-step enzymes.
- GOLD_SLICE / reaction_gold.tsv：Gold target reactions are propan-2-ol/acetone/methyl acetate route; answer steps are different reactions.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> All steps are assigned to Rhodococcus sp. BCP1, and complete_pathway_organism_profile_id=ORG_001 claims that strain completes the route. Gold lists Gordonia/Mycolicibacterium/Mycobacterium organisms; BCP1 identity and full-pathway capability are not verified in E0 and no TaxID is supplied. Plausible candidate but capability overreach; 5-6 band, score 5. No verified contradiction, so no cap.

<details><summary>V0.4理由与本行变化背景</summary>

全部7步归属同一Rhodococcus sp. BCP1(ORG_001)，并以complete_pathway_organism_profile_id声明其完成整条路径。该身份/能力声称仅EVID_009/EVID_008=INTERNAL_KNOWLEDGE_ONLY，无TaxID、无反应级/全路径能力证据；gold的propane degradation I对应Gordonia sp. TY-5、Mycolicibacterium smegmatis、Mycobacterium goodii等多菌。将单菌写成整条路径菌、且无证据支持，属作用范围过度外推与支持不足；但EVIDENCE_GAP下无法核实BCP1是否确实不能，不判虚构/不cap。取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：Gold organisms include Gordonia sp. TY-5, Mycolicibacterium smegmatis, and Mycobacterium goodii; gold is non-exhaustive and does not prove BCP1 incapable.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> All 15 trait fields are present: 10 filled, 5 explicit unknown, 0 omitted. Values are plausible genus-level for Rhodococcus but all are marked INTERNAL_KNOWLEDGE_ONLY; there are no gold trait rows for Rhodococcus sp. BCP1. Key traits remain unverified, so D4 is 5-6 band, score 5.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状字段齐全(filled 10, explicit_unknown 5, omitted 0)。已填性状多为属级/generic描述(F7&#x27;利用多种有机物&#x27;、F8&#x27;降解丙烷及烃&#x27;、F15&#x27;广泛分布/泛化种&#x27;)；F12革兰氏阳性、F13不产孢、F11杆状、F10不运动与Rhodococcus属一致，但均仅INTERNAL_KNOWLEDGE_ONLY、无raw_text、无定量值；关键性状温度/pH/盐度/基因组均null。F9把途径酶列为酶活属循环表述。部分性状属级合理但缺菌株级证据、含过度泛化与置信偏高(F12/F13=high)。关键项证据不足，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Gold trait rows cover Gordonia sp. TY-5, Mycolicibacterium smegmatis, and Mycobacterium goodii; no Rhodococcus sp. BCP1 rows, so they neither verify nor contradict the answer&#x27;s traits.
- GOLD_SLICE / trait_scoreability_mask.tsv：Shows which gold trait subfields are observed/scoreable for the gold organisms; no BCP1 scoreability rows.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> All nine evidence_registry entries are INTERNAL_KNOWLEDGE_ONLY with database, record_id, and locator null; no locatable source supports the route, enzyme, organism, or trait claims. This is MISSING_SOURCE, not verified mis-citation. D5 1-2 band, score 2 because claims are at least mapped by internal evidence IDs.

<details><summary>V0.4理由与本行变化背景</summary>

全部证据为INTERNAL_KNOWLEDGE_ONLY(EVID_001–009)，无数据库条目/DOI/record_id，属MISSING_SOURCE(P34)；决策相关组(CORE/APPLICATION_CRITICAL：CG01/02/03/05/07/08/09)均无条目级可定位来源。按P34/P41，MISSING_SOURCE低分档、默认不cap；答案仅提供内部claim_scope映射，无可追查外部依据，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> The answer uses confidence labels and explicit nulls for five traits, but route enzymes and several traits are medium/high confidence based only on INTERNAL_KNOWLEDGE_ONLY. It does not explain evidence type or limitations; F12/F13 high confidence overstates support. This is partial uncertainty disclosure, not systemic misleading; 5-6 band, score 5.

<details><summary>V0.4理由与本行变化背景</summary>

答案用confidence标签并如实标注source_type=INTERNAL_KNOWLEDGE_ONLY（区分证据类型，正面）。但uncertainties为空数组、无显式不确定性/限制说明；对内部知识给high(F12/F13)、medium(多步)置信，强度超过依据；未披露交付路线与题面&#x27;propane degradation I&#x27;不一致这一主要限制。属多处过度确信+主要限制未说明，取4。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`207c0ab1b22fbb502e48cecdbd54c613e5005f21114d9bd682e724e5e28b3bec`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 答案覆盖了步骤、酶、菌、性状与来源等模块，但题面将 propane degradation I 的必答主链锁定为 gold S03→S02→S04→S01；答案在 acetone 后改走 hydroxyacetone/methylglyoxal 支路，并把 gold 的 acetone→methyl acetate→acetate/methanol 明确列为 alternative_branches，导致 S04/S01 未交付。D1 完成度/任务符合度的主要结论被路线偏离破坏，故在&#91;1,4&#93;内取3而非4。

<details><summary>V0.4理由与本行变化背景</summary>

模块完整度本身较高：4步均含底物/产物英文名+SMILES、酶与对应菌（S4酶整体null属诚实未知）、两个profile各15项性状齐备、证据登记9条、不确定性清单具体。但题面把路线固定为propane degradation I并明令不得改选，冻结gold该路线为propane→propan-2-ol→acetone→methyl acetate→acetate+methanol（4步，Gordonia sp. TY-5；EC 1.14.13.227 / 1.1.1.M22 / 1.14.13.226 / 3.1.1.114）；答案把acetone之后改走M. vaccae JOB5的acetol→methylglyoxal支路作为被评分主链，并把gold该路线的acetone→methyl acetate主链降为alternative_branch，同时在route_summary中自称所交付即propane degradation I。按八.D1/D2边界（P100）“自称合规却交付不同化学路线”属D1关键错误，cap≤4；因其余交付完整性好，档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：支持 gold 主链 S03 propane→2-propanol、S02 2-propanol→acetone、S04 acetone→methyl acetate、S01 methyl acetate→acetate+methanol；不支持答案的 acetol/methylglyoxal 主链。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_123：支持本案 ordered_step_count=4 且 LINEAR_UNIQUE；只说明必答主链长度为4，不证明答案替代支路正确。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 前两步 propane→2-propanol→acetone 的方向、主官能团转化与 gold 一致，路径内部连续；但 acetone 后被替换为 hydroxyacetone→methylglyoxal 支路，关键中间体/终点与题面锁定主链不符，且多个步骤省略 NADH/NAD+ 等氧化还原载体，属部分可用、需实质修订的5–6档；支路本身内部可辨但证据低，取5。

<details><summary>V0.4理由与本行变化背景</summary>

第1步（propane+O2→2-propanol）与第2步（2-propanol→acetone）化学方向正确、与gold一致，无明显原子不守恒或无依据跳步；S1/S3列O2为辅因子、水为副产物，S2仅列主底物/主产物而漏NAD+/NADH，属局部计量/辅因子缺陷（P103的7–8档内处理，不cap）。acetone之后采用acetol→methylglyoxal支路：反应本身在化学上可成立、步骤连续（未一步跳到中心代谢物），但该支路不是冻结路线的主链内容，其支持仅到教科书/自由文本级且本case证据缺口不可核验，S3无EC、S4酶整体null。综合落5–6档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：支持 gold S03/S02/S04/S01 的底物-产物方向与主链连接；不支持 S04 被 acetol 支路替代或 S01 被 methylglyoxal 支路替代。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> D3a有已确认 KEY 失败：S04 应为 acetone→methyl acetate（acetone monooxygenase methylacetate-forming, EC1.14.13.226），答案 S3 给 acetone→hydroxyacetone 且 EC null；S01 未交付；S02/S03 仍为程序U（名号/EC配对未核）。无已确认S，核心目标酶推荐失效，故在 D-KEY4 受限&#91;1,4&#93;内取2；不把未核U当S或F，也不机械取4。

<details><summary>V0.4理由与本行变化背景</summary>

第1步给出EC 1.14.13.227并绑定propane monooxygenase，与冻结gold该步EC同号（gold酶名为propane 2-monooxygenase），属可靠对应；第2步给出通用EC 1.1.1.1（alcohol dehydrogenase, NAD+），反应类型（仲醇+NAD+氧化为酮）与EC大类不矛盾，但gold对该步用1.1.1.M22的具体归类，答案具体性不足；第3步EC与基因均null、第4步酶整体null，属诚实未知而非错配。未见酶名与EC互相矛盾、也未见以广谱家族相关性冒充具体催化证据。落5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_123：支持 S04 为 acetone monooxygenase (methylacetate-forming) EC1.14.13.226，S02 accepted ADH 为 EC1.1.1.M22 集合，S03 accepted propane 2-monooxygenase 含 EC1.14.13.227；不支持 S02 EC1.1.1.1 配对或 S04 EC null 的 acetol-forming 酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：支持 S04 acetone→methyl acetate 与 S01 methyl acetate→acetate+methanol；不支持答案 S3/S4 的 acetol/methylglyoxal 目标反应。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Gordonia sp. TY-5 在前两步与 gold 的 exact organism 对上，身份与部分步骤对应合理；但 S3/S4 改由 Mycobacterium vaccae JOB5 承担，TaxID/全路径能力未在冻结 gold 或 E0 中核验，complete_pathway_organism_profile_id=ORG_002 的整路能力只有低中置信文献。属有合理候选和部分支持、关键身份/作用范围仍未充分核验的5–6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

第1、2步归Gordonia sp. TY-5，与gold步级归属EXACT一致（gold TaxID 235467），身份层要素（菌名/菌株）正确且TaxID诚实填null；第3、4步归Mycobacterium vaccae JOB5——JOB5是经典丙烷降解菌，但不在gold该路线的步级菌列（gold为TY-5/M. goodii 12523/M. smegmatis），其支持仅到经典生理学/粗酶水平，且无任何编号编造、未由“存在某酶序列”推断整条路径。无身份编造、无无关类群、无序列外推，故不满足cap；但两步归属与gold不匹配且证据粒度不足，落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_123：支持 Gordonia sp. TY-5 为 S01/S02/S04 及 S03 部分步骤的 exact organism；不含 M. vaccae JOB5 的全路径能力证明。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 两 profile 均填15项，未知项多数如实 null，F7/F8/F9 等与 EVID_001/EVID_002 的丙烷利用/酶活声称大致相称；但 gold 中 Gordonia TY-5 多数性状 UNKNOWN，M. vaccae JOB5 不在 trait gold，无法核验大量性状。F2 把30°C培养温度写成 optimum_c，raw_text 自述未测最适，是关键性状解释问题；故属部分准确/部分适用、关键项证据不足的5–6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

两profile各15项字段齐全，其中11项有值、4项诚实null（F3/F4/F5/F14），无编造编号或离谱数值。主要问题：①F2_temperature 把“grown at 30 °C”培养温度写入optimum_c（两profile同），而preference文本自述“未测定最适”——违反P52/P113“培养温度不等于最适温度”的字段语义；②F10–F13、F15等以属/种级描述（EVID_007/008）支撑菌株级profile，粒度偏粗且多条confidence标medium；③F6填好氧呼吸/O2但raw_text为null，来源链不完整。gold对TY-5性状除F14（TaxID 235467）外全部UNKNOWN，答案F14/null属诚实未知而非错误。落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_123：Gordonia TY-5 多数性状 UNKNOWN，F14 有 TaxID 235467；M. vaccae JOB5 无记录；不支持答案 M. vaccae 性状或 TY-5 的30°C最适温度。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_123：Gordonia TY-5 仅 F14 observed_accuracy，其余 completeness_only；不能把 UNKNOWN 当作已核准确。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_123：TY-5 的 F2 子字段无观测；M. smegmatis 的 F2 maximum=45 等不适用于 M. vaccae JOB5。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案给出 EVID_001–EVID_009，含具体文献题名/期刊/年份、EC 记录和 claim_scope，部分关键结论可定位；但若干属级描述和书籍章节较笼统，且 E0=EVIDENCE_GAP 不能核验引用存在性与实际支持范围。属部分关键结论可定位、其他模块仍缺映射或必要核验的5–6档，取6；无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付了9条来源（8条文献/教科书+ExplorEnz条目，locator含作者/年份/期刊/卷期页）并以evidence_id逐条映射到步骤与性状，claim_scope写明支持范围，结构可读性好。但本case E0为整题EVIDENCE_GAP（entries=0、GAP-123-CASE 103条claim无冻结事实命中），全部引用的实际支持内容无法核对，故决策相关组均为UNRESOLVED_SOURCE，不构成已核实错引、不cap。按P35/P41“存在条目级可定位结论→5–6档”与UNRESOLVED_SOURCE保留低分待核的口径，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：列出 EVID_001–EVID_009 及其 locator/claim_scope；只能证明答案交付了这些来源记录，不能证明其存在或实际支持范围。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案有 uncertainties 数组、逐 step uncertainty、confidence 分级与 null 规则，明确区分低置信/未鉴定酶和 alternative_branches；主要限制与文献分歧有披露。但 F2 仍把培养温度包装成 optimum_c，且部分属级性状标 high/medium，略过度。属7–8档中“大部分标注正确、少量条件问题”，取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据相称：明确写出acetone下游文献分歧、S3/S4缺分子水平酶鉴定、propane monooxygenase的EC为中等置信、两株菌TaxID/保藏号/基因组未确认一律null；confidence分层（未核实项low/unknown，文献直证项high）基本合理，并如实标注“文献培养温度30 °C，未测定最适”。属“大部分观测/预测/未知被正确标注、主要限制与冲突已说明”。扣分点：F2仍把30填入optimum_c与自述不一致；属级性状多标medium；ExplorEnz条目标DATABASE_DIRECT但在EVIDENCE_GAP下不可核验。属单点/局部过度确信而非系统性误导，7档内取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：证明答案披露了EC不确定、S3/S4未鉴定、TaxID/保藏号缺失和支路分歧；不证明这些披露在科学上全部充分。

</details>

## Qwen

答案SHA256：`b64ac7cb4920bd0a9d63c6c49d88d4623ff04135c30bd45bb6f4ed175dc1ec7a`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 答案给出3步末端氧化链（propane→1-propanol→propanal→propanoate），但题目指定的gold主链为4步丙烷經propan-2-ol、acetone、methyl acetate至acetate/methanol；缺失S01/S04且S02/S03为非match。另有15项性状全为null。路线明显偏离且必要主链大部分未交付，落入D1低档；因任务路线偏离按D1关键错误处理，分数压在4分以下。

<details><summary>V0.4理由与本行变化背景</summary>

3–4档。①任务参数偏离（关键错误）：题面 route_scope 指定 propane degradation I，冻结 gold 的同一 pathway（BSY-p00863）主链为 subterminal oxidation（propane→propan-2-ol→acetone→methyl acetate→acetate+methanol，终点 Acetate|Methanol），答案却交付 terminal oxidation（propane→1-propanol→propanal→propanoate），并在 route_summary 自称&#x27;在 propane degradation I 主链中……&#x27;，属&#x27;自称合规却交付不同化学路线&#x27;，按八.D1/D2边界条款与OBS-D1D2归D1关键错误；②15项性状全部 value:null（明确未知非编造），性状模块实质空白，D1反映完成度不足。关键错误cap≤4，档内因路线偏离叠加性状全缺取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：Defines the required gold main-chain steps, orientation and terminal products; does not by itself prove that no alternative terminal-oxidation chemistry exists.
- ANSWER_TEXT / ANSWER：Shows the delivered three-step terminal-oxidation route and the absence of the gold S01/S04 route steps.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 就答案自身所答的末端氧化路線而言，propane→1-propanol→propanal→propanoate三步方向一致、主有機物連續且無明顯原子斷裂；醇脱氢酶與醛脱氢酶步驟化學上可成立。主要缺陷是氧/NAD(P)輔因子未在反應式中列明，且此為替代路線而非gold主鏈。按D2對所答化學獨立評價，替代化學可成立時最高6分，故取6。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档。答案交付的是 terminal oxidation 主链（propane→1-propanol→propanal→propanoate）：三步反应类型（单加氧羟化→醇脱氢→醛脱氢）各自化学自洽，无方向反转、无原子明显不守恒、无一步跳到中心代谢物；辅因子（O2/NAD+）标注不全属局部计量缺陷，按八.辅因子条款不cap。但该路线并非题面指定的 propane degradation I（冻结为 subterminal oxidation，止于 acetate+methanol），且仅有 INTERNAL_KNOWLEDGE_ONLY 自证、无外部可核证据（四.5第3步：无证据按未证实登记、不自动判错也不给高分）。路线化学部分成立但关键中间体/终点与指定路线不符、证据有限，路线偏离另在D1计，不连坐，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s terminal-oxidation chemistry and continuity.
- RUBRIC_CLAUSE / R2-62：Alternative chemistry is evaluated on its own D2 quality and is not credited as target-route completion.

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 本题4個必答目標中，S02/S03已確認為route-blocked nonmatch（F），S01/S04 alignment not confirmed（U），S=0；已確認KEY失敗適用D-KEY4上界4。答案三個酶步驟全屬另一條末端氧化路線，對gold目標反應無已核目標信用；錯誤路線內部酶自洽不獲D3a目標信用。由於無任何目標步獲得S，取1。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档。三步酶功能-EC在形式层面与反应类型匹配：S1 alkane 1-monooxygenase EC 1.14.15.3（单加氧酶↔羟化）、S2 alcohol dehydrogenase EC 1.1.1.1（醇脱氢↔醇→醛）、S3 aldehyde dehydrogenase EC 1.2.1.3（醛脱氢↔醛→酸），无酶名与EC自相矛盾、无家族相关性冒充具体催化。但均为泛化酶名、无 gene_or_protein、confidence=low，且证据全为 INTERNAL_KNOWLEDGE_ONLY；三个EC在E0 item_gap 中均无冻结记录，当前无法核实 accepted name/reaction 与条目状态。属合理候选+部分支持、关键步骤缺具体核验，取5（不因错引归D5而连坐）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：Shows required target reactions and why the answer&#x27;s terminal-oxidation steps are not the gold target steps.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_123：Shows accepted enzyme associations for the gold target steps; does not by itself prove any specific protein activity.
- ANSWER_TEXT / ANSWER：Shows which enzyme/EC claims were actually delivered.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案反覆使用Mycobacterium sp. TY-6作為三步對應菌，TaxID為null，僅有INTERNAL_KNOWLEDGE_ONLY證據；該菌名/菌株身份及步級或全路徑能力在E0中無法核實。gold列出的主要菌為Gordonia sp. TY-5、Mycolicibacterium smegmatis、Mycobacterium goodii，但gold非窮盡；因此不把未核實直接判為錯。按合理候選但關鍵身份/能力未充分核驗，取5。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档。单一菌 Mycobacterium sp. TY-6（ORG_001）被用于全部三步，身份仅以 INTERNAL_KNOWLEDGE_ONLY（EVID_005）自证，无 TaxID、无保藏号、无基因组号，身份定位/反应级能力/完整路径能力三层均无法核实；同一菌覆盖整条三步链，存在把属级/单步信息外推为全路径能力的风险，但 Mycobacterium 属为已知烷烃降解类群、未发现跨属/无关类群错配，故身份错配未坐实＝UNRESOLVED，不判KE、不cap；菌株级能力证据缺失，档内取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_123：Lists gold-associated organisms and shows they differ from the answer&#x27;s candidate; does not prove that no other organism can perform the claimed alternative steps.
- ANSWER_TEXT / ANSWER：Shows the delivered microbial identity, null TaxID and reuse across steps.

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> ORG_001的15項性狀全部為null且confidence=unknown；沒有交付任何可評價的性狀值。依P44，全部必需性狀均為null/空值時D4按MISSING記1分，不宣稱檢測到科學錯誤。

<details><summary>V0.4理由与本行变化背景</summary>

唯一 organism_profile（ORG_001）的 F1–F15 全部 value:null、confidence=unknown、evidence_id=null，无任何可评价性状内容。按量表四.4/P44&#x27;全部必需性状均为null/空值时D4按MISSING记1分，不宣称检测到科学错误&#x27;。MISSING=1按合同参与加权总分与科学子分，权重保留、不删除、不重归一。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all 15 trait values are null/unknown.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_123：Shows which traits have scoreable observed values; not used to backfill answer values.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry的EVID_001–EVID_005全部為INTERNAL_KNOWLEDGE_ONLY，無database、record_id或可定位外部文獻；decision-relevant claim groups均只有內部知識，沒有可核對的條目級來源。此屬MISSING_SOURCE低分檔，不是已核實錯引；無VERIFIED_MIS_CITATION_*，不觸發D5 cap。取2。

<details><summary>V0.4理由与本行变化背景</summary>

低分档。答案全部证据（EVID_001–EVID_005）source_type 均为 INTERNAL_KNOWLEDGE_ONLY，database/record_id 为 null，仅有自建 locator 与局部标签，无法沿任何可定位文献/数据库条目/计算记录核查路线、酶-EC、菌株身份或性状——按四.3/P34 属 MISSING_SOURCE（完全无外部引用、仅INTERNAL_KNOWLEDGE_ONLY自证）。MISSING_SOURCE 默认不触发关键错误；E0 为 EVIDENCE_GAP、无已核实错引，故无 LOCAL/CRITICAL/SYSTEMIC。给2（低分档；略高于最低因答案保留自建证据登记与claim_scope/confidence结构）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all delivered evidence entries are INTERNAL_KNOWLEDGE_ONLY and lack external locators.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分5 → V0.5新分8，变化+3。

新裁判理由：

> 答案明確使用low/unknown confidence，15項性狀全填null，uncertainties列出氧條件未指定、初始單加氧酶未核實、性狀缺來源；沒有把推測包裝成高置信觀測。主要限制是route_summary仍把末端氧化鏈表述為propane degradation I，未明說其為替代路線；但source_type=INTERNAL_KNOWLEDGE_ONLY與低置信已部分披露。屬7–8檔，取8。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档。答案有具体且诚实的不确定性披露：oxygen 未指定、初始单加氧酶具体酶系/EC/基因未核实、菌株性状无来源故全部填 null 并标 unknown、EVID 全标 low（属正面披露，不因篇幅加分）。但①把 terminal oxidation 直接写成题面指定的 &#x27;propane degradation I&#x27; 主链（route_summary 断言、is_single_continuous_route=true），未披露该化学路线可能与题面指定路线不一致，属对路线合规性的过度确信；②酶-EC 仅以 INTERNAL_KNOWLEDGE_ONLY 的 low 包装而未提示应复核。整体披露较具体、无系统性把预测写成实证、无掩盖已知矛盾，故不cap，档内取5。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows explicit uncertainty statements, low confidence labels and null/unknown handling.

</details>

## Grok

答案SHA256：`d68c6c1c2651f2801c19a8847e25385d1ec7453c48f3592afaaa3c08ebb873aa`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 2/10. The answer delivers a complete-looking terminal oxidation chain and all module types, but it does not follow the gold required propane degradation I main chain: gold requires S03 propane→propan-2-ol, S02 propan-2-ol→acetone, S04 acetone→methyl acetate, S01 methyl acetate→acetate+methanol. The answer provides propane→1-propanol→propanal→propanoate. Required S01/S04 are missing; S02/S03 are different reactions. This is a severe route/task deviation, D1 key error cap≤4; score 2 because the answer is organized and includes all module types, but target-route compliance fails.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Shows the required main chain is S03 propane→propan-2-ol, S02 propan-2-ol→acetone, S04 acetone→methyl acetate, S01 methyl acetate→acetate+methanol; does not assess the answer&#x27;s terminal-oxidation chemistry.
- GOLD_SLICE / formal_cases.tsv：Records 4 ordered gold steps, LINEAR_UNIQUE, required for the task.

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 6/10. The answer&#x27;s own route is a chemically plausible terminal oxidation: propane→1-propanol→propanal→propanoate, with O2 in step 1 and NAD+/NADH in steps 2-3. It is continuous and directionally consistent. It omits a reducing equivalent/electron donor in step 1 and uses a simplified water/H+ balance, so it is not higher than 6; moreover, as an alternative route it is capped at 6 by C06. No D2 key error.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Confirms the gold target route differs; D2 is scored independently on the answer&#x27;s terminal-oxidation chemistry.

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 1/10. D3a is target-reaction enzyme correctness. None of the four gold target reactions is supported: S01 methyl acetate hydrolase and S04 acetone monooxygenase are absent; S02 target propan-2-ol→acetone is replaced by 1-propanol→propanal (EC 1.1.1.1, not accepted 1.1.1.M22); S03 target propane→propan-2-ol via propane 2-monooxygenase is replaced by propane→1-propanol via a broad propane monooxygenase. So S=0/N=4, no target credit. The enzyme names are plausible for the alternative route but do not earn target credit. Score 1.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：Required target enzymes: methyl acetate hydrolase 3.1.1.114; secondary alcohol dehydrogenase 1.1.1.M22; propane 2-monooxygenase 1.14.13.227/M31; acetone monooxygenase 1.14.13.226. Does not support the answer&#x27;s terminal-oxidation enzymes.
- GOLD_SLICE / reaction_gold.tsv：Required directed reactions/products; the answer&#x27;s steps differ or are missing.

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 5/10. The answer proposes a single strain, Rhodococcus rhodochrous PNKb1, for all steps and claims it completes the pathway. The identity is a plausible propane-degrader candidate, but no TaxID/genome and no frozen strain-level record support PNKb1; all support is EVID_001 internal knowledge. Gold target organisms are different (Gordonia TY-5 etc.), but gold is non-exhaustive and does not by itself disprove PNKb1. Thus 5-6 band: reasonable candidate/partial support, key strain-level and whole-pathway capability unverified. Score 5.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：Gold target route organisms are Gordonia sp. TY-5, Mycolicibacterium smegmatis, and Mycobacterium goodii; does not by itself disprove an alternative organism&#x27;s capability because gold is non-exhaustive.

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 5/10. 9/15 traits filled, 6 explicit unknowns. F1/F6/F7-F9 and F10-F13 are plausible qualitative traits, but support is genus-level/internal; key quantitative traits (temperature, pH, salinity), collection, genome, and habitat are null. No frozen PNKb1 trait rows. Thus partial traits, key evidence insufficient, 5-6 band; score 5.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Gold has no PNKb1 trait rows; cannot verify the answer&#x27;s PNKb1 traits. Target organism traits do not apply to PNKb1.
- GOLD_SLICE / trait_scoreability_mask.tsv：Shows which target-organism traits are scoreable; it is not a source for PNKb1.

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 4/10. The answer delivers an evidence_registry with claim_scope mapping, but all three entries are INTERNAL_KNOWLEDGE_ONLY; no database record IDs, DOIs, or entry-level records are delivered. D5 source status is MISSING_SOURCE for decision-relevant groups. No verified mis-citation, so no cap; low 3-4 band. Score 4 for explicit claim mapping and literature locators.

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> SCORED 8/10. The answer explicitly distinguishes internal knowledge from observations, marks unknowns as null, states route-name ambiguity, alternative branches, missing EC/gene/TaxID/genome, and limits claims. Minor overconfidence in high confidence for Gram/sporulation from genus-level description, but not systemic. 7-8 band; score 8.

## GPT5.6

答案SHA256：`b3171cf62c174591b2c9f4c6922ea642f31c81583c4a2d4ba3c3b353171d09af`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定propane degradation I，但答案主链为丙烷末端氧化至丙酸，与gold主链（propane→isopropanol→acetone→methyl acetate→acetate+methanol）明显不一致；且15项性状全部null。虽提供3步路径、酶和菌字段，但核心任务路线与性状模块大面积失败，落1–2档，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：证明gold主链方向与步骤；不支持答案的末端氧化路线。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_123：证明根底物为Propane、terminal main products为Acetate|Methanol；不证明所有丙烷降解路线。

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案自身三步化学（Propane→1-Propanol→Propanal→Propanoic acid）方向连续、结构合理，属可成立的末端氧化表达；但辅因子O2/NAD+未列、终点丙酸未继续到C2/C1，且并非gold主链。按D2独立化学质量与base range&#91;1,6&#93;，取上沿6，表示主干可成立但需实质修订。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：支持答案自身三步转化链；不证明实验活性、辅因子完整性或目标主链一致性。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四个必答目标步均无目标信用：S01、S04在答案中缺失；S02、S03答案给出的是末端氧化路线的1-丙醇/丙醛步骤，与gold的异丙醇→丙酮、丙烷→异丙醇不匹配。错误路线内部酶自洽不获目标信用，故落1–2档，取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_123：gold各步主底物/主产物与方向；不支持答案的末端氧化步骤。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_123：gold accepted酶/EC集合；不支持答案EC与gold步骤的对应。
- ANSWER_TEXT / ANSWER_TEXT：答案实际交付的酶名/EC；不证明其对应gold目标反应。

</details>

### D3b 微生物身份与能力：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案三步均绑定Mycobacterium sp. TY-6，无TaxID、保藏号或菌株级能力证据；gold步骤菌为Gordonia sp. TY-5、Mycolicibacterium smegmatis、Mycobacterium goodii strain 12523等。属合理属级候选但多处身份/能力不匹配且复用同一菌，落3–4档，取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_123：gold各步参考菌及身份；不证明TY-6执行这些步骤。
- ANSWER_TEXT / ANSWER_TEXT：答案交付的菌名/菌株；无TaxID和菌株能力证据。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题目要求每个organism_profile返回15项性状；答案全部15项均为null/unknown，未交付任何可评价性状值。按P44全部必需性状null时D4记MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：证明15项性状均未填写；不证明任何性状正确或错误。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry四条均为INTERNAL_KNOWLEDGE_ONLY，无database、record_id或locator；路线、酶、菌、性状均无可定位外部来源可核对。属几乎无法定位重要结论依据，落1–2档，取2；未出现可核实错引，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：证明来源仅为内部知识标签；不证明其对应任何外部条目。

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确说明题面未指定氧条件、按有氧主链表达；主动把TaxID/保藏/基因组/性状留null；对EC分类和菌株反应归属标注low/medium等不确定性。未见系统性把预测写成实证，但未指出与指定主链的替代关系，限制说明部分笼统。落5–6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：证明答案已作部分不确定性披露；不证明其所有科学声称已核实。

</details>
