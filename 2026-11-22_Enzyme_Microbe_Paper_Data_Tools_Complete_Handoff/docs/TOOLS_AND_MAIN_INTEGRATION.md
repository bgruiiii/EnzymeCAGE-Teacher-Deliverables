# 已备独立工具、补资产与main接入边界

独立实现位于[tools/standalone](../tools/standalone/)，公共API是`predict_reaction`、`predict_steps`，CLI为`python -m enzyme_host_tool predict`或`predict-steps`。完整步骤列表用法见[工具说明](../tools/README.md)。predict_steps接已拆步骤，逐步保留状态、候选、全分数、来源与性状，不借用其他步骤的酶。

已有[路径拆步组件](../tools/reference_sources/depending_t6_prod/src/nodes/multi_step_bridge_node.py)处理有序相邻SMILES节点并生成步骤ID；它不是任意DAG推断器。模型评分必须用原目标步骤，不能改成检索Top1反应。

资产先查已存在的CURRENT95任务资产/UID映射，相关[build_3b_index](../tools/reference_sources/current95_five_model/prep_scripts/recovery_helpers.py)与[扩展索引](../tools/reference_sources/current95_five_model/historical_a109/c95_asset_index_ext.py)已备。确有真缺口时，已有[T3B反应生成器](../tools/reference_sources/t3b_asset_generator/run_reaction_asset_v1.py)和[运行合同](../tools/reference_sources/t3b_asset_generator/T3B_GENERATOR_RUNTIME_CONTRACT.json)，以及[结构/蛋白/GVP生成路线](../tools/reference_sources/protein_asset_lanes/)。旧真实补建成功不等于任何新酶都保证成功，失败状态须保留。

新增R4已有资产接入已经完成并采用：[关键复核与原始回执](R4_REAL_SCORING_REVIEW.md)。固定S02=13/13、正确S03=31/31候选全部真实评分，5seed共220个概率值，直接平均一次、全分数/排序/Top10前缀均已核，零丢弃。使用build_3b_index→C95AssetIndex→merged配置/任务UID映射，无需生成这些已有资产。旧v1的18/31描述仅保留为历史索引边界。此前R0 parquet检索和完整C8读取已分别实测；本次新增验收是两个固定池评分，不把分项验证写成同一次新端到端验收。真缺件的自动补建→校验→增量加载保持按需，未接默认分支；main没有合并或部署。

我们没有权限直接改depending main，未合并或部署。请黄老师决定是否采用独立工具、上游路径在哪个入口接、选用模型与资产根、如何部署。性状先查本地2478库/已有预测，仍缺且用户需要才独立预测，不把重型系统默认打入主应用。工程反馈见[给黄老师的说明](../maintainer/REPLY_TO_HUANG.md)。
