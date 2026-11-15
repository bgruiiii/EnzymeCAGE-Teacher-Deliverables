# BIOPATH150_128：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：L-threitol degradation

污染物：l-Threitol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 46.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 33 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 46.5 | COMPARABLE | RECOVERED_BATCH_B |
| Qwen | 42 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 28.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 30 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`dc1de6535547a4fab8eecc92eeea81b2f44f9719671fc9b595cca1e7ca41eb86`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 任务模块基本齐全：给出3步主链、每步酶与菌、两个profile各15项性状及证据登记；但题面锁定L-threitol degradation，gold主链为4步至D-erythrose 4-phosphate，答案采用脱氢→磷酸化→裂解支路并止于DHAP+甲醛，缺S04终点，属严重路线/任务符合度偏离，D1落在&#91;1,4&#93;；档内取4因其余交付与格式完整。

<details><summary>V0.4理由与本行变化背景</summary>

三步均给出主底物/主产物英文名与SMILES、一个首选酶与一个对应微生物；两个profile按物种+菌株去重（S2/S3同为S. meliloti 1021共用ORG_002），各自填满15项性状；chosen_route_name原样为&#x27;L-threitol degradation&#x27;，符合题面无改选路线要求。缺口：三步EC全为null（题面明确要求EC，按填写指示未知可null，但属系统性缺项），两profile的F3_pH、F4_salinity、F5_culture_collection为null，ORG_001的F14仅有GC值。落7档（大部分必要内容完整、关联清楚、少量遗漏），不因篇幅加分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：gold主链为S02→S01→S03→S04，S04终产物为D-erythrose 4-phosphate；不支持答案的3步裂解终点作为同一锁定主链。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_128：formal case登记ordered_step_count=4、LINEAR_UNIQUE；不支持将3步替代支路视为完整必答主链。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 前三步内部化学连续、方向为降解、S1与S2的辅因子/计量基本配平；但S3换成逆醛醇裂解为DHAP+甲醛，未走gold S03/S04异构酶段，也未达指定终点，关键转化/连接需实质修订。按5–6档取6；D2_chemical_range为&#91;1,6&#93;。

<details><summary>V0.4理由与本行变化背景</summary>

S1（L-threitol+NAD+→L-erythrulose+NADH+H+，仲醇脱氢）与S2（L-erythrulose+ATP→L-erythrulose 1-phosphate+ADP，激酶）的主底物、主产物、辅因子、方向与立体化学同gold BSY-r02438/BSY-r02167一致，原子与电荷自洽。S3改为逆醛醇裂解生成DHAP+甲醛，与gold S03/S04（L-erythrulose 1-phosphate→D-erythrulose 4-phosphate→D-erythrose 4-phosphate，异构化）不同；该裂解在计量上自洽、答案已明确声明为赤藓糖醇途径类比且未获专门文献确认，属&#x27;未证实替代&#x27;（四.5第3步），且题面只给路线名未给终点，gold下游不进入覆盖率扣分（四.2/P29）。落5–6档取6：主干成立、关键末端转化仍需修订、合理性证据有限。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：gold S02/S01支持前两步脱氢与磷酸化；gold S03/S04为异构化至D-erythrose 4-phosphate，不支持S3裂解为DHAP+甲醛作为同一主链。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 目标步S=0、F=1、U=3；S02虽有结构/方向MATCH但酶名不在accepted集且无EC，仍为U；S01为表示边界UNKNOWN；S03为已确认KEY失败（gold异构酶被替换为裂解酶）；S04未交付/对齐未确认。存在预定义KEY已核失败，D-KEY4上限4；因无已支持目标、仅少量局部可用信息，取2。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名&#x27;L-threitol dehydrogenase&#x27;与gold酶名&#x27;erythritol/L-threitol dehydrogenase&#x27;同族同名（gold多注EC 1.1.1.56/1.1.1.9/1.1.1.12/1.1.1.M28/M29，答案留null）；S2&#x27;erythrulose kinase&#x27;与gold&#x27;L-erythrulose kinase&#x27;/EC 2.7.1.209对应；S3&#x27;erythrulose-1-phosphate formaldehyde-lyase&#x27;与其自选的裂解反应自洽，但与gold的L-erythrulose 1-phosphate isomerase（EC 5.3.1.33）功能不同且无核验。三步EC全null（诚实留空），不存在酶名-EC互相矛盾、也不存在把家族相关性冒充具体催化证据，故不触发本维关键错误。落5–6档取6：有合理候选与部分支持，关键步骤仍缺具体核验。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：gold S03为L-erythrulose 1-phosphate→D-erythrulose 4-phosphate，S04为D-erythrulose 4-phosphate→D-erythrose 4-phosphate；不支持答案S3的DHAP+甲醛产物作为该步目标反应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：gold S03 accepted酶为L-erythrulose 1-phosphate isomerase/EC 5.3.1.33；不支持答案的formaldehyde-lyase名称作为该步已接受酶。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Brucella abortus 2308与Sinorhizobium meliloti 1021身份格式完整并给TaxID，但答案把Brucella用于S1、Sinorhizobium用于S2/S3；gold步级菌为Mycolicibacterium smegmatis/Pectobacterium等，E0无本案菌株反应级能力记录，且answer complete_pathway=null。属合理候选、身份/能力未充分核验，5–6档取5；无已核身份错配cap。

<details><summary>V0.4理由与本行变化背景</summary>

菌为Brucella abortus 2308（TaxID 359391）与Sinorhizobium meliloti 1021（TaxID 266835）。两TaxID在E0无冻结记录（GAP-128-021/022/024/025）→UNRESOLVED，不判虚构；B. abortus见于gold菌集（S03/S04步，taxid 235），S. meliloti不在gold菌集。答案以low confidence声明两菌对L-苏糖醇的实际利用未确认，complete_pathway_organism_profile_id=null，未把单步菌写成全路径菌，避免了八.D3b的关键错误。落5–6档取6：有合理候选与部分支持，身份与步级反应能力均未充分核验；身份与能力分别列为待核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_128：gold S02 organism为Mycolicibacterium smegmatis；S03/S04列Brucella abortus等，但非穷尽；不支持答案把Brucella/Sinorhizobium分配到这些步骤的结论。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 两profile各15项齐全，未知项有null/unknown；但多数性状仅有INTERNAL_KNOWLEDGE_ONLY，无冻结核验；Brucella在trait_gold多为UNKNOWN，S. meliloti无trait_gold记录；F14中NC_003047通常只对应染色体而genome_size_bp写总基因组规模，存在子字段不一致。部分合理但关键项证据不足，5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

两profile的15项性状结构齐全，未知项（F3_pH、F4_salinity、F5_culture_collection等）诚实置null，未编造。已给值（B. abortus 37°C最适、好氧、氧化酶/过氧化氢酶/脲酶阳性、无动力、革兰氏阴性、无芽孢、GC 57.2%；S. meliloti 28–30°C、好氧兼微氧呼吸、有动力、共生固氮、革兰氏阴性、无芽孢）为常见教科书描述，方向无明显错误，未见把预测写成观测或把物种观测推广为全部菌株的表述。但E0对Brucella abortus(235)的性状全为UNKNOWN、对S. meliloti无任何性状记录（GAP-128-027…046），无法逐项核实；ORG_002的F14把染色体登录号NC_003047与6,691,694 bp（全基因组量级）并列，存在粒度不一致；培养温度/观察值未与被推广为耐受极限。落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_128：gold Brucella abortus 235多为UNKNOWN，仅genome GCA_000740135.1；S. meliloti无本案trait行；不支持答案多数Brucella/Sinorhizobium性状为已核观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_128：Brucella仅F14 scoreable，其余completeness_only；S. meliloti不在本案mask中；支持“关键项证据不足”而非逐项判错。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry四条全部source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；决定相关组CG01/CG02/CG03/CG05/CG07均无可定位外部来源，按MISSING_SOURCE低档；无已核实错引，不cap。档内取2因有内部claim-scope映射但无法外部核验。

<details><summary>V0.4理由与本行变化背景</summary>

answer的4条证据（EVID_001–EVID_004）全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，只能看到自述claim_scope，无法定位到任何文献、数据库条目或计算记录；按四.3六状态，本题全部claim组仅有自我声明→MISSING_SOURCE（低分档，默认不触发关键错误cap）。E0对该案的唯一记录（TaxID 294 Pseudomonas fluorescens）与答案任何声称无关，答案所引TaxID 359391/266835为EVIDENCE_GAP，均保持UNRESOLVED。无经核实错引，故severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，本维不cap；评分取2档（几乎无法定位重要结论依据）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / P34：MISSING_SOURCE包含完全无引用或仅INTERNAL_KNOWLEDGE_ONLY；D5按低分档评定，默认不cap。
- RUBRIC_CLAUSE / P41：D5按claim group登记状态集合；决策相关组均为MISSING_SOURCE时按低档，不因支持组内部映射上调。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> route_summary与uncertainties明确说明无专门L-threitol文献、整体低置信、EC/基因未知、菌株能力未确认、complete_pathway=null；较好区分推断与未知，并披露替代支路。扣分点：部分性状仍以medium/high标注但仅有内部知识。7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案系统披露不确定性：route_summary直接说明无L-苏糖醇专门文献、路线由赤藓糖醇途径类比、整体置信度低；每步uncertainty说明EC/基因未知与推断依据；uncertainties五条覆盖立体化学推断、两菌实际利用未确认、pH/盐度/保藏号等填null、TaxID与个别数值为记忆性填写建议复核；alternative_branches明确标记&#x27;不属于本题评分主链&#x27;；证据性质以INTERNAL_KNOWLEDGE_ONLY登记，未把预测冒充观测。局部问题：F10/F12/F13等记忆性性状仍标high，与&#x27;记忆值&#x27;总体声明略不一致，属单点过度确信，档内扣分。落7–8档取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- RUBRIC_CLAUSE / P45：诚实填写未知/null可在D6得较高分；编造填满不应获得整体优势。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；本例有具体不确定性披露，未见系统性把预测写成实证。

</details>

## DeepSeek

答案SHA256：`7e4194df435afd504ea9c69791d0541e6df0ea76cedeb043333cc97fbaa78c19`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> D1 3–4：四步、每步酶/菌及15项性状字段均出现，但实际主链不是题面冻结的L-threitol主链，且15项性状全部null/unknown；任务符合度和完整性均只能落在低档。

<details><summary>V0.4理由与本行变化背景</summary>

路径4步完整（每步substrates/products含name+smiles、enzyme含ec_number、microorganism齐备）、步骤连接清楚且chosen_route_name原样填&#x27;L-threitol degradation&#x27;；但15项性状全部为null占位、evidence_registry为空（题面要求的&#x27;各项最强来源&#x27;未交付），构成两处必要内容缺失。主要模块均有涉及但性状仅占位、来源遗漏，落5–6档低段取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：冻结gold主链S02→S01→S03→S04及终点D-erythrose 4-phosphate；不支持替代分支本身错误。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：列出各目标步冻结酶/EC与步骤关系；不支持答案酶替代。
- ANSWER_TEXT / ANSWER_BIOPATH150_128：答案实际给出S1–S4步骤、null性状和空证据表；作为原文定位。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D2 5：替代路线的碳骨架和计量大体自洽（L-threitol→L-threose→L-threonate→2-dehydro-3-deoxy-L-threonate→pyruvate+formaldehyde），但首步产物/方向与冻结L-threitol主链冲突，脱氢步骤缺NAD+/NADH，合理性依据有限；按允许区间&#91;1,5&#93;取上沿但仍需实质修订。

<details><summary>V0.4理由与本行变化背景</summary>

答案主链L-threitol→L-threose→L-threonate→2-dehydro-3-deoxy-L-threonate→pyruvate+formaldehyde四步化学自洽：S1/S2为伯醇→醛→酸的连续氧化、S3为脱水（净失H2O、碳架保持）、S4为2-酮-3-脱氧裂解成pyruvate(3C)+formaldehyde(1C)，原子计数守恒、方向合理、无跳步。但与gold经erythrulose磷酸化至D-erythrose-4-P的路线完全不同，答案未声明为替代路线且evidence_registry为空（无依据）；题面仅给路线名无唯一定位。按四.5：与gold不同不自动判错，作未证实登记，&#x27;主干部分成立但合理性证据有限&#x27;取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：gold主链转化与方向；不禁止化学上自洽的替代分支，但不回填目标完成。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：gold酶反应对应；不支持答案替代酶。
- ANSWER_TEXT / ANSWER_BIOPATH150_128：答案实际化学步骤与缺失辅因子定位。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> D3a落在程序允许的&#91;1,4&#93;：S01/S02为已确认KEY目标失败，S03/S04无绑定；confirmed_target_rate=0.0，没有任何必答目标反应获得已确认S信用，核心目标催化对应几乎不可用。S03/S04只作为局部待核保留，不改变已确认KEY失败决定的低档。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶名与反应类型一致（脱氢酶对氧化、脱水酶对脱水、醛缩酶对裂解），EC大类（1.1.1.x/4.2.1.x/4.1.2.x）与酶类型相符，属合理候选；但四个具体EC（1.1.1.123/1.1.1.124/4.2.1.42/4.1.2.20）在E0均为EVIDENCE_GAP无冻结记录，accepted name/reaction无法核对，未取得具体催化核验，答案自评confidence=low。&#x27;有合理候选和部分支持但关键步骤缺具体核验&#x27;取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：gold各步accepted酶/EC；不支持答案的替代酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：gold各步底物/产物与方向；用于核对S01/S02非匹配。
- ANSWER_TEXT / ANSWER_BIOPATH150_128：答案实际酶、EC及步骤定位。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> D3b 3–4：TaxID 294身份可由E0核对为Pseudomonas fluorescens，但答案未给菌株，且把同一物种分派给四个不同反应；没有任何步级反应能力证据，也不在gold步级菌列表中，微生物对应主结论不能确认。未达到已核实关键错误，故key_error=UNRESOLVED、不cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案四步均用Pseudomonas fluorescens(TaxID 294)：其种级身份经E0(f3e0:tp:EV146-01)核实为P. fluorescens、name-taxid一致(SUPPORTED)，属&#x27;部分支持&#x27;；但该菌对S1–S4的反应级催化能力(CG08)与&#x27;降解L-threitol&#x27;的作用范围完全无交付证据、E0标注为UNRESOLVED，且strain=null仅种级。非编造、非跨类群错配、未推翻主要推荐。按&#x27;合理候选和部分支持但作用范围未充分核验&#x27;取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-01：支持TaxID 294对应Pseudomonas fluorescens的物种身份；不支持任何步级反应能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_128：gold各步/整路径微生物记录；用于比较，不把P. fluorescens自动判为虚构。
- ANSWER_TEXT / ANSWER_BIOPATH150_128：答案将P. fluorescens分派给S1–S4的原文定位。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> D4按MISSING=1：organism_profiles&#91;0&#93;.traits的15项均value=null/confidence=unknown，未交付任何可评价性状值；这不是检测到错误，按P44处理。

<details><summary>V0.4理由与本行变化背景</summary>

org profile的F1–F15全部为value:null、confidence:unknown，未交付任何可评价性状值；按P44&#x27;全部必需性状均为null/空值时同样处理——D4按MISSING记1分，不宣称检测到科学错误&#x27;。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_128：gold可用性状参照；不用于回填答案缺失值。
- ANSWER_TEXT / ANSWER_BIOPATH150_128：答案15项性状全为null/unknown的定位。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> D5 1–2：evidence_registry为空，所有evidence_id=null，仅在uncertainties声明一般文献知识；决策相关组均MISSING_SOURCE，无已核实错引，故低档但不cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry为空，四步酶/菌、路线、性状均无任何evidence_id或来源记录，仅&#x27;基于一般文献知识&#x27;的自我声明→decision-relevant各组均为MISSING_SOURCE。按四.3/P34：MISSING_SOURCE低分档、默认不cap；几乎无法定位任何重要结论依据，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_128：答案实际无来源交付；uncertainties承认无直接证据。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> D6 7–8：答案将酶/EC与菌信息标为low/unknown，明确说基于一般文献且无直接证据，性状全null，SMILES推断与立体化学限制写入uncertainties；未见系统性把预测写成观测。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露较具体诚实：各步enzyme/microorganism confidence=low，step.uncertainty与uncertainties注明&#x27;EC/菌株基于一般文献知识、未提供直接证据&#x27;及&#x27;SMILES立体化学可能不准&#x27;，15性状诚实填unknown未编造；未见把预测写成观测或掩盖矛盾。唯未显式标注整条路线为替代/推测、未讨论与已知路线的差异；按&#x27;大部分观测/预测/未知被正确标注、主要限制已说明&#x27;取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_128：答案的不确定性、低置信和未知标签定位。

</details>

## Kimi

答案SHA256：`3161161d942e5d8a6bcfd308b942c7a1584665a5e07d7bf420135cbc2f4b7e5e`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 交付结构齐全：三步主链各给底物/产物/SMILES/首选酶+EC/对应微生物，另交15项性状、证据登记与不确定性说明，机器可读。但题面以route_scope锁定L-threitol degradation，冻结任务范围为4步主链S02→S01→S03→S04并终止于D-erythrose 4-phosphate；答案自称按该路线整理，实际交付脱氢酶→激酶→醛缩酶三步并止于DHAP+formaldehyde，替代S03位点、完全缺S04终点步。按P100属『自称合规却交付不同化学路线』的任务参数偏离，为D1关键错误，封顶4；因模块覆盖与酶-菌-性状关联清晰、工程无缺陷，取封顶上限4。

<details><summary>V0.4理由与本行变化背景</summary>

输出结构完整：3步主链各含底物/产物(name+SMILES)、酶(名称+EC)、对应菌；route_scope.chosen_route_name原样填&#x27;L-threitol degradation&#x27;；organism_profiles一条含全部15项性状；evidence_registry与uncertainties齐备。仅gene_or_protein与若干量化性状为null（题面允许）。第3步化学与gold分歧按D2处理、不在本维重复扣；命题定位不足（题面仅给路线名）入review_queue。7-8档取8：大部分必要内容完整、关联清楚。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：支持：冻结四步定向主链（S02 l-Threitol→L-Erythrulose；S01 L-Erythrulose+ATP→L-erythrulose 1-phosphate；S03→D-erythrulose 4-phosphate；S04→D-erythrose 4-phosphate）及终点身份。不支持：其他路线在化学上不可能，或对所答酶作具体催化活性裁定。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：支持：本题四步对应的冻结酶/EC记录与步序对应。不支持：对未列EC（1.1.1.122/2.7.1.53/4.1.2.2）作真伪判断。
- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;：支持：答案实际只交付三步、第三步为逆醛醇裂解、未交付S04；不支持：把该替代链回填为目标主链完成。
- QUESTION_TEXT / QUESTION.route_scope/要求1-5：支持：路线名须原样填写且主链按指定路线；不支持：以路线名相同即视为化学路线一致。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 按所答化学自身质量评：S1（L-threitol+NAD+→L-erythrulose+NADH+H+）与S2（L-erythrulose+ATP→L-erythrulose 1-phosphate+ADP）为成对辅因子参与、方向正确的氧化/磷酸化；S3为L-erythrulose 1-phosphate的逆醛醇裂解生成DHAP+formaldehyde，按答案自身SMILES可核对C4H9O7P→C3H7O6P+CH2O计量闭合；三步首尾相接（S1产物=S2底物，S2产物=S3底物），无反向、无中心代谢物跳跃。缺陷：所给L-threitol与L-erythrulose的SMILES在指定手性中心与冻结L-构型相反（程序逐步诊断标记STEREO_CONFLICT_SPECIFIED），且中段以裂解替代异构酶转化。按C06显式立体冲突候选≤5、本案D2允许区间&#91;1,5&#93;，落入『主干部分成立但关键中间体需实质修订』档，取5（该档低端，问题非轻微）。

<details><summary>V0.4理由与本行变化背景</summary>

第1步L-threitol经NAD+脱氢生成L-erythrulose(伴NADH+H+)、第2步ATP依赖性磷酸化为L-erythrulose 1-phosphate，其方向、结构与连接与gold S02/S01一致且原子守恒。第3步以EC 4.1.2.2(ketotetrose-phosphate aldolase)将L-erythrulose 1-phosphate裂解为DHAP+formaldehyde，计量平衡(C4H9O7P=C3H7O6P+CH2O)、化学自洽；但此为与gold(S03异构→D-erythrulose 4-phosphate；S04→D-erythrose 4-phosphate)不同的分岐路线，且未声明为替代分支、未给该路线专属证据；E0无EC 4.1.2.2冻结记录，无法判定其错误。主干成立但关键转化需修订、合理性证据有限，5-6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：支持：冻结各步底物/产物isosmiles与方向，用于比对答案结构的立体构型与转化类型；不支持：对所答替代裂解反应作真实酶学定性。
- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;.substrates/products.smiles：支持：答案实际SMILES与辅因子列表，可核对计量与连续性；不支持：把自带引用当作化学事实核验。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 按程序冻结事实：S01/S02/S03均为ROUTE_BLOCKED_NONMATCH（S01/S02立体冲突、S03中段被外源反应替代），S04为ROUTE_BLOCKED_MISSING；S=0、F=3、U=1，confirmed_target_rate=0.0；三个已确认KEY失败适用D-KEY4硬上限4，允许区间&#91;1,4&#93;。逐目标核对：答案S2(激酶EC 2.7.1.53)对S01（accepted为2.7.1.209）、答案S1(EC 1.1.1.122)对S02（accepted为1.1.1.12/56/9/M28/M29）、答案S3(醛缩酶EC 4.1.2.2)对S03（accepted为5.3.1.33），均无目标信用；未命中accepted本身不作已证伪，但路线诊断的NONMATCH是已核固化事实。在&#91;1,4&#93;内取2：模块已交付、前两步反应类别与gold同位置对应、中间体名称可辨认，提供少量局部可读信息（相对1的改善即在此定位），但错误路线内部自洽不获目标信用，核心酶-反应推荐不可用，故取低档2而非3/4。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名与反应类型功能匹配（脱氢酶/激酶/醛缩酶），但均无gene/protein，仅EC标签。EC 1.1.1.122、2.7.1.53与gold(1.1.1.56/1.1.1.9等与2.7.1.209)不同；EC 4.1.2.2对应的是与gold该步异构酶(5.3.1.33/5.3.1.34)不同的催化机制。三者E0均无冻结记录(GAP-128-001/002/003)→UNRESOLVED，不得判错。Step1自评medium并披露EC命名歧义；Step2/3自评high但缺具体催化证据。有合理候选与部分支持、关键酶-反应对应仍缺核验→5档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：支持：本题各必答步的冻结accepted酶名/EC集与步对应；不支持：把『不在集合内』直接当作已证伪，也不证明任意具体蛋白底物谱。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：支持：各必答步的定向反应与底物/产物身份，是逐步NONMATCH/MISSING的事实基础；不支持：对未核EC的真伪裁定。
- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;.enzyme：支持：答案实际交付的三个酶/EC与缺S04；不支持：把自称EC对应视为已支持。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案把三步全部归给Klebsiella aerogenes（TaxID 548，strain=null），并声明complete_pathway_organism_profile_id=ORG_001，即把路线关联升级为整路能力声称。身份为物种级、无株级定位；步级归属与整路能力只引EVID_001（MetaCyc路线页面，无record_id），未交付反应级或菌株级能力证据；E0对TAXID:548无冻结记录（GAP-128-004/023），也未出现可核矛盾，故按UNRESOLVED处理、不判身份编造、不cap。按P69三层区分：身份定位可得部分认可，反应级与全路径能力未核；落入『有合理候选和部分支持但关键身份/作用范围未充分核验』档（5–6），取5（物种级且能力范围超出所交付证据）。

<details><summary>V0.4理由与本行变化背景</summary>

三步微生物统一归 Klebsiella aerogenes(ORG_001, TaxID 548, strain null)，并声明 complete_pathway_organism_profile_id=ORG_001。该菌非gold路线菌(Mycolicibacterium/Pectobacterium/Brucella/Agrobacterium)，但属历史上polyol代谢研究对象(旧名Aerobacter/Enterobacter aerogenes，答案已披露)，为合理候选。身份与整路径能力仅由EVID_001(page级、record_id=null)支撑；TaxID 548 E0无记录；由笼统路线关联直接claim整条路径能力属过度外推。合理候选+部分支持、关键身份与作用范围未充分核验→5档。无已核实身份编造/错配，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_128：支持：冻结步级微生物记录与PATHWAY_COMPLETE行为Mycolicibacterium smegmatis(1772)，说明本题gold另给菌。不支持：据此断言K. aerogenes不能降解L-threitol（gold非穷尽、允许多菌）。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;/complete_pathway_organism_profile_id：支持：答案自称整路菌且未给株级/反应级证据；不支持：把自称当作能力已核。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项性状全字段出现（11项有值、4项如实null：F3/F4/F5/F14），未编造数值，温度仅给『中温菌』偏好并明确未确认边界，单位/数值型缺口以null承载（完成度扣分归D1，不在此重复重扣）。多数一般性状（兼性厌氧、革兰氏阴性、杆状、运动、不产孢、栖息地）标low并指向INTERNAL_KNOWLEDGE_ONLY，属诚实标注。问题在关键项：F7『可代谢L-threitol为碳源』、F8『可裂解为DHAP+formaldehyde』、F9『三步连续降解活性』均标high，却只引本条答案的路线页面（EVID_001），把路线关联当成观测性状；E0对TaxID 548所有性状子字段均无记录（GAP-128-047..053），无法核验其准确性与适用范围。按D4『部分性状准确且适用但关键项证据不足/条件解释需修订』档（5–6）取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现：11项填写(含F2仅填preference、量化字段null)，4项明确null，未编造量化数值。定性性状(革兰氏阴性、兼性厌氧、杆状、不产孢、有运动、栖息地广)符合Klebsiella常识但均标low且来自INTERNAL_KNOWLEDGE_ONLY；F7/F8/F9以high从笼统来源声称整条路径降解能力，属把单步/笼统支持写成整路径能力的过度外推。E0无taxid:548性状记录(GAP-128-047..053)，无法逐一核对。部分性状准确适用、关键项证据不足→5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_128：支持：本题冻结性状记录仅覆盖1772/29471/235/362，无TaxID 548行；不支持：据此判定K. aerogenes任何性状为假。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_128：支持：冻结可评分性状掩码同样未含TaxID 548，说明本快照无可评分参照；不支持：把无参照等同于性状错误。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：支持：实际填写的值、置信度与来源指向；不支持：把INTERNAL_KNOWLEDGE_ONLY当作已核观测。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 按claim group登记来源：核心组均有具名数据库+定位（EVID_002/003/004给ExplorEnz官方EC条目号，EVID_005给NCBI Taxonomy记录号548，EVID_001给MetaCyc路线页面但无record_id），故不属『全部仅有笼统来源』；但E0对1.1.1.122、2.7.1.53、4.1.2.2、TAXID:548及MetaCyc自由文本均无冻结记录（GAP-128-001..023），任何关键结论都无法完成『核对支持内容』，故全部登记UNRESOLVED_SOURCE，不判虚构、不判错引、不cap。性状相关组（CG10–CG16）明确仅有INTERNAL_KNOWLEDGE_ONLY，登记MISSING_SOURCE，属缺失型低档因素但默认不cap。综合：条目级可定位、无法核对→5–6档取5；若未来核验发现官方条目与声称不符，应重估（可能转LOCAL/CRITICAL）。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记见d5_registry：决策相关组CG01/CG03/CG09(路线/终点/全路径能力)仅由EVID_001(MetaCyc page级, record_id=null)=GENERIC_SOURCE支撑，结论与来源关联弱；CG05酶-EC与CG07菌身份有具体EC/TaxID record_id但E0无冻结记录=UNRESOLVED_SOURCE；性状CG10-13来源INTERNAL_KNOWLEDGE_ONLY=MISSING_SOURCE。无VERIFIED_MIS_CITATION_*(无已核实错引)，不cap。条目级引用存在但内容不可核对、CORE路线结论关联弱→3-4档上界取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：支持：答案实际交付的来源类型、库名、记录号/定位与置信度；不支持：这些来源本身真实存在或支持其声称。
- SCOPE_ROW / SCOPE#BIOPATH150_128#CG04：支持：本题条件组冻结登记（氧条件null→FALSE/SUPPORTING）；不支持：对来源真实性作核验。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 披露质量总体较好：uncertainties逐条写明氧条件null、旧名Aerobacter/Enterobacter aerogenes归并、EC 1.1.1.122的D-threitol/多底物表述导致底物特异性较低、formaldehyde下游未确定且不计入评分主链；菌株未知时strain如实null；性状普遍用low+INTERNAL_KNOWLEDGE_ONLY与数据库条目相区分。缺陷：EVID_001以DATABASE_DIRECT/high呈现却无record_id，complete_pathway_organism_profile_id与F7/F8/F9的high置信把『一条路线关联』反复表述为能力/观测，属同一根本断言的单点过度确信，未有系统性掩盖或明知矛盾不披露，故不cap；按P119档内扣分，落到5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体诚实：氧条件null说明、旧菌名(Aerobacter/Enterobacter)与菌株未定、EC 1.1.1.122命名歧义、formaldehyde下游排除均明确；性状多项low/unknown并说明未能解析到单一原始表型记录。但EVID_001标DATABASE_DIRECT/high(实为page级、record_id=null)，F7/F8/F9以high声称整条路径能力，属对核心路线/能力的局部过度确信；无系统性把预测写成实证、无明知掩盖。按SC6单点过度确信不cap、档内扣→6档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties + 各confidence/source_type字段：支持：答案实际作出的不确定性披露与置信标注分布；不支持：这些披露内容在科学上成立。

</details>

## Qwen

答案SHA256：`91d93b6e687dc52873d34b1beb4e29aad0038fdde53c1343b1cb12fe5a8e4e83`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> D1落在&#91;1,4&#93;受限范围。答案只给3步且S03替换为醛缩裂解、缺S04终点，所有步骤缺EC，微生物缺菌株/TaxID，15项性状仅4项填充；核心任务路线未完整交付，按指定路线偏离关键错误封顶4。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块与格式：route_scope.chosen_route_name逐字回显题面路线名&#x27;L-threitol degradation&#x27;；3步均给出主底物/主产物英文名+SMILES、首选酶名与对应菌，steps与organism_profile引用自洽；15项性状全部出现（4项填写、11项显式null/unknown、0项遗漏）；evidence_registry与uncertainties齐备。按5–6档（主要模块均有涉及，但若干必要内容缺失或实质不足）取6：性状仅4/15有实质内容、所有EC为空、菌无株号/TaxID；上述为诚实未知而非编造，故取本档上限而不更低（P15/P45）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：支持题面指定主链要求S03异构化至D-erythrulose 4-phosphate并S04至D-erythrose 4-phosphate；不支持把醛缩裂解到DHAP+formaldehyde作为本题主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_128：支持gold终点身份，不支持答案以DHAP为终点替代。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> D2按化学自身质量评。前两步底物/产物方向与主链前段相符，但辅因子ATP/NAD+未列，属局部计量缺陷；S03醛缩裂解在化学上可设想，却替换了指定主链必需的异构化，且后续无S04至D-erythrose 4-phosphate，故主干仅部分成立、关键转化需实质修订，取5-6档较低分5。

<details><summary>V0.4理由与本行变化背景</summary>

S1（L-threitol→L-erythrulose，脱氢，SMILES OCC(O)C(O)CO→OCC(=O)C(O)CO）与S2（L-erythrulose→L-erythrulose 1-phosphate，磷酸化）与gold主链前两步（reaction_gold S02→S01）方向、结构一致，原子守恒；S3给出醛缩酶裂解生成DHAP+甲醛，产物加和C4H9O7P与原底物一致，作为酮糖磷酸的醛缩断裂在化学上可成立，但该转化与gold的异构酶路线（EC 5.3.1.33→5.3.1.34）不同且无外部证据，按四.5第3步登记为未证实替代（不判错也不给高分）；NAD+/ATP未列为局部计量缺陷（P103，不cap）；答案未声明替代路线边界。5–6档（主干成立、关键转化需修订、合理性证据有限）取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：支持gold主链前两步及S03/S04异构化连续性；不证明答案醛缩裂解路线在本题指定终点下成立。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> D3a受D-KEY4约束：S03为预定义KEY目标且已确认目标反应失败，整维上界4。答案前两步给出可辨认的L-threitol→L-erythrulose→L-erythrulose 1-phosphate局部路线信息，但自动对齐仍为UNRESOLVED；S03用醛缩酶替代异构酶，S04在矩阵中缺失/对齐未确认。无已确认S，按&#91;1,4&#93;受限范围取3：少数局部可用信息与关键失败边界可辨，但核心主功能严重受损。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名&#x27;L-threitol 2-dehydrogenase&#x27;与gold &#x27;erythritol/L-threitol dehydrogenase&#x27;功能同类；S2 &#x27;L-erythrulose kinase&#x27;与gold酶名一致（gold EC 2.7.1.209），答案将EC留null不构成酶名-EC矛盾；S3 &#x27;L-erythrulose-1-phosphate aldolase&#x27;无EC、无gold条目、无E0记录，属未核实候选。无EC大类别与反应类型错配、无以广谱家族相关性冒充具体催化证据，故不触发本维关键错误（错引问题归D5，不在此重复计数）。5–6档（有合理候选和部分支持，若干关键步骤仍缺具体核验）取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：支持各目标步的accepted酶/EC范围；不证明答案具体蛋白或菌株活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：支持指定主链的底物到产物方向及S03/S04反应类型；不支持S03醛缩裂解作为本题目标反应。

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> Klebsiella pneumoniae是真实物种，但未给菌株、TaxID或可定位身份记录；三步均归同一菌且complete_pathway_organism_profile_id=ORG_001，等于无充分证据地把单一步/物种级名义推成整路径能力。Gold各步涉及Mycolicibacterium smegmatis、Pectobacterium atrosepticum、Brucella abortus、Agrobacterium radiobacter；与gold不同不自动判错，但当前缺少K. pneumoniae的步级或整路能力证据，故落在3-4档取3。

<details><summary>V0.4理由与本行变化背景</summary>

三步及complete_pathway_organism_profile_id均指向Klebsiella pneumoniae（物种级、strain=null、ncbi_taxid=null、confidence=low，证据仅EVID_002 INTERNAL_KNOWLEDGE_ONLY）。gold步骤菌为Mycolicibacterium smegmatis/Pectobacterium atrosepticum/Brucella abortus/Agrobacterium radiobacter，与本答案全不相同，但gold非穷尽；E0无Klebsiella记录（GAP-128-026），无法核实其不具备该能力，故key_error=UNRESOLVED、不cap。无编造TaxID/保藏号/登录号（编号类声称全为null）；但把整条路径归于单一物种且无反应级/全路径证据，属未限定作用范围的能力声称，按5–6档（合理候选、关键身份与作用范围未充分核验）取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_128：支持gold各步的已列微生物与整路径菌；不支持把K. pneumoniae自动写成整路径菌，也不证明其无能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> D4只评已给性状。答案仅填F1兼性厌氧、F11杆状、F12革兰氏阴性、F13不产芽孢，这些对K. pneumoniae通常相符且未出现明显数值/单位错误；但温度、pH、盐度、底物谱、基因组等关键定量项均null，且已填4项均无体系来源。缺失完成度主归D1，D4按已给内容与关键缺口取5-6档较低分5。

<details><summary>V0.4理由与本行变化背景</summary>

已填4项：F1&#x27;兼性厌氧&#x27;、F11&#x27;杆状&#x27;、F12&#x27;革兰氏阴性&#x27;、F13&#x27;不产芽孢&#x27;，与K. pneumoniae物种级通行性状一致，未把培养/观测值写成耐受上下限，未把预测冒充观测，无离谱数值；11项（含温度/pH/盐度/基因组）为显式null（明确未知，不按错误计；完成度扣分归D1，P112）。四项均无raw_text与外部来源（EVID_002仅内部知识），关键定量性状缺证据。5–6档（部分性状准确且适用，但关键项证据不足）取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_128：提供gold所列菌的性状参照；不提供K. pneumoniae性状记录，不能用gold其他菌回填。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_128：说明哪些性状子字段可作观测准确性分母；不把缺失项自动当错误。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D5六状态按claim group登记。答案唯一证据EVID_001/EVID_002均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null，无法把路线、酶、菌或性状追到可定位条目；决策相关组均为MISSING_SOURCE，属低分档。未发现经核实的错引，故不触发D5关键错误cap，取1-2档较高分2以反映其至少区分了内部知识与未知。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅EVID_001/EVID_002两条，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null，按四.3/P34全部登记MISSING_SOURCE；决策相关组（CG01/CG02/CG05/CG07/CG09等）全部缺失→低分档，默认不cap。无任何已核实错引（不存在VERIFIED_MIS_CITATION_*），severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。E0唯一记录（TaxID 294 Pseudomonas fluorescens）与本题声称无关，既非支持也非矛盾。答案以claim_scope逐step/逐profile标注内部知识归属，属有限的生成过程说明，但主要结论无法外部定位；低分档取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> D6看证据性质与不确定性表述。答案多处明确null、low/unknown、INTERNAL_KNOWLEDGE_ONLY，并列出氧条件未指定、缺直接文献、EC/菌株/基因组未填等限制，整体较诚实；但route_summary仍把无直接来源的路线称为常见主链，且complete_pathway_organism_profile_id=ORG_001未随该整路径能力声称加限定，属少量过度确信。按7-8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

route_summary、逐步uncertainty与uncertainties数组明确声明&#x27;缺乏直接来源&#x27;、&#x27;低置信推断&#x27;、&#x27;EC/菌株/保藏信息未填&#x27;，unknown/low标签与证据强度相称；区分了未知与推断，未把内部知识包装为数据库直查或实证观测，未掩盖限制，也未系统性夸大。7–8档（大部分观测/预测/未知被正确标注、主要限制已说明）取7；扣分因四项定性性状无raw_text仍以low直填、对S3替代裂解路线未作专门的证据边界说明。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`f34161a6ea3ae256919d5dc085d30e195e59723d96344c0ce45d109cfacdcf7f`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer gives a recognizable partial pathway and three enzyme names, but it omits all microorganisms, all 15 traits, and the gold terminal step. The route also diverges after the first two transformations. This is far from the complete pathway+enzyme+microorganism+traits task, placing it in the 3–4 band and selecting 3 because core modules are broadly absent.

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT：Task requires a main route, each step with enzyme and corresponding microorganism, and 15 traits.
- ANSWER_TEXT / ANSWER_TEXT：Shows only 3 steps, all microorganisms null, empty organism_profiles, and no traits.

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Base D2 range for this case is &#91;1,5&#93;. The answer’s first two transformations are recognizable, but the S1 substrate carries a specified stereochemical conflict; S3 replaces the gold isomerase with an aldol cleavage to DHAP plus formaldehyde; and the gold terminal D-erythrose 4-phosphate step is absent. The main trunk is partly recognizable but multiple important steps/connections are wrong or unsupported, so 3 is selected.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：Gold main chain has entry dehydrogenation, kinase, isomerase to D-erythrulose 4-phosphate, then terminal isomerase to D-erythrose 4-phosphate.
- ANSWER_TEXT / ANSWER_TEXT：Shows the answer’s 3-step sequence and the foreign S3 aldol cleavage.

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The supplied gold/accepted sets and visible answer support only limited target credit. The kinase step has a recognizable accepted name match, but the entry step has a specified stereo conflict, S3 names a different aldolase reaction rather than the gold isomerase, and the terminal target is missing. With only few target functions usable and key/major gaps, the low band 3–4 applies; select 3. No confirmed KEY4 cap is applied because target alignment remains unresolved in the provided registry.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：Gold S01/S02/S03/S04 accepted enzymes and EC families for the required four-step route.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：Gold reaction direction and products; supports comparison of S3 and S4.
- ANSWER_TEXT / ANSWER_TEXT：Shows the answer’s enzyme names, absent ECs, divergent S3 reaction, and missing S4.

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> No microbial identity, strain, TaxID, or capability is delivered. All step.microorganism fields are null and organism_profiles is empty. This is a missing microorganism module, not a detected scientific error.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows all microorganism fields null and organism_profiles empty.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The task requires 15 traits per organism, but the answer provides no organism_profiles and no trait values at all. D4 is therefore MISSING=1; the honest non-fabrication is relevant to D6, not a supply of trait content.

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT：Task requires all 15 traits for each organism profile.
- ANSWER_TEXT / ANSWER_TEXT：Shows no organism_profiles and no trait fields.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All delivered route/enzyme claims trace only to INTERNAL_KNOWLEDGE_ONLY entries EVID_001 and EVID_002, with null database, record, and locator. There are no locatable external sources for the key claims, and microbe/trait/terminal groups lack delivered sources. This is MISSING_SOURCE, not a verified mis-citation; D5 falls in the low band and 2 is selected.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows the evidence_registry entries and null locators; establishes absence of locatable delivered sources, not that the scientific claims are false.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer is unusually transparent about uncertainty: it labels evidence as INTERNAL_KNOWLEDGE_ONLY, gives medium/low confidence, states EC/microbe/gene facts are unverified, lists specific limitations, and does not fabricate microorganisms or traits. Some route assertions remain somewhat assertive, but the main limitations and unknowns are broadly disclosed, supporting the 7–8 band and 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows explicit uncertainty disclosures, low/medium confidence labels, and internal-knowledge-only source status.

</details>

## GPT5.6

答案SHA256：`3b967948d544ebedc2a6da14d026bd43860a9c5a207460d9a84937789ce36447`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定路线L-threitol degradation，本题task_scope（QUESTION_ROUTE_LOCK_PLUS_FULL_GOLD_MAIN_CHAIN）登记4个必答步，并要求每步给主底物/主产物、首选酶及EC、对应微生物，每个profile一次给15项性状。答案只交付1步（S1：l-Threitol→L-Threulose），enzyme与microorganism均为null，organism_profiles为空、15项性状0项。绝大部分必要模块缺失→档&#91;1,2&#93;；因仍给出可辨认的入口转化、路线名原样回显、氧条件未指定如实保留、且未编造酶/菌，档内取2而非1。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT#BIOPATH150_128：支持：题面要求主链逐步给酶/EC与一个对应微生物、每profile 15项性状、路线名原样填写。不支持：任何具体化学或菌株事实。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：支持：gold主链4步（S02→S01→S03→S04）及其各步主底物/主产物与方向，用于确认必答步数与终点；不支持答案已覆盖这些步。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_128：支持：ordered_step_count=4、final_graph_status=LINEAR_UNIQUE，说明本题为单链4步；不支持任何交付质量判断。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已交付的唯一转化：l-threitol（OCC(O)C(O)CO，C4H10O4）→L-Threulose/L-erythrulose（OCC(=O)C(O)CO，C4H8O4），C2位脱氢氧化、方向为污染物→氧化产物、元素与2H差自洽，与gold入口步BSY-r02438（l-Threitol+NAD+→L-Erythrulose+NADH，SUBSTRATE_TO_PRODUCT/reversible）一致。未写NAD+/NADH属局部计量缺陷（P103，单独不cap）。但主链其余3步转化与连接完全未交付，路径止于L-erythulose、未到题面任务终点，连续性不成立→档&#91;5,6&#93;；仅1/4主链且辅因子未列，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_128：支持：S02行BSY-r02438为l-Threitol+NAD+→L-Erythrulose+NADH（SUBSTRATE_TO_PRODUCT，reversible），可核对该底物-产物关系的方向与结构；不支持答案其余3步存在，也不支持任何酶或菌。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：支持：S02目标反应对应erythritol/L-threitol dehydrogenase及EC集合（G4策展粒度）；不支持具体蛋白活性或某菌能力。

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 程序固定事实：4个必答步的酶信息整体未交付（所有step.enzyme=null，无酶名、无EC、无可辨认催化功能），release决定D3a=MISSING、允许区间&#91;1,1&#93;。按C04.2与P44记MISSING=1。D-KEY4上界4被1自然满足，且不据此代签key_error=Y。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_128：支持：本题4步各自存在可接受的酶名/EC（G4策展粒度，如S01 2.7.1.209、S02 1.1.1.x族、S03 5.3.1.33、S04 5.3.1.34），说明目标酶本可填写；不支持答案已交付任何酶。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_128：支持：答案中每个step的enzyme对象均为null，确无酶名/EC/功能交付；不支持任何催化正确性判断。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求每步绑定一个对应微生物并按物种+菌株去重给出profile。答案steps&#91;0&#93;.microorganism=null且organism_profiles=&#91;&#93;，无物种、菌株、TaxID、保藏号或整路能力声称。微生物模块整体缺失→按P44记MISSING=1；不宣称检测到身份或能力错误，也不因D5/D3a低分连坐。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_128：支持：本题各步存在可核对的物种级对应（如Mycolicibacterium smegmatis、Pectobacterium atrosepticum等）与一条PATHWAY_COMPLETE行；不支持答案已交付任何菌或具备整路能力。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_128：支持：答案未填写任何微生物字段、也未给出profile；不支持任何菌株身份或催化能力判断。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles=&#91;&#93;，15项性状一项未交付（filled=0、explicit_unknown=0、omitted=15），无任何profile可承载性状，故不存在可评的数值/单位/条件。按P44与P112，全部必需性状为空记D4=MISSING=1，不宣称检测到科学错误；完成度不足已在D1计一次，不在此重复重扣。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_128：支持：本题各菌的部分性状子字段存在可评观测（如M. smegmatis F10/F11/F12/F13、P. atrosepticum F7/F9）及不可评/仅完整性项；不支持答案已交付任何性状。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_128：支持：温度等子字段的计分口径（部分pending_teacher_adjudication、仅完整性项不作准确率分母）；不改变答案未交付性状这一事实。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案仅登记1条证据EVID_001：source_type=MODEL_INFERENCE，database/record_id/locator均为null，claim_scope仅覆盖S1底物-产物关系。按P34属MISSING_SOURCE（内部推断类），决策相关组（路线、酶、菌、终点）无任何条目级可定位可核来源→低分档&#91;1,2&#93;。E0对本题为EVIDENCE_GAP（仅1条与本题无关的TaxID 294记录），无经核实错引，故不判虚构、不cap、不低到1；因其仍登记claim_scope并标low置信、与D6披露一致，档内取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_128：支持：全文唯一来源记录为内部推断且无库名/记录号/定位；不支持任何外部可定位来源存在。
- E0_EVIDENCE / f3e0:tp:EV146-01：支持：TaxID 294官方对应Pseudomonas fluorescens的种级身份；不支持本题任何L-threitol降解、酶或菌株声称，故不能用于放行本题来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 证据性质披露充分且相称：route_scope.notes与route_summary明示氧条件未指定、后续专一酶/微生物/条件缺乏可核实信息；steps&#91;0&#93;.uncertainty把该步限定为“可作主路线表示”而缺酶/EC/菌；uncertainties逐条列出缺完整路线来源、缺专一酶及EC、缺微生物与15项性状；唯一证据标MODEL_INFERENCE+low，未把推断写成观测，未见掩盖矛盾。属&#91;7,8&#93;上沿；因route_summary正文未在同处标注该转化为模型推断（仅在证据层标注），取8非9。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_128：支持：答案明确标注推断性质、low置信与三类具体未知；不支持任何被省略内容的正确性。

</details>
