# BIOPATH150_086：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：3-sulfopropanediol degradation I

污染物：(S)-2,3-dihydroxypropane-1-sulfonate；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 43.5 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 42.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 53.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 35.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 46 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 25 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`5d4989c2cfa6234b7e7232a02bc7b991b03356cfcd3d32e60738662ec20383ac`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案格式和模块基本齐全（steps、organism_profiles、15项性状、evidence_registry均有），chosen_route_name也原样填写；但其实际主链与题面指定路线的gold主链明显不对应：gold为3步至(R)-3-sulfolactate，答案S1先将DHPS生成(S)-3-sulfolactaldehyde，S2生成(S)-3-sulfolactate后继续延伸至乙酰磷酸/亚硫酸盐，起始产物、终端产物和步序均不一致。该偏离属于D1任务路线/主链符合度关键错误，最高4；考虑交付结构完整、模块齐全，取4。

<details><summary>V0.4理由与本行变化背景</summary>

覆盖登记：路径/酶/微生物/性状/来源/不确定性均有内容；15项性状填写10项、明确未知5项、遗漏0；5步中4步EC为null。JSON合法、路线名与氧条件按题面原样填写。但交付主链化学（首步C3伯醇氧化、中间体、终点乙酰磷酸+亚硫酸盐）与题面指定路线3-sulfopropanediol degradation I的gold实际步骤（3步、终点(R)-3-sulfolactate）不同，属P100自称合规却交付不同化学路线的任务参数偏离，触发本维关键错误；因模块完整，cap档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：gold root为(S)-DHPS，terminal主产物为(R)-3-sulfolactate
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_086：gold ordered_step_count=3，LINEAR_UNIQUE
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_086：gold三个必答步酶名为(R)-sulfopropanediol 2-dehydrogenase、sulfopropanediol 3-dehydrogenase、(S)-sulfopropanediol 2-dehydrogenase
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：gold S01/S02/S03的底物产物与方向；答案S1-S5反应不对应
- ANSWER_TEXT / ANSWER.steps.S1-S5：答案自述的DHPS→sulfolactaldehyde→sulfolactate→sulfopyruvate→sulfoacetaldehyde→acetyl phosphate主链

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案自身化学链基本连续：S1-S3为醇/醛氧化并给出NAD+/NADH，S4脱羧，S5为Xsc裂解并给出EC 2.3.3.15，底物产物连接和原子计量大体成立；S5的EC与E0官方同酶条目同名对应。但关键中间体为(S)-3-sulfolactate，而gold终端为(R)-3-sulfolactate，存在显式立体化学冲突，且主链延伸至gold终点之外；按C06显式立体冲突候选≤5，取5。S4未列TPP等辅因子按P103局部计量问题处理，不另行cap。

<details><summary>V0.4理由与本行变化背景</summary>

五步各步化学（伯醇→醛→酸、2-羟酸→2-酮酸、脱羧、C–S磷酸解）内部自洽、方向与连接基本成立，含NAD+/磷酸辅因子，未见方向反转或明显不守恒；但相对指定路线gold的关键中间体与首个转化需修订，且全凭内部知识无独立证据，按合理替代路线四步判断登记为未证实。主干部分成立但关键转化需修订、合理性证据有限，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：gold terminal为(R)-3-sulfolactate，答案S2给出(S)-3-sulfolactate
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：gold S02方向为(2R)-DHPS→(R)-3-sulfolactate；答案S2底物为3-sulfolactaldehyde且产物为S构型
- E0_EVIDENCE / f3e0:tp:EV007-23：官方条目体系中sulfoacetaldehyde acetyltransferase名存在，编号2.3.3.15；支持S5酶名/EC方向，不外推到其他步骤
- ANSWER_TEXT / ANSWER.steps.S1-S5：答案自述的辅因子、产物和反应类型；用于评价自身化学连续性

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> D3a只计目标反应。本题目标N=3：S01/S02为ROUTE_HOLD_REPRESENTATION（UNRESOLVED），S03为ROUTE_BLOCKED_MISSING。答案S1-S5的酶名/EC与accepted集合不对应：S1为(S)-3-sulfopropanediol dehydrogenase但无EC且产物为(S)-3-sulfolactaldehyde；S2为醛脱氢酶；S3为3-sulfolactate dehydrogenase；S5 Xsc EC 2.3.3.15不属于本题三个目标步，且S1-S4均无EC。无任一目标步获得S，关键入口S03又为MISSING，目标催化对应几乎不可用。U不自动判F，故不把S01/S02写成已核错误；但无正向目标支持不能抬分。按C04 &#91;1,2&#93;取下沿1。

<details><summary>V0.4理由与本行变化背景</summary>

各步给出酶名（S1–S5），S5附EC 2.3.3.15与gene xsc，S1–S4 EC=null（诚实未知）。命名与反应类型自洽，未见EC大类与反应类型矛盾；但EC/基因多数未核验，属合理候选+部分支持、关键步骤缺具体核验，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_086：gold三个目标步accepted酶名为(R)-sulfopropanediol 2-dehydrogenase、sulfopropanediol 3-dehydrogenase、(S)-sulfopropanediol 2-dehydrogenase
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：gold S01/S02/S03的底物产物与方向；答案S1-S5不匹配目标反应
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：gold主链终点为(R)-3-sulfolactate；答案S2为(S)-3-sulfolactate并继续下游
- E0_EVIDENCE / f3e0:tp:EV007-23：EC 2.3.3.15对应sulfoacetaldehyde acetyltransferase；该事实支持S5酶名/EC，但S5非本题三个目标步，不能据此增加目标D3a信用

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 物种级Ruegeria pomeroyi有gold PATHWAY_COMPLETE(taxid 89184)支持其种级全路径能力，故不是核心身份编造；但答案将同一菌株DSS-3用于全部替代5步，ncbi_taxid与步级能力均未给可定位证据，且gold步级微生物为Cupriavidus pinatubonensis。属5-6档下部：部分合理候选与种级支持，但菌株级身份、步级归属和全路径范围仍有多处关键未核。

<details><summary>V0.4理由与本行变化背景</summary>

全链用Ruegeria pomeroyi DSS-3，ncbi_taxid=null。该物种在gold organism_gold中为PATHWAY_COMPLETE(taxid 89184)，物种级身份成立；但答案未交付taxid/菌株级证据，gold STEP菌为Cupriavidus pinatubonensis，步级归属未核验。属合理候选+部分支持、关键作用范围未充分核验，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_086：gold步级微生物为Cupriavidus pinatubonensis；PATHWAY_COMPLETE对Ruegeria pomeroyi(taxid 89184)为种级complete，不支持DSS-3菌株级或替代五步归属。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 部分性状与gold R. pomeroyi种级背景一致（如F12革兰氏阴性、F13不产芽孢），且未知项多以null披露；但F10运动性、F11形态、F14基因组等在gold已有观测记录而答案填null，F7/F8/F9/F15等广义性状多为内部知识、缺种/菌株级定位支持。无观测数值离谱或编造，但关键项证据不足，落在5-6档下部。

<details><summary>V0.4理由与本行变化背景</summary>

提供性状多为定性且与gold Ruegeria(89184)一致：F12革兰氏阴性、F13不产芽孢、F1 aerotolerant/好氧、F2中温、F4海洋型可核实/相符；温度/pH/盐度数值、保藏号、基因组均为诚实null（计入D1完成度，不重复扣D4）。F8广谱降解为笼统外推但置信low。关键数值性状缺证据，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_086：gold提供Ruegeria pomeroyi(taxid 89184)种级性状，含gram positive=false observed、sporulation=false predicted等；不代表DSS-3菌株所有性状已核实。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_086：显示R. pomeroyi部分性状子字段为completeness_only或观测缺失；不把缺失自动判为错误。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 决策相关核心组CG01/CG02/CG03/CG05/CG07主要为MISSING_SOURCE/UNRESOLVED_SOURCE：路线与S1-S4酶仅EVID_001 INTERNAL_KNOWLEDGE_ONLY；菌株与性状引EVID_003但为凭记忆自由文本；仅S5 EC 2.3.3.15有具体数据库/record_id且E0确认名称/编号。无已核实错引；核心路线与菌株来源不可定位，按3-4档下部给3。

<details><summary>V0.4理由与本行变化背景</summary>

核心结论（路线、酶-反应、核心菌身份、步级归属）证据均为INTERNAL_KNOWLEDGE_ONLY（EVID_001/002/004），无条目级可定位外部来源；性状仅EVID_003为文献名(González 2003/Moran 2004)但free-text未核验。决策相关组全部MISSING_SOURCE；无经核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，低分档默认不cap，取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV007-23：支持EC 2.3.3.15官方条目中sulfoacetaldehyde acetyltransferase名称/编号存在；不支持R. pomeroyi DSS-3表达该酶或该步属于gold必答步。
- ANSWER_TEXT / ANSWER_BODY：答案自述EVID_001/EVID_002/EVID_003/EVID_004多为INTERNAL_KNOWLEDGE_ONLY或凭记忆；作为D5实际交付来源状态依据。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案整体较诚实：大量null、逐步uncertainty、EVID来源标为INTERNAL_KNOWLEDGE_ONLY并说明凭记忆未核；主要限制与待验证点有列出。不足是部分性状仍以medium/high置信包装内部知识（F12/F13 high、F6/F15 medium），route_summary较断言。属7-8档下部：大部分观测/预测/未知标注清楚，少量置信表达偏强。

<details><summary>V0.4理由与本行变化背景</summary>

答案多处诚实声明内部知识、未核验、编号/数值填null，列出7条不确定性；EVID_003/004明确凭记忆未直接核验。但部分性状(F12/F13)以high confidence呈现未经外部核验内容，属单点偏确信；总体披露较具体、未系统性把预测写成观测。取7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BODY：答案自行披露内部知识、null与不确定项；也暴露部分medium/high置信缺少对应定位来源。

</details>

## DeepSeek

答案SHA256：`e2fc96b2d62aad9e6ba48ac34496aafe7e7161e5069cb17b6e4fe9dc488e0495`。

### D1 完整性与任务符合度：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> 答案覆盖了路径、酶、微生物、15项性状等主要模块，route_scope 也原样写了题面路线名；但主链交付不完整：答案只明确交付了到 3-sulfolactate 的氧化序列，并把 3-sulfolactate 裂解为 pyruvate/sulfite 作为第三步主链，未交付 gold 所定终点 (R)-3-sulfolactate 及任务范围中的 3 个必答目标步的完整对应；这属于若干必要内容遗漏/范围偏移，不是科学维度对错本身。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块全覆盖：3步路径、每步酶与EC、对应微生物、15项性状、证据自登记，格式可解析，route_scope.chosen_route_name原样填写。但题面指定路线名“3-sulfopropanediol degradation I”下交付的化学主链与冻结gold定义的该路线不同：gold首步(S)-DHPS→1-hydroxy-2-oxo-3-sulfopropane，第二步→(R)-2,3-DHPS，第三步→(R)-3-sulfolactate；答案三步为DHPS→3-sulfolactaldehyde→3-sulfolactate→pyruvate+sulfite，中间体与酶集合全不同，且未声明替代路线/范围边界（自称route I），证据仅内部知识。按P100“自称合规却交付不同化学路线”属D1关键错误：cap≤4；其余交付完整，档内取上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_086：本题 formal case 为 LINEAR_UNIQUE，ordered_step_count=3；仅支持任务有3个有序主链步这一范围事实，不把全图材料当作旁支分母。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：题面路线名为 3-sulfopropanediol degradation I，gold terminal main product 为 (R)-3-sulfolactate；支持 D1 对任务终点/范围的核对。
- ANSWER_TEXT / e2fc96b2d62aad9e6ba48ac34496aafe7e7161e5069cb17b6e4fe9dc488e0495：答案确实返回3个step并含enzyme/EC/microorganism与15项traits；但第三步是3-sulfolactate裂解为pyruvate+sulfite，且未以downstream_continuation标明，故与本题主链终点范围不完全一致。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案的三个化学转化单独看均可成立：醇氧化到醛、醛氧化到酸、磺基乳酸裂解为pyruvate与sulfite；但相对本题指定主链，第一步产物写成 3-sulfolactaldehyde，未交付 gold S03 的 1-Hydroxy-2-oxo-3-sulfopropane 中间体，也跳过了 gold S01 的还原/差向化连接；第二步给出未标明R构型的 3-sulfolactate，而 gold 终点为 (R)-3-sulfolactate；第三步又把主链延伸到 gold 终点之后。辅因子省略属局部计量缺陷，可档内处理，不足以单独触发cap；但关键中间体、构型/连接和终点边界仍需实质修订，故落在5–6档并取6。

<details><summary>V0.4理由与本行变化背景</summary>

交付路线内部化学自洽：S1伯醇→醛（2电子氧化）、S2醛→羧酸、S3 sulfolactate→pyruvate+sulfite，原子与电荷计量基本成立；未列NAD(P)+/H+属局部计量缺陷（P103，不自动cap）。但相对题面指定的route I，首步氧化位点不同（答案C1醛 vs gold C2酮），关键中间体与连接不符合该路线；S2产物为未注明立体化学的3-sulfolactate，与gold终点(R)-3-sulfolactate仅名称级对应；S3为终点下游延伸（P29不据此扣覆盖率，也不加分）；替代路线无任何可核证据（INTERNAL_KNOWLEDGE_ONLY）。按5-6档“主干部分成立，但关键中间体、转化或连接仍需修订；合理性证据有限”取5；路线偏离已在D1独立判KE，本维不重复cap，仅共用RE-01登记。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：gold reaction rows 支持本题主链的S03（(S)-2,3-dihydroxypropane-1-sulfonate → 1-Hydroxy-2-oxo-3-sulfopropane）、S01反向表示、S02到(R)-3-sulfolactate以及终点方向事实；不扩展到答案未交付的替代路线。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：支持本题指定主链终点为 (R)-3-sulfolactate，而非pyruvate/sulfite；用于D2终点/连接核对。
- E0_EVIDENCE / f3e0:tp:EV146-11：支持 sulfolactate → pyruvate + hydrogensulfite 的官方编号事实为 EC 4.4.1.24，且对该底物R-构型专一；不核验答案所写EC 4.4.1.27，也不把该事实回填为答案目标信用。
- ANSWER_TEXT / e2fc96b2d62aad9e6ba48ac34496aafe7e7161e5069cb17b6e4fe9dc488e0495：答案给出三步SMILES与反应类型：S1到3-sulfolactaldehyde，S2到3-sulfolactate，S3裂解为pyruvate+sulfite；辅因子未列，S2产物未标明R构型。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> All three required target reactions lack target-credit match. S03 entry substrate is reused in answer S1, but product is 3-sulfolactaldehyde rather than 1-hydroxy-2-oxo-3-sulfopropane; gold S01 intermediate is absent; gold S02 substrate (2R)-2,3-dihydroxypropane-1-sulfonate is absent. Answer enzymes are not the accepted enzyme sets. With S=0 and no usable target catalytic correspondence, C&lt;0.20 supports &#91;1,2&#93;; choose 1.

<details><summary>V0.4理由与本行变化背景</summary>

三个酶名与EC大类和各步反应类型一致（1.1.1醇脱氢、1.2.1醛脱氢、4.4.1 C-S裂解），属合理候选；但EC 1.1.1.398、1.2.1.89、4.4.1.27均无冻结记录（GAP-086-002/004/005）→UNRESOLVED，无官方条目支持其accepted name/reaction。其中S3“3-sulfolactate sulfolyase”的官方现编号为EC 4.4.1.24（EV146-11，系统名(2R)-3-sulfolactate hydrogensulfite-lyase，pyruvate-forming，R-构型专一），答案写4.4.1.27，与官方现编号不一致，属局部编号问题（4.4.1.27无记录、可能为历史/撤转编号，按P73不判虚构）；且无证据表明这些酶在A. tumefaciens C58中催化所写底物。按5-6档“有合理候选和部分支持，但若干关键步骤仍缺具体核验”取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：Gold required structures: S03 S-DHPS to 1-hydroxy-2-oxo-3-sulfopropane; S01 to (2R)-2,3-dihydroxypropane-1-sulfonate; S02 to (R)-3-sulfolactate.
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_086：Accepted gold enzyme names/EC for S01-S03; does not include answer&#x27;s 1.1.1.398, 1.2.1.89, or 4.4.1.27 as target-step accepted pairs.

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> The answer uses Agrobacterium tumefaciens C58 for all steps and declares complete-pathway organism profile ORG_001. Species-level Agrobacterium tumefaciens identity is plausible, but C58 TaxID 176299 and step/pathway capability are not verified in E0; gold target-step organisms are different. This is partial candidate support with key identity/capability still unresolved, fitting 5.

<details><summary>V0.4理由与本行变化背景</summary>

物种名Agrobacterium tumefaciens有物种级已验证映射（crosswalk 358，SPECIES_NAME_IDENTITY_ONLY），是合理候选；但菌株级TaxID 176299无冻结记录（GAP-086-017/018），无法核实菌株身份粒度；三步归属同一ORG_001及complete_pathway_organism_profile_id=ORG_001的整条路径能力声称仅有内部知识，无反应级或全路径证据（P69三层：身份定位≠反应级能力≠完整路径能力）。gold步级菌为Cupriavidus pinatubonensis(248026)、全路径菌为248026/314263/89184，但gold非排他，不能据此判答案菌错误。按5-6档“有合理候选和部分支持，但若干关键身份或作用范围仍未充分核验”取5，不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_086：Gold step organisms and pathway-complete organisms for this case; does not list Agrobacterium tumefaciens C58.
- GOLD_SLICE / verified_species_name_crosswalk.tsv#case:BIOPATH150_086：Supports species-name mapping Agrobacterium tumefaciens to TaxID 358 only; does not verify C58 TaxID 176299 or pathway capability.

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> All 15 traits are present (12 filled, 3 explicit unknown), but no trait evidence IDs/raw_text and no applicable frozen trait reference for A. tumefaciens C58 are provided. Values are low/unknown confidence. No verified contradiction is available, but key evidence is insufficient, so 5.

<details><summary>V0.4理由与本行变化背景</summary>

15项性状结构完整，F4/F5/F14诚实null；关键性状（F2温度optimum 28℃、F3 pH optimum 7.0、F1/F6好氧、F7/F8底物与降解能力）数值本身合理但与全部其他性状一样无来源（evidence_id=null、confidence low），taxid 176299在冻结性状库无记录（GAP-086-037至045），不得用代表记录回填、也不能默认正确（P46）。F9把本答案推断的路径酶直接列为“enzyme activity”，有把推断写成已有活性描述的风险（P115）；F8“降解sulfoquinovose和3-sulfopropanediol”是支撑目标污染物能力的关键声称但零支持。按5-6档“部分性状准确且适用，但关键项证据不足或条件解释需修订”取5；缺失完成度扣分归D1，不重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_086：Trait scoreability rows exist only for Cupriavidus pinatubonensis, Roseovarius nubinhibens, and Ruegeria pomeroyi; no scoreable row for A. tumefaciens C58.

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> Only EVID_001 is supplied, with source_type INTERNAL_KNOWLEDGE_ONLY and null database/record/locator; all trait evidence IDs are null. Decision-relevant route, enzyme, microbe, and trait claims have no locatable source. MISSING_SOURCE low band, no verified mis-citation.

<details><summary>V0.4理由与本行变化背景</summary>

唯一的来源记录EVID_001为source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均null，claim_scope只是条目名列表；按P34登记MISSING_SOURCE（完全无引用或仅内部知识自我声明）。决策相关组CG01/CG02/CG03/CG05/CG07/CG08/CG09均无条目级可定位可核对证据；性状、形态、栖息地、基因组等组同样无来源；无任何可核引用对象，故无已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION，不cap。按“全部缺失→低分档”取2。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> Confidence labels exist, but core route/enzymes/microbe are given medium confidence on internal-only evidence while uncertainties array is empty and no limitations or alternative-route risk is explained. Trait low/unknown labels are better, but core claims still exceed disclosed support. Not systemic; 5.

<details><summary>V0.4理由与本行变化背景</summary>

有逐字段confidence标注：性状多为low、F4/F5/F14为unknown，属于部分不确定性披露；但路线三步以medium confidence包装纯内部知识，uncertainties为空、route_summary为断言式，未说明其主链与gold route I的差异、未列出主要限制与待验证点，也未区分观测/预测/推断（性状无raw_text，未声明数据性质）。属“有不确定性说明但过于笼统、部分结论强度仍超过依据”，5-6档取5；未达系统性把预测写成实证或掩盖已知矛盾，不cap（D5无已核实错引，也不联动降分）。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`1315b7abf5800d0440b99f3883917b0cdc80366beb4296d5647c7424b583c515`。

### D1 完整性与任务符合度：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 答案返回完整 biodegradable_answer_v2 结构：3步主链、逐步底物/产物与SMILES、每步酶/EC与微生物、一个去重 organism_profile、完整15项性状及证据登记；route_scope 原样填写指定路线名，氧条件按题面为 null。主要模块均实质回应。扣分边界是所给主链终点/步骤化学与冻结gold主链未完全对齐（答案至 pyruvate+bisulfite，gold终点为 (R)-3-sulfolactate），但路线诊断为 BOUNDARY_REVIEW、任务符合状态为 OK，不能据此把 D1 直接判为已确认任务偏离；因此落在7–8档，取8因交付完整、仅路线边界待复核。

<details><summary>V0.4理由与本行变化背景</summary>

任务模块完整：路线名原样回显；3 步各含主底物/主产物英文名与 SMILES、一个首选酶与 EC、一个对应微生物；菌按“物种+菌株”去重为 1 条 profile；15 项性状全部返回（12 项有值、3 项明确未知 F3/F10/F14）；5 条 evidence_registry 与逐条 uncertainties。属 7–8 档“大部分必要内容完整、关联清楚”，取 8：扣分仅在 3 项性状以 null 交付（gold 对 314263 的运动性/基因组有观测，属完成度遗漏）及温度/盐度数值与基因组子字段空缺，属少量遗漏。答案主链步骤化学与冻结 pathway 是否同一路线属化学/D2 议题并已入 review_queue，本维不据此连坐cap；未因篇幅或术语加分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_086：冻结formal_cases显示 pathway BSY-p00661、名称 3-sulfopropanediol degradation I、LINEAR_UNIQUE、ordered_step_count=3；支持本题主链长度与图状态，不证明答案化学或终点正确。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：root 为 (S)-2,3-dihydroxypropane-1-sulfonate，gold terminal 为 (R)-3-sulfolactate；用于记录路线终点边界，不能单独据此判答案错误。
- SCOPE_ROW / SCOPE#BIOPATH150_086#CG04：题面氧条件为 null，CG04 condition_met=FALSE、criticality=SUPPORTING；支持氧条件回显，不延伸评价答案化学。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案三步内部化学连续：DHPS氧化为3-sulfolactaldehyde，醛氧化为3-sulfolactate，硫裂解生成pyruvate+bisulfite；方向为降解，未见首步直接开环、无依据跳跃或明显原子不守恒。主要扣分是路线终点与立体化学偏离：冻结gold终点为 (R)-3-sulfolactate，答案生成的是 (S)-3-sulfolactate并继续裂解到pyruvate+bisulfite；且E0证据 f3e0:tp:EV146-11 记录 EC 4.4.1.24 为 (2R)-sulfolactate sulfo-lyase、对R构型专一，与答案使用(S)-3-sulfolactate不符。该问题属于显式立体/路线边界缺陷，按C06候选上限≤5；现有材料未将其核实为D2关键错误，故取5。D2 9–10不适用。

<details><summary>V0.4理由与本行变化背景</summary>

主干方向与计量成立：S1 NAD+ 依赖的 3-位醇氧化→(S)-3-磺基乳醛，S2 醛脱氢→(S)-3-磺基乳酸，S3 硫裂解→丙酮酸+亚硫酸氢盐，C3H6O6S→C3H4O3+H2SO3 计量平衡；无方向反转、无一步跳中心代谢、无原子明显不守恒，SMILES 与所写结构自洽。但存在两处实质缺陷：(a) 与冻结 pathway BSY-p00661 的步骤化学不同——gold 为 2-脱氢→(2R)-DHPS→3-脱氢三步至 (R)-3-磺基乳酸，答案经 (S)-3-磺基乳醛/ (S)-3-磺基乳酸至丙酮酸，答案未声明这是相对指定路线的替代路线，所引 EVID_001/EVID_002/EVID_003 在 E0 无法核验（GAP-086-013/014/015）；(b) 已获官方条目核实的 EC 4.4.1.24 为 (2R)-3-磺基乳酸专一，答案 S3 底物写作 (S)-构型，末步连接按字面不成立。属 5–6 档“主干部分成立，关键中间体/连接仍需修订、合理性证据有限”，取 6。未判关键错误：起始步并非错误起始步，题面未指定终点故不构成“未声明严重偏离指定终点”。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：gold terminal main product 为 (R)-3-sulfolactate；支持答案终点/立体化学与冻结路线终点的边界比较，不等同自动判错。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：反应gold行显示 S02 主产物为 (R)-3-sulfolactate，S03/S01/S02带方向信息；支持gold主链立体化学与终点核对。
- E0_EVIDENCE / f3e0:tp:EV146-11：官方EC 4.4.1.24 为 (2R)-3-sulfolactate hydrogensulfite-lyase（pyruvate-forming），并注明对R构型专一；支持答案(S)-3-sulfolactate使用该EC的立体冲突，不扩展到其他步骤。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分6 → V0.5新分2，变化-4。

新裁判理由：

> 按N=3的本题目标反应：S01、S02 为 ROUTE_HOLD_REPRESENTATION/UNRESOLVED（酶名/EC与accepted对应及路线表示未确认，不能计S，也不自动判F）；S03 为 KEY_ENTRY 且 delivered=null、five_state=MISSING、step_conclusion=REACTION_MISSING_OR_WRONG。故已确认目标S为0，存在1个关键入口目标漏交付，另有2个目标待核。答案确实提供一个可读的三步酶模块（局部信息），但无目标级已确认催化支持，且关键入口步缺失，核心目标推荐失效；落在C05低档。取2而非1，因存在可定位的局部酶/EC与反应信息；不能取3以上，因无目标级可用支持且S03漏交付。

<details><summary>V0.4理由与本行变化背景</summary>

S1 hpsN/EC 1.1.1.337 与 S2 hpsO/EC 1.2.1.86 在冻结证据中无记录（GAP-086-001/003），答案亦自承凭内部知识（EVID_005），只能按酶类别（醇脱氢酶/醛脱氢酶）与所写反应类型相符作部分支持；S3 EC 4.4.1.24 经官方条目核实酶名与反应（sulfolactate→pyruvate+hydrogensulfite）正确，条目级可核对，但官方系统名为 (2R)-3-sulfolactate hydrogensulfite-lyase 且注明 R-构型专一，与答案 (S)-底物不符。三步中一步获条目级核实并含一处底物构型错配、两步缺具体核验，属“有合理候选和部分支持，但若干关键步骤仍缺具体核验”的 5–6 档，取 6。无 D3a 关键错误：未出现 EC 大类与反应类型不匹配，也未出现酶名与 EC 互相矛盾。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_086：冻结酶gold列出三个必答步的参考酶名与EC：S01 (R)-sulfopropanediol 2-dehydrogenase、S02 sulfopropanediol 3-dehydrogenase EC 1.1.1.308、S03 (S)-sulfopropanediol 2-dehydrogenase；支持目标反应酶对应核对，不证明答案酶已正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：冻结反应gold提供S01/S02/S03的底物、产物、方向与主链角色；支持S03作为必答目标而答案未绑定交付的判定边界。
- E0_EVIDENCE / f3e0:tp:EV146-11：官方EC 4.4.1.24 为R构型专一的sulfolactate sulfo-lyase；支持答案S3所用EC与其(S)-3-sulfolactate底物不一致，但不支持把S01/S02的未核直接判错。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分7 → V0.5新分5，变化-2。

新裁判理由：

> Roseovarius nubinhibens在gold中以物种级PATHWAY_COMPLETE出现（taxid 314263），但答案声称菌株ISM并把同一菌株绑定到每一步；gold必答步的STEP行却列Cupriavidus pinatubonensis。物种级身份有部分支持，菌株级与步级能力归属未充分核验，落在5-6档，取5。

<details><summary>V0.4理由与本行变化背景</summary>

物种 Roseovarius nubinhibens 在冻结 organism_gold 中为该 pathway 的 PATHWAY_COMPLETE 生物（TaxID 314263，species 级），故选菌方向有物种级真实记录支持；但答案交付的是菌株级身份“ISM”且 ncbi_taxid 留 null，冻结记录无该菌株级条目（F5/F15 在 gold 为 UNKNOWN），属身份阶梯①“粒度不足”——记录真实、同 lineage、档内扣分、不cap。三步酶-菌归属（HpsN/HpsO/SuyAB 均在 R. nubinhibens ISM）仅有 EVID_001（未核实）与 EVID_004（内部知识）支撑，且答案自述首步 HpsN 的直接证据来自 Cupriavidus pinatubonensis JMP134（另一物种），反应级与完整路径能力证据未随交付（v0.3 三层分别核验）。综合取 7（档内偏低）。未判关键错误：非跨属/无关类群错配，主要微生物推荐未被推翻。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_086：支持Roseovarius nubinhibens物种级PATHWAY_COMPLETE及taxid 314263；同时必答STEP行匹配菌为Cupriavidus pinatubonensis。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 15项性状齐全：12项填写、3项明确未知、0项遗漏。中温偏好、革兰氏阴性、杆状、不产芽孢等与物种级gold相符；但DSMZ DSM 15170、盐度类别、栖息地、HpsN活性等主要依赖INTERNAL_KNOWLEDGE_ONLY，且 motility与基因组信息在gold有记录而答案留null。属部分性状可核、关键项证据不足的5-6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

按同物种代表记录口径比对 314263 的物种级观测：杆状（cell shape=rod-shaped）、革兰氏阴性（gram positive=false）、中温偏好（temperature preference=mesophilic）、不产芽孢（sporulation=false）、好氧/耐氧（aerotolerant=true）均与答案一致；F3/F10/F14 诚实置 null（gold 对 F10、F14 有观测，属完成度缺口而非错误）；F4 定性“海洋/需盐”与 gold 该子字段仅 PREDICTED、scoreable=FALSE 不冲突。未核实项：F5“DSMZ DSM 15170”、F7“DHPS 可作唯一碳源”、F9“HpsN 活性”、F15“海洋浮游”均无冻结记录（gold F5/F15=UNKNOWN）→UNRESOLVED。未出现“预测冒充观测”、数值离谱或物种级观测被写成全菌株耐受极限。属 7–8 档“主要性状可核实且适用，仅少量条件或数值问题”，因关键数值/来源项证据不足取 7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_086：支持Roseovarius nubinhibens物种级mesophilic、rod-shaped、Gram-negative、sporulation=false等；不支持DSM 15170与ISM菌株级全部性状。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_086：标明各性状是否有可评分观测值及completeness_only范围；不等同于答案来源已支持。

</details>

### D5 来源与可核查性：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 核心路线仅给MetaCyc条目名而无record_id/URL；EC 1.1.1.337、1.2.1.86及全部性状主要为INTERNAL_KNOWLEDGE_ONLY；两篇PubMed文献仅有作者/期刊/页码且E0未解析。决策相关组多为GENERIC/MISSING来源，关键结论不能完整核对，但无已核实虚构或错引，故不cap；按3-4档取4。

<details><summary>V0.4理由与本行变化背景</summary>

按 claim group 登记：决策相关组中，路线核心（CG01/CG02/CG03）仅以途径名“MetaCyc Pathway: 3-sulfopropanediol degradation I”定位（record_id=null，E0 未解码该自由文本 GAP-086-014）；EC 1.1.1.337 与 1.2.1.86 仅有 INTERNAL_KNOWLEDGE_ONLY（EVID_005）＝MISSING_SOURCE；EC 4.4.1.24 存在条目级可定位且事实层获支持的结论（EV146-11）；核心菌物种名有 gold species 级 PATHWAY_COMPLETE 记录（314263）；12 项性状来源为 EVID_004 内部知识。即“部分关键结论可定位并核对，其他模块仍缺映射或必要生成记录”，且远未达到“决策相关组全部笼统”或“全部缺失”，故不落入 3–4 档，取 5。无已核实错引：EVID_001 标 DATABASE_DIRECT 而实为记忆性归属，属来源质量缺陷（D6 亦计），未构成引用不存在或不支持声称的已核实结论；E0 查不到者一律 UNRESOLVED，不判虚构、不判 CONTRADICTED、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：仅核实EC 4.4.1.24一条官方事实；不支持路线、EC 1.1.1.337/1.2.1.86、菌株或性状来源链。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> 答案较明确地区分DATABASE_DIRECT、LITERATURE_DIRECT与INTERNAL_KNOWLEDGE_ONLY，逐项给出low/medium/unknown，并用uncertainties集中披露EC、宿主记忆值与未核性状；null使用也多数诚实。扣分点是部分路线/宿主仍以medium置信陈述而缺冻结支持，个别性状来源强度偏乐观。属7-8档，取7。

<details><summary>V0.4理由与本行变化背景</summary>

披露质量总体好：uncertainties 逐条列出三个 EC 未与 BRENDA/ExplorEnz 核实、路线宿主按 MetaCyc“凭记忆”、DSMZ/TaxID/基因组未逐项核实、辅因子未全列、中间体立体化学按题面 (S) 书写；字段级 confidence 多为 low/medium，INTERNAL_KNOWLEDGE_ONLY 单列（EVID_004/EVID_005），alternative_branches 以 is_part_of_scored_main_route=false 明确排除非主链。扣分：route_summary/EVID_001 以“DATABASE_DIRECT+medium”包装记忆性途径归属并陈述为事实（仅在后文“凭记忆”一句部分抵销）；F7“可作唯一碳源”、F9“HpsN 活性”以 medium/low 陈述而无独立支持，属单点过度确信；未披露 S3 底物 (S)-构型与 EC 4.4.1.24 R-专一性的冲突。尚未达到“系统性把预测写成实证/掩盖已知矛盾”的程度，属 7–8 档取低，7。

背景标签：。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Qwen

答案SHA256：`53081a862d7787a178dbacede59bf736a8723fe81227af78553ad23af61a7cbb`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> JSON结构与输出模块基本完整，但未按题面指定三主链作答：答案给出S1-S5替代路线至pyruvate+sulfite，而gold指定S03-&gt;S01-&gt;S02至(R)-3-sulfolactate；15项性状全部null，完整性/任务符合度明显受损，按D1 3-4档下沿给3。

<details><summary>V0.4理由与本行变化背景</summary>

步骤模块交付较完整（S1–S5 均给底物/产物英文名与SMILES，并绑定酶名与菌名），但两个必要模块实质未交付：五步 enzyme.ec_number 全部为 null、organism_profiles&#91;0&#93;.traits 的15项性状全部为 null；13/15项无TaxID/保藏号/基因组号。更关键的是交付的五步化学链与题面指定路线 3-sulfopropanediol degradation I 的curated主链不同（gold首步为C2氧化生成1-hydroxy-2-oxo-3-sulfopropane，再经(R)-2,3-DHPS至终点(R)-3-sulfolactate），答案却在 route_scope/route_summary 中自称在指定路线下——按P100及八.D1，这属于任务参数偏离中的自称合规却交付不同化学路线，将触发本维关键错误，最高给4分；再叠加EC缺失与性状全空，档内取3分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：Gold主链为S03-&gt;S01-&gt;S02，终点(R)-3-sulfolactate；不支持答案S1-S5至pyruvate+sulfite的替代路线。
- ANSWER_TEXT / ANSWER.steps：答案实际交付5步替代路线及全部null性状。

</details>

### D2 反应化学科学性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 按D2独立评替代路线化学：S1-S5转化方向连续、主结构变化大体可成立，但非题面指定主链；多步氧化/转氨辅因子未列，S5缺NH3副产物/计量说明，证据仅内部低置信。按5-6档下沿给5。

<details><summary>V0.4理由与本行变化背景</summary>

逐步看，五步反应类型均成立且方向一致：伯醇→醛（S1）、醛→羧酸（S2）、2-羟基酸→2-酮酸（S3）、酮酸转氨（S4）、磺基裂解为pyruvate+sulfite（S5）；未见反应方向反转、原子明显不守恒或无依据跳步（辅因子NAD(P)+/H2O未列属局部计量缺陷，按八.辅因子条款为7–8档级问题）。但关键中间体（3-sulfolactaldehyde、(S)-3-sulfolactate）与题面指定路线的curated主链不符，全链无任何来源，合理性证据为零——符合&#x27;主干部分成立，但关键中间体、转化或连接仍需修订；合理性证据有限&#x27;（5–6档），取5。起始步的化学类型本身并非错误转化，故不另判D2关键错误（任务路线偏离已在D1独立判定，四.1不连坐、不双计）。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：答案逐步底物/产物、酶名与反应类型；仅据其化学表达评D2。

</details>

### D3a 目标反应与酶对应：2 / SCORED

V0.4旧分5 → V0.5新分2，变化-3。

新裁判理由：

> D3a目标步S=0、F=1（S03 KEY确认失败）、U=2（S01/S02对齐未确认）。答案S1以(S)-2,3-dihydroxypropane-1-sulfonate dehydrogenase将底物氧化为3-sulfolactaldehyde，与gold S03产物1-Hydroxy-2-oxo-3-sulfopropane及(S)-sulfopropanediol 2-dehydrogenase不符；其他目标酶未绑定。按KEY失败受限&#91;1,4&#93;内，因几乎无目标步可用支持，给2。

<details><summary>V0.4理由与本行变化背景</summary>

五个酶名与所写反应类型自洽（两个醇/醛脱氢酶、一个2-羟基酸脱氢酶、一个转氨酶、一个裂解酶），未见&#x27;酶名与EC互相矛盾&#x27;或&#x27;EC大类与反应类型不匹配&#x27;这类可判的关键错误；但EC全部为null、无任何条目级来源，关键步骤的酶-反应对应无法核验；E0两条EC记录（2.3.3.15、4.4.1.24）与答案所写酶名不对应（related_claims为空，EV007-23所述SulX/2.3.1.-并非本答案声称）——属&#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;（5–6档），取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：Gold S03底物(S)-2,3-dihydroxypropane-1-sulfonate生成1-Hydroxy-2-oxo-3-sulfopropane；S02终点(R)-3-sulfolactate。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_086：Gold S03接受酶为(S)-sulfopropanediol 2-dehydrogenase EC 1.1.1；S01/S02另有指定酶。

</details>

### D3b 微生物身份与能力：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 答案将Cupriavidus necator JMP134同时用于全部步骤并设complete_pathway_organism_profile_id=ORG_001，声称整路径能力；但无TaxID、基因组/实验/文献支持，且gold step organisms为Cupriavidus pinatubonensis等，未列C. necator JMP134。身份为真实种/株但能力/全路径声称未核，按3-4档给4。

<details><summary>V0.4理由与本行变化背景</summary>

答案把全部五步以及 complete_pathway_organism_profile_id=ORG_001 都归给同一菌 Cupriavidus necator JMP134（ncbi_taxid=null，confidence=low，证据仅 EVID_001 INTERNAL_KNOWLEDGE_ONLY）。gold 的三步curated菌为 Cupriavidus pinatubonensis（taxid 248026，genome GCA_019602855.1），pathway_complete 名单为 248026/314263/89184，均不含 C. necator；答案把一个没有任何单步支持记录的菌写成整条路径完成菌，且物种与步骤菌不匹配——符合3–4档&#x27;多处物种/菌株不匹配，将单步支持写成整条路径能力&#x27;，取4（考虑到物种名真实、答案自标 low 置信，未再下压）。冻结证据不能证明 C. necator 不能执行该路线，故不判为本维已核实关键错误（key_error=UNRESOLVED）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_086：Gold step organisms为Cupriavidus pinatubonensis TaxID 248026；PATHWAY_COMPLETE另列314263、89184；未列C. necator JMP134。
- ANSWER_TEXT / ANSWER.microorganism：答案自述Cupriavidus necator JMP134并标为全路径菌。

</details>

### D4 性状科学性：1 / MISSING

V0.4旧分1 → V0.5新分1，变化+0。

新裁判理由：

> 15项性状全部以value=null、confidence=unknown交付，无任何可评价性状值；按P44全部必需性状null时D4=MISSING=1，不宣称已检出科学错误。

<details><summary>V0.4理由与本行变化背景</summary>

任务要求每个 organism_profile 一次返回全部15项性状；答案 organism_profiles&#91;0&#93;.traits 的 F1–F15 全部为 value:null、confidence:&#x27;unknown&#x27;（filled=0, explicit_unknown=15, omitted=0），未交付任何可评价的性状数值、单位或条件。按P44（全部必需性状均为null/空值时D4按MISSING记1分，不宣称检测到科学错误）处理；不确定性披露的诚实性在D6单独评价，不在此重复加减。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;MISSING_SCORE_RULE_FIXED_1。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.traits：证明15项性状均未给可评价数值。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案仅登记EVID_001，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id均null，locator仅为路线名；路线、酶、菌等实质结论无可定位外部条目。按MISSING_SOURCE低档，给2；无已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

唯一的证据是 EVID_001（source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id=null，claim_scope 覆盖 route/steps/enzymes/microorganism），即全部关键结论只有自我声明，无任何可定位的条目、DOI、登录号、保藏号或计算记录；EC全为null使编号类核验也无对象。按P34/P41，决策相关组全部为MISSING_SOURCE→低分档且默认不cap；关键结论完全不可追查（1–2档），取2（答案至少结构化登记了证据条目与置信标签，未伪称外部来源）。E0两条官方条目与本答案无claim关联，不构成已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：仅内部知识自述，无数据库/文献记录定位。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案对EC未确认、辅因子/计量未确认、微生物仅低置信内部知识、性状未知等披露较具体；低置信与unknown标签基本与证据强度相称。仅有complete_pathway_organism_profile_id等少量主张未单独加注，按7-8档取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案对证据性质与边界的表述总体诚实、具体：五步 enzyme/microorganism 的 confidence 均为 low，15项性状标为 unknown，uncertainties 明确列出&#x27;氧条件未指定&#x27;&#x27;各步EC未确认&#x27;&#x27;微生物与性状仅低置信度内部知识、未给出保藏/基因组/文献来源&#x27;，没有把预测写成实证观测，也未掩盖已知矛盾。扣分点：route_summary 把&#x27;在指定路线下&#x27;的链作为既成事实陈述，未标注这是推断、也未提示其与该路线curated主链可能存在的差异；这属于披露强度局部不足、并非系统性误导。按7–8档（大部分证据性质与限制已标注）取7，不触发D6关键错误。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：证明不确定性披露存在且较具体。

</details>

## Grok

答案SHA256：`8bba28ce32f58230c9363940a42e76fd4a77a75691b6d9195e7e7bc444f2d9ef`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案格式完整，steps、organism_profiles、15项性状及evidence_registry均已交付，主要模块均被涉及；但题面指定路线要求冻结主链S03→S01→S02并以(R)-3-sulfolactate为终点，答案改交(S)-DHPS→(S)-3-sulfolactaldehyde→(S)-3-sulfolactate→pyruvate的替代链，仍声称是题面指定路线。该任务路线偏离属D1关键错误，cap≤4；因交付模块和格式基本完整，取4而非更低。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：支持题面路线起点为(S)-2,3-dihydroxypropane-1-sulfonate、终点为(R)-3-sulfolactate。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：支持必答主链步骤S03→S01→S02及其主底物/主产物方向；不支持答案的(S)-sulfolactaldehyde/(S)-sulfolactate/pyruvate替代链作为本题指定主链完成。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_086：支持本题为3步LINEAR_UNIQUE、ordered_step_count=3的冻结任务。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案的三步化学总体可辨认，氧化/醛氧化/磺酸裂解与辅因子书写基本连贯，原子与电荷大体可成立；但S3把上游(S)-3-sulfolactate直接交给SuyAB/3-sulfolactate sulfo-lyase，而冻结E0证据显示对应官方EC 4.4.1.24为(2R)-sulfolactate sulfo-lyase且对R-构型专一，答案也自认可能需要未列入的磺基乳酸消旋酶。该显式立体/连续性冲突使关键转化仍需实质修订，不能进入7–8档；按5–6档取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：支持官方EC 4.4.1.24为(2R)-sulfolactate sulfo-lyase，反应为sulfolactate→pyruvate+hydrogensulfite，且官方注明对R-构型专一；用于核对答案S3以(S)-3-sulfolactate直接裂解的立体冲突。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：支持冻结路线中S02产物为(R)-3-sulfolactate；与答案S2产物(S)-3-sulfolactate形成构型差异参照。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_086：支持题面路线终点为(R)-3-sulfolactate；用于说明答案继续到pyruvate的链与冻结终点事实不同，但D2按自身化学质量另评。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按target_fact_contract，N=3：S01、S02为ROUTE_HOLD_REPRESENTATION/UNRESOLVED，S03为KEY_ENTRY且MISSING；S=0，U=2，M=1。C=S/N=0&lt;0.20，C04选择&#91;1,2&#93;带。无任何目标反应获得已确认S支持，且关键入口目标S03缺失，使酶对应主推荐不可用；在&#91;1,2&#93;内没有可定位的已核目标功能改善证据，取1。D-KEY4上界4虽因KEY M适用，但本带已低于4；M不代签key_error=Y。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_086：支持本题必答目标酶为(R)-sulfopropanediol 2-dehydrogenase、sulfopropanediol 3-dehydrogenase、(S)-sulfopropanediol 2-dehydrogenase；不支持答案S1-S3酶名直接完成这些目标。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：支持三个必答目标反应的底物/产物与方向；答案S3未绑定S03目标反应，S01/S02保持待核。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_086：支持本题required step count=3、LINEAR_UNIQUE；用于固定D3a分母N=3。

</details>

### D3b 微生物身份与能力：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer gives step-level organisms Ruegeria pomeroyi DSS-3 and Paracoccus pantotrophus NKNCYSA and explicitly avoids claiming a single complete-path organism. The names are plausible and the scope statement is honest, but there is no E0 or gold record-level identity/capability verification for TaxID 246200 or NKNCYSA, and step assignments differ from the gold step organism Cupriavidus. This falls in the 5-6 band; 6 because whole-path overclaim is avoided and scope limits are stated.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_086：Gold lists Cupriavidus pinatubonensis for step-level S01-S03 and Ruegeria pomeroyi among pathway-complete organisms; it does not verify answer TaxID 246200 or Paracoccus NKNCYSA.

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> Species-level Ruegeria pomeroyi records support some qualitative traits such as rod-shaped, Gram-negative, non-sporulating, mesophilic/aerotolerant, but numeric temperature/pH/salinity are mostly null, F15 is unsupported, F7/F8/F9 are internal claims, and ORG_002 has no gold trait reference. This is the 5-6 band; 5 because key quantitative/application traits lack sufficient applicable evidence.

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_086：Gold trait records for Cupriavidus, Roseovarius and Ruegeria; supports some Ruegeria qualitative traits only, not Paracoccus NKNCYSA or unobserved answer values.
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_086：Marks which traits are observed-scoreable versus completeness-only; does not convert missing values into errors.
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_086：Shows subfield scoreability, including pending temperature endpoint policy; does not support exact numeric values absent from the answer.

</details>

### D5 来源与可核查性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> All six evidence_registry entries are source_type INTERNAL_KNOWLEDGE_ONLY. Some locators give article citations, a genome accession or TaxID, but no record-level entry, DOI-level verification, or claim-linked database record supports the route/enzyme/organism claims. No verified mis-citation is established. This is the 3-4 band; 4 because a few locators are more specific than bare internal self-declaration.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：Official EC 4.4.1.24 entry; relevant to the answer&#x27;s sulfo-lyase family claim, but the answer did not cite this record and the entry is R-specific.
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_086：Gold organism records; does not verify answer&#x27;s internal-knowledge-only citations or TaxID 246200.

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> The answer openly notes null ECs, R/S naming risk, possible missing racemase, route-boundary uncertainty, null oxygen condition, absent raw_text, and no single complete-path organism. Some high confidence labels are placed on internal-knowledge traits and enzyme assignments, but the limitations are generally specific and not systematically misleading. This is the 7-8 band; 7 because several confidence labels exceed the delivered source strength.

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:tp:EV146-11：Official EC 4.4.1.24 entry indicates R-specific sulfo-lyase activity; this supports the answer&#x27;s own caution about step S3 stereochemistry but does not verify its S-substrate claim.

</details>

## GPT5.6

答案SHA256：`7ecff7ef34ded6e6c2fee041cf80fa342dc9a08a5e2ebd4b71e01a605e6f810d`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求：指定路线3-sulfopropanediol degradation I主链逐步给底物/产物名+SMILES、一个首选酶及EC、一个对应菌，另交15项性状与来源。答案只交2步化学式（S1 S-二羟基丙烷磺酸→3-sulfolactaldehyde；S2→glycolaldehyde+亚硫酸盐），且该序列不是题面锁定gold链（S03→S01→S02，终点(R)-3-sulfolactate）；S1 enzyme整体null，两步microorganism全null，organism_profiles与evidence_registry均为空（15项性状0项、来源0条）。属&#x27;大部分必要内容缺失+路线化学替换&#x27;：落1–2档；因两步底物/产物名称与SMILES可辨认、route_scope按题面原样回填，取档内上沿2（低分档，不因文字/术语加分）。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_086：只支持答案实际交付了哪些字段/哪些为空；不证明任何科学内容正确，也不外推模型能力。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：支持题面锁定主链的逐步底物/产物与顺序，用于判断答案所交转化与终点是否与之不同；不扩展到答案化学在其他路线中的合理性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_086：支持各步的策展粒度酶名/EC存在；不证明具体蛋白活性，也不支持答案S2所写酶功能。
- QUESTION_TEXT / QUESTION_BIOPATH150_086：支持本题必答字段集合与路线锁定要求；不评价任何科学正确性。

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按答案自报化学独立评价：S1把(S)-DHPS的C1羟甲基氧化为醛（3-sulfolactaldehyde），与gold入口步C2羟基质子化生成酮（1-hydroxy-2-oxo-3-sulfopropane）位置不同，属另一转化；S2写3-sulfolactaldehyde(C3)→glycolaldehyde(C2)+亚硫酸盐(C0)，按答案自报SMILES计数碳原子3→2，缺一个碳单元且未给任何说明或副产物，违反基本计量约束；S2所标EC 4.4.1.24官方反应为(2R)-sulfolactate→pyruvate+hydrogensulfite（R构型专一），不支持该醛裂解底物/产物。两步之间前体—产物衔接成立、无跳步，故不落1–2档；但两个重要步骤分别存在位置不符与原子不守恒，落3–4档，取档内下沿3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_086：支持对答案自身SMILES的碳计数与步骤衔接核对；不外推到其他步骤或其他化合物。
- E0_EVIDENCE / f3e0:tp:EV146-11：支持EC 4.4.1.24=(2R)-sulfolactate sulfo-lyase、反应sulfolactate→pyruvate+hydrogensulfite且对R构型底物专一；不支持答案所写sulfolactaldehyde裂解为glycolaldehyde+亚硫酸盐，也不外推为其他EC的历史/分类问题。
- RUBRIC_CLAUSE / RUBRIC_TABLE5_R2：支持把无说明的原子不守恒作为D2关键错误候选；不自动等同于其他维度的关键错误。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按必答三步核对：S=0/3。S03（KEY_ENTRY，(S)-DHPS→1-hydroxy-2-oxo-3-sulfopropane，accepted (S)-sulfopropanediol 2-dehydrogenase/EC 1.1.1）为已确认实证交付缺失（M）——答案S1的enzyme整体为null（name与EC均无），omission locator明确；S01、S02为U（对齐未确认，答案未给出对应目标反应的酶/反应）。存在已确认KEY失败→D-KEY4上界4，落受限候选&#91;1,4&#93;；同时无任何目标步获支持、可用部分仅限底物名称/SMILES等局部信息，故不取4（4为最高许可而非默认），取2。局部未核S01/S02以成对ne字段保留，不影响受限区间判定。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_086：支持入口步酶信息缺失与所给酶的定位；不证明该酶在其他反应中无效。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_086：支持各必答步的策展粒度(G4)可接受酶名/EC集合；不证明具体蛋白底物谱或实验活性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_086：支持各目标步的方向与主底物/主产物，用于判定答案是否交付该目标反应。

</details>

### D3b 微生物身份与能力：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 微生物对应模块整体未交付：两步microorganism均整体为null，organism_profiles为空数组，无任何物种/菌株/TaxID、也无单步归属或全路径能力声称可评价。按P44/P69，模块完全缺失记MISSING=1，不宣称检测到科学错误；此状态与NE（争议不可判）不同，1分按权重参与总分。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_086：支持微生物模块整体未交付；不据此推断错误身份或错误能力。

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面要求每个organism_profile一次返回15项性状（F1–F15，含value/raw_text/evidence_id/confidence）。答案organism_profiles为空数组，15项性状0项交付（filled=0, explicit_unknown=0, omitted=15），全部必需性状均为空值，按P44记MISSING=1；不宣称检测到性状数值错误，也不用代表记录回填答案缺失的来源。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_086：支持15项性状零交付；不表示性状值错误。
- QUESTION_TEXT / QUESTION_BIOPATH150_086：支持性状字段集合与&#x27;未知填null&#x27;的交付要求；不提供任何性状真值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案evidence_registry为空数组，steps&#91;*&#93;.reaction_evidence_id/trait_evidence_id全null，enzymes/微生物/性状均无任何文献、数据库条目或计算记录；按六状态语义各claim组登记MISSING_SOURCE（缺失而非误导，默认不cap），落1–2档。答案确实给出可外部定位的具体标识（路线名、EC 4.4.1.24、化合物名与SMILES），但这不是交付来源，只作为档内上沿的最低依据，故取2；不因核验缺口本身另作低分或判虚构。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_086：支持&#x27;完全无交付来源&#x27;；不把可核标识当作已交付引用。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 证据性质与不确定性披露总体诚实：首步酶/EC、全部微生物与15项性状均显式null而非编造，两步uncertainty与uncertainties&#91;&#93;具体列出未核实点，酶confidence标low，未把预测包装成观测（无系统性误导，不cap）。不足：route_summary以确定语气陈述两步化学而无任何证据类型标注；central_metabolism_entry.explanation称&#x27;本题未指定其后续路线&#x27;与题面已锁定路线范围不符；也未说明所答化学与题面路线链/终点(R)-3-sulfolactate的差异。落7–8档，因主要限制与冲突未完整说明取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_BIOPATH150_086：支持披露质量与语气判断；不把诚实null当作科学正确性加分来源。
- QUESTION_TEXT / QUESTION_BIOPATH150_086：支持题面已指定路线范围，用于判断&#x27;未指定后续路线&#x27;表述不当；不评价化学对错。

</details>
