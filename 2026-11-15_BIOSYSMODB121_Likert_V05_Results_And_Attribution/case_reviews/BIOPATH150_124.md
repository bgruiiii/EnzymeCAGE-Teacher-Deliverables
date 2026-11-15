# BIOPATH150_124：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：2-methylpropene degradation

污染物：Isobutylene；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 44.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 44 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 49.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 37 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 41 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 40.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`22780ff08d0581f79a4f89842112ba5e605a3028d79e627d5e9a491f7e424011`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分9 → V0.5新分4，变化-5。

新裁判理由：

> 交付层面完整：8步均给出底物/产物/SMILES、酶/EC、对应微生物，4个organism_profiles各含15项性状，并有evidence_registry与uncertainties。但冻结路线诊断为DEVIATES，且D1任务允许区间为&#91;1,4&#93;；在该受限区间内取4，因为模块完整但路线级符合度已受冻结诊断限制，不能按完整合规高档处理。

<details><summary>V0.4理由与本行变化背景</summary>

题面要求逐项实质回应：8步主链均给出主底物/主产物英文名与SMILES、一个首选酶、一个对应微生物并引用profile；route_scope.chosen_route_name原样填写题面指定路线名，无改选；4条profile按“物种+菌株”去重（Py2/AD1/PM1/L108），各含全部15项性状（11项有效填写、4项以value全null+confidence=unknown明确未知，无遗漏）；另附evidence_registry、central_metabolism_entry与uncertainties。扣分点：S5 连接酶 EC 按题面允许置null但属一个必填子字段未实质作答；S8 产物数组仅列1分子acetyl-CoA（反应类型文字写明两分子）；各步ncbi_taxid全null（题面允许，不计为编造）。整体无重要遗漏或范围偏离，取9档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_124：冻结formal_cases给出8步、LINEAR_UNIQUE及题面路线；不等于答案化学每一表示均匹配。
- ANSWER_TEXT / ANSWER.steps; ANSWER.organism_profiles; ANSWER.evidence_registry：显示答案确实交付8步、4个菌株profile、15项性状及来源登记。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> 主链碳骨架顺序总体连贯：环氧化、环氧水解、两级氧化、CoA连接、变位酶重排、β-氧化到乙酰-CoA，方向为降解方向。但冻结诊断将S04/S05/S06/S08判为NONMATCH，理由含立体/表示冲突；S8反应类型称生成两分子乙酰-CoA而products只列一个乙酰-CoA，存在局部计量/表示问题。D2允许区间&#91;1,5&#93;，主干部分成立但关键中间体与连接仍需修订，取5。

<details><summary>V0.4理由与本行变化背景</summary>

逐步核对主链化学：S1 末端烯烃环氧化（O2/NADH参与）→S2 环氧化物水解→S3 伯醇脱氢→S4 醛脱氢成酸→S5 CoA硫酯化（ATP/CoA→AMP+PPi）→S6 B12依赖变位重排→S7 β-羟基酰基-CoA脱氢→S8 硫解，方向、主产物身份与SMILES均正确，且与gold线性主链同序（S03→S07→S01→S02→S04→S08→S05→S06），终点acetyl-CoA与gold terminal一致，另将TCA下游单列为downstream_continuation而未混入主链。局部缺陷：S1缺H+（辅因子/计量层面）、S8产物数组只列1分子acetyl-CoA（文字写明两分子），属局部计量与呈现问题，按辅因子条款在7–8档内处理、不cap；但全链证据为类比重构、答案自述证据水平偏低，故取8而非更高。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：冻结gold给出每步有向底物/产物与立体表示；用于核对主链方向与结构。
- ANSWER_TEXT / ANSWER.steps S1–S8：显示答案提交的转化、方向、SMILES及products数量。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：提供gold步骤相关酶/EC背景，不证明答案每一步的表示均等价。

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 按冻结target映射：S=1（S03入口环氧化），F=4（S04、S05、S06、S08，含KEY终端），U=3（S01、S02、S07），N=8；confirmed_target_rate=0.125。已确认KEY失败触发D-KEY4上限4，故只在&#91;1,4&#93;内取分。只有入口一个主要目标获支持，多数必答主链目标已失败或待核，主功能严重受损且可用/失效边界有限，取3。

<details><summary>V0.4理由与本行变化背景</summary>

关键步骤的酶功能与反应类型逐一对应成立：S1 烷烯单加氧酶 EC 1.14.13.69（与gold一致）；S2 环氧化物水解酶（功能正确，但EC 3.3.2.3为撤转历史号，gold为现行3.3.2.10）；S3 醇脱氢酶 EC 1.1.1.1、S4 醛脱氢酶 EC 1.2.1.3 均为通用号（gold为更专一的1.1.1.400/1.2.1.98），答案自述“通用编号、非底物专一酶”；S5 连接酶EC按实际未知置null并说明；S6 变位酶 EC 5.4.99.64+hcmA/hcmB（与gold一致，且自标“凭记忆待核”）；S7 EC 1.1.1.35（与gold一致）；S8 EC 2.3.1.9 落在gold多注集合 2.3.1.16|2.3.1.9 内，按多注条款不扣。故主要步骤酶对应有可靠支持、但多处需进一步确认（通用号2处、撤转号1处、缺失号1处），取7档；这些EC在E0中无记录或仅TRANSFERRED状态，属UNRESOLVED、不判虚构、不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：用于定位8个必答目标的有向反应及终端；不扩展支持答案的未核U步骤。
- ANSWER_TEXT / ANSWER.steps S1–S8：显示答案对S01–S08目标步骤的酶/反应/表示及S8终端产物。
- E0_EVIDENCE / f3e0:ec:3.3.2.3：官方EC 3.3.2.3为TRANSFERRED并拆分；只登记历史状态，不确认当前步骤催化，也不判答案虚构。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> 答案给出4个真实可辨认的菌名/菌株，并未把任一菌写成完整路径菌（complete_pathway_organism_profile_id=null）。但步级微生物归属大多只有内部推断：Xanthobacter Py2、Agrobacterium AD1无冻结记录；Methylibium petroleiphilum虽在gold出现，但答案把它分配给S3/S4而非其gold对应步；Aquincola L108的mutase步有gold支持，但把CoA连接酶和β-氧化步也归于该菌缺乏当前证据。属合理候选与部分支持并存、多个关键步级归属待核，取5。

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份层：四个指派均为真实物种/菌株（Xanthobacter autotrophicus Py2、Agrobacterium radiobacter AD1、Methylibium petroleiphilum PM1、Aquincola tertiaricarbonis L108），无一编造，TaxID/保藏号/基因组号一律null而未虚构编号；S6变位酶菌与gold一致（Aquincola tertiaricarbonis，gold TaxID 391953），S3/S4菌与gold的Methylibium petroleiphilum部分吻合。能力层：答案全程只声明单步催化并明确“菌株在步骤间不连续”“多数步骤为类比推断”，未把单步菌写成整条路径菌，未由序列存在性外推路径能力。不足：S1对支链末端烯烃、S2对2,2-dimethyloxirane、S5 CoA活化步骤的菌-反应对应均属类比外推且无可定位来源；S4/S5步级归属与gold不同（gold该步为Methylibium petroleiphilum），属未见正反证据的替代候选。故按“主要微生物对应及身份有可靠支持、若干具体条目需确认”取7档，不cap（身份未错配、能力主要推荐未被推翻）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_124：列出gold步级菌株及TaxID；不证明答案所用的其他菌株不能催化同一步，但可用于核对归属粒度。
- ANSWER_TEXT / ANSWER.organism_profiles; ANSWER.steps&#91;*&#93;.microorganism：显示答案的菌名/菌株、对应步骤及confidence；complete_pathway为空。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 4个profile均填满15项外壳，未知项多数用null，未把null伪装成观测。Methylibium与Aquincola的部分粗粒度性状有gold支持（如革兰氏阴性、不产芽孢、Methylibium杆状）；但Xanthobacter与Agrobacterium性状无冻结记录，温度/pH/盐度数值多留null，功能/栖息地描述多为内部推断。Aquincola F11写成杆状，而gold记录为oval-shaped，属局部性状冲突。整体为部分准确、关键证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

已填写性状的定性部分大体准确且适用：四菌氧需求“好氧/专性需氧”、革兰氏阴性及门级归属（α-/β-变形菌）、产孢阴性、杆状形态、PM1降解MTBE/TBA、L108经2-hydroxyisobutyryl-CoA变位酶支路等均与已知菌学一致；未出现“预测值冒充观测值”或数量级离谱的数值。问题：(1) 关键定量性状普遍缺失——F2温度数值、F3 pH、F4盐度数值、F14基因组、F5保藏号全部null（按P112缺失的完成度扣分主归D1，D4按已给内容与关键缺口评定）；(2) 已核实错值1处：A. tertiaricarbonis L108 细胞形态填“杆状”，冻结gold记录为 oval-shaped（OBSERVED）；(3) 多数性状来源为INTERNAL_KNOWLEDGE_ONLY、无外部条目，且同一evidence在性状字段标medium而在注册表标low，适用性与证据强度偏弱。综合取“部分性状准确且适用、关键项证据不足”档=6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_124：提供Methylibium、Aquincola等已观测性状；不覆盖Xanthobacter/Agrobacterium全部性状，也不把预测子字段当观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_124：标明部分性状仅completeness_only或待裁定，不能作为数值准确性分母。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;*&#93;.traits：显示答案具体性状值、null、confidence及internal evidence_id。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分3 → V0.5新分1，变化-2。

新裁判理由：

> D5按答案实际交付的来源记录评价。EVID_001–EVID_009全部为INTERNAL_KNOWLEDGE_ONLY，database、record_id、locator均为null；S1–S8与ORG_001–ORG_004仅指向这些内部自声明ID，没有任何可定位文献、数据库条目或计算记录。决策相关结论几乎全部无法沿来源核查，属MISSING_SOURCE低分档；因未交付可核外部引用，按1-2档下沿取1。没有已核实错引，故不触发D5关键错误cap。

<details><summary>V0.4理由与本行变化背景</summary>

逐claim group核对：evidence_registry 共9条，source_type全部为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全为null，无任何可定位文献、数据库条目或计算记录→按六状态全部组登记MISSING_SOURCE。答案用evidence_id+claim_scope建立了内部映射（可读性优于纯无引用），但无法外部追查，决策相关组（CORE/APPLICATION_CRITICAL）同样无条目级可核对证据，故落低分档=3。MISSING_SOURCE属缺失而非误导，默认不触发cap。EC 3.3.2.3虽经E0核为TRANSFERRED（2006删除、拆分3.3.2.9/3.3.2.10），但该号历史存在、答案以内部知识而非数据库引用形式交付，按P73登记为历史分类问题，不判虚构、不构成已核实错引，故D5_SEVERITY=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / B480-0401：显示所有证据条目均为INTERNAL_KNOWLEDGE_ONLY且无database/record_id/locator；仅用于D5来源可追溯性评价，不证明科学正确性或错误。
- RUBRIC_CLAUSE / P34：仅有INTERNAL_KNOWLEDGE_ONLY自我声明属MISSING_SOURCE，D5按低分档评定，默认不cap。
- RUBRIC_CLAUSE / P41：D5按决策相关claim group的来源状态构成定档；支持组条目不能跨档上调。

</details>

### D6 不确定性与诚实度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 答案对证据性质与边界披露充分：route_summary明确多数步骤为类比推断、整体证据水平偏低；uncertainties逐项列出S1底物特异性、S2类比、S3/S4通用EC、S5 EC缺失、S6 EC凭记忆建议核对、S7/S8未在菌株层面确证、TaxID/保藏/基因组因不确定置null。未把预测系统性写成实证，也未掩盖主要矛盾。D6按披露质量取9；D5来源缺失不自动使D6 cap。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体优良：route_summary明示“主链由两段既有证据重构拼接、菌株在步骤间不连续、整体证据水平偏低”；每步uncertainty具体（S1底物特异性未验证、S2类比指派、S3/S4通用EC非专一酶、S5 EC与基因未知故置null、S6 EC凭记忆待核且立体化学未定、S7/S8未在菌株层确证）；uncertainties另列9条，含“各菌株性状大多缺乏原始文献、仅按一般细菌学常识填写、缺失项如实置null”；未把预测/推断写成实证观测，未掩盖主要限制；alternative_branches以is_part_of_scored_main_route=false明确排除，范围声明规范。扣分点：部分仅内部常识支撑的性状字段标 medium confidence（如F1/F6/F12），而对应evidence_registry条目confidence注册为low，置信表达与证据强度存在轻度不一致——属单点/局部包装偏强，非系统性误导，档内扣分不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties; ANSWER.route_summary：显示答案明确区分推断、记忆值、未知及待核对点；不证明其科学内容正确。

</details>

## DeepSeek

答案SHA256：`5daa2bb9d9339330b448fa3826170e76290f11afbf70b607374c0d63d1594456`。

### D1 完整性与任务符合度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案按题面给定路线名填写，交付6步，每步有底物/产物、酶对象和微生物引用；15项性状字段齐全但全部为null。Gold任务为LINEAR_UNIQUE且ordered_step_count=8；答案止于3-hydroxybutyryl-CoA，缺少acetoacetyl-CoA及terminal acetyl-CoA相关必答步，主要模块覆盖但不完整，落在5–6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

路径S1–S6、每步酶与对应菌均实质交付且关联清楚（底物/产物/SMILES/酶/菌齐全），但15项性状全部为null（明确未知、无一项填数），主链止于3-羟基丁酰辅酶A、未至gold终止物acetyl-CoA（缺后2步），evidence_registry为空。属主要模块均有涉及但必要内容实质遗漏，落5–6档，档内偏低取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv：BIOPATH150_124为LINEAR_UNIQUE，ordered_step_count=8
- GOLD_SLICE / reaction_gold.tsv：gold主链含S05/S06至terminal acetyl-CoA；答案未覆盖该下游段
- ANSWER_TEXT / ANSWER：交付6步，止于3-hydroxybutyryl-CoA；无acetoacetyl-CoA/acetyl-CoA步骤；15项性状均为null
- QUESTION_TEXT / QUESTION：要求主链、逐步酶/微生物、15项性状；未知项允许null

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 已交付的6个反应按异丁烯→2,2-dimethyloxirane→2-methylpropane-1,2-diol→2-hydroxy-2-methylpropanal→2-hydroxy-2-methylpropanoate→2-hydroxyisobutyryl-CoA→3-hydroxybutyryl-CoA排列，化学转化与gold前段一致；NAD+/ATP/CoA及部分CoA SMILES未列，按局部计量/表达缺陷处理，不推翻主链化学结论。缺失下游步主要由D1完整性承担，不在D2按覆盖率硬扣；D2允许上限为8，9–10门未开。

<details><summary>V0.4理由与本行变化背景</summary>

S1环氧化→S2水解→S3/S4两步氧化→S5 CoA活化→S6变位酶重排，主底物/主产物身份、SMILES、方向与顺序与gold线性步1–6一致，无起始步错误、无方向反转、无原子明显不守恒。全程缺辅因子（O2、NAD(H)、ATP、CoA、H2O）标注属局部计量缺陷（7–8档内）；止于3-羟基丁酰辅酶A且题面未指定终点，属覆盖问题记D1，不作D2化学错误。故取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：6步反应化学连续：环氧化、环氧化物水解、二醇氧化、醛氧化、CoA活化、变位酶重排；辅因子缺失，部分SMILES为null
- GOLD_SLICE / reaction_gold.tsv：gold主链前段的反应顺序与方向支持S03→S07→S01→S02→S04→S08
- GOLD_SLICE / case_root_identity.tsv：污染物为Isobutylene，路线名为2-methylpropene degradation

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分7 → V0.5新分2，变化-5。

新裁判理由：

> 按C03/C04计：N=8；S=1（S03 alkene monooxygenase EC 1.14.13.69 为CONFIRMED_TARGET/SUPPORTED）；M=3（S05、S06、S08按冻结矩阵为MISSING/未绑定交付）；U=4（S01、S02、S04、S07为UNRESOLVED_NONACCEPTED或ROUTE_HOLD_REPRESENTATION）；F=0，H=0。C=1/8=0.125。仅一个已核目标功能可用，且terminal/key段缺失使主推荐不可用；按C05的2分锚点：少量已核功能/局部信息有用，但核心目标推荐仍失效，故给2。EC 5.4.99.3等无冻结记录者保持UNRESOLVED，不据此判Y。

<details><summary>V0.4理由与本行变化背景</summary>

S1烯单加氧酶EC 1.14.13.69与gold一致；S3/S4/S6酶名与gold逐字吻合；S2环氧水解酶命名对应gold 3.3.2.10（E0载3.3.2.3为已撤转、拆分为3.3.2.9/3.3.2.10）。S2–S5缺EC，S6所填EC 5.4.99.3与gold 5.4.99.64不符且E0无冻结记录→UNRESOLVED（不判错）。主要酶-反应对应可靠、仅少量条目需确认，取7；无经核实关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv：gold各必答步酶/EC：S03 alkene monooxygenase EC 1.14.13.69；S01/S02/S04/S07相应酶名/EC；S05/S06/S08存在必答酶记录
- GOLD_SLICE / reaction_gold.tsv：gold主链含S05、S06至acetyl-CoA terminal；答案未交付该下游段
- ANSWER_TEXT / ANSWER：S1有EC 1.14.13.69；S2-S5 EC为null；S6标5.4.99.3；未给S05/S06相应反应步骤

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分7 → V0.5新分4，变化-3。

新裁判理由：

> Mycobacterium sp. ELW1身份真实且对S01/S02/S03/S07等部分步骤有支持，但答案把ORG_001标为complete_pathway_organism_profile_id并令同一ELW1覆盖全部6步；冻结organism_gold的PATHWAY_COMPLETE行对TaxID 1547487为FALSE，且S04/S08步骤归属分别指向Methylibium petroleiphilum与Aquincola tertiaricarbonis。把单步/部分支持写成整条路径能力，属D3b关键错误，按3-4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

微生物身份Mycobacterium sp. ELW1与gold organism一致（TaxID 1547487），gold PATHWAY_COMPLETE对该菌记pathway_complete=TRUE，支持其整路径能力；但S5/S6步级归属统归ELW1，而gold步级来源为Methylibium petroleiphilum与Aquincola tertiaricarbonis，答案未给步级能力证据（UNRESOLVED，不判错）。主要身份与整路径能力有可靠支持、仅少量具体条目待确认，取7；无经核实关键错误。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_124：确认ELW1的TaxID身份及部分步骤归属；PATHWAY_COMPLETE行显示1547487 pathway_complete=FALSE；S04/S08的step归属非ELW1。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：给出各步酶与organism_gold的关联背景；不支持将单一ELW1扩展为全部步骤的完整路径菌。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 15项性状字段虽全部出现，但value全为null、confidence=unknown，filled=0、explicit_unknown=15；按量表P44，全部必需性状均为null/空值按D4 MISSING=1处理，不宣称检测到具体科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

本题要求15项性状；答案唯一profile（Mycobacterium sp. ELW1）的F1–F15全部为value=null、confidence=unknown，未交付任何可评价的性状数值或描述。按量表四.4（全部必需性状均为null/空值时D4记MISSING=1，不宣称检测到科学错误）执行。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：确认15项性状均以null/unknown交付；不支持任何性状数值或来源已交付。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_124：显示多组性状观测可计分/仅完整性计分的背景；不把答案null回填为观测值。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> evidence_registry为空，所有step/trait/evidence_id均为null，无DOI、数据库条目、计算记录或原文定位；路径、酶、菌和性状均无法沿答案自身记录追查。属MISSING_SOURCE低分档；未见可核实错引，故不触发D5关键错误cap。

<details><summary>V0.4理由与本行变化背景</summary>

答案evidence_registry为空，S1–S6各步reaction_evidence_id/evidence_id、酶与菌evidence_id、性状evidence_id全部为null，未交付任何可定位条目；各claim组来源状态均为MISSING_SOURCE（完全无引用），属缺失而非误导，默认不cap；无已核实错引，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。MISSING_SOURCE按低分档，取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：登记答案未交付任何来源记录；该空登记本身不支持或反驳科学断言。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案列有不确定性说明，且对缺失EC、SMILES和性状填null/unknown，较诚实；但多个未给来源的酶/微生物步骤仍标medium confidence，且未披露路径止于3-hydroxybutyryl-CoA、未到acetyl-CoA及整体无证据来源。属有部分不确定性披露但置信强度仍超过依据，落5-6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

uncertainties列出氧条件未指定、部分EC/基因/菌株保藏与基因组未知填null、两个CoA化合物SMILES缺失，未知项标注诚实且大量null未编造；但把无任何来源的酶/菌步以confidence=medium包装，且未披露主链止于3-羟基丁酰辅酶A（相对完整降解路线）及S5/S6归属属外推，披露偏笼统、部分结论强度超过依据。属有不确定性说明但过于笼统、部分强度超依据，取6；不构成系统性误导cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：支持答案对氧条件、null值及SMILES缺失作了部分披露；不支持其medium confidence的酶/菌判断已被来源支持。

</details>

## Kimi

答案SHA256：`a5f930a22a62a9c5a9efe0699e3dcd19ddb8a8fc02b96343c52a23de0a183739`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> D1 is restricted to &#91;1,4&#93;. The answer retains the route name and supplies four coherent steps with enzyme, microorganism, traits, and uncertainty, but it does not deliver the required linear main chain S01-S08 or the gold terminal acetyl-CoA; it substitutes a glutathione branch and stops at 2-hydroxy-2-methylpropanoate. This is a substantial completion/terminal failure, so 3 within the restricted range.

<details><summary>V0.4理由与本行变化背景</summary>

结构与任务符合度：route_scope.chosen_route_name逐字回填题面路线名，4个step均给出底物/产物（含name与SMILES）、首选酶、对应菌，两个profile各15项性状齐全且未知如实null，证据登记为局部EVID编号并自洽，未出现题面禁止的模型身份字段。扣分点：题面命名路线（gold共8步至acetyl-CoA）在主链内只覆盖前4步，2-羟基异丁酸之后仅写入不计分的downstream_continuation/central_metabolism_entry；S3酶与EC缺失（虽属如实未知）；NAD(P)H/NAD+的SMILES为null。整体属&#x27;主要模块均有涉及但有若干必要内容遗漏&#x27;，取5–6档上沿。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：Shows the required eight-step linear gold chain and S07 epoxide hydrolase; does not by itself judge the answer.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_124：Gold terminal is acetyl-CoA; does not support a main-route stop at hydroxyisobutyrate.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> Within the allowed D2 range &#91;1,6&#93;, the four-step epoxide/glutathione/aldehyde route is locally connected and chemically plausible: epoxidation, thiol opening, glutathione-dependent hydrolysis, and NAD+-dependent aldehyde oxidation. However it is an alternative branch rather than the specified gold chain to acetyl-CoA, and the glutathione route on isobutylene oxide is not independently established here. This supports the upper part of the limited band, 6, not higher.

<details><summary>V0.4理由与本行变化背景</summary>

主链化学：S1环氧化与gold S03同一转化（异丁烯+dioxygen+NAD(P)H→2-methyl-1,2-epoxypropane+水+NAD(P)+，产物SMILES CC1(C)CO1与gold 2,2-dimethyloxirane一致）；S2为GSH对环氧化物开环的S-共轭，区域化学（进攻CH2端）与结构式正确；S4醛→2-羟基异丁酸与gold S02化学一致且NAD+计量闭合。问题在于：S3把&#x27;硫醚→醛+再生GSH&#x27;写成异构化/水解，但该转化相对底物需要氧化当量（未列NAD+/O2），字面计量不闭合，属关键中间转化的机理缺口；同时以谷胱甘肽分支替代gold的环氧化物水解酶（EC 3.3.2.10→2-甲基丙烷-1,2-二醇）路线，替代路线已明确声明但仅以异戊二烯体系外推（冻结证据不可核，四.5第3步→登记未证实，不判错也不给高分）。偏离未推翻&#x27;异丁烯经环氧化起始&#x27;的主结论，不触发D2 cap；&#x27;主干部分成立但关键中间体/连接需修订&#x27;→6档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：Gold uses alkene monooxygenase entry and epoxide hydrolase S07; the answer&#x27;s GST branch is chemically plausible but not the gold main chain.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：Supports the entry epoxidation enzyme context; does not establish the answer&#x27;s GST/hydrolase branch.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> Release facts give S=1/8, F=1 confirmed KEY failure, U=6, with D-KEY4 cap &#91;1,4&#93;. Only the entry epoxidation step is confirmed; S07 is a confirmed KEY nonmatch and six MAJOR steps remain alignment-unconfirmed. The usable target portion is limited to the entry context, so within &#91;1,4&#93; choose 3, not 4.

<details><summary>V0.4理由与本行变化背景</summary>

酶-反应对应：S1 alkene monooxygenase EC 1.14.13.69 与gold S03的酶名/EC/菌逐字一致（可靠支持）；S2 EC 2.5.1.18为谷胱甘肽转移酶通名，家族级对应合理，但被引文献只证明AD45的GST作用于异戊二烯/二氯环氧乙烷类底物，不等于已证实催化异丁烯氧化物（家族相关性≠具体催化证据，故不能给高档）；S3如实把酶与EC标为未知（low/null），未编造编号；S4 EC 1.2.1.3为通用醛脱氢酶，gold该步为1.2.1.98/1.2.1.-（多注集合），答案选集外号，冻结证据无1.2.1.3条目（GAP-124-005）→按四.5保守条款登记UNRESOLVED、不判错。综合&#x27;主要步骤酶对应有支持，若干关键条目需进一步确认&#x27;→6档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：Supports the accepted target enzyme list for required steps; does not support the answer&#x27;s substituted GST branch.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：Shows required step direction and S07 epoxide hydrolase target; does not credit the answer&#x27;s alternative route.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Mycobacterium sp. ELW1 for the alkene monooxygenase entry step matches the gold organism exactly. Rhodococcus sp. AD45 is a plausible isoprene/epoxide-GST strain, but the answer&#x27;s isobutylene-specific GST/hydrolysis capability is inferred and not confirmed in the frozen record; no complete-pathway organism claim is made. This fits 5-6; choose 5 because strain-level capability remains unverified.

<details><summary>V0.4理由与本行变化背景</summary>

微生物对应：S1 Mycobacterium sp. ELW1 与gold S03该步菌完全一致（身份定位可靠）；S2–S4用 Rhodococcus sp. AD45，该菌是真实的异戊二烯降解菌，其GSH体系有文献方向支持，但对异丁烯氧化物的步级催化与整菌能力是外推（答案S2.uncertainty已声明&#x27;同类底物推定&#x27;）。答案未填任何TaxID/保藏号/基因组号（全部null），不存在身份编号编造或用另一菌株编号顶替的身份错配；complete_pathway_organism_profile_id=null，未把单步菌写成整条路径菌，符合身份定位≠反应级能力≠完整路径能力的三层纪律。缺口是AD45步级能力与ELW1的F7等能力声称无冻结证据可核，属&#x27;合理候选+部分支持、关键作用范围未充分核验&#x27;→6档，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_124：Supports Mycobacterium sp. ELW1 for the entry epoxidation step; does not support Rhodococcus AD45 downstream capability.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：Supports the ELW1/alkene monooxygenase entry context; does not establish the AD45 branch.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> All 15 trait fields are present for both profiles and many unknowns are explicitly null, which is good disclosure. However several non-null traits are unsupported by raw_text or by frozen observed records, and some are genus-level or internal-knowledge extrapolations. No confirmed key trait error is established; partial accuracy and evidence insufficiency support 5.

<details><summary>V0.4理由与本行变化背景</summary>

性状：两profile各15项齐全，未知如实null（ORG_001有F2/F3/F4/F5/F14共5项未知；ORG_002有F3/F4/F5/F14共4项未知，合计与本表traits_counts登记一致），无编造数值、无把观测写成预测的标签。已给值多为属级通用且方向正确（革兰氏阳性/抗酸、不产孢、无运动性、杆状或杆-球生长循环、O2为末端电子受体），功能性状（ELW1以异丁烯为碳源、烯烃单加氧酶活性；AD45 GST活性EC 2.5.1.18）与gold该步酶/菌方向一致。问题：关键定量项证据不足——ORG_002最适温度30°C与mesophile定级来自EVID_004（INTERNAL_KNOWLEDGE_ONLY，low），ORG_001的F10–F13/F15亦仅内部知识；AD45&#x27;以异丁烯为碳源&#x27;属异戊二烯数据外推；gold对ELW1全部性状为UNKNOWN、对AD45无记录（GAP-124-056~061/068~075），无法核实。属&#x27;部分性状准确且适用，关键项证据不足&#x27;→6档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_124：ELW1 records are mostly UNKNOWN except TaxID; absence of an observed value does not make a filled value false, but it limits verification.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_124：Indicates many ELW1 traits are completeness-only or unscoreable in the frozen trait table; does not validate the answer&#x27;s filled values.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_124：Shows subfield scoreability and pending range policy; not a source of observed values for ELW1.

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer supplies an evidence_registry with mapped evidence IDs; some route and enzyme claims point to specific literature or database citations. However many citations are free-text and not verifiable in E0, the S4 reaction relies on INTERNAL_KNOWLEDGE_ONLY, and trait evidence largely lacks locators or raw_text. No verified mis-citation is established. Decision-relevant groups are only partly traceable, so 5.

<details><summary>V0.4理由与本行变化背景</summary>

可追溯性：每条事实都绑定了EVID编号，registry给出数据库/文献级定位（Kottegoda 2015 AEM 81；Ensign 2001 Biochemistry 40:5845-5853；van Hylckama Vlieg 1998 AEM 64:2800-2805；EC 1.2.1.3条目标识），属条目级可定位，明显优于纯笼统库名；但E0对该case只有3条与本答案无claim关联的条目（related_claims均为空），相关EC（1.14.13.69、2.5.1.18、1.2.1.3）与四条引文全部为EVIDENCE_GAP_NO_RECORD/FREE_TEXT，一律UNRESOLVED_SOURCE；性状与S3/S4反应证据依赖EVID_004（INTERNAL_KNOWLEDGE_ONLY）=MISSING_SOURCE；S3无EC、无生成记录。决策相关组（CG01/02/03/05/07/08）呈&#x27;部分条目级可定位但不能核对+部分缺失&#x27;，按P41落入5–6档下沿，取5；无任何经核实的错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Used only to evaluate what the system actually delivered for traceability; not to backfill missing sources.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> The answer clearly states that oxygen was not specified; it flags the missing S3 EC, the inferred S4 oxidation, and alternative-branch uncertainty. Many unknowns are explicitly null, and confidence is mostly low/medium. Minor concerns remain: some ELW1 traits are labeled high confidence without raw_text, and internal-only trait statements are not individually marked as inferred. The disclosure is good but not fully uniform, so 7.

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界：答案披露质量较具体——每步有uncertainty、逐字段confidence（S3/S4低置信、F15标&#x27;推测&#x27;、题面氧条件null被明确写出），另列4条uncertainties并声明替代支路不计入主链，未把预测冒充观测，也未掩盖S3酶未知。扣分点：若干净化性状（F10–F13、F15等）以&#x27;medium&#x27;置信包装INTERNAL_KNOWLEDGE_ONLY内容且未提示应复核，ORG_002的30°C定值同样只有low置信而无raw_text/来源说明；同时把GSH分支作为主链呈现时，未指出与已知环氧化物水解酶（EC 3.3.2.10）路线并存这一冲突点。属&#x27;披露较充分但部分结论强度略超依据&#x27;的单点/多点过度确信，非系统性误导，档内扣分不cap→6档。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Used only to evaluate evidence-nature and uncertainty disclosure, not scientific truth.

</details>

## Qwen

答案SHA256：`ad78e995c094c14fa881b400b2a237679c79b2a460de95aca2242baa2f102370`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> JSON is complete and includes path, enzymes, one microorganism, traits, sources, and uncertainty. However the route departs from the specified 2-methylpropene gold main chain: after S1 epoxidation it uses an epoxide-isomerization/isobutyryl-CoA/valine-like route and omits gold S01/S02/S05/S06/S08 and terminal acetyl-CoA. Several ECs are null and many traits are null. D1 task deviation is a verified key error, capped at 4; score 3.

<details><summary>V0.4理由与本行变化背景</summary>

档位7–8（大部分必要内容完整、关联清楚、少量工程缺陷）：9步主链每步均给出主底物/主产物（name+smiles）、首选酶与对应菌并绑定profile；15项性状全数出现（8填7明确null，无遗漏）；route_scope.chosen_route_name原样回显题面路线名，氧条件保持null未被擅自改写；另附route_summary、central_metabolism_entry、downstream_continuation、evidence_registry与uncertainties。扣分点为5步EC为null、多数CoA硫酯SMILES为null（属可接受缺失但属交付不完整）以及全部9步共用一个菌profile。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：Confirms the gold step order and terminal acetyl-CoA; does not by itself prove M156 false.
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_124：Confirms the task terminal is acetyl-CoA, not propanoyl-CoA.

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> S1 isobutene epoxidation to 2-methyl-1,2-epoxypropane matches the gold S03 transformation and is chemically coherent. The subsequent epoxide-isomerization route to 2-methylpropanal and the isobutyryl-CoA/valine-like CoA steps are chemically plausible in outline, but they diverge from the gold main chain, several steps have null SMILES/EC, and the route lacks continuity evidence. This is partial usability, not a verified first-step or direction collapse; band 5-6, choose 5.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（主干部分成立、关键中间体/连接需修订、合理性证据有限）取6：首步异丁烯→2-methyl-1,2-epoxypropane（2,2-dimethyloxirane）与gold S03同向同产物，方向与原子数自洽；后续醛→酸→异丁酰CoA→甲基丙烯酰CoA→3-羟基异丁酰CoA→3-羟基异丁酸→甲基丙二酸半醛→丙酰CoA+CO2连续无跳步、无方向反转、无中心代谢物跳跃。但S2用环氧异构化直接得异丁醛，与gold S07（环氧水解酶→2-甲基丙烷-1,2-二醇）不同且答案未声明为替代路线、无任何可核依据；全链属未证实替代路径。不cap：与gold不同不自动判错，四步判断第1步题面未给步骤级路线、无起始步错误/无反转/无不守恒。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：Confirms S03 epoxidation and the different gold downstream sequence; does not prove the alternate chemistry impossible.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：Shows the gold enzyme set; answer enzyme names/EC are not all the same and many ECs are null.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> Target-layer counts from the release contract are S=1, F=2, U=5. The one confirmed target is S03/S1 epoxidation; S04 and S07 are confirmed KEY failures; S05/S06/S08 are missing and S01/S02 remain alignment-unresolved. Because confirmed KEY failures cap D3a at 4, the score stays in &#91;1,4&#93;. The usable part is limited to one clear entry step, with two key failures and several unresolved/missing targets, so score 3 rather than 4.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（有合理候选和部分支持，若干关键步骤缺具体核验）取6：S1烷基单加氧酶对应环氧化、S3醛脱氢酶EC 1.2.1.3对应醛→酸、S6烯酰CoA水合酶EC 4.2.1.17对应水合、S8 EC 1.1.1.31对应3-羟基异丁酸脱氢、S9 EC 1.2.1.27对应甲基丙二酸半醛氧化脱羧，类别—反应类型均匹配，未见EC大类别错配或酶名-EC互相矛盾；但9步中5步EC为null，S2仅给功能名，且1.2.1.3/4.2.1.17/1.2.1.27在E0无冻结记录、1.1.1.31仅第三方名称级一致且claim注释仍为UNRESOLVED。不cap：错引归D5，本维无已核实酶功能失效。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：Confirms the gold reactions for S04/S07 and the omitted S05/S06/S08 steps.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：Confirms accepted enzyme names/EC for key steps; does not certify arbitrary strain activity.

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> All steps are assigned to Mycobacterium sp. M156, with no TaxID, culture collection, genome, or strain-level capability evidence. Gold uses Mycobacterium sp. ELW1 and other organisms across steps; M156 is not in the delivered organism gold. The whole-pathway claim via ORG_001 is unsupported. This is not a verified false identity, but it is a broad strain-level attribution and whole-path capability written beyond evidence; score 3.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（有合理候选和部分支持，关键身份或作用范围未充分核验）取5：仅一条profile Mycobacterium sp. M156（taxid null），却同时作为全部9步的催化剂并声明complete_pathway_organism_profile_id=ORG_001。属级（Mycobacterium）与gold所用Mycobacterium sp. ELW1/M. austroafricanum同属，作为候选合理；但菌株M156无任何冻结身份记录，步级归属与整条路径能力完全依赖EVID_001/EVID_002内部记忆与low/medium置信，性状子字段亦为GAP-124-062~067。不cap：身份未证明虚构、非跨属/跨kingdom、无已核实身份错配（不得凭记忆放行也不得凭怀疑判错）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_124：Shows gold step organisms; absence of M156 does not prove M156 false, but no strain-level support is delivered.

</details>

### D4 性状科学性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> Several delivered traits are plausible genus-level Mycobacterium features (aerobic, rod-shaped, Gram-positive mycolic-acid envelope, non-spore-forming), and many unknown traits are explicitly null. But they are applied to unverified strain M156, and F7/F8/F9 use route/capability claims rather than strain-level observations. The trait block is partially usable but key applicability evidence is missing; score 4.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（部分性状准确且适用，但关键项证据不足或条件解释需修订）取5：所填8项（aerobic、O2为末端电子受体、利用短链烯烃、经环氧化降解短链烯烃、alkene monooxygenase活性、杆状、Gram阳性含分枝菌酸、非产孢）与Mycobacterium属级特征相符，方向上未见&#x27;嗜冷菌最适80°C&#x27;式离谱错误；但全部为属级常识套用于未核菌株M156（粒度不匹配），来源仅EVID_001/EVID_002内部记忆、confidence多为low，温度/pH/盐度/保藏号/基因组/运动性诚实置null。未把预测写成观测（标low/unknown），按四.4不重复重扣完成度。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_124：Shows available gold trait records and that many M. sp. ELW1 traits are UNKNOWN; does not verify M156.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_124：Shows which trait fields are scoreable; many M156-relevant fields lack observed sources.

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> The answer delivers EVID_001-EVID_003, but all are INTERNAL_KNOWLEDGE_ONLY with no database, record ID, DOI, or locatable external entry. Step and trait claims are mapped to local evidence IDs, so this is not zero traceability, but it is effectively missing-source traceability under the six-state scheme. MISSING_SOURCE defaults to low band and does not trigger a verified mis-citation cap.

<details><summary>V0.4理由与本行变化背景</summary>

档位1–2（几乎无法定位重要结论依据）取2：EVID_001–EVID_003全部source_type=INTERNAL_KNOWLEDGE_ONLY、database与record_id为null，决策相关组（CG01/CG02/CG03/CG05/CG07/CG09）均为MISSING_SOURCE——按四.3属&#x27;无引用或仅内部知识自我声明&#x27;低分档，默认不cap。E0未提供任何可核实的错引事实（无CONTRADICTED），故severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不登记VERIFIED_MIS_CITATION_*，D5不执行cap；答案以claim_scope逐条自陈用途只提升可读性，不能被当作可定位条目。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> The answer is reasonably transparent about many unknowns: oxygen condition is null, many trait values are explicit nulls with unknown confidence, step uncertainties mention missing ECs, and downstream continuation is labeled inferred. However the alternate route and whole-path M156 capability are presented with more confidence than the evidence supports. This is mid-band uncertainty handling, not systematic fabrication.

<details><summary>V0.4理由与本行变化背景</summary>

档位5–6（有不确定性说明，但部分结论强度超过依据）取6：正面项——全链confidence多为low、未知一律null、uncertainties具体列出EC/菌株/生理参数缺口、route_scope.notes声明&#x27;下游异丁酸/缬氨酸样代谢为推断延伸&#x27;、evidence_registry明示INTERNAL_KNOWLEDGE_ONLY，未把预测包装成DATABASE_DIRECT。扣分项——route_summary与complete_pathway_organism_profile_id以陈述语气给出未核实路线与单菌全路径能力，未披露存在gold所记二醇—2-羟基异丁酸路线的分歧，S1/S3给medium偏强。属单点/局部过度确信，非系统性把预测写成实证，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`c1c84ef3639b1386ea493a14b844b9ae42de15810c0fa00bfffd52f5f03c9ef4`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 仅覆盖4/8个必答主链步；微生物模块完全未交付，15项性状完全未交付；主链止于2-羟基-2-甲基丙酸，未到gold终点acetyl-CoA。虽路线名未改选，但核心任务模块大部缺失，D1落弱档3。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION：题面要求每步给一个对应微生物，并按organism_profile返回15项性状。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_124：本题冻结主链共8个必答步；不支持答案只交4步。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_124：gold终点为acetyl-CoA；不支持把2-羟基-2-甲基丙酸作为本题主链终点。
- ANSWER_TEXT / ANSWER.steps：答案实际只交4步，且microorganism全null、organism_profiles空。

</details>

### D2 反应化学科学性：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已交付S1-S4的转化方向、结构、辅因子和连接与gold对应步一致：S1环氧化、S2环氧化物水解、S3伯醇脱氢、S4醛脱氢均化学成立且含NAD+/NADH等辅因子。S4中性酸与gold 2-hydroxyisobutyrate阴离子仅为表示层电荷差异；下游缺失归D1，不另作D2化学错误。档内给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：支持已交付四步的底物、产物、方向与辅因子；不支持未交付下游步。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：支持相应步骤的accepted酶名/EC范围，不证明具体蛋白实验活性。
- ANSWER_TEXT / ANSWER.steps：答案四步的化学表达与辅因子信息。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 原答仅S1对应gold S03的alkene monooxygenase EC 1.14.13.69有accepted功能支持；S2/S3/S4仅给epoxide hydrolase、alcohol dehydrogenase、aldehyde dehydrogenase等通用名且EC=null，不能计S；S04/S05/S06/S08无可对应交付。确认覆盖0.125，核心主链严重不足，落&#91;1,2&#93;；一项关键入口已核与局部反应类型信息支持2分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：支持S03精确EC；S01/S02/S07的accepted名为具体脱氢酶/水解酶，不支持答案通用酶名直接视为S。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：支持目标步顺序与方向，用于判断答案映射和缺步，不新增化学裁定。
- ANSWER_TEXT / ANSWER.steps：答案仅一项显式EC和三个通用酶名。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 所有step.microorganism=null且organism_profiles=&#91;&#93;，未交付任何微生物物种/菌株身份、单步归属或整路径能力信息；按模块MISSING=1处理，不宣称检测到具体微生物错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.microorganism：答案未交付任何微生物对应信息。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles为空，15项性状0填写、0明确未知、15遗漏；按D4模块MISSING=1处理，不宣称检测到性状科学错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.organism_profiles：答案未交付任何organism_profile及15项性状。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D5按claim group：路线/起点/终点/关键酶/微生物身份等决策相关组仅有EVID_001/EVID_002且source_type=INTERNAL_KNOWLEDGE_ONLY，无数据库、文献或条目级可定位记录；属MISSING_SOURCE低分档。无已核实错引，不触发cap；有内部证据ID与claim_scope映射但不可外部定位，取2非1。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：仅内部知识声明，无外部落点；不证明引用存在或不支持结论。

</details>

### D6 不确定性与诚实度：9 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案明确区分已确认、推测与未知：S1 EC 1.14.13.69的官方底物为丙烯、异丁烯生理底物未确认；S2-S4的EC/基因/菌置空；uncertainties说明无菌株、无性状、下游衔接不计入主链；置信度与证据相称，无系统性把预测写成实证。少量“已报道好氧主链”表述未附来源，故给9而非10。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案对未知、限制和未计入主链内容的披露。

</details>

## GPT5.6

答案SHA256：`b83960511b87db5514cba9f709d1d064a4ad75c7420d8e9208da21b367fc4340`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面路线名正确，答案也给出了底物/产物、酶/EC与微生物，但仅交付4个step（S1-S4），止于2-hydroxyisobutyric acid；按本题冻结主链，required共8步且终点为acetyl-CoA，S04/S05/S06/S08未交付，终点未达。organism_profiles虽有15项性状外壳，但F2-F15的value全部为null，性状模块实质未填写。因此属于3-4档中“仅覆盖少数必要模块，多处缺步骤/性状”，取4分。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_124：本题formal案例为LINEAR_UNIQUE且ordered_step_count=8；仅用于确认冻结主链的完整步数，不把分支或全图并集当默认分母
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_124：路线名为2-methylpropene degradation，gold terminal main product为acetyl-CoA；支持判断答案未达指定终点
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：显示本题必答主链含S04、S05、S06、S08等下游步骤且S06为终点步；答案未给出这些步骤，仅用于缺步定位

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 已交付的S1-S4可对应gold的环氧化、环氧化物水解、二醇氧化、醛氧化四步：底物→产物方向正确，主有机骨架连续，S1产物为环氧丙烷类、S2水解为二醇、S3/S4生成羟基醛和羟基酸，主干部分成立。但路线止于2-hydroxyisobutyric acid，未连接S04/S08/S05/S06至acetyl-CoA，主链后段和终点缺失；S3以water作副产物代替H+，S4醛氧化未列H2O且NAD+/NADH的SMILES相同，属局部氧化还原/计量表达缺陷。按D2 5-6档“主干部分成立但关键连接/转化仍需修订”，取6分；不因缺步直接判D2关键错误，缺步主归D1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：gold主链显示S03环氧化→S07水解→S01二醇氧化→S02醛氧化，并继续S04/S08/S05/S06至acetyl-CoA；S01/S02使用NADH/H+，S03使用O2/NADH/H+。用于核对已交付前四步化学与下游连续性及局部辅因子表达差异
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_124：gold terminal main product为acetyl-CoA；支持判断答案未完成至指定终点的连续性
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_124：冻结主链为8步LINEAR_UNIQUE；用于确认答案只覆盖前四步而非完整主链

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D-KEY4 cap ≤4 applies because the required KEY terminal step S06 and downstream S04/S05/S08 are empirically not delivered; the answer stops at 2-hydroxyisobutyric acid. Among delivered steps, S03 epoxidation matches the accepted alkene monooxygenase/EC row, while S01/S02/S07 remain nonaccepted or pair-unverified. This is the 3–4 range; within it, only a few targets are usable and key failure clearly dominates, so 3 rather than 4.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_124：Gold required enzyme steps S01-S08 and terminal acetyl-CoA; used to identify missing downstream steps and nonaccepted enzyme rows. Does not by itself prove a different claimed enzyme cannot catalyze a step.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_124：Gold directed reactions and terminal S06 acetyl-CoA; supports the omission finding, not any unclaimed catalytic incompatibility.
- E0_EVIDENCE / f3e0:ec:3.3.2.3：EC 3.3.2.3 is recorded as transferred/deleted with replacement history; this does not by itself prove the historical enzyme could not catalyze the answer&#x27;s epoxide hydrolysis, so the pair remains unresolved.

</details>

### D3b 微生物身份与能力：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer attributes every delivered step to one strain, Mycobacterium sp. E20, with no TaxID, no strain-level capability evidence, and only INTERNAL_KNOWLEDGE_ONLY support. Gold uses Mycobacterium sp. ELW1 and other organisms for these step types; E20 is not proven false, but identity and step-level ability remain unverified. This fits the weak 3–4 band; plausible genus and honest low confidence support 4 rather than 3.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_124：Gold lists step-level organisms such as Mycobacterium sp. ELW1 and other taxa; it does not by itself prove Mycobacterium sp. E20 is invalid.

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All 15 required traits for ORG_001 are present as null/unknown with no trait values. Per P44, all required trait values null/empty is D4 MISSING=1, not a scientific-error finding.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_124：Confirms which trait fields are scoreable or completeness-only in the frozen slice; does not supply answer trait values.

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Only one evidence entry is delivered, EVID_001, with source_type INTERNAL_KNOWLEDGE_ONLY and no database, record_id, or locator. All decision-relevant claim groups are therefore MISSING_SOURCE. MISSING_SOURCE defaults to the low D5 band without cap; the presence of local claim IDs but no locatable external record supports 2 rather than 1.

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer consistently uses low/unknown confidence, explicitly records oxygen-condition uncertainty, missing TaxID/genome/trait data, and enzyme/EC uncertainty. It does not present internal knowledge as observed evidence. The main limitation is a few unsourced &#x27;literature&#x27; statements, but overall uncertainty disclosure is strong and supports 7–8, at 8.
