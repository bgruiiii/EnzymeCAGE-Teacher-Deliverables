# BIOPATH150_106：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：β myrcene degradation

污染物：Geraniol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 57 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 48 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 73 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 59 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 65.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 49.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`5429730662c8f57c5da74222dc8caca086dab6d75daa19e18a18e44a2becc70d`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 输出包含8步主链、每步酶/菌、15项性状框架和明确不确定性，模块基本齐备；但所选链与gold分支/终点关系未绑定，未交付linalool/myrcene分支，若干性状为null，故落在5–6档上沿。

<details><summary>V0.4理由与本行变化背景</summary>

全部必要模块实质交付：8步主链每步含底物/产物英文名+SMILES、酶+EC(部分null)、对应微生物；15项性状齐备；evidence_registry、uncertainties、downstream/alternative_branches齐备；路线名原样保留。少数EC/taxid为null属允许的明确未知，不构成任务偏离或路线改选。处7-8档（充分，少量缺失/粒度问题）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_106：Gold为BRANCHED_DAG、n_required=4、β myrcene degradation；不能把全图旁支简单当作单一线性主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_106：Gold根为Geraniol，终产物记录为Geranate|Myrcene；答案起点正确，但未交付Myrcene终点。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：Gold显示S01→S02与S04→S03两条分支；不证明答案S3–S8下游全部为目标步。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> S1–S8化学方向总体为底物→产物，S1/S2与gold一致，后续Atu/Liu路线连贯；但S5合并多个修正β-氧化反应且逐中间体不清，S1/S2及部分步骤辅因子未完整列出，属局部计量/表达缺陷，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

S1香叶醇→香叶醛、S2香叶醛→香叶酸与gold S01/S02的主转化及氧化方向一致；S3-S8经Atu/Liu途径延伸至乙酰CoA+乙酰乙酸，转化类型与连接连贯合理。局部问题：S5把修正β-氧化多步合并，3-isohexenylglutaconyl-CoA→3-甲基巴豆酰CoA+乙酰CoA的碳计量不闭合、产物归属笼统（答案自标low/推断）。属局部计量与表述缺陷，处7档；无起始步错误、无方向反转、无关键断裂，故不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：仅直接支持gold S01/S02及S03/S04反应；不覆盖答案S3–S8下游Atu/Liu步骤。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：列出S01/S02等gold酶/EC条目；不证明答案S5合并酶系或S3/S7空EC已确认。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> S1的geraniol dehydrogenase EC1.1.1.183与S2的geranial dehydrogenase EC1.2.1.3均命中gold accepted set，S01/S02在策展粒度有支持；但S03/S04的linalool/myrcene分支未作为步骤交付，selected branch/current_path_id未绑定，且S01/S02表示等价仍待裁，故为部分主干可用、5–6档。未施加确认KEY4硬上限，因key_authority_status仍为pending且key_definition_complete=false。

<details><summary>V0.4理由与本行变化背景</summary>

S1 geraniol dehydrogenase EC 1.1.1.183、S2 geranial dehydrogenase EC 1.2.1.3 与gold酶表一致；S4 geranoyl-CoA carboxylase 6.4.1.5、S6 3-甲基巴豆酰CoA羧化酶 6.4.1.4、S8 HMG-CoA裂解酶 4.1.3.4 均与相应反应类型匹配；S3/S5/S7 EC未确认如实填null。核心步骤酶-反应对应正确，仅下游EC未被冻结证据覆盖，处8档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：S01 accepted set含geraniol dehydrogenase EC1.1.1.183；S02 accepted set含geranial dehydrogenase EC1.2.1.3；仅为G4策展粒度，不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：gold S01=Geraniol→Citral(geranial)，S02=geranial→Geranate；S03/S04属另一分支，答案未逐步交付。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_106：记录BRANCHED_DAG、n_required=4；不自动绑定答案所选主链。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> Castellaniella defragrans物种身份与gold TaxID 75697一致，且gold对该物种有PATHWAY_COMPLETE=TRUE；但答案使用strain 65Ph3且TaxID=null，菌株级身份未核，S3–S8的步级归属多为自己承认为推断，故为合理候选+部分支持、若干关键作用范围未充分核验的5–6档。

<details><summary>V0.4理由与本行变化背景</summary>

推荐单一菌Castellaniella defragrans，与gold organism_gold(taxid 75697)覆盖S01/S02并PATHWAY_COMPLETE一致，物种选择正确；将Atu/Liu下游酶赋予该菌为推断（答案自述主要证据来自Pseudomonas citronellolis，已披露）。菌株号65Ph3为答案自述凭记忆、TaxID为null，无冻结证据可核→UNRESOLVED，不判错。无虚构身份、无跨类群错配，处7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：gold同物种Castellaniella defragrans TaxID 75697、GCA_014203015.1；物种级支持不自动核验strain 65Ph3。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：gold对TaxID 75697有部分观测性状与PATHWAY_COMPLETE行；不证明该菌株完成答案全部S3–S8步骤。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 15项均返回，已给F1/F6/F7/F8/F9/F11/F12/F13/F15等与C. defragrans物种常识或gold部分观测相容；但F2/F3/F4/F5/F10/F14明确unknown，而gold对温度、盐度、保藏、运动性、基因组等有部分观测，关键性状缺口明显，且部分值为内部推断，故5–6档下沿。

<details><summary>V0.4理由与本行变化背景</summary>

9项性状给出且基本与gold(75697)观测一致：F11杆状、F12革兰氏阴性、F13不产芽孢、F6硝酸盐呼吸/反硝化与gold观测吻合；F2/F3/F4/F5/F10/F14如实置null(明确未知)。问题：性状来源为INTERNAL_KNOWLEDGE_ONLY(无定位记录)，F15栖息地&#x27;中等偏窄&#x27;、F8&#x27;多种单萜&#x27;属描述性推断(low/medium)。填充值准确+诚实null，处7档，不判MISSING因已实质作答。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：gold对TaxID 75697有温度、盐度、保藏、运动性、基因组等部分观测；不核验strain 65Ph3，也不覆盖所有答案值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_106：标示部分性状可作observed_accuracy、部分仅completeness_only；不把缺失自动当错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_106：温度/盐度等子字段存在pending adjudication或completeness_only；不能强行按完整数值准确率评分。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry全部为INTERNAL_KNOWLEDGE_ONLY或MODEL_INFERENCE，无DOI、数据库条目、record_id或可定位locator；关键路线/酶/菌/性状结论只能追到答案自建EVID标签，属MISSING_SOURCE低档。E0为EVIDENCE_GAP，无已核实错引，故不cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 6条中EVID_001-005均为INTERNAL_KNOWLEDGE_ONLY自我声明、EVID_006为MODEL_INFERENCE，无任何DOI/数据库条目/登录号等可定位外部记录；路线、酶、菌、性状关键结论均无外部可追溯来源，D5主要目标(可追查)几近落空。按P34 MISSING_SOURCE判低档(2)；这是缺失而非误导，默认不触发cap，key_error=N。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 逐项给出confidence、source_type、null未知和uncertainties，明确区分内部知识/模型推断与已知事实，披露EC未确认、S5为推断、strain凭记忆、氧条件null等；仅F12/F13等个别高置信与整体证据强度略有张力，但未构成系统性误导。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性与边界披露具体诚实：逐项标confidence、未知置null/unknown；uncertainties明文列出S3/S5/S7 EC未确认、S5合并推断、下游酶赋C. defragrans为推断、菌株号凭记忆待核；区分内部知识与模型推断。未见预测冒充观测或掩盖矛盾；高置信标签(F12/F13)落在已核实正确项，无系统性误导。处8档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`c1970937fef83eacdee9ff20009edf112ffc55c417ec481163955ca6208b2d8d`。

### D1 完整性与任务符合度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案按题面填写 chosen_route_name=β myrcene degradation，给出9步、每步酶与微生物，1个去重 organism_profile 及15项性状，主要模块均有涉及。按D-M01所评P106_1两项主链步骤核心完整；但S3-S9多数底物/产物SMILES为null，S5 EC为null，部分性状以低置信内部知识填补而非null，交付完整性存在遗漏，故D1=7。

<details><summary>V0.4理由与本行变化背景</summary>

六个交付模块均有实质内容（9步主链、每步绑定酶与菌、15项性状、evidence_registry、uncertainties），route_scope.chosen_route_name逐字回显题面路线名，未出现改选路线或更改氧条件等任务参数偏离；但题面明确要求每步给主底物与主产物的SMILES，S3–S9共6步SMILES为null（12项应填字符串缺失），菌株/保藏号/TaxID全为null（仅物种级身份），且gold为双分支DAG而答案只交付一支——属“主要模块均有涉及，但若干必要内容遗漏”档（5–6），档内取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_106：题面路线名为β myrcene degradation、污染物为Geraniol；不证明答案步骤完整
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_106：本题为分支DAG，全图4步；D-M01只评一条采用主链，未选分支不扣缺步
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：Pseudomonas citronellolis出现在S01 geraniol dehydrogenase记录中；不证明全路径能力
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：P. citronellolis可评分性状记录；不证明答案全部15项来源

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 所评P106_1主链（Geraniol-&gt;Geranial-&gt;Geranate）前两步方向与化学正确，符合reaction_gold。但答案把β-氧化延伸写为主链：S6 thiolysis产物3,7-Dimethyl-6-octenoyl-CoA为C10，与C10 3-oxogeranoyl-CoA裂解应得C8 acyl-CoA+acetyl-CoA不守恒；S7将C6双键直接水合为β-氧化步骤无依据；S9产物2,6-Dimethylhept-5-enoyl-CoA为C9，与C10 3-oxoacyl-CoA裂解应得C8+acetyl-CoA不守恒。多个重要下游步骤违反原子守恒且无说明，构成D2关键错误，分数受限≤4；核心前两步正确、边界清楚，取4。

<details><summary>V0.4理由与本行变化背景</summary>

主链前两步与gold逐字吻合：Geraniol→Geranial（伯烯丙醇氧化为醛）与Geranial→Geranic acid（醛氧化为酸），SMILES与方向正确；S3–S9为CoA活化+类β-氧化序列（水合→氧化→硫解，C10→C8→C6），碳数收支自洽、反应类型与所写酶功能一致，化学上成立。缺陷为通篇未写任何辅因子（NAD+/NADH、CoA、ATP），属局部计量缺陷，按P103留在7–8档不cap；S7–S9为推测步骤但已在uncertainty标注；未覆盖gold的myrcene支属覆盖问题而非化学错误，末端延伸至gold终点下游不加分亦不扣分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：S01 Geraniol-&gt;Citral、S02 Citral-&gt;Geranate；支持前两步目标反应，不覆盖β-氧化延伸
- ANSWER_TEXT / ANSWER.steps&#91;5&#93;.products：S6产物3,7-Dimethyl-6-octenoyl-CoA为C10；C10 3-oxoacyl-CoA经thiolysis应生成acetyl-CoA(C2)+C8 acyl-CoA
- ANSWER_TEXT / ANSWER.steps&#91;8&#93;.products：S9产物2,6-Dimethylhept-5-enoyl-CoA为C9；C10 3-oxoacyl-CoA经thiolysis应生成acetyl-CoA(C2)+C8 acyl-CoA
- RUBRIC_CLAUSE / P100：D2评价反应化学本身（转化、方向、守恒、连续性）

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 按所采用P106_1主链两项目标反应评D3a。S01 geraniol-&gt;geranial用geraniol dehydrogenase EC 1.1.1.183，accepted集合含该名/EC，属已确认目标功能（S）。S02 geranial-&gt;geranic acid用geranial dehydrogenase，名称在accepted集合，但显式EC 1.2.1.82不在accepted集合（1.2.1.3/1.2.1.86），且representation比较处于hold，故为U/PAIR_UNVERIFIED，不能算S。无已确认KEY失败；已支持部分清楚，待核部分明确，但仍阻止进入7-8，故D3a=6。

<details><summary>V0.4理由与本行变化背景</summary>

S1 geraniol dehydrogenase EC 1.1.1.183与gold的BSY-e04182（同EC、同反应geraniol→citral）一致，属可靠支持；S2酶名geranial dehydrogenase与gold酶名相符，但EC 1.2.1.82落在gold多注集合{1.2.1.3,1.2.1.86}之外且冻结证据无该号官方条目，按P65–P66记UNRESOLVED、不判错；S3–S9使用类别自洽的通用β-氧化酶（4.2.1.130水合酶、2.3.1.16硫解酶、4.2.1.17烯酰-CoA水合酶、1.1.1.35羟基酰-CoA脱氢酶），S5 EC诚实置null并标注未确定；整体属“有合理候选和部分支持，但若干关键步骤缺具体核验”档（5–6），取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：S01 accepted geraniol dehydrogenase含EC 1.1.1.183；S02 accepted geranial dehydrogenase为EC 1.2.1.3/1.2.1.86，不含1.2.1.82
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：S01 Geraniol-&gt;Citral、S02 Citral-&gt;Geranate；支持目标反应功能，不单独确认显式EC配对
- SCOPE_ROW / SCOPE#BIOPATH150_106#CG04：题面氧条件为null，条件组不成立，仅作背景

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> P. citronellolis为真实物种，organism_gold在S01 geraniol dehydrogenase行给出与答案一致的物种名，可支持身份与S01单步归属；但答案把同一物种用于全部9步并设置complete_pathway_organism_profile_id=ORG_001，冻结organism_gold的PATHWAY_COMPLETE仅为Castellaniella defragrans，S02-S09及全路径能力没有相应证据。属部分身份/单步支持但全路径声称未核，取5-6档下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

物种级身份Pseudomonas citronellolis在organism_gold为EXACT匹配（TaxID 53408、GCA_001586155.1），且见于S01的geraniol dehydrogenase步骤，身份定位成立；strain/TaxID/保藏号一律null（诚实null），身份粒度为物种级。但同一物种被指派到全部9步并设complete_pathway_organism_profile_id=ORG_001，构成完整路径能力声称，而gold仅支持其单步（S01）归属、未登记其全路径能力——属疑似“单步支持写成全路径能力”，E0无事实记录可核实，故记UNRESOLVED、不cap；按身份粒度不足档内扣，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：支持P. citronellolis与S01 geraniol dehydrogenase的物种级对应；不表示其完成整条路径，也不覆盖S02-S09的步级归属。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：S01有geraniol dehydrogenase酶行；不证明P. citronellolis对答案S3-S9各酶均有反应级能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 可核对项：F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating与trait_gold的P. citronellolis观测/预测行一致；F2 30°C和F3 pH7落在观测范围内但最适值本身无观察来源；F7称利用香叶醇、F8称降解单萜醇类，在trait_gold无相应观察；F14已有GCA_001586155.1及基因组统计却留空。属部分性状可用、关键应用性状证据不足，取5-6档下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating四项与gold中P. citronellolis(53408)的OBSERVED记录完全一致，属关键性状可核实；F1&quot;aerobic&quot;与gold aerotolerant相容；F2最适30℃、F3最适pH7落在gold观测生长区间内但最适子字段无观测真值可比（completeness_only），且F2/F3的min/max（gold可提供）被留空；F4/F5诚实null（F5在gold本即UNKNOWN）；F14三项null而gold本有GCA_001586155.1与基因组大小/GC区间，属完成度不足；F15填&quot;土壤和水体&quot;是栖息地名称列举，未按题目要求描述广适性；全部性状来源仅EVID_001(内部知识)。属“部分性状准确且适用，但关键项证据不足”档（5–6），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：支持P. citronellolis的motility/rod-shaped/Gram-negative/non-sporulating等观测；F7/F8香叶醇利用与单萜降解、F2/F3最适值无观察行。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_106：说明optimum_c等子字段为completeness_only或无观察来源；观测范围不等于最适值。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案唯一证据为EVID_001/EVID_002，均source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全空；路径、酶-EC、菌株全路径与多数性状均无法沿条目核查。E0为EVIDENCE_GAP，不把未核判为虚构；但就可追溯性本身，属于几乎无法定位重要结论依据的1-2档，取2。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅两条EVID_001/EVID_002，source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null，claim_scope只作宽泛分组（organism traits/taxonomy、pathway enzymes/reactions），决策相关组（CG01路线、CG02起点、CG03终点、CG05酶-EC、CG07核心菌身份）无任何条目级可定位证据，属MISSING_SOURCE低分档（P34：缺失而非误导，默认不cap）；E0为EVIDENCE_GAP，无任何已核实错引，severity不适用；故按“几乎无法定位重要结论依据”给1–2档，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry.EVID_001：仅证明答案自报INTERNAL_KNOWLEDGE_ONLY；不提供可定位数据库条目或文献。
- ANSWER_TEXT / ANSWER.evidence_registry.EVID_002：仅证明答案自报INTERNAL_KNOWLEDGE_ONLY；不提供可定位数据库条目或文献。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案有具体不确定性记录：S5 EC未定、S7-S9 β-氧化为推测、strain/TaxID/基因组未指定；多数步骤confidence为low/medium。但S2的EC在冻结目标中未解，答案仍标high；全路径与F7/F8应用性状以内部知识呈现，未系统说明证据类型与适用边界。属5-6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

答案提供了具体而非笼统的不确定性披露：uncertainties列出EC未定、S7–S9 β-氧化步骤为推测、菌株/TaxID未指定，并在S5/S7/S8/S9的uncertainty字段重复标注，source_type诚实标为INTERNAL_KNOWLEDGE_ONLY而非冒充数据库直查，trait confidence按项区分低/中/高——这些属正面。但S1/S2酶以及F12等高置信标签建立在纯内部知识之上且未加“建议复核”限定；未披露“路线名β myrcene degradation所对应的myrcene支未被交付”这一范围边界；complete_pathway_organism_profile_id未加边界说明；F15以栖息地名称充当广适性。属“有不确定性说明，部分结论强度仍略超依据、范围披露不全”档（5–6），取6，未达系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案主动列出的部分未知与推测；不覆盖所有关键未核项。
- ANSWER_TEXT / ANSWER.steps.confidence：显示S1/S2等被标high、S7-S9标low；不证明这些置信标签与实际证据强度相符。

</details>

## Kimi

答案SHA256：`a5fb41668e13bda2773ccf0d5e41f7024ea6b9f65e8222295bfb4476501762a3`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分7 → V0.5新分9，变化+2。

新裁判理由：

> 以可对齐的已认可主链P106_1（S01 Geraniol→geranial；S02 geranial→Geranate）核对：答案从Geraniol起，S1/S2均给出底物、产物、SMILES、首选酶与EC、对应微生物；organism_profiles按同一菌去重为一个profile并由各步复用，15项性状齐全（未知按null），route_scope.chosen_route_name原样保留。S3–S6为Geranate下游延伸，题面未要求且按D-M01/P29不据此扣缺步；但答案未在downstream_continuation/notes中明确标出该延伸属评分主链外，属范围呈现小缺陷。主链必要模块覆盖完整、字段关联清楚，故给9。

<details><summary>V0.4理由与本行变化背景</summary>

六个步骤均给出底物/产物英文名、逐步酶（名称+EC，S6 EC为null）与对应微生物，route_scope.chosen_route_name逐字回填题面路线“β myrcene degradation”，15项性状全部出现（7项有值、8项明确null、0项遗漏），路线连续、模块关联清楚。扣分点：geranoyl-CoA、isohexenylglutaconyl-CoA、3-hydroxy-3-isohexenylglutaryl-CoA、acetyl-CoA及NAD+/ATP/CoA等成员SMILES为null；S6裂解酶无EC；温度、pH、盐度、保藏号、运动性、基因组等冻结gold中已有观测记录的性状仍以null交付（属如实未知而非编造，完成度扣分）。属“大部分必要内容完整、少量遗漏”档，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_106：本题路线名为β myrcene degradation，全图为BRANCHED_DAG；全图ordered_step_count不等于必须交付全部分支。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：提供S01 Geraniol→Citral/geranial与S02 Citral/geranial→Geranate的两步主链行；支持将该两步作为已认可主链P106_1核对，不扩展到下游未列步骤。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：Castellaniella defragrans与S01/S02酶行存在STEP级关联；不证明未列的下游每步均由该菌完成。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案原文确实填写route_scope、6个steps、一个去重organism_profile及15项trait外壳；部分trait值与部分下游SMILES为null/未知。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 按已认可主链P106_1评：S1 geraniol→geranial为醇氧化，S2 geranial→geranic acid/Geranate为醛氧化，方向与碳骨架连续；S2与gold的Geranate仅质子化/电荷表示不同（route诊断CHARGE_NOTATION_ONLY）。S1答案用NADP+/NADPH而gold反应行列NAD+/NADH，属局部辅因子差异；S2名称/电荷表示亦需少量规范化。S3–S6为P106_1终点外下游内容，不作为D2加分，也不据此补主链；不改变主链化学结论，故给8。

<details><summary>V0.4理由与本行变化背景</summary>

主链 geraniol→geranial→geranic acid→geranoyl-CoA→isohexenylglutaconyl-CoA→3-hydroxy-3-isohexenylglutaryl-CoA→acetyl-CoA + 7-methyl-3-oxooct-6-enoic acid 方向一致、前驱后继衔接完整，氧化还原对（NADP+/NADPH、NAD+/NADH）与ATP/CoA/碳酸氢盐/AMP/PPi、ADP/Pi计量基本成对，裂解前后碳数守恒。S1–S2与gold S01–S02同反应、同多注酶集合（答案取EC 1.1.1.183为NADP+型geraniol dehydrogenase，与所选酶自洽，并非与gold冲突）。gold为BRANCHED_DAG（含geraniol→linalool→myrcene第二支），答案只给单一主链并自geranate继续向下游延伸：题面未指定终点，未覆盖gold另一分支与超出gold终点的延伸均不进入覆盖率扣分；延伸段与经典无环单萜降解路线化学一致，但冻结证据无记录（见unverified_subclaims）。属“主链及关键转化有充分依据、少量局部问题”档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：S01为Geraniol→Citral/geranial并带NAD+/NADH；S02为Citral/geranial+H2O+NAD+→Geranate+NADH+H+；支持主链两步的方向与转化，不证明答案NADP+辅因子完全等同。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_106：本案root为Geraniol，gold terminal主产物含Geranate|Myrcene；支持P106_1终点为Geranate的范围核对。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S1写NADP+/NADPH，S2写geranic acid而非Geranate；这些是已见的局部表示/辅因子差异。

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 按已认可主链P106_1的2个必答目标反应核对：S01答案geraniol dehydrogenase/EC 1.1.1.183落在accepted集合，且程序登记为CONFIRMED_TARGET/SUPPORTED；S02答案aldehyde dehydrogenase (NAD+)/EC 1.2.1.3亦在accepted集合，geranic acid与gold Geranate仅电荷/质子化表示差异（REPRESENTATION_EQ_CHARGE_BLIND），可判目标功能成立。两目标均有适用功能级支持，无已核KEY失败；但S02表示边界仍需规范化且key_definition_complete=false，阻止9–10；在&#91;7,8&#93;内取7，反映主对应可靠而局部表示/关键性登记边界尚需少量修订。

<details><summary>V0.4理由与本行变化背景</summary>

S1取EC 1.1.1.183 geraniol dehydrogenase，与gold S01备选酶BSY-e04182逐字对应；S2取EC 1.2.1.3，与gold S02 BSY-e00313对应；S4 EC 6.4.1.5 为geranoyl-CoA carboxylase特异号且与ATP依赖羧化反应类型相符；S3 EC 6.2.1.3 按AMP-forming酰基-CoA连接酶家族级指派，反应类型匹配但非该底物专属；S5 EC 4.2.1.57 与“isohexenylglutaconyl-CoA hydratase”的水合酶类属相符，但号-名对应未经冻结证据核验；S6仅给裂解酶名称、EC为null并如实标low。主要步骤酶-反应对应有可靠支持，个别条目待核，未出现EC大类与反应类型明显错配或名号互斥，属7–8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：S01 accepted集合包含geraniol dehydrogenase EC 1.1.1.183；S02 accepted集合包含geranial dehydrogenase EC 1.2.1.3；此为策展功能/G4支持，不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：S02 gold主产物为Geranate；答案geranic acid为同一羧酸的质子化表示候选，需按电荷表示边界处理。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S1明确给EC 1.1.1.183；S2明确给EC 1.2.1.3与geranic acid；未见已核催化矛盾。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案统一使用Castellaniella defragrans 65Phen。Gold organism_gold对S01–S04均给出C. defragrans EXACT、taxid 75697、genome GCA_014203015.1、pathway_complete TRUE，物种身份与整路能力主要匹配。未给TaxID、strain 65Phen未逐字在gold中核验，且S3–S6属额外步骤，故8而非9。

<details><summary>V0.4理由与本行变化背景</summary>

全链统一使用 Castellaniella defragrans 65Phen（单一profile，符合去重要求）。冻结gold中该物种（taxid 75697，GCA_014203015.1）在S01/S02/S03/S04各步均有EXACT匹配记录，并存在PATHWAY_COMPLETE=TRUE行，支持“该物种是本路线对应菌、具路径级能力”；答案未填ncbi_taxid，菌株号65Phen与gold物种级记录中的保藏号DSM 12142（该种模式株）相容，但以物种级记录支撑菌株级声称属粒度不足，且S3–S6（geranoyl-CoA下游）在gold中无步级归属记录，答案已自述低置信与归属不确定性。未见租借他菌株/他TaxID支持本菌株的身份错配，不构成关键错误；属“主要微生物对应有可靠支持、少量条目待确认”档，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：支持C. defragrans species EXACT、taxid 75697、pathway_complete TRUE；不支持逐字核验strain 65Phen或答案未给出的TaxID。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：答案给出C. defragrans 65Phen且所有步骤复用同一profile。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> F11 rod-shaped、F12 Gram-negative与trait_gold观察一致；F6 nitrate respiration得到observed reduction/respiration nitrate支持。F1/F7/F8/F9有文献/路线合理性但菌株级支持未在E0核验；F2/F5/F10/F14等可核项诚实null，完成度主归D1。提供性状部分准确、关键证据仍有缺口，落5–6档，取6因可核项和诚实null边界清楚。

<details><summary>V0.4理由与本行变化背景</summary>

7项有值性状中：F11 rod-shaped、F12 Gram-negative与gold对75697的OBSERVED记录一致；F6厌氧呼吸/硝酸盐末端受体与gold“respiration: nitrate=true/reduction: nitrate=true”观察相符；F1“兼性厌氧、可反硝化生长”与BacDive aerobe;anaerobe及硝酸盐呼吸观察大体相容（另有预测facultative anaerobe=false的多值冲突，属可用但需注明条件）；F7/F8（β-myrcene、geraniol等单萜利用）与F9（geraniol dehydrogenase活性作为菌株性状）分别仅有文献级与BRENDA酶条目级支撑，是把物种/酶条目级信息写成菌株级性状，属跨粒度外推；温度、pH、盐度、保藏号、运动性、基因组等关键性状全部null（gold有可查观测），关键项证据缺口明显。按已给内容与关键缺口定档，属“部分性状准确且适用、关键项证据不足”档，取6；缺失的完成度扣分主要归D1，不在此重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：支持C. defragrans taxid 75697的F6 nitrate respiration、F11 rod-shaped、F12 Gram-negative；F7/F9未给出答案所称geraniol dehydrogenase的菌株级条目。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_106：标识F1/F2/F5/F6/F7/F8/F9/F10/F11/F12/F14为observed_accuracy，F3/F4/F13/F15为completeness_only；用于区分准确性缺口与完成度。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：答案提供7项有值性状、8项explicit_unknown；可用于判断已给性状与null分布。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D5按来源可追溯性单独评价：答案对S1-S6的酶、菌和性状均挂了evidence_id，EVID_003–EVID_007给出BRENDA EC记录号，EVID_002给出可定位的PubMed书目，EVID_008给出BacDive菌株记录，因此不是MISSING_SOURCE或仅有笼统库名，可进入5–6档。但EVID_001仅为“MetaCyc pathway page”且无record_id，S4–S6的“proposed”下游段主要依赖该页面；EVID_004为通类醛脱氢酶记录；EVID_008无record_id；EVID_002虽与SUPP:PMID:8526489书目吻合，但补证摘要只到P. citronellolis与富集培养层面，未确认Castellaniella defragrans 65Phen及全部步骤/性状。上述为来源定位或支持范围待核，未见经冻结证据确认的CRITICAL/SYSTEMIC错引，故不cap；因多处关键映射仍不完整，取5–6档下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付了8条evidence_registry并逐步绑定：EVID_001为MetaCyc pathway page（record_id=null，仅页面名，属笼统）；EVID_002为完整书目文献（Harder &amp; Probian, AEM 61:3804-3808, 1995，可定位）；EVID_003–007以BRENDA EC号为record_id，属条目级可定位；EVID_008为BacDive菌株记录但无record_id（笼统）。决策相关组（CG01路线核心/CG02起点/CG03终点/CG05关键酶/CG07核心菌）并非全部笼统，存在条目级与完整书目记录，故落入5–6档；但核心路线序列与S6步骤只有路径页名支撑，且E0整题为EVIDENCE_GAP，所有引用内容与引用-声称链均无法核对，相关声称保持UNRESOLVED_SOURCE待核。无任何经核实的错引，不触发关键错误cap（同一单元不叠加cap）。取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / SUPP:PMID:8526489：确认Harder &amp; Probian 1995书目记录及给定摘要；摘要涉及P. citronellolis、富集培养、硝酸盐与单萜降解，但摘要层面未确认Castellaniella defragrans 65Phen，也未逐项确认答案全部酶/步骤/性状；不能据此判虚构或已核实错误。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：提供本题gold酶/EC参照行，可用于对照答案所引EC是否在已给参照范围内；不证明答案外部BRENDA条目本身存在或支持全部声称。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：提供Castellaniella defragrans 75697等gold生物参照行；不证明EVID_002/EVID_008的具体支持范围或菌株级能力。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：提供本题trait参照记录与粒度示例，用于判断D5性状来源映射是否可核；不把gold记录回填为答案原来源。
- SCOPE_ROW / SCOPE#BIOPATH150_106#CG14：本题底物利用声称的条件性criticality登记；用于D5判断相关性状声称是否承担目标污染物能力论证。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确列出uncertainties：氧条件未指定未写入route_scope、S4–S6归属不确定、S6 EC/下游未定；逐步confidence多为medium/low/unknown，多个trait null诚实。未见系统性把预测写成实证；仅个别高confidence对未核来源略强，故8而非9。

<details><summary>V0.4理由与本行变化背景</summary>

答案对证据性质与边界披露较具体：明确route_scope.oxygen_condition按题面留null而不套用文献反硝化条件；S2–S6逐步uncertainty说明同工酶/基因归属未定、裂解段为“拟议”且置信低；uncertainties列出三条（氧条件、下游步骤归属、7-methyl-3-oxooct-6-enoic acid去向与EC未定）；未知性状一律null+confidence=unknown，未把null包装成观测；来源类型显式标注DATABASE_DIRECT/LITERATURE_DIRECT。不足：F9把BRENDA EC条目级活性以DATABASE_DIRECT+medium呈现为菌株酶活，F7/F8以单篇文献medium呈现，未标明“数据库条目级推断/文献级推断”与菌株观测的差别，属单点过度确信而非系统性把预测写成实证；未声称实验验证，也未掩盖已知矛盾。属7–8档取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案披露了氧条件、S4–S6归属和S6 EC/下游不确定性。

</details>

## Qwen

答案SHA256：`a79bbcf5cbc1b28593b058b39b670e79487e351ee4f90f32741c754d93be446d`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分5 → V0.5新分8，变化+3。

新裁判理由：

> 按D-M01只评一条已认可主链；答案S1-S2构成Geraniol→Geranial→Geranic acid/Geranate的连续链，对应P106_1两步主链，未交付P106_2分支不按漏步扣分。chosen_route_name原样；两步均有底物/产物、酶+EC、微生物；15项性状字段齐全，未知为null。仅缺具体菌株/TaxID及显式选链说明，属少量修订/工程性缺口，落7-8档，取8。

<details><summary>V0.4理由与本行变化背景</summary>

六个登记模块均有涉及，但实质完成度不足：路径只交付1条支链2步（gold为4步分支DAG，ordered_step_count=4）；微生物仅到属级Pseudomonas sp.、无种/株/TaxID；15项性状仅3项有值（F7/F8/F9，且均为&#x27;可能…&#x27;式推断），其余12项显式null+unknown（属明确未知，不计为遗漏也不当作错误）；来源模块实质为空（唯一EVID_001自述INTERNAL_KNOWLEDGE_ONLY、未附外部文献）；不确定性说明给得具体。落在5–6档下沿（主要模块涉及但若干必要内容缺失或仅占位），取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_106：题面路线名β myrcene degradation、根物Geraniol、终端主产物Geranate|Myrcene的身份定位
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_106：全图为BRANCHED_DAG、ordered_step_count=4；仅说明全图材料数，不是要求全部旁支的缺步分母
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：P106_1的S01 Geraniol→Citral/geranial与S02 Citral/geranial→Geranate构成可评的两步主链；不表示P106_2分支必须交付

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> S1醇氧化Geraniol→Geranial，S2醛氧化Geranial→Geranic acid；NAD+/NADH、H+、H2O列明，方向为底物→产物，两步连续，主链终点与P106_1的Geranate一致。geranic acid与geranate为质子化表示差异，未造成主链化学断裂；程序已限D2九至十门不成立且D2允许上界为8，故取8。

<details><summary>V0.4理由与本行变化背景</summary>

两步化学成立：S1为伯醇→醛的NAD+依赖氧化（Geraniol C10H18O→Geranial C10H16O，NAD+→NADH+H+，氢计量闭合）；S2为醛→酸的NAD+依赖氧化并含水（Geranial+H2O→Geranic acid，NAD+→NADH+H+），方向、原子与辅因子均与gold S01/S02一致，中间体geranial=gold Citral、产物geranic acid=gold Geranate（中性酸vs阴离子写法差异不构成错误），步骤间连接连续。未违反起点错误、方向反转、跳步或不守恒。达到7–8档（主链及关键转化有依据），但不给更高：仅覆盖gold两支中的Geranate支、linalool/myrcene支未触及，且依据仅来自gold比对而非答案自证。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：S01与S02的方向、主底物/主产物、NAD+/NADH与H+、H2O辅因子记录；S02产物为Geranate，支持答案geranic acid的质子化等价表示判断
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_106：本题终端主产物包含Geranate；不表示必须交付Myrcene分支

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 仅评P106_1两步。S2 geranial dehydrogenase配EC 1.2.1.3与给定accepted名称-EC对一致，可支持目标反应；S1 geraniol dehydrogenase配EC 1.1.1.1在给定accepted集中未成对：geraniol dehydrogenase对应EC 1.1.1.183，EC 1.1.1.1对应alcohol dehydrogenase I/II/III，故S1名称-EC配对未核，记U而非F或S；EC 1.1.1.1本身仍在S01 accepted EC集合中，不判已证催化不相容。S=1、U=1、N=2，C=0.5，按C04落&#91;5,6&#93;；关键入口S1仍未核，不能进入7-8，取5。

<details><summary>V0.4理由与本行变化背景</summary>

两步各给一个酶与EC，反应类型与酶功能类别相匹配：S2的geranial dehydrogenase配EC 1.2.1.3与gold S02完全相同；S1的醇脱氢反应配EC 1.1.1.1，该号在gold S01候选集合内（alcohol dehydrogenase I/II/III），但gold主注为1.1.1.183/1.1.1.144/1.1.1.347，答案以&#x27;geraniol dehydrogenase&#x27;命名搭配广谱EC 1.1.1.1属名称-编号粒度不精确（非功能矛盾，亦非EC大类错配）。均无gene/protein标识、confidence=low、无外部支持。落5–6档（有合理候选与部分支持，关键步骤缺具体核验），因两步均与gold候选一致取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：S01列出geraniol dehydrogenase=EC 1.1.1.183及alcohol dehydrogenase I/II/III=EC 1.1.1.1；S02列出geranial dehydrogenase=EC 1.2.1.3。支持S2名称-EC配对，不支持S1把geraniol dehydrogenase与EC 1.1.1.1成对

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案仅给Pseudomonas sp.（无strain/TaxID），S01属级候选与gold中Pseudomonas spp.部分相符，S02在给定gold organism行中仅见Castellaniella；EVIDENCE_GAP无法判错，故取5–6档下沿5：合理候选和部分支持，但关键身份、菌株及步级能力未核。

<details><summary>V0.4理由与本行变化背景</summary>

两步均只给属级&#x27;Pseudomonas sp.&#x27;：无种名、无菌株、无TaxID、无保藏号，属身份粒度不足而非身份错配或编造（未填任何可核编号，符合题面&#x27;未知填null不得编造&#x27;）。属级选择本身有合理性：gold S01（geraniol dehydrogenase）步骤下确列Pseudomonas aeruginosa/citronellolis/mendocina；但S02步骤gold仅列Castellaniella defragrans与Penicillium digitatum，答案把S2也归Pseudomonas sp.缺乏步骤级能力证据。未声称整条路径能力（complete_pathway_organism_profile_id=null），无越级外推。落5–6档（有合理候选和部分支持，关键身份与作用范围未充分核验），取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：gold微生物行参考；不穷尽合理替代，也不证明答案菌株身份
- ANSWER_TEXT / BIOPATH150_106_ANSWER：答案微生物声称；未提供菌株/TaxID/外部来源

</details>

### D4 性状科学性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 15项性状槽均出现，但仅F7/F8/F9有低置信属级文本，其余12项明确null/unknown；已给文本为‘可能利用/具有潜力’等无外部来源的属级描述，无具体数值/条件，关键性状证据不足；未发现可核明显错误，按3–4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状中仅3项有值，且均为无量化内容的方向性推断：F7&#x27;可能利用香叶醇作为碳源/底物&#x27;、F8&#x27;具有香叶醇氧化降解潜力&#x27;、F9&#x27;geraniol dehydrogenase/geranial dehydrogenase活性&#x27;，无任何数值、单位、实验条件或菌株级对象，来源全部指向内部知识EVID_001、confidence=low，raw_text=null。对象仅到属级&#x27;Pseudomonas sp.&#x27;，性状适用性无法落到种/株。正面之处是均以&#x27;可能/潜力&#x27;措辞并标low，未把预测冒充观测；但就筛选用途而言，已给内容几乎不可核验、不可用于耐受/能力判断，落3–4档（多处关键项缺适用依据）上限4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：gold性状参考；答案Pseudomonas sp.无明确菌株匹配，不能回填缺失来源
- ANSWER_TEXT / BIOPATH150_106_ANSWER：答案性状实际填写情况；不证明其准确

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 唯一证据EVID_001的source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id为null，locator仅为一般知识自述，无外部可定位条目；所有实际科学声称按MISSING_SOURCE低档。没有已核错引，不cap；因有claim_scope映射但无外部可核来源，取1–2档上沿2。

<details><summary>V0.4理由与本行变化背景</summary>

唯一来源记录EVID_001的source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id=null、locator明写&#x27;未附外部文献记录&#x27;，按四.3属MISSING_SOURCE：完全无可定位条目级证据，落低分档（1–2）。答案对步骤、酶、微生物、F7–F9的引用都指向同一条内部知识，无任何跨组可核对映射，&#x27;几乎无法定位重要结论依据&#x27;成立。属缺失而非误导，按P34/GENERIC-MISSING语义不触发cap；答案如实自述&#x27;内部知识/未附文献&#x27;，不按虚构处理。取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_106_ANSWER：答案自述内部知识；不属于可定位外部来源
- SCOPE_ROW / SCOPE#BIOPATH150_106#CG14：题面条件登记；不提供来源真实性

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确标出低置信/unknown，披露氧条件未指定、菌株未确证、路线入口与下游证据不足；将中心代谢入口写作‘推测’，source_type自述INTERNAL_KNOWLEDGE_ONLY。未见系统性把预测写成实证，故7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体良好：route_scope.notes与route_summary明确声明&#x27;以香叶醇为接入中间体、保守推到geranic acid、更下游证据不足未展开&#x27;；uncertainties列出氧条件未指定、直接以香叶醇为入口的连续主链证据不足、下游CoA/β氧化与中心代谢入口未列；两步各有step.uncertainty，全部confidence为low/unknown，12项未知性状显式置null而非编造。未发现把预测写成实证或掩盖矛盾的系统性误导。扣分点：EVID_001整体以&#x27;一般微生物降解知识&#x27;支撑核心路径与酶/菌归属，而正文未在同一处把&#x27;该两步与酶-菌归属均未经外部核验&#x27;作为统一限制句标出（仅分散在step.uncertainty与locator），属局部过度确信；且属级性状未注明&#x27;属级推断、不适用于具体菌株&#x27;。落7–8档下沿，取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_106_ANSWER：答案不确定性披露；不证明科学结论正确
- QUESTION_TEXT / BIOPATH150_106：题面条件；答案正确保留null

</details>

## Grok

答案SHA256：`3e80179eff936ec1920eefabfa003706cb605db0b377a19926b55ebec01870d2`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按已认可主链 P106_1（Geraniol→geranial→geranate，2步）评：答案route_scope原样填写β myrcene degradation，steps S1–S2给出主底物/主产物/酶/微生物，同一菌去重为ORG_001，15项性状字段齐全（未知项填null），evidence_registry局部自洽。S2的EC为null且若干性状为未知，属完成度/信息不足扣减；未把未选的P106_2分支计为漏步，也无整模块缺失或格式性致命缺陷。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案交付的route_scope、两步主链、酶/微生物、15项性状字段与证据登记
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：支持P106_1主链为Geraniol→citral/geranial→geranate，且未选P106_2分支不构成本维漏步
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：支持S01/S02相应微生物为Castellaniella defragrans物种级记录；不证明65Phen菌株级身份
- QUESTION_TEXT / BIOPATH150_106：题面固定路线名、15项性状、同一菌去重、未知填null及JSON交付要求

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按P106_1评化学：S1为geraniol+NAD+→geranial+NADH+H+的醇氧化，S2为geranial+H2O+NAD+→geranic acid+NADH+H+的醛氧化；两步底物/产物连续，方向为降解性氧化，辅因子在列，终点geranate对应已认可终点。S2采用中性geranic acid而非gold的geranate电荷表示，route diagnosis标为REPRESENTATION_EQ_CHARGE_BLIND，属局部表示/电荷记法问题，不改主链化学结论；因本案D2 nine_ten_eligible=false，不进入9–10，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际给出的两步反应式、SMILES、NAD+/NADH/H+/H2O与geranial→geranic acid连续性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：支持S01 geraniol+NAD+→citral+NADH+H+及S02 citral+NAD++H2O→geranate+NADH+H+；支持S02电荷表示差异
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_106：支持root=Geraniol、terminal main products含Geranate，用于判断终点范围
- QUESTION_TEXT / BIOPATH150_106：题面指定物质Geraniol、路线β myrcene degradation与题目终点口径

</details>

### D3a 目标反应与酶对应：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按答案选定的P106_1主链评其两目标步（S01/S02），未把未选的P106_2分支S03/S04计为漏步。S01为MATCH/SUPPORTED，功能支持存在，显式EC 1.1.1.183与accepted set一致，gene geoA仅为MINOR归属U，故S01可S且为KEY_ENTRY。S02为UNKNOWN/REPRESENTATION_EQ_CHARGE_BLIND/UNRESOLVED，答案给geranial dehydrogenase但EC=null，target function按冻结事实未确认，不能S；有声称且未核实，故U，不判F。S=1,U=1,N=2，C=0.5进入C04 &#91;5,6&#93;；无已确认KEY F/M，不触发D-KEY4≤4，但KEY_TERMINAL U阻止7–8，S01支持清楚而半条主链关键末端仍待核，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际交付的S01/S02酶名、EC、gene_or_protein及对应微生物
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：支持S01接受geraniol dehydrogenase EC 1.1.1.183；S02接受geranial dehydrogenase名称及EC集，但不证明答案未填的EC或具体蛋白活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：支持S01/S02目标反应及方向；S02存在电荷/表示差异，不能据名称匹配直接升为S
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：支持S01/S02相应物种为Castellaniella defragrans；不证明65Phen菌株级功能实验

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案两步均绑定Castellaniella defragrans 65Phen；gold在S01/S02均支持C. defragrans物种行，物种身份可靠。但TaxID为null、65Phen菌株级记录未核验，且complete_pathway_organism_profile_id与F8广义降解能力把物种/路径级支持推到菌株级，未达充分可核。按身份阶梯：物种级真实记录支持菌株级声称，档内扣分、不cap，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：支持C. defragrans在S01/S02的物种级归属及TaxID 75697/GCA_014203015.1；不支持菌株65Phen的独立身份或全部F8能力。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：支持部分物种级性状；不证明菌株65Phen与所用实验条件完全一致。
- ANSWER_TEXT / ANSWER_BEGIN：答案明确给出C. defragrans 65Phen并赋complete_pathway_organism_profile_id；该路径能力仍需菌株/全路径证据。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项中8项有值、7项明确null；F6硝酸盐呼吸/反硝化、F11杆状、F12革兰氏阴性、F13不产芽孢有物种级gold支持。F1兼性厌氧与gold预测facultative anaerobe=false及BacDive混合记录不完全一致；F7/F8单萜利用、F9 GeoA/GeoB活性主要依赖内部知识；F2/F3/F4/F5/F10/F14/F15缺值。已给性状有可用骨架，但关键定量性状与部分适用性证据不足，落5-6档并取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：支持F6 nitrate reduction/respiration、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating等物种级记录；F1存在混合观察/预测，不直接支持“兼性厌氧”单一表述。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_106：标明F1/F6/F7/F8/F9/F11/F12/F13等可评分性；F2/F4等部分子字段待温度/盐度范围政策裁决。
- ANSWER_TEXT / ANSWER_BEGIN：答案实际填写8项、7项显式null；不把null当作观测错误，但也不能视为已核定量性状。

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的EVID_001-EVID_003均标为INTERNAL_KNOWLEDGE_ONLY；虽附作者/期刊/EC名，但没有DOI、数据库条目或冻结记录可定位，核心路线、酶-EC、菌株身份和性状结论与来源的关联很弱。未见可核实的VERIFIED_MIS_CITATION，故不cap；按六状态中MISSING_SOURCE/弱可定位来源落3-4档，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示三条证据均为INTERNAL_KNOWLEDGE_ONLY；不提供可定位的数据库记录或DOI。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：可支持物种级身份的部分事实，但不能回填为答案原交付来源。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_106：可支持部分性状事实，但不把答案的内部知识来源升级为可追溯来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案对未知处理较诚实：大量null、明确说明氧条件未指定、GeoB无EC、后段CoA/β-氧化不写入主链、菌株保藏号/TaxID/基因组未核验，并列出替代好氧Atu路线及范围边界。问题在于若干INTERNAL_KNOWLEDGE_ONLY被标为high/medium，且部分物种/菌株外推未完全限定，属局部过度确信而非系统性误导。按7-8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案对null、未核验项、替代路线和边界有明确披露；同时保留高置信内部知识标签。

</details>

## GPT5.6

答案SHA256：`206add4c62ebcc764dbfc1a2277630622469912e511d59a8e4303e990771d9e6`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按已认可主链P106_1（Geraniol→Citral→Geranate）看，答案S1/S2覆盖该两步入题主链且路线名原样填写；未选P106_2分支不按缺步扣分。但15项性状全部为null/unknown，属整块占位；S3未作为downstream/alternative分离且enzyme=null，菌株也未给出。主要模块有涉及但存在明显占位与关联缺口，落在5–6档下沿。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：显示P106_1的S01 Geraniol→Citral、S02 Citral→Geranate为一条两步已认可主链；答案S1/S2与该链对应，S3在Geranate终点之后。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_106：本题路线名为β myrcene degradation，gold终端主产物含Geranate|Myrcene；支持题面路线/终点上下文，不直接证明答案科学正确。
- ANSWER_TEXT / ANSWER.steps&#91;0:3&#93;;ANSWER.organism_profiles&#91;0&#93;.traits：答案给出3步、1个organism profile、15项性状全null/unknown，S3 enzyme为null；支持完整性/占位判断。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_106：gold性状表含多个gold菌的observed性状行；答案profile无任何observed性状值，支持性状模块为占位而非已交付实质内容。

</details>

### D2 反应化学科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按与答案S1/S2对应的P106_1评：S1 Geraniol→Geranial（醇氧化）与S2 Geranial→Geranic acid（醛氧化）方向、主要结构和步骤连接正确；S2酸式与gold geranate的质子化/盐形式差异可接受；NAD+/H+未列属局部计量缺陷，不达cap。S3位于Geranate终点之后，按P29不进入所评主链D2加分；其未分离为downstream且C10→C5计量不完整作为保留问题记录，不改变P106_1主链结论。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_106：gold S01/S02显示Geraniol→Citral→Geranate的方向与连接；答案S1/S2与之对应；S3不在P106_1两步主链内。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：S01 accepted酶集合含EC 1.1.1.1，S02含EC 1.2.1.3；支持功能级酶-EC合理性，不证明具体蛋白实验活性。
- ANSWER_TEXT / ANSWER.steps&#91;0:3&#93;.substrates/products/smiles：答案S1/S2转化和S3 C10酸→C5酸且未列伴生产物；支持D2化学与连续性判断。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_106：终端主产物含Geranate|Myrcene；支持将S3置于Geranate之后作为范围外/下游处理，不用于抬高D2。

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 7: The delivered geraniol-&gt;geranial-&gt;geranic acid branch uses S01 alcohol dehydrogenase EC 1.1.1.1 and S02 aldehyde dehydrogenase EC 1.2.1.3, which correspond to accepted S01/S02 enzyme/EC sets at function level. S3 has enzyme null and is outside this gold branch. 9–10 blocked: high_tier_eligible=false, E0 gap, KEY definition incomplete; only function-level G4, not specific protein/experimental.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_106：Accepted enzyme rows include EC 1.1.1.1 for S01 and EC 1.2.1.3 for S02 at function level; does not verify specific protein/experimental activity.
- ANSWER_TEXT / ANSWER.steps S1-S3：Answer supplies the two named enzyme/EC pairs and a null enzyme for S3.

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 5: P. putida is a plausible species-level candidate but no strain, TaxID, or reaction/whole-path capability evidence is delivered. Gold organism rows for S01/S02 list other Pseudomonas species; gold is non-exhaustive, so this is not a verified mismatch. Honest low confidence supports 5–6 lower end.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_106：Gold lists organisms for S01/S02, including P. aeruginosa, P. citronellolis, P. mendocina; P. putida not listed. Gold non-exhaustive, so no verified contradiction.
- ANSWER_TEXT / ANSWER.steps S1-S3 microorganism：Answer uses P. putida for all steps with no strain, TaxID, or cited capability evidence.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Per P44/C08, all 15 required traits are null/unknown; D4 is MISSING=1, not a scientific error.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：All 15 trait values are null/unknown with confidence unknown.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 2: All four evidence entries are INTERNAL_KNOWLEDGE_ONLY with no database, record_id, or locator. Decision-relevant claim groups therefore have MISSING_SOURCE; no external traceability. No verified mis-citation, so no cap. Some internal claim mapping supports 2 rather than 1.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Four entries all INTERNAL_KNOWLEDGE_ONLY, database/record/locator null.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 8: The answer consistently labels confidence low/unknown, lists specific uncertainties (strain, third-step enzyme/stoichiometry, oxygen), and uses nulls for unknown traits. It does not present predictions as observations. It does not discuss the omitted myrcene branch, so 8 not 9–10.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Uncertainties include strain, third step, oxygen; confidence low/unknown.

</details>
