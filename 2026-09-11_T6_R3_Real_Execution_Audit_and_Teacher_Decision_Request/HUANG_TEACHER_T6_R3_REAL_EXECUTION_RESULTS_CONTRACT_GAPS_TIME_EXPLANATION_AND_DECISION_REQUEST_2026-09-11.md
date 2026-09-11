# T6-R3 真实执行结果、长耗时说明、固定拓扑缺口与老师裁定请求

日期：2026-09-11

## 一、先说结论

本次 T6-R3 **不是没有运行，也不是模型计算失败**。三 GPU 的 6/6 forward、老师 `StateGraph` 的真实 compile/invoke/stream、EnzymeCAGE 排序、UID 到微生物映射以及 C8 性状生产函数均产生了可核验的真实结果。这些结果有工程和科学诊断价值，应保留，不需要因为当前总门未过而重新计算。

但本次仍**不能报告 T6/G7 通过**。真实运行暴露出老师固定拓扑及公共数据合同中的关键断点：

1. 当前图没有“先查 enviPath，MISS 后再预测”的 lookup-first 节点和 HIT/MISS 路由；
2. 当前图中的预测后备实际是 BioTransformer，不是 depending v3.2，且本轮真实路径没有到达 prediction；
3. 反应来源字段在检索链中丢失，bridge 又可能在没有调用 enviPath 时默认标成 enviPath；
4. graph-native/bridge 产生的 reaction task ID 与 T5 只接受 `RT-*` 的合同不兼容；
5. 无 LLM 凭据时 `organism_selection` fail-closed，图在 trait 之前结束；
6. canonical lowercase aromatic SMILES 会被当前入口误判并进入不可用的 LLM fallback。

这些问题涉及老师固定的 graph/state/schema、正式工具角色和跨模块 ID 合同。学生没有修改上述老师代码，也不应自行决定后宣布通过，现请求老师一次性裁定。

本次本地审计状态为：

```text
PARTIAL_PASS_REAL_TECHNICAL_EXECUTION_REJECT_T6_FINAL_AND_G7
MODEL_RERUN_REQUIRED=false
GRAPH_RERUN_REQUIRED_NOW=false
ZERO_MODEL_EVIDENCE_CORRECTION_REQUIRED=true
TEACHER_ADJUDICATION_REQUIRED=true
T6_OVERALL_READY=false
G7_PASSED=false
```

## 二、本次到底跑出了什么，哪些结果对老师有价值

### 2.1 已真实通过且可以保留

```text
固定 Python/环境门=PASS
T3B native load=3/3
三 GPU bounded forward=6/6
老师 StateGraph real compile=PASS
老师 StateGraph real invoke=PASS
老师 StateGraph real stream=发生，最终子进程退出码均为0
最终四个 LangGraph 子进程=4/4 exit 0
smoke records=S1—S8 共8条
evidence documents=8条
G-SCHEMA=8/8
5个 enzyme UID 均完成宿主映射
得到4个 organism candidates
C8 trait records=75，其中 OBSERVED=42、MISSING=33
最终 attempt 在 PYTHONHASHSEED=0 下重复结果一致
老师 topology 四文件未修改
```

四个最终真实子进程耗时：

```text
base_run1=153.360s
base_run2=156.262s
staged_run1=111.071s
staged_run2=109.613s
合计约530.3s，即8分50秒
```

这批结果证明：

- 固定模型、输入资产和三 GPU forward 可以工作；
- 当前老师图可以真实 compile/invoke/stream，不是 mock 或报告拼接；
- reaction 候选进入 EnzymeCAGE 后，酶排序、宿主映射和 C8 trait 生产函数本身可运行；
- 当前失败集中在图路由、来源语义和跨模块公共 ID，而非“所有模型都不能运行”。

### 2.2 结果应如何准确表述

可以表述：

```text
REAL_TECHNICAL_EXECUTION=PARTIAL_PASS
ENZYMECAGE_HOST_C8_COMPONENTS=REAL_EXECUTION_PROVEN
C8_TO_T5=PASS_COMPONENT_CHAIN_AFTER_TYPED_REATTACH
```

不能表述：

```text
T6_OVERALL_READY=true
G7_PASSED=true
TEST_01_TO_20=19/20 PASS
C8_TO_T5_IN_GRAPH_CONTINUOUS=PASS
ENVIPATH_LOOKUP_THEN_DEPENDING=PASS
```

原因是 C8 与 T5 虽然分别真实调用成功，但 trait 是从 checkpoint state 在图外续接，T5 又是在把 reaction 重新挂到冻结 `RT-*` ID 后才成功；这不是 graph-native 连续闭环。

## 三、十几个小时为什么一直慢

### 3.1 R3-R1：约19小时54分

可核计时证据：

```text
总 wall time=19h54m
无命令、无文件写入证据的空窗=17h20m
真实三 GPU forward=245s
```

因此，R3-R1 的主要耗时不能归因于模型计算。证据只能证明执行端长时间没有产生命令或文件活动；无法从现有包证明该时间具体花在何种“思考”上，所以这里不把原因虚构成集群、GPU 或数据传输问题。工程上应归类为：执行模型长时间规划/停滞、没有调用已经冻结的入口。

### 3.2 R3-R2：约91分23秒后才完成一次成功技术运行

R3-R2 从 attempt1 到 attempt8：

| attempt | 到达位置 | 结果 | 暴露的问题 |
|---|---|---|---|
| 1 | base_run1 | FAIL | Pydantic 对象被当作 dict 下标读取；输入入口问题 |
| 2 | base_run1 | FAIL | runner 实现缺陷 |
| 3 | staged_run1 | FAIL | logger handler 实际为 pair；计数逻辑错误 |
| 4 | staged_run1 | FAIL | staged overlay 校验逻辑错误 |
| 5 | staged_run1 | FAIL | overlay 路径被错误限制在 v1 root 内 |
| 6 | 四次运行完成 | FAIL determinism | `PYTHONHASHSEED` 未在子进程启动前固定 |
| 7 | 四次运行完成 | FAIL base determinism | set/order 与 live API 字段规范化仍漂移 |
| 8 | 四次运行完成 | PASS | 最终技术运行成功，约8分50秒 |

前7轮大部分是在**现场开发和修测试 runner/证据工具**，不是在重复做有意义的科学计算。最终成功运行只占约8分50秒；其余约82分主要用于修 runner、等待失败运行到触发点以及再次启动。

最终运行后又花约15分钟生成报告、validator、mutation 与 closure；本地复核发现其中仍有口径错误。这说明本轮慢的根本工程原因是“让大语言模型在正式执行阶段边运行边重写工具”，而不是 T6 本身必然要运行十几个小时。

本说明不把上述耗时归因于操作者，也不把长空窗归因于 GPU/模型；现有时间证据不支持这种说法。

## 四、本轮修复中，哪些有意义、下次可以直接复用

### 4.1 应固化，下一次不应再次探索

1. **固定解释器与环境入口**

```text
Python=/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python
Python version=3.12.3
ASE=3.29.0
LangGraph=1.2.9
PYTHONHASHSEED=0（必须在创建子进程之前放入环境）
```

LightGBM 使用已冻结 T2B venv 中 4.7.0 的只读末位 overlay；不 pip、不下载、不改变 `sys.executable`。下次直接核 module 来源与身份，不再重新讨论“是否存在”。

2. **固定资产 registry 与一次性核验结果**

```text
GVP SHA256=8e1c5138aaf6fe45af2ca14b61631925cdbed661a052deff35155b01027ff96e
ESM node SHA256=960e882fd116466785b7d648a085e78be1b5e00975cc3b8660ac566e724ea89e
ESM mean SHA256=e44f70f4e2e5f9cc1269a8271397c5f51736ec4d7c0268f3a7f1427bc0201707
staged rxn2fp bytes=6500
staged rxn2fp SHA256=7e1a3d3740a465762863e41ba0090d87851129749aa9d093d7558a1885293ea4
UID map SHA256=7b92e8e625cb73f070c8e902687ea5bbdbf749f04a19828e550e3fe205684fe6
C8 lookup SHA256=d51a540db2f9798d65e25b46f22960ba29ae2d4b288be218c83c299f24f5d5af
```

同一版本日常复现只做快速身份门；同一轮每个大资产最多完整哈希一次并共享结果。只有老师要求最终验收或文件元信息发生变化时才重算全量 SHA。

3. **固定成功运行顺序与进程隔离**

```text
生成 base/staged 配置
→ base_run1
→ base_run2
→ staged_run1
→ staged_run2
→ 分别比较规范化后的重复结果
```

base 和 staged package root 必须分进程运行，避免 wrapper singleton 污染；live UniProt/KEGG 原始响应与确定性比较视图分开保留。

4. **冻结已成功的 runner 候选**

| runner | SHA256 | 用途与限制 |
|---|---|---|
| `as_executed_p15_real_langgraph_chain.py` | `3857a355fa23ed9c11fb34b83a95f7fb45ccdcb43f594acd708aade73a1e6846` | driver 候选 |
| `as_executed_p15_shared.py` | `36e37e5b4fe127d88c94fd0da3a61e70e40161db04c1055709138e29d4711bd3` | 观察/规范化候选 |
| `as_executed_p15b_chain_base.py` | `3e4983a10bb726a613d55eb96e9ce3b84fe7d689a3ae4b0b5e5f26eb4cb51708` | base runner；含输入与 task-ID 临时绕行，不能冒充生产修复 |
| `as_executed_p15c_chain_staged.py` | `d89b6ff2b8d24371967894898797e656be84754b303612cf30c10aa789a14146` | staged runner 候选 |
| `as_executed_r1_common.py` | `424e4de70eae15e8e7fdc83756511987e7d9f688bdc28d1b512f7b5d6c84cd07` | 公共路径/身份工具候选 |

这些修复有意义：只要文件身份、环境与老师 base 不变，下次不应再次让执行模型从头定位 Python、资产、LightGBM、worker 或确定性设置。

### 4.2 只可作为诊断绕行，不能固化成正式成功

1. 将 canonical lowercase aromatic SMILES 改为同分子的 Kekulé 表示，只证明测试能够绕过入口；没有修复生产入口。
2. 将 graph/bridge reaction 按 SMILES 重新挂到冻结 `RT-*` task ID，只证明 T5 production callable；没有修复公共 ID 合同。
3. 从 checkpoint 取 state 后在图外直接调用 trait/T5，只证明组件能运行；没有证明图内连续闭环。

这些绕行揭示了问题，因而有诊断价值；但老师未裁定前，下一次不能把它们写成正式图的行为。

### 4.3 不应复用的错误工具

以下工具包含已确认的判定缺陷，不能下次原样调用后宣布 PASS：

```text
p16_finalize.py
p17_validator.py
p18_mutations.py
p19_closure.py
```

主要问题包括：把 `source_tag/source_tool=null` 视为来源保留；TEST-11 混用 occurrence 和 unique task 分母；把图外 typed reattach 写成图内 C8→T5 连续通过；未正确解析已授权 UniProt/KEGG host；把正确 6500-byte `rxn2fp.pkl` 错误期望为 44 bytes 且未纳入总门；mutation 只覆盖13项而非原科学合同。

## 五、为什么最后仍失败：请老师按以下代码位置裁定

以下均为老师固定拓扑或公共合同问题。学生本轮未修改这些文件。

### 5.1 缺少 enviPath lookup-first

真实证据：

```text
teacher graph nodes=12
enviPath known-route node=absent
enviPath calls=0
Route C 4051 similarity retrieval calls>0
reaction_prediction edge=存在但本轮真实 smoke 不可达
depending v3.2 graph calls=0
```

相关代码：

| 文件 | SHA256 | 当前行为/需确认处 |
|---|---|---|
| `src/graph.py` | `736362c5cd7c4e307c453cb44dfa328d3e5a40a6f15489e6e3c04970623ba5f0` | 无 enviPath lookup node/edge；prediction 路径在真实 case 不可达 |
| `src/nodes/reaction_node.py` | `1392de0b4f69b01d3ceedc4c896e5256b1becb787349664bb6e157604a358b71` | Route C 始终返回 Top-K，相当于没有 known-route HIT/MISS 语义 |
| `src/tools/reaction_retriever.py` | `648455f1b4aec34dac1f7de9353fbcae499588d21666c3ad429ef7801bff37de` | 实现的是4051条冻结反应相似检索，不是 enviPath known-route 查询 |
| `src/nodes/reaction_prediction_node.py` | `6dc0853cf30ea40d2325c7a296200bfac65805564231a9dfef3118a622ef25ba` | 当前 prediction fallback 指向 BioTransformer |
| `src/tools/reaction_predictor.py` | `860d582ca6b9f18270748e8f35ebab00ed56446218307fac27e33193e83da308` | BioTransformer 入口 |
| `src/tools/depending_v32_adapter.py` | `fce500204b2aadd46fef0dc83a39278904c4782d79728b341de822a839c12418` | depending v3.2 adapter 存在，但当前真实 graph 未 import/调用 |

请老师裁定：

- 是否正式增加 `enviPath known-route lookup → HIT/MISS` 节点与边；
- MISS 后正式调用 depending v3.2，还是继续调用 BioTransformer；
- 或者修改 T6 合同，明确当前图只做 Route C 相似检索，不再声称 enviPath lookup-first。

### 5.2 来源字段丢失并可能错误标为 enviPath

真实 retrieved rows：

```text
source=retrieved
source_tag=null
source_tool=null
```

同时 `src/schemas/bridge.py` 默认 `source_tool="enviPath"`；本轮 enviPath 调用为0，bridge 却仍可能携带 enviPath 标签，因此存在来源误归因。

相关代码：

| 文件 | SHA256 | 需确认处 |
|---|---|---|
| `src/state.py` | `578c44f997e8e90e5e7d4bbe68afb5a11bb60bbe22a7b86b50785e448f8df775` | 公共 state 如何强制承载来源与 route/task 身份 |
| `src/schemas/bridge.py` | `a26fa402e5461940c61ca39d88db191d93f8603982fcfccf3affe6f2efa5060e` | `source_tool="enviPath"` 默认值在零调用时产生错误归因 |

请老师裁定：数据库检索、BioTransformer、ECLIPSE、depending 等来源应在哪个公共类型中强制为非空；未知来源是否应显式写 `unknown/unavailable`，而不是默认 enviPath。

### 5.3 graph/bridge task ID 与 T5 合同断裂

真实失败：

```text
graph native ID=NONE_SINGLE_STEP_M5 → T5拒绝
bridge ID=R-...:stepN.branch        → T5拒绝
T5只接受 RT-*                     → 只有手工 typed reattach 后通过
```

相关代码：

| 文件 | SHA256 | 当前行为/需确认处 |
|---|---|---|
| `src/nodes/multi_step_bridge_node.py` | `f5f97836f1e02af3a8f2155d1323eb5d7f02d86e8c628c1672ce283ceae30364` | 生成 `R-*` step ID |
| `src/utils/route_step_organism_aggregator.py` | `ac04a6e237d52f0c007726390e1cc8b9d9091923f80daa59313178f9d84083cd` | 只接受 `RT-*` task ID |
| `src/state.py` | `578c44f997e8e90e5e7d4bbe68afb5a11bb60bbe22a7b86b50785e448f8df775` | 应由公共 state/schema 统一 task ID，而不是 runner 临时重挂 |

请老师指定唯一公共 ID 合同：由上游直接生成 `RT-*`，由 bridge 持久化 crosswalk，或由 T5 正式接受两种 typed ID。学生不自行选择。

### 5.4 无 LLM 时图在 trait 之前终止

本轮真实 m5 顺序：

```text
orchestrator
→ substrate
→ reaction
→ enzyme_pool
→ enzymecage
→ reranking
→ microbe
→ organism_selection
→ END
```

`organism_selection` 因无 LLM credential fail-closed；图内没有继续到 trait/synthesis。随后执行器在图外续接 production trait/T5，虽然证明组件可调用，但不是图内闭环。

请老师裁定：

- 无 LLM credential 时是否允许确定性规则透传/ranking 后进入 trait；
- 如果必须 fail-closed，T6 是否接受“图到 organism_selection + 图外组件测试”，以及最终状态如何命名；
- 如果必须验证完整图，正式运行需要提供哪种受控 LLM 配置。

### 5.5 canonical lowercase aromatic SMILES 入口兼容

canonical lowercase aromatic SMILES 被 substrate regex 误判后进入 LLM fallback；无凭据时 fail-closed。执行器改成同分子的 Kekulé 大写表示后才绕过。

请老师裁定：生产入口应直接接受 canonical lowercase aromatic SMILES，还是上游合同要求统一提供 Kekulé 表示。建议在入口加一个不依赖 LLM 的 RDKit parse/normalize 硬门，并保留原输入与规范化输入两个字段，避免来源不可追踪。

## 六、证据报告还需一次零模型纠正，但不需要重跑模型

本地复核发现包内自报 `19/20` 过宽。至少应改为：

```text
TEST-03=NOT_ESTABLISHED_REAL_GRAPH
TEST-04=FAIL_SOURCE_PROVENANCE_NULL_AND_FALSE_ENVIPATH_DEFAULT
TEST-11=FAIL_OR_NOT_ESTABLISHED_DENOMINATOR_SEMANTICS
TEST-12/16=C8_AND_T5_PRODUCTION_CALLABLE_PASS_AFTER_REATTACH
TEST-12/16 GRAPH_CONTINUOUS=NOT_ESTABLISHED
TEST-17=PASS_REAL_GRAPH_EXECUTION_WITH_TERMINAL_FAIL_CLOSED_LIMITATION
```

TEST-11 当前把4个 branch occurrences、3个 unique upstream tasks 和2个 unmatched steps 混在同一分母中。应分别报告：

1. branch occurrence 覆盖；
2. unique upstream task 覆盖；
3. 每条 route 的 step denominator。

这些都能从现有 JSON/JSONL/CSV 重新计算，不需要重跑 GPU、模型或当前老师图。

另外，mutation、access 和 persistent validator 应在隔离副本上做一次 CPU/零模型纠正：

- 补齐原合同的科学 mutation，而不是只保留13项环境/运输门；
- access 应判“仅访问授权的 `rest.uniprot.org`、`rest.kegg.jp`，unauthorized=0”，不能写“无外部网络”；
- `rxn2fp.pkl` 正确身份是 6500 bytes 和上述 SHA，所有子门必须进入总布尔结果。

这些属于证据工具修正，不应触发科学重跑。

## 七、请求老师一次性回复的六项决定

请老师按编号回复即可：

1. 是否在固定图加入 enviPath known-route lookup 与 HIT/MISS edge？
2. lookup MISS 后正式 predictor 是 depending v3.2 还是 BioTransformer？
3. `CandidateReaction` 的 `source_tag/source_tool` 如何强制保留？`bridge.py` 的 enviPath 默认值如何处理？
4. graph-native `NONE_SINGLE_STEP_M5`、bridge `R-*` 与 T5 `RT-*` 应采用哪一种统一公共 ID 合同？
5. 无 LLM credential 时，`organism_selection` 是否允许确定性降级并继续到 trait/synthesis？
6. canonical lowercase aromatic SMILES 由 substrate parser 直接接受，还是由上游统一转 Kekulé？

收到裁定后，学生只对老师批准的最小文件和合同做新版本验证；不改写老师未授权拓扑。

## 八、后续执行建议：避免再次耗费十几个小时

1. 当前停止重跑模型和当前老师 graph，先等待上述 P0 裁定。
2. 只做一次零模型证据纠正，并冻结修正后的 finalizer/validator。
3. 老师给出新 base/patch 后，复用本轮固定 Python、LightGBM overlay、资产 registry、GPU worker 和 p15 runner。
4. 先跑不超过2分钟的 Python/import/schema/runner smoke；任何 runner 类型错误在这里暴露，不能等到真实模型后再修。
5. 只对受老师修改影响的 component tests 复验；未变化的大资产不重复全量探索和多次哈希。
6. 正式运行期间禁止大语言模型现场重写 runner；只能调用已冻结脚本。若失败，保留 checkpoint 和最小 traceback，先人工裁定是否需要改脚本。
7. 成功条件必须预先固定：真实 lookup/prediction 路由、来源、task ID、无 LLM 策略、TEST-01—20、完整 mutation、三文件 closure 均有明确机器门。

按当前实测，若老师的新拓扑变更范围有限，环境与资产不再重新探索，科学运行本身应按“分钟级到一小时内”规划，而不应再次默认十几个小时。

## 九、审计与实物定位

本次执行由两个模型分段完成。第一次返回R1检查点，保存E0—E7全部实物；第二次模型按检查点SHA接续§8，禁止重复E0—E7：

```text
03_HPC_Returned_Result_Summaries/
enzymecage_three_module_t6_r3_r1_operator_checkpoint_stage8_20260911.tar.gz
bytes=2553000
SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf

R1关键证据：
PYTHON_RUNTIME_PREFLIGHT.json SHA256=4b70c9ed...
LIGHTGBM_GATE_CLOSE.json SHA256=b5272389...
UNIFIED_GRAPH_RUNTIME_GATE.json SHA256=7cb3aece...
COMPONENT_TESTS_GATE.json SHA256=447de88b...
FIXED_ASSET_IDENTITY_GATE.json SHA256=bc58a271...
UID_SEQUENCE_GVP_POCKET_ESM_PREFORWARD_GATE.json SHA256=cbf41769...
T3B_BOUNDED_FORWARD_GATE.json SHA256=b153e4cd...
REAL_SMOKE_INPUTS.csv SHA256=97e5d6d6...
```

R2接续返回包：

```text
03_HPC_Returned_Result_Summaries/
enzymecage_three_module_t6_r3_r2_resume_stage8_teacher_topology_technical_completion_20260911.tar.gz
bytes=728862
SHA256=6844b68ac782c51556e91d77cba7c3f5f12e4e1c679a270fbcdc97ad49c3b162
```

R2的`RESUMED_FROM_CHECKPOINT_SHA256`命中上述R1 archive；所以E0—E7是有证据的前序阶段，不是R2缺跑。当前缺口位于§8后的合同闭环、报告语义和R2原始external sidecars，而不是E0—E7。

本地完整审计：

```text
04_Local_Review_Audits/
ENZYMECAGE_THREE_MODULE_T6_R3_R2_RESUME_STAGE8_TEACHER_TOPOLOGY_TECHNICAL_COMPLETION_RETURN_LOCAL_AUDIT_2026-09-11.md
SHA256=97431e4d20acafecaf880dca74f8c2d8a1f71a4f95ec8156eb3d521e27290789
```

可复用运行边界：

```text
04_Local_Review_Audits/
T6_R3_R1_REUSABLE_RUNTIME_RECIPE_AND_PERSISTENCE_BOUNDARY_2026-09-11.md
SHA256=21ea736defc589169c3af42414d5a8c9f20e892bdc36320a531ae265dd9f5ff5
```

时间、执行模型错误和资产复用明细：

```text
T6_R3_R1_PHASE_TIMING_AND_BOTTLENECK_ATTRIBUTION_2026-09-11.csv
T6_R3_R1_LLM_EXECUTOR_ERROR_ATTRIBUTION_2026-09-11.csv
T6_R3_R1_ASSET_HASH_COST_AND_REUSE_PLAN_2026-09-11.csv
T6_R3_R1_GOLDEN_RUNTIME_FILE_IDENTITIES_2026-09-11.csv
```

最终请求：请老师先裁定第七节六项固定拓扑/公共合同问题。本轮真实计算与组件结果应保留；当前不以重复模型运行代替合同修复。
