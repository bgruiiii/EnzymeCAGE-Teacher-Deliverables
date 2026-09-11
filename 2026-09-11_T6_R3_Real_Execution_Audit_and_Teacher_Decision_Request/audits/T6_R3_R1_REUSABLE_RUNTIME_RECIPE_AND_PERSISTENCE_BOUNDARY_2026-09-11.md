# T6-R3-R1/R2可复用运行配方与持久化边界

日期：2026-09-11

状态：`TECHNICAL_RUNNER_CANDIDATE_WITH_TEACHER_CONTRACT_GAPS`；不是最终G7黄金包

依据：

```text
T6-R3-R1检查点 SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf
T6-R3-R2技术完成包 SHA256=6844b68ac782c51556e91d77cba7c3f5f12e4e1c679a270fbcdc97ad49c3b162
T6-R3-R2本地审计=ENZYMECAGE_THREE_MODULE_T6_R3_R2_RESUME_STAGE8_TEACHER_TOPOLOGY_TECHNICAL_COMPLETION_RETURN_LOCAL_AUDIT_2026-09-11.md
```

## 1. 可直接冻结复用的入口

```text
Python=/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python
Python version=3.12.3
ASE=3.29.0
LangGraph=1.2.9
PYTHONHASHSEED=0（必须在子进程启动前设置）
teacher BASE_COMMIT=2d4cc766322a6a01b8a88491aed07536b3b0a320
teacher BASE_TREE=c0acb9bd30b985ad43bf969946842da97a68a400
source patch SHA256=074f5c31d516e1f699648008ed86767244e25fb128905e119366ad346f8f027a
```

LightGBM：

```text
${PY} bare import=FAIL
capability=冻结T2B venv LightGBM 4.7.0只读末位overlay
T2B interpreter=/usrdata/EnzymeCAGE_envs/enzymecage_three_module_t2b_v32_single_smiles_runtime_adapter_staged_20260907/bin/python
T2B site-packages=/usrdata/EnzymeCAGE_envs/enzymecage_three_module_t2b_v32_single_smiles_runtime_adapter_staged_20260907/lib/python3.12/site-packages
lightgbm package=<上述site-packages>/lightgbm
shared library=<上述site-packages>/lightgbm/lib/lib_lightgbm.so
```

不得把最终R2包内过时的`NOT_IMPORTABLE_UNREQUIRED`当黄金状态。必须使用R1检查点的`LIGHTGBM_GATE_CLOSE.json`、compatibility和module-source matrix重建最终环境锁。

## 2. 可复用科学runner候选

| 文件 | bytes | SHA256 | 状态 |
|---|---:|---|---|
| `as_executed_p15_real_langgraph_chain.py` | 16925 | `3857a355fa23ed9c11fb34b83a95f7fb45ccdcb43f594acd708aade73a1e6846` | 可复用driver候选 |
| `as_executed_p15_shared.py` | 19953 | `36e37e5b4fe127d88c94fd0da3a61e70e40161db04c1055709138e29d4711bd3` | 可复用观察/规范化候选 |
| `as_executed_p15b_chain_base.py` | 48286 | `3e4983a10bb726a613d55eb96e9ce3b84fe7d689a3ae4b0b5e5f26eb4cb51708` | 可复用base runner候选，含task-ID/输入workaround限制 |
| `as_executed_p15c_chain_staged.py` | 23357 | `d89b6ff2b8d24371967894898797e656be84754b303612cf30c10aa789a14146` | 可复用staged runner候选 |
| `as_executed_r1_common.py` | 20100 | `424e4de70eae15e8e7fdc83756511987e7d9f688bdc28d1b512f7b5d6c84cd07` | 可复用公共路径/身份工具候选 |

成功调用顺序：

```text
生成base/staged四份配置
→ base_run1
→ base_run2
→ staged_run1
→ staged_run2
→ 比较base norm bytes
→ 比较staged norm bytes
```

最终成功耗时：

```text
base_run1=153.360s
base_run2=156.262s
staged_run1=111.071s
staged_run2=109.613s
total≈530.3s
```

运行时必须保留：

- `PYTHONHASHSEED=0`在spawn环境中；
- 固定Python和overlay顺序；
- base与staged package root分进程，不能同进程切换wrapper singleton；
- raw live UniProt/KEGG响应与规范化确定性视图分开；
- 所有score保留raw，规范化比较只屏蔽明确允许的float/time/live transport字段。

## 3. 暂时禁止晋升黄金的工具

| 文件 | SHA256 | 禁止原因 |
|---|---|---|
| `p16_finalize.py` | `00277e0abd5c652e290c72a501566749d77e6c86c92c6335260b5c8f85b19429` | TEST-04/11和C8→T5口径过宽；persistent将6500错误写成44且不参与status |
| `p17_validator.py` | `fc31efcfa5ab2493e599f547d425c5d31b0ce124ef4846bfdf35e161ef2adc75` | 信任persistent status；错误要求no external hosts；接受TEST-04/11过宽与manual reattach |
| `p18_mutations.py` | `3e57600dce94a15fc0eb6f8e174eb331dd9fc5294fd39261fc5a0b25c32c37f4` | 只覆盖13项新增门，漏原科学mutation合同 |
| `p19_closure.py` | `c582139a2ae8729aedab3b4968f3a3d31dbbe7b172d61ea891bb7eaa266d8cc6` | 依赖有缺陷p17；本地最终仍缺identity/validation |

它们只能作为失败历史和重构参考，不能下次原样调用后宣布PASS。

## 4. 资产复用

继续复用检查点已完成的资产registry，不重新探索路径：

```text
GVP SHA256=8e1c5138aaf6fe45af2ca14b61631925cdbed661a052deff35155b01027ff96e
ESM node SHA256=960e882fd116466785b7d648a085e78be1b5e00975cc3b8660ac566e724ea89e
ESM mean SHA256=e44f70f4e2e5f9cc1269a8271397c5f51736ec4d7c0268f3a7f1427bc0201707
staged rxn2fp bytes=6500 SHA256=7e1a3d3740a465762863e41ba0090d87851129749aa9d093d7558a1885293ea4
uid map SHA256=7b92e8e625cb73f070c8e902687ea5bbdbf749f04a19828e550e3fe205684fe6
C8 lookup SHA256=d51a540db2f9798d65e25b46f22960ba29ae2d4b288be218c83c299f24f5d5af
```

日常复现只核路径、realpath、regular/non-symlink、bytes、只读/registry身份；老师最终新版本验收再按其合同完整SHA一次。同一轮每个大资产只算一次并共享。

## 5. 已知不可固化为成功的合同缺口

```text
enviPath lookup-first absent；
prediction fallback实际BioTransformer且真实prediction path不可达；
retrieved source_tag/source_tool为null；
bridge默认source_tool=enviPath造成误归因；
graph native/bridge task ID不能进入T5 aggregator；
无LLM时organism_selection终止，trait只在图外续接；
lower-case canonical aromatic SMILES会落入LLM解析并fail-closed；
TEST-11 denominator混用branch occurrences和unique upstream tasks。
```

老师未裁定前，不得把runner候选命名为G7 final，也不得修改老师graph/state/schema。

## 6. 下一版本正确入口

老师裁定后，新版本只允许：

```text
1. 复用本文件环境和资产registry；
2. 将老师新BASE_COMMIT/TREE作为新版本；
3. 对老师批准的图/ID/provenance变化做最小patch；
4. 跑2分钟环境/入口门；
5. 只对受影响路径做component tests；
6. 调用冻结p15 runner结构，不现场重写；
7. 用修正版finalizer/validator/mutation/closure；
8. 输出三文件。
```

LLM只能选择TASK_ID、核authority和调用这些固定入口；不能正式运行时热改runner。

## 7. 晋升黄金的条件

```text
老师对六项合同缺口完成裁定；
新老师base真实运行；
TEST-01—20全部按修正语义PASS；
C8→T5图内或老师批准的边界状态成立；
原合同+新增mutation全部通过；
access区分authorized/unauthorized；
persistent门全部真实参与all-pass；
archive/identity/validation本地三文件收件；
本地独立审计PASS。
```

当前只冻结为`T6_TECHNICAL_RUNNER_CANDIDATE_V1`。
