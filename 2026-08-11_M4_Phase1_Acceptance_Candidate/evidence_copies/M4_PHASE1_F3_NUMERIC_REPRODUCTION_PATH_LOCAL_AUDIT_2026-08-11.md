# Local audit: M4 Phase 1 F3 numeric reproduction path package

Date: 2026-08-11

Audited package:

```text
01_Path_Contract_Objective/
M4_Phase1_Acceptance_Execution_2026-08-11/
F3_Numeric_Reproduction_Path_2026-08-11/
```

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M4_PHASE1_CONDITIONAL_APPROVAL_2026-08-11.md
```

Teacher-required condition:

```text
F3 verification path = script + Rhea/UniProt snapshot versions,
to be delivered with the Phase 1 acceptance package.
```

## 1. Verdict

Verdict:

```text
ACCEPT_F3_NUMERIC_REPRODUCTION_PATH_PACKAGE
```

The package satisfies the narrow local requirement:

```text
F3 counts can be reproduced from local fixed inputs with a script, and the
Rhea/UniProt snapshot source is recorded with file identities.
```

This audit does not claim the Phase 1 acceptance package is complete. It also
does not claim that the >=100 UID acceptance subset has been run.

## 2. Package files

| File | Present | Role |
|---|---|---|
| `F3_REPRODUCE_COUNTS.py` | yes | stdlib-only reproduction script |
| `F3_REPRODUCTION_REPORT.md` | yes | human-readable report |
| `F3_REPRODUCTION_REPORT.json` | yes | machine-readable counts and boundaries |
| `F3_INPUT_SNAPSHOT_MANIFEST.tsv` | yes | source file identities and snapshot versions |
| `F3_REPRODUCTION_SHA256SUMS.txt` | yes | package integrity hashes |

SHA256 verification:

```text
F3_REPRODUCE_COUNTS.py: OK
F3_REPRODUCTION_REPORT.md: OK
F3_REPRODUCTION_REPORT.json: OK
F3_INPUT_SNAPSHOT_MANIFEST.tsv: OK
```

Execution check:

```text
python3 F3_REPRODUCE_COUNTS.py
F3_REPRODUCTION_PASS
```

## 3. Snapshot identity audit

The package records these snapshot/source identities:

| Source | Snapshot / role | SHA256 |
|---|---|---|
| `data/raw/rhea/RHEA-140_2026-01-21/tsv/rhea2ec.tsv` | Rhea complete-EC source table; `RHEA-140_2026-01-21` | `5a90d95d4aab686b4a0c46db6495b89c6431696f4bb351a5a63e4c84a3187d44` |
| `data/raw/rhea/RHEA-140_2026-01-21/tsv/rhea2uniprot_sprot.tsv` | reviewed UniProt/Swiss-Prot UID mapping inside `RHEA-140_2026-01-21` | `89efa346087108e8b0abbeb3d8739a15d1979951bcfa9b42fa01d8786c5d827e` |
| `data/raw/rhea/RHEA-140_2026-01-21/uid2seq.pkl` | local sequence universe for same Rhea snapshot | `e427c6301dbff05a18e9de973f4480cb11474b1a8cf763f31dd0fc91f6f733cc` |
| `data/processed/rhea/2026-01-21/all_enzymes.csv` | strict cleaned 2026 enzyme UID universe | `a99965d91101c3415e222736ebc6ceaa151310be9be70c32a95fe2ee81d7cf30` |
| `data/processed/rhea/2026-01-21/pockets/pocket_info.csv` | strict pocket metadata / valid-pocket universe | `7c8904c4fe9858d641dd155d70465d5e6e5e46ca95780ec20207b1f8d927f391` |
| `t3_1_full_esm2_3b_extraction/outputs/final_feature_counts.csv` | local ESM2-3B corrected feature UID universe | `5df73708481699b96a70b7ed4aa91bca74a0358e2be4de39ffe1772f9018d366` |
| `selected_training_uids.csv` | training-clean selected UID universe | `91db83657eb388c657cce0f89c9a7fa423a0db21040ce2a8d729ee9da762d712` |

Important wording:

```text
The UniProt source is rhea2uniprot_sprot.tsv inside RHEA-140_2026-01-21,
that is, a reviewed UniProtKB/Swiss-Prot cross-reference shipped with the Rhea
snapshot. It is not a live UniProt query and not a broader TrEMBL/all-EC sweep.
```

## 4. Reproduced counts

The script reproduces the F3 counts from the 2026-08-04 local audit:

| Count | Reproduced value | Result |
|---|---:|---|
| raw Rhea-linked UniProt UID | 236,103 | PASS |
| strict cleaned 2026 main-table UID | 195,743 | PASS |
| strict valid pocket UID | 191,062 | PASS |
| strict UID missing valid pocket | 4,681 | PASS |
| local ESM2-3B corrected feature UID | 107,705 | PASS |
| strict UID missing local ESM2-3B | 88,038 | PASS |
| complete EC count | 6,151 | PASS |
| Rhea official complete-EC source UID | 218,010 | PASS |

Complete-EC coverage reproduced:

| Asset / UID set | Covered | Missing |
|---|---:|---:|
| local sequence | 218,010 | 0 |
| strict cleaned `all_enzymes.csv` | 186,909 | 31,101 |
| strict pocket metadata | 182,998 | 35,012 |
| strict valid pocket rows | 182,770 | 35,240 |
| local ESM2-3B 107,705 subdomain | 103,206 | 114,804 |
| training-clean selected 107,731 UID | 103,231 | 114,779 |

Machine-readable expected-count check:

```text
expected_count_mismatches = {}
```

## 5. Method audit

Script method:

```text
complete EC regex: ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$
complete EC join:
  rhea2ec.tsv complete EC MASTER_ID
  -> rhea2uniprot_sprot.tsv MASTER_ID
  -> reviewed UniProt accession ID
valid pocket rule:
  non-empty pocket_residues in pocket_info.csv, counted by unique UniprotID
```

This matches the F3 audit's stated local Rhea 140 EC baseline. It does not
replace the source contract with a live UniProt/BRENDA/TrEMBL candidate source.

## 6. Boundary / no-overclaim audit

This package does not support claiming:

```text
Phase 1 acceptance package is complete;
Phase 1 >=100 UID acceptance run has started;
full 4,681 UID backfill is authorized or complete;
production D4 assets were generated or merged;
production pool was modified;
live UniProt complete-EC sweep was performed;
P2Rank predicted pockets equal strict AlphaFill pockets;
the prohibited full-D4-loader PASS label for the predicted-pocket route.
```

Allowed narrow claim:

```text
F3 numeric reproduction path has been prepared locally and reproduces the
previously audited F3 counts from fixed local snapshots.
```

## 7. Next action

After this F3 reproduction package, the next local task can proceed to
sample-freeze planning for the >=100 UID acceptance subset.

Do not start the >=100 UID acceptance run until the frozen subset contract and
prompt are separately prepared and audited.

Final local audit status:

```text
F3_REPRODUCTION_SCRIPT_PRESENT_PASS
F3_SNAPSHOT_MANIFEST_PRESENT_PASS
F3_SHA256SUMS_PASS
F3_EXPECTED_COUNTS_MATCH_PASS
F3_RHEA_UNIPROT_SNAPSHOT_VERSION_RECORDED_PASS
NO_LIVE_UNIPROT_QUERY_PASS
NO_UID_BACKFILL_PASS
NO_PRODUCTION_MUTATION_PASS
NEXT_STEP_SAMPLE_FREEZE_PLANNING
```
