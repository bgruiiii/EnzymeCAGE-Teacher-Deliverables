# 基模API测试框架交接

2026-11-17。供复用既有模型采集框架时参考。本包覆盖国内四模型的阿里调用，以及后来Grok/GPT的OpenCode调用；讲清实际发送位置、输入输出、流解析、断点与历史问题。

## 最先看这几处

| 想了解什么 | 入口 |
|---|---|
| 请求怎么装配、怎么发、响应怎么保存 | [调用链与数据流](docs/CALL_CHAIN.md) |
| 到底哪个函数发了HTTP请求 | [源码导航与行号](docs/SOURCE_MAP.md) |
| 当时出了什么问题、哪些代码不能照搬 | [已知问题与处理](docs/KNOWN_ISSUES.md) |
| 师兄接到自己的题目/账号时怎样复用 | [最小迁移指导](docs/REUSE_GUIDE.md) |
| 不读Key、不联网的流解析示例 | [离线示例](examples/README.md) |

## 框架做的事

```text
题目元信息 + 原题模板 + 答题JSON要求
→ 渲染为独立user消息，核题目/消息SHA
→ 给每个“题目×模型”建立slot、请求body和稳定session
→ 费用预留、持久提交记录、进程锁
→ Python直接POST到阿里/OpenCode
→ 原始SSE/错误体/进度增量归档
→ 提取最终正文、usage、返回模型与终止状态
→ 本地JSON/Schema检查
→ 索引、汇总、原始流重放与断点接续
```

这是**让基模回答题目的采集框架**。其后进行的Gold程序评分、Hit@1和李克特裁判评分另有代码，不是同一个发送任务。基模作答请求没有塞Gold、旧分、其他模型答案或检索工具输出。

## 两条实际接口

| 场景 | 协议与端点 | 真正的发送代码 |
|---|---|---|
| 国内Qwen/DeepSeek/Kimi及G8阶段GLM | 阿里Chat Completions：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `source/aliyun/g8_formal_runner.py` → `HttpTransport.stream()` → `urllib.request.urlopen()` |
| GLM后续max128K修正配置 | 同阿里端点，单独配置 | `source/aliyun/glm_max128k_runner.py` → `HttpTransport.stream()` |
| Grok/GPT扩展采集 | OpenCode Go Responses：`https://opencode.ai/inference/go/openai/v1/responses` | `source/opencode/batch.py`、`gpt56_full.py`等 → `opener.open(req)` |

早期通用采集器`source/aliyun/run_collection_v2.py`还保留`requests.post()`发送路径。它是代码沿革基础，不表示后续每个正式批次都从它的`main()`发请求。

## 原实验的输入与参数

- 正式题集实际121题。部分目录叫150是历史名字；四主配置原生A批共484位置。旧B120恢复集和首次采集不同。
- 一题一个独立user消息，原题内已有路线/条件、逐步反应、首选酶/EC、微生物、性状和JSON输出要求。没有额外system/developer和Gold。
- 阿里通常用`messages`、`max_tokens`；OpenCode Responses用`input`、`max_output_tokens`，不能只换URL不换封套。
- 原OpenCode Grok/GPT请求上限65536；Grok显式temperature=0，Luna历史请求不发temperature。GLM后续修正为独立131072配置，不能说全部模型输出预算相同。
- OpenCode带`Authorization: Bearer <本机Key>`、真实客户端标识和持久`x-opencode-session`；工具为空。历史Grok省略tool_choice，Luna发none。
- 历史参数是当时实际记录，不是保证当前任何模型仍支持同样字段或价格。

## 源码怎样放置

```text
source/aliyun/             原始采集器、G8正式发送、GLM独立配置
source/opencode/           pilot→session修复→收流→小批→全量→5.6独立接续
source/repair_reference/   当时修复测试/安装器参考
reference/                原题模板、原输出JSON Schema
examples/                 全部为SYNTHETIC的请求和SSE，不是真实答卷
provenance/               源文件SHA和函数行号索引
```

**`source/`是17份历史源码的字节一致快照，不是已经移植好的通用SDK。** 原脚本有旧路径、批次常量、旧授权门和已知缺陷；不要在新机器上直接运行历史批次入口。特别是`full_run_historical.py`含已知费用bug，`full_run_repair_candidate.py`另存的是当时修复候选，不冒充它已经完整替代了现场版本。先看KNOWN_ISSUES再取用对应函数。

## 可立即执行的离线检查

在解压后的本目录运行，Python≥3.10，无需Key或第三方库：

```bash
python3 -B tools/replay_demo.py
python3 -B tools/verify_package.py
```

示例会重放合成Chat/Responses流、演示费用预留结算差异，不发HTTP、不读账号。离线通过只证明包内示例和文件一致性，不证明真实服务连通或模型答案正确。

本包不带密钥、账户账本、真实鉴权头、完整Gold、真实121题和真实答卷。原题模板和输出Schema便于理解输入格式；真实数据身份可由原项目冻结索引核对。源码来源和许可见[NOTICE](NOTICE.md)。
