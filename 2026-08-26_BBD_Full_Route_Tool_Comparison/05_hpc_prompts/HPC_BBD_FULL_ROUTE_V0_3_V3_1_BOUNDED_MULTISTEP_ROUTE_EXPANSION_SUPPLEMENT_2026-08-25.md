# HPC executor-only prompt — BBD full-route v0.3 v3.1 bounded multi-step route-expansion supplement

Date: 2026-08-25  
Executor: chenyu / HPC  
Task type: blind multi-step prediction supplement only; scoring stays local  
Expected return root:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

Expected return folder:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825
```

Expected archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz
```

## 0. One-sentence goal

The previous return successfully produced first-step predictions for 93 BBD full-route parents, but it did not produce real multi-step route expansion. This supplement should build bounded predicted route graphs by iteratively expanding predicted products, still using blind input only.

Required routes:

```text
1. BioTransformer ENVMICRO bounded multi-step route expansion
2. enviPath BBD Rules bounded multi-step route expansion
3. BBD-finetuned ECLIPSE PREDEC bounded multi-step route expansion
```

Optional diagnostic route:

```text
4. BBD-finetuned ECLIPSE NoEC bounded multi-step route expansion
```

Do not score against answers on HPC. Return predicted route edges/nodes/paths and raw outputs. Local scoring will be done after return.

## 1. Why this supplement is needed

Previous returned archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz
```

Local audit conclusion:

```text
The package is compliant and useful, but all normalized prediction rows have prediction_depth=1.
04_OPTIONAL_ROUTE_EXPANSION is empty.
Therefore it supports first-step scoring only, not true route-to-terminal / multi-step pathway scoring.
```

This supplement should not redo that whole task from scratch unless necessary. It should use the same strict blind parents and extend predictions across multiple depths.

## 2. Hard rules

1. Use only the strict blind parent input and previous prediction outputs listed below.
2. Do not read, copy, grep, package, or infer from any restricted answer file.
3. Do not run scoring against accepted products, downstream answer nodes, route edges, terminal nodes, or path answers.
4. Do not tune max depth, frontier size, filtering, ranking, EC cutoffs, or stopping rules using answer-derived information.
5. Do not retrain ECLIPSE or BioTransformer.
6. Do not modify production data, production model files, GitHub, or shared repository history.
7. Do not package enviPath credentials or credential values.
8. Keep enviPath database lookup separate from prediction. Database lookup is not a prediction route.
9. If a tool cannot support multi-step expansion, return a typed blocker for that route and still complete other routes.
10. Put all return files under:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

## 3. Allowed inputs

### 3.1 Strict blind parent package

Use the same strict blind package as the previous run:

```text
/root/projects/EnzymeCAGE-master/HPC_Inputs/bbd_known_pathway_full_route_v0_3_candidate_v3_1_strict_blind_fix_20260821.tar.gz
```

If not present there, locate the same archive under:

```text
/root/projects/EnzymeCAGE-master
/root/projects/EnzymeCAGE-master/custom/docs
/home/a/EnzymeCAGE/custom/docs
```

Expected archive SHA256:

```text
ea9bf0497592f686013c789d42259260c2c69ba00d8a073435d6408cf2e02d90
```

Inside it, the only prediction input is:

```text
blind/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_1_BLIND_PARENT_INPUTS_FOR_PREDICTION_STRICT.csv
```

Expected strict blind identity:

```text
rows=93
sha256=be11658b0ede11093bb8bb833281994cb2f507629eaf7b3524de74a4e46acb66
bytes=20776
```

Expected columns:

```text
full_route_case_id
scope
pollutant_name
pollutant_category
parent_smiles
parent_canonical_smiles
input_note
```

### 3.2 Previous first-step prediction package

Use this package as a starting point / provenance reference if available:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz
```

Expected archive SHA256:

```text
5eee73713a3034c75e44e149874758146f69f3d6ee83f91bfc2536a5170e6f5f
```

Important:

```text
You may reuse its depth-1 normalized predictions as the depth-1 layer.
You may reuse its asset discovery and tool-loading code.
Do not treat it as scored output.
Do not read any restricted local answer files.
```

Relevant previous files:

```text
03_PREDICTIONS/biotransformer_envmicro_s1/PREDICTIONS_NORMALIZED.jsonl
03_PREDICTIONS/envipath_bbd_rules_s1/PREDICTIONS_NORMALIZED.jsonl
03_PREDICTIONS/eclipse_predec_bbd_finetuned_10fold_aggregated_s1/PREDICTIONS_NORMALIZED.csv
03_PREDICTIONS/eclipse_noec_bbd_finetuned_10fold_aggregated_s1/PREDICTIONS_NORMALIZED.csv
scripts/run_bbd_full_route_v0_3_v3_1_three_tool_blind_predictions.py
01_ASSET_DISCOVERY/*.json
```

If the previous first-step package is unavailable, rerun depth-1 predictions as part of this supplement and record why.

## 4. Forbidden inputs

Do not use these in this HPC supplement:

```text
restricted/
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_ROUTE_ANSWER_KEY.jsonl
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_REACTION_EDGES.csv
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_COMPOUND_NODES.csv
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_PARENT_ROUTE_SUMMARY.csv
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_ROUTE_PATHS_PARENT_TO_TERMINAL.csv
any file containing accepted_product, answer_key, hit/miss/correctness, target product, route graph answer, reaction edge answer, terminal product answer, or path answer
```

## 5. Multi-step expansion definition

Use this common route-expansion definition for all tools.

For each original parent case and each route:

```text
depth 0 = original parent_canonical_smiles from strict blind
depth 1 = products predicted from depth 0 source
depth 2 = products predicted from selected depth 1 frontier nodes
...
depth 6 = products predicted from selected depth 5 frontier nodes
```

Required maximum depth:

```text
max_depth=6
```

Why depth 6:

```text
The local BBD full-route answer graph has average path depth about 3.5 and most paths are <=6 steps. Depth 6 is a practical route-level supplement without exploding to an unlimited search.
```

Frontier cap:

```text
max_frontier_nodes_per_case_per_depth=10
max_child_predictions_per_source=10
```

Frontier policy:

```text
At each depth, collect all child candidates from the current frontier.
Canonicalize with RDKit.
Remove invalid SMILES from the next frontier.
Flag parent-copy / source-copy predictions.
Do not expand source-copy self loops.
Deduplicate next frontier by canonical SMILES.
Rank next frontier by route-specific score if available; otherwise by prediction rank and discovery order.
Keep only the top 10 canonical nodes for the next depth.
```

Cycle policy:

```text
Track canonical SMILES already seen in the current case and route.
Do not expand a node again if it has already appeared in an earlier depth for that same case and route.
Still write the skipped edge/node with cycle_or_seen_before=true where relevant.
```

Stopping policy:

```text
Stop a case-route when the next frontier is empty.
Do not stop just because a predicted product looks like a small molecule or central metabolite.
Do not use any answer-derived terminal list on HPC.
```

## 6. Tool-specific routes

### 6.1 BioTransformer ENVMICRO

Use the same validated command family:

```bash
java -jar <biotransformer-3.0.0.jar> \
  -k pred \
  -b env \
  -ismi "<source_smiles>" \
  -ocsv "<case_depth_source_output_csv>" \
  -s 1
```

For route expansion, prefer iterative one-step calls:

```text
source node at depth d -> BioTransformer -s 1 -> child nodes at depth d+1
```

This gives cleaner source→target edge provenance than one opaque `-s 6` call.

If the BioTransformer vendor output has enough information to reconstruct `-s 2` or `-s 3` lineage, you may also run it as a diagnostic, but do not replace the required iterative edge table unless lineage is clear.

Preserve raw CSV per source node:

```text
03_ROUTE_EXPANSION/biotransformer_envmicro_multistep/raw/<full_route_case_id>/depth_<d>/source_<source_node_id>.csv
```

If BioTransformer rejects a source molecule, write a source-level blocker row and continue with the rest of the frontier.

### 6.2 enviPath BBD Rules

Use the same validated prediction route:

```text
legacy_api_host=https://envipath.org/api/legacy/
prediction=POST form https://envipath.org/api/legacy/util hiddenMethod=predict
prediction_setting_id=https://envipath.org/setting/a0fbc3d8-ca45-44f1-9c3c-80d8531ffe25
prediction_setting_name=Global Setting - BBD Rules
```

Credential source if present:

```text
/root/projects/EnzymeCAGE-master/HPC_Inputs/envipath_account_env.local.sh
```

Do not print or package credentials.

Two acceptable implementation paths:

1. If the official API response contains multi-generation nodes/edges for a single parent, extract that graph directly and record the API parameters.
2. If the official API only gives reliable one-step products, use iterative one-step calls over the frontier, exactly like BioTransformer.

Keep database lookup separate:

```text
05_ENVIPATH_DATABASE_LOOKUP_SEPARATE/
```

Database lookup is optional in this supplement. If included, it is for provenance/debugging only and must not be mixed into prediction route graphs.

### 6.3 ECLIPSE PREDEC, current best route

Use the existing BBD-finetuned 10-fold ECLIPSE product models. Do not retrain.

Expected model directories:

```text
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_0_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_1_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_2_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_3_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_4_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_5_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_6_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_7_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_8_uspto_rdkit/
/root/projects/EnzymeCAGE-master/results/ECLIPSEProdModel/bbd_40_3_9_uspto_rdkit/
```

Each fold should contain:

```text
config.json
tokens.json
split_bbd.json
expert/checkpoints/*.ckpt
eclipse/model.pkl
eclipse/config.json
```

Prior inference shape:

```python
model.moe_config["use_enzyme"] = True
(pred_smiles_predec, pred_proba_predec), pred_ec = model.smiles_to_smiles_inf(batch)
```

For each frontier source SMILES, run PREDEC and aggregate across 10 folds:

```text
group by canonical predicted product
rank by fold frequency descending, then mean score descending
keep top 10
```

Record predicted EC output if available:

```text
predicted_ec_raw
predicted_ec_rank_or_score
ec_source=PREDEC_predicted_by_ECLIPSE
```

### 6.4 Optional ECLIPSE NoEC diagnostic

If cheap after loading the same models, also run:

```python
model.moe_config["use_enzyme"] = False
(pred_smiles_noec, pred_proba_noec), _ = model.smiles_to_smiles_inf(batch)
```

Label route:

```text
eclipse_noec_bbd_finetuned_10fold_multistep_optional
```

If runtime is too high, skip this optional route and write:

```text
eclipse_noec_multistep_status=skipped_optional_runtime_control
```

## 7. Required outputs

Create this return structure:

```text
bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825/
├── FINAL_STATUS.txt
├── README_BBD_FULL_ROUTE_V0_3_V3_1_BOUNDED_MULTISTEP_ROUTE_EXPANSION_SUPPLEMENT.md
├── RUN_MANIFEST.json
├── MANIFEST.sha256
├── 00_INPUT_AUDIT/
│   ├── strict_blind_identity.json
│   ├── strict_blind_identity.md
│   ├── previous_s1_prediction_package_identity.json
│   └── copied_strict_blind_input.csv
├── 01_ASSET_DISCOVERY/
│   ├── biotransformer_asset_identity.json
│   ├── envipath_asset_identity.json
│   ├── eclipse_asset_identity.json
│   └── asset_discovery_log.md
├── 02_ROUTE_STATUS/
│   ├── route_status_summary.csv
│   ├── source_level_blockers.csv
│   ├── route_blockers.json
│   └── route_blockers.md
├── 03_ROUTE_EXPANSION/
│   ├── biotransformer_envmicro_multistep/
│   │   ├── PREDICTED_ROUTE_EDGES.jsonl
│   │   ├── PREDICTED_ROUTE_NODES.csv
│   │   ├── PREDICTED_ROUTE_PATHS.jsonl
│   │   ├── ROUTE_EXPANSION_SUMMARY.csv
│   │   ├── ROUTE_EXPANSION_SUMMARY.md
│   │   └── raw/
│   ├── envipath_bbd_rules_multistep/
│   │   ├── PREDICTED_ROUTE_EDGES.jsonl
│   │   ├── PREDICTED_ROUTE_NODES.csv
│   │   ├── PREDICTED_ROUTE_PATHS.jsonl
│   │   ├── ROUTE_EXPANSION_SUMMARY.csv
│   │   ├── ROUTE_EXPANSION_SUMMARY.md
│   │   └── raw/
│   ├── eclipse_predec_bbd_finetuned_10fold_multistep/
│   │   ├── PREDICTED_ROUTE_EDGES.jsonl
│   │   ├── PREDICTED_ROUTE_NODES.csv
│   │   ├── PREDICTED_ROUTE_PATHS.jsonl
│   │   ├── PREDICTED_ROUTE_PATHS_TOP10_BY_CASE.csv
│   │   ├── ROUTE_EXPANSION_SUMMARY.csv
│   │   ├── ROUTE_EXPANSION_SUMMARY.md
│   │   └── raw_or_intermediate/
│   └── eclipse_noec_bbd_finetuned_10fold_multistep_optional/
├── 04_QC_ONLY_NO_SCORING/
│   ├── prediction_depth_distribution.csv
│   ├── per_case_frontier_size_by_depth.csv
│   ├── invalid_or_unparseable_prediction_rows.csv
│   ├── parent_copy_or_self_loop_rows.csv
│   ├── cycle_or_seen_before_rows.csv
│   └── qc_summary.md
├── 05_ENVIPATH_DATABASE_LOOKUP_SEPARATE/
├── 06_EXECUTOR_AUDIT/
│   └── BBD_FULL_ROUTE_V0_3_V3_1_BOUNDED_MULTISTEP_ROUTE_EXPANSION_SUPPLEMENT_EXECUTOR_AUDIT.md
├── scripts/
│   └── run_bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion.py
└── logs/
    ├── input_audit.log
    ├── asset_discovery.log
    ├── biotransformer_multistep.log
    ├── envipath_multistep.log
    ├── eclipse_predec_multistep.log
    ├── eclipse_noec_multistep_optional.log
    └── packaging.log
```

## 8. Required edge schema

Each `PREDICTED_ROUTE_EDGES.jsonl` row must include:

```text
full_route_case_id
scope
pollutant_name
pollutant_category
tool_id
route_id
original_parent_smiles
original_parent_canonical_smiles
source_node_id
target_node_id
source_depth
target_depth
source_smiles_raw
source_smiles_canonical
target_smiles_raw
target_smiles_canonical
target_inchikey
edge_rank_from_source
edge_rank_global_within_case_depth
path_score_raw
path_score_semantics
local_edge_score_raw
local_edge_score_semantics
fold_id
fold_count
predicted_ec_raw
ec_source
raw_output_ref
normalization_status
source_status
target_is_source_copy
target_is_original_parent_copy
cycle_or_seen_before
expanded_to_next_depth
```

Notes:

```text
source_depth starts at 0 for the original parent.
target_depth = source_depth + 1.
Do not leave source_smiles_canonical or target_smiles_canonical blank for ok rows.
```

## 9. Required node schema

Each `PREDICTED_ROUTE_NODES.csv` row must include:

```text
full_route_case_id
tool_id
route_id
node_id
depth_first_seen
smiles_raw_first_seen
smiles_canonical
inchikey
is_original_parent
is_frontier_expanded
first_source_node_id
best_path_score_raw
best_path_score_semantics
seen_count
invalid_reason
```

## 10. Required path schema

`PREDICTED_ROUTE_PATHS.jsonl` should contain reconstructed predicted paths, at least top 10 per case if full path enumeration is large.

Required fields:

```text
full_route_case_id
tool_id
route_id
path_id
path_depth
compound_smiles_canonical_path
compound_node_id_path
edge_id_path
path_score_raw
path_score_semantics
path_status
stopped_reason
```

Allowed stopped reasons:

```text
max_depth_reached
frontier_empty
all_candidates_invalid
all_candidates_seen_before
tool_blocked_for_frontier
runtime_cap_reached
```

## 11. QC summaries

For each route, report:

```text
input_parent_count
max_depth_requested
max_depth_reached
parents_with_depth_1
parents_with_depth_2
parents_with_depth_3
parents_with_depth_4
parents_with_depth_5
parents_with_depth_6
total_predicted_nodes
total_predicted_edges
total_predicted_paths
invalid_prediction_count
self_loop_count
cycle_or_seen_before_count
source_level_blocker_count
raw_output_count
restricted_answer_key_read
scoring_performed
```

Do not include Hit@K, accuracy, recall, MRR, correct/incorrect, or answer-derived fields.

## 12. Runtime controls

This can be slower than one-step prediction. Use conservative bounds, but complete useful route graphs.

Recommended control:

```text
max_depth=6
max_frontier_nodes_per_case_per_depth=10
max_child_predictions_per_source=10
```

If one route becomes too slow, do not kill the whole job. Instead:

```text
finish other routes
write partial outputs for the slow route
record stopped_reason=runtime_cap_reached
record route status=completed_with_partial_depth
```

Suggested minimum acceptable partial if runtime forces stopping:

```text
depth>=3 for all three required routes
or depth>=6 for at least BioTransformer and ECLIPSE PREDEC, with enviPath partial/blocker documented
```

But the target is still:

```text
depth 6 for BioTransformer ENVMICRO, enviPath BBD Rules, and ECLIPSE PREDEC.
```

## 13. Final packaging

After finishing:

```bash
cd /root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
tar -czf bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825
sha256sum bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz > bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz.identity.txt
```

Append to the identity sidecar:

```text
archive_name=bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz
archive_path=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz
created_utc=<UTC time>
final_status=<FINAL_STATUS.txt content>
restricted_answer_key_read=false
scoring_performed=false
strict_blind_rows=93
max_depth_requested=6
```

## 14. Success / blocked boundary

Ideal complete status:

```text
FINAL_STATUS=COMPLETE_BOUNDED_MULTISTEP_ROUTE_EXPANSION_READY_FOR_LOCAL_SCORING
```

Acceptable partial status:

```text
FINAL_STATUS=PARTIAL_BOUNDED_MULTISTEP_ROUTE_EXPANSION_WITH_TYPED_BLOCKERS_READY_FOR_LOCAL_SCORING
```

PASS conditions:

```text
strict blind identity verified
restricted answer not read
scoring not performed
at least BioTransformer, enviPath prediction, and ECLIPSE PREDEC have route-expansion outputs or typed blockers
PREDICTED_ROUTE_EDGES and PREDICTED_ROUTE_NODES exist for completed routes
prediction depth distribution is reported
archive and identity sidecar are written under HPC_Returned_Result_Summaries
```

BLOCKED conditions:

```text
input strict blind archive missing or SHA mismatch
strict blind row count not 93
restricted answer file was read
all three required routes blocked before producing any route-expansion edge output
```

