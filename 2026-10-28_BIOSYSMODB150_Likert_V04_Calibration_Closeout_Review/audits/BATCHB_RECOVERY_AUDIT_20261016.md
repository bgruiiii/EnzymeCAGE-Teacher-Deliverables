# 批次B四模型剩余6槽补齐最终本地审计

- 审计日期：2026-10-16
- 审计结论：`PASS_AFTER_SCHEMA_ONLY_RETURN_REPAIR`
- 批次A标签：`batchA_native_single_shot`
- 批次B标签：`batchB_recovery_inclusive`

## 结论

6个剩余模型-题目槽均使用与批次A逐字节相同的请求体再次派发，6/6得到`USABLE`终态：Qwen 1/1、DeepSeek 1/1、Kimi 2/2、GLM max 2/2。批次A、G9和G10均未回填或重算。

结合此前GLM max重挑战结果，批次B恢复输出数为：GLM max 16、Kimi 2、DeepSeek 1、Qwen 1，共20份恢复输出。F022/BIOPATH150_023在A、B两次均达到131072上限，按黄老师方法论不做第三次采样并从共同题集剔除。

因此批次B可用题数为：

| 模型 | 批次A可用 | 批次B可用 | 恢复输出 |
|---|---:|---:|---:|
| qwen3.8-max | 120 | 121 | 1 |
| deepseek-v4.1-flash | 120 | 121 | 1 |
| kimi/kimi-k3 | 119 | 121 | 2 |
| GLM-5.3 max-128K corrected | 104 | 120 | 16 |

四模型共同题集为120题，即冻结121题减去BIOPATH150_023。共同题集内共有480个模型输出，其中20份为`recovered=true`，其余460份为批次A原生可用输出。

## 独立核验

1. 原始回包SHA256=`4979877588546dc2ed7ab23e3824f8133a6e76ba251480140e88023c77608772`，单根93成员、内部78/78哈希通过。
2. 审计发现原始回包漏装receiver所需的Draft-07 schema；没有schema时，脱离runtime调用receiver会因schema文件缺失被错误归类为JSON_INVALID。该问题是封装缺陷，不是模型输出缺陷。
3. 从正式输入回包提取同一冻结schema（SHA256=`ebf2d47fd4737d7bdb020910b269b9245990d6e9a3e5b37570d8c572ac3bb9ae`）后，6份持久化raw SSE用对应冻结runner重放均为`USABLE`、schema_valid=true、slot_pass=true，完整性发现为空。
4. 6个请求体与三份正式源回包对应槽逐字节一致；6个provider request ID非空且唯一；batch标签、recovered标记和recovery时间戳6/6齐全。
5. R005第一次在途请求因主机休眠结果未知，恢复重派的请求体SHA及本地commit key一致。故本轮有6个唯一目标、6份终态响应、7次实际传输尝试，其中1次为主机中断恢复。
6. 6份终态usage的本地费用估算为14.665906元；账本残留3.750016元为R005中断重派的重复预留。第一次中断请求是否被供应商计费未知。

## 回包修复

保留原回包不动，另生成R1修复回包：

```text
03_HPC_Returned_Result_Summaries/
biosysmodb150_batchb_four_model_remaining6_recovery_return_r1_20261016.tar.gz
bytes=3325874
sha256=de9718022a5cf4ddfbcf8d2e62b7b6db55930d638ea5699b5090830d2ec3e91d
```

R1只新增冻结schema和`REPAIR_DISCLOSURE.json`，原响应、状态和科学结果零修改；确定性双构建一致，单根95成员，内部80/80哈希通过，脱离runtime独立重放6/6通过。后续共同题集与批次B评分必须使用R1修复回包。

## 审计修正

执行报告原来的“GLM 16、Kimi 4、DS 2、Qwen 2”混合了A/B记录数。正确的恢复输出数是GLM 16、Kimi 2、DeepSeek 1、Qwen 1。46目录报告及其SHA256SUMS已同步修正。

```text
FINAL_AUDIT_STATUS=PASS_AFTER_SCHEMA_ONLY_RETURN_REPAIR
BATCH_A_MODIFIED=false
BATCH_B_COMMON_CASES=120
BATCH_B_OUTPUTS=480
BATCH_B_RECOVERED_OUTPUTS=20
QWEN_BATCHB_USABLE=121
DEEPSEEK_BATCHB_USABLE=121
KIMI_BATCHB_USABLE=121
GLM_MAX_BATCHB_USABLE=120
PERSISTENT_FAILURE_CASE=BIOPATH150_023
UNIQUE_TARGETS_THIS_RUN=6
RECORDED_FINAL_RESPONSES_THIS_RUN=6
TRANSPORT_ATTEMPTS_THIS_RUN=7
FORMAL_SCORES_RECOMPUTED=false
API_CALLS_DURING_AUDIT=0
NETWORK_CALLS_DURING_AUDIT=0
```
