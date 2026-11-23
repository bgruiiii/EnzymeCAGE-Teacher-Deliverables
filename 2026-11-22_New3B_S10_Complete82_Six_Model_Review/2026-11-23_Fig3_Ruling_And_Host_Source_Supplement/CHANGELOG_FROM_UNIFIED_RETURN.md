# CHANGELOG FROM UNIFIED RETURN（R1 定向返修，2026-11-23）

范围：仅B/D字段与收口说明；A/图3a/3b/第六规则等已通过数值**零重算、零改动**，逐字节复制入`approved_numeric/`并在`APPROVED_ARTIFACTS_REGISTER.tsv`登记来源SHA（与review/ACCEPTED_NUMERIC_IDENTITIES.json逐一对上）。

## B（review F01/F02）
1. `UID_SPECIES_TRACE_7468_R1.tsv`：新增三列一标志——`source_record_species_traceable`（记录层可追，7430）、`microbe_scope_accepted`（范围层）、`species_identity_state`（ENUM：已识别7408 / **占位未识别22** / source-set 7 / no-hit 30 / 冲突1）、`identified_microbe_source_for_followup`（**工作定义=traceable∧scope=true∧不在22名单，基线5579**）。
2. 22个占位UID按 review F01 已登记名单精确单列（taxids 2725×3/1781162×1/77133×16/201089×1/171953×1；逐行带`source_locator`指回F01与B1），未用正则泛化、未联网、未改B1。
3. 原5601保留为"记录可追溯且范围已接受"的基础层计数，**不再等价"均可推荐物种"**；多proteome同物种71、历史歧义flag 229保留原证据含义（检查`ambiguity_flag_not_recoded`证明无一被改判未知）；source-set能否到物种仍以原记录证据为准。
4. `SPECIES_FIELD_DICTIONARY_AND_JOIN_PROTOCOL_R1.tsv`给师姐明确答案：采用列=`identified_microbe_source_for_followup`，谓词一句话已写，文件/列名固定；强调其含义止于"后续候选来源物种证据"，不证可培养/可购买/整链功能。
5. **V1覆盖表撤回"可直接作判定B最终数"建议**：在`approved_numeric/`中按原字节保留，登记为**广义来源追溯对照附录**（含非微生物来源与占位标签）；596行谓词差异引用review F02，本窗口不生产新的正式覆盖率。

## D（review F03）
1. `CASE_EXPORT_PROTOCOL_FIELDS_R1.tsv`：三证据轴物理分开——A召回依据（StepResult.groups/RecallGroup字段、PoolCandidate.provenance_records[]的source_datasets/accessions/evidence_tiers等**检索构池原字段**；冻结池验证运行没有召回记录的族显式标NOT_AVAILABLE，不从B1/T2反推、不凑四选一）；B生物来源绑定（HostSource全嵌套字段+R1物种三列）；C模型是否实际评分（execution_mode REAL_FORWARD/CACHE_REPLAY/TEST_ONLY、scoring_status、forward_executed、全量all_candidate_scores与Top-k切片分列、typed未评/未披露、GOLD_NOT_AVAILABLE）。
2. `CASE_EXPORT_RUN_CONTRACT_R1.json`：run_id/起止/五seed身份/mode推导规则为导出层契约；RT-ID标REQUIRES_C_WIRING。
3. `CASE_EXPORT_EXAMPLE_SCHEMA_ONLY_R1.json`：按三轴重写示例；注明两份R4 RAW只覆盖axis-C评分证据，axis-A/B来自带检索与来源后端的工具运行，**不声称所有列已在两份RAW里**；两固定步不同路径、缓存示例不改成真实标签的原有声明保留。
4. 未生成/运行任何新真实案例。

## 收口项
- **CHECKS**：3c构成改为按实际校验（84=60旧规则附录+24第六规则附录），废除"expected 132"错误声明；`e is None or True`恒真检查删除，换成对release decision原件断言（uid=="Q66Q78"、acceptance/cause、22/4/3）。EnzGFM拆批措辞沿用原审计原句（名次变化≠全部Top1变化；新臂Top1变化2步）。
- **C**：措辞校正——"约2个工作日"为有前提估计；授权对象是**隔离接入分支/目标代码线由维护者合并部署**，不是默认直改main；现场/远端版本号仅为历史核查证据，本轮未新查在线状态；未获授权不启动接线。
- **RUN_END/MANIFEST顺序**：本包先落`RUN_END_UTC.txt`再生成`MANIFEST.tsv`并磁盘复核。BASE包"RUN_END在清单后被改写、仅该文件SHA不符"的情况如实保留在本说明，未倒改BASE。

## 未动清单
review目录只读引用；BASE/全部原产物、协议、掩码、封签、旧覆盖率明细未改写一个字节；228主口径、已通过60/72行区间、12匹配步、四套保留集不变。
