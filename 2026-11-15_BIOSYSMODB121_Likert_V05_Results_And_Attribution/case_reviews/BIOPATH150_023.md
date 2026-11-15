# BIOPATH150_023：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-hydroxyphenylacetate degradation

污染物：4-Hydroxyphenylacetate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | — | UNSCORED | LEGACY_A_NATIVE121 |
| DeepSeek | 58.5 | COMPARABLE | LEGACY_A_NATIVE121 |
| Kimi | 56.5 | COMPARABLE | LEGACY_A_NATIVE121 |
| Qwen | 35 | COMPARABLE | LEGACY_A_NATIVE121 |
| Grok | 63.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 34.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

原答案正文不可用/为空；保留位置，不填0、不造分。

## DeepSeek

答案SHA256：`0d5f14d218635df9566ac1f219339ce0110d911379984fb366e314c75b84ed6b`。

复审/来源说明：接入原有023题参考材料；只评价现成正文，没有补采答案。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案提交完整可解析JSON：route_scope.chosen_route_name原样填题面路线&quot;4-hydroxyphenylacetate degradation&quot;、氧气null如实；8个step均给出主底物/产物英文名+SMILES、酶(含EC，S6/S7 EC null如实)、对应微生物；单一organism_profile去重并含全15项性状；含route_summary与central_metabolism_entry。缺陷仅在局部字段(S2产物名-结构存疑、部分EC/性状null)，不影响模块覆盖与格式符合度，按TABLE0 D1良好档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_023：Gold为LINEAR_UNIQUE、ordered_step_count=8、route_name=4-hydroxyphenylacetate degradation，提供步数与路线名对齐基准
- QUESTION_TEXT / BIOPATH150_023：题面要求主链每步主底物/产物+SMILES+酶+EC+菌、15性状、路线名原样
- ANSWER_TEXT / steps+organism_profiles：8步与15性状齐备、路线名逐字一致

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 起点(4-HPA→3,4-DHPA)、S2间位开环(双加氧酶)、S3脱氢、终点(琥珀酸半醛→琥珀酸)化学正确且方向为降解正向。但S4以&quot;5-羧甲基-2-羟基粘康酸delta-异构酶(EC 5.3.3.10)&quot;把C8底物转成C7产物&quot;2-羟基庚-2,4-二烯-1,7-二酸&quot;(SMILES计8→7碳)，缺脱羧(CO2)步骤、碳数不守恒；答案S4 uncertainty亦自承&quot;可能为脱羧而非异构化&quot;。主链成立但关键转化需实质修订，归TABLE0 D2部分可用档取6；本题未新增高档KEY，D2科学证据门最高8不触发，但该步缺陷足以阻止7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：Gold S07(C8三羧酸)→S04(EC 4.1.1.68脱羧,产物列CO2)→C7 (4Z)-2-oxohept-4-enedioate，证明C8→C7需独立脱羧步骤
- ANSWER_TEXT / S4：答案S4底物为C8(OC(=O)C(O)=CC=C(CC(=O)O)C(=O)O)而产物为C7(OC(=O)C(O)=CC=CCC(=O)O)，酶标EC 5.3.3.10异构酶，未脱羧

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 酶谱系大体可靠：S2 EC 1.13.11.15精确、S8 EC 1.2.1.16在Gold集合内、S1 EC 1.14.13.3为4-HPA 3-单加氧酶(HpaBC)合法功能、S4 EC 5.3.3.10与S5 EC 5.3.3.11均为真实Hpa异构酶、S6水合酶/S7醛缩酶EC null为如实未知。扣分点：S3用EC 1.2.1.85而Gold为1.2.1.60(名-号配对存疑)；S4所配异构酶与其C8→C7产物声称不相容(功能-产物对应问题)。按C03/C04 S+F+M+U合成，已支持部分清楚、待修明确，落&#91;5,6&#93;带取6；无已确认KEY失败，D-KEY4不触发，科学证据门上界8未达。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_023：Gold S05=EC1.13.11.15、S03=EC1.2.1.60、S07=EC5.3.3.10、S02集合含EC1.2.1.16，用于逐条对号
- ANSWER_TEXT / S3,S4：S3 EC1.2.1.85与Gold 1.2.1.60不符；S4异构酶与C8→C7产物声称不符

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全程用Escherichia coli W(TaxID 562)。organism_gold PATHWAY_COMPLETE列TaxID 562为pathway_complete=TRUE，且Hpa操纵子为E. coli W经典HPA通路，整路能力成立、菌选择科学正确。不足：TaxID 562为物种级，strain&quot;W&quot;的菌株级身份无独立菌株级TaxID/基因组记录支持，属身份阶梯①粒度不足→档内扣、不cap(能力结论未被推翻)。按TABLE0 D3b与P106–110取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_023：PATHWAY_COMPLETE 行 TaxID 562 pathway_complete=TRUE，支持E. coli完成整条HPA通路

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已填性状多数正确/合理：F1 facultative anaerobe、F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating、F2 mesophile 均与trait_gold(562)观测一致；F7碳源、F8 HPA降解对E. coli W合理。但F3/F4/F9/F14整体null(Gold有观测)，F5&quot;ATCC 9637&quot;、F8、F15未经冻结材料核验，F2缺min/max，且各项&quot;最强来源&quot;实为INTERNAL_KNOWLEDGE_ONLY、raw_text全null。属部分性状准确但关键项证据不足、条件/数值需修订，按TABLE0 D4取6；缺失主归D1不重复重扣。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_023：TaxID 562观测：F1 aerotolerant/facultative、F10 motility=true、F11 rod、F12 gram negative=true、F13 sporulation=false，用于核对已填性状
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_023：F3/F4/F9/F14 可评分且Gold有观测，答案却整体null，提示关键项证据/数值不足

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry仅两条source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全部null，route/enzyme/microorganism/trait所有关键结论无任何可定位可核对条目，D5按claim group统一落MISSING_SOURCE低分档(P34)。因是缺失而非已核实错引，不构成关键错误、不cap。答案仅给claim_scope分组、未给可定位来源，未达&quot;笼统库名&quot;以上关联，故在低分档取3(非最低1-2，因结构/范围声明尚存)。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：两条EVID均为INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator，无法定位任何真实来源

</details>

### D6 不确定性与诚实度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案对部分步骤给出具体不确定性(S4&quot;EC/反应类型可能为脱羧而非异构化&quot;、S6/S7&quot;EC未知&quot;、未知字段置null)，并把证据诚实标为INTERNAL_KNOWLEDGE_ONLY，非系统性误导。但多数step的enzyme/microorganism仍标confidence=high，与内部知识级证据强度不相称；uncertainties数组留空、未列路线变体(S4脱羧缺失)等主要不确定点。属部分结论强度超过依据、披露过于笼统，按TABLE0 D6与P119取5，不构成cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps.confidence+uncertainties：多步标high但来源仅内部知识；uncertainties为空；仅S4-S7局部有具体不确定说明

</details>

## Kimi

答案SHA256：`1f1e9cacb4aa6ed614d5138c2a66dc17fa6ed71357623046ff2a994c7e47ff82`。

复审/来源说明：接入原有023题参考材料；只评价现成正文，没有补采答案。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案JSON结构完整，route_scope.chosen_route_name原样保留，8步、酶/菌、ORG_001与15项性状均有输出；但主链内容未完整对应题面023的指定gold主链：S5/S6段未交付gold S04-&gt;S08的必经物质流，S5产物为foreign，S6未提供gold S08所需底物。按D1任务符合度/主链交付判为已核内容偏离；因模块整体仍齐全、多数步骤存在，取受限范围上沿4，不把D2的碳守恒问题重复计为另一独立科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_023：要求给出指定4-hydroxyphenylacetate degradation主链，每步给底物/产物/酶/菌并填写15项性状
- ANSWER_TEXT / BIOPATH150_023：原答案提供8步及15项性状，但S5/S6主链内容与gold S04-&gt;S08不一致
- GOLD_SLICE / reaction_gold.tsv：023 gold指定S04 decarboxylation与S08 hydration的底物/产物身份及线性顺序
- GOLD_SLICE / formal_cases.tsv：023为8步LINEAR_UNIQUE，required n=8

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 前四步及S7/S8的化学骨架可读且大体对应gold，但S5产物与gold S04产物不一致，S6又以该中间体水合生成4-hydroxy-2-oxoheptanedioate，导致S04-&gt;S08的物质流连续性和碳骨架守恒出现关键缺口；属D2主链局部违反基本化学约束/连接失败。因并非整链全错且有可判可用部分，取关键错误上限内4。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_023：S5产物与S6底物/产物SMILES显示中间体不承接gold S04产物且S6碳骨架连续性可疑
- GOLD_SLICE / reaction_gold.tsv：S04要求生成(4Z)-2-oxohept-4-enedioate并释放CO2；S08要求该中间体水合为(S)-4-hydroxy-2-oxoheptanedioate
- GOLD_SLICE / formal_cases.tsv：023为LINEAR_UNIQUE 8步主链，S04-&gt;S08为连续主链段

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按8个必答目标反应看，S1-S4、S7、S8的酶/功能与enzyme_gold对应较清楚；S5虽给EC4.1.1.68但目标产物与gold S04不一致，S6 hpaH缺EC且未绑定gold S08底物/反应，计为可用目标6/8，落入C04的&#91;5,6&#93;。无D3a关键错误：未见EC大类矛盾、酶名与EC互斥、或把广谱家族相关性冒充具体催化证据，故不cap，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_023：各步酶名、EC、基因与原反应声称；S5/S6目标反应内容不足
- GOLD_SLICE / enzyme_gold.tsv：023各gold step的酶名、EC候选及反应对应
- GOLD_SLICE / reaction_gold.tsv：目标反应底物/产物身份用于判定S5/S6是否绑定目标反应

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所有步骤统一使用Escherichia coli，与organism_gold的step级E. coli记录及PATHWAY_COMPLETE中E. coli taxid 562完整路径记录方向一致；但答案将profile固定为MG1655/TaxID511145并声称complete_pathway，而冻结slice的完整路径记录是种级E. coli 562/GCA_003018455.1，未给511145菌株级完整路径证据。按身份粒度不足处理：记录真实且同lineage，档内扣、不cap，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_023：所有步骤使用E. coli MG1655/TaxID511145并声称完整路径
- GOLD_SLICE / organism_gold.tsv：step级E. coli记录及PATHWAY_COMPLETE taxid562/GCA_003018455.1；未给511145完整路径证据

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状均出现。F1兼性厌氧/耐氧、F2嗜温偏好、F11杆状、F12 Gram-negative、F13不产芽孢与trait_gold观测一致；F14 NC_000913.3与MG1655菌株身份相符，F5 ATCC700926为菌株级保藏号。主要不足是F2/F3/F4多个数值端点未填或来自内部知识，F10填null而gold有motility观测，F15在gold为UNKNOWN时给出内部推断；未见已核关键性状错误，按主要性状可核实、局部不足取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_023：15项性状原值、证据与置信度
- GOLD_SLICE / trait_gold.tsv：E. coli 562的F1/F2/F11/F12/F13等观测值及F15 UNKNOWN；F5物种代表记录DSM4599
- GOLD_SLICE / trait_scoreability_mask.tsv：F2/F3/F4子字段可评分状态，提示若干端点仅completeness/pending，不应臆造精确核验
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv：F2/F3/F4 min/max/optimum等子字段的评分门与待裁状态

</details>

### D5 来源与可核查性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案提供了EVID_001 MetaCyc pathway、EVID_002 NCBI genome、EVID_003 NCBI Taxonomy、EVID_004 ATCC、EVID_006 ExplorEnz等可定位记录，路线/反应、菌种身份与基因组有部分可核对链；但多个酶-EC仍主要依赖单一MetaCyc pathway且record_id为空，hpaH/hpaI未给EC，许多性状依赖INTERNAL_KNOWLEDGE_ONLY。无已核实错引，不作D5 cap；决策相关组部分可定位，按5-6取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_023：原答案登记的六条证据、claim_scope和置信度；显示性状多处仅INTERNAL_KNOWLEDGE_ONLY
- QUESTION_TEXT / BIOPATH150_023：要求每个事实至多引用一个最强证据并可追溯

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案用uncertainties列出氧条件null、S2-S6 SMILES立体/规范形式风险、hpaH/hpaI EC未把握、motility未强填；各步与性状有high/medium/low/unknown置信标注，并将多项性状证据标为INTERNAL_KNOWLEDGE_ONLY。主要不足是部分内部推断仍给medium/high且未提示S5/S6连续性风险；但未见系统性把预测写成实证或掩盖主要矛盾，按大部分未知/限制已披露取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_023：不确定性说明、置信度分层和内部知识来源标注
- QUESTION_TEXT / BIOPATH150_023：要求未知填null或unknown，并区分证据性质

</details>

## Qwen

答案SHA256：`cac30970793042e0a2f8f8e6357ce4c33e02f2dc9d4d34adb6926f0f822f3e49`。

复审/来源说明：接入原有023题参考材料；只评价现成正文，没有补采答案。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面指定4-hydroxyphenylacetate degradation并要求8步主链至succinate；答案仅给4步homogentisate分支，止于fumarate+acetoacetate，未覆盖Gold的3,4-dihydroxyphenylacetate开环主链及succinate终点。虽JSON和逐步字段可辨认，但核心任务路线被替换且必要步骤大部缺失，属D1任务符合度关键失败，限1–4档内取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_023：要求按题面指定route_scope并给出主链、每步酶/菌、15项性状
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：Gold主链8步：S01/S05/S03/S07/S04/S08/S06/S02；终点为succinate
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_023：ordered_step_count=8，LINEAR_UNIQUE

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2按实际所答化学独立评价。答案给出的homogentisate路线内部连贯：S1羟基化、S2双加氧开环、S3异构化、S4水解，方向为主底物到产物，无明显原子/方向反转。但这是相对题面Gold的化学可成立替代分支，且S1酶EC/辅因子不确定、S2-S4中间体SMILES缺失，按替代路线候选上限取6，不高于6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / S1-S4：homogentisate→maleylacetoacetate→fumarylacetoacetate→fumarate+acetoacetate的连续转化
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：题面指定Gold为3,4-dihydroxyphenylacetate开环主链至succinate；答案化学属替代分支

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 只按目标反应评价。Gold需8个目标反应；答案S1虽以4-HPA为底物但产物为homogentisate而非3,4-dihydroxyphenylacetate，属所答另一结构/转化；其S2-S4分别对应homogentisate开环、马来酰乙酰乙酸异构化、延胡索酰乙酰乙酸水解，均非Gold S05/S03/S07/S04/S08/S06/S02目标反应。无可核目标反应S，核心目标催化对应基本缺失，按C04低覆盖率&#91;1,2&#93;并在C05取1；不以错误路线内部酶自洽加分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_023：Gold各步目标酶：4-coumarate 3-monooxygenase、3,4-dihydroxyphenylacetate dioxygenase、5-carboxymethyl-2-hydroxymuconic semialdehyde dehydrogenase等
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：8个必答目标反应及主产物
- ANSWER_TEXT / steps S1-S4：答案给出homogentisate分支酶，而非目标3,4-dihydroxyphenylacetate分支酶

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案统一推荐Pseudomonas putida S-12，TaxID 303。Gold的PATHWAY_COMPLETE行含TaxID 303 Pseudomonas putida且pathway_complete=TRUE，故物种级身份与整路能力有基础支持，未构成跨属/无关类群错配。但答案把物种级TaxID 303用于菌株S-12的菌株级声称，且仅有INTERNAL_KNOWLEDGE_ONLY证据，属D3b身份粒度不足；按身份阶梯通常限7档附近，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_023：PATHWAY_COMPLETE含TaxID 303 Pseudomonas putida；step级Gold菌多为E. coli等，但不排除303物种级整路能力
- ANSWER_TEXT / ORG_001：答案声称Pseudomonas putida S-12，TaxID 303；证据EVID_001为internal knowledge only

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles&#91;0&#93;.traits的F1-F15全部value=null/unknown，未交付任何可评价性状值。按P44，全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ORG_001.traits：15项性状全部value null且confidence unknown

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry仅有EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id均为null，locator只是内部描述；反应、酶、菌均未绑定可定位外部条目或文献。按MISSING_SOURCE低分档且默认不cap，D5几无关键结论可追溯性，取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / EVID_001：唯一证据为internal knowledge only，无数据库记录/文献定位
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_023：Gold提供可定位酶/反应参照，用于对比答案未交付对应来源映射

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案列出氧条件未指定、S1酶EC/辅因子证据不足、菌株及15项性状缺乏可靠来源等不确定性，且性状多填unknown，具备部分披露。但所有步骤酶/菌仍标medium confidence，且把homogentisate替代分支表述为“按题面指定路线”，未明确披露该分支与Gold主链的边界差异，属部分结论强度超过依据；未达系统性把预测写成实证，故D6在5–6档取6，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：披露氧条件、S1酶EC/辅因子、菌株和性状来源不足
- ANSWER_TEXT / steps S1-S4.confidence：酶与菌confidence普遍medium但证据仅INTERNAL_KNOWLEDGE_ONLY
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：Gold主链为3,4-dihydroxyphenylacetate分支至succinate，答案未披露其替代分支边界

</details>

## Grok

答案SHA256：`f3a53a9e00274b90f3c7a2eca64c73932553ed3f1ecdc2713c58aaac66ea171a`。

复审/来源说明：原任务范围行漏登引用目录，离线回收；模型分数、理由和引用逐字未改，无新增调用。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> JSON完整，步骤、酶、菌与15项性状均有回应，route名称也原样填写；但主链止于pyruvate+succinate semialdehyde，未交付Gold终点Succinate所需的S02琥珀酸半醛脱氢步，且把题面未指定的氧条件自行填为aerobic，并多出S6异构步。属主要模块齐全但必要内容遗漏、任务范围处理需修订的5–6档。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION:氧条件: null：题面明确氧条件为null（未指定），不是aerobic
- ANSWER_TEXT / route_scope.oxygen_condition：答案自行填写aerobic，并解释为题面未指定但按途径推断
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：Gold有8个必答步，S02 r01495为4-Oxobutanoate→Succinate，答案没有对应主链step
- ANSWER_TEXT / steps.S8：主链终点为pyruvate与succinate semialdehyde，未到succinate
- SCOPE_ROW / BIOPATH150_023：n_required=8，gold_terminal_main_products=Succinate

</details>

### D2 反应化学科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 前段关键化学（3-羟化、间位开环、脱氢、异构、脱羧、水合、醛缩）大体与Gold一致，方向和步骤连接可读；但终点停在pyruvate/succinate semialdehyde，未到Succinate，且S5/S6以2-hydroxyhepta-2,4-diene-1,7-dioate及额外异构步表示，与Gold的(4Z)-2-oxohept-4-enedioate/EC4.2.1.163路径存在表示和中间体差异。主链成立，局部连接和终点需修订，7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：Gold主链8步；S04产物(4Z)-2-oxohept-4-enedioate，S02终点Succinate
- ANSWER_TEXT / steps.S8：S8产物为pyruvate+succinate semialdehyde，未继续到succinate
- ANSWER_TEXT / steps.S5-S6：S5生成2-hydroxyhepta-2,4-diene-1,7-dioate，S6额外异构为2-oxohept-3-ene-1,7-dioate
- SCOPE_ROW / BIOPATH150_023：gold_terminal_main_products=Succinate；n_required=8
- RUBRIC_CLAUSE / C06：仅缺步不另用覆盖率硬换D2分，按连续性/核心转化评价

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 多数目标酶EC与Gold对应：S1 1.14.14.9、S2 1.13.11.15、S3 1.2.1.60、S4 5.3.3.10、S5 4.1.1.68、S8 4.1.2.52；但主链缺S02琥珀酸半醛脱氢酶步（仅在downstream提及），S7用EC4.2.1.80而Gold S08为4.2.1.163，且S6为Gold未列异构步。主要对应可靠，但终点/个别EC需修订，7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_023：Gold酶EC：S01 1.14.14.9、S05 1.13.11.15、S03 1.2.1.60、S07 5.3.3.10、S04 4.1.1.68、S08 4.2.1.163、S06 4.1.2.52、S02 1.2.1.79
- ANSWER_TEXT / steps.S7.enzyme：答S7 hydratase EC4.2.1.80，与Gold S08 EC4.2.1.163不同
- ANSWER_TEXT / downstream_continuation&#91;0&#93;：S02反应/酶只出现在downstream_continuation，未作为主链step交付
- ANSWER_TEXT / steps.S6.enzyme：S6异构酶无EC，为Gold未列额外步
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：Gold S02为终步4-Oxobutanoate→Succinate

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全程用Escherichia coli W（TaxID 562），与Gold多数STEP为Escherichia coli及PATHWAY_COMPLETE 562 true一致；但菌株W只以物种级TaxID支撑，答案自己也注明W独立TaxID未核验，属物种级记录支持菌株级声称的粒度不足，按身份阶梯档内扣分，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_023：多数STEP organism=Escherichia coli 562；PATHWAY_COMPLETE 562 true
- ANSWER_TEXT / organism_profiles.ORG_001：organism_name E. coli，strain W，ncbi_taxid 562
- ANSWER_TEXT / uncertainties&#91;1&#93;：承认菌株W独立TaxID未核验
- RUBRIC_CLAUSE / P107：物种级支持菌株级属粒度不足，通常7档附近、默认不cap

</details>

### D4 性状科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项均返回，E. coli W主要性状（兼性厌氧、中温、非嗜盐、运动、杆状、革兰阴性、不产芽孢）与trait_gold观察/预测不冲突；F5 ATCC 9637为W菌株特异信息，Gold DSM 4599是物种级另一代表，不据此判错；F14全null、F2/F3/F4数值上下限缺，属缺失/待核而非已核错误。主要性状适用，仅少量数值与粒度需补，取8档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_023：E. coli 562 observed F1 aerotolerant、F2 mesophilic、F4 non-halophilic、F5 DSM4599、F10 motility true、F11 rod、F12 gram negative、F13 sporulation false
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_023：F3/F15 completeness_only；F2/F4部分子字段未观测或待裁
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_023：F2/F3/F4的min/opt/max多数字段not scoreable或pending_teacher_adjudication
- ANSWER_TEXT / organism_profiles.ORG_001.traits：答案15项traits值
- RUBRIC_CLAUSE / P113：温度观测不等于最适温度；同物种代表记录按规则使用

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry五条全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id为null，仅有描述性locator；路线、酶、菌、15性状的关键结论没有可定位的数据库条目、文献或计算记录可核对。按MISSING_SOURCE低分档；这是缺失而非已核错引，默认不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry.EVID_001-EVID_005：全部source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id为null
- ANSWER_TEXT / steps.*.reaction_evidence_id：步骤证据主要指向EVID_001/EVID_002等内部知识条目
- RUBRIC_CLAUSE / P34：INTERNAL_KNOWLEDGE_ONLY按MISSING_SOURCE低分，默认不触发cap
- RUBRIC_CLAUSE / P41：D5按claim group来源状态；全部缺失为低分档

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案主动列出氧条件未指定、TaxID为物种级、F14全null、gene符号未核验、S6无独立EC、S7烯醇/酮式互变、SMILES未标立体、下游氧化不计主链等限制，未知与内部知识有区分；但多条INTERNAL_KNOWLEDGE_ONLY仍标high confidence，置信表达不完全相称，属单点/局部过强而非系统性误导，8档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：列明氧条件、TaxID、F14、gene符号、EC、SMILES等未知/限制
- ANSWER_TEXT / route_scope.notes：说明题面未指定氧条件及为何填aerobic
- ANSWER_TEXT / evidence_registry.EVID_001/EVID_002：INTERNAL_KNOWLEDGE_ONLY标high，置信与证据强度不完全一致
- RUBRIC_CLAUSE / P119：单点过度确信档内扣；系统性误导才是cap候选
- RUBRIC_CLAUSE / P121：D5已核实错引不自动使D6 cap，D6按披露质量独立定档

</details>

## GPT5.6

答案SHA256：`032846a4d0f46e73384d555494488c42031e39d116a5df2131fc6c4974b19745`。

复审/来源说明：接入原有023题参考材料；只评价现成正文，没有补采答案。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 任务要求8步主链并逐题给出性状，原答仅交付S1-S2两步，6个必需步骤未交付；organism_profiles仅1条且15项性状全为null/unknown，核心任务模块大部缺失，符合D1关键错误与1-2档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_023：ordered_step_count=8，final_graph_status=LINEAR_UNIQUE
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：登记8个必需步骤S01-S08，末端主产物为Succinate
- ANSWER_TEXT / steps&#91;0&#93;-steps&#91;1&#93;：原答仅含S1、S2两步且无下游展开
- RUBRIC_CLAUSE / P98：D1关键错误包括核心任务模块大部缺失

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1芳香环3-羟化与S2邻位双加氧开环方向与Gold相应主链片段一致，但未列O2/FADH2等辅因子，S2产物SMILES缺失；且原答未展开S2之后的6步至末端Succinate，主链仅部分成立，关键中间体与连接缺失，按5-6档取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps&#91;0&#93;-steps&#91;1&#93;：S1羟化、S2开环；未列O2/FADH2；S2产物SMILES为null；无下游展开
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：S01反应含O2/FADH2，S05反应含O2；末端S02为Succinate
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏通常为局部计量缺陷，不自动cap

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 本题N=8。S2的目标反应与Gold S05一致且酶EC 1.13.11.15在enzyme_gold中命中，可记S；S1目标反应核心与Gold S01一致，但原答EC 1.14.13.18未在冻结Gold/E0中确认，且EVID_001仅为INTERNAL_KNOWLEDGE_ONLY，配对待核记U；其余6个必需步骤未交付记M。S/N=1/8=0.125，落入&#91;1,2&#93;；仅一个已确认目标，主目标酶对应整体失效，取2。无已核实EC类别矛盾或名号互斥，key_error=N。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps&#91;0&#93;.enzyme;steps&#91;1&#93;.enzyme：S1用EC 1.14.13.18，S2用EC 1.13.11.15；仅两步
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_023：S05酶为3,4-dihydroxyphenylacetate dioxygenase EC 1.13.11.15；S01 Gold候选为4-coumarate 3-monooxygenase EC 1.14.14.9；未见EC 1.14.13.18
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_023：S01与S05为目标反应；S02末端为Succinate；共8个必需步骤
- RUBRIC_CLAUSE / C04：D3a按S/F/M/U/H逐目标分类并以S/N选带

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1/S2所用Escherichia coli与organism_gold中两步的E. coli物种记录相符，且E. coli 562在Gold中有pathway_complete=TRUE；但原答具体菌株NCIB 9485未在冻结organism_gold/trait_gold中核实，complete_pathway_organism_profile_id=ORG_001又超出仅两步的交付与仅hpa基因簇的笼统文献声称。物种级支持不能自动证明菌株级身份和整路能力，按5-6档取5；无已核实跨类群/异菌株错配，key_error=N。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps&#91;0&#93;.microorganism;steps&#91;1&#93;.microorganism：两步均用E. coli NCIB 9485，并声明complete pathway organism为ORG_001
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_023：S01、S05的matched organism为Escherichia coli TaxID 562；pathway_complete行显示562 TRUE；未见NCIB 9485
- RUBRIC_CLAUSE / P69：身份定位、反应级能力、完整路径能力须分层核验

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles&#91;0&#93;的15项性状全部为null/unknown，未给出任何可评价的性状值；按P44/P112，全部必需性状为null/空值时D4记MISSING=1，不宣称检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：15项性状全部null/unknown，无任何raw_text或evidence_id
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_023：E. coli 562存在若干观测性状行，但原答未使用；不能把未填写的Gold值回填为答案证据
- RUBRIC_CLAUSE / P44：全部必需性状均为null/空值时D4按MISSING记1分

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> EVID_001为INTERNAL_KNOWLEDGE_ONLY且record_id=null，只给MetaCyc宽泛路径名；EVID_002为LITERATURE_DIRECT但无数据库、无record_id、无DOI/具体文献定位。核心路线/反应/酶和菌株声称均无条目级可定位可核对证据，只有笼统库名或内部声明；按MISSING_SOURCE/GENERIC_SOURCE合成落3-4档，取3。无已核实虚构或错引，key_error=N。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry&#91;0&#93;;evidence_registry&#91;1&#93;：EVID_001=INTERNAL_KNOWLEDGE_ONLY、MetaCyc、record_id null；EVID_002=LITERATURE_DIRECT、database/record_id null、locator为笼统报道
- RUBRIC_CLAUSE / P34：仅INTERNAL_KNOWLEDGE_ONLY归MISSING_SOURCE，低分档默认不cap
- RUBRIC_CLAUSE / P35：决策相关组全部仅有笼统来源可入3-4档；条目级证据才入5-6档
- RUBRIC_CLAUSE / P41：D5按claim group合成；SUPPORTING证据不能抵消核心组缺失

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 原答明确写出氧条件未指定、性状无原文均保留null、下游未展开，具备部分不确定性披露；但EVID_001仅内部知识仍标medium confidence，且仅两步却填complete_pathway_organism_profile_id=ORG_001，结论强度超过依据。属局部过度确信/披露不足而非系统性误导，按5-6档取6；D5来源问题不自动使D6 cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / route_scope.notes;uncertainties：披露氧条件未指定、性状null、下游未展开；同时enzyme confidence=medium且complete_pathway=ORG_001
- RUBRIC_CLAUSE / P119：单点过度确信通常5-6档，系统性误导才cap候选
- RUBRIC_CLAUSE / P121：D5已核实错引不自动使D6 cap，D6按披露质量独立定档

</details>
