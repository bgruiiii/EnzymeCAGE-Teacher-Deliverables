# Local audit: M4 second-milestone E2 staged status table authorization request

Date: 2026-08-13

Audited draft:

```text
01_Path_Contract_Objective/
M4_Second_Milestone_E2_Staged_Status_Table_Plan_2026-08-13/
M4_SECOND_MILESTONE_E2_STAGED_STATUS_TABLE_AUTHORIZATION_REQUEST_2026-08-13.md
```

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_PROJECT_NEXT_STEPS_GUIDANCE_2026-08-13.md
```

## 1. Verdict

Verdict:

```text
LOCAL_AUDIT_PASS_FOR_USER_REVIEW_BEFORE_TEACHER_SUBMISSION
```

The draft covers the teacher-required M4 E2 second-milestone elements without
claiming full 4,681 execution, production D4 merge, production pool mutation,
or strict AlphaFill equivalence.

It is a teacher-facing authorization request draft, not an execution result and
not an uploaded deliverable.

## 2. Teacher requirement coverage

Teacher 2026-08-13 required the E2 plan to include:

| Requirement | Draft coverage |
|---|---|
| Observation point 1: one cache-miss UID smoke | Section 1 reports A3CST9 only, with SHA256 and bounded scope |
| full 4,681 staged status table plan | Section 2 defines denominator, route, statuses, output tables, and fields |
| no-pocket about 44% strategy | Section 3 explains Phase 1 44/100 no-pocket and blocker handling |
| 8 non-virus 404 accession-variant review plan | Section 4 gives the 7 virus / 8 non-virus split, initial read-only lookup, and systematic review method |
| workload/timeline | Section 5 gives 2-3 day and 3-5 day scenarios with evidence anchors |

## 3. Evidence basis

The draft reuses only locally audited or freshly checked evidence:

| Evidence | Status |
|---|---|
| Phase 1 acceptance | Teacher 2026-08-13 states M4 Phase 1 passed; local audit records 41/100 PASS and blocker counts |
| F3 count | local audit records `strict_uid_missing_valid_pocket=4,681` |
| A3CST9 one-UID smoke | local audit records `LOCAL_AUDIT_PASS_AS_M4_E2_ONE_UID_CACHE_MISS_STAGED_ONLY_SMOKE` |
| no-pocket meaning | Phase 1 corrected rerun records `44/100 BLOCKED_AFDB_P2RANK_NO_POCKET` |
| fetch-blocked count | Phase 1 corrected rerun records 15 fetch-blocked, with 12 HTTP 404 and 3 HTTP 000 |
| 7 virus / 8 non-virus split | 2026-08-13 UniProt read-only lookup confirmed the split |
| 8 non-virus AFDB status | 2026-08-13 AlphaFoldDB read-only API lookup returned 404 for all 8 primary UIDs |
| Q9Z1Y9 secondary accessions | UniProt lookup found inactive `Q05A70,Q9JHH1` mapped to `Q9Z1Y9`; AFDB returned 404 for primary and secondaries |

## 4. Boundary audit

No-overclaim checks:

| Check | Result |
|---|---|
| Claims full 4,681 already run | PASS: explicitly says not started |
| Claims all 4,681 are backfilled | PASS: only forbidden wording list mentions this as not allowed |
| Claims production D4 merge | PASS: explicitly says no production merge |
| Claims production pool mutation | PASS: explicitly says no production pool mutation |
| Equates P2Rank pocket with strict AlphaFill pocket | PASS: explicitly forbids equivalence |
| Claims model inference/ranking/scoring | PASS: explicitly says none performed in smoke |
| Claims all fallback candidates were tested | PASS: states only A3CST9 was attempted |
| Silently replaces accession variants | PASS: requires review table and separate teacher裁定 |
| Changes P2Rank command contract | PASS: requires same `prank predict -c alphafold` contract unless separately裁定 |

Forbidden labels:

```text
M4_PRODUCTION_D4_BACKFILL_COMPLETE
M4_ALL_4681_UIDS_BACKFILLED
PASS_FULL_D4_LOADER
```

These appear only in a "forbidden wording" section, not as claimed outcomes.

## 5. Corrections made during audit

Two wording corrections were applied before this audit was finalized:

```text
1. PASS status token changed back to the Phase 1 audited token:
   PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER

2. Runtime anchor changed from ambiguous "PASS row warm/batched" wording to:
   "45 PASS UIDs full D4 loader-valid warm/batched average about 16.34 s/UID."

3. Red-line wording changed from "未经本次裁定" to "未经老师裁定",
   because this local draft itself does not issue authorization.
```

## 6. Remaining submission steps

Before teacher submission:

```text
1. User review the draft wording.
2. If approved, place it into the correct enzyme-side teacher deliverables repo
   under a dated 2026-08-13 folder.
3. Update the teacher-visible README/index and checksum manifest as required by
   that repo's existing format.
4. Do not upload private chat-message drafts.
```

Do not start a full 4,681 Chenyu/HPC run until teacher E2 authorization is
received.
