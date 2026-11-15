# BIOPATH150_090：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：cinnamate and 3-hydroxycinnamate degradation to 2-hydroxypentadienoate

污染物：Cinnamate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 52.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 39 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 45 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 41.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 47 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 25.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`c14ce13d9b5ef4e3568f119b2069a11055df3733d2140dab10a0b094f383b521`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 题目要求的路线名、逐步酶/EC/微生物与15项性状均以可解析JSON交付，终点2-hydroxypentadienoate出现；但程序路线诊断为DEVIATES且D1_task_range限&#91;1,4&#93;，主链/分支化学表示在S03/S04出现非匹配，故取受限范围上沿4；不另签独立D1关键错误。

<details><summary>V0.4理由与本行变化背景</summary>

5个step均给出底物/产物（含name与SMILES）、enzyme、microorganism、predecessor与branch_id；单一organism_profile按物种+菌株去重覆盖全部15项性状；evidence_registry 4条；route_scope.chosen_route_name与题面路线名逐字一致；分支步S5以branch_id+alternative_branches(is_part_of_scored_main_route=false)明确声明不属评分主链。主要模块实质回应、关联清楚，仅EC编号在S1/S2/S4/S5留null（题面允许未知留null，但相对题面‘首选酶及EC’属字段级遗漏），故落7–8档、取偏高8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案实际交付的路线名、步骤、酶/微生物与15项性状；不证明其科学正确性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_090：冻结案例为5步分支DAG；不等于要求交付全部旁支或赋予目标反应信用。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 主碳骨架（cinnamate→dihydrodiol→2,3-dihydroxycinnamate→ring cleavage→2-hydroxypentadienoate+fumarate）及各步方向总体成立；但程序将S03/S04判为STEREO_CONFLICT_SPECIFIED，S3反应类型文字称“间位/extradiol”又写“1,2-键断裂”，若干H+/辅因子省略，故在允许的D2_chemical_range&#91;1,5&#93;内取上沿5，而非更高。

<details><summary>V0.4理由与本行变化背景</summary>

肉桂酸主链四步与gold S04→S03→S05→S02化学一致：2,3-双加氧得顺式二氢二醇、NAD+依赖脱氢再芳香化得2,3-二羟基肉桂酸、间位裂解得2-羟基-6-氧代壬-2,4,7-三烯二酸、C-C水解得2-羟基戊二烯酸并副产延胡索酸；终产物与gold terminal（Fumarate、(2Z)-2-hydroxypenta-2,4-dienoate）一致；分支S5（3-羟基肉桂酸→2,3-二羟基肉桂酸）与gold S01同一节点汇入并已声明不属评分主链。局部缺陷：多步未列H+，S5以NADPH对应gold的NADH——按辅因子/简化反应式条款属局部计量缺陷，落7–8档，取上段8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案给出的底物、产物、方向与反应类型；不证明立体化学或EC完全正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：提供冻结gold的方向、底物/产物与角色；不自动验证答案全部立体表示。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：给出各步参考酶与EC；不证明答案的具体酶名/EC均已正确。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分7 → V0.5新分1，变化-6。

新裁判理由：

> 固定事实S=0、F=2（S03/S04）、U=3（S01/S02/S05）；S04为确认KEY入口失败，D-KEY4上界4。已核失败不存在可计入的S，覆盖率为0，按C04/C05落于&#91;1,2&#93;；选择1：核心入口骤败且无已核目标催化对应，局部U不能转成目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶的名称/基因与gold对应酶一致：S1的hcaA1/hcaA2/hcaC/hcaD对应gold HCAMULTI-CPLX（putative 3-phenylpropionate/cinnamate dioxygenase）；S2的hcaB对应PHENPRODIOLDEHYDROG-MONOMER；S3的mhpB对应间位裂解双加氧酶；S4的mhpC对应2-hydroxy-6-oxononatrienedioate hydrolase；分支mhpA亦为羟化酶类。缺陷：仅S3给出EC=1.13.11.84，而gold同反应为1.13.11.16，E0无EC 1.13.11.84冻结记录（GAP-090-005），按四.5/四.6只能记UNRESOLVED待核、不判错；S1/S2/S4/S5的EC留null。酶-反应对应有可靠名称支持而EC核验不足，取7–8档下段7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案交付的酶名/EC及其与步骤的对应；不证明目标反应完成。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：显示gold目标反应与方向；用于定位S03/S04非匹配与S05待核，不扩展到未声称内容。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：显示参考酶/EC；不证明答案EC 1.13.11.84正确。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 答案所有步骤均用Escherichia coli K-12 substr. MG1655（TaxID 511145）；gold步级/整路微生物为Escherichia coli（562，species-level）并列PATHWAY_COMPLETE for E. coli，物种身份相符。但K-12菌株级身份、511145和ATCC 700926未在E0冻结核验，整路能力仅由综述/内部知识支撑，故取7档（良好但菌株级/能力粒度仍需确认），不判为跨属或全路错误。

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤归属单一Escherichia coli K-12 substr. MG1655 profile（符合‘同一菌去重’），物种与gold步级organism（Escherichia coli，EXACT，taxid 562）一致；gold PATHWAY_COMPLETE亦列E. coli（562）为整路径菌，支持物种级全路径能力声称；菌株级身份（K-12 MG1655、taxid 511145）在E0无记录（GAP-090-025），且实验菌株与gold代表记录不同——按四.4同物种代表记录条款不因此判错；未见仅凭序列存在性直接外推整条路径的表述（hca/mhp基因簇与整路径能力均单列）。取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案交付的统一菌名、菌株和TaxID；不证明菌株级身份或整路能力已核验。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_090：显示gold步级为Escherichia coli（562，species-level）并有E. coli整路能力记录；不验证K-12 MG1655的TaxID 511145或菌株级完整能力。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 15项性状全部给出，多项与gold物种观测一致：运动性、革兰氏阴性、无芽孢、杆状、兼性厌氧/氧耐受、非嗜盐类别；但温度上下限、pH范围、F5保藏号、F8/F15等仅EVID_002内部知识或EVID_001综述，F2/F3/F4若干子字段在scoreability mask为pending/completeness_only，F14 NC_000913未在E0，故取7档而非更高；未发现可核关键性状离谱到误导筛选。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部按结构交付（无遗漏、无整项null）：运动性true、杆状、革兰氏阴性、不产芽孢、兼性厌氧、盐度非嗜盐、温度偏好中温均与gold物种级观测记录一致；F2/F3/F4端点值按trait_subfield_scoreability_mask/trait_subfield_scoreability_mask属pending_teacher_adjudication或completeness_only（F3整项completeness_only），本轮不据此判错；F5(ATCC 700926)、F14(NC_000913/4,641,652 bp/50.8%)、F7/F8/F9芳香底物利用与MhpB/MhpC酶活声称在E0无冻结记录（GAP-090-061~079）→UNRESOLVED；温度上限45℃高于gold观测上限35–41℃但该子字段待裁决。综合落7–8档下段。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案实际填写的15项性状及confidence/evidence_id；不证明全部数值。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_090：提供E. coli物种级观测/预测背景；不自动验证K-12菌株级全部字段。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_090：显示哪些性状/子字段可作为observed_accuracy或仅completeness_only；不改变答案原值。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_090：显示部分数值子字段pending teacher adjudication或completeness_only；用于限制D4不能给更高档。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 核心路线/酶/微生物/部分性状有EVID_001完整文献题录与EVID_004 MetaCyc路径名，但E0无相应冻结记录可核对；EVID_002对多数性状为INTERNAL_KNOWLEDGE_ONLY，EVID_003 NC_000913在E0为GAP；无已核实错引。核心组来源可定位但未核，辅助组缺失/笼统，故给5档（部分可定位、仍需核验/映射），不触发cap。

<details><summary>V0.4理由与本行变化背景</summary>

证据框架完整（4条EVID、claim_scope与逐条confidence），核心结论有可定位的条目级线索：Diaz等2001综述带作者/期刊/卷期页，NC_000913为条目级访问号，MetaCyc给路线名——故不落‘全部仅笼统来源’的3–4档；但E0对本案无claim关联记录（79个gap：综述自由文本GAP-090-016、NC_000913 GAP-090-003、MetaCyc GAP-090-023、EC 1.13.11.84 GAP-090-005），全部决策相关组只能记UNRESOLVED_SOURCE，性状组为INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE），MetaCyc无record_id（GENERIC_SOURCE）；E0两条记录（P. putida 12880与taxid 303）与本答案无关，无任何经核实错引→severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION、不cap。按‘保留低分+待核’取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案实际交付的文献/数据库/内部知识来源形态与claim_scope；不构成冻结核验。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案逐步骤给uncertainty，明确EC未定/记忆值、ATCC/TaxID记忆值、MhpB/MhpC证据有限，区分LITERATURE_DIRECT/DATABASE_DIRECT/INTERNAL_KNOWLEDGE_ONLY及confidence；主要限制与待核点具体。仅少量内部知识性状仍标high/medium，但无系统性把预测写成实证或掩盖矛盾，取8档。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体：EC编号不确定、MhpB/MhpC对不饱和底物的证据有限、hca对肉桂酸底物特异性、ATCC/TaxID为记忆值、温度/pH为教科书常识值未逐项核对，均逐条列出；证据性质以source_type分栏（LITERATURE_DIRECT/DATABASE_DIRECT/INTERNAL_KNOWLEDGE_ONLY），预测与观测未被系统性混淆；但F1/F6/F11/F12/F13以high置信度绑定INTERNAL_KNOWLEDGE_ONLY且无逐字段‘记忆值’提示，F2数值未标条件来源——属单点式过度确信而非系统性误导，档内扣分不cap。取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案对证据性质、未知和限制的披露；不证明披露内容本身正确。

</details>

## DeepSeek

答案SHA256：`f6e02856afaba89e45d56421de776c712ceba2757acc4fcc35bd3310e98bd8c5`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 交付模块齐全（4步、酶、菌、15项性状），但实际路线并非题面/gold锁定主链：S1用cinnamate羟化到3-hydroxycinnamate替代gold S04的cinnamate dioxygenase入口，且gold S03二氢二醇脱氢酶步缺失。路线诊断DEVIATES，任务偏离按D1关键错误封顶；因模块交付完整，取封顶内上沿4。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的模块均已实质交付：4步主链（Cinnamate→3-Hydroxycinnamate→2,3-Dihydroxycinnamate→C9开环产物→2-Hydroxypentadienoate+马来酸），每步均有底物/产物英文名与SMILES、一个酶（2/4步带EC，题面允许未知填null）、一个对应微生物；route_scope.chosen_route_name逐字为题面指定路线名，氧条件维持null未改动；单一profile按物种+菌株去重，题面要求的15项性状全部出现（13填写+2显式null）。仅少量缺陷：S1、S4缺EC；未声明3-hydroxycinnamate这一root的分支处理。未更换指定路线名/条件，不构成任务参数偏离的关键错误，化学层问题归D2另评。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT#BIOPATH150_090：题面锁定route name与15项性状交付要求；不证明答案实际路线正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：gold S04为cinnamate dioxygenase入口，S03为二氢二醇脱氢酶步；不支持答案S1的羟化替代。
- ANSWER_TEXT / ANSWER_TEXT#steps：答案S1-S4展示实际交付路线与模块清单。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 羟化、双羟化与meta开环的碳骨架转化大体可成立，终点2-hydroxypentadienoate也交付；但S4水解把gold的fumarate写成maleate，属显式立体化学冲突，按D2≤5；S1入口替代与部分EC/结构未核使只能取5。

<details><summary>V0.4理由与本行变化背景</summary>

化学骨架成立：2,3-二羟基肉桂酸经EC 1.13.11.16开环生成C9三烯二酸、再水解为2-羟基戊二烯酸，与gold的S05→S02下游方向一致；终点即题面指定2-hydroxypentadienoate；C9→C5+C4的碳骨架分配与水解计量自洽，无原子明显不守恒。问题：①cinnamate首步被替换为未声明的单加氧羟化（cinnamate 3-monooxygenase），gold记录的是双加氧活化（EC 1.14.12.19）＋脱氢（EC 1.3.1.87），答案既未声明替代路线也未给可核证据；②水解副产物写成马来酸（顺式），gold为延胡索酸（反式）；③O2/NADH等辅因子未列（局部计量缺陷）。上述偏离未推翻“cinnamate→2-hydroxypentadienoate”这一主要结论，按四.5第4步“否→档内扣分”，不cap；5–6档中问题较多，取5–6档偏上的6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：gold S02水解产物为(2Z)-2-hydroxypenta-2,4-dienoate与Fumarate；S05给出C9开环中间体。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：gold S02为2-hydroxy-6-oxononatrienedioate hydrolase；不证明答案S4的maleate副产物。
- ANSWER_TEXT / ANSWER_TEXT#steps：答案S1-S4展示羟化、双羟化、开环与水解；S4给出Maleate而非Fumarate。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> release目标事实为S=0、F=1、U=4，S04为已确认KEY入口目标失败并触发D-KEY4≤4。没有已支持的S目标；S03在矩阵为MISSING/未绑定，其余S01/S02/S05为ALIGNMENT_NOT_CONFIRMED。基于核心KEY失败、无可确认目标催化对应，在&#91;1,4&#93;内取1。

<details><summary>V0.4理由与本行变化背景</summary>

四步均有酶候选，S3的EC 1.13.11.16与gold该开环步骤同号、反应类型（双加氧开环）一致，属合理候选；但①S3把该酶命名为“2,3-dihydroxycinnamate 1,2-dioxygenase”，1,2-（intradiol）与其所交付的三烯二酸（meta-cleavage型）产物及gold记录的2,3-dioxygenase名称不符，属名称与EC/反应类型不一致的局部矛盾；②S1“cinnamate 3-monooxygenase”与S4水解酶均无EC，关键步骤缺具体核验；③EC 1.14.13.151与EC 1.13.11.16在E0中均无冻结记录（GAP-090-007/013、004/010），不得凭记忆放行或判错。无经核实使主要酶推荐失效的矛盾，故不cap；属“有合理候选和部分支持，但若干关键步骤仍缺具体核验”5–6档，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：S04为cinnamate dioxygenase入口；gold S04产物与答案S1产物不同，支持确认性入口失败。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：gold accepted S04为EC 1.14.12.19；该记录支持gold目标，不证明答案S1的cinnamate 3-monooxygenase。
- ANSWER_TEXT / ANSWER_TEXT#steps：答案S1-S4给出实际酶/EC与底物产物；S1替代了S04入口转化。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案统一推荐Pseudomonas putida KT2440（TaxID 160488）并声明complete_pathway_organism_profile_id=ORG_001，但E0无KT2440菌株级身份/单步能力/全路径能力记录；gold步级菌为E. coli，全路径完成者为E. coli/R. globerulus。P. putida为合理芳香物降解候选，但菌株级能力与全路径声称未核，不能判已证伪，故取5–6档下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

菌名Pseudomonas putida为真实物种：E0 taxid:303记录（rank=species，CURRENT）支持物种级学名；但菌株KT2440与TaxID 160488在E0无冻结记录（GAP-090-024/026），记录明确“种级记录不核实菌株”，故菌株级身份仅粒度不足、非已核实错配。四步的反应级能力全部只挂INTERNAL_KNOWLEDGE_ONLY（EVID_002），complete_pathway_organism_profile_id=ORG_001的整条路径能力声称无任何外部证据；gold侧的E. coli只是参照来源之一，不能据此判答案错。不存在已核实的跨类群/异菌株推翻主要微生物推荐的证据，故不cap；属“有合理候选和部分支持，但关键身份与作用范围未充分核验”5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_090：gold步级菌为E. coli（TaxID 562），PATHWAY_COMPLETE为E. coli/R. globerulus；gold非穷尽，不证明P. putida KT2440不能。
- E0_EVIDENCE / f3e0:bacdive:12880：该记录为P. putida mt-2 PaW1（DSM 3931等），不是KT2440；不支持KT2440菌株级能力。
- E0_EVIDENCE / f3e0:taxid:303：该记录为P. putida物种级TaxID 303；不自动支持KT2440（TaxID 160488）或全路径能力。
- ANSWER_TEXT / ANSWER_TEXT#organism_profiles：答案将全部步骤归到ORG_001 P. putida KT2440并声称全路径。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项性状均出现，F4/F5为显式null/unknown；其余13项以INTERNAL_KNOWLEDGE_ONLY的EVID_002填medium，包含温度范围、pH范围、基因组登录号与数值。E0无P. putida KT2440（TaxID 160488）菌株级性状记录，无法逐项核验；数值大体合理且未发现与gold P. putida记录直接矛盾，但证据不足与适用范围问题阻止高档，取5–6档下沿5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全（13填写+盐度、保藏号2项显式null），数值在P. putida物种层面大体合理（革兰氏阴性、杆状、极生鞭毛运动、不产孢、专性需氧、嗜温、基因组约6.18 Mb/GC 61.5%），无单位/量纲明显错乱；但全部仅挂INTERNAL_KNOWLEDGE_ONLY，raw_text全为null、置信一律medium，E0对KT2440的性状无任何记录（GAP-090-029…044，均NO_TRAIT_RECORD_IN_SNAPSHOT），无一项可核；F8把“甲苯、二甲苯”降解写入KT2440，而E0唯一菌株卡为mt-2 PaW1(pWWO)且明示“种级记录不核实菌株、培养温度不证明最适”，该菌株级底物谱属可疑外推；F14给出具体登录号NC_002947.1亦未核。属“部分性状准确且适用，但关键项证据不足、条件解释需修订”5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_090：trait_gold只给E. coli与R. globerulus；无P. putida KT2440，故不能支持答案性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_090：可评分mask覆盖E. coli与R. globerulus；不含KT2440，说明本题冻结性状参照未覆盖答案菌株。
- E0_EVIDENCE / f3e0:bacdive:12880：记录为P. putida mt-2 PaW1，培养温度26/30°C，不是KT2440；不能回填为KT2440性状。
- ANSWER_TEXT / ANSWER_TEXT#organism_profiles：答案给出13项填值、2项unknown及confidence=medium。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry仅有EVID_001/EVID_002，source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null；步骤、酶、菌、性状最多回指这两个内部桶，不能定位外部条目或计算记录。无已核实虚构/错引，故不cap；属MISSING_SOURCE低档，因仍有内部claim映射但不具备可追溯外部依据，取2。

<details><summary>V0.4理由与本行变化背景</summary>

答案的全部结论只挂在EVID_001/EVID_002两条source_type=INTERNAL_KNOWLEDGE_ONLY的自建条目上，database/record_id/locator全为null，claim_scope仅“pathway steps”“organism traits”，无任何条目级可定位可核对的证据；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09/CG17）全部MISSING_SOURCE。无引用即不存在已核实错引（无VERIFIED_MIS_CITATION_*），按四.3/P34“MISSING_SOURCE是缺失而非误导，默认不触发cap”，故key_error=N。D5属“几乎无法定位重要结论依据”1–2档，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#evidence_registry：答案仅登记INTERNAL_KNOWLEDGE_ONLY证据，无数据库条目/文献定位。
- E0_EVIDENCE / f3e0:bacdive:12880：E0可提供P. putida mt-2 PaW1记录，但答案未引用该记录，不能回填其来源。

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案在多数具体酶、菌、性状与基因组数值上统一标medium confidence，但证据源为INTERNAL_KNOWLEDGE_ONLY、raw_text为空、uncertainties为空，未说明主要限制或待核点；仅F4/F5标unknown。证据类型在registry中有所披露，故非系统性把预测写成实证；但多处结论强度超过依据，取3–4档偏高4。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties为空数组、全部raw_text为null、无任何限制或待验证点说明；四步（含S3酶标high）与13项性状一律以medium置信呈现，并给出具体登录号NC_002947.1与数值区间，未区分观测/预测/推断，结论强度普遍超过依据。有限正面之处：source_type=INTERNAL_KNOWLEDGE_ONLY如实标注了证据性质，F4/F5两项诚实置null+unknown，未见掩盖已知矛盾或虚构来源。属“多处过度确信、主要限制未说明”3–4档，非系统性误导（不cap），取4。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#confidence：答案统一给medium confidence且uncertainties为空；仅少数性状null/unknown。
- RUBRIC_CLAUSE / RUBRIC_CLAUSE#P119：D6区分单点过度确信与系统性误导；本答案有披露INTERNAL_KNOWLEDGE_ONLY但限制说明不足。

</details>

## Kimi

答案SHA256：`344a09ae516cc1dacdfdcbad6abeea743a7d9fd8fa70d96089b0e469537dba9b`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 主模块均有交付：4步主链、酶、菌、15性状和不确定性说明均在；但将题面路线名中的3-hydroxycinnamate仅列为不评分支路，且未建立当前认可主链绑定，不能视为完整符合全部命名路线范围。按D1允许&#91;1,4&#93;取4：模块覆盖较好但路线完整性/符合度仍有实质缺口。

<details><summary>V0.4理由与本行变化背景</summary>

任务要求的模块全部实质交付：4步主链（S1–S4）每步含主底物/主产物的英文名与SMILES、一个首选酶、一个对应微生物，且predecessor_step_ids首尾相连；route_scope.chosen_route_name逐字为题面路线名，未改选路线，氧条件如实保留null；organism_profiles按物种+菌株一条并一次返回15项性状，无合并错乱。扣分点：S2/S3的EC按题面规则诚实填null（4步中2步无EC）、F4盐度数值与F3上下限未引用，属少量字段级缺口，定在8档而非更高。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_090：Gold为BRANCHED_DAG、5个ordered steps；不能把全部旁支自动当主链必答分母，但可用于核对题面路线范围和终点。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_090：题面路线含cinnamate与3-Coumarate入口，终产物为Fumarate与(2Z)-2-hydroxypenta-2,4-dienoate；仅支持范围核对，不证明答案路线已绑定。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 肉桂酸主支的连通性总体接近gold：cinnamate→二氢二醇→二羟基肉桂酸→开环C9中间体→2-hydroxypenta-2,4-dienoate/fumarate；但SMILES/名称在立体化学与电荷表示上有冲突，末端产物未写(2Z)，且fumarate被标为byproduct而gold列为MAIN_PRODUCT。未发现方向反转或原子明显不守恒等D2关键错误；在D2允许&#91;1,5&#93;内取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步对应：S1芳环顺式二羟基化（cinnamate→cis-二氢二醇，等价于gold的3-(cis-5,6-dihydroxycyclohexa-1,3-dien-1-yl)prop-2-enoate）、S2顺式二醇脱氢复芳构化为(E)-3-(2,3-dihydroxyphenyl)acrylate（=2,3-dihydroxy-trans-cinnamate）、S3外二醇开环得2-hydroxy-6-oxonona-2,4,7-trienedioate、S4水解得2-hydroxypenta-2,4-dienoate并释放fumarate；方向全为正向，终点与题面指定终点一致，连接性与SMILES可辨。扣分点：四步均未列O2/NADH/NAD+/H2O，字面计量不成立，按八.辅因子条款属局部计量缺陷（7–8档），不cap；fumarate被标为byproduct而gold标MAIN_PRODUCT，属角色标签差异而非化学冲突；S1立体化学未标注。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：Gold反应行给出主链方向、底物/产物、末端Fumarate为MAIN_PRODUCT及立体/表示信息；支持化学连通性核对，不证明答案表示完全一致。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> 程序事实为S=0、F=4、U=1，confirmed_target_rate=0.0；S02与S04为已确认KEY失败，D-KEY4上限4保留。答案对S04给出accepted EC 1.14.12.19、对S02给出3.7.1.14，存在有限局部酶-EC可用信息，但路线步NONMATCH使目标信用被阻断；S01 alignment未确认。C=0落在低带&#91;1,2&#93;，取2而非1是因为仍有少量可定位的accepted酶-EC对应；不把KEY上限机械写成4。

<details><summary>V0.4理由与本行变化背景</summary>

已给的两个EC与gold完全对应且酶名-反应类型自洽：S1 3-phenylpropionate/cinnamate dioxygenase EC 1.14.12.19（gold S04同号）；S4 2-hydroxy-6-oxonona-2,4,7-trienedioate hydrolase EC 3.7.1.14（gold S02同号），且答案自述该EC接受名对应饱和类似物，属诚实限定。S2脱氢酶与S3外二醇双加氧酶的EC按规则填null（gold分别为1.3.1.87与1.13.11.16），属关键两步缺具体核验，落在7–8档；无EC大类别错配、无酶名与EC互相矛盾，故取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：Gold酶行给出S02=3.7.1.14、S04=1.14.12.19等accepted关系；仅支持功能/编号对照，不证明具体蛋白实验活性或路线步结构已匹配。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 物种层E. coli与gold各步organism行一致，单步菌归属有物种级支持；但答案过度具体化为K-12 MG1655、TaxID 511145、ATCC 700926，并对该菌株声称complete_pathway_organism_profile_id，而冻结E0无该菌株记录，gold仅给E. coli 562物种级及Rhodococcus globerulus路径完成记录。按身份定位≠反应级能力≠全路径能力，判为合理候选但菌株级作用范围仍未充分核验，取6。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份与gold一致：gold organism_gold五步均记Escherichia coli（物种级，taxid 562），答案四步统一归属Escherichia coli，未把单步菌写成他种菌，也未由序列存在性推断整条路径能力以外的结论。菌株级细节（K-12 MG1655、TaxID 511145、ATCC 700926、NC_000913.3/GC_000005845.2）在E0中无记录，按四.6记UNRESOLVED待核，不得据此判身份错配或虚构；同时其整条路径能力声称与gold的E. coli物种级pathway_complete=TRUE方向一致。故按&#x27;主要微生物对应及身份有可靠支持、少量具体条目需确认&#x27;取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_090：Gold各步organism为Escherichia coli 562；PATHWAY_COMPLETE另列E. coli 562与Rhodococcus globerulus 33008；支持物种级对应，不支持K-12 MG1655菌株级能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 部分性状与E. coli 562的物种级gold一致：运动性、杆状、革兰氏阴性、不产孢、兼性厌氧等；但F2 optimum 37与F3 optimum 7在冻结子字段掩码中无观察来源，F7/F8把肉桂酸/芳香酸降解能力写成K-12事实且仅有EVID_007内部知识或通用路径名支持，F14为K-12特异基因组值而E0缺失。判为部分准确但关键项证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

多项关键性状与gold物种级观测一致：F1兼性厌氧（gold facultative anaerobe=true，aerotolerant=true）、F2温度偏好mesophilic、F4盐度类别非嗜盐且单位为% NaCl (w/v)、F10有运动性、F11直杆状、F12革兰氏阴性、F13不产芽孢、F14基因组规模4,641,652 bp与GC 50.8%落在gold物种级区间内。问题：F2最适37°C、F3最适pH 7、F5保藏号ATCC 700926、F15栖息地描述均无冻结记录支撑（E0无对应条目，gold对应子字段为completeness_only/UNKNOWN）；F7/F8/F9把通路/数据库层面的归属外推为菌株性状描述。按同物种代表记录口径，不因所用菌株与代表株不同而判错；综合定7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_090：Gold给出E. coli 562的物种级观察/预测性状；支持部分形态、革兰氏、运动性、产孢等核对，不支持K-12 MG1655全部菌株级数值。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_090：掩码显示E. coli 562的F2 optimum/F3 optimum等子字段无观察来源或仅为completeness；支持对未核最优值扣分，不把缺失直接判为错误。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> EVID_001仅为MetaCyc路径名/locator、无record_id，属决策相关路线/酶组的笼统来源；大量性状使用INTERNAL_KNOWLEDGE_ONLY的EVID_007；EVID_002/003/004/005/006虽给具体编号/URL，但E0均无对应记录，只能登记UNRESOLVED。未发现已核实错引，也无CRITICAL/SYSTEMIC。核心路线/酶来源整体偏笼统或待核，取4。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出了条目级定位信息：EC 1.14.12.19与3.7.1.14（ExPASy URL）、TaxID 511145、ATCC 700926、GCF_000005845.2/NC_000913.3、MetaCyc通路名，以及逐项evidence_id与claim_scope，主链每步都绑定reaction_evidence_id——可追溯性结构明显优于笼统库名。但这些标识符在统一冻结快照中均无记录（GAP-090-001/002/006/008/012/014/017/020/021/022），MetaCyc条目record_id为null（邻粒度不足），性状类来源多为EVID_007（INTERNAL_KNOWLEDGE_ONLY）。按四.3：无已核实错引，不cap；决策相关组呈UNRESOLVED_SOURCE、部分模块MISSING_SOURCE，属&#x27;部分关键结论可定位、其余仍待核&#x27;，取5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_090：Gold有物种级性状记录可用于对照；答案自身仍须交付可定位来源，gold不能回填为模型证据。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：Gold酶行提供accepted酶/EC参照；不证明答案引用的外部URL或编号已在E0核实。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案对S2/S3 EC缺失、末端类似物、氧条件null有较具体不确定性说明；但多项性状（F1/F6/F11/F12/F13等）由EVID_007内部知识支持却标high/medium，F7/F8把菌株降解能力写成陈述，证据强度与披露不完全相称。未达到系统性误导cap，按5档处理。

<details><summary>V0.4理由与本行变化背景</summary>

正面：uncertainties三条具体且诚实——明示S2/S3未定EC而拒绝借用相近芳香族EC、明示S1立体化学缺失、明示EC 3.7.1.14接受名针对饱和侧链底物、明示题面氧条件为null而未擅自改写；EVID_007明确标注为INTERNAL_KNOWLEDGE_ONLY，属证据性质自述。反面：对菌株级身份（TaxID 511145）、基因组登录号、以及革兰氏/形态/产孢等仅由内部知识支持的性状使用high confidence，且把通路/数据库层归属直接表述为菌株性状，属单点过度确信而非系统性误导。按八.D6严重度条款档内扣分，不cap，取6。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_090：Gold可核对部分物种级性状，但答案的菌株级高置信声明仍需自身证据；支持判断置信与证据相称性。

</details>

## Qwen

答案SHA256：`4679e43e8a4e966efc8df81082a21ae5efce4d46775e2fc69bf639215d33f953`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 路线名回显合规，但实际S1-S3以cinnamate→3-hydroxycinnamate→C7开环→2-hydroxypentadienoate替代gold主链，未交付S04入口双加氧、S03脱氢、S05开环、S02水解等关键步；模块字段完整可辨，但任务符合度主结论失效，D1按任务偏离取3。

<details><summary>V0.4理由与本行变化背景</summary>

七项输出模块齐备：3步主链（底物/产物英文名+SMILES）、每步酶（名称，S3含EC）、每步对应菌、15项性状框架（11项填值、4项null）、evidence_registry与uncertainties；路线名按题面原样抄录、JSON可解析。扣分点：2/3步EC为null、4项性状null（如实未知）、主链仅3步且中段化学存疑（化学问题另计D2）。属7-8档‘大部分必要内容完整，仅少量遗漏’，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：支持gold必答步S01-S05的底物/产物与顺序；不支持答案S1-S3为同一主链。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：支持gold各步accepted酶/EC；不支持答案所用酶名与EC。
- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;：支持答案实际交付的三步路线与酶/微生物归属；不证明其等同于题面指定gold主链。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> S1羟基化、S3水解到题面终产物在反应类型上可辨，但S2把3-hydroxycinnamate直接开环为C7产物+glyoxylate，缺少gold的二羟基化/脱氢和C9开环中间体，且O2/辅因子未列；主链部分可辨但关键转化需重写，按5。

<details><summary>V0.4理由与本行变化背景</summary>

起点cinnamate与终点2-hydroxypentadienoate正确，但中段化学不成立：S2以‘3-hydroxycinnamate 2,3-dioxygenase’把单酚3-羟基肉桂酸直接开环为C7的2-hydroxy-6-oxohepta-2,4-dienoate+glyoxylate。extradiol双加氧开环需邻苯二酚底物（须先形成2,3-二羟基肉桂酸）；答案省略该二羟基化，属违反基本化学约束/无依据跳步，且单步裂解不应少两碳（C9→C7+乙醛酸根），与gold S05的C9产物(2-hydroxy-6-oxonona-2,4,7-trienedioate)不符。属3-4档，触发D2关键错误，cap≤4，取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：gold显示S05将2,3-dihydroxy-trans-cinnamate开环为C9产物、S02再水解为2-hydroxypentadienoate+fumarate；不支持答案S2的C7直接开环路线。
- ANSWER_TEXT / ANSWER.steps&#91;1&#93;：支持答案S2的底物/产物/酶声称；其化学合理性仍需独立核验。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> S=0；S03/S04已核F，S04为KEY入口失败；S01/S02/S05对齐未确认U。无任何目标步获S支持，KEY4受限&#91;1,4&#93;内取2：核心目标推荐失效，仅局部酶名/终产物信息有用。

<details><summary>V0.4理由与本行变化背景</summary>

各步给出酶名，但S1（cinnamate 3-hydroxylase）与S2（3-hydroxycinnamate 2,3-dioxygenase）EC为null、低置信，S3 EC 3.7.1.15无冻结记录；S2酶类（2,3-dioxygenase）与单酚开环所需反应不匹配（同根RE-01）。答案诚实标注low与null EC可减轻但不能代替科学正确性。本维独立评估结论为‘多处反应与酶不匹配/关键步骤缺具体核验’的档内低分（4），非独立cap——依据：EC多未给/未核，酶名属家族级候选。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：支持gold S04入口酶EC1.14.12.19、S03脱氢酶EC1.3.1.87、S02水解酶EC3.7.1.14等；不支持答案S1-S3酶对应。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：支持gold必答步底物/产物与方向；答案S1-S3未绑定这些目标反应。
- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;.enzyme：支持答案实际酶名与EC；不能据此给目标信用。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> P. putida TaxID303身份由E0可核（species级），但无strain、无步级催化或全路径能力证据；complete_pathway_organism_profile_id=ORG_001属未核全路径声称；gold参考菌为E. coli，故不能高档。合理候选+身份局部支持按5。

<details><summary>V0.4理由与本行变化背景</summary>

菌身份用Pseudomonas putida（TaxID 303），E0官方记录确认303=P. putida（名称关联SUPPORTED），无编造或跨类群错配；但全部3步均归同一P. putida且无株级身份，步级催化与complete_pathway_organism_profile_id=ORG_001（整路径能力）均为UNRESOLVED待核（CG08/CG09）。P. putida为公认芳香族降解菌、作为替代路线可接受，但步级/整路径能力缺独立证据，属5-6档‘有合理候选和部分支持，若干关键作用范围未充分核验’，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持TaxID303=Pseudomonas putida物种名；不支持菌株、步级催化或全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_090：gold步级微生物为Escherichia coli 562，另有Rhodococcus globerulus全路径记录；不支持答案P. putida全路径声称。
- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;.microorganism：支持答案把三步均归属P. putida ORG_001；不证明能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> F1/F6/F10-F13/F15等基础性状与P. putida常识/物种身份一致，F2仅给中温无数值；F7-F9目标芳香/肉桂酸利用和关键酶活仅内部知识，E0未核；F4/F3/F5/F14 null如实。关键目标性状证据不足，按5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状中11项填值、4项null（F3/F4/F5/F14如实未知），无遗漏。已填性状（aerobic、mesophilic、motile、rod-shaped、Gram-negative、non-spore、芳香族降解）对P. putida总体合理，但均为INTERNAL_KNOWLEDGE泛化表述、无raw_text、无P. putida专属记录（E0/gold性状仅覆盖E. coli 562与R. globerulus 33008），温度无具体数值。属5-6档‘部分性状准确且适用，但关键项证据不足’，取5；无‘预测冒充观测’或数值离谱的关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：仅支持P. putida mt-2 PaW1菌株记录、培养温度26/30°C与保藏号/底物面板；不支持cinnamate利用或物种全范围。
- E0_EVIDENCE / f3e0:taxid:303：仅支持TaxID303物种身份；不支持性状数值或菌株级表型。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_090：gold性状记录为E. coli 562与Rhodococcus globerulus 33008；不能直接回填P. putida或答案缺失来源。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：支持答案实际填写的15项性状与null分布。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> evidence_registry两条均为INTERNAL_KNOWLEDGE_ONLY，无数据库/文献条目或可定位记录；仅TaxID303身份可由E0正向核对，但答案本身未交付该来源。按MISSING_SOURCE低档2，不判虚构、不cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry仅EVID_001/EVID_002两条，source_type均为INTERNAL_KNOWLEDGE_ONLY（无database/record_id，locator仅为路径名与表型描述），按四.3全部登记MISSING_SOURCE；无条目级可定位可核对来源，D5取低分档。诚实标注内部知识与low置信，属缺失非误导，默认不cap。TaxID 303名称关联经E0支持属事实层（不回填为来源）。取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅核对TaxID303=Pseudomonas putida；不支持路线、酶、性状或全路径能力。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案在steps.uncertainty和uncertainties列出氧条件未指定、EC/菌株未确认、副产物按化学计量推断；confidence多为low/medium/unknown，evidence type标INTERNAL_KNOWLEDGE_ONLY；未系统性把预测写成实证。部分基础性状用medium且缺raw_text，故7非8/9。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties列明氧条件未定、EC/菌株未确认、副产物为化学计量推断；各步uncertainty与confidence（酶/菌low）与证据相称；4项性状诚实置null。主要是内部知识但明确标注。轻微不足：泛化性状多标medium（无原文）略高于依据，且未点出S2环裂解本身化学存疑。属7-8档‘大部分被正确标注、主要限制已说明’，取7；无系统性把预测当实证的误导。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持答案明确披露氧条件、EC/菌株和副产物不确定性。

</details>

## Grok

答案SHA256：`641a733d1306ce1d9c13ea17fb846d4b6e772bb1621fadf697183dd3834f4b75`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 交付了5步主链、逐步酶名与微生物、15项性状、证据表和不确定性；route_scope.chosen_route_name原样保留。主要缺陷是所有步骤EC均null，且程序路线诊断为DEVIATES并伴随多步结构/立体表示非match；按本题D1允许区间&#91;1,4&#93;取上沿4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_090：支持本题为5步BRANCHED_DAG及路线名；不代表必须交付全部旁支。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_090：支持根/终点化合物名称；不支持对答案来源或酶EC的核验。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链五步的化学转化、方向与终点（2-hydroxypentadienoate）总体可辨认，辅因子基本列出；但程序诊断S02–S05为STEREO_CONFLICT_SPECIFIED的非match，S01为charge-blind的UNKNOWN，SMILES立体化学与gold指定不一致或未指定，且个别H+计量缺失。按本题D2允许区间&#91;1,5&#93;取上沿5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：支持五步gold反应方向、主底物/主产物与立体表示；不支持把答案的近似SMILES自动视为完全匹配。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_090：支持题面终点与根化合物名称；不支持未声称的下游步骤。

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 五个gold目标反应均能在答案中找到功能对应的酶名：cinnamate dioxygenase、dihydrodiol dehydrogenase、3-hydroxycinnamate hydroxylase、ring-cleavage dioxygenase、hydrolase；但所有explicit EC均为null，名称与accepted enzyme名/EC未形成已核配对，且程序多步为NONMATCH/UNKNOWN。主要功能有候选支持但需实质修订，取5–6档上沿6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：列出五步accepted enzyme names与EC；答案只给功能名且EC为空，不能据此自动确认精确名-EC配对。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确给出Rhodococcus jostii RHA1及TaxID 101510，身份层面可定位；但所有步级催化归属与complete_pathway_organism_profile_id=ORG_001均依赖EVID_002内部知识。冻结gold的STEP organism为E. coli，PATHWAY_COMPLETE为E. coli 562与R. globerulus 33008，未支持RHA1完成该路径。身份候选合理但能力/整路支持不足，取5–6档下沿5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_090：支持gold步级微生物与PATHWAY_COMPLETE名单；不支持RHA1完成本题路线或各步催化。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状全部出现，未知项以null/unknown诚实保留；RHA1的F1好氧、F6 O2呼吸、F12 Gram-positive等定性值与身份大体相称。但冻结trait_gold只含E. coli与R. globerulus，未含RHA1；F14仅给CP000431而genome size/GC null，温度/pH/盐度多缺数值与条件。关键性状证据不足，取5–6档下沿5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_090：提供E. coli 562与R. globerulus 33008的冻结性状；不支持RHA1性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_090：指示本案可用性状分母与未决子字段；不把未核RHA1性状自动视为正确。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 核心路线、酶、菌与性状均只依赖EVID_001/EVID_002/EVID_003的INTERNAL_KNOWLEDGE_ONLY；EVID_003虽自称NCBI CP000431但注明recalled not re-queried，未交付可核条目级来源。决策相关组全部MISSING_SOURCE，无已核实错引；按D5低分档取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案实际交付的来源登记仅为内部知识/recalled记录；不把内部知识声明当作外部已核来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案在uncertainties和每步uncertainty中明确EC/基因未确认、氧条件为推断、RHA1未直接检索、立体化学未写、性状无可靠原文；但F1/F6/F8/F12等仍以high confidence配INTERNAL_KNOWLEDGE_ONLY呈现，存在单点过度确信。整体披露具体、非系统性误导，取7–8档下沿7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案对未知、推断与来源性质的实际披露；不证明未核内容为真。

</details>

## GPT5.6

答案SHA256：`96dd556bebdc55f4ee69b623a227352fffb3d9594d742088115be69ae15e6901`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Only three steps are delivered, no enzyme/EC for any step, no trait values, and the route chemistry deviates from the specified main chain. Output is parseable and gives some names/SMILES, but core required modules are largely missing; 1–2 band applies, score 2.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_090：Formal case lists ordered_step_count=5 for this pathway; answer delivers only S1–S3.
- ANSWER_TEXT / ANSWER.steps：Answer has three steps; all enzyme fields are null and no required enzyme/EC or trait values are delivered.

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The specified route is oxidative ring activation/cleavage. The answer instead uses side-chain reductions and a direct ring-cleavage jump to 2-hydroxypentadienoate, omitting the gold ring-activation and 2-hydroxy-6-oxonona-2,4,7-trienedioate/fumarate-producing transformations. Multiple core transformations are wrong or unsupported; 3–4 band, score 3.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_090：Gold reaction rows define the specified route: S04 cinnamate dioxygenation, S01 3-hydroxycinnamate hydroxylation, S05 ring-cleavage product, and S02 hydrolysis to 2-hydroxypentadienoate plus fumarate. They do not support the answer&#x27;s reductions/direct cleavage.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_090：Gold enzyme rows show the expected reaction types for the specified steps; the answer&#x27;s step chemistry does not match them.

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All enzyme fields are null for S1–S3; no enzyme name or EC is delivered. The entire enzyme module is absent, so D3a is MISSING=1 per C04.2 and the release decision. The target mapping U/M facts remain program-side facts and are not converted into a scored enzyme-credit band.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.enzyme：All enzyme objects are null; no enzyme name or EC is present to evaluate.

</details>

### D3b 微生物身份与能力：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案把所有步骤及 complete_pathway_organism_profile_id 都绑定到 Thauera aromatica K172，ncbi_taxid=28380，且 evidence_id=null。补充冻结记录显示 TaxID 28380 的官方分类是 Sardinops（genus，parent Clupeinae），并非 Thauera aromatica；这是跨类群的核心身份错配，不是单纯待核。答案同时未给出任何反应级或全路径能力证据，却将同一菌设为完整路径菌。低置信度和诚实 null 不能消除 TaxID 与声称身份的冲突；gold 不同本身不作为唯一扣分理由。按 D3b 身份阶梯，核心身份错配使主要微生物推荐不可靠，触发关键错误上界≤4；保留名称/菌株字符串存在但无法支持推荐，取 3。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / SUPP:TAX:28380：官方分类身份记录：TaxID 28380 为 Sardinops（genus，parent Clupeinae），不支持答案声称的 Thauera aromatica；仅用于身份核验，不证明该菌不能降解该路线。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 required trait values are null/unknown; no trait value is delivered. Per P44, all required traits null/empty means D4 MISSING=1, not a scientific-error score.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：All 15 traits are present structurally but all values are null/unknown; no trait fact is delivered.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry is empty and every step/enzyme/microorganism/trait evidence_id is null. No decision-relevant claim has a locatable source. This is MISSING_SOURCE across groups, not verified mis-citation; D5 low band 1–2, score 1.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：The registry is empty; no source record is delivered for any claim.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer candidly states that enzymes/EC are unknown, CoA intermediates are missing, oxygen condition is unspecified, and microorganism confidence is low. It does not present predictions as experimental observations. Minor limitation: the proposed route transformations are not explicitly labeled predicted/inferred, so not 9–10.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Uncertainties explicitly disclose missing enzymes, missing intermediates, unspecified oxygen, and low organism confidence.

</details>
