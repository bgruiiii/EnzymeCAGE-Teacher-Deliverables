# Kimi-K3调用通道与Token Plan可用性说明

核查日期：2026年11月20日。此说明用于并入本轮参数试验阶段反馈，不是全部模型试验的最终结项报告。

黄老师您好：

历史Kimi正式采集使用百炼公共按量计费Chat Completions入口`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`，实际请求与响应模型ID均为`kimi/kimi-k3`，不是Token Plan通道。历史结果保留，不因本轮通道不可用而作废。

考虑到本轮可用预算，我们改用已配置的百炼Token Plan完成能够执行的模型配置。但经核查，截至今日：

- 官方Token Plan**个人版**“支持的模型”列表未列Kimi-K3。
- 官方Token Plan**团队版**列出的Kimi型号为`kimi-k2.5`、`kimi-k2.6`、`kimi-k2.7-code`，也未列K3。
- 我们11月19日已取得的模型目录响应共31个ID，无`kimi-k3`或`kimi/kimi-k3`；本次核查复用该目录，没有再花额度进行鉴权或生成探针。目录出现K2系列也不构成当前Key拥有这些型号调用权限的证明。
- 百炼通用Kimi API文档仍列有K3，并说明按输入、输出Token数量计费；**百炼通用API存在该型号，不等于Token Plan套餐包含该型号**。通用文档的`kimi-k3`与历史`kimi/kimi-k3`也不能未经核实便声称权重/快照相同。

因此，本轮将Kimi的10个计划题位记录为**通道/套餐可用性阻塞，未发送、未评分**，不记为模型答题失败或科学零分，也不以K2系列代替K3。历史按量通道的本机凭据曾被401拒绝，该事件不能用来证明K3已下线或额度耗尽；恢复按量调用需要有效凭据与单独明确的费用安排，不会自动启用。

当前结论是“**官方公开列表与现有目录均未提供本轮所需K3的Token Plan调用支持**”，不扩张为永久不支持，亦不排除未来更新或另行确认的特殊授权。若后续恢复原型号合规通道，可按预登记范围独立补测，并披露通道与版本差异。

## 官方依据

1. [Token Plan个人版订阅与权益：支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)
2. [Token Plan团队版订阅与权益：支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-team-overview)
3. [Token Plan常见问题：模型范围、鉴权与计费入口隔离](https://help.aliyun.com/zh/model-studio/token-plan-faq)
4. [Kimi通用API：模型列表与计费](https://help.aliyun.com/zh/model-studio/kimi-api)

本说明不包含密钥或本地依赖链接；官方页面可直接在线核查。对应页面快照及历史配置身份已在本地审计目录封存。当前未充值、未换模型、未新增生成请求。
