# M3-P1-2.1 答案钥匙解锁门禁与评分政策冻结本地审计

审计日期：2026-07-26（Asia/Shanghai）  
审计阶段：答案钥匙内容读取前  
结论：**PASS — ANSWER KEY UNLOCK AUTHORIZED**

## 1. 审计边界

本审计只核验：

1. 统一合同、输入、A/B/C 返回包和既有独立审计的身份；
2. 三个返回包的安全成员与内部 `MANIFEST.sha256`；
3. Rhea、EC、UniProt 与 D4 UID 可用域资产身份；
4. 答案钥匙的 SHA256 和字节数，不解析 JSON 内容；
5. 评分规则是否在答案解锁前明确冻结。

截至本审计通过时：

```text
answer key content:
  NOT READ
answer key JSON:
  NOT PARSED
answer key identity-only hash:
  VERIFIED
```

## 2. 冻结评分政策

文件：

```text
01_Path_Contract_Objective/
M3_P1_2_1_Reaction_Predictor_Pilot_Contract_2026-07-24/
M3_P1_2_1_ANSWER_KEY_UNLOCK_AND_SCORING_POLICY_FREEZE_2026-07-26.json
```

身份：

```text
SHA256:
  d47be0cad2419174bd5775088c75582025ec15f6756cba3afd8ca345240148b4
frozen_at_utc:
  2026-07-26T08:50:58Z
answer_key_content_access_at_freeze:
  NOT_READ_OR_PARSED
```

该文件从本审计通过后保持只读语义，不因评分结果修改。允许的后续工作只包括：

- 按答案钥匙实际字段名读取已冻结语义；
- 实现和运行确定性评分器；
- 披露不可评分项和分子/分母。

禁止：

- 修改 A/B/C 原始预测；
- 修改 rank；
- 给 A 路补造 rank/confidence；
- 合并 B 路三个模型后重排；
- 把 product-only 当完整反应；
- 查看答案后修改评分语义。

## 3. 三路身份门禁

| 路线 | 返回 archive SHA256 | 既有审计 SHA256 | 状态 |
|---|---|---|---|
| A | `48f8253b...2b8a` | `409db5ad...1225` | raw vendor PASS；统一排名合同不兼容 |
| B | `4ce4b395...3856` | `b5db2d8d...51c8` | 59 条技术验证 PASS；三个模型分开评分 |
| C-exact | `2998bee8...ffba` | `2ff3de4a...b8c4` | 12 条技术验证 PASS |
| C-generic | 无正式输出 | 不适用 | `NOT_READY / NOT_SCORED` |

返回包安全与内部清单复核：

```text
A:
  82 members
  manifest 68/68 PASS
B:
  36 members
  manifest 28/28 PASS
C-exact:
  85 members
  manifest 70/70 PASS

single root:
  3/3 PASS
duplicate members:
  0
absolute / parent-traversal / backslash paths:
  0
symlink / hardlink / device / FIFO:
  0
```

## 4. 答案钥匙封存身份

只做流式 SHA256 和 `stat`，未调用 JSON parser：

```text
expected SHA256:
  6f2d377afa443aae9806b78ba883dc6a12aae9426964aa11e2d82efc3cebd156
observed SHA256:
  6f2d377afa443aae9806b78ba883dc6a12aae9426964aa11e2d82efc3cebd156
expected bytes:
  4971
observed bytes:
  4971
parse_performed:
  false
result:
  PASS
```

## 5. 下游映射资产门禁

| 资产 | SHA256 | 结果 |
|---|---|---|
| `rhea-reaction-smiles.tsv` | `34f7fb5e...e02` | PASS |
| `rhea-directions.tsv` | `a10e6102...71b` | PASS |
| `rhea2ec.tsv` | `5a90d95d...7d44` | PASS |
| `rhea2uniprot_sprot.tsv` | `89efa346...827e` | PASS |
| `rhea2uniprot_trembl.tsv.gz` | `efd3c540...73a0` | PASS |
| `uid_asset_availability.csv.gz` | `28a1f881...e829` | PASS |

D4 完整资产 UID 复算：

```text
expected:
  107705
observed:
  107705
result:
  PASS
```

## 6. 评分口径冻结

```text
Route A:
  只评未排序 raw product set recovery
  Top-1/3/5 = NOT_SCOREABLE_CONTRACT_INCOMPATIBLE

Route B:
  ChatGPT / DeepSeek / Qwen 分别按冻结 rank 评 Top-1/3/5
  不做跨模型合并或重排

Route C-exact:
  按 numeric directed Rhea ID 升序评 Top-1/3/5

Route C-generic:
  NOT_READY / NOT_SCORED

strict product:
  RDKit canonical isomeric SMILES 精确相等
  目标必须位于右侧

full reaction:
  分方向比较左右两侧 canonical molecule multiset
  不删除 currency molecule
  不允许反向等价
  product-only 不合格

RP-P06:
  只承认 RHEA:52886 降解方向

candidate pool:
  正确 directed Rhea -> master Rhea -> UniProt UID
  -> complete_d4_enzyme_assets=True 交集
  非空只表示技术上可进入 D4 排序域，不代表正确酶存在或排第一
```

## 7. 门禁程序与复核结果

验证器：

```text
custom/scripts/
validate_enzymecage_m3_p1_2_1_unlock_gate_20260726.py
SHA256:
  6abacd10d059e4fd92351253c00f80584146f944dea197848c686f758f767c5a
```

第一次运行因验证器把 manifest 的 `./relative/path` 重复拼接顶层目录而
fail-closed。该次没有解析答案钥匙，也没有改变评分政策。只修复路径规范化后从头
重跑，结果：

```text
checks:
  25
pass:
  25
answer_key_content_parsed:
  false
gate_status:
  PASS_ANSWER_KEY_UNLOCK_AUTHORIZED
```

## 8. 最终裁定

三路正式采用的原始产物与独立审计均已冻结，评分语义也已在答案内容读取前固定。
A 路的合同不兼容被作为正式结果保留，不会用后验伪造字段修补；它不阻止 B 和
C-exact 进入第二阶段评分。

因此：

```text
ANSWER KEY UNLOCK:
  AUTHORIZED
TARGET SCORING:
  AUTHORIZED UNDER FROZEN POLICY ONLY
FINAL ROUTE SELECTION:
  NOT AUTHORIZED BY THIS GATE
```
