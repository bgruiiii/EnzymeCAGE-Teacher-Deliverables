# BIOPATH150_011：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：m-cresol degradation pathway

污染物：m-Cresol；氧条件：aerobic。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 48 | COMPARABLE | NATIVE_BATCH_A |
| DeepSeek | 42.5 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 64.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 46.5 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 45.5 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 40.5 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`6b58843f450afaa9bb8203dc20eb5bc2e7398bbf668a98d7ab1d2b2c2da62119`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 答案结构完整：给出5步、逐步酶/EC、去重后的1个菌株档案、15项性状槽位和证据登记；但题面指定的是冻结的 m-cresol 降解主链，答案实际交付的是经3-methylcatechol的间位裂解路线，首步转化和后续主链均与目标路线不同。该任务路线偏离触发D1关键错误上限≤4；在受限范围内取4，反映模块覆盖完整但路线符合度明确失败。

<details><summary>V0.4理由与本行变化背景</summary>

输出完整性与任务符合度：5步主链每步均给主底物/主产物（name+SMILES）、一个首选酶（name+EC+基因）与一个对应菌；organism_profiles按物种+菌株仅一条ORG_001并被各步引用（同一菌去重正确）；15项性状全部在列（10项填写、5项明确null）；evidence_registry 7条、uncertainties 5条；route_scope.chosen_route_name逐字回填题面路线名。扣分点：题面路线名&quot;m-cresol degradation pathway&quot;无pathway ID/化学路线唯一限定，答案实际交付3-甲基儿茶酚间位裂解路线（与gold的甲基羟化路线不同），却在notes称&quot;未改选其他路线&quot;，属路线定位与合规表述的张力，已登记review_queue；按7-8档取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：冻结gold显示S01-S05的目标有向反应；S01为m-Cresol到3-Hydroxybenzyl alcohol，不支持答案S1的m-Cresol到3-Methylcatechol。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_011：冻结case给出目标路线名与终点化合物；用于核对答案是否沿目标路线交付，不用于评价错误路线内部化学。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分8 → V0.5新分6，变化-2。

新裁判理由：

> 答案所答的dmp间位裂解链化学上连贯：m-cresol羟化、3-methylcatechol间位开环、水解、水合、醛缩酶裂解依次衔接，给出O2/NADH/H2O等辅因子，未发现明显方向反转、原子跳变或断链。因其为对指定路线的化学可成立替代而非目标路线，D2按替代化学上限带评，取6。

<details><summary>V0.4理由与本行变化背景</summary>

路径科学性与连续性：题面未指定化学终点，按m-cresol主链化学评价。S1酚羟化（m-cresol→3-methylcatechol，O2/NADH参与，NAD+/H2O为副产物）方向与区域化学成立；S2间位开环（3-methylcatechol+O2→2-hydroxy-6-oxohepta-2,4-dienoate，与答案2-hydroxy-6-methyl-6-oxohexa-2,4-dienoate同一物）；S3水解生成2-hydroxypenta-2,4-dienoate+acetate；S4水合；S5醛醇裂解生成pyruvate+acetaldehyde；逐步计量自洽（如C7H8O4+H2O→C5H6O3+C2H4O2）。与gold甲基羟化路线不同，但gold非唯一允许答案，答案已在route_summary/route_scope/alternative_branches声明所用路线与不属主链的分支，属合理替代路线（四.5）正常评分。扣分点：替代路线依据主要为文献列表/内部知识，未经冻结证据核实；H+/电荷仅在部分步标注（局部简化）。取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分7 → V0.5新分1，变化-6。

新裁判理由：

> 目标S01为已确认的KEY入口失败：gold定向反应是m-Cresol到3-Hydroxybenzyl alcohol，对应xylenol methylhydroxylase；答案S1却给m-Cresol到3-Methylcatechol、phenol 2-monooxygenase。S03亦为非匹配；S02/S04/S05目标步没有绑定交付，仅保留为未确认对齐。没有目标步获得S。已确认KEY失败适用D-KEY4上限≤4；在无可用目标催化对应的情况下取1。S02/S04/S05的局部未核保留，不转为已核错误，也不给目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

酶对应科学正确性：5步酶名/EC/基因与反应类型在领域层面一致——phenol 2-monooxygenase 1.14.13.7（羟化）、catechol 2,3-dioxygenase 1.13.11.2（间位开环）、2-hydroxymuconate-semialdehyde hydrolase 3.7.1.9（水解）、2-hydroxypenta-2,4-dienoate hydratase 4.2.1.80（水合）、4-hydroxy-2-oxopentanoate aldolase 4.1.3.39（醛醇裂解），无EC大类与反应类型错配，dmpKLMNOP/dmpB/dmpD/dmpE/dmpG对应合理。扣分点：E0无上述EC条目（GAP-011-003/007/011/013/015），所引BRENDA条目不可核；E0仅ec:3.7.1.5（acylpyruvate hydrolase，另一酶），不能支持3.7.1.9。按&quot;主要步骤有合理对应、少量关键条目待核&quot;取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：显示目标S01-S05的定向反应与主产物；S01为m-Cresol到3-Hydroxybenzyl alcohol，不支持答案S1的m-Cresol到3-Methylcatechol。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_011：目标S01可接受酶为xylenol methylhydroxylase等，不支持答案S1的phenol 2-monooxygenase作为目标入口酶。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案统一使用Pseudomonas sp. CF600并把ORG_001标为complete_pathway_organism_profile_id。CF600作为dmp途径假单胞菌是合理候选，但E0没有CF600身份、TaxID、保藏号或全路径能力记录；来源仅为通用文献/内部知识。没有已核物种/菌株矛盾，也无跨类群错配，故不cap；但关键身份与全路径能力未核，属部分支持、需实质核验，取5。

<details><summary>V0.4理由与本行变化背景</summary>

微生物对应正确性：S1–S5统一归属Pseudomonas sp. CF600（strain CF600，dmp系统，ncbi_taxid null），complete_pathway_organism_profile_id=ORG_001；菌名/菌株真实存在，步级归属与单步反应能力自洽，未把&quot;仅单步支持的菌&quot;写成多路径菌以外的夸大。扣分点：身份粒度仅&quot;sp.+菌株&quot;，无TaxID/保藏号/基因组号；E0仅有P. putida（taxid:303、bacdive:12880 mt-2）记录，不覆盖CF600，不能支持其身份或能力；全路径能力与F7–F9能力声称仅EVID_001文献列表与EVID_007内部知识支撑、未核实。按&quot;合理候选、部分支持、关键身份与作用范围未充分核验&quot;取6；未核实≠编造，不判身份错配、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_011：显示目标路线涉及Pseudomonas alcaligenes/Pseudomonas putida等记录；仅用于比较目标菌记录，不据此证明CF600不能执行答案替代路线。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 15项性状全部出现，其中10项填写、5项明确未知（F2/F3/F4/F5/F14）。已填的F1/F6/F10-F13属假单胞菌常见基础性状，来源为EVID_007内部知识；F7-F9涉及CF600对m-cresol/酚类的利用及dmp酶活，来源为EVID_001通用文献。E0没有CF600性状记录，缺关键菌株级支持；但答案诚实标注未知，且未见与冻结记录直接冲突，故取部分可用、需实质核验的5分。

<details><summary>V0.4理由与本行变化背景</summary>

性状正确性与适用性：15项齐全，10项填写（F1/F6/F7/F8/F9/F10/F11/F12/F13/F15），5项明确null（F2/F3/F4/F5/F14），符合&quot;不确定填null&quot;。定性性状（革兰氏阴性、杆状、可运动、不产芽孢、好氧呼吸O2）与假单胞菌属一般生物学一致；F7/F8/F9的底物/降解/酶活描述与其dmp路线自洽；F15按属级广适性表述并给low。扣分点：上述性状全部标EVID_007（INTERNAL_KNOWLEDGE_ONLY），无CF600菌株级观测；F1/F7/F8/F9为属/种级常识外推到菌株级且未限定粒度；量化性状全null无法核验。按&quot;部分性状准确适用、关键项证据不足、条件解释待修订&quot;取6；未把预测写成观测，不判KE。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_011：trait gold包含P. alcaligenes/P. putida等菌的性状记录，不含答案所称CF600；用于表明CF600菌株级性状未获冻结记录确认。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分4 → V0.5新分5，变化+1。

新裁判理由：

> D5登记显示：EVID_002-EVID_006把各EC声称映射到BRENDA条目并给出record_id，属条目级定位；但核心路线、CF600身份/全路径能力及一般性状主要依赖EVID_001通用文献或EVID_007内部知识。E0没有这些EC/CF600记录，故相关来源保持UNRESOLVED_SOURCE；未发现已核错引，不cap。部分关键结论有定位、其他模块缺条目级映射，取5。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group登记来源状态：决策相关组CG01/CG02/CG03/CG05的路线证据为EVID_001（作者/期刊/年代文献列表，无DOI/图表定位=GENERIC_SOURCE）与EVID_002–006（仅&quot;BRENDA EC x&quot;号自述，E0无条目可核=UNRESOLVED_SOURCE）；CG07/CG08/CG09身份与全路径能力、CG04/CG10氧相关、CG15/CG16一般性状仅有EVID_007 INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）；CG11/CG12/CG13/CG17为null无来源。E0三条记录（bacdive:12880、taxid:303、ec:3.7.1.5）均不涉及CF600或其EC声称，不能核对任何关键结论；EC 3.7.1.9等无冻结记录（GAP-011-003/007/011/013/015/047–052）→UNRESOLVED，不判虚构、不判CONTRADICTED。无已核实错引→不cap；决策相关组既无条目级可核对证据、也非全部MISSING（存在笼统文献/库名），按GENERIC_SOURCE 3–4档取4。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> 答案列出不确定性、未知项和对EC记忆值的medium置信说明，并将5项性状明确置null；也声明了4-methylcatechol替代分支。但它把替代路线和CF600全路径能力以较确定语气呈现，基础性状多标medium却仅有内部知识/通用文献，未明确说明目标路线符合性尚未建立。属部分披露、部分结论强于依据，但非系统性把预测写成实证，取6。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质与边界：uncertainties具体列出羟化区域选择性、同一中间体两种命名、EC 4.2.1.80/4.1.3.39按记忆填写、CF600保藏/基因组/温-pH-盐度缺失、全步用同一菌；各性状confidence区分unknown/low/medium；alternative_branches明确标注is_part_of_scored_main_route=false；EVID_007自我声明为INTERNAL_KNOWLEDGE_ONLY。扣分点：F1/F7/F8/F9等仅内部知识却标medium，属单点强度略超依据；route_scope称&quot;未改选其他路线&quot;而实际化学路线与gold路径不同，表述略过度确信。整体非系统性误导、未掩盖主要矛盾，按7-8档取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## DeepSeek

答案SHA256：`c33045861346a4388890249e4dc1a19b59f16ce2afdf23c4c21df395b7ba7918`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分8 → V0.5新分4，变化-4。

新裁判理由：

> 答案结构完整，路径、逐步酶、微生物、15项性状字段和证据数组均实际呈现；但实际化学主链是m-cresol→3-methylcatechol的6步meta-cleavage路线，而题面要求并锁定的是gold m-cresol degradation pathway主链S01–S05。答案S01产物3-methylcatechol不是gold S01的3-hydroxybenzyl alcohol，S03也未交付gold对应转化，属于指定路线/任务内容偏离。因交付模块完整、字段可辨，D1按任务偏离关键错误cap≤4取4，而非1–2的严重缺模块。

<details><summary>V0.4理由与本行变化背景</summary>

六个步骤均实质给出主底物/主产物英文名与SMILES、一个首选酶及EC、一个对应微生物；route_scope.chosen_route_name逐字回填题面路线名、氧条件aerobic一致；同一菌按物种+菌株去重为单条ORG_001并可被各步引用；15项性状一次交齐（11项有值、4项明确未知、0遗漏）。少量缺陷：F2只有preference无数值、F14基因组全null、来源登记仅为自我声明（后者主要在D5计）。落7–8档，取8。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：支持gold目标主链的方向与步骤产物；不支持答案的meta-cleavage替代路线。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_011：支持题面目标步骤的酶/EC参考身份；不证明答案替代路线上的酶。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分7 → V0.5新分6，变化-1。

新裁判理由：

> D2按答案自身化学质量评价。其6步路线为连续好氧meta-cleavage：m-cresol→3-methylcatechol→2-hydroxy-6-oxohepta-2,4-dienoate→2-hydroxypenta-2,4-dienoate+acetate→4-hydroxy-2-oxopentanoate→pyruvate+acetaldehyde→acetyl-CoA；方向、主要碳骨架转化和步骤连接基本合理。未见主链第一步即错、方向反转、明显原子不守恒或无依据跳跃。辅因子未逐项列出属于局部计量/表达不足，按D2允许区间&#91;1,6&#93;取6；该分只表示替代路线的化学连续性，不回填D3a目标完成。

<details><summary>V0.4理由与本行变化背景</summary>

主链化学自洽：S1 芳香环羟化 m-Cresol(C7H8O)→3-甲基邻苯二酚(C7H8O2)，SMILES与命名一致；S2 间位开环 3-甲基邻苯二酚+O2→2-羟基-6-氧代庚-2,4-二烯酸(C7H8O4)，碳数守恒；S3 水解 +H2O→2-羟基戊-2,4-二烯酸(C5H6O3)+乙酸(C2H4O2)，C7闭合；S4 水合→4-羟基-2-氧代戊酸(C5H8O4)；S5 醛缩裂解→丙酮酸(C3)+乙醛(C2)，C5闭合；S6 氧化→乙酰辅酶A。方向均为底物→产物，无起始步错误、无无依据跳步。扣分项：辅因子（S1的O2/NADH、S2的O2、S6的CoA/NAD+）未标注，属局部计量缺陷（P103，不cap）；且该路线为与gold不同之替代路线，仅以内部知识声明、无交付可核证据，按四.5第3步登记未证实、不据此给高分；题面未指定终点，答案延伸至中心代谢不扣覆盖率。落7–8档，取7。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：支持目标路线身份；不证明答案替代路线已被实验确认。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分6 → V0.5新分1，变化-5。

新裁判理由：

> D3a只计目标反应相应粒度的酶/功能支持。gold S01要求xylenol methylhydroxylase/EC 1.14.13.M67等并把m-cresol转为3-hydroxybenzyl alcohol；答案S1给phenol hydroxylase EC 1.14.13.7并生成3-methylcatechol，产物与目标S01不符。gold S03要求benzyl alcohol dehydrogenase EC 1.1.1.90，答案也未交付该步。S01为预定义KEY入口，已核F触发D-KEY4上限；S02/S04/S05目标对齐仍为U。目标主链无已支持S，核心目标酶对应几乎不可用，故在&#91;1,4&#93;受限范围内取1。

<details><summary>V0.4理由与本行变化背景</summary>

六个酶-EC在名称与EC大类层面与所标反应类型自洽：单加氧酶1.14.13.7↔羟化、双加氧酶1.13.11.2↔间位开环、水解酶3.7.1.14↔C–C水解、水合酶4.2.1.80↔水合、醛缩酶4.1.3.39↔醛缩裂解、醛脱氢酶1.2.1.10↔氧化；并给出dmpB/dmpC/dmpE/dmpG/dmpH等基因标注，未见酶名与EC互相矛盾的已核事实。但六个具体EC在统一冻结证据中均无条目（GAP-011-006/019/010/014/012/008），无法核accepted name/reaction；f3e0:ec:3.7.1.5 为另一EC（acylpyruvate hydrolase），既不支持也不反驳S3的3.7.1.14。关键步骤全缺具体核验、无独立支持，属&#x27;有合理候选和部分支持，但若干关键步骤仍缺具体核验&#x27;（5–6档），取6；无已核实错误，不cap。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_011：支持目标步骤的accepted酶名/EC；不证明答案替代酶。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：支持目标有向反应与产物；不证明答案的3-methylcatechol路线。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案将全部6步归给Pseudomonas sp. CF600（strain CF600，TaxID 303），并声明complete_pathway_organism_profile_id=ORG_001。E0 taxid:303只确认Pseudomonas putida物种级记录，记录名称不含CF600 strain token；organism_gold中确有TaxID 303的PATHWAY_COMPLETE行，支持P. putida 303物种级完整路径能力。故微生物推荐有部分依据，但CF600菌株级身份及其完整路径能力仍属物种级/内部知识支持，不能当作已核菌株级证据。按D3b身份阶梯属粒度不足/部分未核，取5–6档中的6：物种与通路候选合理，关键菌株粒度未确认但未推翻主要候选。

<details><summary>V0.4理由与本行变化背景</summary>

推荐 Pseudomonas sp. CF600（strain=CF600, ncbi_taxid=303）并在六步全部归属该菌、complete_pathway_organism_profile_id=ORG_001。官方TaxID 303记录为 Pseudomonas putida、rank=物种级、CURRENT；答案以物种级ID支持&#x27;CF600&#x27;菌株级身份，而CF600不在任何记录名变体中（item注记F3R1CLM-004336/004426 UNRESOLVED）——属D3b身份阶梯①粒度不足：档内扣、默认不cap；物种层面与gold所列Pseudomonas putida(303, PATHWAY_COMPLETE=TRUE)对齐，主要微生物推荐未被推翻。&#x27;单菌完成六步全路径&#x27;（能力L3）与步级归属（L2）无冻结事实支持（F3R1CLM-000247/004042 UNRESOLVED），按三层分离原则登记待核，不据此判错。落5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅确认Pseudomonas putida物种级分类；不确认CF600菌株身份或该菌株完整路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_011：支持P. putida 303作为gold路径完整菌的物种级记录；不扩展到CF600菌株全路径能力。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 部分性状与TaxID 303的trait_gold一致：F2 preference=mesophilic、F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating均可核；F1 aerobic和F6 oxygen respiration大体不违背好氧背景。但F7把phenol、m-cresol、o-/p-cresol和3,4-dimethylphenol列为碳源/能源，F9声称catechol 2,3-dioxygenase activity，F8声称经meta-cleavage降解m-cresol，均未在冻结303性状记录中显示，且仅由INTERNAL_KNOWLEDGE_ONLY支持。多数数值性状为null，F5未填保藏号。按D4部分准确、关键项证据不足取5–6档中的5。

<details><summary>V0.4理由与本行变化背景</summary>

15项一次交齐：11项有值、4项（F3/F4/F5/F14）明确null+unknown，未编造数值，符合诚实未知纪律。已给内容中，F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-sporulating、F2 preference=mesophilic 与 trait_gold 中 Pseudomonas putida(303) 的种级OBSERVED记录一致；按四.4同物种代表记录条款，不得仅因答案用CF600而记录来自代表株就判错（培养温度记录亦不等于最适值）。但关键项缺可核依据：F7（利用phenol与m-/p-/o-cresol、3,4-二甲基苯酚）在冻结面板中无cresol条目、且面板差异不可跨株迁移；F8/F9（经间位裂解降解m-cresol、catechol 2,3-dioxygenase活性）无记录；F1/F6/F15亦无直接记录；温度/pH/盐度/基因组关键数值缺失。无已核数值离谱或预测冒充观测的证据→不cap。落5–6档，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_011：支持部分可核性状；不支持答案中未列出的cresol碳源谱或catechol 2,3-dioxygenase活性。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_011：支持哪些性状可作为观测准确性/完整性处理；不把未核值自动判错。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> D5只看实际交付的来源。答案仅登记EVID_001和EVID_002，source_type均为INTERNAL_KNOWLEDGE_ONLY，database、record_id、locator均null；没有DOI、数据库条目、方法版本或可定位原文。路线、酶-EC、微生物身份、性状等决策相关组实际均为MISSING_SOURCE。虽然这不自动构成cap，但使D5主要结论几乎不可追查，落入1–2档；因仍有内部evidence_id与claim_scope映射，取2而非1。

<details><summary>V0.4理由与本行变化背景</summary>

答案的evidence_registry仅两条，source_type均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null，仅以claim_scope自述覆盖&#x27;organism identity、oxygen tolerance、…、m-cresol degradation pathway、enzyme assignments&#x27;——按四.3/P34属MISSING_SOURCE（缺失而非误导），决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09/CG04/CG10/CG17）全部缺失来源→低分档；按P41&#x27;全部缺失→低分档（默认不cap）&#x27;与P34默认不触发关键错误，故key_error=N、不设cap，取1–2档中的2（答案至少给出了claim_scope与置信度分级结构，非纯空白）。未发现任何已核实错引，severity=NOT_APPLICABLE_NO_VERIFIED_MIS_CITATION。评分者未用gold或E0回填为答案原交付证据（P51）。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：4 / SCORED

V0.4旧分5 → V0.5新分4，变化-1。

新裁判理由：

> 答案把主要证据来源标为INTERNAL_KNOWLEDGE_ONLY，并给未知数值性状null/unknown，这些是正面之处；但F1、F6、F7、F8、F9、F10、F11、F12、F13等多条性状以high/medium confidence呈现，raw_text均为null，uncertainties为空数组，没有说明主要限制、替代路线、菌株粒度或来源不确定性。属于多处过度确信与主要限制未说明，但尚未到系统性把预测冒充实证观测的cap；D6取3–4档中的4。

<details><summary>V0.4理由与本行变化背景</summary>

正面：以source_type=INTERNAL_KNOWLEDGE_ONLY如实标注自身证据性质（未冒用DATABASE_DIRECT），对未知性状填null并用confidence=unknown，未编造数值。负面：step.uncertainty全null、uncertainties为空数组，全篇无任何限制、冲突或待验证说明；且对未核实的菌株身份、全路径能力与多数EC均给high/medium（microorganism.confidence=high×6，enzyme多为medium/high），结论强度明显超过依据。属&#x27;有不确定性说明但过于笼统、部分结论强度仍超过依据&#x27;（5–6档）；未达系统性把预测写成实证、或无明知掩盖已知矛盾的情形→不cap。档内问题较多，取5。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Kimi

答案SHA256：`a357954c6122c7a01b95f054f09226c9a8bdd7bee5e4b38507cb93a6b158c687`。

### D1 完整性与任务符合度：9 / SCORED

V0.4旧分8 → V0.5新分9，变化+1。

新裁判理由：

> 按认可主链P011_2（S01→S03→S04→S05）评价。答案给出7步，每步均有主底物、主产物、SMILES、酶及微生物字段；route_scope原样填写题面路线且好氧条件一致；15项性状字段全部出现，未知项用null而非编造；同一菌以ORG_001去重。额外下游步骤不作为必答主链缺步扣分。少量字段（如S1 EC null、个别来源弱）属允许的未知/来源问题，未构成重要必答模块缺失。

<details><summary>V0.4理由与本行变化背景</summary>

7-8档：七个主链步骤均给出底物/产物英文名+SMILES、酶、菌，route_scope.chosen_route_name照抄题面，单一菌株去重为ORG_001，15项性状全部出现(4项按规则填null=明确未知而非遗漏)，evidence_registry与uncertainties齐备。仅少量诚实未知(S1酶EC=null、温度/pH/盐度/基因组的null)与弱关联，属少量遗漏/工程外的完成度缺口，未达9-10(未见全部适用要求被实质回应、定量性状未交付)。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.route_scope：答案原样填写chosen_route_name=m-cresol degradation pathway与aerobic
- ANSWER_TEXT / ANSWER.steps：steps S1-S7均含底物/产物/SMILES/酶/微生物字段
- ANSWER_TEXT / ANSWER.organism_profiles：单一ORG_001 profile且15项traits字段齐备

</details>

### D2 反应化学科学性：8 / SCORED

V0.4旧分8 → V0.5新分8，变化+0。

新裁判理由：

> 主链化学与P011_2一致：间甲酚→3-羟基苄醇→3-羟基苯甲醛→3-羟基苯甲酸→龙胆酸；答案随后延伸至龙胆酸开环、马来酰丙酮酸异构及水解为延胡索酸/丙酮酸，化学方向、连续性和主要转化均合理。主要局部问题是未列辅因子/完整计量，按P103属7–8档局部计量缺陷，不自动cap；额外下游不因gold范围外而扣分。无方向反转、主链首步错误或严重不守恒，D2取上限8。

<details><summary>V0.4理由与本行变化背景</summary>

7-8档：主链化学成立且方向连续——m-cresol甲基羟化→3-羟基苄醇→3-羟基苯甲醛→3-羟基苯甲酸，随后走gold的龙胆酸分支(3-羟基苯甲酸6-羟化→龙胆酸)，再经龙胆酸1,2-开环→马来酰丙酮酸→异构延胡索酰丙酮酸→水解延胡索酸+丙酮酸，与标准龙胆酸途径一致；起始步正确、无跳步、方向正确。扣分点：全程未标辅因子/氧与NAD(P)H(H2O等简化式)，属局部计量缺陷(7-8档)，故不给9-10。额外下游延续不计分不扣分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：S01/S03/S04/S05的底物—产物方向与P011_2主链化学步骤
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_011：本题路线名、污染物与好氧条件定位
- ANSWER_TEXT / ANSWER.steps：答案实际给出的后续开环与水解步骤；仅用于评价化学连续性，不把gold外下游作为必答

</details>

### D3a 目标反应与酶对应：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 按P011_2四个目标步评估酶对应。S03的EC 1.1.1.90与accepted集合一致，可保留功能级支持；S01无EC且酶名未入accepted；S04所用EC 1.2.1.28不在S04 accepted集合（accepted为1.2.1.7）；S05答案EC 1.14.13.23与S05 accepted的1.14.13.24不符，且该步表示边界仍挂起。因而仅少数目标可用，其余为待核/非匹配，落&#91;3,4&#93;低带；边界尚不足以支持4档上沿，取3。

<details><summary>V0.4理由与本行变化背景</summary>

5-6档：多数步骤酶名与反应功能相符(S1 甲基羟化酶、S2 aryl-alcohol dehydrogenase 1.1.1.90 与gold同号、S5 龙胆酸1,2-双加氧酶1.13.11.4、S6 马来酰丙酮酸异构酶5.2.1.4、S7 acylpyruvate hydrolase 3.7.1.5反应吻合)；但S4以&#x27;3-hydroxybenzoate 6-monooxygenase&#x27;(6-羟化酶，应为1.14.13.24)配EC 1.14.13.23(4-羟化酶)存在酶名-EC疑似矛盾于分支关键步；S3 EC 1.2.1.28与gold 1.2.1.7同类不同号。E0对1.14.13.23/1.13.11.4/1.1.1.90/1.2.1.28/5.2.1.4均无官方条目(GAP)，无法核实→UNRESOLVED，不cap；按&#x27;若干关键步骤仍缺具体核验&#x27;落5-6档。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;SCORING_FLOW_OR_SCOPE_WIRING_REPAIR;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_011：S01/S03/S04/S05的accepted酶名与EC集合；S02的1.14.13.23与S05的1.14.13.24可支持EC错配判断
- ANSWER_TEXT / ANSWER.steps：答案实际给出的S1-S4酶名/EC
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_011：本题为BRANCHED_DAG；P011_2为可完成主链，未选分支不按漏答计

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 物种P. putida与TaxID 303可由E0分类记录支持，gold亦有P. putida 303的PATHWAY_COMPLETE物种级记录；但答案把全部步骤与完整路径能力都归到菌株NCIMB 9866，E0无该菌株记录，gold中P. putida 303的F5为CCUG 49576，另见NCIB 9869但不是NCIMB 9866。属物种级支持下的菌株级身份/全路径能力待核，未坐实为错误菌株，故按5–6档部分支持取6，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

5-6档：菌名Pseudomonas putida 与TaxID 303物种级匹配，P. putida 在gold PATHWAY_COMPLETE(303)=TRUE，物种层面m-cresol降解能力有基线支持；但答案以单一菌株NCIMB 9866承担全部7步并作complete_pathway_organism_profile_id，菌株级身份与全路径能力在冻结证据中无记录(E0仅有species 303与mt-2 PaW1/12880，均非NCIMB 9866)，属物种级知识支撑菌株级声称(身份阶梯①粒度不足)+单步→全路径外推，档内扣至5-6；未见跨属/无关类群错配，不cap。答案uncertainties亦自承&#x27;全路线代表菌来自路线层面推断&#x27;。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持TaxID 303为 Pseudomonas putida 的物种级分类名；不支持菌株NCIMB 9866或全步骤归属。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_011：显示P. putida 303有PATHWAY_COMPLETE物种级记录，及P. putida NCIB 9869的S01记录；不支持NCIMB 9866为各步或全路径菌。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> Gram阴性、杆状、运动、不产孢等常见性状与P. putida物种级gold相符；但关键项如F5 NCIMB 9866、F7间甲酚碳源利用、F8/F9路径相关降解/酶活，主要依赖INTERNAL_KNOWLEDGE_ONLY的EVID_009或笼统EVID_001，未在NCIMB 9866菌株级核实。温度/pH/盐度/基因组填null属诚实未知，不按错误重扣。整体为部分性状准确但关键项证据不足，取5。

<details><summary>V0.4理由与本行变化背景</summary>

5-6档：已填性状(好氧、好氧呼吸/O2、运动性、杆状、革兰氏阴性、不产孢、栖息地、底物/降解/酶活描述)与P. putida 物种级观测大体相符且适用；但均以EVID_009(INTERNAL_KNOWLEDGE_ONLY)支撑、按物种级常识套用到菌株NCIMB 9866，属&#x27;物种数据不自动适用于所有菌株&#x27;的适用性风险；温度/pH/盐度/基因组四项关键定量性状全部null(gold对303有观测范围)，关键项证据不足。诚实null按D4条款不重扣(完成度归D1)，已给内容准确但关键证据不足→5-6档。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_011：提供P. putida 303等物种级性状观测；F5为CCUG 49576，不能回填NCIMB 9866；F7面板需按原测量语义解释。
- E0_EVIDENCE / f3e0:bacdive:12880：BacDive 12880为P. putida mt-2 PaW1/pWWO记录，不是NCIMB 9866；不能支持NCIMB 9866菌株级F5或性状。

</details>

### D5 来源与可核查性：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 答案有结构化evidence_registry：酶EC多给Expasy ENZYME记录号/URL，部分结论可定位；但E0仅含EC 3.7.1.5且其accepted name为acylpyruvate hydrolase，不含答案所称fumarylpyruvate hydrolase，其他EC多为E0 item gap=UNRESOLVED；路径序列与路径级菌归属依赖EVID_001（EAWAG-BBD，无record_id/locator）为GENERIC；多数性状用EVID_009 INTERNAL_KNOWLEDGE_ONLY为MISSING_SOURCE。未发现已核实错引，故不cap；部分关键结论可定位、其他模块缺映射，取5。

<details><summary>V0.4理由与本行变化背景</summary>

5-6档下沿：决策相关组呈混合——CG05酶-EC组给出Expasy逐条record_id+URL(条目级可定位，其中EC3.7.1.5反应可核对吻合)，故非&#x27;全部笼统&#x27;；但核心路径(CG01/02/03)仅EVID_001(EAWAG-BBD，record_id/locator为空=笼统)，步级菌与全路径能力(CG08/09)、菌株身份(CG07)为路线级推断(UNRESOLVED)，12项已填性状全部仅INTERNAL_KNOWLEDGE_ONLY(MISSING_SOURCE)。无经核实错引，不cap；按&#x27;部分关键结论可定位、其他模块仍缺映射&#x27;落5-6档取低端5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:ec:3.7.1.5：官方EC记录仅列acylpyruvate hydrolase/3-acylpyruvate acylhydrolase及通用3-acylpyruvate水解；不确认答案所称fumarylpyruvate hydrolase名称或具体步骤。
- E0_EVIDENCE / f3e0:taxid:303：仅支持Pseudomonas putida物种名；不支持NCIMB 9866菌株身份或全路径来源。
- E0_EVIDENCE / f3e0:bacdive:12880：记录为P. putida mt-2 PaW1/pWWO等，不能作为NCIMB 9866的菌株级来源。

</details>

### D6 不确定性与诚实度：7 / SCORED

V0.4旧分6 → V0.5新分7，变化+1。

新裁判理由：

> 答案明确给出uncertainties，承认S1酶EC缺失、NCIMB 9866全路径归属为路线层推断、温度/pH/盐度/基因组按缺失填null；confidence多用low/medium而非high。部分internal-knowledge性状仍标medium且无raw_text，构成局部过信，但未系统性把预测写成实证，也未掩盖主要矛盾，按7–8档取7。

<details><summary>V0.4理由与本行变化背景</summary>

5-6档：整体披露较诚实——温度/pH/盐度/基因组明确填null、uncertainties列出3条具体限制(S1 EC缺失、NCIMB 9866全路径推断需复核、定量性状未定)，confidence分级为low/medium/unknown，证据类型在registry如实标INTERNAL_KNOWLEDGE_ONLY，未系统性把预测写成观测。扣分点：S4关键分支酶以DATABASE_DIRECT+confidence=high包装、uncertainty=null，而该EC(1.14.13.23)疑似错配且零披露，属单点过度确信(5-6档、非系统性→不cap)；多项性状以medium强度给内部知识值。故取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Qwen

答案SHA256：`b3198db5c8d5540646ab175fd6ab3fc61fd534d2f9e4d4f9c679a9d3b99473a0`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分6 → V0.5新分4，变化-2。

新裁判理由：

> 答案按JSON模板给出了5步路径、每步酶/微生物、15项性状轮廓及不确定性说明，表面模块齐全；但路线诊断明确为DEVIATES，S01为SUBSTITUTED_ENTRY_DIVERGENCE，实际交付的是3-methylcatechol meta-cleavage替代路线，而非题面/gold指定的m-cresol主链。按D1任务参数偏离属关键错误，且完成度并非空白，故在&#91;1,4&#93;内取4。

<details><summary>V0.4理由与本行变化背景</summary>

路线（5步）、酶、微生物、性状、不确定性各主要模块均有实质作答，route_scope.chosen_route_name按要求填写；但S2主产物SMILES为空、S1/S3的EC为空（题面要求每步含ec_number与SMILES），15项性状中F2/F3/F4/F14为未知。属主要模块齐全但若干必要字段/内容遗漏，落5–6档上沿取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：Gold S01为m-Cresol→3-Hydroxybenzyl alcohol，而答案S1产物为3-methylcatechol；该gold行支持路线偏离判断，不外推到其他维。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_011：本题根身份为m-Cresol，gold终点为2,5-Dihydroxybenzoate/3,4-Dihydroxybenzoate；答案终点为pyruvate/acetaldehyde/acetate，仅用于说明任务主链不一致。

</details>

### D2 反应化学科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 答案的meta-cleavage路线在化学上基本连贯：m-cresol→3-methylcatechol→2-hydroxy-6-oxohepta-2,4-dienoate→2-oxopent-4-enoate+acetate→4-hydroxy-2-oxopentanoate→pyruvate+acetaldehyde，方向、主碳流和计量大体成立。但这是对题面指定gold主链的替代路线，且S2产物缺SMILES、S3缺EC，局部表达不足；按D2化学可成立替换上限6给分。

<details><summary>V0.4理由与本行变化背景</summary>

主链采用m-cresol→3-methylcatechol→2-hydroxy-6-oxohepta-2,4-dienoate→2-oxopent-4-enoate+acetate→4-hydroxy-2-oxopentanoate→pyruvate+acetaldehyde的meta裂解路线。逐步碳数、方向与辅因子（O2/NADH/H2O）计量自洽（C7→C5+C2→C5→C3+C2），无起始步错、无原子明显不守恒。但该路线与本题gold参考路线（甲基氧化→3-羟基苯甲酸→原儿茶酸/龙胆酸）不同，属四.5四步判断下的替代路线：已声明、化学成立，但无外部证据（仅内部知识），按“未证实替代路线”评中档，不cap、不因与gold不同判错。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：用于对照gold主链与答案替代路线的差异；D2仍按答案自身化学反应质量评价，不把gold未覆盖的替代路线直接判错。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分6 → V0.5新分1，变化-5。

新裁判理由：

> 本题N=5。S01为已确认NONMATCH且SUBSTITUTED_ENTRY_DIVERGENCE，答案给的是3-methylcatechol而非gold 3-Hydroxybenzyl alcohol；S02、S04、S05在答案中没有对应的目标转化，S03亦未绑定且表示边界未定。没有任何目标反应获得适用S支持；已确认KEY入口失败触发D-KEY4上限4，在&#91;1,4&#93;内因几无可用目标催化对应、核心主推荐不可用而取1。S02–S05的alignment未核不改变已确认失败所在分带。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶功能与反应类型基本对应（单加氧酶羟化、catechol 2,3-dioxygenase开环、hydrolase水解、hydratase水合、aldolase醛缩），无酶名与反应类型互相矛盾。但S1/S3的EC为空，S2/S4/S5的EC（1.13.11.2/4.2.1.80/4.1.3.39）在E0无冻结记录无法核验（UNRESOLVED），属有合理候选但关键步骤缺具体核验，5–6档取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：Gold S01产物为3-Hydroxybenzyl alcohol，S02/S04/S05另有目标反应；该切片不支持答案把3-methylcatechol路径计为目标催化信用。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_011：Gold S01接受酶为xylenol methylhydroxylase/EC 1.14.13类；不支持答案S1的m-cresol hydroxylase作为该目标反应的已核对应。

</details>

### D3b 微生物身份与能力：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案统一推荐Pseudomonas putida NCIB 10011，TaxID 303。冻结TaxID 303记录支持物种名Pseudomonas putida，但不含NCIB 10011这一菌株标记；gold的PATHWAY_COMPLETE行支持P. putida 303等，不是NCIB 10011的菌株级全路径能力。故微生物候选有物种级支持，但菌株身份与整条路径能力仍属粒度不足/未核，按5–6档取6，不因未核自动判错或cap。

<details><summary>V0.4理由与本行变化背景</summary>

全部步骤归属Pseudomonas putida NCIB 10011（taxid 303）。E0 taxid:303支持种级学名Pseudomonas putida，属合理候选；但菌株NCIB 10011无冻结记录（12880为mt-2另一菌株、保藏号不含NCIB 10011），仅物种级支持菌株级声称（粒度不足）；且以单一菌株承担全部5步并置complete_pathway_organism_profile_id=ORG_001，反应级与整条路径能力均无证据（L3 UNRESOLVED）。无跨属/无关类群错配，未推翻主要微生物推荐→不cap，按5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：仅支持TaxID 303的官方名称为Pseudomonas putida及物种级身份；不支持NCIB 10011菌株标记，也不支持整条路径能力。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_011：Gold列出P. putida 303的PATHWAY_COMPLETE记录；未见NCIB 10011的菌株级全路径能力记录。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案按15项外壳填写，其中11项有值、4项为明确null。已给值中F10 motility、F11 rod-shaped、F12 Gram-negative、F13 non-spore-forming与gold P. putida 303物种级性状一致；F1 aerobic、F6 aerobic respiration/oxygen、F7 m-cresol carbon source、F8 aromatic/m-cresol degradation、F9 m-cresol hydroxylase/catechol 2,3-dioxygenase、F15 soil/freshwater等多为常识性或路线推断，未绑定NCIB 10011菌株级证据。性状缺失本身主要归D1；D4按已给内容、关键缺口与适用性给5–6档，取6。

<details><summary>V0.4理由与本行变化背景</summary>

所列定性性状（F1 aerobic、F6 aerobic respiration/O2、F7 m-cresol作碳源、F8降解芳香物、F10 motile、F11 rod-shaped、F12 Gram-negative、F13 non-spore、F15 soil/freshwater）与P. putida种级常识基本一致；但全部仅INTERNAL_KNOWLEDGE_ONLY、无raw_text与记录，F5保藏号NCIB 10011无核实，定量性状（F2温度/F3 pH/F4盐度/F14基因组）均null。属部分性状准确且适用但关键项证据不足，5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_011：Gold P. putida 303物种级记录支持motility、rod-shaped、Gram-negative、sporulation=false等；不支持把全部性状写成NCIB 10011菌株级观测。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_011：该mask显示温度/pH/盐度等子字段的scoreability状态；用于判断缺失与未核边界，不把null当作错误。

</details>

### D5 来源与可核查性：1 / SCORED

V0.4旧分2 → V0.5新分1，变化-1。

新裁判理由：

> 答案的evidence_registry仅有EVID_001与EVID_002，二者均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；路径步骤、酶、微生物、性状均回指这两条内部声明。按D5，INTERNAL_KNOWLEDGE_ONLY归MISSING_SOURCE，决策相关组没有可定位的外部来源；MISSING_SOURCE默认不cap，但可追溯性低档为1–2，本案几无任何可定位依据，取1。

<details><summary>V0.4理由与本行变化背景</summary>

全部结论仅登记EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY自我声明，database/record_id/locator均为null，无可定位外部记录，决策相关组（路线/酶/菌/CG14底物）全部MISSING_SOURCE。E0核验未见CONTRADICTED、无VERIFIED_MIS_CITATION，故不cap；按“全部缺失→低分档”取2。TaxID 303种级学名可SUPPORTED，但不足支撑路线/酶/能力/性状结论。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案整体较诚实地区分证据性质：evidence_registry标为INTERNAL_KNOWLEDGE_ONLY，confidence普遍low/unknown，缺失EC、SMILES和性状用null，uncertainties列明EC未确认、meta-cleavage下游按常见反应推断、菌株性状多为常识性概括。未见系统性把预测写成实证观测，也未见系统性掩盖矛盾；但对complete_pathway_organism_profile_id及部分菌株级性状仍未充分展开限制，故取7–8档上沿8。

<details><summary>V0.4理由与本行变化背景</summary>

答案在每步写uncertainty，并在uncertainties列出3条限制（EC未确认、水解产物与下游推断未逐条给文献、菌株性状为常识性概括未绑定记录）；confidence多标low/unknown，未知项诚实填null。证据性质与限制披露较具体，观测/未知区分基本到位。但complete_pathway_organism_profile_id=ORG_001的整条路径能力未附带不确定性说明，属单点强度略超依据。整体落7–8档下沿取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

## Grok

答案SHA256：`cb48eddcbbd2a3e67cf7d444fbfc20ab2cfdd3356714cefe187f086f72a39a61`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案结构完整，给出了路径、逐步酶/菌、15项性状外壳与不确定性说明；但主链改选为m-cresol直接环羟基化并走meta裂解，未交付gold的S01→S03→S04→S02/S05指定主链及终点。按题面指定路线不可改选，D1任务符合度触发关键偏离，在&#91;1,4&#93;内给3。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：证明gold目标主链为S01→S03→S04→S02/S05及其产物方向；不证明答案替代路线化学不可能。
- ANSWER_TEXT / ANSWER：答案实际交付的替代主链与终点。

</details>

### D2 反应化学科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按答案自身路线评价：m-cresol→3-methylcatechol→meta开环→水解→水合→醛缩裂解→乙酰CoA，方向与主链连续性基本成立，辅因子多有列出；但多处EC/互变/水合细节为回忆性说明，证据有限。按允许&#91;1,6&#93;给6，不因替代路线内部自洽抬高目标完成。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案自身化学主链、方向与连接。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：仅用于说明与目标路线不同；D2按答案自身化学评价。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 对5个gold必答目标：S01、S03为NONMATCH替代反应；S02、S04、S05未交付。S=0，F=2，M=3，U=0，H=0，C=0→&#91;1,2&#93;。错误路线内部酶自洽不获目标信用；核心目标催化对应几乎不可用，给1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：gold必答目标反应与产物；支持S01/S03为替代反应、S02/S04/S05缺失。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_011：gold各目标步accepted酶集合；不支持答案替代酶作为目标完成。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案使用Pseudomonas sp. CF600作为全路径菌；名称/菌株与dmp操纵子路线内部自洽，是合理候选，但E0无CF600 TaxID、菌株级记录或全路径能力证据，gold organism行为P. alcaligenes/P. putida等。按5-6档取5：有合理候选和部分内部一致性，关键身份与全路径能力仍待核。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_011：gold支持P. alcaligenes/P. putida等；不包含CF600菌株级证据。
- E0_EVIDENCE / f3e0:taxid:303：仅支持P. putida物种级分类；不支持Pseudomonas sp. CF600菌株身份或全路径能力。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段齐全，12项明确null；3项定性性状F7/F8/F9对CF600的dmp表型合理，但无菌株级冻结证据、无raw_text，关键定量/培养条件性状缺失。D4按已给内容评：部分性状可合理适用但关键证据不足，给6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_011：gold性状覆盖P. alcaligenes/P. putida等；不能核验CF600的F7-F9具体值。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> EVID_001与EVID_002均为INTERNAL_KNOWLEDGE_ONLY，无record_id、无实际可定位条目；关键路径/酶/菌结论只能追到回忆性书目或IUBMB口述。按MISSING_SOURCE低档处理；未发现可核VERIFIED_MIS_CITATION，故不cap。给2（有具体书目尝试，但无可核对来源）。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：用于判断答案自报来源类型为INTERNAL_KNOWLEDGE_ONLY且无record_id；不回填外部证据。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案清楚标注证据性质为INTERNAL_KNOWLEDGE_ONLY，大量未知填null，并披露EC辅因子差异、3.7.1.9编号不确定性、互变异构、替代龙胆酸路线及SMILES未复核等限制；未把预测系统性写成实证。仅全路径能力声称偏强但已给medium/uncertainty，整体披露具体诚实，给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：答案对未知、证据类型与限制的披露。

</details>

## GPT5.6

答案SHA256：`4b625281072bfa7d8de375790f82a2d77a6dcbfc2233ae42fb72328bf3075554`。

### D1 完整性与任务符合度：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定chosen_route_name=m-cresol degradation pathway；答案已正确回显case/路线名/好氧条件，并给出2步的底物-产物-SMILES、首选酶与EC、对应菌，以及15项性状外壳（4项有值、11项明确null）、来源登记与不确定性说明。但只覆盖一条主链的两步，且第1步产物为3-methylcatechol（gold S01产物为3-hydroxybenzyl alcohol），程序路线诊断为DEVIATES、S01为SUBSTITUTED_ENTRY_DIVERGENCE、S03为SUBSTITUTED_MIDROUTE_FOREIGN，属更换指定路线化学（自称合规却交付不同路线），对照D1/D2边界条款归D1关键错误；性状完成度亦低（11/15明确unknown，非遗漏）。在&#91;1,4&#93;任务偏离受限带内取3：仅覆盖少数必要模块且多处缺步，可用与失效边界勉强可分。

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION#BIOPATH150_011#task_line：只支持题面任务参数：指定路线名、好氧条件、每步需酶/EC/菌与15项性状；不支持任何具体化学或酶的功能正确性。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：支持gold主链入口转化为m-cresol→3-hydroxybenzyl alcohol；不证明其他m-cresol路线不存在，也不用于D3a目标信用。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_011：只证明答案实际交付的转化与字段内容；不证明其化学或酶学正确性。

</details>

### D2 反应化学科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 按D2自身化学质量评价（base range&#91;1,6&#93;）：第1步芳环羟化m-cresol→3-methylcatechol（C7H8O→C7H8O2，SMILES Cc1cccc(O)c1O与3-methylcatechol一致），第2步邻位双加氧裂解3-methylcatechol→2-methyl-cis,cis-muconate（C7H8O4，SMILES与2-甲基粘康酸一致），步骤连接（前步产物即后步底物）连续、方向为降解向、无原子明显不守恒、无一步跳到中心代谢，辅因子层面仅列O2/H2O而未列NADH/NADPH属局部计量简化。但主链止于粘康酸，未到达题面指定终点（2,5-/3,4-dihydroxybenzoate）；合理性依据仅INTERNAL_KNOWLEDGE_ONLY。属“主干部分成立、关键中间体/连接仍需修订、合理性证据有限”，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：支持gold主链的转化序列与终点；不支持把答案路线当作已核正确，也不用于D1缺步分母。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_011：仅支持答案实际给出的结构与步序；不证明其生化被实验证实。

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> D3a仅评目标反应。答案第1步为m-Cresol→3-Methylcatechol，而gold S01为m-Cresol→3-Hydroxybenzyl alcohol；第2步为3-Methylcatechol→2-Methyl-cis,cis-muconate，与gold S02/S03/S04/S05均无对应。目标S02、S04、S05未交付，S01/S03为不同转化而非目标反应。错误路线内部酶自洽不获目标信用。虽EC 1.14.13.7等记录未核，但产物与目标反应不同已足以判目标催化对应几乎不可用，按低档取1。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：给出本题gold主链各步的主底物/主产物与方向；用于核对答案步骤是否为目标反应，不扩展到具体蛋白实验活性。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_011：给出本题gold各必答步的候选酶/EC范围；仅支持该步目标反应可由这些酶/EC催化，不证明答案中非目标路线酶对本任务目标反应有效。

</details>

### D3b 微生物身份与能力：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案对两步均给出同一菌Pseudomonas putida / NCIMB 9866（organism_profile_id=ORG_001，ncbi_taxid=null），未声称全路径能力（complete_pathway_organism_profile_id=null），三层区分基本守住。物种层P. putida是gold S01步骤菌之一且E0有taxid:303物种记录，属合理候选；但菌株层“NCIMB 9866”在gold（P. putida NCIB 9869、P. alcaligenes NCIB 9867）与E0（f3e0:bacdive:12880为P. putida mt-2 PaW1/pWWO，保藏号DSM 3931/ATCC 33015/NCIB 12182/CCUG 2480）中均无对应，属未核的菌株级身份与步级能力声称，且其所归属的反应本身未经对齐。按身份阶梯（物种级支持+菌株级未核，非已坐实异菌株错配）+“合理候选、部分支持、关键身份/作用范围待核”取5，不cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- E0_EVIDENCE / f3e0:taxid:303：只支持物种级学名P. putida的官方身份；不支持任何菌株（NCIMB 9866）身份或反应能力。
- E0_EVIDENCE / f3e0:bacdive:12880：只支持该特定菌株记录的保藏号与培养温度记录；不证明NCIMB 9866存在，也不支持答案的路由能力声称。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_011：支持gold各步微生物与全路径能力归属；不证明答案菌株错误（未命中≠已证伪）。

</details>

### D4 性状科学性：5 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 15项性状字段齐全（4项有值：F5保藏NCIMB/9866、F7“m-Cresol及相关芳香族化合物”、F8“好氧降解甲酚类和儿茶酚类”、F9“芳环羟化与邻位儿茶酚双加氧裂解”；11项value=null为如实未知，按四.4/P112完成度问题归D1，不在D4重复重扣）。有值项均为无来源的定性描述且落在未被证实的菌株上；无任何数值/单位类性状（温度/pH/盐度全null），故不存在已核数值离谱或跨株推广的量纲错误。F5的NCIMB 9866与f3e0:bacdive:12880（mt-2，CCUG 2480/ATCC 33015/NCIB 12182）及gold 303代表记录（CCUG 49576）均不同，但不能据此判错（同物种代表记录口径：不得仅因菌株不同判错）。质量为“部分性状可核实且适用、关键项证据不足”，取5。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_011：支持物种级代表记录的性状原义（培养温度≠最适值；F7裸名称列表≠阳性碳源清单）；不把物种级记录外推到答案的NCIMB 9866菌株，也不回填答案缺失来源。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_011：只支持哪些子字段可作准确性分母；不改变答案已交付内容的正确性判断。
- E0_EVIDENCE / f3e0:bacdive:12880：只支持该菌株记录的保藏号与面板记录差异；不证明答案菌株性状错误。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案为全部结论只登记两条INTERNAL_KNOWLEDGE_ONLY证据（database/record_id/locator均null），无任何可定位文献、数据库条目或计算记录；按D5六状态即决策相关组（CG01/CG02/CG03/CG05/CG07全为MISSING_SOURCE）全部缺失，属低分档1–2；MISSING_SOURCE为缺失而非误导，默认不cap，无经核实的VERIFIED_MIS_CITATION_*。相对1的区分点仅在于答案如实标注了内部知识来源与low confidence（未虚构ID/DOI），故取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_011：只支持答案实际交付的来源字段；不证明任何结论获得外部支持。
- E0_EVIDENCE / f3e0:ec:3.7.1.5：该E0记录与答案任何酶声称无关，仅说明E0中存在与本答案不相干的EC条目；不得用作答案错引或支持证据。

</details>

### D6 不确定性与诚实度：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案对证据性质与未知的处理总体诚实：11/15性状明确null，uncertainties列出初始羟化酶命名/EC归类随菌株与数据库而异、以及未展开后续裂解产物立体化学；confidence多为low/unknown，来源标INTERNAL_KNOWLEDGE_ONLY，未把预测写成实验观测，也未掩盖与题面路线不同的可能。扣分点：第2步以medium confidence标注仅由内部知识支撑的酶-反应对应，F5保藏号在无来源下以low confidence给出，属单点过度确信（P119档内扣、不cap）；同时未明确声明所交付路线与题面指定主链并非同一化学路线这一主要范围差异。综合取7。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_011：只支持答案的披露文本与置信标签，不证明披露内容科学正确。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_011：用于核对答案是否披露与题面主链的范围差异；不用于D2/D3a计分。

</details>
