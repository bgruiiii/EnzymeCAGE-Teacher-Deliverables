# M3-P1-2.1 反应预测器三路线小试结果与路线裁定申请

日期：2026-07-26  
对应老师要求：
`TEACHER_REPLY_M3_NEXT_ROUND_STUDENT_PREREQUISITES_SUPPLEMENT_2026-07-24(1).md`
§2.1  
状态：**三路线小试与答案解锁后评分已完成；最终路线未选择；未修改
`reaction_prediction_node`**

## 一、这次请裁定什么

老师要求为“相似性不 OK → 预测”分支提供 A、B、C 三种路线之一，并统一满足：

```text
Input:
  substrate_smiles: str
Output:
  predicted_reactions: List[
    {reaction_smiles, confidence, provenance}
  ]
硬约束:
  完整 reaction SMILES 可由 RDKit 解析
  confidence ∈ [0,1]
  provenance 可追溯
```

我们先按同一份冻结输入，对三条路线做了小型 pilot。此举来自学生侧“先小试再由
用户与生物学老师选择”的决定，不改写为“老师要求三条路线全部实装”。

本文件申请裁定下一步采用哪条路线、是否允许分层组合，以及 Route B 的
product-only 输出能否进入下一阶段兼容性小试。裁定前不写活代码、不接入生产链。

## 二、评分门禁是否合规

答案钥匙仅在以下门禁全部通过后解锁：

```text
解锁前检查:
  25/25 PASS
答案钥匙 SHA256:
  6f2d377afa443aae9806b78ba883dc6a12aae9426964aa11e2d82efc3cebd156
独立重算:
  43/43 PASS
评分器反向测试:
  6/6 PASS
评分器完整复跑:
  与正式机器报告字节一致
```

解锁后没有修改评分政策、A/B/C 原始输出或 rank。评分采用 RDKit canonical
isomeric SMILES 严格相等；完整反应按有方向的左右两侧分子 multiset 比较；
product-only 不记为完整反应。

## 三、三路线结果

| 路线 | 目标产物找回 | 完整反应 / Rhea | 下游候选酶池 | 正式判断 |
|---|---|---|---|---|
| A BioTransformer ENVMICRO | 25/26 raw products 可解析；可解析子集仅作诊断为 4/6 case | 无完整反应、合法 rank、可用 confidence；RP-P06 有 1 条不可解析产物 | 不可直接恢复 | `NOT_SCOREABLE_CONTRACT_INCOMPATIBLE` |
| B ChatGPT 用户标签 | Top-1/3/5 = 4/6、5/6、5/6 | product-only，不可记 full reaction / Rhea | 不可直接恢复 | 有生成价值，但合同尚不闭合 |
| B DeepSeek 用户标签 | Top-1/3/5 = 4/6、4/6、4/6 | product-only；原始 invalid-case `error.message` 缺失 | 不可直接恢复 | 有生成价值，但合同尚不闭合 |
| B Qwen 用户标签 | Top-1/3/5 = 4/6、4/6、5/6 | product-only；存在 whole-file prefix 偏差 | 不可直接恢复 | 有生成价值，但合同尚不闭合 |
| C-exact 冻结 Rhea 140 精确结构查表 | diagnostic product Top-1/3/5 = 4/6、6/6、6/6 | 正确 directed Rhea Top-1/3/5 = 4/6、5/6、6/6；完整反应 Top-5 = 6/6 | D4-valid 非空 pool = 4/6 | 唯一能返回完整、可映射 Rhea 反应的路线 |
| C-generic 通用规则 | 未运行 | 未建立冻结规则资产 | 未评 | `NOT_READY` |

注：

1. 三个 B 模型的名称/版本是用户填写标签，不是平台 API attestation；三个模型
   分别评分，没有合并重排。
2. 六个有效底物本来就在冻结 Rhea 140 中，所以 C-exact 的 6/6 是已知反应
   查表 baseline，不是新反应泛化 6/6。
3. C-exact 对 Paraoxon 和 Carbaryl 均将正确 Rhea 排在 rank 1，但冻结
   Rhea→UniProt 映射为空；因此两例仍不能仅靠当前链路形成候选酶池。
4. `D4-valid pool 4/6` 只表示技术上形成非空池，不表示正确酶必在池中或会排第一。

## 四、当前不能直接宣布哪一路“已完成实装”

### Route A

当前版本既缺完整反应、可解释排名和合法 confidence，又出现 1/26 原始产物
RDKit 解析失败。不能通过后验补字段把它改写为统一合同 PASS。

### Route B

Route B 是三路中唯一展示“从底物生成新候选产物”能力的方向，但当前返回均为：

```text
substrate >> predicted_product
native_output_type:
  product_only
reaction_completeness:
  partial_unbalanced
```

它还不能直接恢复 Rhea、EC 或候选酶池，不能把 4/6 或 5/6 写成完整生化反应准确率。

### Route C

C-exact 对已收录 Rhea 反应有效，适合作为确定性守门层；但当目标反应不在冻结
Rhea 库中时，它本身不产生新反应。C-generic 尚未建立，不能宣称 Route C 已具有
未知反应预测能力。

所以当前诚实结论是：**三路小试已完成，但老师 §2.1 所要求的真实预测 fallback
尚没有一路可以无条件进入活代码。**

## 五、学生侧建议

建议采用分层方案，但必须先获得裁定并另冻最小合同：

```text
已知 Rhea 精确命中:
  C-exact 作为确定性守门层

检索真正失败:
  B 生成 product-only 候选
    -> Route C 相似反应检索
    -> Rhea / EC / UniProt 候选酶池
    -> D4-valid 域过滤

任何一步无合法候选:
  fail-closed
```

这项建议的边界：

- C-exact 不冒充“未知反应预测器”；
- B 的自报 confidence 只记
  `self_reported_uncalibrated`，不能解释为正确率；
- B 输出先做 RDKit、方向、重复项和 provenance 校验；
- 在下游兼容性小试通过前，不接 `reaction_prediction_node`；
- 组合路线需要新合同，不能把本文件当成实装授权。

如果老师要求 §2.1 必须只选一个“真正的预测工具”，学生侧倾向继续验证 **B**，
因为它至少覆盖了“库外生成”的业务语义；C-exact 保留为既有反应守门层，不作为
所选预测器。该倾向不等于已选择 B。

## 六、请刘老师 / 老师裁定的最小问题

1. 是否同意采用“C-exact 已知反应守门 + B 真实预测 fallback”的分层方向？
2. B 的 `substrate>>product` 是否允许进入一次受控的
   `product-only → Route C similarity → enzyme pool → D4-valid`
   下游兼容性小试，还是必须先输出完整生化反应才能继续？
3. 如果必须先输出完整反应，下一步优先选择哪一项：
   - 继续改造 Route B 的完整反应生成与校验；
   - 建立并冻结 C-generic 降解规则；
   - 更换 Route A 专业工具后重新小试？

## 七、裁定前保持锁定的事项

```text
[x] 不修改 reaction_prediction_node
[x] 不启动 M4b / M4c
[x] 不运行 M3-EXT 补资产或模型晋级
[x] 不把 C-exact 写成未知反应泛化
[x] 不把 B product-only 写成完整反应
[x] 不把 D4 非空池写成正确酶已找回
```

## 八、证据位置

完整自包含证据包：

```text
2026-07-26_M3_P1_2_1_Reaction_Predictor_Route_Adjudication/
```

入口：

```text
2026-07-26_M3_P1_2_1_Reaction_Predictor_Route_Adjudication/README.md
```

其中包含统一合同、冻结输入与答案、解锁前评分政策、三路线返回审计、人类可读
目标评分审计、机器评分 JSON、独立 validator JSON、SHA256 清单和独立提交前审计。

本申请不构成对 EnzymeCAGE v1、任一反应预测路线、任一 case 生物学有效性或
生产可用性的老师验收声明。
