# V04-B-028：定点人工复核

- case：BIOPATH150_125
- 只需核定：D1、D2、D3a。

- 完整题面和原答案在items/本编号目录；评分依据为rubric/、gold/、evidence/。

说明：本答案 visible_answer.txt 为单行 JSON（7,907 字符），机器解析失败（json.decoder.JSONDecodeError，char 6246）；下文位置一律用"字段路径 + 字符偏移(offset=)"定位，引用均为原文逐字摘录。

## REV-B-028-D1 / D1

核查问题：核对完整题面、指定路线/终点和实际交付模块；区分路线缺失、格式可用性与科学正确性。说明是否存在使任务符合度主要结论失效的错误。

- 答案具体声称与原文位置：
  - 工程状态（items/V04-B-028/engineering_status.json）：engineering_class="INVALID_JSON"、finish_reason="stop"、machine_readable=false、visible_empty=false。损坏点（事实定位）：organism_profiles[0].traits.F9_enzyme_activity.evidence_id 的值为裸标识符——原文 `"raw_text":null,"evidence_id":EVID_001,"confidence":"low"`（offset≈6228，"EVID_001" 缺两侧引号），JSON 在此截断失败；全文其余部分人可阅读。
  - route_scope（offset 147）：oxygen_condition="aerobic"（offset 162）；chosen_route_name="methyl tert-butyl ether degradation"；is_single_continuous_route=true；notes="好氧降解主线，题面未指定氧条件，但MTBE已知主降解路线为好氧单加氧途径。"
  - route_summary（offset 500 前）："好氧条件下，MTBE经甲烷/丙烷单加氧酶氧化为叔丁醇（TBA），再经TBA单加氧酶羟基化为2-羟基异丁醛，氧化为2-羟基异丁酸，脱甲基生成甲基丙烯酸，进一步经3-羟基异丁酸进入中心代谢（甲基丙二酸半醛→丙酰辅酶A/丝氨酸途径）。代表菌为Methylibium petroleiphilum PM1。"
  - steps：6 步（S1 offset 510、S2 1386、S3 2122、S4 2856、S5 3536、S6 4181）：
    - S1：Methyl tert-butyl ether（main，SMILES "CC(C)(C)OC"）+ oxygen（cofactor，"O=O"）→ tert-Butyl alcohol（main，"CC(C)(O)C"）+ formaldehyde（byproduct，"C=O"）；reaction_type="O-demethylation (monooxygenation)"；enzyme.name="alkane/ether monooxygenase (methane monooxygenase homologue)"、ec_number=null、gene_or_protein="mmoB-like / alkB-like hydroxylase"、confidence="medium"；uncertainty="起始醚键断裂酶的具体基因与EC尚不确定，多为单加氧酶家族成员。"
    - S2：tert-Butyl alcohol + oxygen → 2-hydroxy-2-methylpropanal（"CC(C)(O)C=O"）；enzyme.name="tert-butyl alcohol monooxygenase"、ec_number=null。
    - S3：2-hydroxy-2-methylpropanal → 2-hydroxyisobutyrate（"CC(C)(O)C(=O)O"）；enzyme.name="2-hydroxyisobutyraldehyde dehydrogenase"、ec_number=null、gene_or_protein="mhpB-like aldehyde dehydrogenase"。
    - S4：2-hydroxyisobutyrate → methacrylate（"C=C(C)C(=O)O"）；reaction_type="dehydration (desaturation)"；enzyme.name="2-hydroxyisobutyrate dehydratase"、ec_number=null、gene_or_protein="hbd-like"。
    - S5：methacrylate → 3-hydroxyisobutyrate（"CC(O)CC(=O)O"）；reaction_type="hydration"；enzyme.name="methacrylate hydratase"、ec_number=null。
    - S6：3-hydroxyisobutyrate → methylmalonate semialdehyde（"CC(=O)CC(=O)O"）；enzyme.name="3-hydroxyisobutyrate dehydrogenase"、ec_number="1.1.1.31"、gene_or_protein="hbdH"。
    - 6 步的 microorganism 全部为 Methylibium petroleiphilum / PM1 / ncbi_taxid=336257 / ORG_001（6 步均写 microorganism 字段）；6 步 trait_evidence_id 均为 null；S2–S5 uncertainty 均为 null。
  - organism_profiles（offset 4880）：1 条 ORG_001；15 项性状全部出现（F2、F1、F4、F3、F5、F6、F7、F8、F9、F10、F11、F12、F13、F14、F15），每项四字段外壳齐全；value=null 的项 F2/F4/F3/F13 confidence="unknown"；带 raw_text 的仅 F5（"Methylibium petroleiphilum PM1, ATCC BAA-1232"）、F7（"PM1 can grow on MTBE and TBA as sole carbon sources"）、F12（"Gram-negative"）、F14（"Methylibium petroleiphilum PM1 genome, NC_008825"）。
  - complete_pathway_organism_profile_id="ORG_001"；central_metabolism_entry.products=["methylmalonate semialdehyde","propionyl-CoA (下游)"]；downstream_continuation=[]、alternative_branches=[]；evidence_registry 2 条（EVID_001 offset 7300 附近：source_type="LITERATURE_DIRECT"、database="PubMed"、record_id="16996055"、locator="Hanson JR et al., 1999 / Kane SR et al., 'Methylibium petroleiphilum PM1 genome'"、claim_scope=["MTBE好氧降解途径","Methylibium petroleiphilum PM1降解MTBE"]、confidence="medium"；EVID_002：source_type="LITERATURE_DIRECT"、database="NCBI"、record_id="336257"、locator="Taxonomy/Genome entry for Methylibium petroleiphilum PM1"、claim_scope=["菌株身份","革兰氏阴性","基因组","碳源利用"]）；uncertainties 2 条（"各步酶的EC编号多数未知或仅同源推断……""菌株生理性状……均为低置信或null"）。
  - 无 model/model_id 等身份字段；无围栏（损坏为字段值缺引号，非围栏问题）。
- 核查来源/新证据ID及支持范围：
  - 题面 question.json（messages[0].content）：case_id=BIOPATH150_125、污染物=Methyl tert-butyl ether、氧条件: null（未指定）、路线范围: methyl tert-butyl ether degradation；要求与 V04-B-022/014 题面为同一模板（已 diff 核对：仅 case 特定字段不同），无步数限制注记（"016仅前3步、006指定4步"不在本条题面）。支持范围：完整性/任务符合度对照。
  - gold/case_root_identity.tsv + formal_cases.tsv（BIOPATH150_125）：路线 BSY-p00868 "methyl tert-butyl ether degradation"，root=Methyl tert-butyl ether，终点=acetyl-CoA，LINEAR_UNIQUE、10 步。支持范围：步数/终点/序列核查基线；不支持：gold 非唯一允许答案（P27）。
  - gold/reaction_gold.tsv（42 行，10 步）：S05 MTBE+O2+NADH+H+ → tert-Butoxymethanol；S08 tert-Butoxymethanol+NAD+ → Tert-butyl formate；S02 Tert-butyl formate+H2O → tert-Butanol+Formate；S04 tert-Butanol+O2+NADPH+H+ → 2-Methylpropane-1,2-diol；S01 2-MPD+NAD+ → 2-Hydroxy-2-methylpropanal；S03 2-HMPaldehyde+NAD+ → 2-Hydroxyisobutyrate；S06 2-HIBA+ATP+CoA → 2-hydroxyisobutyryl-CoA+AMP+PPi；S10 → (S)-3-hydroxybutanoyl-CoA；S07 → acetoacetyl-CoA；S09（REVERSED）acetoacetyl-CoA ← acetyl-CoA+CoA。
  - gold/enzyme_gold.tsv：MTBE monooxygenase EC 1.14.13.M36；tert-butoxymethanol dehydrogenase EC 1.1.1.M26；tert-butyl formate deformylase EC 3.7.1；tert-butyl alcohol hydroxylase EC 1.14.13.229；2-methyl-propane-1,2-diol dehydrogenase EC 1.1.1.400/1.2.1.98；hydroxyisobutyraldehyde dehydrogenase EC 1.2.1.98/1.2.1.-；2-hydroxyisobutanoate-CoA ligase EC 6.2.1.M4；2-hydroxyisobutanoyl-CoA mutase EC 5.4.99.64；3-hydroxybutyryl-CoA dehydrogenase EC 1.1.1.35；acetyl-CoA acetyltransferase EC 2.3.1.16|2.3.1.9。
- 关键事实（供本人判断，非结论）：
  1. 题面要求逐项对照（事实）：
     - route_scope.chosen_route_name 与题面逐字一致 ✓；**oxygen_condition="aerobic" 与题面"氧条件: null（未指定）"不同**——答案自行改为 aerobic 并在 notes 中披露"题面未指定氧条件，但MTBE已知主降解路线为好氧单加氧途径"（"aerobic"在题面允许枚举内；是否构成任务参数偏离由本人按 P100 判定）。
     - 每步主底物+主产物 name+smiles：6 步均交付 ✓（S1 另含 cofactor oxygen 与 byproduct formaldehyde）。
     - 每步首选酶及EC：6 步 enzyme 字段均非空，但 6 步中 5 步 ec_number=null（仅 S6 给 1.1.1.31）；uncertainties[0] 披露"各步酶的EC编号多数未知或仅同源推断"——按题面规则5"未知填 null"的口径交付。
     - 每步对应微生物：6 步均写（同指 ORG_001）；题面"同一菌去重"满足（1 条 profile 复用，题面明文允许）。
     - 15 项性状：全部出现、按展示顺序、四字段外壳齐全；raw_text 仅 4 项有值；完全未知项 4 项（F2/F4/F3/F13，value=null+confidence=unknown）。
     - 证据登记：仅 2 条（EVID_001/EVID_002），字段齐全；step.trait_evidence_id 全 null（题面允许"没有任何来源时填 null"）；F9 的 evidence_id 因缺引号致 JSON 无效（工程缺陷定位见上）。
     - 可选保留字段：complete_pathway_organism_profile_id、central_metabolism_entry、uncertainties 已填；alternative_branches/downstream_continuation 为空数组。
  2. 与 gold 的路线覆盖差异（事实陈述，对错判定不在此）：答案 6 步、终点 methylmalonate semialdehyde（central_metabolism_entry 称经丙酰辅酶A入中心代谢）；gold 10 步、终点 acetyl-CoA。逐段对照：答案 S1（MTBE→TBA+甲醛）对应 gold 三步（S05 MTBE→tert-butoxymethanol；S08 →tert-butyl formate；S02 →tert-butanol+formate），gold 的 C1 产物为 formate，gold 中间体 tert-butoxymethanol 与 tert-butyl formate 未在答案出现；答案 S2（TBA→2-羟基-2-甲基丙醛）对应 gold 两步（S04 TBA→2-methylpropane-1,2-diol；S01 →2-hydroxy-2-methylpropanal），gold 中间体 2-MPD 未在答案出现；答案 S3（醛→2-HIBA）与 gold S03 转化相同；gold S06–S10（2-HIBA→CoA→mutase→(S)-3-HB-CoA→acetoacetyl-CoA→acetyl-CoA）在答案中无对应步；答案 S4–S6（2-HIBA→methacrylate→3-hydroxyisobutyrate→methylmalonate semialdehyde）在 gold 中无对应步（gold 主链无 methacrylate/3-hydroxyisobutyrate/methylmalonate semialdehyde 化合物）。答案 alternative_branches=[]，notes/route_summary 未声明替代路线或与 gold 的分岔。
  3. 量表条款（一句话）：R1 行=D1 档位描述；P13–P15 输出覆盖登记（路径：已给出；酶：已给出；微生物：已给出；性状：要求15项、填写15项、明确未知4项、遗漏0项；来源：部分给出（2 条）；不确定性：已给出）；P14/P125 表 R1 "JSON语法损坏但人可阅读：科学内容照评；D1记录工程缺陷；保留机器不可用标记"；P44/P45 缺失与诚实 null；P98 表 R1 D1 关键错误清单（含"输出损坏且科学内容也无法辨认"——本条科学内容人可阅读，属该条目适用性判断）；P100 任务参数偏离（更改氧条件等任务条件）属 D1 关键错误判定范畴——本条 oxygen_condition 与题面不一致为事实，是否构成偏离及后果由本人判定。
  4. 包内证据缺口：无——完整性对照所需题面与 gold 均在包内。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：路线偏离未声明（A1/P100）+oxygen_condition填aerobic而题面为null（任务参数偏离）+JSON损坏（人可读按R1）三事并存→cap≤4，档内取3。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-028-D2 / D2

核查问题：逐步核对主底物到主产物的化学转化、方向和连续性。若可能是替代路线，先分清任务符合度与所写反应本身是否成立；检索无结果不等于反应不可能。

- 答案具体声称与原文位置：
  - 主链声称（route_summary，offset 500 前 + steps S1–S6）：MTBE（+O2）→ TBA + formaldehyde → 2-hydroxy-2-methylpropanal → 2-hydroxyisobutyrate → methacrylate → 3-hydroxyisobutyrate → methylmalonate semialdehyde；central_metabolism_entry="甲基丙二酸半醛进一步氧化分解，经丙酰辅酶A进入甲基丙二酰辅酶A途径/三羧酸循环相关的中心代谢。"；route_scope.oxygen_condition="aerobic"。
  - 各步反应类型（reaction_type 原文）：S1 "O-demethylation (monooxygenation)"、S2 "hydroxylation (monooxygenation)"、S3 "aldehyde oxidation (dehydrogenation)"、S4 "dehydration (desaturation)"、S5 "hydration"、S6 "oxidation (dehydrogenation)"。
  - 各步辅因子/副产物交付（事实）：S1 列 oxygen（cofactor）与 formaldehyde（byproduct），未列 NADH/水；S2 列 oxygen，未列还原力；S3–S6 均为单底物→单产物，未列 NAD+/NADH/H2O。
  - 步间连续性（事实）：predecessor_step_ids 依次 S1→S2→…→S6；相邻步化合物名逐一衔接（S1 产物 tert-Butyl alcohol = S2 底物；S2 产物 = S3 底物；S3 产物 = S4 底物；S4 产物 = S5 底物；S5 产物 = S6 底物），名称拼写一致。
- 核查来源/新证据ID及支持范围：
  - gold/reaction_gold.tsv（42 行）：gold 主链 10 步序列与辅因子/副产物（S05 MTBE+O2+NADH+H+→tert-Butoxymethanol；S08 +NAD+→Tert-butyl formate；S02 +H2O→tert-Butanol+Formate；S04 tert-Butanol+O2+NADPH+H+→2-Methylpropane-1,2-diol；S01 +NAD+→2-Hydroxy-2-methylpropanal；S03 +NAD+ →2-Hydroxyisobutyrate；S06 +ATP+CoA→2-hydroxyisobutyryl-CoA+AMP+PPi；S10 →(S)-3-hydroxybutanoyl-CoA；S07 +NAD+→acetoacetyl-CoA；S09 反向 acetoacetyl-CoA→acetyl-CoA+CoA）。支持范围：gold 逐步化合物、方向、计量参照；不支持：gold 非唯一允许答案（P27），与 gold 不同不自动判错。
  - gold/case_root_identity.tsv：root=MTBE、终点=acetyl-CoA。支持范围：终点参照（题面未写具体终点化合物）。
  - 答案自引证据：EVID_001（PubMed 16996055，claim_scope=["MTBE好氧降解途径","Methylibium petroleiphilum PM1降解MTBE"]）——facts/PUBMED/ 仅 6501223、2670929 两卡（均为 P. putida 甲苯文献），无 16996055 卡；覆盖登记册无 PUBMED 类行 → 所引来源包内不可定位，不能作为答案路线的包内支持（P51：不回填）。
  - 包内无 MTBE 降解任何文献/路线事实卡；facts 树与 f7_interpretation 均无 methacrylate/3-hydroxyisobutyrate/MTBE 相关卡。
- 关键事实（供本人判断，非结论）：
  1. 合理替代路线四步判断的事实铺垫（P57–P61）：
     - 第1步：题面指定了路线名"methyl tert-butyl ether degradation"，未写具体终点化合物（氧条件=null 未指定）→ 事实=已指定路线。
     - 第2步：答案是否声明替代路线 → 事实=未声明（alternative_branches=[]；notes 仅写"MTBE已知主降解路线为好氧单加氧途径"；route_summary 以"已知主降解路线"语气书写，全文无"替代"表述）。
     - 第3步：答案所写路线（尤其 2-HIBA 之后的 methacrylate 分岔）是否有可核证据 → 事实=唯一自引证据 EVID_001 包内不可定位；包内无任何支持或反驳该分岔的事实卡 → 无→按未证实登记的形态。
     - 第4步：偏离是否使该维度主要结论失效 → 事实铺垫见第 2 点；判定留本人。
  2. 与 gold 逐步对照（事实，不含判定）：
     - 段1 MTBE→TBA：答案 1 步（MTBE+O2→TBA+formaldehyde）；gold 3 步（MTBE+O2+NADH+H+→tert-butoxymethanol→tert-butyl formate→tert-butanol+formate）。差异事实：gold 中间体 tert-butoxymethanol、tert-butyl formate 未出现；gold C1 产物=formate，答案 formaldehyde；gold 计量含 NADH/H2O，答案仅列 O2。
     - 段2 TBA→2-羟基-2-甲基丙醛：答案 1 步（TBA+O2→2-hydroxy-2-methylpropanal）；gold 2 步（S04 TBA+O2+NADPH+H+→2-methylpropane-1,2-diol；S01 2-MPD+NAD+→2-hydroxy-2-methylpropanal）。差异事实：gold 中间体 2-methylpropane-1,2-diol 未出现；答案未列 NADPH/NAD+。
     - 段3 醛→2-HIBA：答案 S3 与 gold S03 转化相同（底物、产物一致；gold 列 NAD+/H2O/NADH/H+，答案未列辅因子）。
     - 段4 2-HIBA 之后：gold 走 CoA 激活（S06–S10，终点 acetyl-CoA）；答案走 2-HIBA→methacrylate→3-hydroxyisobutyrate→methylmalonate semialdehyde（gold 主链无这三个化合物；gold 酶集亦无 dehydratase/hydratase 条目）。两侧在 2-HIBA 处分岔。
  3. 计量与结构观察（事实，判定留本人）：
     - 碳数：S1 5C（MTBE）→4C（TBA）+1C（formaldehyde）；S2–S6 均 4C→4C；链无断碳跳跃。
     - 氧化还原/水计量未列：S2（TBA+O2→醛，脱 2H 无还原力受体）、S3/S6（脱氢无 NAD+）、S4（脱水未列 H2O 副产物）、S5（水合未列 H2O 底物）——P103"辅因子遗漏通常属局部计量缺陷"与 P104"简化表达不自动等同不守恒"的适用对象（任务未明确要求完整配平反应式——题面只要求主底物/主产物+酶+菌，辅因子要求见题面要求8 的示例性表述，是否属"明确要求完整反应式"由本人判定）。
     - 名称与 SMILES 对应观察：S5 产物名"3-hydroxyisobutyrate"配 SMILES "CC(O)CC(=O)O"（碳骨架 CH3-CH(OH)-CH2-COOH，无 2-位甲基分支）；S6 产物名"methylmalonate semialdehyde"配 SMILES "CC(=O)CC(=O)O"（骨架 CH3-CO-CH2-COOH，无甲基分支）；两 SMILES 彼此衔接自洽（S5 产物羟基氧化即 S6 产物）。gold 中无同名化合物可对照。名称-SMILES 一致性为可观察事实，是否构成化学错误由本人判定（gold 侧同类观察：gold 2-Hydroxyisobutyrate="CC(C)(C(=O)[O-])O" 为带甲基分支骨架）。
  4. 量表条款（一句话）：R2 行=D2 档位描述；P98 表 R2 D2 关键错误清单="主链第一步即错；反应方向反转；原子明显不守恒且无说明；违反基本化学约束；一步跳到中心代谢物"；P62 与 gold 不同不自动等于关键错误、替代路线四步判断；P100 本条路线名按题面原样填写（路线名本身无偏离，偏离点在路线内容/氧条件字段——氧条件归 D1 小节，P100 两维分别判定）；P103–P105 辅因子与简化表达条款；P29 题面未写终点化合物（终点参照在 gold）。
  5. 包内证据缺口：答案所写 methacrylate 分岔的任何文献/数据库事实卡（含 EVID_001 所指 PubMed 16996055）均无覆盖 → 待联网核查/记 UNRESOLVED；本轮允许联网补证（协调端2026-10-28口径；冻结包构建期不联网，故该声称在包内无卡，联网核查待补），不做路线存在性推断（"检索无结果不等于反应不可能"）。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：gold 10步压缩为6步（2处无依据跳步）触发P62→cap≤4；2-HIBA后分岔未声明替代且文献不可核，档内取3。（把握度：高）

- 本人人工确认与日期：【待本人签】

## REV-B-028-D3a / D3a

核查问题：核对所写酶名、具体EC和该步反应是否对应；通配EC、近名酶或家族关系不能证明具体催化。缺证时保留待核，不凭负检索判酶不存在。

- 答案具体声称与原文位置：
  - 6 步酶条目（全答案共 6 个 enzyme 对象）：
    - S1（offset 510 段内）：name="alkane/ether monooxygenase (methane monooxygenase homologue)"、ec_number=null、gene_or_protein="mmoB-like / alkB-like hydroxylase"、confidence="medium"、evidence_id="EVID_001"；step.uncertainty="起始醚键断裂酶的具体基因与EC尚不确定，多为单加氧酶家族成员。"
    - S2：name="tert-butyl alcohol monooxygenase"、ec_number=null、gene_or_protein=null、confidence="medium"。
    - S3：name="2-hydroxyisobutyraldehyde dehydrogenase"、ec_number=null、gene_or_protein="mhpB-like aldehyde dehydrogenase"、confidence="medium"。
    - S4：name="2-hydroxyisobutyrate dehydratase"、ec_number=null、gene_or_protein="hbd-like"、confidence="medium"。
    - S5：name="methacrylate hydratase"、ec_number=null、gene_or_protein=null、confidence="medium"。
    - S6：name="3-hydroxyisobutyrate dehydrogenase"、ec_number="1.1.1.31"、gene_or_protein="hbdH"、confidence="medium"。
  - 答案自披露：uncertainties[0]="各步酶的EC编号多数未知或仅同源推断，confidence为medium/low。"
  - 本维可核对象：5 步无 EC（无编号核验对象）；仅 S6 的 EC 1.1.1.31 可走编号核验；酶名 6 个；gene_or_protein 4 个（均为"-like"家族式写法）。
- 核查来源/新证据ID及支持范围：
  - 覆盖登记册：EC 1.1.1.31 → OUT_OF_SNAPSHOT_UNRESOLVED（cases_seen=BIOPATH150_125），fact_card_path 空 → 官方 accepted name/reaction/状态在包内不可核 → P71 要求的编号核验无对象（待联网核查）；登记 note 明示"UNRESOLVED不判虚构也不判支持"。
  - facts/IUBMB_EXPLORENZ/ 全部 20 张 EC 卡（1.14.12.11、1.14.12.25、1.14.15.26、1.14.15.28、1.3.1.19、1.3.1.53、1.3.1.86、2.7.1.106、2.7.1.184、3.3.2.3、3.3.2.9、3.3.2.10、3.7.1.5、3.7.1.8、3.7.1.25、4.1.2.55、4.1.2.57、4.5.1.5、5.3.1.31、5.3.1.34）：不含 1.1.1.31，也不含 gold 侧任何 EC（1.14.13.M36、1.1.1.M26、3.7.1、1.14.13.229、1.1.1.400、1.2.1.98、1.2.1.-、6.2.1.M4、5.4.99.64、1.1.1.35、2.3.1.16、2.3.1.9）→ 答案 5 个 null 步与 gold 对应步的 EC 均无包内事实卡可对照。
  - gold/enzyme_gold.tsv（BIOPATH150_125，19 行，见 D1 小节所列）：支持范围=gold 对该路线逐步酶名/EC 的登记基线；不支持范围=gold 非唯一允许答案（P27）、gold 无某酶不构成对答案酶名的反证。
  - gold/organism_gold.tsv（对应步菌）：MTBE monooxygenase/tert-butyl alcohol hydroxylase/tert-butyl formate deformylase 等步登记 Methylibium petroleiphilum（taxid 105560）；2-MPD 脱氢/羟异丁醛脱氢步登记 Mycobacterium sp. ELW1（1547487）、Mycobacterium austroafricanum（39687）等。支持范围：gold 酶-菌逐步对应参照。
  - 包内无答案 6 个酶名中任何一个的事实卡（无 PubMed 16996055 卡、无 MTBE 文献卡、无基因卡）；EVID_001/EVID_002 包内均不可定位为具体条目（见 V04-B-028 复核其他小节）。
- 关键事实（供本人判断，非结论）：
  1. EC 交付状态（事实）：6 步中 5 步 ec_number=null 且两处披露（S1 step.uncertainty、uncertainties[0]"仅同源推断"）；仅 S6 给 EC 1.1.1.31。按题面规则5"未知的EC一律填 null"口径交付。
  2. EC 1.1.1.31 核验状态（事实）：包内无官方卡、登记册 UNRESOLVED → P71 三项（accepted name/reaction/状态）均不可核；包内不存在支持或反驳"EC 1.1.1.31 = 3-hydroxyisobutyrate dehydrogenase 催化 S6 反应"的事实 → 该酶-EC 对应记 UNRESOLVED 待核，不判虚构（P40/P51/P72）。
  3. 与 gold 的酶对照（事实）：答案 S3 酶名"2-hydroxyisobutyraldehyde dehydrogenase"与 gold S03 酶名"hydroxyisobutyraldehyde dehydrogenase"（EC 1.2.1.98/1.2.1.-）近名；答案 S1 酶名含"methane monooxygenase homologue"字样，gold S05 为 MTBE monooxygenase EC 1.14.13.M36（Methylibium petroleiphilum）；答案 S2"tert-butyl alcohol monooxygenase"与 gold S04"tert-butyl alcohol hydroxylase"EC 1.14.13.229 近名；答案无 EC，无法与 gold EC 直接比较；答案 S4–S6（dehydratase/hydratase/dehydrogenase）在 gold 酶集中无对应条目（对应 gold 步不存在，见 D2 小节段4）。
  4. gene_or_protein 字段性质（事实）：4 个值均为家族/同源式写法（"mmoB-like / alkB-like hydroxylase"、"mhpB-like aldehyde dehydrogenase"、"hbd-like"、"hbdH"），答案自述"多为单加氧酶家族成员""仅同源推断"；包内无这些基因的任何证据卡（UNIPROT 两卡为 E. coli YbhB、Xanthobacter 脱卤酶，与本 case 无关）。
  5. 量表条款（一句话）：R3 关键错误清单（P98 表 R3）="EC大类别与反应类型不匹配；酶名与EC互相矛盾；把广谱家族相关性当成该具体反应的催化证据"——本条 EC=null 的 5 步无编号可比，"把家族相关性当具体催化证据"的判断对象是 gene_or_protein 字段与酶名的使用方式（事实已列，判定留本人）；P71–P72 编号核验只给事实状态、不自动给分或cap；P73 通配EC不能反推具体号（本条 gold 侧含 1.2.1.-/1.14.13.M36/1.1.1.M26 等非全数字编号，答案侧无具体号与之冲突）；P63–P68 保守条款（gold 通配/多注集合时先查官方条目——官方卡包内齐缺，只能记 UNRESOLVED）；"缺证时保留待核、不凭负检索判酶不存在"——答案酶名在包内零覆盖属事实，存在性推断不做。
  6. 包内证据缺口：EC 1.1.1.31 官方卡；答案 6 个酶名的任何文献/数据库事实卡（PubMed 16996055）；gold 侧全部 EC 的官方卡；相关基因/蛋白证据卡——均无覆盖，待联网核查。

- 复核结论（保留/修改/仍待核）：修改（REVISE）
- score_status及分数（NE/NA不猜分）：SCORED，3分

- 是否关键错误（是/否/仍待核）及主要结论影响：是（Y）
- 逐维理由与把握度：答案所引PubMed 16996055已核实为HeLa细胞HB-EGF mRNA论文（Sorensen 2006 Exp Cell Res），摘要与MTBE/降解/细菌零词汇交集→已核实错引；真出处已另行定位（Hanson 1999 PMID 10543787、Kane 2007 PMID 17158667）。EC 1.1.1.31官方名与S6逐字一致、S1/S2有基因级文献（mdpA/mdpJ）、S3/S4/S5字面零命中→按A4同口径Y、cap≤4→取3。（把握度：高）

- 本人人工确认与日期：【待本人签】
