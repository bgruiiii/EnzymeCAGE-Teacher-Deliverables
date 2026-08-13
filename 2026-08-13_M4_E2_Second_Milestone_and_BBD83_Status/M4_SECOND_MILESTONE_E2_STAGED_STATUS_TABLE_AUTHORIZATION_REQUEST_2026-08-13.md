# M4 第二里程碑 E2：full 4,681 staged status table 授权方案草案

日期：2026-08-13

状态：本地方案草案，供提交黄老师前复核；尚未启动 full 4,681 运行，尚未写入 production D4，尚未合并 production pool。

依据：

```text
黄老师 2026-08-13 项目下一步指导：
P0-1 提交 M4 第二里程碑方案 E2。
方案需包含：
1) 观察点 1：1 个 cache-miss UID 提取 smoke；
2) full 4,681 staged status table 计划；
3) no-pocket 约 44% 处理策略；
4) 8 个非病毒 404 accession 变体复核计划；
5) 工作量与时间线。
```

## 0. 边界说明

本方案只请求第二里程碑授权，不声称已经完成 full 4,681。

本方案不包含：

```text
production D4 merge；
production pool mutation；
全量 4,681 已补齐结论；
模型 inference / ranking / scoring；
把 P2Rank predicted pocket 等同 strict AlphaFill pocket。
```

全部后续输出仍按 staged-only 处理，保留 per-UID 状态、来源、命令、版本、SHA256、blocker reason 和 mutation check。

## 1. 已完成观察点 1：1 个 cache-miss UID smoke

我们已按 2026-08-13 E2 观察点 1 做了一个受限 smoke：

```text
archive:
enzymecage_m4_e2_cache_miss_one_uid_smoke_bounded_fallback_20260813.tar.gz

archive_sha256:
8573bd4524934f795dea035204ffb06815e0f937b7f2df6c2345319bd88d62ff

final_status:
M4_E2_CACHE_MISS_ONE_UID_SMOKE_COMPLETE_WITH_ONE_PASS_AND_ATTEMPT_LOG
```

准确结论：

```text
第一个候选 A3CST9 完成 cache-miss staged-only smoke。
后续候选 B8GGQ9 / A7I9P9 / A0A0H2V760 / P0DXZ0 因
stop_after_first_pass=true 未继续尝试，不应表述为已测试或已通过。
```

`A3CST9` 的通过证据：

| 项 | 结果 |
|---|---:|
| pre-attempt ESM-2 3B cache | `cache_miss` |
| pre-attempt pocket-node cache | `cache_miss` |
| pre-attempt GVP cache | `cache_miss` |
| local sequence | present, 398 aa |
| AFDB structure | HTTP 200, model v6, parser PASS, chain A |
| P2Rank | `P2Rank 2.5.1`, top pocket rank 1, score 118.99 |
| final mapped pocket residues | 85 |
| ESM-2 3B | PASS, pocket-node shape `[85, 2560]` |
| GVP | PASS |
| same pocket for ESM/GVP | true |
| isolated loader validation | PASS, dataset length 1, `dataset[0]` constructed |
| staged assets generated | true |
| formal / production mutation | false |

该 smoke 证明的范围：

```text
在 Chenyu 当前环境下，至少一个真实 cache-miss UID 可以按
AFDB -> P2Rank predicted pocket -> ESM-2 3B staged feature ->
same-pocket GVP -> isolated loader validation 的 lower-evidence route 跑通。
```

该 smoke 不证明：

```text
full 4,681 已处理；
production D4 可直接合并；
P2Rank pocket 是 strict AlphaFill ligand-neighbor pocket；
模型预测效果已经验证。
```

## 2. 第二里程碑 full 4,681 staged status table 计划

### 2.1 Denominator

第二里程碑建议以 F3 已复现的基数作为总入口：

```text
strict_uid_missing_valid_pocket = 4,681
```

执行时先冻结 4,681 UID manifest，并在状态表中显式保留：

```text
F3_missing_valid_pocket_member；
final_missing_pocket_member；
Phase1_100UID_member；
Phase1_result_if_any；
sampling_stratum_if_available。
```

说明：

```text
Phase 1 冻结样本来自 final_missing_pocket_uids.csv 的 4,453 子集，
同时要求属于 F3 4,681 missing-valid-pocket universe。
第二里程碑表按老师要求回到 full 4,681 总入口，并对 4,681 与 4,453
之间的 membership 差异单列状态，不在表外丢弃 UID。
```

### 2.2 默认处理路线

授权后对每个 UID 按同一命令合同处理：

```text
UniProt UID / local sequence
-> AlphaFoldDB structure probe
-> P2Rank 2.5.1 `prank predict -threads 4 -c alphafold -visualizations 0`
-> top predicted pocket residues
-> pocket PDB / pocket_info.csv
-> ESM-2 3B staged protein-level and pocket-node features
-> same-pocket GVP staged feature
-> isolated load_geometric_dataset validation
-> per-UID status table + staged asset manifest
```

P2Rank route 在状态表中统一标注为：

```text
evidence_tier = lower_evidence_predicted_pocket
pocket_source = AFDB_P2RANK_TOP_PREDICTED_POCKET
```

不静默使用：

```text
whole-protein 代替 pocket；
固定 residue window 代替 pocket；
未授权的 P2Rank 参数变化；
old-pool pocket rescue；
AlphaFill / PDB-REDO / SMR / experimental PDB fallback。
```

### 2.3 每 UID 最终状态

每个 UID 必须 exactly one final status。建议状态包括：

| 状态 | 含义 |
|---|---|
| `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | AFDB 结构、P2Rank top pocket、ESM-2 3B、same-pocket GVP、isolated loader 全部通过，产物仅 staged；沿用 Phase 1 已审计 PASS token |
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | AFDB 结构可取且 P2Rank 已运行，但当前命令合同下无可用 top predicted pocket |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | AFDB 当前未取到可用结构 |
| `BLOCKED_ACCESSION_REVIEW_REQUIRED` | UID 或 accession 状态需要只读复核，不能静默替换 |
| `BLOCKED_SEQUENCE_MISSING_OR_CONFLICT` | local sequence 缺失或与当前 UniProt 序列冲突 |
| `BLOCKED_ESM2_3B_EXTRACTION_FAILED` | pocket 已定义，但 ESM-2 3B 生成失败 |
| `BLOCKED_GVP_EXTRACTION_FAILED` | same-pocket GVP 生成失败或与 ESM pocket-node 行数不一致 |
| `BLOCKED_LOADER_VALIDATION_FAILED` | staged 资产存在但 isolated loader validation 未通过 |
| `BLOCKED_ENVIRONMENT_ERROR` | Chenyu 环境、网络、工具路径或资源异常，需单列重试 |

### 2.4 主要输出表

授权后交付包建议至少包含：

```text
FULL_4681_UID_MANIFEST.csv
FULL_4681_STAGED_STATUS_TABLE.csv
FULL_4681_TIMING_RESOURCE_TABLE.csv
FULL_4681_STRUCTURE_SOURCE_TABLE.csv
FULL_4681_P2RANK_STATUS_TABLE.csv
FULL_4681_ACCESSION_REVIEW_TABLE.csv
FULL_4681_NO_POCKET_REVIEW_TABLE.csv
STAGED_ASSET_MANIFEST.csv
FORMAL_ASSET_MUTATION_CHECK.json
PRODUCTION_MUTATION_CHECK.json
P2RANK_VERSION_AND_INSTALL_REPORT.txt
ENVIRONMENT_REPORT.txt
COMMAND_LOG.txt
MANIFEST.sha256
FINAL_STATUS.txt
per_uid/<UID>/REPORT.md
per_uid/<UID>/REPORT.json
```

`FULL_4681_STAGED_STATUS_TABLE.csv` 建议字段：

```text
UniprotID
f3_missing_valid_pocket_member
final_missing_pocket_member
phase1_100uid_member
phase1_result_if_any
sampling_stratum_if_available
sequence_source
sequence_length
sequence_sha256
pre_attempt_esm2_3b_cache_status
pre_attempt_pocket_node_cache_status
pre_attempt_gvp_cache_status
afdb_structure_status
afdb_http_status
afdb_model_version
afdb_structure_sha256
accession_review_status
reviewed_accession_candidate
reviewed_accession_action
p2rank_status
p2rank_version
p2rank_command
p2rank_top_pocket_rank
p2rank_top_pocket_score
p2rank_pocket_residue_count
pocket_source
evidence_tier
esm2_3b_status
esm_node_feature_shape
gvp_status
same_pocket_for_esm_node_and_gvp
loader_validation_called
loader_validation_status
dataset_len
dataset0_constructed
staged_asset_manifest_rows
formal_assets_mutated
production_pool_mutated
production_d4_mutated
final_status
final_status_reason
retryable
wall_sec
notes
```

## 3. no-pocket 约 44% 的处理策略

Phase 1 corrected 100 UID rerun 的实证结果：

```text
41/100 PASS；
44/100 BLOCKED_AFDB_P2RANK_NO_POCKET；
15/100 BLOCKED_AFDB_STRUCTURE_FETCH_FAILED；
0/100 BLOCKED_AFDB_STRUCTURE_PARSE_FAILED。
```

其中 `BLOCKED_AFDB_P2RANK_NO_POCKET` 的准确含义是：

```text
AFDB 结构已经取得，P2Rank 也按 `prank predict -c alphafold`
命令合同运行，但没有生成可用 top predicted pocket residues。
这不是下载失败，也不是 ESM-2 3B / GVP / loader 流程失败。
```

这批 UID 本身来自 missing valid pocket 历史缺口，因此属于困难集合；P2Rank predicted-pocket fallback 的目标是尽量补 staged 资产，而不是承诺全部补齐。

建议处理口径：

```text
1. 授权后 full 4,681 运行中，对 no-pocket UID 保留 P2Rank 原始输出、
   run.log、结构来源和序列长度等证据；
2. 在 FULL_4681_NO_POCKET_REVIEW_TABLE.csv 中统计 no-pocket UID 的长度、
   AFDB model version、P2Rank 输出状态、是否短序列/小蛋白；
3. 默认接受其为当前命令合同下的明确 blocker；
4. 不静默修改 P2Rank 参数、pocket 定义或结构来源；
5. 若老师希望进一步提高覆盖，应另行裁定新的 pocket 定义或参数试验。
```

建议给老师的边界表述：

```text
P2Rank no-pocket 是当前结构源和命令合同下的可补边界，不应解释为
"P2Rank 数据库查不到"，也不应解释为 EnzymeCAGE loader 失败。
```

## 4. 8 个非病毒 404 accession 变体复核计划

Phase 1 corrected rerun 中 15 个 AFDB fetch-blocked UID 包括：

```text
7 个病毒 UID；
8 个非病毒 UID。
```

7 个病毒 UID 建议归入当前 AFDB/AlphaFill 覆盖边界：

```text
A0A7H0DNE2
P03133
P04382
P0CAP6
P27328
P68761
Q9IR51
```

8 个非病毒 UID 已做 2026-08-13 只读初查：

| UID | 当前 UniProt 物种 | 长度 | accession / isoform 初查 | 当前 AFDB 结果 |
|---|---|---:|---|---|
| `P29263` | *Prunus serotina* | 14 aa | reviewed；未见 secondary accession；未见 isoform | AFDB API 404 |
| `P85362` | *Cycas revoluta* | 9 aa | reviewed；未见 secondary accession；未见 isoform | AFDB API 404 |
| `P85432` | *Cycas revoluta* | 13 aa | reviewed；未见 secondary accession；未见 isoform | AFDB API 404 |
| `P86056` | *Daucus carota* | 15 aa | reviewed；未见 secondary accession；未见 isoform | AFDB API 404 |
| `Q19QT7` | *Sus scrofa* | 405 aa | reviewed；未见 secondary accession；未见 isoform | AFDB API 404 |
| `Q4AEH3` | *Sapajus apella* | 226 aa | reviewed；未见 secondary accession；未见 isoform | AFDB API 404 |
| `Q73FJ3` | *Bacillus cereus* ATCC 10987 / NRS 248 | 424 aa | reviewed；未见 secondary accession；未见 isoform | AFDB API 404 |
| `Q9Z1Y9` | *Mus musculus* | 266 aa | reviewed；secondary `Q05A70,Q9JHH1` 为 inactive accession，归并至 `Q9Z1Y9`；未见 isoform | primary 和 secondary AFDB 均 404 |

初查解释：

```text
4 个非病毒 UID 是 9-15 aa 极短序列，更可能属于 AFDB/结构预测覆盖边界；
其余 4 个长度正常，但当前 AFDB API 仍未返回模型。
本次初查未发现可直接用于替换原 UID 的可用 AFDB accession 变体。
```

授权后系统复核方法：

```text
1. 对 full 4,681 中所有 AFDB fetch-blocked UID 生成
   FULL_4681_ACCESSION_REVIEW_TABLE.csv；
2. 对每个 UID 查询 UniProt primary accession、secondary accession、
   inactive/obsolete/remapped 状态、canonical/isoform 信息；
3. 对 primary、secondary、合法 isoform 或 reviewed accession candidate
   做 AFDB API 与 v6/v5/v4 file URL 只读探测；
4. 若发现 reviewed_accession_candidate 有可用 AFDB 模型，只记录为
   candidate，不静默替换原 UID；
5. 是否允许 `original_uid -> reviewed_accession_candidate` 用于 staged D4
   资产生成，需老师另行裁定。
```

## 5. 工作量与时间线

在当前 Chenyu 环境已完成 Phase 1、P2Rank 2.5.1、ESM-2 3B、GVP、loader smoke 的前提下，建议给第二里程碑采用两档估计。

较顺利情形：

```text
授权后约 2-3 个工作日提交 full 4,681 staged status package。
条件：
  Chenyu GPU / 网络 / AFDB API 稳定；
  P2Rank 2.5.1、Java、ESM-2 3B checkpoint、GVP、loader 依赖保持可用；
  不做 production merge；
  不引入新的 pocket 参数或结构来源；
  只交付 staged status table、staged PASS assets、blocker tables 和审计包。
```

保守情形：

```text
授权后约 3-5 个工作日提交。
触发条件：
  AFDB/API 大量限流或超时；
  需要分批重试环境错误；
  full 4,681 中出现新的 parser / sequence conflict / accession conflict；
  需要额外人工复核 accession candidate；
  需要多轮本地审计和 teacher-facing package 整理。
```

时间估计依据：

```text
Phase 1 corrected 100 UID rerun：41 PASS / 59 blocker；
A3CST9 one-UID smoke：总 wall 47.573 s，其中 ESM-2 3B 33.805 s、
P2Rank 4.248 s、GVP 3.347 s、loader 2.029 s；
08-03 AFDB-only P2Rank pilot：45 个 PASS UID 的 full D4 loader-valid
warm/batched 平均约 16.34 s/UID。
```

这些 runtime 只能作为 order-of-magnitude anchor，不能线性保证 full 4,681 总耗时。

## 6. 请求黄老师裁定

请老师裁定以下事项：

```text
1. 是否同意启动第二里程碑 full 4,681 staged status table；
2. 是否同意继续使用 AFDB-only + P2Rank 2.5.1 top predicted pocket
   作为 lower-evidence staged fallback；
3. 是否同意 no-pocket UID 在当前命令合同下作为明确 blocker 记录，
   除非另行授权新的 pocket 定义或参数；
4. 是否同意 7 个病毒 AFDB fetch-blocked UID 归入当前覆盖边界；
5. 是否同意对 8 个非病毒 404 / fetch-blocked UID 执行只读 accession
   变体复核，并将可疑 candidate 只写入 review table，不静默替换；
6. 是否同意本阶段仍严格保持 staged-only，不写 production D4，
   不修改 production pool；production merge 等下一步单独裁定。
```

## 7. 红线延续

本方案继续遵守：

```text
P2Rank predicted-pocket = lower-evidence tier；
staged-only；
formal_assets_mutated=false；
production_pool_mutated=false；
production_d4_mutated=false；
full 4,681 未经老师裁定前不启动；
production merge 未经老师裁定不启动。
```

禁止使用以下完成性表述，除非后续老师授权和证据确实支持：

```text
M4_PRODUCTION_D4_BACKFILL_COMPLETE
M4_ALL_4681_UIDS_BACKFILLED
PASS_FULL_D4_LOADER
```
