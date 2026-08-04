# 2026-08-04 M3 三个技术问题修复稿与证据包

本目录回应黄老师 `TEACHER_REPLY_M3_COMBINED_THREE_QUESTIONS_AND_NEXT_STEPS_2026-08-03.md` 中 §9.5 的 P0/P1 证据交付要求。

## 本包已覆盖

### F1：Q1 §1.2 P2Rank 表述修复

已在以下文件中修复：

```text
M3_TEACHER_THREE_TECHNICAL_QUESTIONS_COMPREHENSIVE_RESPONSE_CORRECTED_2026-08-04.md
M3_TEACHER_TECHNICAL_QUESTIONS_Q1_Q2_CORRECTED_DRAFT_2026-08-04.md
```

修复口径：

```text
此前“公开仓库没有完整 P2Rank 生成脚本”的表述不成立。
以官方公开仓库 commit 255a05e167aabc70f6c0322a00702cdc9d6ebfbc 为准，
scripts/extract_p2rank_pockets.py 与 scripts/run_mining_pipeline.py 构成完整 P2Rank pocket 生成链。
本轮路线 C 应表述为“官方公开 P2Rank pocket 生成流程的复现”；在本项目证据分级中，它可作为 lower-evidence predicted-pocket fallback / 对照。
```

`mix-af-p2rank` 出处也已补入修复稿：该字符串见官方 commit `255a05e167...` 的 `config/infer/Enzyme-405.yaml`、`config/infer/Orphan-335.yaml`、`config/infer/case-study/glutarate.yaml`。

### F2：证据文件同步

本目录包含：

```text
Q1 四份 on-demand D4 / P2Rank / failure audit；
Q2 分数语义与 AutoDock 辅助策略文档；
Q3 BioTransformer ENVMICRO 内部机制与结果路径文档；
Q3 BioTransformer ENVMICRO 源码摘录与 jar 身份证据；
修复后的三问题综合回复；
07-22 RHEA:11880 公平性裁定原件；
DELIVERABLE_SHA256SUMS.txt。
```

### F3：全库 missing-pocket / missing-D4 缺口基数估算

本目录新增：

```text
M3_F3_LOCAL_ENZYME_ASSET_POOL_AND_EC_EXPANSION_GAP_AUDIT_2026-08-04.md
```

当前统计边界为本地 release-pinned Rhea 140 / reviewed UniProt 基线，不冒充 live UniProt 全库。

核心结论：

```text
raw Rhea-linked UID                  236,103
strict cleaned main-table UID        195,743
Rhea official complete-EC source UID 218,010
uid2seq sequence coverage            236,103 / 236,103
strict valid pocket rows             191,062 / 195,743
strict UID missing valid pocket        4,681
local ESM2-3B corrected features     107,705 UID
strict UID missing local ESM2-3B      88,038
complete-EC source UID missing local ESM2-3B 114,804 / 218,010
```

### ①：07-22 原件回传

本包内：

```text
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
```

其 SHA256 为：

```text
80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0
```

与黄老师要求的原件哈希一致。

## 尚未在本包关闭

以下仍按老师优先级继续推进，不在本包冒充完成：

```text
F6：弓师兄模型 18 条 blind 评分。
```

## 2026-08-04 追加关闭项

```text
F4：Q2 官方 commit 行号统一复核 + 3B 配置来源说明；
F5：Q3 BioTransformer 源码摘录 + jar 包 SHA256。
```

F5 新增文件：

```text
M3_Q3_BIOTRANSFORMER_ENVMICRO_SOURCE_AND_JAR_IDENTITY_EVIDENCE_2026-08-04.md
```
