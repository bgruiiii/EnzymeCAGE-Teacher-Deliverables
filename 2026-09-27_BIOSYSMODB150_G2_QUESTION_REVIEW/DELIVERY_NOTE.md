# BIOSYSMOdb150 G2题面审阅包

本目录是G2题面生成与泄漏审计交付，不是API执行结果。

主压缩包：

`../2026-09-27_BIOSYSMODB150_G2_QUESTION_REVIEW.tar.gz`

SHA256见本目录的 `ARCHIVE_SHA256SUM.txt`。

当前结果：

```text
formal cases=121
rendered messages=121
unexplained leakage hits=0
ROUTE_GOLD_COLLISION=14 cases
PENDING_OXYGEN_REVIEW=93 cases
teacher sample=13 cases
G2 validator=199/199 PASS
API calls=0
G2=READY_FOR_REVIEW
```

请优先查看压缩包内：

1. `teacher_review/G2_TEACHER_REVIEW_REQUEST_2026-09-27.md`
2. `G2_questions/G2_BUILD_REPORT.md`
3. `G2_questions/teacher_sample_review.tsv`
4. `G2_questions/leakage_hits.tsv`
5. `G2_questions/rendered_messages/`

G2仍等待老师13题人工抽审，未启动G3、G4、G5或G6。
