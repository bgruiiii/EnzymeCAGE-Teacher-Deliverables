# BIOPATH150_006：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：1,2-Dichloroethane degradation pathway

污染物：1,2-Dichloroethane；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 70 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 67.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 76 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 58.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 66.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 50.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`8500deb408474189416ac78f7345d68a8d0ac65b8b48d2355b05fa7acb0641fa`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 题面要求的路线名与好氧条件已原样填写；S1–S4覆盖gold四步主链并给出底物/产物、酶、微生物，ORG_001含全部15项性状，主要交付模块齐全。扣分点：S2的EC为null，虽可按未知填写但与gold可接受EC相比仍是字段缺失；另把S5乙醇酸→乙醛酸作为主链步骤延续到gold终点Glycolate下游，属于少量范围外延伸而非核心模块缺失。故按7–8档取较充分上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

必答模块全部实质交付：5步主链每步给出主底物/主产物name+SMILES并绑定一个酶(含EC或诚实null)与一个菌；ORG_001一次性给出15项性状；route_scope.chosen_route_name原样填写；无重要遗漏或路线/条件偏离（好氧路线与题面一致）。未知EC、TaxID、基因组/保藏号按题面要求诚实置null未虚填。仅S5超出gold终点属可选下游延续，不加分不扣分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv：支持本题路线名与gold终点为Glycolate；不支持答案额外S5应计入必答主链
- GOLD_SLICE / formal_cases.tsv：支持gold为4步线性唯一主链；不自动把额外下游步骤判为科学错误
- GOLD_SLICE / enzyme_gold.tsv：支持S02存在可接受酶/EC记录，可用于核对答案S2的EC缺失；不单独评价D3a科学正确性
- GOLD_SLICE / PROTOCOL_DISCLOSURE_BIOPATH150_006.md：披露本题按冻结4步严格口径评分且路线唯一定位未建立；不构成免责条款
- RUBRIC_CLAUSE / P29：额外下游延续不加分、未延续下游不扣分；用于限制对S5的D1处理

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 前四步有机转化与gold主链一致：S1水解脱卤生成2-氯乙醇，S2醇氧化生成2-氯乙醛，S3醛氧化生成2-氯乙酸，S4水解脱卤生成乙醇酸；方向、主链连接和关键化学转化成立。S5乙醇酸氧化为乙醛酸在化学上可成立，但位于gold终点Glycolate下游，按P29作为额外下游处理；S2未列明电子受体/辅因子属局部计量缺陷，按P103在7–8档内处理，不构成cap。S3/S4的质子化/电荷写法差异按表示差异处理，不据此判化学错误。

<details><summary>V0.4理由与本行变化背景</summary>

四个gold主步的化学转化被完整复现且方向正确：S1水解脱卤(DCE+H2O→2-氯乙醇+Cl-+H+)、S2醇氧化(→2-氯乙醛)、S3醛氧化(NAD+，→2-氯乙酸+NADH+H+)、S4水解脱卤(→乙醇酸+Cl-+H+)；主链化合物与gold S01–S04一致，辅因子(水/NAD+/O2)在列、氧化还原与原子计量成立。S5(乙醇酸→乙醛酸,H2O2)化学正确但位于gold终点之外，属额外下游延续，不加分亦不扣分。无明显跳步、反向或守恒问题。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：支持gold S01–S04的底物/产物配对及线性连接；不证明答案S5属于必答终点内步骤
- GOLD_SLICE / case_root_identity.tsv：支持gold终点为Glycolate；用于定位S5为下游延伸
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏通常为局部计量缺陷，D2在7–8档内处理，不自动cap
- RUBRIC_CLAUSE / P29：额外下游延续不加分、未延续下游不扣分；用于处理S5

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 按严格四步目标链（S01-S04）核验：各步主底物/主产物化学反应与reaction_gold基本对应，S04的haloacetate dehalogenase/EC 3.8.1.3与accepted EC精确匹配，可判为已支持。S01为KEY入口，酶名haloalkane dehalogenase对应accepted名称，但显式EC写成3.8.1.1而accepted为3.8.1.5，EC配对未获支持；S02仅有PQQ依赖醇脱氢酶描述且无EC，未对应accepted methanol dehydrogenase/EC 1.1.2.7；S03写成EC 1.2.1.3而accepted为EC 1.2.1.4，配对未获支持。故只有少数目标有精确accepted支持，另有关键入口的EC错配与两个主要步骤未核，不能进入良好档；但化学主链和S04精确支持使可用部分明确，故在低带取上沿4。S05为超出严格四步终点的下游延伸，不纳入本题D3a目标计数。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶功能与反应类型正确：S1卤烷脱卤酶(水解脱卤)、S2 PQQ依赖醌蛋白醇脱氢酶(与gold EC 1.1.2.7甲醇脱氢酶同属PQQ醌蛋白且答案以细胞色素类为电子受体，与gold S02 ferro/ferricytochrome c一致)、S3 NAD+醛脱氢酶、S4卤乙酸脱卤酶EC 3.8.1.3(与gold一致)、S5乙醇酸氧化酶EC 1.1.3.15(并披露乙醇酸脱氢酶替代)。具体EC号与gold存在差异：S1 3.8.1.1 vs gold 3.8.1.5、S3 1.2.1.3 vs gold 1.2.1.4，属四.5版本/多注差异，因E0 EVIDENCE_GAP无法裁决→不判错、不cap、档内扣分。整体主要步骤酶对应有可靠支持，仅少量条目待核。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_006：支持S04的EC 3.8.1.3精确匹配；显示S01、S03的EC与accepted不一致，S02 accepted为methanol dehydrogenase/EC 1.1.2.7而答案未给出该配对
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：支持S01-S04主底物/主产物与gold反应化学基本对应；不证明答案所给酶名与EC配对均已核
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_006：界定严格四步目标范围至Glycolate；答案S5乙醛酸延伸不属本题四个必答目标步
- RUBRIC_CLAUSE / C02：显式EC配对未核不得判S；accepted名称/EC不匹配只记支持成分，不能由家族相似替代
- RUBRIC_CLAUSE / C05：少数目标精确可用、关键入口EC错配且主要步骤未核时，不能进入7-8；可用边界清楚时低带上沿可用4

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> Xanthobacter autotrophicus在S1-S4均为gold exact物种；GJ10菌株与完整路径能力在冻结gold的PATHWAY_COMPLETE行中有记录；TaxID/genome为null属诚实缺失，少量菌株级编号未核，定7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

核心菌株Xanthobacter autotrophicus GJ10是该污染物经典降解菌，与gold物种级记录(EXACT, taxid 280, genome GCA_005871085.1, pathway_complete=TRUE)一致；五步均归属该菌，未用另一菌株号冒用，未把仅单步支持写成异菌全路径能力；alternative_branches中以is_part_of_scored_main_route=false正确排除Ancylobacter/Pseudomonas等同源执行者。ncbi_taxid诚实置null。仅菌株GJ10的菌株级编号/基因组未在E0核验(物种级一致，按P107粒度不足档内处理)。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_006：S1-S4 Xanthobacter autotrophicus为EXACT；S4另有Moraxella可接受；不支持菌株GJ10的TaxID编号。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：存在Xanthobacter autotrophicus GJ10的PATHWAY_COMPLETE记录但无TaxID；支持完整路径能力声称，不支持菌株级TaxID/基因组编号。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 15项性状均提交；F2最适约30°C、F11杆状、F12革兰氏阴性、F13不产芽孢等与同物种代表记录一致；F4/F5/F14保留null属诚实缺失但遗漏可用代表记录，F1/F10/F15有低置信叙述，定7档。

<details><summary>V0.4理由与本行变化背景</summary>

给定性状多数与gold物种级观测一致：F12革兰氏阴性(gram positive=false)√、F11杆状(cell shape=rod-shaped)√、F13不产孢(sporulation=false)√、F6好氧呼吸/O2(与respiration:nitrate=false一致)√、F9 DhlA/DhlB√。存在的条件/数值问题：F2将“常规培养约30℃”记为optimum_c=30(培养温度≠最适,P113)；F10“具鞭毛可运动”在gold为No robust majority时略偏确信(已标low)；F1“专性好氧”较gold aerotolerant=true略强。F4/F5/F14诚实null属完成度问题(P112)不重复计入D4。属主要性状可核实、少量条件/数值问题档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：Xanthobacter autotrophicus物种代表记录支持F2约30°C、F11杆状、F12革兰氏阴性、F13不产芽孢等；不支持把种级记录回填为菌株级已核来源。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_006：显示F2 minimum/maximum等子字段待教师裁定；F4/F5/F14有可评代表记录而答案未填。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案有结构化evidence_registry，S1/物种身份/部分路径声称有较精确Janssen 1985定位；但S2/S3/S5仅INTERNAL_KNOWLEDGE_ONLY，S4定位笼统，且E0整题GAP无法核验引用内容。部分决策相关组可定位、其他仍需映射，定5-6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组呈混合：路线/S1/核心菌株身份/F7有具体文献条目(EVID_001/002,Janssen 1985 AEM 49:673-677)属条目级可定位，但E0 EVIDENCE_GAP无法核对实际支持→UNRESOLVED_SOURCE；S2/S3/S5关键酶-反应与全部性状仅INTERNAL_KNOWLEDGE_ONLY(EVID_003/004/006/007/008，部分locator为null)→MISSING_SOURCE。无经核实错引，不触发cap。按P41决策相关组“部分关键结论可定位、其他模块缺映射”取5–6档低端=5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_EVIDENCE_REGISTRY：显示各EVID的source_type、locator与claim_scope；INTERNAL_KNOWLEDGE_ONLY不等于已核外部来源。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_006：仅确认本题为冻结四步案例；不支持核验答案引用内容。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案系统列出S2无公认EC、S3 EC指派、S5乙醇酸氧化酶替代、TaxID/基因组/保藏未知及低置信温度/pH；未知与内部记忆多处以low/unknown标注。少量S1高置信和完整路径表述偏强，但未掩盖主要限制，定7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

逐字段给出high/medium/low/unknown置信；uncertainties具体列出S2无公认EC、S3按一般性指派EC 1.2.1.3、S5可能为乙醇酸脱氢酶(副产物是否为H2O2不确定)、TaxID/基因组/保藏号未能核实故置null、F2/F3为低置信记忆值。诚实区分未知与推断，无系统性把预测/推断写成实证观测，未掩盖主要限制。个别性状(F1“专性好氧”、F10“具鞭毛”)以medium/low表述略偏确信但非系统性误导，属档内考虑。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_UNCERTAINTIES：显示对S2/S3/S5、TaxID、基因组、保藏及温度/pH的具体不确定性披露；不支持外部引用内容为真。

</details>

## DeepSeek

答案SHA256：`a5ba518c5604a8cb178e3ecbaab153c6ea49404b172ef7bec50817c5c22482a0`。

### D1 完整性与任务符合度：10 / SCORED

V0.4旧分8 → V0.5新分10，变化+2。

新裁判理由：

> 题面要求的四步主链、逐步底物/产物、每步首选酶及EC、对应微生物、15项性状和证据登记均已实质交付；路线名、好氧条件原样回显，未见重要模块遗漏或任务范围偏离。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的路径、每步酶+EC、每步对应微生物、15项性状、来源登记与不确定性均有交付；route_scope.chosen_route_name与题面给定路线名逐字一致；4步主链覆盖到题面终点。缺口为部分性状诚实null（5/15）、性状无raw_text、来源全为内部知识，属少量遗漏/工程性缺陷，落7–8档取8；不因篇幅加高。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求四步主链、每步主底物/主产物、一个首选酶及EC、一个对应微生物、15项性状及来源。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S4&#93;; ANSWER.organism_profiles&#91;ORG_001&#93;：答案实际交付四步、同一去重菌株profile、15项性状字段及证据登记；不证明其科学内容正确。
- GOLD_SLICE / formal_cases.tsv：gold记录本题为4步线性唯一主链；该行只用于确认必答步数为4，不证明答案内容正确。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链有机转化与方向正确：DCE→2-氯乙醇→氯乙醛→氯乙酸→乙醇酸，终点为gold的Glycolate；SMILES与步骤连接一致。氧化步骤未列NAD+/NADH或细胞色素等辅因子，脱卤步骤未列H2O/H+，属局部计量/表达简化，按辅因子条款不cap，留在7–8档上沿。

<details><summary>V0.4理由与本行变化背景</summary>

主链四步 DCE→2-氯乙醇→氯乙醛→氯乙酸→乙醇酸 与gold四步主链化学一致，方向forward，四个主产物SMILES与gold一致（ClCCCl/OCCCl/ClCC=O/ClCC(=O)&#91;O-&#93;/OCC(=O)&#91;O-&#93;），终点Glycolate合规。仅省略H2O、H+、NAD+/NADH等辅因子与currency，属局部计量缺陷，按八.辅因子条款在7–8档处理、不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：支持gold主链S01–S04的定向底物→产物、终点Glycolate及主要中间体；不证明答案所填每个酶/EC与gold一致。
- GOLD_SLICE / case_root_identity.tsv：支持题面污染物为1,2-Dichloroethane、终点为Glycolate、好氧。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S4&#93;：答案给出的四步化学转化和SMILES；其中未列辅因子/水/H+，该缺失用于D2局部表达评价。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 四步主底物/主产物与gold目标反应骨架严格MATCH（S1-S4对齐，终点Glycolate），不是漏交付或路线失败。S1的DhlA/EC 3.8.1.5与accepted EC 3.8.1.5一致，可作部分主干酶功能支持；但S2-S4分别给1.1.1.1、1.2.1.3、3.8.1.2，而accepted为1.1.2.7、1.2.1.4、3.8.1.3，均为非accepted通用酶/EC且冻结证据GAP，只能记MAJOR/KEY级U，不能确认也不能改判F。按C04，U不自动转NE，JUDGE_REQUIRED按现有材料判；按C05，当前仅有部分主干支持，三个主要酶对应仍待核，足以阻断7-8档，故取5。

<details><summary>V0.4理由与本行变化背景</summary>

S1 haloalkane dehalogenase DhlA EC 3.8.1.5 与gold S01 EC完全一致（关键去卤步有可靠支持）；S4 命名DhlB(haloacid dehalogenase)，EC 3.8.1.2与gold 3.8.1.3不同，二者同属2-haloacid dehalogenase，E0无官方reaction可核→UNRESOLVED，不cap。S2/S3 用通用ADH(1.1.1.1)/ALDH(1.2.1.3)，酶名、EC类别与“醇/醛氧化”反应类型自洽，但为广谱通用号而非pathway具体酶，答案已标medium并声明未确定。主要去卤步骤可靠、两个氧化步骤缺具体核验，落7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / a5ba518c5604a8cb178e3ecbaab153c6ea49404b172ef7bec50817c5c22482a0：仅用于定位答案S1-S4交付的步骤、酶名与EC；不作为其正确性支持证据。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_006：gold S01-S04酶名/EC对照：S01=3.8.1.5、S02=1.1.2.7、S03=1.2.1.4、S04=3.8.1.3；只支持数据库策展粒度的酶-反应对应，不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：支持四步主底物/主产物方向与终点Glycolate，用于确认目标反应骨架；不用于确认答案所给酶的身份正确。
- GOLD_SLICE / PROTOCOL_DISCLOSURE_BIOPATH150_006.md#case:BIOPATH150_006：题面路线名唯一定位不足的风险披露；仅作任务边界背景，不构成免扣条款或错误证明。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 微生物身份主结论为Xanthobacter autotrophicus GJ10；gold的STEP行在S01–S04均支持Xanthobacter autotrophicus，trait_gold的PATHWAY_COMPLETE行支持GJ10整条路径能力，S04亦有Xanthobacter分支。扣分点是：STEP身份证据主要是物种级，答案未给TaxID，GJ10的逐步酶归属未获菌株级逐条记录；按身份粒度不足处理，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

四步均用Xanthobacter autotrophicus GJ10。gold S01/S02/S03 归属X. autotrophicus(EXACT, taxid 280)，S04同时列Moraxella sp. B与X. autotrophicus(EXACT)，故全步用X. autotrophicus合法、非身份错配；gold PATHWAY_COMPLETE 含 taxid 280 pathway_complete=TRUE 及 X. autotrophicus GJ10 pathway_complete=TRUE，整条路径能力有支持。缺口：GJ10 菌株级taxid=null、菌株特异性能力记录未核验（E0缺口），属少量需确认，落8档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：支持S01–S04的Xanthobacter autotrophicus物种级归属；S01另列未解析Sphingobium，S04另列Moraxella；未给GJ10菌株级TaxID。
- GOLD_SLICE / trait_gold.tsv：PATHWAY_COMPLETE行含Xanthobacter autotrophicus GJ10且pathway_complete=TRUE，支持整条路径能力声称；该行多数性状仍为UNKNOWN，不证明所有菌株级性状。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;：答案声称物种Xanthobacter autotrophicus、菌株GJ10、TaxID null，并作为全路径菌引用；用于评价身份粒度，不构成其自身证据。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 已给性状中F11杆状、F12 Gram-negative、F13 non-spore-forming有同物种代表记录支持；F8降解1,2-二氯乙烷及其中间体、F9 DhlA/DhlB活性与GJ10全路径/酶记录方向一致。F5 DSMZ 3875、F6好氧呼吸/氧受体、F7 DCE/甲醇碳源、F15栖息地等属菌株级或未被同物种记录直接覆盖，保留未核；F2/F3/F4/F10/F14诚实填null，不判编造。主要已给性状未被推翻，但若干关键项仍缺菌株级证据，故7档。

<details><summary>V0.4理由与本行变化背景</summary>

已给10项中，身份类可核项正确：F11 rod-shaped、F12 Gram-negative 与gold观测一致，F13 非产孢与预测一致，F8/F9 与路径能力/酶一致，F1 aerobic 与gold aerotolerant 大致相符。F5 DSMZ 3875 与gold物种代表记录 DSM 117702 不同，但按四.4同物种代表记录+E0缺口→UNRESOLVED，不判错；F6/F7/F15 无粒度匹配证据。温度/pH/盐度/基因组均诚实null（主归D1）。属“部分性状准确适用、关键项证据不足”，落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：同物种代表记录支持F11 cell shape=rod-shaped、F12 gram positive=false、F13 sporulation=false；F5 280记录为DSM 117702，非同菌株直接对照；GJ10行多数性状UNKNOWN。
- GOLD_SLICE / trait_scoreability_mask.tsv：标明F2/F3/F4等子字段的可评分/仅完整度状态及F2 range子字段待裁定；不把未核当作错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv：F4 salinity的min/max有可评分标量；F2 min/max待老师冻结range政策；未核子字段不得猜值。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：答案实际填写的10项性状与5项显式unknown；用于逐项对照，不构成其自身来源。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry的EVID_001–EVID_003全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；关键路线、酶-EC、菌株身份和性状结论都无法沿外部可定位条目核查。按D5六状态属MISSING_SOURCE，低分档；这是缺失来源而非已核实错引，默认不cap。

<details><summary>V0.4理由与本行变化背景</summary>

EVID_001/002/003 全部 source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 均为null，无任何可定位文献或数据库条目；按四.3 六状态，各claim组均为 MISSING_SOURCE。D5主要结论“结论来源可追溯”基本不成立，落1–2档取2；MISSING_SOURCE 为缺失非误导，默认不cap。E0 为 EVIDENCE_GAP，编号类声称一律保持UNRESOLVED。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：EVID_001–EVID_003均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator空；支持MISSING_SOURCE判定，不支持任何外部可定位来源或已核实错引。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案对ADH/ALDH具体酶/基因未定、部分性状未知有明确说明，并对多个性状填null；但所有证据均为INTERNAL_KNOWLEDGE_ONLY，却对DhlA/DhlB、菌株身份和若干性状使用high/medium confidence，未系统说明这些是内部知识/推断而非外部观测，也未披露路线名唯一定位风险。属不确定性说明存在但部分结论强度超过依据，6档。

<details><summary>V0.4理由与本行变化背景</summary>

答案提供 uncertainties（S2/S3通用EC未定、部分性状未知）并诚实把未知项填null，具基本不确定性说明；但大量仅 INTERNAL_KNOWLEDGE_ONLY 的身份/性状（如F1/F9/F11/F12/F13）以 confidence=high 呈现，未区分观测/预测/推断，未说明编号与性状不可外部核验，部分结论强度超过依据。属“有说明但笼统、部分过强”，5–6档取6；错误集中于同一证据类型，非系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; ANSWER.evidence_registry; confidence fields：显示答案已列两条不确定性并多处填unknown，但所有证据类型为INTERNAL_KNOWLEDGE_ONLY且部分high/medium置信无外部来源；用于D6披露强度评价，不证明科学错误。

</details>

## Kimi

答案SHA256：`7f623bccd031b38dd4f544afa3974bc8b8e2b5fd8ad4d96aa46c7eb2e36e9276`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 题面要求的路径、逐步底物/产物英文名与SMILES、首选酶/EC、对应微生物以及15项性状均有输出；route_scope正确回填指定路线名与aerobic条件，JSON可解析，同一菌也已用单一organism_profile去重。S1-S4覆盖冻结gold四步主链，S5为glycolate之后的额外下游氧化；按P29只作额外下游，不加分，也不因额外延续本身扣D1。部分性状填null/低置信，但题面明确允许不确定项为null，故不构成D1核心模块遗漏或已核路线偏离；未发现应触发D1关键错误的任务缺失。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖路径、逐步酶/EC、微生物、15项性状与来源登记；chosen_route_name逐字回显题面路线名；同一菌株只保留一个profile并由各步引用；未知TaxID与F4/F14明确null。少量完成度/来源强度问题（两个性状null、多个性状仅internal knowledge）不足以明显降低本维。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.route_scope：回填题面路线名与aerobic氧条件，未改选路线。
- ANSWER_TEXT / ANSWER.steps.S1-S5：五步均给出主底物/主产物、酶/EC和微生物引用；S1-S4覆盖gold主链，S5为额外下游步骤。
- ANSWER_TEXT / ANSWER.organism_profiles.ORG_001.traits：15项性状键均出现，部分填值、部分按题面允许填null；同一物种+菌株仅一个profile。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_006：冻结gold为4步LINEAR_UNIQUE、aerobic、HALOGENATED_COMPOUND主链；用于核对D1主链范围，不把全图旁支当必答分母。
- GOLD_SLICE / PROTOCOL_DISCLOSURE_BIOPATH150_006.md#case:BIOPATH150_006：实际题面只给路线名，未给pathway ID、终点、步数等唯一定位信息；维持4步严格口径并披露定位不足风险，不是免扣条款。
- SCOPE_ROW / SCOPE#BIOPATH150_006#CG04：题面明确氧条件为aerobic；答案route_scope回填一致。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：本题15项性状gold行存在且多项为UNKNOWN，支持null/未知属允许登记，不能仅据D1填空率判科学错误。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> S1-S4主链化学与gold四步一致：1,2-二氯乙烷水解脱卤生成2-氯乙醇，随后醇氧化为氯乙醛、醛氧化为氯乙酸、再脱卤生成glycolate；方向正确、步骤连接连续，SMILES和反应类型清楚。S5 glycolate→glyoxylate位于gold终点Glycolate之后，按P29属额外下游延续，不用于抬高D2。局部问题主要是S2/S3/S5未列出氧化还原辅因子，以及HCl/氯离子表示简化；按P103-P104属局部计量或表达缺陷，不改变主链核心化学结论。酶名/EC与gold的差异留D3a按酶对应维度处理，不在D2重复扣分。

<details><summary>V0.4理由与本行变化背景</summary>

S1-S4主链化学与gold一致：DCE经DhlA水解至2-氯乙醇，再氧化至氯乙醛、氯乙酸，经DhlB脱卤至乙醇酸；方向、碳骨架与连接成立。S5乙醇酸→乙醛酸是合理下游延续，但答案将其列入主链且缺氧化还原辅因子；S2/S3/S5辅因子遗漏属局部计量缺陷，按四.5/八.辅因子条款在7-8档处理，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps.S1-S4：S1-S4给出连续转化方向与SMILES：1,2-DCE→2-氯乙醇→氯乙醛→氯乙酸→glycolate。
- ANSWER_TEXT / ANSWER.steps.S5：S5 glycolate→glyoxylate位于gold终点之后，属额外下游；不作为D2主链得分依据。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：gold四步主底物/主产物与SUBSTRATE_TO_PRODUCT方向，用于核对S1-S4主链化学与连续性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_006：gold起点为1,2-Dichloroethane、终点为Glycolate、条件为Aerobic；用于确定D2主链终点边界。
- SCOPE_ROW / SCOPE#BIOPATH150_006#CG04：aerobic为本题应用关键任务条件；答案主链为水解/氧化型好氧路线，不违氧条件。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_006：gold精确酶/EC与答案存在差异，属D3a酶对应正确性问题；D2不据此重复扣化学分。

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 前四个必答目标反应与冻结gold主链一致：1,2-二氯乙烷→2-氯乙醇→氯乙醛→氯乙酸→乙醇酸；S1的DhlA/EC 3.8.1.5与accepted精确匹配。S2–S4的酶功能方向正确，但S2用alcohol dehydrogenase/EC 1.1.1.1而非accepted methanol dehydrogenase/EC 1.1.2.7，S3用EC 1.2.1.3而非accepted 1.2.1.4，S4用DhlB/EC 3.8.1.2而accepted为2-haloacid dehalogenase/EC 3.8.1.3；这些属于局部名称/EC标注差异，未显示为目标反应化学不相容。答中S5（乙醇酸→乙醛酸）超出冻结4步终点，按N=4不计入目标反应。主链催化对应总体可靠，故落7。

<details><summary>V0.4理由与本行变化背景</summary>

S1 DhlA EC 3.8.1.5与反应匹配；S4 DhlB EC 3.8.1.2也属2-卤酸脱卤酶家族，答案主动说明部分库标3.8.1.3。S2用ADH EC 1.1.1.1、S3用ALDH EC 1.2.1.3，功能类别与醇/醛氧化匹配，但gold列S2为MDH EC 1.1.2.7、S3为EC 1.2.1.4，具体GJ10酶身份未确证；S5为low confidence。总体为核心步骤有合理候选但若干关键酶需进一步确认，未达到EC-反应类型明显错配的cap条件。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_006：给出四步accepted酶/EC：S1 3.8.1.5、S2 1.1.2.7、S3 1.2.1.4、S4 3.8.1.3；支持主链酶对应核验，不支持答案S2–S4的EC标注与accepted完全一致
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：给出四步主底物/主产物与方向；支持答案S1-S4的化学序列与gold主链一致，S5不在冻结四步内
- ANSWER_TEXT / B480-0019：答案实际给出的四步反应、酶名/EC及额外S5；支持对S1精确匹配及S2–S4局部EC差异的定位
- RUBRIC_CLAUSE / C05：主要目标催化对应可靠、剩余已知问题有限或局部对应/支持边界需少量修订时落7–8；高分需名号/范围更充分清楚

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案将全部步绑定到Xanthobacter autotrophicus GJ10，且complete_pathway_organism_profile_id=ORG_001。gold的organism_gold.tsv对S01-S04均列出X. autotrophicus EXACT（S04另有Moraxella sp. B替代），trait_gold.tsv的PATHWAY_COMPLETE行列出X. autotrophicus GJ10且pathway_complete=TRUE。答案未给出错误TaxID，ncbi_taxid为null，属于诚实缺失而非身份错配。按D3b锚点，主要微生物对应与全路径能力有可靠支持，仅TaxID/菌株级编号未给，取7–8档的8。

<details><summary>V0.4理由与本行变化背景</summary>

核心微生物选择Xanthobacter autotrophicus GJ10是DCE降解经典菌株；gold organism_gold对S1-S4均列X. autotrophicus，PATHWAY_COMPLETE亦有X. autotrophicus GJ10行。答案按物种+菌株去重为单一profile并由各步引用，符合任务格式。TaxID与基因组未填，S5归属GJ10未在gold中单列；未见无关类群、异菌株错配或把单步菌写成全路径菌的已核实证据，故不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：S01-S04均列X. autotrophicus EXACT；S04另有Moraxella sp. B；物种级TaxID=280。
- GOLD_SLICE / trait_gold.tsv：PATHWAY_COMPLETE行含X. autotrophicus GJ10且pathway_complete=TRUE，No TaxID；支持全路径菌声称但不提供GJ10菌株TaxID。
- ANSWER_TEXT / ANSWER.steps&#91;&#93;.microorganism; complete_pathway_organism_profile_id：答案一致归属到X. autotrophicus GJ10；故意将ncbi_taxid留null，未编造编号。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案给出全部15项性状，F4与F14明确null，其余有值。按同物种代表记录口径，X. autotrophicus物种级gold可支持若干关键性状：F2 optimum 30°C与mesophilic、F11 rod-shaped、F12 gram-negative、F13 non-sporulating与gold观测/预测一致；F4 salinity null、F14 genome null、F5 ATCC 43050、F15 habitat、F1“aerobic”精确措辞及F7一碳化合物利用仍有待核。整体属于主要性状可核实且适用，但有若干条件/来源/数值缺口，取7。未因菌株GJ10与物种代表株不同而判错。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状均出现，未知项用null，符合任务结构。可与gold物种级代表记录对照的条目多数不矛盾：F11杆状、F12 Gram-negative、F2 30℃/中温偏好、F9 DhlA/DhlB、F13不产孢等有支持或合理。问题在于多数生理性状来自EVID_005 INTERNAL_KNOWLEDGE_ONLY（low/medium），F2把培养/生长温度30写成optimum_c（P52提示培养温度不等于最适），F5 ATCC 43050在E0无记录且与gold DSM 117702不同（同物种代表记录不能仅因菌株不同判错，但仍待核），F1/F6“好氧/O2”与gold aerotolerant=true等表述存在粒度差异。无离谱数值或把预测冒充观测的系统性问题，故7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：X. autotrophicus物种级性状支持F2=30°C/mesophilic、F11=rod-shaped、F12=gram-negative、F13=non-sporulating及部分F5/F14/F6/F7观测；不证明ATCC 43050或F15。
- GOLD_SLICE / trait_scoreability_mask.tsv：标明本题F2/F5/F6/F7/F8/F9/F11/F12/F14等为observed_accuracy或completeness角色；F3/F10/F13/F15等多数为completeness_only，不能机械当数值错误。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv：F2 min/max等子字段待老师裁定；F4 min/max有观测标量但答案明确null，属完成度而非伪造。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案提供了EVID_001–EVID_006及具体locator：路线/酶/菌株有EAWAG-BBD、KEGG、Janssen 1985、van der Ploeg 1991等具体来源；但E0为EVIDENCE_GAP（entries=0），无法核对引用是否实际支持对应结论，故核心组只能登记UNRESOLVED_SOURCE。多数性状使用EVID_005 INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE；F4/F14明确null。决策相关组有具体可定位来源但未核，支持组多缺条目级来源，符合5–6档“部分关键结论可定位、其他模块缺必要记录”。没有已核实错引，不能cap。

<details><summary>V0.4理由与本行变化背景</summary>

核心路径、关键酶与GJ10身份给出EVID_001-EVID_004的条目级定位（EAWAG-BBD/KEGG/PubMed），不是纯笼统库名；但E0为EVIDENCE_GAP，所有引用均无法机核，保持UNRESOLVED_SOURCE。性状模块多依赖EVID_005 INTERNAL_KNOWLEDGE_ONLY，F4/F14为null，登记MISSING_SOURCE。无VERIFIED_MIS_CITATION_LOCAL/CRITICAL/SYSTEMIC，故不触发D5 cap；按“部分关键结论可定位、其他模块缺映射/来源”给5-6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案实际交付的来源记录；EVID_005为INTERNAL_KNOWLEDGE_ONLY，其余为DATABASE_DIRECT/LITERATURE_DIRECT但未被E0核验。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确标出S2/S3通用脱氢酶EC不确定、S5低置信、TaxID/genome/salinity null，并在uncertainties中列出替代酶、GJ10 TaxID未确认及内部知识性状。它还单列alternative_branches并标记is_part_of_scored_main_route=false，未掩盖已知边界。个别数据库/文献来源标high confidence但E0未核，属单点偏强而非系统性误导；按D6锚点取7–8档中的8。

<details><summary>V0.4理由与本行变化背景</summary>

答案清楚区分DATABASE_DIRECT、LITERATURE_DIRECT与INTERNAL_KNOWLEDGE_ONLY，逐步标high/medium/low，列出S2/S3酶身份、S4 EC归类、S5替代酶、TaxID/基因组不可得、盐度/生理数值缺源等不确定性；alternative_branches明确标注不属于评分主链。未见把预测系统性写成实证或掩盖主要矛盾。少量性状使用间接文献/内部知识但标medium，属单点偏乐观，可在档内扣分，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; confidence labels; alternative_branches：答案实际披露的不确定性与证据类型边界；不用于替代D1–D5科学核验。

</details>

## Qwen

答案SHA256：`f16d3ee35ddc3a4e7836a6712a434c6644bc44b6c8ab19f0fb754973abbf0b92`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> JSON结构完整，route_scope的氧条件与路线名原样填写，5步均给出主底物/主产物、酶/EC与微生物，15项性状字段齐全，主要模块均有涉及。但按本题冻结严格四步主链，答案仅S1与S01相符；S2产物为ethylene glycol而非chloroacetaldehyde，属中段替代，S03/S04未交付，另加S05至glyoxylate，终点与gold Glycolate不一致。因题面仅有泛化路线名且route_status=BOUNDARY_REVIEW，不能经AI直接认定D1关键错误；但D1任务符合度与必要步覆盖明显不足，属5–6档，取5：有主要模块但若干必要内容遗漏/替代，需实质修订。

<details><summary>V0.4理由与本行变化背景</summary>

5步主链、每步底物/产物SMILES、酶与EC、微生物、15项性状框架、evidence_registry与uncertainties齐备，交付格式有效；但中段路线（S2起2-氯乙醇→乙二醇→乙醇醛→乙醇酸→乙醛酸）与gold 4步指定主链（2-氯乙醇→氯乙醛→氯乙酸→乙醇酸）实质不同，且route_scope自称遵循指定路线，属任务符合度实质问题。题面仅提供路线名、无pathway ID/终点/步数，路线偏离认定存在命题定位不足风险（已入review_queue披露，但按DECISION_006非免责）。故定6分：主要模块完整、关联清楚，但路线符合度需实质修订。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;S1-S5&#93;：答案实际交付5步及各步主底物/主产物/酶/微生物，15项性状字段齐全；S2产物为ethylene glycol，S3-S5为乙二醇氧化链，终点glyoxylate
- GOLD_SLICE / PROTOCOL_DISCLOSURE_BIOPATH150_006.md#case:BIOPATH150_006：题面仅给泛化路线名，未给pathway ID、终点、关键中间体或步数；严重偏离认定存在定位不足风险，内容型偏离需人工复核，披露不是免扣
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_006：冻结路线名、好氧条件及终点Glycolate
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_006：冻结4步、LINEAR_UNIQUE、aerobic
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：S01→S02→S03→S04主链；S02主产物为chloroacetaldehyde、S04主产物为Glycolate；支持答案S2产物不同、S03/S04未交付及S5额外至glyoxylate
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：本题性状gold大量UNKNOWN；答案15项字段齐全但多项null，D1只记完成度，不据此判科学错误
- SCOPE_ROW / SCOPE#BIOPATH150_006#CG04：题面明确好氧条件为应用关键；答案route_scope填aerobic且好氧链，条件本身符合

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> D2 evaluates the submitted chemistry independently of task-route credit. The chain DCE -&gt; 2-chloroethanol -&gt; ethylene glycol -&gt; glycolaldehyde -&gt; glycolate -&gt; glyoxylate is continuous, directionally degradative, and includes water/redox cofactors without an obvious atom-balance break. Weaknesses: S2 uses a non-gold haloalcohol dehalogenase with EC null, and the later glycolate oxidation goes beyond the frozen glycolate terminal; support for S3-S5 is mainly standard/internal. Band 7-8; score 7 for local uncertainty.

<details><summary>V0.4理由与本行变化背景</summary>

S1 1,2-DCE→2-氯乙醇与gold一致；S2-S5（2-氯乙醇→乙二醇→乙醇醛→乙醇酸→乙醛酸）化学转化方向正确、SMILES结构正确、原子与氧化还原大体守恒、辅因子（H2O/NAD+/O2）在列、步骤连接连续，符合好氧条件；替代中段路线依据为INTERNAL_KNOWLEDGE_ONLY（未证实），按未证实登记不判错亦不给高分；S5延伸至glyoxylate超出gold终点glycolate，按题面终点/范围规则下游延伸不加分亦不扣分。定7分：主链化学成立，关键转化证据有限。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Provides the submitted S1-S5 chemistry and cofactors for independent D2 evaluation.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：Shows gold S01-S04 and glycolate terminal; does not require D2 to treat a non-gold but chemically coherent alternative as task credit.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按冻结4步目标核验：S01的1,2-二氯乙烷→2-氯乙醇与haloalkane dehalogenase/EC 3.8.1.5相符，可判支持；S02目标为2-氯乙醇→氯乙醛（甲醇脱氢酶/EC 1.1.2.7），答案S2却改为水解脱卤生成乙二醇；S03（氯乙醛→氯乙酸）和KEY_TERMINAL S04（氯乙酸→乙醇酸）目标反应均未交付，答案后几步走乙二醇→乙醇醛→乙醇酸替代支路。仅1/4目标反应获支持且存在关键终点缺失/中途替换，受D-KEY4上界限制，落在&#91;3,4&#93;；因可用目标很少取3。

<details><summary>V0.4理由与本行变化背景</summary>

S1 haloalkane dehalogenase EC 3.8.1.5/dhlA 与gold S01完全一致（有数据库条目定位）；S2 haloalcohol dehalogenase/dhlB酶名合理但EC填null（诚实）；S3-S5为广谱通用酶（EC 1.1.1.1 alcohol dehydrogenase、EC 1.2.1.3 aldehyde dehydrogenase、EC 1.1.3.15 glycolate oxidase），反应类型匹配但缺具体催化证据且低置信。各EC号因E0 EVIDENCE_GAP无法冻结核对accepted name/reaction，保持待核。定6分：S1可靠，S2-S5合理候选但缺具体核验。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：确定四个目标反应及主产物；不支持答案中的乙二醇分支回填为S02-S04目标完成。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_006：支持S01答案EC与目标匹配；S02-S04答案所给酶/EC与目标不符或目标步骤缺失。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_006：支持本题按4步目标主链评价，不把乙二醇替代支路作为目标步数扩展。
- RUBRIC_CLAUSE / C05：支持在只有少数目标可用且关键失败明确时取受限范围下沿，而非机械取4。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> The microorganism identity is correctly Xanthobacter autotrophicus GJ10, a recognized DCE degrader, and gold has Xanthobacter across S01-S04 plus pathway_complete rows. However the answer assigns non-gold S2-S5 step capabilities and a whole-pathway ORG_001 claim to GJ10 with only broad literature/internal support. No verified contradiction is present, but several step-level capability claims remain unconfirmed. Band 5-6; score 6.

<details><summary>V0.4理由与本行变化背景</summary>

全部5步微生物为Xanthobacter autotrophicus GJ10，是1,2-DCE降解经典菌株，与gold S01-S03的Xanthobacter autotrophicus（TaxID 280）身份一致；S1-S2（dhlA/dhlB脱卤）有可靠背景支持；complete_pathway_organism_profile_id=ORG_001声称整条路径能力，S3-S5具体酶-菌株证据低置信。未提供TaxID/保藏号（null，诚实）。无身份编造，非仅单步菌冒充全路径。定7分：核心身份可靠，S3-S5能力需确认。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows all step-level microorganism assignments and the whole-pathway ORG_001 claim.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_006：Shows Xanthobacter autotrophicus for S01-S04 and broad pathway_complete rows; does not verify every S2-S5 alternative-route capability.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：Lists Xanthobacter autotrophicus GJ10 in pathway_complete rows but with UNKNOWN traits; not step-specific capability evidence.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> Seven of 15 traits are filled. Several match available species-level gold/representative observations: F11 rod-shaped and F12 Gram-negative. F1/F6/F7/F8/F9 are plausible but not directly matched to GJ10 in E0. Key traits F2, F3, F4, F5, F10, F13, F14, F15 are null; honest null helps D6 but leaves major D4 applicability gaps. Not fabricated; partial accuracy with key gaps gives band 5-6, score 6.

<details><summary>V0.4理由与本行变化背景</summary>

15项中已填7项（F1/F6/F7/F8/F9/F11/F12），其中F11 rod-shaped、F12 Gram-negative与gold trait_gold观测一致，F7（1,2-DCE唯一碳源）、F9（haloalkane dehalogenase活性）符合GJ10经典特性，F1 aerobic与gold aerotolerant近似；F8、F6定性合理。8项定量/其它性状（F2温度/F3 pH/F4盐度/F5保藏/F10运动性/F13产孢/F14基因组/F15栖息地）诚实填null，属明确未知，非错误非遗漏。关键定量性状缺失、F1/F6表述略简化。定6分：已给性状准确适用，关键项证据不足。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows all 15 trait values and null/unknown statuses.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：Provides species-level representative trait observations for Xanthobacter autotrophicus, including F11/F12 and several missing key traits.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_006：Marks which traits/subfields are observed and scoreable; supports treating missing values as completeness/unknown rather than automatically as scientific error.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> S1 and its EC have a locatable literature/database reference, and Xanthobacter identity has a literature locator. But S2-S5 route/enzymes and F11/F12 rest on internal knowledge only or overbroad use of EVID_001; several decision-relevant groups lack verified locatable external support. E0 is EVIDENCE_GAP, so no mis-citation is verified. Band 5-6; score 5.

<details><summary>V0.4理由与本行变化背景</summary>

S1路线/酶及部分性状有EVID_001（Janssen等1985文献，可定位作者/年份/期刊）与EVID_002（IUBMB EC 3.8.1.5数据库条目）支持，条目级可定位；但S2-S5中段与终点仅EVID_003/EVID_004（INTERNAL_KNOWLEDGE_ONLY，无外部条目），F11/F12亦仅内部知识。E0 EVIDENCE_GAP，EVID_001文献内容是否支持全部claim_scope无法冻结核对，保持UNRESOLVED。决策相关组部分条目级可定位、部分缺失，落5-6档；无已核实错引，不cap。取5分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows the answer&#x27;s own source registry, internal-knowledge-only entries, and claim_scope mappings.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> Uncertainty is generally honest: S1 is high with specific literature/database, S2 medium, S3-S5 low with explicit EC/step uncertainties; internal-knowledge-only evidence is labeled low; unknown traits are null and listed. Minor overconfidence affects F1/F7 high labels, but this is not systemic. Band 7-8; score 8.

<details><summary>V0.4理由与本行变化背景</summary>

答案证据性质分层较清楚（LITERATURE_DIRECT/DATABASE_DIRECT与INTERNAL_KNOWLEDGE_ONLY区分），逐项confidence标注，uncertainties数组具体诚实（EC未定、S3-S5证据弱、性状null），null使用明确。但个别性状（F1/F7/F8）标high confidence而E0 GAP下文献内容未核，属单点过度确信；complete pathway能力声称强度略超S3-S5证据。属非系统性，不构成D6 cap。定7分：披露总体与证据相称，局部强度略超依据。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：Shows confidence labels, uncertainty notes, and null handling across steps and traits.

</details>

## Grok

答案SHA256：`47b3e1660274c6cfe6b27402b7d4e42ada1d718849701f830877d29dddb775b4`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 取 9（7–8/9–10 档上沿）：题面指定路线名被原样采用；给出 4 步连续主链，每步有主底物/主产物英文名与 SMILES、首选酶与可给 EC、对应微生物；同一菌在 organism_profiles 中仅一条 ORG_001；15 项性状全部出现，未知项以 null/unknown 明示，无遗漏模块。少量 EC null 与外部来源不足分别归 D3a/D5，不构成 D1 重大缺项。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面要求四步主链、每步酶/EC/微生物、15项性状及 null 规则；不证明答案科学正确。
- ANSWER_TEXT / ANSWER_BEGIN：显示答案实际交付的模块与字段完整性；不证明其来源可追溯。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_006：gold 为 4 步线性主链；仅用于完整性边界对照，不要求答案覆盖全图旁支。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 取 8（7–8 档上沿）：有机主链与 gold 一致，为 1,2-二氯乙烷→2-氯乙醇→氯乙醛→氯乙酸→乙醇酸，方向为底物到产物，终点为 Glycolate；四步连接连续，无反向或跳步。扣分点主要是局部计量/辅因子表达：S1、S4 未列 H+，S2 PQQ 依赖醇脱氢酶未列电子受体（gold S02 列 ferricytochrome c/ferrocytochrome c），属 P103 局部辅因子/计量缺陷，不触发 cap；按 7–8 档取 8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：支持 gold 有机底物/产物序列与终点 Glycolate；不证明答案自身来源，也不要求答案复述全部 redox 载体。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_006：支持题面/gold 终点为 Glycolate；不扩展到下游中心代谢评分。
- ANSWER_TEXT / ANSWER_BEGIN：显示答案给出的化学转化；不证明反应被实验验证。

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1给出haloalkane dehalogenase/EC 3.8.1.5，与gold accepted name/EC及S01反应方向一致，属可核功能级对应。S2仅给quinoprotein alcohol dehydrogenase且EC=null，gold accepted为methanol dehydrogenase/EC 1.1.2.7，不能确认同一名称/EC，也未证不相容，记U。S3给aldehyde dehydrogenase/EC 1.2.1.3，gold accepted为acetaldehyde dehydrogenase/EC 1.2.1.4，显式EC/名称待核，记U。S4给2-haloacid dehalogenase/EC 3.8.1.2，gold accepted同名EC 3.8.1.3，答案自述部分库泛注3.8.1.3，仍属显式EC配对未核，记U。没有已核目标失败或已确认KEY失败，故不触发D-KEY4≤4；但3/4步的EC/名称配对仍待核，阻止进入7–8，按C05同带取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Answer claims S1-S4 enzyme names/ECs and S4 note about alternative EC annotation; used to identify delivered enzyme claims, not as independent proof.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_006：Gold accepted enzyme names/ECs for required steps S01-S04: S01 3.8.1.5; S02 1.1.2.7; S03 1.2.1.4; S04 3.8.1.3. G4-level support only; does not prove specific protein activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：Gold reaction direction and main substrate/product sequence for S01-S04; supports that answer main products align, but does not by itself resolve enzyme name/EC equivalence.
- GOLD_SLICE / PROTOCOL_DISCLOSURE_BIOPATH150_006.md：Strict frozen 4-step scope and route-name uniqueness limitation; disclosure is not a waiver and does not convert unresolved enzyme pairs into confirmed errors.

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b 取 8（7–8 档）：答案核心微生物为 Xanthobacter autotrophicus GJ10/TaxID 280，与 gold organism_gold 的 X. autotrophicus（TaxID 280）及 PATHWAY_COMPLETE X. autotrophicus GJ10 行相容；S01–S04 均归同一菌，且 gold 各步均有 X. autotrophicus accepted 记录（S04 另有 Moraxella sp. B，但非排斥 X. autotrophicus）。主要扣分为身份粒度：TaxID 280 是种级，GJ10 在冻结切片中无独立菌株级 TaxID；属物种级支持菌株级声称的档内扣分，不 cap。全路径能力有 GJ10 PATHWAY_COMPLETE 名称级支持，故在 7–8 档取 8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_006：支持 X. autotrophicus TaxID 280 与 GJ10 PATHWAY_COMPLETE 名称级记录；TaxID 280 不是菌株级 TaxID，也不自动证明所有菌株能力。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：支持种级 TaxID 280 的基因组记录；不提供 GJ10 菌株级 TaxID。
- ANSWER_TEXT / ANSWER_BEGIN：显示答案微生物身份与绑定；不证明其菌株级能力已被实验验证。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4 取 6（5–6 档）：答案 15 项性状字段齐全，8 项填写、7 项明确 null/unknown；已填的 F11 杆状、F12 革兰氏阴性、F13 不产芽孢、F9 DhlA 活性、F8 好氧矿化/转化能力与 gold 种级代表记录大致相符。主要缺口是温度 F2、盐度 F4、保藏 F5、基因组 F14 等 gold 种级代表记录已有可核验项，答案却置 null；F1“专性好氧”比 gold 的 aerotolerant=true 表述更强，F6 好氧呼吸/末端 O2 也仅有内部来源。按同物种代表记录口径，这些是完成度/适用性缺口，不是把种级值自动强加给 GJ10；因关键性状仍缺失、部分条件解释需修订，落在 5–6 档取 6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：支持种级代表记录的已观测/预测性状；同物种代表记录不表示所有 GJ10 菌株完全相同，也不得回填答案缺失来源。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_006：区分 observed_accuracy 与 completeness_only；F2 子字段待老师冻结范围政策，F5/F14 等有可核项。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_006：F2 minimum_c/maximum_c 待裁定；F4 minimum=0、maximum=2 % NaCl 为可核标量；不把文本类别当数值分母。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_006：支持 GJ10 全路径能力名称级记录；不覆盖全部表型性状。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 取 2（1–2 档）：答案 evidence_registry 的 EVID_001–EVID_006 全部 source_type=INTERNAL_KNOWLEDGE_ONLY，locator 为“Recalled ...”式自我记忆说明，没有 DOI、数据库条目、登录号或可定位记录；CORE/APPLICATION_CRITICAL 组均为 MISSING_SOURCE。虽然答案有 evidence_id 与 claim_scope 的结构化外观，但不能把内部自述当作可追溯来源。未发现经核实的错引，故不触发 D5 cap；按 MISSING_SOURCE 低分档取 2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案实际交付来源类型为内部知识自述；不提供可定位外部来源。
- GOLD_SLICE / PROTOCOL_DISCLOSURE_BIOPATH150_006.md：说明命题定位限制；不是答案来源，也不能替答案补证。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 取 7（7–8 档下沿）：答案把多个未知性状明确置 null/unknown，列出 5 条 uncertainties，evidence_registry 明确标 INTERNAL_KNOWLEDGE_ONLY，并区分部分 high/medium/unknown 置信度，整体不是系统性把预测冒充实证。扣分点是若干内部记忆型断言仍标 high（如 F1、F6、F7、F9、F12），且对部分性状的 observed/predicted 性质未逐项展开；属单点过度确信/披露不足，不是系统性误导，故不 cap，取 7 而非 8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案对未知、内部知识来源和部分限制的披露；不证明披露内容均正确。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：用于比较答案置信度与 gold 种级观测/预测口径；不能替答案补来源。

</details>

## GPT5.6

答案SHA256：`47c44dcfe65c724c46fb5433dcedbbdbbbbdc4a2d8cd6ac242310b975f6d3712`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求的指定路线主链已实质交付：S1–S4四步均给出主底物/主产物的英文名与SMILES、一个首选酶(名称+EC)、一个对应微生物(种+菌株)并绑定同一去重profile ORG_001；route_scope.chosen_route_name逐字回显题面路线名、oxygen_condition=aerobic、is_single_continuous_route=true；结构字段齐全、无JSON损坏，程序task_conformance_status=OK。缺陷集中在性状模块：15项性状虽然全部出现，但每项value均为null、evidence_id为null、confidence=unknown，等于0/15项实质填写，只是占位骨架；题面同时要求“各项最强来源”，该部分亦未交付（evidence_registry仅一条INTERNAL_KNOWLEDGE_ONLY概括条目，未映射到任何性状）。据此主要模块均有涉及但存在整块仅占位、必要内容遗漏，属5–6档；因性状模块完全未实质填写，档内取下沿5。未发现更换指定路线/氧条件的任务偏离，也未编造具体蛋白或菌株能力，故D1不构成关键错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：四步主链每步均有底物/产物名+SMILES、酶名+EC、菌名+菌株并引用ORG_001
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：15项性状全部为null/unknown且evidence_id为null，仅占位未填内容
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_006：本题指定路线为4步LINEAR_UNIQUE(ordered_step_count=4)，用作完整性步数参照，不代表需并集所有旁支
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_006：题面路线名与终点化合物Glycolate对应本案
- QUESTION_TEXT / BIOPATH150_006：题面要求：4步主链每步主底物/主产物SMILES、一个首选酶EC、一个对应微生物，并一次性填写15项性状及最强来源
- RUBRIC_CLAUSE / P45：诚实填写未知/null在D1反映完成度不足

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步化学与gold主链一致：S1 1,2-dichloroethane→2-chloroethanol（水解脱卤）、S2 2-chloroethanol→chloroacetaldehyde（醇氧化）、S3 chloroacetaldehyde→chloroacetate（醛氧化）、S4 chloroacetate→glycolate（水解脱卤）；方向均为底物→产物、整体为污染物向终点的降解方向，S1→S2→S3→S4链条连续，终点乙醇酸与gold_terminal_main_products(Glycolate)一致。SMILES经质子化/电荷归一后与gold相同（S3/S4仅为羧酸与羧酸根表示差异，路线诊断为charge-blind同构、jac_sub=jac_prod=1.0），未出现原子不守恒、方向反转或一步跳到中心代谢物等关键错误。局部缺陷是四步均未写出H2O、Cl−、H+及NAD(P)+/NADH等币种代谢物，属P103局部计量缺陷，在7–8档内处理且不cap；题面只要求主底物/主产物，简化表达按P104不自动判错。程序nine_ten_eligible(D2)=false，故取本带上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：四步目标反应的底物/产物、方向(SUBSTRATE_TO_PRODUCT)与主链连接S01→S02→S03→S04
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_006：起点1,2-Dichloroethane、终点Glycolate、好氧类别
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案所答四步产物链与gold一致（仅质子化/电荷写法差异）
- RUBRIC_CLAUSE / P103：主有机物转化正确而辅因子遗漏属7–8档局部计量缺陷，不自动cap
- RUBRIC_CLAUSE / P104：简化反应表达不自动等同原子不守恒或错误反应

</details>

### D3a 目标反应与酶对应：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> N=4且逐目标全部有交付。S01所答Haloalkane dehalogenase + EC 3.8.1.5与accepted集合的酶名/EC配对一致，可作策展粒度(G4)功能级支持（KEY入口步获支持）。S02 Alcohol dehydrogenase EC 1.1.1.1与accepted methanol dehydrogenase EC 1.1.2.7不符；S03 Aldehyde dehydrogenase EC 1.2.1.3与accepted EC 1.2.1.4不符；S04 Haloacetate dehalogenase EC 3.8.1.2与accepted 2-haloacid dehalogenase EC 3.8.1.3不符（疑似名/号互换）。这三步酶类与反应类型在化学上可成立（醇氧化、醛氧化、水解脱卤），但均落在accepted集合之外，且本案E0为整题EVIDENCE_GAP（EC 1.1.1.1、1.2.1.3、3.8.1.2无冻结记录可核），按C03只能登记为U（PAIR_UNVERIFIED/SUPPORT_GAP），不得转S，也不得因未命中accepted直接判F。S01(KEY_ENTRY)已支持、S04(KEY_TERMINAL)仅为U，四个KEY目标均无已核F或实证交付M、无催化矛盾证明，故D-KEY4的≤4上界不被触发，也不存在经核实的关键错误。结果S=1、U=3、F=M=0：可用目标仅1/4且集中在入门步，S02–S04三个MAJOR/KEY步的酶对应仍需实质核验/修订，故排除7–8档（KEY/MAJOR U不得给7）；但支持部分（S01名号配对与反应一致）与待核部分（S02–S04为何不能确认）边界清楚，且三处U均属plausible候选而非已核失败，故取&#x27;少数目标可用、边界清楚&#x27;档的上沿4，不取中点、不机械取上限。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_006：本题逐步accepted酶名/EC：S01 3.8.1.5、S02 1.1.2.7、S03 1.2.1.4、S04 3.8.1.3；仅支持策展粒度的功能推荐，不证明具体蛋白底物谱或实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_006：四个目标反应的底物—产物定义，作为&#x27;目标反应&#x27;口径；不支持的步骤细节不扩展
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案逐步所答酶名/EC，用于与accepted集合比对
- RUBRIC_CLAUSE / C03：S/F/M/U/H五分法优先级；未命中accepted不自动判错；ROUTE_HOLD/CANDIDATE类登记U
- RUBRIC_CLAUSE / C04：U≠0时不机械套覆盖率带，由裁判按既有分档评实际支持与错误；全U不自动NE或低分
- RUBRIC_CLAUSE / C05：档内判据：KEY/MAJOR U不得给7；少数目标可用且边界清楚取3–4档上沿
- RUBRIC_CLAUSE / D-KEY4：仅在预定义KEY存在合法已核F或实证M时压到≤4；本案未触发

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案将四步统一归属Xanthobacter autotrophicus GJ10，并正确去重为单一profile。gold S01-S04均列Xanthobacter autotrophicus为EXACT，S04另有Moraxella但Xanthobacter可接受；trait_gold另列Xanthobacter autotrophicus GJ10的PATHWAY_COMPLETE为TRUE。答案未编造TaxID，只留null；主要微生物身份与整路能力对应可靠，TaxID/菌株级编号未交付属局部待核，不推翻主要推荐，取7–8档上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_006：支持Xanthobacter autotrophicus在S01-S04为EXACT；S04还列Moraxella sp. B，但不排斥Xanthobacter。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：支持GJ10整路能力记录为TRUE；该行无TaxID，不证明答案缺失的TaxID。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：记录答案实际提交的菌名/菌株与统一profile；不把缺失TaxID回填为已核。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案返回了15项性状字段，但全部value为null或对象各子键null，confidence均为unknown；没有任何可评价的性状数值。按量表P44及全null规则，D4记MISSING=1，不宣称检测到科学错误；完成度问题在D1/覆盖登记中反映。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：证明答案15项性状均未交付可评价数值；不证明这些性状在真实世界未知。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_006：gold存在多项observed性状记录；仅说明答案未交付，不作为惩罚编造的证据。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_006：支持部分性状具observed_accuracy可评分；答案全null，故D4无内容可评。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的唯一evidence_registry条目EVID_001为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；路线、酶、微生物与性状结论均无条目级可定位来源。按D5六状态登记为MISSING_SOURCE，而非已核实错引；无cap，但可追溯性落在1–2档，取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：证明答案只提交内部知识型证据，无数据库/记录/定位；不证明任何外部来源不存在。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案多处明确标注酶/EC未核实、菌株培养条件与基因组/15项性状无可核验来源，并将性状全部留null；uncertainties具体列明缺口，未把预测包装成实验观测。S1介质confidence为medium、S2-S4为low，整体披露与证据弱相一致。仍保留‘有报道’等无来源表述，故取7–8档上沿8而非9–10。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：记录答案明确披露酶/基因/EC/性状来源未核实；支持D6正面评价。
- ANSWER_TEXT / ANSWER.steps&#91;0-3&#93;.enzyme.confidence：记录medium/low置信标签；不证明这些置信度本身已被外部证据校准。

</details>
