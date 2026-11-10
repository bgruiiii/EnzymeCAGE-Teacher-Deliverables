# 从给定路径到酶与微生物信息

## 1. 输入与步骤身份

给定路径可有两种已存在的表达，不能混成同一个通用入口：

- **t6桥接输入**：`MultistepRouteInput`是有序SMILES节点链，带`route_id/source_tool/reaction_source/branch_id`。相邻节点构成反应边，拆为独立RT-ID。整条链只有一个可选branch_id，不能完整表达任意分支DAG。
- **评价资料解析**：`b1_run.step1`从特定参与行表按`(case_id,step_occurrence_id)`组装有向反应，保留分支／前后继／拓扑坐标。该历史输入有28列，代码硬绑定2473参与行和533步；它有拆步参考价值，但不是无需评价资料的通用解析器。

桥接只把首步底物与RT-ID下沉到图。已有09-15runner虽然遍历拆出步骤，但只给首步图内候选池，后续步传空池；**未据此确认全步骤自动检索／构池／评分**。这里展示现状，不为阅读交付补开发新调度器。

实际代码：[bridge schema](../code/depending_t6_prod/src/schemas/bridge.py)、[拆步与逐步回填](../code/depending_t6_prod/src/nodes/multi_step_bridge_node.py)、[评测拆步](../code/biosysmodb121_stages/b1_run.py)。

## 2. 保留不同反应表示

原始反应、检索表示、训练兼容模型表示是不同对象。检索前清洗可能中和电荷、去冗余和简化参与分子；模型表示按训练合同处理，不应拿简化检索串直接替代模型资产键。

有向键`canonical_directional`、反向键和无向归组键用于身份／归组；`model_key_sha256`关联模型反应资产。原始方向与分支要另保留，不能因检索采用同反向最大相似度就丢掉方向。

代码：[检索清洗与指纹依赖](../code/retrieval_engine/copied_old_pipeline.py)、[模型兼容清洗](../code/reaction_cleaning/build_pollutant298_training_compatible_reactions.py)。

## 3. 检索Top10反应组

`FixedIndex/retrieve`使用Morgan r=8分子指纹与Tanimoto、反应配对得分，取同向／交叉的`max(S1,S2)`。实际排序为`(-score,sha256(canonical_directional))`。并列算法的复现还依赖冻结`PYTHONHASHSEED`与候选枚举方式。

- `PRODUCTION_INCLUDE_EXACT`保留exact候选并赋1.0。
- `BENCHMARK_QUERY_EXCLUDED`排除代码定义的同向／无向等价候选。
- **1.0不是表示相同或完整化学同一的证据；非exact也可能满分，exact不保证rank1。**

`b2a_retrieve.main`按无向等价键折叠组，保留组内成员；Top10指反应组，不是10条反应—酶关联，也不是最多10个候选酶。组序继承排序规则。

代码：[固定引擎](../code/retrieval_engine/fixed_retrieval_engine.py)、[归组调用](../code/biosysmodb121_stages/b2a_retrieve.py)。原文件docstring中的exact必rank1说法不准确，正文代码未为整理而改写。

## 4. 展开关联酶，而非每组只取一条

`b2b_pool.main`遍历每个Top10组的全部成员反应，展开所有合格科学关联，按`sequence_sha256`形成去重候选集合；关联明细仍保留多个accession、来源和证据。相同序列多个UID不应误当多个独立生物学序列，也不应丢掉其不同宿主来源。

**普通展开本身没有总数上限。**CURRENT95的cap100／Gold受控池是评价合同；t6的B主/C回退及pool>100拒绝又是另一套集成池策略，不能通称一套“默认池化”。Gold连接／命中统计代码存在不意味着普通推荐需要Gold。

代码：[全关联展开](../code/biosysmodb121_stages/b2b_pool.py)、[t6池节点调用壳](../code/depending_t6_prod/src/nodes/enzyme_pool_node.py)。t6内部`enzyme_pool_builder.py`未带回，明确仅引用。

## 5. 资产查找、复用和离线补齐

模型需要的不只是UID：还需要全序列PLM、口袋残基PLM、GVP结构图，以及反应DRFP、分子构象／图和反应中心。按序列／反应键、维度和口袋节点对应关系查找。

已有资产按每模型的历史来源链复用；缺件进入离线构建与核验队列，不是推理时无条件联网生成，也不允许用零向量或别的蛋白替代。新生成资产要登记来源和版本。

代码：[历史反应复用](../code/current95_bundle_main/scripts/prepare_historical_reaction_reuse.py)、[资产账目](../code/current95_five_model/prep_sources/r3_master_ledger.py)、[EnzGFM特征链](../code/current95_five_model/scripts_node/enzgfm_chains.py)、[原特征生成器](../code/EnzymeCAGE-master/feature/main.py)。位置见[资产地图](ASSETS_ON_CHENYU.md)。

## 6. 反应—酶评分与集成

五模型使用两套forward入口、共用一个评价器；不是一个wrapper全部支持。每seed输出raw logit，集成先sigmoid一次，再等权平均五seed概率，按分数降序，同分按UID的SHA断序。这个分数未校准，不是实验催化成功概率。

当前比较链消费已冻结的候选池，不在11月那次forward里重新检索。原始全排名与Top-k指标分别保留；不能把固定池内的排序结果解释成开放检索全链成功率。

代码：[3B／两600M入口](../code/current95_five_model/prep_sources/r3_gf_unified.py)、[两EnzGFM入口](../code/current95_five_model/scripts_node/r4_gf_enzgfm.py)、[集成与指标](../code/current95_five_model/prep_sources/r2_ensemble_eval.py)。

## 7. 宿主映射、选菌与性状注释

酶UID到宿主采用reviewed来源证据，现场UniProt/KEGG查询与冻结UID表回退分开标记，失败明确UNRESOLVED。相同序列的多个生物来源不自动合成同一菌株。

t6静态节点顺序是：

```text
旧wrapper排序 → 可选LLM重排 → microbe
→ organism_selection → trait → synthesis
```

LLM重排是独立后处理，可透传回退，不是CURRENT95神经排序分数；其prompt也不是实验催化效率证据。选菌层在无LLM配置时fail-closed；trait在其后，只注释，不反馈排名／硬筛选。

C8 adapter直接读UID映射和MetaTraits本地lookup，逐source_signature注释F1–F15。BacDive是登记／保藏和离线来源链的一部分，不是这个adapter直接读取的第三张表。预测层存在但当前未激活。详见[宿主与性状](HOST_AND_TRAITS.md)。

## 8. 单步与路径汇总

排序侧有逐步全排名及受控路径覆盖统计；宿主侧按步骤身份聚合来源和覆盖，保留物种／菌株分辨率及观测／缺失状态。某步无酶不能借用别步酶补成“匹配成功”。

[t6路径汇总](../code/depending_t6_prod/src/utils/route_step_organism_aggregator.py)是已有组件，但没有把CURRENT95五模型全排名自动转换成t6 state并输出合并工件的现役胶水。两边输出字段的区别见[代码导航](CODE_MAP.md)与[状态说明](STATUS_AND_LIMITS.md)。
