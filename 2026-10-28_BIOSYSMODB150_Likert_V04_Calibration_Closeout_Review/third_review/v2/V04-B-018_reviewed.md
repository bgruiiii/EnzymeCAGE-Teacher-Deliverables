# V04-B-018：定点人工复核

- case：BIOPATH150_021
- 只需核定：D6。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-018-D6 / D6

核查问题：核对原答案置信标签、null/未知和不确定性披露；区分单点过度确信与系统性误导，不因其他维度错误自动封顶，不把重复引用同一断言算多个独立事件。

- 答案具体声称与原文位置：
  - **置信标签分布（全文清点）**：
    - 步级（S1–S4，第13–175行）：enzyme.confidence 4 处全部 "medium"；microorganism.confidence 4 处全部 "high"；4 步的 enzyme/microorganism/reaction_evidence_id 全部绑 EVID_001，trait_evidence_id 全部 "EVID_002"；step.uncertainty 4 处全部 null（第51、90、129、173行）。
    - 性状级（第182–285行）：high 1 项（F12_gram_cell_envelope，第261行）；medium 9 项（F1、F6、F7、F8、F9、F10、F11、F13、F14）；low 2 项（F2_temperature 第192行、F15_habitat_generalism 第283行）；unknown 3 项（F3_pH、F4_salinity、F5_culture_collection，value/evidence_id 全 null）。
    - route_scope.confidence 无此字段；route_scope.notes=null（第10行）。
  - **未知与 null 披露**：性状侧 3 项 null+unknown（F3/F4/F5）；F2 的 minimum_c/maximum_c=null 仅 optimum_c=30（第184–189行）；F14 仅填 accession/size/GC 三值。步级底物/产物、酶、菌无 null 占位。
  - **uncertainties 数组**：空数组 "uncertainties": []（第332行）——全文零条不确定性记录；无 alternative_branches（[]，第294行）、无 downstream_continuation（[]，第293行）；complete_pathway_organism_profile_id="ORG_001"（第288行，单菌完成 4 步全链声明）。
  - **source_type 事实信号**：EVID_001（第296–308行）source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、**locator=null**、claim_scope=["toluene degradation via toluene-cis-diol to 2-hydroxypentadienoate","enzymes TodC1C2BA, TodD, TodE, TodF","Pseudomonas putida F1 as representative organism"]、confidence="medium"；EVID_002（第309–319行）INTERNAL_KNOWLEDGE_ONLY、locator=null、claim_scope=["Pseudomonas putida F1 physiological and genomic traits"]、confidence="low"；EVID_003（第320–330行）source_type="DATABASE_DIRECT"、database="NCBI"、record_id="NC_009512.1"、locator=null、claim_scope=["genome accession, size, GC content of Pseudomonas putida F1"]、confidence="medium"。
  - 证据-声称绑定实例：F14_genome_basic（第269–278行）value={genome_accession:"NC_009512.1", genome_size_bp:5959964, gc_percent:61.9}、evidence_id="EVID_003"、confidence="medium"；F12 革兰氏阴性 confidence="high" 且 evidence_id="EVID_002"（INTERNAL_KNOWLEDGE_ONLY）；F1/F6/F7/F8/F9 等 9 项 medium 均绑 EVID_002。

- 核查来源/新证据ID及支持范围：
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv 第8行：ACCESSION NC_009512.1 = COVERED_BY_FACT_CARD（facts/NCBI_NUCCORE/nuccore_NC_009512.1.json，cases_seen 含 BIOPATH150_021）→ EVID_003 的 record_id 在包内可定位；该行注明"只登记能否定位既有冻结记录；未联网补齐"。
  - facts/NCBI_NUCCORE/nuccore_NC_009512.1.json：record_status=**SUPPRESSED**、record_type=NUCLEOTIDE、names.definition="Pseudomonas putida F1, complete sequence."、organism={source:"Pseudomonas putida F1", taxid:"351746"}；卡内**无 genome size、无 GC% 字段**。支持范围：登录号可定位、其历史对象与 P. putida F1 对应；不支持范围：5959964 bp 与 61.9% 两个数值在卡内无核验对象；卡注明"历史存在不等于当前有效，也不等于虚构"。
  - facts/NCBI_TAXONOMY/taxid_351746.json：scientific_name="Pseudomonas putida F1"、record_status=CURRENT；卡内仅 names 与日期字段，**无 rank、无 lineage 字段**（P71 要求的三项核验中本卡只提供 ScientificName 一项）。支持范围：TaxID 351746↔"Pseudomonas putida F1" 官方对应；不支持范围：不自动支持任何身份/能力声称（卡自带 support_scope_note）。
  - facts/IUBMB_EXPLORENZ/ec_1.14.12.11.json（S1 答案 EC 1.14.12.11）：ACTIVE，reaction="toluene + NADH + H+ + O2 = (1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol + NAD+"；register 第27行 COVERED_BY_FACT_CARD。ec_1.3.1.19.json（S2 答案 EC 1.3.1.19）：ACTIVE，reaction="cis-1,2-dihydrobenzene-1,2-diol + NAD+ = catechol + NADH + H+"。S3 答案 EC 1.13.11.2 与 S4 答案 EC 3.7.1.11：register 第26行/第51行均 OUT_OF_SNAPSHOT_UNRESOLVED、无卡。支持范围：S1/S2 的 EC 官方条目存在且 ACTIVE；不支持范围：EC 卡不自动给 enzyme.confidence="medium" 背书（P72：核验只给事实状态）。
  - facts/BACDIVE/（12880/13580/153432）：无 P. putida F1 菌株卡；153432 为同物种（P. putida，taxid_block 匹配 level=species、NCBI tax id 303）另一保藏号 CCUG 49576 的单株卡，其唯一温度记录为 37°C growth positive（F7 解释层注明该记录不是最适值、不可跨株迁移）→ 答案 F2 optimum_c=30、"专性需氧"、极生鞭毛、不产芽孢、根际栖息等性状在包内无 F1 菌株级事实卡可核。
  - facts/PUBMED/（6501223、2670929）与 EUROPE_PMC/PMC179094：为甲苯降解文献卡，但本答案 evidence_registry 未引用任何文献（EVID_001/002 均无 database/record_id）→ 与本答案无引用关系。

- 关键事实（供本人判断，非结论）：
  1. 置信-证据结构（客观描述）：全答案 4 步化学+酶+菌全部由唯一一条 INTERNAL_KNOWLEDGE_ONLY、locator=null 的 EVID_001 承载（4×medium 酶 + 4×high 菌）；10 项非空性状由 INTERNAL_KNOWLEDGE_ONLY 的 EVID_002 承载（9 medium + 1 high），仅基因组 3 值由带可定位 record_id 的 EVID_003 承载。多处引用指向同一 EVID_001 属"同一断言重复使用"形态（P120：同一根本断言不因此双计为系统性——条款原文供本人对照）。
  2. 披露面（客观清点）：uncertainties=[]、4 处 step.uncertainty=null、route_scope.notes=null、raw_text 全 15 项均 null → 全文零条自由文本不确定性披露；唯一"弱化"信号是 EVID_002 的 registry 级 confidence="low" 与性状级 medium/high 并存（两处标签不一致的客观事实）。
  3. 可定位 vs 不可定位（三态素材，非判定）：可定位=NC_009512.1（卡存在但 SUPPRESSED，数值字段缺失→其中 size/GC 两值 UNRESOLVED）；可部分定位=taxid 351746（卡有 ScientificName、缺 rank/lineage）、EC 1.14.12.11 与 1.3.1.19（卡 ACTIVE）；不可定位=1.13.11.2、3.7.1.11（register OUT_OF_SNAPSHOT）、全部性状值（无 F1 菌株卡、无文献引用）、gene 名 TodC1C2BA/TodD/TodE/TodF（无基因/蛋白卡、无 UniProt 引用）。
  4. 量表条款（一句话）：R7/D6 关键错误清单（P98 表 R7）="把预测/推断系统性写成实证观测；掩盖已知矛盾或主要限制；置信度与证据强度明显不相称"；P119 单点过度确信（个别字段以强证据标签包装未核实内容且零披露）→档内扣，系统性误导→cap候选，两者分开判定；P120 同一编号多步重复引用仍是同一根本断言；P121 D5 的核实结果不自动使 D6 cap，D6 按覆盖范围/是否掩盖矛盾/披露质量独立定档；P45 诚实填写未知可使 D6 得较高分（本答案性状侧 3 项 null+unknown、4 项数值子字段 null 为诚实未知形态；uncertainties 空数组属"可选保留字段"——题面第9条明示该字段不强制填写、留空数组合法）。
  5. "INTERNAL_KNOWLEDGE_ONLY 是登记过的 source_type 枚举值"（题面第5条 evidence.source_type 见 Schema 枚举）→ 答案使用该标签本身是题面允许的申报行为；其与逐条 medium/high 置信的相称性判断权在本人。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，7分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：单点过度确信：uncertainties=[]零披露；S3/S4的EC（1.13.11.2/3.7.1.11）与NC_009512.1的size/GC不可核且未披露→档内取7。（把握度：高）

- 本人人工确认与日期：【待本人签】
