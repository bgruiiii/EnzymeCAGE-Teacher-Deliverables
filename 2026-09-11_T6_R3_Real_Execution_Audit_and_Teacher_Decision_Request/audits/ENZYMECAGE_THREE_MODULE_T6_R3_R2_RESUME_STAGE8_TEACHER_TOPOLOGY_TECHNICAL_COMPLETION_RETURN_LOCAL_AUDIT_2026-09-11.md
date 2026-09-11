# T6-R3-R2从检查点续跑老师固定拓扑技术完成包本地审计

日期：2026-09-11

审计对象：

```text
03_HPC_Returned_Result_Summaries/
enzymecage_three_module_t6_r3_r2_resume_stage8_teacher_topology_technical_completion_20260911.tar.gz

archive bytes=728862
archive SHA256=6844b68ac782c51556e91d77cba7c3f5f12e4e1c679a270fbcdc97ad49c3b162
external identity=MISSING_LOCAL
external validation=MISSING_LOCAL
```

审计方式：本地只读安全解包；manifest、结构化JSON/JSONL/CSV、四个真实子进程、源代码diff、validator、mutation、access、persistent nonmutation和老师authority独立核验；未运行模型或远端代码；未修改返回包

## 1. 总裁定

```text
LOCAL_AUDIT_VERDICT=PARTIAL_PASS_REAL_TECHNICAL_EXECUTION_REJECT_T6_FINAL_AND_G7
ARCHIVE_SAFETY=PASS
SINGLE_ROOT=PASS
REGULAR_FILES=156
MANIFEST_FILES=PASS_SET_156_OF_156
MANIFEST_SHA256=PASS_155_OF_155
EXTERNAL_THREE_FILE_DELIVERY=FAIL_IDENTITY_AND_VALIDATION_MISSING_LOCAL
E0_TO_E7=PASS_FROZEN_NOT_RERUN
T3B_NATIVE_LOAD=PASS_3_OF_3
T3B_BOUNDED_FORWARD=PASS_6_OF_6
REAL_LANGGRAPH_COMPILE=PASS
REAL_LANGGRAPH_INVOKE=PASS
REAL_LANGGRAPH_STREAM_REACHED_END=PASS_WITH_EARLY_FAIL_CLOSED_AND_PARTIAL_SCENARIOS_DISCLOSED
REAL_SMOKE_RECORDS=PASS_8_OF_8_AS_MIXED_GRAPH_AND_STAGED_RECORDS
TEST_01_TO_20=REJECT_REPORTED_19_OF_20__INDEPENDENTLY_AT_LEAST_3_NOT_ESTABLISHED_OR_FAIL
C8_TRAIT_PRODUCTION_CALLABLE=PASS
T5_ROUTE_AGGREGATOR_PRODUCTION_CALLABLE=PASS_AFTER_TYPED_REATTACH
C8_TO_T5_IN_GRAPH_CONTINUOUS=NOT_ESTABLISHED
GSCHEMA_STRUCTURAL_VALIDATION=PASS_8_OF_8
DETERMINISM=PASS_FOR_FINAL_ATTEMPT_WITH_PYTHONHASHSEED_0
MUTATION=FAIL_INCOMPLETE_CONTRACT_COVERAGE
ACCESS_AUDIT=PASS_AUTHORIZED_UNIPROT_KEGG_ONLY_BUT_VALIDATOR_HOST_PARSER_WRONG
PERSISTENT_NONMUTATION=PASS_BY_CROSS_EVIDENCE_BUT_PACKAGED_VALIDATOR_IS_WEAK_AND_HAS_FALSE_SIZE_EXPECTATION
ENVIPATH_LOOKUP_THEN_DEPENDING=NOT_ESTABLISHED_TEACHER_TOPOLOGY_GAP
SOURCE_PROVENANCE=FAIL_NULL_TAGS_AND_FALSE_ENVIPATH_DEFAULT
T5_TASK_ID_CONTRACT=FAIL_GRAPH_AND_BRIDGE_IDS_REJECTED
NO_LLM_GRAPH_CONTINUATION=FAIL_ORGANISM_SELECTION_STOPS_BEFORE_TRAIT
MODEL_RERUN_REQUIRED=false
GRAPH_RERUN_REQUIRED_NOW=false
ZERO_MODEL_EVIDENCE_CORRECTION_REQUIRED=true
TEACHER_ADJUDICATION_REQUIRED=true
T6_OVERALL_READY=false
G7_PASSED=false
```

真实运行不是假的：四个最终子进程均使用固定Python退出0，老师StateGraph真实compile，invoke/stream真实执行，五seed模型、微生物映射和C8 trait生产函数都产生了实物结果。但包内`19/20`和`C8_TO_T5=PASS`把部分链、图外调用和已披露缺口判得过宽，不能作为最终T6/G7提交。

当前不应再重跑模型或重复当前老师图。先冻结真实输出、零模型纠正报告/validator/sidecar，并将必须由老师决定的拓扑和公共ID问题一次性反馈黄老师。

## 2. Archive与manifest

```text
gzip=PASS
single root=PASS
members=183
regular files=156
directories=27
unsafe absolute/dotdot/link/device/FIFO=0
MANIFEST.files rows=156
MANIFEST.files set coverage=156/156
MANIFEST.files duplicates=0
MANIFEST.sha256 rows=155
sha256sum -c=155/155 PASS
```

`MANIFEST.files`将两个manifest追加在末尾而非全表字典序，因此列表与本地排序序列不相同，但集合完整；这是P2，不返工科学。

本地没有收到同basename identity/validation。包内`p19_closure.py`显示远端曾生成三文件，但本地实物只有archive；当前按本地事实判交付P1，不能写external delivery PASS。不得为此重跑模型或Graph。

## 3. E0—E7继承和真实§8执行

检查点身份命中：

```text
checkpoint SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf
source patch SHA256=074f5c31d516e1f699648008ed86767244e25fb128905e119366ad346f8f027a
teacher BASE_COMMIT=2d4cc766322a6a01b8a88491aed07536b3b0a320
teacher BASE_TREE=c0acb9bd30b985ad43bf969946842da97a68a400
teacher topology four files unchanged=true
```

E0—E7没有重跑。原检查点的3/3 native load、逐UID ESM门和6/6 forward以原始bytes复制，身份可核。

最终§8四个子进程：

```text
base_run1 elapsed=153.360s exit=0
base_run2 elapsed=156.262s exit=0
staged_run1 elapsed=111.071s exit=0
staged_run2 elapsed=109.613s exit=0
final successful driver wall≈530.3s
```

真实证据：

```text
compile=4 children × 1
invoke trace rows=6
stream trace rows=16
node transition rows=160
smoke rows=8 unique S1—S8
evidence documents=8 unique S1—S8
all final child problems=0
```

至少两个完整base stream和两个staged stream到达LangGraph END；SC3两个bridge观察场景按设计在enzyme_pool停止，未宣称终态。

## 4. 老师固定图的真实结果与缺口

### 4.1 enviPath lookup-first未实现

```text
teacher graph nodes=12
enviPath known-route node=absent
enviPath lookup calls=0
Route C 4051 similarity retrieval calls>0
reaction_prediction edge=present但真实smoke不可达
reaction prediction fallback实际为BioTransformer ENVMICRO
depending v3.2 graph calls=0
```

因此不能写“先查enviPath，MISS后depending”。`TEST-03`正确标为`NOT_ESTABLISHED_REAL_GRAPH`，但这不是唯一未通过项。

### 4.2 provenance丢失并存在错误enviPath标签

真实retrieved `CandidateReaction`反复出现：

```text
source=retrieved
source_tag=null
source_tool=null
```

`TEST-04`把“null by design且原样携带”判PASS，但原合同要求database/BioTransformer/ECLIPSE/depending来源全链保留。`null`不是保留来源，故TEST-04不能判PASS。

更严重的是`src/schemas/bridge.py`默认`source_tool="enviPath"`；真实graph零次enviPath lookup时，bridge步骤仍携带`source_tool=enviPath`。这是来源误归因风险。该文件属于老师固定拓扑身份，学生不能自行改，需黄老师裁定。

### 4.3 prediction crosswalk不可达

真实smoke的两个有效case均由Route C返回10条候选，因此未进入reaction_prediction。当前图没有可产生known-route MISS的lookup节点，Route C又无HIT/MISS语义，导致predicted_reactions→candidate_reactions没有在真实图中执行。

`TEST-03`未通过事实成立。后续不能用组件测试替代真实图，也不能由学生添加节点。

### 4.4 无LLM时图到END但未贯通trait

m5真实node顺序：

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

`organism_selection`因无LLM credential显式fail-closed，图内未执行`trait`和`synthesis`。到达END只表示路由结束，不等于三模块全链成功。

执行器从该thread的checkpoint state重建`EnzymeCrewState`，随后在图外直接调用production `trait_filter_node`和T5 aggregator。真实生产函数调用有价值，但不能写成图内continuous PASS。老师需决定无LLM时organism selection是否允许确定性透传/降级，或如何仍进入trait。

### 4.5 T5 task ID公共合同断裂

原始两条路径都失败：

```text
graph native reaction_task_id=NONE_SINGLE_STEP_M5
→ RouteAggregationError：必须匹配RT-...

bridge reaction_task_id=R-...:stepN.branch
→ RouteAggregationError：必须匹配RT-...
```

执行器把bridge reaction按SMILES精确重新挂到三个冻结`RT-*` ID后，production aggregator才得到4个aggregate、0 unresolved。该结果应写：

```text
PASS_COMPONENT_CHAIN_AFTER_TYPED_REATTACH
GRAPH_NATIVE_AND_BRIDGE_ID_CONTRACT=FAIL
```

不能无条件写`C8_TO_T5_REAL_CONTINUOUS_REGRESSION=PASS`。

## 5. TEST-01—20独立复核

包内状态为19 PASS + TEST-03 NOT_ESTABLISHED，但至少应修正：

```text
TEST-03=NOT_ESTABLISHED_REAL_GRAPH
TEST-04=FAIL_SOURCE_PROVENANCE_NULL_AND_FALSE_ENVIPATH_DEFAULT
TEST-11=FAIL_OR_NOT_ESTABLISHED_DENOMINATOR_SEMANTICS
TEST-12/16=C8_AND_T5_PRODUCTION_CALLABLE_PASS_AFTER_REATTACH；GRAPH_CONTINUOUS_NOT_ESTABLISHED
TEST-17=PASS_REAL_GRAPH_EXECUTION_WITH_TERMINAL_FAIL_CLOSED_LIMITATION
```

TEST-11报告：

```text
total_route_step_count=3
bridge_step_count=4
covered_by_upstream_task_ids=4
unmatched_steps=2
```

4个bridge occurrence来自两个两步分支，其中一个上游reaction重复；它们映射到3个unique upstream task。不能把4个occurrence直接作为3步分母的covered count，更不能与2个unmatched混成单一PASS。必须分别报告：branch occurrence覆盖、unique upstream task覆盖和每条route denominator。该项可从现有JSON零模型纠正，不需重跑Graph。

## 6. C8、宿主和性状实证

从真实m5 graph checkpoint中的4个organism candidates继续调用production函数，得到：

```text
unique enzyme UIDs=5
mapped UIDs=5
unique source signatures=4
trait records=75
OBSERVED=42
MISSING=33
IDENTITY_ONLY=0
F1—F15 complete=true
run1/run2 trait records equal=true
```

这证明UID→宿主→C8 trait数据与生产函数可以运行。它不证明graph的`organism_selection→trait`已经贯通，也不证明T5能接受graph-native task ID。

## 7. G-SCHEMA与确定性

包内报告：

```text
Draft202012 schema check=PASS
real evidence documents=8/8 valid
official negatives=15/15 caught
base normalised run1/run2 byte-identical
staged normalised run1/run2 byte-identical
invoke/stream same-input equivalence=PASS
all recorded numeric scores finite=true（本地递归检查）
```

最终确定性是在driver加入`PYTHONHASHSEED=0`后实现。attempt6的base/staged均漂移；attempt7仍因base结果漂移失败；attempt8才一致。因此`PYTHONHASHSEED=0`和live API字段规范化必须进入后续冻结运行配方。

注意：真实stderr含大量`Mean of empty slice`/`invalid value encountered`警告，但最终结构化score本地递归检查没有NaN/Inf。当前记P2运行警告；黄金runner应保存并计数，不能静默忽略未来非有限值。

## 8. Mutation覆盖不合格

本包mutation 13项主要覆盖：解释器、ase、worker/GPU、ESM、forward pair、manifest、validation、staged hash、run order、stream terminal。

原合同要求的以下科学mutation没有执行：

```text
invalid SMILES
pool=101
empty UID
duplicate edge
cycle
cross-step enzyme borrowing
T3每类资产单字节变异
UID map变异
C8 lookup变异
fungal非identity
F5 predicted
F15 ranking
LLM改序/造总分/造证据
schema跨字段非法值
microbe TaxID分组改signature
fallback CRLF hash改stripped hash
旧route_bridge恢复主路径
```

因此`MUTATION=PASS`只可解释为13个新增门通过，不能表示原T6 mutation合同完成。缺口可用隔离副本和冻结输出做CPU补证据，不应重跑模型。

## 9. Access与persistent validator缺陷

### 9.0 LightGBM环境报告过时

最终包的`raw_copies/PYTHON_RUNTIME_PREFLIGHT.json`仍写：

```text
lightgbm bare import=false
LIGHTGBM_IMPORT=NOT_IMPORTABLE_UNREQUIRED
```

同一文件甚至记录早期扫描的EnzymeCAGE code root `reference_count=1`。随后执行阶段已根据用户裁定启用冻结T2B venv LightGBM 4.7.0只读overlay，检查点中存在`LIGHTGBM_GATE_CLOSE.json`、compatibility和module-source matrix；但最终R2包没有复制这些最终证据。

真实Graph运行成功不等于过时E0报告可以保留为当前状态。证据纠正必须从检查点补入：裸import traceback、真实引用path:line、T2B site-packages/lib身份、SOABI、overlay前后module来源和实际TEST-01。黄金配方写`bare unavailable + pinned read-only overlay active`，不能写unrequired。

### 9.1 Access

实际捕获40个network events：

```text
rest.uniprot.org:443
rest.kegg.jp:443
```

这是老师G3允许的网络访问。包内summary却因hostname正则未解析tuple参数而写`distinct_network_hosts=[]`，p17又以`access_no_external_hosts=true`判PASS。正确门应是：

```text
authorized hosts subset={rest.uniprot.org, rest.kegg.jp}
unauthorized hosts=0
port 8001=0
```

现有原始事件支持“仅授权主机”，但validator逻辑错误，需零模型修正。

### 9.2 Persistent input

`p16_finalize.py`把task-local overlay `drfp/rxn2fp.pkl`期望bytes硬编码为44，实物为6500，因此报告`size_matches_frozen=false`；同时该字段没有并入`ok`，最终仍写status PASS。p17只检查`pers["status"]=="PASS"`，属于自报放行。

检查点冻结`FIXED_ASSET_IDENTITY_GATE.json`已证明该文件正确身份为：

```text
bytes=6500
SHA256=7e1a3d3740a465762863e41ba0090d87851129749aa9d093d7558a1885293ea4
```

本轮实物仍为6500，且小型source/topology SHA均命中；所以没有证据表明资产被改坏。但当前persistent validator不可信，必须以正确6500/SHA和全部布尔子门重建，不能保留假期望44。

## 10. 执行器修改和耗时

从首次attempt到最终attempt：

```text
attempt1 start=07:04:36Z
attempt8 end=08:35:59Z
elapsed≈91分23秒
final successful four children≈8分50秒
failed/superseded attempt directories=13
```

主要修复：

```text
A：Pydantic RankedEnzyme不能按dict下标；
B：lower-case aromatic SMILES不被substrate regex识别，harness改用同分子的Kekule表示；
C：logger handlers实际是(logger, handler) pair；
D：staged scenario缺per-scenario forward delta；
E：增加typed reattach后调用T5 aggregator；
F：overlay配置应指向相邻staged bundle，不是v1 root内部；
G：子进程启动前固定PYTHONHASHSEED=0。
```

其中B暴露真实输入兼容问题：规范lower-case aromatic SMILES会触发LLM fallback并因无credential fail-closed。harness的Kekule同分子改写可用于测试bridge，但不能证明生产入口对原canonical SMILES无问题。应纳入老师/工程缺口，不应只当测试修复。

当前as-executed runner可冻结为复现实验候选；`p16/p17/p18/p19`因上述语义、mutation和sidecar问题不能直接晋升黄金validator/closure。

## 11. Teacher决策清单

一次性请黄老师裁定：

```text
1. 是否在固定图加入enviPath known-route lookup及HIT/MISS edge；
2. MISS后的正式prediction是否为depending v3.2，还是保留BioTransformer；
3. retrieved CandidateReaction的source_tag/source_tool如何强制携带，bridge默认enviPath如何处理；
4. graph-native NONE_SINGLE_STEP_M5、bridge R-*与T5只接收RT-*的公共ID合同如何统一；
5. 无LLM credential时organism_selection是否允许确定性降级继续trait，还是保持fail-closed；
6. canonical lower-case aromatic SMILES应由substrate parser直接接受还是要求上游统一Kekule表示。
```

这些涉及老师固定graph/state/schema或正式组件角色。学生不能自行改完后宣布G7。

## 12. 下一步与返工边界

不再运行当前T6科学模型/Graph。只做一次零模型纠正：

```text
修TEST矩阵口径；
将C8→T5降为component chain after typed reattach；
修TEST-11三种分母；
修authorized network解析；
修persistent 6500/SHA硬门；
补原合同缺失的CPU mutation；
生成完整本地audit/teacher decision材料；
拿回或重建明确标注LOCAL_AUDIT的identity/validation，不能冒充原执行器sidecar；
冻结as-executed runner和环境配方，不把有缺陷的validator晋升黄金工具。
```

只有黄老师下发新拓扑/合同后，才做一个针对新版本的T6运行；届时直接复用本次环境、资产registry、worker和runner，不重走E0—E7探索。

## 13. P0/P1/P2

```text
P0/teacher authority：enviPath/depending、provenance默认、task ID、无LLM trait路由等固定图合同缺口；等待老师裁定。
P1：TEST-04/11及C8→T5判定过宽；mutation覆盖不足；access/persistent validator错误；external sidecars缺失。
P2：MANIFEST.files排序、运行warning、失败attempt保留方式；不触发科学重跑。
```

最终结论：真实技术运行取得重大进展，但T6/G7仍不能过。下一动作是零模型证据纠正并一次性反馈黄老师，而不是再让执行器继续热修或重跑整链。
