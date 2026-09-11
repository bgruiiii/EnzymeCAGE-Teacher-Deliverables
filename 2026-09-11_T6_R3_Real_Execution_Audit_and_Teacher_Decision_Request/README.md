# 2026-09-11 T6-R3真实执行、合同逐项审计与老师决策请求

黄老师您好，本目录是陈浩然侧对您09-09 T6-R3要求的真实执行返回与独立复核。它不是一个仅含说明文字的包：目录同时提供老师原始要求、R3-R1检查点原包、R3-R2技术完成原包、真实graph/forward/smoke/C8证据、逐项合规矩阵、完整本地审计、耗时归因和可复用运行配方。

## 建议审阅顺序

1. [`HUANG_TEACHER_T6_R3_REAL_EXECUTION_RESULTS_CONTRACT_GAPS_TIME_EXPLANATION_AND_DECISION_REQUEST_2026-09-11.md`](HUANG_TEACHER_T6_R3_REAL_EXECUTION_RESULTS_CONTRACT_GAPS_TIME_EXPLANATION_AND_DECISION_REQUEST_2026-09-11.md)
2. [`TEACHER_REQUIREMENT_COMPLIANCE_MATRIX.csv`](TEACHER_REQUIREMENT_COMPLIANCE_MATRIX.csv)
3. [`audits/ENZYMECAGE_THREE_MODULE_T6_R3_R2_RESUME_STAGE8_TEACHER_TOPOLOGY_TECHNICAL_COMPLETION_RETURN_LOCAL_AUDIT_2026-09-11.md`](audits/ENZYMECAGE_THREE_MODULE_T6_R3_R2_RESUME_STAGE8_TEACHER_TOPOLOGY_TECHNICAL_COMPLETION_RETURN_LOCAL_AUDIT_2026-09-11.md)
4. [`T6_RESULT_EVIDENCE_INDEX.csv`](T6_RESULT_EVIDENCE_INDEX.csv)
5. [`E0_E7_CHECKPOINT_EVIDENCE_INDEX.csv`](E0_E7_CHECKPOINT_EVIDENCE_INDEX.csv)
6. [`audits/T6_R3_R1_PHASE_TIMING_AND_BOTTLENECK_ATTRIBUTION_2026-09-11.csv`](audits/T6_R3_R1_PHASE_TIMING_AND_BOTTLENECK_ATTRIBUTION_2026-09-11.csv)
7. [`audits/T6_R3_R1_LLM_EXECUTOR_ERROR_ATTRIBUTION_2026-09-11.csv`](audits/T6_R3_R1_LLM_EXECUTOR_ERROR_ATTRIBUTION_2026-09-11.csv)

## 本次正式状态

```text
LOCAL_AUDIT_VERDICT=PARTIAL_PASS_REAL_TECHNICAL_EXECUTION_REJECT_T6_FINAL_AND_G7
T3B_NATIVE_LOAD=PASS_3_OF_3
T3B_BOUNDED_FORWARD=PASS_6_OF_6
REAL_LANGGRAPH_COMPILE_INVOKE_STREAM=PASS_WITH_DISCLOSED_TERMINAL_LIMITATIONS
REAL_SMOKE_RECORDS=PASS_8_OF_8_AS_MIXED_GRAPH_AND_STAGED_RECORDS
GSCHEMA=PASS_8_OF_8
C8_TRAIT_PRODUCTION_CALLABLE=PASS
T5_ROUTE_AGGREGATOR=PASS_AFTER_TYPED_REATTACH
C8_TO_T5_IN_GRAPH_CONTINUOUS=NOT_ESTABLISHED
TEST_01_TO_20=REJECT_EXECUTOR_REPORTED_19_OF_20
ENVIPATH_LOOKUP_THEN_DEPENDING=NOT_ESTABLISHED
T6_OVERALL_READY=false
G7_PASSED=false
MODEL_RERUN_REQUIRED=false
TEACHER_ADJUDICATION_REQUIRED=true
```

真实技术运行有价值，但没有满足老师全部终验强门。当前不能通过改报告把结果写成20/20或G7；也不应再次重跑未变化的模型、E0—E7或大资产。

## 与老师要求对照后的关键差异

老师09-09要求以修复后拓扑真实运行，并要求真实graph、20项、8条smoke、3/3 native load、6/6 forward、C8→T5、确定性、mutation、access、零写和三文件交付。

本次真实完成了3/3 load、6/6 forward、四个最终LangGraph子进程、8条smoke、G-SCHEMA、宿主映射与C8 trait生产函数。但是：

- graph中没有enviPath lookup-first，depending v3.2在graph内调用次数为0；
- retrieved来源字段为空，bridge存在零调用时默认标enviPath的风险；
- graph/bridge reaction task ID不能直接被T5接受；
- 无LLM凭据时graph在trait前结束，trait/T5由checkpoint图外续接；
- 包内TEST-04、TEST-11和C8→T5判定过宽；
- mutation没有覆盖老师原合同全部科学负例；
- 返回时只收到archive，执行器external identity/validation未落到本地；
- E0—E7证据不在R2中重复生成，因为换模型后的R2续跑合同明确要求按R1检查点身份继承、禁止重跑；本GitHub包已将R1关键实物展开到`evidence/e0_e7/`供直接审阅。R2仍有若干§8以后具名报告文件未独立带齐，这是最终交付完整性问题，但不是E0—E7科学证据缺失。

逐项证据位置和裁定见`TEACHER_REQUIREMENT_COMPLIANCE_MATRIX.csv`。

## 十几个小时的耗时事实

```text
R3-R1 wall=19h54m
R3-R1无命令/无文件写入证据空窗=17h20m
真实三GPU独立forward=245s

R3-R2 attempt1→attempt8≈91m23s
最终成功四个子进程≈8m50s
```

因此主要耗时不是模型本身。R3-R1主要是执行端长时间无活动；R3-R2主要是正式执行阶段现场修runner与证据工具。没有证据支持把这段延迟归因于学生操作、GPU计算或结果传输。

## 两个原始返回包

```text
returned_archives/enzymecage_three_module_t6_r3_r1_operator_checkpoint_stage8_20260911.tar.gz
SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf

returned_archives/enzymecage_three_module_t6_r3_r2_resume_stage8_teacher_topology_technical_completion_20260911.tar.gz
SHA256=6844b68ac782c51556e91d77cba7c3f5f12e4e1c679a270fbcdc97ad49c3b162
```

R1保存E0—E7、资产、native load、6/6 forward和检查点；R2保存§8真实graph与后续报告。两包由R2的`RESUMED_FROM_CHECKPOINT_SHA256=50efeafd...`连接，是同一T6-R3运行的前后两段，不是两次互相替代的科学运行。R2原始external identity/validation在本地缺失，本GitHub包不伪造它们。

## 交付边界

- 本GitHub目录及同名tar/identity/validation是“老师审阅包”的三文件交付，validation只验证本地包结构、manifest、内部原包身份和审计材料完整性。
- 它不替代缺失的R2执行器external validation，也不把本地审计写成远端执行器PASS。
- 学生未修改老师固定graph/state/schema；当前等待老师对报告中六项合同差异作出裁定。
- T4已在09-10目录完成并关闭，本目录只反馈T6，避免重复打扰老师。

## 安全说明

本目录不包含credential、token、私钥、`.env`内容、T4 gold、模型权重或大型数据库。所有返回包仅为小型证据归档。
