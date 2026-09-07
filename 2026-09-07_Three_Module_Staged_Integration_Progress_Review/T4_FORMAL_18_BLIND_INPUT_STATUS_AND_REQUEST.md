# T4正式18条blind输入状态与请求

日期：2026-09-07

## 当前状态

```text
T4_STATUS = BLOCKED_INPUT_MISSING
STUDENT_EXECUTION_SKIPPED = false
FORMAL_INPUT_IDENTITY_AVAILABLE = false
SELF_SELECTED_18_USED_AS_REPLACEMENT = false
```

T4没有执行的原因不是学生侧未准备评分流程，而是当前没有定位到“老师本轮指定的正式18条blind输入冻结包”的
唯一文件身份。正式比较至少需要同一输入、答案隔离和固定评分口径，不能仅凭“也是18条”就替换。

## 已有但不能自动替代的材料

仓库已有2026-08-04的18条污染物小测试gold/schema/scorer。这是一份历史测试资产，可用于追溯旧评估，但目前
没有权威证据证明它等同于本轮T4要求的正式18条输入，也不能确认是否满足本轮depending v3.2与ECLIPSE同口径
比较所需的parent集合、版本和盲隔离要求。

学生侧另在构建NON-BBD外部文献验证集，用于提前检查外部泛化。该集合尚处于文献核证和用户科学复核阶段，且
明确定位为附加内部验证，永不替代老师T4。

## 请黄老师确认或提供

请黄老师任选一种方式明确：

1. 提供本轮T4正式18条blind parent输入文件及其SHA256；或者
2. 明确授权使用仓库2026-08-04历史18条中的哪一个精确输入文件，并确认其为本轮T4唯一口径；或者
3. 提供新的18条名单及blind/gold隔离要求。

建议正式输入至少包含：

```text
case_id
parent_name
parent_smiles
parent_smiles_rdkit_canonical（如已冻结）
```

同时请给出：输入文件bytes/SHA256、是否允许公开名称、目标模型名单、Top-K上限、答案文件由谁保管。

## 输入到位后的执行承诺

输入身份确定后，我们会：

```text
只把blind parent输入发送预测端；
depending v3.2与ECLIPSE等使用同一parent集合和同一Top-K；
先冻结原始输出，再在本地解锁答案评分；
报告Hit@1/3/5/10、MRR@10和product recovery；
保留空预测和失败案例，不从分母删除；
完成本地独立重算后再请老师裁定模型角色。
```

在T4和老师复核之前，depending v3.2不会被提升为默认主基线。
