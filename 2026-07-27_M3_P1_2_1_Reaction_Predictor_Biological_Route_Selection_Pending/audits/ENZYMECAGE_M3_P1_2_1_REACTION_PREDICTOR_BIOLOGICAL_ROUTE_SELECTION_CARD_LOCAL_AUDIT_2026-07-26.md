# M3-P1-2.1 反应预测器 A/B/C 详细选择卡本地独立审计

审计日期：2026-07-26（Asia/Shanghai）  
审计对象：
`M3_P1_2_1_REACTION_PREDICTOR_BIOLOGICAL_ROUTE_SELECTION_CARD_2026-07-26.md`  
对象 SHA256：
`f4d9e23ecec8d6ee78d02607c9705e8a8246a79237142a76b87a79d3d211b0b9`  
结论：**PASS FOR LIU-TEACHER A/B/C SELECTION / R1-R2 CLEARLY NON-EXECUTED / NO IMPLEMENTATION AUTHORIZATION**

## 1. 本次纠正内容

旧选择框架曾把学生侧组合构想 R1/R2/R3 错写成刘老师主选择。该框架已经撤回。

本版恢复黄老师 2026-07-24 §2.1 的正式主选择：

```text
A:
  专业反应预测工具
B:
  LLM 生成候选 reaction SMILES + 有效性校验
C:
  规则库/已知降解路径模板
```

选择卡中刘老师勾选区只包含 A/B/C。R1/R2 只位于文末附加建议区，并明确：

```text
提出方:
  学生侧/Codex
已执行:
  no
已评分:
  no
老师已批准:
  no
可替代 A/B/C:
  no
```

旧 R3 不再保留为独立编号；“建设 C-generic”回到正式选项 C 的下一步含义。

## 2. 统一合同一致性

选择卡复述的老师合同与 2026-07-24 权威文档一致：

```text
Input:
  substrate_smiles: str
Output:
  List[{reaction_smiles, confidence, provenance}]
硬门:
  RDKit parse
  confidence in [0,1]
  provenance
```

选择卡进一步说明最终需要完整 reaction，而本轮 A/B 的 product-only 输出不能冒充
完整反应。该说明与既有评分政策一致。

## 3. 实测数字交叉核对

### 3.1 门禁

```text
answer-key unlock:
  25/25 PASS
independent recomputation:
  43/43 PASS
adversarial scorer tests:
  6/6 PASS
```

与正式目标评分审计一致。

### 3.2 Route A

选择卡所列：

```text
valid cases executed:
  6/6
raw products:
  26
RDKit parse:
  25/26
diagnostic parseable-subset case hit:
  4/6
diagnostic parseable-subset product hit:
  4/7
formal score:
  NOT_SCOREABLE_CONTRACT_INCOMPATIBLE
```

与 A v0.5 返回审计和目标评分审计一致。选择卡没有把可解析子集 4/6 写成正式成绩，
也没有把 BioTransformer v0.5 的失败外推为所有专业工具均失败。

### 3.3 Route B

选择卡所列：

```text
predictions:
  24 + 9 + 26 = 59
RDKit parse:
  59/59
substrate retained on left:
  59/59
ChatGPT-labelled Top-1/3/5:
  4/6, 5/6, 5/6
DeepSeek-labelled:
  4/6, 4/6, 4/6
Qwen-labelled:
  4/6, 4/6, 5/6
```

与技术验证和目标评分审计一致。选择卡明确这些是 diagnostic-product case-level
成绩，不是 full reaction、Rhea、EC 或正确酶成绩。

Gemini 被写为格式不合规淘汰，未伪造其评分。模型版本继续标注为用户标签而非 API
attestation。

### 3.4 Route C

选择卡所列 C-exact：

```text
raw Rhea rows:
  36,014
excluded unparsable:
  2
searchable:
  36,012
directed Rhea Top-1/3/5:
  4/6, 5/6, 6/6
full reaction Top-5:
  6/6
target non-null frozen Rhea EC:
  5/6
D4-valid pool nonempty:
  4/6
```

与 C rerun2 返回审计和目标评分审计一致。选择卡没有：

- 把 C-exact 写成未知反应预测；
- 把 diagnostic product Top-3 `6/6` 冒充 directed Rhea Top-3；
- 把外部 EC 3.5.1.137 写回 Carbaryl 的冻结 Rhea EC-null；
- 把 D4 非空池 4/6 写成正确酶找回 4/6。

C-generic 被如实标作 `NOT_READY / 未运行 / 未评分`。

## 4. 优缺点与选择后动作审计

每条路线均包含：

```text
本轮实际测试对象
实测成绩
可证明能力
不能证明的能力
主要优点
主要缺点/风险
如果选择该路线，下一步做什么
生产锁
```

A 的下一步没有要求复用已失败的 BioTransformer v0.5；B 的下一步要求新 blind set 和
完整反应门；C 的下一步明确指向 C-generic 资产建设，C-exact 只作已知反应守门。

## 5. 学生推荐身份审计

选择卡推荐 B 作为下一阶段研究方向，理由建立在已完成结果上：

```text
A current tool:
  contract incompatible
B:
  only tested route with generative product behavior
C-exact:
  known-reaction lookup only
C-generic:
  not ready
```

推荐没有被写成刘老师已选择、黄老师已授权或 production ready。

## 6. R1 工程逻辑与边界

R1 为：

```text
B product-only
  -> S >> P
  -> directed two-sided local Rhea similarity
  -> frozen full Rhea reference reaction
```

选择卡明确 `S >> P` 是 partial/unbalanced reaction，不是完整生化反应；只允许
正向的 reactant-to-reactant 与 product-to-product 比较，不允许用
`max(S_direct, S_reverse)` 将反向反应误作降解方向。

只有桥接出的冻结完整 Rhea reference reaction 才可进入下游。真正库外反应继续
fail-closed。因此 R1 是已知反应桥接兼容性建议，不是 unknown full-reaction
fallback。

## 7. R2 工程逻辑与边界

R2 为新的 B 完整反应 blind pilot，要求：

```text
RDKit
元素/原子守恒
形式电荷
方向
底物保留
模型版本
provenance
confidence 语义
```

R2 最直接测试老师原始完整 reaction contract，但当前尚未执行，不能赋予任何成功率。

学生侧建议若选 B 则 R2 优先、R1 作为附加兼容性实验；该顺序被明确标记为建议，
不是当前实测结论。

## 8. 文件与引用一致性

已同步纠正：

```text
M3_NEXT_ROUND_PRETEACHER_MASTER_INDEX_AND_DECISION_STATUS_2026-07-26.md
M3_NEXT_ROUND_HUANG_TEACHER_FIXED_ADJUDICATION_AND_MINIMUM_AUTHORIZATION_CARD_2026-07-26.md
M3_2026_07_23_24_TEACHER_TASK_LIST_ITEM_BY_ITEM_RESPONSE_AND_EVIDENCE_LOCATOR_2026-07-26.md
```

上述文件现在均以 A/B/C 作为刘老师主选择。黄老师 RP 卡仅把 R1/R2 作为 B 路的
未测试学生建议，不会自动授权 R1。

## 9. 最终结论

```text
formal main choice restored to A/B/C:
  PASS
A/B/C evidence numbers cross-checked:
  PASS
capability boundaries:
  PASS
R1/R2 marked student-proposed:
  PASS
R1/R2 marked not executed/not scored:
  PASS
production authorization:
  NO
Liu-teacher selection still required:
  YES
Huang-teacher pilot authorization still required:
  YES
```

本选择卡可以交刘老师阅读并只勾选 A/B/C。任何后续 pilot 仍需独立冻结合同并由
黄老师明确授权。
