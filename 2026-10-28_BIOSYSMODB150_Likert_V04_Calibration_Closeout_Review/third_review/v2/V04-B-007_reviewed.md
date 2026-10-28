# V04-B-007：定点人工复核

- case：BIOPATH150_007
- 只需核定：D3a、D3b。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-007-D3a / D3a

核查问题：核对所写酶名、具体EC和该步反应是否对应；通配EC、近名酶或家族关系不能证明具体催化。缺证时保留待核，不凭负检索判酶不存在。

- 答案具体声称与原文位置：
  - 本答案共 4 步（S1–S4，线性，visible_answer.txt 第13–190行），2 个酶条目各复用 2 步：
  - steps[0].enzyme（S1，第39–45行）：name="Haloalcohol dehalogenase HheC"（第40行）、ec_number="4.5.1.1"（第41行）、gene_or_protein="HheC"（第42行）、confidence="medium"（第43行）、evidence_id="EVID_001"。该步反应声称（第19–37行）：1,3-Dichloro-2-propanol（main）→ Epichlorohydrin（main）+ Hydrogen chloride（byproduct），reaction_type="dehalogenation"（第38行）。
  - steps[1].enzyme（S2，第83–89行）：name="Epoxide hydrolase EchA"（第84行）、ec_number="3.3.2.10"（第85行）、gene_or_protein="EchA"（第86行）、confidence="medium"、evidence_id="EVID_001"。该步反应声称（第63–81行）：Epichlorohydrin（main）+ Water（cofactor）→ 3-Chloro-1,2-propanediol（main），reaction_type="epoxide hydrolysis"（第82行）。
  - steps[2].enzyme（S3，第127–133行）与 steps[3].enzyme（S4，第171–177行）：分别与 S1、S2 相同（HheC 4.5.1.1 / EchA 3.3.2.10，confidence 均 "medium"）。
  - route_summary（第12行）："1,3-二氯-2-丙醇经 HheC 脱卤生成环氧氯丙烷，再经 EchA 水解生成 3-氯-1,2-丙二醇，再由 HheC 脱卤生成缩水甘油，最后经 EchA 水解生成甘油。"
  - evidence_registry EVID_001（第302–314行）：source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null、claim_scope=["1,3-DCP degradation steps","enzymes HheC and EchA","Agrobacterium radiobacter AD1 pathway"]、confidence="medium"。
  - uncertainties[0]（第328行）："酶 EC 编号和菌株性状基于一般文献知识；未核对原始文献中菌株 AD1 的完整表型。"
- 核查来源/新证据ID及支持范围：
  - gold/enzyme_gold.tsv（BIOPATH150_007，8 行酶记录，全为通配 EC）：S01/S03 = halohydrin epoxidase A（EC-4.5.1.-，BSY-e03966）；S02/S04 = epoxide hydrolase A（EC-3.3.2.-，BSY-e03967）；S05/S07 = halohydrin epoxidase B（EC-4.5.1.-）；S06/S08 = epoxide hydrolase B（EC-3.3.2.-）。支持范围：gold 登记该路线各步首选酶与通配 EC；不支持范围：gold 是核查基线非唯一允许答案（量表 P27），且 gold 内无某酶名/EC 不等于其不存在。
  - gold/reaction_gold.tsv（BSY-p00077）：S01 1,3-Dichloro-2-propanol → Epichlorohydrin；S02 Epichlorohydrin → 3-Chloro-1,2-propanediol；S03 3-Chloro-1,2-propanediol → Glycidol；S04 Glycidol → Glycerol。支持范围：答案 S1–S4 与 gold S01–S04 的底物/产物名逐一对应（同一化学序列）；不支持范围：gold 另有 S05–S08 第二分支（(R)-型对映体序列，formal_cases.tsv 登记 BRANCHED_DAG 8 步），该分支属 D1/D2 范围，本维不评。
  - facts/IUBMB_EXPLORENZ/ec_3.3.2.10.json（EVIDENCE_COVERAGE_REGISTER.tsv 第49行，COVERED_BY_FACT_CARD，BIOPATH150_007）：record_status="ACTIVE"，accepted_name="soluble epoxide hydrolase"，systematic_name="epoxide hydrolase"，reaction="an epoxide + H2O = a glycol"。支持范围：该 EC 活跃存在、官方反应为"环氧化物+水→二醇"，与答案 S2/S4 所写 epoxide hydrolysis 化学方向一致；不支持范围：support_scope_note 明写"不自动支持或反驳任何答案声称"；该卡也不核验 "EchA" 基因/蛋白名本身。
  - facts/IUBMB_EXPLORENZ/ec_4.5.1.5.json（register 第64行，COVERED_BY_FACT_CARD）：accepted_name="S-carboxymethylcysteine synthase"，record_status="ACTIVE"。支持范围：仅说明 4.5.1.5 是另一具体编号的另一酶；不支持范围：**不能**用于核验答案的 4.5.1.1（不同编号）。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv 第63行：EC 4.5.1.1 → coverage_status=OUT_OF_SNAPSHOT_UNRESOLVED、fact_card_path 空、cases_seen=BIOPATH150_007，note"只登记能否定位既有冻结记录；未联网补齐；UNRESOLVED不判虚构也不判支持"。支持范围：说明 4.5.1.1 在快照内无卡；不支持范围：既不支持也不反驳。
  - 包内缺口（事实）：EC 4.5.1.1 无官方卡（accepted name/reaction/状态均不可核）；"HheC"、"EchA" 基因/蛋白名无任何事实卡（facts/UNIPROT/ 两张卡分别为 Xanthobacter autotrophicus dhlA 与 E. coli ybhB，与 HheC/EchA 无关）。
- 关键事实（供本人判断，非结论）：
  1. 答案 D3a 交付 2 个酶条目，均带具体 EC 号与基因/蛋白名、confidence="medium"、唯一证据 EVID_001 为 INTERNAL_KNOWLEDGE_ONLY（locator=null、无记录号）。
  2. 与 gold 的对照（事实）：gold 该两步反应的 EC 均为通配 4.5.1.- 与 3.3.2.-；答案给出同族具体号 4.5.1.1 与 3.3.2.10。量表条款：P64"gold为通配EC时，答案给出同族具体号不自动判错；先查官方accepted name/reaction再定"；P73"通配EC不能反推答案具体号正确"。
  3. 官方卡核验可得性（P71 要求 EC 核 accepted name/reaction/状态）：3.3.2.10 可核（ACTIVE，accepted name/reaction 与所写步骤一致方向）；4.5.1.1 不可核（OUT_OF_SNAPSHOT_UNRESOLVED）→ 该 EC 的名称/反应/状态记 UNRESOLVED、待联网核查。
  4. 酶名对照（事实）：gold 名为 "halohydrin epoxidase A" 与 "epoxide hydrolase A"；答案名为 "Haloalcohol dehalogenase HheC" 与 "Epoxide hydrolase EchA"。名称写法不同；包内无 HheC/EchA 的官方记录卡，无法核对名称-EC 对应，待联网核查。
  5. 量表相关条款（原文位置供查）：R3/D3a 关键错误清单（P174 行 R3）为"EC大类别与反应类型不匹配；酶名与EC互相矛盾；把广谱家族相关性当成该具体反应的催化证据"；P72"核验程序只提供事实状态（SUPPORTED/CONTRADICTED/UNRESOLVED），不自动给分或cap"；P72 要求每条证据记录支持什么/不支持什么。
  6. 答案自身披露：uncertainties[0]（第328行）主动声明"酶 EC 编号…基于一般文献知识"；step 级 uncertainty 字段全为 null（第56、100、144、188行）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：EC 4.5.1.1官方条目=DDT-dehydrochlorinase（DDT→DDE+chloride，1961），条目内无任何haloalcohol/halohydrin内容；HheC/EchA文献真实存在但该PubMed记录化学表列EC 3.8.1.-（非4.5.1.1）。核心酶-EC对应已核实不成立→Y、cap≤4→取3。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-007-D3b / D3b

核查问题：分别核对物种/菌株身份、该菌完成所写单步的证据和整条路径能力；身份真实或单步记录不自动证明指定菌株完成全部步骤。

- 答案具体声称与原文位置：
  - 身份层：steps[0..3].microorganism（第46–53、90–97、134–141、178–185行）均为 organism_name="Agrobacterium radiobacter"、strain="AD1"、ncbi_taxid=null、organism_profile_id="ORG_001"、confidence="medium"、evidence_id="EVID_002"。即：声称具体菌株 "AD1"，但未交付任何 TaxID 编号。
  - organism_profiles[0]（第191–293行）：organism_name="Agrobacterium radiobacter"（第194行）、strain="AD1"（第195行）、ncbi_taxid=null（第196行）；15 项性状中 10 项有值（F1/F6/F7/F8/F9/F10/F11/F12/F13/F15，均挂 EVID_002，confidence 除 F12="high" 外均为 "medium"），5 项 null/unknown（F2/F3/F4/F5/F14）。
  - 反应级层：4 步的 microorganism 全部绑定 ORG_001（即声称该菌逐步完成全部 4 步反应）。
  - 完整路径层：complete_pathway_organism_profile_id="ORG_001"（第294行）；route_summary（第12行）末句"该主链在好氧条件下由 Agrobacterium radiobacter AD1 完成。"
  - 证据：EVID_002（第315–325行）source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null、claim_scope=["traits of Agrobacterium radiobacter AD1"]、confidence="medium"；EVID_001（第302–314行）claim_scope 含 "Agrobacterium radiobacter AD1 pathway"。
  - 披露：uncertainties[0]（第328行）"酶 EC 编号和菌株性状基于一般文献知识；未核对原始文献中菌株 AD1 的完整表型。"
- 核查来源/新证据ID及支持范围：
  - gold/organism_gold.tsv（BIOPATH150_007，STEP 级 30 行 + PATHWAY_COMPLETE 2 行）：
    - S01/S03 行含 Agrobacterium radiobacter（taxid 362，EXACT）、Agrobacterium radiobacter AD1(pTB3)（No TaxID，NORMALIZED_EXACT）、Arthrobacter sp. AD2（168809）、Corynebacterium sp.（1720）、Corynebacterium sp. N-1074（No TaxID）。
    - S02/S04 行：Agrobacterium radiobacter AD1 与 Agrobacterium radiobacter strain AD1(pTB3) 两行的 organism_match_status=**UNRESOLVED**（gold 自身未解析到 taxid）；另有 Arthrobacter sp. AD2、Corynebacterium sp. N-1074（NORMALIZED_EXACT）。
    - S05–S08 行：Agrobacterium radiobacter AD1(pTB3)、Arthrobacter sp. AD2、Corynebacterium sp. N-1074。
    - PATHWAY_COMPLETE 2 行：taxid 168809（Arthrobacter sp. AD2）与 No TaxID（Corynebacterium sp. N-1074），均 pathway_complete=TRUE、download_available=FALSE。gold **未**把 Agrobacterium radiobacter AD1 登记为该路线 pathway_complete。
    - 支持范围：gold 登记逐步酶-菌对应与全路径菌；不支持范围：gold 非穷举（量表 P27、P54），gold 无某菌不构成反证；S02/S04 的 AD1 行 UNRESOLVED 是 gold 自身状态，非对答案的裁定。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：本答案 ncbi_taxid=null，故无按答案交付编号登记的 TAXID 行；全表 79 行内无 TAXID 362 或 168809 的登记行。
  - facts/NCBI_TAXONOMY/ 共 10 张卡（105560、183193、226186、280、28040、303、336257、351746、390235、420662），**无 Agrobacterium radiobacter（362）卡**；taxid_303 是 Pseudomonas putida（不同物种）。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv（12 行）含一行物种名映射：source_name="Agrobacterium radiobacter"、source_taxid=358、reviewed_species_taxid=362、reviewed_species_name="Agrobacterium radiobacter"、status=VERIFIED_SPECIES_MAPPING_USER_SELECTED_GOLD_VERSION。支持范围：说明该物种名在包内有已核实的 species-level 名称/ID 映射记录；不支持范围：答案未交付 TaxID，该行不构成对答案 taxid 字段的核验，也不核验菌株 AD1。
  - facts/BACDIVE/bacdive_13580.json：description="Agrobacterium radiobacter DSM 30147 is an aerobe, Gram-negative, motile plant pathogen…"。支持范围：物种级（另一菌株 DSM 30147）的表型记录；不支持范围：不是 AD1 的记录，不支持逐步催化与整条路径声称。
  - 包内缺口（事实）：无 AD1 菌株级身份卡、无 AD1 单步催化实验证据卡、无 AD1 整条路径能力证据卡。
- 关键事实（供本人判断，非结论）：
  1. 三层声称各有原文：身份层=第46–53行等（物种名+strain="AD1"，taxid=null）；反应级层=4 步各绑定 ORG_001；完整路径层=第294行 complete_pathway_organism_profile_id="ORG_001" 与第12行 route_summary 末句。P69：三层声称分别核对，不得互相冒充。
  2. 身份层核验状态（事实）：答案 taxid=null → P71/P67 的编号核验（ScientificName/rank/lineage 三项）在本答案**无编号对象**；包内也无该物种分类卡。物种名的 crosswalk 映射行存在（358→362），但仅覆盖物种名映射，不覆盖 AD1 菌株身份。
  3. 反应级层核验状态（事实）：gold S01–S04 各步行中出现 "Agrobacterium radiobacter"/"AD1" 名称（S01/S03 两行 EXACT/NORMALIZED_EXACT；S02/S04 两行 gold 自身 UNRESOLVED）；同步骤 gold 行同时登记 Arthrobacter sp. AD2、Corynebacterium sp. 等其他菌。包内无 AD1 的独立单步实验证据卡（PubMed/UniProt/BacDive 卡均与 AD1 无关）。
  4. 完整路径层核验状态（事实）：gold PATHWAY_COMPLETE 指向 Arthrobacter sp. AD2（168809）与 Corynebacterium sp. N-1074（No TaxID）；A. radiobacter AD1 不在 gold 全路径行中。gold 非穷举，此差异本身不判对错。
  5. R4/D3b 关键错误清单（P175 行 R4）："物种/菌株或TaxID编造；由基因组存在某酶直接推断完成整条路径；把仅支持单步的菌写成全路径菌"。本答案 taxid=null → "TaxID编造"一项无核验对象（事实铺垫，不预判）。
  6. P106–P110 身份阶梯（粒度不足/异菌株错配/无关类群）的适用前提是先有官方核实结论；本答案无 taxid 交付且包内无该物种卡 → 尚无可套用的编号核实结论（事实铺垫，不预判档位）。
  7. 答案自身披露：菌 confidence="medium" 但唯一证据 EVID_002 为 INTERNAL_KNOWLEDGE_ONLY（无 locator/记录号）；10 项性状值挂同一 EVID_002（F12 标 "high"）；uncertainties[0] 明写"未核对原始文献中菌株 AD1 的完整表型"；性状 5 项诚实 null/unknown。
  8. 包内证据缺口清单：AD1 菌株身份（TaxID/保藏号）卡、AD1 单步反应级证据、AD1 整条路径能力证据、register TAXID 登记行（因答案 taxid=null 未产生）——均无覆盖 → 待联网核查/记 UNRESOLVED。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，5分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：能力/存在层命中：Europe PMC 'A. radiobacter AD1'82条、'以环氧氯丙烷为唯一碳源生长'摘要原句；菌株身份层未核：BacDive 0命中、NCBI Taxonomy无菌株级条目、保藏号未检出、'AD1(pTB3)'来源未检出→部分支持+未核项→取5。（把握度：高）

- 本人人工确认与日期：【待本人签】
