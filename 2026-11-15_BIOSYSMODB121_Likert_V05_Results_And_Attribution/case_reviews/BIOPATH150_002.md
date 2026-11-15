# BIOPATH150_002：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：Asulam pathway

污染物：Asulam；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 56 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 28.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 26 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 33.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 21.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 23.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`361ea2cd21062065200431b9e43bdc8bdc4ff99097f9ab95efd96db70623d753`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 路线名、好氧条件与7步连续主链均已给出，主要模块有涉及；但S1/S2两步的enzyme与microorganism均为null，任务明确要求每步一个首选酶/EC和一个对应微生物，且多个性状为未知，属于必要内容遗漏而非轻微工程缺陷，故取5-6档下沿。

<details><summary>V0.4理由与本行变化背景</summary>

主链7步、路线名、氧条件、酶/菌/profile与不确定性模块均有交付；但S1/S2两个步骤的酶与微生物整体为null，任务要求的逐步酶菌绑定未完全满足；15项性状中多个明确未知。取5–6档内偏上分，因主要框架完整但必要步骤关联缺失。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求每步给出主底物/主产物、一个首选酶及EC、一个对应微生物，并填写15项性状。
- ANSWER_TEXT / ANSWER.steps：答案给出7步主链，但S1/S2的enzyme与microorganism为null；可支持完整性扣分定位。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_002：gold为BRANCHED_DAG、9步全图材料；不等同于必须交付全部旁支。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 主链化学整体连续：Asulam水解到Sulfanilamide、Sulfanilamide水解到4-Aminobenzenesulfonate、4-Aminobenzenesulfonate双加氧脱氨到4-Sulfocatechol、4-Sulfocatechol开环到3-Sulfomuconate、内酯化到4-Sulfomuconolactone、水解脱磺到Maleylacetate与Sulfite，均与gold相关步的化学方向一致；局部存在辅因子/产物NAD+未写全、S5产物SMILES为null、S7为额外下游延续等小问题，不推翻主链。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S6的化学转化与gold单支主链基本吻合：Asulam水解到Sulfanilamide，再水解到Sulfanilic acid，经4-aminobenzenesulfonate 3,4-dioxygenase到4-Sulfocatechol，再开环、内酯化、水解脱磺到Maleylacetate与sulfite；S7以maleylacetate reductase到3-oxoadipate，属gold终点外下游延续，未见明显化学方向或原子守恒硬伤，且答案有范围说明。少量SMILES/辅因子标注不完整，取7–8档内偏上。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：gold反应行显示各步主底物/主产物方向；支持主链化学连续性核对，不证明替代酶或具体菌能力。
- ANSWER_TEXT / ANSWER.steps：答案给出连续7步及SMILES/反应类型；可定位局部辅因子与空SMILES问题。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_002：gold terminal含Maleylacetate/Sulfite等；答案额外延续至3-Oxoadipate不自动构成主链化学错误。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 按认可主链 P002_1 评六步：S05 Asulam→Sulfanilamide 与 S06 Sulfanilamide→4-Aminobenzenesulfonate 只给反应而酶/菌为 null，记 M；S01（答 S3）与 S04（答 S6，KEY_TERMINAL）分别有 accepted 酶名支持，记 S；S02（答 S4）ClcA/EC 1.13.11.- 与 S03（答 S5）ClcB/EC 5.5.1.7 非 accepted 匹配且配对未核，记 U。KEY_ENTRY S05 缺酶触发 D-KEY4≤4；可用仅 2/6 且关键入口缺失，不足以给 4，定 3。未选分支 S07-S09 不按全 DAG 计入。

<details><summary>V0.4理由与本行变化背景</summary>

S3酶名与gold的4-aminobenzenesulfonate 3,4-dioxygenase一致但无EC；S4/S5给出的ClcA/ClcB与gold的protocatechuate 3,4-dioxygenase、3-carboxymuconate lactonizing enzyme type 2并非同一具体酶，S5 EC 5.5.1.7与gold 5.5.1.2不同；S1/S2酶完全缺失；S6酶名接近gold但无EC；S7 EC 1.3.1.32合理但未核。存在合理候选与部分对应，但若干关键步骤缺具体核验，取5分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_002：支持 S01/S04 的 accepted 酶名；同时显示 KEY_ENTRY S05 需要 asulam hydrolase，而答案该步 enzyme 为 null。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：定义 P002_1 六步主链的目标反应与底物/产物；不支持把 ClcA/ClcB 作为 S02/S03 的 accepted 匹配。
- RUBRIC_CLAUSE / C04-USER：KEY_ENTRY S05 的已定位缺失触发 D-KEY4≤4，但上界不默认给 4。
- RUBRIC_CLAUSE / C05：在 &#91;1,4&#93; 内按可用目标和关键失败边界选择整数；本例少数目标可用且关键入口缺失，取 3 而非上沿 4。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案给出具体菌株H. intermedia S1与C. testosteroni T-2，且对C. testosteroni给出Junker &amp; Cook 1997文献定位；但H. intermedia S1的步骤归属主要依赖INTERNAL_KNOWLEDGE_ONLY，TaxID 39241及部分反应级能力未获冻结证据核验，且部分步骤菌株与gold organism行不一致；属合理候选与部分支持并存、若干关键身份/能力仍待核，取5-6档下沿。

<details><summary>V0.4理由与本行变化背景</summary>

S3–S7给出了具体菌与步级归属，H. intermedia与C. testosteroni均为真实候选属/种；但S3的H. intermedia S1与gold S01的Sphingomonas sp. strain RW1不同，S4–S7的C. testosteroni T-2不在本题gold步级菌记录中，TaxID 39241与菌株S1均主要依赖内部知识或未核文献。属于有合理候选和部分支持，但若干关键身份与作用范围仍未充分核验，取5–6档内偏上。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_002：gold给出各步已列微生物；未列微生物不等于自动错误，但可显示答案所用菌株需独立身份/能力依据。
- ANSWER_TEXT / ANSWER.evidence_registry：EVID_002为C. testosteroni文献定位；EVID_004/005为INTERNAL_KNOWLEDGE_ONLY，支持范围有限。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 两株菌均按15项外壳返回，部分性状如H. intermedia运动性、杆状、革兰氏阴性、不产孢与gold可观察记录一致；但大量关键项为null或仅INTERNAL_KNOWLEDGE_ONLY，H. intermedia S1身份未绑定到gold 65786，C. testosteroni性状无冻结记录，温度/盐度/pH/基因组等关键定量项多缺；属部分性状可用、关键证据不足，取5档。

<details><summary>V0.4理由与本行变化背景</summary>

ORG_001的氧需求、运动性、杆状、革兰氏阴性、不产孢等与gold可核对性状大体一致，但F8/F9把磺胺酸3,4-双加氧酶活性归给H. intermedia，gold步级记录更支持其protocatechuate 3,4-dioxygenase/后续酶，F14基因组信息在gold有GCA_005938115.1及基因组统计却填null；ORG_002的C. testosteroni T-2性状多为内部知识低置信。部分性状准确且适用，但关键项证据不足，取6分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_002：gold对H. intermedia 65786等给出部分观察性状；可用于对照已给性状，不自动适用于S1菌株。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_002：标记哪些性状有观察值/可评分；支持识别缺失与待核项。
- ANSWER_TEXT / ANSWER.organism_profiles：答案给出两套15项性状及confidence/evidence_id；可定位null与内部知识来源。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案交付了EVID_001–EVID_006：EVID_002有完整文献题名/期刊/年份定位，EVID_001有PPDB Asulam条目locator，但EVID_003仅泛称经典文献，EVID_004/005/006为INTERNAL_KNOWLEDGE_ONLY；核心路线、酶-EC、微生物身份与性状多数组别呈MISSING/GENERIC/UNRESOLVED混合，部分关键结论可定位、其他模块仍缺映射或可核内容，符合5-6档但取5。E0_EVIDENCE_GAP下未核不等于虚构，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

D5按claim group看来源交付：EVID_002给出Junker &amp; Cook 1997具体文献，S4–S7/ORG_002有部分可定位关联；但S1仅PPDB条目名且无record_id，S2/EVID_006为INTERNAL_KNOWLEDGE_ONLY，S3/EVID_003为笼统经典文献，S3/S6关键酶无EC条目，TaxID 39241与两菌性状亦为内部知识。决策相关组非全部笼统，但多处缺映射且E0无法核对，取5档下沿。无已核实错引，不触发D5 cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：可定位交付来源类型、locator与claim_scope；支持D5按实际交付记录评档。
- RUBRIC_CLAUSE / R2-06：D5六状态与claim group登记口径；UNRESOLVED_SOURCE待核不自动cap、不判虚构。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案多处明确填null/unknown，confidence多为low/medium，uncertainties逐条列出未核对项（S1/S2无酶无菌、TaxID/EC基于内部知识、SMILES未确证等），未把预测系统性写成实证；仅个别内部知识断言仍偏强，但已作待核声明，整体披露质量较好，取7-8档上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

答案对S1/S2未确证、S3/S6低置信、C. testosteroni/TaxID与EC编号未逐条核对、4-sulfomuconolactone SMILES未确证等均作了明确披露；未知项多填null，confidence使用low/medium/unknown。主要限制与待验证点较清楚，未见系统性把预测写成实证；取7–8档内偏上。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：列出S1/S2缺酶缺菌、EC/TaxID内部知识、SMILES未确证等限制；支持D6披露质量评价。
- ANSWER_TEXT / ANSWER.steps&#91;&#93;.confidence：步骤与性状confidence字段区分low/medium/unknown；支持证据性质标注核对。

</details>

## DeepSeek

答案SHA256：`7d0bbf5186561cef162ca17c165a71936a604059b0a058a5a1ce5a6f7fcf02fc`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> Route name and aerobic condition are echoed, but after Asulam→Sulfanilamide (gold S05) the answer substitutes a different chain to 4-aminophenol, benzoquinone, hydroquinone and β-ketoadipate, ending outside the gold terminal products. Only one target step is clearly recognizable. Because the branch-case current_path_id is unbound I do not use all 9 gold rows as a default missing-step denominator, but the independently delivered route still deviates from the task-locked Asulam main route; within &#91;1,4&#93;, score 3.

<details><summary>V0.4理由与本行变化背景</summary>

覆盖登记：路径已给出（7步）、酶部分给出（7步均有酶名但仅S1/S5有EC）、微生物已给出（单一ORG_001、无TaxID）、性状明确未知（15项全null）、来源未提供、不确定性未提供。主要模块均有涉及，但来源整块缺失、性状全空、多数步骤无EC，属5–6档“若干必要内容遗漏/仅占位”，取5。路线名与好氧条件按题面原样回显、JSON可解析；路线化学偏离属D2判据（OBS-D1D2），不在D1连坐。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.route_summary：Shows the answer&#x27;s declared Asulam pathway and its delivered 7-step branch; does not by itself establish task-route conformity.
- GOLD_SLICE / reaction_gold.tsv：Shows gold Asulam→Sulfanilamide at S05 and Sulfanilamide→4-Aminobenzenesulfonate at S06; does not support the answer&#x27;s 4-aminophenol branch as the Asulam main chain.

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分3 → V0.5新分4，变化+1。

新裁判理由：

> The first step Asulam→Sulfanilamide is chemically recognizable, and the later quinone/hydroquinone/ring-cleavage/maleylacetate segment is internally continuous. However the central S2 Sulfanilamide→4-Aminophenol is stated as a monooxygenation while the SMILES-level equation drops the sulfonamide sulfur and nitrogen without byproducts, so the core connection is not atom-balanced; it also diverges from the gold S06 reaction. Under the D2 cap for a core unbalanced/foreign central transformation, score 4 within the &#91;1,6&#93; allowed range.

<details><summary>V0.4理由与本行变化背景</summary>

四步判断：①题面指定路线名Asulam pathway（未列唯一步骤序列）；②答案未声明替代路线或范围边界，直接以该名交付；③无可核证据（evidence_registry为空）；④偏离使主要结论失效——S2把磺胺经“单加氧”写成4-氨基苯酚，净脱去磺酰基并以羟基取代，单步单加氧不能完成该转化，属无依据跳跃/违反基本化学约束；主链自S2起改走4-氨基苯酚→苯醌→氢醌→4-羟基粘康酸半醛的通用酚降解支路，不再是gold的磺酸化支路（磺胺→4-氨基苯磺酸→3,4-二羟基苯磺酸→…→Maleylacetate+Sulfite）。D2关键错误成立，cap≤4；首步与gold一致、S3–S7内部化学大致可行，档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.steps.S2：Shows the substrate/product pair and reaction_type=monooxygenation; supports the atom-balance/foreign-connection concern.
- GOLD_SLICE / reaction_gold.tsv：Shows gold S06 is Sulfanilamide→4-Aminobenzenesulfonate; does not support Sulfanilamide→4-Aminophenol.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 题面锁定 Asulam pathway，任务范围为完整 gold 主链，n_required=9。答案 S1（Asulam→Sulfanilamide，asulam hydrolase）与 gold S05 功能层对应：酶名命中 accepted asulam hydrolase，且 3.5.1.86 落在 accepted 3.5.1.- 范围内，计 1 个 S。答案 S2 给 Sulfanilamide→4-Aminophenol（monooxygenase），而 gold S06 是 Sulfanilamide→4-Aminobenzenesulfonate（sulfanilamide hydrolase），故 S06 为已核目标失败 F。S3-S7 为 4-aminophenol/benzoquinone/hydroquinone/4-hydroxymuconic semialdehyde/β-ketoadipate 的离金路线，不交付 S01-S04、S07-S09，这些必答目标缺失，其中 S04、S08 为 KEY_TERMINAL 且明确漏答。按 N=9，S=1、F=1、M=7，C=1/9&lt;0.20，落入&#91;1,2&#93;；有一个正确入口步骤提供少量可用目标信息，但核心主链与关键终点失败，故取 2。

<details><summary>V0.4理由与本行变化背景</summary>

7步酶名与所写反应类型内部基本自洽（水解/单加氧/氧化/还原/开环/脱氢/还原），但仅S1（EC 3.5.1.86）、S5（EC 1.13.11.24）给出EC，其余全null；S1与gold通配EC 3.5.1.-同亚类，按四.5保守条款不判错；两具体EC在E0无冻结记录→UNRESOLVED待核，不判虚构。S2酶名与其转化本身的匹配问题属D2化学判据（OBS-D3A-D5：错引归D5，不作D3a KE依据），此处不重复计为独立关键错误。属“有合理候选和部分支持，但若干关键步骤仍缺具体核验”5–6档，取5；无已核实关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_002：支持题面起点为 Asulam、好氧条件；不支持答案后续离金步骤为 gold 目标反应
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：支持答案 S1 的底物/产物与 gold S05 对应；不支持后续离金步骤
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_002：支持 S05 的 accepted 酶名；答案 EC 3.5.1.86 为 3.5.1.- 下的具体化，可作功能层支持，不证明具体蛋白实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：支持答案 S2 的产物 4-Aminophenol 与 gold S06 不一致，构成 S06 目标失败；不证明其酶功能正确
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：支持 S04、S08 为 gold 终点反应且答案未交付相应底物/反应，构成关键终点漏答
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_002：支持本题为分支 DAG、原始必答步数为 9；不支持把离金分支计入目标完成
- ANSWER_TEXT / ANSWER：显示答案给出 Asulam→Sulfanilamide 后转入 4-aminophenol/benzoquinone/hydroquinone 等离金路线，未给 S01-S04/S07-S09 目标反应

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Pseudomonas sp. has species-level support in the gold organism slice for several Asulam-pathway steps and for pathway_complete, but the answer adds strain ATCC 13985 with no TaxID or strain-level evidence and assigns the same strain to every step, including non-gold transformations. This gives a plausible partial candidate, yet key strain identity and step-level capability scope remain unverified; within the 5–6 band choose 5.

<details><summary>V0.4理由与本行变化背景</summary>

全部7步归属同一Pseudomonas sp. ATCC 13985（ORG_001），无TaxID、无步级或全路径能力证据。正向上，Pseudomonas sp.在gold中为本题步骤菌（S05/S06/S07/S09）且PATHWAY_COMPLETE行含TaxID 306，物种级归属有合理性；但菌株级身份（ATCC 13985）与反应级/全路径能力均无证据（E0 GAP→UNRESOLVED，未核≠虚构），且该菌被用于非gold步骤。按八.D3b身份阶梯：无已核实的同物种异菌株或跨类群错配，不cap；属“合理候选和部分支持，但关键身份与作用范围未充分核验”5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.organism_profiles.ORG_001：Shows the answer&#x27;s claimed strain and full-pathway organism profile; does not verify ATCC 13985 or step capabilities.
- GOLD_SLICE / organism_gold.tsv：Supports Pseudomonas sp. at species/taxon level for some gold steps and pathway completeness; does not establish the specific strain ATCC 13985 or non-gold step capabilities.

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> The answer returns all 15 trait keys but every value is null/unknown for the only organism profile. Under the rubric&#x27;s all-null trait rule, D4 is recorded as MISSING=1 rather than fabricating trait errors; completion deficiency is reflected here while D1 carries the broader delivery issue.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状（F1–F15）全部以null/unknown占位，未交付任何性状值、单位、条件或来源；按P44“全部必需性状均为null/空值时同样处理——D4按MISSING记1分，不宣称检测到科学错误”执行。性状缺失的完成度扣分已在D1体现，此处不重复重扣（P112）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.organism_profiles.ORG_001.traits：Shows all required trait values are null or unknown; no usable trait values were delivered.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> The evidence_registry is empty and every evidence_id is null; no route, enzyme-EC, microorganism, trait, or confidence claim is tied to a locatable source. This is MISSING_SOURCE across the relevant claim groups, not a verified mis-citation. The answer therefore falls in the lowest D5 band.

<details><summary>V0.4理由与本行变化背景</summary>

答案未交付任何来源：evidence_registry=&#91;&#93;，各步reaction_evidence_id/trait_evidence_id=null，enzyme/microorganism evidence_id=null，仅有medium/low/unknown置信标签（属INTERNAL_KNOWLEDGE_ONLY式自我声明）。全部claim组为MISSING_SOURCE，无条目级可定位可核对结论，属1–2档“几乎无法定位重要结论依据”，取2。MISSING_SOURCE是缺失而非误导，按P34默认不触发关键错误cap；E0为EVIDENCE_GAP，编号类声称保持UNRESOLVED待核，不判虚构、不计已核实关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.evidence_registry：Shows the registry is empty; no source can be located.
- ANSWER_TEXT / answer.route_summary：Shows route assertions are presented without source locators.

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> The answer gives some confidence labels (medium/low/unknown) and honestly nulls all traits, but it states the route as a factual degradation pathway with medium confidence for unsourced enzyme/organism claims, sets a complete-pathway organism profile, and provides no explicit limitation or evidence-type disclosure. This is multiple overconfidence/evidence-nature problems without systematic fabrication; 3–4 band, score 4.

<details><summary>V0.4理由与本行变化背景</summary>

F1–F15全部标unknown、未编造数值（正面）；但主链7步中5步标medium、2步low且evidence_id全为null（无来源却给中等置信），uncertainties=&#91;&#93;，未说明路线依据、替代路线可能性、证据类型或主要限制，route_summary以断言语气陈述未经核验的主链。属“多处过度确信，主要限制未说明”3–4档，取4；尚未达到“系统性把预测写成实证/掩盖已知矛盾”的cap程度（无明知掩盖证据，且性状为诚实unknown），不cap。D5缺失不自动联动D6（P121）。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer.route_summary：Shows definitive route language and confidence labels despite null evidence IDs.
- ANSWER_TEXT / answer.steps.S1：Shows medium confidence assigned without an evidence_id.

</details>

## Kimi

答案SHA256：`c1a45413257cb682d95891932bf676ebfd79c759e4ab41b7f29811f13c33c12c`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 按1–2档：多数必要模块缺失。答案只给出1个水解反应步骤，且enzyme=null、microorganism=null、organism_profiles=&#91;&#93;，没有15项性状；仅因仍能辨认Asulam水解为Sulfanilamide这一局部步骤，取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求逐步给出主底物/主产物（含SMILES）+一个首选酶（含EC）+一个对应微生物，并一次返回15项性状；冻结gold该路线共9步。答案只交付1步（对应gold S05），8步缺失，enzyme与microorganism全为null，organism_profiles为空数组（15项性状0项），属&#x27;大部分必要内容缺失&#x27;的1–2档；考虑JSON完整、首步化学可读、未知声明诚实，取档内2分。按八.D1&#x27;核心任务模块大部缺失&#x27;触发关键错误，cap≤4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：证明答案只交付一个反应步骤且未交付酶、微生物和性状模块；不证明该步科学正确。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_002：仅用于说明参考图含多步/分支材料，不据此把全部分支强制作为缺步分母。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 3–4档：仅交付的S1水解步骤在底物/产物方向上与gold S05一致，Asulam→Sulfanilamide并释放甲醇/CO2在化学上可成立；但主链在Sulfanilamide处被截断，缺少后续主链连续性，且把该步当作路线终点，故取3。

<details><summary>V0.4理由与本行变化背景</summary>

已交付的唯一一步化学成立：Asulam+H2O→Sulfanilamide+Methanol+CO2（C8H10N2O4S+H2O=C8H12N2O5S，两侧一致），方向为底物→产物，与gold S05（asulam hydrolase）一致，无反转、无不守恒、无无依据跳步。但主链在9步中只完成1步，S06（sulfanilamide hydrolase）至S04（maleylate/sulfite）等关键下游转化全部缺位，属&#x27;主干部分成立，关键转化仍需补全&#x27;的5–6档，取5分；答案已声明范围边界，故不触发D2关键错误（四.5第2步已声明）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：支持该单步的底物/产物与降解方向；不证明Sulfanilamide是路线终点，也不证明酶/微生物。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_002：说明参考路线不止一个步骤且有其他终点；不要求全部旁支都交付。

</details>

### D3a 目标反应与酶对应：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 酶模块整体未交付：唯一交付步骤的enzyme为null，全文没有酶名或EC，无法按目标反应粒度评价酶对应；按C04.2与SCORING_FLOW_FIX，D3a记MISSING=1。

<details><summary>V0.4理由与本行变化背景</summary>

按P44：该维对应模块确未交付，记1分并标MISSING，不宣称检测到酶学错误。答案对唯一一步把enzyme整体填null，全篇无任何酶名、EC或基因/蛋白标识，属于无酶内容可评；其&#x27;酶未鉴定&#x27;的诚实声明属完成度问题，已在D1计。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.enzyme：证明酶模块未交付；不证明该反应没有酶或该反应错误。

</details>

### D3b 微生物身份与能力：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 微生物模块整体未交付：steps&#91;0&#93;.microorganism=null，organism_profiles为空，没有物种/菌株身份、TaxID、保藏号或步级归属；按P44记MISSING=1。

<details><summary>V0.4理由与本行变化背景</summary>

按P44：微生物模块确未交付，记1分并标MISSING，不宣称检测到身份或能力错误。steps&#91;0&#93;.microorganism 整体为null，organism_profiles为空数组，既无物种/菌株身份，也无步级归属或全路径能力声称。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：证明微生物身份及步级归属未交付；不证明任何具体菌不能完成该步。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 性状模块整体未交付：没有organism_profiles，也没有任何15项性状记录；按P44及P15口径记MISSING=1，不宣称检测到具体性状错误。

<details><summary>V0.4理由与本行变化背景</summary>

按P44及其v0.3括注：全部必需性状均为null/空值时按MISSING记1分，不宣称检测到科学错误。答案organism_profiles为空数组，15项性状无一项以字段形式出现（filled=0, explicit_unknown=0, omitted=15）；&#x27;因菌未鉴定故不给性状&#x27;的说明登记在D1完成度与D6披露，不在D4重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：证明15项性状记录未交付；不证明任何具体性状错误。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分3 → V0.5新分4，变化+1。

新裁判理由：

> 3–4档：仅对单步反应给出EVID_001（EAWAG-BBD/UM-BBD，record_id=Asulam Pathway，无locator），且E0为EVIDENCE_GAP无法核验；CG03/CG05/CG07及性状组无来源。未发现经核实的错引，故不cap；因至少有一个反应级数据库条目但不可核对，取4。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07等）中仅CG01–CG03有一个pathway级指针（EAWAG-BBD &#x27;Asulam Pathway&#x27;，DATABASE_DIRECT/medium，locator为空），不可条目级定位；酶（CG05）、核心菌身份（CG07）、步级归属（CG08）、全路径能力（CG09）与全部性状组（CG10–CG14）均无来源（MISSING_SOURCE）。没有任何条目级可定位可核对的结论，落在&#x27;仅给笼统库源、结论与来源关联很弱&#x27;的3–4档；鉴于首步反应有明确数据库指向且未编造引用，取档内3分。&#x27;数据库仅记录一步&#x27;的引用-声称链在E0无记录可核→UNRESOLVED，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示答案实际交付的来源记录；EVID_001无locator，EVID_002仅为内部知识。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 5–6档：答案明确把enzyme、microorganism、EC和性状缺失列为未知，并区分DATABASE_DIRECT与INTERNAL_KNOWLEDGE_ONLY；但把“Asulam pathway只有一步、Sulfanilamide为终点”作为较确定的路线结论，未标记为主要不确定性，且与gold的多步/其他终点材料相冲突，故取6。

<details><summary>V0.4理由与本行变化背景</summary>

正面：答案区分数据库已记录与文献报道、明确声明酶与微生物未鉴定、把N-乙酰化支路标为INTERNAL_KNOWLEDGE_ONLY/low并声明不属于评分主链，列出4条不确定性与置信标签，披露具体诚实。扣分点：以DATABASE_DIRECT+medium包装&#x27;该路线仅明确记录一步、下游未记录&#x27;这一未经核实的收录范围断言且零披露其不确定性，属单点过度确信（P119）而非系统性误导，按档内扣至6分；不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案对酶、微生物、后续步骤和N-乙酰化支路的不确定性披露；不证明路线终点判断正确。

</details>

## Qwen

答案SHA256：`2caed8ef43498f3f503d7ab4473242a9ba8f8e1dc4134fb60a1764d2d119d800`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 仅交付一个起始水解步骤，且答案自述后续步骤未纳入；没有形成从Asulam到终点的完整或可辨认主链。未把全图分支步数当作缺步分母，但即使不选分支，答案也明确缺少主链与终点交付，故落入1–2档；因仍有一个可辨认步骤和基础字段，取2。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求Asulam pathway主链逐步交付；答案只交付S1起始水解一步，并明确后续未纳入，formal_cases登记该主链ordered_step_count=9。核心任务模块大部缺失，D1按1–2档取2：仍保留起始底物、路线名与好氧条件，且诚实声明后续证据不足，故不取1。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_002_answer：仅证明答案自限为单一步骤，不证明其科学正确性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_002：证明本案为BRANCHED_DAG及全图材料规模；不直接作为未绑定主链的缺步分母。

</details>

### D2 反应化学科学性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 唯一给出的反应把任务Asulam结构写成了另一种连接方式，并将水解脱甲氧羰基产物写成4-amino-3-sulfamoylaniline；gold的Asulam水解步骤S05为Asulam→Sulfanilamide。主链首步核心转化与产物均不符，落入1–2档；因仍表达了一个水解步骤概念，取2。

<details><summary>V0.4理由与本行变化背景</summary>

首步水解产物写成4-amino-3-sulfamoylaniline（SMILES含两个环外氨基加磺酰胺），与gold S05的Sulfanilamide不一致；按答案反应式计量出现额外N/不守恒。D2按1–2档取2：起始底物与水解类型方向正确，但唯一主链步骤的核心产物错误，后续主链断裂，不能构成可信路径。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_002：任务Asulam的冻结身份SMILES；不支持答案中的另一种Asulam连接方式。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：gold S05为Asulam→Sulfanilamide；不支持答案的4-amino-3-sulfamoylaniline产物。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 仅交付1步（steps&#91;0&#93;），可映射到KEY入口S05：底物Asulam和酶名asulam hydrolase与参考S05相符，但产物名称/ SMILES为二氨基磺酰胺类，并非参考Sulfanilamide，且EC为null；其余S01-S04、S06-S09共8个必答目标均未交付。因此S=0，S05为已核KEY目标失败，8步为M；覆盖率0按&#91;1,2&#93;，KEY上限≤4不抬分，局部仅有底物/酶名对应，选2。

<details><summary>V0.4理由与本行变化背景</summary>

酶名asulam hydrolase与gold S05名称一致，方向合理；但EC、gene_or_protein均null，唯一证据为INTERNAL_KNOWLEDGE_ONLY，且针对的产物写错。D3a按5–6档取5：有合理候选和部分支持，关键EC/具体催化证据不足。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：支持S05目标反应为Asulam -&gt; Sulfanilamide；不支持答案所给二氨基磺酰胺产物。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_002：支持S05 accepted酶名为asulam hydrolase且EC为3.5.1.-；不证明答案产物正确或缺失EC可补足反应失败。
- ANSWER_TEXT / steps&#91;0&#93;：答案将产物写成4-amino-3-sulfamoylaniline，SMILES含两个环氨基，和参考Sulfanilamide结构不符。
- ANSWER_TEXT / steps：答案只交付一个步骤，未交付S01-S04及S06-S09的8个必答目标步骤。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案只给Pseudomonas sp. AS-1。gold在S05 asulam hydrolase下列出Pseudomonas sp.（TaxID 306），故属/种级步骤归属有部分支持；但AS-1菌株级身份、TaxID及菌株级能力均无冻结记录，且答案未声称全路径能力。按5–6档“合理候选但关键身份/作用范围未充分核验”，取5。

<details><summary>V0.4理由与本行变化背景</summary>

推荐Pseudomonas sp. AS-1。gold S05的asulam hydrolase有Pseudomonas sp.（TaxID 306），支持属级候选与单步反应关联；但AS-1菌株、TaxID、保藏/基因组信息均无记录，属菌株级身份粒度不足/未核。D3b按5–6档取5：合理候选和部分支持，关键身份未充分核验；E0整题GAP，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_002：支持Pseudomonas sp.为S05 asulam hydrolase的步骤级归属；不支持AS-1菌株或全路径能力。
- ANSWER_TEXT / BIOPATH150_002_answer：证明答案交付的菌株级身份字段；不证明该菌株真实存在。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 15项字段均出现，4项有值、11项明确未知。F9“具有磺草灵水解酶活性”有Pseudomonas sp.在S05的步骤级关联支持；F1“好氧”、F7“可利用磺草灵作为碳源/底物”、F8“可降解磺草灵”均无AS-1菌株级或相应性状证据，且F7/F8从单步酶关联外推到底物利用/广降解。按5–6档“部分性状可用但关键项证据不足”，取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项字段齐全，4项有值（F1/F7/F8/F9）均为低置信内部知识，其余11项明确null。F9水解酶活性有gold S05属级单步支持；F7/F8把单步酶活性外推为底物利用/降解能力，缺适用证据；F1无gold观测。D4按3–4档取4：部分性状可能合理，但关键项证据不足且有外推。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_002：说明gold对Pseudomonas sp.这些性状无观测值；不把UNKNOWN当作CONTRADICTED。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_002：仅支持步骤级asulam hydrolase菌属关联，不外推到碳源利用或广降解表型。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 唯一证据EVID_001的source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，无法定位到任何外部条目或计算记录；决策相关claim组均无条目级可核来源。没有已核实错引，故不cap；按“几乎无法定位重要结论依据”落入1–2档，因至少存在evidence_id与claim_scope映射，取2。

<details><summary>V0.4理由与本行变化背景</summary>

全部结论只由EVID_001支撑，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null；无文献、数据库或计算记录可定位。按六状态逐组登记为MISSING_SOURCE；E0整题EVIDENCE_GAP，编号/性状声称保持UNRESOLVED，不判虚构/错引。D5按1–2档取2；MISSING_SOURCE默认不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_002_answer：证明原交付只有内部知识自述，没有可定位外部来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案多处明确标注low/unknown、null与证据不足，uncertainties具体说明后续中间体/酶/菌株鉴定缺口；未伪造EC、TaxID或多数性状。仅“当前可确认/仅确认起始水解反应”略有证据强度过高，但整体披露充分。按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露较充分：route_scope.notes、route_summary、uncertainties明确后续中间体/酶/菌证据不足，EC/gene及多数性状null，confidence多为low/unknown；未把预测标成实验观测。扣分点：&#x27;当前可确认的主链起始步骤&#x27;措辞偏强；F7/F8/F9为低置信内部推断，证据性质标注仍较粗。D6按7–8档取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_002_answer：证明答案对未知和限制有具体披露；不证明其科学正确。

</details>

## Grok

答案SHA256：`e0b8d382cd293b17c9dd6de74c9bf92a6f165d1de5fcebbd3bc2d99a2e86cd0d`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1按1–2档取2：题面要求9步主链、每步酶/EC与对应微生物、15项性状；答案仅交付1步化学转化，酶、微生物、organism_profiles和15项性状均未交付，且未达主链终点。因仍有可辨认的起点单步、路线名与好氧条件回显，取2而非1；但核心交付缺失构成D1关键错误，cap≤4。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_002：证明交付范围仅有1步且缺失酶/微生物/性状模块；不评价该单步化学正确性。
- QUESTION_TEXT / QUESTION_TEXT_BIOPATH150_002：证明D1必答模块范围；不提供科学正确性证据。

</details>

### D2 反应化学科学性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2按1–2档取2：单步asulam→sulfanilamide的方向与gold S05一致，水解式可配平；但仅此一步，未连接到gold主链终点（S04/S08），无法构成连续可信主链。未把缺步全部机械归入D2，仅就主链断裂与缺乏连续性定档；甲醇/CO2副产物待核不影响本档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：支持gold S05正向反应为Asulam→Sulfanilamide；不证明酶身份、甲醇/CO2副产物或下游步骤。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：显示gold主链另有更远终点（maleylacetate/sulfite、1,2,4-benzenetriol）；不用于自行选择分支主链。

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a按MISSING固定1：程序合同明确整个酶模块未交付（ANSWER.steps&#91;*&#93;.enzyme.name/ec_number全空）。题面要求每步首选酶/EC；虽然S1反应结构可对应S05，但无任何酶名、EC或功能候选，不能给目标酶信用。N=9，S=0、M=1、U=8；缺失位点为steps&#91;0&#93;.enzyme。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_002：证明酶名与EC字段未交付；不评价未交付的酶功能。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b按MISSING固定1：答案未交付任何微生物身份或能力内容。steps&#91;0&#93;.microorganism为null，organism_profiles为空；题面要求每步绑定一个对应微生物。不能评价身份/能力，也不宣称检测到具体微生物错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_002：证明微生物模块完全未交付；不用于判定未提交的微生物身份对错。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4按MISSING固定1：organism_profiles为空，题面要求的15项性状全部未交付。按P44对全部必需性状缺失作MISSING=1处理，不宣称检测到编造；完成度不足已在D1体现，此处不重复重扣。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_002：证明15项性状模块整体未交付；不评价不存在的性状值正确性。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5按1–2档取2：唯一证据EVID_001为INTERNAL_KNOWLEDGE_ONLY，database、record_id、locator均为null，核心结论无法沿可定位来源核查；酶、微生物、性状也未交付，因此来源与生成过程几乎不可追溯。该低分来自MISSING_SOURCE/无法追查，不是已核实虚构；不触发D5错引cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_002：证明唯一来源为内部知识且无定位；不把内部知识自声明升级为可核验来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6按7档：答案明确将酶、EC、菌株、下游步骤留空，区分了内部知识与待核机理，并列出非生物水解可能性与范围限制；未见系统性把预测写成实证。但“已确证主转化”“反复记录”等表述缺少可定位来源，局部置信略强，故不入8–9档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT_BIOPATH150_002：证明答案对未知酶/菌/EC和下游步骤有明确披露；不证明其化学结论已被外部来源支持。

</details>

## GPT5.6

答案SHA256：`9c14ef3a3559c23ddbaaca6165cbcc04cf5bb8e0d26ffa60a26b0f02ff6a153a`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求完整主链、每步首选酶/EC、对应微生物及15项性状。答案只有1个step，enzyme与microorganism均为null，organism_profiles为空，绝大多数必要模块缺失；1–2档内取2，因为路线名、好氧条件和入口底物/产物局部可读，但远未达到完整作答。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求每步酶与微生物及15项性状；不证明答案正确。
- ANSWER_TEXT / ANSWER_BEGIN：仅证明答案只交付一个局部步骤且缺酶、缺微生物、缺性状；不证明任何科学结论。

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2允许范围为&#91;1,4&#93;。答案只给出Asulam经氨基甲酸酯水解生成sulfanilamide（并列出methanol、CO2）的入口局部步骤；该主底物/主产物方向与gold S05一致，方向正确，化学上可解释，但没有后续步骤连接到题面终点，连续性严重不足。因局部入口转化可用而非明显错误，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持已交付的单一入口水解步骤；不支持完整主链或后续步骤。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_002：支持入口主底物/主产物方向；不证明甲醇/CO2为byproduct，也不证明酶或菌活性。

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> C04/P44：唯一交付步骤steps&#91;0&#93;.enzyme整体为null，全案无任何酶名/EC或酶模块，属酶模块整体未交付，D3a=MISSING且score=1。固定release决定允许范围&#91;1,1&#93;；已确认KEY_ENTRY S05的酶信息缺失保留于key_error及missing_basis，不另改分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持酶模块整体未交付；不证明具体酶功能错误。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_002：仅支持S05接受酶名为asulam hydrolase、EC族为3.5.1.-；不支持具体蛋白活性或其它步骤。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求每步绑定一个对应微生物并去重填写organism_profiles；答案steps&#91;0&#93;.microorganism=null且organism_profiles=&#91;&#93;，无任何物种/菌株身份或步级归属可评，按微生物模块整体未交付记MISSING=1。未发现已编造身份，故key_error=N。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持微生物模块整体未交付；不支持任何具体身份或能力结论。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求每个organism_profile一次返回全部15项性状；答案organism_profiles=&#91;&#93;，15项性状均未交付，按D4 MISSING=1。没有编造性状，故key_error=N；缺失完成度已在D1反映，此处不重复判科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持15项性状整体未交付；不支持任何性状值或适用性结论。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案evidence_registry=&#91;&#93;，所有evidence_id均为null；唯一入口转化和未知声明均无可定位来源。D5决策相关组均为MISSING_SOURCE，属于来源缺失而非已核实错引，按低分档记1；不触发D5关键错误cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案未交付任何可定位来源；不支持任何来源真实性或错引结论。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确把酶、EC、对应微生物及下游转化列为未确认，相关字段填null，未编造身份或来源；主要限制与待验证点写清楚。唯一偏强处是入口水解本身以较确定语气陈述而未标注为推断，但不构成系统性误导，故7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案诚实披露酶、菌、下游未知；不证明其化学内容本身正确。

</details>
