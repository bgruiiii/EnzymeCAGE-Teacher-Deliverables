# BIOPATH150_070：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：3-chlorotoluene degradation II

污染物：3-Chlorotoluene；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 67.5 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 64 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 76.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 69.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 46.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 38.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`b359504e6b8b20d620bb7346215daea5a9481e4a5cb4bc0e4fdb4eea3ef2809d`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 题面路线名原样保留；gold主线3步（3-chlorotoluene→3-chlorobenzyl alcohol→3-chlorobenzaldehyde→3-chlorobenzoate）均被实质覆盖，每步给出底物/产物/SMILES/酶/微生物；两个profile按物种+菌株去重，15项性状均出现（10项填写，5项显式unknown/null）。扣分点：答案把3-chlorobenzoate之后的下游步骤也作为主链延伸呈现，虽不构成必要步骤遗漏，但范围表达偏宽；来源均internal-only。D1档位8。

<details><summary>V0.4理由与本行变化背景</summary>

输出覆盖完整：11步主链每步均给出主底物/主产物英文名与SMILES、一个首选酶（含EC，个别null）、一个对应微生物；两条organism_profiles各含15项性状槽位（未填项以value=null+confidence=unknown明确表达未知，非遗漏）；evidence_registry与uncertainties齐备；route_scope.chosen_route_name逐字为“3-chlorotoluene degradation II”。档内扣分点：①题面氧条件为null，答案自行填aerobic（已在notes与uncertainties披露，属轻微偏离登记口径）；②主链在gold终点3-chlorobenzoate之后续接8步下游（按四.2/P29额外下游延续不加分，不作扣分理由，但未置入downstream_continuation，边界表述可改）；③多条冻结证据可填的性状（F5保藏号、F14基因组、F2温度）留null。整体属“大部分必要内容完整，仅少量遗漏或工程缺陷”，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_070：gold路线名与终点3-Chlorobenzoate；支持任务边界，不证明答案正确。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_070：gold ordered_step_count=3、LINEAR_UNIQUE；支持本题必答主链长度为3，不把全图行数当分母。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_070：答案交付覆盖与字段完整性；不改写原文。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 前3步化学转化与gold一致且连续：甲基单加氧羟化、醇脱氢、醛脱氢至3-chlorobenzoate；终点化合物存在，中性/阴离子仅为电荷表示差异。S1缺O2/ferredoxin，S2/S3仅在reaction_type写NAD+而底物列表未列辅因子，属P103局部计量/表示缺陷，不自动cap；3-chlorobenzoate之后的下游不计入本题D2范围。D2档位8。

<details><summary>V0.4理由与本行变化背景</summary>

题面指定路线的3个必答转化化学正确且与gold逐步一致：S1 3-chlorotoluene→3-chlorobenzyl alcohol（甲基羟化）；S2 3-chlorobenzyl alcohol→3-chlorobenzaldehyde（醇脱氢）；S3 3-chlorobenzaldehyde→3-chlorobenzoate（醛脱氢），方向、SMILES与原子守恒均成立；终点3-chlorobenzoate按题面范围已完成（P29）。续接的下游clc修饰邻位裂解链（3-chlorocatechol→2-chloromuconate→内酯→脱卤→马来乙酸→3-酮己二酸→琥珀酰CoA+乙酰CoA）化学连贯合理，且明确标注为额外范围、alternative_branches排除路线I。扣分点：首步及S2/S3未列O2/铁氧还蛋白/NAD+等辅因子（按八.辅因子条款属7–8档局部计量缺陷，不cap）；S4将双加氧与脱羧合并为一步（已在uncertainty披露）；个别下游中间体SMILES为推断值。定7–8档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：gold S03→S01→S02有向反应与终点3-Chlorobenzoate；支持前3步转化和终点判断。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_070：答案前3步化学表达与辅因子缺省情况；下游超出终点不用于加分。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 按3个必答目标反应评D3a：S02的benzyl-alcohol dehydrogenase/EC 1.1.1.90与S03的benzaldehyde dehydrogenase/EC 1.2.1.28均与accepted_set的酶名—显式EC对应一致；S02的route_state仅因电荷表示挂起（CHARGE_NOTATION_ONLY），不构成化学错配。S01（entry）给出xylene monooxygenase/EC 1.17.13.-，而accepted为toluene methyl-monooxygenase/EC 1.14.15.26，显式EC与名称未获accepted支持，保持U。故为2个已核S、1个KEY/MAJOR U、无已核F/M；C=2/3落在&#91;5,6&#93;，支持步逐反应清楚但entry关键缺口明确，取6而非进入7–8。

<details><summary>V0.4理由与本行变化背景</summary>

必答3步的酶-反应对应有两项与gold逐字一致：S2 benzyl alcohol dehydrogenase EC 1.1.1.90/xylB、S3 benzaldehyde dehydrogenase EC 1.2.1.28/xylC；首步酶名称与基因（xylene monooxygenase，xylM/xylA）与官方EC 1.14.15.26记录的基因名一致，但给出的1.17.13.-为类级不完全编号且无冻结记录，属未核不判错。下游酶名-EC-基因多数自洽（5.5.1.7 clcB、3.1.1.45 clcD、1.3.1.32 clcE、2.8.3.6 pcaIJ、2.3.1.16 pcaF），EC缺失处如实填null。无经核实的酶名-EC矛盾或类别错配，故不触发关键错误；属“主要步骤酶对应有可靠支持，仅少量条目需进一步确认”，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：本题accepted酶行：S01 benzyl alcohol dehydrogenase 1.1.1.90；S02 benzaldehyde dehydrogenase 1.2.1.28；S03 toluene methyl-monooxygenase 1.14.15.26。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：S01–S03有向主链反应：S02的差异仅为电荷表示（route diagnosis: CHARGE_NOTATION_ONLY, jac_sub=1.0, jac_prod=1.0），不是已核化学错配。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：官方EC条目accepted name为toluene methyl-monooxygenase，reaction为toluene/p-xylene/m-xylene甲基羟化，并含xylM/ntnM基因名；不直接支持答案的EC 1.17.13.-/xylene monooxygenase声称。
- ANSWER_TEXT / S1：答案S1给出3-chlorotoluene→3-chlorobenzyl alcohol，酶为xylene monooxygenase，EC 1.17.13.-（不完整类级EC），未使用accepted的1.14.15.26。
- ANSWER_TEXT / S2：答案S2给出3-chlorobenzyl alcohol→3-chlorobenzaldehyde，酶为benzyl-alcohol dehydrogenase，EC 1.1.1.90，与accepted名称/EC对应一致。
- ANSWER_TEXT / S3：答案S3给出3-chlorobenzaldehyde→3-chlorobenzoate，酶为benzaldehyde dehydrogenase，EC 1.2.1.28，与accepted名称/EC对应一致。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 本题前3步均指派Pseudomonas putida mt-2，物种与gold organism_gold的Pseudomonas putida/TaxID 303一致；BacDive 12880为mt-2 PaW1(pWWO)菌株记录，支持菌株身份存在。TaxID 303本身为物种级，taxid记录不含strain token mt-2，故菌株级TaxID关联仅局部未核，不推翻主要微生物推荐。D3b档位8。

<details><summary>V0.4理由与本行变化背景</summary>

必答3步的微生物归属为Pseudomonas putida（mt-2），与gold organism_gold三行（303, Pseudomonas putida）物种级一致；TaxID 303与种名经官方记录核验为SUPPORTED。菌株级token“mt-2”在E0记录名称字段未出现（STRAIN_TOKEN_NOT_IN_RECORD_NAMES，UNRESOLVED），属D3b身份阶梯①粒度不足（物种级真实记录支持菌株级声称），默认不cap、档内扣。下游11步中8步归Pseudomonas sp. B13，E0无B13任何记录（GAP-070-085等），全部UNRESOLVED待核，不判虚构。答案未把单步支持写成整条路径能力，且明确声明B13不具备xyl上游、需协同，避免过度外推；complete_pathway_organism_profile_id=null亦未过度声称。综合取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_070：gold三步微生物均为Pseudomonas putida，TaxID 303；支持物种级身份，不自动证明mt-2菌株级TaxID记录。
- E0_EVIDENCE / f3e0:taxid:303：TaxID 303官方记录为Pseudomonas putida物种级；不支持strain token mt-2。
- E0_EVIDENCE / f3e0:bacdive:12880：BacDive 12880为Pseudomonas putida mt-2 PaW1(pWWO)菌株记录；支持菌株记录存在，不自动支持各步酶活或整路能力。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_070：答案实际菌名、菌株与TaxID填写。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> P. putida mt-2已给性状中，革兰氏阴性、杆状、不产芽孢、可运动、好氧呼吸/O2等与trait_gold观察项一致；温度/pH/盐度/保藏号/基因组等关键定量项多填null，按D1完整性处理，不在D4重复重扣。F7/F8/F9的具体甲苯/二甲苯底物表述及“不能厌氧生长”强于trait_gold的aerotolerant记录，属局部证据/条件问题，故D4为7。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状中可核验者均正确：ORG_001运动性“可运动（具鞭毛）”（trait_gold motility=true）、杆状、革兰氏阴性、不产芽孢（gram positive=false、sporulation=false）均为SUPPORTED；好氧/O2呼吸与gold观测（aerotolerant=true、nitrate respiration=false）不冲突；F7/F8/F9对TOL上游途径的描述与gold降解芳香烃背景一致。ORG_002按属级常识低置信度填写，未做菌株级定量外推。关键缺口：F5保藏号（冻结E0 bacdive:12880实含DSM 3931/ATCC 33015）、F14基因组（gold含GCA_024508115.1）、F2/F3/F4数值均留null，属完成度问题主归D1，D4按“部分性状准确适用、关键项证据不足”取7；B13全部性状无E0记录，登记待核。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_070：TaxID303观察性状：aerotolerant=true、motility=true、rod-shaped、gram positive=false、sporulation=false等；支持部分定性性状，不直接支持全部底物/氧表述。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_070：温度/pH/盐度等子字段的可评分掩码；缺失子字段不按错误计，仅影响完整性。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_070：答案实际性状值与null分布。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 答案所有EVID_001-EVID_005均为INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator，无法定位到任何外部条目或文献；decision-relevant组均为MISSING_SOURCE。没有可核实的错引，因此不触发D5 cap。D5低档1-2；因至少有局部claim_scope映射但无真实来源，取2。

<details><summary>V0.4理由与本行变化背景</summary>

轨迹性按claim group登记：全部5条evidence_registry均为INTERNAL_KNOWLEDGE_ONLY（无database、record_id、locator），按四.3属MISSING_SOURCE（缺失而非误导，默认不cap）；决策相关组（CG01/02/03/05/07/08）无任何条目级可定位可核对来源，故不入5–6档，评3–4档低端。正向可定位支持（3步化学与两步EC与gold一致、TaxID 303种名核验）仅登记在事实核验层，不改变原交付来源状态（OBS-POS-LOCATABLE）。多数EC与B13声称因E0缺口为UNRESOLVED_SOURCE性质，未见任何经核实的VERIFIED_MIS_CITATION，severity不适用。取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_070.evidence_registry：答案自交付证据记录；五条均为internal-only，无外部定位。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确区分internal knowledge、null、类级/不完全EC与未核对数据库，uncertainties列出入口EC、SMILES推断、步骤合并、TaxID未知等具体限制；未把预测系统性写成实证。route_summary有“经典文献”式强措辞，但uncertainties已披露未逐条核对，属局部表达问题。D6档位8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露较具体：uncertainties逐条列出氧条件推断、路线基于经典文献未逐条核对、内酯立体化学为推断值、脱卤酶基因/EC未知、EC类级编号、S4合并两步、菌株级信息缺失；各step.uncertainty多数明确，未知性状用null/unknown而非编造，confidence整体随证据走低（medium/low/unknown）。扣分点：S5–S9对B13的microorganism.confidence标high，而其唯一依据为INTERNAL_KNOWLEDGE_ONLY，属同一身份断言的单点/重复过度确信（P120同一根本断言不构成系统性），档内扣。未出现把预测系统性写成实证或掩盖主要矛盾，故不cap；定7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_070.uncertainties：答案不确定性披露原文；支持D6正面判断。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_070：答案整体证据性质标注与null处理。

</details>

## DeepSeek

答案SHA256：`8a235047836e6fc80d6994cda5efc93a4e1e930cbbfa9942e424567a953e3bc8`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 题面路线名原样回显(chosen_route_name=3-chlorotoluene degradation II)。必答3步(入口3-氯甲苯→3-氯苯甲醇、S01→3-氯苯甲醛、S02→3-氯苯甲酸)全部交付，每步均有底物/产物英文名与SMILES、首选酶+EC、对应微生物；两profile各15项性状全部出现，数值未知处用null/unknown而非编造。S4–S9超出gold终点3-氯苯甲酸，属额外下游延续：按P29不加分不扣分，其中S7–S9 SMILES与S5 EC缺失只作非必答字段的少量不完整记录。档位7–8，取8：必要内容完整、模块对应清楚，仅少量非必答遗漏。

<details><summary>V0.4理由与本行变化背景</summary>

全部任务模块实质交付：route_scope.chosen_route_name原样为&#x27;3-chlorotoluene degradation II&#x27;；9步主链每步均有英文名底物/产物（6步含SMILES）、首选酶（含EC或null）与对应微生物；2个organism_profile各含15项性状；同一菌去重（S1–S3属ORG_001，S4–S9属ORG_002）。扣分点：S7–S9的SMILES为null、S5的EC为null、两profile多项性状值为null（属题面允许的诚实未知），属少量遗漏而非范围偏离，落7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv：gold必答主链为3步；不支持把S4–S9下游计入必答分母
- GOLD_SLICE / case_root_identity.tsv：题面路线终点为3-氯苯甲酸；答案S3命中，额外下游不改变交付完整性判断
- ANSWER_TEXT / steps&#91;0-2&#93;：答案确实交付必答三步与两套15项性状

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 必答主链三步的结构、方向与连接均正确：3-氯甲苯甲基羟化→3-氯苯甲醇(OCc1cccc(Cl)c1)→3-氯苯甲醛(O=Cc1cccc(Cl)c1)→3-氯苯甲酸(O=C(&#91;O-&#93;)c1cccc(Cl)c1)，与reaction_gold的SUBSTRATE_TO_PRODUCT方向逐行结构MATCH；终点符合题面路线终点。首步缺O2/还原型铁氧还蛋白、脱氢步缺NAD+，按P103属局部计量/辅因子简化，不是原子不守恒或方向错误，不cap。额外下游S4–S9(修饰邻位裂解至3-氧化己二酸)化学上自洽但S7/S8/S9缺SMILES，不能完全核验；不属必答范围。因辅因子简化且本案d2 9–10证据门未确立，9–10不成立，取8。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3与gold主链逐步一致：3-Chlorotoluene→3-Chlorobenzyl alcohol→3-Chlorobenzaldehyde→3-Chlorobenzoate（=gold终点），方向、结构、SMILES与gold一致（3-氯甲苯SMILES确为间位氯）。S4–S9在gold终点之下继续延伸，走经典修饰邻位裂解途径（3-氯儿茶酚→2-氯粘康酸→trans-dienelactone→maleylacetate→3-氧代己二酸），化学自洽，属gold范围外延伸，按P29/四.2不进入覆盖率扣分。主要缺陷为全链辅因子缺失（O2/铁氧还蛋白、NAD+/NADH），按P103属局部计量缺陷，落7–8档，不cap；取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：三步主链底物/产物及forward方向；不支持答案下游S4–S9的化学自动成立
- GOLD_SLICE / enzyme_gold.tsv：参考反应对应；不证明具体蛋白实验活性
- ANSWER_TEXT / steps&#91;0-2&#93;：答案三步SMILES与gold结构一致；辅因子未列

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 按本题N=3的必答目标反应评价：答案S2=gold S01（benzyl alcohol dehydrogenase/1.1.1.90）、S3=gold S02（benzaldehyde dehydrogenase/1.2.1.28），均为accepted名/EC精确匹配，计S=2。答案S1=gold S03（3-chlorotoluene→3-chlorobenzyl alcohol）底物、产物与方向匹配，但酶标为xylene monooxygenase/1.14.13.169，不在accepted集合（gold/官方EC条目为toluene methyl-monooxygenase/1.14.15.26），冻结E0无1.14.13.169条目，故为UNRESOLVED_NONACCEPTED/U，不判F。C=2/3≈0.67→C04的&#91;5,6&#93;；无已确认KEY的合法F或实证M，D-KEY4不触发；入口KEY U阻止进入7–8/9–10。两个已支持目标逐反应清楚、待修入口明确，取6而非下沿5。答案S4–S9超出gold终点3-氯苯甲酸，属非本题3个目标反应，未计入D3a。

<details><summary>V0.4理由与本行变化背景</summary>

S2 benzyl alcohol dehydrogenase EC 1.1.1.90、S3 benzaldehyde dehydrogenase EC 1.2.1.28与enzyme_gold逐字一致，两个核心步骤获直接支持。S1给xylene monooxygenase EC 1.14.13.169，与gold的toluene methyl-monooxygenase EC 1.14.15.26同属甲基羟化化学，但该EC在E0无记录（GAP-070-008）；S4–S9的EC（1.14.12.10、null、1.13.11.1、5.5.1.7、3.1.1.45、1.3.1.10）均无E0条目，但酶名-反应类型总体相符（双加氧/内酯水解/还原酶），S5的EC以null诚实标注。属&#x27;有合理候选和部分支持、若干关键步骤仍缺具体核验&#x27;，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_070：本题gold主链LINEAR_UNIQUE、ordered_step_count=3；用于N=3目标反应评价，不把下游额外步骤计入D3a。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：列出必答三步accepted酶名/EC：S01 benzyl alcohol dehydrogenase 1.1.1.90；S02 benzaldehyde dehydrogenase 1.2.1.28；S03 toluene methyl-monooxygenase 1.14.15.26。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：给出三步主底物/主产物、方向与线性顺序，用于将答案S1–S3绑定到gold S03/S01/S02目标反应。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：官方EC条目accepted name=toluene methyl-monooxygenase，reaction含toluene→benzyl alcohol；仅支持该EC条目本身，不证明EC 1.14.13.169或xylene monooxygenase的催化范围。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分5 → V0.5新分7，变化+2。

新裁判理由：

> 必答步微生物均为Pseudomonas putida mt-2：物种与organism_gold三步行EXACT Pseudomonas putida(TaxID 303)一致；菌株mt-2有冻结BacDive 12880菌株记录(strain_designation=mt-2 PaW1, pWWO；保藏号DSM 3931/ATCC 33015/CCUG 2480)，身份定位有依据。但答案未填ncbi_taxid，且未提供反应级/菌株级催化证据(身份定位≠反应级能力≠全路径能力)；S4–S9归属Pseudomonas sp. B13超出必答终点，E0无B13记录，其性状与能力未核。无身份编造、无把单步写成全路径菌(PATHWAY_COMPLETE未声称)，主要微生物推荐未被推翻，不cap。7–8档取7：身份对应可靠，能力层与菌株级细节仍需确认。

<details><summary>V0.4理由与本行变化背景</summary>

P. putida mt-2身份有E0菌株记录支持（f3e0:bacdive:12880：species级NCBI taxid 303、strain_designation &#x27;mt-2 PaW1, pWWO&#x27;、保藏号含ATCC 33015/CCUG 2480），且与gold物种Pseudomonas putida一致，按同物种代表记录口径（四.4）不因所用实验菌株与gold代表株不同而判错。但S4–S9六步全部归Pseudomonas sp. B13，B13在E0无任何记录（GAP-070-084等NO_TRAIT_RECORD），其身份与整段氯代儿茶酚途径能力均未核；S1–S3的反应级能力亦无E0证据。无已核实身份错配（不cap），属&#x27;若干关键身份或作用范围仍未充分核验&#x27;，5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：参考三步宿主为Pseudomonas putida(EXACT, taxid 303)；不支持任意菌株的具体反应级能力
- E0_EVIDENCE / f3e0:bacdive:12880：mt-2 PaW1(pWWO)为真实P. putida菌株记录；不外推其对各步的催化活性，培养温度不代表最适
- E0_EVIDENCE / f3e0:taxid:303：物种级学名与状态；物种级记录不核菌株

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> ORG_001(P. putida mt-2)的定性性状与物种级代表记录大体相容：mesophilic偏好、Gram-negative、杆状、运动、非产孢、chemoheterotrophy等有species级观测/预测支持；温度/pH/盐度/基因组等关键定量子字段一律留null，未编造数值，诚实缺失不按错判。主要缺口：关键定量性状缺失；全部性状evidence_id/raw_text为null；ORG_002(Pseudomonas sp. B13)与ORG_001使用几乎同一套模板性状(含相同酶活与栖息地)，属跨菌株套用、无独立支持；F8降解谱与F9酶活写成菌株能力但无冻结证据。无离谱数值、无物种级观测冒充菌株定量。5–6档取6：部分性状准确适用，关键项证据不足且条件/适用范围未交代。

<details><summary>V0.4理由与本行变化背景</summary>

ORG_001（P. putida mt-2）可核项与trait_gold一致：F2 preference=mesophilic（gold OBSERVED）、F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming（taxid 303观测）；F1 &#x27;aerobic&#x27;与gold &#x27;aerotolerant=true&#x27;相容但不完全同义；F3/F4/F5/F14全null为诚实未知（完成度损失已计D1），无编造数值。薄弱项：F7仅&#x27;heterotrophic&#x27;过于笼统、F8 &#x27;degrades toluene, xylenes, and 3-chlorotoluene&#x27;与F9仅罗列途径酶（把途径酶当性状酶活）均无来源；ORG_002（B13）全部性状为属级通识默认值（杆状/Gram-negative/不产孢/好氧）却给F11/F12/F13 medium–high，无任何E0记录，属未经限定的属级外推。无已核实数值错误，落&#x27;部分性状准确且适用、关键项证据不足&#x27;5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：物种级代表记录支持aerotolerant、mesophilic偏好、运动、杆状、Gram-negative、非产孢等；不支持mt-2菌株级定量，也不支持B13
- GOLD_SLICE / trait_scoreability_mask.tsv：F2 min/max及F4 max待教师裁决、F3为completeness_only；不能把未裁决端点当已核数值
- ANSWER_TEXT / organism_profiles&#91;0-1&#93;.traits：答案确实以null承载多数定量未知，同时给出未带证据的降解谱与酶活描述

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 全部关键结论(路径步骤、酶、菌、性状)只指向单条EVID_001：source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，claim_scope仅泛列pathway/steps/enzymes/microorganisms。按P34，INTERNAL_KNOWLEDGE_ONLY属MISSING_SOURCE；无条目级可定位可核对来源，也没有被核实为不存在或不支持的引用，故不构成VERIFIED_MIS_CITATION、不cap。D5落在1–2档；档内取2：答案至少保持claim→evidence_id的自洽映射并如实标注内部知识，但没有任何可定位记录。

<details><summary>V0.4理由与本行变化背景</summary>

来源登记仅EVID_001一条：source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null，claim_scope覆盖pathway/steps/enzymes/microorganisms；两profile性状evidence_id全为null。按四.3，仅INTERNAL_KNOWLEDGE_ONLY自我声明→各claim group均为MISSING_SOURCE，决策相关组（CG01/CG02/CG03/CG05/CG07）无一可定位到条目级记录，属&#x27;几乎无法定位重要结论依据&#x27;的1–2档。该情形是缺失而非误导，默认不触发关键错误；无已核实错引，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry&#91;0&#93;：唯一来源为内部知识、无数据库/记录/locator；不支持任何结论可追溯

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案系统使用了confidence标签(low/medium/unknown)，对全部酶与菌归属统一标low，并在uncertainties中明说“EC号和菌株归属基于内部知识，未引用具体数据库记录，置信度低”“部分中间产物SMILES未提供”；未知性状以null+unknown呈现，未把预测冒充实测观测。限制：F8/F9等菌株能力描述与下游延续仍以较肯定措辞出现，S4–S9超出必答终点且其未核性质未在uncertainties中点明；“polar flagella”等具体形态为中置信但无来源。无系统性误导、无掩盖已知矛盾，不cap。7–8档取7：主要限制已披露，个别结论强度略超依据。

<details><summary>V0.4理由与本行变化背景</summary>

正面：全链step confidence统一low，S1 uncertainty注明依据（TOL质粒xylene monooxygenase推测），S5&#x27;EC号未知&#x27;、S7/S8&#x27;SMILES未提供&#x27;逐项披露；uncertainties明示&#x27;酶EC号和菌株归属基于内部知识，未引用具体数据库记录，置信度低&#x27;与&#x27;部分中间产物SMILES未提供&#x27;，与内部知识型证据强度基本相称。扣分：证据性质仅以confidence表达，未系统区分观测/预测/推断；性状侧F11/F12/F13对两个profile（含零证据的B13）给high且无来源说明，F6/F7/F10给medium，属局部/单点过度确信；未披露与gold终点（3-氯苯甲酸）之间的范围关系。非系统性误导、无掩盖矛盾证据，按P119档内扣，5–6档取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：答案确实声明内部知识、低置信与SMILES缺失
- ANSWER_TEXT / confidence fields：不确定性标签实际存在并区分low/medium/unknown

</details>

## Kimi

答案SHA256：`444fa0351091a939351c1ae617831527ca5231c8cbaf6818580556d8ede26977`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 题面指定路线名原样保留；3个必答主链步骤均给出底物/产物/SMILES、首选酶/EC、对应微生物；两个organism_profiles各含15项性状，未知项以null/unknown标注；额外S4–S9已声明为下游延伸，未冒充题面必经步，不构成缺步。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块完整：steps S1–S9逐步给出主底物/主产物英文名+SMILES、一个首选酶（含EC）与一个对应微生物；organism_profiles去重为ORG_001/ORG_002且各含全部15项性状；route_scope.chosen_route_name按题面原样回填；evidence_registry与uncertainties均交付。属&#x27;大部分必要内容完整，仅少量遗漏/工程缺陷&#x27;档（7–8），取8：扣分点为全部evidence.record_id为null、辅因子/电子载体未列入steps、部分性状留null（F3/F4/F14，而参考记录中存在可用值）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：支持题面指定路线名、必答主链、每步酶菌与15项性状要求；不证明答案内容科学正确。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S3&#93;：支持完整性登记：主链3步、两个profile与15项性状均已交付；不评价科学正确性。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_070：支持本题gold为LINEAR_UNIQUE、ordered_step_count=3；不把下游S4–S9纳入必答范围。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 前3个必答转化方向、结构与连接与gold一致：3-氯甲苯→3-氯苄醇→3-氯苯甲醛→3-氯苯甲酸（盐）；无反向/跳步；S1–S3未列O2/ferredoxin/NAD(P)+等辅因子，属局部计量表达缺陷，按P103留在7–8档；S4–S9为下游延伸，未用于抬高D2。

<details><summary>V0.4理由与本行变化背景</summary>

前3步S1–S3与gold逐步一致：3-氯甲苯→3-氯苄醇→3-氯苯甲醛→3-氯苯甲酸，方向、结构与SMILES均与gold反应行相符，构成可信主链。S4–S9为氯代儿茶酚修饰邻位裂解途径的合理下游延伸，并在route_scope.notes与uncertainties中明确声明&#x27;数据库命名路线可能仅到3-氯苯甲酸&#x27;，未冒充已确认。档内扣分依据：①各步普遍未列O2、NAD+/NADH、铁氧还蛋白等辅因子，字面计量不闭合（属局部计量缺陷，按P102–P103落入7–8档，不cap）；②S9产物3-氧代己二酸SMILES&#x27;O=C(O)CC(=O)CC(=O)O&#x27;较正确六碳结构少一个CH2，属局部结构缺陷，不改变主链结论。综合取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：支持gold三步反应方向与主底物/主产物；不自动证明辅因子计量完整。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：支持EC 1.14.15.26的甲基羟化反应方向；不证明答案全部辅因子与计量。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S3&#93;：支持答案给出的三步碳骨架转化与连续顺序；不证明未写出的辅因子。

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 3个必答目标反应均有对应酶/EC：S1对应gold S03 EC 1.14.15.26（xylene/toluene methyl-monooxygenase同EC），S2对应gold S01 EC 1.1.1.90且名含accepted name，S3对应gold S02 EC 1.2.1.28且名含accepted name；主要功能/EC对应可靠，但S1酶名非accepted exact、S02端点电荷表示待裁、三个gene_or_protein标注MINOR未核，且base range上限&#91;1,8&#93;，故取8而非9–10。

<details><summary>V0.4理由与本行变化背景</summary>

S2/S3的酶名与EC（benzyl alcohol dehydrogenase 1.1.1.90；benzaldehyde dehydrogenase 1.2.1.28）与gold enzyme_gold逐一吻合；S1 EC 1.14.15.26在E0为ACTIVE条目、accepted name=toluene methyl-monooxygenase且含xylM基因名，答案用同义词&#x27;xylene monooxygenase&#x27;并绑定xylM/xylA，名称变体未见于记录变体→该名称关联记UNRESOLVED，不判错。S4–S9六个EC（1.14.12.10、1.3.1.25、1.13.11.1、5.5.1.7、3.1.1.45、1.3.1.32）在冻结快照无记录（GAP-070-006/007/011/013/014/017/018/025/028/033/036/037/042/044），保持待核；答案已自陈S6 EC为家族级归属。核心步骤有可靠支持、下游待核，属7–8档，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：支持gold三步accepted酶名与EC；不证明任意具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：支持目标反应方向与底物/产物；不自动证明基因归属。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：支持EC 1.14.15.26的官方accepted name/reaction与xylM基因名；未列出xylene monooxygenase exact名称。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 必答三步对应微生物均为Pseudomonas putida mt-2；gold step organism为P. putida（TaxID 303），E0 BacDive 12880支持mt-2/pWW0菌株身份与保藏号；物种/菌株身份匹配。菌株对3-氯甲苯的逐反应能力仍主要来自TOL上链文献而非实验验证，且S4–S9的B13属题面终点外延伸，不用于抬高必答主链分。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3归Pseudomonas putida mt-2，与gold STEP级微生物（Pseudomonas putida, taxid 303）一致；E0 bacdive 12880为&#x27;Pseudomonas putida mt-2 PaW1, pWWO&#x27;菌株记录，支持其菌株身份与pWW0背景。S4–S9归Pseudomonas knackmussii B13，属氯代儿茶酚修饰邻位裂解途径的经典宿主，但冻结快照无B13任何记录（GAP-070-053…062），身份与能力均待核。答案未把单步菌写成整条路径菌：complete_pathway_organism_profile_id=null，route_summary明确&#x27;前3步P. putida mt-2，后6步B13&#x27;，身份定位/单步能力/整条路径能力三层未越级。取7（核心归属有支持，下游菌待核）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_070：支持gold三步organism为Pseudomonas putida、TaxID 303；不证明mt-2菌株的具体底物活性。
- E0_EVIDENCE / f3e0:bacdive:12880：支持mt-2 PaW1/pWWO菌株记录、ATCC 33015保藏号；不证明3-氯甲苯整细胞降解能力。
- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida物种级身份；不扩展到具体菌株能力。

</details>

### D4 性状科学性：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> P. putida mt-2主性状（运动性、杆状、革兰氏阴性、不产芽孢、ATCC 33015）与gold/E0一致；芳香烃降解与TOL酶活性有文献来源；F2把30°C培养记录写成optimum_c且pH/盐度/基因组留null，F1“严格好氧”较gold aerotolerant更强，属少量条件/数值问题，按7–8档取8。B13为终点外延伸，未用于抬高必答链分。

<details><summary>V0.4理由与本行变化背景</summary>

ORG_001多项与参考一致：F5 ATCC 33015与E0 bacdive 12880保藏号集合相符；F10运动性=true、F11杆状、F12革兰氏阴性、F13不产芽孢、F2 preference=mesophilic均与gold观测一致。问题：①F1&#x27;严格好氧&#x27;与gold观测oxygen_tolerance=aerotolerant不一致（同物种代表记录口径下按UNRESOLVED登记，不直接判错，但属条件/范围表述待修订）；②F2 optimum_c=30无观测来源（subfield mask标optimum为completeness_only），答案自标low/内部知识；③F3、F4、F14留null，而参考记录有pH(5–8)、盐度(%NaCl)、基因组条目，诚实null不重扣但影响适用性完整性；④ORG_002（B13）全部性状无冻结记录（GAP-070-053…062），全为UNRESOLVED。属&#x27;部分性状准确且适用，关键项证据不足&#x27;档（5–6），取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_070：支持P. putida温度、运动性、形态、革兰氏、产孢、保藏等性状参照；不自动支持所有菌株与所有培养条件。
- E0_EVIDENCE / f3e0:bacdive:12880：支持mt-2菌株ATCC 33015保藏号与26/30°C培养记录；培养温度不等于最适温度。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：支持答案性状填写位置与置信度；不证明未核数值正确。

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 核心路线给出MetaCyc/UM-BBD与Harayama等可定位文献，关键酶EC 1.14.15.26可由E0官方EC条目核对，P. putida身份有TaxID 303/BacDive 12880支持；但多数步骤EC无冻结记录、数据库条目record_id为null、多个性状仅EVID_006内部知识，故属部分关键结论可定位而其他模块缺映射/必要记录（5–6档），无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组状态：CG01路线序列仅以&#x27;MetaCyc pathway: 3-chlorotoluene degradation II&#x27;与&#x27;UM-BBD 3-Chlorotoluene Pathway Map&#x27;（均无record_id）支撑，属GENERIC；CG05酶-EC与CG07核心菌身份给到具体书目定位（Harayama 1989 J Bacteriol 171(9):5048-5055；Schmidt&amp;Knackmuss 1980 Biochem J 192(2):339-347；Stolz 2007 IJSEM 57:572-576），为条目级可定位但冻结快照未解析（GAP-070-047/048/049/051/052），记UNRESOLVED；性状类多家为INTERNAL_KNOWLEDGE_ONLY（EVID_006）属MISSING。正向可核项（EC 1.14.15.26条目、taxid 303、mt-2保藏号ATCC 33015）登记于事实层，不回填来源状态。无经核实错引，severity总体不适用；存在部分条目级可定位结论＋若干模块仅笼统/内部来源，属5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:1.14.15.26：支持EC 1.14.15.26的官方条目与反应；不证明其他EC或文献引文。
- E0_EVIDENCE / f3e0:bacdive:12880：支持mt-2菌株身份/保藏；不证明所有性状来源。
- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida物种身份；不证明未交付的TaxID或基因组登录号。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案有uncertainties、置信度与null未知字段，并说明路线边界；但大量P. putida性状以EVID_006 INTERNAL_KNOWLEDGE_ONLY标成medium/high，F2以培养温度写optimum_c，证据强度与披露不完全相称；属有说明但部分结论过强，非系统性伪装观测，不cap，取5–6档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体较好：区分DATABASE_DIRECT/ LITERATURE_DIRECT/ INTERNAL_KNOWLEDGE_ONLY三档来源，EVID_006明确标内部知识且置信low；route_scope.notes与uncertainties主动说明命名路线可能仅覆盖到3-氯苯甲酸、S4–S9为下游补全；TaxID、基因组与盐度/pH未知如实填null并声明；alternative_branches显式标is_part_of_scored_main_route=false。扣分点：S6–S9及ORG_002多项对未核实内容给&#x27;high&#x27;置信并零披露（局部过度确信，非系统性），F1&#x27;严格好氧&#x27;与参考记录的差异未提示风险；xylene monooxygenase/EC名称特异性未标待核。属&#x27;大部分证据性质标注正确、少量过度确信&#x27;档（7–8），取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持答案已披露部分未知、低置信与路线边界；不证明所有置信标签与证据强度相称。
- E0_EVIDENCE / f3e0:bacdive:12880：支持mt-2菌株记录与培养温度；不证明答案所有性状的medium/high置信。

</details>

## Qwen

答案SHA256：`220a19449e268c7c6c23d7654c928b16bee7f5802931482754fb587c5ce447b9`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 题面指定路线名原样填写；required三步主链、逐步酶/EC、微生物、15项性状字段均交付，11项填写、4项明确unknown，无明显漏步。额外S4把主链延伸到3-氯儿茶酚，超出gold终点3-氯苯甲酸，属下游延伸/范围小瑕疵，按P29不作为缺步扣分但不加分。D1给8。

<details><summary>V0.4理由与本行变化背景</summary>

全部必要模块实质交付：4步主链均含主底物/主产物(name+SMILES)、首选酶含EC、对应微生物；organism_profiles按物种+菌株去重为1条；15项性状全部出现（11项填写+4项诚实null）；route_scope.chosen_route_name原样为“3-chlorotoluene degradation II”且氧条件保持null；evidence_registry齐备。范围上S4较gold终点(3-氯苯甲酸)多延伸一步至3-氯儿茶酚，但属连续主链内的合理下游延伸、且另有范围声明，不构成重要范围偏离。7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION#BIOPATH150_070：题面任务、指定路线与15项性状要求；不证明答案科学正确性。
- ANSWER_TEXT / ANSWER#BIOPATH150_070：定位答案实际交付的步骤、性状、来源与null；不证明其内容为真。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_070：冻结gold显示ordered_step_count=3、LINEAR_UNIQUE；只用于必答步范围，不要求全部下游。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_070：冻结gold终点为3-Chlorobenzoate；支持D1范围边界。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> required主链S1-S3的有机转化、方向、顺序与终点均与gold一致：3-氯甲苯→3-氯苄醇→3-氯苯甲醛→3-氯苯甲酸。S1把gold的还原型铁氧还蛋白电子供体写成NADH，属局部辅因子/计量简化，按P103通常7-8档内处理，不cap。S4在题面终点之后继续到3-氯儿茶酚，超出D2评价边界，不作为目标信用或高分依据。D2给8。

<details><summary>V0.4理由与本行变化背景</summary>

S1 3-氯甲苯→3-氯苄醇（甲基单加氧）、S2 3-氯苄醇→3-氯苯甲醛（醇脱氢）、S3 3-氯苯甲醛→3-氯苯甲酸（醛脱氢）与gold主链逐步一致，方向正确、连接连续、主产物与SMILES无误，S3即达gold终点3-氯苯甲酸。S4 3-氯苯甲酸→3-氯儿茶酚（benzoate 1,2-dioxygenase，净脱羧生成CO2）化学上合理、原子计量C7→C6+CO2闭合，属题面/gold终点之外的合理下游延伸，按scope规则不计覆盖率扣分。局部问题：S1电子供体写作NADH，而该甲基单加氧酶(gold S03)用还原型铁氧还蛋白，属辅因子/电子供体局部计量缺陷。7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：冻结gold三步反应方向与主底物/主产物；支持S1-S3的化学连续性核对，不支持S4作为必答步。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：gold酶名与EC用于核对主链步骤；不证明具体蛋白实验活性。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：EC条目给出toluene methyl-monooxygenase反应及辅因子；不自动支持xylene monooxygenase名称或具体菌株能力。

</details>

### D3a 目标反应与酶对应：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> D3a目标集N=3。两个必答目标（gold S01/S02）为MATCH且答案给出与accepted一致的酶名/EC：benzyl alcohol dehydrogenase 1.1.1.90、benzaldehyde dehydrogenase 1.2.1.28，可计S=2。入口目标（gold S03）在反应层MATCH且答案EC 1.14.15.26与gold/accepted EC一致，但酶名&#x27;xylene monooxygenase&#x27;不在accepted name集，程序登记UNRESOLVED_NONACCEPTED/U，不判F。因此S=2,U=1，C=2/3≈0.67，候选带&#91;5,6&#93;；关键入口U阻止进入7–8，但已支持步逐反应清楚、待核边界明确，故取6。无已核关键失败，不触发D-KEY4。

<details><summary>V0.4理由与本行变化背景</summary>

S1 EC 1.14.15.26 与gold的toluene methyl-monooxygenase一致（EC正确、反应类型匹配）；S2 EC 1.1.1.90、S3 EC 1.2.1.28 与gold酶名/EC逐一吻合。S1酶名写作“xylene monooxygenase”，EC正确但该确切名称不在E0该EC条目的names列表中（名称特异性未核）。S4 EC 1.14.12.10 benzoate 1,2-dioxygenase 反应类型合理但不在gold/E0。S2/S3/S4的EC在E0均无条目(GAP)，酶-反应对应仅靠gold或合理性支持。主要步骤有可靠支持、少量条目待核，7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：Gold酶行：S01 benzyl alcohol dehydrogenase EC 1.1.1.90；S02 benzaldehyde dehydrogenase EC 1.2.1.28；S03 toluene methyl-monooxygenase EC 1.14.15.26。支持S2/S3的名称—EC配对；对S1仅支持EC值，不支持答案的&#x27;xylene monooxygenase&#x27;作为accepted name配对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：Gold有向反应：3-chlorotoluene→3-chlorobenzyl alcohol；3-chlorobenzyl alcohol→3-chlorobenzaldehyde；3-chlorobenzaldehyde→3-chlorobenzoate。支持三步净反应对齐；不自行解决酶名接受性。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：官方EC 1.14.15.26为ACTIVE，accepted names含toluene methyl-monooxygenase，reaction含toluene→benzyl alcohol；未列&#x27;xylene monooxygenase&#x27;为accepted name。故S1名称—EC配对保持UNRESOLVED，不判CONTRADICTED。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_070：确认本案gon主链为LINEAR_UNIQUE、ordered_step_count=3、路线名3-chlorotoluene degradation II。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案微生物为Pseudomonas putida mt-2，gold与E0支持P. putida物种及mt-2菌株身份（BacDive 12880记录mt-2 PaW1/pWWO并含ATCC 33015），身份定位可靠。各步均写同一菌株，gold step-level微生物为P. putida exact；但E0/BacDive记录主要支持身份与保藏号，不逐一证明mt-2对每步酶的 strain-level 催化能力，且extra S4不在必答范围。按身份可靠、能力细节尚需确认给7。

<details><summary>V0.4理由与本行变化背景</summary>

四步统一归属 Pseudomonas putida mt-2：物种与gold organism(Pseudomonas putida, TaxID 303)一致，菌株mt-2为真实菌株(E0 bacdive 12880=mt-2 PaW1/pWWO)，无身份编造、无跨类群错配。S1–S3步级归属与gold organism列一致；未填TaxID但物种名可核。S4(3-氯苯甲酸→3-氯儿茶酚)的菌株级催化归属无冻结记录，属未核实外推；整条路径能力未被显式声明为complete_pathway(该字段null)，未做序列存在性→整路径外推。主要微生物身份有可靠支持、S4步级能力待核，7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_070：gold各步微生物为Pseudomonas putida（TaxID 303）；支持物种级对应，不证明mt-2菌株逐酶能力。
- E0_EVIDENCE / f3e0:bacdive:12880：支持P. putida mt-2 PaW1/pWWO菌株身份与ATCC 33015保藏号；不自动证明每一步酶活或完整路径能力。
- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida TaxID 303物种身份；不证明具体菌株能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 可核实项：F5 ATCC 33015与E0 mt-2记录一致；F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming均与gold观测一致。F1写&#x27;aerobic&#x27;而gold为aerotolerant，非直接矛盾但未充分对应；F6 aerobic/oxygen合理但证据弱。F2/F3/F4/F14为明确null，按D1完成度处理，不当作编造。F7/F8/F9把toluene/xylene/chlorotoluene利用与降解/酶活写成medium confidence，但主要依赖pathway级EVID_001而非trait级证据，F7 gold面板也未列toluene/xylene为阳性碳源；属部分准确但关键项证据不足，给6。

<details><summary>V0.4理由与本行变化背景</summary>

可核实项正确：F5 ATCC 33015 经E0 bacdive 12880保藏号集合证实为mt-2菌株保藏号；F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming 均与gold观测一致；F6 aerobic/O2与gold无厌氧受体记录相容；F1“aerobic”与gold aerotolerant大致相容。F2温度/F3 pH/F4盐度/F14基因组填null为诚实未知（完成度扣分归D1，不重复重扣）；F7/F8/F9/F15为可合理支持但粗粒度陈述。性状证据多为INTERNAL_KNOWLEDGE_ONLY(EVID_002)，无离谱数值或物种级→菌株级误推广。主要性状可核且适用、少量条件/来源问题，7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_070：gold性状记录用于核对F1/F5/F6/F7/F8/F9/F10-F15；物种级代表记录不自动等同所有菌株，不证明未给来源。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_070：标明各trait是否observed/scoreable及待裁决子字段；支持D4按可核子项评价。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_070：标明F2 minimum/maximum、F4 maximum等待裁决；避免把范围端点强行当已冻结唯一真值。
- E0_EVIDENCE / f3e0:bacdive:12880：支持mt-2菌株身份与ATCC 33015；培养温度记录不等于最适温度，不自动支持全部性状。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 路线/酶主要引用EVID_001（MetaCyc pathway名，record_id=null，无逐步reaction记录），属pathway级或generic来源；性状多引用EVID_002（INTERNAL_KNOWLEDGE_ONLY）；F5 ATCC 33015有具体record_id且E0 BacDive可支持该保藏号，属可定位条目。但decision-relevant路线与酶-EC仍缺entry-level映射，不能给7-8。无VERIFIED_MIS_CITATION证据，不cap；按部分关键结论可定位、其他模块缺映射给5。

<details><summary>V0.4理由与本行变化背景</summary>

来源构成：EVID_001 MetaCyc“Pathway: 3-chlorotoluene degradation II”为路线级引用（路径名与gold pathway名一致、可定位到该路径，但record_id=null、属自由文本未解析成可查标识，GAP-070-050），覆盖路线/酶/微生物；EVID_003 ATCC 33015 为条目级且经核正确（支持F5）；EVID_002 INTERNAL_KNOWLEDGE_ONLY覆盖大量性状，属MISSING_SOURCE。未发现已核实错引（路径名匹配、ATCC号与mt-2一致），故无VERIFIED_MIS_CITATION，不cap。部分关键结论可定位可核对、其他模块缺条目级映射，落5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_070：定位实际交付的来源记录与claim_scope；不证明来源内容真实或充分。
- E0_EVIDENCE / f3e0:bacdive:12880：支持ATCC 33015与mt-2保藏记录存在；不等同于答案所引ATCC记录全文已核。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：gold酶/EC可核对S01/S02/S03；只作评价参考，不回填为答案来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案明确列出氧条件未指定、下游未纳入主链、S1酶名/EC归属可能差异、S4二氢二醇中间体、性状缺来源等不确定性；对unknown性状填null，confidence分high/medium/low/unknown，EVID_002标为INTERNAL_KNOWLEDGE_ONLY。主要限制与待核点已披露；个别广谱性状以medium confidence呈现但非系统性把预测写成实证，按7-8档给8。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量较好：EVID_002明确标为INTERNAL_KNOWLEDGE_ONLY、confidence=low；F2/F3/F4/F14以null如实表示无来源；uncertainties具体列出氧条件未定、下游范围边界、单加氧酶名称/EC归属差异、二氢二醇中间体、性状缺源等；对S4超出主链范围亦有声明。弱点：多项内部知识性状（F1/F6/F7/F8/F9/F11/F12/F13）标注medium置信，证据强度与置信略不相称，属单点/轻度过度确信，非系统性把预测写成实证。7档。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_070：定位不确定性说明、confidence标签与null披露；不证明未核事实为真。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_070：用于对照哪些性状为observed/predicted/缺失；不把gold回填为答案来源。

</details>

## Grok

答案SHA256：`02e1c74f9e5b22aa7b6c9f207c28ac597a6b44cef22a2e71a716a08f422f01a3`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案覆盖steps、酶、菌、15项性状、证据等模块，但将题面指定路线3-chlorotoluene degradation II解释为苯环双加氧并止于开环产物；gold该路线为甲基侧链氧化至3-氯苯甲酸。属于更换指定路线的任务参数偏离，D1关键错误成立，按&#91;1,4&#93;上限取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_070：gold终点为3-氯苯甲酸，支持题面指定路线终点判断；不评价替代路线内部化学。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：gold主链为3-氯甲苯→3-氯苯甲醇→3-氯苯甲醛→3-氯苯甲酸；不支持答案的苯环双加氧主链。

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 替代苯环双加氧路线三步化学上基本连贯：双加氧→二醇脱氢→间位开环，方向与主产物结构大体合理；但区域选择性/开环位点仅有推断，缺少实验或条目支持，且未覆盖gold侧链氧化主链。按D2自身化学质量给允许范围&#91;1,6&#93;上沿6，未给7+。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：gold主链为甲基侧链氧化，仅用于路线边界；不证明替代苯环双加氧路线化学必然错误。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三个gold必答步均无目标反应对应：S01需benzyl alcohol dehydrogenase EC 1.1.1.90，答案给dihydrodiol dehydrogenase EC 1.3.1.19；S02需benzaldehyde dehydrogenase EC 1.2.1.28，答案给catechol 2,3-dioxygenase EC 1.13.11.2；S03需toluene methyl-monooxygenase EC 1.14.15.26，答案给toluene dioxygenase EC 1.14.12.11。替代路线内部酶自洽不获目标信用，按S=0的&#91;1,2&#93;取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：gold目标酶为benzyl alcohol dehydrogenase、benzaldehyde dehydrogenase、toluene methyl-monooxygenase；不支持答案的三种替代路线酶作为目标步。
- E0_EVIDENCE / f3e0:ec:1.14.15.26：官方EC条目支持toluene methyl-monooxygenase为甲基羟化酶；不支撑答案的toluene dioxygenase环双加氧声称。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给P. putida F1（taxid 351746）作为各步菌；种名P. putida与gold物种级P. putida 303一致，但F1菌株、taxid 351746及CP000712.1在E0无记录，菌株级身份和单步能力仅内部知识；答案未声称完整路径能力（complete_pathway=null），避免了整路外推。按部分支持/关键身份待核给6。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida物种级身份；不核实F1菌株、taxid 351746或CP000712.1。
- E0_EVIDENCE / f3e0:bacdive:12880：支持同物种mt-2菌株记录；不等于F1菌株身份，也不证明答案整条路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_070：gold仅给出物种级P. putida taxid 303；不声称具体菌株F1。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已给性状中，中温偏好、运动、杆状、革兰氏阴性、不产芽孢等与gold物种级P. putida代表记录一致；但专性好氧与gold的aerotolerant记录存在表述差异，F7/F8/F9/F14的F1菌株特异性或具体基因组/酶活缺乏E0核对，pH/盐度/保藏/栖息地等多项为null。按部分性状可核实、关键项证据不足给6；缺失完成度主要归D1，不重复重扣。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_070：支持P. putida物种级代表的中温偏好、运动、杆状、革兰氏阴性、不产芽孢等；不核实F1菌株特异性或所有F7/F8/F9具体声称。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_070：说明F3/F15仅completeness、F2若干子字段待裁定；支持不按缺失子字段机械重扣D4。
- E0_EVIDENCE / f3e0:bacdive:12880：支持同物种mt-2记录；不核实F1菌株，也不支持跨株外推。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案只交付EVID_001/EVID_002两个INTERNAL_KNOWLEDGE_ONLY条目，无数据库、record_id、locator或DOI；所有路线/酶/菌/性状/基因组声称均无法沿外部来源核查。按D5六状态登记为MISSING_SOURCE，低分档取1；这是来源缺失而非已核实错引，不触发cap。

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确区分未知/null、内部知识、推断和未核实点：route_scope notes说明路线编号歧义，uncertainties列出区域选择性、开环位点、F1矿化能力及缺失性状；complete_pathway置null，未把预测冒充观测。少数性状给high但仅内部证据，属局部置信偏高；整体披露质量好，给7-8档上沿8。

## GPT5.6

答案SHA256：`980f7580f6948d4dcc7d11106c3f4136475449bbba3324f8786e55752ee84e6f`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求每步给出酶+EC、对应微生物及15项性状；答案仅交付3步主链骨架和路线名，三步enzyme/microorganism均为null，organism_profiles为空，酶、微生物、性状三个核心必需模块整体缺失。D1只评完整性/任务符合度；路径骨架本身可辨认，故在3–4档取低值3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：确认本题3个必答步各需一个首选酶/EC对应；不证明答案已交付这些酶信息。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_070：确认每步对应微生物参考；不证明答案已交付对应微生物。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_070：确认本题15项性状参考范围；不证明答案已交付性状。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 三步方向与主链化学与gold一致：3-chlorotoluene→3-chlorobenzyl alcohol→3-chlorobenzaldehyde→3-chlorobenzoic acid；无方向反转或原子明显不守恒。辅因子、氧、NAD(P)及feredoxin未列，属局部计量/简化缺陷（P103），不cap；终点以3-chlorobenzoic acid表示，与gold 3-chlorobenzoate仅有质子化/电荷表示差异（route diagnosis标注CHARGE_NOTATION_ONLY），作为局部表示问题，不改变主链化学结论。故7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：确认本题主链三步的主要底物/产物与方向；不证明答案已给出酶或微生物。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_070：确认本题路线起止与终点为3-Chlorobenzoate；不自动消除质子化/电荷表示差异。

</details>

### D3a 目标反应与酶对应：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 整个酶模块未交付：三步enzyme均为null，无酶名、EC或可辨认功能；按C04/RELEASE d3a_decision，D3a=MISSING、score=1，missing_basis必需。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_070：确认三个必答步的参考首选酶/EC；不证明答案已填写相应酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_070：确认三个必答目标反应；不证明答案已给出酶对应。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 整个微生物模块未交付：三步microorganism均为null，organism_profiles为空；按要求，模块完全缺失时D3b按MISSING=1，不宣称检测到科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_070：确认每步对应微生物参考；不证明答案已交付微生物信息。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状均未交付：organism_profiles为空；按P44，全部必需性状为空/无对象时D4=MISSING=1，不宣称科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_070：确认本题15项性状参考与可评分范围；不证明答案已交付性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_070：确认各性状可评分/完整性角色；不证明答案已填写。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5来源：evidence_registry只有EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，仅低置信；路线核心结论无可定位文献/数据库/计算记录。按P34/MISSING_SOURCE低分档，且几乎无法定位重要结论依据，取1。未核实引用不判虚构。

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案将路线明确标为推定，route_summary/每步uncertainty说明缺直接反应记录，酶/菌/EC/性状未知均填null，evidence confidence=low，uncertainties列明无直接文献、酶菌未确定、氧条件未指定；未把预测写成实证，也未掩盖主要限制。D6 9–10档，取9。
