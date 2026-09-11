# T6黄金复现冻结、LLM执行器归因与加速方案

日期：2026-09-11

用途：在本次T6-R3-R1返回并通过审计后，把成功运行路线冻结为可直接重放的工程配方；以后不再重复探索环境、资产、入口、worker和validator。同时用证据判断故障来自科学模型、环境、资产、执行脚本、LLM执行器还是Qoder等承载平台。

状态：执行前方案；最终路径、bytes、SHA和时间必须在T6-R3-R1回包审计后从实物填写，不能提前猜测

## 1. 核心原则

```text
第一次成功 = 探路、排障、形成黄金配方；
第二次及以后 = 核对黄金身份、直接重放，不重新设计；
LLM负责解释合同、触发冻结工具、审计结果；
LLM不再每轮现场重写scientific worker、validator或closure；
正式老师验收保留完整科学门，但同一资产/模型/结果在同一轮只核或算一次；
没有证据不得把错误归因于用户、Qoder、科学模型或某个依赖。
```

## 2. 目前已经暴露的潜在问题

### 2.1 环境

```text
系统Python与EnzymeCAGE py312混用；
历史成功解释器未进入后续硬合同；
ase只在模型初始化时才暴露缺失；
LightGBM来自T2B冻结venv只读overlay，不在${PY}裸环境；
overlay可能遮蔽numpy/scipy/torch等既有依赖；
graph和EnzymeCAGE可能需要union runtime；
子进程可能用错误sys.executable。
```

### 2.2 大资产与模型

```text
同一大文件被多个阶段/validator重复SHA；
NFS或共享盘读取吞吐影响哈希和torch.load；
五checkpoint每个worker分别加载，初始化远慢于forward；
GVP/ESM node/ESM mean体积大；
仅核dataset[0]会隐藏其他UID缺失；
文件路径存在不等于内容身份正确；
首次成功后的资产身份没有形成统一可复用注册表。
```

### 2.3 执行脚本与validator

```text
manifest正则0条命中时出现0==0空真；
UID长度正则写错后解析0条；
or True/固定PASS/只核行数等假门；
validation在生成前要求自身存在；
失败包缺validation；
manifest漏两个manifest自身；
外置validator可能重复烧GPU；
报告生成、科学运行和closure混在一个动态脚本里。
```

### 2.4 LLM执行器

```text
长prompt理解偏差；
只完成流程形式，不追踪科学目标；
忘记历史成功入口并重新探索；
为了满足门临时写脚本，引入新正则/状态机错误；
发现一个问题修一次，未先完整扫描；
把组件PASS写成整链PASS；
在日志与报告生成上花费远多于科学计算；
上下文过长后遗漏早期约束；
停顿期间没有区分模型在跑、哈希在跑还是LLM在思考。
```

### 2.5 平台/工具

```text
Qoder或其他IDE代理的工具调用延迟；
命令超时、输出截断、上下文压缩；
shell session环境变量丢失；
前台会话终止但子进程状态不清；
无法稳定复用同一远端session；
模型回复耗时与真实命令耗时混在一起。
```

## 3. 如何判断是不是科学模型本身的问题

只有满足以下证据，才可归因于EnzymeCAGE/depending/LangGraph科学实现：

```text
黄金环境preflight通过；
入口、source、checkpoint、asset SHA全部匹配；
实际进入正式callable；
错误堆栈发生在模型forward、数据语义或真实节点内部；
同一冻结输入可稳定复现；
排除磁盘、CUDA OOM、网络和错误Python；
未经过LLM现场改写科学代码。
```

典型科学模型问题：

- forward产生NaN/Inf；
- 固定输入输出不确定性超过冻结容差；
- 正确资产与UID进入模型但排序结果科学能力不足；
- graph真实节点的公共state合同不兼容；
- 路线/候选池/宿主模块真实执行后返回空或错误结果。

以下不是科学模型问题：

- `ModuleNotFoundError`；
- Python/overlay选错；
- checkpoint路径错；
- manifest/validation错误；
- LLM生成正则错误；
- GPU worker根本未进入forward；
- API或NFS故障。

## 4. 如何判断是不是LLM执行器的问题

满足任一项并有diff/log支持，可归为LLM执行错误：

```text
prompt已经明确固定路径，LLM却选择另一个入口；
已有冻结launcher，LLM仍重写并引入行为变化；
运行前未执行prompt明确要求的preflight；
生成validator存在空真、固定PASS或未调用真实实现；
修改老师禁止修改的graph/state；
把NOT_RUN或组件PASS写成整链PASS；
同一包问题没有一次扫描完，导致多轮非必要返工；
用报告、fixture或历史结果冒充当前真实运行；
命令耗时很短，但大量wall time没有任何运行日志、进程或I/O证据。
```

必须保留：

```text
LLM_EXECUTOR_ACTION_LOG.jsonl
LLM_GENERATED_FILE_DIFFS/
COMMAND_TIMELINE.csv
PROCESS_TIMELINE.csv
PHASE_TIMING_BREAKDOWN.csv
PROMPT_REQUIREMENT_COVERAGE.csv
```

`COMMAND_TIMELINE.csv`至少记录：command_id、phase、argv、start/end UTC、elapsed、exit、stdout/stderr SHA、CPU/GPU/I/O类别、生成该命令的执行器。这样可区分“真实命令慢”和“LLM思考/返工慢”。

## 5. 如何判断是不是Qoder平台问题

不能仅因Qoder总耗时长就判定Qoder有问题。只有出现以下可复现证据才成立：

```text
同一冻结prompt、同一机器、同一launcher，Qoder触发的工具调用比直接shell稳定多出显著等待；
Qoder丢失已设置的session/env，而直接shell不丢；
Qoder截断/改写命令或忽略exit code；
Qoder在进程仍运行时误报结束，或结束后无法取回日志；
相同小型基准在其他执行器连续成功，而Qoder连续失败；
差异不能由模型版本、上下文、网络、机器负载和prompt变化解释。
```

建议在最终T6之外做一个10分钟以内的执行器基准，不重复GPU科学计算：

```text
输入：同一冻结preflight/manifest/validator任务；
执行器：Qoder与候选替代工具；
机器、文件、prompt、输出要求相同；
比较：总wall time、实际command time、无日志空窗、命令错误数、漏门数、返工次数、最终hash；
至少重复2次；
```

若Qoder明显劣于其他执行器，再停止使用Qoder做协调；但科学运行仍应由冻结shell/Python launcher完成，而不是依赖任何LLM自由发挥。

## 6. 最重要的架构改进：把LLM移出热路径

本次T6成功后冻结一个只读运行包：

```text
t6_golden_runtime_<commit>_<date>/
├── RUN_RECIPE.yaml
├── ENVIRONMENT.lock.json
├── PYTHON_OVERLAY_ORDER.txt
├── ASSET_REGISTRY.csv
├── CHECKPOINT_REGISTRY.csv
├── SOURCE_PATCH.diff
├── TEACHER_TOPOLOGY_IDENTITIES.csv
├── runtime_preflight.py
├── uid_asset_preflight.py
├── run_native_load.py
├── run_gpu_worker.py
├── run_graph.py
├── run_test20.py
├── validate_evidence.py
├── clean_closure.py
├── mutations/
├── EXPECTED_OUTPUT_SCHEMA/
├── MANIFEST.files
└── MANIFEST.sha256
```

以后LLM只允许：

```text
1. 读取老师最新authority；
2. 比较base/输入是否仍适用黄金包；
3. 生成新的TASK_ID和独立输出目录；
4. 调用冻结runtime_preflight；
5. preflight PASS后调用冻结launcher；
6. 读取结果并做独立审计；
7. 若真实base/合同变化，提交明确差异，不在运行中热改黄金包。
```

禁止LLM在正式运行过程中现场重写worker、validator、manifest parser或closure。需要修改时先在独立开发副本测试和mutation通过，再发布新的黄金包版本。

## 7. 环境一次固定

冻结：

```text
主解释器绝对路径和realpath；
sys.prefix/base_prefix；
Python和SOABI；
LightGBM只读overlay路径、版本、共享库和追加顺序；
ase/torch/PyG/RDKit/numpy/scipy/sklearn/pydantic/langgraph/xgboost等version/module.__file__；
PYTHONPATH完整顺序；
CUDA driver/runtime、GPU UUID；
wrapper source bytes/SHA；
五checkpoint bytes/SHA；
环境preflight输出schema。
```

以后先跑30秒到2分钟的快速preflight。身份一致直接运行；不一致时快速停止，不加载大资产。

不建议每次新建venv或重新安装。当前T2B LightGBM overlay如果最终通过，应冻结为明确launcher能力；它不是`${PY}`裸环境的一部分，不能忘记。

## 8. 大资产一次完整核验、多次快速复用

建立`ASSET_REGISTRY.csv`：

```text
asset_id
logical_role
path
realpath
bytes
SHA256
filesystem/device/inode
mode/read_only
verified_utc
source_manifest_sha256
consumer
```

### 8.1 日常复现模式

若老师base、资产版本和冻结registry未变：

```text
核路径/realpath；
核regular/non-symlink；
核bytes、只读权限和registry SHA；
核manifest身份；
不重新读取所有55GB计算SHA；
直接运行冻结launcher。
```

注意：mtime/inode只能作为快速漂移信号，不能单独替代正式SHA证明。

### 8.2 老师正式终验模式

当前TEST-20要求持久输入pre/post SHA不变，因此最终验收仍做完整SHA，但必须优化：

```text
每个文件每轮只算一次pre SHA；
所有组件、validator和报告共享同一registry；
post只按合同覆盖持久输入，不能每个脚本各算一遍；
外置validator复用已冻结raw registry，不再次读取同一大文件，除非合同明确要求独立复算；
独立文件可按存储吞吐适度并行，避免过高并发拖垮NFS；
记录每个asset的hash elapsed和实际吞吐MiB/s；
若未来获得授权，使用只读挂载、内容寻址或fs-verity/Merkle身份进一步加速。
```

不能在未经老师/系统授权时擅自把形式终验降级为只看mtime。

## 9. 模型计算加速

```text
三反应用三个单GPU worker并行；
每worker只初始化一次五seed模型；
同一worker处理base/repeat和分配给它的全部请求；
不要让外置validator再加载五checkpoint；
模型初始化后立即保存checkpoint和runtime身份，不反复构建；
若后续多个输入连续到来，可在授权的单任务内复用同一persistent worker；
禁止跨任务保留无法审计的后台模型服务；
先做逐UID轻量资产门，避免模型加载后才发现ESM/GVP缺口。
```

## 10. 测试与证据加速

```text
环境preflight最先；
受影响组件测试在开发阶段跑；
最终source tree的完整157项只跑一次；
TEST-01—20只跑真实production callable；
科学raw输出一旦通过即只读冻结；
报告生成只读取冻结raw；
mutation在小型隔离副本运行，不加载五checkpoint；
closure只核证据和身份，不重复科学计算；
P2标题/排版不触发任何运行；
一个包先完整扫描所有P0/P1，再一次性修复。
```

## 11. 当前T6-R3-R1回包后的冻结清单

本地审计必须生成：

```text
T6_R3_R1_REUSABLE_RUNTIME_RECIPE_AND_PERSISTENCE_BOUNDARY_2026-09-11.md
T6_R3_R1_GOLDEN_RUNTIME_FILE_IDENTITIES.csv
T6_R3_R1_PHASE_TIMING_AND_BOTTLENECK_ATTRIBUTION.csv
T6_R3_R1_LLM_EXECUTOR_ERROR_ATTRIBUTION.csv
T6_R3_R1_ASSET_HASH_COST_AND_REUSE_PLAN.csv
```

至少填写：

```text
最终成功/失败状态；
精确Python和overlay；
全部必需module路径；
模型/graph入口；
source patch；
worker/validator/closure SHA；
大资产registry；
每阶段wall/command/CPU/GPU/I/O时间；
LLM现场生成和修改文件数；
发生过的错误、发现门和是否可由黄金包消除；
哪些措施可永久复用，哪些每次仍需快速验证。
```

## 12. 是否更换Qoder的裁定门

不凭感觉更换，按以下表判断：

| 证据 | 裁定 |
|---|---|
| 科学命令本身耗时，Qoder只等待 | 不归因Qoder |
| LLM反复写错脚本，但平台工具稳定 | 可能是所用模型/长prompt问题，先用冻结launcher减少自由度 |
| 工具调用、session/env或进程状态在Qoder内可复现异常 | Qoder平台问题候选 |
| 同一小型基准其他执行器稳定更快且更准确 | 可更换协调执行器 |
| 换执行器但仍让LLM现场重写所有脚本 | 根因未消除，仍可能重复返工 |

推荐顺序：

```text
先冻结工具链，降低LLM自由度；
再用小型相同任务比较Qoder和候选执行器；
证据确认后再更换；
不拿正式T6整链反复做平台AB测试。
```

## 13. 给不熟悉代码的用户的固定汇报格式

每次必须先用白话回答：

```text
现在处于哪一步；
真实运行了什么；
没运行什么；
结果是否成功；
若失败，是模型、数据、环境、资产、脚本、LLM还是平台；
证据是什么；
下一步是否要老师裁定；
预计还需哪些必要计算；
哪些工作下次可以直接复用、不再重复。
```

不能只报门编号、文件名或代码堆栈。

## 14. 当前判断（等待回包后更新）

基于现有证据：

```text
EnzymeCAGE本身：历史同输入6/6 forward成功，当前没有证据证明模型本身坏了；
环境/入口：曾重复选错Python，是已证实问题；
资产：真实可用，但核验和加载成本高，存在重复工作；
validator：已发生多次设计缺陷，是已证实问题；
LLM执行：现场脚本开发和合同理解造成明显返工，是已证实风险；
Qoder平台：尚无独立对照或工具级日志证明，当前不能定责；
最大改进：冻结黄金运行包，让LLM退出正式科学运行热路径。
```

本次T6-R3-R1回包后，按第11节补齐实物身份和时间归因，再决定是否更换Qoder。
