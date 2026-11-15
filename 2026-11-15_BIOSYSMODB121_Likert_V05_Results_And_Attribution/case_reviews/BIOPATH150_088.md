# BIOPATH150_088：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：sulfolactate degradation III

污染物：2-Hydroxy-3-sulfonatopropanoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 42.5 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 35.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 42.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 35 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 49.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 37 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`e9b09890e81cb1ababa2871b6d8f8237982d8847c05e0b59583f69c59457d1a8`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> 题面锁定 sulfolactate degradation III，任务/gold 主链要求 3 步：2-hydroxy-3-sulfonatopropanoate -&gt; 2-oxo-3-sulfonatopropanoate -&gt; L-cysteate -&gt; pyruvate + sulfite。答案只在 steps 中给出 1 步，直接把 2-hydroxy-3-sulfonatopropanoate 经 EC 4.4.1.24 裂解为 pyruvate + sulfite，缺少 S02、S03 及相应酶/微生物，且使用了不同路线与 Cupriavidus necator H16。格式与性状表基本可读，但核心路径缺失约 2/3 且明显偏离指定路线，属 D1 严重任务符合度问题。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖登记显示路径/酶/菌/15项性状/证据登记/不确定性均已交付，格式可解析，模块面齐备；但题面把路线范围固定为sulfolactate degradation III，答案在route_scope.notes自称&#x27;按题面原样填写…未改选其他路线&#x27;，同时声明&#x27;该路线重建为单步C–S键裂解脱磺主链&#x27;，交付的化学路线与冻结gold的三步线性主链（S02 sulfolactate dehydrogenase→S03 L-cysteate aminotransferase→S01 L-cysteate sulfo-lyase，ordered_step_count=3、LINEAR_UNIQUE）不同。按&#91;P100&#93;任务参数偏离（自称合规却交付不同化学路线）归本维关键错误，cap≤4；因其余交付完整、无格式缺陷，档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：gold 主链含 S02-&gt;S03-&gt;S01：S02 生成 2-Oxo-3-sulfonatopropanoate，S03 生成 L-Cysteate，S01 生成 Pyruvate+Sulfite
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_088：该案 ordered_step_count=3、LINEAR_UNIQUE，说明评分主链按 3 步计
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_088：gold 目标步对应 Ruegeria pomeroyi、Roseovarius nubinhibens、Paracoccus pantotrophus NKNCYSA；答案所用 Cupriavidus necator H16 不在该 step 绑定中
- ANSWER_TEXT / ANSWER.steps：答案只有一步，route_summary 明确写为单步 C-S 裂解脱磺主链

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案所给直接反应 2-hydroxy-3-sulfonatopropanoate -&gt; pyruvate + sulfite 由 EC 4.4.1.24 支持：E0 官方事实明确 EC 4.4.1.24 为 (2R)-sulfolactate sulfo-lyase，催化 sulfolactate -&gt; pyruvate + hydrogensulfite，因此不是无依据化学跳跃。但它替代了题面锁定的三步主链，省略 2-oxo-3-sulfonatopropanoate 与 L-cysteate 两个关键中间体；产物写 sulfite 而非 hydrogensulfite，且未显式给出 H+ 平衡，属局部计量/表达问题。按 C06，化学可成立替换候选至多 6 分，故选 6。

<details><summary>V0.4理由与本行变化背景</summary>

交付的单步反应化学本身成立：底物2-羟基-3-磺酸基丙酸根→丙酮酸+亚硫酸盐，原子与电荷守恒（C3H4O6S2-→C3H3O3-+SO3^2-+H+），方向正向，产物与gold terminal（Sulfite|Pyruvate）一致；E0条目f3e0:tp:EV146-11证实EC 4.4.1.24的官方反应即为sulfolactate→pyruvate+hydrogensulfite。但该主链缺失gold的关键中间体与连接（3-磺硫丙酮酸、L-半胱氨酸两步），是以旁路式单步替代整条路径，步骤催化语义（STEP_REACTION_SEMANTICS_L2）与构型专一性未核，合理性证据限于内部知识加EC级事实。属&#x27;主干部分成立、关键中间体与连接需修订、证据有限&#x27;的5–6档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：EC 4.4.1.24 官方为 (2R)-sulfolactate sulfo-lyase，反应 sulfolactate -&gt; pyruvate + hydrogensulfite；支持该直接反应，不支持 gold 的 S01/S02/S03 目标步
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：gold 指定三步路线 S02-&gt;S03-&gt;S01；答案一步替代并省略关键中间体
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：仅给出一步直接裂解；产物列 sulfite 为 byproduct，未列 H+，也未给 3-sulfopyruvate/L-cysteate

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分6 → V0.5新分1，变化-5。

新裁判理由：

> D3a 按目标反应计：N=3。答案未交付 S02 的 sulfolactate dehydrogenase/EC 1.1.1，未交付 S03 的 L-cysteate aminotransferase/EC 2.6.1.1，也未交付 S01 的 L-cysteate sulfo-lyase/EC 4.4.1.25；唯一酶 EC 4.4.1.24 虽是真实直接 sulfolactate sulfo-lyase，但不属于任一必答目标步的 accepted 集合。该错误路线酶自洽不能增加目标信用。S=0、U=0、C=0，落入 &#91;1,2&#93;；几乎无可用目标催化对应，取 1。

<details><summary>V0.4理由与本行变化背景</summary>

酶功能与EC大类一致：EC 4.4.1.24为裂解酶（sulfo-lyase），与答案所称C–S键β-消除脱磺、产物丙酮酸+亚硫酸盐相符，E0证实其accepted name/reaction；不存在&#x27;EC大类与反应类型不匹配&#x27;&#x27;酶名与EC互相矛盾&#x27;的情形，故不触发D3a关键错误。但&#x27;3-sulfolactate sulfolyase (ComA)&#x27;的逐字命名与基因comA未见于冻结记录变体（UNRESOLVED），官方酶为(2R)-构型专一而答案未处理立体化学，答案又仅以INTERNAL_KNOWLEDGE_ONLY交付酶证据。属&#x27;有合理候选和部分支持、关键条目仍缺具体核验&#x27;的5–6档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_088：必答步 accepted：S01 为 EC 4.4.1.25，S02 为 EC 1.1.1，S03 为 EC 2.6.1.1；答案 EC 4.4.1.24 不在这些 accepted 集合中
- E0_EVIDENCE / f3e0:tp:EV146-11：EC 4.4.1.24 是官方直接 sulfolactate -&gt; pyruvate + hydrogensulfite 酶，但不是 gold S01/S02/S03 的目标酶对应
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：目标 S02/S03/S01 的底物/产物与答案单步直接裂解不匹配
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案仅声明 EC 4.4.1.24 用于直接裂解，未声明任何必答目标反应

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> C. necator物种名有crosswalk物种级支持，但菌株H16/TaxID 381666在E0无记录（GAP-088-021/024），单步酶归属和complete_pathway能力均无外部证据；答案把内部知识外推为整路能力。按D3b 5–6档取5：合理候选、部分身份支持，但关键菌株身份、反应级与整路能力未核验；未核实不判错，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案把该步归属Cupriavidus necator H16（TaxID 381666），并称其可利用3-磺酸基乳酸作为唯一碳源与硫源、complete_pathway_organism_profile_id=ORG_001。TaxID 381666在冻结证据中无任何记录（GAP-088-021/GAP-088-024，查询计划待派发），身份不能核实也不判虚构；crosswalk仅有species级Cupriavidus necator=106590，不覆盖菌株级编号。菌株能力声称仅INTERNAL_KNOWLEDGE_ONLY，无反应级或路径级证据，也未与题面/gold所列Ruegeria pomeroyi/Roseovarius nubinhibens/Paracoccus pantotrophus比较说明（gold非穷尽，不同不自动判错）。身份与作用范围均未充分核验，不触发已核实关键错误，属5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_088：gold主链微生物为Ruegeria pomeroyi、Roseovarius nubinhibens、Paracoccus pantotrophus，不含C. necator；非match不自动等于已证伪。
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_088：仅支持Cupriavidus necator物种名映射到106590；不支持H16菌株、TaxID 381666或降解能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项性状均给出，结构和单位基本完整；但全部仅INTERNAL_KNOWLEDGE_ONLY，无raw_text或外部条目，且C. necator H16的性状在E0为trait subfield gaps；关键温度、pH、盐度、碳源、基因组未核验。按D4 5–6档取5：部分性状合理可用，关键证据不足，需实质核验；不把未核验当已错。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部填写（温度最适30 °C、DSM 428、GC 66.4%、革兰氏阴性、不产孢、杆状、好氧、可运动等），但全部来自EVID_003（INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为null）；C. necator H16无冻结性状记录（GAP-088-042…054，BacDive新查询不在默认白名单），无法核实任何数值。多数项以medium/low标注，但F12革兰氏阴性、F13不产孢标high confidence与内部知识证据类型不相称（属单点过度确信，档内扣分，非系统性）。无已核实错误（不判数值错误），按&#x27;部分性状可能适用、关键项证据不足&#x27;的5–6档取5；完成度问题已在D1计，不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_088：gold性状覆盖Ruegeria/Roseovarius/Paracoccus，不覆盖C. necator H16；不能直接核验答案性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_088：scoreability mask针对gold菌；C. necator相关性状仍属EVIDENCE_GAP_TRAIT_SUBFIELD。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 所有关键组只有INTERNAL_KNOWLEDGE_ONLY/EVID_00x，无database、record_id或locator；按D5六状态为MISSING_SOURCE低档。答案有claim_scope和不确定说明，故在1–2档取2而非1；无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry三条（EVID_001/002/003）全部为source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，只能给出claim_scope文字，无法定位到任何条目，故决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09/CG17）全部为MISSING_SOURCE；按四.3/P34属缺失而非误导，低分档、默认不cap。已核实错引为零：EC 4.4.1.24的命名/基因关联为UNRESOLVED（非CONTRADICTED），TaxID 381666无记录亦为UNRESOLVED，均不判虚构，D5_SEVERITY=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。&#x27;几乎无法定位重要结论依据&#x27;的1–2档取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：E0外部记录存在，但答案未交付该来源；D5只评原交付，不得用E0回填。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确标出路线重建、ComA/EC、C. necator TaxID/DSM/GC等为内部知识/记忆待核，列出多步变体可能，confidence多为medium/low；未把预测写成实验观测。按D6 7–8档取8：主要限制和冲突已说明，少量具体值仍以中等置信填充但无系统性误导。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性与证据性质披露具体：uncertainties逐条说明路线编号与单步磺解的对应为内部知识推断、ComA/EC 4.4.1.24为记忆值、氧化脱磺变体与路线编号对应不确定、TaxID/DSM 428/GC 66.4%及温度pH为记忆性填写；每条evidence均明示INTERNAL_KNOWLEDGE_ONLY并给confidence；替代分支明确标is_part_of_scored_main_route=false，未冒充主链。不足：F12革兰氏阴性、F13不产孢等记忆值标high confidence，与证据类型略不相称（单点过度确信，非系统性），且未点明单步重建可能整体替换指定路线这一最大限制（仅写&#x27;可能不完整&#x27;）。属7–8档&#x27;大部分已正确标注、主要限制已说明&#x27;取7，不cap。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`f4906848dc657ec1f82f201a11b1169b1fb18f148922e48a8f7880291638fb3f`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 答案结构完整并给出3步、酶/EC和菌，但主链明显偏离冻结的sulfolactate degradation III：仅入口S02相当步骤匹配；S03被磺基丙酮酸脱羧酶替代，S01 L-cysteate sulfo-lyase缺失；15项性状全null、来源为空。按任务路线偏离/D1关键错误在&#91;1,4&#93;内取3：仅少数必要步骤可用，缺关键步骤和性状/来源。

<details><summary>V0.4理由与本行变化背景</summary>

路径、酶、微生物三个模块各3步均有实质内容（底物/产物名+SMILES、酶名+EC、菌名+菌株+TaxID），但style上冒充合规：route_scope.chosen_route_name写&#x27;sulfolactate degradation III&#x27;却交付磺基丙酮酸脱羧酶路线（EC 4.1.1.97→2.3.1.187，终点acetyl-CoA+sulfite），而路线III为L-cysteate氨基转移酶/磺基裂解酶路线（EC 2.6.1.1/4.4.1.25，终点pyruvate+sulfite），属P100&#x27;自称合规却交付不同化学路线&#x27;任务参数偏离；另15项性状全null、无任何来源。按关键错误封顶≤4，档内取3（三模块有交付但路线与性状双双失守）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：给出冻结三步主链顺序与产物：S02 2-hydroxy-3-sulfonatopropanoate→3-sulfopyruvate；S03 3-sulfopyruvate→L-cysteate；S01 L-cysteate→pyruvate+sulfite；不支持答案的脱羧/乙酰转移替代路线。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_088：终端主产物为Sulfite|Pyruvate；不证明答案acetyl-CoA为终端。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 按所答替代路线自身化学质量评价：S1磺基乳酸脱氢酶氧化、S2磺基丙酮酸脱羧、S3磺基乙醛乙酰转移酶生成acetyl-CoA+亚硫酸，三步连接和主要有机转化可成立；但S1缺氧化还原载体、S2脱羧式漏CO2，属局部计量/副产物缺陷，且为替代路线，按候选上限&#91;1,6&#93;给6。

<details><summary>V0.4理由与本行变化背景</summary>

按交付路线逐步解析SMILES：S1磺基乳酸&#91;O-&#93;C(=O)-CH(OH)-CH2-SO3-氧化为3-磺基丙酮酸&#91;O-&#93;C(=O)-C(=O)-CH2-SO3-（脱氢，方向正确）；S2脱羧生成磺基乙醛O=CH-CH2-SO3-（α-酮酸脱羧，计量正确）；S3磺基乙醛+CoA→乙酰CoA+亚硫酸盐（C-S裂解，原子守恒）。三步均真实酶促转化、方向与连接连续，无起始步错误/无依据跳步/无不守恒。但该路线为未声明、无证据的合理替代路线（四步判断：已偏离未声明+无证据→不给高分），且S1脱氢未标电子受体（局部辅因子遗漏）。取5–6档高分端6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：提供gold路线作对照，不直接证明答案替代路线正确；D2按答案自身化学连续性评价。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 已确认KEY S03目标失败：答案用sulfopyruvate decarboxylase/EC4.1.1.97替代gold S03 L-cysteate aminotransferase/EC2.6.1.1，产物sulfoacetaldehyde为路线外；入口S02仅结构匹配、sulfolactate dehydrogenase/EC1.1.1.334与accepted 1.1.1配对未核；S01 sulfo-lyase未交付。S=0,F=1,U=2；D-KEY4 cap≤4。仅入口局部信息可用，核心目标信用失效，取2。

<details><summary>V0.4理由与本行变化背景</summary>

每步酶名与反应类型匹配（sulfolactate dehydrogenase↔氧化；sulfopyruvate decarboxylase↔脱羧；sulfoacetaldehyde acetyltransferase↔碳硫裂解/乙酰转移），均为该路线的真实酶，属合理候选。但三个EC（1.1.1.334、4.1.1.97、2.3.1.187）在E0均无冻结记录（GAP-088-001/003/007），无法核accepted name/reaction；无基因/蛋白、无来源；且酶集属非题面指定路线。按&#x27;合理候选+若干关键步骤仍缺具体核验&#x27;取5–6档，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：S03反应行显示3-sulfopyruvate+L-glutamate→L-cysteate+α-ketoglutarate，与答案脱羧不同。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_088：accepted S03酶为L-cysteate aminotransferase EC2.6.1.1；不支持答案EC4.1.1.97。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 物种称Ruegeria pomeroyi DSS-3，TaxID 246200；gold种级Ruegeria pomeroyi(89184)有PATHWAY_COMPLETE，但菌株DSS-3/246200无冻结记录，且逐步催化归属无来源；S02/S03 gold步级菌为Roseovarius/Paracoccus。仅提供合理候选与部分种级支持，关键菌株身份和逐步能力未充分核验，取5。

<details><summary>V0.4理由与本行变化背景</summary>

Ruegeria pomeroyi是真实物种，gold对Ruegeria pomeroyi（种级89184）标PATHWAY_COMPLETE=TRUE，故&#x27;整条路径能力&#x27;在种级并非编造；但答案把同一菌株DSS-3用于三步（含脱羧酶步）且complete_pathway_organism_profile_id=ORG_001，菌株级TaxID 246200在E0无记录（GAP-088-019）→身份粒度未核，该脱羧酶路线的反应级/整路径能力亦未核，存在过度外推风险。按&#x27;合理候选+若干关键身份/作用范围未充分核验&#x27;取5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_088：S02/S03步级菌为Roseovarius/Paracoccus；PATHWAY_COMPLETE含Ruegeria pomeroyi 89184与Roseovarius 314263，但不含TaxID246200或对替代步骤的验证。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 15项性状均以value=null/confidence=unknown返回，属全部必需性状为空；按P44/D4规则记MISSING=1，不宣称科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状（F1–F15）全部value=null、confidence=unknown，organism_profiles&#91;0&#93;.traits无任何数值/观测。按P44&#x27;全部必需性状均为null/空值时D4按MISSING记1分，不宣称检测到科学错误&#x27;，故MISSING=1，不判为性状错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 答案evidence_registry为空，所有step/reaction/trait evidence_id为null，confidence多为low/unknown；没有任何可定位文献、数据库条目或计算记录。仅MISSING_SOURCE，未发现已核实错引，故不cap；D5在&#91;1,2&#93;低档取1。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry为空，steps各字段evidence_id全null，无数据库/条目录/定位，route_summary与各步结论零可追溯来源。所有claim组均为MISSING_SOURCE→按P34/P41低分档、默认不cap；无任何引用即无已核实错引（severity=NOT_APPLICABLE）。D5=2（不是1，因为给出了EC/ Taxon等可核对标识，但仍无任何来源记录）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案对酶/菌普遍给low confidence、对15项性状给unknown/null，未冒充高置信；但route_summary以确定性叙述替代路线，uncertainties为空，未说明证据类型/适用边界及来源缺失，属有不确定性标签但过于笼统、部分结论强于依据，取5-6档内6。

<details><summary>V0.4理由与本行变化背景</summary>

各步confidence=low、全部性状unknown、避免编造，属诚实的低置信标注；但无实质不确定性说明，未区分观测/预测/推断，未披露主要限制，route_summary把通路作为定论陈述且未说明这是相对题面指定路线III未声明的替代路线。按&#x27;有不确定性说明但过于笼统、部分结论强度超过依据&#x27;取5–6档，取5。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`58d9f16524bb6c58093ba9249e9e62f4822da7901893c148141fc5be4b8224c4`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> 答案格式与模块齐全，但主链化学为SlcD-ComDE-Xsc-Pta，不是题面指定route III的gold S02→S03→S01；缺少L-cysteate sulfo-lyase终点步，任务符合度关键错误成立，按&#91;1,4&#93;取2。

<details><summary>V0.4理由与本行变化背景</summary>

格式与模块覆盖完整（4 步均含底物/产物英文名与 SMILES、首选酶+EC、对应菌；单一 profile 去重；15/15 性状；证据登记与不确定性说明在位），但任务符合度失败：题面要求原样采用路线 &#x27;sulfolactate degradation III&#x27;，答案虽原样回填路线名，交付的主链却自第2步起改走 3-sulfopyruvate 脱羧支链（sulfoacetaldehyde→acetyl phosphate→acetyl-CoA），与本 case 冻结 gold 定义的三步 L-cysteate 支链（终点 pyruvate+sulfite）不同，属 P100 所称&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离，按八.D1 触发本维关键错误，capped≤4；因其余模块交付完整、偏离有披露，capped 档内取上限 4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：Gold route III directed reactions S02-&gt;S03-&gt;S01；不支持答案的替代四步链。
- ANSWER_TEXT / ANSWER：答案实际交付的替代主链及缺失的L-cysteate sulfo-lyase终点步。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 替代路线各步化学连接连贯：S1氧化、S2脱羧、S3脱硫磷酸解、S4磷酸转乙酰，均列辅因子且原子流向基本合理；但非gold路线且缺少独立实验支持，D2在&#91;1,6&#93;内取6。

<details><summary>V0.4理由与本行变化背景</summary>

首步与 gold order1 化学与方向一致（2-羟基-3-磺酸基丙酸根→3-sulfopyruvate，含 NAD+/NADH 与 SMILES，分子式与电荷一致）；但第2步转向脱羧支链，缺少 gold 的 L-cysteate 关键中间体与 L-cysteate sulfo-lyase 断键步，终点不同。就答案自述链本身，四步方向、结构、原子计量与连接基本自洽（S2 脱羧放出 CO2；S3 C–S 磷酸解生成 acetyl phosphate+sulfite；S4 磷酸转乙酰生成 acetyl-CoA；Pta 步已注明为文献推定），未见方向反转、无依据跳步或明显不守恒。按四.5：题面已指定路线、答案已声明支链边界与编号不确定，但支链证据在冻结快照无法核实（GAP-088-017）→&#x27;按未证实登记，不自动判错也不给高分&#x27;，落 5–6 档取 5；本维不 cap（任务参数偏离的 cap 在 D1 独立判定，四.1 不连坐）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：用于评价替代路线自身的化学连续性；不证明其是题面指定route III。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> S=0、F=1、U=2：S03为已确认KEY失败（答案S2脱羧替代gold S03转氨），S01缺失/对齐未确认，S02仅结构匹配且EC配对未核。D3a受D-KEY4约束在&#91;1,4&#93;，取2：仅有局部结构匹配，无可确认目标功能信用。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶名/EC/反应类型内部自洽且无自相矛盾：1.1.1.337 承担 NAD+ 依赖氧化、4.1.1.79 承担脱羧、2.3.1.234 承担 sulfoacetaldehyde 的 C–S 磷酸解、2.3.1.8 承担磷酸转乙酰；首步与 gold 的 sulfolactate dehydrogenase（EC 1.1.1 通配）同族，未出现&#x27;水解酶解释羟化&#x27;类大类错配。但四个 EC 在冻结快照均无记录（GAP-088-002/004/005/006），按四.6 无法核 accepted name/reaction/条目状态，只能记 UNRESOLVED；E0 的 EC 4.4.1.24 记录只确立一步 sulfolactate sulfo-lyase 的官方编号，既不支持也不否定本答案的四步链 → &#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;，5–6 档取 6。所引来源是否支持该酶-反应对应归 D5，不作本维关键错误依据（OBS-D3A-D5）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：Gold S03为3-sulfopyruvate + L-glutamate -&gt; L-cysteate + alpha-ketoglutarate；S01为L-cysteate -&gt; sulfite + pyruvate；不支持答案S2脱羧或缺失S01。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_088：Gold accepted enzymes；S02仅EC1.1.1家族，不确认EC1.1.1.337具体配对。
- ANSWER_TEXT / ANSWER：答案实际酶-反应分配；显示S2脱羧且无L-cysteate sulfo-lyase。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案四步均把微生物写为 Chromohalobacter salexigens DSM 3043 / TaxID 290398。该身份与保藏号真实，且该菌已知可降解 sulfolactate；但其把 ComDE–Xsc–Pta 氧化-脱羧主链整体归给 C. salixigens。补证中该酶组对应 Roseovarius nubinhibens ISM 的分叉路线，而 C. salixigens 摘要显示的是 SlcC/ComC/SuyAB，未支持 Xsc/ComDE/Pta 全路径。身份正确、广谱磺酸乳酸降解能力部分正确，但作用范围/路径能力错配，主要微生物推荐不能成立；按身份阶梯与路径能力条款计 D3b 关键错误，取上限 4。

<details><summary>V0.4理由与本行变化背景</summary>

身份三件套（Chromohalobacter salexigens / DSM 3043 / TaxID 290398）具体且内部一致，四步共用同一 profile、按物种+菌株去重，步级引用自洽；未出现由基因组存在某酶直接推断完成整条路径的写法，也未把单步菌写成全路径菌而不声明（complete_pathway_organism_profile_id 显式指向 ORG_001）。问题在于三层核验无法完成：TaxID 290398 与相关文献在冻结快照无记录（GAP-088-020/023、GAP-088-017），整条路径能力仅由未核文献 EVID_001 支撑；E0 唯一分类记录为 taxid 303（Pseudomonas putida），与本答案所声称菌无关，不能用于支持或反驳 → &#x27;有合理候选和部分支持，但若干关键身份或作用范围仍未充分核验&#x27;，5–6 档取 6；本维不 cap（无经核实的跨类群/异菌株错配）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_088：Gold 步骤微生物为 S01 Ruegeria pomeroyi/Roseovarius nubinhibens、S02 Roseovarius nubinhibens、S03 Roseovarius nubinhibens/Paracoccus pantotrophus；PATHWAY_COMPLETE 为 Roseovarius/Ruegeria；未列 C. salixigens。
- E0_EVIDENCE / SUPP:TAX:290398：仅支持 C. salixigens DSM 3043 的官方分类身份、rank 与别名；不证明该菌执行本答案的 ComDE–Xsc–Pta 路径。
- E0_EVIDENCE / SUPP:PMID:20007648：支持 C. salixigens DSM 3043 可降解 sulfolactate，并提到 SlcC、ComC、SuyAB；未支持 Xsc/ComDE/Pta 全路径归属。
- E0_EVIDENCE / SUPP:PMID:19581363：支持 Roseovarius nubinhibens ISM 的 SlcD–ComDE–Xsc–Pta/CuyA 分叉路线；不是 C. salixigens 的路线证据。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案将四步微生物统一绑定到 ORG_001 C. salixigens DSM 3043。

</details>

### D4 性状科学性：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> ORG_001 的 15 项均出现，但多个关键性状的数值/条件解释与冻结证据不符：F2 把 DSMZ 培养基培养温度 30°C 写成 optimum_c=30，培养温度不等于最适温度；F4 给 0.5–3.0 mol/L NaCl，与 SUPP:DSM:3043 的 0–32% w/v solar salt 范围和单位不一致；F14 GC 63.9% 与 DSMZ 60.5 mol% 冲突；F8/F9 把 C. salixigens 的降解/酶活写成 ComDE/Xsc 路线，补证只支持 SlcC/ComC/SuyAB；F10 无证据却给运动性。F1/F5/F7 及基因组登录号有部分支持，pH 等未知留空可接受。按多处数值/条件解释不符落 3–4 档，取 4；未认定单一关键错误已使主筛选结论失效，key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

15 项性状全部出现（filled 14、explicit_unknown 1、omitted 0），对象型字段结构完整、单位与条件在位（F4 mol/L NaCl、F14 NC_007963/3,696,649 bp/63.9% GC），pH 诚实填 null 并标 unknown，置信度按 high/medium/low/unknown 分级，未见把预测写成 DATABASE_DIRECT 观测的实证冒充。但本菌（TaxID 290398）在冻结快照无任何性状记录（GAP-088-025–041），全部关键数值无法核实；另有局部问题：F2 以 30 ℃ 作 optimum 且无 raw_text（培养温度不等于最适值，需核对来源语义）、F10 运动性无来源且 low、F15 由耐盐区间外推到栖息地广适性 → &#x27;部分性状准确且适用，但关键项证据不足或条件解释需修订&#x27;，5–6 档取 6。诚实 null 与缺失的完成度扣分不在本维重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：ORG_001 C. salixigens DSM 3043 的 15 项性状值。
- E0_EVIDENCE / SUPP:DSM:3043：支持 DSMZ 保藏号 DSM 3043、30°C 培养条件、好氧培养、0–32% w/v solar salt 耐受、基因组登录 NC_007963.1、G+C 60.5 mol%；明确培养温度不是最适温度。
- E0_EVIDENCE / SUPP:PMID:20007648：支持 C. salixigens DSM 3043 以 sulfolactate 为唯一碳源/能源生长；摘要提及 SlcC/ComC/SuyAB，不支持 F8/F9 的 ComDE/Xsc 酶组表述。
- E0_EVIDENCE / SUPP:TAX:290398：仅支持 C. salixigens DSM 3043 身份；不证明具体性状数值。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_088：Gold 性状记录针对本路线 Gold 微生物（Ruegeria/Roseovarius/Paracoccus），不提供 C. salixigens 的直接性状值；不能据此回填或替 C. salixigens 的性状。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 答案有具体 evidence_registry 与步骤/性状映射，但核心来源链错配：EVID_001 的 locator 写成 C. salixigens 的 Denger et al. 2009，实际 PMID 19581363 是 Roseovarius nubinhibens ISM 的分叉路线；EVID_003 将 Xsc 标为 EC 2.3.1.234，而官方 ENZYME 2.3.1.234 是 N6-L-threonylcarbamoyladenine synthase，不是 sulfoacetaldehyde acetyltransferase；EVID_002 MetaCyc 路线无 locator 且答案自述不能确证；EVID_004 被用于 F2/F4/F10 等超出可核范围。存在核心路线/酶-EC 来源不支持主要结论，按 D5 CRITICAL 关键错误 cap≤4；因仍有部分真实可定位来源（DSMZ 身份/培养、基因组登录、C. salixigens sulfolactate 文献），取 3。

<details><summary>V0.4理由与本行变化背景</summary>

逐组登记见 d5_registry：决策相关组（CORE：CG01/CG02/CG03/CG05/CG07/CG09；APPLICATION_CRITICAL：CG08/CG17，以及按声称取 APPLICATION_CRITICAL 的 CG14）来源状态以 UNRESOLVED_SOURCE 为主，无任何 VERIFIED_MIS_CITATION（冻结快照未提供可核对条目，唯一两条记录与答案所引对象不同）；CG12（pH 全 null）为诚实 MISSING_SOURCE，不扣为错引。交付记录具备条目级可定位性（完整文献书目、DSM 3043、NC_007963、四个 EC 号），但关键路线身份映射（EVID_002）经答案自认无法确证，且全部条目在快照内无法核对 → 按 P41 &#x27;存在条目级可定位可核对结论→5–6 档&#x27;取低端 5；UNRESOLVED 保持待核，不升为已核实关键错误、不 cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案的 evidence_registry 及步骤/性状引用映射。
- E0_EVIDENCE / SUPP:PMID:19581363：实际为 Roseovarius nubinhibens ISM 的分叉磺酸乳酸路线；不支持答案将其作为 C. salixigens DSM 3043 路线来源。
- E0_EVIDENCE / SUPP:ENZYME:2.3.1.234：官方记录为 N6-L-threonylcarbamoyladenine synthase（t6A synthase），不是 sulfoacetaldehyde acetyltransferase；不支持答案的 Xsc EC 2.3.1.234 对应。
- E0_EVIDENCE / SUPP:ENZYME:1.1.1.337：官方宽泛 L-2-hydroxycarboxylate dehydrogenase 记录，不能证明 C. salixigens 具体蛋白或本路线步骤活性。
- E0_EVIDENCE / SUPP:ENZYME:4.1.1.79：支持 sulfopyruvate decarboxylase 的名称/反应；不证明 C. salixigens 中的具体步骤归属。
- E0_EVIDENCE / SUPP:DSM:3043：支持部分 DSMZ 身份/培养/盐耐受/基因组登录事实；不支持 F2 最适温度、F4 精确 mol/L 范围、F10 运动性等超出记录范围的声称。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_088：Gold 步骤酶为 L-cysteate sulfo-lyase、sulfolactate dehydrogenase、L-cysteate aminotransferase；与答案的 ComDE/Xsc/Pta 路线不同，不能作为答案核心来源链的替代支持。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确披露route III归属不确定、列出替代分支、对多数不确定性状给low/medium/unknown并说明部分步骤为pathway推断；主要限制与冲突已说明。个别高置信（F7/F8/F9完整降解）与未核路线并存，故取8而非9-10。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界披露质量较高：route_scope.notes 主动说明路线编号归属无法确证；uncertainties 逐条列出编号不确定、可能实指 sulfo-lyase 路线则主链错误、EC 1.1.1.337 置信中等、菌株部分性状缺直接来源；步级 uncertainty 明确（S1 酶归属、S3 pathway 推断、S4 Pta 文献推定）；alternative_branches 均标 is_part_of_scored_main_route=false，未混入评分主链；F3 诚实 null 标 unknown。扣分点：四步 microorganism 一律标 high、F7–F9 以未核文献标 high，属局部/单点过度确信（八.D6 规定档内扣、不 cap）；未见系统性把预测写成实证、未见掩盖已知矛盾 → &#x27;大部分观测/预测/未知被正确标注，主要限制与冲突已说明&#x27;，7–8 档取 7。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案对不确定性、替代分支与置信度的实际披露。

</details>

## Qwen

答案SHA256：`c7484ea95b5e33731f1f9f959dc046249446e22df1a363a6679c1fae7e7fdec0`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D1核心任务模块大部分缺失且路线内容偏离：题面要求sulfolactate degradation III主链逐步交付并返回15项性状，冻结任务显示必答主链为3步（S02-&gt;S03-&gt;S01），答案仅给S1一步，且15项性状全部为null；其单步直接裂解路线不是题面指定的三步主链，构成D1任务符合度/完整性问题。因存在可辨认的S1、路线名和单步酶菌信息，档内取1–2档的2而非1；但缺失多数必要内容与路线偏离阻止进入3–4档。D1关键错误成立，cap&lt;=4。

<details><summary>V0.4理由与本行变化背景</summary>

必要模块覆盖明显不足：主链仅1步（gold路线III为3步线性主链），15项性状全部为空值，仅1条无法定位条目的笼统来源；更关键的是route_scope回显了指定路线名却交付了与路线III不同的化学内容（单步sulfo-lyase裂解），属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离。按D1关键错误条款cap≤4，因仍具备完整JSON外壳、底物/产物/酶/菌字段齐全且不虚构，取3档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_088：该案例ordered_step_count=3、n_required=3，题面主链为三步必答，不是单步主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：冻结主链为S02（sulfolactate dehydrogenase）、S03（L-cysteate aminotransferase）、S01（L-cysteate sulfo-lyase）三步；答案只交付S1，未交付S02/S03。
- ANSWER_TEXT / S1：答案steps数组只有S1一步；没有S2/S3或相应中间体步骤。
- ANSWER_TEXT / ORG_001：唯一organism_profile的15项性状字段均为null，未提供任务要求的性状值。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分3 → V0.5新分6，变化+3。

新裁判理由：

> 答案只给一步：2-Hydroxy-3-sulfonatopropanoate -&gt; pyruvate + sulfite，底物到终点产物方向合理；E0证据表明sulfolactate→pyruvate+hydrogensulfite的官方反应可由EC 4.4.1.24支持，因此该直接裂解作为化学替代路线本身可成立。但题面指定sulfolactate degradation III的3步主链，答案省略S02/S03并把S01式的sulfo-lyase直接套到起始底物上，属于化学可成立替换；按C06，D2化学可成立替换候选≤6，且缺少指定路线关键中间体/连接，不能进入7–8。答案EC写4.4.1.28而非E0的4.4.1.24属D3a问题，不在此维重复扣；产物写sulfite而非hydrogensulfite、立体化学未定为局部问题，不构成D2关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

按题面终点（sulfite+pyruvate）评价主链化学：答案只给一步，直接由2-hydroxy-3-sulfonatopropanoate裂解为pyruvate+sulfite，跳过了2-oxo-3-sulfonatopropanoate与L-cysteate两个关键中间体，并把路线III的起点转化替换为另一反应；单步自身的元素/电荷表述成立（C3H4O6S2-→pyruvate-+HSO3-，SMILES与gold对应物一致），故不落1–2档；但相对指定路线属&#x27;起始步错误+跳过两个中间步骤的断链&#x27;，主链连续性不成立，按关键错误cap≤4取3档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：官方事实：EC 4.4.1.24为(2R)-sulfolactate sulfo-lyase，反应为sulfolactate→pyruvate+hydrogensulfite且对R-构型专一；支持直接lyase化学作为可成立替代，但不支持答案所写EC 4.4.1.28，也不证明指定三步主链已被交付。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：指定主链含S02脱氢、S03转氨、S01磺基裂解三步；答案仅保留直接裂解到pyruvate/sulfite，省略S02/S03中间体，因此是替代路线而非指定主链。
- ANSWER_TEXT / S1：答案S1将起始底物直接转化为pyruvate+sulfite，并声称属于sulfolactate degradation III；未给S02/S03中间步骤。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分4 → V0.5新分1，变化-3。

新裁判理由：

> All three required target steps are absent: S02 sulfolactate dehydrogenase (EC 1.1.1) to 2-oxo-3-sulfonatopropanoate, S03 L-cysteate aminotransferase (EC 2.6.1.1), and S01 L-cysteate sulfo-lyase (EC 4.4.1.25). The answer instead gives one direct alternative lyase step to pyruvate/sulfite; no required target reaction receives credit. Score 1: almost no usable target catalytic correspondence and the core target recommendation is unusable.

<details><summary>V0.4理由与本行变化背景</summary>

唯一酶-反应对应为&#x27;sulfolactate lyase / EC 4.4.1.28&#x27;，作用于sulfolactate→pyruvate+sulfite：功能类型（lyase、脱磺酸）与E0中同转化的EC 4.4.1.24一致，属合理候选；但编号4.4.1.28在E0无任何记录（GAP-088-008/016），官方记录对同一转化的编号是4.4.1.24，且无gene/protein标识；该酶也不属于路线III任何一步（路线III第三步为作用于L-cysteate的EC 4.4.1.25）。属于&#x27;有合理候选但具体EC核验不成立、关键对应未落实&#x27;，落3–4档上缘取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_088：Lists required gold enzymes/ECs for S01-S03; does not support the answer&#x27;s direct sulfolactate lyase EC 4.4.1.28 for any required step.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：Defines the required S02 -&gt; S03 -&gt; S01 main-chain reactions; the answer&#x27;s one-step direct conversion does not match any required target reaction.
- E0_EVIDENCE / f3e0:tp:EV146-11：The official sulfolactate sulfo-lyase record is EC 4.4.1.24 for (2R)-sulfolactate -&gt; pyruvate + hydrogensulfite; it does not verify the answer&#x27;s EC 4.4.1.28 or target-step coverage.

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> Pseudomonas putida TaxID 303 has a supported species-level name-TaxID association in E0, but no strain is given and no step-level or whole-pathway capability is supported. The answer also sets complete_pathway_organism_profile_id=ORG_001 without evidence. Species identity is partially supported; reaction and whole-pathway capability are unsupported, placing D3b in the 3-4 band; score 4 because the identity record itself is correct.

<details><summary>V0.4理由与本行变化背景</summary>

唯一微生物为Pseudomonas putida、TaxID 303：E0官方分类记录学名精确匹配（species-level，SUPPORTED），身份定位成立且未编造；但无株号、无该步反应级能力证据、无整条路线能力证据，却在complete_pathway_organism_profile_id直接声称该菌完成整条路线，且该菌不在gold给出的步骤菌（Ruegeria pomeroyi / Roseovarius nubinhibens / Paracoccus pantotrophus）之列。按&#x27;身份定位≠反应级能力≠完整路径能力&#x27;三层分别核验，本维属有合理候选与身份支持、能力与作用范围未核，落5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Supports the species name Pseudomonas putida / TaxID 303 association only; does not support strain identity, step catalysis, or whole-pathway capability.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_088：Shows gold step-level organisms and pathway-complete organisms for comparison; gold is non-exhaustive, but the answer&#x27;s P. putida step/pathway capability is not supported by the delivered evidence.

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> All 15 required traits for ORG_001 are present only as null/unknown values; no trait value, unit, condition, or source is delivered. Under the all-traits-null rule, D4 is MISSING with score 1.

<details><summary>V0.4理由与本行变化背景</summary>

任务要求15项性状，答案虽保留了15个字段外壳，但全部value为null（对象型仅保留全null子键）、confidence均为unknown、evidence_id均为null，属全部必需性状为空值；按四.4不宣称检测到科学错误，记MISSING=1并保留权重参与总分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_088：Provides available gold trait records for the case organisms; the answer delivered no trait values to compare.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_088：Shows which trait fields are scoreable in gold; not relevant to filling the answer&#x27;s all-null trait delivery.

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> The answer provides one evidence entry: MetaCyc route-name locator with no record_id, reused for route, substrate, products, enzyme, and microorganism. This is generic rather than entry-level and cannot be checked against a specific MetaCyc record. Decision-relevant groups lack specific locatable records; no verified mis-citation, so no cap. Score 3 in the generic-source band.

<details><summary>V0.4理由与本行变化背景</summary>

全案只有一条证据（EVID_001：MetaCyc，record_id=null，locator仅为路线名&#x27;sulfolactate degradation III&#x27;），决策相关组CG01/CG02/CG03/CG05/CG07/CG08/CG09均无法定位到条目；EC 4.4.1.28无冻结记录，属UNRESOLVED_SOURCE待核。无经核实错引（未判虚构、未判CONTRADICTED引用），不触发cap；按&#x27;决策相关组全部仅有笼统来源→3–4档&#x27;取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry.EVID_001：Shows the delivered source is a generic MetaCyc route-name locator with no record_id; it cannot be verified as supporting enzyme, identity, or trait claims.
- E0_EVIDENCE / f3e0:tp:EV146-11：Supports an official EC 4.4.1.24 record; it does not support the answer&#x27;s EC 4.4.1.28 or its generic MetaCyc claim.
- E0_EVIDENCE / f3e0:taxid:303：Supports the TaxID 303 name association independently; it is not the answer&#x27;s delivered source and does not upgrade D5.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer explicitly notes oxygen condition unspecified, strain/stereochemistry not fully confirmed, and traits lacking direct sources/null. However it labels the enzyme and microorganism confidence medium and DATABASE_DIRECT without a specific record, and asserts complete_pathway_organism_profile_id without qualification. This is partial uncertainty disclosure with some overstatement, fitting the 5-6 band; score 6 for the explicit null/unknown disclosures.

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且诚实：明确写出氧条件未指定、菌株与立体化学未确认、性状缺直接来源故统一填null，并把15项性状的confidence统一标unknown，未把预测冒充观测；但存在单点过度确信：把单步裂解表述为&#x27;指定路线下&#x27;的主要过程并以medium/DATABASE_DIRECT包装无record_id的来源，complete_pathway声明也未附局限。属单点过度确信而非系统性误导，按5–6档取6，不cap。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit uncertainty statements for oxygen, strain/stereochemistry, and traits; does not cover the whole-pathway overclaim.
- ANSWER_TEXT / ANSWER.evidence_registry.EVID_001：Shows DATABASE_DIRECT/medium confidence attached to a generic route-name locator without record_id.

</details>

## Grok

答案SHA256：`33b1da17091bbef67450151fc1fd494204319a1798dda056b5f6f0a0a529ec49`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定路线sulfolactate degradation III，任务合同要求3个必答主链步（S02→S03→S01）。答案只交付1步直接C-S裂解，并在route_summary/uncertainty中明确声称不经过3-磺基丙酮酸、L-磺基丙氨酸等指定主链中间体，导致两个必答主链步缺失且实质改换路线；15项性状虽按字段返回但多数为null，不能弥补主链任务失败。按D1关键错误判定，属核心主链大部缺失并严重偏离指定路线，落在1–2档；因仍有可辨认的单步与profile交付，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_088：题面要求route_scope.chosen_route_name必须为sulfolactate degradation III，不得改选其他路线。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_088：本题gold为LINEAR_UNIQUE，ordered_step_count=3，支持任务存在3个有序主链步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：gold主链为S02→S03→S01：2-Hydroxy-3-sulfonatopropanoate→2-Oxo-3-sulfonatopropanoate→L-Cysteate→Pyruvate+Sulfite；不扩展到答案未交付内容。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案仅含steps&#91;0&#93;单步直接裂解，且在route_summary/uncertainty中声明不经过3-磺基丙酮酸和L-磺基丙氨酸。

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案自身的单步C-S裂解在化学上可成立：EC 4.4.1.24的冻结证据支持(2R)-sulfolactate→pyruvate+hydrogensulfite，方向为降解，终产物pyruvate/sulfite与gold终端一致，未发现原子明显不守恒或方向反转。但它以一步直接裂解替代题面指定的三步主链，省略2-oxo-3-sulfonatopropanoate与L-cysteate等关键中间转化；按C06，化学可成立替换候选≤6。其路线名称“III”的对应关系答案自述未核，且与gold三步序列不一致，不能进入7–8档；取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：EC 4.4.1.24的官方反应为(2R)-3-sulfolactate→pyruvate+hydrogensulfite，支持答案单步裂解在自身反应层面可成立；不支持其就是题面route III主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：gold指定主链包含S02→S03→S01三步及2-Oxo-3-sulfonatopropanoate、L-Cysteate中间体；不支持答案的一步直接裂解等同该主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_088：题面污染物的gold终端主产物为Pyruvate|Sulfite，答案终端产物与此一致；不证明所走中间步骤相同。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案将主链写成单步SuyAB/EC 4.4.1.24直接裂解，并声明不经过3-磺基丙酮酸、L-磺基丙氨酸或磺基乙醛。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三个登记必答步S02/S03/S01均未交付。所答S1是EC 4.4.1.24直接磺基乳酸裂解，与S02的1.1.1脱氢、S03的2.6.1.1转氨、S01的4.4.1.25 L-半胱磺酸裂解均不同，不能获得目标反应信用；错误路线内部酶自洽不补目标分。仅EC 4.4.1.24官方条目和终点产物局部可核，但不足以构成目标主链，C=0且目标信用按步阻断，落&#91;1,2&#93;；取1因无可用目标催化对应。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：支持EC 4.4.1.24直接裂解反应，不支持其等同gold S01/S02/S03任一步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：gold必答步为S02 2-Hydroxy-3-sulfonatopropanoate -&gt; 2-Oxo-3-sulfonatopropanoate、S03 2-Oxo-3-sulfonatopropanoate -&gt; L-Cysteate、S01 L-Cysteate -&gt; Sulfite+Pyruvate；均非所答一步。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Paracoccus pantotrophus NKNCYSA身份在gold organism_gold中有精确名称行，故身份定位有依据、非编造。但该菌株执行所答EC 4.4.1.24直接裂解步骤的反应级能力未在E0中核验，EVID_001文献条目不在E0。属合理候选加部分支持、关键能力未充分核验，落5–6；取6因身份精确且无已核实身份矛盾。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_088：支持P. pantotrophus NKNCYSA为gold相关菌株（精确名称行）；不支持其具备EC 4.4.1.24直接裂解能力。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状均出现：9项显式unknown/null，6项填写（F7 L-cysteate、F8 C3-有机磺酸盐降解、F9 SuyAB活性、F11球菌、F12革兰氏阴性、F13不产芽孢）。填写项与所引文献在语义上自洽，但E0/trait_gold对P. pantotrophus NKNCYSA只有UNKNOWN记录，关键性状值未独立核验，也无已核实矛盾。落5–6；取6因完整性好、诚实null多、填写项无已核实错误但证据不足。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_088：P. pantotrophus NKNCYSA的trait_gold行为UNKNOWN；不支持所填具体性状值，也不构成CONTRADICTED。

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> EVID_002/EC 4.4.1.24有E0条目级核验，支持直接酶-反应及pyruvate/hydrogensulfite终点化学；但路线核心、菌株直接能力、完整路径能力及多数性状依赖EVID_001/EVID_003，二者不在E0，保持UNRESOLVED_SOURCE。无任何VERIFIED_MIS_CITATION_*，不cap。部分关键结论可定位核对、其他核心模块未核，落5–6；取5因核心路线/能力仍缺可核来源。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：支持EC 4.4.1.24官方酶名与反应，不支持菌株能力或路线名映射。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_088：支持P. pantotrophus NKNCYSA身份定位，不支持其直接EC 4.4.1.24能力。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确区分已知、预测、未知：披露路线编号/机理风险、EC 4.4.1.24与4.4.1.25可能对调、菌株TaxID与性状缺失、物种级形态外推、SMILES非立体写法等；多数未知项诚实null。未见系统性把预测写成实证或掩盖矛盾。部分confidence（F9 high、路线medium）略强，但有明确限制说明，落7–8；取8因披露质量高，未给9因路线身份仍待核。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案自述不确定性；用于评价其证据性质与边界披露，不证明所述科学内容为真。

</details>

## GPT5.6

答案SHA256：`6e6b1757a51eb0a359a133fee363410059fc1df362ae74d6d3b2f6b8ccdc508b`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Only one of the three required main-chain steps is delivered; the entry oxidation S02 and transamination S03 are absent, and all 15 traits are null/unknown. The answer names the locked route but gives a direct one-step cleavage rather than the required three-step chain, so task completeness and route conformity are substantially deficient but the JSON remains readable and partial step/organism content exists.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：Shows required S02/S03/S01 reactions and main-chain sequence; does not by itself prove the answer&#x27;s alternative chemistry is invalid.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_088：Shows accepted enzymes for the required steps; not evidence delivered by the answer.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_088：Shows ordered_step_count=3 for the required chain.

</details>

### D2 反应化学科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The delivered single step is a chemically plausible C-S sulfo-lyase cleavage of 2-hydroxy-3-sulfonatopropanoate to pyruvate and sulfite, and E0 supports EC 4.4.1.24 for the sulfolactate cleavage reaction. Minor issues remain: no stereochemistry, uses sulfite rather than hydrogensulfite, and omits proton balance. This is alternative chemistry evaluated on its own D2 quality; task-route deviation is handled in D1.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：Supports EC 4.4.1.24 as (2R)-sulfolactate sulfo-lyase giving pyruvate plus hydrogensulfite; does not support Desulfovibrio sp. G11 or route III.

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Required N=3. The answer supplies one alternative direct cleavage step using EC 4.4.1.24 and does not deliver the required S02 dehydrogenase step, S03 aminotransferase step, or S01 L-cysteate sulfo-lyase step. Target coverage is 0; valid local EC/terminal-product information prevents score 1, but key entry/terminal steps are missing.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：Supports EC 4.4.1.24 local sulfolactate cleavage; does not support required S02/S03/S01 target steps.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_088：Shows accepted enzymes for required steps S01/S02/S03; answer&#x27;s EC does not match those accepted target steps.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_088：Shows required reaction sequence and intermediates; supports missing target steps.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_088：Shows N=3 required steps.

</details>

### D3b 微生物身份与能力：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer gives only Desulfovibrio sp. G11, with no TaxID and no reaction-level or strain-capability evidence. It is not in the provided gold organism rows, and the evidence is internal-only. Because the organism is not proven false, no key error is assigned, but support is too weak and identity/capability remain unverified.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_088：Lists gold step organisms (Ruegeria/Roseovarius/Paracoccus); does not contain Desulfovibrio sp. G11, but gold is non-exhaustive and therefore does not alone prove the answer wrong.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 required traits are present only as null/unknown values. Under the rubric, when all required traits are null/empty, D4 is recorded as MISSING=1 rather than as a detected scientific error.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_088：Shows that trait records exist for gold organisms; the answer itself delivers no trait values.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer&#x27;s evidence_registry contains only EVID_001 and EVID_002, both INTERNAL_KNOWLEDGE_ONLY, with no database, record_id, or locator. Important route, enzyme, microorganism, and trait conclusions therefore cannot be traced to a locatable source. No verified mis-citation is present because no external citation was delivered.

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer reasonably labels its evidence as INTERNAL_KNOWLEDGE_ONLY, uses medium/low confidence, and explicitly lists uncertainties including missing strain, TaxID, genome, and oxygen-condition information. It does not systematically present predictions as observations. Some route-summary and complete-pathway-profile wording is stronger than the evidence, so the score is not higher.
