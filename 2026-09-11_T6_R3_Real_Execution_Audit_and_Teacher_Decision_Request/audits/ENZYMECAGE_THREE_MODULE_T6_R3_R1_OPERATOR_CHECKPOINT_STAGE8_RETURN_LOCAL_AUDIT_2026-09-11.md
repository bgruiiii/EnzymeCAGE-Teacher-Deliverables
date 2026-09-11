# T6-R3-R1操作员§8检查点返回本地审计

日期：2026-09-11

审计对象：

```text
03_HPC_Returned_Result_Summaries/
enzymecage_three_module_t6_r3_r1_operator_checkpoint_stage8_20260911.tar.gz

bytes=2553000
SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf
external identity=MISSING_LOCAL
external validation=MISSING_LOCAL
```

审计方式：本地只读安全解包、manifest重算、结构化状态/worker/时间线/源码patch/未执行脚本核验；未运行T6、模型或检查点脚本

## 1. 总裁定

```text
LOCAL_AUDIT_VERDICT=PASS_CHECKPOINT_CORE_READY_FOR_CONTROLLED_OTHER_EXECUTOR_RESUME_WITH_DELIVERY_LIMITATIONS
CHECKPOINT_ONLY=true
T6_FINAL_READY=false
G7_PASSED=false
ARCHIVE_SAFETY=PASS
SINGLE_ROOT=PASS
REGULAR_FILES=368
MANIFEST_FILES=PASS_368_OF_368
MANIFEST_SHA256=PASS_367_OF_367
EXTERNAL_THREE_FILE_DELIVERY=FAIL_IDENTITY_AND_VALIDATION_MISSING_LOCAL
E0_TO_E7_REUSE=ALLOWED_DO_NOT_RERUN
T3B_NATIVE_LOAD=PASS_3_OF_3
T3B_BOUNDED_FORWARD=PASS_6_OF_6
REAL_SMOKE_INPUTS=PASS_FROZEN_8_OF_8
FULL_CHAIN_REAL_LANGGRAPH_COMPILE_INVOKE_STREAM=NOT_RUN
TEST_01_TO_20=NOT_RUN
C8_TO_T5_REAL_CONTINUOUS_REGRESSION=NOT_RUN
GSCHEMA_DETERMINISM_MUTATION_ACCESS_NONMUTATION=NOT_RUN
ENVIPATH_LOOKUP_THEN_PREDICTION=NOT_ESTABLISHED_IN_TEACHER_FIXED_TOPOLOGY
CURRENT_EXECUTOR_CONTINUATION=NOT_RECOMMENDED
OTHER_EXECUTOR_CONTROLLED_RESUME=RECOMMENDED
```

检查点核心内容可以用于另一执行器接续，不需要重新运行环境、157项、3.94GB/大资产核验、native load或§7独立6/6 forward。检查点不是T6最终结果，不能上传老师作为T6/G7完成。

## 2. 真正做到哪里

已经真实完成：

```text
§4 E0 Python环境与入口=PASS
§4.3统一graph运行时=PASS
§5老师base/patch/固定拓扑=PASS
§6.1具名组件检查=157/157
§6.2固定资产身份=PASS
§6.3 native load=3/3
§6.3逐UID sequence/GVP/pocket/ESM=PASS
§7三GPU真实forward=6/6
§8附加enviPath只读观察=完成，结果NOT_ESTABLISHED
§8-A smoke输入预注册=8/8冻结
```

尚未真实执行：

```text
§8-B完整老师graph compile/invoke/stream（附加enviPath观察器曾编译并运行有限观察场景，但不能替代完整整链）
8条smoke输出
C1—C4
TEST-01—20
C8→T5真实连续链
最终G-SCHEMA
双run determinism
scientific mutations
final access audit
persistent inputs pre/post
最终T6 archive/identity/validation
```

用户叫停时没有T6任务进程或GPU compute process在运行，因此没有杀死科学进程、没有中断原子写入。

## 3. §7真实forward可复用

```text
three workers=3
physical GPU=0/1/2
distinct UUID=3/3
each worker visible CUDA devices=1
worker exits=0/0/0
runtime model objects=5 each
runtime initialized exactly once per worker
unique(reaction_task_id, UID)=6/6
base+repeat=true
repeat tolerance=1e-5
max deltas=1.21e-13 / 2.79e-09 / 4.32e-07
forward gate problems=0
wall for parallel workers=245 seconds
runtime initialization≈223 seconds each
```

固定解释器：

```text
/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python
```

固定source patch：

```text
SHA256=074f5c31d516e1f699648008ed86767244e25fb128905e119366ad346f8f027a
changed files=36（13 scientific source + 23 tests）
teacher fixed topology files modified=0
```

检查点的`RESUME_READINESS.json`将`python_absolute_path`写成`?`、`python_overlay_order`写成`?`，并把`pool_uid_map_present`写false；这些摘要字段不应覆盖worker、环境和原始返回目录中的实物证据。下一执行器须从冻结环境文件读取，而不是使用问号字段。

## 4. enviPath发现

只读观察确认老师固定图：

```text
real StateGraph=true
nodes=12
enviPath lookup node=absent
lookup calls=0
Route C 4051 similarity retrieval calls=3
depending v3.2 graph calls=0
reaction_prediction edge=present
reaction_prediction实际fallback=BioTransformer ENVMICRO
```

因此当前图没有实现“enviPath known-route HIT → 直接使用；MISS → depending v3.2预测”。它不能由学生或下一执行器自行修改，因为graph/state/router/edge归黄老师。

该问题不应阻止继续执行老师现有固定图的其余测试；但最终不能宣称这条lookup-first合同已通过。应完成其余技术证据后向黄老师提供：现状、真实trace和是否补enviPath节点/修改fallback的裁定选项。

## 5. 为什么原任务极慢

检查点时间账本：

```text
原任务wall window=71682秒=19小时54分
有可测时长的105个事件合并busy=229秒
各事件时长相加（含3个并行worker）=746.6秒
没有命令记录、没有文件写入证据的>10分钟空窗=14段
这些完全无证据空窗总计=62441秒=17小时20分
```

最大两段空窗：

```text
6小时48分51秒
6小时00分46秒
```

真正三GPU forward只用了约4分05秒。大量时间没有科学命令、GPU进程或文件写入证据，说明慢不来自EnzymeCAGE forward。

现有日志无法把17小时20分严格区分为Qoder平台挂起、LLM内部深度思考、等待输入或未记录活动；因此不能声称已证明“Qoder平台bug”。但从工程结果看，当前协调执行器不适合继续该任务：它没有把已通过的科学门快速转换成§8实际命令。

## 6. 为什么检查点打包也慢

最终archive仅：

```text
compressed=2.55MB
uncompressed≈29.6MB
regular files=368
```

压缩本身不应耗时一小时。包内记录显示执行器为检查点写了：

```text
c1_collect.py=62337 bytes
c2_closure.py=22318 bytes
c1收集至少5次
c2 closure至少3次
总计7个收集/封口阶段记录
```

其中：

- 第一次收集凭记忆用了上一轮文件名；
- 第一次closure在最后打印不存在的`recheck["all_pass"]`而KeyError；
- 第二次closure将366个快照文件写进identity，但archive实际368个，且manifest漏自身；
- 第三次才修正。

从首次收集05:47 UTC到最后成功封口约25分钟，之前/期间另有约40分钟无证据空窗。耗时主因是LLM现场开发和修复打包工具，不是tar压缩或大文件复制。

本地仍未收到外置identity/validation，尽管内部文档称远端已创建。这是检查点交付P1。当前不要求原执行器再花时间补取；本地可用archive+完整内部manifest完成接续审计。最终T6必须重新满足三文件。

## 7. 80个变更文件是什么

不是80个科学源码变更：

```text
staged repository changes=36
  scientific source=13
  tests=23
teacher topology changes=0

original return directory files=80
  report/evidence=59
  GPU worker evidence=21

task-local deployed scripts=25
development staging scripts=30
```

所以UI的80主要是证据交付文件数。真正需下一执行器继承的科学source仍是固定36文件patch。

## 8. §8候选脚本边界

检查点保留三个从未执行的候选脚本：

```text
p15_shared.py
  bytes=19953
  SHA256=36e37e5b4fe127d88c94fd0da3a61e70e40161db04c1055709138e29d4711bd3

p15b_chain_base.py
  bytes=45649
  SHA256=73c16c33159dc61d2c4f1966caabbd0c0f0c90e64531abd9640724317256f0b0

p15c_chain_staged.py
  bytes=22330
  SHA256=5d2ea97abc238342c2f54c867b8a7b96415582077278588b32e441f0fad7098a
```

本地AST语法检查通过。但它们没有真实import冒烟、没有执行；总驱动`p15_real_langgraph_chain.py`也未写。因此不能把它们当已验证工具。下一执行器应做一次2分钟内的语法/导入/配置键预检，然后运行；不得花小时重写，真实失败才做最小task-local修复。

## 9. 下一步

停止使用当前Qoder会话继续开发。改由另一执行器，严格执行：

```text
不重跑E0—E7；
不重新哈希大资产；
不重跑独立§7 6/6 forward；
不再研究enviPath或重跑5次观察门；
不修改老师拓扑；
从§8-B开始；
先运行已有p15候选脚本；
再完成TEST-01—20、C8→T5、schema/determinism/mutation/access/pre-post；
最后一次性生成T6三文件；
环境/脚本/打包问题先快速门，禁止深度思考无命令空窗。
```

最终状态若其他技术门全部通过，应诚实写成：

```text
T6_TECHNICAL_EXECUTION_COMPLETE_WITH_TEACHER_TOPOLOGY_LOOKUP_GAP
T6_OVERALL_READY_FOR_LOCAL_AUDIT=false
G7_PASSED=false
ENVIPATH_LOOKUP_THEN_DEPENDING=NOT_ESTABLISHED_AWAITING_HUANG_TEACHER
```

待黄老师裁定是否补enviPath节点/修改prediction fallback，学生不自行决定。

## 10. P0/P1/P2

```text
P0/authority：老师固定图缺少enviPath lookup-first且fallback并非depending；需老师裁定，不能由学生修图。
P1：检查点外置identity/validation未本地收件；resume摘要三个字段不完整；§8脚本未执行。
P2：检查点自身多轮封口历史、部分报告格式；不应再让旧执行器返工。
```

当前最佳动作不是补检查点sidecar，也不是重跑前七阶段，而是用另一执行器从§8-B受控接续。
