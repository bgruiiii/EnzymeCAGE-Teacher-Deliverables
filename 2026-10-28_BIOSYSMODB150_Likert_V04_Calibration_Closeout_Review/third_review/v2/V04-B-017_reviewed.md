# V04-B-017：定点人工复核

- case：BIOPATH150_007
- 只需核定：D3b、D6。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-017-D3b / D3b

核查问题：分别核对物种/菌株身份、该菌完成所写单步的证据和整条路径能力；身份真实或单步记录不自动证明指定菌株完成全部步骤。

- 答案具体声称与原文位置：
  - 身份层：steps[0..3].microorganism（S1 第46–53行、S2 第92–99行、S3 第138–145行、S4 第184–191行）均为 organism_name="Agrobacterium radiobacter"、strain="AD1"、ncbi_taxid=null、organism_profile_id="ORG_001"、confidence="low"、evidence_id="EVID_001"（S1）/"EVID_001"（其余步亦 EVID_001）。即：声称具体菌株 "AD1"，未交付 TaxID。
  - organism_profiles[0]（第197–321行）：organism_name="Agrobacterium radiobacter"（第200行）、strain="AD1"（第201行）、ncbi_taxid=null（第202行）；15 项性状：10 项有中文文本值且全部 confidence="low"、挂 EVID_002（F1 第215–220行"好氧"、F6 第252–260行"有氧呼吸/氧气"、F7 第261–266行"可利用1,3-二氯-2-丙醇及其降解中间体作为碳源和能源"、F8、F9 第273–278行"具有卤代醇脱卤酶（EC 4.2.1.22）和环氧化物水解酶（EC 3.3.2.3）活性"、F10"运动性（通常具鞭毛）"、F11"杆状"、F12"革兰氏阴性"、F13"不产芽孢"、F15"土壤、根际等环境中较常见"）；5 项 null/unknown（F2/F3/F4/F5/F14，evidence_id=null）。
  - 反应级层：4 步的 microorganism 全部绑定 ORG_001（第50、96、142、188行）。
  - 完整路径层：complete_pathway_organism_profile_id="ORG_001"（第322行）；route_summary（第12行）"在好氧条件下，1,3-二氯-2-丙醇经卤代醇脱卤酶形成环氧氯丙烷…进入中心代谢"（无菌名句）。
  - 证据：EVID_001（第332–344行）source_type="INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null、claim_scope=["1,3-Dichloro-2-propanol pathway steps","enzyme assignments","microorganism assignment"]、confidence="low"；EVID_002（第345–355行）同 source_type、claim_scope=["Agrobacterium radiobacter AD1 general traits"]、confidence="low"。
  - 逐步披露：4 处 step.uncertainty（第56、102、148、194行）均为"酶与菌株依据内部知识推断，未给出外部实验证据，置信度低。"；uncertainties[0]（第358行）"路线与酶/菌主要来自内部知识，缺少外部数据库或文献证据；具体数值性状未填写。"
- 核查来源/新证据ID及支持范围：
  - gold/organism_gold.tsv（BIOPATH150_007，STEP 级 30 行 + PATHWAY_COMPLETE 2 行）：
    - S01/S03 行含 Agrobacterium radiobacter（taxid 362，EXACT）与 Agrobacterium radiobacter AD1(pTB3)（No TaxID，NORMALIZED_EXACT），另有 Arthrobacter sp. AD2（168809）、Corynebacterium sp.（1720）、Corynebacterium sp. N-1074（No TaxID）。
    - S02/S04 行："Agrobacterium radiobacter AD1" 与 "Agrobacterium radiobacter strain AD1(pTB3)" 的 organism_match_status=**UNRESOLVED**（gold 自身未解析），另有 Arthrobacter sp. AD2、Corynebacterium sp. N-1074。
    - PATHWAY_COMPLETE 2 行：168809（Arthrobacter sp. AD2）与 No TaxID（Corynebacterium sp. N-1074），pathway_complete=TRUE；gold 未登记 A. radiobacter AD1 为该路线全路径菌。
    - 支持范围：gold 登记逐步酶-菌对应与全路径菌；不支持范围：gold 非穷举（量表 P27、P54），gold 无某菌不构成反证。
  - evidence/EVIDENCE_COVERAGE_REGISTER.tsv：本答案 ncbi_taxid=null → 无 TAXID 登记行；全表无 TAXID 362/168809 行。
  - facts/NCBI_TAXONOMY/（10 张卡）：无 Agrobacterium radiobacter 卡；taxid_303 为 Pseudomonas putida（不同种）。
  - evidence/crosswalk/verified_species_name_crosswalk.tsv：含 "Agrobacterium radiobacter 358→362 Agrobacterium radiobacter"（VERIFIED_SPECIES_MAPPING_USER_SELECTED_GOLD_VERSION）。支持范围：物种名有官方映射记录；不支持范围：不核验 AD1 菌株身份（答案亦未交付 TaxID）。
  - facts/BACDIVE/bacdive_13580.json：Agrobacterium radiobacter DSM 30147 物种级记录（非 AD1）。facts/UNIPROT/ 两张卡（dhlA/Xanthobacter、ybhB/E. coli）与本题无关。包内无 AD1 单步催化或全路径能力证据卡。
- 关键事实（供本人判断，非结论）：
  1. 三层声称各有原文：身份层=第47–49行等（物种名+strain="AD1"，taxid=null）；反应级层=4 步各绑定 ORG_001；完整路径层=第322行 complete_pathway_organism_profile_id="ORG_001"。P69：三层分别核对，不得互相冒充。
  2. 身份层：taxid=null → P71/P67 编号核验（ScientificName/rank/lineage）无编号对象；包内无该物种分类卡；crosswalk 仅提供物种名映射（358→362）。
  3. 反应级层：gold S01–S04 步级行中出现 "Agrobacterium radiobacter"/"AD1" 名称（S02/S04 行 gold 自身 UNRESOLVED）；同步骤 gold 行也登记 Arthrobacter sp. AD2、Corynebacterium sp. 等。包内无 AD1 独立单步实验证据卡。
  4. 完整路径层：gold PATHWAY_COMPLETE 指向 Arthrobacter sp. AD2 与 Corynebacterium sp. N-1074；A. radiobacter AD1 不在 gold 全路径行中；gold 非穷举，不构成反证。
  5. R4/D3b 关键错误清单（P175 行 R4）："物种/菌株或TaxID编造；由基因组存在某酶直接推断完成整条路径；把仅支持单步的菌写成全路径菌"。taxid=null → "TaxID编造"无核验对象；答案也未见"由基因组存在某酶推断全路径"的表述路径（答案证据无基因组声称，F14=null）——两项均为事实铺垫，不预判。
  6. P106–P110 身份阶梯适用前提是有官方核实结论；本答案无 taxid 交付、包内无该物种卡 → 无可套用的编号核实结论（事实铺垫，不预判档位）。
  7. 答案自身披露（与 D6 交叉但此处仅记事实）：全部菌/性状 confidence="low"，唯一证据均为 INTERNAL_KNOWLEDGE_ONLY（database/record_id/locator 全 null）；4 处 step.uncertainty + uncertainties[0] 共 5 处主动披露"内部知识推断、缺外部证据"；10 项性状值为中文常识性描述而非文献引文；5 项诚实 null/unknown。
  8. 包内证据缺口清单：AD1 菌株身份卡、AD1 单步反应级证据、AD1 全路径能力证据、register TAXID 行（答案 taxid=null 未产生）——均无覆盖 → 待联网核查/记 UNRESOLVED。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，5分

- 是否关键错误（是/否/仍待核）及主要结论影响：仍待核（UNRESOLVED）
- 逐维理由与把握度：与B007-D3b同口径：AD1文献存在性（82条）+能力命中（环氧氯丙烷唯一碳源生长）；BacDive/NCBI菌株条目/保藏号三处负检索→部分支持+未核项→取5。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-017-D6 / D6

核查问题：核对原答案置信标签、null/未知和不确定性披露；区分单点过度确信与系统性误导，不因其他维度错误自动封顶，不把重复引用同一断言算多个独立事件。

- 答案具体声称与原文位置：
  - confidence 标签分布（逐字段盘点）：
    - step.enzyme.confidence：4 步全部 "low"（第43、89、135、181行）。
    - step.microorganism.confidence：4 步全部 "low"（第51、97、143、189行）。
    - organism_profiles 15 项性状：F2/F4/F3/F5/F14 = value null、confidence "unknown"、evidence_id null（第204–214、221–232、233–242、243–251、303–312行）；F1/F6/F7/F8/F9/F10/F11/F12/F13/F15 共 10 项 = confidence "low"、evidence_id="EVID_002"（如 F12 第291–296行"革兰氏阴性"low）。无任何性状标 high/medium。
    - evidence_registry：EVID_001 confidence="low"（第343行）、EVID_002 confidence="low"（第354行）；两者 source_type 均 "INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null（第332–355行）。
    - route_scope.oxygen_condition="aerobic"、chosen_route_name="1,3-Dichloro-2-propanol pathway"（第7–8行，题面原样）。
  - 未知/null 披露：ncbi_taxid=null、gene_or_protein=null（4 步酶均 null，第42、88、134、180行）、5 项性状 null/unknown、central_metabolism_entry 为解释性文本。
  - 不确定性披露：step.uncertainty 4 处（第56、102、148、194行，同文："酶与菌株依据内部知识推断，未给出外部实验证据，置信度低。"）；uncertainties[0]（第358行）"路线与酶/菌主要来自内部知识，缺少外部数据库或文献证据；具体数值性状未填写。"；route_scope.notes（第10行）"题面指定路线名称原样保留；按好氧条件下卤代醇/环氧化物转化主链填写。"
  - null 字段的枚举合规（事实）：confidence 未见自造枚举值，全部为 high/medium/low/unknown 四值之一。
- 核查来源/新证据ID及支持范围：
  - evidence_registry 仅 2 条，均 source_type="INTERNAL_KNOWLEDGE_ONLY"。支持范围：答案如实标注了证据性质为内部知识（未冒充数据库来源）；不支持范围：INTERNAL_KNOWLEDGE_ONLY 标签本身不核验内容真伪。
  - 包内冻结证据与答案声称的客观关系（供判断"置信与证据是否相称"的输入，非结论）：
    - EC 4.2.1.22：register 第61行 OUT_OF_SNAPSHOT_UNRESOLVED（BIOPATH150_007）——包内无卡，答案标 low。
    - EC 3.3.2.3：register 第50行 COVERED_BY_FACT_CARD（facts/IUBMB_EXPLORENZ/ec_3.3.2.3.json），卡内 record_status="TRANSFERRED"、accepted_name=null、former_name_note="epoxide hydrolase. Now known to comprise two enzymes, microsomal epoxide hydrolase (EC 3.3.2.9) and soluble epoxide hydrolase (EC 3.3.2.10)"、replacement_history="transferred to: 3.3.2.9, 3.3.2.10; deleted 2006"。答案引用该号且标 low，但 uncertainties/step.uncertainty 中**未披露**该编号已撤转（披露内容只覆盖"内部知识、缺外部证据"）。
    - gold（BIOPATH150_007）该两步通配 EC 为 4.5.1.- 与 3.3.2.-；P73"通配EC不能反推答案具体号正确；历史撤转编号不等于虚构——登记为历史分类问题"。
    - 菌株 AD1：无包内身份卡（见 D3b 小节）；gold PATHWAY_COMPLETE 未登记 AD1。答案对身份/能力均标 low 并多处披露内部知识来源。
  - EVIDENCE_COVERAGE_REGISTER.tsv：答案未交付任何 TaxID/保藏号/登录号，故无对应登记行。
- 关键事实（供本人判断，非结论）：
  1. 置信标签总体分布：全答案无一处 "high" 与无一处 "medium"（除 route_scope 布尔/枚举字段外）；steps 级 8 个 confidence 全 "low"，性状 10 项 "low"、5 项 "unknown"；证据 2 条均 "low"。标签与其自标 source_type（INTERNAL_KNOWLEDGE_ONLY）一致方向（事实：标签未高于其声明的证据类型）。
  2. "内部知识当实证"的事实信号检查：source_type 全为 INTERNAL_KNOWLEDGE_ONLY，database/record_id/locator 全 null——**没有**把内部知识标成 DATABASE_DIRECT/high 的事实信号；同时也无任何外部可核来源（5 处披露文字与之呼应）。
  3. 披露覆盖范围：披露集中在"来源性质（内部知识/缺外部证据/置信低）"，未覆盖：EC 3.3.2.3 已撤转（包内有卡可核、答案未提）、gold 路线为 8 步两分支而答案 4 步（该冲突是否属"已知矛盾"取决于答案是否知晓，包内无答案知情的直接证据——只记事实：披露文字中未提及分支/步数差异）。
  4. 量表条款（供定位，不判分）：R7/D6 关键错误清单（P178 行 R7）"把预测/推断系统性写成实证观测；掩盖已知矛盾或主要限制；置信度与证据强度明显不相称"；P119"单点过度确信（个别字段以强证据标签包装未核实内容且零披露）与系统性误导分开判定：前者档内扣分（通常5–6档），后者才是cap候选"；P120"同一错误编号被多步重复引用通常仍是同一根本断言，不因此双计为系统性"——本答案 EVID_001 被全部 4 步与酶复用，按 P120 属单一根本断言的复用形态（事实）；P121"D6…按覆盖范围、是否掩盖矛盾及其他不确定性披露质量独立定档"；P45"诚实填写未知/null：D6可因准确披露未知获得较高分"；P170（9档正面范例要求"记忆值明确声明待复核；冲突与待验证点具体列出"）。
  5. null 使用事实：taxid、gene_or_protein、5 项性状等均按题面要求填 null 未编造数值；F14_genome_basic 的三个子键（genome_accession/size/gc）均 null。
  6. 包内证据缺口：EC 4.2.1.22 官方卡、AD1 身份卡、EC 3.3.2.3 撤转的联网确认（包内卡已给出 TRANSFERRED 状态，无需联网即可登记该事实）——其中 4.2.1.22 与 AD1 部分记 UNRESOLVED、待联网核查。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，8分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：单点过度确信：所引EC 3.3.2.3为TRANSFERRED状态未披露、conf标签与证据有落差；披露缺失面在本组最小→档内取8。（把握度：高）

- 本人人工确认与日期：【待本人签】
