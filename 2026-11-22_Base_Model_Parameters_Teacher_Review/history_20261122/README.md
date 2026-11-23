# 基模参数任务：统一交付资料

更新：2026年11月22日。本文件夹整合此前全部参数测试阶段；对外只需转发本文件夹链接。

**请先读 [给黄老师的统一报告及40题继续派发请示](REPORT_TO_HUANG.md)。** 报告含原任务逐项回应、全部测试结果、费用、未完成项及请老师裁定的问题。

目前结论：额度受限的阶段测试已收口，原40题完整多配置验收尚未完成。API额度限制与Kimi-K3 Token Plan通道阻塞已明确披露；未把失败或未发题算作科学零分，未继续扩量。

## 核查表格

| 材料 | 内容 |
|---|---|
| [原要求逐项对照](TEACHER_REQUIREMENT_RESPONSE.tsv) | 13项原要求、完成情况和剩余边界 |
| [10题配置](PILOT10_CONFIGURATION_6.tsv) | exact模型ID、通道、实际参数及搜索控制限制 |
| [10题模型汇总](PILOT10_ARM_SUMMARY_6.tsv) | 五线50份有效、Kimi10位未发；原始/恢复数分列 |
| [10题逐题状态与评分](PILOT10_CASE_RESULTS_60.tsv) | 60题位、实际attempt、命中分母、交付状态 |
| [早期GLM005 high/low](EARLY_GLM_HIGH_LOW_COMPARISON.tsv) | 同题请求仅effort不同；high顶满、low有效 |
| [双档原轮6对](PAIRED3_ORIGINAL_RESULTS_6.tsv) | 原14次中的主试验配对，unknown/格式失败保留 |
| [双档恢复后6对](PAIRED3_RECOVERED_RESULTS_6.tsv) | 不覆盖原轮；跨日、格式失败及high空答显式列出 |
| [GPT/Grok诊断](GPT_GROK_DIAGNOSTICS.tsv) | strict一次正向观察与8192总cap反例 |
| [分阶段费用](CALL_ACCOUNTING_BY_PHASE.tsv) | 4+53+14+4计数及分币种费用口径 |
| [75次逐attempt费用账](CALL_ACCOUNTING_75.tsv) | 观察费用、旧价参考、未知预留分别列示 |
| [8笔未知费用预留](UNKNOWN_COST_RESERVATIONS.tsv) | 原失败费用未知，不因恢复成功清零 |
| [Kimi通道说明](KIMI_TOKENPLAN_STATUS.md) | 支持范围、同型号阻塞及待老师确认安排 |
| [审计摘要](AUDIT_SUMMARY.json) | 数量核对、完成状态、不可外推的结论 |
| [校验清单](SHA256SUMS) | 本文件夹其余15份文件的SHA256 |

## 阅读边界

- schema有效不是科学正确，reaction命中不是完整路径正确率。10题单档、3题双档、协议诊断不混为一个质量分母。
- Qwen恢复后3对、GLM1对共同有效；样本少且参考reaction有地板效应，不作正式非劣或最小预算判断。
- LENGTH_EMPTY属于配置/交付失败，不是科学答错；没有因低分再采样。原失败、partial和恢复答卷均本地留存。
- CNY参考价、USD标价、套餐占用、现金和未知预留不能相加为“实际总支出”；Token Plan实扣Credits不可观测。
- 公开包只含审阅报告、结构化汇总与来源身份，不含Key、私有凭据路径、完整题面/Gold、原始答卷、思考文本或SSE。不能只凭公开汇总独立重放私有流。
- 旧阶段目录及错误的根目录单文件入口均由本文件夹替代；其他任务不动，原始证据与Git历史保留。
