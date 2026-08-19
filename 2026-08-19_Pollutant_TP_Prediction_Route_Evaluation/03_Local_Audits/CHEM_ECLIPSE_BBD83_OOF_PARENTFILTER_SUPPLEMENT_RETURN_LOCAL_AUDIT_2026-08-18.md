# chem-eclipse BBD83 OOF-only + parent-filter supplement return local audit

Audit date: 2026-08-18  
Auditor: local Codex review  
Returned package:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/chem_eclipse_bbd_fullfold_bbd83_oof_parentfilter_supplement_20260817.tar.gz
```

Package SHA256:

```text
24c51efa995a3beb1d03a44fc04b8ca3488842c6b724ae29f649733492f3e861
```

## 1. Bottom-line verdict

The supplement package is scientifically usable for local scoring and follow-up comparison. It correctly provides all-fold, parent-filtered, OOF-only, and OOF+parent-filtered BBD83 prediction tables for both NoEC and PREDEC routes. Local checks confirmed:

- The package extracts successfully.
- `MANIFEST.sha256` validates with return code 0.
- The package audit declares `restricted_answer_key_read=false`, `computed_hit_at_k=false`, `computed_accuracy=false`, and `computed_mrr=false`.
- All-fold original aggregated tables match the previous full-fold return exactly by `(case_id, predicted_product, rank)`.
- OOF-only `contributing_folds` are valid: every OOF row uses folds listed in the original case-level `fold_test_membership_seed_ids`.
- Parent-filtered tables contain zero unchanged-parent rows.

Main result after local scoring:

- All-fold PREDEC parent-filtered remains strong: **Hit@10 66 / 83 = 79.5%**, MRR@10 **0.589**.
- Conservative OOF-only PREDEC parent-filtered is lower: **Hit@10 38 / 81 = 46.9%**, MRR@10 **0.389**.
- Parent filtering mostly improves early rank / MRR, not total Hit@10 coverage.

## 2. Packaging and format audit

Returned files are under:

```text
HPC_Returned_Result_Summaries/chem_eclipse_bbd_fullfold_bbd83_oof_parentfilter_supplement_20260817/
```

Generated core files:

```text
11_BBD83_PREDICTIONS_OOF_FILTERED/BBD83_NO_EC_ALL_AGGREGATED.csv
11_BBD83_PREDICTIONS_OOF_FILTERED/BBD83_NO_EC_PARENT_FILTERED_AGGREGATED.csv
11_BBD83_PREDICTIONS_OOF_FILTERED/BBD83_NO_EC_OOF_ONLY_AGGREGATED.csv
11_BBD83_PREDICTIONS_OOF_FILTERED/BBD83_NO_EC_OOF_PARENT_FILTERED_AGGREGATED.csv
11_BBD83_PREDICTIONS_OOF_FILTERED/BBD83_PREDEC_ALL_AGGREGATED.csv
11_BBD83_PREDICTIONS_OOF_FILTERED/BBD83_PREDEC_PARENT_FILTERED_AGGREGATED.csv
11_BBD83_PREDICTIONS_OOF_FILTERED/BBD83_PREDEC_OOF_ONLY_AGGREGATED.csv
11_BBD83_PREDICTIONS_OOF_FILTERED/BBD83_PREDEC_OOF_PARENT_FILTERED_AGGREGATED.csv
11_BBD83_PREDICTIONS_OOF_FILTERED/*.jsonl
11_BBD83_PREDICTIONS_OOF_FILTERED/OOF_PARENTFILTER_SUMMARY.md
oof_parentfilter_audit.md
oof_parentfilter_audit.json
MANIFEST.sha256
```

Manifest:

```text
sha256sum -c MANIFEST.sha256
return code: 0
```

Format deviations from the requested suggested layout:

- `FINAL_STATUS.txt` is absent.
- `01_INPUT_MANIFEST/input_manifest.json` is absent.
- Requested summary CSVs are absent:
  - `BBD83_PARENT_COPY_AND_COVERAGE_SUMMARY.csv`
  - `BBD83_CASE_LEVEL_FILTER_STATUS.csv`
- The exact requested `*_TOP10.csv` filenames were not used. Instead, the package provides aggregated full candidate tables with `rank_aggregated`; local scoring used the top 10 rows per case after sorting by `rank_aggregated`.

Interpretation: these are packaging / convenience gaps, not blockers for local scoring.

## 3. Executor-side no-answer-key declaration

`oof_parentfilter_audit.json` reports:

```json
{
  "restricted_answer_key_read": false,
  "computed_hit_at_k": false,
  "computed_accuracy": false,
  "computed_mrr": false
}
```

Therefore, local scoring against the restricted BBD83 answer key remains valid.

## 4. Candidate table structure and filtering checks

All aggregated CSVs contain these fields:

```text
benchmark_case_id
pollutant_name
parent_smiles
parent_smiles_rdkit_canonical
route
prediction_policy
predicted_product_smiles_rdkit_canonical
best_beam_log_likelihood
contributing_folds
rank_aggregated
predicted_ec
model_checkpoint_sha256
status
blocker_reason
```

Local structure counts:

| File | Rows | Cases | Parent-copy rows | Max rank |
|---|---:|---:|---:|---:|
| `BBD83_NO_EC_ALL_AGGREGATED.csv` | 643 | 83 | 68 | 15 |
| `BBD83_NO_EC_PARENT_FILTERED_AGGREGATED.csv` | 575 | 83 | 0 | 14 |
| `BBD83_NO_EC_OOF_ONLY_AGGREGATED.csv` | 235 | 81 | 46 | 2 |
| `BBD83_NO_EC_OOF_PARENT_FILTERED_AGGREGATED.csv` | 189 | 81 | 0 | 2 |
| `BBD83_PREDEC_ALL_AGGREGATED.csv` | 718 | 83 | 48 | 18 |
| `BBD83_PREDEC_PARENT_FILTERED_AGGREGATED.csv` | 670 | 83 | 0 | 17 |
| `BBD83_PREDEC_OOF_ONLY_AGGREGATED.csv` | 230 | 81 | 25 | 2 |
| `BBD83_PREDEC_OOF_PARENT_FILTERED_AGGREGATED.csv` | 205 | 81 | 0 | 2 |

OOF coverage:

- OOF cases: 81
- OOF accepted product labels in local answer key: 145
- Cases without OOF predictions:
  - `SPD-BBD2-PARENT-c0018`
  - `SPD-BBD2-PARENT-c0691`

OOF fold validation:

- Checked aggregated OOF rows: 859
- OOF fold violations: 0

All-fold original table validation against previous return:

| Route | Previous rows | Supplement all-fold rows | Missing from supplement | Extra in supplement |
|---|---:|---:|---:|---:|
| NoEC | 643 | 643 | 0 | 0 |
| PREDEC | 718 | 718 | 0 | 0 |

## 5. Local scoring method

Local scoring used the restricted answer key:

```text
08_Benchmark_Handoffs/bbd83_answer_key_scoring_handoff_20260816/restricted/KNOWN_PATHWAY_POLLUTANT_ACCEPTED_PRODUCTS_V0_2.csv
```

Scoring policy:

- RDKit canonicalize predicted and accepted product SMILES.
- Sort candidate rows by `rank_aggregated`.
- Use top 10 rows per case for Hit@K and MRR@10.
- Case-level Hit@K: at least one accepted first-generation product appears in top K.
- Product recovery@10: accepted product labels recovered in top 10.

Answer-key counts:

| Item | Count |
|---|---:|
| BBD83 cases | 83 |
| Accepted product labels | 148 |
| Canonicalization failures | 0 |

## 6. Local scoring results

### 6.1 All-fold aggregated routes

| Route / file | Cases | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product recovery@10 | Parent rank1 | Parent in top10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| NoEC all | 83 | 18 / 83 = 21.7% | 39 / 83 = 47.0% | 44 / 83 = 53.0% | 47 / 83 = 56.6% | 0.345 | 59 / 148 = 39.9% | 29 | 68 |
| NoEC parent-filtered | 83 | 25 / 83 = 30.1% | 43 / 83 = 51.8% | 45 / 83 = 54.2% | 47 / 83 = 56.6% | 0.408 | 59 / 148 = 39.9% | 0 | 0 |
| PREDEC all | 83 | 35 / 83 = 42.2% | 57 / 83 = 68.7% | 65 / 83 = 78.3% | 66 / 83 = 79.5% | 0.566 | 87 / 148 = 58.8% | 10 | 46 |
| PREDEC parent-filtered | 83 | 37 / 83 = 44.6% | 60 / 83 = 72.3% | 66 / 83 = 79.5% | 66 / 83 = 79.5% | 0.589 | 87 / 148 = 58.8% | 0 | 0 |

Interpretation:

- Parent filtering improves early ranking, especially NoEC Hit@1 and PREDEC MRR.
- Hit@10 coverage is unchanged for both all-fold routes because the recovered accepted products were already within the pre-filter top 10.

### 6.2 Conservative OOF-only routes

Denominator: 81 OOF-available cases and 145 accepted labels attached to those cases.

| Route / file | Cases | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product recovery@10 | Parent rank1 | Parent in top10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| NoEC OOF-only | 81 | 13 / 81 = 16.0% | 26 / 81 = 32.1% | 26 / 81 = 32.1% | 26 / 81 = 32.1% | 0.228 | 28 / 145 = 19.3% | 28 | 46 |
| NoEC OOF parent-filtered | 81 | 15 / 81 = 18.5% | 26 / 81 = 32.1% | 26 / 81 = 32.1% | 26 / 81 = 32.1% | 0.251 | 28 / 145 = 19.3% | 0 | 0 |
| PREDEC OOF-only | 81 | 23 / 81 = 28.4% | 38 / 81 = 46.9% | 38 / 81 = 46.9% | 38 / 81 = 46.9% | 0.370 | 45 / 145 = 31.0% | 11 | 25 |
| PREDEC OOF parent-filtered | 81 | 26 / 81 = 32.1% | 38 / 81 = 46.9% | 38 / 81 = 46.9% | 38 / 81 = 46.9% | 0.389 | 45 / 145 = 31.0% | 0 | 0 |

Interpretation:

- PREDEC remains better than NoEC under the conservative OOF-only lens.
- Parent filtering improves rank position but not total OOF Hit@10 coverage.
- Conservative PREDEC OOF parent-filtered remains below the prior BioTransformer ENVMICRO BBD83 baseline of Hit@10 50 / 83 and MRR@10 0.428.

## 7. Comparison to previous local audit

Previous full-fold audit conclusion:

- PREDEC all-fold aggregated: Hit@10 66 / 83, MRR@10 0.566.
- PREDEC OOF-only: Hit@10 38 / 81, MRR@10 0.370.

This supplement confirms:

- Parent-filtered PREDEC all-fold: Hit@10 unchanged at 66 / 83, MRR@10 improves to 0.589.
- Parent-filtered PREDEC OOF-only: Hit@10 unchanged at 38 / 81, MRR@10 improves to 0.389.

Therefore, parent-filtering is useful for candidate presentation and rank quality, but it does not rescue additional cases at top 10 in this returned run.

## 8. Recommended next step

For reporting:

```text
ECLIPSE BBD fine-tuned PREDEC can be retained as a useful complementary candidate source.
The all-fold parent-filtered score is strong, but the conservative OOF parent-filtered score remains lower than BioTransformer.
Therefore the safe integration strategy is not to replace BioTransformer, but to compare complementarity case-by-case and possibly merge candidates after removing unchanged-parent predictions.
```

If another chenyu run is requested, ask for:

1. Case-level hit/miss comparison against BioTransformer after local scoring is provided back to them or scored locally.
2. PREDEC parent-filtered top candidates joined with BioTransformer top candidates for complementarity review.
3. Optional external non-BBD / non-enviPath-lineage benchmark before claiming generalization.
