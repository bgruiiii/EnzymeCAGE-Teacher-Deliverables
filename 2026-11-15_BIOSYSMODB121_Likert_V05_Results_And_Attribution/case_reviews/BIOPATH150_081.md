# BIOPATH150_081：评分与新旧变化

[题目目录](INDEX.md) · [主报告](../TEACHER_REPORT.md) · [量表](../methods/SCORING_RUBRIC_USED.txt)

原路线名称：L-arginine degradation XIV (oxidative Stickland reaction)

污染物：2-Amino-5-guanidinovaleric acid；氧条件：原题未指定。

**以下为AI辅助评分及裁判理由，不等于专家逐条确认或实验验证。**

| 模型 | 当前总分 | 状态 | 选定答案来源 |
| --- | ---: | --- | --- |
| GLM | 39.5 | COMPARABLE | RECOVERED_BATCH_B |
| DeepSeek | 38 | COMPARABLE | NATIVE_BATCH_A |
| Kimi | 37.5 | COMPARABLE | NATIVE_BATCH_A |
| Qwen | 30 | COMPARABLE | NATIVE_BATCH_A |
| Grok | 46 | COMPARABLE | ACCEPTED_CUMULATIVE_COLLECTION |
| GPT5.6 | 31 | COMPARABLE | FIRST_ATTEMPT |

## GLM

答案SHA256：`5bee94b41338537404e44045bffd471f704697b2dc825dfe7d694594c7fec031`。

### D1 完整性与任务符合度：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> 格式与模块覆盖完整，但未按题面锁定的 oxidative Stickland 主链交付：答案给出的是精氨酸转氨酶/γ-胍基丁酸支路，而非冻结主链的 arginine deiminase/citrulline/ornithine 核心。任务路线符合度主要结论失效，D1关键错误封顶≤4；因路径、酶、菌、性状均成体系且关联清楚，档内取4而非更低。

<details><summary>V0.4理由与本行变化背景</summary>

模块覆盖完整：5步主链含底物/产物/SMILES/role，每步酶+EC（S1/S3的EC为null），2个菌profile各15项性状，4条证据登记，专门不确定性列表，格式符合v2且可解析。问题在任务符合度：route_scope.notes与route_summary宣称所交付即题面指定&#x27;L-arginine degradation XIV (oxidative Stickland reaction)&#x27;，实际主链为精氨酸转氨/2-酮精氨酸→4-胍基丁酰-CoA→4-胍基丁酸→GABA+尿素（假单胞菌ATC分支），属&#x27;自称合规却交付不同化学路线&#x27;（P100）。据此构成D1关键错误，cap≤4；因交付完整、格式规范，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_BIOPATH150_081：题面锁定路线名称与主链交付要求；不证明答案化学或酶对应正确。
- ANSWER_TEXT / ANSWER.route_summary+steps：答案实际交付的5步转氨/胍基丁酸路线；不证明其属于指定主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：冻结主链包含 arginine deiminase 与 thiolase 等核心步骤；不穷尽所有替代路线。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 在锁定路线下，答案首步不是 arginine deiminase 生成 L-citrulline，而是转氨生成5-胍基-2-氧戊酸；后续也未接回 citrulline/ornithine/2,4-diaminopentanoate 核心。替代支路内部化学大体连续、氧化脱羧与CoA硫酯化可成立，但指定主链的首步与核心序列错误，D2关键错误封顶≤4；档内取3。

<details><summary>V0.4理由与本行变化背景</summary>

答案主链首步为转氨(Arg+2-OG→5-胍基-2-氧戊酸+Glu)，与指定路线XIV冻结gold首步精氨酸脱亚胺酶(Arg+H2O→citrulline+NH4+)不一致；随后走2-酮精氨酸→4-胍基丁酰-CoA→4-胍基丁酸→GABA+尿素，未走gold的鸟氨酸→D-鸟氨酸→2,4-二氨基戊酸→2-氨基-4-氧戊酸→乙酰-CoA+D-丙氨酸主链。首步、关键中间体与终产物三处不符，属未声明偏离且仅有内部知识支撑，使该维&#x27;主链正确性/连续性&#x27;主要结论失效，触发D2关键错误cap≤4。单步化学自洽（已核S1原子平衡），档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：冻结主链的方向与核心转化顺序；不证明替代路线所有酶均无活性。
- ANSWER_TEXT / ANSWER.steps.S1-S5：答案首步与后续序列；用于比对指定主链的化学连续性。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 原答案给出的是 L-精氨酸转氨→5-胍基-2-氧戊酸→4-胍基丁酰-CoA→4-胍基丁酸→GABA/尿素的路线；与冻结 gold 主链（精氨酸脱亚胺酶→瓜氨酸→鸟氨酸→D-鸟氨酸→2,4-二氨基戊酸→2-氨基-4-氧戊酸→乙酰-CoA+D-丙氨酸）不同。逐目标核对：S01 Ord/EC1.4.1.26、S02 鸟氨酸氨甲酰转移酶/EC2.1.3.3、S03 精氨酸脱亚胺酶/EC3.5.3.6、S04 2-氨基-4-氧戊酸硫解酶/EC2.3.1.263、S05 D-鸟氨酸4,5-氨基变位酶/EC5.4.3.5、S06 鸟氨酸消旋酶/EC5.1.1.10/5.1.1.12 均未出现；终产物也不是 gold 的 D-alanine|acetyl-CoA。没有可用的目标反应催化对应，主推荐失效。

<details><summary>V0.4理由与本行变化背景</summary>

各步酶候选与所写反应类型基本匹配，无酶名-EC矛盾：转氨对应转氨酶；EC 1.2.7.8(2-氧代酸:铁氧还蛋白氧化还原酶)对应氧化脱羧；EC 2.7.2.7(丁酸激酶)对应酰基磷酸底物水平磷酸化但底物特异性为推断；EC 3.5.3.7(胍基丁酸酶)对应胍基水解。S1/S3的EC为null，S2/S3/S4关键底物特异性均为推断、置信low，属&#x27;合理候选部分支持、关键步骤缺具体核验&#x27;，取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：支持 gold 目标反应的底物、产物、方向与顺序；不支持原答案的转氨/胍基丁酸路线。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：支持目标酶名/EC：Ord 1.4.1.26、鸟氨酸氨甲酰转移酶 2.1.3.3、精氨酸脱亚胺酶 3.5.3.6、2-氨基-4-氧戊酸硫解酶 2.3.1.263、D-鸟氨酸4,5-氨基变位酶 5.4.3.5、鸟氨酸消旋酶 5.1.1.10/5.1.1.12；不支持原答案所列酶/EC。
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_081：支持 gold 终点为 D-alanine|acetyl-CoA；不支持原答案的 4-aminobutanoate/urea 终点。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_081：显示 gold 步骤关联 Acetoanaerobium sticklandii 等目标微生物；不支持原答案以 Clostridium sporogenes/Pseudomonas aeruginosa 作为目标步骤对应菌。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分5 → V0.5新分5，变化+0。

新裁判理由：

> 微生物名称与菌株（C. sporogenes ATCC 15579、P. aeruginosa PAO1）本身是可辨认候选，P. aeruginosa PAO1部分性状与基因组信息也较合理；但目标步的菌株级催化能力无冻结证据，C. sporogenes ATCC 15579的TaxID 1508亦未核，且所用菌并非冻结目标行的A. sticklandii。无整条路径能力声称。按5–6档，有合理候选和部分支持但关键身份/作用范围未充分核验，取5。

<details><summary>V0.4理由与本行变化背景</summary>

推荐 Clostridium sporogenes ATCC 15579(TS 1508) 承担S1-S4、Pseudomonas aeruginosa PAO1(TS 208964) 承担S5。C. sporogenes 为已知 Stickland 发酵菌、P. aeruginosa 为胍基丁酸酶来源，作为各步菌属合理候选；分步写菌符合&#x27;不要求整条路径只有一个代表菌&#x27;；答案标注low置信并明说S5在梭菌中未确证。未见&#x27;序列存在性→整条路径能力&#x27;的过度外推。但TS 1508/208964在E0无记录、上述菌株对具体转氨/胍基分支的能力未核实，属&#x27;合理候选、关键身份与作用范围未充分核验&#x27;，取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_081：冻结目标步的菌株/物种对应；不证明其他菌不能做同反应。
- ANSWER_TEXT / ANSWER.organism_profiles：答案声称的菌株身份与步级归属；不证明其催化能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分6 → V0.5新分6，变化+0。

新裁判理由：

> 两个profile均返回15项性状，P. aeruginosa PAO1的基因组登录号、大小、GC、Gram、运动性、产孢等多项与常见事实相符；C. sporogenes profile整体可读，但部分值由内部知识推定（最适37°C、糖利用有限、末端受体H+），且菌株/保藏号与冻结trait行不完全对应。按5–6档，部分性状准确且适用、关键项证据不足，取6。

<details><summary>V0.4理由与本行变化背景</summary>

ORG_001(C. sporogenes)多项性状与gold物种级数据吻合：革兰氏阳性、杆状、运动性+、产芽孢、生长温度37°C、GC≈28%落在gold 26.5–29.7区间；pH/盐度诚实置null。小瑕疵：将温度生长观测37°C写成&#x27;最适约37°C&#x27;，略过度诠释（培养/生长温度≠最适）。ORG_002(P. aeruginosa PAO1)性状（好氧、单极鞭毛、G-、不产芽孢、NC_002516/约6.26Mb/GC66.6%）科学上合理但该TaxID在gold切片无记录(E0 GAP)、无法核验，且该菌仅用于末端一步、与梭菌语境关联弱。综合&#x27;部分性状准确且适用、关键项证据不足&#x27;，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_081：冻结性状观测与预测记录；不把培养温度当最适温度，不证明所有菌株相同。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_081：区分observed_accuracy与completeness_only；不将预测背景当观测。
- ANSWER_TEXT / ANSWER.organism_profiles.traits：答案实际性状值；用于与冻结记录比对。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分3 → V0.5新分2，变化-1。

新裁判理由：

> 答案evidence_registry的4条来源均为INTERNAL_KNOWLEDGE_ONLY，只有数据库名/记录名而无locator，无法定位到具体条目并核对支持内容。按D5六状态，决策相关组均为MISSING_SOURCE；无已核实错引，不cap。因确实提供了evidence_id与claim_scope映射，但不是可核查来源，取2。

<details><summary>V0.4理由与本行变化背景</summary>

evidence_registry 4条全部 source_type=INTERNAL_KNOWLEDGE_ONLY，locator=null，record_id多为库名/物种名/路线名而非条目级定位。按四.3属 MISSING_SOURCE（仅有内部知识自我声明），决策相关组(CORE/APPLICATION_CRITICAL)全部无条目级可核对来源，D5低分档。E0=EVIDENCE_GAP，引用内容无法核实→不作已核实错引、不cap。&#x27;几乎无法定位到条目级依据&#x27;，取3。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.evidence_registry：答案自述来源类型与record_id；不证明来源真实存在或支持结论。
- RUBRIC_CLAUSE / R2-34：INTERNAL_KNOWLEDGE_ONLY按来源缺失处理；不自动触发错引cap。

</details>

### D6 不确定性与诚实度：8 / SCORED

V0.4旧分7 → V0.5新分8，变化+1。

新裁判理由：

> 答案对证据性质有较好区分：多数步骤和性状显式标注low/medium/unknown，uncertainties列出未实时查询、转氨酶/氧化脱羧酶归属未证、S5酶来自假单胞菌等限制，未知性状以null保留。个别通用性状标high但属常识级，未构成系统性把预测当观测。按7–8档，主要限制与未知已说明，取8。

<details><summary>V0.4理由与本行变化背景</summary>

答案专门列出uncertainties（路线、各步酶、辅因子/特异性、菌株能力、性状来源），逐条标注low/medium置信并明示&#x27;基于内部知识重建、未实时查询数据库&#x27;，区分观测与推断，诚实说明未知与矛盾。仅个别性状以high置信标注无引用来源、并把自身路线断言为&#x27;题面给定&#x27;略超证据（单点过度确信），未见系统性把预测当实证或掩盖矛盾。&#x27;大部分证据性质正确标注、主要限制已说明&#x27;，取7。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案对不确定性、内部知识和置信度的自述；用于D6披露质量评价。
- RUBRIC_CLAUSE / R2-119：个别high标签不自动构成系统性误导。

</details>

## DeepSeek

答案SHA256：`c09dd8b1add83aa1e1516614c54d471d9027fffe13f9566a2a813103fbbce6d3`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 答案回显了指定路线名，但实际交付的是 L-arginine→2-ketoarginine→2-ketoornithine→1-pyrroline-2-carboxylate→2-ketoglutarate 的另一条四步路线，未覆盖题面锁定的 oxidative Stickland 六步主链；15项性状只填5项，其余显式未知。属严重任务/路线偏离，按D1关键错误cap≤4，取3。

<details><summary>V0.4理由与本行变化背景</summary>

答案以JSON交付4步主链、3个酶（S3 enzyme为null）、1个菌和15项性状，但主链化学路线与题面指定路线不符：题面要求L-arginine degradation XIV (oxidative Stickland reaction)，gold为6步且终点D-alanine/acetyl-CoA；答案终止于2-ketoglutarate，且S3缺酶、15项性状仅5项有值。属D1任务参数/路线偏离关键错误，cap≤4，档内取3。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT#BIOPATH150_081：锁定指定路线为L-arginine degradation XIV (oxidative Stickland reaction)；不是替代路线许可。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_081：显示答案实际给出的是另一条四步路线，不能据此证明目标主链完成。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：显示本题冻结主链和终点D-alanine/acetyl-CoA；gold非穷尽，但用于任务符合度对照。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 答案的四步路线自身看似连贯，但相对于题面锁定的 oxidative Stickland 目标主链，起点、转化序列和终点均不符：以L-arginine dehydrogenase起始，转向2-ketoglutarate，未到D-alanine/acetyl-CoA；S2水解还遗漏urea。按D2关键错误cap≤4，取3。

<details><summary>V0.4理由与本行变化背景</summary>

四步内部可辨认，但主链不是题面指定路线：首步被写成氧化脱氨生成2-ketoarginine，而gold指定路线首步为arginine deiminase生成citrulline；后续继续走向2-ketoglutarate，与gold终点D-alanine/acetyl-CoA不符，且未声明替代路线。按合理替代路线四步判断，未声明地严重偏离题面指定路线/终点使D2主要结论失效，cap≤4；因步骤结构仍可辨，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- QUESTION_TEXT / QUESTION_TEXT#BIOPATH150_081：指定 oxidative Stickland 路线，为主链方向评价提供任务边界。
- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_081：显示答案对目标主链的替代化学；不能回填目标完成。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：给出冻结主链和终点D-alanine/acetyl-CoA；用于比较核心转化、方向和终点。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 六个必答目标反应S01-S06在冻结矩阵中均为MISSING/ROUTE_BLOCKED_MISSING；答案的S1-S4是另一条路线，不能获得任何目标反应信用。错误路线内部酶自洽不获目标信用；无可用目标催化对应，按&#91;1,2&#93;下沿取1。

<details><summary>V0.4理由与本行变化背景</summary>

S1/S2/S4给出酶名与EC，酶大类与所述反应类型大体相配；S3标为spontaneous并enzyme=null。关键问题是EC 1.4.1.24、3.5.3.23、1.5.1.12的accepted name/reaction在E0 EVIDENCE_GAP下无法核验，且这些酶不是gold指定路线的对应酶；有合理候选但关键步骤缺具体核验，5分。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_081：仅证明答案给出了另一路线的酶/EC，不证明其对应本题必答目标反应。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：列出六个必答目标反应；用于确认答案无目标步对应。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：给出各目标步可接受酶集；不能把替代路线内部酶自洽算作目标成功。

</details>

### D3b 微生物身份与能力：7 / SCORED

V0.4旧分7 → V0.5新分7，变化+0。

新裁判理由：

> TaxID 1511在gold中对应Acetoanaerobium sticklandii（常与旧名Clostridium sticklandii关联），且gold pathway_complete=TRUE，支持主要微生物身份与目标路线全路径能力；答案也一致使用同一profile。扣分点在于ATCC 12634菌株级身份及对答案替代路线各步的具体催化能力未获E0/现有材料核验，故不宜进入9-10。

<details><summary>V0.4理由与本行变化背景</summary>

答案全步使用Clostridium sticklandii ATCC 12634、TaxID 1511。gold organism_gold中TaxID 1511对应Acetoanaerobium sticklandii（Clostridium sticklandii为异名），且PATHWAY_COMPLETE给TaxID 1511 pathway_complete TRUE，主要物种身份与完整路径能力有支持；但菌株ATCC 12634及本答案四个具体非gold步骤的反应级能力未在E0/gold逐步核验，档内取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_081：显示答案使用Clostridium sticklandii ATCC 12634/taxid1511作为唯一菌，并声明complete_pathway ORG_001。
- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_081：支持Acetoanaerobium sticklandii taxid1511作为目标路线全路径菌；不自动核验ATCC12634菌株或替代路线各步能力。

</details>

### D4 性状科学性：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 15项性状中实际填写5项，其余10项显式null/unknown，无遗漏字段。已填F10 motile、F11 rod-shaped、F12 Gram-positive、F13 spore-forming与gold observed值一致；F1 obligate anaerobe仅低置信、与gold“aerotolerant No robust majority”关系不明确。温度、pH、盐度、基因组等关键定量项缺失，按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

15项字段齐全，但仅5项有值：F10 motile、F11 rod-shaped、F12 Gram-positive、F13 spore-forming与gold TaxID 1511观察值相符；F1 obligate anaerobe仅internal knowledge，gold为aerotolerant no robust majority（不直接支持也不直接矛盾）；温度/pH/盐度/基因组等10项为null。部分性状准确但关键定量项缺失且无原始记录，5分。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_081：显示已填和显式未知的性状项，以及来源标注为内部知识。
- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_081：支持部分观察性状并与答案已填值对照；不把物种级记录扩展为答案未声称内容。

</details>

### D5 来源与可核查性：2 / SCORED

V0.4旧分2 → V0.5新分2，变化+0。

新裁判理由：

> 答案的step和trait均只指向EVID_001/EVID_002，二者source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；无法从可定位文献、数据库条目或计算记录核对关键结论。按MISSING_SOURCE低分档取2；这是缺失而非已核实错引，不cap。

<details><summary>V0.4理由与本行变化背景</summary>

两条evidence_registry均为INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator全null；所有决策相关组只有内部自述，无法沿可定位条目核对。E0为EVIDENCE_GAP，不能核实错引，故保持UNRESOLVED、不判虚构/不判CONTRADICTED；按MISSING_SOURCE低分档给2，不触发cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_081：显示来源仅内部知识，无可定位数据库条目或文献记录。
- RUBRIC_CLAUSE / P34：内部知识自我声明按MISSING_SOURCE低分档，默认不触发关键错误cap。

</details>

### D6 不确定性与诚实度：6 / SCORED

V0.4旧分5 → V0.5新分6，变化+1。

新裁判理由：

> 答案对多数已填项标了low，对缺失性状标unknown/null，并明确evidence为INTERNAL_KNOWLEDGE_ONLY，未见把预测系统性冒充实验；但uncertainties为空，complete_pathway_organism_profile_id与route_summary较断言化，主要限制未文字化。按5–6档取6。

<details><summary>V0.4理由与本行变化背景</summary>

全篇使用low/unknown置信，未把未核实内容标high，这是正面；但uncertainties为空，route_summary和complete_pathway声称以事实语气给出，未说明证据性质、主要限制、替代路线或冲突；披露过于笼统，部分结论强度超过依据，档内5。

背景标签：OFFLINE_DERIVATIVE_WITH_ORIGINAL_TRANSFER;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER_TEXT#BIOPATH150_081：显示低置信/unknown标注和内部知识来源，同时也显示限制说明不足。
- RUBRIC_CLAUSE / P119：用于区分单点/局部披露不足与系统性误导；本答案不按系统性cap。

</details>

## Kimi

答案SHA256：`15b6a37e11301361b57f924b58277e31469fdf121fa1ac9929e5e4e3c11eb8e7`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 答案格式完整，含4步主链、每步酶与微生物、15项性状；但主链步骤与题面指定路线的冻结主链完全不符（gold为6步ADI/ornithine racemase/aminomutase/Ord/thiolase，答为4步2-oxoarginine/4-guanidinobutyrate支路），构成严重任务偏离。按D1任务符合度关键错误，capped≤4，取3。

<details><summary>V0.4理由与本行变化背景</summary>

模块与格式层面完整：4步均给出主底物/主产物英文名与SMILES、逐步酶（2步EC/null并自述不确定）、逐步微生物与profile引用；15项性状齐备（11填、4明确未知、0遗漏）；证据登记、不确定性、下游与分支声明齐全。但交付的化学主链不是题面指定路线（BSY-p00604）的主链：指定路线起点为精氨酸脱亚胺酶（S03）经瓜氨酸/鸟氨酸支路、末端为乙酰-CoA+D-丙氨酸，答案却以2-酮精氨酸→4-胍基丁酸为主链，并把与该路线一致的ADI支路列为非主链分支，且在notes/route_summary中自称即为该路线。按P100「自称合规却交付不同化学路线」属D1关键错误，cap≤4；因无缺模块、交付无工程缺陷，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：显示指定路线gold主链的实际步骤与中间体，用于对比答案主链；不证明答案化学本身错误。
- ANSWER_TEXT / ANSWER.steps：答案实际给出的4步主链与酶/微生物。
- SCOPE_ROW / SCOPE#BIOPATH150_081#CG04：题面氧条件未指定，不能作为额外扣分依据。

</details>

### D2 反应化学科学性：4 / SCORED

V0.4旧分4 → V0.5新分4，变化+0。

新裁判理由：

> D2按答案自身化学质量评价：4步方向与辅因子基本闭合，但该序列是2-oxoarginine/4-guanidinobutyrate支路，并非题面指定的oxidative Stickland主链；缺少Stickland还原支路配对，且butyryltransferase/butyrate kinase对4-guanidinobutanoyl底物的广谱性未获支持。主链部分成立但关键化学体系/连接仍需修订，取4。不因与gold不同自动判错，但化学体系与指定route条件不符。

<details><summary>V0.4理由与本行变化背景</summary>

逐维看化学本身：四步反应类型（氧化脱氨→2-氧代酸:铁氧还蛋白氧化还原脱羧→酰基-CoA磷酸解→底物水平磷酸化）类型正确、方向一致、原子计量基本自洽，无凭空跳步，SMILES与命名对应。但这不是指定路线的主链：首步是脱氢酶生成2-酮精氨酸（指定路线首步为脱亚胺酶），瓜氨酸/鸟氨酸/D-鸟氨酸/2,4-二氨基戊酸等关键中间体全部缺失，末端4-胍基丁酸也不同于该路线的乙酰-CoA+D-丙氨酸。按合理替代路线四步判断：①题面已指定路线；②答案未声明这是替代路线（反把与该路线一致的ADI途径列为非主链分支）；③证据仅路径名、无条目级可核记录；④偏离使D2「给出该路线主链」的主要结论失效。故D2关键错误成立，cap≤4；因逐步化学成立、连接清楚，档内取4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.steps：答案自身4步化学式与辅因子。
- RUBRIC_CLAUSE / R2-62：与gold不同不自动错误；D2按自身化学质量评价。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 逐目标核对：答案4步为2-oxoarginine/4-guanidinobutyrate支路，与gold 6步ADI/ornithine racemase/aminomutase/Ord/thiolase主链无一步对应。S=0；S03入口目标被答案S1替换为不同反应（F），其余目标未交付（M）。U=0，C=0，落&#91;1,2&#93;；几乎无目标催化对应，取1。错误路线内部酶自洽不获目标信用。

<details><summary>V0.4理由与本行变化背景</summary>

S3磷酸丁酰转移酶EC 2.3.1.19、S4丁酸激酶EC 2.7.2.7的名称-EC-反应类型彼此一致；S1精氨酸脱氢酶与S2 2-氧代酸:铁氧还蛋白氧化还原酶EC与基因留null并自述不确定，符合诚实null。问题在于：把丁酸（C4直链）特异酶用于胍基丁酰底物属广谱性外推、直接催化证据有限（答案自述）；且指定路线的关键酶集合（Ord/EC 1.4.1.26、鸟氨酸氨甲酰转移酶2.1.3.3、精氨酸脱亚胺酶3.5.3.6、硫解酶2.3.1.263、D-鸟氨酸4,5-氨基变位酶5.4.3.5、鸟氨酸消旋酶5.1.1.10/12）完全缺失。属「有合理候选和部分支持，但若干关键步骤仍缺具体核验」的5–6档，取5；不因错引归D5而在此另计。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：gold各必答步的酶名/EC。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：gold各必答步的底物/产物与方向。
- ANSWER_TEXT / ANSWER.steps：答案实际给出的4步反应与酶。

</details>

### D3b 微生物身份与能力：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 微生物身份为Clostridium sticklandii ATCC 12662，与gold的Acetoanaerobium sticklandii（同物种，旧名）对应，身份定位基本正确；但答案把4步2-oxoarginine/4-guanidinobutyrate支路全部归给该菌并设complete_pathway_organism_profile_id，该特定路线的单步/全路径能力无对应证据（gold PATHWAY_COMPLETE仅支持gold主链）。属合理候选+部分身份支持，但关键作用范围未核，取5。

<details><summary>V0.4理由与本行变化背景</summary>

物种身份与该路线主菌一致：答案为Clostridium sticklandii（gold为Acetoanaerobium sticklandii，TaxID 1511，全部步的主归属），属同物异名，非跨类群错配；ncbi_taxid按纪律留null未编造。菌株与保藏号ATCC 12662为菌株级声称，E0无记录、gold F5=UNKNOWN，属未核（未核≠错误），不触发身份阶梯cap。步级反应能力（2-氧代酸脱羧、胍基丁酰磷酸化等）缺少该菌的具体催化证据，答案自述菌株层面证据有限；complete_pathway_organism_profile_id=ORG_001的单菌完成路径声称，gold对TaxID 1511的PATHWAY_COMPLETE=TRUE仅支持物种级对gold路线的完整路径能力。综合属「有合理候选和部分支持，但若干关键身份或作用范围仍未充分核验」，取6。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_081：gold主要organism为Acetoanaerobium sticklandii (TaxID 1511)，PATHWAY_COMPLETE行支持gold主链，不支持答案替代支路。
- ANSWER_TEXT / ANSWER.organism_profiles：答案使用Clostridium sticklandii ATCC 12662并声称整条路径。

</details>

### D4 性状科学性：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 已给性状中F11杆状、F12革兰氏阳性、F13产孢与gold observed一致；F2 preference=mesophilic与gold一致。但F2数值、F3/F4/F14等关键项为null，F5 ATCC 12662、F6受体氨基酸、F7/F8/F9/F15等无对应gold observed支持，部分仅EVID_002内部知识。按D4正确性/适用性，部分准确但关键证据不足，取5；缺失完成度不重复重扣。

<details><summary>V0.4理由与本行变化背景</summary>

按性状重要度看：已填的核心观测性状与gold一致——F11杆状（rod-shaped）、F12革兰氏阳性（true）、F13产芽孢（true）、F2温度偏好「中温/嗜温」（preference=mesophilic）；F6厌氧发酵+氨基酸为受体的描述与Stickland生理相符。但关键数值与可核项缺失：F2把gold观测的minimum 30°C/maximum 37°C留null；F10运动性（gold观测true）留null；F14基因组（GCA_000196455.1、GC 33.3%、约2.72 Mb）留null；F5 ATCC 12662与F9具体酶活为未核声称；F1「专性厌氧」与gold aerotolerant=No robust majority仅不矛盾。属「部分性状准确且适用，但关键项证据不足」的5–6档，取6；性状缺失的完成度问题主要归D1，不在此重复重扣。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_081：gold observed性状：F11 rod-shaped、F12 gram positive true、F13 sporulation true、F2 preference mesophilic；不支持答案未给或未核项。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_081：标明F3/F4等为completeness_only，F2数值可评分；用于区分缺失与错误。
- ANSWER_TEXT / ANSWER.organism_profiles&#91;0&#93;.traits：答案实际填写的15项性状值。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> EVID_001以MetaCyc pathway名支撑答案主链，但gold同名pathway的步骤为S03 arginine deiminase→S02 ornithine carbamoyltransferase→S06 ornithine racemase→S05 D-ornithine aminomutase→S01 Ord→S04 thioacylase，与答案4步2-oxoarginine/4-guanidinobutyrate支路不同；核心引用存在但不支持所声称反应序列，登记VERIFIED_MIS_CITATION_CRITICAL。其余EVID_002为INTERNAL_KNOWLEDGE_ONLY，EVID_003/004/005因E0 gap无法核验，登记UNRESOLVED_SOURCE。D5按CRITICAL cap≤4，考虑其余证据尚有具体书目/保藏记录，取3。

<details><summary>V0.4理由与本行变化背景</summary>

按claim group合成：决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）的路线、酶、菌归属几乎全部由EVID_001「MetaCyc—Pathway: L-arginine degradation XIV」路径名支撑，record_id=null、无法定位到条目（GENERIC_SOURCE）；ATCC 12662、EC 2.3.1.19/2.7.2.7以及两篇文献的条目/内容在E0均无记录（EVIDENCE_GAP→UNRESOLVED_SOURCE）；多项性状仅EVID_002 INTERNAL_KNOWLEDGE_ONLY（MISSING_SOURCE）。决策相关组不存在「条目级可定位且可核对」的证据，按R2合成规则落3–4档，取4。因统一冻结证据为整题缺口，不把路径名引用认定为已核实错引（不cap），疑似「引用不支持其reaction_sequence」登记为UNRESOLVED待核；EVID_003/005为可定位文献书目（SUPPORTING组），不得跨档上调决策相关组。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;NEW_RATER_KEY_ERROR_JUDGEMENT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：显示同名pathway的实际步骤与顺序，用于核对EVID_001支持范围。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：显示gold各步酶名/EC，证明EVID_001不能支持答案的酶-反应序列。
- ANSWER_TEXT / ANSWER.evidence_registry：答案实际交付的引用记录与locator。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案对EC/基因归属、电子受体、菌株层面证据、表示差异等列出具体不确定性，并大量使用null/low，不是系统性把预测写成观测。但核心路线断言过强：未披露其4步支路与所引MetaCyc pathway及题面指定主链不一致，属主要限制/冲突未说明。按D6单点/主要披露不足，不改cap，取5。

<details><summary>V0.4理由与本行变化背景</summary>

披露面明显优于均值：逐条列出EC/基因未知（按纪律填null）、电子受体的其它表示可能、菌株层面证据有限、不同表示会合并磷酸转移/激酶两步；逐字段给low/medium置信；主动声明下游延续与ADI分支不属评分主链并排除。但存在路线级过度确信：把EVID_001（仅路径名、无record_id）标为DATABASE_DIRECT并以medium覆盖reaction_sequence/main_compounds/enzyme_assignment/organism_assignment，uncertainties还断言「主链化合物序列一致」，等于把未核路线包装为数据库直查支持；未发现明知掩盖矛盾的证据。按P119，单点/路线级过度确信属5–6档，取6。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER.uncertainties：答案实际披露的不确定性列表。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：用于说明答案未披露主链与gold冲突。

</details>

## Qwen

答案SHA256：`d14438ac8e5647bd25132163eb545964664d2c33dad8f49d2e4ecc1711fc8b85`。

### D1 完整性与任务符合度：3 / SCORED

V0.4旧分4 → V0.5新分3，变化-1。

新裁判理由：

> 答案覆盖了路径、酶、微生物和15项性状的填报外壳，但把题面指定的 L-arginine degradation XIV (oxidative Stickland reaction) 主链换成了精氨酸转氨酶/4-胍基丁酸路线；指定主链的脱亚胺酶入口、鸟氨酸/瓜氨酸相关步骤及D-alanine/acetyl-CoA终点均未交付。属任务路线严重偏离，D1关键错误成立，在≤4内取3。

<details><summary>V0.4理由与本行变化背景</summary>

六个交付模块（路径4步、每步酶、每步菌、单profile共15性状字段、2条证据、4条不确定性）均有实质交付且格式正常，覆盖度本身不差；但题面以route_scope指定唯一路线，答案原样回填路线名，却交付精氨酸转氨酶—胍基丁酸支路（Arg→5-guanidino-2-oxopentanoate→4-guanidinobutanoyl-CoA→4-guanidinobutanoate→4-aminobutanoate+尿素），与冻结gold该路线登记的S01–S06主链（Arg→citrulline→ornithine→D-ornithine→(2R,4S)-2,4-diaminopentanoate→(2R)-2-amino-4-oxopentanoate→acetyl-CoA+D-alanine）不同，且未声明为替代路线，属‘自称合规却交付不同路线’的任务参数偏离，按八.D1与P100列为本维关键错误并封顶；因模块交付完整、撰写清楚，取封顶档上限4。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：支持gold主链各步底物/产物与方向，包括S03精氨酸脱亚胺酶入口和S04终点D-alanine/acetyl-CoA；不支持答案的转氨酶替代路线。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：支持gold各步首选酶/EC，如S03 EC3.5.3.6、S04 EC2.3.1.263；不支持答案S1 EC2.6.1.84替代入口。
- ANSWER_TEXT / ANSWER：显示答案自行交付4步转氨酶/胍基丁酸路线，而非题面指定主链。

</details>

### D2 反应化学科学性：3 / SCORED

V0.4旧分6 → V0.5新分3，变化-3。

新裁判理由：

> 答案四步在替代精氨酸转氨酶路线上大体连续：转氨、氧化脱羧、硫酯水解、胍基水解，化学方向可理解；但它不是题面指定主链，且缺失gold的脱亚胺/鸟氨酸/瓜氨酸核心转化与D-alanine/acetyl-CoA终点，S2辅因子和电子受体交代不足。按本题允许的D2范围&#91;1,4&#93;取3。

<details><summary>V0.4理由与本行变化背景</summary>

就答案自身四步核对：S1转氨（Arg+2-oxoglutarate→5-guanidino-2-oxopentanoate+L-glutamate）、S2氧化脱羧（C5→C4+CO2并生成CoA硫酯）、S3硫酯水解、S4胍基水解（C5H11N3O2+H2O→GABA+urea），方向一致、主产物结构对应、逐步碳氮氧计量守恒，未出现反向、起始步化学错误或无依据跳步，属化学上可成立的支路；但该支路不是题面指定路线的化学主链（路线身份问题已在RE-01/D1独立计入，不重复计为D2关键错误），且辅因子（ferredoxin/NAD+、CoA计量）只以文字带过、合理性证据有限，故落5–6档并取6。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：给出指定主链的底物/产物、方向和终点；用于对照答案替代路线，不支持把替代路线回填为指定主链完成。
- ANSWER_TEXT / ANSWER：显示答案四步的化学转化及缺失的指定主链步骤。

</details>

### D3a 目标反应与酶对应：1 / SCORED

V0.4旧分5 → V0.5新分1，变化-4。

新裁判理由：

> 六个必答gold目标反应均未得到目标酶/EC匹配：答案的EC2.6.1.84、1.2.7.7、3.5.3.21及未编号酰基-CoA水解酶，均不对应S01-S06的accepted酶集合（Ord 1.4.1.26、OTC 2.1.3.3、arginine deiminase 3.5.3.6、thiolase 2.3.1.263、aminomutase 5.4.3.5、racemase 5.1.1.10/12）。模块有酶但全在错误路线，按SCORED失败锚点评，不给MISSING；目标催化对应几乎为零，取1。

<details><summary>V0.4理由与本行变化背景</summary>

酶名—EC类别与所述反应类型大体自洽：2.6.1（转氨）、1.2.7（以铁硫蛋白为受体的氧化还原脱羧）、3.5.3（胍基水解）；S3 EC明确留null属诚实缺失。但S3为关键水解步骤却无EC，2.6.1.84与答案所用氨基受体2-oxoglutarate的匹配性存疑，且全部EC在E0均无记录可核（GAP-081-002/007/009），只有合理候选与部分支持，故落5–6档取5。

背景标签：TASK_ROUTE_OR_TARGET_POLICY_CONTEXT;TARGET_REACTION_ACCEPTED_EVIDENCE_RULE_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：列出本题gold六步accepted酶名/EC；不支持答案四个替代酶对应的目标反应。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：列出gold各目标步骤底物/产物，用于确认答案步骤属于不同路线而非目标步骤。
- ANSWER_TEXT / ANSWER：显示答案所填酶和EC及其对应反应。

</details>

### D3b 微生物身份与能力：3 / SCORED

V0.4旧分5 → V0.5新分3，变化-2。

新裁判理由：

> 答案把全部步骤和完整路径能力都归给 Clostridium botulinum（TaxID 1491），而gold主链步骤对应的是 Acetoanaerobium sticklandii（TaxID 1511），且 gold PATHWAY_COMPLETE 记录未含1491。TaxID/菌株能力在E0中不可核验，因此不能判虚构；但以单一C. botulinum承担全路径属于将未核验能力写成完整路径，主要微生物对应与范围支持不足，取3。

<details><summary>V0.4理由与本行变化背景</summary>

四步均指派同一物种Clostridium botulinum（TaxID 1491，strain为null），该物种是真实的氨基酸发酵厌氧菌，作Stickland类候选尚属合理；但全题无株级身份，步级催化归属与完整路径能力都没有条目级证据（EVID_001仅为无record_id的MetaCyc路线名，EVID_002为INTERNAL_KNOWLEDGE_ONLY），且与gold主要物种Acetoanaerobium sticklandii（TaxID 1511）不同。属‘有合理候选和部分支持，但关键身份与作用范围未充分核验’，5–6档取5。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_081：支持gold各步对应 Acetoanaerobium sticklandii 等生物及PATHWAY_COMPLETE清单；不支持答案把C. botulinum 1491写成该主链全路径菌。
- ANSWER_TEXT / ANSWER：显示答案统一使用C. botulinum及完整路径归属声称。

</details>

### D4 性状科学性：3 / SCORED

V0.4旧分7 → V0.5新分3，变化-4。

新裁判理由：

> 答案提供15项性状中11项填写、4项明确null，完成度尚可；但所有性状绑定到C. botulinum ORG_001，而该菌不是gold主链对应菌，且E0无该菌性状记录，多项为泛化/低置信度内部知识，关键定量项缺失（pH、盐度、保藏、基因组均null）。按性状适用性与关键缺口取3。

<details><summary>V0.4理由与本行变化背景</summary>

已填性状（专性厌氧、Gram-positive、杆状、产芽孢、运动性阳性、嗜温、氨基酸发酵且以氨基酸为末端电子受体、氨基酸碳源、土壤/沉积物/食品栖息地）与所指物种Clostridium botulinum的公认种级性状相符；未给数值故无单位/范围误读，也未把预测冒充实测（confidence多为low，EVID_002明示内部知识）；温、pH、盐度、保藏号、基因组数值为诚实null（完整性扣分归D1，不在此重复重扣）。性状均为种级、缺原始记录与定量值，属少量条件/来源问题，7–8档取7。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT;REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_081：提供gold主链菌的性状记录；不含C. botulinum 1491，不能支持答案性状值，也不能判其全部错误。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_081：显示本题可观测/可评分性状覆盖范围；不支持将generic内部知识当作已核性状。
- ANSWER_TEXT / ANSWER：显示答案15项性状的填写与null分布。

</details>

### D5 来源与可核查性：3 / SCORED

V0.4旧分3 → V0.5新分3，变化+0。

新裁判理由：

> 核心结论主要依赖EVID_001（MetaCyc pathway name，无record_id/locator仅路径名）和EVID_002（INTERNAL_KNOWLEDGE_ONLY）。决策相关组（路线、酶-EC、菌身份、全路径能力）没有条目级可定位记录；性状与分类学为内部知识。因E0为EVIDENCE_GAP，不能判已核错引，但来源交付本身仅达到笼统/内部知识档，按D5 3–4档取3。

<details><summary>V0.4理由与本行变化背景</summary>

决策相关组（CG01/CG02/CG03/CG05/CG07/CG08/CG09）只见到EVID_001（MetaCyc库名+路线名，record_id=null，无法定位到条目）与EVID_002（INTERNAL_KNOWLEDGE_ONLY）；性状各组（CG10–CG16）全为内部知识。按四.3/P41：决策相关组全部仅有笼统来源→3–4档，SUPPORTING组条目级证据不得跨档上调，故取3。路线名指向的条目的实际支持范围（是否支持答案四步与C. botulinum归属）因E0无该条目记录、且该引文为未解析自由文本（GAP-081-026），记UNRESOLVED_SOURCE待核，不判已核实错引、不cap。

背景标签：EVIDENCE_INTERPRETATION_CONTEXT。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案实际交付的来源仅为路径名级数据库引用与内部知识，无具体record_id或可定位条目。

</details>

### D6 不确定性与诚实度：5 / SCORED

V0.4旧分6 → V0.5新分5，变化-1。

新裁判理由：

> 答案对氧条件未指定、第一步替代可能、辅因子/EC未知、性状仅为泛化知识等作了披露，且大量性状用low/unknown，具备部分不确定性说明。但其route_summary仍把替代转氨酶路线写成“指定路线中”的主链，并把ORG_001标为完整路径菌，未披露该路线与gold主链不一致；证据类型/置信度与主要结论强度仍不完全相称。取5。

<details><summary>V0.4理由与本行变化背景</summary>

证据性质披露总体诚实：confidence多为low/medium，EVID_002明示INTERNAL_KNOWLEDGE_ONLY，uncertainties具体列出氧条件未定、首步存在转氨/脱氢两种可能、CoA中间体与辅因子未核、性状未绑定菌株或文献；S3 EC留null亦属诚实。不足在于把仅有无record_id路线名的EVID_001以medium标为支撑main reactions与organism assignment，且未披露所交付四步路线与题面指定路线主链不一致这一主要限制，属部分结论强度超过依据（单点过度确信/限制未说明），5–6档取6；非系统性把预测写成实证，不cap。

背景标签：REASSESSMENT_EFFECT_NOT_SEPARATELY_IDENTIFIED。

这些标签不是规则独立因果贡献；参考纠正、执行修复和评分者裁量可并存。

</details>

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / ANSWER：显示答案已列不确定性但未披露路线主链偏离及完整路径能力依据不足。

</details>

## Grok

答案SHA256：`f8ea79190a58a3bf0650dd9a46cbf75ec118986feec1d9a82eb78dab5e2be7ef`。

### D1 完整性与任务符合度：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案按格式交付了路线、酶、微生物、性状与不确定性，但route_scope只原样写了路线名；route_summary与steps实际执行的是另一条L-arginine→2-oxo-5-guanidinopentanoate→4-guanidinobutanoyl-CoA→4-aminobutanoate→succinate链，未交付gold的arginine deiminase/ornithine轴及D-alanine/acetyl-CoA终点。该内容偏离属于D1任务符合度关键错误，按cap≤4取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_081：gold给出指定路线名、起点L-arginine与终点D-alanine|acetyl-CoA；不支持答案以succinate为终点的替代链。
- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_081：gold记录六个有序必答步；不支持答案七步替代链作为指定主链。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：gold反应行给出S01-S06目标反应；答案的S1-S7反应不在该目标主链上。

</details>

### D2 反应化学科学性：4 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案自身步骤大体连贯，但按题面指定主链核D2核心化学时，gold首步为S03 arginine deiminase（L-arginine→citrulline），答案首步为转氨生成2-oxo-5-guanidinopentanoate，且一路到succinate而非D-alanine/acetyl-CoA；指定主链起点、核心转化和终点均不符，属D2主链方向/核心转化关键错误，按cap≤4取4。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：gold首步为L-arginine→citrulline，末步为D-alanine/acetyl-CoA；不支持答案的succinate终端替代链。
- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：gold目标步酶为Ord/OTC/arginine deiminase/thiolase等；不支持答案的转氨酶/胍基丁酸酶链作为指定主链。

</details>

### D3a 目标反应与酶对应：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 六个目标步S01-S06均未在答案中以目标反应形式交付；答案S1-S7的酶与反应属于另一条精氨酸→胍基丁酸→succinate路线，不能获得目标信用。因酶模块并非完全未填，不按整维MISSING=1，而按目标失败锚点在&#91;1,2&#93;内取2：有可读的酶功能细节，但目标反应对应不可用。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：gold目标步酶集合为Ord、OTC、arginine deiminase、thiolase、aminomutase、racemase；不支持答案替代酶作为目标步。
- GOLD_SLICE / reaction_gold.tsv#case:BIOPATH150_081：gold目标反应底物/产物与答案S1-S7不匹配；答案酶只在替代路线内部自洽。

</details>

### D3b 微生物身份与能力：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案统一使用Clostridium sticklandii DSM 519（Acetoanaerobium sticklandii的旧名/同物）作为各步微生物；gold organism_gold将Acetoanaerobium sticklandii TaxID 1511映射到全部目标步且PATHWAY_COMPLETE=TRUE。旧名与DSM 519未在TaxID三件套中独立核验，故不取9–10，给8。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_081：TaxID 1511 Acetoanaerobium sticklandii映射到S01-S06且全路径可完成为TRUE；未单独核验DSM 519字符串。

</details>

### D4 性状科学性：6 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> gold可评观测项中，运动性true、杆状、革兰氏阳性、temperature preference mesophilic与答案相符；但答案将产孢、基因组基本信息填null，而这些在gold中有观测/记录；F5、F6、F7、F8、F9、F15等多为内部知识且未在E0核验。故为部分性状准确、关键项证据不足，给6。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_081：TaxID1511观测项支持motility=true、rod-shaped、gram positive、mesophilic；同时记录sporulation=true与genome数据，答案未填。
- GOLD_SLICE / trait_scoreability_mask.tsv#case:BIOPATH150_081：标出F2/F10/F11/F12/F13/F14等可评观测项；F1/F3/F4等多为completeness/predicted background。
- GOLD_SLICE / trait_subfield_scoreability_mask.tsv#case:BIOPATH150_081：给出温度等子字段的可评/待裁粒度；不支持把未核内部知识升为已观测。

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry仅有EVID_001/EVID_002两条INTERNAL_KNOWLEDGE_ONLY；路线、酶、微生物、性状均无可定位数据库条目、DOI或计算记录。部分性状可被gold旁证，但答案未交付这些来源。无已核实错引，因无实际可核引用；按MISSING_SOURCE低档，取2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / trait_gold.tsv#case:BIOPATH150_081：可用于旁证少数性状，但这不是答案交付的来源记录；不支持把内部知识声明升为可追溯证据。

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案对内部知识、低/中置信、EC/基因未核实、未知性状null、TaxID等未知均有明确披露；route_scope.notes与uncertainties列出范围不确定和辅因子SMILES未给。个别性状/归属可能偏强，但未系统性把预测写成实证，给8。

## GPT5.6

答案SHA256：`250f520ba95e2f727e373058e6eaddabeaace7d3cac264fd7e29f0e268f9b4a2`。

### D1 完整性与任务符合度：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 题面锁定6步主链，答案仅交付1步且该步不对应任何gold必答步；15项性状全为null/unknown，核心任务模块大部缺失，按D1关键错误低档给2。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / formal_cases.tsv#case:BIOPATH150_081：证明本案主链为LINEAR_UNIQUE且ordered_step_count=6，不是单步任务
- ANSWER_TEXT / 250f520ba95e2f727e373058e6eaddabeaace7d3cac264fd7e29f0e268f9b4a2：证明答案steps仅1条，且性状均为null/unknown

</details>

### D2 反应化学科学性：3 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> S1命名上可辨为L-arginine氧化脱氨，但底物SMILES=C1=CC(=CC=C1)为苯环占位，与L-arginine结构不符；未列水/电子受体，按所交付结构反应不守恒，且只有单步无法构成可信主链。D2不因路线偏离重复扣，但所给化学表达有实质错误，故入3–4档取3。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 250f520ba95e2f727e373058e6eaddabeaace7d3cac264fd7e29f0e268f9b4a2：显示所交付底物SMILES为苯环占位，不是精氨酸结构；同时显示未列电子受体
- GOLD_SLICE / case_root_identity.tsv#case:BIOPATH150_081：给出目标污染物2-Amino-5-guanidinovaleric acid的冻结isosmiles，用于与答案底物SMILES对照；不支持任何具体酶活性

</details>

### D3a 目标反应与酶对应：1 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 6个必答目标步均无目标反应酶对应；唯一S1所用L-arginine dehydrogenase/EC1.4.99.1不在本案accepted集合（Ord、OTC、arginine deiminase、thiolase、aminomutase、racemase），不能映射到任一gold步，故无目标S。按C04/C05低档给1；酶模块并非全null，不记整维MISSING。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / enzyme_gold.tsv#case:BIOPATH150_081：列出6个gold步的accepted酶/EC集合，其中没有L-arginine dehydrogenase/EC 1.4.99.1；不证明该酶在别处无活性
- ANSWER_TEXT / 250f520ba95e2f727e373058e6eaddabeaace7d3cac264fd7e29f0e268f9b4a2：显示答案仅给出S1一个酶，且为该off-target酶/EC

</details>

### D3b 微生物身份与能力：7 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 微生物为Clostridium sticklandii DSM 519（Acetoanaerobium sticklandii旧名）。Gold对Acetoanaerobium sticklandii TaxID 1511给出全路径能力，物种/路径能力有支持；但答案未给TaxID，DSM 519菌株身份未在本快照单独核验，按“粒度不足档内扣”给7，非已核身份错误。

<details><summary>裁判引用及其声称的支持范围</summary>

- GOLD_SLICE / organism_gold.tsv#case:BIOPATH150_081：显示Acetoanaerobium sticklandii TaxID 1511在PATHWAY_COMPLETE行pathway_complete=TRUE，支持物种级全路径能力；不支持精确核验DSM 519菌株
- ANSWER_TEXT / 250f520ba95e2f727e373058e6eaddabeaace7d3cac264fd7e29f0e268f9b4a2：显示答案给出的物种/菌株与TaxID为null

</details>

### D4 性状科学性：1 / MISSING

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> organism_profiles&#91;0&#93;.traits的15项均为value=null或unknown，未交付任何可评性状值或来源；按P44全null按D4 MISSING=1处理。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 250f520ba95e2f727e373058e6eaddabeaace7d3cac264fd7e29f0e268f9b4a2：显示15项性状全为null/unknown，没有任何性状值或来源

</details>

### D5 来源与可核查性：2 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> evidence_registry仅EVID_001/EVID_002，source_type=INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator均为null；核心路线、酶、菌结论无可定位外部来源，属MISSING_SOURCE低档。未核出具体错引，不触发D5 cap。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 250f520ba95e2f727e373058e6eaddabeaace7d3cac264fd7e29f0e268f9b4a2：显示证据登记仅有内部知识且无外部定位；不支持任何已核实错引

</details>

### D6 不确定性与诚实度：8 / SCORED

无本报告V0.4同答基准，不计算虚构的新旧差值。

新裁判理由：

> 答案多处明确low/unknown，并在uncertainty中列出未指定氧条件、电子受体、下游未扩展、底物SMILES待核；未把内部知识包装成实证。完整路径字段虽有声明，但主要限制已披露；按7–8档取8。

<details><summary>裁判引用及其声称的支持范围</summary>

- ANSWER_TEXT / 250f520ba95e2f727e373058e6eaddabeaace7d3cac264fd7e29f0e268f9b4a2：显示答案明确标注低置信/未知及底物SMILES待核等限制；不等同于科学内容正确

</details>
