# 运行说明

所有命令均在本日期目录运行。Python≥3.10；需要实际调用时安装`requirements.txt`。合成离线检查不需要真实key，不需要本地原工程路径或完整Gold。

## 1. 先跑合成示例，不调用API

```bash
python3 tools/verify_package.py .
python3 -B -m unittest discover -s tests -v
python3 tools/likert_cli.py prepare --item examples/synthetic_item.json --out work/example_request.json
python3 tools/likert_cli.py validate --request work/example_request.json --response examples/synthetic_response.json
python3 tools/likert_cli.py merge --request work/example_request.json --response examples/synthetic_response.json --out work/example_result.json
python3 tools/likert_cli.py totals --rating work/example_result.json
```

示例分数只是标记为SYNTHETIC的验证fixture，不能用于论文、模型排名或科学结论。真实评分由模型返回，不是示例中预填的整数。

## 2. 只补原NE维度

```bash
python3 tools/likert_cli.py prepare --item examples/synthetic_item.json --dimensions D3a --out work/partial_request.json
python3 tools/likert_cli.py merge --request work/partial_request.json --response examples/synthetic_repair_response.json --baseline examples/synthetic_repair_baseline.json --out work/partial_merged.json
```

只替换指定旧NE，另外六维逐字段不变。试图覆盖已有数值/MISSING会被拒绝。原F2总分函数处理NE/NA，不自行补0或变权重。

## 3. 真实输入必须包含什么

参照[synthetic_item.json](../examples/synthetic_item.json)的字段，换成你有权使用且已冻结的真实材料：

- 匿名item/case/batch身份，逐字原题和原答案；
- 本案Gold切片、任务scope、accepted、证据与真实引用目录；
- 程序已构造的各维范围、D3a决定和KEY上限；分支案还要带一条或多条已采纳路径的范围说明，不能用全图行数当单条主链必答分母；
- 证据版本、具体支持范围。评价侧补证与模型原交付来源分开，不能把新找到的文献回填成模型引用。

这个移植入口消费**已准备的事实合同**，不声称从一段答案自动得出Gold或所有科学判断。原合同的生成代码保留在`code/runtime/v05_release/build_items.py`、`rules_03a.py`及原批次装配源码；用它们重放历史706份，需要原有冻结输入与registry等数据资产。真实基准数据未公开，不因此用合成材料替代真实运行。

## 4. 真实API调用需明确开启

1. 在本机复制`config_templates/scoring.example.json`为忽略提交的`config.local.json`；核实exact model、HTTPS入口、当前服务与价格、金额/次数上限，再设置`live_authorized=true`。
2. 在本机环境中设置该配置指定的`ALIYUN_SCORING_API_KEY`，不要把值写进仓库或聊天。
3. 准备真实输入（`synthetic=false`），装配后执行：

```bash
python3 tools/likert_cli.py prepare --item private_inputs/item.json --out work/real_request.json
python3 tools/likert_cli.py run --request work/real_request.json --config config.local.json --work work/live_run --i-confirm-live-paid-calls
```

该命令会付费调用，文档整理/验证阶段未执行。默认配置和SYNTHETIC输入均禁止真实调用。配置中的2/8元每百万token只是历史折算示例，不保证当前价格；usage估算不是套餐现金实扣。

请求先预留费用，返回先归档和结算再验证。work内保留原始请求、SSE、安全meta、usage、响应model、费用账与结果。同一请求身份已尝试但无结果时拒绝盲重发，unknown储备不清零。明确的错误返回也不能因最终没有有效评分就记成免费。

移植CLI是受控单key单请求入口；原批次并发和备用key切换的实际代码保留在`code/executed_workflows/execution/`，没有假称本次新CLI已经上线复测全部并发/多key组合。继承现有长批次时必须接原最新完整账，不新建一份余额洗掉历史。

## 5. 许可与资料边界

work、private_inputs及本机配置默认被本目录`.gitignore`排除。不得将真实key、原始答案/SSE、完整Gold、账户信息或许可未知全文顺手提交。历史源码中出现的环境路径是原实现记录；请从可运行适配入口开始，勿直接启动未知环境的历史批次脚本。
