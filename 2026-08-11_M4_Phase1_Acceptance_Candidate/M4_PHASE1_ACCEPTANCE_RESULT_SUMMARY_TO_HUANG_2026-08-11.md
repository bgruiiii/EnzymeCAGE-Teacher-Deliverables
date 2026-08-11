# M4 Phase 1 验收候选包提交说明

黄老师您好，

根据您 2026-08-11 对 M4 Phase 1 的条件同意意见，我们完成了
Phase 1 100 UID frozen acceptance package 的本地整理和审计。当前材料是
**验收候选包**，用于请您审查裁定；不是 full 4,681 UID backfill，也没有
写入 production D4 或 production pool。

## 1. 本次提交位置

GitHub 交付仓库：

```text
bgruiiii/EnzymeCAGE-Teacher-Deliverables
```

本次提交目录：

```text
2026-08-11_M4_Phase1_Acceptance_Candidate/
```

主返回包：

```text
evidence_copies/
enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811.tar.gz
```

外部 identity：

```text
evidence_copies/
enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811.tar.gz.identity.txt
```

本地审计：

```text
evidence_copies/
M4_PHASE1_ACCEPTANCE_CIF_PARSER_FIX_RERUN_RETURN_LOCAL_AUDIT_2026-08-11.md
```

## 2. 对您前置条件的对应

### 条件 1：F3 核验路径

已随验收包交付，并在 Chenyu 上从 payload source snapshot 重新运行。

关键结果：

```text
f3_reproduction_pass=true
expected_count_mismatches={}
strict_cleaned_2026_main_table_uid=195743
strict_uid_missing_valid_pocket=4681
```

本地 F3 审计：

```text
evidence_copies/
M4_PHASE1_F3_NUMERIC_REPRODUCTION_PATH_LOCAL_AUDIT_2026-08-11.md
```

### Phase 1 frozen 100 UID 子集

冻结清单保持 100 行、100 个唯一 `UniprotID`，分层为：

| Stratum | Count |
|---|---:|
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 35 |
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 25 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 40 |

所有 100 个 UID 均满足：

```text
strict_2026_uid=true
local_sequence_present=true
f3_missing_valid_pocket_member=true
final_missing_pocket_uid_member=true
appeared_in_previous_2026_08_03_pilots=false
main_acceptance_denominator=true
```

本地 UID freeze 审计：

```text
evidence_copies/
M4_PHASE1_ACCEPTANCE_UID_FREEZE_LOCAL_AUDIT_2026-08-11.md
```

### P2Rank 工具身份

验收包使用稳定隔离路径：

```text
/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1
```

身份记录：

```text
p2rank_version=P2Rank 2.5.1
p2rank_archive_sha256=d243f2d9036ac053fefb9407b5fe1c85f4fe077c519fd975ac585e995feab274
command_contract=prank predict -threads 4 -c alphafold -visualizations 0 ...
```

说明：release tarball 内无 `.git` 元数据，因此本地能严格证明的是
release archive SHA256、版本和命令合同；`255a05e` 作为您要求的官方
commit 字段保留为 expected identity field，但不写成本地 git metadata
已证明。

P2Rank 本地审计：

```text
evidence_copies/
M4_PHASE1_P2RANK_ISOLATED_TOOL_DIR_ESTABLISHMENT_RETURN_LOCAL_AUDIT_2026-08-11.md
```

## 3. Phase 1 100 UID 结果

最终状态分布：

| Final status | Count |
|---|---:|
| `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 41 |
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | 44 |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | 15 |
| `BLOCKED_AFDB_STRUCTURE_PARSE_FAILED` | 0 |

解释：

```text
41/100 完成 staged AFDB-only P2Rank predicted-pocket D4 assets，并通过
ESM-2 3B、same-pocket GVP 与 isolated loader validation。

44/100 是 AFDB structure 可用且 P2Rank 已运行，但在批准命令合同下未
产生可用 top predicted pocket；这不是下载失败。

15/100 是 AFDB structure 获取失败。本地复核 STRUCTURE_SOURCE_TABLE.csv
显示其中 12 个为 HTTP 404，3 个为 HTTP 000。
```

之前首轮返回中 7 个 `BLOCKED_AFDB_STRUCTURE_PARSE_FAILED` 被审计为脚本
假 blocker；本次 clean rerun 已修复：

| UID | 修复后状态 |
|---|---|
| `C5B8H7` | `BLOCKED_AFDB_P2RANK_NO_POCKET` |
| `Q9BZG8` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` |
| `Q29451` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` |
| `A0A0U3S9Q3` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` |
| `P0DJN3` | `BLOCKED_AFDB_P2RANK_NO_POCKET` |
| `A6SUD8` | `BLOCKED_AFDB_P2RANK_NO_POCKET` |
| `Q8UFS9` | `BLOCKED_AFDB_P2RANK_NO_POCKET` |

## 4. 资产和边界

PASS UID staged asset manifest：

```text
41 PASS UIDs
246 required manifest rows = 41 x 6
0 missing required PASS asset entries
0 non-PASS UID staged manifest entries
```

Mutation flags：

```text
formal_assets_mutated=false
production_pool_mutated=false
formal_feature_root_mutated=false
formal_split_root_mutated=false
production_data_root_mutated=false
production_dataset_root_mutated=false
```

本次没有执行：

```text
full 4,681 UID backfill
production D4 merge
production pool mutation
strict AlphaFill pocket claim
```

## 5. 请老师审查裁定

请老师审查本次 Phase 1 acceptance candidate：

```text
是否认可该 100 UID frozen subset 的 staged 端到端验收结果与 blocker
统计口径；
是否认可 F3 数字复现路径已满足前置条件；
是否允许在 Phase 1 验收裁定后，另行进入第二里程碑 full 4,681 UID
status table 的授权讨论。
```

我们不会在未获您另行裁定前启动 full 4,681 backfill 或 production merge。
