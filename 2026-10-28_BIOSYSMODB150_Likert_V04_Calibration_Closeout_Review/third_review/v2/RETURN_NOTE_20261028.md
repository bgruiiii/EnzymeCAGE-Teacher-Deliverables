# 交回说明 — GONG_TARGETED_REVIEW_20261027（v2，2026-10-28）

实际裁决人：REVIEWER_C（人工评价者）——本包所有分数与关键错误判定均为其本人拍板；
AI 仅承担事实核查底稿、证据检索与转录，未代做任何裁决（见各 md 确认栏签名要求）。

## 本版相对上一版（DEFER 版 zip）的变化

1. **30 个指定维度全部完成裁决**：A 桶 16 单（D1/D2/D5/D6）+ B 桶 14 单（D3a/D3b/D4），
   无遗留 DEFER/NE。分数与关键错误判定先由裁决人定原则、逐条确认草案后落账。
2. **按协调端 RETURN_FOLLOWUP_20261028 完成两项口径修正**：
   - 底稿中"本任务禁止联网"表述作废，B 桶 14 单已联网补证（官方库优先：
     ExplorEnz/IUBMB、NCBI Taxonomy、UniProt reviewed、PubMed/Europe PMC、BacDive、ATCC）；
   - COVERED_BY_FACT_CARD 类表述已修正为"可定位≠支持"。
3. **联网补证登记**：新增证据 76 条（EV146-01~25 / EV007-01~25 / EV029-01~26），
   合并登记见 `ADDED_EVIDENCE_FILLED.tsv`（列同模板）；三份检索汇总
   （BB_SUMMARY_AGENT146/007/029.md）含逐单元事实清单与失败检索词；
   `ADDED_EVIDENCE_AGENT146_snapshots/` 为 25 个原文快照（sha256 已验证）。
   结果总表第 10 列已把新证据 ID 回填到对应维度行。
4. **未触碰**：复核包原件（gold/、items/、rubric/、review_forms/）一律只读；
   金标内容未外发至任何第三方（联网检索只查官方公共库，检索词不含金标产物内容）。

## 包内清单

| 文件 | 说明 |
| --- | --- |
| `REVIEW_RESULTS_FILLED.tsv` | 30 行结果总表（第 14 列 human_confirmation 待裁决人本人签名） |
| `V04-B-XXX_reviewed.md` ×15 | 每份答案的核查底稿+裁决记录（确认栏待签名） |
| `ADDED_EVIDENCE_FILLED.tsv` | 76 条联网补证合并登记 |
| `ADDED_EVIDENCE_AGENT146/007/029.tsv` | 按检索批次保留的原始登记（溯源用） |
| `BB_SUMMARY_AGENT146/007/029.md` | 逐单元检索事实清单（含阴性检索与失败词） |
| `ADDED_EVIDENCE_AGENT146_snapshots/` | 原文快照 25 件 |

## 交回前必办（裁决人本人）

- [ ] `REVIEW_RESULTS_FILLED.tsv` 第 14 列逐行签名（署名或代号）；
- [ ] 15 份 md 末尾"本人人工确认"栏签名+日期；
- [ ] 确认后交付协调端。

## 遗留提示（供协调端知悉）

- B023-D5 留有备注：taxid 183193 卡（官方名 Streptomyces sp.）与答案声称
  P. putida F1 的错引核实素材已齐备，本次按"统一 P40 档内"口径记 UNRESOLVED，
  裁决人保留升级为关键错误的复核权。
- D6 单点过度确信类（7–8 档）与 P119/P120"单点≠系统性"口径一致，未设 cap。
