# V04-B-011：定点人工复核

- case：BIOPATH150_029
- 只需核定：D3a、D3b、D4。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-011-D3a / D3a

核查问题：核对所写酶名、具体EC和该步反应是否对应；通配EC、近名酶或家族关系不能证明具体催化。缺证时保留待核，不凭负检索判酶不存在。

- 答案具体声称与原文位置：
  - 本答案共 5 步（S1–S5，visible_answer.txt 第13–302行），每步 1 个 enzyme 条目，均绑定同一证据 EVID_001。逐条：
    - S1（第49–55行）：name="cyclohexanol dehydrogenase"（第50行）、ec_number="1.1.1.160"（第51行）、gene_or_protein=null、confidence="medium"、evidence_id="EVID_001"。该步反应_type="oxidation"（第48行）：Cyclohexanol+NAD+ → Cyclohexanone+NADH+H+（第19–47行）。
    - S2（第115–121行）：name="cyclohexanone monooxygenase"（第116行）、ec_number="1.14.13.22"（第117行）、confidence="medium"、evidence_id="EVID_001"。reaction_type="Baeyer-Villiger monooxygenation"（第114行）。
    - S3（第166–172行）：name="6-hexanolide lactonase"（第167行）、ec_number="3.1.1.31"（第168行）、confidence="low"、evidence_id="EVID_001"。reaction_type="hydrolysis"（第165行）。
    - S4（第222–228行）：name="6-hydroxyhexanoate dehydrogenase"（第223行）、ec_number=null（第224行）、confidence="low"；step.uncertainty（第239行）"该步酶学名称与 EC 编号不完全确定，EC 填 null。"
    - S5（第283–289行）：name="adipate semialdehyde dehydrogenase"（第284行）、ec_number=null（第285行）、confidence="low"；step.uncertainty（第300行）同文。
  - evidence_registry 仅 2 条（第418–456行）：EVID_001 source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator="常见好氧微生物环己醇降解主链：cyclohexanol -> cyclohexanone -> 6-hexanolide -> 6-hydroxyhexanoate -> adipate semialdehyde -> adipate；代表菌 Acinetobacter sp. SE19。"、claim_scope 含 "step:S1"…"step:S5","enzyme"、confidence="medium"；EVID_002 亦为 INTERNAL_KNOWLEDGE_ONLY、locator 为属级生理归纳、confidence="low"。
  - uncertainties[2]（第460行）："6-羟基己酸脱氢酶和己二酸半醛脱氢酶的具体 EC 编号未确定，填 null。"

- 核查来源/新证据ID及支持范围：
  - gold/enzyme_gold.tsv（BIOPATH150_029，BSY-p00274，7 行酶记录）：S1 cyclohexanol dehydrogenase EC 1.1.1.245；S2 cyclohexanone monooxygenase EC 1.14.13.22；S3 两并列酶 6-hexanolide hydrolase EC 3.1.1（截断形式）与 1-oxa-2-oxocycloheptane lactonase EC 3.1.1.-（通配）；S4 6-hydroxyhexanoate dehydrogenase EC 1.1.1.258；S5 6-oxohexanoate dehydrogenase EC 1.2.1.63（两行同EC不同enzyme_id）。支持范围：gold 登记本路线逐步首选酶名与EC；不支持范围：gold 是核查基线非唯一允许答案（量表 P27），gold 内无某酶不等于该酶不存在。
  - gold 与答案逐条对照（事实）：S2 酶名与EC逐字符一致（cyclohexanone monooxygenase / 1.14.13.22）；S1 酶名与 gold 逐字符一致但 EC 不同（答案 1.1.1.160 vs gold 1.1.1.245）；S3 答案名"6-hexanolide lactonase"与 gold 两个名（6-hexanolide hydrolase / 1-oxa-2-oxocycloheptane lactonase）均不同字，EC 3.1.1.31 对 gold 截断/通配形式（3.1.1 与 3.1.1.-）；S4 酶名与 gold 逐字符一致、答案 EC=null 对 gold 1.1.1.258；S5 答案名"adipate semialdehyde dehydrogenase"与 gold 名"6-oxohexanoate dehydrogenase"不同字，答案 EC=null 对 gold 1.2.1.63。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：EC 1.1.1.160=OUT_OF_SNAPSHOT_UNRESOLVED（第15行）、EC 1.14.13.22=OUT_OF_SNAPSHOT_UNRESOLVED（第30行）、EC 3.1.1.31=OUT_OF_SNAPSHOT_UNRESOLVED（第48行）——三行均注明"只登记能否定位既有冻结记录；未联网补齐；UNRESOLVED不判虚构也不判支持"。
  - evidence/facts/IUBMB_EXPLORENZ/ 共 20 张卡（ec_1.14.12.11、ec_1.3.1.19、ec_1.3.1.86、ec_3.7.1.5、ec_3.7.1.25 等）；**没有** 1.1.1.160、1.1.1.245、1.14.13.22、3.1.1.31、1.1.1.258、1.2.1.63 任一张卡 → 答案三个具体 EC 与 gold 三个 EC 在本包内均无官方 accepted name/reaction 可核（P66 第三分支的"无法核验"前提成立；P71 要求的 EC 核验对象缺失）。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv 为物种名映射表，与酶名/EC无关，本维无用例。
  - 包内缺口（事实）：上述 6 个 EC 的 IUBMB 卡、答案 S3/S5 酶名的任何事实卡、环己醇降解相关文献卡均无 → 记 UNRESOLVED、待联网核查。

- 关键事实（供本人判断，非结论）：
  1. 答案 D3a 交付 5 个酶条目：3 个有具体 EC（1.1.1.160 / 1.14.13.22 / 3.1.1.31）、2 个 EC=null 并两处主动披露（S4/S5 step.uncertainty + uncertainties[2]）。
  2. 与 gold 的差异类型分布（事实，不判级）：酶名层面——S1、S2、S4 与 gold 同名，S3、S5 不同名；EC 层面——S2 与 gold 同号，S1 与 gold 异号（1.1.1.160 vs 1.1.1.245），S3 为具体号对 gold 通配/截断号，S4/S5 答案 null。
  3. 包内证据缺口：答案与 gold 涉及的全部 6 个 EC 均无 IUBMB 冻结卡，EVIDENCE_COVERAGE_REGISTER 相应行均为 OUT_OF_SNAPSHOT_UNRESOLVED → P64/P66 的"查官方条目再定"动作在包内无法执行。
  4. 量表条款（一句话）：R3/D3a 关键错误清单（P98 表 R3）="EC大类别与反应类型不匹配；酶名与EC互相矛盾；把广谱家族相关性当成该具体反应的催化证据"；P71 要求具体EC先核 accepted name/reaction/状态；P66 单值冲突无法核验时→UNRESOLVED、保留低分与待核标记、不cap；P64 gold 通配EC时答案具体号不自动判错；P72 核验只给事实状态不自动给分或cap。
  5. EC 大类与反应类型的字面对应（纯登记，不判"匹配"结论）：1.1.1.160 与 1.1.1.245 同属 EC 1.1.1（NAD/脱氢）；答案 S3 反应_type="hydrolysis" 且 EC 3.1.1.31 属酯酶亚类、gold S3 EC 3.1.1 同亚类；S4/S5 无编号可对。"酶名与EC互相矛盾"与"家族相关性当催化证据"两项在本条答案中是否有核验对象，由本人核（答案酶名与EC是否矛盾需官方条目，包内缺卡）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：6个EC官方条目全命中：S2（1.14.13.22）与所写步骤逐字一致；但S1的1.1.1.160官方=dihydrobunolol dehydrogenase（bunolol药物代谢酶）、S3的3.1.1.31官方=6-phosphogluconolactonase（磷酸戊糖途径），底物与所写步骤不同分子；SE19自身UniProt审阅记录（chnA–chnE）的EC集与gold完全同集、其S3官方登记为通配3.1.1.-。两处已核实不对应（按A4同口径）→Y、cap≤4→取3。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-011-D3b / D3b

核查问题：分别核对物种/菌株身份、该菌完成所写单步的证据和整条路径能力；身份真实或单步记录不自动证明指定菌株完成全部步骤。

- 答案具体声称与原文位置：
  - steps[0..4].microorganism（5 处，第56–63、122–129、173–180、229–236、290–297行）：全部为 organism_name="Acinetobacter sp."、strain="SE19"、**ncbi_taxid=null**、organism_profile_id="ORG_001"、confidence="medium"、evidence_id="EVID_001"——即 5 步同绑一个 profile（第3条题面要求"同一菌去重"形态）。
  - organism_profiles[0]（第303–405行）：organism_name="Acinetobacter sp."（第306行）、strain="SE19"（第307行）、ncbi_taxid=null（第308行）；15 项性状见 D4 小节。
  - complete_pathway_organism_profile_id="ORG_001"（第406行）：该菌被声明为完成整条路径（5 步全链）。
  - evidence_registry EVID_001（第419–439行）：INTERNAL_KNOWLEDGE_ONLY，locator 末句"代表菌 Acinetobacter sp. SE19"，claim_scope 含 "microorganism"、无逐 step 微生物分列，confidence="medium"；EVID_002（第440–455行）INTERNAL_KNOWLEDGE_ONLY，claim_scope "organism:ORG_001"+5 项性状。
  - uncertainties[3]（第461行）："菌株性状多依据属级常识与内部知识，未逐项核对原始文献。"

- 核查来源/新证据ID及支持范围：
  - gold/organism_gold.tsv（BIOPATH150_029，22 行）：STEP 级 19 行 + PATHWAY_COMPLETE 12 行。STEP 级中与 SE19 相关：S1 cyclohexanol dehydrogenase—Acinetobacter sp. SE19（organism_match_status=EXACT、taxid=135835、无genome_id）；S3 6-hexanolide hydrolase—SE19（EXACT、135835）；S4 6-hydroxyhexanoate dehydrogenase—SE19（EXACT、135835）；S2 cyclohexanone monooxygenase—Acinetobacter johnsonii（40214，GCA_016027055.1）；S5 6-oxohexanoate dehydrogenase—A. johnsonii 与 Paenarthrobacter ureafaciens（37931）。PATHWAY_COMPLETE 行含 taxid=135835（genome_id 空、pathway_complete=TRUE、download_available=FALSE）等 12 菌。支持范围：gold 登记逐步酶-菌对应与全路径菌名单；不支持范围：gold 非穷举，gold 无某菌不构成反证（P27、P54）。
  - gold 与答案对照（事实）：答案菌株名"Acinetobacter sp. SE19"与 gold normalized 名 EXACT 同字；gold 中 SE19 挂在 S1/S3/S4 三步及 PATHWAY_COMPLETE 名单；gold 的 S2、S5 步另有他菌记录（gold 为多酶/多菌登记制，见 enzyme_gold 同步多行）。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：TAXID 表仅 10 行（183193、226186、28040、294、303、319、336257、351746、390235、471）；**无 TAXID 135835 行**——但答案 ncbi_taxid=null，本答案没有交付可核验的 TaxID 对象（P71 对"凡交付具体编号"才强制核验）。
  - facts/NCBI_TAXONOMY/ 10 张卡无 135835；facts/BACDIVE/ 三张卡（12880=Pseudomonas sp. mt-2 PaW1、13580=Agrobacterium radiobacter DSM 30147、153432=Pseudomonas putida CCUG 49576）无 Acinetobacter 卡。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv 有 "Acinetobacter johnsonii→40214" 与 "Acinetobacter sp. NCIB 9871→40214" 两行，无 SE19 行（且该 crosswalk 属物种名映射，非 SE19 身份卡）。
  - 包内缺口（事实）：无 SE19/135835 的任何分类卡、保藏卡、单步反应级文献卡、全路径能力卡 → 该菌株身份三层（P69 身份定位/反应级/全路径）在包内均无独立证据；gold 侧 EXACT 名单是唯一同向记录。

- 关键事实（供本人判断，非结论）：
  1. 三层声称各有原文对象：身份层=第52–54行+第306–308行（菌名+strain SE19+taxid null）；反应级=每步 microorganism 绑定（5 处）；全路径层=第406行 complete_pathway_organism_profile_id="ORG_001"。
  2. 答案未交付 TaxID（null），故 P67/P71 的 TaxID 三项核验在答案侧无对象；gold 侧 135835 无卡也无 register 行，包内对该 TaxID 本身同样不可核。
  3. 与 gold 的对照（事实）：菌株名与 gold EXACT 同字；gold 把 SE19 登记在 3/5 步与 PATHWAY_COMPLETE 名单（download_available=FALSE）；gold S2/S5 步的酶另有 A. johnsonii 等记录——gold 多行登记是否意味着"同一步多菌均可"属命题口径问题，登记待考，不归责模型。
  4. 答案自身披露：全链只用 INTERNAL_KNOWLEDGE_ONLY 的 EVID_001/EVID_002；EVID_002 自标 confidence="low" 且 locator 写明"属级……归纳"；uncertainties[3] 明示"属级常识、未逐项核对原始文献"；菌株级定量/观测证据零交付。
  5. 量表条款（一句话）：R4/D3b 关键错误清单（P98 表 R4）="物种/菌株或TaxID编造；由基因组存在某酶直接推断完成整条路径；把仅支持单步的菌写成全路径菌"；P69 三层不得互相冒充；P106–P110 身份阶梯（粒度不足/异菌株/无关类群）的适用前提是取得官方核实结论，本条包内无该菌任何官方卡→尚无可套用的核实结论；P27/P54 gold 非穷举、不凭 gold 负覆盖判错。
  6. 包内证据缺口清单：SE19 分类卡、SE19 保藏/文献卡、SE19 反应级证据、SE19 全路径能力证据、TAXID 135835 register 行——均无 → 待联网核查/记 UNRESOLVED。

- 复核结论（保留/修改/仍待核）：保留（RETAIN）
- score_status及分数（NE/NA不猜分）：SCORED，8分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：TaxID 135835现行有效（species级）；Cheng 2000（PMID 10940013）：整菌以环己醇为唯一碳源生长+SE19基因簇（14-kb）在重组E. coli完成环己醇→己二酸；单步（UniProt chnA–chnE五条审阅记录）与全路径（文献）两层独立来源齐→支持充分→取8。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-011-D4 / D4

核查问题：核对实际填写的性状和精确支持范围，区分培养条件与最适值、底物同化/生长与酶活；沿用同物种代表性状口径，不把阴性测试变成阳性。

- 答案具体声称与原文位置：
  - organism_profiles[0]（ORG_001，Acinetobacter sp. SE19，第303–405行）15 项性状逐项登记如下（值 / raw_text / evidence_id / confidence；本答案全部性状 raw_text=null）：
    | 字段 | 值 | evidence_id | confidence | 行号 |
    |---|---|---|---|---|
    | F2_temperature | null | null | unknown | 310–315 |
    | F1_oxygen_tolerance | "好氧" | EVID_002 | medium | 316–321 |
    | F4_salinity | null | null | unknown | 322–327 |
    | F3_pH | null | null | unknown | 328–333 |
    | F5_culture_collection | null | null | unknown | 334–339 |
    | F6_respiration_electron_acceptor | {respiration_mode:"有氧呼吸", terminal_electron_acceptor:"oxygen"} | EVID_002 | medium | 340–348 |
    | F7_carbon_substrate_utilization | "可利用环己醇作为碳源和能源" | EVID_001 | medium | 349–354 |
    | F8_degradation_capacity_broad | "可降解环己醇、环己酮和己内酯等脂环族化合物" | EVID_001 | medium | 355–360 |
    | F9_enzyme_activity | "具有环己醇脱氢酶和环己酮单加氧酶活性" | EVID_001 | medium | 361–366 |
    | F10_motility | null | null | unknown | 367–372 |
    | F11_cell_morphology | "短杆状至球状" | EVID_002 | **low** | 373–378 |
    | F12_gram_cell_envelope | "革兰氏阴性" | EVID_002 | medium | 379–384 |
    | F13_sporulation | "不产芽孢" | EVID_002 | medium | 385–390 |
    | F14_genome_basic | null | null | unknown | 391–396 |
    | F15_habitat_generalism | null | null | unknown | 397–402 |
  - 步级 trait_evidence_id 5 步全为 "EVID_002"（第65、131、182、238、299行）。
  - uncertainties[3]（第461行）："菌株性状多依据属级常识与内部知识，未逐项核对原始文献。"

- 核查来源/新证据ID及支持范围：
  - gold/trait_gold.tsv（case 029，taxid 135835，SE19，STEP scope，15 行）：F1–F13、F15 全部 value_status=UNKNOWN、source_database 空、raw_text 空；仅 F14_genome_basic 有 OBSERVED 行（source_database=NCBI_TAXONOMY、source_field=OrganismTaxID、value=135835、raw_text="TaxID 135835"）。支持范围：gold 在本 case 对 SE19 除 TaxID 外无任何观测性状值；不支持范围：gold UNKNOWN 不是"该性状为假"，只是无冻结观测（P114 允许独立文献/菌株库参与核验）。
  - gold/trait_scoreability_mask.tsv（135835 行，15 行）：F1–F13、F15 observed_value_present=FALSE、scoreable=FALSE、denominator_role=completeness_only；F14 observed_value_present=TRUE、scoreable=TRUE、observed_accuracy。**gold 侧可评分项仅 F14**（答案该项填 null）。
  - gold/trait_subfield_scoreability_mask.tsv（SE19 行）：F2 四子字段、F3 三子字段、F4 五子字段全部 scoreable=FALSE、"no observed source for this sub-field in the frozen local inputs"。
  - evidence/f7_interpretation/F7_INTERPRETATION_NOTES.md（判 F7 前必读，事实摘录）：该目录恢复的是 BacDive 153432 与 12880 两条记录底物面板的测量符号（+/-）与测试类型（assimilation/hydrolysis/fermentation/energy source/reduction）；历史 gold F7 裸名称列表不是阳性碳源清单；硝酸盐还原是还原测试不是碳源同化；酶活/生长/同化须区分；153432 与 12880 两株在 L-arabinose 与 arginine 两项符号相反——面板级不可跨株迁移；37°C 是培养记录不是最适值或上下限。
  - evidence/f7_interpretation/BACDIVE_153432_AND_12880_metabolite_panel.tsv：17 项×2 株的 +/- 与测试类型逐行可查（malate+、adipate-、decanoate+、gluconate+、maltose-、N-acetylglucosamine-、D-mannitol-、D-mannose+、L-arabinose 153432=+/12880=-、D-glucose assimilation+/fermentation-、gelatin-、esculin-、urea-、arginine 153432=-/12880=+、tryptophan-、nitrate-）。
  - 面板与本题的关系（事实）：两张 BacDive 卡均非 Acinetobacter（153432=P. putida CCUG 49576、12880=Pseudomonas sp. mt-2 PaW1），面板 17 项代谢物**不含环己醇/环己酮/己内酯** → 答案 F7/F8/F9 声称对象与面板零交集，面板既不能支持也不能否证本答案 F7。
  - evidence/facts/BACDIVE/bacdive_153432.json support_scope_note：培养温度是"该株培养记录，不是物种最适温度或生长上下限"；本卡不支持把该株性状外推为同物种其他菌株实测性状。
  - 包内无 Acinetobacter 任何事实卡（BACDIVE 3 张卡均为假单胞菌/农杆菌），EVID_001/EVID_002 均为 INTERNAL_KNOWLEDGE_ONLY → 答案 9 项非空性状在包内无外部证据可核。

- 关键事实（供本人判断，非结论）：
  1. gold 侧可评分性（对照表结论）：SE19 的 15 项中 gold 仅 F14 可评分（observed_accuracy），其余 14 项 scoreable=FALSE（completeness_only）；答案 F14 恰好填 null。即答案 9 项非空性状全部落在 gold 侧不可评分区，是否因此走"独立文献/菌株库核验"或"关键缺口"路径由本人按 P114/P113 定。
  2. "阴性测试被写成阳性"是否存在：包内与 SE19 相关的性状证据为零（trait_gold 全 UNKNOWN、无 SE19 事实卡、F7 面板不含该菌也不含其底物）→ **包内不存在可判"阴性被写成阳性"的记录**；该检查项结果=UNRESOLVED/包内无对象（不是"未发现"的同义判定，而是无核对对象）。
  3. 测量原义区分（事实铺垫，适用 P113/P52）：答案 F7 写"可利用环己醇作为碳源和能源"（同化/生长语义）、F8 写"可降解……"（降解能力语义）、F9 写"具有……酶活性"（酶活语义）——三类对象在答案文本内是分开表述的；包内无任何一类的 SE19 实测记录可对照。
  4. 培养条件 vs 最适值：本答案 F2_temperature=null、F3_pH=null、F4_salinity=null，未填任何温度/pH/盐度数值 → 不存在"培养温度被写成最适值"的对象；F7 解释层关于 37°C 培养记录≠最适值的条款在本答案无适用对象。
  5. 证据结构事实：9 项非空性状仅由 2 条 INTERNAL_KNOWLEDGE_ONLY 承载（F7/F8/F9→EVID_001，F1/F6/F11/F12/F13→EVID_002），全部 raw_text=null、无 database/record_id/locator 可定位（EVID_002 在 D5 语义上属 MISSING_SOURCE 类自我声明，P34；此为状态登记事实，非评分）。
  6. 量表条款（一句话）：R5/D4 关键错误清单（P98 表 R5）="预测值冒充观测值；数值离谱到误导筛选；把物种级观测自动推广到所有菌株"——本答案未填任何数值性状（无"数值离谱"对象）；P112 诚实 null 与编造严格区分、缺失扣分主归D1；P114 gold UNKNOWN 时允许独立核验但"未核实的属级常识不能冒充菌株级定量观测"；P115 酶活/单步观测与整菌生长/完整降解能力不得自动外推；P52 同物种代表口径（本答案无代表记录可引）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，5分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：已填性状8项中F7（整菌唯一碳源生长）/F9（chnA/chnB酶记录）/F14（TaxID）命中、F8部分命中（途径覆盖但未逐项列清单）；F1/F6（氧）、F11（形态）、F12（革兰）、F13（芽孢）及保藏号在BacDive/文献可及层全未检出（阴性检索已登记）。命中项真实但未核项挂非空值→P40/P60→取5。（把握度：高）

- 本人人工确认与日期：【待本人签】
