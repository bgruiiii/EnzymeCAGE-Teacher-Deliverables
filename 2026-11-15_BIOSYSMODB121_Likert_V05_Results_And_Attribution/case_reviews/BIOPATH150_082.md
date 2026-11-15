# BIOPATH150_082：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：acrylate degradation I

污染物：3-hydroxypropanoyl-CoA(4-)；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 42.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 43.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 73 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 40.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 47.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 34.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`0d5bcddbcbba34797c904d29caf8d3627837e172cb983d34862c1bbc7aa61fee`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案覆盖路径、酶、微生物、性状与证据登记等主要模块，但主链仅3步且S2的enzyme/microorganism整体为null；BRANCHED_DAG的current_path_id=null，无法按单一认可主链精确核对缺步，故仅给部分可用档下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

完整JSON，交付3步主链、2个菌株profile各15项性状、evidence_registry与uncertainties；主要缺项为S2整步酶与微生物均为null（题面要求每步给首选酶+EC+微生物），且主链仅覆盖到acetyl-CoA一支。按5-6档『主要模块均有涉及但若干必要内容遗漏』偏上取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_082：确认本题为BRANCHED_DAG且全图ordered_step_count=5；按D-M01该全图行数不默认作为单一主链缺步分母，仅支持任务为分支路线背景。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 3-羟基丙酰-CoA经丙二酸半醛、乙醛到乙酰-CoA的净氧化还原框架大体可配平，但答案把gold的水解+脱氢合并为一步，并以丙二酸半醛→乙醛→乙酰-CoA替代gold的氧化脱羧步骤；中间体与路线特异性连接证据有限，属弱档上沿4。

<details><summary>V0.4理由与本行变化背景</summary>

主链终点acetyl-CoA为gold终产物之一，净反应与gold等价（3-hydroxypropanoyl-CoA+2NAD++H2O→acetyl-CoA+CO2+2NADH）；但机制偏离：跳过gold的3-hydroxypropionate中间体（S01水解+S04脱氢），S1把水解+氧化并为一步并命名非标准dehydrogenase，S2用malonate semialdehyde直接脱羧成acetaldehyde（gold为EC 1.2.1.18乙酰化氧化脱羧直接到acetyl-CoA）。主干成立但关键中间体/连接需修订，替代无外部可核证据（仅内部知识），按5-6档取5；未构成原子不守恒或方向反转，不触发关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：展示gold的S01/S04/S02与S05/S03分支转化；不覆盖答案所写的丙二酸半醛→乙醛→乙酰-CoA分步替代。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 按已给认可主链范围核D3a（P082_1及可用的P082_2；不把全图未选分支当缺步分母，且source_selected_path_id=null的限制已在理由中体现）。答案自建3-hydroxypropanoyl-CoA→malonate semialdehyde→acetaldehyde→acetyl-CoA路线：S1产物为malonate semialdehyde而非目标S01的3-Hydroxypropionate，S2为malonate semialdehyde脱羧成acetaldehyde而非目标S02的3-Oxopropanoate+CoA→acetyl-CoA+CO2，S3的EC 1.2.1.10对应acetaldehyde→acetyl-CoA而非目标S02的EC 1.2.1.18；S04、S05、S03目标反应亦未按目标反应交付。故目标步S=0，无可用的目标酶-反应对应支持；按C04低档&#91;1,2&#93;，取1：核心目标催化对应基本缺失/失败，答案自身的替代路线自洽不能补目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

S3 acetaldehyde dehydrogenase (acetylating) EC 1.2.1.10(adhE)与该步acetaldehyde+CoA+NAD+→acetyl-CoA+NADH反应类型匹配，属可靠对应；S1命名『3-hydroxypropionyl-CoA dehydrogenase』EC null，且该步含CoA硫酯水解，单一dehydrogenase难覆盖，对应偏弱；S2酶null（诚实未知）。有合理候选与部分支持、关键步骤仍缺具体核验，按5-6档取5。EC 1.2.1.10在E0无记录(GAP-082-006)待核，不据此判错。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：目标步反应方向与主产物：S01为3-hydroxypropanoyl-CoA→3-Hydroxypropionate+CoA，S04为3-Hydroxypropionate→3-Oxopropanoate，S02为3-Oxopropanoate+CoA→acetyl-CoA+CO2，S05为3-hydroxypropanoyl-CoA→acryloyl-CoA，S03为acryloyl-CoA→Acrylate+CoA；用于比对答案S1-S3，不支持答案的malonate semialdehyde→acetaldehyde→acetyl-CoA作为目标反应完成。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_082：目标步accepted酶/EC范围：S01 EC3.1.2.4/4.2.1.116，S04 EC1.1.1.59/1.1.1.298，S02 EC1.2.1.18，S03 EC2.3.1，S05 EC3.1.2.4/4.2.1.116；不支持答案S1的无EC 3-hydroxypropionyl-CoA dehydrogenase或S3的EC1.2.1.10作为目标S02对应。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_082：本题根物为3-hydroxypropanoyl-CoA(4-)，gold终点主产物包含Acrylate|acetyl-CoA；用于确定目标范围，不证明答案任何步骤的酶对应正确。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S1-S3的实际反应、产物与酶字段：S1酶无EC；S2酶整体null；S3使用EC1.2.1.10但底物为acetaldehyde，不是目标S02的3-Oxopropanoate+CoA反应。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案把S1归属Ruegeria pomeroyi DSS-3、S3归属E. coli K-12 MG1655；两者身份字段可辨认，但均未与本题gold步骤菌（Halomonas sp. HTNK1、Candida albicans、Ruegeria pomeroyi等）绑定，E0对TaxID 373774与562无记录，S2微生物亦为null。存在多处步骤-菌归属不匹配，且无完整路径能力声称，定弱档4。

<details><summary>V0.4理由与本行变化背景</summary>

R. pomeroyi DSS-3为真实海洋玫瑰杆菌、参与丙烯酸/DMSP代谢，作为路径菌有合理性（gold在S05亦用R. pomeroyi 89184）；E. coli K-12为真实菌且AdhE确为EC 1.2.1.10代表酶，但E. coli非本题丙烯酸降解路径菌，仅作代表酶宿主。TaxID 373774与gold的89184不一致，E0无记录(GAP-082-022)不能判错，保持UNRESOLVED。有合理候选与部分支持、若干身份/作用范围未充分核验，按5-6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_082：列出gold各步对应菌，包括Halomonas sp. HTNK1、Candida albicans、Ureibacillus massiliensis、Ruegeria pomeroyi等；不证明其他菌绝对不能催化，但支持答案未按已认可步骤菌归属。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 两个profile均返回15项性状；E. coli部分为常见可核特征，R. pomeroyi的形态/运动/革兰氏等与同物种代表记录大致相容。但R. pomeroyi DSS-3的TaxID 373774、DSM 15171及E. coli多数数值在冻结材料中无逐项记录，部分字段只有叙述性preference或类别，故为部分可用、需实质核验的6。

<details><summary>V0.4理由与本行变化背景</summary>

两profile各15项齐全。R. pomeroyi的F10有运动性、F11杆状、F12革兰氏阴性、F13不产芽孢与gold 89184观测一致；F2中温、F4海洋型与gold(BacDive 30℃/盐度)方向一致。关键缺口：R. pomeroyi F14基因组全null（gold有GCA_018972145.1/约4.1–4.6Mb/GC~64%）未填；DSM 15171、E. coli基因组NC_000913/4641652bp/50.8%均无E0记录待核。E. coli非路径菌，其性状虽标准真实但适用性偏弱。按5-6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_082：提供Ruegeria pomeroyi(89184)、Ureibacillus等部分物种级性状记录；不含E. coli K-12 MG1655与TaxID 373774的完整逐项记录，不能全量核验。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_082：标明本case可计分/不可计分与待裁决子字段；支持D4只能按局部可核性状定档，不能按填满率机械给高分。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry全部为INTERNAL_KNOWLEDGE_ONLY，无database、record_id或locator；关键路线、酶、菌与性状结论均无法沿外部条目追查。答案如实标注内部知识且无已核错引，故不触发cap，但D5仍为明显不足档的2。

<details><summary>V0.4理由与本行变化背景</summary>

六条evidence全部source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator均null，无法追到任何可定位文献/条目/计算记录，按MISSING_SOURCE低分档。虽evidence_registry逐条列claim_scope且内部自洽，但不提供可追溯性。无编造/错引（E0无记录，编号类声称一律UNRESOLVED），不触发关键错误cap。按D5 1-2档取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案较系统地区分内部知识、低/中置信与明确未知，route_summary、steps&#91;*&#93;.uncertainty与uncertainties均列明路线级和步骤级限制；未把预测系统性写成实证，未掩盖主要矛盾。个别E. coli常规性状标注high/medium confidence但无外部来源，属轻微过度确信，不足以降入5–6。

<details><summary>V0.4理由与本行变化背景</summary>

答案系统性区分证据性质：全部evidence标INTERNAL_KNOWLEDGE_ONLY，逐字段confidence(high/medium/low/unknown)，uncertainties逐条列路线级、S1/S2/S3及菌档记忆性误差；替代分支明确标is_part_of_scored_main_route=false。未知诚填null（S2酶/菌、R. pomeroyi F14）。少量E. coli性状标high来自内部知识但属教科书事实且有记忆来源披露，不构成系统性误导。按7-8档取7。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`150fcc363657170e4ecdc19d48580b4f81cffb9d04ec3eeb1c1a02973d33fc44`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 按已认可主链 P082_1（S01→S04→S02）核验，未选 P082_2 分支不计缺步。答案模块齐全（4步、每步有酶/菌、15性状、证据登记），但交付主链不是 P082_1 或 P082_2：其 S1-S4 改为 3-hydroxypropanoyl-CoA→3-oxopropanoyl-CoA→acetyl-CoA+formyl-CoA→formate→CO2，属另选路线；题面锁定 acrylate degradation I，替代路线不能作为合法替代。因任务符合度关键偏离触发D1关键错误，按上限给4。

<details><summary>V0.4理由与本行变化背景</summary>

结构层面完整（4步均含底物/产物/酶/菌，15项性状全列、4项诚实null，含evidence_registry与confidence标签），但交付的化学路线与题面指定的 acrylate degradation I 不同：答案首步为3-羟基丙酰CoA脱氢（EC1.1.1.298）→3-氧丙酰CoA→乙酰CoA+甲酰CoA→甲酸→CO2，缺少gold路线中的3-羟基丙酰CoA水解→3-羟基丙酸→3-氧丙酸→乙酰CoA+CO2主支及acryloyl-CoA→Acrylate支，而route_scope.chosen_route_name仍填『acrylate degradation I』，属P100『自称合规却交付不同化学路线』的任务参数偏离→D1关键错误，cap≤4；档内因各模块齐全取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：gold adopted route edges and target steps for P082_1/P082_2；does not support the answer&#x27;s alternate CoA-thioester/formyl-CoA chain
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_082：route name acrylate degradation I and root/terminal identity；route-name only
- RUBRIC_CLAUSE / C01：题面指定路线为任务约束；另选路线不算合法替代
- RUBRIC_CLAUSE / C06：D1任务符合度与关键错误锚点

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分5 → V0.5新分7，变化+2。

新裁判理由：

> D2按所答化学自身质量评价，不因非gold自动降分。S1氧化（NAD+→NADH）、S2硫解生成acetyl-CoA+formyl-CoA、S3水解formyl-CoA为formate、S4甲酸氧化为CO2，方向连续且主链化学总体成立；NAD+/NADH、CoA、H2O有列。局部问题为多数主产物/中间体SMILES缺省、H+未列、S2/S3酶无EC，但辅因子遗漏按P103属局部计量缺陷，不自动cap；因此给7–8档中7，未达8的更充分结构/计量支持。

<details><summary>V0.4理由与本行变化背景</summary>

四步化学（醇氧化→硫解→甲酰CoA水解→甲酸氧化）方向forward、计量大体成立、步骤连续无断裂，未见D2关键错误（方向反转/原子明显不守恒/一步跳到中心代谢物）；但该路线与gold主链不同，且全凭INTERNAL_KNOWLEDGE无任何可核证据，按四.5登记为未证实替代路线——不自动判错也不给高分，属『主干部分成立、合理性证据有限』5档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / C06：D2化学方向、连续性、原子守恒与辅因子局部缺陷锚点
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏通常为局部计量缺陷，不自动cap
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：gold target route reference only；D2对答案替代链按自身化学独立评价，gold不直接认证该替代链全部步骤

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 按主链 P082_1 的目标步 S01/S04/S02 核验，未选 P082_2 的 S03/S05 不按缺步计入。S01目标为3-hydroxypropanoyl-CoA水解为3-hydroxypropanoate，答案S1却用dehydrogenase氧化为3-oxopropanoyl-CoA；S04目标为游离3-hydroxypropanoate氧化，答案无对应；S02目标为3-oxopropanoate经1.2.1.18生成acetyl-CoA+CO2，答案S2改为硫解生成acetyl-CoA+formyl-CoA；S3/S4的formyl-CoA/formate步骤不在该主链目标内。S=0；S04为M，S01/S02因表示/绑定边界为U；C=0对应&#91;1,2&#93;，答案有可辨认的局部酶/反应信息但无目标催化信用，取2。关键错误因关键性定义未完成且证据快照为EVIDENCE_GAP，保持UNRESOLVED。

<details><summary>V0.4理由与本行变化背景</summary>

S1给出EC1.1.1.298、S4给出EC1.2.1.2，S2/S3的EC=null（诚实未知）；两种EC与酶名/功能（脱氢、甲酸脱氢）大体对应，但EC未获冻结证据核实（E0 GAP，item_gaps 004/008/010/014），且S1把gold中用于游离酸步骤的EC1.1.1.298套到CoA酯底物存在底物粒度疑点；属『合理候选和部分支持、若干关键步骤缺具体核验』5档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_082：target accepted enzyme names/EC for S01/S04/S02 etc；does not support answer&#x27;s dehydrogenase/thiolase/formyl-CoA steps as target reactions
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：target reaction substrates/products for adopted steps；shows S01 hydrolysis, S04 oxidation, S02 acetyl-CoA+CO2
- RUBRIC_CLAUSE / C03：D3a S/F/M/U分类与目标反应口径
- RUBRIC_CLAUSE / C04：D3a分带、U的JUDGE_REQUIRED处理与NE出口
- RUBRIC_CLAUSE / C05：D3a 1–10档内锚点

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> The identity Pseudomonas putida KT2440 with TaxID 160488 is a plausible strain identity, but E0 for this case is EVIDENCE_GAP and the answer supplies no strain-level reaction evidence or whole-path capability evidence. All four steps and complete_pathway_organism_profile_id ORG_001 are assigned to the same strain with only EVID_001 INTERNAL_KNOWLEDGE_ONLY. Gold step organisms are non-exhaustive, so a gold-organism mismatch alone is not a cap; the low score reflects unsupported whole-path overreach and absence of step-level capability verification.

<details><summary>V0.4理由与本行变化背景</summary>

全部4步归 Pseudomonas putida KT2440（TaxID 160488），单profile ORG_001并声明complete_pathway；姓名/菌株/TaxID字段完整，但该菌不在gold任何step或PATHWAY_COMPLETE记录中，TaxID与整条路径能力均未获冻结证据核实（E0 GAP，item_gaps 020/024），并以INTERNAL_KNOWLEDGE支撑整路径能力；属『合理候选和部分支持、关键身份/作用范围未充分核验』5档，不判编造。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Frozen answer microorganism assignment and whole-path claim.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_082：Lists gold step organisms; non-exhaustive and not proof that P. putida KT2440 cannot be used.
- RUBRIC_CLAUSE / D-M01：Identity, single-step capability, and whole-path capability are separate; gold mismatch alone is not a cap.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> All 15 trait slots are present: 11 filled and 4 explicit null/unknown, so the field set is complete. Several values are plausible for P. putida KT2440 (for example F14 genome accession/size/GC, F1 oxygen, F12 Gram negative, F11 rod, F13 non-sporulating), but every trait has evidence_id null and E0 contains no P. putida KT2440 trait record. No specific unit/identity contradiction is verified. This is the 5-6 band: partial plausible content but key evidence insufficient; score 5 because support is uniformly absent.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全列（11项有值、F3/F4/F5/F9四项诚实null）；形态/革兰/产孢/运动性等定性项合理，F14给出具体登录号NC_002947.3与数值，但全部无evidence_id、confidence多为low/medium，温度最优值30℃等关键定量项无来源，pH/盐度填null；按已给内容与关键缺口评定为『部分性状准确且适用、关键项证据不足』5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Frozen answer trait values and evidence_id fields.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_082：Trait records cover gold organisms only; no P. putida KT2440 row, so cannot confirm or contradict answer traits.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_082：Scoreability mask for gold organisms; does not validate P. putida KT2440 values.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> All decision-relevant claims rely on EVID_001 with source_type INTERNAL_KNOWLEDGE_ONLY; there are no database, literature, record, or locator entries, and all trait evidence_id fields are null. This is MISSING_SOURCE, not a verified mis-citation. The D5 1-2 band applies; score 1 because no important conclusion is locatable to an actual source. No cap is triggered.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅1条EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator均null，被steps复用；全部性状evidence_id=null。无任何可定位文献/数据库/计算记录，全部关键结论归MISSING_SOURCE（低分档，默认不cap）；E0整题GAP无法核验，不判虚构、不判CONTRADICTED，按『几乎无法定位重要结论依据』取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Frozen answer evidence registry; shows INTERNAL_KNOWLEDGE_ONLY and no locatable external records.
- RUBRIC_CLAUSE / C07：MISSING_SOURCE low band and no automatic cap; not a substitution for scientific correctness scoring.

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer uses confidence labels (medium/low/unknown) and records INTERNAL_KNOWLEDGE_ONLY, so it does not uniformly assert high confidence and some nulls are explicit. However route_summary and the whole-path ORG_001 assignment are stated as fact, many unsupported trait values carry medium confidence, uncertainties is empty, and limitations are not explained. This is the 5-6 band: partial uncertainty disclosure but conclusion strength exceeds evidence. No systematic misinformation is proven, so no D6 cap.

<details><summary>V0.4理由与本行变化背景</summary>

各字段带confidence（low/medium/unknown），unknown性状诚实填null，具备基本不确定性标注；但uncertainties数组为空，未说明路线为未证实替代、未列主要限制或冲突，steps以medium信心包装仅由INTERNAL_KNOWLEDGE(低)支撑的酶/菌主张，并把未证实路线当作指定路线交付；属『有不确定性说明但过于笼统、部分结论强度超过依据』的单点/局部过度确信，非系统性误导，5档。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Frozen answer confidence labels, source_type, route_summary, and empty uncertainties field.
- RUBRIC_CLAUSE / C06：D6 separates single-point overconfidence from systemic misleading; no automatic D5-D6 linkage.

</details>

## Kimi

答案SHA256：`28b63c86f8e0f5fcc141ac20af367b4f7c73be2b5964d9f0a19bab59aa9e5477`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 按已认可主链P082_1评，题面要求3步主链、每步底物/产物英文名与SMILES、首选酶及EC、对应微生物，并给同一菌去重后的15项性状。答案原样填写chosen_route_name=acrylate degradation I，给出3步、每步酶/EC/菌、15项性状齐全且同一Ruegeria pomeroyi DSS-3去重为一个profile；有少量低置信无来源性状，但不构成D1关键缺失或路线偏离。

<details><summary>V0.4理由与本行变化背景</summary>

主链3步均给出底物/产物(名称+SMILES)、首选酶+EC、对应微生物；chosen_route_name逐字为&#x27;acrylate degradation I&#x27;符合题面；15项性状齐备(14填1明确未知)、同菌去重为单profile(ORG_001)；含中心代谢入口、下游与带is_part_of_scored_main_route=false的备选支路。完整性高；仅主链只覆盖双分支之一(至acetyl-CoA)且未显式说明与题面branched范围的对应，属少量范围说明不足。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION:BIOPATH150_082：任务要求3步主链、每步底物/产物/酶/EC/菌、15项性状及来源；氧条件null，路线名固定为acrylate degradation I
- ANSWER_TEXT / ANSWER:route_scope/steps/profiles：答案填写acrylate degradation I、3步P082_1、15项性状、同菌去重
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：P082_1主链为S01-&gt;S04-&gt;S02，终点acetyl-CoA；全图ordered_step_count不是单主链缺步分母
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_082：本题路线acrylate degradation I，graph_status=BRANCHED_DAG，仅用于范围定位

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 所评P082_1三步化学与gold主链一致：S01为3-hydroxypropanoyl-CoA硫酯水解生成3-hydroxypropanoate和CoA；S04为NAD+依赖氧化生成3-oxopropanoate；S02为CoA/NAD+参与的氧化脱羧生成acetyl-CoA与CO2。方向为底物到产物，步骤连续，终点为P082_1的acetyl-CoA。仅省略H+、以NAD+书写NAD(P)+等局部简化，不改变主链化学结论；D2九十分门未开，落7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

三步化学：S1 3-hydroxypropanoyl-CoA硫酯水解→3-hydroxypropanoate+CoA；S2 3-hydroxypropanoate+NAD+→3-oxopropanoate+NADH；S3 3-oxopropanoate+CoA+NAD+→acetyl-CoA+CO2+NADH。与金标S01/S04/S02逐步一致，方向正确、连续性(产物=下一步底物)成立、碳数守恒(3→2+1)，辅因子基本齐备。终产物acetyl-CoA为金标terminal之一，符合&#x27;主链&#x27;交付。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：P082_1三步反应方程、方向、底物/产物：S01水解、S04氧化、S02氧化脱羧至acetyl-CoA
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_082：起点3-hydroxypropanoyl-CoA(4-)；终产物含acetyl-CoA；P082_1终点匹配
- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;：答案三步底物、产物、cofactor、reaction_type与连续性

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分9 → V0.5新分6，变化-3。

新裁判理由：

> 按P082_1三个必答目标评酶对应。S04答案名3-hydroxypropionate dehydrogenase/EC 1.1.1.59与该步accepted名称-EC对匹配；S02答案名malonate-semialdehyde dehydrogenase (acetylating)/EC 1.2.1.18与该步accepted名称-EC对匹配，故S=2。S01的EC 3.1.2.4在该步accepted EC集内，但答案名3-hydroxyisobutyryl-CoA hydrolase不在该步accepted enzyme names，显式名称-EC配对未由冻结证据核验，计U=1（KEY entry），故不能进入7–8档；C=2/3落&#91;5,6&#93;，已支持两步逐反应清楚，取6。未见已核关键失败。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶-EC：S1 3-hydroxyisobutyryl-CoA hydrolase EC 3.1.2.4；S2 3-hydroxypropionate dehydrogenase EC 1.1.1.59；S3 malonate-semialdehyde dehydrogenase (acetylating) EC 1.2.1.18。三者EC与金标enzyme_gold对应步一致，酶名与EC功能类型吻合；EC accepted name未在E0机器核验，但金标EC为同一值，支持对应。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_082：S01 accepted names/EC含3.1.2.4但名称集不含3-hydroxyisobutyryl-CoA hydrolase；S04含3-hydroxypropionate dehydrogenase/1.1.1.59；S02含malonate-semialdehyde dehydrogenase (acetylating)/1.2.1.18
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：P082_1目标反应S01/S04/S02的底物、产物与方向
- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;.enzyme：答案酶名/EC：S1 3-hydroxyisobutyryl-CoA hydrolase/3.1.2.4；S2 3-hydroxypropionate dehydrogenase/1.1.1.59；S3 malonate-semialdehyde dehydrogenase (acetylating)/1.2.1.18
- RUBRIC_CLAUSE / C03：显式名称-EC配对待核时计U，不猜配对正确；S/U分类与KEY4不自动触发

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> Identity is specific and plausible (Ruegeria pomeroyi DSS-3, TaxID 246200, ATCC 700808/DSM 15171, NC_003911), but E0 is EVIDENCE_GAP and no claim-linked record verifies it. The answer assigns all three acetyl-CoA branch steps to the same strain and claims complete-pathway capability via EVID_002; gold organism_gold lists R. pomeroyi at S05 only and does not list it as PATHWAY_COMPLETE. Gold is non-exhaustive, so this is not a verified contradiction; 5-6 partial support with key strain capability still unverified.

<details><summary>V0.4理由与本行变化背景</summary>

答案统一推荐Ruegeria pomeroyi DSS-3(TaxID 246200)承担全部三步并作complete_pathway菌。金标步级微生物为Halomonas sp. HTNK1/Candida albicans/Ureibacillus massiliensis，Ruegeria仅出现在S05(acryloyl-CoA hydratase)。但Ruegeria pomeroyi的acrylate降解路径(经3-hydroxypropionate至acetyl-CoA)有文献(EVID_002 Todd 2010)支持，属合理可辩护候选，未构成由序列存在性过度外推；gene_or_protein留空、逐酶归属未确证。身份编号(E0)未核验。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_082：Lists R. pomeroyi at S05 only and lists other organisms as PATHWAY_COMPLETE; does not prove R. pomeroyi cannot perform the branch and does not confirm DSS-3 whole-path capability.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_082：Provides species-level R. pomeroyi (TaxID 89184) trait rows; not a strain-level DSS-3 (246200) capability record.
- ANSWER_TEXT / ANSWER.evidence_registry EVID_002：Todd et al. citation is delivered for strain-route association; E0 gap prevents verification of its actual support.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> Trait profile is partially accurate: Gram-negative and rod-shaped are supported by gold species-level observations; genome size/GC are plausible. But F10 says non-motile while gold R. pomeroyi 89184 records motility=true; F2 labels 30°C growth temperature as optimum_c though growth temperature is not optimum; F5/F7/F8/F9/F15 are largely unresolved or low-confidence. The motility issue is a supporting trait (CG15), not a systemic D4 key error; 5-6 partial accuracy with supporting-trait error and unresolved key data.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状：F12革兰氏阴性、F11杆状、F13不产孢、F14基因组(size≈4.60Mb,GC64.1%)、F1好氧、F7异养、F8降解谱等与金标观测/预测一致或合理；F3 pH诚实地null。但F10运动性填&#x27;不运动(non-motile)&#x27;与金标presence of motility=true(OBSERVED)矛盾，属明确布尔错误；F10/F11/F13无来源(low置信)、F14 raw_text中染色体4.11Mb+质粒0.49Mb与genome_size_bp=4601053口径不一致。主要性状可核实，存在少量数值问题。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_082：R. pomeroyi 89184 shows gram positive=false, cell shape=rod-shaped, motility=true, temperature growth=30°C, genome size up to 4,601,048 bp, GC 64.1%; species-level, not DSS-3-specific.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_082：Marks many R. pomeroyi trait rows as non-scoreable/completeness-only or predicted background; supports partial D4 rather than high confidence.
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：Answer gives one profile with 15 traits; several are low/unknown confidence and some conflict with species-level gold.

</details>

### D5 来源与可核查性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> Most key claims map to evidence IDs: route/enzymes to EVID_001, strain/route to EVID_002, identity to EVID_004/EVID_005, temperature to EVID_006. However E0 is EVIDENCE_GAP, so no source can be verified; MetaCyc page has no record ID; several traits have no evidence and are low/unknown. No verified mis-citation or cap. 7: key conclusions are traceable by delivered locators, with local records incomplete/unverified.

<details><summary>V0.4理由与本行变化背景</summary>

答案给出6条evidence_registry并逐claim绑定：步级reaction/enzyme→EVID_001(MetaCyc通路页,无record_id)、微生物→EVID_002(Todd 2010)+EVID_004(ATCC 700808)、基因组→EVID_005(NC_003911)、温度→EVID_006(DSM 15171)、多项性状→EVID_003(Moran 2004)。4条含具体record_id(ATCC/NC/DSM)或可定位文献，属条目级可定位；但核心路径/酶仅引&#x27;MetaCyc通路页&#x27;无稳定ID，F10/F11/F13无来源。E0为EVIDENCE_GAP，全部引用-声称链支持内容无法机器核实→UNRESOLVED_SOURCE待核，无已核实错引，不cap。属&#x27;部分关键结论可定位，其他模块待核/缺来源&#x27;的5–6档，取上。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Answer delivers EVID_001-EVID_006 with claim scopes and maps them to steps/traits; it does not include verifiable official records for all claims.
- RUBRIC_CLAUSE / R2-P33-P42：D5 uses claim-group source status; E0 gap requires UNRESOLVED rather than treating unverified as fabricated.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> The answer is unusually transparent: preserves oxygen null, leaves gene/protein null, marks many traits low/unknown, lists uncertainties, and excludes alternative branches from the scored main route. A few physiological traits (F6/F7/F8) remain medium-confidence and F10 is low-confidence but non-null without evidence; these are not systemic overclaiming. 8: most evidence types and boundaries are clearly labeled, with limited local over-specificity.

<details><summary>V0.4理由与本行变化背景</summary>

答案设uncertainties 4条并逐step写uncertainty(酶基因未确证、EC 1.2.1.18 NAD+/NADP+并存、支路排除)，confidence多标medium/low，F3诚实null；gene_or_protein一律留空，较好区分已知/未知/预测。不足：F10/F11/F13以low置信给出确定值且raw_text为null，未显式标&#x27;推断/待核&#x27;；F10与金标矛盾而未见冲突披露，属单点过度确信(档内扣)，非系统性误导。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; confidence fields：Answer explicitly records oxygen null, gene/protein null, low-confidence traits, and alternative branch exclusions; supports good D6 disclosure.
- RUBRIC_CLAUSE / R2-P119-P121：Distinguishes single-point overconfidence from systemic misleading; no systemic D6 cap applies here.

</details>

## Qwen

答案SHA256：`0b3952c5ee5ac5afea27a5aef3f6dfd1f010097350697d101e452b6f539c6849`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> Route name and oxygen null are echoed, and the JSON has pathway/enzyme/microorganism/traits/source/uncertainty modules. However only two steps are supplied, no EC numbers are given, CoA substrate/product SMILES are null, and 13 of 15 traits are explicit null. The main modules are nominally present but necessary step-level and field-level completion is weak, fitting the 3–4 band. Because D1 base range is HELD_PENDING_REPRESENTATION_REVIEW, this numeric score is submitted for review.

<details><summary>V0.4理由与本行变化背景</summary>

六个输出模块均有实质交付（2步路径、酶名、菌名、15项性状字段、1条证据、4条不确定性），但题面明列的每步SMILES与EC全部缺失、15项性状仅F8/F9有值（其余13项诚实未知）、gold为5步分支DAG（formal_cases.tsv ordered_step_count=5）而答案仅2步且未涉及acrylate分支；属“主要模块均有涉及、若干必要内容遗漏/仅占位”的5–6档，问题较多取低端5分。路线名原样回显acrylate degradation I、氧条件如实留null，未发现任务参数擅自更换，故不判D1关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BODY：Requires steps with enzyme/EC/microorganism, SMILES, and 15 traits; does not support answer content.
- ANSWER_TEXT / ANSWER.steps：Shows only two steps, missing EC/SMILES, and many explicit-null traits.

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer gives one continuous two-step alternative from the correct root to acetyl-CoA: oxidation to malonyl-CoA semialdehyde, then oxidative decarboxylation to acetyl-CoA plus CO2. Direction and broad carbon flow are partly plausible, but no SMILES or cofactors are supplied, the CoA intermediate identity is ambiguous, and the transformations do not demonstrate an accepted route. This is only partial usability with substantive revision needed, fitting 5–6; 5 because support is thin.

<details><summary>V0.4理由与本行变化背景</summary>

起始底物正确（3-hydroxypropanoyl-CoA(4-)为gold root），终点乙酰-CoA为gold两个终点之一（另为Acrylate），两步方向一致、碳数与CoA归属可自洽（C3→C3→C2+CO2）。但首步以CoA硫酯直接氧化替代gold首步EC 3.1.2.4水解（3-羟基丙酰-CoA+H2O→3-羟基丙酸+CoA），关键中间体写为“malonyl-CoA semialdehyde(4-)”而非gold的3-羟基丙酸/3-氧代丙酸；NAD+/CoA等辅因子全缺、SMILES全为null、无任何可定位依据，属“主干部分成立、关键中间体与连接需修订、合理性证据有限”的5–6档，取5。起点与终点均在gold范围内、无原子明显不守恒、未声明但未严重偏离题面终点，因此不触发D2关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0..1&#93;：Shows the claimed two-step oxidation/decarboxylation sequence.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：Lists gold reaction branches and directions; does not by itself prove an alternative chemistry is impossible.

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 按D-M01选择P082_1（S01→S04→S02，终点acetyl-CoA）与答案对照：答案S1将3-hydroxypropanoyl-CoA转为malonyl-CoA semialdehyde，未交付S01的3-hydroxypropanoate/水解酶反应；答案S2以malonyl-CoA semialdehyde dehydrogenase将CoA硫酯醛转为acetyl-CoA+CO2，底物、EC与S02的3-oxopropanoate+CoA/EC 1.2.1.18/malonate-semialdehyde dehydrogenase (acetylating)未对齐；S04亦缺失。未选P082_2分支不另计缺步。目标反应无确认S，核心入口/内部步未对应，落C04的C=0档&#91;1,2&#93;；按C05无已核目标成功，取1。

<details><summary>V0.4理由与本行变化背景</summary>

第二步酶名“malonyl-CoA semialdehyde dehydrogenase”在功能类别上与gold EC 1.2.1.18 malonate-semialdehyde dehydrogenase (acetylating) 相近，属部分支持；首步“3-hydroxypropanoyl-CoA dehydrogenase”不在gold酶单内，两步EC均为null、无基因/蛋白标识、无任何可定位条目，属“有合理候选和部分支持、关键步骤酶对应仍缺具体核验”的5–6档，取5。酶名与所写反应类型内部不矛盾（脱氢酶对氧化/氧化脱羧），故不按“酶名与EC互相矛盾”触发cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：支持P082_1中S01 3-hydroxypropanoyl-CoA→3-Hydroxypropionate+CoA+H+、S04 3-Hydroxypropionate→3-Oxopropanoate、S02 3-Oxopropanoate+CoA→acetyl-CoA+CO2；不显示malonyl-CoA semialdehyde为S01产物
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_082：支持S01 hydrolase EC3.1.2.4/4.2.1.116、S02 malonate-semialdehyde dehydrogenase (acetylating) EC1.2.1.18、S04 dehydrogenase EC1.1.1.59/1.1.1.298；不支持答案中的3-hydroxypropanoyl-CoA dehydrogenase及无EC的malonyl-CoA semialdehyde dehydrogenase作为对应目标酶
- ANSWER_TEXT / ANSWER.steps&#91;0-1&#93;.enzyme/products：答案自述S1为3-hydroxypropanoyl-CoA dehydrogenase生成malonyl-CoA semialdehyde；S2为malonyl-CoA semialdehyde dehydrogenase生成acetyl-CoA+CO2
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_082：支持本案为BRANCHED_DAG、全图ordered_step_count=5；全图步数不作为所选单条主链的缺步分母

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Cupriavidus necator JMP134 is a recognizable species/strain candidate, but the answer gives no TaxID and no step-level or complete-pathway evidence for this route. Both steps are assigned to the same organism, and complete_pathway_organism_profile_id ORG_001 asserts whole-path capability without support. Identity is plausible but capability/scope is largely unverified, fitting 5–6; 5 because support is very thin.

<details><summary>V0.4理由与本行变化背景</summary>

答案两步统一推荐Cupriavidus necator JMP134（TaxID=null），并以complete_pathway_organism_profile_id=ORG_001构成“全路径能力”声称。物种名本身可核（verified_species_name_crosswalk显示Cupriavidus necator=Ralstonia eutropha，TaxID 106590，仅SPECIES_NAME_IDENTITY_ONLY），但该菌不在冻结gold的step/pathway_complete菌单（Halomonas sp. HTNK1为主，另有Candida albicans、Ureibacillus massiliensis、Ruegeria pomeroyi）中，且step级催化与全路径能力零可定位依据，属“合理候选、关键身份与作用范围未充分核验”的5–6档，取5。E0无事实记录，未核≠虚构、也未核出身份错配，故不按身份阶梯cap（key_error=UNRESOLVED）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_082：Lists gold organisms for target steps; absence of C. necator JMP134 is not proof of falsity.
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：Shows the answer claims C. necator JMP134 for both steps and complete pathway.

</details>

### D4 性状科学性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> All 15 trait slots are present, but 13 are explicit null and only F8 and F9 are filled with low confidence. F8 asserts broad degradation capacity for the target transformation, and F9 asserts a dehydrogenase activity, both without a frozen trait record. Explicit nulls are not errors, but the only affirmative trait/capability claims are unsupported and application-relevant. This is weak, fitting 3–4; 4 because the explicit unknowns and low-confidence labels limit overclaiming harm.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状字段齐备，13项以null+confidence=unknown诚实标注（不计错、不重复扣D1）；仅F8（“可经acrylate degradation I 将3-羟基丙酰-CoA转为乙酰-CoA”）与F9（“3-hydroxypropanoyl-CoA dehydrogenase活性（推断）”）有值，均confidence=low、raw_text=null、唯一来源为INTERNAL_KNOWLEDGE_ONLY。gold性状/可评性掩模中无Cupriavidus necator JMP134条目，无任何数值、单位或菌株级实测可比对，属“部分性状适用但关键项证据不足、部分结论强度略超依据”的5–6档，取5；无“预测冒充观测”的确定性包装、无离谱数值，不判D4关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_082：Contains no Cupriavidus necator JMP134 trait rows; cannot verify F8/F9.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_082：Shows which trait rows are scoreable; C. necator JMP134 has no listed observed trait denominator.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> The answer supplies only EVID_001, source_type INTERNAL_KNOWLEDGE_ONLY, with a database label MetaCyc and a pathway-name locator. It provides no stable record ID, DOI, figure/table, or locatable entry, and the same label is reused for route, enzymes, organism, and traits. Decision-relevant groups are therefore MISSING_SOURCE; no verified mis-citation because E0 is a case-level evidence gap. This fits the lowest D5 band (1–2), with 2 because a pathway label is present but not locatable.

<details><summary>V0.4理由与本行变化背景</summary>

D5按claim group登记：决策相关组（CG01/02/03/05/07/08/09）全部只由唯一一条evidence_registry（EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，database=MetaCyc，record_id仅为路径名“acrylate degradation I”，claim_scope为步骤/酶/菌/降解能力/酶活）承载，属量表P34的MISSING_SOURCE；无任何条目级、可定位可核对的反应/酶/菌/性状记录，结论与来源关联很弱，落“仅笼统库名或自我声明”的3–4档，取3。MISSING_SOURCE默认不触发cap；本案E0为EVIDENCE_GAP，无已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：Shows only an internal-knowledge pathway label, not a locatable record.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> The answer explicitly marks most values unknown, uses low/unknown confidence, lists oxygen uncertainty, missing EC/cofactors, missing CoA SMILES, and lack of reliable trait sources. It does not systematically present predictions as observations. The main limitation is that some route/organism claims remain unsupported while still being stated, but this is not broad systematic overconfidence. Fits 7–8; 7 because unsupported core route/organism claims remain only lightly bounded.

<details><summary>V0.4理由与本行变化背景</summary>

证据性质披露总体较诚实：全部confidence取low/unknown，逐step写uncertainty，并将“氧条件未指定、两酶EC与辅因子未确认、CoA酯SMILES未给、性状多缺来源”列入uncertainties，F9自标“（推断）”，属“大部分未知/推断被正确标注、主要限制已说明”。但complete_pathway_organism_profile_id=ORG_001（全路径能力）与F8能力句未在uncertainties中作为未核推断点明，且以database=MetaCyc包装内部知识，个别结论强度略超依据；无系统性把预测写成实证、无掩盖矛盾的证据，按单点过度确信属档内扣分，不cap，取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit uncertainty and low/unknown labels; does not validate the route or organism.

</details>

## Grok

答案SHA256：`459a5c5d84c74f9086fe6d9c304418ae33d87fc4bb5ff8ec1b4faeb2bd5815a3`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Output is complete in format (5 steps, enzymes, one organism, 15 traits, evidence registry), but the task-specified acrylate degradation I main route is not followed: after S1 the answer goes to propanoyl-CoA/methylmalonyl-CoA/succinyl-CoA rather than the gold acrylate/acetyl-CoA branches. Route diagnosis is DEVIATES; this task-route deviation is a D1 key error, capped at ≤4. Within 3–4, 3 reflects substantial first-step overlap but a wrong main chain.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 459a5c5d84c74f9086fe6d9c304418ae33d87fc4bb5ff8ec1b4faeb2bd5815a3：Shows the answer&#x27;s delivered route and terminal product succinyl-CoA; does not establish task-route conformity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：Gold reaction rows show the required acrylate degradation I branches and terminal products Acrylate|acetyl-CoA; they do not support the answer&#x27;s succinyl-CoA terminal route.

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer&#x27;s alternative chemical route is internally continuous and chemically plausible: 3-hydroxypropanoyl-CoA dehydration to acryloyl-CoA, NADPH-dependent reduction to propanoyl-CoA, carboxylation to (S)-methylmalonyl-CoA, epimerization to (R)-methylmalonyl-CoA, and mutase conversion to succinyl-CoA. Cofactors for S2–S3 are listed; S5 adenosylcobalamin is noted but not listed as a cofactor. Because this is a chemically valid replacement route rather than the task route, D2 is capped in the 1–6 replacement range; 6 reflects coherent chemistry with only local cofactor/expression limits.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 459a5c5d84c74f9086fe6d9c304418ae33d87fc4bb5ff8ec1b4faeb2bd5815a3：Shows the answer&#x27;s step-by-step alternative chemistry, cofactors, and continuity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：Used only to distinguish the specified route from the answer&#x27;s chemically coherent replacement route; not used to award target credit.

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按C03/C04/C05对原登记5个目标步判断：答案S1给出3-羟基丙酰-CoA脱水为丙烯酰-CoA（EC 4.2.1.116），仅对应目标S05且程序登记为CANDIDATE，不能升S；答案S2把目标S03的AcuN/2.3.1替换为EC 1.3.1.84的丙烯酰-CoA还原为丙酰-CoA，目标S03不成立（U，不判已核F）；S01、S02、S04未交付（M）。故S=0、M=3、U=2，模块已交付故非MISSING/NE；仅有单个候选目标反应可用，其余核心目标缺失/替换，C05在&#91;1,2&#93;取2：比1多一个可定位候选，但无已确认目标步，不能进3–4。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps.S1-S5：答案交付5步：S1 EC4.2.1.116（3-羟基丙酰-CoA→丙烯酰-CoA+H2O）；S2 EC1.3.1.84（丙烯酰-CoA→丙酰-CoA）；S3 EC6.4.1.3；S4 EC5.1.99.1；S5 EC5.4.99.2；未交付S01/S02/S04对应目标反应，S2产物丙酰-CoA不对应S03的Acrylate终点。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：目标反应为S01、S02、S03、S04、S05；答案S1只与S05的3-羟基丙酰-CoA→丙烯酰-CoA对应，答案S2的产物丙酰-CoA不是S03目标产物Acrylate，S01/S02/S04未见对应目标反应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_082：目标accepted酶/EC包括S01 3.1.2.4/4.2.1.116、S02 1.2.1.18、S03 AcuN 2.3.1、S04 1.1.1.59/1.1.1.298、S05 3.1.2.4/4.2.1.116；答案的EC1.3.1.84、6.4.1.3、5.1.99.1、5.4.99.2不属于这些目标步的accepted集合。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 微生物身份本身正确：SUPP:TAX:272943确认TaxID 272943为Cereibacter sphaeroides strain ATCC 17023 / DSM 158 / ATH 2.4.1，Rhodobacter sphaeroides为历史别名；SUPP:DSM:158确认DSM 158为该型株。S2所写NADPH依赖丙烯酰-CoA还原酶活性有SUPP:PMID:23955006摘要级支持，3-羟基丙酸经丙酰-CoA同化也有SUPP:PMID:30455284种级支持。但S1、S3-S5在菌株2.4.1中的逐步催化及整五步路径能力主要依赖INTERNAL_KNOWLEDGE_ONLY的EVID_006/EVID_007；补充证据未直接证明丙酰-CoA羧化酶、甲基丙二酰-CoA差向异构酶、甲基丙二酰-CoA变位酶在该菌株中完成所述全路径。答案仍把同一菌株写为complete_pathway_organism_profile_id=ORG_001，属多个关键能力尚待确认，不宜7-8；身份未错且无核心身份被推翻，key_error=N。落5-6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / SUPP:TAX:272943：官方分类身份、rank及别名；仅证明TaxID 272943为Cereibacter sphaeroides strain ATCC 17023 / DSM 158 / ATH 2.4.1，Rhodobacter sphaeroides为别名；不证明各步活性、整路径能力或全部菌株性状。
- E0_EVIDENCE / SUPP:DSM:158：DSMZ exact-strain catalogue identifiers与观测培养条件；确认DSM 158为该型株，培养28°C厌氧光照；培养温度不等同最适温度，其他菌株不能替代。
- E0_EVIDENCE / SUPP:PMID:23955006：摘要级支持R. sphaeroides AcuI为NADPH依赖丙烯酰-CoA还原酶、参与3-羟基丙酸同化；支持S2相关活性，未证明全部五步或S1/S3-S5逐步能力。
- E0_EVIDENCE / SUPP:PMID:30455284：摘要级支持R. sphaeroides可利用3-羟基丙酸并经丙酰-CoA同化；支持种级/部分路径能力，不直接证明丙酰-CoA羧化酶、差向异构酶、变位酶在2.4.1中完成全路径。
- ANSWER_TEXT / answer_sha256:459a5c5d84c74f9086fe6d9c304418ae33d87fc4bb5ff8ec1b4faeb2bd5815a3：原答案将同一R. sphaeroides 2.4.1用于S1-S5并声明complete_pathway_organism_profile_id；用于定位其整路径微生物声称。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状齐全，且若干关键项有部分支持：F5的DSM 158由SUPP:DSM:158支持；F8/F9的3-羟基丙酸同化及丙烯酰-CoA还原酶活性由SUPP:PMID:30455284和SUPP:PMID:23955006摘要级支持；F1的兼性厌氧/光能异养描述与DSMZ培养描述大体相容。但F2 optimum_c=30°C无直接最适证据，SUPP:DSM:158只给培养28°C并明确培养温度不等于最适/耐受极限；F3、F4、F6、F10-F13主要依INTERNAL_KNOWLEDGE_ONLY的EVID_008，补充证据未核；F14仅有基因组accession，size/GC为null；F15自标low confidence。未见离谱到误导筛选的数值或把预测冒充观测的明确证据，故不触发D4关键错误；但多项关键/条件性状证据不足，落5-6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / SUPP:DSM:158：支持F5的DSM 158及部分培养描述；培养28°C厌氧光照，不是最适/最低/最高温度；不同菌株不能替代。
- E0_EVIDENCE / SUPP:PMID:30455284：摘要级支持R. sphaeroides利用3-羟基丙酸并经丙酰-CoA同化，可用于F7/F8的部分支持；不证明F2/F3/F4/F6/F10-F13等性状。
- E0_EVIDENCE / SUPP:PMID:23955006：摘要级支持R. sphaeroides AcuI的NADPH依赖丙烯酰-CoA还原酶活性，可用于F9的部分支持；不证明其他性状或全路径能力。
- E0_EVIDENCE / SUPP:TAX:272943：支持Rhodobacter sphaeroides 2.4.1/TaxID 272943的身份及别名；仅身份，不证明全部15项性状。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_082：本题gold性状切片未列Rhodobacter sphaeroides 2.4.1的性状行，不能用于支持或反驳其性状；不因不在gold自动判错。
- ANSWER_TEXT / answer_sha256:459a5c5d84c74f9086fe6d9c304418ae33d87fc4bb5ff8ec1b4faeb2bd5815a3：原答案organism_profiles&#91;ORG_001&#93;.traits.F1-F15的逐项填写与confidence；用于定位已给性状内容。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 is low because every evidence registry entry is source_type=INTERNAL_KNOWLEDGE_ONLY. Even where database names and EC record IDs appear, they are self-declared internal knowledge, not delivered locatable external evidence. Decision-relevant groups (route, entry, terminal, enzyme-EC, core organism identity) have only MISSING_SOURCE. There is no verified mis-citation, so no D5 key-error cap; the score is in the low missing/generic-source band.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 459a5c5d84c74f9086fe6d9c304418ae33d87fc4bb5ff8ec1b4faeb2bd5815a3：Shows all evidence entries are INTERNAL_KNOWLEDGE_ONLY and thus do not establish locatable external traceability.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 is strong: the answer labels evidence as INTERNAL_KNOWLEDGE_ONLY, distinguishes unknown values, explains route-boundary uncertainty, notes that the MetaCyc page was not directly checked, and discloses missing genome size/GC and omitted cofactor SMILES. Some step enzymes use high confidence despite internal sourcing, but this is a local overconfidence issue mitigated by explicit uncertainty notes; it is not systematic misleading.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 459a5c5d84c74f9086fe6d9c304418ae33d87fc4bb5ff8ec1b4faeb2bd5815a3：Shows explicit uncertainty disclosure, null handling, and INTERNAL_KNOWLEDGE_ONLY labeling.

</details>

## GPT5.6

答案SHA256：`ddc24ad59bf346d436c5e0ecef7d809460f95eae70935dd9b75dd66ca6bb2318`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 4分（3–4档）：答案只给出两步路线，15项性状全部为null/unknown，仅对这两步提供酶与微生物；题面要求的主链步骤和性状模块大部分未实质交付。JSON可读且路线名已回显，不能进入5–6档。D1核心完整性关键错误成立，分数封顶≤4。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT#BIOPATH150_082：题面要求主链逐步底物/产物/SMILES、酶与EC、对应微生物，并返回15项性状及来源。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_082：确认答案只交付两步且15项性状为null/unknown；不证明科学正确性。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 4分（落在给定D2&#91;1,4&#93;内）：S1的3-hydroxypropanoyl-CoA→acryloyl-CoA+H2O是化学上合理的脱水/水合方向，并对应gold分支的S05转化。S2将acryloyl-CoA还原为propionyl-CoA本身可成立，但不是题面acrylate degradation I中Acrylate/acetyl-CoA终点的核心转化，且缺少S01/S04/S02/S03所需主链步骤。因分支主链未绑定，不把该覆盖不符升级为已核D2关键错误；化学质量仅限低档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：提供gold各步底物/产物与方向；S05对应3-hydroxypropanoyl-CoA→acryloyl-CoA+H2O，但不支持S2的propionyl-CoA作为该路线终点。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_082：确认答案实际给出的两步化学及终点。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按已认可主链（P082_1/P082_2）目标反应N=5。答案steps&#91;0&#93;为3-hydroxypropanoyl-CoA→acrylyl-CoA+water，酶EC 4.2.1.116，与gold S05（可逆水合/脱水）相符，计S；steps&#91;1&#93;为acrylyl-CoA+NADH→propionyl-CoA+NAD+，EC 1.3.1.84，不对应任何gold目标反应。S01（目标水解至3-hydroxypropionate）所答为另一目标反应S05，S03（至acrylate）所答为还原反应，均计F；S02、S04未见交付，计M。S=1/5，C=0.20，落入&#91;3,4&#93;；仅少数目标可用且多数目标失败/缺失，取档内下沿3。整酶模块并非未交付，不按MISSING=1；关键性定义未完成，不另以KEY4压分；酶名/EC未出现本维大类别矛盾，key_error=N。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_082：提供本case目标反应S01/S02/S03/S04/S05的底物、产物与方向；其中S05为3-hydroxypropanoyl-CoA⇌acryloyl-CoA，S03为acryloyl-CoA→acrylate，S01为3-hydroxypropanoyl-CoA→3-hydroxypropionate+CoA；不证明答案的propionyl-CoA分支属于目标路线
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_082：提供accepted酶名/EC集合：S05接受EC 4.2.1.116，S01接受EC 3.1.2.4/4.2.1.116，S02接受1.2.1.18，S03接受2.3.1，S04接受1.1.1.59/1.1.1.298；仅功能级策展支持，不证明具体蛋白实验活性
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_082：题面路线为acrylate degradation I，root为3-hydroxypropanoyl-CoA(4-)，gold terminal main products为Acrylate|acetyl-CoA；不包含答案的propionyl-CoA终点
- ANSWER_TEXT / S1：答案实际交付：3-hydroxypropanoyl-CoA→acrylyl-CoA+water，酶3-hydroxypropanoyl-CoA dehydratase EC 4.2.1.116；可与目标S05对应
- ANSWER_TEXT / S2：答案实际交付：acrylyl-CoA+NADH→propionyl-CoA+NAD+，酶acrylyl-CoA reductase EC 1.3.1.84；不对应任何目标步
- QUESTION_TEXT / BIOPATH150_082：题面指定route_scope.chosen_route_name=acrylate degradation I，且要求按指定路线，不得改选其他路线
- RUBRIC_CLAUSE / C03：D3a按每目标反应登记S/F/M/U/H；所答为另一目标反应/结构可计F，未交付计M
- RUBRIC_CLAUSE / C04：S/N覆盖率选择非重叠候选分带；0.20≤C&lt;0.50→&#91;3,4&#93;；整酶模块未交付才MISSING=1
- RUBRIC_CLAUSE / C05：档内选择：少数目标可用且多数失败/缺失时取低分；4为最高许可而非默认值

</details>

### D3b 微生物身份与能力：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 4分（3–4档）：两步均归到Clostridium propionicum DSM 1682，未给TaxID或可定位证据；该菌株不在本题gold各步organism列表中，且complete_pathway_organism_profile_id=ORG_001把两步归因外推为完整路径能力。 acrylyl-CoA还原在生物学上有合理候选性，但整体身份/步级能力/全路径能力三层均缺证据。gold非穷尽且E0为缺口，故不判已核关键错误，只给低档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_082：列出各gold步骤的参考微生物及完整路径记录；不证明Clostridium propionicum DSM 1682具有这两步或整条路径能力。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_082：确认答案把两步及complete_pathway均归到同一菌株，且未提供TaxID/能力证据。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4按MISSING=1：15项必需性状全部为null/unknown，未交付任何可评价的性状值。按P44，全部必需性状均为null/空值时D4记MISSING=1并说明缺失，不宣称发现具体科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_082：确认15项性状均为null/unknown，未提供可评价性状值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 2分（1–2档）：证据登记EVID_001–EVID_003全部为INTERNAL_KNOWLEDGE_ONLY，database、record_id、locator均为null，路线、酶、微生物与性状均无法沿可定位来源核查。属于MISSING_SOURCE而非已核实错引，默认不cap；D5按缺失来源低分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_082：确认答案只提供内部知识型证据ID，无可定位数据库/文献记录。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 7分（7–8档）：答案明确把证据标为INTERNAL_KNOWLEDGE_ONLY，使用medium/low confidence，未知性状、TaxID、基因组信息置null，并列出氧条件未指定、辅因子变化及菌株未核验等不确定性。仍存在过度延伸：把两步归因写成complete_pathway_organism_profile_id=ORG_001，未讨论与gold主链/终点的差异；不构成系统性误导，故不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_082：确认答案对内部知识、低置信和未知项有披露，同时将两步外推为完整路径菌。

</details>
