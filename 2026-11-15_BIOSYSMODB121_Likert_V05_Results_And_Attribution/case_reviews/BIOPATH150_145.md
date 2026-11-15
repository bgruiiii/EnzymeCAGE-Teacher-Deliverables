# BIOPATH150_145：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：sulfoquinovose degradation V

污染物：6-sulfo-alpha-D-quinovose；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 43 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 34 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 45.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 30 | COMPARABLE | NATIVE_BATCH_A |
| Grok | — | UNSCORED | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 24 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`7deb75371beaabb1f96b504afe580fa342269973140c2ee97db2fe16e8c2dcda`。

### D1 完整性与任务符合度：2 / SCORED

V0.4旧分4 → V0.5新分2，变化-2。

新裁判理由：

> Task required route V main chain, but the answer explicitly substitutes E. coli K-12 sulfoglycolysis and ends at 2,3-dihydroxypropane-1-sulfonate instead of route V terminal isethionate. This is severe task deviation with major required steps absent, so D1 is capped and scored at the low end (2).

<details><summary>V0.4理由与本行变化背景</summary>

档位3–4：核心任务模块（4步路径、每步酶/EC/菌、15项性状、证据、不确定性）均有实质交付且格式完整，但路线执行严重偏离——题面规定chosen_route_name须原样填写&#x27;sulfoquinovose degradation V&#x27;且不得改选其他路线，答案在route_scope.notes与uncertainties中明示无法核实该名称与数据库变体I–V的对应关系，随后改按E. coli K-12硫醌糖酵解主链（YihS/YihV/YihT/YihU，终点DHPS）作答；该化学路线与冻结gold路线V的步骤酶（mutarotase 5.3.1.43、transketolase 2.2.1.15、4-deoxy-4-sulfo-D-erythrose isomerase 5.3.1.37、sulfoacetaldehyde reductase 1.1.1.433、isethionate exporter）及终点2-Hydroxyethanesulfonate均不同。按量表P100/D1边界条款，任务参数偏离（更换指定路线、交付不同路线）归D1关键错误，cap≤4；其余模块完整且诚实披露，档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：Shows route V required steps and terminal isethionate; does not support answer&#x27;s E. coli sulfoglycolysis to 2,3-dihydroxypropane-1-sulfonate as route V.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_145：Route V terminal compound is 2-Hydroxyethanesulfonate; answer gives a different terminal.
- ANSWER_TEXT / ANSWER.route_scope.notes：Answer itself says the route-name mapping to database variants is unverified and that it uses a literature E. coli K-12 pathway.

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> The supplied E. coli sulfoglycolysis steps are locally plausible and partly supported at EC-function level (especially sulfofructose kinase and sulfoquinovose isomerase), but the answer does not follow the specified route V main-chain direction and terminal, and several required target transformations/connections are absent. Under the allowed &#91;1,4&#93; D2 range, this is weak-partial rather than a verified chemistry contradiction.

<details><summary>V0.4理由与本行变化背景</summary>

就答案实际交付的E. coli K-12主链评价化学质量：SQ→6-sulfo-D-fructose（醛糖-酮糖异构化）→6-sulfo-D-fructose-1-phosphate（ATP依赖C1磷酸化）→DHAP+sulfolactaldehyde（C3–C4醛醇裂解）→2,3-dihydroxypropane-1-sulfonate（NADH依赖醛还原），方向正确、步骤连续、原子与辅因子（ATP/ADP、NADH/NAD+）在列，DHAP明确进入中心代谢，未见不守恒、方向反转或一步跳到中心代谢物。局部问题：以非手性SMILES略去α→β变旋步骤（异构酶实际作用于β-sulfoquinovose）；关键转化的证据仅一篇不可在E0核验的文献，属证据有限，未达9–10。路线本身与题面指定V不同的问题按D1边界条款归D1，不在D2重复扣分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:2.7.1.184：Official EC entry supports ATP-dependent sulfofructose kinase reaction, but not the full E. coli route or target route V.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Official EC entry names sulfoquinovose isomerase and beta-sulfoquinovose reaction; it does not directly verify alpha-SQ substrate usage or complete route V.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：Shows the required route V chemistry (mutarotase, transketolase, erythrose isomerase, sulfonatoacetaldehyde reduction, isethionate export) and terminal, which the answer does not follow.

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> The seven required route-V target reactions are not delivered; the frozen matrix records G0_NONE and ROUTE_BLOCKED_MISSING for each. The answer contains a valid enzyme module but on a different route, so the dimension is SCORED low rather than MISSING=1. Only sulfoquinovose isomerase is a partial local hit; no full target-step credit.

<details><summary>V0.4理由与本行变化背景</summary>

四步酶名称与所催化反应类型相符：sulfoquinovose isomerase（yihS）与E0 EC 5.3.1.31的accepted name、gene name、reaction一致；6-sulfofructose kinase与E0 EC 2.7.1.184（sulfofructose kinase、yihV、ATP+6-deoxy-6-sulfo-D-fructose=ADP+1-phosphate）一致；醛缩酶（yihT, 4.1.2.-）与还原酶（yihU, 1.1.1.-）在E0无条目、仅低置信度记忆并统由同一文献承载，EC全部给通配号需补具体编号。主要步骤酶对应有可靠支持、少量条目待确认→7档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：Lists the seven required route-V reactions and connects them to the specified main chain; answer steps do not match these target reactions.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Supports a sulfoquinovose isomerase EC entry, but not target-step completion for route V as a whole.
- ANSWER_TEXT / ANSWER.steps：Answer supplies four alternative-route enzyme steps; none are credited as completed route-V targets under the frozen matrix.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> E. coli K-12 identity is plausible and E. coli is supported at species level for the sulfoquinovose isomerase step, but gold&#x27;s full-pathway organism is Clostridium sp. MSTE9. The answer assigns E. coli K-12 to all steps and marks ORG_001 as complete-pathway organism; that whole-path capability is not verified in E0. This is partial support with a major full-path scope gap, not a verified contradiction.

<details><summary>V0.4理由与本行变化背景</summary>

物种Escherichia coli身份在gold中作为sulfoquinovose isomerase步骤菌出现（TaxID 562，物种级），答案给出K-12菌株与TaxID 83333；该菌株级编号在冻结E0无记录（GAP-145-027为待查询），不能核实、也不能判虚构或矛盾。四步均归属同一菌并按物种+菌株去重，符合题面去重要求；但“SQ为唯一碳源、完成整条YihS–YihU主链”的全路径能力仅由一篇不可核验文献承载，E0无TaxID/能力记录；gold本路径PATHWAY_COMPLETE为Clostridium sp. MSTE9（1105031），与答案不同，但因答案明示交付另一条已表征路径且文献不可核验，未判CONTRADICTED。有合理候选与部分支持、关键身份与作用范围尚未充分核验→6档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_145：Gold lists E. coli only for the S04 sulfoquinovose isomerase step and lists the full-pathway organism as Clostridium sp. MSTE9; it does not verify E. coli K-12 whole-path capability.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_145：Contains E. coli species-level traits, not K-12 strain-level whole-path capability evidence.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Supports an isomerase EC entry but not whole-cell pathway completion by E. coli K-12.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> All 15 traits are present for E. coli K-12. Core general traits such as facultative anaerobiosis, motility, rod morphology, Gram-negative envelope, non-sporulation, and salinity preference are supported by species-level gold records. Several K-12-specific numeric or source claims (temperature optimum/maximum, ATCC number, SQ sole-carbon growth, genome accession) are not verified in frozen gold or are pending/not scoreable, so D4 is partial rather than high.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状全部填写（filled=15, explicit_unknown=0, omitted=0），身份一致（均挂E. coli K-12）。可评分性状与gold物种级记录一致：F1兼性厌氧（aerotolerant/facultative anaerobe）、F10运动性、F11杆状、F12革兰氏阴性、F13不产芽孢均SUPPORTED；F4“非嗜盐菌”与gold salinity preference=non-halophilic一致；F9磺醌糖异构酶活性与E0 5.3.1.31一致。F2/F3的min/max与F4 min/max按trait_subfield_scoreability_mask属pending_teacher_adjudication/completeness_only，未作准确性扣分（F2 max 45°C、F3 min 4.5与gold观测区间有出入，登记待核）；F5 ATCC 10798与F14 NC_000913/4,641,652 bp/GC 50.8%在E0无记录→UNRESOLVED，且按同物种代表记录条款不因菌株与代表株不同判错。少量数值/来源待核，主要性状可核实且适用→7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_145：Supports several E. coli species-level traits; does not verify K-12-specific ATCC, genome, or SQ sole-carbon claims.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_145：Marks which E. coli trait fields have observed-accuracy roles; some temperature and pH subfields are completeness-only or pending.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_145：Shows E. coli temperature max/min and pH/salinity subfields are pending or completeness-only, so those numeric claims are not scored as outright wrong.

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> The pathway, enzyme, organism, and substrate claims rely mainly on EVID_001, a free-text literature citation without DOI/PMID/record_id; E0 marks that citation unresolved. Trait and genome claims rely on EVID_002, explicitly INTERNAL_KNOWLEDGE_ONLY. Some claims are mapped to a named paper, but no locatable record is delivered for verification, and many trait conclusions have no external record. No verified mis-citation or cap is established.

<details><summary>V0.4理由与本行变化背景</summary>

答案仅交付两条来源：EVID_001为特定文献（作者/题名/年份，database=PubMed，record_id=null），承载全部路径步骤与E. coli生长声称，E0将其列为未解析自由文本（GAP-145-019）→UNRESOLVED_SOURCE；EVID_002为INTERNAL_KNOWLEDGE_ONLY，承载15项性状与身份→MISSING_SOURCE。决策相关组（CG01/02/03/05/07/08/09/14）无一条目级可核验记录，也无已核实错引，故不cap；但CG05的两个酶-反应对应可由E0条目核对为SUPPORTED，且答案对每步作claim_scope式登记、如实标注record_id缺失，属“部分关键结论可定位可核对、其他模块仍缺映射”→5档；性状相关SUPPORTING组为内知来源，不跨档上调。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：EVID_001 is an incomplete literature citation; EVID_002 is internal knowledge only; neither gives a verifiable record-level locator for most claims.
- E0_EVIDENCE / f3e0:ec:5.3.1.31：Official EC fact exists, but does not verify the answer&#x27;s paper citation or broad source claims.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> The answer openly flags the route-name/variant uncertainty, broad ECs, low-confidence gene symbols, missing bibliographic details, and alternative branches. It mostly distinguishes confidence and uncertainty. Some K-12 trait values from internal knowledge are marked high/medium without raw_text, but this is not a systemic presentation of predictions as observations.

<details><summary>V0.4理由与本行变化背景</summary>

答案明确区分证据性质与确定度：EVID_002标为INTERNAL_KNOWLEDGE_ONLY、EVID_001标为LITERATURE_DIRECT并如实声明期刊/卷期页/PMID未确证、record_id留空；uncertainties逐条列出路线变体对应不明、四步EC未确证、yihT/yihU基因符号低置信、DHPS终产物为中等置信记忆、文献细节缺失，并在route_scope.notes主动披露可能与该编号所指变体不一致，未掩盖与gold的终点/全路径菌差异。扣分点：F1/F10/F11/F12/F13等以内知来源标high置信，个别置信强度略高于来源等级；但整体披露具体、非系统性误导、无明知掩盖→8档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Lists route variant, EC, gene, terminal product and bibliographic uncertainty explicitly.
- ANSWER_TEXT / ANSWER.evidence_registry：Discloses EVID_001 as literature-direct and EVID_002 as internal knowledge only; confidence labels vary.

</details>

## DeepSeek

答案SHA256：`dcfd495599d63eda75e3307a368303ac057efbc413efb3ce096e97d15da1b7dc`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> Chosen route name is echoed, but the answer delivers a five-step alternative (isomerase/kinase/aldolase/dehydrogenase/sulfolyase) and omits the specified mutarotation, transketolase, sulfoacetaldehyde reductase, and isethionate-exporter terminal chain. Major modules are present, but the core main chain and specified terminal are missing; this is a key task-conformity failure and caps D1 at ≤4. Within 3–4, score 3 because the required main chain is largely absent while some modules and all 15 trait fields are populated.

<details><summary>V0.4理由与本行变化背景</summary>

D1关键错误成立：任务参数偏离——自称合规却交付不同化学路线。答案route_scope.chosen_route_name原样写为&quot;sulfoquinovose degradation V&quot;（满足题面字段要求），但五步化学为 isomerase→kinase→aldolase→sulfolactaldehyde dehydrogenase→sulfolactate sulfolyase，止于pyruvate+sulfite；冻结route V为 mutarotase(S05)→sulfoquinovose isomerase(S04)→transketolase(S06/S02/S03)→sulfoacetaldehyde reductase(S01)→isethionate exporter(S07)，终端2-Hydroxyethanesulfonate。全文未声明替代路线或范围边界，反而以route V之名叙述该路线，属P100明列的D1关键错误。除路线/条件遵守外，路径、酶、菌、15项性状、来源登记、不确定性六类模块均已实质交付且内部引用自洽，故在cap档（≤4）内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：Shows the required seven-step directed gold main chain and terminal 2-Hydroxyethanesulfonate; does not by itself prove no alternative route can exist.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_145：Shows the required step enzymes, including sulfoquinovose mutarotase/isomerase, transketolase, sulfoacetaldehyde reductase, and isethionate exporter; answer replaces these with different steps.

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> Within the allowed D2 range &#91;1,4&#93;, the alternative organic steps are largely balanced and chemically plausible, but they are not the specified route: direct alpha-quinovose to fructose bypasses the required mutarotation, no transketolase/isethionate steps appear, the terminal is pyruvate/sulfite rather than 2-Hydroxyethanesulfonate, and cofactors such as ATP/NAD are omitted. This prevents a stronger band and places it at the upper end of the allowed range only because the local organic transformations are mostly plausible.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6偏上：答案交付的主链在化学上自洽且可辨认——醛糖-酮糖异构化→ATP依赖磷酸化→1-磷酸果糖醛缩酶裂解为DHAP与3-磺酸甘油醛→醛氧化为3-磺酸甘油酸→磺基裂解为丙酮酸与亚硫酸盐，各步连接、方向与碳骨架守恒均无断裂，未见&quot;首步即错/方向反转/一步跳中心代谢物&quot;等关键化学错误；其中S2的磷酸化反应与冻结EC 2.7.1.184官方反应（ATP + 6-deoxy-6-sulfo-D-fructose = ADP + 6-deoxy-6-sulfo-D-fructose 1-phosphate）逐字一致。扣分点：①S1直接用α-端基异构体作异构酶底物，省略了gold中的变旋步骤，而冻结5.3.1.31的反应底物为β-sulfoquinovose；②S2未列ATP/ADP、S4未列NAD(P)+等辅因子（局部计量缺陷，按P103在7–8档内处理，不cap）；③除S2外各步缺乏可核支持。路线与被指定路线不同一事按P100归D1判定，本维不因此连坐cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：Shows the required transketolase/isethionate route and terminal; the answer&#x27;s alternative transformations are not the target route.

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> All seven required gold target reactions are absent or unaligned. The answer&#x27;s enzymes belong to a different route; EC 5.3.1.30 is unverified and the target accepted EC 5.3.1.31 is not matched; the kinase/aldolase/dehydrogenase steps are not gold targets. No target step earns S; this is target-level all-M/omission with the enzyme module delivered on a wrong route. C=0 gives &#91;1,2&#93;; choose 1 because there is almost no usable target catalytic correspondence.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6取低：酶功能-反应类型总体匹配（异构酶/激酶/醛缩酶/脱氢酶/磺基裂解酶与该五步反应类型一致，无&quot;水解酶解释羟化&quot;式类别错配），但具体核验薄弱且存在名称-编号不咬合：①S1取&quot;sulfoquinovose isomerase&quot;配EC 5.3.1.30，而冻结EC 5.3.1.31恰为accepted name sulfoquinovose isomerase且反应为β-sulfoquinovose=6-deoxy-6-sulfo-D-fructose；5.3.1.30无冻结记录，按四.6/P66记UNRESOLVED，不cap但档内扣分；②S2写作&quot;sulfoquinovose kinase&quot;且EC=null，而与该反应对应的冻结条目accepted name为sulfofructose kinase(2.7.1.184)，名称偏差且未给编号；③S3、S4无EC、无基因/蛋白标识；④S5 EC 4.4.1.19无冻结记录→UNRESOLVED。合计：合理候选+部分支持，关键步骤仍缺具体核验，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.31：Official EC 5.3.1.31 is sulfoquinovose isomerase acting on beta-sulfoquinovose to 6-deoxy-6-sulfo-D-fructose; it does not verify the answer&#x27;s EC 5.3.1.30 or alpha-substrate step.
- E0_EVIDENCE / f3e0:ec:2.7.1.184：Supports a sulfofructose kinase reaction to fructose-1-phosphate, but this is not one of the seven gold target steps and is not assigned to P. putida by this record.

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> P. putida KT2440 is a real-looking identity, but the answer supplies no external evidence that it catalyzes the specified steps or completes the route. All steps and the complete-pathway claim are assigned to the same organism, while the gold step organisms and complete-pathway organism differ. This is a broad reaction-capability/identity-scope problem, not a proven TaxID fabrication, so 3–4 is appropriate; choose 3 because the complete-pathway claim is unsupported.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6取低：答案把全部5步统一归给 Pseudomonas putida KT2440（TaxID 160488），并设complete_pathway_organism_profile_id=ORG_001，等于声称单一菌株完成整条路线；而冻结route V的步级归属分布于 Clostridium sp. MSTE9（S02/S03/S04/S05/S06/S07）与 Bilophila wadsworthia（S01）等，P. putida KT2440不在其中。身份侧：TaxID 160488在E0无冻结记录（GAP-145-024，待联网卡），按四.6记UNRESOLVED，不判编造；能力侧：答案仅有INTERNAL_KNOWLEDGE_ONLY（EVID_002），既无反应级证据也无全路径能力证据，属&quot;身份定位≠反应级能力≠完整路径能力&quot;三层均未落实。因无已核实的身份错配或能力反证，不触发关键错误cap，但作用范围与全路径能力声称明显超出支持，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_145：Lists target-step organisms and the gold complete-pathway organism Clostridium sp. MSTE9; it does not list P. putida KT2440 and does not prove P. putida cannot perform an alternative route.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> All 15 traits are present with units/fields and plausible values, but key strain-specific values (temperature, pH, salinity, DSM 6125, genome NC_002947) have no frozen P. putida KT2440 trait record and no raw_text; trait_gold covers other organisms. Some values are plausible, but key items remain evidence-insufficient. This fits the 5–6 band; choose 5 because the key strain-specific evidence is absent.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6取低：15项性状全部填写且结构合规、内部无自相矛盾（中温、好氧、G−、杆状、有鞭毛、不产孢、非嗜盐；F2给4/30/37 °C并把preference标为&quot;中温菌&quot;，未把观测统计值冒充生物学耐受极限；F14给NC_002947/6,181,873 bp/61.5%），数值量级与P. putida的通行印象不冲突，无&quot;嗜冷菌最适80 °C&quot;式离谱值。但：①全部性状仅挂INTERNAL_KNOWLEDGE_ONLY（EVID_002/EVID_004），无条目级来源；②P. putida KT2440在本题冻结trait_gold/trait_scoreability_mask中完全无记录，全部子字段为EVIDENCE_GAP（GAP-145-032~050），准确性无法核实；③F5保藏号(DSM 6125)、F10–F14多项被标confidence=high，而其依据仅为内部知识，预测/记忆被包装成强证据；④F7/F8为笼统能力描述，未与目标污染物降解能力建立专属对应。按&quot;部分性状合理但关键项证据不足&quot;取5，未发现已核实的关键性状/身份/数值错误，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_145：Contains trait records for the gold organisms, not for P. putida KT2440; it does not support the answer&#x27;s P. putida trait values and does not contradict them.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> All answer evidence entries are INTERNAL_KNOWLEDGE_ONLY with no database, record_id, or locator. Important route, enzyme, organism, and trait conclusions therefore cannot be externally traced. No verified mis-citation exists, so this is MISSING_SOURCE low band without a cap. Score 2 rather than 1 because local evidence IDs and claim scopes are at least mapped to answer claims.

<details><summary>V0.4理由与本行变化背景</summary>

低分档（1–2偏高）：evidence_registry四条全部为 source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 均为null，claim_scope只有自述短语；按P34这属MISSING_SOURCE（&quot;完全无引用，或仅有INTERNAL_KNOWLEDGE_ONLY类自我声明&quot;），对D5所涉全部决策相关组（CG01/CG02/CG03/CG05/CG07）与支持组均为&quot;全部缺失→低分档&quot;。答案唯一可称道处是逐模块（步骤/性状/基因组）登记了证据指针并标了置信度，使&quot;哪条结论无来源&quot;可辨认，故不取1而取2。无已核实错引（E0无引用对象可核），按P34/R1口径MISSING_SOURCE默认不触发关键错误cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer discloses some missing ECs and a possible collection-number issue and labels evidence as internal knowledge, but still gives high confidence to unverified EC 5.3.1.30, organism/pathway capability, and genome/traits, and does not note the route/terminal divergence. Uncertainty disclosure exists but is incomplete; this fits 5–6, choose 5 because key limitations are not disclosed.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6取低：正面——出现独立uncertainties字段，具体列出3个未定EC（S2/S3/S4）与保藏号可能多值，属真实披露；每步与每项性状均带confidence字段，未出现&quot;作为AI/已获专家批准&quot;等自述。不足——①S1把未核实的EC 5.3.1.30标为confidence=high，全菌身份与F5/F10–F14多项亦标high，而其依据统一为INTERNAL_KNOWLEDGE_ONLY，置信度与证据强度明显不相称；②未披露&quot;全部四条证据均无外部可定位来源&quot;这一整体限制；③未披露所交付主链并非题面指定route V的化学，使读者会把该路线误读为路线本身；④未说明F2温度区间是观测统计而非生物学耐受极限（仅靠preference措辞间接表达）。属单点/多处过度确信而非系统性把预测写成实证，按D6严重度条款档内扣分、不cap，取5。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`ed7d983dd7e8d5e5a134acc6c07250abd81e026c842aef53d6f6e6d8699c861c`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> D1档3–4：答案只交付三步 sulfo-TAL 替代链，未覆盖题面指定七步主链及末端 2-hydroxyethanesulfonate；核心任务模块大部缺失并偏离指定路线，故取3。

<details><summary>V0.4理由与本行变化背景</summary>

D1评价任务模块完成度、路线/条件遵守与交付完整性。答案JSON完整，路径、酶、菌、15项性状、来源与不确定性均已交付；但题面明确限定route_scope.chosen_route_name=sulfoquinovose degradation V且不得改选其他路线，答案虽回填该名称，实际主链S1–S3为转醛醇酶型三步并止于DHPS，与冻结gold路线BSY-p00984的7步转酮醇酶型主链及终点isethionate不同，属自称合规却交付不同路线，按八.D1/D2边界构成D1关键错误，cap≤4；因其余模块交付完整，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_145：Gold根/终点：6-sulfo-alpha-D-quinovose→2-Hydroxyethanesulfonate；不支持答案以DHPS为终点。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_145：Gold为7个有序必答步、LINEAR_UNIQUE；不用于要求所有旁支。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：Gold步骤顺序与反应；答案三步与目标主链不一一对应。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> D2档3–4：答案的sulfo-TAL三步化学自身基本连贯（异构化、转醛醇裂解、NADH还原），但未覆盖指定主链的关键转化与末端isethionate，连接性不足以构成题面主链；在允许&#91;1,4&#93;内取4。

<details><summary>V0.4理由与本行变化背景</summary>

D2评价反应化学本身。答案三步转醛醇酶路径在文献层面可成立（异构化、转醛醇裂解、醛还原），方向与主产物连接基本合理；但S1直接用EC 5.3.1.31作用于α-底物而缺mutarotase，S2/S3无EC，且相对题面指定路线V缺少后续转酮醇/异构化/还原至isethionate的步骤。因答案已在uncertainties中声明路线名对应不确定，且引用了文献来源（未核），按四.5合理替代路线四步判断不判D2关键错误；作为部分成立、关键中间体与连接仍需修订，取5–6档中的6分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：Gold目标反应与产物；答案替代反应不同，不能回填目标主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_145：Gold终点为isethionate；答案终止于DHPS。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> D3a档1–2：七目标步均未建立目标酶-反应对应；仅S1使用EC 5.3.1.31，但底物为alpha-SQ而官方反应为beta-SQ；S2转醛醇酶与目标transketolase不同，S3还原至DHPS非目标sulfoacetaldehyde reductase；其余目标缺失。少量局部信息不改变核心目标失效，取2。

<details><summary>V0.4理由与本行变化背景</summary>

D3a评价酶功能、名称、EC与反应对应。S1的EC 5.3.1.31在E0中核验为sulfoquinovose isomerase，名称与EC匹配；但官方反应以β-sulfoquinovose为底物，答案以α-底物直接转化且缺mutarotase，步骤催化未核（F3R1CLM-002700 UNRESOLVED）。S2转醛醇酶、S3磺基乳醛还原酶均无EC，仅低置信基因/名称，关键步骤缺具体核验。整体有合理候选和部分支持，但若干关键酶-反应对应未充分核验，取5–6档中的5分；无已核实酶功能关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.31：官方EC 5.3.1.31名称/基因为sulfoquinovose isomerase/yihS，反应使用beta-sulfoquinovose；不支持答案alpha底物S1或步骤催化。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_145：各目标步accepted酶名/EC；答案转醛醇酶与DHPS还原酶不在目标accepted集合。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：目标反应/产物；答案S2/S3产物与目标transketolase/sulfoacetaldehyde reductase不同。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> D3b档5–6：Bacillus cereus ATCC 14579为合理候选且答案给出文献/数据库引用，但E0无该TaxID/genome/性状记录，且以同一菌承载整条替代路径的整路能力声称未在冻结证据中核实；未发现已核实身份错误，取6。

<details><summary>V0.4理由与本行变化背景</summary>

D3b评价微生物身份、单步催化与整条路径能力。答案统一推荐Bacillus cereus ATCC 14579（TaxID 226900）并标complete_pathway_organism_profile_id=ORG_001，声称其经转醛醇酶途径降解sulfoquinovose。E0无TaxID 226900冻结记录（GAP-145-001），BacDive条目无record_id，身份、反应级能力与完整路径能力均未核；答案将同一菌用于全部步骤，存在由单步/文献候选外推到整条路径的风险。因身份未核，不判编造或错配，也不cap；按合理候选但关键身份与作用范围未充分核验，取5–6档中的5分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_145：Gold目标步对应Bilophila wadsworthia、Clostridium sp. MSTE9、Alkalicoccus urumqiensis、Escherichia coli、Bacillus aryabhattai；不直接核实B. cereus。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_145：Gold性状记录针对目标路线菌；无B. cereus ATCC 14579记录。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> D4档5–6：15项均返回，未知pH/盐度如实null，形态/革兰/芽孢/运动性等与B. cereus常见描述相容；但关键性状（温度、碳源、降解、酶活、基因组）在E0无B. cereus记录，F2把培养温度30°C写入optimum_c需修订，F7/F8/F9依赖未核文献，取5。

<details><summary>V0.4理由与本行变化背景</summary>

D4评价性状对应菌株、数值/单位/条件与解释。答案对B. cereus ATCC 14579给出15项性状：13项填写、2项（pH、盐度）明确null，无遗漏。温度30°C、兼性厌氧、革兰阳性、杆状、产芽孢、运动性、基因组5,411,809 bp/35.3% GC等与常见B. cereus描述方向一致；但E0无该菌株性状记录（GAP-145-051~063），关键数值、保藏号与基因组登录号均未核，且F2仅填培养温度30°C而非耐受范围，答案已作说明。按部分性状合理但关键项证据不足，取5–6档中的6分；未发现数值离谱或预测冒充观测的已核实关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_145：Gold性状记录针对目标路线菌；无B. cereus ATCC 14579性状记录。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_145：Gold可评分性状掩码针对目标菌；不核实答案B. cereus性状。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D5档5–6：答案交付了具体DOI、EC、BacDive/NCBI条目标识，部分可定位（EC 5.3.1.31名称/基因与E0一致）；但路线、末端、菌株身份、性状和基因组等核心组在E0无冻结记录，均为UNRESOLVED_SOURCE；未发现已核实错引，取5。

<details><summary>V0.4理由与本行变化背景</summary>

D5按claim group登记来源状态。答案有6条evidence_registry：EVID_006（EC 5.3.1.31）为可定位条目，E0核验accepted name匹配，支持酶名称/EC，但不支持α-底物步骤或S2/S3；EVID_001 DOI、EVID_004 NC_004722.1、EVID_005 TaxID 226900均无冻结记录，登记UNRESOLVED_SOURCE；EVID_002 MetaCyc pathway无record_id、EVID_003 BacDive strain entry无record_id，登记GENERIC_SOURCE。决策相关组中仅CG05有部分条目级可核对证据，核心路线/起点/终点/微生物身份仍缺映射或未核；无已核实错引，不触发cap。按“部分关键结论可定位并核对，其他模块仍缺映射”取5–6档中的5分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.31：仅支持EC名称/基因与beta-sulfoquinovose官方反应；不支持答案全部步骤催化或B. cereus整路能力。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> D6档7–8：答案明确列出路线名映射、EC/基因缺失、S3主链归属、立体化学及pH/盐度未知，confidence与证据类型基本相称；未发现系统性把预测写成实证，取8。

<details><summary>V0.4理由与本行变化背景</summary>

D6评价证据性质、不确定性与结论边界。答案uncertainties具体列出路线名对应不确定、S2/S3 EC与基因未确证、第三步主链归属不确定、立体构型标注风险、pH/盐度无可靠来源；明确区分培养温度不等于耐受极限，并说明null为诚实未知。主要限制披露较具体。但部分未核身份/性状仍以DATABASE_DIRECT/high或medium包装（如F1/F5/F10–F13/F14），属单点过度确信而非系统性把预测写成实证；按单点过度确信档内扣，取7分，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Qwen

答案SHA256：`9aa133817675ea707fe07091cef27d575f6b5cf998e1f930201559ed8c68ef83`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> JSON完整可读，但题面锁定route V七步，答案只给4步且为另一条异构/激酶/醛缩酶/脱氢酶链，缺S05变旋酶、S02/S03转酮醇酶、S01还原酶和S07外排，终点为3-sulfo-L-lactate而非isethionate；15项性状全null。任务模块部分存在但主链严重偏离，D1关键错误成立，cap≤4，取3。

<details><summary>V0.4理由与本行变化背景</summary>

结构层面所有模块均有可辨认交付（4步含底物/产物/SMILES、酶+EC、对应菌、15项性状逐项null、2条证据、逐step uncertainty），但题面末段要求chosen_route_name原样填写且&#x27;不得改选其他路线&#x27;；答案回填了路线名，交付的化学主干却是异构→2.7.1.184激酶磷酸化→4.1.2.51醛缩酶裂解→未定EC脱氢的磺基糖酵解型路线，与冻结gold route V的七步主干（5.1.3.43变旋→5.3.1.31异构→2.2.1.15转酮醇酶→5.3.1.37→2.2.1.15→1.1.1.433还原→isethionate外排）不一致，且notes自称&#x27;按题面指定路线填写&#x27;，属自称合规却交付不同路线的任务参数偏离（P100，D1关键错误）；叠加15项性状全部null（诚实但完成度不足）。cap档内取3：字段齐全、逐step绑定清楚，但核心路线内容不是题面指定路线。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_145：pathway_name=sulfoquinovose degradation V，ordered_step_count=7，LINEAR_UNIQUE，quarantined=FALSE；支持本题为7步主链。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_145：root=6-sulfo-alpha-D-quinovose，terminal=2-Hydroxyethanesulfonate；支持终点边界。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：列出S05变旋酶、S02/S03转酮醇酶、S01还原酶、S07外排等步骤；不支持答案4步激酶/醛缩酶链作为route V主链。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> D2按所答化学评：S1-S4内部链大体连贯（异构、磷酸化、醛缩裂解、氧化），但目标route V第一步S05 α-&gt;β被跳过，S1直接用EC 5.3.1.31于α底物；核心S02/S03转酮醇酶被激酶/醛缩酶替代，终点为3-sulfo-L-lactate而非isethionate。任务路线不可改选，化学自洽不能回填目标主链。在&#91;1,4&#93;内取3。

<details><summary>V0.4理由与本行变化背景</summary>

按合理替代路线四步判断：①题面已指定具体路线（sulfoquinovose degradation V）；②答案未声明替代路线或范围边界；③替代路线无可核证据——唯一凭据EVID_001只有MetaCyc库名与路线名、record_id=null，该自由文本在E0中未解析成可查询条目（GAP-145-023），不能转入正常评分；④偏离使D2主要结论失效：route V依赖的两步转酮醇酶(EC 2.2.1.15)与磺基乙醛还原酶(EC 1.1.1.433)步骤整体缺失，主链终点由gold的2-Hydroxyethanesulfonate(isethionate)改为3-磺基-L-乳酸且零声明。故D2关键错误成立、cap≤4。档内取4：S1与gold S04同酶同转化（EC 5.3.1.31），EC 2.7.1.184确为真实的磺基果糖激酶，四步SMILES自洽可读；但主链不是题面指定路线，且S2/S4辅因子（ATP、电子受体）未列（P103属局部计量缺陷，仅档内考虑）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:5.3.1.31：官方酶条目为sulfoquinovose isomerase，反应为β-sulfoquinovose=6-deoxy-6-sulfo-D-fructose；不支持α直接底物或整条route V。
- E0_EVIDENCE / f3e0:ec:2.7.1.184：官方 sulfofructose kinase 反应为ATP+6-deoxy-6-sulfo-D-fructose=ADP+F1P；支持S2酶对，但该反应不是gold route V S02转酮醇酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：gold route V步骤S05/S04/S02/S03/S06/S01/S07；答案激酶/醛缩酶链不匹配目标序列。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_145：gold目标酶集含EC 5.1.3.43、5.3.1.31、2.2.1.15、5.3.1.37、1.1.1.433；不支持答案EC 2.7.1.184/4.1.2.51路线。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 按7个必答目标步核：答案4步为另一磺基糖酵解链（异构/激酶/醛缩酶/脱氢酶），与route V的S05 mutarotase、S02/S03 transketolase、S01 reductase、S07 exporter不对应；仅EC 5.3.1.31酶名/反应和EC 2.7.1.184本身可核，但未落实到目标步。全目标步未交付/被替代，模块非空，按C04失败锚点取2，不判整维MISSING。

<details><summary>V0.4理由与本行变化背景</summary>

逐step酶-反应对应：S1 EC 5.3.1.31的accepted name与答案&#x27;sulfoquinovose isomerase&#x27;精确一致（SUPPORTED），但官方reaction以β-sulfoquinovose为底物而答案以α端基起步，底物端未获支持（UNRESOLVED）；S2 EC 2.7.1.184官方reaction（ATP+6-deoxy-6-sulfo-D-fructose=ADP+6-deoxy-6-sulfo-D-fructose 1-phosphate）与该步转化一致（SUPPORTED），唯酶名&#x27;6-deoxy-6-sulfo-D-fructose kinase&#x27;为官方名的描述性改写（UNRESOLVED_SPECIFICITY）；S3 EC 4.1.2.51在冻结证据中无记录（GAP-145-007/014，UNRESOLVED）；S4 EC=null并如实声明，仅给脱氢酶名称。有合理候选与部分支持、若干关键步仍缺具体核验→5–6档取5；未见EC大类与反应类型相互矛盾的经核实错误，不判关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_145：目标步accepted酶集逐行列出；答案四步酶集与之不同。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：目标反应序列与答案四步不能逐行绑定。
- E0_EVIDENCE / f3e0:ec:5.3.1.31：支持EC名称与β底物反应；仅提供局部可核酶信息。
- E0_EVIDENCE / f3e0:ec:2.7.1.184：支持S2激酶名称/反应；该反应不是目标route V S02。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 四步均用Rhodopseudomonas palustris CGA009；gold route V各步对应Bilophila/Clostridium/Alkalicoccus/E. coli/Bacillus等不同菌。R. palustris身份本身可能，但E0无TaxID 258594记录，且EVID_002只支持身份不支持步级/全路能力；complete_pathway_organism_profile_id=ORG_001无证据。按3-4档取4，保留身份/能力UNRESOLVED。

<details><summary>V0.4理由与本行变化背景</summary>

答案以单一菌株Rhodopseudomonas palustris CGA009承担全部4步并声明complete_pathway_organism_profile_id=ORG_001，但其微生物证据只有EVID_002（NCBI Taxonomy，record_id=258594，claim_scope仅microorganism）；按D3b三层口径（身份定位≠反应级能力≠完整路径能力），身份层条目不能支持任何步级催化或整条路径能力，属证据类别错配。TaxID 258594在冻结证据中无记录（GAP-145-002/026/030），身份亦UNRESOLVED；该菌不在gold route V步骤菌名单内，但无冻结证据可核实其能力，故不登记跨属/异菌株cap，只记key_error=UNRESOLVED。档位：核心能力声称完全无适用依据、身份未核→3–4档，取4（菌名/株号数字可辨认、置信度已标low）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_145：列出route V各步目标菌（Bilophila、Clostridium、Alkalicoccus、E. coli、Bacillus），不含R. palustris；gold菌表非穷尽，仅用于显示目标步菌不同，不证明R. palustris无能力。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_145：性状行属于其他route V菌，不填充R. palustris的null性状。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 全15项性状均为null，属于明确未知但整模块无观测值；按量表P44/四.4 D4 MISSING=1，不宣称科学错误；完成度问题在D1已记录。

<details><summary>V0.4理由与本行变化背景</summary>

题目要求每个profile一次返回15项性状并给最强来源；答案organism_profiles&#91;0&#93;.traits的F1–F15全部为value:null、raw_text:null、evidence_id:null、confidence:unknown，并在uncertainties中说明&#x27;性状缺乏直接来源，均填null&#x27;。按rubric四.4/P44，全部必需性状均为null/空值时D4记MISSING=1，表示未提供可评价性状结果，不宣称检测到科学错误；完成度不足已在D1反映，两处不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> EVID_001仅为MetaCyc路线名、无record_id，却覆盖pathway/steps/enzymes/microorganism；EVID_002给TaxID 258594但E0无记录；核心步级来源无法定位，只有部分身份定位尝试。无已核错引，按3-4档取3。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CORE：CG01/CG02/CG03/CG05/CG07/CG09）全部只有一条无法定位的MetaCyc路线名（EVID_001，record_id=null，claim_scope含pathway/steps/enzymes/microorganism）或完全无来源（complete_pathway声明）。唯一带条目号的EVID_002（TaxID 258594）在冻结证据中无记录→UNRESOLVED_SOURCE。E0无任何经核实错引（LOCAL/CRITICAL/SYSTEMIC均为0），故不触发D5 cap；按P35决策相关组全部笼统落入3–4档，取3——答案连一条与所交付步骤对应的可定位条目都没有，替换后的路线名也无法用冻结证据解析（GAP-145-023）。SUPPORTING组（性状/形态/不确定性）全为MISSING_SOURCE，不得跨档上调。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案对酶/菌低置信、15性状全null、SMILES立体化学和辅因子未确认有披露，未把性状写成观测；但未披露其4步链与route V目标步/终点的重大冲突，EVID_001以DATABASE_DIRECT包装路线级来源。按5-6档取6，未达系统性误导。

<details><summary>V0.4理由与本行变化背景</summary>

正面：逐step给出uncertainty、酶/菌confidence为medium/low、EC未确认填null、SMILES声明为近似且立体化学未全指定、15项性状全null并说明缺来源、uncertainties逐条列限制——证据性质与边界披露具体诚实。负面：把与题面指定route V不同的路线直接写成&#x27;按题面指定路线sulfoquinovose degradation V填写&#x27;且零披露替代；complete_pathway_organism_profile_id=ORG_001未加任何限定；EVID_001以DATABASE_DIRECT标签包装无record_id的路线名。部分结论强度超过依据（5–6档），但披露整体具体、未见系统性把预测写成观测或掩盖已知矛盾→取6，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

评分请求中断，未获得正式评分；原正文可读，未知费用保留。

## GPT5.6

答案SHA256：`0062e45102f717cb3c1f19445c39c9acfaa224f233a1442c25a8ad1a309068c8`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定sulfoquinovose degradation V且要求7步主链；答案只给2步，且S1以aldolase裂解生成DHPS+pyruvate，与gold路线V的S05→S04→S02→S06→S03→S01→S07及终点isethionate不符。核心必答步绝大多数缺失，D1关键错误成立，按1–2档取2（有结构化片段但主任务不可用）。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_145：gold路线V名称、起点与终点；终点为2-Hydroxyethanesulfonate，不支持答案的DHPA终端。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：gold路线V的7步主链序列；答案两步不在该序列中，支持必答步缺失判断。

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1/S2两步内部方向大致可读（aldol裂解、脱磺酸），但均为替代路线，未覆盖gold路线V的核心转化（mutarotation/isomerase/transketolase等），且止于DHPA而非isethionate；无独立证据支持，连续性仅限两步。按D2较弱档3–4取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：gold路线V的关键转化与顺序；答案两步并非该主链转化，不能据此获得目标主链连续性信用。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_145：gold terminal isethionate；答案terminal DHPA不支持目标终点完成。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a只计目标反应。7个必答目标步在矩阵中均为ROUTE_BLOCKED_MISSING/MISSING；答案的S1/S2（aldolase/desulfonylase）不对应路线V任何目标步，且E0无4.1.2.57/4.4.1.31记录。替代路线内部自洽不获目标信用，故目标酶对应几乎无可用项，按C04失败锚点&#91;1,2&#93;取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_145：gold路线V目标酶集合；答案的sulfoquinovose aldolase/desulfonylase不在其中。
- E0_EVIDENCE / f3e0:ec:5.3.1.31：仅官方sulfoquinovose isomerase卡；不支持答案的aldolase/desulfonylase声称。

</details>

### D3b 微生物身份与能力：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案只给Rhodopseudomonas palustris CGA009一个profile，用于两个替代步骤，并设置complete_pathway_organism_profile_id=ORG_001；该菌不在gold路线V的目标菌列表中，且EVID_002仅为INTERNAL_KNOWLEDGE_ONLY，无反应级或全路径能力证据。步骤归属与全路径能力均未获支持；按D3b较弱档3–4取3，不判已核实身份错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_145：gold路线V目标菌列表；R. palustris CGA009不在其中，但absence不证明其无能力。
- ANSWER_TEXT / ANSWER#evidence_registry：答案对R. palustris的归属仅为INTERNAL_KNOWLEDGE_ONLY，无数据库/文献定位。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 任务要求每个profile 15项性状；答案ORG_001的15项均value=null/confidence=unknown，未交付任何可评价性状值。按P44/量表四.4，全部必需性状null按D4 MISSING=1，不宣称科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_145：性状可评分性掩码；答案未提供任何可用性状值，支持MISSING判断。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案三条evidence均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null；没有可定位文献/数据库/计算记录。按D5六状态为MISSING_SOURCE（默认不cap），决策相关组全部缺失，低分档取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#evidence_registry：三条证据均为INTERNAL_KNOWLEDGE_ONLY，无外部定位。
- E0_EVIDENCE / f3e0:ec:5.3.1.31：E0仅提供官方EC卡，不是答案实际交付的来源记录。

</details>

### D6 不确定性与诚实度：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案有部分不确定性说明（氧条件未指定、性状无来源、下游未展开），并标注证据为INTERNAL_KNOWLEDGE_ONLY；但route_summary把两步替代路线写成主链事实，complete_pathway_organism_profile_id=ORG_001无支持，酶/菌confidence=medium，未披露路线偏离与全路径能力限制。属部分披露但部分结论强度超过依据，按5–6档取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#uncertainties：答案披露了氧条件、性状来源和下游未展开，但未披露路线偏离及全路径能力限制。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_145：gold路线V与答案两步替代路线不同，用于核对答案是否披露该主要限制。

</details>
