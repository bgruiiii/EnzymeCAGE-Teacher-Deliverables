# HPC executor-only prompt：T6-R3-R2从已审计检查点接续§8-B，不重做E0—E7

日期：2026-09-11

执行者：新的远端执行器；不要使用已停止的原Qoder会话继续

任务类型：受控续跑；复用同一T6-R3-R1科学工作区和冻结证据，只完成未运行阶段

## 0. 唯一目标

从已审计的T6-R3-R1检查点继续：

```text
§8-B真实老师LangGraph compile/invoke/stream
→ 8条冻结smoke输出和C1—C4
→ TEST-01—20
→ C8→T5真实连续链
→ G-SCHEMA / determinism / mutation / access / persistent pre-post
→ archive / identity / validation最终交付。
```

已经通过的E0—E7绝对禁止重做。不得重新探索环境、重新整合source、重新哈希大资产、重新native load或重新运行独立6/6 forward。

## 1. 固定检查点与本地审计

```text
AUTHORITY_PAYLOAD=/root/projects/EnzymeCAGE-master/HPC_Inputs/t6_r3_r2_checkpoint_authority_and_local_audit_payload_20260911.tar.gz
AUTHORITY_PAYLOAD_BYTES=23927
AUTHORITY_PAYLOAD_SHA256=1ec7096aef76ebb9d777c9af252068406f043714ed50a3fba2152b07bbcde218
AUTHORITY_PAYLOAD_ROOT=t6_r3_r2_checkpoint_authority_and_local_audit_payload_20260911
AUTHORITY_PAYLOAD_REGULAR_FILES=4

CHECKPOINT=/usrdata/EnzymeCAGE_data/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_three_module_t6_r3_r1_operator_checkpoint_stage8_20260911.tar.gz
CHECKPOINT_BYTES=2553000
CHECKPOINT_SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf

LOCAL_AUDIT_FILE=ENZYMECAGE_THREE_MODULE_T6_R3_R1_OPERATOR_CHECKPOINT_STAGE8_RETURN_LOCAL_AUDIT_2026-09-11.md
LOCAL_AUDIT_BYTES=8897
LOCAL_AUDIT_SHA256=23c471c06fd8b0b400a55456331c2e83fbac0a102d9bb6c3a55223113b71a499
```

先核authority payload安全、单根和四成员SHA；payload中的黄老师原件和本地审计优先于旧执行器报告。不得从payload之外猜老师裁定。

安全列出并解包检查点到新的task-local input目录。检查：单根、安全成员、`MANIFEST.files=368/368`、`MANIFEST.sha256=367/367`。检查点外置sidecar缺失已在本地审计披露，不因此重做检查点或拒绝接续。

## 2. 继续使用原科学工作区

```text
ORIGINAL_TASK_ID=enzymecage_three_module_t6_r3_r1_pinned_python_forward_real_langgraph_20_test_final_20260910
WORK_ROOT=/usrdata/EnzymeCAGE_data/workspaces/${ORIGINAL_TASK_ID}
STAGED_REPO=${WORK_ROOT}/depending_teacher_fixed_r1
RETURN_ROOT=/usrdata/EnzymeCAGE_data/EnzymeCAGE-master/HPC_Returned_Result_Summaries
RETURN_DIR=${RETURN_ROOT}/${ORIGINAL_TASK_ID}
```

这是用户明确授权的同一run续接，不是fresh科学重跑。续接前只做5分钟以内轻量身份门：

```text
WORK_ROOT/STAGED_REPO/RETURN_DIR存在；
BASE_COMMIT=2d4cc766322a6a01b8a88491aed07536b3b0a320；
BASE_TREE=c0acb9bd30b985ad43bf969946842da97a68a400；
source patch SHA256=074f5c31d516e1f699648008ed86767244e25fb128905e119366ad346f8f027a；
老师graph/state/multi_step_bridge/bridge schema四文件SHA仍与检查点一致；
关键E0—E7 gate文件存在且命中检查点manifest SHA；
worker 3/3 exit=0、unique pairs=6/6、forward gate problems=0；
当前无旧T6进程和GPU compute process。
```

只核小型gate文件、路径、bytes和已冻结SHA；不得重新读取3.94GB/55GB资产或checkpoint计算SHA。

## 3. E0—E7冻结事实

直接继承，不重新运行：

```text
PYTHON=/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python
PYTHON_PREFLIGHT=PASS
UNIFIED_GRAPH_RUNTIME=PASS
TEACHER_FIXED_TOPOLOGY=PASS_UNCHANGED
COMPONENT_TESTS=PASS_157
FIXED_ASSET_IDENTITY=PASS
T3B_NATIVE_LOAD=PASS_3_OF_3
UID_SEQUENCE_GVP_POCKET_ESM=PASS
T3B_BOUNDED_FORWARD=PASS_6_OF_6
REAL_SMOKE_INPUTS=FROZEN_8_OF_8
```

关键小文件身份：

```text
PYTHON_RUNTIME_PREFLIGHT.json SHA256=4b70c9ed441b90dfa6e8f0fc3c71683c842ed190157542e1cb04bba866aaa7a1
UNIFIED_GRAPH_RUNTIME_GATE.json SHA256=7cb3aece572fd3e688b96cc280f12192fe55e6854ac334b3ffe24a617d75ce48
COMPONENT_TESTS_GATE.json SHA256=447de88b7a7d53878ef7585678d2b74f5ee2b508fcc38e009d432bcaa8f6da49
FIXED_ASSET_IDENTITY_GATE.json SHA256=bc58a271218999c6cc2a282a443271ed2ed6fc4a971e29a5b74cc1b3ced86a97
UID_SEQUENCE_GVP_POCKET_ESM_PREFORWARD_GATE.json SHA256=cbf4176994717e3135a8746bd1ec8b5f072f9d5369a1272b1fa1748e48e2fcb8
T3B_BOUNDED_FORWARD_GATE.json SHA256=b153e4cd09fc513dd5f01cbd16366ba21a278027ca17a3c1243cb2905e8d720f
REAL_SMOKE_INPUTS.csv SHA256=97e5d6d6701ac23890ae8ee4c71c9039280c4f447fe63510bb7fec76b13f8595
```

不得把历史6/6复制成§8的graph-internal forward；§8真实图仍需按冻结场景执行。禁止的是重复独立§7基准，而不是阻止真实graph调用模型。

## 4. enviPath/depending边界已经查清，不再勘察

固定事实：

```text
ENVIPATH_LOOKUP_THEN_PREDICTION=NOT_ESTABLISHED
teacher fixed graph enviPath node=absent
enviPath lookup calls=0
Route C 4051 similarity retrieval exists but不是enviPath known-route lookup
reaction_prediction fallback actual tool=BioTransformer ENVMICRO
depending v3.2 graph calls=0
```

证据：

```text
ENVIPATH_LOOKUP_THEN_PREDICTION_TRACE.json
SHA256=bd8673dc0489e8d6a97aeb2f40eccf76a5075f8a0190e2876843b49927fdfd84
```

不要第6次运行enviPath观察器，不写新分析脚本，不修改graph/state/router/edge。继续测试老师现有固定图；最终把该项列为`AWAITING_HUANG_TEACHER_TOPOLOGY_ADJUDICATION`，不自行修复，也不把Route C/depend­ing内部retrieval冒充enviPath。

## 5. §8候选脚本：先快速审查，随后执行

检查点包含：

```text
p15_shared.py bytes=19953 SHA256=36e37e5b4fe127d88c94fd0da3a61e70e40161db04c1055709138e29d4711bd3
p15b_chain_base.py bytes=45649 SHA256=73c16c33159dc61d2c4f1966caabbd0c0f0c90e64531abd9640724317256f0b0
p15c_chain_staged.py bytes=22330 SHA256=5d2ea97abc238342c2f54c867b8a7b96415582077278588b32e441f0fad7098a
```

它们AST语法本地通过，但从未执行。最多用2分钟完成：

```text
compile(source, filename, 'exec')语法检查；
静态配置键与import列表核对；
使用固定Python做不加载模型的模块import入口检查；
确认没有自建StateGraph、monkeypatch或老师source写入。
```

然后将原字节复制到`WORK_ROOT/scripts/`并执行。不得因风格、标题或可选优化重写。如果真实import/运行失败，只允许最小task-local修复，并保存原件、新件、diff、traceback；不得改36文件source patch或老师拓扑。

## 6. 最小driver，不做框架开发

缺失的`p15_real_langgraph_chain.py`只做以下协调：

```text
1. 从已验证v1 archive物化task-local base package：5个config原字节 + 5 checkpoint硬链；
2. 核base config与overlay config只在rxn_fp/mol_conformation/reaction_center三字段不同；
3. 生成base/staged run1/run2四份JSON配置；
4. 用固定Python分别启动：
   base run1 -> p15b_chain_base.py
   base run2 -> p15b_chain_base.py
   staged run1 -> p15c_chain_staged.py
   staged run2 -> p15c_chain_staged.py
5. 每个子进程记录argv/start/end/elapsed/exit/stdout/stderr；
6. 不修改子脚本科学逻辑，不自己手填最终state；
7. 任一真实P0失败立即停止后续科学场景并保留证据。
```

禁止创建新的抽象框架、通用runner或超过该七项职责的driver。连续10分钟没有真实命令、进程或文件活动时，立即停止并返回精确阻塞，不进入深度思考循环。

## 7. 完成剩余验收

§8-B通过后，直接使用冻结输出完成：

```text
REAL_LANGGRAPH_INVOKE_TRACE.jsonl
REAL_LANGGRAPH_STREAM_TRACE.jsonl
NODE_STATE_TRANSITIONS.jsonl
REAL_SMOKE_OUTPUTS.jsonl（与冻结8输入逐条对应）
C1—C4
C8_TO_T5_REAL_CONTINUOUS_REGRESSION.json
TEST_CASE_MATRIX.csv（TEST-01—20恰20项，组件PASS不能替代）
SCHEMA_VALIDATION_REPORT.json
DETERMINISTIC_ORDER_CHECK.json
MUTATION_CHECK.json
ACCESS_AUDIT.jsonl
PERSISTENT_SOURCE_NONMUTATION.json
```

双run只使用base/staged run1/run2现有四个进程结果，不额外再跑图。mutation使用小型隔离证据副本，不重新加载五checkpoint。外置validator不得再运行GPU或真实graph，只核不可变raw evidence。

## 8. 最终状态与老师裁定

如果除enviPath合同外所有技术门通过：

```text
T6_R3_TECHNICAL_EXECUTION_COMPLETE_WITH_TEACHER_TOPOLOGY_LOOKUP_GAP
TEACHER_FIXED_TOPOLOGY_EXECUTED=true
REAL_LANGGRAPH_COMPILE_INVOKE_STREAM=PASS
REAL_SMOKE_RECORDS=PASS_8_OF_8
TEST_01_TO_20=<逐项真实结果；只有20/20才写PASS_20_OF_20>
C8_TO_T5_REAL_CONTINUOUS_REGRESSION=PASS
ENVIPATH_LOOKUP_THEN_DEPENDING=NOT_ESTABLISHED_AWAITING_HUANG_TEACHER
T6_OVERALL_READY_FOR_LOCAL_AUDIT=false
G7_PASSED=false
```

不能为了拿G7修改老师图，也不能由执行器裁定envipath是否应加入。若其他P0门失败，写首个真实`BLOCKED_AT_*`。

## 9. 三文件一次封口

最终包必须独立新basename，不能覆盖检查点或首轮失败包：

```text
TASK_ID=enzymecage_three_module_t6_r3_r2_resume_stage8_teacher_topology_technical_completion_20260911
RETURN_ROOT=/usrdata/EnzymeCAGE_data/EnzymeCAGE-master/HPC_Returned_Result_Summaries
ARCHIVE=${RETURN_ROOT}/${TASK_ID}.tar.gz
IDENTITY=${ARCHIVE}.identity.txt
VALIDATION=${ARCHIVE}.validation.txt
```

使用已经通过审计的clean closure顺序。不要开发新的closure：

```text
package content final
→ manifest N/N和N-1/N-1
→ archive
→ fresh U1
→ identity
→ validation写前不存在
→ pre-write
→ exclusive first write
→ fresh U2 post-write
→ final-readonly
```

READY或BLOCKED都必须返回同basename三文件。失败检查点已出现过缺sidecar，本次不能重复。

## 10. 时间纪律

```text
resume身份门≤5分钟；
p15静态/import检查≤2分钟；
driver编写/配置≤10分钟；
四个真实子进程按各自运行时计时，不在中间重构；
剩余CPU测试/证据派生≤30分钟；
closure≤10分钟；
任何无命令/进程/文件活动空窗不得超过10分钟。
```

如受真实I/O或模型进程限制，记录PID/argv/进度文件并继续等待；“LLM仍在思考”不是延长时间预算的理由。

## 11. 最终只打印

```text
ARCHIVE=<path> bytes=<n> SHA256=<sha>
IDENTITY=<path> bytes=<n> SHA256=<sha>
VALIDATION=<path> bytes=<n> SHA256=<sha>
RESUMED_FROM_CHECKPOINT_SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf
E0_E7_RERUN=false
REAL_LANGGRAPH=<status>
REAL_SMOKE=<status>
TEST_01_TO_20=<status>
C8_TO_T5=<status>
ENVIPATH_LOOKUP_THEN_DEPENDING=NOT_ESTABLISHED_AWAITING_HUANG_TEACHER
FINAL_STATUS=<technical complete with teacher gap or first real blocker>
PHASE_TIMING=<resume/driver/base/staged/tests/closure seconds>
```

然后停止。不上传GitHub、不反馈老师、不运行T4/DBP/SCNET。
