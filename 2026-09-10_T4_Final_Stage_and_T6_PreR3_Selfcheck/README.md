# 2026-09-10 T4最终封口阶段 + T6进入R3前microbe自查

黄老师您好，本目录是陈浩然侧对您09-09回复的当前正式返回。

建议先看：

1. [`RESPONSE_TO_HUANG_TEACHER_T4_FINAL_STAGE_T6_PRER3_SELFCHECK_AND_REWORK_EXPLANATION_2026-09-10.md`](RESPONSE_TO_HUANG_TEACHER_T4_FINAL_STAGE_T6_PRER3_SELFCHECK_AND_REWORK_EXPLANATION_2026-09-10.md)
2. [`T6_ITERATION_REASON_TIME_AND_OUTCOME.csv`](T6_ITERATION_REASON_TIME_AND_OUTCOME.csv)
3. [`T6_R3A_R2A_R3_FINAL_LOCAL_AUDIT_2026-09-10.md`](T6_R3A_R2A_R3_FINAL_LOCAL_AUDIT_2026-09-10.md)

## 当前状态

```text
T4科学/评测内容：已完成并通过内容审计；只剩R4 external closure三文件封口
T6进入R3前microbe自查：已完成并通过本地审计
T6-R3真实LangGraph invoke/stream：未运行
C8→T5真实连续回归：未运行
T6 overall/G7：未通过
```

T4不是仍在跑模型。depending v3.2和ECLIPSE正式18条runtime-blind结果已冻结；R4只修最终交付顺序，不改变预测、指标、重合或ECLIPSE统计。

T6本轮按老师要求关闭：8001依赖、4 UID/8 records entryType、direct REST、冻结reviewed UID map fallback、UNRESOLVED、NCBI TaxID聚合、host evidence和G-SCHEMA。三文件均在本目录。

## 为什么改了多轮、为什么慢

主报告和逐轮CSV已诚实区分：

```text
必要纠正：production节点接线、104MB map fallback、TaxID与G-SCHEMA；
可避免返工：我们混用了聚合合同、写错row-hash/名称口径、旧报告混入、validator固定PASS和sidecar循环；
责任：属于我们的提示词、报告生成器和validator设计返工，不是学生操作慢；
后半段没有GPU/模型运行，长耗时主要来自多轮审计和重新实现。
```

## 请老师确认

我们已完成您要求的T6进入R3前自查。请确认是否按您09-09已修复拓扑立即启动真实T6-R3；学生侧不会修改graph/state/router/edge。

T4模型角色仍按中立A/B请求等待您裁定；T4不阻塞独立T6。

## 三文件身份

```text
archive bytes=146872
archive SHA256=14c6b3ab04b7306eed2c52ece849039a37dfab8245ef48a5335df3faa32a494b
identity SHA256=711556300de4d6dea03107f9bc875cca1dcd4deed3c62d9cc6085cff3cbee504
validation SHA256=c60813bf4870751771e377ff1af513ec2d2e575cbc9e234346ca39a1c472c921
validation=P12/12 + Q10/10 + mutation12/12 + final-readonly PASS
```

本目录不包含credential、T4 gold原件、大数据库或模型权重。
