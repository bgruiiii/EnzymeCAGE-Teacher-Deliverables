# 基模参数初步验证：GLM同题high/low阶段反馈

> 2026-11-20更新：本目录保留11月19日历史阶段记录，20题只是当时提案，实际后来执行的是10题单档。最新完成范围、工程恢复、费用与Kimi未发状态请看[最新审阅报告](../2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/REPORT_TO_HUANG.md)。下文“最新方案建议”属于历史时点，不是当前执行授权。

2026-11-19。**[给黄老师的审阅版阶段报告](REPORT_TO_HUANG.md)**。

同一Token Plan通道glm-5.3、同一原题，实际body只差reasoning_effort：high思考131070、输出131072，length且无可用答卷；low思考982、输出4841，33.66秒完整schema有效。各一次、不同时刻，尚未评reaction质量，不是总体最优预算或非劣结论。

- [high/low核验表](GLM_HIGH_LOW_COMPARISON.tsv)
- [六模型任务进展](TASK_RESPONSE_STATUS.tsv)
- [四次生成调用费用口径](CALL_ACCOUNTING.tsv)
- [独立审计摘要](AUDIT_SUMMARY.json)
- [文件校验清单](SHA256SUMS)

累计4次生成POST及1次目录GET，无剩余许可；40题分层pilot和全量尚未启动。额度原因下的阶段安排，不是老师免除了40题要求。Token Plan实扣Credits/现金未返回，旧按量估算不当实扣。

最新方案建议：因可用额度不足，拟先采用20道共同题的探索性pilot，保持同题配对和预登记；统计把握度降低，不能等同40题验收。每配置仍各20次生成，实际参与档位和总调用上限需先明确。20题当前未执行，既有实测仍为4次。

只发布报告和白名单汇总，不发布Key、完整题面、Gold、原始答卷、思考文本、SSE或私人账本。公开表可核对数值与完成范围，不提供未公开原始流的独立重放能力。
