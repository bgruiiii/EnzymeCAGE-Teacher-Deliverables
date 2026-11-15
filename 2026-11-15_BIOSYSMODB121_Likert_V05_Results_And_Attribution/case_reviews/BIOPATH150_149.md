# BIOPATH150_149：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：L-canavanine degradation II

污染物：L-canavanine(1+)；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 36 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 34 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 43 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 38 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 44 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 20 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`40b5f886e977d0e2f0bfc31b410e8d3e8d1d1973323a37a174cb0b53b2f50ea8`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> Covers all requested module categories and gives a coherent two-step route with one organism and 15 trait fields, but only 2 of the 6 required gold route steps are addressed and the gold terminal products are not reached. The answer reconstructs an alternative arginase/canaline route while retaining the required route name. D1 key error for core route-module omission is present, so capped at 4; within the 3-4 band choose 4 because the delivered subset is clear and well structured.

<details><summary>V0.4理由与本行变化背景</summary>

D1任务符合度：输出模块齐全（2步主链、每步酶与菌、15项性状、来源与不确定性均有交付），但route_scope.chosen_route_name虽原样填『L-canavanine degradation II』，实际steps交付的是canaline途径——S1用arginase(EC 3.5.3.1)水解L-canavanine生成L-canaline+urea，S2将canaline转氨为L-homoserine；而gold该路线首化学步为canavanine-gamma-lyase(EC 4.4.1.43)直接裂解L-canavanine生成L-homoserine+hydroxyguanidinium（gold S04）。这属『自称合规却交付不同化学路线』的任务参数偏离（P100），D1关键错误成立，cap≤4；档内取4分（模块覆盖与格式完整，但核心路线偏离）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_149：Shows the gold case has six ordered steps and terminal products Fumarate|Hydroxyguanidinium; used with task scope, not as an invitation to require all unselected branches.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：Lists target step enzymes S01-S06; does not by itself prove any organism capability.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_149：Defines the route endpoints for the specified pathway.

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> The answer&#x27;s two-step chemistry is internally partially plausible for a canaline route, but it is not the specified target chemistry: it replaces the target canavanine-gamma-lyase conversion with arginase hydrolysis and an unconfirmed canaline aminotransferase step. The second step&#x27;s oxime mechanism and enzyme identity are speculative, and the path does not reach the specified terminal products. Under the base D2 range &#91;1,4&#93;, choose 3: some localized chemistry is readable, but multiple key transformations remain unsupported and off-target.

<details><summary>V0.4理由与本行变化背景</summary>

D2路径化学：两步主干化学自洽且元素守恒（S1 L-canavanine + H2O → L-canaline + urea；S2 L-canaline + pyruvate → L-homoserine + 2-hydroxyiminopropanoate），均为文献中真实存在的canaline支路反应，SMILES与计量基本对应。但这是与gold不同的替代路线，且全部为INTERNAL_KNOWLEDGE_ONLY、无可核证据，S2机制与副产物不确定。按合理替代路线四步判断：已声明重建（第2步）、无可核证据（第3步按未证实登记，不自动判错也不给高分）。主干成立但合理性证据有限，5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：Provides the target reaction identities and products; used to compare chemistry, not to require unselected downstream branches.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：Shows target enzymes and ECs; does not support the answer&#x27;s alternative arginase route.

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> For the six required target reactions, no target enzyme/function is delivered. The answer gives arginase and an unnamed L-canaline aminotransferase for an alternative two-step route; wrong-route internal enzyme consistency cannot earn target credit. S=0 and C=0, so the &#91;1,2&#93; band applies. Choose 1 because there is no usable target catalytic correspondence for the specified route.

<details><summary>V0.4理由与本行变化背景</summary>

D3a酶对应：S1给arginase EC 3.5.3.1（水解酶大类与水解反应类型匹配，文献中arginase可水解canavanine），属合理候选，但非gold指定酶且冻结证据无EC 3.5.3.1记录可核；S2仅给canaline aminotransferase名称，ec_number/gene_or_protein均null，机制未确证。有合理候选与部分支持，关键步骤缺具体核验，不构成EC大类与反应类型不匹配或酶名-EC矛盾的关键错误；5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：Lists the accepted target enzyme functions for S01-S06; does not support arginase or an unannotated canaline aminotransferase as target steps.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：Shows the target directed reactions; alternative-route reactions are not target credit.

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> P. putida taxid 303 is a real species-name/TaxID association, but the answer uses it as the sole step organism and as complete_pathway_organism_profile_id without step-level or whole-path capability evidence. The gold target organisms are different (P. canavaninivorans, with other legitimate isozyme-associated organisms), and E0 BacDive 12880 is a different strain record supporting only collection/temperature facts. This is a D3b key error for unsupported whole-path capability; cap at 4. Choose 4 because the species identity is at least name-supported and the attribution is explicit, but the main microbial recommendation is not adequately supported.

<details><summary>V0.4理由与本行变化背景</summary>

D3b微生物：TaxID 303=Pseudomonas putida经E0核实SUPPORTED（学名匹配），身份无编造；但答案以种级P. putida承担整条降解路径（complete_pathway_organism_profile_id=ORG_001），其canavanine降解能力无独立实验或条目证据，E0 BacDive 12880为P. putida mt-2 PaW1菌株记录、底物面板无canavanine项；且gold该路线菌为Pseudomonas canavaninivorans。身份正确、能力声称缺乏适用证据，属有合理候选和部分支持但关键作用范围未充分核验，5–6档取5；因无身份错配、无编造，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Supports official species-name/TaxID association only; does not support canavanine degradation or whole-pathway capability.
- E0_EVIDENCE / f3e0:bacdive:12880：BacDive strain mt-2 PaW1 record supplies culture collection and culture-temperature facts; does not establish P. putida species-level traits or L-canavanine pathway capability.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_149：Shows target-step organisms in gold; P. putida is not the gold whole-path organism.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> The answer returns all 15 traits for P. putida and labels several as low confidence/null where unknown. Many general traits are plausible for P. putida (Gram-negative rod, motile, non-sporulating, mesophilic, non-halophilic, broad habitat), but the evidence registry is only INTERNAL_KNOWLEDGE_ONLY, and key claims such as canavanine use, arginase activity, and broad degradation capacity lack applicable strain/pathway evidence. Some traits are accurate at a general level, but key support is insufficient; 5-6 band, choose 5.

<details><summary>V0.4理由与本行变化背景</summary>

D4性状：15项全填，结构规范；P. putida的形态（直杆状）、革兰氏阴性、运动性、好氧呼吸、不产孢、中温、非嗜盐、土壤/根际广布等教科书级性状大体正确，F5保藏与F14基因组诚实null。但F3 pH 6.0–7.0–8.5、F7『以L-canavanine为氮源』、F9『精氨酸酶型水解L-canavanine』等关键项无来源、confidence low或由S1推导，属部分性状准确适用但关键项证据不足；5–6档取6。未把预测值冒充观测（confidence分级明确），不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Species-name/TaxID only; not species-level trait verification.
- E0_EVIDENCE / f3e0:bacdive:12880：Strain-level culture temperature and collection facts only; does not verify most species-level traits or canavanine use.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> All answer evidence_registry entries are INTERNAL_KNOWLEDGE_ONLY with null database, record, and locator fields. Decision-relevant claims for route, enzymes, organism identity/capability, and traits therefore have MISSING_SOURCE rather than locatable external evidence. There is no verified mis-citation, so no D5 cap applies, but the dimension is in the low source-missing band. Choose 2 because claim-to-internal-ID mapping exists but no important conclusion is externally traceable.

<details><summary>V0.4理由与本行变化背景</summary>

D5可追溯性：evidence_registry三条全部为INTERNAL_KNOWLEDGE_ONLY（EVID_001/002/003），无数据库/文献可定位条目，决策相关组（路线核心步骤、起点、终点、酶-EC、微生物身份）均属MISSING_SOURCE。按P34/P41，全部仅有内部知识自我声明→低分档，默认不cap；因答案对每条证据给出claim_scope与confidence，结构优于完全无记录，取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Only verifies the P. putida TaxID-name association; it is not delivered by the answer as its source.
- E0_EVIDENCE / f3e0:bacdive:12880：Only strain-level collection/temperature facts; not used by answer as a locatable citation.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> The answer gives explicit uncertainty statements, uses nulls for unknown culture collection and genome fields, flags the unverified route/mapping and the speculative second-step mechanism, and labels many trait values low or medium confidence. It still somewhat overstates P. putida as a representative whole-path organism and uses internal general knowledge for several trait claims. Most major uncertainties are disclosed, with some confidence still exceeding support. 7-8 band, choose 7.

<details><summary>V0.4理由与本行变化背景</summary>

D6证据性质：uncertainties列5条具体不确定性（无法确证题面路线、S1酶可能为特异性canavanine hydrolase、S2机制未定、氧条件未指定、种级无保藏号），confidence分级使用规范、null使用诚实、区分观测/预测/未知较好。唯route_summary称P. putida为『代表降解菌』、F7/F9把canavanine氮源与酶活作为较肯定陈述，属局部过度确信而非系统性误导（非多点掩盖矛盾）。7–8档取7，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit disclosure of unverified route, enzyme, strain, and trait limitations; does not convert unsupported claims into verified facts.

</details>

## DeepSeek

答案SHA256：`4374ec46a0c12c9c1279f570600a61697e49fbe6d0d38d0687ddde5dea7d86ec`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 题面锁定L-canavanine degradation II；答案在route_scope回显该路线名，但steps只交付canavanine→canaline→homoserine两步水解，6个必答步0步对应，属P100“自称合规却交付不同化学路线”的D1关键错误（cap≤4）。路线/酶/菌/15项性状等模块形式齐全，故在&#91;1,6&#93;允许范围内取3，不取1–2（非整段缺失）也不取5–6（任务核心已失效）。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖登记层面各模块均有可辨认交付（2步、2酶、1菌profile、15项性状、2条证据条目、2条不确定性），但题面点名路线 L-canavanine degradation II 的指定主链几乎未实质交付：答案首步改用 arginase(EC 3.5.3.1) 将 L-canavanine 水解为 L-canaline+尿素，第二步以 canaline hydrolase 得 L-高丝氨酸+羟胺，与gold主链（canavanine-gamma-lyase EC 4.4.1.43 起始、经 homoserine dehydrogenase/aspartate-semialdehyde dehydrogenase/aspartate ammonia-lyase 至 Fumarate|Hydroxyguanidinium）完全不同，却在 route_scope 原样回填题面路线名，属「自称合规却交付不同路线」的任务参数偏离（八.D1/D2边界、表5 D1行），构成D1关键错误；cap档内因结构完整、性状齐全取3分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：列出本案6个必答步及其酶名/EC，仅支持“必答范围包含这些步”，不证明替代水解路线在自然科学上为假
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：给出各必答步的底物/产物与方向，用于判定答案两步不属于指定主链；不外推到其他路线不存在
- ANSWER_TEXT / ANSWER#BIOPATH150_149：仅用于定位答案实际交付内容，不作为科学支持

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案两步水解在方向（降解）、原子计量与衔接上自洽：canavanine+H2O→canaline+urea；canaline+H2O→homoserine+hydroxylamine；每步前后衔接连续。但该化学链止于L-homoserine，未连接到参考主链后续转化（homoserine→aspartate semialdehyde→aspartate→fumarate）及题面终点（Fumarate|Hydroxyguanidinium），作为“L-canavanine degradation II”主链的化学依据不足。按程序给定D2允许区间&#91;1,4&#93;取上沿4；不按步骤覆盖率换算D2分。

<details><summary>V0.4理由与本行变化背景</summary>

按四.5四步：(1)题面已指定具体路线，进入第2步；(2)答案未在 route_scope/notes 声明替代路线或范围边界，反而回填 route II，属未声明偏离；(3)偏离无可核证据（evidence_registry 两条均为 INTERNAL_KNOWLEDGE_ONLY）；(4)偏离使本维主要结论失效——首步化学与指定路线首步不同，且止于 L-高丝氨酸、未达指定路线终点 Fumarate|Hydroxyguanidinium，属「错误起始步/未声明地严重偏离指定路线」，触发D2 cap≤4。档内按答案自身化学质量取上限：两步水解方向正确、原子与电荷计量自洽（canavanine+H2O→canaline+urea；canaline+H2O→homoserine+NH2OH）、中间体衔接连贯，故取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：用于对照主链转化与终点；不证明答案两步化学式不成立
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_149：给出路线根化合物与terminal_compound_names(Fumarate|Hydroxyguanidinium)，用于范围边界

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分4 → V0.5新分1，变化-3。

新裁判理由：

> 酶模块已实际交付（step.enzyme非空，故不按整维MISSING=1处理），但6个必答步0步对应：答案两步为canavanine→canaline（arginase, 3.5.3.1）与canaline→homoserine（canaline hydrolase, 3.5.3.17），不含导入步、canavanine-gamma-lyase、homoserine dehydrogenase、aldehyde dehydrogenase、aspartate ammonia-lyase或羟基胍转运任一步。逐目标事实均为未交付/另一反应，S=0、U=0→按C04落&#91;1,2&#93;；无任何可用目标催化对应，取1；错误路线内部酶自洽不增加目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

两步酶名与EC大类内部不矛盾（均填水解酶类），但：(i) arginase EC 3.5.3.1 对 L-canavanine 的适用性属酰胺水解酶广谱外推，却标 confidence=high；(ii)「canaline hydrolase」填 EC 3.5.3.17，而该EC亚类为线性脒水解酶，与本步 N–O 键裂解底物类别的相符性存疑；(iii) 两个EC在冻结证据快照中均无记录（GAP-149-002/004/005/008），accepted name/reaction 与底物适用范围无法核对；且与指定路线酶集不对应。按「若干关键步骤酶对应仍缺具体核验」取4；疑似问题登记为UNRESOLVED，不判Y、不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：给出6个必答步的accepted酶/EC集合；仅支持这些步可被哪些酶催化，不支持答案酶属于该集合
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：给出各步底物-产物，用于判定答案两步不是任一必答步反应

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 答案把两步都归给Sinorhizobium meliloti 1021（TaxID 266834），并以complete_pathway_organism_profile_id=ORG_001声称其完成整条路线。E0无该taxid记录（GAP-149-012/013），无任何适用身份或能力证据；该菌也不对应参考中任一步的微生物（P. canavaninivorans为主，另见H. elongata/E. coli行）。身份为真实物种/菌株形式、未核实为编造，不按跨类群cap；但步级归属与整路能力均无支持，属多处能力不匹配/无适用依据，落3–4档取3，不升5–6。

<details><summary>V0.4理由与本行变化背景</summary>

两步反应与 complete_pathway_organism_profile_id 均绑定 Sinorhizobium meliloti 1021（TaxID 266834、ATCC 53121），但TaxID与保藏号在本快照无记录（GAP-149-012，已入查询计划待联网卡），身份定位层、反应级能力层、全路径能力层三层均只有 INTERNAL_KNOWLEDGE_ONLY 声明：把两步反应能力和整条路径完成能力一并归于单一菌株而没有任何独立反应级或全路径证据；step.microorganism.evidence_id 与反应共用同一条内部证据，不能分层支持。因身份无法核实、也不能仅因与gold菌株不同判错，不cap；按「关键身份或作用范围仍未充分核验」取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_149：给出各必答步的参考微生物身份；不支持S. meliloti 1021参与任一步，也不据此断言其绝对不能
- E0_EVIDENCE / f3e0:taxid:303：仅陈述Pseudomonas putida种级分类记录；与S. meliloti身份/能力无关，不支持任何答案声称

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D4只评ORG_001（Sinorhizobium meliloti 1021）的性状正确性与适用性。SUPP:TAX:266834仅核实其分类身份；冻结trait_gold与可评分掩码没有该菌任何性状行。答案15项性状多仅有EVID_002 INTERNAL_KNOWLEDGE_ONLY且raw_text为null，F8“可降解L-刀豆氨酸”和F9“精氨酸酶/刀豆氨酸水解酶活性”是支撑目标能力的关键性状，却无S. meliloti 1021菌株级证据；SUPP:PMID:36320885摘要只支持某些Rhizobiales存在canavanine-γ-lyase途径，不能确认该菌株或该酶活组合。其余如Gram-negative、rod、non-spore、基因组信息等虽大体合理，但本地无来源可核。因此D4落在“部分性状准确且适用，但关键项证据不足”的5分档；不判1–4因无已核数值/菌株错配，不判7–8因关键性状未获可核支持。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状结构完整，F4盐度以全null+confidence unknown明确未知；已给值（F2 最适30°C/中温、F3 最适pH 7.0、F14 GCF_000006965.1/6,691,694 bp/GC 62.7%、F5 ATCC 53121、F1/F6 好氧/O2、F10 运动、F11 杆状、F12 革兰氏阴性、F13 不产孢、F15 土壤/根际/根瘤）彼此自洽、与所声称菌株身份一致，未见数值离谱、单位错误或把观测推广成耐受极限的情形；但全部性状挂同一条 INTERNAL_KNOWLEDGE_ONLY 证据、无 raw_text、无外部可定位来源，且本快照对 taxid 266834 无任何可评性状记录（trait_scoreability_mask 全部 completeness_only），而支撑推荐的关键性状（F8 降解能力、F9 酶活）恰为零证据。按「部分性状准确且适用，但关键项证据不足」取5；未核数值按四.4/P48 登记，不改判NE。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;EVALUATOR_REFERENCE_SUPPLEMENT_USED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / organism_profiles&#91;0&#93;.traits：答案给出的ORG_001 S. meliloti 1021的15项性状及其confidence/evidence_id；用于检查所声称内容，不证明其科学正确性。
- E0_EVIDENCE / SUPP:TAX:266834：仅支持Rhizobium meliloti (strain 1021)的分类身份、rank与别名；不支持任何性状数值、酶活、降解能力或全路径能力。
- GOLD_SLICE / trait_gold.tsv：冻结gold性状表本题行仅覆盖Pseudomonas canavaninivorans、Halomonas elongata、Escherichia coli；无Sinorhizobium meliloti 1021性状行，不能核验ORG_001性状值。
- GOLD_SLICE / trait_scoreability_mask.tsv：可评分掩码仅列上述三菌，无S. meliloti 1021的可评分性状子字段；说明该profile的性状无本地gold可用作准确率核验。
- E0_EVIDENCE / SUPP:PMID:36320885：摘要仅支持某些Pseudomonadaceae与Rhizobiales共生菌经canavanine-γ-lyase/homoserine途径利用canavanine；不支持S. meliloti 1021菌株具有arginase/canaline hydrolase活性或菌株级性状数值。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案全部关键结论（路线两步、两个酶/EC、菌株、15性状）只挂EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，无可定位条目或文献，等同决策相关组全部MISSING_SOURCE，按低分档&#91;1,2&#93;。因答案确实建立了证据登记与claim_scope对应（路线/酶/菌 vs 性状分开），可取2；无已核实错引，不cap，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

<details><summary>V0.4理由与本行变化背景</summary>

答案 evidence_registry 仅 EVID_001/EVID_002 两条，source_type 均为 INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 全为 null，按四.3属 MISSING_SOURCE（完全无引用或仅自我声明），不能计为条目级可定位证据；决策相关组 CG01/CG02/CG03/CG05/CG07 全部仅有此类自我声明，落低分档（默认不cap，表5 D5行）。无任何经核实的错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION；EC 3.5.3.1/3.5.3.17、TaxID 266834、GCF_000006965.1 因冻结快照无记录保持UNRESOLVED，不判虚构、不判CONTRADICTED。取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：该记录为Pseudomonas putida mt-2 PaW1菌株记录；与答案S. meliloti及两步水解无关，不支持任何答案声称
- E0_EVIDENCE / f3e0:taxid:303：Pseudomonas putida种级分类记录；不核实S. meliloti，也不支持答案的酶/路线声称

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案明确把全部证据类型标为INTERNAL_KNOWLEDGE_ONLY，给出2条uncertainties（路线可能还有下游步骤、酶名/EC可能有同义词）并分级confidence，属正向披露；但酶/EC标high confidence且无任何核验，未披露所答化学与指定路线不一致、也未披露整路菌声称缺少依据，部分结论强度超过依据。落5–6档取5，不升7–8（未说明主要限制与冲突），不降至1–2（非系统性冒充实证）。

<details><summary>V0.4理由与本行变化背景</summary>

答案给出两条 uncertainties，逐项标 confidence，把 F4 明确置 unknown，并把来源类型如实标为 INTERNAL_KNOWLEDGE_ONLY，具备基本不确定性披露；但关键处强度超过依据：仅凭内部知识把两步EC标 high、把 S. meliloti 1021 的全路径能力写成事实、route_scope 仍宣称 route II 而对其化学主链与指定路线的差异零披露。属单点/多点过度确信而非系统性伪造（来源类型已如实标注，未见掩盖已核实矛盾），按D6严重度条款档内扣分，取5，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER#BIOPATH150_149：仅用于定位披露文字与confidence字段，不构成科学支持

</details>

## Kimi

答案SHA256：`4050c606fb7cc089c23784dc8e90ccbf894d3738d22f32a162b6c3f9f3820dcb`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> D1按任务路线符合度与完整性判为3–4档低分：答案只给两步（arginase、L-canaline reductase），且第一步产物L-canaline不是冻结L-canavanine degradation II主链中的可对应步骤；题面路线名虽回显，实际主链与gold/accepted酶链不符，属于任务路线偏离与大量必要步骤缺失。

<details><summary>V0.4理由与本行变化背景</summary>

六模块均有交付：路径2步、每步酶与菌、单profile 15项性状（10填5明确未知、0遗漏）、evidence_registry 4条、uncertainties 5条，结构完整；但题面明确指定路线并规定不得改选，答案在route_scope.notes/route_summary中自称即为L-canavanine degradation II，实际交付的却是arginase(EC 3.5.3.1)水解产L-canaline+urea、再经L-canaline reductase还原裂解产L-homoserine+NH3的两步路线，与冻结gold该路线主链（canavanine-gamma-lyase EC 4.4.1.43→L-homoserine+Hydroxyguanidinium→homoserine dehydrogenase 1.1.1.M79→aldehyde dehydrogenase 1.2.1.M5→aspartate ammonia-lyase 4.3.1.1→Fumarate+Ammonium）在首步酶、中间体与终点上全部不同，属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离，按P100归D1关键错误、cap≤4；档内因结构完整、模块缺失少取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：列出冻结路线S01–S06的accepted酶与EC；不证明答案的两步arginase/L-canaline reductase路线属于该任务主链。
- ANSWER_TEXT / ANSWER.steps：仅说明原答实际只交付两步及其化学内容，不用于支持任务正确性。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> D2只评价所答化学自身的连续性/方向/守恒。两步中L-canavanine→L-canaline+urea及L-canaline→L-homoserine+ammonium在局部化学上可讲通，但主链不连接冻结路线的canavanine-gamma-lyase分支，终点停于L-homoserine而非gold的Fumarate/Hydroxyguanidinium分支终点；属于弱档，给4而非3，因局部两步方向与结构大体自洽，但主链目标和终点严重不衔接。

<details><summary>V0.4理由与本行变化背景</summary>

答案两步化学自身尚自洽（水解产canaline+urea；NADPH依赖N–O键还原裂解产homoserine+NH3，水与NADPH/NADP+辅因子在列，SMILES与主产物对应），但本维评价的是题面指定路线的主链化学：该路线首步为canavanine-gamma-lyase(EC 4.4.1.43)直接裂解生成L-homoserine+Hydroxyguanidinium，随后homoserine dehydrogenase(1.1.1.M79)与aldehyde dehydrogenase(1.2.1.M5)生成L-aspartate，再经aspartate ammonia-lyase(4.3.1.1)产fumarate+ammonium；答案两步的转化类型、中间体与终点完全不同，且未被声明为替代路线而是声称即为该路线，按四.5第2/4步判定偏离使本维&#x27;指定路线主链化学成立&#x27;主要结论失效，cap≤4；档内因化学自洽、辅因子在列取4。与D1共用RE-01但本维依据为化学层而非任务参数层。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：给出冻结路线各步的底物/产物、方向与分支终点；用于对比答案主链，不作为替代化学必然错误的证明。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_149：gold终点为Fumarate|Hydroxyguanidinium；不支持答案将L-homoserine作为该路线末端。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> D3a只计目标反应对应，不按所答替代路线计。答案仅给出精氨酸酶（arginase，EC 3.5.3.1）将L-canavanine水解为L-canaline与urea，以及无EC的L-canaline reductase将L-canaline还原裂解为L-homoserine与ammonium；这两步均不对应本题目标步（如S01 ABC-type L-canavanine importer/7.4.2、S04 canavanine-gamma-lyase/4.4.1.43、S05 aspartate ammonia-lyase/4.3.1.1等），也未给出目标主链终点Fumarate/Hydroxyguanidinium。酶模块并非全空，故不记整维MISSING；目标反应无S可用且无可核目标酶对应，按C04低带&#91;1,2&#93;取C05的1，未把错误路线内部自洽当作目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

步骤1给arginase/EC 3.5.3.1，名称-EC大类-反应类型（水解）自洽，属合理候选；但对L-canavanine底物的催化声称在E0无冻结EC记录（GAP-149-001/002/006），无法核accepted name/reaction与底物范围。步骤2给&#x27;L-canaline reductase&#x27;，无EC、gene/protein为null、EVID_003无database/record/locator，属推定候选。两关键步骤均缺具体核验，且都不是gold该路线关键酶（4.4.1.43/1.1.1.M79/1.2.1.M5），落5–6档取5；因属无法核验而非已证实错配，关键错误记UNRESOLVED、不cap（局部未核见unverified_subclaims）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：列出本题目标步骤酶，包括S01 ABC-type L-canavanine importer/7.4.2、S04 canavanine-gamma-lyase/4.4.1.43、S05 aspartate ammonia-lyase/4.3.1.1等；不支持答案的arginase与L-canaline reductase作为目标步对应酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：给出本题目标主链反应物、主产物及有向连接；答案的L-canavanine→L-canaline/urea→L-homoserine/NH4为另一反应序列，不能获得目标反应对应信用。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> D3b给5–6档。答案物种名Pseudomonas canavaninivorans与gold organism_gold的EXACT物种身份一致，且gold标PATHWAY_COMPLETE；但答案未给菌株、TaxID或菌株级能力证据，并把答案自设的两步arginase/L-canaline reductase反应都归给该种，步骤级能力仍待核。身份对但不支持进入7–8档。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份Pseudomonas canavaninivorans与gold路径菌一致（TaxID 2859001、GCA_024749365.1，见FV-01），未编造菌株号/TaxID/保藏号（均填null），不存在跨类群或异菌株错配、也无引用背书的编号错配；但两步的反应级能力（arginase、canaline reductase）与种级性状仅凭种名与属级通性内部知识推定（EVID_004），未达反应级证据，且与gold该路线所载酶谱不同。身份层正确、能力层未核，落5–6档取5；无已核实身份错误，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_149：gold确认Pseudomonas canavaninivorans TaxID 2859001及整条路径能力；该支持不自动证明答案两步替代反应的步骤级归属。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;：答案仅给物种名，未给菌株、TaxID及菌株级能力证据。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> D4给5–6档下限。原答15项字段齐全，多数未知项诚实填null或unknown；但唯一有gold观测的F14（GCA_024749365.1）未填，其余F1/F6/F7/F10–F13/F15主要是假单胞菌属级通性推定，非P. canavaninivorans菌株级证据。部分性状可作低置信候选，但关键项证据不足、适用性需实质修订。

<details><summary>V0.4理由与本行变化背景</summary>

仅1个profile：10项给值全部confidence=low并在raw_text明示&#x27;属级通性/推定/未核对&#x27;，5项（F2/F3/F4/F5/F14）诚实null，未见把预测当观测、也无数值离谱项；但所给性状是假单胞菌属通性外推到种级（革兰氏阴性、杆状、极生鞭毛、不产芽孢、好氧/O2末端受体、土壤水体栖息地），L-canavanine碳氮源利用靠种名推定，均无种/株级观测支持；gold该种除F14基因组OBSERVED外全部UNKNOWN（trait_scoreability_mask均为completeness_only），无法逐项核实；F14 null 而gold有GCA_024749365.1属完成度缺口（主记D1）。落5–6档取5，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_149：P. canavaninivorans仅F14有可观测genome/TaxID记录，其余性状为UNKNOWN；不支持把属级通性写成该种观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_149：标注P. canavaninivorans仅F14为observed_accuracy，其他多为completeness_only；用于区分完整度与准确性。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> D5按实际交付来源评3–4档。EVID_001给MetaCyc PWY-5505名称/URL但E0无记录且原答自认凭记忆；EVID_002只给ExplorEnz/BRENDA与EC 3.5.3.1，无locator且E0无EC记录；EVID_003无record/locator；核心微生物与属级性状仅EVID_004 INTERNAL_KNOWLEDGE_ONLY。未发现已核实错引，故不cap；但核心路线/酶/菌来源关联很弱。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry有4条且逐条写明claim_scope，映射结构良好；但决策相关组无一条经核实可定位：EVID_004为INTERNAL_KNOWLEDGE_ONLY，承载全部微生物归属与性状（MISSING_SOURCE）；EVID_002的EC 3.5.3.1在E0无记录（UNRESOLVED_SOURCE）；EVID_001的MetaCyc PWY-5505为自由文本URL且未解析（GAP-149-011，UNRESOLVED_SOURCE）；EVID_003无database/record/locator（GENERIC_SOURCE）。无任何已核实错引（查不到≠虚构≠CONTRADICTED），不触发cap；按四.3/P41落3–4档，因注册表结构清楚、逐claim范围明确取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示原答仅交付上述来源记录与内部知识声明；用于D5来源状态，不用于证明科学内容正确。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> D6给7–8档。原答明确说明多项未知、低置信度、L-canaline reductase无EC、PWY-5505为凭记忆、NADPH/NADP(+) SMILES未填、菌株/TaxID未知；未把内部推定系统性包装成实验观测。仅路线摘要“主链为两步”语气略强，但整体限制披露充分。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体较好：EVID_004标INTERNAL_KNOWLEDGE_ONLY，性状逐项标&#x27;属级通性/推定&#x27;与low/unknown，酶2无EC并明确写出机理二选一（NADPH还原裂解 vs 水解产羟胺）的不确定性，uncertainties还主动提示PWY-5505凭记忆可能编号偏差，观测/预测/未知区分清楚、主要限制具体；不足：route_summary把&#x27;两步主链&#x27;作为该路线的定义性陈述（未提示路线身份可能不符，与D1/D2问题同源却零披露），步骤1酶给medium而其底物催化未核。属&#x27;大部分标注正确、少量结论强度略超依据&#x27;，落7–8档取7，非系统性误导不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：原答实际披露了主要未知、机制不确定性与来源记忆风险；支持D6中高档。

</details>

## Qwen

答案SHA256：`62469c7ff2ac09802d904841b2508905b8a4eb6a11dbf5d0edd202161d5d58a7`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 题面要求 L-canavanine degradation II 主链；答案虽回填路线名，但仅给3步，实际为转氨-脱羧-水解的不同路线，Gold 的 S01 importer、S04 canavanine-gamma-lyase、S05 aspartate ammonia-lyase、S06 antiporter 等必要主链/终点步未交付。JSON与性状外壳完整，但任务符合度失败，按D1任务偏离与缺步在&#91;1,6&#93;内取3。

<details><summary>V0.4理由与本行变化背景</summary>

结构层完整：3步均给出主底物/主产物英文名与SMILES、辅因子角色（2-oxoglutarate/L-glutamate、H2O/CO2）、首选酶与对应菌；15项性状齐全（9填9/6明确null/0遗漏）；evidence_registry与uncertainties在位；chosen_route_name原样回填&#x27;L-canavanine degradation II&#x27;、未改选。但交付的主链化学与题面指定路线不符：以转氨-脱羧-水解替代冻结主链的canavanine-gamma-lyase起始序列，属&#x27;自称合规却交付不同化学路线&#x27;的任务参数偏离（八.D1/D2边界条款），D1关键错误成立、cap≤4；因模块与格式无缺，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BEGIN：题面明确指定 L-canavanine degradation II 并要求按指定路线给出主链；不支持答案可自行改换化学路线。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：列出Gold S01–S06的aced酶与EC；支持答案未交付这些目标步骤，不支持把替代路线回填目标完成。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：列出Gold六步的底物/产物与方向；支持答案路线与指定主链不同，不支持将答案三步视为已交付目标链。
- ANSWER_TEXT / ANSWER_BEGIN：支持答案原文位置与内容；不证明其科学正确或任务符合。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分3 → V0.5新分4，变化+1。

新裁判理由：

> S1转氨与S3水解在方向/连接上可辨认；但S2把2-氧代酸脱羧直接写成生成3-(胍基氧基)丙酸。α-酮酸脱羧应先生成醛，需额外氧化/氧化还原载体才能得到羧酸，答案未给该氧化步骤。主链中间步化学不成立，按D2 &#91;1,4&#93;内给4。

<details><summary>V0.4理由与本行变化背景</summary>

按四.5四步判断：①题面已指定具体路线（L-canavanine degradation II）；②答案未声明替代路线或范围边界（chosen_route_name原样填指定名，route_summary自称&#x27;按转氨-脱羧-水解主链进行&#x27;）；③该替代路线无可核证据（仅INTERNAL_KNOWLEDGE_ONLY，EC全null）；④偏离发生在首步与整条主链，使D2&#x27;路径科学正确且连续、符合任务条件&#x27;的主要结论失效，故cap≤4。三步内部化学大体自洽（α-酮酸转氨、脱羧、O-连接胍基水解），但末步把O-连接羟胍水解产物写成guanidine，比羟胍少一个氧、计量未闭合且无说明；又无任何条目级支持，故档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持S2原文的底物、产物与反应类型；不证明该脱羧产物可直接由所示底物生成。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 六个必答目标步没有一步给出目标accepted酶/功能：S01 importer、S02 aldehyde dehydrogenase、S03 homoserine dehydrogenase、S04 canavanine-gamma-lyase、S05 aspartate ammonia-lyase、S06 antiporter均未交付；答案三步属另一路线，错误路线内部自洽不获目标信用。S=0且事实可判，按C04 &#91;1,2&#93;取1。

<details><summary>V0.4理由与本行变化背景</summary>

三步酶名与所写反应类型在功能类别上一一对应（转氨酶↔转氨、脱羧酶↔脱羧、酰胺水解酶↔C–N水解），不构成&#x27;EC大类与反应类型不匹配&#x27;或&#x27;酶名与EC互相矛盾&#x27;（EC全为null，无可核编号冲突），也未把广谱家族相关性当成具体催化证据，故不触发D3a关键错误。但三个关键步骤全部EC=null、gene/protein=null，证据仅EVID_001内部知识，无任何条目级支持，属&#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;（5–6档），取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_149：列出S01–S06目标aced酶与EC；支持答案所给三种酶均未命中目标步骤。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_149：列出目标步骤的反应方向与主底物/产物；支持答案的转氨-脱羧-水解并非这些目标反应。
- ANSWER_TEXT / ANSWER_BEGIN：支持答案三个enzyme.name与EC null的原文位置；不证明这些酶对应目标步。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> TaxID 303 与 Pseudomonas putida 的物种名有官方记录支持，但答案把所有三步及完整路径能力都归给该种，未给菌株、单步催化或全路径能力证据；目标路线Gold主要对应 P. canavaninivorans，另有个别步对应 H. elongata/E. coli。身份可定位但能力声称严重超范围，按D3b身份/能力分层给4。

<details><summary>V0.4理由与本行变化背景</summary>

身份层：Pseudomonas putida + TaxID 303，经E0官方分类记录核实为CURRENT学名，且声称粒度为物种级（strain=null），与记录粒度一致，不构成身份错配或编造，故不触发D3b身份阶梯①–③的关键错误。能力层：S1–S3三步催化归属与complete_pathway_organism_profile_id=ORG_001的整条路径能力声称均无条目级支持（EVID_001仅内部知识），冻结证据亦无P. putida降解canavanine的记录；gold的PATHWAY_COMPLETE菌为Pseudomonas canavaninivorans(2859001)，三步菌与之全部不同。按&#x27;未核不得凭记忆放行、也不得凭记忆判错&#x27;记UNRESOLVED。落在&#x27;多处反应能力缺乏匹配支持、把无单步支持的菌写成整条路径能力&#x27;的3–4档，取4（身份要素正确使其不至更低）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持TaxID 303为Pseudomonas putida的物种名/分类记录；不支持任何催化或全路径能力。
- E0_EVIDENCE / f3e0:bacdive:12880：支持P. putida mt-2 PaW1菌株记录、保藏号与培养温度；不支持该菌完成L-canavanine degradation II或各步催化。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_149：列出Gold步级微生物主要为P. canavaninivorans（个别步H. elongata/E. coli）；不支持答案的P. putida全链归属。
- ANSWER_TEXT / ANSWER_BEGIN：支持答案将P. putida重复绑定到三步并声明complete_pathway_organism_profile_id=ORG_001。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 15项性状外壳齐全，9项有值、6项null；F1/F6/F10/F11/F12/F13/F15等P. putida种级一般性状合理，但F8/F9把目标路线降解能力与转氨酶活当作该种性状，均为低置信INTERNAL_KNOWLEDGE且无冻结证据；无具体菌株，属种级泛化。按D4部分性状可用、关键功能项证据不足给6。

<details><summary>V0.4理由与本行变化背景</summary>

15项齐全（9填9/6明确null/0遗漏）。已填项集中于物种级一般性状（F1 aerobic、F6 aerobic respiration/O2、F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming、F15 soil and water），与P. putida一般描述相符，但全部无条目级来源（EVID_002为INTERNAL_KNOWLEDGE_ONLY、raw_text=null）；任务关键项F8（降解能力）与F9（转氨酶活）与本答案未证实的路线绑定，缺支持；数值类性状（F2/F3/F4/F5/F14）如实留null，未用近似值占位，也没有把物种级观测推广成菌株级。属&#x27;部分性状准确且适用，但关键项证据不足&#x27;（5–6档），取5。全部confidence=low并在uncertainties声明为物种层泛化，未构成&#x27;预测冒充观测&#x27;，不触发D4关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持各性状的值、raw_text、confidence与evidence_id原文；不证明其逐项准确。
- E0_EVIDENCE / f3e0:bacdive:12880：仅支持P. putida mt-2菌株的保藏号与26/30°C培养记录；不支持F8/F9及多数种级性状，也不支持37°C为最适值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_149：本题可打分性状表未列P. putida；该表支持“不能把Gold其他菌的性状观测直接套给本答案菌”。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> D5只评价答案实际交付来源：evidence_registry两条均为INTERNAL_KNOWLEDGE_ONLY，无database、record_id或可定位文献；路线、酶、菌、性状关键结论均无可核查来源。按MISSING_SOURCE低档，缺失不属于已核实误导，故不cap，给1。

<details><summary>V0.4理由与本行变化背景</summary>

答案仅交付两条EVID_001/EVID_002，source_type均为INTERNAL_KNOWLEDGE_ONLY、database/record_id为null，locator为自由文本描述；按四.3属MISSING_SOURCE（完全无引用或仅内部知识自我声明）。决策相关组CG01/CG02/CG03/CG05/CG07/CG08/CG09全部为MISSING_SOURCE，无一条条目级可定位可核对证据→&#x27;全部缺失→低分档&#x27;，默认不触发cap。答案对无来源一事披露清晰（source_type明示、confidence=low、uncertainties列明未核实），故取低分档上限2而非1。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持evidence_registry两条均为INTERNAL_KNOWLEDGE_ONLY、database/record_id为null，以及uncertainties原文。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案对酶EC、菌株、性状普遍标low/unknown，明确列出未在线核实、EC null、菌株/保藏未核、氧条件未指定，且未把INTERNAL_KNOWLEDGE写成实验观测；但route_summary与F8仍以陈述语气给出路线能力，故未给9–10，给8。

<details><summary>V0.4理由与本行变化背景</summary>

正面：全部结论统一标confidence=low，evidence_registry明示source_type=INTERNAL_KNOWLEDGE_ONLY，uncertainties具体列出三处限制（未能核实MetaCyc/BioCyc的具体反应与EC、菌株与保藏信息未核实且性状为物种层泛化、氧条件未指定），每步uncertainty字段也写明EC与菌株未核；未把预测冒充实证观测。不足：置信度一律low而无分层，route_summary以肯定语气陈述&#x27;按转氨-脱羧-水解主链进行&#x27;，未在摘要处标注该主链属推断而非已核实路线，个别结论强度略超依据。落5–6档取6；单点/统一过度自信不等于系统性误导，无掩盖已知矛盾证据，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BEGIN：支持低/未知置信、uncertainties列表与INTERNAL_KNOWLEDGE_ONLY来源类型；不证明路线能力本身正确。

</details>

## Grok

答案SHA256：`54e43797c267425e7573ee3afe46fd3398cf25693bccee3a055dec0a68b689b3`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 3: the route name is echoed, and enzyme/microorganism/trait/evidence modules are present, but the main route is mostly undelivered: only one of six required gold steps is supplied, with S01/S02/S03/S05/S06 absent. This is a major completeness defect, not an entirely unreadable answer.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Lists six required route steps; the answer supplies only a single S04-type hydrolysis step and omits the other five required steps.

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 5: the single delivered transformation matches the gold S04 chemistry (L-canavanine + H2O -&gt; L-homoserine + hydroxyguanidinium) and is directionally plausible, but the answer presents it as the whole main route and omits the downstream homoserine/aspartate/fumarate branch and the S06 branch. The main trunk is only partly established.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Gold S04 is L-canavanine + H2O -&gt; L-homoserine + hydroxyguanidinium; it does not support treating this single step as the complete six-step route.

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a 2: five of six required target reactions are missing. The only delivered step&#x27;s substrate/product chemistry is locally consistent with gold S04, but its enzyme is given as the descriptive &#x27;L-canavanine hydrolase&#x27; with no EC and is not confirmed against the accepted canavanine-gamma-lyase EC 4.4.1.43. The usable target coverage is 0-1/6, so the low &#91;1,2&#93; band applies; 2 rather than 1 reflects the one locally useful S04-type reaction.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：Gold S04 accepted enzyme is canavanine-gamma-lyase EC 4.4.1.43; answer gives no EC and a descriptive hydrolase name, so enzyme identity is not confirmed.
- GOLD_SLICE / reaction_gold.tsv：Gold requires six target steps; answer supplies only one S04-type step, so five targets are absent.

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3b 5: Enterococcus faecalis and TaxID 1351 form a plausible species-level identity, and the historical Streptococcus faecalis connection is disclosed. However no strain is given, the reaction-level capability is sourced only from internal knowledge, and the gold route assigns S04 to Pseudomonas canavaninivorans. The correspondence is partial and not verified at the required granularity.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：Gold S04 microorganism is Pseudomonas canavaninivorans TaxID 2859001; this supports an organism mismatch, but does not by itself prove E. faecalis cannot catalyze the reaction.

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D4 6: all 15 trait fields are present, with three explicit nulls. Many E. faecalis traits are standard and plausible (Gram-positive coccus, nonmotile, non-sporeforming, facultative anaerobe, mesophilic, 6.5% NaCl category), but several values rely only on internal knowledge, and F6&#x27;s terminal electron acceptor &#x27;pyruvate&#x27; is questionable. No frozen E. faecalis trait record is supplied, so accuracy and applicability are only partially verified.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Gold trait rows cover P. canavaninivorans, Halomonas elongata, and E. coli; no E. faecalis TaxID 1351 rows are present, so the answer&#x27;s E. faecalis traits are not verified by this gold slice.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5 2: the route, enzyme, microorganism and trait claims are all backed only by EVID_001/EVID_002, both INTERNAL_KNOWLEDGE_ONLY, with no DOI, database record, accession or stable locator. This is MISSING_SOURCE rather than verified mis-citation, so no cap applies, but key conclusions are essentially untraceable.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer：Shows both evidence entries are INTERNAL_KNOWLEDGE_ONLY with null database/record_id; no external source is delivered.

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 8: the answer is unusually explicit about uncertainty: it labels many fields null, uses low/medium confidence honestly, discloses the route-number swap risk, says the EC/gene are unknown, keeps strain and genome null, limits traits to species level, and explains SMILES protonation. The main limitations are stated rather than hidden; no systemic overclaim is evident.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / answer：Shows explicit disclosure of route-number uncertainty, missing EC, strain uncertainty, species-level trait limits, and SMILES protonation assumptions.

</details>

## GPT5.6

答案SHA256：`c2abc658c5d2ccbda345063cb65e6913ae34f0fb0a6851483a2b32b1c394b628`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D1 1–2 band: only one non-gold step is delivered, five of six required main-chain steps are omitted, no microorganism and no 15 traits are provided; route chemistry is substituted. Readable partial content supports 2 rather than 1.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Shows six required gold steps S01–S06 and terminal products Fumarate|Hydroxyguanidinium; does not require unmentioned DAG branches.
- GOLD_SLICE / enzyme_gold.tsv：Shows accepted enzymes for the six required steps; the answer&#x27;s single arginase step is not the specified route step.

</details>

### D2 反应化学科学性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D2 base range &#91;1,4&#93;. The single arginase hydrolysis is locally chemically plausible, but it is not the gold main chain and provides no S02–S06 continuity or terminal products. Severe main-chain break; score 2, not 1, because one chemically readable local reaction is present.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Gold S04 converts L-canavanine + H2O to L-homoserine + Hydroxyguanidinium; gold S02/S03/S05/S06 supply continuation. It does not support arginase hydrolysis to L-canaline + urea as this route&#x27;s main chain.

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> C04/C05 bottom anchor: the answer gives one enzyme (arginase EC 3.5.3.1) for a non-gold hydrolysis; no required gold step S01–S06 has an accepted enzyme match. The module is not empty, so it is SCORED at the bottom anchor rather than MISSING. No usable target catalytic correspondence remains.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：Gold accepted enzymes include canavanine-gamma-lyase EC 4.4.1.43 for S04 and other specific enzymes for S01–S06; arginase EC 3.5.3.1 is not listed for this route.

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> No microorganism is delivered: steps&#91;0&#93;.microorganism=null and organism_profiles=&#91;&#93;. The task required a corresponding microorganism for each step. D3b is therefore MISSING=1, not NE and not a scientific-error score.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：Gold lists step-level organisms such as Pseudomonas canavaninivorans; the answer supplies none.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> No organism_profiles and therefore no traits are delivered; all 15 required traits are omitted. Per P44 and the traits-count closure, D4 is MISSING=1 rather than a scientific-error score.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Gold provides trait records for step organisms; the answer provides no trait values or explicit nulls.

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Only EVID_001 is INTERNAL_KNOWLEDGE_ONLY; database, record_id, and locator are null. The key route/enzyme conclusion has no locatable external source. This is MISSING_SOURCE, not a verified mis-citation; D5 is in the 1–2 band and scored 1.

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D6 7–8: the answer labels the route as inferred, sets enzyme confidence low, and explicitly records missing microorganism and downstream-step uncertainty. Minor issue: it states the arginase hydrolysis as the route&#x27;s &#x27;明确主反应&#x27; despite internal-only support, so 7 rather than 8. Missing modules are handled in D1/D3b/D4, not as D6 deception.
