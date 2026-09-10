# EnzymeCAGE 当前状态索引

日期：2026-09-10

## 2026-09-10最新增量反馈

| 项 | 状态 | 老师查看路径 |
|---|---|---|
| T4正式18条 | depending v3.2和ECLIPSE评测内容及R4 external closure均已完成并通过本地审计；无需T4-R5；模型角色/是否追加OOF仍请老师裁定 | [`../2026-09-10_T4_Final_Stage_and_T6_PreR3_Selfcheck/`](../2026-09-10_T4_Final_Stage_and_T6_PreR3_Selfcheck/) |
| T6进入R3前自查 | 8001移除、4 UID/8 records reviewed、direct REST、冻结UID-map fallback、TaxID聚合、G-SCHEMA和三文件均本地审计通过；真实T6-R3/G7尚未运行 | [`../2026-09-10_T4_Final_Stage_and_T6_PreR3_Selfcheck/`](../2026-09-10_T4_Final_Stage_and_T6_PreR3_Selfcheck/) |
| 返工和耗时 | 慢主要来自我们侧提示词任务设计、报告生成器和validator反复纠正，不归因于学生操作，也不是后半段模型计算 | [`../2026-09-10_T4_Final_Stage_and_T6_PreR3_Selfcheck/T6_ITERATION_REASON_TIME_AND_OUTCOME.csv`](../2026-09-10_T4_Final_Stage_and_T6_PreR3_Selfcheck/T6_ITERATION_REASON_TIME_AND_OUTCOME.csv) |

## 2026-09-08最新增量反馈

| 项 | 状态 | 老师查看路径 |
|---|---|---|
| 三模块staged集成总状态 | T2D/G4、T3B/G5、T5/G6已有带限制轨；T6进行中，G7未过 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/) |
| T6-R2真实接线 | R1五seedforward已过；R2真实图在route_bridge断链，20项本地纠正15 PASS/3 PARTIAL/1 FAIL/1 BLOCKED；G1—G5待老师契约裁定 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/T6_R2_CONTRACT_GAPS_DECISION_REQUEST_AND_STUDENT_CONTINUATION.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/T6_R2_CONTRACT_GAPS_DECISION_REQUEST_AND_STUDENT_CONTINUATION.md) |
| T6 G5字段恢复 | 两条canonical reaction已从冻结M3证据精确恢复，SHA 2/2一致；数据定位关闭，正式公共字段仍待老师裁定 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/T6_G5_REACTION_FIELD_RECOVERY_NOTE.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/T6_G5_REACTION_FIELD_RECOVERY_NOTE.md) |
| 数据库与模型权重上云调研 | 晨羽live路径/容量已盘点并本地纠正；当前已知下限52.650 GiB，迁移模型版本和波次待老师决定 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/DATABASE_AND_MODEL_WEIGHT_CLOUD_MIGRATION_LIVE_INVENTORY.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/DATABASE_AND_MODEL_WEIGHT_CLOUD_MIGRATION_LIVE_INVENTORY.md) |
| T4正式18条blind | 已定位A7/gold冻结包并回传parent-only清单+SHA，等待老师回签 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/T4_FORMAL_18_PARENT_INPUT_IDENTITY_RETURN.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/T4_FORMAL_18_PARENT_INPUT_IDENTITY_RETURN.md) |
| T6 | 执行中间快照尚未本地审计；3B forward/20项测试/终验未完成 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/CURRENT_ENGINEERING_PROGRESS_AND_T6_CHECKPOINT.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/CURRENT_ENGINEERING_PROGRESS_AND_T6_CHECKPOINT.md) |
| 智能体编排 | 已确认11概念角色只作科学I/O；最终拓扑、拆并和编排由老师裁定 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/ORCHESTRATION_BOUNDARY_ACKNOWLEDGEMENT.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/ORCHESTRATION_BOUNDARY_ACKNOWLEDGEMENT.md) |

## 当前优先审阅

| 项 | 状态 | 老师查看路径 |
|---|---|---|
| P18173/P80550 accession 存疑项澄清 | 已按 08-17 老师要求补充：P18173 的 Q8SXV0 为 deterministic probe order 首个 AFDB v6 200，不是生物偏好；P80550 38aa 溯源到 frozen 2026-01-21 processed snapshot；两者均保持 record-only unresolved | [`../2026-08-18_M4_E2_Accession_Ambiguity_Clarification_P18173_P80550/`](../2026-08-18_M4_E2_Accession_Ambiguity_Clarification_P18173_P80550/) |
| M4 Phase 1 | 老师 2026-08-13 指导中确认验收通过；原 100 UID 证据包保留 | [`../2026-08-11_M4_Phase1_Acceptance_Candidate/`](../2026-08-11_M4_Phase1_Acceptance_Candidate/) |
| M4 第二里程碑 E2 | 08-14 full 4,681 staged status table 已回包并通过本地核心审计；1,704 staged PASS、1,324 P2Rank no-pocket、1,650 AFDB fetch-failed、3 ESM-2 3B failed；不是 production merge | [`../2026-08-14_M4_E2_Full_4681_Staged_Status_Table/`](../2026-08-14_M4_E2_Full_4681_Staged_Status_Table/) |
| 1,650 accession 二次复核 | 08-16 table-only 结案；5 candidate 仅记录，1,645 no-candidate；未替换、未补资产、未改 formal/production | [`../2026-08-16_M4_E2_Fetch_Failed_1650_Accession_Secondary_Review/`](../2026-08-16_M4_E2_Fetch_Failed_1650_Accession_Secondary_Review/) |
| BBD83 209a4b4 status-clean 审计 | 08-13 P1 re-check 完成；status-machine 修复通过；runtime_failure=0；科学覆盖仍低 7/83；08-14 正式 transport archive/identity 已补交并本地审计 | [`../2026-08-13_M4_E2_Second_Milestone_and_BBD83_Status/audits/BOWEN_DEMOV2_209A4B4_BBD83_2026_08_13_P1_CLOSURE_RECHECK_LOCAL_AUDIT.md`](../2026-08-13_M4_E2_Second_Milestone_and_BBD83_Status/audits/BOWEN_DEMOV2_209A4B4_BBD83_2026_08_13_P1_CLOSURE_RECHECK_LOCAL_AUDIT.md); [`../2026-08-13_M4_E2_Second_Milestone_and_BBD83_Status/audits/BOWEN_DEMOV2_209A4B4_STATUS_CLEAN_BBD83_RERUN_TRANSPORT_PACKAGE_LOCAL_AUDIT_2026-08-14.md`](../2026-08-13_M4_E2_Second_Milestone_and_BBD83_Status/audits/BOWEN_DEMOV2_209A4B4_STATUS_CLEAN_BBD83_RERUN_TRANSPORT_PACKAGE_LOCAL_AUDIT_2026-08-14.md) |

## 历史已完成并已 push

| 项 | 状态 | 老师查看路径 |
|---|---|---|
| F1 P2Rank 表述修复 + `mix-af-p2rank` 出处 | 完成 | [`../2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/`](../2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/) |
| F2 Q1/Q2/Q3 证据同步 + 07-22 原件 | 完成 | [`../M3_THREE_TECHNICAL_QUESTIONS_CORRECTION_AND_EVIDENCE_INDEX_2026-08-04.md`](../M3_THREE_TECHNICAL_QUESTIONS_CORRECTION_AND_EVIDENCE_INDEX_2026-08-04.md) |
| F3 missing-pocket / missing-D4 缺口估算 | 完成本地 Rhea 基线估算 | [`../2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/M3_F3_LOCAL_ENZYME_ASSET_POOL_AND_EC_EXPANSION_GAP_AUDIT_2026-08-04.md`](../2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/M3_F3_LOCAL_ENZYME_ASSET_POOL_AND_EC_EXPANSION_GAP_AUDIT_2026-08-04.md) |
| F4 Q2 行号 + ESM-2 3B 配置来源修复 | 完成 | [`../2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/M3_TEACHER_TECHNICAL_QUESTIONS_Q1_Q2_CORRECTED_DRAFT_2026-08-04.md`](../2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/M3_TEACHER_TECHNICAL_QUESTIONS_Q1_Q2_CORRECTED_DRAFT_2026-08-04.md) |
| F5 BioTransformer ENVMICRO 源码与 jar 身份证据 | 完成 | [`../2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/M3_Q3_BIOTRANSFORMER_ENVMICRO_SOURCE_AND_JAR_IDENTITY_EVIDENCE_2026-08-04.md`](../2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/M3_Q3_BIOTRANSFORMER_ENVMICRO_SOURCE_AND_JAR_IDENTITY_EVIDENCE_2026-08-04.md) |
| 18 条污染物 gold/schema/scorer 固化 | 完成 | [`../2026-08-04_M3_P1_2_1_Small_Pollutant_Gold_Standard_Schema_Scoring_Freeze/`](../2026-08-04_M3_P1_2_1_Small_Pollutant_Gold_Standard_Schema_Scoring_Freeze/) |
| M3-EXT Paraoxon S1 Stage A | 完成；technical PASS，未跑模型 | [`../2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/`](../2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/) |
| M3-EXT Paraoxon S2 正式案例文件草案 | 完成；标注 `B pool = 0` 和 `C pool / prediction fallback` 运行面 | [`../2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/M3_EXT_PARAOXON_FORMAL_CASE_DRAFT_AFTER_S1_STAGE_A_PASS_2026-08-06.md`](../2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/M3_EXT_PARAOXON_FORMAL_CASE_DRAFT_AFTER_S1_STAGE_A_PASS_2026-08-06.md) |

## 正在推进但尚未完成

| 项 | 当前状态 | 下一步 |
|---|---|---|
| F6 三工具横向评分 | 等待弓师兄模型输出 | 收到后用已冻结 18 条 schema/scorer 打分 |
| M3-EXT Paraoxon 后续模型运行 | 尚未授权执行；S2 只建议另写 execution contract | 等老师接受 S2 后，再单独冻结 C pool / prediction fallback 执行合同 |

## 仍需老师后续裁定

见 [`PENDING_TEACHER_DECISIONS.md`](PENDING_TEACHER_DECISIONS.md)。
