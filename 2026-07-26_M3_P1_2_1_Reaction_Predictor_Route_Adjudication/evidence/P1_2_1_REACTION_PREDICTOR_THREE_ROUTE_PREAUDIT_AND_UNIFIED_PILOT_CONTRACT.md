# P1-2.1 反应预测器三路线预审与统一小试合同

任务：`M3-P1-2.1 Reaction Predictor Three-Route Pilot`  
合同版本：`rp-pilot-contract-v0.1`  
本地冻结日期：2026-07-24（Asia/Shanghai）  
状态：**PREAUDIT COMPLETE / PILOT NOT RUN / ROUTE NOT SELECTED**

## 1. 权威要求、用户决定与本文件边界

老师在
`00_Authority_Teacher_Plan/TEACHER_REPLY_M3_NEXT_ROUND_STUDENT_PREREQUISITES_SUPPLEMENT_2026-07-24(1).md`
§2.1 要求，为“相似性不 OK → 预测”分支提供 A、B、C 三个选项之一，并满足：

```text
Input : substrate_smiles: str
Output: predicted_reactions: List[
  {reaction_smiles, confidence, provenance}
]
约束:
  reaction SMILES 可被 RDKit 解析
  confidence ∈ [0,1]
  标注预测来源
```

本轮用户决定先对 A/B/C 三条路线分别做小型 pilot，再由用户与生物学老师
审核选择；这不是“老师已要求三条路线全部实装”的改写。

本文件只冻结小试接口、输入、隔离规则、评价方法和停止条件。当前不：

- 运行任何预测器或大模型；
- 修改 `reaction_prediction_node`；
- 选择最终路线；
- 进入 M4b/M4c；
- 声称模型无泄漏、达到生产可用或已经由老师验收。

## 2. 预审结论

| 路线 | 小试实现 | 当前判断 | 运行位置/责任 |
|---|---|---|---|
| A 外部专业工具 | BioTransformer 3.0 environmental microbial backend（`EnvMicroBTransformer` / ENVMICRO；CLI `env`） | 领域最匹配；但本机缺 Java/Maven/JAR，且原生输出和 confidence 是否完全满足统一合同须真跑确认 | 晨羽/HPC 执行；本地只做审计 |
| B 外部大模型 | 同一盲测 prompt 询问多个独立模型 | 可生成候选，但置信度只能视为未校准自报值，化学有效性必须另验 | 用户收集原始回答；Codex 标准化、审核、统计 |
| C 本地规则/通路模板 | 冻结 Rhea 140 exact lookup + 独立冻结的 generic rules | exact lookup 可做接口 baseline，但不是泛化预测；项目中尚未发现可直接宣称就绪的通用降解规则库 | 本地/HPC；先冻结规则资产再运行 |

候选工具预审：

- BioTransformer 3.0 官方仓库：
  `https://github.com/Wishartlab-openscience/Biotransformer`，
  预审 HEAD `7149f7ec6b2f32f9f789bab53aa4a71db49e59e2`。
  environmental microbial backend 面向 soil/aquatic microbiota，优先进入
  A 路小试；后端类/数据名是 `EnvMicroBTransformer` / ENVMICRO，CLI token
  固定为 `env`。
- enviPath 可做环境污染物转化预测，但 Python client 依赖远程服务且新 API
  账户条件需另核；本轮保留为 A 路备选，不与 BioTransformer 混跑。
- AiZynthFinder 主要是目标分子的逆合成规划，不直接等价于
  “污染物底物 → 微生物降解产物”。
- ASKCOS 主要面向合成规划；虽含 forward prediction，也不是环境微生物降解专用。

上述“领域适配”不是精度结论。

## 3. 统一输入与答案隔离

### 3.1 冻结文件

- 可发给 B 路模型：
  `UNIFIED_PILOT_INPUTS.json`
- **禁止发给 B 路模型**：
  `UNIFIED_PILOT_ANSWER_KEY.json`
- 统一机器可读输出：
  `PREDICTED_REACTIONS_OUTPUT_SCHEMA.json`

三条路线只能读取同一份 `UNIFIED_PILOT_INPUTS.json`。A/C 所需的工具数据库
可以按各自原生方式使用，但必须披露版本；B 路不得接收化合物名称、Rhea ID、
目标反应、目标产物、EC、候选酶或证据文档。

### 3.2 冻结案例

有效案例 6 个，非法输入 1 个：

| case_id | 设计目的 |
|---|---|
| RP-P01 | 项目 split-unseen 难例；简单水解但当前检索资产有缺口 |
| RP-P02 | 项目 split-unseen 难例；Rhea 140 中 EC-null |
| RP-P03 | 简单水解 sanity case |
| RP-P04 | 脱卤 sanity case |
| RP-P05 | 多辅因子/去甲基复杂 case |
| RP-P06 | 反应方向陷阱 |
| RP-N01 | 非法 SMILES；必须 fail-closed |

Paraoxon/Carbaryl 的项目 split 审计来自
`/home/a/EnzymeCAGE-Teacher-Deliverables/M3_EXT_CANDIDATE_SHORTLIST_v0.md`。
其余化学与生物学证据来自
`00_Authority_Teacher_Plan/8 个候选污染物降解反应证据包.md`。
冻结 Rhea 反应来自：

```text
data/raw/rhea/RHEA-140_2026-01-21/tsv/rhea-reaction-smiles.tsv
SHA256 34f7fb5eff7d230c2d0243b2a669b236b075a35ffda76ebe0137b0f5dd374e02
```

### 3.3 小试定位

这 6 个有效底物在冻结 Rhea 中有已知答案，公共数据库或外部模型训练语料也可能
含这些反应。因此本轮只能回答：

- 工具能否接收真实底物；
- 能否输出可验证的候选；
- 接口、方向、provenance 和失败语义能否满足合同；
- 在这组 sanity/challenge cases 上是否值得进入下一轮。

它不能作为“真正未知底物泛化能力”或“无泄漏模型优劣”的结论。

## 4. 统一输入/输出合同

### 4.1 输入

每次调用只接收：

```text
case_id: str
substrate_smiles: str
```

处理前必须用运行环境中锁定版本的 RDKit 解析 `substrate_smiles`。解析失败时：

- 不调用下游预测；
- `status="rejected_invalid_input"`；
- `predicted_reactions=[]`；
- 保存机器可读错误原因；
- 不尝试自动修复输入。

### 4.2 输出

每个 case 输出：

```text
case_id
substrate_smiles
status
predicted_reactions: [
  {
    rank,
    reaction_smiles,
    confidence,
    confidence_semantics,
    provenance
  }
]
error
```

硬约束：

1. 最多返回 Top-5；列表顺序与 `rank=1..N` 一致，不允许并列 rank。
2. `reaction_smiles` 使用完整 `reactants>>products` 形式，且两侧非空。
3. RDKit 必须能建立 reaction 对象；反应物和产物的每个 molecule SMILES
   也必须能解析。
4. 输入底物或其经预注册标准化后的等价结构必须出现在左侧。
5. `confidence` 必须是有限数值且位于 `[0,1]`。
6. `provenance` 必须披露 route、工具/模型、精确版本、原生输出类型、配置和时间。
7. 不得为了通过原子/电荷守恒检查而偷偷添加模型未输出的水、氧、辅因子、
   质子或其他分子。
8. 原生 product-only 输出可以由适配器转换为
   `输入底物>>原生预测产物`，但必须标
   `native_output_type="product_only"` 和
   `reaction_completeness="partial_unbalanced"`；这不是完整生化方程。
9. 无候选时返回空列表，不能用查表答案或另一条路线的结果补齐。

### 4.3 confidence 语义

统一的 `[0,1]` 只是接口尺度，不表示三条路线已经校准到同一概率含义：

- A：只有工具提供可追溯的原生 `[0,1]` 概率，或有文档支持、预先登记的
  单调归一化时才能填值。不得用 rank 人为编造 confidence。若工具没有可用
  score，则该候选可保留在 raw/化学审核材料中，但**统一合同判不兼容**，
  不能伪造合规 JSON。
- B：模型必须自报 `[0,1]`，并固定
  `confidence_semantics="self_reported_uncalibrated"`；不能解释为经验正确率。
- C：exact lookup 与 generic rule 的数值只能标作
  `heuristic_tier_mapping`，不是概率。具体档位映射在运行前须经用户/刘老师
  批准并写入规则资产；当前合同不擅自定值。

任何后验调分都必须另存新字段和版本，不能覆盖原始 confidence。

## 5. 三路线隔离执行合同

### 5.1 通用隔离

1. 在所有路线完成 raw output 固化和 SHA256 前，不打开 answer key 评分。
2. 路线之间不得读取、复述或修补对方结果。
3. 每条路线单独保存：
   - 完整输入；
   - 完整原始输出；
   - 标准化输出；
   - 工具/模型/规则版本；
   - 参数与环境；
   - 开始/结束时间；
   - 错误和重试；
   - SHA256。
4. 运行后只能做预先声明的确定性格式转换；化学人工修正必须另存为
   `review_annotation`，不得覆盖原始预测。

### 5.2 路线 A：BioTransformer environmental microbial backend

预注册候选命令形态：

```bash
java -jar biotransformer-3.0.0.jar \
  -k pred -b env -ismi '<substrate_smiles>' -s 1
```

这里的功能模块是 `EnvMicroBTransformer` / ENVMICRO，但固定 commit 的 CLI
映射键是 `env`（源码映射：
`"env" -> bType.ENV -> EnvMicroBTransformer`）。帮助文本中出现的
`envimicro` 不能直接当作可执行 token；2026-07-23 的 v0.1 尝试已证明
`-b envimicro` 会在 7/7 case 上被 CLI 拒绝。

真跑前由 HPC 执行者用 `--help`/README 再核对输出参数，并记录：

- BioTransformer 版本、JAR SHA256、源码 commit；
- Java 和 Maven 版本（若从源码构建）；
- `database/` 与 `supportfiles/` 的版本/SHA256；
- 完整命令、stdout、stderr、原生 CSV/SDF；
- 每 case 用时、峰值内存（可取得时）。

当前本机预审结果：

```text
java: not found
mvn: not found
biotransformer JAR: not found
A-route execution: HPC required
```

许可风险必须在采用 A 路前单独 review：

- `database/ENVMICRO` 标为 CC BY-NC-SA 4.0，含非商业、署名和 ShareAlike 条件；
- README 要求引用 enviPath，并称商业用途需另获许可；
- 主软件 `LICENSE.md`、README 与 `pom.xml` 对 LGPL 名称/版本表述不完全一致。

本小试只作研究预审，不等于已解决后续部署许可。

### 5.3 路线 B：多个外部大模型

主分析要求至少 3 个彼此独立且能明确披露版本的模型实例。所有模型使用完全相同
的 system/user prompt、相同输入顺序、相同 Top-5 上限。主分析关闭联网/工具；
若平台不能关闭，必须如实标注，并与关闭联网结果分层统计，不能混为一组。

必须返回并保存：

- 平台、模型精确版本、访问日期；
- 是否联网、是否调用外部工具；
- temperature、top_p、seed（平台可见时）；
- 完整 system/user prompt；
- 未删改原始回答；
- 重试次数与原因。

统一盲测 user prompt：

```text
任务：对给定单一底物提出最多 5 个可能由环境微生物催化的“一步”转化反应。

你只能使用输入中的 case_id 和 substrate_smiles。不得向我追问化合物名称、
Rhea ID、EC、目标产物或候选酶。不得声称做过实验。

对每个 case 返回一个 JSON 对象：
{
  "case_id": "...",
  "substrate_smiles": "...",
  "status": "ok|rejected_invalid_input|no_prediction|error",
  "predicted_reactions": [
    {
      "rank": 1,
      "reaction_smiles": "reactants>>products",
      "confidence": 0.0,
      "confidence_semantics": "self_reported_uncalibrated",
      "provenance": {
        "route": "B",
        "source_name": "<model name>",
        "source_version": "<exact version if known>",
        "native_output_type": "full_reaction|product_only",
        "reaction_completeness": "full_claimed|partial_unbalanced"
      }
    }
  ],
  "error": null
}

硬要求：
1. confidence 必须在 0 到 1，但只是模型自报、未经校准的值。
2. 最多 5 条，按可能性降序，rank 连续。
3. 不确定辅因子时不要编造；如只会预测产物，用
   substrate_smiles>>product_smiles，并标 partial_unbalanced。
4. 输入 SMILES 非法时必须拒绝，predicted_reactions 返回空数组。
5. 只返回 JSON，不要 Markdown，不要反问，不要补充输入里没有的答案标签。
```

外部模型如果不遵守 JSON 格式，原始回答仍保留；确定性 parser 失败即记
`format_fail`，不能人工重写成“模型原答”。

### 5.4 路线 C：规则/通路模板

C 路必须分开报告两个子模式：

- `C-exact`：只对冻结 Rhea 140 做底物 exact-structure lookup。
  它验证合同接入和已知反应召回，不能写成新反应预测。
- `C-generic`：使用运行前冻结、带来源和版本的 SMARTS/通路规则生成产物。
  它才用于初步考察规则泛化。

规则来源、SMARTS、方向、适用域、优先级、冲突解决、confidence tier、
版本和 SHA256 必须在查看本轮 route outputs 前冻结。每个候选 provenance
至少包含 `lookup_rhea_id` 或 `rule_id`。规则不匹配时 abstain，禁止退回
answer key。若本轮开始前仍没有合格 generic rule asset，则如实报告
`C-generic=NOT_READY`，不得临时从 6 个答案反推 6 条 case-specific 规则。

`C-exact` 和 `C-generic` 的成绩分别报告，不合并成一个 C 路分数。

## 6. 统一验证与评分

### 6.1 两阶段验证

第一阶段在不打开答案钥匙时执行：

1. JSON/schema 合规；
2. 输入 SMILES 解析或正确拒绝；
3. reaction SMILES 解析；
4. 输入底物位于左侧；
5. confidence 范围与语义；
6. provenance 完整；
7. 原子/总电荷平衡状态；
8. 无偷偷补写分子。

第二阶段在三路线结果和 SHA256 全部冻结后打开答案钥匙：

1. 反应方向；
2. 诊断性目标产物 Top-1/Top-3/Top-5 recovery；
3. 完整 Rhea 反应等价命中（单列，不能用 product-only 冒充）；
4. 是否可映射 Rhea/EC；
5. 是否能把结果继续交给 EnzymeCAGE 构建候选酶池。

RDKit 解析与标准化版本必须写入运行记录。目前本机没有 RDKit，因此：

```text
RDKit validation: pending pilot runtime
C-route RDKit batch validation: HPC or later approved isolated environment
```

不得因本地缺依赖而声称化学验证已通过。

### 6.2 预注册匹配规则

- 分子比较使用运行时锁定 RDKit 版本的 canonical isomeric SMILES。
- 盐、质子化和常见 currency molecules 的宽松比较只能作为
  `standardized_product_match`，必须同时保留严格匹配结果。
- 诊断性目标产物出现在预测右侧才算 recovery；出现在左侧不算。
- Nitrobenzene case 以 RHEA:52886 的降解方向为准，反向命中计
  `direction_fail`。
- 其他具有直接化学合理性的产物进入人工审核队列，不自动判“化学错误”；
  但不计入本轮预注册 target recovery。
- 非法输入若被“预测”出产物，计 input-safety fail。

### 6.3 指标

每条路线/子模式分别报告分子分母，不只给百分比：

| 类别 | 指标 |
|---|---|
| 接口 | schema pass、invalid-input rejection、Top-5/rank pass |
| 化学 | reaction parse、substrate retention、atom balance、charge balance |
| 目标 | direction pass、Top-1/3/5 diagnostic-product recovery、full-reaction match |
| 追溯 | provenance completeness、raw-output/hash completeness |
| 下游 | Rhea recovery、EC recovery、candidate-enzyme-pool recoverability |
| 工程 | wall time、峰值内存/硬件（可取得时）、人工分钟数、外部调用/费用 |

“可恢复候选酶”不等于“正确酶排名第一”；两者必须分开。

## 7. 通过门槛与停止条件

本轮不预设哪条路线必须胜出。进入下一轮实现至少要求：

1. 非法输入 1/1 正确拒绝；
2. 所有纳入评分的 reaction SMILES 100% RDKit 可解析；
3. provenance 100% 完整；
4. 不伪造 confidence，不隐瞒 product-only；
5. 至少在一个有效 case 上给出可进入下游审核的候选；
6. 许可、部署和成本没有未披露的硬阻塞。

以下任一情况触发 fail-closed/暂停，不修数据后继续：

- 输入或反应 SMILES 解析失败；
- schema 不合规且确定性 parser 无法处理；
- 工具无合法 confidence，而适配器试图用 rank 伪造；
- 答案钥匙提前泄漏；
- 路线之间互抄结果；
- C 路在看过答案后临时造 case-specific 规则；
- A 路许可条件与目标部署冲突且尚未裁定。

## 8. 运行前仍需裁定的最小问题

以下不是本文件擅自决定的路线选择：

1. C 路 `heuristic_tier_mapping` 的具体 `[0,1]` 数值，由用户与刘老师在运行前批准。
2. A 路若 BioTransformer 无可用原生 confidence，是：
   - 仅作为化学候选/接口不合规对照保留，还是
   - 改试有可追溯 score 的 A 路备选工具。
3. 最终生产路线只能在 pilot 审计后选择；三路线可以组合，但组合也需要新合同，
   不能根据本轮结果自动落活代码。

## 9. 下一步顺序

合同经用户确认后，一次只做一个执行子任务：

1. A 路 HPC 最小真跑与独立审计；
2. B 路统一盲测收集与独立审计；
3. C-exact/C-generic 资产冻结、小试与独立审计；
4. 三路线统一评分汇总；
5. 用户与刘老师裁定路线；
6. 裁定后才写 `reaction_prediction_node` 接入实施合同。
