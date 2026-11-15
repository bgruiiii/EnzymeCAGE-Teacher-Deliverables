# BIOPATH150_144：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：γ-butyrobetaine degradation III

污染物：4-(Trimethylammonio)butanoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 45.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 40.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 39.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 30.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 31 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 19 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`d57305db657140f6220957393b84ca0c5f84e51710708dc980ffc4c7760bc192`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 答案提供完整JSON、3步主链、15项性状与证据ID，但主链是CntA/CntB羟化—自发裂解—SSALDH氧化到琥珀酸的替代路线，不是题面锁定的CoA依赖γ-butyrobetaine degradation III四步主链，也未交付到Levocarnitine的指定终点。属于严重任务路线偏离，D1落3–4档，给3。

<details><summary>V0.4理由与本行变化背景</summary>

题面通过chosen_route_name明确指定γ-butyrobetaine degradation III且禁止改选路线；gold切片显示该路线为CoA依赖四步路线（S01 CoA合成EC 6.2.1→S04脱氢EC 1.3.8→S03水合EC 4.2.1.149→S02硫酯酶/脱氢EC 3.1.2/1.1.1.108），终点L-carnitine(BSY-c02740)。答案虽原样填路线名，却交付CntA/CntB Rieske单加氧酶路线（C4羟化→半缩醛胺自发裂解→SSADH→琥珀酸），属‘自称合规却交付不同化学路线’的任务参数偏离，按&#91;P100&#93;及八.D1/D2边界属D1关键错误，cap≤4。其余模块（路径/酶/菌/15性状/证据/不确定性）结构完整、格式规范，故cap档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_144_question：题面锁定route_scope.chosen_route_name=γ-butyrobetaine degradation III，要求按指定路线给主链。
- ANSWER_TEXT / BIOPATH150_144_answer：答案route_summary与S1-S3交付的是CntA/CntB羟化裂解到琥珀酸路线，不是指定CoA路线。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_144：Gold路线终点为Levocarnitine；支持答案终点/主链与指定路线不同，不评价D2化学质量。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案提出的CntA/CntB C4羟化→半缩醛胺自发C–N裂解→SSALDH氧化为琥珀酸路线在有机转化、方向与连续性上基本自洽，主有机产物走向合理。但辅因子/H+计量被简化，自发裂解步无酶且未核，属于可成立的替代路线而非指定路线；按D2可成立替换上限&#91;1,6&#93;取6。

<details><summary>V0.4理由与本行变化背景</summary>

答案路线的内部化学成立：S1 C4羟化(C&#91;N+&#93;(C)(C)CCCC(=O)&#91;O-&#93;+O2+NADH→4-羟基中间体+NAD++H2O)为合理单加氧；S2半缩醛胺自发C–N裂解释TMA+琥珀酸半醛化学正确；S3琥珀酸半醛经脱氢酶氧化为琥珀酸方向正确，碳骨架与计量基本守恒、三步连续，无起始步错误、无无依据跳步、无明显不守恒。但该化学属与gold route III(CoA-肉碱)不同的替代路线，S1无EC、S2产物与酶为推断、整体仅内部知识支撑；按四.5‘未证实→不自动判错也不给高分’，定5–6档取6；路线偏离主要归D1，故D2不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_144_answer：答案给出完整替代化学主链及辅因子，用于评价化学连续性与计量表达。
- RUBRIC_CLAUSE / P103：辅因子遗漏通常为局部计量缺陷，不自动cap；支持D2在档内处理。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分6 → V0.5新分1，变化-5。

新裁判理由：

> Gold四个必答目标步为CoA依赖路线；答案S1为不同C4羟化、S2为自发裂解、S3为SSALDH氧化，均不对应目标步。路线诊断已确认S01/S04为NONMATCH，S02/S03未绑定/缺失，S=0/4，无目标催化信用。已确认KEY失败触发D-KEY4≤4；在&#91;1,4&#93;内因无可用的目标反应对应、主目标路线整体失败，取1。

<details><summary>V0.4理由与本行变化背景</summary>

S1 CntA/CntB与S3 succinate-semialdehyde dehydrogenase均为对应反应类型（单加氧/醛氧化）的合理候选，S2正确判为自发无酶，无‘用3类水解酶解释羟化’等大类别错配或名/EC互斥。但S1关键步骤无EC编号、S3 EC 1.2.1.24按记忆填写且E0无冻结记录无法核accepted name/reaction、整体无外部支持，属‘有合理候选和部分支持但关键步骤缺具体核验’5–6档取6。编号类核实属四.6/D5，不作D3a关键错误依据（OBS-D3A-D5）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_144：Gold S01为gamma-butyrobetainyl CoA synthetase，S02-S04为CoA路线相关酶；不支持答案CntA/CntB—SSALDH目标对应。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：Gold主链为gamma-butyrobetainyl-CoA→crotonobetainyl-CoA→L-carnitinyl-CoA→L-carnitine；与答案羟化裂解路线不同。
- ANSWER_TEXT / BIOPATH150_144_answer：答案S1-S3显示替代路线，未交付Gold四步目标反应。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案统一将各步归属Acinetobacter baumannii（ORB_001，TaxID 509064，strain null），并声称complete_pathway_organism_profile_id=ORG_001。A. baumannii对CntA/CntB型路线是合理候选，但菌株级身份、TaxID与整条路径能力均仅有内部知识，无反应级或全路径证据。落5–6档，给5。

<details><summary>V0.4理由与本行变化背景</summary>

答案以Acinetobacter baumannii（仅到种、无菌株、TaxID 509064按记忆填写）承担全部三步并声称完成整条路线(complete_pathway_organism_profile_id=ORG_001)。A. baumannii是真实的γ-butyrobetaine代谢候选菌，作为候选合理；但身份仅物种级、TaxID与完整路径能力均无冻结证据核验(E0 GAP)，且所用菌与gold route III各步菌(Agrobacterium sp.525a/Sinorhizobium meliloti/E.coli)不同。属‘有合理候选和部分支持但关键身份与作用范围未充分核验’5–6档；因整条路径能力声称超出现有粒度证据，取5。无可核实之异菌株/跨类群错配，不cap（D3b身份阶梯：仅未核不判错）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_144_answer：答案把全部步骤归属A. baumannii ORG_001并声称完整路径能力；用于评价微生物身份与能力粒度。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_144：Gold各步菌为Agrobacterium sp. 525a、Sinorhizobium meliloti、Escherichia coli；仅说明答案菌与Gold目标路线不同，不单独证明答案菌身份错误。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 15项性状全部出现，F3/F4/F5/F14按明确未知/null处理，完成度好。严格好氧、O2呼吸、革兰阴性球杆菌、不产芽孢、无运动、37/44℃等多项为教科书级合理值，但全部来自内部知识，E0无A. baumannii性状记录；F9酶活与CntA/CntB路线绑定也未核。按5–6档给6。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全（11项填充+4项诚实null：F3/F4/F5/F14），身份关联A. baumannii（物种级）。填充值多为教科书级可解释内容（严格好氧、革兰阴性球杆菌、无鞭毛不运动、不产芽孢、37℃/44℃可生长、氧化性利用葡萄糖、环境与临床广适），无明显数值离谱，也未把物种观测倒推为未声称的菌株级性质。扣分：全部来自内部知识、raw_text均为null、E0无A. baumannii性状记录无法核验；F8‘广义降解能力’实写为致病/耐药/耐干燥，偏离字段题意；F9声称CntA/B具体活性未核验；且为与route III不同的物种。属‘部分性状准确且适用但关键项证据不足/条件解释需修订’5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_144_answer：答案给出15项性状、明确null与confidence，用于评价性状内容与不确定性处理。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_144：Gold性状记录主要覆盖Agrobacterium/Sinorhizobium/E. coli；不含A. baumannii TaxID 509064的冻结性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_144：显示本题可评分性状分母与Gold覆盖范围；A. baumannii无observed记录，支持局部未核而非已证伪。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 答案所有材料结论均落在EVID_001-EVID_003，source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，无文献、数据库条目或计算记录可定位。虽evidence_registry有claim_scope映射且较诚实，但外部可追溯性几乎不存在，按MISSING_SOURCE低档给2。

<details><summary>V0.4理由与本行变化背景</summary>

答案evidence_registry三条(EVID_001/002/003)全部source_type=INTERNAL_KNOWLEDGE_ONLY，无database/record_id/DOI/计算记录，属MISSING_SOURCE（完全无外部可定位引用）；claim_scope虽描述内部知识覆盖，但不能定位到任何可核对条目。按四.3/R2合成：全部决策相关组仅缺失来源→低分档、默认不cap；答案对无来源较诚实故取最低档上沿3（非1–2）。E0为EVIDENCE_GAP且无已核实错引→severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION、D5不cap；EC/TaxID等具体号保持UNRESOLVED待核（未核≠虚构≠错引）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_144_answer：显示三条证据均为INTERNAL_KNOWLEDGE_ONLY且无database/record_id/locator；支持MISSING_SOURCE，不支持外部追溯。
- RUBRIC_CLAUSE / P34：MISSING_SOURCE（含仅INTERNAL_KNOWLEDGE_ONLY）按D5低分档，默认不触发cap。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确标注internal knowledge、low/medium confidence，F3/F4/F5/F14诚实null，并在uncertainties中列出路线可能不匹配、EC未核、TaxID未核、自发裂解不确定等限制；没有把内部记忆系统性包装成观测。少数全路径/性状声称仍强于无外部依据，但整体披露具体、边界清楚，给8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且诚实：uncertainties逐条列明路线归属不确定（明确‘若为经L-carnitine或crotonobetainyl-CoA的变体则主链不匹配’）、S1无EC与C4位点依据、S2自发生成与推断、S3 EC与NAD/NADP依赖性按记忆低置信、TaxID记忆未核验、15性状均内部知识且null项未用近似值占位；置信分层high(基本形态/革兰)/medium(路线/性状)/low(EC)合理，未系统性把预测写成实证。扣分点：整体路线仍以medium置信作为route III呈现，route_scope.notes对‘好氧’推断较肯定——属单点/整体轻度过度确信而非系统性误导，不cap；取7档。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / BIOPATH150_144_answer：显示答案对内部知识、未知项、路线/EC/TaxID不确定性的披露质量。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；D6按证据性质表述覆盖范围独立定档。

</details>

## DeepSeek

答案SHA256：`3099391c32a9b05ca36f28b453c696881e6026fd93c850067dae77f4142f9871`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> 答案格式完整但主链化学与题面指定路线不符：S1直接将底物羟基化为L-Carnitine，而gold S01为CoA连接生成gamma-butyrobetaine-CoA；后续S2-S4也非gold步骤。属严重任务偏离，D1关键错误，档内取2。

<details><summary>V0.4理由与本行变化背景</summary>

答案在route_scope原样填写指定路线名并声明is_single_continuous_route=true（自称合规），但交付主链为γ-butyrobetaine经单加氧酶羟化为L-carnitine后转入carnitine降解（TMA+丙二酸半醛→acetyl-CoA），与题面指定的CoA硫酯依赖γ-butyrobetaine degradation III主链机制不同。按P100，&#x27;自称合规却交付不同化学路线&#x27;属任务参数偏离，构成D1关键错误（cap≤4）；因四步齐全、每步酶与菌、15项性状均在，属关键错误档内较高，取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：列出要求的主链反应S01-S04；不支持答案的直接羟基化路线。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_144：指定route_name和terminal Levocarnitine；不支持答案将L-Carnitine作为S1产物并继续下游。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：显示S1底物为4-(Trimethylammonio)butanoate、产物为L-Carnitine、酶为EC 1.14.13.229。

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分3 → V0.5新分7，变化+4。

新裁判理由：

> 按答案自身替代路线评价化学：S1羟基化、S2脱氢、S3醛裂解、S4氧化脱羧，主链连续且主要转化合理；但S3未列CO2，化学计量不完整，且EC未核。属主链成立、局部计量/证据问题，取7。

<details><summary>V0.4理由与本行变化背景</summary>

题面指定路线为γ-butyrobetaine degradation III；答案未声明替代路线却交付以羟化起始的不同主链，且S3将3-脱氢肉碱(C7, C&#91;N+&#93;(C)(C)CC(=O)CC(=O)&#91;O-&#93;)裂解为三甲胺(C3, CN(C)C)+丙二酸半醛(C3, O=CCC(=O)&#91;O-&#93;)，按答案自报SMILES计C7→C6，碳原子不守恒且uncertainty=null无说明。按四.5四步判断：未声明偏离且无可核证据，偏离使&#x27;指定路线主链成立&#x27;的D2主要结论失效；同时&#x27;原子明显不守恒且无说明&#x27;本身为D2关键错误，cap≤4。S2氧化与S4氧化脱羧化学合理，档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0-3&#93;：给出连续四步转化；不证明目标路线或具体EC。
- RUBRIC_CLAUSE / R2-103：辅因子/副产物遗漏通常为局部计量缺陷，不自动cap。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 四个gold必答目标反应均未交付：S01需CoA连接，答案S1为羟基化；S02需L-carnitinyl-CoA-&gt;L-carnitine，答案S2为L-carnitine-&gt;3-dehydrocarnitine；S03/S04也完全不同。无任何target反应获得对应信用，核心目标推荐失效，取1。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶名与反应类型自洽（monooxygenation→monooxygenase 1.14.13.229；oxidation→L-carnitine dehydrogenase 1.1.1.108；aldol cleavage→aldolase 4.1.2.34；oxidative decarboxylation→malonate-semialdehyde dehydrogenase 1.2.1.15），其中S2 EC 1.1.1.108在gold S02注释中出现。但四步EC均无冻结记录可核（EVIDENCE_GAP），S1酶类别（1.14.13单加氧酶 vs 常见2-OG依赖羟化）存疑无法核，且酶集服务于偏离路线。属&#x27;有合理候选和部分支持、关键步骤缺具体核验&#x27;（5–6档），取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：列出S01-S04的底物/产物；答案步骤均不匹配。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_144：列出accepted酶/EC；答案的酶/EC未用于对应target反应。
- ANSWER_TEXT / ANSWER.steps&#91;0-3&#93;：显示答案实际反应；不支持任何gold target反应完成。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 答案统一使用Pseudomonas putida KT2440（TaxID 160488）并声称全路径能力；该菌株身份本身合理，但全路径及逐步催化能力在E0无记录，且答案证据仅为INTERNAL_KNOWLEDGE_ONLY。属合理候选、关键能力未充分核验，取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案四步全部归属同一菌Pseudomonas putida KT2440，并在complete_pathway_organism_profile_id=ORG_001宣称其为完成整条路径之菌，F8声称可生长于γ-butyrobetaine；但全套仅INTERNAL_KNOWLEDGE_ONLY、无任何反应级或全路径能力证据；gold物种为Agrobacterium sp.525a/Sinorhizobium meliloti/E.coli（gold非穷尽不改写为答案必错）。整条路径能力属无依据外推类型（D3b明确警惕&#x27;整条路径菌&#x27;），但TaxID 160488与是否真能降解均无冻结证据核实，故key_error记UNRESOLVED不cap；属&#x27;作用范围未充分核验、单步与整路径能力未区分&#x27;，取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：给出菌名/菌株/TaxID和全路径能力声称；不证明能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_144：gold列出不同菌株；不自动否定P. putida，但也不支持其能力。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_144：冻结mask无P. putida行；无法核验其性状/能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项性状全部填写（11项有值、4项明确未知），对象为P. putida KT2440。多数常规性状合理，但E0无P. putida性状记录，关键数值/条件未核验；按部分性状合理、关键证据不足取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐全，F3/F4/F5/F9诚实填null（明确未知非遗漏）；已填项（aerobe、optimum 30℃、aerobic/O2、Gram-negative、rod-shaped、polar flagella、non-sporulating、genome ~6.18Mb/GC61.5%、广适性）对P. putida KT2440总体合理且内部一致。但全部仅INTERNAL_KNOWLEDGE_ONLY、raw_text与登录号多为null，EVIDENCE_GAP无P. putida性状冻结记录（GAP-144-024/025等），无法核验数值与条件；属&#x27;部分性状合理适用但关键项证据不足&#x27;（5–6档），取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：给出15项性状值/未知；不证明准确性。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_144：gold仅有其他菌株性状；无P. putida记录。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_144：冻结子字段mask无P. putida；无法核验数值。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 答案仅登记EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator，无法定位任何文献、数据库或计算记录。属MISSING_SOURCE低分档，取1；缺失非误导，不触发cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案仅登记EVID_001/EVID_002两条证据，source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null，属MISSING_SOURCE（完全无引用或仅内部知识自述）。决策相关组（CORE/APPLICATION_CRITICAL）亦无任何条目级可定位可核对来源，D5落在低分档；因EVIDENCE_GAP无经核实错引，不触发cap。虽内部claim→evidence映射自洽，但指向非来源，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：两条均为INTERNAL_KNOWLEDGE_ONLY，无定位字段；不支持可追溯性。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 答案用confidence标签并保留部分null/unknown，但大量未核实性状（运动性、革兰氏、基因组大小等）标high/medium，且uncertainties为空；有不确定性披露但过于笼统，部分结论强度超过依据，取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案以INTERNAL_KNOWLEDGE_ONLY标注来源（对证据类型有一定诚实），但uncertainties为空、未做任何不确定性/未知/待验证说明；多项稳定与基因组性状赋high/medium置信却无来源，且未披露主链与题面指定路线不一致这一主要限制。属&#x27;多处过度确信、主要限制未说明&#x27;（3–4档）；未达把预测系统性写成实证观测的系统性误导，故不cap，取4。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：显示高置信标签与未核性状并存；不证明证据强度。
- ANSWER_TEXT / ANSWER.uncertainties：uncertainties为空数组，主要限制未具体列出。

</details>

## Kimi

答案SHA256：`6ed647f83f935cd6cbab76acd762f2fef7b3c0bd4159dddef8b675ead6884cc6`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> 题面指定γ-butyrobetaine degradation III且必须按该路线给主链。答案虽回显路线名，但实际只给一步C–N裂解到crotonate+TMA，且缺少gold要求的S02–S04，属明显任务偏离与大部分必要步骤缺失；有关键任务符合度错误，D1在&#91;1,4&#93;内取2。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的各模块（步骤与底物/产物英文名+SMILES、首选酶、对应菌、15项性状、来源登记、不确定性）均有交付且结构完整，但交付主链并非题面指定路线 γ-butyrobetaine degradation III：gold BSY-p00981 为4步CoA依赖路线（S01 CoA连接EC 6.2.1→S04脱氢EC 1.3.8→S03水合EC 4.2.1.149→S02硫酯酶EC 3.1.2.M6，终点Levocarnitine），答案却是一步C–N裂解生成crotonate+trimethylamine，且自称严格采用题面路线。属“自称合规却交付不同化学路线”的任务参数偏离，触发D1关键错误cap≤4；其余模块完整，档内取4（唯一一步的EC仍为null为附加缺陷）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：证明目标主链包含S01–S04且终点为Levocarnitine；不证明替代化学在所有条件下均不可能。
- ANSWER_TEXT / steps&#91;0&#93;：显示答案只交付一步C–N裂解，未交付S02–S04对应步骤。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分3 → V0.5新分5，变化+2。

新裁判理由：

> D2独立评价所答化学。答案只给一步γ-butyrobetaine到crotonate+trimethylamine的C–N裂解，底物与产物SMILES基本可辨、方向为底物到产物，但缺EC、辅因子/质子说明与连续路径；该转化是否真实存在亦无E0核验。按部分可用、需实质修订，取5。

<details><summary>V0.4理由与本行变化背景</summary>

按四.5四步判断：第1步题面已指定路线；第2步答案未声明替代路线或范围边界，反而声称即为该路线（未声明偏离→cap候选）；第3步该替代化学无可核证据（EVID_001仅复述题面、EVID_002无citation）；第4步偏离使D2主要结论（题面指定主链）失效→D2关键错误cap≤4。所交付单步C–N裂解自身化学可成立（C7H15NO2→C4H5O2−+C3H9N+H+），但属另一路线、且未标H+、缺CoA/ATP/FAD等路线要素与4步连续性；档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / steps&#91;0&#93;：显示单步C–N裂解及crotonate/TMA产物；不能外推为完整主链或证明该酶真实催化。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> D3a只评目标反应对应。S01为KEY入口且已确认目标失败：答案给C–N裂解/putative lyase，不是gold的γ-butyrobetainyl CoA synthetase EC 6.2.1；S02–S04未交付且本地对齐未确认。确认KEY失败给出&#91;1,4&#93;，但无任何目标催化对应，取1。

<details><summary>V0.4理由与本行变化背景</summary>

答案所交付步骤的酶名“γ-butyrobetaine trimethylamine-lyase (putative glycyl radical enzyme)”与其自身所述C–N裂解/消除反应类型相符，未出现EC与酶名互相矛盾；但EC、基因/蛋白均为null、仅low置信，且EVID_001只是复述题面、无条目可定位，具体催化证据未核验。属“有合理候选和部分支持、关键步骤仍缺具体核验”5–6档，取5；不将错引/路线偏离作为本维关键错误（OBS-D3A-D5）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：S01目标反应为γ-butyrobetaine+CoA+ATP→gamma-butyrobetaine-CoA+ADP+phosphate；不支持C–N裂解到crotonate+TMA。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_144：S01接受酶为gamma-butyrobetainyl CoA synthetase EC 6.2.1；不支持答案的lyase名称。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案将Emergencia timonensis（仅物种级，无strain/TaxID）绑定到错误的单步并设置complete_pathway_organism_profile_id，声称gbu型能力；EVID_002仅为PubMed检索词且无精确引文。目标步对应微生物为其他菌，答案微生物的身份/反应级/全路径能力均未获可定位支持，按较弱档取4。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出物种级身份 Emergencia timonensis（strain、TaxID、保藏号均null），并声称其具γ-butyrobetaine裂解能力；该物种身份本身未见已核实错配证据，但菌株级身份、编号与反应级/路径级能力均无可定位支持（EVID_002为PubMed检索词、明确无citation），且非gold路线III的步级菌。按D3b身份阶梯属“粒度不足＋能力待核”，5–6档取5；E0无记录，不判编造、不cap（未核≠虚构）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_144：目标步对应Agrobacterium sp. 525a、Sinorhizobium meliloti、Escherichia coli等；不证明Emergencia timonensis不能进行替代反应。
- ANSWER_TEXT / steps&#91;0&#93;.microorganism; organism_profiles&#91;0&#93;：仅给物种级名称，无strain/TaxID；EVID_002为检索词而非可定位能力证据。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项均出现，10项明确null，5项给出定性值；这体现诚实未知而非编造具体数值。但5项非空性状均依赖EVID_002检索词、无raw_text或无官方性状记录，F1严格厌氧及F7/F8/F9/F15能力不能按相应粒度核实；按部分性状可辨、关键证据不足取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状按字段交付：5项有值（F1严格厌氧、F7碳源/底物利用、F8窄谱降解、F9推定裂解酶活、F15人肠道相关），10项null诚实标注未知；有值项均为定性、无raw_text与可定位记录（EVID_002为检索词），无法核验；属“部分性状合理适用、关键项证据不足”5–6档取5。无已核实数值/单位/菌株错误，不cap；缺失项按明确未知，完成度扣分归D1不重复重扣（四.4/P112）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：显示5项非空、10项null；非空性状为定性描述且引用EVID_002检索词。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_144：gold性状行不覆盖Emergencia timonensis；不能用于验证答案的F1/F7/F8/F9/F15。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 答案仅登记EVID_001（MetaCyc但无record_id，locator只是复述题面路线）和EVID_002（PubMed检索词，明确说exact citation not supplied）。关键路线、酶、菌与性状均无可定位条目级来源；属仅给笼统库名/检索词且结论-来源关联很弱，D5取3。无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

证据登记仅2条：EVID_001标注DATABASE_DIRECT/MetaCyc但record_id=null、locator只是复述题面，无可定位条目；EVID_002标注LITERATURE_DIRECT/PubMed但仅列检索词并明确“exact citation not supplied”。决策相关组（CG01/CG02/CG03/CG05/CG07）全部只有笼统/自我来源，按四.3/P35评3–4档，取3。E0为EVIDENCE_GAP，无经核实错引，不cap，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry&#91;0..1&#93;：显示两条证据均为无record_id的笼统来源；EVID_002明确未提供精确引文。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分5 → V0.5新分7，变化+2。

新裁判理由：

> 答案明确保留氧条件null、EC/gene null、strain/TaxID null及多数性状null，并集中列出不确定性；多数未知/预测标签较清楚。但EVID_001/002以DATABASE_DIRECT/LITERATURE_DIRECT包装无记录ID来源，且主路线以medium confidence呈现，存在局部过强。整体仍属限制说明较好、少量修订，取7。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties具体列出氧条件未推断、EC/基因未确证、菌株/TaxID/保藏/基因组与多数性状未知，null标注诚实（正面）；但EVID_001把“复述题面”包装为DATABASE_DIRECT+medium，EVID_002标LITERATURE_DIRECT却无citation，F1/F7/F8以medium置信标注无raw_text/记录的性状，属单点过度确信；披露总体存在但部分结论强度超过依据，5–6档取5；未达系统性把预测写成实证/掩盖矛盾，不cap（八.D6/P119-P121）。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties; confidence fields：显示答案对未知、EC缺失、菌株/TaxID缺失有明确说明；同时显示两条来源类型标签较强但无精确记录。

</details>

## Qwen

答案SHA256：`680fe0fe437ed2b8a834af69f678e12ed294b12941a45ae2711659398742841b`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> D1 1–2档：仅交付1/4必答步，路线诊断为S01 SUBSTITUTED_ENTRY_DIVERGENCE且S02–S04缺失，明显偏离指定路线；JSON完整但主链大部分缺失。档内取2因仍有可辨认单步与性状框架。

<details><summary>V0.4理由与本行变化背景</summary>

档位3–4（仅覆盖少数必要模块、多处缺步骤与酶菌关联）。答案route_scope.chosen_route_name虽按题面回填&#x27;γ-butyrobetaine degradation III&#x27;，但route_summary与steps&#91;0&#93;实际交付的是&#x27;还原性C-N裂解生成丁酸根+三甲胺&#x27;的单一反应，与题面指定路线的CoA依赖主链不同，且未声明为替代路线或范围边界——属自称合规却交付不同路线（P100任务参数偏离），归本维关键错误；同时任务模块覆盖不足：主链4步仅交付1步，酶无EC（null），微生物仅物种名无株号/TaxID，15项性状7项填写8项明确未知，来源全部为INTERNAL_KNOWLEDGE_ONLY。综合取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_144：Shows ordered_step_count=4 and LINEAR_UNIQUE, so the required main chain has four steps.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：Shows target S01–S04 reactions; does not support a single direct reductive-cleavage step.
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：Answer delivers only S1 with butanoate/trimethylamine; no S02–S04.

</details>

### D2 反应化学科学性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> D2 1–2档：唯一主链步为直接还原性C-N裂解至butanoate+TMA，未按gold S01 CoA/ATP活化，亦无S04/S03/S02连接至L-carnitine；主链首步错误并一步跳到中心代谢物，无法构成目标可信路径。

<details><summary>V0.4理由与本行变化背景</summary>

档位1–2（主链核心转化明显错误、严重断裂）。题面路线III的首步为γ-butyrobetainyl-CoA合成（底物+CoA+ATP→γ-butyrobetaine-CoA，gold S01，EC 6.2.1），随后脱氢(S04)→水合(S03)→硫酯酶(S02)至终点L-肉碱；答案首步即替换为还原性C-N裂解生成丁酸根+三甲胺，既无CoA活化，也无该路线任何中间体与终点产物。合理替代路线四步判断：①题面已指定具体路线→②答案未声明替代路线（反而声称就是指定路线）→③无可核证据（EVID_001为内部知识）→④偏离使本维主链结论失效，故触发关键错误。唯一可取处是该单步在字面上可配平（需H+/2e-），SMILES书写规范，故不取1分，取2。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：Target S01–S04 chemistry; S01 uses CoA/ATP to gamma-butyrobetaine-CoA and proceeds to L-carnitine.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_144：Target S01 enzyme is gamma-butyrobetainyl CoA synthetase EC 6.2.1.
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：Answer claims direct reductive C-N cleavage to butanoate and trimethylamine.

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分3 → V0.5新分1，变化-2。

新裁判理由：

> C04/D-KEY4：S01为已确认KEY_ENTRY失败，S=0、F=1、U=3，且无目标步获支持；答案酶名非accepted且无EC。在&#91;1,4&#93;内取1，近乎无可用目标催化对应，核心KEY失败使主推荐不可用。

<details><summary>V0.4理由与本行变化背景</summary>

档位3–4偏下。全题仅1个酶候选（gamma-butyrobetaine reductase），ec_number/gene_or_protein全为null，无序列或登录号，无法按四.6核对accepted name/reaction。该酶名对其自述的还原裂解反应类型在名义上自洽（还原酶对应还原裂解），但与题面指定路线首步酶γ-butyrobetainyl-CoA synthetase（EC 6.2.1）不对应；因E0为EVIDENCE_GAP、酶名真实性与EC归属无法核实，按UNRESOLVED登记、不cap；缺EC与无任何序列/文献支持使档位落在3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_144：S01 accepted enzyme is gamma-butyrobetainyl CoA synthetase EC 6.2.1; S02–S04 have different accepted enzymes.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：S01 target reaction is CoA/ATP-dependent activation, not reductive cleavage.
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;：Answer gives gamma-butyrobetaine reductase with no EC for a different reaction.

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> D3b 3–4档：仅给Clostridium sporogenes物种、无strain/TaxID/反应级证据，却设置complete_pathway_organism_profile_id=ORG_001；gold各步对应Agrobacterium sp. 525a、Sinorhizobium meliloti、E. coli，C. sporogenes无冻结记录，身份与能力仍UNRESOLVED。档内取3因有可辨认物种名但缺关键身份和能力支持。

<details><summary>V0.4理由与本行变化背景</summary>

档位3–4。答案只给物种名Clostridium sporogenes，strain与ncbi_taxid均为null，无保藏号/基因组号；能力声称（催化该步并作为complete_pathway_organism_profile_id承担整条路径）仅有EVID_002（INTERNAL_KNOWLEDGE_ONLY），无反应级或全路径级证据。该菌不属于gold步级菌（Agrobacterium sp.525a / Sinorhizobium meliloti / Escherichia coli）。身份层级仅到物种且能力层无据，冻结证据无法核验其能否催化该步→按UNRESOLVED登记、不cap；档位3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_144：Gold lists step organisms Agrobacterium sp. 525a, Sinorhizobium meliloti, E. coli; does not list C. sporogenes.
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：Answer gives C. sporogenes without strain, TaxID, or pathway-capability evidence.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> D4 5–6档：15项均出现，8项明确null；已填的C. sporogenes一般性状（厌氧、杆状、Gram+、产孢）合理，但关键降解/酶活/底物利用性状仅有内部低置信声明，无冻结证据，属部分可用但关键项证据不足。档内取5。

<details><summary>V0.4理由与本行变化背景</summary>

档位3–4上缘。15项中7项填写（F1专性厌氧、F7可利用γ-丁基甜菜碱作碳源/能源、F8降解包括γ-丁基甜菜碱在内的季铵盐、F9 γ-丁基甜菜碱还原酶活、F11杆状、F12革兰氏阳性、F13产芽孢），8项为null+unknown（F2/F3/F4/F5/F6/F10/F14/F15）。形态、革兰、产孢、厌氧与C. sporogenes公认物种特征一致；但支撑推荐的关键项F7/F8/F9均无来源、无raw_text、无株级限定，属物种级泛化且E0无法核验→按UNRESOLVED登记、不cap。数值型性状全部为空，无&#x27;数值离谱&#x27;&#x27;预测冒充观测&#x27;的已核证据；故在4分取上缘而非更低。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_144：Provides trait records for gold organisms; no C. sporogenes trait records.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_144：Shows trait scoreability by organism; no C. sporogenes rows.
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：Answer fills seven traits and leaves eight explicit nulls; no raw_text or external evidence.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> D5 1–2档：evidence_registry仅两条INTERNAL_KNOWLEDGE_ONLY，无database/record/locator；决策相关组均为MISSING_SOURCE，无法定位外部依据。无已核实错引，故不cap；档内取2因有内部证据ID映射但无真实来源。

<details><summary>V0.4理由与本行变化背景</summary>

低分档。决定维度分的决策相关组（CG01路线核心、CG02起点首步、CG03终点、CG05酶-反应/关键EC、CG07核心菌身份）在答案中只挂EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY自我声明，没有可定位条目、文献或计算记录，按P34属MISSING_SOURCE（缺失而非误导），默认不触发关键错误cap。evidence_registry带claim_scope、引用自洽，属结构上的最低限度可读性，故取2而非1；但D5只评价系统实际交付的记录，内部知识声明不构成可追溯性。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Answer supplies only internal-knowledge evidence IDs with no locatable external records.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> D6 7–8档：低置信度和null大量使用，uncertainties列出EC/辅因子/菌株/氧条件未确认，证据性质标注较好。扣分因仍把不同还原裂解路线表述为指定路线主链，未披露与CoA依赖路线的冲突。

<details><summary>V0.4理由与本行变化背景</summary>

7–8档下缘。不确定性披露具体且诚实：全部证据标INTERNAL_KNOWLEDGE_ONLY+low；uncertainties逐条写明EC/辅因子/具体菌株未确认、氧条件题面未指定故无法确认是否严格厌氧、性状仅为一般生物学特征且多数来源未核实；未知项以null+unknown如实占位，未把预测写成观测。扣分点有二：一是把自建的还原裂解路线表述为&#x27;在指定路线γ-butyrobetaine degradation III下&#x27;处理，未披露其与题面路线既有步骤/终点可能不一致（路线身份层的过度确信，非系统性误导）；二是8项unknown未区分&#x27;未检索&#x27;与&#x27;经查未知&#x27;。故不给9–10，取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Answer explicitly lists unconfirmed EC, cofactors, strain, and oxygen condition.

</details>

## Grok

答案SHA256：`eb30370ff6196e1a35a1ca4597243fd2b0dc81bad4572044a456027b99a835df`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1处于1–2档：仅覆盖路线名与2个替代步骤的酶名，EC全为null；所有step.microorganism为null、organism_profiles为空，15项性状一项未交付；程序路线诊断为DEVIATES，核心任务模块大部缺失。取2因仍有可读路线骨架，但完整性与任务符合度主结论失效。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案仅交付2个步骤的酶名，未交付任何微生物与15项性状；EC为null。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_144：金标切片显示指定路线终点为Levocarnitine；不支持把琥珀酸半醛/琥珀酸替代链视为本题完整主链。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_144：金标切片显示ordered_step_count=4且LINEAR_UNIQUE；支持4个必答主链步，不支持仅2步交付。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2处于5–6档：所答两步内部连续，S2醛氧化为琥珀酸是标准转化；但S1为需氧C-N裂解推断，酶无EC，证据仅MODEL_INFERENCE，且与题面金标CoA依赖主链不同，关键入口转化合理性证据有限。取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案给出S1氧化裂解、S2醛氧化的连续两步，但S1为推断且无EC。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_144：金标指定路线终点为Levocarnitine；答案的succinate终点属于替代化学，不能回填目标主链完成。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a按4个必答目标步核：S=0，无answer酶名/EC对应任一accepted目标酶；M=2，S02与S03完全未交付（answer仅有2步，无L-carnitinyl-CoA/crotonobetainyl-CoA相关步骤）；U=2，S01/S04虽交付，但其S1为gamma-butyrobetaine monooxygenase、S2为succinate-semialdehyde dehydrogenase，均不对应相应accepted酶，且EC为null、支持未核。S/N=0/4，几乎无可用目标催化对应，且关键终点步S02缺失；按C04低覆盖与C05=1。并非整维MISSING：answer有可辨认酶模块（两条酶名），故SCORED=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_144：列出4个必答步的accepted酶：S01 gamma-butyrobetainyl CoA synthetase/EC 6.2.1；S02 accepted 1.1.1.108|3.1.2|3.1.2.M6；S03 crotonobetainyl-CoA hydratase/EC 4.2.1.149；S04 gamma-butyrobetainyl-CoA dehydrogenase/EC 1.3.8。该表支持目标酶身份集合，不支持answer中的两个酶作为目标步酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：定义目标步的主底物/主产物与方向：S01 4-(trimethylammonio)butanoate→gamma-butyrobetaine-CoA；S02 L-carnitinyl-CoA→Levocarnitine；S03 crotonobetainyl-CoA/L-carnitinyl-CoA互变；S04 gamma-butyrobetaine-CoA→crotonobetainyl-CoA。answer的succinate semialdehyde/琥珀酸路线不对应这些目标反应。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_144：题面污染物为4-(Trimethylammonio)butanoate，gold终点为Levocarnitine；用于确认目标主链终点边界，不证明answer替代路线正确。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_144：本题gold为LINEAR_UNIQUE且ordered_step_count=4，支持D3a按4个必答目标步核验；不等于要求交付所有旁支。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b模块完全未交付：所有step.microorganism为null，organism_profiles为空数组，无任何物种/菌株身份或能力声称；按P44记MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案未交付任何微生物对象或profile，故D3b无可评价内容。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4模块完全未交付：organism_profiles为空，15项性状一项未填写，也无明确未知记录；按P44记MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案未交付任何organism_profile，故15项性状及其来源均不存在。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5处于1–2档：所有关键结论仅EVID_001 MODEL_INFERENCE，database/record/locator均为null，无可定位外部来源；无已核实错引，MISSING_SOURCE默认不cap；取2因有证据登记但无外部可追溯性。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：EVID_001 source_type=MODEL_INFERENCE，database/record_id/locator均为null，claim_scope含route/reaction/enzyme；仅自我声明，无可定位外部来源。

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6处于9档：答案将路线明确标为推断，evidence.source_type=MODEL_INFERENCE、confidence=low；uncertainties逐条列出路线差异、厌氧替代、EC/微生物/辅因子未知；未把预测写成观测，边界披露充分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案明确说明本主链是推断而非数据库核对，列出替代路线及EC/微生物/辅因子未知，并标注MODEL_INFERENCE与low confidence。

</details>

## GPT5.6

答案SHA256：`a104d69b5f0fde17cd0e4a36fd7e1178d26464678d2144dbd910890db7f1fa75`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 1–2档：4个必答主链步仅交付1步，酶、微生物、性状模块均为空；路线名回显正确，但核心任务模块大部缺失，档内取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_144：登记4步必答主链与完整任务范围；不作为旁支分母
- ANSWER_TEXT / ANSWER.steps：答案仅1步，enzyme/microorganism为null，organism_profiles为空
- QUESTION_TEXT / QUESTION_BEGIN：题面要求每步给出主底物/主产物、一个首选酶及EC、一个对应微生物，并同一菌去重填写15项性状

</details>

### D2 反应化学科学性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 &#91;1,4&#93;档：答案仅给4-(Trimethylammonio)butanoate直接脱氢到crotonobetaine，未体现gold的CoA活化/硫酯中间体/水合/硫酯酶四步连续性，且无辅因子和终点L-carnitine；核心路径严重断裂，档内取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_144：gold显示S01 CoA synthetase、S04 FAD依赖脱氢、S03水合、S02硫酯酶至L-carnitine；不支持游离酸直接脱氢到crotonobetaine作为完整主链
- ANSWER_TEXT / ANSWER.steps：答案仅一步直接脱氢至crotonobetaine，无CoA/辅因子/后续步骤

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a MISSING=1：steps&#91;0&#93;.enzyme=null，全答无任何enzyme.name或ec_number；整个酶模块未交付，不能评具体酶对应。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.enzyme：enzyme=null，无酶名/EC
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_144：gold列有各步酶，但答案未交付；仅支持缺失定位

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b MISSING=1：steps&#91;0&#93;.microorganism=null，organism_profiles为空；无物种/菌株/TaxID，微生物模块未交付。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.microorganism：microorganism=null；organism_profiles为空
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_144：gold列有分步微生物记录，但答案未交付；仅支持缺失定位

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4 MISSING=1：organism_profiles为空，未返回任何15项性状；性状模块未交付。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：organism_profiles为空，无任何性状
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_144：gold列有性状/UNKNOWN记录，但答案未交付profile或性状；仅支持缺失定位

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 1–2档：evidence_registry为空，route/step/酶/菌/性状结论均无可定位来源；属MISSING_SOURCE低档，未核实错引，不cap；档内取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：证据登记为空，未提供任何可定位来源

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 5–6档：明确列出酶/EC、微生物、性状未知并置null，未编造；但将唯一主链反应写成‘可确认’且无来源/证据类型，限制披露不完整；档内取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：列出酶、微生物、性状未知并置null；未给唯一反应步骤的证据类型/来源

</details>
