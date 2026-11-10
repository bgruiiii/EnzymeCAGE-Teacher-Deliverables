# 晨羽资产位置与版本

本仓库只带代码和索引说明，**没有数据库、序列池、权重或张量本体**。以下为已留存源码／manifest中的节点路径与身份，不是本次重新登录节点的可访问性检查。目录名、文件存在、历史SHA相同和当前runtime实际消费是不同事实。

## 1. 反应与反应—酶关联

历史检索底座根：

```text
/usrdata/EnzymeCAGE_data/workspaces/
enzymecage_pollutant_biodegradation_category_capacity_census_r0_20260920/01_funnel/
```

上面两行拼接为一个连续路径。关键文件：

| 文件 | 历史内容／键 | bytes／SHA |
|---|---|---|
| REACTION_MASTER_POOL.parquet | 29061反应；有向／反向／无向键与检索表示 | 9385310；f587356a9c06e3461a3b910d967f606d26518b33cea47ad877ccc663272976fd |
| ALL_SCIENTIFIC_PAIRS.parquet | 292582科学关联、174650不同序列的历史核心库；反应×序列及provenance | 52577470；b0c686748dc79ae81494502f9e5b0b5daea45653b847f2af32612e651ba6d46c |

对应[schema主表](../schemas/knowledge_base_reaction_master_pool.schema.tsv)和[关联表](../schemas/knowledge_base_all_scientific_pairs.schema.tsv)。消费代码为b2a/b2b；不能将另一阶段的TrEMBL千万级扩展关联数套到这两个冻结文件上。

10月EXTENDED曾登记增量overlay；本次节点回包未带其正文／生成执行目录，只有历史身份引用。这里不将它描述为已完整定位的统一新版数据库。训练集也不能直接等同整个检索库。

## 2. 排序器权重：精确到臂与seed

[CHECKPOINTS_25.tsv](../assets/CHECKPOINTS_25.tsv)给每个主checkpoint的完整节点路径、seed、既有bytes和完整SHA，作为精确索引。权重本体不在仓库，checksum来自历史冻结身份，不是本次加载重新计算。

主要根：

```text
# 第一版3B、第一版600M
/usrdata/EnzymeCAGE_data/EnzymeCAGE-master/HPC_Returned_Result_Summaries/
enzymecage_v1_20260714/{3b_ensemble,600m_ensemble}/seed_{seed}/best_model.pth

# 更新S10的600M、EnzGFM；根必须包含这个长训练run名
/usrdata/EnzymeCAGE_data/training_runs/
enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922/
10_full_training_enzgfm_then_esmc_continuation_r1_20260926/
{esmc600m,enzgfm650m}/seed_{seed}/best_model.pth

# EnzGFM E0，旧formal；目录含plus_brenda不表示E0加了BRENDA
/usrdata/EnzymeCAGE_data/training_runs/
enzymecage_enzgfm_old_formal_plus_brenda_20260928/
03_e0_e1_five_seed_training_20260929/E0/seed_{seed}/epoch_{epoch}.pth
```

每组路径内换行仅为排版，应拼接。E0的seed40–44选定epoch分别9/5/5/7/3，不要猜所有臂都叫best_model.pth；以上仅便览，**以25行精确表为准**。

## 3. 蛋白与反应特征

关键代码：[r3_paths.py](../code/current95_five_model/prep_sources/r3_paths.py)、[r3_consumer.py](../code/current95_five_model/prep_sources/r3_consumer.py)、[enzgfm_chains.py](../code/current95_five_model/scripts_node/enzgfm_chains.py)。链内先命中者优先，不能绕开模型配方任意混搭。

| 资产类别 | 已记录位置 | 用途／身份 |
|---|---|---|
| 旧600M global／pocket | `/usrdata/EnzymeCAGE_data/feature/protein/ESM-C_600M_baseline_1152_round1_20260708/` | 1152维历史定义；分protein_level与pocket_node_feature |
| corrected pocket | `/usrdata/EnzymeCAGE_data/feature/protein/esmc600m_corrected_pocket_107705_20260713/` | corrected残基索引与口袋特征；不是旧compact/BOS等价替换 |
| GVP flat | `/usrdata/EnzymeCAGE_data/feature/protein/gvp/gvp_protein_feature_flat.pt` | 结构图，与口袋节点逐行对应 |
| S10蛋白资产根 | `/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922/` | 下分03_gvp_assets、04_plm_assets、02_carrier_uid_and_pocket及loader routing |
| EnzGFM基础特征 | 上根`04_plm_assets/enzgfm/merged/` | global按序列键；pocket按UID，2048维 |
| R1补充特征 | 上根`s11_r1_self_included_four_model_20260927/assets/` | EnzGFM merged_main/supp/supp2等；模型各有优先级 |
| E0训练bundle | `enzgfm_chains.py`中的E0RUN／W2CODE及其p2_assets | 同UID训练整bundle优先；不是仅按名字选一个R1特征 |
| CURRENT95反应资产 | `/usrdata/EnzymeCAGE_data/workspaces/current95_ngpu32g_20261031/asset_repair_r3_20261101/output/materialize_{main,delta15}/merged/reaction/` | DRFP、反应中心、构象／分子图，按模型反应键绑定 |
| 当前比较批次overlay | `/usrdata/EnzymeCAGE_data/workspaces/current95_ngpu32g_20261031/five_model_complete_20261103/overlay/` | pocket/global/GVP救援；历史run资产，不是新的通用库 |

3B的实际materialized资产与A109门由其forward入口及路径模块记录；本包不另编一个未经证实的“全局3B唯一目录”。本包没有完整feature receipt／数值数组清单，不能据路径说明宣称所有来源值已逐体相等。

## 4. 蛋白基础模型：与排序器权重分开

| 编码器 | 记录位置／用途 |
|---|---|
| ESM-C 600M | `/usrdata/EnzymeCAGE_data/models/esmc_600m/`，仅特征抽取；历史权重SHA为8ef856e1a237ee3f995442df997a962e70057faadecf38fc0c8561bd3c2f4324 |
| EnzGFM 650M | `/usrdata/EnzymeCAGE_models/EnzGFM_650M_20260920/extracted/EnzGFM_650M`；历史权重SHA为6fe6e90e4ef83789d3d117da0fb20246d46bcab462473536b85cd78ea6a7cb9d |
| ESM-2 3B | 特征／模型消费身份已有记录；本次没有导出其唯一原始权重位置，保持未定位，不按默认HF缓存猜路径 |

ranker进程读取离线特征，不需要在每个训练batch重新加载或微调大型PLM。EnzGFM抽取环境与ranker环境分开，见[历史环境记录](../assets/ENVIRONMENTS.json)；依赖未全锁定，不是安装锁文件。

## 5. 宿主与性状release

记录的稳定release根：

```text
/usrdata/EnzymeCAGE_data/data/releases/20260915_microbial_traits_v1/
```

| 相对路径 | 内容／消费者 |
|---|---|
| enzyme_host_mapping/uid_to_source_keep_bacteria_fungi_archaea.csv | 168335行／26列；宿主回退、C8 adapter直接输入 |
| microbial_traits/base/C8_METATRAITS_LOOKUP_INDEX.jsonl | 37170条F1–F15槽位；adapter直接输入 |
| microbial_traits/base/C8_BACDIVE_AVAILABILITY_LOOKUP.csv | 登记／保藏分辨率；当前adapter非直接读取 |
| microbial_traits/base/C8_LOOKUP_SOURCE_UNIVERSE.csv | 来源集合索引，非实际观测性状数 |
| microbial_traits/predicted_trait_assets/ | 已冻结预测候选／合并资料，当前adapter未激活使用 |

UID表历史SHA：`7b92e8e625cb73f070c8e902687ea5bbdbf749f04a19828e550e3fe205684fe6`；MetaTraits lookup历史SHA：`d51a540db2f9798d65e25b46f22960ba29ae2d4b288be218c83c299f24f5d5af`，实码有固定身份门。

历史CURRENT链接记录指向上述release。t6也曾使用字节相同的08-20回包副本，后续有只读路径切换记录；**本次未核当前进程环境、软链或实际打开路径**，不把release存在直接写成“现网已切换”。

MetaTraits bulk记录根为`/usrdata/EnzymeCAGE_data/data/metatraits/incoming/metatraits_bulk_tsv_snapshot_20260818`。C8构建器还读取其历史依赖payload中的BacDive closure／代表菌株等；精确输入表达式在源码中，未把任何原始数据库行带回。
