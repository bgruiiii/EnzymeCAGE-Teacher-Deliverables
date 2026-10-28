# V04-B-005：定点人工复核

- case：BIOPATH150_146
- 只需核定：D2、D3a、D3b、D6。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-005-D2 / D2

核查问题：逐步核对主底物到主产物的化学转化、方向和连续性。若可能是替代路线，先分清任务符合度与所写反应本身是否成立；检索无结果不等于反应不可能。

- 答案具体声称与原文位置：
  - route_summary（visible_answer.txt 第12行）："6-sulfo-beta-D-quinovose 经 sulfoquinovose degradation VI 途径被 Bacteroides thetaiotaomicron VPI-5482 降解：首先氧化为 6-sulfo-D-gluconolactone，水解为 6-sulfo-D-gluconate，脱水生成 2-dehydro-3-deoxy-6-sulfo-D-gluconate，醛缩裂解为 pyruvate 和 3-sulfolactaldehyde，后者氧化为 3-sulfolactate，最后脱磺酸生成 pyruvate 和 sulfite。"
  - route_scope（第6–11行）：chosen_route_name="sulfoquinovose degradation VI"（第8行，与题面给定名称逐字一致）、oxygen_condition=null（第7行）、is_single_continuous_route=null（第9行）、notes=null（第10行）→ 答案未写任何"替代路线/范围边界"文字。
  - steps S1–S6（第13–257行），主底物/主产物/反应类型逐条：
    - S1（第14–52行）6-sulfo-beta-D-quinovose "O[C@@H]1O[C@H](CS(=O)(=O)O)[C@@H](O)[C@H](O)[C@H]1O" → 6-sulfo-D-gluconolactone "O=C1O[C@H](CS(=O)(=O)O)[C@@H](O)[C@H](O)[C@H]1O"，reaction_type="oxidation"（第33行）。
    - S2（第53–91行）lactone → 6-sulfo-D-gluconate "OC(=O)C(O)C(O)C(O)C(O)CS(=O)(=O)O"，"hydrolysis"（第72行）。
    - S3（第92–130行）→ 2-dehydro-3-deoxy-6-sulfo-D-gluconate "OC(=O)C(=O)CC(O)C(O)CS(=O)(=O)O"，"dehydration"（第111行）。
    - S4（第131–174行）→ pyruvate "CC(=O)C(=O)O"（role=main）+ 3-sulfolactaldehyde "O=CC(O)CS(=O)(=O)O"（role=main），"aldol cleavage"（第155行）。
    - S5（第175–213行）3-sulfolactaldehyde → 3-sulfolactate "OC(=O)C(O)CS(=O)(=O)O"，"oxidation"（第194行）。
    - S6（第214–257行）3-sulfolactate → pyruvate（main）+ sulfite "[O-]S([O-])=O"（byproduct），"desulfonation"（第238行）。
  - 后置字段：central_metabolism_entry.products=["pyruvate"]（第380行）、downstream_continuation=[]（第383行）、alternative_branches=[]（第384行）、uncertainties=[]（第405行）、6 步 step.uncertainty 均 null（第51、90、129、173、212、256行）。
  - 答案自带反应证据：6 步 reaction_evidence_id 均="EVID_002"（第49、88、127、171、210、254行）；EVID_002（第395–403行）source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null（第399行）、claim_scope=["pathway_steps"]、confidence="medium"。

- 核查来源/新证据ID及支持范围：
  - gold/reaction_gold.tsv（BIOPATH150_146 / BSY-p00985，linear_display_order 1→5）：S05 6-sulfo-beta-D-quinovose → 6-deoxy-6-sulfo-D-fructose；S01 该果糖 +ATP → 6-deoxy-6-sulfo-D-fructose 1-phosphate（+ADP/H+）；S03 1-phosphate → (2S)-3-sulfolactaldehyde + glycerone phosphate；S02 (2S)-3-sulfolactaldehyde +NAD(P)+ +H2O → (2S)-3-sulfolactate +NAD(P)H +H+；S04 (2S)-3-sulfolactate[cytosol] → 同名化合物[extracellular space]（转运）。支持范围：gold 的逐步底物/产物/方向（gold_orientation=SUBSTRATE_TO_PRODUCT，arrow_class=forward）；不支持范围：gold 是核查基线不是唯一允许答案（P27），gold 未覆盖的合理路线不自动判错（P54）。
  - gold/case_root_identity.tsv（BIOPATH150_146 行）：pathway_name="sulfoquinovose degradation VI"、root=6-sulfo-beta-D-quinovose、terminal=(2S)-3-sulfolactate、aerobic_or_anaerobic="No data"。支持范围：gold 的路线名与起止化合物。
  - gold/formal_cases.tsv（BIOPATH150_146 行）：ordered_step_count=5、final_graph_status=LINEAR_UNIQUE、selection_tier=TIER_B_BROAD_ENVIRONMENTAL_OR_ORGANOSULFUR…（SULFONATED_OR_ORGANOSULFUR）、quarantined=FALSE。
  - gold/enzyme_gold.tsv：该路线 EC 为 5.3.1.31 / 2.7.1.184 / 4.1.2.57 / 1.2.1.97，转运步 ec_number_normalized=NOT_OBSERVED。支持范围：gold 各步首选酶与EC；不支持范围：不直接判答案所写反应不可能。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv（case 146 相关行）：EC 1.1.1.375、1.2.1.83、3.1.1.17、4.1.2.58、4.2.1.155、4.4.1.23 → 六行全部 coverage_status=OUT_OF_SNAPSHOT_UNRESOLVED（note："未联网补齐；UNRESOLVED不判虚构也不判支持"）。
  - facts/IUBMB_EXPLORENZ/ 共 21 张 EC 卡，**不含上述 6 个号**；本 case 卡为 ec_5.3.1.31、ec_2.7.1.184、ec_4.1.2.57、ec_4.1.2.55、ec_5.3.1.34、ec_2.7.1.106，后三张分别对应 2-dehydro-3-deoxy-phosphogluconate…aldolase / D-erythrulose 4-phosphate isomerase / glucose-1,6-bisphosphate synthase，与本答案 6 步反应均无对应。
  - facts/PUBMED/（6501223、2670929）、facts/EUROPE_PMC/（PMC179094）为甲苯与对枯烯文献卡，与本 case 无关；facts/ 全树 grep "sulfoquinovose" 仅命中 ec_5.3.1.31.json。→ 包内无任何支持本答案氧化路线的文献/条目。
  - 答案自有证据 EVID_002：INTERNAL_KNOWLEDGE_ONLY、locator=null → 包内无法定位核对其 claim_scope="pathway_steps" 的实际内容（支持范围=自我声明，无外部可核记录）。

- 关键事实（供本人判断，非结论）：
  1. 若走四步判断（P57–62），各步所需事实：第1步题面是否指定具体路线/终点——事实：题面给了路线范围名"sulfoquinovose degradation VI"（题面第6行"路线范围"、第11行"route_scope.chosen_route_name 必须原样填写…不得改选其他路线"），题面正文未给化合物终点；gold 终点=(2S)-3-sulfolactate（case_root_identity）。第2步答案是否明确声明替代路线或范围边界——事实：**未声明**（route_scope.notes=null 第10行、alternative_branches=[] 第384行、uncertainties=[] 第405行；route_summary 第12行自称所写即"sulfoquinovose degradation VI 途径"）。第3步是否有可核证据——事实：答案交付的 EVID_002 为 INTERNAL_KNOWLEDGE_ONLY 且 locator=null；包内对其 6 个 EC 全记 OUT_OF_SNAPSHOT_UNRESOLVED，无文献卡；按 P60 语义"无→按未证实登记，不自动判错也不给高分"（此处仅陈述包内证据状态，不作结论）。第4步偏离是否使主要结论失效——留待本人判断。
  2. 与 gold 的一致点（事实）：主底物 6-sulfo-beta-D-quinovose 与 gold 起点一致；第5步 3-sulfolactaldehyde → 3-sulfolactate 与 gold S02 的主转化同类（gold 另有 NAD(P)+/H2O→NAD(P)H/H+ 辅因子，答案 S5 未写辅因子）；产物中 pyruvate、3-sulfolactaldehyde、3-sulfolactate 均为 gold 路线出现过的化合物（3-sulfolactaldehyde、3-sulfolactate 在 gold 分别为 S03/S02 中间体）。
  3. 与 gold 的差异点（事实）：首步答案为氧化（1.1.1.375 生成 gluconolactone），gold 为异构化（5.3.1.31）；gold 有 ATP 磷酸化步（2.7.1.184），答案无磷酸化步；gold 醛缩底物为 6-deoxy-6-sulfo-D-fructose 1-phosphate、产物为 (2S)-3-sulfolactaldehyde + glycerone phosphate（4.1.2.57），答案醛缩底物为未磷酸化 6-sulfo-D-gluconate、产物为 pyruvate + 3-sulfolactaldehyde（4.1.2.58）；gold 第5步为转运出胞（3-sulfolactate exporter，无EC），答案第6步为脱磺生成 pyruvate + sulfite（4.4.1.23）；gold 终点为 sulfolactate，答案继续至 pyruvate+sulfite（位于 gold 终点下游）。
  4. 步间连续性（事实，逐字段自查）：S1 产物 6-sulfo-D-gluconolactone = S2 底物；S2 产物 = S3 底物；S3 产物 = S4 底物；S4 的 main 产物之一 3-sulfolactaldehyde = S5 底物；S5 产物 = S6 底物；每步 predecessor_step_ids 依次为 []/S1/S2/S3/S4/S5，order 1–6 连续。碳数逐级为 6→6→6→6→(3+3)→3→(3+3)，各步 SMILES 中 C 数与名称一致（无明显碳数失衡的字面迹象）。
  5. 量表条款（一句话）：P57–62 四步判断（与gold不同不自动cap，未声明且偏离为cap候选）；P100 D1/D2边界（"自称合规却交付不同化学路线"的任务参数偏离归 D1，反应化学质量归 D2，两维独立不连坐）；P29（题面指定具体终点才构成 D2 范围边界——本题面只给路线名）；P103–105（辅因子遗漏通常属局部计量缺陷）。与之相关的字面事实：全 6 步底物/产物成员共 13 个 role="main" + 1 个 role="byproduct"（S6 sulfite 成员，第232–236行），**无任何 role="cofactor" 成员、全文无 water**；即 S1 氧化步未写氧化当量受体、S2 水解步未写 water、S5 氧化步未写 NAD(P)+（对照 gold S02 为 NAD(P)+/H2O→NAD(P)H/H+）。
  6. 包内证据缺口：路线级支持证据（EVID_002 locator=null）无法核对；6 个 EC 全部 OUT_OF_SNAPSHOT_UNRESOLVED；无任何与本氧化路线相关的文献/条目卡；题面路线名与 gold 路线名是否指同一化学内容，包内无命名对照文件 → 以上均记 UNRESOLVED、待联网核查。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，5分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：六步链内部连续、无原子守恒问题、无触发条款命中；但全链证据为INTERNAL_KNOWLEDGE_ONLY、6个EC不可核、未声明为替代路线→四步判断'按未证实登记，不自动判错也不给高分'→第3档取5。路线/终点符合度按P100归D1（本轮未列该维），特此登记。（把握度：中）

- 本人人工确认与日期：【待本人签】

## REV-B-005-D3a / D3a

核查问题：核对所写酶名、具体EC和该步反应是否对应；通配EC、近名酶或家族关系不能证明具体催化。缺证时保留待核，不凭负检索判酶不存在。

- 答案具体声称与原文位置：
  - steps[].enzyme 共 6 条，全部 gene_or_protein=null、evidence_id="EVID_002"、confidence="medium"：
    - S1（第34–40行）name="sulfoquinovose dehydrogenase"、ec_number="1.1.1.375"（第35–36行，confidence 第38行）。
    - S2（第73–79行）name="6-sulfo-D-gluconolactonase"、ec_number="3.1.1.17"（第74–75行）。
    - S3（第112–118行）name="6-sulfo-D-gluconate dehydratase"、ec_number="4.2.1.155"（第113–114行）。
    - S4（第156–162行）name="2-dehydro-3-deoxy-6-sulfo-D-gluconate aldolase"、ec_number="4.1.2.58"（第157–158行）。
    - S5（第195–201行）name="3-sulfolactaldehyde dehydrogenase"、ec_number="1.2.1.83"（第196–197行）。
    - S6（第239–245行）name="3-sulfolactate sulfolyase"、ec_number="4.4.1.23"（第240–241行）。
  - 6 步 reaction_evidence_id="EVID_002"（第49、88、127、171、210、254行）；EVID_002（第395–403行）source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null、claim_scope=["pathway_steps"]、confidence="medium"。→ 答案交付的酶-EC 证据在包内不可定位；claim_scope 字面只写 pathway_steps，未列 enzyme/EC（事实：按题面第6条 claim_scope 应描述该证据支持的范围）。
  - 步级酶不确定性：6 步 step.uncertainty 均 null（第51、90、129、173、212、256行）；uncertainties=[]（第405行）。

- 核查来源/新证据ID及支持范围：
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：本答案 6 个 EC 各占 1 行（EC 1.1.1.375、1.2.1.83、3.1.1.17、4.1.2.58、4.2.1.155、4.4.1.23），coverage_status 全部为 OUT_OF_SNAPSHOT_UNRESOLVED、fact_card_path 空、cases_seen=BIOPATH150_146。支持范围：登记"本快照能否定位该编号"；不支持范围：note 明写"UNRESOLVED不判虚构也不判支持"。
  - facts/IUBMB_EXPLORENZ/（21 张 EC 卡）中不存在上述 6 个号的任何卡 → 按 P71 无法核 accepted name、reaction、active/transferred/deleted 状态。
  - facts/IUBMB_EXPLORENZ/ec_5.3.1.31.json、ec_2.7.1.184.json、ec_4.1.2.57.json：gold 侧三条卡（accepted name 与 reaction 见各卡；均 ACTIVE）。支持范围：gold 各步酶的官方名称/反应；不支持范围：与本答案 6 个编号无对应，不能用来核本答案。
  - gold/enzyme_gold.tsv：本 case gold EC 集合={5.3.1.31, 2.7.1.184, 4.1.2.57, 1.2.1.97} + 转运步 NOT_OBSERVED。事实：与答案 EC 集合{1.1.1.375, 3.1.1.17, 4.2.1.155, 4.1.2.58, 1.2.1.83, 4.4.1.23} 交集为空。
  - facts/PUBMED/、facts/EUROPE_PMC/、facts/UNIPROT/、facts/NCBI_NUCCORE/ 内无与这 6 个酶名对应的卡；全树 grep "sulfoquinovose" 仅命中 ec_5.3.1.31.json → 6 个酶名包内均无独立佐证。

- 关键事实（供本人判断，非结论）：
  1. 六条酶-EC 配对逐一列出（位置见上），全部 confidence="medium"、gene_or_protein=null、无任何具体基因/蛋白标识可核。
  2. 编号核验状态：6/6 = OUT_OF_SNAPSHOT_UNRESOLVED，包内无 accepted name/reaction/状态可比 → 按 P66/P71–P72 每条只能记 UNRESOLVED（核验只提供事实状态，不自动给分或cap；不凭"号码看似合理"放行）。
  3. 类别级字面事实（EC 编号一般规则，非包内证据）：1.1.1.375 与 1.2.1.83 属一级类 1（氧化还原酶）、3.1.1.17 属一级类 3（水解酶）、4.2.1.155/4.1.2.58/4.4.1.23 属一级类 4（裂解酶），与各步 reaction_type（oxidation / hydrolysis / dehydration / aldol cleavage / oxidation / desulfonation）在一级类别层面字面相容；这只是类别层面事实，不构成对具体号的核验（P73：通配/相近编号不能反推具体号正确）。
  4. 酶名-反应-编号三者一致性：包内无这 6 张卡 → "酶名与EC互相矛盾""EC大类别与反应类型不匹配"两项在包内无法坐实也无法排除（记 UNRESOLVED，待联网核查）。
  5. 与 gold 的对齐差异（事实，非结论）：本答案 6 步的反应对象与 gold 5 步不同（见 D2 差异点），故不存在"同一步换编号"的直接比对；若走 P65/P66 的编号冲突条款，需先认定"是否同一步同一反应"（事实铺垫：两边中间体与辅因子写法不同，gold 为磷酸化路线、答案为非磷酸化氧化路线）。
  6. 量表条款（一句话）：R3/D3a 关键错误清单（P98 表 R3）为"EC大类别与反应类型不匹配；酶名与EC互相矛盾；把广谱家族相关性当成该具体反应的催化证据"；P63–P66 是 gold 通配/多注与单值冲突的保守处理；P71–P73 要求具体号先核官方条目、通配不反推、核验只给三态。
  7. 答案自身披露（事实）：酶 confidence 全为 medium、step.uncertainty 全 null、uncertainties=[]，即答案未列出任何酶-EC 层面的待核点。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：6个EC官方条目全取：4个（1.1.1.375/4.2.1.155/1.2.1.83/4.4.1.23）官方accepted name与reaction为完全不同的酶；仅3.1.1.17（广谱lactonase）与4.1.2.58（产物侧同构、底物名两侧不同）部分对得上；官方另有正确编号1.1.1.390/1.2.1.97/4.4.1.24存在。已核实'编号-酶-反应'不对应落在多数关键步（按本人A4同口径扩用于官方条目核验）→关键错误Y、cap≤4→取3。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-005-D3b / D3b

核查问题：分别核对物种/菌株身份、该菌完成所写单步的证据和整条路径能力；身份真实或单步记录不自动证明指定菌株完成全部步骤。

- 答案具体声称与原文位置：
  - steps[].microorganism 6 处全部相同（S1 第41–48行，S2 第80–87行，S3 第119–126行，S4 第163–170行，S5 第202–209行，S6 第246–253行）：organism_name="Bacteroides thetaiotaomicron"、strain="VPI-5482"、ncbi_taxid=226186、organism_profile_id="ORG_001"、confidence="high"（第46行等）、evidence_id="EVID_001"（第47行等）；6 步 trait_evidence_id="EVID_001"（第50、89、128、172、211、255行）。
  - organism_profiles[0]（第259–377行）：organism_name="Bacteroides thetaiotaomicron"（第262行）、strain="VPI-5482"（第263行）、ncbi_taxid=226186（第264行）。
  - complete_pathway_organism_profile_id="ORG_001"（第378行）→ 该 profile 被同时声明为完成整条路径的菌。
  - 性状中的身份/能力相关声称：F5_culture_collection={collection:"ATCC", accession:"29148"}、confidence="medium"（第299–307行）；F14_genome_basic={genome_accession:"NC_004663.1", genome_size_bp:6260361, gc_percent:42.9}、confidence="medium"（第359–368行）；F7 value="sulfoquinovose"、F8 value="degrades sulfoquinovose"、F9 value="sulfoquinovose dehydrogenase"，均 confidence="medium"（第317–334行）；F1 value="obligate anaerobe"、confidence="high"（第277–282行）；F15 value="human gut commensal, specialized to mammalian gastrointestinal tract"、medium（第369–374行）。全部 15 项 raw_text=null。
  - 证据：EVID_001（第386–394行）source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null、claim_scope=["organism_traits"]、confidence="medium"。→ 事实：该 claim_scope 字面只覆盖 organism_traits，而它同时被 6 步 step.microorganism.evidence_id 引用（身份/步级归属）；organism_profiles 身份区在 Schema 中无 evidence_id 字段。

- 核查来源/新证据ID及支持范围：
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：TAXID 226186 → COVERED_BY_FACT_CARD、facts/NCBI_TAXONOMY/taxid_226186.json；ACCESSION NC_004663.1 → COVERED_BY_FACT_CARD、facts/NCBI_NUCCORE/nuccore_NC_004663.1.json（cases_seen=BIOPATH150_146）；CULTURE 5 行为 ATCC 33015 / ATCC 43050 / ATCC 700007 / NCIB 9871 / NCIMB 9871，**无 ATCC 29148 行**。
  - facts/NCBI_TAXONOMY/taxid_226186.json：scientific_name="Bacteroides thetaiotaomicron VPI-5482"（与答案物种+菌株字段逐字一致）、record_status=CURRENT、record_dates.create=2002/05/08、update=2018/11/23；卡内 names 只有 scientific_name 与空 other_names，**无 rank 字段、无 lineage 字段**；support_scope_note："本卡仅陈述官方分类记录的学名、rank、lineage 与状态……不自动支持任何身份或能力声称。"→ 支持：学名文本、记录状态、与答案 taxid 的对应；不支持：rank/lineage 两项核验（包内无该字段）、任何能力声称。
  - facts/NCBI_NUCCORE/nuccore_NC_004663.1.json：definition="Bacteroides thetaiotaomicron VPI-5482, complete sequence."、organism.taxid=226186、record_status=CURRENT、create=2003/03/28；卡内**无序列长度与 GC% 字段**（grep facts/ 无 "6260361"、无 "42.9"）；support_scope_note 限定为标题与状态，"历史存在≠当前有效≠虚构"。→ 支持：登录号存在且归属该菌株；不支持：genome_size_bp=6260361 与 gc_percent=42.9。
  - ATCC 29148：register 无行，facts/BACDIVE/ 三张卡为 12880、13580、153432（分别为 Pseudomonas sp. mt-2 PaW1、Agrobacterium radiobacter DSM 30147、另一单株记录），均不含 ATCC 29148 → 包内无覆盖，待联网核查/记 UNRESOLVED。
  - gold/organism_gold.tsv（BIOPATH150_146）：STEP 级 13 行的菌为 Escherichia coli(562)、Alkalicoccus urumqiensis(1548213)、Bacillus aryabhattai(412384)、Pseudomonas putida(303)、Clostridium sp. MSTE9(1105031)；PATHWAY_COMPLETE 行 taxid=1548213、genome_id=GCA_002993335.1、pathway_complete=TRUE。事实：gold 登记中**没有 Bacteroides thetaiotaomicron**，gold 全路径菌为另一物种；gold 非穷举（P27/P54），此差异本身不构成反证。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv（12 条）：不含 Bacteroides 属任何条目。
  - facts/ 全树 grep "sulfoquinovose" 仅命中 ec_5.3.1.31.json；grep "thetaiotaomicron" 命中 taxid_226186.json 与 nuccore_NC_004663.1.json 两张身份卡 → 包内无该菌关于 sulfoquinovose 降解的反应级或整路径级证据卡（无 PubMed/PMC/BacDive 卡）。

- 关键事实（供本人判断，非结论）：
  1. 三层声称（P69）在本答案的落点：身份层=物种+菌株+TaxID（第42–44行、第262–264行），其中 taxid 226186 有卡覆盖且卡内学名与答案逐字一致，但卡缺 rank/lineage 两项 → P71 三项核验完成 1/3；反应级层=6 步各声明该菌完成该步，支撑证据 EVID_001 的 claim_scope 字面为 ["organism_traits"]、locator=null、source=INTERNAL_KNOWLEDGE_ONLY；完整路径层=complete_pathway_organism_profile_id="ORG_001"（第378行），包内无该菌整条路径能力证据，gold PATHWAY_COMPLETE 指向 Alkalicoccus urumqiensis。
  2. 答案内身份类编号共 3 组：taxid 226186（有卡、一致）、NC_004663.1（有卡、归属一致，但长度/GC 无卡）、ATCC 29148（无卡、无 register 行）。
  3. 与 gold 的关系（事实）：gold 该 case 步级菌 5 种与 PATHWAY_COMPLETE 菌均不含 B. thetaiotaomicron；答案把同一菌绑定全部 6 步并标全路径（gold 步级菌在各步间并不相同，如 E. coli、Alkalicoccus urumqiensis、Bacillus aryabhattai、Pseudomonas putida 各承担部分步）。gold 是基线不是穷举，此对照只登记差异不判对错（P27）。
  4. 答案自身披露与粒度：strain 有值（VPI-5482，菌株级粒度）、菌 confidence="high"（6 处）、性状 confidence 高低不一（high 5 项 / medium 7 项 / low 2 项 / unknown 1 项）、15 项 raw_text 全 null；无 step.uncertainty、无 uncertainties 条目披露身份或能力待核点。
  5. 量表条款（一句话）：R4/D3b 关键错误清单（P98 表 R4）="物种/菌株或TaxID编造；由基因组存在某酶直接推断完成整条路径；把仅支持单步的菌写成全路径菌"；P67 要求 TaxID 核 ScientificName/rank/lineage 且粒度一致；P106–P110 身份阶梯三档（粒度不足/异菌株错配/无关类群）与"能力是否独立成立"的组合判断；P72 核验只给三态；rubric 预定义表 CG07（身份 CORE）、CG08（步级归属 APPLICATION_CRITICAL）、CG09（全路径能力 CORE）。
  6. 包内证据缺口（一律待联网核查/UNRESOLVED）：taxid_226186 卡的 rank 与 lineage 字段；ATCC 29148 的保藏记录；NC_004663.1 的长度与 GC 值；该菌任一步（6 步任一）的反应级催化证据；该菌完成 sulfoquinovose degradation VI 全路径的实验证据；B. thetaiotaomicron 与本 case 的 gold 关联。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，4分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：身份/保藏层全命中（TaxID 226186官方rank/lineage、ATCC 29148型菌株有效）；能力层：PubMed题录零命中，Europe PMC全文层10篇无一为该菌SQ降解研究，含该菌的群落实验把SQ→DHPS归因E. coli。能力声称未证实→P40/P60→取4。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-005-D6 / D6

核查问题：核对原答案置信标签、null/未知和不确定性披露；区分单点过度确信与系统性误导，不因其他维度错误自动封顶，不把重复引用同一断言算多个独立事件。

- 答案具体声称与原文位置：
  - confidence 标签逐条清点（全答案 confidence 字段共 29 个 = 6 酶 + 6 菌 + 15 性状 + 2 证据；分布如下）：
    - 酶 confidence="medium" ×6：第38、77、116、160、199、243行（同块 evidence_id 行为第39、78、117、161、200、244行）。
    - 菌 confidence="high" ×6：第46、85、124、168、207、251行（同块 evidence_id 行为第47、86、125、169、208、252行）。
    - 性状 confidence：high ×5（F1 第281行、F10 第339行、F11 第345行、F12 第351行、F13 第357行）；medium ×7（F2 第275行、F5 第306行、F7 第321行、F8 第327行、F9 第333行、F14 第367行、F15 第373行）；low ×2（F3 第297行、F6 第315行）；unknown ×1（F4 第287行）。
    - evidence_registry confidence="medium" ×2：EVID_001 第393行、EVID_002 第402行。
  - null / 未知披露：
    - route_scope：oxygen_condition=null（第7行）、is_single_continuous_route=null（第9行）、notes=null（第10行）。
    - gene_or_protein=null ×6（第37、76、115、159、198、242行）；EVID_001/002 的 database=null、record_id=null、locator=null（第388–390、397–399行）。
    - 性状：F4 value=null、evidence_id=null、confidence="unknown"（第283–288行，唯一 unknown 性状）；F6 terminal_electron_acceptor=null（第311行）；15 项 raw_text 全为 null（各性状 raw_text 行）；F2 仅给 optimum_c=37、minimum/maximum=null（第266–276行）；F3 仅给 optimum=7.0（第289–298行）；F14 三子键有值（第359–368行）。
    - 空数组/空值：downstream_continuation=[]（第383行）、alternative_branches=[]（第384行）。
  - uncertainties 数组内容：**空数组 0 条**（第405行 "uncertainties": []）；6 步 step.uncertainty 均为 null（第51、90、129、173、212、256行）→ 全答案无任何逐项不确定性文字。
  - 高标签与其绑定证据的强度关系（事实并列）：6 处菌 "high" 与 5 处性状 "high" 的 evidence_id 均为 EVID_001，而 EVID_001 自身 source_type="INTERNAL_KNOWLEDGE_ONLY"、locator=null、confidence="medium"（第386–394行）；6 处酶 "medium" 绑定的 EVID_002 同为 INTERNAL_KNOWLEDGE_ONLY、locator=null、confidence="medium"（第395–403行）。
  - 题面相关条文（题面 messages[0].content 第19行原文）："没有任何来源时填 null，并把该事实的 confidence 填为 low 或 unknown"；第18行：枚举字段未知时填 unknown。事实：本答案 6 步的菌与反应均有 evidence_id（非 null），故该条"无来源时"前提在答案侧是否成立取决于 EVID 是否算"来源"（EVID 为答案自建标签、source_type=INTERNAL_KNOWLEDGE_ONLY、locator=null）。

- 核查来源/新证据ID及支持范围：
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv（全表 78 条登记）：本答案引用的 8 个标识符对应 8 行——EC 1.1.1.375 / 1.2.1.83 / 3.1.1.17 / 4.1.2.58 / 4.2.1.155 / 4.4.1.23 六行全 OUT_OF_SNAPSHOT_UNRESOLVED；TAXID 226186 → COVERED_BY_FACT_CARD；ACCESSION NC_004663.1 → COVERED_BY_FACT_CARD。（同 case 另有 EC 2.7.1.106、4.1.2.55、5.3.1.31、5.3.1.34 与 TAXID 294 五行，cases_seen=BIOPATH150_146，但不出现在本答案中，属同 case 其他条目的标识符。）支持范围：登记哪些标识符可核；不支持范围：不评价标签是否过高。
  - facts/NCBI_TAXONOMY/taxid_226186.json 与 facts/NCBI_NUCCORE/nuccore_NC_004663.1.json：support_scope_note 均明写"不自动支持任何身份或能力声称"（taxid 卡）/"仅陈述标题与状态"（nuccore 卡）。支持范围：身份与记录存在；不支持范围：菌株降解能力、全路径能力、基因组数值。
  - facts/ 中无 ATCC 29148、无 6 个 EC 卡、无该菌文献卡（见 D3a/D3b 节）→ 与这些字段绑定的 medium/high 标签在包内无可核支撑。
  - gold/organism_gold.tsv：gold PATHWAY_COMPLETE=Alkalicoccus urumqiensis(1548213)，gold 步级菌中无 B. thetaiotaomicron → 与答案 complete_pathway 声称并列的事实对照（gold 非穷举，P27）。
  - rubric/LIKERT…TEXT_EXTRACT.txt：R7 行（P12 表 R7）"是否清楚区分观测、预测、推断及未知；置信度与证据是否相称……例：单一间接来源标 high confidence，且不披露替代路线或身份冲突"；P119（D6 严重度）单点过度确信档内扣、系统性误导才 cap 候选；P120 同一根本断言多步重复引用仍是一个事件；P171 cap 候选条件（系统性把预测写成实证/掩盖已知矛盾/置信与证据明显不相称）；P121 D5 错引不自动联动 D6；CG20（不确定性与置信度标签，criticality=SUPPORTING，"单点过度确信档内扣"）。

- 关键事实（供本人判断，非结论）：
  1. 标签全景：high 集中在 6 处菌归属 + 5 项形态/氧/运动性状；medium 用于 6 处酶 + 7 项性状 + 2 条证据；low 仅 F3、F6 两项；unknown 仅 F4 一项。全答案未使用任何 step.uncertainty 或 uncertainties 条目（0 条）。
  2. 证据类型事实：两条证据均 source_type=INTERNAL_KNOWLEDGE_ONLY、locator=null、record_id=null → 属自我声明型来源；答案把它们的 confidence 自标为 medium，并以此支撑 confidence=high 的菌归属与 5 项性状（标签高于证据条目自身标签，为答案内字段的事实关系）。
  3. 与冻结证据的对位事实：可核的两个身份标识（taxid 226186、NC_004663.1）与答案字段一致；6 个 EC 全部 OUT_OF_SNAPSHOT_UNRESOLVED（不可核）；ATCC 29148、基因组长度/GC、菌株降解能力、全路径能力 5 类声称包内无覆盖。
  4. 披露完整性事实：route_scope 三处 null 已如实留空；F4 以 unknown+null 诚实标注；F6 电子受体 null；15 项 raw_text 全 null（任务规定 raw_text 无原文则 null）；但与之并存的是 uncertainties=[]、6 步 uncertainty=null，即答案未列出任何待验证点，包括包内记为 UNRESOLVED 的 6 个 EC 与非 gold 菌全路径声称。
  5. 若按 P119/P120 判断需认定的事实铺垫：a) high/medium 标签涉及的独立断言数量（菌身份与 6 步归属是否属同一根本断言的重复、5 项性状是否同源）；b) 答案是否"掩盖已知矛盾"——需本人认定答案是否知悉（包内只提供"gold 菌清单不含该菌""6 个 EC 不可核"这类并列事实，不提供答案的知晓状态）；c) 是否属"单一间接来源标 high confidence 且零披露"的字面情形——事实：证据 source_type 为 INTERNAL_KNOWLEDGE_ONLY 且 locator=null，菌标签为 high，uncertainties 为空。
  6. 包内与过度确信相关的事实信号（逐条，均非结论）：EVID_001/002 无 locator 可核；6 EC 全 UNRESOLVED；taxid/nuccore 卡明示不支持能力声称；gold 全路径菌与答案不同；B. thetaiotaomicron 不在 gold 步级菌中；答案 0 条不确定性披露。以上信号不自动构成 cap（P121：D5 状态不联动；四.1：不连坐）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，7分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：单点过度确信（R7/P119）：uncertainties=[]零披露，6个不可核EC与非gold菌全路径声称未作待核披露；其余null/unknown字段诚实填写→档内7–8取7。（把握度：高）

- 本人人工确认与日期：【待本人签】
