# Likert V0.5评分实现与代码入口

本目录补充此前教师仓库缺少的**实际Likert评分实现**：任务／参考事实装配、程序范围与上限、评分模型调用、返回校验、断点与费用账、逐维补评、总分复算及来源留档。这里是评价侧代码，不是生成降解路径的模型，也不是程序五层化学命中评分器。

**先读[实际执行流程](docs/WORKFLOW.md)，再按[代码导航](docs/CODE_MAP.md)定位实现。** 可直接运行的移植入口是[tools/likert_cli.py](tools/likert_cli.py)；历史完整协议和最后补评源码均保留在[code/](code/)。原文件SHA、导出SHA和移植说明见[来源清单](provenance/SOURCE_MANIFEST.tsv)。

## 打开后看什么

| 需要核对 | 入口 |
|---|---|
| 程序判断、AI评分、后验校验谁先谁后 | [WORKFLOW.md](docs/WORKFLOW.md) |
| 哪个文件／函数实际做哪一步 | [CODE_MAP.md](docs/CODE_MAP.md) |
| 实际全量运行时，包括判范围、transport、budget、validator | [code/runtime/](code/runtime/) |
| 实跑批次、NE修复、认可主链接线及补证原实现 | [code/executed_workflows/](code/executed_workflows/) |
| 可运行的七维请求、局部补评、校验和复算入口 | [code/likert_eval/](code/likert_eval/)和[命令说明](docs/RUNNING.md) |
| 当前补评实际使用的完整科学规则 | [SYSTEM_RUBRIC_USED_S8.txt](rubric/SYSTEM_RUBRIC_USED_S8.txt) |
| 人工复核、HELD／NE和人类效度到底是什么状态 | [HUMAN_REVIEW_AND_LIMITS.md](docs/HUMAN_REVIEW_AND_LIMITS.md) |
| 无真实题目／Gold的可运行示例 | [examples/README.md](examples/README.md) |
| 此次整理实际检查了什么 | [audits/](audits/) |

## 三条本机离线命令

在本目录运行，Python 3.10及以上：

```bash
python3 tools/verify_package.py .
python3 -B -m unittest discover -s tests -v
python3 tools/likert_cli.py validate --request examples/synthetic_request.json --response examples/synthetic_response.json
```

以上均不调用API、不读密钥。示例明确为`SYNTHETIC`，不是实际科学结果。运行API需自行配置本机环境、真实冻结输入、当前服务／价格与预算，并显式开启配置和CLI两道调用确认；默认配置禁止付费。详见[RUNNING.md](docs/RUNNING.md)。

## 代码层次与使用边界

- `code/runtime/`保留实际全量运行的31个模块，包含严格完整输出协议及确定性事实／区间代码。复现历史整个批次还需要相同冻结数据、scope、accepted、证据和版本，不能只凭代码重新推定科学真值。
- `code/executed_workflows/`保存已执行工作流源码快照，保留原接口和历史路径。它们用于核对原调用关系，不能直接在未知机器上运行其中的历史批次入口。
- `code/likert_eval/`是此次为协作者制作的相对路径适配入口：完整七维或指定维度请求、实际S8验证函数与格式兼容、原F2总分公式、生产transport／账本／原通信留存。`prepared_item`要求上游已冻结事实和范围，不假装从原答案自动证明所有科学事实。该入口的离线验证通过，不冒称此次重新完成全量API实测。

本轮已有706个评分位置可计算总分、残余NE为0，来源为主批674＋另32份校准；这不是121题×6模型的无隔离统一分母。**人类独立外部效度尚不能据此宣称完成；0012范围复审标记仍保留。** 数量摘要见[LOCAL_RUN_SUMMARY.json](audits/LOCAL_RUN_SUMMARY.json)，非人类终审证据。

此处只上传源码、规则／协议、配置模板、合成示例和必要审查摘要。没有真实API key、私人配置、完整Gold、原始题面／答卷／SSE、账户信息、完整账本、权重或数据库。原始历史路径可能仍出现在源码快照中；可运行入口不依赖这些路径。此次未改变depending仓库，也未将离线评分描述成已接入其在线主图。权利与第三方依赖见[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
