# V04-B-008：定点人工复核

- case：BIOPATH150_016
- 只需核定：D6。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

## REV-B-008-D6 / D6

核查问题：核对原答案置信标签、null/未知和不确定性披露；区分单点过度确信与系统性误导，不因其他维度错误自动封顶，不把重复引用同一断言算多个独立事件。

- 答案具体声称与原文位置：
  - 范围背景（先决事实）：题面路线范围 "p-Cymene degradation to p-cumate"；gold/SCOPE_ADDENDUM_BIOPATH150_016.md 第3行"评分范围界定文件（DECISION_016=A）"；第5行"必答范围：p-cymene → p-cumate，对应gold线性前3步"；第9行"背景范围（非必答）：S04–S08…仅作为数据库完整链背景信息"。本答案 steps 恰为 3 步、止于 p-Cumate（第13–131行），未自行给出下游延续。
  - confidence 标签分布（逐字段盘点）：
    - step.enzyme.confidence：S1/S2/S3 全部 "medium"（第38、77、116行）。
    - step.microorganism.confidence：S1/S2/S3 全部 "**high**"（第46、85、124行），evidence_id 分别为 EVID_001/002/003（第47、86、125行）。
    - step.uncertainty：3 步全部 null（第51、90、129行）。
    - organism_profiles 15 项性状（第138–253行）：confidence="high" 共 5 项——F1_oxygen_tolerance="aerobic (obligate aerobe)"（第150–155行）、F6_respiration_electron_acceptor="aerobic respiration/oxygen"（第187–195行）、F11_cell_morphology="rod-shaped"（第220–225行）、F12_gram_cell_envelope="Gram-negative"（第226–231行）、F13_sporulation="non-sporulating"（第232–237行），全部挂 EVID_004；confidence="medium" 共 7 项（F2 第139–148行 optimum_c=30/preference"中温菌（mesophile）"、F7、F8、F9、F10、F14 第238–247行 genome_accession="NC_009512.1" 挂 EVID_005、F15）；confidence="unknown" 共 3 项（F4/F3/F5，value 全 null、evidence_id null，第156–186行）。无 "low" 标签。
    - evidence_registry 5 条（第264–309行）：EVID_001–EVID_003（每步反应+菌逐步声称）、EVID_004（菌株性状）、EVID_005（基因组登录号）confidence 全部 "medium"；source_type 全部 "INTERNAL_KNOWLEDGE_ONLY"、database=null、record_id=null、locator=null。
  - 未知/null 披露：F4/F3/F5 性状诚实 null/unknown；central_metabolism_entry.products=[]、explanation=null（第258–261行）；downstream_continuation=[]、alternative_branches=[]（第262–263行）。
  - 不确定性披露：**uncertainties=[]（第311行，空数组）**；3 处 step.uncertainty=null；route_scope.notes=null（第10行）。
  - 其他标签事实：ncbi_taxid=351746（第44、83、122、137行）、strain="F1"；trait 值为英文陈述句（如 F7="p-cymene, toluene, and other aromatic hydrocarbons"），raw_text 全 null。
- 核查来源/新证据ID及支持范围：
  - evidence_registry 5 条均为 INTERNAL_KNOWLEDGE_ONLY。支持范围：答案未冒充外部数据库来源（未标 DATABASE_DIRECT 之类）；不支持范围：该标签不核验内容真伪，也不等价于披露了证据边界。
  - facts/NCBI_NUCCORE/nuccore_NC_009512.1.json（register 第8行 ACCESSION NC_009512.1 → COVERED_BY_FACT_CARD，cases_seen=BIOPATH150_016;BIOPATH150_021）：record_id="nuccore:NC_009512.1"、record_status="**SUPPRESSED**"、names.definition="Pseudomonas putida F1, complete sequence."、organism.taxid=351746。支持范围：答案 F14 与 EVID_005 所引用的登录号在冻结快照中有对应官方记录且对象确实是 P. putida F1；不支持范围：卡同时记录该登录号当前状态为 SUPPRESSED——答案的 uncertainties=[] 与 step.uncertainty=null 中**均未披露该状态**（P73：当前状态 suppressed 的登录号历史存在不判虚构；引用是否扣分视交付时点可得知性，登记待决）。
  - facts/NCBI_TAXONOMY/taxid_351746.json（register 第75行 COVERED_BY_FACT_CARD，cases_seen=BIOPATH150_016;BIOPATH150_021）：record_status="CURRENT"、names.scientific_name="Pseudomonas putida F1"（菌株级记录；卡内未含 rank/lineage 字段，organism=null）。支持范围：答案 taxid=351746 的编号在快照中可核且学名与 "Pseudomonas putida F1" 一致；不支持范围：不自动支持任何能力/性状声称（support_scope_note 明写）。
  - facts/EUROPE_PMC/epmc_PMC179094.json：title="p-Cymene catabolic pathway in Pseudomonas putida F1: cloning and characterization of DNA encoding conversion of p-cymene to p-cumate."（CURRENT）。事实：包内存在直接涉及本题路线与该菌的文献卡；答案 evidence_registry **未引用**它（无 PMCID/文献类来源条目）。此为 D5/D3a/D3b 交叉事实，此处仅登记。
  - facts/PUBMED/pubmed_2670929.json、pubmed_6501223.json：F1 的 toluene（tod）系统文献卡——支持 F1 菌株真实存在/芳香烃背景；不支持 p-cymene 逐步声称本身。
  - facts/BACDIVE/bacdive_12880.json：Pseudomonas putida mt-2（PaW1/ATCC 33015 等保藏记录）——同种异菌株记录；答案 F5_culture_collection=null，未引用保藏号。
  - gold/SCOPE_ADDENDUM_BIOPATH150_016.md 第10行："不得因未覆盖S04–S08扣D1或D2"——本答案 3 步收口在 p-cumate，属必答范围内完成（事实陈述，不判分）。
  - EVIDENCE_COVERAGE_REGISTER.tsv：EC 1.14.13.157（第29行）、EC 1.1.1.90（第22行）、EC 1.2.1.3（第35行）均 OUT_OF_SNAPSHOT_UNRESOLVED（BIOPATH150_016 在列）——答案 3 个具体 EC 在包内均无官方卡，但本维为 D6，EC 真伪核验归 D3a/R3 通道，此处只登记"答案对这些 EC 标 medium 且证据 locator=null"的事实。
- 关键事实（供本人判断，非结论）：
  1. 置信标签与证据类型的匹配输入（事实，非结论）：3 处 microorganism.confidence="high" 与 5 处性状 confidence="high"，其引用证据（EVID_001–005）confidence 全为 "medium" 且 source_type 全为 INTERNAL_KNOWLEDGE_ONLY、locator=null。即：**所有 high 标签都高于其引用证据条目的 medium 标签，且证据为无定位信息的内部知识**。是否存在"置信与证据强度明显不相称"（P178 R7 第三类）由本人定。
  2. "内部知识当实证"的事实信号：无冒充外部来源的信号（5 条证据均诚实标 INTERNAL_KNOWLEDGE_ONLY）；但同一批内部知识同时支撑 high（身份 3 处、性状 5 处）与 medium（反应 3 处）两级标签——标签分级 vs 证据同源是本人判断输入。
  3. 披露完备性事实：uncertainties=[]（空数组）+ 3 处 step.uncertainty=null + notes=null——**全答案零不确定性披露**；同时存在两处包内可核、答案未披露的事实：EC 1.14.13.157/1.1.1.90/1.2.1.3 无包内官方卡（UNRESOLVED）与 NC_009512.1 当前状态 SUPPRESSED（有卡）。"是否构成掩盖已知矛盾"取决于答案交付时点可得知性与矛盾归属，量表未决事项由本人定（P73 待决登记口径）。
  4. 量表条款（供定位，不判分）：R7/D6 关键错误清单（P178 行 R7）三句原文；P119"单点过度确信…与系统性误导…分开判定：前者档内扣分（通常5–6档），后者才是cap候选"；P120"同一错误编号被多步重复引用通常仍是同一根本断言，不因此双计为系统性"——本答案 EVID_001/002/003 为三条独立登记条目但模板同构、每条覆盖一步（claim_scope 逐步），非同一编号复用（事实）；P121"D5已核实错引不自动使D6 cap…D6按覆盖范围、是否掩盖矛盾及其他披露质量独立定档"；P170（正面范例：'记忆值明确声明待复核；冲突与待验证点具体列出'——本答案无可声明内容，uncertainties 为空）；P171（cap候选：'系统性把预测/推断写成实证；掩盖已知矛盾或主要限制；置信与证据明显不相称'）。
  5. 诚实 null 事实：F4/F3/F5 三项 null/unknown；central_metabolism products=[]；未编造保藏号（F5 null）。
  6. 包内证据缺口：3 个 EC 的官方卡（包内 UNRESOLVED，待联网核查）；性状值（如 optimum_c=30、obligate aerobe）无包内文献级支持卡（BacDive 卡为 mt-2 菌株记录，非 F1）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，7分

- 是否关键错误（是/否/仍待核）及主要结论影响：否（N）
- 逐维理由与把握度：单点过度确信：全答案零披露；SUPPRESSED状态NC_009512.1未披露；organism high×3与5项性状high挂在medium的INTERNAL_KNOWLEDGE_ONLY证据上；按R7/P119/P120不构成系统性误导→档内取7。（把握度：高）

- 本人人工确认与日期：【待本人签】
