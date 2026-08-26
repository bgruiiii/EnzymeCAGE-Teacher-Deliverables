# HPC executor-only prompt — BBD full-route v0.3 v3.1 multistep simple-path repair v2 cleanup supplement

Date: 2026-08-26  
Executor: chenyu / HPC  
Task type: tiny cleanup supplement only; do not rerun prediction tools; do not score  
Expected return root:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

Expected return folder:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_v2_cleanup_supplement_20260826
```

Expected archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_v2_cleanup_supplement_20260826.tar.gz
```

## 0. One-sentence goal

The previous simple-path repair package fixed the major repeated-node / repeated-edge path defect, but it still contains 13 root-only zero-edge placeholder path rows and one archive-SHA identity inconsistency. This v2 cleanup must remove the zero-edge placeholder paths, recompute summaries with correct non-empty-path coverage, and fix final archive identity metadata.

Do not rerun BioTransformer, enviPath, ECLIPSE, or any model inference.

Do not read restricted answer files.

Do not score.

## 1. Previous package to clean

Use this package as the only main input:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_supplement_20260826.tar.gz
```

Expected package identity from the returned sidecar / local audit:

```text
archive_sha256=5fa02f1d566ede109a9c6d731f5dd67bfe2021c0592010e6e870b7dbed13dc4d
final_status=COMPLETE_MULTISTEP_SIMPLE_PATH_REPAIR_READY_FOR_LOCAL_AUDIT
restricted_answer_key_read=false
scoring_performed=false
```

Local audit of that package found:

```text
Core repeated-path repair: PASS
Strict contract compliance: PASS_WITH_MINOR_REPAIR_REQUIRED
```

Residual issues to fix:

```text
1. BioTransformer ENVMICRO has 8 path_depth=0 root-only rows.
2. enviPath BBD Rules has 5 path_depth=0 root-only rows.
3. Summary fields counted those root-only rows as cases_with_any_simple_path.
4. In-package executor audit recorded archive_sha256=8bf7f8a0c8a8abcdfe179f9fc24760def306323f0dd9a8e298bef31e42f20bd4, but the actual returned tarball and identity sidecar report 5fa02f1d566ede109a9c6d731f5dd67bfe2021c0592010e6e870b7dbed13dc4d.
```

## 2. Hard rules

1. Do not rerun BioTransformer.
2. Do not rerun enviPath prediction or lookup.
3. Do not rerun ECLIPSE inference.
4. Do not retrain any model.
5. Do not read, copy, grep, package, or infer from any restricted answer file.
6. Do not run scoring against accepted products, downstream answer nodes, route edges, terminal nodes, or path answers.
7. Do not use BBD answer/restricted route files to choose, rank, prune, or validate paths.
8. Do not modify production data, production model files, GitHub, or shared repository history.
9. Do not package credentials, model checkpoints, raw prediction directories, or large unrelated assets.
10. Keep this a cleanup-only package. It should be small.
11. Put all return files under:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

## 3. Allowed input files

From the extracted previous repair package, use only:

```text
README_BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_SUPPLEMENT.md
RUN_MANIFEST.json
MANIFEST.sha256
00_INPUT_AUDIT/previous_multistep_package_identity.json
00_INPUT_AUDIT/allowed_input_files_used.csv
01_REPAIRED_ROUTE_PATHS/<route_id>/PREDICTED_ROUTE_PATHS_SIMPLE.jsonl
01_REPAIRED_ROUTE_PATHS/<route_id>/PREDICTED_ROUTE_PATHS_SIMPLE_TOP10_BY_CASE.csv
01_REPAIRED_ROUTE_PATHS/<route_id>/SIMPLE_PATH_REPAIR_SUMMARY.csv
01_REPAIRED_ROUTE_PATHS/<route_id>/SIMPLE_PATH_REPAIR_SUMMARY.md
02_QC_NO_SCORING/*.csv
02_QC_NO_SCORING/qc_summary.md
03_EXECUTOR_AUDIT/BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_SUPPLEMENT_EXECUTOR_AUDIT.md
scripts/repair_bbd_full_route_v0_3_v3_1_multistep_simple_paths.py
logs/*.log
```

Do not use any local benchmark `restricted/` files.

Do not use the original bounded multistep edge/node graph unless needed only for provenance cross-check. This task should be possible from the previous simple-path repair package alone.

## 4. Exact rows to remove

Remove every repaired path row where:

```text
path_depth == 0
len(edge_id_path) == 0
```

Known zero-edge placeholder rows from local audit:

BioTransformer ENVMICRO:

```text
FR-BBD3-CAND-c0347__sp01
FR-BBD3-PARENT-c0039__sp01
FR-BBD3-PARENT-c0352__sp01
FR-BBD3-PARENT-c0426__sp01
FR-BBD3-PARENT-c0444__sp01
FR-BBD3-PARENT-c0526__sp01
FR-BBD3-PARENT-c0939__sp01
FR-BBD3-PARENT-c1039__sp01
```

enviPath BBD Rules:

```text
FR-BBD3-PARENT-c0039__sp01
FR-BBD3-PARENT-c0116__sp01
FR-BBD3-PARENT-c0444__sp01
FR-BBD3-PARENT-c0939__sp01
FR-BBD3-PARENT-c1201__sp01
```

Do not hard-code only these IDs as the complete logic. The required rule is:

```text
remove all path_depth=0 / empty edge_id_path rows from all route outputs
```

## 5. Required recomputation

After removing zero-edge rows, recompute for each route:

```text
simple_path_rows
cases_with_any_simple_path
cases_with_nonempty_simple_path
cases_with_root_only_no_clean_path
cases_with_depth_1_simple_path
cases_with_depth_2_simple_path
cases_with_depth_3_simple_path
cases_with_depth_4_simple_path
cases_with_depth_5_simple_path
cases_with_depth_6_simple_path
max_simple_path_depth
repaired_repeated_node_path_count
repaired_repeated_smiles_path_count
repaired_repeated_edge_path_count
all_contains_parent_copy_edge_false
all_contains_source_self_loop_edge_false
```

Definitions:

```text
cases_with_any_simple_path = cases with at least one retained path row with path_depth >= 1.
cases_with_nonempty_simple_path = same as cases_with_any_simple_path.
cases_with_root_only_no_clean_path = cases that had only root-only zero-edge placeholder rows before cleanup and now have no retained path row.
```

Expected corrected coverage from local audit:

```text
BioTransformer ENVMICRO: cases_with_nonempty_simple_path = 85/93
enviPath BBD Rules: cases_with_nonempty_simple_path = 88/93
ECLIPSE PREDEC: cases_with_nonempty_simple_path = 93/93
ECLIPSE NoEC optional: cases_with_nonempty_simple_path = 93/93
```

Expected corrected row counts:

```text
BioTransformer ENVMICRO: 787 - 8 = 779 retained path rows
enviPath BBD Rules: 750 - 5 = 745 retained path rows
ECLIPSE PREDEC: 930 retained path rows
ECLIPSE NoEC optional: 930 retained path rows
```

If your recomputed counts differ, do not force them. Report the observed values and explain the difference in the audit.

## 6. Required output structure

Create this return folder:

```text
bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_v2_cleanup_supplement_20260826/
├── FINAL_STATUS.txt
├── README_BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_V2_CLEANUP_SUPPLEMENT.md
├── RUN_MANIFEST.json
├── MANIFEST.sha256
├── 00_INPUT_AUDIT/
│   ├── previous_repair_package_identity.json
│   ├── previous_repair_package_identity.md
│   └── allowed_input_files_used.csv
├── 01_REPAIRED_ROUTE_PATHS_V2/
│   ├── biotransformer_envmicro_multistep/
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_V2.jsonl
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_V2_TOP10_BY_CASE.csv
│   │   ├── SIMPLE_PATH_REPAIR_V2_SUMMARY.csv
│   │   └── SIMPLE_PATH_REPAIR_V2_SUMMARY.md
│   ├── envipath_bbd_rules_multistep/
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_V2.jsonl
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_V2_TOP10_BY_CASE.csv
│   │   ├── SIMPLE_PATH_REPAIR_V2_SUMMARY.csv
│   │   └── SIMPLE_PATH_REPAIR_V2_SUMMARY.md
│   ├── eclipse_predec_bbd_finetuned_10fold_multistep/
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_V2.jsonl
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_V2_TOP10_BY_CASE.csv
│   │   ├── SIMPLE_PATH_REPAIR_V2_SUMMARY.csv
│   │   └── SIMPLE_PATH_REPAIR_V2_SUMMARY.md
│   └── eclipse_noec_bbd_finetuned_10fold_multistep_optional/
│       ├── PREDICTED_ROUTE_PATHS_SIMPLE_V2.jsonl
│       ├── PREDICTED_ROUTE_PATHS_SIMPLE_V2_TOP10_BY_CASE.csv
│       ├── SIMPLE_PATH_REPAIR_V2_SUMMARY.csv
│       └── SIMPLE_PATH_REPAIR_V2_SUMMARY.md
├── 02_QC_NO_SCORING/
│   ├── zero_edge_rows_removed.csv
│   ├── repaired_path_v2_qc_summary.csv
│   ├── path_duplicate_check_v2.csv
│   ├── corrected_path_coverage_summary.csv
│   └── qc_summary.md
├── 03_EXECUTOR_AUDIT/
│   └── BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_V2_CLEANUP_SUPPLEMENT_EXECUTOR_AUDIT.md
├── scripts/
│   └── cleanup_bbd_full_route_v0_3_v3_1_multistep_simple_paths_v2.py
└── logs/
    ├── input_audit.log
    ├── v2_cleanup.log
    └── packaging.log
```

Do not include raw prediction outputs, model files, checkpoints, credentials, or the full copied previous archive.

## 7. Required `PREDICTED_ROUTE_PATHS_SIMPLE_V2.jsonl` invariants

Every retained JSONL row must satisfy:

```text
path_depth >= 1
len(edge_id_path) >= 1
simple_path_valid == true
has_repeated_node_id == false
has_repeated_smiles_canonical == false
has_repeated_edge_id == false
contains_parent_copy_edge == false
contains_source_self_loop_edge == false
restricted_answer_key_read == false
scoring_performed == false
path_depth == len(edge_id_path)
len(compound_node_id_path) == len(edge_id_path) + 1
len(compound_smiles_canonical_path) == len(edge_id_path) + 1
```

Every route should still retain at most 10 path rows per case.

If a case has no retained path after zero-edge cleanup, do not create a fake row for it. Record it only in:

```text
cases_with_root_only_no_clean_path
zero_edge_rows_removed.csv
corrected_path_coverage_summary.csv
```

## 8. Required QC files

### 8.1 `zero_edge_rows_removed.csv`

Columns:

```text
route_id
tool_id
full_route_case_id
path_id
pollutant_name
pollutant_category
path_depth
edge_id_path
reason
```

Reason should be:

```text
root_only_zero_edge_placeholder_removed
```

### 8.2 `corrected_path_coverage_summary.csv`

Columns:

```text
route_id
tool_id
optional_route
input_parent_count
old_simple_path_rows
zero_edge_rows_removed
retained_simple_path_rows
old_cases_with_any_path_including_root_only
cases_with_nonempty_simple_path
cases_with_root_only_no_clean_path
max_simple_path_depth
restricted_answer_key_read
scoring_performed
```

### 8.3 `repaired_path_v2_qc_summary.csv`

Columns:

```text
route_id
simple_path_rows_v2
all_path_depth_ge_1
all_edge_id_path_nonempty
all_simple_path_valid
repaired_repeated_node_path_count
repaired_repeated_smiles_path_count
repaired_repeated_edge_path_count
all_contains_parent_copy_edge_false
all_contains_source_self_loop_edge_false
```

### 8.4 `path_duplicate_check_v2.csv`

Columns:

```text
route_id
simple_path_rows_v2
unique_case_smiles_path_count
duplicate_case_smiles_path_rows
max_paths_per_case
cases_exceeding_top10
```

## 9. Archive identity requirement

The previous repair package had a mismatch between:

```text
actual returned tarball / identity sidecar SHA256
```

and:

```text
archive_sha256 line inside executor audit
```

For this v2 package, fix the packaging order:

1. Write all files except the archive SHA line.
2. Finalize all logs.
3. Generate `MANIFEST.sha256`.
4. Run `sha256sum -c MANIFEST.sha256` and record PASS.
5. Create the `.tar.gz`.
6. Compute final archive SHA256.
7. Write a sidecar identity file beside the archive.
8. If you include archive SHA256 inside an executor audit or README, make sure it matches the final tarball SHA256. If that is hard because the audit is inside the tarball, then write:

```text
archive_sha256_recorded_in_sidecar_only=true
```

and do not put a stale in-package archive SHA256 in the package.

This is acceptable and better than putting a wrong archive SHA inside the tarball.

## 10. Required acceptance checks

Before packaging, run and record:

```text
previous_repair_archive_sha256_match=true
restricted_answer_key_read=false
scoring_performed=false
all four route directories processed
all generated V2 JSONL files parse
all generated V2 TOP10 CSV files parse
no path_depth=0 rows in any V2 JSONL or V2 TOP10 CSV
no empty edge_id_path in any V2 JSONL or V2 TOP10 CSV
all simple_path_valid=true
repaired_repeated_node_path_count=0 for every route
repaired_repeated_smiles_path_count=0 for every route
repaired_repeated_edge_path_count=0 for every route
contains_parent_copy_edge=false for every retained path
contains_source_self_loop_edge=false for every retained path
duplicate_case_smiles_path_rows=0 for every route
cases_exceeding_top10=0 for every route
MANIFEST.sha256 generated after all files and logs are final
sha256sum -c MANIFEST.sha256 passes for every file
archive identity sidecar exists and contains the final tarball SHA256
no stale in-package archive SHA256 is reported
```

Expected final corrected counts:

| Route | Expected retained rows | Expected zero-edge removed | Expected cases with non-empty simple path |
|---|---:|---:|---:|
| biotransformer_envmicro_multistep | 779 | 8 | 85 |
| envipath_bbd_rules_multistep | 745 | 5 | 88 |
| eclipse_predec_bbd_finetuned_10fold_multistep | 930 | 0 | 93 |
| eclipse_noec_bbd_finetuned_10fold_multistep_optional | 930 | 0 | 93 |

If observed values differ, do not force them. Report observed values and why.

## 11. Final status rules

If all checks pass:

```text
FINAL_STATUS=COMPLETE_MULTISTEP_SIMPLE_PATH_REPAIR_V2_CLEANUP_READY_FOR_LOCAL_AUDIT
```

If required route files are generated but a non-critical provenance note remains:

```text
FINAL_STATUS=COMPLETE_MULTISTEP_SIMPLE_PATH_REPAIR_V2_CLEANUP_WITH_PROVENANCE_NOTE_READY_FOR_LOCAL_AUDIT
```

If any route still contains zero-edge paths or repeated paths:

```text
FINAL_STATUS=FAIL_MULTISTEP_SIMPLE_PATH_REPAIR_V2_CLEANUP_NEEDS_REPAIR
```

## 12. Required final message after execution

After packaging, report only:

```text
return_folder=<absolute path>
return_archive=<absolute path>
archive_sha256=<sha256>
identity_sidecar=<absolute path>
final_status=<status string>
manifest_check=<PASS/FAIL>
restricted_answer_key_read=false
scoring_performed=false
zero_edge_rows_removed=<total and per-route>
retained_simple_path_rows=<per-route>
cases_with_nonempty_simple_path=<per-route>
```

Do not paste large tables into chat. The archive should contain the detailed tables.
