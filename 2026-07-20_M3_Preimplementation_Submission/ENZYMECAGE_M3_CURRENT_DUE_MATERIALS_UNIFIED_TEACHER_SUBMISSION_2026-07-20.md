# EnzymeCAGE M3 当前可交付材料统一提交与确认申请

日期：2026-07-20

回复老师文件：

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_P0_ADJUDICATION_AND_IMPLEMENTATION_CONTRACT_2026-07-17.md
```

## 一、本次提交目的

按照老师“先确认三案例，再写 M3-P1 代码”的顺序，本次把当前不越过权限、能够
完成的材料一次提交：

1. 三个待冻结案例的选择与机理自审；
2. 老师要求尽快提供的 #2--#5 数据资产包；
3. #6 wrapper 当前接口能力、缺口和调用模式确认申请。

本次没有把待确认案例写成已冻结，没有启动 M3-P1/M3-P2/M3-P3/M3-P4，也没有
增加 HTTP 服务、资产补齐、B+C 并集、MetaTraits 或新模型推理。

## 二、提交物与状态

| 老师资产编号 | 本次材料 | 当前状态 |
|---|---|---|
| #1 | `ENZYMECAGE_M3_CASE_SELECTION_AND_MECHANISM_SELF_REVIEW_REQUEST_2026-07-20.md` | 三案例预冻结申请；等老师确认后才生成正式 YAML/JSON |
| #2 | Rhea 140 四个固定 TSV | 已装入 `m3_agent_data_assets.tar.gz` 并通过本地审计 |
| #3 | 4,051 个 query-excluded 参考反应索引和 radius-8 指纹库 | 已装包并通过本地审计 |
| #4 | 107,705 UID 的 D4 冻结资产可用性表 | 已装包并通过本地审计 |
| #5 | 公平 query-excluded EC-to-UID 表 | 已装包并通过本地审计 |
| #6 | `ENZYMECAGE_M3_ASSET_6_WRAPPER_INTERFACE_STATUS_AND_CALL_MODE_DECISION_REQUEST_2026-07-20.md` | Python 契约已说明；当前无 HTTP，等老师确认调用模式 |

## 三、#1 三案例预冻结结果

| Case | 角色 | Reaction SHA256 | B pool/命中 | C pool/命中 | 建议运行路线 |
|---|---|---|---:|---:|---|
| 1 | strong 污水 plausible | `240655c6546e987d720edcb3f4467e2076ac97245172d81343831e7dfc97f3a8` | 1/1 | 5/1 | B-primary |
| 2 | medium 非污水 | `19fe5b26e16a1a8ca60628be8718d3162cabded0299e2276a8503aec787bcf15` | 10/3 | 17/3 | B-primary |
| 3 | weak 非污水技术边界 | `03900c0cd72deb2cdbdc826defd03e694d0ac53cd1ec8fbba509845fe1b92152` | 0/0 | 79/0 | C-fallback 后候选召回失败 |

三个案例的 B、C 独立 pool 均不超过 100。Case 1/2 两路均召回正确 UID；case 3
是 21 个 weak query 中唯一同时满足两池上限的候选，但 B/C 都没有召回正确 UID。
因此 case 3 只能作为“上游候选召回失败”的技术边界，不能写成模型排序成功。

污水相关性也保持原边界：case 1 只是规则支持的抗生素/新污染物 plausible case，
需要老师或领域专家审核；case 2/3 不宣称污水相关。

详细 reaction SMILES、Rhea/EC、完整 B/C UID、机理自审、历史 rank 和八项逐 case
记录状态均在 #1 申请正文中列明。本次没有重跑模型；所列历史 rank 来自冻结
A1A 证据，pool 来自公平 query-excluded B1 证据。

## 四、#2--#5 数据资产交付

提交文件：

```text
m3_agent_data_assets.tar.gz
m3_agent_data_assets.tar.gz.identity.txt
```

晨羽 HPC 共享路径：

```text
数据目录：
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/m3_agent_data_assets/

交付压缩包：
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/m3_agent_data_assets.tar.gz

压缩包身份文件：
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/m3_agent_data_assets.tar.gz.identity.txt
```

老师要求的 #2--#5 在数据目录中的具体位置：

```text
#2 Rhea 140 四个 TSV：
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/m3_agent_data_assets/assets/rhea140/

#3 route-C 参考反应索引与 radius-8 指纹库：
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/m3_agent_data_assets/assets/route_c/reference_reaction_index.csv.gz
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/m3_agent_data_assets/assets/route_c/reference_morgan_radius8.pkl

#4 D4 UID 资产可用性表：
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/m3_agent_data_assets/assets/d4/uid_asset_availability.csv.gz

#5 公平 query-excluded EC-to-UID 表：
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/m3_agent_data_assets/assets/route_b/ec_to_uid_query_excluded.csv.gz
```

建议老师优先取完整 `m3_agent_data_assets.tar.gz`，并使用紧邻的 identity 文件
核对 SHA256；目录内路径用于导师侧工具开发时直接读取。

外部身份：

```text
SHA256: 734964077898de8dd3abd167fe1285d1d905f33296abe687edc54bcf65858dc1
bytes:  9334420
```

已审计内容：

```text
Rhea 140 固定 TSV                         4 个，固定哈希全部匹配
route-C 非 query 参考反应                 4,051
route-C Morgan radius                     8
route-C 指纹分子                          4,000
D4 完整资产 UID                           107,705
route-B 唯一完整 EC                       2,320
route-B 唯一 (EC, UID)                    101,638
route-B/route-C 对 451 query 的直接泄漏   0
```

HPC 独立验证器重建了全部资产，复现全部 451 条 C top-10 邻居和 B 候选池；八项
变异测试均按预期拒绝。返回目录 manifest、外部 tar.gz、identity、确定性 gzip、
ustar 元数据和 fresh extraction 均通过本地独立审计。

这些是离线、release-pinned 的 Rhea 140 和冻结 formal/D4 数据，不是在线 API
逐条查询结果。它们证明工具输入可复现，不证明候选召回、EnzymeCAGE 排序或
真实污水生物学效果优秀。

## 五、#6 当前接口能力

D4 v1.1 当前只提供已验收 Python 函数级接口：

```python
from enzymecage_wrapper import EnzymeCAGERequest, EnzymeCAGEResponse, predict
```

请求字段为 `reaction_smiles`、`enzyme_pool_uids`、`top_k`、`return_ci`；响应为
`ranked_enzymes`、`model_version`、`evidence_hash`。缺反应资产时 forward 前
fail closed，缺酶资产 UID 被过滤，全无效 UID 返回空列表。

当前没有 HTTP URL、监听端口、认证或 OpenAPI；SSH port forwarding 不能转发
不存在的服务。为保持老师既有“M3 不做 FastAPI”边界，本地建议导师侧 LangGraph
在同一晨羽环境直接 Python import。若导师侧不部署在晨羽，请老师另行裁定 SSH
作业协议或授权独立 HTTP 服务化任务。

Python wrapper 本身没有 API key、token 或应用级用户认证；当前访问控制只来自
晨羽账户、SSH 和文件/运行环境权限。

## 六、请老师本轮确认的事项

### 6.1 三案例冻结

请老师确认：

1. case 1 Rhea:40543 作为 strong 污水 plausible；
2. case 2 Rhea:11532 作为 medium 非污水；
3. case 3 Rhea:24292 是否接受为“候选召回失败型 weak 技术边界”。

老师确认后再生成正式 #1 YAML/JSON，并以确认后的三个 reaction SHA256 为固定
case 身份。在此之前不写 M3-P1 Agent 代码。

### 6.2 Wrapper 调用模式

请老师确认 M3 集成是否采用：

```text
同一晨羽环境直接 Python import（本地建议）；
或远程 SSH 作业协议；
或另行授权 HTTP 服务化。
```

## 七、当前里程碑边界

```text
M3-P0 路线裁定                          已完成
#1 三案例选择与学生机理自审             已完成，待老师确认冻结
#2--#5 数据资产                         已完成并通过本地审计
#6 Python 契约与 HTTP 缺口说明           已完成，待老师确认调用模式
正式 #1 case YAML/JSON                   等老师冻结后生成
M3-P1 Agent 代码                         BLOCKED_PENDING_TEACHER_CASE_FREEZE
M3-P2/P3/P4                              NOT_AUTHORIZED
```

本次只申请老师审阅和裁定，不把本地通过升级成老师已验收，也不把候选召回或
历史 rank 包装成真实世界最优酶结论。
