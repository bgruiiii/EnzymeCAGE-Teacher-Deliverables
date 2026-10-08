# BIOSYSMOdb150四模型121题正式API采集收口

日期：2026-10-08  
范围：Qwen、DeepSeek、GLM-low、Kimi K3，同一冻结121题；本文件不执行评分或新增API调用。

## 最终状态

```text
FORMAL_MODELS=4
FORMAL_CASES_PER_MODEL=121
FORMAL_SLOTS=484
FORMAL_COMMITTED=484
FORMAL_TERMINAL=482
FORMAL_USABLE_JSON=469
MODEL_CONTENT_FAILURES=13
RESULT_UNKNOWN_HELD=2
NOT_DISPATCHED=0
FORMAL_RETRIES=0
NO_MORE_API_CALLS_REQUIRED=true
API_COLLECTION_STATUS=CLOSED_READY_FOR_OFFLINE_MERGE
```

两个独立阶段均绑定内嵌输入包
`48a7e6835fe65994c14b293f4d4ead36aa616835c8727a82abc3f84c559fb222`；
Kimi与三模型的121 case顺序直接比较零差异。所有正式请求采用同一题面、schema、64K、
temperature=0、search=false及一次回答纪律；GLM另有冻结的thinking=true/effort=low模型级参数。

## 四模型结果

| 模型 | committed | terminal | usable | 内容失败 | held | 可用率/121 |
|---|---:|---:|---:|---:|---:|---:|
| qwen3.8-max | 121 | 120 | 120 | 0 | 1 | 99.17% |
| deepseek-v4.1-flash | 121 | 121 | 120 | 1 length+empty | 0 | 99.17% |
| ZHIPU/GLM-5.3 low | 121 | 121 | 110 | 11 invalid JSON | 0 | 90.91% |
| kimi/kimi-k3 | 121 | 120 | 119 | 1 length+empty | 1 | 98.35% |
| 合计 | 484 | 482 | 469 | 13 | 2 | 96.90% |

固定失败清单：

```text
Qwen held:       BIOPATH150_084
DeepSeek length: BIOPATH150_125
GLM invalid JSON: BIOPATH150_021,077,092,114,119,123,125,127,132,138,146
Kimi held:       BIOPATH150_050
Kimi length:     BIOPATH150_128
```

两次held发生在相邻时间的客户端shutdown事件，属于工程结果未知，不冒充模型内容失败。13个内容失败
均已有HTTP/SSE模型终态。按老师“一题一次、内容失败不重问、失败不静默删除”的合同，15个非可用槽
全部保留在各自121分母，不补JSON、不挑探针答案、不重新请求。

## 证据绑定

三模型正式回包：

```text
sha256=76a45fac8b54a3e5b6be549245cd7927233f4adbd9082766a886bf6bdf68b8ec
audit_sha256=4ede4adafe84901d322151e2500a246e0cb99a49f30c9f784658e5741305e3a6
```

Kimi正式回包：

```text
sha256=e17504af6c2927e9ba37c9f31eb0ec75aa346bfdc1ac28badd213fbcdf31e34c
audit_sha256=4fbc0a029d551689c4e4d6c8986f785492d4fe85a40b1b366cac5915c758544e
```

两包成员卫生、内部SHA、请求体合同、调用账本和detached replay均经本地独立审计通过。内部tmp/lock
仅为包装卫生问题；合并时读取权威`global_calls.json`/`kimi_calls.json`，忽略`.tmp/.lock`。
Kimi provenance中“用户逐字豁免辅助件”的表述不准确，以Kimi本地审计F3校正；直接实算身份仍成立。

## 成本与运行披露

三模型正式终态加Qwen held预留约182.45元；Kimi正式含held预留435.86014元；正式484槽合计估算
约618.31元。探针、smoke、pilot属于工程费用，不抵扣正式槽，也不混入正式评分。

Kimi返回5种system fingerprint；exact model ID与请求参数未变。最终报告须按fingerprint披露数量、
可用率、token与耗时，不因看到科学分后剔除某个fingerprint。

## 剩余离线收尾

API采集已经关闭。下一阶段只允许离线工作：

1. 建立四模型484槽只读合并索引，以`case_id + exact_model_id`唯一键绑定原始包、slot和raw SHA；
   held与内容失败生成显式缺失记录，不生成替代答案。
2. 在正式输出中按冻结种子20261006每模型抽2题，共8份，完成人工形态审阅；不得换样。
3. 对469份可用JSON运行冻结G3/G9评分器；15个非可用槽按固定121分母和既有缺失规则处理，
   工程held与模型内容失败分别披露。
4. 生成模型级科学分、工程可用率、成本、时长、fingerprint分层及权重±5pp敏感性报告。

在以上离线步骤完成前，状态为`API_COLLECTION_CLOSED / FINAL_SCIENTIFIC_REPORT_PENDING`；不得再启动
任何四模型正式、补问、JSON修复或选择性复现调用。
