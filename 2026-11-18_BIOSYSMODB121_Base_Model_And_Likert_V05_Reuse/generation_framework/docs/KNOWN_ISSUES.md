# 历史问题：发生了什么，复用时怎样处理

下表依据原始执行源码与后续独立审计整理；“本地代码修复”和“服务端问题已解决”不能混写。

| 问题 | 证据与后果 | 当时处理/复用建议 |
|---|---|---|
| 首个OpenCode请求缺session | HTTP400 MissingSessionID；pilot旧版不带session | R1加入持久`x-opencode-session`，重启不临时换掉同一目标身份；不要复制旧pilot发送头作为最终版本 |
| 空tools与tool_choice不兼容 | 历史Grok对特定空工具参数组合拒绝 | 只做已登记的协议修复，原题不改；按具体模型支持项装配，不给所有模型硬塞同一参数 |
| 将长推理误判卡死 | Grok曾连续输出reasoning、很久后才出正文 | 观察原始流字节/事件/最后活跃时间；区分无字节超时、无正文和总时长，不因没正文直接杀进程 |
| Chat解析器直接套Responses | 事件结构不同，终帧可能再次带完整正文 | 协议分别解析，增量与终帧重放比对，不能重复拼接；本包提供离线合成演示 |
| HTTP200被误作成功 | SSE中可能出现error/incomplete，无完成usage | 同时核终帧、状态、正文和usage；完整接收与科学正确分开 |
| GPT6持续HTTP429 | 原错误为Token rate limit exceeded；短请求、新Key也曾失败 | 只证明服务拒绝，不能据此断言余额耗尽、精确TPM或恢复时间；程序退避不是平台重置时间；后来5.6独立新线成功，未把型号混成121题 |
| 调度等待与其他长请求join耦合 | Luna冷却后不一定有独立调度者立即续发 | 修复候选将等待队列独立处理，用假时钟测试；不能让测试真睡数十分钟 |
| 本地提交不等于HTTP确已发出 | TLS/上传边界未知；中断后可能已计费 | 发送前持久提交，unknown保留，重启先查档；不要把所有已提交都当已完成或免费失败 |
| 费用预留先被覆盖再结算 | 历史full_run的settle_success先将a.list_accounted改实际费用，再以它减预留，差额失效 | 保存原reserved_list/reserved_allowance再更新；候选文件有对应修复；本包离线演示会显示旧新差别 |
| B来源计费字段被替换后才门控 | 历史finalize把r临时覆写为go-plus/cash0后传gate | 不能把改写后的对象当服务原始事实；修复候选用真实返回直接核；原始流审计未发现实际现金异常，但不证明旧门控正确 |
| 旧预留高估与漏结算 | 最终审计纠正旧“约70.2美元占用”，另补漏结已知费用 | 不改历史原账来制造一致；从原usage与attempt生成派生结算，不清真正unknown，不把纠正当退款 |
| allowance误作标价或现金 | 部分响应allowance约为list_cost的4倍 | 分开list_cost/allowance/cash/unknown，不把4倍固定为新模型规则，不将其与价目表月额度直接错比 |
| 旧模块全局路径串写 | 早期监护写入旧R2监控文件 | 原件恢复后复验；迁移时显式给输出root，避免import旧模块后仍指向旧W目录 |
| 旧状态报告滞后 | FINAL_STATUS/配置文件可能未跟随正在运行的worker更新 | 以实时ledger、attempt/lifecycle和实际代码绑定为据；不要拿上一轮摘要断言“当前没在跑” |
| 输出上限与返回usage不一致 | 12份Grok报告output_tokens超请求65536，最高92071 | 保留原usage和请求，同时披露服务差异；不截断或伪改计费数字，原因不能凭空推定 |
| 模型原答JSON/Schema失败 | GPT5.6首答114/121结构有效，7题失败；083缺字段，其余6份语法错 | 原始终帧/正文重放证实不是本地拼坏；授权后原题独立第二答，不给旧错答、不覆盖首次通过率 |

## 费用bug的最小例子

先预留0.8美元，实际0.1美元。正确做法应把accounted减0.7、unknown减0.8。旧代码先把attempt.reserved覆盖成0.1后再相减，会让accounted仍是0.8、unknown剩0.7，造成虚高。本包离线演示测试这个算术，不是真实账户费用。

`source/opencode/full_run_historical.py`保留现场历史源码，包含上述已知问题；`full_run_repair_candidate.py`是另存候选。候选曾有定向离线测试，但不能据文件名就认为所有后续现场批次均已运行它。师兄应从修复机制取用，不执行旧安装器去改自己的工程。

## 原结果怎样解释

- Grok累计：121位置、120完整、119结构有效；087未完整、145字段格式失败。
- GPT5.6：121首答、114结构有效；7题另获授权各重答一次后形成114首答＋7第二答的121可用视图，不能写首答121/121。
- GPT6：35份部分结果，未与5.6拼接，不并入六模型主排名。

这些是当时采集结项口径，不代表后来李克特或Hit@1评价的最新数量。采集问题未要求重买已经成功的答卷。

## 审计出处

- 原项目`04_Local_Review_Audits/FOREIGN_NATIVE_GO_PLUS_FIRST10_FINAL_REVIEW_20261109/REVIEW.md`：流重放、计费三口径、额度换算勘误。
- 原项目`04_Local_Review_Audits/FOREIGN_NATIVE_LUNA_RATE_DIAG_20261110/`：DIAGNOSIS、LUNA_ONLY_READONLY_FINDINGS、LIVE_PROBE_CONCLUSION。
- 原项目`04_Local_Review_Audits/FOREIGN_NATIVE_DUAL_SOURCE_FIX_20261110/README.md`：结算、计费门、调度的修复范围。
- [最终国外模型采集审计报告](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-11-11_BIOSYSMODB121_Foreign_Model_Collection_Final_Audit/TEACHER_REPORT.md)：完整接收、7题版本映射及费用纠正。

上述原项目路径用于回溯，不是包内依赖。必要内容已在本页摘明，不需要访问作者本机才能读懂问题。
