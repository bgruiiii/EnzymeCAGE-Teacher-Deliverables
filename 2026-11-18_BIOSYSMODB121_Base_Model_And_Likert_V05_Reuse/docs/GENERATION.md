# 国内4模型、国外2模型的原实验派发

## 原实验输入

正式题域121题，题号不连续；“150”是目录历史名字。原消息是一条user，既有路线/氧条件与答题JSON要求，无额外system/developer，不带Gold和其他模型答案。参考材料只在后续评价时使用。

`questions/original_messages/BIOPATH150_*.json`保留原文件，包含本地case_metadata和消息SHA。真正POST的是其中messages（Responses时转换为input）。不要将包含旧路线的整个JSON误当污染物-only输入。

## 六模型与实际入口

| 主配置 | 服务与协议 | 代码入口 |
|---|---|---|
| qwen3.8-max | 阿里Chat Completions | generation_framework/source/aliyun/g8_formal_runner.py |
| deepseek-v4.1-flash | 阿里Chat Completions | 同G8；不是后来裁判dated ID的独立实验 |
| kimi/kimi-k3 | 阿里Chat Completions | 同G8沿革；实际阶段参数按请求体 |
| ZHIPU/GLM-5.3 max128K corrected | 阿里Chat Completions | generation_framework/source/aliyun/glm_max128k_runner.py |
| grok-4.7 | OpenCode Go Responses | generation_framework/source/opencode/batch.py、full_run_historical.py |
| gpt-5.6-luna | OpenCode Go Responses | generation_framework/source/opencode/gpt56_full.py |

原生四配置各121位置；GLM-low不是第五个主模型。国外GPT6另有35份部分结果，没有和5.6拼成121，也没混入六模型主比较。

多数历史请求输出上限65536，GLM后续max128K配置131072；Grok显式温度0、Luna历史请求不传temperature，不能宣称所有模型参数绝对一致。原schema要求每步一个首选酶；多步不是多个候选排名。

原始A批失败与后来恢复视图须分开。包内原答索引是已发布选择：GPT5.6为114首答＋7份已选第二答；原四模型含已登记恢复版本；Grok为累计接收。7次第二答未改变首答114/121结构通过率。

## 谁真正发送请求

阿里G8：`run_slot()`→`HttpTransport.stream()`→`urllib.request.urlopen()`。

OpenCode：`dispatch()`或`dispatch_stream()`/`gpt56_full.run()`→`opener.open(req)`；流式接收复用`r2.receive()`，然后提取正文和usage。原始底层不是调用OpenCode交互式编码助手替我们答题，也没有让另一个模型改题转发。

详细函数行号、收流和问题位置见：

- [框架README](../generation_framework/README.md)
- [调用链](../generation_framework/docs/CALL_CHAIN.md)
- [源码导航](../generation_framework/docs/SOURCE_MAP.md)
- [历史问题](../generation_framework/docs/KNOWN_ISSUES.md)

历史脚本有硬编码路径、任务上限、旧预算和已知bug，不能直接启动它们的旧全量main。新薄入口collect_one只处理师兄传入的一份完整请求，保留原始流和去重，不承担20题实验设计。
