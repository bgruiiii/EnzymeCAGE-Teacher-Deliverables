# V04-B-022：定点人工复核

- case：BIOPATH150_146
- 只需核定：D1、D3b、D5。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-022-D1 / D1

核查问题：核对完整题面、指定路线/终点和实际交付模块；区分路线缺失、格式可用性与科学正确性。说明是否存在使任务符合度主要结论失效的错误。

- 答案具体声称与原文位置：
  - 工程状态（items/V04-B-022/engineering_status.json）：engineering_class=USABLE、finish_reason=stop、machine_readable=true；visible_answer.txt 共 406 行，为单个 JSON 对象，无 markdown 围栏、无对象外文字。
  - route_scope（第6–11行）：oxygen_condition=null（第7行）；chosen_route_name="sulfoquinovose degradation VI"（第8行）；is_single_continuous_route=true（第9行）；notes（第10行）："题面未指定氧条件，oxygen_condition 按题面填 null；路线名按题面原样保留。"
  - route_summary（第12行）："主链按磺基糖酵解型处理：6-sulfo-beta-D-quinovose 先异构化为 6-sulfo-D-fructose，再经 ATP 依赖的 1-磷酸化生成 6-sulfo-D-fructose-1-phosphate；随后醛缩裂解为 glycerone phosphate 与 3-sulfolactaldehyde，3-sulfolactaldehyde 再被还原为 2,3-dihydroxypropane-1-sulfonate。……"
  - steps：共 4 步。S1（第14–52行）：6-sulfo-beta-D-quinovose（main，SMILES 第22行）→ 6-sulfo-D-fructose（main，第28–29行），reaction_type="aldose-ketose isomerization"，enzyme.name="6-sulfo-D-quinovose isomerase"、ec_number="5.3.1.34"（第35–36行），microorganism=Bacteroides thetaiotaomicron VPI-5482 / taxid 226186 / ORG_001。S2（第53–103行）：6-sulfo-D-fructose + ATP（cofactor，smiles=null）→ 6-sulfo-D-fructose-1-phosphate + ADP（cofactor，smiles=null），ec_number="2.7.1.106"（第87行）。S3（第104–149行）：6-sulfo-D-fructose-1-phosphate → glycerone phosphate + 3-sulfolactaldehyde，ec_number="4.1.2.55"（第133行）。S4（第150–190行）：3-sulfolactaldehyde → 2,3-dihydroxypropane-1-sulfonate，reaction_type="reduction"，enzyme.name="3-sulfolactaldehyde reductase"、ec_number=null（第174行）、confidence="low"。每步 substrates/products 成员均含 name+smiles+role；每步均绑定 microorganism（4 步同指 ORG_001）。
  - organism_profiles：仅 1 条 ORG_001（第192–305行）；15 项性状全部出现（第199–303行），每项含 value/raw_text/evidence_id/confidence 四字段外壳；raw_text 全部为 null；value 为 null 的项 F4_salinity、F3_pH（第216–227行）confidence="unknown"。
  - evidence_registry：6 条（EVID_001–EVID_006，第316–400行）；各 step 的 reaction_evidence_id/trait_evidence_id、enzyme.evidence_id、microorganism.evidence_id 均为单个字符串且指向已登记条目。
  - complete_pathway_organism_profile_id="ORG_001"（第307行）；central_metabolism_entry.products=["glycerone phosphate"]（第308–313行）；downstream_continuation=[]、alternative_branches=[]（第314–315行）；uncertainties 4 条（第401–406行，含氧条件、MetaCyc 无 record_id、S4 还原酶 EC 不确定、ATP/ADP 不填 SMILES 的原因）。
  - 全文无 model / model_id / anonymous_model_id 等身份字段。
- 核查来源/新证据ID及支持范围：
  - 题面 question.json（messages[0].content）：任务要求=每步给主底物/主产物英文名+SMILES、一个首选酶及EC、一个对应微生物；同菌去重；15项性状及各项最强来源；route_scope.chosen_route_name 必须原样填写；未知的酶/菌/EC/TaxID/数值一律 null；可选保留字段不评分。支持范围：完整性/格式/任务符合度对照。**题面无任何步数限制注记**（"016仅前3步、006指定4步"为其他 case 的注记，本条题面不存在，已全文核对）。
  - gold/case_root_identity.tsv + formal_cases.tsv（BIOPATH150_146）：路线 BSY-p00985 "sulfoquinovose degradation VI"，root=6-sulfo-beta-D-quinovose，终点=(2S)-3-sulfolactate，LINEAR_UNIQUE、5 步。支持范围：路线步数/终点/化合物序列的核查基线；不支持范围：gold 不是唯一允许答案（P27）。
  - gold/reaction_gold.tsv（18 行）：异构化（S05：6-sulfo-beta-D-quinovose→6-deoxy-6-sulfo-D-fructose）→磷酸化（S01：+ATP→6-deoxy-6-sulfo-D-fructose 1-phosphate +ADP+H+）→醛缩（S03：→(2S)-3-sulfolactaldehyde + glycerone phosphate）→脱氢（S02：+NAD(P)+→(2S)-3-sulfolactate）→转运出胞（S04）。支持范围：逐步化合物序列；不支持范围：不用于判化学对错（D2 归属）。
  - gold/enzyme_gold.tsv：5.3.1.31（sulfoquinovose isomerase）/2.7.1.184（6-deoxy-6-sulfofructose kinase、sulfofructose kinase）/4.1.2.57（6-deoxy-6-sulfofructose-1-phosphate aldolase、sulfofructosephosphate aldolase）/1.2.1.97（3-sulfolactaldehyde dehydrogenase），转运步 ec_number_normalized=NOT_OBSERVED。gold/organism_gold.tsv：步级菌 5 种（E. coli 562、Alkalicoccus urumqiensis 1548213、Bacillus aryabhattai 412384、Pseudomonas putida 303、Clostridium sp. MSTE9 1105031），PATHWAY_COMPLETE=1548213。
- 关键事实（供本人判断，非结论）：
  1. 题面要求逐项对照（事实）：
     - route_scope.chosen_route_name 与题面逐字一致 ✓；oxygen_condition=null 与题面"氧条件: null（未指定）"一致 ✓。
     - 每步主底物+主产物 name+smiles：4 步均交付 ✓；S2 的 ATP/ADP smiles=null 且 uncertainties[3]（第405行）披露原因。
     - 每步首选酶及EC：S1–S3 给出 EC（5.3.1.34 / 2.7.1.106 / 4.1.2.55）；S4 ec_number=null（第174行），uncertainty（第189行）与 uncertainties[2]（第404行）两处披露——按题面规则5"未知的EC一律填 null"的口径交付。
     - 每步对应微生物：4 步均写 microorganism（同指 ORG_001）；题面"同一菌去重"满足（1 条 profile 被复用，题面明文允许复用且明文"不要求整条路径只有一个代表菌"）。
     - 15 项性状：全部出现、按展示顺序排列、每项四字段外壳齐全；完全未知项（F4、F3）按题面补充纪律处理（value=null+confidence=unknown）；raw_text 全 null（题面"没有原文则 null"）。
     - 证据登记：6 条，字段集合齐全；单字符串引用规则满足；内部标识符自洽（EVID_001–006、ORG_001、S1–S4 连续）。
     - 文字字段中文 ✓；无模型身份字段 ✓；无围栏、单对象 ✓。
  2. 与 gold 的路线覆盖差异（事实陈述，对错判定不在此）：答案主链 4 步、止于 2,3-dihydroxypropane-1-sulfonate；gold 5 步、终点 (2S)-3-sulfolactate + 转运出胞。gold 前三个化学转化（异构化/磷酸化/醛缩）与答案 S1–S3 转化逐一对应，但化合物名称写法不同（答案"6-sulfo-D-fructose(-1-phosphate)"，gold"6-deoxy-6-sulfo-D-fructose (1-phosphate)"）；gold 第 4 个化学步是 3-sulfolactaldehyde +NAD(P)+ →(2S)-3-sulfolactate，答案 S4 是同一底物还原为 2,3-dihydroxypropane-1-sulfonate，两侧第 4 步产物不同；答案未设转运步。答案 alternative_branches=[]，route_scope.notes 未声明替代路线、未披露与 gold 的任何冲突（原文见上）。
  3. 量表条款（一句话）：R1 行=D1 档位描述；P13–P15 输出覆盖先登记（路径：已给出；酶：已给出；微生物：已给出；性状：要求15项、填写15项、明确未知2项、遗漏0项；来源：已给出；不确定性：已给出）；P44 要求模块未输出才登记 MISSING（本条各模块均有输出）；P45 诚实 null 归 D1 完成度不足；P98 表 R1 关键错误="核心任务模块大部缺失；严重偏离指定路线/条件；输出损坏且科学内容也无法辨认"；P100 任务参数偏离（更换指定路线名、更改氧条件）属 D1 关键错误判定范畴——本答案两项 route_scope 参数均按题面填写（事实陈述，是否构成偏离由本人判定）；P29 题面未写具体终点化合物（终点信息在 gold/case_root_identity）。
  4. 包内证据缺口：无——完整性对照所需题面与 gold 均在包内；本维不需要新证据。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，4分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：交付链终点DHPS与gold路线VI终点sulfolactate不同、未声明替代→P100关键错误（本人原则A1）→cap≤4；4步/15性状/6证据交付完整，档内取4。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-022-D3b / D3b

核查问题：分别核对物种/菌株身份、该菌完成所写单步的证据和整条路径能力；身份真实或单步记录不自动证明指定菌株完成全部步骤。

- 答案具体声称与原文位置：
  - 三层声称（P69）在本答案的原文定位：
    - 身份层：steps S1–S4 microorganism（第41–48、92–99、138–145、179–186行）+ organism_profiles[0]（第193–197行）：organism_name="Bacteroides thetaiotaomicron"、strain="VPI-5482"、ncbi_taxid=226186、organism_profile_id="ORG_001"。
    - 反应级层：4 个 step 各自把该菌绑定到本步反应，S1–S3 evidence_id="EVID_001"（第47、98、144行），S4 evidence_id="EVID_002"（第185行）；microorganism.confidence：S1–S3 "medium"、S4 "medium"。
    - 完整路径层：complete_pathway_organism_profile_id="ORG_001"（第307行）——同一 profile 被声明为完成整条路径的菌。
  - evidence_registry：EVID_001（第317–330行）DATABASE_DIRECT/MetaCyc/record_id=null/locator="Pathway name: sulfoquinovose degradation VI"/claim_scope 含"route-organism association"；EVID_002（第331–343行）INTERNAL_KNOWLEDGE_ONLY/locator="Bacteroides thetaiotaomicron VPI-5482 sulfoquinovose utilization with formation of 2,3-dihydroxypropane-1-sulfonate; bibliographic record not supplied"/claim_scope 含"route-organism association"/confidence="low"。EVID_003（NCBI Taxonomy 226186，claim_scope 含"organism identity"）由 F15 性状引用（第301行），未直接挂到 step.microorganism。
  - 15 项性状全挂在 ORG_001 名下（第199–303行），性状来源 EVID_004/006/001/005/003。
- 核查来源/新证据ID及支持范围：
  - facts/NCBI_TAXONOMY/taxid_226186.json：record_status=CURRENT，names.scientific_name="Bacteroides thetaiotaomicron VPI-5482"，other_names=[]，**卡内无 rank、lineage 字段**（names 仅 scientific_name+other_names 两键）。支持范围：TaxID 226186 与该学名（含菌株词 VPI-5482）的官方配对；不支持范围：无 rank/lineage 可核（P67 三项中两项包内无对象），不自动支持任何能力声称。
  - facts/NCBI_NUCCORE/nuccore_NC_004663.1.json：record_status=CURRENT，definition="Bacteroides thetaiotaomicron VPI-5482, complete sequence."，organism 字段含 taxid="226186" 与 lineage 文本"Bacteria; Pseudomonadati; Bacteroidota; Bacteroidia; Bacteroidales; Bacteroidaceae; Bacteroides."。支持范围：该基因组记录属于 taxid 226186 的 B. thetaiotaomicron VPI-5482（间接提供 lineage 上下文）；不支持范围：不证明该菌催化任何反应。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：TAXID 226186 → COVERED_BY_FACT_CARD（cases_seen=BIOPATH150_146）。支持范围：仅登记"能定位冻结记录"这一事实。
  - gold/organism_gold.tsv（BIOPATH150_146）：步级 13 行、菌 5 种（Escherichia coli 562、Alkalicoccus urumqiensis 1548213、Bacillus aryabhattai 412384、Pseudomonas putida 303、Clostridium sp. MSTE9 1105031）；PATHWAY_COMPLETE 行 taxid=1548213、genome_id=GCA_002993335.1。支持范围：gold 登记的逐步酶-菌对应与全路径菌参照；不支持范围：gold 非穷举（P27/P54），gold 无某菌不构成反证。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv（12 行）：无 Bacteroides 相关条目 → 别名核对无支持。
  - facts/ 其余卡（BACDIVE 12880/13580/153432、PUBMED 6501223/2670929、EUROPE_PMC PMC179094、UNIPROT P12994/P22643）：对象分别为 Pseudomonas sp. mt-2、Agrobacterium radiobacter、甲苯/对枯烯文献、E. coli YbhB、Xanthobacter 脱卤酶——与本答案菌及本 case 无对应关系。
- 关键事实（供本人判断，非结论）：
  1. 身份层核验状态（事实）：TaxID 226186 有官方卡、scientific_name 与答案菌名+菌株词逐字一致（"Bacteroides thetaiotaomicron VPI-5482"）；P67 要求的 ScientificName/rank/lineage 三项中，rank 与 lineage 在 taxonomy 卡内无字段（nuccore 卡另有 lineage 文本可参照）；strain="VPI-5482" 与卡内菌株词一致。粒度=菌株级 TaxID（226186 在 NCBI 中即 VPI-5482 型菌株记录——卡内学名含菌株词这一事实）。
  2. 反应级核验状态（事实）：答案把该菌绑定到 4 个反应步，所引 EVID_001 在包内无可定位条目（MetaCyc、record_id=null，见 D5 小节），EVID_002 自标 INTERNAL_KNOWLEDGE_ONLY 且明写"bibliographic record not supplied"；包内无任何 B. thetaiotaomicron 的单步催化证据卡（facts 全树无该菌文献/菌株/蛋白卡）。→ 反应级能力声称在包内无支持证据（记待核/UNRESOLVED 的材料齐备，定性留本人）。
  3. 完整路径层核验状态（事实）：complete_pathway_organism_profile_id="ORG_001"；包内无该菌整条路径能力证据；gold PATHWAY_COMPLETE 指向 Alkalicoccus urumqiensis（1548213）；答案菌与 gold 步级菌 5 种交集为空（gold 非穷举，此差异不判对错）。
  4. 与 gold 对照（事实）：gold 步级菌与本答案菌无重叠；答案菌 confidence 为 medium/low；EVID_002 confidence="low"。
  5. 量表条款（一句话）：R4 关键错误清单（P98 表 R4）="物种/菌株或TaxID编造；由基因组存在某酶直接推断完成整条路径；把仅支持单步的菌写成全路径菌"——本条 TaxID 有官方卡、非编造形态（事实铺垫）；P69 三层声称分别核对；P71–P72 编号核验只给事实状态；P106–P110 身份阶梯（粒度不足/异菌株/无关类群）适用前提是先取得官方核实结论，本条身份层有官方学名支持、rank/lineage 字段缺卡（尚不能完整走完 P67 三项核验，事实铺垫）；P72 核验不自动给分或cap。
  6. 包内证据缺口清单：taxid_226186 卡缺 rank/lineage 字段；无 B. thetaiotaomicron 任何反应级证据卡；无该菌整条路径能力证据卡；无该菌性状来源卡（ATCC 29148 无卡，见 D5）；crosswalk 无该菌别名行——均待联网核查/记 UNRESOLVED。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，4分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：同B005-D3b：身份/保藏层命中（TaxID 226186、ATCC 29148型菌株），能力层PubMed题录零命中、全文层无该菌SQ降解研究、群落研究归因E. coli→未证实登记取4。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-022-D5 / D5

核查问题：逐一比对原答案的引用与claim_scope，区分可定位、笼统、缺失、待核和已核实错引；LOCAL不自动封顶，关键错引需说明主要结论如何失效。新增证据不能回填原引用。

六状态定义原文摘录（量表 P34–P40，供本人对照）：
- P34 MISSING_SOURCE：完全无引用，或仅有INTERNAL_KNOWLEDGE_ONLY类自我声明。D5按低分档评定；这是缺失而非误导，默认不触发关键错误cap。
- P35 GENERIC_SOURCE：只有笼统库名/模型名/文献列表，无法定位到条目。"通常评3–4档"仅适用于决策相关组（DECISION_RELEVANT：预定义表CORE与APPLICATION_CRITICAL组）全部仅有笼统来源的情形；……只有当笼统来源使D5主要结论完全不可追查、且评分者写明主要结论失效依据时，才作为cap候选。
- P36 VERIFIED_MIS_CITATION_LOCAL：经统一冻结证据核实，引用不存在或引用存在但不支持所声称结论，且按任务级claim group关键性预定义表（R2任务条件式）与逐题CASE_CLAIM_GROUP_SCOPE登记：错引落在SUPPORTING组，或落在APPLICATION_CRITICAL组但任务条件不成立、或虽成立而未实际推翻目标筛选/适用性结论，不影响该维度主要结论。正常档位内扣分，不自动cap；错误数量与影响决定档内分。
- P37 VERIFIED_MIS_CITATION_CRITICAL：经核实错引落在CORE组（核心路径/路线条件、关键酶-反应对应、核心菌株身份等）且实际推翻相应主要结论，或落在APPLICATION_CRITICAL组、该题任务条件成立（按CASE_CLAIM_GROUP_SCOPE登记）且实际推翻目标筛选/适用性结论。触发D5关键错误，cap≤4；cap档内取分按其余证据质量。关键组身份不自动等于封顶：必须核实且使相关主要结论失效。
- P38 VERIFIED_MIS_CITATION_SYSTEMIC：多项错引、系统性虚构、主要证据链失效或严重误导筛选/应用决策。触发D5关键错误，cap≤4。
- P40 UNRESOLVED_SOURCE：引用可疑但当前冻结证据无法核实（查不到、接口失败、记录粒度不足或历史状态复杂）。保留低分与待核标记；不得冒充已证实错引，不计入已核实关键错误，不触发cap。

- 答案具体声称与原文位置（evidence_registry 6 条逐项，visible_answer.txt 第316–400行）：
  1. EVID_001（第317–330行）：source_type="DATABASE_DIRECT"、database="MetaCyc"、record_id=null、locator="Pathway name: sulfoquinovose degradation VI"、claim_scope=["chosen route name","main reaction sequence","sulfosugar intermediates","route-organism association"]、confidence="medium"。消费方：S1–S3 的 enzyme/microorganism/reaction（第39、47、49–50行等）、F7（第249行）、F9（第261行）。
  2. EVID_002（第331–343行）：source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator="Bacteroides thetaiotaomicron VPI-5482 sulfoquinovose utilization with formation of 2,3-dihydroxypropane-1-sulfonate; bibliographic record not supplied"、claim_scope=["3-sulfolactaldehyde reduction","2,3-dihydroxypropane-1-sulfonate formation","route-organism association"]、confidence="low"。消费方：S4 enzyme/microorganism/reaction（第177、185、187行）。
  3. EVID_003（第344–356行）：source_type="DATABASE_DIRECT"、database="NCBI Taxonomy"、record_id="226186"、locator="Bacteroides thetaiotaomicron VPI-5482"、claim_scope=["organism identity","ncbi_taxid","habitat context"]、confidence="high"。消费方：F15_habitat_generalism（第301行）。
  4. EVID_004（第357–369行）：source_type="DATABASE_DIRECT"、database="ATCC"、record_id="29148"、locator="Bacteroides thetaiotaomicron VPI-5482"、claim_scope=["culture collection accession","growth temperature context","anaerobic culture context"]、confidence="high"。消费方：F2_temperature（第207行）、F5_culture_collection（第234行）。
  5. EVID_005（第370–382行）：source_type="DATABASE_DIRECT"、database="NCBI RefSeq"、record_id="NC_004663.1"、locator="Bacteroides thetaiotaomicron VPI-5482 complete genome"、claim_scope=["genome accession","genome size","GC percent"]、confidence="high"。消费方：F14_genome_basic（第295行）。
  6. EVID_006（第383–399行）：source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator="General phenotypic description of Bacteroides thetaiotaomicron VPI-5482; no primary excerpt supplied"、claim_scope=["oxygen tolerance","respiration mode","motility","cell morphology","Gram cell envelope","sporulation","broad polysaccharide degradation capacity"]、confidence="medium"。消费方：F1/F6/F8/F10/F11/F12/F13（第213、243、255、267、273、279、285行）。
- 核查来源/新证据ID及支持范围（逐条写明"支持什么/不支持什么"，所需事实是否齐备；定性均留本人）：
  1. EVID_001（MetaCyc）：包内 facts/ 无 MetaCyc 库任何卡；覆盖登记册 identifier_type 仅 ACCESSION/CULTURE/EC/TAXID/UNIPROT_ACC 五类，无 pathway 名条目，无本条对应行。→ 引用对象（MetaCyc 条目）包内不可定位；locator 仅路线名文字、record_id=null。claim_scope 声称支持"main reaction sequence / sulfosugar intermediates / route-organism association"，其内容核验所需事实包内齐缺 → 待核（UNRESOLVED_SOURCE 所需事实形态）。gold 侧有同路线名基线（case_root_identity：sulfoquinovose degradation VI），但 gold 不是被引来源、不能回填（P51）。
  2. EVID_002：source_type=INTERNAL_KNOWLEDGE_ONLY 且明写"bibliographic record not supplied" → P34 定义形态完全吻合（事实）；无包内核验对象。
  3. EVID_003（NCBI Taxonomy 226186）：facts/NCBI_TAXONOMY/taxid_226186.json 存在，scientific_name 与 locator 逐字一致，record_status=CURRENT，登记 COVERED_BY_FACT_CARD → 引用可定位、身份类声称可核；claim_scope 第三项"habitat context"在卡内无对应字段（卡仅学名+别名）→ 该子声称包内不可核。事实=条目可定位且身份部分相符；"habitat context"部分支持范围不足。
  4. EVID_004（ATCC 29148）：覆盖登记册 CULTURE 类无 29148 行（CULTURE 仅 ATCC 33015/43050/700007）；facts/ 无 ATCC 或 BACDIVE 卡涉及 B. thetaiotaomicron → 引用对象包内不可定位 → 待核；claim_scope 的 accession/温度/厌氧培养三项核验所需事实包内齐缺。
  5. EVID_005（NCBI RefSeq NC_004663.1）：facts/NCBI_NUCCORE/nuccore_NC_004663.1.json 存在，definition="Bacteroides thetaiotaomicron VPI-5482, complete sequence."，record_status=CURRENT，登记 COVERED_BY_FACT_CARD → accession 可定位、"genome accession"子声称可核且相符；claim_scope 的"genome size / GC percent"在卡内无字段（卡仅 definition/organism/状态/日期）→ 该两项包内不可核（答案 F14 给 6,260,361 bp、42.8%，第291–292行，卡内无对照事实）。事实=条目存在且属该菌；数值子声称支持范围不足。
  6. EVID_006：INTERNAL_KNOWLEDGE_ONLY 且 locator 明写"no primary excerpt supplied" → P34 定义形态吻合（事实）；7 项性状声称无包内核验对象。
- 关键事实（供本人判断，非结论）：
  1. 6 条引用中：2 条为 INTERNAL_KNOWLEDGE_ONLY（EVID_002/006，P34 形态）；2 条包内可定位且对象匹配（EVID_003 taxid 卡、EVID_005 nuccore 卡，但两者 claim_scope 均含卡内无字段的子声称）；2 条包内不可定位（EVID_001 MetaCyc、EVID_004 ATCC 29148，均无登记行、无事实卡 → P40 UNRESOLVED 形态；EVID_001 同具 P35"笼统"特征：record_id=null、locator 仅文字）。各条最终归入哪一状态由本人判定。
  2. 任务级关键性预定义（rubric/CASE_CLAIM_GROUP_SCOPE.tsv，BIOPATH150_146 5 行）：CG04 氧条件/F2 温度/pH/盐度均 SUPPORTING（题面未限定）；CG14 底物利用=CLAIM_CONDITIONAL。登记表未逐行列 CORE 组；酶-反应/路线/菌株身份属 CORE 的口径见 P37 括号内定义。判定所需输入已在包内。
  3. 答案自披露：uncertainties[1]（第403行）"MetaCyc 证据仅能以路线名作为 locator，未提供可核验 record_id"——与 EVID_001 状态一致（D6 归属，不在此评）。
  4. "已核实错引"判定所需事实齐备性：本条 6 项引用中，包内不存在任何一张与被引对象矛盾的事实卡（无 MetaCyc 卡、无 ATCC 29148 卡、无 B. thetaiotaomicron 文献卡），故"引用存在但不支持结论"形态的核实（P36/P37）在本条没有可依据的矛盾事实；可定位的 2 条为正向相符。事实陈述：包内证据形态不足以坐实任何一条已核实错引，也不足以排除（UNRESOLVED 保留）。
  5. 量表条款（一句话）：P39 严重度判定纪律（按预定义表逐组处理、同一单元多处错引只 cap 一次）；P41 claim-level 登记与合成规则（逐组列明、不压成单一标签）；P51 冻结快照、查不到记 UNRESOLVED 不判虚构；P52 同物种代表记录口径（本条未涉及）；R6 行 D5 关键错误定义。步骤/性状的 D3b/D4 后果分别归各自维度独立判定（P24）。
  6. 包内证据缺口：MetaCyc sulfoquinovose degradation VI 条目卡、ATCC 29148 保藏记录卡、B. thetaiotaomicron VPI-5482 表型文献卡、NCBI Taxonomy 226186 卡的 rank/lineage 字段、NC_004663.1 的 size/GC 数值字段——均无覆盖，待联网核查。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，4分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：6条引用中2条不可定位（MetaCyc条目/ATCC 29148）、2条INTERNAL、2条可定位相符但claim_scope超卡内字段；包内无矛盾卡，不足以坐实已核实错引→P40 UNRESOLVED保留低分+待核，不cap，档内取4。（把握度：高）

- 本人人工确认与日期：【待本人签】
