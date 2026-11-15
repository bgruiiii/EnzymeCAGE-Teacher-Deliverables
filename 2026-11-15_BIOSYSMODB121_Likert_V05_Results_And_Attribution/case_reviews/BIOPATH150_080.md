# BIOPATH150_080：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：ferulate degradation

污染物：(2E)-3-(4-hydroxy-3-methoxyphenyl)prop-2-enoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 46.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 52.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 56 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 41 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 65 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 40 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`6d90f2e9d209289aed4b4f037650b8e7e0570a3b4d6fa7a93daed9de29f77e2c`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 全部要求模块均有实质交付：10步主链、每步酶与EC、每步微生物、15项性状、来源与不确定性均有对应内容。但冻结路线诊断显示S01 NONMATCH、S02/S03未按冻结主链绑定，答案在S2直接合并feruloyl-CoA到vanillin+acetyl-CoA并延伸到下游，故任务符合度/完整性只能落在D1允许的&#91;1,4&#93;内，取4而非更低，因为交付是完整的、局部关联清楚。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块全部实质交付：route_scope.chosen_route_name原样回填&#x27;ferulate degradation&#x27;；10步均给主底物/主产物英文名与SMILES、一个首选酶与一个对应微生物；单一菌株profile按&#x27;物种+菌株&#x27;去重；15项性状中14项有实质值、F4盐度整体明确未知（非遗漏）；evidence_registry与uncertainties齐备。仅5个步骤EC按题面允许填null，属题面明示可接受的诚实缺失而非模块遗漏；整体无范围偏离或工程缺陷，故取7–8档内高分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BIOPATH150_080：题面要求ferulate degradation主链、逐步酶/EC、对应微生物、15项性状；支持完整性任务范围，不支持答案路线步骤已被正确绑定。
- GOLD_SLICE / reaction_gold.tsv：冻结gold给出S01→S03→S02的三步主链及方向；支持路线对齐判断，不证明答案的合并S2或下游延伸获得目标信用。
- ANSWER_TEXT / ANSWER_BIOPATH150_080：答案确实交付了完整模块；不支持其步骤边界与冻结gold一致。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分9 → V0.5新分5，变化-4。

新裁判理由：

> S1的CoA硫酯化、S3香草醛氧化、S4 O-脱甲基、S5原儿茶酸3,4-开环以及后续β-酮己二酸途径基本化学连贯；但S2把冻结gold的S03水合中间体与S02醛缩裂解合并为一步feruloyl-CoA→vanillin+acetyl-CoA，丢失3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA中间步，且S01表示/立体诊断NONMATCH。主干部分成立但关键中间连接需修订，落在D2允许的&#91;1,5&#93;内取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与方向整体正确且连续：S1腺苷酸化生成feruloyl-CoA（ATP+CoA→AMP+PPi合规）；S2以水合-醛缩裂解净生成vanillin+acetyl-CoA（与双功能HCHL一致，答案显式写明该机制）；S3香草醛氧化为香草酸；S4 Rieske型O-脱甲基生成原儿茶酸+甲醛；S5 3,4-双加氧开环生成3-carboxy-cis,cis-muconate；S6内酯化、S7脱羧、S8内酯水解、S9 CoA转移、S10硫解至succinyl-CoA+acetyl-CoA，均符合β-酮己二酸途径。键级、切断位点与SMILES一致，无起始步错误、无方向反转、无未说明跳步。扣分点为局部辅因子简化（O-脱甲基以游离甲醛表示、未写THF载体；S3未落H+），属7–8档局部计量缺陷级别，不改变主要结论；答案延伸至gold终点（vanillin+acetyl-CoA）下游，按P28/P29不作覆盖率扣分亦不加分，故取9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：gold S01 ferulate→feruloyl-CoA，S03 feruloyl-CoA→3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA，S02→vanillin+acetyl-CoA；支持S2合并/漏中间体的判断。
- ANSWER_TEXT / ANSWER_BIOPATH150_080：答案S2直接给feruloyl-CoA→vanillin+acetyl-CoA；支持合并步骤和S01表示差异，不支持其完全对齐冻结S01/S03/S02三步边界。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> D3a按目标反应逐行判。程序路线事实已固定：S01为确认的KEY失败（NONMATCH，STEREO_CONFLICT_SPECIFIED），触发D-KEY4上限≤4；S02/S03仍为未确认对齐，不能当作S。当前已确认S=0，故只在低带&#91;1,2&#93;取分；答案虽给出可辨认的feruloyl-CoA synthetase与feruloyl-CoA hydratase/lyase等局部酶信息，但核心入口目标失效且无任一必答步达到已确认目标支持，故不取3–4；取2而非1，是因为仍存在少量可定位的酶名/EC与accepted集合可比对的局部信息，但该信息不转化为目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶名与反应类型逐一对应，无&#x27;水解酶解释羟化&#x27;或&#x27;名称为加氧酶而编号为脱氢酶&#x27;类矛盾：S1连接酶（6.2.1.34，落在gold对feruloyl-CoA synthetase的6.2.1.12/6.2.1.34多注集合内，按四.5保守条款不扣分）；S2 HCHL（金标酶名一致，EC 4.2.1.101无法核验）；S5原儿茶酸3,4-双加氧酶EC 1.13.11.3、S8烯醇内酯酶EC 3.1.1.24、S9 CoA转移酶EC 2.8.3.6均为对应反应类型的合理具体号但冻结证据无法核对；S3/S4/S6/S7/S10按题面允许填null并写明原因。属&#x27;主要步骤酶对应有可靠支持、若干条目仍需确认&#x27;的7档，不构成D3a关键错误（错引问题归D5，不作为本维KE依据）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：给出本题S01–S03金标目标反应、方向与终点；支持S01入口反应/结构对齐失败及S02/S03未对齐的核对，不证明答案的替代合并步骤已获目标信用。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_080：给出S01 accepted feruloyl-CoA synthetase/EC 6.2.1.12|6.2.1.34及S02/S03 hydratase/lyase无观察EC；仅支持accepted集合比对，不把S02/S03答案合并步骤自动确认为目标完成。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 全部步骤统一指向Pseudomonas putida KT2440（TaxID 160487），身份定位本身可读，但冻结gold的step organism为Sphingomonas sp. SYK6，且pathway-complete记录中无KT2440；EVIDENCE_GAP使KT2440身份/全路径能力不能核验。没有已核跨属/无关类群错配，故不触发身份关键错误；但把整条ferulate主链归为单一KT2440能力属未核的路径级声称，取5。

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤归属单一菌株Pseudomonas putida KT2440（TaxID 160487），菌名/菌株/TaxID三件套内部自洽，物种为已知芳香族降解模式菌，属可接受候选；但&#x27;该菌株逐步催化并独自完成整条ferulate→β-酮己二酸主链&#x27;的能力声称主要依赖内部知识与KT2440基因组文献，未获条目级反应/能力证据；S1–S2的化学反应证据引用的却是Pseudomonas sp. HR199菌株的文献，与本答案菌株粒度不匹配。按身份阶梯与三层核验（身份定位≠反应级能力≠全路径能力），身份合理、能力未充分核验→5–6档；因核对不到推翻主要微生物推荐的反证（EVIDENCE_GAP），不判关键错误、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：冻结organism_gold的step organism为Sphingomonas sp. SYK6，pathway-complete列表不含KT2440；支持KT2440全路径能力未由gold确认，不证明其绝对不能降解。
- ANSWER_TEXT / ANSWER_BIOPATH150_080：答案声称KT2440单菌完成整条主链；支持能力声称存在，不支持其已获E0核验。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项性状全部返回，F4明确未知，若干性状与KT2440常见描述一致且给出证据标签；但冻结trait记录无KT2440，温度、pH、ATCC号、基因组大小/GC、底物谱等均不能核验，约占关键性状主体。按已给内容、明确未知与未核缺口评5，不把未核直接当错。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现（14项有值、F4盐度整体明确未知），关键性状取值与KT2440的通行描述相符：好氧、革兰氏阴性、杆状、极生鞭毛运动、不产芽孢、最适约30 °C、pH中性、基因组NC_002947约6.18 Mb、GC约61.5%；ATCC 47054按low confidence标注并写入&#x27;需核对&#x27;，SMILES与性状层区分了未知。扣分点：全部性状证据为EVID_001内部知识或通用文献，无菌株级条目来源；温度把&#x27;常规培养温度30 °C&#x27;与最适值并列，存在培养温度/最适温度混用风险；F14数值未逐位核对。属&#x27;部分性状准确且适用、关键项证据不足或条件解释需修订&#x27;的5–6档，因E0无性状记录无法核实但不构成已核实错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：冻结trait_gold只覆盖Sphingomonas及其他pathway-complete菌，无KT2440；支持KT2440性状未获冻结记录核验，不支持其数值必错。
- ANSWER_TEXT / ANSWER_BIOPATH150_080：答案完整给出15项并披露ATCC低置信、SMILES推导等；支持不确定披露存在，不支持性状数值已核实。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案实际交付evidence_registry并逐条给出source_type、database/locator、claim_scope；主链部分有EVID_005/006文献定位，基因组有RefSeq/Taxonomy记录号，但核心路线与性状大量依赖EVID_001 INTERNAL_KNOWLEDGE_ONLY。E0为EVIDENCE_GAP，引用不能核验，按UNRESOLVED_SOURCE/MISSING_SOURCE登记，不判虚构；部分关键结论可定位、部分缺映射，取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案确实交付了证据登记（6条）并把evidence_id映射到步骤、酶与性状，其中EVID_002/005/006为可定位的书目条目（作者/年份/期刊/卷期页），EVID_003/004为带record_id的数据库条目（NC_002947、160487），故不是纯GENERIC_SOURCE；但E0整题EVIDENCE_GAP（entries=0），这些条目是否实际支持所声称内容一律无法核对，只能登记UNRESOLVED_SOURCE，另有多条核心声称（route_summary、S4 vanillate O-demethylase、全部生理性状）仅依赖INTERNAL_KNOWLEDGE_ONLY的EVID_001，登记MISSING_SOURCE。决策相关组（CG01/02/03/05/07/09、CG08/17）呈MISSING+UNRESOLVED混合、无已核实错引（不得判虚构/不得判CONTRADICTED），故落&#x27;部分关键结论可定位、其他模块仍缺可核对映射&#x27;的5–6档，取5；不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_080：答案提供来源类型和文献/记录定位；支持D5可读映射存在，不支持这些来源已在E0核实。
- GOLD_SLICE / trait_gold.tsv：冻结trait记录无KT2440；支持答案KT2440性状来源未在本地gold核验，不判其引用虚构。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案区分了INTERNAL_KNOWLEDGE_ONLY、LITERATURE_DIRECT、DATABASE_DIRECT，列出未确认EC、推导SMILES、低置信ATCC等，未系统性把预测写成观测；但route_summary与complete_pathway_organism_profile_id把KT2440完成整条主链表述得较强，相关能力未核且很少直接披露。属单点/局部过度确信而非系统性误导，取6。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且分层：逐条列出未确认的EC（香草醛脱氢酶、O-脱甲基酶、环化异构酶、脱羧酶、硫解酶）、明确说明ATCC 47054为低置信记忆需核对、说明β-carboxymuconolactone与muconate的SMILES为按机制推导、并声明&#x27;各步证据以经典文献与内部知识为主，未逐条核对原始数据库记录&#x27;；证据类型标签使用规范（INTERNAL_KNOWLEDGE_ONLY/LITERATURE_DIRECT/DATABASE_DIRECT区分清楚），confidence与依据大体相称。不足在于：整条主链可由KT2440单菌完成、严格好氧、革兰氏阴性等断言给high confidence却主要由内部知识支撑，属单点过度确信倾向；未造成系统性误导、未掩盖主要矛盾。按D6严重度条款为档内扣分而非cap，取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_080：答案披露多处EC/SMILES/ATCC不确定性，同时把KT2440全路径能力写为确定总结；支持D6局部过度确信判断。

</details>

## DeepSeek

答案SHA256：`c5ce61fe39ca8b586282e1dc7cba5f07e892696698e15c453953f31b8cabea3e`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 主要模块均已涉及：route_scope正确填写ferulate degradation，steps给出底物/产物、酶、微生物，organism_profiles给出15项性状及来源字段，JSON结构完整。但若干必答主产物的SMILES为null（如feruloyl-CoA、acetyl-CoA及多个下游主产物），且gold主链的3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA中间步未被单独交付，S2将两步合并；另有下游延伸未明确标注为非主评分链。属于主要模块在但若干必要内容遗漏/关联不够完整，落5–6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

任务符合度：route_scope.chosen_route_name原样为ferulate degradation（未改选路线），oxygen_condition按题面null保留；10步连续主链，每步均有主底物/主产物英文名、酶名+EC、一个对应微生物，organism_profiles按物种+菌株单条去重（ORG_001）并被步级引用；15项性状全部返回（F4盐度以子键全null表达明确未知，符合题面&#x27;未知填null&#x27;）；evidence_registry按内部规则连续编号且引用自洽。缺陷：feruloyl-CoA、acetyl-CoA、3-carboxy-cis,cis-muconate、4-carboxymuconolactone、3-oxoadipate enol-lactone、3-oxoadipate、3-oxoadipyl-CoA、succinyl-CoA等约9个主产物smiles为null，结构信息仅部分实质交付；15项性状的evidence_id全部指向同一内部知识条目（&#x27;各项最强来源&#x27;未实质满足）。故属&#x27;大部分必要内容完整、关联清楚、少量遗漏&#x27;的7–8档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案覆盖10个步骤、1个菌株profile和15项性状；多个主产物SMILES为null，S2合并feruloyl-CoA hydratase/lyase两步并延伸至下游。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_080：本题路线ferulate degradation，gold ordered_step_count=3，LINEAR_UNIQUE，用于核对主链规模与任务范围。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_080：gold终点主产物为Vanillin|acetyl-CoA；用于判断下游延伸是否属于题面终点之外内容。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链化学方向与连续性总体正确：S1阿魏酸活化为feruloyl-CoA；S2给出feruloyl-CoA hydratase/lyase整体转化为vanillin+acetyl-CoA；S3–S5香草醛氧化、脱甲基、原儿茶酸开环，S6–S10 β-酮己二酸途径至acetyl-CoA/succinyl-CoA，方向均为降解方向。主要辅因子在多数步骤列出；未发现首步错误、方向反转或不守恒等关键化学错误。局部问题是S2合并gold中同一酶的两个表示步，且额外下游步骤未标为non-scored continuation；不改变主要化学结论。按7–8档取8；本案D2 9–10不适用。

<details><summary>V0.4理由与本行变化背景</summary>

化学主链：S1 ferulate + ATP + CoA → feruloyl-CoA + AMP + diphosphate（连接酶步，与gold S01底物/产物一致）；S2 feruloyl-CoA + H2O → vanillin + acetyl-CoA为双功能feruloyl-CoA hydratase/lyase的净反应，覆盖gold S03（水合生成3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA）与S02（裂解为vanillin+acetyl-CoA）两步，属合理简化而非错误；S3–S10为香草醛→香草酸→原儿茶酸→3-羧基黏康酸→4-羧基黏康酸内酯→3-氧代己二酸烯醇内酯→3-氧代己二酸→3-氧代己二酰CoA→乙酰CoA+琥珀酰CoA，是教科书β-酮己二酸（protocatechuate branch）途径，方向、碳数与主要辅因子（NAD+/NADH、O2、H2O、琥珀酰CoA）自洽，未见原子明显不守恒或无说明跳步。下游段超出gold题面范围（gold 3步、终点Vanillin|acetyl-CoA），按四.2不进入覆盖率扣分、按四.5作为未证实延伸登记。局部问题：S2未标出被合并的水合中间体；S2把乙酰CoA标为byproduct（gold标MAIN_PRODUCT）；多个CoA类化合物结构为null。主链结论不受影响，8档取中。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案主链从ferulate经feruloyl-CoA到vanillin+acetyl-CoA，并延伸至protocatechuate及β-ketoadipate；多数步骤含辅因子说明。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：gold主链反应S01–S03的底物、产物、方向为SUBSTRATE_TO_PRODUCT；用于核对主链方向和终端产物。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_080：gold root为ferulate，terminal main products为Vanillin|acetyl-CoA；答案在S2达到该终端，后续为额外下游。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按3个必答目标反应核对：S01目标ferulate→feruloyl-CoA，答案S1酶名feruloyl-CoA synthetase、EC 6.2.1.34，与accepted集中该步可接受名称/EC相符，可记S。S02/S03目标为feruloyl-CoA hydratase/lyase相关步骤；答案S2酶名与该accepted名称相符，但其显式EC 4.2.1.98在accepted集中为NOT_OBSERVED，显式EC配对仍U；同时答案未单独交付S03的3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA中间产物，S2以合并反应表示，目标步归属/表示仍需裁定。故仅1/3目标明确为S，C=1/3落&#91;3,4&#93;；两个KEY/MAJOR相关目标仍未解决或未按步交付，边界不足以支持取上沿，取3。未发现可登记为Y的已核实关键错误，key_error记UNRESOLVED。

<details><summary>V0.4理由与本行变化背景</summary>

酶-反应对应：S1 feruloyl-CoA synthetase / EC 6.2.1.34与gold enzyme_gold同酶名同号（gold另注6.2.1.12，属多注集合内合法值）；S2酶名feruloyl-CoA hydratase/lyase与gold完全相同（gold该酶EC为NOT_OBSERVED，答案自填4.2.1.98无法核验）；S3 vanillin dehydrogenase 1.2.1.67、S4 vanillate O-demethylase 1.14.13.82、S5 protocatechuate 3,4-dioxygenase 1.13.11.3、S6 3-carboxymuconate cycloisomerase 5.5.1.2、S7 4-carboxymuconolactone decarboxylase 4.1.1.44、S8 3-oxoadipate enol-lactonase 3.1.1.24、S9 3-oxoadipate CoA-transferase 2.8.3.6、S10 3-oxoadipyl-CoA thiolase 2.3.1.174——各EC大类与反应类型均相配（连接酶/水合裂解酶/醛脱氢酶/Rieske单加氧酶/双加氧酶/环异构酶/脱羧酶/内酯水解酶/CoA转移酶/硫解酶），未见EC大类别与反应类型不匹配或酶名与EC互相矛盾。但10个EC中仅6.2.1.34有gold参照，其余8个均无冻结记录（item_gaps逐一登记：GAP-080-004/005/008/009/010/012/014/017/019/021/025/028/031/034/036/038/041/044/046/049），属&#x27;有合理候选与部分支持、若干关键步骤仍缺具体核验&#x27;的5–6档，取6；无已核实错配，不触发关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S1酶名/EC为feruloyl-CoA synthetase 6.2.1.34；S2为feruloyl-CoA hydratase/lyase 4.2.1.98，并将feruloyl-CoA直接转为vanillin+acetyl-CoA，未单独给出3-hydroxy中间体。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_080：gold/ accepted行显示S01可接受feruloyl-CoA synthetase且EC含6.2.1.12与6.2.1.34；S02/S03均为feruloyl-CoA hydratase/lyase且EC为NOT_OBSERVED；支持S01为S、S02/S03显式EC配对为U。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：gold S01–S03的具体底物/产物显示S03应生成3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA，而答案S2未单独交付该中间产物。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_080：本题required main chain为3步，用于计算D3a的N=3与S/N覆盖。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer uses Pseudomonas putida KT2440 (TaxID 160488) for every step and marks complete_pathway_organism_profile_id=ORG_001. Identity is plausible, but no step-level or whole-path capability evidence is delivered beyond INTERNAL_KNOWLEDGE_ONLY; gold uses Sphingomonas sp. SYK6 for required steps but a different organism is not automatically wrong. This fits the 5-6 band; choose 5 because the whole-path capability claim is unsupported.

<details><summary>V0.4理由与本行变化背景</summary>

身份三件套与作用范围：全部10步统一指派 Pseudomonas putida KT2440（TaxID 160488，organism_profile_id=ORG_001），并设 complete_pathway_organism_profile_id=ORG_001、route_summary称其经β-酮己二酸途径降解ferulate——即同时作&#x27;身份定位&#x27;&#x27;步级反应能力&#x27;&#x27;整条路径能力&#x27;三层声称（P69）。身份粒度（菌株级+TaxID）内部自洽，物种为公认芳香族降解菌、作为候选合理；gold步级菌为Sphingomonas sp. SYK6（TaxID 502559），但gold非唯一允许答案，仅因物种不同不判错（四.5/P27）。问题：TaxID 160488在E0无记录（GAP-080-061/064），整条路径能力声称无任何独立实验/数据库依据，且答案以单一步级内部知识把概念层面的物种/单步常识扩写为全路径能力，属&#x27;关键身份或作用范围未充分核验&#x27;的5–6档，取5。冻结证据既不能证实也不能证伪该菌株能力，故本维key_error记UNRESOLVED（疑似粒度/能力外推，不cap、不计已核实关键错误）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_080：Gold lists Sphingomonas sp. SYK6 for the required steps and other PATHWAY_COMPLETE organisms; it does not establish KT2440 capability, and absence is not a contradiction.
- ANSWER_TEXT / ANSWER.organism_profiles.ORG_001：Answer claims P. putida KT2440 for all steps and as complete-pathway organism, with only INTERNAL_KNOWLEDGE_ONLY support.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> All 15 trait slots are present; F4 salinity is explicitly unknown. Many values are plausible species/strain traits, but every trait source is INTERNAL_KNOWLEDGE_ONLY with null raw_text/locator, and E0 has no KT2440 trait record. Specific F14 genome values and F5 accession are unverified. This fits the 5-6 band; choose 5.

<details><summary>V0.4理由与本行变化背景</summary>

性状正确性与适用性：15项全部返回，身份对象为KT2440菌株级，未把物种级观测硬套到其他菌株。F4盐度五子键全null属明确未知（P45/P112：诚实null不计错误，也不与遗漏等同）。其余14项给出具体值：最适30°C/mesophilic、&#x27;obligate aerobe&#x27;、pH 7.0、ATCC 47054、aerobic/O2、广谱芳香族利用（含ferulate、vanillate、protocatechuate）、β-酮己二酸途径、三种酶活、polar flagella运动、rod-shaped、Gram-negative、non-sporulating、NC_002947.3 / 6,181,873 bp / 61.5%、土壤与根际广适——量级与类别均无&#x27;离谱到误导筛选&#x27;之处，且全部标confidence=low、raw_text=null、evidence_id=EVID_013（INTERNAL_KNOWLEDGE_ONLY）。关键缺口：E0对taxid 160488的性状子字段全部NO_TRAIT_RECORD_IN_SNAPSHOT（GAP-080-106…119），trait_scoreability_mask显示KT2440不在本题observed_accuracy分母中，因而任一数值（含ATCC号、基因组登录号/大小/GC）都无法核实；温度/pH/盐度三组在本题scope为SUPPORTING（题面未限定），不构成应用关键误引。综合为&#x27;部分性状合理且适用，但关键项证据不足&#x27;的5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_080：Gold trait rows cover Sphingomonas sp. SYK6 and PATHWAY_COMPLETE organisms, not P. putida KT2440; no KT2440 trait values are provided.
- ANSWER_TEXT / ANSWER.organism_profiles.ORG_001.traits：Answer gives all 15 traits for KT2440, with low confidence and EVID_013 INTERNAL_KNOWLEDGE_ONLY.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> Evidence_registry contains only INTERNAL_KNOWLEDGE_ONLY entries (EVID_001-EVID_013) with null database, record_id, and locator. Under D5 six-state rules this is MISSING_SOURCE for all claim groups. No locatable source supports any main conclusion. The answer at least labels evidence IDs and claim scopes, so choose 2 rather than 1.

<details><summary>V0.4理由与本行变化背景</summary>

可追溯性按claim group判：evidence_registry EVID_001–EVID_013 全部 source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，claim_scope仅重复酶名+EC或&#x27;Pseudomonas putida KT2440 traits&#x27;；所有 step.reaction_evidence_id（EVID_002、004–012）、step.microorganism.evidence_id（EVID_003）与全部性状evidence_id（EVID_013）都指回这些自我声明。按P34，&#x27;仅有INTERNAL_KNOWLEDGE_ONLY类自我声明&#x27;即MISSING_SOURCE；决策相关组（CORE：CG01/CG02/CG03/CG05/CG07/CG09；APPLICATION_CRITICAL：CG08/CG17）无一具备条目级可定位可核对结论，故只能落低分档，不能进5–6档（P41）。全部缺失属&#x27;缺失而非误导&#x27;，默认不触发关键错误（P34/P41），E0亦无已核实错引（EVIDENCE_GAP），故key_error=N、severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。低分档取2而非1：答案把证据类型如实标为内部知识、未伪造任何数据库条目或登录号条目，且事实层映射（fact→evidence_id）自洽。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：All 13 evidence entries are INTERNAL_KNOWLEDGE_ONLY with null database/record/locator; no traceable source.

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> The answer uses low confidence for most traits and medium for enzymes, and source_type INTERNAL_KNOWLEDGE_ONLY, giving some evidence-nature labeling. But uncertainties is empty, no limitations or conflicts are discussed, and medium confidence on catalytic steps exceeds the internal-only support. This fits the 5-6 band; choose 5.

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界表述：uncertainties为空数组、steps&#91;*&#93;.uncertainty全为null、route_summary/notes无任何&#x27;预测/推断/未核实/局限&#x27;说明；10步在仅INTERNAL_KNOWLEDGE_ONLY证据下统一标confidence=medium，且未提示三处实质性局限——(i) S2把gold的水合与裂解合并、省略3-hydroxy中间体；(ii) S3–S10超出gold终点（Vanillin|acetyl-CoA）属未核实延伸；(iii) KT2440整条路径能力与全部性状数值均无来源。属&#x27;多处过度确信、证据类型与置信度不相称、主要限制未说明&#x27;的3–4档。正面之处：所有证据条目诚实标为INTERNAL_KNOWLEDGE_ONLY（未冒充DATABASE_DIRECT/LITERATURE_DIRECT观测）、性状confidence=low、F4盐度填null，部分未知被如实记录，不构成&#x27;系统性把预测写成实证观测&#x27;，未达cap门槛（P119/P171），故key_error=N，档内取4。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Source type is self-declared INTERNAL_KNOWLEDGE_ONLY; uncertainties array is empty and no limitations are stated.

</details>

## Kimi

答案SHA256：`df28384e4bb3596ef205e15afb56df977d57ee554110cfd012164191c43b4969`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 答案交付了路径、酶、微生物、15项性状槽位和证据注册等模块，但冻结route diagnosis将必答S01绑为NONMATCH、S02为MISSING、S03为UNKNOWN，route_status=DEVIATES；在D1允许&#91;1,4&#93;内，因任务主链符合度受限取4，其余模块完整度不足以解除该门。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖全部要求模块：路线5步含主底物/主产物英文名与SMILES、每步一个酶+EC与对应微生物、4个organism_profiles各15项性状、evidence_registry与uncertainties。route_scope.chosen_route_name 原样填写 &#x27;ferulate degradation&#x27;，氧条件 null 原样保留。JSON可解析。多项性状为明确 null（未知，非遗漏，按P15不重扣D1）；S3–S5 为题面未指定终点下的合理下游延续，不构成范围偏离。档位8：大部分必要内容完整、关联清楚，仅少量性状留空/工程层面的 record_id 缺失。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Defines the frozen required directed main-chain steps and terminal products; does not by itself prove the answer&#x27;s delivered chemistry.
- GOLD_SLICE / enzyme_gold.tsv：Lists accepted enzyme rows for the required steps; does not automatically validate route alignment or every answer organism.

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 主链化学大体成立：S1为CoA活化，S2为水合/逆羟醛裂解生成vanillin+acetyl-CoA，S3-S5的氧化、O-去甲基化和开环方向总体合理。但route diagnosis记录S01为STEREO_CONFLICT_SPECIFIED/NONMATCH，且答案把S03水合中间体并入S2净反应，缺少明确中间体步，连续性仍需修订；在D2允许&#91;1,5&#93;内取5。

<details><summary>V0.4理由与本行变化背景</summary>

起始步 ferulate+ATP+CoA→feruloyl-CoA+AMP+PPi 与 gold S01 一致；S2 以水合/逆羟醛裂解生成 vanillin+acetyl-CoA，等价 gold S03+S02（合并为一步，属酶催化机制上的简化，P104 不自动判错）；下游 vanillin→vanillate（醛脱氢）、vanillate→protocatechuate（氧化O-去甲基，释甲醛）、protocatechuate→3-carboxy-cis,cis-muconate（3,4-内二醇开环）方向、原子守恒与连接均合理，主要辅因子在列。gold 终点为 vanillin+acetyl-CoA（3步），S3–S5 属题面未指定终点下的合理延续，按P28/P29 不计 gold 范围外覆盖率扣分。档位8：主链及关键转化合理，仅 S2 合并两步略简化。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Supports the required chemical sequence and terminal vanillin/acetyl-CoA; does not require all downstream continuation to be scored.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> 冻结计数为S=0、F=1、U=2：S01为已确认KEY入口失败，S02/S03仅为alignment未确认，不能补成已支持。局部酶名/EC有参考价值，但目标反应主推荐失效；D-KEY4将候选带压到&#91;1,4&#93;，无已支持目标时取2。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶名与反应类型一致：CoA连接(6.2.1.34)、水合/裂解(4.2.1.101)、醛脱氢(1.2.1.67)、O-去甲基单加氧(1.14.13.82)、内二醇双加氧(1.13.11.3)。S1 EC 6.2.1.34 属 gold S01 可接受集(6.2.1.12/6.2.1.34)之一，无矛盾；S2 已声明 EC 4.2.1.101 覆盖水合半反应、裂解由同一蛋白完成（简化但披露）。其余 EC 在 E0 无可核记录，保持 UNRESOLVED 待核（未核≠错）。档位7：主要步骤酶对应合理，多个 EC 待核。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：Gold enzyme rows define accepted targets; S01 still route-failed and S02/S03 remain unresolved, not confirmed support.
- GOLD_SLICE / reaction_gold.tsv：Gold reactions define required transformations; they do not make unresolved answer alignments supported.

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 步骤微生物对应总体合理：HR199、P. fluorescens AN103在gold的PATHWAY_COMPLETE组织名单中出现，S3用SYK-6与原step organism一致；ADP1用于下游开环也属常见模型菌。主要不足是多数TaxID为null、步骤级能力依赖未核文献/内部知识，9-10证据门不成立；故取8。

<details><summary>V0.4理由与本行变化背景</summary>

各步菌均真实且在 gold organism 集中出现：Pseudomonas sp. HR199（gold pathway_complete 登记 TaxID 86003，用于 S1/S4）、P. fluorescens AN103（gold pathway_complete &#x27;No TaxID&#x27;，S2）、Sphingomonas paucimobilis / Sphingobium sp. SYK-6（gold STEP TaxID 502559，S3，答案披露异名）、Acinetobacter baylyi ADP1（TaxID 62977，S5，gold 未列但为 pca 经典模式菌）。三层区分：身份真实；步级反应归属与文献对象一致（AN103-Ech、SYK-6-LigV、HR199-VanAB、ADP1-PcaHG）；complete_pathway_organism_profile_id=ORG_001(HR199) 与 gold pathway_complete 登记一致。TaxID 多填 null（如实），ADP1 TaxID 待核。档位7：主要菌-反应对应可靠，个别 TaxID/属名归属待核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：Lists SYK-6 as step organism and HR199/AN103 as pathway-complete organisms; does not prove every answer step-level attribution or ADP1 downstream role.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 四个profile均返回15项性状字段，未知多为null并标注low/unknown，未把预测直接写成观测。部分性状有文献或数据库定位，但HR199/AN103的形态、运动性、革兰氏、产孢等多依赖EVID_011内部知识，SYK-6/ADP1基因组数值和若干温度/碳源值未能核验；属部分可用但关键项证据不足，取6。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状多为属/种级定性事实（革兰氏阴性、杆状、好氧、不产芽孢、Pseudomonas 运动 / Acinetobacter ADP1 不运动），基本相同且多标注 &#x27;属级推断/low&#x27;；多数定量性状（温度/pH/盐度/保藏号）如实填 null（明确未知）。SYK-6 基因组 AP012222/4199332 bp、ADP1 NC_005966/3598621 bp/40.3% GC 量级合理但 E0 不可核。问题：SYK-6 F2 optimum_c=30 取自&#x27;常规培养约30°C&#x27;，属培养温度≠最适温度（P113）的条件解释偏差；多项属级推断被填为菌株性状。档位6：部分性状准确且适用，关键定量项证据不足/条件解释需修订。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Most gold trait cells are UNKNOWN; only some observed identity/genome fields are present. Does not confirm the answer&#x27;s filled trait values.
- GOLD_SLICE / trait_scoreability_mask.tsv：Indicates many traits are completeness-only and not observed-accuracy denominators.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv：Shows subfields pending/not scoreable; does not support answer values beyond the frozen masks.

</details>

### D5 来源与可核查性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> evidence_registry为S1-S5给出具体作者/期刊/页码或GenBank样的定位，且步级与profile级有claim_scope映射；EVID_011仅internal for形态/一般性状，已如实标low。E0为EVIDENCE_GAP，无法核验引用实际支持内容，故不判错引；按可定位性与映射质量取7，9-10需内容核验。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 提供 8 条，核心路线/酶/身份/部分基因组可映射到具体文献题录或数据库条目并带 claim_scope（如 S1_reaction、ORG_001_traits），结构上可追溯。但本案为 EVIDENCE_GAP：全部文献题录与访问号无可核事实，一律按 UNRESOLVED_SOURCE 待核（未核≠虚构≠CONTRADICTED）。一般表型性状（F1/F6/F10–F13）仅 EVID_011 INTERNAL_KNOWLEDGE_ONLY → MISSING_SOURCE。决策相关组(CG01/02/03/05/07/08/09/17)并非仅笼统来源，且无经核实错引，故不触发 cap。档位6：部分关键结论可定位但均待核，其他模块缺外部来源映射。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Supports that specific locators and claim scopes were delivered; does not confirm their bibliographic content.
- RUBRIC_CLAUSE / P40：UNRESOLVED_SOURCE is not treated as fabricated or automatically low; it is scored on known delivery/source-location facts.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确保留未知、null、low/medium confidence、EC归属不确定、SYK-6命名变更和氧条件未指定但实际需氧等限制，并把alternative_branches标为不属于评分主链；不确定性与证据边界总体清楚。仍有部分high/medium confidence引用和基因组/性状数值未核，故取8而非9-10。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露较充分：uncertainties 逐条列 EC 1.14.13.82 归属不确定、HR199/AN103 无基因组/保藏号、SYK-6 NBRC 与基因组&#x27;二手记忆/GC未核&#x27;、氧条件 null 但主链实际好氧；各 trait/enzyme 带 confidence 分档，属级推断明确标注；S2/S3/S4 的 step.uncertainty 有具体说明。个别 high 置信度用于未经 E0 核实的酶/身份，但均可对应文献题录并已列边界。档位7：大部分观测/预测/未知正确标注，主要限制与冲突已说明。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Supports that uncertainty and evidence-type labels were explicitly delivered; does not verify the underlying facts.

</details>

## Qwen

答案SHA256：`5bae399f66dec29c14a832ab632a34dbb2c2b98405e9df0d0ba0a932f12de58e`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案结构上覆盖路径、酶、菌和15项性状字段，但15项性状全部为null/unknown，且题面主链所需的S03离散中间步未按逐步主链交付（答案S2将S03→S02合并为净转化）。按本案D1任务范围&#91;1,4&#93;取4：模块大体可见，但必要内容有明显缺口；未达到D1关键错误所要求的大部模块缺失或严重路线名偏离，故不另cap。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（主要模块均有涉及但若干必要内容遗漏/仅占位），取5。路径、酶、微生物三模块逐步给出且路线名原样回填；但题目要求的15项性状全部以null占位（无任何数值、单位、条件），4个中间体SMILES为null，微生物仅有物种名无strain/TaxID，来源模块仅有内部知识自述。属完成度不足，不构成核心模块大部缺失的D1关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_080：支持本题路线名为ferulate degradation、gold终端为Vanillin|acetyl-CoA；不支持答案把终端扩至acetyl-CoA/succinyl-CoA后自动获得任务完成度。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：支持gold三必答步及S03中间体的独立存在；不支持把S03合并进S2后仍视为逐步完整交付。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 主链化学大体连贯：ferulate→feruloyl-CoA、香草醛→香草酸→原儿茶酸、3,4-开环后进入β-酮己二酸节点均属合理方向；但答案把gold S03的feruloyl-CoA水合中间体与S02的裂解合并为S2，未把3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA作为独立主链步表达，关键中间体与逐步连续性不足。按D2范围&#91;1,6&#93;取6（5–6档上沿）：主干成立但关键连接仍需修订，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8（主链及关键转化有充分依据，少量局部问题），取7。首步ferulate→feruloyl-CoA与净第二步feruloyl-CoA→vanillin+acetyl-CoA与gold反应条目一致，方向正确、无一步跳到中心代谢物；S3–S9为教科书β-酮己二酸途径延续，方向与碳骨架守恒自洽。主要扣分点：9步普遍缺ATP/CoA、O2、NAD+、H2O等辅因子（P103局部计量缺陷，档内处理不cap）；多个中间体SMILES为null；答案在gold终点后继续延伸，按四.2/P29既不加分也不作覆盖率扣分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：支持S01 ferulate→feruloyl-CoA、S03 feruloyl-CoA+H2O→3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA、S02→vanillin+acetyl-CoA的方向与顺序；不支持将S03中间体省略后仍视为逐步连续。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_080：支持S01/S02/S03的酶名与EC族关系；不支持把答案S2的净反应当作与gold逐步酶反应完全等价。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按release合同固定D3a计数：S=0、F=1（KEY）、U=2、H=0、N=3；confirmed_target_rate=0.0。S03为已确认KEY失败并触发D-KEY4上界4；S01/S02仍为ALIGNMENT_NOT_CONFIRMED，不能当S计。已确认KEY失败使目标主功能严重受损，可用部分与失效边界只能勉强分清，取3而非4；不因其他自动未决抹去KEY失败。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（有合理候选和部分支持，但若干关键步骤仍缺具体核验），取6。S1酶名ferulate-CoA ligase/4-coumarate-CoA ligase与EC 6.2.1.12和gold酶条目BSY-e01452一致；S2酶名feruloyl-CoA hydratase/lyase与gold一致（EC留null，缺失不判错）。其余EC 1.2.1.3、1.14.13.82、1.13.11.3、5.5.1.2、3.1.1.24、2.8.3.6、2.3.1.174与反应类型类别相符但E0无冻结条目可核，保持UNRESOLVED；未发现EC大类与反应类型错配、酶名与EC互相矛盾等已核实关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：支持S03为feruloyl-CoA→3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA的必经中间步；不支持answer S7的3-oxoadipate enol-lactone水解作为S03目标反应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_080：支持S01可接受EC 6.2.1.12/6.2.1.34、S02/S03为feruloyl-CoA hydratase/lyase族；不支持把answer S7的EC 3.1.1.24视为S03匹配。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案全路径统一使用Pseudomonas fluorescens，无strain、TaxID或反应级能力证据；P. fluorescens作为ferulate降解相关菌有合理性（gold另有P. fluorescens AN103路径完成行），但答案未绑定该菌株，也未给步级归属或整路径能力证据。按5–6档取6：有合理候选和部分背景支持，但关键身份/作用范围仍未充分核验；无已核实身份错误，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6，取6。答案9步统一归给Pseudomonas fluorescens（物种级，strain/TaxID/保藏号全null）。该物种在gold PATHWAY_COMPLETE名单中以Pseudomonas fluorescens AN103出现（pathway_complete=TRUE），故物种级存在性与整路径降解记录有依据，非编造；但gold STEP级微生物为Sphingomonas sp. SYK6，答案未给菌株级身份、未逐级区分身份/反应级/整路径能力，属D3b身份阶梯①粒度不足（档内扣，默认不cap），且无已核实的身份错配或无关类群引用。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_080：支持gold步级菌为Sphingomonas sp. SYK6，并另列Pseudomonas fluorescens AN103为PATHWAY_COMPLETE；不支持answer未绑定AN103却把P. fluorescens物种级统一写成全路径菌。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_080：显示P. fluorescens AN103多数字段UNKNOWN、F14仅有TaxID式记录；不支持answer的整路径能力或步级反应能力已获对应粒度证据。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> organism_profiles&#91;0&#93;.traits.F1–F15全部为null/unknown，未交付任何可评价性状值；按P44全性状null记MISSING=1，不在D4宣称检测到科学错误。完成度问题已在D1反映，不重复重扣。

<details><summary>V0.4理由与本行变化背景</summary>

题目要求每个profile一次返回全部15项性状；答案organism_profiles&#91;0&#93;.traits的F2_temperature、F1_oxygen_tolerance、F4_salinity、F3_pH、F5_culture_collection、F6_respiration_electron_acceptor、F7–F13各字符串项、F14_genome_basic、F15_habitat_generalism全部为value:null、confidence:unknown。按P44「全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到科学错误」处理，故给1分并保留权重参与总分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_080：显示本题多种trait为completeness_only或UNKNOWN；不支持把null当作已核错误，但也无可评观测值。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_080：支持P. fluorescens AN103及Sphingomonas sp. SYK6多种性状为UNKNOWN；不支持answer已交付可评价性状。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> D5只评实际交付来源。答案仅EVID_001 source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null，且同一条内部知识覆盖pathway/steps/enzymes/microorganism；决策相关组均为MISSING_SOURCE，无法定位关键结论依据。MISSING_SOURCE默认不cap，故key_error=N；按1–2档取1。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG09）全部只有EVID_001一条INTERNAL_KNOWLEDGE_ONLY自述（database/record_id/locator皆null，claim_scope只泛列pathway/steps/enzymes/microorganism），无任何条目级可定位可核对来源→按P34/P41落缺失低分档1–2；取2（保留其显式claim_scope与逐条low置信标注的有限价值）。属缺失而非误导，默认不触发cap；E0为EVIDENCE_GAP，无可核实错引，故无VERIFIED_MIS_CITATION，severity不适用。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry.EVID_001：证明答案实际只交付一条内部知识来源且无外部定位信息；不支持任何路径、酶、菌或性状结论可被外部追溯。
- RUBRIC_CLAUSE / R2-30：用于按来源六状态评价实际交付来源；不将EVIDENCE_GAP本身当作错引或低分证据。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确标注EVID_001为INTERNAL_KNOWLEDGE_ONLY、各步confidence低或unknown，并列出氧条件未指定、未绑定菌株、SMILES缺失、部分EC基于通用酶类推断等待验证点；大部分未知/推断被正确标注，主要限制已说明。仍有complete_pathway_organism_profile_id=ORG_001及全步骤同一菌的较强归属未逐项限定，故取7–8档上沿8而非9–10；不构成系统性误导，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8（大部分观测/预测/未知被正确标注，主要限制与冲突已说明），取7。route_summary明示「缺乏直接外部证据…按低置信度记录」；steps&#91;*&#93;.enzyme/microorganism.confidence全为low，各步uncertainty写明辅因子/计量/SMILES缺失；uncertainties列出氧条件未定、未绑定保藏菌株、SMILES缺失、EC基于通用酶类推断四条具体限制；未把推断包装成数据库直查观测，未编造引用。扣分点：置信标注全局化，未逐条区分「可核事实/路径推断/未知」，也未说明超出gold终点的延展段属何种证据性质。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持答案已披露氧条件、菌株身份、SMILES和EC推断等限制；不支持完整路径能力已被证实。
- ANSWER_TEXT / ANSWER.evidence_registry.EVID_001：支持答案将证据来源标为内部知识并低置信度；该标签本身不等于观测证据。

</details>

## Grok

答案SHA256：`ebf67eb056516a2fa832dfbf4d6628e3ef999f46b49d051bb45c59401e5bfbea`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求的ferulate degradation主链核心三步均在答案中实质给出（S1 ferulate→feruloyl-CoA，S2 feruloyl-CoA→3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA，S3→vanillin+acetyl-CoA），并额外给出下游S4–S6；两个organism_profile均返回全部15项性状字段。扣分点主要是feruloyl-CoA、3-hydroxy酰基CoA、acetyl-CoA和3-carboxy-cis,cis-muconate等主产物SMILES为null，且部分性状为显式unknown，属于局部完整性/表达缺陷而非主模块缺失。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv：Supports the pollutant/route name and gold terminal Vanillin|acetyl-CoA; does not by itself validate the answer&#x27;s extra downstream steps.
- GOLD_SLICE / formal_cases.tsv：Supports the existence of a linear 3-step gold main chain; not a mandate to score every branch or downstream continuation.
- GOLD_SLICE / reaction_gold.tsv：Supports directed gold core reactions S01, S03 and S02; does not validate extra S4–S6.
- ANSWER_TEXT / ANSWER：Supports what was actually delivered, including missing null SMILES and trait unknowns.

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 核心化学链与gold S01/S03/S02一致：CoA连接、水合、逆醛醇裂解、香草醛氧化、单加氧酶脱甲基和原儿茶酸3,4-开环均有方向、主产物与辅因子记录，S1还把ATP/CoA及AMP/PPi列入。主要扣分是若干主产物SMILES缺失，且S4–S6属于题面终点后的下游外延，不能为D2目标额外加分；但未见核心方向反转、原子明显不守恒或无依据跳步。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Supports the directed core transformations and cofactor roles for S01, S03 and S02; does not cover S4–S6.
- GOLD_SLICE / case_root_identity.tsv：Supports ferulate as root and Vanillin|acetyl-CoA as terminal main products.
- ANSWER_TEXT / ANSWER：Supports the delivered reaction sequence and identifies missing SMILES and downstream extension.

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按原答案实配：S1 ferulate→feruloyl-CoA用feruloyl-CoA synthetase EC 6.2.1.34，命中accepted集合的6.2.1.12|6.2.1.34；S2（对应gold S03）用trans-feruloyl-CoA hydratase EC 4.2.1.101，功能名与gold feruloyl-CoA hydratase/lyase的水合半反应相符，但该显式EC在E0无独立核验；S3（对应gold S02）用enoyl-CoA hydratase/aldolase且EC null，裂解功能与gold lyase相符并诚实留空EC。三步目标催化对应整体可靠，主要剩余问题是S2显式EC未核，属局部待核，不推翻目标功能。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：Supports feruloyl-CoA synthetase EC 6.2.1.12/.34 for S01 and feruloyl-CoA hydratase/lyase name for S02/S03; does not supply an EC for S02/S03.
- GOLD_SLICE / reaction_gold.tsv：Supports the reaction direction and substrate-product pairs used to map answer S1/S2/S3 to gold S01/S03/S02.
- ANSWER_TEXT / ANSWER：Supports the delivered enzyme names/EC, including null EC for S3 and explicit EC 4.2.1.101 for S2.

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 必答S1–S3所用的Pseudomonas sp. HR199在gold organism_gold中以PATHWAY_COMPLETE出现（TaxID 86003），答案虽未填TaxID，但物种+菌株名与已知完整路径菌名称一致，未把单步菌误写成全路径菌；complete_pathway_organism_profile_id仍为null。S5–S6另用P. putida KT2440并给TaxID 160488、genome AE015451，这部分不在本题gold/e0冻结记录中，属局部待核。总体微生物身份与步级归属有合理支持，但KT2440身份/能力证据不足，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：Supports HR199 as a pathway-complete organism name in the gold slice; does not supply a strain-level capability proof for every step or validate KT2440.
- GOLD_SLICE / trait_gold.tsv：Shows organism/trait coverage and that HR199/KT2440 trait cells are mostly UNKNOWN; not evidence of step-level catalysis.
- ANSWER_TEXT / ANSWER：Supports the delivered organism assignments and the null complete_pathway_organism_profile_id.

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 两个profile均返回15项性状字段，未知项用null/unknown如实保留，KT2440还给出genome accession AE015451；但HR199与KT2440的多数非空性状来自INTERNAL_KNOWLEDGE_ONLY，gold trait slice对这两株的观测值基本为UNKNOWN/completeness_only，无法核验其数值、条件与适用范围。未见明显离谱数值或把物种级观测硬套到菌株的已核冲突，故按“部分性状可合理，关键证据不足”取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Shows which trait records exist; for HR199/KT2440 most trait cells are UNKNOWN and cannot confirm the answer&#x27;s non-null values.
- GOLD_SLICE / trait_scoreability_mask.tsv：Marks these trait fields as completeness_only rather than observed-accuracy denominators; does not validate the answer values.
- ANSWER_TEXT / ANSWER：Supports the delivered trait values, confidence labels and explicit nulls.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry五条全部为INTERNAL_KNOWLEDGE_ONLY；locator写“recalled ... not live-queried”“KEGG/MetaCyc-style routes”及文献作者名，但没有DOI、数据库条目、reaction/EC/TaxID记录或可定位原文。按D5六状态，决策相关组均为MISSING_SOURCE，属几乎无法定位重要结论依据；无经核实错引，故不触发cap，但低档取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the delivered source records are all internal-only with non-locatable locators; does not provide external supporting records.

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案设有uncertainties数组，明确区分题面未指定氧条件、Ech拆分、EC重编号未核对、SMILES缺失及未核TaxID/基因组等；大量未知字段用null/unknown，未把预测写成实验观测。但多个仅凭内部记忆的酶、EC、菌株和性状仍标为medium confidence，且KT2440“专性好氧”等表述未标注待核，存在单点偏强/披露不够精确，故取5–6档上沿6而非更高。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the delivered uncertainty/confidence statements; does not verify the underlying facts.

</details>

## GPT5.6

答案SHA256：`ebcb7d4f4c46455d3e9be07aff774e691eee5e3d4040e177b780f1d38eb881e6`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 路径、酶、菌及15项性状字段均有涉及，但未交付gold主链必需的3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA中间步；S2只列vanillin，未把acetyl-CoA列为主产物；15项性状全为null。主要模块均有涉及但必要内容遗漏，落5–6档，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_080：LINEAR_UNIQUE，ordered_step_count=3；本题必答主链为3步，不是全DAG旁支。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：支持S01 ferulate→feruloyl-CoA、S03 feruloyl-CoA→3-hydroxy中间体、S02 3-hydroxy中间体→vanillin+acetyl-CoA；用于定位答案遗漏的中间步与terminal main product。
- ANSWER_TEXT / ANSWER：答案S2直接feruloyl-CoA→vanillin；15项性状value/raw_text/evidence_id均为null。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1活化为feruloyl-CoA方向正确；S2将feruloyl-CoA直接裂解为vanillin，跳过3-hydroxy中间体且未把acetyl-CoA列入主产物（仅在uncertainty提及），关键中间体/连接需修订。后续vanillin→vanillate及protocatechuate为额外下游，不改变主链终点判断。主干部分成立，落5–6档取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：定义S01、S03、S02的底物/产物与方向；支持S2跳过3-hydroxy中间体及未列acetyl-CoA的判断。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_080：gold terminal main products为Vanillin|acetyl-CoA；支持本题终点主产物判断。
- ANSWER_TEXT / ANSWER：答案S2只列vanillin为主产物，uncertainty称伴随acetyl-CoA但未列入products。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 逐目标：S01 ferulate→feruloyl-CoA，酶feruloyl-CoA synthetase/EC 6.2.1.34与accepted集合相符，可记S；S02/S03需经3-hydroxy中间体，答案S2直接feruloyl-CoA→vanillin，未交付S03底物/产物，也未列S02的acetyl-CoA。可判S/N=1/3，落&#91;3,4&#93;；可用与失效边界清楚但仅少数目标可用，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_080：S01 accepted feruloyl-CoA synthetase含EC 6.2.1.12/6.2.1.34；S02/S03 accepted feruloyl-CoA hydratase/lyase；仅支持策展G4酶名/EC对应，不证明具体蛋白活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_080：定义S03 feruloyl-CoA→3-hydroxy中间体及S02 3-hydroxy中间体→vanillin+acetyl-CoA；支持答案目标反应未完成。
- ANSWER_TEXT / ANSWER：答案S1匹配S01；S2用feruloyl-CoA→vanillin，未给3-hydroxy中间体，也未在主产物列acetyl-CoA。

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案全程使用Pseudomonas sp. HR199，并声明complete_pathway_organism_profile_id=ORG_001；gold的PATHWAY_COMPLETE行确列Pseudomonas sp. HR199（TaxID 86003，pathway_complete=TRUE），支持整条ferulate路径能力。未给TaxID/保藏号且缺逐步骤独立菌证，但身份与整路能力有可靠支持，落7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_080：PATHWAY_COMPLETE行含Pseudomonas sp. HR199 TaxID 86003且pathway_complete=TRUE；STEP行另列Sphingomonas sp. SYK6，但非排他；支持HR199身份与整路能力，不证明每步独立实验。
- ANSWER_TEXT / ANSWER：所有step均用同一Pseudomonas sp. HR199；未给TaxID/保藏号。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段均存在但value/raw_text/evidence_id为null，confidence=unknown；未提供任何可评价性状值。按全部必需性状为null/空值按D4 MISSING=1处理，不判科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：15项性状均以null/unknown返回，未交付可评价性状值。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_080：HR199在gold中多数性状为UNKNOWN；仅用于说明不得用代表记录回填答案缺失来源。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry两条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为空，所有路径/酶/菌声称只映射到内部自建EVID_001/002，无可定位外部条目。按MISSING_SOURCE低档；非已核实错引，不cap。因至少给出内部登记与claim_scope，落1–2档取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：两条evidence均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为null；无外部可定位来源。
- RUBRIC_CLAUSE / P34：MISSING_SOURCE按低分档，默认不触发关键错误cap。
- RUBRIC_CLAUSE / P41：D5按claim group登记；支持组证据不能跨档上调核心组缺失。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案把证据登记为INTERNAL_KNOWLEDGE_ONLY、confidence medium，明确列出氧条件未指定、EC/基因命名可变、TaxID/保藏/基因组未填，15项性状null/unknown；大部分未知和限制已披露。主路线仍以肯定语气给出，且未明说跳过3-hydroxy中间体，故落7–8档取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：uncertainties披露氧条件、EC/基因、TaxID等未知；evidence_registry标注INTERNAL_KNOWLEDGE_ONLY；性状为unknown。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；本案未达系统性误导cap。

</details>
