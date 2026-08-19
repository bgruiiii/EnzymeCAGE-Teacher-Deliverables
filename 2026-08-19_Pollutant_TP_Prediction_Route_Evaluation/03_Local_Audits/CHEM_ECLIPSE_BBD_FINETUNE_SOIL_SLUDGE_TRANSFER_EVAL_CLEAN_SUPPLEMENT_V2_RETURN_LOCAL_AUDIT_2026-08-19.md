# Local audit — Soil/Sludge transfer evaluation clean supplement v2 return

Date: 2026-08-19  
Return archive:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819.tar.gz
```

Identity file:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819.tar.gz.identity.txt
```

Related prompt:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/07_HPC_Prompts/HPC_SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_REPACKAGE_FIX_PROMPT_2026-08-19.md
```

## 1. Verdict

The v2 package fixes the two remaining issues from the prior clean supplement.

Local audit verdict:

```text
PASS_FINAL_REPORT_READY
```

The package is acceptable as the clean Soil/Sludge transfer evaluation supplement for final-report use.

What v2 fixed:

1. `MANIFEST.sha256` and `MANIFEST.files` now cover every regular non-manifest file, including `05_CLEANUP_AUDIT/manifest_check.txt`.
2. `04_METRICS/metrics_summary_v2.csv` now explicitly separates BioTransformer row coverage including placeholders from valid non-empty prediction coverage.

No evidence of model/API rerun:

```text
training_rerun=false
eclipse_prediction_rerun=false
biotransformer_full_rerun=false
envipath_api_rerun=false
prediction_outputs_changed=false
credentials_packaged=false
```

## 2. Archive identity

Local SHA256:

```text
93d45eb521b384c9b34b22d57c053241e754a61ccd308efb960d44c669585820
```

Identity sidecar reports:

```text
archive_name=chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819.tar.gz
archive_sha256=93d45eb521b384c9b34b22d57c053241e754a61ccd308efb960d44c669585820
archive_bytes=50833
source_package=chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_20260819
source_package_final_status=SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_COMPLETE
final_status=SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_REPACKAGE_FIX_COMPLETE
manifest_check=PASS
manifest_covers_manifest_check_txt=true
metrics_summary_v2_has_valid_nonempty_columns=true
biotransformer_combined_all_valid_valid_nonempty_parent_predictions=1679/1788
biotransformer_combined_all_valid_empty_or_error_parent_count=109
biotransformer_bbd_parent_excluded_valid_nonempty_parent_predictions=1628/1731
biotransformer_bbd_parent_excluded_empty_or_error_parent_count=103
```

The archive hash matches the identity sidecar.

## 3. Manifest audit

Fresh extraction and manifest check:

```text
sha256sum -c MANIFEST.sha256
```

All listed files passed.

Independent coverage check:

```text
actual non-manifest files: 15
MANIFEST.sha256 entries: 15
MANIFEST.files entries: 15
missing from MANIFEST.sha256: none
extra in MANIFEST.sha256: none
missing from MANIFEST.files: none
extra in MANIFEST.files: none
manifest_check.txt in MANIFEST.sha256: true
manifest_check.txt in MANIFEST.files: true
MANIFEST.sha256 / MANIFEST.files self-included: false
```

This fixes the v1 manifest omission.

## 4. Metrics v2 audit

`04_METRICS/metrics_summary_v2.csv`:

```text
rows: 36
routes:
  eclipse_noec: 12
  eclipse_predec: 12
  biotransformer_envmicro: 12
bad oracle/envipath metric rows: 0
```

New required columns are present:

```text
row_coverage_including_placeholders
row_coverage_rate_including_placeholders
valid_nonempty_prediction_count
empty_or_error_parent_count
valid_nonempty_prediction_rate
coverage_note
```

Key BioTransformer rows:

| Dataset / denominator / filter | Parents | Row coverage incl. placeholders | Valid non-empty | Empty/error | Valid non-empty rate | Hit@1 | Hit@3 | Hit@5 | Hit@10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| combined / all_valid / parent_filtered | 1788 | 1788 | 1679 | 109 | 0.9390 | 10.63% | 21.48% | 27.52% | 30.93% |
| combined / bbd_parent_excluded / parent_filtered | 1731 | 1731 | 1628 | 103 | 0.9405 | 10.40% | 21.14% | 27.21% | 30.73% |
| soil / all_valid / parent_filtered | 1521 | 1521 | 1414 | 107 | 0.9297 | 9.93% | 20.18% | 26.10% | 29.39% |
| sludge / all_valid / parent_filtered | 276 | 276 | 273 | 3 | 0.9891 | 14.13% | 28.99% | 36.23% | 40.22% |

The `coverage` and `coverage_rate` columns are retained from v1, but v2 now makes their meaning explicit through `row_coverage_including_placeholders` and the valid-nonempty columns.

Safe final-report wording:

```text
BioTransformer metrics retain empty/error parents as misses in the full denominator; valid non-empty coverage is 1679/1788 for combined all-valid and 1628/1731 for the BBD-parent-excluded denominator.
```

## 5. Per-parent and empty/error audit

`per_parent_scoring_table_with_biotransformer.csv`:

```text
rows: 5364
eclipse_noec: 1788 rows
eclipse_predec: 1788 rows
biotransformer_envmicro: 1788 rows
```

BioTransformer validity:

```text
valid_prediction=True, empty_or_error_prediction=False: 1679
valid_prediction=False, empty_or_error_prediction=True: 109
```

`biotransformer_empty_or_error_parent_list.csv`:

```text
rows: 109
```

This is consistent with the v2 identity and README.

## 6. README and v2 audit text

The README correctly says:

```text
This v2 package is a repackage/reporting-semantics fix only.
It does not rerun or change ECLIPSE, BioTransformer, or enviPath outputs.
```

It also correctly states:

```text
BioTransformer ENVMICRO has 1679/1788 valid non-empty parent predictions on the combined all-valid set, with 109 empty/error parent rows retained as misses in the full-denominator metrics.
```

`05_CLEANUP_AUDIT/v2_repackage_fix_audit.md` reports:

```text
training_rerun=false
eclipse_prediction_rerun=false
biotransformer_full_rerun=false
envipath_api_rerun=false
prediction_outputs_changed=false
manifest_covers_manifest_check_txt=true
metrics_summary_v2_has_valid_nonempty_columns=true
```

## 7. Final interpretation

This v2 supplement supports the current pollutant-transformation route conclusion:

```text
On the Soil/Sludge transfer set, BBD-only ECLIPSE PREDEC improves over ECLIPSE NoEC, but BioTransformer ENVMICRO remains the stronger current blind-prediction baseline at Hit@3/5/10 and product-label recovery.
```

Pair this with the separate enviPath lookup supplement:

```text
For parents already present in the local Soil/Sludge enviPath snapshot, enviPath lookup recovers known pathway products completely; this is database retrieval / known-pathway lookup, not blind prediction accuracy.
```

Practical route for the final report:

```text
1. Known parent/pathway exists in enviPath -> use enviPath known-pathway lookup first.
2. Unknown parent -> use BioTransformer ENVMICRO as current strongest blind prediction baseline.
3. ECLIPSE PREDEC -> keep as a complementary candidate generator and future improvement target.
```

