# BIOSYSMOdb150 G2老师审阅包

本包是G2题面生成和泄漏审计材料，不是API执行包。

## 当前结果

```text
formal cases=121
rendered messages=121
unexplained leakage hits=0
teacher sample=13
G2 validator=199/199 PASS
API calls=0
G2 status=READY_FOR_REVIEW
next_stage_allowed=false
```

## 老师重点审阅

- `teacher_review/G2_TEACHER_REVIEW_REQUEST_2026-09-27.md`
- `G2_questions/G2_BUILD_REPORT.md`
- `G2_questions/teacher_sample_review.tsv`
- `G2_questions/leakage_hits.tsv`
- `G2_questions/allowed_input_atoms.tsv`
- `G2_questions/rendered_messages/`

本轮发现14个ROUTE_GOLD_COLLISION，已保留并逐题标注，没有自动放行；93个case没有可靠氧条件，题面使用null，没有猜测；13题固定种子抽样等待老师人工审阅。

## 上游绑定

本包绑定G1 gate PASS、老师G1批复和G1 manifest。G1完整gold包仍在前一份教师交付包中。

本包不包含API key，不包含模型回答，不启动G3/G4/G5/G6。
