# 实际调用链和保存内容

## 1. 题目如何变成请求

原正式题面位于原项目`G2_questions/rendered_messages/BIOPATH150_*.json`，121题冻结索引另存。基础装配代码为`run_collection_v2.py`中的`render_blank_template()`、`render_prompt()`、`build_messages()`、`build_request_body()`。原通用模板见本包`reference/original_prompt.template.txt`。

用户消息包含输入污染物、指定路线/氧条件、完整输出字段和空JSON模板。它不是只问一个反应或只问一个酶。`case_id`为题目关联键；不能靠污染物名字合并不同路线。

G8正式运行直接读取已冻结请求body，不在发出前让另一个AI润色问题。外模扩展也复用原messages；`batch.body_for()`仅把`messages`放入Responses的`input`，保持题目内容SHA不变。

## 2. 阿里实际发送

```text
G8 main()
→ 读取InputPackage/slot矩阵、核请求body SHA
→ run_slot()
→ 锁内检查已提交状态、持久标DISPATCH_COMMITTED、预留预算
→ HttpTransport.stream(body)
→ urllib.request.Request(method='POST', data=JSON bytes, Bearer key)
→ urllib.request.urlopen()
→ parse_stream()
→ visible_answer.txt / raw_stream.sse / parse_meta.json / slot状态
```

早期`run_collection_v2.py`自身的路径为`execute_task()`→`run_attempt()`→`stream_attempt()`→`RequestsTransport.open_stream()`→`requests.post()`。注意识别正式批次究竟调用哪一个入口。

GLM后续有独立`glm_max128k_runner.py`：固定`ZHIPU/GLM-5.3`、131072输出预算及其协议，单独复验返回。这是独立修正配置，不能把它和原GLM-low混成一个实验臂。

阿里Chat Completions读取`choices[].delta.content`为正文、`reasoning_content`为提供方返回的推理字段、`finish_reason`和usage另存。早期G8收流先在内存累计再落盘；它不是后来OpenCode那套边接收边持久化的实现，迁移时不能混称。

## 3. OpenCode实际发送

小批路径：

```text
batch.worker()
→ batch.request()/body_for()核原题和参数
→ batch.dispatch()
→ 先落slot/attempt/session/预留费用
→ urllib.request.Request(..., x-opencode-session=固定session)
→ opener.open(req)
→ r2.receive()边收边保存raw_stream.sse和lifecycle
→ r2.materialize()解析终帧、正文、usage、Schema
→ r1_runner.gate()核返回和计费
→ 更新slot/ledger，保留失败/unknown
```

全量并发路径：`full_run_historical.worker_par()`→`parallel_queue()`→`dispatch_commit()`→`dispatch_stream()`→`r2.receive()`→`materialize()`→`finalize()`。发送与结算相关缺陷见KNOWN_ISSUES，不能照搬历史全量入口。

5.6独立正式路径：`gpt56_full.run()`→`check()`→`can_dispatch()`→持久提交→`opener.open(req)`→复用`r2.receive()`等。前5题从已通过审计的原始流复用，只发剩116题。`recollect7.run()`只处理明确列出的7个失败首答的新轮次，不给旧答或修格式反馈，原首答不覆盖。

## 4. Responses与Chat有什么不同

| 内容 | Chat Completions | Responses |
|---|---|---|
| 题目 | messages | input |
| 输出上限 | max_tokens | max_output_tokens |
| 正文增量 | choices[].delta.content | response.output_text.delta |
| 完成证据 | finish_reason及协议终止标识 | response.completed且response.status=completed |
| 不完整 | length/断流等 | response.incomplete/failed/断流 |
| 最终usage | 最后usage帧等 | completed响应的usage |

Responses终帧可能再次携带完整正文。增量正文和终帧正文不能拼两遍。可以互相核对，保存正文时选择单一来源。HTTP200也可能在SSE里返回error；有reasoning字节但暂时没正文并不代表进程卡死。

## 5. 每个目标应该保留什么

```text
run/<slot>/<attempt>/
  request_body.json       实际请求body，不能含鉴权头
  safe_request_headers.json  仅白名单头，不含Authorization/Cookie
  raw_stream.sse          真正收到的原始字节
  lifecycle.json          提交/首字节/阶段/最后字节等
  terminal_event.json     如提供，有完成/失败状态和usage
  visible_answer.txt      提取正文，原样保存
  schema_validation.json  JSON可读、字段是否合法
  result.json             模型、状态、usage、list/allowance/cash
  http_error_body.bin     如服务明确拒绝，敏感值先脱敏
```

实际各代文件名稍有差异，按代码核对，不能看到某个文件缺失就补造完成。进程已提交、HTTP已返回、收流完成、JSON有效、Schema通过、科学正确是不同层次。

## 6. 三条不能混淆的线

1. 采集：模型读取原题，输出完整降解答卷。
2. 程序科学评测：把输出与Gold对照，算路径/结构/酶/身份/性状或Hit@1。
3. 李克特：评价侧另外装配题目、答案和证据，让裁判打七维分。

本包交接第一条线。把Gold带入基模作答，会改变实验；把作答schema校验当科学准确率，也会改变解释。
