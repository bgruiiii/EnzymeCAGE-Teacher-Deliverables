# BIOPATH150_141：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：S-(6-hydroxy-4-methylhexan-4-yl)-L-cysteinylglycine degradation

污染物：S-&#91;1-(2-hydroxyethyl)-1-methylbutyl&#93;-(l)-cysteinylglycine；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 58 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 24 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 54 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 43 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 40 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 34.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`922ce973259b3678dadb8a2c7c1c412e904fcce49e14a5bd0a2911ba8a2483cf`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> Route name is copied exactly. The answer gives two chemical steps with substrates/products/SMILES, enzyme/EC and microorganism, plus two organism profiles with all 15 trait fields. It omits the required S03 dipeptide/tripeptide permease/import step, so completeness is partial rather than full; D1 remains in the 5-6 band, upper end 6 because the core chemical steps and profiles are present.

<details><summary>V0.4理由与本行变化背景</summary>

两个化学步骤均给出主底物/主产物英文名与SMILES、首选酶+EC、对应微生物，route_scope.chosen_route_name原样回显题面路线名、氧条件按题面null填写；两个organism_profile各15项性状齐全（各3项明确null、0遗漏、0空占位），来源与不确定性模块均有实质内容。相对gold三步主链（S03 dipeptide/tripeptide permease摄取步 + S02二肽水解 + S01 β-裂解）少一个转运步，属少量遗漏而非模块缺失，落7–8档，取8分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / question:BIOPATH150_141：Task requires specified route, each step substrate/product/enzyme/EC/microorganism, and 15 traits per organism profile.
- ANSWER_TEXT / answer:BIOPATH150_141：Answer supplies route name, two steps, two organism profiles, and 15 trait fields; does not supply an import/permease step.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：Gold has three required steps including the S03 dipeptide/tripeptide permease; does not imply alternative organisms are automatically wrong.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The two delivered chemical transformations correspond to gold S02 and S01: cysteinylglycine hydrolysis to cysteine conjugate plus glycine, then PLP-dependent beta-elimination to the thiol plus pyruvate and ammonia. Structures, direction and endpoint match; neutral/charged notation difference is representational. The omitted S03 import step is primarily completeness/task coverage, not a chemical-transformation error. Main chain chemistry is strong, with only limited local issues, so 8.

<details><summary>V0.4理由与本行变化背景</summary>

S1为Cys-Gly二肽键水解（S-取代半胱氨酰甘氨酸+H2O→S-取代半胱氨酸+甘氨酸），与gold S02反应类型及产物一致；S2为PLP依赖Cα–S键β-裂解（S-取代半胱氨酸→叔碳硫醇+丙酮酸+氨），与gold S01一致，主产物6-hydroxy-4-methylhexan-4-thiol的SMILES SC(C)(CCC)CCO与gold末端3-Methyl-3-sulfanylhexan-1-ol（CCCC(C)(CCO)S）同构，终点与题面/gold terminal（Pyruvate|3-Methyl-3-sulfanylhexan-1-ol）吻合；两步原子数闭合（C10/S1/N1/O4）。S2未显式列出水为辅底物，属局部计量/辅因子表达缺陷（按P103在7–8档处理，不cap）；对具体R基结合物的直接实验依据缺（局部待核），不改变主链化学结论。取8分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：Gold gives directed S02 hydrolysis and S01 beta-elimination steps; supports reaction chemistry, not specific organism or source delivery.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_141：Gold root and terminal identities align with the answer&#x27;s substrate and thiol/pyruvate endpoint.
- ANSWER_TEXT / answer:BIOPATH150_141：Answer&#x27;s two step structures and SMILES match the gold chemical transformations; does not contain an import step.

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> D3a按目标反应逐行核对：①终端β-裂解步（gold S01）由答案S2给出cysteine conjugate beta-lyase EC 4.4.1.13，与accepted集合的4.4.1.13一致，产物为硫醇+丙酮酸+氨，与gold终产物对应；表示层charge-only hold不抹去该酶-EC匹配。②肽键水解步（gold S02）答案S1给cysteinylglycine dipeptidase EC 3.4.13.6，而accepted为EC 3.4.13.23；反应类型相符但显式EC非accepted且未核，按U处理，不能记S，也不能未核判F。③gold S03 dipeptide/tripeptide permease为必答进入/转运步，答案完全未交付，记M。整体为1个已支持目标、1个未核目标、1个缺失目标，C≈1/3，落入&#91;3,4&#93;带；已支持终端步与缺失/未核边界清楚，但存在必答转运酶缺失和EC非accepted，取4不取更高；无经核独立关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

S2酶“cysteine conjugate beta-lyase EC 4.4.1.13”与gold S01酶EC 4.4.1.13完全一致，酶名与EC类别（裂解酶4.4.1）相符；S1给“cysteinylglycine dipeptidase EC 3.4.13.6/Dug1p”，EC大类3.4.13（二肽酶）与水解反应匹配，但gold S02为EC 3.4.13.23（cysteinylglycine-(S) conjugate dipeptidase），具体号不一致，且E0无EC:3.4.13.6冻结记录（GAP-141-004），按四.5保守条款无法核验→UNRESOLVED，不判错、不cap。两步中一步可靠对应、一步关键EC待核，落5–6档，取6分。错引归D5，不作为本维KE依据（OBS-D3A-D5）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：Gold必答酶：S01 cysteine-thiol lyase EC 4.4.1.13；S02 cysteinylglycine-(S) conjugate dipeptidase EC 3.4.13.23；S03 dipeptide/tripeptide permease，EC为NOT_OBSERVED。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：Gold反应顺序与参与者：S03入口转运；S02肽键水解生成S-(6-hydroxy-4-methylhexan-4-yl)-L-cysteine与glycine；S01 β-裂解生成3-Methyl-3-sulfanylhexan-1-ol、pyruvate与ammonium。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_141：本题为LINEAR_UNIQUE，ordered_step_count=3，required step数=3，支持按三个必答目标核D3a而非只核答案两步。
- ANSWER_TEXT / ANSWER_TEXT：答案S1酶EC 3.4.13.6、S2酶EC 4.4.1.13；答案没有给出dipeptide/tripeptide permease步骤。
- RUBRIC_CLAUSE / C03：D3a目标行S/F/M/U/H分类及未核EC不自动判错。
- RUBRIC_CLAUSE / C04：D3a分带与M/U混合事实的评分出口。
- RUBRIC_CLAUSE / C05：D3a档内3/4分锚点与上沿选择条件。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer gives step-level microorganisms only, with complete_pathway_organism_profile_id null, so it avoids claiming a whole-path organism. However it assigns S. cerevisiae to the dipeptidase step and E. coli to the beta-lyase step, whereas gold lists S. hominis and Corynebacterium sp. Ax20. TaxIDs 4932/562 and exact step capabilities are not present in E0, so identity and reaction-level capability remain unverified. Plausible candidates with partial support but key capability unresolved fit 5-6; choose 5.

<details><summary>V0.4理由与本行变化背景</summary>

两步分别归Saccharomyces cerevisiae（TaxID 4932，无strain）与Escherichia coli（TaxID 562，无strain）：物种名真实、层级为物种级，但未给菌株，属身份粒度不足；其单步催化能力（酵母Dug1p作用于S-取代半胱氨酰甘氨酸、大肠杆菌β-裂解酶活性）仅为同源推断，答案自标low/medium并披露未核。E0无4932/562冻结记录（GAP-141-017/019），现有两条E0条目为Pseudomonas putida（12880/303），与本答案菌无关、不得外推；答案未把单步菌写成全路径菌（complete_pathway_organism_profile_id=null），属正面。主要身份与能力未充分核验，落5–6档，取5分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_141：Gold step organisms are S. hominis for S01 and S03 and Corynebacterium sp. Ax20 for S02; does not by itself disprove alternative capable organisms.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：Gold lists step enzymes; does not provide capability evidence for S. cerevisiae or E. coli.
- ANSWER_TEXT / answer:BIOPATH150_141：Answer supplies step-level organisms and TaxIDs but only INTERNAL_KNOWLEDGE_ONLY evidence; no whole-path claim.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> All 15 trait fields are present for both profiles, with explicit null/unknown for missing salinity, culture collection and genome data. The values are broadly plausible species-level statements and are labeled low/medium confidence. However the answer organisms are not the gold trait organisms and no E0 trait rows verify their F2/F3/F6/F7/F8/F9/F14 values; key numeric/conditions remain unsupported. That fits partial accuracy with key evidence gaps, 5-6; choose 6 for full field coverage and explicit unknowns.

<details><summary>V0.4理由与本行变化背景</summary>

两profile均一次返回15项，F4盐度/F5保藏/F14基因组诚实填null（明确未知，非错误），其余为S. cerevisiae与E. coli的物种级通识：最适30°C/37°C、pH5/7、兼性厌氧、革兰氏阴性（E. coli）、周生鞭毛、不产芽孢、子囊孢子等方向正确且与所指对象适用；但全部来源为INTERNAL_KNOWLEDGE_ONLY（EVID_003/EVID_004，database/record_id=null），无株级粒度、无法独立核验，属“关键项证据不足”；F9把Dug1p归入M17金属肽酶家族存疑（未核）。E0无4932/562性状记录（GAP-141-021..030/044..053），按未核≠错误处理。落5–6档，取6分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_141：Gold trait rows cover S. hominis and Corynebacterium sp. Ax20, not the answer&#x27;s S. cerevisiae/E. coli; they cannot verify the answer&#x27;s trait values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_141：Scoreability mask is for gold organisms; no answer-specific scoreable trait rows for S. cerevisiae/E. coli.
- ANSWER_TEXT / answer:BIOPATH150_141：Answer supplies all 15 trait fields for each profile, with some explicit nulls and INTERNAL_KNOWLEDGE_ONLY evidence.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> All four evidence_registry entries are source_type INTERNAL_KNOWLEDGE_ONLY with database, record_id and locator null. No decision-relevant group has an external locatable source. This is MISSING_SOURCE rather than verified mis-citation; the explicit internal mapping and confidence labels make 2 more appropriate than 1, but traceability remains very low.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry四条（EVID_001–EVID_004）全部source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，按四.3归MISSING_SOURCE；决策相关组（CORE：CG01/02/03/05/07；APPLICATION_CRITICAL：CG08/17）全部缺失，按P41“全部缺失→低分档（默认不cap）”落1–2档。答案虽以claim_scope数组结构化自述并诚实披露未核，但无可定位条目，取档内上限2分。无已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer:evidence_registry：Shows all delivered evidence entries are internal knowledge only, with no external database/literature locator.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> The answer clearly labels internal knowledge, uses low/medium confidence, fills unknown fields with null, and lists concrete uncertainties including unverified EC/gene assignments and uncertain downstream steps. It does not systematically present predictions as observed facts. Some broad statements are moderately confident, but the limits and unknowns are disclosed, supporting the 7-8 band upper end.

<details><summary>V0.4理由与本行变化背景</summary>

每一步设uncertainty字段、uncertainties四条系统披露“未确认该具体结合物的实验菌株/EC与基因基于同源推断/叔碳硫醇下游不确定/性状为物种级通识未逐项核对”，并明确把下游氧化脱硫列为downstream、把N-乙酰化支路标is_part_of_scored_main_route=false，未把预测写成观测；未知项诚实null。轻度过确信在于以medium置信承载内部知识推断（如S1酶-菌对应），但已同时披露，不属“零披露包装”或系统性误导，不cap。落7–8档，取7分。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer:uncertainties：Answer discloses unverified EC/gene/organism assignments and uncertain downstream route.
- ANSWER_TEXT / answer:evidence_registry：Answer labels all evidence as internal knowledge rather than presenting it as experimental observation.

</details>

## DeepSeek

答案SHA256：`2ad7c0b6745a491c5a667624488720728c28527a3cdd1081f578a5072fdf94c4`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 题面要求3步主链、每步酶/EC/对应微生物、每菌15项性状及来源。答案只给2步，microorganism全null，organism_profiles=&#91;&#93;，evidence_registry=&#91;&#93;，且缺少gold S03 entry/transport。pathway/enzyme仅部分覆盖，核心微生物与性状模块完全缺失；按D1 3–4档取3（仅覆盖少数必要模块，多处缺步骤、酶菌关联或性状），不因JSON可读而提高。

<details><summary>V0.4理由与本行变化背景</summary>

交付2步化学主链（底物/产物名称与SMILES齐全）与2个酶（含EC），route_scope.chosen_route_name与题面给定路线名一致；但 steps&#91;0..1&#93;.microorganism 全为 null、organism_profiles 为空数组、evidence_registry 为空数组，即每步微生物、15项性状、来源/生成记录三个模块完全未交付，且未列gold的摄入转运步。属&#x27;仅覆盖少数必要模块&#x27;的3–4档；因路径与酶两模块实质完成、路线合规，档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求主链每步给主底物/主产物、酶与EC、对应微生物，并给每菌15项性状及来源；不证明答案已交付这些内容
- ANSWER_TEXT / ANSWER_BEGIN：答案仅交付2步，微生物字段全部null，organism_profiles与evidence_registry为空；支持D1完整性低分
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_141：题目主链为3个必答步；不把其他分支或全图材料当作额外分母

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> 答案S1二肽水解的底物/产物结构与方向对应gold S02，属主干部分成立。但S2 C-S lyase虽方向正确、副产物含pyruvate/ammonia，主产物却为6-hydroxy-4-methylhexane-4-thiol（SMILES SCC(C)(CCC)CCO），与gold S01主产物3-Methyl-3-sulfanylhexan-1-ol不同；该SMILES相对底物多出一个CH2，碳骨架/原子不守恒且未说明，未到达gold终点。核心末端转化错误，按3–4档取3；D2关键错误（原子明显不守恒/核心转化错误）成立，capped≤4。

<details><summary>V0.4理由与本行变化背景</summary>

两步化学转化与gold一致：S1为Cys-Gly二肽水解（产物 S-(6-hydroxy-4-methylhexan-4-yl)-L-cysteine + glycine，与reaction_gold BSY-r03203一致）；S2为Cys-S-共轭β-裂解（产物硫醇+pyruvate+氨，与BSY-r01905一致），方向forward、连接正确、碳计量自洽（S2底物10C=硫醇7C+pyruvate 3C）。首步未把H2O列为参与者、S2产物角色标注略粗（pyruvate/氨标为byproduct），属辅因子/参与者局部计量缺陷，按辅因子条款在7–8档内处理，不cap；未见起始步错误、方向反转或明显不守恒，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：gold S01给出该C-S lyase步的主产物/副产物；不支持答案S2的foreign主产物
- ANSWER_TEXT / ANSWER_BEGIN：答案S2主产物名称/SMILES；与gold S01主产物结构不一致，且SMILES相对底物多一个碳

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> C03/C04：N=3，S=0、F=1、U=2、M=0、H=0。gold S01为预定义KEY终端目标，答案S2给出foreign主产物，程序路线诊断NONMATCH并绑定proof_id REAL-ROUTE-B480-0454-BIOPATH150_141__S01__BSY-r01905，故S01为已确认KEY失败(F)，触发D-KEY4上界≤4。S02为PAIR_UNVERIFIED（EC 3.4.13.19对accepted 3.4.13.23），S03为ALIGNMENT_NOT_CONFIRMED，均保留为U，不当作已支持或已证伪；无已核S，核心主推荐严重受损，取低档2（&#91;1,2&#93;）而非上沿4。局部U写入ne字段。

<details><summary>V0.4理由与本行变化背景</summary>

两步酶均为合理候选：S2 EC 4.4.1.13（cysteine-S-conjugate β-lyase）与gold enzyme_gold 的 EC-4.4.1.13 一致；S1 为3.4.13族二肽酶，具体号3.4.13.19与gold 3.4.13.23不同，E0无该EC冻结记录（GAP-141-002/007）无法核验accepted name/reaction；两步均无基因/蛋白、confidence=unknown、无来源记录。属&#x27;有合理候选和部分支持，若干关键步骤仍缺具体核验&#x27;→5–6档，取6；EC号差异按四.5/四.6登记为UNRESOLVED待核，不判错、不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：gold三步结构与主产物；支持S01为终端C-S lyase、S02为二肽酶、S03为transport；不自动证明答案全部酶/EC
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：accepted酶/EC集合；S02答案EC 3.4.13.19不在accepted精确集合，故S02为PAIR_UNVERIFIED而非S
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_141：本题主链3个必答目标；不把全图其他材料当作额外目标
- ANSWER_TEXT / ANSWER_BEGIN：答案实际交付的两步酶/EC与主产物；支持S01失败、S02 U的判定

</details>

### D3b 微生物身份与能力：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 题面要求每步给一个对应微生物；答案所有step.microorganism=null，organism_profiles=&#91;&#93;，没有交付任何微生物身份/菌株/单步能力/全路径能力声称。按P44及MISSING规则：微生物模块确未交付，D3b记MISSING=1，不宣称检测到科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

每步 microorganism 字段均为 null，organism_profiles 为空数组：物种/菌株身份与步级归属完全未交付，无可评价的微生物对应内容，按MISSING记1；不宣称检测到科学错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求每步微生物；不证明答案已交付
- ANSWER_TEXT / ANSWER_BEGIN：答案微生物字段全部null且profiles为空；支持D3b MISSING
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_141：gold给出各步参考微生物；仅用于说明可核验对象存在，不把答案缺失回填为已交付

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 题面要求每个organism_profile一次返回全部15项性状（F1–F15）；答案organism_profiles=&#91;&#93;，没有任何traits字段，15项均未交付。按P44：全部必需性状为空/未交付时D4记MISSING=1，不宣称检测到科学错误；完成度缺口主归D1。

<details><summary>V0.4理由与本行变化背景</summary>

无任何 organism_profiles，15项性状（F1–F15）在答案中完全未出现（filled=0、explicit_unknown=0、omitted=15），属字段集合未交付而非&#x27;诚实null&#x27;，按MISSING记1；完成度扣分已在D1体现，此处不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求每profile返回全部15项性状；不证明答案已交付
- ANSWER_TEXT / ANSWER_BEGIN：答案未交付任何profile与traits；支持D4 MISSING=1
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_141：gold有可核性状参照；不把参照回填为答案已交付来源

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 答案evidence_registry=&#91;&#93;，所有reaction_evidence_id、enzyme.evidence_id均为null；仅uncertainties说明“酶和微生物来源未确定”，但没有文献/数据库/计算记录可定位到具体结论。按D5 MISSING_SOURCE低分档取1：几乎无法定位重要结论依据；MISSING_SOURCE默认不cap，无VERIFIED_MIS_CITATION_*。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 为空数组，两步的 reaction_evidence_id 与 enzyme.evidence_id 均为 null，底物/产物与终点结论无任何来源记录或生成记录，属MISSING_SOURCE（缺失而非误导）；决策相关组CG01/CG02/CG03/CG05/CG07均无条目级可核对来源，无已核实错引、无CRITICAL/SYSTEMIC情形，默认不cap；按D5低分档取1。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求来源登记；不证明答案已交付来源
- ANSWER_TEXT / ANSWER_BEGIN：答案完全无来源记录，仅有“来源未确定”的文字；支持MISSING_SOURCE低分档

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案将酶confidence标为unknown、微生物全部null，并在uncertainties说明酶/微生物来源未确定及“主链可能延伸至硫醇下游代谢”，未系统性把预测写成实证，也未编造身份/数值。但不确定性说明较笼统：未明确区分路线/产物是预测还是推断，未对S2主产物结构这一关键结论作待核说明，部分结论强度仍超过无证据依据。按5–6档取6（有不确定性说明但过于笼统，部分结论强度仍超过依据）。

<details><summary>V0.4理由与本行变化背景</summary>

未知项标注诚实：两步 enzyme.confidence=unknown、microorganism=null、organism_profiles=&#91;&#93;，uncertainties 明确写出&#x27;酶和微生物来源未确定；主链可能延伸至硫醇下游代谢&#x27;，未把预测包装成数据库观测、未给虚高置信、无掩盖矛盾；但未系统说明本路线属推断/预测及其依据，披露偏简短。属&#x27;大部分未知被正确标注、主要限制已说明&#x27;的7–8档，取7。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求未知填null、区分不确定性；不证明答案披露充分
- ANSWER_TEXT / ANSWER_BEGIN：答案有部分未知披露，但未对关键产物结构作具体待核说明；支持5–6档

</details>

## Kimi

答案SHA256：`0bed2048011252a71136b3417ff91f8646c6ab49b1cc6305ab27a2b656203971`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> D1按一条认可主链评：题面要求3步（S03入口透性酶→S02二肽水解→S01 β-消除）。答案给出S1水解和S2 β-消除两步，缺少S03入口透性酶步骤，路径覆盖2/3；但JSON可读、路线名原样、步骤字段和15项性状字段齐全。按&#91;5,6&#93;中段取5：主要模块有涉及，但必要入口步缺失且仅给两步主链。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖登记：两步主链均给出底物/产物英文名+SMILES、单个首选酶+EC、单个对应菌；route_scope.chosen_route_name按题面原样填写（未改选路线）；organism_profiles按物种+菌株去重为1条并被两步引用；15项性状全部出现（F3_pH、F4_salinity为诚实null）；evidence_registry与uncertainties已交付。遗漏：gold主链含S03二肽/三肽通透酶转运步（EC NOT_OBSERVED、无化学转化），答案未列，属少量遗漏。按&#x27;大部分必要内容完整、关联清楚，仅少量遗漏&#x27;取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：被测答案原文；用于定位步骤数、字段完整性与缺失入口步，不视为外部证据。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_141：冻结case元数据；支持本题为LINEAR_UNIQUE且required step count为3，不把全图旁支当作必答分母。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：冻结gold反应行；支持S01/S02/S03的底物、产物、方向及步骤存在，不证明答案来源或具体蛋白活性。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> D2只看化学：S1为半胱氨酰甘氨酸二肽水解生成S-取代半胱氨酸+甘氨酸；S2为半胱氨酸S-共轭物β-消除生成相应硫醇+丙酮酸+氨。两步方向、结构连接与gold S02/S01核心转化一致，产物SMILES与gold terminal thiol/pyruvate相符。主要不足是主链缺少S03入口透性酶步、跨膜进入未表达，且所给微生物/酶支持不能回填D2。按允许&#91;3,6&#93;取6：主干化学成立，但路线连续性/完整性仍有必要修订。

<details><summary>V0.4理由与本行变化背景</summary>

两步化学与gold一致：步1（gold S02）二肽水解生成S-取代半胱氨酸（SMILES N&#91;C@@H&#93;(CSC(C)(CCO)CCC)C(=O)O，与gold BSY-c16749同结构）+甘氨酸；步2（gold S01）β-消除/C–S断裂生成CCCC(C)(S)CCO（与gold 3-Methyl-3-sulfanylhexan-1-ol的SMILES CCCC(C)(CCO)S同结构）+丙酮酸+氨；方向、连接与碳骨架计量（C10→C7+C3）成立，止于gold/题面终点并声明下游未列入评分主链（不因未延续下游扣分）。局部缺陷：两步均未列H2O参与（水解与β-裂解均需水），字面计量不完整，按P103作局部计量缺陷在7–8档处理，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：被测答案的反应式与SMILES；用于核对两步转化的方向、底物/产物和连续性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：冻结gold反应行；支持S02水解和S01 β-消除的底物/产物/方向，不证明答案的微生物归属。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_141：冻结根/终点身份；支持本题终点含Pyruvate与3-Methyl-3-sulfanylhexan-1-ol，不扩展到未声称下游。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 本题目标层N=3。答案仅给出两步：S1用EC 3.4.13.6 cysteinylglycinase完成S-取代半胱氨酰甘氨酸水解，S2用EC 4.4.1.13进行C–S裂解；两步化学反应方向与参考主链的两项转化相符，但S1的EC与冻结accepted集3.4.13.23不同，S2的名称—EC配对在冻结状态中仍为U；同时缺少S03 dipeptide/tripeptide permease这一预定义KEY_ENTRY步骤。没有已核S，也没有可成立F；部分交付可读、一步EC与accepted相同、另一步功能性合理但待核，且关键入口步缺失，按C04部分M+U与C05低档边界评3分。

<details><summary>V0.4理由与本行变化背景</summary>

步2 EC 4.4.1.13=cysteine-S-conjugate beta-lyase，与gold同一EC，基因Irc7p与该活性相符，属主要步骤可靠支持。步1 EC 3.4.13.6（cysteinylglycinase）与gold EC 3.4.13.23（cysteinylglycine-(S) conjugate dipeptidase）同属3.4.13.-二肽酶，反应类型（肽键水解）匹配、酶名与EC不矛盾，但为通用二肽酶、对S-共轭底物的适配系答案自述外推（EVID_001 claim_scope明示applied here）。E0无任何EC条目（GAP-141-003/006/008/012），accepted name/reaction无法核实→按P66登记UNRESOLVED、保留扣分、不cap。取7（主要步骤对应有支持，少量条目待确认）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：冻结参考必答酶集合：S01 cysteine-thiol lyase/EC 4.4.1.13；S02 cysteinylglycine-(S) conjugate dipeptidase/EC 3.4.13.23；S03 dipeptide/tripeptide permease为NOT_OBSERVED。该表只支持目标酶集合，不自动证明答案酶名/EC配对正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：冻结参考反应方向与产物：S02为S-取代半胱氨酰甘氨酸水解为S-取代半胱氨酸+甘氨酸；S01为β-消除/C–S裂解生成硫醇+丙酮酸+铵；S03为摄取/转运步。支持目标反应定义，不证明答案所用具体酶即为accepted。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S2&#93;.enzyme：答案明确只交付两步酶：EC 3.4.13.6与EC 4.4.1.13；没有交付任何permease/转运步。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案两步均归Saccharomyces cerevisiae S288c。S2有Irc7p/SGD条目支持S. cerevisiae具cysteine-S-conjugate β-lyase活性；S1只以DUG/Dug1p内部知识支持Cys-Gly二肽酶，且明确不声称对该exact S-取代底物有活性。S288c的TaxID 559292、ATCC 204508、GCF_000146045.2在E0中无冻结记录，不能核实。故有合理候选和部分支持，但步级能力与菌株身份/作用范围仍有关键未核；按&#91;5,6&#93;取5。

<details><summary>V0.4理由与本行变化背景</summary>

身份层：Saccharomyces cerevisiae S288c（TaxID 559292、ATCC 204508、GCF_000146045.2）为真实可识别的菌株粒度，无编造迹象。反应层：步2 Irc7p β-裂解酶有SGD条目型来源（EVID_003）、步1的DUG通路Cys-Gly二肽酶为INTERNAL_KNOWLEDGE_ONLY（EVID_007，答案亦声明对该确切底物不作断言），均属物种级证据。路径层：两步均归同一菌并设complete_pathway_organism_profile_id=ORG_001，等于以物种级/单步酶活推断整条主链能力，属八.D3b①粒度不足并含单步→全路径外推，档内扣分；身份与能力均无经核实错误，不cap。取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：被测答案的微生物字段与profile；用于核对S. cerevisiae S288c身份及两步归属。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_141：冻结参考微生物归属；参考菌为S. hominis/Corynebacterium sp. Ax20，不等同答案菌，也不能证明S. cerevisiae能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 15项性状字段齐全，F3 pH与F4盐度为明确null（2项），其余13项有值；S. cerevisiae的F1/F2/F6/F10/F11/F12/F13等为常见表型，F14 genome accession/大小/GC与S288c参考基因组常识相符，F8/F9与Irc7p活性叙述一致。但多数性状仅INTERNAL_KNOWLEDGE_ONLY或未在E0核实，pH/盐度关键项为空，且没有同菌gold参照。按&#91;5,6&#93;取6：部分性状准确且适用，关键项证据/条件仍不足。

<details><summary>V0.4理由与本行变化背景</summary>

15项中13项填写，F3_pH与F4_salinity为诚实null；性状与所指身份（S. cerevisiae S288c）关联，内容与身份自洽（兼性厌氧/无运动性/卵圆出芽/真核细胞壁/单倍体MATα不产孢/GCF_000146045.2与12.16 Mb、38.3% GC），F8/F9限定作用范围、未把单步酶活写成广谱降解；F2仅给optimum_c=30并用preference注明为实验室培养常用温度，未当成测得最适或上下限。但E0中该菌株全部性状子字段为EVIDENCE_GAP_TRAIT_SUBFIELD（无官方性状记录），除F14外多数性状仅由INTERNAL_KNOWLEDGE_ONLY（EVID_006）支撑，F5/F14条目级来源不可核。按&#x27;部分性状准确且适用、关键项证据不足&#x27;取6；缺失项归D1，不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：被测答案的15项性状字段、null项和confidence标签；用于评估已给内容及显式未知。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_141：冻结参考菌性状；对应S. hominis/Corynebacterium sp. Ax20，不覆盖S. cerevisiae S288c，故不能直接核验答案性状。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给EVID_001/002/003/004/005具体数据库/记录ID及EVID_006/007内部知识来源；核心路线、关键酶、S. cerevisiae身份至少可定位到EC、SGD、ATCC、NCBI Assembly条目，不是纯GENERIC_SOURCE。但E0无EC 3.4.13.6/4.4.1.13、SGD YFR055W、TaxID 559292、ATCC 204508、GCF_000146045.2等冻结记录，均只能UNRESOLVED_SOURCE；许多性状仅INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE。未发现经核实的错引（无VERIFIED_MIS_CITATION_*），不cap。按部分关键结论可定位、其他模块缺映射/记录取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案对两步与关键身份给出条目级可定位记录（ExPASy ENZYME 3.4.13.6/4.4.1.13、SGD YFR055W/IRC7、NCBI Assembly GCF_000146045.2、ATCC 204508），非仅笼统库名，故不落3–4档。但E0本题slice仅含与本案无关的Pseudomonas putida记录（bacdive:12880、taxid:303），EC/TaxID/ATCC/assembly/自由文本条目全部为EVIDENCE_GAP→一律UNRESOLVED_SOURCE，不判虚构、不判CONTRADICTED、不cap；同时决定相关组内存在INTERNAL_KNOWLEDGE_ONLY（EVID_006/007：步1菌归属与多数性状）。按P41合成规则落5–6档，取5。无已核实错引，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：被测答案的evidence_registry及引用映射；用于判断来源交付是具体条目、内部知识还是缺失。
- E0_EVIDENCE / f3e0:bacdive:12880：E0快照条目为P. putida记录，不是本答案的S. cerevisiae，也不能核验本题EC/身份；仅用于说明E0缺口。
- E0_EVIDENCE / f3e0:taxid:303：E0快照仅给Pseudomonas putida种级分类记录；不支持S. cerevisiae S288c或本题EC，仅用于说明快照不覆盖答案来源。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：冻结accepted酶/EC行；可用于对照答案EC，不证明答案外部引用存在或具体蛋白活性。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 答案区分DATABASE_DIRECT与INTERNAL_KNOWLEDGE_ONLY，给出confidence low/medium/high，逐step uncertainty与全局uncertainties说明非直接O2、exact底物无记录、S. cerevisiae为代表性选择；pH/盐度明确null。主要局限是部分核心记录（EC、TaxID、ATCC、SGD）未核，且对EC 4.4.1.13/EVID_002标high、F14标high但E0不可核，属于局部过强而非系统性把预测写成实测。按&#91;7,8&#93;取7：不确定性和边界大体清楚，仍有少量置信/来源边界需收紧。

<details><summary>V0.4理由与本行变化背景</summary>

答案区分DATABASE_DIRECT与INTERNAL_KNOWLEDGE_ONLY，逐条给confidence；未知项（F3_pH、F4_salinity）填null而非编造；uncertainties具体列出氧条件未定、无该确切底物的完整降解菌记录、替代二肽酶（EC 3.4.13.19）未列第二候选；步1菌confidence=low与证据不足相称，F8限定&#x27;不作广谱异源物降解菌处理&#x27;。轻微问题：complete_pathway_organism_profile_id=ORG_001形式上声明整条路径能力，与正文&#x27;未找到完整降解菌记录&#x27;存在内部张力；F14以high置信呈现但其条目在E0不可核；多数性状以medium置信寄于INTERNAL_KNOWLEDGE_ONLY。属局部强度不当而非系统性把预测写成实证、未掩盖已知矛盾→按7–8档取8，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：被测答案的uncertainties、step uncertainty与confidence标签；用于判断证据性质区分和边界披露。

</details>

## Qwen

答案SHA256：`daae4c4d40932f7ce3f4503e444f2404b38f45c22fd70aa1d85d16098abc0eda`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 题面要求的主要模块均有实质回应：route_scope.chosen_route_name原样保留题面路线名、oxygen_condition=null与题面一致，steps各含底物/产物(SMILES)/首选酶+EC/对应菌并绑定profile，15项性状齐全且有3项显式null(F4/F5/F14)、无遗漏，来源与不确定性模块均在。但按本题task_scope该主链为3步(含S03二肽/三肽通透酶摄取步)，答案只交2步、未给出该步；另S1底物与S2产物的名称(7碳)与SMILES(6碳)碳数不一致，削弱步骤-结构对应。属“主要模块均涉及、若干必要内容遗漏”区间，除该步外字段与关联完整、未知显式标注，取本档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块实质回应：两步主链链条清楚（第1步二肽水解、第2步C-S裂解），每步均给主底物/主产物英文名与SMILES、一个首选酶含EC、一个对应微生物并绑定organism_profile_id；路线起点即题面根化合物S-(6-hydroxy-4-methylhexan-4-yl)-L-cysteinylglycine；route_scope.chosen_route_name逐字回填题面路线名，氧条件null按未指定保留；15项性状全部出现（12填写+3明确未知+0遗漏），明确未知不与遗漏混同。扣分点：未给具体菌株（strain=null）、仅1个菌覆盖两步、证据模块薄弱属他维；gold的S03双肽/三肽通透酶为转运步而非化学转化，未单列不按遗漏重扣。落7–8档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_141：仅支持本题参考主链的步数与图形态，不证明答案必须覆盖全DAG旁支，也不替代选链绑定
- ANSWER_TEXT / ANSWER.steps：仅支持答案实际交付两步及其字段，不证明其科学正确性

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 主链化学骨架部分成立：S1为二肽水解(胱氨酰甘氨酸→S-取代半胱氨酸+甘氨酸)，S2为半胱氨酸结合物C-S β-裂解(→硫醇+丙酮酸+氨)，转化类型、前向方向与步骤衔接(S1产物即S2底物)一致，C/N计数在答案自身结构内自洽，未见方向反转或明显原子不守恒。但全部交付结构相对题面/参考化合物少一个碳(S1底物SMILES CCC(C)(CCO)...为6碳，case root为CCCC(C)(CCO)...7碳；S2产物SMILES CCC(C)(CCO)S为6碳，参考S01主产物CCCC(C)(CCO)S为7碳)，且同一物质名称写7碳而SMILES写6碳，终点主产物与gold终点(3-Methyl-3-sulfanylhexan-1-ol|Pyruvate)结构不符。属“主干部分成立、关键中间体/结构需实质修订、合理性证据有限”5–6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold一致且连续：第1步为S-取代胱氨酰甘氨酸+H2O→S-取代半胱氨酸+甘氨酸（对应gold S02二肽酶水解，产物BSY-c16749与glycine一致）；第2步为S-取代半胱氨酸+H2O→硫醇+丙酮酸+氨（对应gold S01 C-S裂解，产物为3-methyl-3-sulfanylhexan-1-ol、pyruvate、ammonium）。方向SUBSTRATE_TO_PRODUCT、前驱关系、辅底物水、主产物骨架均正确；丙酮酸以中性酸形式、铵以NH3形式给出属可接受的质子化差异。缺陷：第2步产物6-hydroxy-4-methylhexane-4-thiol的SMILES写作CCC(C)(CCO)S（6个碳），而名称（hexane骨架+4位甲基=7碳）与底物侧链（7碳，gold同物为CCCC(C)(CCO)S）要求7个碳，字面少一个CH2且未说明，构成局部结构/计量不守恒；属7–8档&#x27;少量局部问题不改变主要结论&#x27;，但结构表示需修订，取7不取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：仅支持这两步的底物/主产物结构与反应方向，不证明具体蛋白活性或其他步骤
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_141：仅支持题面化合物的7碳骨架与终点结构，不外推到其他化合物
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.substrates&#91;0&#93;.smiles：仅支持答案自身交付的结构字符串与名称并存且碳数不一致

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> 程序冻结计数：S=0、F=1(KEY终点步S01 NONMATCH，ROUTE_BLOCKED_NONMATCH)、U=2，N=3，C=0.00；D-KEY4已确认KEY存在合法F，触发上界4，故在&#91;1,4&#93;内定档。已核可用信息仅有S02结构级别对齐(二肽水解底物/产物方向一致，但EC配对未核)，无任何确认目标信用；KEY终点步产物结构不符使主推荐(终点产物)失效。按C05的&#91;1,4&#93;受限档：无确认S、仅少量局部可用化学信息且核心结论失效→取2；不因两个未决匹配的存在抹去已确认KEY失败，也不机械取上界4。

<details><summary>V0.4理由与本行变化背景</summary>

第2步cysteine conjugate beta-lyase EC 4.4.1.13与gold S01 cysteine-thiol lyase的EC 4.4.1.13完全一致，酶功能（C-S β-消除）与反应类型相容；第1步给cysteinylglycine dipeptidase，功能名称与二肽水解反应类型匹配，但具体EC 3.4.13.19与gold S02的3.4.13.23不同。E0本题切片对EC 3.4.13.19与4.4.1.13均无冻结条目（item级GAP-141-002/005/007/011），无法按accepted name/reaction裁定，按四.5/四.6保守处理：保留低分与待核标记，不判错、不cap。未发现&#x27;酶名-EC互相矛盾&#x27;或&#x27;EC大类别与反应类型不匹配&#x27;的已核实证据，落7–8档（少量条目待确认），取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：仅支持S01目标反应的结构与方向，用于核对终点主产物一致性
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：仅支持各步参考酶名/EC与NOT_OBSERVED状态，不证明任意具体蛋白底物谱
- ANSWER_TEXT / ANSWER.steps：仅支持答案交付的产物结构字符串

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 身份层：答案只声称Pseudomonas putida(TaxID 303, strain=null)，其名称-TaxID关联经E0官方分类记录支持(SUPPORTED)，且声称粒度与种级记录自洽，未见身份错配或编造。能力层：两步均绑定同一ORG_001，且complete_pathway_organism_profile_id=ORG_001，但无任何反应级或全路径能力证据(CG08/CG09均UNRESOLVED)；gold步级参考菌为Staphylococcus hominis与Corynebacterium sp. Ax20，属另一可接受候选而非须自动判错。故为“合理候选+部分身份支持、关键作用范围/能力未核验”5–6档，取5，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

两步均归Pseudomonas putida（TaxID 303，strain=null）。身份层面：E0核实303=Pseudomonas putida（种级，状态CURRENT），答案未越级声称菌株号/保藏号，故非编造、非跨类群错配。作用范围层面存在三层越级：仅种级身份记录，无任何该菌催化这两步的反应级证据（EVID_002为INTERNAL_KNOWLEDGE_ONLY），却设complete_pathway_organism_profile_id=ORG_001把整条路径能力归于该菌；gold步级来源菌为Staphylococcus hominis（S01/S03）与Corynebacterium sp. Ax20（S02），答案未给出替代归属依据。属于&#x27;有合理候选和部分支持、但关键作用范围未充分核验&#x27;，落5–6档，因整条路径能力声称完全无支撑取5。不按已核实关键错误处理（未核≠错误），key_error记UNRESOLVED。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持种级学名-TaxID关联与分类状态；不支持菌株身份、保藏号或任何催化/整路能力
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_141：仅支持参考步级菌归属；不证明其他菌不能催化，也不证明答案菌具备该能力

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 格式与完整性：15项全部出现，12项填值、3项(F4/F5/F14)显式null且confidence=unknown，未编造保藏号/基因组号。适用性：性状对象为种级Pseudomonas putida，无同株冻结性状记录；E0仅f3e0:bacdive:12880(mt-2 PaW1株)提供26°C/30°C growth培养记录，按解释层培养温度≠最适值，故F2 optimum_c=30属把培养记录性数值写成最适值且raw_text=null；F1 aerobic/F6 O2末端受体、F7碳源谱、F8/F9等均无同株可核证据(CG10-CG15来源为INTERNAL_KNOWLEDGE_ONLY)。属“部分性状合理且适用、但关键项证据不足或条件解释需修订”5–6档，取5；未出现数值离谱或把物种级观测强推为全物种性质，故不cap。

<details><summary>V0.4理由与本行变化背景</summary>

12项填写、3项明确未知（F4盐度、F5保藏、F14基因组），无遗漏；性状按种级Pseudomonas putida给出，与未声明菌株的粒度一致，未把单菌株观测推广为全物种性质，也未把预测值冒充观测值（全部confidence=low、evidence=EVID_002 INTERNAL_KNOWLEDGE_ONLY）。可核项多为种级一致性描述（革兰氏阴性、杆状、运动、不产孢、好氧呼吸以氧为末端电子受体、化能异养），与物种属性相符；数值与重要项证据不足：F2 optimum_c=30与F3 optimum=7.0属未核实预测（E0 bacdive:12880仅给26/30°C培养记录，培养温度≠最适温度，不能回填为最适值），F9&#x27;具肽酶及半胱氨酸结合物裂解活性&#x27;直接用于支撑路线但无来源。属&#x27;部分性状准确且适用、关键项证据不足&#x27;，落5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：仅支持该菌株培养记录与保藏号集合；培养温度不证明最适值或上下限，不覆盖形态/氧需求/碳源谱等字段
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_141：仅说明本题参考侧性状子项的可评分状态，不适用于答案所用种级对象本身

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案evidence_registry仅两条：EVID_001=MODEL_INFERENCE、EVID_002=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null，claim_scope仅为内部标签；按六状态口径，决策相关组(CG01/CG02/CG03/CG05/CG07/CG08/CG09)均无可定位交付来源=MISSING_SOURCE。唯一正向可核是TaxID 303名称关联(SUPPORTED)，但答案自身未交付该定位，属评价侧证据不回填。无任何VERIFIED_MIS_CITATION_*，故不触发cap；全部决策相关组仅自我声明→低分档，取2(略高于1因claim_scope与confidence标签使“缺来源”本身可读)。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：全部决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09及CG10–CG14）均为MISSING_SOURCE——EVID_001为MODEL_INFERENCE（database/record_id/locator全null），EVID_002为INTERNAL_KNOWLEDGE_ONLY，按四.3定义属&#x27;完全无引用或仅内部知识自我声明&#x27;；无任何可定位条目、DOI或数据库记录，亦无计算输入/模型版本/输出记录。按P34/P41：全部缺失→低分档且默认不触发cap；八.D5要求&#x27;来源缺失达到使D5主要结论完全不可追查且写明依据&#x27;才构成关键错误——本答案确无一条可追查结论，但其证据登记结构自洽、claim_scope明确、未编造编号或伪造文献，故落1–2档并取档内上限2。无已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION；身份类事实（TaxID 303）虽经E0核实正确，但答案未交付该来源，不回填为原交付证据（OBS-POS-LOCATABLE）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：仅支持答案实际交付的来源记录形态，不构成可追溯条目
- E0_EVIDENCE / f3e0:taxid:303：仅支持种级名称-TaxID关联可在评价侧核实；不代表答案交付了该来源

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 证据性质标注较具体且一致：全部事实confidence=low/unknown，来源类型明写MODEL_INFERENCE/INTERNAL_KNOWLEDGE_ONLY，uncertainties分三条说明“无专属实验降解文献、菌归属为低置信推断未确认菌株、硫醇下游缺乏可靠来源故不列入主链”，未把推断包装成观测。不足：未披露自身结构式与名称碳数不一致(6 vs 7碳)，F2 optimum_c=30由培养记录性质转换而来且raw_text=null而未说明推导，属局部披露不足；非系统性误导，不cap。属7–8档“大部分观测/预测/未知正确标注、主要限制已说明”，取7。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界披露总体诚实且具体：来源标签把两步反应与酶归属明确标为MODEL_INFERENCE、把菌性状标为INTERNAL_KNOWLEDGE_ONLY，全部性状confidence=low/unknown，未把推断包装成数据库直查；uncertainties三条分别点明&#x27;无本底物专属实验路线文献，按胱氨酰甘氨酸结合物一般机制推断&#x27;&#x27;微生物归属为低置信推断、未确认菌株&#x27;&#x27;硫醇下游氧化/脱硫缺乏来源，未纳入主链&#x27;；未知项以null/no claim诚实交付（F4/F5/F14；P. putida基因组未虚填）。扣分：第2步硫醇SMILES与自身名称的碳数不一致未被察觉与披露，EC选择的不确定性未单列，置信表达统一low略欠分层。属&#x27;大部分观测/预测/未知被正确标注、主要限制已说明&#x27;，落7–8档，取8。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：仅支持答案自身的不确定性表述，不证明其结论正确
- ANSWER_TEXT / ANSWER.steps&#91;1&#93;.products&#91;0&#93;：仅支持存在未被披露的名称/SMILES碳数不一致

</details>

## Grok

答案SHA256：`05dccdf296913bfd4b39a02a69d924788fef7c51bf02c2dd26124a6f0a81ae6f`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 路线名按题面原样填写，但只交付了两步化学转化，未交付3步必答主链中的转运步；每一步的enzyme与microorganism均为null，organism_profiles为空数组，因而题目要求的每步首选酶/EC、对应微生物及15项性状全部缺失。任务核心模块大部缺失，D1主要完成度结论失效，按D1关键错误封顶≤4后在3–4档取低分3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：gold主链为S03转运、S02二肽酶水解、S01半胱氨酸硫醚裂解共3个必答步；答案只覆盖S02与S01两个化学步，缺少S03。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：gold为必答步记录酶/EC候选（S01 4.4.1.13、S02 3.4.13.23、S03 NOT_OBSERVED）；答案各步enzyme均为null，显示酶模块未交付。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_141：gold为步级微生物记录（如Staphylococcus hominis、Corynebacterium sp. Ax20）；答案microorganism均为null且无organism_profiles，显示微生物模块未交付。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_141：gold包含相关菌株的15项性状记录材料；答案organism_profiles为空，未填写任何性状。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出的两个化学转化与gold化学步相符：S1为胱氨酰甘氨酸缀合物肽键水解生成S-取代L-半胱氨酸和甘氨酸，对应gold S02；S2为S-取代L-半胱氨酸C-S β-裂解生成6-hydroxy-4-methylhexane-4-thiol（与gold 3-Methyl-3-sulfanylhexan-1-ol同一结构）与pyruvate、ammonia，对应gold S01。方向为底物到产物，主链连续，终点产物与gold terminal一致，水辅因子及简化表达未造成明显原子不守恒。缺S03转运步及低置信推断属局部问题，不改变化学主链判断；D2按允许范围&#91;1,8&#93;取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：gold S02行显示parent cysteinylglycine + H2O -&gt; S-(6-hydroxy-4-methylhexan-4-yl)-L-cysteine + glycine；gold S01行显示该S-取代L-半胱氨酸 -&gt; 3-Methyl-3-sulfanylhexan-1-ol + pyruvate + ammonium。答案S1/S2分别对应这两步化学转化与方向；不支持被省略的S03转运步或任何酶/微生物能力。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_141：gold终端主产物为Pyruvate与3-Methyl-3-sulfanylhexan-1-ol；答案S2产物pyruvate与6-hydroxy-4-methylhexane-4-thiol（同一结构）对应，终点化学一致。

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> C04整酶模块未交付：所有steps&#91;*&#93;.enzyme均为null，无可辨认酶/EC；D3a=MISSING、score=1。M=N是目标层事实，不把缺失当已核实催化错误；D-KEY4 cap=4不替代MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：gold列出S01-S03所需酶/EC；答案未交付任何enzyme对象，仅用于定位缺失模块，不用于推断答案酶正确性。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P44微生物模块完全未交付：steps&#91;*&#93;.microorganism均为null且organism_profiles为空；D3b=MISSING、score=1，不宣称已检测到身份/能力错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_141：gold列出步骤微生物；答案未交付任何菌名/菌株/归属，仅支持MISSING定位。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P44性状模块完全未交付：organism_profiles为空，题目要求的15项性状全部未提供；D4=MISSING、score=1，不宣称性状科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_141：gold存在Staphylococcus hominis与Corynebacterium sp. Ax20的性状记录；答案未交付profile/traits，仅支持MISSING定位。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 1–2档：重要结论仅能追到MODEL_INFERENCE的EVID_001/EVID_002，database/record/locator均null，且答案自述未核对原始记录；无DECISION_RELEVANT条目级可核对来源，属MISSING_SOURCE；非已核实错引，不cap。

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 9档：答案明确区分MODEL_INFERENCE、未核对记录与未知，逐条列限（酶/菌/性状null、SMILES推导、氧条件null、β-裂解底物效率未知）；无把预测冒充观测或掩盖矛盾；D5来源缺失不自动拉低D6披露质量。

## GPT5.6

答案SHA256：`92a8a2659e40f1f172dcf4b13909758d592df67caf5c51035d4407fc3f8b6a88`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1为3–4档：仅部分交付路线与酶，缺少required S03入口/通透步；所有step.microorganism为null，organism_profiles为空，15项性状完全未交付。路线名保持题面指定，但主要任务模块缺失严重，取3分。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：题面要求每步给出一个对应微生物，并提交15项性状及各项最强来源。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：gold主链含S01/S02/S03三个必答步；证明答案缺少S03入口/通透步，不支持把两步当作完整三步步链。
- ANSWER_TEXT / ANSWER：答案实际仅交付S1/S2，且无微生物与性状内容。

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2为5–6档：S1肽键水解与S2半胱氨酸S-共轭物β-裂解两步核心化学转化、方向及主产物与gold一致；终点硫醇/丙酮酸/氨合理。缺少S03入口步主要归D1；S2额外列水为辅因子及来源支持有限，使本维不进入更高档，取6分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：gold S02为二肽水解，S01为β-裂解生成硫醇/丙酮酸/铵；支持答案两步的核心化学转化与方向。
- ANSWER_TEXT / ANSWER：答案给出S1水解、S2β-裂解及相应底物/产物。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a按目标反应逐项核酶对应。金标要求3步：S01半胱氨酸-硫醇裂解酶EC 4.4.1.13；S02半胱氨酰甘氨酸-(S)-共轭二肽酶EC 3.4.13.23；S03二肽/三肽通透酶（无EC）。答案仅交付2步：其β-裂解步骤给出EC 4.4.1.13，EC与金标accepted一致但名称—EC配对及具体催化支持在冻结证据中仍为UNRESOLVED/CANDIDATE_ONLY，不能计S；其肽键水解步骤给出EC 3.4.13.6，与金标accepted EC 3.4.13.23不一致且关系未核，计U而非S；金标S03通透酶/进入步骤在答案中完全缺失，计M。故无已确认S，存在一个明确漏交必答步骤和两个未达S的U；主链酶对应不完整，不能进入9–10或良好档。依C05，少数目标有局部可用线索但可用部分与主要缺失/非accepted对应边界仅勉强分清，取3分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_141：金标列明S01 cysteine-thiol lyase EC 4.4.1.13、S02 cysteinylglycine-(S) conjugate dipeptidase EC 3.4.13.23、S03 dipeptide/tripeptide permease无EC；支持逐目标步酶/EC对照，不自动证明答案具体蛋白活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_141：金标给出S01 β-裂解和S02肽键水解的方向、底物与主产物；用于核对答案所配反应类型和EC指向，不自动确认答案的显式EC配对或微生物能力。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b对应模块完全未交付：所有step.microorganism为null，organism_profiles为空，无法评价菌种/菌株身份、单步能力或全路径能力。按MISSING=1记分，不宣称已检测到具体微生物科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明答案没有交付任何微生物身份或能力声称。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4对应15项性状及来源完全未交付；organism_profiles为空，无任何observed/predicted性状可评。按全部性状缺失记MISSING=1，不宣称检测到具体性状数值错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明答案没有交付任何organism_profile或15项性状。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5为1–2档：关键路线/酶声称仅由evidence_registry EVID_001/EVID_002支撑，二者source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；重要结论无法定位到外部可核对来源。未发现已核实虚构或错引，故不cap，但取低档1分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：证明答案只给内部知识型证据，无外部定位信息。
- RUBRIC_CLAUSE / P34：MISSING_SOURCE/仅INTERNAL_KNOWLEDGE_ONLY按D5低分档，不默认cap。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6为7–8档：答案明确把酶/EC标为low confidence，evidence_registry标为INTERNAL_KNOWLEDGE_ONLY，uncertainties列明未指定氧条件、未确认整链微生物、缺少该特定化合物直接实验证据；总体诚实，未把预测写成实证。扣分点是未对缺失的性状/微生物模块逐项说明未知。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案对酶/EC证据性质与主要未知有具体说明。

</details>
