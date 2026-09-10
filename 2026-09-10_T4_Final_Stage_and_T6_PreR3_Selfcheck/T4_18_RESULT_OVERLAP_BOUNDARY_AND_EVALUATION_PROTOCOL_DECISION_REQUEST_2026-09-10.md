# 给黄老师的 T4 18 题结果、重合边界与评测协议裁定请求（T4-R2 纠正草稿）

- 状态：**本地草稿 — 未发送 / 未上传。** 仅作为 T4-R2 本地审计证据包的一部分返回；是否发送由您决定。
- 本草稿**不作任何模型角色结论**，**不推荐选项 A 或选项 B**。
- 相对 R1 草稿的变化：重合主事实前置为 13/39 正确 parent-product 对；逐资产矩阵已按
  asset-local 规则重派生；删除"运行时查询外部 enviPath 知识库"的错误说法；opaque ranker
  明确为 UNKNOWN_FOR_ALL_18 并与"无可审计 locator"分开；披露 fold6/fold8 提示词 SHA 转录纠正。

## 1. 现有四工具指标（macro/micro 口径已纠正；3 条 invalid 但指标不变）

评分为冻结脚本在冻结 normalized 上的重放；depending 侧唯一改动是 3 行
`ok -> invalid_smiles` 规范化状态纠正（SPD-BBD-cbf rank10、SPD-BBD-tol rank9/10），
原/纠正两版重放的逐 case、逐 product 与全部数值指标**完全一致**
（NORMALIZATION_CORRECTION_METRIC_INVARIANCE.json）。

| 工具 | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | macro（18 例每例 product recall@10 等权均值） | micro（recovered/39 接受产物） |
|---|---|---|---|---|---|---|---|
| depending_v3_2（runtime） | 10/18 | 12/18 | 14/18 | 15/18 | 0.6366 | 0.575 | 19/39 = 0.487179 |
| eclipse_predec_bbd_finetuned_10fold_aggregated（runtime） | 6/18 | 13/18 | 15/18 | 16/18 | 0.5343 | 0.6028 | 21/39 = 0.538462 |
| biotransformer_envmicro（08-04 冻结基线重放） | 9/18 | 13/18 | 16/18 | 16/18 | 0.6194 | 0.6528 | 20/39 = 0.512821 |
| enviformer_latest（08-04 冻结基线重放） | 0/18 | 1/18 | 1/18 | 1/18 | 0.0278 | 0.0185 | 1/39 = 0.025641 |

口径：hit@k 按 **case**（共 18）计；macro 为每例 product recall 等权均值；micro 为
recovered/39。macro 小数（如 0.575）不得叙述为 "recovered/39"。

## 2. depending"见过答案"的主事实：13/39 正确 parent-product 对在 corpus 共同出现

39 个正确 (parent, product) 半反应对中，**13/39** 的两侧同时出现在 corpus_v1.jsonl 的**同一条
具体记录**里（P2_EXACT_PARENT_PRODUCT_PAIR_SEEN；每条都有可回查 locator，见
DEPENDING_EXACT_MATCH_EVIDENCE_LOCATORS.csv 16 行，R2 已逐行回查原语料行通过）。这是最贴近
"模型见过这个答案吗"的可审计数字。

## 3. 补充严格口径：完整生化两侧集合 P1=0/39

若要求 canonical 后**两侧集合完全相等**（corpus 记录通常还带水/离子/辅因子组分），则
P1_EXACT_REACTION_SEEN=0/39。该 0/39 只是更严格的另一集合定义，**不**否定第 2 节的 13/39；
两个口径现在分列于 DEPENDING_39_GOLD_REACTION_OVERLAP_BY_ASSET_CORRECTED.csv
（asset-local 字段）与 DEPENDING_39_GOLD_REACTION_GLOBAL_LAYERED_STATUS.csv（39 行全局层）。

## 4. 其余可审计暴露锚点

```text
15/18 题目 parent 在 corpus 具体记录 reactant 侧出现（dmta/gly/mal/pthn 仅 educt-only 记录；pha/pyr/tbp2 未出现）
16/39 正确产物曾在 corpus 任一记录 product 侧出现（P3=16）
15 个 top10 首次命中中 7/15 能连到具体 corpus pair locator；6 为 parent-side-only；2 为 template-only；3 例无 top10 命中
逐资产纠正后分布（reaction）：corpus P2=13/P3=3/P4=16/P6=7；donor P4=31/P6=8；
templates.json P5=29、templates.tsv.gz P5=8、templates_implicitH P5=26（其余 P6）；每 ranker OPAQUE=39
```

## 5. envipath 语义（R1 错误已撤回）与 ranker UNKNOWN

depending engine B 的 envipath 规则**来自本地冻结文件**
（data/hfix/templates_implicitH.jsonl，sha256=3c3db55c...；
reaction_v3/data/lib_envipath/templates.tsv.gz，sha256=19ac04ca...；均与 T2B-R4 运行时资产门
记录一致）。本次运行**无外部 enviPath 知识库 HTTP 查询**
（runtime_external_envipath_dependency=false）；R1 中"query an external enviPath knowledge base
at runtime"一句为错误描述，已撤回。`source_tag=envipath` 不自动判泄漏，`source_tag=retrieval`
也不自动判无泄漏，分类只看 locator。三个 LightGBM ranker 参数文件无可恢复训练行身份：
`ranker_training_overlap=UNKNOWN_FOR_ALL_18`（对全部 18 题未知，**不是**零重合）；这与
"无可审计 locator 的案例=0/18"是两回事，R1 摘要中混写的 q6 字段已拆分替换。

## 6. ECLIPSE：全 fold 聚合、训练重合已证实、非严格 OOF

ECLIPSE 用全部 10 个 fold 的聚合预测（ALL_FOLD_IN_DOMAIN_ENSEMBLE_RUNTIME_BLIND）。
390 个 gold-reaction×fold 单元中 **TRAIN=190**（VAL=35 / TEST=25 / NONE=140）；180 个
parent×fold 单元 TRAIN=142 / VAL=21 / TEST=17，18/18 题的 parent 都有 TRAIN 暴露；冻结逐 fold
预测给出 113/390 命中单元。fold0 已用本地相同 SHA split 文件独立复现（20/3/2/14）；fold1-9 原
split 未装包，保留"不能独立重放"限制。**这不是 strict OOF**（ECLIPSE_STRICT_OOF=false）。
fold6/fold8 的 T4-R1 提示词值各抄错 1 个十六进制字符，实际冻结 split SHA 以首包
RUNTIME_MODEL_AND_SCRIPT_IDENTITIES.csv 为准（fold6 b17ba7ae787c...、fold8
ecdd54c591cb...）；该差错只属提示词转录，不影响 390/180 矩阵。

## 7. 当前评测的有效边界

```text
RUNTIME_GOLD_ZERO_CONTACT = PASS_WITH_NO_OPEN_TRACE_LIMITATION（gold 未进入预测阶段；ACCESS 为事后重建非实时开放 trace）
STRICT_UNSEEN_BLIND_EVALUATION = NOT_ESTABLISHED（depending 语料重合已证实 + ECLIPSE 全 fold TRAIN 暴露已证实）
CURRENT_METRICS = VALID_RUNTIME_BLIND_IN_DOMAIN_RECOVERY（指标有效，但只能作为运行时盲测的 in-domain recovery 口径）
```

## 8. 模型角色

本包不对 depending_v3_2 / eclipse_predec_bbd_finetuned_10fold 谁作主模型、谁作对照作任何结论
或推荐；MODEL_ROLE_DECISION=AWAITING_HUANG_TEACHER_REVIEW。

## 9. 中立请求裁定（两选项，无倾向）

- **选项 A**：接受当前口径（runtime-blind in-domain recovery + 上述重合边界披露）继续审阅与角色
  讨论，不追加新计算。
- **选项 B**：下发严格 held-out / OOF 评测协议（指定允许 fold、聚合规则、评测入口），执行器按
  协议另行执行；本协议不由执行器自行设计。

在您裁定前，本草稿不发送、不上传；本T4任务不进入T6、也不改变T6模型角色；T6按独立老师合同继续推进，不以本T4 A/B裁定为前置门；无任何git push。
