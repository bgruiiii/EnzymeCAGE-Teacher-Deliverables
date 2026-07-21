# EnzymeCAGE M3-P1 解冻条件闭环、Case 1 边界复核与案例扩展裁定申请

日期：2026-07-21

回复老师文件：

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_CASE_FREEZE_AND_WRAPPER_MODE_ADJUDICATION_2026-07-20(3).md
```

当前状态：学生侧 6.1、6.2 已完成并通过本地复核；6.3 保持老师已接受路径与身份；
本文件同时按 6.4 提交微生物侧简要现状。尚未启动或宣称完成 M3-P1 Agent、
三案例推理、M4/M5 接入或任何新案例资产构建。

## 一、本轮结论

老师规定的两个 M3-P1 解冻条件现已闭环：

```text
[x] 6.1 三个正式 case JSON 到位并独立复核
[x] 6.2 晨羽稳定绝对路径、Python 3.12.3 激活命令、单 GPU 配置手段到位
```

请老师确认接收后，按原裁定由导师侧启动 M3-P1 Agent 正式代码实现。学生侧
没有提前编写导师侧 LangGraph 代码，也没有运行三案例或调用模型。

三案例整体角色保持老师冻结原文：

```text
Case 1：B-primary + strong pool=1 → pipeline 走通验证 + 污水占位（非排序验证）
Case 2：B-primary + medium 3/8 recall → EnzymeCAGE 排序能力测量（唯一）
Case 3：B 空 → C-fallback → pool ∩ positive = 0 → fail-closed 分支验证

组合覆盖 M3 三种系统行为：B 走通 / B 走通 / B 空 → C → fail-closed。
组合不覆盖“EnzymeCAGE 效果全景评估”，后者不在 M3 契约范围内。
```

## 二、6.1 三个正式 Case JSON

直接提交文件：

```text
README.md
case_1_rhea_40543.json
case_2_rhea_11532.json
case_3_rhea_24292.json
```

三份 JSON 均包含老师要求的所有字段。反应 SHA256、Rhea/EC、canonical
reaction SMILES、难度、路线、污水状态、角色、B/C 独立 pool、完整已知正例、
历史 D4 rank、学生原机理自审以及 Rhea 140/B1/A1A provenance 已逐项复算。

| Case | B pool / 命中 | C pool / 命中 | 冻结执行角色 |
|---|---:|---:|---|
| Rhea:40543 | 1/1 | 5/1 | B-primary 最小 pipeline；非排序验证 |
| Rhea:11532 | 10/3 | 17/3 | B-primary；唯一排序测量案例 |
| Rhea:24292 | 0/0 | 79/0 | C-fallback 后 fail closed；不调用 `predict()` |

Case 3 的 `role` 为
`UPSTREAM_RECALL_FAILURE_FAIL_CLOSED_DEMO`。没有增加第四个 case，没有合并
B+C，没有改变 pool 成员，也没有补资产。

文件身份：

```text
2910a3800f1f942036b124712d9ab3f0d49c876e6e71856597eac97516b27e6c  README.md
8596a089ac4f3a4fc6164079fb359ddfdde9fd25a45e903fe8bdf9e3ed67b8e2  case_1_rhea_40543.json
cdaf710c1838e976fab284a6275e3b4d57bcee6e6be0f86bd03a474c3314196b  case_2_rhea_11532.json
3fb4c772abe397a98bfbb34255bb55798d85215105b765912bde80b7a01ef30d  case_3_rhea_24292.json
```

## 三、6.2 晨羽稳定运行上下文

### 3.1 稳定绝对路径

```text
D4_WRAPPER_ROOT=
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/
d4b1a_wrapper_hash_relative_path_final_package_correction_20260716

ENZYMECAGE_V1_PACKAGE_ROOT=
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/
enzymecage_v1_20260714

ENZYMECAGE_CODE_ROOT=
/usrdata/EnzymeCAGE_data/EnzymeCAGE-master
```

逻辑路径、realpath、挂载来源、可读性和冻结身份均已复核。D4 70/70、v1
48/48、M3 数据资产23/23项在环境修正前后均通过；模型注册表和科学代码锚点
未改变。

### 3.2 固定 Python 环境

```bash
source /usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/activate
```

```text
Python = 3.12.3
Pydantic = 2.12.5
pydantic-core = 2.41.5
temporary overlay = false
```

第一次预检如实阻断于固定环境缺少 Pydantic；随后只用五个固定 SHA256 的
离线 wheel 补齐获准依赖。未使用在线索引、`/tmp` overlay、`--target`、
`--user`，也未改变 torch、PyYAML、RDKit、NumPy 或模型科学依赖。

direct 和 activated 两种 import-only 探针均通过，wrapper/schema/predictor
均解析到已接受 D4 根目录，`_runtime_for_audit() is None`。本轮未调用
`predict()`、未初始化 runtime、未加载模型或 checkpoint。

### 3.3 单 GPU 配置方式

```text
method = MANUAL_CUDA_VISIBLE_DEVICES
activation_pattern = export CUDA_VISIBLE_DEVICES=<one physical GPU index>
visible_device_contract = exactly 1
```

本轮没有固定或占用物理 GPU。正式作业时由调用方选择一个物理 GPU 索引，
保证 wrapper 只看见一张卡。

直接提交的稳定上下文：

```text
stable_runtime_context.json
SHA256: 145aaebcefb189f712edbf1efefb1d4ce61cf0a5e5cba68ab20b0bba72191af6
contract: enzymecage_m3_p1_stable_runtime_context_v1
item 6.2: PASS
```

## 四、6.3 数据资产路径

老师已接受且当前保持不变：

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/
m3_agent_data_assets/
```

```text
MANIFEST.sha256:
db875a42c9e4fe79a4490d974dbba6c2a7778ef092844787559f5f26166e6d26

原 tar.gz SHA256:
734964077898de8dd3abd167fe1285d1d905f33296abe687edc54bcf65858dc1

原 tar.gz size:
9,334,420 bytes
```

本轮没有更新资产，因此不重复上传或重新打包。

## 五、6.4 微生物侧最新反馈（独立于 M3，不阻塞 M3）

按老师 7 月 18 日对 MT-D1--D8 的裁定，当前 enzyme→organism 数据源口径为：

```text
UniProt reviewed organism + NCBI taxon ID：主证据
KEGG Organism：独立补充/交叉证据，保留 0/1/N multiplicity
TrEMBL unreviewed：v1 默认不纳入，除非后续单独授权并带降级标志
```

已接受 D5 证据为 UniProt 10/10 精确返回；KEGG 对十个固定 UID 的映射呈
7 个单映射、1 个零映射、2 个多映射。不得把 KEGG 多命中折叠成唯一宿主，也
不输出未经校准的 `organism_confidence` float。

老师已于 7 月 18 日另行授权 M4a（`Enzyme2OrganismTool` +
`OrganismAggregator`）启动。当前授权范围内的实现、离线测试和 M4a-4 联调
基准证据已完成本地审计，状态为“可提交老师审阅”，不是“老师已验收 M4a”。
具体实现、基准结果和待裁定问题由独立的 M4a 教师材料提交，不并入 M3
解冻条件。

metaTraits v1 allowlist 校对与老师7月18日裁定一致：

| Trait | v1 角色 |
|---|---|
| temperature | soft |
| pH | soft |
| salinity | soft |
| oxygen_preference | soft |
| biofilm | 不使用；无数据时标 unknown |
| safety/pathogenicity | soft + 人工复核标记 |

上述为老师裁定的 v1 trait 政策；当前 M4a 不消费 trait，也没有据此执行过滤。
所有可用 trait 均为 `soft + uncertainty_flag`，不执行不可逆 hard 剔除；
专家 hard allowlist、方向和阈值仍待确认。M4b/M4c 尚未获得授权，porTraits、
bulk observation 抓取和模型训练均未启动。

当前 M4a 尚待老师裁定的事项包括：A/B/C 排序公式及稳定 tie-break、snapshot
合同草案、维护方邮件、最终 checkpoint 加载策略、零额外本地模型时的共存证据
解释，以及 exact-tax-ID 与 species/同物种其他菌株的 trait 归因规则。以上事项
不阻塞本轮 M3-P1 解冻，也不构成微生物完整链路已经完成的声明。

## 六、Case 1 冻结后生物学边界复核

我们在冻结后进一步核对了官方 UniProt/ExPASy/ChEBI 证据。复核结论是：

```text
Rhea:40543、EC 1.14.15.33、UID O87605、反应方向和羟化机理均正确；
B=1、C=5及 B-primary pipeline 角色不变；
但该反应是大环内酯抗生素生物合成中的羟基化步骤，
不是抗生素在污水中的降解、去除、解毒或矿化。
```

此前材料已经写明“plausible、未在污水体系验证、未证明产物更易降解”，
所以没有直接声称真实降解效果；但“污水抗生素场景占位”仍可能被误读。
后续报告应明确写成：

> Case 1 是 B-primary 最小 pipeline 验证和抗生素相关酶促转化占位。项目表把
> 底物列入广义抗生素新污染物，但具体反应属于抗生素生物合成；没有建立污水
> 降解、去除、解毒、矿化或工程效果证据。

因为老师已经冻结 Case 1，且 6.1 要求保留学生原机理自审，我们没有静默修改
JSON、反应、route 或 pool。现请老师重新裁定其保留或替换。

## 七、现有测试集内替换建议：RHEA:46976

这是已有正式测试集内的推荐，不是下面第八节所说的额外外部反应。

```text
Rhea master: 46976
forward direction: 46977
reaction SHA256: 9737dd8c994296811f87278e33cc7c8b1743112ddf9ecb745ba6de1e1dc2971a
reaction: (S)-6-hydroxynicotine + O2
          -> 6-hydroxy-N-methylmyosmine + H2O2
difficulty: STRONG_TOP_5
known positives: Q93NH4, A0A075BSX9
historical ranks: 2, 3
B pool: 0 / 0
C pool: 15 / 2
runtime route under current contract: C-fallback
```

正式切分复核结果：

```text
train rows for Rhea:46976 = 0
valid rows for Rhea:46976 = 0
test rows for Rhea:46976 = 41，其中正例2条
```

因此它是训练和验证均未见的正式 test 反应，但不是完全独立于原测试集的外部
反应。它已经被查看过历史 rank，若用于 M3 只能作为披露后的案例演示，不能
作为无偏总体性能估计。

官方证据支持两个 UID 参与尼古丁降解，生物学业务含义明显强于现有 Case 1。
但现有证据只支持“尼古丁降解相关、烟草废物/污水场景 plausible”，不支持
“已在真实污水工程中验证”或“必然提高污水处理效率”。

数据库粒度还需保留以下事实：冻结 Rhea 140 `rhea2ec.tsv` 没有为
RHEA:46976 直接挂 EC；包含后续自发水解的总体反应 RHEA:11880 才挂
EC 1.5.3.5。当前公平 B 合同不跨相关/多步反应继承 EC，因此 B 为空，不能
静默把1.5.3.5写进当前精确 B 查询。

如果老师选择替换，新的正式配置中 RHEA:46976 的直接 `ec` 应保留为 `null`
或老师指定的等价缺失值，并把 RHEA:11880/EC 1.5.3.5 只记录为相关总体反应
provenance；不能把相关总体反应 EC 冒充查询反应的直接 EC。

替换还会改变三案例角色组合：Case 2 仍保留 B-primary 排序测量，新的 Case 1
则由“B-primary 最小走通”变为“B 空、C-fallback 成功并召回2/2正例”。这样
会增加成功 fallback 分支的覆盖，但不再保留原 pool=1 的专用最小 B-primary
案例。因此如选择替换，三案例首页角色说明也需由老师一并重新冻结，不能只换
反应文件而沿用旧说明。

若老师同意替换，需要重新冻结 Case 1 配置和身份；在此之前我们保持现有三份
JSON 不变。

## 八、额外外部新污染物降解案例建议（尚未选定）

原始 train/valid/test 按 `CANO_RXN_SMILES` 反应组、固定 seed=42 做
80/10/10 切分，得到3,601/450/451个反应，三者反应交集为0。当时没有按
污水或新污染物业务场景分层选取测试反应；M3 的污水筛选是在正式切分以后
追加的业务筛选。

因此我们另提出一个尚未执行的建议：后续单独寻找一个具有可靠新污染物降解
证据、且 canonical 反应同时不在 train/valid/test 中的外部反应，作为独立
外部挑战案例。该建议与 RHEA:46976 完全分开，目前：

```text
具体反应尚未选择
正确酶尚未冻结
未生成候选池
未调用 EnzymeCAGE
未补任何 D4 资产
未把它加入当前三个 M3 case
```

若老师原则同意，我们建议先按生物学与数据独立性标准选定并冻结反应、正确酶
和证据，再运行 B/C 候选召回与模型，避免看完模型结果后只挑成功案例。还需
先检查候选是否位于 D4 可计算资产域；域外资产补齐不在当前 M3 授权内，应由
老师决定作为独立 M3 扩展还是后续 M4/M5 任务。

## 九、请求老师逐项裁定

```text
M3-Q1：是否确认学生侧6.1、6.2到位，并按原裁定启动导师侧 M3-P1 实现？

M3-Q2：对冻结 Case 1，请选择：
       A. 保留 Rhea:40543，但采用第六节更严格的生物合成/非降解披露；
       B. 重新冻结 Rhea:46976 作为替代 Case 1，保持当前精确 B 合同，
          以 C-fallback 成功案例运行；
       C. 其他老师指定方案。

M3-Q3：是否原则同意后续另选一个同时不在 train/valid/test 的外部新污染物
       降解反应，先冻结后运行，并另行确定资产补齐与阶段归属？
```

老师裁定前，我们不修改冻结 Case 1，不新增第四个 M3 case，不跨 Rhea 反应
继承 EC，不启动外部案例资产构建，也不把上述建议写成已经获得的效果结论。

## 十、不做项确认

本轮没有并且不会自行执行：

```text
HTTP / FastAPI / OpenAPI / SSH tunnel
B+C union
pool >100 静默截断
D4 wrapper 或 v1 模型身份修改
外部候选资产补齐
M4b/M4c 或 M5 接入
未经老师重新冻结的 Case 1 替换
真实污水治理效果宣称
```
