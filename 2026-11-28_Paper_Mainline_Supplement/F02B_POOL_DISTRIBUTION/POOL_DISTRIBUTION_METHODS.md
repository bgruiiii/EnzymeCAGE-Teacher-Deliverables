# F02b 候选池大小分布方法（一页）

任务：`PAPER_F02AB_CPU_20261126`。生成脚本：`compute_fig3_f02ab.py`（纯 stdlib CPU）。

## 去重与单位

- 步骤表 2292 行 = 382 个唯一 step × 6 个臂，**不是一个池一行、更不能把 2292 行当 2292 个池**。先做跨臂一致性核验（同一 step 六臂的 N/G 必须相同），382 步全部一致后才按 step 折叠为 382 行（`CROSS_ARM_POOL_CONSISTENCY_382.tsv` → `POOL_SIZE_PER_STEP_382.tsv`）。
- N=该步候选关联总数（`n_candidates`），G=该步参考（Gold）关联总数（`n_reference`）。sum(N)、sum(G) 是**步骤关联总数**：同一条 UID 若在多个步骤出现会被重复计入，不能当 unique UID 数解读。
- 每步 N/G 与 FROZEN_R4 两列对账全 OK（见 `CROSS_ARM_POOL_CONSISTENCY_382.tsv` 第 9–11 列）。六臂共用同一 N/G 来源是既有共享冻结池结构；本卡只证明表间一致，引用既有共享池审计，未重新打开六套原始资产逐体验证成员集合。

## 视图与统计口径

四视图同 F02a（MAIN228 主口径、SUPP262 补充、FULL338/FULL382 full-set 补充）。每视图对 N、G 分别报告：count、min、Q05、Q25、median、Q75、Q95、max、mean、population_sd，另列 sum(N)、sum(G)（`POOL_SIZE_DISTRIBUTION_BY_VIEW.tsv`）。

- **分位数定义（唯一版本）**：排序后 h=(n-1)·p，在 h 两侧邻点线性插值（等价于 type-7 / `statistics.quantiles(method="inclusive")` 的推广）。全表只用这一套，不混用多套分位算法。
- population_sd 为总体标准差（除以 n），非样本标准差。

## 分桶与小池

`POOL_SIZE_BINS_BY_VIEW.tsv`：N 按不重叠区间 1–10、11–20、21–50、51–100、>100 分桶，count 与占视图步数的比例，空桶保留 0。

- N≤10 的步骤数及其视图比例在分布表 `steps_N_le10`/`share_N_le10` 列单列。这些小池步骤的随机 Hit@10=1（Top-10 已覆盖整池），是 Hit@10 解读时必须对照的结构性上限；它们**保留在分母中，不删除、不另选"大池子集"当新主结果**。
- 实测最大 N=100，>100 桶全视图为 0；与历史 CAP100 池上限一致，本轮按实际值报告，未做任何裁剪。
- 全部 382 步满足 N≥1、1≤G≤N，无 G=0/N=0/非整数输入异常；best_reference_rank 均在 1..N 且 hit 标记与 rank≤k 机械一致（核验见脚本 `load_steps`，测试 T1/T4）。

## 解读边界

本分布提供读图参照（池大小如何影响随机 Hit 期望），**不构成因果结论**：低 Hit 不能仅凭分布归因于候选池或参考覆盖不足，也不改变任何原始成绩、排名、掩码或分母。
