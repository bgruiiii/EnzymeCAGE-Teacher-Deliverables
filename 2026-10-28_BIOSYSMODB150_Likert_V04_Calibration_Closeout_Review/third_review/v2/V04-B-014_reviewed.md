# V04-B-014：定点人工复核

- case：BIOPATH150_020
- 只需核定：D5。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-014-D5 / D5

核查问题：逐一比对原答案的引用与claim_scope，区分可定位、笼统、缺失、待核和已核实错引；LOCAL不自动封顶，关键错引需说明主要结论如何失效。新增证据不能回填原引用。

六状态定义原文摘录（量表 P34–P40，供本人对照）：
- P34 MISSING_SOURCE：完全无引用，或仅有INTERNAL_KNOWLEDGE_ONLY类自我声明。D5按低分档评定；这是缺失而非误导，默认不触发关键错误cap。
- P35 GENERIC_SOURCE：只有笼统库名/模型名/文献列表，无法定位到条目。"通常评3–4档"仅适用于决策相关组（DECISION_RELEVANT：预定义表CORE与APPLICATION_CRITICAL组）全部仅有笼统来源的情形；……只有当笼统来源使D5主要结论完全不可追查、且评分者写明主要结论失效依据时，才作为cap候选。
- P36 VERIFIED_MIS_CITATION_LOCAL：经统一冻结证据核实，引用不存在或引用存在但不支持所声称结论，且按任务级claim group关键性预定义表（R2任务条件式）与逐题CASE_CLAIM_GROUP_SCOPE登记：错引落在SUPPORTING组，或落在APPLICATION_CRITICAL组但任务条件不成立、或虽成立而未实际推翻目标筛选/适用性结论，不影响该维度主要结论。正常档位内扣分，不自动cap；错误数量与影响决定档内分。
- P37 VERIFIED_MIS_CITATION_CRITICAL：经核实错引落在CORE组（核心路径/路线条件、关键酶-反应对应、核心菌株身份等）且实际推翻相应主要结论，或落在APPLICATION_CRITICAL组、该题任务条件成立（按CASE_CLAIM_GROUP_SCOPE登记）且实际推翻目标筛选/适用性结论。触发D5关键错误，cap≤4；cap档内取分按其余证据质量。关键组身份不自动等于封顶：必须核实且使相关主要结论失效。
- P38 VERIFIED_MIS_CITATION_SYSTEMIC：多项错引、系统性虚构、主要证据链失效或严重误导筛选/应用决策。触发D5关键错误，cap≤4。
- P40 UNRESOLVED_SOURCE：引用可疑但当前冻结证据无法核实（查不到、接口失败、记录粒度不足或历史状态复杂）。保留低分与待核标记；不得冒充已证实错引，不计入已核实关键错误，不触发cap。（P40 末段：科学错误已由官方证据核实、但所引来源与该断言的引用-声称链尚未核实时：相应科学维度按已核实科学错误处理，D5保持UNRESOLVED_SOURCE待核、不cap。）

- 答案具体声称与原文位置（evidence_registry 7 条逐项，visible_answer.txt 第254–347行；工程状态 engineering_status.json：engineering_class=USABLE、machine_readable=true）：
  1. EVID_001（第256–267行）：source_type="DATABASE_DIRECT"、database="KEGG PATHWAY"、record_id="map00623"、locator="Toluene degradation; methyl side-chain oxidation branch to benzoate"、claim_scope=["route_scope","reaction_order","substrate_product"]、confidence="high"。消费方：S1–S3 的 reaction_evidence_id（第49、90、131行）。
  2. EVID_002（第269–279行）：source_type="DATABASE_DIRECT"、database="KEGG ENZYME"、record_id="1.1.1.90"、locator="aryl-alcohol dehydrogenase; TOL upper pathway xylB"、claim_scope=["enzyme","reaction"]、confidence="high"。消费方：S2 enzyme（第80行）。
  3. EVID_003（第281–291行）：source_type="DATABASE_DIRECT"、database="KEGG ENZYME"、record_id="1.2.1.28"、locator="benzaldehyde dehydrogenase (NAD+); TOL upper pathway xylC"、claim_scope=["enzyme","reaction"]、confidence="high"。消费方：S3 enzyme（第121行）。
  4. EVID_004（第293–303行）：source_type="DATABASE_DIRECT"、database="KEGG ENZYME"、record_id="1.14.15.28"、locator="xylene monooxygenase; TOL upper pathway xylMA"、claim_scope=["enzyme","reaction"]、confidence="medium"。消费方：S1 enzyme（第39行）。
  5. EVID_005（第305–318行）：source_type="DATABASE_DIRECT"、database="GenBank"、record_id="AJ344068"、locator="Pseudomonas putida plasmid pWW0 complete sequence; xyl upper-pathway genes"、claim_scope=["organism-pathway association","gene_or_protein","F7_carbon_substrate_utilization","F8_degradation_capacity_broad","F9_enzyme_activity"]、confidence="high"。消费方：S1–S3 microorganism（evidence_id 第47、88、129行）、F7（第193行）、F8（第199行）、F9（第205行）。
  6. EVID_006（第320–335行）：source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null、claim_scope=["F1_oxygen_tolerance","F6_respiration_electron_acceptor","F10_motility","F11_cell_morphology","F12_gram_cell_envelope","F13_sporulation","F15_habitat_generalism"]、confidence="medium"。消费方：F1（第157行）、F6（第187行）、F10（第211行）、F11（第217行）、F12（第223行）、F13（第229行）、F15（第241行）。
  7. EVID_007（第337–347行）：source_type="DATABASE_DIRECT"、database="ATCC"、record_id="33015"、locator="Pseudomonas putida mt-2"、claim_scope=["F5_culture_collection","F2_temperature"]、confidence="medium"。消费方：F2（第151行）、F5（第178行）。
- 核查来源/新证据ID及支持范围（逐条写明"支持什么/不支持什么"；定性均留本人）：
  1. EVID_001（KEGG PATHWAY map00623）：facts/ 无 KEGG 库任何卡；覆盖登记册 identifier_type 仅 ACCESSION/CULTURE/EC/TAXID/UNIPROT_ACC，无 pathway 类行 → 引用条目包内不可定位 → 待核（UNRESOLVED 形态）。gold 侧有同路线基线（case_root_identity：Toluene degradation to benzoate，3 步，Toluene→Benzoate），但 gold 不是被引来源、不能回填（P51）。
  2. EVID_002（KEGG ENZYME 1.1.1.90）：facts/IUBMB_EXPLORENZ/ 20 张 EC 卡中无 1.1.1.90；登记册 EC 1.1.1.90 → OUT_OF_SNAPSHOT_UNRESOLVED（cases_seen=BIOPATH150_016;BIOPATH150_020）→ 条目内容包内不可核 → 待核。gold/enzyme_gold.tsv S02 行登记 benzyl alcohol dehydrogenase EC 1.1.1.90——EC 号与 gold 一致，但被引来源（KEGG ENZYME 条目）本身不可核，gold 只能作旁证不能替代被引来源（P51）。
  3. EVID_003（KEGG ENZYME 1.2.1.28）：包内无 1.2.1.28 卡；登记册 EC 1.2.1.28 → OUT_OF_SNAPSHOT_UNRESOLVED（cases_seen=BIOPATH150_016;BIOPATH150_020）→ 待核。gold S03 登记 benzaldehyde dehydrogenase EC 1.2.1.28（另有 1.2.1.64/1.2.1.29 变体行）——同上，EC 号与 gold 一致、被引条目不可核。
  4. EVID_004（KEGG ENZYME 1.14.15.28）：**facts/IUBMB_EXPLORENZ/ec_1.14.15.28.json 存在**（登记册 EC 1.14.15.28 → COVERED_BY_FACT_CARD）：record_status=ACTIVE，accepted_name="cholest-4-en-3-one 26-monooxygenase [(25R)-3-oxocholest-4-en-26-oate forming]"，other_names=["CYP142"]，reaction=胆甾-4-烯-3-酮侧链氧化（生成 (25R)-3-oxocholest-4-en-26-oate），replacement_history="created 1.14.15.28 2016 as EC 1.14.13.221, transferred 2018 to EC 1.14.15.28"。→ 被引编号的官方条目在包内可定位；其 accepted name/reaction 与答案 locator 及 S1 所声称的"xylene monooxygenase / 甲苯甲基氧化"无对应（官方条目内容为甾体底物氧化）。"引用存在但不支持所声称酶-反应对应"这一判定所需的对照事实在包内齐备；是否登记为 VERIFIED_MIS_CITATION 及严重度（claim group 归属：S1 酶-反应对应按 P37 属 CORE 组形态）由本人判定。参照事实：gold S01 登记两套酶——toluene methyl-monooxygenase EC 1.14.15.26（包内 ec_1.14.15.26.json：accepted_name="toluene methyl-monooxygenase"，reaction 第(1)条 toluene + O2 → benzyl alcohol，ACTIVE）与 xylene monooxygenase EC 1.14.13.-（通配，包内无卡）；官方 1.14.15.26 卡支持答案所写反应，但答案引用的编号是 1.14.15.28（P66：官方条目优先；P73：历史撤转编号不等于虚构）。答案 S1 uncertainty（第51行）与 uncertainties[0]（第350行）自行披露"EC 按复合酶条目填写；若按电子供体或组分拆分，个别数据库表述可能不同"。
  5. EVID_005（GenBank AJ344068）：facts/NCBI_NUCCORE/nuccore_AJ344068.json 存在（登记册 ACCESSION AJ344068 → COVERED_BY_FACT_CARD）：record_status=CURRENT，definition="Pseudomonas putida plasmid pWW0 complete genome."，organism="Pseudomonas putida"（taxid 303）。→ accession 可定位、pWW0 质粒记录存在且属 P. putida；答案 locator 写"complete sequence; xyl upper-pathway genes"，卡 definition 为"complete genome"，卡内无基因注释字段 → "gene_or_protein"及 F7/F8/F9 性状子声称的支持内容包内不可核（支持范围不足的事实；是否构成超出被引记录内容的引用由本人判定）。"organism-pathway association"子声称：卡仅证明记录存在与物种归属，不含该菌完成该路径的信息（P69 层级区分）。
  6. EVID_006：source_type=INTERNAL_KNOWLEDGE_ONLY 且 locator=null → P34 定义形态完全吻合（事实）；7 项性状声称无包内核验对象。
  7. EVID_007（ATCC 33015）：登记册 CULTURE ATCC 33015 → COVERED_BY_FACT_CARD facts/BACDIVE/bacdive_12880.json：species="Pseudomonas putida"、strain_designation="mt-2 PaW1, pWWO"、culture_collection_numbers 含"ATCC 33015"（同卡含 DSM 3931、NCIB 12182、CCUG 2480、ATCC 23973、JCM 6156、BCRC 10460）、culture_temperature_records=[{growth:positive,26°C},{growth:positive,30°C}]、ncbi_taxid_block 303（Matching level: species）、type_strain="no"。→ F5_culture_collection 子声称可定位支持（33015 在该株保藏号集合内）；F2_temperature：卡有 30°C growth 记录、答案 optimum_c=30——卡字段语义为"growth 记录"，P52 明文"培养温度不等于最适值"（事实铺垫，"optimum"标签与记录语义的关系由本人判定）。另注：答案标 database="ATCC"，包内实际提供对照的是 BACDIVE 菌株记录卡（被引 ATCC 条目本身包内无卡）。
- 关键事实（供本人判断，非结论）：
  1. 7 条引用构成（事实）：1 条 INTERNAL_KNOWLEDGE_ONLY（EVID_006，P34 形态）；3 条 KEGG（EVID_001/002/003）包内均不可定位 → 待核；1 条 EC 编号包内有官方卡且官方内容与所声称酶-反应不对应（EVID_004，判定材料齐备，定性留本人）；2 条包内可定位（EVID_005 nuccore 卡、EVID_007 经 BACDIVE 卡间接支持），各自 claim_scope 中部分子声称可核、部分卡内无字段。
  2. 任务级关键性预定义（rubric/CASE_CLAIM_GROUP_SCOPE.tsv，BIOPATH150_020 6 行）：CG04 氧与氧化还原条件（题面 aerobic）→ condition_met=TRUE、active_criticality=APPLICATION_CRITICAL；CG10 性状氧需求 → APPLICATION_CRITICAL；CG11 温度/CG12 pH/CG13 盐度 → SUPPORTING；CG14 底物利用谱 → CLAIM_CONDITIONAL。酶-反应/路线/菌株身份属 CORE 的口径见 P37 括号内定义。判定所需输入已在包内。
  3. 答案自身披露与引用状态的关系（事实）：S1 uncertainty 与 uncertainties[0] 已披露 EC 表述可能因数据库而异；microorganism 字段 ncbi_taxid 全为 null（第44、85、126行）→ 无 TaxID 引用可核；F14_genome_basic 整项 value=null（第232–237行）→ 无基因组引用可核；uncertainties[1]（第351行）披露"染色体级基因组 accession 未填写"。
  4. "已核实错引"所需事实齐备性（事实陈述）：EVID_004 一条存在官方卡且内容不对应的完整对照；其余条目为不可定位（3 条 KEGG、1 条 INTERNAL、2 条部分可定位）——包内证据形态仅支持对 EVID_004 做错引核实，对不可定位条目按 P40/P51 记 UNRESOLVED 待核、不判虚构。
  5. 量表条款（一句话）：P39 严重度判定纪律（按预定义表逐组处理、不看答案倒推分组、同一单元多处错引只 cap 一次）；P41 逐 claim group 登记状态集合、SUPPORTING 不得跨档上调；P51 冻结快照、查不到记 UNRESOLVED；P56 单条链接失效不等于虚构、核验后才标虚构；P66 gold 单值与答案具体号冲突时官方条目优先；P73 历史撤转编号不判虚构；R6 行 D5 关键错误定义；D5 与 D3a/D6 的分轴见 P136（EC 错配本身属 D3a 层，引用-声称链属 D5 层，共用同一 ROOT_ERROR_EVENT_ID 不双计）。
  6. 包内证据缺口：KEGG PATHWAY map00623 条目卡、KEGG ENZYME 1.1.1.90/1.2.1.28/1.14.15.28 条目卡（其中 1.14.15.28 已由 IUBMB 官方卡替代核验）、ATCC 33015 原始条目卡（现由 BACDIVE 12880 卡覆盖）、AJ344068 的基因注释内容——均无直接覆盖；缺口内事项待联网核查/记 UNRESOLVED。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：EVID_004引EC 1.14.15.28，官方卡accepted name=胆固醇26-单加氧酶（CYP142），与所声称xylene monooxygenase不对应→已核实错引落在关键酶-反应对应（R6 VERIFIED_MIS_CITATION_CRITICAL）→cap≤4；其余引用3条KEGG不可定位（P40不cap），档内取3。（把握度：高）

- 本人人工确认与日期：【待本人签】
