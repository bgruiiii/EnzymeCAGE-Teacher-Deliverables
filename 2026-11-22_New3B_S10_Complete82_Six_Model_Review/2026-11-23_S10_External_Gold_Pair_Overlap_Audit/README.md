# 11月23日新增任务：外测与S10训练正样本配对级重叠审计

**已完成。配对重叠为120/382（31.41%）、110/338（32.54%），超过预定20%分支。**

先读[给师姐的完整结果与采用说明](REPORT_FOR_SISTER.md)。按原约定改用[228步配对排除主表](PAPER_MAIN_S10_TRAIN_PAIR_EXCLUDED_228.tsv)，全量338/382保留在上一级作为补充；新表不是82条完整路径。更保守的精确序列别名口径为227步，敏感性结果一并提供。

反应级、配对级、正样本UID membership、原S7家族占比均按382/338两个视图、train/valid/test三个split分别量化。匹配与名单先冻结，再读既有六臂排名做离线复算，不重训、不重新评分、不改候选或Gold。

[六行重叠汇总](OVERLAP_SUMMARY_2VIEWS_3SPLITS.tsv) · [逐步证据](STEP_OVERLAP_382.tsv) · [Gold配对证据](GOLD_PAIR_MATCHES_2523.tsv) · [全部敏感性复算](SIX_ARM_FILTERED_RECOMPUTATION_60.tsv) · [独立核查](INDEPENDENT_CHECKS.json)
