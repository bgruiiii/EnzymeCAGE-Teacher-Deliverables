# 2026-10-28 v0.4小样本校准收尾审阅包

状态：整理/统计已独立核对；当前申请在老师认可v0.4后尽快启动120题/480份全量AI辅助评分。人工抽查由老师统筹，尽可能并行，不由执行器新增前置轮次。量表及全量执行均尚待批准。

## 当前核心请示：尽快全量出分

[条件式全量评分申请](FULL_SCORING_AUTHORIZATION_REQUEST_20261028.md)：不重采样原模型、不改原答；只做出分必需的核验适配和合同锁定。
人工抽查的人数/样本量/时间交黄老师安排；若有不可豁免前置，请一次明确最小范围，其余小修/单项保留不要阻塞整批。
这是申请，不是将原方法自动改为已批准的480份AI评分；正式调用须在确认后按版本/费用上限执行。原DECISION_REQUESTS.tsv保留为历史校准收尾请求，本次启动目标以本申请和TEACHER_REPORT为准。

## 阅读顺序
1. [详细反馈](TEACHER_REPORT.md)
2. [老师要求与本次交付对照](TEACHER_REQUIREMENT_DELIVERY_MATRIX.tsv)
3. [完整候选Word](rubric/LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1.docx) / [纯文本](rubric/LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1_TEXT_EXTRACT.txt)
4. [逐维统计](tables/DESCRIPTIVE_AGREEMENT_BY_DIMENSION.tsv)、[方法与来源](METHOD_AND_RECORD_PROVENANCE.md)、[AI参与记录](AI_ASSISTANCE_PROVENANCE.md)
5. [30维裁决](tables/ADJUDICATION_30_DECISIONS.tsv)、[修订](tables/ADJUDICATION_CHANGELOG.tsv)、[B001保留](B001_D2_SCIENTIFIC_RESERVATION.md)
6. [独立审计](audits/ASTRA_CLOSEOUT_AUDIT_20261028.md)、[公开数据校验](PUBLIC_REVIEW_VALIDATION.json)

## 数据路径
- [32份匿名原题与答案](answers/) / [对应关系](tables/ORIGINAL_32_ITEM_PAIRING.tsv)
- [A原分](inputs/A/ratings_initial_frozen.tsv) / [32份理由](inputs/A/case_reviews/)
- [B原汇总](inputs/B/SUMMARY_PREREVIEW.md)
- [224维原始对照](tables/ORIGINAL_224_DIMENSION_PAIRS.tsv) / [触发清单](tables/DISPUTE_TRIGGER_REGISTER.tsv)
- [v2历史底稿](third_review/v2/) / [确认回复公开稿](third_review/CONFIRMATION_RESPONSE_PUBLIC.md)
- [新证据76条](evidence/ADDED_EVIDENCE_REGISTER_76_NORMALIZED.tsv) / [本地快照SHA核对索引](evidence/SNAPSHOT_INTEGRITY_INDEX.tsv) / [原规范化事实快照](evidence/frozen_snapshot/)
- [政策矩阵](tables/POLICY_FINALIZATION_MATRIX.tsv) / [定稿备忘](V04_FINALIZATION_MEMO_CANDIDATE.md)

32份/224维、219数值对；30维/15份定点；确认后3分数/2KE修订，候选KE=9是/11否/10待核。
B自述AI预评分、A历史经历及流程偏离如实保留，统计仅描述已收意见，不冒称严格独立H1。
25份原文的本地哈希通过不代表本仓库含raw或76条均已独立认证。[公开/未公开边界](CONTENTS_AND_ACCESS_BOUNDARIES.md)。

## 下载和复算
[整体下载本期公开审阅包](archives/LIKERT_V04_PUBLIC_TEACHER_REVIEW_20261028.tar.gz)

只需Python标准库、无需本地工作区、不联网：
~~~bash
python3 scripts/verify_public_statistics.py --base .
~~~

[MANIFEST.sha256](MANIFEST.sha256)校验整个日期目录；[PAYLOAD_SHA256SUMS](PAYLOAD_SHA256SUMS)校验下载包内payload。
[来源索引](SOURCE_FILE_INDEX.tsv)记录原件和公开衍生件。不得用讨论后分数覆盖原分。
