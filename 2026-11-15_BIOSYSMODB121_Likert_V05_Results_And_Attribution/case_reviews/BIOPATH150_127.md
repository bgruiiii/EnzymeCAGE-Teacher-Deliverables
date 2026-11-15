# BIOPATH150_127：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：D-threitol degradation

污染物：D-Threitol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 44 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 43.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 42 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 53.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 30 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 41.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`77131029d5a961b4d7738d7e10f337b6edad9ca6ccc9a8abb41c6fc3d12e7303`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 题面要求的三步主链、逐步酶/菌及15项性状均有交付；但各步EC全部为null，且程序路线诊断route_status=DEVIATES并将D1轴允许范围限定为&#91;1,4&#93;，故在受限范围上沿取4，不能进入更高档。

<details><summary>V0.4理由与本行变化背景</summary>

主链3步、底物/产物SMILES、酶名、对应菌、15项性状与不确定性均有交付，路线名按题面填写；但三步EC均为null、15项性状均无逐项来源、菌无株号/TaxID，属若干必要内容遗漏，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION.BIOPATH150_127：要求三步主链、每步首选酶及EC、对应微生物、15项性状；不证明答案科学正确。
- ANSWER_TEXT / ANSWER.steps：答案实际交付3步与15项性状；仅证明交付情况和EC为空，不证明内容正确。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_127：gold确认本题主链步数为3；不把全图其他行当作缺步分母。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分9 → V0.5新分5，变化-4。

新裁判理由：

> 三步主链的名称、顺序和终点（D-erythrose 4-phosphate）大体对应gold；但S02入口步被程序固定为NONMATCH/STEREO_CONFLICT_SPECIFIED，答案S1的D-Threitol SMILES与gold指定立体结构冲突，属显式立体化学缺陷，按D2显式立体冲突上限落在&#91;1,5&#93;，取5而非更高。

<details><summary>V0.4理由与本行变化背景</summary>

三步化学方向与gold一致：D-threitol→D-erythrulose→D-erythrulose 4-phosphate→D-erythrose 4-phosphate；NAD+/NADH、ATP/ADP辅因子在列，主链连续，终点合规。仅有局部证据缺失与立体化学表述未展开，不改变主结论，取9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：gold确定S02底物立体结构与反应方向；不证明答案其他步骤正确。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.substrates&#91;0&#93;.smiles：答案实际SMILES；用于与gold比较确认立体冲突，不扩展到产物或微生物。
- ANSWER_TEXT / ANSWER.steps&#91;1..2&#93;：答案后续步骤的化学表达；不证明磷酸电荷表示已核。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> 程序固定S=0、F=1、U=2：S02为已确认KEY目标失败，S01/S03为表示/电荷未确认的U；没有可计入的已支持目标信用。受D-KEY4的&#91;1,4&#93;限制，且除已确认失败外仅保留局部未核，取2而非更高；不以错误路线内部酶自洽增加目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名/功能与gold相符：D-threitol dehydrogenase、erythrulose kinase、D-erythrulose 4-phosphate isomerase；但三步EC全为null，且无基因/蛋白标识与来源，属主要对应有支持但关键标识缺失，7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_127：数据库策展G4接受名/EC；不证明具体蛋白底物谱、实验活性或菌株能力。
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.enzyme：答案实际酶名与EC交付情况；EC全部为null，不因此自动判错但也不能计为已验证配对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：S02 KEY入口底物与方向；用于固定target failure的路线依据，不扩展到其他步。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案全程使用Enterobacter aerogenes（现称Klebsiella aerogenes），仅物种名，无 strain、无TaxID、无反应级或全路径能力证据；也未提供任何对应来源。物种候选并非已证伪，但身份与全路径能力均未充分核验，符合5–6档的“有合理候选和部分支持、关键作用范围未充分核验”，取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出Enterobacter aerogenes作为三步及完整路径菌，但无株号、TaxID、步级反应能力或全路径能力证据，仅INTERNAL_KNOWLEDGE_ONLY并自述未找到直接文献。该菌为合理候选，但关键身份与作用范围未充分核验；与gold所列菌不同不自动判错（gold非穷尽），5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism：答案的微生物身份与全路径能力声称；不证明其正确。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_127：gold列出Mycolicibacterium smegmatis、Brucella abortus、Agrobacterium radiobacter、Pectobacterium atrosepticum等精确微生物；gold非穷尽，不证明E. aerogenes不能完成该路线。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项性状均已给出；部分基础性状（革兰氏阴性、杆状、运动、不产孢、兼性厌氧、ATCC 13048）对Enterobacter aerogenes属常见描述，但所有trait evidence_id均为null，温度35°C、pH 7.0、盐度等数值缺少可定位来源，且本地冻结性状记录没有该菌。故只能落在“部分准确且适用、关键项证据不足”的5–6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全，Enterobacter aerogenes的常见性状（革兰阴性、杆状、运动、无芽孢、兼性厌氧、ATCC 13048等）大体合理；但温度、pH、盐度及多数性状无冻结记录/来源，关键项未核，5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：答案实际性状值与confidence；不证明其准确。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_127：gold性状行属于其他分类群，未含Enterobacter aerogenes；不能用于验证或反驳该菌性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_127：仅说明gold菌株的性状可评分字段；不适用于Enterobacter aerogenes。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案只有EVID_001一条证据，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；所有性状evidence_id为null。按D5六状态，决策相关组均为MISSING_SOURCE，仅能落在1–2档；不是已核实错引，无D5 cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案唯一证据EVID_001为INTERNAL_KNOWLEDGE_ONLY，无数据库/文献记录ID或定位；所有关键组（路线、酶、菌、性状）均无可追查外部来源，属MISSING_SOURCE低分档。无已核实错引，按缺失不cap，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：答案唯一来源条目；仅内部知识，无定位记录，不能支持可追溯性。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits.*.evidence_id：性状没有逐项来源；不证明性状错误，只证明来源缺失。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确列出多项不确定性：EC/基因未知、E. aerogenes选择无直接D-threitol文献、激酶/异构酶为类比推断、C2氧化与末端氧化选择存疑、旧名分类提示；并用low/medium/unknown区分置信。未见系统性把预测写成实证观测，也未掩盖主要限制，故D6取7–8档上沿附近，给8。

<details><summary>V0.4理由与本行变化背景</summary>

答案逐步标low置信，uncertainties明确列出酶/菌/路线歧义、未直接引用实验文献、旧名等，未把内部推断写成实证；但多数性状仍为低/中置信且无来源，披露未达9–10，取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案实际披露内容；支持D6披露质量，不证明科学结论正确。
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.confidence：答案对步骤置信的表述；不替代科学核验。

</details>

## DeepSeek

答案SHA256：`ee75d9c98d349d48b60908be1979a3b667ccd390b3a5ab190946355a5b13c3b6`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 结构化交付完整：3步均给出底物/产物名称与SMILES、一个首选酶、一个对应菌，15项性状齐全、无遗漏字段，JSON可解析；但所选主链为D-threitol→D-threose→D-threose 4-phosphate→D-erythrose 4-phosphate，与题面锁定的D-threitol degradation参考主链（D-threitol→D-erythrulose→D-erythrulose 4-phosphate→D-erythrose 4-phosphate）不一致，同时声明is_single_continuous_route=true并原样使用路线名，属“自称合规却交付不同化学路线”的任务符合度关键错误（R2-100/OBS-D1D2）；程序路线诊断为DEVIATES且D1允许区间为&#91;1,4&#93;，故在区间内取上沿4：结构完整是取上沿而非更高的理由，路线化学质量另在D2独立评价。

<details><summary>V0.4理由与本行变化背景</summary>

3步主链、每步底物/产物/SMILES、酶与菌、15项性状、JSON结构均交付；路线名原样保留；仅S2/S3的EC缺失、部分性状证据弱，属少量遗漏，不构成任务模块缺失。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:route_scope+route_summary+steps&#91;0..2&#93;：支持答案自称单一路线且以D-threose/D-threose 4-phosphate为中间体；不支持任何酶活性或菌株能力成立。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：支持参考主链S02的底物D-Threitol/产物D-Erythrulose与S01/S03的连接顺序；不评价答案任何具体酶或菌株，也不扩展到性状或来源层。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_127：支持题面路线D-threitol degradation的起终点为D-Threitol→D-erythrose 4-phosphate(2-)；不支持任何步骤化学细节。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分3 → V0.5新分5，变化+2。

新裁判理由：

> 方向为降解并向题面终点D-erythrose 4-phosphate，三步连接连续（S1→S2→S3，predecessor_step_ids自洽）。化学上：S1伯醇氧化为醛糖、S2 ATP依赖磷酸化、S3 C2差向异构化均属可成立的转化类型，碳骨架保持C4，无反应方向反转、无一步跳中心代谢物；但S1未列NAD+/NADH（P103局部计量缺陷，非cap），关键中间体为D-threose而非参考D-erythrulose，S2/S3的酶功能无任何独立依据，合理性证据有限。按5–6档“主干部分成立但关键中间体/转化仍需修订”，并受程序D2允许区间&#91;1,5&#93;（显式立体冲突候选上限）限制，取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链首步即与gold不符：答案D-threitol→D-threose，gold为D-threitol→D-erythrulose；第二步又改为D-threose→D-threose 4-phosphate，而gold为D-erythrulose→D-erythrulose 4-phosphate；虽终点D-erythrose 4-phosphate正确，但两个核心中间体与主链转化错误，构成D2关键错误，cap≤4取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：支持参考主链的中间体、方向与终点；不支持答案替代中间体（D-threose系列）在参考记录中存在。
- ANSWER_TEXT / ANSWER:steps&#91;0..2&#93;：支持答案三步的底物/产物、SMILES与所标reaction_type；不支持其酶学可实现性。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> N=3（S01/S02/S03全为必答KEY步）；已确认S=0、F=2（S02入口、S03终点，NONMATCH/STEREO_CONFLICT_SPECIFIED均带REAL-ROUTE失败证明）、U=1（S01对齐未确认）。两项已确认KEY失败触发D-KEY4上界4，且confirmed_target_rate=0，故只能落在&#91;1,2&#93;：主推荐的目标催化对应几乎不存在。相对1的有限定位仅为：入口底物身份正确、入口酶名与accepted“D-threitol dehydrogenase”同族（name-level，且答案EC 1.1.1.185与accepted 1.1.1.403不一致，未核）、S3产物名与参考终点一致；这些属错误路线内部的局部呼应，不构成目标功能信用，故取2而非更高。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名D-threitol dehydrogenase方向合理但EC 1.1.1.185与gold的1.1.1.403不符且E0无该EC记录；S2用D-threose kinase，gold为D-erythrulose kinase EC2.7.1.210；S3用D-threose-4-phosphate 3-epimerase，gold为D-erythrulose 4-phosphate isomerase EC5.3.1.34，且3-epimerase与C2差向异构的底物-产物关系不匹配。多步核心酶-反应对应错误，D3a关键错误成立，cap≤4取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：逐目标支持参考步的底物/产物与方向（S02:D-Threitol→D-Erythrulose；S03:D-erythrulose 4-phosphate→D-erythrose 4-phosphate）；不支持答案的D-threose中间体。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_127：支持各步accepted酶名/EC（S02=D-threitol dehydrogenase/1.1.1.403；S01=D-erythrulose kinase/2.7.1.210；S03=EC 5.3.1.34）；不证明任何具体蛋白底物谱。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_127：支持本题为LINEAR_UNIQUE、ordered_step_count=3的必答主链；不提供化学裁定。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 微生物身份与参考基本一致：答案给Mycobacterium smegmatis（现名Mycolicibacterium smegmatis），organism_gold显示该种是S01/S02/S03三步的来源菌，PATHWAY_COMPLETE=TRUE（taxid 1772），故“该菌参与D-threitol降解”有物种级依据。菌株“mc2 155”/TaxID 246196在冻结切片无记录（GAP-127-013/014），按规则保持UNRESOLVED、不判虚构；以物种级记录支持菌株级声称属粒度不足（R2-107，档内扣、默认不cap）。答案对逐步（自选替代酶）归属的菌株能力无独立依据，且F8把路径细节写成“经D-threose”，属作用范围表述超出支持。综合取7档下沿。

<details><summary>V0.4理由与本行变化背景</summary>

选用Mycobacterium smegmatis mc2 155（TaxID246196），与gold的Mycolicibacterium smegmatis（TaxID1772）同物种/近缘；gold PATHWAY_COMPLETE支持该物种可完成D-threitol路径，且S1/S2/S3均含该物种，故微生物选择有合理支持；但菌株mc2 155与TaxID246196无E0记录，菌株级三步能力未核，属粒度不足，档内取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_127：支持Mycolicibacterium smegmatis(taxid 1772)是三步的来源菌且PATHWAY_COMPLETE=TRUE；不支持菌株mc2 155/246196的身份或该菌携带答案所列具体替代酶。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_127：支持参考步骤的酶来源菌为M. smegmatis（S01/S02），S03有多个可选来源菌；不证明答案所列D-threose系列酶存在。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 多数关键性状与冻结记录一致或落在观测范围内：F10非运动（presence of motility=false）、F11杆状、F12革兰氏阳性、F13不产孢、F14的genome size 6,988,209 bp与GC 67.4%均在trait_gold观测范围内（5,838,428–7,309,287 bp；67.3–67.6%），F2 preference=mesophilic与记录一致。问题集中在关键项语义与证据：①F2把单条37℃培养记录写成optimum_c=37且raw_text称“grows optimally at 37°C”，违背“培养温度≠最适值”的解释层口径；②F8把降解路径细节写成经D-threose，超出记录支持；③F9把三个通路酶列为“酶活”，其中两个无任何依据；④F5 ATCC 700084、F14 NC_008596.1在冻结切片无对应记录（保留待核、不判错）；⑤F3/F4为诚实null（F4其实有观测的0/6 %NaCl，漏填记在D1完整度，D4不重复重扣）。综合落5–6档“部分性状准确且适用，但关键项证据不足或条件解释需修订”，取上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

多数一般性状与gold观测一致（F10非运动、F11杆状、F12 Gram阳性、F13不产孢；F2最适37℃/mesophilic与gold一致），但F8把D-threitol降解写成经D-threose，F9列出的三种酶沿错误支路，F4/F3为明确未知，F5/F14/F7证据弱或菌株级未核；关键降解/酶活性状错误使D4只能部分可用，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_127：支持taxid 1772的观测性状：motility=false、cell shape=rod-shaped、gram positive=true、sporulation=false、genome size与GC范围、temperature growth记录与preference=mesophilic；不支持把37℃当作最适值。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_127：支持F2 optimum_c无可评分来源（completeness_only）、maximum_c=45与salinity min 0/max 6为已观测标量；不支持将培养温度升级为最适值。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）实际交付的来源全部是EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY自述：database、record_id、locator均为null，claim_scope只有泛化词组，无法定位任何反应、酶、菌株或性状条目，属MISSING_SOURCE（R2-34），按P41“全部缺失→低分档，默认不cap”。未发现经核实的错引或虚构（不登记VERIFIED_MIS_CITATION_*，亦不判CONTRADICTED）；答案把来源性质如实标为内部知识且claim→evidence_id映射自洽，故在1–2档内取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator；所有关键结论仅内部知识，无法定位到条目或计算记录。按MISSING_SOURCE低分档，无已核实错引，不cap，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:evidence_registry+evidence_id_refs：支持“全部来源为INTERNAL_KNOWLEDGE_ONLY且无database/record/locator”这一交付事实；不支持其中任何科学内容为真或为假。
- RUBRIC_CLAUSE / R2-34：MISSING_SOURCE定义与“低分档、默认不cap”的处置；不把缺失自动升级为错引。

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案只用source_type=INTERNAL_KNOWLEDGE_ONLY标注证据性质（未伪称数据库直查），且F3/F4以value null + confidence=unknown诚实标未知；但同一内部知识支撑下把F1/F6/F10/F11/F12/F13六项性状标为high confidence，uncertainties为空数组、每步uncertainty=null，route_summary与F8/F9把无依据的替代主链表述为既定事实，主要限制与替代可能性未说明。属“多处过度确信、主要限制未说明”（3–4档），尚不构成系统性把预测包装成实验观测的cap候选，故取4、不cap；D5来源缺失不自动连坐本维。

<details><summary>V0.4理由与本行变化背景</summary>

答案用confidence标签区分high/medium/unknown，缺失性状填null并标unknown，有一定不确定性披露；但uncertainties为空，未说明内部知识推断与替代路线不确定性，错误主链仍以medium呈现，部分结论强度超过依据。属披露过于笼统，档内取5。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:confidence+uncertainties：支持“自述内部知识却多处标high、无不确定性说明”的表述事实；不裁决这些性状真值。
- RUBRIC_CLAUSE / R2-119：单点过度确信与系统性误导的区分及档位处置；不把单点/多处过度确信直接转cap。

</details>

## Kimi

答案SHA256：`5b43775f98a2480e3b9d0d2326755477f448b28423873ef1be5027d4bda5343e`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> JSON可读且route_scope路线名原样，但必答三步主链只交付两步，缺S03至D-erythrose 4-phosphate；第二步microorganism=null，第一步与第二步均无EC。模块大体可辨但关键终点与酶菌关联不完整，按D1 3–4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

路线只交付2步，gold为3步且终止于D-erythrose 4-phosphate；S2的microorganism整体为null，两个酶均未给EC；15项性状齐全且明确未知标注清楚。主要模块有涉及，但必要内容遗漏，按5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：显示答案仅含S1/S2及S2微生物null，支持完整性不足定位；不独立证明目标化学。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：显示本题必答主链含S01/S02/S03三步及终点方向；不扩展到答案未交付内容。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 两步反应概念（醇氧化、酮糖磷酸化）方向可辨，但程序诊断为S01/S02 STEREO_CONFLICT_SPECIFIED/NONMATCH；答案SMILES与gold目标结构在指定立体化学上冲突，且缺S03终端异构化，主链连续性不足。按D2 3–4档取4并受关键化学冲突限制。

<details><summary>V0.4理由与本行变化背景</summary>

S1的D-Threitol→D-Erythrulose与S2的D-Erythrosine→D-Erythrulose 4-phosphate在化学方向与gold一致；但缺gold S03的D-erythrulose 4-phosphate→D-erythrose 4-phosphate异构化步，且central_metabolism_entry直接把erythrulose-4-phosphate推测为转酮酶入口，连接缺步骤。主干部分成立但关键连接需修订，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：给出答案SMILES与反应顺序；不能自行证明其与目标立体化学一致。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：给出目标反应有向结构及SMILES，用于核对D-threitol/D-erythrulose/D-erythrulose 4-phosphate；不支持答案中未声称的下游。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 程序给出的S01/S02为确认KEY目标失败（STEREO_CONFLICT_SPECIFIED/NONMATCH），S03为缺失/对齐未确认；无目标步达到S，confirmed_target_rate=0。按D-KEY4仅可在&#91;1,4&#93;内取分；因仍有两个可辨认反应名但无目标信用，取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

S1给出膜结合多元醇脱氢酶SldAB但无EC；S2给出D-erythrulose kinase putative但无EC。两步酶功能方向与gold一致，但关键酶-EC对应未核，属有合理候选和部分支持，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：显示两个酶名/EC null及S03缺步；酶名出现不等于目标反应已获支持。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_127：列出目标步accepted酶名/EC；仅支持目标反应功能粒度，不证明答案所给具体蛋白或菌株活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：给出目标反应有向结构；用于支持S01/S02立体化学非匹配及S03终端目标。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出一个可辨微生物G. oxydans 621H并配到S1，但S2微生物为null、S3缺失；G. oxydans对D-threitol的具体单步氧化能力仅有内部知识/低置信来源，E0无相应菌株/酶记录。属部分候选与部分支持、关键身份/能力待核，按5–6档取下沿5；无已核实身份错配，故不cap。

<details><summary>V0.4理由与本行变化背景</summary>

S1推荐Gluconobacter oxydans 621H，物种为已知多元醇氧化菌，属合理候选；但E0无该菌记录，身份/能力未核。S2的microorganism整体为null，未覆盖该步。答案未声称全路径能力。按部分支持取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：显示G. oxydans 621H身份与性状块；不证明其D-threitol氧化能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_127：gold列出M. smegmatis等目标步菌；不能据此直接判定G. oxydans不能做该步，也不支持其能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> D4部分可用但关键项有错误：F5_culture_collection把Gluconobacter oxydans 621H的保藏号写为DSMZ DSM 3503，而补充证据显示DSM 3503是G. oxydans模式株（strain designation I；ATCC 19357等），并非621H；F2_temperature以EVID_002/DSM 3503记录给出optimum_c=30，但补充证据明确培养温度不是最适值，且该记录并非621H菌株；F14_genome_basic的NC_006677、2702173 bp、60.9%在E0中无冻结记录（GAP-127-001等），只能UNRESOLVED，不能判错也不构成已核支持；F1/F6/F7/F8/F9/F11-F13/F15多为物种级内部知识，Gram阴性、杆状、不产孢、好氧等大体合理，但菌株级适用性与证据不足。按D4锚点落在5-6档（部分性状准确且适用，但关键项证据不足或条件解释需修订），因存在已核F5错配及F2条件误读，取5分。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现：12项填写、3项明确未知、0遗漏。F1/F2/F5/F6/F7/F8/F9/F11–F15内容总体合理，但E0无G. oxydans 621H的性状记录，关键项（DSM 3503、NC_006677、温度等）均未核；F5的DSM 3503与621H菌株匹配也待核。按部分性状准确但关键证据不足，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：答案中Gluconobacter oxydans 621H的15项性状、置信度与evidence_id
- E0_EVIDENCE / SUPP:DSM:3503：DSM 3503为G. oxydans模式株（strain designation I；ATCC 19357等），不是621H；培养温度25°C不是最适值
- E0_EVIDENCE / SUPP:TAX:290633：G. oxydans 621H的官方分类身份与别名；不证明步骤活性或全部性状
- GOLD_SLICE / trait_gold.tsv：本案gold性状切片含Mycolicibacterium smegmatis/Brucella abortus/Agrobacterium radiobacter/Pectobacterium atrosepticum等，无G. oxydans 621H性状行；不能用于支持或反驳答案菌株的多数性状

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> route核心步与酶仅EVID_001 INTERNAL_KNOWLEDGE_ONLY，无locator/record；G. oxydans身份、DSM 3503、NC_006677及部分性状虽有来源名/记录号，但E0无法核验，登记UNRESOLVED；不少性状仍仅内部知识。决策相关核心来源多为MISSING_SOURCE，个别UNRESOLVED_SOURCE，未发现已核实虚构或错引，不cap；按3–4档取下沿3。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关核心组CG01/CG02/CG03/CG05/CG07仅有INTERNAL_KNOWLEDGE_ONLY或缺失来源，无条目级可核对证据；性状组部分有数据库条目但E0不可核，记UNRESOLVED_SOURCE。无已核实错引，不cap；按全部缺失低分档取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示EVID_001为内部知识、EVID_002/003为记录号、EVID_004为内部知识；仅评价实际交付来源。
- ANSWER_TEXT / ANSWER.route_summary：显示核心路线被明示为重建；不提供可定位外部来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案明确披露route为重建、EC与第二步微生物未知、磷酸化位点不确定，并在uncertainties列出主要限制；未知性状多处置null。仍有若干EVID_004内部知识以medium confidence包装，属单点/局部过强而非系统性误导，故按7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

答案明确说明未检索到权威通路数据库记录、路线为重建、S2酶/菌未知、EC置null，并列出多条具体限制；多数观测/推断/未知标注合理。但部分内部知识性状标为medium、F5标high，证据强度略高于可核实程度，属单点/局部过度确信，非系统性误导，取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案对路线重建、EC缺失、S2微生物未知、位点不确定的披露；支持D6正面评价。
- ANSWER_TEXT / ANSWER.evidence_registry：显示EVID_004为内部知识却承载多项medium confidence性状；用于识别局部过度确信。

</details>

## Qwen

答案SHA256：`ed573e082d041065098ae14d7f22c24ed0a00d10caf3d2c2dad50c409c84494c`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分7 → V0.5新分9，变化+2。

新裁判理由：

> 路线名原样填写为D-threitol degradation；三步主链均给出底物/产物英文名与SMILES、首选酶及EC、对应微生物，并且单一菌profile去重后15项性状全部出现，未见必答模块缺失或明显路线改选。少量低置信/内部来源性状与科学问题归D2/D3a/D5处理，不在D1重复重扣。

<details><summary>V0.4理由与本行变化背景</summary>

7–8档：三步均给出主底物/主产物(英文名+SMILES)、首选酶+EC、对应微生物；15项性状全部出现且按物种+菌株单条profile去重；chosen_route_name原样为D-threitol degradation。任务结构完整，仅少数性状为诚实null、组织上全部步骤共用单一菌，不构成完整性缺失。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_127：正式案为LINEAR_UNIQUE且ordered_step_count=3；用于核对必答主链长度。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：金标三步主链从D-Threitol到D-erythrose 4-phosphate，S01/S02/S03均为主链；用于D1完整性核对。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 三步的反应类型与主链连接（D-Threitol→L-Erythrulose→L-Erythrulose 4-phosphate→D-Erythrose 4-phosphate）基本连续，方向未反，NAD+/ATP辅因子在列；但第一步主产物写作L-Erythrulose而gold为D-Erythrulose，第二、三步又沿用L-erythrulose中间体，属于显式立体化学冲突，按C06候选≤5，故取5而非6。

<details><summary>V0.4理由与本行变化背景</summary>

7–8档：主链拓扑与gold一致（D-Threitol→erythrulose→erythrulose-4-phosphate→D-erythrose 4-phosphate），方向正确，辅因子完整在列（S1 NAD+/NADH/H+，S2 ATP/ADP），终点E4P符合题面终点。局部问题：中间体标注为L-Erythrulose/L-Erythrulose 4-phosphate而gold为D-型，且产物SMILES未编码立体化学，属命名/立体化学局部需修订，不改变主链结论，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_127：根化合物为D-Threitol、末端为D-erythrose 4-phosphate；支持起点/终点核对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：金标主产物为D-Erythrulose、D-erythrulose 4-phosphate、D-erythrose 4-phosphate；用于识别答案L-erythrulose中间体的显式立体冲突。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 三步目标反应均有可辨认酶名/EC并指向氧化、磷酸化、异构化，D-threitol dehydrogenase等名称与目标功能大体对应；但三个显式EC均与gold accepted不同（1.1.1.122 vs 1.1.1.403；2.7.1.101 vs 2.7.1.210；5.3.1.33 vs 5.3.1.34），且E0无对应EC冻结记录，按P64/P66不能仅凭gold不等判F，配对保持UNRESOLVED。因关键目标支持未确认但非已证催化矛盾，按有限支持取&#91;5,6&#93;下沿5，不能给7以上。

<details><summary>V0.4理由与本行变化背景</summary>

5–6档：三步酶功能类型与反应相符（脱氢酶/激酶/异构酶），酶名与gold高度对应；但三个具体EC（1.1.1.122/2.7.1.101/5.3.1.33）与gold（1.1.1.403/2.7.1.210/5.3.1.34）不同，且E0无冻结记录（GAP-127-002/004/005）无法核实，按P66保留低分与待核、不判错不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_127：gold accepted酶与EC：D-erythrulose kinase 2.7.1.210、D-threitol dehydrogenase 1.1.1.403、D-erythrulose 4-phosphate isomerase 5.3.1.34；用于差异核对，不单独证明答案EC错误。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：三步目标反应S01/S02/S03及其主底物/主产物，用于核对D3a目标步与酶功能对应。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Pseudomonas putida TaxID 303 identity is supported at species-name level, but no strain is given and no frozen evidence supports P. putida step-level D-threitol dehydrogenase/kinase/isomerase roles or whole-pathway D-threitol degradation. Gold step organisms differ. Identity is not fabricated, but capability is unverified; 5-6 band, choose 5 because the whole-pathway claim is unsupported.

<details><summary>V0.4理由与本行变化背景</summary>

5–6档：所选Pseudomonas putida(TaxID 303)为真实有效物种（E0身份SUPPORTED，非编造），但答案将同一菌写为三步催化者并声明完成整条路径(ORG_001=complete_pathway)，仅有&#x27;general phenotype&#x27;内部知识，无反应级/全路径证据；作用范围未充分核验。与gold用菌(M. smegmatis等)不同但无冻结证据判错，按身份阶梯（身份定位≠反应级能力≠整路径能力）取5，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Supports official Pseudomonas putida name/rank/TaxID 303 only; does not support strain identity, step activity, or D-threitol pathway capability.
- E0_EVIDENCE / f3e0:bacdive:12880：P. putida strain record with collection numbers and culture-temperature records; does not support D-threitol degradation or the answer&#x27;s three enzyme activities.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_127：Gold step organisms include Mycolicibacterium smegmatis and others; gold is not exhaustive, so difference alone is not a confirmed error.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> All 15 trait fields are present, with 10 filled and 5 explicit unknown/null. Basic P. putida traits such as aerobic, motile, rod-shaped, Gram-negative and non-spore-forming are plausible, but the key F7-F9 D-threitol utilization/degradation/enzyme-activity claims are unsupported by the frozen P. putida evidence. 5-6 band, choose 5 because key application traits lack evidence.

<details><summary>V0.4理由与本行变化背景</summary>

5–6档：P. putida一般性状（F10 motile、F11 rod、F12 Gram-negative、F13 non-spore、F1/F6 aerobic呼吸）符合该种常见表型，F2/F3/F4/F5/F14如实填null；但F7/F8/F9声称可利用/降解D-苏糖醇并具三种酶活，仅INTERNAL_KNOWLEDGE_ONLY且confidence=low、raw_text=null，属关键能力项缺证；该菌无E0性状记录无法逐值核验。综合关键项证据不足取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_127：Provides trait reference rows for gold organisms; does not provide a full P. putida trait profile or D-threitol degradation trait for the answer profile.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_127：Shows which gold-organism traits are scoreable; does not verify the answer&#x27;s P. putida traits.
- E0_EVIDENCE / f3e0:bacdive:12880：Supports limited P. putida strain record facts (collection, culture-temperature observations); its substrate panel does not support D-threitol utilization or the answer&#x27;s pathway enzyme activities.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> All three evidence_registry entries are source_type INTERNAL_KNOWLEDGE_ONLY with free-text locators and no database/record IDs. This is MISSING_SOURCE for decision-relevant groups, not a verified mis-citation. Low D5 band 1-2; choose 2 because internal claim mapping exists, but no conclusion is externally traceable.

<details><summary>V0.4理由与本行变化背景</summary>

1–2档：evidence_registry三条来源全为INTERNAL_KNOWLEDGE_ONLY，无DOI/数据库条目/计算记录可定位；全部决策相关组(CG01/02/03/05/07/08/09)与性状组均为MISSING_SOURCE。按P34 MISSING_SOURCE属低分档、默认不cap。唯一经E0核验者仅CG07身份(TaxID 303=P. putida, SUPPORTED)，但答案自身来源仍缺失，且SUPPORTING不能上调档。无经核实错引，severity=NOT_APPLICABLE，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows the answer&#x27;s actual delivered source records: INTERNAL_KNOWLEDGE_ONLY with no external locator; does not support traceability to database or literature.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> The answer explicitly states oxygen is unspecified, flags kinase/isomerase EC and strain attribution as low-confidence, and labels L-erythrulose formation as inferred. Many traits are null/unknown rather than fabricated high-confidence. Some generic P. putida traits are still low-confidence internal claims without raw text, so 7-8 band, choose 7.

<details><summary>V0.4理由与本行变化背景</summary>

5–6档偏上：答案有明显不确定性披露（uncertainties列出氧条件未指定、下游酶EC/底物立体化学/菌株归属证据不足、L-erythrulose生成系推断），多项未知如实填null，置信度多为low/unknown，属诚实。但F7/F8/F9把D-苏糖醇利用/降解/酶活作为值填出（仅low），S1 EC以medium包装无来源，部分结论强度略超依据、证据类型未逐项标注观测/预测，属单点式过度确信而非系统性误导，档内取6不cap。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit uncertainty disclosures: oxygen unspecified, EC/stereo/attribution limits, and inference for L-erythrulose formation.

</details>

## Grok

答案SHA256：`735c09cd6051362e10697b201d7c89ed48ee000a87a76c87218ee37217518f94`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 falls in the 3–4 band: only the pathway sketch is delivered; all enzyme, microorganism, and 15-trait modules are absent, and the chemical route also departs from the gold D-threitol degradation main chain. Within-band score 3 because the pathway module is recognizable but core required deliverables are missing.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows required enzyme, microorganism, and trait modules are not delivered; does not by itself prove any particular enzyme is scientifically impossible.
- QUESTION_TEXT / QUESTION：Establishes required deliverables; does not establish answer correctness.

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 falls in the 3–4 band, upper part: the three-step sequence is internally continuous and roughly atom-accounting coherent, but core target transformations are wrong relative to the specified D-threitol degradation route: S1 gives L-erythrulose instead of D-erythrulose, S2 gives L-erythrulose 1-phosphate instead of D-erythrulose 4-phosphate, and S3 yields DHAP plus formaldehyde instead of D-erythrose 4-phosphate. Cofactors are also omitted, but the principal issue is multiple core transformation mismatches.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the delivered transformations and stereochemical claims; does not establish their correctness.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：Establishes the gold step substrates, products, and orientation; does not by itself prove every alternative route is chemically impossible.

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> C04 whole-module MISSING: all three steps have enzyme=null and no enzyme name or EC anywhere. The release contract records M=3/3 with the entire enzyme module not delivered, so D3a is MISSING and fixed at 1, not a scientific error score.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Establishes that no enzyme name or EC was delivered; does not establish any enzyme-reaction correctness.

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer delivers no microorganism module: every step has microorganism=null and organism_profiles is empty. Under the task requirement for one corresponding microorganism per step, this is D3b MISSING=1, not a scientific contradiction.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Establishes absence of species/strain identity and capability claims; does not establish any identity correctness.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Because organism_profiles is empty, the answer provides none of the required 15 traits. Under the missing-traits rule, D4 is MISSING=1; this does not claim the answer made a positive trait error.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Establishes that no 15-trait block is delivered; does not establish any trait value as correct or incorrect.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 falls in the 1–2 band: the evidence_registry contains only MODEL_INFERENCE entries with null database, record_id, and locator, and the answer itself states no database route was located. Decision-relevant route/enzyme claims are therefore MISSING_SOURCE. There is no verified mis-citation and no D5 cap, but traceability is almost absent.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows source_type=MODEL_INFERENCE with null database/record/locator and explicit statement that no database route was located; does not create a locatable external source.

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 falls in the 9–10 band: the answer explicitly labels the route as low-confidence model inference, states that no database route was located, records unknown enzymes/EC/microorganisms, lists alternative first-step chemistry and EC 4.1.2.2 mismatch, and does not present prediction as observation. Minor room remains because the route is speculative, but uncertainty disclosure is strong and proportionate.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows explicit low-confidence labeling, unknown declarations, alternative-route discussion, and EC mismatch disclosure.
- RUBRIC_CLAUSE / RUBRIC：Supports the D6 banding approach; does not add scientific evidence for the route itself.

</details>

## GPT5.6

答案SHA256：`5812026d28b5dc951a2fc1339e001e1e438eae7e5e5d007bf319ae0323d1f178`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 档位&#91;1,2&#93;：必答3步主链仅交付1步（S1 D-Threitol→D-Threose），参考S01/S03完全未给出；15项性状仅F5有值、14项显式null；route_scope.chosen_route_name与题面一致。核心模块大部缺失，但单步/单菌结构尚可辨认且未知标注明确，故取档内上沿2。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / 5adb26d4ab7e6b3d6407b24b245d0b3c9422a4b425daae15da878949aeddf119：题面要求给出指定路线主链逐步底物/产物/酶/EC/菌，并填15项性状；仅用于任务范围，不评价化学。
- ANSWER_TEXT / 5812026d28b5dc951a2fc1339e001e1e438eae7e5e5d007bf319ae0323d1f178：仅证明原答实际交付1步与1项性状，不外推其正确性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_127：本案主链为3步；不表示需要覆盖全部旁支，也不证明答案其他内容错误。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 只交付了一步D-Threitol氧化为D-Threose，方向为氧化且主有机转化在简化式上可成立；但该步未列NAD+/NADH等氧化还原辅因子，且产物D-Threose与gold的D-Erythrulose处于表示/互变异构待核状态，不能确认等价。更关键的是缺少通往D-erythrose 4-phosphate的后续关键中间体与步骤连接，无法构成完整主链；按TABLE0属主干部分成立但关键中间体、转化与连续性仍需实质补足，取5–6档下沿。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：gold主链含S02 D-Threitol→D-Erythrulose、S01 D-Erythrulose→D-erythrulose 4-phosphate、S03→D-erythrose 4-phosphate；S02含NAD+→NADH/H+辅因子。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案仅给出一个氧化步D-Threitol→D-Threose，未给下游两步，也未列NAD+/NADH。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_127：本题gold终点为D-erythrose 4-phosphate(2-)，答案未到达该终点。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 目标步事实：S01缺步=M，S03缺步=M，S02为ROUTE_HOLD_REPRESENTATION/UNRESOLVED=U；故S=0、M=2、U=1、N=3，C=S/N=0，落入C&lt;0.20的&#91;1,2&#93;带。答案仅S1给出D-threitol dehydrogenase名称，与S02目标酶名有局部关联，但EC 1.1.1.28与accepted 1.1.1.403的配对未获确认，产物D-Threose与gold D-Erythrulose仍属表示待核；S01的D-erythrulose kinase与S03的D-erythrulose 4-phosphate isomerase均未交付，含KEY终点缺失，主酶推荐不可用。故取2而非1，但不进入更高档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_127：gold必答酶含D-erythrulose kinase 2.7.1.210、D-threitol dehydrogenase 1.1.1.403、D-erythrulose 4-phosphate isomerase 5.3.1.34；答案仅给D-threitol dehydrogenase且EC为1.1.1.28。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：gold三步反应中S02产物为D-Erythrulose，答案S1产物为D-Threose；S01与S03反应未在答案中交付。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案只有一步，含D-threitol dehydrogenase/EC 1.1.1.28和D-Threose产物；无S01/S03。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_127：gold S02为D-Threitol→D-Erythrulose，而答案产物为D-Threose；该差异在当前材料中登记为表示待核而非已证伪。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 档位&#91;5,6&#93;：单步只给1个菌（Pseudomonas sp. ATCC 14676），属合理候选，但无TaxID/基因组号，唯一来源EVID_002无数据库/记录号/DOI；冻结快照无该菌株条目（E0仅为P. putida mt-2记录与P. putida种级），身份与步级催化能力均未核验。无已核实物种错配、无单步→整路外推，故不cap，未核取低端5。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：P. putida mt-2 PaW1菌株记录（ATCC 33015等）；不支持ATCC 14676身份或能力。
- E0_EVIDENCE / f3e0:taxid:303：P. putida种级分类记录；种级不覆盖菌株级身份。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_127：参考步级菌（含M. smegmatis）；为参考记录，不据此判定其他菌必错。
- ANSWER_TEXT / 5812026d28b5dc951a2fc1339e001e1e438eae7e5e5d007bf319ae0323d1f178：仅证明所交付菌名/菌株与低置信标签。

</details>

### D4 性状科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 档位&#91;3,4&#93;：15项性状仅F5（ATCC 14676）有值，与自报菌株自洽但无冻结记录可核（E0无ATCC 14676；bacdive 12880为P. putida mt-2）；温度/pH/盐度/氧/碳源/酶活/基因组等关键性状全为null。缺项完成度归D1，D4按已给内容与关键缺口评定；无已核错数值、无跨株外推、无编造，取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_127：参考性状仅覆盖M. smegmatis/B. abortus/A. radiobacter/P. atrosepticum；不提供ATCC 14676任何性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_127：标明各菌各性状可评分性；本案答案菌株不在其中。
- ANSWER_TEXT / 5812026d28b5dc951a2fc1339e001e1e438eae7e5e5d007bf319ae0323d1f178：仅证明交付状态与自洽性，不证明保藏号真实。

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 档位&#91;3–4&#93;：决策相关组（CG01/02/03/05/07/08）均无可核对条目级证据。EVID_001为BRENDA EC条目指针（record_id=&#x27;EC 1.1.1.28&#x27;）但快照无内容→UNRESOLVED_SOURCE；EVID_002无database/record_id/DOI→MISSING_SOURCE；终点与S01/S03无来源。无任何已核实错引→不cap；claim映射关系尚明确、无虚构迹象，取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：仅P. putida mt-2菌株记录；不支持ATCC 14676、EC 1.1.1.28或D-threose转化。
- E0_EVIDENCE / f3e0:taxid:303：仅P. putida种级分类；不支持任何菌株级或反应级声称。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_127：accepted S02 EC=1.1.1.403；仅证参考号，不据此判1.1.1.28为虚构。
- ANSWER_TEXT / 5812026d28b5dc951a2fc1339e001e1e438eae7e5e5d007bf319ae0323d1f178：仅证明原交付来源记录形态（无DOI/无记录号）。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 档位&#91;7,8&#93;：下游未知、缺证据、null与unknown标注具体，uncertainties两条明确，置信多为low/unknown；但把无可定位标识的EVID_002标为LITERATURE_DIRECT，route_summary用&#x27;已知主反应&#x27;表述未核实转化，属单点过度确信（非系统性误导、无掩盖矛盾），档内取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 5812026d28b5dc951a2fc1339e001e1e438eae7e5e5d007bf319ae0323d1f178：仅证明披露文本与标签；不证明其来源真实。
- QUESTION_TEXT / 5adb26d4ab7e6b3d6407b24b245d0b3c9422a4b425daae15da878949aeddf119：题面规定未知填null并区分证据性质，作为D6披露口径。

</details>
