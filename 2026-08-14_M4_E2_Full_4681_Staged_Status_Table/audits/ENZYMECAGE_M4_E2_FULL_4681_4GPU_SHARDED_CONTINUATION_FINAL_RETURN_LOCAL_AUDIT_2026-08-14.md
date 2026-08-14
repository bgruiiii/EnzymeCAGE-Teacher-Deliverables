# EnzymeCAGE M4 E2 full 4,681 four-GPU sharded continuation final return local audit

Date: 2026-08-14

## Audited artifacts

Returned archive:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814.tar.gz
```

Identity sidecar:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814.tar.gz.identity.txt
```

Extracted root used for local audit:

```text
/tmp/m4_e2_full_4681_audit_mo8Dwa/
enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814/
```

## Local verdict

```text
CORE_FULL_4681_STATUS_TABLE: PASS
ARCHIVE_IDENTITY_MATCH: PASS
MANIFEST_SHA256_CHECK: PASS
STATUS_COUNT_RECOMPUTATION: PASS
PASS_UID_STAGED_ASSET_MANIFEST: PASS
PRODUCTION_MUTATION_CHECK: PASS
ACCESSION_REVIEW_DETAIL: CAVEAT_UNDERFILLED_FIELDS
PER_UID_REPORT_JSON_STRICTNESS: CAVEAT_NAN_VALUES
FINAL_PRODUCTION_BACKFILL_ACCEPTANCE: NOT_CLAIMED
```

Plain-language conclusion:

```text
The returned package is a valid final M4 E2 staged status-table package for the
4,681-UID denominator. It contains one terminal status row per UID, no
unattempted placeholder rows, internally consistent pass/blocker counts, a
verified archive identity, verified MANIFEST.sha256, and staged assets only for
the 1,704 PASS UIDs.

This audit does not claim production D4 merge, production pool mutation, full
scientific pocket completion, or strict AlphaFill equivalence. The result must
be reported as lower-evidence AFDB + P2Rank predicted-pocket staged assets.
```

## Archive and identity

Local archive size:

```text
658M
archive_bytes=689316623
```

Local SHA256:

```text
b01e717139f6eb48739e0861f82b339cdc0132ee4777acdd18354ee9da38bdd4
```

Identity sidecar reports the same SHA256:

```text
archive_sha256=b01e717139f6eb48739e0861f82b339cdc0132ee4777acdd18354ee9da38bdd4
```

Archive listing and extraction:

```text
tar entries: 43034
extracted files: 23014
extracted size: 1.2G
single root: enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814/
```

`MANIFEST.sha256` verification from inside the extracted root:

```text
manifest_exit=0
```

## Final status

`FINAL_STATUS.txt` contains exactly:

```text
M4_E2_FULL_4681_4GPU_SHARDED_CONTINUATION_COMPLETE_WITH_PASS_AND_BLOCKER_COUNTS
```

Identity sidecar reports:

```text
task_id=enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_20260814
run_type=m4_e2_full_4681_four_gpu_sharded_continuation_staged_only
base_completed_uids=70
num_shards=4
gpu_ids=0,1,2,3
n_full_uid_manifest=4681
n_full_status_rows=4681
n_unique_uids=4681
```

Base partial-run scan report:

```text
base_completed_uids=70
base_pass=56
base_fetch_failed=11
base_no_pocket=3
remaining_uids=4611
shard_sizes=[1153,1153,1153,1152]
```

Shard summary:

```text
shard 0 / GPU 0: assigned=1153 completed=1153 pass=416 blocked=737
shard 1 / GPU 1: assigned=1153 completed=1153 pass=416 blocked=737
shard 2 / GPU 2: assigned=1153 completed=1153 pass=408 blocked=745
shard 3 / GPU 3: assigned=1152 completed=1152 pass=408 blocked=744
```

`SHARD_ASSIGNMENT_TABLE.csv` recomputation:

```text
rows=4681
unique_uids=4681
base_completed=true: 70
base_completed=false: 4611
assigned_shard 0/1/2/3: 1153 / 1153 / 1153 / 1152
```

## Required table presence and row counts

```text
FULL_4681_UID_MANIFEST.csv              4681 rows + header
FULL_4681_STAGED_STATUS_TABLE.csv       4681 rows + header
FULL_4681_TIMING_RESOURCE_TABLE.csv     4681 rows + header
FULL_4681_STRUCTURE_SOURCE_TABLE.csv    4681 rows + header
FULL_4681_P2RANK_STATUS_TABLE.csv       4681 rows + header
FULL_4681_ACCESSION_REVIEW_TABLE.csv    1650 rows + header
FULL_4681_NO_POCKET_REVIEW_TABLE.csv    1324 rows + header
STAGED_ASSET_MANIFEST.csv               10224 rows + header
SHARD_ASSIGNMENT_TABLE.csv              4681 rows + header
SHARD_RUN_SUMMARY_TABLE.csv             4 rows + header
```

The required §2.4 status-table columns are all present exactly, with no missing
or extra columns.

## Recomputed status counts

From `FULL_4681_STAGED_STATUS_TABLE.csv`:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER    1704
BLOCKED_AFDB_P2RANK_NO_POCKET                  1324
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED            1650
BLOCKED_ESM2_3B_EXTRACTION_FAILED                 3
BLOCKED_ACCESSION_REVIEW_REQUIRED                 0
BLOCKED_SEQUENCE_MISSING_OR_CONFLICT              0
BLOCKED_GVP_EXTRACTION_FAILED                     0
BLOCKED_LOADER_VALIDATION_FAILED                  0
BLOCKED_ENVIRONMENT_ERROR                         0
```

Total:

```text
1704 + 1324 + 1650 + 3 = 4681
```

These counts match the identity sidecar.

Phase 1 100-UID membership recomputation:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER     41
BLOCKED_AFDB_P2RANK_NO_POCKET                   44
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED             15
```

This reproduces the previously audited Phase 1 41/44/15 split.

Membership fields:

```text
f3_missing_valid_pocket_member=True: 4681
final_missing_pocket_member=True:    4453
sequence_source=local_payload_uid2seq: 4681
```

## PASS staged assets

`STAGED_ASSET_MANIFEST.csv`:

```text
rows=10224
unique PASS UIDs represented=1704
asset count distribution per UID={6: 1704}
asset_uids_minus_pass=0
pass_minus_asset_uids=0
exists=false rows=0
sha256/size mismatches=0
```

All PASS rows in `FULL_4681_STAGED_STATUS_TABLE.csv` have:

```text
pocket_source=AFDB_P2RANK_TOP_PREDICTED_POCKET
evidence_tier=lower_evidence_predicted_pocket
esm2_3b_status=PASS
gvp_status=PASS
same_pocket_for_esm_node_and_gvp=True
loader_validation_called=True
loader_validation_status=PASS
dataset_len=1
dataset0_constructed=True
staged_asset_manifest_rows=6
```

No non-PASS UID appears in the staged asset manifest.

## Blocker interpretation

AFDB fetch:

```text
afdb_structure_status=PASS:                         3031
afdb_structure_status=BLOCKED_AFDB_STRUCTURE_FETCH_FAILED: 1650
afdb_http_status=200:                               3031
afdb_http_status=404:                               1633
afdb_http_status=000:                                 17
```

P2Rank:

```text
p2rank_status=PASS_TOP_POCKET_MAPPED:             1707
p2rank_status=BLOCKED_AFDB_P2RANK_NO_POCKET:      1324
p2rank_status blank because AFDB fetch failed:     1650
```

The 1,707 P2Rank mapped rows consist of 1,704 final PASS rows plus 3 rows that
mapped a top pocket but failed at ESM-2 3B extraction.

ESM-2 3B failed UIDs:

```text
Q09833  sequence_length=477  top_pocket_residues=27  p2rank_score=26.36
Q9US43  sequence_length=189  top_pocket_residues=22  p2rank_score=18.47
Q9USH6  sequence_length=190  top_pocket_residues=38  p2rank_score=39.26
```

Each of these has:

```text
AFDB HTTP 200
P2Rank top pocket mapped
esm2_3b_status=BLOCKED_ESM2_3B_EXTRACTION_FAILED
retryable=True
staged_asset_manifest_rows=0
```

This is a small per-UID blocker class, not an environment-wide failure.

No-pocket table:

```text
FULL_4681_NO_POCKET_REVIEW_TABLE.csv rows=1324
all retryable=False
all p2rank_version=P2Rank 2.5.1
all no_pocket_reason="AFDB structure fetched; P2Rank ran under the approved
command contract; no usable top predicted pocket residues were produced or
mapped."
```

This should be worded as "P2Rank ran but did not produce usable mapped pocket
residues", not as a download failure or P2Rank installation failure.

## Mutation and prohibited wording checks

`FORMAL_ASSET_MUTATION_CHECK.json`:

```json
{
  "checked": true,
  "formal_assets_mutated": false,
  "production_d4_mutated": false,
  "production_pool_mutated": false
}
```

`PRODUCTION_MUTATION_CHECK.json` reports the same false mutation flags.

All 4,681 status rows also have:

```text
formal_assets_mutated=False
production_pool_mutated=False
production_d4_mutated=False
```

Forbidden completion strings searched locally:

```text
M4_PRODUCTION_D4_BACKFILL_COMPLETE
M4_ALL_4681_UIDS_BACKFILLED
PASS_FULL_D4_LOADER
```

Result:

```text
no matches
```

## Environment and tool identity

Environment report records:

```text
Python 3.12.3
PyTorch 2.7.1+cu126
CUDA available=True
GPU=NVIDIA GeForce RTX 4090 D
Java=openjdk 17.0.19
ESM checkpoint=/root/.cache/torch/hub/checkpoints/esm2_t36_3B_UR50D.pt
ESM checkpoint sha256=7de8b4082ba15891959ab368b77ce3886697af1efb16d3c9e9e7b0c5d3f07500
```

P2Rank report records:

```text
P2Rank 2.5.1
P2RANK_DIR=/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1
expected_p2rank_archive_sha256=d243f2d9036ac053fefb9407b5fe1c85f4fe077c519fd975ac585e995feab274
actual_p2rank_archive_sha256=d243f2d9036ac053fefb9407b5fe1c85f4fe077c519fd975ac585e995feab274
archive_sha256_verified=True
command_contract=prank predict -threads 4 -c alphafold -visualizations 0
```

All non-empty `p2rank_command` strings in the status table contain the approved
contract:

```text
prank predict -threads 4 -c alphafold -visualizations 0
```

## Caveat 1: accession review table is structurally present but detail-light

`FULL_4681_ACCESSION_REVIEW_TABLE.csv` contains one row for each of the 1,650
AFDB fetch-failed UIDs:

```text
rows=1650
unique_uids=1650
afdb_primary_probe_status=404: 1633
afdb_primary_probe_status=000:   17
review_notes all equal "AFDB v6 structure could not be fetched for the original UID."
```

However, all of the following columns are blank for all 1,650 rows:

```text
uniprot_query_status
primary_accession
secondary_accessions
canonical_or_isoform
organism
afdb_secondary_probe_status
reviewed_accession_candidate
reviewed_accession_action
```

Therefore this package supports:

```text
No reviewed accession candidate was used for staged asset generation, and no
accession replacement was silently performed.
```

It does not support overclaiming:

```text
All 1,650 AFDB fetch-failed UIDs received detailed UniProt secondary-accession
review inside this returned package.
```

Teacher's corrected Q9Z1Y9 wording was present in the prompt. In this returned
package, the Q9Z1Y9 accession-review row is present but does not include the
corrected Q05A70/Q9JHH1 secondary-accession explanation. This should be handled
in the teacher-facing summary by referring to the already teacher-confirmed
8-UID accession review closure, not by claiming the full package itself contains
that detailed review.

## Caveat 2: per-UID REPORT.json uses NaN literals

All 4,681 `per_uid/<UID>/REPORT.json` files were parseable by Python's default
`json` module, and their recomputed status counts exactly match the main status
table. However, 4,581 per-UID report JSON files contain `NaN` literals in fields
such as `phase1_result_if_any` or `sampling_stratum_if_available`.

Plain consequence:

```text
The CSV tables are the strict machine-readable authority for the full status
package. The per-UID REPORT.json files are useful local/Python audit evidence
but should not be advertised as strict RFC-compliant JSON without sanitizing
NaN to null.
```

## Timing summary

From `FULL_4681_TIMING_RESOURCE_TABLE.csv`:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER:
  n=1704, median=8.451s, max=54.129s, mean=8.915s
BLOCKED_AFDB_P2RANK_NO_POCKET:
  n=1324, median=5.471s, max=26.336s, mean=5.769s
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED:
  n=1650, median=1.690s, max=40.036s, mean=2.358s
BLOCKED_ESM2_3B_EXTRACTION_FAILED:
  n=3, median=6.436s, max=7.568s, mean=6.786s
```

These are per-UID wall times in the returned table, not end-to-end cluster
elapsed time.

## Teacher-facing wording boundary

Allowed wording:

```text
The full 4,681 M4 E2 staged status table has returned and passed local core
audit. It contains 4,681 unique UID rows, recomputed status counts
1704 PASS / 1324 P2Rank no-pocket / 1650 AFDB fetch-failed / 3 ESM2-3B failed,
and 1,704 lower-evidence AFDB+P2Rank predicted-pocket staged asset sets. The
archive identity and MANIFEST.sha256 verify, and formal/production mutation
checks are false.
```

Required caveats:

```text
This is not a production D4 merge and not proof that all 4,681 UIDs were
backfilled. It is a staged status table plus staged PASS assets only.

The accession-review table is structurally present for 1,650 AFDB fetch-failed
UIDs, but detailed UniProt secondary-accession fields are blank; do not claim
that the full package itself performed detailed accession-variant review for all
fetch-failed UIDs.

The 1,324 no-pocket rows mean P2Rank ran under the approved command contract but
did not produce usable mapped top-pocket residues. They should not be described
as P2Rank installation/download failures.
```

