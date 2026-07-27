# M3-P1-2.1 反应预测器 A-first 三工具评测生物学决定记录

日期：2026-07-27  
决定来源：生物学侧会议结论（师姐建议，经项目侧确认）  
对应前置材料：`M3_P1_2_1_REACTION_PREDICTOR_BIOLOGICAL_ROUTE_SELECTION_CARD_2026-07-26.md`  
状态：**A-FIRST RESEARCH STRATEGY SELECTED / THREE-TOOL BENCHMARK REQUIRED / PRODUCTION LOCKED**

## 1. 决定

下一阶段采用黄老师 2026-07-24 清单中的 **A 路线（专业反应预测工具）作为优先研究路线**，
但不在尚无充分比较证据时指定单一工具。

先在同一冻结合同下比较三个工具：

1. 弓师兄正在开发的模型；
2. BioTransformer 3.0–ENVMICRO；
3. enviFormer。

先在项目现有统一测试集上做可比性测试，再用能够证明或严格标记训练暴露状态的外部数据
做泛化测试。比较结束后才选择 A 路线内部的最终工具。

如果三个工具均不能满足项目最低合同，再转入 C 路线，考虑建设带 provenance 的自有
降解数据库、规则或模板资产。

当前不选择 B 路线作为主路线。此前 LLM product-only 小试保留为历史 baseline，不删除，
但不作为这次三工具评测对象。

## 2. 三个工具的当前状态

### 2.1 弓师兄模型

```text
性质:
  组内正在开发的模型

当前已知:
  尚未取得冻结版本、调用入口、依赖、训练数据范围和输出合同

当前状态:
  WAITING_TOOL_HANDOFF / NOT YET BENCHMARKED
```

正式进入比较前必须冻结版本、代码/权重身份、训练数据边界、输入输出和 provenance。

### 2.2 BioTransformer 3.0–ENVMICRO

```text
既有实测:
  已完成 2026-07-24 小试

既有结果:
  25/26 个返回产物可被 RDKit 解析
  未返回满足旧统一合同的完整 reaction_smiles
  无合法 rank 和可用 confidence

既有结论:
  NOT_SCOREABLE_CONTRACT_INCOMPATIBLE
```

该结论表示旧合同下不能直接接入，不表示 BioTransformer 已经最好，也不表示它不能参加
新的“主要底物—主要产物”兼容性比较。新的比较必须与正在进行的 EnzymeCAGE
FULL_FORMAL vs MAJOR_PAIR 成对消融结果衔接，不能提前假设 product-only 输入对酶排序无影响。

### 2.3 enviFormer

论文与软件身份：

```text
title:
  Predictive modeling of biodegradation pathways using transformer architectures

journal:
  Journal of Cheminformatics

year / volume / article:
  2025 / 17 / 21

DOI:
  10.1186/s13321-025-00969-7

software reference reported by the paper:
  EnviFormer v1.0.1
  Zenodo DOI 10.5281/zenodo.13858575
```

论文元数据已于 2026-07-27 通过 Crossref DOI 记录核对。当前项目侧仍在做安装、可调用性和
输出技术验证，因此准确状态为：

```text
PAPER IDENTITY VERIFIED
TOOL VALIDATION IN PROGRESS
NO PROJECT BENCHMARK RESULT YET
```

不得把论文报告结果或工具可用性自动写成本项目测试通过。

## 3. 统一比较合同

三个工具必须使用同一输入集合、同一答案冻结方式和同一评分器。至少比较：

```text
input:
  substrate_smiles

raw output:
  原工具输出原样保存

normalized output:
  predicted product(s)
  rank
  raw score / confidence（若工具提供）
  score semantics
  tool name and exact version
  model/checkpoint identity
  provenance

technical gates:
  RDKit parse
  atom-map handling disclosed
  duplicate/canonicalization policy frozen
  invalid input fail-closed
  deterministic or seed/repeat behavior disclosed

prediction metrics:
  major-product Top-1 / Top-3 / Top-5
  valid-output rate
  no-output / invalid-output rate
  runtime and failure mode

downstream compatibility:
  能否构造项目允许的反应表示
  能否进入 EnzymeCAGE 候选酶流程
  若只能给主要产物，必须引用 FULL_FORMAL vs MAJOR_PAIR 消融结果
```

工具自报 confidence 不得直接解释成跨工具可比较的生物学概率；未经校准时只在各自工具
内部展示。

## 4. 两级测试集

### 4.1 现有统一测试集

现有 6 个有效底物可用于：

- 回归检查；
- 接口兼容性；
- 与 2026-07-26 A/B/C 小试对照；
- 评分器和 validator 调试。

这 6 个案例答案已经解锁，后续不得再称为新 blind set。

### 4.2 模型未见外部数据

外部泛化集必须在答案解锁前冻结，并逐工具记录训练暴露判断：

```text
CONFIRMED_UNSEEN:
  有训练数据清单/时间边界支持，且完成结构与反应去重

LIKELY_UNSEEN:
  数据发布时间晚于冻结训练截止时间，但无法取得完整训练清单

EXPOSURE_UNKNOWN:
  无法证明模型是否见过
```

只有 `CONFIRMED_UNSEEN` 可以无保留地称为“模型未见数据”。`LIKELY_UNSEEN` 和
`EXPOSURE_UNKNOWN` 必须单独报告，不能混入未见集成绩。

外部集还应：

- 优先选择数据库尚未纳入或论文新近报告、具有直接结构和产物证据的降解反应；
- 对各工具训练库做 canonical substrate/product/reaction 去重；
- 保留论文、数据库版本、发布日期、结构标准化和排除日志；
- 在预测完成前锁住答案；
- 不用当前 6 例重复充当 blind evidence。

## 5. 选择门

三工具比较后，只有同时满足以下最低条件的工具才可进入下一轮候选：

1. 可重复调用，版本和依赖可冻结；
2. 对合法输入有可审计输出，对非法输入 fail-closed；
3. 输出可经 RDKit 和冻结 validator 处理；
4. 在现有集和外部集分别报告结果，不混淆训练暴露；
5. 能与 EnzymeCAGE 所需反应表示建立经消融支持的接口；
6. 保存 raw output、标准化结果、版本、运行日志和 provenance；
7. 不以论文成绩代替本项目实测。

最终工具的选择依据和阈值在正式 benchmark 合同中冻结；本记录不虚构尚未讨论的数值
胜出阈值。

## 6. C 路线的触发条件和边界

C 路线是 A 三工具均不满足最低合同时的后备研究路线，不是当前已经实施的路线。

如果触发 C：

- 先建立数据库/规则资产的来源、版本、许可、结构标准化、适用域和排除条件；
- C-exact 只作为已知 Rhea 反应守门，不冒充未知反应预测；
- 新建 C-generic 规则/模板后再用独立 blind set 测试；
- 不把现有 C-exact 6/6 查回成绩计作 C-generic 泛化能力。

## 7. 授权边界

本决定确定研究和比较顺序，但不自动授权：

```text
production reaction_prediction_node mutation:
  no

EnzymeCAGE production integration:
  no

C database/rule asset construction:
  no

formal new blind benchmark:
  pending Huang-teacher scope confirmation
```

当前正在进行的 enviFormer 工作只可表述为技术验证；在正式合同、冻结测试集和独立审计
形成前，不宣称完成三工具比较。

## 8. 给黄老师的准确表述

> 生物学侧确定下一阶段优先走 A 路线，但不预先指定单一工具。拟在统一合同下比较弓师兄
> 模型、BioTransformer 3.0–ENVMICRO 和 enviFormer，并增加能够披露训练暴露状态的外部
> 泛化集；比较后再择优。enviFormer 当前仍在技术验证，弓师兄模型尚待交接，BioTransformer
> 只有既有 product-only 小试结果。若三个工具均不能满足最低合同，再考虑 C 路线自建
> 数据库/规则资产。该决定不等于生产接入授权。

