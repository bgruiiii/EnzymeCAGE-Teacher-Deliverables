# 基模参数与输出预算：统一阶段交付

更新：2026-11-23。回应黄老师v2反馈的审阅交付包。本次新增内容统一放在 `2026-11-23_Base_Model_Parameters_V2_Followup` 文件夹；11月22日阶段目录保留原版本，今天只需转发本文件夹链接。

**先读 [给黄老师的统一反馈](REPORT_TO_HUANG.md)。** 本轮只收口现有证据，不新增调用、不修评分、不启动40题。

当前结论：Qwen新两题双档全部交付，低档合计少约17%总输出，但一题增加、一题减少，不能证明普遍省量或质量非劣；Kimi-K3在OpenCode Go完成两题max单档，原“所有渠道都不可用”的说法已不适用，但high与Moonshot直连仍未做。GLM high暂停可靠质量对照，Grok本入口不承诺硬总预算，这两项是范围受限裁定，不是机制修复验收。

| 文件 | 内容 |
|---|---|
| [统一报告](REPORT_TO_HUANG.md) | v2三项要求、结果、费用、限制与请老师裁定的问题 |
| [当前13项对照](TEACHER_REQUIREMENT_RESPONSE.tsv) | 不把未完成改成完成 |
| [Qwen新两题配对](QWEN_PAIRED2_RESULTS.tsv) | 4份新答卷，按题保留两档差异 |
| [Kimi正式两题](KIMI_FORMAL2_RESULTS.tsv) | 2份有效答卷，独立于Qwen及旧百炼Kimi |
| [当前83槽逐项账](CALL_ACCOUNTING_83_CURRENT.tsv) | 75旧槽+8新槽，不等于83个成功HTTP请求 |
| [当前分阶段账](CALL_ACCOUNTING_BY_PHASE_CURRENT.tsv) | 币种、参考价、已观察费用分别列 |
| [机器可读当前终态](CURRENT_FINAL_STATE.json) | 当前83槽、费用与验收状态的唯一顶层视图 |
| [8笔旧未知预留](UNKNOWN_COST_RESERVATIONS.tsv) | 原位继承，不因新答卷成功清零 |
| [Kimi补发追溯](KIMI_RECOVERY_TRACEABILITY.tsv) | 明示旧/新队列SHA不一致和授权时序限制 |
| [更正与边界](CORRECTIONS_AND_LIMITS.md) | 不倒签、不改旧commit，不夸大cap或科学结论 |
| [审计摘要](AUDIT_SUMMARY.json) | 原始流、schema、旧G3复核范围及保留项 |
| [11月22日历史包](history_20261122/README.md) | 原75槽、10题单档、3题双档和诊断原样留存；只代表旧时点 |
| [校验清单](SHA256SUMS) | 本候选目录全部其他常规文件SHA256 |

历史包中的“Kimi阻塞、累计75、请示是否开40题”等表述保留为当时记录；当前状态以本层统一报告和CURRENT_FINAL_STATE为准。正式40题目前按老师v2暂停，并非取消或通过验收。

本文件夹只含审阅汇总，不含Key、完整题面、Gold、答卷、思考或SSE。公开汇总不能独立重放私有原始流。额度余额、标价、套餐占用、参考CNY和cash不可混加为总支出。
