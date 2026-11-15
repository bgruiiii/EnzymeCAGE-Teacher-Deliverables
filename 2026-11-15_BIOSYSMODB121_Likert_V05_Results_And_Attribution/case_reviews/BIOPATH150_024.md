# BIOPATH150_024：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-hydroxymandelate degradation

污染物：(S)-4-Hydroxymandelate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 74.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 65.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 59 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 48 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 66.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 42 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`509a7b234f4840d35dd87f4a2974b31601f1f4a4164b034bdba5bfbef771201d`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案原样填写 route_scope.chosen_route_name=4-hydroxymandelate degradation，氧条件null与题面一致；S1–S5均给出底物、产物、酶与对应微生物，两个organism_profiles均完整给出15项性状；S1的EC按题面允许以null标注未知，不因不猜测重扣。S5及route_summary的β-酮己二酸延续属终点后延伸，按P29不额外加分也不因此扣D1。整体模块完整、任务符合度高，仅存在轻微非关键过度延伸，给9。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的路径、逐步酶与微生物、15项性状、证据登记与不确定性说明均已实质交付；chosen_route_name原样填写&#x27;4-hydroxymandelate degradation&#x27;；两profile各15项齐全。少量缺陷：S1未给EC（题面允许未知填null）、ORG_001的F5/F14与ORG_002的F5无任何来源、S1–S3未绑定菌株，故取7–8档上沿8分，未达9–10档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_024：题面指定route_scope.chosen_route_name原样填写、每步需给底物/产物/酶/EC/微生物、15项性状、未知填null
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：该case的pathway_name为4-hydroxymandelate degradation，terminal main products含3,4-Dihydroxybenzoate；与答案route name一致
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：已认可主链P024_1为S05→S04→S02→S01四步并止于protocatechuate；全图其他MISSING/分支不直接构成所评主链漏答
- ANSWER_TEXT / 509a7b234f4840d35dd87f4a2974b31601f1f4a4164b034bdba5bfbef771201d：答案含完整route_scope、S1–S5各字段及两个profile的15项性状；S5为adopted terminal之后的下游延伸
- RUBRIC_CLAUSE / C06：D1完整性与任务符合度锚点
- RUBRIC_CLAUSE / P29：题面终点之外的额外下游延续不加分、未延续不扣分

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 所评主链取P024_1四步。答案S1–S4与gold主链逐步一致：S1 (S)-4-hydroxymandelate→p-hydroxybenzoylformate；S2 p-hydroxybenzoylformate→4-hydroxybenzaldehyde+CO2；S3 4-hydroxybenzaldehyde→4-hydroxybenzoate；S4 4-hydroxybenzoate→protocatechuate。S5为终点后延伸，化学合理，按P29不加分也不扣分。主要问题是S1缺电子传递醌/醌醇、S3缺NAD+/NADH/H+、S4缺NADPH/H+/H2O/NADP+等辅因子；依P103属局部计量缺陷，D2在7–8档且不cap。主链关键转化、方向与终点均正确，少量局部修订可解决，给8。

<details><summary>V0.4理由与本行变化背景</summary>

主链首步（α-羟基酸氧化生成4-羟基苯甲酰甲酸）、脱羧、醛氧化、3-位羟化、3,4-位邻位裂环的方向与连接均与gold S05→S04→S02/S03→S01一致；底物/产物SMILES与gold根、各中间体及终点(protocatechuate)吻合；原儿茶酸之后再给3-carboxy-cis,cis-muconate一步化学成立，属下游延续，按四.2不进入覆盖率定档。缺陷：S1电子传递醌、S3的NAD+、S4的NADPH/H+未作为底物列全，属辅因子遗漏的局部计量缺陷（八.辅因子条款），故落在7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：gold S05/S04/S02/S01定义(S)-4-hydroxymandelate→p-hydroxybenzoylformate→4-hydroxybenzaldehyde+CO2→4-hydroxybenzoate→protocatechuate，并列出醌/NAD+/NADPH等辅因子；P024_1止于protocatechuate
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：相关目标步的accepted酶名/EC：S05 (S)-mandelate dehydrogenase；S04 benzoylformate decarboxylase 4.1.1.7；S02 4-hydroxybenzaldehyde dehydrogenase 1.2.1.28；S01 4-hydroxybenzoate hydroxylase 1.14.13.2
- ANSWER_TEXT / 509a7b234f4840d35dd87f4a2974b31601f1f4a4164b034bdba5bfbef771201d：交付的S1–S4主底物/主产物与主链一致；S1/S3/S4辅因子在substrates/products中省略；S5为下游延伸
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏通常为局部计量缺陷，D2在7–8档处理，不自动cap
- RUBRIC_CLAUSE / P29：额外下游延续不加分，未延续下游不扣分
- RUBRIC_CLAUSE / C06：D2路径科学性与连续性锚点

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 按已给采纳主链 P024_1（S05→S04→S02→S01，起点(S)-4-羟基扁桃酸，终点3,4-二羟基苯甲酸）逐目标核对：答案S1以(S)-mandelate dehydrogenase对应S05（ec_number=null，但名称与ACCSET接受名一致）；S2 benzoylformate decarboxylase EC4.1.1.7对应S04；S3 benzaldehyde dehydrogenase(NAD+) EC1.2.1.28对应S02；S4 4-hydroxybenzoate 3-monooxygenase EC1.14.13.2对应S01。四步底物/主产物与有向反应一致，均属目标主链。S5原儿茶酸开环超出gold终点3,4-二羟基苯甲酸，按D3a只计目标反应，不增加也不作为目标缺失；未选S03旁支及S06消旋支路不在P024_1主链，不按全DAG求并集扣分。主要缺口仅为关键入口S05未给EC（功能名已accepted支持），故落在&#91;7,8&#93;并取8，未达9因显式EC/名号完整性不足。

<details><summary>V0.4理由与本行变化背景</summary>

S2苯甲酰甲酸脱羧酶EC 4.1.1.7、S3苯甲醛脱氢酶EC 1.2.1.28、S4 4-羟基苯甲酸3-单加氧酶EC 1.14.13.2的酶名-反应-EC与gold enzyme_gold.tsv对应一致；S1酶名(S)-mandelate dehydrogenase与gold同一步酶一致，但EC按不猜测规则填null（gold为EC 1.1.99.31）。S5 EC 1.13.11.3超出gold酶表且冻结快照无该EC记录，其酶-反应用常规知识合理但未核。酶催化前几步对4-羟基取代底物的活性系宽底物谱推断且已声明，故取8分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：支持所选主链 P024_1 的四步酶名/EC 与答案 S1-S4 的功能对应；不支持具体蛋白实测或 S06 分支。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：支持答案 S1-S4 的主底物/主产物与有向主链对应；不支持把 S5 原儿茶酸开环计为目标步骤。
- ANSWER_TEXT / ANSWER：显示目标四步已给酶名；S1未给EC；S5为超出3,4-二羟基苯甲酸终点的额外下游。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 多数步骤采用Pseudomonas putida，且S01–S04相应的P. putida物种级身份/步级归属有organism_gold与E0 taxid 303支持；KT2440（taxid 160488）的具体菌株身份与PobA/PcaGH步级能力在E0无记录，属局部未核。没有已核实的核心身份错误，故7档。

<details><summary>V0.4理由与本行变化背景</summary>

各步微生物均为P. putida，gold organism_gold.tsv在S01–S05均列Pseudomonas putida(TaxID 303)，物种级对应成立；S4–S5改用KT2440(TaxID 160488)作菌株级归属，但冻结快照与gold只有303的物种级支持，属身份阶梯①粒度不足（物种级真实记录支持菌株级声称），档内扣分至7档、默认不cap。未见跨属/无关类群或已核实异菌株身份错配；TaxID 160488无冻结记录，保持UNRESOLVED而非虚构。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_024：物种级P. putida出现在多个参考步的微生物行；不证明KT2440菌株级能力。
- E0_EVIDENCE / f3e0:taxid:303：支持TaxID 303= Pseudomonas putida的官方分类名称/状态；不支持KT2440菌株身份，也不支持步级催化能力。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> ORG_001（P. putida 303）的嗜温、pH 7、非嗜盐、好氧呼吸、运动性、杆状、革兰阴性、不产芽孢等多与trait_gold/解释层一致；ORG_002（KT2440）的许多性状与F14数值无E0记录，F2最适温度30°C亦非直接观测子字段，属局部未核。整体有少量未核与强度问题，7档。

<details><summary>V0.4理由与本行变化背景</summary>

P. putida(303)多数性状与gold观测一致：盐度类别&#x27;非嗜盐&#x27;对应gold salinity preference=non-halophilic、可运动对应motility=true、杆状、革兰阴性、不产孢、中温性均获支持；但F5保藏号在ORG_001/ORG_002均填null而gold对303存在CCUG 49576记录（诚实未知只记完成度）、F2 optimum 30 °C与KT2440的F14(6,181,003 bp/61.5% GC)等数值无可核观测来源且以medium置信给出，属少量数值/来源与条件解释问题，落在7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_024：支持P. putida 303的若干物种级观测性状；不支持KT2440菌株级具体数值，也不把培养温度自动等同最适温度。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_024：标注温度上下限等子字段待裁；F2 optimum_c无观测来源，不能按准确值计分。
- E0_EVIDENCE / f3e0:bacdive:12880：支持P. putida mt-2 PaW1/pWWO的菌株记录与培养温度/底物面板；不支持KT2440身份，也不证明所有P. putida菌株相同。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 答案提供了evidence_registry与逐事实evidence_id，但核心路线S1–S3主要依赖EVID_003（PubMed无record_id/locator，为笼统来源），性状大量依赖EVID_001（INTERNAL_KNOWLEDGE_ONLY）；EVID_002指向NC_002947但E0无记录，只能UNRESOLVED。无已核实虚构/错引，NO cap；按部分关键结论可定位、其他模块仍缺映射，5档。

<details><summary>V0.4理由与本行变化背景</summary>

证据登记结构完整（三条evidence含claim_scope与confidence），但内容层级偏低：EVID_003仅写&#x27;PubMed&#x27;、record_id与locator为null，却承担路线步骤、酶系与物种级归属等决策相关结论→GENERIC_SOURCE；EVID_001为INTERNAL_KNOWLEDGE_ONLY（性状）→按四.3记MISSING_SOURCE；仅EVID_002给出条目级RefSeq登录号NC_002947，但其&#x27;KT2440编码pobA与pca基因簇&#x27;等claim_scope在冻结快照无对应记录(GAP-024-005)无法核对→UNRESOLVED_SOURCE。决策相关组(CG01/CG02/CG05/CG07/CG08)全部停留在笼统或未核来源，无已核实条目级可核对结论，故取3–4档上沿4分；无经核实错引，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案以uncertainties、逐step uncertainty与confidence区分推断/未知，明确声明S1–S2为宽底物谱推断、EC null、氧条件null、菌株归属不确定；仅部分内部知识性状仍用high/medium置信呈现，属轻微过度确信，非系统性误导。8档。

<details><summary>V0.4理由与本行变化背景</summary>

答案系统区分证据性质：EC无法确认即填null并列出候选、明确说明S1/S2对4-羟基取代底物为宽底物谱推断、声明S1–S3未能绑定菌株、说明题面氧条件为null而路线按文献好氧构建，并单列uncertainties。仅个别处偏强：&#x27;专性好氧（无氧条件下不生长）&#x27;以high置信给出、KT2440数值以medium置信陈述而未标为记忆值，属单点过度确信（八.D6），档内扣不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`b4f10795f0130161fa535f346c37743aefcc4e9c70747889c823587b55ce2367`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案可解析，route_scope.chosen_route_name逐字保留题面路线名；steps S1–S4对应已认可主链P024_2的S05→S04→S03→S01四个目标转化，逐步给出酶/微生物，单一Pseudomonas putida ATCC 12633 profile去重，15项性状字段齐全（未知按null/unknown），并有证据登记与不确定性说明。扣分点为多个中间体SMILES/EC为null，且S5–S10属主链终点后的下游延伸并放在steps而非可选downstream字段；主链与格式基本完整，按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

档位7（大部分必要内容完整，仅少量遗漏）：10步主链每步均给出主底物/主产物英文名、一个酶（含名称，S1的EC为null）与对应微生物；菌按物种+菌株去重为单条profile，15项性状全部出现（13填写、2明确未知），route_scope.chosen_route_name与题面一致、氧条件按null照实；缺口为6个中间体/辅酶SMILES为null及首步EC未定，属诚实null但仍是必要字段的少量遗漏，未见路线改选或格式损坏。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / b4f10795f0130161fa535f346c37743aefcc4e9c70747889c823587b55ce2367：答案JSON完整；route_scope.chosen_route_name原样；steps S1-S4覆盖已认可主链P024_2的4步；organism_profiles单条去重且15项性状字段齐全；部分SMILES/EC为null并已披露。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：题面路线名为4-hydroxymandelate degradation，起点为(S)-4-Hydroxymandelate；用于核对route_scope名称与起点，不要求全部下游。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：显示adopted main chain P024_2的转化序列S05→S04→S03→S01；仅用于主链覆盖核对，全图其他分支不计缺步。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_024：全图6步/BRANCHED_DAG是参考材料总数，不是本题必须全交付的分母。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链S1–S4的有机转化与P024_2一致且方向正确：S1 (S)-4-hydroxymandelate→4-hydroxybenzoylformate；S2→4-hydroxybenzaldehyde；S3→4-hydroxybenzoate；S4→protocatechuate。S5–S10的β-酮己二酸下游在化学上连贯（开环、内酯化/脱羧、水解、CoA转移、硫解），不构成方向反转或主链跳步。主要问题是多处辅因子/副产物未列（S1电子受体、S2 CO2、S3 NAD+/NADH、S4 O2/NADPH、S5 O2）及若干SMILES为null；按P103这些属局部计量/披露缺陷，不触发D2关键错误，但使答案不能进入9–10。主链和关键转化有充分依据，按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

档位8（主链及关键转化有充分依据，少量局部问题）：S1–S4与gold主支BSY-r03108→BSY-r02852→BSY-r00236/r01489→BSY-r00094的底物/产物与方向逐一吻合（(S)-4-Hydroxymandelate→4-Hydroxybenzoylformate→4-Hydroxybenzaldehyde→4-Hydroxybenzoate→Protocatechuate）；S5–S10的β-酮己二酸开环与转化（3-羧基粘康酸→内酯→氧代己二酸→CoA转移→硫解）化学与方向正确，但位于gold终点下游，按P29额外下游不加分、覆盖率不扣分；未列O2/NADPH/NAD+/琥珀酰CoA等辅因子属局部计量缺陷（P103，7–8档），不cap；无起始步错误、无方向反转、无无说明跳步。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / b4f10795f0130161fa535f346c37743aefcc4e9c70747889c823587b55ce2367：答案steps&#91;0-3&#93;给出与P024_2一致的四个主链有机转化；steps&#91;4-9&#93;给出连续下游转化；同时暴露S2缺CO2、S3/S4等缺辅因子及若干SMILES为null。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：提供P024_2主链S05→S04→S03→S01的底物/产物与辅因子参与事实；用于核对主链化学、方向及辅因子遗漏，不把全图所有分支当必答分母。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：列出主链相关酶名与EC，用于辅助定位S05/S04/S03/S01反应；不据此替D2给酶对应分。
- SCOPE_ROW / SCOPE#BIOPATH150_024#CG04：题面氧条件为null，CG04条件不成立且为SUPPORTING；不能据此把答案使用的需氧/加氧步骤判为题面氧条件违背。

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 按 adopted path P024_1 的四步主链评：答案 S1-S4 依次覆盖 (S)-4-hydroxymandelate→p-hydroxybenzoylformate（S05）、p-hydroxybenzoylformate→4-hydroxybenzaldehyde（S04）、4-hydroxybenzaldehyde→4-hydroxybenzoate（S02）、4-hydroxybenzoate→3,4-dihydroxybenzoate（S01）。S04 的 4.1.1.7、S02 的 1.2.1.28、S01 的 1.14.13.2 与参考 accepted 集合相符；S05 仅给功能名称且 EC 为 null，名称也未逐字等于参考 accepted 的“(S)-mandelate dehydrogenase”，因此不能进入 9-10，但其目标反应方向和底物/产物对应清楚，属于局部编号/名称表达不完整，不把整条主链判为失败。答案 S5-S10 的下游延伸不计入该 adopted path 的目标信用，也不据此抬高 D3a。

<details><summary>V0.4理由与本行变化背景</summary>

档位7：gold覆盖步骤的酶-反应对应正确——S2苯甲酰甲酸脱羧酶4.1.1.7（gold S04）、S3 4-羟基苯甲醛脱氢酶1.2.1.28（gold S02/S03合法注释）、S4 4-羟基苯甲酸3-单加氧酶1.14.13.2（gold S01）；S1酶功能（(S)-4-羟基扁桃酸氧化为4-羟基苯甲酰甲酸）与gold S05的(S)-扁桃酸脱氢酶反应一致，EC按题意留null；S5–S10的EC（1.13.11.3/5.5.1.2/4.1.1.44/3.1.1.24/2.8.3.6/2.3.1.174）与公认途径一致但E0无冻结记录（item gaps），保持待核；未发现EC大类与反应类型互斥或酶名-EC矛盾，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：支持 adopted path P024_1 的目标反应底物—产物方向与端点；不支持答案额外 S5-S10 的下游反应，也不单独确认 S05 的精确酶名/EC
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：支持 S04=4.1.1.7、S02=1.2.1.28、S01=1.14.13.2 的 accepted 酶/EC 对应；S05 的参考 accepted 为 (S)-mandelate dehydrogenase EC 1.1.5/1.1.99.31，不等同于答案的“(S)-4-Hydroxymandelate dehydrogenase”且答案 EC 为 null，故仅支持其目标反应方向而非精确酶编号
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_024：确认本题为 4-hydroxymandelate degradation、BRANCHED_DAG 与 6 步 gold 结构；不能据此把全部分支都当作同一 adopted path 的必答分母

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> P. putida种级在gold中具有步级归属与PATHWAY_COMPLETE支持（303，GCA_024508115.1），答案也使用P. putida与TaxID 303；但答案把全部步骤绑定到ATCC 12633，E0无该菌株级记录，属物种级支持菌株级声称的粒度不足，档内取7，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

档位7（粒度不足档内扣，默认不cap）：全部10步归属Pseudomonas putida（ATCC 12633，TaxID 303）；E0核验种级学名关联SUPPORTED、株-种token关联SUPPORTED，gold organism_gold亦记录P. putida种级PATHWAY_COMPLETE=TRUE，故物种身份与种级完整路径能力有支持；但&#x27;ATCC 12633本株完成整条10步路径&#x27;属菌株级能力声称，E0步级归属(L2)与完整路径能力(L3)均UNRESOLVED，属P107①粒度不足→档内扣；无跨属/跨kingdom错配、无无关类群编号，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持TaxID 303为Pseudomonas putida当前分类记录；不支持ATCC 12633菌株级身份或菌株级能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_024：支持P. putida 303参与所列步骤及种级全路径能力；不等同于ATCC 12633菌株级验证。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 15项性状字段齐全；运动性、杆状、革兰氏阴性、不产孢等与P. putida 303的gold记录一致，降解/酶活等主要性状大体可用。扣分点：pH最小/最大为6.0/8.5，而可评的种级记录为5/8；温度端点与最适值仅部分重叠/无最适观测；盐度与基因组两项为null。主要性状仍可核实，故取7而非9-10。

<details><summary>V0.4理由与本行变化背景</summary>

档位6（部分性状准确适用，但关键项证据不足且存在可核数值不符）：可核性状与种级gold一致——运动性true、杆状、革兰氏阴性、不产孢、好氧呼吸/末端受体O2（记录nitrate reduction=false、denitrification=false）；但pH两个可评分数值子字段不符：pH minimum填6.0（gold种级观测=5）、pH maximum填8.5（gold=8），均为exact-match分母；F5保藏号ATCC 12633不在冻结P. putida记录（CCUG 49576；ATCC 33015/DSM 3931等）内，属待核（P52：不因株不同自动判错，但也不回填）；F7/F8/F9具体底物利用与酶活声称无冻结记录；温度/盐度端点按mask为pending_teacher_adjudication，不作准确性判定；未见&#x27;预测冒充观测&#x27;或离谱数值，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_024：支持P. putida 303的运动性、形态、Gram、产孢、温度/盐度范围、底物与酶活记录；种级记录不等于ATCC 12633菌株级验证。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_024：支持pH可评标量为5和8，答案6.0/8.5构成数值不符；温度端点标为pending，不据此判CONTRADICTED。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案evidence_registry仅含EVID_001/EVID_002，source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；所有决策相关claim组均为MISSING_SOURCE，无法从具体路径、酶或性状追到可定位条目。MISSING_SOURCE默认不cap，但D5落在1-2档；其证据ID组织有一定可读性，取2。

<details><summary>V0.4理由与本行变化背景</summary>

档位2（低分档）：evidence_registry仅两条，均source_type=INTERNAL_KNOWLEDGE_ONLY且database/record_id/locator全为null，无法定位到条目级证据，全部claim group只能登记MISSING_SOURCE（P34：按低分档评定，默认不触发cap）；无任何经核实的错引，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不执行cap；身份字段（TaxID 303）在事实层被E0支持，但不改变答案原交付来源状态，也不回填为模型证据（OBS-D5-IDENT/OBS-POS-LOCATABLE）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_SECTION：支持答案只交付internal knowledge标签，未交付可定位数据库/文献/计算记录；不把事后gold回填为原交付来源。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案有逐步uncertainty、null值与confidence标签，并明确部分SMILES/EC未确定；但总体仅有两条笼统uncertainties，若干EC或性状（如部分EC、F5/F12/F13）用high/medium包装且无来源，证据类型与置信强度不完全相称。属局部过度确信/披露不足，未达系统性误导，取6。

<details><summary>V0.4理由与本行变化背景</summary>

档位6（有不确定性说明，但部分结论强度超过依据）：正面——未知项（多个SMILES、S1的EC、F4盐度、F14基因组）如实置null，逐步给出confidence与uncertainty说明，且evidence.source_type一律自报INTERNAL_KNOWLEDGE_ONLY，未把预测写成观测；负面——多条性状与路径结论以medium/high置信呈现却无来源，未说明性状系种级代表记录向菌株外推、未提示需复核，也未声明相对gold终点的范围边界；属单点/局部过度确信而非系统性误导，按P119档内扣，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_SECTION：支持答案确实披露了部分未知/低置信；也支持部分字段仍以较高置信呈现而无来源。

</details>

## Kimi

答案SHA256：`585e8bf8336c41a2c65952eecb0cc747b6a891b52f6572f4aa4faffc452b8466`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 路线名称按要求原样填写，steps 1–3均给出底物/产物、SMILES、首选酶与对应微生物，15项性状也全部出现，模块关联基本清楚；但按本题已认可主链，主链需由S05→S04→S02/S03→S01四步到达3,4-Dihydroxybenzoate，答案仅把前3步作为主链并在4-hydroxybenzoate处结束，末端S01（4-hydroxybenzoate hydroxylase，EC 1.14.13.2）只在downstream_continuation/central_metabolism_entry中文字提及，未作为必答主链step给出对应微生物与主产物关联。该遗漏属必要主链内容不完整，归5–6档；其余结构完整、关联较清楚，取6。

<details><summary>V0.4理由与本行变化背景</summary>

8分档：路径、酶、菌、15项性状、来源与不确定性均有实质交付，route_scope.chosen_route_name原样保留；但主链只列三步，并把4-hydroxybenzoate→protocatechuate放入downstream，较gold六步BRANCHED_DAG少一主链步骤，属重要范围/完整性缺口，未到9-10分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：确认题面路线名与gold终点包含3,4-Dihydroxybenzoate，用于范围核对；不证明答案其他内容错误
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：显示S05→S04→S02/S03→S01构成到3,4-Dihydroxybenzoate的四步主链，S01是末端羟化步；不把全图未选分支当作必答分母
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：确认S01对应4-hydroxybenzoate hydroxylase/EC 1.14.13.2，用于确认答案未作为主链step交付的末端步身份；不自动核验答案蛋白级活性

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 按已认可主链评价现有主链化学：答案给出的4-hydroxymandelate→4-hydroxybenzoylformate→4-hydroxybenzaldehyde→4-hydroxybenzoate三步有机主转化方向一致、产物连续，未出现方向反转、主链首步错误或无依据跳入中心代谢物。S2脱羧未列H+、S3未列NAD+/NADH，均属辅因子/计量局部缺陷，按P103–P105通常不触发D2关键错误；S1采用的O2/H2O2氧化与gold S05的脱氢酶电子受体不同，主要有机转化仍成立，酶—EC归属留D3a。缺少S01末端羟化步按范围/完整性问题归D1，不另用覆盖率硬扣D2。综合存在多处局部计量与主链边界表述问题，7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

8分档：S1氧化、S2脱羧、S3醛氧化三步方向与主产物正确，SMILES与原子守恒基本成立；S2未列H+、S3底物未列NAD+，属局部计量/辅因子遗漏，按P103在7-8档处理，不cap。首步酶学选择归D3a，不在D2重复扣。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：核对S04脱羧含H+、S02/S03醛氧化含NAD+/NADP+与水等辅因子，以及各主产物的有机转化；仅作化学连续性/局部计量核对，不自动把不同酶选择判为D2关键错误
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：确认S04苯甲酰甲酸脱羧酶EC 4.1.1.7与S02/S03醛脱氢酶条目存在，用于辅助判断答案所给三步有机转化并非凭空跳跃；不核验具体底物谱或实验活性

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> 按采用主链 P024_1（S05→S04→S02→S01）评判：S04 的 benzoylformate decarboxylase EC 4.1.1.7 与 S02 的 4-hydroxybenzaldehyde dehydrogenase EC 1.2.1.64 有 accepted 支持；但 S05 关键入口答成 4-hydroxymandelate oxidase EC 1.1.3.19（O2/H2O2），与 gold 的 (S)-mandelate dehydrogenase EC 1.1.5/1.1.99.31（电子传递醌）不符，不能计 S；S01 关键终点被明确排除在 steps 之外，仅放在 downstream_continuation，主链止于 4-hydroxybenzoate，漏掉生成 3,4-dihydroxybenzoate 的末端步。因此存在关键入口不匹配与关键终点漏交付，D-KEY4 上界 4，按部分可用且关键主功能受损给 3。

<details><summary>V0.4理由与本行变化背景</summary>

8分档：S2 EC 4.1.1.7 benzoylformate decarboxylase与S3 EC 1.2.1.64 4-hydroxybenzaldehyde dehydrogenase均与gold酶表相符；S1 EC 1.1.3.19 4-hydroxymandelate oxidase在E0无记录且gold S05用EC 1.1.99.31，属首步酶-EC待核的局部问题，不足以推翻整维。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：支持这些步骤的 accepted 酶/EC 集合；不支持答案 S05 的 EC 1.1.3.19 作为该锁定步骤的 accepted 匹配。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：支持 S05 为醌依赖脱氢反应，以及 S01 为生成 3,4-dihydroxybenzoate 的末端羟基化；不支持答案以 O2/H2O2 氧化酶步骤替代 S05，也不支持主链止于 4-hydroxybenzoate。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：支持 3,4-dihydroxybenzoate 为 gold 终产物之一；不支持将 4-hydroxybenzoate 作为完整主链终点。
- RUBRIC_CLAUSE / C04：支持已确认 KEY 步骤 F/M 时 D3a 上界为 4。
- RUBRIC_CLAUSE / C05：支持在受限范围内按部分可用与关键失败严重程度选 3 分，而非机械取 4 分。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> P. putida物种级身份与全路径能力在organism_gold中有支持（taxid 303, PATHWAY_COMPLETE），但答案把各步统一归到ATCC 12633菌株级；E0仅有P. putida 12880记录，ATCC 12633与各步催化能力未核，故取5–6档中段6，不作已核错误cap。

<details><summary>V0.4理由与本行变化背景</summary>

7分档（粒度不足/待核）：P. putida为gold多步与PATHWAY_COMPLETE支持的物种；但答案把全部步骤归到ATCC 12633菌株，E0仅有P. putida种级TaxID 303与另一株mt-2 PaW1记录，ATCC 12633菌株级记录未核，按身份阶梯①档内扣、不cap；答案已声明代表性归属，未把它写成全路径菌。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida物种级TaxID 303官方记录；不自动核实ATCC 12633菌株身份或各步催化能力。
- E0_EVIDENCE / f3e0:bacdive:12880：为P. putida mt-2 PaW1/pWWO记录，保藏号含ATCC 33015等；不核实ATCC 12633，也不证明ATCC 12633各步能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_024：显示P. putida taxid 303为PATHWAY_COMPLETE候选之一；不证明答案为ATCC 12633菌株级归属。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> P. putida物种级多项定性性状（运动、杆状、革兰阴性、不产孢）与trait_gold一致；温度/盐度只有偏好/类别，pH与基因组为明确null，关键定量项不足；F1‘严格好氧’较gold代表记录aerotolerant略强，未达已核错误，故5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

6分档：F6/F10/F11/F12/F13与gold种级表型一致，F2/F4偏好/类别与gold mesophilic/non-halophilic相符；但F2/F3/F4/F14关键数值缺失，F1“严格好氧”与gold aerotolerant记录不完全一致，F5 ATCC 12633未核，F9写成“4-hydroxymandelate氧化到4-hydroxybenzoate的酶活组合”不是单一酶活，关键项证据与条件解释需修订，故5-6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_024：P. putida代表记录支持运动性、杆状、Gram-negative、不产孢等定性性状；物种级代表不等同ATCC 12633菌株级全部性状。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_024：显示pH min/max、温度端点、盐度端点等为scoreable或pending/不可scoreable子字段；用于判断关键定量缺口，不用于把null判错。
- E0_EVIDENCE / f3e0:bacdive:12880：未包含ATCC 12633；其培养温度为26/30°C记录，不能回填ATCC 12633或外推为最适温度。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案给出数据库/条目/EVID映射，但CORE路线CG01-CG03只有MetaCyc自由文本无record_id；EC 1.1.3.19/4.1.1.7/1.2.1.64、ATCC 12633、DSMZ记录均不在E0，无法核对支持内容；只有taxid 303物种身份可在E0核对。属部分关键结论可定位、其他核心缺映射的5–6档，取5，因核心路线来源仍笼统。

<details><summary>V0.4理由与本行变化背景</summary>

6分档：决策相关组有EC号、TaxID 303、ATCC 12633等可定位线索，但E0只含f3e0:taxid:303与f3e0:bacdive:12880；EC 1.1.3.19/4.1.1.7/1.2.1.64、ATCC 12633、MetaCyc/BacDive条目均无冻结记录可核，EVID_001/EVID_006又缺record_id，属部分关键结论可定位、其他记录不完整；无经核实错引，不cap，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持P. putida物种级TaxID 303记录存在；不支持ATCC 12633菌株级身份或EC/路线条目。
- E0_EVIDENCE / f3e0:bacdive:12880：为P. putida另一个菌株记录；不能核实EVID_005/EVID_006所称ATCC 12633/DSM 291，也不支持各EC条目。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 答案用confidence、uncertainties、null明确标注未知，并说明氧条件未指定、S2酶专一性中等、代表菌归属；但ATCC 12633及多项高置信性状缺少E0级披露，单点过度确信，未达系统性误导，故7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

8分档：uncertainties明确写出氧条件null、S2脱羧酶专一性中等、代表菌可替换；各字段用high/medium/low/unknown标注，未把预测写成实证；F1/F9等个别高置信表述略强，但属单点，不构成系统性误导，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案原文含不确定性说明、confidence分层及null未知；同时可见部分高置信性状无raw_text且ATCC 12633未披露核验缺口。

</details>

## Qwen

答案SHA256：`f4c6ffa5205d873c95571c63a81a0e4809b34db48167d8f67826106854d29c8d`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 按已认可主链（P024_1/P024_2）应覆盖 S05→S04→S02/S03→S01 四步，其中S01为4-hydroxybenzoate→3,4-dihydroxybenzoate末端。答案只给S1、S2两步：S1从(S)-4-hydroxymandelate直接到4-hydroxybenzaldehyde，S2到4-hydroxybenzoate；未交付4-hydroxybenzoate→3,4-dihydroxybenzoate，且以一步氧化脱羧替代S05/S04的p-hydroxybenzoylformate中间过程。route_scope名称与格式、逐步骤酶/菌、15项性状外壳均已给出，故非无输出；但主链关键内容缺失较多，只能落在5–6档下沿。

<details><summary>V0.4理由与本行变化背景</summary>

主要模块均有涉及：2步主链含底物/产物英文名+SMILES、每步酶+EC、对应菌，15项性状字段齐全（9填/6 null），含evidence_registry与uncertainties；route_scope.chosen_route_name按题面原样填写。但主链只到4-hydroxybenzoate，相较4-hydroxymandelate degradation路线（gold ordered_step_count=6、BRANCHED_DAG）遗漏4-hydroxybenzoate→protocatechuate末步，且温度/pH/盐度/保藏/基因组/栖息地6项为null。属5–6档，格式与模块覆盖较完整故档内取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：提供S05→p-hydroxybenzoylformate、S04→4-hydroxybenzaldehyde、S02/S03→4-hydroxybenzoate、S01→3,4-dihydroxybenzoate的gold反应行；用于核对已认可主链步骤，不证明gold穷尽所有替代路线
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：列出各步accepted酶名/EC，含S05 (S)-mandelate dehydrogenase、S04 benzoylformate decarboxylase、S01 4-hydroxybenzoate hydroxylase；用于说明缺失/替代步骤背景，不评价具体蛋白实测活性
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：路径终端主产物含3,4-Dihydroxybenzoate；用于核对主链终点范围，不代表其他替代路线必然错误

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> S1为(S)-4-hydroxymandelate经O2氧化脱羧生成4-hydroxybenzaldehyde、CO2、H2O2，主碳骨架与产物连接可通；S2为4-hydroxybenzaldehyde经NAD+脱氢生成4-hydroxybenzoate、NADH、H+，与gold S02同向且连续。主要问题是答案主链止于4-hydroxybenzoate，未将S01 4-hydroxybenzoate→3,4-dihydroxybenzoate列入主链而只放downstream；S1还以4-hydroxymandelate oxidase一步氧化脱羧替代gold S05+S04并绕过p-hydroxybenzoylformate，缺可核支持。按C06，化学可成立替换仍≤6；当前主干部分成立但关键末端转化缺失、合理性证据有限，取5–6档下沿。未发现方向反转或明显不守恒等可确认的D2关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

S2（4-hydroxybenzaldehyde+H2O+NAD+→4-hydroxybenzoate+NADH+H+，醛脱氢酶）与gold S02/S03一致；S1用4-hydroxymandelate oxidase一步氧化脱羧生成4-hydroxybenzaldehyde，净反应以4-hydroxymandelic acid计C/H/O配平、O2/CO2/H2O2在列（底物写阴离子、产物按中性计，存在1个质子/电荷记账差，属局部计量），但绕开gold的(S)-mandelate dehydrogenase(S05)+benzoylformate decarboxylase(S04)两步、缺p-hydroxybenzoylformate中间体，酶-反应对应未核实；且缺4-hydroxybenzoate→protocatechuate(S01)。主干化学部分成立、关键中间体与转化仍需修订、证据仅内部知识，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：提供S02的4-hydroxybenzaldehyde+NAD+→4-hydroxybenzoate+NADH+H+反应行，以及S05/S04/S01的化学步骤；用于核对答案已给步骤的化学方向与连续性，不证明替代氧化酶路线必然错误
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：路径终端主产物含3,4-Dihydroxybenzoate；用于核对答案止于4-hydroxybenzoate而未完成末端转化

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 答案仅交付两步。第1步把(S)-4-hydroxymandelate经4-hydroxymandelate oxidase直接转为4-hydroxybenzaldehyde，这与目标S05（经(S)-mandelate dehydrogenase生成p-hydroxybenzoylformate）不符，属于另一反应而非目标主链。第2步主底物/主产物为4-hydroxybenzaldehyde→4-hydroxybenzoate，与S02主反应相符，酶名4-hydroxybenzaldehyde dehydrogenase也可在accepted名称中找到，但给出的EC 1.2.1.44不在该步accepted EC集合中，故只能算局部有用对应，不能算完整S。S04、S01、S06未交付：无p-hydroxybenzoylformate脱羧步、无3,4-dihydroxybenzoate终产物、无(R)-4-hydroxymandelate消旋步。KEY_ENTRY S05与KEY_TERMINAL S01失败/缺失，符合KEY上界；整体仍属核心目标推荐失效，仅有少量局部可用信息，按C05 2分档选择2。

<details><summary>V0.4理由与本行变化背景</summary>

酶功能类别与步骤方向合理（S1氧化酶氧化CH-OH，S2醛脱氢酶→酸）；但EC 1.1.3.46与EC 1.2.1.44在冻结证据快照中均无记录(GAP-024-007/012)，无法核accepted name/reaction与条目状态；1.2.1.44亦不在gold对同名酶4-hydroxybenzaldehyde dehydrogenase所用EC集合(1.2.1.28/1.2.1.64，gold非穷尽，不据此判错)。有合理候选、部分支持，关键步骤缺具体核验→5档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：显示目标S05、S01、S06的主底物/主产物，不支持答案S1把(S)-4-hydroxymandelate直接转为4-hydroxybenzaldehyde，也不支持答案止于4-hydroxybenzoate。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：显示各目标步可接受酶/EC；不包含答案S05所用的4-hydroxymandelate oxidase/EC 1.1.3.46，也不将EC 1.2.1.44列入S02 accepted EC集合。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：确认题面起点及两个终产物范围；不等同于答案已完成主链。
- RUBRIC_CLAUSE / C05：支持在核心目标推荐仍失效但存在少量局部可用信息时选择2分，而非自动给1分或按命中率取中值。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Pseudomonas putida TaxID 303 is an official species identity, and gold records PATHWAY_COMPLETE for TaxID 303. The no-strain species-level presentation is acceptable for species identity, but the step-level attribution of P. putida to the answer&#x27;s 4-hydroxymandelate oxidase lacks a frozen step-level capability record, so this is a 7 not 8.

<details><summary>V0.4理由与本行变化背景</summary>

身份Pseudomonas putida / TaxID 303经E0核实（f3e0:taxid:303：names含Pseudomonas putida、record_status=CURRENT）SUPPORTED；gold organism_gold中P. putida(303)为各步合法菌且pathway_complete=TRUE，菌-路径关联有据；未给菌株（允许null，菌株级未涉）；步级酶-菌归属（尤其氧化酶步）为L2 UNRESOLVED、完整路径能力L3为UNRESOLVED。主要身份与对应有可靠支持，仅具体步级归属待确认→7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Official taxonomy record supports TaxID 303 = Pseudomonas putida at species level; it does not support any particular step-level catalytic activity.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_024：Gold organism rows support P. putida assignments and a PATHWAY_COMPLETE row for TaxID 303; they do not confirm the answer&#x27;s specific oxidase step.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> Several P. putida traits match gold observations: motility, rod morphology, Gram-negative, no sporulation; aerobic respiration and oxygen terminal acceptor are plausible. However F7-F9 make target-substrate utilization, degradation, and enzyme-activity claims that are not supported by the frozen trait panel, and the answer uses medium confidence for those unsupported specifics. This is partial usability with key trait evidence gaps, so 6.

<details><summary>V0.4理由与本行变化背景</summary>

F10可运动、F11杆状、F12革兰氏阴性、F13不产孢与trait_gold(303,OBSERVED)一致；F1好氧、F6好氧呼吸/O2为合理默认；但F7(以4-hydroxymandelate为碳源)、F8(降解至4-hydroxybenzoate)、F9(具两酶活性)系由路径外推，trait_gold无对应观测记录，属把推断当性状(标medium)且未限定范围；F2/F3/F4/F5/F14/F15为null属完成度(记D1)。部分性状准确适用、关键外推项证据不足→5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_024：Gold trait observations for TaxID 303 support motility, rod shape, Gram-negative, and no sporulation; F7 panel does not list 4-hydroxymandelate, and specific F9 4-hydroxymandelate oxidase activity is not established.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> Decision-relevant claims use only EVID_001/EVID_002 with source_type=INTERNAL_KNOWLEDGE_ONLY; there is no locatable database record, literature DOI/locator, or computation record. Under D5 MISSING_SOURCE applies to core groups, so the score is in the low band. No verified mis-citation is asserted, so no D5 cap is triggered.

<details><summary>V0.4理由与本行变化背景</summary>

全部证据EVID_001/EVID_002均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null，无任何可定位文献/数据库/计算记录与结论建立可核对对应关系→MISSING_SOURCE；决策相关组(CORE/APPLICATION_CRITICAL)全部缺失→低分档；TaxID 303虽正确但不构成路径/酶/性状声称的来源。无已核实错引，按条款默认不cap。1–2档取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> The answer explicitly lists oxygen-condition uncertainty, unknown strain/collection/genome data, stereochemistry not encoded, incomplete cofactor SMILES, and downstream scope exclusion. Many traits are honestly null. The main deduction is that several INTERNAL_KNOWLEDGE_ONLY metabolic claims are still given medium confidence without a clear prediction/observation distinction, and complete_pathway_organism_profile_id is asserted despite only two steps being shown.

<details><summary>V0.4理由与本行变化背景</summary>

source_type诚实标注INTERNAL_KNOWLEDGE_ONLY（未伪装数据库直查）；逐项confidence多low/unknown；uncertainties逐条列出（氧条件null/(S)构型未在SMILES/辅因子SMILES缺/下游未入主链/菌株与保藏未知）；未知性状填null。缺点：酶/路线以medium包装未核实内容、F7/F8/F9以medium把推断呈现为性状，略超依据，属档内扣、非系统性误导。7档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`29cb9ad1e40d8045bc186fcfc36276393b4b947c1bd23a16988ec28054535f55`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求的路线名、逐步底物/产物/SMILES、首选酶及EC、对应微生物、15项性状字段和证据登记均已实质交付；答案声明并完成S05→S04→S02→S01到原儿茶酸的连续主链，racemase支路明确列为非评分替代分支。仅有氧条件题面未指定而答案在route_scope中自行判为好氧并说明理由，属轻微边界解释，不构成重要模块遗漏或范围偏离；9–10档取9。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：Defines pollutant, route name and terminal compounds; used for task-scope completeness only, not as proof of every branch.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：Shows the connected S05→S04→S02→S01 path to protocatechuate; not evidence that all DAG branches were required.

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步化学主链连续且方向正确：S1醇氧化为酮、S2脱羧、S3醛脱氢、S4单加氧羟基化至原儿茶酸；SMILES、主产物和步骤连接与gold反应方向一致。S1电子受体泛化、S2以H+表示脱羧环境属局部计量/表达简化，按P103不自动cap，但足以避免9–10档；8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：Supports directed transformations S05, S04, S02 and S01 on a connected main chain; not all parallel branches.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：Shows accepted enzymes for the same reaction steps; enzyme names/EC are evaluated separately in D3a.

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按答案声明的连续主链S05→S04→S02→S01评：S05 EC1.1.99.31、S04 EC4.1.1.7、S02 EC1.2.1.28、S01 EC1.14.13.2均落在accepted sets，名称与EC无已核矛盾。S06 mandelate racemase是替代终支，S03是与S02同反应的并行支路，未纳入该主链不构成已选主链漏步；因分支正式绑定缺失且9–10门不可用，取允许高档&#91;7,8&#93;上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：Accepted enzyme/EC rows support the four delivered target functions at curation G4; they do not prove protein-specific activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：Supports reaction direction and step connectivity for S05/S04/S02/S01; S06 is a separate alternative branch.

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案把四步均归给Acinetobacter calcoaceticus NCIB 8250（TaxID 471）并声称完整路径能力。身份写法具体，但E0没有该菌株的claim-linked记录；gold PATHWAY_COMPLETE列的是Pseudomonas putida、P. fluorescens、Aspergillus niger等，不能反证A. calcoaceticus错误，但也未支持其对四步的整路能力。标准属级特征不能替代菌株级整路能力证据，故按有合理候选但关键能力未充分核验给5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_024：Lists gold organism/step associations and PATHWAY_COMPLETE organisms; does not include or verify A. calcoaceticus NCIB 8250.

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 给出的F1专性好氧、F6好氧呼吸、F10不运动、F11球杆菌、F12革兰氏阴性、F13不产芽孢与Acinetobacter常见分类性状相符；温度/pH/盐度/基因组/栖息地以null明确未知，处理诚实。但F7以目标底物为唯一碳源、F8降解谱、F9 L-扁桃酸脱氢酶活性均是无冻结记录支持的具体菌株能力声称，属关键项证据不足，故给6而非7–8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_024：Gold trait rows cover listed Pseudomonas/Sphingomonas/Saccharomyces/Aspergillus organisms, not A. calcoaceticus NCIB 8250; no direct verification for this profile.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_024：Shows scoreability and observed/unknown status by organism for this case; no A. calcoaceticus row is present.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部EVID_001–EVID_003均为INTERNAL_KNOWLEDGE_ONLY，database和record_id为null，仅给内部标签与概括性locator；重要路线、酶、菌和性状结论均无法沿可定位数据库/文献条目核查。属MISSING_SOURCE低分档；无已核实错引，不触发D5 cap。因证据ID与claim_scope内部映射尚可读，取2而非1。

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确列出EC历史混淆、电子受体未定、NCIB 8250物种界定/基因组未核实、EC归属未逐条复核、路线边界等不确定性，并将多项未知填null；证据性质以INTERNAL_KNOWLEDGE_ONLY标注。少数标准分类性状给high confidence但无外部记录，属局部过度确信而非系统性误导，故取8。

## GPT5.6

答案SHA256：`c6087b814fd2ad90ff9be2c2034f55716a65337bad42eafb3e1e0584f9c510ce`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给出一条连续四步主链并绑定酶与一个微生物profile，route_scope名称原样且氧条件保持null；但两步缺EC、15项性状全为null、来源均为INTERNAL_KNOWLEDGE_ONLY，完整性仅达较弱档上沿。按本题D1允许范围&#91;1,4&#93;取4；未把分支全图行数当缺步分母。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：支持答案实际交付的四步链、两步缺EC、15项性状全null；不证明其科学正确性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_024：本题gold为BRANCHED_DAG，全图ordered_step_count不等于单条主链必答分母；不能据此把未选旁支全算缺步。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步化学连接整体成立：氧化、脱羧、醛氧化、4-羟基苯甲酸羟化到protocatechuate；但S1底物SMILES O=C(O)&#91;C@H&#93;(O)c1ccc(O)cc1与题面/gold指定的(S)-4-Hydroxymandelate立体构型冲突，属显式立体冲突，按D2候选锚点≤5。辅因子未列属局部计量问题，不单独cap；故取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：gold S05指定(S)-4-Hydroxymandelate，支持S1立体冲突判断；gold链支持其余三步方向，不支持把S1的SMILES视为(S)。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_024：题面/gold根化合物为(S)-4-Hydroxymandelate；不证明答案中任何具体SMILES正确。

</details>

### D3a 目标反应与酶对应：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按答案可对应的已认可主链P024_1（S05→S04→S02→S01）评D3a。S01/S02有目标反应与accepted EC层面的部分支持；S04无EC且酶名不在accepted名单，S05关键入口无EC且路线诊断为NONMATCH/STEREO待核，均属未确认U而非已证F；全图S03/S06属未选分支，不按所评主链缺步扣分。因部分主干目标可用但仍有MAJOR/关键入口待核，不能进7–8档，按C04不取区间中点、取&#91;5,6&#93;下沿5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_024：给出S01/S02/S04/S05等目标步的accepted酶名与EC：S01有4-hydroxybenzoate hydroxylase/p-hydroxybenzoate hydroxylase EC 1.14.13.2；S02的accepted EC集含1.2.1.3；S04为benzoylformate decarboxylase EC 4.1.1.7；S05为(S)-mandelate dehydrogenase EC 1.1.5/1.1.99.31；不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_024：给出用于对应答案的S05→S04→S02→S01主链底物/产物与有向连接；支持目标反应定位，不自动确认答案酶名-EC配对。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 物种级Pseudomonas putida在gold各相关步及E0 taxid303中有支持，答案统一使用P. putida KT2440 (taxid160488)属同物种但不同菌株；E0无160488记录，且答案complete_pathway_organism_profile_id=ORG_001宣称完整路径能力但无对应实验证据。身份未被证明错误，按合理候选+部分支持取5-6档上沿6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_024：gold有P. putida taxid303的步级/全路径记录，以及P. fluorescens等；不支持KT2440 taxid160488的菌株级能力，也不证明其不能。
- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida种级taxid303身份；不支持KT2440或整路径能力。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles&#91;0&#93;.traits的F1-F15全部value为null、confidence=unknown；没有可评价的性状内容。按P44/P112及全部必需性状null规则，D4记MISSING=1，不宣称检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_024：gold中存在若干对P. putida可评分性状；答案交付全null，支持MISSING而不判科学错误。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所有关键结论的evidence_registry条目均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null，无法沿文献或数据库条目定位；属MISSING_SOURCE低档。无已核实错引，不触发D5 cap；给2而非1因仍保留了内部evidence_id与claim_scope映射。

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / P34：MISSING_SOURCE/INTERNAL_KNOWLEDGE_ONLY按低分档且默认不cap；不把缺失当虚构。
- ANSWER_TEXT / ANSWER_TEXT：答案实际只交付内部知识标签，无外部可定位来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案多处明确低/unknown置信，uncertainties列出氧条件未指定、前两步酶/EC/菌株直接证据不足、无KT2440完整路径实验证据；未把预测系统性写成实证。小瑕疵是仍以complete_pathway_organism_profile_id=ORG_001表达整路径归属，故取8而非9。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：支持不确定性披露与低置信标注；不证明科学内容正确。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；本答案大部分披露具体，故不cap。

</details>
