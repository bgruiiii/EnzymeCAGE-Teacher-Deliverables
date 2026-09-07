# 阶段证据状态索引

日期：2026-09-07

本页只列本次阶段反馈所依据的关键身份和裁定，不上传大型HPC archive、restricted答案或凭据。

## 1. T2 owner bundle

```text
remote commit=9f5ad0bfa71c06471a53891ec7be40af4ff07fc2
tree=3660d3bca88db943df4acdbff3e39246dac2a726
bundle manifest=30/30
templates.tsv.gz bytes=31059
templates.tsv.gz SHA256=19ac04ca4d6c516f7dce0f7536959847bec91ba81a68384c58551ead18ebe4f1
```

## 2. T2B最终采用的staged累计patch和技术结果

```text
SOURCE_PATCH SHA256=3b592f744feec2f5d2dcc6508a87e457a0bd35aa199a34780dec7d95d974bd10
changed set=5 files
depth1 result SHA256=98326cd6cf95bb608650ca5617b7c5c42b2cd51333cb57040638b738c3f48f29
depth1 fresh generated before cap=48
depth1 returned Top-10=10
depth2 engine invocation=1
depth2 returned records=2
rankers=uspto/envipath/retrieval
verdict=PASS_WITH_LIMITATIONS_READY_FOR_T2C
```

R4返回archive：

```text
bytes=8301381
SHA256=1e7052190c1ef6e4757941c2988fb324d1dd482d55ffa58eccdc0c4f5211610d
manifest=27/27 OK
```

限制：R4高级访问审计发生自递归，外置identity/validation尚未本地收件；这些不作为正式成果证据。

## 3. 统一证据链

已冻结并通过结构/枚举/跨字段及负例检查的主要关系：

```text
query → route → reaction_task → enzyme → organism aggregate → trait → evidence record
```

关键公共键：`route_id`、`reaction_task_id`、`enzyme_uid`、`source_signature`、`source_tool`、
`source_record_id`、`model_version`、`evidence_hash`。

## 4. T5 staged合同轨

```text
T5A=PASS_WITH_LIMITATIONS
T5B=TECHNICAL_PASS_WITH_LIMITATIONS_VALIDATION_RECEIPT_DEFERRED
T5C=PASS_WITH_LIMITATIONS_CONTRACT_TRACK
T5_OVERALL=PASS_WITH_LIMITATIONS_STAGED_CONTRACT_ONLY
```

已证明：UID→source映射、C8只读adapter、证据层级、宿主跨步骤聚合合同、trait precedence/conflict、真菌缺失
fail-closed。未证明：基于T2/T3真实多步路线的完整性状整链。

## 5. 当前阶段门

```text
G0合同门=PASS
G1源码门=PASS
G2基线门=PASS
G3 schema门=PASS
T2B=PASS_WITH_LIMITATIONS_READY_FOR_T2C
T2C/T2D=IN_PROGRESS/NOT_COMPLETED
T3=BLOCKED_BY_T2
T4=BLOCKED_INPUT_MISSING
T5=PASS_WITH_LIMITATIONS_STAGED_CONTRACT_ONLY
T6/G7=BLOCKED_BY_T2_T3
G8模型角色门=BLOCKED_BY_T4_AND_TEACHER_REVIEW
```
