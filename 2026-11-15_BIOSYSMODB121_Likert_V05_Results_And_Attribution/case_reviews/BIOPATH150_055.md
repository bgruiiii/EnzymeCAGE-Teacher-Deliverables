# BIOPATH150_055：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：catechol degradation to 2-hydroxypentadienoate II

污染物：Catechol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 74.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 50 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 62 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 56.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 64 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 36.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`67b58451cb9623d36cab76872f750e3d7563ec35f6f252ccb9ad2a64fdcb88b9`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 四条必答主链步骤均给出底物/产物/SMILES、首选酶/EC和对应微生物；同一菌去重为ORG_001；route_scope.chosen_route_name原样填写；15项性状键齐全并如实null。仅少量表达/工程小缺陷，D1按9档。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求逐项核对：route_scope.chosen_route_name 原样回填题面路线名；氧条件 null 照填；4 步主链（S1–S4）每步均给主底物/主产物英文名+SMILES、一个首选酶含 EC、一个对应微生物并以 ORG_001 统一引用，满足“同一菌去重”；15 项性状字段全部出现（12 项实质填写、3 项明确未知、0 遗漏），未知项按题面要求填 null 而非占位；evidence_registry 4 条、uncertainties 5 条。全部适用要求均被实质回应，无重要模块遗漏或范围偏离，仅属交付完整性高档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_055_question：题面要求主链、逐步酶/EC/菌、15项性状并锁定路线名。
- ANSWER_TEXT / ANSWER:BIOPATH150_055：答案含4步、每步酶/EC/菌及15项性状，路线名原样。
- GOLD_SLICE / formal_cases.tsv：gold为LINEAR_UNIQUE 4步；D-M01不以全DAG旁支作缺步分母。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 主链化学顺序为catechol→2-hydroxymuconate semialdehyde→2-hydroxymuconate→4-oxalocrotonate→2-hydroxypentadienoate，方向、碳骨架连接、脱羧终点与gold一致；O2、NAD+/NADH、H2O、CO2等关键辅因子在列。局部未标H+和立体/电荷表示，但不改变主结论，D2按9档。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与 gold 线性主链逐步一致：catechol(+O2)→2-hydroxymuconate semialdehyde→2-hydroxymuconate(+NADH)→4-oxalocrotonate→2-hydroxypentadienoate(+CO2)，起止点与题面指定终点吻合，方向均为底物→产物，碳数（6→6→6→5+CO2）与氧化还原衔接成立，无起始步错误、无无依据跳步、无原子明显不守恒。O2、NAD+、H2O、NADH、CO2 均在列；仅 S2/S4 未列 H+ 且各中间物 SMILES 未标 E/Z——按辅因子与简化反应式条款属局部计量/表达缺陷，D2 在 7–8 档以上处理、不自动 cap；alternative_branches 的水解分支显式标注 is_part_of_scored_main_route=false，downstream_continuation 声明不参与主链评分，范围边界清楚。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;EXPLICIT_PROGRAM_CAP_APPLIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:BIOPATH150_055：答案给出四步转化、方向、辅因子和终点。
- GOLD_SLICE / reaction_gold.tsv：gold逐步反应支持同一主链的底物-产物与方向；不证明具体蛋白实验活性。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 原始N=4，四步均交付了首选酶名与EC，无整模块缺失M。程序侧四目标均为ROUTE_HOLD_REPRESENTATION/UNRESOLVED，属于表示等价待裁定，不是已确认催化失败，也不自动构成本维NE。按现有材料逐目标核对：答案S1的catechol 2,3-dioxygenase/EC 1.13.11.2、S3的4-oxalocrotonate tautomerase/EC 5.3.2.6、S4的4-oxalocrotonate decarboxylase/EC 4.1.1.77与gold accepted集合相应步骤一致；S2的2-hydroxymuconate semialdehyde dehydrogenase/EC 1.2.1.61与gold/accepted S03的EC 1.2.1.85不一致，但现有冻结材料未给出该EC催化失败证明，故只登记待核，不判F。因四目标均KEY/MAJOR且表示边界未决，按C05不能进入7–8档，取5–6档上沿6：多数酶-反应对应清楚，仍有一个显式EC配对和整体表示边界妨碍进入良好档。未发现可确认的关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶-反应对应整体成立：S1 catechol 2,3-dioxygenase/EC 1.13.11.2（双加氧、间位裂解）、S3 4-oxalocrotonate tautomerase/EC 5.3.2.6（酮-烯醇异构）、S4 4-oxalocrotonate decarboxylase/EC 4.1.1.77（脱羧）均与 gold 主链酶及反应类型一致，酶名与 EC 类别无互相矛盾；xylE 标注与所声称酶一致。唯一实质待核点是 S2 填 EC 1.2.1.61 而 gold 为 1.2.1.85（同一 2-hydroxymuconate semialdehyde 脱氢反应）：冻结证据快照中无任何 EC 条目（item_gaps GAP-055-004），按四.5/gold 具体号冲突保守条款记 UNRESOLVED、保留待核，不判错、不 cap，D3a 在 7 档取分（主要步骤可靠支持、少量条目需进一步确认），未达 9–10 档所要求的“关键步骤酶对应均有充分且适用的支持”。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;S1-S4&#93;.enzyme：答案交付的四步首选酶名与EC；仅用于逐目标核对，不等于具体蛋白实验活性证据
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：gold S01/S02/S03/S04目标酶名/EC为5.3.2.6、4.1.1.77、1.2.1.85、1.13.11.2；属数据库策展粒度，不证明任意具体蛋白底物谱或实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：目标反应底物/产物与方向；支持目标反应身份核对，不证明任意具体酶活性
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_055：ordered_step_count=4且LINEAR_UNIQUE，仅支持任务链形态，不单独证明酶对应正确

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 核心微生物写成Pseudomonas putida mt-2，profile给出TaxID 303；E0的TaxID 303为官方Pseudomonas putida种级记录，BacDive 12880为mt-2 PaW1/pWWO菌株记录；gold organism表也把P. putida与各步及PATHWAY_COMPLETE关联。菌株级逐酶分布仍有文献未冻结的局部待核，但不推翻主要微生物推荐，D3b按8档。

<details><summary>V0.4理由与本行变化背景</summary>

核心微生物推荐为 Pseudomonas putida mt-2（TOL 质粒 pWW0），身份要素真实且可部分核验：E0 BacDive 12880 为“mt-2 PaW1, pWWO”菌株记录（type strain=no），其 ncbi_taxid_block 指向 species 级 TaxID 303，与答案 profile 填写的 303 一致；TaxID 303 官方记录支持物种名精确匹配。但菌株级身份关联为 UNRESOLVED（STRAIN_TOKEN_NOT_IN_RECORD_NAMES），答案亦自述“mt-2 株级 NCBI TaxID 未能确证，仅填物种级 303”，属身份阶梯①粒度不足→档内扣分、默认不 cap。能力层面：四步均归同一 ORG_001，所引 EVID_004（Worsey &amp; Williams 1975，TOL 质粒介导儿茶酚间位裂解）方向支持但 E0 无该文献记录（GAP-055-023），完整路径能力声称 CG09 在 E0 为 UNRESOLVED；未见用另一菌株编号顶替、未见由序列存在性直接推断整条路径。主要微生物推荐未被已核实证据推翻，故不触发 cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：官方记录支持Pseudomonas putida种名、rank与current状态；不支持菌株级酶活或整路能力。
- E0_EVIDENCE / f3e0:bacdive:12880：记录支持mt-2 PaW1/pWWO菌株身份、保藏号和26/30°C培养记录；培养温度不等于最适，也不证明具体酶活。
- GOLD_SLICE / organism_gold.tsv：gold把P. putida 303与各步及PATHWAY_COMPLETE关联；这是物种级关联，不自动细化到mt-2逐酶实验。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 15项键齐全并大量明确null；F2偏好中温、F4非嗜盐、F10运动、F11杆状、F12革兰氏阴性、F13不产芽孢与gold大体相符。F1“专性好氧”较gold的aerotolerant记录略强；F7-F9的TOL质粒/间位裂解酶表述方向合理但E0未冻结；温度、pH、盐度数值、保藏号、基因组等关键数值缺。D4按7档：主要定性性状可核，关键数值/条件证据有限。

<details><summary>V0.4理由与本行变化背景</summary>

按 TaxID 303 的可评分性状逐项比对：F2 preference=中温性（gold temperature preference=mesophilic，OBSERVED）一致；F4 category=非嗜盐（gold salinity preference=non-halophilic）一致；F6 好氧呼吸/O2（gold respiration: nitrate=false、denitrification 各项 false）方向一致；F10 运动、F11 杆状、F12 革兰氏阴性、F13 不产芽孢均与 gold 观测一致。温度/pH/盐度上下限、保藏号（答案 F5=null，而 E0 12880 已给出 DSM 3931/ATCC 33015/CCUG 2480 等）、基因组号（F14=null）大量诚实留空——按 D4 条款，缺失的完成度扣分主归 D1，D4 只按已给内容与关键缺口评定，不与编造混同。F1 写“专性好氧”而冻结观测标签为 aerotolerant=true，属表述层面的标签差异，尚不构成数值离谱或把种级观测推广到全菌株的误读；F7/F8/F9 的甲苯/二甲苯及芳香族降解能力有文献方向依据但来源待核。综合：主要性状可核实且适用于所指对象，仅少量条件/数值与来源问题，未触及关键错误（无预测冒充观测、无把特定观测推广为普遍耐受范围）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：支持P. putida多项定性性状及部分温度/盐度/pH观测；不证明mt-2全部性状或最适值。
- GOLD_SLICE / trait_scoreability_mask.tsv：标示F2/F4等子字段的待裁定/仅完整性角色，提醒不能把范围端点自动当最适或上下限。
- E0_EVIDENCE / f3e0:bacdive:12880：支持mt-2 26/30°C培养记录和保藏号；培养温度不等于最适，不支持所有性状。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出具体定位：S1有UniProtKB P23259，菌株/部分性状有Worsey &amp; Williams 1975文献，且claim_scope与步骤有对应；但S2-S4仅INTERNAL_KNOWLEDGE_ONLY，EVID_001和EVID_004在E0无冻结记录，均为UNRESOLVED_SOURCE，S2-S4为MISSING_SOURCE。按DECISION_RELEVANT组混合MISSING/UNRESOLVED，无VERIFIED_MIS_CITATION，不cap；因部分关键结论可定位但核对不足、其他核心步缺来源，D5按5档。

<details><summary>V0.4理由与本行变化背景</summary>

按 claim group 登记后合成：决策相关组中，CG07 身份有官方 TaxID 名称匹配的正向支持（该支持登记于事实核验层，不回填来源状态），CG01/CG05 的 S1 引具体条目 EVID_001（UniProtKB P23259）但 E0 无该记录（GAP-055-001）→UNRESOLVED_SOURCE；S2–S4 反应与酶仅 EVID_003 且 source_type=INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE；CG03 终点亦仅内部知识；CG09 完整路径能力在 E0 为 UNRESOLVED；CG14 的底物/降解能力引 EVID_004 真实文献方向但 E0 无记录（GAP-055-023）→UNRESOLVED_SOURCE。全案未出现经核实的不存在/不支持引用，无 VERIFIED_MIS_CITATION_*，故不触发 cap（P37/P167）。档位方面：既非“全部仅有笼统来源”（答案用了具体记录号与具体文献，非裸库名），也非“全部缺失”；存在部分条目级可定位材料但核心反应证据链大量映射缺失，落在 5–6 档“部分关键结论可定位并核对，其他模块仍缺映射”的下半，取 5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:BIOPATH150_055：答案只交付了这些来源记录和claim_scope；不把E0外部记录视为模型原证据。
- GOLD_SLICE / enzyme_gold.tsv：gold可用于核对accepted酶列，但不把gold回填成答案已交付来源。

</details>

### D6 不确定性与诚实度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案明确区分DATABASE_DIRECT、LITERATURE_DIRECT与INTERNAL_KNOWLEDGE_ONLY，逐项标low/medium/unknown，并列出TaxID未确证、基因名未确证、性状通用知识、SMILES立体缺失等限制；没有把预测系统性写成实证，也没有掩盖主要矛盾。个别置信标签偏强但不构成系统性误导，D6按9档。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体好：uncertainties 逐条列出路线编号解读歧义（II 号为氧化分支、并列水解分支）、株级 TaxID 未确证、S3/S4 基因名未确证、15 项性状主要依据通用知识且数值未知、SMILES 立体化学未标；alternative_branches 显式标注 is_part_of_scored_main_route=false，downstream_continuation 与 central_metabolism_entry 均声明属路线范围外不参与评分；多数字段 confidence 标 medium/low/unknown，与 INTERNAL_KNOWLEDGE_ONLY 来源相称，未知项填 null 而非填充。不足：EVID_001 以 DATABASE_DIRECT+high confidence 承载一个 E0 无法核验的条目，且 S1 酶/宿主身份未标“建议复核”；F1“专性好氧”未说明与冻结观测标签（aerotolerant）的差异。属单点过度确信、非系统性把预测写成实证，按 P119/P169 档内扣分不 cap。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER:BIOPATH150_055：答案自身披露证据类型、未知、null和限制。
- RUBRIC_CLAUSE / P119-P121：区分单点过度确信与系统性误导；D5错引不自动连坐D6。

</details>

## DeepSeek

答案SHA256：`31f96e7b4de8fb162e88b6ae5aff92f28688c9b7641d45b7de2c1f32dd418cec`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> 答案只给出2步：S1为catechol 2,3-双加氧酶开环生成2-hydroxymuconate semialdehyde，对应金标S04入口；S2用水解酶直接生成2-hydroxypentadienoate II和formate，是水解支路。题面锁定的4步主链还要求S03脱氢酶、S01 tautomerase、S02 decarboxylase，答案均未交付；虽保留了入口和终点，但核心主链大部缺失并改走替代支路，属严重任务偏离。

<details><summary>V0.4理由与本行变化背景</summary>

答案各模块表面齐全，且route_scope原样回显题面路线名；但gold显示题面指定路线II为4步氧化主链，答案实际交付2步水解分支（HMSH直接生成terminal+formate），未声明为替代路线，属自称合规而交付不同化学路线的任务参数偏离，触发D1关键错误cap≤4；其余模块完整，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_055：ordered_step_count=4、LINEAR_UNIQUE，给出本题4步必答主链的任务规模。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：列出金标主链S04（catechol→2-hydroxy-6-oxohexa-2,4-dienoate）、S03（脱氢酶至2-hydroxyhexa-2,4-dienedioate）、S01（tautomerase至2-oxohex-3-enedioate）、S02（decarboxylase至terminal 2-hydroxypenta-2,4-dienoate）；不把答案的水解支路列为预登记主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_055：定义污染物catechol与终点(2Z)-2-hydroxypenta-2,4-dienoate的身份。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：列出S01-S04所需接受的酶/EC；显示答案缺失脱氢酶、tautomerase与decarboxylase步骤。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 按所答化学独立评价：S1 catechol + O2 → 2-hydroxymuconate semialdehyde，为已知meta-cleavage开环，方向正确；S2 semialdehyde + H2O → 2-hydroxypentadienoate II + formate，主碳骨架连续且计量框架可解释，属已知水解支路。未发现反向、明显不守恒或跳跃至中心代谢物；但该两步水解支路不是金标指定的脱氢酶/tautomerase/脱羧酶主链，答案也未说明其为替代支路，未列质子/电荷细节属局部表达问题，故不能取9-10，落在7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

第一步catechol经catechol 2,3-dioxygenase EC 1.13.11.2开环生成2-hydroxymuconate semialdehyde，与gold一致；第二步HMSH水解生成2-hydroxypentadienoate II与formate，碳数与氧化还原计量可成立，属已知水解分支，化学连续性合理。与题面指定II路线的符合性问题已归D1，不在此重复cap；但该分支未声明、EC未核，故不给更高。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：金标S04入口反应与答案S1化学对应（catechol + O2 → 2-hydroxy-6-oxohexa-2,4-dienoate）；金标S03/S01/S02显示指定脱氢酶/tautomerase/脱羧酶主链，而非答案S2水解支路。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_055：确证污染物catechol与终点(2Z)-2-hydroxypenta-2,4-dienoate身份，支持答案方向指向题面终点。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：列出金标主链接受酶/EC；支持S04中的catechol 2,3-dioxygenase EC 1.13.11.2，但未把EC 3.7.1.20水解酶列为金标必答步骤。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 人工判读：S04 入口目标可由答案 S1 支持（catechol 2,3-dioxygenase，EC 1.13.11.2，catechol→2-hydroxymuconate semialdehyde）；S03、S01、S02 的指定目标反应未交付，答案 S2 是水解酶支路到 terminal+formate，不能回填 S03/S01/S02 目标信用。按 S=1、M=3、U=0 计 C=1/4=0.25，落入&#91;3,4&#93;；因仅入口步可用且 terminal 目标步缺失，取 3。程序矩阵的 UNRESOLVED 事实仍原样回显，不据此伪造已支持。

<details><summary>V0.4理由与本行变化背景</summary>

第一步catechol 2,3-dioxygenase EC 1.13.11.2与gold的酶-反应对应一致，支持较强；第二步酶名2-hydroxymuconate semialdehyde hydrolase与水解反应类型相符，但EC 3.7.1.20在E0无冻结记录，不能核实accepted name/reaction。按7档：主要步骤有支持，仅第二步EC需进一步确认。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：支持 S04 的 catechol 2,3-dioxygenase/EC 1.13.11.2 接受集，以及 S01/S02/S03 的目标酶集合；不支持将 3.7.1.20 hydrolase 支路回填为 S03 目标反应。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：支持四步有序主链与各步底物/产物；用于判定 S03/S01/S02 目标反应在答案中缺失。
- ANSWER_TEXT / ANSWER_TEXT：定位答案 S1 的入口匹配与 S2 的替代支路；不把替代支路计为目标步信用。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> P. putida mt-2 的身份由 E0 BacDive 12880（strain mt-2 PaW1/pWWO，TaxID 303）支持；gold organism_gold 也接受 P. putida 作为相关步骤的物种级微生物。菌株级 hydrolase 反应能力与“完整路径 mt-2”仍缺直接粒度证据，按身份可靠、具体能力需确认取 7，不触发 cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案两步均用Pseudomonas putida mt-2，未把单步菌写成完整路径菌；E0 bacdive 12880支持mt-2 PaW1/pWWO菌株记录，TaxID 303支持种级身份。第一步C23O与P. putida的对应有gold支持；第二步HMSH活性在mt-2中的具体步级能力未在E0核实。按7档：身份可靠，少量具体能力待确认。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持 P. putida mt-2 PaW1/pWWO 菌株记录与 TaxID 303；不支持直接证明该株完成指定四步路径或具有所述 hydrolase 活性。
- E0_EVIDENCE / f3e0:taxid:303：支持 Pseudomonas putida 的官方分类名与当前状态；不自动支持菌株级催化或全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_055：支持 P. putida 在相关目标步骤的物种级接受记录及 PATHWAY_COMPLETE 物种级记录；菌株级外推仍需独立证据。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 已填性状中 Gram-negative、rod-shaped、motile、non-sporulating 等可由 trait_gold 的 P. putida 物种级观测支持；部分具体碳源/降解/酶活/栖息地表述为物种级或常识性概括，未在冻结性状表中逐项核到菌株级。数值型温度/pH/盐度等未填并明确 null，不当作错误；整体按主要性状可核、少量具体项待确认取 7。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状多数基础项与gold一致：F10运动性、F11杆状、F12革兰氏阴性、F13不产孢均有trait_gold支持；F1/F6的需氧描述对P. putida合理。F7/F8/F9的底物利用与酶活、F15栖息地描述为合理但E0未核。F2/F3/F4/F5/F14以null/unknown如实留空，未编造数值。按7档：主要性状可核实且适用，关键降解性状仍需补证。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_055：支持 P. putida 物种级形态、运动性、革兰氏、产孢等观测；不支持把物种级记录全部外推为 mt-2 菌株级定量性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_055：标明哪些性状可作观测准确度、哪些仅为 completeness；用于避免把 null 或不可评分项当作错误。
- ANSWER_TEXT / ANSWER_TEXT：定位答案已填与明确未知的性状；未填项只作完成度信息，不伪造成科学错误。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 答案 evidence_registry 仅有 EVID_001/EVID_002，二者 source_type 均为 INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 全为 null；路径、酶、菌、性状的关键结论均无可定位外部来源。按 D5 的 MISSING_SOURCE 低分档取 1；这是来源缺失，不是已核实错引，不触发 D5 cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案的evidence_registry两条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全空，无法沿具体文献、数据库条目或计算记录追查任何路径、酶、菌或性状结论；决策相关CORE/APPLICATION_CRITICAL组均为MISSING_SOURCE。未发现经核实的错引，故不触发错引cap；按MISSING_SOURCE低分档取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：仅支持答案实际交付的来源登记为 INTERNAL_KNOWLEDGE_ONLY，且无外部数据库/记录定位；不支持任何外部可追溯性。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案对缺失性状使用 null/unknown，属于诚实未知；但 evidence_registry 明确只有内部知识仍以 medium/high confidence 包装，uncertainties 为空，且未说明两步 hydrolase 支路相对指定主链的替代性/边界。存在部分不确定性标注，但主要限制说明不足，取 5。

<details><summary>V0.4理由与本行变化背景</summary>

答案以confidence字段和null区分部分未知，未把未知项编造成数值；但未说明主要限制、未区分内部知识与可观测/预测证据，且对第二步酶和多项性状给medium置信却无可定位依据，个别关键步骤标high。属有不确定性说明但较笼统、部分结论强度略超依据，未达系统性误导cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：支持答案使用内部知识来源、confidence 标签与空 uncertainties；不支持把内部知识表述为已核实验观测。

</details>

## Kimi

答案SHA256：`612a9989f0e3d41175d369422cf3af0d05838cb564e2b1fa590491434267a2d0`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 答案覆盖路径、酶、微生物、15项性状与来源，格式可读；但题面锁定路线为 catechol degradation to 2-hydroxypentadienoate II，指定主链按gold为4步（S04儿茶酚2,3-双加氧酶→S03半醛脱氢酶→S01 tautomerase→S02 decarboxylase）。答案主链只给2步，并在S2用2-hydroxymuconate-semialdehyde hydrolase (EC 3.7.1.9)直接生成终点和甲酸，属于水解支路而非指定的脱氢支路；答案自己在uncertainties也承认若II为脱氢支路则应为4步。故交付了不同化学主链，缺指定必经步，D1任务符合度关键错误成立，按≤4记4：模块和部分内容仍可读，入口反应/终点可辨，但核心路线不符。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的路径、逐步酶+EC、对应微生物、15项性状、来源与不确定性均实质交付；route_scope.chosen_route_name原样填写题面路线名。唯一疑点是主链选用水解支路（与gold route II的脱氢支路不同），但答案已显式声明I/II命名歧义并将脱氢支路列入alternative_branches，属已披露解释而非隐瞒偏离，故不判D1关键错误；扣分限于路线解释风险。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_055：确认该题gold为LINEAR_UNIQUE且ordered_step_count=4，支持题面路线II需要4步有序主链，而非答案的2步主链。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：列出指定路线S01-S04的酶/EC：S04 catechol 2,3-dioxygenase 1.13.11.2；S03 2-hydroxymuconate semialdehyde dehydrogenase 1.2.1.85；S01 tautomerase 5.3.2.6；S02 2-oxo-3-hexenedioate decarboxylase 4.1.1.77；未将2-hydroxymuconate-semialdehyde hydrolase 3.7.1.9列为该主链步骤。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：给出S04→S03→S01→S02的连续反应序列与终点(2Z)-2-hydroxypenta-2,4-dienoate；支持D1判断答案缺少指定主链的脱氢/tautomerase/decarboxylase步骤。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 所答两步化学自身连贯：S1 catechol+O2→2-hydroxymuconate semialdehyde用EC 1.13.11.2，符合meta-裂解入口；S2 semialdehyde+H2O→2-hydroxypentadienoate+formate用EC 3.7.1.9，属可辨认水解支路，底物/产物连续、终点与gold terminal一致，辅因子水/氧已列出。未发现主链方向反转、原子明显不守恒或无依据跳步。它和题面指定II的脱氢支路不同，但该任务路线偏离已在D1按任务符合度处理，D2按C00/P60只评所答化学自身质量，不用替代内容回填目标完成。D2 9-10程序门未开且本题nine_ten_eligible&#91;D2&#93;=false，最高给8；局部未核EC/基因注释和立体化学未细化，扣至8。

<details><summary>V0.4理由与本行变化背景</summary>

S1儿茶酚经儿茶酚2,3-双加氧酶外二醇开环生成2-羟基黏康酸半醛；S2经EC 3.7.1.9水解去甲酰化生成2-羟基-2,4-戊二烯酸并释放甲酸。方向、结构与终点均正确，符合meta-裂解化学。主链取水解支路（gold route II为经EC 1.2.1.85/5.3.2.6/4.1.1.77的脱氢支路），属已声明替代路线且止于题面同一终点，化学合理、未推翻主要结论，四步判断后不作cap，档内取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：支持核对S1入口反应catechol+dioxygen与终点(2Z)-2-hydroxypenta-2,4-dienoate；不单独验证答案S2的水解酶EC 3.7.1.9支路。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_055：确认根化合物Catechol与终点(2Z)-2-hydroxypenta-2,4-dienoate的身份，支持终点对应判断；不扩展到替代支路酶归属。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> D3a band &#91;3,4&#93; under C04. Manual review finds one supported target: S04 entry catechol 2,3-dioxygenase EC 1.13.11.2 with the expected extradiol-cleavage product. S03 is mismatched: answer uses hydrolase EC 3.7.1.9, while the accepted S03 enzyme set is dehydrogenase EC 1.2.1.85. S01 tautomerase and S02 terminal decarboxylase are undelivered. Only one of four required targets has usable target credit; key terminal/intermediate missing, so score 3.

<details><summary>V0.4理由与本行变化背景</summary>

S1儿茶酚2,3-双加氧酶EC 1.13.11.2与反应类型匹配（gold enzyme_gold与organism_gold均列EC 1.13.11.2 catechol 2,3-dioxygenase）；S2 2-羟基黏康酸半醛水解酶EC 3.7.1.9属该水解支路的真实酶，但E0无EC 3.7.1.9冻结记录（GAP-055-006/015），保持待核。核心酶对应可靠、仅一条待核，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：Accepted enzyme names/EC for S01-S04; supports S04 match and identifies S03/S01/S02 required enzymes; not specific protein activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：Gold reaction direction and substrate/product relations for S01-S04.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> P. putida mt-2 is a plausible and partly supported step microorganism: E0 has a P. putida mt-2 strain record and gold supports P. putida species-level pathway completeness. However taxid 340177 is not verified in E0, and whole-pathway capability at strain level is not fully established. This supports 7, not 8.

<details><summary>V0.4理由与本行变化背景</summary>

推荐Pseudomonas putida mt-2作为两步对应菌；gold organism_gold显示P. putida(taxid 303)可支持S01/S04步骤，物种级身份成立。E0 bacdive:12880记录为mt-2 PaW1(pWWO)、species级taxid 303；答案profile taxid 340177无冻结记录（GAP-055-026/027），粒度为菌株级且未核，不判错误也不判cap。属身份粒度/待核，档内取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：Supports a Pseudomonas putida mt-2 PaW1(pWWO) strain record and culture collection context; does not verify taxid 340177 or full pathway capability.
- E0_EVIDENCE / f3e0:taxid:303：Supports the species name Pseudomonas putida at taxid 303; does not verify the answer&#x27;s taxid 340177.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_055：Gold step assignments include Pseudomonas putida and species-level PATHWAY_COMPLETE for taxid 303; not a strain-level mt-2 verification.

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Most filled traits align with gold P. putida data: mesophilic preference, pH 7.0 growth, motility, rod-shaped, Gram-negative, non-sporulating, and aromatic degradation. Nulls for salinity, culture collection, and genome are explicit unknowns rather than fabricated values. The exact 30°C optimum and strict-aerobe label are not directly frozen, so 7 rather than 8.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全；F10有运动、F11杆状、F12革兰氏阴性、F13不产孢、F6好氧呼吸O2与gold物种记录一致（motility=true, rod-shaped, gram negative, sporulation=false）；F2最适30°C、F3最适pH7与物种记录（温度25-37、pH 7）相容；F4/F5/F14诚实null。弱点：多数性状以INTERNAL_KNOWLEDGE_ONLY按菌株级交付（物种级泛化到mt-2），F1&#x27;严格好氧&#x27;相对gold&#x27;aerotolerant&#x27;略过强。取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_055：P. putida species-level trait records for temperature range, pH, motility, morphology, Gram, sporulation, carbon source, and degradation; not strain-specific mt-2.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_055：Marks which trait fields are scoreable and which are completeness-only; used to avoid treating missing observations as errors.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_055：Shows observed scalar subfields versus pending/range fields, especially temperature and salinity.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Core route/enzyme/microbe conclusions have at least a named MetaCyc pathway page and a full literature citation, but EVID_001 lacks a record_id/stable locator and EVID_002 is not E0-verified. Traits rely heavily on EVID_003 internal knowledge only. No verified mis-citation is available, so this is partial traceability at 5, not a cap.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组：CG01/02/03路线用EVID_001（MetaCyc pathway page，record_id null）→GENERIC_SOURCE；CG05酶用EVID_001+E0无EC记录→GENERIC/UNRESOLVED；CG07/08微生物用EVID_002（Assinder&amp;Williams1990完整题录，可定位）但E0自由文本未核→UNRESOLVED_SOURCE；性状多INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE。存在可定位条目级文献题录与具体pathway页名，但无record级可核对证据、taxid无记录，落5-6档取5。无已核实错引，severity=NOT_APPLICABLE，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows the delivered source records and claim_scope assignments; not external verification of those sources.
- E0_EVIDENCE / f3e0:taxid:303：Supports only the species name Pseudomonas putida; does not verify the answer&#x27;s EVID_001/EVID_002 citations.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> The answer clearly discloses the main MetaCyc route-I/II naming uncertainty, marks unconfirmed strain collection/genome fields as null, and uses confidence labels. Some internal-knowledge traits are given medium/high confidence, but this is not systemic misrepresentation. Good disclosure and boundaries support 8.

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties两条具体披露（I/II命名歧义与替代支路；mt-2保藏号/基因组未确认、拒绝用KT2440回填），F4/F5/F14诚实null并标unknown，披露质量良好。弱点：F12革兰氏阴性/F7/F8/F9等在INTERNAL_KNOWLEDGE_ONLY或单篇文献下标high，属单点过度确信而非系统性误导；档内扣、不cap，取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit uncertainty about route-I/II and strain collection/genome data; not external verification.

</details>

## Qwen

答案SHA256：`5717caf8fcf38dc852e77a02740f4f7e750e40b688c5c142342ca8098939bdf1`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 任务合同要求的 route II 主链有四步（S04→S03→S01→S02）；答案只给出两步：儿茶酚经 catechol 2,3-dioxygenase 到 2-hydroxymuconate semialdehyde，再经 hydrolase 直接到 2-hydroxypenta-2,4-dienoate。该写法绕过了脱氢酶、 tautomerase 与 decarboxylase 三个必答目标步，且 15 项性状仅 3 项填写、12 项显式未知。虽有正确入口与终点，但主链模块缺失严重，属路线/任务偏离，按 D1 低档且关键错误上界≤4；取3。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖登记：路径仅2步（题面指定路线II在gold中为4步）、酶2步、菌1株、性状3/15有值+12项明确未知、来源部分、不确定性已给。答案route_scope原样填写路线名，但第2步以2-hydroxymuconate-semialdehyde hydrolase(EC 3.7.1.9)一步替代gold路线II的脱氢酶/tautomerase/脱羧酶序列，且未声明为替代分支，属P100‘自称合规却交付不同化学路线’的任务参数偏离（关键错误）。档内：各模块均有涉及、结构完整、首步化学正确，取3–4档上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：显示 route II 的必需四步顺序；不支持把两步 hydrolase 捷径当作 route II。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：列出 route II 各步可接受酶；不证明答案已交付这些步骤。
- ANSWER_TEXT / ANSWER.steps：答案实际只交付两步 hydrolase 分支；未交付 S03/S01/S02 的酶与反应。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 按答案自身化学评价：S1 为 catechol 2,3-dioxygenase 催化的儿茶酚开环，生成 2-hydroxymuconate semialdehyde；S2 为 hydrolase 催化的水解，生成 2-hydroxypenta-2,4-dienoate 与 formate。两步方向、主产物与辅底物（O2、H2O）清楚，终点正确，属化学上可成立的分支。但它不是题面 route II 的四步序列，亦未明确声明为替代分支，因此不能给 9–10；主链化学成立，取8。

<details><summary>V0.4理由与本行变化背景</summary>

两步化学自身成立且计量平衡：S1 Catechol+O2→2-hydroxymuconate semialdehyde（O2作辅底物在列，与gold S04一致）；S2 HMS+H2O→2-hydroxypenta-2,4-dienoate+formate（含H2O在列，元素守恒），终点与题面/gold终点一致，无错误起始步、无无依据跳步、无不守恒。但相对指定路线II缺少2个关键中间体转化（2-hydroxyhexa-2,4-dienedioate与2-oxohex-3-enedioate），以一未核实的水解酶分支接通，属‘主干部分成立、关键中间体/转化需修订、合理性证据有限’，不满足四.5的cap条件（未声明地严重偏离的是路线而非题面终点），故不判本维关键错误，取5–6档上端6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：确认儿茶酚入口与终点产物结构；不把 hydrolase 两步分支回填为 route II 目标完成。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：支持 catechol 2,3-dioxygenase 与儿茶酚开环步骤；不支持答案 S2 hydrolase 属于 route II 的必答步。
- ANSWER_TEXT / ANSWER.steps&#91;0..1&#93;：用于核对答案自身两步的方向、产物与连续性。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按目标反应逐项看：S04（catechol 2,3-dioxygenase，EC 1.13.11.2，儿茶酚→2-hydroxymuconate semialdehyde）有 accepted set 支持；S01 tautomerase、S02 decarboxylase、S03 dehydrogenase 均未交付。答案 S2 使用 hydrolase EC 3.7.1.9，直通终点，不对应 S03/S01/S02 的目标反应。可判 S=1、M=3，C=0.25，落在&#91;3,4&#93;；且缺失包含 KEY 目标，按 D-KEY4 上界≤4。仅少数目标可用，取3。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶-反应对应与gold一致（catechol 2,3-dioxygenase，EC 1.13.11.2，见enzyme_gold BSY-e03417/8/9），有可靠支持；S2酶（2-hydroxymuconate-semialdehyde hydrolase，EC 3.7.1.9）名称-EC-反应类型（C–C水解酶）自洽，但E0无该EC记录、gold亦无此步骤，属‘若干关键步骤仍缺具体核验’。两步中1步未核、且该步承载整段下游转化，故置于5–6档取6。无EC大类与反应类型矛盾、无名-号互相矛盾证据，不判关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：支持 S04 的 catechol 2,3-dioxygenase/EC 1.13.11.2 目标功能；也列出其余必答步的 accepted 酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：给出必答目标反应序列；不把 hydrolase 直通终点视为 S03/S01/S02 的替代完成。
- ANSWER_TEXT / ANSWER.steps：核对答案只交付两步酶反应，缺少三个目标反应。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 微生物身份 Pseudomonas sp. CF600 有 gold PATHWAY_COMPLETE 行（TaxID 79676）支持其作为该路线完整路径菌；但答案未给 TaxID，且把同一菌同时绑定到 S1/S2 两步，缺少逐目标步的反应级归属证据。菌株身份与整路径能力有可靠支持，逐步骤归属仍需确认，达不到 9–10；取7。

<details><summary>V0.4理由与本行变化背景</summary>

菌株身份 Pseudomonas sp. CF600 与gold PATHWAY_COMPLETE记录一致（trait_gold中taxid 79676、pathway_complete=TRUE、download_available=FALSE），整条路径能力声称有gold支持；ncbi_taxid诚实留null，无TaxID身份错配、无跨类群错配。步级归属（同一菌承担C23O与水解酶两步）无步级记录（gold步级菌为P. putida 303、P. nitroreducens、Alcaligenes等），属‘主要微生物对应及身份有可靠支持，仅少量具体条目需确认’，不构成身份阶梯②/③，不判关键错误，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_055：支持 CF600 作为该 case 的完整路径菌；不自动细化到每一步的酶级归属。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_055：确认 CF600 的 pathway_complete 标记；多数性状为 UNKNOWN，不能回填为已核实性状。
- ANSWER_TEXT / ANSWER.microorganism：核对答案为 CF600 单菌重复用于两步，且 TaxID 为空。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15 项性状中仅 F7/F8/F9 填写，其余 12 项显式 null/unknown。F7“可利用儿茶酚作为碳源和能源”、F8“可经间位裂解途径降解儿茶酚等芳香族化合物”、F9“catechol 2,3-dioxygenase 活性”方向合理，但 CF600 在冻结 trait_gold 中这些性状均为 UNKNOWN，且答案用 EVID_001 路线级来源支撑性状，缺少性状级证据。属部分性状可能适用但关键证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

性状15项中3项有值：F7‘可利用儿茶酚作为碳源和能源’、F8‘可经间位裂解途径降解儿茶酚等芳香族化合物’、F9‘catechol 2,3-dioxygenase活性’，均为定性、粒度适当且与CF600的间位裂解通路生物学相符，未见数值/单位/菌株错配，也未见把特定观测推广为普遍耐受范围；12项为明确未知（value=null, confidence=unknown），属信息不足而非错误。但三项均无快照性状记录可核（GAP-055-034/035/036，E0两条记录均属P. putida不可回填），关键性状（温度/pH/氧/革兰/保藏等）全部明确未知，属‘部分性状准确且适用，但关键项证据不足’，取5–6档低端5。完成度缺口已在D1登记，不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_055：显示 CF600 多数性状在冻结本地输入中为 UNKNOWN；不能把路线级信息回填为已观测性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_055：标识 CF600 性状的可评分性；多数为 completeness_only 或无观测源。
- ANSWER_TEXT / ANSWER.traits：核对答案只填 3 项定性性状，其余显式未知。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出 3 条 evidence_registry：EVID_001 为 MetaCyc 路线名但 record_id=null；EVID_002/003 给出 BRENDA EC 编号 1.13.11.2 与 3.7.1.9，属条目级定位。E0 中无这些 EC/route 的冻结记录，故来源只能登记为 generic/unresolved，未核实到错引。酶步骤有部分条目级定位，但路线、菌株、性状来源多为笼统或未解析，属“部分关键结论可定位、其他仍缺映射”，取5。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：路线（CG01/CG02/CG03）、菌株身份（CG07）与步级归属（CG08）的交付来源主要为EVID_001（MetaCyc路线名，record_id=null）→GENERIC_SOURCE；EC 3.7.1.9与F7/F8/F9无快照记录→UNRESOLVED_SOURCE；仅EC 1.13.11.2一条达到条目级可定位（BRENDA record_id=1.13.11.2）且与gold酶表一致。决策相关组中既有条目级可核对内容，也有大量笼统/待核映射，落‘部分关键结论可定位并核对，其他模块仍缺映射’的5–6档，取5。E0无任何相反记录，无已核实错引，不触发cap；同一单元不叠加cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：用于评价答案实际交付的来源定位；不把未核记录升级为已核实。
- E0_EVIDENCE / f3e0:taxid:303：E0 本题仅含 BacDive 12880 与 TaxID 303 条目；不含 MetaCyc/BRENDA 路线或 EC 1.13.11.2/3.7.1.9 记录。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案明确写出氧条件未指定、route II 数据库记录编号未给出、多数生理性状未知并填 null；confidence 使用 medium/unknown，未把预测系统性写成实验观测。主要不足是未披露其 hydrolase 分支并非题面 route II 的四步序列，也未说明 EC 来源未核。整体不确定性表述较清楚，但边界与路线差异说明不足，取7。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露较具体：题面氧条件未指定、路线II具体数据库记录编号未给出、微生物多数生理性状未知已填null、甲酸按副产物处理，且各step有uncertainty字段，未见系统性把预测当实证、未见已知矛盾被掩盖。但EVID_001以DATABASE_DIRECT+medium标注一个record_id=null的路线级来源，并同时支撑路线、两步反应、菌株与F7/F8，属证据强度超出依据的轻度过度确信（单点/少点，非系统性），且不同时披露‘所交付分支与路线II步骤集合不同’。按5–6档处理，取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：核对答案对氧条件、route record ID、性状未知的披露。
- ANSWER_TEXT / ANSWER.confidence：核对答案使用 medium/unknown，而非把未核内容标成 high。

</details>

## Grok

答案SHA256：`c105e277141a71c36a8c1aafc500d57c45c48ef0e09d421d8553619e7d6d2a92`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案以合法JSON交付了route_scope（原样保留指定路线名）、2步主链、每步酶/EC与微生物、1个organism_profile及全部15项性状字段，并给出证据登记；就其所选水解支路而言，底物-产物、酶、菌和性状模块均有明确对应。存在需复核之处：答案将路线II解释为水解支路并自述未核实，且把题面null氧条件自行推为aerobic；但该路线名本身处于BOUNDARY_REVIEW，按D-M01澄清不能把gold全图步数直接当作缺步分母，故不据此判关键范围偏离或扣成缺步。D1为8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：实际交付了完整JSON模块、2步主链、酶/EC、微生物、15项性状与证据登记
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_055：本题终点为(2Z)-2-hydroxypenta-2,4-dienoate；不直接证明答案所选支路为gold主链
- SCOPE_ROW / SCOPE#BIOPATH150_055#CG04：题面氧条件为null，条件组不成立；答案自行标注aerobic属于需复核的推断

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 就答案实际给出的水解支路而言，两步化学连接成立：catechol经2,3-双加氧开环生成2-hydroxymuconate semialdehyde，随后经EC 3.7.1.9水解/脱甲酸生成2-hydroxypenta-2,4-dienoate（相当于2-oxopent-4-enoate的烯醇式）；底物-产物连续，O2/H2O与formate标注使计量基本可读，并明确说明酮-烯醇互变与SMILES未标立体化学。未发现主链方向反转、原子明显不守恒或无依据跳跃；替代支路身份问题归D1/待复核，不在D2重复扣。D2给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案两步的底物、产物、辅因子与酶EC及互变说明
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：提供本题gold各步反应方向与主产物用于化学连续性对照；不证明答案水解支路属于被锁定主链
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：提供gold酶/EC记录用于对照；不自动否定答案所给EC 3.7.1.9的独立化学合理性

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> C04/C05 low band with D-KEY4 upper bound. The gold-required chain has four reactions: S04 entry, S03 dehydrogenase, S01 tautomerase, S02 terminal decarboxylase. The answer supplies an S04-like entry with accepted catechol 2,3-dioxygenase EC 1.13.11.2, but S03 is answered as an alternative hydrolase EC 3.7.1.9 rather than the required dehydrogenase, and S01/S02 are absent. Only limited entry target credit is usable; the terminal key step is missing. Band &#91;3,4&#93;, score 3 because the usable portion is limited and the key terminal failure is severe.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：Gold accepted enzyme/EC sets for required steps; the answer matches only the S04-like EC 1.13.11.2 entry.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：Gold establishes required directed reactions and terminal product; it does not support substituting the S03 dehydrogenase with a hydrolase branch.
- ANSWER_TEXT / ANSWER_TEXT：Answer gives EC 1.13.11.2 and EC 3.7.1.9; it does not give S03 EC 1.2.1.85, S01 EC 5.3.2.6, or S02 EC 4.1.1.77.

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b 7-band: Pseudomonas putida mt-2 identity is supported at strain-record level by E0 bacdive:12880 and the species TaxID 303 is current. The answer discloses that TaxID 303 is species-level, not a strain-specific TaxID. Species-level pathway-complete support exists for P. putida 303. The remaining weaknesses are granularity and unverified strain-specific complete route II/hydrolase capability, which are not verified contradictions and do not trigger cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：Supports existence and strain designation of mt-2 PaW1(pWWO); does not by itself prove complete route II capability or strain-specific TaxID.
- E0_EVIDENCE / f3e0:taxid:303：Supports species-level TaxID 303 only; does not authenticate a strain-level mt-2 TaxID.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_055：Supports species-level P. putida identity and species pathway-complete row; does not prove strain mt-2 complete route II or its hydrolase branch.

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4 5–6 band. Many basic species-level traits match gold (mesophilic preference, motility, rod shape, Gram-negative, non-sporulating, oxygen-linked respiration), and nulls for pH/salinity/collection/genome are explicitly marked unknown. However key strain-specific and application-relevant claims (obligate aerobic wording, broad carbon-substrate list, pWW0 degradation capacity, specific enzyme activities) rest on internal knowledge and species-level extrapolation; F15 is not scoreable in the frozen trait mask. No verified contradiction, so no cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_055：Supports several species-level traits; does not support obligate-aerobic wording or the full mt-2 substrate/degradation list.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_055：Shows some trait fields are completeness-only or not scoreable for observed accuracy; supports limited D4 banding.
- E0_EVIDENCE / f3e0:bacdive:12880：Supports strain existence and some culture records; culture temperature is not an optimum or tolerance limit.

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 3–4 band. Decision-relevant claims are linked to internal evidence IDs EVID_001-EVID_005, but EVID_001/002/004/005 are INTERNAL_KNOWLEDGE_ONLY or MODEL_INFERENCE, and EVID_003 is an internal free-text citation not machine-resolved in E0. Some locators are specific and tied to steps/claims, so D5 is above 1–2, but they are not locatable delivered records. No verified mis-citation exists, so no D5 cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows the delivered source types and claim-scope mapping; most core entries are internal knowledge or model inference.
- E0_EVIDENCE / f3e0:bacdive:12880：Supports strain identity facts; it does not verify the answer&#x27;s internal source registry or free-text citations.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：Provides target enzyme rows for comparison; it does not supply the answer&#x27;s claimed source for EC 3.7.1.9 or the pWW0 literature citations.

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 7-band. The answer explicitly discloses route-II uncertainty, tautomer/representation limits, null traits, and that TaxID 303 is species-level rather than strain-specific. It does not systematically present predictions as observations. However several core internal-knowledge claims are marked high confidence, and the hydrolase branch is not verified. This is confidence overstatement/local unreliability, not systemic masking; score 7 rather than 8–10.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows explicit route, tautomer and TaxID caveats; also shows high confidence assigned to internal-knowledge core claims.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：Provides the gold chain against which the answer&#x27;s alternative branch and route uncertainty are disclosed; does not show deliberate concealment.

</details>

## GPT5.6

答案SHA256：`a99e1213cf6043638d70c9ce99d05019afb58a2b26bcd71f9f544075d8bca74b`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 is within the program D1 range &#91;1,4&#93;. The answer delivers the route name, five step objects, enzymes, one microorganism profile, and evidence labels, but all 15 traits are null and route diagnosis is DEVIATES. The step and enzyme-microbe association is readable, yet the incomplete trait module and task-level route deviation keep it in the weakened 3-4 band; 4 reflects clearly readable modules with major gaps.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows route name, five steps, enzyme and microorganism fields, and all-null traits.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_055：Gold case is LINEAR_UNIQUE with ordered_step_count 4; not a denominator for all background or branches.

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 is within the program range &#91;1,6&#93;. The conceptual catechol meta-cleavage sequence is recognizable, but the first-step product SMILES O=CC(O)=CC=CC=O lacks the carboxylate oxygen expected for 2-hydroxy-6-oxohexa-2,4-dienoate and has two aldehyde termini; downstream SMILES reuse the mismatch. The decarboxylation step omits CO2 and the S3 enzyme/function label is questionable. These are key chemistry errors, so D2 is capped at 4; 4 is chosen because the intended route and several transformations remain partially recognizable and the failure boundary is clear.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the claimed structures and missing CO2 in the decarboxylation step.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：Gold S04 links catechol to (2Z,4E)-2-hydroxy-6-oxohexa-2,4-dienoate; gold S02 links (3E)-2-oxohex-3-enedioate to (2Z)-2-hydroxypenta-2,4-dienoate plus CO2.

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按C03/C04核对四个必答目标：S01与S02为ROUTE_BLOCKED_MISSING（S02为KEY_TERMINAL），S03为ROUTE_HOLD_REPRESENTATION/UNRESOLVED，S04为ROUTE_BLOCKED_NONMATCH/UNRESOLVED；没有任何目标步达到S。答案为另一条5步meta-cleavage序列，虽出现EC 1.13.11.2、1.2.1.85、4.1.1.77等accepted集内编号，但未能绑定到本题4步目标反应，且关键终点步缺失、入口步目标反应不符，使酶-目标反应主推荐不可用。按C05的1分档：几乎无可用目标催化对应，核心漏交付/不符使主推荐不可用；不把未核S03/S04擅自升为S或F。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_055：定义本题4步目标主链的底物/产物、方向与终点；S02终点产物为(2Z)-2-hydroxypenta-2,4-dienoate，不证明答案5步序列等同
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_055：列出各目标步accepted酶名/EC：S01 5.3.2.6、S02 4.1.1.77、S03 1.2.1.85、S04 1.13.11.2；仅说明这些名称/EC可接受，不证明答案中的反应绑定正确
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_055：确认case与route名称及终点化合物，用于锁定本题目标主链范围

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P. putida mt-2 with TaxID 303 is consistent with E0 taxid:303 and the BacDive 12880 strain record for mt-2 PaW1. organism_gold lists Pseudomonas putida 303 at all four gold steps, and the answer uses the same profile consistently. Strain-level per-step enzyme activity is not individually demonstrated in the frozen slice, so this stays in the 7-8 band; 8 reflects strong species/strain identity and step attribution with only strain-level generalization left.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Official taxonomy record for Pseudomonas putida TaxID 303 at species level; does not by itself prove strain-specific step activity.
- E0_EVIDENCE / f3e0:bacdive:12880：BacDive strain record for Pseudomonas putida mt-2 PaW1 with NCBI tax id 303; identity record, not step-specific enzyme activity.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_055：Lists Pseudomonas putida TaxID 303 as an organism for all four gold steps.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The sole organism profile ORG_001 contains all 15 required traits, but every trait value is null/unknown and no trait evidence is supplied. Per P44, when all required traits are null/empty, D4 is MISSING with score 1; this records non-delivery, not a proven scientific contradiction.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all 15 required trait fields present but null/unknown.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All six answer evidence entries are source_type INTERNAL_KNOWLEDGE_ONLY with null database, record_id, and locator. No external traceable source is delivered for route, enzyme, microorganism, or traits. This is MISSING_SOURCE across decision-relevant groups, so D5 falls in the low band. The registry at least maps claims locally, so 2 rather than 1. No verified mis-citation is present in E0, so no D5 cap applies.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows internal-only source labels and no external locators.

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer explicitly labels all registry entries as INTERNAL_KNOWLEDGE_ONLY and lists some missing EC/structure uncertainties. It does not systematically present predictions as experimental observations. However, it assigns high confidence to S1/S2 while using internal-only evidence and structurally inconsistent SMILES, and its uncertainty statement is too narrow. This is a 7-8 disclosure profile; 7 reflects the narrower limitations and some overconfidence, without systemic-misrepresentation cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows explicit internal-knowledge labels, partial uncertainty list, and high confidence on some internal-only steps.

</details>
