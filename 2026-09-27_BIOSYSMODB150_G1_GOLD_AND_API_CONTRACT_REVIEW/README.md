# BIOSYSMOdb150 G1老师审阅包说明

## 这是什么

这是提交给黄老师的G1内容审阅包，不是模型API执行包，也不是G2题目包。

本包请老师审阅：

- 150个case为什么暂定隔离24个；
- G1正式gold候选、quarantine和补选候选；
- 32个缺失SMILES的源头回溯结果；
- 2条S4R1名称错绑但G1未受污染的记录；
- 5个主链结构不可判定case是否继续留在正式实验；
- 性状、范围值、保藏编号和SMILES评分口径；
- 是否条件批准后续G2-G6。

## 本次附带的API探索合同

包内同时放入两份合同，请老师重点比较：

1. `BIOSYSMODB_150_PATHWAY_FIVE_LLM_API_BENCHMARK_MASTER_EXECUTION_CONTRACT_2026-09-23.md`
   - Astra整理的API探索总合同；
   - 说明实验目标、五模型、并发、smoke、pilot、正式调用和本地评分的整体设计；
   - 请老师审阅设计是否合理。

2. `BIOSYSMODB150_API_ANSWER_COLLECTION_EXECUTION_PLAN_2026-09-26.md`
   - 根据黄老师设计裁决改写的实施主合同；
   - 其中G1-G9硬门、指定路线、搜索对称性、评分器冻结和正式全量顺序优先；
   - 如果老师确认设计无问题，后续按这份实施合同执行。

旧的pre-teacher版本不放入本包，避免把已经被老师裁决替换的旧流程混在当前合同里。

## 老师需要先看什么

建议按以下顺序：

1. `BIOSYSMODB150_G1_REVIEW_AND_G2_G6_CONDITIONAL_BATCH_APPROVAL_REQUEST_2026-09-27.md`
2. `25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26/G1_gold/teacher_gold_review.md`
3. `25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26/quarantine/cases.tsv`
4. `25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26/G1_smiles_recovery/local_audit_report.md`
5. `25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26/G1_smiles_recovery_r1/local_audit_report.md`
6. `25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26/gates/G1_gold.stage_gate.json`

其他TSV、manifest、SHA256SUMS和scripts是复核材料。

## 当前结果

```text
原始case：150
G1原quarantine：24
当前formal候选：126
R3建议另隔离的主链结构不可判定case：5
若老师采纳建议，正式主实验：121
```

当前程序门仍为：

```text
status=READY_FOR_REVIEW
next_stage_allowed=false
```

## 验收结果

```text
G1 validator：73454/73454 PASS
G1 mutation：4/4 PASS
G1-R3 SMILES审计：354/354 PASS
G1-R3-R1身份回溯：103/103 PASS
Bailian/LLM API调用：0
```

## 本包不包含

- 原始BIOSYSMOdb大型数据库文件；
- API key或环境变量；
- G2题目；
- 五个模型的新增API回答；
- G8正式全量执行授权。

原始输入的bytes/SHA已记录在`G1_inputs.manifest.json`和`G1_inputs.content_manifest.json`中。

## 老师批示方式

请在主申请文件末尾确认：

- 正式题数选择121还是126；
- 5个主链结构不可判定case如何处理；
- MetaTraits、范围值、F5编号、无SMILES字段的评分口径；
- 是否一次性条件批准G2-G6，商业API上限为80次。

老师批示后，执行方会按批示重新绑定G1 gate；没有老师签署，不能开始G2。
