# 本地运行与输入输出

以下示例均从拉取后的本目录运行。验证阶段不需要Key。单次收集工具使用Linux文件锁；其离线测试在Linux/Python3.10通过。历史源码只作导航，不以路径改名冒充通用SDK。

## 1. 查题目与导出既有参考

打开`questions/POLLUTANT_INDEX_121.tsv`，选题由师兄自行决定。

```bash
python3 -B tools/export_case_reference.py --case BIOPATH150_060 --out work/reference_060
```

输出是原题、旧任务scope、Gold/accepted切片和参考说明，**不是新答案的对齐/打分事实**。它不会改题、生成答案或推定新路线已被认可。全局别名表可能没有case字段，导出时原样保留。

## 2. 基模单次请求：默认只准备，不发送

将自己构造的请求body保存为`my_request.json`；协议封套参考`examples/original_generation_requests/`中的实际六模型请求。使用自己的配置文件，参考`config_templates/collection_opencode.example.json`或`collection_aliyun.example.json`。

```bash
python3 -B tools/collect_one.py --request my_request.json --config config.local.json --out work/my_case
```

这会核模型/协议、保存精确请求和状态，不读密钥、不发HTTP。不会改用户提供的messages/input、输出上限或科学内容；它只采用固定JSON编码，实际发送的同一bytes会落盘。

实际发送需自己在环境里设置配置指定的`BASE_MODEL_API_KEY`，将自己的配置`live_authorized`设true，并显式加`--live`：

```bash
python3 -B tools/collect_one.py --request my_request.json --config config.local.json --out work/my_case --live
```

不要将Key写进请求体、源码、压缩包或聊天。每个目标使用自己单独的out目录。相同目录重启遇已提交/完成/未知会去重，不自动重试；请求内容变了则拒绝混用旧目录。必须在自己任务层面管理批量预算、限流和unknown，不能将换一个目录当作未发过请求。

这个入口只处理一份给定请求，不带20题抽样、循环重试或自动充值，不进行业务Schema/科学校验。HTTP200、JSON可读与科学正确仍分开。原始流、正文、usage、真实返回模型和计费字段保存在out目录。返回model缺失或不符不会用请求值回填。

## 3. V0.5评分：输入不是只有一段答案

按`likert_v05/examples/synthetic_item.json`的结构准备自己的prepared_item：

- 新实验实际题面、原始回答、case/item身份；
- 适用Gold、任务scope、accepted与证据目录；
- 根据新答案/新任务确定的程序事实、允许范围、已有上限依据；
- 所引用材料确实存在，不能沿旧答案的CTX/对齐矩阵偷换。

代码不会从污染物名字自动生成所有正确参考。真实事实合同的来源实现见`code/runtime/v05_release/build_items.py`、`rules_03a.py`和`latest_scoring_source/`；它们有原实验路径/数据依赖，移植时必须按实际题答重建输入。

在评分代码子目录运行：

```bash
cd likert_v05
python3 tools/likert_cli.py prepare --item ../work/my_item.json --out ../work/my_rating_request.json
python3 tools/likert_cli.py validate --request ../work/my_rating_request.json --response ../work/judge_response.json
python3 tools/likert_cli.py merge --request ../work/my_rating_request.json --response ../work/judge_response.json --out ../work/my_rating.json
python3 tools/likert_cli.py totals --rating ../work/my_rating.json
```

实际裁判API调用和本地配置见`likert_v05/docs/RUNNING.md`。该导出CLI裁判ID仍钉为`deepseek-v4.1-flash-1017`，不能只把它改成GPT就宣称验证通过；“GPT生成答卷”和“裁判给答卷打分”是两次不同调用。

## 4. 快速核对代码确实可运行

```bash
python3 -B tools/verify_bundle.py
python3 -B generation_framework/tools/replay_demo.py
python3 -B likert_v05/tools/verify_package.py likert_v05
python3 -B likert_v05/tools/likert_cli.py validate --request examples/real_original_task/request.json --response examples/real_original_task/response.json
python3 -B -m unittest discover -s tools -p 'test_collect_one.py' -v
```

`likert_v05`的合成示例只用于协议测试，真实样例来自原S12正常返回，不能将其分数当新自由路线实验预期。所有随包配置默认禁用真实调用；此包整理与验收没有发任何模型请求。
