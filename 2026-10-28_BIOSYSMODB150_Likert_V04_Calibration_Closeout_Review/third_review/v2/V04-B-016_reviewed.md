# V04-B-016：定点人工复核

- case：BIOPATH150_146
- 只需核定：D3a。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-016-D3a / D3a

核查问题：核对所写酶名、具体EC和该步反应是否对应；通配EC、近名酶或家族关系不能证明具体催化。缺证时保留待核，不凭负检索判酶不存在。

- 答案具体声称与原文位置：
  - 原文定位说明（事实）：items/V04-B-016/visible_answer.txt 是**单行 JSON**（全文 1 行、5727 字符），故按 JSON 字段路径 + 字符偏移定位；engineering_status.json：engineering_class="INVALID_JSON"、machine_readable=false、finish_reason="stop"；json.loads 在字符 3944 报 "Expecting value"，缺陷为 F7_carbon_substrate_utilization.evidence_id 写成未加引号的 `EVID_placeholder`（字符约 3943 起）——该缺陷只涉及 F7 性状证据字段，不涉及本维酶字段（事实陈述，处置属 D1/技术痕迹条款）。
  - steps[0].enzyme（S1，字符约 838–947）：name="sulfoquinovose isomerase SulA"（字符 838）、ec_number="5.3.1.31"（877）、gene_or_protein="sulA"（900）、confidence="medium"（925）、evidence_id="EVID_001"（947）；对应反应：reaction_type="ketose-aldose isomerization"，底物 6-sulfo-D-quinovose "OCC1OC(O)C(O)C(O)C1CS(O)(=O)=O" → 产物 6-deoxy-6-sulfo-D-fructose "OCC1(O)C(O)C(O)C(CS(O)(=O)=O)O1"；step.uncertainty=null（字符 1199）。
  - steps[1].enzyme（S2，字符约 1609–1725）：name="6-deoxy-6-sulfofructose aldolase SulD"（1609）、ec_number="4.1.2.-"（1656，**通配号**）、gene_or_protein="sulD"（1678）、confidence="medium"（1703）、evidence_id="EVID_001"（1725）；对应反应：reaction_type="aldol cleavage"，底物仅 6-deoxy-6-sulfo-D-fructose → 产物 dihydroxyacetone phosphate "O=P(O)(O)OCC(O)CO" + 2-sulfoacetaldehyde "OCCS(O)(=O)=O"；step.uncertainty=null（字符 1977）。
  - steps[2].enzyme（S3，字符约 2433–2549）：name="sulfoacetaldehyde acetyltransferase SulX"（2433）、ec_number="2.3.1.-"（2483，**通配号**）、gene_or_protein="sulX"（2505）、confidence="low"（2530）、evidence_id="EVID_001"（2549）；对应反应：reaction_type="phosphotransacetylation with desulfonation"，2-sulfoacetaldehyde + phosphate（cofactor）→ acetyl phosphate + sulfite（byproduct）；step.uncertainty（steps[2] 尾部字段）原文："SulX催化2-磺基乙醛生成乙酰磷酸并释放亚磺酸盐的具体EC编号与底物细节存在不确定性"。
  - 其余酶名出现处：route_summary（字段字符 356–492）中文写"磺酸奎诺糖异构酶（SulA）……磺酸果糖醛缩酶（SulD）……磺基乙醛磷酸转移酶"；organism_profiles[0].traits.F9_enzyme_activity.value="磺酸奎诺糖异构酶（SulA）与磺酸果糖醛缩酶（SulD）活性，可降解磺酸基奎诺糖"（字段字符 4086–4212），confidence="low"、evidence_id=null。
  - evidence_registry[0]（字符约 5240–5580）：evidence_id="EVID_001"（5250）、source_type="LITERATURE_DIRECT"（5275）、database=null、record_id=null、locator="Frommer W D, et al. sulfoquinovose degradation by Pseudomonas putida SQ1; sulfoquinovose catabolic gene cluster (sulA/sulD/sulX)"、claim_scope=["pathway steps S1-S3","organism identity","substrates and products"]、confidence="medium"（5567）。
  - uncertainties 数组（字符 5591 起）共 3 条，含第 2 条："路线编号VI与各sulfoquinovose降解分支（I-VI）的边界在文献中不完全一致，本答案按磺糖酵解主链填写"；第 3 条为 SMILES 示意性声明。

- 核查来源/新证据ID及支持范围：
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：EC **5.3.1.31 → COVERED_BY_FACT_CARD**、fact_card_path=facts/IUBMB_EXPLORENZ/ec_5.3.1.31.json、cases_seen=BIOPATH150_146、note"只登记能否定位既有冻结记录；未联网补齐；UNRESOLVED不判虚构也不判支持"。支持范围：该编号在本快照可核；不支持范围：不评价答案。
  - 通配号 4.1.2.- 与 2.3.1.-：register 54 行 EC 全为具体号，**无对应行**（无编号核验对象）→ 按 P73，通配号本身不能反推任何具体号正确，本条也不产生"编号错配"事实。
  - facts/IUBMB_EXPLORENZ/ec_5.3.1.31.json：accepted_name="sulfoquinovose isomerase"；systematic_name="6-deoxy-6-sulfo-β-D-glucopyranose aldose-ketose-isomerase"；reaction="(1) β-sulfoquinovose = 6-deoxy-6-sulfo-D-fructose (2) β-sulfoquinovose = 6-sulfo-D-rhamnose"；record_status=ACTIVE；other_names=["yihS (gene name)"]；replacement_history=["created 5.3.1.31 2014, modified 2022"]；support_scope_note 明写"不自动支持或反驳任何答案声称，评价者须逐项比对后自行登记 FACT_VERIFICATION_STATUS"。支持范围：官方酶名、反应式、条目状态与历史；不支持范围：基因名 SulA（卡内 other_names 只列 yihS）、菌归属、路线归属。
  - facts/IUBMB_EXPLORENZ/ec_4.1.2.57.json（gold 侧醛缩步卡）：accepted_name="sulfofructosephosphate aldolase"、reaction="6-deoxy-6-sulfo-D-fructose 1-phosphate = glycerone phosphate + (2S)-3-sulfolactaldehyde"、other_names=["yihT (gene name)"]、ACTIVE。支持范围：gold 醛缩步所用编号的官方底物与产物；不支持范围：该卡不涉及答案 S2 的未磷酸化底物写法，故既不支持也不反驳它。
  - facts/IUBMB_EXPLORENZ/ec_2.7.1.184.json（gold 磷酸化步卡）：accepted_name="sulfofructose kinase"、reaction="ATP + 6-deoxy-6-sulfo-D-fructose = ADP + 6-deoxy-6-sulfo-D-fructose 1-phosphate"、ACTIVE。支持范围：gold 有该激酶步；不支持范围：不判答案省略该步为错。
  - gold/enzyme_gold.tsv（BIOPATH150_146 / BSY-p00985）：S05 sulfoquinovose isomerase（BSY-e03759/03760/03761/03762，EC-5.3.1.31）；S01 6-deoxy-6-sulfofructose kinase 与 sulfofructose kinase（EC-2.7.1.184）；S03 6-deoxy-6-sulfofructose-1-phosphate aldolase 与 sulfofructosephosphate aldolase（EC-4.1.2.57）；S02 3-sulfolactaldehyde dehydrogenase（EC-1.2.1.97）；S04 3-sulfolactate exporter（ec_number_normalized=NOT_OBSERVED）。支持范围：gold 各步酶名/EC 登记。
  - gold/reaction_gold.tsv 对照事实：gold S03 醛缩步底物为 6-deoxy-6-sulfo-D-fructose 1-phosphate、主产物 (2S)-3-sulfolactaldehyde + glycerone phosphate（BYPRODUCT）；gold S01 为 ATP→ADP 磷酸化；gold 无"2-sulfoacetaldehyde / acetyl phosphate"中间体。
  - 包内检索（零网络）：facts/ 全树 grep "sulfoquinovose|Frommer|SQ1|sulfoacetaldehyde|yihS" 仅命中 ec_5.3.1.31.json 一个文件；facts/PUBMED/（6501223 甲苯论文、2670929 甲苯 tod 基因簇）与 facts/EUROPE_PMC/（PMC179094 对枯烯论文）均与 Frommer / Pseudomonas putida SQ1 无关 → 答案 EVID_001 的 locator 在包内**无法定位**（无书目卡、register 无行）→ 记 UNRESOLVED，不判虚构（P40、P56）。
  - facts/NCBI_TAXONOMY/taxid_303.json：scientific_name="Pseudomonas putida"、record_status=CURRENT（本维只涉及酶，菌身份归 D3b，此处仅登记该卡存在）。

- 关键事实（供本人判断，非结论）：
  1. 三条酶条目清单：S1 具体号 5.3.1.31（medium）、S2 通配号 4.1.2.-（medium）、S3 通配号 2.3.1.-（low）；S1/S2 的 step.uncertainty=null，S3 自带 step.uncertainty 明确写"具体EC编号与底物细节存在不确定性"；三条 evidence_id 均为 EVID_001。
  2. S1 与官方卡逐项对位（事实）：ec_number="5.3.1.31" 与卡 record_id 一致、record_status=ACTIVE；name 去掉基因后缀"sulfoquinovose isomerase"与 accepted_name **逐字一致**；S1 底物→产物（6-sulfo-D-quinovose → 6-deoxy-6-sulfo-D-fructose）与卡 reaction (1) 对应；卡另列 reaction (2)（β-sulfoquinovose = 6-sulfo-D-rhamnose），答案未涉及。→ 本步"酶名/具体EC/反应"三项在包内均有直接支持卡。
  3. S1 的基因名事实：答案 gene_or_protein="sulA"，而 ec_5.3.1.31 卡 other_names 只列 "yihS (gene name)" → 包内无 SulA 覆盖（也不构成否定证据）→ 基因名一项 UNRESOLVED、待联网核查。
  4. S2 的对位事实：答案未交付具体号（4.1.2.-），按 P73 无编号可核；gold 同段醛缩步官方卡 4.1.2.57 的反应底物是**6-deoxy-6-sulfo-D-fructose 1-phosphate**、产物是 glycerone phosphate + (2S)-3-sulfolactaldehyde，而答案 S2 底物为未磷酸化 6-deoxy-6-sulfo-D-fructose、产物为 dihydroxyacetone phosphate + 2-sulfoacetaldehyde（底物与产物命名两侧均不同）；另事实：答案全 3 步中没有 gold 的 ATP 磷酸化步（gold S01 / EC 2.7.1.184）。→ 包内无任何"未磷酸化 sulfofructose 醛缩酶"条目可核该酶-反应对应 → 记 UNRESOLVED。是否按 P66（gold 单值与答案冲突先核官方条目）处理，取决于先认定"是否同一步同一反应"（事实铺垫，判断留本人）。
  5. S3 的对位事实：通配号 2.3.1.- 无核验对象；酶名"sulfoacetaldehyde acetyltransferase SulX"与基因名 sulX 在包内零覆盖（全树 grep 无命中）；答案自身标 confidence="low" 并写入 step.uncertainty 披露 EC 与底物细节不确定。
  6. 证据链事实：EVID_001 source_type="LITERATURE_DIRECT" 但 database=null、record_id=null、locator 为文字描述（作者 + 路线 + sulA/sulD/sulX 基因簇），claim_scope 含 "pathway steps S1-S3"；包内无该文献任何书目卡 → 按 P40 属"引用可疑但冻结证据无法核实"→ UNRESOLVED，不得冒充已证实错引。
  7. 量表条款（一句话）：R3/D3a 关键错误清单（P98 表 R3）="EC大类别与反应类型不匹配；酶名与EC互相矛盾；把广谱家族相关性当成该具体反应的催化证据"；四.6/P71 要求以具体 EC 交付者先核 accepted name/reaction/状态（本条仅 S1 有具体号且包内卡齐）、P72 核验只给三态不自动给分或cap、P73 通配不反推；P63–P66 为 gold 通配/多注与单值冲突的保守处理顺序。
  8. 包内证据缺口清单（一律待联网核查/UNRESOLVED）：SulA/SulD/SulX 基因名、4.1.2.- 与 2.3.1.- 所指具体酶、未磷酸化 sulfofructose 醛缩酶条目、sulfoacetaldehyde acetyltransferase 酶名、Frommer 等 SQ1 文献书目（locator 无法定位）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，4分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：官方命中：yihS=SQ异构酶基因名（UniProt P32140，EC 5.3.1.31）、SQ1原始文献真实（Felux 2015 PNAS+DSM 100120）、sulfoacetaldehyde acetyltransferase=EC 2.3.3.15（other name Xsc）；未检出：sulA/sulD/sulX三基因名在UniProt/文献/综述全库零命中、答案EVID_001作者'Frommer W D'未检出（最接近Frommeyer B 2020，主题不同）。按P27/P54负检索不判虚构→未证实登记→取4。（把握度：高）

- 本人人工确认与日期：【待本人签】
