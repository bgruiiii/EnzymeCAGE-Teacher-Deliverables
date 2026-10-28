# V04-B-010：定点人工复核

- case：BIOPATH150_016
- 只需核定：D3b。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-010-D3b / D3b

核查问题：分别核对物种/菌株身份、该菌完成所写单步的证据和整条路径能力；身份真实或单步记录不自动证明指定菌株完成全部步骤。

- 范围边界先决事实（本条目必须先登记）：
  - gold/SCOPE_ADDENDUM_BIOPATH150_016.md 原文：第3行"性质：评分范围界定文件（DECISION_016=A，用户2026-10-23确认）"；第5行"必答范围：p-cymene → p-cumate，对应gold线性前3步"（S01 BSY-r00339 → S02 BSY-r00340 → S03 BSY-r00341 止于 p-Cumate）；第9行"背景范围（非必答）：S04–S08（BSY-r00342…r00346，p-cumate下游开环至2-Methylpropanoate与cis-2-Hydroxypenta-2,4-dienoate）仅作为数据库完整链背景信息"；第10行"答案完成至p-cumate即为覆盖题面范围；**不得因未覆盖S04–S08扣D1或D2**…答案若自愿给出下游延续并另行声明不属于评分主链，按四.5四步判断处理其科学内容"；第11行"gold的terminal_compound字段…与题面路线名的不一致已由M3复核登记…该内部不一致不归责模型答案"。
  - 本答案 steps 恰为 3 步、止于 "p-Cumate (4-isopropylbenzoate)"；downstream_continuation[0] 自行声明 "属于本题范围之外的下游途径"（cumA 开环段）。即 D3b 的整条路径能力层按 addendum 口径 = "完成至 p-cumate 的 3 步"，gold 的 S04–S08 下游步不进评分范围（P29/P28）。

- 答案具体声称与原文位置（注：visible_answer.txt 为单行 JSON、无行号，以 JSON 路径定位）：
  - 身份层：steps[*].microorganism（S1/S2/S3 共 3 处）均为 organism_name="Pseudomonas putida"、strain="F1"、**ncbi_taxid=null**、organism_profile_id="ORG_001"、confidence="medium"、evidence_id="EVID_001"。即：声称具体菌株 "F1"，未交付 TaxID。
  - organism_profiles[0]：organism_name="Pseudomonas putida"、strain="F1"、ncbi_taxid=null。15 项性状：有值且挂 EVID_001 的 5 项——F1_oxygen_tolerance="好氧（需氧菌）"（confidence="low"）、F6_respiration_electron_acceptor="好氧呼吸/O2"（low）、F7_carbon_substrate_utilization="可利用对伞花烃（p-cymene）作为唯一碳源与能源"（confidence="medium"）、F8_degradation_capacity_broad="可降解芳香烃类（如对伞花烃、甲苯等）及其衍生物"（low）、F9_enzyme_activity="具有对伞花烃单加氧酶（CymA）及相应醇/醛脱氢酶（CymB、CymC）活性"（medium）；有值但 evidence_id=null 的 6 项（confidence 全 "low"）——F10"运动（极生多鞭毛）"、F11"杆状"、F12"革兰氏阴性，外膜包膜"、F13"不产芽孢"、F14_genome_basic.genome_accession="NC_009512"、F15"广泛存在于土壤、水体等环境的广适性腐生菌"；null/unknown 4 项（F2/F3/F4/F5）。
  - 反应级层：3 步 microorganism 全部绑定 ORG_001（steps[0..2].microorganism.organism_profile_id="ORG_001"）。
  - 完整路径层：complete_pathway_organism_profile_id="ORG_001"；route_summary 末句"典型菌株为 Pseudomonas putida F1"；central_metabolism_entry.explanation "本路线止于 p-cumate；p-cumate 可进一步经 cumA 加双氧酶开环进入 central metabolism，但超出本题路线范围。"
  - 证据：evidence_registry 仅 1 条 EVID_001：source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null、claim_scope=["p-cymene 甲基氧化为 p-cumate 的三步反应","Pseudomonas putida F1 含 cymA/cymB/cymC 基因","菌株生理性状"]、confidence="medium"。
  - 披露：uncertainties 共 3 条——[0]"各步酶的精确 EC 编号未确认，部分填写 null 或类级别编号"；[1]"Pseudomonas putida F1 的 NCBI TaxID、保藏号及多数生理性状数值未能从可靠来源确认，均填 null"；[2]"理化性状部分基于对假单胞菌属的通用知识，置信度较低"。
- 核查来源/新证据ID及支持范围：
  - gold/organism_gold.tsv（BIOPATH150_016，STEP 级行，S01–S03 为必答范围）：
    - S01 行含 **Pseudomonas putida F1（taxid 351746，EXACT，酶 BSY-e04004 "p-cymene methyl hydroxylase"，EC 1.14.13.-）**，另有 Pseudomonas putida（303，酶 e00238 EC 1.14.15.25 / e04004）、Pseudomonas putida PL（No TaxID）、Pseudomonas sp. gs1（644631）。
    - S02 行仅两个菌：Pseudomonas putida（303，酶 e00239 "p-cumic alcohol dehydrogenase" EC 1.1.1.M33）与 Sphingobium japonicum（332055，酶 e04283 EC 1.1.1.-）。**S02 行无 351746（F1）登记**。
    - S03 行含多条 351746（F1）：e00121（EC 1.2.1.28）、e00127（EC 1.2.1.28）、e00246（EC 1.2.1.29）、e00615（EC 1.2.1.3）等 aldehyde dehydrogenase 条目；另登记 303、PL、mt-2、HR199、gs1、Rhodococcus jostii 等大量其他菌。
    - PATHWAY_COMPLETE 4 行：303（genome GCA_024508115.1，pathway_complete=TRUE、download_available=TRUE）、**351746（pathway_complete=TRUE、download_available=FALSE）**、No TaxID（PL，TRUE）、644631（gs1，TRUE）。
    - 支持范围：gold 把 P. putida F1（351746）登记为 S01 与 S03 的步级菌、并登记为该路线 pathway_complete=TRUE；不支持范围：gold 非穷举（量表 P27、P54）；S02 行无 F1 是 gold 登记状态，非对答案的反证；gold PATHWAY_COMPLETE 与题面终点的不一致已由 addendum 第11行登记为不归责答案。
  - facts/EUROPE_PMC/epmc_PMC179094.json（record_status="CURRENT"）：title="p-Cymene catabolic pathway in Pseudomonas putida F1: cloning and characterization of DNA encoding conversion of p-cymene to p-cumate."。支持范围：包内冻结文献卡，标题直接涉及"该菌将 p-cymene 转化为 p-cumate"的整条范围内容（身份+转化方向的包内支持候选）；不支持范围：答案 evidence_registry 未引用该文献（EVID_001 为 INTERNAL_KNOWLEDGE_ONLY、locator=null），卡片存在不自动并入答案证据；support_scope 逐条比对由评价者自行登记。
  - facts/NCBI_TAXONOMY/taxid_351746.json（register 第75行 COVERED_BY_FACT_CARD，cases_seen=BIOPATH150_016;BIOPATH150_021）：record_status="CURRENT"、names.scientific_name="Pseudomonas putida F1"。支持范围：该 TaxID 的官方学名记录与 "Pseudomonas putida F1" 一致（菌株级记录）；不支持范围：**答案 ncbi_taxid=null，无编号可核**——该卡不构成对答案 taxid 字段的核验（P71 核验对象是答案交付的编号）；support_scope_note 明写"不自动支持任何身份或能力声称"。另：该卡解析体中无 rank/lineage 字段（names 仅 scientific_name/other_names=[]，organism=null）→ P67 要求的三项中 rank/lineage 在本卡不可得（事实）；taxid_303.json 是 Pseudomonas putida（物种级，另有类型材料 ATCC 12633 等 other_names）。
  - facts/NCBI_NUCCORE/nuccore_NC_009512.1.json（register 第7/8行 COVERED_BY_FACT_CARD，cases_seen=BIOPATH150_016;…）：record_status="**SUPPRESSED**"、definition="Pseudomonas putida F1, complete sequence."、organism.taxid=351746。与答案的对应：答案 F14 写 "NC_009512"（无 .1，register 以 ACCESSION NC_009512 登记，第7行，cases_seen 含 BIOPATH150_016）指向同一卡。支持范围：该登录号对应 P. putida F1 基因组；不支持范围：答案 F14 的 evidence_id=null、confidence="low"，且 uncertainties[1] 同时声明"保藏号…未能从可靠来源确认，均填 null"（与 F14 实际写了 NC_009512 并存的事实）。
  - facts/PUBMED/pubmed_2670929.json、pubmed_6501223.json：P. putida F1 的 toluene tod 系统文献卡——支持 F1 菌株真实存在与芳香烃代谢背景；不支持 p-cymene 逐步/整路径声称本身。facts/BACDIVE/bacdive_12880.json：P. putida mt-2（PaW1）——同种异菌株记录。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv（12 行）：无 "Pseudomonas putida" 行 → 无别名核对需求/支持。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：答案 taxid=null → 无 TAXID 登记行；无 F1 专属覆盖行。
- 关键事实（供本人判断，非结论）：
  1. 三层声称各有原文：身份层=steps[*].microorganism + organism_profiles[0]（物种名+strain="F1"，taxid=null）；反应级层=3 步各绑定 ORG_001；完整路径层=complete_pathway_organism_profile_id="ORG_001" + route_summary 末句。范围边界：per addendum，完整路径层="p-cymene→p-cumate 前 3 步"，S04–S08 不进评分（第9–10行原文已引）。
  2. 身份层核验状态（事实）：taxid=null → P71/P67 编号核验无对象；包内同时存在与所写菌株名一致的官方记录（taxid_351746 卡 "Pseudomonas putida F1"，CURRENT），但卡无 rank/lineage 字段；crosswalk 无需别名映射（名称直写）。
  3. 反应级层核验状态（事实）：gold S01、S03 行有 351746；S02 行无 351746（仅 303 与 Sphingobium japonicum）；S03 的 gold 条目含 EC 1.2.1.3（答案 S3 的 EC 也是 1.2.1.3，属 D3a 范围，此处只登记 gold 有该 EC×351746 组合行）。包内另有 PMC179094 文献卡标题覆盖 "p-cymene → p-cumate by F1"；答案未引用之。
  4. 完整路径层核验状态（事实）：gold PATHWAY_COMPLETE 行 taxid=351746 pathway_complete=TRUE（download_available=FALSE）——gold 把 F1 登记为该路线全路径菌（必答范围至 p-cumate 口径下，与答案 complete_pathway 声称同向）；gold 非穷举，登记本身不自动等于逐字核验答案能力声称（P72）。
  5. R4/D3b 关键错误清单（P175 行 R4）："物种/菌株或TaxID编造；由基因组存在某酶直接推断完成整条路径；把仅支持单步的菌写成全路径菌"。事实铺垫：taxid=null → "TaxID编造"无核验对象；答案证据链中无基因组编号支撑能力声称（F14 的 NC_009512 挂在性状、evidence_id=null），EVID_001 claim_scope 明写"F1 含 cymA/cymB/cymC 基因"+"三步反应"两条并置——是否构成"由基因存在推断整条路径"由本人定。
  6. P106–P110 身份阶梯适用前提是先取得官方核实结论；本答案 taxid=null、包内无针对答案交付编号的核验 → 尚无可套用的编号核实结论（事实铺垫，不预判档位）。P69 三层分别核对；P72 核验只给事实状态。
  7. 答案自身披露：EVID_001 为 INTERNAL_KNOWLEDGE_ONLY（locator=null）、claim_scope 明确覆盖三层声称；microorganism confidence="medium"；uncertainties[1] 明写 TaxID/保藏号/多数性状数值未确认填 null；uncertainties[2] 明写属级通用知识置信低；6 项性状值（F10–F15）有值但 evidence_id=null 且标 low（值与证据分离的登记事实）。
  8. 包内证据缺口清单：F1 菌株身份的保藏号/测序号核验（答案未交付编号）、F1 完成各步的独立实验证据卡（PMC179094 为文献卡，其正文细节不在卡内字段）、S02 步的 F1 步级 gold 行——按 gold 现值 S02 无 351746 登记；上述缺口中"联网可补"部分记 UNRESOLVED、待联网核查。

- 复核结论（保留/修改/仍待核）：保留（RETAIN）
- score_status及分数（NE/NA不猜分）：SCORED，8分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：TaxID 351746官方rank/lineage补齐（no rank，lineage至P. putida）；PMC179094官方开放全文：F1经p-cumate利用p-cymene、cym操纵子六基因、基因产物经功能实验鉴定（S1–S3逐步对应）；cymAa/cymAb两亚基与答案单写cymA属字面差异，登记不判错。支持充分、小瑕疵→取8。（把握度：高）

- 本人人工确认与日期：【待本人签】
