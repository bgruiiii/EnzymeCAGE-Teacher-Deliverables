# M4 E2 fetch-failed 1,650 accession secondary review

Date: 2026-08-16

## What This Package Is

This is the Chen Haoran-side table-only secondary accession review for the
1,650 `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` rows from the teacher-accepted
M4 E2 full 4,681 staged status table package.

It is independent of the accepted M4 E2 second milestone. It does not replace
UIDs, does not generate assets, does not run P2Rank / ESM-2 3B / GVP / loader,
and does not mutate formal or production assets.

## Source Denominator

Source package:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814.tar.gz
```

Source archive SHA256:

```text
b01e717139f6eb48739e0861f82b339cdc0132ee4777acdd18354ee9da38bdd4
```

Source table hashes verified in the return:

```text
FULL_4681_STAGED_STATUS_TABLE.csv
41b1166eef15d0c9dac0a2253369b7d5c9a324c6daefa5bc7481e4991f8b1b3a

FULL_4681_ACCESSION_REVIEW_TABLE.csv
e199bc3a6d323d4875ddacdb91f14af2ee233d32d9d6f65d1ff996acfd87dc94
```

## Main Result

```text
review_denominator                         1650
total_uids_reviewed                        1650
candidate_found_count                         5
no_candidate_found_count                   1645
api_retry_exhausted_count                     0
primary_differs_from_original_count           0
network_review_rerun                      False
scientific_result_files_changed           False
replacement_performed_any                 False
asset_generation_started_any              False
formal_assets_mutated_any                 False
production_pool_mutated_any               False
production_d4_mutated_any                 False
```

The 5 recorded accession candidates are:

```text
P0DXV0 -> P0DXV0
P18173 -> Q8SXV0
P49823 -> A0A8I3PZS7
P54835 -> A0A8I3N404
P80550 -> F1RSB4
```

These are candidate accessions recorded for teacher review only. They are not
UID replacements and no downstream asset generation was performed.

## Chenyu Repackaged Archive

The audited manifest-fix Chenyu archive is included because it is small enough
for GitHub:

```text
hpc_archive/enzymecage_m4_e2_fetch_failed_1650_accession_secondary_review_manifest_fix_20260816.tar.gz
```

Archive SHA256:

```text
546ea3ae39f0b803ea4554629aeddf1293832c5a259ea96ab040ccef2533ffce
```

Identity sidecar:

```text
hpc_identity/enzymecage_m4_e2_fetch_failed_1650_accession_secondary_review_manifest_fix_20260816.tar.gz.identity.txt
```

## Key Review Files

Full review table:

```text
tables/FULL_1650_ACCESSION_SECONDARY_REVIEW_TABLE.csv
```

Candidate-only table:

```text
tables/ACCESSION_CANDIDATE_ONLY_TABLE.csv
```

Summary:

```text
reports/ACCESSION_REVIEW_SUMMARY.md
reports/ACCESSION_REVIEW_SUMMARY.json
```

Input validation:

```text
reports/INPUT_SOURCE_VALIDATION_REPORT.md
reports/INPUT_SOURCE_VALIDATION_REPORT.json
```

Fixed package validation:

```text
reports/FIXED_VALIDATION_REPORT.json
reports/VALIDATION_REPORT.json
```

Local audit:

```text
audits/M4_E2_FETCH_FAILED_1650_ACCESSION_SECONDARY_REVIEW_MANIFEST_FIX_RETURN_LOCAL_AUDIT_2026-08-16.md
```

API request log:

```text
logs/API_REQUEST_LOG.csv
```

## Boundary Wording

Correct wording:

```text
1,650 fetch-failed UIDs were reviewed for accession candidates.
5 candidate accessions were recorded for teacher review only.
1,645 rows had no available AFDB v6 accession candidate.
No UID replacement and no asset generation were performed.
Formal and production mutation flags are false.
```

Do not describe this package as:

```text
rescued assets
production backfill
UID replacement
D4 / production pool merge
full asset completion
```

## Packaging Note

The first returned archive had one stale internal `MANIFEST.sha256` entry for
`scripts/run_log.txt`. The uploaded archive is the corrected manifest-fix
repackage. Local audit confirmed:

```text
MANIFEST.sha256 passes for all files;
core result files are unchanged from the first return;
the fix is limited to package manifest/reporting integrity.
```
