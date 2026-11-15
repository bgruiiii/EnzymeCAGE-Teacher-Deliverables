# BIOPATH150_109：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：sulfoquinovose degradation I

污染物：6-sulfo-alpha-D-quinovose；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 51 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 39.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 62.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 40 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 61.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 43 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`73c5f8b74c6dd8510ac1ce4fe35f77d973640aae4ca6c091f1823fd27cf2a00f`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 主模块均有涉及（4步路径、酶、菌、15项性状、来源与不确定性），但gold必答5步中缺S05且末端/终点不符，属若干必要内容遗漏；按D1&#91;1,6&#93;给5。

<details><summary>V0.4理由与本行变化背景</summary>

六个交付模块均有实质内容：4步主链（每步底物/产物英文名+SMILES、首选酶、对应微生物）、单一16S之外的身份字段（菌名/菌株/TaxID/ORGANISM_PROFILE_ID）、15项性状全填、evidence_registry与uncertainties齐备；route_scope.chosen_route_name逐字填写为sulfoquinovose degradation I，JSON完整可解析。扣分点：四步酶的ec_number全部为null（字段合规但EC内容未交付），且省略gold的入口变旋步（sulfoquinovose mutarotase，EC 5.1.3.43），属少量遗漏与工程性缺项，入7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面指定sulfoquinovose degradation I、要求主链、首选酶及EC、对应微生物与15项性状。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_109：gold ordered_step_count=5、n_required=5；仅用于完整性对照，不把全DAG旁支当分母。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> S1-S3化学连接大体成立，但首步跳过alpha→beta变旋，末端以脱氢氧化生成sulfolactate替代gold还原生成DHPS，主链终点方向错误；按D2&#91;1,4&#93;且关键错误Y给3。

<details><summary>V0.4理由与本行变化背景</summary>

前三个转化与gold主链化学一致：S1 sulfoquinovose异构化为6-脱氧-6-磺基-D-果糖（醛酮异构化）；S2 ATP依赖磷酸化生成1-磷酸并显式列出ATP/ADP；S3醛缩酶裂解为DHAP+(2S)-3-磺乳乙醛，与gold BSY-r03029产物一致，方向与连接成立。末端第4步写成(S)-磺乳乙醛经脱氢酶氧化为(S)-磺乳酸，而gold BSY-r02372为3-磺乳乙醛还原酶（EC 1.1.1.373/1.1.1.61）催化还原生成(S)-2,3-dihydroxypropane-1-sulfonate（BSY-c16235），产物与氧化还原方向不符；另入口α/β变旋步被并入第1步（未单列，属少量）。因题面只给路线名（未指定终点化合物），答案已在alternative_branches中声明DHPS分支且标is_part_of_scored_main_route=false，并在uncertainties中披露yihU方向与产物不确定，按四.5四步判断作档内扣分（主干成立、关键末端转化需修订）取5–6档之6，未达“反应方向反转/主链第一步即错”类关键错误门槛，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：gold S02为REVERSED_TO_COMPLETE_NAME，主产物(S)-DHPS；S05为alpha-SQ→beta-SQ mutarotase；支持末端还原与入口变旋，不扩展到其他性状。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_109：gold terminal compound为(S)-2,3-dihydroxypropane-1-sulfonate，不是sulfolactate。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> S2 kinase、S3 aldolase与accepted集相符；S1 isomerase底物alpha与gold beta不符；S4 dehydrogenase与gold reductase方向/产物冲突；S05 mutarotase未交付。确认KEY失败/缺失触发D-KEY4≤4，2/5可用且边界清楚，给3。

<details><summary>V0.4理由与本行变化背景</summary>

S1 sulfoquinovose isomerase（yihS）由冻结E0 EC 5.3.1.31的accepted name（含sulfoquinovose isomerase、yihS gene name）与reaction（β-sulfoquinovose=6-deoxy-6-sulfo-D-fructose）正向支持；S2 6-sulfofructose kinase（yihV）、S3 6-sulfofructose-1-phosphate aldolase（yihR）与gold酶名（EC 2.7.1.184、4.1.2.57）一致；S4把yihU写成“(S)-sulfolactaldehyde dehydrogenase”催化醛→羧酸氧化，与gold 3-sulfolactaldehyde reductase（EC 1.1.1.373/1.1.1.61，醇脱氢方向）功能不符，属一处酶功能/方向错误。四步EC均未提交（任务明示未知填null，故不判编造，仅降低可核性）。主要步骤酶对应有支持但一处功能错误+EC层完全未交付，入5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：列出S01-S05 accepted酶名与EC类别；支持S01/S03功能匹配，并显示S02为reductase、S05为mutarotase；不证明具体蛋白实验活性。
- E0_EVIDENCE / f3e0:ec:5.3.1.31：官方EC 5.3.1.31反应底物为beta-sulfoquinovose；不能支持答案以alpha-SQ为直接底物的声称。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：S02主产物为DHPS，S04底物为beta-SQ，S05为alpha→beta；支持S02/S04/S05目标状态。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> E. coli物种及全路径能力有gold PATHWAY_COMPLETE支持；K-12菌株级TaxID 83333未在E0核验，按物种级支持菌株级声称的粒度不足处理，7分档，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

四步均归属Escherichia coli（K-12），与gold organism_gold中S01–S04的Escherichia coli(562)一致，且gold PATHWAY_COMPLETE行为taxid 562、pathway_complete=TRUE，支持“E. coli可完成整条硫糖酵解”的物种级能力声称；答案另给出菌株K-12与TaxID 83333，其菌株级身份在冻结E0中无记录（GAP-109-014/017），按四.6不凭记忆放行、保持UNRESOLVED。按八.D3b身份阶梯①（物种级真实记录支持菌株级声称，粒度不足）档内扣分、通常7档附近，不cap；身份定位、反应级能力、完整路径能力三层已分别核对，未把单步酶存在写成全路径能力。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_109：多个步骤匹配Escherichia coli taxid 562，且PATHWAY_COMPLETE行E. coli 562 pathway_complete=TRUE；未提供K-12 taxid 83333的菌株级记录。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 15项均填写；E. coli主要性状（F1/F10/F11/F12/F13等）与gold同物种代表记录一致；F2最大值45超出gold观测上限41、F5/F14为未核菌株级记录，属少量数值/粒度问题，7分档。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部交付（filled=15，无遗漏），且多项与gold观测记录一致：运动性true、细胞形态rod-shaped、革兰氏阳性false（即阴性）、sporulation=false、兼性厌氧/耐氧、盐度preference=non-halophilic；数值型不确定项以null+类别描述处理，未出现“填满字段换取印象分”的编造模式，置信度多标medium/low。需核项：F2最高温45°C高于gold观测最高温区间35–41°C（但F2 min/max子字段在trait_subfield_scoreability_mask中为pending_teacher_adjudication，且观测区间≠生物学耐受极限）、F5保藏号ATCC 10798与gold物种记录DSM 4599不同（同物种可有多个保藏号，四.4不因代表记录不同判错）、F14 NC_000913与gold GCA_003018455.1为不同菌株/登录号且E0无记录。综合“主要性状可核实且适用于所指对象，仅少量条件或数值问题”，入7–8档取7；未发现“预测值冒充观测值”或“物种级观测推广到所有菌株”的系统性问题。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_109：E. coli 562的F1 aerotolerant/facultative anaerobe、F10 motility、F11 rod、F12 gram negative、F13 sporulation false、F7/F8/F9/F14等观测/预测行；物种级代表记录不保证所有菌株数值相同。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_109：标明F2 maximum/minimum等子字段对E. coli 562待老师裁决；支持不把未决子字段当作已核实错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_109：F2 min/max、F5、F14等子字段的评分/待核状态；支持D4局部未核说明。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 核心路线引具体Denger等2014文献但E0无法解析核验（UNRESOLVED_SOURCE）；多数性状仅INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；无已核实错引，部分关键结论可定位而其他缺映射，5分档。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组（CG01/CG02/CG03/CG05/CG07/CG09为CORE，CG08为APPLICATION_CRITICAL，CG14中“以SQ为唯一碳源”按claim-level承担目标污染物能力论证）的来源只有EVID_001一条按记忆引用的自由文本文献（Denger et al., Nature 2014，无DOI/卷期/record_id），冻结E0将其登记为GAP-109-006（自由文本未解析成可查询标识符），引用-声称链无法核对→UNRESOLVED_SOURCE（不判虚构、不判CONTRADICTED）；性状与路线识别来源EVID_002/EVID_003为INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE。全案无条目级可定位可核对来源，也无经核实的错引（不触发cap）。按四.3合成规则：决策相关组无条目级证据、来源可追查性处于缺失/待核档，取4（EVID_001确给出作者/刊名/年份线索且claim_scope映射结构清楚，故不压到最低）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示EVID_001为具体文献但无DOI/卷页；EVID_002为INTERNAL_KNOWLEDGE_ONLY；未见已核实虚构引用。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案逐项说明路线识别、末端方向、EC、SMILES立体、菌株和性状来源限制，未知/null与结论边界清楚；个别步置信度偏高但不构成系统性误导，8分档。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties逐条给出6类具体限制：路线名依赖知识判定未核数据库、S4末端产物与yihU方向/辅因子未定、四酶EC均未确认、SMILES不含立体化学、K-12亚株与F14登录号可能不一致、全部性状为教科书级未逐条核对；alternative_branches把DHPS分支标为is_part_of_scored_main_route=false，清楚区分观测/记忆/推断；置信度总体与证据相称（内部知识来源标low/medium，未用high包装未核实性状）。不足：S4末端产物虽标medium并在uncertainties中说明，但在主链正文以陈述句给出，属单点表述强度偏高，未达“系统性把预测写成实证”或“掩盖已知矛盾”，入7–8档取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：记录答案对路线识别、S4方向/辅因子、EC缺失、SMILES立体、菌株亚株和性状来源的披露。

</details>

## DeepSeek

答案SHA256：`fa0b1f272512d1a5aebd9c8b54563d27072a6b1097637063dc79d7ccdcb2d010`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> Form is complete (5 steps, organism, 15 traits), but the specified main route is not delivered: the answer ends at pyruvate + sulfite instead of the gold terminal (S)-2,3-dihydroxypropane-1-sulfonate and omits the S05 mutarotase entry. This is a D1 task/route deviation; cap 4.

<details><summary>V0.4理由与本行变化背景</summary>

模块与字段基本齐备：5 步均给出主底物/主产物英文名与 SMILES、一个酶、一个菌，15 项性状全槽位回应，JSON 可解析，菌按物种+菌株去重为 1 条 profile；若只看完整性约 5–6 档。但任务参数偏离成立（P100：自称合规却交付不同化学路线）：route_scope.chosen_route_name 声称 sulfoquinovose degradation I，而 S4–S5 交付的是 3-sulfolactaldehyde 氧化/脱磺酸支路（→3-sulfolactate→pyruvate+sulfite），alternative_branches 为空、无范围声明（RE-01）。另有全部 5 步 enzyme.ec_number 均为 null、不满足题面&#x27;一个首选酶及EC&#x27;的明确字段要求，以及缺 α→β mutarotase 起始步。按本维关键错误封顶 4，档内取 4（其余字段齐备、菌与前三步化学与 gold 一致，问题集中在路线符合度）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：Task locks route name sulfoquinovose degradation I and requires the main route.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_109：Gold terminal product is (S)-2,3-dihydroxypropane-1-sulfonate.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Gold S02 is the terminal reductive step to (S)-2,3-dihydroxypropane-1-sulfonate; S05 is alpha-&gt;beta mutarotase.
- ANSWER_TEXT / ANSWER：Answer route_summary and S4/S5 end at 3-sulfolactate, pyruvate and sulfite; S1 directly isomerizes alpha-quinovose.

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> The answer gives a coherent alternative sulfoglycolytic sequence, but against the specified route it has multiple important step/direction mismatches: S4 oxidizes 3-sulfolactaldehyde to 3-sulfolactate instead of reducing it to DHPS, S5 desulfonates to pyruvate/sulfite instead of ending at DHPS, and S1 bypasses the S05 mutarotase. This is a 3-4 band with key direction/terminal failure; score 4 because the local chemistry is otherwise readable.

<details><summary>V0.4理由与本行变化背景</summary>

主链前三步与 gold 化学一致：异构化（对应 gold S04）→磷酸化（gold S01）→醛缩裂解生成 DHAP+3-sulfolactaldehyde（gold S03，DHAP 在 gold 中为 byproduct 角色，答案亦按主产物列出但化学连接正确）。问题在于：(1) S1 直接以 α-端基异构体作为 sulfoquinovose isomerase 底物，缺 gold S05 的 α→β mutarotase，且 E0 官方 5.3.1.31 反应底物为 β-sulfoquinovose（RE-02）；(2) S4 把 gold S02 的还原（3-sulfolactaldehyde→(S)-2,3-dihydroxypropane-1-sulfonate）改为氧化生成 3-sulfolactate；(3) S5 再脱磺酸得 pyruvate+sulfite，使终点与指定路线不一致且未声明替代分支、无任何可核证据。按四.5 四步判断：题面已指定路线→无替代声明→cap 候选→偏离使&#x27;主链即该路线主链&#x27;的结论失效。落 3–4 档并封顶 4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Gold S02 is reductive to DHPS; S05 is alpha-&gt;beta mutarotase; S04 substrate is beta-quinovose.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：Gold S02 uses 3-sulfolactaldehyde reductase; S05 uses sulfoquinovose mutarotase.
- ANSWER_TEXT / ANSWER：Answer S4 uses dehydrogenase to 3-sulfolactate; S5 produces pyruvate + sulfite; S1 starts from alpha-quinovose.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> Of 5 required targets, S01 kinase and S03 aldolase are functionally supported by accepted names; S02 is a confirmed KEY terminal mismatch (dehydrogenase oxidation to 3-sulfolactate vs reductase to DHPS); S04 is a substrate mismatch (alpha vs beta) and S05 is missing. S=2, F=2, M=1; coverage 0.4 -&gt; &#91;3,4&#93;, with D-KEY4 cap. Score 3 because two key route endpoints fail and only two targets are usable.

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3 酶名与 gold 对应酶名/功能基本一致（sulfoquinovose isomerase / 6-sulfo-D-fructose 1-kinase≈6-deoxy-6-sulfofructose kinase / 6-sulfo-D-fructose 1-phosphate aldolase≈6-deoxy-6-sulfofructose-1-phosphate aldolase），S1 酶名与 E0 5.3.1.31 accepted name 一致；但全部 5 步 EC 为 null，无法按四.6 核对 accepted name/reaction/条目状态；S1 所配底物与官方 β-sulfoquinovose 反应不符（RE-02）；S4 用 &#x27;3-sulfolactaldehyde dehydrogenase&#x27;，与 gold 同节点 &#x27;3-sulfolactaldehyde reductase&#x27;（EC 1.1.1.373/1.1.1.61）功能方向相反；S5 &#x27;3-sulfolactate desulfonase&#x27; 无任何冻结证据。属&#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;—5 档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：Accepted targets: S01 kinase EC 2.7.1.184; S02 reductase EC 1.1.1.373/1.1.1.61; S03 aldolase EC 4.1.2.57; S04 isomerase EC 5.3.1.31; S05 mutarotase EC 5.1.3.43.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Gold S02 produces DHPS; S05 alpha-&gt;beta; S04 beta-quinovose -&gt; fructose.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Official EC 5.3.1.31 reaction uses beta-sulfoquinovose, not alpha-quinovose.
- ANSWER_TEXT / ANSWER：Answer enzyme names/reactions for S1-S5 and absent EC/mutarotase.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> E. coli is species-level supported for S01-S04 and PATHWAY_COMPLETE by organism_gold, but the answer claims K-12 MG1655 (TaxID 511145, NC_000913.3) and complete pathway for that strain; the gold record is E. coli 562/GCA_003018455.1 and S05 is Clostridium. Species-level support does not verify strain-level capability; no key error, but identity/range granularity is 5-6. Score 5.

<details><summary>V0.4理由与本行变化背景</summary>

gold organism_gold 以物种级 E. coli（TaxID 562，GCA_003018455.1）作为 S01/S02/S03/S04 四步的对应菌，并有 PATHWAY_COMPLETE 行（pathway_complete=TRUE），因此&#x27;该路径由 E. coli 承担&#x27;方向正确且身份主体无错；答案以单一 profile（E. coli K-12 MG1655，TaxID 511145）覆盖全部 5 步，属物种级真实记录支持菌株级声称（P107①：档内扣、默认不 cap），TaxID 511145 在 E0 无冻结记录（GAP-109-012/015）故菌株级身份保持 UNRESOLVED；S5 脱磺酸酶归属 E. coli 无任何步级证据；complete_pathway_organism_profile_id=ORG_001 的整路径能力声称在物种级有 gold 支持，但被用于其氧化-脱磺酸支路，支持范围不能外推。取 6 档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_109：Gold step organisms are E. coli 562 for S01-S04 and Clostridium sp. MSTE9 for S05; PATHWAY_COMPLETE is E. coli 562/GCA_003018455.1, not K-12 MG1655.
- ANSWER_TEXT / ANSWER：Answer uses E. coli K-12 MG1655/TaxID 511145 for all steps and claims ORG_001 complete pathway.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> Generic E. coli traits (motility, rod, Gram-negative, non-spore-forming, facultative anaerobic) are supported, but several strain-specific traits and genome/ATCC values are not verified against the E. coli 562 gold; F4 is honest null; F2/F3 endpoints are partly pending and some values exceed gold ranges. No key error; 5-6 band, score 6 because many core traits are correct.

<details><summary>V0.4理由与本行变化背景</summary>

F1 兼性厌氧、F10 周生鞭毛运动、F11 杆状、F12 Gram-negative、F13 不产孢与 gold 物种级观测方向一致；F2 preference &#x27;嗜温&#x27; 与 gold mesophilic 一致；F4 整体 null 属诚实未知（P112：缺失完成度主归 D1，D4 不重复重扣）。存疑项：F2 maximum 45 略高于 gold 观测区间 35–41、minimum 20 落在 gold 4–35 内、optimum 37 无 gold 对应子字段；F3 minimum 5.5 略低于 gold 6.0–7.0——这两个子字段在 trait_subfield_scoreability_mask 中标记 pending_teacher_adjudication，故只登记不据此单独判错。F5 ATCC 47076、F14 NC_000913.3/4641652 bp/50.8% 在 E0 无记录（GAP）待核；F7/F8/F9 关于 sulfoquinovose 利用与&#x27;硫代糖酵解酶（含 dehydrogenase、desulfonase）&#x27;的酶活描述属无来源的物种/菌株级外推；全部 raw_text 为 null，无法复核原值。属&#x27;部分性状准确且适用，但关键项证据不足或条件解释需修订&#x27;—取 6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_109：Gold species-level E. coli 562 traits support motility, rod-shaped, Gram-negative, non-spore-forming, facultative anaerobic; temperature/pH ranges partly differ.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_109：Some E. coli trait fields are completeness-only or pending, limiting accuracy scoring.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_109：E. coli F2/F3/F4 endpoint subfields are partly pending teacher adjudication.
- ANSWER_TEXT / ANSWER：Answer K-12 MG1655 trait values.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> All evidence_registry entries are INTERNAL_KNOWLEDGE_ONLY with no database, record_id, or locator; no pathway, enzyme, microorganism, or trait claim can be traced to a locatable source. D5 1-2; score 1.

<details><summary>V0.4理由与本行变化背景</summary>

全部 evidence_registry 条目 source_type=INTERNAL_KNOWLEDGE_ONLY 且 database/record_id/locator 全为 null，claim_scope 只是内部范围描述；路径、酶、菌、性状四类结论无一条可定位到数据库条目、文献或计算记录，也无 raw_text 可回查。按六状态逐组登记为 MISSING_SOURCE（缺失而非误导，默认不触发关键错误）；决策相关组（CG01/CG02/CG03/CG05/CG07/CG09 等）不存在任何条目级可定位可核对证据，落入 1–2 档，取 2（答案对未知 EC 有诚实说明，略优于完全零披露）。无已核实错引，severity 不适用。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：All three evidence registry entries have source_type INTERNAL_KNOWLEDGE_ONLY and null database/record_id/locator.

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> The answer lists EC and stereochemistry uncertainty and labels evidence as internal-only, but gives high confidence to K-12 identity/traits and presents the pyruvate/sulfite route as the named route without disclosing the terminal/strain limitations. Some uncertainty disclosure, but major limitations are not clearly bounded; 5-6 band, score 5.

<details><summary>V0.4理由与本行变化背景</summary>

正面：答案给出 uncertainties 两条（EC 未确认、中间体立体化学不确定），并把来源类型显式标为 INTERNAL_KNOWLEDGE_ONLY，F4 以 null 表示未知，属部分诚实披露。负面：F1/F6/F11/F12/F13/F14 及微生物身份在多处以 high 置信包装无来源内容、raw_text 全为 null，confidence 与证据强度明显不相称；未披露菌株级身份（TaxID 511145、ATCC 47076）未核；更关键的是未披露 S4–S5 支路与指定路线终点不一致这一主要限制，也未把&#x27;该路线终点应为 DHPS&#x27;列为待验证点。属&#x27;多处过度确信，证据类型混淆，主要限制未说明&#x27;（3–4 档），取 4；未见系统性把预测写成实测观测或明知掩盖矛盾，故不 cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Answer uncertainties and confidence labels; route_summary asserts the route without disclosing terminal/strain limitations.

</details>

## Kimi

答案SHA256：`70863d69bcd499a657b3b6b60157bea782c52d30a0170a505ea31b65d9f0bdd0`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 答案给出指定路线名、4个步骤的底物/产物/酶/菌、15项性状及来源登记，主模块均有涉及；但5个必答步中缺S05 sulfoquinovose mutarotase入口步，且S2–S4的EC为null，属若干必要内容遗漏。按D1 5–6档取6：主要模块覆盖，但完整性与关联需实质修订。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的模块均实质交付：4步主链逐步给出底物/产物英文名与SMILES、绑定酶（含ec_number字段，未知处按题面要求填null）、绑定微生物，并按物种+菌株去重为ORG_001；route_scope.chosen_route_name逐字填写sulfoquinovose degradation I；15项性状一次给全且逐项带raw_text/evidence_id/confidence；evidence_registry 5条并带claim_scope。缺gold S05的α→β mutarotase一步（答案在uncertainties中明确声明未单列），属少量遗漏且关联清楚，落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_109：证明本题ordered_step_count=5，必答主链含5步；不证明答案已交付全部5步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：证明S05为sulfoquinovose mutarotase入口步，答案未给对应步骤。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> S1异构、S2 ATP依赖磷酸化、S3 retro-aldol裂解、S4 NADH依赖还原的方向与产物与sulfo-EMP主链一致，辅因子ATP/ADP、NADH/NAD+已列明，终点(S)-2,3-dihydroxypropane-1-sulfonate正确；缺S05 mutarotase使入口连接需修订，S02存在表示层面电荷/立体边界，但主链化学连续、局部问题不改主要结论。按7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

四步化学与gold方向一致：S1醛糖-酮糖异构化（α-quinovose→6-sulfo-D-fructose，开链SMILES与gold的6-deoxy-6-sulfo-D-fructose等价）；S2 ATP依赖磷酸化生成1-磷酸并并列ATP/ADP；S3 retro-aldol裂解生成glycerone phosphate与(3S)-sulfolactaldehyde；S4 NADH依赖还原生成(S)-2,3-dihydroxypropane-1-sulfonate，终点与gold terminal逐字一致，未越界延伸到下游。局部问题：省略α→β mutarotase一步（已声明）、S1以α-异头体直接作异构酶底物（官方5.3.1.31反应底物为β-sulfoquinovose）、H+等小离子未列；均不改变主链与终点结论，7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：支持S01–S05的反应方向、主产物与辅因子角色；不证明答案已覆盖S05。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_109：支持本题终点为(S)-2,3-dihydroxypropane-1-sulfonate；不扩展到下游。

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> S01激酶、S02还原酶、S03醛缩酶的功能名与accepted G4相符；但S05 KEY入口步未交付，且S04将sulfoquinovose isomerase配EC 5.3.1.34，而E0记录5.3.1.34为D-erythrulose 4-phosphate isomerase，5.3.1.31才是sulfoquinovose isomerase。按D-KEY4/关键入口缺失及显式EC错配上界4；可用部分清楚，取4。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶的命名与功能链条（sulfoquinovose isomerase/yihS、sulfofructose kinase/yihV、sulfofructose-1-phosphate aldolase/yihT、sulfolactaldehyde reductase/yihU）与sulfoglycolysis文献路线一致，S2–S4对未知EC诚实填null。但S1把sulfoquinovose isomerase标注为EC 5.3.1.34并confidence=high：冻结官方条目5.3.1.34的accepted name为D-erythrulose 4-phosphate isomerase（eryI），reaction为D-erythrulose-4-phosphate = D-erythrose 4-phosphate；同快照5.3.1.31才是sulfoquinovose isomerase/yihS。酶名与EC互相矛盾，落入八.D3a关键错误最低清单，按四.5/P66官方支持gold→按错误处理，cap≤4；因S1名称、基因与功能本身正确且其余步骤未虚构，档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.31：E0记录5.3.1.31的accepted name为sulfoquinovose isomerase，支持该EC对应目标S04酶功能；不支持5.3.1.34。
- E0_EVIDENCE / f3e0:ec:5.3.1.34：E0记录5.3.1.34为D-erythrulose 4-phosphate isomerase，反应为D-erythrulose-4-phosphate异构化；不支持将其配给sulfoquinovose isomerase。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：支持S01/S02/S03/S04/S05的accepted酶名与EC；S05为sulfoquinovose mutarotase EC 5.1.3.43。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案4个已给步骤均归E. coli K-12 MG1655；gold organism_gold对S01/S02/S03/S04均有E. coli物种级EXACT行，且E. coli物种PATHWAY_COMPLETE=true。主要微生物对应可靠；但答案用菌株级K-12 MG1655/TaxID 511145，E0无该菌株级记录，属粒度不足档内扣。S05未给，不评其菌。按7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

全链统一归属Escherichia coli K-12 substr. MG1655（单一profile、四步复用同一条且已按物种+菌株去重），与gold步骤级归属中S01–S04均出现Escherichia coli（EXACT, 562）同物种一致；所选菌为sulfoglycolysis的经典研究对象，未见身份或作用范围错误。但gold与E0侧仅有物种级记录（562, GCA_003018455.1；PATHWAY_COMPLETE=TRUE），答案给出菌株级身份（MG1655、TaxID 511145）而未附同粒度条目，属八.D3b①“粒度不足”，档内扣分（7档附近）不cap；complete pathway声称有gold物种级PATHWAY_COMPLETE支持，不构成把单步支持写成全路径能力。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_109：支持E. coli物种级对S01/S02/S03/S04的EXACT归属及PATHWAY_COMPLETE；不支持K-12 MG1655菌株级TaxID 511145。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 15项性状齐全，多数E. coli性状与gold物种级记录一致（兼性厌氧、革兰阴性、杆状、不产孢、运动、pH中性、非嗜盐类别等）；但F2把ATCC propagation 37°C当作最适温度，gold最适子字段未观测；F5/F14菌株级记录未核；F15 gold为UNKNOWN而答案给值。关键条件解释需修订，按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部给出并与gold物种级可核项一致：F1兼性厌氧（gold aerotolerant=true、facultative anaerobe=true）、F11杆状、F12革兰氏阴性、F13不产孢、F10运动性（gold motility=true，答案以K-12驯化株hedge）均吻合；F4数值null但category“非嗜盐”与gold salinity preference=non-halophilic一致；F3 optimum 7落在gold pH growth 7.0–8.5附近并标low。局部问题：F2把ATCC繁殖温度37°C写成“最适”（培养温度≠最适，四.4/证据解释层），F5（ATCC 700926）与F14（U00096.3、4,641,652 bp、GC 50.8%）无冻结记录不可核但落在gold区间内且不矛盾。7–8档取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_109：支持E. coli物种级F1/F7/F10/F11/F12/F13等；F2有生长范围/偏好但最适子字段未观测；F5为DSM 4599；F15 UNKNOWN。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_109：标明E. coli F2 maximum/minimum待教师冻结、F3/F15 completeness_only；不支持把未评分字段当已核。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案交付了EVID_001–EVID_005及逐事实evidence_id，路线/酶/菌/性状有来源映射结构；但E0仅提供EC 5.3.1.31与5.3.1.34两条，ATCC 700926、TaxID 511145、U00096.3、PubMed DOI、EcoSal Plus均为gap或自由文本未解析，无法逐条核对。无已核VERIFIED_MIS_CITATION_*，不cap；部分关键结论可定位、其他仍UNRESOLVED，按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组（CG01/CG02/CG03/CG05/CG07/CG09）无一条目级结论可在冻结快照内核验——EVID_001只给MetaCyc/EcoCyc通路名且record_id=null，EVID_002给出DOI但快照未解析（GAP-109-007），TaxID 511145、ATCC 700926、U00096.3均无冻结记录；唯一可对照的EC 5.3.1.34与官方条目不符，但所引来源与该断言的引用-声称链未核，按P40保持UNRESOLVED_SOURCE、不判已核实错引、不cap。答案的逐step evidence_id映射与claim_scope结构清楚、非“只有库名/文献列表”，故不落3–4档笼统来源档；但核对未完成、无一条成功验证，按5档（部分关键结论可定位、核对未完成）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.31：E0可核的EC条目之一；不能外推到答案所列ATCC/GenBank/PubMed/EcoSal记录。
- E0_EVIDENCE / f3e0:ec:5.3.1.34：E0可核的另一EC条目；不覆盖其他来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> uncertainties明确列出氧条件null、异头体未单列、多个EC未填；confidence分级与null使用较诚实，未系统性把预测写成观测。但S1 sulfoquinovose isomerase EC 5.3.1.34标high，与E0另一酶记录冲突，属单点过度确信，档内扣至7。

<details><summary>V0.4理由与本行变化背景</summary>

披露总体具体且诚实：uncertainties列明氧条件null、未单列α/β mutarotase步、YihV/T/Y/U的专属EC不填以避免猜测、盐度/pH/运动性证据弱；低置信项明确标low；F15明确声明“该株为实验室参考株，不据此推断致病性”；证据类型分DATABASE_DIRECT与LITERATURE_DIRECT。但S1把未经核实且与官方条目矛盾的EC 5.3.1.34以confidence=high包装，并在uncertainties中称其为“较确定”，全程零披露——属八.D6/锚点SC6的单点过度确信（6档），非系统性把预测当实证、无明知掩盖证据，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.34：显示5.3.1.34为D-erythrulose 4-phosphate isomerase，用于判断S1 high confidence是否过度。

</details>

## Qwen

答案SHA256：`2afdc0f041f062a1cb9ba150b98697745a9abe0d77656536d2a06f28e9d89fb9`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> The answer returns a complete JSON object and uses the requested route name, but it does not deliver the specified main chain: it omits the gold S05 mutarotase step and replaces the gold S02 terminal reduction to (S)-2,3-dihydroxypropane-1-sulfonate with an oxidative sulfolactate branch to pyruvate/sulfite. This is a task-level route/endpoint deviation and caps D1 at 4.

<details><summary>V0.4理由与本行变化背景</summary>

路径（5步）、每步酶、每步微生物、15项性状、来源结构、不确定性说明各模块均有实质交付；route_scope.chosen_route_name原样填“sulfoquinovose degradation I”，符合题面指定路线；organism_profiles按同物种去重为单一ORG_001。属“大部分必要内容完整，关联清楚，仅少量遗漏”：2步（S3/S4）enzymes有名称但EC为null，性状仅3项有值其余诚实null，均为题面允许的未知/缺失表达，故为7档偏低端。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Gold S02 terminal product is (S)-2,3-dihydroxypropane-1-sulfonate; S05 is the alpha-to-beta mutarotase step. It does not support pyruvate/sulfite as the task terminal.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_109：Frozen terminal identity is (S)-2,3-dihydroxypropane-1-sulfonate.
- ANSWER_TEXT / ANSWER.steps S1-S5：The answer routes 3-sulfolactaldehyde to (R)-3-sulfolactate and then pyruvate/sulfite; it contains no mutarotase step.

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> The upstream isomerization, phosphorylation, and aldol cleavage are chemically coherent, but the terminal branch conflicts with the specified degradative direction: instead of reducing 3-sulfolactaldehyde to (S)-2,3-dihydroxypropane-1-sulfonate, the answer oxidizes it to (R)-3-sulfolactate and cleaves it to pyruvate/sulfite. Within the allowed D2 range &#91;1,4&#93;, this warrants 4 because the main chain is partly coherent but the terminal direction/connection is not the required one.

<details><summary>V0.4理由与本行变化背景</summary>

核心sulfo-EMP三步化学表达成立：S1异构化、S2 ATP依赖磷酸化、S3醛缩裂解生成3-磺基乳醛+DHAP，与gold前段化学一致，无方向反转、无原子明显不守恒。但S4/S5将3-磺基乳醛氧化为(R)-3-磺基乳酸再经sulfo-lyase裂解为pyruvate+sulfite，偏离gold该路线的3-磺基乳醛还原酶支路（终点(S)-2,3-二羟基丙烷-1-磺酸/DHPS），且答案未声明为替代支路、亦无可核证据，仅内部推断；同时略去α→β变旋步骤（把异构酶直接作用于α型）。属“主干部分成立，但关键转化/连接仍需修订、合理性证据有限”，取5档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Gold S03 produces (2S)-3-sulfolactaldehyde; gold S02 leads to (S)-2,3-dihydroxypropane-1-sulfonate. It does not support oxidation to (R)-3-sulfolactate followed by pyruvate/sulfite.
- ANSWER_TEXT / ANSWER.steps S3-S5：Shows NAD+-dependent oxidation of 3-sulfolactaldehyde and sulfo-lyase cleavage to pyruvate/sulfite, opposite to the gold terminal reduction direction.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> Target-by-target: S03 aldolase reaction is supported at accepted name/function level (S); S02 is failed because the answer substitutes oxidative sulfolactate formation for the required terminal reduction (F); S04 is failed/unsupported because the answer uses alpha-quinovose as substrate for sulfoquinovose isomerase while the official EC record specifies beta-sulfoquinovose (F); S05 mutarotase is missing (M); S01 kinase reaction matches but explicit EC 2.7.1.209 is not the accepted 2.7.1.184 and remains locally unresolved (U). With S=1/N=5 and confirmed KEY entry/terminal failures, D3a falls in &#91;3,4&#93; after the KEY4 cap; 3 is chosen because only one target reaction is cleanly supported and both KEY entry and terminal fail.

<details><summary>V0.4理由与本行变化背景</summary>

S1 sulfoquinovose isomerase/EC 5.3.1.31经E0核实accepted name一致（酶名-EC对应支持）；S3醛缩酶、S4脱氢酶名称与反应类型自洽但EC为null；S2标EC 2.7.1.209（gold为2.7.1.184，同属2.7.1转移酶类，具体号E0无记录不可核实）；S5 EC 4.4.1.29为真实sulfo-lyase类型但E0无记录。整体“有合理候选和部分支持，但若干关键步骤仍缺具体核验”，取6档；未见EC大类别与反应类型根本错配，故不判关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：Establishes accepted enzyme identities for the required steps; does not establish the answer&#x27;s alternative dehydrogenase/sulfo-lyase branch.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Establishes the required terminal reduction, aldol cleavage products, and alpha-to-beta mutarotase step.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Official EC record states beta-sulfoquinovose as substrate; it does not support alpha-sulfoquinovose as the direct substrate.

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The core microorganism identity is Escherichia coli TaxID 562, which is supported in gold for several required steps and as a PATHWAY_COMPLETE organism. However, the answer gives only species-level identity, and its alternative dehydrogenase/sulfo-lyase branch to pyruvate and its complete-pathway claim for that altered route are not independently supported. This is partial/plausible support rather than fully verified step-level and whole-route capability, so D3b is 6.

<details><summary>V0.4理由与本行变化背景</summary>

核心微生物推荐Escherichia coli/taxid 562在organism_gold中为EXACT匹配且PATHWAY_COMPLETE=TRUE，身份与整条路线菌选择有可靠支持，物种粒度为题面允许（未指定菌株可null）。但答案把全部5步均归给E. coli，其中S4(磺基乳醛脱氢酶)、S5((R)-磺基乳酸sulfo-lyase)并非E. coli的酶（E. coli该路线走还原酶至DHPS），属反应级能力的过度归属；complete_pathway_organism_profile_id=ORG_001虽在canonical路径上被gold支持，却与答案自选的sulfo-lyase支路自相矛盾。“主要微生物对应有可靠支持，但若干作用范围未充分核验”，取6档；未编造菌名/TaxID，非跨类群错配，不判关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_109：Supports E. coli species identity and a gold-route pathway-complete record; does not certify every alternative enzyme attribution in the answer or the pyruvate/sulfite terminal route.
- ANSWER_TEXT / ANSWER.organism_profiles ORG_001：Shows the answer&#x27;s species-level identity and whole-pathway claim.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> The answer returns all 15 trait fields, mostly as honest nulls, and the nulls are not treated as scientific errors. Among the filled traits, F9 partly overlaps gold-supported E. coli enzyme activities, but F7/F8/F9 are broad internal-knowledge claims with no direct trait record; F8 also asserts a sulfite-releasing degradation capacity not supported by the gold route. Some traits are plausible, but key items lack direct evidence or need revision, fitting 5-6; 5 is chosen because the filled traits are few and mostly unsupported.

<details><summary>V0.4理由与本行变化背景</summary>

15项中3项有值：F7(E. coli可利用SQ作碳/硫源)大体合理但无真实观测来源；F8声称E. coli“经sulfoquinovose degradation I释放亚硫酸盐”、F9声称E. coli具sulfo-lyase/磺基乳醛脱氢酶活性，均与gold中E. coli该路线还原产DHPS不符、并重复末端支路误归属，属把模型推断写成菌株性状且无观测支持。其余12项诚实null（完成度归D1，不在此重复扣）。已有值含明显不适用/难成立的条目、且关键项证据不足，属“多处…不符”，取4档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_109：Supports many E. coli traits and enzyme activities but not the answer&#x27;s broad sulfoquinovose-to-sulfite trait claim or the specific alternate dehydrogenase/sulfo-lyase activity set.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_109：Shows which trait fields have observed scoreable evidence; used to avoid treating nulls or unsupported traits as observed facts.
- ANSWER_TEXT / ANSWER.organism_profiles ORG_001.traits：Shows the three filled trait claims and their internal-only evidence.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> The only evidence entry is INTERNAL_KNOWLEDGE_ONLY with no database, record_id, or locatable external source. Per D5 source-state rules this is MISSING_SOURCE for the decision-relevant claim groups. There is no verified mis-citation, so no cap applies, but traceability is almost entirely absent, placing D5 in the lowest band at 1.

<details><summary>V0.4理由与本行变化背景</summary>

全答案唯一来源为evidence_registry&#91;EVID_001&#93;，source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id=null；所有step及性状均由EVID_001背书。按四.3/P34，纯内部知识自我声明属MISSING_SOURCE（缺失而非误导），决策相关组全部缺失→低分档且默认不cap。答案虽嵌入EC号与TaxID等可查标识，但均未提供可定位的文献/数据库条目或计算记录，无法从答案追到外部依据，故取2档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry EVID_001：Shows the answer supplies only an internal-knowledge declaration, not a locatable database record or literature citation.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer explicitly lists several uncertainties: unspecified oxygen condition, missing ECs, species-level-only organism identity, and missing trait sources. It also uses confidence labels and nulls rather than fabricating trait values. However, it presents a specific alternative route and enzyme set with medium confidence based only on internal knowledge, and it does not clearly distinguish inferred route claims from supported observations. This is honest but still overconfident in places, fitting 5-6; 6 is chosen given the explicit uncertainty section.

<details><summary>V0.4理由与本行变化背景</summary>

正面：uncertainties&#91;&#93;具体列出氧条件未定、两酶EC缺失、仅到E. coli种级、多数性状无来源；逐step给出不确定点（α异头物、SMILES null、立体化学按裂解酶推断）与confidence=medium，cofactor SMILES诚实null，属较好的不确定性披露。不足：对E. coli“完成整条路线（含sulfo-lyase产亚硫酸盐）”以medium置信、零披露地呈现，未说明其与canonical DHPS终点的分歧，构成单点过度确信/证据性质标注不足。非系统性误导，取6档（5–6档内偏高）。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit disclosure of several limitations and unknowns.
- ANSWER_TEXT / ANSWER.evidence_registry EVID_001：Shows the evidence basis is internal only, making medium-confidence route claims a disclosure-quality concern.

</details>

## Grok

答案SHA256：`be08c043e0d24f308e8ef1cda0436048be08cdf7115856c76905229c6f81db58`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Pathway, microorganism, 15 traits, evidence registry and uncertainties are present, and the route name is exact. However the answer delivers only four of the five required main-chain steps, omitting the S05 sulfoquinovose mutarotase entry conversion, and every step leaves enzyme EC null despite the task requiring one preferred enzyme and EC per step. This is a 5-6 completeness/task-conformance profile, lower half because required EC fields are systematically omitted and one required step is absent.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：Shows S05 is an enzyme-supported required step in the frozen main chain; does not by itself judge the answer text.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Supports that S05 is the alpha-to-beta mutarotation step; does not prove further chemistry.

</details>

### D2 反应化学科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The delivered chemistry for S2-S4 is largely coherent: phosphorylation to F1P, aldol cleavage to DHAP plus (S)-sulfolactaldehyde, and NADH-dependent reduction to the gold terminal DHPS. Cofactors ATP/ADP, NADH/NAD+ and H+ are included. The main deductions are that S1 starts from the alpha anomer and directly uses sulfoquinovose isomerase without the beta-mutarotation step, and DHAP is labelled main rather than byproduct. These are local/entry issues, not a wholesale collapse of the path, so 7 rather than 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Supports the ordered main-chain transformations and terminal DHPS; does not support an alpha-to-fructose isomerase shortcut without mutarotation.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_109：Supports the terminal product identity; does not verify the answer&#x27;s SMILES protonation state.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Supports the beta anomer reaction for EC 5.3.1.31; does not list alpha-sulfoquinovose as substrate.

</details>

### D3a 目标反应与酶对应：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Manual mapping against the accepted enzyme sets supports the kinase, aldolase and reductase functions (S01, S03, S02) by accepted enzyme name at G4-level curation, despite missing EC fields. The S04 isomerase name is present, but the answer uses the alpha anomer directly whereas EC 5.3.1.31 is documented on beta-sulfoquinovose; that target is left unresolved rather than treated as a proven contradiction. Most importantly, the required S05 entry mutarotase conversion is absent and S05 is a predefined key entry step. D-KEY4 therefore caps D3a at 4; the remainder shows substantial supported enzyme content, so 4 rather than 3.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：Supports accepted enzyme names/ECs for the five required steps; does not confirm optional gene/protein attribution or missing EC fields.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：Supports the required S05 entry step and the beta substrate for S04; does not prove other answer enzymes wrong.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Supports beta-sulfoquinovose as documented substrate and does not list alpha-sulfoquinovose.

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer consistently recommends Escherichia coli K-12 substr. MG1655 for the four delivered steps, and gold organism rows support E. coli at species level for the corresponding steps; the gold PATHWAY_COMPLETE row also supports an E. coli whole-pathway claim at species level. However the answer&#x27;s strain-specific TaxID 511145 and strain-level capability are not present in E0, and S05 has no assigned microorganism. This is a reasonable candidate with partial support, but specific identity/range remains insufficiently verified: 5-6 band, upper half 6.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_109：Supports E. coli species-level organism assignment and complete-pathway status for E. coli; does not verify strain K-12 MG1655 TaxID 511145.

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 traits are filled. Species-level E. coli gold supports the main qualitative traits: facultative/aerotolerant oxygen profile, non-halophilic salinity preference, motility, rod shape, Gram-negative, non-sporulating, and several carbon-source/degradation activities. The answer&#x27;s specific optimum 37 C, pH 7, ATCC 700926, NC_000913.3 genome values and habitat-generalist interpretation are not frozen in E0 or are not scoreable at subfield granularity. No verified trait contradiction appears, but several quantitative/accession specifics require confirmation, so 7 rather than 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_109：Supports species-level oxygen, salinity, motility, morphology, Gram, sporulation and carbon-source traits; does not verify strain-specific ATCC/genome/optimum values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_109：Supports the distinction between observed-accuracy traits and completeness-only traits.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_109：Supports treating the 37 C optimum as not independently verified in the frozen local inputs.

</details>

### D5 来源与可核查性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer supplies a structured evidence registry with specific literature and database locators (EVID_001-EVID_005) and maps them to steps and traits. However E0 only contains EC 5.3.1.31 and 5.3.1.34; the cited core literature, TaxID 511145, NC_000913.3 and ATCC 700926 are not frozen for verification, and most trait sources are INTERNAL_KNOWLEDGE_ONLY. No verified mis-citation is established, so D5 is not capped. The result is partial traceability: some key conclusions are locatable, but many source-support links remain unresolved or internal-only, placing D5 in 5-6, scored 6.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.31：Supports only the beta-sulfoquinovose EC fact; it does not verify the answer&#x27;s full literature claim or other database IDs.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：Shows accepted enzyme records exist for the targets; does not verify the answer&#x27;s delivered EVID_001 citation content.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_109：Supports species-level E. coli organism records; does not verify TaxID 511145 or ATCC 700926.

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer distinguishes several evidence types and limitations: it explicitly notes missing ECs, unverified SMILES stereochemistry, the K-12 strain caveat, oxygen-condition ambiguity, and alternative sulfoglycolytic routes. It also labels EVID_005 as internal knowledge with medium confidence. Weak points are that several trait and strain-specific fields are presented at high confidence despite unresolved E0 records, but this is not a systemic conversion of prediction into observation. Main uncertainty disclosure is present, so 7.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows the answer itself disclosed EC, SMILES, strain, oxygen and route-variant limitations; does not verify the truth of the underlying claims.
- ANSWER_TEXT / ANSWER.evidence_registry：Shows some trait evidence is explicitly internal-only; this supports judging uncertainty labeling separately from D4 correctness.

</details>

## GPT5.6

答案SHA256：`f202ea5708e52654bb91f7b28d3f882169ccee803783915c14d4ff47f7536da8`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主要模块（steps、enzyme、microorganism、organism_profiles、traits、evidence_registry）均有回应，但未按5步主链完整交付：答案只有4步，S1把alpha-底物直接写成异构化为fructose而缺少gold的mutarotase入口步，S3产物与gold的aldolase产物不符，且在gold终点DHPS之后又以S4继续到pyruvate/sulfite。多项必要SMILES/EC为null，15项性状大量null。属于主要模块涉及但若干必要内容遗漏/占位/起点终点不清，未达到仅少量遗漏的7–8档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_109：本案ordered_step_count=5，LINEAR_UNIQUE；说明必答主链为5步，而不是把全部旁支作为分母。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：列出5个必答步的顺序及主底物/主产物；用于核对交付步数、步序和终点，不作为全部旁支并集。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_109：本案gold terminal main product为(S)-2,3-dihydroxypropane-1-sulfonate。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际仅交付steps S1–S4和一个organism_profile；S4在DHPS之后继续生成pyruvate/sulfite；多项必需SMILES、EC编号与性状为null。

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S2的fructose→fructose-1-phosphate激酶步与gold的S01大体相符，但主链化学有多处重要错误：S1把alpha-sulfoquinovose直接写成异构化为6-deoxy-6-sulfo-D-fructose，E0的EC 5.3.1.31反应使用beta-sulfoquinovose，gold还要求S05 alpha→beta mutarotase入口；S3的aldolase产物写成DHPS + D-glyceraldehyde 3-phosphate，而gold S03的aldolase产物为(2S)-3-sulfolactaldehyde + glycerone phosphate，且少了后续S02还原为DHPS的步骤。S4在gold终点DHPS后继续到pyruvate/sulfite，不作为得分主链的一部分。故属于多个重要步骤错误、核心中间体与连续性不成立，落在3–4档；局部正确的S2不足以升到5–6档。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.31：官方EC 5.3.1.31条目的reaction列明确为beta-sulfoquinovose生成6-deoxy-6-sulfo-D-fructose（及beta-sulfoquinovose生成6-sulfo-D-rhamnose）；该条目本身不支持alpha-sulfoquinovose直接异构化为fructose。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：给出本案5个必答步的具体主底物/主产物：S05 alpha→beta mutarotase；S04 beta→fructose异构化；S01 fructose→fructose-1-phosphate；S03 F1P→(2S)-3-sulfolactaldehyde+glycerone phosphate；S02→DHPS；gold终点为DHPS。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：accepted酶/EC包括5.1.3.43、5.3.1.31、2.7.1.184、4.1.2.57、1.1.1.373/1.1.1.61；这些条目支持目标反应粒度，不证明答案中未给EC或错误步骤的化学替代。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S1使用alpha-sulfoquinovose→fructose；S3使用F1P→DHPS+D-glyceraldehyde 3-phosphate；S4在DHPS之后继续生成pyruvate+sulfite；S2为fructose→F1P激酶步。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按目标反应功能判断：S2激酶在名称-反应层面对应accepted S01，是少量可用目标支持；但S05入口变旋酶缺失，S02终端还原酶缺失，S04异构酶被用于alpha而非gold beta底物，S03醛缩酶虽名称相近却给出DHPS+G3P而非gold的sulfolactaldehyde+DHAP。多个KEY目标映射失败/缺失，D3a只能落在低档；D-KEY4上界4下取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_109：列出S05-&gt;S04-&gt;S01-&gt;S03-&gt;S02的目标反应顺序及S03产物sulfolactaldehyde+glycerone phosphate；不支持答案S3的DHPS+G3P。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_109：列出五步accepted酶名/EC；支持S05 mutarotase与S02 reductase是独立目标步。
- E0_EVIDENCE / f3e0:ec:5.3.1.31：官方5.3.1.31反应记录为β-sulfoquinovose到6-deoxy-6-sulfo-D-fructose；不扩展到alpha底物或具体蛋白活性。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> E. coli作为物种在gold中支持S01-S04多步且有PATHWAY_COMPLETE E. coli 562；答案统一使用E. coli K-12 MG1655/TaxID 511145，属物种级支持菌株级声称，且E0无511145记录。另S4 desulfonylase被归给E. coli但gold无该步反应级菌株证据。按身份阶梯为粒度不足/局部未核，不cap；给5-6档上沿6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_109：支持E. coli物种对S01-S04多步及PATHWAY_COMPLETE E. coli 562；不核验K-12 MG1655/511145株级身份或S4 desulfonylase能力。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_109：含E. coli 562及部分菌株性状；不含TaxID 511145菌株级完整记录。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项键均出现，但F2/F3/F4/F5/F10/F11/F14为null/明确未知；非空项多为low/unknown。F1 facultatively anaerobic、F12 Gram-negative、F13不产芽孢与E. coli物种gold相容；F6仅部分；F7/F8/F9偏泛化且依赖INTERNAL_KNOWLEDGE_ONLY；F15把栖息地广适性写成肠道/水体/土壤等，gold F15为UNKNOWN，属无依据外推。Honest null不判错，缺失主归D1；D4因部分性状可用但关键证据/条件不足给6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_109：E. coli 562的F1有aerotolerant/facultative anaerobe记录，F12 gram positive=false，F13 sporulation=false；F15为UNKNOWN；不支持答案F15的具体广适性推广。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_109：显示F3/F15等为completeness_only，F2/F4部分子字段待裁定；用于区分completeness与observed_accuracy，不把null直接当错误。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部重要结论只指向EVID_001/EVID_002，二者source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null。按D5六状态，decision-relevant组（路线、酶、身份等）均为MISSING_SOURCE；无已核实错引，不cap。D5落在1-2低档；因有内部evidence_registry与claim_scope但仍无可定位外部来源，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示仅两条INTERNAL_KNOWLEDGE_ONLY证据，database/record_id/locator为null；不能作为可定位外部来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确列uncertainties：EC未确认、SMILES/立体化学未核验、未确认同株同条件直接实验；多数confidence为low/unknown，evidence_registry明确标INTERNAL_KNOWLEDGE_ONLY，honest null较多。残留问题是部分酶仍标medium、route_summary/complete_pathway表述较肯定。未构成系统性把预测当观测；D6在7-8档取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：列出EC/SMILES/同株同条件未确认等限制；支持D6诚实披露但不是外部来源。

</details>
