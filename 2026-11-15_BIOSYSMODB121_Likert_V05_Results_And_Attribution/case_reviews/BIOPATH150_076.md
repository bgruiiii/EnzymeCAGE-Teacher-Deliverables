# BIOPATH150_076：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：gentisate degradation I

污染物：2,5-Dihydroxybenzoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 68 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 51 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 66 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 61 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 69 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 52.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`a5c46678fc0f611a60108701205f19e1ab163857639f67776eee0a7408520b7e`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 题面锁定 gentisate degradation I；答案给出三步连续主链 gentisate→maleylpyruvate→fumarylpyruvate→fumarate+pyruvate，每步含底物/产物英文名与SMILES、首选酶及EC、对应微生物；同一 Ralstonia sp. U2 去重为单一 profile，15项性状均出现，未知项按 null/unknown 处理。未见任务路线偏离或关键模块缺失，按 D1 9分。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的模块均实质交付：3步主链逐步给出主底物/主产物英文名+SMILES、首选酶+EC、对应微生物；organism_profiles按物种+菌株去重为1条并由step引用；15项性状字段齐全（8项填写、7项显式null且confidence=unknown，按P15/P45属明确未知而非遗漏）；evidence_registry与uncertainties均给出。route_scope.chosen_route_name原样为“gentisate degradation I”，无更换路线、无任务参数偏离、无范围偏离；扣分仅因性状完成度不足（7/15未知），非格式或模块缺失。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_076：指定路线为 gentisate degradation I，终点为 Fumarate|Pyruvate
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_076：LINEAR_UNIQUE，ordered_step_count=3，n_required=3
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：三步主链方向与主产物：gentisate→maleylpyruvate→fumarylpyruvate→fumarate+pyruvate

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 三步化学方向与 gold 主链一致：S1 为龙胆酸1,2-双加氧开环生成 maleylpyruvate，S2 为 maleylpyruvate 顺反异构生成 fumarylpyruvate，S3 水解 fumarylpyruvate 生成 fumarate 与 pyruvate；终点正确，O2/H2O 辅因子及谷胱甘肽说明基本到位。路线诊断对 entry step 仅标 charge notation representation boundary，不是已核化学错误；按 D2 8分（程序允许上界为8）。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold reaction_gold逐步吻合：S1 gentisate+O2经1,2-双加氧开环生成3-maleylpyruvate（Z型，SMILES与gold isosmiles一致）；S2谷胱甘肽依赖顺反异构化为3-fumarylpyruvate（E型，一致）；S3水解C-C键生成fumarate+pyruvate，与gold终产物一致。方向、连接与终点均正确，alternative_branches已标is_part_of_scored_main_route=false不混入主链。缺陷：S1产物写为二价阴离子但反应式未列H+、S3水解未列H+，属局部计量/辅因子缺陷（P103、锚点SC3的7–8档情形），不构成关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：三步有向反应及主产物：gentisate+O2→maleylpyruvate，maleylpyruvate→fumarylpyruvate，fumarylpyruvate+H2O→fumarate+pyruvate
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_076：根化合物 2,5-Dihydroxybenzoate 与终点 Fumarate|Pyruvate

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 逐目标核：S1/gold S02 为 gentisate 1,2-dioxygenase EC 1.13.11.4，accepted name/EC 对齐，功能支持较明确；S2/gold S03 名称属 maleylpyruvate isomerase 类，但显式 EC 5.2.1.8 与 accepted EC 5.2.1.4 不一致，冻结材料未提供可确认该号的EC记录；S3/gold S01 名称 fumarylpyruvate hydrolase 属 accepted 名称，但显式 EC 3.7.1.3 与 accepted EC 3.7.1.20 不一致且未核。无已确认 KEY 失败，不触发 D-KEY4；但两个 KEY 目标为 U，主酶对应仅部分可用，按 C04 JUDGE_REQUIRED 与 C05 5分。

<details><summary>V0.4理由与本行变化背景</summary>

S1 gentisate 1,2-dioxygenase + EC 1.13.11.4 与gold enzyme_gold逐项一致（酶名、EC、加氧开环功能匹配），得可靠支持；S2标EC 5.2.1.8、S3标EC 3.7.1.3，均与gold该两步的EC（5.2.1.4、3.7.1.20）不一致，但统一冻结证据中无这两个EC条目（GAP-076-008/019、GAP-076-005/015），无法核accepted name/reaction，按四.6/P66/P73记UNRESOLVED、不判错也不放行；两步的酶功能描述（GSH依赖顺反异构化、C-C水解生成fumarate+pyruvate）与gold反应内容一致。属“有合理候选与部分支持、关键步骤具体编号仍缺核验”的5–6档，取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_076：accepted酶名/EC：S01 fumarylpyruvate hydrolase EC 3.7.1.20；S02 gentisate 1,2-dioxygenase EC 1.13.11.4；S03 maleylpyruvate isomerase类 EC 5.2.1.4
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_076：目标路线与终点身份，用于限定D3a逐目标评价范围

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> organism_gold的S01/S02/S03 STEP行均以EXACT列出Ralstonia sp. U2（TaxID 70356），并存在该TaxID的PATHWAY_COMPLETE行(pathway_complete=TRUE)；答案逐步归属同一菌株、按物种+菌株去重且complete_pathway_organism_profile_id=ORG_001，与三层分叙要求不冲突；TaxID留null属诚实未知。不足：未给TaxID/基因组编号，步级文献引用未核，confidence仅medium，故落7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份与gold organism_gold完全吻合：organism_name=Ralstonia sp. U2、strain=U2，gold在S01/S02/S03三步骤行均有该菌EXACT匹配记录；PATHWAY_COMPLETE行taxid 70356 pathway_complete=TRUE，支持“完整路径能力”声称；三步归属同一菌并由单一profile去重引用，符合步级归属要求。未编造TaxID（null为如实缺失，属D1完成度问题而非身份错误）；“Pseudomonas sp. U2→Ralstonia sp. U2”沿革说明与gold命名一致。仅具体菌株级编号与基因证据待核，属“主要微生物对应与身份有可靠支持、少量条目需确认”的7–8档，取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_076：逐步列出Ralstonia sp. U2（TaxID 70356）对应S01/S02/S03酶记录并含PATHWAY_COMPLETE=TRUE；不证明具体蛋白实验活性，也不核验答案所引文献。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项中8项有值（F1/F6/F7/F8/F9/F11/F12/F13），7项明确null；有值项全部来自EVID_003内部知识或EVID_002未核文献，无raw_text、无条目级观测，且数值型性状（温度/pH/盐度/基因组）全null。trait_gold对Ralstonia sp. U2各性状为UNKNOWN、trait_scoreability_mask标completeness_only，无观测精度分母可判其错；按P46按合理性与支持程度定档：部分性状可用但关键项证据不足→5–6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

已给8项性状均为定性且方向合理（好氧；O2为末端电子受体；利用萘/水杨酸/龙胆酸；经gentisate途径降解芳香族；龙胆酸1,2-双加氧酶等活性；杆状；革兰氏阴性；不产芽孢），与Ralstonia属级常识一致；温度/pH/盐度/保藏/基因组等数值项一律null并标unknown，未编造数值、未把培养或单步观测外推为耐受极限（符合P113/P115）。但trait_gold对Ralstonia sp. U2（70356）F1–F13/F15全部UNKNOWN、trait_scoreability_mask为completeness_only，冻结证据无法核实这些性状，属“部分性状准确且适用、关键项证据不足”的5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_076：Ralstonia sp. U2(70356)各性状均为UNKNOWN，仅F14有TaxID观测；不能据此判答案性状错，也不能支持其具体取值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_076：标出U2各性状observed_value_present=FALSE、denominator_role=completeness_only；不构成本题观测精度分母。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 决策相关组（CG01/02/03/05/07/08/09）来源形态为：EVID_001仅库名MetaCyc无record_id（笼统）、EVID_003内部知识、EVID_002为无DOI/卷页的自由文本文献（答案自述未核对）；无任何record_id/DOI级可定位可核对结论，属“仅给笼统库名与文献列表、结论—来源关联弱”的3–4档；答案的来源类型标注与claim_scope映射清楚、无已核实错引，故取上沿4。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）无任何条目级可定位可核对来源：路线与S2/S3酶EC来自EVID_001（INTERNAL_KNOWLEDGE_ONLY，仅写库名“MetaCyc”，record_id/locator为null→MISSING_SOURCE），S1酶/菌身份/全路径能力来自EVID_002（记忆型文献，E0未解析，GAP-076-027→UNRESOLVED_SOURCE），一般性状来自EVID_003（内部知识→MISSING_SOURCE）。按P41决策相关组全部缺失/笼统且无条目级可核对证据→3–4档；未见经核实错引或虚构（EC 5.2.1.8/3.7.1.3、文献均查不到→UNRESOLVED，不判虚构），MISSING/GENERIC默认不cap，故不触发关键错误。答案的claim_scope映射本身较规范，取该档上限4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_EVIDENCE_REGISTRY：答案自交付的来源登记与不确定性披露；不含可外部核对的记录ID，不能作为已核条目证据。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案区分了观测/推断/未知：EC依内部知识、nagK/nagL归属不确定而留空、文献凭记忆未核、U2菌株生理性状无可靠来源一律null、TaxID未知、并提示Pseudomonas→Ralstonia分类学变动；来源类型标注INTERNAL_KNOWLEDGE_ONLY/LITERATURE_DIRECT与置信度大体相称。单点过强：S1的gene_or_protein=nagI标high且未加待核说明（其所依文献未核）。属单点过度确信而非系统性误导→7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据相称：uncertainties逐条说明EC编号凭内部知识未核库、nagK/nagL基因归属记忆不确定而留空、文献凭记忆卷页未核、菌株生理性状无可靠来源一律null、TaxID未知与学名沿革风险；每步uncertainty另说明底物书写形式、O2进入产物、GSH为辅因子等边界；未知与预测区分清楚，无把预测写成实证观测的系统性误导。仅个别处偏强：S1酶标confidence=high而其依据文献未核实（属P119单点过度确信，档内扣分），故取8而非9。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_UNCERTAINTIES：答案自交付的不确定性与置信度披露文本；用于评价证据性质表述，不作为科学正确性证据。

</details>

## DeepSeek

答案SHA256：`3282b5adb31ac3b5f03fc5ce9d4ccce950c96b58ff6fe7b7674f9e1c70cd5691`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> Main route, route name, three substrate/product steps, enzyme/EC and microorganism fields are present and systematically ordered. However the entire 15-trait module is only explicit null/unknown and the evidence registry is empty, so necessary modules are partly placeholder rather than substantially complete. This fits the 5–6 band; within it, score 6 because the main pathway and associations are clear and the missing trait content is explicit rather than fabricated.

<details><summary>V0.4理由与本行变化背景</summary>

路径、逐步酶、逐步微生物三个内容模块均实质交付（3步，每步含主底物/主产物+SMILES、enzyme+EC、microorganism），路线名按题面原样填写gentisate degradation I。但任务硬性要求的15项性状全部为null（仅confidence=unknown标注，filled=0/15），来源清单为空。属“主要模块均有涉及，但若干必要内容遗漏”档（5–6），因性状模块整体未交付取低端5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：Answer provides three ordered steps with substrate/product names, enzymes, ECs and a microorganism.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_076：Gold records a three-step linear main route for this case, not the full DAG background.

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The named chemistry follows the gold gentisate degradation I main chain: gentisate ring cleavage to maleylpyruvate, isomerization to fumarylpyruvate, then hydrolysis to fumarate and pyruvate. Direction and terminal products match the task. The first step omits dioxygen/H+ in the written reaction and the representation/charge notation is under representation review, so the 9–10 band is not met; within the 7–8 band, score 8 because the main chemical sequence and terminal conversion are clear and the defect is local.

<details><summary>V0.4理由与本行变化背景</summary>

三步主链与gold逐步一致：S1 2,5-二羟基苯甲酸根经gentisate 1,2-开环生成maleylpyruvate（产物SMILES与gold 4,6-dioxohept-2-enedioate连通性相同）；S2 异构为fumarylpyruvate（反式双键，与gold一致）；S3 水解为pyruvate+fumarate，终点即gold终点（BSY-c06675|BSY-c11414）。方向正确、无跳步、无违反化学约束。扣分点：S1未列dioxygen为辅底物（及H+），未给配平，属局部计量缺陷，按7–8档处理，不cap；取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：Answer&#x27;s step sequence and named substrate/product conversions.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：Gold reaction rows show the directed gentisate → maleylpyruvate → fumarylpyruvate → fumarate + pyruvate main chain.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_076：Gold case root and terminal products are 2,5-dihydroxybenzoate and fumarate/pyruvate.

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> All three delivered enzyme names/ECs match the accepted sets for the target steps: gentisate 1,2-dioxygenase EC 1.13.11.4, maleylpyruvate isomerase EC 5.2.1.4, and fumarylpyruvate hydrolase EC 3.7.1.20. This is function-level accepted/G4 support, not protein-specific experimental evidence. Optional gene/protein labels nagI/nagL/nagK remain unverified MINOR annotations and do not change the target-function match. High tier is blocked by the release range and representation hold; within 7–8, score 8.

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名与EC逐条与gold enzyme_gold吻合：1.13.11.4 gentisate 1,2-dioxygenase、5.2.1.4 maleylpyruvate isomerase（gold该EC下设glutathion-/mycothiol-dependent与cis-trans isomerase多个合法变体，答案用通用名+同EC不判错）、3.7.1.20 fumarylpyruvate hydrolase；反应类型（双加氧开环/异构/水解）与EC大类匹配。扣分点：EC官方条目与gene_or_protein（nagI/nagL/nagK）在冻结E0中无记录（GAP-076-001/003/006），答案亦未附任何来源，功能-身份细节未充分核验，故不给9–10。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.enzyme：Answer&#x27;s preferred enzyme names and EC numbers for each step.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_076：Gold enzyme rows list the corresponding enzyme names and ECs for the three target steps.

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> The answer uses Pseudomonas alcaligenes NCIB 9867 for all three steps and sets complete_pathway_organism_profile_id=ORG_001. Gold lists P. alcaligenes for the gentisate 1,2-dioxygenase step, so the species is a reasonable candidate, but the specific strain NCIB 9867 and the whole-pathway capability for the same strain are not verified in the given gold/E0 records, and no answer-side source is delivered. This fits the 5–6 band: reasonable candidate with partial support, but key strain/pathway scope remains unverified. Score 6.

<details><summary>V0.4理由与本行变化背景</summary>

物种身份Pseudomonas alcaligenes与gold organism_gold一致（EXACT，TaxID 43263，genome GCA_001597285.1，物种级），且gold中该种出现在本题gentisate 1,2-dioxygenase步（S02）。但gold中该种仅出现在该单步，而答案把同一菌株NCIB 9867用于全部三步，并置complete_pathway_organism_profile_id=ORG_001（全路径能力声称）；菌株NCIB 9867无冻结记录、答案未附任何步级反应能力或全路径证据，构成“单步支持向整条路径能力扩展”的未核扩展。属“有合理候选和部分支持，但若干关键身份或作用范围仍未充分核验”（5–6档），取6；疑似问题登记UNRESOLVED，不按已核实关键错误cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism：Answer assigns Pseudomonas alcaligenes NCIB 9867 to every step and claims ORG_001 as complete-pathway organism.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_076：Gold step rows include P. alcaligenes for one gentisate dioxygenase step but do not provide a strain-level NCIB 9867 full-pathway record.

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> All 15 required trait fields are present but every value is null and confidence unknown. Under the all-null/empty trait rule, D4 is MISSING with score 1 and is not treated as a detected scientific error. The missing module is the entire required trait value set.

<details><summary>V0.4理由与本行变化背景</summary>

任务要求每个profile一次返回全部15项性状；答案organism_profiles&#91;0&#93;.traits中F1–F15全部为value=null（confidence=unknown），未交付任何可评性状数值/条目。按量表四.4/P44“全部必需性状均为null/空值时D4记MISSING=1分，不宣称检测到科学错误”。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：All 15 trait values are null; no trait observation, prediction or source is delivered.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> The answer does not deliver any source records: evidence_registry is empty and all step/enzyme/microorganism/trait evidence_id fields are null. Thus the route, enzyme, microorganism and trait claims cannot be traced to answer-side sources. This is MISSING_SOURCE, not a verified mis-citation, so no D5 key-error cap applies. With almost no traceability, D5 is in the 1–2 band; score 1.

<details><summary>V0.4理由与本行变化背景</summary>

答案evidence_registry为空数组，全部step.reaction_evidence_id/trait_evidence_id、enzyme.evidence_id、microorganism.evidence_id与各性状evidence_id均为null，未交付任何可定位文献/数据库条目/计算记录。按四.3六状态，决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）与支持组均登记MISSING_SOURCE；MISSING_SOURCE是缺失而非误导，默认不触发cap，但“几乎无法定位重要结论依据”落1–2档，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Answer&#x27;s evidence_registry is an empty array; no source records are delivered.

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> The answer explicitly marks all trait values as unknown/null, which is honest, but it gives high confidence to three enzyme claims and medium confidence to the microorganism despite delivering no sources, and it provides no uncertainty narrative explaining evidence type, limitations or the representation hold. This is partial uncertainty disclosure with some confidence exceeding delivered evidence, fitting the 5–6 band; score 5.

<details><summary>V0.4理由与本行变化背景</summary>

正面：15项性状以value=null+confidence=unknown诚实留空，未编造。负面：三步酶全部confidence=high且evidence_id=null，微生物标medium亦无任何来源；uncertainties为空数组，未说明菌株NCIB 9867身份待核、未说明全路径能力无独立证据、未披露任何限制或替代路线。属“多处过度确信、主要限制未说明”（3–4档），取4；未达到系统性误导（全程零披露且掩盖已知矛盾）的cap门槛，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.confidence：Answer labels enzyme claims high confidence and microbe claims medium confidence while delivering no source registry.
- ANSWER_TEXT / ANSWER.uncertainties：Answer&#x27;s uncertainties array is empty; no narrative limitation or evidence-type statement is delivered.

</details>

## Kimi

答案SHA256：`01485ec5638361f59541ad418ba823e0790188bfe86237727fc1614f70dbbe0c`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 三步主链按order 1–3给出（gentisate→maleylpyruvate→fumarylpyruvate→fumarate+pyruvate），每步含主底物/主产物英文名+SMILES、一个首选酶+EC、一个对应微生物；单一去重菌株档案ORG_001被三步引用；15项性状外壳齐全（11项有值、4项整体null属题面允许的明确未知、0项遗漏）；chosen_route_name逐字回显gentisate degradation I，氧条件按题面null处理。无模块缺失、无路线改选、无格式损坏。7–8档取8：内容完整、模块关联清楚，仅性状Null与中性酸SMILES等少量待完善；不因程序结构等价挂起就把完成度判为0或NE。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块实质回应：三步主链每步均给出主底物/主产物英文名与SMILES、一个首选酶含EC、一个对应微生物并引用同一profile；15项性状全部出现（11项填写、4项按题面要求诚实填null、无遗漏）；证据登记与不确定项清单各就位；route_scope.chosen_route_name 原样填写 gentisate degradation I，氧条件按题面null回填。仅存少量工程/计量层面小瑕（步骤式未列H+、性状有4项未知），未见模块缺失或范围偏离，故取9–10档且档内略偏下。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION#BIOPATH150_076：仅用于比对任务要求与交付范围；不证明任何科学声称
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_076：仅支持终点名称层面的对齐；不支持步骤SMILES电荷等价或具体催化
- ANSWER_TEXT / ANSWER#BIOPATH150_076：交付字段、顺序与覆盖情况的定位

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 逐主链自查：①gentisate(C7H5O4−)+O2→maleylpyruvate+H+，原子/电荷配平（H 5=4+1，O 4+2=6）；②maleyl(Z)→fumaryl(E)异构，原子不变；③fumarylpyruvate+H2O→fumarate+pyruvate(+H+)，C7=4+3、O 6+1=7、电荷−2=−2−1+1。方向均为底物→产物，O2/H2O作cofactor显式列出，终点与题面终点化合物一致，cis/trans构型标记正确，步骤衔接（前步产物=后步底物）自洽。局部缺陷：未列H+、SMILES以中性酸形式给出、异构酶GSH依赖性未写入反应式（已在uncertainties披露）。故给7–8档上沿8；本案未提供d2_nine_ten_evidence_ok门为真，9分不取。

<details><summary>V0.4理由与本行变化背景</summary>

三步化学与gold主链逐级吻合：①gentisate在双加氧酶作用下开环生成maleylpyruvate（O2列为cofactor，顺式构型与gold (2Z)-4,6-dioxohept-2-enedioate一致）；②maleylpyruvate经顺反异构生成fumarylpyruvate；③fumarylpyruvate水解生成fumarate+pyruvate，与gold终点化合物(Pyruvate|Fumarate)一致。方向、连接、原子计数与SMILES连通性均成立；仅未列H+（gold把H+作为小离子参与物），属局部计量/简化表达缺陷，按辅因子简化条款在9档内不降cap。未发现起始步错误、方向反转、无依据跳步或终点偏离。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：支持三步方向与主底物/主产物集合；不含SMILES电荷记法等价裁定
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_076：支持起点与终点化合物身份；不支持中间体结构等价
- ANSWER_TEXT / ANSWER#BIOPATH150_076：用于按答案自身结构核查守恒与连续性

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> D3a按三个必答目标步计。S1对应gold S02：gentisate 1,2-dioxygenase / EC 1.13.11.4与accepted集合一致；S2对应gold S03：maleylpyruvate isomerase / EC 5.2.1.4一致；两目标按功能及显式EC支持可判S。S3对应gold S01（KEY_TERMINAL）：酶名Fumarylpyruvate hydrolase在accepted名称集合内，但显式EC给3.7.1.5，而accepted为3.7.1.20；E0的3.7.1.5官方条目为acylpyruvate hydrolase且未列该名称，故名称—EC配对未核（U），不能判S，也未被合法证明为不相容F。表示/电荷待核不使整维NE；按S=2、U=1，覆盖率2/3，落入&#91;5,6&#93;。两个已支持步逐反应关联清楚，单一KEY终端EC配对待修明确但仍阻止进入良好档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶-反应对应总体成立：步骤1 gentisate 1,2-dioxygenase + EC 1.13.11.4 与gold一致；步骤2 maleylpyruvate isomerase + EC 5.2.1.4 与gold一致（gold该位点含GSH依赖/非依赖多注，答案取集合内通用号并在uncertainties声明GSH依赖性未确认，处置得当）；步骤3以“Fumarylpyruvate hydrolase + EC 3.7.1.5”交付，而冻结EC条目3.7.1.5的accepted name为acylpyruvate hydrolase/3-acylpyruvate acylhydrolase（反应：3-acylpyruvate+H2O=carboxylate+pyruvate），gold该步为EC 3.7.1.20——即酶名（特定名）与所给EC（广谱号）不精确配对。该步反应类型（水解、产物羧酸+pyruvate）仍正确，未出现EC大类与反应类型不匹配或把家族相关性冒充具体催化的情形，故按档内扣分处理、不触发本维cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;.enzyme：支持答案三步分别给出的酶名与EC：1.13.11.4、5.2.1.4、Fumarylpyruvate hydrolase/3.7.1.5。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_076：支持gold接受酶行：S02 gentisate 1,2-dioxygenase EC 1.13.11.4；S03 maleylpyruvate isomerase EC 5.2.1.4；S01 fumarylpyruvate hydrolase EC 3.7.1.20。据此S1/S2匹配，S3显式EC不符。
- E0_EVIDENCE / f3e0:ec:3.7.1.5：官方EC 3.7.1.5记录为acylpyruvate hydrolase，反应为a 3-acylpyruvate + H2O = a carboxylate + pyruvate；未列名称fumarylpyruvate hydrolase，亦不支持其等于gold accepted EC 3.7.1.20。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：支持本题三步主链及终点产物Fumarate/Pyruvate，用于确认D3a目标步数N=3与步对应；不直接证明具体酶EC配对。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案以单菌Klebsiella pneumoniae M5a1（TaxID 573）贯穿三步并置complete_pathway_organism_profile_id=ORG_001；三层分开核：身份（E0无TaxID 573记录，GAP-076-030/031）待核、单步能力（EVID_002纯化酶文献为自由文本未解析，GAP-076-026）待核、全路径能力（EVID_001称粗酶液三步活性，未解析，GAP-076-020）待核。无任何已核跨属/异菌株错配或无关类群，也未把单步证据冒充为已核全路径（来源显式绑定并标medium）。题面不要求单一代表菌，与gold步骤菌不同不构成错误。5–6档取6：身份与能力有合理候选与部分支持，但关键项仍未核验。

<details><summary>V0.4理由与本行变化背景</summary>

微生物层给出单一菌株 Klebsiella pneumoniae M5a1（TaxID 573），三步同株并在route_summary声明“其龙胆酸途径已有文献报道”。问题有二：其一，以物种级TaxID 573承载菌株级（M5a1）身份声称，属粒度不足（身份阶梯①），身份本身在冻结证据中无记录可核；其二，该株的反应级能力与整条路径能力全部依赖自由文本文献（Cooper &amp; Skinner 1980；Suárez 1996），E0未解析、无法核验，属“合理候选+部分支持但关键身份/作用范围未充分核验”。gold生物列表未含该菌（含的是Klebsiella michiganensis等），但gold非穷尽、且答案所用菌株来自其自引文献而非编造，不判跨属/无关类群错配、不触发cap。综合取5–6档且偏上：6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_076：列出本case冻结的步骤菌与全路径菌集合（不含TaxID 573）；不支持也未否证M5a1
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_076：支持各步反应-酶功能粒度；不提供任何菌株能力证明
- ANSWER_TEXT / ANSWER#BIOPATH150_076：定位身份与能力声称的原文

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项全部出现：11项有值、4项（F3/F4/F5/F14）整体null为明确未知、0项遗漏（filled+explicit_unknown+omitted=15）。有值项主要来自EVID_004=INTERNAL_KNOWLEDGE_ONLY（教科书层），F7/F8/F9来自未核文献；E0对TaxID 573无任何性状记录（GAP-076-038…045），gold同物种代表记录亦无K. pneumoniae，故无参照可核。数值/条件层面：F2把生长温度常识写成“最适约37℃”，按C07培养温度≠最适值，属条件解释需修订；F3/F4/F5/F14以null处理，未编造，符合题面纪律。5–6档取5：部分性状可用且适用性表述克制，但关键项证据不足、条件解释待改。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部出现：11项填写（F1兼性厌氧、F2最适约37℃、F6好氧呼吸/末端受体O2、F7龙胆酸等芳香酸碳源、F8多种羟基苯甲酸降解、F9龙胆酸1,2-双加氧酶活性、F10不运动、F11短杆菌具荚膜、F12革兰氏阴性、F13不产孢、F15栖息地广布），4项按题面诚实填null（F3 pH、F4盐度、F5保藏号、F14基因组）。填写项多为该物种教科书层面事实，方向大体可信且未把预测冒充观测（source_type自标INTERNAL_KNOWLEDGE_ONLY、F2/F15标low）；但全部无菌株级来源，F2最适37℃、F6呼吸方式等以物种级常识挂到M5a1菌株上且未声明物种—菌株粒度差，F7/F8把碳源/降解能力直接绑定目标污染物而仅凭自引文献。冻结证据中无该菌任何性状记录可核（trait掩码不含taxid 573），故按“部分性状准确且适用、关键项证据不足”取5–6档偏上：6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_076：本case性状记录仅覆盖gold菌株，不含TaxID 573；对答案性状既非支持也非反驳
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_076：说明各菌株性状可评分粒度；不含573行
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_076：示例范围/多值记录与文本类子字段不作数值准确度分母；不支持573

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 证据登记4条并逐步/逐性状绑定evidence_id，属部分映射；但核心EVID_001/EVID_002为无DOI/卷期的文献条目、EVID_003为无record id的MetaCyc页面名，E0均无对应记录可核→按UNRESOLVED_SOURCE登记（待核≠错引）；性状类10项依赖EVID_004 INTERNAL_KNOWLEDGE_ONLY，按P34记MISSING_SOURCE。无任何已核VERIFIED_MIS_CITATION_*，故不cap、严重度=NOT_APPLICABLE。决策相关组存在部分可定位的条目层级（作者/年份/期刊、页面名）但不可核对→5–6档取下沿5；若后续核验为支持可上调至6。

<details><summary>V0.4理由与本行变化背景</summary>

答案交付了可读的证据登记：路线化学指向具名MetaCyc路径页，酶指向具名文献（Suárez等1996）与路径页，菌株路径能力指向具名文献（Cooper &amp; Skinner 1980），化学结论与gold一致——具备“部分关键结论可定位”的形态；但全部条目缺record_id/DOI/卷期页与具体图段对应，性状段落仅INTERNAL_KNOWLEDGE_ONLY，且所引自由文本在冻结证据中一律无法解析核对（GAP-076-001/006/020/024/025/026/030/031/038–045）。无任何经核实错引：第三步EC配对差异只在事实层登记CONTRADICTED（见fact_verification_register FV-04），而所引MetaCyc页面本身不可查，故按UNRESOLVED_SOURCE处理、不计已核实关键错误、不cap。综合落在“部分可定位+其余模块缺映射”的5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:3.7.1.5：仅提供3.7.1.5官方字段，用于判断答案所称酶名-EC配对的核验状态，不涉及其文献链
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_076：显示冻结性状来源体系；不含573记录，不能用于核对答案性状来源
- ANSWER_TEXT / ANSWER#BIOPATH150_076：定位实际交付的来源记录与其claim_scope

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> uncertainties逐条写明：氧条件未指定故route_scope留null、GSH依赖性未确认、步2/3证据仅粗酶液水平、缺保藏/基因组编号故null、SMILES以中性酸形式给出；confidence按high/medium/low/unknown分级，未知项用null并标unknown，属观测/推断/未知的合理区分。单点过强：EVID_003以DATABASE_DIRECT+medium包装无record id的页面、TaxID 573以medium随行未标待核，属单点过度确信（P119档内扣），非系统性误导、无掩盖矛盾。7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体良好：uncertainties逐条点明氧条件按题面null、GSH依赖性未确认、步2/3证据仅粗酶液活性水平、缺保藏号与基因组、SMILES电离状态简化；证据登记用source_type区分文献/数据库/内部知识，未把内部知识包装成数据库直查。扣分点：F1/F6/F10/F11/F12/F13等以INTERNAL_KNOWLEDGE_ONLY支撑却标medium，F2最适37℃为物种级常识挂到M5a1菌株且未声明粒度差——属单点/局部过度确信，而非系统性把预测写成实证、亦无掩盖矛盾证据，故在7–8档内取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_076：用于评价证据性质标注与披露质量；不用于证明其内容真伪

</details>

## Qwen

答案SHA256：`16419565eaf266e1d60f7129f5c473db807666e4edf7b639b62f48bc908f710b`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 三条必答步、每步酶/EC、对应微生物及15项性状外壳全部交付；路线名原样，未知性状显式null，无任务条件偏离。少量性状为明确未知而非遗漏。

<details><summary>V0.4理由与本行变化背景</summary>

模块级完成度：①route_scope.chosen_route_name原样回填题面指定路线（仅大小写&#x27;i/I&#x27;差异），未改选其他路线；oxygen_condition按题面null填写；②3个step均给出主底物/主产物英文名+SMILES、首选酶名+EC、对应微生物及profile引用；③organism_profiles按&#x27;物种+菌株&#x27;单条ORG_001去重并由三步复用，未把同一菌重复登记；④15项性状全部以字段返回：填写10项、显式null未知5项（F2/F3/F4/F5/F14）、遗漏0项；⑤evidence_registry 5条与uncertainties 3条结构完整。扣分：微生物未给菌株、5项关键性状未知、无gene_or_protein与任何可定位记录；属&#x27;大部分必要内容完整、少量遗漏&#x27;档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_076：确认本题为线性3步、无背景步，供完整性核对；不支持对答案科学正确性的加分。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 主链方向为底物到终点，开环—异构—水解连续；O2与H2O作为辅因子列出，终点为fumarate与pyruvate，与gold三步主链一致。SMILES立体/电荷表示为局部简化，未改变主链化学结论。

<details><summary>V0.4理由与本行变化背景</summary>

按gold逐步比对化学：S1 gentisate(2,5-二羟基苯甲酸)+O2→maleylpyruvate，产物SMILES为Z-4,6-二氧代庚-2-烯二酸，与gold BSY-c12167结构等价；S2顺反异构→fumarylpyruvate（E式），与gold BSY-c12158等价；S3水解→fumarate+pyruvate，与gold BSY-c11414/BSY-c06675等价。起点、方向、三步顺序与终点均与gold一致（terminal=Pyruvate|Fumarate），O2与H2O作为辅因子在substrates中列出，并另列central_metabolism_entry/downstream_continuation把下游明确排除于主链之外。局部缺陷：S1未列H+产物、S2未标注异构酶的谷胱甘肽/霉菌硫醇依赖机制，属简化与局部计量缺陷（八.辅因子与简化反应式条款），不cap；取9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：支持gold主链的底物—产物方向与终点；不证明具体蛋白或菌株活性。

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 答案交付了3个必答目标步的酶信息：S1为gentisate 1,2-dioxygenase/EC 1.13.11.4，与gold目标步S02的accepted酶名和EC一致；S2为maleylpyruvate isomerase/EC 5.2.1.4，EC落在accepted集合内，但酶名不是accepted集中精确名称；S3为fumarylpyruvate hydrolase/EC 3.7.1.22，名称接近accepted名称而显式EC与gold/accepted的3.7.1.20不一致且未核。程序五态对所有目标均为UNRESOLVED，无已证F或M；S02另有表示/电荷边界待核。因此不能进入7–8档（全部主要目标未S且关键U存在），但并非全无可用支持：至少S02的酶名/EC、S3的酶名及S2的EC提供部分主干关联，故取5–6档下沿5。S3的EC非match属KEY_TERMINAL潜在问题，但无确认关键失败证明，不适用D-KEY4≤4。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名与gold一一对应：gentisate 1,2-dioxygenase（EC 1.13.11.4，gold BSY-e03356–e03359）、maleylpyruvate isomerase（EC 5.2.1.4，gold BSY-e03819 maleylpyruvate cis-trans isomerase）、fumarylpyruvate hydrolase（gold BSY-e02157/e02158）。前两步EC与gold完全一致且功能类别（双加氧酶/异构酶）与反应类型匹配；第三步EC写作3.7.1.22，而gold冻结值为EC-3.7.1.20，E0本题切片无3.7.1.22或3.7.1.20官方EC条目（item gap GAP-076-004，E0仅有3.7.1.5=acylpyruvate hydrolase），按四.5&#x27;gold单值与答案冲突且无法核验→UNRESOLVED，保留低分与待核标记、不cap&#x27;，档内扣分取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_076：Gold enzyme rows list the target-associated enzymes/ECs: S02 gentisate 1,2-dioxygenase EC 1.13.11.4; S03 maleylpyruvate isomerase family EC 5.2.1.4; S01 fumarylpyruvate hydrolase/3-fumarylpyruvate hydrolase EC 3.7.1.20. This does not verify the answer&#x27;s EC 3.7.1.22 or the exact non-listed synonym &#x27;maleylpyruvate isomerase&#x27;.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：Supports the target main-chain reactions and direction: gentisate + O2 -&gt; 3-maleylpyruvate; 3-maleylpyruvate -&gt; 3-fumarylpyruvate; 3-fumarylpyruvate + H2O -&gt; fumarate + pyruvate. It does not by itself resolve the answer&#x27;s name/EC pair or representation-bound target state.
- ANSWER_TEXT / ANSWER.steps&#91;0..2&#93;.enzyme：Answer claims step1 gentisate 1,2-dioxygenase EC 1.13.11.4; step2 maleylpyruvate isomerase EC 5.2.1.4; step3 fumarylpyruvate hydrolase EC 3.7.1.22.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> P. putida / TaxID 303的物种级身份名称有E0支持，但未给菌株；答案把同一种用于全部步骤并设complete_pathway_organism_profile_id=ORG_001，缺步骤级催化归属与全路径能力证据。属合理候选但关键作用范围未充分核验。

<details><summary>V0.4理由与本行变化背景</summary>

身份层：organism_name=Pseudomonas putida、ncbi_taxid=303与官方分类记录学名一致（SUPPORTED），strain=null为诚实未知，未编造保藏号/基因组号，无身份错配。能力层：三步催化归属全部落在同一物种且无任何菌株级或反应级证据；E0的12880为mt-2 PaW1(pWWO)菌株记录，只含保藏号与培养温度26/30°C，不含酶学或底物能力数据；complete_pathway_organism_profile_id=ORG_001的整条路径能力声称亦无证据（该字段本轮不评分，不作为能力证据）。gold步级菌为Ralstonia sp. U2、Bradyrhizobium sp. JS329、Haloferax sp. D1227等不同类群，但gold非穷尽，不能据此判P. putida错误。按&#x27;身份定位≠反应级能力≠完整路径能力&#x27;三层判定：有合理候选与身份部分支持、关键能力未核，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持TaxID 303的学名为Pseudomonas putida；不支持菌株、步骤酶归属或全路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_076：gold步骤微生物行未列P. putida；gold非穷尽，故不能据此判错，但也不能回填能力证据。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项外壳完整，10项填值、5项显式unknown；填值多为P. putida物种级低置信度概述，无raw_text或外部记录，F7/F8目标降解能力与F9酶活缺适用证据。无离谱数值，但关键项证据不足。

<details><summary>V0.4理由与本行变化背景</summary>

全部性状均来自INTERNAL_KNOWLEDGE_ONLY的物种层面一般知识（EVID_005，confidence=low/unknown），无任何可核记录：F1好氧、F6有氧呼吸/氧、F7可利用有机酸与芳香族化合物（含龙胆酸）、F8经龙胆酸途径降解2,5-二羟基苯甲酸、F9具三步酶活、F10有运动性、F11杆状、F12革兰氏阴性、F13不产芽孢、F15土壤/淡水/根际广适。核验侧：trait_gold无taxid 303行；E0的12880记录不含氧耐受、运动性、Gram、产孢、碳源定量等字段（其底物面板同化阳性项为malate/decanoate/gluconate/D-mannose/D-glucose，不含gentisate）。F2温度/F3 pH/F4盐度/F5保藏/F14基因组显式null属诚实未知，只计完成度（已归D1），不在D4重复重扣；无把预测写成观测、无把培养温度写成最适值，但关键数值性状空缺、能力性状（F7/F8/F9）无证据支撑，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_076：该gold切片未给TaxID 303的直接性状行；不能将物种级常识回填为答案来源。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> evidence_registry五条全部为INTERNAL_KNOWLEDGE_ONLY，无数据库条目、记录ID、DOI或稳定定位；决策相关claim组均MISSING_SOURCE，无法从外部核对。无已核实错引，不cap，按缺失来源低档。

<details><summary>V0.4理由与本行变化背景</summary>

逐组登记后，全部决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）仅由INTERNAL_KNOWLEDGE_ONLY自述证据支撑（EVID_001–EVID_005，database与record_id均为null，locator只是复述声称内容），按四.3属MISSING_SOURCE；性状组CG10/CG11/CG12/CG13/CG14/CG15/CG16同样无任何数据库条目/文献/计算记录。经核实无任何错引（无&#x27;引用存在但不支持&#x27;或编造条目），故不触发关键错误cap，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。按P41&#x27;全部缺失→低分档（默认不cap）&#x27;：答案至少有结构化的claim→evidence映射与诚实的来源类型标注，未伪造条目，故取低分档上缘3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 明确列出氧条件未指定、无具体菌株、性状按物种级低置信度填写、SMILES近似；多数未知/预测有低置信度标注。但complete_pathway_organism_profile_id与F8/F9仍把未核物种级能力写成可完成/具酶活，属单点过度确信，档内扣分不cap。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量：steps&#91;*&#93;.uncertainty逐条具体（氧条件题面未指定、SMILES立体化学简化、未指定菌株），uncertainties&#91;0..2&#93;明确说明氧条件未定、性状为物种层面一般知识且置信度较低、中间体质子化/立体化学近似；5项未知性状以value=null+confidence=unknown显式标注，未把预测/常识包装成观测；无掩盖矛盾、无对单一间接来源标high confidence。扣分点：酶与菌归属以INTERNAL_KNOWLEDGE_ONLY却标confidence=medium，属轻度偏高；未额外点明&#x27;P. putida的龙胆酸途径能力尚未核实&#x27;。整体披露具体、非系统性误导，按7档（&#x27;大部分观测/预测/未知被正确标注，主要限制已说明&#x27;）。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`9bb1a04601aa0aa217e1b708ef5abe104292db3a4c426625dd9ac80d81bc4151`。

### D1 完整性与任务符合度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步主链、每步底物/产物、酶/EC、对应微生物、15项性状字段与来源/不确定性均已交付；路线名保持题面指定。扣分主要因15项性状仅8项有值、7项明确未知，完成度不足，但未知项按题面允许填null，非格式缺失。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_076：答案实际交付的三步、性状、来源与不确定性字段；不扩展到未交付内容。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_076：gold显示本题为3步线性唯一主链；不表示所有15项性状均有观测值。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链方向与顺序正确：2,5-二羟基苯甲酸经龙胆酸1,2-双加氧开环为马来酰丙酮酸，再异构为延胡索酰丙酮酸，最后水解为延胡索酸与丙酮酸。关键转化、终产物与连接均与gold一致；氧/水辅因子已在列，谷胱甘肽作为不进入净计量的辅因子有说明。少量局部表示/电荷与质子未完全配平，故取7–8档上沿而非9–10。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：支持S02→S03→S01的主链转化、方向与终产物；不证明答案所有SMILES电荷/质子完全一致。
- ANSWER_TEXT / ANSWER#BIOPATH150_076.steps：答案实际给出的三步化学转化与辅因子说明。

</details>

### D3a 目标反应与酶对应：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a按本题N=3个必答目标步评价。答案三步均交付了可辨认的酶名/EC：S1为gentisate 1,2-dioxygenase EC 1.13.11.4，S2为maleylpyruvate isomerase EC 5.2.1.4，S3为fumarylpyruvate hydrolase EC 3.7.1.5。reaction_gold与enzyme_gold显示S02(EC 1.13.11.4)和S03(EC 5.2.1.4)的酶/EC与accepted集合相符，S01接受EC为3.7.1.20；答案S3所用EC 3.7.1.5在E0中为acylpyruvate hydrolase，并非已核实的fumarylpyruvate hydrolase=EC 3.7.1.20，故该KEY末端步的名称—EC配对仍为UNRESOLVED而非已证失败。S02结构诊断为charge notation待核，不能据此判错。整体看，两个目标步有可适用的accepted支持，一个KEY目标步存在具体待核EC配对缺口；无已证F/M，也无已确认关键错误，但存在KEY/MAJOR U，不能进入7–8分档。依C05在&#91;5,6&#93;内取6：已支持部分逐反应关联较清楚，待修/待核边界具体，但仍不足以进入良好档。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：本case三必答目标步的底物/产物、方向与顺序：S02 2,5-Dihydroxybenzoate+O2→(2Z)-4,6-dioxohept-2-enedioate；S03→4,6-dioxohept-2-enedioate；S01→Fumarate+Pyruvate。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_076：S02 accepted enzyme includes gentisate 1,2-dioxygenase EC 1.13.11.4；S03 accepted EC为5.2.1.4；S01 accepted EC为3.7.1.20（accepted name含fumarylpyruvate hydrolase/3-fumarylpyruvate hydrolase），不把EC 3.7.1.5直接列为S01 accepted匹配。
- E0_EVIDENCE / f3e0:ec:3.7.1.5：EC 3.7.1.5为ACTIVE，accepted names为acylpyruvate hydrolase/3-acylpyruvate acylhydrolase，reaction为a 3-acylpyruvate + H2O = a carboxylate + pyruvate；这可支持其催化酰基丙酮酸水解，但不能确认它就是S01 accepted的fumarylpyruvate hydrolase EC 3.7.1.20。

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步均指定Ralstonia sp. U2，gold organism行在S01/S02/S03均有该菌精确记录，PATHWAY_COMPLETE亦将TaxID 70356标为完整路径菌；身份与整路能力方向正确。答案未填TaxID/保藏号等身份编号，且来源依赖内部知识/未核文献，故取7–8档上沿而非9–10。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_076：支持Ralstonia sp. U2在各步的精确归属及PATHWAY_COMPLETE记录；不支持答案未交付的TaxID/基因组编号。
- ANSWER_TEXT / ANSWER#BIOPATH150_076.organism_profiles：答案实际给出的物种/菌株与整路能力声称。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已给的F1/F6/F7/F8/F9与Ralstonia sp. U2的需氧、萘/龙胆酸降解及nag酶活性方向一致；F11/F12/F13的杆状、革兰氏阴性、不产芽孢为属级外推且答案已披露。温度、pH、盐度、运动性、基因组和栖息地等关键项为null，冻结trait_gold对U2这些性状多为UNKNOWN，故只能给部分可用档：5–6，取6因已有值方向合理且外推有披露。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_076：显示Ralstonia sp. U2的F1–F15大多为UNKNOWN，仅F14有TaxID观测；不支持答案给出的具体性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_076：显示U2多数性状不可计观测准确率，仅可计完整性；不证明答案值错误。
- ANSWER_TEXT / ANSWER#BIOPATH150_076.traits：答案实际填写的性状值、null项与属级外推说明。

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 核心路线主要靠EVID_001（INTERNAL_KNOWLEDGE_ONLY，仅KEGG/MetaCyc笼统名称，无record_id/locator）；菌/酶/部分性状靠EVID_002（内部知识，但给出Zhou et al. 2001, J. Bacteriol. 183:700-708书目，可定位但E0未核验）；EVID_003为属级外推。决策相关组有部分可定位书目，但多数核心组仍缺条目级记录，故取5–6档下沿5；无已核实错引。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_076.evidence_registry：答案实际交付的三条证据记录及其source_type/locator；不扩展到未交付来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确区分观测/预测/未知：氧条件未指定但说明按路径需氧推断；TaxID、保藏号、基因组及菌株级温度/pH/盐度/运动性/栖息地等置null；革兰氏/形态/产孢标为属级外推；nagI/nagL/nagK对应关系说明为文献记忆未复核。不确定性与证据边界总体具体。扣分因EVID_002多项仍标high而实际未核，存在轻度证据强度偏高，未达系统性误导。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_076.uncertainties：答案实际披露的未知、推断、外推与未复核点。

</details>

## GPT5.6

答案SHA256：`bd8ddc35d8b93c36c5aec811e6f89ba2aa7e41d7b6da8e71c0bd6f1cb3d09df3`。

### D1 完整性与任务符合度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 路线名gentisate degradation I原样填写，3个步骤、每步酶/EC与对应微生物均已给出，15项性状字段齐全并诚实置null，JSON结构与route_scope符合。主要不足：S1主产物、S2底物与主产物、S3底物的SMILES均为null，中间体结构交付不完整；15项性状全部为未知，虽可按题面置null、且D1应反映完成度不足，但整体性状模块实质信息为空，仍需实质补全。故落在5–6档，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_076：该题冻结为LINEAR_UNIQUE、ordered_step_count=3，任务要求三步主链；不能据此要求全部旁支。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_076：根化合物为2,5-Dihydroxybenzoate，终点主产物为Fumarate|Pyruvate；支持任务范围核对。
- ANSWER_TEXT / bd8ddc35d8b93c36c5aec811e6f89ba2aa7e41d7b6da8e71c0bd6f1cb3d09df3：答案交付了3步、酶/EC、微生物及15项性状字段，但多个SMILES与全部性状值为null。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步主链化学顺序与方向正确：2,5-Dihydroxybenzoate经gentisate 1,2-dioxygenase开环为maleylpyruvate，再异构为fumarylpyruvate，最后水解为fumarate和pyruvate，终点与gold的Fumarate|Pyruvate一致；S1列入O2、S3列入H2O，步骤连续，无方向反转或核心化学断裂。局部问题为maleylpyruvate与fumarylpyruvate的SMILES未给出、S1/S3未列H+副产物，属于局部结构与计量表达缺陷，不改变主链结论；按7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：gold反应行给出S02 2,5-Dihydroxybenzoate+O2→3-maleylpyruvate、S03 3-maleylpyruvate→3-fumarylpyruvate、S01 3-fumarylpyruvate+H2O→Fumarate+Pyruvate，支持主链顺序、方向与终点核对。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_076：冻结终点主产物为Fumarate|Pyruvate，支持答案终点核对。
- ANSWER_TEXT / bd8ddc35d8b93c36c5aec811e6f89ba2aa7e41d7b6da8e71c0bd6f1cb3d09df3：答案实际给出三步转化、主底物/主产物名称及部分SMILES，可核对化学顺序与产物；中间体SMILES缺失属表达/结构信息不足。

</details>

### D3a 目标反应与酶对应：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按内容把答案3个酶声称与accepted集合比对：S1 gentisate 1,2-dioxygenase EC1.13.11.4=accepted；S2 maleylpyruvate isomerase EC5.2.1.4=accepted EC（名称较通用）；S3 fumarylpyruvate hydrolase名称=accepted但EC3.7.1.2≠accepted 3.7.1.20，且E0无3.7.1.2记录。三步功能对应均获G4策展级支持，2/3名号精确配对，terminal EC为局部缺陷；9–10因显式EC配对未确认被阻断，落7–8，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_076：accepted enzyme-EC pairs：gentisate 1,2-dioxygenase=1.13.11.4；maleylpyruvate isomerase=5.2.1.4；fumarylpyruvate hydrolase=3.7.1.20；不支持为terminal步填3.7.1.2
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_076：gold三步反应方向SUBSTRATE_TO_PRODUCT与产物（maleylpyruvate→fumarylpyruvate→fumarate+pyruvate）；不证明答案EC号

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部步骤与complete_pathway_organism_profile_id均指向Pseudomonas putida KT2440(taxid 160488)，EVID_002仅INTERNAL_KNOWLEDGE_ONLY。E0只有P. putida species(303)与mt-2 PaW1(12880)记录，无KT2440/160488身份或反应级/整路能力证据；P. putida为合理芳香降解候选但菌株身份、步级催化归属与全路径能力均未核验，且whole-pathway声称无支持。5–6档（合理候选+关键身份/作用范围未核）取5；whole-pathway过度声称作疑似关键问题登记但不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：官方Pseudomonas putida物种记录；不识别菌株KT2440/160488，不支持gentisate路径能力
- E0_EVIDENCE / f3e0:bacdive:12880：P. putida mt-2 PaW1菌株记录（培养温度/保藏号等）；非KT2440，不含路径能力

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles&#91;0&#93;.traits 的F1–F15全部为value:null、confidence:unknown，未交付任何可评价性状值；按P44“全部必需性状均为null/空值→D4按MISSING记1分，不宣称检测到科学错误”，取MISSING=1，权重保留。

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部关键结论（路径/酶/菌）仅由EVID_001/EVID_002支持，source_type=INTERNAL_KNOWLEDGE_ONLY、database/record_id/locator=null；按P34记MISSING_SOURCE（完全无引用/仅内部知识自我声明），D5低分档。无已核实错引，不cap。取2：存在evidence_id与claim_scope结构，但无任何可定位可核对来源。

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确标注confidence(low/medium/unknown)与source_type=INTERNAL_KNOWLEDGE_ONLY，uncertainties列出未填SMILES、菌株整链实验来源未定、部分EC/基因未定；基本区分内部推断与未知、主要限制已说明。次要问题：把主链表述为既定事实、未显式标“predicted/inferred”。7档（大部分证据性质与未知被正确标注，主要限制已说明）。
