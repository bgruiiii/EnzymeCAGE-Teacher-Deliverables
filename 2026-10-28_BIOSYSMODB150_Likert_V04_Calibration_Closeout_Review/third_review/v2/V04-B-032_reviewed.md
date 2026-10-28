# V04-B-032：定点人工复核

- case：BIOPATH150_029
- 只需核定：D2、D6。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-032-D2 / D2

核查问题：逐步核对主底物到主产物的化学转化、方向和连续性。若可能是替代路线，先分清任务符合度与所写反应本身是否成立；检索无结果不等于反应不可能。

- 答案具体声称与原文位置（visible_answer.txt，行号为该文件行号）：
  - route_scope（第6–11行）：oxygen_condition=null；chosen_route_name="cyclohexanol degradation"；is_single_continuous_route=true；notes=null。
  - route_summary（第12行）：声称"环己醇经环己醇脱氢酶氧化为环己酮，再经环己酮单加氧酶进行Baeyer-Villiger氧化生成ε-己内酯，随后水解、氧化生成己二酸，进而通过β-氧化途径转化为琥珀酰辅酶A和乙酰辅酶A进入中心代谢。"
  - steps 共10步（第13–408行），branch_id 全部为 null，predecessor_step_ids 顺序链接，alternative_branches=[]（第522行），downstream_continuation=[]（第521行）：
    - S1（第13–52行）：Cyclohexanol "OC1CCCCC1"（main）→ Cyclohexanone "O=C1CCCCC1"（main）；reaction_type="oxidation"；酶 Cyclohexanol dehydrogenase，EC "1.1.1.245"，confidence="high"（第38行）；未列任何辅因子成员。
    - S2（第53–91行）：Cyclohexanone "O=C1CCCCC1" → ε-Caprolactone "O=C1CCCCCO1"；reaction_type="Baeyer-Villiger oxidation"；酶 Cyclohexanone monooxygenase，EC "1.14.13.22"，"high"；未列 NADPH/O2→NADP+/H2O。
    - S3（第92–130行）：ε-Caprolactone → 6-Hydroxyhexanoic acid "OCCCCCC(=O)O"；reaction_type="hydrolysis"；酶 6-Hexanolactone lactonohydrolase，EC "3.1.1.25"，"medium"；未列水。
    - S4（第131–169行）：6-Hydroxyhexanoic acid → 6-Oxohexanoic acid "O=CCCCCC(=O)O"；"oxidation"；酶 6-Hydroxyhexanoate dehydrogenase，EC "1.1.1.258"，"medium"；未列 NAD+/NADH。
    - S5（第170–208行）：6-Oxohexanoic acid "O=CCCCCC(=O)O" → Adipic acid "O=C(O)CCCC(=O)O"；"oxidation"；酶 6-Oxohexanoate dehydrogenase，EC "1.2.1.63"，"medium"；未列 H2O/NADP+/NADPH。
    - S6（第209–247行）：Adipic acid → Adipyl-CoA（smiles=null，第224行）；"CoA activation"；酶 Adipate-CoA ligase，EC "6.2.1.14"，"medium"；未列 CoA/ATP。
    - S7（第248–286行）：Adipyl-CoA（null）→ 2,3-Dehydroadipyl-CoA（null）；"oxidation"；Adipyl-CoA dehydrogenase，EC "1.3.8.7"。
    - S8（第287–325行）：→ 3-Hydroxyadipyl-CoA（null）；"hydration"；Enoyl-CoA hydratase，EC "4.2.1.17"。
    - S9（第326–364行）：→ 3-Oxoadipyl-CoA（null）；"oxidation"；3-Hydroxyadipyl-CoA dehydrogenase，EC "1.1.1.259"。
    - S10（第365–408行）：3-Oxoadipyl-CoA（null）→ Succinyl-CoA（null）+ Acetyl-CoA（null），两个产物 role 均为 "main"（第377–388行）；"thiolysis"；β-Ketoadipyl-CoA thiolase，EC "2.3.1.16"。
  - central_metabolism_entry（第517–520行）：products=["Succinyl-CoA","Acetyl-CoA"]，"这两个产物进入三羧酸循环。"
  - 全部10步 uncertainty=null（如第51、90、129行等）；顶层 uncertainties=[]（第624行）。
  - 每步 microorganism 均为 Acinetobacter calcoaceticus / NCIMB 9871 / ncbi_taxid 471 / ORG_001，confidence="high"（如第41–48行）。
- 核查来源/新证据ID及支持范围：
  - gold/reaction_gold.tsv BIOPATH150_029（第115–141行；路线 BSY-p00274）：S1 BSY-r00139 Cyclohexanol+NAD+→Cyclohexanone+NADH+H+（forward, SUBSTRATE_TO_PRODUCT）；S2 BSY-r00140 Cyclohexanone+NADPH+H++dioxygen→Caprolactone+NADP++H2O；S3 BSY-r00141 Caprolactone+H2O→H++6-Hydroxyhexanoate（羧酸根式，canonicalsmiles C(CCC(=O)[O-])CCO；其中 H2O 在库内挂在一个名为"Uranium(2+);dihydroxide"的条目下、identity 为 token H2O——库内数据怪相，照录）；S4 BSY-r00146 6-Hydroxyhexanoate+NAD+→H++6-Oxohexanoate+NADH；S5 BSY-r00147 6-Oxohexanoate+H2O+NADP+→H++Adipate（羧酸根式 C(CCC(=O)[O-])CC(=O)[O-]）+NADPH。支持：gold主链为5步、终点=Adipate；不支持：gold 链内无任何 CoA 活化或 β-氧化步，无第6步及以后内容。
  - gold/formal_cases.tsv（BIOPATH150_029 行）：ordered_step_count=5、final_graph_status=LINEAR_UNIQUE；gold/case_root_identity.tsv：pathway_name="cyclohexanol degradation"，root=Cyclohexanol，terminal_compound_names=Adipate，aerobic_or_anaerobic="No data"。支持：gold 路线名、步数、终点、氧条件登记事实。
  - gold/enzyme_gold.tsv（BIOPATH150_029）：S1 cyclohexanol dehydrogenase EC 1.1.1.245；S2 cyclohexanone monooxygenase EC 1.14.13.22；S3 两条酶注 "6-hexanolide hydrolase" EC-3.1.1（通配）与 "1-oxa-2-oxocycloheptane lactonase" EC-3.1.1.-（通配）；S4 6-hydroxyhexanoate dehydrogenase EC 1.1.1.258；S5 两条酶注均 6-oxohexanoate dehydrogenase EC-1.2.1.63（KEGG 注 R05099）。支持：S1/S2/S4/S5 答案酶名与 EC 与 gold 逐字对应（仅大小写差异）；S3 的 gold EC 为通配（量表 P63–P65 的适用场景事实）。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：答案所用全部10个 EC（1.1.1.245 第17行、1.14.13.22 第30行、3.1.1.25 第47行、1.1.1.258 第18行、1.2.1.63 第36行、6.2.1.14 第67行、1.3.8.7 第41行、4.2.1.17 第60行、1.1.1.259 第19行、2.3.1.16 第42行）均登记 OUT_OF_SNAPSHOT_UNRESOLVED；TAXID 471 亦 OUT_OF_SNAPSHOT_UNRESOLVED（第77行）。支持：包内对这些编号无冻结事实卡可核（P71 编号核验在包内无法完成）；不支持：UNRESOLVED 既不判虚构也不判支持。
  - evidence/facts/ 目录：无上述 EC 的 IUBMB_EXPLORENZ 事实卡（该目录仅含 1.14.12.11 等其他 case 的卡）。支持：S5 等步的"酶 accepted name/reaction 对应"在包内无法核验，记 UNRESOLVED，待联网核查。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv："Acinetobacter sp. NCIB 9871"→reviewed_species Acinetobacter johnsonii（taxid 40214，scope=SPECIES_IDENTITY_ONLY_RETAIN_STRAIN_TOKEN）；EVIDENCE_COVERAGE_REGISTER 第12–13行把 NCIB 9871 与 NCIMB 9871 都登记指向该 crosswalk（crosswalk 文件内只有含"NCIB 9871"的行，无含"NCIMB"字串的行）。支持：该保藏号的物种级映射事实；不支持：不认证菌株级身份与降解能力（属 D3b 范围，此处仅登记）。
  - 答案自带证据：evidence_registry 共11条（第523–623行），全部 source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null，locator 为自由文本。支持：答案未声称任何数据库/文献直引。
  - 量表条款（rubric/LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1_TEXT_EXTRACT.txt）：P57–P62（四步判断）、P63–P65（通配EC保守条款）、P100（D1/D2边界）、P103–P105（辅因子与简化反应式）、P28–P29（题面范围边界）。
- 关键事实（供本人判断，非结论）：
  1. 逐步化学对照（答案前5步 vs gold 5步）：主底物/主产物逐一对应且方向一致——cyclohexanol→cyclohexanone（同S1）、cyclohexanone→caprolactone（同S2，BV氧化=gold的单加氧转化）、caprolactone→6-hydroxyhexanoate类（同S3，水解）、6-hydroxyhexanoate→6-oxohexanoate（同S4）、6-oxohexanoate→adipate类（同S5）。差异三点：①答案S1–S5均未列辅因子/水（gold每步均列 NAD(H)/NADPH(NADP+)/O2/H2O）；②答案产物写酸式（"6-Hydroxyhexanoic acid"、"Adipic acid"），gold 写羧酸根阴离子（6-Hydroxyhexanoate、Adipate）；③S3 答案给具体 EC 3.1.1.25，gold 该步为通配 EC 3.1.1 / 3.1.1.-。
  2. 原子数目客观核对（按答案 SMILES 计分子式）：S1 C6H12O→C6H10O（净失2H）；S2 C6H10O→C6H10O2（净增1O）；S3 C6H10O2→C6H12O3（净增H2O）；S4 C6H12O3→C6H10O3（净失2H）；S5 C6H10O3→C6H10O4（净增1O）。S1–S5 碳数均保持 C6；S10 主链碳骨架 C6→C4+C2。S6–S9 主产物 SMILES 全为 null，CoA 基团无结构，无法做原子核对。
  3. 连续性客观核对：S1–S10 每步主底物与上一步主产物的 name/SMILES 字符串一致（如 S2 产物 "O=C1CCCCCO1" = S3 底物同串；S5 产物 "Adipic acid" = S6 底物同名），predecessor_step_ids 链条完整（S2←S1…S10←S9），答案未声明任何反向或分叉步。
  4. 范围事实：gold 主链5步、终点 Adipate；答案 S6–S10（CoA活化→脱氢→水合→脱氢→硫解→Succinyl-CoA+Acetyl-CoA）为 gold 链之外的5步延伸。题面（question.json）只给路线范围 "cyclohexanol degradation"，未指定终点化合物、中间体或步数；但答案 route_summary（第12行）明确预告了该延伸。按 P28/P29 登记事实：P29 的"题面指定了具体终点"前提在本题不成立（题面未指定终点），本情形是"答案延伸超出 gold 终点"，条款如何适用由本人判断。
  5. 四步判断（P57–P62）事实铺陈：①题面已指定路线名（"cyclohexanol degradation"，与 gold pathway_name 逐字符相同），未指定终点；②答案未声明替代路线——chosen_route_name 原样填写、is_single_continuous_route=true、notes=null、alternative_branches=[]、uncertainties=[]、10步 uncertainty 全 null，全文无"替代/偏离"字样，也未披露与 gold 的任何差异；③可核证据：答案11条证据全为 INTERNAL_KNOWLEDGE_ONLY，包内对全部10个 EC 无冻结事实卡（OUT_OF_SNAPSHOT_UNRESOLVED）；gold 本身支持 S1–S5 的主链转化与 S1/S2/S4/S5 的酶名+EC；④偏离是否使该维度主要结论失效：是（关键错误，见复核结论）。
  6. 检索边界：包内对 S3 具体号 3.1.1.25 及 S6–S10 各 EC 无冻结卡——"检索无结果不等于反应不可能"，这些酶-反应对应与 S6–S10 延伸化学是否成立，包内无法证实也无法证伪，待联网核查/记 UNRESOLVED。
  7. D1/D2 边界事实（P100）：答案未更换题面路线名、未改题面氧条件（题面 null→答案 null）；route_scope 任务参数与题面一致。若本人认定另有任务参数偏离，其 D1 后果须独立判定，本底稿不评 D1（不连坐，P22）。
- 复核结论（保留/修改/仍待核）：保留（RETAIN）
- score_status及分数（NE/NA不猜分）：SCORED，8分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：S1–S5获gold主链与酶名/EC支持，官卡可核部分相符；S6–S10为gold链外延伸，题面未指定终点，按P29不计分；S3 EC 3.1.1.25不可核属局部→第4–5档取8。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-032-D6 / D6

核查问题：核对原答案置信标签、null/未知和不确定性披露；区分单点过度确信与系统性误导，不因其他维度错误自动封顶，不把重复引用同一断言算多个独立事件。

- 答案具体声称与原文位置（visible_answer.txt）：
  - confidence 标签分布：enzyme——"high" 2处（S1 第38行、S2 第77行），"medium" 8处（S3–S10，如第116、155、194行等）；microorganism——"high" 10处（S1–S10 全部，如第46行）；organism_profiles.traits——"high" 3项（F5_culture_collection 第448行、F9_enzyme_activity 第475行、F12_gram_cell_envelope 第493行）、"medium" 8项（F1 第427行、F6 第457行、F7 第463行、F8 第469行、F10、F11、F13、F15）、"unknown" 4项（F2_temperature 第421行、F4_salinity 第433行、F3_pH 第439行、F14_genome_basic 第505行）、"low" 0项；evidence_registry——EVID_003 "high"（第549行），其余10条 "medium"。全部15项性状 raw_text=null。
  - 未知披露：4项性状 value=null+evidence_id=null+confidence="unknown"（F2/F4/F3 第417–440行、F14 第501–506行）；步骤级 uncertainty 全部 null（第51、90、129、168、207、246、285、324、363、407行）；顶层 uncertainties=[]（第624行）。
  - source_type 事实信号：evidence_registry 11条全部 "INTERNAL_KNOWLEDGE_ONLY"（第526、535、544、553、562、571、580、589、598、607、616行），database=null、record_id=null，locator 为自由文本（如第529行 "Acinetobacter calcoaceticus NCIMB 9871 general microbiology"、第538行 "cyclohexanol dehydrogenase reaction"）。
  - 身份相关高置信声称：第41–48行 organism_name="Acinetobacter calcoaceticus"、strain="NCIMB 9871"、ncbi_taxid=471、confidence="high"；F5_culture_collection value={collection:"NCIMB",accession:"9871"}、confidence="high"（第441–449行）。route_summary 与 notes 未提及任何身份或路线不确定性。
  - 氧相关性状：F1_oxygen_tolerance="obligate aerobic" confidence="medium"（第423–428行）、F6 respiration_mode="aerobic"/acceptor="oxygen" medium（第450–458行）；而 route_scope.oxygen_condition=null（第7行，与题面"氧条件: null（未指定）"一致）。
- 核查来源/新证据ID及支持范围：
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv 第77行：TAXID 471 OUT_OF_SNAPSHOT_UNRESOLVED——包内无法核实"471 的 ScientificName 是否为 Acinetobacter calcoaceticus"（P71 三要素核验无法完成，记 UNRESOLVED，不判虚构）。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv："Acinetobacter sp. NCIB 9871"→物种级 Acinetobacter johnsonii（taxid 40214，SPECIES_IDENTITY_ONLY_RETAIN_STRAIN_TOKEN，状态 VERIFIED_SPECIES_MAPPING_USER_SELECTED_GOLD_VERSION）；register 第12–13行将 NCIB 9871 与 NCIMB 9871 均登记到该 crosswalk。支持：该保藏号在包内的物种级核验结果；不支持：不支持"NCIMB 9871=A. calcoaceticus"这一物种归属，也不评价菌株级能力（D3b 范围）。
  - gold/organism_gold.tsv（BIOPATH150_029）：本 case 各步酶注下挂的菌包括 Acinetobacter johnsonii（taxid 40214）、Acinetobacter sp. NCIB 9871（taxid 40214）、Acinetobacter sp. SE19（135835）、Paenarthrobacter ureafaciens（37931）等；全表无 "Acinetobacter calcoaceticus" 行。支持：gold 侧无该菌名记录；不支持：不证明该菌不存在或不能降解环己醇（包内无覆盖，待联网核查）。
  - gold/formal_cases.tsv（BIOPATH150_029）：aerobic_or_anaerobic="No data"。支持：gold 未给该 case 氧条件，与答案 route_scope 填 null 的做法一致；对 F1 "obligate aerobic" 无支持亦无反驳。
  - 包内其他事实卡（PUBMED/EUROPE_PMC/BACDIVE/NCBI_TAXONOMY/UNIPROT）均属其他 case（如 taxid_280=Xanthobacter autotrophicus 属 BIOPATH150_006 侧、pubmed_6501223=甲苯双加氧酶突变体研究属 BIOPATH150_021 侧），对本 case 的身份与性状声称无覆盖。
  - 量表条款：R7 表行（D6 维度定义与档位描述）、P98 表 R7 锚点例（"单一间接来源标 high confidence，且不披露替代路线或身份冲突"）、P119（单点过度确信 vs 系统性误导：前者档内扣、后者才是cap候选）、P120（同一证据多处重复引用通常是同一根本断言，不双计为系统性）、P45（诚实填 null 未知，D6 可因准确披露获得较高分）、P71–P74（编号类声称须冻结核验，UNRESOLVED 不判虚构）。
- 关键事实（供本人判断，非结论）：
  1. 证据类型结构事实：全答案11条证据无一条 DATABASE_DIRECT 或 LITERATURE_DIRECT，全部自我声明 INTERNAL_KNOWLEDGE_ONLY，database/record_id 全 null——答案未把任何内容包装成数据库直引。
  2. "高置信标签引用低阶来源"的事实点位：10处 microorganism confidence="high" 全部指向 EVID_001（其自身 source_type=INTERNAL_KNOWLEDGE_ONLY、confidence="medium"，第531行）；F5_culture_collection "high"（第448行）同样指向 EVID_001（medium）；S1 酶 "high" 指 EVID_002（medium，第540行）；S2 酶 "high" 指 EVID_003（"high"，第549行）；F9 "high" 指 EVID_001。即答案内部存在"子事实置信（high）> 所引证据条目自身置信（medium）"的标注关系（照录事实，是否相称由本人判断）。
  3. 重复引用事实：EVID_001 被 S1–S10 十处 microorganism.evidence_id、十处 trait_evidence_id，以及11项有值性状（F1、F5、F6、F7、F8、F9、F10、F11、F12、F13、F15）的 evidence_id 复用——按 P120，同一根本断言的多步重复引用不因此双计为多个独立事件或"系统性"。
  4. 未知披露事实：F2/F3/F4/F14 共4项性状诚实填 null+unknown+evidence_id=null；但步骤级 uncertainty 10处全 null、顶层 uncertainties=[]，route_summary/notes 均未披露任何限制（如"CoA 延伸段无证据支持""菌株身份与 TaxID 未核验"）；S6–S10 全部标 "medium" 而非 low/unknown，且这5步在 gold 链外、包内无任何编号覆盖。
  5. 包内核验状态事实：答案全部10个 EC 与 TaxID 471 均 OUT_OF_SNAPSHOT_UNRESOLVED——high/medium 标签所指的具体酶-反应对应与身份编号在冻结快照内既无法核实也无法证伪。
  6. 交叉事实（供置信-证据相称性判断，身份结论本身属 D3b 不在本底稿范围）：包内 crosswalk 将 NCIB 9871 物种级核验为 A. johnsonii（40214），gold organism_gold 本 case 无 A. calcoaceticus 行，而答案对 "A. calcoaceticus NCIMB 9871" 的身份标 "high" 且零不确定性披露。
  7. 氧条件性状事实：F1 "obligate aerobic"（medium）为答案自行给出的菌株性状值；题面氧条件未指定（null），gold 该 case 氧条件登记 "No data"——包内无覆盖支持或反驳该性状值（UNRESOLVED）。
- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，7分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：单点过度确信：10个EC与TaxID 471全不可核而high/medium标签未作待核披露；F1 obligate aerobic无覆盖；null/unknown字段诚实→档内取7。（把握度：高）

- 本人人工确认与日期：【待本人签】
