# HPC executor-only prompt — enviPath Soil/Sludge known-pathway lookup supplement

Date: 2026-08-19  
Executor: chenyu / HPC  
Task type: lookup/audit supplement only; do not rerun ECLIPSE training or prediction  
Expected return root:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

Expected return folder:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/envipath_soil_sludge_known_pathway_lookup_supplement_20260819
```

Expected archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/envipath_soil_sludge_known_pathway_lookup_supplement_20260819.tar.gz
```

## 0. Goal

Use the existing enviPath Soil/Sludge assets to audit the **known-pathway lookup route** for the same Soil/Sludge evaluation set used in:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818
```

Question to answer:

```text
For the 1788 Soil/Sludge parent compounds, can enviPath lookup recover the expected Soil/Sludge records and accepted transformation products?
```

Important:

```text
This is not a prediction accuracy test.
This is an oracle-like known-pathway retrieval / data integrity / lookup-capability audit.
Do not mix these lookup results into BioTransformer/ECLIPSE Hit@K prediction metrics.
```

## 1. Hard rules

1. Do not retrain or rerun ECLIPSE.
2. Do not rerun BioTransformer unless only needed for metadata repair; this task is enviPath lookup only.
3. Do not score database lookup as a prediction model.
4. Do not expose or package enviPath credentials.
5. Do not modify production data, model files, or GitHub.
6. Use typed blockers if an input file is missing.
7. Put all return files under:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

## 2. Inputs

### 2.1 Prior Soil/Sludge transfer return

Use this existing return directory if present:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818
```

If only the archive exists, extract it read-only into a task scratch directory:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818.tar.gz
```

Required files from that package:

```text
01_EVAL_SET/soil_sludge_unique_parent_blind_inputs.csv
01_EVAL_SET/soil_sludge_unique_parent_answer_key_RESTRICTED.csv
01_EVAL_SET/soil_sludge_parent_product_dedup.csv
01_EVAL_SET/soil_sludge_raw_rows_canonicalized.csv
02_OVERLAP_AUDIT/bbd_overlap_audit.csv
```

The restricted answer key may be used in this task because this is a local lookup audit, not a blind prediction run.

### 2.2 enviPath assets

Use the already downloaded assets:

```text
/root/projects/EnzymeCAGE-master/data/envipath.csv
/root/projects/EnzymeCAGE-master/data/envipath/bbd.json
/root/projects/EnzymeCAGE-master/data/envipath/soil.json
/root/projects/EnzymeCAGE-master/data/envipath/sludge.json
```

Known identities:

| Dataset | File | Package ID | compounds | reactions | pathways |
|---|---|---|---:|---:|---:|
| BBD | `bbd.json` | `32de3cf4` | 1399 | 1480 | 219 |
| Soil | `soil.json` | `5882df9c` | 2608 | 2445 | 317 |
| Sludge | `sludge.json` | `521c547a` | 1067 | 494 | 183 |

Processed table:

```text
data/envipath.csv
rows: 4630
BBD rows: 1549
Soil rows: 2584
Sludge rows: 497
columns include: rdkit_reactants / rdkit_products / ec_num / dataset / pathway
```

## 3. Required lookup layers

Run two lookup layers if possible.

### 3.1 Required: local snapshot exact lookup

This is the main required layer.

Build a lookup index from:

```text
/root/projects/EnzymeCAGE-master/data/envipath.csv
```

Steps:

1. Load all Soil and Sludge rows.
2. Canonicalize `rdkit_reactants` and `rdkit_products` with RDKit.
3. Build an index:

```text
parent_canonical_smiles -> rows with product_canonical_smiles, dataset, pathway, ec_num, row_id/reaction_id if available
```

4. For every parent in `soil_sludge_unique_parent_blind_inputs.csv`, query this index by canonical parent SMILES.
5. Compare returned products against `soil_sludge_unique_parent_answer_key_RESTRICTED.csv`.

Expected if parsing is internally consistent:

```text
parent_found_rate should be near 100%
product_recall should be near 100%
```

If not, identify whether the issue is:

```text
canonicalization mismatch
dataset label mismatch
multi-reactant / mixture parent
salt / counterion representation
missing row from envipath.csv
answer-key construction mismatch
```

### 3.2 Optional / bounded: official enviPath API search check

If credentials and endpoint access are available, run a bounded official API check.

Credential source, if present:

```text
/root/projects/EnzymeCAGE-master/HPC_Inputs/envipath_account_env.local.sh
```

Do not print or package credential values.

Use prior validated enviPath route information:

```text
envipath-python version = 0.2.4
primary_host = https://envipath.org
legacy_api_host = https://envipath.org/api/legacy/
Soil package API = https://envipath.org/api/legacy/package/5882df9c-????-????-????-????????????
Sludge package API = https://envipath.org/api/legacy/package/521c547a-????-????-????-????????????
```

If the full package UUIDs are available in the local JSON metadata, use them. If only the short package IDs are available, record that limitation and use local snapshot lookup as the authoritative full audit.

Do not make uncontrolled remote requests.

Recommended API scope:

1. Run a stratified sample of at least 100 parents:
   - Soil-only parents;
   - Sludge-only parents;
   - parents with BBD overlap;
   - parents with multiple accepted products;
   - parents that local lookup misses, if any.
2. If the API route is stable and request volume is acceptable, optionally run all 1788 parents with rate limiting.
3. Record request count, HTTP status distribution, and login status without secrets.

If official API search is not feasible, set:

```text
official_api_lookup_status = blocked_or_skipped
```

and explain why. This is not a failure of the required local snapshot lookup.

## 4. Required outputs

Create:

```text
envipath_soil_sludge_known_pathway_lookup_supplement_20260819/
├── FINAL_STATUS.txt
├── README_ENVIPATH_SOIL_SLUDGE_KNOWN_PATHWAY_LOOKUP_SUPPLEMENT.md
├── MANIFEST.sha256
├── 00_INPUT_MANIFEST/
│   ├── input_manifest.json
│   └── input_manifest.md
├── 01_LOCAL_SNAPSHOT_LOOKUP/
│   ├── local_snapshot_parent_lookup_results.csv
│   ├── local_snapshot_product_recall_by_parent.csv
│   ├── local_snapshot_unmatched_parents.csv
│   ├── local_snapshot_product_mismatch_details.csv
│   └── local_snapshot_lookup_summary.md
├── 02_OFFICIAL_API_LOOKUP_OPTIONAL/
│   ├── official_api_lookup_results.csv
│   ├── official_api_lookup_summary.md
│   ├── official_api_request_audit.json
│   └── official_api_blocker_or_skip_reason.md
├── 03_COMPARISON_WITH_PREDICTION_ROUTES/
│   ├── lookup_vs_prediction_summary.md
│   └── lookup_vs_prediction_parent_level_join.csv
├── 04_EXECUTOR_AUDIT/
│   └── ENVIPATH_SOIL_SLUDGE_KNOWN_PATHWAY_LOOKUP_SUPPLEMENT_EXECUTOR_AUDIT.md
├── scripts/
│   └── run_envipath_soil_sludge_lookup_supplement.py
└── logs/
    ├── local_snapshot_lookup.log
    ├── official_api_lookup.log
    └── packaging.log
```

## 5. Required columns

### 5.1 `local_snapshot_parent_lookup_results.csv`

Required columns:

```text
parent_id
parent_smiles
parent_smiles_rdkit_canonical
lookup_status
matched_dataset_list
matched_pathway_list
matched_row_count
matched_product_count
matched_product_smiles_list
accepted_product_count
accepted_product_smiles_list
all_accepted_products_recovered
product_recall
product_precision_against_answer
notes
```

Allowed `lookup_status`:

```text
found_exact_parent
not_found
canonicalization_mismatch
ambiguous_mixture_or_salt
error
```

### 5.2 `local_snapshot_product_recall_by_parent.csv`

One row per parent:

```text
parent_id
parent_smiles_rdkit_canonical
datasets_from_answer
num_accepted_products
num_lookup_products
num_accepted_products_recovered
product_recall
lookup_extra_products_count
all_accepted_products_recovered
```

### 5.3 `local_snapshot_product_mismatch_details.csv`

One row per missing or extra product:

```text
parent_id
parent_smiles_rdkit_canonical
mismatch_type
product_smiles_rdkit_canonical
product_source
dataset
pathway
row_id_or_reaction_id
notes
```

Allowed `mismatch_type`:

```text
accepted_product_not_recovered_by_lookup
lookup_product_not_in_answer_key
```

### 5.4 `lookup_vs_prediction_parent_level_join.csv`

Join local lookup results with prior ECLIPSE/BioTransformer per-parent outcomes if available.

Required columns:

```text
parent_id
parent_smiles_rdkit_canonical
lookup_status
all_accepted_products_recovered_by_lookup
lookup_product_recall
eclipse_noec_hit10
eclipse_predec_hit10
biotransformer_hit10
notes
```

If BioTransformer per-parent scoring is unavailable from the prior package, derive `biotransformer_hit10` from:

```text
03_PREDICTIONS/biotransformer_envmicro_top10_predictions.csv
01_EVAL_SET/soil_sludge_unique_parent_answer_key_RESTRICTED.csv
```

Do not rerun BioTransformer for this join.

## 6. Required summary metrics

Report local snapshot lookup metrics:

```text
num_parents
parent_found_count
parent_found_rate
parents_all_accepted_products_recovered
all_products_recovered_parent_rate
accepted_product_labels_total
accepted_product_labels_recovered_by_lookup
accepted_product_label_recall
lookup_extra_products_total
parents_with_extra_lookup_products
```

Report by:

```text
combined
soil
sludge
bbd_parent_excluded
bbd_parent_overlap_only
```

Also list the top failure categories if any:

```text
canonicalization mismatch
multi-component mixture/salt
small inorganic/cofactor/dead-end parent
missing from processed envipath.csv but present in raw JSON
raw JSON parser issue
answer-key mismatch
```

## 7. Interpretation rules

Use these exact concepts:

```text
local_snapshot_lookup = known-pathway oracle / data integrity check
official_api_lookup = external service retrieval check
prediction_routes = ECLIPSE / BioTransformer / enviPath predictive API, if available
```

Do not write:

```text
enviPath lookup accuracy beats prediction models
```

Instead write:

```text
enviPath lookup can recover known Soil/Sludge records when the parent already exists in the enviPath package.
This supports using enviPath as a known-pathway retrieval layer, not as a fair blind predictor on the same Soil/Sludge-derived evaluation set.
```

## 8. FINAL_STATUS values

Use exactly one:

```text
ENVIPATH_SOIL_SLUDGE_LOOKUP_SUPPLEMENT_COMPLETE
ENVIPATH_SOIL_SLUDGE_LOOKUP_SUPPLEMENT_COMPLETE_WITH_API_BLOCKER
BLOCKED_MISSING_PRIOR_SOIL_SLUDGE_EVAL_SET
BLOCKED_MISSING_ENVIPATH_LOCAL_ASSETS
ENVIPATH_SOIL_SLUDGE_LOOKUP_SUPPLEMENT_FAILED
```

## 9. Packaging

When done:

```bash
RETURN_ROOT=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
RETURN_DIR=$RETURN_ROOT/envipath_soil_sludge_known_pathway_lookup_supplement_20260819
ARCHIVE=$RETURN_ROOT/envipath_soil_sludge_known_pathway_lookup_supplement_20260819.tar.gz
IDENTITY=$RETURN_ROOT/envipath_soil_sludge_known_pathway_lookup_supplement_20260819.tar.gz.identity.txt

cd "$RETURN_DIR"
find . -type f ! -name MANIFEST.sha256 | sort | xargs sha256sum > MANIFEST.sha256
sha256sum -c MANIFEST.sha256
cd "$RETURN_ROOT"
tar -czf "$ARCHIVE" envipath_soil_sludge_known_pathway_lookup_supplement_20260819
sha256sum "$ARCHIVE" > "$IDENTITY"
ls -lh "$ARCHIVE" "$IDENTITY"
```

Do not include credentials.

## 10. What to report back

Report:

1. Final status.
2. Archive path and identity path.
3. Local snapshot parent found rate.
4. Local snapshot accepted-product recall.
5. Official API lookup status, if attempted.
6. Any mismatch categories.
7. A short interpretation separating lookup/oracle from prediction.
