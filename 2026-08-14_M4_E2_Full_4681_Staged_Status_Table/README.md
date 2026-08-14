# M4 E2 full 4,681 staged status table

Date: 2026-08-14

## What This Package Is

This is the Chen Haoran-side M4 E2 full 4,681 staged status-table return package
for Huang teacher review.

It contains the GitHub-side reviewable files:

```text
tables/
reports/
hpc_identity/
audits/
```

The original full Chenyu archive is not committed to GitHub because it is 658M.
Teacher can access it directly on Chenyu/HPC at the path below.

## Chenyu Original Archive

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814.tar.gz
```

Identity sidecar on Chenyu:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814.tar.gz.identity.txt
```

Local audited archive SHA256:

```text
b01e717139f6eb48739e0861f82b339cdc0132ee4777acdd18354ee9da38bdd4
```

Archive size:

```text
689316623 bytes
```

## Main Result

The full 4,681 UID denominator returned one terminal status row per UID:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER    1704
BLOCKED_AFDB_P2RANK_NO_POCKET                  1324
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED            1650
BLOCKED_ESM2_3B_EXTRACTION_FAILED                 3
```

Plain meaning:

```text
1,704 UIDs produced lower-evidence AFDB + P2Rank predicted-pocket staged assets.
1,324 UIDs had AFDB structures and P2Rank ran, but no usable mapped top pocket.
1,650 UIDs could not fetch AFDB v6 structure.
3 UIDs mapped a P2Rank pocket but failed ESM-2 3B feature generation.
```

## Key Review Files

Local audit:

```text
audits/ENZYMECAGE_M4_E2_FULL_4681_4GPU_SHARDED_CONTINUATION_FINAL_RETURN_LOCAL_AUDIT_2026-08-14.md
```

Core status table:

```text
tables/FULL_4681_STAGED_STATUS_TABLE.csv
```

Staged asset manifest:

```text
tables/STAGED_ASSET_MANIFEST.csv
```

Mutation checks:

```text
reports/FORMAL_ASSET_MUTATION_CHECK.json
reports/PRODUCTION_MUTATION_CHECK.json
```

Identity sidecar copy:

```text
hpc_identity/enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814.tar.gz.identity.txt
```

## Boundaries

Do not describe this package as:

```text
production D4 merge
production pool mutation
all 4,681 UIDs successfully backfilled
strict AlphaFill pocket equivalence
full scientific pocket completion
```

Correct wording:

```text
full 4,681 staged status table completed;
1,704 lower-evidence AFDB + P2Rank predicted-pocket staged PASS asset sets;
1,324 P2Rank no-pocket blockers;
1,650 AFDB structure fetch blockers;
3 ESM-2 3B extraction blockers;
formal/production mutation checks false.
```

## Caveats

The accession-review table is structurally present for the 1,650 AFDB
fetch-failed UIDs, but detailed UniProt secondary-accession fields are blank in
this returned package. Therefore do not claim this package itself performed
detailed secondary-accession review for all 1,650 fetch-failed UIDs.

The per-UID `REPORT.json` files inside the Chenyu archive contain Python-style
`NaN` values in many records. The CSV tables are the strict machine-readable
authority for this delivery.

