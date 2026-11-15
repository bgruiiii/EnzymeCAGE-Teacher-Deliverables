# BIOPATH150_129：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：erythritol degradation II

污染物：Erythritol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 42.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 35 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 45 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 51.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 29.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 33.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`18851a0120a73f603c6087b2ca0c53ba5d3860791c30f4bbcbb7d6ad6230f684`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 答案输出结构完整：3步、1个organism_profile、15项性状、evidence_registry均在；route_scope原样填写。程序route_status=INCOMPLETE且3个gold必答步均MISSING/UNBOUND，说明指定主链覆盖不完整。按D1允许&#91;1,6&#93;，主要模块有涉及但必要主链内容缺失，取5。

<details><summary>V0.4理由与本行变化背景</summary>

题面固定路线名erythritol degradation II且要求原样填写、不得改选。答案原样填写路线名，但交付的化学主链是Brucella abortus的磷酸化优先ery路线（S1 erythritol+ATP→D-erythritol 4-phosphate；S2直接脱氢至D-erythrose 4-phosphate），缺少冻结gold路线II主链的关键中间体D-erythrulose与D-erythrulose 4-phosphate，属P100/TABLE5 D1行&#x27;自称合规却交付不同路线&#x27;的D1关键错误，cap≤4。其余交付（逐步酶/菌绑定、同一菌去重、15项性状外壳、来源登记、不确定性清单）齐备且格式正常；另F14基因组登录号在gold中对应GCA_000740135.1而答案填null，属个别完整性缺失。故cap档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_129：确认本题3个ordered steps、LINEAR_UNIQUE；不证明答案步骤与gold对应。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：给出gold目标反应顺序/结构；不支持答案的替代步。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案化学内部基本连贯（磷酸化、NAD+氧化、转酮醇反应），但主链与gold不同：S1用erythritol→erythritol 4-phosphate而非D-erythrulose→D-erythrulose 4-phosphate；S2用erythritol 4-phosphate→D-erythrose 4-phosphate而非erythritol→D-erythrulose；S3为转酮醇酶下游而非D-erythrulose-4-phosphate isomerase。D2允许&#91;1,4&#93;，多个重要步不符，取4；未见原子不守恒。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3内部化学连贯：磷酸化步列明ATP/ADP，氧化步列明NAD+/NADH，S3为真实转酮醇反应（EC 2.2.1.1），底物/产物SMILES与结构一致；起点erythritol与终点D-erythrose 4-phosphate均与gold一致。但相对题面指定路线II，关键中间体D-erythrulose与D-erythrulose 4-phosphate被替换，S2以一步脱氢直接生成D-erythrose 4-phosphate（答案自述文献另有erythrulose phosphate中间体版本），且全部依赖内部记忆、无独立依据；S3越出gold终点属下游延续（P29不加分不扣分）。故落5–6档（主干部分成立、关键中间体与转化需实质修订、合理性证据有限），取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：gold S01-S03底物/产物与方向；用于比较答案化学路径，不证明替代路线在别处无酶活。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_129：gold起点Erythritol与终点D-erythrose 4-phosphate；不扩展到下游中心代谢。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> gold accepted：S01 D-erythrulose kinase/EC 2.7.1.210；S02 erythritol/L-threitol dehydrogenase（1.1.1.12/56/9/M28/M29）；S03 D-erythrulose-4-phosphate isomerase/EC 5.3.1.34。答案S1 erythritol kinase、S2 erythritol-phosphate dehydrogenase、S3 transketolase/EC 2.2.1.1均不对应目标步；无目标催化信用。D3a=1。

<details><summary>V0.4理由与本行变化背景</summary>

三步骤均绑定可辨认的酶候选：S1 erythritol kinase（gene eryC，EC null）、S2 erythritol-phosphate dehydrogenase（eryB，EC null）、S3 transketolase（EC 2.2.1.1，与经典转酮醇反应一致）。关键前两步EC缺失（答案诚实填null）、基因名基于记忆未核，E0亦无EC记录（GAP-129-004/010）；该酶集合并非gold路线II参照酶（1.1.1.x/2.7.1.210/5.3.1.34）。无已核实错引（错引归D5，不作D3a关键错误依据）。落5–6档，取5（多个关键步骤缺具体核验）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_129：列出S01-S03 accepted酶/EC；不支持答案的erythritol kinase、erythritol-phosphate dehydrogenase或transketolase作为目标步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：列出目标反应底物/产物；用于判定酶-反应不对应，不证明替代酶在别处无活性。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> B. abortus物种/TaxID 235在gold S03出现，但答案把strain 2308用于全部步骤并设complete_pathway_organism_profile_id=ORG_001；gold PATHWAY_COMPLETE为M. smegmatis 1772，且E0无B. abortus 2308全路径或S1/S2步级能力记录。部分身份/候选合理但关键范围未核，取5。

<details><summary>V0.4理由与本行变化背景</summary>

推荐菌为Brucella abortus 2308（TaxID 235，ORG_001），菌名/菌株/TaxID三件套自洽，且与冻结gold中S03候选菌Brucella abortus同物种一致，未见跨属或无关类群错配。整条路径能力声称（complete_pathway_organism_profile_id=ORG_001）与步级归属均以ery操纵子记忆为依据，E0无该TaxID记录（GAP-129-021/024），不能判定正确或错误；能力声称的粒度（菌株级）与可用来源粒度（内部记忆）不匹配，属档内扣分而非已核实关键错误。落5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_129：B. abortus 235仅列于S03；PATHWAY_COMPLETE为M. smegmatis 1772；不支持B. abortus 2308全路径声明。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 15项性状均出现；B. abortus 235在trait_gold中F1–F13、F15多为UNKNOWN，仅F14有genome/TaxID记录，答案F14却留null。所填温度、革兰氏、运动性、产孢、栖息地等一般描述plausible，但缺可见冻结观测支持；部分可用、关键证据不足，取6。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现（12填值、3明确未知、0遗漏），对象均为B. abortus 2308。已填值多为标准微生物学事实（最适约37°C、好氧、革兰氏阴性球杆菌、无鞭毛、不产芽孢、胞内寄生、可代谢赤藓糖醇），与身份相符；但raw_text全为null、来源仅内部记忆，氧需求/温度/保藏号等关键项未核（GAP-129-047/049）；F7&#x27;可利用葡萄糖&#x27;属物种级常识向菌株外推，F5 ATCC 23448自标低置信；F14 genome可为gold所载GCA_000740135.1却填null（完整性缺口按P112主归D1）。落5–6档（部分性状准确且适用、关键项证据不足），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_129：B. abortus 235多数性状为UNKNOWN，仅F14 genome/TaxID有观测；不支持答案多数性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_129：B. abortus多数性状为completeness_only，仅F14 observed_accuracy；用于D4可评分范围。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_129：B. abortus子字段无观测，F2 minimum等待裁决；不支持具体数值核验。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry 4条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null；路线、酶、菌、性状均无外部可定位来源。E0亦为EVIDENCE_GAP。D5来源状态为MISSING_SOURCE，低档取2；无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 4条全部为INTERNAL_KNOWLEDGE_ONLY（database/record_id/locator均为null），按P34记MISSING_SOURCE；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）全部缺可定位来源，符合P41&#x27;全部缺失→低分档（默认不cap）&#x27;。无任何已核实错引，故不登记VERIFIED_MIS_CITATION_*，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION；答案诚实标注内部知识并给出claim_scope映射（故取2而非1，但不构成可追溯性证据）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_129：参考目标酶记录，不是答案交付来源；不能弥补答案缺外部来源。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_129：参考目标微生物记录，不是答案交付来源。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_129：参考目标性状记录，不是答案交付来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案明确声明全部证据为内部知识、列出多条不确定性，并对EC/基因组/pH/盐度等未知填null；但多项性状仍标high confidence且无来源。整体披露较诚实，单点/局部过度确信，取7；非系统性误导。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量高：每步有uncertainty，全局uncertainties具体列出S2中间体歧义、S3通路边界、ATCC记忆值、基因组三项null，并明确声明&#x27;所有证据均为内部知识、未经数据库或文献原文核验&#x27;，未知与冲突未被掩盖。但F1/F6/F10/F11/F12/F13以high置信包装未核实记忆值，与依据强度不完全相称，属单点/局部过度确信（非系统性误导，不cap），档内扣分。落7–8档，取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_129：B. abortus多数性状UNKNOWN，说明答案高置信性状缺冻结观测；用于评估置信披露。

</details>

## DeepSeek

答案SHA256：`27086a3ccdc348e5848d2c549d4c3baa5db8c28e43dbf8041658a480338d11b2`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> JSON完整，3步、1个菌、15项性状齐全；但题面锁定route_scope=erythritol degradation II，答案实际给出PTS/erythritol-1-phosphate路线，未按gold的S02→S01→S03主链交付。D1任务符合度关键错误成立，按≤4取4：内容完整但指定路线实质偏离。

<details><summary>V0.4理由与本行变化背景</summary>

形式完整性高：3步均含底物/产物/酶/微生物、SMILES齐全，15项性状齐备、证据登记与route_summary俱全；但交付的化学路线与题面指定的&#x27;erythritol degradation II&#x27;不符——gold该路线首步为NAD+依赖氧化生成D-赤藓酮糖，答案改为PTS磷酸化(赤藓糖醇1-磷酸/赤藓酮糖1-磷酸中间体)，属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离，按八.D1/D2边界与&#91;P100&#93;构成D1关键错误(cap≤4)。形态完整、模块无缺故档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：证明题面锁定 erythritol degradation II，指定路线不得改选。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：证明gold主链为 erythritol→D-erythrulose→D-erythrulose 4-phosphate→D-erythrose 4-phosphate；不证明替代路线化学必然错误。
- ANSWER_TEXT / ANSWER：证明答案交付的是 erythritol 1-phosphate/D-erythrulose 1-phosphate 的PTS路线。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分3 → V0.5新分5，变化+2。

新裁判理由：

> 起点 erythritol 与终点 D-erythrose 4-phosphate 名称对应；S1 PTS磷酸化和S2 NAD+氧化在自身路线内可成立。但S3把 D-erythrulose 1-phosphate 经 EC 5.1.3.38 转为 D-erythrose 4-phosphate，route diagnosis对S03标NONMATCH/STEREO_CONFLICT_SPECIFIED；显式立体/结构冲突使D2不能高，主干部分成立但关键终端转化需修订，取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学存在实质错误：S1(磷酸化)、S2(氧化)反应本身可成，但把磷酸基放在C1(erythritol 1-phosphate、D-erythrulose 1-phosphate)；S3写为D-erythrulose 1-phosphate→D-erythrose 4-phosphate并由差向异构酶(EC 5.1.3.38)催化——按答案自带SMILES，底物磷酸在C1、产物磷酸在C4，差向异构化不能迁移磷酸基团，该步违反基本化学约束，非可信路径。与指定路线中间体(4-磷酸)不符，且无替代声明/可核证据。属多个重要步骤与基本化学约束问题，落3-4档，取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：证明目标终端步的底物/产物与立体化学参照；不证明答案所有局部步骤均错误。
- ANSWER_TEXT / ANSWER：证明答案S3使用 D-erythrulose 1-phosphate 与 EC 5.1.3.38。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 逐目标统计为S=0、F=1、U=2：S03为预定义KEY terminal，route diagnosis给NONMATCH/STEREO_CONFLICT_SPECIFIED并登记confirmed target failure；S01/S02为MAJOR KEY但alignment未确认/目标反应未交付。目标反应没有一条S，且至少一个KEY已确认失败，适用D-KEY4上界&#91;1,4&#93;；取1，因几乎无可用目标催化对应，核心主推荐不可用。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶均为可辨识的功能候选(PTS permease/erythritol 1-phosphate dehydrogenase/D-erythrulose 1-phosphate 4-epimerase)，S1、S2诚实留空EC；但2/3关键步骤缺EC或蛋白/基因标识，S3的EC 5.1.3.38在冻结证据中无记录无法核对accepted name/reaction。整体属&#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;的5-6档，取5；不构成D3a关键错误（酶名与EC类别未见经核实的矛盾）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_129：证明目标步 accepted酶/EC 集合；不扩展到具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：证明目标底物/产物方向与S03终端步。
- ANSWER_TEXT / ANSWER：证明答案交付的酶/EC与目标步不匹配，S01/S02目标反应未交付。

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 答案把S1-S3全部归给 Bacillus subtilis 168（TaxID 224308），并声称complete_pathway_organism_profile_id=ORG_001。gold organism行显示S01/S02为 Mycolicibacterium smegmatis，S03为 Brucella/Agrobacterium/Pectobacterium/Mycolicibacterium等；答案的菌株身份、单步催化归属和整路能力仅由INTERNAL_KNOWLEDGE_ONLY支撑。因身份与作用范围未核验且与gold organism不匹配，D3b取3；未把未核验直接判为已证伪。

<details><summary>V0.4理由与本行变化背景</summary>

Bacillus subtilis 168(全步同株、已按物种+菌株去重)是真实可辨识物种/菌株，身份合理；但与gold该路线菌(Mycolicibacterium smegmatis / Brucella abortus / Agrobacterium radiobacter / Pectobacterium atrosepticum)不同（不同不自动判错）。问题在于把整条路径能力(complete_pathway_organism_profile_id=ORG_001)归于该菌而仅有INTERNAL_KNOWLEDGE_ONLY、无反应级/全路径能力证据，TaxID 224308亦无冻结记录。属&#x27;有合理候选和部分支持，关键身份与作用范围未充分核验&#x27;，取5；未见经核实的身份编造或跨类群错配，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_129：证明gold给出的步骤菌与完整路径菌；不证明其他菌绝对无该能力。
- ANSWER_TEXT / ANSWER：证明答案全部使用 Bacillus subtilis 168 并声称整路能力。

</details>

### D4 性状科学性：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案给出15项性状（13项填写，F3 pH与F4盐度以全null对象作为explicit unknown），但全部性状对象为 Bacillus subtilis 168，而本题gold trait行覆盖 M. smegmatis/Brucella/Agrobacterium/Pectobacterium，E0切片无 B. subtilis 性状记录。关键温度、保藏号、基因组数值及多项定性性状无法核验，且对指定route organism的适用性未建立；只能给部分内容档，取4。

<details><summary>V0.4理由与本行变化背景</summary>

性状均针对所述菌B. subtilis 168，多数与公认特征一致(F1兼性厌氧、F10周生鞭毛运动、F11杆状、F12革兰阳性、F13产芽孢、F14基因组约4.2Mb/43.5%GC/NC_000964.3、F2嗜温15/37/45)，pH与盐度诚实填null/unknown(明确未知≠错误)。但F7(利用erythritol)、F8(降解赤藓糖醇)、F9(列路径酶为菌酶活)、F5(BGSC 1A1)等关键项仅有内部知识、无E0记录，部分转录自路径本身略显循环。属&#x27;部分性状准确且适用、关键项证据不足&#x27;的5-6档，取6；未见离谱数值或把预测冒充观测，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_129：证明gold性状记录覆盖的菌株与字段；不覆盖 B. subtilis 168。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_129：证明哪些trait/subfield可作观测准确度；不证明 B. subtilis 性状值正确。
- ANSWER_TEXT / ANSWER：证明答案交付的15项性状与B. subtilis 168身份绑定。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> evidence_registry三条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null；路线、酶、菌、性状和基因组声称均无法追到可定位文献/数据库条目。E0本身为EVIDENCE_GAP，决策相关组只能登记MISSING_SOURCE；无已核实错引，不触发D5 cap，但来源可追溯性低档，取1。

<details><summary>V0.4理由与本行变化背景</summary>

全部结论(路线、酶、菌、性状、基因组、保藏号)仅指向三条evidence_registry条目，source_type均为INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator全null，无DOI/数据库条目/计算记录可定位→按六状态归MISSING_SOURCE，D5取低分档(2)，MISSING默认不cap。E0为EVIDENCE_GAP，无已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION；EC/TaxID仅属UNRESOLVED待核，不判虚构。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明答案只给内部知识标签，无外部定位。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案列出部分不确定性（PTS亚基、EC未定、部分性状缺直接文献），但又在B. subtilis身份、整路能力及多项性状上给high/medium置信，而支撑仅为INTERNAL_KNOWLEDGE_ONLY；限制说明笼统，关键结论强度超过证据。未达到系统性把预测写成实证观测的cap程度，取5。

<details><summary>V0.4理由与本行变化背景</summary>

有正面披露：pH/盐度诚实填unknown/null，逐字段置信度标签，uncertainties列出PTS酶EC未定与部分性状缺直接文献，source_type如实标INTERNAL_KNOWLEDGE_ONLY。但存在过度确信：多处以high包装内部知识(F1/F10-F13及菌身份)，且化学上存疑的S3(磷酸迁移)uncertainty=null、零披露；整体属&#x27;有不确定性说明但部分结论强度超过依据&#x27;的5-6档，取5；非系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明答案有部分不确定性披露，同时多处高置信仅由内部知识支撑。

</details>

## Kimi

答案SHA256：`f4c7e0a137b210589ca0d62aa015b21d2121cff817169e6c4e5ecd7eff0ce9a1`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 题面路线名原样保留，steps/organism_profiles/15项性状均交付；但答案主链未到达gold终点D-erythrose 4-phosphate，且以D-erythrulose 1-phosphate插入步替代gold S01，属必要内容遗漏/关联不清。D1按5–6档取5；route representation仍处BOUNDARY_REVIEW，故只评可判的交付完整性，不把路线化学错误重复计入D1关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

三个主链步骤齐全（每步底物/产物含英文名与SMILES、一个首选酶、一个对应微生物），单一去重profile ORG_001被三步引用，15项性状全部出现（12项填写+3项明确未知F4/F5/F14），证据登记与不确定性说明均已交付，路线名逐字填写正确。扣分点：S2/S3的EC空缺（题面允许null，但属字段不完整）；主链止于D-erythrulose 4-phosphate，未走完gold所示第三步异构化。属7–8档（大部分必要内容完整，仅少量遗漏），取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_129：gold formal case is LINEAR_UNIQUE with ordered_step_count=3; does not by itself prove answer route chemistry.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_129：gold terminal is D-erythrose 4-phosphate; supports missing-terminal completeness finding.
- ANSWER_TEXT / ANSWER.steps&#91;S1-S3&#93;：answer delivers three steps, enzyme fields and one organism profile; does not establish scientific correctness.

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> D2按化学主链评：S1的Erythritol→D-erythrulose与参考链S02一致；但S2把D-erythrulose磷酸化为1-磷酸，任务参考链S01为4-磷酸，关键中间体位置错；S3以NAD+依赖脱氢把1-磷酸转成4-磷酸，实质上是磷酸位置移动，无相应氧化还原，化学不成立，且未完成S03的D-erythrulose 4-phosphate→D-erythrose 4-phosphate终端异构化。仅首步正确，后两重要步错误，落入3–4档；因含基本化学约束违背和终端缺失，取低端3。

<details><summary>V0.4理由与本行变化背景</summary>

S1（Erythritol+NAD+→D-erythrulose+NADH，SMILES与gold canonical一致）与gold S02一致，方向与原子计量成立；S2激酶反应类型合理，但产物写为D-erythrulose 1-phosphate，gold S01产物为D-erythrulose 4-phosphate（磷酸位点差异，E0无官方记录无法裁决）；S3以NAD+依赖&#x27;脱氢酶&#x27;把1-磷酸转为4-磷酸，底物与产物氧化态相同（净NAD+→NADH在化学上无对应氧化），磷酸基迁移机制未说明，答案自身也标注NAD(H)净变化不确定；且缺gold S03异构酶步（→D-erythrose 4-phosphate）。主干部分成立、关键中间体与连接需实质修订、合理性证据有限→5–6档取5；因偏离已在uncertainty中声明、首步正确，不按关键错误cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：支持gold参考链：S02 Erythritol→D-erythrulose；S01 D-erythrulose→D-erythrulose 4-phosphate；S03 D-erythrulose 4-phosphate→D-erythrose 4-phosphate。不支持答案中的D-erythrulose 1-phosphate中间体。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_129：本题终端主产物为D-erythrose 4-phosphate(2-)，不是答案下游的DHAP/甲醛裂解产物。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> D3a只评目标反应的酶对应。按gold，S02应为Erythritol→D-erythrulose（erythritol/L-threitol dehydrogenase，accepted EC集合不含答案S1的1.1.1.162）；S01应为D-erythrulose→D-erythrulose 4-phosphate（D-erythrulose kinase，答案S2酶名相符但EC为空、产物写为1-phosphate而非gold 4-phosphate）；S03应为D-erythrulose 4-phosphate→D-erythrose 4-phosphate（D-erythrulose 4-phosphate isomerase 5.3.1.34），答案S3却给1-phosphate dehydrogenase生成4-phosphate，未交付gold终末异构化。故仅少数目标有局部可用信息，主要对应未成立或仍待核，落入低档取3；未见已核关键错误证明，不触发D-KEY4上界。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名erythritol dehydrogenase与醇脱氢反应类型匹配，但EC 1.1.1.162不在gold该步多注集合(1.1.1.56/1.1.1.9/1.1.1.12/1.1.1.M28/1.1.1.M29)之内；按四.5保守条款须先核官方accepted name/reaction，E0无EC记录→UNRESOLVED待核，不判错。S2 &#x27;D-erythrulose kinase&#x27;与gold酶名一致，EC留null属诚实未知。S3标为脱氢酶，而gold对应末步为异构酶EC 5.3.1.34，且该步EC亦null、基因归属eryB仅有操纵子注释支持。合理候选+部分支持、若干关键步骤缺具体核验→5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_129：本题gold各步accepted酶名/EC：S01 D-erythrulose kinase 2.7.1.210；S02 erythritol/L-threitol dehydrogenase（1.1.1.12|1.1.1.56|1.1.1.9|1.1.1.M28|1.1.1.M29）；S03 D-erythrulose 4-phosphate isomerase 5.3.1.34；不证明具体蛋白实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：gold反应顺序与主产物：S02 Erythritol→D-erythrulose；S01 D-erythrulose→D-erythrulose 4-phosphate；S03 D-erythrulose 4-phosphate→D-erythrose 4-phosphate
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_129：路线名erythritol degradation II及gold终末主产物D-erythrose 4-phosphate
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_129：本题gold为LINEAR_UNIQUE、3个必答有序步

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Brucella abortus名称真实且gold S03包含Brucella abortus，但答案把它用于全部步骤；gold S02/S01步级微生物为Mycolicibacterium smegmatis；答案TaxID 359与gold Brucella abortus TaxID 235不一致；complete_pathway声称与gold PATHWAY_COMPLETE M. smegmatis 1772不一致。有部分身份/能力支持，但多个步级归属与身份范围未核清，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

全链统一推荐Brucella abortus（物种级，strain=null，ncbi_taxid=359），并以complete_pathway_organism_profile_id=ORG_001声称整条路径能力。gold步级菌为Mycolicibacterium smegmatis(S01/S02)与Brucella abortus/Agrobacterium radiobacter/Pectobacterium atrosepticum/M. smegmatis(S03)——Brucella在gold末步出现，说明物种选择有基线依据，不因与gold步级归属不同即判错；但（i）TaxID 359与gold organism_gold登记的Brucella abortus TaxID 235不一致，E0无官方Taxonomy记录→身份要素UNRESOLVED；（ii）整条路径能力仅有1975年文献的自由文本引用，无反应级/全路径级可核证据；（iii）strain为null，粒度仅到物种。属5–6档（合理候选+部分支持、关键身份与作用范围未充分核验），取5；无已核实身份错配，故不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_129：gold step organisms: S02/S01 Mycolicibacterium smegmatis; S03 includes Brucella abortus taxid 235; PATHWAY_COMPLETE is M. smegmatis 1772. Does not exhaustively exclude other organisms.
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_129：species-name crosswalk materials; does not verify answer TaxID 359.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Brucella abortus的gold性状大多为UNKNOWN，仅F14有genome GCA_000740135.1与TaxID 235。答案给出15项，但多数依赖EVID_005 INTERNAL_KNOWLEDGE_ONLY；温度/pH数值和optimum无独立观测支持；F14基因组信息填null而gold有genome accession。数值总体可信但关键证据不足，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

性状针对Brucella abortus物种级填写：温度20/37/40°C、pH 6.6–7.4、革兰氏阴性、不运动、球杆菌、不产孢、兼性胞内寄生、赤藓糖醇为优选碳源等，与通行物种描述方向一致且与所推荐菌自洽；盐度/保藏号/基因组三项诚实null（明确未知，不等同错误）；温度记录未误写为耐受极限。扣分点：全部非null性状唯一来源为EVID_005=INTERNAL_KNOWLEDGE_ONLY，无raw_text、无定位；gold trait_gold中Brucella abortus除TaxID/Genome ID外全为UNKNOWN，E0无性状记录可核。部分性状准确且适用、关键项证据不足→5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_129：Brucella abortus trait rows are mostly UNKNOWN; F14 has Genome ID GCA_000740135.1 and TaxID 235. Does not support answer&#x27;s temperature/pH/oxygen values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_129：trait scoreability mask; Brucella abortus most traits completeness_only / no observed source.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 核心路线/酶/菌声称有具体文献或数据库ID（EVID_002/003/004/006），但E0 EVIDENCE_GAP无法核验引用，记UNRESOLVED_SOURCE；EVID_001为MetaCyc笼统页；大量性状仅EVID_005 INTERNAL_KNOWLEDGE_ONLY，记MISSING_SOURCE。无已核实错引，核心部分可定位、其他模块缺映射，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组(CG01/02/03/05/07/08)均给出条目级引用（EVID_002具体文献、EVID_003记录号1.1.1.162、EVID_006记录号359），但统一冻结证据快照E0为EVIDENCE_GAP（entries=0，整题GAP-129-CASE），全部只能登记UNRESOLVED_SOURCE，不判虚构、不计已核实关键错误；性状组(CG10–CG13)唯一来源EVID_005=INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE；EVID_001仅&#x27;MetaCyc pathway page&#x27;无record_id→GENERIC_SOURCE。存在条目级可定位结论但无已核实错引，按四.3合成规则落5–6档（部分关键结论可定位待核、性状模块缺可核对映射），取5；同一单元不设cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;EVID_001-EVID_006&#93;：answer supplies locators/claims; this does not verify citation existence or support.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_129：gold trait rows show most Brucella abortus traits are UNKNOWN; supports the D5 finding that much trait sourcing is missing.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案明确列出路线I/II命名不确定、S2/S3 EC未确认、Brucella菌株/保藏/基因组null、下游裂解是否属主链不确定、TaxID凭记忆填写；confidence多为low/medium并使用null。个别高置信字段（S1酶、F9、F12）强于已核依据，但不是系统性把预测写成实证。7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且成体系：uncertainties逐条列出5项（MetaCyc I/II命名归属存疑、S2/S3 EC未确认、所用菌株号未知、裂解步未鉴定故未入主链、TaxID凭记忆），S2/S3各有uncertainty字段，EVID_005明确标注为INTERNAL_KNOWLEDGE_ONLY&#x27;无逐字原文&#x27;，F4/F5/F14诚实null，alternative_branches显式标注is_part_of_scored_main_route=false。扣分点：S1 EC 1.1.1.162标high、F12革兰氏阴性标high却仅凭内部知识，属单点过度确信（非系统性误导、无掩盖矛盾），按八.D6严重度条款档内扣分。属7–8档（大部分观测/预测/未知被正确标注、主要限制已说明），取下沿7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties&#91;0-4&#93;：answer&#x27;s own uncertainty declarations and null usage; supports D6 disclosure quality, not scientific correctness.

</details>

## Qwen

答案SHA256：`74a429c6d1a6e685ffb59d4af1ff6978c3b36b4a7d44f74e4b9279b1c7070db8`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 答案具备完整JSON骨架、3个步骤及15项性状字段，但未按题面锁定的 erythritol degradation II 主链交付：gold路线为 erythritol→D-erythrulose→D-erythrulose 4-phosphate→D-erythrose 4-phosphate，答案却给出 phosphorylation-first 的 erythritol→L-erythritol 4-phosphate→L-erythrulose 4-phosphate→D-erythrose 4-phosphate。该差异不是局部化学瑕疵，而是任务指定路线/主链符合度失败，属D1关键错误；其余字段完整不能抵消该任务偏离。

<details><summary>V0.4理由与本行变化背景</summary>

题目要求给出“指定路线”下的主链并明确“不得改选其他路线”。答案虽把 route_scope.chosen_route_name 回填为 erythritol degradation II，但 S1 以 erythritol kinase 先将 erythritol 磷酸化，与 gold 该路线首步脱氢（erythritol→D-erythrulose）不同，整条主链实为另一条磷酸化优先的赤藓糖醇路线；模块（3 步＋酶＋菌＋15 性状＋证据＋不确定性）虽齐全，但任务参数偏离成立，属 D1 关键错误，cap≤4，取 3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_129：题面锁定 route_scope.chosen_route_name=erythritol degradation II，不得改选其他路线。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：gold路线II的有向主链：S02 erythritol→D-erythrulose；S01 D-erythrulose→D-erythrulose 4-phosphate；S03 D-erythrulose 4-phosphate→D-erythrose 4-phosphate。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际交付的S1-S3底物/产物/E.C.仅为该答案自身内容，用于定位路线偏离。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分3 → V0.5新分8，变化+5。

新裁判理由：

> 按D2对所答化学独立评价：答案内部S1磷酸化、S2 NAD+依赖氧化、S3异构化至D-erythrose 4-phosphate，步骤连接连续，主有机物转化方向为降解至终点，未发现方向反转、原子明显不守恒或一步跳中心代谢物。局部问题包括S1/S2未列H+、立体化学/命名细节有不确定性，属7–8档局部计量与表达瑕疵，不构成关键错误；路线选择本身不在此维回填目标完成。

<details><summary>V0.4理由与本行变化背景</summary>

答案各步原子数可配平、终点同为 D-erythrose 4-phosphate，但主链首步被替换：S1 磷酸化取代 gold 的脱氢，中间体（erythritol 4-phosphate、L-erythrulose 4-phosphate）与指定路线的（D-erythrulose、D-erythrulose 4-phosphate）不同；S3 又把 L-erythrulose 4-phosphate 直接异构为 D-erythrose 4-phosphate，L/D 立体标注自相矛盾且无说明。属未声明地严重偏离指定路线的化学转化序列，D2 关键错误 cap≤4，取 3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案自身S1-S3的底物/产物/辅因子与连接关系，用于化学连续性和计量评价。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_129：仅用于确认本题终点化合物为D-erythrose 4-phosphate；不用于路线选择完成度加分。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 按目标反应逐项看：gold必答S01、S02的目标反应在答案中未交付，答案给出的是不同底物的磷酸化/脱氢步骤；S03虽有对应终产物D-erythrose 4-phosphate，但底物/EC/名称配对（L-erythrulose 4-phosphate isomerase EC 5.3.1.28 对 accepted D-erythrulose 4-phosphate isomerase EC 5.3.1.34）仍属表示/配对未决，不能记为已支持。当前无任一目标反应获确认S，两个必答目标缺失，D3a主推荐不可用，落在1–2档低端；不将未决S03当作已核成功抬高分数。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名与反应类型自洽（kinase→2.7.1、dehydrogenase→1.1.1、isomerase→5.3.1），未见 EC 大类与反应类型矛盾；但全部 EC/基因（2.7.1.215/1.1.1.316/5.3.1.28、eryA/B/C）在 E0R11 均无记录可核（GAP），且酶组对应的是另一路线（见 D1/D2）。有合理候选、部分支持，但关键步骤缺具体核验，5–6 档取 5，不 cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_129：gold路线II各必答步的accepted酶名/EC：S01 2.7.1.210；S02 accepted集；S03 5.3.1.34；仅支持数据库策展粒度。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：gold必答目标反应及其主底物/主产物，用于判断答案是否交付对应目标反应。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际给出的目标酶/中间体内容；仅用于与目标反应对齐，不证明具体蛋白活性。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 5–6档：给出真实物种/真实菌株名（Agrobacterium tumefaciens C58，ncbi_taxid诚实留null），属合理候选；物种名身份可由crosswalk部分支持（A. tumefaciens→358，仅物种名映射），但步级催化与整条路径能力（complete_pathway_organism_profile_id=ORG_001）只有路线级EVID_001，无该菌株反应级/全路径证据。gold各步菌为Mycolicibacterium smegmatis（S03另列Brucella abortus/Agrobacterium radiobacter/Pectobacterium atrosepticum），与所答不同但不据此自动判错。取5分：身份合理、关键作用范围未充分核验。

<details><summary>V0.4理由与本行变化背景</summary>

全链统一使用 Agrobacterium tumefaciens C58（物种名在 crosswalk 中真实存在，但 ncbi_taxid 未给），C58 是否为三步提供这些酶、能否完成整条路径均无 E0 记录可核（GAP）；gold 步级菌为 M. smegmatis / A. radiobacter 等，但 gold 非穷尽、同物种代表记录口径不因菌株不同自动判错。无已核实身份错配或“单步冒充全路径”的证据，故不 cap；5–6 档取 5，身份与能力待核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_129：给出各步已知菌（M. smegmatis为主，S03另有多菌）与PATHWAY_COMPLETE行；不支持A. tumefaciens C58的步级或全路径能力，也不能据此判其必错
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_129：仅支持物种名Agrobacterium tumefaciens→358身份映射；不支持菌株C58、TaxID或任何催化能力

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 5–6档：15项全数返回，10项有内容、5项（F2/F3/F4/F5/F14）诚实null，未编造数值；有内容的主要是定性性状（F1/F6/F10–F13/F15），来源仅EVID_002=INTERNAL_KNOWLEDGE_ONLY且标low，属诚实标注但非已核支持；F7/F8/F9把路线声称（可利用/降解赤藓糖醇、三步酶活）当作性状，缺独立性状证据。gold性状记录只覆盖M. smegmatis/B. abortus/A. radiobacter/P. atrosepticum，不含C58，无法核实其准确性，按P46以合理性+支持程度评5分。

<details><summary>V0.4理由与本行变化背景</summary>

15 项齐全（10 filled / 5 explicit_unknown / 0 omitted），数值型性状诚实填 null；定性性状（aerobic、革兰氏阴性、杆状、运动、不产孢、生境较广）属属级常识，来自 INTERNAL_KNOWLEDGE_ONLY（low）；关键碳源/降解/酶活性状绑定不可核的路线来源。部分性状适用、关键项证据不足，5–6 档取 5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_129：提供1772/235/362/29471的性状参照；不覆盖Agrobacterium tumefaciens C58，不能用于核实答案性状
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_129：标明各物种性状可评分性/完整性角色；不含C58行，不改变答案性状待核状态

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分3 → V0.5新分5，变化+2。

新裁判理由：

> 决策相关组（CORE：CG01/02/03/05/07/09；APPLICATION_CRITICAL：CG08）均只由一条路线级DATABASE_DIRECT条目EVID_001（MetaCyc ERYTHRITOL-DEG-2 + locator）支撑：条目级可定位，但E0为EVIDENCE_GAP无法核对内容是否支持所答步骤/菌，登记UNRESOLVED_SOURCE；性状组（CG10–CG15）仅INTERNAL_KNOWLEDGE_ONLY或null→MISSING_SOURCE。按P41‘存在条目级可定位结论→5–6档’，取5；无已核实错引，不cap、不判虚构。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/02/03/05/07、CG08/09/14）仅有单条 route 级 MetaCyc 记录（ERYTHRITOL-DEG-2），在 E0R11 不可核，登记为 UNRESOLVED_SOURCE；性状类全部为 INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）。无已核实错引，故不 cap；决策相关组缺可核对条目级证据，按 3–4 档取 3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：仅说明答案实际交付的引用形态（1条数据库条目+1条内部知识声明）；不支持其内容真实性或覆盖范围

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 5–6档：答案给出confidence分级并列出uncertainties（氧条件未指定；中间体立体化学/辅因子质子平衡无原文；保藏号/基因组/培养参数未填），未知项null而非编造，属正面披露；但把整条路线、三酶与C58全路径能力以medium/路线级来源呈现，未说明菌株级与路线同一性不确定性，属‘部分结论强度仍超过依据’。故5–6档取6，不cap（非系统性误导）。

<details><summary>V0.4理由与本行变化背景</summary>

答案诚实标注 confidence（medium/low/unknown）、未知项填 null，并具体列出中间体立体化学、辅因子平衡、保藏号/基因组缺失等限制；但未披露主链与题面指定路线的识别风险，以 medium 置信把另一路线当作指定路线呈现，属单点过度确信而非系统性误导，5–6 档取 6，不 cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持其确已披露部分未知与限制；不支持其已披露路线同一性与菌株能力不确定性

</details>

## Grok

答案SHA256：`42097b20d1536054037594a9e9289ce4cca397657e6465b2894f24b55a8e369b`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Three-step pathway and enzyme names are present, but the answer omits both the per-step corresponding microorganism and all 15 organism traits/profiles. The delivered route also diverges from the specified erythritol degradation II target main chain. This fits partial module coverage with major omissions; score 3 within the allowed task-deviation/low-coverage range.

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_129：Requires one enzyme and one corresponding microorganism per step, plus all 15 traits per organism profile.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_129：Gold terminal is D-erythrose 4-phosphate; this identifies the target route terminal but does not by itself prove every alternative chemistry impossible.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_129：Gold has three ordered required steps.

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer is internally sequential and roughly atom-balanced, but its target main-chain chemistry diverges at all three required steps: S1 gives L-erythrulose instead of target D-erythrulose; S2 gives L-erythrulose 1-phosphate instead of D-erythrulose 4-phosphate; S3 cleaves to DHAP plus formaldehyde instead of forming D-erythrose 4-phosphate. Multiple critical intermediates/products and the endpoint differ, with only internal-knowledge support; score 4 in the low chemical-validity/route-mismatch band.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：Frozen target route uses D-erythrulose, D-erythrulose 4-phosphate, and D-erythrose 4-phosphate; it does not establish that the answer&#x27;s alternative route cannot exist.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_129：Lists accepted target enzymes/EC for the frozen route; does not verify the answer&#x27;s L-erythrulose route.

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a仅评目标反应酶对应。原答3步均无EC，且无一步与accepted名称/EC形成已确认匹配；原答S3用L-erythrulose-1-phosphate aldolase生成DHAP+甲醛，与gold S03的D-erythrulose 4-phosphate isomerase→D-erythrose 4-phosphate不符，程序路线诊断亦标S03 SUBSTITUTED_MIDROUTE_FOREIGN；原答S1产物L-erythrulose与gold S02的D-erythrulose存在立体冲突；S2的1-磷酸与gold S01的4-磷酸仅可能表示等价，仍为UNKNOWN。仅脱氢酶/激酶局部官能团线索有用，核心目标酶对应未成立，故落C04低档并按C05取2。不能NE：gold与路线诊断可支持低档定界；也不能升档：无目标级accepted支持。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：Gold主链产物对照：S02→D-erythrulose，S01→D-erythrulose 4-phosphate，S03→D-erythrose 4-phosphate；不证明具体蛋白活性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_129：Gold accepted enzymes: S01 D-erythrulose kinase EC 2.7.1.210; S02 erythritol/L-threitol dehydrogenase; S03 D-erythrulose 4-phosphate isomerase EC 5.3.1.34；仅为功能/EC级参考，不证明任意具体蛋白底物谱或实验活性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_129：Gold终点为D-erythrose 4-phosphate(2-)；支持对主链终步产物方向作对照。
- ANSWER_TEXT / steps&#91;0..2&#93;.enzyme：原答三步酶名均为EC null；未给出可核accepted EC或具体蛋白证据。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> No microorganism identity, strain, TaxID, or organism_profile is delivered for any required step. The task explicitly requires a corresponding microorganism per step; this module is entirely absent, so MISSING=1 under P44 rather than a scientific-error score.

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_129：Requires one corresponding microorganism per step and organism profiles.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer delivers no organism profiles and therefore no 15-trait records. The task requires all 15 traits for each profile; this module is entirely absent, so MISSING=1 under P44.

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_129：Requires all 15 traits per organism profile, with explicit nulls for unknown items.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The only evidence entry is EVID_001 with source_type INTERNAL_KNOWLEDGE_ONLY and null database, record_id, and locator. All route and enzyme claims reference this entry, so important conclusions cannot be traced to a locatable record. No verified mis-citation is established, so this is MISSING_SOURCE low-band, not a cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_129：Shows the answer&#x27;s only evidence entry is internal-knowledge only and lacks a record/locator.

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer repeatedly labels the route assignment and step chemistry as low-confidence/internal inference, explicitly states that ECs, genes, microorganisms, and representative strains are unknown, and lists alternative Brucella phosphorylation-first catabolism as a competing route. It does not present predictions as observations and does not hide the main limitations; confidence is consistent with the stated evidence.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_129：Shows explicit uncertainty labels, null handling, and disclosure of an alternative route.

</details>

## GPT5.6

答案SHA256：`841354aa91755e4de20f71ede8afa0adbadde302a93ab925d8c94348c1b072ca`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面指定erythritol degradation II且要求主链、逐步酶/菌与15项性状。答案回显路线名并给出两步行文，但只覆盖主链片段、缺第三/终点步，且15项性状全为null；属主要必要内容不全而非格式不可评，D1落在&#91;1,6&#93;弱档上沿。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_129：支持gold起点Erythritol与终点D-erythrose 4-phosphate；不支持答案止于erythrulose 1-phosphate。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_129：支持该题gold为3步LINEAR_UNIQUE；不支持答案只给出2步。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 在给定D2允许&#91;1,4&#93;内评分。答案两步局部化学上连贯且氧化还原/磷酸化配平可辨（Erythritol+ATP→Erythritol 1-phosphate；Erythritol 1-phosphate+NAD+→Erythrulose 1-phosphate），但主链先磷酸化后氧化，与指定路径的核心顺序/终点不符，且未给出向中心代谢的可核延续；取弱档上沿4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：支持gold方向为S02 Erythritol→D-Erythrulose、S01 D-Erythrulose→D-erythrulose 4-phosphate、S03→D-erythrose 4-phosphate；不支持答案的磷酸化先行两步链。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 程序给出目标对齐待判；人工按gold核对：目标S02为erythritol/L-threitol dehydrogenase催化Erythritol→D-Erythrulose，目标S01为D-erythrulose kinase EC 2.7.1.210，目标S03为D-erythrulose 4-phosphate isomerase EC 5.3.1.34。答案S1为erythritol kinase EC 2.7.1.27、S2为erythritol-1-phosphate dehydrogenase，产物止于erythrulose 1-phosphate，三个目标反应均未交付；酶模块并非整体空白，故不记整维MISSING，按全目标缺失的&#91;1,2&#93;档取2（有局部替代链信息但无目标催化信用）。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_129：支持S01 accepted D-erythrulose kinase EC 2.7.1.210与S02 erythritol/L-threitol dehydrogenase；不支持答案的erythritol kinase EC 2.7.1.27或erythritol-1-phosphate dehydrogenase作为目标步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_129：支持三个目标反应的底物/产物与顺序；不支持答案的两步替代链获得目标反应信用。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案把所有步都归给Brucella abortus strain 2308 (taxid 444178)，并声明complete_pathway_organism_profile_id=ORG_001。Gold仅S03纳入Brucella abortus（taxid 235，物种级），S01/S02为Mycolicibacterium smegmatis；Brucella作为 erythritol 利用相关候选可辨，但菌株/taxid与整条路径能力均无冻结证据支持，属部分候选、关键身份与作用范围未充分核验的5–6档，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_129：支持S01/S02为Mycolicibacterium smegmatis、S03含Brucella abortus（taxid 235）；不能确认答案的B. abortus 2308/taxid 444178为整条路径菌。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 唯一organism_profile ORG_001的F1-F15全部为value null/空对象且confidence=unknown；无任何性状事实可评。按rubric P44，全部必需性状均为null/空值时D4按MISSING记1分，不宣称检测到具体科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_129：gold中可见M. smegmatis等菌的性状记录；答案未提供任何对应值，不能据gold回填答案。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_129：支持部分性状子字段的可评分性/待裁决状态；不改变答案全部null的交付事实。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案evidence_registry的EVID_001-EVID_003均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为null；路线、酶-EC、微生物、性状均无外部可定位来源。属MISSING_SOURCE低档，非已核实错引，不触发cap；有内部证据结构但几乎无法核查重要结论，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_129：答案自报来源均为INTERNAL_KNOWLEDGE_ONLY且无定位符；不提供外部可追溯性。

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案对EC null、性状null、路线映射和菌株不确定性有明确说明，confidence使用medium/low/unknown，优于系统性把预测写成实证；但它把内部知识包装为medium并声称complete_pathway_organism_profile_id=ORG_001，且route_summary未披露其与指定主链的偏离，部分限制仍偏笼统。落5–6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_129：答案确实列出若干未知与限制；同时可读出其内部知识支撑的路径/菌株声称强于已交付证据。

</details>
