# HPC executor-only prompt：T6-R3老师修复后拓扑真实LangGraph、20项终验与三文件最终执行

日期：2026-09-10  
执行者：Chenyu AI / executor only  
任务性质：T6真实最终运行；允许CPU和2—3个独立单GPU worker；禁止训练与production写入

## 0. Authority已满足与唯一目标

黄老师09-09要求“先回传8001/entryType自查再谈重跑”。该自查现已：

```text
本地独立审计通过；
archive/identity/validation三文件通过；
上传老师GitHub commit=0e6ca8ececf29317cc6aa465267bcae2cadcd7ed；
老师入口=2026-09-10_T4_Final_Stage_and_T6_PreR3_Selfcheck/。
```

黄老师同一文件同时明确：只以老师修复后拓扑跑T6-R3，学生不改图、不重排。本轮唯一目标是按该拓扑真实执行T6-R3：

```text
fresh teacher main exact base
→ 应用已审计pre-R3固定补丁
→ 接入已冻结T2/T3/T5/C8组件（不改老师拓扑）
→ 真实StateGraph compile + invoke + stream
→ 8条smoke和3条反应native load/6条forward
→ TEST-01—TEST-20
→ determinism/mutation/access/schema
→ archive/identity/validation三文件。
```

本轮不得再做microbe报告封口；其证据直接作为固定输入。若真实图或组件失败，保留首个真实堆栈并返回`BLOCKED_AT_*`，不能继续用报告修复冒充T6运行。

## 1. Authority payload

```text
t6_r3_teacher_authority_prer3_selfcheck_and_20test_contract_payload_20260910.tar.gz
bytes=15648
SHA256=0554305d60295c94d3c92e674175e6744faf496c0d6f3e15df95b34feaf8054d
single root=t6_r3_teacher_authority_prer3_selfcheck_and_20test_contract_payload_20260910/
regular files=3
```

成员：

```text
老师09-09原件：5995 bytes / SHA256=953920dfe98106c763b5d726aa7de98105cc0a971adfa755e47fc8d417aeccb4
pre-R3自查最终本地审计：4974 bytes / SHA256=30c9711042daf0e5ddfff53ddf3bb3af0827d46bcae7cefde5d575c00904ba80
原T6 20项合同：20806 bytes / SHA256=ab4aa93d174fdf33e198c4f70abdd8c220523a60d0ded26964e2988a12901b38
```

冲突优先级：老师09-09原件 > pre-R3最终审计 > 原20项合同。原合同的旧base、旧route_bridge拓扑预期和旧microbe口径均被09-09裁定及pre-R3审计替代；TEST-01—20的科学目标继续有效。

## 2. Fresh路径

```bash
TASK_ID=enzymecage_three_module_t6_r3_teacher_fixed_topology_real_langgraph_20_test_final_20260910
ROOT=/usrdata/EnzymeCAGE_data/EnzymeCAGE-master
WORK_ROOT=/usrdata/EnzymeCAGE_data/workspaces/${TASK_ID}
STAGED_REPO=${WORK_ROOT}/depending_teacher_fixed_final
INPUT_ROOT=${WORK_ROOT}/inputs
RUNTIME_ASSETS=${WORK_ROOT}/runtime_assets
RETURN_ROOT=${ROOT}/HPC_Returned_Result_Summaries
RETURN_DIR=${RETURN_ROOT}/${TASK_ID}
ARCHIVE=${RETURN_ROOT}/${TASK_ID}.tar.gz
IDENTITY=${ARCHIVE}.identity.txt
VALIDATION=${ARCHIVE}.validation.txt

AUTHORITY_PAYLOAD=${ROOT}/HPC_Inputs/t6_r3_teacher_authority_prer3_selfcheck_and_20test_contract_payload_20260910.tar.gz
PRER3=${RETURN_ROOT}/enzymecage_three_module_t6_r3a_r2a_r3_clean_external_validation_order_three_file_final_20260910.tar.gz
PRER3_ID=${PRER3}.identity.txt
PRER3_VAL=${PRER3}.validation.txt
```

六个输出路径和任何同basename临时sidecar任一存在立即`BLOCKED_NONFRESH_TARGET`；不删除、不覆盖、不续跑。

## 3. 固定代码base与pre-R3补丁

```text
teacher remote=git@github.com:Water-Quality-Risk-Control-Engineering/depending.git
branch=main
BASE_COMMIT=2d4cc766322a6a01b8a88491aed07536b3b0a320
BASE_TREE=c0acb9bd30b985ad43bf969946842da97a68a400

PRER3 archive bytes=146872
PRER3 archive SHA256=14c6b3ab04b7306eed2c52ece849039a37dfab8245ef48a5335df3faa32a494b
PRER3 identity SHA256=711556300de4d6dea03107f9bc875cca1dcd4deed3c62d9cc6085cff3cbee504
PRER3 validation SHA256=c60813bf4870751771e377ff1af513ec2d2e575cbc9e234346ca39a1c472c921
PRER3 SOURCE_PATCH.diff SHA256=40dd1f16d64d941e747d7f96360bc3d4051eb8d3452d0d088ed37fe4620e8563
```

先核PRER3三文件、P12/12、Q10/10、OVERALL PASS。fresh clone并detach到精确BASE_COMMIT/TREE，对PRER3累计patch做`git apply --check/apply`。禁止使用旧9f5ad0bf或旧R2 staged tree作为最终base。

老师G1文件必须保持BASE_COMMIT字节身份；若累计patch触及graph/state/router/edge或改变老师节点顺序，立即BLOCK，不自动合并。

## 4. 旧T6固定输入仍按SHA使用

从原20项合同继续使用并逐项核：

```text
T2D archive SHA256=0ef31f7ab29bf15f0b18ab59c6b6f6c9d7f3c7498e96bb31c8d91672c94fe4af
T3A archive SHA256=3836180271f372a2ea3612333f4429b17039f0524346d09bd3f3b85eb66ebfaa
T3B archive SHA256=f8f9d8e0b85ef7d5fe8c0b7a617575b9a9cc5cfc27a9b9a2515340dc88d84201
T3B-R1 archive SHA256=eb434860397e8c2110fbcc5087622aa5cc924f177c968c3ac2e78f8cd1ddc805
T5A-R2 archive SHA256=051c80d9d04c1a240e902163ef75bd1bd90e8b52d65d6ea1f25972d64ffa6085
T5B-R2 archive SHA256=444589018e84912338604e210642b901c72db0f0e42c284573e44be7bacf1694
T5C-R2 archive SHA256=a02ee942c9ee4fa6c790ddb2253ec175cd129a1a6cd27a961c2bc2bcdba8ff26
UID map SHA256=7b92e8e625cb73f070c8e902687ea5bbdbf749f04a19828e550e3fe205684fe6
C8 lookup SHA256=d51a540db2f9798d65e25b46f22960ba29ae2d4b288be218c83c299f24f5d5af
```

全部普通文件、非symlink、安全archive、manifest通过。不得按mtime/“最新”猜文件。

## 5. 集成预检：先判老师main已有能力，避免盲叠旧patch

在改任何非拓扑代码前输出`CURRENT_TEACHER_TREE_COMPONENT_INVENTORY.csv`：

```text
PredictedReaction唯一对象及字段；
depending v3.2 adapter；
reaction_task_id/typed reattach；
route-step aggregator；
C8 adapter与F1—F15；
microbe direct REST/map fallback；
official G-SCHEMA validator；
老师graph节点/edge顺序。
```

规则：

1. PRER3已包含的G2/G3/G4/G5/microbe实现直接复用，不再改。
2. 老师base已有的T2/T5能力不得从旧patch覆盖。
3. 缺失的T5C纯工具/adapter才允许从固定T5C reference逐文件语义移植；不得修改graph/state。若必须新增老师未定义state键，输出`BLOCKED_PUBLIC_STATE_CONTRACT`并停止。
4. `src/schemas/evidence.py`共同字段用三方字段矩阵核对，禁止整文件ours/theirs。
5. microbe候选按positive NCBI TaxID；只有后续T5 route-step按`source_signature + resolution + TaxID + normalized exact name`精确聚合，两层不得再混用。

输出`CUMULATIVE_PATCH_MERGE_PLAN.csv`和所有最终source SHA。先跑CPU组件回归；通过后冻结代码，后续失败不得反复改算法。

## 6. 真实T3B native load和6条forward

固定三个反应任务和三UID身份沿用原合同。三反应必须3/3真实`load_geometric_dataset`，保存tensor shape/dtype/device/finite。每反应最多2 UID，总forward严格6条。

为加速可使用2—3个独立worker并行，但每个进程必须：

```text
CUDA_VISIBLE_DEVICES只暴露1张卡；
固定seed、eval、no_grad；
不训练、不backward；
不共享可写reaction asset/cache；
输出worker/card/reaction/UID/checkpoint/config/asset SHA和原始score。
```

禁止单进程多卡、DDP或改wrapper。3/3 load或6/6 forward任一失败，保留真实堆栈并`BLOCKED_AT_T3B_NATIVE_LOAD/FORWARD`。

## 7. 真实LangGraph运行

必须使用安装环境真实`langgraph.graph.StateGraph`和老师base的真实graph builder：

```text
compile至少1次；
invoke至少1次；
stream至少1次并消费到终态；
保存逐node event、state key变化、route/task/source/UID/host/trait/evidence hash；
禁止自建StateGraph、monkeypatch graph或task脚本手填最终state。
```

拓扑必须体现老师09-09裁定：检索/单步预测成功直连酶池，多步桥只作旁路预留。真实运行不能在旧route_bridge断点停止。

冻结8条smoke preregistration与C1—C4控制场景沿用原合同；不得看结果后换样本。host来源必须用已审计PRER3节点输出，不能图外重查拼结果。

## 8. TEST-01—TEST-20

完整执行authority payload中原20项合同§6，逐项建立`TEST_CASE_MATRIX.csv`。补充解释：

```text
TEST-16的分辨率隔离属于T5 route-step精确聚合；不得据此改变microbe节点的TaxID生产主键；
TEST-17使用老师新拓扑，不再期待旧route_bridge主路径；
TEST-12 host必须来自真实microbe节点输出，C8真实adapter后进入T5；
TEST-20核所有持久输入pre/post SHA零变化。
```

每项必须有真实production callable、输入身份、expected、observed、raw log、PASS/FAIL。禁止`or True`、固定PASS、只查字段存在、把异常一律当PASS。

## 9. C8→T5真实连续回归

必须用真实microbe节点输出：

```text
UID/host evidence
→ C8 lookup/adapter真实调用
→ 15个trait slots
→ 冻结T5 route-step aggregator
```

禁止手填F1—F15。observed/missing/identity-only必须来自真实lookup；porTraits不启用。若候选不覆盖OBSERVED，诚实记录coverage不足，不能换样本。

## 10. 确定性、mutation、访问和零写

同一8条输入fresh process完整运行两次，规范化科学JSONL逐字节一致。mutation至少覆盖原合同§7全部类别，并额外覆盖：

```text
microbe TaxID分组被改成signature；
fallback完整CRLF hash被换成stripped hash；
validation预创建/固定PASS；
旧route_bridge被恢复为主路径。
```

访问审计必须证明T4 blind/gold/restricted、NON_BBD、未授权网络=0 reads；production/formal/输入=0 writes；训练/backward=0。

## 11. 速度优化纪律

```text
Phase A CPU integration/preflight只跑相关测试；
代码冻结后不因报告/sidecar问题再改source；
Phase B 6 forward可由2—3个单GPU worker并行；
Phase C graph场景可独立进程并行，但每个场景必须是真实完整invoke/stream；
完整20项和155项/历史组件回归只在final code tree跑一次；
报告层复用统一clean closure，不重新发明validator；
archive/identity/validation作为原子结果一次返回。
```

任何阶段首个真实科学失败可提前封包，不继续无意义全量测试；但已完成证据必须保留。

## 12. 必须返回

至少包含原20项合同§8全部文件，并新增：

```text
CURRENT_TEACHER_TREE_COMPONENT_INVENTORY.csv
TEACHER_FIXED_TOPOLOGY_IDENTITY.json
PRER3_SELFCHECK_INPUT_IDENTITY.json
C8_TO_T5_REAL_CONTINUOUS_REGRESSION.json
GPU_WORKER_ASSIGNMENT_AND_ISOLATION.csv
PHASE_TIMING_BREAKDOWN.csv
FAILURE_OR_READY_DECISION.json
```

关键必有：

```text
REAL_LANGGRAPH_INVOKE_TRACE.jsonl
REAL_LANGGRAPH_STREAM_TRACE.jsonl
NODE_STATE_TRANSITIONS.jsonl
T3B_NATIVE_LOAD_AND_FORWARD_RESULTS.jsonl
REAL_SMOKE_INPUTS.csv / REAL_SMOKE_OUTPUTS.jsonl
TEST_CASE_MATRIX.csv
SCHEMA_VALIDATION_REPORT.json
DETERMINISTIC_ORDER_CHECK.json
MUTATION_CHECK.json
ACCESS_AUDIT.jsonl
PERSISTENT_SOURCE_NONMUTATION.json
SOURCE_PATCH.diff / T6_INCREMENTAL_PATCH.diff
END_TO_END_REPORT.md
COMMAND_LOG.txt
FINAL_STATUS.txt
MANIFEST.files / MANIFEST.sha256
scripts/
```

## 13. 统一clean三文件closure

直接复用已经通过审计的顺序，不再另造自引用门：

```text
archive内部只写CONTENT_READY或精确BLOCKED，不提前写external PASS；
archive落盘；
写identity；
确认validation及临时同名文件不存在；
pre-write验证archive+identity；
exclusive首次写validation；
第二fresh解包post-write核三文件；
final-readonly；
archive/identity/validation原子返回。
```

validation必须真实重放patch、相关组件测试、TEST-01—20、graph compile/invoke/stream证据、8条smoke、3 load/6 forward、C8→T5、schema、determinism、mutation、access和pre/post SHA。

## 14. 最终状态

只有全部成立才在外置validation写：

```text
T6_R3_TEACHER_FIXED_TOPOLOGY_FINAL_READY_FOR_LOCAL_AUDIT
TEST_01_TO_20=PASS_20_OF_20
REAL_LANGGRAPH_COMPILE_INVOKE_STREAM=PASS
T3B_NATIVE_LOAD=PASS_3_OF_3
T3B_BOUNDED_FORWARD=PASS_6_OF_6
REAL_SMOKE_RECORDS=PASS_8_OF_8
C8_TO_T5_REAL_CONTINUOUS_REGRESSION=PASS
GSCHEMA=PASS
DETERMINISM=PASS
MUTATION=PASS
PERSISTENT_INPUT_NONMUTATION=PASS
EXTERNAL_THREE_FILE_DELIVERY=PASS
T6_OVERALL_READY_FOR_LOCAL_AUDIT=true
G7_PASSED=AWAITING_LOCAL_AUDIT
```

任一不成立，精确写`BLOCKED_AT_<FIRST_GATE>`、expected/observed、非敏感完整堆栈和已完成证据；不得写20/20、T6 overall ready或G7 pass。

最终只打印三文件绝对路径、bytes/SHA、phase timing、GPU worker结果、首个失败门或READY常量，然后停止。不merge production、不push、不跑T4。
