# BIOPATH150_051：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：2-hydroxypenta-2,4-dienoate degradation

污染物：(2Z)-2-hydroxypenta-2,4-dienoate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 76 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 52 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 80 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 57 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 82.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 40.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`5f723f0cfd8867c1506623fa85c0da8c1418bfce42e1ac456cc8b7f82025b8a4`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分9 → V0.5新分9，变化+0。

新裁判理由：

> route_scope.chosen_route_name按题面原样填写；主链为3步，逐步给出主底物/产物、酶与EC、对应微生物，且同一菌去重为1个organism_profile并完整列出15项性状。与本题3步线性唯一主链及终点acetyl-CoA的交付要求基本对应，未见缺步、改选路线或关键模块缺失；仅有少量表述/来源粒度不齐等局部问题，不影响D1完成度结论。

<details><summary>V0.4理由与本行变化背景</summary>

全部适用模块实质回应：主链3步覆盖题面指定路线（chosen_route_name逐字为『2-hydroxypenta-2,4-dienoate degradation』），每步含主底物/主产物(名+SMILES)、首选酶+EC、对应菌；15/15性状、6条证据登记、不确定性说明齐备；步数与gold ordered_step_count=3一致且到达gold终点acetyl-CoA。仅S1中H2O的role标为unknown、step3提及H+未列等细部瑕疵。9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 5f723f0cfd8867c1506623fa85c0da8c1418bfce42e1ac456cc8b7f82025b8a4：答案正文实际包含3步主链、每步底物/产物、酶/EC、微生物，以及1个organism_profile的全部15项性状；route_scope名称与题面一致
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_051：gold正式案为3步线性唯一路径，背景步为0，支持本题完整性对照的分母为3而非全图旁支
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_051：题面指定路线名及gold终点为acetyl-CoA，用于核对route_scope与主链终点是否交付

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 三步主链的化学方向与gold一致：2-hydroxypenta-2,4-dienoate水合生成4-hydroxy-2-oxopentanoate，再经逆羟醛裂解生成acetaldehyde与pyruvate，acetaldehyde再经CoA/NAD+依赖的氧化酰化生成acetyl-CoA；终点与gold terminal acetyl-CoA一致，辅因子和NADH也已列出。局部问题包括：4-hydroxy-2-oxopentanoate未标(S)立体化学，S2把pyruvate标为main而gold标为byproduct，底物/产物的电荷与立体表示不够完整；这些属于局部表示或角色标注问题，不改变主链关键转化与连续性，故在7–8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

三步化学与gold逐步一致：①水合(EC 4.2.1.80)生成4-hydroxy-2-oxopentanoate；②逆羟醛裂解(EC 4.1.3.39)生成pyruvate+acetaldehyde；③CoA/NAD+依赖氧化酰化(EC 1.2.1.10)生成acetyl-CoA+NADH。方向正确、原子收支成立、S3辅因子与NADH在列，替代分支明示is_part_of_scored_main_route=false；仅(4S)立体化学未在SMILES标注（已披露）、S3未列H+。档内9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：gold三步反应及有向连接：S03水合到(S)-4-hydroxy-2-oxopentanoate，S02裂解为acetaldehyde与pyruvate，S01由acetaldehyde+CoA+NAD+生成acetyl-CoA+NADH；同时显示S02中pyruvate为BYPRODUCT、S03产物带(S)立体信息
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_051：gold终点主产物为acetyl-CoA，支持答案主链终点和降解方向
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：三步accepted酶名/EC范围支持答案mhpD 4.2.1.80、mhpE 4.1.3.39、mhpF 1.2.1.10与目标反应的功能对应；不扩展为具体蛋白实验活性证明
- ANSWER_TEXT / 5f723f0cfd8867c1506623fa85c0da8c1418bfce42e1ac456cc8b7f82025b8a4：答案实际给出的三步反应式、SMILES、辅因子、产物角色和终点，用于核对主链化学连续性及局部表示问题

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> Under JUDGE_REQUIRED &#91;1,8&#93;, the answer provides the three required target enzyme functions with explicit ECs: 4.2.1.80 hydratase (answer S1, gold S03), 4.1.3.39 aldolase (S2, gold S02), and 1.2.1.10 acylating acetaldehyde dehydrogenase (S3, gold S01). Each EC/name corresponds to the accepted enzyme sets at G4 curation granularity. The optional mhpD/mhpE/mhpF gene labels and charge/stereo representation equivalence remain UNRESOLVED/MINOR, and 9-10 is blocked by the base gate and KEY target hold. Score 8: main catalytic correspondences are reliable, with limited unresolved local items.

<details><summary>V0.4理由与本行变化背景</summary>

三步酶-反应对应与gold enzyme_gold逐一吻合：EC 4.2.1.80（2-hydroxypenta-2,4-dienoate hydratase）、EC 4.1.3.39（4-hydroxy-2-oxovalerate/oxopentanoate aldolase）、EC 1.2.1.10（acetaldehyde dehydrogenase (acylating)；gold MHPF-MONOMER对应mhpF）；酶名与EC不矛盾，未出现大类别-反应类型错配。E0未收录EC条目（GAP-051-003/005/009）属待核，不构成已核实错误。9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：Lists accepted enzyme names/EC numbers for the three gold steps; does not prove specific protein activity or exact representation equivalence.
- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;.enzyme：Shows answer enzyme/EC pairs; representation and gene attribution are separately unresolved.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：Shows directed reaction context; not a protein-level activity record.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> The answer assigns all three steps to Escherichia coli K-12 MG1655. Gold organism rows list E. coli species 562 for the accepted enzymes at all three steps, and E. coli 562 is PATHWAY_COMPLETE. This supports the species-level E. coli capability and pathway assignment. The specific strain K-12 MG1655 and TaxID 511145 are not present in the frozen E0/gold organism rows; this is a strain-level granularity gap, not a verified contradiction. Same-species support with unresolved strain specificity fits the 7 band; not capped.

<details><summary>V0.4理由与本行变化背景</summary>

菌名Escherichia coli为gold三步EXACT菌，且PATHWAY_COMPLETE(taxid 562)=TRUE支持种级全路径能力；但答案给出菌株K-12 MG1655与TaxID 511145，仅有物种级记录支持菌株级声称——属身份阶梯①粒度不足，档内扣分（约7档），默认不cap；未发现跨属/跨kingdom或同物种异菌株错配，也未由序列存在直接断言整条路径而无任何依据。7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_051：Supports E. coli species-level occurrence for the three accepted enzymes and pathway-complete status; does not certify K-12 MG1655 or TaxID 511145.
- ANSWER_TEXT / ANSWER.steps&#91;0-2&#93;.microorganism：Shows the answer&#x27;s strain-level claim; strain-specific support is unresolved.

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> All 15 traits are present for ORG_001. Species-level E. coli gold supports the general traits: aerotolerant/facultative, Gram-negative, rod-shaped, motile, non-sporulating. Other values are plausible but rely on EVID_006 INTERNAL_KNOWLEDGE_ONLY and are not strain-specific in E0: optimum 37 C, pH 7.0, 0.5-1% NaCl, ATCC 700926, NC_000913 genome size 4,641,652 bp, GC 50.8%, and the broad aromatic/mhp utilization claims. No verified key trait contradiction is present, but several exact K-12/ATCC/genome and catabolic claims need confirmation. Score 7 fits major supported traits with local strain-specific and numeric issues.

<details><summary>V0.4理由与本行变化背景</summary>

物种级关键性状与trait_gold(562)吻合：F1兼性厌氧/耐氧、F4非嗜盐、F10运动、F11杆状、F12革兰氏阴性、F13不产孢均有观测记录；F2中温与F3 pH7.0落在观测范围。但菌株级数值（F5 ATCC 700926、F14 NC_000913/4,641,652 bp/GC 50.8%、F2最适37°C）与F9 mhp酶活、F8芳香族降解、F15栖息地缺E0/gold观测支持，均属内部知识待核；未发现已核实的数值/单位/身份错误，也未把预测冒充观测（F7/F8已标medium并声明未在线核对）。7档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_051：Supports species-level E. coli general traits and some growth/pH/salinity ranges; not K-12 MG1655-specific exact values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_051：Indicates which trait fields are observed/scoreable versus completeness-only or prediction background; does not verify answer&#x27;s internal-only values.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_051：Shows pending/scoreable scalar subfields and gaps; used to bound D4 confidence, not to upgrade unresolved strain-level values.
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：Shows delivered trait claims; many exact values are internally sourced and unverified.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> The answer provides a structured evidence registry: EVID_001 literature citation for the route/enzymes, EVID_002-004 ExplorEnz EC records, EVID_005 NCBI RefSeq NC_000913, and EVID_006 INTERNAL_KNOWLEDGE_ONLY for many traits. Core route/enzyme/microbe claims have locatable citations, but E0 contains no linked records for EC 4.2.1.80/4.1.3.39/1.2.1.10, TaxID 511145/NC_000913, or the EVID_001 citation, so those are UNRESOLVED_SOURCE, not verified and not mis-citation. Many supporting trait groups use EVID_006 and are MISSING_SOURCE. No CRITICAL/SYSTEMIC verified mis-citation; 5-6 band, with 6 because the core claim-to-source mapping is explicit and locatable.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/02/03/05/07/08/09/17）均给出条目级可定位引用（具体EC条目、具体综述全文、RefSeq登录号），但本题E0快照无任何对应记录，全部无法核对→UNRESOLVED_SOURCE；性状支持组多依赖INTERNAL_KNOWLEDGE_ONLY(EVID_006)→MISSING_SOURCE。无任何已核实错引（无VERIFIED_MIS_CITATION_*），不触发cap。按合成规则属『部分关键结论可定位、其余缺可核对映射/待核』，5档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows delivered source record types and mappings; does not verify the content of literature, EC, RefSeq, or internal-only trait claims.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：Confirms the cited EC numbers correspond to accepted enzyme entries; it does not verify EVID_001&#x27;s literature contents or all trait mappings.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> The answer explicitly discloses oxygen condition null, non-online EC checks, possible downstream status of S3, omitted 4S stereochemistry, internal-only trait values, and unverified gene/genome identifiers. It distinguishes database, literature, and INTERNAL_KNOWLEDGE_ONLY source types. Confidence labels are mostly medium and some high on standard E. coli general traits; this is local overconfidence rather than systemic presentation of predictions as observations. Main limitations and conflicts are clearly stated. Score 8: strong uncertainty disclosure with minor overconfidence on internal traits.

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与置信度逐条标注（LITERATURE_DIRECT/DATABASE_DIRECT/INTERNAL_KNOWLEDGE_ONLY、high/medium），uncertainties列6条含立体化学未标、未在线核对、主链终点保留意见与基因编号未核，披露具体且与依据大体相称；但EVID_002–004把记忆来源标为DATABASE_DIRECT(IUBMB ExplorEnz)，与uncertainties自述『未能在线核对数据库原始记录』相互矛盾，属单点过度确信（非系统性误导）；性状raw_text全为null。档内7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows explicit limitation disclosure and source-type labeling; does not verify the underlying scientific claims.

</details>

## DeepSeek

答案SHA256：`2e56406c27423194cfc5906ed12e73991eb3bbb1470dbb593f0b40daafff6795`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 路线名原样填写，S1/S2两步及15项性状均出现；但缺少gold终末步S01（acetaldehyde→acetyl-CoA），主链到acetyl-CoA未交付；route_summary/explanation使用英文，违反文字字段中文要求。按P13/P15/P100，属主要模块涉及但必要内容遗漏。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖gold主链前两步(S1 hydration, S2 aldolase)且路线名原样回填；末步acetaldehyde→acetyl-CoA(gold terminal)未作为评分主链步骤给出，仅在central_metabolism_entry标为下游；15项性状全部返回但F4盐度、F14基因组为诚实null。主要模块均有涉及但缺1个必要步骤，落5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_051：supports required three-step main chain count; not a quality score
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：supports missing terminal conversion and gold terminal acetyl-CoA

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> S1水合生成4-hydroxy-2-oxopentanoate、S2醛缩裂解生成pyruvate+acetaldehyde在化学上成立且相连；但产品未标(S)立体化学、S1未列H2O、pyruvate被标为main而非byproduct，且缺少S01 acetaldehyde→acetyl-CoA终末转化，故主链不完整。

<details><summary>V0.4理由与本行变化背景</summary>

S1 2-hydroxypenta-2,4-dienoate +H2O→(S)-4-hydroxy-2-oxopentanoate(hydratase)，S2→pyruvate+acetaldehyde(aldolase)，化学转化、方向与碳数守恒成立且与gold主链前两步一致；未列H2O属辅因子/溶剂级局部计量小缺陷(7–8档处理)。缺乙酰CoA末步归D1完整性/范围。7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：supports S03 hydration, S02 aldol cleavage, and S01 terminal oxidation
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：supports enzyme reactions but not D2 chemistry alone

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按C03-C05：S03入口步给出2-hydroxypenta-2,4-dienoate→4-hydroxy-2-oxopentanoate，酶名与EC 4.2.1.80匹配accepted set，可按功能粒度记S（产物立体未标属表示边界，不单独升为功能失败）。S02中间裂解步酶名在accepted set内，但显式EC 4.1.2.43不在accepted EC 4.1.3.39/4.1.3.43内，且无冻结官方EC记录，按PAIR_UNVERIFIED记U，不能记S。S01终端乙酰-CoA步完全未交付；题面/gold终端为acetyl-CoA，答案止于pyruvate/acetaldehyde，属已确认KEY_TERMINAL实证漏交付，适用D-KEY4上限4。可用目标仅入口步清楚，S02待核、S01关键缺失，故在受限&#91;1,4&#93;取3而非默认4。

<details><summary>V0.4理由与本行变化背景</summary>

S1酶2-hydroxypenta-2,4-dienoate hydratase EC 4.2.1.80与gold S03(EC-4.2.1.80)一致；S2酶名4-hydroxy-2-oxovalerate aldolase正确，但EC 4.1.2.43与gold S02登记EC 4.1.3.39/4.1.3.43不符，E0无4.1.2.43冻结记录(GAP-051-004/012)，按四.6无法核验→UNRESOLVED待核、不判错不cap；仅一条EC子项存疑，未推翻主要酶-反应对应。5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：支持本题accepted酶/EC集合：S03含EC 4.2.1.80；S02含EC 4.1.3.39/4.1.3.43；S01含EC 1.2.1.10（另1.1.1.1）。不支持把4.1.2.43列为S02 accepted EC，也不证明具体蛋白实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：支持S03入口底物到4-hydroxy-2-oxopentanoate、S02中间体到acetaldehyde+pyruvate、S01 terminal acetaldehyde+CoA→acetyl-CoA的有向主链事实；不单独核实答案S02的EC配对。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_051：支持本题gold terminal主产物为acetyl-CoA；不证明答案已交付该步。

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> P. putida mt-2/TaxID303身份有E0 BacDive 12880菌株记录及TaxID303支持；organism_gold对S02/S03有P. putida 303 exact记录；两步均归同一菌株符合去重要求。TaxID303为物种级、菌株名mt-2为株级，粒度略有混合；S01未交付不构成对已交付步骤的微生物错配。

<details><summary>V0.4理由与本行变化背景</summary>

两步骤均绑定Pseudomonas putida mt-2(TaxID 303)。E0 taxid:303为P. putida种级记录(学名匹配SUPPORTED)；f3e0:bacdive:12880为mt-2 PaW1(pWWO)株记录(含ATCC 33015)，支持mt-2菌株身份；gold pathway_complete含TaxID 303，且mt-2/pWWO的TOL下路携带xylH/xylI，整条路径能力有据。菌株token未见于种级记录(STRAIN_TOKEN_UNRESOLVED)属粒度备注。7–8档取8。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：supports strain identity and ATCC 33015; not full-path capability
- E0_EVIDENCE / f3e0:taxid:303：supports species name and current TaxID 303; not strain-level taxid exclusivity
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_051：supports P. putida 303 for delivered steps; not S01 delivery

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 多项性状可与trait_gold/E0对上：pH growth约7、ATCC 33015、motility、rod-shaped、Gram-negative、non-sporulating、aromatic hydrocarbon degradation等；F4/F14明确null符合允许未知。F2 optimum 30、F7 toluene/xylenes、F9特定酶活、F15 habitat generality未在冻结性状记录中直接核验，属局部未核/条件解释问题；主要性状可核实，故给7。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状与gold/12880记录大体一致：pH optimum 7.0(gold pH growth 7.0)、mesophilic、Gram-negative、rod-shaped、motile、non-sporulating、ATCC 33015(见12880株记录)、F9列catechol 2,3-dioxygenase/hydratase/aldolase(meta-cleavage)。F4盐度、F14基因组为诚实null(归D1完整性)。部分值(温度optimum 30、F7芳烃、F9酶谱)源自内部知识待独立核验；F15以栖息地列举替代广适性描述略欠规范。7–8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_051：supports pH, motility, morphology, Gram, sporulation, aromatic degradation, etc.; not F2 optimum or toluene/xylene panel
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_051：distinguishes observed-accuracy vs completeness-only subfields
- E0_EVIDENCE / f3e0:bacdive:12880：supports ATCC 33015 and 26/30°C growth records; not optimum

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> evidence_registry三项EVID_001-003全部为INTERNAL_KNOWLEDGE_ONLY，无database、record_id、locator或可定位外部条目；D5按MISSING_SOURCE处理，关键结论几乎无法沿记录追查。未发现已核虚构/错引，故不触发错引cap。

<details><summary>V0.4理由与本行变化背景</summary>

EVID_001–003全部为INTERNAL_KNOWLEDGE_ONLY(database/record_id/locator均为null)，无任何可定位文献/数据库条目或计算记录，按P34属MISSING_SOURCE，D5按低分档评定；无经核实错引(EC 4.1.2.43与gold不符但E0无记录→UNRESOLVED待核，不计已核实关键错误、不cap)。取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案给出confidence字段及F4/F14未知null，显示部分不确定性；但无uncertainties说明，route_summary和多数性状以内部知识作事实性陈述，F7/F9等高置信声称缺少证据类型与限制披露，主要限制未说明。属部分披露但强度超过依据。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties为空数组、无总体不确定性说明；多个仅内部知识的声称(F6/F7/F8/F9/F10/F11/F12/F13及两步酶)标high，证据类型与置信度不相称；但F4盐度、F14基因组诚实置null、温度/pH/保藏标medium，显示部分诚实。属多处过度确信但非全面系统性误导(未掩盖已知矛盾)，5–6档取5，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`ade71964143a84ec258a8b731d40269852f2b5571ca1543747174cd5f970cb80`。

### D1 完整性与任务符合度：10 / SCORED

V0.4旧分9 → V0.5新分10，变化+1。

新裁判理由：

> route_scope.chosen_route_name按题面原样填写，氧条件保持null；steps S1-S3均给出底物/主产物英文名与SMILES、首选酶及EC、对应微生物；organism_profiles按同一物种+菌株去重并返回全部15项性状。必答模块完整，未见指定路线偏离或重要遗漏。

<details><summary>V0.4理由与本行变化背景</summary>

9–10档：路线名逐字回显题面chosen_route_name；3步主链均给出底物/产物英文名与SMILES、首选酶+EC+基因、对应微生物（同一菌去重为ORG_001）；15项性状全部给出并各挂evidence_id；证据登记5条、不确定性3条。仅少量交付层瑕疵（个别无据性状以低置信数值而非null填充，如F3 optimum 7.0），无重要模块遗漏或范围偏离，故取9不在10。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_051：本题为LINEAR_UNIQUE、ordered_step_count=3、n_required=3；答案给出三步主链及完整模块
- ANSWER_TEXT / ade71964143a84ec258a8b731d40269852f2b5571ca1543747174cd5f970cb80：答案原文包含route_scope、三步steps、organism_profiles及15项traits，字段结构完整

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 三步主链方向与化学转化和gold主链一致：S1以4.2.1.80水合，S2以4.1.3.39醛缩裂解生成丙酮酸与乙醛，S3以1.2.1.10在CoA/NAD+参与下将乙醛氧化为乙酰辅酶A，终点为acetyl-CoA，辅因子基本在列。局部问题包括S1/S2中间体未标(S)立体化学、S3未列H+、S2将pyruvate标作main而非byproduct；这些属表示或局部计量层面的少量修订，不改变已交付主链。表示边界按BOUNDARY_REVIEW保留，未将去立体表示当作完全确认。

<details><summary>V0.4理由与本行变化背景</summary>

主链与gold逐步一致：S1为2-羟基戊-2,4-二烯酸水合（对4.2.1.80），S2为4-羟基-2-氧代戊酸醛缩裂解生成丙酮酸+乙醛（对4.1.3.39），S3为乙醛+CoA+NAD+氧化生成乙酰CoA+NADH（对1.2.1.10）；起点等于gold root、终点等于gold terminal(acetyl-CoA)，方向与连接正确，辅因子CoA/NAD+在列，无跳步或方向反转。仅少量局部表达缺陷：产物未写(S)-构型（gold为(S)-4-hydroxy-2-oxopentanoate）、第三步未列H+，属简化/局部计量，按辅因子与简化反应式条款在7–8档外仍属轻微，故9。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;V04_VALUE_OUTSIDE_SUPPLIED_V05_INTERVAL;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：gold主链反应顺序为S03水合、S02醛缩裂解、S01乙醛至acetyl-CoA；answer三步方向与产物连接总体一致，但存在立体/电荷表示边界
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：相应步的accepted EC集合包含4.2.1.80、4.1.3.39、1.2.1.10；answer所用EC与该函数层一致
- ANSWER_TEXT / ade71964143a84ec258a8b731d40269852f2b5571ca1543747174cd5f970cb80：answer的S1-S3化学转化、辅因子与产物连接原文；用于核对局部表示和计量差异

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> All three target reactions match accepted enzyme names and explicit EC values at G4 curation level: S1 MhpD/EC 4.2.1.80, S2 MhpE/EC 4.1.3.39, S3 MhpF/EC 1.2.1.10. The optional mhpD/mhpE/mhpF gene attributions are MINOR unresolved, and representation hold blocks 9-10, so the upper allowed band score is 8.

<details><summary>V0.4理由与本行变化背景</summary>

9–10档：三步酶-反应对应均与gold enzyme_gold一致——4.2.1.80（2-hydroxypentadienoate/2-oxopent-4-enoate hydratase族）、4.1.3.39（4-hydroxy-2-oxovalerate aldolase）、1.2.1.10（acetaldehyde dehydrogenase (acetylating) MhpF）；酶名、EC、反应类型互不矛盾，MhpD/MhpE/MhpF归属与gold metacyc酶标识(MONOMER-354/MHPELY-MONOMER/MHPF-MONOMER系列)方向一致。扣分点：基因名mhpD/mhpE/mhpF与EC官方accepted name/reaction未在E0核验（GAP-051-003/006/008），故不取10。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：Lists accepted enzyme names/EC for the three gold steps, including MhpF/1.2.1.10, MhpE/4.1.3.39 and MhpD/4.2.1.80; supports function-level reaction correspondence, not specific protein activity.

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> Gold organism rows assign Escherichia coli (species taxid 562) to all three corresponding enzyme steps, and the pathway-complete organism list includes E. coli. The answer&#x27;s species-level E. coli assignments are therefore supported. The additional strain K-12 MG1655, TaxID 511145, ATCC 700926 and genome accession are strain-level extras not present in E0; they are unresolved but not contradicted, giving 8 rather than a lower band.

<details><summary>V0.4理由与本行变化背景</summary>

7档（身份阶梯①粒度不足）：三步步级菌均写Escherichia coli K-12 MG1655，而organism_gold对4.2.1.80/4.1.3.39/1.2.1.10三步均列出Escherichia coli(562, EXACT)并给出PATHWAY_COMPLETE(562)=TRUE，故种级身份与整路径能力有真实记录支持，物种选择正确、能力结论不依赖任何错配编号；但声称粒度为菌株级并给出TaxID 511145，冻结证据内无该菌株级记录（GAP-051-025），属物种级记录支持菌株级声称的粒度不足，按①档内扣（通常7档附近）、默认不cap。未发现跨属/无关类群错配，无已核实虚构，故不构成关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_051：Supports E. coli species-level assignment and pathway-complete status for E. coli taxid 562; does not verify strain K-12 MG1655, TaxID 511145, ATCC 700926 or genome accession.

</details>

### D4 性状科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> All 15 traits are present. Species-level gold supports E. coli being facultatively anaerobic, non-halophilic, Gram-negative, rod-shaped, motile, non-sporulating, using glucose, carrying the Mhp enzymes and having the pathway-complete status. Several exact strain-specific values and optima are unverified, but no checked trait is contradicted, so 8.

<details><summary>V0.4理由与本行变化背景</summary>

7–8档偏中：与gold 562物种级代表记录对照，F1兼性厌氧（aerotolerant=true、facultative anaerobe=true）、F4非嗜盐类别（salinity preference=non-halophilic）、F7化能有机异养与葡萄糖利用（chemoheterotrophy=true、fermentation:glucose=true）、F9所列MhpD/MhpE/MhpF活性、F10运动性、F11杆状、F12革兰氏阴性、F13不产芽孢均一致；温度上下限与盐度数值如实留空或低置信，符合诚实null。扣分点：F2最适37°C、F3 pH optimum 7.0、F5 ATCC 700926、F14 NC_000913.3/4,641,652 bp/50.8%、F15栖息地描述所在子字段在冻结证据中无记录或为completeness_only/pending_teacher_adjudication（不得作准确性分母），但以medium/high置信呈现未经核验的菌株级数值，属条件与证据强度不匹配；未发现已核实数值错误或把物种级观测宣称为全物种性质，故不判关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_051：Species-level E. coli trait records support several general traits and enzyme annotations; exact K-12 MG1655 strain values are not all covered.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_051：Shows which trait items have observed accuracy denominators and which are completeness-only or pending; used to avoid treating unverified strain-level exact values as confirmed.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> The answer maps core route/enzyme claims to a named MetaCyc/EcoCyc pathway record, genome claims to NCBI accession NC_000913.3, and some traits to BacDive/ATCC entries; however locators are null and these answer-specific records are not present in E0, so the core sources remain UNRESOLVED rather than verified. F7/F3/F4/F15 rely on INTERNAL_KNOWLEDGE_ONLY. No verified mis-citation or systemic fabrication was established, so no D5 cap applies; partial traceability gives 6.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组(CORE：CG01/CG02/CG03/CG05/CG07；APPLICATION_CRITICAL：CG08/CG17)与支持组均登记了与结论一一对应的claim_scope：路线/酶/菌/基因组/性状各有指向条目（MetaCyc/EcoCyc路线名、RefSeq NC_000913.3、BacDive DSM 18039、ATCC 700926），另有5项性状明确标为INTERNAL_KNOWLEDGE_ONLY，未见编造式DOI或与结论无关的文献列表。但无一决策相关组能在冻结证据中完成“条目级可核对”：E0仅含P. putida 12880与taxid 303两条，EC/TaxID 511145/ATCC/RefSeq/MetaCyc条目均为EVIDENCE_GAP，故相关组统一记UNRESOLVED_SOURCE（低分+待核），不记已核实错引、不cap；因SUPPORTING组与部分CORE组具备可定位标识但无法核对，且内部知识来源比例较高，取5（部分关键结论可定位、核对未完成，其他模块缺映射）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the delivered evidence registry and mappings; does not itself verify the cited database contents.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_051：Confirms the task route identity but not the answer&#x27;s source records or their actual support.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> The answer explicitly notes the null oxygen condition, alternative TOL/P. putida chemistry, missing numeric temperature/pH/salinity bounds, and approximate cofactor SMILES. Confidence labels mostly track evidence strength. Some high-confidence labels for unverified strain/TaxID/ATCC/genome are overconfident but not systemic and do not hide a known contradiction, so 8.

<details><summary>V0.4理由与本行变化背景</summary>

7–8档：不确定性披露具体且不空泛——明确指出题面氧条件为null、指出P. putida mt-2 TOL meta-途径为同源替代但不属评分主链、说明温度上下限/pH/盐度数值缺乏直接来源故填null或低置信、并说明辅因子SMILES为非立体简化；EVID_005以INTERNAL_KNOWLEDGE_ONLY如实标注，未把预测包装成实验观测，也无掩盖已知矛盾。扣分点：F5保藏号、F14基因组数值、F2最适温度等以high/medium置信挂在不可核记录上，属单点过度确信；且未提示“物种级代表记录≠菌株级实测”的粒度边界（F8/F9/F14均以菌株profile呈现）。未达系统性误导，不构成本维cap。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Shows the answer&#x27;s uncertainty statement and confidence labels; does not verify the underlying facts.

</details>

## Qwen

答案SHA256：`0398eb1e123a5d2126e0a48721bf318fedcddf1094a3e12f74638273741ac234`。

### D1 完整性与任务符合度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> JSON完整、route_scope.chosen_route_name与题面一致，两步主链及15项性状字段均已交付；但任务合同要求3步主链并终止于acetyl-CoA，答案漏掉acetaldehyde→acetyl-CoA的末端S01步骤，并在S2 uncertainty中把该下游排除，主链仅2/3，故7而非8-10。

<details><summary>V0.4理由与本行变化背景</summary>

主要模块(路径/酶/微生物/性状/证据/不确定性)均有涉及，chosen_route_name按题面原样填写；主要缺陷是主链仅交付2步，缺gold第三步(乙醛+CoA+NAD+→乙酰CoA, EC 1.2.1.10)，并以&#x27;S2.uncertainty乙醛的后续氧化步骤不属于本题面指定的主链范围&#x27;作未获题面支持的边界声明；15项性状11填4诚实未知。属&#x27;主要模块均有涉及但若干必要内容遗漏&#x27;档(5–6)，问题偏中度故取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_051：冻结formal_cases显示ordered_step_count=3，支持本题必答主链为3步，不支持把2步答案视为完整。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：S01反应及acetyl-CoA终点为任务主链末端；答案未交付该步。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 已交付的hydratase水合步与aldolase醛裂解步方向正确、产物关系与原子计数基本闭合，无明显化学错误；但题面要求的末端acetyl-CoA转化缺失，答案把acetaldehyde下游排除出主链，主链不完整，故落在5-6档而不到7-8档。

<details><summary>V0.4理由与本行变化背景</summary>

已交付两步化学与gold一致：S1 EC 4.2.1.80水合加成H2O，2-hydroxypenta-2,4-dienoate→(4S)-4-hydroxy-2-oxopentanoate(与gold BSY-r03581同向同构型)；S2 EC 4.1.3.39醛裂解，C5→C3丙酮酸+C2乙醛，原子守恒、方向与连接正确。缺陷：未延伸至gold终点乙酰CoA(缺S01步)，把pyruvate标为main(相对主链应为byproduct)，且&#x27;从而进入中心代谢&#x27;对乙醛略过度(乙醛需进一步氧化)。主链关键转化有充分依据、少量局部问题，属7–8档取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：支持S03水合、S02醛裂解及S01乙酰CoA末端的反应方向和参与者；不支持省略S01后仍称完整主链。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：支持对应步骤的酶名/EC类别；不单独证明具体蛋白活性或补足缺失步骤。

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> S03 hydratase（EC 4.2.1.80）与S02 aldolase（EC 4.1.3.39）可由答案名称、反应方向及accepted set功能级条目识别为可用；S01末端acetaldehyde→acetyl-CoA未交付。计数为S=2、M=1、U=0，原覆盖率0.667本落&#91;5,6&#93;，但S01为预定义KEY_TERMINAL缺失，按D-KEY4整维上界4，故取受限档上沿4而非5-6。

<details><summary>V0.4理由与本行变化背景</summary>

两步酶-EC对应均与gold酶表一致：S1 2-hydroxypenta-2,4-dienoate hydratase EC 4.2.1.80(=gold BSY-r03581 2-hydroxypentadienoate hydratase)，S2 4-hydroxy-2-oxovalerate aldolase EC 4.1.3.39(=gold BSY-r03483)，酶名与反应类型匹配、无家族相关性冒充具体催化。E0对两EC无独立冻结记录(GAP-051-007/009)，EC正确性按gold酶表旁证、E0侧保持UNRESOLVED待核，不影响本维整体评分。缺第三步酶属D1完整性而非D3a错误。取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：支持S03 4.2.1.80与S02 4.1.3.39的accepted酶名/EC家族；不支持自动证明具体蛋白活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：支持S03→S02→S01主链及S01为乙酰CoA末端；答案缺失S01。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> Pseudomonas putida mt-2/ATCC 33015的身份由E0菌株记录支持；gold organism对P. putida物种在S02/S03/S01有步级行，支持物种级对应。但答案把mt-2用于步级催化并标complete_pathway_organism_profile_id，而E0菌株记录未直接证明其步级酶活与全路径能力，属粒度不足，故7档而非8-10。

<details><summary>V0.4理由与本行变化背景</summary>

两步微生物均写Pseudomonas putida mt-2，与gold organism_gold两步EXACT的Pseudomonas putida(303)一致；mt-2身份经E0 f3e0:bacdive:12880(mt-2 PaW1, pWWO)与f3e0:taxid:303核实，ATCC 33015亦由此卡支持F5。缺陷：complete_pathway_organism_profile_id=ORG_001把&#x27;整条路径菌&#x27;落到菌株级，而gold pathway_complete证据为物种级(303)→按身份阶梯①粒度不足、档内扣不cap；ncbi_taxid诚实null。取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持P. putida mt-2 PaW1/pWWO菌株记录及ATCC 33015等保藏号，不证明具体步级酶活或全路径能力。
- E0_EVIDENCE / f3e0:taxid:303：支持P. putida物种TaxID身份与学名，不支持菌株级能力外推。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_051：支持P. putida物种在多个步级的EXACT行；同名物种行不等同于mt-2菌株级活性证明。

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> F5 ATCC 33015与E0 mt-2菌株记录吻合；F10运动、F11杆状、F12革兰氏阴性、F13不产孢与P. putida物种gold一致；F9所述hydratase活性也有步级酶记录支撑。F1/F6/F7/F8/F15较宽泛且多为medium内部知识，F2/F3/F4/F14诚实null；未见离谱数值或关键性状错误，但部分物种级/宽泛性状向mt-2菌株外推，故7。

<details><summary>V0.4理由与本行变化背景</summary>

已填11项性状(氧/保藏/呼吸/碳源/降解谱/酶活/运动/形态/革兰/产孢/栖息地)对P. putida物种级基本准确：革兰阴性、杆状、运动、不产孢与gold一致，ATCC 33015经E0核实，芳香烃降解经gold物种级支持；关键定量性状(温度/pH/盐度/基因组)诚实留null。扣分点：全部性状仅引INTERNAL_KNOWLEDGE_ONLY、以medium置信呈现、缺可定位来源，F7/F8较笼统，未标注观测/预测性质。属&#x27;部分性状准确适用但关键项证据不足&#x27;档(5–6)，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持mt-2菌株记录含ATCC 33015与26/30°C培养记录；不证明最适温度或所有性状。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_051：支持P. putida物种的motility、rod-shaped、Gram-negative、non-sporulating等观测；不支持跨菌株定量外推。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_051：提示部分trait子字段仅completeness或待裁定，不应按填满率机械加分。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 答案evidence_registry仅有EVID_001/EVID_002，source_type均为INTERNAL_KNOWLEDGE_ONLY，无database、record_id或可定位外部locator；核心路线/酶/微生物/性状组均为MISSING_SOURCE。E0可核实部分身份/性状事实，但答案未交付这些外部记录；无已核实错引，故低分不cap。

<details><summary>V0.4理由与本行变化背景</summary>

全部关键结论仅由EVID_001/EVID_002(INTERNAL_KNOWLEDGE_ONLY)支撑，无任何可定位外部来源或计算记录→MISSING_SOURCE。按claim group：决策相关组(CG01/02/03/05/07等)全为内部知识、全部缺失→低分档、默认不cap。正向可定位支持：ATCC 33015经E0 f3e0:bacdive:12880核实正确，仅登记事实层、不回填来源状态。无经核实错引，severity=NOT_APPLICABLE。取3(MISSING_SOURCE低档上限，因子claim_scope登记结构尚存)。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案自报来源仅为INTERNAL_KNOWLEDGE_ONLY，不能作为可定位外部文献/数据库记录。
- E0_EVIDENCE / f3e0:bacdive:12880：E0可支持mt-2/ATCC 33015身份，但答案自己未交付该记录；不能回填为答案来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案明确写出氧条件null、未填TaxID/基因组/温度/pH/盐度、基因蛋白未填及可能互变异构，未知项用null/unknown，未把预测系统性写成实验观测；但对P. putida mt-2的宽泛性状与完整路径仍以medium confidence陈述，且把末端下游排除为主链外，边界说明尚不够充分，故7而非8-10。

<details><summary>V0.4理由与本行变化背景</summary>

答案诚实披露：氧条件未指定、TaxID/基因组/温度/pH/盐度缺可靠来源故留null、并列出酮-烯醇互变不确定性；来源自标INTERNAL_KNOWLEDGE_ONLY，未把内部知识伪装成数据库观测。瑕疵：内部知识性状统一标medium置信略偏乐观，&#x27;进入中心代谢/乙醛下游不在主链&#x27;的边界声明偏自信，但属单点、非系统性、无明知掩盖证据。属7–8档取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案列出氧条件、缺失TaxID/基因组/温度/pH/盐度、基因蛋白及互变异构等不确定性，支持D6中上档。
- ANSWER_TEXT / ANSWER.evidence_registry：答案自报来源为内部知识并标medium，未伪装成外部实验观测；但未披露菌株级全路径能力边界。

</details>

## Grok

答案SHA256：`a3dab47316b2bbd62593ced09378eb65799bc0ca27aab4e31a5f628e533caf76`。

### D1 完整性与任务符合度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer supplies the required three-step main route, gives substrate/product names and SMILES for each step, one preferred enzyme/EC and one corresponding microorganism per step, uses one deduplicated P. putida mt-2 profile, returns all 15 trait fields (12 filled, 3 explicit unknown), preserves the exact route name, and keeps oxygen_condition null as in the question. No important task module is omitted; only optional strain-level identifiers and some trait values are null.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_051：Confirms a linear unique three-step gold route and three required steps; does not itself score answer completeness.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_051：Confirms the route, root substrate, and terminal product identity; not a substitute for answer completeness.

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The main chemistry is coherent and follows the degradative direction: hydration of 2-hydroxypenta-2,4-dienoate to 4-hydroxy-2-oxopentanoate, retro-aldol cleavage to acetaldehyde plus pyruvate, and NAD+-dependent acetylating aldehyde dehydrogenase conversion of acetaldehyde to acetyl-CoA. Cofactors/water/NAD+/CoA and byproducts are mostly shown, and the terminal acetyl-CoA matches gold. Local issues remain: exact Z/S stereochemistry and some protonation/charge states are not fully specified in SMILES, and S2 labels pyruvate as a main product whereas gold treats it as a byproduct; these are local representation/role issues, not main-chain breaks.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：Gold reaction rows support the directed hydration, retro-aldol, and acetaldehyde-to-acetyl-CoA transformations and identify the terminal product.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：Gold enzyme rows list the accepted ECs for the three steps; not experimental proof of a specific protein.

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The three target reactions map to accepted function/EC pairs: answer S3 uses acetaldehyde dehydrogenase (acetylating) EC 1.2.1.10 for gold S01; answer S2 uses 4-hydroxy-2-oxovalerate aldolase EC 4.1.3.39 for gold S02; answer S1 uses 2-oxopent-4-enoate hydratase EC 4.2.1.80 for gold S03. S01 is fully confirmed. S02/S03 remain route-hold representation cases because stereo/charge are not automatically bound, but the accepted enzyme names and ECs support function-level correspondence, so they are not treated as wrong. Optional gene annotations xylJ/xylK/xylQ remain minor unverified additional claims. The high-tier 9-10 gate is blocked by the representation hold and the base range &#91;1,8&#93;.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：Lists the accepted enzyme names and ECs for the three gold steps, including EC 4.2.1.80, 4.1.3.39, and 1.2.1.10.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：Supports the reaction direction/connectivity for the three steps; exact stereo/charge is not automatically bound.

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer assigns all three steps to Pseudomonas putida mt-2 and deduplicates it into one profile. E0 BacDive 12880 identifies mt-2 PaW1(pWWO) with NCBI tax id 303; taxid 303 is current and species-level. Gold organism rows include P. putida 303 as an exact step-level organism for S01/S02/S03, and PATHWAY_COMPLETE includes 303 with pathway_complete TRUE. The species-level TaxID for a strain-level claim is a granularity issue, not a contradiction; the strain name and pathway support are present. Minor strain-level genome/collection identifiers are not delivered.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：BacDive record for mt-2 PaW1(pWWO) with NCBI tax id 303 and culture collection numbers; does not by itself prove every enzyme activity.
- E0_EVIDENCE / f3e0:taxid:303：Current taxonomy record for Pseudomonas putida at species level; supports species identity, not a unique strain-level taxid.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_051：Gold organism rows list P. putida 303 for step-level matches and PATHWAY_COMPLETE support.

</details>

### D4 性状科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 trait fields are returned, with 12 filled and 3 explicit unknown. The main trait claims are largely consistent with P. putida/mt-2 and with gold where covered: aerobic, mesophilic, non-halophilic, Gram-negative rod, motile, non-sporulating, TOL-related aromatic degradation, XylJ/XylK/XylQ activities, and habitat generalism with a species-versus-strain caveat. Many values are drawn from a species-level Bergey&#x27;s description rather than strain-specific measurements; F5 and F14 are null despite some E0 strain-level information being available. No gross numeric or identity error is present, and the answer explicitly limits species-level extrapolation.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_051：Gold trait rows support several species-level P. putida traits such as aerotolerance, mesophilic preference, non-halophily, Gram reaction, morphology, motility, and sporulation.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_051：Shows which P. putida trait subfields are observed/scorable and which remain completeness-only; not a direct answer score.
- E0_EVIDENCE / f3e0:bacdive:12880：Strain record provides mt-2 culture collection numbers and limited culture temperatures; does not comprehensively measure all 15 traits.

</details>

### D5 来源与可核查性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The evidence registry maps the route, enzyme/EC, organism, and traits to KEGG entries, two specific literature citations, and a Bergey&#x27;s species description. Key enzyme/EC and TOL biology claims have specific locators; several traits rely on a generic Bergey&#x27;s source, and the KEGG/literature entries are not present in E0 for independent verification. No verified mis-citation is found: unavailable verification is registered as UNRESOLVED/GENERIC/MISSING, not as fabricated. Traceability is good but not complete, so the dimension is in the 7-8 band.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：The delivered registry lists specific KEGG IDs, two full literature citations, and a generic Bergey&#x27;s source; it is evaluated as delivered, not backfilled.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：Gold enzyme rows allow checking the EC/name pairs independently of the answer&#x27;s citations.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_051：Gold organism rows support the P. putida attribution but do not verify the answer&#x27;s literature locators.
- E0_EVIDENCE / f3e0:bacdive:12880：E0 strain record supports identity/limited culture data; it does not verify the answer&#x27;s KEGG or literature citations.

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer clearly separates database/literature claims, model inference, explicit unknowns, and limitations. It notes the enol/keto tautomer issue for the hydratase step, states that SMILES do not encode all stereochemistry, marks missing culture collection/genome/pH values as null/unknown, discloses that several traits are based on species-level descriptions rather than mt-2-specific measurements, and avoids substituting the KT2440 genome for mt-2. There is no systematic prediction-as-observation overclaim or concealed major contradiction.

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：Lists the answer&#x27;s explicit limitations, including tautomer/stereo representation and missing strain-level identifiers.
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_051：Shows which traits are species-level or unknown in the frozen reference, supporting the appropriateness of the answer&#x27;s caveats.

</details>

## GPT5.6

答案SHA256：`06b1f57ece0400ccc54a1b32656fafdf1bd4ac3bcb3752d5b4258d15e8d326d6`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主路线只给2/3步，缺KEY终点S01（acetaldehyde→acetyl-CoA）；15项性状全部null；但格式完整、路线名正确、前两步有底物/产物/酶/菌。D1档3–4，取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_051：gold主链为3步且终点acetyl-CoA；不表示所有旁支都要交付
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_051：3步唯一线性主链；不能把全图材料都当作单答案必答分母

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 前两步水合与醛醇裂解化学上连贯，底物/产物名称基本对应gold S03→S02；但主链止于pyruvate/acetaldehyde，缺少acetaldehyde→acetyl-CoA的KEY终点转化，且S2把pyruvate标main、acetaldehyde标byproduct与gold角色相反。D2档5–6，取6（可用主干成立，关键终点连接缺失）。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：gold S02/S03方向与产物角色；S02中acetaldehyde为MAIN_PRODUCT、pyruvate为BYPRODUCT；S01为独立终点步
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_051：gold终点为acetyl-CoA

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按三个必答目标反应核D3a：S01（BIOPATH150_051__S01__BSY-r01634，KEY_TERMINAL）在答案中无对应步骤，答案止于S2的pyruvate/acetaldehyde，未给出acetaldehyde→acetyl-CoA的酶/EC，属已定位的实证交付缺失M；S02答案给出4-hydroxy-2-oxovalerate aldolase但EC写4.1.3.17，且把pyruvate标main、acetaldehyde标byproduct，程序路线诊断为NONMATCH/ROUTE_BLOCKED_NONMATCH，显式EC配对与目标功能支持均UNRESOLVED，不能当S或F，记U；S03答案S1给2-hydroxypenta-2,4-dienoate hydratase EC 4.2.1.80，EC在accepted集，但产物缺(S)立体/电荷表示待核，程序为ROUTE_HOLD_REPRESENTATION，记U。故N=3,S=0,F=0,M=1,U=2，无确认S；仅存在局部可用信息（hydratase的accepted EC/名称和aldolase名称），但关键终末步缺失使主推荐失效，按C05在&#91;1,2&#93;取2而非1；不取中点上探，不因表示待核转NE。KEY4上界虽适用但当前档已低于4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_051：Gold主链反应：S03为2-hydroxypenta-2,4-dienoate hydratase步骤；S02为4-hydroxy-2-oxovalerate aldolase步骤，acetaldehyde为主要产物、pyruvate为副产物；S01为acetaldehyde至acetyl-CoA的终末步骤。该证据不支持答案止于pyruvate/acetaldehyde。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_051：显示S02 accepted酶名/EC为4-hydroxy-2-oxovalerate aldolase配EC 4.1.3.39或4.1.3.43；S03 accepted为EC 4.2.1.80。答案S02的EC 4.1.3.17不在该accepted集合内，属配对/支持待核，不构成已核名号矛盾。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_051：Gold ordered_step_count=3且LINEAR_UNIQUE；本题必答主链为三步，支持答案两步终止时缺失终末步。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_051：Gold终末主产物为acetyl-CoA；答案停在pyruvate/acetaldehyde，未达到该终末主产物。
- ANSWER_TEXT / ANSWER.steps&#91;0&#93;.enzyme：答案S1使用2-hydroxypenta-2,4-dienoate hydratase EC 4.2.1.80；产物名缺(S)立体化学，符合表示待核而非确认目标信用。
- ANSWER_TEXT / ANSWER.steps&#91;1&#93;.enzyme：答案S2使用4-hydroxy-2-oxovalerate aldolase EC 4.1.3.17，并将pyruvate标main、acetaldehyde标byproduct；其后无acetyl-CoA步骤。

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 两步均指P. putida mt-2；E0 BacDive 12880支持mt-2菌株身份/保藏信息，taxid 303支持种级身份；gold organism表在S02/S03列出P. putida种级对应。菌株级对步反应的催化能力未直接核验，属物种级到菌株级粒度不足，档内扣不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持P. putida mt-2身份/培养记录；不证明整条路径能力
- E0_EVIDENCE / f3e0:taxid:303：支持P. putida种级学名/rank；不核实菌株能力
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_051：gold在S02/S03列出P. putida种级对应；不等于mt-2菌株级实验能力

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 全部15项性状value均为null/unknown，无任何可评分性状值；按全null记MISSING=1，不宣称科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_051：gold有部分性状记录；答案未交付任何性状值
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_051：性状可评分结构；答案全null

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> route/enzyme/organism核心声称仅由EVID_001/EVID_002 INTERNAL_KNOWLEDGE_ONLY承载，无database/record_id/locator；决策相关组均MISSING_SOURCE，无法核到条目。无已核实错引，故不cap；D5档1–2，取2。

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案标注traits unknown、TaxID/保藏/基因组缺失，并区分confidence；但把内部知识路线写成“文献和数据库支持”，且complete_pathway_profile无证据仍标ORG_001，核心结论强度高于证据。属部分披露、局部过度确信，不cap；D6档5–6取6。
