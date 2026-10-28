# V04-B-023：定点人工复核

- case：BIOPATH150_021
- 只需核定：D2、D5。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

- 格式状态事实（先行登记）：items/V04-B-023/visible_answer.txt 为**单行、非法 JSON**——第1处语法错误在字符偏移 5768 附近，原文为 `"evidence_id":"EVID_002,"confidence":"high"`（evidence_id 值缺闭合引号），按 P98 表 R1"JSON语法损坏但人可阅读"形态登记；本底稿在仅修复该一处引号后完成解析，解析含 4 steps、1 profile、2 条 evidence。以下引用一律用 JSON 路径（如 steps[0].enzyme.ec_number），行号不可用。

## REV-B-023-D2 / D2

核查问题：逐步核对主底物到主产物的化学转化、方向和连续性。若可能是替代路线，先分清任务符合度与所写反应本身是否成立；检索无结果不等于反应不可能。

- 答案具体声称与原文位置：
  - route_scope：oxygen_condition="aerobic"、chosen_route_name="Toluene degradation to 2-hydroxypentadienoate (via toluene-cis-diol)"（与题面逐字符一致）；route_summary：甲苯→(1S,2R)-3-甲基环己-3,5-二烯-1,2-顺式二醇→3-甲基邻苯二酚→HOPDA→2-hydroxypenta-2,4-dienoate+乙酸。
  - steps[0]（S1）：底物 Toluene（main，SMILES "Cc1ccccc1"）+O2（cofactor）+NADH（cofactor）→ 产物 "(1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol (toluene cis-dihydrodiol)"（main，"OC1C(O)C=C(C)C=C1"）+NAD+（byproduct）；reaction_type="aromatic cis-dihydroxylation (dioxygenation)"。
  - steps[1]（S2）：顺式二醇（同字符串）+NAD+ → 3-methylcatechol（main，"Cc1cccc(O)c1O"）+NADH（byproduct）；reaction_type="cis-dihydrodiol dehydrogenation (rearomatization)"。
  - steps[2]（S3）：3-methylcatechol（同字符串）+O2 → "2-hydroxy-6-oxohepta-2,4-dienoate (HOPDA)"（main，"OC(=O)C(O)=CC=CC(=O)C"）；reaction_type="extradiol (meta) ring cleavage"。
  - steps[3]（S4）：HOPDA（同字符串）+H2O → "2-hydroxypenta-2,4-dienoate (2-hydroxypentadienoate)"（main，"OC(=O)C(O)=CC=C"）+Acetate（byproduct，"CC(=O)O"）；reaction_type="C-C hydrolase (hydrolytic cleavage)"。
  - predestinator_step_ids 链：S1→S2→S3→S4 线性；central_metabolism_entry.products=["2-hydroxypenta-2,4-dienoate","Acetate"]，explanation 明写"本路线评分范围止于 2-hydroxypentadienoate"。
  - uncertainties（4 条）：S2 EC 1.3.1.19/1.3.1.86 归类差异、S3 EC 1.13.11.15/1.13.11.2 差异、S4 EC 3.7.1.5 原始底物为 2-hydroxymuconic semialdehyde"对应 HOPDA 类似反应"、菌株性状来自种级描述。

- 核查来源/新证据ID及支持范围：
  - gold/reaction_gold.tsv（BIOPATH150_021，BSY-p00229，共 20 行参与者记录，按 linear_display_order 1–4 四步）：
    - 第1步（BSY-r01751，gold_orientation=forward）：底物 Toluene+O2+NADH+**H+** → 产物 (1S,2R)-3-Methylcyclohexa-3,5-diene-1,2-diol+NAD+。
    - 第2步（BSY-r01747，forward）：底物 NAD++二醇 → 产物 **H+**+NADH+3-Methylcatechol。
    - 第3步（BSY-r01753，**gold_orientation=none**，gold 内部登记特征；含义属命题侧待考，不归责模型）：底物 3-Methylcatechol+O2 → 产物 2-Hydroxy-6-oxohepta-2,4-dienoate+**H+**。
    - 第4步（BSY-r01746，forward）：底物 HOPDA+H2O → 产物 (2Z)-2-hydroxypenta-2,4-dienoate+**H+**+Acetate。
    - gold 终点化合物=Acetate | (2Z)-2-hydroxypenta-2,4-dienoate（gold/case_root_identity.tsv 该行 terminal 字段）。
  - gold/enzyme_gold.tsv 逐步 EC（登记对照用，酶-EC 对应判定属 D3a）：第1步 toluene 1,2-dioxygenase system EC 1.14.12.11（答案同）；第2步 cis-toluene dihydrodiol dehydrogenase EC 1.3.1.19（答案 1.3.1.86）；第3步 catechol 2,3-dioxygenase / 3-methylcatechol 2,3-dioxygenase 均 EC 1.13.11.2（答案同）；第4步 2-hydroxy-6-oxohepta-2,4-dienoate hydrolase EC 3.7.1.25（答案 3.7.1.5）。
  - facts/IUBMB_EXPLORENZ 官方卡（support_scope_note 均声明不自动支持/反驳答案）：ec_1.14.12.11.json（ACTIVE）reaction="toluene + NADH + H+ + O2 = (1S,2R)-3-methylcyclohexa-3,5-diene-1,2-diol + NAD+"——与 gold 第1步逐字符同构；ec_3.7.1.25.json（ACTIVE）reaction="(2Z,4E)-2-hydroxy-6-oxohepta-2,4-dienoate + H2O = (2Z)-2-hydroxypenta-2,4-dienoate + acetate"——与 gold 第4步同构；ec_1.3.1.19.json（ACTIVE）reaction="cis-1,2-dihydrobenzene-1,2-diol + NAD+ = catechol + NADH + H+"（苯环无甲基版本）；ec_1.3.1.86.json（ACTIVE）accepted_name=crotonyl-CoA reductase，reaction="butanoyl-CoA + NADP+ = (E)-but-2-enoyl-CoA + NADPH + H+"；ec_3.7.1.5.json（ACTIVE）accepted_name=acylpyruvate hydrolase，reaction="a 3-acylpyruvate + H2O = a carboxylate + pyruvate"。1.13.11.2 无卡（register OUT_OF_SNAPSHOT）。
  - facts/NCBI_TAXONOMY/taxid_183193.json：官方记录 scientific_name="**Streptomyces sp. DNK-G02**"（record_status=CURRENT）——答案 steps[0..3].microorganism.ncbi_taxid 与 profile 均填 183193 对应 P. putida F1；该卡仅陈述官方分类记录（本条属身份/编号事实，D2 只登记其与反应化学无关；两卡 raw_body_sha256 同值 c1a380d2… 的快照制作特征一并登记待考）。
  - 包内缺口：无 3-甲基底物版本的 1.3.1.19/1.3.1.86 判定卡（1.3.1.19 卡反应式为无甲基苯二醇）、无 1.13.11.2 卡；答案 S2/S4 的 EC 与 gold 不同号属 D3a 核验对象（非本维）。

- 关键事实（供本人判断，非结论）：
  1. **逐步对照表**（答案 vs gold，客观一致/差异）：
     | 步 | 转化 | 方向 | 与 gold 对照 |
     |---|---|---|---|
     | S1 | 甲苯→顺式二醇（双加氧） | 正向 | 主底物/主产物同名同 SMILES 底物侧一致；差异：gold 底物含 H+，答案缺 H+；gold 产物 NAD+ 为 REDOX_CARRIER，答案标 role="byproduct" |
     | S2 | 顺式二醇→3-甲基邻苯二酚（脱氢） | 正向 | 主底物/主产物一致（连续字符串相同）；差异：gold 产物含 H+，答案缺 H+ |
     | S3 | 3-甲基邻苯二酚→HOPDA（间位开环） | 正向 | 主底物/主产物一致；差异：gold 产物含 H+，答案缺 H+；gold 该行 gold_orientation=none |
     | S4 | HOPDA→2-羟戊-2,4-二烯酸酯+乙酸（水解） | 正向 | 主底物/主产物/副产物一致；差异：gold 产物含 H+，答案缺 H+；主产物答案 SMILES 为烯醇式 "OC(=O)C(O)=CC=C"（C5），gold 为 "(2Z)" 酮式电离表示 C=C/C=C(/C(=O)O)\[O-]（C5）；乙酸答案 "CC(=O)O" vs gold "CC(=O)[O-]"（质子化状态差） |
  2. 连续性（客观核对）：S1 产物字符串=S2 底物字符串；S2 产物=S3 底物；S3 产物=S4 底物——三处逐字符一致，链无跳步；4 步全部在同一 case 路线名下。
  3. 碳数守恒（客观计数）：C7（甲苯）→C7（二醇）→C7（甲基邻苯二酚）→C7（HOPDA，答案 SMILES OC(=O)C(O)=CC=CC(=O)C 计 7 碳）→C5+C2（HPD+乙酸），全链 7→7→7→7→(5+2)；答案未发生 C 数增减。氧/N 计量未逐原子核验（答案未声明配平口径；P104 简化表达条款供对照）。
  4. **四步判断的事实铺设**（P57–P62）：第1步题面已指定路线名（与 gold 同名同终点，case_root_identity.tsv 佐证）；第2步**答案未声明任何替代路线**——alternative_branches=[]，uncertainties 四条均为 EC 归类/性状来源披露，无一条声明"本路线与 gold 不同"或另立路线；第3步的事实基础=答案路线与 gold 主链同序（gold display order 1→4 对应答案 S1→S4）同向同终点；第4步"偏离是否使主要结论失效"待本人裁。适用条款：P62"与gold不同不自动等于关键错误"；P103 辅因子遗漏通常属局部计量缺陷（7–8档）条款的适用性由本人判——本答案 4 步各缺 gold 所列 H+ 一项、且 S1 把 NAD+ 标为 byproduct（role 标签差异登记为事实）。
  5. 酶-EC 差异（S2 1.3.1.86 vs gold 1.3.1.19；S4 3.7.1.5 vs gold 3.7.1.25）与官方卡 reaction 字段的对照材料已在"核查来源"列出；该对应是否构成 D3a/关键错误属 D3a 范围（本答案未派 D3a），此处仅作为"答案自己在 uncertainties 第1、3条主动披露了这两处编号差异"的事实记录。
  6. 与本题面指定的氧条件：route_scope.oxygen_condition="aerobic" 与题面 aerobic 一致；4 步中 2 步以 O2 为反应物（S1、S3），与好氧语义相符（化学事实层登记）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，7分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：主链4步与gold骨架吻合，S1/S4获官方卡支持；S2/S4所引EC官方卡为无甲基版本属局部问题（归D3a核验）→第4档取7。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-023-D5 / D5

核查问题：逐一比对原答案的引用与claim_scope，区分可定位、笼统、缺失、待核和已核实错引；LOCAL不自动封顶，关键错引需说明主要结论如何失效。新增证据不能回填原引用。

- 答案具体声称与原文位置：
  - evidence_registry 共 2 条：
    - **EVID_001**：source_type="LITERATURE_DIRECT"、database="PubMed"、record_id=字符串 **"null"**（非 JSON null，字面四字符）、locator="Zylstra & Gibson (1989) J Biol Chem; Finette et al. (1984) — Pseudomonas putida F1 tod pathway genes and enzymes"、claim_scope=["S1 reaction","S2 reaction","S3 reaction","S4 reaction","enzymes","microorganism identity"]、confidence="high"。绑定对象：4 步的 enzyme.evidence_id、microorganism.evidence_id、reaction_evidence_id 全部=EVID_001；organism profile 的 F9_enzyme_activity.evidence_id=EVID_001。
    - **EVID_002**：source_type="DATABASE_DIRECT"、database="ATCC/Bergey's Manual"、record_id="ATCC 700007"、locator="Pseudomonas putida F1 strain record"、claim_scope=["organism identity","F5_culture_collection","F1_oxygen_tolerance","F12_gram_cell_envelope","F2_temperature","F3_pH","F7_carbon_substrate_utilization"]、confidence="medium"。绑定对象：F2/F1/F5/F6/F7/F12 六项性状（F6 的 evidence_id=EVID_002 但 claim_scope 未列 F6——claim_scope 与实际引用范围的差集登记为事实）。
  - 性状引用形态：F2/F1/F5/F3/F6/F7 六项带英文 raw_text（如 F3 raw_text="Grows best near neutral pH (about pH 7)."），F8/F10/F11/F13/F15 五项 evidence_id=null、confidence=medium/high/low 不等（如 F13 confidence="high" 而 evidence_id=null——状态与置信不一致的客观记录）；F9 绑 EVID_001。
  - 因 JSON 损坏点恰在 F6 的 evidence_id 字段，原始交付中该字段值在字节层不可靠（"EVID_002" 后缺引号），修复解析后为 "EVID_002"（登记事实）。

- 量表六状态定义原文摘录（供本人对照，P33–P40）：
  - MISSING_SOURCE：完全无引用，或仅有 INTERNAL_KNOWLEDGE_ONLY 类自我声明。D5按低分档评定；这是缺失而非误导，默认不触发关键错误cap。
  - GENERIC_SOURCE：只有笼统库名/模型名/文献列表，无法定位到条目。"通常评3–4档"仅适用于决策相关组全部仅有笼统来源的情形；存在部分可定位可核对条目级证据时进入5–6档。
  - VERIFIED_MIS_CITATION_LOCAL：经统一冻结证据核实，引用不存在或不支持所声称结论，且不影响该维度主要结论；正常档位内扣分。
  - VERIFIED_MIS_CITATION_CRITICAL：错引落在CORE组且实际推翻相应主要结论，或APPLICATION_CRITICAL组任务条件成立且实际推翻目标筛选/适用性结论；cap≤4。
  - VERIFIED_MIS_CITATION_SYSTEMIC：多项错引、系统性虚构、主要证据链失效或严重误导；cap≤4。
  - UNRESOLVED_SOURCE：引用可疑但当前冻结证据无法核实；保留低分与待核标记；不得冒充已证实错引，不触发cap。
  - （配套）P41 claim-level 登记规则、P39 严重度按预定义表判定、P51 新增证据不回填、P56 单条链接失效不等于虚构。

- 核查来源/新证据ID及支持范围（逐条定位结果）：
  - **EVID_001（PubMed/文献）**：evidence/EVIDENCE_COVERAGE_REGISTER.tsv 的 identifier_type 仅 ACCESSION/CULTURE/EC/TAXID/UNIPROT_ACC 五类，**无 PMID/DOI 类登记行** → 覆盖登记层面无直接行。包内文献卡事实：facts/PUBMED/pubmed_2670929.json = Zylstra G J & Gibson D T, 1989, J Biol Chem 264(25):14940-6, 标题"Toluene degradation by Pseudomonas putida F1. Nucleotide sequence of the todC1C2BADE genes and their expression in Escherichia coli."（DOI 字段=null）；facts/PUBMED/pubmed_6501223.json = Finette B A, Subramanian V, Gibson D T, 1984, J Bacteriol 160(3):1003-9, 标题"Isolation and characterization of Pseudomonas putida PpF1 mutants defective in the toluene dioxygenase enzyme system."。两卡与 locator 文字的作者/年份/期刊对应关系为可登记事实；**答案交付的 record_id="null"、无 PMID/DOI/页码**，从答案记录本身无法唯一定位到条目，定位依赖评分者以 locator 文字匹配包内卡（匹配动作本身属核验，结果由本人登记）。两卡 support_scope_note 均声明"文献存在不等于支持答案的每条子声称，子声称支持范围须评价者比对原文登记"——S1–S4 各步反应级支持范围在包内未经原文比对。
  - **EVID_002（ATCC 700007）**：register 第11行 CULTURE ATCC 700007 = **OUT_OF_SNAPSHOT_UNRESOLVED**、fact_card_path 空、cases_seen=BIOPATH150_021，注"只登记能否定位既有冻结记录；未联网补齐；UNRESOLVED不判虚构也不判支持" → 包内无 ATCC 700007 保藏记录可核；facts/BACDIVE/bacdive_153432.json 的 culture_collection_numbers="CCUG 49576"（非 ATCC 700007，不能互相替代）。EVID_002 claim_scope 内的 F1/F2/F3/F5/F7/F12 各项在包内均无 P. putida F1 菌株级事实卡（153432 为另一株 CCUG 49576，F7 解释层明示面板不可跨株迁移）→ 该条所引对象不可定位，状态素材=UNRESOLVED。
  - **TaxID 183193**：register 第68行 TAXID 183193 = COVERED_BY_FACT_CARD（cases_seen=BIOPATH150_021）；卡内容=Streptomyces sp. DNK-G02。EVID_001 claim_scope 含 "microorganism identity" 而 identity 交付字段（taxid 183193）的官方记录与答案菌名不同属——此为可登记的核验事实；其是否构成"引用存在但不支持所声称结论"及严重度归组（CORE 微生物身份），按 P39/P67/P106–P110 由本人判定。注意 EVID_001 未引用任何 TaxID（其 locator 只提文献），taxid 是答案直接交付字段而非被引条目——"错引"与"字段交付错误"的边界登记待本人裁。
  - **EC 类**：答案 4 个 EC 的 register 状态：1.14.12.11 COVERED（卡 ACTIVE）、1.3.1.86 COVERED（卡 ACTIVE）、1.13.11.2 OUT_OF_SNAPSHOT、3.7.1.5 COVERED（卡 ACTIVE）。3.7.1.5 官方卡 accepted_name=acylpyruvate hydrolase（reaction 与 HOPDA 水解不同底物版本）；答案 uncertainties 第3条已自行披露该卡原始底物为 2-hydroxymuconic semialdehyde。gold 对应 EC 3.7.1.25 卡 ACTIVE、accepted_name=2-hydroxy-6-oxohepta-2,4-dienoate hydrolase。酶-EC 错引的归组与定级属 D3a/D5 交界，材料齐备、判定留本人。

- 关键事实（供本人判断，非结论）：
  1. 交付形态：仅 2 条 evidence 承载全部 4 步反应+酶+菌+6 项性状；无 INTERNAL_KNOWLEDGE_ONLY 条目（与本包其他答案不同，本答案 EVID_001 自报 LITERATURE_DIRECT/high）；record_id 字段值为字符串"null"（EVID_001）——登记为交付事实。
  2. 可定位性盘点（三态素材）：可定位或部分可定位=pubmed_2670929/6501223（卡在包内、需 locator 文字匹配）、EC 1.14.12.11/1.3.1.86/3.7.1.5/1.3.1.19（卡在）；不可定位=ATCC 700007（register OUT_OF_SNAPSHOT）、P. putida F1 菌株级性状 7 项、taxid 183193 官方记录与菌名不符（卡在但内容异属）。"部分关键结论可定位并核对，其他模块仍缺映射"（P35 后半句）所描述的形态是否匹配本答案，由本人判。
  3. claim_scope 完整性差集（客观记录）：EVID_002 实际被 F6 引用但 claim_scope 未列 F6；F8/F10/F11/F13/F15 五性状 evidence_id=null 但 confidence 填了 medium/high（如 F13"不形成芽孢" confidence="high"、无 evidence）——"无来源却高置信"的逐条清单已列，是否触发 R7/D6 语境问题由 D6/本人处理（本条未派 D6，仅登记）。
  4. 题面相关条款：题面第6条要求"没有任何来源时填 null，并把该事实的 confidence 填为 low 或 unknown"——F13（high、evidence_id=null）、F8/F11（medium、evidence_id=null）为与该要求的客观差异点（属任务符合度/D1 语义，登记不判定）。
  5. 量表条款（一句话）：R6/D5 关键错误清单（P98 表 R6）="引用编造；已核实错引且严重度为CRITICAL或SYSTEMIC；来源缺失/笼统达到使主要结论完全不可追查程度且写明失效依据"；P37 关键组身份不自动等于封顶，必须核实且使主要结论失效；P40 UNRESOLVED 不计已核实关键错误；P51 评分者新增证据（如包内文献卡与 locator 的匹配）只用于判卷、不得回填为模型原交付证据；P56 只有核验后才能标虚构，其余用"无法定位/来源不支持该断言"。
  6. 包内证据缺口清单：PMID/DOI 类覆盖登记行、ATCC 700007 冻结记录、P. putida F1 菌株级性状卡、Zylstra 1989 原文全文比对件（卡仅有书目字段，摘要级子声称支持范围不可比）——均无 → 相关子项记 UNRESOLVED/待联网核查。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，4分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：按统一P40口径：ATCC 700007不可定位、pubmed卡仅书目级→低分+待核不cap，档内取4。备注：taxid 183193卡官方名Streptomyces sp.与答案声称P. putida F1异属，错引核实素材已齐备；如按B014同口径可升级为关键错误——本次按统一口径记UNRESOLVED，留本人复核。（把握度：中）

- 本人人工确认与日期：【待本人签】
