# 致黄老师：基模生成参数试验阶段反馈

日期：2026年11月19日。**本报告是已核验的阶段反馈，不是参数优化最终结项。**

**在线报告：** https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/REPORT_TO_HUANG.md

黄老师您好：

按您11月18日关于生成参数与输出预算的回复，我们先复用原题与原调用记录，完成了Grok单题验证，以及GLM在同一Token Plan通道、同题下的high/low两次初步验证。现将实测和未完成事项分别汇报。

## 一、GLM单题对照：low完整返回，high耗尽输出预算

选择原121题中曾经长度失败的代表题 `BIOPATH150_005`。两次均使用百炼Token Plan Chat Completions、`model=glm-5.3`、`max_tokens=131072`、`temperature=0`及`response_format=json_object`。**实际发送body已逐字段核对，唯一差异是reasoning_effort=high/low，messages完全相同**，不只根据输入token数相同推断同题。

| 观察项 | high | low |
|---|---:|---:|
| 输入token | 5658 | 5658 |
| 思考token | 131070 | **982** |
| 总输出token | 131072 | **4841** |
| 终止原因 | length | **stop** |
| 正文字符 | 2 | **10627** |
| 结构结果 | LENGTH_EMPTY，无有效JSON | **完整返回、schema有效** |
| 记录耗时 | 759.538秒 | **33.660秒** |

原始SSE、保存正文、usage、请求身份及父账已独立核验。可以确认：**在这道失败代表题的各一次观察中，low得到了结构可用答卷，high没有得到。**

不能据此宣称low总体更优、所有题均能完成、已经找到最小预算，或符合您要求的质量非劣条件。本次尚未评价这份答案的逐题reaction命中率，schema有效不是科学正确。两次虽在请求层仅改effort，但为不同时刻、各一次采样，服务端权重/snapshot未独立核验。

Token Plan通道由项目执行方在原本机按量凭据被拒后选用，并非您的原回复指定。其ID为`glm-5.3`，旧按量正式答卷ID为`ZHIPU/GLM-5.3`；二者权重/版本等价性未独立证明，因此新通道单列，不与旧默认档结果混成仅改effort的对照。

## 二、对六模型要求的逐项进展

| 模型 | 已完成 | 尚未完成 |
|---|---|---|
| Grok-4.7 | 原Go Responses入口，原题仅将请求cap65536改为131072；完整返回，schema有效；实际输出72526 | 未触新边界，尚不能证明任意自定义cap映射或硬上限已充分验证 |
| GLM-5.3 | 原按量low一次401；随后Token Plan同题high/low各一次，结果见上表 | 多题完成率、质量配对与low/high/max三档pilot未做 |
| Qwen3.8-Max | 原请求、用量及建议字段映射已整理 | 新thinking_budget各档及max_completion_tokens在实际入口的调用验证未做 |
| DeepSeek-V4.1-Flash | 旧长度失败与原请求证据已复用 | effort=high及新总输出设置的实测未做 |
| Kimi-K3 | 原请求/总输出统计已复用，未返回的独立思考计数保持未知 | high/max新档位调用及质量对照未做 |
| GPT-5.6-Luna | 沿旧审计确认6份JSON语法错误、1份缺必填字段；7份第二答独立保留，不把它们归为长度失败 | strict/JSON Schema模式在原入口的支持与效果未新测；未加预算或重采 |

Grok本次耗时732.181秒，输出72526中reasoning67655，cap131072未触边界。原12笔超过旧65536请求值的provider usage继续披露，不能因本次成功而抹去。

GLM high的131072输出及length是本次触顶截断的证据；因请求值恰等于模型最大输出，尚未区分请求字段作用与服务端默认/固有上限，不据此宣布所有cap映射已验证。无需为这个措辞再制造超长输出。

旧按量请求含enable_search=false，新Token Plan请求未发送该字段，两次high/low沿同一策略，未观察到工具调用元数据。官方关于Responses内置工具的描述不构成Chat绝无内部搜索的保证，故内部搜索仍标未独立排除。通道与搜索差异随结果保留。

## 三、调用与费用

已完成**4次生成POST＋1次模型目录GET**，其中：

- 旧按量GLM low：401 invalid_api_key，无模型答卷，不是low思考效果证据；无usage，实际费用未知，保留原3.750016元预留。
- Grok：已核标价 **USD0.44854**、Go套餐消耗 **USD1.79416**、该响应cash=0。标价、套餐消耗和现金不是可相加的三笔支出。
- Token Plan GLM high/low：usage未返回Credits或账单字段，**实际套餐扣减和现金扣款不可由本地响应确定**。按旧按量8/28元每百万token推算约3.715280/0.180812元，仅为历史参考估计，不是本次实扣，不据此宣称low实际便宜多少。

四次调用都保留，失败未清零；授权4/4已用尽，没有重试或额外模型探针。当前全部新提交停止。

## 四、40题pilot尚未执行，不宣称已获豁免

您第六节要求的40题分层pilot、逐题reaction指标、paired bootstrap10000次、相对参考档95%CI下界>−5个百分点及完成率100%，**目前均未完成**。这是执行方基于可用额度先做有界单题验证的分阶段安排，不是您免除了这些要求，也没有把单题成功替代完整验收。

第八节“如果只能先改一件事”理解为优先级建议，不能解释为“只做小测试就算全部完成”。关于题面信息是否与系统输入对等的争议是另一项实验设计，本轮仅改生成配置，没有解决该争议。

## 五、后续建议，请您确认分阶段安排

1. 将GLM low作为值得继续验证的候选，暂不宣布其可直接替代主表配置；本题low没有出现>120k思考/空答，但不据此对整模型下结论或自动换5.2/删旧结果。
2. 先核实Qwen/Kimi/DeepSeek等关键字段在实际接口的支持，再在额度允许且范围明确后执行您要求的40题对照；不能先跑40题，再发现字段无效。
3. 若暂不能开展完整40题试验，则保留本阶段证据并明确报告未完成项，请您确认后续优先级，不将本轮写成最终预算选择或能力排名。

目前未启动40题、多配置矩阵或121题重采，也没有更改原题、原Gold及旧成绩。

## 六、在线核查材料

所有下列链接均可在GitHub直接打开，不依赖本机路径：

- [同题high/low逐项对照](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/GLM_HIGH_LOW_COMPARISON.tsv)
- [六模型任务进展](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/TASK_RESPONSE_STATUS.tsv)
- [四次调用费用口径](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/CALL_ACCOUNTING.tsv)
- [独立审计摘要](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/AUDIT_SUMMARY.json)
- [本次交付说明](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/README.md)
- [文件校验清单](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/SHA256SUMS)

本次公开材料不含密钥、完整题面、原始答卷、思考文本、SSE或私有账本；它们仍在本地封存。公开表用于核对本报告的数值、版本和完成范围，不冒称可仅凭汇总表重放全部原始流。
