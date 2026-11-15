# BIOPATH150_022：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：4-toluenesulfonate degradation I

污染物：Tosylate；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 47.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 58 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 71 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 59.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 80 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 59 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`d8d89924bd834c2c3d9900bf36de37174023a71075101d18a22a9e94daddceae`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 任务模块齐全：7步、酶/EC、微生物、15项性状、来源登记均有可辨认内容，JSON可读。但题面锁定主链的终点段被改写：S4未按gold交付4-sulfobenzoate→3,4-dihydroxybenzoate+sulfite，而写成→4-sulfocatechol+CO2并继续延伸到3-oxoadipate；route_status=DEVIATES。按D1允许范围&#91;1,4&#93;取4：模块覆盖较好，但主链任务符合度明显受损，不能进入7–8档。

<details><summary>V0.4理由与本行变化背景</summary>

全部必要模块均实质交付：7步主链（含底物/产物英文名+SMILES、辅因子）、每步首选酶+EC、对应微生物、1条organism_profile含全部15项性状、evidence_registry与uncertainties；route_scope.chosen_route_name原样填4-toluenesulfonate degradation I、氧条件aerobic，任务参数与交付格式符合。少量性状为null（诚实未知），且S4起化学走向偏离gold终端但属化学反应问题（归D2），非模块缺失或路线名/条件更换，故D1不触发关键错误；9–10档因下游化学走向偏离与若干空字段扣至8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_022：支持本题gold为主链4步、LINEAR_UNIQUE；不支持把答案的额外下游步当作题面必答。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：支持S04 gold产物为sulfite与3,4-dihydroxybenzoate；不支持答案的4-sulfocatechol+CO2作为该锁定主链终点。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> S1–S3的主底物、主产物、方向与gold基本一致，连续性好；局部省略H+/H2O等属表达与计量瑕疵。S4把4-sulfobenzoate 3,4-dioxygenase写成生成4-sulfocatechol+CO2，与gold S04生成3,4-dihydroxybenzoate+sulfite不符；S5–S7在该替代分支内部连续、可解释，但不恢复题面主链终点。主干部分成立、关键末端转化需实质修订，D2在允许&#91;1,6&#93;内取5。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3与冻结gold S01–S03逐一吻合（tosylate→4-sulfobenzyl alcohol→4-sulfobenzaldehyde→4-sulfobenzoate，含O2/NADH与H2O，方向与主链连续正确）。但S4把4-sulfobenzoate 3,4-dioxygenase的产物写为4-sulfocatechol+CO2（保留磺酸基、以CO2为离去基），与gold BSY-r00255该酶催化4-Sulfobenzoate+O2+NADH→Sulfite+3,4-Dihydroxybenzoate(protocatechuate)+NAD+直接矛盾；该错误使题面路线I的关键脱磺酸步骤失效，并把S5–S7整段建立在错误中间体上（超出gold 4步的延伸本身不因覆盖扣分，但其化学错误属实）。S1–S3精确正确与S4核心转化错误并存，落3–4档取上限4，触发D2关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：支持S01–S04的gold反应方向与主产物，尤其S04为4-sulfobenzoate→sulfite+3,4-dihydroxybenzoate；不支持答案S4的产物集合作为该主链转化。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：支持S04对应4-sulfobenzoate 3,4-dioxygenase/EC 1.14.12.8；酶名并非自动证明答案所写产物正确。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> S1用toluenesulfonate methyl-monooxygenase/EC 1.14.13.-，与accepted S01对应，confirmed target；S2/S3分别给4-sulfobenzyl alcohol dehydrogenase/1.1.1.-、4-sulfobenzaldehyde dehydrogenase/1.2.1.-，只到不完整家族EC，按U处理；S4虽写4-sulfobenzoate 3,4-dioxygenase，但程序事实为NONMATCH/ROUTE_BLOCKED_NONMATCH，终点目标反应未完成。S=1,U=2,F=1，且D-KEY4给出&#91;1,4&#93;上界；少量目标可用、关键终点失败，取3。该上界不代签本维独立key_error，故key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶toluenesulfonate methyl-monooxygenase EC 1.14.13.-/tsaMBCD与gold BSY-e04018精确对应；S2 4-sulfobenzyl alcohol dehydrogenase(1.1.1.-)、S3 4-sulfobenzaldehyde dehydrogenase(1.2.1.-)、S4 4-sulfobenzoate 3,4-dioxygenase(1.14.12.-)酶名与gold家族一致但仅给family级EC未给1.1.1.257/1.2.1.62/1.14.12.8具体号；S7 maleylacetate reductase EC 1.3.1.32正确但未核；S6以chloromuconate cycloisomerase EC 5.5.1.7解释脱磺酸，酶功能(异构/内酯化)与反应类型(脱磺酸)不匹配，答案自标low并说明不确定。有合理候选与部分支持、若干关键步骤缺具体核验→5–6档取6；酶名/家族对主要步骤成立，S6问题被诚实标注且属非核心，未使本维主要结论失效，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：支持S01–S04的accepted酶名与EC集合；支持S01匹配1.14.13.-，但不把家族级1.1.1.-/1.2.1.-自动升级为已确认具体配对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：支持S04目标反应为4-sulfobenzoate→sulfite+3,4-dihydroxybenzoate；不支持答案S4产物作为目标反应完成。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 主要微生物为Comamonas testosteroni T-2，与gold在S01–S03的T-2直接条目相符；S04 gold侧仅见C. testosteroni种级(TaxID 285)与种级pathway_complete，answer把整条路径与S04都归到T-2，存在种级→菌株级粒度不足。answer所填TaxID 34008在冻结gold中无对应记录（T-2行在organism_gold为No TaxID），保持未核，不能判虚构，也不能据此认定身份已完全核实。主要微生物推荐未被推翻，属少量具体条目待确认，取7。

<details><summary>V0.4理由与本行变化背景</summary>

菌名Comamonas testosteroni + strain T-2与gold organism_gold对S01–S03的EXACT匹配(Comamonas testosteroni T-2, No TaxID)一致，主要微生物推荐与单步酶归属成立；但ncbi_taxid=34008与冻结gold物种级TaxID 285(且T-2为No TaxID)不符，E0仅含taxid 303(Pseudomonas putida)记录，无法核验34008→UNRESOLVED待核；S5–S7属超gold背景，T-2对整条路径的能力声称未获反应级/全路径证据。身份名称/菌株正确、单一编号字段待核、能力声称部分未核→5–6档取6；名称与菌株正确使微生物推荐未被推翻，故不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：支持C. testosteroni T-2出现在S01–S03；S04与pathway_complete仅给C. testosteroni种级(TaxID 285)；支持T-2为No TaxID，不支持TaxID 34008被该gold证实。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 15项齐全，且有若干与gold观察/预测相符的项目：F11杆状、F12革兰氏阴性、F13不产孢、F10有运动性、F8芳烃/烃降解能力等。问题在于关键数值与条件多处留null或只给类别：F2仅有mesophilic/约30°C偏好，min/max null；F4仅给非嗜盐类别，数值null；F1“专性好氧”比gold的aerotolerant表述更绝对；F7把物种碳源谱概括为“不利用糖类”，未逐项对齐gold的observed citrate/fermentation glucose等；F15栖息地广适性在gold为UNKNOWN而答案给出较宽泛描述。部分性状准确，关键项证据不足或表述过宽，取6（5–6档）。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状中F10有运动性、F11杆状、F12革兰氏阴性、F13不产孢与gold物种285观测记录一致且高置信；F1专性好氧、F6好氧呼吸O2、F7以tosylate为唯一碳源/硫源并利用有机酸氨基酸不利用糖类、F8降解芳烃/甾体、F15土壤淡水污泥等广适性，均与物种级记录大体相符、属合理描述（F15 gold为UNKNOWN不核）。但F2温度(min/max)、F4盐度(min0/max2)、F5保藏(JCM 6233)、F14基因组(gc/accession)等gold有观测/可评分值的定量/身份性状被诚实置null（未编造），构成关键定量性状缺口。无‘预测冒充观测’或‘物种级推广到全菌株’的错误；已给内容准确+关键缺口→5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：支持C. testosteroni种级观察/预测性状：motility=true、rod-shaped、gram positive=false、sporulation=false、temperature preference=mesophilic等；不支持把种级资料自动写成T-2菌株全部定量事实。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_022：支持F2/F4等数值子字段的观察/完整性口径与F1 aerotolerant观察项；提示种级与菌株级、观察与预测背景需区分。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry三条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null；没有DOI、数据库条目、计算记录或可定位书段落，关键路径、酶、菌和性状只能追到答案内部标签。属MISSING_SOURCE低分档，不是已核错引，不cap；有内部claim分组但无外部可核定位，取2。

<details><summary>V0.4理由与本行变化背景</summary>

全部结论来源仅INTERNAL_KNOWLEDGE_ONLY（EVID_001/002/003，database/record_id/locator均null），无任何可定位的文献/数据库条目/计算记录，连‘笼统库名’都未给出，落MISSING_SOURCE低分档（1–2）。答案自陈‘无可检索的数据库或文献编号可附’属诚实声明（credit计入D6，不回填D5）。无外部引用可核，不构成已核实错引→不cap。按六状态全组登记MISSING_SOURCE，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / EVID_001：仅证明该条自述为INTERNAL_KNOWLEDGE_ONLY且无database/record_id/locator；不支持其科学结论或任何外部可追溯性。
- ANSWER_TEXT / EVID_003：仅证明S6–S7来源同样为内部知识低置信，无可定位记录；不支持D5高分。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案较充分披露不确定性：S6明确写低置信候选及可能经4-sulfomuconolactone中间体；EC 1.3.1.32自述凭记忆未核；S2/S3/S4/S5/S7基因名填null；TaxID 34008注明物种级、T-2独立TaxID未确认；保藏、基因组、温度/pH/盐度数值未查证也有说明。未达到9–10的原因是S4产物选择仍以medium呈现，未披露其相对gold终点/替代脱磺酸顺序的主要冲突；F1/F15等也有过度概括。整体非系统性误导，取7。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且诚实：uncertainties列7项（S6酶不确定、EC凭记忆未核、基因名多数未知、保藏/基因组/温pH盐未查证、taxid为物种级且T-2独立TaxID未确认、全为内部知识、sulfomuconate命名），未知一律填null不编造，S4/S5/S6/S7均带步级uncertainty，区分观测/预测/内部知识与记忆，总体证据性质标注良好。不足：对S4的错误化学（4-sulfocatechol+CO2）以medium置信呈现，未披露‘脱磺酸生成protocatechuate+sulfite’的替代/正统路线，属单点过度确信（非系统性、无明知掩盖）→7–8档取7，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：支持答案确实披露多项未知、低置信候选、未核EC与TaxID粒度限制；不支持把未核事实视为已证实。
- ANSWER_TEXT / S6：支持S6脱磺酸机制被明确标为低置信/不确定；不证明S4主链产物选择已获支持。

</details>

## DeepSeek

答案SHA256：`8a82c24cb19566e6d8b1e8e5ddbb7d2380f78bc6a85e17ce6c05b463388a19b5`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> Route name and aerobic condition are echoed; all four required main-chain steps, enzyme/microbe fields, one organism profile, and 15 trait slots are present. The S04 main product sulfite is omitted and one extra downstream step is added; extra beyond the specified endpoint does not add or subtract. 7–8 band with minor omission.

<details><summary>V0.4理由与本行变化背景</summary>

全部模块实质交付：5步均含主底物/主产物英文名+SMILES、首选酶+EC、对应微生物；route_scope.chosen_route_name原样填&#x27;4-toluenesulfonate degradation I&#x27;符合题面强制项；15项性状框架齐全（填10、诚实null 5，非遗漏）。扣分点：5项性状null、uncertainties与逐步uncertainty全空、主链多出终点外S5一步未标注为下游延续。属&#x27;大部分必要内容完整，仅少量遗漏&#x27;档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：Supports the four required gold steps and S04 terminal products, including sulfite and 3,4-dihydroxybenzoate; does not support the answer&#x27;s omitted sulfite.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_022：Confirms the linear four-step main chain and task scope; not a source supporting answer evidence.
- ANSWER_TEXT / steps S1-S5; organism_profiles&#91;0&#93;.traits：Locates delivered steps and trait fields; locator does not itself establish correctness.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> S1-S3 chemistry and direction match gold. S4 uses 4-sulfobenzoate 3,4-dioxygenase to produce 3,4-dihydroxybenzoate but omits sulfite, a gold main product; the charge/protonation representation is held but core chemistry is not reversed. S5 is downstream of the specified endpoint, so it neither earns main-chain extra credit nor creates an endpoint penalty. 7–8 band with a local product omission.

<details><summary>V0.4理由与本行变化背景</summary>

S1–S4与gold四步主链化学逐一吻合：4-甲苯磺酸→4-磺基苯甲醇（单加氧/羟化）、→4-磺基苯甲醛（醇氧化）、→4-磺基苯甲酸（醛氧化）、→3,4-二羟基苯甲酸（脱磺酸双加氧），方向、结构与SMILES与gold一致，终点3,4-DHA在S4达成。局部缺陷：S4未列副产物sulfite（gold终点含sulfite），且全程未列O2/NADH等辅因子，属局部计量/辅因子缺陷（§八.P103，7–8档，不cap）；S5（原儿茶酸开环→3-羧基粘康酸）为终点外延续，按P29不进入覆盖率加分/扣分。故7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：Supports S1-S4 transformations and terminal products; shows sulfite is a main S04 product, which the answer omits.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_022：Confirms route terminal is sulfite plus 3,4-dihydroxybenzoate; does not support the answer&#x27;s downstream S5 as part of the scored endpoint.
- ANSWER_TEXT / steps S1-S4：Locates answer products and reaction order; does not itself verify chemistry.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 仅评D3a目标酶对应。S01–S03均有可辨认酶名/EC，但显式EC配对未核或不在accepted集合：S01答案EC 1.14.13.186，accepted为1.14.13.-/1.14.99；S02答案EC 1.1.1.90，accepted为1.1.1.257/1.1.1.M5；S03答案EC 1.2.1.28，accepted为1.2.1/1.2.1.62。上述按U处理，不构成已核不相容F。S04的4-sulfobenzoate 3,4-dioxygenase与EC 1.14.12.8和accepted完全一致，但源状态为REPRESENTATION_EQ_CHARGE_BLIND/UNKNOWN，表示待裁，不能计为已确认MATCH。综合可用D3a对应很少，最多一个目标可近似视为精确accepted对应，其余显式EC仍待核，边界不清；按C04低档&#91;3,4&#93;取低分3。S5为终点后下游，不计入本题四个目标。

<details><summary>V0.4理由与本行变化背景</summary>

酶名与反应类型均匹配（单加氧/醇脱氢/醛脱氢/双加氧/开环），无大类错配。S4 EC 1.14.12.8与gold BSY-e00180完全一致；S1 EC 1.14.13.186落在gold通配1.14.13.-族内；但S2 EC 1.1.1.90（gold 1.1.1.257）、S3 EC 1.2.1.28（gold 1.2.1.62）与gold具体号不一致且均无冻结EC记录（GAP-022-005/014，EVIDENCE_GAP）→按§四.5/P66记UNRESOLVED、保留低分与待核、不cap。S5 1.13.11.3为gold外下游且化学正确。属&#x27;部分支持、若干关键步缺具体核验&#x27;档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：逐目标accepted酶名/EC集合：S01=1.14.13.-/1.14.99；S02=1.1.1.257/1.1.1.M5；S03=1.2.1/1.2.1.62；S04=1.14.12.8。用于判断答案显式EC是否落在accepted范围；不等同具体蛋白底物谱或实验活性证明。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：S01–S04为底物到产物的定向主链，S04主产物为3,4-Dihydroxybenzoate与Sulfite；用于确认D3a目标步与终点范围。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_022：本题主链LINEAR_UNIQUE、ordered_step_count=4；D3a目标为四个必答步，S5不在目标步集合。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> The core species Comamonas testosteroni and strain T-2 are supported for S1-S3, but the answer attaches species-level TaxID 285 to strain T-2 while gold lists T-2 with No TaxID. S4 and complete_pathway are supported only at species level, not strain level. This is a granularity/scope issue, not a confirmed wrong-species replacement; 5–6 band.

<details><summary>V0.4理由与本行变化背景</summary>

物种Comamonas testosteroni为gold各步主链菌（taxid 285物种级），菌株T-2在gold organism条目中为S01–S03记录菌，身份与题面菌选择正确、可支持单步及该路线的降解能力。粒度问题：答案将物种级TaxID 285挂到菌株T-2 profile（gold T-2为&#x27;No TaxID&#x27;），属§八.D3b身份阶梯①&#x27;粒度不足&#x27;（真实物种记录支持菌株级声称）→档内扣、默认不cap；complete_pathway指定T-2全路径能力略超T-2菌株级证据（gold PATHWAY_COMPLETE为物种级）。综合取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：Supports C. testosteroni and T-2 for S1-S3, but T-2 has No TaxID; S4 and PATHWAY_COMPLETE are species-level records, not strain-level T-2 evidence.
- ANSWER_TEXT / steps&#91;*&#93;.microorganism; complete_pathway_organism_profile_id：Locates the strain/TaxID and whole-pathway claims; locator does not verify them.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> Motility, rod morphology, Gram-negative, and non-sporulating match observed gold. Several key traits are null (temperature, salinity, collection, genome), and broad F7/F8/F9/F15 statements rely on internal knowledge or generalized species-level claims; F1 &#x27;aerobic&#x27; also simplifies gold&#x27;s observed aerotolerant record. Some traits are accurate, but key evidence and scope need revision; 5–6 band.

<details><summary>V0.4理由与本行变化背景</summary>

已填10项中多项经gold可核且正确：F10 motile(gold motility=true)、F11 rod-shaped、F12 Gram-negative(gold gram阳性=false)、F13 non-sporulating(gold sporulation=false)，F6(氧为末端受体)与gold各替代受体均为false一致，F8广谱降解芳香族与gold degradation:aromatic compound=true一致；按§四.4同物种代表记录条款，物种级性状参照用于T-2不判错。局部：F1填&#x27;aerobic&#x27;而gold观测为&#x27;aerotolerant&#x27;（措辞差异）、F7/F9/F15为未核描述性声称、且这些以medium而非预测标签给出。关键性状无离谱错误、无&#x27;物种观测冒充菌株定量&#x27;。属&#x27;主要性状可核实且适用，仅少量条件问题&#x27;档，取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：Supports observed motility, rod shape, Gram-negative, and non-sporulating; also shows missing/unsupported temperature, salinity, collection, genome, and broad substrate claims.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_022：Identifies which traits are observed/scoreable versus completeness-only; does not convert nulls or unsupported traits into errors.
- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：Locates the 15 trait values and confidence labels; locator does not verify the claims.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> The sole evidence entry is EVID_001 with source_type INTERNAL_KNOWLEDGE_ONLY and null database, record_id, and locator. All key steps, enzyme claims, microbe claims, and traits point to this same internal label, so important conclusions cannot be traced to a locatable source. This is MISSING_SOURCE, not a verified mis-citation; low 1–2 band.

<details><summary>V0.4理由与本行变化背景</summary>

全答案仅一条evidence_registry(EVID_001)，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，却挂到全部5步与所有性状——按§四.3六状态定义即MISSING_SOURCE（完全无引用或仅INTERNAL_KNOWLEDGE_ONLY自我声明）。决策相关组(CORE/APPLICATION_CRITICAL)全部MISSING_SOURCE→低分档、默认不cap。无已核实错引，故severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。因有claim_scope结构但无任何可定位条目，取低分档3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry&#91;0&#93;：Shows only an internal-knowledge label with no database, record, or locator; it cannot establish traceability.

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> The answer uses nulls for several unknowns and provides confidence labels, which is some uncertainty disclosure. However it provides no limitations or uncertainties list, marks broad internal-knowledge claims as medium confidence, and gives F12 high confidence despite internal-only sourcing. Partial disclosure with some confidence stronger than the evidence; 5–6 lower band.

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties为空数组、每步uncertainty=null，全篇无任何观测/预测/推断区分与限制说明；所有步骤与性状统一medium置信(F12 high)，而证据仅为INTERNAL_KNOWLEDGE_ONLY——属&#x27;多处过度确信、证据类型混淆、主要限制未说明&#x27;。但未发现被系统性掩盖的已知矛盾(证据缺口处并非明知冲突)，故按P119未达&#x27;系统性误导&#x27;，不cap。3–4档取4。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / confidence fields; uncertainties=&#91;&#93;; evidence_registry&#91;0&#93;：Locates confidence labels, empty uncertainties, and internal-only source type; supports assessing disclosure quality, not scientific truth.

</details>

## Kimi

答案SHA256：`7adef9936ce6b58806c8a2bcae3c10abd84219f107d62a515e7322b3c6caaa64`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 四步必答主链全部交付；route_scope精确回显题面指定路线与好氧条件；每步均有主底物/产物英文名与SMILES、酶、对应微生物，且organism_profiles仅一个T-2 profile并完整返回15项性状。S1–S3的EC按题面允许填null，属于完成度小缺口而非模块缺失或路线偏离；D1落在7–8档，取8。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8取低值：全部必需模块均有实质交付——4步均给出主底物/主产物英文名与SMILES、酶名+基因、对应菌；route_scope.chosen_route_name与题面路线名逐字一致、氧条件aerobic在chemistry上落实；15项性状全部出现（11填、4显式unknown），来源与不确定性两节齐备。扣分点：题目明确要求每步“酶及EC”，S1–S3的EC全为null（虽按题面纪律诚实填null，但属字段级遗漏）；F3/F4/F5/F14显式unknown，其中F5、F4、F14在冻结记录中存在同物种观测值（JCM 6233、0–2% NaCl、GCA_016599875.1），仍属完成度不足；无基因组数据。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_022：LINEAR_UNIQUE、4个必答步、route_name=4-toluenesulfonate degradation I、aerobic
- SCOPE_ROW / SCOPE#BIOPATH150_022#CG04：题面氧条件为aerobic，用于D1条件符合性核对
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：S01–S04四步的主底物/主产物与有序主链；不等同于答案正确性本身
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：各步accepted酶名/EC集合，用于核对答案是否覆盖酶与EC交付要求
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：各步相关微生物记录及物种/菌株粒度；S04仅有物种级行
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：15项性状的已知记录与UNKNOWN状态；不证明答案所有性状值正确
- ANSWER_TEXT / ANSWER：提交内容：route_scope、4步、单profile、15性状、evidence_registry

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 四步主链化学与gold一致：S1甲基羟化、S2醇氧化、S3醛氧化、S4 ipso双加氧脱磺酸基生成原儿茶酸与亚硫酸盐；主底物/产物SMILES、方向和步骤连续性正确，O2/NADH/NAD+等辅因子基本在列。仅见H+未列及S04电荷表示边界复核等局部问题，不改变主链结论；D2受程序上限&#91;1,8&#93;，在7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

档位9：四步主链与冻结gold逐步一致——起点tosylate→4-磺基苯甲醇（甲基羟化）、→4-磺基苯甲醛（醇脱氢）、→4-磺基苯甲酸（醛脱氢）、→原儿茶酸+亚硫酸盐（ipso双加氧脱磺酸基）；方向正确、主产物SMILES与gold一致、氧化还原载体O2/NADH及其产物NAD+/H2O在列；终点与gold terminal（Sulfite|3,4-Dihydroxybenzoate）一致；下游芳环裂解被正确置于downstream_continuation且声明不属评分主链。未取10：各步H+未写、S1的还原型辅因子计量未完全配平（属局部计量缺陷，P103/P104），故留9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：S01–S04的底物/产物、role、方向和有序连接，用于D2逐步化学核对
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_022：题面路线终点相关主产物为Sulfite与3,4-Dihydroxybenzoate，且为Aerobic
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：S04 accepted EC 1.14.12.8；仅作S04反应/酶对应参照，不证明具体蛋白实验活性
- ANSWER_TEXT / ANSWER：提交的四步底物/产物SMILES、反应类型与辅因子；用于D2化学连续性评价

</details>

### D3a 目标反应与酶对应：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 4步酶名/EC可与accepted/GOLD对应：S1 TsaMB/toluene-sulfonate monooxygenase，S2 4-sulfobenzyl alcohol dehydrogenase，S3 TsaD/aldehyde dehydrogenase，S4 EC 1.14.12.8 exact。S1-S3缺显式EC，S4产物表示待裁，故D3a落在&#91;7,8&#93;取7而非8/9；9-10因base range与证据门不成立。key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8取低值：四步酶对应在功能上正确且与gold酶集吻合——S1两组分单加氧酶TsaM氧酶+TsaB还原酶（黄金记录为4-toluene-sulfonate monooxygenase两组分/甲苯磺酸甲基单加氧酶）、S2 4-磺基苯甲醇脱氢酶TsaC、S3 TsaD醛脱氢酶、S4 4-磺基苯酸3,4-双加氧酶EC 1.14.12.8（与gold一致），无“EC大类与反应类型不匹配”类错误。扣分：S1–S3的EC全填null，并断言“无已确认的专属EC”，而gold对S2给1.1.1.257、S3给1.2.1.62、S1给1.14.99/1.14.13.-；该断言与冻结gold的EC指派不符且官方EC条目在E0中无记录（GAP-022-009），故未达7–8档上限。属条目级核验缺口，不构成D3a关键错误（错引归D5）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：accepted酶名与EC集合；支持S1-S4功能对应，不核验答案文献真实性，也不解决S4电荷表示。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：S01-S04反应方向与主产物；不核验S1-S3显式EC缺失。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 物种/菌株主对应可靠：Comamonas testosteroni T-2在S1-S3有gold exact，S4 gold仅到种级。TaxID 285为种级身份，T-2菌株在gold无TaxID；whole-path T-2能力在E0未核。按身份阶梯，种级支持菌株声称档内扣至7，不cap；key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8取高值：物种与菌株身份正确——gold organism_gold在S01–S03均列出“Comamonas testosteroni T-2”，species级taxid 285与pathway_complete=TRUE一致；“整条路线可在同一菌株T-2连续完成”的完整路径能力声称与gold PATHWAY_COMPLETE（taxid 285）方向一致，未把单步菌误写成不能完成路径。扣分：把物种级TaxID 285直接挂在菌株级T-2身份上，而gold的T-2行明确为“No TaxID”，属身份阶梯①“粒度不足”（物种级真实记录支持菌株级声称），按P107档内扣、默认不cap；S04的菌株级归属在gold仅到species级。cap条件不成立：主要微生物推荐（C. testosteroni T-2降解tosylate）未被推翻。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：S1-S3 T-2 exact、S04仅种级、PATHWAY_COMPLETE仅种级285；不证明T-2菌株TaxID或S4 T-2归属。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：TaxID 285种级记录；不等同T-2菌株级身份。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 已给性状中革兰氏阴性、杆状、运动、不产孢等经trait_gold可核；F2仅preference可核、optimum 30无观测支持；F1把aerotolerant写成专性好氧偏强；F15 gold为UNKNOWN；F3/F4/F5/F14为null。D1计完成度，D4按已有内容落在5-6档取6，不判编造，不cap；key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6取上限：多条可观测性状与冻结同物种记录相符——F11杆状、F12革兰氏阴性、F13不产芽孢、F10有运动性（存在性）、F2偏好mesophilic；且温度最适30°C被明确标注low confidence并在uncertainties复述为估计，未冒充观测。但关键项证据不足或表述过强：F1“专性好氧（obligate aerobe）”强于冻结观测值aerotolerant=true；F2最适值为估计而min 10/max 37（观测）未填；F3/F4/F5/F14显式unknown，其中F4（0–2% NaCl）、F5（JCM 6233）、F14（GCA_016599875.1）在冻结记录中存在同物种观测；“极生鞭毛”与F15“环境广适型/土壤-地表水-活性污泥”超出冻结证据（F15 gold为UNKNOWN）。无“数值离谱到误导筛选”或“把物种观测写成全物种耐受范围”的关键错误，故不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：支持部分性状观测与UNKNOWN状态；不支持F2 optimum 30或F15广适。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_022：指示F2 optimum_c无观测来源；不将无来源直接判为错误。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 核心路线/酶/菌身份有具体文献或数据库定位（EVID_001 MetaCyc、EVID_002 Junker 1997、EVID_003 Locher 1991），但E0无法核验，登记UNRESOLVED_SOURCE；性状主要依赖EVID_004 INTERNAL_KNOWLEDGE_ONLY，登记MISSING_SOURCE；无已核实错引，不cap。按5-6档取6，保留待核。key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

按六状态集合合成，5–6档取低值。决策相关组(CORE/APPLICATION_CRITICAL)：CG01/CG02/CG03有EVID_001 MetaCyc同名路线条目+EVID_002/003完整书目引文（作者/年/期刊/卷/页，条目级可定位），但冻结快照无这些条目的内容、自由文本引文未解析为可查询标识符（GAP-022-036/037/038），无法核对引用-声称链→UNRESOLVED_SOURCE；CG05酶-反应对应亦为UNRESOLVED_SOURCE；CG07身份组中文献支持物种/菌株名，但ncbi_taxid 285本身无专属可定位来源且E0无记录（GAP-022-040/042）→UNRESOLVED_SOURCE（字段级身份编号来源缺失另行登记，不升级为已核实错引）；CG10（氧需求，APPLICATION_CRITICAL且条件成立）与其余性状组仅EVID_004 INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE。无经核实错引（不得判虚构、不得判CONTRADICTED；MISSING/GENERIC按规则默认不cap），故severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION、不触发cap；因决策相关组仍属“可定位但未核对”，未达7–8档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：只评价答案实际交付的来源记录；不把评分者新增证据回填。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案多处用null、low confidence与uncertainties披露EC/基因组/温度等未知，整体区分了未知；但F1专性好氧、F15广适、F7唯一碳源等以medium/high呈现，部分超出内部知识依据。属单点过强而非系统性误导，D6在7-8档取7，不cap；key_error=N。

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8取低值：不确定性披露具体且成体系——uncertainties逐条说明EC未确认、保藏号/基因组未确认、NAD+/NADH SMILES因避免结构错误而留空、30°C为低置信估计；逐字段confidence分级（酶medium、温度low、多数性状medium），证据登记表显式声明EVID_004为INTERNAL_KNOWLEDGE_ONLY，使读者可区分观测与记忆/推断；未发现系统性把预测写成实证或掩盖矛盾。扣分：物种级记忆值（F6/F7/F8/F9/F15）以medium/high呈现而未在正文标注“记忆值、建议复核”，F1“专性好氧”“极生鞭毛”“环境广适型”表述强于冻结证据，属单点过度确信（P119，档内扣分），不构成系统性误导cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：评价答案自身的证据性质与不确定性披露；不核验外部来源真伪。

</details>

## Qwen

答案SHA256：`3ed5ee101dce95f525c33f7615ca3e0577dfe164c6b4ef0ef67ff396a95c5fdc`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> 四步主链均交付，route_scope路线名与好氧条件原样符合题面；每步均有主底物/主产物名称与SMILES、首选酶/EC、对应微生物；15项性状字段全部出现，未知项以null/unknown处理，无重要遗漏。仅因部分性状为明确未知，未取10。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求模块均被实质交付：route_scope.chosen_route_name原样填写&quot;4-toluenesulfonate degradation I&quot;（未改选路线）、氧条件aerobic；4步均含底物/产物英名+SMILES、单一首选酶+EC、单一对应微生物；organism_profiles按物种+菌株去重为单条ORG_001并由step引用；15项性状按展示顺序齐全（9项填写、6项明确null）；evidence_registry与uncertainties齐备。未见格式损坏、未把空样板照抄、未见任务参数偏离。小幅扣分仅因性状普遍以内部知识充当&quot;最强来源&quot;（来源质量另在D5评）、6项关键性状为null属完成度局限（按P15明确未知≠遗漏，不重扣）。9分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_022：支持本题为4步线性主链；不评价答案科学正确性。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_022：支持题面路线名与好氧条件；不扩展到答案具体酶菌正确性。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 四步碳骨架与gold主链一致：tosylate→4-sulfobenzyl alcohol→4-sulfobenzaldehyde→4-sulfobenzoate→protocatechuate+sulfite；方向、连接及主要O2/NADH/NAD+辅因子基本合理。S1-S3漏写H+，S4为电荷/质子化表示差异，属局部计量或表示问题，不改变主链化学结论，故7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

主链四步与冻结gold（LINEAR_UNIQUE，ordered_step_count=4）逐步一致：S01 Tosylate+O2+NADH→4-(hydroxymethyl)benzenesulfonate+NAD++H2O；S02→4-Formylbenzenesulfonate；S03→4-Sulfobenzoate；S04 4-Sulfobenzoate+O2+NADH→protocatechuate+sulfite。方向forward、起始步正确、无跳步、原子与辅因子（O2/NADH/NAD+/H2O）在列，SMILES与gold canonical/isosmiles一致；终点落在gold terminal（Sulfite|3,4-Dihydroxybenzoate），未越界延续下游。未取10分仅因S02/S03未列H+（currency局部简化），反应式非完全配平书写形式，属局部计量缺陷（八.辅因子条款），不影响主链结论。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：支持四步主转化、方向与主产物；不核答案具体酶EC或菌株身份。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_022：支持起点与终点主产物范围；不扩展至下游或替代分支。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 四条必答目标反应均已交付可辨认的酶名与显式EC（S1 4-toluenesulfonate monooxygenase/1.14.13.174；S2 4-sulfobenzyl alcohol dehydrogenase/1.1.1.313；S3 4-sulfobenzaldehyde dehydrogenase/1.2.1.62；S4 4-sulfobenzoate dioxygenase/1.14.12.20），酶模块已交付非MISSING。按程序冻结事实，S1–S3结构-方向为MATCH、S4为表示边界挂起（仅电荷写法差异），四步均为UNRESOLVED_NONACCEPTED/ROUTE_HOLD，即S=0、F=0、M=0、U=4，不得把未核当已证伪。按可读材料：S3的EC 1.2.1.62恰在accepted集合内，但酶名不在accepted名集合，名—号配对仍待核；S1的1.14.13.174属accepted通配1.14.13.-族内具体号但无冻结条目、按P64不自动判错；S2的1.1.1.313与accepted 1.1.1.257/1.1.1.M5、S4的1.14.12.20与accepted 1.14.12.8具体号不一致，且均无冻结记录（EC:1.1.1.313/1.14.12.20/1.14.13.174/1.2.1.62 均为EVIDENCE_GAP_NO_RECORD），按P66登记UNRESOLVED。故主干功能层面存在部分适用支持，但4/4均为MAJOR/含KEY步未核，不能进入7–8档（C05：KEY/MAJOR U不得给7），也未出现已核失败可判低档；落入5–6档。取5：S2与S4存在具体EC与accepted集的具体差异尚待核验，边界未清，不足以支持该带上沿。

<details><summary>V0.4理由与本行变化背景</summary>

四步酶的功能类别与反应类型全部匹配（甲基单加氧酶/醇脱氢酶/醛脱氢酶/芳环双加氧酶），不存在&quot;酶名与EC类别互相矛盾&quot;的关键错误：S03 EC 1.2.1.62与gold一致；S01 1.14.13.174对gold通配1.14.13.-属同族具体号（四.5不自动判错）；S02 1.1.1.313与gold 1.1.1.257、S04 1.14.12.20与gold 1.14.12.8 具体号不同，而这三个EC在E0无冻结记录（GAP-022-002/007/011/015），无法核对官方accepted name/reaction→按四.5记UNRESOLVED、保留低分与待核、不cap。整体属&quot;有合理候选与部分支持，但若干关键步骤仍缺具体核验&quot;，档内取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：给出本题四步的参考酶名与EC：S01为1.14.99与1.14.13.-，S02为1.1.1.257/1.1.1.M5，S03为1.2.1与1.2.1.62，S04为1.14.12.8；仅支持参考侧酶-反应条目，不证明答案具体蛋白底物谱。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：逐步骤底物/产物身份与方向（Tosylate→4-(Hydroxymethyl)benzenesulfonate→4-Formylbenzenesulfonate→4-Sulfobenzoate→Sulfite+3,4-Dihydroxybenzoate），支持答案S1–S3结构-方向MATCH与S4仅电荷表示差异。
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案自述的四步酶名、显式EC与gene_or_protein（tsaA/tsaB/tsaC/tsaD）；仅证明其交付内容与声称，不证明编号正确。
- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida种级学名与TaxID 303存在且为CURRENT记录（CG07的TAXID_NAME_ASSOCIATION=SUPPORTED）；不支持菌株T-2身份、也不支持任何酶催化或整路能力声称。
- E0_EVIDENCE / f3e0:bacdive:12880：支持Pseudomonas putida mt-2 PaW1(pWWO)菌株记录（保藏号集合与26/30°C培养记录）；种级代表记录，不等于T-2菌株，也不支持T-2的酶或路径能力。

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 答案在所有步骤及complete_pathway_organism_profile_id中均使用Pseudomonas putida T-2 (TaxID 303)。冻结organism_gold显示PATHWAY_COMPLETE为Comamonas testosteroni 285；T-2为Comamonas testosteroni T-2(No TaxID)；P. putida S-313仅出现在S01-S03步骤菌。T-2被误标为P. putida，且全路径菌结论错误，主要微生物推荐失效，按身份阶梯3-4档取3。

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份分层看：①物种层——Pseudomonas putida是gold S01–S03的步级降解菌（P. putida S-313），且TaxID 303经E0核对为Pseudomonas putida（物种级学名对应SUPPORTED），物种推荐本身站得住；②菌株层——答案把菌株标记写作&quot;P. putida T-2&quot;并给物种级TaxID 303，但f3e0:taxid:303记录names不含strain token T-2（item标注STRAIN_TOKEN_NOT_IN_RECORD_NAMES，UNRESOLVED），而gold organism_gold中&quot;T-2&quot;出现在Comamonas testosteroni（No TaxID）名下，构成待裁的菌株级身份差异（未核不判错、不cap）；③完整路径能力层——complete_pathway_organism_profile_id=ORG_001声称单一菌株跑完全4步，gold S04仅列C. testosteroni，全路径能力（L3）无独立证据（CG09 UNRESOLVED）。三段均为&quot;合理候选+部分支持、关键身份/范围未充分核验&quot;，5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：支持正确全路径菌与步骤菌身份；不支持P. putida T-2或T-2完成全路径。
- E0_EVIDENCE / f3e0:taxid:303：支持P. putida物种TaxID 303；不支持菌株T-2或全路径能力。

</details>

### D4 性状科学性：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 性状统一挂在P. putida T-2名下。一般P. putida表型（好氧、运动、杆状、革兰阴性、不产孢）可能有物种级合理性，但T-2在冻结organism_gold中是Comamonas testosteroni T-2，不是P. putida T-2；F7/F8/F9的底物利用/降解能力/酶活又直接依赖EVID_001对P. putida T-2的宽泛声称。性状适用对象错误，关键筛选性状不能归给所指菌株，按3-4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状齐备（9填、6明确null）：温度/pH/盐度/保藏号/基因组/栖息地均诚实为null，按P45与P112属完成度限制而非科学错误，不在D4重复重扣；已给的9项（好氧、好氧呼吸末端受体氧、以4-toluenesulfonate为碳源、四步降解能力、单加氧酶活、运动、杆状、革兰阴性、不产孢）与P. putida物种级常识一致、无与本任务冻结记录冲突的数值，且全部标注low/medium confidence，未把预测包装成观测。主要短板：这些性状仅由EVID_003 INTERNAL_KNOWLEDGE_ONLY支撑、且把物种级性状直接套到&quot;T-2&quot;菌株而未标粒度；温度/pH/盐度等关键定量性状在本菌上无证据（同物种代表记录12880只有26/30°C培养温度，按P113不得当作最适或上下限回填）。属&quot;部分性状准确且适用，但关键项证据不足或条件解释需修订&quot;，5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：支持正确路径菌/步骤菌的已知性状；不支持P. putida T-2菌株性状。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：支持T-2为Comamonas testosteroni T-2，全路径菌为Comamonas testosteroni 285。
- E0_EVIDENCE / f3e0:bacdive:12880：为P. putida mt-2 PaW1菌株记录，可支持P. putida物种背景；不支持P. putida T-2菌株。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 核心路线、酶-EC和P. putida T-2关联主要依赖EVID_001：只有MetaCyc pathway名称，无record_id，E0中无对应MetaCyc记录，属UNRESOLVED_SOURCE；一般性状依赖EVID_003 INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE。EVID_002虽为真实TaxID 303记录，但只支持P. putida物种，不支持T-2菌株，且未用于步骤microorganism。未发现可核实的VERIFIED_MIS_CITATION，故不cap；按3-4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group看：决策相关组中，CG01/CG02/CG03/CG05/CG08/CG09/CG04/CG14全部依赖同一条EVID_001——&quot;MetaCyc / Pathway: 4-toluenesulfonate degradation I&quot;，record_id=null、无稳定链接，E0 item gap GAP-022-039 记为free-text未解析，属路线级笼统来源（GENERIC_SOURCE，非虚构）；CG10（氧需求）只引EVID_003 INTERNAL_KNOWLEDGE_ONLY，属MISSING_SOURCE；CG07有真正条目级可核对证据（EVID_002，NCBI Taxonomy record_id=303，核对f3e0:taxid:303 支持物种级学名/TaxID 对应=SUPPORTED），但菌株T-2关联UNRESOLVED。按四.3/P41，决策相关组&quot;存在部分可定位可核对的条目级证据&quot;→5–6档；因可条目级核对的仅一个分类学条目，酶/菌株/全路径/性状关键结论仍缺映射，档内取低端5。无已核实错引，故不cap、severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持P. putida物种TaxID 303记录存在；不支持T-2菌株或MetaCyc pathway关联。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：支持正确全路径菌与步骤菌身份；不支持答案EVID_001的P. putida T-2关联。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案对未知性状多填null/unknown，EVID_003标为INTERNAL_KNOWLEDGE_ONLY且confidence low，uncertainties也承认未直接核对数据库记录编号、多数性状无原始文献；这些是正面披露。但主路线、酶EC和P. putida T-2全路径菌仍以medium confidence呈现，未披露T-2身份与全路径菌冲突，不确定性说明偏笼统，故5-6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

答案整体做了证据性质分级：路线/酶/菌多为medium、内部知识性状为low、未知项为unknown，并在uncertainties明确写出&quot;未直接核对数据库记录编号；菌株T-2多数性状未逐项给出原始文献，未知项填null&quot;，属具体而非笼统的披露，正向计分。扣分点：①EVID_001以DATABASE_DIRECT/medium包装一个record_id=null的路线名引用（GAP-022-039），未披露其不可条目级核对；②菌株T-2与物种级TaxID 303并置呈现且零披露其粒度不匹配，属对同一条身份断言的单点过度确信；③未区分&quot;物种级常识&quot;与&quot;该菌株观测&quot;。未发现系统性把预测写成实证、未掩盖已知矛盾、置信与证据未整体性错配，故不cap，按八.D6单点过度确信5–6档取6。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持P. putida物种TaxID 303；不支持T-2菌株，提示身份披露不足。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：显示答案所称P. putida T-2全路径菌与冻结身份不一致；用于评价不确定性披露，不直接替代D3b。

</details>

## Grok

答案SHA256：`9922870827cef1f9fdd1cc06d44901750a640c1166b430dfd3b0b479604e9773`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Four required steps are delivered with substrate/product names and SMILES, enzyme names, and a corresponding microorganism; the route name and aerobic condition match the question. All 15 trait fields are present, with 9 filled and 6 explicit nulls, so there is no omitted trait module. Minor completeness/role issues: EC is null for S1-S3 (allowed as unknown but less complete), and sulfite is called a byproduct although gold lists it as a terminal main product. These are small, not major, task-completeness defects.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_022：Confirms the case is LINEAR_UNIQUE with 4 ordered required steps and Aerobic condition; it does not by itself certify answer quality.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_022：Confirms tosylate as root and sulfite/protocatechuate as terminal products; not a trait or enzyme-support record.

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The main chemical route is correct and continuous: S1 methyl hydroxylation, S2 alcohol oxidation to aldehyde, S3 aldehyde oxidation to 4-sulfobenzoate, and S4 oxidative desulfonation to protocatechuate plus sulfite. SMILES and cofactor use are consistent with the gold reactions; the S4 product representation differs only by charge notation and is chemically equivalent for this task. Minor issue: sulfite is labeled byproduct rather than a terminal main product, but it is still delivered. This is a 9 rather than 10.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：Provides directed S01-S04 substrates, products, cofactors, and order; does not itself validate the answer&#x27;s citations or protein-level claims.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_022：Confirms the terminal product set includes sulfite and 3,4-dihydroxybenzoate; not a general chemistry validation beyond this case.

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All four enzyme names correspond to accepted enzyme sets: S1 methyl-monooxygenase, S2 4-sulfobenzyl alcohol dehydrogenase synonym, S3 TsaD/aldehyde dehydrogenase synonym, and S4 4-sulfobenzoate 3,4-dioxygenase with exact EC 1.14.12.8. Explicit EC is absent for S1-S3, which is allowed as unknown but blocks 9-10; the tsaMB/tsaC/tsaD gene attributions are minor unresolved annotations. S4 is under representation review rather than a catalytic contradiction. The allowed D3a range is &#91;1,8&#93;, so 8 is the appropriate high end.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：Lists accepted enzyme names and EC for the four gold reactions; G4 curation-level support, not protein-specific substrate/activity proof.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：Provides the reaction context for enzyme matching; does not independently verify gene attributions.

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The main microorganism, Comamonas testosteroni T-2, is the gold step organism for S1-S3 and is the literature organism for this pathway. The answer gives ncbi_taxid 285, which is species-level for C. testosteroni rather than a strain-level T-2 TaxID; gold lists T-2 as &#x27;No TaxID&#x27; and species 285 separately. This is a granularity issue, not an unrelated-taxon error. S4 T-2-specific support is less explicit than for S1-S3, but the species-level PATHWAY_COMPLETE gold and the pathway literature make the main recommendation substantially supported. 7-8 band; 8 because identity and capability are largely reliable.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：Lists C. testosteroni T-2 step rows for S1-S3 with No TaxID and species-level C. testosteroni 285 PATHWAY_COMPLETE; does not give a strain-level TaxID for T-2 or explicit S4 T-2 row.

</details>

### D4 性状科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The filled traits largely match species-level gold: motility true, rod-shaped, Gram-negative, non-spore-forming, and aerobic/oxygen-respiring. Temperature, pH, salinity, culture collection, genome, and habitat are explicit nulls, which are honest unknowns rather than fabricated values. Some claims are stronger or broader than the gold trait table: F1 &#x27;专性好氧&#x27; is stronger than gold&#x27;s aerotolerant observation, and F7/F9 are pathway/literature-level claims rather than T-2-specific trait observations. These are minor overgeneralizations, not key trait failures. 7-8 band; 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：Provides species-level 285 trait observations and predicted labels; does not automatically prove strain T-2-specific values or an obligate-aerobe label.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_022：Marks which trait fields are observed-accuracy or completeness-only; supports not treating explicit nulls as scientific errors.

</details>

### D5 来源与可核查性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Every step and many traits have evidence_id mapping. EVID_001 and EVID_002 are specific literature citations, EVID_003 is an ExplorEnz record, and EVID_004 is a Bergey&#x27;s species description. However all are source_type INTERNAL_KNOWLEDGE_ONLY; the literature entries lack DOI/record_id, EVID_002 and EVID_004 lack full bibliographic detail, and E0 cannot verify the citations or TaxID 285. Most key conclusions are locatable but not fully verifiable, and no verified mis-citation is present. This fits the 7-8 band at 7 because key mappings exist but record completeness is limited.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：Maps enzyme/reaction claims to gold enzyme rows; does not verify the answer&#x27;s literature citations.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：Maps organism claims to gold organism rows; does not verify the answer&#x27;s citations or TaxID 285 record.
- E0_EVIDENCE / f3e0:taxid:303：E0 taxid 303 is Pseudomonas putida; it does not support the answer&#x27;s C. testosteroni TaxID 285 claim.
- E0_EVIDENCE / f3e0:bacdive:12880：E0 BacDive 12880 is Pseudomonas putida mt-2; it does not support C. testosteroni T-2 traits.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The uncertainties section clearly discloses missing EC for S1-S3, lack of T-2-specific temperature/pH/salinity/collection/genome data, species-level basis for several traits, the unresolved S4 gene symbol, and the ring-cleavage boundary. Confidence labels are mostly calibrated, using medium/low for species-level traits. Minor overconfidence remains in F1 &#x27;专性好氧&#x27; and in some high-confidence pathway-level trait claims, but this is not systemic and the main limitations are stated. 7-8 band; 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：Shows which traits are observed versus predicted and highlights species-level gaps; not a direct D6 score.

</details>

## GPT5.6

答案SHA256：`3dc9dc0ce483ae5f2ea7cdbcf5339f6d7d6f63776f60921c607e15d04d3fd7ff`。

### D1 完整性与任务符合度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面指定路线与好氧条件被原样回显；答案交付4步，每步有底物/产物英文名与SMILES、酶名及同一菌T-2引用，15项性状字段齐全且同菌去重。所有EC为null、多数性状为null/低置信，完成度不足，但无整块模块漏交、无路线改选或重大格式偏离，故在7–8档取低分7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_022：本题为4步线性唯一主链，n_required=4
- ANSWER_TEXT / ANSWER.steps&#91;0..3&#93;：答案交付4步、底物/产物名称与SMILES、酶名和同一菌株引用
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：15项性状字段齐全，但多数为null/unknown

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四步主链与gold四步转化、方向及终点一致：S1甲基羟化→S2醇氧化→S3醛氧化→S4脱磺化生成原儿茶酸/亚硫酸盐。未列O2、NADH/NAD+等辅因子属局部计量缺陷，按P103不cap；未见方向反转、骨架错误或无依据跳步。程序D2的9–10门未放行，故在7–8档取上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：S01-S04有向主转化及辅因子语境
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_022：本题终点主产物为Sulfite与3,4-Dihydroxybenzoate
- ANSWER_TEXT / ANSWER.steps&#91;S1-S4&#93;.substrates/products：答案四步主化合物与gold转化顺序一致，仅辅因子未列

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按目标步事实：S2=CONFIRMED_TARGET/SUPPORTED；S1/S3/S4=UNRESOLVED（S1为非accepted未决，S3/S4为表示对齐待核）。无已确认F/M，故不触发D-KEY4；3个U不能当作S，也不能自动判错。S=1、N=4，明确可用目标仅少数，适用边界未充分确认，依C04/C05在受限低档取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_022：S01接受酶含1.14.99/1.14.13.-；S02含1.1.1.257/1.1.1.M5；S03含1.2.1/1.2.1.62；S04含1.14.12.8
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_022：S01-S04目标反应与方向
- ANSWER_TEXT / ANSWER.steps&#91;S1-S4&#93;.enzyme：答案给出四个酶名但EC均为null；S2与accepted名称相符，其余未达到已确认支持

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Comamonas testosteroni T-2身份在organism_gold的S01-S03有直接T-2行支持；S04仅有物种级C. testosteroni（TaxID 285）行。答案将所有步骤归给T-2且TaxID为null；主要微生物推荐仍为同种且T-2在多数步骤有直接记录，属于S04菌株粒度未充分核验而非关键身份推翻，故7档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_022：S01-S03有C. testosteroni T-2行；S04只有C. testosteroni物种级行；不证明T-2在S04的直接步骤归属。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状中仅5项 filled（F1/F6/F7/F8/F9），10项明确unknown/null，0遗漏。已填性状均低置信且无trait evidence_id；F1把C. testosteroni写成aerobic growth context，而gold观测为aerotolerant=true，表述不够准确；F6为completeness_only，不能计observed accuracy；F9是通路层面描述而非标准酶活条目。关键温度、pH、盐度、保藏、运动性、形态、革兰氏、产孢、基因组均null。部分性状可用且诚实null，但关键证据缺口大，取5-6档低端5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_022：给出C. testosteroni物种级观测/预测性状；F1观测aerotolerant=true；不证明T-2菌株级全部性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_022：F6为completeness_only，不能作为observed accuracy分母；F1/F7/F8/F9等可评分但需按来源语义。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry仅EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null，却被S1-S4、酶、菌全部复用。按D5六状态，这属于MISSING_SOURCE而非已核实错引；决策相关组均无可定位来源，处1-2档。给2而非1，因答案至少给出claim_scope并明确低置信。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：仅INTERNAL_KNOWLEDGE_ONLY，无数据库条目/文献定位；不支持将任何关键结论视为可追溯。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案持续使用low/unknown/null，明确列出EC、菌株标识、性状来源缺口，并把唯一证据标为INTERNAL_KNOWLEDGE_ONLY；未虚构DOI/TaxID/保藏号。个别已填性状仍较泛化且未逐条区分推断/观测，因此8而非9-10。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：显示答案对未知和来源不足有明确披露；不证明其科学结论正确。

</details>
