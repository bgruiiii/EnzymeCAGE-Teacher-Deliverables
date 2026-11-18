# 合成请求与原始流示例

本目录全部是SYNTHETIC，不是真实题目、模型响应、费用或科学结果。只用于理解Chat/Responses封套和离线解析，不可计入实验统计。

- `chat_request.json`：messages封套。
- `responses_request.json`：input封套。
- `safe_headers.json`：不含任何密钥的头部形状。
- `chat_stream.sse`、`responses_stream.sse`：中文增量与终帧。
- `expected.json`：期望正文和合成usage。

在包根执行`python3 -B tools/replay_demo.py`。脚本只从历史源码AST提取纯解析函数执行，不import历史runner，不调用其中main/prepare/run，不联网、不读Key。示例输出不满足完整生物学答题Schema，这是有意的最小协议演示，不能据此报告科学schema通过。
