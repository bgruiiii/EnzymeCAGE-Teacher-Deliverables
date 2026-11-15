# BIOPATH150_079：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：5,5&#x27;-dehydrodivanillate degradation

污染物：2,2&#x27;-Dihydroxy-3,3&#x27;-dimethoxy-5,5&#x27;-dicarboxybiphenyl；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 45 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 32 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 73.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 66.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 71 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 31 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`9ccd9fb0d513764ee9e40abd59993091de74b8bb564038c176c98b4e76448114`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 输出完整可解析，route_scope.chosen_route_name原样填写，程序task_conformance_status=OK；steps、酶、微生物、15项性状、来源和不确定性模块均存在。主要问题：所给五步链并非题面指定四步主链的完整复现，S1产物与gold S01不同，S2/S04对应目标未交付，仅S3与必答终点相关；S4/S5还延伸到终点下游。按D1 5–6档取6：主要模块均涉及且关联清楚，但必要主链内容有实质遗漏/错配，不因格式完整而升入7–8。

<details><summary>V0.4理由与本行变化背景</summary>

五个step均给出底物/产物英文名与SMILES、首选酶/基因、对应微生物，route_scope.chosen_route_name按题面原样填写；15项性状全部出现，9项填写、6项明确unknown/null，无字段集合遗漏。EC多处null属题面允许的诚实缺失。扣分点：S2把meta-cleavage dioxygenase与hydrolase压缩为一步，且vanillate下游至PCA/TCA作为主链延续而未与gold终点vanillate明确分层；这些主要是模块粒度和边界表达问题，不构成D1任务参数偏离的关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION.BIOPATH150_079：题面要求指定路线下给出主链、每步底物/产物/酶/EC/微生物，并填写15项性状；不证明答案路线步骤正确。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_079：该case为LINEAR_UNIQUE、ordered_step_count=4；仅说明必答主链长度与图形状态，不替代逐步化学核验。

</details>

### D2 反应化学科学性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 主链核心转化严重错误：gold S01为DDVA单次O-脱甲基生成2,2&#x27;,3-三羟基-3&#x27;-甲氧基-5,5&#x27;-二羧基联苯，答案S1却写成双O-脱甲基生成四羟基产物；答案S2又把无甲氧基的四羟基联苯直接裂解为含甲氧基的5-羧基香草酸，答案自述该计量/甲氧基来源存疑，构成明显原子不守恒与无依据跳步，并跳过gold S04双加氧酶及S02 meta-cleavage水解步骤。S3脱羧到vanillate本身可成立，但不足以挽救已断裂的主链。按D2 1–2档取2：核心转化和连续性明显失效，仅局部下游信息可用。

<details><summary>V0.4理由与本行变化背景</summary>

gold主链S01为DDVA单次O-脱甲基生成5,6,6&#x27;-Trihydroxy-5&#x27;-methoxy&#91;biphenyl&#93;-3,3&#x27;-dicarboxylate（保留一个甲氧基），S04再对三羟基-甲氧基底物开环，S02水解酶生成5-carboxyvanillate。答案S1却把两个甲氧基都脱去生成2,2&#x27;,3,3&#x27;-tetrahydroxy产物；S2又把四羟基底物直接变成含甲氧基的5-carboxyvanillate，绕过gold的meta-cleavage产物与hydrolase，并伴随明显原子/甲氧基来源不连续。S3脱羧步骤正确，S4-S5属gold终点vanillate下游延续。首步核心转化错误且S1-S2连续断裂，触发D2关键错误cap≤4；因S3及下游仍有合理内容，档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：gold逐步显示S01为DDVA单O-脱甲基到2,2&#x27;,3-三羟基-3&#x27;-甲氧基-5,5&#x27;-二羧基联苯，随后S04双加氧、S02水解、S03脱羧；不支持S1双脱甲基到四羟基或S2直接裂解到5-羧基香草酸。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_079：gold酶行列出S01 O-脱甲基酶、S02 OH-DDVA meta-cleavage hydrolase、S03 5-carboxyvanillate decarboxylase、S04三羟基甲氧基联苯双加氧酶；用于核对答案是否实现对应转化。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 四个必答目标中：S03 5-carboxyvanillate decarboxylase→vanillate与accepted名称及产物相符，判S；S01虽写出accepted O-demethylase名称，但产物为双脱甲基四羟基联苯而非目标单脱甲基产物，判F；S04所需2,2&#x27;,3-三羟基-3&#x27;-甲氧基联苯双加氧酶未交付，判F；S02所需OH-DDVA meta-cleavage hydrolase完全缺失，判M。S=1、F=2、M=1、U=0，C=0.25，落&#91;3,4&#93;；因仅末端目标可用、KEY入口失败且主链多数目标失败，取3。D3a未另签独立key_error=Y；KEY失败已在上限/区间内反映。

<details><summary>V0.4理由与本行变化背景</summary>

S1 LigX为O-脱甲基加氧酶、S3 LigW2为5-carboxyvanillate decarboxylase、S5 LigAB为原儿茶酸4,5-双加氧酶，酶名与反应类型基本对应；但S2用LigZ dioxygenase直接给出5-carboxyvanillate，遗漏gold S02的meta-cleavage hydrolase，酶-产物对应不完整；多处EC为null，仅VanA/VanB给EC 1.14.13.82。属有合理候选与部分支持、若干关键步骤仍缺具体核验，定5-6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_079：accepted酶行支持S01 O-demethylase、S02 hydrolase、S03 decarboxylase、S04三羟基甲氧基联苯双加氧酶；不证明答案S2四羟基底物酶同于S04。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：gold反应行给出四个必答步的底物/产物与顺序，用于判定S1产物错配、S2缺hydrolase、S3匹配。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案将全部步骤归属Sphingobium sp. SYK-6（strain SYK-6），与gold organism_gold中的Sphingomonas sp. SYK6（TaxID 502559）为同一SYK-6菌株的旧/新命名关系，答案也在route_summary说明曾名Sphingomonas/SYPHINGO...；gold PATHWAY_COMPLETE行支持该菌完整路径能力。未提交TaxID不影响D3b本身，但身份名称与TaxID有待核，故按7–8档取8而非9–10。

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤归属Sphingobium sp. SYK-6（strain SYK-6），与gold的Sphingomonas sp. SYK6同一菌株token一致，且gold PATHWAY_COMPLETE也指向同一TaxID 502559；answer将taxid、保藏号等未知项填null，没有用无关编号冒充。少量扣分来自未给TaxID与分类异名说明，但菌株身份和步级归属总体正确，未发现由序列存在性外推整条路径的错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_079：gold各步与PATHWAY_COMPLETE行均指向Sphingomonas sp. SYK6 / TaxID 502559，支持同一SYK-6菌株及完整路径能力；不直接证明Sphingobium名称的官方TaxID对应。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项性状全部返回：9项填值、6项明确未知、0项遗漏。trait_gold仅F14 genome_basic为OBSERVED（TaxID 502559），其余F1–F13/F15均为UNKNOWN；trait_scoreability_mask将F1–F13/F15列为completeness_only，仅F14为observed_accuracy。答案F14全null，且未在profile给出TaxID 502559；其余好氧、革兰氏阴性、底物谱等仅有EVID_002内部知识，不能按已核实观测计。按D4 5–6档取5：有部分合理性状和完整字段结构，但关键可观测项F14缺失，其他关键性状证据不足，不能进入7–8。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现，9项填写、6项明确unknown/null；温度、pH、盐度、保藏、运动性、基因组等关键定量/身份性状未编造。已填F1好氧、F6好氧呼吸/O2、F7木素衍生芳香物利用、F8广谱降解、F9酶活、F11杆状、F12革兰氏阴性/糖鞘脂外膜、F13不产芽孢、F15栖息地等，对SYK-6总体合理，但均无raw_text且E0无性状记录可核，仅能按适用性与证据不足评5-6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_079：gold仅F14 genome_basic为OBSERVED（TaxID 502559），其余14项为UNKNOWN；不把UNKNOWN当作答案错误，也不支持答案内部知识性状为已核实观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_079：F14为observed_accuracy，F1–F13/F15为completeness_only；用于D4区分已观测准确性与完成度，不把完成度缺失误判为科学错误。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> EVID_001标为LITERATURE_DIRECT/PubMed，但record_id=null，locator仅为作者团队系列工作且自述未能逐条核对，属笼统文献来源；EVID_002为INTERNAL_KNOWLEDGE_ONLY。路线/关键酶/菌株/终点等决策相关组只有笼统或内部来源，没有条目级可定位可核对记录；性状组多为内部知识或缺失。未发现经核实的虚构或错引，GENERIC/MISSING默认不触发cap。按D5 3–4档取3：仅给笼统库名/作者列表，结论与来源关联很弱。

<details><summary>V0.4理由与本行变化背景</summary>

答案实际交付EVID_001为PubMed作者/综述性来源但database=PubMed、record_id=null、locator仅写Masai/Katayama/Fukuda等系列工作，无法定位到具体条目；EVID_002为INTERNAL_KNOWLEDGE_ONLY并用于多项性状。决策相关组CG01/CG02/CG03/CG05/CG07等仅有笼统来源，无条目级可定位可核对证据，符合3-4档；性状组多为MISSING_SOURCE。E0为EVIDENCE_GAP，无法核实错引，故不判VERIFIED_MIS_CITATION，不触发D5 cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / EVID_001：EVID_001仅有PubMed及作者团队概述、无record_id/稳定locator；支持“笼统文献来源”判断，不支持其已定位到具体条目。
- ANSWER_TEXT / EVID_002：EVID_002为INTERNAL_KNOWLEDGE_ONLY，无外部数据库/文献定位；支持性状来源缺失判断，不等同于虚构。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确区分了未知与推断：EC编号多处null、TaxID/基因组/温度/pH/盐度等null，uncertainties列出S2甲氧基/计量疑点、LigW/LigW2同工酶未定、来源为训练记忆、氧条件题面未指定等；没有把预测系统性写成实验观测。个别高置信（如S4/S5）和部分内部知识性状仍有过度确信，但限制披露总体具体。按D6 7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案对未知项大量填null/unknown，uncertainties逐条披露S2计量/中间体疑点、LigW/LigW2生理主酶未定、多个EC未确证、TaxID/保藏/基因组/定量性状缺失，以及整体来自训练知识记忆、建议复核；未把预测系统性写成实证。扣分点：部分内部知识性状仍给medium confidence且无raw_text，但已用INTERNAL_KNOWLEDGE_ONLY登记并总括披露，不构成系统性误导。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：逐条列出EC、TaxID、性状、S2计量/甲氧基及来源记忆限制；支持D6披露较充分，不把这些unknown当作已核实正确。

</details>

## DeepSeek

答案SHA256：`d13dc28849488c14da34c63f97967fbc9b885195008ff1e0456b315eafae378a`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Main modules are attempted, but only one of the four required gold steps (S03 terminal decarboxylation) is represented correctly; the entry step is wrong/merged, S02 and S04 are absent, all EC fields are null, all 15 traits are explicitly unknown, and evidence_registry is empty. This fits the 5–6 band (main modules involved but several necessary omissions/placeholders), scored at 5 because required main-chain content and EC/evidence completion are missing.

<details><summary>V0.4理由与本行变化背景</summary>

主要模块均被结构性地涉及：路线名原样回填（chosen_route_name=5,5&#x27;-dehydrodivanillate degradation，无换路线）、三步各绑定一个酶（含gene LigX/LigW/LigM）与一个菌，同菌去重为单一ORG_001且引用自洽；但若干必要内容仅占位或遗漏：15项性状全部为null/unknown（零实质内容）、evidence_registry为空（各项来源全缺）、主链仅3步且把首段两个gold转化压缩为一步。符合5–6档“主要模块均有涉及，但若干必要内容遗漏、仅占位或关联不清”，取低端5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows 3 steps, null ECs, all-null traits, and empty evidence_registry.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：Shows the four required gold main-chain steps and terminal Vanillate; does not require scoring downstream beyond the terminal.

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> The first answer step collapses the gold S01 O-demethylation, S04 ring-cleavage dioxygenation, and S02 hydrolase into a direct DDVA→5-carboxyvanillate conversion with no byproducts/cofactors, an unsupported multi-step jump and core continuity break. S2 correctly gives the terminal decarboxylation to vanillate + CO2, and S3 is an extra downstream demethylation not part of the required terminal scope. Score 3 in the 3–4 band because a severe core transformation/connectivity error remains despite one correct terminal step.

<details><summary>V0.4理由与本行变化背景</summary>

S1把C16联苯(DDVA)直接写成经“双加氧”一步生成C9的5-羧基香草酸，既错置了首步反应类型（gold首步为5,5&#x27;-dehydrodivanillate O-demethylase催化的O-脱甲基化，释放甲醛并消耗O2/NADH），又无任何开环产物、辅底物或副产物说明，原子明显不守恒且无说明（少一个苯环与多个碳，无CO2/小分子去向）——属主链第一步即错+无依据跳跃。S2（5-羧基香草酸→香草酸+CO2，脱羧）与gold S03一致且化学成立；S3（香草酸→原儿茶酸+甲醛，O-脱甲基化）化学成立但位于gold终点（香草酸）之外，按四.2/P29不加分也不作为覆盖率扣分。整体符合3–4档“多个重要步骤错误…违反基本化学约束或无依据跳跃”，取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s compressed first step and extra downstream step.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：Shows S01 O-demethylation, S04 ring-cleavage dioxygenation, S02 hydrolase and S03 terminal decarboxylation; does not prove all alternative routes impossible.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_079：Shows the root substrate and terminal Vanillate for this route.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> Only answer S2 clearly matches a required target: 5-carboxyvanillate decarboxylase (gold S03, accepted EC 4.1.1) converting 5-carboxyvanillate to vanillate + CO2. S1 names a &#x27;5,5&#x27;-dehydrodivanillate dioxygenase&#x27; rather than the accepted S01 O-demethylase and gives a different product; S02 and S04 are absent. All explicit ECs are null. The supported target fraction is 1/4 plus a mismatched entry and missing key steps, so the score lies in &#91;1,4&#93;; 3 reflects the one exact terminal match but severe target coverage failure.

<details><summary>V0.4理由与本行变化背景</summary>

S2的LigW=5-carboxyvanillate decarboxylase与S3的LigM=vanillate O-demethylase，酶名/功能与所催反应及gold对应步骤一致；但S1把作用于DDVA的酶写成“5,5&#x27;-dehydrodivanillate dioxygenase”，而gold同一步的酶名为5,5&#x27;-dehydrodivanillate O-demethylase（EC-1.14.13），即基因LigX选得对、功能标注错，首步酶-反应对应存在一处实质矛盾；三步EC全为null（属诚实未知而非错误编号，但使酶-EC对应无法核验）。符合5–6档“有合理候选和部分支持，但若干关键步骤仍缺具体核验”，取5；该错误未达到“核心步骤酶功能明显错误使主要推荐失效”（酶候选本身仍指向DDVA作用酶），不触发关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows enzyme names, null ECs, and answer products.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_079：Shows accepted S01 O-demethylase and S03 decarboxylase names/ECs; does not certify answer&#x27;s LigX/LigW/LigM gene annotations.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：Shows required S01,S02,S03,S04 reactions and products; does not prove any unverified alternative target.

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> All three steps assign the same strain profile SYK-6, which matches the gold strain token Sphingomonas sp. SYK6 (TaxID 502559) and the gold PATHWAY_COMPLETE organism. However, the answer over-specifies the species as &#x27;Sphingomonas paucimobilis&#x27; while gold leaves it as &#x27;Sphingomonas sp.&#x27;, provides no TaxID, and gives no independent step-level capability evidence. This is a reasonable candidate with partial identity/capability support, fitting 5–6; 6 because the strain token matches across all steps.

<details><summary>V0.4理由与本行变化背景</summary>

三步均归属同一菌株SYK-6，与gold五条步级记录的matched_organism_name（Sphingomonas sp. SYK6，TaxID 502559，organism_match_status=EXACT）在菌株级完全对齐，且未把单步菌写成“整条路径菌”或额外声称全路径能力（complete_pathway_organism_profile_id=null）。待确认项：种名写作Sphingomonas paucimobilis（gold只到Sphingomonas sp.，属历史命名沿革），且ncbi_taxid全为null未给身份编号——属“少量具体条目需确认”，不推翻菌株级推荐。符合7–8档，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows one profile Sphingomonas paucimobilis SYK-6 with null TaxID assigned to all steps.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_079：Shows Sphingomonas sp. SYK6 TaxID 502559 for all steps and a PATHWAY_COMPLETE row; does not resolve the answer&#x27;s species epithet &#x27;paucimobilis&#x27; or its null TaxID.

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> All 15 required trait fields are present only as null/unknown values, with no substantive trait value delivered. Per the rubric&#x27;s all-null trait provision, D4 is scored MISSING=1 as non-delivery, not as a detected scientific error. Gold has most traits UNKNOWN and one F14 observed TaxID, but the answer delivered no observed trait value.

<details><summary>V0.4理由与本行变化背景</summary>

唯一organism_profile的15项性状全部以null/空对象交付（字符串型value=null；对象型各子键null；confidence=unknown；evidence_id=null），即该模块没有交付任何可评价的性状内容。按量表四.4/P44“全部必需性状均为null/空值时同样处理——D4按MISSING记1分，不宣称检测到科学错误”，本维记MISSING=1保留权重；同时不把“诚实未知”当作错误或遗漏处理（该完成度缺口已在D1反映）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows every trait value is null/unknown.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_079：Shows most traits UNKNOWN and F14 observed TaxID; does not make null trait values into false scientific claims.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_079：Shows only F14 is observed_accuracy scoreable; other traits are completeness_only.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> The answer has an empty evidence_registry and every step/trait evidence_id is null, so none of the key route, enzyme, organism or trait claims can be traced to a delivered source. This is MISSING_SOURCE across decision-relevant groups. E0 is EVIDENCE_GAP, so there is no verified mis-citation and no cap; D5 is scored low because source delivery is absent, not because a fabrication was verified.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry为空数组，steps的reaction_evidence_id/trait_evidence_id、enzyme/microorganism.evidence_id与全部性状evidence_id均为null——所有结论只依赖内部知识（MISSING_SOURCE）。按四.3/P34，MISSING_SOURCE属缺失而非误导，落低分档且默认不cap；仅LigX/LigW/LigM等基因标识与统一low/unknown置信度提供了极有限的可追查抓手，故取低分档上限2。答案未引用任何条目，故不存在可核实的错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不触发关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows no source records and no evidence_id assignments.

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer marks step enzymes/microorganisms as low confidence and all traits as unknown, which is honest about uncertainty. But route_summary states the course as fact without limitations, uncertainties is empty, and the central route compression is not disclosed as a gap or prediction. This fits 5–6: some uncertainty labeling but too generic, with some conclusions stronger than the evidence.

<details><summary>V0.4理由与本行变化背景</summary>

正面：所有酶/菌置信度统一标low、全部性状标unknown，未编造任何数值或编号，未出现high confidence包装未核内容。不足：uncertainties为空、每步uncertainty=null，未区分观测/预测/推断与未知，未说明主要限制与待验证点；route_summary以陈述语气断言“LigX双加氧酶开环生成5-羧基香草酸…”（该首步本身缺乏依据），结论强度超过所给依据。属“有不确定性说明但过于笼统，部分结论强度仍超过依据”，取5；非系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows low/unknown confidence fields, an assertive route_summary, and empty uncertainties.

</details>

## Kimi

答案SHA256：`f05ccba209e616b6e9b0bb7b675d9f5221ea317bee8576400228f6ff5274b947`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 题面指定路线名route_scope.chosen_route_name逐字回显；四个必答主链步（DDVA O-脱甲基→OH-DDVA开环→开环产物水解→5CVA脱羧至香草酸）均逐步给出底物/产物/首选酶/对应菌；10步、单profile按物种+菌株去重、15项性状齐备（10填5显式null）、evidence_registry完整。扣分点：S1未给EC（题面要求每步给EC），S5–S10为终点后下游延续却置于steps而非downstream_continuation，范围表达略越界（不加分亦不按缺步扣分），故8而非9–10。

<details><summary>V0.4理由与本行变化背景</summary>

六模块（路径/酶/微生物/性状/来源/不确定性）均有实质交付；route_scope.chosen_route_name原样保留题面路线名；10步均含主底物与主产物英文名+SMILES并绑定首选酶与微生物；15项性状全部出现（10项填值、5项显式unknown/null，按P15明确未知≠遗漏）；来源登记10条且内部evidence_id引用自洽；CHPD支路另列并声明不属主链。局部不足：S1的LigX未给EC（自称未分配）、F11/F15填值无来源、主链终点延伸超出gold 4步范围（已在uncertainties声明）。落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：仅支持题面要求与交付字段核对，不证明科学正确性
- GOLD_SLICE / case_root_identity.tsv：仅支持题目终点/路线身份，不扩展到答案下游步骤
- ANSWER_TEXT / ANSWER：仅支持交付完整性与字段覆盖，不证明科学内容正确

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 四个必答化学转化与gold逐步一致：S1 DDVA氧化O-脱甲基生成OH-DDVA+甲醛；S2 邻苯二酚环间位双加氧开环；S3 开环产物C–C水解生成5-羧基香草酸+CHPD；S4 5CVA脱羧生成香草酸+CO2；终点合规，后续PCA 4,5-开环→PDC→OMA→CHA→丙酮酸/草酰乙酸连接与方向合理。局部缺陷：S1漏写NADH/H2O/NAD+等计量（P103局部计量缺陷，不cap）、多步省略H+/电荷、S8以CHM标作LigI底物（实际为PDC水解酶，答案已在uncertainty说明）、立体构型未指定；不改变主链与关键转化结论，7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S4与gold线性顺序一致（S01 O-脱甲基→S04邻苯二酚环开环→S02水解→S03脱羧），主产物OH-DDVA、间位开环产物、5-CVA+CHPD、Vanillate的化学连接与质量守恒与gold化合物对应；S5–S10为SYK-6公认的PCA 4,5-开环下游，方向与连接正确。局部问题：S1缺NADH/H2O/NAD+、S4缺H+等辅因子与配平简化，部分中间体立体化学未指定，S8把CHM自发内酯化并入LigI步（已说明），属局部计量缺陷（P103）。下游延续不因gold覆盖不足加减分（P28/P29）。7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：仅支持gold各步方向/主底物/主产物与计量参照，不证明gold外下游
- GOLD_SLICE / enzyme_gold.tsv：仅支持各必答步反应-酶对应名称，不扩展到具体蛋白活性
- ANSWER_TEXT / ANSWER：支持答案化学表达本身；不证明SMILES电荷/立体逐字等价

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 读原答并按给定accepted/gold判断功能对应（非按自动匹配未确认直接NE）：四个必答步的酶名与accepted酶名一一对应——S1=5,5&#x27;-dehydrodivanillate O-demethylase（gold S01）、S2=2,2&#x27;,3-trihydroxy-3&#x27;-methoxy-5,5&#x27;-dicarboxybiphenyl dioxygenase（gold S04）、S3=OH-DDVA meta-cleavage compound hydrolase（gold S02）、S4=5-carboxyvanillate decarboxylase（gold S03），底物—产物方向一致。局部待核：S1缺EC（gold 1.14.13）；S4给4.1.1.-与gold 4.1.1家族前缀一致但未核小类；S2 1.13.11.-、S3 3.7.1.-为通配（gold NOT_OBSERVED，不能反推具体号）；ligX/ligZ/ligY/ligW为预先标注MINOR的归属未核。功能级对应可靠、仅少量局部待核 → &#91;7,8&#93;取下沿7；9–10不成立（EC/编号未核，九十分证据门NOT_ELIGIBLE且base range上限8）。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S4酶名与gold条目逐一对应（5,5&#x27;-dehydrodivanillate O-demethylase、OH-DDVA meta-cleavage compound hydrolase、5-carboxyvanillate decarboxylase、2,2&#x27;,3-trihydroxy-3&#x27;-methoxy-5,5&#x27;-dicarboxybiphenyl dioxygenase），反应类型与EC大类相容（1.14.13、3.7.1.-、4.1.1.-、1.13.11.-）；下游LigAB(1.13.11.8)、VanAB(1.14.13.82)、LigC(1.2.1.45)、LigI(3.1.1.57)、LigJ(4.2.1.83)、LigK(4.1.3.17)均属合理候选，且答案自述记忆归属建议核对。E0证据缺口使具体EC无法核验，按四.5/四.6登记UNRESOLVED而非错误。主要步骤有支持、少量条目待确认，7–8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：仅支持名称-反应层面与家族级EC比对，不证明具体蛋白底物谱或实验活性
- ANSWER_TEXT / ANSWER：支持答案所交酶名/EC原样；不证明其编号已核

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 全部步骤归属Sphingobium sp. SYK-6（ORG_001），与gold的Sphingomonas sp. SYK6为同一菌株名的属名写法规差异；单步归属与complete_pathway_organism_profile_id=ORG_001的全路径能力声称方向与gold pathway_complete=TRUE一致；未把某单步菌夸大为另一无关菌。待核：交付TaxID 317655与gold TaxID 502559不同且E0无记录可核（GAP-079-001/036/037），属名沿革未在答案中说明；三层（身份定位≠步级能力≠全路径能力）大体分开表述，但步级能力多为综述级支撑。身份主干可靠、仅少量具体条目待确认 → 7。

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤归属Sphingobium sp. SYK-6单一菌株，与gold的Sphingomonas sp. SYK6为同一SYK-6菌株（属名为分类学重命名，未经E0核验）；步级单酶归属与gold前4步菌株一致；完整路径能力声称与gold organism PATHWAY_COMPLETE=TRUE方向一致；未出现由基因组存在某酶直接外推整条路径的表述。TaxID 317655与gold 502559的差异无法核实（GAP-079-001/036/037），按身份阶梯属待核身份字段、非已核实错配，不cap，档内扣分。7分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：仅支持gold株级身份与整路能力标记，不核验答案TaxID 317655
- ANSWER_TEXT / ANSWER：支持答案身份与能力声称原样，不证明编号正确

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 15项齐备：10项给值、5项（F3/F4/F5/F10/F13）诚实null，null的完成度问题主归D1不重复重扣。已给性状与SYK-6身份相符（革兰氏阴性、短杆状、好氧、木质素芳香物降解、基因组AP012222），并逐项附confidence。缺陷：F2把“常规培养温度30°C”写成optimum_c=30（培养温度≠最适值，虽标low并附raw_text，仍属条件解释需修订）；F1/F6氧性状由途径酶推理得到而非菌株观测；F11无evidence。trait_scoreability_mask显示仅F14为observed_accuracy、其余completeness_only，准确性可判面窄，不能以“查不到”压分；不冒充观测、无离谱数值，故7。

<details><summary>V0.4理由与本行变化背景</summary>

15项中10项填值、5项诚实null（F3/F4/F5/F10/F13，按P15明确未知≠遗漏≠错误）；F7/F8/F12有具体来源且与SYK-6性状相符。但F2以“30°C常规培养温度”填为optimum_c，违反证据解释层“培养温度≠最适温度”（P52/P113）；F11形态、F15栖息地无来源且raw_text为null；F1/F6由途径酶推断而来未标注为预测。属“部分性状准确且适用，但关键项证据不足或条件解释需修订”的5–6档，取上限6分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv：仅支持哪些性状可作准确性判据，不提供性状真值
- GOLD_SLICE / trait_gold.tsv：仅支持gold性状可得性，不证明答案性状错误
- ANSWER_TEXT / ANSWER：支持答案性状取值与自述来源，不证明其已核

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 交付10条evidence_registry，S1–S10逐步绑定reaction_evidence_id、多数性状有evidence_id，来源可定位到具体综述/文献与MetaCyc/NCBI条目，决策相关组（路线、酶-反应、菌株身份、性状）均有条目级定位而非仅笼统库名。不足：多数为作者-年-卷-页式书目定位、无DOI/record_id，未给具体图表/段落；F11/F15无来源；F2温度以酶学论文支撑，属跨粒度引用。E0整题EVIDENCE_GAP，全部引用存在性与支持范围无法核验（UNRESOLVED_SOURCE），无已核实错引，故不cap；映射基本覆盖但未充分可核 → 5–6档取6（7–8需已核支持）。

<details><summary>V0.4理由与本行变化背景</summary>

证据登记10条：8条为具体到期刊卷期页的文献、2条数据库条目（MetaCyc条目无record_id；NCBI Taxonomy仅给317655）；各步与多数性状可追到具体条目，内部evidence_id引用自洽，未见张冠李戴或明显编造。E0为EVIDENCE_GAP（entries=0），全部引用-声称链无法机器核验，按P40/P51登记UNRESOLVED_SOURCE待核，不判虚构、不cap；F11/F15无来源、EVID_001无record_id使支持组记录不完整。属“部分关键结论可定位并核对、其他模块仍缺映射”的5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：仅支持答案实际交付的来源记录与映射关系，不回填评价者补证

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> uncertainties列出5条具体限制（EC编号待BRENDA/ExplorEnz核对、基因组大小/GC未知、保藏号null、CHPD支路基因归属未定、开环产物立体构型未指定、下游范围弹性），逐字段confidence分级并在evidence_registry标注DATABASE_DIRECT/LITERATURE_DIRECT；未知项如实null，未系统性把预测写成实证。不足：F1/F6把途径酶推理写成菌株性状、F2把培养温度当最适值而未见证据类型区分，TaxID 317655未列入待核清单，属单点过度确信/证据类型模糊而非系统性误导 → 8。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties专门列出EC记忆归属待核、LigX/LigZ/LigY/LigW无专属EC、辅因子表述不一、立体化学未指定、CHPD支路基因归属不确定、保藏号/基因组大小/GC不掌握并已按null记录，并说明主链范围定义弹性；诚实null与high/medium/low置信梯度基本与证据相称。局部问题：F2把培养温度写成最适值（仅以low confidence弱化）、S6/S9/S10未核实EC标high，属单点过度确信（P119），档内扣分而非系统误导。7–8档取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：仅支持答案的不确定性披露与证据类型表述，不证明披露内容本身正确

</details>

## Qwen

答案SHA256：`39f98a1dbd77a2eb346846143c14fb073dc538fa9b472504575e5ace04155a82`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 四个必答主链步骤均出现并覆盖到题面路线的主转化：S1 O-去甲基、S2 双加氧开环、S3 水解、S4 脱羧至vanillate；S5为终点后下游延续，downstream_continuation亦另列，不作为缺步扣分。15项性状字段齐全，同菌以ORG_001去重。扣分点：S2产物与S3底物SMILES为null、S1-S4多数EC为null，属于必要字段的少量遗漏。

<details><summary>V0.4理由与本行变化背景</summary>

六类模块均实质交付：5步均含主底物/主产物、首选酶、对应微生物；15项性状全列（8填、7明确未知、0遗漏）；route_scope.chosen_route_name按题面原样回显；uncertainties与各step uncertainty齐备。扣分点：多数步骤EC空缺（gold可提供1.14.13、4.1.1类）、S2/S3开环中间体SMILES为null、F14基因组为null；均为诚实未知且题面允许null，属字段级遗漏而非占位。落7档（大部分完整、少量遗漏）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_079：记录本题为LINEAR_UNIQUE、ordered_step_count=4；仅用于核对必答模块存在性，不要求覆盖全DAG旁支。
- ANSWER_TEXT / ANSWER.steps&#91;0-4&#93;：显示S1-S4覆盖主链并额外给出S5下游步骤；S2产物与S3底物的smiles为null。
- QUESTION_TEXT / QUESTION_TEXT：要求每步主底物/主产物英文名及SMILES、首选酶及EC、对应微生物，并返回15项性状；未知允许填null。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 主链方向与gold一致：S01 O-去甲基→S04双加氧开环→S02水解生成5-carboxyvanillate→S03脱羧生成vanillate；终点vanillate达到，S5为终点后额外下游，不加分不扣D2。主转化成立，但S01未列NADH/H+/H2O/NAD+，S2产物无SMILES，S3副产物名称/碳数与gold的4-carboxy-2-hydroxypenta-2,4-dienoate存在待核差异；按C02/P103作为局部计量/结构缺陷，不改变主链结论，落7-8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

主链S1→S2→S3→S4与gold四步在转化类型、顺序与方向、主产物上逐一对齐：S1 O-去甲基化得trihydroxy-methoxy联苯（对应BSY-c16593）+甲醛（对应S01）；S2环开裂双加氧得开环产物（对应S04）；S3水解得5-carboxyvanillate（BSY-c16591）（对应S02）；S4脱羧得vanillate（BSY-c16427）+CO2（对应S03）。S5为vanillate O-去甲基化下游延展，化学成立。局部问题：S1未列NADH计量（已披露）、S2/S3中间体SMILES为null、开环副产物命名与gold略有出入。均属局部计量/未确证问题，不改主链结论，落7-8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：给出四步主链的底物/产物方向与终点vanillate；不验证答案中缺失的辅因子、精确电荷表示及开环中间体SMILES。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_079：确认题面路线名与terminal compound为Vanillate；不支持额外下游步骤作为必答内容。
- ANSWER_TEXT / ANSWER.steps&#91;0-4&#93;：显示主链S1-S4化学转化及S5额外下游；S1辅因子不完整，S3副产物结构待核。

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 四个必答目标反应在名称/功能粒度均可对应：S01 5,5&#x27;-dehydrodivanillate O-demethylase、S04 2,2&#x27;,3-trihydroxy-3&#x27;-methoxy-5,5&#x27;-dicarboxybiphenyl dioxygenase、S02 OH-DDVA meta-cleavage compound hydrolase、S03 5-carboxyvanillate decarboxylase；无显式EC错配（S1-S4均null），主产物5-carboxyvanillate与vanillate对齐。中间体产物身份/SMILES及多数显式EC缺失，且E0为EVIDENCE_GAP，9-10被证据门阻断；7-8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶功能与gold酶名逐一对应且无矛盾：5,5&#x27;-dehydrodivanillate O-demethylase（BSY-e00958, EC1.14.13类）、ring-cleavage dioxygenase（BSY-e02630）、OH-DDVA hydrolase（BSY-e01217）、5-carboxyvanillate decarboxylase（EC4.1.1类）；S5 vanillate O-demethylase功能正确。扣分：多数步骤EC为null（本可给1.14.13/4.1.1类），S5 EC 1.14.13.83无冻结记录未核。落7档（主要酶对应有可靠支持，少量需进一步确认）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_079：给出四步accepted酶名/EC家族，支持功能级对应；不证明具体蛋白底物谱或实验活性，也不验证答案未给出的中间体SMILES。
- ANSWER_TEXT / ANSWER.steps&#91;0-3&#93;.enzyme：答案提供酶名，S1-S4的ec_number为null；S5的EC 1.14.13.83为终点后额外步骤。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 所有步骤均归到Sphingobium sp. SYK-6（菌株SYK-6），与gold步骤菌Sphingomonas sp. SYK6共享SYK-6菌株标识；答案还以complete_pathway_organism_profile_id=ORG_001声明整路径菌，而gold PATHWAY_COMPLETE行为TRUE。主要微生物推荐未被推翻；但Sphingobium/Sphingomonas属名差异、TaxID 502559未交付且E0无核验，只能取7档。

<details><summary>V0.4理由与本行变化背景</summary>

全步归属Sphingobium sp. SYK-6，与gold organism Sphingomonas sp. SYK6（taxid 502559）为同一SYK-6菌株的现行名；gold organism_gold显示四步均由SYK6完成，答案complete_pathway_organism_profile_id=ORG_001的全路径能力声称与gold一致（SYK-6确为该路径模式菌）；ncbi_taxid诚实null，未编造TaxID/保藏号，无身份错配。粒度上为物种+菌株名、无TaxID，取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_079：步骤菌记录为Sphingomonas sp. SYK6、TaxID 502559，且PATHWAY_COMPLETE=TRUE；不能证明Sphingobium属名同义或答案的null TaxID正确。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：答案使用Sphingobium sp. SYK-6，未填TaxID；以ORG_001声称整路径。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 15项性状字段齐全，缺失项以null/low明确标注。已填性状（好氧、革兰氏阴性、杆状、不产孢、可降解芳香底物等）对SYK-6类群合理，但主要来自INTERNAL_KNOWLEDGE_ONLY或泛化路径文献；gold仅F14有观察值而答案F14为null，且E0无性状记录可核。按部分性状可用但关键证据不足落5-6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

8项填入性状（F1好氧、F6好氧呼吸/O2、F7碳源利用、F8降解谱、F9酶活、F11杆状、F12革兰氏阴性、F13不产孢）在属级层面正确且与Sphingobium一致，均标low/medium并注明INTERNAL_KNOWLEDGE_ONLY；7项（温度/pH/盐度/保藏/运动/F14基因组/栖息地）诚实null。gold trait_gold全项UNKNOWN、仅F14有TaxID观测而答案F14为null；缺乏菌株级证据、关键项未核。按5-6档（部分性状准确且适用但关键项证据不足），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_079：除F14的TaxID观察行外，其余性状均为UNKNOWN；不能验证答案已填的好氧、革兰氏、形态、碳源等性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_079：仅F14标为observed_accuracy可评分，其余多为completeness_only；不把缺失自动当科学错误。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：显示8项有值、7项明确未知；已填性状多引用EVID_002内部知识。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 核心路线/酶/菌与性状主要依赖两条来源：EVID_001为Masai et al.自由文本文献、EVID_002为INTERNAL_KNOWLEDGE_ONLY。EVID_001被复用于S1-S5、organism、pathway，但无DOI/条目/图表/claim-level定位；EVID_002不能作为数据库/文献核验来源。决策相关组均为GENERIC/UNRESOLVED或MISSING，无已核实错引，故不cap；按GENERIC_SOURCE且决策相关组仅笼统来源落3-4档，因有具名研究和claim_scope标注取4。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（主链/起点/终点/酶-反应/菌身份/步级归属/全路径）来源均为EVID_001（Masai et al.自由文本，无DOI/条目定位）→笼统来源；性状多为EVID_002 INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE。全案EVIDENCE_GAP，无条目级可定位可核对证据；亦无已核实错引、虚构或撤转编号。按四.3决策相关组全部仅有笼统来源→3-4档，取4。诚实标注（内部知识、未知）计入D6正面，不豁免D5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：仅显示答案实际交付的来源记录：EVID_001为自由文本文献，EVID_002为内部知识；不证明这些来源真实支持具体步骤。
- ANSWER_TEXT / ANSWER.steps&#91;0-4&#93;.reaction_evidence_id：全部主链步骤复用EVID_001，属一源多步映射；不提供逐步可定位证据。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> uncertainties明确列出氧条件未指定、EC/基因/辅因子缺失、开环中间体结构未确证、菌株保藏/基因组/多数性状缺来源；各步及性状confidence以medium/low/unknown标注，EVID_002亦标为内部知识低置信。未系统性把预测写成观测；仅整路径能力与部分性状依赖泛化来源而未独立核验，属局部披露/证据强度问题，落7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties与各step uncertainty明确区分：氧化反应系按常见好氧酶系推断、EC/基因/辅因子缺失、开环中间体结构未确证、菌株保藏与基因组及多数生理性状缺直接来源；EVID_002显式标INTERNAL_KNOWLEDGE_ONLY低置信、EVID_001标medium，无把预测当实证、无掩盖矛盾；置信表达与证据总体相称。少数广谱降解/酶活性状用medium属单点可接受。取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：列出氧条件、EC/基因、开环结构、菌株保藏/基因组/性状来源等限制；不提供独立验证。
- ANSWER_TEXT / ANSWER.evidence_registry：显示EVID_002为INTERNAL_KNOWLEDGE_ONLY，答案以low置信度标注相关性状。

</details>

## Grok

答案SHA256：`636b5fd4a824350308d8020d1b565130bbc7178e021facaeda916ce897be458e`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案按题面路线名原样填写，覆盖了本题4个必答步骤的对应化学主链，并继续列出下游香草酸→原儿茶酸；每步均给出底物/产物英文名与SMILES、一个酶对象和一个微生物对象，同一SYK-6去重为ORG_001，15项性状全部出现且未知项用null。扣分点为：5步EC均为null（虽符合未知填null纪律，但题面要求的EC字段整体未实质填写），且题面氧条件为null而route_scope填aerobic并附说明，属于披露后的假设而非擅自改选已指定条件；另有6项性状为null。整体属大部分必要内容完整、关联清楚，少量字段缺失/假设，未达9–10的‘全部适用要求均被实质回应’标准。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案覆盖所述主链步骤、酶/微生物字段、15项性状与null未知项，可作为D1完整性与任务符合度定位。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_079：本题gold ordered_step_count=4，LINEAR_UNIQUE；用于核对必答主链规模，不把gold下游或旁支自动作为D1缺步分母。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_079：路径名称及terminal main product=Vanillate，用于判断答案额外S5属下游延续而非必答主链缺步。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 4个必答步骤的主有机转化与gold一致：S1 O-脱甲基化生成三羟基甲氧基联苯二羧酸和甲醛；S2外二醇开环生成间位裂解产物；S3水解生成5-羧基香草酸和4-羧基-2-羟基戊-2,4-二烯酸；S4脱羧生成香草酸和CO2。S5香草酸→原儿茶酸属题面/gold终点下游延续，按P29不额外加分也不扣D2。主要化学骨架、方向与连接均成立；仅见局部辅因子/小分子遗漏（S1未列NADH/H+/H2O/NAD+，S2/S3未列H+，S4未列H+）及S2/S3不标双键立体化学，按P103–P104属局部计量/表达缺陷，不构成关键错误。D2程序上限为8且9–10证据门未开，给8需明确理由：主链转化充分且仅有局部辅因子省略，不改主要结论。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案逐步给出主底物/主产物、反应类型和SMILES；S1–S4对应gold四步，S5为下游延续。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：gold四步反应的主底物/主产物、方向与连接：S01 O-脱甲基化、S04开环、S02水解、S03脱羧至Vanillate。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_079：gold酶名/EC粒度：5,5&#x27;-dehydrodivanillate O-demethylase、OH-DDVA meta-cleavage compound hydrolase、5-carboxyvanillate decarboxylase、2,2&#x27;,3-trihydroxy-3&#x27;-methoxy-5,5&#x27;-dicarboxybiphenyl dioxygenase。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_079：gold terminal main product为Vanillate；S5原儿茶酸为下游延续，不作为主链缺步扣分。

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步必答目标反应分别由答案S1/S2/S3/S4覆盖，并与accepted enzyme names（S01/S04/S02/S03）逐字匹配；所有EC均诚实填null，accepted sets为G4策展粒度，缺EC不自动否定已可识别的酶功能。答案额外给出的S5不是必答目标，不能抬高目标信用。由于表示等价性仍未正式确认、无显式EC且自动target mapping仍为U，9-10被证据门阻断；在&#91;1,8&#93;内取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：Shows delivered enzyme names and null EC; does not by itself verify catalytic activity.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_079：Supports G4 curation-level enzyme names and accepted EC families for the four required reactions; does not prove specific protein activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：Supports reaction direction and step identity at gold level; does not resolve representation equivalence.

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所有步骤都绑定Sphingobium sp. SYK-6，并在organism_profiles中给出同一菌株；gold各步organism为Sphingomonas sp. SYK6 TaxID 502559，答案用常见现用名Sphingobium sp. SYK-6但未给TaxID。该同株对应在冻结crosswalk中未直接列出，属于命名别名/编号未核的局部问题；gold PATHWAY_COMPLETE支持SYK-6全路径能力。未见跨属或无关类群错误，故给8而不是9-10，不触发关键错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：Shows consistent strain assignment; does not supply TaxID or verify synonym.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_079：Supports Sphingomonas sp. SYK6 step assignments and pathway-complete capability; does not resolve Sphingobium alias by itself.
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_079：Lists verified species-name mappings but does not include Sphingobium/Sphingomonas SYK-6 alias; synonym remains unverified.

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状全部出现；9项非null，6项明确null。gold除F14身份/TaxID外无观测性状值，trait_scoreability_mask也把非F14标为completeness_only而非accuracy；因此不能把未核性状判错，也不能判为已核实正确。已填性状多来自INTERNAL_KNOWLEDGE_ONLY且无raw_text/记录，适用性和准确性只获部分支持；F14为null与gold只给TaxID、未给genome_size/gc并不冲突。按性状重要度及证据不足定6，完成度缺失不在此重复重罚。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：Shows delivered trait values and explicit nulls; does not verify trait accuracy.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_079：Gold has UNKNOWN for most trait values and only F14 TaxID observed; cannot confirm answer trait values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_079：Marks non-F14 traits completeness_only and F14 observed_accuracy; supports not treating missing values as scientific error.

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的evidence_registry全部为source_type=INTERNAL_KNOWLEDGE_ONLY，无database record_id、DOI或可核数据库条目；E0又为全case EVIDENCE_GAP。因此核心路线/酶/菌/性状组只能是MISSING_SOURCE加UNRESOLVED_SOURCE，而不是已核实错引，不触发D5 cap。由于每步有claim_scope和具体作者/年份/期刊locator，比完全无定位略好，取低档上沿4，而非1-2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：Shows delivered source entries and their internal-only type; does not verify their truth or record identity.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确说明EC未确认、TaxID/保藏号/基因组/温度/pH/盐度未知、SMILES未标立体化学，并把原儿茶酸下游与评分主链分开；不确定性和null披露具体，未系统性把预测写成实证。部分性状值在INTERNAL_KNOWLEDGE_ONLY下给high/medium且无raw_text，属局部过度自信；不构成系统性误导，故9-10被门挡住但8相称。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：Shows uncertainty disclosures and where confidence may exceed delivered support; does not verify the underlying facts.

</details>

## GPT5.6

答案SHA256：`f6aba6864c59711bb25d16642a97a945bb11d8a80f7efac5d86ada2a21531087`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 3–4档：JSON与路线名可读，但仅2步而非gold 4步，两个酶均无EC，15项性状全为null/unknown；覆盖少数必要模块且多处缺步/缺字段。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_079：gold任务要求4步主链；不支持答案仅2步即为完整交付。

</details>

### D2 反应化学科学性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 1–2档：首步以LigW直接氧化裂解联苯生成5-carboxyvanillate，跳过gold S01 O-脱甲基、S04双加氧、S02水解，并以protocatechuate为终点而非vanillate；主链核心转化错误且不连续。给2因5-carboxyvanillate是gold真实中间体，但只属局部可辨认信息，不构成目标主链。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_079：gold主链为S01 O-脱甲基→S04双加氧→S02水解→S03脱羧至Vanillate；不支持直接裂解至5-carboxyvanillate再至protocatechuate。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a 1–2档：四目标步均无完整目标反应信用；S01酶名/反应不符，S03酶名与accepted有局部匹配但产物为protocatechuate而非vanillate且无EC，S02/S04未交付。给2仅因S03酶名局部可辨认，错误路线内部酶自洽不获目标信用。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_079：gold S01为5,5&#x27;-dehydrodivanillate O-demethylase，S03为5-carboxyvanillate decarboxylase；不支持LigW直接裂解或LigX生成protocatechuate。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b 7–8档：菌株SYK-6与gold所有步骤的Sphingomonas sp. SYK6在菌株层级对应，且gold标注该TaxID 502559为pathway_complete；答案的complete_pathway_organism_profile_id=ORG_001有依据。仅因属名写作Sphingobium sp.、TaxID为null、物种/菌株身份细节需确认，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_079：gold所有步骤为Sphingomonas sp. SYK6（TaxID 502559），并标注pathway_complete=TRUE；支持SYK-6菌株身份与整路能力，不等于答案具体属名写法已逐字核实。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4按P44：15项必需性状全部为null/unknown，无可评价性状观测；记MISSING=1，不宣称检测到科学错误，完成度不足主要已在D1体现。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_079：gold 15项中除F14 TaxID外均为UNKNOWN；说明本题性状观测稀缺，但不回填答案缺失的性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_079：多数性状scoreable=FALSE、denominator_role=completeness_only；仅F14为observed_accuracy，不能把全null性状当已交付观测。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 1–2档：evidence_registry仅EVID_001/EVID_002，source_type=LITERATURE_DIRECT，但database/record_id/locator均为null，无作者/年份/DOI/条目可定位；重要结论几乎无法追查。无已核虚构或错引，按缺失/不可定位低档，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案只给内部EVID标签与笼统LITERATURE_DIRECT，无可定位外部记录；不支持可追溯性。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 7–8档：答案明确列出氧条件未指定、EC未确认、保藏号/TaxID/基因组未确认、15项性状无来源记unknown；证据性质与未知披露较清楚。中等置信包装路线结论略偏强，但未系统性把预测写成实证，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案披露了EC、TaxID、性状等未知；不证明其路线科学正确。

</details>
