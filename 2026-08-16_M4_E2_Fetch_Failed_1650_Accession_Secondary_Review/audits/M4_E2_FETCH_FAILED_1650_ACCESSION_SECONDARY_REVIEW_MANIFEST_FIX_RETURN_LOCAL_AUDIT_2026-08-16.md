# M4 E2 Fetch-Failed 1,650 Accession Secondary Review Manifest-Fix Return Local Audit

Date: 2026-08-16

Audited archive:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_fetch_failed_1650_accession_secondary_review_manifest_fix_20260816.tar.gz
```

Identity sidecar:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_fetch_failed_1650_accession_secondary_review_manifest_fix_20260816.tar.gz.identity.txt
```

Audit status:

```text
LOCAL_AUDIT_PASS_FOR_TEACHER_FACING_UPLOAD
```

## 1. Archive And Identity Check

Observed local archive:

```text
archive_sha256=546ea3ae39f0b803ea4554629aeddf1293832c5a259ea96ab040ccef2533ffce
archive_bytes=223041
identity_sha256=be9b690b8ddfdbb9c92e5cfcb88af595744e7ffacd0dd115915e7d408f4224c1
```

Identity sidecar reports:

```text
task_id=enzymecage_m4_e2_fetch_failed_1650_accession_secondary_review_manifest_fix_20260816
run_type=m4_e2_accession_review_manifest_fix_repackage_only
archive_sha256=546ea3ae39f0b803ea4554629aeddf1293832c5a259ea96ab040ccef2533ffce
archive_bytes=223041
final_status=M4_E2_ACCESSION_REVIEW_MANIFEST_FIX_COMPLETE_REPACKAGE_ONLY
review_denominator=1650
candidate_found_count=5
no_candidate_found_count=1645
api_retry_exhausted_count=0
replacement_performed_any=False
asset_generation_started_any=False
formal_assets_mutated_any=False
production_pool_mutated_any=False
production_d4_mutated_any=False
network_review_rerun=False
scientific_result_files_changed=False
```

Audit result:

```text
PASS: identity archive_sha256 matches local archive sha256.
PASS: identity states repackage-only, no network rerun, no scientific result file change.
```

## 2. Manifest Integrity Check

Command:

```bash
cd extracted_root/enzymecage_m4_e2_fetch_failed_1650_accession_secondary_review_manifest_fix_20260816
sha256sum -c MANIFEST.sha256
```

Result:

```text
ACCESSION_CANDIDATE_ONLY_TABLE.csv: OK
ACCESSION_REVIEW_SUMMARY.json: OK
ACCESSION_REVIEW_SUMMARY.md: OK
API_REQUEST_LOG.csv: OK
COMMAND_LOG.txt: OK
FINAL_STATUS.txt: OK
FIXED_VALIDATION_REPORT.json: OK
FULL_1650_ACCESSION_SECONDARY_REVIEW_TABLE.csv: OK
INPUT_SOURCE_VALIDATION_REPORT.json: OK
INPUT_SOURCE_VALIDATION_REPORT.md: OK
NO_MUTATION_CHECK.json: OK
REPACKAGE_FIX_REPORT.json: OK
REPACKAGE_FIX_REPORT.md: OK
VALIDATION_REPORT.json: OK
scripts/run_log.txt: OK
scripts/run_review.py: OK
```

Audit result:

```text
PASS: previous stale scripts/run_log.txt manifest defect is fixed.
PASS: all manifest-listed files verify successfully.
```

## 3. Result Preservation Check

Compared against the previous returned directory extracted during local audit.
The following scientific/result files are byte-identical:

```text
ACCESSION_CANDIDATE_ONLY_TABLE.csv
ACCESSION_REVIEW_SUMMARY.json
ACCESSION_REVIEW_SUMMARY.md
API_REQUEST_LOG.csv
COMMAND_LOG.txt
FINAL_STATUS.txt
FULL_1650_ACCESSION_SECONDARY_REVIEW_TABLE.csv
INPUT_SOURCE_VALIDATION_REPORT.json
INPUT_SOURCE_VALIDATION_REPORT.md
NO_MUTATION_CHECK.json
VALIDATION_REPORT.json
scripts/run_review.py
```

Observed expected difference:

```text
scripts/run_log.txt differs from the previous archive.
This is expected for the packaging fix and is now manifest-consistent.
```

Fix reports added:

```text
REPACKAGE_FIX_REPORT.json
REPACKAGE_FIX_REPORT.md
FIXED_VALIDATION_REPORT.json
```

Audit result:

```text
PASS: scientific/result tables are unchanged.
PASS: fix is limited to package manifest/reporting integrity.
```

## 4. Table Content Check

Main table:

```text
FULL_1650_ACCESSION_SECONDARY_REVIEW_TABLE.csv
data_rows=1650
original_uid_unique=True
```

Candidate table:

```text
ACCESSION_CANDIDATE_ONLY_TABLE.csv
data_rows=5
```

Summary:

```text
review_denominator=1650
total_uids_reviewed=1650
candidate_found_count=5
no_candidate_found_count=1645
api_retry_exhausted_count=0
primary_differs_from_original_count=0
total_api_calls=3817
uniprot_lookup_status_counts={"DIRECT_LOOKUP_SUCCESS": 1650}
reviewed_accession_action_counts={
  "NO_AVAILABLE_AFDB_V6_ACCESSION_CANDIDATE_FOUND": 1645,
  "RECORD_ONLY_NO_REPLACEMENT": 5
}
```

Candidate accession inventory:

```text
P0DXV0 -> P0DXV0
P18173 -> Q8SXV0
P49823 -> A0A8I3PZS7
P54835 -> A0A8I3N404
P80550 -> F1RSB4
```

Audit result:

```text
PASS: counts remain 5 candidate / 1,645 no candidate.
PASS: candidate pairs match the previously audited return.
```

## 5. Mutation And Boundary Check

All 1,650 rows have:

```text
replacement_performed=False
asset_generation_started=False
formal_assets_mutated=False
production_pool_mutated=False
production_d4_mutated=False
```

Forbidden production/backfill claim scan found no matches for the requested
claim strings.

Audit result:

```text
PASS: no UID replacement.
PASS: no staged asset generation.
PASS: no formal or production mutation.
PASS: no production/backfill overclaim detected.
```

## 6. Final Conclusion

```text
The manifest-fix archive is locally auditable and ready for teacher-facing
upload as a table-only accession secondary review package.

It should be described as:
  1,650 fetch-failed UIDs reviewed for accession candidates;
  5 candidate accessions recorded for teacher review only;
  1,645 no available AFDB v6 candidate;
  no replacement and no asset generation performed.

It must not be described as:
  rescued assets;
  production backfill;
  UID replacement;
  D4/pool merge;
  full asset completion.
```
