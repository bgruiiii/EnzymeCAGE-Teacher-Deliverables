# V04-B-001：定点人工复核

- case：BIOPATH150_146
- 只需核定：D2、D3a、D3b。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-001-D2 / D2

核查问题：逐步核对主底物到主产物的化学转化、方向和连续性。若可能是替代路线，先分清任务符合度与所写反应本身是否成立；检索无结果不等于反应不可能。

- 答案具体声称与原文位置：
  - steps[0]（S1，唯一一步，visible_answer.txt 第13–62行）：主底物 6-sulfo-beta-D-quinovose（SMILES: C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)S(=O)(=O)O，role=main）+ water（cofactor）→ 主产物 D-glucose（main）+ sulfite [O-]S(=O)[O-]（byproduct）；reaction_type="hydrolytic desulfonation"。
  - route_summary（第12行）：声称"sulfoquinovose degradation VI 路线中经水解脱硫生成 D-葡萄糖与亚硫酸盐"。
  - 中间体、磷酸化、醛缩、 sulfolactate 均未出现；主链只有 1 步。
- 核查来源/新证据ID及支持范围：
  - gold/reaction_gold.tsv（BIOPATH150_146，路线 BSY-p00985，5步线性）：S5 SQ --异构化--> 6-deoxy-6-sulfo-D-fructose；S1 +ATP --> 1-phosphate；S3 醛缩 --> (2S)-3-sulfolactaldehyde + glycerone phosphate；S2 +NAD(P)+ --> (2S)-3-sulfolactate；S4 转运出胞。全程硫保留在分子内，无 sulfite 产物；gold 终点=(2S)-3-sulfolactate。
  - gold/enzyme_gold.tsv：路线 VI 各步酶为 sulfoquinovose isomerase（EC 5.3.1.31）、6-deoxy-6-sulfofructose kinase（EC 2.7.1.184）、fructose-bisphosphate aldolase 类（EC 4.1.2.57）、3-sulfolactaldehyde dehydrogenase（EC 1.2.1.97）；gold 内不存在"sulfoquinovose sulfohydrolase"这类水解酶。
  - evidence/facts/IUBMB_EXPLORENZ/ec_5.3.1.31.json：EC 5.3.1.31 ACTIVE，accepted name=sulfoquinovose isomerase，reaction=β-sulfoquinovose = 6-deoxy-6-sulfo-D-fructose（支持 gold 第1步是异构化而非水解）。support_scope_note 声明不自动支持/反驳答案。
  - 冻结证据快照中无"sulfoquinovose sulfohydrolase"条目（答案 EC=null，无可核编号）；EVIDENCE_COVERAGE_REGISTER.tsv 对本条水解酶声称无覆盖记录。包内既不能证实也不能证伪该水解反应。
  - 答案自带证据 EVID_001=INTERNAL_KNOWLEDGE_ONLY（locator: "sulfoquinovose degradation VI; sulfoquinovose sulfohydrolase reaction"），无外部可核来源。
- 关键事实（供本人判断，非结论）：
  1. 答案把题面指定的路线 VI 表述为"一步水解脱硫"，与 gold 的五步异构化-磷酸化-醛缩路线**不是同一条化学路线**；终点也不同（答案终点 D-glucose+sulfite，gold 终点 sulfolactate）。
  2. 答案未声明这是替代路线，也未披露与 gold 路线名的冲突（route_scope.notes 只写"按题面指定路线填写，不改动路线名称"）。
  3. 量表相关条款：四.5 四步判断（P57–62，与gold不同不自动cap）；D1/D2边界（P100，自称合规却交付不同化学路线的任务参数偏离归D1，D2只评写出的反应本身）；简化表达/辅因子（P103–105）。
  4. 单看这一步水解反应本身：主底物+水→葡萄糖+亚硫酸盐，C–S键断裂、原子数自洽（C6→C6），方向合理；"检索无结果不等于反应不可能"——包内无该酶冻结证据，需联网核查或记待核。
  5. 若认定为"未声明的替代路线偏离"，其D2后果与D1后果须分别独立判定、不连坐（P100/四.1）。
- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：主链1步直达葡萄糖入糖酵解，触发'一步跳到中心代谢物'（P62/R2）→cap≤4；单步水解反应本身原子自洽、方向合理，故档内取3。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-001-D3a / D3a

核查问题：核对所写酶名、具体EC和该步反应是否对应；通配EC、近名酶或家族关系不能证明具体催化。缺证时保留待核，不凭负检索判酶不存在。

- 答案具体声称与原文位置：
  - steps[0].enzyme（S1，本答案唯一步，visible_answer.txt 第44–50行）：name="sulfoquinovose sulfohydrolase"（第45行）、ec_number=null（第46行）、gene_or_protein=null（第47行）、confidence="low"（第48行）、evidence_id="EVID_001"（第49行）。
  - 与酶绑定的反应声称：reaction_type="hydrolytic desulfonation"（第43行）；route_summary（第12行）"6-磺酸基-β-D-奎诺糖经水解脱硫生成 D-葡萄糖与亚硫酸盐"。
  - evidence_registry EVID_001（第203–217行）：source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator="sulfoquinovose degradation VI; sulfoquinovose sulfohydrolase reaction"（第209行）、claim_scope=["route","step","enzyme","microorganism"]（第210–215行）、confidence="low"（第216行）。
  - 答案自带的酶不确定性披露：step.uncertainty（第61行）"该路线下酶的具体 EC 编号、菌株菌株号与性状来源不足，相关字段填为 null。"（原文如此）；uncertainties[0]（第220行）"首选酶的 EC 编号与具体菌株证据不足，相关字段填为 null。"。
  - 定位说明：全答案仅 1 个酶条目，无 EC 号、无基因/蛋白名，故本维可核对象=酶名 + 该步反应本身。

- 核查来源/新证据ID及支持范围：
  - gold/enzyme_gold.tsv（BIOPATH150_146 / BSY-p00985，13行酶记录）：5步酶为 sulfoquinovose isomerase（EC 5.3.1.31，S05）、6-deoxy-6-sulfofructose kinase 与 sulfofructose kinase（EC 2.7.1.184，S01）、6-deoxy-6-sulfofructose-1-phosphate aldolase 与 sulfofructosephosphate aldolase（EC 4.1.2.57，S03）、3-sulfolactaldehyde dehydrogenase（EC 1.2.1.97，S02）、3-sulfolactate exporter（ec_number_raw 空、ec_number_normalized=NOT_OBSERVED，S04）。支持范围：gold 登记本 case 路线逐步首选酶与EC；不支持范围：gold 是核查基线不是唯一允许答案（量表 P27），gold 内不存在某酶名不等于该酶不存在。
  - facts/IUBMB_EXPLORENZ/ec_5.3.1.31.json：accepted_name="sulfoquinovose isomerase"，reaction="(1) β-sulfoquinovose = 6-deoxy-6-sulfo-D-fructose (2) β-sulfoquinovose = 6-sulfo-D-rhamnose"，record_status=ACTIVE，other_names=["yihS (gene name)"]。支持范围：gold 首步是异构化、官方酶名与EC一一对应；不支持范围：support_scope_note 明写"不自动支持或反驳任何答案声称"，且本卡不涉及"sulfoquinovose sulfohydrolase"。
  - facts/IUBMB_EXPLORENZ/ 另有 ec_2.7.1.184.json（accepted_name="sulfofructose kinase"，reaction="ATP + 6-deoxy-6-sulfo-D-fructose = ADP + …1-phosphate"，ACTIVE）与 ec_4.1.2.57.json（accepted_name="sulfofructosephosphate aldolase"，reaction="6-deoxy-6-sulfo-D-fructose 1-phosphate = glycerone phosphate + (2S)-3-sulfolactaldehyde"，ACTIVE）。支持范围：仅描述这两条 gold EC 的官方名称与反应；不支持范围：与答案所称水解酶无对应关系。facts/ 全树 grep "sulfoquinovose" 仅命中 ec_5.3.1.31.json 一个文件。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv（79行含表头=78条登记；identifier_type 只有 ACCESSION/CULTURE/EC/TAXID/UNIPROT_ACC 五类）：不存在与"sulfoquinovose sulfohydrolase"对应的任何行；本答案 ec_number=null，因此没有可供四.6 编号核验的对象。
  - 包内缺口（事实）：该酶名与其水解反应在冻结证据树中零覆盖（无 EC 卡、无 register 行、无 PubMed/UniProt/nuccore/BacDive 卡）→ 记 UNRESOLVED、待联网核查；本轮允许联网补证（协调端2026-10-28口径；冻结包构建期不联网，故该声称在包内无卡，联网核查待补），故不做任何名称存在性推断。

- 关键事实（供本人判断，非结论）：
  1. 答案 D3a 交付的酶条目共 1 个：EC=null、gene_or_protein=null、enzyme.confidence="low"，并有两处主动披露（第61行 step.uncertainty、第220行 uncertainties[0]）"EC 编号证据不足，填 null"。
  2. 与 gold 的差异（事实）：gold 该路线 5 步酶为异构酶/激酶/醛缩酶/脱氢酶/转运子，无水解脱硫酶条目；答案酶名与 gold 五个酶名均不相同；两边没有可直接比较的 EC（答案为 null）。
  3. 包内证据缺口：酶名"sulfoquinovose sulfohydrolase"与该水解反应无任何冻结事实卡或覆盖登记 → 既不能证实也不能证伪。
  4. 量表条款（一句话）：R3/D3a 关键错误清单（P98 表 R3）为"EC大类别与反应类型不匹配；酶名与EC互相矛盾；把广谱家族相关性当成该具体反应的催化证据"——本答案 EC=null，故"酶名与EC矛盾"与"编号大类错配"两项在本条无核验对象（事实铺垫）；四.6/P71–P72 要求具体EC先核 accepted name/reaction/状态且核验只给事实状态、不自动给分或cap；P73 通配EC不反推具体号（本条无编号）。
  5. 若走"缺证时保留待核、不凭负检索判酶不存在"的判断，可用事实：答案已自标 low 并两处披露证据不足；包内既无支持证据也无反证（"检索无结果不等于反应不可能"，本包不联网）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：核心酶名'sulfoquinovose sulfohydrolase'在ExplorEnz无条目、PubMed精确短语零命中；官方唯一系统名含sulfohydrolase者为EC 3.13.1.1（底物UDP糖，非游离SQ）；文献已知SQ→葡萄糖+亚硫酸盐路线均为加氧酶两步型（EC 1.14.14.181/1.14.11.84），与所写单步水解脱硫不同构。按P27负检索不判'不存在'，但核心声称零来源且与官方已知路线不同构→按未证实登记取低分3。（把握度：中）

- 本人人工确认与日期：【待本人签】

## REV-B-001-D3b / D3b

核查问题：分别核对物种/菌株身份、该菌完成所写单步的证据和整条路径能力；身份真实或单步记录不自动证明指定菌株完成全部步骤。

- 答案具体声称与原文位置：
  - steps[0].microorganism（S1，唯一一步，visible_answer.txt 第51–58行）：organism_name="Pseudomonas fluorescens"（第52行）、strain=null（第53行）、ncbi_taxid=294（第54行）、organism_profile_id="ORG_001"（第55行）、confidence="low"（第56行）、evidence_id="EVID_001"（第57行）。
  - organism_profiles[0]（第64–187行）：organism_name="Pseudomonas fluorescens"（第67行）、strain=null（第68行）、ncbi_taxid=294（第69行）；15项性状 value 全为 null（对象型子键全 null）、raw_text 全 null、evidence_id 全 null、confidence 全 "unknown"（第71–186行）。
  - complete_pathway_organism_profile_id="ORG_001"（第189行）：同一 profile 被声明为"完成整条路径"的菌（本答案主链仅 1 步）。
  - evidence_registry EVID_001（第203–217行）：source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator="sulfoquinovose degradation VI; sulfoquinovose sulfohydrolase reaction"、claim_scope=["route","step","enzyme","microorganism"]、confidence="low"。
  - 答案自带披露：step.uncertainty（第61行）含"菌株菌株号与性状来源不足，相关字段填为 null"（原文如此）；uncertainties[0]（第220行）"首选酶的 EC 编号与具体菌株证据不足，相关字段填为 null。"；uncertainties[1]（第221行）为 SMILES 近似表达声明。

- 核查来源/新证据ID及支持范围：
  - gold/organism_gold.tsv（BIOPATH150_146）：STEP 级 13 行 + PATHWAY_COMPLETE 1 行；出现的菌为 Escherichia coli（taxid 562）、Alkalicoccus urumqiensis（1548213）、Bacillus aryabhattai（412384）、Pseudomonas putida（303）、Clostridium sp. MSTE9（1105031）；PATHWAY_COMPLETE 行 taxid=1548213、genome_id=GCA_002993335.1、pathway_complete=TRUE、download_available=TRUE。支持范围：gold 登记的该路线逐步酶-菌对应与 gold 全路径菌；不支持范围：gold 是逐步酶登记非"可降解该污染物菌"的穷举，gold 无某菌不构成对该菌的反证（量表 P27、P54）。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：TAXID 294 → coverage_status=OUT_OF_SNAPSHOT_UNRESOLVED、fact_card_path 空、cases_seen=BIOPATH150_146，note"只登记能否定位既有冻结记录；未联网补齐；UNRESOLVED不判虚构也不判支持"。支持范围：说明该 TaxID 在本快照不可核；不支持范围：既不支持也不反驳答案身份。
  - facts/NCBI_TAXONOMY/ 共 10 张卡（105560、183193、226186、280、28040、303、336257、351746、390235、420662），**无 taxid_294 卡**；其中 taxid_303.json 是 Pseudomonas putida（与本案答案菌不同种）。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv（12 条已核实物种名映射）：不含 Pseudomonas fluorescens 或其别名 → 无别名核对支持。
  - facts/BACDIVE/ 三张卡为 bacdive_12880（Pseudomonas sp. mt-2 PaW1，含 ATCC 33015/CCUG 2480）、bacdive_13580（Agrobacterium radiobacter DSM 30147）、bacdive_153432；facts/PUBMED/（6501223、2670929）与 facts/EUROPE_PMC/（PMC179094）分别为甲苯与对枯烯文献卡。支持范围：与本 case 及本菌无关；不支持范围：不能用于本条任一层声称。
  - 包内缺口（事实）：无 Pseudomonas fluorescens 的任何事实卡、无其单步催化文献卡、无其整条路径能力证据卡。

- 关键事实（供本人判断，非结论）：
  1. 三层声称（P69 身份定位 ≠ 反应级能力 ≠ 完整路径能力）在本答案各有一处原文：身份层=第52–54行 + 第67–69行（物种名+物种级 TaxID 294、strain=null）；反应级层=第51–58行（该菌绑定 S1 这一步）；完整路径层=第189行 complete_pathway_organism_profile_id="ORG_001"。
  2. 覆盖状态：TaxID 294=OUT_OF_SNAPSHOT_UNRESOLVED，包内无该 TaxID 卡 → P71 要求的 ScientificName/rank/lineage 三项核验在包内无对象，身份层记 UNRESOLVED、待联网核查；包内同时无该菌反应级与路径级证据（两项均无覆盖）。
  3. 与 gold 的对照（事实）：gold 该 case 步级菌 5 种中无 Pseudomonas fluorescens，gold PATHWAY_COMPLETE 指向 Alkalicoccus urumqiensis（1548213）；答案菌与 gold 登记菌交集为空；gold 非穷举，此差异本身不判对错。
  4. 答案自身披露：菌 confidence="low"、唯一证据 EVID_001 为 INTERNAL_KNOWLEDGE_ONLY（locator 为路线/酶名文字、confidence=low、无记录号）；15 项性状全 null/unknown（诚实未知）；第61行与第220行两处披露菌株证据不足；strain 字段为 null（未给菌株号）。
  5. 量表条款（一句话）：R4/D3b 关键错误清单（P98 表 R4）为"物种/菌株或TaxID编造；由基因组存在某酶直接推断完成整条路径；把仅支持单步的菌写成全路径菌"；P67 要求 TaxID 核 ScientificName/rank/lineage 三项且粒度一致；P106–P110 身份阶梯三档（粒度不足/异菌株错配/无关类群）的适用前提是先取得官方核实结论，本条 TaxID 无卡 → 尚无可套用的核实结论（事实铺垫，不预判档位）；P72 核验只给事实状态，不自动给分或cap。
  6. 包内证据缺口清单：taxid_294 卡、P. fluorescens 任何分类卡、该菌单步反应级证据、该菌整条路径能力证据、crosswalk 别名行——均无覆盖 → 待联网核查/记 UNRESOLVED。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，4分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：身份层：TaxID 294=有效物种名（rank=species、lineage完整）；能力层：该菌降解SQ的文献PubMed零命中，属内文献路线菌为P. putida SQ1。身份真、能力未证实→P60不自动判错也不给高分→取4。（把握度：高）

- 本人人工确认与日期：【待本人签】
