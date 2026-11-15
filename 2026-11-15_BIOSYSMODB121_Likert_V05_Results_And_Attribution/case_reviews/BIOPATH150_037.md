# BIOPATH150_037：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：Aldoxime degradation

污染物：Pyridine-3-carbaldehyde oxime；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 68 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 52.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 66 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 49 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 72 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 48.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`11d993dfa789952d1d7c926d403666fd0f3b467d9913858cbc6db74ca9dd59aa`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案给出完整的三步主链、每步底物/产物、酶与EC、对应微生物，并为两个 profile 返回全部15项性状字段；route_scope.chosen_route_name 与题面一致，未见必须模块遗漏或明显范围偏离。仅按D1完整性/任务符合度取9，不因科学置信度低而抬或压。

<details><summary>V0.4理由与本行变化背景</summary>

题面指定路线名（Aldoxime degradation）原样回显，未改选路线；3步主链每步均给出主底物/主产物的英文名与SMILES、一个首选酶及EC、一个对应微生物，并按“物种+菌株”去重为2条profile（OxB-1、J1未合并）；两条profile均完整返回15项性状外壳，未核项按纪律填null而非编造；另附route_summary、uncertainties与evidence_registry。未达9–10档的原因：性状模块大量字段为null/明确未知、无TaxID、无字段级来源，属“大部分必要内容完整、少量遗漏”档。traits计数按首个profile（ORG_001）登记：filled=8、explicit_unknown=7、omitted=0（ORG_002为filled=10、explicit_unknown=5、omitted=0，同样闭合）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the provided route/steps/enzymes/microbes/15 trait fields; does not establish scientific correctness.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_037：Gold route name and terminal nicotinate; supports task-scope comparison only.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 主链化学与gold一致：醛肟脱水为烟腈，烟腈水合为烟酰胺，烟酰胺水解为烟酸并释放氨；方向为污染物向终点烟酸/烟酸盐，原子与连续性成立。S1产物水、S2消耗水、S3释放氨均已给出；差异主要是烟酸/烟酸盐的质子化/电荷表示与肟立体未指定，属表示层小问题，不改变化学主链。

<details><summary>V0.4理由与本行变化背景</summary>

三步化学与gold逐步对应且方向正确：S1 吡啶-3-甲醛肟（ON=Cc1cccnc1）脱水→3-氰基吡啶（N#Cc1cccnc1）+水，对应gold S02（BSY-r03561）；S2 3-氰基吡啶+水→烟酰胺（NC(=O)c1cccnc1），对应gold S03（BSY-r03562，gold行反向标注但化学同一转化）；S3 烟酰胺+水→烟酸（OC(=O)c1cccnc1）+氨，对应gold S01（BSY-r03325）。原子与元素守恒、连接连续、无跳步，终点止于题面/gold指定的烟酸（Nicotinate），下游maleamate途径与吡啶开环另列于downstream_continuation而不计入主链；腈水解酶替代分支明确标注is_part_of_scored_main_route=false。属“关键转化、方向、结构与连接均获可靠支持”档，取9（未给10因辅因子/水以role表达、未统一配平说明）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;EXPLICIT_PROGRAM_CAP_APPLIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the proposed three-step chemistry and connectivity; exact charge/stereo notation not fully specified.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：Gold reaction connectivity and directed substrate-to-product sequence; does not by itself verify enzyme identity or protein activity.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> N=3。答案S2（nicotinonitrile→nicotinamide，nitrile hydratase EC 4.2.1.84）对应gold S03，五态SUPPORTED且credit_class=CONFIRMED_TARGET，计1个S。答案S1（aldoxime dehydratase EC 4.2.1.104）对应gold S02：名称与accepted aldoxime dehydratase(4.2.1)相符，但具体EC配对、立体表示边界及E0官方记录缺口使其仍为U，不能计S，也不能因未命中具体号判F。答案S3（nicotinamide→nicotinic acid+ammonia，amidase EC 3.5.1.4）对应gold S01：accepted为nicotinamidase EC 3.5.1.19，且gold S01因电荷表示边界为UNKNOWN，名称/EC配对与目标功能均UNRESOLVED，计U；尚无合规冻结证据把amidase判为与目标反应不相容，故不记F。由此S=1、U=2、F=M=0，C=S/N=1/3，落入&#91;3,4&#93;候选带。两个U均为KEY但非已确认F/M，不触发D-KEY4的≤4上界；带内取3而非4，因为仅一个目标获已核功能匹配，两个KEY步的表示/证据边界仍未清楚到足以支持该带上沿。U不使整维NE，D3a可Scored并在ne_unverified保留待核。

<details><summary>V0.4理由与本行变化背景</summary>

S2 腈水合酶 EC 4.2.1.84 与gold酶表完全一致（BSY-e03578, 4.2.1.84）；S1 醛肟脱水酶落在gold通配EC-4.2.1族内（gold给4.2.1与4.2.1.84），答案给出同族具体号4.2.1.104，按四.5/四.6保守条款不自动判错，但E0无EC条目记录、无法核accepted name/reaction→UNRESOLVED待核；S3 用amidase EC 3.5.1.4，gold记为nicotinamidase EC 3.5.1.19，二者反应类型（酰胺水解）与酶名不矛盾，属可辩护的候选差异而非类别错配，但缺该具体反应的催化证据。均为“主要步骤有支持、若干关键条目仍需核验”档，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / S2：答案S2为Nicotinonitrile→Nicotinamide，nitrile hydratase EC 4.2.1.84；与gold S03的nitrile hydratase目标匹配。
- ANSWER_TEXT / S1：答案S1为Pyridine-3-carbaldehyde oxime→Nicotinonitrile，aldoxime dehydratase EC 4.2.1.104；名称与accepted aldoxime dehydratase(4.2.1)相符，但具体EC/表示边界待核。
- ANSWER_TEXT / S3：答案S3为Nicotinamide→Nicotinic acid+ammonia，amidase EC 3.5.1.4；与gold S01 accepted nicotinamidase EC 3.5.1.19的名称/EC配对尚待核。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_037：列出本案accepted酶：S01 nicotinamidase 3.5.1.19；S02 aldoxime dehydratase 4.2.1；S03 nitrile hydratase 4.2.1.84。支持S03功能匹配，S01/S02按保守条款保持配对/范围待核。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：给出S02→S03→S01的底物/产物方向及终产物Nicotinate，用于把答案三步对应到目标反应并确认N=3。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_037：路径名为Aldoxime degradation，终产物为Nicotinate，支持任务路线与终点范围。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Bacillus sp. OxB-1 与 Rhodococcus rhodochrous 的主要微生物选择合理；gold有 Bacillus sp. OxB-1 的 PATHWAY_COMPLETE 身份记录，也有 R. rhodochrous 的 S03 物种级记录。主要不足是答案使用 J1 菌株级标识而gold只有物种级/其他菌株记录，且多数微生物证据为内部知识或未可核验文献；按D3b物种支持菌株声称的粒度不足档内扣，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

三步微生物归属的物种均与gold相容：Bacillus sp. OxB-1 出现在gold PATHWAY_COMPLETE（TaxID 98228），Rhodococcus rhodochrous（TaxID 1829）为gold S03步级菌，未见编造、跨属或无关类群；菌株号OxB-1/J1按纪律未填TaxID（null），菌株级身份未获核实，但未用另一菌株编号冒充；答案未声称单一菌完成整条路径（complete_pathway_organism_profile_id=null），身份定位/反应级能力/整路径能力三层未混写。扣分点：S1对杂芳族醛肟的活性、S3把酰胺酶活性归给J1均属推断（答案自述），反应级证据不足。属“主要对应及身份有可靠支持、少量条目需确认”档，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows claimed step-level microbes and strain names; does not establish strain-level activity.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_037：Gold has R. rhodochrous at S03 and Bacillus sp. OxB-1 in PATHWAY_COMPLETE; it does not provide J1 strain-specific identity or Bacillus step-level aldoxime dehydratase evidence.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> R. rhodochrous J1 的革兰氏阳性、无芽孢、不运动、腈水合酶/酰胺酶等与gold物种级记录或已知菌株特性相符；但温度、pH、盐度、保藏号、基因组等多项可获gold观测值仍为null，Bacillus sp. OxB-1 的多数性状仅为属级内部知识，且F1“专性好氧”与gold的aerotolerant记录存在表述强度问题。按部分性状可用、若干关键项证据不足取6，未发现使主要性状结论失效的已核实关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

可与gold观测值比对的性状方向正确：R. rhodochrous 革兰阳性（gold gram positive=true）、不运动（motility=false）、不产孢（sporulation=false）一致；氧需求“专性好氧”与gold aerotolerant=true大体相容但措辞偏强；温度/pH/盐度/保藏号/基因组等gold持有观测值的子字段（DSM 111905、温度28–37 °C、盐度0–6%等）答案全部如实置null，属完成度问题（主归D1），不重复重扣。Bacillus profile 的F1/F6/F7/F8/F9/F11/F12/F13为属级内部知识（EVID_005 low / EVID_001 medium），标注低置信、未把预测冒充实测；无离谱数值、无把物种观测写成全物种耐受极限。属“部分性状准确且适用，但关键项证据不足”档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows all 15 trait slots and values/nulls; does not verify strain-level accuracy.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_037：Gold provides species-level R. rhodochrous observations and only identity/TaxID for Bacillus sp. OxB-1; it does not support Bacillus strain-level trait values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_037：Marks which observed trait fields are scoreable versus completeness-only; does not convert missing/unverified fields into errors.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分3 → V0.5新分5，变化+2。

新裁判理由：

> 答案给EVID_001/EVID_002两条文献描述及EVID_003-EVID_005内部知识条目，但S1/S2无DOI/PubMed ID/记录号，S3和多数性状仅INTERNAL_KNOWLEDGE_ONLY；E0为整题EVIDENCE_GAP，无法核实引用内容。按D5部分关键结论有可定位线索、其他模块缺映射或仅有内部知识取5；未发现经核实的VERIFIED_MIS_CITATION，故不cap。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记：决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）严格按表：EVID_001为无record_id、无DOI、仅“系列论文+年份区间”的文献叙述（GENERIC_SOURCE），EVID_002有期刊/年份/卷但无页码/DOI/条目ID、无法定位到具体反应图表（GENERIC_SOURCE），EVID_003/004/005为INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；性状组（CG10–CG15）同样为内部知识或null；书目组（CG18）无DOI/页码。无任何条目级可定位可核对结论，故不进入5–6档；GENERIC与MISSING混合且核心组存在完全缺失来源，取3–4档的下限3。E0整题缺口，无已核实错引→不触发cap，key_error=N。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows delivered source descriptions and internal-knowledge flags; does not verify citation existence or content.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案在uncertainties中明确说明S1底物谱/EC为记忆值待核、S3酶归属为推断、许多性状无公开记录而置null；confidence字段区分high/medium/low/unknown，未把预测系统性写成观测。个别高置信条目（如J1腈水合酶）属已知特性，未见掩盖主要矛盾或系统性误导。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据性质基本相称：uncertainties明确写出“EC 4.2.1.104按记忆填写、未能与数据库核对”“OxdB对吡啶-3-甲醛肟活性未见明确文献，为一般底物谱推断”“第三步酶/菌归属为级联通识推断（medium）”“多数生理性状无公开记载故置null”；下游maleamate途径与吡啶开环单列为downstream_continuation，腈水解酶分支标注不属于评分主链；置信度大体分层（工业级腈水合酶high，属级性状low/medium，未知unknown）。扣分点：EVID_002以high置信包装无条目定位的文献支持，个别内部知识性状标medium，属单点过度确信而非系统性误导（P119/SC6），档内扣分不cap。属7–8档，取8。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows explicit uncertainty and confidence labeling; does not verify the underlying claims.

</details>

## DeepSeek

答案SHA256：`8f61193ef79e7215ccb8faa82c62aa60c501081d007e0ab579c6e93f8ef86fdc`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> TABLE0 D1 5–6档：主链/酶/菌三个必需模块完整且逐步关联清楚（3步各自底物—产物—酶+EC—菌一一对应），route_scope.chosen_route_name原样回显题面&#x27;Aldoxime degradation&#x27;，与程序task_conformance_status=OK一致；但15项性状全部为占位式null、evidence_registry三条均为INTERNAL_KNOWLEDGE_ONLY且database/record_id/locator全null，属&#x27;若干必要内容遗漏、仅占位或关联不清&#x27;，故不入7–8档；因核心路径与关联无缺步、无路线偏离，档内取6而非5。

<details><summary>V0.4理由与本行变化背景</summary>

路线名逐字填写题面指定的 Aldoxime degradation、氧条件如实置 null，无任务参数偏离；路径（S1–S3 三步，各含主底物/主产物 name+SMILES）、逐步酶（含EC）、逐步微生物三模块均实质交付且步-酶-菌关联清楚。但性状模块15/15全为 null（等于该模块未交付），来源登记仅 INTERNAL_KNOWLEDGE_ONLY、无任何可定位条目。整体落 5–6 档“主要模块均有涉及，但若干必要内容遗漏”，取5（遗漏规模较大，故取该档低端）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_037：证明答案交付了3步主链与1个菌profile，同时证明性状全null、来源清单不可定位；不用于支持任何科学正确性判断
- QUESTION_TEXT / question.json#BIOPATH150_037：题面要求每步底物/产物/酶+EC/菌、15项性状及各项最强来源、未知填null；仅作完成度比对基准

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> TABLE0 D2 7–8档：三步化学为醛肟脱水（ON=Cc1cccnc1→N#Cc1cccnc1 + H2O，脱水酶）、腈水合（N#Cc1cccnc1 + H2O→NC(=O)c1cccnc1，水合酶）、酰胺水解（NC(=O)c1cccnc1 + H2O→OC(=O)c1cccnc1 + NH3），每步原子/质量与H2O共底物明确、无跳步，方向为污染物→烟酸，终点与gold terminal(Nicotinate)一致，无方向反转或中心代谢物跳跃；局部扣分仅两处：起点醛肟未标E/Z立体（gold为E型），S01/S02的gold表示等价性（charge/stereo blind）仍在BR裁定中，故取本带上沿8而不上探9（D2 9–10门本案未为真）。

<details><summary>V0.4理由与本行变化背景</summary>

三步主链化学连续且方向正确：①醛肟脱水（ON=Cc1cccnc1 → N#Cc1cccnc1 + H2O，C6H6N2O→C6H4N2+H2O）；②腈水合（N#Cc1cccnc1 + H2O → NC(=O)c1cccnc1）；③酰胺水解（NC(=O)c1cccnc1 + H2O → OC(=O)c1cccnc1 + NH3）。三步底物-产物对与 gold reaction_gold 的三对（Pyridine-3-carbaldehyde oxime→3-Cyanopyridine→Nicotinamide→Nicotinate）逐化合物一致，终点达 gold terminal Nicotinate，与题面路线 Aldoxime degradation 相符；无起始步错误、无方向反转、无跳步，水为辅底物/副产物标注合理、计量可平。仅缺独立外部支持（该问题归D5），不足以压低本维，取9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：gold有序主链S02(醛肟→3-氰基吡啶+H2O)、S03(3-氰基吡啶+H2O→烟酰胺)、S01(烟酰胺+H2O→烟酸+铵)的名称/方向/化学计量；不支持醛肟E/Z或烟酸/烟酸盐电荷记法的结构等价裁定
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_037：仅支持起点底物与终点产物身份（root=Pyridine-3-carbaldehyde oxime，terminal=Nicotinate）；不支持任何具体酶或菌的能力

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> N=3（gold LINEAR_UNIQUE 3 个必答目标）。逐目标看：答案S2（order 2，nitrile hydratase EC 4.2.1.84）对应gold S03 nitrile hydratase，目标功能/显式EC配对为CONFIRMED_TARGET/MATCH/SUPPORTED，计一个S。答案S1（order 1，aldoxime dehydratase EC 4.99.1.5）对应gold S02，名称与目标醛肟脱水酶一致，但显式EC与参考accepted EC 4.2.1的表示/配对仍因路线表示边界（REPRESENTATION_EQ_STEREO_BLIND）及E0 GAP未核，计U；不得当S，也不得因未命中accepted自动判F。答案S3（order 3，Amidase EC 3.5.1.4）对应gold S01 nicotinamidase EC 3.5.1.19，目标accepted酶不同且S01存在电荷表示边界（REPRESENTATION_EQ_CHARGE_BLIND），目标功能/配对未核，计U；无已核失败证据，不能判F。S=1、U=2、F/M=0，无已确认KEY失败，故D-KEY4不触发；但两个U落在KEY入口/终点，不能进入7–8档。该维仍可判：一条必答步有明确功能匹配，且其余为有定位的表示/证据待核而非已证错误，故不整维NE；按C04/C05取部分主干支持档的下沿5分，而非把U机械当失败或取中点。

<details><summary>V0.4理由与本行变化背景</summary>

S2 nitrile hydratase + EC 4.2.1.84 与 gold 该步酶行完全对应；S1 aldoxime dehydratase 与脱水反应类型匹配，EC 4.99.1.5 为该酶的具体号，gold 侧为 4.2.1 通配，按四.5 通配EC保守条款不因具体号与通配不同判错；S3 amidase EC 3.5.1.4 属酰胺C–N水解族，与 gold 的 nicotinamidase EC 3.5.1.19 为同族替代、特异性略弱但反应类型无矛盾。三处EC在E0中均无冻结记录，无法核 accepted name/reaction（UNRESOLVED待核，不作已核实错误）。主要步骤酶-反应对应成立、仅少量条目待确认，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_037：列出本题gold三步酶名/EC：S01 nicotinamidase EC 3.5.1.19、S02 aldoxime dehydratase EC 4.2.1、S03 nitrile hydratase EC 4.2.1.84；仅支持参考酶名/EC集合，不证明答案任意具体蛋白活性或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：支持本题三步主反应定位：S02 aldoxime→3-cyanopyridine，S03 3-cyanopyridine↔nicotinamide（gold方向为REVERSED_TO_COMPLETE_NAME），S01 nicotinamide→nicotinate+ammonium；支持反应化学/方向定位，不自动证明答案酶配对。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_037：确认本案LINEAR_UNIQUE且ordered_step_count=3，用于N=3和分母边界。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_037：确认路径名Aldoxime degradation、起点Pyridine-3-carbaldehyde oxime、终点Nicotinate；不单独证明每步酶催化。
- ANSWER_TEXT / ANSWER.steps：答案原文：S1 aldoxime dehydratase EC 4.99.1.5；S2 nitrile hydratase EC 4.2.1.84；S3 Amidase EC 3.5.1.4；用于逐目标比对D3a。
- RUBRIC_CLAUSE / C04：D3a在存在U时的JUDGE_REQUIRED处理、非重叠分带与不得把未核当F/NE的条款。
- RUBRIC_CLAUSE / C05：D3a 1–10档内锚点，尤其5分“部分主干目标有适用支持”、7–8不得含KEY U、带内上沿需同时充分满足。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> TABLE0 D3b 7–8档取低沿：微生物身份层有可靠支持——organic名与菌株&#x27;Bacillus sp. OxB-1&#x27;与gold PATHWAY_COMPLETE记录（TaxID 98228，pathway_complete=TRUE）名称+菌株完全一致，整路能力层亦有该记录支持，且答案按题面允许TaxID未知填null（未编造）；但步骤层酶归属（4.99.1.5/4.2.1.84/3.5.1.4同属一菌）缺反应级证据，gold步级organism行分别指向Pseudomonas chlororaphis、Rhodococcus YH3-3、Rhodococcus rhodochrous，未列Bacillus步级归属，属&#x27;少量具体条目需确认&#x27;，故取7不上探8。

<details><summary>V0.4理由与本行变化背景</summary>

三步微生物归属统一为 Bacillus sp. OxB-1，ncbi_taxid 如实填 null（未编造编号）；该“物种+菌株”名与 gold organism_gold 的 PATHWAY_COMPLETE 记录 Bacillus sp. OxB-1（taxid 98228，pathway_complete=TRUE）逐字一致，属本题 gold 承认的整条路径菌，身份定位与全路径能力方向一致。缺项在于：未交付 TaxID/保藏号，也未给步级反应能力证据，nitrile hydratase/amidase 两步归属属内部知识推断。按“主要微生物对应及身份有可靠支持，仅少量具体条目需确认”取7；E0 无法核验编号类声称，登记待核而非判错。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_037：支持存在PATHWAY_COMPLETE行(TaxID 98228,pathway_complete=TRUE)及步级organism行(587753/No TaxID 6186/1829)；不支持Bacillus sp. OxB-1携带答案所列三种酶
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_037：purely身份侧：trait_gold以TaxID 98228标organism_name=&#x27;Bacillus sp. OxB-1&#x27;、scope=PATHWAY_COMPLETE；其15项性状均为UNKNOWN，不支持任何表型/性状主张

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> P44/P112：organism_profiles&#91;0&#93;.traits下F1–F15共15项value全部为null（confidence=unknown、evidence_id=null），属&#x27;全部必需性状均为null/空值&#x27;，按合同记MISSING=1，不宣称检测到科学错误；性状缺失的完成度扣分已在D1体现，此处不双重重扣。

<details><summary>V0.4理由与本行变化背景</summary>

organism_profiles&#91;0&#93;.traits 的 F1–F15 共15项 value 全为 null、raw_text 与 evidence_id 均为 null、confidence=unknown，性状模块整体未交付。按 rubric 四.4/P44（全部必需性状为null/空值时D4按MISSING记1分，不宣称检测到科学错误）记 MISSING=1，权重保留参与总分；完成度不足已在D1反映，此处不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_037：仅说明gold侧存在可评分性状遮罩（如587753/1829的F1–F14 observed），用于确认&#x27;任务要求15项&#x27;；不得回填为答案交付内容，也不得据此判答案错误

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> D5 1–2档：decision-relevant组（CG01/CG02/CG03/CG05/CG07）来源全为INTERNAL_KNOWLEDGE_ONLY自我声明（P34 MISSING_SOURCE），evidence_registry三条的database/record_id/locator全为null，任何关键结论都无法定位到可核对条目或计算记录；不属已核实错引（E0=EVIDENCE_GAP，未核≠虚构），默认不cap（P34/P41）。档内取2而不取1：答案至少以EVID_001–003按步绑定claim_scope并如实标low，读者可判定&#x27;全部为内部知识、不可外核&#x27;；1分档留给完全无映射或经核实引用不存在/不相关的情形。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组 CG01/CG02/CG03/CG05/CG07（CORE）、CG08（APPLICATION_CRITICAL）、CG09（CORE）的来源状态全部为 MISSING_SOURCE：三条证据 EVID_001–003 均为 INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 全 null，路径、酶-EC、菌身份与全路径能力均无条目级可定位记录可追查，连笼统库名/文献列表都没有。无任何经核实错引（E0为EVIDENCE_GAP，编号类声称保持UNRESOLVED），按 P34/P41“全部缺失→低分档、默认不cap”落 1–2 档；缺失覆盖全部核心组，故取该档上限2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_037：证明答案实际交付的来源仅为内部知识声明、无任何可定位外部条目；不用于证明任何结论为真或为假

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> D6 7–8档取低沿：答案把三类步级证据统一标为INTERNAL_KNOWLEDGE_ONLY+low，null使用诚实（性状全null、TaxID null），uncertainties明确写出&#x27;氧条件未指定&#x27;&#x27;菌株保藏编号、基因组及多数表型性状未知&#x27;，未把预测写成观测，也无掩盖矛盾；但enzyme.confidence与microorganism.confidence标为medium而所据证据为low/内部知识，属单点强度与依据不相称的档内扣分（P119，非系统性误导、不cap），故取7不上探8。

<details><summary>V0.4理由与本行变化背景</summary>

正面：15项性状全部标为 null/unknown，uncertainties 明列“氧条件未指定”“菌株保藏编号、基因组及多数表型性状未知”，未把预测写成观测；证据登记自标 INTERNAL_KNOWLEDGE_ONLY/low，属诚实披露。问题：steps&#91;*&#93;.enzyme 与 microorganism 的 confidence 一律 medium，而其自建证据明标 INTERNAL_KNOWLEDGE_ONLY/low，结论强度超过依据（单点过度确信、非系统性误导）；不确定性说明偏笼统，未点明酶号与菌株能力为记忆推断、也未提出待复核的替代酶（如 nicotinamidase）。按 5–6 档“有不确定性说明但过于笼统、部分结论强度超过依据”，取6，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_037：证明答案的证据性质标注、置信度标签与不确定性披露实文；不支持任何科学断言为真

</details>

## Kimi

答案SHA256：`4461ae11f1098e306e33efddeea8edab4519ac02b4c37294e2efb3c9c2fdfe43`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 答案返回单一JSON，route_scope.chosen_route_name逐字为题面指定的 Aldoxime degradation，氧条件按题面null处理；3步覆盖从吡啶-3-甲醛肟到烟酸的主链，每步均给主底物/主产物英文名与SMILES、酶及EC、对应微生物；两个organism_profiles按物种+菌株去重，且每株均返回15项性状外壳，未知项以null/unknown标注。未发现关键任务模块缺失、改选路线或重要格式缺陷。部分性状为诚实未知，构成少量完成度扣减，故取9而非10。

<details><summary>V0.4理由与本行变化背景</summary>

档位9：全部适用任务模块实质交付——主链3步均给出底物/产物英文名与SMILES、一个首选酶及EC、一个对应微生物；route_scope.chosen_route_name原样回填题面路线名“Aldoxime degradation”，氧条件null与题面一致；两株菌按物种+菌株去重（ORG_001/ORG_002），每个profile的15项性状逐项返回，未知项以null明确标注；无模块缺失、无范围偏离，仅存在需在D3a/D4/D5/D6处理的证据强度问题，故不入10档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_037：题面要求原样填写 Aldoxime degradation、逐步给底物/产物/酶EC/微生物、每profile填15项性状，未知填null。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_037：本题gold主链ordered_step_count=3，final_graph_status=LINEAR_UNIQUE，用于核对答案是否覆盖一条三步主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_037：题面路线名为 Aldoxime degradation，gold终点主产物为 Nicotinate；支持D1任务范围与终点核对。
- ANSWER_TEXT / 4461ae11f1098e306e33efddeea8edab4519ac02b4c37294e2efb3c9c2fdfe43：答案实际包含3个step、route_scope、2个organism_profiles及每profile 15项性状字段。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链化学方向与连续性成立：S1醛肟脱水生成3-氰基吡啶，S2腈水合生成烟酰胺，S3酰胺水解生成烟酸并释放氨；S1产物即S2底物、S2产物即S3底物，终点烟酸与gold terminal Nicotinate一致。各步水/氨的role已标注，主要原子与电荷关系无已核不守恒；alternative nitrilase支路明确标为不属于评分主链。局部问题为S1醛肟未明确E/Z表示，以及S3所用amidase与gold nicotinamidase不同；后者主要归D3a/D5酶对应与来源判断，D2按化学转化本身评价。因本题D2的nine_ten_eligible=false，取允许上限8。

<details><summary>V0.4理由与本行变化背景</summary>

档位8：三步化学转化（醛肟脱水→腈水合→酰胺水解）方向正确、逐级衔接且计量守恒（S1 C6H6N2O→C6H4N2+H2O；S2 +H2O→C6H6N2O；S3 +H2O→C6H5NO2+NH3），起点与终点（烟酸）与gold主链和terminal一致，无首步错误、无无依据跳步或方向反转。扣分点为S1对芳香醛肟的直接底物证据有限（答案自述）及S3酰胺水解与gold nicotinamidase步的机制证据不足，属局部问题、不改变主链成立，故不入9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：gold主链反应方向：S02（吡啶-3-甲醛肟→3-氰基吡啶）、S03（3-氰基吡啶→烟酰胺）、S01（烟酰胺→烟酸+铵），支持D2核对三步转化和连接。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_037：root为Pyridine-3-carbaldehyde oxime，terminal为Nicotinate，支持终点与降解方向核对。
- ANSWER_TEXT / 4461ae11f1098e306e33efddeea8edab4519ac02b4c37294e2efb3c9c2fdfe43：答案S1-S3的底物/产物名称、SMILES、reaction_type及主/辅因子角色，用于核对化学连续性与计量表达。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> N=3。gold S03（腈水合酶 EC 4.2.1.84）对应答案S2，名称与EC匹配且目标合同为SUPPORTED，计1个S。gold S01（烟酰胺酶 EC 3.5.1.19）对应答案S3 amidase EC 3.5.1.4：名称/EC不在该步accepted集合内，且冻结证据GAP不能确认其催化烟酰胺或确认不相容，按U/SUPPORT_GAP，不按F。gold S02（醛肟脱水酶，accepted EC 4.2.1 wildcard）对应答案S1 EC 4.2.1.115：同family具体号可能合法，但具体名称-EC配对与表示边界未核，按U/PAIR_UNVERIFIED。无已确认KEY失败或实证漏交付，故不触发D-KEY4的4分上限；但两项为KEY/MAJOR U，不能进入7-8。按C05部分主干目标有适用支持、待核部分明确的5-6档取较低值5，避免把未知当失败或当成功。

<details><summary>V0.4理由与本行变化背景</summary>

档位6：S2 nitrile hydratase EC 4.2.1.84与gold完全一致；S1 aldoxime dehydratase属gold通配EC 4.2.1族但具体号4.2.1.115在冻结快照无记录，需官方accepted name/reaction核验；S3以amidase EC 3.5.1.4替代gold nicotinamidase EC 3.5.1.19，反应类型同为酰胺水解、酶名与EC内部自洽，但对该底物的催化仅有内部知识且答案自标low。属“有合理候选与部分支持、若干关键步骤仍缺具体核验”，不入7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_037：gold酶行：S01 nicotinamidase EC 3.5.1.19；S02 aldoxime dehydratase EC 4.2.1；S03 nitrile hydratase EC 4.2.1.84。支持逐目标步酶名/EC核对，不证明具体蛋白底物谱。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：用于把答案S1/S2/S3映射到gold S02/S03/S01的目标反应与方向；不支持把具体EC配对或蛋白活性自动确认。
- ANSWER_TEXT / 4461ae11f1098e306e33efddeea8edab4519ac02b4c37294e2efb3c9c2fdfe43：答案实际酶声称：S1 aldoxime dehydratase EC 4.2.1.115；S2 nitrile hydratase EC 4.2.1.84；S3 amidase EC 3.5.1.4；用于D3a逐目标步比对。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> D3b取5–6档上沿6：P. chlororaphis与R. rhodochrous物种身份分别与gold organism行相容，S2 nitrile hydratase对应的R. rhodochrous有支持；但P. chlororaphis B23的菌株/OxdA声称及J1末端amidase能力仅有internal/低置信支持，TaxID均null，关键末端能力未充分核验。

<details><summary>V0.4理由与本行变化背景</summary>

档位7：S1菌Pseudomonas chlororaphis与gold S02记录物种一致（TaxID 587753），B23是该酶的代表菌；S2菌Rhodococcus rhodochrous与gold S03记录物种一致（TaxID 1829），J1为腈水合酶工业代表菌；S3沿用J1酰胺酶属合理候选但步级证据不足。菌株级身份（B23/J1）与步级能力均无条目级记录，按粒度不足档内扣分、不cap；答案未编造TaxID/保藏号（全为null），也未把单步菌写成整条路径菌（complete_pathway_organism_profile_id=null）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_037：显示P. chlororaphis与R. rhodochrous的物种级步骤对应；不确认B23/J1菌株级身份或末端amidase活性。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> D4取5–6档下沿5：两profile均填满15项，但温度/pH/盐度/保藏/基因组等关键定量项为null；已给一般性状中Gram、运动性、产孢、杆状等大体与物种级trait_gold相符，F6定O2、F7/F8底物/降解能力多为internal-only或未获gold支持。缺失完成度主要归D1，D4按已给内容与关键缺口取5。

<details><summary>V0.4理由与本行变化背景</summary>

档位7：已填性状与gold物种级观测大体吻合（P. chlororaphis：运动性true、杆状、革兰氏阴性、不产孢；R. rhodochrous：无运动性、革兰氏阳性、不产孢），F1/F6氧相关描述与gold aerotolerant记录方向一致但语义不完全等同；温度/pH/盐度/保藏/基因组按null明确未知，属诚实null、不判错（完成度已在D1计入）。扣分点为F7/F8以内部知识或自由文本把酶存在外推为醛肟/腈类利用与降解能力，以及F1/F6以medium置信承载未核实内部知识，故不入8档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_037：支持部分革兰、运动性、产孢、形态等物种级性状；不支持答案所有F6/F7/F8及关键定量值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_037：指示部分性状/子字段可评分或仅completeness；不替答案补值。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> D5取3–4档上沿4：决策相关来源多为笼统作者/主题型文献（EVID_001/EVID_002，record_id与DOI均null）或INTERNAL_KNOWLEDGE_ONLY（EVID_003–005）；无条目级可核对记录。未发现经核实的VERIFIED_MIS_CITATION_*，E0的EVIDENCE_GAP只保持UNRESOLVED，不cap，故取4。

<details><summary>V0.4理由与本行变化背景</summary>

档位4：决策相关组（CG01/CG02/CG05/CG07/CG08）的来源全部为“作者+主题”式自由文本文献（record_id=null、无DOI/PMID）或INTERNAL_KNOWLEDGE_ONLY，无任何条目级可定位可核对结论；E0为整题EVIDENCE_GAP，EC号与菌株身份无法核验，一律UNRESOLVED，不判虚构、不判CONTRADICTED、不cap。因答案逐条给出claim_scope、source_type与confidence并保持组间边界，取3–4档上限4；该分不含任何已核实错引的cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示答案实际交付的来源类型与locator；不证明其文献真实性或支持的底物谱。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> D6取7–8档上沿8：答案明确标注S1底物特异性有限、S3酰胺酶缺直接实验证据、温度/pH/盐度/基因组等null、氧条件未指定，并区分high/medium/low；未见系统性把预测写成实证。S2的high置信度来源粒度偏粗已在D5扣分，但属单点过度确信而非系统性误导，D6不cap。

<details><summary>V0.4理由与本行变化背景</summary>

档位7：uncertainties数组具体列出四类限制（S1底物特异性、S3直接证据缺失、性状null原因、氧条件null），S1菌-酶标low、S3标low，未知项统一null且注明“按null如实记录”，属“大部分观测/预测/未知被正确标注，主要限制已说明”。扣分点为F1/F6/F11–F13等内部知识性状仍以medium置信呈现（单点过度确信），但无系统性把预测写成实证、无掩盖已知矛盾，故不cap，不入8档。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案对主要未知、证据强度与边界的披露；不证明被披露事实本身为真。

</details>

## Qwen

答案SHA256：`a5d8740a20d8fb56423fa7be7f7893d3dc0249b30c369d59e6f995ca52574cf8`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 三步路径、酶/EC、对应微生物及路线名均给出；15项性状在两个profile中全部为null（明确未知），虽符合题面“不确定填null”，但性状模块仅有占位，完成度不足；无任务路线偏离。按D1 5–6档取6：主模块均有涉及、关联清楚，但性状模块全占位。

<details><summary>V0.4理由与本行变化背景</summary>

路径、酶、微生物三个模块逐步齐备：S1–S3各含主底物/主产物（含SMILES）、一个首选酶+EC、一个对应菌，route_scope.chosen_route_name原样填&#x27;Aldoxime degradation&#x27;，主链止于烟酸，符合题面路线与终点范围，故不属核心模块大部缺失或路线偏离。但任务要求的15项性状在两个profile中全部为null（仅占位、无实质内容），且来源模块仅有内部知识声明，属&#x27;主要模块均有涉及，但若干必要内容遗漏、仅占位&#x27;的5–6档；因缺失面覆盖整个性状模块，档内取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：用于核对答案覆盖的步骤、酶、微生物、性状与来源字段；不证明其科学正确性。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 三步化学与gold主链一致：醛肟脱水→烟腈，腈水合→烟酰胺，酰胺水解→烟酸；方向、主要原子收支和步骤连接正确。仅S1立体/电荷表示与S3烟酸质子化/烟酸根表示存在表示等价待核，属局部表示问题，不改变主链；按7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链三步化学与gold BSY-p00343的线性顺序一致：S02醛肟脱水（Pyridine-3-carbaldehyde oxime→3-cyanopyridine/nicotinonitrile+H2O）、S03腈水合（→nicotinamide）、S01酰胺水解（→nicotinate+ammonium）。方向均为正向、原子与连接合理（烟腈C1=CC(=CN=C1)C#N、烟酰胺C(=O)N、烟酸C(=O)O），止于题面与gold共同终点nicotinate，无起始步错误、无无依据跳步。局部问题：S2/S3把水写作role=unknown而非cofactor/substrate、氨SMILES简写为&#x27;N&#x27;、未标注重量/辅因子细节，属不改变主结论的局部表达与计量缺陷（P103/P104），7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：支持gold三步主链的底物/产物、方向与连接；不支持答案具体酶或菌株的实验活性。
- ANSWER_TEXT / ANSWER：用于比对答案给出的化学转化；不证明其外部来源。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 按C03逐目标核：答案S2（nitrile hydratase EC 4.2.1.84，nicotinonitrile→nicotinamide）与冻结accepted S03匹配，计S；答案S1（aldoxime dehydratase，EC 4.99.1.5）名称对应S02，但EC与冻结accepted 4.2.1不一致且无官方条目可核，计U；答案S3（amidase EC 3.5.1.4，nicotinamide→nicotinic acid）与冻结accepted nicotinamidase EC 3.5.1.19不一致，且不能由一般酰胺酶自动确认目标酶功能，计U。S=1、N=3、C=0.333，落&#91;3,4&#93;。无已核KEY失败/F/M，U不能自动判错或整维NE；仅少数目标已确认，两个关键主功能仍待核，边界不清晰，按C05取3而非4。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名与反应类型逐一对应：aldoxime dehydratase（脱水）、nitrile hydratase EC 4.2.1.84（水合，与gold r03562逐字一致）、amidase EC 3.5.1.4（酰胺水解，gold为nicotinamidase EC 3.5.1.19，具体号不同但同属酰胺水解功能大类）。S1给出4.99.1.5，gold侧为EC-4.2.1，属通配/版本次差异（四.5保守条款，不自动判错）。三条EC均无E0记录可核（GAP-037-002/006/008/009/017/019），保持UNRESOLVED；S3用一般酰胺酶替代特异性烟酰胺酶，答案自身已声明该不确定性。整体为&#x27;主要步骤酶对应有可靠支持、少量条目需确认&#x27;，7–8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_037：gold accepted enzyme names/ECs at curated reaction level: S01 nicotinamidase 3.5.1.19; S02 aldoxime dehydratase 4.2.1; S03 nitrile hydratase 4.2.1.84; does not prove specific protein substrate spectrum or experimental activity
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：target reaction substrate-product/direction: pyridine-3-carbaldehyde oxime→3-cyanopyridine; 3-cyanopyridine→nicotinamide; nicotinamide→nicotinate
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：answer&#x27;s own enzyme claims and step products
- RUBRIC_CLAUSE / C04：U&gt;0 does not automatically require NE; unresolved target support is scored by available S/N and confirmed evidence
- RUBRIC_CLAUSE / C05：within &#91;3,4&#93;, select lower score when only a few targets are usable and the boundary to unresolved major targets is not clear

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出每步对应菌，未声称complete pathway（complete_pathway=null）。R. rhodochrous J1与gold的R. rhodochrous（TaxID 1829）物种级相符，但菌株J1无本案证据；Rhodococcus sp. N-774不在gold的YH3-3/P. chlororaphis/N-771等记录中，且无TaxID。三层身份/单步能力/全路径能力均未核，属5–6档“合理候选、关键身份与作用范围未充分核验”，取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案按步归属菌、未把单步菌写成整路径菌（complete_pathway_organism_profile_id=null），且未编造任何TaxID（全null）。S2 R. rhodochrous J1 与gold S03物种级记录（TaxID 1829）一致；但S1用 Rhodococcus sp. N-774，gold S02记录为Rhodococcus YH3-3或Pseudomonas chlororaphis；S3用 R. rhodochrous J1，gold S01为P. chlororaphis。三处均为真实存在的分类单元、非虚构编号，步级催化能力无证据且自述低置信，属&#x27;有合理候选和部分支持，但若干关键身份或作用范围仍未充分核验&#x27;（5–6档取5）。按身份阶梯与&#x27;未核≠错误&#x27;，未核实推翻主要微生物推荐，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：gold给出P. chlororaphis、Rhodococcus YH3-3、R. rhodochrous 1829等物种/菌株对应；不支持答案J1或N-774的菌株级归属。
- ANSWER_TEXT / ANSWER：用于定位答案实际给出的菌名/菌株；不证明其身份或能力。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 两个organism_profiles的15项性状全部value=null、confidence=unknown、evidence_id=null；没有交付任何可评价性状值。按P44/D-TRAITS，全部必需性状null记MISSING=1，不宣称科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

任务要求每个organism_profile一次返回15项性状；答案两个profile的F1–F15共30个字段全部value=null、confidence=unknown、evidence_id=null，未交付任何可评价性状数值，属&#x27;全部必需性状均为null/空值&#x27;情形，按P44记MISSING=1（表示未提供可评价结果，不宣称检测到科学错误），并与D1的完成度扣分分别记录、不重复计为科学错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：用于确认所有15项性状均为null/unknown；不评价其缺失背后的科学真假。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> evidence_registry三条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null；CORE路线/酶/菌结论无任何可定位文献、数据库条目或计算记录。按MISSING_SOURCE低分档，1–2档取1；无已核实错引，不触发D5 cap。

<details><summary>V0.4理由与本行变化背景</summary>

三条evidence均为source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null，按四.3属MISSING_SOURCE；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08）全部缺失来源，D5落低分档（1–2），且MISSING_SOURCE为缺失而非误导、默认不cap。答案至少在每条evidence上登记了claim_scope并显式自述内部知识、低置信，略优于完全空白，档内取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：用于确认答案仅交付INTERNAL_KNOWLEDGE_ONLY且无外部定位信息；不把内部声明当作可核来源。

</details>

### D6 不确定性与诚实度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 答案明确标注所有关键酶/EC/菌归属为low/INTERNAL_KNOWLEDGE_ONLY，uncertainties列出氧条件未指定、来源不足、性状全null、amidase非特异等；未把推断冒充观测。证据性质与置信度相称，仅因来源缺失不影响D6诚实披露，按9档。

<details><summary>V0.4理由与本行变化背景</summary>

答案把全部结论标注为内部知识来源并统一给low/unknown置信，未把预测或推断包装成观测；uncertainties逐条列出四类具体限制（氧条件未指定无法判好氧/厌氧、酶EC与菌归属无外部来源、性状全null、S3用一般酰胺酶而非烟酰胺酶），各step.uncertainty也逐点说明。无掩盖矛盾、无高置信包装，置信表达与依据相称，符合9–10档&#x27;披露具体、边界清楚、诚实说明未知&#x27;；因未讨论替代宿主/酶候选（如gold所列P. chlororaphis）的取舍，档内取9。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：用于核对答案对未知、低置信与内部知识的披露；不证明其科学内容正确。

</details>

## Grok

答案SHA256：`9e47d764c70eb78b7a07f511a277edd4d78145a558f999550333a3b29a5061da`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链三步、每步底物/产物/SMILES、首选酶及EC、对应微生物均给出；两个organism_profile按物种+菌株去重，15项性状字段齐全。性状中多项诚实填null，完成度中上但非全满，故取7–8档上沿外的8分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_037：gold formal case为LINEAR_UNIQUE且ordered_step_count=3；答案给出3步主链。该证据不证明酶学正确性。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步化学为醛肟脱水→腈→酰胺→羧酸，方向为主链降解方向，终点为烟酸，步骤连续且主要计量可配平。S1底物立体未指定、末端酶选择差异不在D2强行判错；作为表示层/局部问题处理，主链科学质量良好。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：gold反应行给出S02醛肟→3-氰基吡啶、S03 3-氰基吡啶→烟酰胺、S01烟酰胺→烟酸+铵的连续主链；不核验答案具体蛋白活性。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 仅评D3a目标反应相应粒度的酶/功能支持。N=3；按当前target_fact_contract，gold S03对应answer order 2（step_id S2）的nitrile hydratase EC 4.2.1.84，target function/name-EC为CONFIRMED_TARGET/SUPPORTED，记S。gold S01（answer order 3，amidase EC 3.5.1.4；gold accepted为nicotinamidase EC 3.5.1.19）与gold S02（answer order 1，aldoxime dehydratase EC 4.8.1.2；gold为4.2.1通配类）均为ROUTE_HOLD_REPRESENTATION/UNRESOLVED（REFERENCE_OR_EVIDENCE_UNAVAILABLE），不判F、不判M，也不能计为S。因此仅1/3必答目标获已核粒度支持，另2个KEY/MAJOR目标的功能及名-EC配对仍待核。无已核KEY失败，故不触发D-KEY4；但KEY/MAJOR U阻断7–8与9–10。C04/C05下，3–4上沿需已核可用部分、适用范围及关键边界均充分；这里两个核心目标仍待核，故取本带下沿3，不把未知当支持或错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_037：列出gold已接受酶名/EC：S01 nicotinamidase 3.5.1.19；S02 aldoxime dehydratase 4.2.1；S03 nitrile hydratase 4.2.1.84。仅支持数据库策展粒度G4的反应功能，不证明具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：定义本题三步主链反应及方向：S02 吡啶-3-甲醛肟→3-cyanopyridine；S03 3-cyanopyridine→nicotinamide；S01 nicotinamide→nicotinate+ammonium。用于将answer S1/S2/S3映射到gold S02/S03/S01；不证明具体酶活性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_037：确认本题为Aldoxime degradation、LINEAR_UNIQUE、3 ordered steps；不提供酶功能支持。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_037：确认路线名Aldoxime degradation及终点Nicotinate；不提供酶功能支持。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Bacillus sp. OxB-1与Rhodococcus rhodochrous J1在gold中有身份/路径能力支持，R. rhodochrous TaxID 1829正确；未把单步菌写成整路菌。终点步用J1而gold该步STEP为P. chlororaphis，需额外确认，但pathway_complete含1829，故中上而非高档满分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_037：gold含Bacillus sp. OxB-1 pathway_complete、R. rhodochrous 1829 pathway_complete及S03 nitrile hydratase的R. rhodochrous；不直接核验J1在终点烟酰胺酶步的菌株级能力。

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> R. rhodochrous J1的F10不运动、F12革兰氏阳性、F13不产芽孢与gold observed一致；F1/F6/F11等主要依赖INTERNAL_KNOWLEDGE_ONLY，Bacillus OxB-1的F8/F9无gold性状记录。大量null属诚实未知，D1已计完成度；D4按已给性状的准确性与适用性取7分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_037：gold observed支持R. rhodochrous 1829 F10 motility=false、F12 gram positive=true、F13 sporulation=false；Bacillus OxB-1多数性状为UNKNOWN，不能核验答案F8/F9。

</details>

### D5 来源与可核查性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 关键步骤提供PubMed/文献定位与claim_scope映射，来源不是纯库名；但S1反应为MODEL_INFERENCE、若干菌性状为INTERNAL_KNOWLEDGE_ONLY，且E0为CASE_EVIDENCE_GAP无法核验条目内容。无已核实错引，不cap；按可定位核心引用与部分缺口取7分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案实际交付的evidence_registry、source_type、locator与claim_scope；E0为空，不能据此核实文献内容。

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案清楚区分LITERATURE_DIRECT、MODEL_INFERENCE、INTERNAL_KNOWLEDGE_ONLY与unknown；uncertainties列出醛肟脱水酶外推、EC历史差异、非同一菌全路、腈水解酶分支排除、null原因。主要限制与待验证点披露充分，置信标签总体与证据相称。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案的不确定性说明、source_type与confidence标签；不证明科学内容本身正确。

</details>

## GPT5.6

答案SHA256：`6732d7284791c37cd3b43377c9ea084ced9c7d30d95cb887fb4a140b6fb9bb74`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步主链、每步酶与微生物、路线名与终点均有交付；但两个profile的15项性状全部为null/unknown，仅占位，且来源全为内部知识。完成度落在5–6档，因性状与来源缺口取5。

### D2 反应化学科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步化学转化与gold主链方向/终点一致：醛肟脱水、腈水合、酰胺水解；未列H2O/NH3等辅因子属局部计量缺陷，按P103不cap，取7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：给出S02、S03、S01的定向主底物/主产物与顺序；不证明答案所用具体酶或菌株。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_037：题面终点为Nicotinate；答案Nicotinic acid为其质子化形式，不额外证明性状或菌株能力。

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 本题目标主链为三步：金标S02醛肟脱水（accepted aldoxime dehydratase，EC通配4.2.1）、金标S03腈水合（accepted nitrile hydratase EC 4.2.1.84）、金标S01烟酰胺水解（accepted nicotinamidase EC 3.5.1.19）。答案S2的Nitrile hydratase EC 4.2.1.84与accepted集合精确一致，可支持；答案S1的Aldoxime dehydratase名称与目标醛肟脱水一致，但所给具体EC 4.2.1.135相对金标通配EC 4.2.1及E0缺口仍属精确EC配对未核，按C02只记名称支持与EC待核；答案S3的Amidase EC 3.5.1.4对应目标烟酰胺水解反应类型，但不在本题accepted nicotinamidase集合内，不能判为已确认错误，只登记支持缺口。终末KEY步酶支持尚未确认，不能进入7–8档；但已支持部分可逐反应定位、待核边界明确，故在&#91;5,6&#93;内取6，不机械取上限，也不把未核amidase直接判错触发D-KEY4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_037：给出金标三步目标酶：S01 nicotinamidase EC 3.5.1.19；S02 aldoxime dehydratase EC 4.2.1；S03 nitrile hydratase EC 4.2.1.84；不证明答案任何具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_037：给出金标目标反应与方向：S02醛肟脱水到3-cyanopyridine，S03腈水合到nicotinamide，S01烟酰胺水解到nicotinate；支持目标反应层面，不扩展到未声称的蛋白底物谱。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_037：该案为LINEAR_UNIQUE、ordered_step_count=3，支持本题按三步主链核对目标酶；不证明答案酶活性。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Bacillus sp. OxB-1与Rhodococcus rhodochrous在gold path_complete中存在，物种/菌株主干合理；但Bacillus不在S02步骤级菌列表，Rhodococcus J1的strain与S02/S03步骤级归属无冻结证据，且TaxID均null。部分支持，取5档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_037：path_complete行支持Bacillus sp. OxB-1与Rhodococcus rhodochrous 1829的路径级身份；不证明strain J1或其在S02/S03的步骤级归属。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 两个organism_profiles的F1–F15全部value=null、confidence=unknown；按P44/R2，全部必需性状均为null/空值时D4=MISSING=1，不宣称检测到科学错误；D1已反映完成度不足。

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案evidence_registry的EVID_001–005全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；关键结论不可定位到具体文献/数据库条目，属MISSING_SOURCE低档。未发现已核实错引，不cap；因逐声称有内部registry，档内取2。

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确标注低置信、氧条件未指定、连续降解链缺直接证据、后续步骤按常见反应推定，traits全部unknown；未把内部知识写成实验观测，限制披露具体，取8档。
