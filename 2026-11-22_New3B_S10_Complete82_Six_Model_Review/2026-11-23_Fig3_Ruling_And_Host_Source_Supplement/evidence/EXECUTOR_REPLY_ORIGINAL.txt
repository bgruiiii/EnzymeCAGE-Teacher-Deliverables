# 给师姐的统一返包回复 R1（待主审，未发送；2026-11-23）

相对上一稿：B 的字段判定已按主审意见修正为**三层分离**，D 的证据轴已拆开；A/C/E 仅措辞收口。已通过数值全部原样保留（SHA登记见`APPROVED_ARTIFACTS_REGISTER.tsv`）。

## A. V6 第六套规则（不变）
掩码与保留数：382→370、338→326、主262→250、主228→216（剔除同为12个同方向匹配步）；清单`approved_numeric/V6_MATCHED_REACTIONS_12.tsv`、封签`SIXTH_RULE_PREMETRIC_SEAL.json`。只进3c敏感性；不替换主口径；第六规则成绩为V1期附录，不再重算。

## B. "能追到来源物种"字段（已修正，请用R1文件）
1. **采用列**：`UID_SPECIES_TRACE_7468_R1.tsv#identified_microbe_source_for_followup`（7468行，join键=scientific_uid+`join_key_sequence_sha256`）。
2. **精确谓词**：`lookup_status=FOUND ∧ 权威来源键非空 ∧ cur_species_tax_id非空 ∧ in_microbe_scope=true ∧ 不在22个已登记Unknown/uncultured占位名单`，且候选序列SHA与B1行一致。一句话含义：**该候选有一个已识别、已接受为微生物范围的来源物种，可作为后续候选来源物种证据**；不证明可培养、可购买或整链功能。基线**5579**。
3. 各层数字（`SPECIES_TRACE_STATUS_COUNTS_R1.tsv`）：记录层可追7430（含非微生物与占位）；范围已接受5607；记录可追∧范围已接受=5601（保留为记录层基础数）；**占位未识别22单列**；已识别微生物来源5579；source-set 7、no-hit 30、冲突1分列；C8的4845只是性状库记录轴、不是来源门；多proteome同物种71与历史歧义flag229保留原义，不判未知。
4. 你问的"1798 false但source_found"：**确认你的理解正确**——"有来源"与"可用微生物"两层，判定落在acceptance+identifiability上，本列即该组合。
5. 覆盖率：请用上述列自行计算判定B（你接手项）。上一版11,760行覆盖表保留为**广义来源追溯对照附录**（含植物等非微生物来源与占位标签），不作最终判定B；两口径差异主审已独立给出596行清单（review F02）。

## C. 接线与排期（措辞收口）
需要黄老师**书面授权**，对象是**隔离接入分支/目标代码线**、由维护者合并部署——不是默认直改main。前提（授权+目标代码线确认+输入合同+GPU窗口）齐备后估计约2个工作日（接线协议与离线验证1天＋有界真实运行验收1天）；未获前提则明确"暂不接线"，案例图按D先对齐字段、等验收一次成图。版本号快照属历史核查记录，本轮未新查在线状态。

## D. 真实案例逐步导出协议（已按三轴重做）
`CASE_EXPORT_PROTOCOL_FIELDS_R1.tsv` + `CASE_EXPORT_RUN_CONTRACT_R1.json` + `CASE_EXPORT_EXAMPLE_SCHEMA_ONLY_R1.json`：
- **轴A 召回依据**：来自检索/构池原字段（RecallGroup 组信息、PoolCandidate.provenance_records 的 source_datasets/accessions/evidence_tiers、sources/evidence_tiers tokens）；冻结池验证运行没有族记录的写NOT_AVAILABLE——不从B1/T2反推、不凑"登记/EC/兜底/仅打分"四选一。
- **轴B 生物来源绑定**：HostSource 全字段（状态/权威键/路线/物种/菌株/代表登记/evidence_ids/文件行定位）+R1三列物种判定。
- **轴C 模型评分状态**：execution_mode（REAL_FORWARD/CACHE_REPLAY/TEST_ONLY）、scoring_status、forward_executed、API请求数、**全量all_candidate_scores与Top-k前缀分列**、typed未评/未披露、Gold缺失时`GOLD_NOT_AVAILABLE`（不是候选全错）；性状逐槽OBSERVED/PREDICTED/MISSING/IDENTITY_ONLY+每后端ERROR/NOT_CONFIGURED，观测与预测可并存、登记单列。
- 已落盘范围如实标注：两份R4 RAW只覆盖轴C；轴A/B由带检索与来源后端的工具运行时产生；run_id/RT-ID属导出层/接线层契约。两固定步不同路径、不可拼整链；缓存示例不改真实标签。未生成新案例。

## E. 逐臂数值限制（定稿确认）
你的E段写法按原审计文本确认：旧600M 1e-5 replay门保留原披露；新600M 171步超0.05 logit门、正式概率最大差0.0148868、70步名次变化但Top1与Hit@1/3/5/10不变；EnzGFM拆批为**名次变化**——E0 10步/140候选、新臂19步/411候选，其中**新臂Top1变化2步**、1步Hit@5变化（不把10/19步都写成Top1变化）；新3B例外为**单个UID `Q66Q78`**（非Q66/Q78两对象；ACCEPT_FIXED_S10_REPLICATION_ONLY、原因UNVERIFIED、train22/valid4/test3），机器断言见`LIMITATIONS_CONFIRMATION_Q66Q78_R1.json`。无新增数值补测。

## 状态
本稿为待主审的返修统一稿：未发送、未上传；228主口径与所有已通过数值未动。
