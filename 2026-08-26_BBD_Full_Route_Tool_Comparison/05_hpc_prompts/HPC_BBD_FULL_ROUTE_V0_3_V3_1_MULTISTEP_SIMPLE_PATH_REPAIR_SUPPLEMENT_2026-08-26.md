# HPC executor-only prompt — BBD full-route v0.3 v3.1 multistep simple-path repair supplement

Date: 2026-08-26  
Executor: chenyu / HPC  
Task type: repair supplement only; do not rerun prediction tools; do not score  
Expected return root:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

Expected return folder:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_supplement_20260826
```

Expected archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_supplement_20260826.tar.gz
```

## 0. One-sentence goal

The previous multistep return successfully produced bounded multistep predicted route **edge/node graphs**, but the returned `PREDICTED_ROUTE_PATHS.jsonl` files, especially for ECLIPSE, contain repeated nodes / repeated edges and therefore are not safe for direct path-level interpretation. This repair supplement should reuse the existing returned `PREDICTED_ROUTE_EDGES.jsonl` and `PREDICTED_ROUTE_NODES.csv` files and regenerate clean **simple acyclic predicted paths** only.

Do not rerun BioTransformer, enviPath, ECLIPSE, or any model inference.

Do not read restricted answer files.

Do not score.

## 1. Background and local audit findings

Previous multistep archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz
```

Expected archive SHA256:

```text
ee8e06fffe76bec29825702c18deb1211e33b7c4609ff3132be8428179fe83cf
```

Local audit conclusion:

```text
PASS for edge/node-level bounded multistep route expansion.
PARTIAL for path-level route reconstruction.
```

Reason:

```text
PREDICTED_ROUTE_PATHS.jsonl exists, but many paths are not simple paths.
ECLIPSE PREDEC and ECLIPSE NoEC path rows often repeat the same node, same SMILES, or same edge ID.
Therefore local scoring should not use the old PREDICTED_ROUTE_PATHS directly.
```

Observed local path QC:

| Route | Old path rows | Repeated-node paths | Repeated-edge paths |
|---|---:|---:|---:|
| biotransformer_envmicro_multistep | 786 | 49 | 21 |
| envipath_bbd_rules_multistep | 745 | 0 | 0 |
| eclipse_predec_bbd_finetuned_10fold_multistep | 930 | 917 | 828 |
| eclipse_noec_bbd_finetuned_10fold_multistep_optional | 930 | 921 | 834 |

This repair should make the path layer match the already valid edge/node graph layer.

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
10. Put all return files under:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

## 3. Allowed input

Use only this previous blind multistep prediction return:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz
```

Expected SHA256:

```text
ee8e06fffe76bec29825702c18deb1211e33b7c4609ff3132be8428179fe83cf
```

Allowed files inside the extracted archive:

```text
00_INPUT_AUDIT/strict_blind_identity.json
00_INPUT_AUDIT/previous_s1_prediction_package_identity.json
RUN_MANIFEST.json
02_ROUTE_STATUS/route_status_summary.csv
02_ROUTE_STATUS/route_blockers.json

03_ROUTE_EXPANSION/<route_id>/PREDICTED_ROUTE_EDGES.jsonl
03_ROUTE_EXPANSION/<route_id>/PREDICTED_ROUTE_NODES.csv
03_ROUTE_EXPANSION/<route_id>/ROUTE_EXPANSION_SUMMARY.csv
03_ROUTE_EXPANSION/<route_id>/ROUTE_EXPANSION_SUMMARY.md
```

Do not use old `PREDICTED_ROUTE_PATHS.jsonl` as a path source. You may audit it only to count old defects and show that the repair fixed them.

Do not use any `restricted/` files from the local benchmark build.

## 4. Routes to repair

Repair these route directories:

```text
biotransformer_envmicro_multistep
envipath_bbd_rules_multistep
eclipse_predec_bbd_finetuned_10fold_multistep
eclipse_noec_bbd_finetuned_10fold_multistep_optional
```

The NoEC route is optional/partial-depth in the previous return. Still repair its path layer from its existing edges/nodes, but mark:

```text
optional_route=true
previous_status=completed_with_partial_depth_runtime_cap_reached
```

## 5. Required repair logic

For each route:

1. Load `PREDICTED_ROUTE_NODES.csv`.
2. Load `PREDICTED_ROUTE_EDGES.jsonl`.
3. Keep only edge rows with:

```text
normalization_status == "ok"
source_node_id not empty
target_node_id not empty
source_smiles_canonical not empty
target_smiles_canonical not empty
```

4. Exclude direct self-loop edges from simple path traversal:

```text
source_node_id == target_node_id
source_smiles_canonical == target_smiles_canonical
target_is_source_copy == true
```

5. Exclude direct original-parent-copy edges from simple path traversal:

```text
target_is_original_parent_copy == true
```

6. Build a directed graph separately for each `full_route_case_id`.
7. Root node for each case is the node with:

```text
is_original_parent == True
```

If this is missing, fall back to the node whose `depth_first_seen == 0`.

8. Enumerate simple acyclic paths from the root, with these constraints:

```text
max_edges_per_path = 6
max_paths_per_case = 10
no repeated node_id inside one path
no repeated smiles_canonical inside one path
no repeated edge_id inside one path
```

9. Ranking / selection must be prediction-only:

Use existing prediction score fields only. Do not use answer information.

Recommended path ranking:

```text
1. Prefer longer simple paths, because this repair is for route expansion.
2. Then prefer higher path score if score semantics support higher-is-better.
3. For ECLIPSE log-likelihood scores, less negative / higher numeric value is better.
4. For no-score routes, use deterministic order by path length desc, then edge discovery order.
5. Deduplicate identical compound_smiles_canonical_path.
6. Keep top 10 simple paths per case.
```

10. `path_depth` must equal:

```text
len(edge_id_path)
```

11. `compound_node_id_path` length must equal:

```text
len(edge_id_path) + 1
```

12. `compound_smiles_canonical_path` length must equal:

```text
len(edge_id_path) + 1
```

13. `path_status` should be:

```text
simple_acyclic_path
```

14. `stopped_reason` should use one of:

```text
max_depth_reached
frontier_empty
no_clean_outgoing_edge
max_paths_per_case_cap
partial_depth_route_input
```

Do not write `complete` unless you define it as prediction-graph complete, and explain that it is not biological mineralization.

## 6. Important interpretation constraints

This repair is only for predicted path hygiene.

Do not claim:

```text
complete mineralization
complete environmental degradation
biologically confirmed path
correctness / accuracy / hit rate
```

Allowed wording:

```text
bounded simple predicted paths reconstructed from blind multistep prediction edge/node graphs
max depth <= 6
no scoring performed
restricted_answer_key_read=false
```

## 7. Required output structure

Create this return folder:

```text
bbd_full_route_v0_3_v3_1_multistep_simple_path_repair_supplement_20260826/
├── FINAL_STATUS.txt
├── README_BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_SUPPLEMENT.md
├── RUN_MANIFEST.json
├── MANIFEST.sha256
├── 00_INPUT_AUDIT/
│   ├── previous_multistep_package_identity.json
│   ├── previous_multistep_package_identity.md
│   └── allowed_input_files_used.csv
├── 01_REPAIRED_ROUTE_PATHS/
│   ├── biotransformer_envmicro_multistep/
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE.jsonl
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_TOP10_BY_CASE.csv
│   │   ├── SIMPLE_PATH_REPAIR_SUMMARY.csv
│   │   └── SIMPLE_PATH_REPAIR_SUMMARY.md
│   ├── envipath_bbd_rules_multistep/
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE.jsonl
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_TOP10_BY_CASE.csv
│   │   ├── SIMPLE_PATH_REPAIR_SUMMARY.csv
│   │   └── SIMPLE_PATH_REPAIR_SUMMARY.md
│   ├── eclipse_predec_bbd_finetuned_10fold_multistep/
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE.jsonl
│   │   ├── PREDICTED_ROUTE_PATHS_SIMPLE_TOP10_BY_CASE.csv
│   │   ├── SIMPLE_PATH_REPAIR_SUMMARY.csv
│   │   └── SIMPLE_PATH_REPAIR_SUMMARY.md
│   └── eclipse_noec_bbd_finetuned_10fold_multistep_optional/
│       ├── PREDICTED_ROUTE_PATHS_SIMPLE.jsonl
│       ├── PREDICTED_ROUTE_PATHS_SIMPLE_TOP10_BY_CASE.csv
│       ├── SIMPLE_PATH_REPAIR_SUMMARY.csv
│       └── SIMPLE_PATH_REPAIR_SUMMARY.md
├── 02_QC_NO_SCORING/
│   ├── old_path_defect_counts.csv
│   ├── repaired_path_qc_summary.csv
│   ├── actual_node_depth_summary_from_nodes_csv.csv
│   ├── clean_edge_traversal_summary.csv
│   ├── path_duplicate_check.csv
│   └── qc_summary.md
├── 03_EXECUTOR_AUDIT/
│   └── BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_SUPPLEMENT_EXECUTOR_AUDIT.md
├── scripts/
│   └── repair_bbd_full_route_v0_3_v3_1_multistep_simple_paths.py
└── logs/
    ├── input_audit.log
    ├── path_repair.log
    └── packaging.log
```

Do not include raw prediction outputs, model files, checkpoints, credentials, or full copied previous archive unless needed for a tiny manifest identity file.

## 8. Required `PREDICTED_ROUTE_PATHS_SIMPLE.jsonl` schema

Each JSONL row must include:

```text
full_route_case_id
scope
pollutant_name
pollutant_category
tool_id
route_id
optional_route
path_id
path_rank_within_case
path_depth
compound_node_id_path
compound_smiles_canonical_path
compound_inchikey_path
edge_id_path
edge_score_raw_path
edge_score_semantics_path
path_score_raw
path_score_semantics
path_status
stopped_reason
simple_path_valid
has_repeated_node_id
has_repeated_smiles_canonical
has_repeated_edge_id
contains_parent_copy_edge
contains_source_self_loop_edge
restricted_answer_key_read
scoring_performed
```

Expected invariant for every row:

```text
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

## 9. Required summary metrics

For each route, report:

```text
route_id
tool_id
optional_route
previous_edge_rows
previous_node_rows
old_path_rows
old_repeated_node_path_count
old_repeated_smiles_path_count
old_repeated_edge_path_count
clean_traversable_edge_count
excluded_self_loop_edge_count
excluded_parent_copy_edge_count
excluded_invalid_edge_count
input_parent_count
cases_with_root_node
cases_with_any_simple_path
cases_with_depth_1_simple_path
cases_with_depth_2_simple_path
cases_with_depth_3_simple_path
cases_with_depth_4_simple_path
cases_with_depth_5_simple_path
cases_with_depth_6_simple_path
max_simple_path_depth
simple_path_rows
repaired_repeated_node_path_count
repaired_repeated_smiles_path_count
repaired_repeated_edge_path_count
restricted_answer_key_read
scoring_performed
```

## 10. Acceptance checks before packaging

Run these checks and write the results into `02_QC_NO_SCORING/qc_summary.md` and `03_EXECUTOR_AUDIT/...md`.

Required pass conditions:

```text
previous_multistep_archive_sha256_match=true
restricted_answer_key_read=false
scoring_performed=false
all four route directories processed
all generated simple path files parse as JSONL
all generated TOP10 CSV files parse as CSV
all simple_path_valid=true
repaired_repeated_node_path_count=0 for every route
repaired_repeated_smiles_path_count=0 for every route
repaired_repeated_edge_path_count=0 for every route
contains_parent_copy_edge=false for every path
contains_source_self_loop_edge=false for every path
MANIFEST.sha256 generated after all files and logs are final
sha256sum -c MANIFEST.sha256 passes for every file
```

If a route cannot produce any simple path for a case, do not fake a path. Record it in summary counts only.

## 11. Suggested implementation outline

Use one small script:

```text
scripts/repair_bbd_full_route_v0_3_v3_1_multistep_simple_paths.py
```

Suggested steps:

```python
extract previous archive to a temporary working directory
verify archive sha256
for each route:
    load nodes
    load edges
    compute old path defect counts from old PREDICTED_ROUTE_PATHS.jsonl
    build clean directed adjacency from valid non-self non-parent-copy edges
    for each case:
        identify root node
        run DFS / beam-style traversal to max depth 6
        keep only simple paths with no repeated node/smiles/edge
        rank deterministically using prediction-only scores
        keep top 10
    write PREDICTED_ROUTE_PATHS_SIMPLE.jsonl
    write PREDICTED_ROUTE_PATHS_SIMPLE_TOP10_BY_CASE.csv
    write SIMPLE_PATH_REPAIR_SUMMARY.csv/md
write cross-route QC files
write executor audit
write README
write FINAL_STATUS.txt
write RUN_MANIFEST.json
write logs
generate MANIFEST.sha256 last
verify sha256sum -c MANIFEST.sha256
tar.gz the return folder
write identity sidecar
```

Important: `MANIFEST.sha256` must be generated after `logs/packaging.log` is fully closed/finalized. The previous return had a manifest mismatch only for `logs/packaging.log`; avoid repeating that.

## 12. Final status rules

If all checks pass:

```text
FINAL_STATUS=COMPLETE_MULTISTEP_SIMPLE_PATH_REPAIR_READY_FOR_LOCAL_AUDIT
```

If all route files are generated but one optional route has no simple paths due to its previous partial-depth input:

```text
FINAL_STATUS=COMPLETE_REQUIRED_ROUTES_SIMPLE_PATH_REPAIR_OPTIONAL_NOEC_PARTIAL_READY_FOR_LOCAL_AUDIT
```

If any required route fails:

```text
FINAL_STATUS=PARTIAL_MULTISTEP_SIMPLE_PATH_REPAIR_WITH_TYPED_BLOCKERS_READY_FOR_LOCAL_AUDIT
```

Write typed blockers in:

```text
03_EXECUTOR_AUDIT/BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_SUPPLEMENT_EXECUTOR_AUDIT.md
02_QC_NO_SCORING/qc_summary.md
RUN_MANIFEST.json
```

## 13. Required final message after execution

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
brief_route_summary=<one line per route>
```

Do not paste large tables into chat. The archive should contain the detailed tables.
