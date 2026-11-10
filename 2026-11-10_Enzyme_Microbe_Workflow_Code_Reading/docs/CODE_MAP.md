# 核心代码导航与输入输出

这里按工作流指向实际文件／符号。`code/`保留原快照子树；它们不是一个安装包，未补造缺失的模块。完整函数与行号由AST静态生成在[CODE_INDEX.tsv](../provenance/CODE_INDEX.tsv)，来源和字节身份见[SOURCE_MANIFEST.tsv](../provenance/SOURCE_MANIFEST.tsv)。

## 输入、清洗、检索、酶池

| 文件与入口 | 输入 → 输出 | 状态／阅读重点 |
|---|---|---|
| [bridge.py](../code/depending_t6_prod/src/schemas/bridge.py) `MultistepRouteInput` | 有序SMILES节点与来源 → 输入合同 | 一条链一个branch_id，不是逐步DAG |
| [multi_step_bridge_node.py](../code/depending_t6_prod/src/nodes/multi_step_bridge_node.py) `split_multistep_route`、`apply_step_enzyme_matches` | 相邻节点 → 逐步RT-ID；RT-ID→酶UID回填 | 有实码；单次图调用仅下沉首步 |
| [b1_run.py](../code/biosysmodb121_stages/b1_run.py) `step1` | 特定28列参与行表 → `step_queries.tsv` | 历史评价解析器，保留方向与分支；依赖Gold输入，非开放CLI |
| [清洗工具](../code/reaction_cleaning/build_pollutant298_training_compatible_reactions.py) | 原反应 → 训练兼容反应与状态 | 身份／表示层；不等于简化检索清洗 |
| [fixed_retrieval_engine.py](../code/retrieval_engine/fixed_retrieval_engine.py) `FixedIndex`、`retrieve` | 检索串＋索引 → `(canonical_directional,score)` | exact赋1.0但不优先；相似1.0不是身份 |
| [copied_old_pipeline.py](../code/retrieval_engine/copied_old_pipeline.py) | 分子／反应 → 指纹、配对相似度 | 实际import依赖；与上游retrieve.py字节不同，未在本轮重跑等价测试 |
| [b2a_retrieve.py](../code/biosysmodb121_stages/b2a_retrieve.py) `main` | 单步查询＋知识底座 → Top10反应组／成员 | 去同／反向组重复，不是10个酶 |
| [b2b_pool.py](../code/biosysmodb121_stages/b2b_pool.py) `main` | Top10组全部成员＋科学关联 → 序列池／provenance | 前段展开全部合格关联，后段才接Gold作评价 |
| [enzyme_pool_node.py](../code/depending_t6_prod/src/nodes/enzyme_pool_node.py) `enzyme_pool_node` | t6候选反应 → `enzyme_pool_final`及B/C来源 | 不等同b2b；内部builder源码仍仅引用 |

`b121_common.py/gates_authority.py`补齐了前述历史脚本的公共工具与冻结断言。文件开头或main的固定计数是特定运行合同，不是普通新输入必须满足的自然规律。

## 资产与模型计算

| 文件与入口 | 作用 | 不应误读为 |
|---|---|---|
| [b2c_assets.py](../code/biosysmodb121_stages/b2c_assets.py) | 查询候选与反应资产覆盖 | 运行时自动补资产 |
| [prepare_historical_reaction_reuse.py](../code/current95_bundle_main/scripts/prepare_historical_reaction_reuse.py) | 按模型反应键复用历史资产 | 检索相似即可通用复用 |
| [r3_master_ledger.py](../code/current95_five_model/prep_sources/r3_master_ledger.py)、[require_all_models_ready.py](../code/current95_five_model/prep_scripts/require_all_models_ready.py) | 账目／就绪门与模型交集 | 用评分挑选候选或科学效果证明 |
| [feature/main.py](../code/EnzymeCAGE-master/feature/main.py)及同目录生成器 | PLM、构象、中心、口袋／GVP的既有工具 | 阅读时应运行的安装／下载流程 |
| [extract_p2rank_pockets.py](../code/EnzymeCAGE-master/scripts/extract_p2rank_pockets.py) | P2Rank离线口袋提取 | 已替代全部历史口袋定义 |
| [extract_enzgfm_current95.py](../code/current95_five_model/prep_scripts/extract_enzgfm_current95.py) | 额外EnzGFM特征抽取 | ranker训练中微调EnzGFM基础模型 |
| [enzgfm_chains.py](../code/current95_five_model/scripts_node/enzgfm_chains.py) `R1Chains` | EnzGFM pocket/global/GVP查找与来源标记 | 各来源值完全相同 |
| [r3_consumer.py](../code/current95_five_model/prep_sources/r3_consumer.py) | 两600M等臂的资产消费适配 | 所有模型共享一套口袋定义 |
| [旧模型代码](../code/EnzymeCAGE-master/enzymecage/model.py)、[S8代码](../code/s8_loader_code/model.py) `EnzymeCAGE` | 几何增强反应—酶打分 | 两个SHA不同就一定是全新网络 |
| [r3_gf_unified.py](../code/current95_five_model/prep_sources/r3_gf_unified.py) | `--arm`选3B／旧600M／新600M forward | 通用五模型wrapper |
| [r4_gf_enzgfm.py](../code/current95_five_model/scripts_node/r4_gf_enzgfm.py) | 两个EnzGFM臂forward | t6已调用此入口 |
| [r2_ensemble_eval.py](../code/current95_five_model/prep_sources/r2_ensemble_eval.py) | logit→sigmoid→五seed均值→排名／指标 | 先平均logit，或先平均五份指标 |
| [S10_TRAINER_SOURCE.py](../code/training/S10_TRAINER_SOURCE.py) | 实际S10训练循环 | 可在本地立即运行的新训练CLI |

[run_scoring_all.sh](../code/current95_five_model/scripts_node/run_scoring_all.sh)展示历史五臂串行调用顺序，含节点绝对路径和本包未带的准入文件。只用于看调用关系，不是本仓库的启动脚本。

## 宿主、性状与汇总

| 文件与入口 | 输入 → 输出 | 主要边界 |
|---|---|---|
| [enzymecage_client.py](../code/depending_t6_prod/src/tools/enzymecage_client.py) `call_enzymecage` | reaction＋UID池 → t6 `RankedEnzyme` | 旧v1 wrapper协议；dry-run不算真实预测 |
| [wrapper/schema.py](../code/wrapper/schema.py)、[predictor.py](../code/wrapper/predictor.py) | 旧请求／响应及门面 | 历史接口，不覆盖CURRENT95五臂 |
| [microbe_recommender.py](../code/depending_t6_prod/src/tools/microbe_recommender.py) `map_enzyme_hosts`、`resolve_host_identity` | 酶UID → reviewed宿主证据或UNRESOLVED | live／冻结回退要分别标记 |
| [organism_aggregator.py](../code/depending_t6_prod/src/utils/organism_aggregator.py) `aggregate_organisms` | 酶来源记录 → 宿主候选 | 不把物种代表冒充精确菌株 |
| [organism_selection_node.py](../code/depending_t6_prod/src/nodes/organism_selection_node.py) | 宿主候选 → 选菌状态 | LLM硬依赖，无配置fail-closed；不依赖trait_score |
| [trait_query.py](../code/depending_t6_prod/src/tools/trait_query.py) `C8TraitAdapter.annotate` | 候选支持酶UID＋冻结索引 → 性状注释 | 不是`.query`；无在线trait API／硬筛／改排序 |
| [trait_filter_node.py](../code/depending_t6_prod/src/nodes/trait_filter_node.py) | 选菌后state → 注释和证据 | 名为filter，当前实现只注释 |
| [route_step_organism_aggregator.py](../code/depending_t6_prod/src/utils/route_step_organism_aggregator.py) `aggregate_route` | 逐步宿主性状 → 路径汇总 | 不提升来源分辨率，不补造缺失性状 |
| [evidence_synthesis_node.py](../code/depending_t6_prod/src/nodes/evidence_synthesis_node.py) | state证据 → 汇总报告 | 有代码不等于已经证实完整图连续执行 |
| [run_metatraits_c7_1_mapping.py](../code/metatraits_etl/run_metatraits_c7_1_mapping.py) | bulk字段 → F1–F15映射资料 | 历史离线整理，不是现场查询 |
| [run_c8_1_lookup_index.py](../code/c8_lookup_index_builder/run_c8_1_lookup_index.py) | 来源映射、MetaTraits与BacDive离线资料 → lookup | builder可以依赖BacDive，runtime adapter不等于直接读同一表 |

## 接口字段不要混用

CURRENT95的`RANKINGS_FULL.tsv.gz`实际列为：

```text
step_id, rank, runtime_uid, sequence_sha256, ensemble_prob_float64,
gold_flag, label_class, no_discrimination
```

`gold_flag/label_class`属于评价输出的标签连接；模型forward不应靠它们做推荐。仓库只保留字段定义，没有真实标签表。

t6则主要在`EnzymeCrewState`及Pydantic对象中传递`reaction_task_id/ranked_enzymes/organism_candidates/host_trait_annotations`等字段。`runtime_uid→uid`、CURRENT95 step_id→t6 RT-ID、候选／来源对象装配需要显式映射，**本快照不声称已有这一转换胶水**。概念上能对应，不等于代码已接通。
