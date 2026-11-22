# 查询现有性状，再按需预测：实际工具入口

优先查包内[C8基础索引](../data/traits/C8_METATRAITS_LOOKUP_INDEX.jsonl.gz)、[2478来源分层资料](../data/traits/TRAITS_2478_LAYERED.jsonl.gz)及已有预测。`standalone/enzyme_host_tool/traits_backends.py`和[旧查询适配器](reference_sources/depending_t6_prod/src/tools/trait_query.py)是已有消费者。来源键/TaxID和观测、预测、缺失分别保留，不将同物种参考升级为原菌株实测。

本机完整MetaTraits原表根为`/home/a/EnzymeCAGE/data/metatraits/`，包括`ncbi_species_summary_no_predictions.tsv.gz`、`ncbi_species_summary_all.tsv.gz`、`gtdb_species_summary_no_predictions.tsv.gz`、`NCBI2GTDB.tsv.gz`、`GTDB2NCBI.tsv.gz`。原数据库未重复上传；此次1100物种结果及145962条原始命中在[data/traits/local_species_lookup](../data/traits/local_species_lookup/)。实际[查询脚本](reference_sources/local_metatraits_lookup/query_local_metatraits.py)、[回读验证脚本](reference_sources/local_metatraits_lookup/verify_lookup_outputs.py)与C7映射原文件已附；这些是此次固定目标运行的源码快照，保留原路径，迁移时须改数据库/输入/输出及映射脚本位置，不能直接运行去覆盖旧查询。

仍缺且用户需要预测时，需明确目标菌/所需性状，准备工具适用的基因组/蛋白输入，在独立SCNET/porTraits环境运行。近期实际使用的[执行脚本集](reference_sources/portraits/)完整保留，入口包括[run_genomespot.sh](reference_sources/portraits/run_genomespot.sh)、[run_e2m.sh](reference_sources/portraits/run_e2m.sh)、[run_downstream.sh](reference_sources/portraits/run_downstream.sh)、[run_collate.sh](reference_sources/portraits/run_collate.sh)。

它们依赖Slurm、Apptainer、工具容器和模型数据库，读取[config.sh](reference_sources/portraits/config.sh)、目标索引及工作根；迁移时换成本次输入、全新输出根和真实资源路径，不直接重启旧412/DEHP批次。四工具为GenomeSPOT、MICROPHERRET、BacDiveAI、Traitar；BacDiveAI预测与BacDive保藏登记不同。脚本集是已用组件，不是一个下载后无需部署即可任意菌株全量预测的服务。

晨羽现有冻结资料根为`/usrdata/EnzymeCAGE_data/data/releases/20260915_microbial_traits_v1/`，`microbial_traits/base/`为已有库，`microbial_traits/predicted_trait_assets/`为预测补充。SCNET重型依赖及作业需在对应已配置环境运行；不声称晨羽默认具备SCNET全部容器。默认应用不内嵌重型系统，也不替所有未知微生物预测全部性状。main如何开放按需入口由黄老师决定。
