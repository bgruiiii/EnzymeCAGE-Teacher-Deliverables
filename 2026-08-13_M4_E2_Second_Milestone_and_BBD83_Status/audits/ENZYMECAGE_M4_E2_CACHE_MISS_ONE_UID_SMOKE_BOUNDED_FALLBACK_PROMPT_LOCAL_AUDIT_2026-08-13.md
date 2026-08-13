# Local audit: M4 E2 cache-miss one-UID smoke bounded fallback prompt

Date: 2026-08-13

Audited prompt:

```text
07_HPC_Prompts/
HPC_ENZYMECAGE_M4_E2_CACHE_MISS_ONE_UID_SMOKE_BOUNDED_FALLBACK_EXECUTOR_ONLY_PROMPT_2026-08-13.md
```

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_PROJECT_NEXT_STEPS_GUIDANCE_2026-08-13.md
```

Input candidate audit:

```text
04_Local_Review_Audits/
ENZYMECAGE_M4_E2_CACHE_MISS_SMOKE_CANDIDATE_PREFLIGHT_RETURN_LOCAL_AUDIT_2026-08-13.md
```

Input candidate return:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_cache_miss_smoke_candidate_preflight_20260813.tar.gz
```

## 1. Verdict

Verdict:

```text
ACCEPT_M4_E2_CACHE_MISS_ONE_UID_SMOKE_PROMPT_FOR_USER_REVIEW
```

The prompt is suitable for user review as the next Chenyu/HPC executor-only
instruction for teacher's M4 E2 observation point 1.

It asks Chenyu to obtain exactly one complete cache-miss smoke PASS:

```text
extract -> staged cache write -> same-pocket GVP/ESM pocket-node -> isolated
loader validation.
```

It does not authorize:

```text
full 4,681 backfill;
bulk UID backfill;
production D4 merge;
production pool mutation;
M4b implementation;
arbitrary external UniProt UID substitution.
```

## 2. Why bounded fallback is acceptable

Teacher asked for:

```text
1 cache-miss UID extraction smoke.
```

The prompt keeps that target by requiring:

```text
stop_after_first_pass=true;
n_pass must be 0 or 1;
do not attempt later fallback UIDs after the first complete PASS.
```

The fallback queue is not a mini backfill. It is an execution-safety measure:

```text
If A3CST9 fails due to environment, AFDB, P2Rank, ESM, GVP, or loader issues,
the executor may continue to the next pre-audited UID rather than returning
without any observation-point evidence. Every attempted UID must still be
reported.
```

## 3. Candidate queue audit

The prompt uses only the top five locally audited candidates:

```text
A3CST9 -> B8GGQ9 -> A7I9P9 -> A0A0H2V760 -> P0DXZ0
```

These candidates came from the M4 final-missing-pocket universe, not arbitrary
external UniProt selection.

Candidate preflight facts reused in the prompt:

```text
local_sequence_present=True;
phase1_pass_asset_present=False;
current_target_esm2_3b_cache_status=cache_miss;
current_target_pocket_node_cache_status=cache_miss;
current_target_gvp_cache_status=cache_miss;
afdb_structure_probe_status=AFDB_STRUCTURE_AVAILABLE;
p2rank_preflight_status=PASS;
P2Rank top_pocket_found=True.
```

The prompt also requires rechecking these facts before each attempt because
Chenyu state may have changed after preflight.

## 4. Route audit

The prompt preserves the accepted Phase 1 lower-evidence route:

```text
AlphaFoldDB structure only;
P2Rank 2.5.1 top predicted pocket only;
ESM-2 3B model_name=esm2_t36_3B_UR50D, repr_layer=36, embedding_dim=2560;
same predicted-pocket PDB for GVP and ESM pocket-node features;
isolated load_geometric_dataset validation;
staged outputs only.
```

It explicitly forbids rescue routes:

```text
AlphaFill fallback;
old-pool pocket reuse as rescue;
PDB-REDO;
SMR;
experimental PDB.
```

## 5. Output and auditability

The prompt requires an attempt log and per-UID reports:

```text
ATTEMPT_STATUS_TABLE.csv
ATTEMPT_TIMING_RESOURCE_TABLE.csv
per_uid/<UID>/REPORT.md/json
```

This is important because if multiple UIDs are attempted, the final package
will not hide failed or skipped attempts behind the one successful example.

For a PASS UID, the required staged smoke assets are:

```text
staged_smoke_assets/<UID>/pockets/pocket/<UID>.pdb
staged_smoke_assets/<UID>/pockets/pocket_info.csv
staged_smoke_assets/<UID>/esm3b/protein_level/seq2feature.pkl
staged_smoke_assets/<UID>/esm3b/pocket_node_feature/esm_node_feature.torch.pt
staged_smoke_assets/<UID>/gvp/gvp_protein_feature_flat.pt
staged_smoke_assets/<UID>/validation_input.csv
```

The summary must report:

```text
attempt_queue
attempted_uids
skipped_uids
blocked_uids
pass_uid
n_attempted
n_pass
stop_after_first_pass=true
loader_validation_called
loader_validation_pass
production_pool_mutated=false
full_4681_backfill_run=false
production_d4_mutated=false
```

## 6. Safety boundary audit

The prompt permits generated smoke outputs only under:

```text
WORK_ROOT
RETURN_DIR
```

It forbids writes to:

```text
/usrdata/EnzymeCAGE_data/feature
/usrdata/EnzymeCAGE_data/formal_splits
/usrdata/EnzymeCAGE_data/models
/usrdata/EnzymeCAGE_runs/checkpoints
/root/projects/EnzymeCAGE-master/data
/root/projects/EnzymeCAGE-master/dataset
```

It also forbids source-code edits in the project repo; the run script must be
written only under:

```text
${RETURN_DIR}/scripts/
```

## 7. Packaging correction

The previous candidate preflight return had a manifest self-inclusion bug. This
prompt corrects that by requiring:

```text
find . -type f ! -name MANIFEST.sha256 -print0 | sort -z | xargs -0 sha256sum > MANIFEST.sha256
sha256sum -c MANIFEST.sha256
```

So the returned manifest should verify cleanly.

## 8. Red-line audit

The prompt does not use the forbidden success labels:

```text
M4_PRODUCTION_D4_BACKFILL_COMPLETE
M4_ALL_4681_UIDS_BACKFILLED
PASS_FULL_D4_LOADER
```

The allowed PASS token is route-specific:

```text
PASS_CACHE_MISS_AFDB_P2RANK_PREDICTED_POCKET_STAGED_D4_LOADER_SMOKE
```

This is not a strict AlphaFill full-loader PASS token.

## 9. Residual risk

Residual risk:

```text
The prompt requires isolated loader validation but does not hard-code the exact
local helper calls, because the executor must adapt to the current Chenyu repo
state. The returned artifact must therefore be audited carefully for whether
the loader truly read the staged smoke assets rather than silently falling back
to production caches.
```

This risk is acceptable because the prompt requires explicit loader source proof
fields and keeps all production mutation flags false.
