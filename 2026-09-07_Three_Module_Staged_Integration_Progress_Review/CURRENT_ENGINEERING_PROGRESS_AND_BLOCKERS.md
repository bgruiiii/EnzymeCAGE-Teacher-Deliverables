# 当前工程进度、限制与下一步

日期：2026-09-07

## 1. 当前总体判断

目前完成的是“关键组件和staged接口证据”，还不是production完整智能体。按当前合同拆分，整体约完成
55%—60%；若不计尚未收到正式输入的T4，可继续推进到整链staged验收。

## 2. 已完成或已形成可用证据

| 工作项 | 当前状态 | 已完成内容 | 仍保留的边界 |
|---|---|---|---|
| 源码、环境、资产与安全冻结 | `PASS_WITH_LIMITATIONS` | 固定Git/运行环境/主要资产身份并建立不修改production的staged流程 | 部分历史sidecar与部署差异继续留账 |
| 既有M3三案例及完整反应输入回归 | `PASS_WITH_LIMITATIONS` | B-primary、C-fallback、召回失败三类行为；full-reaction输入；pool≤100；CPU入口与wrapper metadata | 仍为staged累计patch，未作production merge |
| 统一证据链schema | `PASS_WITH_LIMITATIONS` | route—reaction—enzyme—organism—trait结构、枚举、跨字段validator及负例 | 需在后续真实主图中逐模块落字段 |
| T2A资产恢复 | `PASS_WITH_LIMITATIONS` | 师兄仓库缺失generator bundle已补齐并核30/30，v3.2所需模板、规则、corpus、donor index、三个ranker身份固定 | v3.2只能先作evaluation candidate |
| T2B单SMILES adapter | `PASS_WITH_LIMITATIONS_READY_FOR_T2C` | 非固定池输入可fresh生成；输入/参数门；8资产身份门；cache恢复；parent/cycle；depth1冻结；真实depth2；CLI及来源/分数语义 | 高级访问审计工具有自递归；部分外置sidecar未收；不作科学准确率结论 |
| T5A性状输入与UID映射 | `PASS_WITH_LIMITATIONS` | 五类输入与17 UID→16 source映射；只读门、负例和validator | 30行/小样本只证明schema，不代表真实整链 |
| T5B性状adapter/node | `TECHNICAL_PASS_WITH_LIMITATIONS` | C8只读adapter、节点接线、host evidence source枚举 | validation receipt部分延期收件；未作production merge |
| T5C宿主跨步骤聚合合同 | `PASS_WITH_LIMITATIONS_CONTRACT_TRACK` | reaction_task顺序、supporting enzyme合并、trait precedence/conflict、真菌缺失fail-closed | 跨步骤为合同fixture；待T2/T3真实路线输入复验 |

## 3. 正在继续的工作

### T2C：预测结果接入LangGraph

当前真实代码的`reaction_prediction_node`仍是占位，而且检索无结果时的状态会使图直接结束。下一步将：

```text
修复M5空检索→prediction的路由；
显式选择depending evaluation backend；
调用已经通过技术门的v3.2单SMILES adapter；
把PredictedReaction无损转换并写入下游实际读取的candidate_reactions；
保留source_tag、source_tool、model_version、raw_score语义和evidence hash。
```

### T2D：多步路径拆步与回挂

T2C之后，把多步/分支路线按反应边拆成唯一`reaction_task_id`，逐步进入候选酶流程，再把结果准确回挂。某一步
无酶时必须保留`UNMATCHED_ENZYME`，不能借用其他步骤结果。

### T3：新预测反应进入EnzymeCAGE前的资产

预测反应通常不在冻结反应资产索引中。按老师此前裁定保留双轨：

```text
T3A 最近参考反应proxy：只作较低等级桥接证据；
T3B staged真实新反应资产：生成并验证DRFP、映射、反应中心及相关输入；
两者必须分字段，proxy不得冒充真实新反应资产。
```

### T6：5—10条真实小型整链smoke

在T2/T3/T5依赖闭合后，运行污染物→路线→单步反应→候选酶→EnzymeCAGE→宿主→性状→证据报告的真实小型
整链测试，届时才能判断G7整链门。

## 4. T4正式18条blind

截至本次阶段反馈，未定位到本轮T4所需的老师指定18条blind输入冻结包及其身份。我们没有擅自从历史数据中挑
18条替代，因为这会破坏与depending v3.2、ECLIPSE等路线的同输入、盲隔离和可复核性。

详细说明见[`T4_FORMAL_18_BLIND_INPUT_STATUS_AND_REQUEST.md`](T4_FORMAL_18_BLIND_INPUT_STATUS_AND_REQUEST.md)。

## 5. 模型角色保持不变

```text
已知parent/pathway：enviPath本地快照lookup优先；
未知parent盲预测：BioTransformer ENVMICRO仍为当前主基线；
ECLIPSE PREDEC：补充候选生成器；
depending v3.2：已具技术adapter，但在T4和老师复核前只作evaluation candidate。
```

## 6. 本次希望老师重点看什么

1. 11个概念角色的科学流程和I/O关系是否符合您的总体理解；
2. 工程上无需正好实现11个节点，实际应如何合并请老师判断；
3. T4正式18条输入应使用哪一份冻结包，或请老师提供唯一输入身份；
4. 其余T2C/T2D/T3/T6继续按现有合同推进即可，不需要等待本次阶段审阅结束。
