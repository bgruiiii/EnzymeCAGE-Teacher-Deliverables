# Local audit — BBD full-route v0.3 v3.1 multistep simple-path repair v2 cleanup supplement

Date: 2026-08-26  
Audited archive:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_v2_cleanup_supplement_20260826.tar.gz
```

Identity sidecar:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_v2_cleanup_supplement_20260826.tar.gz.identity.txt
```

Previous repair package used as input:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_supplement_20260826.tar.gz
```

## 1. Bottom-line verdict

V2 cleanup package:

```text
PASS
```

Teacher-facing path-layer readiness:

```text
PASS_FOR_TEACHER_FACING_PATH_LAYER
```

Plain-language conclusion:

```text
This v2 cleanup fixed the two residual issues from the previous simple-path repair package.

1. All root-only zero-edge placeholder paths were removed.
2. Path coverage summaries now correctly count only non-empty simple paths.
3. Archive identity is clean: the final tarball SHA256 is recorded in the sidecar only, and no stale in-package archive SHA256 remains.
4. MANIFEST.sha256 passes for all extracted files.

The path layer is now clean enough to use in the final local/tool-comparison report, with the scientific caveat that these are bounded predicted paths over the BBD-local route graph, not complete mineralization or biologically confirmed full environmental degradation.
```

## 2. Archive identity and manifest

Actual local archive SHA256:

```text
13107f9fa6b376327e817b64373bd58e6c0db635dc563de848c156dd49e6a592
```

Identity sidecar reports the same SHA256:

```text
13107f9fa6b376327e817b64373bd58e6c0db635dc563de848c156dd49e6a592  bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_v2_cleanup_supplement_20260826.tar.gz
```

Sidecar status:

```text
final_status=COMPLETE_MULTISTEP_SIMPLE_PATH_REPAIR_V2_CLEANUP_READY_FOR_LOCAL_AUDIT
restricted_answer_key_read=false
scoring_performed=false
archive_sha256_recorded_in_sidecar_only=true
```

Internal manifest:

```text
sha256sum -c MANIFEST.sha256
```

Result:

```text
PASS for all extracted files
```

No stale in-package archive SHA256 was found. The package correctly records final archive SHA256 in the sidecar only.

## 3. Input and scope audit

Previous repair package identity:

```text
previous_repair_archive_sha256=5fa02f1d566ede109a9c6d731f5dd67bfe2021c0592010e6e870b7dbed13dc4d
previous_repair_archive_sha256_match=true
allowed_input_files_present=32
allowed_input_files_total=32
restricted_answer_key_read=false
scoring_performed=false
```

Package scope is correct for a cleanup-only return:

```text
00_INPUT_AUDIT/
01_REPAIRED_ROUTE_PATHS_V2/
02_QC_NO_SCORING/
03_EXECUTOR_AUDIT/
scripts/
logs/
```

No model checkpoint, raw prediction output directory, enviPath credential, or restricted answer table was packaged.

Focused text search found no answer-key / hit-rate / target-product leakage. Hits were limited to compliance statements such as `restricted_answer_key_read=false`.

## 4. V2 output files

All expected route folders are present:

```text
01_REPAIRED_ROUTE_PATHS_V2/biotransformer_envmicro_multistep/
01_REPAIRED_ROUTE_PATHS_V2/envipath_bbd_rules_multistep/
01_REPAIRED_ROUTE_PATHS_V2/eclipse_predec_bbd_finetuned_10fold_multistep/
01_REPAIRED_ROUTE_PATHS_V2/eclipse_noec_bbd_finetuned_10fold_multistep_optional/
```

Each route folder contains:

```text
PREDICTED_ROUTE_PATHS_SIMPLE_V2.jsonl
PREDICTED_ROUTE_PATHS_SIMPLE_V2_TOP10_BY_CASE.csv
SIMPLE_PATH_REPAIR_V2_SUMMARY.csv
SIMPLE_PATH_REPAIR_V2_SUMMARY.md
```

## 5. Zero-edge placeholder cleanup

Removed rows:

| Route | Old rows | Zero-edge rows removed | Retained rows | Cases with non-empty simple path |
|---|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 787 | 8 | 779 | 85/93 |
| enviPath BBD Rules | 750 | 5 | 745 | 88/93 |
| ECLIPSE PREDEC | 930 | 0 | 930 | 93/93 |
| ECLIPSE NoEC optional | 930 | 0 | 930 | 93/93 |

Removed zero-edge placeholder IDs:

```text
BioTransformer ENVMICRO:
FR-BBD3-CAND-c0347__sp01
FR-BBD3-PARENT-c0039__sp01
FR-BBD3-PARENT-c0352__sp01
FR-BBD3-PARENT-c0426__sp01
FR-BBD3-PARENT-c0444__sp01
FR-BBD3-PARENT-c0526__sp01
FR-BBD3-PARENT-c0939__sp01
FR-BBD3-PARENT-c1039__sp01

enviPath BBD Rules:
FR-BBD3-PARENT-c0039__sp01
FR-BBD3-PARENT-c0116__sp01
FR-BBD3-PARENT-c0444__sp01
FR-BBD3-PARENT-c0939__sp01
FR-BBD3-PARENT-c1201__sp01
```

This exactly matches the local audit request.

## 6. Independent V2 path validation

This audit independently parsed every `PREDICTED_ROUTE_PATHS_SIMPLE_V2.jsonl` and every `PREDICTED_ROUTE_PATHS_SIMPLE_V2_TOP10_BY_CASE.csv`.

Required invariants checked:

```text
JSONL parses
CSV parses
path_depth >= 1
edge_id_path is non-empty
path_depth == len(edge_id_path)
len(compound_node_id_path) == len(edge_id_path) + 1
len(compound_smiles_canonical_path) == len(edge_id_path) + 1
no repeated node ID
no repeated canonical SMILES
no repeated edge ID
simple_path_valid == true
contains_parent_copy_edge == false
contains_source_self_loop_edge == false
restricted_answer_key_read == false
scoring_performed == false
path_rank_within_case between 1 and 10
no case has more than 10 retained paths
no duplicate case+SMILES path rows
```

Independent validation result:

| Route | JSONL rows | CSV rows | Cases | Max paths/case | Duplicate SMILES-path rows | Validation failures |
|---|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 779 | 779 | 85 | 10 | 0 | 0 |
| enviPath BBD Rules | 745 | 745 | 88 | 10 | 0 | 0 |
| ECLIPSE PREDEC | 930 | 930 | 93 | 10 | 0 | 0 |
| ECLIPSE NoEC optional | 930 | 930 | 93 | 10 | 0 | 0 |

## 7. V2 path-depth distribution

Independent path-depth distribution:

| Route | depth1 | depth2 | depth3 | depth4 | depth5 | depth6 |
|---|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 2 | 9 | 1 | 1 | 3 | 763 |
| enviPath BBD Rules | 11 | 112 | 118 | 163 | 74 | 267 |
| ECLIPSE PREDEC | 0 | 0 | 0 | 0 | 0 | 930 |
| ECLIPSE NoEC optional | 0 | 0 | 0 | 41 | 37 | 852 |

No `path_depth=0` rows remain.

Important interpretation note:

```text
ECLIPSE NoEC was optional and previous execution was partial-depth by runtime cap. Its V2 simple paths are graph paths reconstructed from existing generated nodes/edges; do not reinterpret this as a fresh NoEC expansion run to depth 6.
```

## 8. V1-to-V2 diff check

This audit compared V2 rows against the previous V1 simple-path repair package.

Result:

```text
BioTransformer: V2 removed exactly 8 rows, all zero-edge placeholders; no added rows; no retained-row content changes.
enviPath: V2 removed exactly 5 rows, all zero-edge placeholders; no added rows; no retained-row content changes.
ECLIPSE PREDEC: no rows removed, added, or changed.
ECLIPSE NoEC: no rows removed, added, or changed.
```

Therefore V2 is a surgical cleanup of V1, not a rerun or hidden rewrite.

## 9. Remaining scientific caveat

This package fixes the path hygiene layer. It does not change the scientific scope:

```text
These are bounded predicted simple paths up to depth <= 6, reconstructed from blind multistep prediction graphs.
They are not evidence of complete mineralization.
They are not biologically confirmed full degradation routes.
They should be interpreted against BBD-local known route endpoints / graph nodes, with scoring performed only locally against restricted answers.
```

## 10. Recommended use

This v2 package can be used as the clean path-layer evidence for the final BBD full-route tool-comparison report.

Recommended wording:

```text
The multistep route-expansion path layer was repaired and cleaned in v2. All retained paths are non-empty simple paths with no repeated nodes, no repeated SMILES, no repeated edge IDs, and no parent/self-loop edges. Corrected non-empty path coverage is BioTransformer 85/93, enviPath BBD Rules 88/93, ECLIPSE PREDEC 93/93, and optional ECLIPSE NoEC 93/93. No scoring was performed on HPC and no restricted answer files were read.
```

No further chenyu repair is needed for the simple-path cleanup layer.
