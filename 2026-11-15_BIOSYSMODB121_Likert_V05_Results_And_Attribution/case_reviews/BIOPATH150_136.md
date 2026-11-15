# BIOPATH150_136：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：sulfoacetaldehyde degradation IV

污染物：Sulfonatoacetaldehyde；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 49.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 37 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 29.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 29 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 40 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 27.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`d437477abf0bb92d189183f1a5d6fd8c1b712dbc98a0a37d4429d5cc4e3d80c1`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> D1允许区间&#91;1,4&#93;。答案给出了路线名、步骤、酶、菌与15项性状，但主链呈现上把S6亚硫酸盐还原支路作为未标注alternative_branches的步骤列入，且固定路线诊断为DEVIATES；按D1任务符合度关键问题封顶，取4而非3，因为所有要求模块与字段类型均实质交付，未到“只覆盖少数模块”。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块齐备：chosen_route_name逐字填写题面路线名，6个步骤均给出主底物/主产物英文名与SMILES、首选酶、对应微生物，菌按物种+菌株去重（单条ORG_001）；15项性状字段集合完整（10项填写、5项明确null、0遗漏）。扣分点：S1/S2的EC留null，而gold同一反应载有EC 1.1.1.433与4.4.1.38，属字段未实质回应；TaxID、保藏号、基因组信息未填；S6为硫支路却以branch_id=null、predecessor=S2列入主链步骤，主链/下游/分支的结构标注不清晰。属7–8档&#x27;大部分必要内容完整、仅少量遗漏或工程缺陷&#x27;，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / d437477abf0bb92d189183f1a5d6fd8c1b712dbc98a0a37d4429d5cc4e3d80c1：支持答案实际交付内容、字段完整性及S6未标注为替代分支。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_136：仅支持路线名与gold终点；不证明哪些额外步骤合法。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：支持gold主链三步及其方向；S04–S06及未声明支路不属于该主链评分分母。
- RUBRIC_CLAUSE / C01：题面指定路线为任务约束；另选路线/未声明主链属D1任务符合度问题。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> D2允许区间&#91;1,5&#93;。主碳链关键转化与gold一致：sulfoacetaldehyde→isethionate、isethionate→acetaldehyde+sulfite、acetaldehyde+CoA→acetyl-CoA；但S3省略H+，S6亚硫酸盐还原式不完整且为未声明支路，固定诊断又标出S01立体/表示冲突。主干可信但需实质修订，取5，不取更低因主要有机转化成立。

<details><summary>V0.4理由与本行变化背景</summary>

主链S1–S3与gold三步逐一对应：sulfoacetaldehyde+NADH→isethionate（还原）、isethionate→acetaldehyde+sulfite（C–S裂解/亚硫酸盐消除）、acetaldehyde+CoA+NAD+→acetyl-CoA+NADH（乙酰化醛氧化），方向、结构、连接正确，并在S3即达gold终点acetyl-CoA；S4–S5为终点下游延伸（按P29不扣分、不加分），S6为亚硫酸盐还原的硫支路。局部问题：S2/S3未列H+、S6未给化学计量配平（简化式），S2把sulfite标为main而gold标BYPRODUCT——按P103属局部计量/标注缺陷，7–8档内处理，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / d437477abf0bb92d189183f1a5d6fd8c1b712dbc98a0a37d4429d5cc4e3d80c1：支持答案实际反应式、方向与缺失的计量/辅因子。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：支持三步参考反应、方向与辅因子；不外推到S4–S6。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_136：支持题面终点为acetyl-CoA。
- RUBRIC_CLAUSE / C01：支持路线锁定题中D2只评所答化学质量，不回填目标完成。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> N=3；S=1（S03 isethionate sulfite-lyase），F=1（确认KEY S01 NONMATCH），U=1（S02 PAIR_UNVERIFIED）。确认KEY失败使D3a≤4且confirmed_target_rate=1/3。一个目标有支持、一个关键终止目标失败、一个入口目标待核，故取3而非默认4；不把S02待核猜成失败或成功。

<details><summary>V0.4理由与本行变化背景</summary>

三个核心步的酶身份与反应类型和gold一致：sulfoacetaldehyde reductase（sarD，EC 1.1.1.433）、isethionate sulfite-lyase（islA/islB，EC 4.4.1.38）、acetaldehyde dehydrogenase (acetylating) EC 1.2.1.10，S3的EC与gold r01634行一致；S4/S5下游EC 2.3.1.8/2.7.2.1在冻结证据中无官方条目（UNRESOLVED）。扣分点集中在S1/S2：EC留null并断言&#x27;无确认EC编号&#x27;，而gold对同一反应载有对应EC（RE-01），属酶-EC字段缺失兼EC状态失实陈述；但酶名-反应对应本身可靠，未达到&#x27;核心步骤酶功能明显错误&#x27;。按7–8档&#x27;主要步骤酶对应有可靠支持，仅少量条目需进一步确认&#x27;取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / d437477abf0bb92d189183f1a5d6fd8c1b712dbc98a0a37d4429d5cc4e3d80c1：支持答案实际酶名、EC与对应步骤。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_136：支持accepted酶名/EC集合与S03函数匹配；不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：支持目标反应与方向；S01固定NONMATCH不由此改写。
- RUBRIC_CLAUSE / C04：支持D3a计数、&#91;1,4&#93;确认KEY失败封顶及未知保留规则。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> species层Bilophila wadsworthia与gold三步行及PATHWAY_COMPLETE（TaxID 35833）一致；但答案进一步声称strain 3_1_6且以ORG_001承担整条路径，gold切片无该strain记录与TaxID。按身份阶梯属粒度不足/菌株层待核，不cap，取7。

<details><summary>V0.4理由与本行变化背景</summary>

单一致病菌Bilophila wadsworthia覆盖S1–S3，与gold organism_gold三步EXACT匹配（TaxID 35833）一致，且gold PATHWAY_COMPLETE列35833（GCA_902374275.1）pathway_complete=TRUE，支持&#x27;整条路径能力&#x27;这一层级声称；答案的complete_pathway_organism_profile_id=ORG_001与此相容。缺口：菌株号3_1_6、TaxID、保藏号无冻结菌株级记录，答案自述&#x27;依据文献记忆填写、未核对&#x27;，属身份阶梯①粒度不足（物种级真实记录支持菌株级声称）——档内扣、默认不cap。取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / d437477abf0bb92d189183f1a5d6fd8c1b712dbc98a0a37d4429d5cc4e3d80c1：支持答案声称的物种/菌株/整路能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_136：支持species层身份及species层整路能力；不支持strain 3_1_6。
- RUBRIC_CLAUSE / C06：支持身份定位≠反应级能力≠完整路径能力及粒度不足不自动cap。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 多项性状与B. wadsworthia gold相符：严格厌氧、杆状、革兰氏阴性、不产孢、37°C生长、非发酵。但把37°C生长观测写成“最适37°C”；F5保藏与F14基因组虽gold有species记录却全null；F6亚硫酸盐末端受体、F7底物谱、F9路径酶活缺直接性状记录。部分准确但关键证据/条件需实质修订，取6。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状多与gold物种级记录相容：严格厌氧（aerotolerant=false）、革兰氏阴性、杆状、不产芽孢（预测行）一致；F7 asaccharolytic与gold发酵阴性记录方向一致，F9列出的三种酶与本题路径酶一致。问题：F2把&#x27;37°C生长观测&#x27;写成optimum_c=37与中温偏好（P52/P113：培养温度≠最适；gold的optimum子字段无观测源、min/max待老师裁决）；F6末端受体亚硫酸盐、F8降解谱、F15栖息地广适性为物种级推断，冻结记录无法核实（F6 sulfite为&#x27;No robust majority&#x27;预测）；F3/F4/F5/F14诚实null（gold实有DSM 109342、GCA_902374275.1、GC 58.1–62.8等记录未填）——完成度扣分归D1，D4不重复重扣（P112）。取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / d437477abf0bb92d189183f1a5d6fd8c1b712dbc98a0a37d4429d5cc4e3d80c1：支持答案具体性状值、null与置信度。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_136：支持species层性状；培养温度不等于最适；predicted背景不升级为观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_136：标识哪些性状可作observed_accuracy，哪些仅completeness/predicted背景。
- RUBRIC_CLAUSE / C07：支持性状原测量语义与不跨测试推断。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 主路线、酶、菌和性状的关键声称基本都指向INTERNAL_KNOWLEDGE_ONLY，无database/record/locator，按MISSING_SOURCE处理；唯一LITERATURE_DIRECT(EVID_006)只服务非评分替代分支且free-text未解析。decision-relevant核心组不可定位到可核来源，且无已核实错引，故低分档取2，不cap、不判虚构。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG08）的全部交付来源均为INTERNAL_KNOWLEDGE_ONLY：EVID_001–EVID_005无database、无record_id、无locator，主链结论无法沿记录追到任何可定位条目，符合MISSING_SOURCE低分档（P34/P41）；唯一可定位文献EVID_006（Ruff等2003, Biochem J 369）只服务非评分主链的Xsc替代分支，且为自由文书目、未在冻结证据中核到全文（UNRESOLVED_SOURCE）；支持组条目级证据不得跨档上调（P41）；E0本案唯一记录（EC 4.4.1.24）与答案声称无对应。无已核实错引，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / d437477abf0bb92d189183f1a5d6fd8c1b712dbc98a0a37d4429d5cc4e3d80c1：支持答案实际交付来源状态；internal-only不能当外部可核来源。
- RUBRIC_CLAUSE / R2-34：支持MISSING_SOURCE低分且默认不cap。
- RUBRIC_CLAUSE / R2-41：支持按claim group合成D5，不将支持组引用抵消核心组缺失。

</details>

### D6 不确定性与诚实度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案系统给出confidence，未知项多为null，uncertainties明确列出路线定义未核、EC缺失、strain未核、internal knowledge限制，未把预测系统性写成实证。仅F2“最适37°C”与“文献已知”表述略强，但整体披露质量高，取9。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据性质大体相称：明确标注多数事实为INTERNAL_KNOWLEDGE_ONLY、路线定义未直接核对、S3–S6基因细节未确认、菌株号凭记忆、氧条件按题面填null；null与confidence分层清楚，没有把预测冒充观测。扣分点：S1/S2以确定语气断言&#x27;该酶无确认EC编号&#x27;，与gold对同一反应载有EC 1.1.1.433/4.4.1.38不符（RE-01），属少点过度确信而非系统性误导，按P119档内扣、不cap；另有F2把生长温度写成最适的解释性拔高。取8。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / d437477abf0bb92d189183f1a5d6fd8c1b712dbc98a0a37d4429d5cc4e3d80c1：支持答案对未知、低置信、内部知识与限制的披露。
- RUBRIC_CLAUSE / R2-45：支持诚实null不同于编造，D6可因披露获较高分。

</details>

## DeepSeek

答案SHA256：`4c5b919346ea529f75de3b0f094189fed14e663e5eaf4b09b71afb8918b0dd11`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 覆盖路径、酶、菌、性状字段，但交付主链不是题面指定的S02→S03→S01：4条步骤中仅S2对应gold S01；S02还原和S03裂解缺失，S1以非gold直接裂解替代；15项性状全为null。按D1 3-4档（仅覆盖少数必要模块、多处缺步）取4。

<details><summary>V0.4理由与本行变化背景</summary>

结构完整：4步主链（底物/产物名称+SMILES、每步酶+EC、对应微生物）与15项性状外壳齐备，route_scope.chosen_route_name按题面原样回显。但任务要求“15项性状及各项最强来源”：15项value全部为null（明确未知，完成度扣分主归D1），evidence_registry为空、所有evidence_id为null（来源模块未交付），uncertainties为空、无限制说明；且步骤3–4越过gold终点acetyl-CoA延伸至acetate而未标注为下游延续。主要模块均有涉及但必要内容多处遗漏，5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：gold必答主链顺序与方向；不支持答案直接裂解替代主链。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_136：本题formal case为3步线性唯一主链；不等于要求全部旁支。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分4 → V0.5新分6，变化+2。

新裁判理由：

> 所答化学链sulfoacetaldehyde→acetaldehyde+sulfite→acetyl-CoA→acetyl phosphate→acetate内部连续，S2-S4转化与辅因子大体成立；首步直接C-S裂解缺少gold的还原/裂解中间体，且硫化物电荷/质子表达有局部缺陷，不能给7-8。按5-6档取6：主干部分成立但关键中间转化和依据有限。

<details><summary>V0.4理由与本行变化背景</summary>

主链第1步（steps&#91;0&#93;）将磺酸基乙醛直接裂解为acetaldehyde+sulfite；而指定路线IV在gold中首两步为S02 sulfonatoacetaldehyde+NADH→isethionate（EC 1.1.1.433）与S03 isethionate→acetaldehyde+sulfite（EC 4.4.1.38）。答案未声明替代路线、无任何证据，且首步酶EC 4.4.1.24经E0核实为(2R)-sulfolactate sulfo-lyase（sulfolactate→pyruvate+HSO3−），不支持所称裂解；首步反应式未列H+/水，亚硫酸盐为二价阴离子造成电荷轻微不配平。首步偏离使“交付指定路线主链”的主要结论失效，触发关键错误cap≤4；第2步acetaldehyde→acetyl-CoA（EC 1.2.1.10）与gold一致，第3–4步为超出gold终点的下游延伸、化学合理但E0未核，其余质量尚可，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：gold主链化学与方向；不支持答案首步直接裂解为等价主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_136：题面污染物入口与gold终点为acetyl-CoA；额外下游不进入目标主链评分。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> N=3。S01：答案S2 acetaldehyde→acetyl-CoA，name/EC 1.2.1.10命中accepted，计S（电荷/立体表示局部未核）。S02：答案S1为sulfoacetaldehyde→acetaldehyde+sulfite，不是必需的还原到isethionate，计F。S03：isethionate→acetaldehyde+sulfite缺失，计M。S=1,F=1,M=1，C=0.333→&#91;3,4&#93;；KEY_ENTRY失败使D-KEY4上界≤4。取3：仅一个必答步可用，关键路线入口错误/缺失。

<details><summary>V0.4理由与本行变化背景</summary>

4个酶/EC中，steps&#91;1&#93; EC 1.2.1.10 acetaldehyde dehydrogenase (acetylating)与gold S01一致；steps&#91;2&#93; EC 2.3.1.8与steps&#91;3&#93; EC 2.7.2.1化学上合理但E0无记录（待核）。关键首步把EC 4.4.1.24标为“sulfoacetaldehyde lyase”：E0记录该EC的accepted name为(2R)-sulfolactate sulfo-lyase、reaction为sulfolactate→pyruvate+hydrogensulfite（对R-构型底物专一），与所称酶名/底物/产物不符，属关键步骤酶-EC对应错误，触发关键错误cap≤4；其余酶对应尚可，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：官方EC 4.4.1.24为(2R)-sulfolactate sulfo-lyase，pyruvate-forming且R-构型专一；不支持sulfoacetaldehyde lyase声称。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_136：gold必答步的accepted酶/EC集合；不支持答案首步EC 4.4.1.24替代。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：gold必答反应顺序与底物产物；不支持直接裂解旁路作为目标主链。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> D. desulfuricans taxid 881身份有gold支持，organism_gold并有该pathway的PATHWAY_COMPLETE行；但答案把4步全部归给同一物种，无step-level催化证据，首步为非gold酶且下游PTA/Ack超出gold终点。身份正确、全路径支持部分成立，但多个作用范围仍待核，按5-6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

微生物推荐Desulfovibrio desulfuricans并填TaxID 881。gold PATHWAY_COMPLETE显示Desulfovibrio desulfuricans（taxid 876）完整路径=TRUE，物种选点与“完整路径菌”声称有参照支持；但gold物种级记录中TaxID 881实为Desulfovibrio vulgaris（同属异种），身份编号与物种名不一致（E0无881记录，GAP-136-021待核）；四步均归同一菌且无步级反应-菌证据。身份字段错配未推翻主要微生物推荐（物种真实且为完整路径菌），按八.D3b阶梯属档内扣分、不cap，5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_136：支持D. desulfuricans taxid 881的物种身份与gold pathway-complete状态；不支持答案非gold酶/下游步的step-level催化。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_136：本题gold主链状态；用于限制step-level归属范围。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 15项性状全部value=null、confidence=unknown，无任何可评价性状值；按P44全部必需性状null记D4 MISSING=1，不宣称科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状（F1–F15）value全部为null、confidence=unknown，未交付任何数值、单位、实验条件或来源。按四.4/P44“全部必需性状均为null/空值时D4按MISSING记1分，不宣称检测到科学错误”，整维记MISSING=1，完成度缺口在D1计分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_136：gold存在可评价性状记录；答案未交付任何性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_136：区分可评分与completeness-only子项；不把null当错误。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> evidence_registry为空，所有step/enzyme/microorganism/trait evidence_id均为null；没有任何可定位来源或生成记录。D5核心组均为MISSING_SOURCE，按低档取1。无已核实错引，不触发D5 cap；来源缺失不是虚构。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry为空、所有step/trait的evidence_id为null，全文无任何文献、数据库条目或计算记录，结论无法追查，属MISSING_SOURCE（缺失而非误导），按四.3/P34默认不触发关键错误cap；1–2档“几乎无法定位重要结论依据”取2。EC 4.4.1.24酶名不符属科学层错误（已在D3a计分），不是已核实错引，D5不据此cap（OBS-D3A-D5）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 所有酶/菌步骤标为medium confidence但evidence_id均为null，complete_pathway_organism_profile_id仍填ORG_001；虽15项性状标unknown，主要功能声称缺乏证据性质说明和限制，属多处过度确信/证据类型不清。按3-4档取4，不判系统性误导cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出confidence标签（酶/菌medium、15项性状unknown）并诚实把未知性状留null，未编造；但无任何限制、矛盾或待验证点说明，route_summary以事实口吻陈述未经核实的首步裂解与整条路线，结论强度超过证据（“部分结论强度仍超过依据”）。未见系统性把预测写成观测、也未见明知掩盖，属披露不足而非系统性误导，不cap，5–6档取5。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`3a9b39da01e5b2698e4fb3b3ae73321be53850c82265ac12ab13e7f01df7df5f`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 题面要求指定路线完整主链；答案只有1个步骤（S1），未交付S02/S03及终点acetyl-CoA。15项性状虽完整，但主链完整性严重不足，按D1 3–4档取3。

<details><summary>V0.4理由与本行变化背景</summary>

必要模块形式齐全：1步主链含底物/产物英文名与SMILES、酶+EC、菌、15项性状（13填写+2明确未知，无遗漏）、证据登记4条、不确定性2条；chosen_route_name原样回显题面路线名，工程格式无缺陷。但交付的化学路线本身与题面指定路线的主链不同（答案自称“该路线的主链为一步水解性脱磺反应”，gold为S02→S03→S01三步主链），属“自称合规却交付不同路线”的任务参数偏离，按P100/OBS-D1D2归本维关键错误，cap≤4；档内取4因其余模块与格式完整、无缺失。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT：题面要求给出指定路线主链的每一步，并要求每一步底物、产物、酶与对应微生物；不支持用单步替代完整主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：冻结gold显示S02-&gt;S03-&gt;S01三步主链及相应中间体；不证明答案的一步乙酸路线。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_136：gold终点为acetyl-CoA；不支持答案以acetate作为本路线终点。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案仅交付S1一步；用于完整性定位，不表示该步已获目标信用。

</details>

### D2 反应化学科学性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 答案给出一步水解裂解：Sulfonatoacetaldehyde + water -&gt; Acetate + Sulfite；与冻结路线S02（sulfonatoacetaldehyde + NADH -&gt; isethionate）的方向/产物不符，且未接S03/S01至acetyl-CoA。核心转化明显错误并严重断裂，按D2低档取2。

<details><summary>V0.4理由与本行变化背景</summary>

D2评反应化学与连续性，按四.5四步判断：第1步题面已指定路线名；第2步答案未声明替代路线（仅声明acetyl-CoA属下游），属未声明偏离→cap候选；第3步该单步反应在冻结证据中无可核条目（EC 4.4.1.12无记录），只能按未证实登记；第4步该偏离使“指定路线主链的化学”这一主要结论失效：首步与gold S02（NADH依赖还原为isethionate）不同，跳过isethionate与acetaldehyde两个中间体，并以acetate替代gold终点acetyl-CoA。属“主链第一步即错+无依据跳跃”组合，cap≤4；档内取3因还叠加终点偏移与两步缺失。配平层面（加水后C/H/O/S与电荷可平）不构成额外独立错误，不重复计。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：gold S02为sulfonatoacetaldehyde还原为isethionate，随后S03裂解为acetaldehyde/sulfite，S01生成acetyl-CoA；不支持答案的一步acetate/sulfite裂解。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_136：gold主链终端为acetyl-CoA；不支持acetate作为本路线主产物。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案只给一步水解裂解；用于化学定位。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> S02为目标入口KEY步，答案以非match的S1水解裂解替代；S01/S03仍为U且无目标酶/反应支持。答案只给sulfoacetaldehyde lyase EC 4.4.1.12，非accepted S02/S03/S01酶，E0亦无4.4.1.12记录；几乎无可用目标催化对应，按C05取1。

<details><summary>V0.4理由与本行变化背景</summary>

本维只评酶-反应对应。答案给出单一酶“sulfoacetaldehyde lyase / EC 4.4.1.12”，酶名类型（碳-硫裂解酶，EC 4.4.1.-）与其声称的水解性C–S裂解在类别上自洽，未见“EC大类与反应类型不匹配”或“酶名与EC互相矛盾”的可核证据；但EC 4.4.1.12的accepted name/reaction/条目状态在冻结证据中完全无记录（GAP-136-006/014/018），E0唯一EC条目是4.4.1.24（不同酶、不同底物），不能替代核验。故按“有合理候选、关键对应缺具体核验”取5，不cap、不判错。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_136：accepted目标酶为S02 sulfoacetaldehyde reductase (NADH) EC 1.1.1.433、S03 isethionate sulfite-lyase EC 4.4.1.38、S01 acetaldehyde dehydrogenase类；不支持EC 4.4.1.12。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：gold目标底物/产物与答案S1不同；不支持sulfoacetaldehyde直接裂解为acetate。
- E0_EVIDENCE / f3e0:tp:EV146-11：E0仅有EC 4.4.1.24（sulfolactate sulfo-lyase）的官方事实，不是答案的4.4.1.12；不能证明4.4.1.12存在或支持该反应。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.enzyme：答案酶名/EC与S1反应定位。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出Rhodobacter capsulatus（TaxID 1060，物种级、无株），但E0无该TaxID的记录；该菌被绑定到非match的S1反应，不能视为目标步能力支持。身份未证伪、菌株缺失有披露，按5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出物种级身份Rhodobacter capsulatus（TaxID 1060，strain=null），未把物种级记录写成菌株级，也未声称整条路径能力（complete_pathway_organism_profile_id=null），粒度上不构成身份错配。但：①TaxID 1060在冻结证据中无任何记录（GAP-136-001/020），ScientificName/rank/lineage无法核对；②“该菌催化该脱磺反应”缺反应级证据（P69三层：身份≠反应级能力≠全路径能力）；③gold该路线的STEP与PATHWAY_COMPLETE菌名单不含该物种（gold非穷尽，缺席不判错）。综合取5：合理候选+粒度合适，但关键身份与作用范围均未充分核验。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_136：gold目标步列出的菌不含Rhodobacter capsulatus；但gold非穷尽，缺失本身不证明该菌不能完成相关反应。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.microorganism：答案的物种、TaxID与无株声明。
- ANSWER_TEXT / ANSWER.uncertainties：答案主动声明未把物种级身份可靠限定到菌株。

</details>

### D4 性状科学性：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> D4要求性状对应所指对象且关键性状可核、适用。答案把 Rhodobacter capsulatus 配 ncbi_taxid=1060，但冻结官方 SUPP:TAX:1060 显示 1060 为 Rhodobacter 属（rank=genus），不是该种，身份粒度不符。F8/F9 又把 EC 4.4.1.12 sulfoacetaldehyde lyase 与一歩 sulfonatoacetaldehyde→acetate+sulfite 作为关键降解/酶活性状，而 SUPP:ENZYME:4.4.1.12 官方为 Deleted entry；gold 主链为 S02→S03→S01 至 acetyl-CoA（S02 reductase 1.1.1.433，S03 isethionate sulfite-lyase 4.4.1.38），不是该一歩反应。其余温度、pH、盐度、运动性等性状在冻结 trait_gold 无 R. capsulatus 记录，BacDive 仅给搜索 URL，不能逐项核实；部分值可能合理，但关键降解/酶活及身份已失效，D4只能低档3。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部给出（13项填写、F5与F14明确null+unknown，无遗漏），多数条目带confidence分级，未出现“预测值冒充观测值”的显式标签，也未出现明显离谱数值（如极端温度），且菌株级保藏号/基因组在无据时留空，符合“诚实null”要求。但：Rhodobacter capsulatus (taxid 1060) 的全部性状子字段在冻结证据中均无官方记录（GAP-136-032…041，唯一来源EVID_003为BacDive检索页无record_id），因此温度/pH/盐度/氧需求等关键项均不可核实；F7/F8/F9把目标污染物降解能力写在物种级profile上，承担应用判断却无条目级证据。按“部分性状可合理对应但关键项证据不足”取5，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / SUPP:TAX:1060：官方分类记录：taxonId 1060 为 Rhodobacter 属（rank=genus），不是 Rhodobacter capsulatus 种；分类身份本身不证明种级性状。
- E0_EVIDENCE / SUPP:ENZYME:4.4.1.12：官方 ENZYME 记录对 EC 4.4.1.12 标记为 Deleted entry；不支持 sulfoacetaldehyde lyase 活性或该酶-EC 配对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：gold 主链 S02 为 sulfonatoacetaldehyde→isethionate，S03 为 isethionate→acetaldehyde+sulfite，S01 为 acetaldehyde→acetyl-CoA；不是一步 sulfonatoacetaldehyde→acetate+sulfite。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_136：本题冻结 trait_gold 切片没有 Rhodobacter capsulatus/TaxID1060 的性状行；多数所填性状在本材料中不可逐项核实。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 答案交付了 EVID_001–EVID_004，但关键来源链有核心错引。EVID_002 以 EC 4.4.1.12 高置信支持 sulfoacetaldehyde lyase，而 SUPP:ENZYME:4.4.1.12 官方为 Deleted entry，来源存在却不支持该酶-EC 声称，属 CORE 已核错引。EVID_004 以 TaxID 1060 支持 R. capsulatus 种级身份，而 SUPP:TAX:1060 为 Rhodobacter 属（rank=genus），属种级/属级粒度错配，亦为 CORE 已核错引。EVID_001 仅为 MetaCyc 页面标题、EVID_003 仅为 BacDive 搜索 URL，均无具体 record_id，路线/性状来源无法定位到条目，保持 UNRESOLVED/GENERIC，不抵消核心错引。D5按关键错误 cap≤4；两处核心错引且其余来源不可核，取低档3。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付了4条来源登记（MetaCyc路线页、IUBMB EC条目、BacDive检索页、NCBI Taxonomy），并逐条写claim_scope与confidence，形式上可定位；但决定档位的决策相关组（CG01/CG02/CG03路线、CG05酶-EC、CG07菌身份、CG08步级归属）全部只有页面/编号级定位，其内容在E0快照中无记录，登记为UNRESOLVED_SOURCE待核；性状类组仅给BacDive检索URL（GENERIC_SOURCE）。全案无经核实错引（唯一EC条目4.4.1.24与本案无关），severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不cap；按UNRESOLVED_SOURCE“保留低分+待核标记”取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / SUPP:ENZYME:4.4.1.12：官方 ENZYME 记录对 4.4.1.12 标记为 Deleted entry；不支持答案所称 sulfoacetaldehyde lyase 与该 EC 的高置信支持。
- E0_EVIDENCE / SUPP:TAX:1060：官方分类记录：TaxID 1060 为 Rhodobacter 属（rank=genus），不是 Rhodobacter capsulatus 种；不支持答案的种级身份错配声称。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_136：gold 必答步 accepted 酶为 S02 1.1.1.433、S03 4.4.1.38、S01 1.2.1.10/1.1.1.1；EC 4.4.1.12 不在这些必答步 accepted 集合中。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_136：冻结 trait_gold 无 R. capsulatus/TaxID1060 性状行；EVID_003 的 BacDive 搜索 URL 不能绑定到具体性状记录。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案有不确定性说明（氧条件未指定、菌株/基因组不推断，F5/F14为null），但把未核的EC 4.4.1.12和路线关联标为high/medium，且未披露只交付1/3主链；部分披露但部分结论强度超过依据，按5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案有专门的不确定性声明且较具体：明确题面未给氧条件而不外推好氧/厌氧；明确路线级证据不能确定实验菌株、故不下推菌株/保藏号/基因组（F5、F14留null）；逐项给confidence并区分medium/low/unknown。这些属正面披露。不足在于：把单步主链以“路线级证据”与high置信（EVID_001/EVID_002）呈现，未披露该主链与路线常见主链及自身唯一证据粒度之间的冲突；关键酶与TaxID以high/medium包装的未核内容零披露。属单点/局部过度确信而非系统性误导，档内扣分取6，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案明确披露氧条件未指定与菌株/基因组不推断。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.enzyme：答案对未核EC给high confidence；用于披露强度定位。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：gold显示3步主链；答案未披露其单步路线与目标主链的差距。

</details>

## Qwen

答案SHA256：`de03b9e7d1dc9eccf0735da0cb84a003081190f87dae83ba526e4e81b18688d9`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 本题必答主链为3步，答案仅交付1步且产物为sulfoacetate，未构成S02→S03→S01到acetyl-CoA的主链；15项性状仅2项非null。核心任务内容大部缺失，按D1 1–2档取2。

<details><summary>V0.4理由与本行变化背景</summary>

档位3–4：题面指定路线IV的最小完整主链为三步（ordered_step_count=3，终点acetyl-CoA），答案只交付1步、15项性状中13项为null，必要模块大部缺失；且route_scope原样填写路线名却交付与该路线不同的化学走向（首步为氧化，gold首步为还原），属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离，按八.D1判关键错误，cap≤4，取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_136：显示本题gold主链为3步；不直接评价答案化学或替代步骤。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：显示必答有向转化与主产物；不代替评分者判断答案文本。
- ANSWER_TEXT / ANSWER.steps：确认答案只交付1步及该步产物；不证明目标步骤已支持。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> D2允许范围为&#91;1,4&#93;。单步sulfonatoacetaldehyde→sulfoacetate的氧化在局部化学上可成立，但未写辅因子，且不能连接指定路线的S02→S03→S01，主链连续性严重不足；按3–4档取3。

<details><summary>V0.4理由与本行变化背景</summary>

档位3–4：答案首步把醛写成氧化为羧酸（C2H4O4S→C2H4O5S，需外加氧/水与NAD(P)+）却未给任何辅因子与计量，且与题面指定路线IV首步方向相反（gold S02为sulfoacetaldehyde+NADH→isethionate+NAD+，REVERSED_TO_COMPLETE_NAME）；同时以非终点产物sulfoacetate收束，缺S03的C–S裂解与S01的乙酰化，主链不连续。走四.5四步：题面已指定路线、答案未声明替代路线、无可核证据、偏离使该维主要结论失效，故判关键错误cap≤4，取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：显示指定路线的三步转化与终点；不证明答案替代步骤错误。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：显示答案仅给出一步局部氧化，无后续连接。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> D3a的N=3个required目标步均未交付/未匹配；答案唯一给出的EC 1.2.1.81步骤不是S01/S02/S03的accepted酶。虽不是整个酶模块为null（故不记MISSING=1），但目标催化对应几乎为零，按C05 1分。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（取5）：答案以醛脱氢酶类候选（sulfoacetaldehyde dehydrogenase，EC 1.2.1.81）解释磺酸基乙醛→磺基乙酸的氧化，EC大类别（1.2.1.x 醛脱氢酶）与所声称的醛氧化反应类型不矛盾，属合理候选；但E0无该EC冻结记录（GAP-136-003/009），accepted name/reaction/条目状态均无法核验，且未给基因或蛋白标识，关键步骤缺具体核验。按四.6未核即UNRESOLVED，不判虚构、不判矛盾、不计已核实关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_136：显示三个目标步的accepted酶集合；不支持答案EC 1.2.1.81用于这些目标步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：显示目标转化方向与底物/产物；不证明替代步骤化学错误。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：确认答案酶和产物不对应任何目标步。

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> Cupriavidus necator JMP134名称/菌株可辨认，但无反应级或整条路径能力证据；complete_pathway_organism_profile_id=ORG_001构成无支持的整路能力声称。身份单独可核不足以救回微生物推荐，按3–4档取3。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（取5）：Cupriavidus necator 在species级身份上真实（verified_species_name_crosswalk，TaxID 106590，SPECIES_NAME_IDENTITY_ONLY），但答案未给TaxID/保藏号，且无任何反应级证据表明菌株JMP134具有sulfoacetaldehyde dehydrogenase活性或能氧化磺酸基乙醛（GAP-136-030/031无冻结性状/酶记录）；属&#x27;有合理候选、身份与作用范围未充分核验&#x27;。未按身份阶梯降档：不存在经核实的异菌株/跨类群错配；能力声称按自身证据独立评价仍为未核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_136：列出目标步的gold菌与整路菌；未列C. necator不等于证明其不能，只说明无冻结支持。
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_136：仅支持物种名称身份，不支持JMP134菌株的反应/整路能力。
- ANSWER_TEXT / ANSWER.complete_pathway_organism_profile_id：显示答案作出整路菌绑定；无相应能力证据。

</details>

### D4 性状科学性：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 15项性状中13项为null/unknown；F8/F9仅用INTERNAL_KNOWLEDGE_ONLY填写，且是重述非gold反应，不是可核实的菌株性状。缺失主归D1，D4按已给两条无支持性状及关键性状空缺取3。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（取5）：15项字段齐全，13项以value:null+confidence:unknown诚实标注未知（不是编造，完成度问题归D1，不在此重复重扣）；已填2项（F8广义降解能力、F9酶活）实质是复述本答案自身未核的路径声称，指向INTERNAL_KNOWLEDGE_ONLY的EVID_001且confidence=low，无定量数值、无实验条件、无作用范围限定；关键性状证据不足，取5。未按&#x27;预测冒充观测&#x27;判关键错误：两项均标low、未包装为数据库观测，亦无离谱数值或物种级观测被推广为全物种性质。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_136：冻结trait gold无该菌株性状行；absence不等于已证伪。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_136：说明可评分性状/子字段范围；不判答案F8/F9为真。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：确认多数性状未知、仅F8/F9非null且来源为内部知识。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> D5各decision-relevant组仅有INTERNAL_KNOWLEDGE_ONLY的EVID_001，无数据库/文献条目或稳定可核对定位；属MISSING_SOURCE低档，不是已核实错引。低置信披露有利于D6但不提升D5可追溯性。

<details><summary>V0.4理由与本行变化背景</summary>

档位1–2（低分档，取2）：唯一证据条目EVID_001自标source_type=INTERNAL_KNOWLEDGE_ONLY、database与record_id均为null，仅有自由文本locator，无法定位到任何文献/数据库条目或计算记录；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08）全部MISSING_SOURCE，D5主要结论（关键结论可追溯）不成立。MISSING_SOURCE按条款默认不触发关键错误，且本题E0记录与答案声称无claim关联、无经核实的错引，故不cap，取低分2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：确认没有可定位外部来源；只说明来源状态。
- ANSWER_TEXT / ANSWER.route_summary：显示作者自述未核验；不构成外部来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案明确低置信、说明无法在线核验、未知多置null并列出uncertainties，主要限制清楚；但complete_pathway与F8/F9仍以主张形式出现而未完全标为预测/待核。按7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8（取7）：全篇confidence=low/unknown、多数value:null，并明确写出&#x27;未能在线核验&#x27;&#x27;未能确认权威反应方向与微生物归属&#x27;&#x27;多数字段缺乏可核验来源&#x27;，uncertainties列出三条具体待验证点，未把预测包装成观测，来源类型自标INTERNAL_KNOWLEDGE_ONLY——披露与证据强度大体相称。扣分点：仍未披露&#x27;路线名与所交付化学走向不一致&#x27;这一冲突，route_summary以指定路线名陈述内部知识推断，属单点强度略高于依据；未构成系统性误导，不cap，档内取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示作者披露未核验与多数null；不证明科学正确。
- ANSWER_TEXT / ANSWER.route_summary：显示不确定性标注质量。

</details>

## Grok

答案SHA256：`86635eb34c20202fcefe2bf787376bb1e2dd1fa5316b36dd920313b2ec74dadc`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定路线IV要求S02→S03→S01三步并到acetyl-CoA；答案只给一个Xsc裂解步，产物为acetyl phosphate/sulfite，S01/S03缺失且未到指定终点。路线名称虽回显，但主链内容严重偏离；因JSON完整、有酶/菌/性状与限制说明，取2而非1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_136：显示本题gold为3步linear unique路线，ordered_step_count=3；不证明Xsc不能作为另一路线反应。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：显示S02/S03/S01的目标底物-产物与方向；不扩展到未声称步骤。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案只交付一个Xsc裂解步，且未给S01/S03。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Xsc裂解（sulfonatoacetaldehyde + phosphate→acetyl phosphate + sulfite）本身化学可成立，但属替代路线；未连接指定S02/S03/S01，也无到acetyl-CoA的连续性。仅一反应，H+/辅因子标注不完整，合理性证据仅为内部知识；按替代化学质量给5-6档下沿5，不把错路线酶自洽回填D3a。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：显示指定路线IV的目标转化与终点；不证明答案Xsc反应不能作为另一路线存在。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：答案只给出一个Xsc裂解转化，未给出后续连接。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> N=3。S02（KEY_ENTRY）答案给Xsc EC 2.3.3.15，产物acetyl phosphate；accepted S02为sulfoacetaldehyde reductase EC 1.1.1.433，产物isethionate，故为错误目标转化。S01（KEY_TERMINAL）与S03未交付。S=0,F=1,M=2,U=0，C=0→&#91;1,2&#93;；无可用目标催化对应，取1。KEY失败上限4不抬高。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：S02目标为sulfonatoacetaldehyde→isethionate，S01终点acetyl-CoA；支持目标反应身份。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_136：S02 accepted酶为sulfoacetaldehyde reductase EC 1.1.1.433；不证明Xsc对另一反应无活性。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.enzyme：答案将Xsc EC 2.3.3.15绑定到S1，未给S01/S03。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Ruegeria pomeroyi DSS-3为可辨认物种/菌株，答案明确说其只是Xsc相关代表菌、非路线IV指定菌；未给TaxID/保藏号，也无冻结证据证明其催化Xsc或整路能力。未把单步写成整路，故5-6档取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_136：列出本题gold步骤菌；Ruegeria不在其中，但不证明其永不适用于替代路线。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.microorganism：答案交付Ruegeria pomeroyi DSS-3并自述未确认路线IV指定菌。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项全出现；filled=8、explicit_unknown=7、omitted=0。温度/pH/盐度数值、保藏、基因组、部分酶活/运动性为null；已给好氧、海洋盐度类别、DMSP/有机硫、杆状、革兰氏阴性、不产孢等与身份相符但仅内部知识，无E0/gold条目可核。部分性状可用但关键项证据不足，5-6档取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：显示答案交付了15项性状及8项有值/7项明确null；不证明这些值已被外部记录核验。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_136：本题gold有若干步级菌株性状，但无Ruegeria pomeroyi DSS-3行；不能据此核验其具体值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> EVID_001/002均为INTERNAL_KNOWLEDGE_ONLY，无DOI、数据库record_id或可定位条目；关键路线/酶/菌/性状组均MISSING_SOURCE，无已核实错引，severity不适用。来源缺失不是虚构，但几乎无法定位重要结论依据，1-2档取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示两条证据的source_type均为INTERNAL_KNOWLEDGE_ONLY、database/record_id为null；不证明其内容。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确区分内部知识、低/中置信、null未知，列路线IV未核、菌株非指定、无TaxID/保藏/基因组；限制与冲突说明充分。仅Xsc“公开文献可核定”及个别Gram/产孢high confidence略强于内部知识来源，整体仍属7-8档，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案明确列出路线IV、菌株、TaxID、性状数值等未知与限制；不证明其科学结论正确。

</details>

## GPT5.6

答案SHA256：`389d27cd409d5fa9f39f722ba14ea1b264dbe341a80b455d5a8039299bb531d1`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The task requires the three-step sulfoacetaldehyde degradation IV main chain to acetyl-CoA plus 15 traits. The answer supplies only one alternative step to acetyl phosphate, omits two required gold steps, and provides no trait values. This is a severe task-route deviation and major incompleteness, in the D1 &#91;1,4&#93; range; 2 reflects that the answer is coherent but does not cover the required main route or traits.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：Shows the required S02, S03, S01 reactions and terminal acetyl-CoA; does not support the answer&#x27;s acetyl phosphate shunt as the specified route.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_136：Shows LINEAR_UNIQUE ordered_step_count=3 and the case identity; not a denominator for every branch.

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The single sulfonatoacetaldehyde→acetyl phosphate shunt is internally plausible as a different transformation, but it does not build the specified main chain: isethionate, acetaldehyde, and acetyl-CoA continuity are absent. In the D2 &#91;1,6&#93; range, 4 reflects one chemically recognizable alternative step but no task-route backbone.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：Shows the gold main-chain intermediates and terminal acetyl-CoA; the answer&#x27;s acetyl phosphate product is not the S02 product.

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> No required target step receives target credit: S01 and S03 are missing, and the sole delivered step is mapped to S02 as a product-foreign transformation (acetyl phosphate instead of isethionate) using EC 2.3.1.57, which is not the accepted S02 EC 1.1.1.433. Even treating the S02 enzyme/EC identity as locally unresolved, the product mismatch blocks target credit. S=0 gives the &#91;1,2&#93; band; choose 1 because there is no usable target catalytic correspondence.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_136：Lists accepted enzyme/EC records for S01–S03; EC 2.3.1.57 is not an accepted S02 enzyme record.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_136：Shows S02 target product is 2-Hydroxyethanesulfonate, not acetyl phosphate.

</details>

### D3b 微生物身份与能力：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer gives Paracoccus pantotrophus without strain or TaxID, and provides no step-level or whole-path capability evidence. It also sets complete_pathway_organism_profile_id although only one alternative step is present. This is a candidate-level microorganism claim with missing identity/capability support, in the 3–4 band; choose 3 because no capability evidence supports the correspondence.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_136：Lists gold step organisms and pathway-complete organisms for this case; Paracoccus pantotrophus is not present. Absence is not proof that the species is false.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 required trait fields are delivered only as null/unknown values. Under the rubric&#x27;s all-null trait rule, D4 is MISSING=1; no scientific error is asserted, but there is no evaluable trait value or source.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_136：Shows available trait records for gold organisms; not used to fill the answer&#x27;s missing traits.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_136：Shows trait scoreability structure; the answer supplies no trait values to compare.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Both evidence_registry entries are INTERNAL_KNOWLEDGE_ONLY; EVID_001 gives only an EC number/locator and EVID_002 gives no database or locator. Core route, enzyme, and organism claims therefore have no externally traceable source. This falls in the 1–2 band (almost no important conclusion is locatable); no verified mis-citation exists, so no cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows both delivered evidence entries are internal-knowledge-only and lack external traceable locators.

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer explicitly lists major unknowns (strain, collection/genome, 15 traits, oxygen/electron acceptor) and labels evidence as INTERNAL_KNOWLEDGE_ONLY. However, it assigns medium confidence to the enzyme/organism and sets complete_pathway_organism_profile_id for a one-step alternative, so confidence and scope exceed support. This is within the 5–6 band.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows the answer discloses missing strain, traits, and oxygen/electron-acceptor uncertainty.
- ANSWER_TEXT / ANSWER.evidence_registry：Shows the answer labels both evidence entries as INTERNAL_KNOWLEDGE_ONLY.

</details>
