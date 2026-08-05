# M3 2026-08-03 老师清单逐项回应

日期：2026-08-04  
状态：最终逐项回应；已 GitHub 同步并完成远端链接检查。
回应对象：黄老师 2026-08-03《M3 三个技术问题综合回复》裁定与下一步清单，以及其对 07-23/07-24 前置输入的补充要求。

## 1. 先给老师看的结论

本轮清单中，除弓师兄模型返回后的 F6 三工具横向评分闭环外，我们能自行完成的内容已经完成到可审计状态，并已统一 GitHub 同步。

当前状态可概括为：

```text
已完成:
  F1 P2Rank 表述修复；
  F2/07-22 原件和 Q1/Q2/Q3 证据包整理；
  F3 本地 Rhea 基线 missing-pocket / missing-D4 缺口估算；
  F4 Q2 行号和 ESM-2 3B 配置来源修复；
  F5 BioTransformer ENVMICRO 源码摘录和 jar 身份证据；
  D5 MetaTraits 新合同预调研再确认；
  ⑤⑥⑦、D1-D8、2.2 confidence 旧裁定和本轮再审计；
  Task 7 TraitValue not_applicable 契约再确认；
  M3-EXT 候选二次裁定材料整理；
  18 条污染物 gold standard / blind input / schema / scorer 固化；
  BioTransformer ENVMICRO 与 enviFormer latest 的 18 条 replay scoring。

等待项:
  F6 三工具横向比较仍等待弓师兄模型输出；
  M3-EXT 是否晋级正式挑战案例、是否补 D4/Route-B/Route-C 资产，仍等待老师二次裁定；
  M4b / M4c、OnDemand D4 工具化和正式 reaction_prediction fallback 引擎选型仍按老师后续合同裁定推进。
```

本文件及所列交付包已统一 push；文内 GitHub 链接已完成远端打开检查。

## 2. 本轮新增/整理的主要入口

酶侧 teacher-deliverables 仓库：

```text
https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables
```

本轮已新增/更新入口：

- 三个技术问题修复与证据包：  
  `2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/`
- 三个技术问题修复与证据包索引：  
  `M3_THREE_TECHNICAL_QUESTIONS_CORRECTION_AND_EVIDENCE_INDEX_2026-08-04.md`
- 18 条污染物 gold/schema/scorer 可审阅包：  
  `2026-08-04_M3_P1_2_1_Small_Pollutant_Gold_Standard_Schema_Scoring_Freeze/`
- 本最终逐项回应：  
  `M3_2026_08_03_TEACHER_REQUIREMENTS_FINAL_RESPONSE_2026-08-04.md`

微生物侧 teacher-deliverables 仓库：

```text
https://github.com/bgruiiii/EnzymeCAGE-MetaTraits-Teacher-Deliverables
```

本轮需要重新指路的入口：

- D5 新合同预调研再确认索引：  
  `METATRAITS_D5_2026_08_03_TEACHER_LIST_RECONFIRMATION_INDEX_2026-08-04.md`
- 菌层 D1-D8 / confidence / Task7 再确认包：  
  `2026-08-04_M3_Bacteria_Layer_D1_D8_Confidence_and_Task7_Reconfirmation/`
- 菌层再确认根索引：  
  `M3_2026_08_03_METATRAITS_REQUIREMENTS_RECONFIRMATION_INDEX_2026-08-04.md`
- Task 7 contract：  
  `TRAIT_VALUE_NOT_APPLICABLE_SCHEMA_CONTRACT.md`
- D4 soft 生物学决定记录：  
  `2026-07-27_M3_D4_Wastewater_Trait_Soft_Policy_Decision/`

## 2.1 逐项 GitHub 链接索引（已推送并检查通过）

为避免再次出现“已完成但老师没看到路径”的问题，本轮正式发送时建议黄老师优先看本节链接。

酶侧：

| 对应项 | GitHub 链接 |
|---|---|
| 本逐项回应 | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/M3_2026_08_03_TEACHER_REQUIREMENTS_FINAL_RESPONSE_2026-08-04.md |
| F1/F2/F3/F4/F5 技术问题修复与证据包 | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence |
| F1/F2/F3/F4/F5 技术问题修复与证据包索引 | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/M3_THREE_TECHNICAL_QUESTIONS_CORRECTION_AND_EVIDENCE_INDEX_2026-08-04.md |
| F3 本地 Rhea 基线缺口估算 | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/M3_F3_LOCAL_ENZYME_ASSET_POOL_AND_EC_EXPANSION_GAP_AUDIT_2026-08-04.md |
| F5 BioTransformer source/jar 证据 | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/M3_Q3_BIOTRANSFORMER_ENVMICRO_SOURCE_AND_JAR_IDENTITY_EVIDENCE_2026-08-04.md |
| 07-22 原件 | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md |
| 18 条污染物 gold/schema/scorer 包 | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-08-04_M3_P1_2_1_Small_Pollutant_Gold_Standard_Schema_Scoring_Freeze |
| 18 条污染物 gold/schema/scorer README | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/2026-08-04_M3_P1_2_1_Small_Pollutant_Gold_Standard_Schema_Scoring_Freeze/README.md |
| M3-EXT shortlist | https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/blob/main/M3_EXT_CANDIDATE_SHORTLIST_v0.md |

微生物侧：

| 对应项 | GitHub 链接 |
|---|---|
| MetaTraits / 菌层 2026-08-03 再确认索引 | https://github.com/bgruiiii/EnzymeCAGE-MetaTraits-Teacher-Deliverables/blob/main/M3_2026_08_03_METATRAITS_REQUIREMENTS_RECONFIRMATION_INDEX_2026-08-04.md |
| D5 新合同预调研再确认索引 | https://github.com/bgruiiii/EnzymeCAGE-MetaTraits-Teacher-Deliverables/blob/main/METATRAITS_D5_2026_08_03_TEACHER_LIST_RECONFIRMATION_INDEX_2026-08-04.md |
| D5 新合同预调研包 | https://github.com/bgruiiii/EnzymeCAGE-MetaTraits-Teacher-Deliverables/tree/main/2026-07-24_MT_D5_New_Contract_Reaudit_and_Resubmission |
| 菌层 D1-D8 / confidence / Task7 再确认包 | https://github.com/bgruiiii/EnzymeCAGE-MetaTraits-Teacher-Deliverables/tree/main/2026-08-04_M3_Bacteria_Layer_D1_D8_Confidence_and_Task7_Reconfirmation |
| Task 7 TraitValue contract | https://github.com/bgruiiii/EnzymeCAGE-MetaTraits-Teacher-Deliverables/blob/main/TRAIT_VALUE_NOT_APPLICABLE_SCHEMA_CONTRACT.md |
| Task 7 自包含交付包 | https://github.com/bgruiiii/EnzymeCAGE-MetaTraits-Teacher-Deliverables/tree/main/2026-07-24_Task7_TraitValue_Not_Applicable_Contract |
| D4 soft 生物学决定记录 | https://github.com/bgruiiii/EnzymeCAGE-MetaTraits-Teacher-Deliverables/tree/main/2026-07-27_M3_D4_Wastewater_Trait_Soft_Policy_Decision |

## 3. 对 F1-F6 逐项回应

| 项 | 老师要求 | 当前状态 | 结果和证据 |
|---|---|---|---|
| F1 | 修复 Q1 §1.2 P2Rank 表述，说明 `mix-af-p2rank` 出处 | 已完成 | 已更正为：官方公开 EnzymeCAGE commit `255a05e167aabc70f6c0322a00702cdc9d6ebfbc` 存在完整 P2Rank 脚本链；路线 C 是官方 P2Rank pocket workflow 的复现，在本项目证据分级中作为 predicted-pocket fallback / 对照。`mix-af-p2rank` 出自官方 `config/infer/*.yaml` 中的 feature asset 命名。 |
| F2 / ① | Q1 audit、Q2/Q3 文档、07-22 原件同步 teacher-deliverables | 已完成并已 push | 包路径：`2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/`。07-22 原件 SHA256 已核对为 `80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0`。 |
| F3 | 全库 missing-pocket / missing-D4 缺口基数与可补齐率估算 | 已完成本地 Rhea 基线估算 | 统计边界是 release-pinned Rhea 140 / reviewed UniProt 本地基线，不是 live UniProt 全库。主要缺口不是 UID 或序列，而是完整 D4 资产链。 |
| F4 | Q2 代码行号统一复核 + 3B 配置来源说明 | 已完成 | 已按官方 commit `255a05e...` 复核 `train.py`、`model.py`、`base.py`、`evaluate.py`、`geometric.py` 行号。`config/train/pretrain_esm2_3b/seed_42.yaml` 已说明为本项目 Chenyu/本地 ESM-2 3B corrected-pocket 正式运行配置，不是官方公开 repo 自带配置。 |
| F5 | BioTransformer ENVMICRO 源码摘录 + jar 身份证据 | 已完成 | 已补 `BiotransformerExecutable` / `EnvMicroBTransformer` / `ChemStructureExplorer` 关键源码摘录。HPC 返回包工具身份为 commit `7149f7ec6b2f32f9f789bab53aa4a71db49e59e2`，jar SHA256 为 `e5c3c27de7dfc87b448f1eed6fe986ef48ed90c53bad9b848f95378f08efee80`。 |
| F6 | 弓师兄模型 18 条 blind 评分，三工具横向比较闭环 | 未完成；前置已完成 | 18 条 gold standard、blind input、统一 schema、统一 scorer 已固化；BioTransformer/enviFormer replay 已完成。弓师兄模型输出尚未返回，因此 F6 标记为 `F6_PREPARED_WAITING_GONG_MODEL_OUTPUT`，不写成 fully complete。 |

F3 本地 Rhea 基线核心数字：

```text
raw Rhea-linked UID                  236,103
strict cleaned main-table UID        195,743
Rhea official complete-EC source UID 218,010
uid2seq sequence coverage            236,103 / 236,103
strict valid pocket rows             191,062 / 195,743
strict UID missing valid pocket        4,681
local ESM2-3B corrected features     107,705 UID
strict UID missing local ESM2-3B      88,038
complete-EC source UID missing local ESM2-3B 114,804 / 218,010
```

## 4. 反应 fallback 前置：18 条污染物 gold/schema/scorer

本轮已经把 Chenyu rerun1 返回包整理为 teacher-deliverables 可审阅包：

```text
2026-08-04_M3_P1_2_1_Small_Pollutant_Gold_Standard_Schema_Scoring_Freeze/
```

包内包含：

```text
gold_standard/
schema/
scripts/
validation/
replay/biotransformer_envmicro/
replay/enviformer_latest/
audits/
archive_identity/
README.md
DELIVERABLE_SHA256SUMS.txt
```

验证结果：

```text
case_count         = 18
reaction_row_count = 39
product_row_count  = 39
blind input rows    = 18
blind columns        = case_id, pollutant_name, parent_smiles, parent_inchikey, input_policy
```

Blind input 不含 product、reaction、answer、evidence、url 等答案列。

两工具 replay scoring：

```text
BioTransformer ENVMICRO:
  Hit@1  = 9/18  = 0.500000
  Hit@3  = 13/18 = 0.722222
  Hit@5  = 16/18 = 0.888889
  Hit@10 = 16/18 = 0.888889
  MRR@10 = 0.619444
  recovered products@10 = 20/39

enviFormer latest:
  Hit@1  = 0/18  = 0.000000
  Hit@3  = 1/18  = 0.055556
  Hit@5  = 1/18  = 0.055556
  Hit@10 = 1/18  = 0.055556
  MRR@10 = 0.027778
  recovered products@10 = 1/39
```

边界：这仍是 F6 前置，不是最终三工具横向比较；弓师兄模型回来后再用同一 schema/scorer 打分。

## 5. 菌层与 MetaTraits 侧逐项回应

| 项 | 老师要求 | 当前状态 | 结果和证据 |
|---|---|---|---|
| D5 / ④ | 用 P0 Top-MRR 正确酶反查宿主菌，验证 MetaTraits 接口、coverage、rate limit、no_robust_majority，并附 raw JSON | 已完成且已再确认 | D5 新合同版交付在 `2026-07-24_MT_D5_New_Contract_Reaudit_and_Resubmission/`；本轮新增索引 `METATRAITS_D5_2026_08_03_TEACHER_LIST_RECONFIRMATION_INDEX_2026-08-04.md`。 |
| ⑤ | MetaTraits 数据面接入方式 | 旧裁定已完成，仍需在本次重新指路 | production 主路径仍是 official versioned snapshot；网站 endpoint 只作 experimental fallback。正式 snapshot 未到前不启动生产硬过滤。 |
| ⑥ | organism ID 对齐 | 初测完成，结果为负 | 已显式区分 exact strain / exact species / no exact match。当前样本结果为 `exact_strain=0`、`exact_species=0`、`no_exact_match_established=10`。 |
| ⑦ / D4 | 污水 Trait 硬约束清单 | v1 已确定 soft-only | 生物学侧已确认：污水相关性状保留为用户参考、建议、解释和不确定性提示，不自动删除候选菌。 |
| D1-D8 | 框架 D1-D8 逐条立场 | 已由 2026-07-18 老师文件裁定，D3 后续修正 | 本轮已再审计；最终回复中重新指路，不假设老师已看到旧材料。 |
| 2.2 / D2 | 酶→菌 confidence 来源 | 已有裁定口径 | v1 不输出伪精确 `organism_confidence` float；透传 reviewed status、annotation score、protein existence、KEGG multiplicity 等证据维度。如后续 schema 强制 numeric confidence，应另写 `CONFIDENCE_MAPPING_PROPOSAL.md`。 |
| Task 7 / ② | TraitValue schema + `not_applicable` 示例 | 已完成旧交付，本轮已再确认 | `TRAIT_VALUE_NOT_APPLICABLE_SCHEMA_CONTRACT.md` 和 `2026-07-24_Task7_TraitValue_Not_Applicable_Contract/`；contract-only，不落 Pydantic 活代码，不启动 M4b。 |

特别说明：MetaTraits exact TaxID → trait 通路目前没有打通；D5 中 direct TaxID API 初测为负结果，因此当前只能用于 bounded soft-trait prototyping，不能用于 production hard filtering。

## 6. M3-EXT 候选二次裁定材料

老师 2026-08-03 已确认 `M3_EXT_CANDIDATE_SHORTLIST_v0.md` 符合 2026-07-21 授权边界。本轮重新整理了二次裁定材料。

当前状态：

```text
候选筛选材料已完成；
仍等待二次裁定；
未补 D4；
未重建 route_b / route_c；
未跑 EnzymeCAGE；
未纳入首页三案例；
未声称系统验证案例。
```

保留候选：

- Paraoxon hydrolysis：RHEA:18053 / 18054，frozen Rhea EC `3.1.8.1`，B/C = 0/13。
- Carbaryl hydrolysis：RHEA:62380 / 62381，frozen Rhea EC `null`，external EC candidate `3.5.1.137`，B/C = 0/72。

已排除候选：

- Nitrobenzene dioxygenation：nitrobenzene molecule 在 formal train 中出现 52 行，违反 molecule exclusion gate；同时存在多组分酶系统边界。

后续仍需老师裁定：

1. Paraoxon / Carbaryl 是否晋级正式 M3-EXT 官方挑战案例；
2. 是否授权对应 evidence UID 的 D4 构造可行性；
3. Carbaryl 的 external EC bridge 是否可用；
4. 后续 fair full-pool Route-B 的来源和纳入规则；
5. 是否授权 EC-null evidence-discovery pilot。

## 7. 当前不能过度声称的内容

本轮不会把以下内容写成完成：

```text
F6 三工具横向比较已经完成；
弓师兄模型已经评分；
BioTransformer 已被正式选为 reaction_prediction fallback 引擎；
M3-EXT 候选已经晋级正式案例；
M3 内已经补齐正式 D4 资产；
MetaTraits exact TaxID -> trait 通路已打通；
organism_confidence 0-1 数值已经实现；
污水 trait 已作为 hard filter 自动删除候选菌。
```

## 8. 需要老师后续知道的 pending / 裁定项

```text
F6:
  等弓师兄模型输出后，用同一 18 条 blind input、schema 和 scorer 完成三工具横向比较。

M3-EXT:
  等老师二次裁定是否晋级正式案例及是否授权资产补齐。

OnDemand D4:
  当前作为 M4 前置摸底归档；是否工具化待 M4 合同裁定。
  若 M4 允许 EC/Rhea 外扩候选进入排序模型，建议老师同时裁定：
  A. 遇到少量域外 UID 时，是否采用 UID-only on-demand D4 backfill，
     生成隔离 staged assets 后再临时评分；
  B. 如果目标是系统性覆盖更宽 Rhea/EC 酶域，是否另开 full-coverage
     D4 资产补齐/重整理，或设计 full strict Rhea asset/training 对照。
  本轮只提供缺口基线与按需补资产可行性证据，不擅自启动全量重训。

MetaTraits / M4b:
  official versioned snapshot 和 production organism_uid -> traits 通路仍未闭合；
  M4b / M4c 未自动启动。

Reaction fallback:
  BioTransformer ENVMICRO 当前是候选引擎中表现较好的一个；
  是否正式作为 fallback，需要等弓师兄模型一起比较后再裁定。
```

## 9. 发送前动作完成状态

发送给老师前的本地与远端动作状态：

```text
1. 统一 git add / commit / push：已完成
   - EnzymeCAGE-Teacher-Deliverables
   - EnzymeCAGE-MetaTraits-Teacher-Deliverables
2. 打开并检查所有 GitHub 链接：已完成，全部 200
3. 必要时把本文同字节复制到 MetaTraits teacher-deliverables 根目录：当前不需要；MetaTraits 侧已有独立索引与包链接
4. 再给黄老师发简短消息，主链接指向本逐项回应：待用户发送
```
