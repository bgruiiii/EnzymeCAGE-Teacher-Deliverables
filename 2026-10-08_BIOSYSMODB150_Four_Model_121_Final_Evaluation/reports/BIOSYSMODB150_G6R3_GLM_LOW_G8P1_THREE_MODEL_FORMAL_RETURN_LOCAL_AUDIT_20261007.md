# BIOSYSMOdb150 G6-R3 / G8-P1三模型正式回包本地审计

日期：2026-10-07  
方式：本地只读、零API调用；不修改原回包、历史gate或模型答案。

## Findings

### F1（高）：13个非可用正式槽均不得重跑

正式363槽全部已经提交；362个有内容终态，1个为结果未知held，`NOT_DISPATCHED=0`。

- GLM-low 11槽：HTTP 200、SSE完整、`finish=stop`、正文非空，但原始JSON语法无效。
- DeepSeek 1槽：HTTP 200、`finish=length`，65,536 completion全部为reasoning，visible为0。
- Qwen 1槽：先落`DISPATCH_COMMITTED`后客户端退出，仅保存请求体，无raw/响应/request ID，状态为
  `RESULT_UNKNOWN_HELD_NEVER_RESENT`。

老师原合同规定JSON解析失败不得重问；正式每题一次，失败不得静默删除。本轮执行卡又冻结为零自动
重试和at-most-once。前12槽是模型内容终态，不能选择性补问；Qwen held可能已到达服务端，重发会
造成重复调用，也不能补发。若将来做工程复现实验，必须作为独立supplement并保留本轮失败，不能替换
正式槽或提高正式成功率。

### F2（中）：GLM-low正式JSON可用率仅110/121

GLM-low解决了high模式思考耗尽问题：正式121槽无length/空正文，平均42.162秒，平均completion
3,622 tokens；但11/121正文无法直接解析为JSON，可用率90.91%。失败case为：

```text
BIOPATH150_021, 077, 092, 114, 119, 123, 125, 127, 132, 138, 146
```

11份正文均以`{`开头、以`}`结束并包含实质内容，错误为内部缺逗号或缺值等JSON语法错误；不是
网络、截断、空壳或receiver误判。GLM-low pilot的9/10门仅说明小样本通过，未保证121题格式稳定。
该失败率应作为模型/配置表现进入最终报告，不能离线补JSON后冒充原始可用答案。

### F3（中）：Qwen一槽held使回包保持PARTIAL

`G8P1-S208 / BIOPATH150_084 / qwen3.8-max`于`2026-10-06T15:13:15Z`提交后，runner在客户端
shutdown期间退出。slot status保持`DISPATCH_COMMITTED`，没有raw或provider request ID。全局账本
按最坏预留2.479296元结算并永久held，随后resume没有重发。该处理符合at-most-once，但Qwen终态为
120/121，正式回包只能是`G8_P1_THREE_MODEL_PARTIAL_AUDITED`。

### F4（低）：回包含过期临时账本与未入内部SHA的锁文件

权威`ledger/global_calls.json`为377次、估算184.780276元；同时打入的
`ledger/global_calls.json.tmp`是旧快照（226次、108.73122元）。四个`.runner.lock`和
`global_calls.json.lock`未列入内部SHA256SUMS，不过外层tar SHA仍绑定全部成员。后续合并必须只读
权威`.json`，忽略`.tmp/.lock`；未来packager应排除这些运行时文件，避免口径混淆。

## 回包身份与可复现性

```text
file=biosysmodb150_g6r3_glm_low_then_g8p1_three_model_return_20261007T015420Z.tar.gz
bytes=95,804,898
sha256=76a45fac8b54a3e5b6be549245cd7927233f4adbd9082766a886bf6bdf68b8ec
members=4,897
uncompressed_bytes_about=1,427,619,840
```

- 无绝对路径、`..`、重复成员、链接或设备。
- 顶层`SHA256SUMS`独立复核4,458/4,458通过；`audit/SHA256SUMS`为521/521通过。
- 内部SHA并集覆盖全部实质文件；仅SHA文件自身和五个运行锁文件未覆盖，外层tar SHA覆盖全包。
- 四个phase detached replay均逐字节复现原判决：probe 1/1、smoke 3/3、pilot 9/10、formal
  350/363；formal integrity=0。
- 未检出API key或Bearer凭证形态。

## 调用与参数合同

```text
GLM probe=1
GLM smoke=3
GLM pilot=10
three-model formal=363
TOTAL_COMMITTED=377
KIMI_CALLS=0
RETRIES=0
```

正式矩阵恰为121 cases × 3 models，槽ID唯一；每模型121槽。参数实算：

| 模型 | 槽数 | 固定参数 |
|---|---:|---|
| qwen3.8-max | 121 | 64K, temperature=0, search=false，无thinking字段 |
| deepseek-v4.1-flash | 121 | 64K, temperature=0, search=false，无thinking字段 |
| ZHIPU/GLM-5.3 | 121 | 64K, temperature=0, search=false, thinking=true, effort=low |

363份slot status均含合法ISO UTC `committed_utc`；362个终态provider request ID全部非空且唯一；
响应model字段与三精确ID一致，system fingerprint均未暴露。121个GLM形态指标无模板空壳、无全null
且无证据的退化判例。唯一extra warning来自GLM case137的额外字段，不影响schema通过。

## 正式结果

| 模型 | 终态 | 可用JSON | 非可用原因 | 可用率（/121） |
|---|---:|---:|---|---:|
| Qwen3.8 Max | 120 | 120 | 1 result-unknown held | 99.17% |
| DeepSeek v4.1 Flash | 121 | 120 | 1 length+empty | 99.17% |
| GLM-5.3 low | 121 | 110 | 11 invalid JSON | 90.91% |
| 合计 | 362 | 350 | 13 | 96.42% |

DeepSeek失败槽：`G8P1-S308 / BIOPATH150_125`，completion=65,536、reasoning=65,536、正文0。
GLM失败槽及JSON错误位置已由raw重建，与落盘visible逐字节一致。全363槽中无代码围栏答案被
receiver剥离后“救活”；12个内容失败直接解析均失败。

正式阶段实测：

| 模型 | 平均秒/题 | P90秒 | completion均值 | 估算成本CNY |
|---|---:|---:|---:|---:|
| Qwen | 673.432（120终态） | 942.989 | 29,592.2 | 136.3089 |
| DeepSeek | 160.555 | 229.142 | 25,317.7 | 25.9615 |
| GLM-low | 42.162 | 62.107 | 3,622.1 | 17.7004 |

正式三模型实测合计约179.9708元；全局184.780276元还包括GLM探针/smoke/pilot及held预留，
与377调用账本一致，未触发1000元硬顶。

## 重跑裁决

```text
RERUN_GLM_INVALID_11=false
RERUN_DEEPSEEK_LENGTH_1=false
RERUN_QWEN_RESULT_UNKNOWN_1=false
RESUME_NOT_DISPATCHED=0
```

因此现在不发任何三模型补跑。最终四模型汇总时各模型分母保持121：内容失败原样计入；Qwen held
单列为工程结果未知并保留在分母，不伪装成模型科学回答。等待Kimi原题面121槽回包后，再把四条独立
账本按case/model键合并；不得用smoke、pilot、探针或后续复现答案填补正式空位。
