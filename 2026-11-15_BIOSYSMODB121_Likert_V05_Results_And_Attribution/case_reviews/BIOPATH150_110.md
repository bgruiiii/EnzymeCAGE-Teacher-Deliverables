# BIOPATH150_110：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：gentisate degradation II

污染物：2,5-Dihydroxybenzoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 47 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 38.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 53.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 38.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 53 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 43.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`8561ea5d51855cc73bc8e1b6f6f94ddd521f75866a3dd93fc3db552afe77e193`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 任务锁定 gentisate degradation II 并要求给出主链；答案只给3步，并用 maleylpyruvate isomerase→fumarylpyruvate→fumarate+pyruvate 替代 gold 的4步主链，缺 S01/S03，S02 为 NONMATCH。route_scope 名称与格式、两套性状等模块齐全，但主链任务完成度不足；在 &#91;1,4&#93; 内取4。

<details><summary>V0.4理由与本行变化背景</summary>

模块交付本身较完整：3步主链、每步一个酶（含EC或基因名）与一个对应微生物、两个organism_profile各15项性状（ORG_001填10项/明确未知5项、ORG_002填7项/明确未知8项，均无遗漏）、evidence_registry与uncertainties齐全，route_scope.chosen_route_name按题面原样填写。但存在任务参数偏离：字段声明route II而实际交付route I型化学，构成D1关键错误（P100），故cap≤4；因其余模块实质回应，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：提供 gold 4步主链 S04→S02→S03→S01、各步方向和终点 Pyruvate；不表示答案3步替代支路可完成题面主链。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_110：表明本题 ordered_step_count=4、LINEAR_UNIQUE；不用全图旁支给答案增加或减少主链分母。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 就答案自身给出的三步支路看，S1 gentisate 1,2-dioxygenase 裂解、S2 谷胱甘肽依赖异构化、S3 水解生成 fumarate+pyruvate 的方向与主产物基本连贯，且终点含 Pyruvate；但该支路与 gold S02/S03 并非同一转化，部分 SMILES/互变与质子化表达未逐项核清，故在允许 &#91;1,5&#93; 内取5。

<details><summary>V0.4理由与本行变化背景</summary>

答案主链化学本身成立且连续：S1 gentisate经1,2-加双氧裂解生成maleylpyruvate（列O2与Fe2+为辅因子，未把Fe2+写成计量反应物）；S2谷胱甘肽依赖顺反异构化生成fumarylpyruvate（列glutathione）；S3水解裂解生成fumarate+pyruvate（列H2O），终点覆盖gold终点pyruvate，未见起始步错误、方向反转、无说明跳步或明显不守恒。问题在于S2–S3为route I型关键中间体与连接，与题面指定route II主链不一致，需要按路线修订；按四.5四步判断：路线已指定、替代有部分声明、替代证据仅泛引且E0不可核（按未证实登记，不auto判错也不给高分）、尚未推翻终点与化学合理性，故不触发D2 cap，在5–6档（主干部分成立，关键中间体与连接需修订）取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_110：本题终点主产物为 Pyruvate；答案 S3 产生 pyruvate，但该记录不证明其替代支路的全部中间体。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 程序事实 S=0、F=1、U=3；S02 为预先确认 KEY 的 NONMATCH 目标失败，D-KEY4 触发并限制在 &#91;1,4&#93;。S01/S03 未交付，S04 表示等价待核；错误支路内部酶自洽不给目标信用。考虑仍有部分酶信息与局部可读内容，取2。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶-反应对应可靠：gentisate 1,2-dioxygenase/EC 1.13.11.4与gold该步酶一致。S2 maleylpyruvate isomerase未给EC（按题面规则诚实填null）、基因nagM仅自述中等置信，待核。S3 fumarylpyruvate hydrolase给EC 3.7.1.5并自述&#x27;来自记忆、建议BRENDA/KEGG核对&#x27;：E0官方条目accepted name为acylpyruvate hydrolase/3-acylpyruvate acylhydrolase，反应为a 3-acylpyruvate+H2O=a carboxylate+pyruvate，记录中不含&#x27;fumarylpyruvate hydrolase&#x27;名称，名称关联与步级催化语义在E0均登记UNRESOLVED——按四.6保守条款记待核，不判错引、不判CONTRADICTED、不cap。整体&#x27;部分关键步骤缺具体核验&#x27;，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：S02 目标反应是 maleylpyruvate hydrolase 生成 maleate+pyruvate；答案 S2 为 maleylpyruvate isomerase→fumarylpyruvate，属不同目标反应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：给出 S02 accepted enzyme/EC 3.7.1.23 及 S04 gentisate 1,2-dioxygenase 1.13.11.4；不证明答案替代支路。
- E0_EVIDENCE / f3e0:ec:3.7.1.5：EC 3.7.1.5 官方记录存在且为通用 acylpyruvate hydrolase 反应；不核实答案所称 fumarylpyruvate hydrolase 的特定名称，也不支持其为本题 S02。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案逐步给出菌并区分 K. pneumoniae M5a1 与 Pseudomonas sp. U2，但 K. pneumoniae 仅给 species-level TaxID 573 支持 strain-M5a1 声称，Pseudomonas sp. U2 的 taxid 为 null；全路径能力仅由 ORG_002 的 complete_pathway 声称承载。身份定位≠单步能力≠全路径能力，关键菌株身份与能力未在 E0 核验，按合理候选但关键项未充分核验取5。

<details><summary>V0.4理由与本行变化背景</summary>

未见编造TaxID或跨类群错配：K. pneumoniae的TaxID 573为种级真实号（菌株M5a1的层级不足属粒度问题）；U2菌株身份与gold&#x27;Ralstonia sp. U2&#x27;（TaxID 70356）为同菌株的分类学命名版本差异（答案用旧名Pseudomonas sp.并诚实留TaxID null），按P68保守处理、不凭名称不等判错。能力层：U2携带nag基因簇完成gentisate代谢的声称有文献引用但E0不可核；K. pneumoniae M5a1经gentisate途径降解3-hydroxybenzoate/gentisate的声称仅INTERNAL_KNOWLEDGE_ONLY，TaxID 573在E0无记录（GAP-110-025/026）→UNRESOLVED。无角色推翻主要微生物推荐结论的证据，不cap；属&#x27;有合理候选和部分支持、关键身份与作用范围未充分核验&#x27;，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_110：gold 对对应步列出的菌包括 Escherichia coli、Pseudomonas alcaligenes、Ralstonia sp. U2 等；不能据此自动确认答案的 K. pneumoniae M5a1 或 Pseudomonas sp. U2 身份/能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 两个 profile 均返回全部15项字段；温度、pH、盐度、保藏号、基因组等关键定量项多为 null，定性项以 K. pneumoniae 种级常识和 Pseudomonas 属级常识填写，并在 uncertainties 说明“多为种级常识”。诚实 null 不判编造，但关键定量数据缺失、种/菌株粒度未核，取5。

<details><summary>V0.4理由与本行变化背景</summary>

两个profile各15项齐全、未知项以null诚实表达（温度/pH/盐度/保藏号/基因组项无编造数值）。已填性状在对象匹配上总体合理：ORG_001的革兰氏阴性、不产芽孢、杆状、无动力、兼性厌氧、以O2为末端电子受体等与K. pneumoniae常识相符；ORG_002的好氧、革兰氏阴性、不产芽孢、以萘为唯一碳源经nag/gentisate分支代谢与其菌株背景相符。但关键性状几乎全部依赖INTERNAL_KNOWLEDGE_ONLY或不可核文献（E0无K. pneumoniae记录，U2在trait_gold中除TaxID外均UNKNOWN），且把部分内部知识性状标为high置信；按P46&#x27;不直接判错也不默认正确&#x27;，属部分性状准确但关键项证据不足，取6。缺失项完成度已在D1计，不在D4重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_110：仅提供本case gold菌株的性状记录，不是答案所用 K. pneumoniae M5a1 或 Pseudomonas sp. U2 的直接证据；用于识别证据缺口，不回填答案来源。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案有 evidence_registry，但关键路线/酶主要依赖 EVID_001 MetaCyc 路线名（无 locator）和 EVID_002 文献声称，未在 E0 核对；菌株与性状多处 EVID_003/004 为 INTERNAL_KNOWLEDGE_ONLY，属 MISSING_SOURCE。无已核实错引，不cap；按决策相关组来源弱且部分未核取4。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付了claim→evidence_id映射与claim_scope，区分了DATABASE_DIRECT（EVID_001，MetaCyc条目名）、LITERATURE_DIRECT（EVID_002，含作者/年份/期刊）与INTERNAL_KNOWLEDGE_ONLY（EVID_003/EVID_004），结构上优于只列库名的情形。但决策相关组无一条经核实可核对的条目级结论：EVID_001无稳定条目ID/locator且其下方三步与gold route II主链不一致；EVID_002书目不完整、E0无该文献记录；核心微生物身份与多数性状仅内部知识。按四.3/P41，决策相关组呈GENERIC_SOURCE与UNRESOLVED_SOURCE/MISSING_SOURCE混合，且有部分关键结论可沿映射追查→取5；无已核实错引，不cap，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:3.7.1.5：官方 EC 3.7.1.5 记录存在，但为通用 acylpyruvate hydrolase 反应；不核验答案所称 fumarylpyruvate hydrolase 名称或目标 S02，也不支持 EVID_001/002 的其余内容。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案在 uncertainties 与各字段 confidence 中明确披露路线编号不确定、EC 记忆、互变 SMILES、U2 taxid null、K. pneumoniae 菌株数据缺失等；证据登记区分 DATABASE/LITERATURE/INTERNAL。扣分点在于部分 high/medium 置信仍来自内部知识且未逐条给出原始定位。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体而非笼统：明确指出路线变体编号未确证、S2 EC缺失原因、S3 EC来自记忆需核对、SMILES为互变异构体之一、U2种级分类与TaxID未确证、M5a1菌株级性状缺失且多为种级常识；未知项一律null而未编造，central_metabolism_entry与downstream_continuation如实标注为下游延续。扣分点：F1/F10/F12/F13等仅有INTERNAL_KNOWLEDGE_ONLY来源的性状被标为high置信，部分结论强度超过依据，属单点/多点过度确信但未掩盖矛盾、非系统性误导；按D6严重度条款档内扣分，取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`7b01f64025838f5afb3a6e091f7cca53a768e5807ef702b13c4f72e94e6bc7f0`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案给出route名称、3个step的底物/产物/酶/菌，但题面要求的主链为4步；缺少gold S01末端D-malate/3-isopropylmalate dehydrogenase步，S3为替代分支；15项性状均为null占位。按D1 5–6档取5：主要模块均有涉及，但必要内容遗漏和性状占位明显，不把S3化学错误重复计入D1。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块覆盖：主链3步（每步底物/产物均含英文名+SMILES）、每步一个首选酶+EC、每步一个对应微生物且用单一profile去重（ORG_001）、route_scope.chosen_route_name原样填写、不确定项按题面填null。但两个必需模块实质缺内容：15项性状全部value=null（明确未知，按P15/P45不等同遗漏或错误），来源模块只有INTERNAL_KNOWLEDGE_ONLY自述、无可定位记录。按档位：主要模块均有涉及且关联清楚，但性状整体仅占位、来源未交付，落5–6档；因未知为诚实填写、结构自洽无格式缺陷，取本档上限6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_110：gold的ordered_step_count=4、n_required=4；支持必答主链步数，不直接证明答案化学正确性。
- ANSWER_TEXT / ANSWER.steps：答案仅交付S1-S3；未见S01末端脱羧/脱氢步。
- ANSWER_TEXT / ANSWER.organism_profiles.traits：15项性状全部为null/unknown，未交付可评价性状值。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> S1 gentisate 1,2-dioxygenase开环至maleylpyruvate的主有机转化正确，缺O2/H+属局部计量问题；S2 maleylpyruvate hydrolase水解为maleate和pyruvate正确；S3改用maleate isomerase/EC 5.2.1.1将maleate转为fumarate，非gold S03 maleate hydratase/EC 4.2.1.31至(R)-malate，并缺末端pyruvate步。主干前半段成立，但关键连接和终点需实质修订，按5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

S1（2,5-Dihydroxybenzoate→Maleylpyruvate，1,2-双加氧开环）与S2（Maleylpyruvate+H2O→Maleate+Pyruvate，主/副产物角色与gold一致）在化学与SMILES connectivity上与gold第1、2步（S04、S02）一致。局部缺陷：S1未列dioxygen为辅底物、未列H+，属辅因子遗漏的计量局部缺陷（按P103在7–8档内处理，不cap）。实质问题：S3以maleate isomerase把Maleate异构为Fumarate，与gold的主链后续（S03 maleate hydratase→(R)-malate，S01脱羧→pyruvate+CO2）不符，未声明为替代分支（is_single_continuous_route=true），也无证据（E0无EC 5.2.1.1记录，GAP-110-007），主链终点落在Fumarate（gold terminal=Pyruvate）。按四.5四步：主干前两步成立且已到pyruvate，但末端与连接需修订、替代未证实→5–6档，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：gold S04开环、S02水解、S03 maleate hydratase至(R)-malate、S01至pyruvate；支持目标主链的化学连接。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：gold accepted酶名/EC对应S01-S04；不证明具体蛋白活性。
- ANSWER_TEXT / ANSWER.steps：答案S1-S3的化学转化；S3为maleate至fumarate的异构化，非gold S03水合至(R)-malate。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 按accepted set逐目标：答案S1对应gold S04，gentisate 1,2-dioxygenase/EC 1.13.11.4与accepted相符，可记S；答案S2名称maleylpyruvate hydrolase符合，但EC 3.7.1.9对accepted 3.7.1.23未在E0核验，记U/PAIR_UNVERIFIED；答案S3为maleate isomerase/EC 5.2.1.1至fumarate，非accepted maleate hydratase/EC 4.2.1.31至(R)-malate，记F；gold S01末端D-malate/3-isopropylmalate dehydrogenase至pyruvate未交付，记M。S=1、F=1、M=1、U=1，存在关键F/M，D-KEY4上界≤4；在&#91;1,4&#93;内因仅entry和部分hydrolase可用、关键失败边界清楚取3。

<details><summary>V0.4理由与本行变化背景</summary>

S1 gentisate 1,2-dioxygenase/EC 1.13.11.4与gold该步酶名及EC一致（gold参照层支持）；S2酶名maleylpyruvate hydrolase与gold一致，但EC 3.7.1.9与gold 3.7.1.23冲突，E0无3.7.1.9记录（GAP-110-006），按四.5保守条款（官方条目不可核→UNRESOLVED、保留低分与待核、不判错不cap）；S3 maleate isomerase/EC 5.2.1.1在E0无记录（GAP-110-007）。三处酶名与EC大类、反应类型内部自洽（双加氧酶/水解酶/异构酶），但两个关键EC缺核验且一处与gold冲突→&#x27;有合理候选和部分支持，若干关键步骤仍缺具体核验&#x27;，5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：accepted酶集合：S04 gentisate 1,2-dioxygenase EC 1.13.11.4；S02 EC 3.7.1.23；S03 maleate hydratase EC 4.2.1.31；S01 D-malate/3-isopropylmalate dehydrogenase EC 1.1.1.83/4.1.1.112。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：gold S03为maleate+H2O至(R)-malate；S01为末端pyruvate生成；不支持maleate isomerase至fumarate作为目标S03。
- ANSWER_TEXT / ANSWER.steps：答案仅给S1-S3；S3的酶/反应与accepted S03不同，S01缺失。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> P. alcaligenes种级在gold S02/S03/S04及PATHWAY_COMPLETE中出现，种级身份和完整路径能力有支持；但答案写菌株NCIMB 9867，gold可见物种名、TaxID 43263和GCA_001597285.1，未直接给出该菌株token，属物种级支持菌株级声称的粒度不足。按D3b身份阶梯7档附近取7；主要微生物推荐未被推翻，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份获gold支持：organism_gold在本题S04（gentisate 1,2-dioxygenase，EC 1.13.11.4）、S02（maleylpyruvate hydrolase）、S03（maleate hydratase）步骤均记录Pseudomonas alcaligenes（种级，TaxID 43263），答案三步统一归属该种、与gold种级记录不冲突，不因实验菌株与代表株不同而判错（四.4）。但答案给出菌株NCIMB 9867、taxid=null：gold trait_gold对43263的保藏号列表（DSM 50342|ATCC 14909|…|NCIMB 9945等）未含该号，也无TaxID/基因组记录，属身份阶梯①粒度不足+未核（档内扣、默认不cap，不判虚构）。S3 maleate isomerase的P. alcaligenes归属无gold反应级记录→作用范围未核。综合：主要物种对应有可靠支持，菌株粒度与一步能力未核→6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_110：P. alcaligenes taxid43263/GCA_001597285.1在PATHWAY_COMPLETE行且S02/S03/S04有STEP归属；支持物种级和路径能力，不直接确认菌株NCIMB 9867。
- ANSWER_TEXT / ANSWER.microorganism：答案每步均用P. alcaligenes NCIMB 9867，并声明complete_pathway_organism_profile_id=ORG_001。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 所有15项性状均以value=null、confidence=unknown返回；按P44全部必需性状为null/空值时D4记MISSING=1，不宣称检测到科学错误。完成度问题主要归D1，不在D4重复重扣。

<details><summary>V0.4理由与本行变化背景</summary>

15项必需性状全部以value=null交付（对象型亦整体null），raw_text、evidence_id为null，confidence均为unknown，模块内没有任何可评价的性状数值、单位、条件或适用性内容。按rubric P44（&#x27;全部必需性状均为null/空值时同样处理——D4按MISSING记1分，不宣称检测到科学错误&#x27;）记MISSING=1，不宣称发现性状科学错误；完成度不足已在D1体现，不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles.traits：15项性状字段均存在但无任何可评价值；支持D4 MISSING判定，不支持任何性状正确性。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry的EVID_001-EVID_004全部为INTERNAL_KNOWLEDGE_ONLY，database、record_id、locator均为null；没有DOI、数据库条目、计算记录或可定位原文，属MISSING_SOURCE低分档。非已核实错引，按规则不cap，取2。

<details><summary>V0.4理由与本行变化背景</summary>

答案证据登记4条全部source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，无DOI、数据库条目或计算记录可与结论对应，按四.3属MISSING_SOURCE（&#x27;仅有INTERNAL_KNOWLEDGE_ONLY类自我声明&#x27;）。决策相关组（CG01/CG02/CG03/CG05/CG07）均无可定位条目级证据，重要结论依据几乎无法追溯→落1–2低分档；因答案至少逐条登记了claim_scope并如实标注内部知识（结构可读），取2。无经核实错引（无可核引用），故不触发错引cap，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION；EC 1.13.11.4/3.7.1.9/5.2.1.1在E0无记录（GAP-110-003/006/007），编号类声称保持UNRESOLVED待核，不判虚构。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案自报四条证据均为INTERNAL_KNOWLEDGE_ONLY且无外部定位；支持MISSING_SOURCE判定。
- E0_EVIDENCE / f3e0:ec:3.7.1.5：E0本题仅含EC 3.7.1.5 acylpyruvate hydrolase条目；不覆盖答案使用的EC 1.13.11.4/3.7.1.9/5.2.1.1，不能作为其外部来源。

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案把酶/反应confidence多标为high、菌标为medium，但来源仅INTERNAL_KNOWLEDGE_ONLY；uncertainties为空，未说明证据类型、限制或待验证点，整体多处过度确信。15项性状null/unknown是诚实的正面因素，但不足以抵消主链披露不足；按3–4档取4，非系统性误导，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

正面：全部证据条目显式标注source_type=INTERNAL_KNOWLEDGE_ONLY（证据性质未被伪装成实验观测），15项性状诚实填null且confidence=unknown，未用编造值填满字段。负面：三处酶/EC声称仅凭内部知识却标confidence=high、菌株关联标medium（多处结论强度超过依据），uncertainties为空、未写明任何限制、待核点或与gold路线的差异；对EC编号未提示需核对官方条目。属&#x27;有不确定性说明但过于笼统、部分结论强度仍超过依据&#x27;，且非系统性把预测写成实证、无明知掩盖证据→5–6档取5，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案uncertainties为空数组；未提供主链限制、证据类型或待验证点说明。
- ANSWER_TEXT / ANSWER.evidence_registry：来源类型均为INTERNAL_KNOWLEDGE_ONLY，但酶/反应confidence标high；支持过度确信判定。

</details>

## Kimi

答案SHA256：`f49073c797d3c143869ba7aa2225bada643b466149a63a092aa9ac29462ac6d7`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 答案交付了可解析的路径、酶、微生物、15项性状、来源与不确定性模块，主模块均有涉及；但指定主链为4步，答案仅给3步，缺gold S01（D-malate/3-isopropylmalate dehydrogenase至pyruvate的末端步），并在S03替换为不同反应。因此属主要模块有涉及但若干必要内容遗漏/关联不符，定5分。

<details><summary>V0.4理由与本行变化背景</summary>

三步均给出主底物/主产物英文名与SMILES、一个首选酶、一个对应微生物；同一菌按物种去重为单一ORG_001并由各步引用；15项性状全部出现（12项有值、3项显式null且confidence=unknown、0项遗漏）；route_scope.chosen_route_name原样回填题面路线名，另附氧条件推断说明与范围声明。扣分点：第2步酶缺EC（题面明确要求&#x27;一个首选酶及EC&#x27;）；菌株与TaxID全为null、温度无最小/最适/最大数值、基因组信息整体null，属必要内容的部分缺位而非模块缺失，故列7–8档并取偏高分8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_110：formal_cases记录本题LINEAR_UNIQUE、ordered_step_count=4，用于核对必答主链长度；不证明答案任何一步化学正确。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_110：记录root为2,5-Dihydroxybenzoate、terminal main product为Pyruvate；用于D1终点完整性核对，不扩展到其他性状。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> S1（gentisate 1,2-dioxygenase开环）与S2（maleylpyruvate hydrolase水解）在答案自身路线中化学上大体连续且可辨认；S3用maleate isomerase将maleate转为fumarate，反应本身可成立，但不是题面指定路线中S03的maleate hydratase→(R)-malate，并且缺S01的D-malate→pyruvate末端转化。主干仅部分成立，关键转化与终点仍需实质修订，定6分。

<details><summary>V0.4理由与本行变化背景</summary>

S1为龙胆酸1,2-双加氧酶催化芳香环1,2-位开环，O2以cofactor在列，与gold S04（gentisate+dioxygen→3-maleylpyruvate）一致；S2为maleylpyruvate水解为maleate+pyruvate并含水，与gold S02一致，且答案对&#x27;谷胱甘肽非依赖&#x27;的定性符合gold路线Ⅱ的界定；S3以马来酸异构酶（EC 5.2.1.1）把maleate异构化为fumarate，与gold gentisate degradation II的S03 maleate hydratase（EC 4.2.1.31）→(R)-malate及S01脱羧脱氢酶→pyruvate段不同。按四.5四步判断：题面仅给路线名、未给终点，答案明确声明了路线与范围并给出文献级依据；S3属&#x27;未证实变体&#x27;而非错误起始步、无依据跳步或不守恒，主链与关键前两步成立，故不cap，在7–8档内取低分7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：列出S04 gentisate→3-maleylpyruvate、S02 3-maleylpyruvate→maleate+pyruvate、S03 maleate→(R)-malate、S01 (R)-malate→pyruvate的定向反应；用于比较答案转化与连接，不证明替代反应在本题任务中可计目标信用。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> N=4。S04对应步（答案S1 gentisate 1,2-dioxygenase EC 1.13.11.4）与S02对应步（答案S2 maleylpyruvate hydrolase，缺EC但名称命中）有可核功能支持；S03为KEY内部步，答案给maleate isomerase EC 5.2.1.1，而gold accepted为maleate hydratase EC 4.2.1.31，属关键酶-反应不符；S01为KEY_TERMINAL，答案未交付D-malate/3-isopropylmalate dehydrogenase步骤。KEY失败/实证缺失触发D-KEY4上界4，在&#91;1,4&#93;内因可用目标有限且关键失败清楚取3。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶名gentisate 1,2-dioxygenase与EC 1.13.11.4与gold关键酶一致，反应类型（双加氧开环）匹配；S2酶名maleylpyruvate hydrolase与gold一致，但ec_number留null并称&#x27;未见公认EC编号&#x27;，与gold所列EC 3.7.1.23不符（见FV-04），属关键步骤EC信息缺口加一处负向过度断言；S3 maleate isomerase与EC 5.2.1.1的顺反异构化反应类型自洽，但该EC在E0无记录，只能UNRESOLVED待核。三个酶—反应对应本身均无误配，故不构成D3a关键错误；因存在关键步骤EC缺口与一处与gold相左的负向断言，在7–8档取低分7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：列出S01 accepted D-malate/3-isopropylmalate dehydrogenase (EC 1.1.1.83/4.1.1.112)、S02 maleylpyruvate hydrolase (EC 3.7.1.23)、S03 maleate hydratase (EC 4.2.1.31)、S04 gentisate 1,2-dioxygenase (EC 1.13.11.4)；支持目标酶身份核对，不支持答案S3的EC 5.2.1.1或缺失的S01。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_110：terminal main product为Pyruvate，用于判断S01/KWY终端步缺失；不证明M. osloensis对该路线的活性。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案全链使用Moraxella osloensis（无strain、无TaxID），并以该种作为complete_pathway_organism_profile。M. osloensis是合理候选，且答案给出Crawford 1975/1977及Bergey&#x27;s引用支持其gentisate途径；但E0无M. osloensis organism/trait记录，S2、S3步骤归属confidence low，完整路径能力声称未获冻结证据核验。属合理候选+部分支持但关键身份/作用范围未充分核验，定5分。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份Moraxella osloensis为真实且已知的龙胆酸降解菌，S1（龙胆酸1,2-双加氧酶）有1975年纯化研究的文献线索，属身份定位＋单步能力层；但菌株、TaxID、保藏号粒度不足（strain/taxid均null，保藏号仅出现在性状F5），S2水解与S3异构化对M. osloensis的归属基本依赖&#x27;该菌走谷胱甘肽非依赖途径&#x27;的路径级外推，答案自评low并作披露；同时complete_pathway_organism_profile_id=ORG_001把整条路径能力归于一株菌，属三层声称中最高层的未充分核验外推。非编造物种、非跨属/跨kingdom错配，故不触发八.D3b身份阶梯的cap；按&#x27;有合理候选和部分支持，但若干关键身份或作用范围未充分核验&#x27;列5–6档并取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_110：列出gold步骤对应菌及complete pathway菌Pseudomonas alcaligenes，未列M. osloensis；gold非穷尽，不能据此判M. osloensis为错。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 15项性状全部出现，12项填入、3项明确null；已给值（革兰氏阴性、不运动、球杆状、不产孢、好氧、ATCC 19976、以gentisate为碳源等）对M. osloensis大体合理，且答案对未知项诚实留null。但E0没有M. osloensis性状记录，ATCC 19976与Bergey&#x27;s/Crawford来源均未冻结核验，多个关键性状证据不足且raw_text缺失。属部分性状可核且适用、但关键证据不足，定5分。

<details><summary>V0.4理由与本行变化背景</summary>

已填12项性状与Moraxella osloensis的通行描述一致：革兰氏阴性、好氧（严格好氧）、不运动、球杆状成对、不产孢、好氧呼吸以O2为末端电子受体、龙胆酸作碳源、谷胱甘肽非依赖降解、含龙胆酸1,2-双加氧酶活性、栖居于人黏膜并有环境分离报道；F5 ATCC 19976为模式株的说法合理；pH、盐度、基因组三项以null＋confidence=unknown诚实交付，未编造数值。扣分点：所有性状均无raw_text，温度仅给偏好类别而无最小/最适/最大数值，全部依赖单一Bergey&#x27;s二级来源，且E0无该物种任何性状记录（GAP-110-027…035），故&#x27;关键性状已充分核验&#x27;尚不成立；在7–8档取低分7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_110：本题trait_gold仅含E. coli、Pseudomonas alcaligenes、Haloferax、Ralstonia、Streptomyces记录，无M. osloensis行；gold非穷尽，不能据此判答案性状错误，也不能回填为已核支持。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案提供evidence_registry并把步骤、酶、菌、性状逐项映射到EVID_001–EVID_006，形式上可追溯；但决定相关组（路线、关键酶、核心菌、完整路径）的来源多为MetaCyc页面名、Bergey&#x27;s条目、ATCC 19976或Crawford文献自由文本，E0中无法核验，登记为UNRESOLVED_SOURCE。没有经冻结证据核实的VERIFIED_MIS_CITATION，不cap；部分关键结论有映射但缺乏可核记录，定5分。

<details><summary>V0.4理由与本行变化背景</summary>

答案对每条结论都挂了EVID_001–EVID_006并写了claim_scope，属文献/数据库条目级定位而非纯库名罗列，关联强度合格。但统一冻结证据内：EC 1.13.11.4、EC 5.2.1.1、ATCC 19976均无记录（GAP-110-004/001/008/017/002），Crawford 1975/1977、Bergey&#x27;s、MetaCyc页均为自由文本未解析缺口（GAP-110-019/020/021/022），故决策相关组（CG01/CG02/CG03/CG05/CG07/CG09）没有任何一条关键结论在冻结证据内被正面核对，只能登记UNRESOLVED_SOURCE；CG01/CG19所用MetaCyc来源无record_id，兼有GENERIC_SOURCE性质。EVID_001所述&#x27;maleylpyruvate→maleate→fumarate&#x27;序列与gold gentisate degradation II（maleate hydratase步）不一致，属疑似错引，但冻结证据无法核验，登记UNRESOLVED、不cap、不计已核实关键错误。综合取5分（部分关键结论可定位、但均待核，其余模块缺可核条目）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:3.7.1.5：E0仅提供EC 3.7.1.5 acylpyruvate hydrolase条目；不支持答案引用的EC 5.2.1.1、EC 1.13.11.4、ATCC 19976或Crawford/Bergey&#x27;s内容，不能据此判答案错引。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确列出路线I/II编号可能对调、S2无公认EC、M. osloensis部分性状未知、SMILES质子化差异等不确定性，并对S2/S3使用low confidence；对未知字段大量诚实null，未系统性把预测写成实验。轻微问题是route_summary对M. osloensis完整路径表述较肯定，但整体披露具体且与证据强度基本相称，定8分。

<details><summary>V0.4理由与本行变化背景</summary>

答案设有专门uncertainties：明确指出gentisate degradation I/II编号可能对调并写出对调后的替代步骤（EC 5.2.1.4→EC 3.7.1.5）；说明S2缺EC；说明TaxID/基因组/温度/pH/盐度缺源而填null；提示SMILES质子化态差异。步级confidence与证据强度大体相称（S1酶high、S2 low、S3 medium，S2/S3菌归属low），alternative_branches明确标is_part_of_scored_main_route=false，符合&#x27;范围声明不计入主链&#x27;的规范做法。扣分点：以&#x27;未见公认EC编号&#x27;作负向断言而gold实有EC 3.7.1.23，属单点过度确信；&#x27;严格好氧/不运动/革兰氏阴性&#x27;等以medium呈现但未标明为二级资料转述。整体无系统性把预测当观测、无掩盖已知矛盾，故不cap，7–8档取高8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Qwen

答案SHA256：`fa80df0d077cc633cc25850ddbeb15dce1dcd00bca8294a4d5f32e627e7707ad`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> All major modules are present and JSON-valid, but the answer implements a different three-step gentisate route (maleylpyruvate isomerase/fumarylpyruvate hydrolase) rather than the required gentisate degradation II main chain. This is a route-lock/task-conformance failure, so D1 is capped in the weak-to-major-deviation band; score 3 given that modules are present but the main route requirement is substantially violated.

<details><summary>V0.4理由与本行变化背景</summary>

交付形态完整：三步均含主底物/主产物名+SMILES、首选酶+EC、对应微生物；15项性状字段齐全（8填7空）、证据与不确定性字段齐备，route_scope.chosen_route_name 原样填“gentisate degradation II”。但对其交付的化学路线与题面指定路线的符合度构成关键错误：冻结gold的 gentisate degradation II 主链为 gentisate→(EC 1.13.11.4) 3-maleylpyruvate→(3.7.1.23水解) maleate+pyruvate→(4.2.1.31水合) (R)-malate→(1.1.1.83/4.1.1.112氧化脱羧) pyruvate 共4步；答案交付的是 maleylpyruvate isomerase(5.2.1.4)→3-fumarylpyruvate→fumarylpyruvate hydrolase(3.7.1.2)→fumarate+pyruvate 的另一分支（3步），属“自称合规却交付不同化学路线”的任务参数偏离（量表P100/八.D1），触发本维关键错误，cap≤4；其余完整性良好，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_110：Gold case is gentisate degradation II, LINEAR_UNIQUE, ordered_step_count=4; this supports the required four-step main-chain scope, not the answer&#x27;s three-step alternative.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：Gold reactions support S04-&gt;S02-&gt;S03-&gt;S01 as the main chain; they do not support the answer&#x27;s alternative S1-&gt;S2-&gt;S3 chain as the task route.

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> The answer&#x27;s alternative three-step path is internally connected: gentisate ring cleavage to 3-maleylpyruvate, isomerization to 3-fumarylpyruvate, and hydrolysis to fumarate plus pyruvate. However, it is not the specified gentisate degradation II chemistry, and the exact EC 3.7.1.2 record is not in the frozen evidence. Under the D2 chemical range &#91;1,5&#93;, the route is partially plausible but requires substantial target-route/evidence revision; score 5.

<details><summary>V0.4理由与本行变化背景</summary>

对已交付主链的化学本身评价：第1步 gentisate+O2 开环生成3-maleylpyruvate，C7与O/H/电荷可配平（+H+），与gold首步一致；第2步顺反异构 maleyl→fumaryl 无原子变化；第3步 fumarylpyruvate+H2O→fumarate+pyruvate，C7=4+3、O6+1=4+3，加H+后守恒，产物含 pyruvate（gold 终点化合物），主链连续、方向合理。但该分支并非题面指定路线（gold 为 maleate 分支）的化学，且答案对替代分支未给任何可核证据（仅 INTERNAL_KNOWLEDGE_ONLY），按四.5第3步“未证实登记、不自动判错也不给高分”取5–6档，化学自洽性较好，档内取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：Gold shows the target main-chain reactions and direction for gentisate degradation II; it does not validate the answer&#x27;s alternative route as the target route.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> Program-fixed target states give S=0, F=1, U=3. The confirmed KEY failure at S02 (answer uses maleylpyruvate isomerase EC 5.2.1.4 instead of maleylpyruvate hydrolase EC 3.7.1.23) plus missing S01/S03 invalidates the target main route. Only the S04 enzyme/EC name-level match remains as limited local useful information, so within D-KEY4 &#91;1,4&#93; the score is 2, not 1, but the main recommendation remains unusable.

<details><summary>V0.4理由与本行变化背景</summary>

第1步 gentisate 1,2-dioxygenase / EC 1.13.11.4 与gold酶表逐字一致（同一酶名与EC），有可靠支持；第2步 maleylpyruvate isomerase / EC 5.2.1.4 功能类别（异构酶）与所写顺反异构反应自洽，但快照无记录（GAP-110-009）；第3步 fumarylpyruvate hydrolase 名称与水解反应合理，但 EC 3.7.1.2 无冻结记录（GAP-110-005），而E0官方条目 f3e0:ec:3.7.1.5 显示“3-acylpyruvate+H2O=羧酸+pyruvate”这一水解化学对应 acylpyruvate hydrolase（EC 3.7.1.5），提示第3步EC号可能错配；因3.7.1.2条目本身不在快照，按UNRESOLVED待核，不判错、不cap。综合“有合理候选和部分支持，若干关键步骤缺具体核验”，取5–6档，档内取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：Gold S02 reaction is 3-maleylpyruvate + H2O -&gt; maleate + pyruvate, not the answer&#x27;s isomerization to 3-fumarylpyruvate.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：Gold S02 accepted enzyme is maleylpyruvate hydrolase EC 3.7.1.23; S04 accepts gentisate 1,2-dioxygenase EC 1.13.11.4 at name/EC level.

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> Ralstonia sp. U2 is a real organism name present in gold for the S04 gentisate 1,2-dioxygenase step, but the answer assigns it to all steps and sets complete_pathway_organism_profile_id=ORG_001. Gold provides only S04 single-step association for Ralstonia sp. U2, while the PATHWAY_COMPLETE row is for Pseudomonas alcaligenes 43263. The whole-path capability claim is an unsupported single-step-to-whole-path extrapolation, so D3b is capped at ≤4; score 3 reflects limited identity/step support but invalid whole-path recommendation.

<details><summary>V0.4理由与本行变化背景</summary>

唯一推荐菌 Ralstonia sp. U2（strain U2）与gold organism_gold 中 S04 gentisate 1,2-dioxygenase 的 EXACT 匹配记录（TaxID 70356，Bacteria）一致，第1步菌-酶归属获可靠支持；答案未填 ncbi_taxid/基因组号，未出现异菌株或跨类群身份错配。但第2–3步（异构酶/水解酶分支）的菌株级归属无冻结记录，且 complete_pathway_organism_profile_id=ORG_001 的“整条路径能力”在gold中仅 Pseudomonas alcaligenes（43263）有 PATHWAY_COMPLETE 行，Ralstonia sp. U2 无该分支步级或全路径记录。属“有合理候选和部分支持，若干关键身份/作用范围未充分核验”，取5–6档，档内取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_110：Ralstonia sp. U2 rows are linked to S04 gentisate 1,2-dioxygenase; the PATHWAY_COMPLETE row is Pseudomonas alcaligenes 43263. This does not support a Ralstonia sp. U2 whole-path claim.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Eight traits are filled and seven are explicit null/unknown. F9 gentisate 1,2-dioxygenase activity has S04 single-step support for Ralstonia sp. U2, and several generic traits are plausible. However, F7 carbon-substrate utilization and F8 broad degradation capacity are key traits without strain-specific frozen support, and F1/F6/F11/F12/F13 rely on genus-level internal knowledge with low confidence. No observed numeric/unit conflict can be established, but key applicability/support is insufficient; score 5 is partial applicability with substantive unresolved key trait evidence.

<details><summary>V0.4理由与本行变化背景</summary>

15项字段齐全，8项填值（F1好氧、F6 aerobic/oxygen、F11杆状、F12革兰氏阴性、F13不产芽孢、F7 gentisate作碳源、F8可降解gentisate、F9 gentisate 1,2-dioxygenase活性），7项（温度/pH/盐度/保藏/运动性/基因组/栖息地）诚实留null，无编造数值，未见“预测冒充观测”；但填值均为属级一般性状与路径推导，全部来自 INTERNAL_KNOWLEDGE_ONLY 且自标low，trait_gold对 Ralstonia sp. U2（70356）全为UNKNOWN、mask标completeness_only，关键定量性状全缺；F9有gold酶-物种关联的部分支持。按“部分性状准确且适用但关键项证据不足”，取5–6档，档内取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_110：Ralstonia sp. U2 trait rows are UNKNOWN except the NCBI TaxID row; no observed values are provided for F1-F13/F15. Absence is not a contradiction.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_110：Supports Ralstonia sp. U2 at S04 gentisate 1,2-dioxygenase step level; it does not establish whole-path carbon-source or degradation-capacity traits.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_110：Most Ralstonia sp. U2 traits are completeness-only/not scoreable for observed accuracy in the frozen mask; this shows lack of observed denominators, not that the filled values are proven wrong.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> The answer&#x27;s evidence_registry entries EVID_001 and EVID_002 are source_type INTERNAL_KNOWLEDGE_ONLY with no database record_id and only internal locator descriptions. The pathway, enzyme, microorganism and trait claims are therefore MISSING_SOURCE, not verified mis-citations. This is the low traceability band; score 2 reflects a minimal local evidence mapping and honest internal-knowledge labeling, but no locatable external source for important conclusions.

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry两条证据（EVID_001、EVID_002）source_type均为 INTERNAL_KNOWLEDGE_ONLY，database与record_id为null，无DOI、条目、计算记录或可定位locator，全部决策相关组（CG01/CG02/CG03/CG05/CG07）均属 MISSING_SOURCE；按四.3/P34完全无引用或仅内知自我声明→D5低分档（1–2），且MISSING默认不cap。因答案对每个claim_scope做了结构化登记、未伪造可定位条目、也未作“已核实”式包装，档内取2而非1。无已核实错引，severity不适用。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:3.7.1.5：The E0 slice contains only the EC 3.7.1.5 record; it does not verify the answer&#x27;s EC 1.13.11.4/5.2.1.4/3.7.1.2 claims or the internal trait sources.

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer honestly nulls many unknown traits, labels internal-knowledge evidence, uses low confidence for generic traits, and lists uncertainties about oxygen condition and missing strain/collection/genome data. However, the main pathway steps carry medium confidence on internal knowledge only, and the answer does not fully delineate observation vs inference vs prediction for the route. This is partial uncertainty disclosure with some overconfidence in the main route; score 6.

<details><summary>V0.4理由与本行变化背景</summary>

答案逐条标了来源类型与置信度（EVID_001 medium、EVID_002 low），uncertainties明确列出“属级性状基于内部分类学知识、置信度低”“保藏/基因组/多数性状缺直接来源”“氧条件未指定”，诚实留null，未见把预测写成实证观测；但路线级把异构酶分支当作题面指定路线陈述、未披露该分支与 maleate 分支的差异，且整条主链的酶/反应/菌归属以 medium 置信度包装仅有内知的内容，属“部分结论强度超过依据”的局部过度确信而非系统性掩盖。按D6 5–6档取6，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / fa80df0d077cc633cc25850ddbeb15dce1dcd00bca8294a4d5f32e627e7707ad：Answer text contains the confidence, null/unknown, internal-knowledge and uncertainty declarations assessed for D6.

</details>

## Grok

答案SHA256：`1505408219b4d341409cbef57a30f3f45b873be10b68dba1c3abef643e77658c`。

### D1 完整性与任务符合度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定 gentisate degradation II，答案路线名正确，并交出 S1/S2、一个去重 ORG_001 及15项性状外壳；但任务范围4个必答步中仅覆盖入口 S04 与水解 S02，缺 S03 maleate hydratase 和终止 S01 D-malate dehydrogenase，且 S2 的 enzyme.ec_number 为 null，route_summary 将主链缩短。不是整模块缺失，故不记 MISSING/NE；属主要模块均有涉及但若干必要步骤遗漏，取5分。题面氧条件为 null 而答案填 aerobic 属额外假设，非主扣分点。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_110：ordered_step_count=4、LINEAR_UNIQUE、n_required=4、terminal=Pyruvate
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：gold 前向主链为 S04-&gt;S02-&gt;S03-&gt;S01；S02 的 pyruvate 角色为 BYPRODUCT；S03 为 maleate hydratase；S01 为终止步
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：必答步 accepted 酶包括 maleylpyruvate hydrolase EC 3.7.1.23、maleate hydratase EC 4.2.1.31、gentisate 1,2-dioxygenase EC 1.13.11.4 及终止步 D-malate/3-isopropylmalate dehydrogenase
- SCOPE_ROW / SCOPE#BIOPATH150_110#CG04：题面氧条件为 null（未指定）；答案填 aerobic 是额外假设

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1 的 2,5-dihydroxybenzoate + O2 -&gt; maleylpyruvate 与 S2 的 maleylpyruvate + H2O -&gt; maleate + pyruvate 化学上对应 gold S04/S02；但 gold 主链继续 maleate hydratase S03 与终止 D-malate dehydrogenase S01 至 pyruvate，且 S02 的 pyruvate 在 gold 中为 BYPRODUCT。答案止于 S2，把 pyruvate 作为主链终点并把 maleate 后续降为 downstream，导致核心连续性与终止转化不完整。已交付部分无方向反转或明显不守恒，故不落1-4；但缺关键下游使主链不能成立，不能给7-8，取5分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：S04 入口开环与 S02 水解可支持答案已交付两步；gold 随后 S03 maleate hydratase、S01 终止脱羧生成 pyruvate，且 S02 pyruvate 为 BYPRODUCT
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：S02 accepted EC 为 3.7.1.23；S03 为 4.2.1.31；S01 为 1.1.1.83/4.1.1.112；答案 S2 未给 EC
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_110：本案为4步 LINEAR_UNIQUE 主链，terminal=Pyruvate

</details>

### D3a 目标反应与酶对应：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer delivers two target enzyme functions: S1 gentisate 1,2-dioxygenase EC 1.13.11.4 corresponding to gold S04, and S2 maleylpyruvate hydrolase corresponding to gold S02. It omits required S03 maleate hydratase and the KEY terminal S01 (R)-malate dehydrogenase/pyruvate-forming step. Under D-KEY4 this key-terminal omission caps D3a at &lt;=4; within &#91;1,4&#93;, 4 is supported because the two delivered matches and the missing boundary are clear, but it is not a majority-success exemption.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：Lists S03 maleate hydratase and S01 D-malate/3-isopropylmalate dehydrogenase as gold required enzymatic steps; supports the required-step status, not the answer&#x27;s omitted chemistry.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_110：Shows the formal case has four ordered steps; supports the four-target denominator, not a determination that all branch material is required.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：Shows S04 and S02 reactions matching the two delivered steps and shows S03/S01 in the gold chain; does not establish the answer&#x27;s omitted steps as correct.

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P. alcaligenes is supported at species level for the delivered step organisms and as PATHWAY_COMPLETE in gold (taxid 43263). The answer&#x27;s strain NCIMB 9867 and its TaxID/genome are not independently verified, so species-level support for a strain-level complete-pathway claim is a minor identity deduction, not a cap.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_110：Gold supports P. alcaligenes (taxid 43263) for S02/S04 step organisms and PATHWAY_COMPLETE, but does not establish strain NCIMB 9867 or its TaxID.

</details>

### D4 性状科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Most delivered species-level traits match P. alcaligenes gold observations: obligate aerobe, mesophilic preference, motility, rod-shaped, Gram-negative, non-sporulating, and gentisate-pathway utilization. Several fields are explicit null, and the NCIMB 9867 culture collection/strain-specific values are unverified; this supports 7 rather than 8.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_110：Species-level P. alcaligenes traits support obligate aerobe, mesophilic, motility, rod shape, Gram-negative, non-sporulating, and pathway utilization; they do not prove NCIMB 9867-specific values or all unknown fields.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_110：Marks several trait subfields as completeness-only or pending adjudication; supports withholding high-tier credit while allowing species-level accuracy scoring.

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All answer evidence entries are source_type INTERNAL_KNOWLEDGE_ONLY. Some give database names/record IDs, but they are not delivered as externally locatable citations and cannot be checked against the snapshot. Decision-relevant groups are MISSING_SOURCE; this is a low traceability score, not a verified mis-citation cap.

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer is largely transparent: it flags the unspecified oxygen condition, route-variant uncertainty, missing MetaCyc check, no EC for maleylpyruvate hydrolase, strain-name history, and downstream maleate placement; many traits are explicit null. However, the statement that maleylpyruvate hydrolase has no confirmed EC is contradicted by gold EC 3.7.1.23, and some internal-only traits are labeled high confidence. This is a local overconfidence/evidence-labeling issue, not systemic.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：Gold lists maleylpyruvate hydrolase EC 3.7.1.23 for S02, contradicting the answer&#x27;s statement that no confirmed EC exists; it does not support systemic misrepresentation.

</details>

## GPT5.6

答案SHA256：`7d0dc7f6127155bbb6528b665d8b3bfe0ddbca4dd9caf9f891d2418883070e28`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定 gentisate degradation II，并要求给出该路线主链；答案虽原样回填 chosen_route_name，但实际交付的是 maleylpyruvate→fumarylpyruvate→fumarate+pyruvate 的替代分支，仅第1步对应 gold 入口开环，缺 maleate hydratase 与 D-malate/3-isopropylmalate dehydrogenase 等指定主链步；15项性状全为 null，多个中间体 SMILES 也缺失。属于严重任务/路线偏离叠加交付不完整，D1关键错误成立，按3–4档低端评3分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：该切片显示 gold 指定主链的步序与主要参与者为 S04 入口开环→S02 maleylpyruvate→maleate+pyruvate→S03 maleate→(R)-malate→S01 (R)-malate→pyruvate；用于核对答案实际路线偏离，不作为全图旁支自动分母。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：列出各 gold 步 accepted 酶名/EC（gentisate 1,2-dioxygenase、maleylpyruvate hydrolase、maleate hydratase、D-malate/3-isopropylmalate dehydrogenase 等）；仅支持名称—EC层面的路线对照，不证明任何具体菌株实验活性。

</details>

### D2 反应化学科学性：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按答案自身化学独立评价：S1 gentisate 1,2-dioxygenase 开环生成 maleylpyruvate，S2 maleylpyruvate 异构化为 fumarylpyruvate，S3 fumarylpyruvate 加水分解为 fumarate+pyruvate，方向连续且起于污染物、止于中心代谢物，主链转化整体化学上可成立。主要扣分点是 maleylpyruvate/fumarylpyruvate 等中间体未给 SMILES、S3未显式配平H+、结构级支持不足；这些是局部问题，且路线与题面指定路线不一致归D1，不在D2重复扣。D2 未达9–10的结构与支持完整性要求。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案原文中的三步底物/产物与反应类型；用于评价所答化学的连续性、方向与局部缺口，不作为外部证据支持其正确性。
- RUBRIC_CLAUSE / TABLE0-D2：D2 7–8档：主链及关键转化有充分依据，少量局部问题不改变主要结论；9–10尚要求结构与连接均获可靠支持。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 四必答目标中仅S04入口步可判为与答案S1的gentisate 1,2-dioxygenase/EC 1.13.11.4对应；S02/S03目标反应被异构酶/水解酶步骤替代，S01终端malate dehydrogenase缺失。按C04计数S=1、F=2、M=1，C=0.25落&#91;3,4&#93;；仅少数目标可用且主链严重受损，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_JSON：显示答案仅三步及其酶/EC与反应；不证明其匹配全部必答目标。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_110：给出S04→S02→S03→S01目标反应、方向与终端；支持判断S02/S03/S01未按目标交付。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_110：给出各必答步accepted酶/EC；支持S02=3.7.1.23、S03=4.2.1.31、S01=1.1.1.83/4.1.1.112，而答案S2/S3为不同酶。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 物种Pseudomonas alcaligenes与gold中S02/S03/S04及PATHWAY_COMPLETE的P. alcaligenes一致，可作部分支持；但答案无strain/TaxID，且把P. alcaligenes用于其替代S2/S3步骤，步骤级能力未在冻结证据中核验。属合理候选+部分支持、若干能力未充分核验，取5-6档的上沿6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_JSON：显示三步均用P. alcaligenes、无strain/TaxID。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_110：支持P. alcaligenes出现在gold S02/S03/S04及PATHWAY_COMPLETE；不覆盖答案S2/S3替代酶的步骤级能力，也不支持菌株级身份。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题目要求15项性状；答案organism_profiles&#91;0&#93;.traits的F1-F15全部为null/unknown，未交付任何可评价的性状值或来源。按P44，全部必需性状均为null/空值，D4记MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_JSON：显示15项性状均为null/unknown，无具体值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_110：列出该case可评分性状范围；不提供答案性状值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案evidence_registry的EVID_001-EVID_004全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；decision-relevant各组只能登记MISSING_SOURCE。无已核实错引，默认不cap；因有局部claim_scope映射但无外部可定位来源，取低档2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_JSON：显示四条证据均为内部知识、无外部定位。
- E0_EVIDENCE / f3e0:ec:3.7.1.5：E0仅含EC 3.7.1.5记录；不核验答案EC 1.13.11.4、5.2.1.1、3.7.1.9，也不支持其外部来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确把证据标为INTERNAL_KNOWLEDGE_ONLY，酶/菌置信多为low或medium，性状均为unknown；uncertainties列出氧条件未指定、中间体结构未确认、缺菌株级直接来源。未见把预测写成实证或掩盖矛盾；局部仅缺逐声称的预测/观测标签，取7-8档上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_JSON：显示内部知识来源、低/中置信与未知披露；不证明科学结论正确。

</details>
