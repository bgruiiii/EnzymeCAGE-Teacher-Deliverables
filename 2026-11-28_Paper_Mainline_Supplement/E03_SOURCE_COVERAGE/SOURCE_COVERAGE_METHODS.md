# E03 来源覆盖率与真实缺失说明（Methods 可用稿）

日期：2026-11-26。任务：`PAPER_E03_F02E_PREP_20261126`。本页整理两张已冻结的表——
`MICROBE_UID_EVIDENCE_FOR_PAPER_7468.tsv.gz`（下称 BASE，7468 行来源表）与
`UID_SPECIES_TRACE_7468_R1.tsv`（下称 R1，7468 行派生判定表）——的计数与层级关系。
所有数字经本窗口独立重算核验（见 `COVERAGE_RECHECK.json`），与原件声明值全部一致，无差异。
本轮不补物种、不做新检索、不改变任何缺失定义。

## 1. 三层结构（不同轴，不可相加）

1. **记录层（BASE.source_lookup_status）**：对 7468 条候选酶 UID 逐条做指定来源查询的结果。
   FOUND **7430**、FOUND_SOURCE_SET **7**、NO_HIT **30**、IDENTITY_CONFLICT **1**，合计 7468。
   含义是“该行能否追到一个权威来源记录”，与是否微生物、物种是否已识别无关。
2. **工作定义层（R1.identified_microbe_source_for_followup）**：谓词 =
   `source_record_species_traceable ∧ microbe_scope_accepted ∧ species_identity_state=IDENTIFIED_SPECIES`
   （按已审字段词典）。采用条数 **5579**。辅助层分解：记录可追 7430；范围已接受 5607
   （独立于追溯的一轴）；两轴同时满足 **5601**；其中 22 条 Unknown/uncultured 占位标签
   按已审 `species_identity_state` 单列剔除；5601 − 22 = **5579**。
3. **原始空字段（BASE 列本身）**：`species_name` 原空 **31** 行、`source_signature` 原空 **38** 行
   （严格定义：字段值为空字符串）。检测无空白串或 NA/None 类占位混入。两处缺失**原样保留**，
   不填假物种，也不并入 30/7/1 计数改写。

## 2. 比例口径（分子/分母并列，不选口径）

- 记录层：7430/7468 = 0.994912（约 99.49%，仅展示用；整数不变）。
- 工作定义层：5579/7468 = 0.747054（约 74.71%）。
- 条件比例：5579/5601 = 0.996072，分母为“记录可追且范围接受”层，仅在此条件下引用。

## 3. 层次与措辞边界

- **5579 是候选酶 UID 条数，不是 5579 个物种或菌株**；7468 同理是 UID 行数。
- 7430 记录来源可追 ≠ 都可用于微生物后续推荐（范围、可识别性是另外的判定轴）。
- FOUND_SOURCE_SET 的 7 条按原记录证据单独判定，不宣布“全局无法确定物种”，也不冒充单一来源。
- **NO_HIT 30 只能写“指定查询未命中”**；不得写“无活性”“无来源”“不能降解”。
- IDENTITY_CONFLICT 1 条显式保留，不静默选边。
- C8 记录存在 4845 是**性状资料轴**（本窗口另在 BASE#c8_record_status==OK 交叉观察到同值 4845），
  不是来源判定门；历史歧义 flag 229 与多 proteome 同物种 71 保留原义（71 引自已审计数表，
  本窗口未重算），均不得重编码为 unknown。
- 广义覆盖表（V1 附录）仅作对照，不冒充本轮判定 B；本轮不新算任何 Top-k 来源覆盖率。

## 4. English draft (short)

> For each of the 7,468 candidate-enzyme UID records, the source-lookup status is reported at the
> record level: 7,430 FOUND, 7 FOUND_SOURCE_SET, 30 NO_HIT, and 1 IDENTITY_CONFLICT (sum 7,468).
> A reviewed working definition for follow-up microbe sourcing additionally requires microbe-scope
> acceptance and an identified species label (excluding 22 registered Unknown/uncultured placeholder
> records among the 5,601 traceable-and-accepted UID records), yielding 5,579 UID rows
> (74.71% of all rows; 99.61% of the 5,601). These 5,579 are candidate-enzyme UID rows, not 5,579
> distinct species or strains. NO_HIT rows are reported strictly as query misses under the specified lookup, not as absence of activity, absence of any source, or non-degradability.
> Fields originally empty in the frozen table (31 species_name, 38 source_signature) are kept as
> real missingness and never imputed. C8 record presence (4,845) is a trait-evidence axis and not a
> source gate.
