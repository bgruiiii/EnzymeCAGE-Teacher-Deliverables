# F02a 随机基线方法（一页）

任务：`PAPER_F02AB_CPU_20261126`。生成脚本：`compute_fig3_f02ab.py`（纯 stdlib CPU，零模型调用、零网络、零随机模拟）。

## 设定

- **条件固定候选池**：每个已评步骤（step_occurrence）有一个冻结候选池，大小 N=该步评分候选数（`n_candidates`），其中 G=已登记参考成员数（`n_reference`，即候选池内保留的参考/Gold 成员）。N、G 直接取自冻结步骤表 `SIX_MODEL_STEP_RESULTS_2292.tsv`，并逐步与 `STEP_STATUS_411_FORMAL_R4_readonly.tsv` 的 `r4_n_retained`/`r4_n_gold_retained` 对账一致；同一 step 六个臂共用同一步骤池（跨臂 N/G 全 382 步一致，见 `CROSS_ARM_POOL_CONSISTENCY_382.tsv`）。
- N 是**该冻结步骤的评分候选数**，G 是**候选池中保留的参考成员数**。二者都不是全数据库潜在催化酶总数，也不是物种数；G 非穷尽（参考集合只是可催化该反应的已登记成员），基线因此是"条件于该池"的随机参照。
- 随机机制：对 N 个候选均匀随机全排列（不放回），取前 k' = min(k, N) 个，指标与真实评测同为"Top-k 内**至少一个**参考命中"（Hit@1/Hit@10），不是召回 G 个参考的比例。

## 解析期望（精确、无模拟误差）

```text
E[Hit@1] = G / N
E[Hit@k] = 1 - C(N-G, k') / C(N, k')，  k' = min(k, N)
当 k' > N-G 时未命中概率为 0，E[Hit@k] = 1（鸽笼必然命中）。
```

用 `math.comb` + `Fraction` 精确计算，另用"不放回未命中概率连乘"作第二实现对全部 382 步交叉核对，两法逐位相等（见 CHECKS/测试 T5）。不对所有步骤套 1/N 或 10/N；G>1 用组合式；N≤10 且 G≥1 时随机 Hit@10 恒为 1。

## 视图与汇总口径

四视图键集合直接取自冻结对象（`FROZEN_VIEWS.json`）：MAIN228（主，228 步/76 路径，`STEP_MASKS_FROZEN.json[COMPLETE82_STEP338][PRIMARY_DROP_TRAIN_GOLD_UID_PAIR].kept`）、SUPP262（补，262 步/88 路径）、FULL338（in_complete82=True 全 338 步/82 路径）、FULL382（全部 382 步/95 路径）。

- **step-macro**：先逐步算精确期望，再对视图内步骤**等权平均**（`RANDOM_BASELINE_BY_VIEW.tsv`）。不把全部候选拼成一个大池，不用平均 N、平均 G 代公式，不按候选数加权。
- 单位：`*_prop` 列为 0–1 比例；`*_pct` 列为同一数值×100 的百分数，全表统一此口径。
- `OBSERVED_VS_RANDOM_BY_VIEW.tsv` 给出四视图×六臂的观察值（由现有 hit 列直接等权聚合，MAIN228/SUPP262 已逐步核对与 `FIG3B_ABSOLUTE_PERFORMANCE_CI.tsv` 点估计一致）、同一随机期望、以及绝对百分点差。**六臂共用同一随机基线**，这是共享步骤池的结构，不是六个独立池。

## 解读边界

- 解析期望是参照值，不是统计显著性检验；本表不为基线虚构 95% CI。
- observed 高于 chance 只描述排序相对随机参照的位置，不构成泛化能力或生化有效性的证明。
- 路径层"全部步骤同中率"不在本卡范围。
