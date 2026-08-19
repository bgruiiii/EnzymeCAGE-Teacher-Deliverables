# HPC executor-only prompt — Soil/Sludge transfer clean supplement v2 repackage fix

Date: 2026-08-19  
Executor: chenyu / HPC  
Task type: tiny repackage-only fix  
Expected return root:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

Expected return folder:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819
```

Expected archive:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819.tar.gz
```

## 0. Goal

Make a v2 clean supplement by fixing two small issues in the prior clean supplement:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_20260819
```

or, if only the archive exists:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_20260819.tar.gz
```

This is a repackage/reporting-semantics fix only.

Do not train models.  
Do not rerun ECLIPSE.  
Do not rerun BioTransformer.  
Do not rerun enviPath API.  
Do not change any prediction outputs.

## 1. Why v2 is needed

Bowen-side local audit of the prior clean supplement:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/CHEM_ECLIPSE_BBD_FINETUNE_SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-19.md
```

found that the main scientific cleanup was successful, but two teacher-facing packaging/reporting issues remain:

1. `05_CLEANUP_AUDIT/manifest_check.txt` exists in the archive but is missing from both `MANIFEST.sha256` and `MANIFEST.files`.
2. In `04_METRICS/metrics_summary_corrected.csv`, BioTransformer still has `coverage=1788` and `coverage_rate=1.0`. That column counts rows including empty/error placeholders. For teacher-facing reporting, the table must also explicitly show valid non-empty prediction coverage:

```text
BioTransformer valid non-empty parent predictions = 1679/1788
BioTransformer empty/error parent rows = 109
```

## 2. Hard rules

1. Do not rerun any model or API route.
2. Do not change prediction/scoring values except adding/renaming reporting columns as specified below.
3. Do not expose or package credentials.
4. Do not modify production data, production models, GitHub, or shared assets.
5. Do not describe enviPath lookup as blind prediction accuracy.
6. Generate all files under the expected return folder only.
7. Generate `MANIFEST.files` and `MANIFEST.sha256` after all other return files are final.

## 3. Required inputs

Use the prior clean supplement directory:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_20260819
```

If only the prior archive exists, extract it read-only into scratch:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_20260819.tar.gz
```

Required prior files:

```text
README_SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT.md
00_SOURCE_PACKAGE_AUDIT/source_file_inventory.tsv
00_SOURCE_PACKAGE_AUDIT/source_package_identity.md
04_METRICS/biotransformer_empty_or_error_parent_list.csv
04_METRICS/metrics_summary_corrected.csv
04_METRICS/per_parent_scoring_table_with_biotransformer.csv
04_METRICS/route_status_corrected.csv
04_METRICS/skipped_or_blocked_routes.csv
05_CLEANUP_AUDIT/cleanup_methods.md
05_CLEANUP_AUDIT/corrected_counts_check.md
05_CLEANUP_AUDIT/manifest_check.txt
06_OPTIONAL_ENVIPATH_LOOKUP_DOC_NOTE/envipath_lookup_doc_correction_note.md
```

If any required prior file is missing, return a typed blocker package instead of inventing data.

## 4. Required v2 fixes

### 4.1 Manifest completeness fix

In v2, every regular file under the return folder must be listed in both:

```text
MANIFEST.files
MANIFEST.sha256
```

except the manifest files themselves:

```text
MANIFEST.files
MANIFEST.sha256
```

Specifically, v2 must include:

```text
05_CLEANUP_AUDIT/manifest_check.txt
```

in both manifests.

Recommended order:

1. Copy prior clean supplement files into the v2 return folder.
2. Apply the metrics-table fix below.
3. Update README / cleanup audit text.
4. Generate `MANIFEST.files`.
5. Generate `MANIFEST.sha256`.
6. Run `sha256sum -c MANIFEST.sha256`.
7. Write `05_CLEANUP_AUDIT/manifest_check.txt` with the result.
8. Regenerate `MANIFEST.files` and `MANIFEST.sha256` one final time so `manifest_check.txt` itself is covered.
9. Run `sha256sum -c MANIFEST.sha256` again and save the terminal output outside the return folder or in the identity sidecar notes. Do not modify return-folder files after the final manifest.

Safe command pattern:

```bash
cd "${RETURN_DIR}"
find . -type f ! -name MANIFEST.sha256 ! -name MANIFEST.files -print0 | sort -z | xargs -0 sha256sum > MANIFEST.sha256
```

For `MANIFEST.files`, write a TSV:

```text
relative_path	bytes	sha256
```

covering the same file set as `MANIFEST.sha256`.

### 4.2 BioTransformer coverage semantics fix

Create:

```text
04_METRICS/metrics_summary_v2.csv
```

based on the prior:

```text
04_METRICS/metrics_summary_corrected.csv
```

Keep the original metric values unchanged, but add explicit coverage-semantics columns:

```text
row_coverage_including_placeholders
row_coverage_rate_including_placeholders
valid_nonempty_prediction_count
empty_or_error_parent_count
valid_nonempty_prediction_rate
coverage_note
```

For ECLIPSE rows:

```text
row_coverage_including_placeholders = old coverage
row_coverage_rate_including_placeholders = old coverage_rate
valid_nonempty_prediction_count = old coverage
empty_or_error_parent_count = num_parents - old coverage
valid_nonempty_prediction_rate = old coverage / num_parents
coverage_note = valid generated predictions; no placeholder coverage inflation known
```

For BioTransformer rows:

- combined + all_valid:

```text
num_parents = 1788
row_coverage_including_placeholders = 1788
empty_or_error_parent_count = 109
valid_nonempty_prediction_count = 1679
valid_nonempty_prediction_rate = 1679/1788
coverage_note = metrics retain empty/error parents as misses; valid non-empty coverage is 1679/1788
```

- combined + bbd_parent_excluded:

```text
num_parents = 1731
row_coverage_including_placeholders = 1731
empty_or_error_parent_count = 103
valid_nonempty_prediction_count = 1628
valid_nonempty_prediction_rate = 1628/1731
coverage_note = metrics retain empty/error parents as misses; valid non-empty coverage is 1628/1731
```

- soil + all_valid:

```text
num_parents = 1521
empty_or_error_parent_count = 107
valid_nonempty_prediction_count = 1414
valid_nonempty_prediction_rate = 1414/1521
```

- soil + bbd_parent_excluded:

```text
num_parents = 1470
empty_or_error_parent_count = 101
valid_nonempty_prediction_count = 1369
valid_nonempty_prediction_rate = 1369/1470
```

- sludge + all_valid:

```text
num_parents = 276
empty_or_error_parent_count = 3
valid_nonempty_prediction_count = 273
valid_nonempty_prediction_rate = 273/276
```

- sludge + bbd_parent_excluded:

```text
num_parents = 270
empty_or_error_parent_count = 3
valid_nonempty_prediction_count = 267
valid_nonempty_prediction_rate = 267/270
```

These BioTransformer values should apply to both `raw` and `parent_filtered` rows, because BioTransformer has no parent-copy rows in this evaluation.

Also keep a copy of the prior file for traceability:

```text
04_METRICS/metrics_summary_corrected_v1_retained.csv
```

### 4.3 README v2 update

Write:

```text
README_SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2.md
```

It must include this exact meaning:

```text
This v2 package is a repackage/reporting-semantics fix only.
It does not rerun or change ECLIPSE, BioTransformer, or enviPath outputs.
```

It must say:

```text
BioTransformer ENVMICRO has 1679/1788 valid non-empty parent predictions on the combined all-valid set, with 109 empty/error parent rows retained as misses in the full-denominator metrics.
```

And:

```text
For the BBD-parent-excluded denominator, BioTransformer has 1628/1731 valid non-empty parent predictions, with 103 empty/error parent rows retained as misses.
```

Safe bottom-line wording:

```text
BioTransformer ENVMICRO remains the strongest current blind-prediction baseline on Soil/Sludge Hit@3/5/10.
BBD-only ECLIPSE PREDEC improves over ECLIPSE NoEC but remains a complementary candidate generator rather than the leading standalone route.
enviPath known-pathway lookup should be reported separately as database retrieval, not prediction accuracy.
```

### 4.4 Cleanup audit v2

Write:

```text
05_CLEANUP_AUDIT/v2_repackage_fix_audit.md
```

Include:

```text
training_rerun=false
eclipse_prediction_rerun=false
biotransformer_full_rerun=false
envipath_api_rerun=false
prediction_outputs_changed=false
manifest_covers_manifest_check_txt=true
metrics_summary_v2_has_valid_nonempty_columns=true
```

Also state the exact source package:

```text
chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_20260819
```

## 5. Required v2 return structure

Return folder:

```text
chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819/
├── README_SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2.md
├── MANIFEST.files
├── MANIFEST.sha256
├── 00_SOURCE_PACKAGE_AUDIT/
│   ├── source_file_inventory.tsv
│   └── source_package_identity.md
├── 04_METRICS/
│   ├── metrics_summary_v2.csv
│   ├── metrics_summary_corrected_v1_retained.csv
│   ├── route_status_corrected.csv
│   ├── per_parent_scoring_table_with_biotransformer.csv
│   ├── biotransformer_empty_or_error_parent_list.csv
│   └── skipped_or_blocked_routes.csv
├── 05_CLEANUP_AUDIT/
│   ├── cleanup_methods.md
│   ├── corrected_counts_check.md
│   ├── manifest_check.txt
│   └── v2_repackage_fix_audit.md
└── 06_OPTIONAL_ENVIPATH_LOOKUP_DOC_NOTE/
    └── envipath_lookup_doc_correction_note.md
```

## 6. Identity sidecar

Next to the archive, write:

```text
chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819.tar.gz.identity.txt
```

Required fields:

```text
archive_name=chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819.tar.gz
archive_sha256=<sha256>
archive_bytes=<bytes>
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
training_rerun=false
eclipse_prediction_rerun=false
biotransformer_full_rerun=false
envipath_api_rerun=false
prediction_outputs_changed=false
credentials_packaged=false
```

Allowed final statuses:

```text
SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_REPACKAGE_FIX_COMPLETE
SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_BLOCKED_SOURCE_PACKAGE_MISSING
SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_BLOCKED_REQUIRED_FILE_MISSING
SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_BLOCKED_MANIFEST_FAILED
SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_FAILED
```

## 7. Completion criteria

This task is complete only if:

1. `MANIFEST.sha256` and `MANIFEST.files` cover every regular file except themselves.
2. `05_CLEANUP_AUDIT/manifest_check.txt` is covered by both manifests.
3. `sha256sum -c MANIFEST.sha256` passes after all return-folder files are final.
4. `metrics_summary_v2.csv` contains the new valid-nonempty coverage columns.
5. BioTransformer combined all-valid valid-nonempty coverage is explicitly `1679/1788`, not silently implied by `coverage=1788`.
6. No model/API rerun occurred.
7. The archive and identity sidecar are placed under:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

