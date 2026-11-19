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

## 五、额度受限下拟先缩为20题探索性pilot

目前可用API额度不足以支持原40题多配置矩阵，**我们拟先将下一阶段共同题集从40题缩为20题，以控制用量，作为探索性pilot**。这是执行方提出的样本量调整，不是您的原40题要求已获豁免，也不是已经执行完20题。本次high/low单题结果仍只是前置验证。

拟保留原121题域，以及按步数和旧思考长度分层、同题配对、预登记抽样/参数/统计定义的原则，不看新成绩后挑题，也不简单截取原40题清单前20行。20题难以均匀填满所有交叉层，实际分配与未覆盖范围将提前公开，不假装分层代表性与40题相同。

**20题不是合计20次调用。** 每个参与模型/参数配置各回答同一套20题；例如同一模型low/high两档就是40次生成。相同档位数量下，题目相关调用数由40×K降为20×K，但实际token/Credits消耗不保证恰好减半。参与哪些档位、可合法复用哪些相同配置结果及累计调用/用量上限，仍需先列清，不能把“缩到20题”理解成自动开放六模型全部档位。

缩样本的限制将明确报告：

- 20题的统计精度和检验把握度低于40题，更容易得到宽区间；bootstrap10000次不能弥补样本信息不足。
- 如果开展配对统计，仍报告您原定的reaction质量指标、95%CI及−5个百分点界限，不因样本变少而放宽阈值。区间不能满足条件就写“证据不足”，不能据此宣称非劣或选定最小预算。
- 即使20题全部完整返回，也只证明本20题样本完成率100%，不保证121题或其它题均能成功，更不单独证明科学正确。
- 不直接将20题探索结果等同于原40题正式验收；后续如额度恢复，可按预登记扩展规则增加未测题，同时保留20题阶段结果，不事后择优。

后续先完成必要字段支持核对，GLM low列为继续验证候选，不直接替换主表；再在明确配置范围和用量上限后开展20题。希望先以这一受额度约束的缩减方案向您说明，并请您确认后续验证优先级。

**截至本报告更新，20题和40题均未发起，仍只有前述4次生成。** 未启动121题重采，没有更改原题、原Gold或旧成绩。

## 六、在线核查材料

所有下列链接均可在GitHub直接打开，不依赖本机路径：

- [同题high/low逐项对照](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/GLM_HIGH_LOW_COMPARISON.tsv)
- [六模型任务进展](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/TASK_RESPONSE_STATUS.tsv)
- [四次调用费用口径](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/CALL_ACCOUNTING.tsv)
- [独立审计摘要](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/AUDIT_SUMMARY.json)
- [本次交付说明](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/README.md)
- [文件校验清单](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-19_BIOSYSMODB121_Parameter_Early_Stage_High_Low/SHA256SUMS)

本次公开材料不含密钥、完整题面、原始答卷、思考文本、SSE或私有账本；它们仍在本地封存。公开表用于核对本报告的数值、版本和完成范围，不冒称可仅凭汇总表重放全部原始流。
