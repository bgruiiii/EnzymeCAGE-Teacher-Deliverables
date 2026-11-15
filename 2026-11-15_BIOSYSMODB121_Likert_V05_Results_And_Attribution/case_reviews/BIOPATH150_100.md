# BIOPATH150_100：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-amino-3-hydroxybenzoate degradation

污染物：4-Amino-3-hydroxybenzoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 39.5 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 38.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 56.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 42 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 46 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 22.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`d2564f4dd99a0e12d79203e6e91ae4d5fd6286ff5e6b0f97c17abec37e0bab42`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> Task scope requires a six-step linear main chain. Answer gives four steps, with S2 bound to a nonmatching S04, and required steps S01/S02/S03/S05 absent; all ECs are null and all 15 traits are null. D1 3–4 band: only partial necessary content, multiple missing steps and major missing fields. Score 3 rather than 4 because the omissions affect core completeness.

<details><summary>V0.4理由与本行变化背景</summary>

七类模块均有实质回应：4步主链每步给出底物/产物英文名与SMILES、酶名、对应菌及profile引用；15项性状字段结构齐全；uncertainties与每步uncertainty均有内容。但全部酶的EC为null、15项性状全为显式未知（无任何性状内容）、主链止于4-oxalocrotonate而未延续到gold终点(2Z)-2-hydroxypenta-2,4-dienoate（该下游仅列入本轮不评分的downstream_continuation）。符合5–6档“主要模块均有涉及，但若干必要内容遗漏、仅占位或关联不清”；因结构完整、路线名原样回填题面给定值，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_100：Shows ordered_step_count=6 and LINEAR_UNIQUE, supporting a six-step required main chain; does not by itself prove answer completeness.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：Lists required gold steps S01-S06 and their order; supports missing-step count.
- ANSWER_TEXT / ANSWER：Answer has only four steps and no EC values; supports incomplete delivery.

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The first extradiol cleavage is plausibly representation-equivalent to the gold entry step, and the later S2-S4 sequence is internally coherent as a 2-aminophenol-type analogue. However, the downstream steps differ from the gold main chain, are explicitly analogical, lack direct evidence, and the ordering/intermediates require revision. D2 5–6 band: main trunk partially established; score 5.

<details><summary>V0.4理由与本行变化背景</summary>

首步为extradiol 2,3-加双氧开环（S1：4-Amino-3-hydroxybenzoate + O2 → 2-amino-5-carboxymuconic semialdehyde），与gold首步（BSY-r02960，4-amino-3-hydroxy-benzoate 2,3-dioxygenase，EC-1.13.11，产物BSY-c18180）在反应类型与元素组成上一致，方向正确、无原子明显不守恒。但S2–S4为答案自述的“与2-aminophenol/邻苯二酚间位开裂途径类比推导”，其顺序（醛氧化→脱羧→脱氨，经2-aminomuconate到4-oxalocrotonate）与gold主链顺序（脱氨→脱羧→脱氢→互变→脱羧）不同，且无任何可定位证据；按四.5第3步“无可核证据→按未证实登记，不自动判错也不给高分”。未出现起始步错误、方向反转、无说明跳至中心代谢物等D2关键错误，故不cap；档位取5–6档下沿（主干部分成立、关键中间体与连接需修订、合理性证据有限）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：Shows the gold six-step route and its intermediates; does not support the answer&#x27;s alternative downstream ordering.
- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s proposed extradiol cleavage and downstream analogue route; self-labels S2-S4 as analogical.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> Program facts: S=0, F=1, U=5, N=6; confirmed KEY failure at S04 caps D3a at ≤4. The S04 mismatch is a key enzyme-reaction failure, and the remaining entry/downstream alignments are unresolved. Within the low band, score 2 reflects limited local information (entry enzyme name is plausible) but no confirmed target support and a key failure that invalidates the main enzyme-correspondence conclusion.

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名“4-amino-3-hydroxybenzoate 2,3-dioxygenase”与gold步酶4-amino-3-hydroxy-benzoate 2,3-dioxygenase subunit一致（gold EC 1.13.11），答案EC填null未与之冲突。S2–S4酶名（2-amino-5-carboxymuconic semialdehyde dehydrogenase / 2-amino-5-carboxymuconate decarboxylase / 2-aminomuconate deaminase）与各自所写反应类型自洽（醛氧化-脱羧-水解脱氨），未见酶名与EC互相矛盾（全EC为null避免该矛盾），但均为类比候选、无蛋白/基因标识、无可定位支持，属“有合理候选和部分支持，若干关键步骤仍缺具体核验”（5–6档）；关键步骤酶对应未获证实，取下沿5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_100：Shows accepted enzymes for S01-S06; S04 is 2-amino-5-carboxymuconic 6-semialdehyde deaminase subunit, EC 3.5.99.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：Shows S04 reaction BSY-c18180 to BSY-c17269 with ammonium; does not support the answer&#x27;s S2 dehydrogenase reaction.
- ANSWER_TEXT / ANSWER：Answer S2 uses 2-amino-5-carboxymuconic semialdehyde dehydrogenase and produces 2-amino-5-carboxymuconate.

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> Bordetella sp. 10d is an exact-matched organism for several gold steps and has PATHWAY_COMPLETE TRUE in organism_gold. The answer uses this strain consistently and correctly for the available identity/whole-pathway level. Missing TaxID and unverified alternative-step support keep it at 8 rather than 9.

<details><summary>V0.4理由与本行变化背景</summary>

唯一推荐菌Bordetella sp. 10d与gold organism_gold.tsv中EXACT记录（TaxID 170622，Bacteria）一致，答案未填TaxID、未编造编号；该菌在gold中确为S01/S02/S03/S04/S06的步级菌，且存在PATHWAY_COMPLETE=TRUE行，故“同一菌承担四步”与gold的菌-路径关系不冲突。但四步共用单一profile、步级反应能力均为类比推导、无来源（置信low），属“有合理候选和部分支持，若干关键身份或作用范围仍未充分核验”（5–6档）；因核心身份与gold一致且无身份错配/编造，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_100：Shows Bordetella sp. 10d TaxID 170622 exact-matched for S01/S02/S03/S04/S06 and PATHWAY_COMPLETE TRUE; does not prove every alternative-step activity.
- ANSWER_TEXT / ANSWER：Answer uses Bordetella sp. 10d for its four steps and sets complete_pathway_organism_profile_id=ORG_001.

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> All 15 required traits are present only as null/unknown values. P44 treats all-null/empty required trait output as D4 MISSING=1, not as a detected scientific error.

<details><summary>V0.4理由与本行变化背景</summary>

任务要求每个organism_profile一次返回全部15项性状及各项最强来源；答案唯一profile ORG_001的F1–F15全部为null（confidence=unknown、evidence_id=null），未交付任何可评价的性状内容。按P44“全部必需性状均为null/空值时同样处理——D4按MISSING记1分，不宣称检测到科学错误”，记MISSING=1；该分值按权重参与加权总分与科学子分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all 15 trait values are null/unknown with confidence unknown.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> All evidence_registry entries are INTERNAL_KNOWLEDGE_ONLY with database, record_id, and locator null. This is MISSING_SOURCE rather than verified mis-citation. Claim-to-internal-ID mapping exists, but there is no locatable external traceability for the key route, enzyme, or microorganism claims. D5 low band; score 2.

<details><summary>V0.4理由与本行变化背景</summary>

全部结论只挂INTERNAL_KNOWLEDGE_ONLY自我声明（EVID_001/EVID_002/EVID_003；database、record_id、locator均null），无任何条目级可定位可核对来源；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）状态集均为MISSING_SOURCE。按四.3/P34，MISSING_SOURCE属缺失而非误导，D5按低分档、默认不触发关键错误cap；P41“全部缺失→低分档”。答案对claim_scope的自我标注结构化、未伪装为外部来源，故取低分档上限2（不取1）。本题E0为EVIDENCE_GAP，不产生任何已核实错引，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all sources are INTERNAL_KNOWLEDGE_ONLY with no database/record/locator.
- RUBRIC_CLAUSE / P34：MISSING_SOURCE includes only INTERNAL_KNOWLEDGE_ONLY self-declaration; default no cap.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The answer clearly labels internal knowledge, low/medium confidence, and explicit uncertainties: EC/gene unknown null, S1 product from naming/chemistry, strain from memory, S2-S4 analogical, oxygen condition null but notes aerobic requirement. Main limitations are disclosed; some S1 confidence may be slightly strong, but this is not systemic misleading. D6 7–8 band; score 8.

<details><summary>V0.4理由与本行变化背景</summary>

答案逐条区分“文献记忆/化学推导/类比外推”：route_summary直言S2–S4为类比推导、置信低；uncertainties列明开环产物结构依化学推导、EC与基因名不可确定故填null、菌株归属低置信、脱羧与脱氨先后可能不同、题面未给氧条件而途径实际需分子氧；每步另设uncertainty字段，置信标签low/medium与依据基本相称。仅S1/EVID_001标medium略强于“仅内部知识”的依据，属单点过度确信而非系统性误导，已在档内扣分；未见把预测写成实证观测或掩盖矛盾。取8（9–10档要求“重要结论均合理标注边界”且披露更严密）。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows explicit disclosure of internal knowledge, low/medium confidence, unknown EC/gene, analogical S2-S4, and oxygen-condition caveat.
- RUBRIC_CLAUSE / P119：Separates single-point overconfidence from systemic misleading; disclosure quality is scored independently.

</details>

## DeepSeek

答案SHA256：`1377b116c059d832f006a2c40fb5cbf8b6424ba4b6ddfa61c3c63520f4ffd337`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案可解析，chosen_route_name原样填写，steps与organism_profiles均有内容；但仅4步，多个主产物/中间体SMILES为null，S3/S4酶EC为null，evidence_registry为空，15项性状来源全null，必要字段多处占位。主要模块均有涉及但若干必要内容遗漏、关联不清，落5–6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

路径、酶、微生物、性状四个内容模块均有实质作答：4步主链、每步一个酶名与一个菌名、15项性状字段齐全（9项有值、6项如实null、0项遗漏）；route_scope.chosen_route_name与题面逐字一致，未见更换路线或条件偏离。但&#x27;各项最强来源&#x27;模块整体未交付（evidence_registry为空、全部evidence_id=null），且模板要求的主/产物SMILES除首底物与CO2外均为null，属若干必要内容遗漏而非少量工程缺陷。落5–6档，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION.answer_requirements：要求每步底物/产物英文名及SMILES、酶及EC、微生物，并填15项性状及最强来源
- ANSWER_TEXT / ANSWER.steps：仅4步且多SMILES/EC为空
- ANSWER_TEXT / ANSWER.evidence_registry：证据数组为空，性状evidence_id均为null

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> S1/S2开环与脱氨方向大体可与金标前两步对应，但S1缺O2/H+等计量，S2缺H2O/NH4+；S3将2-羟基-5-羧基粘康酸半醛“氧化”为5-羧基-2-羟基粘康酸，S4再脱羧成2-羟基-2,4-戊二烯酸+CO2。按命名碳数，S4从C7级底物到C5产物+CO2少一个碳，且跳过金标S05→S03→S01→S02的脱羧/脱氢/互变/再脱羧连续转化，主链关键转化不成立。属多个重要步骤错误及明显计量不守恒，D2主要结论失效，cap≤4；前两步部分合理取3。

<details><summary>V0.4理由与本行变化背景</summary>

起始两步成立：S1为2,3-双加氧开环、S2为脱氨，与gold S06/S04一致；终点亦为gold terminal（2-hydroxypenta-2,4-dienoate）。但中段失效：S3以醛氧化(dehydrogenase)生成5-carboxy-2-hydroxymuconate，替代gold S05的脱羧（应生成2-hydroxy-6-oxohexa-2,4-dienoate+CO2）；S4再把该C7化合物一步脱羧为C5终产物并只放出1个CO2，碳数少1且无说明，等价于跳过gold S03/S01/S02三步（dehydrogenase/tautomerase/decarboxylase），全程无简化声明或范围边界声明。主链连续性与计量不成立→关键错误cap≤4；因起始步、方向与终点正确，档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：金标主链S06→S04→S05→S03→S01→S02的底物/产物、方向及终端产物(2Z)-2-羟基戊-2,4-二烯酸；S05为脱羧生成2-羟基-6-氧代己-2,4-二烯酸+CO2，随后还有S03/S01/S02
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_100：终端化合物为(2Z)-2-hydroxypenta-2,4-dienoate，不能由C7中间体一步脱羧到C5+CO2而无碳损失

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 按N=6逐目标看：程序S01-S03为ROUTE_HOLD_REPRESENTATION/UNRESOLVED，S04-S06为ROUTE_BLOCKED_MISSING/UNBOUND；因route_status=BOUNDARY_REVIEW且omission_locator为空，按C03不能把UNBOUND直接当作确证M，故无确认S/F/M，保留U。答案的开环双加氧酶和脱氨酶名称/EC方向与accepted集合局部一致，提供少数目标局部可用信息；但所有配对仍未核，脱氢酶/脱羧酶名称与accepted底物/名称不完全一致，tautomerase及2-oxo-3-hexenedioate decarboxylase无明确对应。核心目标推荐未建立，落3–4档，取3；无已确认KEY失败，key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

S1（4-amino-3-hydroxybenzoate 2,3-dioxygenase，EC 1.13.11.48）与S2（2-amino-5-carboxymuconate semialdehyde deaminase，EC 3.5.99.9）的酶名与gold酶名一致，EC族级（1.13.11 / 3.5.99）与反应类型匹配，未见EC大类与反应类型矛盾、也未见酶名与EC互斥；S3/S4仅给酶名、EC为null（任务允许未知填null），其中S3的dehydrogenase与其自述的氧化反应自洽，与gold实际脱羧步骤的差异属反应本身问题，已在D2计分，不重复计入D3a（OBS-D3A-D5）。但两个具体EC在E0无记录、无法核实，S3/S4完全无EC，关键步骤仍缺具体核验→5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_100：各必答步accepted酶名/EC：S06 1.13.11；S04 3.5.99；S05 NOT_OBSERVED；S03 1.2.1.85；S01 5.3.2.6；S02 4.1.1.77；不证明具体蛋白实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：金标六步主链及方向，用于对照答案酶与底物/产物绑定；UNBOUND不等于答案未交付
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.enzyme：答案仅4个酶；S1双加氧酶EC1.13.11.48，S2脱氨酶EC3.5.99.9，S3脱氢酶EC null，S4脱羧酶EC null

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> TaxID 285/Comamonas testosteroni物种身份有gold物种记录支持；但答案每一步均归给同一物种，step-level催化与全路径能力无交付证据，且gold各步另有Bordetella/Paenibacillus等归属。身份未错，能力/粒度不足，落5-6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份真实且与gold一致：Comamonas testosteroni / TaxID 285在gold物种级记录中为EXACT，未见编造、也未见用序列存在性直接推断整条路径的措辞。但作用范围粒度不足：答案把同一物种用于全部4步（隐含全路径角色，且complete_pathway_organism_profile_id仍为null未显式声明），而gold步级记录中C. testosteroni仅见于S01（tautomerase）与S02（decarboxylase），S1/S2对应步级记录为Bordetella sp. 10d、S05为Paenibacillus sp. JJ-1b；答案未给菌株、未附来源、菌confidence=medium。属&#x27;有合理候选和部分支持，但若干关键身份或作用范围仍未充分核验&#x27;，取5；不cap（gold非穷尽，无已核实身份错配，TaxID 285仍在待核计划内）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_100：支持物种身份及部分步骤关联，不支持答案全部S1-S4的步级催化或全路径能力。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_100：仅支持物种级性状/身份背景，不自动外推为步级反应能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 已给性状中F10 motility、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating与gold观察一致；F1 &#x27;aerobic&#x27;与gold &#x27;aerotolerant&#x27;不完全同义，F7/F8/F15为低置信宽泛声称，F2/F3/F4/F5/F9/F14多为null。部分准确但关键数值/证据不足，5分。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状中F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating与gold观测（285：motility=true、cell shape=rod-shaped、gram positive=false、sporulation=false）一致，属可核实的准确项。但关键项缺口明显：F2温度、F4盐度、F5保藏号、F14基因组在gold中已有观测（10–37℃、0–2% NaCl、JCM 6233、GCA_016599875.1）而答案全为null；F1写&#x27;aerobic&#x27;而gold观测为&#x27;aerotolerant&#x27;，类别不等同；F7/F8/F15为泛化描述且逐项evidence_id=null、confidence=low，无来源支持。属&#x27;部分性状准确且适用，但关键项证据不足&#x27;，取5；缺失的完成度扣分主归D1，此处不重复重扣（八.D4条款）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_100：支持F10-F13等已观察性状；不证明答案F1措辞、F7/F8/F15宽泛声称或未填数值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_100：用于区分可评分观察值与仅完整性字段，不把null自动判错。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry为空，所有step/trait/enzyme/microorganism的evidence_id均为null；无任何可定位文献、数据库或计算记录，D5落1-2档。无已核实错引，不触发cap；取2。

<details><summary>V0.4理由与本行变化背景</summary>

答案的证据登记表整体为空（evidence_registry=&#91;&#93;），所有reaction_evidence_id/trait_evidence_id/enzyme.evidence_id/microorganism.evidence_id/性状evidence_id均为null，且未给任何数据库条目、DOI或计算记录，仅以confidence标签代替来源，属INTERNAL_KNOWLEDGE_ONLY式自我声明→各claim组均为MISSING_SOURCE。任何路径步、酶、菌、性状结论都无法沿记录追到条目。E0为整题EVIDENCE_GAP，编号类断言（EC 1.13.11.48、3.5.99.9、TaxID 285）保持UNRESOLVED，不判虚构、不判CONTRADICTED，故无已核实错引、severity不适用。决策相关组无一条目级可定位证据→D5落低分档（1–2）；按MISSING_SOURCE默认不cap，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：证明答案未交付来源；不支持任何科学声称的可追溯性。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案用confidence low/unknown标示部分缺失，但uncertainties=&#91;&#93;，无文字限制；S1酶标high、EC无来源，S2 medium等，证据性质与置信度未充分解释；属笼统不确定性+局部过度确信，5-6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

正面：对未知项如实置null（F2/F3/F4/F5/F9/F14，以及S3/S4无EC），逐条给出confidence标签，未编造数值或编号来填满字段，故非系统性把预测写成实证。负面：对无任何来源的EC 1.13.11.48给&#x27;high&#x27;、对全部步级菌归属给&#x27;medium&#x27;，未区分观测/预测/内部知识，uncertainties为空，未说明任何限制、矛盾或待验证点，部分结论强度明显超过依据。属&#x27;有不确定性说明但过于笼统、部分结论强度仍超过依据&#x27;的单点过度确信（八.D6/P119），5–6档取5，不cap（无系统性误导、无明知掩盖）。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：证明答案未给出文字不确定性与限制说明；confidence标签本身不等同于证据说明。

</details>

## Kimi

答案SHA256：`898fd74c1afafd0e638e099d678180ad37f7059cfea83ff766982b6d249720e2`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 结构交付较完整：7步均含底物/产物、酶、微生物，15项性状字段齐全且未知项如实为null，去重为一个Bordetella sp. 10d profile。扣分点在于多数性状为明确未知、主链与冻结gold主链的表示边界仍未绑定，且答案未按gold终点收敛；但route diagnosis为BOUNDARY_REVIEW且task_conformance_status=OK，未将其直接按任务偏离cap处理。

<details><summary>V0.4理由与本行变化背景</summary>

七个主链步骤齐备：每步给出英文名+SMILES的底物/产物、一个首选酶（S1的EC诚实填null）、一个对应微生物；同菌按物种+菌株去重为单一ORG_001；route_scope.chosen_route_name逐字为&#x27;4-amino-3-hydroxybenzoate degradation&#x27;，未改选路线；15项性状全部出现（4项填写、11项显式null+unknown），按P15/P45不作为遗漏等同错误但计入完成度不足；alternative_branches的picolinic acid分支明确标注is_part_of_scored_main_route=false。整体落7-8档：大部分必要内容完整、关联清楚；性状模块大面积未知与S1缺EC为少量至中度遗漏，档内取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_100：支持本题为LINEAR_UNIQUE、ordered_step_count=6的冻结任务；不直接证明答案主链等价。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案给出的是4-氨基-3-羟基苯甲酸经2-氨基苯酚的间位开环替代路线；主有机转化方向连贯，S2加入O2、S3加入NAD+、S4脱氨释放铵、S5脱羧、S6水合、S7醛醇裂解，步骤连接与方向总体合理。主要扣分为若干质子/水/辅因子未配平、S1脱羧步骤未给H+，以及部分中间体名称存在互变异构表述边界；按辅因子局部缺陷处理，不因此cap。

<details><summary>V0.4理由与本行变化背景</summary>

逐步化学自洽且主有机碳骨架守恒：S1 4-amino-3-hydroxybenzoate→2-aminophenol+CO2（C7→C6+CO2，脱羧位置与OH/NH2邻位关系相符）；S2 O2参与的1,6-型（间位）开环，C6H7NO+O2→C6H7NO3；S3 NAD+依赖醛脱氢生成2-aminomuconate+NADH；S4 水解脱氨放出NH4+得4-oxalocrotonate；S5 脱羧失CO2得2-oxopent-4-enoate（该步EC 4.1.1.77与gold同一步脱羧酶一致，属正向可定位支持）；S6 水合得4-hydroxy-2-oxovalerate；S7 醛醇裂解得pyruvate+acetaldehyde；辅因子（O2、NAD+/NADH、H2O、CO2、NH4+）在列，方向正确、连接连续，无起始步错误、无无依据跳步、无未说明的不守恒。与gold 6步路线（2,3-双加氧酶起始、终点(2Z)-2-hydroxypenta-2,4-dienoate）不同，但题面只指定路线名未指定化学路线；按四.5四步判断：已声明路线（route_summary/notes）、证据仅部分（EVID_001为自由文本、E0不可核）→登记待独立核验，不判关键错误；越过gold终点继续至中心代谢物按P29不扣分。落7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：提供gold主链方向与终点供对照；不把gold外替代路线自动判错，D2按所答化学自身连续性评价。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 六个必答目标中，答案S5的4-oxalocrotonate decarboxylase/EC 4.1.1.77与gold S02的2-oxo-3-hexenedioate decarboxylase/EC 4.1.1.77在功能层可视为同一脱羧反应，底物/产物为互变异构表示，属于少量可用目标信息。其余目标大多未按gold反应交付：S06入口为脱羧到2-氨基苯酚而非2,3-双加氧开环，S03/S04/S05/S01亦不匹配。覆盖率约1/6，落C&lt;0.20的&#91;1,2&#93;带；核心目标推荐仍失效，取2。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶名与反应类型逐项匹配：1,6-双加氧开环（S2）、NAD+依赖醛脱氢（S3）、水解脱氨（S4）、脱羧（S5）、水合（S6）、醛醇裂解（S7），无EC大类别与反应类型冲突（未出现水解酶解释羟化或加氧酶挂脱氢编号等错配）。EC 4.1.1.77与gold同一步脱羧酶一致（正向可定位）；EC 1.13.11.46、1.2.1.32、3.5.99.5、4.2.1.80、4.1.3.39在E0无记录，gold侧仅为通配1.13.11/3.5.99，无法核对accepted name/reaction与条目状态（四.6），保留待核、不判错。S1整体酶仅给名称、EC与基因/蛋白诚实null并提供uncertainty说明。落6档：有合理候选与部分支持，若干关键步骤仍缺具体核验。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_100：支持gold各必答步酶名/EC；不证明答案替代路线全部目标反应完成。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：支持gold各步反应方向与底物/产物；用于逐目标反应对照。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 微生物身份名称/菌株Bordetella sp. 10d与gold organism记录中的EXACT身份相符，这是加分点；答案未填TaxID，并将S1-S7全部归给同一菌株且声明完整路径能力，但该替代路线下的步级催化与全路径能力仅由EVID_002内部知识支撑，gold的PATHWAY_COMPLETE=FALSE针对gold路径、不能直接证伪替代路线，但也不支持答案的完整路径声称。按身份正确、能力/范围证据不足，落5-6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

身份层可定位：答案所用&#x27;Bordetella sp.&#x27;/&#x27;10d&#x27;与gold organism_gold在S01–S04/S06列出的Bordetella sp. 10d（TaxID 170622，Bacteria）一致，PATHWAY_COMPLETE行同taxid，故不存在跨属/cross-kingdom或编造身份；答案未编造TaxID/保藏号（诚实null），S2 uncertainty自述该酶在Pseudomonas sp. AP-3研究最深入、在10d为功能对应物，未出现&#x27;由基因组存在某酶直接推断完成整条路径&#x27;式越级。能力层：全7步菌-反应归属仅由EVID_002（INTERNAL_KNOWLEDGE_ONLY）支撑，且gold把同一菌置于tautomerase/decarboxylase/dehydrogenase/deaminase/2,3-dioxygenase步，与答案的脱羧酶步、1,6-双加氧酶步归属不一致——但E0无冻结事实记录，不能登记已核实错配，按UNRESOLVED保留。落6档：有合理候选与部分身份支持，关键作用范围未充分核验；不cap（无核实编造、无全路径越级）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_100：支持Bordetella sp. 10d名称/菌株身份及gold路径的PATHWAY_COMPLETE=FALSE；不证明其能完成答案的替代7步路线。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案只给一个Bordetella sp. 10d profile，15项字段齐全但仅F1、F7、F8、F9有值，其余诚实null。关键性状F7/F8/F9直接支撑其降解推荐，却主要依赖EVID_002内部知识；F8写成可完全矿化，证据强度不足。没有发现数值离谱或跨菌株推广的明确错误，但关键项证据不足，落5-6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

唯一profile（Bordetella sp. 10d）15项性状：4项填写（F1 oxygen_tolerance=&#x27;aerobic&#x27;、F7以4-氨基-3-羟基苯甲酸为唯一碳源、F8可降解该污染物及2-氨基苯酚、F9 2-氨基苯酚1,6-双加氧酶活性），confidence low/medium，来源均为EVID_002内部知识；11项显式null+confidence unknown。gold trait_gold对taxid 170622的F1–F15除F14的OrganismTaxID(170622)外均为UNKNOWN，trait_scoreability_mask将该菌绝大多数性状标为completeness_only（F14=observed_accuracy仅TaxID子字段），故答案的null与可得数据一致，属完成度问题（主归D1），不判编造；F14本可引用TaxID 170622而答案留null，属关键信息缺口。已填4项为定性、与所主张路线自洽但不可独立核验；温度/pH/盐度/基因组等关键定量性状全缺。落5档：部分性状可用且适用，关键项证据不足。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_100：显示Bordetella sp. 10d在本切片中多数性状为UNKNOWN；不证明答案性状错误，只说明未获冻结观测支持。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分3 → V0.5新分5，变化+2。

新裁判理由：

> 答案有evidence_registry，并为多步给出EVID_001文献、EVID_003/EVID_004/EVID_005数据库EC定位；这些条目至少部分可定位。但核心路线/菌株关联与S1脱羧主要依赖EVID_002 INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE；文献与EC条目在E0 EVIDENCE_GAP下均无法统一核验，登记UNRESOLVED_SOURCE。无已核实错引，不触发D5 cap。存在部分条目级线索但核心组来源缺失，取5。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组（CORE：CG01/CG02/CG03/CG05/CG07/CG09；APPLICATION_CRITICAL：CG08/CG17）的状态集合全部为MISSING_SOURCE（EVID_002=INTERNAL_KNOWLEDGE_ONLY）或UNRESOLVED_SOURCE（EVID_001未解析自由文本GAP-100-028；EVID_003/004/005的BRENDA记录在E0无冻结EC记录）。决策相关组不存在条目级可定位且可核对的结论（唯一可核对项S5 EC 4.1.1.77与gold同一步一致，量级上不足以把整维提升到5–6档），故按P41低分档；同时并非&#x27;几乎无法定位&#x27;（有证据登记表、数据库名、文献题录与步骤绑定），取3。无任何已核实错引（E0整题EVIDENCE_GAP），severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不触发cap（UPD-07/P51）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_100：支持Bordetella sp. 10d身份名称；不支持答案内部知识来源已可核验。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案较清楚地标注未知与限制：氧条件按题面保留null，S1缺EC/基因，Bordetella sp. 10d缺TaxID/基因组，S5-S7下游为推定，2-氨基粘康酸半醛可生成吡啶甲酸的非主链分支也明确标为非评分主链。未发现系统性把预测写成实证或掩盖矛盾；个别关键能力仍以内部知识中等置信表述，属局部扣分而非cap。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界总体如实：uncertainties列5条具体限制（氧条件题面null故保留null但路线为好氧型；S1脱羧酶缺EC/基因；Bordetella sp. 10d缺可核验保藏号/TaxID/基因组且多数性状未知；S5–S7下游为推定、可能共享经典meta途径酶系；2-氨基粘康酸半醛自发环化生成picolinic acid的非生产性分支）；EVID_002明确自标INTERNAL_KNOWLEDGE_ONLY，未知字段统一null+confidence unknown，分步置信多为low/medium，属披露具体诚实。不足：核心路线与F7/F8/F9能力声称以medium confidence呈现，未明确声明整条路线缺乏本菌实验/文献验证、也未指出与gold/数据库参考路线不同；但EVID_002的来源类型已显式披露、未把预测写成OBSERVED、无掩盖矛盾证据，属单点/局部过度确信而非系统性误导（P119/SC6）。落6档。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_100：支持本题存在表示/路线边界核验背景；不改变D6按答案披露质量独立评价。

</details>

## Qwen

答案SHA256：`faa7c6b52eacbf8ce00028f6d45617a32d0772bbb9bf322df298ba3f87417ae8`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 答案结构完整，但交付的是原儿茶酸邻位开环路线，未按冻结gold主链S06→S04→S05→S03→S01→S02交付，缺少入口双加氧、脱氨、脱羧、脱氢及终点产物；D1任务符合度受限在&#91;1,4&#93;，给3。

<details><summary>V0.4理由与本行变化背景</summary>

五步主链齐全：每步均给主底物与主产物的英文名、一个酶加EC、一个微生物，predecessor_step_ids连接成单链；route_scope.chosen_route_name 逐字填写题面路线名，is_single_continuous_route=true；organism_profiles按物种去重为1条并被各步引用；15项性状字段全部出现（12项有值，F4/F5/F14三项明确null）。扣分：题面明确要求每一步给出SMILES，但S3产物、S4底物与产物、S5底物共4处关键中间体为null，S2产物自述为“简化表示”，属必要结构字段缺失；任务要求“各项最强来源”，实际只有内部知识标签（来源质量归D5，不在此双计）。归入5–6档（主要模块均有涉及、若干必要内容遗漏），取6分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：列出gold S01-S06主链与终点产物；不支持答案的原儿茶酸路线。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_100：显示本案为LINEAR_UNIQUE且ordered_step_count=6；不是允许改选路线的依据。
- ANSWER_TEXT / ANSWER.steps：答案给出5步原儿茶酸邻位开环路线，而非gold主链。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 在D2独立化学轴上，答案的原儿茶酸邻位开环链内部基本连贯：脱氨、双加氧开环、环异构、脱羧、内酯水解，主碳流和辅因子大体可辨；但它是替代路线，终点不同，若干中间体SMILES缺失且立体化学未完全指定。D2上限&#91;1,6&#93;，给6。

<details><summary>V0.4理由与本行变化背景</summary>

按四.5四步判断：①题面指定了路线范围（路线名）；②答案未声明这是替代路线，反而在route_scope.notes声称“严格按指定路线名称填写，不改选其他路线”，属未声明偏离；③入口步无可核证据，EVID_001仅为INTERNAL_KNOWLEDGE_ONLY，无论文/数据库条目/计算记录；④偏离是否使主要结论失效——入口步化学与冻结gold首步（4-Amino-3-hydroxybenzoate + dioxygen → (2Z,4E)-5-amino-2-formylhexa-2,4-dienedioate，酶为1.13.11 2,3-双加氧酶）在反应类型和中间体上完全不同，但“芳香胺水解脱氨生成原儿茶酸”是否化学上不可能，无法以冻结证据核实，故不登记为已核实关键错误、不cap。S2–S5为经典原儿茶酸邻位开环（β-酮己二酸）主链：方向正确、连接连续，3-羧基粘康酸→4-羧基粘康内酯→3-氧代己二酸烯醇内酯→3-氧代己二酸，计量基本成立，但内酯类结构未给SMILES。题面未指定终点，gold终点(2Z)-2-hydroxypenta-2,4-dienoate之外的下游不进入覆盖率扣分。综合为“主干部分成立、关键入口转化需修订、合理性证据有限”，取5分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：用于对照gold反应方向与终点；答案化学按D2自身质量独立评价。
- ANSWER_TEXT / ANSWER.steps：支撑对5步化学转换、辅因子与缺失结构的评价。
- RUBRIC_CLAUSE / C00：任务路线偏离归D1；D2仍独立评价所答化学质量，替代内容不回填目标完成。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 6个必答目标中0个获得目标支持：S02为已确认KEY终点失败，S01、S03-S06为对齐未确认U；答案替代路线内部酶自洽不获得目标信用。按C04/D-KEY4落&#91;1,4&#93;，无非S目标信用支撑，给下沿1。

<details><summary>V0.4理由与本行变化背景</summary>

五步均给出酶名+EC：S1 4-amino-3-hydroxybenzoate deaminase/3.5.99.2；S2 protocatechuate 3,4-dioxygenase/1.13.11.3；S3 3-carboxymuconate cycloisomerase/5.5.1.2；S4 4-carboxymuconolactone decarboxylase/5.3.3.12；S5 3-oxoadipate enol-lactonase/3.1.1.24。S2/S5的酶名—反应类型与常见β-酮己二酸途径一致，属合理候选；但全部酶仅有INTERNAL_KNOWLEDGE_ONLY标签，E0无任何EC条目（item gaps GAP-100-001/005/006/012/013/014），无法核accepted name/reaction/状态。S4把脱羧酶标为EC 5.3.3.12（EC 5.3.3属分子内氧化还原酶类），EC大类与脱羧反应类型可能不符；S1“脱氨酶”实体亦无可核记录：关键入口步骤酶对应缺具体核验，够5–6档下限。按OBS-D3A-D5，引用/编号可定位问题归D5，不作为本维关键错误依据；故不cap、key_error=UNRESOLVED。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_100：给出gold各步accepted酶/EC；不支持答案替代路线酶作为目标步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：给出gold目标反应与终点；S02为KEY终点步骤。
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.enzyme：答案酶/EC对应原儿茶酸路线，不作为目标步S01-S06的支持。
- RUBRIC_CLAUSE / C04：D3a候选分带、KEY4上界与U/H处理。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 全部步骤使用Pseudomonas aeruginosa TaxID 287，身份本身是合理候选，且Pseudomonas中β-酮己二酸相关酶有一定合理性；但未给菌株，complete_pathway_organism_profile_id声称全路径能力缺乏冻结证据，gold完整路径行为Bordetella sp. 10d。属于部分支持、关键作用范围未核，给5。

<details><summary>V0.4理由与本行变化背景</summary>

全部5步与complete_pathway_organism_profile_id均归属单一物种Pseudomonas aeruginosa（strain=null，ncbi_taxid=287），身份粒度与声称粒度同为物种级，内部一致；P. aeruginosa为常见芳香族降解菌，属合理候选。但：①TaxID 287在E0无冻结记录（GAP-100-030），身份三件套只有物种名+TaxID、无菌株/保藏号/基因组号；②该菌集与gold登记的Bordetella sp. 10d/Pseudomonas putida/Comamonas testosteroni/Paenibacillus sp. JJ-1b/Pseudomonas fluorescens不同；③整条路径能力声称(complete_pathway=ORG_001)无全路径证据，仅有内部知识，未按“身份定位≠反应级能力≠完整路径能力”三层分别举证。按D3b身份阶梯：无证据表明编号指向无关类群或另一菌株，不判②/③档身份错配、不cap；属“有合理候选和部分支持，但关键身份与作用范围未充分核验”，取5分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_100：gold列出各步菌株与PATHWAY_COMPLETE=Bordetella sp. 10d；不证明P. aeruginosa完成本题全路径。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;; complete_pathway_organism_profile_id：答案声称P. aeruginosa覆盖全部步骤并具完整路径能力；无外部定位证据。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项性状齐全，形态、革兰氏、产孢、运动性及部分生理描述对P. aeruginosa属合理概括，未知项用null。但冻结切片无P. aeruginosa性状记录；F8/F9把目标降解能力和五类酶活写成物种能力，证据不足；部分最适值缺条件/单位。给5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状字段全部出现，12项有值、3项（F4盐度、F5保藏号、F14基因组）明确null——按P15/P45，明确未知体现信息不足，完成度扣分主归D1，D4不重复重扣。已给值中温度最适37℃、pH最适7.0、革兰氏阴性、杆状、不产孢、有运动性、好氧化能异养、以氧为末端电子受体等对P. aeruginosa属常见描述，方向不离谱；但唯一来源为EVID_007（INTERNAL_KNOWLEDGE_ONLY，species级概括），E0无TaxID 287任何性状记录（GAP-100-040至048），数值/单位/实验条件无法核验，raw_text全为null；F8把“可降解4-氨基-3-羟基苯甲酸、原儿茶酸”与F9把本答案五种酶活写成物种性状，属由路线归属反推的物种级能力声称，超出可支持范围（P115同类外推）。综合“部分性状准确且适用，但关键项证据不足、条件解释需修订”，取5分；未发现数值离谱到误导筛选或把物种级观测自动推广到所有菌株（答案未给菌株），故不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_100：gold性状行主要覆盖其他菌；未见P. aeruginosa TaxID 287性状记录。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_100：显示本题可评分性状分母对应的gold菌株；不提供P. aeruginosa验证。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：支撑对15项填写、未知null与过强性状声称的评价。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> evidence_registry七条全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；关键路线、酶、菌、性状均无法沿可定位文献/数据库核验。属于MISSING_SOURCE，未见已核实错引，不cap；给2。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付了evidence_registry EVID_001–EVID_007，且每一步与性状均有evidence_id指向具体条目并写明claim_scope，映射结构清楚；但7条证据的source_type全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null。按四.3，这属MISSING_SOURCE（完全无引用或仅内部知识自我声明）；决策相关组CG01/CG02/CG03/CG05/CG07及APPLICATION_CRITICAL组CG08/CG14均无一条条目级“可定位可核对”证据，故落低分档；属缺失而非已核实错引，按P34/P41默认不cap。答案未编造数据库/登录号，且逐条诚实标注内部知识，档内不取1–2而取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示所有证据条目均为内部知识、无外部定位。
- RUBRIC_CLAUSE / P34：MISSING_SOURCE包括仅有INTERNAL_KNOWLEDGE_ONLY；默认不触发关键错误cap。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案明确把证据标为内部知识、confidence多为medium，列出氧未指定、SMILES不完整、种级概括等限制，未知性状用null。但对完整路径能力、F8/F9等强声称仍以medium呈现，未充分标明为推断；披露具体但强度略超内部依据。给6。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties列出5条具体限制：氧条件未指定、S2需分子氧、粘康酸/内酯类SMILES不确定、下游辅酶A步骤未列入主链、酶菌关联无外部文献或数据库、性状为物种级概括——披露具体、与部分结论相符，且每条事实都带source_type标签（INTERNAL_KNOWLEDGE_ONLY）。减分点：所有未核实的性状与步骤仍统一以confidence=medium、raw_text=null呈现，属结论强度超过依据；route_scope.notes声称“不改选其他路线”与其交付的入口化学（水解脱氨，而非gold首步双加氧）不同，属对自身合规性的过度确信；但错误集中于单一断言结构、未见系统性把预测写成实证、未见掩盖已知矛盾。按P119/P121：单点/多点过度确信档内扣分，不cap。取6分。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; ANSWER.evidence_registry&#91;*&#93;.source_type：支撑对不确定性披露、内部知识标签与置信强度匹配度的评价。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；披露质量按覆盖范围与证据强度评价。

</details>

## Grok

答案SHA256：`09d5b121a8fc1a272aedf263275e749b61db18f2e444acda2ce8764ad0f386e0`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> JSON可读，route_scope.chosen_route_name正确，15项性状均出现且多数明确null；但任务要求6步主链至终点，答案只交付S1/S2两步并明确不展开下游，缺失4个必答步及终点。属于仅覆盖少数必要模块，3–4档；核心任务模块大部缺失触发D1关键错误，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_100：显示本题gold有6个有序必答步；不证明答案化学正确性。
- ANSWER_TEXT / ANSWER：证明答案只交付两步，其余四步未交付。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 交付的S1/S2方向为底物到产物，名称/酶层面可与gold入口S06和脱氨S04对应，未发现方向反转或已核原子不守恒；但只覆盖前两步，S05/S03/S01/S02及终点未给出，主链连续性和终点未建立。5–6档：主干部分成立但关键转化缺失，需实质修订，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：给出gold反应参与者与顺序；S04/S06表示等价/电荷仅自动绑定未确认，不证明答案SMILES完全等价。
- ANSWER_TEXT / ANSWER：证明答案只展开前两步并明确不展开下游。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 6个必答目标中，S1/S2按酶名可与S06/S04对应，但表示/互变异构自动绑定未确认；S01/S02/S03/S05未交付，且S02为KEY_TERMINAL。已确认KEY终点漏交付触发D-KEY4上界≤4；可用部分仅两步且关键终点缺失，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_100：给出6个目标步的accepted酶名/EC；不证明答案已交付全部步骤或精确结构。
- QUESTION_TEXT / QUESTION：题面锁定4-amino-3-hydroxybenzoate degradation路线并要求主链。
- ANSWER_TEXT / ANSWER：证明答案仅交付两步，未交付其余目标步。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已交付步骤的核心微生物Bordetella sp. 10d与gold S04/S06 organism精确一致，且gold PATHWAY_COMPLETE行支持该菌整路能力；但答案仅给两步的菌归属，未给TaxID/保藏号，另四步无对应微生物。5–6档，因已交付身份精确且无序列外推，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_100：支持Bordetella sp. 10d对应S04/S06且PATHWAY_COMPLETE=TRUE；不覆盖缺失步骤、TaxID或保藏号。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状均出现，10项明确null，5项填写。填写的F1/F6/F7/F8/F9对Bordetella sp. 10d具有菌株特异性且与路线叙述一致，但冻结trait_gold对F1/F7/F8/F9为UNKNOWN，不能核实；无已核数值/单位错误或物种级外推。5–6档，因未知披露清楚且无已核冲突，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_100：这些字段在冻结trait记录中为UNKNOWN，不支持也不证伪答案值；F14 TaxID 170622为观测项。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_100：Bordetella多数性状为completeness_only/FALSE，无observed accuracy分母；不证明答案错误。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案仅有EVID_001/EVID_002，两条均为INTERNAL_KNOWLEDGE_ONLY，无数据库条目、DOI、稳定链接或可核对记录；决策相关组大多为MISSING_SOURCE。无已核实错引，默认不cap。重要结论几乎无法独立定位，1–2档，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示两条来源均为INTERNAL_KNOWLEDGE_ONLY，无外部可定位记录；不证明其内容为假。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案清楚标注EC/gene/TaxID等未知，使用low/medium/unknown置信度，uncertainties明确说明文献记忆、未回查、下游未展开及SMILES未逐库比对；没有系统性把预测写成观测。个别内部记忆仍标medium，阻止9–10；7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：支持答案对未知、证据性质和限制有明确披露；不证明科学内容正确。

</details>

## GPT5.6

答案SHA256：`2b4993bcf3d61d3678151e0e95385c4773693ab11f7525d5f480c8cf2857ad52`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 1–2档：题面要求六步主链、每步酶/EC/微生物及15项性状；答案仅1步，无微生物、无organism_profiles与15项性状，核心任务模块大部缺失。存在起点和一步酶名，取2而非1。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION.task_requirements：题面要求六步主链、每步主底物/主产物/酶/EC/微生物及15项性状。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案仅交付1步；microorganism=null；organism_profiles为空；无15项性状。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_100：gold全图ordered_step_count=6，任务范围登记n_required=6；不证明所有旁支必答，但本题主链范围已登记。

</details>

### D2 反应化学科学性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 1–2档：唯一入口转化采用3,4-双加氧开环，产物名2-Amino-5-carboxymuconate-6-semialdehyde与gold S06 2,3-双加氧产物(2Z,4E)-5-amino-2-formylhexa-2,4-dienedioate不一致，且产物SMILES=null、无后续连接；入口核心转化不能构成可信主链，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案给出4-Amino-3-hydroxybenzoate + O2 -&gt; 2-Amino-5-carboxymuconate-6-semialdehyde，酶为3,4-dioxygenase，产物SMILES=null。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：gold S06为4-amino-3-hydroxybenzoate 2,3-dioxygenase生成(2Z,4E)-5-amino-2-formylhexa-2,4-dienedioate；不支持答案的3,4-开环产物。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_100：gold S06酶名为4-amino-3-hydroxy-benzoate 2,3-dioxygenase subunit，EC 1.13.11；不证明3,4-dioxygenase存在或不存在。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 本题target_fact_contract登记原N=6，六个必答目标反应均未获得目标级支持；答案只给一个非目标的3,4-开环酶步骤，EC为空、confidence=low、来源为INTERNAL_KNOWLEDGE_ONLY，不能计为任一gold目标反应支持。按C03目标反应口径，不能把未绑定/内部知识候选回填为目标完成；按C04，S=0、C=S/N=0/6&lt;0.20，落入&#91;1,2&#93;候选带；按C05，几乎无可用目标催化对应，核心目标酶推荐不可用，故取1分。未核EC/具体功能不作为正分依据，也不因此把整维转NE。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps&#91;0&#93;.enzyme：答案仅交付一个3,4-双加氧开环酶名，EC为空、confidence=low，来源登记为INTERNAL_KNOWLEDGE_ONLY；未交付其他必答步骤
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_100：该gold case为LINEAR_UNIQUE，ordered_step_count=6，用于确认本题任务合同的目标步数量为6，而不是答案的1步
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_100：gold入口步S06接受酶为4-amino-3-hydroxy-benzoate 2,3-dioxygenase subunit，EC 1.13.11；accepted集合不支持答案的3,4-dioxygenase作为该目标入口反应对应酶
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_100：gold S06为4-Amino-3-hydroxybenzoate + dioxygen生成(2Z,4E)-5-amino-2-formylhexa-2,4-dienedioate；gold主链终点为S02生成(2Z)-2-hydroxypenta-2,4-dienoate；答案所给3,4-开环产物不是该目标主链的S06产物

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b按P44：答案step.microorganism=null且organism_profiles为空，未交付任何微生物身份、单步催化归属或全路径能力声称；对应模块缺失，记MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.microorganism：证明该步microorganism为null，未给菌名/菌株/TaxID/能力。
- ANSWER_TEXT / ANSWER.organism_profiles：证明organism_profiles为空数组。
- QUESTION_TEXT / QUESTION.task_requirements：题面要求每步绑定一个对应微生物并按物种+菌株去重填写profile。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4按P44：organism_profiles为空，15项性状均未交付；无已给性状内容可评，记MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：证明没有organism_profiles，因而没有15项性状。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.trait_evidence_id：证明该步trait_evidence_id为null。
- QUESTION_TEXT / QUESTION.task_requirements：题面要求每个profile一次返回全部15项性状。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 1–2档：唯一来源EVID_001为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null；核心组CG01/CG03/CG05/CG07均无来源或仅内部知识，重要结论无法定位。无已核实错引，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：证明唯一证据为内部知识、无database/record_id/locator。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.reaction_evidence_id：证明该步仅引用EVID_001。
- RUBRIC_CLAUSE / C05：MISSING_SOURCE低档且默认不cap。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 7–8档：答案明确EVID_001为INTERNAL_KNOWLEDGE_ONLY、confidence=low，并在uncertainties列出EC、微生物、产物SMILES、后续步骤均未确认；仅“可确认的主反应”措辞略强，但未系统把预测写成实证，主要限制已说明。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：列出EC、微生物、产物SMILES、后续步骤未确认。
- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：标明INTERNAL_KNOWLEDGE_ONLY与low confidence。
- RUBRIC_CLAUSE / C06：D6按证据性质与不确定性披露独立评分。

</details>
