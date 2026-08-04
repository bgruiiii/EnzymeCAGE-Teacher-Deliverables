# M3 三个技术问题修复稿与证据包索引（2026-08-04）

黄老师 2026-08-03 反馈中点名的 F1/F2/07-22 原件回传材料，以及后续已补齐的 F4/F5 证据，已集中放在：

```text
2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/
```

重点文件：

```text
M3_TEACHER_THREE_TECHNICAL_QUESTIONS_COMPREHENSIVE_RESPONSE_CORRECTED_2026-08-04.md
M3_Q3_BIOTRANSFORMER_ENVMICRO_SOURCE_AND_JAR_IDENTITY_EVIDENCE_2026-08-04.md
README.md
DELIVERABLE_SHA256SUMS.txt
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
```

本次修复重点：

```text
1. 修复 Q1 §1.2 P2Rank 事实错误：
   官方公开仓库 commit 255a05e167aabc70f6c0322a00702cdc9d6ebfbc
   存在完整 P2Rank 脚本链。

2. 补充 mix-af-p2rank 出处：
   见官方 config/infer/*.yaml 的 feature asset 文件名。

3. 同步 Q1 四份 audit、Q2/Q3 文档和 07-22 原件。

4. 07-22 原件 SHA256：
   80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0

5. 追加关闭 F4：
   Q2 代码行号已统一到官方公开 commit 255a05e167aabc70f6c0322a00702cdc9d6ebfbc；
   `config/train/pretrain_esm2_3b/seed_42.yaml` 已说明为本项目 Chenyu/本地 ESM-2 3B corrected-pocket 正式运行配置，
   不是官方公开仓库自带配置。

6. 追加关闭 F5：
   新增 BioTransformer ENVMICRO 源码摘录与 jar 身份证据；
   HPC 返回包记录 `actual_commit=7149f7ec6b2f32f9f789bab53aa4a71db49e59e2`，
   jar SHA256 为 `e5c3c27de7dfc87b448f1eed6fe986ef48ed90c53bad9b848f95378f08efee80`。
```

仍在继续推进、不在本索引中冒充完成：

```text
F3 全库缺口基数与可补齐率估算；
F6 弓师兄模型 18 条 blind 评分。
```

D5 MetaTraits 新合同预调研复审/补齐不放在本 EnzymeCAGE teacher-deliverables 包中；其根目录索引已放在 MetaTraits teacher-deliverables 仓库：

```text
/home/a/EnzymeCAGE-MetaTraits-Teacher-Deliverables/METATRAITS_D5_2026_08_03_TEACHER_LIST_RECONFIRMATION_INDEX_2026-08-04.md
```
