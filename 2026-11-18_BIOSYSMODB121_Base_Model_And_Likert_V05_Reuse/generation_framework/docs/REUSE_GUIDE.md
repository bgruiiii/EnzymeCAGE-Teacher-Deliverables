# 师兄复用时的最小路线

## 先取机制，不复制历史批次入口

先看`SOURCE_MAP.md`里真正发送、接收、解析和持久化的位置；源码有旧目录、旧121题/484槽硬编码、旧模型和历史预算，不能把整个文件当通用SDK直接启动。此包没有改造新的付费runner，只有可独立运行的离线重放示例。

1. 用自己的题目形成固定case_id和完整messages，保存消息SHA；原始题目与请求参数一起登记。
2. 为选定模型固定确切ID、协议、上下文/输出上限、温度与推理字段支持项。原生API、网关别名及版本可见性如实记录。
3. 单独创建自己的work目录、运行身份、session与结果索引。身份至少绑定case、model、协议/端点、请求body SHA；不要共享作者历史ledger。
4. 复用构建body、发送前提交、原始流增量落盘、正文/usage提取、Schema校验、去重和unknown保护。Chat和Responses分别走对应解析器。
5. 预算用当前价格；OpenCode同时记录list_cost、allowance、cash和unknown。保留旧预留数后再结算，用真实返回做门控，不复制历史已知bug。
6. 先做本地合成/历史流回放；真正连通验证用计划任务里的少量目标，成功结果直接复用，再逐步扩量，避免额外反复购买探针。

## 请求要改哪些字段

| 接阿里/其他Chat兼容服务 | 接OpenCode Responses |
|---|---|
| messages、model、max_tokens、采样参数 | input、model、max_output_tokens、该模型实际支持参数 |
| 自己的Bearer key和HTTPS端点 | 自己的Bearer key、Go端点、稳定x-opencode-session、真实客户端标识 |
| choices/delta流与最后usage帧 | response事件、完成/失败终帧及usage.opencode |

不要把阿里`enable_thinking`、`enable_search`或某个response_format字段不加核对地发给其他模型。原OpenCode通过Go路径调用，不自动改成不带`/go/`的余额按量路径。没有支持项时登记缺省/不可观测，别伪称所有模型完全同参数。

最新的OpenCode模型目录和各模型支持协议会变。2026-11-17另一次只读检查发现两份历史Key的可见模型清单不同；目录GET成功也不证明长请求推理、实时额度和套餐现金零扣费已经核实。按自己的凭据和实际回包确认，不复制作者账号状态。

## 哪些状态不能丢

- NOT_DISPATCHED：可以派发。
- DISPATCH_COMMITTED/UNKNOWN：可能已发出或计费，先核档，不自动重发。
- COMPLETE：原始流、正文和用量完整；还须分开JSON/Schema结果。
- JSON/Schema失败：属于已返回的原答版本，不能因为格式差就覆盖原件。
- 第二答：单独attempt/session及版本映射，不按分数在多个答案中择优。

上述为交接中的通用语义，历史代码各阶段的精确状态名略有不同，迁移时建立显式映射，不靠名字猜含义。

## 范围边界

本框架只负责采集和工程校验。要用于裁判评分，需另装配相同量表/Gold/任务范围并换成裁判请求；要算预测准确率，还需独立Gold评测。格式通过不等于反应、酶或菌株正确。

不要运行`source/repair_reference/install_when_idle.py`替自己安装补丁；该脚本绑定作者旧现场。它的价值是展示有锁/有在途时不改运行代码的处理方式。
