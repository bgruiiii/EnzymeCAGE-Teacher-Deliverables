# Local audit: M4 Phase 1 acceptance CIF parser fix clean 100-UID rerun return

Date: 2026-08-11

Audited archive:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811.tar.gz
```

External identity:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811.tar.gz.identity.txt
```

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M4_PHASE1_CONDITIONAL_APPROVAL_2026-08-11.md
```

Corrective prompt:

```text
07_HPC_Prompts/
HPC_ENZYMECAGE_M4_PHASE1_ACCEPTANCE_CIF_PARSER_FIX_CLEAN_100UID_RERUN_EXECUTOR_ONLY_PROMPT_2026-08-11.md
```

## 1. Verdict

Verdict:

```text
LOCAL_AUDIT_PASS_AS_PHASE1_ACCEPTANCE_CANDIDATE_WITH_HONEST_BLOCKER_COUNTS
```

This corrected Chenyu return satisfies the local audit requirements for the
teacher-authorized Phase 1 acceptance candidate:

```text
100 frozen UIDs were rerun cleanly;
the CIF/PDB parser false-blocker class is cleared;
41 UIDs produced staged lower-evidence AFDB-only P2Rank predicted-pocket D4
assets and passed ESM-2 3B, same-pocket GVP, and isolated loader validation;
59 UIDs have explicit blocker statuses;
F3 numeric reproduction passed on Chenyu from the packaged payload source
snapshot;
internal manifest and external identity checks pass;
formal/production mutation flags are false.
```

Important boundary:

```text
This is not teacher approval, not a full 4,681-UID backfill, not a production
merge, and not a claim that P2Rank predicted pockets are equivalent to strict
AlphaFill-derived pocket assets.
```

Recommended next action:

```text
Use this corrected return as the current Phase 1 acceptance package candidate
for teacher-facing packaging/upload, after user approval.
```

## 2. Archive identity and integrity

Local archive SHA256:

```text
4dcbfb5387812c284dd00aade46ec3fb1a5c923ab8e751376a423ada7d8d1afa
```

External identity reported archive SHA256:

```text
4dcbfb5387812c284dd00aade46ec3fb1a5c923ab8e751376a423ada7d8d1afa
```

Archive bytes:

```text
24334733
```

External identity reported archive bytes:

```text
24334733
```

Internal manifest:

```text
sha256sum -c MANIFEST.sha256: exit code 0, all listed files OK
```

External identity fields match `PHASE1_ACCEPTANCE_REPORT.json` for:

```text
n_input_uids
n_unique_input_uids
n_pass_afdb_p2rank_predicted_pocket_d4_loader
n_blocked_total
n_afdb_structure_parse_failed
n_p2rank_no_pocket
n_esm2_3b_cache_hit
n_esm2_3b_cache_miss
```

## 3. Required file coverage

Required top-level files/directories are present:

```text
CIF_PARSER_FIX_PROOF.json
ENVIRONMENT_REPORT.txt
F3_Numeric_Reproduction_Path_2026-08-11/
FINAL_STATUS.txt
FORMAL_ASSET_MUTATION_CHECK.json
MANIFEST.sha256
P2RANK_VERSION_AND_INSTALL_REPORT.txt
PER_UID_STATUS_TABLE.csv
PER_UID_TIMING_RESOURCE_TABLE.csv
PHASE1_ACCEPTANCE_REPORT.md
PHASE1_ACCEPTANCE_REPORT.json
SAMPLED_UIDS.csv
SAMPLE_DESIGN_REPORT.md
SAMPLE_DESIGN_REPORT.json
STAGED_ASSET_MANIFEST.csv
STRUCTURE_SOURCE_TABLE.csv
scripts/run_m4_phase1_acceptance_cif_parser_fix.py
per_uid/<UID>/REPORT.md
per_uid/<UID>/REPORT.json
```

For PASS UIDs:

| Check | Result |
|---|---:|
| PASS UIDs | 41 |
| `STAGED_ASSET_MANIFEST.csv` rows | 246 |
| Expected rows | 41 x 6 = 246 |
| Unique asset UIDs | 41 |
| Non-PASS UIDs with staged manifest entries | 0 |
| Missing required PASS asset entries | 0 |
| `exists=False` or absent manifest-listed files | 0 |

The archive contains additional staged helper files under `staged_assets/`, but
the manifest includes the 6 required deliverable asset paths per PASS UID.

## 4. F3 numeric reproduction audit

F3 means the count-reproduction check that proves why the current strict enzyme
universe has `4,681` UIDs missing valid pocket assets.

Chenyu F3 rerun report:

| Check | Result |
|---|---|
| `f3_reproduction_pass` | true |
| `expected_count_mismatches` | `{}` |
| `strict_cleaned_2026_main_table_uid` | 195,743 |
| `strict_uid_missing_valid_pocket` | 4,681 |
| `full_4681_backfill_authorized_or_claimed` | false |
| `uid_backfill_run` | false |
| `production_assets_mutated` | false |

Interpretation:

```text
The teacher-required F3 reproduction path is present and was rerun on Chenyu
from the packaged payload source snapshot. The key counts match expected
values.
```

## 5. Frozen UID audit

Returned `SAMPLED_UIDS.csv` SHA256 matches the local frozen manifest:

```text
dd8504524880c19cf0177a762889d44a7225e035dc9dc0b82861867b0678bd18
```

Frozen sample checks:

| Check | Result |
|---|---:|
| rows | 100 |
| unique `UniprotID` | 100 |
| `strict_2026_uid=true` | 100 |
| `local_sequence_present=true` | 100 |
| `f3_missing_valid_pocket_member=true` | 100 |
| `final_missing_pocket_uid_member=true` | 100 |
| `appeared_in_previous_2026_08_03_pilots=false` | 100 |
| `main_acceptance_denominator=true` | 100 |

Strata:

| Stratum | Total |
|---|---:|
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 35 |
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 25 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 40 |

## 6. Main result recount

Reported and locally recounted status distribution:

| Final status | Count |
|---|---:|
| `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 41 |
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | 44 |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | 15 |
| `BLOCKED_AFDB_STRUCTURE_PARSE_FAILED` | 0 |

By stratum:

| Stratum | PASS | P2Rank no pocket | AFDB fetch failed |
|---|---:|---:|---:|
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 6 | 28 | 1 |
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 25 | 0 | 0 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 10 | 16 | 14 |

Interpretation:

```text
Every frozen UID has exactly one final status. The corrected rerun improves the
previous package from 38 PASS / 62 blocked to 41 PASS / 59 blocked, and removes
the 7 script-induced CIF parser false blockers.
```

## 7. CIF parser fix audit

Required proof file:

```text
CIF_PARSER_FIX_PROOF.json
```

Proof contents:

| Field | Value |
|---|---|
| `test_uid` | `C5B8H7` |
| `raw_cif_first_line` | `data_AF-C5B8H7-F1` |
| `normalized_pdb_exists` | true |
| `normalized_pdb_atom_line_count` | 753 |
| `normalize_structure_status` | `PASS` |

Previously false-blocked UID outcomes:

| UID | Corrected final status |
|---|---|
| `C5B8H7` | `BLOCKED_AFDB_P2RANK_NO_POCKET` |
| `Q9BZG8` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` |
| `Q29451` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` |
| `A0A0U3S9Q3` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` |
| `P0DJN3` | `BLOCKED_AFDB_P2RANK_NO_POCKET` |
| `A6SUD8` | `BLOCKED_AFDB_P2RANK_NO_POCKET` |
| `Q8UFS9` | `BLOCKED_AFDB_P2RANK_NO_POCKET` |

Interpretation:

```text
The prior `BLOCKED_AFDB_STRUCTURE_PARSE_FAILED` class is cleared. Three of the
seven became PASS after the parser fix; four became genuine P2Rank no-pocket
blockers under the approved route.
```

## 8. Why blocked remains high

Plain-language explanation:

```text
These 100 enzymes were deliberately sampled from the missing-pocket gap, so
they are hard cases by design. Phase 1 acceptance asks the tool to either build
staged assets or record precise blockers. It does not require 100/100 PASS.
```

Blocker meanings:

| Blocker | Count | Meaning |
|---|---:|---|
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | 44 | AFDB structure was available and P2Rank ran, but no usable top predicted pocket was produced under the approved command contract. This is not a download failure. |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | 15 | AFDB structure could not be fetched for this run. `STRUCTURE_SOURCE_TABLE.csv` shows 12 HTTP 404 cases and 3 HTTP 000 cases. |

Structure table recount:

| Structure field | Count |
|---|---:|
| HTTP 200 | 85 |
| HTTP 404 | 12 |
| HTTP 000 | 3 |
| parser `PASS` | 85 |
| selected chain `A` | 85 |
| AFDB model version `v6` | 85 |

The report field is named `list_of_afdb_404_uids`, but local recount shows the
15 fetch-blocked UIDs consist of 12 HTTP 404 plus 3 HTTP 000 statuses.

Fetch-blocked UIDs:

```text
A0A7H0DNE2,P03133,P04382,P0CAP6,P27328,P29263,P68761,P85362,
P85432,P86056,Q19QT7,Q4AEH3,Q73FJ3,Q9IR51,Q9Z1Y9
```

P2Rank no-pocket UIDs:

```text
A0PPX3,A3PCN9,A3PI89,A5FAD3,A6SUD8,A6U306,A7Z9N5,A8ERD0,
B1X900,B5ZBT1,B8GZJ6,B9RRX2,C4Z1K1,C5B8H7,O28185,O32868,
P05794,P0DJM9,P0DJN3,P0DJR1,P10801,P19980,P21792,P31198,
P47724,P80575,P85061,P9WN59,Q03284,Q0RDK8,Q12H06,Q1QVB6,
Q24QL6,Q2RGY3,Q39BW2,Q54RY8,Q59584,Q6GEE6,Q7LZG3,Q7WG14,
Q87WS0,Q8UFS9,Q9FCD2,Q9PIA5
```

## 9. P2Rank and route audit

P2Rank report:

| Field | Value |
|---|---|
| `P2RANK_DIR` | `/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1` |
| expected archive SHA256 | `d243f2d9036ac053fefb9407b5fe1c85f4fe077c519fd975ac585e995feab274` |
| actual archive SHA256 | `d243f2d9036ac053fefb9407b5fe1c85f4fe077c519fd975ac585e995feab274` |
| archive SHA verified | true |
| version | `P2Rank 2.5.1` |
| command contract | `prank predict -threads 4 -c alphafold -visualizations 0 ...` |
| commit field | `expected-but-not-locally-proven (no .git metadata in release tarball)` |

Route status:

```text
AlphaFoldDB structure only;
P2Rank top predicted pocket only;
ESM-2 3B model_name=esm2_t36_3B_UR50D, repr_layer=36,
embedding_dim=2560;
same predicted-pocket PDB for GVP and ESM pocket-node features;
isolated loader validation;
staged assets only.
```

The successful PASS token is:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER
```

No strict AlphaFill full-loader PASS token is used as the successful route
token in `PER_UID_STATUS_TABLE.csv`.

## 10. Mutation and boundary audit

Per-UID mutation flags:

| Field | Count |
|---|---:|
| `formal_assets_mutated=False` | 100 |
| `production_pool_mutated=False` | 100 |

`FORMAL_ASSET_MUTATION_CHECK.json`:

```json
{
  "formal_feature_root_mutated": false,
  "formal_split_root_mutated": false,
  "production_data_root_mutated": false,
  "production_dataset_root_mutated": false
}
```

Boundary checks:

```text
No full 4,681 UID backfill claimed.
No production D4 merge claimed.
No production pool mutation claimed.
No claim that P2Rank predicted pockets equal strict AlphaFill pockets.
No teacher approval claimed.
Commit 255a05e is not claimed as locally proven; the P2Rank report correctly
states that the release tarball has no .git metadata.
```

## 11. Final local interpretation

This corrected package is locally acceptable as the current M4 Phase 1
acceptance candidate because it meets the teacher-authorized shape:

```text
F3 count reproducibility;
frozen 100 UID denominator;
AFDB-only P2Rank lower-evidence pocket route;
staged D4 assets for PASS cases;
honest blocker counts for non-PASS cases;
no production mutation.
```

The remaining 59 blockers should be reported as blockers, not hidden or
treated as failures of the rerun. The key wording for the teacher should be:

```text
41/100 completed as staged AFDB-only P2Rank predicted-pocket D4 acceptance
assets; 44/100 were blocked because P2Rank produced no usable top predicted
pocket after AFDB structure retrieval; 15/100 were blocked by AFDB structure
fetch failure; 0/100 remain blocked by the previous CIF parser bug.
```
