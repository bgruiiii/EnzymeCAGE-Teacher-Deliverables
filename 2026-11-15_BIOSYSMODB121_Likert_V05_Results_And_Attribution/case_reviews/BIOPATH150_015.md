# BIOPATH150_015：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：Orcinol degradation pathway

污染物：Orcinol；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 48.5 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 22.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 56 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 44.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 73 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 26 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`23c9d8783501d9e4ab2738a0cfe411d7ca3b0c9a9ec85eedb6b6a4f241778a77`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 模块层面覆盖路径、酶、微生物、15项性状与不确定性，但主链任务只交付S1入口对齐；S2改线，S3/S4目标步与acetate/pyruvate终点未交付。按D1任务偏离/完整性cap≤4，档内取4因各模块可读且关联基本清楚。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8（大部分必要内容完整、关联清楚、仅少量遗漏）：题面给定路线名原样回填、氧条件aerobic一致；3步主链每步给出主底物/主产物英文名与SMILES、一个首选酶（含EC或诚实null）、一个对应菌；organism_profiles按物种+菌株去重为单一ORG_001并由step引用；15项性状全部按统一外壳返回（F5/F14诚实null）；evidence_registry与uncertainties齐备。未达9–10之处：S2无EC、主链止于2-甲基-4-氧代己二酸而把后续转化放入非评分downstream_continuation字段、F5保藏号与F14基因组留null（属完成度而非科学错误）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面锁定Orcinol degradation pathway与aerobic条件；题面要求逐步给出主底物/产物、酶与微生物。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：冻结主链为S01–S04并至acetate/pyruvate；不支持答案在S02改线并省略S03/S04目标步。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> S1好氧羟基化与S1底物/产物一致，辅因子与计量基本合理；S2–S3为可自洽但无来源的甲基氢醌醇/马来酰乙酸类似途径，且未落至acetate/pyruvate终点。主干部分成立，但关键中间体、连接与终点需实质修订，按5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（主干部分成立，关键中间体与连接仍需修订，合理性证据有限）：S1与参考首步化学一致——orcinol(Cc1cc(O)cc(O)c1)+O2+NADH→2,3,5-三羟基甲苯(Cc1c(O)c(O)cc(O)c1)+H2O+NAD+，含辅因子且计量自洽；S2底物正确、开环反应类型正确（邻位二醇内向开环），但产物写作2-甲基马来酰乙酸，与参考S02产物2,4,6-三氧代庚酸为同分子式构造异构体；S3把参考的‘三氧代庚酸水解酶水解’改为‘马来酰乙酸还原酶还原’，产物2-甲基-4-氧代己二酸为β-酮己二酸类似物，主链未走到参考末端（乙酰丙酮酸→丙酮酸+乙酸），末端归属被放进非评分downstream/central字段。答案自述全链为间苯二酚途径类比与化学推导、无外部证据，按四.5第3步属‘未证实’：不自动判错、也不给高分，故档内取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：支持S01底物/产物与冻结路径一致；S02–S04显示参考主链连接与终点，不支持把答案替代路线当作同一冻结目标反应。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> S01结构匹配但酶/EC未获accepted支持（U）；S02为已确认KEY目标反应失败，产物改为2-methylmaleylacetate而非2,4,6-trioxoheptanoate；S03/S04目标步未确认。无S信用，KEY4上界4，档内取2：仅有入口局部信息，主催化链不可用。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（有合理候选和部分支持，但关键步骤仍缺具体核验）：三步酶-反应类型配对内部自洽（单加氧酶↔羟化、双加氧酶↔开环、还原酶↔C=C还原）；S1酶名orcinol 2-monooxygenase与参考‘orcinol hydroxylase’功能一致，S2酶名与参考‘2,3,5-trihydroxytoluene-1,2-oxygenase’一致（EC诚实null）。但S1所给EC 1.14.13.42与参考EC 1.14.13.6冲突且冻结证据无该EC条目（GAP-015-001），S3所给EC 1.3.1.32亦无冻结记录（GAP-015-004）；全部酶均无外部支持。按四.5保守条款：冲突无法核验→UNRESOLVED、保留低分与待核标记，不cap，档内取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：冻结S01 accepted为orcinol hydroxylase/1.14.13.6；不支持答案EC 1.14.13.42或S03 maleylacetate reductase作为目标S03酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：冻结S02产物为2,4,6-trioxoheptanoate；不支持答案S02产物2-methylmaleylacetate作为本题目标反应产物。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案使用Pseudomonas putida/TaxID 303，物种身份与E0 taxid 303名称匹配；organism_gold有P. putida TaxID 303 pathway_complete TRUE。未给菌株，S03目标菌Terrabacter sp. DBF63未覆盖，但整菌推荐在物种级仍成立；按7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6、档内取6（有合理候选和部分支持，若干身份与作用范围未充分核验）：身份层面Pseudomonas putida / TaxID 303 经E0分类记录核实为学名匹配（SUPPORTED），菌株字段诚实null、与种级声称粒度一致；S1/S2步级归属与参考一致，参考亦将taxid 303列为该pathway的PATHWAY_COMPLETE菌（正支持登记于事实层，不回填为来源）。未充分核验之处：全部步归属仅凭内部知识、无条目来源；S3步归属与参考S03的Terrabacter sp. DBF63（参考侧organism_match_status=UNRESOLVED）不同；整条路径能力为物种级推断（E0标注L3 UNRESOLVED）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：官方分类记录支持TaxID 303对应Pseudomonas putida物种名；不核实具体菌株或降解能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_015：显示S01/S02/S04为P. putida、S03为Terrabacter sp. DBF63，且P. putida TaxID 303有PATHWAY_COMPLETE TRUE；仅物种级。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> P. putida物种级多个性状与gold观察一致（运动、杆状、革兰氏阴性、不产孢、好氧呼吸等）；但F3 pH max 8.5与gold 8不符，F4数值min/max缺，F5 CCUG 49576与F14基因组均null，F9路径酶活未经支持。部分准确且适用，但关键项证据/数值需修订，取6。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6、档内取6（部分性状准确且适用，但关键项证据不足或条件解释需修订）：多数定性性状与参考观测方向一致（F6好氧呼吸/O2为末端受体、F8含酚类芳香族降解、F10运动性阳性、F11杆状、F12革兰氏阴性、F13不产芽孢）；但F1写作‘专性好氧，需分子氧’与参考观测aerotolerant=true类别不符；F2给出min 4/opt 30/max 40，与参考观测区间不完全一致且端点属pending_teacher_adjudication不可评；F3上限8.5对参考8.0略高；F7苔黑酚/间苯二酚利用与F9路径酶活属未核外推；F5保藏号与F14基因组参考有记录而答案诚实留null（完成度问题归D1，不在此重复重扣）。答案已自述全部性状为物种级通用值、非菌株实测，符合四.4同物种代表记录口径，故不因菌株未定判错。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_015：提供P. putida TaxID 303的观察性状与预测背景；支持运动、杆状、G−、不产孢等，显示pH max=8、保藏号CCUG 49576、基因组GCA_024508115.1等。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_015：标记F2 min/max、F4 max为pending_teacher_adjudication；F3 min=5、max=8为scoreable；不把pending子域当已核实正确或错误。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> D5按claim group登记：路线、酶-EC、微生物步级归属、性状等决策相关组均仅有INTERNAL_KNOWLEDGE_ONLY/局部标签，属MISSING_SOURCE低分档；无已核实错引，不触发cap。可定位来源几乎缺失，取2。

<details><summary>V0.4理由与本行变化背景</summary>

1–2档（几乎无法定位重要结论依据）：evidence_registry三条（EVID_001/002/003）全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，路径步骤、酶-EC、菌归属与15项性状均无可定位条目或计算记录；按四.3属MISSING_SOURCE（仅有自我声明），决策相关组（CG01/CG02/CG03/CG05/CG07/CG04/CG10/CG14）全部缺失→低分档、默认不触发cap；答案未编造任何外部引用并逐条给出claim_scope与low置信度，属缺失而非误导，故取低分档上限2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：答案自述全部证据为内部知识，evidence_registry无DOI、数据库条目或计算记录；仅支持来源缺失判断，不证明科学结论错误。

</details>

### D6 不确定性与诚实度：9 / SCORED

V0.4旧分7 → V0.5新分9，变化+2。

新裁判理由：

> 答案明确全部证据为内部知识，置信度多low/medium，并逐项披露EC、菌株、产物命名、羟基化位点与替代支路不确定性；未把预测冒充观测，主要限制与冲突说明充分。按9–10档取9。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8（大部分观测/预测/未知被正确标注，主要限制与冲突已说明）：uncertainties逐条列出EC记忆性、S2酶命名与EC不确定、S3产物命名属化学推导、首步羟化位点由类比推导，并把备选C4羟基化支路明确标注is_part_of_scored_main_route=false；各字段confidence（low/medium/unknown）与内部知识来源基本相称，F5/F14以unknown/null诚实留空；并主动披露性状为物种级通用值而非菌株实测。扣分项：‘专性好氧’以medium置信度给出、未披露与观测aerotolerant类别的差异（单点过度确信，非系统性误导），故不cap、档内取7。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：答案原文显示对EC、菌株、产物命名、羟基化位点与内部知识局限的明确披露；支持D6证据边界判断。

</details>

## DeepSeek

答案SHA256：`019212c401c355a325c6380fc3bae31c04497bbd574304373787a917fae1b0bd`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 答案结构完整并回显指定路线名与好氧条件，但实际主链为替代路线：S1/S2与gold非match，S3/S4缺失；15项性状全为null。按P100任务偏离与完整性，D1落3-4档，因覆盖结构尚可但任务主链偏离明显，取3。

<details><summary>V0.4理由与本行变化背景</summary>

路径/酶/微生物三模块均有交付：5 步逐条给出主底物与主产物（S5 产物 SMILES 为 null）、酶名（2/5 给 EC）与对应菌株；但任务要求的 15 项性状全部为 null 占位（填写 0/15、明确未知 15/15），evidence_registry 仅一条全空占位，主链止于开环产物未及终产物。属 5–6 档“主要模块均有涉及，但若干必要内容遗漏、仅占位”，因两个模块实际为占位取低 5 分；化学正确性问题按八.D1/D2 边界条款归 D2，不在 D1 重复扣分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_015：题面锁定Orcinol degradation pathway与aerobic条件。
- ANSWER_TEXT / 019212c401c355a325c6380fc3bae31c04497bbd574304373787a917fae1b0bd：答案给出5步替代路线、每步酶/菌，但15项性状均为null。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_015：gold主链起点Orcinol，终点Acetate|Pyruvate；不支持答案的终止产物。

</details>

### D2 反应化学科学性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D2只看所答化学自身质量。S1 Orcinol(C7H8O2)→2,4-二羟基-6-甲基苯甲醛(C8H8O3)增加一个碳且无说明，违反原子守恒；S3把2,4-二羟基-6-甲基苯甲酸去甲基成2,4-二羟基苯甲酸，标作decarboxylation但失去的不是羧基碳，核心转化不可信。虽有S2/S4局部看似合理，主链核心仍失效，落1-2档，取2。

<details><summary>V0.4理由与本行变化背景</summary>

化学层面主链不成立：S1 标“monooxygenation”却把 orcinol（C7H8O2，Cc1cc(O)cc(O)c1）变为 2,4-dihydroxy-6-methylbenzaldehyde（C8H8O3，O=Cc1c(O)cc(O)cc1C），凭空多出一个碳原子，违反原子守恒且无任何说明；S3 用 orsellinate decarboxylase 把 2,4-dihydroxy-6-methylbenzoic acid（C8H8O4）变为 2,4-dihydroxybenzoic acid（C7H6O4，O=C(O)c1c(O)cc(O)cc1），前后差 C1H2 而非 CO2，脱羧应移除羧基碳而答案丢失的是甲基碳，方向与原子归属错误；S5 产物仅有名称、SMILES 为 null，无法核结构。主链首步即错并伴随多处基本化学约束违反，触发 D2 关键错误（cap≤4）；S2 醛氧化与 S4 羟化的反应类型与计量方向尚可，故在 3–4 档内取 3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 019212c401c355a325c6380fc3bae31c04497bbd574304373787a917fae1b0bd：S1产物SMILES含醛基与甲基，分子式C8H8O3，而底物Orcinol为C7H8O2；S3称decarboxylation但产物保留羧基并失去甲基。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：gold S01为Orcinol→2,3,5-Trihydroxytoluene，S03为2,4,6-Trioxoheptanoate→Acetylpyruvate+Acetate；不支持答案的S1/S3转化。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分4 → V0.5新分1，变化-3。

新裁判理由：

> D3a只计目标反应相应粒度的功能/accepted支持。S01/S02为已确认目标非match；S03/S04未对齐；答案没有任何目标步达到适用功能支持。答案的orcinol 2-monooxygenase/1.14.13.7也不等于accepted orcinol hydroxylase/1.14.13.6。按D-KEY4与&#91;1,4&#93;范围，核心目标几乎无可用对应，取1。

<details><summary>V0.4理由与本行变化背景</summary>

5 步均给酶名，但仅 S1（EC 1.14.13.7）与 S4（EC 1.14.13.8）给 EC，且两条 EC 在本案冻结证据中均无记录（item_gaps GAP-015-002/003/006/007），按四.6 保持 UNRESOLVED——既不判错也不凭号码放行；S2/S3/S5 无 EC、无基因/蛋白标识、无任何来源。酶功能与所称反应的匹配性仅在 S2（醛脱氢酶氧化为酸）、S4（单加氧酶羟化）、S5（开环双加氧酶）方向成立；S1 标 monooxygenation 却交付多一个碳的产物、S3 标脱羧却丢失甲基碳，酶功能不能支持其所称转化。整体属“多处反应与酶不匹配 + 若干关键步骤缺具体核验”的 3–4 档，因部分步骤酶类型合理取 4，不触发已核实关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 019212c401c355a325c6380fc3bae31c04497bbd574304373787a917fae1b0bd：S1给orcinol 2-monooxygenase/1.14.13.7；S2/S3/S5无EC；S4给1.14.13.8；目标步未形成accepted匹配。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：gold S01为Orcinol→2,3,5-Trihydroxytoluene，S02为2,3,5-Trihydroxytoluene→2,4,6-Trioxoheptanoate；答案S01/S02产物不同。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：accepted S01酶为orcinol hydroxylase/1.14.13.6；S02为2,3,5-trihydroxytoluene-1,2-oxygenase/1.13.11.M3；不支持答案S01酶/EC配对。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> D3b分层：P. putida与TaxID 303的物种级身份有官方记录支持，且gold多步使用Pseudomonas putida 303/全路径记录；但答案另加strain ORC，未在taxid 303记录名中出现，菌株级身份未核；把同一ORC profile写成complete_pathway_organism_profile_id，也缺菌株级全路径证据。物种主推荐合理、若干关键菌株与作用范围待核，落5-6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

物种选择有据：Pseudomonas putida + TaxID 303 与冻结分类记录一致（物种级名称匹配 SUPPORTED），且 gold 将 S01/S02/S04 归属于 P. putida（TaxID 303，pathway_complete=TRUE）。但菌株 “ORC” 在冻结记录中查不到：E0 的 BacDive 12880 是菌株 mt-2 PaW1(pWWO)（保藏号 DSM 3931/ATCC 33015 等），不含 ORC token；以物种级 TaxID 支撑菌株级身份属身份阶梯①粒度不足，按条款档内扣分、默认不 cap（不判编造）。同时 5 步全部绑定同一菌株、无任何步级催化或整条路径能力证据或引用，complete_pathway 声称（CG09）在 E0 中为 UNRESOLVED。综合属“有合理候选和部分支持，但若干关键身份或作用范围仍未充分核验”的 5–6 档，取 5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：官方分类记录支持Pseudomonas putida与TaxID 303的物种名关联；不支持ORC菌株身份或全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_015：gold S01/S02/S04及PATHWAY_COMPLETE行支持Pseudomonas putida(TaxID 303/GCA_024508115.1)在gold路线中的物种/参考级关联；不自动支持ORC菌株或替代路线。
- ANSWER_TEXT / 019212c401c355a325c6380fc3bae31c04497bbd574304373787a917fae1b0bd：答案将全部步骤归Pseudomonas putida ORC，TaxID 303，并以ORG_001声明complete_pathway。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 答案的organism_profiles&#91;0&#93;.traits中15项性状全部value=null、confidence=unknown；按P44与四.4，全部必需性状均为null/空值时D4按MISSING记1分，不宣称检测到具体科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

任务要求每个 organism_profile 一次返回全部 15 项性状及各项最强来源；答案的 ORG_001 profile 15 项性状全部为 value=null、raw_text=null、evidence_id=null、confidence=unknown，即未交付任何性状数值、单位、条件或来源。按 P44“全部必需性状均为 null/空值时 D4 记 MISSING=1，不宣称检测到科学错误”处理；该 1 分按共享 totals 合同参与加权总分与科学子分，权重保留。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 019212c401c355a325c6380fc3bae31c04497bbd574304373787a917fae1b0bd：15项性状字段均存在但值全为null，confidence=unknown。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_015：gold含Pseudomonas putida 303的多个可观测性状；答案未交付对应值，不能回填。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> D5只看原交付来源。答案只有EVID_001，source_type=UNKNOWN，database/record_id/locator均null，claim_scope为空；各step的enzyme.evidence_id、reaction_evidence_id、trait evidence_id均为null。核心路线、酶、菌、性状均无可定位来源，属MISSING_SOURCE，低分档取1；无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案未交付任何可定位来源：所有 steps 的 reaction_evidence_id/trait_evidence_id 与 enzyme.evidence_id、microorganism.evidence_id 均为 null；唯一 evidence_registry 条目 EVID_001 的 source_type=UNKNOWN 且 database/record_id/locator 全 null、claim_scope 为空，属完全无引用（连笼统库名都未给）。决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）全部为 MISSING_SOURCE；两条 EC 的编号类声称在冻结证据中查不到（GAP-015-002/003/006/007），另登记 UNRESOLVED_SOURCE 待核，不判虚构、不计已核实错引、不 cap。按“几乎无法定位重要结论依据”的 1–2 档取 2（存在形式上登记但内容全空的证据槽，非零结构）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 019212c401c355a325c6380fc3bae31c04497bbd574304373787a917fae1b0bd：唯一来源条目为UNKNOWN且无定位；所有事实字段未引用可用来源。
- RUBRIC_CLAUSE / P33-P42：D5六状态与claim group来源登记；MISSING_SOURCE为低分档且默认不cap。

</details>

### D6 不确定性与诚实度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 性状全null并标unknown是诚实披露；但route_summary与多步酶/菌以medium/low confidence断言，uncertainties为空，未说明替代路线、菌株身份与证据缺口，主要限制缺失，属多处过度确信，落3-4档取3。

<details><summary>V0.4理由与本行变化背景</summary>

答案只以 confidence 标签表达不确定（15 项性状 unknown、S2/S3/S5 酶 low、其余 medium），uncertainties 为空数组，未写任何限制说明，未区分观测/预测/推断，也未披露 EC 与菌株身份未经核实；同时对一个无任何来源、且在化学上不成立的 5 步路径与“整条路径菌”采用 medium 置信。属“多处过度确信、主要限制未说明”的 3–4 档；因 15 项性状如实填 null、未编造数值，且无系统性把预测写成实证或刻意掩盖矛盾的证据，不构成 D6 关键错误，档内取 4。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 019212c401c355a325c6380fc3bae31c04497bbd574304373787a917fae1b0bd：答案有unknown/low标签，但无uncertainties说明，主路线以medium confidence断言。
- RUBRIC_CLAUSE / P119-P121：D6区分单点过度确信与系统性误导；未核内容标medium且零披露按档内扣分处理。

</details>

## Kimi

答案SHA256：`1140cf56581d8d9e3b7c67a341445eabf8f16994a7df2cdf68fb7590a8a4978d`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 题面要求的路线、逐步酶与微生物、15项性状均属必答内容。答案回显了正确route_scope并交付S1、S2两步及15项性状字段，但指定主链共有4个必答步（S01-S04）且终点为Acetate|Pyruvate；答案仅到开环，S3/S4及终点未交付，S2产物仅为 tentative 通用名且SMILES为null，两个酶的EC均填null而冻结gold列有对应EC。属主要模块均有涉及但若干必要内容遗漏、部分仅占位，符合5-6档；未达到核心模块大部缺失或严重路线偏离的D1关键错误门槛。

<details><summary>V0.4理由与本行变化背景</summary>

档5–6取5：路线名合规，步骤/酶/菌/性状/来源/不确定性六模块均有交付；但主链仅2步（gold含S01–S04四步），缺下游两步，step2产物为占位通用名且smiles=null；性状12项填、3项null。属“主要模块均涉及但若干必要内容遗漏”，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：冻结主链含S01-S04四步；S02产物为2,4,6-Trioxoheptanoate，支持答案只交S1-S2且S2产物未具体化。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_015：本题指定路线终点为Acetate|Pyruvate，支持答案未交付至终点。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：冻结表列出S01/S02接受酶及EC（1.14.13.6；1.13.11.M3），支持答案EC字段缺失；不证明具体蛋白实验活性。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> S1的底物、产物、O2/NADH辅因子与gold S01方向及化学转化一致，连续性到S02成立。S2主底物2,3,5-trihydroxytoluene及O2正确，描述为extradiol型meta开环在反应类型上接近gold S02，但产物仅给“structure tentative”通用名、SMILES为null，未给出gold的2,4,6-trioxoheptanoate，关键中间体身份与原子/计量信息不足；S3/S4未交付，但仅缺步不另按覆盖率硬换D2分，故按现有化学表达评为部分成立、关键中间体仍需修订的5-6档。未见方向反转、首步错误、明显不守恒或无依据跳步，key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

档5–6取6：step1 Orcinol→2,3,5-Trihydroxytoluene与gold S01一致（含O2/NADH底物、H2O/NAD+副产物）；step2间位开环方向与gold S02一致，但环裂解产物未指认结构（smiles=null，未给2,4,6-trioxoheptanoate），主链未至acetate/pyruvate。关键中间体未定，故非7–8档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：S01底物/产物/辅因子与S02底物及期望产物2,4,6-Trioxoheptanoate；支持S1一致、S2产物身份未按gold具体化。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_015：指定路线终点为Acetate|Pyruvate，支持答案化学链未到达题面主链终点。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按N=4计：S1目标反应为CONFIRMED_TARGET/SUPPORTED，答案orcinol hydroxylase与accepted功能匹配，虽EC null仍可按功能级给S；S2为ROUTE_HOLD_REPRESENTATION/UNRESOLVED，答案给generic ring-cleavage dioxygenase但产物身份未定，不能判S或F，记U；S3、S4在答案中无对应步骤，记M，其中S4为KEY_TERMINAL，实证交付缺失触发D-KEY4上限≤4。故S=1、U=1、M=2，C=S/N=0.25落入&#91;3,4&#93;；仅有1个已核目标可用且S2身份待核使可用边界不足以支持该带上沿，取3。无已核催化矛盾，故key_error=N；D-KEY4仅作为受限区间上限，不代签key_error=Y。局部U不阻塞整维评分，但按C08保留未核说明。

<details><summary>V0.4理由与本行变化背景</summary>

档5–6取6：step1 enzyme=orcinol hydroxylase与gold BSY-e00037（EC 1.14.13.6）名实一致；step2环裂解双加氧酶名与gold oxygenase方向一致。但两酶EC均null、S03/S04酶未交付、step2酶confidence=low，属部分支持，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：S01 accepted enzyme orcinol hydroxylase/EC 1.14.13.6；S02 accepted 2,3,5-trihydroxytoluene-1,2-oxygenase/EC 1.13.11.M3；支持S1功能匹配、S2名称对应关系待核且答案未给EC。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：S02期望产物为2,4,6-Trioxoheptanoate；S03/S04为必答后续目标步，支持答案S3/S4缺失及S2产物身份未定。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_015：路线终点为Acetate|Pyruvate，支持S04 KEY_TERMINAL缺失使目标主功能严重受损。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> D3b主要微生物身份可靠：P. putida与taxid303均与gold和E0核对一致，gold PATHWAY_COMPLETE中taxid303为true；但答案无strain、仅S1/S2步级归属，S03/S04微生物对应未交付，S03 gold本身UNRESOLVED，故处7档而非9–10档。

<details><summary>V0.4理由与本行变化背景</summary>

档7–8取8：物种P. putida(TaxID303)经f3e0:taxid:303核实SUPPORTED；步级归属与gold organism_gold S01/S02 EXACT一致；种级PATHWAY_COMPLETE(303)=TRUE支持整条路径能力。菌株null为诚实缺失、未过度外推，故8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_015：S01/S02/S04对应P. putida taxid303；PATHWAY_COMPLETE taxid303为true；不证明具体菌株实验能力。
- E0_EVIDENCE / f3e0:taxid:303：官方分类记录支持Pseudomonas putida/taxid303身份；不证明路径能力或菌株级表型。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 性状多数与gold观察或同物种代表记录相容：motility、rod-shaped、Gram-negative、non-sporulating、mesophilic、pH growth=7.0、phenol degradation等有支持；但F1写成obligate aerobe强于gold的aerotolerant记录，F2 optimum 30°C与F3 optimum 7.0属completeness-only字段，F8扩展至toluene/naphthalene、F15 habitat generalism证据较弱；F5/F14以null诚实缺失。综合落7档，而非9–10。

<details><summary>V0.4理由与本行变化背景</summary>

档7–8取7：motility/rod/gram-negative/sporulation-false/mesophilic/pH=7.0/aerobic respiration等与trait_gold一致；但多数性状来自INTERNAL_KNOWLEDGE_ONLY，F1写“obligate aerobe”而gold记aerotolerant、F5保藏号与F14基因组null（gold有值）属完成度缺口。主要性状可核实且适用，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_015：种级observed/predicted性状；支持motility、rod、Gram-negative、non-sporulating等；不自动支持未列出的toluene/naphthalene。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_015：标注哪些性状值与子字段可评分/仅完整性；不等于对答案值的正确性放行。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_015：F2 optimum_c、F3 optimum等为completeness_only或待师裁；不能当作已观测最适值。
- E0_EVIDENCE / f3e0:bacdive:12880：BacDive 12880为P. putida mt-2 PaW1菌株记录；培养温度26/30°C不是最适值，不核实任意菌株。
- E0_EVIDENCE / f3e0:taxid:303：taxid303物种身份；不支持菌株级性状普适性。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D5为部分关键结论可定位、其他模块来源弱：核心路线有EVID_001具体文献题录，但题录为free text且E0未解析/核验；taxid303有EVID_002并可由E0核对；大量性状依赖EVID_003 INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE；S03/S04终段未交付且无对应来源。无已核实错引，不cap；综合5档。

<details><summary>V0.4理由与本行变化背景</summary>

取5（5–6档下沿）：CG07身份条目级可定位并核对（SUPPORTED），但核心路线/酶仅自由文本文献不可核（UNRESOLVED_SOURCE）、性状多为内部知识（MISSING_SOURCE）；无任何已核实错引→无cap（severity=NOT_APPLICABLE）。因核心结论可追查性弱、多模块缺映射，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：S01/S02参考酶-反应行；不证明答案文献引用的实际支持关系。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：参考反应链用于核对答案声称；不替代EVID_001正文核验。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_015：种级性状参考；用于判断EVID_003覆盖范围，不回填为答案来源。
- E0_EVIDENCE / f3e0:taxid:303：官方taxid303记录；支持身份记录可定位，不证明路径能力或具体性状。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> D6总体诚实：对EC缺失、开环产物结构未定、菌株号未确认、内部知识来源和种级性状限制均有明确说明；低/medium confidence与null使用较克制，未把预测系统性写成实证。局部仅有F1 obligate aerobe等措辞略强，但未形成系统性误导，故8档。

<details><summary>V0.4理由与本行变化背景</summary>

档7–8取8：uncertainties逐条诚实（step2产物未定、菌株/EC未知、性状为种级内部知识低/中置信），区分文献/数据库/内部知识与预测/未知，声明下游不列入评分主链；仅complete_pathway标记与仅2步存在轻微表述张力，故8非9–10。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Qwen

答案SHA256：`4bb6553923e019660f82da840816c2f48cf4607231bd9195a7a7696ff071325f`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 答案给出3步主链、逐步酶和同一菌，15项性状字段均出现（多数为null）；但题面指定Orcinol degradation pathway的冻结主链为4步，答案仅S1与目标入口相符，未交付目标S03/S04及acetate/pyruvate终点，后续中间体走成2-methylmaleylacetate→2-methyl-3-oxoadipate，主链覆盖明显不完整。按D1 5–6档：主要模块均有涉及，但若干必要内容遗漏、终点与部分关联不清。

<details><summary>V0.4理由与本行变化背景</summary>

结构完整：route_scope按题面填&#x27;Orcinol degradation pathway&#x27;，3步均含底物/产物名称、enzyme、microorganism，organism_profile按物种+菌株去重为ORG_001，15项性状全列（10填+5诚实null，filled+unknown=15）。主要缺失：S2产物、S3底物与产物共3处SMILES为null（诚实null但化学SMILES不齐），主链止于2-methyl-3-oxoadipate未达gold末端。覆盖各模块、格式合规，属&#x27;大部分完整、少量遗漏&#x27;档，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_015：冻结formal_cases记录该题ordered_step_count=4、LINEAR_UNIQUE；只说明全图主链材料为4步，不证明答案已交付全部目标步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：冻结4步主链：S01 orcinol→2,3,5-trihydroxytoluene，S02→2,4,6-trioxoheptanoate，S03→acetylpyruvate+acetate，S04→pyruvate+acetate；不证明答案的2-methylmaleylacetate路线。
- ANSWER_TEXT / 4bb6553923e019660f82da840816c2f48cf4607231bd9195a7a7696ff071325f：答案实际只有S1-S3三步，未出现目标S03 trioxoheptanoate hydrolase、S04 acetylpyruvate hydrolase及acetate/pyruvate终点；organism_profiles含15项性状但多项null。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> S1主转化orcinol→2,3,5-trihydroxytoluene与冻结gold一致，但未列O2/NADH等辅因子；S2称2,3,5-trihydroxytoluene经双加氧开环生成2-methylmaleylacetate，与冻结gold的2,4,6-trioxoheptanoate不同且产物SMILES缺失，属关键中间体需修订/待核；S3用maleylacetate reductase EC 1.3.1.32还原到2-methyl-3-oxoadipate，化学上可讲通但未继续到acetate/pyruvate终点。整体主干部分成立，关键中间体、终点连续性和辅因子完整性未充分支持，落5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

S1 orcinol→2,3,5-trihydroxytoluene与gold S01一致，底物/产物SMILES正确；S2酶名&#x27;2,3,5-trihydroxytoluene 1,2-dioxygenase&#x27;与gold S02一致，产物2-methylmaleylacetate与gold 2,4,6-trioxoheptanoate同为C7H8O5、可能互变异构（答案已注明未确认）；但S3以maleylacetate reductase(EC1.3.1.32)还原为2-methyl-3-oxoadipate，与gold S03水解酶(trioxoheptanoate hydrolase)→acetylpyruvate+acetate路线分歧，且止于中间体未达末端。辅因子O2/NADH未列属局部计量缺陷。主干部分成立、关键转化与连接需修订、合理性证据仅内部知识→5档。起点正确、无无依据跳步、替代路线按未证实登记不自动判错，故不构成D2关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：冻结S02产物为2,4,6-trioxoheptanoate、S03为acetylpyruvate+acetate、S04为pyruvate+acetate，并给出各步方向；不证明答案的2-methylmaleylacetate→2-methyl-3-oxoadipate为同一目标反应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：冻结accepted酶名/EC：S01 orcinol hydroxylase 1.14.13.6，S02 2,3,5-trihydroxytoluene-1,2-oxygenase 1.13.11.M3，S03 trioxoheptanoate hydrolase 3.7.1.-，S04 acetylpyruvate hydrolase 3.7.1.6；只支持对应反应功能，不证明具体蛋白活性。
- ANSWER_TEXT / 4bb6553923e019660f82da840816c2f48cf4607231bd9195a7a7696ff071325f：答案S2产物SMILES为null，S3止于2-methyl-3-oxoadipate，未给出后续到acetate/pyruvate；S1/S2辅因子未列。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按四个必答目标逐项：S01 orcinol hydroxylase对目标入口功能为S（EC未填但功能名可支持，不因缺EC降为M/F）；S02为必需中间步，程序为ROUTE_HOLD_REPRESENTATION/UNRESOLVED，答案酶名接近accepted name而产物2-methylmaleylacetate与gold 2,4,6-trioxoheptanoate的对应未解，记U；S03目标trioxoheptanoate hydrolase未交付，答案第3步为maleylacetate reductase EC 1.3.1.32的另一还原步，记M；S04目标acetylpyruvate hydrolase及acetate/pyruvate终点未交付，记M。S=1,N=4,C=0.25→&#91;3,4&#93;；仅S01已支持且S02跨带未决，取带内下沿3。无已核催化矛盾，key_error=N；KEY缺失/未决影响已由M/U计入。

<details><summary>V0.4理由与本行变化背景</summary>

S1 orcinol hydroxylase、S2 2,3,5-trihydroxytoluene 1,2-dioxygenase酶名与gold一致但EC均null（诚实缺失）；S3 maleylacetate reductase EC1.3.1.32与其声称的还原反应类型自洽，但与gold S03 trioxoheptanoate hydrolase不同，且EC1.3.1.32在E0无冻结记录无法核accepted name/reaction。无EC大类与反应类型错配、无酶名-EC互相矛盾→不判D3a关键错误；&#x27;合理候选+部分支持、关键步骤缺具体核验&#x27;取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：冻结S01-S04的accepted酶名/EC；S01答案orcinol hydroxylase可对应目标功能，S02目标为2,3,5-trihydroxytoluene-1,2-oxygenase，S03为trioxoheptanoate hydrolase 3.7.1.-，S04为acetylpyruvate hydrolase 3.7.1.6；不证明具体蛋白底物谱。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：冻结S02产物2,4,6-trioxoheptanoate、S03产物acetylpyruvate+acetate、S04产物pyruvate+acetate；用于区分答案S02产物未解、S03/S04目标反应未交付。
- ANSWER_TEXT / 4bb6553923e019660f82da840816c2f48cf4607231bd9195a7a7696ff071325f：答案S1酶为orcinol hydroxylase；S2产物为2-methylmaleylacetate；S3酶为maleylacetate reductase EC 1.3.1.32；无目标S03 trioxoheptanoate hydrolase、S04 acetylpyruvate hydrolase及acetate/pyruvate终点。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 3–4档：答案对所有步骤只给Pseudomonas sp. ORC，未给TaxID/保藏号/菌株级来源；gold S01/S02/S04为Pseudomonas putida，S03为Terrabacter sp. DBF63（UNRESOLVED）。ORC身份与单步能力均未核，且同一菌覆盖不同gold步骤；可取3–4档上沿4，但不把未核身份判成已证伪，故不cap。

<details><summary>V0.4理由与本行变化背景</summary>

全部3步及profile均用&#x27;Pseudomonas sp. ORC&#x27;，无TaxID/基因组/保藏号，仅INTERNAL_KNOWLEDGE_ONLY。属Pseudomonas与gold核心菌Pseudomonas putida同属（合理候选），但菌株&#x27;ORC&#x27;在E0无记录（f3e0:taxid:303为P. putida 303、f3e0:bacdive:12880为P. putida mt-2），身份与完整路径能力均未核；且complete_pathway_organism_profile_id=ORG_001声称单菌完成整条路径，而gold显示S3由Terrabacter sp. DBF63参与。无经核实编造/跨类群错配→不判D3b关键错误；&#x27;合理候选+部分支持、关键身份与作用范围未充分核验&#x27;取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_015：gold步骤菌：S01/S02/S04 Pseudomonas putida，S03 Terrabacter sp. DBF63；不支持ORC菌株身份或能力。
- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida TaxID 303物种记录；不核实Pseudomonas sp. ORC菌株。
- E0_EVIDENCE / f3e0:bacdive:12880：为P. putida mt-2(pWWO)菌株记录；不是ORC，不能回填其菌株性状或能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 5–6档下沿：15项均出现，其中5项明确null，属诚实未知；F10–F13等与Pseudomonas一般特征相符，但F7/F8/F9把orcinol利用、降解和羟化酶活性写成ORC菌株能力，均只有INTERNAL_KNOWLEDGE_ONLY且无菌株级证据。可给部分可用5分，关键项证据不足阻止进入良好档。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全列，10填+5诚实null（温度/pH/盐度/保藏/基因组null）。已填定性项（F1 aerobic、F6好氧呼吸O2、F10 motile、F11 rod、F12 Gram-negative、F13 non-spore、F15栖息地广）与Pseudomonas一般特征一致，且答案明确标注&#x27;仅按Pseudomonas属一般特征低置信度、未获菌株级来源&#x27;（诚实属级外推）；定量耐受性状未编造。问题：属级特征外推到未核实菌株ORC、菌株级适用性未证。未把预测当观测、无数值离谱、无把种级观测写成全体菌株耐受极限→不cap；&#x27;部分性状准确适用、关键项证据不足&#x27;取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_015：gold为Pseudomonas putida性状记录；不能自动转移到Pseudomonas sp. ORC，且培养温度不等于最适温度。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_015：标出若干子字段待裁定或仅完整性角色；不支持把未核性状判为已核错误。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 1–2档：evidence_registry三条全部为INTERNAL_KNOWLEDGE_ONLY，没有数据库条目、文献DOI、稳定链接或可定位记录；核心路线、酶、菌、性状均无法沿原交付来源核查。属MISSING_SOURCE低分，不属已核实错引，故不cap。

<details><summary>V0.4理由与本行变化背景</summary>

全部证据（EVID_001/002/003）source_type均INTERNAL_KNOWLEDGE_ONLY自我声明，无数据库条目/文献/计算记录，locator为描述性prose无稳定标识；决策相关组（CG01/02/03/05/07/08/09）与关键应用组（CG04/10/14）仅有内部知识→MISSING_SOURCE低分档。EC1.3.1.32在E0无记录→UNRESOLVED_SOURCE待核。无任何经核实错引→severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不cap。答案有evidence_registry的claim→EVID映射与claim_scope（可算生成记录雏形），故取3而非1-2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：只支持P. putida TaxID 303分类记录；不支持答案ORC身份、酶或性状来源。
- E0_EVIDENCE / f3e0:bacdive:12880：只支持P. putida mt-2菌株记录；不是ORC，不能作为答案原交付来源。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：accepted酶/EC参考；不是答案实际交付的可追溯来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 7–8档下沿： uncertainties明确列出EC未确认、SMILES未确认、性状仅属级低置信、辅因子未完全确认；置信度与internal knowledge大体相称，未见系统性把预测写成观测。但complete_pathway_organism_profile_id与route_summary整路表述仍超出已有证据，故取7不取8/9。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露强：uncertainties四项具体（EC未定、互变异构/SMILES未定、性状仅属级低置信、辅因子未确认）；confidence分级真实（null项unknown、属级外推low、路径medium）；明确全证据为INTERNAL_KNOWLEDGE_ONLY，观测/预测/未知划分清楚。不足：F7/F9等以medium包装属级内部知识、complete_pathway_organism_profile_id=ORG_001整条路径能力未标不确定——属单点过度确信，非系统性误导。&#x27;大部分合理标注、主要限制已说明&#x27;取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案自述的不确定性清单；只证明其披露内容，不证明底层断言为真。
- ANSWER_TEXT / ANSWER.evidence_registry：来源类型均为INTERNAL_KNOWLEDGE_ONLY，支持D6对其证据性质披露的总体判断。

</details>

## Grok

答案SHA256：`7807bee9c9a329065b34fa59f2ee5edc2decb5077684f88aab17afd9b7bdccbb`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步主链、路线名、好氧条件、每步底物/产物/SMILES、酶与微生物、一个去重profile及15项性状字段均实质回应；11项填写、4项显式unknown、0遗漏。部分EC与pH/盐度/保藏/基因组为null，属任务允许的未知，但使完整性与精确度不能进入9–10。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_015：确认本题为线性唯一4步Orcinol降解路线；不直接证明答案完整性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_015：确认路线名与Acetate/Pyruvate终点；不替代答案字段完整性核验。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1-S4碳骨架、方向与连接均与gold主链一致：orcinol→2,3,5-trihydroxytoluene→2,4,6-trioxoheptanoate→acetylpyruvate+acetate→pyruvate+acetate；好氧开环与水解方向正确。S2-S4以中性酸/省略H+表达，属电荷/质子表示局部缺陷，不改变主链化学结论。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：支持四步主链的方向、主底物/主产物及连接；不证明蛋白级实验活性。

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1与S4的酶名/EC分别命中accepted set的orcinol hydroxylase 1.14.13.6与acetylpyruvate hydrolase 3.7.1.6；S2/S3虽EC为null，但酶名分别对应accepted name 2,3,5-trihydroxytoluene-1,2-oxygenase与trioxoheptanoate hydrolase，且无已核催化矛盾。四步目标功能均可按accepted/G4功能粒度支持，故落&#91;7,8&#93;上沿；D3a 9–10被base range &#91;1,8&#93;及S2/S3表示/对齐未完全绑定阻断。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：支持四步accepted酶名与S1/S4 EC；不证明具体蛋白底物谱或实验活性。

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 核心菌Pseudomonas putida与TaxID 303为正确物种级身份；gold的PATHWAY_COMPLETE行支持P. putida 303完成该路线，S1/S2/S4步级归属也与gold一致。S3的gold步级来源为Terrabacter sp. DBF63，答案仍写P. putida，属局部步级归属待核，阻止进入9–10；未达到身份错误cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_015：支持P. putida 303的物种身份及PATHWAY_COMPLETE行；S03步级来源为Terrabacter，不自动支持P. putida的S3专一酶来源。
- E0_EVIDENCE / f3e0:taxid:303：官方分类记录支持Pseudomonas putida与TaxID 303；不支持菌株级或步级能力。

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 多数已填性状与gold相符：中温偏好、杆状、革兰氏阴性、不产芽孢、运动性、有氧呼吸/氧受体；pH、盐度、保藏号、基因组显式null也属诚实未知。扣分点在于“专性好氧”强度高于gold的aerotolerant记录，“极生鞭毛”超出仅支持motility的证据，以及苔黑酚碳源/能源的F7表述偏强。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_015：支持P. putida 303的motility、rod-shaped、Gram-negative、sporulation=false、mesophilic等观测；不直接支持strict aerobe或polar flagella。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_015：说明F2 min/max与F4 maximum等子字段仍待裁定或仅完整性；不用于把缺失自动判错。

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案交付了EVID_001-EVID_004及claim_scope，但除TaxID 303外多为INTERNAL_KNOWLEDGE_ONLY；EVID_002为泛化“classical literature”无定位，S2/S3关键开环/水解缺少可核条目。S1/S4 EC号与TaxID 303可定位，E0可核TaxID 303，其余EC记录E0未随附，登记UNRESOLVED而非错引。属部分关键结论可定位、其他模块缺映射的5–6档，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持TaxID 303与Pseudomonas putida学名；不支持菌株级或路线/酶文献。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：支持accepted酶名与S1/S4 EC；不替代答案实际交付的外部来源。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_015：支持P. putida的PATHWAY_COMPLETE行；不证明EVID_002为可定位文献。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确列出菌株/保藏/基因组未能定位、两个酶无确认EC、温度仅有中温判断、NADH SMILES省略及未核实真菌支路；null与unknown使用基本诚实。扣分在于部分INTERNAL_KNOWLEDGE_ONLY证据仍标high confidence（如S1酶/菌、氧耐受、形态/革兰/产孢），属单点或局部过度确信而非系统性误导。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_015：用于对照已披露/未披露的性状证据强度；不把UNRESOLVED当CONTRADICTED。

</details>

## GPT5.6

答案SHA256：`c016272d34baebf838d50a39960dcb1299e024a1a33b1aad2348eb61ca24175b`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求4步Orcinol主链并填写15项性状；答案只给出S1一步，S02–S04缺失，唯一organism_profile的15项性状全为null/unknown。核心任务模块大部缺失，落在1–2档；因仍给出一步结构化内容，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：Gold main chain has four ordered steps S01–S04; supports required main-chain length.
- ANSWER_TEXT / ANSWER.steps：Answer contains only one step and all 15 traits are null/unknown; supports incompleteness, not scientific correctness.

</details>

### D2 反应化学科学性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1将Orcinol羟化为2,4,6-trihydroxytoluene，而gold S01主产物为2,3,5-Trihydroxytoluene；第一步目标产物即错，S02–S04未给出，不能构成连续降解主链。核心第一步错误，落在1–2档；底物与羟化类型局部可辨，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：Gold S01 product is 2,3,5-Trihydroxytoluene; gold chain continues S01→S02→S03→S04.
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：Answer S1 product is 2,4,6-Trihydroxytoluene; supports product mismatch, not enzyme EC.

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1给出酶名Orcinol hydroxylase，与accepted名称局部一致，但EC为null，且其绑定产物2,4,6-trihydroxytoluene不是目标S01产物；目标反应未完成，不能给S信用。S02–S04无任何酶信息，属缺失。无已核实D3a关键错误（无EC类别冲突或名号矛盾），但S=0、覆盖极低，落在&#91;1,2&#93;，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_015：Gold S01 accepted enzyme name is orcinol hydroxylase with EC 1.14.13.6; S02–S04 have separate accepted enzymes.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_015：Gold S01 product is 2,3,5-Trihydroxytoluene; does not support answer S1 product 2,4,6-Trihydroxytoluene as target reaction.
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.enzyme：Answer supplies only one enzyme name, no EC, and no downstream enzymes.

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1给出Pseudomonas putida，与gold S01物种级身份一致；但strain、TaxID为空，且S02–S04没有对应微生物。答案未把单步菌写成整路径菌，complete_pathway_organism_profile_id为null。属于合理候选与部分支持，但多个关键步骤身份缺失，落在5–6档，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_015：Gold S01 organism is Pseudomonas putida species-level; S03 is Terrabacter sp. DBF63; supports only S01 species match.
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.microorganism：Answer gives one species-level microorganism and no downstream microorganism assignments.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 唯一organism_profile的15项性状全部为null/unknown，没有交付任何可评价性状值。按P44，全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：All 15 trait entries are null/unknown; supports MISSING status, not trait correctness.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry仅有EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，claim_scope为泛化内部知识声明；没有可定位外部来源。决策相关组均为MISSING_SOURCE，但无已核实错引，因此不触发D5 cap；可追溯性极低，取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：Shows only internal-knowledge evidence; does not provide a locatable external source.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案对酶和微生物均标low confidence，15项性状全部标unknown，uncertainties明确列出EC、菌株/TaxID及下游步骤未确定；未系统性把预测写成观测。主要不足是route_summary与S1产物表述仍偏确定，未把产物本身标为待核。整体披露较充分，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit uncertainty for EC, strain/TaxID and downstream steps; also shows remaining overconfident product/route summary.

</details>
