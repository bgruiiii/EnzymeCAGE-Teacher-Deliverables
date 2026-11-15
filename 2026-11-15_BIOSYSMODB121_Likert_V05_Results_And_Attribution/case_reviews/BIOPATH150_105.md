# BIOPATH150_105：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-coumarate degradation (anaerobic)

污染物：4-Coumarate；氧条件：anaerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 50 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 46 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 47.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 61.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 48 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 35 | COMPARABLE | USER_AUTHORIZED_RECOLLECTION_R1 |

## GLM

答案SHA256：`f535e384b2acc937c5f9c9efd4c0a752a33b7858ab12e18dcdedc8b7724e716b`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 格式与模块基本完整：5步、每步底物/产物/SMILES/酶/EC/菌、15项性状和证据表均给出。但主链采用5步β-氧化型替代路径，未按Gold六步主链交付4-羟基苯甲醛和4-羟基苯甲酸段等必经转化，任务符合度落在弱档；因路线偏离确认，取4而非5。

<details><summary>V0.4理由与本行变化背景</summary>

5步均给出主底物/产物英文名+SMILES、首选酶+EC、对应微生物；route_scope原样填 anaerobic 与 &#x27;4-coumarate degradation (anaerobic)&#x27;，止于题面终点benzoyl-CoA；15项性状齐备(12填写、3明确未知)，另附evidence_registry/uncertainties。主要扣分：多条已填性状无evidence_id(违反&#x27;各项最强来源&#x27;)；以单一代表菌覆盖全链(题面允许但削弱分步微生物表述)。非工程损坏。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：Shows the six-step gold main chain and terminal benzoyl-CoA; does not by itself establish that the answer&#x27;s alternative route is chemically invalid.
- ANSWER_TEXT / ANSWER：Shows the answer delivered a five-step CoA-dependent route and omitted gold S02/S01 intermediates.
- SCOPE_ROW / SCOPE#BIOPATH150_105#CG04：Confirms anaerobic task condition; does not verify the answer&#x27;s specific route.

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> S1-S5的CoA活化、水合、脱氢、硫解和还原脱羟在方向上连贯，可到达benzoyl-CoA，未见明显原子不守恒。但该路径绕开Gold的4-羟基苯甲醛/4-羟基苯甲酸段，关键中间体与步骤连接同参考主链不同，S1-S4主要依赖自述知识；落在部分可用、需实质修订的5档上限。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学自洽且连续：S1 CoA活化；S2 水合生成3-OH(马氏加成于芳基碳)；S3 NAD+脱氢为3-oxo；S4硫解经核算断裂C2-C3键生成4-hydroxybenzoyl-CoA+acetyl-CoA(原子与方向正确)；S5还原脱羟基→benzoyl-CoA，止于题面终点。属β-氧化型合理替代路线(与gold的hydratase/lyase→4-hydroxybenzaldehyde路线不同但同为文献记载的厌氧4-coumarate路线)；S5未列低电位电子供体属局部计量缺陷(7-8档)。无起始步错/无依据跳步/无不守恒。alternative_branches已标is_part_of_scored_main_route=false。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：Shows gold route via 4-coumaroyl-CoA, 3-hydroxy intermediate, 4-hydroxybenzaldehyde, 4-hydroxybenzoate, 4-hydroxybenzoyl-CoA, benzoyl-CoA.
- ANSWER_TEXT / ANSWER：Shows answer&#x27;s alternative beta-oxidation-like route and its cofactor handling.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> S=0，F=4（S03-S06为确认的KEY目标失败），U=2（S01/S02对齐未确认）。答案没有目标步获得S信用；仅S5的酶名和末端反应与Gold S03有局部相似，但EC/路线仍不符，不能回填目标信用。按C04低带取2，D-KEY4上界4未突破。

<details><summary>V0.4理由与本行变化背景</summary>

S2 EC4.2.1.17(enoyl-CoA hydratase)、S3 EC1.1.1.35、S4 EC2.3.1.16与反应类型/名称一致；S5酶功能(还原脱羟基)与反应相符但EC 1.3.7.13与gold该步标注1.1.7.1不符、S1 &#x27;4-coumarate—CoA ligase&#x27; 名称正确但EC6.2.1.33与gold该步6.2.1.12/6.2.1.34不符——E0无官方EC记录，按UNRESOLVED待核，不判错不cap。S2-S4为通用β-氧化酶套用于芳香底物，答案明示未逐一鉴定专一酶。故有多处关键EC待核，落6档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：Shows target reactions for S03-S06; confirms the answer&#x27;s corresponding chemistry/EC does not match required target steps.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：Lists accepted enzyme/EC sets; does not prove every alternative enzyme cannot act, but supports target nonmatch for program-fixed steps.
- ANSWER_TEXT / ANSWER：Shows answer enzyme names/EC on an alternative route.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Thauera aromatica K172身份本身合理，S5的4-hydroxybenzoyl-CoA reductase也有文献关联；但答案把同一菌用于S1-S4并声明complete_pathway_organism_profile_id=ORG_001，缺少全路径能力和步级归属证据。Gold中Thauera仅覆盖S01/S03，多个步骤对应未核，落在合理候选但关键作用范围未充分核验的5档。

<details><summary>V0.4理由与本行变化背景</summary>

核心身份 Thauera aromatica K172 真实正确(物种+菌株级一致)，TaxID留null未编造；但将全部5步(含S2-S4 β-氧化步与S1连接步)统一归给T. aromatica并在complete_pathway_organism_profile_id=ORG_001宣称全路径能力，缺该菌完成这些专一反应/整链能力的直接证据(gold将各步分给T. aromatica/R. palustris/Sphingomonas/Aromatoleum多菌)——属&#x27;单菌写为整链菌&#x27;的范围过度外推。答案uncertainties已披露仅作代表菌、其他厌氧菌亦可，属诚实但仍是粒度过度。E0 gap无法核实，不判身份编造、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_105：Shows Thauera appears at S01/S03 in gold, while multiple other steps have different gold organisms; does not prove Thauera cannot also act at other steps.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：Shows required step reactions; supports examining step-level organism attribution.
- ANSWER_TEXT / ANSWER：Shows answer used one Thauera profile for all steps and made a complete-pathway claim.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 15项性状均返回，明确未知3项。F1/F6/F10/F12/F13等与Gold观测或预测相符，F2中温偏好相符；但F7广谱碳源与4-coumarate利用、F8广谱降解、F15栖息地广适性缺少直接证据，F11杆状与Gold球杆状略有差异，F5/F14可核实值未填。属部分可用、需实质修订的6档。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状多数可核实且正确/合理：F1兼性厌氧-反硝化、F6硝酸盐呼吸→N2、F10具运动性、F12革兰氏阴性、F13不产芽孢与gold观测一致；F2 preference&#x27;中温性&#x27;与gold mesophilic一致；F9 Hcr酶活与Breese&amp;Fuchs对应。明显不填造数值(温度/盐度/pH/基因组数值均null)，避免编造。扣分：F11&#x27;杆状&#x27;对gold&#x27;coccobacillus-shaped&#x27;略不准；F7(可含4-香豆酸)、F8广谱降解、F15栖息地多为概括且无evidence_id或低置信；F5/F14本可填(DSM 14805、GAC_023093675.1/GC~67-68%)却null(完成度问题另记D1)。故落7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_105：Supports F1 oxygen/respiration, F2 mesophilic, F10 motility, F11 coccobacillus, F12 gram-negative, F13 non-sporulating, F5 DSM 14805, F14 genome data; does not confirm F7/F8/F15 claims.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_105：Indicates which trait fields are observed-accuracy versus completeness-only; does not convert missing values into errors.
- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s actual 15 traits and confidence labels.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D5按claim group登记：CG03终端和CG07身份有可定位文献（Breese &amp; Fuchs 1998; Anders et al. 1995），但CG01/CG02/CG05核心路线与S1-S4酶-EC主要依赖INTERNAL_KNOWLEDGE_ONLY（EVID_004）；CG08步级归属和CG14底物利用缺少可核条目。部分关键结论可定位、核心路线来源缺失，落5档；E0为EVIDENCE_GAP，不能判虚构，只记UNRESOLVED。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组呈混合：核心路线化学S1-S4仅EVID_004(INTERNAL_KNOWLEDGE_ONLY)=MISSING_SOURCE，全路径能力(CG09)亦无直接来源=MISSING_SOURCE；微生物身份CG07引EVID_002(Anders等1995)、S5引EVID_003(Breese&amp;Fuchs1998)两篇可定位文献=UNRESOLVED_SOURCE(E0无法核验其支持范围)。无任何已核实错引，severity不适用、不cap。因决策相关组存在部分可定位条目(身份、S5)但不可核对、且核心路线化学多为内部知识，落5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s actual delivered sources and their declared scopes; does not verify the citations.
- RUBRIC_CLAUSE / D5：Supports scoring MISSING_SOURCE/UNRESOLVED_SOURCE without treating E0 gap as mis-citation.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确区分null/unknown与已给值，给出confidence，说明EC编号凭记忆未核对、基因/TaxID/基因组未核，并列出其他厌氧菌和电子供体缺口。主要限制披露较具体；但route_summary以&#x27;确立/教科书级&#x27;描述无直接引用的路线，属局部过度确信、不构成系统性误导，取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体诚实：明确区分内部知识(EVID_004/EVID_001=INTERNAL_KNOWLEDGE_ONLY)与文献(EVID_002/EVID_003)；主动声明EC 6.2.1.33与1.3.7.13凭记忆未核对、S1-S4专一酶基因未定位、TaxID/保藏号/基因组未核实故null、S5电子供体缺失、并以T. aromatica为统一代表菌并列出其他可行菌。未知与预测未被包装成实证，置信标签(low/unknown)与证据相称。扣分：部分内部推断(F7/F8/F15)披露仍偏笼统、部分给medium置信。整体落7-8档上沿，取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows explicit unknown/uncertainty disclosures and confidence labels.
- RUBRIC_CLAUSE / D6：Supports distinguishing occasional overstatement from systemic misuse of evidence.

</details>

## DeepSeek

答案SHA256：`2d509e613e0a370a6720941f94934252c9dcd310c88c7a4c113544fbd1d06cdb`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> route_scope 原样回显 chosen_route_name=4-coumarate degradation (anaerobic) 与 anaerobic；JSON 字段齐全、无格式缺陷。5 步构成 4-coumarate→4-coumaroyl-CoA→4-hydroxybenzaldehyde+acetyl-CoA→4-hydroxybenzoate→4-hydroxybenzoyl-CoA→benzoyl-CoA 的连贯主链，每步均有底物/产物（含 SMILES）、酶与微生物，同一菌按物种+菌株去重为 ORG_001，符合第 3/4 条要求。按 D-M01 澄清，不以全图 ordered_step_count/n_required 或矩阵全体行构造单链缺步分母（current_path_id=null，该部分不据此扣分）。独立可判的完成度缺口仍存在：S3、S5 的 enzyme.ec_number 为 null，未满足“每步一个首选酶及 EC”；15 项性状虽全部出现却全部为 null（属诚实未知、非编造，按 P45 计入完成度不足）；evidence_registry 为空，性状“最强来源”与逐事实来源均未交付。总体属“主要模块均有涉及、若干必要内容遗漏/仅占位”，5–6 档；交付结构清楚、关联可读，取 6。

<details><summary>V0.4理由与本行变化背景</summary>

路线名原样填写（4-coumarate degradation (anaerobic)）、5步主链完整连至题面终点benzoyl-CoA、每步绑定酶与R. palustris CGA009，路径/酶/菌三模块完整且关联清楚。但任务明确要求的15项性状全部为null（仅占位）、evidence_registry为空（各项最强来源未交付），两个必需模块未实质交付，属5-6档‘若干必要内容遗漏、仅占位’；因核心科学模块完整正确，档内取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_105：题面要求：指定路线与厌氧条件、每步主底物/主产物名+SMILES+一个首选酶及EC+一个微生物、15项性状及最强来源
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_105：起点 4-Coumarate、终点 benzoyl-CoA(4-)、Anaerobic；仅用于任务身份，不用于给答案加分
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_105：LINEAR_UNIQUE、ordered_step_count=6 为全图材料计数，按D-M01不作单条主链缺步分母
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：gold 主链各步的主底物/主产物与连接（S04→S06→S05→S02→S01→S03），用于核对答案覆盖的转化与终点；不证明任何评分固定值
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际交付：5步主链、每步酶与微生物、15性状全null、evidence_registry空
- SCOPE_ROW / SCOPE#BIOPATH150_105#CG04：题面氧条件 anaerobic 为应用关键任务条件（D1用于核对条件遵守）

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 主链方向与连接成立：4-Coumarate→4-Coumaroyl-CoA（CoA活化）→4-Hydroxybenzaldehyde+Acetyl-CoA（水合/裂解）→4-Hydroxybenzoate（醛氧化，含 NAD+/H2O→NADH）→4-Hydroxybenzoyl-CoA（ATP+CoA→AMP+PPi）→Benzoyl-CoA（还原脱羟），终点与题面指定终点一致，无方向反转、无一步跳中心代谢物、无未说明的严重原子不守恒。缺陷：(a) 全部 CoA 硫酯 SMILES 缺核糖 3′-磷酸（实为 dephospho-CoA），与 4-coumaroyl-CoA/4-hydroxybenzoyl-CoA/benzoyl-CoA/乙酰-CoA 名称冲突，属关键中间体的结构表述错误，系统出现于 S1/S2/S4/S5；(b) S1 未列 ATP/CoA 与 AMP/PPi——题面只要求主底物/主产物，属局部计量简化；(c) S5 以 NADPH/NADP+ 作还原当量，而该步（EC 1.1.7.1，4-hydroxybenzoyl-CoA reductase）在 gold 中以还原型 2&#91;4Fe-4S&#93; ferredoxin 为电子供体，属局部辅因子/载体错误。以上均不推翻主链化学结论，不构成“主链第一步即错/方向反转/明显不守恒”等关键错误，但关键中间体结构需修订，故不进入 7–8 的“少量局部问题”，定为 5–6 档，取 6。

<details><summary>V0.4理由与本行变化背景</summary>

主链有机转化与gold逐步net一致：4-coumarate→4-coumaroyl-CoA→4-hydroxybenzaldehyde(+acetyl-CoA)→4-hydroxybenzoate→4-hydroxybenzoyl-CoA→benzoyl-CoA；方向与题面终点benzoyl-CoA合规，S2把gold的S06(水合)+S05(裂解)合为一步属双功能酶的合理简化。唯一局部问题：S5把生理电子供体reduced ferredoxin写作NADPH，属辅因子/电子载体局部误配，也属简化计量缺陷，不改变有机主链，按P103/SC3在7-8档处理。档内取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：gold 各步主底物/主产物结构、方向与辅因子（含 S03 的还原型 2&#91;4Fe-4S&#93; ferredoxin 与 H+、S01/S04 的 ATP/CoA/AMP/PPi）
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_105：终点 benzoyl-CoA(4-) 及 Anaerobic 条件
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：S03 目标酶为 4-hydroxybenzoyl-CoA reductase（EC 1.1.7.1），仅证酶类对应；不证明答案选用 NADPH 正确
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际书写的 SMILES 与辅因子：CoA 硫酯均缺 3′-磷酸；S5 使用 NADPH/NADP+；S1 仅列主底物/主产物
- SCOPE_ROW / SCOPE#BIOPATH150_105#CG04：厌氧条件为应用关键，用于核对所答化学是否与指定条件一致

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> N=6（S01、S02、S03、S04、S05、S06）。程序对齐显示 S01/S02 为 UNKNOWN（UNRESOLVED）、S03–S06 未绑定；按 C03“对齐未绑定不等于漏答”，改按实际交付与 accepted 支持评定：gold S04（入口，KEY）由答案 S1 交付（4-coumarate:CoA ligase，EC 6.2.1.12 在 accepted 集）；gold S01 由答案 S4 交付（4-hydroxybenzoate:CoA ligase，EC 6.2.1.25 在 accepted 集）；gold S03（终点，KEY）由答案 S5 交付（4-hydroxybenzoyl-CoA reductase，名称在 accepted 集，EC null）；gold S02 由答案 S3 以 4-hydroxybenzaldehyde dehydrogenase 交付（名称不在 accepted 名集、EC null，SUPPORT_GAP→U）；gold S06/S05 被答案 S2 合并为一步（EC 4.2.1.124 对应 accepted NOT_OBSERVED，不可核→U），且未交付 3S-(4-hydroxyphenyl)-3-hydroxy-propanoyl-CoA 的必经中间步（缺步 M=1，定位：全文无产生该中间体的 step）。计 S≈3、U≈2、M=1，C≈0.5→&#91;5,6&#93;；KEY 入口/终点均为交付而非已核失败，无 KEY4 ≤4 上界。5个酶中 S3/S5 缺 EC、2 个 EC 待核，近半目标处于 U/M，故不入 7–8；已支持部分逐反应关联清楚、待修部分定位明确，取 6。

<details><summary>V0.4理由与本行变化背景</summary>

S1 4-coumarate:CoA ligase EC6.2.1.12 与gold S04所注EC6.2.1.12一致；S4 4-hydroxybenzoate:CoA ligase EC6.2.1.25 与gold S01所列EC6.2.1.25一致；S5 4-hydroxybenzoyl-CoA reductase 名称与gold一致但EC填null（gold为1.1.7.1）；S3 vanillin/4-hydroxybenzaldehyde dehydrogenase 功能等价、EC填null。S2 EC4.2.1.124 在gold为NOT_OBSERVED、E0无记录不能核实。多数步骤酶-反应对应有可靠支持，少量EC缺失/待核，落7-8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：各必答步的参考酶名与EC：S01 6.2.1.25/6.2.1.27、S02 1.2.1.64/1.2.1.67/1.2.1.96（vanillin dehydrogenase）、S03 1.1.7.1、S04 6.2.1.12/6.2.1.34、S05/S06 NOT_OBSERVED；仅证参考粒度，不证具体蛋白活性
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_105：各步参考微生物：S01/S03/S04/S05/S06 为 Rhodopseudomonas palustris，S02 为 Sphingomonas sp. SYK6；仅身份定位，不等于整路径能力
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：6个必答目标反应的目标底物/产物（S06 产生 3S-(4-hydroxyphenyl)-3-hydroxy-propanoyl-CoA，S05 再裂解为 4-hydroxybenzaldehyde+acetyl-CoA）
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案实际给出的酶名/EC及各步反应；S2 为合并步、S3/S5 无EC；全文无 3-羟基丙酰-CoA 中间体
- SCOPE_ROW / SCOPE#BIOPATH150_105#CG04：厌氧条件为任务条件，用于核对路线而非直接给酶对应加分

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Main organism identity is supported at species level: Rhodopseudomonas palustris appears in several gold step rows and a PATHWAY_COMPLETE row. The answer&#x27;s strain CGA009/TaxID 258594 and the S02 R. palustris 4-hydroxybenzaldehyde dehydrogenase attribution remain unverified; this is a grain/step-specific identity gap, not a cap-level unrelated-taxon error. 7 fits the 7-8 band with only limited specific items needing confirmation.

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤归 Rhodopseudomonas palustris 菌株 CGA009；物种与gold全路径菌R. palustris（1076，PATHWAY_COMPLETE=TRUE）一致，CGA009为其经典代表菌株，单菌贯通整条路径与gold路径完整菌一致，未把单步菌写成整条路径菌（证据反方向：物种本身即全路径菌）。菌株级TaxID 258594在E0(EVIDENCE_GAP)无记录、gold只给物种级1076，故菌株级编号待核但不构成已核实错误。落7-8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_105：Supports Rhodopseudomonas palustris at species level for several steps and records a PATHWAY_COMPLETE row; does not verify strain CGA009/TaxID 258594 or every step-level organism attribution, especially S02.

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> All 15 required traits are present only as null/unknown values with confidence unknown. Under P44, all required traits null/empty is D4 MISSING=1, not a scientific-error finding.

<details><summary>V0.4理由与本行变化背景</summary>

organism_profiles&#91;0&#93;.traits 的 F1_oxygen_tolerance…F15_habitat_generalism 全部为 null、confidence=unknown，无任何可评价性状数值、单位或来源。按P44‘全部必需性状均为null/空值时D4记MISSING=1分，不宣称检测到科学错误’处理；完成度扣分已归D1，不在D4重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：Shows all 15 trait fields are null/unknown; used only for the MISSING determination, not as a trait-correctness claim.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> The answer&#x27;s evidence_registry is empty and every evidence_id is null. All D5 claim groups are MISSING_SOURCE, so important conclusions have almost no locatable delivered basis. This is the 1-2 band; 1 is chosen because there is no delivered source record at all. No verified mis-citation exists, so no D5 cap is triggered.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 为空数组，全部 step 的 reaction_evidence_id/trait_evidence_id/enzyme.evidence_id/microorganism.evidence_id 均为 null，仅给酶名、基因名(CouA–E)与菌名而无任何可定位条目。所有claim组来源状态=MISSING_SOURCE（P34：缺失非误导，默认不cap），按D5低分档‘几乎无法定位重要结论依据’取2；无已核实错引，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows the answer delivered no source records and no evidence mapping; used for D5 source-status determination.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> The answer labels enzyme/microorganism confidence low and all traits unknown, which is honest at a generic level. However it does not distinguish observation from prediction, does not discuss limitations or evidence gaps, and route_summary is stated without qualification. This fits the 5-6 band; 6 is chosen because confidence labels are consistently cautious but disclosure remains too generic.

<details><summary>V0.4理由与本行变化背景</summary>

各步 enzyme/microorganism confidence 一律 low、性状一律 unknown，未把预测/推断包装成观测（诚实，无系统性过度确信）；但 uncertainties 为空、无证据性质区分、未说明主要限制、矛盾与待验证点（如菌株级编号、S2 EC、S5电子供体均未标注为待核），仅靠统一低标签、过于笼统。按5-6档‘有不确定性说明但过于笼统’取5。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.confidence_fields：Shows low/unknown confidence labels and absence of detailed evidence-type or limitation discussion; used for D6 calibration only.

</details>

## Kimi

答案SHA256：`db5de8abed5724da60e1d341b319955e84b2147c1b23b66282a15a3a3ea61e31`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分9 → V0.5新分4，变化-5。

新裁判理由：

> 输出模块齐全、JSON可解析，路线名与厌氧条件原样，但必答主链有一处侧链中间步缺失/合并，且入口表示/立体边界与gold不符；只覆盖到部分必要路径内容，故在D1允许范围&#91;1,4&#93;取4。

<details><summary>V0.4理由与本行变化背景</summary>

六个步骤、3个去重菌profile、每profile15项性状、evidence_registry与uncertainties均交付；route_scope原样填写anaerobic与题面路线名。扣分点：S6越出gold终点benzoyl-CoA仍列入主链；部分可查性状留null；但无核心模块缺失，格式完整。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_105：支持本案为ordered_step_count=6的线性主链任务；不证明答案每步正确。
- ANSWER_TEXT / ANSWER.steps：显示答案实际交付6步、3个菌profile及15项性状；不证明化学正确。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 主链从4-香豆酸活化到苯甲酰-CoA基本化学方向成立；侧链一步用HCHL将水合/裂合净反应合并，缺3S-(4-羟基苯基)-3-羟基丙酰-CoA中间体；入口立体/表示与gold S04不一致；辅因子多处省略属局部。按D2允许范围&#91;1,5&#93;取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学骨架成立：S1 CoA活化、S2 HCHL净裂合生成4-羟基苯甲醛+乙酰-CoA、S3醛氧化、S4 CoA活化、S5还原脱羟、S6脱芳构化均属已知厌氧芳香族代谢转化。与gold比，S2把水合/裂合两步合并为一步净反应，S6越出gold终点benzoyl-CoA；S3/S5/S6辅因子或电子供体未列全，属局部计量/简化，不改变主结论。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：支持gold主链各步底物/产物、顺序及S04立体表示；不证明答案缺失中间体仍等价。
- ANSWER_TEXT / ANSWER.steps：用于核对答案主链方向、步骤连接和物质流；不证明来源支持。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> 已确认S04入口目标反应失败（KEY_ENTRY，D-KEY4 cap≤4），S06侧链中间步未交付，其余多步自动对齐/表示待核；可见局部酶-反应信息支持少量目标，但主功能因KEY失败严重受损，取3且不超过4。

<details><summary>V0.4理由与本行变化背景</summary>

关键步骤酶名/EC大体匹配：S1 6.2.1.12、S3 1.2.1.64（gold多注之一）、S4 6.2.1.27、S6 1.3.7.8；S2 4.2.1.101为HCHL合理具体号但gold未观察EC；S5 1.3.7.9与gold 1.1.7.1存在版本/分类差异，E0无法核，不判错。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：列出各gold步可接受的酶名/EC；不能证明答案EC在同一具体反应中已核。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：支持S04入口、S06侧链中间步及S05裂合步的方向；不证明答案合并步骤可替代必答步。
- ANSWER_TEXT / ANSWER.steps：用于核对答案实际酶/EC交付；不证明其已获accepted支持。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 给出了步骤级菌株且R. palustris CGA009、T. aromatica K172等与gold物种/代表记录方向相容；R. capsulatus B100用于前段缺可核反应级证据，部分TaxID/菌株身份只能待核。按D3b部分支持、关键身份未充分核验取5。

<details><summary>V0.4理由与本行变化背景</summary>

身份层面：R. palustris CGA009、T. aromatica K172与gold代表菌一致或兼容；R. capsulatus B100为真实菌株但不在gold步级代表菌中，S1-S3三步反应能力无步级证据，属多处未充分核验。答案未把单步菌写成全路径菌，且明确各步代表菌不同。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_105：支持gold各步的物种级微生物对应及部分菌株/基因组字段；不证明答案另列R. capsulatus B100或所有菌株级声称。
- ANSWER_TEXT / ANSWER.organism_profiles：用于核对答案微生物名、菌株和TaxID交付；不证明身份已验证。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项均结构出现，多项null如实；可核物种代表性状中温度偏好、运动、革兰氏、产孢、部分基因组/培养物与gold相容。但许多性状依赖内部知识或物种代表记录外推，T. aromatica形态/保藏和R. palustris氧/降解表述存在不确定，故部分可用需实质核验，取5。

<details><summary>V0.4理由与本行变化背景</summary>

R. palustris CGA009与T. aromatica K172多数性状与gold观测/预测相符（温度、运动性、革兰氏、产孢、硝酸盐呼吸、基因组等），但R. capsulatus B100的F7/F8/F9（4-香豆酸/芳香族利用、HCHL活性）无gold或条目支持，属关键性状证据不足；T. aromatica F5 DSM 6984与gold物种级DSM 14805不一致待核；R. palustris F4/F3、T. aromatica F14留null。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_105：提供T. aromatica、R. palustris等观察/预测性状和培养物、基因组字段；不覆盖R. capsulatus B100，也不证明答案所有推断。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_105：标明各性状/子字段是否可作观察准确度评价；用于避免将不可评子字段当确定错。
- ANSWER_TEXT / ANSWER.organism_profiles：用于核对答案性状值、null及confidence；不证明其来源正确。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 路线/酶/菌株步骤附有EVID_001-003 pathway/PubMed定位，部分基因组/保藏有EVID_004-005；但核心数据库条目无record_id且E0证据缺口无法核验，性状多数EVID_006内部知识，故部分关键结论可定位、其他模块缺映射，取5。无已核实错引故不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案有evidence_registry并逐step/逐trait映射，但E0为EVIDENCE_GAP，所有引用-声称链不能核实；EVID_001仅MetaCyc pathway名无record_id（GENERIC），性状大量EVID_006内部知识（MISSING），EVID_002/003/004/005有题录或登录号但未随E0原文（UNRESOLVED）。无经冻结证据核实的错引，不cap；按部分关键结论可定位、其他模块缺映射给6分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示答案实际交付的来源类型、locator和claim_scope；不证明数据库条目存在或支持内容。
- ANSWER_TEXT / ANSWER.steps：显示各步骤如何引用来源；不证明引用内容已核。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案有uncertainties、confidence和null，明确S3酶、代表菌、TaxID、内部知识性状的不确定；但仍把部分内部知识性状标medium、把净反应合并后以较确定方式表述，证据强度局部超过可核依据，属单点/多处过度确信而非系统性误导，取6。

<details><summary>V0.4理由与本行变化背景</summary>

答案逐字段给confidence并列出4条uncertainties：S3酶/辅因子不确定、步-菌绑定为代表性菌株、缺TaxID、部分性状来自内部知识；未把预测系统写成实验实证，替代分支明确标为非主链。扣分：EVID_001/003的引用支持范围未披露可疑，部分medium标签仍高于可核程度。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案披露了S3酶、代表菌、TaxID和内部知识性状的不确定性；不证明披露是否完全相称。
- ANSWER_TEXT / ANSWER.evidence_registry：显示部分性状被标为内部知识来源；用于判断D6披露质量。

</details>

## Qwen

答案SHA256：`05546c7d9da2793fa179ec64eeba55901636f2755c4f6163b9055041ceb2156f`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 题面指定6步主链至benzoyl-CoA；答案仅交付S1-S4四步，止于4-hydroxybenzoate，缺4-hydroxybenzoate→4-hydroxybenzoyl-CoA及4-hydroxybenzoyl-CoA→benzoyl-CoA两步，包括末端关键步。路线名与厌氧条件正确，已交付步骤均有底物/产物/酶/菌对应，15项性状字段齐全但若干为null。属主要模块均有涉及但若干必要内容遗漏，5分。

<details><summary>V0.4理由与本行变化背景</summary>

主要模块均有涉及：4步逐步给出底物/产物/SMILES、每步酶与菌，路线名与厌氧条件原样符合题面；15项性状10项填值、5项诚实null；证据登记表与不确定性齐备。但主链仅覆盖gold六步中的前四步，缺4-羟基苯甲酸→4-羟基苯甲酰CoA→苯甲酰辅酶A(J01/J03)两步，5/15性状为未知，属&#x27;若干必要内容遗漏&#x27;，落5–6档取高。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：指定route name与anaerobic条件，并要求15项性状；支持任务符合度判断
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_105：ordered_step_count=6、LINEAR_UNIQUE；支持该题主链必要步数为6，不作为额外旁支分母
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_105：terminal_compound_names=benzoyl-CoA(4-)；支持路线终点身份
- ANSWER_TEXT / ANSWER_TEXT：答案实际只有S1-S4且route_summary止于4-hydroxybenzoate；traits十五字段存在但有若干null

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 已给出的S1-S4四步化学上连续且方向正确：CoA连接、双键水合、逆羟醛裂解、醛氧化；辅因子与副产物（AMP/PPi、NADH/H+）基本合理，S2未注明3S立体化学属局部小缺陷。缺失的末端两步归D1完整性，不在D2按同一遗漏重复降科学分；本请求D2 9-10门未开，取7-8档上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

所给四步化学与gold线性前四步一一吻合：S1 CoA连接(S04)、S2水合(S06)、S3逆羟醛裂解(S05)、S4醛氧化(S02)；方向、结构合理，逆羟醛C9=7+2守恒、醛氧化NAD+/H2O配平。主链止于4-羟基苯甲酸未延至gold终点苯甲酰辅酶A，属完整性缺口(主要在D1)而非化学错误，落7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：S1-S4的化学转化、方向、辅因子及连续连接；S2立体化学未注明
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：gold给出六步反应顺序与终点benzoyl-CoA，支持S1-S4对应S04/S06/S05/S02及末端缺失比较；不证书答案酶的特异性或实验活性
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_105：支持指定路线终点为benzoyl-CoA(4-)；用于说明答案止于中间体

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 按C03：S04入口4-coumarate→4-coumaroyl-CoA的酶名/EC 6.2.1.12与accepted集合一致，记S；S02醛氧化用EC 1.2.1.3，不在accepted vanillin dehydrogenase 1.2.1.64/67/96内；S06/S05给EC 4.2.1.17或泛名hydratase/aldolase，accepted为4-coumaroyl-CoA hydratase/aldolase或feruloyl-CoA hydratase/lyase且EC NOT_OBSERVED，记U；S01 4-hydroxybenzoate-CoA ligase与S03 4-hydroxybenzoyl-CoA reductase无交付，记M。C=S/N=1/6≈0.17落入&#91;1,2&#93;；核心末端缺失且多数目标支持未核，取2（入口一步可核为相对1的改善）。

<details><summary>V0.4理由与本行变化背景</summary>

S1 4-coumarate-CoA ligase EC 6.2.1.12 与gold S04精确一致；S3 4-coumaroyl-CoA hydratase/aldolase（EC null，诚实）与gold S05/S06双功能酶一致；S2 enoyl-CoA hydratase EC 4.2.1.17 为该双功能酶水合半反应的家族级近似(gold EC NOT_OBSERVED)；S4 aldehyde dehydrogenase EC 1.2.1.3 与gold vanillin dehydrogenase(1.2.1.67)同反应类型但异号。2步需具体核验，落5–6档取高。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：答案酶名/EC：S1 6.2.1.12、S2 4.2.1.17、S3 EC null、S4 1.2.1.3；无4-hydroxybenzoate-CoA ligase和4-hydroxybenzoyl-CoA reductase
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：支持accepted酶集合：S04接受4-coumarate-CoA ligase EC 6.2.1.12；S02接受vanillin dehydrogenase EC 1.2.1.64/67/96；S05/S06接受4-coumaroyl-CoA hydratase/aldolase或feruloyl-CoA hydratase/lyase且EC NOT_OBSERVED；仅为策展粒度，不证明具体蛋白实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：支持六步必答目标及末端benzoyl-CoA；用于判定S01/S03未交付
- RUBRIC_CLAUSE / C04：C&lt;0.20→&#91;1,2&#93;的分带依据；局部U不自动整维NE

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 微生物身份为Rhodopseudomonas palustris CGA009；gold organism_gold在物种级R. palustris支持S01/S03/S04/S05/S06多数步，但CGA009菌株级TaxID 258594及S02步归属无E0条目级核验，物种级不能自动外推菌株级。落5–6档，取6因物种候选合理、部分步骤有物种级支持。

<details><summary>V0.4理由与本行变化背景</summary>

选用Rhodopseudomonas palustris CGA009；gold organism_gold以物种级taxid 1076将R. palustris列为S01/S03/S04/S05/S06催化菌，且PATHWAY_COMPLETE=TRUE支持其为完整路径菌；S4醛氧化在gold归Sphingomonas，但R. palustris为全路径菌、物种级可达。菌株CGA009与TaxID 258594在E0无冻结记录(GAP-044/045)，UNRESOLVED待核、不判错，落7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_105：显示gold物种级R. palustris及Sphingomonas等步级归属；不证明CGA009菌株级能力或S02由CGA009完成。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_105：显示gold完整路径能力记录为物种级；不自动替代菌株级身份与能力证据。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 15项均出现，10项有值、5项明确null；运动、杆状、革兰氏阴性、不产孢等与gold观测一致；F14 NC_005296/5459213/64.8与CGA009特定基因组待E0核验；F1‘兼性厌氧’与gold aerotolerant/ facultative anaerobe预测不完全一致，属档内扣。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状与gold物种级代表记录(taxid1076)一致者：F10运动=true、F11杆状、F12革兰氏阴性、F13不产孢；F14 5.46Mb/GC64.8%落在物种观测区间(2.79–6.12Mb；64.1–66.2%)内；F7/F8/F9由所引通路记录支撑；F1&#x27;可厌氧光合生长&#x27;与光养特性及gold aerotolerant=true相符。5项未知为诚实null不计错。关键项来源偏弱、F14 accession不可核，落7档而非更高。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_105：显示R. palustris物种级观测/预测性状；不证明CGA009菌株级全部数值或F1表述完全一致。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_105：显示各性状/子字段可评分角色；不把预测背景值变成观测确认。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> EVID_001为MetaCyc pathway级定位但record_id=null且未逐步映射；EVID_002有NC_005296但E0无法核验；EVID_003为INTERNAL_KNOWLEDGE_ONLY覆盖多个性状。核心组有部分可定位来源、多个具体映射/性状来源缺失；无已核实错引，不cap；落5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组(CG01/02/03/05/07)仅由EVID_001 MetaCyc通路名(无record_id)与EVID_002 NCBI基因组号(E0无记录)等笼统/待核来源支撑；生理形态性状仅INTERNAL_KNOWLEDGE_ONLY(=MISSING_SOURCE)；无经核实的条目级可定位可核对结论，落3–4档取4。EVIDENCE_GAP下查不到一律UNRESOLVED，未判虚构、无已核实错引，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案实际交付的EVID_001–003、claim_scope与record_id；不证明这些来源内容真实或支持逐条声称。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案用confidence high/medium/low/unknown，未知项null，uncertainties列出替代路线和缺失SMILES；EVID_003标INTERNAL_KNOWLEDGE_ONLY，未把预测普遍写成实测；主要限制有说明。少量未把末端缺步明确标为范围限制，档内取8。

<details><summary>V0.4理由与本行变化背景</summary>

明确区分来源类型(DATABASE_DIRECT vs INTERNAL_KNOWLEDGE_ONLY)、逐项confidence、诚实null；uncertainties显式披露厌氧还原路线替代(3-(4-羟苯基)丙酸→β-氧化)并声明本题不采用；辅酶SMILES缺省有说明；下游延续另列。不足：F14 genome以high confidence包装不可核accession(单点过度确信，档内扣)，主链止步未作为范围限制显式声明。落7档。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案对证据性质、未知与置信度的标注；不核验所述科学事实为真。

</details>

## Grok

答案SHA256：`4943c5cbddbc3e854cdac4f83a0f3defdfbe0da7697b2e66faff31ae48b63dee`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所有主要模块均有交付（路径、酶、微生物、15项性状、来源与不确定性），但答案自选β-氧化式主链并明确排除冻结参考中的水合酶/裂解酶主链，且必答6步中S01/S02未按目标链交付。按D1任务路线偏离与完整性缺陷，取&#91;1,4&#93;上沿4。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_105_question：题面要求原样填写指定路线名与厌氧条件，并要求给出主链、每步酶/EC与微生物。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：冻结主链为S04→S06→S05→S02→S01→S03，不是答案S1-S5的β-氧化式主链；支持任务路线偏离判定。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_105：该case为LINEAR_UNIQUE、6个必答步，支持完整性分母为6而非全DAG旁支。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出的β-氧化式化学连续且基本可成立：CoA活化、水合、NAD+依赖脱氢、硫解、还原性脱羟基均有主产物对应，氧化还原与碳流大致闭合。但该主链与冻结参考的中间体序列不同，且S2立体化学、S3/S5辅因子SMILES不完整，故在允许&#91;1,5&#93;内取5而非更高。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：提供冻结主链的转化和方向；用于对照答案β-氧化式序列，不把替代路线回填为D3a目标完成。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：列出冻结步骤的酶/EC背景；不自动证明答案任意具体蛋白底物谱或实验活性。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按C03/C04逐目标核对：6个必答目标中，S01（4-hydroxybenzoate→4-hydroxybenzoyl-CoA）与S02（4-hydroxybenzaldehyde→4-hydroxybenzoate）在答案中无对应底物/产物及酶，登记M；S05目标为3S-(4-hydroxyphenyl)-3-hydroxy-propanoyl-CoA→4-hydroxybenzaldehyde+acetyl-CoA，答案S3改为脱氢生成3-oxo中间体，属另一目标反应，登记F；S06目标为(E)-4-coumaroyl-CoA→3S-羟基中间体，答案S2为同一水合类型但未给指定立体化学且被程序判为STEREO_CONFLICT_SPECIFIED，按已定路线状态登记F。S03、S04因电荷/表示等价与名—EC配对待核，登记U，不自动当S或F。故S=0，C=0，落入C04的&#91;1,2&#93;；答案仍含局部可用信息（入口4-coumarate-CoA连接酶与终点4-hydroxybenzoyl-CoA还原酶名称分别接近accepted集合），但核心目标主链因2个缺失、2个替代/立体冲突而不成立，取2而非1；U不将本维整体转NE。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：提供本题6个必答步骤的accepted酶名与EC集合；只支持目标反应的功能/编号对应范围，不证明答案具体蛋白活性或整条路线成立。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：提供各必答步的主底物、主产物、方向与顺序；用于核对S01/S02未交付及S05/S06为替代反应/立体冲突。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_105：记录本题ordered_step_count=6、LINEAR_UNIQUE；只支持必答目标数为6的全图材料，不作为所有旁支必答分母。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_105：题面路线名为4-coumarate degradation (anaerobic)，终点为benzoyl-CoA(4-)；支持本题评分主链的路线范围与终点核对。
- ANSWER_TEXT / 4943c5cbddbc3e854cdac4f83a0f3defdfbe0da7697b2e66faff31ae48b63dee：答案steps S1-S5的底物/产物、酶名与EC；支持S1/S5局部对应定位，以及S2/S3/S4替代反应和S01/S02中间体缺失定位。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案核心微生物为Rhodopseudomonas palustris CGA009；gold对R. palustris物种级身份及PATHWAY_COMPLETE有支持，多个步骤也有R. palustris记录。菌株级TaxID 258594与每步菌株特异性能力未被E0独立核验，属粒度不足/档内扣，不构成无关类群或整条推荐被推翻，故取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_105：支持R. palustris物种级身份及PATHWAY_COMPLETE；不直接支持CGA009菌株级TaxID 258594或ATCC BAA-98。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：显示部分步骤可由R. palustris来源酶支持；不自动把单步支持扩展为所有菌株特异性能力。

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 多项定性性状与gold物种级观测一致：杆状、革兰氏阴性、运动、不产孢、非嗜盐、中温偏好；F1氧耐受写“兼性厌氧”与gold aerotolerant/facultative预测不完全一致，F5 ATCC BAA-98、F14 NC_005296.1等菌株级标识未核验。主要性状仍可用，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_105：提供R. palustris物种级观测/预测性状；支持部分定性性状，不直接核验CGA009菌株级ATCC或RefSeq。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_105：标明哪些性状子字段scoreable及哪些仅completeness；用于区分观测准确性与缺失。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的evidence_registry全部为INTERNAL_KNOWLEDGE_ONLY；虽然给出EC号、TaxID、ATCC、RefSeq等定位串，但没有可核对的文献/数据库条目或生成记录，按D5六状态均落MISSING_SOURCE。决策相关组无条目级可核对来源，取1–2档中的2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示全部证据均为INTERNAL_KNOWLEDGE_ONLY；不构成可定位外部来源。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_105：仅提供case背景；不替代答案应交付的来源记录。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案有专门uncertainties段，明确说明EC采用通用类、温度/pH/盐度/基因组数值缺源填null、SMILES与电荷/立体化学限制、Taxonomy/ATCC/RefSeq来自既有知识而非实时检索；多数未知被诚实标注。但部分性状仍以high confidence+INTERNAL_KNOWLEDGE_ONLY给出，未逐项降级，故未进8以上。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：提供答案自身的限制与未知披露；用于D6证据性质与边界评价。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_105：显示部分性状仅有completeness或预测背景，不能当作观测实证；用于检查答案是否区分证据性质。

</details>

## GPT5.6

答案SHA256：`6942327f794604673092093f39a3588b2795525e4fca111662b71fa11cc46c98`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案有 route_scope、3 个步骤、1 个菌株 profile、15 项性状字段及证据登记，但只给出 3 步且未到题面/gold 终点 benzoyl-CoA；S2/S3 为另一路线，缺关键终端步骤，属多处缺步骤、任务链不完整。按 1–2 与 3–4 档界，取 3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：给出 gold 主链反应与 benzoyl-CoA 终点；只用于任务完整性对照，不证明答案全部内容。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_105：给出路线名、起点和终点身份；不证明被测答案已交付完整主链。

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1 的 4-coumarate CoA 活化化学与方向可成立；S2 的还原性侧链转化可作为替代思路但与 gold 主链不同；S3 将 4-hydroxyphenylpropionyl-CoA 写成 4-hydroxyphenylacetyl-CoA + acetyl-CoA，碳数不守恒，且 enoyl-CoA hydratase 不能承担硫解性缩短；到 benzoyl-CoA 的连续性断裂。属多个重要步骤错误/连接需修订，取 3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps.S3：显示 S3 底物/产物与所列酶；用于核对化学计量和酶功能，不作为外部实验证明。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：显示 gold 主链的 4-coumaroyl-CoA 水合/裂解与后续转化；不覆盖答案自设还原路线。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按目标反应读答案：S1 的 4-coumarate CoA 活化与 gold 入口 S04 accepted EC 6.2.1.12 化学相近，但程序路线绑定仍为 BOUNDARY_REVIEW；S2 产物是 4-hydroxyphenylpropionyl-CoA，不是 gold S06 的 3-hydroxy 中间体；S3 也非 gold S05；S01/S02/S03/S05/S06 的目标反应未交付，终端缺失。即使给入口 1 个 S，S/N≤1/6&lt;0.20，落 &#91;1,2&#93;，且核心主链失效，取 2。KEY 终端缺失可触发上界，但本分已低于上界；无独立 key_error=Y。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_105：给出 gold 各目标反应、方向与终端；用于逐目标核对，不证明答案替代路线正确。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_105：给出各 gold 步 accepted 酶名/EC 的参考粒度；不证明具体蛋白底物谱或菌株活性。
- ANSWER_TEXT / ANSWER.steps：显示答案实际声称的底物、产物、酶与 EC；只作被测文本，不作外部证据。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Rhodopseudomonas palustris CGA009 的身份在物种层面合理，gold 也支持 R. palustris 对该路线为 PATHWAY_COMPLETE，且 S1 对应步骤有 R. palustris 记录；但答案未给 TaxID，CGA009 的菌株级身份及 S2/S3/整条替代路线的能力无对应证据，complete_pathway_organism_profile_id 的声称超出已核粒度。属合理候选加部分支持、关键作用范围未核，取 5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_105：提供 gold 步骤菌归属及 R. palustris PATHWAY_COMPLETE 的物种级支持；不支持 CGA009 菌株级全部特性或答案替代路线。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_105：给出本题为 LINEAR_UNIQUE 任务框架；不证明菌株级能力。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15 项字段齐全但仅 5 项有值，10 项明确 unknown；已填 F1/F6/F7/F8/F9 属概括性、低置信描述，部分与 R. palustris 厌氧芳香族代谢背景相容，但 F1 的“兼性厌氧”表述不精确，温度/pH/盐度/保藏号/基因组等关键数值项均缺，且没有可定位来源。按部分性状可用、关键证据不足，取 5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_105：提供 R. palustris 物种级 observed/predicted 性状参照；不等于 CGA009 菌株级全部性状，也不回填答案缺失来源。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_105：标明哪些性状子字段可评分/仅完整性；不直接给答案加减分。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部步骤、菌和性状只指向 EVID_001，且 EVID_001 的 source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 均为 null；claim_scope 只是宽泛内部知识描述。没有可定位、可核对的来源，属 MISSING_SOURCE，D5 低档；未发现经核实的错引，故不触发错引 cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示唯一来源为 INTERNAL_KNOWLEDGE_ONLY，且无数据库条目/定位；只用于来源可追溯性评价。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案多处使用 low/unknown，明确填写 uncertainties，逐步 uncertainty 说明 EC 未定、菌株证据有限、SMILES/性状未知；主要限制与待验证点已披露。但 complete_pathway_organism_profile_id 与部分 F7/F8/F9 概括性结论仍以低置信呈现，证据类型与适用边界没有完全展开，故未到 9–10，取 7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案主动列出的未知和限制；不证明其科学内容本身正确。

</details>
