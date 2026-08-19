# HPC executor-only prompt — BBD-finetuned ECLIPSE soil/sludge transfer evaluation

Date: 2026-08-18  
Executor: chenyu / HPC  
Task type: evaluation only; do not retrain unless explicitly instructed later  
Expected return root:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

Expected return folder:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818
```

Expected archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818.tar.gz
```

## 0. One-sentence goal

Evaluate whether the already trained **BBD-only fine-tuned ECLIPSE product model** transfers to enviPath Soil and Sludge transformation-product cases.

This is a cross-dataset transfer test, not a strict non-BBD external benchmark.

## 1. Hard rules

1. Do not train or fine-tune on Soil or Sludge for this task.
2. Do not modify production data, production models, GitHub, or shared assets.
3. Do not expose or package account credentials.
4. Do not send product labels / DOI / reaction records into prediction inputs.
5. Do not claim this is a final strict external benchmark.
6. If a required model or tool is missing, return a typed blocker package instead of silently changing the experiment.
7. Put all returned results under:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

## 2. Available enviPath assets on chenyu

Use the already downloaded assets. Do not re-download unless local files are missing or corrupt.

Raw enviPath JSON files:

```text
/root/projects/EnzymeCAGE-master/data/envipath/bbd.json
/root/projects/EnzymeCAGE-master/data/envipath/soil.json
/root/projects/EnzymeCAGE-master/data/envipath/sludge.json
```

Known identities:

| Dataset | File | Size | Package ID | compounds | reactions | pathways |
|---|---|---:|---|---:|---:|---:|
| BBD | `bbd.json` | 8.9 MB | `32de3cf4` | 1399 | 1480 | 219 |
| Soil | `soil.json` | 27 MB | `5882df9c` | 2608 | 2445 | 317 |
| Sludge | `sludge.json` | 4.9 MB | `521c547a` | 1067 | 494 | 183 |

The three files were downloaded on 2026-08-17 via:

```text
download_envipath_with_auth.py
```

using credentials from:

```text
HPC_Inputs/envipath_account_env.local.sh
```

Do not include that credential file or credential values in the return package.

Processed combined table:

```text
/root/projects/EnzymeCAGE-master/data/envipath.csv
```

Known processed-table identity:

```text
rows: 4630
columns include: rdkit_reactants / rdkit_products / ec_num / dataset / pathway
BBD rows: 1549
Soil rows: 2584
Sludge rows: 497
```

Additional asset:

```text
/root/projects/EnzymeCAGE-master/data/envipath/bbd_scenarios.json
```

Known identity:

```text
rows/scenarios: 1914
size: 1.2 MB
```

## 3. Required model/tool discovery

Before prediction, locate and record the exact assets used for:

1. BBD-only fine-tuned ECLIPSE product model folds.
2. H-ECLIPSE EC prediction model or route used for PREDEC.
3. BioTransformer ENVMICRO executable / environment, if available.
4. enviPath prediction / lookup route, if available.

Use existing trained BBD-only ECLIPSE models from the 2026-08-17 work. Do not retrain in this task.

If the BBD-only ECLIPSE fold models cannot be located, return:

```text
FINAL_STATUS = BLOCKED_MISSING_BBD_FINETUNED_ECLIPSE_MODEL
```

and include a detailed asset search log.

## 4. Build the Soil/Sludge evaluation set

Use:

```text
/root/projects/EnzymeCAGE-master/data/envipath.csv
```

Select rows where:

```text
dataset in {"Soil", "Sludge"}
```

or the local dataset labels equivalent to Soil / Sludge.

Required parsing:

1. Extract parent/reactant SMILES from `rdkit_reactants`.
2. Extract product SMILES from `rdkit_products`.
3. Canonicalize parent and product SMILES using RDKit.
4. Exclude rows where parent or product cannot be canonicalized.
5. Exclude parent-copy rows where canonical parent equals canonical product.
6. Deduplicate exact canonical parent-product pairs.
7. Also build a unique-parent answer table where each parent has all accepted products observed in Soil/Sludge.

Do not set an arbitrary cap such as 10 or 20. Use all valid Soil/Sludge cases after cleaning and deduplication.

## 5. Overlap audit

Report overlap with BBD-lineage assets because the model was BBD-finetuned.

At minimum, compute:

1. Soil/Sludge parent canonical SMILES present in BBD rows of `data/envipath.csv`.
2. Soil/Sludge parent canonical SMILES present in BBD83 benchmark parents, if the BBD83 input table is locally available.
3. Soil/Sludge parent-product pair present in BBD rows of `data/envipath.csv`.
4. Product overlap with BBD rows, reported separately.

Do not automatically remove all product-overlap rows from the transfer test, but report them separately.

For headline metrics, provide at least two denominators:

```text
all_valid_soil_sludge
bbd_parent_excluded_soil_sludge
```

If BBD83 input table cannot be located, mark only that sub-check as incomplete and continue with the `data/envipath.csv` BBD overlap check.

## 6. Prediction routes

### 6.1 ECLIPSE NoEC

Run product prediction using the BBD-only fine-tuned product model without EC conditioning.

Output top 10 predictions per unique parent.

### 6.2 ECLIPSE PREDEC

Run the same PREDEC route used in the BBD83 evaluation:

```text
parent SMILES -> H-ECLIPSE predicted EC -> product model with predicted EC
```

Output top 10 predictions per unique parent.

Do not use gold `ec_num` for the main PREDEC score. Gold EC can be used only as an optional diagnostic upper-bound route:

```text
ECLIPSE OracleEC
```

If OracleEC is run, label it clearly as non-blind / upper-bound and do not mix it with the main score.

### 6.3 BioTransformer ENVMICRO

If BioTransformer is available, run ENVMICRO on the same unique-parent blind input list.

Output top 10 canonical product predictions per parent.

If unavailable, return a typed blocker:

```text
biotransformer_status = blocked_missing_biotransformer_envmicro
```

and continue scoring the other routes.

### 6.4 enviPath route

Because the evaluation data comes from enviPath Soil/Sludge, direct database lookup is not a fair predictor.

If an actual enviPath prediction/rule route exists that takes only parent input and predicts products, run it and label it:

```text
enviPath_predictive_route
```

If only direct lookup against Soil/Sludge records is available, do not score it as a prediction model. Report it separately as:

```text
enviPath_database_lookup_oracle
```

This distinction is important.

## 7. Scoring rules

Use RDKit canonical SMILES for exact matching.

For each unique parent:

```text
accepted_products = all deduplicated canonical products observed for that parent in Soil/Sludge
```

For each route, compute:

```text
coverage
blocker count
invalid prediction count
parent-copy at rank 0
parent-copy within top 10
Hit@1
Hit@3
Hit@5
Hit@10
MRR@10
accepted product labels recovered@10
```

Compute each metric for:

1. raw predictions;
2. parent-filtered predictions, where predictions equal to the parent canonical SMILES are removed before ranking.

Also provide dataset-specific metrics:

```text
Soil only
Sludge only
Soil + Sludge combined
```

And denominator-specific metrics:

```text
all_valid_soil_sludge
bbd_parent_excluded_soil_sludge
```

## 8. Required output structure

Create:

```text
chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818/
├── FINAL_STATUS.txt
├── README_CHEM_ECLIPSE_BBD_FINETUNE_SOIL_SLUDGE_TRANSFER_EVAL.md
├── MANIFEST.sha256
├── 00_ASSET_MANIFEST/
│   ├── envipath_asset_manifest.md
│   ├── envipath_asset_manifest.json
│   ├── model_tool_asset_manifest.md
│   └── model_tool_asset_manifest.json
├── 01_EVAL_SET/
│   ├── soil_sludge_raw_rows_canonicalized.csv
│   ├── soil_sludge_parent_product_dedup.csv
│   ├── soil_sludge_unique_parent_blind_inputs.csv
│   ├── soil_sludge_unique_parent_answer_key_RESTRICTED.csv
│   └── eval_set_summary.md
├── 02_OVERLAP_AUDIT/
│   ├── bbd_overlap_audit.csv
│   └── bbd_overlap_audit.md
├── 03_PREDICTIONS/
│   ├── eclipse_noec_top10_predictions.csv
│   ├── eclipse_predec_top10_predictions.csv
│   ├── eclipse_oracle_ec_top10_predictions_OPTIONAL.csv
│   ├── biotransformer_envmicro_top10_predictions.csv
│   ├── envipath_predictive_route_top10_predictions.csv
│   └── route_blockers.json
├── 04_SCORING/
│   ├── metrics_summary.csv
│   ├── metrics_summary.md
│   ├── per_parent_scoring_table.csv
│   ├── per_dataset_scoring_table.csv
│   └── parent_copy_and_invalid_prediction_audit.csv
├── 05_EXECUTOR_AUDIT/
│   └── CHEM_ECLIPSE_BBD_FINETUNE_SOIL_SLUDGE_TRANSFER_EVAL_EXECUTOR_AUDIT.md
├── scripts/
│   └── run_soil_sludge_transfer_eval.py
└── logs/
    ├── asset_discovery.log
    ├── eval_set_build.log
    ├── eclipse_noec.log
    ├── eclipse_predec.log
    ├── biotransformer_envmicro.log
    ├── envipath_route.log
    └── scoring.log
```

If a route is unavailable, still create the expected prediction filename with headers and zero rows, and explain the blocker in:

```text
03_PREDICTIONS/route_blockers.json
05_EXECUTOR_AUDIT/CHEM_ECLIPSE_BBD_FINETUNE_SOIL_SLUDGE_TRANSFER_EVAL_EXECUTOR_AUDIT.md
```

## 9. Required README contents

The README must include:

1. One-line result status.
2. Exact input assets and row counts.
3. Whether Soil/Sludge were excluded from BBD-only fine-tuning.
4. Evaluation set counts:
   - raw Soil rows;
   - raw Sludge rows;
   - canonicalized valid rows;
   - deduplicated parent-product pairs;
   - unique parents;
   - BBD-overlap-excluded unique parents.
5. Main metrics table for:
   - ECLIPSE NoEC;
   - ECLIPSE PREDEC;
   - BioTransformer ENVMICRO, if available;
   - enviPath predictive route, if available.
6. Parent-copy behavior.
7. Clear caveat:

```text
This is a Soil/Sludge cross-dataset transfer test for BBD-only fine-tuned ECLIPSE.
It is not the final strict non-BBD external benchmark.
```

## 10. Required final status values

Use exactly one:

```text
SOIL_SLUDGE_TRANSFER_EVAL_COMPLETE
SOIL_SLUDGE_TRANSFER_EVAL_COMPLETE_WITH_ROUTE_BLOCKERS
BLOCKED_MISSING_BBD_FINETUNED_ECLIPSE_MODEL
BLOCKED_EVAL_SET_BUILD_FAILED
SOIL_SLUDGE_TRANSFER_EVAL_FAILED
```

## 11. Packaging commands

After finishing, run:

```bash
RETURN_ROOT=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
RETURN_DIR=$RETURN_ROOT/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818
ARCHIVE=$RETURN_ROOT/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818.tar.gz
IDENTITY=$RETURN_ROOT/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818.tar.gz.identity.txt

cd "$RETURN_DIR"
find . -type f | sort | xargs sha256sum > MANIFEST.sha256
cd "$RETURN_ROOT"
tar -czf "$ARCHIVE" chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_20260818
sha256sum "$ARCHIVE" > "$IDENTITY"
ls -lh "$ARCHIVE" "$IDENTITY"
```

Do not include large model checkpoint files in the return archive unless they are small enough and directly required for audit. Prefer manifests and paths for model assets.

Do not include credentials.

## 12. What to report back in chat

Report only:

1. Final status.
2. Archive path.
3. Identity file path.
4. Main metric table.
5. Any route blockers.
6. Short interpretation of whether BBD-only ECLIPSE transfers to Soil/Sludge.

Do not paste credentials, full logs, or restricted answer-key contents in chat.
