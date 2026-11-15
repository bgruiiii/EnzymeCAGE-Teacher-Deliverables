# BIOPATH150_125：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：methyl tert-butyl ether degradation

污染物：Methyl tert-butyl ether；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 50 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 44 | COMPARABLE | RECOVERED_BATCH_B |
| Kimi | 55 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 57 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 60.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 44.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`ae163762b4e4f31c0e77749d8419a82540f7e377f9043422dad19df9fcc3fe81`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 所有主要交付模块均出现：9步路线、逐步酶/菌、2个organism_profiles、每profile 15项性状、来源注册与不确定性说明；但路线诊断DEVIATES且未覆盖认可主链的终点/若干必答步，故在D1固定&#91;1,4&#93;内取上沿4，表示呈现较完整但任务符合度受限。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖全部任务模块：9步主链（每步主/产物name+SMILES、enzyme、microorganism）、2个organism_profiles各15项性状、evidence_registry与uncertainties齐备；route_scope.chosen_route_name逐字保持题面路线名&#x27;methyl tert-butyl ether degradation&#x27;，无改选路线。扣分点：9步中7步ec_number为null（仅S8给1.1.1.31、S9给1.2.1.27），酶名多为功能性通名，未达&#x27;每步酶+EC&#x27;的完整交付强度；属诚实未知但仍是必要字段的部分缺项。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT#BIOPATH150_125：题面要求主链、每步底物/产物/SMILES、首选酶及EC、对应微生物、15项性状；指定路线名称为methyl tert-butyl ether degradation。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_125：显示答案交付了9步路线及2个菌株profile；不能证明其覆盖认可gold主链全部必答步或终点。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 前段MTBE→tert-butyl formate→tert-butanol→diol→2-hydroxyisobutyrate主干大体可成立；但S4以单步脱氢直接由diol到羧酸，压缩了醛中间体，S6变位酶产物与gold S10的(S)-3-hydroxybutanoyl-CoA不符，后续走向propionyl-CoA/formate而非gold terminal acetyl-CoA。属于主干部分成立但关键中间体和连接需实质修订，在D2允许&#91;1,5&#93;内取5。

<details><summary>V0.4理由与本行变化背景</summary>

上游主链（S1 MTBE→tert-butyl formate；S2→tert-butanol+formate；S3→2-methylpropane-1,2-diol；S4→2-hydroxyisobutyrate；S5→2-hydroxyisobutyryl-CoA）方向正确、原子基本守恒（S1净式MTBE+O2→TBF+H2O成立），与gold净转化一致，S1与S4虽各合并一个中间体但有披露。关键问题在下游分支：S6称2-hydroxyisobutyryl-CoA mutase生成3-hydroxyisobutyryl-CoA（分支型），而gold S10该mutase产物为(S)-3-hydroxybutanoyl-CoA（线性），二者结构不同；S7–S9走缬氨酸支路（3-HIB→methylmalonate semialdehyde→propionyl-CoA）而非gold的acetoacetyl-CoA→acetyl-CoA，终点为propionyl-CoA（下游续接succinyl-CoA另列）。按四步判断：题面仅给路线名未指定终点；答案已明确声明替代分支并披露不确定性（替代分支均标is_part_of_scored_main_route=false）；该分支为真实生化可能但菌株专属证据为间接、且S6产物与特征化产物不符——偏离未推翻&#x27;MTBE经TBA、2-HIB进入中央代谢&#x27;的主结论，故档内扣分、不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：gold主链给出S06→S10→S07→S09等反应方向与产物；显示S10应为2-hydroxyisobutyryl-CoA到(S)-3-hydroxybutanoyl-CoA，S09通向acetyl-CoA。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_125：答案自述S1–S9路径及替代分支；显示S4简化、S6产物和S9终产物与gold主链分叉。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> Release目标映射为S=0、F=2（S06、S10两个KEY失败）、U=8；无confirmed target enzyme支持，且两个确认KEY失败使目标酶路线主推荐失效。因仍有部分步骤的结构/名称局部信息可读，给2而非1；但可用目标信用和主要失效边界不清，不能进入3以上。

<details><summary>V0.4理由与本行变化背景</summary>

酶类别与反应类型总体匹配：单加氧酶/P450对氧化羟化、dehydrogenase对脱氢、ligase对CoA活化、mutase对重排、hydrolase对硫酯水解，均无酶名-EC互矛盾。正向支持：S8 EC 1.1.1.31 accepted name &#x27;3-hydroxyisobutyrate dehydrogenase&#x27;与答案酶名逐字一致、反应底物/产物名称层面一致（E0 f3e0:tp:EV029-15）。不足：7/9步无EC/基因标识、酶名多为功能性；S9 EC 1.2.1.27无冻结记录（UNRESOLVED，不判虚构）；S6酶类正确但产物身份偏；S8/S9已诚实声明为缬氨酸同源酶的间接参与，未把家族相关性冒充具体催化证据。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：显示S06、S10及终点S09的必答gold反应；不确认答案其他U步骤。
- E0_EVIDENCE / f3e0:tp:EV029-15：仅提供EC 1.1.1.31的第三方URL/引文层记录，且该记录本身标注不可独立核验；不证明答案S8在目标gold步骤中的催化信用。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_125：定位答案S6/S10分支与S8 EC声明；不能把错误路线内部酶自洽转化为目标信用。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 两个菌株身份/菌名分开写，M. vaccae JOB5与Aquincola tertiaricarbonis L108均为与MTBE/叔碳化合物降解相关的合理候选；但S1/S2对JOB5、S7–S9对L108的逐步能力及complete_pathway声明主要靠自由文本/内部知识，未能充分核验。处于5–6档，取6因身份层面未发现需cap的矛盾。

<details><summary>V0.4理由与本行变化背景</summary>

选用的两株菌为该路线经典且正确的模式菌：ORG_001 Mycobacterium vaccae JOB5（S1–S2，丙烷生长下共代谢MTBE/TAME，答案F8正确注明&#x27;不能以MTBE为唯一碳源生长&#x27;，未把共代谢写成唯一碳源整路径）；ORG_002 Aquincola tertiaricarbonis L108（S3–S9，叔碳/MTBE降解菌）。菌名/菌株为实存，无TaxID交付(null)故无身份编造；complete_pathway_organism_profile_id=ORG_002对L108这类完整降解菌属可辩护。扣分：L108下游按缬氨酸支路的反应级能力仅间接支持（见D2），粒度/菌株专属证据需补；未把单步菌错误写成全路径菌（JOB5未被标为complete-pathway）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_125：gold列出多步对应菌与PATHWAY_COMPLETE行；支持Aquincola tertiaricarbonis为complete-path候选，但不逐字确认答案的JOB5/L108每一步能力分配。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_125：显示答案按菌株分开profile并将JOB5用于前两步、L108用于后续步骤；也显示complete_pathway选择。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 每个profile均给出15项性状，广泛使用null/unknown/低置信度，避免了填满即高分的误判；M. vaccae与A. tertiaricarbonis的许多属/种级性状合理，但若干菌株级性状仅EVID_006内部知识或EVID_004自由文本，Astrain F11杆状与gold observed oval-shaped存在待核差异。属部分准确且适用但关键项证据不足，取6。

<details><summary>V0.4理由与本行变化背景</summary>

两profiles性状大体为正确的物种级事实（JOB5：好氧、革兰氏阳性抗酸、杆状、无运动、不产孢、丙烷营养共代谢；L108：好氧、革兰氏阴性、不产孢、MTBE降解菌），未见离谱数值或把预测冒充观测。扣分：ORG_001多项性状仅由EVID_006 INTERNAL_KNOWLEDGE_ONLY支撑却标high（来源级别诚实但置信偏高）；A. tertiaricarbonis存在可评分实测温度（gold：min 4、max 40、growth 30℃）而答案仅给&#x27;中温性&#x27;无数值，关键性状证据不足；L108形态gold为oval-shaped而答案作杆状（轻微）。同物种代表记录口径下不因菌株差异判错。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_125：提供多个菌的观测性状记录，包括Aquincola tertiaricarbonis的F11 oval-shaped；不支持把EVID_006内部知识全部当观测。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_125：显示性状值、raw_text、evidence_id与confidence；可核对哪些是null、内部来源或高置信声明。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案提供了evidence_registry并把条目映射到step/酶/菌/性状，部分条目有具体文献作者、年份与主题，可定位到文章级；但无DOI/record_id，EVID_005–007为INTERNAL_KNOWLEDGE_ONLY，关键步骤与性状仍有缺映射。无VERIFIED_MIS_CITATION，不能cap；按部分关键结论可定位、其他仍缺映射，取5。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry含7条：4条特定文献（Smith 2003、Schuster~2012、Rohwerder&amp;Müller、Lechner 2007，含作者/期刊/主题locator但无DOI/record_id）+3条INTERNAL_KNOWLEDGE_ONLY（EVID_005/006/007）。按集合语义：存在条目级可定位可核对结论——S8 EC 1.1.1.31经E0核对（名称+反应）支持，据此进入5–6档；但大量核心反应/酶/性状结论缺条目级来源（文献为自由文本无法机器定位、其余为内部知识），决策相关组以UNRESOLVED_SOURCE与MISSING_SOURCE混合为主。无经核实错引（无CONTRADICTED、无VERIFIED_MIS_CITATION）→不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_125：显示实际交付的来源映射及其证据类型；D5只评这些原交付，不用评价者补证。
- E0_EVIDENCE / f3e0:tp:EV029-15：E0仅有一条EC 1.1.1.31的第三方URL/引文记录且不可独立核验；不能验证答案大多数自由文本/内部来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案多处明确null、confidence、alternative_branches与uncertainties，说明S4/S6等不确定性并未掩盖；主要限制、替代分支和部分未核信息可读。问题是部分M. vaccae性状以EVID_006内部知识配high/medium confidence，存在局部过度确信，但非系统性把预测写成实证。7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且充分：uncertainties列出首步产物歧义、esterase可能自发水解、S4脱氢酶未分子证实、下游B12-mutase与methacrylate替代、S7–S9缬氨酸同源酶参与证据间接、TaxID/基因组未核实；alternative_branches三条均标is_part_of_scored_main_route=false；声明了终点(propionyl-CoA)与下游续接，边界清晰。扣分：ORG_001多项物种事实以INTERNAL_KNOWLEDGE_ONLY却标high，属单点/局部过度确信（虽source_type诚实标注），档内扣不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_125：显示不确定性披露、替代分支标注与confidence分布；用于评价证据性质与边界表达。

</details>

## DeepSeek

答案SHA256：`f7390a7260a22827671bf9785ceab51db20ab520edfd57f228c7350f834c648c`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 答案给出7步连贯路线、逐步酶/菌、15项性状和证据表，格式可读；但题面/任务合同要求完整10步gold主链（formal_cases ordered_step_count=10）。答案改走MTBE→TBA+甲醛入口，未覆盖tert-butoxymethanol/tert-butyl formate等gold步（S05/S08/S02等），仅少部分必答步可对应，属核心任务模块大部缺失/明显路线偏离。按TABLE0 3–4档取3（仅覆盖少数必要模块，多处缺步），并因关键任务模块缺失记D1关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖路径、酶、微生物、15项性状与来源登记；路线止于题面/gold终点acetyl-CoA，15项中9项填写、6项明确unknown；S3/S4缺EC、来源记录无条目级定位，但属局部缺失，不影响本维主要完成度。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_125：n_required/ordered_step_count=10，LINEAR_UNIQUE；本题要求完整主链
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：gold主链S05→S08→S02→S04→S01→S03→S06→S10→S07→S09的底物/产物顺序；不把旁支视为分母
- ANSWER_TEXT / ANSWER_BEGIN：答案仅7步且S1产物为tert-Butyl alcohol+Formaldehyde，缺少tert-Butoxymethanol/tert-Butyl formate步骤
- QUESTION_TEXT / QUESTION_BEGIN：题面指定route_scope.chosen_route_name并锁定路线范围

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 按化学自身质量评价，答案路线大体连贯：MTBE O-脱烷基到TBA+甲醛是已知好氧替代入口；TBA羟化、HIB-CoA变位、3-HB-CoA脱氢、硫解到acetyl-CoA均可成立，终点与gold terminal acetyl-CoA一致。主要问题是单加氧酶步骤未列O2/NADH等辅因子，S3把二醇直接氧化成酸并跳过2-hydroxy-2-methylpropanal，部分中间体/连接需实质修订；证据登记多为笼统PubMed定位。按TABLE0 5–6档取6（主干部分成立，关键中间体/连接仍需修订），不因与gold不同自动判错，也不因自洽替代路线回填任务完成。

<details><summary>V0.4理由与本行变化背景</summary>

主链MTBE→TBA→2-甲基丙烷-1,2-二醇→2-羟基异丁酸→HIB-CoA→3-HB-CoA→乙酰乙酰-CoA→乙酰-CoA总体连续，起始直接裂解属可讨论的替代路线；但S3把diol→醛→酸的gold两步合并为diol→酸一步，S7又缺少CoA/第二分子乙酰-CoA的计量表达，关键中间体与连接仍需修订。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：7步连接、化学转化、缺失辅因子/S3跳跃
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_125：terminal compound为acetyl-CoA；仅端点身份
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：gold S04/S10/S07/S09支持TBA→diol、HIB-CoA→3-HB-CoA、3-HB-CoA→acetoacetyl-CoA、acetoacetyl-CoA→acetyl-CoA的对应化学类型；不外推答案全部步骤

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 按冻结目标合同，10个必答目标反应中仅S01–S04有绑定声称且function/pair均为UNRESOLVED（EC非match或未绑定），S05–S10为MISSING/未绑定；无S，C=S/N=0/10，落入&#91;1,2&#93;。KEY入口S05的答案MTBE步产物为TBA+甲醛而非tert-butoxymethanol，属已核目标反应不符；终点等亦未形成可核S。答案中S4–S7虽有名称相近的下游步骤，但EC/结构/目标绑定未确认，不能回填S。无已核目标催化可支撑主功能，按C05取1（在&#91;1,2&#93;内无已核成功，不能因文字或替代路线自洽升2）。

<details><summary>V0.4理由与本行变化背景</summary>

S7 EC 2.3.1.9属于gold多注集合，可接受；S3/S4 EC为null；S1/S2/S5/S6所填EC均无E0官方条目，且与gold所列1.14.13.M36、1.14.13.229、5.4.99.64、1.1.1.35不同，不能判错但关键步骤缺具体核验；S3酶名与一步生成酸产物的匹配也需修订。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：S05 gold reaction为MTBE→tert-Butoxymethanol；S09为acetoacetyl-CoA→acetyl-CoA；未绑定答案步不自动视为S
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_125：S05 accepted enzyme为MTBE monooxygenase EC-1.14.13.M36；仅支持该目标反应，不支持TBA+甲醛
- ANSWER_TEXT / ANSWER_BEGIN：S1产物为TBA+甲醛；S4–S7下游步骤名称/EC及部分SMILES为空

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 微生物身份为Mycobacterium austroafricanum IFP 2012，物种本身是真实MTBE降解相关类群，gold中也有M. austroafricanum物种级PATHWAY_COMPLETE行，故不是身份虚构。但答案把全部7步都归给同一菌株，且仅以EVID_006 INTERNAL_KNOWLEDGE_ONLY支持；gold多个步骤的实际策展菌为Methylibium petroleiphilum、Aquincola tertiaricarbonis等，答案缺少反应级/菌株级能力证据。按5–6档“合理候选和部分支持，但若干关键作用范围未充分核验”，取5。

<details><summary>V0.4理由与本行变化背景</summary>

Mycobacterium austroafricanum IFP 2012在gold organism_gold的S03步骤中有EXACT名称/菌株匹配（No TaxID），物种为已知MTBE降解相关菌；但答案把全部七步及完整路径能力归给该单一菌株，缺少反应级/全路径级证据，gold另有Methylibium petroleiphilum、Aquincola tertiaricarbonis承担多步，故为合理候选但作用范围未充分核验。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_125：支持M. austroafricanum为相关物种且存在PATHWAY_COMPLETE物种行；不支持IFP 2012已完成答案列出的全部具体步骤。
- ANSWER_TEXT / ANSWER.steps：表明答案将所有步骤绑定到同一菌株；不证明该绑定已获反应级证据。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 已填性状中F10不运动、F11杆状、F12革兰氏阳性与gold M. austroafricanum物种记录一致；F1好氧和F6好氧呼吸/O2对相关物种合理，但F7–F9关于MTBE/TBA/2-羟基异丁酸碳源、广降解能力和单加氧酶活性的表述没有IFP 2012菌株级记录支持。F2/F3/F4/F5/F14/F15为null，属完成度问题（D1承载），不在D4重复重罚。按“部分性状准确适用，但关键项证据不足”，取6。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状中好氧、好氧呼吸/O2、不运动、杆状、革兰氏阳性与M. austroafricanum物种记录基本相符；但F2温度、F3 pH、F4盐度、F5保藏、F14基因组、F15栖息地均null，F7/F8/F9的MTBE/TBA利用与单加氧酶活性、F12抗酸、F13不产孢缺少IFP 2012菌株级或官方条目支持，关键项证据不足。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_125：支持M. austroafricanum物种的motility、细胞形态、革兰氏、部分温度/基因组等记录；不支持IFP 2012全部非空性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_125：表明不同性状/子字段可评分性不同，数值缺失不自动当作错误。
- ANSWER_TEXT / ANSWER.organism_profiles：显示答案实际填写的9项非空性状及6项null/unknown。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 酶证据为PubMed加EC文本但没有record_id/DOI/具体条目；EVID_006为INTERNAL_KNOWLEDGE_ONLY，覆盖菌与性状。决策相关组几乎均为GENERIC_SOURCE或MISSING_SOURCE，缺少条目级可定位可核对来源；E0对答案多数EC无记录，无法核验但也无已核实错引。按“仅给笼统库名/模型名，结论与来源关联很弱”取3。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组CG01/CG02/CG03/CG05/CG07/CG09均无条目级可定位记录：S1/S2/S5/S6/S7仅有PubMed文字locator且record_id=null（GENERIC_SOURCE），S3/S4反应证据为null，菌株与性状仅INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；无经核实错引，故不触发错引cap，但核心来源整体不可追查，按低分档3分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：表明答案仅交付PubMed+EC文本及internal knowledge，不含可定位记录ID。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案有uncertainties数组并对多项性状显式填null，存在基本不确定性披露；但S1/S2/S7标为high confidence、EVID_006内部知识支持的多项性状标为medium，未清楚说明这些是内部推断而非观测/可定位记录，部分结论强度超过依据。属“不确定性说明存在但过泛、部分结论过强”，取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案列出三条uncertainties，并将6项性状与部分EC明确置null/unknown，具备基本不确定性说明；但S1/S2/S7以high confidence包装无条目级记录的EC，EVID_006为INTERNAL_KNOWLEDGE_ONLY却支撑多项medium confidence性状，未清楚区分观测/预测/内部推断，也未披露与gold替代路线的差异，部分结论强度超过依据。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：表明答案列出部分EC/基因组/中间步骤不确定性；不证明所有高置信标签均与证据相称。

</details>

## Kimi

答案SHA256：`cd2aff01ba4f4d2f848d88d15ad0c150c669dce2a0eec5d132389357bbfa11a2`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 答案返回5个步骤、15项性状及证据登记，主要模块均有涉及；但本题任务范围为完整gold主链10个必答步并终止于acetyl-CoA，答案步骤止于2-hydroxyisobutyric acid，S05/S08/S06/S10/S07/S09等必要步未作为step交付，主链入口与终点均不完整。按D1 5–6档“主要模块均有涉及，但若干必要内容遗漏”，因缺失的是任务必要步而非轻微工程缺陷，取5分下沿。

<details><summary>V0.4理由与本行变化背景</summary>

题面指定的chosen_route_name原样填写(methyl tert-butyl ether degradation)，五步主链各含底物/产物name+SMILES、单酶、单菌，15项性状、evidence_registry与uncertainties均有实质交付，菌按物种+菌株去重(仅ORG_001)；主要缺陷为S1把MTBE→tert-butoxymethanol→tert-butyl formate两步合并为一步、主链止于2-hydroxyisobutyric acid（下游至acetyl-CoA仅在downstream_continuation声明未展开），属少量必要内容遗漏，落在7–8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_125：ordered_step_count=10且final_graph_status=LINEAR_UNIQUE，用于说明本题完整必答主链长度，不表示所有旁支都必答。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_125：gold terminal_compound_names=acetyl-CoA，用于定位答案未到题面路线终点。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：gold主链S05→S08→S02→S04→S01→S03→S06→S10→S07→S09序列，用于缺失步骤定位；不外推替代路线自动错误。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 所答5步内部底物-产物连接连续：MTBE→tert-butyl formate→tert-butanol（+formate）→2-methylpropane-1,2-diol→2-hydroxyisobutyraldehyde→2-hydroxyisobutyrate；S2–S5与gold相应转化方向/结构大体相容，主链未出现方向反转或明显原子不守恒。S1将MTBE直接写成tert-butyl formate，跳过gold的tert-butoxymethanol中间体；答案止于2-hydroxyisobutyrate，至acetyl-CoA仅文字说明未作主链步骤连接；辅因子/O2未列按P103属局部计量问题，不据此cap。因关键中间体与终点连接仍需实质修订，按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold前段方向一致：MTBE单加氧氧化、tert-butyl formate酯解为tert-butanol+formate、TBA羟化为2-methylpropane-1,2-diol、二醇氧化为2-hydroxyisobutyraldehyde、醛氧化为2-hydroxyisobutyric acid；方向均为正向、碳数与氧化还原趋势合理。局部问题：S1把tert-butoxymethanol中间体并入一步（连续性简化）、各步未列O2/NADH等辅因子（P103局部计量，7–8档）；题面未指定具体终点，答案止于2-hydroxyisobutyrate并声明下游至acetyl-CoA，不据此cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：用于比较gold主链转化、方向与中间体序列；与gold不同不自动等于错误。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_125：gold终点为acetyl-CoA，用于判断答案主链终点连接是否完整。
- SCOPE_ROW / SCOPE#BIOPATH150_125#CG04：题面氧条件为null（未指定），条件不成立；答案选择好氧主链并披露，不据此按任务条件违背处理。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 按C03枚举10个原始目标：S01–S04为已交付但对齐/支持待核（均为UNRESOLVED；S03为ROUTE_HOLD_REPRESENTATION，属表示/电荷盲待核，不判F），S05–S10六目标为MISSING（答案steps中无对应目标步）；无S、无已核F、无H。S05为KEY_ENTRY、S09为KEY_TERMINAL，二者实证交付缺失触发D-KEY4上界；且无任何目标达到S，整题目标主链推荐不可用。按C05 1–2档，因仍有S01–S04的结构对应和部分酶功能作为局部信息可用，故取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶名与反应类型不矛盾：S1/S3为单加氧酶(EC null)，S2羧酸酯酶EC 3.1.1.1（酯水解），S4醇脱氢酶EC 1.1.1.1（醇氧化），S5醛脱氢酶EC 1.2.1.3（醛氧化），均属相应反应大类，无类别互相矛盾；但两个关键单加氧酶EC缺失、三条EC为通用酶类，与gold专一酶(1.14.13.M36、1.14.13.229、1.1.1.400、1.2.1.98、3.7.1)不一致，关键步骤缺具体核验，落5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_125：ordered_step_count=10，作为原始必答目标数N=10的来源；不把全图旁支自动并入单主链。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_125：gold各目标步的酶名/EC记录定位；仅用于识别目标步及accepted记录，不证明答案具体蛋白活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：gold主链S05–S10等反应序列，用于缺失步与目标反应定位；不外推未核EC为虚构。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_125：gold终点acetyl-CoA，用于定位KEY_TERMINAL目标S09及其缺失影响。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Methylibium petroleiphilum PM1的身份与整路径能力在organism_gold中有支持：多个步骤列Methylibium，PATHWAY_COMPLETE行亦列105560且pathway_complete=TRUE。答案以同一profile对应各步，主要微生物推荐有依据；但S4/S5对应的gold S01/S03在step表中主要列Mycobacterium等，未列Methylibium，逐步骤归属仍有局部待核，故取7档而非更高。

<details><summary>V0.4理由与本行变化背景</summary>

Methylibium petroleiphilum PM1身份正确：organism_gold对105560(PM1)为EXACT匹配，且PATHWAY_COMPLETE=TRUE（完整路径菌），故以其贯穿各步有独立依据；未填ncbi_taxid为零值完整性缺口，步级专一酶归属与gold部分步(如S01/S03归Mycobacterium spp.)不同，属少量具体条目待确认，未推翻主要微生物推荐。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_125：支持Methylibium petroleiphilum PM1身份与整路径能力；不逐一证明答案每个步骤都由该菌的实验酶学支持。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 部分关键性状与gold/mask相符：F12革兰氏阴性、F11直杆、F13不产孢、F10有运动性、F2有30°C培养上下文。问题在于多项关键子字段证据不足或过具体：F1写成“严格好氧”而gold仅明确aerotolerant=true；F2 optimum_c=30°C无观测支持；F5 ATCC BAA-1232、F14 CP000555未在冻结trait输出中核到；F9/F15含推断。pH、盐度如实null是正面披露。按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状均对正确菌株PM1给出：F10运动性、F11杆状、F12革兰氏阴性、F13不产芽孢与trait_gold观察值一致；F2 optimum 30℃与gold温度生长30/上限30相合；但F5 ATCC BAA-1232、F14 CP000555在E0无冻结记录且gold F14记为GCA_017306535.1，F1“严格好氧”相对gold aerotolerant=true程度偏强，F7/F8/F9偏概括，关键身份/数值项证据不足，落5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_125：支持部分观测性状与未知状态；不支持将未观测optimum_c、ATCC、CP000555自动视为已核。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_125：标明哪些性状子字段可作observed_accuracy、哪些仅completeness_only；用于区分可核与未核，不代替具体数值核验。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出了可定位来源：EVID_002 Nakatsu et al. 2006、EVID_003 Kane et al. 2007、EVID_004 LPSN，以及EVID_001 EAWAG-BBD路线图和EVID_005 ExplorEnz/KEGG酶类条目。优点是有具体文献与数据库记录；不足是关键路线/酶-反应主要依赖无record_id的路线图或明确写为generic class的酶条目，EVID_005不证明具体底物反应，EVID_001也未核到具体map记录。无已核实错引，E0仅有无关EC 1.1.1.31，故不作错引cap；按部分可追溯取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付了可定位来源：EVID_001 EAWAG-BBD MTBE通路图（无record_id）、EVID_002 Nakatsu 2006与EVID_003 Kane 2007完整书目引文、EVID_004 LPSN物种页、EVID_005 ExplorEnz/KEGG的EC条目；部分关键结论可定位。但EVID_001无记录ID、多数组在E0未被解析核对（GAP-125-*），无任何经核实错引，故不cap，按“存在部分条目级可定位可核对结论→5–6档”取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：评价答案实际交付的来源记录；EVID_005自述generic enzyme class，不能扩展到具体反应支持。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案较清楚地区分未知与推断：氧条件题面null并在notes说明自行选择好氧；S1/S3 EC与基因未确定置null；pH、盐度、温度上下限、基因组大小/GC显式null；downstream_continuation明确不作为评分主链。主要限制有披露。局部仍有过度确定（如严格好氧、ATCC/CP000555中等置信但未核），但非系统性把预测当观测，故取7。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties数组具体（S1/S3酶EC未定、氧条件未指定故先取好氧主链、pH/盐度/温限/基因组大小GC未见记录置null、F5/F14中等置信待复核），各事实用confidence分级、未知填null不编造，F15主动声明栖息地证据有限不夸大为广适；个别条目(如F7/F8)置信偏高但非系统性误导，属7–8档取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Qwen

答案SHA256：`83f433d33d761a7055b4f9e360173254720868a39ed59aa27ffe9bbb03ecd1af`。

### D1 完整性与任务符合度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案交付单一连续主链（S1–S8，止于acetyl-CoA）、每步主底物/产物/酶/菌以及一个去重profile，15项性状均出现（8项填写、7项明确null）；但多个CoA中间体SMILES为null，且主链精确绑定仍受BOUNDARY_REVIEW限制。按7–8档，因字段缺失和范围待核取下沿7。

<details><summary>V0.4理由与本行变化背景</summary>

路径/酶/微生物/性状/来源与不确定性五模块均涉及且步骤-酶-菌关联清楚，chosen_route_name按题面原样填；但8步中4步SMILES为null、7步EC为null，15项性状中7项为null，属&#x27;若干必要内容遗漏&#x27;落5–6档，结构完整取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_125：全图ordered_step_count=10且LINEAR_UNIQUE，仅作材料背景，不当作单条主链缺步分母。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_125：gold终点为acetyl-CoA；支持答案终点存在，不证明全路径逐步等价。
- ANSWER_TEXT / ANSWER_BEGIN：支持交付完整性、字段覆盖和缺失SMILES定位。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 下游TBA→2-methylpropane-1,2-diol→2-hydroxy-2-methylpropanal→2-hydroxyisobutyrate→CoA→3-hydroxybutyryl-CoA→acetoacetyl-CoA→acetyl-CoA总体与gold主链化学方向一致；但S1把gold的MTBE→tert-butoxymethanol→tert-butyl formate→TBA+formate缩并为MTBE→TBA+formaldehyde，且多步缺辅因子/CoA计量、S8只写一个acetyl-CoA并省略CoA，CoA中间体SMILES缺失。主干部分成立但关键连接和计量需实质修订，取5–6档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

8步主链方向与连续性成立，且tert-butanol→2-甲基丙烷-1,2-二醇→2-羟基-2-甲基丙醛→2-羟基异丁酸→2-羟基异丁酰CoA→3-羟基丁酰CoA→乙酰乙酰CoA→乙酰CoA与gold主干化学一致，终点乙酰CoA与题面/gold终点吻合；S1把MTBE直接裂解为TBA+甲醛为已知好氧机理但未标O2，S5用CoA转移酶替连接酶，多步未标NAD+/CoA/ATP，属局部计量/机理缺陷，按辅因子条款在7–8档处理不cap，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：支持gold各步底物/产物与方向；不证明答案缩并S1或省略CoA计量正确。
- ANSWER_TEXT / ANSWER_BEGIN：支持答案化学步骤、缺失辅因子和缺失SMILES定位。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 按冻结target_fact_contract：N=10；S仅S04（tert-butyl alcohol hydroxylase，已核功能匹配）=1；M为S07/S09/S10（S09为KEY_TERMINAL，S07/S10为必答MAJOR）=3；U为S01/S02/S03/S05/S06/S08=6。C=S/N=0.10&lt;0.20，按C04选&#91;1,2&#93;。C05档内取2不取1：本答案有1个已确认目标酶功能及若干名称级局部信息可用，但整体目标主链被替代/漏关键步，终点与多个必经转化未获确认，核心目标推荐仍失效。不因U自动判NE或低分，也不把未命中accepted自动判错；替代路线内部酶自洽不回填目标信用。D-KEY4：存在KEY/MAJOR缺步，上限4已满足，score=2低于上限；因confirmed_key_failure_cap为null且无独立已核催化矛盾，不另签key_error=Y。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶名与反应类型基本对应gold名称（MTBE单加氧酶、tert-butanol羟化酶、二醇脱氢酶、羟基异丁醛脱氢酶、3-羟基丁酰CoA脱氢酶、乙酰乙酰CoA硫解酶），S8 EC 2.3.1.9属gold多注集内；但7/8步EC为null、S5用CoA转移酶而gold为连接酶(EC 6.2.1.M4)、且无官方EC核验，属关键步骤缺具体核验落5–6档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_125：提供本题必答步的accepted酶名/EC及同工酶集合；支持S04的tert-butyl alcohol hydroxylase等目标酶功能级核对；不等于具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：提供目标步方向、主底物/主产物和S05→S08→S02→S04→S01→S03→S06→S10→S07→S09主链关系；支持判定替代路线与缺步，不用作具体酶实验验证。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_125：支持根物methyl tert-butyl ether与终点acetyl-CoA的本题路线边界；不证明任何中间酶。
- ANSWER_TEXT / ANSWER.steps.S1-S8.enzyme：仅证明原答案S1-S8所填酶名、EC空值/2.3.1.9及步骤产物；不产生外部科学支持，不将待核步骤转为S。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案统一使用Methylibium petroleiphilum PM1，物种/菌株身份与gold organism记录一致；gold PATHWAY_COMPLETE行taxid 105560支持PM1具备完整MTBE路径能力，故整路菌推荐有依据。扣分点是答案未给TaxID/保藏号，且逐步骤单一菌归属未逐步引用，取7–8档上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

全步归属 Methylibium petroleiphilum PM1；该物种在gold organism_gold中列为pathway_complete=TRUE(taxid 105560)，为已知MTBE完整降解菌，故单一菌承担整条路径的身份与整路径能力声称有gold支持；ncbi_taxid填null未做编号错配；仅PM1菌株级记录未单独核，落7–8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_125：支持PM1物种/菌株身份与完整路径能力；不证明每一步的酶归属均由同一菌株实验验证。
- ANSWER_TEXT / ANSWER_BEGIN：支持答案微生物身份、无TaxID及逐步菌归属定位。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 已填性状中F11 rod-shaped、F12 Gram-negative与gold观测一致；F1/F6/F7/F8/F9与PM1的MTBE降解/好氧背景大体相容，F15栖息地表述无直接观测但标low。7项明确null按诚实未知处理，主要扣分是多个已填性状缺直接trait记录且没有单位/条件扩展。取7档。

<details><summary>V0.4理由与本行变化背景</summary>

已填8项性状（F1好氧、F6好氧呼吸/O2、F7利用MTBE与TBA为碳源、F8降解MTBE、F9单加氧酶/羟化酶活性、F11杆状、F12革兰阴性、F15汽油污染地下水适应）与gold物种级记录(F1 aerotolerant、F11 rod-shaped、F12 gram negative=true)方向一致、定性准确；但温度/pH/盐度/保藏/运动/产孢/基因组7项为null(gold部分有值)，且所有性状仅INTERNAL_KNOWLEDGE_ONLY、confidence=low、无单位/定量核验，关键项证据不足落5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_125：支持PM1的rod-shaped、Gram-negative等观测；不直接支持F7 MTBE/TBA碳源或F15栖息地泛化。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_125：标识可评分观测性状与completeness-only性状；支持区分未知与错误。
- ANSWER_TEXT / ANSWER_BEGIN：支持已填/null性状值与confidence定位。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> EVID_001/EVID_002均为INTERNAL_KNOWLEDGE_ONLY，无database、record_id、DOI或可定位locator；仅给出内部claim_scope。按D5六状态，决策相关组均为MISSING_SOURCE，属于几乎无法定位重要结论依据的低分档；无已核实错引，故不cap，取1–2档上沿2。

<details><summary>V0.4理由与本行变化背景</summary>

答案仅有INTERNAL_KNOWLEDGE_ONLY自述两条evidence(EVID_001/EVID_002)，database与record_id均null，无可定位数据库条目、DOI或计算记录；决策相关组(CG01/02/03/05/07)全部MISSING_SOURCE，按P34低分档；无已核实错引不cap，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案实际交付来源仅为内部知识、无外部可定位条目。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确写出氧条件未指定、按好氧已知体系填写；多数EC缺失、CoA下游步骤低置信、多个性状未知均列入uncertainties，EVID_001/002也标INTERNAL_KNOWLEDGE_ONLY与low/medium。没有系统性把预测写成实证，也没有掩盖主要矛盾；仅complete_pathway与部分性状表述略强，取8档。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties列出氧条件假设、缺EC、CoA步骤低置信、性状未知4项；酶/菌confidence分medium/low、未知性状标unknown；route_scope.notes披露好氧假设；未把预测写成实证。不足：未披露与gold不同的首步替代路线(alternative_branches为空)，对单一路线&#x27;已知主链&#x27;表述略强。落7–8档取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持答案对氧条件、EC缺失、低置信步骤和未知性状的披露。

</details>

## Grok

答案SHA256：`765a91fce6f2c45d39cbf16da2b72cf45817ed94a3d23e39e93b69c054e3bbeb`。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求指定 methyl tert-butyl ether degradation 主链至 acetyl-CoA，并逐步给酶、EC、微生物及每 profile 的15项性状。答案 JSON 可读且结构完整，给出8步底物/产物/酶/微生物和两个 organism_profiles 的全部15项字段；但相对任务冻结的10步主链，只覆盖多数步骤，缺少 tert-butoxymethanol 脱氢与 tert-butyl formate deformylase 等必经段，并把 tert-butyl formate 支路列为 alternative、首步直接写 MTBE→叔丁醇+甲醛；同时若干性状为诚实 null/unknown。属于主要模块均有涉及但若干必要内容遗漏、需实质修订的5–6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_125：冻结任务信息显示该路线 ordered_step_count=10、LINEAR_UNIQUE；用于核对主链任务长度为10步，不证明答案每步科学正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：gold切片显示 MTBE 经 tert-butoxymethanol、tert-butyl formate 等至叔丁醇后进入下游主链，并最终到 acetyl-CoA；用于指出答案省略/改写的前段必要步骤，不把gold当穷尽路线。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案原文显示实际交付8步、两个菌株profile及15项性状字段；不证明其步骤均与冻结主链一致。

</details>

### D2 反应化学科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按答案自身路径，MTBE 起始单加氧/半缩醛分解后进入叔丁醇，再经羟化、醇脱氢、醛脱氢、辅酶A连接、钴胺素依赖变位酶、3-羟基丁酰辅酶A脱氢和硫解到 acetyl-CoA；方向为污染物向终点，碳骨架连续，未见明确反向、严重断裂或明显原子不守恒。主要扣分点是首段采用直接 TBA+甲醛并跳过 gold 的 tert-butoxymethanol/tert-butyl formate 段，S1/S2 的中间体与酶表达较简化，部分辅因子、SMILES和立体信息未完整列出；这些属于主链成立下的局部修订问题，D2 取7而非上限8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_125：冻结案例根身份显示起点为 Methyl tert-butyl ether、终点为 acetyl-CoA；用于核对答案的整体方向与终点。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：gold主链显示 tert-butoxymethanol→tert-butyl formate→tert-butanol→2-methylpropane-1,2-diol→2-hydroxy-2-methylpropanal→2-hydroxyisobutyrate→2-hydroxyisobutyryl-CoA→3-hydroxybutanoyl-CoA→acetoacetyl-CoA→acetyl-CoA 的方向与连接；用于对比答案前段的直接支路及下游连续性。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案原文显示其实际反应步骤、方向、产物与对直接分解/替代支路的说明；不自动证明其全部化学细节已核验。

</details>

### D3a 目标反应与酶对应：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按accepted set与gold逐步反应核对：S06(ligase)、S07(3-hydroxyacyl-CoA dehydrogenase, EC1.1.1.35)、S09(acetyl-CoA acetyltransferase, EC2.3.1.9)、S10(mutase)等下游对应较清楚；但S02(tert-butyl formate deformylase)与S08(tert-butoxymethanol dehydrogenase)在答案中未作为评分主链步骤交付，答案把叔丁基甲酸酯支路放入alternative_branches且is_part_of_scored_main_route=false，S1则直接写MTBE-&gt;TBA+formaldehyde。S02/S08为预定义KEY/MAJOR目标步，确认的KEY漏交付触发D-KEY4上界≤4；4是最高许可，不因其余步骤较多而抬分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 765a91fce6f2c45d39cbf16da2b72cf45817ed94a3d23e39e93b69c054e3bbeb：定位答案实际steps、酶名/EC、mapped目标步与alternative_branches声明。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_125：提供各目标步accepted酶名/EC集合；支持S06/S07/S09/S10等名称/EC核对，不证明任意具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：提供S02/S08目标反应及主链顺序；支持确认答案未在主链交付这两个反应。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_125：ordered_step_count=10且LINEAR_UNIQUE，用于说明本题10个必答目标步的材料范围；不把全DAG旁支并入单主链。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 两个profile使用M. petroleiphilum PM1与A. tertiaricarbonis L108，均为gold/organism_gold可定位的MTBE/叔丁基化合物相关菌；PATHWAY_COMPLETE记录支持PM1与A. tertiaricarbonis的整路能力。扣分点：PM1 TaxID 420662与gold中105560的粒度/记录对应未核，L108 TaxID为null；S03/S04等步的菌株归属在organism_gold中对应Mycobacterium spp.而非PM1，答案用PM1整路能力作关联但缺少逐步直接证据。整体属主微生物对应可靠、少量具体身份/步级归属待确认，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 765a91fce6f2c45d39cbf16da2b72cf45817ed94a3d23e39e93b69c054e3bbeb：定位答案PM1/L108身份、TaxID、step-level归属和complete_pathway_organism_profile_id。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_125：提供逐步菌株记录与PATHWAY_COMPLETE菌株；支持PM1、A. tertiaricarbonis相关性与步级归属差异，不证明任意菌株所有步骤实验活性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_125：辅助说明各步accepted酶记录；不把酶记录自动升级为菌株全路能力。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 两个profile均返回15项性状，明确null按未知处理，未把缺项当错误；氧关系、革兰氏、产孢、温度偏好等多项与gold/常识一致。已核冲突：ORG_002 A. tertiaricarbonis L108的F11_cell_morphology写作“杆状”，trait_gold为oval-shaped；PM1的F5 ATCC BAA-1232、F14 CP000555及若干high-confidence性状缺少冻结trait记录支持。整体属部分性状准确且适用、关键项证据不足/局部冲突，取5–6档中的6，因支持部分与错误边界已可读。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 765a91fce6f2c45d39cbf16da2b72cf45817ed94a3d23e39e93b69c054e3bbeb：定位各profile 15项性状、confidence、null与raw_text声明。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_125：提供A. tertiaricarbonis oval-shaped、PM1部分性状与genome记录；支持一处形态冲突和若干未支持字段，不把UNKNOWN当错误。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_125：区分observed_accuracy与completeness_only；支持仅对可评分子字段作准确性判断。

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry六条全部source_type=INTERNAL_KNOWLEDGE_ONLY；虽给出作者/年份/期刊与claim_scope，并把EVID映射到steps/traits，但没有DOI/稳定条目定位、数据库retrieved record或原文片段，不能算条目级可核对来源。E0仅有与本题不直接相关的EC 1.1.1.31记录，未发现已核实错引，因此不触发D5 cap；按来源缺失/笼统与弱条目对应定3–4档，因claim映射较明确取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 765a91fce6f2c45d39cbf16da2b72cf45817ed94a3d23e39e93b69c054e3bbeb：定位答案实际交付的来源登记、claim_scope与INTERNAL_KNOWLEDGE_ONLY声明。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案用uncertainties、confidence与null系统披露未知：明确题面未指定氧条件、直接裂解/叔丁基甲酸酯支路选择、酶基因/EC未核实、性状raw_text未核对且非数据库检索。主要限制与待验证点写得具体；少量高置信性状（如F7/F8）与一处L108形态冲突未获支持，属局部过度确信而非系统性误导。取7–8档中的8，因整体证据性质标注与范围说明较充分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 765a91fce6f2c45d39cbf16da2b72cf45817ed94a3d23e39e93b69c054e3bbeb：定位不确定性说明、confidence标签、null与支路声明；不作外部事实证明。

</details>

## GPT5.6

答案SHA256：`46ac1a477a428abddd6c58a057e4b0021752edc72509ba4162387bc0bdd0370b`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案仅交付steps S1–S4，任务合同n_required=10的十条必答主链中缺少金标S05入口、S06/S07/S08/S10中间步及S09终点acetyl-CoA；每步酶均未给EC；15项性状虽列全但绝大多数为空/null，仅F8/F9有低置信文本。路线名与氧条件回显正确，但核心任务模块大部缺失，D1关键错误成立；表现符合3–4分档中仅少数必要模块完成、多处缺步骤/酶菌关联/性状的情形，取该档下沿3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_125：n_required=10、ordered_step_count=10；用于确认本题必答主链长度，不把全图旁支当额外缺步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：金标主链S05入口、S08/S02/S04/S01/S03/S06/S10/S07/S09终点acetyl-CoA；用于核对答案缺步与终点，不判断替代S1化学正确性。
- ANSWER_TEXT / ANSWER：答案实际交付仅4步且无acetyl-CoA终点、多数性状为空；仅支持交付完整性事实，不替代科学正确性判断。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 交付的四步化学骨架大体成立：S2（tert-butanol→2-methyl-1,2-propanediol）对应金标S04，S3对应S01，S4对应S03；S1为MTBE直接氧化裂解为tert-butanol+formaldehyde，C5H12O→C4H10O+CH2O计量可成立，但并非金标S05→S08→S02的连续主链。自2-hydroxyisobutyric acid之后到acetyl-CoA的S06/S10/S07/S09全部缺失，关键中间体、连接和终点不完整。属于主干部分成立但关键转化/连接仍需实质修订的5–6分档，边界尚不足以进入7–8分档，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：金标线性主链为S05→S08→S02→S04→S01→S03→S06→S10→S07→S09至acetyl-CoA；支持答案S1替代入口及后段缺步的定位，不把与gold不同本身判为化学错误。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_125：金标各步酶名/EC用于核对答案所给酶名称与反应方向；G4支持不等于具体蛋白实验活性。
- ANSWER_TEXT / ANSWER：答案仅含4个连续步骤且缺少后段中心代谢接入；支持D2连续性/完整性的局部评估。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 10个必答目标反应中，答案仅对S04/S01/S03给出可辨认酶名对应（分别为答案S2/S3/S4），但EC均null，名称–EC配对与相应粒度支持未核，按U；S02/S05/S06/S07/S08/S09/S10未交付，按M；其中S05为KEY_ENTRY、S09为KEY_TERMINAL，事实上确证缺失。无任何目标反应达到S；答案S1为MTBE直接裂解为TBA+formaldehyde，不对应金标S05 MTBE→tert-butoxymethanol，不记目标信用。主要目标酶对应和关键入口/终点均不成立，D3a主要结论失效并受关键缺失上界约束，落1–4受限范围；可用候选仅少数、主要失效边界可辨，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_125：金标各必答步的accepted酶名/EC用于核对答案酶对应；仅支持功能/EC粒度，不证明具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_125：金标目标反应、方向与S05入口/S09终点；用于确认答案缺失目标和关键步，不把替代S1回填目标信用。
- ANSWER_TEXT / ANSWER：答案仅给出4步酶名且均无EC；后6个必答步及S05/S09关键步未交付；支持U/M分类与缺失定位。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Methylibium petroleiphilum PM1身份与gold TaxID 105560/ PATHWAY_COMPLETE相符，全路径能力有profile级支持；但答案把PM1用于所有四步，其中对应S01/S03的步骤在organism_gold逐步行中未列PM1，且未给TaxID/基因组号。身份层大体可靠、若干步级归属未充分核验，落5-6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_125：支持PM1物种/菌株身份及PATHWAY_COMPLETE=True；不自动支持答案中每个具体步骤均由PM1催化。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_125：支持部分步骤的酶-菌关联事实；不能推广到未列出的菌株-步骤组合。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项结构中仅F8/F9填有内容，且均为INTERNAL_KNOWLEDGE_ONLY/low；F8“可降解MTBE及相关醚类或石油烃”与F9“MTBE初始氧化相关单加氧酶活性”方向合理，但trait_gold对PM1没有直接逐项支持，其他13项明确未知/null。null的完成度问题归D1；D4按已给内容落5-6档，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_125：PM1的F8/F9无直接逐项匹配的观测条目；F8/F9仅可作有限背景核验，不自动确认答案的广义表述。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_125：显示PM1哪些性状子字段可评分；未观测项不应被当作已核实数值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案只有EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null，claim_scope虽列三条但无法定位到条目或文献。决策相关组（路线/反应、酶、微生物身份、全路径能力）均为MISSING_SOURCE；无已核实错引，按缺失低档取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry&#91;0&#93;：显示仅有INTERNAL_KNOWLEDGE_ONLY来源；不提供可定位数据库/文献记录。
- RUBRIC_CLAUSE / C08：D5只评价实际交付来源；评分者新增gold不能回填为模型证据。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确把证据标为INTERNAL_KNOWLEDGE_ONLY/low，route_scope氧条件保持null，uncertainties列出EC未定、氧条件未指定、下游未纳入，未用编造EC或数值填充未知。route_summary略强但主要限制已披露；落7-8档，取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示答案主动披露氧条件、EC和下游边界未定；不证明科学内容正确。
- RUBRIC_CLAUSE / C06：D6按证据性质、不确定性与结论边界独立评价，不因D5来源缺失自动cap。

</details>
