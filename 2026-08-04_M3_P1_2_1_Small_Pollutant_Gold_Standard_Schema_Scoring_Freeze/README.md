# M3 P1.2.1 18 条污染物 gold standard / schema / scoring freeze

日期：2026-08-04  
状态：`M3_P1_2_1_GOLD_SCHEMA_SCORING_FREEZE_PASS`  
用途：回应黄老师 2026-08-03 清单中 reaction fallback 横向比较的前置要求：

```text
18 条污染物 gold standard 固化；
统一评估脚本；
三工具输出 schema 归一化定义；
弓模型返回后按同一脚本完成 F6 三工具横向比较。
```

## 1. 本包是什么

本包从 Chenyu 返回包：

```text
enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_rerun1_20260804.tar.gz
```

中提取可审阅文件，放入 teacher-deliverables，避免只给一个压缩包导致老师无法直接查看。

本包包含：

- 18 条小污染物 strict v0.1 gold standard；
- 18 条 blind parent input；
- 39 条 accepted product/reaction gold labels；
- 三工具统一 prediction normalized schema；
- 统一评分脚本；
- gold/schema/scorer 验证报告；
- BioTransformer ENVMICRO 与 enviFormer latest 的 replay scoring；
- 本地审计和原始返回包 identity。

## 2. 关键文件

Gold standard：

```text
gold_standard/SMALL_POLLUTANT_STRICT_V0_1_CASES.csv
gold_standard/SMALL_POLLUTANT_STRICT_V0_1_BLIND_PARENT_INPUTS.csv
gold_standard/SMALL_POLLUTANT_STRICT_V0_1_GOLD_STANDARD_REACTIONS.csv
gold_standard/SMALL_POLLUTANT_STRICT_V0_1_GOLD_STANDARD_PRODUCTS.jsonl
```

统一 schema：

```text
schema/THREE_TOOL_PREDICTION_NORMALIZED_SCHEMA.md
schema/THREE_TOOL_PREDICTION_NORMALIZED_SCHEMA.json
```

统一评分和验证脚本：

```text
scripts/score_three_tool_predictions.py
scripts/validate_gold_schema_scoring_freeze.py
```

验证报告：

```text
validation/VALIDATION_REPORT.md
validation/VALIDATION_REPORT.json
FREEZE_REPORT.md
FREEZE_REPORT.json
```

Replay scoring：

```text
replay/biotransformer_envmicro/SCORING_SUMMARY.json
replay/biotransformer_envmicro/CASE_LEVEL_SCORING.csv
replay/biotransformer_envmicro/PRODUCT_LEVEL_SCORING.csv
replay/biotransformer_envmicro/NORMALIZED_PREDICTIONS.jsonl

replay/enviformer_latest/SCORING_SUMMARY.json
replay/enviformer_latest/CASE_LEVEL_SCORING.csv
replay/enviformer_latest/PRODUCT_LEVEL_SCORING.csv
replay/enviformer_latest/NORMALIZED_PREDICTIONS.jsonl
```

本地审计：

```text
audits/ENZYMECAGE_M3_P1_2_1_SMALL_POLLUTANT_GOLD_SCHEMA_SCORING_FREEZE_RERUN1_RETURN_AUDIT_2026-08-04.md
```

返回包 identity：

```text
archive_identity/enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_rerun1_20260804.tar.gz.identity.txt
```

## 3. 核心计数

验证报告记录：

```text
case_count         = 18
reaction_row_count = 39
product_jsonl_count = 39
blind_columns = case_id, pollutant_name, parent_smiles, parent_inchikey, input_policy
schema_json_parseable = true
synthetic_scoring_runs = true
```

Blind input 只包含 parent 侧输入和 case metadata，不包含 product、reaction、answer、evidence、url 等答案列。

## 4. 已完成的两工具 replay scoring

BioTransformer ENVMICRO：

```text
Hit@1  = 9/18  = 0.500000
Hit@3  = 13/18 = 0.722222
Hit@5  = 16/18 = 0.888889
Hit@10 = 16/18 = 0.888889
MRR@10 = 0.619444
recovered products@10 = 20/39
```

enviFormer latest：

```text
Hit@1  = 0/18  = 0.000000
Hit@3  = 1/18  = 0.055556
Hit@5  = 1/18  = 0.055556
Hit@10 = 1/18  = 0.055556
MRR@10 = 0.027778
recovered products@10 = 1/39
```

## 5. 当前边界

本包完成的是 F6 前置条件，不是 F6 最终闭环。

当前不能声称：

```text
三工具横向比较已经完成；
弓师兄模型已经评分；
BioTransformer 已被正式选为 fallback 引擎；
18 条 benchmark 代表所有污染物降解反应。
```

当前可以声称：

```text
18 条污染物 gold standard、blind input、统一 schema、统一 scorer 已固化并通过 Chenyu 验证；
BioTransformer ENVMICRO 和 enviFormer latest 已用同一 scorer replay；
弓师兄模型返回后，可以用同一 schema/scorer 完成 F6 横向比较。
```

## 6. SHA256

本包文件身份见：

```text
DELIVERABLE_SHA256SUMS.txt
```
