# HPC executor-only prompt — BBD known-pathway full-route v0.3 v3.1 three-tool blind predictions

Date: 2026-08-21  
Executor: chenyu / HPC  
Task type: blind tool execution only; scoring stays local  
Expected return root:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

Expected return folder:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821
```

Expected archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz
```

## 0. One-sentence goal

Run blind predictions for the 93-parent BBD known-pathway full-route v0.3 v3.1 candidate benchmark using:

```text
1. BioTransformer ENVMICRO
2. enviPath BBD Rules prediction, plus database lookup as a separate non-prediction layer
3. BBD-finetuned ECLIPSE current best route, i.e. PREDEC / predicted-EC-conditioned product prediction
```

Return raw outputs, normalized product candidates, route metadata, and typed blockers. Do not score against answers on HPC.

## 1. Hard rules

1. Use only the strict blind input listed below.
2. Do not read, copy, grep, package, or infer from any restricted answer file.
3. Do not run local scoring against accepted products.
4. Do not tune thresholds, beam sizes, EC cutoffs, or model choices using answer-derived information.
5. Keep enviPath database lookup separate from prediction output. Lookup is known-pathway retrieval, not blind prediction accuracy.
6. Do not modify production data, production model files, GitHub, or shared repository history.
7. Do not package enviPath credentials or credential values.
8. If a route is unavailable, return a typed blocker with evidence instead of silently substituting another route.
9. Put all returned files under:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

## 2. Input package

Use the supplied local package:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/21_BBD_Known_Pathway_Full_Route_Testset_2026-08-21/bbd_known_pathway_full_route_v0_3_candidate_v3_1_strict_blind_fix_20260821.tar.gz
```

If this package is copied to chenyu, place or locate it under the HPC project, for example:

```text
/root/projects/EnzymeCAGE-master/HPC_Inputs/bbd_known_pathway_full_route_v0_3_candidate_v3_1_strict_blind_fix_20260821.tar.gz
```

Known archive identity:

```text
archive_sha256=ea9bf0497592f686013c789d42259260c2c69ba00d8a073435d6408cf2e02d90
```

Inside the package, the only prediction input is:

```text
blind/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_1_BLIND_PARENT_INPUTS_FOR_PREDICTION_STRICT.csv
```

Known strict blind identity:

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

Important:

```text
full_route_case_id is an allowed case identifier.
It is not an answer leak even though the column name contains "route".
```

## 3. Forbidden local answer assets

Do not use these on HPC for this prediction run:

```text
restricted/
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_ROUTE_ANSWER_KEY.jsonl
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_REACTION_EDGES.csv
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_COMPOUND_NODES.csv
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_PARENT_ROUTE_SUMMARY.csv
BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_ROUTE_PATHS_PARENT_TO_TERMINAL.csv
any file containing accepted_product, answer_key, hit/miss/correctness, target product, route graph answer, reaction edge answer, or terminal product answer
```

Scoring will be done locally after the raw/normalized blind predictions return.

## 4. Prior validated tool entrypoints to reuse

Use these paths as a navigation map so you do not need to rediscover the tools from scratch.

### 4.1 BioTransformer ENVMICRO

Prior validated route index:

```text
/root/projects/EnzymeCAGE-master/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/BIOTRANSFORMER_ENVIPATH_PRIOR_VALIDATED_TEST_PATHS_FOR_CHENYU_2026-08-18.md
```

Prior BBD83 four-route script:

```text
/root/projects/EnzymeCAGE-master/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_bbd_known_pathway_v0_2_four_route_blind_rerun1_20260805/scripts/run_bbd_known_pathway_v0_2_four_route.py
```

Audited command template:

```bash
java -jar <biotransformer-3.0.0.jar> \
  -k pred \
  -b env \
  -ismi "<parent_smiles>" \
  -ocsv "<case_output_csv>" \
  -s 1
```

Known source identity from prior audits:

```text
tool_id=biotransformer_envmicro
repository=https://github.com/Wishartlab-openscience/Biotransformer.git
commit=7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
java=openjdk 1.8.x worked previously
```

Known historical jar locations, if still present:

```text
/tmp/enzymecage_m3_p1_2_1_three_tool_valid_single_parent_biotransformer_envmicro_prediction_rerun1_20260728/Biotransformer/target/biotransformer-3.0.0.jar
/tmp/enzymecage_m3_p1_2_1_three_tool_valid_single_parent_biotransformer_envmicro_prediction_rerun4_20260728/Biotransformer/target/biotransformer-3.0.0.jar
```

Do not assume `/tmp` still exists. If the jar is missing, rebuild from the audited commit and record source commit, build log, jar path, jar SHA256, Java version, and Maven version.

Note: prior packages have recorded more than one historical jar SHA256. Do not silently hide this. For this run, record the actual jar SHA256 used and whether it matches a prior audited jar.

### 4.2 enviPath direct prediction and lookup

Prior validated route index:

```text
/root/projects/EnzymeCAGE-master/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/BIOTRANSFORMER_ENVIPATH_PRIOR_VALIDATED_TEST_PATHS_FOR_CHENYU_2026-08-18.md
```

Prior BBD83 enviPath rerun script:

```text
/root/projects/EnzymeCAGE-master/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_bbd_known_pathway_v0_2_four_route_blind_rerun1_20260805/scripts/run_bbd_known_pathway_v0_2_envipath_rerun1.py
```

Prior API identity:

```text
envipath-python version=0.2.4
legacy_api_host=https://envipath.org/api/legacy/
database_search=GET https://envipath.org/api/legacy/search
prediction=POST form https://envipath.org/api/legacy/util hiddenMethod=predict
prediction_setting_id=https://envipath.org/setting/a0fbc3d8-ca45-44f1-9c3c-80d8531ffe25
prediction_setting_name=Global Setting - BBD Rules
EAWAG-BBD package=https://envipath.org/package/32de3cf4-e3e6-4168-956e-32fa5ddb0ce1
```

Credential source to use if present:

```text
/root/projects/EnzymeCAGE-master/HPC_Inputs/envipath_account_env.local.sh
```

Do not print or package credential values.

Required separation:

```text
predictions/envipath_prediction/        # one-step BBD Rules prediction using parent only
envipath_database_lookup/               # known-pathway database search / lookup; not prediction scoring
```

If the official prediction route is blocked but database lookup works, set:

```text
envipath_prediction_status=blocked_<specific_reason>
envipath_database_lookup_status=ok
```

### 4.3 ECLIPSE current best route

Use the already trained BBD-only fine-tuned ECLIPSE models from the 2026-08-17 / 2026-08-18 work. Do not retrain.

Prior ECLIPSE fullfold prompt:

```text
/root/projects/EnzymeCAGE-master/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/07_HPC_Prompts/HPC_CHEM_ECLIPSE_BBD_FINETUNE_FULLFOLD_AND_BBD83_PREDICTION_CONTINUATION_2026-08-17.md
```

Prior Soil/Sludge transfer prompt:

```text
/root/projects/EnzymeCAGE-master/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/20_Pollutant_TP_Prediction_Route_Evaluation_2026-08-19/04_HPC_Prompts/HPC_CHEM_ECLIPSE_BBD_FINETUNE_SOIL_SLUDGE_TRANSFER_EVAL_EXECUTOR_ONLY_PROMPT_2026-08-18.md
```

Prior Soil/Sludge transfer script, if present or extractable:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818/scripts/run_soil_sludge_transfer_eval.py
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818.tar.gz
```

Model paths observed in the prior return:

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

H-ECLIPSE hierarchy path observed previously:

```text
/root/projects/EnzymeCAGE-master/results/summary/hierarchy.csv
```

Actual prior ECLIPSE inference shape:

```python
from chem_eclipse.models.ECLIPSEProdModel import ECLIPSEProdModel

model.moe_config["use_enzyme"] = False
(pred_smiles_noec, pred_proba_noec), _ = model.smiles_to_smiles_inf(batch)

model.moe_config["use_enzyme"] = True
(pred_smiles_predec, pred_proba_predec), pred_ec = model.smiles_to_smiles_inf(batch)
```

For this run, the primary ECLIPSE route is:

```text
eclipse_predec_bbd_finetuned_10fold_aggregated
```

Meaning:

```text
parent SMILES -> predicted EC by H-ECLIPSE/PREDEC route -> BBD-finetuned product model -> top product candidates
```

Also run this diagnostic route if it is cheap after model loading:

```text
eclipse_noec_bbd_finetuned_10fold_aggregated
```

Do not run OracleEC / gold EC unless explicitly requested later. This task has no gold EC input.

## 5. Required prediction outputs

### 5.1 Minimum required: parent-level first-step candidate outputs

For each of the 93 input parents, each runnable prediction route should output top 10 product candidates.

Required route IDs:

```text
biotransformer_envmicro_s1
envipath_bbd_rules_s1
eclipse_predec_bbd_finetuned_10fold_aggregated_s1
```

Optional but strongly useful:

```text
eclipse_noec_bbd_finetuned_10fold_aggregated_s1
```

Write normalized prediction files:

```text
03_PREDICTIONS/biotransformer_envmicro_s1/PREDICTIONS_NORMALIZED.jsonl
03_PREDICTIONS/envipath_bbd_rules_s1/PREDICTIONS_NORMALIZED.jsonl
03_PREDICTIONS/eclipse_predec_bbd_finetuned_10fold_aggregated_s1/PREDICTIONS_NORMALIZED.csv
03_PREDICTIONS/eclipse_predec_bbd_finetuned_10fold_aggregated_s1/PREDICTIONS_FOLDWISE.jsonl
03_PREDICTIONS/eclipse_noec_bbd_finetuned_10fold_aggregated_s1/PREDICTIONS_NORMALIZED.csv
03_PREDICTIONS/eclipse_noec_bbd_finetuned_10fold_aggregated_s1/PREDICTIONS_FOLDWISE.jsonl
```

Each normalized row must include at least:

```text
full_route_case_id
scope
pollutant_name
pollutant_category
parent_smiles
parent_canonical_smiles
tool_id
route_id
prediction_depth
source_predicted_parent_smiles_canonical
prediction_rank
predicted_product_smiles_raw
predicted_product_smiles_canonical
predicted_product_inchikey
score_raw
score_semantics
fold_id
fold_count
raw_output_ref
normalization_status
case_status
```

Use:

```text
prediction_depth=1
source_predicted_parent_smiles_canonical=parent_canonical_smiles
```

for the first-step outputs.

### 5.2 Optional bounded full-route expansion outputs

If time and tool/runtime allow, also run bounded multi-step / route-expansion outputs. This is optional and must not block the required first-step outputs.

Recommended bounded scope:

```text
max_depth=3
max_frontier_per_parent_per_depth=10
deduplicate frontier by RDKit canonical SMILES
filter parent-copy self loops from the frontier
stop expanding a case if the frontier is empty
```

Acceptable tool-specific routes:

```text
BioTransformer: use vendor multistep -s 2 and/or -s 3 if supported, or iterative -s 1 with caps if cheap.
enviPath: use official multistep output if the API returns multi-generation graph edges; otherwise keep one-step only and say why.
ECLIPSE: iterative expansion is optional only; do not let it prevent the primary 93-parent PREDEC first-step run.
```

If run, write:

```text
04_OPTIONAL_ROUTE_EXPANSION/<route_id>/PREDICTED_ROUTE_EDGES.jsonl
04_OPTIONAL_ROUTE_EXPANSION/<route_id>/PREDICTED_ROUTE_NODES.csv
04_OPTIONAL_ROUTE_EXPANSION/<route_id>/ROUTE_EXPANSION_SUMMARY.md
```

Required edge fields:

```text
full_route_case_id
tool_id
route_id
source_depth
target_depth
source_smiles_canonical
target_smiles_raw
target_smiles_canonical
edge_rank
path_prefix_rank_or_id
score_raw
score_semantics
raw_output_ref
normalization_status
```

Again: no scoring on HPC.

## 6. Required metadata and blocker outputs

Create:

```text
bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821/
├── FINAL_STATUS.txt
├── README_BBD_FULL_ROUTE_V0_3_V3_1_THREE_TOOL_BLIND_PREDICTIONS.md
├── RUN_MANIFEST.json
├── MANIFEST.sha256
├── 00_INPUT_AUDIT/
│   ├── strict_blind_identity.json
│   ├── strict_blind_identity.md
│   └── copied_strict_blind_input.csv
├── 01_ASSET_DISCOVERY/
│   ├── biotransformer_asset_identity.json
│   ├── envipath_asset_identity.json
│   ├── eclipse_asset_identity.json
│   └── asset_discovery_log.md
├── 02_ROUTE_STATUS/
│   ├── route_status_summary.csv
│   ├── route_blockers.json
│   └── route_blockers.md
├── 03_PREDICTIONS/
│   ├── biotransformer_envmicro_s1/
│   ├── envipath_bbd_rules_s1/
│   ├── eclipse_predec_bbd_finetuned_10fold_aggregated_s1/
│   └── eclipse_noec_bbd_finetuned_10fold_aggregated_s1/
├── 04_OPTIONAL_ROUTE_EXPANSION/
├── 05_ENVIPATH_DATABASE_LOOKUP_SEPARATE/
│   ├── ENVIPATH_DATABASE_LOOKUP_RESULTS.jsonl
│   ├── ENVIPATH_DATABASE_LOOKUP_SUMMARY.csv
│   └── ENVIPATH_DATABASE_LOOKUP_NOTE.md
├── 06_EXECUTOR_AUDIT/
│   └── BBD_FULL_ROUTE_V0_3_V3_1_THREE_TOOL_BLIND_PREDICTIONS_EXECUTOR_AUDIT.md
├── scripts/
│   └── run_bbd_full_route_v0_3_v3_1_three_tool_blind_predictions.py
└── logs/
    ├── input_audit.log
    ├── asset_discovery.log
    ├── biotransformer_envmicro.log
    ├── envipath_prediction.log
    ├── envipath_database_lookup.log
    ├── eclipse_predec.log
    ├── eclipse_noec.log
    └── packaging.log
```

`route_status_summary.csv` should contain:

```text
route_id
status
input_parent_count
parents_with_nonempty_predictions
normalized_prediction_count
raw_output_count
typed_blocker
notes
```

Allowed status values:

```text
ok
completed_with_partial_errors
blocked
skipped_optional
```

Typed blockers:

```text
biotransformer_status=blocked_missing_java
biotransformer_status=blocked_missing_maven
biotransformer_status=blocked_missing_or_unbuildable_source
biotransformer_status=blocked_missing_database
biotransformer_status=blocked_jar_runtime_error
biotransformer_status=blocked_runtime_error

envipath_prediction_status=blocked_missing_credentials
envipath_prediction_status=blocked_login_failed
envipath_prediction_status=blocked_endpoint_unreachable
envipath_prediction_status=blocked_prediction_setting_unavailable
envipath_prediction_status=blocked_api_shape_changed
envipath_prediction_status=blocked_runtime_error

eclipse_status=blocked_missing_chem_eclipse
eclipse_status=blocked_missing_bbd_finetuned_fold_model
eclipse_status=blocked_missing_hierarchy
eclipse_status=blocked_model_load_failed
eclipse_status=blocked_inference_failed
```

## 7. Implementation notes

1. Adapt previous scripts, but update the input schema from old BBD83 v0.2:

```text
old case id: benchmark_case_id
new case id: full_route_case_id
old parent canonical maybe absent
new parent_canonical_smiles is present and already RDKit-audited
```

2. Do not carry old expected row count 83 into this run. The new strict blind has 93 rows.
3. Do not carry old old-BBD83 SHA checks into this run. Use the v3.1 SHA values above.
4. For BioTransformer, keep vendor output raw CSV per case and normalize to top 10 deduplicated canonical products.
5. For enviPath prediction, keep raw JSON per case and normalize first-generation products to top 10.
6. For ECLIPSE, aggregate across 10 folds by canonical predicted product, ranking by fold frequency first and mean score second, matching the prior Soil/Sludge transfer script unless you find a documented better method.
7. Preserve parent-copy predictions in raw normalized files. Add a boolean column:

```text
predicted_product_is_parent_copy=true|false
```

Local scoring will decide raw vs parent-filtered metrics.

## 8. Final packaging

After finishing, run:

```bash
cd /root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
tar -czf bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821
sha256sum bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz > bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz.identity.txt
```

Then append to the identity sidecar:

```text
archive_name=bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz
archive_path=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz
created_utc=<UTC time>
final_status=<FINAL_STATUS.txt content>
restricted_answer_key_read=false
strict_blind_rows=93
```

## 9. Success / blocked boundary

PASS:

```text
strict blind identity verified
restricted answer not read
at least one prediction route completed with normalized outputs
all unavailable routes have typed blockers
raw outputs and normalized outputs are packaged
archive and identity sidecar are written under HPC_Returned_Result_Summaries
```

Ideal complete status:

```text
FINAL_STATUS=COMPLETE_THREE_TOOL_BLIND_PREDICTIONS_READY_FOR_LOCAL_SCORING
```

Acceptable partial status:

```text
FINAL_STATUS=PARTIAL_COMPLETE_WITH_TYPED_ROUTE_BLOCKERS_READY_FOR_LOCAL_SCORING
```

BLOCKED:

```text
input archive missing or strict blind SHA mismatch
strict blind row count not 93
restricted answer file was read
all prediction routes blocked before producing normalized output
```

