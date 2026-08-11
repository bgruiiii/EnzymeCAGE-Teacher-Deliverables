# Local audit: M4 Phase 1 acceptance UID freeze

Date: 2026-08-11

Audited package:

```text
01_Path_Contract_Objective/
M4_Phase1_Acceptance_Execution_2026-08-11/
Phase1_Acceptance_UID_Freeze_2026-08-11/
```

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M4_PHASE1_CONDITIONAL_APPROVAL_2026-08-11.md
```

Accepted subset policy source:

```text
01_Path_Contract_Objective/
M4_OnDemand_D4_Backfill_Contract_Direction_Response_2026-08-09/
M4_ONDEMAND_D4_BACKFILL_DIRECTION_RESPONSE_STEP3_WORKLOAD_TIMELINE_ACCEPTANCE_SUBSET_PHASE2_NOTE_2026-08-09.md
```

## 1. Verdict

Verdict:

```text
ACCEPT_PHASE1_ACCEPTANCE_UID_FREEZE
```

The package freezes a compliant 100-UID Phase 1 acceptance subset.

Every main-denominator UID is:

```text
strict 2026 enzyme UID;
present in local sequence evidence;
member of the F3 strict missing-valid-pocket set;
member of the approved final-missing stratum universe;
fresh relative to the 2026-08-03 100-UID pilots.
```

This is a selection/freeze step only. It does not start the acceptance run and
does not process any UID.

## 2. Package files

| File | Present | Role |
|---|---|---|
| `BUILD_PHASE1_ACCEPTANCE_UID_FREEZE.py` | yes | stdlib-only reproducible freeze builder |
| `SAMPLED_UIDS.csv` | yes | frozen 100-UID acceptance manifest |
| `SAMPLE_DESIGN_REPORT.md` | yes | human-readable design report |
| `SAMPLE_DESIGN_REPORT.json` | yes | machine-readable design report |
| `CANDIDATE_POOL_SUMMARY.csv` | yes | stratum eligibility/freshness summary |
| `INPUT_SNAPSHOT_MANIFEST.tsv` | yes | input file identities |
| `UID_FREEZE_SHA256SUMS.txt` | yes | package integrity hashes |

Execution check:

```text
python3 BUILD_PHASE1_ACCEPTANCE_UID_FREEZE.py
PHASE1_ACCEPTANCE_UID_FREEZE_PASS
```

SHA256 check:

```text
BUILD_PHASE1_ACCEPTANCE_UID_FREEZE.py: OK
SAMPLED_UIDS.csv: OK
SAMPLE_DESIGN_REPORT.md: OK
SAMPLE_DESIGN_REPORT.json: OK
CANDIDATE_POOL_SUMMARY.csv: OK
INPUT_SNAPSHOT_MANIFEST.tsv: OK
```

## 3. Source identity audit

Key fixed inputs:

| Source | SHA256 |
|---|---|
| `data/processed/rhea/2026-01-21/all_enzymes.csv` | `a99965d91101c3415e222736ebc6ceaa151310be9be70c32a95fe2ee81d7cf30` |
| `data/processed/rhea/2026-01-21/pockets/pocket_info.csv` | `7c8904c4fe9858d641dd155d70465d5e6e5e46ca95780ec20207b1f8d927f391` |
| `data/raw/rhea/RHEA-140_2026-01-21/uid2seq.pkl` | `e427c6301dbff05a18e9de973f4480cb11474b1a8cf763f31dd0fc91f6f733cc` |
| `t3_1_full_esm2_3b_extraction/outputs/final_feature_counts.csv` | `5df73708481699b96a70b7ed4aa91bca74a0358e2be4de39ffe1772f9018d366` |
| `final_missing_pocket_uids.csv` | `c65d6035455296b9954abcdf9676a6a53d4dc7d9b19ae9cb385c8c5ff592a940` |
| `alphafill_success_no_pocket.csv` | `d3ac00a9e9ba3f12616bce47f591f2d20bb14838e10e5afe0edcbcc496ede66d` |
| `missing_uids_with_old_pool_pocket.csv` | `c57a073ac9dfc8ec77fd9a38c4356c83fc362a9bb9ee47e2afb1f85fad71abc0` |
| `missing_uids_without_old_pool_pocket.csv` | `b84c0e39ff33c094a6f3259612f5b77af652ff4c86222e7d3aa723c768707089` |
| 2026-08-03 strict AlphaFill 100-UID pilot archive | `89c83cc29e4b3320b2a27e2f38bece39a297e95e97ad5bae80040c08f309b4ab` |
| 2026-08-03 mixed P2Rank pilot archive | `ee522d2caccebd646210e3144e390d328a1796d92e3210c355d289b5146a7790` |
| 2026-08-03 AFDB-only P2Rank control archive | `cf689b2429b40788da77daf6fe08d66a331f432c7a4f40fd7e48f22b733ab6ea` |

## 4. Selection method audit

Selection rule:

```text
For each teacher-approved stratum:
1. intersect source UID table with final_missing_pocket_uids;
2. intersect with F3 strict missing-valid-pocket set;
3. require strict 2026 all_enzymes membership;
4. require local uid2seq sequence membership;
5. exclude any UID seen in the 2026-08-03 pilots;
6. sort by sha256(seed|stratum|uid), then UID;
7. take the target count.
```

Selection seed:

```text
20260811
```

Important F3 relationship:

```text
F3 strict missing-valid-pocket UID = 4,681.
final_missing_pocket_uids.csv = 4,453 UID.
```

The approved 35/25/40 strata are final-missing strata. Therefore the frozen 100
UIDs are selected from the 4,453 final-missing subset while still requiring
membership in the broader F3 4,681 missing-valid-pocket universe.

## 5. Result audit

Frozen subset:

| Check | Result |
|---|---:|
| sampled rows | 100 |
| unique sampled UID | 100 |
| duplicate UID | 0 |
| strict 2026 UID flag true | 100 |
| local sequence flag true | 100 |
| F3 missing-valid-pocket flag true | 100 |
| final-missing-pocket flag true | 100 |
| appeared in previous 2026-08-03 pilots | 0 |
| local ESM2-3B present | 0 |
| local ESM2-3B missing | 100 |

Stratum allocation:

| Stratum | Target | Eligible | Fresh | Selected | Deficit |
|---|---:|---:|---:|---:|---:|
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 35 | 1,578 | 1,523 | 35 | 0 |
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 25 | 726 | 701 | 25 | 0 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 40 | 3,727 | 3,652 | 40 | 0 |

Interpretation:

```text
The selected UIDs are compliant enzyme UIDs for this acceptance purpose.
They are not arbitrary enzyme picks and not live external candidates.
```

All 100 selected UIDs are missing current local ESM2-3B features. This is
acceptable for the Phase 1 acceptance purpose because the approved task includes
ESM-2 3B on-demand/cache behavior, and the manifest records that status before
execution.

## 6. Boundary / no-overclaim audit

This package does not support claiming:

```text
Phase 1 acceptance run has started;
any UID was processed by P2Rank in this step;
any AFDB structure was fetched in this step;
any staged D4 asset was generated in this step;
full 4,681 UID backfill is authorized or complete;
production D4 assets were generated or merged;
production pool was modified.
```

Allowed narrow claim:

```text
The Phase 1 >=100 UID acceptance subset has been frozen locally with
teacher-approved 35/25/40 strata and all 100 UIDs pass the local compliance
filters for strict enzyme UID, sequence availability, F3 missing-valid-pocket
membership, final-missing stratum membership, and 2026-08-03 freshness.
```

## 7. Next action

Next local task:

```text
Prepare and audit the Chenyu/HPC executor prompt for the Phase 1 acceptance run
using this frozen SAMPLED_UIDS.csv, the stable P2Rank 2.5.1 tool directory, and
the F3 reproduction package.
```

Do not run the acceptance job until the executor prompt is separately reviewed.

Final local audit status:

```text
UID_FREEZE_SCRIPT_PRESENT_PASS
UID_FREEZE_SHA256SUMS_PASS
SAMPLED_UIDS_100_UNIQUE_PASS
STRATA_35_25_40_PASS
NO_STRATUM_DEFICIT_PASS
STRICT_2026_ENZYME_UID_PASS
LOCAL_SEQUENCE_PRESENT_PASS
F3_MISSING_VALID_POCKET_MEMBER_PASS
FINAL_MISSING_STRATUM_MEMBER_PASS
FRESH_RELATIVE_TO_2026_08_03_PILOTS_PASS
NO_P2RANK_RUN_PASS
NO_UID_BACKFILL_PASS
NO_PRODUCTION_MUTATION_PASS
NEXT_STEP_HPC_ACCEPTANCE_PROMPT_DRAFT
```
