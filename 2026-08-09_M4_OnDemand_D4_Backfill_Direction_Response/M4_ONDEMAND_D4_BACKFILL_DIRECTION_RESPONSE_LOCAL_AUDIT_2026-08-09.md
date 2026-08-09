# Local audit: M4 OnDemand D4 final combined direction response draft

Date: 2026-08-09

Audited draft:

```text
01_Path_Contract_Objective/
M4_OnDemand_D4_Backfill_Contract_Direction_Response_2026-08-09/
M4_ONDEMAND_D4_BACKFILL_DIRECTION_RESPONSE_FINAL_COMBINED_DRAFT_2026-08-09.md
```

Authority source:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_AUDIT_AUTHORIZATION_NEXT_STEPS_2026-08-07.md
```

## 1. Verdict

Verdict:

```text
FINAL_COMBINED_DIRECTION_RESPONSE_LOCAL_DRAFT_PASS
```

The draft is acceptable as the teacher-facing M4 direction-response file for the
2026-08-09 package. This package contains the direction response and local audit
only; it does not contain implementation output or staged D4 assets.

## 2. Upload/location audit

Teacher 2026-08-07 explicitly said:

```text
S1/S2 fixes: push 至原交付包位置 and update DELIVERABLE_SHA256SUMS.txt.
```

For M4, the teacher requested a direction response with:

```text
1) toolization design;
2) workload/timeline estimate;
3) Phase 1 acceptance UID subset policy.
```

No explicit M4 GitHub upload directory, dated package name, or push location was
specified in the teacher reply.

The user explicitly authorized upload after local completion. Therefore the
package uses the existing teacher-deliverables convention of a date-stamped
dedicated folder:

```text
2026-08-09_M4_OnDemand_D4_Backfill_Direction_Response/
```

This is not an interpretation that the teacher specified this exact folder.

## 3. Source drafts incorporated

The combined draft is based on the three audited local preparation steps:

```text
M4_ONDEMAND_D4_BACKFILL_DIRECTION_RESPONSE_STEP1_BOUNDARY_AND_EVIDENCE_BASE_2026-08-09.md
M4_ONDEMAND_D4_BACKFILL_DIRECTION_RESPONSE_STEP2_PHASE1_TOOLIZATION_DESIGN_2026-08-09.md
M4_ONDEMAND_D4_BACKFILL_DIRECTION_RESPONSE_STEP3_WORKLOAD_TIMELINE_ACCEPTANCE_SUBSET_PHASE2_NOTE_2026-08-09.md
```

and their local audits.

## 4. Teacher-facing path audit

The combined draft avoids local-only evidence paths. This is intentional because
the teacher cannot see local filesystem paths unless they are later packaged
into a GitHub-visible directory or tar-internal path.

The draft does include generic output filenames expected in a future package,
for example:

```text
SAMPLED_UIDS.csv
PER_UID_STATUS_TABLE.csv
MANIFEST.sha256
per_uid/<UID>/*
```

Those are described as future package contents, not as currently uploaded files.

## 5. Red-line audit

| Check | Result |
|---|---|
| Claims M4 is formally approved | PASS: draft explicitly says direction response and asks for裁定 |
| Claims implementation has started | PASS: explicitly says not started / after authorization |
| Claims all 4,681 UIDs processed | PASS: explicitly says not processed and separates later milestone |
| Claims production D4 merge is allowed | PASS: explicitly requires later teacher authorization |
| Equates P2Rank with AlphaFill pocket | PASS: repeatedly labels P2Rank as lower-evidence predicted-pocket |
| Relabels P2Rank PASS as `PASS_FULL_D4_LOADER` | PASS: explicitly forbids |
| Presents 45/100 as guaranteed full success rate | PASS: calls pilot timing/coverage non-linear and not guaranteed |
| Writes fastest 1-2 days unconditionally | PASS: tied to Chenyu dependencies already usable and minimal wrapper |
| Confuses Chenyu with 340 host | PASS: says 340 is not Chenyu/HPC |
| Claims 340-host GVP assets are found | PASS: says may exist and must be checked/audited |
| Uses ESM-C 600M as substitute for ESM-2 3B | PASS: explicitly forbidden |
| Claims upload location was teacher-specified | PASS: explicitly says teacher did not specify exact M4 folder |
| Uses local-only teacher-visible paths | PASS: none found in combined draft |

## 6. Numeric audit

Numbers in the combined draft match prior local evidence:

| Item | Value |
|---|---:|
| strict AlphaFill 100 UID PASS | 16 / 100 |
| mixed-structure P2Rank PASS | 42 / 100 |
| AFDB-only P2Rank PASS | 45 / 100 |
| mixed P2Rank strict-failure rescue | 26 / 100 |
| AFDB-only strict-failure rescue | 29 / 100 |
| strict all-UID mean wall | 14.37 sec/UID |
| mixed P2Rank all-UID mean wall | 7.78 sec/UID |
| AFDB-only all-UID mean wall | 13.76 sec/UID |
| strict missing valid pocket count | 4,681 |
| strict ESM2-3B missing count | 88,038 |
| acceptance stratum allocation | 35 / 25 / 40 |

## 7. What this combined draft did not do

This package did not:

```text
select actual acceptance UIDs;
run Chenyu/HPC;
probe current P2Rank/Java paths;
inspect the 340 host;
generate new staged assets;
```

## 8. Final local audit status

```text
UPLOAD_LOCATION_BOUNDARY_PASS
USER_AUTHORIZED_DATE_STAMPED_PACKAGE_PASS
NO_LOCAL_PATH_FOR_TEACHER_PASS
NO_M4_AUTHORIZATION_OVERCLAIM_PASS
P2RANK_LOWER_EVIDENCE_TIER_PASS
WORKLOAD_TWO_TIER_ESTIMATE_PASS
ACCEPTANCE_SUBSET_POLICY_PASS
CHENYU_340_DISTINCTION_PASS
ESMC600M_NOT_SUBSTITUTE_PASS
READY_FOR_USER_REVIEW_BEFORE_ANY_UPLOAD
```
