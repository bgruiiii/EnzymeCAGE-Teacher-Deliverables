# 五模型、训练与当前选型状态

## 1. 五组身份

| 实验臂ID | 编码器／维度 | ranker数据 | forward入口 |
|---|---|---|---|
| legacy_esm2_3b | ESM-2 3B／2560 | 旧formal | r3_gf_unified.py |
| legacy_esmc600m | ESM-C 600M／1152 | 旧formal | r3_gf_unified.py |
| new_esmc600m | ESM-C 600M／1152 | 更新S10 | r3_gf_unified.py |
| current_e0_enzgfm650m | EnzGFM 650M／2048 | 旧formal | r4_gf_enzgfm.py |
| new_enzgfm650m | EnzGFM 650M／2048 | 更新S10 | r4_gf_enzgfm.py |

每组seed40–44，共25个主checkpoint，其精确路径、字节和既有SHA在[CHECKPOINTS_25.tsv](../assets/CHECKPOINTS_25.tsv)。这份表从逐checkpoint身份表提取，不沿用早期资产概览中的粗略目录／疑似计数字节字段；本次没有加载／重哈希远端权重。

“3B原版v1”是**本项目早期训练版本**，不是作者原版权重。E0是实验组，S10是流程阶段，名字不代表先后优劣；E0实际训练时间晚于S10。

目前仅建议重点比较第一版3B与更新S10的EnzGFM，未作最终生产选择，不替协作者决定。保留五组入口，不删去表现较低的对照。

## 2. 相较作者框架的改动

沿用EnzymeCAGE几何增强反应—酶交互网络、结构/GVP、DRFP与反应中心等主体。更换蛋白PLM特征需同时适配全序列向量、口袋节点向量与投影维度，并核对残基／GVP对齐；新版加入`plm_model/plm_dim`配置。

本地保存作者代码支持ESM-2 650M及ESM-C 600M。我方增加3B和EnzGFM路线，并重建自己的训练数据。**PLM只离线提特征，正式训练的是下游ranker，不是对3B或EnzGFM基础模型全参数微调。**S10及E0从随机初始化训练ranker，无旧／pilot ranker warm start。

## 3. 数据与训练过程

| 数据 | train | valid | test | 合计 |
|---|---:|---:|---:|---:|
| 旧formal身份口径 | 623854 | 79563 | 70815 | 774232 |
| 更新S10 | 604539 | 75733 | 75556 | 755828 |

旧formal来自项目Rhea140/Swiss-Prot路线，S10在底座上引入Rhea142新增及BRENDA直接证据，重做序列科学键去重、训练carrier、资产筛选、负样本及反应家族分组。S10共112245正样本、643583负样本、5770有向反应。扩展检索库不等于直接训练数据，千万级同源候选未全部作为已验证正样本入训。

E0保留旧formal的UID、重复行、标签、负例和split；不是加入BRENDA后的E1。E1未因目录名出现而自动完成。S10两个臂共享行／split／carrier／主要训练设置，是较接近的编码器路线对照。

正式S10/E0：五seed、各20epoch、batch256、Adam、初始lr=3e-4、逐epoch乘0.95、BCEWithLogitsLoss；按validation macro reaction AUC选best。S10覆盖全部训练行，处理尾批；best固定之后才打开test，不按外部测试选seed或epoch。实际循环见[S10训练源码](../code/training/S10_TRAINER_SOURCE.py)。

作者原脚本也使用相同主要优化设置；不能说本项目另发明损失、换优化器或专门加大lr。训练数据、重复权重、负例、split、资产映射和输入特征同时变化，故不能把全部性能提升归因于数据量或PLM中的一个因素。

## 4. forward与特征路线

两个forward入口分别是[三臂入口](../code/current95_five_model/prep_sources/r3_gf_unified.py)和[两EnzGFM入口](../code/current95_five_model/scripts_node/r4_gf_enzgfm.py)。共同评价器[r2_ensemble_eval.py](../code/current95_five_model/prep_sources/r2_ensemble_eval.py)先对每seed raw logit做一次sigmoid，再等权平均五seed分数，全排名按分数降序、精确同分按UID SHA断序。

模型分数未校准。五seed指标平均不等于五seed概率集成；不得用当前外部测试拟合权重或挑seed。

3B、旧600M、新600M和两EnzGFM各有资产消费链。旧600M保留历史compact/BOS口袋定义，新600M采用corrected/biological索引；EnzGFM E0有同UID训练bundle优先，新EnzGFM有其R1补充链。它们不是随意替换任一向量都兼容。

## 5. 已有结果与解读边界

既有CURRENT95最终共同池为382步、16448候选关联、7468唯一UID；完整覆盖路径子集为82路径／338步。两套分母不得混用。这里仅摘已核的全382步结果，不提供真实参考标签或答卷：

| 模型 | Hit@1 | Hit@3 | 全排名MRR |
|---|---:|---:|---:|
| 3B-v1 | 91/382 | 176/382 | 0.397035 |
| 600M-v1 | 89/382 | 158/382 | 0.381673 |
| 600M-S10 | 90/382 | 177/382 | 0.399525 |
| EnzGFM-E0 | 77/382 | 178/382 | 0.376980 |
| EnzGFM-S10 | 94/382 | 204/382 | 0.418830 |

来源为2026-11-04本地最终独立审计，未在此包重跑。S10 EnzGFM有最高表内点估计，不等于显著性结论或对所有新任务的保证。

限制保留：旧600M有`NUMERIC_GATE_PENDING_REVIEW`；新600M救援批未满足原数值阈值，按影响量化与披露准入；EnzGFM有batch形状／padding敏感性与训练谱系DRFP差异披露。共同候选不等于所有特征值完全相同，不能签五模型所有数值门无条件通过。正常t6旧wrapper与本次五模型forward也不是同一个消费者。
