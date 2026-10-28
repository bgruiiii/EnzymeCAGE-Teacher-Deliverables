# V04-B-021：定点人工复核

- case：BIOPATH150_006
- 只需核定：D1。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-021-D1 / D1

核查问题：核对完整题面、指定路线/终点和实际交付模块；区分路线缺失、格式可用性与科学正确性。说明是否存在使任务符合度主要结论失效的错误。

- 答案具体声称与原文位置（visible_answer.txt，行号为该文件行号）——先列 question.json 任务要求清单，再逐项对照实际交付：
  - 【要求清单1｜单一JSON对象、无解释无围栏】交付：文件仅含1个 JSON 对象（第1–466行），无 markdown 围栏、无模型身份字段。
  - 【要求清单2｜每步 substrates/products 各≥1成员、成员含英文名+SMILES，并绑定含 ec_number 的首选酶与对应微生物】交付：
    - S1（第14–67行）：底物 1,2-Dichloroethane "ClCCCl"(main) + water "O"(cofactor)；产物 2-chloroethanol "ClCCO"(main) + chloride "[Cl-]" + H+ "[H+]"；酶 haloalkane dehalogenase，EC "3.8.1.5"，gene_or_protein "dhlA"，confidence "high"；菌 Xanthobacter autotrophicus / GJ10 / ncbi_taxid=null / ORG_001，"high"。
    - S2（第68–123行）：底物 2-chloroethanol "ClCCO" + water "O"；产物 ethylene glycol "OCCO" + chloride + H+；酶 haloalcohol dehalogenase，**ec_number=null（第107行）**，gene "dhlB"，"medium"；菌同上；step.uncertainty="EC编号未确定，酶名按文献中的haloalcohol dehalogenase填写。"（第122行）。
    - S3（第124–179行）：底物 ethylene glycol "OCCO" + NAD+（smiles=null，第139行）；产物 glycolaldehyde "OCC=O" + NADH（null，第151行）+ H+；酶 alcohol dehydrogenase，EC "1.1.1.1"，"low"；菌同上；uncertainty="乙二醇氧化步骤在GJ10中的具体酶系未完全确定。"（第178行）。
    - S4（第180–240行）：底物 glycolaldehyde + NAD+（null）+ water；产物 glycolate "OCC(=O)O" + NADH（null）+ H+；酶 aldehyde dehydrogenase，EC "1.2.1.3"，"low"；菌同上；uncertainty 同型（第239行）。
    - S5（第241–291行）：底物 glycolate + oxygen "O=O"；产物 glyoxylate "O=CC(=O)O" + hydrogen peroxide "OO"；酶 glycolate oxidase，EC "1.1.3.15"，"low"；菌同上；uncertainty 同型（第290行）。
    - 统计：全答案 chemical 成员共25个（S1:5、S2:5、S3:5、S4:6、S5:4），其中 name+SMILES 均非 null 者21个，smiles=null 者4个（NAD+/NADH 各2处）；5/5步均有 enzyme（其中1步 EC=null）与 microorganism。
  - 【要求清单3｜按物种+菌株去重、每步都要写对应菌】交付：organism_profiles 仅1条 ORG_001（Xanthobacter autotrophicus / GJ10 / ncbi_taxid=null，第293–395行），S1–S5 的 organism_profile_id 全部引用 ORG_001；5步均写了对应菌（同一株）。
  - 【要求清单4｜空样板不得原样照抄】交付：steps=5个成员、organism_profiles=1个、evidence_registry=4个成员，非空样板。
  - 【要求清单5｜未知一律填null、枚举按Schema】交付：S2 酶 ec_number=null；profile 及各步 ncbi_taxid=null；8项性状 value=null（见要求7）。枚举取值照录：role∈{main,cofactor,byproduct}；confidence∈{high,medium,low,unknown}（本答案出现 high/medium/low/unknown）；route_scope.oxygen_condition="aerobic"（Schema枚举内）；source_type∈{LITERATURE_DIRECT,DATABASE_DIRECT,INTERNAL_KNOWLEDGE_ONLY}（枚举内）。
  - 【要求清单6｜每事实至多一个最强证据、单字符串、可复用、无来源填null并配 low/unknown】交付：reaction_evidence_id、trait_evidence_id、enzyme.evidence_id、microorganism.evidence_id、各性状 evidence_id 全部为单字符串；所引 EVID_001–EVID_004 均在 evidence_registry（第405–460行）登记，内部引用自洽。照录一处配对关系：S3–S5 酶证据 EVID_003 自身 confidence="low"（第446行），对应步骤酶 confidence 亦为 "low"；无来源的性状（8项）evidence_id=null 且 confidence="unknown"。
  - 【要求清单7｜局部标签自建】交付：ORG_001、EVID_001–EVID_004、S1–S5 连续编号，无数据库真实 ID 冒充。
  - 【要求清单8｜多底物/产物用数组、role 区分】交付：S1/S2/S3/S4/S5 均用数组；main/cofactor/byproduct 角色区分齐整（如 S1 water=cofactor、chloride/H+=byproduct）。
  - 【要求清单9｜可选字段】交付：uncertainties=3条中文（第461–465行）；alternative_branches=[]（第404行）；downstream_continuation=[]（第403行）；complete_pathway_organism_profile_id="ORG_001"（第396行）；central_metabolism_entry products=["glyoxylate"]、explanation 中文（第397–402行）。
  - 【要求10–12｜键序不限/无模型身份字段/文字字段用中文】交付：无 schema 外字段（除 branch_id="main"——模板样板为 null、Schema 允许 string|null，5步均填 "main"）；无模型身份字段；route_summary/notes/step.uncertainty/uncertainties/explanation 为中文；**raw_text 7处为英文摘录句**（F1 第308行、F6 第335行、F7 第341行、F8 第347行、F9 第353行、F11 第365行、F12 第371行），照录事实。
  - 【要求15项性状】交付：15/15项全部出现（第299–393行，展示顺序与题面一致）。有值7项：F1 "aerobic"（high）、F6 {aerobic respiration, oxygen}（medium）、F7 "can use 1,2-dichloroethane as sole carbon and energy source"（high）、F8（medium）、F9（high，EVID_002）、F11 "rod-shaped"（low）、F12 "Gram-negative"（low）；明确未知8项（value=null+evidence_id=null+confidence="unknown"）：F2_temperature、F4_salinity、F3_pH、F5_culture_collection、F10_motility、F13_sporulation、F14_genome_basic、F15_habitat_generalism。按 P15 口径＝要求15项、填写7项、明确未知8项、遗漏0项。
  - 【任务参数｜路线名原样填写】交付事实：route_scope.chosen_route_name="1,2-Dichloroethane degradation pathway"（第8行）与题面"路线范围: 1,2-Dichloroethane degradation pathway"**逐字符相同（一字不差）**；oxygen_condition="aerobic"（第7行）与题面"氧条件: aerobic（好氧）"一致；is_single_continuous_route=true（第9行，模板样板为 null）；notes（第10行）=中文声明"按题面指定路线名称填写；好氧主链采用水解脱卤生成2-氯乙醇，再经乙二醇氧化至乙醛酸进入中心代谢。"；route_summary（第12行）同口径五步描述。
- 核查来源/新证据ID及支持范围：
  - gold/PROTOCOL_DISCLOSURE_BIOPATH150_006.md（本题专门范围附录，逐字引用）：性质＝"校准协议披露文件（DECISION_006=D，用户2026-10-23确认）。**不修改题面与gold**，不构成免扣条款。"；评分口径＝"本题维持冻结的4步指定路线（gold主链4步至Glycolate）作为'指定路线'基准。模型更换该主链中段并仍声称遵循指定路线时，可按量表八.D1/D2边界条款与四.5四步判断评价路线偏离；D1评价路线/任务符合度，D2独立评价所提交化学内容，不自动跨维度连坐。"；披露＝"实际题面仅提供路线名`1,2-Dichloroethane degradation pathway`，未下发pathway ID、来源库、终点化合物、关键中间体或步数等唯一定位信息。因此'严重偏离指定路线'的认定存在命题定位不足的风险，该局限必须在评分记录与后续报告中如实披露。"；边界＝"本披露**不是**免责或免扣条款……已核实的化学/路线偏离仍按其自身判据处理；评价者对本题的把握度可按量表规则如实登记。"支持：本题"指定路线"的范围边界与披露义务的权威口径；不支持：不免除、不预判任何已核实偏离的评价结论。
  - gold/reaction_gold.tsv BIOPATH150_006（第2–22行；BSY-p00075，4步）：S1 1,2-Dichloroethane+H2O→2-Chloroethanol+Chloride ion+H+；S2 2-Chloroethanol+Ferricytochrome c→Chloroacetaldehyde+Ferrocytochrome c+H+；S3 Chloroacetaldehyde+H2O+NAD+→H++Chloroacetate+NADH；S4 Chloroacetate+H2O→H++Glycolate+Chloride ion。支持：gold 主链4步、中段中间体与终点 Glycolate；不支持：gold 链内无 ethylene glycol/glycolaldehyde 相关步，也无第5步。
  - gold/formal_cases.tsv：BIOPATH150_006 ordered_step_count=4、final_graph_status=LINEAR_UNIQUE、aerobic_or_anaerobic=Aerobic；gold/case_root_identity.tsv：pathway_name="1,2-Dichloroethane degradation pathway"、root=1,2-Dichloroethane、terminal=Glycolate。支持：gold 步数、终点、氧条件登记事实。
  - gold/enzyme_gold.tsv（BIOPATH150_006）：S1 "1,2-dichloroethane dehalogenase / haloalkane dehalogenase" EC 3.8.1.5；S2 methanol dehydrogenase EC 1.1.2.7；S3 acetaldehyde dehydrogenase EC 1.2.1.4；S4 2-haloacid dehalogenase EC 3.8.1.3。支持：gold 酶-步对应；与答案 S2–S4 所填酶（haloalcohol dehalogenase/EC null、alcohol dehydrogenase 1.1.1.1、aldehyde dehydrogenase 1.2.1.3）不同（差异照录，是否关键错误由本人判断）。
  - gold/organism_gold.tsv（BIOPATH150_006）：S1–S3 菌注 EXACT＝Xanthobacter autotrophicus（taxid 280，genome GCA_005871085.1），S1 另有 Sphingobium japonicum UT26S（match_status=UNRESOLVED 行）；S4＝Xanthobacter autotrophicus 与 Moraxella sp. B（118147）。支持：gold 侧菌为物种级 X. autotrophicus；gold 表中不出现 "GJ10" 菌株级字样。
  - evidence/facts/NCBI_TAXONOMY/taxid_280.json：scientific_name="Xanthobacter autotrophicus"（物种级分类记录，含 type material 名单如 ATCC 35674；卡内无 "GJ10" 字串；support_scope_note 自述"不自动支持任何身份或能力声称"）。支持：该物种名真实存在于冻结分类库；不支持：不支持 GJ10 菌株身份、不支持任何降解能力。
  - evidence/facts/UNIPROT/uniprot_P12994.json：卡内容为 Escherichia coli K-12 的 YbhB 蛋白（register 第79行把 P12994 登记在 BIOPATH150_006 名下）——本答案未引用任何 UniProt 编号，仅照录包内存在此卡。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：本答案所用 EC 3.8.1.5（第56行）、1.1.1.1（第14行）、1.2.1.3（第35行）、1.1.3.15（第23行）全部 OUT_OF_SNAPSHOT_UNRESOLVED；CULTURE ATCC 43050 OUT_OF_SNAPSHOT（第10行，本答案 F5=null 未引用）；TAXID 28040（第70行）虽登记 COVERED_BY_FACT_CARD，但对应卡 facts/NCBI_TAXONOMY/taxid_28040.json 的 scientific_name="Micromonospora griseorubida"，与本答案无关（本答案 taxid=null）。支持：包内对本答案酶 EC 无冻结条目可核，P71 要求的 EC 核验在包内无法完成→UNRESOLVED（不判虚构、不判支持）；本答案未编造 TaxID/保藏号（相关字段为 null）。
  - 题面来源：items/V04-B-021/question.json（任务区给 case、污染物中英名、氧条件 aerobic、路线范围、题目正文与要求1–12及15项性状表；"完整空白填写格式"段预填 oxygen_condition="aerobic"、chosen_route_name="1,2-Dichloroethane degradation pathway"）。
  - 量表条款：R1 表行（D1 定义与五档描述）、P100（D1/D2 边界：路线/任务参数偏离归 D1）、P101（无泛化路线名免责；披露不得写成免扣条款）、P13–P15（输出覆盖登记与"要求15项、填写x、未知y、遗漏z"口径）、P44–P45（缺失登记 vs 诚实 null）、P28–P29（题面边界与 gold 下游步）、P105（辅因子字段要求的 D1/D2 分账，不双计）、P22（不连坐）。
- 关键事实（供本人判断，非结论）：
  1. 清单交付统计：格式项（1/1、键序、无模型字段、样板复制、多成员数组、单字符串证据引用、局部标签自洽）全部有交付；每步微生物 5/5 有；每步酶名 5/5 有、EC 4/5 有（S2=null）；主链成员名+SMILES 10/10 有，辅因子 NAD+/NADH 共4处 smiles=null（Schema 允许 null，照录）；15项性状 15/15 出现（填写7、明确未知8、遗漏0）；route_scope 路线名与题面一字不差、氧条件与题面一致。
  2. 缺什么（照录）：S2 酶 EC 编号（null，答案已在该步 uncertainty 主动披露"EC编号未确定"）；ncbi_taxid 全 null（物种名+菌株名已给）；8项性状为明确未知（P15 口径属"明确未知"，非遗漏）；raw_text 7处为英文而非中文（对照要求12的文字字段语言规定）。
  3. 多什么（题面清单之外的照录）：5步 branch_id 填 "main"（样板为 null、Schema 允许 string）；gene_or_protein "dhlA"/"dhlB"（Schema 允许字段）；step.uncertainty 3处与 uncertainties 3条（可选字段）；S5 为 gold 4步链之外的第5步（见事实5）。
  4. 路线内容对照事实：S1 与 gold S1 化学一致（1,2-DCE 水解脱卤 → 2-chloroethanol+Cl-+H+；答案酶 haloalkane dehalogenase/EC 3.8.1.5 与 gold S1 酶名尾段+EC 相同）。S2–S4 中段与 gold 不同——答案：2-chloroethanol →(水解脱卤) ethylene glycol →(醇氧化) glycolaldehyde →(醛氧化) glycolate；gold：2-chloroethanol →(细胞色素c氧化脱卤) chloroacetaldehyde →(NAD+醛氧化) chloroacetate →(2-卤酸脱卤) glycolate。答案在 S4 到达 glycolate（与 gold 终点同名化合物），另加 S5 至 glyoxylate（gold 链外1步；题面未指定终点）。
  5. 范围边界事实（附录+条款）：附录已逐字确认"题面仅提供路线名，未下发终点/中间体/步数"且"评分口径维持4步指定路线（gold主链4步至Glycolate）为基准""该局限必须在评分记录与后续报告中如实披露""披露不是免责或免扣条款"。据此：本题"指定路线"在题面层面缺唯一定位信息（命题定位不足风险），而 gold 口径仍以4步至 Glycolate 为基准——两者的张力须在本维结论中如实登记（P101/P28）。答案侧的事实是：未使用"替代路线/偏离"字样，但 notes（第10行）与 route_summary（第12行）明确写出了自己所走的中段化学（水解脱卤→乙二醇→乙醛酸），即所选路线内容在答案内是自我声明的。
  6. 答案声明是否与gold一致的事实：notes/route_summary 声明的中段与 gold 中段（事实4）不同；答案未披露"与 gold 中段不同"这一事实本身（未声明"替代"）。"是否存在使任务符合度主要结论失效的错误"＝是（关键错误，见复核结论；P100适用）（P100：路线/任务参数偏离归 D1 判定；偏离认定须结合附录披露的定位不足风险，两者均为已登记事实）。
  7. 证据性质事实（与 D5/D6 相关，此处照录供 D1 引用完整性判断）：EVID_001=LITERATURE_DIRECT（locator "Janssen et al., 1985, Journal of Bacteriology: Degradation of 1,2-dichloroethane by Xanthobacter autotrophicus GJ10"，claim_scope 覆盖 S1/S2/ORG_001/性状，high）；EVID_002=DATABASE_DIRECT（database "IUBMB Enzyme Nomenclature"，record_id "3.8.1.5"，high）；EVID_003/EVID_004=INTERNAL_KNOWLEDGE_ONLY（low）。包内冻结快照中**无** Janssen 1985 事实卡、EC 3.8.1.5 为 OUT_OF_SNAPSHOT_UNRESOLVED——这两个引用在包内无法核对，记 UNRESOLVED（待联网核查，不判虚构）。
  8. 辅因子分账事实（P105 场景）：题面未设"辅因子"专列字段，辅因子以 substrates/products 的 role=cofactor/byproduct 表达；答案 S1 water、S3/S4 NAD+、S5 oxygen 均以 cofactor 表达，S2 gold 侧的细胞色素c体系未出现（答案 S2 反应类型不同，本身不需要该体系）。题面是否"明确要求辅因子与配平"＝否（题面只要求底物/产物+酶+菌+性状+证据），是否构成字段要求未满足＝否（题面未设辅因子专列字段，P105分账不构成字段未满足）。
- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，4分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：S2–S4中段与gold指定路线不同且未声明替代，按P100'自称合规却交付不同化学路线'属D1关键错误（本人裁决原则A1）→cap≤4；其余交付完整度高（路线名逐字符一致、模块齐全、诚实null），档内取4。命题定位不足风险（附录）已在底稿登记，不免扣（P101）。（把握度：高）

- 本人人工确认与日期：【待本人签】
