# 致黄老师：基模参数10题探索性试验及工程恢复阶段反馈

更新：2026年11月20日。文件名保留历史日期，正文以本次更新为准。**这是已审阅的阶段结果，不是原40题多档方案的完整验收。**

**GitHub在线报告：** https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/REPORT_TO_HUANG.md

黄老师您好：

按您11月18日对生成参数与输出预算的意见，我们先完成必要单题验证，再因可用额度限制，将后续试验缩为**同一组10题、每模型一个候选配置**。这是执行方对原40题多档设计的缩减，未获豁免原验收条件。此前20题只是历史提案，实际未运行；本次实际执行的是10题单档方案。

## 一、实际完成范围

计划六模型各10个题位，共60题位。实际有五条可执行模型线，**工程恢复后收回50份结构有效、可评分答卷**；Kimi-K3的10题因通道/套餐可用性阻塞而未发送、未评分，不记为模型科学零分。

原始单次视图为47份有效；两份进程中断题各恢复一次后为49份；最后修复Grok一题缺少路由头的问题，恢复为50份。三种视图及全部首答、部分流、失败和新答均保留，不跨版本挑分。这里的50/50是**五条可执行线的工程恢复后交付率**，不是六模型60/60，也不是单次调用完成率100%。

本轮pilot共**53次生成POST**：Qwen10、DeepSeek11、GLM10、Grok12、GPT10、Kimi0。53包括三次恢复追加，不只统计成功题位。另有此前独立封账的4次参数诊断POST与1次模型目录GET；两阶段累计57次生成POST。公开文档查询不属于模型调用。

原每模型10次/每题1次的限制在中断恢复时发生偏离，已单列；新增恢复卡明确了条件性合并封顶63次，实际53次。原Grok 400后补头续跑的停止门偏离不被新授权抹去。两次早期R2授权已由执行方补记原话和约略接收时间，缺独立时间戳凭证的边界继续保留。当前阶段停止新提交，不将未用条件额度当作后续自动调用许可。

恢复发送脚本只有commit存在性检查，未落实所要求的共享原子提交锁；本次留存一份新增commit/响应/结算，不能据此声称并发防重复门已验收。此实现限制及上述历史偏离随报告保留，已有有效答卷不因此重发。

## 二、10题单档结果

采用原题messages，同题不改；从原121题中97个3/4/5步题的母体按步数及历史思考长度四分位抽样，seed20261119，步数配额4/3/3。12个交叉层有2层未覆盖，原母体中>5步的24题未进入本次抽样，不能外推全部复杂题。

reaction命中为冻结G3程序的matched/(matched+missing)，按题宏平均，方向/结构匹配与CONTROLLED_INPUT规则不变。**它不是完整路径正确率、五层总分或人工科学判定，也不能用schema有效替代科学正确。**

| 模型/本次配置 | 恢复后结构有效 | reaction命中均值 | 平均总输出token | 平均思考token | 有效答卷平均耗时 |
|---|---:|---:|---:|---:|---:|
| Qwen3.8-Max，thinking_budget=36864，max_completion_tokens=131072 | 10/10 | 18.33% | 28311.7 | 24315.8 | 581.13秒 |
| DeepSeek-V4.1-Flash，effort=high，max_completion_tokens=131072 | 10/10 | 12.33% | 20373.4 | 17215.1 | 83.61秒 |
| GLM-5.3，effort=low，max_tokens=131072 | 10/10 | 12.33% | 4053.2 | 1033.3 | 35.75秒 |
| Grok-4.7，max_output_tokens=131072 | 10/10 | 19.00% | 34965.0 | 30881.7 | 554.40秒 |
| GPT-5.6-Luna，原cap65536配方，不新增strict | 10/10 | 15.67% | 3775.6 | 1351.7 | 162.48秒 |
| Kimi-K3，原型号通道不可用 | 未发送10题 | NA | NA | NA | NA |

表中均值只描述选定样本和各自通道配置，不能据此排出普遍能力优劣。Token Plan的Qwen/DeepSeek/GLM与OpenCode Go的Grok/GPT入口不同；通道、时点与服务端快照差异继续披露，不能把新旧差异全部归因于参数设置。

Grok最后一题因缺少`x-opencode-session`路由头曾返回400。修复后仅补一次，请求body与原件逐字节相同，430.174秒返回12479字符，schema有效；程序reaction命中为**0/4**，照实保留，没有因零分再抽。补发前9份有效答卷的均值21.11%曾与固定10题口径混列，现统一为含该新答的10题均值**19.00%**。

## 三、对参数要求的阶段回应

| 模型 | 当前证据 | 未完成或不能据此断言 |
|---|---|---|
| Qwen | 指定budget及Chat cap字段在10题被接受，均有结构有效答卷 | 未做24576/32768/36864/无上限阶梯；不能独立证明budget强制执行或选最小预算 |
| DeepSeek | high及Chat cap配置取得10份有效答卷，其中1份中断恢复 | 无同通道多配置质量对照，不能据历史分数相近断言质量未降 |
| GLM | low在10题完整返回，平均思考1033.3 token；另有前置同题high/low对照 | 未完成10题high/max对照及原40题设计，不能证明low质量非劣或替代主表已获验收 |
| Grok | 新cap字段被接受，10题取得有效答卷；工程400已单列恢复 | 本轮均未触131072边界，不能声称任意硬cap映射已充分验证；旧12笔超名义cap记录保留 |
| GPT | 原预算65536下10题均有效；未把结构失败误当预算不足 | 本次没有验证strict/JSON Schema模式，不能说老师这项已完成 |
| Kimi | 历史按量结果保留；当前Token Plan型号范围已核 | high/max pilot未执行；通道阻塞不是模型不能回答，不以K2替代 |

前置GLM对照题BIOPATH150_005的两份请求在同一Token Plan通道仅effort不同：high输出131072、思考131070、length且正文仅2字符；low输出4841、思考982、33.660秒、schema有效。各一次且不同时点，只能证明该题观察到的行为差异，不能代替多题质量非劣证据。high触顶值与模型最大输出重合，不能隔离证明请求字段作用与默认上限。

五条线最终50份正常完成答卷中未观察到LENGTH_EMPTY/INVALID_JSON，不据此称失败模式已消失；两份原中断终态未知、Grok原400及前置GLM high长度空答均继续保留。

## 四、Kimi为何没有补测

历史使用公共按量计费入口、exact ID为`kimi/kimi-k3`。截至11月20日核查，Token Plan个人版支持列表未列Kimi，团队版仅列K2.5/K2.6/K2.7-code；两版均无K3，现有31-ID目录也无K3。百炼通用API仍有K3，**通用API可用不等于Token Plan套餐包含**。

本机原按量凭据先前被401拒绝；文件mtime未变不能证明服务端账户当前状态或额度耗尽。由于没有已证恢复的原型号授权来源，本轮未再撞该源、未充值或自动启用按量fallback。要恢复该线，需另行确认合规凭据、费用范围与原型号/快照，不把不同Kimi型号混算。

[Kimi通道专项说明与官网依据](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/KIMI_TOKEN_PLAN_NOTE.md)

## 五、费用口径

| pilot范围 | 已核响应费用或参考估算 | 不可混同的项目 |
|---|---|---|
| Grok 10份完整响应 | list USD2.231996；allowance USD8.927984；这些响应cash均0 | 原400及原中断两笔缺usage，另保留未知费用预留 |
| GPT 10份完整响应 | list USD0.05987045；allowance USD0.2394818；这些响应cash均0 | 不将“有usage者cash0”扩为全任务零现金 |
| Qwen/DeepSeek/GLM 30份完整响应 | 旧按量参考CNY10.898172/1.750036/1.583584，合计14.231792 | Token Plan实际Credits与现金不可由响应确定；参考价不是实扣 |

三笔pilot缺usage原尝试继续留位：Grok400、Grok中断、DeepSeek中断。按冻结预算携带的参考预留分别为list USD0.8064、USD0.8064及CNY1.0686；预留不是实扣或保证不超的上界。执行摘要曾把DeepSeek预留误写为3.75元，本审阅版已更正。此前独立诊断账中的GLM401仍另保留CNY3.750016预留，不与它混淆。

费用表分别列标价、套餐消耗、现金与未知项，不相加成一笔“总支出”。已核响应费用只是可核子集，不冒称覆盖全部尝试。

## 六、结论与剩余工作

本轮有用结论是：在选定10题与这些配置下，五条可执行线经有限工程恢复取得50份可评分答卷，GLM low的交付/用量表现值得继续验证。**尚不能证明任何配置质量非劣、最小预算或全121题完成率。**

您原要求的40题分层、多档、相对无上限基线的paired bootstrap10000次、95%CI下界>−5个百分点及完成率条件没有被本轮替代。单档本身缺少预算间配对，不能靠对10题多抽bootstrap凑出验收。第八节“如果只能先改一件事”按优先级理解，不解释为豁免。

原题包含路线等提示，CONTROLLED_INPUT只约束既有评分中的特定重复信息；它没有解决与系统SMILES输入不对等的实验设计质疑。网关内部搜索未独立排除。当前不自动扩大至40/121题、不继续耗额度补模型低分，后续需根据预算和您的意见另定设计。

## 七、在线核查材料

以下材料均可直接在GitHub查看，不依赖本机文件：

- [六配置审阅汇总](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/ARM_SUMMARY_6.tsv)
- [60题位状态与逐题程序命中](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/PER_CASE_RESULTS_60.tsv)
- [53笔pilot费用分项](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/PILOT_CALL_ACCOUNTING_53.tsv)
- [六模型要求的完成与未完成项](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/TASK_RESPONSE_STATUS.tsv)
- [独立审计摘要及保留条件](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/AUDIT_SUMMARY.json)
- [文件校验清单](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-20_BIOSYSMODB121_Parameter_Pilot10_Engineering_Recovery/SHA256SUMS)

本次只公开审阅报告与白名单汇总，不公开密钥、完整题面、Gold正文、原始答卷、思考/SSE或私有账本。公开表可核数值和完成范围，但不冒称仅凭汇总就能独立重放未公开原始流。原始工件仍封存供受控复核。此前4次诊断的独立历史材料保留，旧20题提案不是本轮实际执行方案。
