# 当前工程进度与T6执行检查点

日期：2026-09-08

## 1. 当前总体判断

三模块的主要staged组件轨已经推进到T6整合验证，但完整整链尚未通过。T2路线桥、T3B真实新反应资产和T5合同轨
已有可用证据；T6仍缺真实3B forward、完整图运行、20项自动化测试和终验，因此G7保持未通过。

## 2. 当前工作项

| 工作项 | 当前状态 | 已形成的证据 | 尚未完成/限制 |
|---|---|---|---|
| T0源码/环境/安全/资产 | `PASS_WITH_LIMITATIONS` | 固定Git、环境、主要资产身份和staged零写纪律 | 历史sidecar与部署差异留账 |
| T1 M3三案例基线 | `PASS_WITH_LIMITATIONS` | B-primary、C-fallback、召回失败；full-reaction；pool≤100；CPU入口/wrapper身份 | staged累计patch，未merge production |
| G-SCHEMA | `PASS_WITH_LIMITATIONS` | route→reaction→enzyme→organism→trait证据对象、枚举、跨字段validator | 需在真实整链输出继续复验 |
| T2 | `PASS_WITH_LIMITATIONS_STAGED` | owner bundle 30/30；单SMILES；predicted→candidate；真实LangGraph桥；多步edge任务、唯一ID和typed回挂 | 多来源重复edge、完整整图及部分sidecar留T6/总审计 |
| G4 | `PASS_WITH_LIMITATIONS` | T2A—T2D staged审计闭合 | depending仍为evaluation candidate |
| T3A proxy | `PARTIAL_PASS_SELECTION_BLOCKED_RANKING` | 3/3按full-reaction radius8找到相似度≥0.70 proxy并标FROZEN_PROXY | 0/3完成真实proxy EnzymeCAGE排名；不得冒充真实资产 |
| T3B真实资产 | `PASS_WITH_LIMITATIONS_NATIVE_LOADER_3_OF_3` | 三条DRFP/AAM/center/SDF冻结；原生loader、dataset length=3、`ds[0]`均3/3 | 真实forward未完成；若干报告/sidecar限制留账 |
| G5 | `PASS_WITH_LIMITATIONS_T3B` | T3B轨满足最小真实资产loader门 | 只放行T6 staged smoke，不代表新反应科学准确率 |
| T5 | `PASS_WITH_LIMITATIONS_STAGED_CONTRACT_ONLY` | UID→source→F1—F15、只读adapter/node、宿主跨步骤聚合合同、fungal fail-closed | 真实多步输入需在T6复验；部分validation receipt延期 |
| G6 | `PASS_WITH_LIMITATIONS_CONTRACT_TRACK` | T5A—T5C staged合同轨可用 | 不能外推为真实整链trait完成 |
| T6 | `IN_PROGRESS_EXECUTOR_CHECKPOINT_NOT_LOCALLY_AUDITED` | 执行端报告固定SHA、T2D/T5C三方合并、真实StateGraph compile及部分invoke失败证据已落盘 | 3B forward、完整invoke/stream、20项测试、mutation/determinism/schema/三文件未完成 |
| G7 | `NOT_PASSED` | 无 | 等T6完整返回并本地独立审计 |
| T4 | `PARENT_IDENTITY_RETURN_AWAITING_TEACHER_COUNTERSIGN` | 已定位老师08-07接受的A7/gold 18 cases；本次回传parent-only清单及SHA | 回签前不启动正式预测 |
| 自建NON-BBD外部文献集 | `PAUSED_NOT_T4` | 仅形成有限provisional文献核证 | 不替代T4，不进入本轮预测 |

## 3. T2/T3自昨日以来的新增进展

T2已经不是昨日的“T2C/T2D进行中”。目前有效累计轨已覆盖：

```text
depending v3.2 single-SMILES
→ predicted_reactions转candidate_reactions
→ M3真实LangGraph回归桥
→ 多步route edge拆分
→ 唯一reaction_task_id
→ typed step result按原任务回挂
```

T3B三条Benzotriazole路线反应资产由原生`load_geometric_dataset`真实加载3/3。执行中纠正了R1报告把首UID
重复三次的问题；真实UID为`A0A011QK89 / A0A017SP50 / A0A017SR40`。但原生loader通过不等于模型forward通过，
因此本次不把G5扩写成完整G7。

## 4. T6当前真实边界

以下内容来自执行端09-08中间快照，尚未取得archive做本地独立审计：

```text
10项固定输入SHA门：执行端报告匹配；
T2D累计patch：执行端报告clean apply；
T5C reference：执行端报告独立apply；
evidence.py/state.py：执行端报告完成语义三方合并且py_compile通过；
真实StateGraph：执行端报告build_graph_t6 compile成功；
invoke：先后暴露无LLM凭据、D4 wrapper环境变量缺失、无GPU加载3B过慢；
T3B native loader后台结果：尚未取回确认；
6条forward：未完成；
TEST-01—20、determinism、mutation、access audit、schema、manifest/三文件：未完成。
```

因此当前不能写`PASS_WITH_LIMITATIONS_AWAITING_LOCAL_AUDIT`，更不能写READY。主要运行卡点是执行通道连续
`40500 timeout`以及当前调用环境无GPU，加载3B ensemble超出调用窗口。这是当前执行环境/资源卡点，不是已经
证明模型科学失败，也不是已完成整链。

## 5. 编排裁定后的处理

T6中形成的13节点拓扑依据此前冻结合同开展，时间上先于/并行于老师09-08新裁定。现按新裁定处理：

```text
只保留为staged技术探索证据；
不称为老师批准的最终LangGraph拓扑；
不merge production；
不据此继续自行设计或重排节点；
后续正式接线等待老师节点契约。
```

老师同时明确T2C/T2D/T3/T6继续推进，因此我们会继续补齐可复核的技术测试与运行证据，但始终把“技术整合验证”
和“最终编排裁定”分开。

## 6. 接下来

1. 取得T6完整或检查点返回包并本地独立审计，不能只信执行端状态文字；
2. 在合适GPU执行环境补真实forward，完成20项测试和整链终验；
3. 按老师节点契约收敛最终工程拓扑，不自行提案；
4. 等老师回签本次T4 parent身份后，启动depending v3.2与ECLIPSE同口径盲测。
