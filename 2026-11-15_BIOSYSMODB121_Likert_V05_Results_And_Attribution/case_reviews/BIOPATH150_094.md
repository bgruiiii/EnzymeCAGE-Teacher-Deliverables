# BIOPATH150_094：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：testosterone and androsterone degradation to androstendione (aerobic)

污染物：Androsterone；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

本轮参考：用户确认雄酮至雄烯二酮2步；睾酮入口是背景，未答背景不扣分。

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 67 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 45.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 55.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 58 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 51 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 42 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`1fe7422fa21d99efd7fd4ee3e7f619cccca1eccd76ee89c3101497b363f8a02c`。

复审/来源说明：用户确认060四步/094两步后首次评分；原引用TABLE0维度名离线对应既有行，模型原分/理由/引用未改。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> 题面指定路线名称原样填写（aerobic，与route_scope一致），无改选路线；用户确认的2个必答步（雄酮→雄烷二酮→雄烯二酮）均已交付，每步给出主底物/主产物英文名+SMILES、首选酶+EC、对应微生物；同一菌按物种+菌株去重为1条profile（ORG_001）并由两步共同引用，符合去重要求；15项性状字段全部出现，缺项以null如实标注；睾酮背景步未答按已确认范围不扣分（背景不计入必备分母）。扣分点为若干性状子项（F3全部、F14全部、F2/F4数值）留空与SMILES未标注立体，属少量遗漏与表示不足，不构成核心任务缺失或路线偏离。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块全覆盖：route_scope原样填写题面路线名与aerobic；雄酮主链两步每步均给底物/产物英文名与SMILES、一个首选酶+EC、一个对应菌并绑定organism_profile_id；15项性状按展示顺序全部出现（13项有实质内容、2项显式unknown）；evidence_registry与uncertainties齐备。诚实null（pH、基因组、温盐数值）按量表二/P45不记为遗漏或错误；睾酮支路以alternative_branches声明is_part_of_scored_main_route=false、下游与中央代谢声明超范围，符合P29终点边界。档内取9：S2电子受体未具名、若干性状数值子字段空缺属需补全而非模块缺失或范围偏离。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / task/route_scope：指定路线名须原样填写、每步需底物产物名+SMILES、首选酶+EC、对应微生物、15项性状
- SCOPE_ROW / SCOPE_ROW#BIOPATH150_094：n_required=2，required_step_ids=S02|S03，S01为BACKGROUND_NOT_REQUIRED，未答背景不扣分
- ANSWER_TEXT / steps&#91;S1&#93;,steps&#91;S2&#93;：两步完整交付且顺序为雄酮→雄烷二酮→雄烯二酮
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_094：起终点为Androsterone→Androstenedione，与答案终点一致

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 化学主链与冻结参考两步一致：S1为3α-羟基氧化为3-酮基（罗酮→5α-雄烷-3,17-二酮），NAD+为电子受体并列出NADH/H+；S2为A环Δ4-脱氢（雄烷二酮→雄-4-烯-3,17-二酮），受体以“未指定氧化型电子载体”如实标注，与参考的通用氧化/还原载体口径一致；反应方向为有向正向，终点为参考指定终点雄烯二酮，无跳步、无反向、无替代路线，立体未显式标注已在uncertainties披露（表示缺陷而非化学错误），故不入低档；扣分仅因立体学表示缺失与S2电子受体未具体化，属不改变主要结论的局部问题，落7–8档并取上沿。

<details><summary>V0.4理由与本行变化背景</summary>

两步主链与gold逐项吻合：S1 雄酮3α-羟基氧化为5α-雄烷-3,17-二酮（对应gold S02 Androsterone→Androstanedione，方向一致），S2 A环引入C4=C5生成雄烯二酮（对应gold S03 Androstanedione→Androstenedione）。S1给出NAD+/NADH/H+，氧化还原方向正确；产物SMILES（C4=CC(=O)平面形式）与gold canonical结构构成连接一致；答案自述SMILES为非立体平面形式，属已披露的表达简化而非原子不守恒。扣分点：S2电子受体仅写&quot;unspecified&quot;、无smiles（gold亦仅记为&quot;a reduced two electron carrier&quot;），属局部辅因子/计量简化，按八.辅因子条款在7–8档处理、不触发关键错误；止于题面终点androstenedione，未延续下游不扣覆盖率（四.2/P29）。档内取8。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02：Androsterone+NAD(P)+→Androstanedione+NAD(P)H+H+；S03：Androstanedione+氧化型载体→Androstenedione+还原型载体
- GOLD_SLICE / source_reaction_records.tsv#case:BIOPATH150_094：BSY-r02482为androsterone 3-dehydrogenase；BSY-r03042标题含oxidized/reduced electron carrier，支持受体未指定不构成错误
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_094：题面终点Androstenedione，答案止于该终点
- ANSWER_TEXT / steps&#91;S1&#93;,steps&#91;S2&#93;：两步主底物/主产物SMILES骨架与参考一致（仅立体未表）

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 逐个必答目标核验：S1对应EC 1.1.1.50，落在参考酶BSY-e01958的多注EC集合(1.1.1.357|1.1.1.213|1.1.1.209|1.1.1.50)之内，按集合内任一合法编号可接受；S2酶名3-oxo-5alpha-steroid 4-dehydrogenase与EC 1.3.99.5与参考酶BSY-e02771完全一致。两个必答目标均为S，无已核功能不相容、无名称—EC矛盾，KEY(ENTRY/TERMINAL)均有对应支持且无已核关键失败，故不适用D-KEY4上界；仅余立体与酶同工酶/基因未指认、以及答案证据为内部知识（不影响目标酶—反应对应本身的正确性）等局部问题，按既定科学证据门在7–8档内取8。

<details><summary>V0.4理由与本行变化背景</summary>

两步酶名与EC与gold对应：S1 3alpha-hydroxysteroid dehydrogenase (NAD(P)+) EC 1.1.1.50落在gold S02 3alpha-hydroxysteroid dehydrogenase/carbonyl reductase的多注EC集合（1.1.1.357|1.1.1.213|1.1.1.209|1.1.1.50）内，按四.5多注保守条款可接受、不扣；S2 3-oxo-5alpha-steroid 4-dehydrogenase EC 1.3.99.5与gold S03 3-keto-5alpha-steroid Delta4-dehydrogenase完全相同。酶功能类别与反应类型匹配，无&quot;水解酶解释羟化&quot;类错配。限制：gene_or_protein均null（题面允许未知）；EC的官方accepted name/reaction在E0无条目（GAP-094-005/008/013/016），仅能与gold对照，达不到9–10档&quot;身份与作用范围清楚&quot;。档内取8。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_094：S02 3alpha-hydroxysteroid dehydrogenase/carbonyl reductase（含EC 1.1.1.50）；S03 3-keto-5alpha-steroid Delta4-dehydrogenase EC 1.3.99.5
- SCOPE_ROW / SCOPE_ROLES.tsv#case:BIOPATH150_094：S02=REQUIRED/ENTRY，S03=REQUIRED/TERMINAL，S01=BACKGROUND_NOT_REQUIRED；无已登记确认失败证明
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：两个必答反应的方向与参与者与答案所选酶功能相容
- ANSWER_TEXT / steps&#91;S1&#93;.enzyme,steps&#91;S2&#93;.enzyme：答案自述两个酶的EC与名称，可与参考逐项比对

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 微生物对应在物种层与参考一致：两个必答步的参考策展关联均为Comamonas testosteroni（TaxID 285，GCA_016599875.1），答案两步也均归该物种，主微生物推荐未被推翻，故不触发关键错误。但答案把身份具体化到菌株层（ATCC 11996）并给出TaxID 1126，而冻结参考对同一物种给的是TaxID 285、保藏号JCM 6233：菌株级声称缺乏菌株级证据（粒度不足，按身份阶梯档内扣、默认不cap），编号与参考不一致且无法用本轮材料核实1126的ScientificName/rank/lineage，不能判为已核身份错配、也不得直接判虚构，按未决待核处理；因此落“合理候选+部分支持、若干身份条目未充分核验”的5–6档并取上沿6。全路径能力声称限于用户修正后的2步范围，与两步的STEP级关联相容，不另加cap。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份与步级归属与gold一致：Comamonas testosteroni在organism_gold中对S01/S02/S03均为EXACT匹配，答案两步均归属同一物种并绑定同一profile（ORB_001），未把单步菌写成他种菌；complete_pathway_organism_profile_id=ORG_001的全路径能力声称与gold PATHWAY_COMPLETE(taxid 285, pathway_complete=TRUE)方向一致，未见&quot;由基因组存在某酶直接推断整条路径&quot;的越级表述。限制：菌株级身份（ATCC 11996 + TaxID 1126）在E0无任何记录（GAP-094-027/029），gold记录为物种级taxid 285/GCA_016599875.1；编号待核不能按已核实身份错配处理，也不能按&quot;号码看似合理&quot;放行（四.6/P67），故按八.D3b阶梯保守取7（粒度待核档内扣），不cap、不判编造。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_094：三个参考步的策展关联菌均为Comamonas testosteroni、TaxID 285、GCA_016599875.1，未给菌株级编号
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_094：TaxID 285 的保藏记录为JCM 6233（bacdive 165379），与答案ATCC 11996不同编号
- GOLD_SLICE / source_pathway_annotations.tsv#case:BIOPATH150_094：TaxID 285 pathway_complete=TRUE为旧路径级标签，不自动证明菌株级或修正后全链能力
- ANSWER_TEXT / steps&#91;*&#93;.microorganism：物种名正确、两步同菌，但菌株与TaxID为内部知识标注且未被冻结材料核实

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 已给性状中可核项大体正确：F10运动性=可运动（参考observed true）、F11杆状（rod-shaped）、F12革兰氏阴性（gram positive=false）、F13不产芽孢（sporulation=false）、F8降解芳香/烃类能力（参考predicted true）、F9含羟基甾体脱氢酶活性（与酶参考相容）；但多项可评分观测被留空或弱化：F2未给min 10/max 37数值（仅在preference写30–37°C，略窄于参考growth 28–37）、F4未给0–2% NaCl数值、F14未给GCA_016599875.1/基因组大小/GC（参考59.4–61.9%），F5给的ATCC 11996与参考JCM 6233不一致且未核；F1把参考observed“aerotolerant=true”表述为“专性好氧”，属性状类别表述与参考观测不完全一致但未推翻有氧代谢结论；F15参考为UNKNOWN，答案给出广布生境/临床来源但无条目级支持。综合为“部分性状准确适用、关键项证据不足或表述需修订”，未达关键性状离谱到误导筛选的程度，不cap，落5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

已给性状多数与gold观测一致：F10可运动（presence of motility=true）、F11杆状、F12革兰氏阴性（gram positive=false）、F13不产芽孢、F2偏好&quot;中温性&quot;（gold preference=mesophilic，生长28–37°C）；F1&quot;好氧、非发酵&quot;与gold aerotolerant=true、facultative anaerobe=false方向一致；F4&quot;非嗜盐&quot;与gold盐度0–2% NaCl观测相符。限制与缺口：温度min/max（gold观测10/37°C）、盐度数值、基因组GCA_016599875.1均填null，按P112属completeness（主归D1，不重复重扣）；F5 ATCC 11996与gold观测JCM 6233为不同保藏库编号、未核；F7&quot;以睾酮等C19雄激素为唯一碳源&quot;、F15栖息地广布描述无gold观测条目；F1以high confidence给&quot;专性&quot;好氧，精确耐氧类型待核。关键性状（氧需求、甾体降解/碳源）方向与gold一致，故不入3–4档；档内取7。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_094：F1 aerotolerant=true(observed)；F2 growth 28–37℃/min 10/max 37/mesophilic；F4 0–2% NaCl；F5 JCM 6233；F10 motility true；F11 rod-shaped；F12 gram positive=false；F13 sporulation=false；F14 genome size 2086285–6062703bp、GC 59.4–61.9%；F15 UNKNOWN
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_094：F2 minimum_c=10、maximum_c=37；F4 minimum=0、maximum=2 为可评分观测子项；optimum/preference不构成数值准确性分母
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_094：F3/F6/F15无观测值仅completeness_only；F2/F4/F5/F7–F14有观测可评分
- ANSWER_TEXT / organism_profiles&#91;ORG_001&#93;.traits：答案给出的性状值、confidence与evidence_id分布

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分3 → V0.5新分4，变化+1。

新裁判理由：

> 答案evidence_registry共5条，source_type全部为INTERNAL_KNOWLEDGE_ONLY，record_id与locator基本为空，只有MetaCyc/IUBMB/BRENDA等库名与EC号、路线名，无法定位到具体条目；决策相关组（路线/反应、酶-EC、微生物身份、性状）均无条目级可定位可核对证据，符合“仅给笼统库名/模型名/路线名，结论与来源关联很弱”的3–4档；因给出了可核对的EC编号与路线名、并对内部知识属性作了声明，取该档上沿4。来源缺失/笼统按规则默认不构成关键错误cap；评分方资料未回填为模型证据，也未把“无法核验”判为错引。

<details><summary>V0.4理由与本行变化背景</summary>

全部证据条目source_type=INTERNAL_KNOWLEDGE_ONLY（EVID_001–EVID_005），无一条record_id；所写数据库名（MetaCyc、IUBMB/BRENDA）与一个pathway locator属自我声明，未构成可定位到条目的记录。按四.3/P34，INTERNAL_KNOWLEDGE_ONLY自述归MISSING_SOURCE；决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09及CG04/CG10，含CG14中支撑目标污染物能力的声称）全部无可核对条目级证据，按P41落低分档（默认不cap）。无已核实错引（E0整题EVIDENCE_GAP，编号类声称保持UNRESOLVED，不判虚构/不判CONTRADICTED）。档内取3：evidence_registry对每条证据列了claim_scope、映射结构清楚且诚实标注内部知识，比&quot;几乎无法定位&quot;略好，但无任何可核对来源，不能进5–6档。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：五条证据全为INTERNAL_KNOWLEDGE_ONLY，record_id/locator为空，仅库名+EC/路线名
- RUBRIC_CLAUSE / P34：完全无引用或仅INTERNAL_KNOWLEDGE_ONLY类自我声明按MISSING_SOURCE低分档，默认不触发cap
- RUBRIC_CLAUSE / P35：决策相关组全部仅有笼统来源时落3–4档；部分条目级证据才升5–6档
- RUBRIC_CLAUSE / P51：D5只评价模型实际交付的记录，评价者新增证据不得回填

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 正面：uncertainties具体列出SMILES未标立体、EC 1.3.99.5来自内部知识未核对、TaxID/ATCC未逐项核对、无外部实时检索，并在S2 uncertainty中明示生理电子受体未确证、基因未知，属于与依据相称的诚实披露。负面：全部证据为INTERNAL_KNOWLEDGE_ONLY，却在结果字段中把S1酶、多条性状(F1/F6/F7/F11/F12/F13)标为confidence=high、F5为medium，证据类型与置信强度不相称，属多处过度确信而非系统性把预测写成实测、也未见掩盖矛盾，故落“有不确定性说明但部分结论强度仍超过依据”的5–6档取6，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露具体且与证据相称：明确声明路线/反应事实主要依据内部知识、无外部实时检索；S2酶与EC&quot;未核对原文&quot;、编码基因与生理电子受体未知并填null；S1同工酶未指定；最适温度/pH/盐度与基因组信息缺乏可靠来源而填null；SMILES为非立体形式；TaxID 1126与ATCC 11996声明未逐项核对。缺失项一律null未编造，downstream_continuation/central_metabolism_entry明确标注&quot;超出本题路线范围（未评分）&quot;，睾酮支路标is_part_of_scored_main_route=false，边界诚实。扣分点：F1/F6/F7/F11–F13等以high confidence给出而依据同为内部知识，属局部过度确信（非系统性、无掩盖已知矛盾），按八.D6/P119档内扣分、不cap。取8。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：具体披露立体缺失、EC内部知识未核、TaxID/ATCC未核、无外部检索
- ANSWER_TEXT / confidence字段：内部知识来源字段仍标high/medium（S1酶high；F1/F6/F7/F11/F12/F13 high；F5 medium）
- RUBRIC_CLAUSE / P119：单点/局部过度确信档内扣（通常5–6档），系统性误导才cap
- RUBRIC_CLAUSE / P121：D5错引/来源不足不自动连坐D6

</details>

## DeepSeek

答案SHA256：`24bb54ea4dcac621654959345b6da17e568873d2e2eebd1036610f50fe6a1be6`。

复审/来源说明：用户2026-11-15明确确认060四步/094两步范围后首次评分；采用独立修正参考版本，原题与原答未改。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 路线名原样保留，两个必答步、酶/菌及15项性状均已给出；背景睾酮入口步按范围不要求且未答不扣。但两个必答步的底物/产物实体与题面指定立体化学不符，任务符合度只能落在较弱档；未达到核心模块大部缺失的关键错误门槛。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求的模块均有实质交付：route_scope.chosen_route_name逐字照录题面路线名；steps两条均给出底物/产物英文名与SMILES、首选酶含EC、对应微生物；organism_profiles按物种+菌株只出现一条且被step引用；15项性状全部出现（11项填写/4项显式未知/0遗漏），alternative_branches声明睾酮支不属于评分主链。扣分点：来源模块实质薄弱（三条evidence均为INTERNAL_KNOWLEDGE_ONLY且database/record_id/locator全为null）、uncertainties为空；辅因子字段未列（任务未强制，归D2局部计量讨论）。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：输出包含两个步骤、每步底物/产物SMILES、酶、微生物及15项性状
- SCOPE_ROW / BIOPATH150_094：必答S02+S03两步；S01睾酮入口为背景，未答不扣
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：gold给出S02/S03应覆盖的底物、产物与立体结构

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 反应类型和连接方向大体正确（C3氧化、Δ4脱氢），但两个必答步的底物/产物均与gold指定立体化学冲突，未真正到达题面指定的Androstenedione；显式立体冲突覆盖两处必答步，主链化学身份失效，按D2显式立体冲突/关键错误上限≤4。

<details><summary>V0.4理由与本行变化背景</summary>

主链 Androsterone→5α-androstane-3,17-dione(Androstanedione)→androst-4-ene-3,17-dione(Androstenedione) 与gold LINEAR_UNIQUE的S02→S03顺序、方向一致：首步C3羟基氧化为酮，第二步Δ4-脱氢生成雄烯二酮；起点为gold根化合物Androsterone，终点为题面路线名“to androstendione”的终点，符合P29终点边界。未列NAD(P)+/NAD(P)H等辅因子，按P103属局部计量缺陷，落7–8档，不cap；产物SMILES与gold iso-SMILES在环稠合立体描述子上存在局部差异（局部问题，不影响主链结论）。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：S1底物Androsterone与产物5α-Androstane-3,17-dione；S2产物Androstenedione的SMILES
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：gold S02/S03指定Androsterone、Androstanedione、Androstenedione的精确立体结构
- SCOPE_ROW / BIOPATH150_094：必答范围为S02-&gt;S03至Androstenedione

</details>

### D3a 目标反应与酶对应：8 / SCORED

V0.4旧分9 → V0.5新分8，变化-1。

新裁判理由：

> S1使用3α-hydroxysteroid dehydrogenase EC 1.1.1.50，属gold S02多EC集合中的合法项；S2使用3-keto-5alpha-steroid Delta4-dehydrogenase EC 1.3.99.5，与gold S03一致。未见酶名—EC—反应类型矛盾；因无更高层蛋白/实验级催化证明，按现有证据门取8。

<details><summary>V0.4理由与本行变化背景</summary>

两步酶对应清楚且与gold相容：S1“3α-hydroxysteroid dehydrogenase”EC 1.1.1.50落在gold S02“3alpha-hydroxysteroid dehydrogenase/carbonyl reductase”的多注EC集合(1.1.1.357|1.1.1.213|1.1.1.209|1.1.1.50)内，按四.5保守条款不判错；S2“3-oxo-5α-steroid 4-dehydrogenase”EC 1.3.99.5与gold S03“3-keto-5alpha-steroid Delta4-dehydrogenase”完全一致；酶名与EC类别（氧化还原酶）相容。EC官方accepted name/reaction因E0整题证据缺口未核，登记待核但不影响当前档位。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：两步酶名与EC绑定
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_094：S02含EC 1.1.1.50；S03为EC 1.3.99.5
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：目标反应类型与方向

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 两个必答步均使用Comamonas testosteroni，TaxID 285与gold STEP行一致且同菌去重；但答案额外给出ATCC 11996菌株级标识，gold仅给物种级285/GCA_016599875.1，complete-pathway标签也不是逐株实证。属物种级证据支持菌株级/全路声称的粒度不足，档内扣分、不cap。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份 Comamonas testosteroni + TaxID 285 与gold organism_gold三处STEP行EXACT一致，且该taxid的PATHWAY_COMPLETE=TRUE；答案把两步均归属同一菌并在步级绑定，与gold步级归属一致，不存在“把单步菌写成全路径菌”的问题。菌株级声称“ATCC 11996”在冻结记录中无对应保藏号条目（gold仅给物种级与基因组GCA_016599875.1），属粒度不足，按D3b身份阶梯①档内扣分（七档附近）、默认不cap；引用支持范围问题另归D5。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：S1/S2均C. testosteroni ATCC 11996 TaxID 285；complete_pathway_organism_profile_id=ORG_001
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_094：S02/S03的策展关联为C. testosteroni TaxID 285
- GOLD_SLICE / source_pathway_annotations.tsv#case:BIOPATH150_094：有285的PATHWAY_COMPLETE旧路径标签，但不自动证明逐株修正范围能力

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> F11杆状、F12革兰氏阴性、F13不产孢、F10运动、F7 citrate/chemoheterotrophy、F8芳香族降解等与gold可评项一致或相容；但F2温度、F14基因组等关键可评项为null，F1写成好氧而gold观测为aerotolerant，F5给ATCC 11996而gold记录JCM 6233，F15无gold观测却作广适描述。部分性状可用但关键项证据不足，取5–6档上沿6。

<details><summary>V0.4理由与本行变化背景</summary>

已填11项性状中，F10运动性(true)、F11杆状、F12革兰氏阴性(gram positive=false)、F13不产芽孢(false)与gold observed一致；F1“好氧”与gold observed aerotolerant=true存在表述粒度差异；F5保藏号ATCC 11996与gold observed JCM 6233不同（可能为同菌不同保藏号，冻结证据无法判定，按P52不据此判错）；F7/F8/F9/F15在gold仅有预测条目或UNKNOWN，不能确认；F2/F3/F4/F14诚实null。关键应用性状（氧需求CG10）方向相符但证据不足，落5–6档取6。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：15项性状取值、置信与evidence_id
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_094：TaxID 285的观测/预测性状，包括F1 aerotolerant、F2温度、F5 JCM 6233、F14基因组
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_094：F2/F5/F7/F8/F9/F10/F11/F12/F13/F14可评分；F3/F4/F6/F15仅完整性
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_094：F2 min/max、F4 min/max等子字段金标值

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> EVID_001–EVID_003全为INTERNAL_KNOWLEDGE_ONLY，database、record_id、locator均null；反应、酶、菌、性状均无可定位外部来源，属MISSING_SOURCE覆盖全部关键结论，按D5低分档取1；缺失默认不cap。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry三条全部source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null，按四.3/P34属MISSING_SOURCE：决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）与条件组（CG04/CG10/CG11–CG14）均只有自我声明，无可定位条目级证据，落低分档取2。全案无经核实错引（E0 EVIDENCE_GAP，EC/TaxID/保藏号类声称保持UNRESOLVED，不判虚构、不判CONTRADICTED），MISSING_SOURCE默认不触发cap，key_error=N。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：所有证据均为内部知识型，无外部记录定位
- RUBRIC_CLAUSE / P33：MISSING_SOURCE/INTERNAL_KNOWLEDGE_ONLY按D5低分档，默认不cap

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案对F2/F3/F4/F14等给null，部分保留未知；但大量性状和步骤仅INTERNAL_KNOWLEDGE_ONLY却标medium/high，无raw_text、uncertainties为空，未说明立体化学冲突和来源限制。属多处过度确信、证据类型与置信不相称，但尚未证明系统性掩盖，取3–4档上沿4。

<details><summary>V0.4理由与本行变化背景</summary>

答案以confidence(medium/high/unknown)与source_type=INTERNAL_KNOWLEDGE_ONLY标注证据性质，并把F2/F3/F4/F14诚实置null，属有不确定性说明；但uncertainties为空、无限制与矛盾说明，且以内部知识支撑的F5/F12/F13标high、complete_pathway_organism_profile_id=ORG_001与全部性状evidence均指向单条内部知识条目，结论强度超过依据，落5–6档取6。属单点/局部过度确信而非系统性误导，不cap。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT：证据均为INTERNAL_KNOWLEDGE_ONLY；部分性状标medium/high但raw_text为null；uncertainties为空
- RUBRIC_CLAUSE / P119：单点/多处过度确信与系统性误导分档；系统性误导才cap

</details>

## Kimi

答案SHA256：`268b3489abce657bc64f587e23f781184caaf739f3051e23bca3014d9b49d2e1`。

复审/来源说明：用户2026-11-15明确确认060四步/094两步范围后首次评分；采用独立修正参考版本，原题与原答未改。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 路线名原样、需答两步均出现、终点为 androstenedione，15项性状也齐全；但S1产物立体化学与参考S02产物 Androstanedione 的指定结构冲突，任务路线符合度不完整。按D1任务偏离/符合度上限取4，不取1–2因大部分模块仍在。

<details><summary>V0.4理由与本行变化背景</summary>

任务要求的主链、逐步底物/产物名与SMILES、一个首选酶及EC、对应微生物均实质交付；route_scope.chosen_route_name 逐字复制题面路线名、oxygen_condition=aerobic；organism_profiles按物种+菌株去重为一条(ORG_001)；15项性状全部占位、13项填写+2项诚实null。属大部分要求完整、关联清楚，仅少量性状数据空缺，落7–8档取高值。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- SCOPE_ROW / BIOPATH150_094：required S02/S03；S01为背景不要求
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02目标产物 Androstanedione 与S03终点 Androstenedione
- GOLD_SLICE / SCOPE_ROLES.tsv#case:BIOPATH150_094：S02 ENTRY、S03 TERMINAL、S01 BACKGROUND_NOT_REQUIRED

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 主链从 androsterone 到 androstenedione，两步方向正确，S2与参考S03匹配，终点符合题面；但S1与参考S02存在关键中间体立体化学冲突，第一步产物结构仍需修订。按5–6档局部成立但关键中间体待修订，取5。

<details><summary>V0.4理由与本行变化背景</summary>

两步化学与gold主链逐步吻合：S1 Androsterone→5α-androstane-3,17-dione（3-OH氧化为酮），S2 5α-androstane-3,17-dione→androst-4-ene-3,17-dione（A环Δ4脱氢成烯酮），方向与连续性正确，止于题面终点androstenedione。SMILES结构自洽。辅因子（NAD(P)+/NAD(P)H）仅在reaction_type文字说明、未作为参与者列出，属局部计量缺陷，按P103落7–8档，不cap；取8。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02 androsterone→Androstanedione；S03 Androstanedione→Androstenedione
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_094：起终点：Androsterone→Androstenedione

</details>

### D3a 目标反应与酶对应：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> N=2。S1酶为3alpha-hydroxysteroid dehydrogenase EC 1.1.1.50，属于参考S02多EC集合，目标功能可支持S。S2用EC 1.3.1.22，而参考S03为EC 1.3.99.5，显式EC配对未核，按C03记U而非F。C=0.5，候选带&#91;5,6&#93;；因终端步骤仍有待核缺口，不取6，取5。KEY角色存在但无已确认KEY F/M，不触发KEY4。

<details><summary>V0.4理由与本行变化背景</summary>

步骤1酶 3α-hydroxysteroid dehydrogenase(B-specific) EC 1.1.1.50 落在gold S02多注EC集合(1.1.1.357|1.1.1.213|1.1.1.209|1.1.1.50)内，名称-反应自洽，属集合内合法选号。步骤2答案取 3-oxo-5α-steroid 4-dehydrogenase(NADP+) EC 1.3.1.22，gold记为 EC 1.3.99.5；二者同属3-oxo-5α-steroid 4-dehydrogenase家族、名称与EC及反应方向自洽，E0为EVIDENCE_GAP无法裁决差异，按四.5保守条款不判错、保留待核。主要步骤酶对应可靠、少量条目需确认，落7–8档取7。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_094：S02 EC集合含1.1.1.50；S03参考EC=1.3.99.5
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02/S03目标反应底物与产物
- GOLD_SLICE / SCOPE_ROLES.tsv#case:BIOPATH150_094：S02 ENTRY、S03 TERMINAL

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 物种 Comamonas testosteroni 与参考 organism_gold 一致；ATCC 11996 为给定菌株，但参考仅给物种级 TaxID 285/GCA_016599875.1，未给 ATCC 11996 的菌株级逐步反应与全路径证据。按身份阶梯属粒度需确认，不判cap；主要微生物对应可靠但具体菌株能力仍需确认，取7。

<details><summary>V0.4理由与本行变化背景</summary>

两步均归属 Comamonas testosteroni ATCC 11996，物种与gold organism_gold 的 Comamonas testosteroni(EXACT, TaxID 285)一致；complete_pathway 声称与gold PATHWAY_COMPLETE(TaxID 285)=TRUE一致。菌株ATCC 11996=DSM 50244类型株与gold JCM 6233/GCA_016599875.1 的菌株级对应在E0中未核实，属粒度/菌株级待核，按身份阶梯①档内扣、默认不cap。主要微生物对应可靠、少量菌株级条目待确认，取7。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_094：三个STEP均匹配 Comamonas testosteroni，TaxID 285
- GOLD_SLICE / source_pathway_annotations.tsv#case:BIOPATH150_094：PATHWAY_COMPLETE 物种级记录，不等于ATCC 11996菌株级全路径证明

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项齐全；F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming 与参考观测一致。但F1写 strictly aerobic 与参考 aerotolerant 不符；F2未填参考观测 min/max（参考有10/37或28/37，optimum本身不可判），F4观测盐度未填，F14基因组全空；F7/F8/F15有超出给定观测的外推。部分准确但关键项证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状中，gold可核的定性项全部正确：F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming、F5 ATCC 11996（与gold类型株同源）；F3 pH≈7与gold预测6.9–7.4相容；F2 optimum 30、mesophile与BacDive相符。但gold可评分的定量项缺失：F2温度min10/max37未填、F4盐度min0/max2%NaCl留null、F14基因组(GCA及size/GC)留null；F1标为strictly aerobic而gold观测aerotolerant=true存在差异。诚实null不计为错误(主归D1)，但关键定量性状证据不足，落5–6档取6。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_094：C. testosteroni 的F1/F2/F4/F5/F10–F14观测及F15 UNKNOWN
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_094：F2/F5/F7–F14可评分或completeness-only的范围
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_094：F2 minimum/maximum、F4 min/max等子字段观测值

</details>

### D5 来源与可核查性：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 路径、酶、菌的关键结论均有具体EVID指向（BRENDA/PubChem/ATCC/BacDive），多数可定位到条目；但EVID_005无locator，若干性状共用泛化菌株来源，F14无来源，记录不完整。无已核实错引，取7。

<details><summary>V0.4理由与本行变化背景</summary>

答案提供了条目级可定位引用：BRENDA EC 1.1.1.50/1.3.1.22、PubChem CID 5879/6128、BacDive DSM 50244、ATCC 11996，并通过step.reaction_evidence_id/trait_evidence_id与各trait.evidence_id建立了较好映射，可追到具体记录（非仅库名）。但E0为EVIDENCE_GAP(entries=0)，无法核对所引条目实际支持内容，全部来源状态保持UNRESOLVED_SOURCE待核；无经核实的错引，不触发cap。决策相关组存在条目级可定位证据→5–6档，取6。另：gold terminal字段=Testosterone与路线名/产物不一致属gold内部问题，登记review_queue不归责答案。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：EVID_001–EVID_006的database/record_id/claim_scope/locator及步骤引用

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 列出S2 EC方向不确定性与未填TaxID/genome等未知，多项null处理清楚；但F1以high写 strictly aerobic 与参考 aerotolerant 冲突且未披露，F8/F15等置信/来源强度偏高。大部分未知与限制已标注但有少量过强表述，取7。

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露较好：uncertainties显式说明为防菌株/装配误配而将ncbi_taxid、基因组size/GC留null，并主动标注S2 EC 1.3.1.22 的方向歧义；各trait给出confidence并附raw_text，F4/F14标unknown；D5式待核与自我限制表达具体。个别项仍有轻度过度确信（F1 strictly aerobic标high、F7/F8/F9源自单一数据库却未标注为未核实），但属单点、非系统性误导，按P119档内扣分而非cap。落7档。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：答案自述的EC方向、未填TaxID/genome等不确定性
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_094：F1 aerotolerant 观测与F15 UNKNOWN，用于核对披露一致性

</details>

## Qwen

答案SHA256：`1bf6536daa4a72b421c61adcebe3b5d20e0d68a3503c80ecc69947c446ec07d8`。

复审/来源说明：用户确认060四步/094两步后首次评分；原引用TABLE0维度名离线对应既有行，模型原分/理由/引用未改。

### D1 完整性与任务符合度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> 主链两步、每步主底物/主产物、酶与EC、微生物及route_scope均已给出，指定路线名原样保留；15项性状字段齐全但F2/F3/F4/F5/F14为null，微生物未给菌株/TaxID，属大部分必要内容完整、少量完成度缺口，取7。

<details><summary>V0.4理由与本行变化背景</summary>

D1取7–8档：路径、两步酶与EC、对应微生物、15项性状字段、来源登记与不确定性模块均已交付；chosen_route_name原样填写，主链止于题面路线名所指的Androstenedione，并将睾酮分支明确标为非评分主链。5项性状为显式null/unknown，菌株与TaxID未填但允许null，属少量粒度不足而非重大范围偏离，故取8。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- SCOPE_ROW / BIOPATH150_094：094必答为雄酮至雄烯二酮两步S02-&gt;S03，睾酮入口S01为背景不要求
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案包含两步主链、酶/EC、微生物及15项性状字段
- RUBRIC_CLAUSE / TABLE0_D1：D1完整性与任务符合度档位锚点

</details>

### D2 反应化学科学性：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 第一步雄酮C3氧化为5alpha-雄烷-3,17-二酮与参考S02一致；第二步生成雄烯二酮并到达题面终点，主链连续。缺陷是第二步写成isomerization且未列氧化型电子载体，按局部化学/计量缺陷处理，不判主链断裂，故取7。

<details><summary>V0.4理由与本行变化背景</summary>

D2取7–8档：S1 Androsterone→5alpha-androstan-3,17-dione与gold S02的Androsterone→Androstanedione一致；S2净底物/产物5alpha-androstan-3,17-dione→Androstenedione与gold S03的Androstanedione→Androstenedione一致，方向正确、连接连续，且止于题面终点。辅因子/电子载体未列入主底物-产物属局部计量缺陷，不单独cap；反应类型与酶标注错误另计入D3a。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02雄酮-&gt;Androstanedione；S03 Androstanedione+氧化载体-&gt;Androstenedione
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S1-S2的底物/产物与反应类型
- RUBRIC_CLAUSE / TABLE0_D2：D2主链化学、方向、连续性与局部计量缺陷锚点

</details>

### D3a 目标反应与酶对应：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> S1对应S02，3alpha-hydroxysteroid dehydrogenase EC 1.1.1.50属于参考S02所列EC备选，目标功能可支持。S2对应S03却用3-oxo-5alpha-steroid Delta4-isomerase EC 5.3.3.12；参考S03为3-keto-5alpha-steroid Delta4-dehydrogenase EC 1.3.99.5，并以氧化型电子载体完成脱氢生成Δ4双键，isomerase类别与目标反应不相容。S03为TERMINAL关键步，构成D-KEY4受限，两个目标中一个可用、一个关键失败且边界清楚，取4。

<details><summary>V0.4理由与本行变化背景</summary>

D3a触发关键错误cap≤4：S1的3alpha-hydroxysteroid dehydrogenase EC 1.1.1.50与gold S02多EC集合相容；但S2把5alpha-androstane-3,17-dione→androst-4-ene-3,17-dione的净脱氢/去饱和反应标为isomerization，并给出isomerase EC 5.3.3.12；该酶不能引入C4–C5双键，gold S03为3-keto-5alpha-steroid Delta4-dehydrogenase EC 1.3.99.5。该核心步骤的酶-反应推荐失效，故cap≤4；S1正确，档内取4。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED;TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_094：S02酶含EC 1.1.1.50备选；S03目标酶为3-keto-5alpha-steroid Delta4-dehydrogenase EC 1.3.99.5
- GOLD_SLICE / source_reaction_records.tsv#case:BIOPATH150_094：BSY-r03042为5alpha-androstanedione + oxidized electron carrier -&gt; androstenedione + reduced carrier
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案S2给出的isomerase/EC5.3.3.12及isomerization反应类型
- RUBRIC_CLAUSE / C03/C04-USER-D-KEY4/C05：D3a五态分类、KEY失败上界与受限档内判据

</details>

### D3b 微生物身份与能力：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案在两个必答步骤均使用Comamonas testosteroni，与参考organism_gold的物种级匹配一致，且同一菌已去重为一个profile；未作不同菌株或跨类群错误声称。未给菌株/TaxID、能力依据仅为内部知识，属主要对应可靠但少量条目仍待确认，取8。

<details><summary>V0.4理由与本行变化背景</summary>

D3b取7–8档：两步均指向Comamonas testosteroni，gold organism S01–S03为EXACT，且PATHWAY_COMPLETE taxid 285=TRUE，支持该物种参与该路线。答案未给菌株与TaxID，属物种级粒度而非身份错配；未把单步能力写成无关类群能力，故不cap，取8。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_094：S02、S03两必答步均匹配Comamonas testosteroni，TaxID 285
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案两步骤均写Comamonas testosteroni并引用同一ORG_001
- RUBRIC_CLAUSE / P69/P106-P110：D3b身份、单步能力、整路径能力分层及身份阶梯

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 已给出的运动性motile、杆状、Gram-negative、非产孢等与参考观测一致，部分氧/呼吸描述亦合理；但F2温度、F5保藏号、F14基因组、F4盐度、F3 pH均为null，F1写aerobic而参考观测为aerotolerant，且若干已填性状仅内部知识/低置信。属部分性状准确但关键项证据不足，取6。

<details><summary>V0.4理由与本行变化背景</summary>

D4取5–6档：已给性状中F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming与gold observed一致；F8/F9与路径中甾体降解及3alpha-HSD活性相符。但F1写作aerobic，gold observed为aerotolerant，不完全对齐；F6无observed支持；F2/F3/F4/F5/F14为null，关键性状证据与条件说明不足。缺失完成度主归D1，D4按已给内容与适用性取6。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_094：参考观测：motility=true、rod-shaped、gram positive=false、sporulation=false、F5 JCM 6233、F2 min10/max37等
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_094：F2/F5/F10-F14可评分，F3/F4/F6/F15仅completeness或不可评分
- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案15项性状的填写值与null分布
- RUBRIC_CLAUSE / P111-P115：D4性状正确性、适用性、honest null与关键缺口处理

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> evidence_registry三条均为INTERNAL_KNOWLEDGE_ONLY，database/record_id为null，locator只是内部知识描述，无法定位到条目或文献；步骤、酶、菌和性状的关键结论均缺少可核外部来源。按MISSING_SOURCE低档处理，无已核实错引cap；有内部claim映射但无可定位来源，取2。

<details><summary>V0.4理由与本行变化背景</summary>

D5取1–2档：路径、酶、微生物与性状的关键结论均只挂到EVID_001/EVID_002/EVID_003，而三条来源的source_type全为INTERNAL_KNOWLEDGE_ONLY，无数据库条目、DOI、文献定位或计算记录可沿记录核对。属MISSING_SOURCE低分档；默认不触发已核实错引cap，故key_error=N。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：EVID_001-EVID_003均source_type=INTERNAL_KNOWLEDGE_ONLY且无database/record_id
- RUBRIC_CLAUSE / P34/P41：INTERNAL_KNOWLEDGE_ONLY归MISSING_SOURCE，D5低分档且默认不cap；decision-relevant组无条目级可核来源

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案列出uncertainties，对第二步EC/菌株归属仅内部知识、15项性状多数无来源、许多null作了披露，并普遍使用low/unknown；但同时把内部知识支撑的酶/菌标为medium，且未识别第二步isomerase与目标脱氢反应的类别冲突。属有不确定性说明但部分结论强度仍超过依据，未达系统性误导，取6。

<details><summary>V0.4理由与本行变化背景</summary>

D6取7–8档：答案用low/medium/unknown与null区分未知，uncertainties明确列出EC/菌株未附原始文献、多数性状缺来源、辅因子未列；没有系统性把预测写成实证。但未披露S2酶-反应机制疑点及题面/gold终点冲突，故取档内中位7。

背景标签：USER_APPROVED_REFERENCE_SCOPE_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：uncertainties及confidence标注显示部分未知/低置信，但关键酶/菌仍标medium
- RUBRIC_CLAUSE / P118-P121：D6单点过度确信与系统性误导分开；置信需与证据相称

</details>

## Grok

答案SHA256：`0f7b0715b7a0297007b543b46d5f5ac1f848fbd11382720906e1a12b4a57103a`。

复审/来源说明：用户2026-11-15明确确认060四步/094两步范围后首次评分；采用独立修正参考版本，原题与原答未改。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 在程序给定D1区间内按可核内容取4。必答雄酮支路S1→S2与背景睾酮支路S3均有交付，且步骤、酶、菌、证据字段均有内容；但答案把背景睾酮入口作为并列主支路，并明确is_single_continuous_route=false，未形成题面主链要求的单一连续主链表述；同时15项性状中F2/F3/F4/F14/F15等为null，完整性/任务符合度只能到较弱档上沿。

<details><summary>裁判引用及其声称的支持范围</summary>

- SCOPE_ROW / BIOPATH150_094：094必答雄酮至雄烯二酮两步，睾酮入口仅背景；未答背景不扣分
- GOLD_SLICE / SCOPE_ROLES.tsv#case:BIOPATH150_094：S02为REQUIRED/ENTRY，S03为REQUIRED/TERMINAL，S01为BACKGROUND_NOT_REQUIRED
- ANSWER_TEXT / steps.S1-S3;traits：答案实际交付的步骤、分支声明及性状null分布
- RUBRIC_CLAUSE / P99-P101：D1评价任务模块完成度、路线/条件遵守与交付完整性

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 主链所需S02/S03的底物-产物方向与脱氢/Δ4-脱氢化学基本成立，S1与S02在底物和产物上匹配；但S2的雄烯二酮SMILES被程序标为STEREO_CONFLICT_SPECIFIED，显式立体化学存在冲突，按C06显式立体冲突候选≤5。背景S3化学可行但不替代主链。因存在已指定立体冲突且无额外高分证据，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02为androsterone→androstanedione，S03为androstanedione→androstenedione，方向为SUBSTRATE_TO_PRODUCT
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_094：题名终点为Androstenedione
- ANSWER_TEXT / steps.S2.products：S2产物SMILES与gold androstenedione存在显式立体冲突标记
- RUBRIC_CLAUSE / C06：D2显式立体冲突候选≤5；仅缺步不另用覆盖率硬换分

</details>

### D3a 目标反应与酶对应：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 两个必答目标反应酶候选均与gold匹配：S1对应S02的3alpha-hydroxysteroid dehydrogenase，EC 1.1.1.50属于gold多EC集合；S2对应S03的3-keto-5alpha-steroid Delta4-dehydrogenase，EC 1.3.99.5完全一致；背景S3的EC 1.1.1.51对应S01。S2标注medium并说明推断，但gold对C. testosteroni有同一酶记录。无已核酶-反应矛盾；按证据门上沿8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_094：S02酶含EC 1.1.1.50，S03酶为EC 1.3.99.5，S01酶为EC 1.1.1.51
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：目标反应S02/S03的催化边界
- ANSWER_TEXT / steps.S1-S3.enzyme：答案实际填写的酶名、EC与置信度
- RUBRIC_CLAUSE / C02/C03/C05：目标功能/EC支持、S/F/M/U分类与D3a档内判据

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所有步骤均写Comamonas testosteroni，TaxID 285，与organism_gold的STEP物种级记录一致；S1/S2/S3的物种-步骤关联均有gold支持。但答案进一步写菌株ATCC 11996，gold冻结记录只到物种级（285；基因组GCA_016599875.1未在本答案中用于菌株级身份），属物种级支持菌株级声称的粒度不足，按P107档内扣、不cap。取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_094：三步均由Comamonas testosteroni TaxID 285的STEP记录支持，物种级
- ANSWER_TEXT / steps.microorganism;ORG_001：答案声称菌株ATCC 11996并给TaxID 285
- RUBRIC_CLAUSE / P69/P106-P110：D3b身份阶梯：物种级支持菌株级声称通常档内扣、不自动cap

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 部分性状与gold可核项一致或相容：F10运动true、F11杆状、F12革兰氏阴性、F13不产芽孢；F5为C. testosteroni常用保藏号（ATCC 11996，gold记JCM 6233同物种代表）。但F2温度、F4盐度、F14基因组等可评分关键项均null，F7/F8/F9等仅为内部知识且未被冻结性状证据直接覆盖；按D4关键项证据不足/条件解释需修订，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_094：F2温度、F4盐度、F5保藏、F10-F13等观测/预测值
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_094：F2/F4/F7/F8/F9/F14为可评分observed_accuracy或completeness_only边界
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_094：F2/F4可评分子字段与gold标量
- ANSWER_TEXT / ORG_001.traits：答案实际填写的性状值与null分布
- RUBRIC_CLAUSE / P112-P115：D4按已给内容、关键缺口与适用性评定，诚实null与编造区分

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry全部为INTERNAL_KNOWLEDGE_ONLY，无database、record_id、DOI或稳定链接；虽然给出claim_scope和文字locator，但均为答案内部自述，不能沿外部可定位条目核对。按MISSING_SOURCE低分档，且无已核实错引，不cap。取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：五条证据均为内部知识自述，无外部记录号/链接
- RUBRIC_CLAUSE / P33-P42：D5六状态与MISSING_SOURCE低分档；INTERNAL_KNOWLEDGE_ONLY默认不触发关键错误cap

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> uncertainties明确列出题面androstendione解释、Δ4酶基因/电子受体未核实、NAD SMILES缺失、温度/pH等null、SMILES未逐条复核、证据均为内部知识；主要限制和未知已具体披露，未系统性把预测写成实证。但部分酶/菌/性状仍给high confidence而仅靠内部知识，属有限过度确信，取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties;evidence_registry：答案对内部知识、未核实字段、null与解释边界的披露
- RUBRIC_CLAUSE / P119-P121：D6单点过度确信与系统性误导分开；D5错引不自动使D6 cap

</details>

## GPT5.6

答案SHA256：`baa00dd96e077394bbed87429f11ab0497f4a654c82d274b8f3fb4bb01dc818a`。

复审/来源说明：用户2026-11-15明确确认060四步/094两步范围后首次评分；采用独立修正参考版本，原题与原答未改。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> JSON可解析且含路线、酶、菌与15项性状；route_scope原样填写指定好氧路线名。但任务范围要求雄酮经S02→S03两步至雄烯二酮，答案S1把雄酮直接写成雄烯二酮，S2为睾酮背景分支，缺S02产物雄烷二酮和S03转化；未答背景不扣分，但实际目标主链只覆盖一个被错误合并的必需步，属严重路线偏离。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / BIOPATH150_094：题面指定route_scope为testosterone and androsterone degradation to androstendione (aerobic)，要求主链。
- SCOPE_ROW / BIOPATH150_094：required_step_ids=S02|S03，n_required=2；S01睾酮为背景不要求。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02 Androsterone→Androstanedione；S03 Androstanedione→Androstenedione；S01 Testosterone为背景。
- ANSWER_TEXT / steps&#91;0&#93;：S1把Androsterone直接转为Androstenedione并用EC 1.1.1.50。
- ANSWER_TEXT / steps&#91;1&#93;：S2为Testosterone→Androstenedione背景分支；无Androstanedione/EC 1.3.99.5步骤。
- RUBRIC_CLAUSE / C01：指定路线/允许主链不可改选，漏必经转化为交付缺失。

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1 Androsterone→Androstenedione用3α-HSD EC 1.1.1.50，但该酶只催化3α-OH→3-酮生成雄烷二酮，不能产生Δ4双键；答案把S02与S03合并为单酶反应并省略雄烷二酮，属首步酶-产物不符/无依据跳步。S2睾酮→雄烯二酮用17β-HSD作为背景分支化学上可成立，但不补目标主链；无辅因子标注为局部缺陷。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02为Androsterone→Androstanedione，S03为Androstanedione→Androstenedione。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_094：S02可接受酶含3alpha-hydroxysteroid dehydrogenase/carbonyl reductase；S03为3-keto-5alpha-steroid Delta4-dehydrogenase EC 1.3.99.5。
- GOLD_SLICE / source_reaction_records.tsv#case:BIOPATH150_094：BSY-r02482为androsterone 3-dehydrogenase生成Androstanedione；BSY-r03042为5alpha-androstanedione→androstenedione。
- ANSWER_TEXT / steps&#91;0&#93;：答案称EC 1.1.1.50直接生成Androstenedione。
- RUBRIC_CLAUSE / P99：D2评反应化学本身，包括方向、结构、连续性与无依据跳步。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按C03逐目标反应：S02需雄酮→雄烷二酮，答案S1用EC 1.1.1.50（金标S02可接受酶之一）但产物写成雄烯二酮，目标反应未完成；S03需雄烷二酮→雄烯二酮/EC 1.3.99.5，答案无该步，记M。S=0,N=2，C=0&lt;0.20→&#91;1,2&#93;；S1保留正确底物和3α-HSD局部信息故取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_094：S02主产物Androstanedione；S03主产物Androstenedione。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_094：S02可接受酶含1.1.1.50；S03酶为EC 1.3.99.5。
- GOLD_SLICE / source_reaction_records.tsv#case:BIOPATH150_094：BSY-r02482为androsterone 3-dehydrogenase；BSY-r03042为5alpha-androstanedione Δ4-dehydrogenase。
- ANSWER_TEXT / steps&#91;0&#93;：S1给出Androsterone与EC 1.1.1.50，但产物错误。
- RUBRIC_CLAUSE / C03：目标反应未完成/缺失按F/M登记，C=S/N选择分带。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案用Comamonas testosteroni ATCC 11996，与金标物种Comamonas testosteroni/TaxID 285一致；但金标仅为物种级/基因组GCA_016599875.1，ATCC 11996菌株身份、反应级能力和complete_pathway_organism_profile_id均无本材料可定位证据，source_pathway_annotations旧PATHWAY_COMPLETE不自动证明修正全链。属合理物种候选、部分支持，关键菌株/全链能力未充分核验，5-6档取6；无已核身份错误故不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_094：三个STEP的matched_organism_name为Comamonas testosteroni，TaxID 285，genome GCA_016599875.1；未给ATCC 11996菌株级匹配。
- GOLD_SLICE / source_pathway_annotations.tsv#case:BIOPATH150_094：PATHWAY_COMPLETE为旧路径级标签，TaxID 285存在；任务说明明确不自动证明修正后全链能力。
- ANSWER_TEXT / ORG_001：声称Comamonas testosteroni ATCC 11996并作为complete_pathway_organism_profile_id。
- RUBRIC_CLAUSE / P69：身份定位、单步反应能力、完整路径能力三层分开核验。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项均出现；F1/F5/F7/F8/F9有内容，但F2/F3/F4/F6/F10-F14大量null或仅低置信泛化。金标可评分项如F2 min 10/max 37、F10运动true、F11杆状、F12 Gram阴性、F13不产孢、F14基因组GCA_016599875.1等，答案未给或仅给模糊描述；F5给ATCC 11996而金标观测记录为JCM 6233，未核验不判错。没有已核数值离谱或把预测冒充观测；主要问题是关键性状证据不足/缺失，按5-6档取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_094：提供C. testosteroni的F1 aerotolerant、F2温度10-37、F5 JCM 6233、F10 motility true、F11 rod-shaped、F12 Gram negative、F13 sporulation false、F14 genome GCA_016599875.1等观测/预测记录。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_094：F1/F2/F5/F7/F8/F9/F10-F14等为scoreable或completeness_only的登记依据。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_094：F2 minimum_c=10、maximum_c=37为可评分观测子项；optimum_c无观测来源。
- ANSWER_TEXT / ORG_001：答案性状字段的null、模糊值及置信度。
- RUBRIC_CLAUSE / P112：诚实null与编造区分，D4按已给内容、关键缺口与适用性评定。

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry有3条并按EVID_001/002/003回指step/菌/酶，但EVID_001/003仅database=文献报道、record_id/locator均null，EVID_002虽有ATCC 11996但无locator；结论与来源只能到笼统文献/库名层，无法沿稳定条目核对。决策相关路线/酶/菌组均只有GENERIC_SOURCE，无已核错引，按3-4档取4；不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / evidence_registry：证据条目字段显示只有笼统库名/文献报道，缺少可定位记录。
- RUBRIC_CLAUSE / P33：D5按claim group登记六状态，区分MISSING/GENERIC/UNRESOLVED/错引。
- RUBRIC_CLAUSE / P35：决策相关组全部仅笼统来源时进入3-4档；条目级可核对才进5-6档。
- RUBRIC_CLAUSE / P41：D5档位由决策相关组状态构成，SUPPORTING组不得跨档上调。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> uncertainties明确列出直接底物-产物/菌株酶学配对有限、基因蛋白基因组未核实、多数性状缺单一最强来源；各trait大量null/unknown，confidence多为low/unknown，未把预测系统性写成实测。部分medium证据（EVID_001/002/003）仍偏强，但属局部过度确信，非系统性误导；7-8档取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / uncertainties：明确披露底物-产物配对、基因/蛋白/基因组及性状来源不确定性。
- ANSWER_TEXT / ORG_001：大量性状为null/unknown/low，未系统冒充观测。
- RUBRIC_CLAUSE / P119：单点过度确信与系统性误导分开；前者档内扣，后者才是cap候选。
- RUBRIC_CLAUSE / P121：D5错引不自动使D6 cap，D6按证据性质表述独立定档。

</details>
