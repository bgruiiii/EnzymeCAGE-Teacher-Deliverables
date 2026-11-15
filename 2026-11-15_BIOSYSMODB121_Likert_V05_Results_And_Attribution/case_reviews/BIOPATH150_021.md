# BIOPATH150_021：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：Toluene degradation to 2-hydroxypentadienoate (via toluene-cis-diol)

污染物：Toluene；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 75 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 67.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 74.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 69.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 66.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 32 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`b27b2ac44ea1e8374a2c96c09e88bd08a12f9209349e4ce2a37b79e193cc9fff`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 路线名与好氧条件原样匹配；steps S1-S4连续覆盖4步，均含底物/产物/酶/EC/菌，organism_profiles按F1去重，15项性状全部出现（F5/F14为明确未知）。任务符合度与完整性仅见少量来源/粒度待核，属9档而非10档。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块全部实质回应：route_scope原样回填题面指定路线名与aerobic；4步主链每步给出主底物/主产物英文名与SMILES、一个首选酶及EC、一个对应微生物；organism_profiles按物种+菌株去重为1条并被全部step引用（题面不要求整条路径只有一个代表菌，此处单菌属可接受）；15项性状齐备（13项填写、F5与F14为明确未知null，按P15/P45不计作遗漏但与错误不同）；evidence_registry与uncertainties均交付。扣分点仅为两项明确未知（完成度不足）与菌株级编号未交付。无模块缺失、无范围偏离，故落9分档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_021：支持本题为LINEAR_UNIQUE、4步主链；不证明答案各步科学内容。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_021：支持题面路线名与终产物范围；不证明答案SMILES或EC。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 四步转化与tod路径一致：双加氧→脱氢芳构化→间位裂解→水解，方向为好氧，终点为2-hydroxypenta-2,4-dienoate与acetate。主要化学连接正确；SMILES仅给连接性、部分顺反与H+未写全，属局部表示/计量缺陷，不破坏主链，故取8档上沿。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步对齐：S1甲苯双加氧→toluene-cis-2,3-dihydrodiol；S2 NAD+依赖脱氢芳构化→3-methylcatechol；S3间位(2,3-)裂解→2-hydroxy-6-oxohepta-2,4-dienoate；S4水解→2-hydroxypenta-2,4-dienoate+acetate，与gold主链顺序、方向与终点（Acetate|(2Z)-2-hydroxypenta-2,4-dienoate）一致，碳数守恒（C7→C5+C2）。辅因子基本在列（O2、NADH/NAD+、H2O），但各步未列出H+，S1/S3的加氧计量未写H+；SMILES仅给连接性未标顺式立体化学（答案自述）。按八.辅因子与简化反应式条款属局部计量/表达缺陷，落9分档而非满分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：支持四步主链的底物-产物方向与顺序；不证明答案所有立体化学表达。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_021：支持题面终点范围；不证明答案中间体SMILES。
- E0_EVIDENCE / f3e0:ec:1.14.12.11：官方EC记录支持toluene dioxygenase催化的甲苯双加氧反应；不证明菌株实验活性。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 按反应身份映射：答案S1↔gold S03、S2↔gold S02、S3↔gold S04、S4↔gold S01。S1 toluene dioxygenase/EC 1.14.12.11与E0官方EC条目及accepted集合一致；S3 catechol 2,3-dioxygenase/EC 1.13.11.2与accepted集合一致。S2名称cis-toluene dihydrodiol dehydrogenase符合accepted，但显式EC 1.3.1.82无冻结E0记录且与accepted 1.3.1.19不一致；S4名称2-hydroxy-6-oxohepta-2,4-dienoate hydrolase符合accepted，但显式EC 3.7.1.9无冻结E0记录且与accepted 3.7.1.25不一致。按C04，已支持目标约2/4、U约2/4，落入&#91;5,6&#93;；已支持部分逐反应关联和主链结构清楚，两个待核EC配对已在答案uncertainties中明示，足以阻止进入7–8档，故取6而非5；不取7因存在两个MAJOR U且其中S01对应KEY_TERMINAL，不取9–10因关键显式EC配对未全核。表示边界待审按局部hold处理，不单独将整维转NE。

<details><summary>V0.4理由与本行变化背景</summary>

酶名与反应类型的对应整体自洽（双加氧酶/脱氢酶/裂解双加氧酶/水解酶），S1的EC 1.14.12.11经E0官方条目accepted name与reaction逐步匹配（SUPPORTED），S3的EC 1.13.11.2与gold一致但E0无该EC条目（GAP-021-004）。S2的1.3.1.82与S4的3.7.1.9与冻结gold（1.3.1.19、3.7.1.25）不一致，E0无对应条目（GAP-021-005/007），按四.5保守条款无法核验→UNRESOLVED、保留低分与待核、不cap；答案对两处均自述中等置信并给出备选编号。因四个关键步骤中两步EC仍缺具体核验，落5–6档并取6分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_021：给出本题必答步的accepted酶名与EC：S01 hydrolase EC 3.7.1.25；S02 dehydrogenase EC 1.3.1.19；S03 toluene 1,2-dioxygenase EC 1.14.12.11；S04 catechol/3-methylcatechol 2,3-dioxygenase EC 1.13.11.2。仅支持数据库策展粒度，不证明具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：给出S01–S04的目标反应参与者、方向与主产物；支持目标反应身份和主链方向，不确认答案的立体化学或电荷表示。
- E0_EVIDENCE / f3e0:ec:1.14.12.11：官方EC 1.14.12.11条目accepted names含toluene dioxygenase，reaction为toluene + NADH + H+ + O2 = (1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol + NAD+；支持S1的酶名/EC与反应类型，不证明todC1C2BA具体蛋白或P. putida F1实测活性。
- E0_EVIDENCE / f3e0:ec:1.3.1.19：官方EC 1.3.1.19条目为cis-1,2-dihydrobenzene-1,2-diol dehydrogenase，reaction为cis-1,2-dihydrobenzene-1,2-diol + NAD+ = catechol + NADH + H+；仅支持该accepted EC条目本身，不支持答案显式EC 1.3.1.82，也不证明甲苯二氢二醇/3-methylcatechol特定底物活性。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> P. putida F1身份与tod基因/步骤归属总体匹配；organism_gold四步均列P. putida，PATHWAY_COMPLETE亦支持P. putida。主要扣分点是ncbi_taxid=303为种级，而strain=F1；E0另有菌株级351746。答案已披露该粒度限制，按身份阶梯作档内扣，不推翻主要微生物推荐。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份正确且可核：P. putida与TaxID 303在E0官方记录学名匹配（SUPPORTED）；菌株选择F1与该路径（tod操纵子）匹配，gold各步微生物均含Pseudomonas putida(303)。问题为粒度：对菌株级声称F1只交付种级TaxID 303，E0的303记录名称不含F1菌株token（菌株级关联UNRESOLVED），而F1自身菌株级记录（351746）答案未交付；按八.D3b身份阶梯①粒度不足→档内扣、默认不cap；答案已在uncertainties披露该粒度。步级催化归属与整路径能力仅由自由文本文献支撑（UNRESOLVED）。无跨属/无关类群或编造身份，故落7分档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida物种级TaxID；不支持其自动等于F1菌株级编号。
- E0_EVIDENCE / f3e0:taxid:351746：支持Pseudomonas putida F1的菌株级TaxID记录存在；不证明具体酶活或整路能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_021：支持各步P. putida归属与PATHWAY_COMPLETE标记；不证明F1菌株的实验活性。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 15项性状全部出现，13项有值，F5/F14明确未知。金标种级记录支持温度偏好、非嗜盐、运动性、杆状、革兰氏阴性、不产孢等；F1/F6/F7/F8/F9与F1 tod表型大体一致。扣分点是氧耐受写成“严格好氧”而金标仅观察aerotolerant、温度最适无直接观测、若干性状来自INTERNAL_KNOWLEDGE_ONLY且非F1实测，故取7档。

<details><summary>V0.4理由与本行变化背景</summary>

主要性状与gold种级记录可核对：F3 optimum 7.0＝gold pH growth 7.0观测；F4非嗜盐＝gold salinity preference non-halophilic；F12革兰氏阴性、F13不产芽孢、F10运动性、F11杆状均与gold观测一致；F2 preference中温＝mesophilic一致。问题：F2 optimum_c=30系由培养温度（实验室常规30°C）推得，而gold无观测最适值（trait_subfield_mask: optimum completeness_only；且有培养温度≠最适值的解释层警示）；F1氧需求写“严格好氧”，gold观测为aerotolerant=true、facultative anaerobe预测为No robust majority，属未被直接支持亦未被推翻；多数性状来源为INTERNAL_KNOWLEDGE_ONLY（EVID_004）且为种级常识用于菌株F1（四.4允许物种级代表记录，但答案未给菌株级来源）。F5/F14为明确未知，完成度扣分归D1不重复重扣。综合落7分档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_021：支持P. putida种级F1-F15的观测/预测背景；不把种级代表记录自动升级为F1菌株实测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_021：标明F3/F15等completeness_only及部分性状分母角色；不改变已给值的正确性判断。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_021：标明温度上下限等子字段待裁定；支持不以未裁定范围机械扣分。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 证据登记覆盖路线、酶、菌与部分性状，EVID_001/002/003/005给出具体文献或UM-BBD定位并声明claim_scope；但E0只能核验少数组（如EC 1.14.12.11、TaxID 303/351746），多个引文为自由文本未解析，登记为UNRESOLVED_SOURCE；F1多数性状仅INTERNAL_KNOWLEDGE_ONLY，登记为MISSING_SOURCE；氧耐受等应用关键性状无外部来源。无已核实错引，不cap，但关键组仅部分可核对，落6档。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付了evidence_registry并以claim_scope逐条映射到步骤/性状，属可读的追溯结构，且EVID_004自标INTERNAL_KNOWLEDGE_ONLY未冒充实证。但决定维度档位的问题：决策相关组（CG01/02/03/05/07/08/09；CG04/10/14）中，路线与酶菌来源仅为UM-BBD页面文字描述与四条自由文本文献（GAP-021-015/018/021/022未解析），无DOI/record_id，E0无可核条目→GENERIC_SOURCE与UNRESOLVED_SOURCE并存；性状组（CG10–CG14）仅INTERNAL_KNOWLEDGE_ONLY，按P34记MISSING_SOURCE。可经E0核对的仅EC 1.14.12.11与TaxID 303种级两项，条目级可核对覆盖不足以进7–8档，但也不是全部笼统/全缺失，故按“部分关键结论可定位、其他模块缺映射”落5分档。无任何经核实错引（未出现引用不存在或不支持声称的已核实情形），不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- SCOPE_ROW / SCOPE#BIOPATH150_021#CG04：题面好氧条件构成CG04应用关键条件；不证明F1氧耐受性状已由外部来源支持。
- SCOPE_ROW / SCOPE#BIOPATH150_021#CG10：题面好氧条件使CG10氧需求成为应用关键组；不证明答案的氧需求表述正确。
- E0_EVIDENCE / f3e0:ec:1.14.12.11：支持官方EC条目存在；不核验EVID_001/002等自由文本引文全文。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> uncertainties逐条披露EC、TaxID、性状INTERNAL_KNOWLEDGE_ONLY与SMILES立体缺失；confidence按内容高低分层，F5/F14明确unknown，未把预测系统性地冒充观测。仍有“严格好氧”等表述略强于种级证据、部分性状缺原始raw_text，属局部过度确信，不构成系统性误导，给8。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量较好且具体：uncertainties逐条列出S2 EC的中等置信与EC 1.3.1.-备选、S4 EC 3.7.1.9与3.7.1.5别名、TaxID按种级303填写且保藏号/基因组为null、多数性状来自种级内部常识、toluene-cis-diol SMILES未标立体化学；步骤级给出medium/low/unknown置信标签；alternative_branches显式标注is_part_of_scored_main_route=false，未把分支混入主链。轻微问题：个别字段以high置信呈现但依赖内部知识（如F12革兰氏阴性），registry层(EVID_001 confidence=medium)与步级high不完全一致，属单点过度确信、非系统性误导，档内扣分。落7–8档上限区间取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`944af51950c8317a4d5d1e85d0ac4d2d5105e1a08eda90a62537df22f511ccfb`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案覆盖题面指定的4步主链：route_scope原样填写指定路线与aerobic；steps&#91;0-3&#93;均给出主底物/主产物英文名及SMILES、首选酶及EC、对应微生物，并有一个按物种+菌株去重的Pseudomonas putida F1 profile及F1–F15性状字段。未见改选路线、终点偏离或模块整体缺失；仅见部分步骤未列O2/NADH/NAD+/H2O等辅因子，以及部分性状按题面允许填null的轻量完整性问题，故落在9–10档下沿。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的route_scope字段（chosen_route_name原样、oxygen_condition=aerobic）齐备；S1–S4四步均给出主底物/主产物英文名+SMILES、一个首选酶+EC、一个对应微生物，且同一菌（P. putida F1）合并为唯一ORG_001，符合“同菌去重”要求；15项性状字段全部出现，其中F3/F4/F5为显式null+confidence=unknown（诚实未知，按P15/P45记完成度不足，不等同遗漏）；evidence_registry 3条覆盖路径酶、性状与基因组。缺口为3/15性状未知、uncertainties为空、未标注辅因子。属7–8档：大部分必要内容完整、关联清楚，少量完成度缺口。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_021：本案为LINEAR_UNIQUE，ordered_step_count=4，与题面4步主链任务一致
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_021：题面指定路线起点为Toluene，终点包含Acetate与(2Z)-2-hydroxypenta-2,4-dienoate
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：给出主链各步主底物/主产物及S03→S02→S04→S01方向，用于核对覆盖与终点
- QUESTION_TEXT / QUESTION_BEGIN：题面要求指定路线、aerobic、每步主底物/主产物+酶/EC+微生物、15项性状
- ANSWER_TEXT / ANSWER.steps&#91;0-3&#93;：答案实际交付4步、一个去重organism_profile及15项性状字段

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 核心化学序列与指定主链一致：Toluene→cis-toluene dihydrodiol→3-methylcatechol→2-hydroxy-6-oxohepta-2,4-dienoate→2-hydroxypenta-2,4-dienoate+acetate；方向、主链连接和终产物均正确。局部问题为S1产物立体未明确、部分步骤未列O2/NADH/NAD+/H2O等辅因子、末端未标(2Z)，按P103–P105属局部计量/表示问题，不破坏主有机物转化；当前程序对D2的nine_ten_eligible为false，故在7–8档内取8。

<details><summary>V0.4理由与本行变化背景</summary>

四步主链与gold一致：Toluene→cis-Toluene dihydrodiol（二氢二醇骨架与gold (1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol同构）→3-Methylcatechol→2-Hydroxy-6-oxohepta-2,4-dienoate→2-Hydroxypenta-2,4-dienoate+Acetate；方向、间位开环再水解的连接顺序、终点（acetate+2-羟基五-2,4-二烯酸）均符合题面指定路线，无起始步错误、无跳步、无原子明显不守恒（SMILES骨架逐碳可对）。缺陷：O2、NADH、NAD+、H2O等辅因子/溶剂全部未列，字面计量不成立——按八.辅因子条款属局部计量缺陷，7–8档不cap；另将acetate标role=byproduct而gold列为主产物，属次要标注问题。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：逐步主底物/主产物、方向及终产物支持该主链化学序列
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_021：确认起点Toluene与终点Acetate、(2Z)-2-hydroxypenta-2,4-dienoate
- E0_EVIDENCE / f3e0:ec:1.14.12.11：官方EC条目反应为toluene+NADH+H++O2→(1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol+NAD+；支持第一步主转化类别，但不为答案未写明的立体与辅因子补充支持
- ANSWER_TEXT / ANSWER.steps&#91;0-3&#93;：答案四步底物/产物序列用于与gold主链逐步比对

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> Three of four enzyme assignments have accepted names and explicit ECs matching the accepted sets (toluene dioxygenase 1.14.12.11, cis-toluene dihydrodiol dehydrogenase 1.3.1.19, 3-methylcatechol 2,3-dioxygenase 1.13.11.2). The terminal hydrolase name matches, but its explicit EC 3.7.1.11 differs from the accepted 3.7.1.25 and no frozen EC entry resolves it. This is a local/substantive explicit-EC problem, not a confirmed key failure; representation hold also blocks high tier. Band &#91;5,6&#93;.

<details><summary>V0.4理由与本行变化背景</summary>

S1 toluene dioxygenase/EC 1.14.12.11经E0核验accepted name与reaction（toluene+NADH+H+ +O2=(1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol+NAD+）与答案首步一致（SUPPORTED）；S2 EC 1.3.1.19、S3 EC 1.13.11.2与gold冻结酶表一致，但E0无反应级记录（1.13.11.2无卡；1.3.1.19官方accepted name为苯二氢二醇脱氢酶、&#x27;toluene dihydrodiol&#x27;名token未见于记录变体）→UNRESOLVED；S4酶名与gold一致而EC写作3.7.1.11，gold冻结值为3.7.1.25，E0对该号无记录（GAP-021-006），按四.5“gold单值与答案冲突且无法核验→UNRESOLVED、档内扣、不cap”处理。基因名TodC1C2BA/TodD/TodE/TodF与P. putida F1 tod操纵子相符但E0未核。总体主要步骤酶-反应对应有可靠支持、个别条目待核→7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:1.14.12.11：Supports official EC name/reaction for toluene dioxygenase/toluene 1,2-dioxygenase system; does not prove P. putida F1 protein expression.
- E0_EVIDENCE / f3e0:ec:1.3.1.19：Supports EC 1.3.1.19 entry and reaction as an official record; exact answer name association remains unverified in E0.
- GOLD_SLICE / enzyme_gold.tsv：Lists accepted EC 3.7.1.25 for the terminal hydrolase; it does not list or validate the answer&#x27;s 3.7.1.11, leaving a mismatch unresolved.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> P. putida F1 is a valid strain identity via TaxID 351746, and P. putida species records appear for the corresponding gold steps; however the answer applies one strain-level profile to all steps and claims a complete pathway, while E0 provides identity only and the step/organism and complete-pathway claims are UNRESOLVED. This is a granularity/capability-support deficiency, not a verified identity error or cap. Band 7.

<details><summary>V0.4理由与本行变化背景</summary>

四步统一绑定Pseudomonas putida F1（taxid 351746，ORG_001）。E0 taxid卡与第三方补录支持ScientificName=&#x27;Pseudomonas putida F1&#x27;、record_status=CURRENT、lineage至种P. putida(303)，属菌株级身份与声称粒度匹配（SUPPORTED）；gold在本路线S01–S04均列P. putida（303，PATHWAY_COMPLETE TRUE），按四.4同物种代表记录口径，不因答案用实验菌株F1与代表株不同而判错。步级催化归属（L2）与整路径能力（L3）属语义层，E0保持UNRESOLVED，为少量待确认条目；未见物种/菌株或TaxID编造，未见由序列存在性过度外推。8档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:351746：Supports official name Pseudomonas putida F1 for TaxID 351746 and lineage to P. putida; does not support step catalysis or complete pathway capability.
- E0_EVIDENCE / f3e0:taxid:303：Supports the species-level P. putida identity; does not convert species-level records into strain F1 capability evidence.
- GOLD_SLICE / organism_gold.tsv：Lists P. putida at several step rows and a PATHWAY_COMPLETE species-level row; does not list P. putida F1 as the exact strain for all steps.

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> The answer returns all 15 trait slots for one P. putida F1 profile. Several traits are consistent with the P. putida species representative (motility, rod shape, Gram-negative, non-sporulating, aerobic/O2, mesophilic preference), and same-species representative use is permitted. However F3/F4/F5 are null despite species-level gold records, F7/F8 are broad substrate/degradation claims not directly supported by the frozen trait rows, and F14 uses a suppressed NC_009512.1 accession with size/GC not shown in E0. Band 7: main traits broadly applicable, local gaps/overbreadth remain.

<details><summary>V0.4理由与本行变化背景</summary>

已给12项性状中，F10运动性、F11杆状、F12革兰氏阴性、F13不产芽孢与种级(303)观测记录一致（SUPPORTED）；F2偏好mesophilic一致；F6好氧/O2与记录无冲突（记录只否证硝酸盐等厌氧呼吸）；F7/F8/F9为种级一般能力陈述，无甲苯/苯/乙苯同化观测记录支撑。关键项证据不足或分型不一致：F2 optimum_c=30无观测来源（该子字段为completeness_only，BacDive 12880的26/30°C属另一菌株培养记录，培养温度≠最适温度，不得回填）；F14 size 5959964/GC 61.9不在E0核酸卡内且所引NC_009512.1为SUPPRESSED；F1“专性需氧”与种级aerotolerant=true分型不一致；F3/pH、F4/盐度、F5/保藏号留null（完成度缺口主归D1，按P112不重复重扣）。多数定性性状可用但关键定量/分型项证据不足、适用粒度未说明→6档；未见数值离谱到误导筛选或明确预测冒充观测的已核实证据，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Provides P. putida 303 species-level observed/predicted traits; supports representative traits but not strain F1-specific values.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv：Shows which trait subfields are scoreable or pending teacher adjudication; temperature min/max and some other subfields are not fully scoreable.
- E0_EVIDENCE / f3e0:accession:NC_009512.1：Confirms the accession record exists but is SUPPRESSED; the excerpt does not support the claimed genome size or GC percentage.

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> Core route, enzyme, microorganism and most trait claims point to EVID_001/EVID_002, both INTERNAL_KNOWLEDGE_ONLY, which rubric D5 treats as MISSING_SOURCE. Only EVID_003 gives a specific NCBI accession, but NC_009512.1 is SUPPRESSED and the E0 excerpt does not verify size/GC. No verified mis-citation is established, so no cap. Decision-relevant groups are mostly missing source, placing D5 in the low 3-4 band; 3 reflects the isolated but unresolved genome accession.

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组（CG01/02/03/05/07/08/09、CG04/CG10、CG14）全部仅有INTERNAL_KNOWLEDGE_ONLY类自我声明（EVID_001/EVID_002）→MISSING_SOURCE；唯一条目级引用为CG17的NCBI NC_009512.1（EVID_003），E0显示记录存在但状态SUPPRESSED且卡内无size/GC字段→UNRESOLVED_SOURCE。无任何经核实的条目级支持，也无已核实错引（不得把“粒度不足/历史状态”判为虚构或CONTRADICTED）。按四.3合成规则：决策相关组基本全部缺失→低分档、默认不cap；考虑答案确实交付了带claim_scope的结构化证据条目与一个可定位登录号（但不足以核对结论），取低分档上限3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:accession:NC_009512.1：Confirms record existence/status SUPPRESSED; does not verify size/GC and does not provide item-level support for the route or enzyme claims.
- ANSWER_TEXT / BIOPATH150_021_ANSWER：Shows EVID_001 and EVID_002 are INTERNAL_KNOWLEDGE_ONLY; EVID_003 is the only database-specific source.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> The answer does disclose source_type INTERNAL_KNOWLEDGE_ONLY for the route/traits and uses medium/low confidence, and it leaves unknown traits null. But the uncertainties array is empty, no main limitations or conflicts are explained, broad F7/F8 claims and F14 are presented with medium confidence, and the suppressed status of NC_009512.1 is not disclosed. This is more than a single local overconfidence but not systemic misleading. Band 5-6.

<details><summary>V0.4理由与本行变化背景</summary>

答案以逐字段confidence（medium/low/high/unknown）与source_type=INTERNAL_KNOWLEDGE_ONLY给出基本不确定性/证据性质标注，F2/F15自标low、F3/F4/F5填null，属诚实标注的正面成分；但uncertainties为空数组、每步uncertainty=null，未说明任何主要限制（性状为种级推断/内部知识、基因组登录号历史状态、EC号自记忆、为何选间位开环而非邻位开环），F12革兰氏标high、F1与F6–F9标medium，结论强度超过其内部知识依据，central_metabolism_entry.explanation亦以断言口吻给出下游转化。属“有不确定性说明但过于笼统、部分结论强度超过依据”的5档；未见系统性把预测写成实证或掩盖已知矛盾，不cap。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_021_ANSWER：Shows confidence labels, INTERNAL_KNOWLEDGE_ONLY evidence types, null unknowns, and the empty uncertainties array.
- E0_EVIDENCE / f3e0:accession:NC_009512.1：Shows the cited accession is SUPPRESSED; the answer does not disclose this status.

</details>

## Kimi

答案SHA256：`3ec6ccae668f8ab19d54e97f412aae93d5d57d567cd90f91ad0019d4fc90f785`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> Route name and oxygen condition are echoed exactly; four ordered steps cover toluene to 2-hydroxypenta-2,4-dienoate plus acetate, with one microorganism and all 15 trait fields present. Minor completeness defects remain: S4 has enzyme name/gene but ec_number=null, and stereo/representation nuance is disclosed rather than fully encoded. 7-8 band: mostly complete, clear associations, only limited omissions.

<details><summary>V0.4理由与本行变化背景</summary>

四步主链、每步底物/产物/SMILES、酶及EC字段、对应微生物、单一去重profile和15项性状均已交付；chosen_route_name原样回填，整体格式完整。少量性状子字段与S4 EC以null保留，属于任务允许的未知处理，不构成重要遗漏。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Answer supplies four steps, one profile, 15 trait fields, and evidence registry; S4 EC is null.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_021：Confirms route name, start toluene, aerobic flag, and terminal products for the task scope.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_021：Confirms four ordered gold steps for this case, not an expanded branch denominator.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> Main directed chemistry is coherent and matches the gold route: toluene cis-dihydroxylation, dihydrodiol dehydrogenation/aromatization, meta ring cleavage to 2-hydroxy-6-oxohepta-2,4-dienoate, then hydrolysis to 2-hydroxypenta-2,4-dienoate plus acetate. Direction and core transformations are correct. Local cofactor/charge details are simplified: S1 includes an extra water byproduct, and H+ is omitted in S2-S4; P103-type local stoichiometric/cofactor defects keep this in the 7-8 band, not a cap.

<details><summary>V0.4理由与本行变化背景</summary>

主链方向、顺序与关键中间体正确：toluene经cis-toluene dihydrodiol、3-methylcatechol、2-hydroxy-6-oxohepta-2,4-dienoate至2-hydroxypentadienoate并释放acetate，止于题面指定终点。S1把Water列为byproduct属于局部计量/副产物表述不严谨，未推翻主链结论，按7-8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows four-step main chain, ring cleavage, terminal products, and cofactor usage; also shows local H+/water simplifications.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：Provides reference reaction orientations and main products for S01-S04; does not by itself resolve stereo-blind representation.

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> Manual comparison to the accepted sets supports all four target enzyme functions: S03=EC 1.14.12.11, S02=EC 1.3.1.19, S04=EC 1.13.11.2, and S01=accepted 2-hydroxy-6-oxohepta-2,4-dienoate hydrolase. S1-S3 explicit ECs match accepted exact ECs; S4 omits EC but gives the accepted hydrolase name/TodF. Optional gene annotations remain unresolved and the route representation boundary blocks 9-10; within D3a allowed &#91;1,8&#93;, 8 is supported by the clear target-function correspondence.

<details><summary>V0.4理由与本行变化背景</summary>

S1-S3的EC 1.14.12.11、1.3.1.19、1.13.11.2与gold酶-反应对应一致；S4 TodF名称与todF基因归属正确，但EC填null，gold为3.7.1.25，属少量条目待补，不构成关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:1.14.12.11：Official EC entry supports toluene dioxygenase/2,3-dioxygenase name and toluene dihydroxylation reaction; does not prove a specific protein assay.
- E0_EVIDENCE / f3e0:ec:1.3.1.19：Official EC entry supports EC 1.3.1.19 identity/reaction for dihydrodiol dehydrogenase; toluene-specific name remains acceptance-bound rather than independently confirmed here.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_021：Lists the accepted enzyme names and ECs for the four required steps, including hydrolase EC 3.7.1.25 for S01.
- ANSWER_TEXT / ANSWER：Answer supplies matching step enzymes and ECs except S4 EC null.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> The main microorganism identity Pseudomonas putida F1 is supported by TaxID 351746, whose official name contains the strain token F1 and lineage to P. putida. However step-level attribution of every reaction to F1 and the complete-pathway capability claim remain unresolved; ATCC 700007 is not in E0 and NC_009512.1 is recorded as SUPPRESSED. No verified identity contradiction or cross-strain cap, so 7: main identity reliable, several specific capability/identifier items still need confirmation.

<details><summary>V0.4理由与本行变化背景</summary>

统一推荐Pseudomonas putida F1，TaxID 351746经E0核验为P. putida F1；gold四步均有P. putida且PATHWAY_COMPLETE指向P. putida，菌种身份与步骤归属有支持。F1菌株级完整tod能力在E0为UNRESOLVED，属局部待核，不判错，故取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:351746：Official taxonomy record gives scientific name Pseudomonas putida F1; supports identity only, not step catalysis or complete pathway capability.
- E0_EVIDENCE / f3e0:taxid:303：Species-level P. putida record supports species identity/lineage; does not certify the F1 strain or its pathway capability by itself.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_021：Gold lists species-level step organisms and a PATHWAY_COMPLETE row; it does not independently certify every F1 step attribution.

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Most species-level checkable traits are consistent with the frozen P. putida reference: Gram-negative, rod-shaped, motile, non-sporulating, mesophilic, pH around 7, and aerobic respiration. Missing minimum/maximum salinity and temperature subfields are explicitly null and not fabricated. Remaining issues: many trait sources are EVID_008 INTERNAL_KNOWLEDGE_ONLY; the oxygen statement &#x27;strict aerobe&#x27; is stronger than gold&#x27;s aerotolerant=true; ATCC/genome identifiers remain unresolved or suppressed. 7 fits major traits plausible/verifiable with several condition/source limitations.

<details><summary>V0.4理由与本行变化背景</summary>

多数性状与gold物种级记录相符：运动性、杆状、革兰氏阴性、不产孢、中温偏好等；温度/pH最适值与部分降解能力主要来自内部知识或未核。F4盐度整项null，F14仅登录号且该登录号记录状态为SUPPRESSED，关键性状未全部充分核验，按7档取分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_021：Species-level trait records support Gram-negative, rod-shaped, motile, non-spore, temperature/pH ranges, and aerobic context; do not prove all F1-specific values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_021：Marks several trait subfields as completeness-only or pending adjudication; prevents treating missing min/max as observed accuracy errors.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_021：Shows temperature min/max and some salinity maximum values are pending teacher adjudication; supports conservative D4 treatment.
- ANSWER_TEXT / ANSWER：All 15 traits are present; F4 salinity value is null, and several source labels are internal-only.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer delivers a structured evidence registry and specific locators for core route, enzyme, taxonomy, genome accession, and ATCC claims. However several key citations are free-text/unreplayable in E0 (EAWAG/KEGG/literature), TodF EC is absent, ATCC 700007 is a gap, NC_009512.1 is SUPPRESSED, and many traits rely on EVID_008 INTERNAL_KNOWLEDGE_ONLY. No verified mis-citation and no cap; this is the 5-6 band: some key conclusions locatable/checkable, other modules still lack mapping or necessary records.

<details><summary>V0.4理由与本行变化背景</summary>

答案提供evidence_registry，并将步骤、酶、微生物和多数性状映射到evidence_id；路线/酶/菌部分有可定位URL或文献。但多数引用不在E0冻结证据内，CG10/CG11-CG13等性状仅INTERNAL_KNOWLEDGE_ONLY或null，ATCC 700007、EC 1.13.11.2等存在E0 gap；无已核实错引、无cap。按部分关键结论可定位、其他模块仍缺映射的5-6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:351746：Supports the TaxID/name identity citation for P. putida F1; does not validate all other evidence records.
- E0_EVIDENCE / f3e0:accession:NC_009512.1：Shows the accession exists historically but is SUPPRESSED; does not establish it as the current genome record.
- E0_EVIDENCE / f3e0:ec:1.14.12.11：Supports one core EC citation; other free-text literature/KEGG claims remain unresolved.
- ANSWER_TEXT / ANSWER：Shows delivered evidence registry and claim scopes; many trait claims point to internal knowledge only.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The answer is unusually explicit about uncertainty: it marks low/medium confidence, leaves unknown EC/SMILES/genome subfields null, and lists specific uncertainties about TodF EC, genome size/GC, cofactors, ATCC/TaxID verification, and stereochemical representation. It does not systematically present predictions as observations. A few statements (e.g., F1 complete tod operon and strict aerobe) are stronger than the frozen evidence, but this is local overconfidence rather than systemic misleading. 8: good disclosure with minor unresolved evidence-strength issues.

<details><summary>V0.4理由与本行变化背景</summary>

答案给出逐项confidence并在uncertainties中披露S4 EC未定、F14大小/GC未核、辅因子SMILES未填、ATCC/TaxID中等置信、F4盐度无来源、立体构型未标。对F1完整tod能力与部分性状有偏强表述，属局部过度确信，未达到系统性把预测写成实证或掩盖主要矛盾。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows explicit null handling, confidence labels, uncertainty statements, and source_type labels.

</details>

## Qwen

答案SHA256：`d75c8ba1b041182758aad2188253606673c54f7f93ca04a945eee29841f6298f`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 答案按题面指定好氧路线返回完整主链：route_scope.chosen_route_name逐字一致，steps&#91;0-3&#93;共四步且每步均给出主底物/主产物英文名与SMILES、一个首选酶及EC、一个对应微生物；同一 Pseudomonas putida F1 去重为单一 organism_profile，并一次给出全部15项性状及 evidence_registry。未见核心模块缺失、指定路线改选或环境条件偏离，按D1 9–10档取9而非10，主要因部分性状仅有 INTERNAL_KNOWLEDGE_ONLY 低置信来源、个别SMILES立体/质子化表示不完整等少量非完整性缺陷；这些缺陷主要归D5/D4/D6评价，不在D1重复重扣。

<details><summary>V0.4理由与本行变化背景</summary>

All required modules delivered: exact route name echoed, four steps with substrate/product names and SMILES, a preferred enzyme with EC per step, a corresponding microorganism, all 15 traits present (10 filled, 5 explicit unknown/null), evidence_registry and uncertainties present. No major task omission or route-name deviation; minor only that many traits are null and no raw_text, which is handled under D4/D5.

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案原文包含 route_scope、四步 steps、单一 organism_profile 的15项性状及 evidence_registry；用于核对交付完整性与任务符合度。
- QUESTION_TEXT / BIOPATH150_021：题面要求指定好氧路线、四步主链格式、每步酶/EC/微生物、15项性状与来源登记；不证明答案科学正确。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_021：本题为 LINEAR_UNIQUE、ordered_step_count=4 的冻结任务材料；仅用于完整性核查，不作为全部旁支必须交付的分母。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：gold存在四步主链及末端产物记录；用于核对答案是否覆盖四步与终点，不代签答案科学正确。
- SCOPE_ROW / SCOPE#BIOPATH150_021#CG04：题面氧条件为 aerobic，且为路线/适用性关键筛选条件；用于核对答案 oxygen_condition 与路线条件回显。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链化学与题面指定路线一致：toluene→toluene-cis-diol→3-methylcatechol→2-hydroxy-6-oxohepta-2,4-dienoate→2-hydroxypenta-2,4-dienoate + acetate，方向为污染物降解向好氧终点，四步底物-产物逐级衔接，终点与gold terminal main products一致。局部问题包括：S1产物SMILES未显式顺式立体化学，S3/S4少列H+等局部质子/计量表示，个别中间体SMILES的质子化/互变异构表达不精确；按P103属局部计量/表示缺陷，不推翻主链。答案S1/S4等EC错配另属D3a评价，不在D2化学维度重复扣分。程序给出D2 nine_ten_eligible=false且允许范围&#91;1,8&#93;，结合主链正确、局部问题有限，取7–8档上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

The four-step main chemistry matches gold: toluene → cis-1,2-dihydroxy-3-methylcyclohexa-3,5-diene → 3-methylcatechol → 2-hydroxy-6-oxohepta-2,4-dienoate → 2-hydroxypentadienoate plus acetate. Direction, ring cleavage, and terminal are correct. Minor local cofactor/leaving-group omissions (H+ in S3/S4) keep it in the 7-8 band rather than 9-10.

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案原文的四步底物/产物、方向与连接关系；用于核对主链化学与连续性，不用于确认酶EC正确性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：gold逐步反应参与者、主底物/主产物、方向与四步连接；支持主链化学框架核对，不覆盖答案全部SMILES立体/质子化细节。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_021：根化合物为Toluene，终点主产物包含Acetate与(2Z)-2-hydroxypenta-2,4-dienoate；支持终点核对。
- E0_EVIDENCE / f3e0:ec:1.14.12.11：官方记录显示toluene dioxygenase/toluene 1,2-dioxygenase系统可催化toluene + NADH + H+ + O2 → cis-diol + NAD+；支持S1化学转化类型核对，但不支持答案将EC写成1.14.12.25。
- SCOPE_ROW / SCOPE#BIOPATH150_021#CG04：题面明确aerobic；用于核对D2环境条件与路线方向，不证明具体菌株能力。

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分3 → V0.5新分4，变化+1。

新裁判理由：

> D3a=4：四个目标步中，S3/S04 的 catechol 2,3-dioxygenase + EC 1.13.11.2 与 accepted set 匹配，可保留；但 S1、S2、S4 三个 KEY 步骤的显式 EC 与 accepted target EC 不符，且 E0 官方条目显示为不同反应：1.14.12.25 为 p-cumate 2,3-dioxygenase（目标 1.14.12.11），1.3.1.53 为二羧酸脱氢酶（目标 1.3.1.19），3.7.1.8 为 2,6-dioxo-6-phenylhexa-3-enoate hydrolase（目标 3.7.1.25）。反应名称/连接大体可读，但关键酶-EC 对应失败，D-KEY4 上界 4；可用部分与失败边界清楚，取 4 而非更低。

<details><summary>V0.4理由与本行变化背景</summary>

Cap: three of four enzyme-EC assignments are contradicted by official EC entries. S1 names toluene dioxygenase but gives EC 1.14.12.25, whose accepted name/reaction is p-cumate 2,3-dioxygenase; S2 names toluene cis-diol dehydrogenase but gives EC 1.3.1.53, a terephthalate dihydrodiol dehydrogenase; S4 names 2-hydroxy-6-oxohepta-2,4-dienoate hydrolase but gives EC 3.7.1.8, HOHPDA hydrolase. S3 EC 1.13.11.2 has no E0 record and remains unverified. Enzyme names are plausible, but the EC correspondence chain fails; 3-4 band, low end.

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:1.14.12.25：官方记录为 p-cumate 2,3-dioxygenase，反应底物为 p-cumate；不支持 toluene dioxygenase 的 1.14.12.25 标注。
- E0_EVIDENCE / f3e0:ec:1.3.1.53：官方记录为 (3S,4R)-3,4-dihydroxycyclohexa-1,5-diene-1,4-dicarboxylate dehydrogenase；不支持 S2 的 toluene cis-diol dehydrogenase 对应。
- E0_EVIDENCE / f3e0:ec:3.7.1.8：官方记录为 2,6-dioxo-6-phenylhexa-3-enoate hydrolase；不支持 S4 的 target 2-hydroxy-6-oxohepta-2,4-dienoate hydrolase 对应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_021：gold accepted ECs：S01 3.7.1.25、S02 1.3.1.19、S03 1.14.12.11、S04 1.13.11.2；支持 S3/S04 的 1.13.11.2，并显示其余三步 EC 不符。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> D3b=7：四步均归 Pseudomonas putida，gold organism_gold 在物种级接受该菌用于 S01–S04，因此主要微生物推荐成立。问题在菌株身份粒度：profile 写 strain F1 但 ncbi_taxid=303，而官方 303 为 P. putida 物种，F1 的 TaxID 为 351746。该粒度不足使 D3b 不能进入 8–10，但未推翻物种级微生物推荐，按 P107 档内扣不 cap。

<details><summary>V0.4理由与本行变化背景</summary>

Pseudomonas putida F1 is a real strain and gold organism rows list P. putida for all four steps, so the species-level attribution is broadly appropriate. However, the profile gives species TaxID 303 rather than strain TaxID 351746, so strain-level identity is under-specified (granularity issue, ladder ①); whole-pathway capability of F1 remains UNRESOLVED (CG09). No verified false species or unrelated taxon; non-cap 7.

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：官方记录为 Pseudomonas putida 物种；支持 species-level 身份，不单独核实菌株 F1。
- E0_EVIDENCE / f3e0:taxid:351746：官方记录为 Pseudomonas putida F1 菌株；用于核对答案 strain F1 的粒度。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_021：gold 在多个步骤接受 Pseudomonas putida 物种级归属；支持物种推荐，不证明 F1 专属 TaxID。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> D4=7：定性性状中 F10 可运动、F11 杆状、F12 革兰氏阴性、F13 不产芽孢与 gold trait_gold 对 P. putida 303 的记录一致；F8 的芳香烃降解有预测级背景。关键数值项 F2/F3/F4/F5/F14 均明确 null，F7/F9/F15 仅内部知识且未核；这些缺口主要影响完整性与局部适用性，未出现把预测当观测或明显误导的性状错误。同物种代表记录可用于参照，但不能回填为 F1 菌株级证据。

<details><summary>V0.4理由与本行变化背景</summary>

Filled qualitative traits for P. putida F1 are mostly compatible with gold: aerobic, motile, rod-shaped, Gram-negative, non-sporulating, and able to degrade aromatic hydrocarbons. F7 toluene utilization, F8 broad aromatic degradation, F9 toluene dioxygenase activity, and F15 habitat are plausible but rely on INTERNAL_KNOWLEDGE_ONLY and are not strain-specific or raw-sourced; quantitative temperature/pH/salinity are honestly null. No grossly wrong numeric or misapplied strain value; 7.

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_021：taxid 303 物种级性状记录支持运动性、杆状、革兰氏阴性、不产芽孢等定性事实；不证明 F1 菌株特异数值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_021：列明哪些性状/子字段可评分或仅作完整性；未核项不应被判为已确证正确或错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_021：温度/盐度等范围端点仍待老师裁定；当前不把缺测或范围待裁定项当错误。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分3 → V0.5新分5，变化+2。

新裁判理由：

> D5=5：核心路线与酶来源主要为 KEGG 通路级 map00623 与 ExplorEnz 名单级（record_id=null），不能逐步定位到具体反应条目；CG05 的 EC-name 对应还存在官方记录矛盾。菌种身份有 NCBI Taxonomy 303 可定位，但只支持 P. putida 物种，不支持 strain F1 的 TaxID，构成 LOCAL 粒度错配；性状来源多为 INTERNAL_KNOWLEDGE_ONLY 或 null。没有已核 SYSTEMIC/CRITICAL 虚构，D5 不 cap；但核心来源映射不足，落在 5–6 档下沿。

<details><summary>V0.4理由与本行变化背景</summary>

Systemic traceability failure. EVID_004 lists EC 1.14.12.25, 1.3.1.53, 1.13.11.2, and 3.7.1.8 as source for S1-S4 enzymes, but official E0 records show 1.14.12.25, 1.3.1.53, and 3.7.1.8 correspond to different enzymes/reactions than claimed. EVID_002 cites species TaxID 303 for strain F1, while E0 shows F1 is TaxID 351746. The route citation is only a KEGG pathway map not in E0, and EC 1.13.11.2 is unresolved. Core enzyme and identity citation chains are broken; cap applied once at the unit level, D5=3.

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持 P. putida 物种身份；不支持 strain F1 的菌株级 TaxID 声称。
- E0_EVIDENCE / f3e0:taxid:351746：官方 P. putida F1 菌株 TaxID；用于核对答案 303 与 F1 的粒度错配。
- E0_EVIDENCE / f3e0:ec:1.14.12.25：官方 p-cumate 2,3-dioxygenase 记录；说明答案的 EC 来源/编号不能支持 toluene dioxygenase 声称。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_021：物种级性状参照；不把代表记录回填为答案已交付来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> D6=7：答案总体区分 DATABASE_DIRECT 与 INTERNAL_KNOWLEDGE_ONLY，性状多处 low/unknown，并明确列出 EC 注释差异、缺失性状与 SMILES 立体化学问题；未把内部知识系统性写成实验观测。扣分点是未披露 TaxID 303 为物种级而 strain F1 另有 351746，且多个错误 EC 以 medium confidence 呈现而未在不确定性中说明。该问题未达到系统性误导，D6 不 cap。

<details><summary>V0.4理由与本行变化背景</summary>

The answer does disclose uncertainties and honestly nulls missing quantitative traits, and evidence source types are labeled. However, it assigns medium confidence to the enzyme EC citations even though three are wrong, gives no specific caveat for S1/S4 ECs, and does not flag that TaxID 303 is species-level rather than strain-level. Some conclusions therefore exceed the disclosed evidence; 5-6 band, upper end.

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：答案实际标注了 DATABASE_DIRECT、INTERNAL_KNOWLEDGE_ONLY 与 low/unknown 置信度，并列出部分不确定性；也显示未披露 strain TaxID 粒度。

</details>

## Grok

答案SHA256：`bf3a74a634fa248c1b22efb668528f12786ff55cf596e61aff133d498808f79a`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步主链、逐步酶与菌、15项性状字段、来源与不确定性均交付，route_scope原样填写；无任务路线偏离。D1按完成度评：F3/F4/F15为明确null，F2数值端点与F14大小/GC亦为空，属诚实未知但反映完成度不足，故取7–8档上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：要求四步主链、每步酶与微生物、15项性状及来源；不证明答案科学正确。
- ANSWER_TEXT / ANSWER：显示答案实际交付四步、菌profile、15性状字段、来源与不确定性；不表示内容均已核实。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_021：gold记录本题为4步线性主链；不作为答案交付完整性的唯一证据。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步连续转化与gold顺序、方向及终点一致：toluene→toluene-cis-diol→3-methylcatechol→2-hydroxy-6-oxohepta-2,4-dienoate→2-hydroxypenta-2,4-dienoate+acetate；S1/S2辅因子较完整。扣分点：S3/S4未列H+产物，SMILES混用中性/离子形式且未指定立体化学；属局部表示/计量缺陷，按7–8档取8，不触发关键错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：支持gold主链连接、方向与终点产物；不认证答案来源或蛋白实验活性。
- E0_EVIDENCE / f3e0:ec:1.14.12.11：官方EC反应支持toluene+NADH+H+ +O2→(1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol+NAD+；不证明具体菌株能力。
- E0_EVIDENCE / f3e0:ec:1.3.1.19：官方EC反应支持dihydrodiol+NAD+→catechol+NADH+H+骨架；不扩展支持未声称底物。

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步目标反应均有可辨认的酶名/EC交付；S1 toluene dioxygenase 1.14.12.11、S2 cis-toluene dihydrodiol dehydrogenase 1.3.1.19、S3 3-methylcatechol 2,3-dioxygenase 1.13.11.2与冻结accepted集合及反应顺序主链相合，S1还可由E0 EC条目直接核对名称/反应/产物。S4酶名与accepted terminal hydrolase一致，但显式EC写作3.7.1.9而accepted/gold为3.7.1.25，且E0无3.7.1.9记录，故该配对保持UNRESOLVED，不能据此判已核失败。gene_or_protein为MINOR可选归属且均待核，路线表示/立体表示为局部待核，未构成已核实KEY失败。按C04/C05在&#91;1,8&#93;内取7：主要对应可靠、剩余问题有限且局部，但不足以给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_021：给出四步accepted酶名/EC集合：S01 terminal hydrolase EC 3.7.1.25；S02 dehydrogenase EC 1.3.1.19；S03 toluene dioxygenase system EC 1.14.12.11；S04 catechol/3-methylcatechol 2,3-dioxygenase EC 1.13.11.2。仅支持参考accepted粒度，不证明答案S4的EC 3.7.1.9正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：支持四步主链的反应顺序/主底物与主产物关系：toluene→dihydrodiol→3-methylcatechol→ring-cleavage product→2-hydroxypenta-2,4-dienoate+acetate；不单独核验S4 EC配对。
- E0_EVIDENCE / f3e0:ec:1.14.12.11：官方EC条目支持toluene dioxygenase/1.14.12.11的名称、反应与(1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol产物；不外推到具体蛋白实测活性或菌株能力。
- E0_EVIDENCE / f3e0:ec:1.3.1.19：官方EC条目支持EC 1.3.1.19属于cis-1,2-dihydrobenzene-1,2-diol dehydrogenase类；accepted集合支持目标S2的名称/EC功能级对应，不证明具体蛋白底物谱或实验活性。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> TaxID 351746由E0确认为Pseudomonas putida F1，菌名/菌株身份对应可靠。步级微生物均归到同一P. putida F1，profile去重合规。但gold/organism_gold的步级与PATHWAY_COMPLETE记录为P. putida物种级（或非F1菌株），F1菌株级单步能力与全路径能力未逐条核验，属身份阶梯“粒度不足”而非已核错配，按7档，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:351746：官方名称为Pseudomonas putida F1；仅支持身份，不支持全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_021：支持P. putida物种级步归属/路径完整记录；不直接证明F1菌株级能力。

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主要表型有物种级记录支持：中温偏好、运动、杆状、革兰氏阴性、不产孢、芳香烃降解。F3/F4/F15为明确null，按D1完成度与D6披露处理而非D4错误。部分F1菌株特异性状/登录号（ATCC 700007、CP000712.1、甲苯唯一碳源、专性好氧）无逐条冻结记录或与物种级记录不完全同粒度，按5–6/7–8边界取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_021：支持P. putida物种级代表性状（mesophilic、motility、rod、Gram-negative、sporulation false、aromatic hydrocarbon等）；不证明F1菌株所有性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_021：显示部分性状子字段可评分/仅完整性；不将待裁决范围转成已核错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_021：说明温度端点等仍待老师冻结政策；不用于宣称答案端点正确或错误。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案evidence_registry五条全部标为INTERNAL_KNOWLEDGE_ONLY；虽给出KEGG/NCBI/ATCC等库名和record_id，但没有交付可定位外部条目、DOI、快照或可核对生成记录，核心路线、酶、身份与性状组均为MISSING_SOURCE，按低分档取2。ATCC 700007、EC 3.7.1.9、CP000712.1等只到UNRESOLVED，不判虚构、不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示所有来源自标INTERNAL_KNOWLEDGE_ONLY；不提供外部可核条目。
- E0_EVIDENCE / f3e0:taxid:351746：仅独立核验身份名称；不把评价证据回填为答案原交付来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确列出终端EC原型差异、SMILES未编码立体化学、辅因子SMILES省略、性状null与F15来源不足，并把来源标为INTERNAL_KNOWLEDGE_ONLY；主要限制与未知披露较具体。但多条内部知识仍给high confidence，证据强度与置信标签部分不相称，未到系统性误导，按7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示不确定性披露与内部知识标签；不证明所披露事实为真。

</details>

## GPT5.6

答案SHA256：`8bb53149a21fff904df0e687369e6de0def448c9b0307182a2ca5e1b3c6bc6fe`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步主链、酶、一个微生物profile和15项性状键均被输出，route_scope的氧条件与路线名也原样给出。但15项性状全为null/未知占位，且冻结路线诊断给出route_status=DEVIATES，D1允许区间为&#91;1,4&#93;；在弱档上沿取4。化学结构/产物错误不在D1重复扣分，分别进入D2/D3a。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求指定路线、每步底物/产物/酶/微生物及15项性状；不支持将null占位视为已完成性状事实。
- ANSWER_TEXT / ANSWER_BEGIN：答案确实交付了四步及15项性状键，但性状值全为null/unknown；支持完整性不足的判断，不证明科学错误。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_021：本题为LINEAR_UNIQUE、ordered_step_count=4的正式案例；只用于确认四步主链范围，不作为全DAG旁支分母。

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 入口步把甲苯转化为名为cis-toluene dihydrodiol的产物，但冻结路线诊断将该步标为NONMATCH/产物结构foreign；末端水解把2-hydroxy-6-oxohepta-2,4-dienoate写成生成2-hydroxypenta-2,4-dienoate加acetaldehyde，而gold末端主产物为acetate，属于核心产物错误。首步与末端均有关键化学错误，另有辅因子/质子省略但非单独扣分主因。D2关键错误成立，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：gold末端S01反应列出主产物(2Z)-2-hydroxypenta-2,4-dienoate与Acetate；未列出acetaldehyde；S03入口产物为(1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol。
- ANSWER_TEXT / ANSWER_BEGIN：答案S4写出Acetaldehyde而非Acetate，S1/S4产物SMILES与gold目标结构不一致；支持D2关键化学错误判断。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 逐目标映射：S04对应答案S3，EC 1.13.11.2与accepted一致，可判S；S02对应答案S2，酶名匹配但EC 1.3.1.58未与accepted 1.3.1.19确认，保持U；S03入口对应答案S1，产物结构按冻结诊断为NONMATCH，判失败；S01末端对应答案S4，accepted为EC 3.7.1.25且生成acetate，答案用EC 3.7.1.9并生成acetaldehyde，判关键失败。S=1、U=1、F=2，且KEY入口/末端失败触发D-KEY4上界≤4；仅一个目标明确可用，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_021：gold/ accepted酶行给出S01末端hydrolase EC 3.7.1.25、S02 EC 1.3.1.19、S03 EC 1.14.12.11、S04 EC 1.13.11.2；只支持参考反应功能粒度，不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_021：gold反应行支持末端产物acetate和入口二羟产物结构；用于核对答案S4/S1的目标反应对应。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 物种Pseudomonas putida正确，gold organism行在四个目标步均出现P. putida（包括S04的P. putida行），E0 taxid 351746又支持‘Pseudomonas putida F1’的菌株身份名称。但答案未给TaxID，且complete_pathway_organism_profile_id=ORG_001属于全路径能力声称；冻结gold的PATHWAY_COMPLETE行是种级P. putida（TaxID 303），不是F1菌株级全路径能力。身份与种级步级归属有支持，菌株级全路径能力待核，判5-6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:351746：支持TaxID 351746的官方ScientificName为Pseudomonas putida F1；不支持其催化各步或完成整条路径的能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_021：支持四个目标步均出现P. putida种级归属，且PATHWAY_COMPLETE行为种级P. putida/TaxID 303；不支持将种级完成路径能力自动扩展为F1菌株级能力。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状键均出现，但全部value=null、confidence=unknown；按P44，全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到具体性状科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求每个organism_profile一次返回全部15项性状；不支持将全null视为已给出可评价性状事实。
- ANSWER_TEXT / ANSWER_BEGIN：答案确实保留15项性状键，但无任何非null值；支持MISSING登记。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的evidence_registry五条全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；路线、酶、微生物和性状没有任何可定位外部来源。按D5六状态，决策相关组均为MISSING_SOURCE，且没有可核实的错引记录，故不cap；但有claim_scope映射，仍属几乎不可追溯的低档，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：答案只交付内部知识型evidence_id和claim_scope，无数据库条目、文献记录或可定位locator；支持MISSING_SOURCE判断。

</details>

### D6 不确定性与诚实度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确把来源标为INTERNAL_KNOWLEDGE_ONLY，且15项性状用unknown/null诚实保留；这部分值得肯定。但多个酶/微生物字段仍给high confidence、evidence_registry medium，而没有任何可定位证据；uncertainties为空，核心化学错误和来源限制未披露。属于多处过度确信但未证明系统性伪造，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案存在internal-only来源标记与全null性状披露，也支持其对多个未定位酶/菌声称使用high/medium confidence且uncertainties为空。

</details>
