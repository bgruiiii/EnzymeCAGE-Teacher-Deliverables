# 代码导航

## 协作者可运行入口

| 步骤 | 文件／函数 | 输入 → 输出 |
|---|---|---|
| 命令入口 | [tools/likert_cli.py](../tools/likert_cli.py) | prepare / validate / merge / totals / run |
| 装配七维或指定维度 | [pipeline.py](../code/likert_eval/pipeline.py) `prepare` | 冻结prepared_item＋维度 → 请求body、身份与SHA |
| 返回校验与无歧义规范化 | [validation.py](../code/likert_eval/validation.py) `validate`、`normalize`、`normalize_response` | 实际输出＋请求 → 错误、复核标记、规范化映射 |
| 合并与复算 | [pipeline.py](../code/likert_eval/pipeline.py) `merge` | 全七维输出，或局部输出＋原七维 → 逐维结果＋原公式总分 |
| 明确授权的单请求调用 | [runner.py](../code/likert_eval/runner.py) `run` | 冻结请求＋本机配置 → 归档、账、验证结果 |

这层是相对路径移植适配，不把原环境路径伪装成在任意机器上可直接执行；源码来源和变动范围见[manifest](../provenance/SOURCE_MANIFEST.tsv)。

## 原实际全量实现

| 实现 | 代码位置 |
|---|---|
| 原题答／任务scope／矩阵、目标合同与装配 | [build_items.py](../code/runtime/v05_release/build_items.py) |
| S/F/M/U/H、证据限制、分带／上下界与KEY门 | [rules_03a.py](../code/runtime/v05_release/rules_03a.py) |
| 认可路径与KEY登记绑定 | [registry_03d.py](../code/runtime/v05_release/registry_03d.py) |
| 证明身份与支持范围 | [proofs_03a_r1.py](../code/runtime/v05_release/proofs_03a_r1.py) |
| 实际请求body和配置门 | [v05_request_builder.py](../code/runtime/v05_release/v05_request_builder.py) |
| 全量调度、缓存恢复、去重、原通信和canonical | [run_lib.py](../code/runtime/v05_release/run_lib.py) |
| SSE／usage／返回模型和中断处理 | [f2r12_transport.py](../code/runtime/f2/f2r12_transport.py) |
| 累计费用和unknown责任 | [f2r12_budget_ledger.py](../code/runtime/f2/f2r12_budget_ledger.py) |
| 断点身份、缓存、原通信档案 | [f2r12_cache_checkpoint.py](../code/runtime/f2/f2r12_cache_checkpoint.py) |
| 完整输出检查 | [release_validation.py](../code/runtime/v05_release/release_validation.py)和[pipeline目录](../code/runtime/pipeline/) |
| 独立共享总分公式 | [f2r12_common.py](../code/runtime/f2/f2r12_common.py) `totals_contract` |

## 已执行的补评与修复

| 工作 | 实际源码快照 |
|---|---|
| NE维度队列、单一评分出口及合并 | [ne_repair.py](../code/executed_workflows/ne_repair/ne_repair.py) |
| 旧全图范围改标参考，接入现成认可链 | [scoped_ne_repair.py](../code/executed_workflows/ne_repair/scoped_ne_repair.py) |
| 多key凭据层（不含真实key） | [s8_credentials.py](../code/executed_workflows/execution/s8_credentials.py) |
| 补评传输、账本与有限换key | [s8_scope_r1_run.py](../code/executed_workflows/execution/s8_scope_r1_run.py) |
| 并发执行版本 | [s8_scope_r1_par.py](../code/executed_workflows/execution/s8_scope_r1_par.py) |
| 旧付费响应离线格式恢复 | [recover_format.py](../code/executed_workflows/format_recovery/recover_format.py) |
| 针对具体缺口的评价侧证据冻结 | [prepare_supplement.py](../code/executed_workflows/evidence_supplement/prepare_supplement.py) |
| 保持原量表的定向补证评分和来源合并 | [score_with_evidence.py](../code/executed_workflows/evidence_supplement/score_with_evidence.py) |

原工作流包含任务固定路径、私有源定位和阶段常量，作用是保留真实实现证据；不要把它们全部改名拼成一份新的“原生产入口”。当前可运行核心与历史原件分目录标明。
