# HPC executor-only prompt: M4 E2 cache-miss one-UID smoke with bounded fallback

You are running on Chenyu/HPC as an executor. Your job is to run a bounded
one-UID cache-miss smoke for M4 E2 observation point 1.

Goal:

```text
Obtain exactly one complete cache-miss smoke PASS, proving:
  extract -> staged cache write -> same-pocket GVP/ESM pocket-node -> isolated
  loader validation.
```

Try candidates in the specified order. Stop immediately after the first complete
PASS. Record every attempted, skipped, blocked, and PASS UID honestly.

Do not run the full 4,681 backfill. Do not mutate production EnzymeCAGE assets,
pools, datasets, model checkpoints, or formal splits.

## 0. Authority and evidence

Authority:

```text
TEACHER_REPLY_PROJECT_NEXT_STEPS_GUIDANCE_2026-08-13.md
```

Teacher-required item:

```text
M4 second milestone E2:
  observation point 1 = 1 cache-miss UID extraction smoke
  (extract -> cache write -> linked full chain, end-to-end).
```

Candidate preflight evidence:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_cache_miss_smoke_candidate_preflight_20260813.tar.gz

03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_cache_miss_smoke_candidate_preflight_20260813.tar.gz.identity.txt
```

Local audit interpretation:

```text
The preflight found usable candidates from the M4 final-missing-pocket universe,
not arbitrary external UniProt UIDs. The top queue is:
  A3CST9 -> B8GGQ9 -> A7I9P9 -> A0A0H2V760 -> P0DXZ0
```

Phase 1 route to preserve:

```text
AlphaFoldDB structure only;
P2Rank 2.5.1 top predicted pocket only;
ESM-2 3B model_name=esm2_t36_3B_UR50D, repr_layer=36, embedding_dim=2560;
same predicted-pocket PDB for GVP and ESM pocket-node features;
isolated load_geometric_dataset validation;
staged outputs only.
```

Evidence tier:

```text
P2Rank predicted pocket lower-evidence tier.
```

## 1. Task identity

```text
TASK_ID=enzymecage_m4_e2_cache_miss_one_uid_smoke_bounded_fallback_20260813
RUN_TYPE=m4_e2_one_uid_cache_miss_smoke_bounded_fallback_staged_only
PRIMARY_ROUTE=AlphaFoldDB structure -> P2Rank predicted pocket -> ESM-2 3B cache-miss extraction -> staged cache write -> same-pocket GVP -> isolated loader validation
```

Allowed completed final status if at least one UID passes:

```text
M4_E2_CACHE_MISS_ONE_UID_SMOKE_COMPLETE_WITH_ONE_PASS_AND_ATTEMPT_LOG
```

Allowed completed final status if all bounded attempts are blocked:

```text
M4_E2_CACHE_MISS_ONE_UID_SMOKE_BLOCKED_NO_PASS_WITH_ATTEMPT_LOG
```

These statuses do not mean full 4,681 is authorized/completed and do not mean
production D4 assets or production pools were modified.

## 2. Candidate attempt queue

Use exactly this queue:

```text
1. A3CST9
2. B8GGQ9
3. A7I9P9
4. A0A0H2V760
5. P0DXZ0
```

Do not add extra UIDs. Do not run all five if an earlier UID passes. Stop after
the first complete PASS.

Preflight evidence summary:

| UID | Stratum | Seq len | P2Rank score | Predicted residues |
|---|---|---:|---:|---:|
| `A3CST9` | `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 398 | 118.99 | 302 |
| `B8GGQ9` | `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 399 | 113.98 | 302 |
| `A7I9P9` | `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 398 | 108.91 | 284 |
| `A0A0H2V760` | `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 400 | 48.35 | 327 |
| `P0DXZ0` | `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 399 | 42.45 | 313 |

For each candidate, the preflight reported:

```text
local_sequence_present=True
phase1_pass_asset_present=False
current_target_esm2_3b_cache_status=cache_miss
current_target_pocket_node_cache_status=cache_miss
current_target_gvp_cache_status=cache_miss
afdb_structure_probe_status=AFDB_STRUCTURE_AVAILABLE
p2rank_preflight_status=PASS
P2Rank top_pocket_found=True
```

Recheck these facts before attempting each UID because the Chenyu state may have
changed since preflight.

## 3. Fresh output locations

Use fresh paths only:

```text
PROJECT_REPO=/root/projects/EnzymeCAGE-master
RETURN_ROOT=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
RETURN_DIR=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_e2_cache_miss_one_uid_smoke_bounded_fallback_20260813
ARCHIVE=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_e2_cache_miss_one_uid_smoke_bounded_fallback_20260813.tar.gz
IDENTITY=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_e2_cache_miss_one_uid_smoke_bounded_fallback_20260813.tar.gz.identity.txt
WORK_ROOT=/tmp/enzymecage_m4_e2_cache_miss_one_uid_smoke_bounded_fallback_20260813
```

If any of `RETURN_DIR`, `ARCHIVE`, `IDENTITY`, or `WORK_ROOT` already exists, do
not overwrite, delete, reuse, or repair it. Create a minimal uniquely suffixed
fail-closed package and report:

```text
M4_E2_CACHE_MISS_ONE_UID_SMOKE_BLOCKED_OUTPUT_PATH_EXISTS
```

## 4. Hard safety boundaries

Read-only inspection is allowed. Generated smoke outputs must stay under:

```text
WORK_ROOT
RETURN_DIR
```

Do not write to or mutate:

```text
/usrdata/EnzymeCAGE_data/feature
/usrdata/EnzymeCAGE_data/formal_splits
/usrdata/EnzymeCAGE_data/models
/usrdata/EnzymeCAGE_runs/checkpoints
/root/projects/EnzymeCAGE-master/data
/root/projects/EnzymeCAGE-master/dataset
```

Do not run:

```text
full 4,681 UID backfill;
bulk UID backfill;
production D4 merge;
production pool mutation;
model training;
AlphaFill fallback;
old-pool pocket reuse as rescue;
PDB-REDO/SMR/experimental-PDB rescue;
apt/conda/pip install.
```

Do not modify source code in the project repo. If you need a run script, write
it under:

```text
${RETURN_DIR}/scripts/
```

## 5. Required environment and route checks

Before attempts, write:

```text
ENVIRONMENT_REPORT.txt
P2RANK_VERSION_AND_INSTALL_REPORT.txt
INPUT_EVIDENCE_REPORT.md
INPUT_EVIDENCE_REPORT.json
FORMAL_ASSET_MUTATION_CHECK.json
```

Check and record:

```text
Python version;
PyTorch version;
CUDA availability if relevant;
ESM package import status;
Bio.PDB import status;
P2Rank path and version;
Phase 1 return path exists;
candidate preflight identity path exists;
production roots snapshots before run.
```

Use the audited P2Rank directory:

```text
P2RANK_DIR=/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1
PRANK=/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1/prank
EXPECTED_PRANK_VERSION=P2Rank 2.5.1
```

Required P2Rank command contract:

```text
prank predict -threads 4 -c alphafold -visualizations 0 ...
```

Keep the PyTorch 2.7 ESM compatibility patch if needed:

```text
torch.load(..., weights_only=False)
```

## 6. Per-UID attempt workflow

For each UID in the queue:

### 6.1 Recheck candidate preconditions

Before doing extraction, recheck and record:

```text
local_sequence_present;
sequence_length;
phase1_pass_asset_present;
current_target_esm2_3b_cache_status;
current_target_pocket_node_cache_status;
current_target_gvp_cache_status;
AFDB structure availability;
P2Rank availability.
```

If the UID is now a target-route cache hit, do not count it as the cache-miss
smoke PASS. Mark:

```text
SKIPPED_NOT_CACHE_MISS_AT_ATTEMPT_TIME
```

and continue to the next UID.

### 6.2 Fetch and normalize AFDB structure

Use AlphaFoldDB only:

```text
https://alphafold.ebi.ac.uk/files/AF-<UID>-F1-model_v6.pdb
https://alphafold.ebi.ac.uk/files/AF-<UID>-F1-model_v6.cif
```

Prefer PDB. If PDB is unavailable and CIF is available, normalize CIF to PDB
using the same corrected parser logic from the Phase 1 CIF fix:

```text
Source CIF -> MMCIFParser -> PDBIO -> normalized PDB -> PDBParser verification.
```

Write all raw/normalized structure files only under:

```text
per_uid/<UID>/raw/
per_uid/<UID>/structure/
```

### 6.3 Run P2Rank top-pocket prediction

Run:

```text
prank predict -threads 4 -c alphafold -visualizations 0 ...
```

Use per-UID `.ds` files. Output must stay under:

```text
per_uid/<UID>/p2rank/
```

Select the top predicted pocket only. Write:

```text
per_uid/<UID>/p2rank/raw/
per_uid/<UID>/pockets/pocket/<UID>.pdb
per_uid/<UID>/pockets/pocket_info.csv
```

If no usable top pocket is produced, mark:

```text
BLOCKED_AFDB_P2RANK_NO_POCKET
```

and continue to the next UID.

### 6.4 ESM-2 3B cache-miss extraction and staged cache write

Run ESM-2 3B for this UID from local sequence only:

```text
model_name=esm2_t36_3B_UR50D
repr_layer=36
embedding_dim=2560
```

Do not write to the production ESM cache. Write smoke-stage outputs only:

```text
staged_smoke_assets/<UID>/esm3b/protein_level/seq2feature.pkl
staged_smoke_assets/<UID>/esm3b/pocket_node_feature/esm_node_feature.torch.pt
```

Required proof fields:

```text
pre_attempt_esm2_3b_cache_status=cache_miss
post_stage_seq2feature_exists=true
post_stage_pocket_node_feature_exists=true
production_esm_cache_mutated=false
```

### 6.5 Same-pocket GVP extraction

Use the same predicted-pocket PDB from 6.3. Write:

```text
staged_smoke_assets/<UID>/gvp/gvp_protein_feature_flat.pt
```

Required proof fields:

```text
same_pocket_for_esm_node_and_gvp=true
post_stage_gvp_exists=true
production_gvp_cache_mutated=false
```

### 6.6 Isolated loader validation

Create a minimal validation input under:

```text
staged_smoke_assets/<UID>/validation_input.csv
```

Run isolated `load_geometric_dataset` validation using the staged smoke assets.
Do not point the loader at production writes. It may read immutable reaction
metadata/configs if required, but output must stay under `RETURN_DIR` or
`WORK_ROOT`.

Validation must prove:

```text
loader_validation_called=true
loader_validation_pass=true
uid_loaded=<UID>
protein_level_feature_loaded_from_staged_smoke=true
pocket_node_feature_loaded_from_staged_smoke=true
gvp_feature_loaded_from_staged_smoke=true
```

If loader validation passes, mark this UID:

```text
PASS_CACHE_MISS_AFDB_P2RANK_PREDICTED_POCKET_STAGED_D4_LOADER_SMOKE
```

Then stop and do not attempt remaining fallback UIDs.

## 7. Required output files

`RETURN_DIR` must contain:

```text
FINAL_STATUS.txt
ENVIRONMENT_REPORT.txt
P2RANK_VERSION_AND_INSTALL_REPORT.txt
INPUT_EVIDENCE_REPORT.md
INPUT_EVIDENCE_REPORT.json
FORMAL_ASSET_MUTATION_CHECK.json
ATTEMPT_STATUS_TABLE.csv
ATTEMPT_TIMING_RESOURCE_TABLE.csv
CACHE_MISS_SMOKE_REPORT.md
CACHE_MISS_SMOKE_REPORT.json
STRUCTURE_SOURCE_TABLE.csv
P2RANK_ATTEMPT_TABLE.csv
STAGED_SMOKE_ASSET_MANIFEST.csv
LOADER_VALIDATION_REPORT.md
LOADER_VALIDATION_REPORT.json
COMMAND_LOG.txt
MANIFEST.sha256
scripts/run_m4_e2_cache_miss_one_uid_smoke.py
per_uid/<UID>/REPORT.md
per_uid/<UID>/REPORT.json
```

For the PASS UID, `STAGED_SMOKE_ASSET_MANIFEST.csv` must include:

```text
staged_smoke_assets/<UID>/pockets/pocket/<UID>.pdb
staged_smoke_assets/<UID>/pockets/pocket_info.csv
staged_smoke_assets/<UID>/esm3b/protein_level/seq2feature.pkl
staged_smoke_assets/<UID>/esm3b/pocket_node_feature/esm_node_feature.torch.pt
staged_smoke_assets/<UID>/gvp/gvp_protein_feature_flat.pt
staged_smoke_assets/<UID>/validation_input.csv
```

For skipped or blocked UIDs, include per-UID reports but do not include staged
smoke asset manifest entries unless an asset was actually produced under the
allowed smoke directory.

## 8. Required summary fields

`CACHE_MISS_SMOKE_REPORT.json` must include:

```text
task_id
final_status
attempt_queue
attempted_uids
skipped_uids
blocked_uids
pass_uid
n_attempted
n_skipped
n_blocked
n_pass
stop_after_first_pass=true
candidate_preflight_archive_sha256
candidate_preflight_identity_fields
phase1_reference_counts
per_uid_final_status
per_uid_blocker_reason
pre_attempt_cache_status_by_uid
post_stage_asset_status_by_uid
loader_validation_called
loader_validation_pass
formal_asset_mutation_check
production_pool_mutated=false
full_4681_backfill_run=false
production_d4_mutated=false
staged_smoke_assets_generated=true/false
```

If a PASS occurs:

```text
n_pass=1
pass_uid=<UID>
staged_smoke_assets_generated=true
```

If no PASS occurs:

```text
n_pass=0
pass_uid=null
staged_smoke_assets_generated=false unless partial staged smoke files were produced
```

## 9. Manifest, archive, and identity

Fix the manifest self-inclusion issue from the candidate preflight package.

Before archiving:

```text
cd ${RETURN_DIR}
find . -type f ! -name MANIFEST.sha256 -print0 | sort -z | xargs -0 sha256sum > MANIFEST.sha256
sha256sum -c MANIFEST.sha256
```

Create:

```text
${ARCHIVE}
${IDENTITY}
```

The identity file must include:

```text
task_id
final_status
attempt_queue
attempted_uids
pass_uid
n_attempted
n_pass
n_blocked
n_skipped
candidate_preflight_archive_sha256
archive_sha256
archive_bytes
created_utc
formal_assets_mutated=false
production_pool_mutated=false
full_4681_backfill_run=false
production_d4_mutated=false
staged_smoke_assets_generated=true/false
stop_after_first_pass=true
```

Do not report success without both archive and identity file.

## 10. Final status tokens

Completed with one PASS:

```text
M4_E2_CACHE_MISS_ONE_UID_SMOKE_COMPLETE_WITH_ONE_PASS_AND_ATTEMPT_LOG
```

Completed but no PASS after bounded attempts:

```text
M4_E2_CACHE_MISS_ONE_UID_SMOKE_BLOCKED_NO_PASS_WITH_ATTEMPT_LOG
```

Blocked before attempts:

```text
M4_E2_CACHE_MISS_ONE_UID_SMOKE_BLOCKED_OUTPUT_PATH_EXISTS
M4_E2_CACHE_MISS_ONE_UID_SMOKE_BLOCKED_REQUIRED_INPUTS_MISSING
M4_E2_CACHE_MISS_ONE_UID_SMOKE_BLOCKED_ENVIRONMENT_MISSING
M4_E2_CACHE_MISS_ONE_UID_SMOKE_BLOCKED_P2RANK_MISSING
```

Per-UID final statuses may include:

```text
PASS_CACHE_MISS_AFDB_P2RANK_PREDICTED_POCKET_STAGED_D4_LOADER_SMOKE
SKIPPED_NOT_CACHE_MISS_AT_ATTEMPT_TIME
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED
BLOCKED_AFDB_STRUCTURE_PARSE_FAILED
BLOCKED_AFDB_P2RANK_NO_POCKET
BLOCKED_ESM2_3B_EXTRACTION_FAILED
BLOCKED_GVP_EXTRACTION_FAILED
BLOCKED_LOADER_VALIDATION_FAILED
BLOCKED_ENVIRONMENT_ERROR
NOT_ATTEMPTED_STOP_AFTER_PRIOR_PASS
```
