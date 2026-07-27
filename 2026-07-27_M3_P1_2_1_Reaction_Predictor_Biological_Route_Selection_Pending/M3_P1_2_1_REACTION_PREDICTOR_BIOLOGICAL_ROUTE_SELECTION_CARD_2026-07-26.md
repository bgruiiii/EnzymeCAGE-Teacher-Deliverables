# M3-P1-2.1 反应预测器 A/B/C 生物学路线详细选择卡

日期：2026-07-26  
用途：刘老师会前阅读并在 A/B/C 中选择下一阶段主路线  
状态：**A/B/C PILOTS REVIEWED / BIOLOGICAL ROUTE SELECTION PENDING / NO IMPLEMENTATION AUTHORIZED**

## 1. 这次真正需要选择什么

黄老师在 2026-07-24 补充任务单 §2.1 要求：当现有反应相似性检索“不 OK”时，
用独立反应预测路径产生候选反应。老师给出的正式选项是：

```text
A：逆合成/正向反应预测工具（专业工具）
B：LLM 生成候选 reaction SMILES + 有效性校验
C：规则库/已知降解路径模板匹配
```

无论选哪一路，最终都应满足同一最小接口：

```text
Input:
  substrate_smiles: str

Output:
  predicted_reactions: List[
    {
      reaction_smiles,
      confidence,
      provenance
    }
  ]

硬门:
  reaction_smiles 是完整反应而非只有底物和主要产物；
  RDKit 可解析；
  confidence ∈ [0,1] 且语义明确；
  provenance 可追溯；
  不满足时 fail-closed。
```

本轮学生侧先用同一套输入分别探测 A/B/C，再请刘老师选择主方向。这个安排不表示
黄老师要求三路全部实装，也不表示三路已经达到生产合同。

## 2. 统一小试与评分条件

### 2.1 输入和盲测门

```text
有效底物:
  6 个
非法输入:
  1 个
diagnostic product targets:
  7 个（其中 1 个 case 有 2 个目标产物）
```

三个路线使用同一套冻结输入。答案钥匙只在以下门禁通过后解锁：

```text
解锁前检查:
  25/25 PASS
独立重算:
  43/43 PASS
评分器反向测试:
  6/6 PASS
评分器完整复跑:
  与正式机器报告字节一致
```

### 2.2 “命中”分别代表什么

本卡严格区分三种结果：

1. `diagnostic-product hit`：预测结果中出现正确主要产物；
2. `full-reaction hit`：有方向的完整反应左右两侧分子集合均与答案一致；
3. `D4-valid pool nonempty`：正确 Rhea 可映射出至少一个当前 D4 域内酶候选。

三者不能互相替代。尤其：

- 主要产物命中不等于完整生化反应正确；
- 完整反应命中不等于 EC 或候选酶映射一定存在；
- 非空候选酶池不等于正确酶一定在池内，更不等于正确酶排第一。

### 2.3 本轮测试集的能力边界

6 个有效目标反应都已经存在于冻结 Rhea 140。因而：

- A/B 可以观察“从底物生成候选产物”的表现；
- C-exact 只能作为“已知反应能否被精确查回”的 baseline；
- 本轮没有证明任何路线能可靠预测 Rhea 库外的未知完整反应。

## 3. 路线 A：外部专业反应预测工具

### 3.1 本轮实际探测对象

本轮没有测试所有专业工具，只测试：

```text
BioTransformer 3.0
backend:
  EnvMicroBTransformer / ENVMICRO
CLI token:
  env
source commit:
  7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
```

选择该工具的理由是 environmental microbial backend 在领域描述上与环境微生物降解
较接近；“领域接近”不是精度背书。

### 3.2 实测结果

```text
有效 case 执行:
  6/6
raw product rows:
  26
RDKit 可解析:
  25/26
不可解析:
  RP-P06 中 1 条产物，碳显式价态超限
可解析子集 diagnostic case hit:
  4/6（仅诊断，不是正式分数）
可解析子集 diagnostic product hit:
  4/7（仅诊断，不是正式分数）
native rank:
  无合法可用值
confidence:
  无可用于统一合同的值
完整 reaction:
  无
直接 Rhea / EC / D4 pool:
  不可恢复
每个 case wall:
  约 1.09—1.27 秒
```

正式结论：

```text
NOT_SCOREABLE_CONTRACT_INCOMPATIBLE
```

没有删除或人工修复那条非法产物后再给 A 补算正式分数。

### 3.3 A 的优点

- 专业工具的规则和知识域比通用 LLM 更容易固定版本、固定命令并保存运行资产；
- 本轮 6/6 有效输入均完成执行，单 case 运行时间较短；
- ENVMICRO 的应用方向与环境微生物转化相关；
- 若找到原生输出完整反应、rank、confidence 和 provenance 的更合适专业工具，
  A 在工程可复现性上可能更容易形成稳定服务。

### 3.4 A 的缺点和风险

- 当前 BioTransformer ENVMICRO 输出的是产物集合，不是老师合同所需的完整反应；
- 缺少合法 native rank 和可用 confidence，不能后验随意补字段；
- 1/26 原始产物 RDKit 不可解析，触发 fail-closed；
- 无法从当前输出直接恢复 Rhea、EC 和候选酶池；
- Maven SNAPSHOT 依赖使“由冻结源码完整重建”尚未被充分证明；
- 本轮失败只证明“当前 BioTransformer ENVMICRO v0.5 不合适”，不能外推成
  “所有专业工具路线都不行”。

### 3.5 如果刘老师选择 A，下一步实际意味着什么

选择 A 不代表直接接入当前 BioTransformer。下一步应当：

1. 先重新筛选一个能原生输出完整反应或能以可审计方式闭合完整反应的专业工具；
2. 冻结版本、源码/模型、依赖、命令、许可、rank/confidence 语义；
3. 使用新的 blind set 做同合同小试；
4. 任一 RDKit、完整性、方向、confidence 或 provenance 门失败即停止；
5. 小试通过且黄老师另行授权前，不修改 `reaction_prediction_node`。

## 4. 路线 B：大语言模型生成候选反应

### 4.1 本轮实际探测对象

保留进入统一技术验证的三个结果：

```text
ChatGPT-labelled
DeepSeek-labelled
Qwen-labelled
```

Gemini 原始输出因没有按统一格式完整返回而淘汰，没有进入评分。

“labelled”表示模型名称和版本是收集时由用户填写的界面标签，不是平台 API
attestation。三个模型分别评分，没有把输出混合重排。

### 4.2 技术有效性

```text
ChatGPT-labelled predictions:
  24
DeepSeek-labelled predictions:
  9
Qwen-labelled predictions:
  26
总预测:
  59
Reaction SMILES 可解析:
  59/59
底物保留在左侧:
  59/59
```

但 59 条结果的共同属性是：

```text
native_output_type:
  product_only
reaction_completeness:
  partial_unbalanced
confidence:
  self_reported_uncalibrated
```

也就是说，形式上写成 `substrate >> predicted_product`，但没有补齐真实反应所需的
水、质子、电子、辅因子、共底物、副产物等，因此不能当作完整生化方程。

### 4.3 目标主要产物评分

| 模型标签 | Top-1 | Top-3 | Top-5 |
|---|---:|---:|---:|
| ChatGPT-labelled | 4/6 | 5/6 | 5/6 |
| DeepSeek-labelled | 4/6 | 4/6 | 4/6 |
| Qwen-labelled | 4/6 | 4/6 | 5/6 |

这里 `Top-5 = 5/6` 的准确含义是：6 个底物中，有 5 个底物的正确 diagnostic
主要产物出现在模型前 5 个候选中。它不表示：

```text
完整反应正确 5/6;
Rhea 找回 5/6;
EC 找回 5/6;
正确酶找回或排第一 5/6。
```

已知偏差：

- 三个模型都没有找回 Paraoxon 的冻结离子态 diagnostic products；
- DeepSeek 非法输入的状态和空预测正确，但缺合同要求的 `error.message`；
- Qwen 存在 whole-file prefix 偏差；
- 模型调用时间、外部费用和人工收集时间没有统一可靠记录，HPC 的 0.18 秒只代表
  59 条结果的 RDKit 后处理，不能当作模型生成成本。

### 4.4 B 的优点

- 是本轮唯一直接表现出“给定底物，生成库中未显式检索出的候选产物”的路线；
- 三个独立模型在 4—5/6 case 上找回主要产物，说明值得继续验证生成能力；
- 59/59 输出能被 RDKit 解析且保留底物方向，基础格式门表现好；
- 不依赖目标反应已在冻结 Rhea 中，理论上能够覆盖真正的库外候选；
- prompt、原始回答、平台标签和后处理可以分别留存 provenance。

### 4.5 B 的缺点和风险

- 当前只生成 product-only partial reaction，不满足老师的完整 reaction 合同；
- 自报 confidence 未校准，不能当作正确概率或直接参加跨来源融合；
- 平台模型版本没有 API 级证明，可复现性弱于本地冻结工具；
- 可能出现幻觉、漏辅因子、元素/电荷不守恒和错误方向；
- 目前不能从原始输出直接恢复 Rhea、EC 或 D4 候选酶池；
- 本轮 6 例不是未知反应 blind 泛化证据，后续不能继续用同 6 例声称新验证。

### 4.6 如果刘老师选择 B，下一步实际意味着什么

选择 B 表示把 B 作为“反应相似性失败后的研究方向”，不是批准当前 product-only
结果进入生产。下一步仍须：

1. 用新的 blind set；
2. 让模型输出完整 reactants/products，而不是只写 `substrate >> product`；
3. 固定 RDKit、原子/元素守恒、形式电荷、方向、底物保留、重复项、模型版本和
   provenance 门；
4. 把 `self_reported_uncalibrated` 与正式 confidence 分开；
5. 只有完整反应通过门禁后，才测试 Rhea/EC/候选酶池衔接；
6. 黄老师另行授权前，不接入活代码。

## 5. 路线 C：规则库或已知降解路径模板

路线 C 必须拆成两部分看，否则会把“查表”误写成“预测”。

### 5.1 C-exact：冻结 Rhea 140 精确结构查表

实现方式：

- 在冻结 Rhea 140 原始 reaction SMILES 中，以底物结构严格命中左侧组分；
- 只返回方向正确的完整冻结 Rhea reaction；
- 继续通过冻结 Rhea→EC→UniProt→D4 映射衔接下游。

实测：

```text
Rhea 原始 rows:
  36,014
预注册排除不可解析 rows:
  2
searchable rows:
  36,012
6 个有效底物有候选:
  6/6
正确 directed Rhea Top-1:
  4/6
正确 directed Rhea Top-3:
  5/6
正确 directed Rhea Top-5:
  6/6
完整反应 Top-5:
  6/6
正确目标有 non-null 冻结 Rhea EC:
  5/6
正确目标 D4-valid pool 非空:
  4/6
全扫描 wall:
  约 36.68 秒
独立 validator 重算:
  约 35.79 秒
```

具体下游边界：

- Paraoxon 和 Carbaryl 的正确 Rhea 都排第 1；
- 但二者冻结 Rhea→UniProt 映射均为空，所以仅靠当前链路仍没有候选酶池；
- Carbaryl 的冻结 Rhea EC 保持 `null`，没有把外部 IUBMB/BRENDA 的
  `3.5.1.137` 写回 Rhea；
- 其余 4/6 可形成非空 D4 pool，但不能据此宣称正确酶必在池内或排第一。

### 5.2 C-exact 的优点

- 当前唯一能直接返回完整、方向明确、可追溯 Rhea 反应的实现；
- frozen asset、检索算法、排名、EC 和 UID 映射均可确定性审计；
- 不依赖外部模型服务，复跑结果稳定；
- 适合作为“已知反应精确命中守门层”，先于真正预测 fallback 运行。

### 5.3 C-exact 的缺点

- 6/6 来自目标反应本来就在冻结 Rhea 中，是查表成功，不是未知反应预测；
- 当目标反应不存在于 Rhea 时，C-exact 不会产生新反应；
- exact match 对结构表示、质子化和盐形式敏感；
- Rhea 命中后仍可能因 EC-null 或 Rhea→UniProt 空映射而无法形成酶池；
- 因而 C-exact 单独不能闭合黄老师要求的“相似性不 OK → 预测”分支。

### 5.4 C-generic：通用降解规则/SMARTS 模板

理论工作方式：

- 从文献、数据库或专家审核的降解反应抽取反应中心；
- 冻结 SMARTS/模板、适用结构域、方向、排除条件、来源和版本；
- 对库外底物应用规则生成候选完整反应；
- 通过结构、守恒、方向和 provenance 门后再进入下游。

当前实况：

```text
冻结规则资产:
  未建立
pilot:
  未运行
评分:
  未进行
status:
  NOT_READY
```

### 5.5 C-generic 的潜在优点和风险

潜在优点：

- 规则来源和适用域可以人工审阅，解释性通常强于 LLM；
- 一旦冻结，可离线、稳定、低成本运行；
- 对规则覆盖到的反应类型可设置明确的 fail-closed 边界。

主要风险：

- 前期需投入生物学专家时间构建、去重和审查规则；
- 覆盖率受规则库限制，对新颖转化容易漏检；
- 过宽 SMARTS 会产生大量假阳性，过窄则几乎退化成查表；
- 本轮完全没有实测成绩，不能用 C-exact 的 6/6 代替 C-generic 的能力。

### 5.6 如果刘老师选择 C，下一步实际意味着什么

选择 C 作为预测主路线，必须指向 C-generic，而不是把 C-exact 冒充预测器。下一步：

1. 先建立带 provenance、方向、适用域和排除条件的最小冻结规则资产；
2. 由生物学专家审查规则含义；
3. 再用新的 blind set 做 bounded rule pilot；
4. C-exact 可继续作为已知反应守门层，但其成绩不得计入 C-generic；
5. 规则资产和 blind pilot 通过且黄老师另行授权前，不接生产。

## 6. A/B/C 横向比较

| 维度 | A：当前 BioTransformer ENVMICRO | B：三个 LLM | C-exact | C-generic |
|---|---|---|---|---|
| 本轮是否真跑 | 是 | 是 | 是 | 否 |
| 是否生成新候选产物 | 是 | 是 | 否，只查冻结库 | 理论上是，未验证 |
| RDKit 产品/反应门 | 25/26 产品可解析 | 59/59 partial reaction 可解析 | 完整冻结反应可解析 | 未知 |
| 正式主要产物 Top-K | 不可评分 | 最佳模型 4/6、5/6、5/6 | 4/6、6/6、6/6 | 未评分 |
| 完整反应 | 无 | 无 | Top-5 6/6 | 未评分 |
| 可直接恢复 Rhea | 否 | 否 | 是 | 未验证 |
| 可形成非空 D4 pool | 否 | 否 | 4/6 | 未验证 |
| 真正库外能力 | 未证明 | 有生成可能，未闭合 | 无 | 可能有，未建立 |
| confidence | 无可用值 | 自报、未校准 | 检索分数，不是生物学概率 | 尚未定义 |
| 可复现性 | 受依赖冻结问题影响 | 受平台/版本影响 | 高 | 取决于规则资产 |
| 当前能否直接接生产 | 否 | 否 | 否，只能作守门层 | 否 |

## 7. 学生侧对正式 A/B/C 的建议

以下是学生侧建议，不是刘老师或黄老师已经同意：

```text
建议主路线:
  B

定位:
  下一阶段研究方向，不是 production 接入

理由:
  A 当前工具已经合同失败；
  C-exact 只能查回已知反应；
  C-generic 尚未建立；
  B 是本轮唯一表现出库外候选生成语义的路线。
```

无论主路线是否选 B，建议保留 C-exact 作为独立的已知反应守门层。守门层不是
fallback 预测器，不应占用 A/B/C 主路线的未知反应能力结论。

## 8. 刘老师只需勾选 A/B/C

请选择一项作为下一阶段主研究路线：

```text
[ ] A：继续专业工具路线
    含义:
      不接当前 BioTransformer v0.5；
      先换工具/闭合合同，再做新 blind pilot。

[ ] B：继续 LLM 路线（学生侧建议）
    含义:
      当前 product-only 不能进生产；
      下一步优先验证完整生化反应生成与严格校验。

[ ] C：继续规则库/降解模板路线
    含义:
      C-exact 只保留为已知反应守门；
      先建设并审查 C-generic 规则资产，再做新 blind pilot。
```

刘老师无需现场设计代码、prompt、SMARTS、相似度公式、confidence 映射或数据库路径。
勾选结果只确定下一步研究方向，仍须黄老师另行授权具体 pilot。

## 9. 文末附加：R1/R2 后续试验建议

### 9.1 身份和边界声明

本节的 R1/R2：

```text
提出方:
  学生侧/Codex 的后续工程建议
是否属于黄老师原始 A/B/C 选项:
  否
是否已经端到端探测:
  否
是否已经答案解锁或评分:
  否
是否已有命中率、Rhea、EC、酶池或排名成绩:
  否
是否构成实施授权:
  否
```

因此 R1/R2 只能在 A/B/C 主体之后作为“如果选择 B，可进一步验证什么”的建议，
不能替代刘老师对 A/B/C 的正式选择，也不能冒充本轮已完成结果。

### 9.2 R1：B product-only → 有方向的两侧 Rhea 相似桥接

建议流程：

```text
LLM 给出主要产物 P
  ↓
构造 S >> P
  ↓
本地只比较正向:
  S 对 reference reactants
  P 对 reference products
  ↓
桥接到冻结、完整、方向明确的 Rhea reference reaction
  ↓
Rhea -> EC -> UniProt -> D4 pool
```

其中 `S >> P` 仍是 partial/unbalanced Reaction SMILES，不是完整生化反应。建议只用
正向两侧相似度，例如：

```text
S_direct =
  sqrt(
    reactant_to_reactant_similarity^2
    + product_to_product_similarity^2
  ) / sqrt(2)
```

禁止用 `max(S_direct, S_reverse)` 将反向反应误作降解方向。只有桥接出的冻结完整
Rhea reference reaction 才能进入下游；无法桥接的真正库外反应继续 fail-closed。

R1 的定位是工程兼容性实验：它可能利用 B 提供的产物侧信息改善已知 Rhea 反应检索，
但不能解决真正库外完整反应预测。

### 9.3 R2：B 直接生成完整生化反应 blind pilot

建议流程：

```text
substrate
  ↓
LLM 输出完整 reactants >> products
  ↓
RDKit parse
  ↓
元素/原子守恒 + 形式电荷 + 方向 + 底物保留
  ↓
模型版本 + provenance + confidence 语义门
  ↓
合格候选才进入 Rhea/EC/酶池衔接测试
```

R2 最直接检验黄老师原始统一合同，并且理论上保留真正库外反应能力；风险是完整生化
方程生成难度更高，失败率可能显著高于 product-only。

### 9.4 学生侧对 R1/R2 的顺序建议

如果刘老师正式选择 B，学生侧建议：

```text
优先:
  R2
原因:
  它直接检验老师要求的完整 reaction contract 和真正预测 fallback。

附加:
  R1
原因:
  它可测试 product-side 信息是否能安全桥接已知 Rhea 反应，
  但不能替代 unknown full-reaction fallback。
```

如果项目阶段性目标被明确改成“优先安全找回已知 Rhea 反应，而不是验证库外反应”，
也可以经黄老师批准先做 R1；届时必须在合同中明确其能力上限。

## 10. 选择前后保持锁定

```text
[x] 当前没有任何一路被宣布 production ready
[x] 不修改 reaction_prediction_node
[x] 不用本轮已见 6 例冒充新的 blind set
[x] 不把 product hit 写成 full-reaction hit
[x] 不把 C-exact 写成未知反应泛化
[x] 不把 D4 非空池写成正确酶找回
[x] 不把 R1/R2 写成已完成或已评分
[x] 刘老师选择后仍等待黄老师授权具体下一步
```

## 11. 证据定位

已推送给黄老师的三路线结果入口：

```text
GitHub:
  https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/
  M3_P1_2_1_REACTION_PREDICTOR_ROUTE_ADJUDICATION_REQUEST_2026-07-26.md
commit:
  601d0d384825e4e0fca1e2790de37db7a664c96a
```

自包含证据包：

```text
https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/
2026-07-26_M3_P1_2_1_Reaction_Predictor_Route_Adjudication
```

本地正式目标评分审计：

```text
04_Local_Review_Audits/
ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_ANSWER_KEY_UNLOCK_AND_TARGET_SCORING_LOCAL_AUDIT_2026-07-26.md
```

本卡是对既有 A/B/C 证据的详细选择版，不修改已冻结原始输出、答案钥匙或评分结果。
