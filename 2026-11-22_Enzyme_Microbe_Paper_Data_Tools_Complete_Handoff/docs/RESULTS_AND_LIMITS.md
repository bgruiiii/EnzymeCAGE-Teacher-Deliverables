# 原始成绩、复算与补测结论

三张主表均保持原字节：[逐候选排名](../data/ranking/STEP_CANDIDATE_RANKINGS.tsv.gz)、[五组汇总](../data/ranking/FIVE_MODEL_SUMMARY.tsv)、[五seed计算记录](../data/ranking/ENSEMBLE_PROBABILITY_TRACE.tsv.gz)。82240候选行=五臂×16448步骤关联，7468唯一UID；382主视图与338子集分开。原汇总可由明细复算，n_gold导出笔误曾窄修，分数/排名未改。

数值控制补测不是重训或全量重测：旧600M本卡100条repeat进入原1e-5门，历史失败保留；新600M219步换特征路线时171步仍超原0.05 logit差门，正式概率最大差约0.0149，70步有其它名次变化，Top1与Hit@1/3/5/10未变。两个EnzGFM保持原整步repeat名次稳定；拆批会改排名，新臂2步Top1改变，因此不擅自改批协议。不能用概率差较小或Top1未变改签原logit门通过。

wrapper实际调用model.evaluate，trace已是每seed概率，聚合直接求均值。旧回包误称logit并二次sigmoid的解释已纠正，见[修正表](../evidence/numeric/D3_CORRECTED_PROBABILITIES.tsv)。正确S03的旧固定v1调用18可用/13缺项留存，不称完整31排名；随后R4复用CURRENT95已有资产，S02全部13、S03全部31候选真实评分已通过[R4关键复核](R4_REAL_SCORING_REVIEW.md)，旧边界已在独立工具中解决。

CPU返修核对60UID公式、44行目标/候选身份、991替换记录和62份后验重建清单通过；映射表实际5421行。启动前收据/原响应CI/旧评估上下文未留全如实备注，后验重建不冒充运行时快照。此轮纠正分项接受，不再追历史细节。见[独立核查](../evidence/numeric/CPU_R1_INDEPENDENT_CHECKS.json)和[原独立概率复算](../evidence/numeric/INDEPENDENT_RECOMPUTATION.json)。

补测保存的全量逐seed控制向量、运行脚本和CPU返修原件见[两份原始回包](../evidence/raw_control_archives/)，历史错误文字原样保留，采用结论以上述独立复算和修正为准。详细原审计文字在[存档](../evidence/reviews/)。

本包不另造显著性结论；若使用另线已有路径级区间，必须采用其最新验收版本，不以五seed波动冒充总体区间。原numeric_quality_note随表保留。另线新3B/六模型不自动替换本包原五组。
