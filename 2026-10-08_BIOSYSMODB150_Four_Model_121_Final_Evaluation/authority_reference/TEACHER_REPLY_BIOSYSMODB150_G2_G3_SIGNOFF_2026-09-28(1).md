# 老师侧批复：G2 内容回签 + G3 六项口径裁决

- 日期：2026-09-28
- 收件：评测实施学生（陈浩然侧）
- 性质：**G2 PASS 回签 + G3 评分口径冻结批准**（对 `BIOSYSMODB150_G2_G3_CONSOLIDATED_DECISION_AND_G4_G9_READINESS_REPORT_2026-09-28.md` 的签署回复，**以 V2 合并包内容为准**）
- 审阅材料：`2026-09-28_BIOSYSMODB150_G2_G9_FINAL_CONSOLIDATED_REVIEW_V2` 包（主决策稿、G2 build report、13 题抽审表、121 道渲染题面、leakage_hits / allowed_input_atoms、G3 决策卡与 mock 敏感性、G3 score_recipe 候选稿、参数审计、各 stage gate）。已抽查渲染题面 4 道（BIOPATH150_009/019/020/054）并核对 mock 敏感性数据；V2 相对前一版主决策稿的唯一变化为新增 §4.4 参数审计节，已一并审阅。
- 本文件确认后由学生侧计算 SHA256，作为 G2 PASS、G3 冻结与 G4 Chenyu 包的共同 approval_source。

---

## 一、G2 回签（§二）

### 2.2 路线限定词碰撞（14 题）—— ✅ 同意推荐方案

保留最小路线限定词用于指定路线与分支消歧；题面直接披露的名称在评分时标记 `CONTROLLED_INPUT`，**复述该名称不计模型自主 recall**；其余上下游步骤、方向、连接、酶菌、结构照常评分。

### 2.3 氧条件 null（93 题）—— ✅ 接受

源库无可靠记录时 `oxygen_condition=null`（PENDING_OXYGEN_REVIEW），不猜测。路线消歧责任由题面 `chosen_route_name` 原样锁定承担，null 不构成路线自由化。五模型输入一致，公平性无问题。

### 2.4 13 题人工抽审 —— ✅ 通过

抽查确认：甲苯双 case（019 via 4-methylcatechol / 020 to benzoate）消歧明确；「`chosen_route_name` 必须原样填写、不得改选」的反自由化指令在位；模板样板「可复制成员、不是答案、不得照抄」的说明在位；null 不编造指令在位。BIOPATH150_144 按同一碰撞政策处理。

**两处记录性意见（不阻塞 PASS）**：

1. 抽审 13 题的实际构成是碰撞题 13/14 全覆盖，与「固定随机种子抽样（seed=20260927）」的表述不一致。碰撞题全审是更严的正确选择，但 G9 报告中抽样策略要如实描述（高风险全覆盖 + 随机补足，还是纯随机恰好命中——按实际写）。
2. BIOPATH150_141 英文名 `S-[1-(2-hydroxyethyl)-1-methylbutyl]-(l)-cysteinylglycine` 的小写 `(l)-` 前缀有立体化学标示歧义（l/L/I 混淆风险）。是否修正由学生决定；若改题面按既定流程重算 G2 及下游 hash，并在 invalidation_ledger 登记。

### G2 结论：**PASS**

## 二、G3 六项口径裁决（§三）

| # | 裁决 | 说明 |
|---|---|---|
| D1 性状组合 | **B**：word-preference 格剔出数值准确率分母，另报 TEXT_COVERAGE | all_correct 归一 100 靠重定义可评分格实现，非调权；all_wrong=0 不受影响 |
| D2 层内子项与 pair | **独立子项等权；pair 按物种/菌株名称一致即计对；主动填错 TaxID 判 IDENTITY_CONFLICT 且 pair 错；TaxID=null 时 pair 仍可按名称计对、TaxID 子项记 miss** | 维持「编造劣于弃权」的激励方向 |
| D3 步骤对齐 | **Jaccard 阈值 0.5；方向 A→B≠B→A；稳定 ID tie-break；split/merge 不设人工宽免** | mock 上 0.4/0.5/0.6 无区分度（partial 恒 77.78）——批准 0.5，但 G9 报告须承认 mock 敏感性局限；真实评分中若发现阈值敏感案例，**记录备案，不许中途改阈值** |
| D4 overclaim | **仅独立报告 + 证据轴统计，不从科学分扣分** | 敏感性表已显示科学分扣 1pp/条会让 honest null 相对编造的排序翻转风险；禁止任何使 null 劣于编造的扣分设计 |
| D5 F14 单源 | **genome accession 只以 `traits.F14.value.genome_accession` 为正式来源；profile 级兼容字段不一致判 CONFLICT** | 单一事实源 |
| D6 achiral | **主 SMILES 分恒为 isomeric canonical；achiral 仅附表 + 敏感性参考** | 与 9-26 裁决一致 |

G3 冻结条件（学生 §三末尾自述，确认生效）：按以上口径重跑三 mock，all_correct=100（按冻结可评分集合）、all_wrong 核心 recall=0、partial 与手算一致，方得 G3=PASS。

## 三、G4–G9 离线就绪确认（§四，知悉不回签）

### 3.0 V2 新增：五模型官方参数与价格审计（§4.4）—— 知悉并确认两条处置

1. **ZHIPU/GLM-5.3 三项 UNKNOWN**（最大输出 / 搜索 / 结构化输出，无 exact-ID 功能卡片）：不得以相似型号（如「glm-5.3 阿里云直供」）的证据借用补齐，保持 UNKNOWN 进入 G4；若 G4 搜索探针对 GLM-5.3 判 NOT_PASS，按既定规则主实验五模型统一 `enable_search=false`，不为此单独重试或放宽探针判据。「官方支持 ≠ 真实生效」的区分保持。
2. **DeepSeek 忙/闲价**（北京时间 8:00–22:00）：G7 预算文件必须同时给出忙时上界与实际运行时段口径，缺一不回签。

确认纪律项：proposed patch 未自动应用、runtime config 未改动、参数审计 validator（409/409）定点纠正记录已见。参数 UNKNOWN 缺口随 G4/G5 真实观察与 G7 披露补齐，现在不作任何参数调整的理由。

离线准备数字记录：Chenyu 包 validator 27/27、故障演练 39/39（429/503/timeout/半截 SSE/length/坏 JSON/空正文/重复 chunk/断点恢复）、密钥扫描 0、G8 矩阵 605 行全 NOT_DISPATCHED、G9 synthetic 30/30、±5pp 敏感性 10 组归一、总装 337/337。**全部状态为离线预演，不构成任何 live 授权**。

回签后的授权序列确认不变：G2 PASS → G3 冻结 → G4 探针（≤15 次）→ G5 smoke（15 次，15/15 门）→ G6 pilot（50 次，49/50 + 截断 ≤10% + 形态抽审）→ **G7 预算单独回签** → G8 正式 605 次。商业 API 总上限 80 次（G4+G5+G6）有效；G5 失败后重跑须重新报批；G7/G8/G9/quarantine/自由路线本次均不授权。

---

