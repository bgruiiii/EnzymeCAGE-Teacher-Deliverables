# M3-P1-2.1 三路线答案钥匙解锁与目标评分本地独立审计

审计日期：2026-07-26（Asia/Shanghai）  
任务：`M3-P1-2.1 Reaction Predictor Three-Route Pilot`  
评分运行时：Python 3.12.13 / RDKit 2026.03.3 / CPU  
结论：**SCORING COMPLETE / C-EXACT FULL-REACTION 6/6 WITH TARGET RHEA TOP-1/3/5 = 4/5/6 / NO FINAL ROUTE SELECTED**

## 1. 解锁合规性

答案钥匙不是提前打开的。解锁前已单独冻结：

```text
scoring policy SHA256:
  d47be0cad2419174bd5775088c75582025ec15f6756cba3afd8ca345240148b4
unlock gate:
  25/25 PASS
answer key SHA256:
  6f2d377afa443aae9806b78ba883dc6a12aae9426964aa11e2d82efc3cebd156
answer key bytes:
  4971
```

解锁门禁审计：

```text
04_Local_Review_Audits/
ENZYMECAGE_M3_P1_2_1_ANSWER_KEY_UNLOCK_GATE_AND_SCORING_POLICY_FREEZE_LOCAL_AUDIT_2026-07-26.md
SHA256:
  2ef6c03965baf9bcf3847a0bd1764c1413c94f6af3d119214dda1e0976ed1252
```

解锁后没有修改评分政策、A/B/C 原始输出或 rank。

## 2. 评分产物与独立验证

机器评分报告：

```text
04_Local_Review_Audits/
ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_TARGET_SCORING_MACHINE_REPORT_2026-07-26.json
SHA256:
  43fbe058647eb66886267181cd0122fb00ad91cdd99dc416f0de7049edf3946d
```

独立验证报告：

```text
04_Local_Review_Audits/
ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_TARGET_SCORING_INDEPENDENT_VALIDATOR_REPORT_2026-07-26.json
SHA256:
  d42e376d977b0aee1d06977db0e230f8ecaa323243e303e55bca49199c8a975b
status:
  PASS_INDEPENDENT_RECOMPUTATION
checks:
  43/43 PASS
```

评分器反向测试：

```text
修改预测身份:
  PASS_DETECTED
修改答案钥匙身份:
  PASS_DETECTED
修改 rank:
  PASS_REJECTED
反转反应方向:
  PASS_NOT_EQUAL
product-only 冒充完整反应:
  PASS_REJECTED
修改冻结评分政策:
  PASS_DETECTED
total:
  6/6 PASS
```

评分器第二次完整运行与正式机器报告字节一致：

```text
BYTE_IDENTICAL_REPLAY:
  PASS
SHA256:
  43fbe058647eb66886267181cd0122fb00ad91cdd99dc416f0de7049edf3946d
```

## 3. 统一分母和匹配口径

```text
有效 case:
  6
非法输入 case:
  1
diagnostic product targets:
  7
```

`RP-P01` 有两个 diagnostic products，因此同时报告：

- case-level：一个 case 的任一 diagnostic product 被找回即为命中；
- product-level：7 个 diagnostic products 分别计数。

主评分使用 RDKit canonical isomeric SMILES 严格相等：

- 保留立体化学和形式电荷；
- 不删除 water、proton 或其他 currency molecules；
- 目标产物必须位于右侧；
- full reaction 比较左右两侧有向 molecule multiset；
- `RP-P06` 只承认 RHEA:52886 降解方向；
- product-only 不得记为 full-reaction hit。

## 4. 总结果

### 4.1 Case-level diagnostic-product recovery

| 路线/模型 | Top-1 | Top-3 | Top-5 | 说明 |
|---|---:|---:|---:|---|
| A BioTransformer | 不可评分 | 不可评分 | 不可评分 | 无合法 rank/confidence，且 1/26 产品不可解析 |
| B ChatGPT 用户标签 | 4/6 | 5/6 | 5/6 | product-only |
| B DeepSeek 用户标签 | 4/6 | 4/6 | 4/6 | product-only；原始 invalid-case error message 缺失 |
| B Qwen 用户标签 | 4/6 | 4/6 | 5/6 | product-only；whole-file prefix 偏差 |
| C-exact | 4/6 | 6/6 | 6/6 | 已知 Rhea 精确结构查表 |
| C-generic | 不评分 | 不评分 | 不评分 | `NOT_READY` |

### 4.2 Product-level diagnostic-product recovery

| 路线/模型 | Top-1 | Top-3 | Top-5 |
|---|---:|---:|---:|
| B ChatGPT 用户标签 | 4/7 | 5/7 | 5/7 |
| B DeepSeek 用户标签 | 4/7 | 4/7 | 4/7 |
| B Qwen 用户标签 | 4/7 | 4/7 | 5/7 |
| C-exact | 5/7 | 7/7 | 7/7 |

A 的可解析子集诊断为 case-level `4/6`、product-level `4/7`，但这不是正式
分数，原因见下一节。

### 4.3 非法输入

| 路线/模型 | RP-N01 |
|---|---:|
| A | 1/1 正确拒绝 |
| B ChatGPT | 1/1 正确拒绝 |
| B DeepSeek | 1/1 正确拒绝 |
| B Qwen | 1/1 正确拒绝 |
| C-exact | 1/1 正确拒绝 |

DeepSeek 的状态和空预测正确，但原始合同要求的 `error.message` 缺失；该偏差没有
因评分而被抹除。

## 5. Route A 裁定

答案解锁后的 RDKit 评分发现：

```text
raw product rows:
  26
RDKit parse:
  25/26
failed case:
  RP-P06
failed raw product:
  O=[N+]([O-])C1=CC=C[CH](=[CH]1O)O
failure:
  explicit valence for carbon greater than permitted
```

没有修复该字符串，也没有静默删除后给出正式成绩。Route A 正式裁定：

```text
Top-1/3/5:
  NOT_SCOREABLE_CONTRACT_INCOMPATIBLE
unranked strict product-set score:
  NOT_SCOREABLE_FAIL_CLOSED_RAW_PRODUCT_PARSE_FAILURE
full reaction:
  NOT_SCOREABLE_NO_FULL_REACTION
direct Rhea / EC / D4 pool:
  NOT_DIRECTLY_RECOVERABLE
```

仅用于排查的可解析子集命中：

| case | raw parse | strict diagnostic-product hit |
|---|---:|---:|
| RP-P01 | 5/5 | 否 |
| RP-P02 | 2/2 | 是 |
| RP-P03 | 6/6 | 是 |
| RP-P04 | 2/2 | 是 |
| RP-P05 | 6/6 | 是 |
| RP-P06 | 4/5 | 否 |

此外，A 仍缺完整 reaction、合法 confidence 和原生可解释排名。此次新发现的
1/26 parse failure 进一步确认不能把 A v0.5 写成统一合同 PASS。

## 6. Route B 分模型结果

三个模型没有合并重排。

| case | ChatGPT 首次命中 rank | DeepSeek 首次命中 rank | Qwen 首次命中 rank |
|---|---:|---:|---:|
| RP-P01 | 未命中 | 未命中 | 未命中 |
| RP-P02 | 1 | 1 | 1 |
| RP-P03 | 1 | 1 | 1 |
| RP-P04 | 1 | 1 | 1 |
| RP-P05 | 2 | 1 | 1 |
| RP-P06 | 1 | 未命中 | 4 |

因此：

- 三个模型都没有找回 Paraoxon 的冻结离子态 diagnostic products；
- ChatGPT 的 Top-3/5 为 5/6；
- Qwen 直到 Top-5 才因 RP-P06 rank 4 达到 5/6；
- DeepSeek 保持 4/6；
- 三者全部是 `product_only / partial_unbalanced`。

Route B 不能记：

```text
full-reaction recovery:
  NOT_SCOREABLE
direct Rhea recovery:
  NOT_DIRECTLY_RECOVERABLE
EC recovery:
  NOT_DIRECTLY_RECOVERABLE
D4 candidate-pool recovery:
  NOT_DIRECTLY_RECOVERABLE
```

这里的 4/6 或 5/6 只表示严格 diagnostic-product recovery，不表示完整生化
方程正确，也不表示能直接交给 EnzymeCAGE 排酶。

## 7. Route C-exact 完整结果

### 7.1 Target Rhea 排名

| case | 候选数 | diagnostic-product 首次命中 | 正确 directed Rhea rank | full reaction |
|---|---:|---:|---:|---:|
| RP-P01 | 1 | 1 | 1 | 命中 |
| RP-P02 | 1 | 1 | 1 | 命中 |
| RP-P03 | 1 | 1 | 1 | 命中 |
| RP-P04 | 1 | 1 | 1 | 命中 |
| RP-P05 | 5 | 2 | 4 | 命中 |
| RP-P06 | 3 | 2 | 2 | 命中 |

聚合：

```text
directed Rhea Top-1:
  4/6
directed Rhea Top-3:
  5/6
directed Rhea Top-5:
  6/6
full reaction strict structure match within returned Top-5:
  6/6
full reaction directed-Rhea ID match within returned Top-5:
  6/6
```

`RP-P05` 的 diagnostic product 在 rank 2 已出现，但完整目标
RHEA:36268 排在 rank 4。因此不能用 product Top-3 的 `6/6` 冒充 target Rhea
Top-3；真正的 directed-Rhea Top-3 是 `5/6`。

`RP-P06` 的 RHEA:52886 位于 rank 2，方向和完整反应均严格命中。

### 7.2 EC 映射

| case | 正确 Rhea | Rhea 140 EC |
|---|---|---|
| RP-P01 | RHEA:18054 | 3.1.8.1 |
| RP-P02 | RHEA:62381 | `null` |
| RP-P03 | RHEA:11313 | 3.8.1.8 |
| RP-P04 | RHEA:25186 | 3.8.1.5 |
| RP-P05 | RHEA:36268 | 1.14.13.178 |
| RP-P06 | RHEA:52886 | 1.7.1.16 |

```text
correct target with non-null frozen Rhea EC:
  5/6
correct target with frozen Rhea EC-null:
  1/6
```

这表示正确 Rhea 找回后的冻结映射可用性，不是一个独立的“EC 预测准确率”。
RP-P02 保持 Rhea `ec=null`，没有把外部 IUBMB/BRENDA 3.5.1.137 写回 Rhea。

### 7.3 D4-valid candidate-enzyme-pool recoverability

| case | Rhea 映射 UniProt UID 数 | D4-valid pool |
|---|---:|---:|
| RP-P01 | 0 | 0 |
| RP-P02 | 0 | 0 |
| RP-P03 | 1 | 1 |
| RP-P04 | 2 | 2 |
| RP-P05 | 1 | 1 |
| RP-P06 | 2 | 2 |

```text
correct-target D4-valid pool nonempty:
  4/6
```

这说明 C-exact 对 RP-P03—P06 可直接形成冻结 D4 域内的非空候选池；Paraoxon
和 Carbaryl 虽然正确 Rhea 均排第 1，但冻结 Rhea-to-UniProt 映射为空，因此
当前仍不能仅靠该链路形成候选酶池。

`4/6` 只表示“技术上能形成非空 D4 pool”，不表示正确酶一定在池中，更不表示
EnzymeCAGE 会把正确酶排第一。

## 8. 工程侧证据

前答案阶段已记录：

| 路线 | 核心运行 | wall | max RSS |
|---|---|---:|---:|
| A | 6 个有效 vendor case | 每 case 1.09—1.27 s | 177,820—197,652 KiB |
| B | 59 条 RDKit 技术验证 | 0.18 s | 61,460 KiB |
| B | 独立 validator | 0.16 s | 59,432 KiB |
| C-exact | 扫描 36,012 Rhea rows | 36.68 s | 79,016 KiB |
| C-exact | 独立 validator 重算 | 35.79 s | 78,404 KiB |

Route B 的模型生成时间、外部调用成本和人工收集分钟数没有可靠统一计量，不能
用 RDKit 后处理的 0.18 s 代替模型调用成本。

## 9. 科学结论与边界

1. C-exact 是本轮唯一能返回完整、可映射 Rhea 反应的路线；它在 Top-5 内对
   6/6 完整目标反应命中。
2. 这不是“新反应泛化 6/6”。六个有效底物本来就在冻结 Rhea 140 中，
   C-exact 的定位是已知反应查表 baseline。
3. Route B 展示了 product-level 生成价值，但目前输出合同无法直接进入 Rhea、
   EC 和候选酶池链路。
4. Route A v0.5 不仅缺 rank/confidence/full reaction，还出现 1/26 RDKit
   产品解析失败，当前不能进入统一评分或生产接入。
5. C-generic 尚未建立，所以本轮没有评价规则路线对真正未知反应的泛化能力。
6. 模型/版本名称仍是用户填写标签，不是平台 API attestation。

## 10. 最终裁定

```text
answer-key unlock:
  COMPLIANT
target scoring:
  COMPLETE
independent recomputation:
  PASS_43_OF_43
adversarial tests:
  PASS_6_OF_6
byte-identical scorer replay:
  PASS
Route A:
  FORMAL SCORE FAIL-CLOSED
Route B:
  PRODUCT-LEVEL SCORE COMPLETE
Route C-exact:
  FULL-REACTION SCORE COMPLETE
Route C-generic:
  NOT_READY
final production route:
  NOT SELECTED
teacher / user biological adjudication:
  STILL REQUIRED
```
