# 当前老师审阅入口（EnzymeCAGE 侧）

更新时间：2026-09-08
用途：给黄老师打开 GitHub 后的第一入口，避免从根目录历史散文件中自行判断最新状态。

## 1. 老师优先看哪些文件

| 优先级 | 内容 | 路径 |
|---|---|---|
| 1 | 2026-09-08最新进度与T4身份回传总入口 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/) |
| 2 | T4正式18条parent-only清单与SHA | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/T4_FORMAL_18_PARENT_INPUT_IDENTITY_RETURN.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/T4_FORMAL_18_PARENT_INPUT_IDENTITY_RETURN.md) |
| 3 | 当前T2—T6进度及T6检查点 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/CURRENT_ENGINEERING_PROGRESS_AND_T6_CHECKPOINT.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/CURRENT_ENGINEERING_PROGRESS_AND_T6_CHECKPOINT.md) |
| 4 | 对老师编排边界裁定的确认 | [`../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/ORCHESTRATION_BOUNDARY_ACKNOWLEDGEMENT.md`](../2026-09-08_Three_Module_Latest_Progress_T4_Identity_Return/ORCHESTRATION_BOUNDARY_ACKNOWLEDGEMENT.md) |
| 5 | 2026-09-07上一版完整阶段反馈 | [`../2026-09-07_Three_Module_Staged_Integration_Progress_Review/`](../2026-09-07_Three_Module_Staged_Integration_Progress_Review/) |
| 6 | 2026-08-26 BBD full-route污染物降解路线工具评估 | [`../2026-08-26_BBD_Full_Route_Tool_Comparison/`](../2026-08-26_BBD_Full_Route_Tool_Comparison/) |
| 7 | 2026-08-19污染物TP预测路线评估历史证据 | [`../2026-08-19_Pollutant_TP_Prediction_Route_Evaluation/`](../2026-08-19_Pollutant_TP_Prediction_Route_Evaluation/) |
| 8 | 2026-08-18 P18173/P80550 accession存疑项澄清 | [`../2026-08-18_M4_E2_Accession_Ambiguity_Clarification_P18173_P80550/`](../2026-08-18_M4_E2_Accession_Ambiguity_Clarification_P18173_P80550/) |

## 1a. 2026-08-26 补充专题：BBD full-route 污染物降解路线工具评估

该专题把原 BBD83 一步产物测试扩展为 BBD-local full-route 盲测集合，
比较 BioTransformer ENVMICRO、enviPath BBD Rules、ECLIPSE PREDEC/NoEC
在一步产物、多步路线覆盖和更严格路线结构相似度上的表现。

- [`../2026-08-26_BBD_Full_Route_Tool_Comparison/`](../2026-08-26_BBD_Full_Route_Tool_Comparison/)

建议先读：

```text
README.md
SISTER_READABLE_BBD_FULL_ROUTE_MULTISTEP_PREDICTION_REPORT_2026-08-26.md
PACKAGE_COMPLETENESS_CHECK_2026-08-26.md
03_summary_tables/ONE_STEP_GENERATION1_SCORE_SUMMARY_2026-08-26.csv
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv
```

一句话结论：

```text
ECLIPSE PREDEC 覆盖/召回最强；BioTransformer 在惩罚错误分支后的路线结构相似度最高。
```

边界：当前只评估 BBD-local 已知路径和 depth≤6 的 bounded route graph，
不声明完整矿化或 CO2/H2O 终点预测。

## 1b. 2026-08-19 补充专题：污染物转化产物预测路线评估

该专题是反应/产物预测侧的探索证据包，不替代上方 M4 E2 与 accession
存疑项的当前审阅事项。

- [`../2026-08-19_Pollutant_TP_Prediction_Route_Evaluation/`](../2026-08-19_Pollutant_TP_Prediction_Route_Evaluation/)

建议先读：

```text
00_READ_FIRST/POLLUTANT_TP_PREDICTION_ROUTE_STAGE_REPORT_2026-08-19.md
00_READ_FIRST/TEST_SET_CONSTRUCTION_NOTE_2026-08-19.md
01_Key_Tables/tool_capability_comparison_2026-08-19.md
06_Detailed_Result_Tables/README_DETAILED_RESULT_TABLES_2026-08-19.md
```

一句话结论：

```text
已知 parent/pathway：优先使用 enviPath 本地快照查询；
未知 parent blind prediction：BioTransformer ENVMICRO 仍是当前主基线；
BBD-finetuned ECLIPSE PREDEC：作为补充候选生成器；
当前 enviFormer checkpoint：不作为主线。
```

边界：Soil/Sludge enviPath 100% recovery 是 known-pathway lookup，不是
blind prediction accuracy；该专题不写入 production D4/pool。

## 2. 当前状态一句话（2026-09-08）

```text
T2路线桥和T3B三条真实反应native-loader轨已形成带限制staged证据；
T5性状合同轨可用；T6正在执行但3B forward、20项测试和G7终验尚未完成；
T4已定位老师08-07接受的A7/gold 18 cases，本次parent-only身份清单等待老师回签；
11概念角色只作科学I/O解读，最终编排按老师后续节点契约执行。
```

以下2026-08-18 M4 E2内容继续保留为历史可追溯状态：

截至 2026-08-26，老师已在 08-13 指导中确认 M4 Phase 1 验收通过；
M4 E2 full 4,681 staged status table 已回包并通过本地核心审计：
1,704 staged PASS、1,324 P2Rank no-pocket、1,650 AFDB fetch-failed、3 ESM-2
3B failed。原始 658M 归档在 Chenyu，不提交到 GitHub；GitHub 包含可审阅
表格、identity、报告和本地审计。
1,650 fetch-failed accession 二次复核已作为独立表格任务完成：5 个
candidate accession 仅入表供老师审阅，1,645 个无可用 AFDB v6 candidate；
未替换 UID，未生成资产，未改 formal/production。
按 08-17 老师要求，`P18173` 与 `P80550` 两个存疑 candidate 已补充
record-only 澄清：`P18173` 的 `Q8SXV0` 来自 deterministic probe order，
不是生物偏好；`P80550` 的 38aa 已溯源到 frozen 2026-01-21 processed
snapshot。两者均保持 unresolved，不进入收口路径。
BBD83 209a4b4 审计显示
08-13 P1 re-check 已完成；status-machine 修复通过；08-14 已补交并
审计正式 transport archive / identity，但科学覆盖仍低，因此不写成
BBD83 全量科学闭环。
污染物转化产物预测路线评估已在 08-19 形成阶段性包；08-26 已进一步
扩展为 BBD full-route v0.3/v3.1 工具比较包：ECLIPSE PREDEC 覆盖/召回
最强，BioTransformer 在惩罚错误分支后的路线结构相似度最高。该结论
仍限于 BBD-local 已知路径和 depth≤6，不写成完整矿化。

## 3. 当前不能误写成完成的内容

```text
08-26 BBD full-route 工具比较只能写成阶段性路线评估，不能写成生产路线裁定；
弓师兄模型尚未按本 full-route 方法完成评分；
Paraoxon S1 Stage A 只能写成 staged D4 constructability technical PASS，不能写成模型验证；
Paraoxon S2 只能写成正式案例草案，不能写成已完成模型运行；
Paraoxon 尚不能写成已通过 EnzymeCAGE 验证的案例；
M4 4,681 UID full status table 不等于 production backfill；
full 4,681 UID production D4 merge 尚未获老师另行授权；
production D4/pool merge 尚未获老师另行授权；
M4 第二里程碑 E2 只能写成 staged status table 回包，不可写成生产资产合并；
1,650 accession 二次复核只能写成 candidate 记录入表，不能写成 UID 替换或补资产成功；
P18173/P80550 accession 澄清只能写成 record-only explanation，不能写成 candidate closure；
BBD83 209a4b4 只可写成 status-clean 通过、科学覆盖仍低；
08-26 full-route 评估不等于 BBD83 / BBD full-route final acceptance；
340 主机 GVP 历史资产尚未确认找到；
ESM-C 600M 不能写成当前 ESM-2 3B 的替代；
full-coverage D4 全量补资产/重整理尚未获老师正式裁定；
M4 是否采用更宽 Rhea/EC 酶域或全量重新训练尚未获老师正式裁定。
```

## 4. 为什么根目录仍保留历史文件

根目录中保留了若干历史提交文件，是为了不破坏已经发给老师的旧 GitHub 链接。当前审阅请优先看本文件夹和仓库顶层 README 的最新入口；历史文件仅作为可追溯证据保留。
