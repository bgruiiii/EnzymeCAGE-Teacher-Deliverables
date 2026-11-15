# BIOPATH150_103：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：2-isopropylphenol degradation

污染物：2-Isopropylphenol；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 45.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 49 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 49.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 47 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 64 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 21 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`aaa4dd83a7163b98940a951a3e2d963540ee9c877a21a91d1f105e024050196e`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 格式与模块交付完整，含7步、酶/菌与15项性状；但主链被替换为侧链羟化/脱烷基+苯酚间位裂解，未按题面锁定的gold主链提交，构成任务路线偏离。按D1任务偏离关键错误封顶，档内取4。

<details><summary>V0.4理由与本行变化背景</summary>

7步主链、逐步主底物/主产物（含SMILES）、逐步首选酶与对应微生物、3条organism_profiles（物种级ORG_001、CF600、mt-2按物种+菌株去重未合并）、每条profile 15项性状外壳齐备；route_scope.chosen_route_name原样回填题面路线名。扣分点：S2酶整体为null（题面允许未知，但属实质缺项）、每条profile的F3/F4/F5/F14/F15共5项为null、来源模块仅自我声明。属&#x27;大部分必要内容完整、关联清楚，仅少量遗漏&#x27;档，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_103：gold主链从2-isopropylphenol经3-isopropylcatechol至2-hydroxy-7-methyl-6-oxo-2,4-octadienoate，终点为(2Z)-2-hydroxypenta-2,4-dienoate与2-methylpropanoate；不支持答案的侧链脱烷基主链作为本题主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：逐反应显示gold必答主链S02→S03→S01及方向；仅作任务路线对照，不把替代化学回填为目标完成。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案自述路线整体连续且主要计量基本成立，后段苯酚→儿茶酚→间位裂解至丙酮酸/乙醛为经典途径；但前两步侧链羟化与叔醇脱烷基缺少直接催化依据，且与gold指定的3-isopropylcatechol主链不同，需实质修订。按D2允许范围取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链计量自洽：S1加单氧（C9H12O→C9H12O2，含O2/NADH与NAD+/H2O）、S2 C-C断裂（C9H12O2→苯酚C6H6O+丙酮C3H6O，原子配平）、S3苯酚邻位羟化、S4间位裂解、S5水解（C6H6O4+H2O→C5H6O3+HCOOH）、S6水合、S7醛缩裂解（C5H8O4→丙酮酸C3H4O3+乙醛C2H4O）均无原子不守恒；S3–S7是教科书苯酚间位裂解链。但入口两段为推定：S1苄位羟化酶EC仅1.14.13.-并自注低置信，S2脱烷基酶整体未知；且主链取向与gold记录的环羟化路线（2-isopropylphenol→3-isopropylcatechol→开环→2-methylpropanoate）完全不同。答案在route_scope.notes与alternative_branches中明确声明该差异并把文献路线标为is_part_of_scored_main_route=false，故按四.5第2–3步：已声明但无可核证据→按未证实登记，不自动判错、也不给高分。5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：gold显示本题指定主链为S02→S03→S01及相应底物/产物方向；不把答案的侧链脱烷基化学自动判错，但答案化学需按自身连续性单独评。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分6 → V0.5新分1，变化-5。

新裁判理由：

> D3a只计目标反应。三个必答目标步均无S：S01为未确认/漏配，S02与S03为已确认KEY目标失败；答案的侧链羟化与苯酚间位裂解不能产生目标步信用。按D-KEY4硬上限及目标对应几乎全失，取1；不另签D3a酶学key_error。

<details><summary>V0.4理由与本行变化背景</summary>

酶名–EC–反应类型内部一致：S3酚2-单加氧酶/1.14.13.7（羟化单加氧）、S4儿茶酚2,3-双加氧酶/1.13.11.2（双加氧开环）、S5水解酶/3.7.1.9（C-C水解）、S6水合酶/4.2.1.80（水合）、S7醛缩酶/4.1.2.39（醛缩裂解），未见&#x27;加氧酶配脱氢酶号&#x27;类互斥；S1以1.14.13.-家族级通配并自注低置信、S2酶整体null属诚实未知。但全部EC在冻结证据中无条目（GAP-103-003/004/006/008/009/013），答案亦自注&#x27;未能逐字核对&#x27;，无任何已核支持。属&#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：gold必答目标步为S02 2-isopropylphenol→3-isopropylcatechol、S03→2-hydroxy-7-methyl-6-oxo-2,4-octadienoate、S01→末端二产物；不支持答案的侧链脱烷基/苯酚间位裂解作为目标步。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_103：accepted目标酶集合只证明这些数据库策展酶名/EC对应gold目标反应，不证明答案中推断酶或替代路线酶对应目标步。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> P. putida为合理候选，CF600的dmp与mt-2的xyl体系用于苯酚/儿茶酚间位裂解属经典对应；但CF600、mt-2均只给TaxID 303种级，缺菌株级身份核验，且无直接证据证明这些菌株经该路线降解2-isopropylphenol。按合理候选+若干关键粒度未核验取6。

<details><summary>V0.4理由与本行变化背景</summary>

三步均推荐Pseudomonas putida：物种名与TaxID 303的物种级名称关联经E0(f3e0:taxid:303, record_status=CURRENT)SUPPORTED；但CF600、mt-2属菌株级声称，E0记为STRAIN_TOKEN_NOT_IN_RECORD_NAMES→UNRESOLVED，答案亦未给菌株级编号（step.microorganism.ncbi_taxid为null，仅在profile层挂303），属D3b身份阶梯①&#x27;物种级记录支持菌株级声称&#x27;——粒度不足，档内扣分、默认不cap。步级能力（dmp操纵子/xyl基因）在2-异丙基苯酚语境无直接证据，但答案在S4 uncertainty中明确披露、且未作整条路径菌声称（complete_pathway_organism_profile_id=null），避免了&#x27;由基因存在外推全路径&#x27;。5–6档取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_103：gold列出本题步骤相关菌株与TaxID；P. putida 303可在部分步骤出现，但不支持将种级TaxID自动绑定为CF600或mt-2菌株级能力。
- E0_EVIDENCE / f3e0:taxid:303：官方TaxID 303为Pseudomonas putida种级记录；只支持种名，不核实CF600/mt-2菌株身份或其降解能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 15项均出现，未知项多以null如实保留；P. putida的革兰氏阴性、杆状、运动、不产孢、好氧呼吸等种级性状大体合理，部分碳源/降解能力与CF600、mt-2经典体系相符。但多个关键数值性状缺失，且把种级一般性状用于菌株profile，ORG_001对2-isopropylphenol利用/脱烷基能力的性状声称缺少对应证据。取6。

<details><summary>V0.4理由与本行变化背景</summary>

15项外壳齐备，但全部数值型性状留空：三份profile的F2(min/opt/max=null)、F3=null、F4=null、F14=null、F15=null；而gold对P. putida(303)有可核观测（pH min 5/max 8、盐度min 0、基因组登录号GCA_024508115.1等），故为完整性缺口（主归D1）而非可核错误。已填项F1&#x27;专性好氧&#x27;、F6&#x27;好氧呼吸/O2&#x27;、F10运动性、F11杆状、F12革兰氏阴性、F13不产芽孢方向与gold观测一致，但来源为属级内部常识（EVID_011，low/medium），未冒充菌株级定量观测。关键缺陷：ORG_001的F7/F8/F9把&#x27;2-异丙基苯酚苄位羟化-脱烷基&#x27;写成种级碳源/降解能力与酶活，承担目标污染物能力论证却无条目级证据（属未核实能力外推）；ORG_003的F8以high标注内部知识。属&#x27;部分性状准确且适用，但关键项证据不足&#x27;，5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_103：gold提供P. putida等性状观测/预测记录；支持部分种级性状，但不把种级记录自动外推到所有菌株，也未支持2-isopropylphenol作为P. putida通用碳源。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_103：标明哪些性状子字段可评分及仅作完整性；未知/缺失不等于错误。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry的EVID_001–EVID_011全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator为空，无法沿外部条目核对路径、酶、菌或性状结论；虽内部证据ID与claim_scope有映射，仍属MISSING_SOURCE低档。

<details><summary>V0.4理由与本行变化背景</summary>

11条evidence_registry全部为source_type=INTERNAL_KNOWLEDGE_ONLY（database/record_id/locator全null），无任何DOI、数据库条目或计算记录；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08）无可定位可核对结论→MISSING_SOURCE。按四.3/P41：决策相关组全部缺失→低分档、默认不触发cap。因连&#x27;笼统库名/模型名/文献列表&#x27;也未给（低于GENERIC_SOURCE的3–4档），落1–2档；仍保留逐claim claim_scope与局部编号使结论–声明对应可读，档内取上限2。无已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / aaa4dd83a7163b98940a951a3e2d963540ee9c877a21a91d1f105e024050196e：答案实际交付的证据登记仅内部知识，无可定位外部来源；不能作为可核对文献/数据库条目使用。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分6 → V0.5新分8，变化+2。

新裁判理由：

> 答案区分了已知、推断与未知：S2酶明确null，S1低置信，S4–S7说明来自经典体系且直接归属未逐字核实，alternative_branches明确不属评分主链，未知性状保留null。主要限制披露较好；扣分点是部分内部知识反应仍标high，且种级性状用于菌株profile时边界说明不足。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且多处：S1自述EC只能归1.14.13.-、菌仅种级；S2酶未知整体null；S4–S7自述EC按经典归类、未逐字核对；uncertainties列出4条并有route_scope.notes说明氧条件未指定而按好氧假设；alternative_branches逐条标is_part_of_scored_main_route=false；未知项统一null未编造数值。扣分点：EVID_003–EVID_007、EVID_010及S3/S4的enzyme.confidence=high、ORG_003 F8=high，而来源全部为内部知识、零外部定位、S3.uncertainty为null，属对未核实内容的单点至多点过度确信（非系统性把预测写成实证、亦无明知掩盖矛盾），故不cap，5–6档取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / aaa4dd83a7163b98940a951a3e2d963540ee9c877a21a91d1f105e024050196e：答案自身对证据性质、置信度、未知与替代分支的披露；不核验其科学真假。

</details>

## DeepSeek

答案SHA256：`591b40049585be76309a3aab1b01b8b65696972780390a210f3e561816af7033`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> JSON结构完整，route_scope.chosen_route_name与题面一致；主路径给出S1-S5的底物/产物/酶/微生物，ORG_001及15项性状字段均出现。但15项性状全部为null且无性状来源，S3酶EC为null，证据仅INTERNAL_KNOWLEDGE_ONLY；属于主要模块均有涉及但性状实质内容仅占位、若干必要内容遗漏，D1不能进入良好档。

<details><summary>V0.4理由与本行变化背景</summary>

路线、酶、微生物三模块均有实质交付：5步逐一给出底物/产物英文名与SMILES、首选酶（S3仅EC为null，题面允许未知填null）、对应微生物，chosen_route_name原样回填题面路线名，同物种同株已去重为单一profile。但性状模块15项全部value=null（filled=0、explicit_unknown=15），属占位性交付；来源与生成记录仅有1条INTERNAL_KNOWLEDGE_ONLY自我声明。落在5–6档（主要模块均涉及，但必要内容遗漏或仅占位）；因性状模块完全未实质交付、来源模块基本缺失，档内取低分5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_103：本题为3个必答主链步、LINEAR_UNIQUE；用于核对主链规模，不证明答案额外下游步骤必需。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_103：题面路线名为2-isopropylphenol degradation，gold终端主产物为2-Methylpropanoate与(2Z)-2-hydroxypenta-2,4-dienoate；不覆盖所有下游延伸。

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> S1-S3的有机主转化与gold主链对应：2-isopropylphenol→3-isopropylcatechol、3-isopropylcatechol→2-hydroxy-6-oxo-7-methylocta-2,4-dienoate、再水解为2-hydroxypenta-2,4-dienoate与isobutyrate；S4-S5继续水合/醛裂解至pyruvate与acetaldehyde，步骤连续且计量可成立。主要有机转化正确，未见已核实主链化学方向/守恒/连接关键错误；O2、NADH、H2O、H+等辅因子缺失属局部计量缺陷，按P103不自动cap。D2当前程序上限为8，九至十分门不满足。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3与gold三步主链化学逐步一致：2-isopropylphenol→3-isopropylcatechol（邻位羟基化，产物SMILES与gold同一化合物）；3-isopropylcatechol→2-hydroxy-7-methyl-6-oxo-2,4-octadienoate（间位开环，产物名仅取代基排序非字母序、SMILES与gold一致）；该二烯酸→2-hydroxypenta-2,4-dienoate + isobutyrate（水解，与gold终点的(2Z)-2-hydroxypenta-2,4-dienoate + 2-methylpropanoate对应）。S4水合、S5醛缩裂解至pyruvate/acetaldehyde属gold终点之外的下游延续，不计入覆盖率、不额外加分，其碳/氢/氧计量自洽。扣分：首步与S2的O2/NADH等辅因子未标注（局部计量缺陷）；立体与质子化态标注简化。属7–8档上部，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：S02/S03/S01三步的主底物/主产物、方向和末端产物；支持前三步有机转化，不覆盖答案额外S4/S5。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_103：gold终端主产物2-Methylpropanoate与(2Z)-2-hydroxypenta-2,4-dienoate；不证明丙酮酸/乙醛下游为必需。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 三个目标反应均有交付，但没有一个目标酶对应达到S。S1对应gold S02：答案EC 1.14.13.7不在accepted集合（1.14.13.44/1.14.13）内，记录为UNRESOLVED_NONACCEPTED，不是已证F。S2对应gold S03：表示边界挂起，five_state=UNRESOLVED；答案EC 1.13.11.2也不在accepted集合（1.13.11.14/1.13.11.39/1.13.11.M5）。S3对应gold S01：表示边界挂起，且水解酶未给EC，不能与accepted 3.7.1/3.7.1.8配对确认。故只有少量可辨认目标酶候选，关键边界仍不清楚，不足以进入5-6档。

<details><summary>V0.4理由与本行变化背景</summary>

五步酶名与反应类型内部自洽：单加氧酶（羟化）、双加氧酶（开环）、水解酶、水合酶（4.2.1.80）、醛缩酶（4.1.3.39），未见&#x27;名称为水解酶而编号为脱氢酶&#x27;类自相矛盾。但关键步骤对应仍缺具体核验且与gold具体酶不同：首步用 phenol 2-monooxygenase EC 1.14.13.7（gold该步为2-hydroxybiphenyl-3-monooxygenase EC 1.14.13.44）；S2用通用 catechol 2,3-dioxygenase EC 1.13.11.2（gold为2,3-dihydroxy-p-cumate 3,4-dioxygenase EC 1.13.11.14/M5）；S3水解酶EC为null。上述EC在冻结证据中均无记录（GAP-103-002/005/010/012），核验状态UNRESOLVED，未核不判错。属&#x27;有合理候选和部分支持、若干关键步骤仍缺具体核验&#x27;的5–6档，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_103：S01/S02/S03的accepted酶名/EC集合；S02 accepted不含1.14.13.7，S03 accepted不含1.13.11.2，S01 accepted含3.7.1/3.7.1.8但答案未给EC。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：目标反应方向与产物；支持目标反应存在，但不证明答案所选具体酶/EC。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> P. putida/TaxID 303的物种身份由E0官方记录支持；gold organism行对S01/S03的部分accepted酶列出P. putida，但入口S02仅列P. nitroreducens，且答案未给菌株。属于合理候选和部分支持、关键入口步骤作用范围未充分核验，落5-6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份可核：Pseudomonas putida + ncbi_taxid 303 经f3e0:taxid:303官方记录核实（学名匹配、状态CURRENT），strain为null，未做菌株级身份声称，无跨属/异菌株错配。步级归属部分支持：gold对该路径的步级记录显示P. putida出现在水解酶步（BSY-e01319 HOMODA hydrolase）与2,3-dihydroxy-p-cumate 3,4-dioxygenase步（BSY-e00250/BSY-e02681），而首步羟基化gold仅列P. nitroreducens；答案将全部5步（含gold终点外的S4/S5）统一归属单一无株号P. putida，作用范围与步级证据尚不匹配。未声称整条路径能力（complete_pathway_organism_profile_id=null），避免单步支持冒充全路径。属&#x27;有合理候选和部分支持、作用范围未充分核验&#x27;的5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：支持Pseudomonas putida与TaxID 303的官方物种名关联；不支持菌株级身份或任何单步/整链能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_103：gold按步列出部分P. putida关联；入口S02未见P. putida，整链能力菌为P. nitroreducens；不自动支持答案具体酶。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 答案15项性状全部为value=null、confidence=unknown，未交付任何可评性状值或来源；按P44/P112，D4记MISSING=1，不宣称检测到具体科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

题目要求每个organism_profile一次返回全部15项性状（含数值、单位、条件与最强来源）；答案organism_profiles&#91;0&#93;.traits的F1–F15全部为value=null、raw_text=null、evidence_id=null、confidence=unknown，即该模块确未交付实质内容。按四.4，全部必需性状为null按MISSING记1分，不宣称检测到科学错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：确认15项性状均为空值；不提供可评数值、单位或条件。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 答案仅登记EVID_001 source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null；路径、酶、微生物均无外部可定位来源。虽TaxID 303可核物种名，但不构成步级来源交付。无已核实错引，不cap，D5落1。

<details><summary>V0.4理由与本行变化背景</summary>

答案证据注册仅1条EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY（database/record_id/locator全为null，claim_scope=pathway/enzyme/microorganism），按四.3属MISSING_SOURCE；全部claim组（含决策相关组CG01/CG02/CG03/CG05/CG07/CG08/CG09）无任何可定位文献、数据库条目或计算记录，D5主要结论（可追查性）完全不可追查。无已核实错引（几乎不存在可核对的引用），故不触发cap；亦无条目级可定位结论可支撑5–6档。落在低分档，取2（因答案如实自标为内部知识、未伪造编号或条目，registry结构与置信度标注完整）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：确认来源交付仅为内部知识登记，无外部数据库条目或文献定位。
- E0_EVIDENCE / f3e0:taxid:303：可核TaxID 303的物种名，但该记录不是答案原交付来源，且不支持步级能力。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案明确把证据性质标为INTERNAL_KNOWLEDGE_ONLY、低置信，逐项列出“基于一般知识推断”、水解酶EC未知、15项性状null；未把预测伪装成观测，也未系统性掩盖未知。按7-8档，给8。

<details><summary>V0.4理由与本行变化背景</summary>

答案对证据性质表述诚实：每步uncertainty明示&#x27;具体酶和菌株未在题面指定；基于一般芳烃降解知识推断&#x27;，全部enzyme/microorganism confidence为low、性状为unknown，evidence_registry自标INTERNAL_KNOWLEDGE_ONLY+low，uncertainties另列水解酶EC未知，未把推断写成实证观测，也未标high confidence。扣分：披露较笼统，未讨论替代酶/替代菌的选择不确定性，也未把&#x27;5步同一物种、无株号&#x27;的作用范围限定与证据粒度对齐；属8档（大部分证据性质标注正确、主要限制已说明，仍有局部粒度不足），不构成系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案对未知、推断与低置信的明确标注；不证明其科学正确性。

</details>

## Kimi

答案SHA256：`46f74a9cda0d714106c4952af92531b8dcb4ff96110306cbfe5a68c9328a1df4`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> 出口结构、逐步酶/EC、对应菌、两个organism_profiles各15项性状、evidence_registry和uncertainties均已交付，模块覆盖较完整；但程序路线诊断为DEVIATES，路线相对本题冻结3步主链发生偏离并额外延伸到下游，D1按任务偏离受限在&#91;1,4&#93;内取4。

<details><summary>V0.4理由与本行变化背景</summary>

模板要求的模块均有实质交付：五步主链（每步含底物/产物英文名与SMILES、一个首选酶+EC、一个对应菌）、按物种+菌株去重的两个profile（ORG_001/ORG_002 各被引用且只出现一次）、每profile完整15项性状骨架、4条证据登记与5条不确定性说明；route_scope.chosen_route_name逐字回显题面路线名、氧条件按题面保留null并加注说明，未改选路线。扣分来自完成度而非错误：两profile各仅5/15项性状有值，其余10项以null+confidence=unknown明示未知（P15/P45：明确未知计入完成度不足，不与遗漏或错误等同），且温度/pH/盐度/保藏号/基因组等关键性状全部未填。按7–8档（大部分必要内容完整、关联清楚，少量遗漏）取低分7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv：Shows BIOPATH150_103 is LINEAR_UNIQUE with ordered_step_count=3; does not by itself require every downstream branch.
- GOLD_SLICE / reaction_gold.tsv：Shows the required directed gold main-chain steps S02-&gt;S03-&gt;S01; used for route comparison only.

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 主链化学总体连续：酚羟化、3-异丙基儿茶酚meta开环、水解、下游水合与醛醇裂解，方向为底物到产物，O2/H2O有列明；但S2/S3关键中间体存在程序标出的立体/表示冲突，S3产物取2-oxopent-4-enoate与gold HODA端点不完全一致，且氧化还原载体/质子有省略，按&#91;1,5&#93;上限取5。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学与gold逐步对齐：S1 2-isopropylphenol 邻位羟化→3-isopropylcatechol（SMILES CC(C)c1cccc(O)c1O，与gold 3-Isopropylcatechol同一结构）；S2 外二醇开环→2-hydroxy-7-methyl-6-oxo-2,4-octadienoate（与gold BSY-c16555同化合物，仅命名词序不同）；S3 水解开环产物→2-methylpropanoate + 2-oxopent-4-enoate（后者即gold终端(2Z)-2-hydroxypenta-2,4-dienoate的酮式写法，碳数9=5+4守恒）。S4–S5（水合→醛缩，pyruvate+acetaldehyde）位于gold终点下游，题面只给路线名而未指定终端化合物，按P29/P153既不加分也不作覆盖率扣分；其化学为标准meta-cleavage lower pathway，方向与连接无误。扣分点仅为局部计量/辅因子缺陷：S1未列NAD(P)H与相应氧化产物、S2未列H+（答案uncertainties&#91;3&#93;已自行声明），按P103属7–8档局部缺陷，不cap。取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv：Gold directed structures for S02/S03/S01 and terminal products; used to judge answer main-chain chemistry, not to demand extra downstream coverage.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> D-KEY4受限&#91;1,4&#93;：本任务N=3，S=0、F=2、U=1、H=0、M=0；S01端点步与S03中间步为已确认KEY目标失败，S02入口底物/产物方向匹配但酶对EC 1.14.13.7相对accepted 1.14.13.44/1.14.13仍PAIR_UNVERIFIED。无任何已确认目标S，两个KEY失败严重损害主功能，入口骨架仅局部可用，故取3。

<details><summary>V0.4理由与本行变化背景</summary>

酶-反应类型在类别层面自洽：S1单加氧酶(EC 1.14.13.7)对应芳香邻位羟化；S2外二醇双加氧酶(1.13.11.2)对应间位开环；S3 C–C水解酶(3.7.1.9)对应水解开环产物；S4水合酶(4.2.1.80/dmpD)与S5醛缩酶(4.1.3.39/dmpE)与CF600 dmp lower pathway的通行酶学一致；S1–S3的gene_or_protein如实留null，未把家族相关性冒充具体催化证据。但S1–S3的具体酶身份/EC在E0中无任何冻结记录（GAP-103-003/006/007），S3所选EC 3.7.1.9（2-hydroxymuconate-semialdehyde hydrolase，作用于2-hydroxymuconate semialdehyde）是否适用于本步底物未能核实；S4–S5的EC同样无E0记录。按四.6与P66：无法核验→UNRESOLVED，保留待核标记、不判关键错误、不cap。定档5–6（合理候选+部分支持，若干关键步骤缺具体核验），取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：Accepted enzyme name/EC sets for S01/S02/S03; does not by itself certify answer&#x27;s nonaccepted alternatives.
- GOLD_SLICE / reaction_gold.tsv：Expected directed substrate/product structures for S01/S02/S03; supports KEY target mismatch identification, not chemical impossibility beyond the mapped reaction.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> P. putida taxid 303可支持物种名，但冻结E0没有KL1菌株关联；CF600的dmpD/dmpE来源只在答案自报文献中，E0无对应记录。答案诚实区分KL1与CF600、不声称单一完整途径菌，但多个步骤的菌株身份和反应级/整路能力仍待核，按5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

P. putida (TaxID 303) 的物种级学名与官方记录精确一致（F3R1CLM-004335 SUPPORTED），但菌株令牌KL1不在记录names中（F3R1CLM-004431 UNRESOLVED），属D3b身份阶梯①粒度不足，档内扣、默认不cap；KL1承担S1–S3的步级催化/降解能力声称无任何冻结反应级证据（CG08整组UNRESOLVED），只能算合理候选；S4–S5换用Pseudomonas sp. CF600并把dmpD/dmpE归入其dmp lower pathway，有可定位文献线索但E0未核（GAP-103-032）。答案未把单步支持写成整条路径能力：complete_pathway_organism_profile_id=null，route_summary与uncertainties&#91;2&#93;主动声明前段KL1与后段CF600不是同一完整途径菌，避免了&#x27;由基因组存在某酶直接推断完成整条路径&#x27;与&#x27;整条路径单菌&#x27;两类外推。非跨属/无关类群错配，不触发cap。定档5–6，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv：Gold organism mappings for required steps include P. putida taxid 303 and P. nitroreducens 46680; supports accepted organism context, not exhaustiveness.
- E0_EVIDENCE / f3e0:taxid:303：Official species-level P. putida name/rank only; does not verify strain KL1 or its reaction capability.
- E0_EVIDENCE / f3e0:bacdive:12880：Strain record for P. putida mt-2 PaW1/pWWO, not KL1; cannot support KL1 strain-level traits or capability.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> CF600的F7/F8/F9有较具体文献原语，P. putida KL1的F1/F6/F7/F8/F9多为物种级或推断性，尤其“2-isopropylphenol为唯一碳源”未在冻结证据中核实；大量null为诚实未知，主要按D1完成度处理，不在D4重复重罚。已给关键性状部分可用但证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

按任务用途，关键性状是&#x27;该菌能否在给定条件下以2-isopropylphenol为碳源/降解&#x27;。ORG_002(CF600) 的F7&#x27;phenol and 3,4-dimethylphenol&#x27;（附raw_text）、F8&#x27;dmp meta-cleavage&#x27;、F9&#x27;DmpD/DmpE&#x27;与dmp途径已知功能方向一致；ORG_001(KL1) 的F1/F6/F7/F8/F9为物种级合理值，但&#x27;唯一碳源和能源&#x27;这一目标关键项只有一条检索式来源(EVID_002)，核不到条目。两profile各10/15项为null（明示未知、confidence=unknown，属完成度问题已在D1计，此处不重复重扣）；温度项未把培养温度当最适值（均null），盐度/耐受未把物种级观测写成菌株级上下限。按5–6档（部分性状准确且适用、关键项证据不足）取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv：Species-level trait rows for P. putida taxid 303 and others; do not validate KL1 strain-specific claims or CF600 traits.
- GOLD_SLICE / trait_scoreability_mask.tsv：Marks which trait fields have observed scoreable values; used to avoid treating nulls as scientific errors.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> EVID_004给出具体期刊卷页，EVID_001/003给出数据库/EC名单但无稳定record_id，EVID_002只是检索式而非具体文章；路线、酶、菌株等决策相关结论仅部分可定位核对，且多处E0无记录不能升级为已核实。无已核实错引，按5–6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记后看决策相关组：路线组（CG01/CG02）只有&#x27;EAWAG-BBD pathway map&#x27;标题而无条目ID（EVID_001）；KL1侧的唯一来源是一条检索式字符串（EVID_002 &#x27;bibliographic search: …&#x27;），不构成可定位引用；酶组（CG05）只列EC号清单（EVID_003），属命名层材料而非反应级条目；步级归属（CG08）亦无条目级证据。同时存在条目级可定位材料——TaxID 303可直接核到物种学名、CF600一条完整文献引文（期刊/卷/页/年齐备）、EC号本身可作条目键——因此不落&#x27;决策相关组全部笼统&#x27;的3–4档，而落5–6档（部分关键结论可定位、其他模块仍缺映射）。E0对这些内容无冻结记录，一律UNRESOLVED，未出现经核实的错引，故不判虚构、不判CONTRADICTED、不触发cap。档内取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 46f74a9cda0d714106c4952af92531b8dcb4ff96110306cbfe5a68c9328a1df4：Answer-delivered evidence_registry entries EVID_001-EVID_004; used only to assess traceability, not to verify their content.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案对氧条件null、KL1/CF600非同一完整途径菌、基因/保藏/基因组未知、辅因子省略、下游接口等均有明确说明；null与confidence多按证据强度区分。个别medium/high标签仍偏宽，但未见系统性把预测写成实证或掩盖主要矛盾，取8。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据相称：uncertainties&#91;0..4&#93;分别交代氧条件按题面保留null、KL1前段酶/基因未能由单一可核记录确定、S4–S5换菌导致主链非同一株贯穿、除O2/H2O外还原剂与辅酶未列入、KL1与CF600保藏号/基因组/培养性状无可核来源；steps逐条uncertainty标注辅因子缺项与支链边界；downstream_continuation明确标注下游不属于评分主链；大量字段以null+confidence=unknown如实留空，未把预测写成观测。扣分点：KL1的F7/F8以medium置信呈现且未标注该来源仅为检索式（单点不够透明），属单点过度确信而非系统性误导，档内扣分；D5已核实错引不存在，故不联动。按7–8档取8。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 46f74a9cda0d714106c4952af92531b8dcb4ff96110306cbfe5a68c9328a1df4：Answer&#x27;s uncertainty/null disclosures and confidence labels; used for evidence-boundary quality only.

</details>

## Qwen

答案SHA256：`f5f28d914a4b5a68a2f147847e26e81fe261cd40ff43761435aa0465e72a1d1f`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> Structured delivery covers steps, enzymes, microorganism, and traits, but the main route is an alternative ipso-dealkylation/catechol route rather than the route-locked gold main chain. Program route diagnosis is DEVIATES; task conformance status is only OK for the chosen route name. D1 task-compliance key failure caps the dimension at 4.

<details><summary>V0.4理由与本行变化背景</summary>

结构层面交付较完整：3步均含主底物/主产物英文名与SMILES、每步一个酶与一个对应微生物，organism_profiles按物种去重为单条ORG_001并由step.microorganism.organism_profile_id引用，15项性状全部返回（12有值+3诚实null），route_scope.chosen_route_name原样填写&quot;2-isopropylphenol degradation&quot;，符合题面不得改选路线的要求。扣分点：题面要求每项性状给出&quot;最强来源&quot;，实际所有事实仅挂INTELLIGEN...（INTERNAL_KNOWLEDGE_ONLY）自建条目，无任何外部可定位来源；首步酶无EC（题面允许未知填null，故不构成编造）；未声明与参考路线的关系边界。落7档（大部分必要内容完整，少量遗漏/证据字段薄弱），档内取7不取8，因来源字段整体未满足题面要求。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：Fixes the required route and terminal chemistry; does not support the answer&#x27;s alternative ipso-dealkylation to catechol/acetone.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_103：Shows the gold terminal products; not the answer&#x27;s muconolactone endpoint.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> The answer&#x27;s alternative route is internally coherent and stoichiometrically plausible for the catechol ortho-cleavage/muconolactone segment, but the key entry transformation to catechol plus acetone is not the gold transformation and lacks direct enzyme support. Main chain partly成立 but the key entry step requires revision/evidence; D2 range is limited to &#91;1,6&#93;.

<details><summary>V0.4理由与本行变化背景</summary>

已交付三步主链在字面计量与方向上自洽：(1) 2-isopropylphenol+O2→catechol+acetone（C9H12O+O2→C6H6O2+C3H6O，碳氢氧化数两侧一致）；(2) catechol+O2→cis,cis-muconic acid（邻位开环，加双氧，合理）；(3) cis,cis-muconic acid→muconolactone（异构化内酯化，分子式不变）。但首步ipso-羟化脱异丙基是与冻结gold不同的替代入口（gold为甲基单加氧→3-异opropylcatechol→间位开环裂解产物→2-甲基丙酸+2-羟基戊-2,4-二烯酸），答案虽在uncertainty中声明证据有限并提示可能存在3-异丙基邻苯二酚支路，却未提供任何可核证据，按四.5第3步&quot;无证据→按未证实登记，不自动判错也不给高分&quot;处理；末段β-酮己二酸仅文字概述未逐项展开（题面未指定终点，不计覆盖率扣分）。落5–6档（主干部分成立、关键连接合理性证据有限），档内取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：Shows the required chemistry for comparison; D2 is assessed independently for the answer&#x27;s chemical plausibility.

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> No target enzyme step earns target credit. S02 and S03 are confirmed KEY target failures: the answer&#x27;s S02 reaction to catechol/acetone is not the target entry, and S03 uses catechol 1,2-dioxygenase on a different substrate rather than the target 3-isopropylcatechol ring-cleavage enzyme. S01 alignment remains unresolved. Error-route enzyme self-consistency does not earn target credit. Confirmed KEY failures trigger D-KEY4 cap &lt;=4; within &#91;1,4&#93;, near-zero target catalysis supports score 1.

<details><summary>V0.4理由与本行变化背景</summary>

S2给出的catechol 1,2-dioxygenase/EC 1.13.11.1与S3的muconate cycloisomerase/EC 5.3.3.4在其自身路线内酶名-EC-反应类型自洽（双加氧开环、环异构化内酯化），属合理候选；但E0冻结快照对EC 1.13.11.1与EC 5.3.3.4均无记录（item_gaps GAP-103-001/014/015/030），按四.6一律UNRESOLVED待核，不能据记忆放行；S1酶名&quot;2-isopropylphenol 2-monooxygenase&quot;非accepted name、EC为null、无基因/蛋白标识，该关键起始步的酶-反应对应完全无可核依据。综合落5–6档（有合理候选与部分支持、关键步骤仍缺具体核验），档内取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_103：Shows target accepted enzyme classes; does not support the answer&#x27;s catechol/muconate route enzymes as target steps.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：Shows target substrate/product pairs; does not support catechol plus acetone or catechol ortho-cleavage as the target entry/midroute steps.

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> TaxID 303 and the name Pseudomonas putida are a valid species-level identity match. However the answer assigns all three steps to P. putida without strain-level or step-specific capability evidence; the first-step enzyme attribution is unsupported, and the gold S02 organism set does not include P. putida. Reasonable candidate and identity are supported, but key step-level scope remains unverified; no D3b key error.

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份层：答案给的Pseudomonas putida与ncbi_taxid=303经E0 f3e0:taxid:303核实为官方学名匹配（SUPPORTED），strain=null未越级声称菌株，也未声称单一菌完成整条路径（complete_pathway_organism_profile_id=null），故不触发身份错配或&quot;单步菌写成全路径菌&quot;；但三步（含起始ipso羟化）全部归同一物种属步级催化归属声称，E0对该归属仅给出UNRESOLVED（F3R1CLM-003996，L2/L3语义未核），答案亦无反应级或全路径能力证据，属八.D3b阶梯①粒度不足+能力未核：档内扣分、默认不cap；且gold步级菌多为Pseudomonas nitroreducens/Paraburkholderia xenovorans（P. putida仅出现在2,3-dihydroxy-p-cumate 3,4-dioxygenase行），答案选择非gold主用菌但未被证伪。落5–6档，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：Supports official species identity for TaxID 303 only; does not support strain-level or step-level catalytic ability.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_103：Shows which organisms are attached to target gold steps; does not establish P. putida for the answer&#x27;s foreign entry reaction.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> Several species-level traits are consistent with frozen P. putida gold observations: motility, rod-shaped morphology, Gram-negative, non-sporulating, and broad phenol/aromatic degradation. But important values are low-confidence internal approximations (e.g., temperature optimum, pH optimum), F5/F14 are null despite available gold records, and F9 enzyme activities and F6 oxygen-respiration detail are not directly supported by the frozen gold. Partial accuracy with key gaps supports 6.

<details><summary>V0.4理由与本行变化背景</summary>

15项字段齐全，12项有值、3项（F4盐度/F5保藏/F14基因组）诚实null，符合&quot;明确未知≠遗漏≠错误&quot;。有值项与gold 303物种级观测一致或相容：F11杆状、F12革兰氏阴性、F13不产孢、F10有运动性与gold OBSERVED一致；F8&quot;可降解酚类及多种芳香族化合物&quot;与gold degradation: phenol=true、aromatic hydrocarbon=true相容；F3最适pH 7.0与gold pH growth=7.0观测一致；F2 preference&quot;中温&quot;与gold mesophilic一致。不足：F2最适30°C无gold最适子字段可核（subfield mask标optimum_c=completeness_only），F9所列酚羟化酶/邻苯二酚1,2-双加氧酶活性不在gold酶活面板内，F7/F15为概括性表述，F6呼吸方式为常识性陈述；关键定量性状（盐度范围、保藏号CCUG 49576、基因组大小/GC）以null留空。综合落5–6档（部分性状准确且适用、关键项证据不足），档内取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_103：Supports several species-level morphological and physiological traits; does not support every answer value or an optimum-temperature claim.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_103：Shows which trait subfields have observed scalar support and which remain completeness-only or pending; does not convert missing answer values into scientific errors.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> All route, enzyme, microorganism, and trait claims trace only to evidence_registry entries with source_type INTERNAL_KNOWLEDGE_ONLY. There are no DOIs, database record IDs, locators, or retrieval records. The only official support in the request is E0 taxid:303 for species identity, but the answer itself did not deliver that record. This is MISSING_SOURCE for decision-relevant groups; no verified mis-citation and no cap.

<details><summary>V0.4理由与本行变化背景</summary>

可追溯性层：全部3条evidence_registry条目source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，claim_scope只是自述支持范围，无任何可定位条目、文献或计算记录→按四.3各claim group均为MISSING_SOURCE（决策相关组CG01/CG02/CG03/CG05/CG07/CG08同样缺失），落低分档；因属&quot;缺失而非误导&quot;，默认不cap，且答案未伪造EC/登录号/保藏号或假称数据库直查（唯一编号TaxID 303经E0核实学名匹配），故不构成已核实错引，无LOCAL/CRITICAL/SYSTEMIC。低分档内取2而非1：答案至少建立了claim_scope级的证据自述映射并对无来源事实统一标low/unknown，但无法定位任何一条关键结论的原始依据。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> The answer generally distinguishes uncertainty from fact: it uses low/medium/unknown confidence, labels raw_text as 内部知识, explicitly nulls several unknown traits, and lists route and downstream uncertainties. It does not systematically present predictions as observations. Minor weakness: not every trait value explicitly states whether it is observed, predicted, or inferred, and some internal-knowledge values still read as settled species traits. No D6 key error.

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体良好：route_summary直言&quot;起始酶与对应菌株的直接证据不足，整体置信度偏低&quot;；三步均设uncertainty字段并点名可能的3-异丙基邻苯二酚支路与下游未逐项展开；uncertainties列出三条具体待验点（含丙酮副产物去向未纳入主链）；未知性状一律null+confidence=unknown而不编造；证据类型统一标INTERNAL_KNOWLEDGE_ONLY，未把内部知识包装成数据库观测。扣分点：F1/F6/F10/F11/F12/F13等以medium confidence给出物种级结论却未逐项注明&quot;记忆值、建议复核&quot;，属个别点位证据强度与置信标签略不相称；但未发现系统性把预测写成实证、也未掩盖已知矛盾，按D6严重度条款仅档内扣分、不cap。落7档。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`f378e3679250730dff5e108c06f8e9d49758b33072b5d456486fc1b029d3472e`。

### D1 完整性与任务符合度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 路线名原样给出；6步均给主底物/产物，前3步可对应gold必答S02→S03→S01，另有下游延续。S2–S6有酶/菌，S1诚实置空菌和EC；两个菌profile均列15项字段，多个未知按null登记。完成度有明确未知缺口，但未见路线名或交付格式重大偏离，按7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：支持必答三步的反应序列与终点；不支持答案所给具体酶身份或EC配对。
- QUESTION_TEXT / BIOPATH150_103_question：支持对每步主底物/产物、酶、微生物、15项性状及未知填null的格式要求。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链前三步化学方向正确：2-isopropylphenol→3-isopropylcatechol；3-isopropylcatechol间位开环为2-hydroxy-7-methyl-6-oxo-2,4-octadienoate；水解为2-hydroxypenta-2,4-dienoate+isobutyrate。产物与gold终点一致；下游水合、醛缩酶裂解和乙酰化脱氢化学连续。主要问题是S01/S03存在电荷/立体表示待核、部分产物未列H+，以及答案越过gold终点继续下游；按主链化学可靠、局部表示问题处理，给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：支持gold主链三步的底物、产物、方向与终点；不支持答案酶/EC身份。

</details>

### D3a 目标反应与酶对应：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按C03逐目标：S02入口反应式与gold MATCH，但所答phenol hydroxylase无EC且未入accepted酶集合，credit_class=UNRESOLVED_NONACCEPTED，记U；S03开环所答3-isopropylcatechol 2,3-dioxygenase EC 1.13.11.2/ipbC不在accepted集合1.13.11.14/1.13.11.39/1.13.11.M5，且结构诊断为ROUTE_HOLD_REPRESENTATION，记U；S01水解所答hydrolase无EC且未入accepted 3.7.1/3.7.1.8，且表示诊断为ROUTE_HOLD_REPRESENTATION，记U。S=0、U=3、N=3，无已核F/M，无确认KEY失败，不触发KEY4；按C04.5全U不自动NE或低分。答案给出与主链一致的逐步反应和可辨认酶名，但三个必答目标的酶对应均未获accepted/冻结证据确认，仅属部分可用支持；未达7–8所需主要对应可靠，故在5–6档取5而非6。诚实置空不抬高D3a。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_103：本题为LINEAR_UNIQUE、ordered_step_count=3；支持D3a按3个必答目标步评价，不把全图旁支作为缺步分母，也不证明酶对应正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：列出S01/S02/S03的目标底物、产物与方向；支持S02入口步反应层面MATCH以及S01/S03存在表示待核，不单独证明所答酶名或EC正确。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_103：列出accepted酶名与EC集合；支持所答phenol hydroxylase无EC、EC 1.13.11.2及hydrolase无EC均未形成accepted匹配，但不据此单独判为催化失败。
- RUBRIC_CLAUSE / C05：D3a带内判据：5–6为部分主干目标有适用支持但仍有实质未核/待修；7–8要求主要目标催化对应可靠。本条支持选5而非6或7。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P. putida mt-2身份有E0菌株记录和TaxID 303支持；P. fluorescens IP01作为异丙苯途径候选合理，但仅有INTERNAL_KNOWLEDGE_ONLY，且TaxID 294为物种级，不支持IP01菌株级身份；S1微生物显式null；mt-2的XylJ/K/Q步级活性未在E0核验。属合理候选、部分支持但关键菌株/能力未充分核验，按5–6档取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:bacdive:12880：支持P. putida mt-2菌株记录与培养温度等记录；不支持其各步酶活或完整2-isopropylphenol降解能力。
- E0_EVIDENCE / f3e0:taxid:303：支持物种级TaxID 303；不核验IP01或其他菌株级身份。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P. putida ORG_002的革兰氏阴性、杆状、运动、不产芽孢、好氧/中温等定性性状与gold可得表型一致；P. fluorescens ORG_001的性状多为种级内部知识，非IP01菌株专属，且温度/pH/盐度/保藏/基因组/栖息地大量null。已给性状大体合理，但菌株级适用性和可核证据不足，按5–6档取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_103：支持P. putida部分表型；不支持P. fluorescens IP01菌株级性状或所有数值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 证据注册表EVID_001–EVID_005均为MODEL_INFERENCE或INTERNAL_KNOWLEDGE_ONLY，数据库、record_id、可定位原文与claim级外部条目均缺失；答案自述未重新核对原文。核心路线、酶、菌和性状均无可追溯外部来源，属MISSING_SOURCE低分档；无已核实错引，不cap，给2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry:EVID_001-EVID_005：显示所有登记来源均为模型推断或内部知识，无可定位外部记录。

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确区分MODEL_INFERENCE与INTERNAL_KNOWLEDGE_ONLY，未知/未核实项大量置null，说明首步菌/EC、IP01与mt-2不能证明降解2-isopropylphenol、TaxID为物种级、性状非菌株专属等限制；置信度多为low/medium且与内部知识相称。披露充分、无系统性把预测写成实证，按9档。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties_and_confidence：显示答案主动披露未核实、物种级TaxID及非菌株专属性状；不证明这些事实为真。

</details>

## GPT5.6

答案SHA256：`da21d9e321fee913bcc68a0676c8732f665922ed6a92cf42256a69b847849005`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求完整主链、每步酶与对应微生物、15项性状；答案仅给1个推定初始羟基化步骤，且无微生物、无性状。虽route_scope名称可辨，但核心必需模块大部缺失，D1按1–2档给2；该缺失本身构成D1关键错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：支持题面要求完整主链、逐步酶菌与15项性状；不证明答案内容正确。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_103：支持本题主链需3个必答步骤；不扩展到其他旁支。
- ANSWER_TEXT / ANSWER：支持答案仅交付1步且无微生物/性状；不用于断言化学错误。

</details>

### D2 反应化学科学性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案仅1个初始羟基化步骤，未到达gold主链终点；所给产物2-Isopropylbenzene-1,3-diol与gold S02产物3-Isopropylcatechol不同，后续S03/S01及末端产物缺失，路径连续性严重断裂。D2按自身化学与连续性低档给2，不把D1任务缺失机械连坐为化学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：支持gold主链的步骤顺序与产物；不支持答案的2-Isopropylbenzene-1,3-diol为同一转化。
- ANSWER_TEXT / ANSWER：支持答案产物与gold S02不同且无后续步骤。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S01/S03未交付；S02所给转化/产物与gold entry NONMATCH；EC 1.14.13.7在E0无冻结记录，不能确认其具体底物-产物专一性。S=0，按C04低档给1；错误路线内部酶自洽不获目标信用，KEY4不另改。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_103：支持gold各步的accepted酶/EC集合；不证明答案的EC 1.14.13.7正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_103：支持S02目标产物；不支持答案产物。
- ANSWER_TEXT / ANSWER：支持答案仅1步且EC 1.14.13.7用于该推定步骤。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求每一步给出对应微生物；答案step.microorganism为null，organism_profiles为空，未交付任何物种/菌株身份或能力声称。D3b模块完全未交付，按MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：支持题面要求每步微生物与profile；不证明任何微生物内容。
- ANSWER_TEXT / ANSWER：支持答案未交付微生物模块。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求每个organism_profile一次返回15项性状；答案organism_profiles为空，无任何性状值、明确未知或证据。D4模块完全未交付，按MISSING=1。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：支持题面要求15项性状；不证明任何性状值。
- ANSWER_TEXT / ANSWER：支持答案未交付性状模块。

</details>

### D5 来源与可核查性：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 唯一证据EVID_001为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；所有结论无法追到可定位条目或文献，按MISSING_SOURCE低档给1。无已核实错引，不触发D5关键错误cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：支持答案仅交付内部知识、无外部可定位来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确把唯一步骤标为推定/低置信，说明未确认专属菌株与实验证据，并列出未知微生物、下游步骤和氧条件未指定；未把预测写成观测。D6按诚实披露给8，不因科学内容缺失自动压低。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：支持答案明确披露推定、低置信和未知。
- RUBRIC_CLAUSE / P45：支持诚实披露可在D6获得较高分；不替代科学正确性评分。

</details>
