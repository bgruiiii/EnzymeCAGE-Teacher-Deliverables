# EnzymeCAGE M3 数据资产 #6 Wrapper 接口现状与调用模式确认申请

日期：2026-07-20

回复老师文件：

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_P0_ADJUDICATION_AND_IMPLEMENTATION_CONTRACT_2026-07-17.md
```

## 一、结论先行

当前晨羽智云上的 D4 v1.1 是老师已验收的 **Python 函数级 wrapper**，尚未部署
HTTP 服务。因此目前不存在可提供的 URL、端口、HTTP 认证方式或 OpenAPI 文档。
Python wrapper 本身也没有 API key、token 或用户认证层；当前访问控制来自晨羽
账户、SSH 和文件/运行环境权限，不能表述为应用级 API 认证。

这不是运行失败，而是既有授权边界：老师在 D4/M3 启动文件中明确 M3 不做
FastAPI 服务化；当前实现也没有 FastAPI、Flask、Django、ASGI 或 WSGI 依赖及
服务入口。

本文件把已经存在的 Python 请求/响应契约完整列出，并申请老师确认 M3 集成采用：

```text
M3I6-A（建议）：LangGraph 与 EnzymeCAGE 运行在同一晨羽环境，直接 Python import；
M3I6-B：由老师另行定义远程 SSH 作业调用协议；
M3I6-C：另行授权设计 HTTP 服务，作为当前 M3 之外的独立任务。
```

在老师确认前，不自行新增 HTTP 层，也不把 SSH 端口转发描述成已经存在的服务。

## 二、冻结实现身份

接受包：

```text
03_HPC_Returned_Result_Summaries/
d4b1a_wrapper_hash_relative_path_final_package_correction_20260716/
```

固定身份：

```text
D4 manifest SHA256:
944fe2d22b6b43808a1d6a6250ad62e652a4b52e7e7b36d91a58a012fecd326d

schema.py SHA256:
a27f33adf78bb2c7a9961d4372cfea0f7728ca91eb89e3b0a6cc7a1e6488fc35

predictor.py SHA256:
b9877649deea4f929778331453a0f1f4eb73d72529e3f1c4b95d0a56c4ab82d3

asset_index.py SHA256:
07dceed083aecb5310ac3b208f0a1bca8e147aeb69897908b529045ba30d7d3c
```

冻结模型版本为 `v1_20260714`，正式推理使用 corrected-pocket ESM-2 3B
五模型 ensemble（seeds 40--44）。运行时要求 Python 3.12.3、冻结科学环境和
恰好一张可见 CUDA GPU。

## 三、当前 Python 调用契约

导入入口：

```python
from enzymecage_wrapper import EnzymeCAGERequest, EnzymeCAGEResponse, predict
```

调用进程必须能同时导入冻结 wrapper 和科学代码，并指向与 wrapper 共置的冻结
v1 包。等价的环境准备形式为：

```bash
export D4_WRAPPER_ROOT=<accepted d4b1a package directory>
export ENZYMECAGE_CODE_ROOT=/usrdata/EnzymeCAGE_data/EnzymeCAGE-master
export ENZYMECAGE_V1_PACKAGE_ROOT=<accepted enzymecage_v1_20260714 package directory>
export PYTHONPATH="${D4_WRAPPER_ROOT}:${ENZYMECAGE_CODE_ROOT}:${PYTHONPATH:-}"
export CUDA_VISIBLE_DEVICES=<one selected GPU>
```

D4 验收时记录到的模型包 observed path 是：

```text
/usrdata/EnzymeCAGE_data/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_v1_20260714
```

它是该次验收运行的证据路径，不应未经部署前复核就宣传成长期稳定服务路径。
实际集成必须重新确认 wrapper 与 `enzymecage_v1_20260714` 仍是已验收身份且路径
可读，不能指向另一个同名但未验收的目录。

最小调用形式：

```python
request = EnzymeCAGERequest(
    reaction_smiles="<canonical reaction SMILES>",
    enzyme_pool_uids=["<UID1>", "<UID2>"],
    top_k=10,
    return_ci=True,
)
response = predict(request)
```

此示例只说明函数契约，不表示任意 reaction 或 UID 都有冻结资产，也不表示已经
完成 M3 三案例推理。

## 四、请求 schema

`EnzymeCAGERequest`：

| 字段 | 类型 | 必填/默认 | 约束与含义 |
|---|---|---|---|
| `reaction_smiles` | string | 必填 | 目标 canonical reaction SMILES；必须存在冻结 DRFP 和分子图资产 |
| `enzyme_pool_uids` | list[string] | 必填 | 至少 1 项；由上游 B-primary/C-fallback 检索提供 |
| `top_k` | integer | 默认 10 | `1 <= top_k <= 100` |
| `return_ci` | boolean | 默认 true | 是否返回五 seed 2.5%/97.5% 经验分位范围 |

正式 M3 调用还受老师裁定约束：B、C 独立 pool 都必须 `<=100`；B 非空用 B，
B 为空才用 C；不做 B+C 并集；不依据已知正确 UID 选路。

`evidence_hash` 使用原始 UID 列表计算，保留重复项；模型 forward 前按首次出现
顺序去重。无效或缺完整酶资产的 UID 会被过滤，不进入 forward 和输出。

## 五、响应 schema

`EnzymeCAGEResponse`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `ranked_enzymes` | list[`RankedEnzyme`] | 按 score 降序、UID 作为并列确定性次序；长度为 `min(top_k, 有效唯一 UID 数)` |
| `model_version` | string | 固定 `v1_20260714` |
| `evidence_hash` | string | reaction、原始 UID 列表和模型版本的 SHA256 追溯摘要 |

`RankedEnzyme`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `uid` | string | 候选酶 UID |
| `score` | float | 五 seed ensemble 平均分 |
| `rank` | integer | 从 1 开始的连续排名 |
| `ensemble_ci` | null 或 `[float, float]` | 五 seed linear 2.5%/97.5% 经验分位范围；`return_ci=false` 时为 null |

`ensemble_ci` 不是统计学置信区间，也不能据此宣称生物学显著性。

## 六、失败与过滤语义

| 条件 | 当前行为 |
|---|---|
| 请求字段类型或 `top_k` 越界 | Pydantic validation error；不进入推理 |
| 未设置有效 package root | `RuntimeError`；不进入推理 |
| 可见 GPU 数不是 1 | `RuntimeError`；不进入推理 |
| reaction 缺 DRFP 或分子图资产 | `MissingReactionAssetError`；forward 前 fail closed |
| 部分 UID 缺完整酶资产 | 静默过滤这些 UID，只对剩余有效 UID 推理 |
| 所有 UID 均无效 | 返回空 `ranked_enzymes`；不执行 forward |
| 已初始化后改用另一个 package root | `RuntimeError` |

上游 M3 Agent 必须把空候选、pool 超限、缺反应资产和全无效候选保留为明确失败
状态，不能把空结果包装成正常推荐，也不能在线补资产。

## 七、运行时边界

1. 五个模型在首次调用时初始化一次；已验收实测 init 约 67.85 秒，warm-50
   约 0.33 秒，warm-100 约 0.56 秒。
2. 模型存在已披露的 batch-context sensitivity。每个 case 的实际候选 pool 必须
   作为一个完整请求提交，不能切块后合并排名，也不能混入其他 case。
3. 当前锁只保护 runtime 初始化；并发多请求推理和共享 `last_trace` 的线程安全性
   未做正式验收。因此不能把当前 wrapper 宣称为可并发 HTTP 服务。
4. D4 只覆盖冻结反应和 107,705 个完整酶资产 UID；不生成新 ESM、GVP、
   pocket-node、DRFP 或分子图资产。
5. 当前 wrapper 只返回模型排序结果，不负责 B/C 检索、污水判断、机理审核、
   酶到菌映射或 MetaTraits。

## 八、为什么 SSH 端口转发当前不能直接解决

SSH 端口转发只能转发一个已经监听的 TCP 服务。当前没有 HTTP 进程和监听端口，
所以单独建立 SSH tunnel 不能产生 API。若采用远程 SSH 方式，需要另行定义命令
入口、输入输出文件或标准流协议、作业串行化、超时和错误回传；这些均尚未冻结。

因此，当前最小且与老师既有 M3 边界一致的方案是 `M3I6-A`：让导师侧
LangGraph 在同一晨羽科学环境内直接 import 冻结 Python wrapper。若导师侧编排
不运行在晨羽，请老师在 `M3I6-B` 与 `M3I6-C` 中另行裁定，本地再按裁定准备，
不先行假设。

## 九、请求老师确认

请老师确认：

1. M3-P1/M3 后续集成是否采用 `M3I6-A`，即同一晨羽环境直接 Python import；
2. 若导师侧 LangGraph 不部署在晨羽，是否改走 SSH 作业协议，或另行授权 HTTP
   服务化；
3. 在调用模式确认前，是否认可本文件作为 #6 的当前能力与缺口说明，而不是把
   尚不存在的 URL、认证或 OpenAPI 虚构为已交付。

本文件不新增服务、不启动 M3-P1，也不改变已经验收的 D4 wrapper。
