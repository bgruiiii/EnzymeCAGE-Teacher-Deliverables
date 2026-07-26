# M3-P1-2.1 路线裁定包独立提交前审计

审计日期：2026-07-26（Asia/Shanghai）  
审计对象：
`2026-07-26_M3_P1_2_1_Reaction_Predictor_Route_Adjudication/`  
结论：**PASS FOR ADJUDICATION SUBMISSION ONLY / NOT AN IMPLEMENTATION PASS**

## 1. 文件与字节身份

```text
人工编写入口:
  2
冻结证据副本:
  12
冻结证据与本地权威源逐字节 cmp:
  12/12 PASS
```

没有重写、截断或“清洗”冻结证据。答案钥匙、评分政策、人类可读评分报告、机器
评分报告和独立 validator 报告的 SHA256 均与本地权威源一致。

## 2. JSON 可解析性

以下 6 个 JSON 均以 Python 3 标准库重新解析：

```text
UNIFIED_PILOT_INPUTS.json:
  PASS
UNIFIED_PILOT_ANSWER_KEY.json:
  PASS
M3_P1_2_1_ANSWER_KEY_UNLOCK_AND_SCORING_POLICY_FREEZE_2026-07-26.json:
  PASS
M3_P1_2_1_REACTION_PREDICTOR_PILOT_EVIDENCE_REGISTRY.json:
  PASS
ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_TARGET_SCORING_MACHINE_REPORT_2026-07-26.json:
  PASS
ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_TARGET_SCORING_INDEPENDENT_VALIDATOR_REPORT_2026-07-26.json:
  PASS
```

## 3. 关键数字交叉核对

主入口与冻结评分报告逐项一致：

```text
解锁门禁:
  25/25 PASS
独立重算:
  43/43 PASS
反向测试:
  6/6 PASS

Route A:
  25/26 raw products RDKit parse
  正式 Top-1/3/5 不可评分

Route B ChatGPT 用户标签:
  case-level product Top-1/3/5 = 4/6, 5/6, 5/6
Route B DeepSeek 用户标签:
  case-level product Top-1/3/5 = 4/6, 4/6, 4/6
Route B Qwen 用户标签:
  case-level product Top-1/3/5 = 4/6, 4/6, 5/6

Route C-exact:
  directed Rhea Top-1/3/5 = 4/6, 5/6, 6/6
  complete reaction Top-5 = 6/6
  nonempty D4-valid pool = 4/6
Route C-generic:
  NOT_READY
```

## 4. 科学措辞与授权边界

主入口已明确保留以下边界：

```text
[x] C-exact 是冻结 Rhea 已知反应查表，不是未知反应泛化
[x] B 是 product-only，不冒充完整反应 / Rhea / EC / D4 pool recovery
[x] A 合同不兼容，不做后验字段修补
[x] D4 非空池不等于正确酶存在或排第一
[x] 模型名称/版本是用户标签，不是 API attestation
[x] 最终路线未选择
[x] 组合方案只是建议，需要新合同和裁定
[x] 未授权 reaction_prediction_node 活代码
[x] 未启动 M4b/M4c
[x] 未启动 M3-EXT 补资产或模型运行
```

## 5. 可提交结论

本包已达到“供刘老师 / 老师判断下一步路线”的文档与证据完整性要求。它没有达到、
也没有声称达到“反应预测 fallback 已实装”或“最终路线已验收”的状态。

```text
adjudication package:
  PASS
final route selected:
  NO
implementation authorization:
  NO
production readiness:
  NOT CLAIMED
```
