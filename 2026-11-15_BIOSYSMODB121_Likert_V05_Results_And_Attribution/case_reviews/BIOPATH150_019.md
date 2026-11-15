# BIOPATH150_019：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：Toluene degradation II (aerobic) (via 4-methylcatechol)

污染物：Toluene；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 50.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 49.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 56 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 46.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 56.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 43 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`21a5400dbdcc2564b37a97aa3f45a2a16f4ca436d03fa3a3e30ebc5e30ebb15e`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分9 → V0.5新分4，变化-5。

新裁判理由：

> All main modules are present (six steps, enzyme/microorganism fields, 15 trait fields), but D1 task compliance is capped by the D1 base range &#91;1,4&#93; because the delivered chemical route departs from the frozen specified route at the required mapped S02 step. Within that cap, the otherwise complete delivery supports the upper value 4 rather than a lower one.

<details><summary>V0.4理由与本行变化背景</summary>

六个主链步骤均给出底物/产物名称与SMILES、首选酶及对应微生物；organism_profiles按物种+菌株去重，15项性状字段齐全；route_scope原样填写题面指定路线。部分性状为null或低置信概括，属任务允许的未知填写，不构成完整性关键缺陷。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：Fixes the required S02 substrate-to-product transformation; supports route deviation at that mapped step, not a general claim about enzyme flexibility.
- ANSWER_TEXT / ANSWER.steps&#91;S4&#93;：Shows the delivered mid-route product 5-methyl-2-oxopent-4-enoate plus formate at the mapped S02 position.

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> The main chain is largely chemically coherent: S1-S3 correspond to the expected toluene-to-4-methylcatechol sequence and the terminal aldolase/endpoint reaches pyruvate and propionaldehyde. However the answer S4 product is foreign to the required S02 intermediate, so the specified route has a key intermediate needing revision. D2 base range is &#91;1,6&#93;; C06 treats a chemically plausible substitution as at most 6, so 6 is selected for the otherwise coherent rest of the chain. S4/S5 representation issues are retained locally rather than turning the dimension NE.

<details><summary>V0.4理由与本行变化背景</summary>

主链方向与关键转化基本正确：toluene→p-cresol→4-methylcatechol→间位裂解→下游至pyruvate+propanal，终点符合题面。S4中间体命名与gold的(2Z)-2-hydroxyhexa-2,5-dienoate不同，S4/S5按另一相近写法处理，存在局部待核，但未出现起始步错误、方向反转或明显不守恒，不触发D2关键错误。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：Provides the required S02 product and shows which downstream representations are held; does not by itself assert the answer&#x27;s foreign product is impossible outside the locked route.
- ANSWER_TEXT / ANSWER.steps&#91;S1-S6&#93;：Shows the visible main-chain transformations and continuity used for D2 scoring.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> Release facts give S=1, F=1, U=4 for the six required targets. S02 is a confirmed KEY failure and the D-KEY4 gate sets the allowed range &#91;1,4&#93;. Only S01 has confirmed target support; S03 is candidate-only, S04/S05 are representation holds, and S06 is not bound. With few usable target reactions and the KEY failure boundary not clear enough for the upper restricted value, score 3 is appropriate. Local unresolved major steps are retained in the paired NE fields.

<details><summary>V0.4理由与本行变化背景</summary>

S1–S5酶名与反应类型基本对应（T4MO、2,3-双加氧酶、水解酶、水合酶），EC多为正确亚类通配；S6给出4-hydroxy-2-oxohexanoate aldolase但EC写4.1.2.-，与gold的4.1.3.43亚类不符，属局部EC注释错误，不推翻该步酶名与反应类型，故不cap；S3–S5具体基因/纯酶表征未核。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_019：Provides accepted enzyme/EC context for each target step; does not by itself confirm protein-level activity.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：Supports the S02 target reaction/product required for D3a target credit.
- ANSWER_TEXT / ANSWER.steps&#91;S4&#93;：Shows the answer&#x27;s mid-route product substitution at the mapped S02 position.

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> Pseudomonas mendocina KR1 is a real species/strain identity and appears exactly in organism_gold at S01; TaxID is honestly null. However the answer assigns KR1 to every downstream step and claims complete-pathway capability, while the frozen inputs provide no step-level KR1 capability record and the PATHWAY_COMPLETE gold row is Ralstonia pickettii. There is no confirmed contradiction, but several scope claims remain unresolved. This fits the partial band; 6 reflects plausible identity with unverified downstream/whole-pathway scope.

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤归到Pseudomonas mendocina KR1；gold在S01确认KR1可携带T4MO并以甲苯生长，故身份定位与首步能力有支持；下游步骤归KR1的逐酶能力缺乏条目级证据，存在将整体降解能力用于各步的粒度风险，但KR1为已知甲苯降解模式菌，未达到身份错配或跨类群cap门槛。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_019：Supports exact P. mendocina KR1 name at S01 only; does not support all downstream steps or whole-pathway completion by KR1.
- ANSWER_TEXT / ANSWER.steps&#91;*&#93;.microorganism：Shows the answer&#x27;s repeated KR1 attribution and complete-pathway claim.

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> All 15 trait fields are present: 12 filled, 3 explicit unknown, 0 omitted. The filled qualitative traits are plausible for Pseudomonas mendocina, and the answer honestly leaves quantitative pH, salinity numbers, culture collection, genome values and TaxID as null/unknown. However the frozen trait_gold and trait_scoreability_mask contain no observed P. mendocina KR1 values, and several species-level generalities are applied to the strain without strain-level evidence. No confirmed contradiction is established, so the partial band 6 is appropriate rather than MISSING or NE.

<details><summary>V0.4理由与本行变化背景</summary>

性状多为P. mendocina物种级一般性状（革兰氏阴性、杆状、运动、不产芽孢、好氧、中温、非嗜盐、甲苯降解），与KR1身份大体相容；温度/pH/盐度数值多留null，F3/F5/F14明确未知，未把大量未核实数值写成确定观测。部分性状如专性好氧、泛栖息型为物种级概括，证据仅内部知识，属局部适用性待核；无关键性状明显错误或离谱数值。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_019：Shows no observed P. mendocina KR1 trait values in frozen inputs (completeness-only/UNKNOWN); does not support or contradict the qualitative values.
- ANSWER_TEXT / ANSWER.organism_profiles&#91;ORG_001&#93;.traits：Shows the delivered trait set, explicit unknowns, and confidence labels used for D4.

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> All decision-relevant claim groups rely on evidence_registry entries marked INTERNAL_KNOWLEDGE_ONLY, with no record_id, DOI, stable locator or claim-level database entry. This is MISSING_SOURCE rather than verified mis-citation: the answer does not fabricate a locatable record, but it also does not deliver a traceable source chain. The low band 3 is appropriate; no D5 cap is applied because no verified mis-citation is established.

<details><summary>V0.4理由与本行变化背景</summary>

证据注册表三条均为INTERNAL_KNOWLEDGE_ONLY，record_id为空；EVID_001仅有MetaCyc通路名/内部复述，EVID_002/003无定位；决策相关组均无条目级可核对来源。按MISSING_SOURCE低分档，属缺失/不可追溯而非已核实错引，默认不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：Shows all three evidence entries are INTERNAL_KNOWLEDGE_ONLY with no record IDs or locatable bibliographic records.

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> The answer explicitly discloses that all content is based on internal knowledge without real-time database/literature access, lists specific uncertainties for S3-S6 enzymes/EC and missing TaxID/genome/trait values, and uses null/unknown where information is absent. It does not systematically present predictions as observations. Some high-confidence qualitative traits and the KR1 whole-pathway capability claim are less caveated, which is a single-point overconfidence issue rather than systemic misleading; score 7.

<details><summary>V0.4理由与本行变化背景</summary>

答案明确声明全部条目基于模型内部知识、未实时查询，列出S2酶命名分歧、S3–S6基因/酶学证据不足、TaxID/保藏/基因组/温盐pH缺失等具体限制；置信度多标medium/low/unknown，未把预测系统性写成实证。少量物种级性状标medium/high但属一般分类性状，未掩盖主要矛盾。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：Shows the answer&#x27;s explicit internal-knowledge disclaimer and item-level uncertainty statements.

</details>

## DeepSeek

答案SHA256：`3fa765d953b1f5d5d288c740f31ca2d565a411b2cef166dc5398054c614539b1`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分9 → V0.5新分5，变化-4。

新裁判理由：

> 答案返回完整可解析JSON，route_scope名称与好氧条件原样填写，6个step均给出底物/产物及SMILES、酶与EC、对应微生物，organism_profiles列全15项性状，工程与字段覆盖基本完整。但按本题冻结主链，仅能确认S01及S03结构对应，answer的S4–S6未绑定gold S02/S04/S06，S05对应步仍为表示待定；所答下游走向pyruvate+acetaldehyde，而冻结主链终点为propionaldehyde|pyruvate。属于主模块齐全但若干必经主链内容缺漏/未交付，取5–6档低段5。

<details><summary>V0.4理由与本行变化背景</summary>

6步均给出主底物/主产物英文名与SMILES、单一首选酶含EC、一个对应微生物；organism_profiles按物种+菌株去重为1条（ORG_001）并由步级引用；route_scope原样回填题面指定路线名与aerobic；15项性状按指定顺序齐全且未知项如实置null；JSON可解析。无重要模块遗漏或范围偏离，判9分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / question.json messages&#91;0&#93;.content：任务要求指定路线名称、好氧条件、逐步酶/菌及15项性状交付
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_019：本题为LINEAR_UNIQUE，gold ordered_step_count=6
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：gold六个必答步及其主底物/主产物，含终步产物Pyruvate与Propionaldehyde
- ANSWER_TEXT / ANSWER.steps S1–S6; ANSWER.organism_profiles&#91;0&#93;.traits：答案实际交付的六步及15性状，不含额外认可证据

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 起点甲苯→对甲酚→4-甲基邻苯二酚的转化与好氧方向合理，后续水解/水合/醛缩成链连续，未见方向反转或明显原子不守恒；辅因子未列属局部计量缺陷，不足以单独cap。主要问题在S3产物的名称“2-Hydroxy-5-methyl-6-oxohexa-2,4-dienoate”与所给SMILES存在结构身份冲突（路线诊断为UNKNOWN而非已证F），且后续走C5/乙醛分支而非冻结主链的C6/丙醛终点，未作为不属评分主链的替代分支说明并论证。主链部分成立但关键中间体表示与分支依据仍需实质修订，取5–6档中段6。

<details><summary>V0.4理由与本行变化背景</summary>

S1–S3与gold S01/S03/S05完全一致（甲苯→对甲酚→4-甲基邻苯二酚→2-羟基-5-甲基-6-氧代己-2,4-二烯酸），起始步、方向与开环产物正确。S4–S6改走2-氧代戊-4-烯酸/4-羟基-2-氧代戊酸支路并以丙酮酸+乙醛收尾，与指定路线下游（2-羟基己-2,5-二烯酸+甲酸→4-羟基-2-氧代己酸→丙酮酸+丙醛）不同；各步碳数守恒、步骤连续，无起始步错误、无无依据跳步，故不构成cap；但分支与终点未声明且无冻结证据支持，按5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：gold主链S01/S03/S05/S02/S06/S04的反应物、产物与终步Pyruvate+Propionaldehyde
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_019：pathway终点名为Propionaldehyde|Pyruvate；不证明任意替代分支均错误
- ANSWER_TEXT / ANSWER.steps S1–S6：答案实际化学序列、S3产物SMILES、S4–S6产物与终点

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 按冻结目标事实：S01为CONFIRMED_TARGET/SUPPORTED，answer S1的toluene 4-monooxygenase EC 1.14.13.236与accepted集合一致；S03为UNRESOLVED_NONACCEPTED，answer S2给出EC 1.14.13.188而非accepted的1.14.13.236，但不能据此判F；S05为ROUTE_HOLD_REPRESENTATION/UNRESOLVED，answer S3产物名称与SMILES身份未决；S02、S04、S06为ROUTE_BLOCKED_MISSING，answer的S4–S6未绑定相应目标反应。可判S=1/6，另有U=2、M=3，核心主链多个必需目标缺失/待核，仅能进入低档&#91;1,2&#93;。存在S01这一已核目标功能信息，但关键主链推荐仍失效，故取2而非1；局部U不使整维NE。

<details><summary>V0.4理由与本行变化背景</summary>

S1（toluene 4-monooxygenase，1.14.13.236）与S3（catechol 2,3-dioxygenase，1.13.11.2）与gold酶-EC逐字一致；S5（4.2.1.80）与gold的『2-羟基己-2,5-二烯酸/2-氧代戊-4-烯酸水合酶』一致，属可靠支持。S2（1.14.13.188）、S4（3.7.1.9）、S6（4.1.2.4）在冻结证据中无记录（GAP-019-006/013/016），酶名-EC配对无法核对，尤其S6的4.1.2.4须官方条目核对。有合理候选与部分支持、若干关键步骤缺核验，判6分；无已核实关键错误，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_019：gold必答步酶名/EC参考行，支持S01/S03/S05/S02/S04/S06的accepted enzyme集合；不证明具体蛋白实验活性
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：gold逐目标反应底物/产物，用于核对S03、S05及S02/S04/S06缺失/未绑定
- ANSWER_TEXT / ANSWER.steps S1–S6 enzyme/EC/products：答案实际EC、酶名及产物；显示S1匹配、S2非accepted、S3表示未决、S4–S6未绑定gold目标步

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> P. mendocina KR1身份真实，S01与gold organism行EXACT，单步对应有部分支持；但同一菌被用于S2-S6并声明complete_pathway_organism_profile_id=ORG_001，gold仅支持S01的KR1，其他步骤与全路径能力无冻结证据，TaxID 300为物种级支持菌株级声称，属粒度不足/未核，不cap，按5-6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

菌名Pseudomonas mendocina KR1在gold organism_gold的S01以EXACT出现，身份定位有名称级支持；但（i）TaxID 300在gold中无记录（KR1登记为No TaxID），以物种级编号支撑菌株级身份属粒度不足；（ii）6步全部归同一菌并以complete_pathway_organism_profile_id=ORG_001声称全路径能力，而gold步级归属分别指向Ralstonia pickettii等，gold的PATHWAY_COMPLETE菌为Ralstonia pickettii。E0无法核实KR1的步级与全路径能力，按6分；无已核实关键错误，不cap，登记UNRESOLVED。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_019：S01有Pseudomonas mendocina KR1与toluene 4-monooxygenase的EXACT行；其他步的gold多列Ralstonia pickettii等，未给KR1全路径支持。
- ANSWER_TEXT / ANSWER：答案把ORG_001用于全部步骤并声称complete pathway；支持观察到全路径声称，不支持其已核。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 15项性状齐全，未知项保留null；但P. mendocina KR1在trait_gold仅UNKNOWN行，无观测记录，温度30℃、运动性、栖息地等依赖EVID_002内部知识且未明确区分观测/预测，关键性状证据不足，按5-6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

15项齐全，盐度、pH、保藏号、基因组4项以null+unknown诚实置空（明确未知≠遗漏）；11项已填性状全部指向EVID_002（INTERNAL_KNOWLEDGE_ONLY），无raw_text、无数据库条目：温度最适30 °C、极性鞭毛运动、栖息地『generalist』等关键项缺可核来源，且均为物种级泛化描述直接用于菌株KR1。gold对P. mendocina KR1无任何性状记录，无法坐实数值错误，故不入3–4档；属『部分性状合理但关键项证据不足』，取5分。CG10氧需求为APPLICATION_CRITICAL且条件成立，答案方向（好氧）与题面一致，未构成筛选风险。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_019：该切片对Pseudomonas mendocina KR1的性状行为UNKNOWN，无观测值可确认；不支持把答案数值当已核。
- ANSWER_TEXT / ANSWER：答案提供15项性状与confidence；支持完整性与部分未知保留，不支持已验证数值准确性。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> EVID_001给出MetaCyc具体record_id与locator，覆盖路线/酶/菌，但E0 EVIDENCE_GAP无法核验其内容；EVID_002为INTERNAL_KNOWLEDGE_ONLY覆盖性状，F3/F4/F5/F14无来源。核心可定位但未核、性状缺源，未发现已核实错引，按5-6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

全部路线/酶/菌声称共用单一MetaCyc通路条目EVID_001（record_id与URL可定位，但E0为EVIDENCE_GAP，条目内容与支持范围无法核对→UNRESOLVED_SOURCE），且为通路级而非步级映射；性状与部分身份字段仅有INTERNAL_KNOWLEDGE_ONLY或无引用（MISSING_SOURCE），TaxID 300无任何来源覆盖。决策相关组存在条目级可定位证据（非纯笼统来源），无已核实错引，不cap；按5–6档下沿取5，全部待核标记保留。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案实际交付EVID_001具体数据库record/locator与EVID_002内部知识；支持D5对已交付记录的定位判断，不支持记录内容已核。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案保留null并用confidence标注部分未知，但uncertainties为空，未说明证据性质边界；内部知识性状给medium/high，未披露全路径能力与S05产物冲突限制，部分结论强度超过依据；未达系统性误导cap，按5-6档取5。

<details><summary>V0.4理由与本行变化背景</summary>

正面：全篇给出confidence标签，4项缺失性状标unknown，未编造数值填满字段。负面：11项已填性状中6项（F1/F6/F9/F11/F12/F13）以high、多项以medium包装仅来自INTERNAL_KNOWLEDGE_ONLY的内容，且无raw_text、无原文摘录；uncertainties为空，未披露S4–S6与gold路线分支/终点的差异，也未说明TaxID 300无来源；『generalist』等推断性表述未标注为推断。属多处过度确信（集中在一个模块、同一机制），尚无已核实矛盾被掩盖，不构成系统性误导，按5–6档取5。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案有confidence与null，也把EVID_002标为INTERNAL_KNOWLEDGE_ONLY；支持部分不确定性披露，不支持其已充分说明限制。

</details>

## Kimi

答案SHA256：`c4b870174aa9215c9046aca9c0f1e1c0d32bc2a2f99a704f91e29ee669de0bc8`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> The answer supplies the required route name/oxygen, seven steps with enzyme and microbe, three 15-trait profiles, evidence registry, and uncertainty disclosure. However the delivered main chain is not a faithful six-step gold route: the S02 hydrolase step is substituted and the S06 relation is not bound, so the route deviates in the actual chemistry. D1 is scored within the allowed &#91;1,4&#93; task range; 4 reflects otherwise strong field completeness but confirmed route-level deviation.

<details><summary>V0.4理由与本行变化背景</summary>

7步主链齐备，每步均给底物/产物英文名+SMILES、一个首选酶含EC、一个对应微生物；route_scope.chosen_route_name原样回填题面路线名，oxygen_condition=aerobic合规；3个organism_profile按物种+菌株去重、各15项性状齐全。仅少量缺陷：S7为gold终点外额外下游延续步（按四.2不加分不扣分），且“各项最强来源”多数由属级内部知识承担，属交付质量轻量问题，故取良好档上位而非充分档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：Gold required six-step order and S02 product identity; used only to locate the route-deviation issue, not to infer missing side branches.
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_019：Confirms six ordered required steps and LINEAR_UNIQUE status; does not by itself make every gold branch a required answer.

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分8 → V0.5新分5，变化-3。

新裁判理由：

> Initial steps S1-S3 and terminal aldol cleavage S6 are chemically coherent and continuous, but the mid-route hydrolysis S4 gives 2-hydroxyhexa-2,4-dienoate instead of gold 2-hydroxyhexa-2,5-dienoate while using EC 3.7.1.9 rather than accepted EC 3.7.1.25; S5 is then built on that foreign intermediate. The main chain is partly established but needs substantial mid-chain revision, so 5 within the allowed D2 range &#91;1,6&#93;.

<details><summary>V0.4理由与本行变化背景</summary>

主链甲苯→对甲酚→4-甲基儿茶酚→间位(extradiol)开环半醛→水解(释甲酸)→水合→醛缩生成丙酮酸+丙醛，方向与连续性正确，与gold六步化学一致；S2以苯酚羟化酶完成对甲酚邻位羟化、S4中间体按2,4-二烯酸命名（gold记2,5-二烯），均属合理表达/替代，不构成起始步错误或不守恒。主要扣项：S1/S2/S3仅列部分氧化还原辅因子（NADH/O2在列，NAD+/H+产物未列）属局部计量缺陷（八.辅因子条款，7–8档内处理），S7额外下游步不计入定档。故8分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：Gold S02 is 2-hydroxy-5-methyl-6-oxohexa-2,4-dienoate -&gt; (2Z)-2-hydroxyhexa-2,5-dienoate + formate; it does not support the answer&#x27;s 2,4-dienoate product.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_019：Gold S02 hydrolase is EC 3.7.1.25; answer S4 is EC 3.7.1.9. This supports a mid-chain enzyme/product revision, not a D5 citation cap.

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分8 → V0.5新分3，变化-5。

新裁判理由：

> Within the D-KEY4 restricted &#91;1,4&#93; range, one confirmed KEY target failure is retained: the S02-corresponding answer step uses EC 3.7.1.9 and yields a foreign 2,4-dienoate product, whereas gold S02 requires EC 3.7.1.25 and 2,5-dienoate. Several other target enzyme claims remain pair/alignment unresolved. Exact matches at other steps do not erase the key failure, so 3 rather than the 4 upper bound.

<details><summary>V0.4理由与本行变化背景</summary>

关键步骤酶-反应对应总体可靠：S1 toluene-4-monooxygenase(1.14.13.236)、S3 catechol 2,3-dioxygenase(1.13.11.2)、S5 2-oxopent-4-enoate hydratase(4.2.1.80)、S6 4-hydroxy-2-oxovalerate aldolase(4.1.3.39)均与gold对应或落在gold多注集合内；S2 phenol 2-monooxygenase(1.14.13.7)与S4 2-hydroxymuconate-semialdehyde hydrolase(3.7.1.9)相对gold(1.14.13.236/3.7.1.25)为替代，化学角色合理但因EVIDENCE_GAP无法核验accepted name/reaction。属“主要步骤有可靠支持、少量条目需进一步确认”档，8分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_019：Gold S02 uses 2-hydroxymuconate semialdehyde hydrolase EC 3.7.1.25; it does not support EC 3.7.1.9 for this target.
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：Gold S02 product is (2Z)-2-hydroxyhexa-2,5-dienoate plus formate; the answer&#x27;s 2-hydroxyhexa-2,4-dienoate is a foreign product.
- ANSWER_TEXT / ANSWER：Answer text locates the S4 enzyme/product and S5 substrate; used only as the evaluated answer text.

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分8 → V0.5新分7，变化-1。

新裁判理由：

> Step-level organisms are plausible and mostly strain-appropriate: P. mendocina KR1 for Tmo, P. putida mt-2 for TOL meta-cleavage enzymes, and Pseudomonas sp. CF600 for dmp phenol hydroxylase. The answer explicitly denies a single whole-path strain and leaves complete_pathway_organism_profile_id null. However CF600&#x27;s p-cresol step and several mt-2 step attributions are not directly confirmed in the gold organism rows or E0, and TaxIDs/collections are null, so 7 rather than 8-9.

<details><summary>V0.4理由与本行变化背景</summary>

分步微生物归属使用真实物种/菌株（P. mendocina KR1、Pseudomonas sp. CF600、P. putida mt-2），且route_scope.notes与uncertainties明确声明“各步代表菌拼装、非同一菌株独立完成全程”，complete_pathway_organism_profile_id=null，正确区分身份定位≠反应级能力≠完整路径能力；TaxID一律null属诚实未知。无编造编号、无由序列推断整条路径。扣项：菌株级能力声称依赖文献定位而EVIDENCE_GAP下无法核验，兼之部分菌株与gold代表菌不同，属少量需确认，8分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_019：Shows gold representative organisms for specific steps, including KR1 for S01 and other organisms for later steps; it does not make all alternative representative assignments invalid.
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_019：Species-name identity crosswalk only; does not establish strain-level catalytic capability.

</details>

### D4 性状科学性：7 / SCORED

V0.4旧分5 → V0.5新分7，变化+2。

新裁判理由：

> Most filled traits are plausible and consistent with same-species representative records where available: P. putida is mesophilic, rod-shaped, Gram-negative, motile, non-sporulating, and has relevant aromatic carbon-source/enzyme traits. Many strain-level values for P. mendocina KR1 and CF600 rest on internal knowledge or low-confidence generic Pseudomonas traits; pH, salinity, genome, and collection are left null. No clear numerical or identity error is visible, but several entries need verification, so 7.

<details><summary>V0.4理由与本行变化背景</summary>

部分性状有针对性与诚实优点：ORG_001的F8（KR1经对甲酚→对羟基苯甲酸→原儿茶酸方向）与F9（TmoABCDEF活性）贴合所指菌，盐度/pH/保藏号/基因组等未知项按null与unknown如实留空。主要短板：三个不同菌株的F1/F6/F10/F11/F12/F13/F2几乎以同一套属级常识（EVID_006=INTERNAL_KNOWLEDGE_ONLY）统一填写，属“把物种/属级一般性状推广到具体菌株”而缺菌株级证据；F2_temperature 将“实验室常规约30°C培养”写入optimum_c，属把培养温度当最适温度（四.4/P52）。属“部分性状准确且适用，但关键项证据不足或条件解释需修订”档，取5分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_019：Species-level P. putida records support several generic traits; KR1 and CF600 rows are largely UNKNOWN, so they cannot verify strain-specific values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_019：Marks which trait rows are observed/scoreable and which are completeness-only; used to avoid treating missing or predicted background as observed accuracy.

</details>

### D5 来源与可核查性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> Core route, enzyme, and step-organism claims carry specific bibliographic or database locators EVID_001-EVID_005, but the E0 case slice is an EVIDENCE_GAP, so their actual support content cannot be verified. Many trait claims use EVID_006 INTERNAL_KNOWLEDGE_ONLY, and the application-critical oxygen-tolerance traits lack an external source. No verified mis-citation exists, so no cap applies; D5 is 6 for partial traceability.

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07、CG04）均有条目级可定位文献来源：EVID_002(Whited &amp; Gibson 1991 J Bacteriol 173:3010-3016)、EVID_004(Shingler 1992 J Bacteriol 174:711-724)、EVID_005(Harayama &amp; Rekik 1990 Mol Gen Genet 221:113-120)、EVID_003(KEGG map00623)、EVID_001(MetaCyc路线名)，各步绑定evidence_id映射清楚，故非“全部笼统来源”，不进3–4档。但本案EVIDENCE_GAP，所引文献/编号均无法核验其是否支持具体声称→UNRESOLVED_SOURCE；性状（尤其一般性状）主要靠EVID_006=INTERNAL_KNOWLEDGE_ONLY→MISSING_SOURCE，证据链薄弱。无已核实错引，不触发CRITICAL/SYSTEMIC cap。属“部分关键结论可定位、其他模块仍缺映射/核验”档，5分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Delivered evidence registry and per-fact evidence_id links; used to judge traceability, not to verify the underlying science.
- RUBRIC_CLAUSE / D5_SOURCE_STATUS：Applies six-state claim-group source registration and no-verified-mis-citation handling.

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> The answer clearly separates representative step organisms from a single whole-path strain, leaves complete_pathway_organism_profile_id null, labels confidence high/medium/low, lists uncertainties, marks alternative branches as not part of the scored main route, and discloses inferred or uncertain steps such as XylJ/XylQ and the multi-strain assembly. Some medium-confidence enzyme assignments remain stronger than the frozen evidence supports, but there is no systematic prediction-as-observation or concealed contradiction, so 8.

<details><summary>V0.4理由与本行变化背景</summary>

不确定性披露较具体诚实：uncertainties五条明确“各步代表菌拼装、无单一菌完成全程、保藏号/基因组号/TaxID未能确认一律null、一般属级性状以内部知识填写并标低置信”，每步带uncertainty，confidence按high/medium/low/unknown分级，alternative_branches各标is_part_of_scored_main_route=false明确排除于主链。少量单点问题：部分文献支持范围待核却标high/medium、F2将培养温度写入optimum_c仍有误导风险（属档内扣，非系统性误导）。属“大部分证据性质已标注、主要限制已说明”档，7分。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：Uncertainty, confidence, alternative-branch, and representative-strain disclosures; used only for evidence-boundary quality.

</details>

## Qwen

答案SHA256：`83dedb138c1e12e8e5a9ec35c35c526c1a016cdda84fe602a2d81706c9df46fd`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 题面指定的路线名被原样回填，氧条件为 aerobic；答案交付 6 个 step，每步均给出主底物/主产物、酶及微生物，并按同一物种+菌株只保留一个 organism_profile；15 项性状字段均出现，未知项按任务允许填 null。仍有少量复杂中间体 SMILES 为 null、部分性状为 null，但这是题面允许的未知表达，属少量局部缺陷，不构成模块缺失或任务路线改选。

<details><summary>V0.4理由与本行变化背景</summary>

任务要求的六步主链（每步主底物/主产物英文名+SMILES、首选酶+EC、对应微生物）、15项性状与证据登记均实质交付；route_scope.chosen_route_name与题面逐字一致，未改选路线；单一菌已按species+strain去重为ORG_001并由step.microorganism.organism_profile_id引用。仅见少量遗漏：steps&#91;S3&#93;.products&#91;0&#93;与steps&#91;S4&#93;.substrates&#91;0&#93;的SMILES为null，未满足“主底物/主产物给SMILES”的字段要求。属“大部分必要内容完整、仅少量遗漏”，7–8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案回显指定路线名、aerobic 条件、6 个步骤、酶/微生物字段、单一 organism_profile 及 15 项性状字段。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_019：该题冻结路线名为 Toluene degradation II (aerobic) (via 4-methylcatechol)，与答案 route_scope.chosen_route_name 一致；支持 D1 的路线名符合性核对。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_019：冻结题级记录显示 ordered_step_count=6，与答案交付 6 个 step 的规模相当；仅用于完整性规模核对，不作为化学正确性证明。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 前段甲苯→4-甲基苯酚→4-甲基邻苯二酚及 4-甲基邻苯二酚开环的主干化学与冻结路线基本相接，但后段出现实质问题：S4 的产物与 gold S02 产物不一致；S5 将 4-methyl-2-oxopent-4-enoate 的“hydration”写成生成 4-hydroxy-2-oxopentanoate + formaldehyde，底物+H2O 与产物总氧数不守恒，且未说明该额外裂解/氧化还原来源；S6 最终给 pyruvate + acetaldehyde，而 gold 终点为 pyruvate + propionaldehyde。主链末端化学被改变，属关键化学转化/计量缺陷，D2 只能落在低档；前段正确性使其不降至 1，取 4。

<details><summary>V0.4理由与本行变化背景</summary>

前段与gold一致：S1 toluene→4-methylphenol、S2 4-methylphenol→4-methylcatechol（单加氧，方向正确）、S3 4-methylcatechol经meta开环生成2-hydroxy-5-methyl-6-oxohexa-2,4-dienoate类半醛，与gold S01/S03/S05相符。后段需实质修订：S5标为hydration（EC 4.2.1.80水合酶）却释出formaldehyde并把C6底物降为C5产物，水合反应不能生成甲醛且产物侧氧计量多1（底物C6H8O3+H2O vs 产物C5H8O4+CH2O），无任何说明；S6据此给pyruvate+acetaldehyde，与gold该步(S)-4-hydroxy-2-oxohexanoate→pyruvate+propionaldehyde不符。主干成立、后段两步骤连接与计量需修订、合理性证据仅内部知识，按“主干部分成立、关键转化仍需修订”5–6档取5；不构成已核实关键错误，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案 S5 将 hydration 写成生成 C5 酸 + formaldehyde，S6 生成 pyruvate + acetaldehyde；支持原子计量与终点化学核对。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：冻结反应行支持 S06 的 hydratase 反应生成 (S)-4-hydroxy-2-oxohexanoate，以及 S04 aldolase 生成 pyruvate + propionaldehyde；不支持答案 S5 的 formaldehyde 生成与 S6 的 acetaldehyde 终点。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_019：冻结题级终点为 Propionaldehyde|Pyruvate；支持 D2 终点产物核对。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> 按 6 个必答目标步核对：S01、S03 路线结构匹配但答案显式 EC 分别 1.14.13.230、1.14.13.109，与 accepted 集合中的 1.14.13.-/1.14.13.236 不匹配且未核，属 U；S05 的 catechol 2,3-dioxygenase/EC 1.13.11.2 虽在 accepted 集合中，但该步产物表示/身份仍 UNKNOWN，属 U；S02、S04、S06 在答案中无可绑定目标反应，按程序事实为 MISSING，其中 S04 为冻结 KEY_TERMINAL。因此 S=0、M=3、U=3，C=S/N=0/6=0，落在 C04 的 C&lt;0.20 候选带 &#91;1,2&#93;。S01/S03/S05 仍有可定位的 accepted 酶名/EC 局部信息，故取 2 而非 1；但无任何目标步达到已确认 S，且关键末端缺失，主线目标酶推荐仍失效。此低分由 M/U 与 D-KEY4 末端缺失承载，不另行签 key_error=Y。

<details><summary>V0.4理由与本行变化背景</summary>

有合理候选与部分支持：S3 catechol 2,3-dioxygenase EC 1.13.11.2与S5 EC 4.2.1.80与gold对应步骤的酶-EC一致。但多个关键酶号未核或与gold不同：S1 toluene 4-monooxygenase EC 1.14.13.230（gold S01为1.14.13.236/通配1.14.13.-）、S2“4-methylphenol monooxygenase”EC 1.14.13.109（gold该步为toluene 4-monooxygenase EC 1.14.13.236）、S4 EC 3.7.1.9（gold为3.7.1.25）、S6 EC 4.1.3.39（gold同一步并列4.1.3.43与4.1.3.39，底物为C6羟基酮酸）；且S5把EC 4.2.1.80水合酶用于释出甲醛的转化，酶名与所声明反应类型不自洽。属“有合理候选和部分支持、若干关键步骤仍缺具体核验”，5–6档取5；EC差异未经冻结证据核实，不cap、不判虚构。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / &#91;PRIVATE_ANONYMOUS_ID_REDACTED&#93;：答案各步酶名/EC：S1 1.14.13.230，S2 1.14.13.109，S3 1.13.11.2，S4 3.7.1.9，S5 4.2.1.80，S6 4.1.3.39；支持 EC 配对与目标绑定核对。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_019：冻结酶表支持各步 accepted 酶名/EC 范围：S01=1.14.13.-/1.14.13.236，S02=3.7.1.25，S03=1.14.13.236，S04=4.1.3.39/4.1.3.43，S05=1.13.11.2，S06=4.2.1.80；用于判断答案 EC 是否在 accepted 集合内。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：冻结反应行支持 S01/S03/S05 的结构匹配、S02/S04/S06 的目标反应与产物边界；用于核对哪些答案步骤可绑定、哪些目标缺失或表示未定。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> P. mendocina KR1身份在gold S01的toluene 4-monooxygenase行出现，属合理候选且无已核实矛盾；但答案将同一菌用于全部6步并声明complete_pathway_organism_profile_id=ORG_001。gold仅S01有KR1对应，下游步级归属与全路径能力无E0支持，gold PATHWAY_COMPLETE代表为Ralstonia pickettii 329。按D3b 5–6档取5：合理候选、部分支持，但多个关键作用范围未核。

<details><summary>V0.4理由与本行变化背景</summary>

身份层有真实支持：gold的organism_gold在S01 toluene 4-monooxygenase下确列“Pseudomonas mendocina KR1”（EXACT匹配，No TaxID），答案的物种+菌株与该记录一致，未编造TaxID（填null）。但作用范围层未核：答案以同一ORG_001承担S1–S6全部步级归属，并置complete_pathway_organism_profile_id=ORG_001，等于声称该菌完成整条路径；gold S02–S06列出的对应菌为Ralstonia pickettii、Stenotrophomonas sp. DDT-1、Comamonas testosteroni、Rhodococcus jostii、Pseudomonas putida NCIB 9816-4/ND6等，gold未在其余步骤列出KR1，但gold非穷尽、缺列不等于反证，故属“尚未充分核验”而非已核实错配。答案全部证据为内部知识，无反应级或全路径能力证据。按“部分支持、若干关键作用范围未充分核验”5–6档取5，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_019：P. mendocina KR1出现在S01的toluene 4-monooxygenase行；PATHWAY_COMPLETE行是Ralstonia pickettii 329；不证明KR1完成全路径，也不证明KR1不能完成。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 性状15项字段齐全，9项填写、6项明确null，完成度可评；但9项均依赖EVID_002的INTERNAL_KNOWLEDGE_ONLY，无单位/条件来源。trait_gold对P. mendocina KR1全部为UNKNOWN，不能确认也不能判错。给定性状多为Pseudomonas属级常识，菌株级适用性未核。按D4 5–6档取5：部分性状可能合理，关键证据不足。

<details><summary>V0.4理由与本行变化背景</summary>

15项性状字段全覆盖，其中9项给出定性值、6项为诚实null（F2/F3/F4/F5/F14/F15），诚实null不在D4重复重扣（完成度归D1）。已给性状为属/种层面的一般描述（好氧、aerobic respiration/O2、toluene、toluene degradation via 4-methylcatechol、toluene 4-monooxygenase活性、motile、rod-shaped、Gram-negative、non-spore-forming），与Pseudomonas属常识相容且不产生筛选误导，F7/F8/F9与gold S01把KR1列为toluene 4-monooxygenase对应菌相容。但全部性状均无条目级来源（EVID_002为内部知识），trait_gold对KR1整列为UNKNOWN、无观测值可比，关键定量性状（温度/pH/盐度/基因组/保藏号）全为null。属“部分性状准确且适用、关键项证据不足”，5–6档取6；未见已核实数值离谱或把物种观测机械推广成菌株极限的情形，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_019：P. mendocina KR1的trait行为UNKNOWN；不能用物种级常识回填菌株级观测，也不能据此判答案错。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_019：该mask用于说明哪些trait子字段可计分；KR1相关行无observed值，不能把字段填写当已核正确。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 路线、酶/EC、菌株身份、路径能力与性状均挂在EVID_001/EVID_002，source_type=INTERNAL_KNOWLEDGE_ONLY，无database/record_id/locator。按P34属MISSING_SOURCE；decision-relevant组均无条目级外部来源。无已核实错引，不能判VERIFIED_MIS_CITATION。D5 1–2档：几乎无法定位重要结论依据；因有局部evidence_registry结构且诚实标internal/low，取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

答案仅登记EVID_001、EVID_002两条，source_type均为INTERNAL_KNOWLEDGE_ONLY，database=null、record_id=null、locator为“Internal knowledge of …”，全部claim组（含决策相关CORE/APPLICATION_CRITICAL组）无可定位条目，按四.3六状态属MISSING_SOURCE（缺失而非误导，默认不cap），决策相关组全部缺失→低分档。答案未伪造编号/条目、也未把内部知识包装成数据库直查，故取2而非1。E0为整题EVIDENCE_GAP，无可核实错引，无CRITICAL/SYSTEMIC，severity_overall=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案一致把证据标为INTERNAL_KNOWLEDGE_ONLY、confidence=low/unknown，6项未知性状用null而非编造，并列出uncertainties及缺失SMILES。主要限制说明较清楚；但仍将complete_pathway_organism_profile_id与route_summary表述为完整路线，未充分展开其内部知识不确定性，属局部过强而非系统性误导。D6 7档：大部分证据性质正确标注，少量边界需修订。

<details><summary>V0.4理由与本行变化背景</summary>

披露具体且诚实：全文confidence统一low/unknown，steps&#91;&#93;.uncertainty逐步说明酶与菌株归属基于内部知识、复杂中间体SMILES缺失、副产物归属基于内部知识；uncertainties列出“未提供外部数据库记录/复杂中间体SMILES缺失/4-甲基邻苯二酚下游副产物归属基于内部知识”，并明确formate/formaldehyde/acetaldehyde后续不计入题面主链。未把预测包装为观测，未掩盖未知。不足：complete_pathway_organism_profile_id=ORG_001与is_single_continuous_route=true未加“能力待核”说明，且未把“预测/推断/未知”分层标注而统一记low。属“大部分观测/预测/未知被正确标注、主要限制已说明”，7–8档取7；非系统性误导，不cap。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`364f2335c2bfaf3f4d034c0e86eb039487cda91389a1de0684fb190e2d329a69`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 模块交付和15项性状均出现，路线名与氧条件正确；但主链中段采用4-甲基儿茶酚下游的脱氢酶/脱羧支路，未按gold指定S02水解酶与S06水合酶主链交付，任务指定主链符合度受关键偏离限制，按D1允许范围&#91;1,4&#93;取上沿4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：gold六步主链包含S02水解酶和S06水合酶；不支持把答案的脱氢酶/脱羧支路直接当作该主链完成。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S8&#93;：答案确实交付了连续路径、酶、微生物和性状，但在S4-S8改为脱氢酶/脱羧支路。

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1-S8的碳骨架和主氧化还原流大致连贯，终产物丙酮酸与丙醛和gold终点一致；但S4-S8为甲基化meta-裂解脱氢/脱羧支路，与gold水解酶/水合酶路径不同，且部分同系物催化依赖类比，D2允许范围&#91;1,6&#93;内取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：gold主链给出S02水解、S06水合及S04终裂解的方向；答案在这些位置使用不同的脱氢/脱羧中间体。
- ANSWER_TEXT / ANSWER.steps&#91;S1-S8&#93;：答案的替代支路在碳数和终产物上可闭合，但并非gold线性主链。

</details>

### D3a 目标反应与酶对应：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按可读名称/EC裁判：S01、S03与accepted完全匹配；S04终裂解和S05开环的名称/EC与accepted集合匹配，表示差异按等价处理；S02所答为EC 1.2.1.85脱氢酶而非accepted EC 3.7.1.25水解酶，S06底物2-oxohex-4-enoate未与gold S06底物绑定。支持4/6，非KEY主要失败2项，落&#91;5,6&#93;取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_019：gold S01/S03接受toluene 4-monooxygenase EC 1.14.13.236，S05接受catechol 2,3-dioxygenase EC 1.13.11.2，S04接受EC 4.1.3.39/4.1.3.43；S02接受EC 3.7.1.25水解酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：gold S02为水解生成2-hydroxyhexa-2,5-dienoate和formate，S06为相应水合；不支持把S02脱氢反应和S06不同C6底物直接计为目标步完成。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P. mendocina KR1与P. putida mt-2均为真实相关菌株；答案把上段与下段分菌并置complete_pathway=null，避免整路冒充。扣分点是KR1/mt-2的ncbi_taxid 300/303为种级而非菌株级，且S2用KR1的二次羟化生理主通量未确认；按身份阶梯档内扣，不判cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_019：gold支持若干步骤的真实菌株归属；对Pseudomonas mendocina KR1与Pseudomonas putida mt-2的菌株级TaxID未给出，种级TaxID不等于菌株级记录。
- ANSWER_TEXT / ANSWER.uncertainties：答案明确说明上下段并非同一菌株，complete_pathway为空，属于限制披露而非整路能力冒充。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 两profile各15项均出现，4项明确null；P. putida种级通用性状与gold种级记录大致一致。P. mendocina KR1缺少冻结种/株性状记录，其运动、形态、革兰、中温、好氧、碳源等主要来自属级内部推断，数值项留空。关键项证据不足但未编造数值，D4=6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_019：gold对P. putida 303有部分种级观测性状；P. mendocina KR1行多为UNKNOWN，不能由gold回填KR1菌株级性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_019：pH、盐度、温度端点等子字段多为completeness_only或pending，数值缺失可按明确未知处理，不等同错误。

</details>

### D5 来源与可核查性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry给出EVID_001-EVID_011；多个酶-EC有KEGG条目定位，但S2、微生物归属和多数性状仅INTERNAL_KNOWLEDGE_ONLY；E0为GAP，无法核验引用内容。按实际交付记录：部分关键结论可定位、其他模块缺条目级来源或可用核验，D5=5，不判错引。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案交付了KEGG record_id与若干INTERNAL_KNOWLEDGE_ONLY条目；支持记录存在性主张，不证明各引用内容已被核验。
- ANSWER_TEXT / ANSWER.uncertainties：答案披露混合菌株和同系物类比，有助于D6，不补足D5缺失的条目级来源。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> uncertainties明确写出上下段并非同一菌株、KR1主通量不确定、S4-S8同系物类比、保藏/基因组/温盐pH无可靠来源；evidence_registry区分DATABASE_DIRECT与INTERNAL_KNOWLEDGE_ONLY，null使用克制。少量TaxID/EC高置信属单点过度，不构成系统性误导，D6=8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案逐条披露混合菌株、主通量不确定性、同系物类比及数值缺失，支持D6高分。
- ANSWER_TEXT / ANSWER.evidence_registry：答案区分DATABASE_DIRECT与INTERNAL_KNOWLEDGE_ONLY并标注置信度，便于判断证据性质；不证明引用内容真实。

</details>

## GPT5.6

答案SHA256：`954af7317387064d70feceb575232c0427a91e5d288a6a67fa051958ee191b93`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求经4-methylcatechol的六步主链并到pyruvate/propionaldehyde；答案只给三步，止于3-methyl-cis,cis-muconate，缺失S02、S04（终点步）、S06并替换S05，属核心任务模块缺失和路线偏离，落在D1 &#91;1,4&#93;受限档内取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_019：确认ordered_step_count=6及主链为六步任务；不支持把三步答案视为完整主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：定义各必答步底物/产物及S04终点产物；不支持3-methyl-cis,cis-muconate作为本题终点。
- ANSWER_TEXT / ANSWER.steps：答案只交付三步且止于3-methyl-cis,cis-muconate；未交付S02/S04/S06。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1 toluene→p-cresol与S2 p-cresol→4-methylcatechol的方向和结构与gold前两步相符；但S3以catechol 1,2-dioxygenase生成3-methyl-cis,cis-muconate，异于S05的2-hydroxy-5-methyl-6-oxohexa-2,4-dienoate，且未延续到S02/S06/S04终点。主链部分成立但关键中段/连续性仍需实质修订，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：支持S01与S03的底物/产物/方向；S05产物与答案S3不同，且S02/S06/S04未交付。
- ANSWER_TEXT / ANSWER.steps：答案化学止于3-methyl-cis,cis-muconate，未连到指定终点。

</details>

### D3a 目标反应与酶对应：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按gold/accepted集合逐目标核对：S01名称为toluene 4-monooxygenase但EC 1.14.13.148不在accepted且无E0记录，为U；S02/S04/S06未交付为M；S03的p-Cresol hydroxylase无EC且不在accepted名集，为U；S05用catechol 1,2-dioxygenase/EC 1.13.11.1并生成3-methyl-cis,cis-muconate，与gold S05的catechol 2,3-dioxygenase/2-hydroxy-5-methyl-6-oxohexa-2,4-dienoate不符，为目标反应失败。存在明确KEY漏答/失败，D-KEY4使上界≤4；可用与失效边界仅勉强可分，取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_019：列出各步accepted酶名/EC；S01 accepted为1.14.13.-/1.14.13.236，S05 accepted为catechol 2,3-dioxygenase/1.13.11.2；不证明 .148 或 1.13.11.1 对目标步成立。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_019：确认S02/S04/S06为必答步及S05目标产物；答案缺S02/S04/S06且S05产物不同。
- ANSWER_TEXT / ANSWER.steps：显示答案的酶/EC与目标步对应关系；不足以把S01/S03升为S，也显示S05与目标产物不同。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S01使用Pseudomonas mendocina KR1与gold organism_gold中该步EXACT身份相符，但未给TaxID；S02/S03把同一菌株用于p-cresol羟化和4-methylcatechol裂解，缺少相应步级能力证据。身份定位不等于步级能力或整条路径能力；有合理候选和部分支持但多个能力未核，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_019：支持S01的KR1身份名称，不支持已给TaxID或S02/S03各步能力；S03/S05 gold行未列KR1。
- ANSWER_TEXT / ANSWER.organism_profiles：答案未给TaxID，且把同一profile用于三步。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> P. mendocina KR1在trait_gold中无可用观测值，E0也无KR1性状记录；答案对温度/pH/盐度/保藏/基因组等8项如实null，对好氧、革兰氏阴性、不产芽孢、甲苯氧化/T4MO等给出泛化描述。多数已填项方向合理但缺少菌株级条件与定量证据，且F8‘相关芳香族化合物’较raw_text外推；取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_019：显示冻结trait_gold中KR1行多为UNKNOWN，不能核实具体菌株性状或数值。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_019：KR1各主要性状在冻结掩码中不可作为observed accuracy分母；不支持把答案性状当已核实。
- ANSWER_TEXT / ANSWER.organism_profiles：显示7项有值、8项明确unknown/null，以及F8泛化措辞。

</details>

### D5 来源与可核查性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> EVID_001为无作者/年份/DOI的泛化研究描述，EVID_002仅KEGG名且record_id为null，EVID_003仅NCBI taxonomy泛称且无TaxID；关键路线、酶-EC、微生物与性状结论均不能由实际条目定位核对。属决策相关组仅笼统来源，E0下不判虚构/错引，取3–4档下沿3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：显示来源为泛化文献/数据库名称，缺少可定位记录ID；不能支持条目级可核对结论。

</details>

### D6 不确定性与诚实度：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案给多数未知项null/unknown，明确披露p-Cresol hydroxylase EC未确认及KR1性状/基因组未逐项确认，部分confidence为low/medium；但route_scope称单一连续路线且route_summary未披露只完成三步/未达题面终点，部分能力/来源表述强于证据。属有不确定性说明但局部结论强度超过依据，取6。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：显示部分未知和EC未确认被披露；也显示未披露主链未完成/终点偏离。

</details>
