# T4正式18条parent输入身份回传

日期：2026-09-08
状态：`PARENT_ONLY_IDENTITY_RETURN_AWAITING_TEACHER_COUNTERSIGN`

## 1. 老师裁定与本地定位

老师09-08确认：本轮T4正式输入是08-07已冻结并审计接受的A7/gold包内18 cases，不是08-04历史小测试的任意
其他版本，也不是学生自建NON-BBD集合。

本地证据表明，A7/A8/A9对应的最终有效包是08-04生成、08-07老师接受冻结的rerun1：

```text
enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_rerun1_20260804.tar.gz
bytes=26359
SHA256=58feccb30056847acee41d2436263d770eea35a44d5d2d5a78e0ad20a06a3d3e
final_status=M3_P1_2_1_GOLD_SCHEMA_SCORING_FREEZE_PASS
teacher_accepted_on=2026-08-07
case_count=18
reaction_count=39
product_count=39
```

老师08-07原裁定写明：A7“18条gold standard固化，接受冻结，18 cases / 39 reactions / 39 products +
blind四件套”；A8评分脚本接受；A9统一schema接受冻结。

## 2. parent-only来源与文件身份

| 文件 | bytes | SHA256 | 用途 |
|---|---:|---|---|
| archive本体 | 26359 | `58feccb30056847acee41d2436263d770eea35a44d5d2d5a78e0ad20a06a3d3e` | A7/A8/A9冻结容器，不上传本GitHub增量包 |
| 包内`gold_standard/SMALL_POLLUTANT_STRICT_V0_1_BLIND_PARENT_INPUTS.csv` | 2220 | `9a4e28fd227f50fb354e86de2b7b332d625d6524e405309276169b35c1fa8bab` | 冻结blind parent来源 |
| 包内`gold_standard/SMALL_POLLUTANT_STRICT_V0_1_CASES.csv` | 6361 | `551d3ce3613808254c75108c674d87931e0feb5a0c547186756ce655038eabeb` | 冻结canonical parent字段交叉核对 |
| 包内`scripts/score_three_tool_predictions.py` | — | `29d213645d32553fd593e8c7f4f9c33660f8fed17fc03d7a1c615777684a35f3` | 老师指定后续固定评分脚本 |
| 包内`schema/THREE_TOOL_PREDICTION_NORMALIZED_SCHEMA.json` | — | `40fb2c19b9f1a7e29c101a7bb3b4d7bbf21a59fdac83cdc1ecf6fe0549be2de6` | 冻结输出schema |
| 本次`T4_FORMAL_18_PARENT_INPUTS.csv` | 1444 | `7b0e76d86c3bd33cc717c988e27c4f1aeba588be2c2ff48af665263382d67151` | 仅四个老师要求的parent字段 |

原始benchmark source archive身份同时保留：

```text
enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728.tar.gz
bytes=15018
SHA256=94637b47f7f0f3c755e7bda2c023b45c8b4f178409d3c39c75573b4b118603e4
```

## 3. 提取规则

本次CSV严格输出：

```text
case_id                         ← blind表 case_id
parent_name                     ← blind表 pollutant_name（按老师字段名重命名）
parent_smiles                   ← blind表 parent_smiles
parent_smiles_rdkit_canonical   ← cases表 parent_smiles_canonical，按case_id精确连接
```

本次18条中，blind表`parent_smiles`已经与cases表冻结canonical值逐条一致；仍保留两列，便于老师按要求回签。

## 4. 盲隔离检查

本次上传的CSV只有四个parent字段。未复制以下字段：

```text
reaction_id / reaction_smiles
product / accepted_product
answer / gold
EC / enzyme
evidence URL / answer-derived metadata
```

本次未上传含gold内容的archive，也未把gold反应/产物文件放入GitHub。预测端后续只接收老师回签后的
`T4_FORMAL_18_PARENT_INPUTS.csv`冻结副本。

## 5. 请老师回签

请老师核对本次18行及文件SHA。回签后我们将：

```text
T4_INPUT_STATUS=FROZEN_BY_TEACHER_COUNTERSIGN
唯一parent集合=本文件逐字节身份
模型=depending v3.2 + ECLIPSE
BioTransformer/enviFormer=沿用已有基线，不重跑
gold=预测端零接触
顺序=先冻结原始预测，再按固定脚本评分
指标=Hit@1/3/5/10 + MRR@10 + product recovery
```
