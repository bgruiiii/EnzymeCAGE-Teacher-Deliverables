# 工具阅读与调用入口

`standalone/`为已采用R4独立工具源码（继承R3，新增原生CURRENT95资产后端），`enzyme_host_tool.predict`导出单步与步骤列表API。`reference_sources/`为既有拆步、资产复用和生成路线的原文件快照，保留科学逻辑及旧路径；有些批脚本顶层会执行，不应为了阅读直接import。

配置需提供：反应检索parquet路径；wrapper代码根、EnzymeCAGE源码根和v1权重包；来源宽表；C8基础索引及指定预测包。R4后端`enzyme_cage_wrapper_native_c95`还需任务merged配置和UID映射；[原生配置示例](standalone/config_examples/tool_config_chenyu_native_c95.json)按实际成功worker整理，main context路径已经给出，sources/traits仍需按解压位置填写。本仓库压缩数据先解压后填实际路径，不把其它机器的绝对路径当成本地可用。

```bash
PYTHONPATH=tools/standalone python -m enzyme_host_tool predict-steps \
  --in tools/standalone/examples/pathway_example.json \
  --config /ABS/PATH/runtime_config.json --out /ABS/PATH/result.json
```

`pathway_example.json`为步骤输入示例；实际配置和模型资产由运行环境提供。本页展示入口，不是已经在任意新环境部署成功的承诺。原依赖/来源摘要保留于[ORIGINAL_PROVENANCE.tsv](standalone/ORIGINAL_PROVENANCE.tsv)。

T3B反应入口：

```bash
/usrdata/EnzymeCAGE_envs/enzymecage_t3b_generator_v1_20260911/bin/python \
  /usrdata/EnzymeCAGE_data/tools/t3b_reaction_asset_generator_v1_20260911/run_reaction_asset_v1.py \
  --reaction-task-json /ABS/PATH/reaction_task.json \
  --output-root /ABS/PATH/fresh_output --mode full
```

任务JSON需reaction_task_id/reaction_smiles/depth/evidence_hash/source_record_id。酶生成路线需对应序列/结构/口袋/当前任务context，参照原代码而不是直接重启旧批次；既有资产优先复用，结果输出任务增量再核验。自动串接状态见[工具与main说明](../docs/TOOLS_AND_MAIN_INTEGRATION.md)。

上游代码原文条款保留于[原文目录](../references/original_terms/)，本包不新增统一许可或声称重授权。
