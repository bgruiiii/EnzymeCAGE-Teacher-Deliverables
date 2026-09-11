# 老师侧回复：T4 18 条 blind 身份回签 + G5 公共契约裁定 + 下一步配合（2026-09-09）

- 日期：2026-09-09
- 收件：陈浩然（主线 + 微生物侧）
- 状态：正式生效
- 依据：对你 2026-09-08 三份返回物（T6 G5 字段恢复、T4 18 条 parent-only 回传、数据库/模型上云调研）的逐项审阅；与 09-08 T4 编排边界回签、09-08 G1—G5 契约回签合并执行

---

## 一、总体判定

你 09-08 三份返回物我已逐项审阅，判定如下：

1. G5 字段恢复是你本轮最扎实的动作：两条 canonical reaction 从冻结 M3 结果表精确恢复、
   UTF-8 原字符串重算 SHA 与既有记录 2/2 一致，且明确"不猜测、等老师裁定前不改 schema"。
   **数据定位问题就此关闭。**
2. T4 18 条 parent-only 回传符合我 09-08 要求：四字段齐全、盲隔离合规、未夹带任何 gold
   衍生字段。我据此回签锁定身份（见 §二）。
3. 上云调研诚实标注"下限 52.650 GiB、迁移版本与波次待老师决定"，没有擅自拍板。方向见 §五。

三项均未越权，诚信执行到位。

---

## 二、T4 正式 18 条 blind 输入身份 —— 回签锁定

1. 你回传的 archive 身份
   `enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_rerun1_20260804.tar.gz`
   （08-04 生成、08-07 由我在 A7/A8/A9 审计中接受冻结）与 08-07 A7 定案吻合
   （18 cases / 39 reactions / 39 products + blind 四件套）。
2. 你本次 18 行 CSV 仅含 `case_id / parent_name / parent_smiles / parent_smiles_rdkit_canonical`
   四字段，与 A7 冻结包内 blind parent 表逐项对应；未复制 reaction / product / gold / EC / evidence
   字段，盲隔离合规。
3. 我回签如下，本轮 T4 唯一输入身份锁定：

```text
T4_INPUT_STATUS = FROZEN_BY_TEACHER_COUNTERSIGN
唯一 parent 集合 = 你回传的 T4_FORMAL_18_PARENT_INPUTS.csv（以本文件 SHA256 锚定身份）
模型 = depending v3.2 + ECLIPSE（BioTransformer / enviFormer 沿用已录基线，不重跑）
gold = 预测端零接触
顺序 = 先冻结原始预测输出，再按冻结脚本 score_three_tool_predictions.py 评分
指标 = Hit@1/3/5/10 + MRR@10 + product recovery
```

4. 08-20 你欠我的「case 文件名补注」就此闭环。

---

## 三、G5 canonical SMILES 公共契约 —— 正式裁定

1. 数据定位已由你 2/2 恢复关闭，我确认无误：S1 / RHEA 11532、S2 / RHEA 46976
   的 `parent>>product` 字符串与 SHA 成对成立。
2. 正式公共 I/O 契约裁定如下，自本回复起生效：

```text
M3 recall 证据（retrieved 每条）必须成对携带：
  reaction_smiles    — canonical parent>>product 半反应
  reaction_sha256    — 64 位 hex（UTF-8 原字符串重算，不加换行）

二选一携带 = 不合规；只带 hash 不带 smiles = 漏带字段。
```

3. 边界说明：你此前 M3 recall 只带 `query_reaction_sha256`、漏带 `reaction_smiles`，属漏带字段，
   **源头不缺数据**。按本契约补齐即可，无需改动生产 schema 之外的任何东西。

---

## 四、G1—G4 裁定重申（并入 09-08 G1—G5 回签）

- **G1 拓扑**：老师侧已修复（检索/单步预测成功 → 直连酶池，多步桥降为旁路预留），
  你无需改图、返拓扑，只以修复后拓扑跑 T6-R3。
- **G2 公共键**：只认 T2B v3.2 `PredictedReaction`，删除本地旧版重复定义，禁止另起副本。
- **G3 数据源**：8001 为多余历史中间层，老师不重启、不重建；你直连 UniProt/KEGG REST
  （reviewed-only）+ 冻结 reviewed UID 映射表降级，移除对 8001 的一切依赖。**先回传自查再谈重跑。**
- **G4 表示**：host 证据来源与 `host_resolution` 只认大写 `UNRESOLVED` 等合法字面量，
  已纳入合法枚举 `UNIPROT_REVIEWED / KEGG_SUPPLEMENT / BACDIVE_OBSERVED / UNRESOLVED`。

---

## 五、数据库 / 模型权重上云 —— 方向裁定

你 52.650 GiB 下限盘点我已知晓。裁定：**当前不阻塞 T4/T6 主线。**

```text
1. 本轮不启动迁移执行，冻结你的 live 路径 / 容量盘点为后续方案底稿；
2. 迁移版本选择、波次切分、回滚与身份校验方案，归入独立的迁移立项清单，
   待 T6 整链终验通过后再单独评审；
3. 你继续做的只有：保持盘点表与晨羽 live 实际路径一致、标注每项体积来源，
   不搬运、不删改、不预占任何生产路径。
```

---

## 六、你下一步需配合的操作

| # | 事项 | 责任 | 返回物 / 说明 |
|---|---|---|---|
| 1 | M3 recall 补 `reaction_smiles` | 你 | 与 `reaction_sha256` 成对携带，见 §三 |
| 2 | 回传 8001 调用点 + entryType 自查 | 你 | 8 条 UNRESOLVED 各自来自哪段代码（有无真调 8001）+ 这 8 个酶 UID 的 UniProt `entryType` 清单 |
| 3 | 对齐 T2B v3.2 PredictedReaction | 你 | 删本地旧版引用，见 §四 G2 |
| 4 | 统一 UNRESOLVED 字面量 | 你 | 禁止 N/A、空串、小写 unresolved，见 §四 G4 |
| 5 | T4 盲测启动 | 你 | 回签后即可启动：depending v3.2 + ECLIPSE，先冻结原始输出再评分，指标见 §二.3 |
| 6 | 以修复后拓扑跑 T6-R3 | 你 | 老师侧已修 G1 拓扑并推送到 depending `main`，你拉取后按节点契约跑，不改图、不重排 |
| 7 | 上云盘点保持只读 | 你 | 见 §五.3，不搬运、不删改 |

---

## 七、红线（不可让步）

```text
1. 编排（节点拆分、合并、编排方式、拓扑）归老师侧，你只按契约接线；
2. 不得另起 PredictedReaction / IntentClassification 旧版副本；
3. 不得重启或重建 8001 服务，不得再指向 127.0.0.1:8001；
4. host 证据来源与 host_resolution 只认大写 UNRESOLVED 等合法字面量；
5. retrieved 证据必须成对携带 reaction_smiles + reaction_sha256；
6. 封禁用语继续生效（无 hard reject / trait_score / uncalibrated confidence）。
```