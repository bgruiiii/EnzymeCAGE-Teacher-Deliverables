# EnzymeCAGE M3 Task 2 Three-Case Homepage Role Local Audit

Date: 2026-07-22

Task scope: latest teacher Section 6.2.1 item 2 only: synchronize the frozen
three-case homepage role wording, then verify it against all three active case
JSON files and the 2026-07-22 RHEA:11880 clarification.

Authorities:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_P1_UNLOCK_CASE1_REBOUND_AND_METATRAITS_M4A_ADJUDICATION_2026-07-21.md

00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
```

## 1. Verdict

```text
TASK2_LOCAL_AUDIT_PASS
TEACHER_EXACT_THREE_LINE_ROLE_WORDING_PASS
ACTIVE_THREE_CASE_COUNT_PASS
README_JSON_POOL_AND_RECALL_COUNT_CONSISTENCY_PASS
OLD_CASE1_HOMEPAGE_WORDING_ABSENT_PASS
RHEA11880_FAIR_RETRIEVAL_BOUNDARY_PASS
RHEA11880_NO_QUERY_EC_OR_KNOWN_POSITIVE_IDENTITY_INHERITANCE_PASS
ONLY_README_FUNCTIONAL_DELIVERABLE_MODIFIED_PASS
STALE_PRE_CLARIFICATION_DRAFT_EXCLUDED_PASS
M3_TASK2_READY_FOR_FINAL_TEACHER_DELIVERY
TEACHER_ACCEPTANCE_NOT_YET_CLAIMED
```

## 2. Audited Deliverable

```text
19_M3_Frozen_Case_Configs_2026-07-21/README.md
SHA256 21c337c91808d32774c03edb137e5a01f455af6f2f96a68fe85cc0bb900a152d
```

The README is the active frozen-case homepage. It lists exactly three active
case files and explicitly states that retained old Case 1 RHEA:40543 is
deprecated evidence rather than a fourth active case.

## 3. Exact Teacher Wording

The README contains the teacher-required three lines verbatim:

```text
Case 1 (RHEA:46976, 尼古丁降解): C-fallback 成功分支演示
Case 2 (RHEA:11532, EC 1.4.3.19): B-primary 排序统计意义
Case 3 (RHEA:24292, EC 2.3.1.1): 上游召回失败 fail-closed
```

No synonym, old label or expanded performance claim replaces any of these
three lines.

## 4. Active JSON Cross-Check

All counts below were freshly computed from array membership in the three
active JSON files. A recalled count is the intersection between that route's
pool and the case's complete `known_positive_uids` array; it is not inferred
from prose.

| Case | JSON role | Route | Strict known positives | B pool / recalled | C pool / recalled | README match |
|---|---|---|---:|---:|---:|---|
| RHEA:46976 | `NICOTINE_DEGRADATION_C_FALLBACK_SUCCESS_DEMO` | C-fallback | 2 | 0 / 0 | 15 / 2 | PASS |
| RHEA:11532 | `ENZYMECAGE_RANKING_CAPABILITY_MEASUREMENT` | B-primary | 8 | 10 / 3 | 17 / 3 | PASS |
| RHEA:24292 | `UPSTREAM_RECALL_FAILURE_FAIL_CLOSED_DEMO` | C-fallback | 295 | 0 / 0 | 79 / 0 | PASS |

Freshly intersected recalled UIDs:

```text
Case 1 B: none
Case 1 C: A0A075BSX9, Q93NH4

Case 2 B: O31616, Q5L2C2, S5FMM4
Case 2 C: O31616, Q5L2C2, S5FMM4

Case 3 B: none
Case 3 C: none
```

No duplicate UID was found within any of the six B/C arrays. Every pool
remains within the teacher's `<=100` gate. The README runtime decisions follow
the frozen routing contract:

```text
Case 1: B empty -> use C -> wrapper may be called
Case 2: use B-primary -> wrapper may be called
Case 3: B empty -> inspect C -> no known positive recalled -> fail closed
        before wrapper
```

## 5. Old Case 1 Wording Negative Check

A literal and whitespace-tolerant scan of the active README found no instance
of the prohibited or obsolete homepage descriptions:

```text
抗生素降解
Case 1 = 抗生素降解
最小 pipeline
Case 1 = 最小 pipeline 验证
pool=1
pool = 1
```

The numerical text `15 / 2` in the current pool table is the frozen Case 1
C-pool/recalled count and is not the obsolete `pool=1` description.

## 6. RHEA:11880 Clarification Check

The README reflects the later 2026-07-22 clarification and therefore does not
repeat the superseded literal reading of the earlier Section 3.3 item 2.

| Clarified boundary | README state | Audit |
|---|---|---|
| RHEA:11880 may contribute candidates when naturally returned by fair Top-K similarity retrieval | stated explicitly | PASS |
| that natural contribution must not be manually removed | stated explicitly | PASS |
| RHEA:11880 is not the RHEA:46976 query or an equivalent target reaction | query identity remains RHEA:46976 | PASS |
| EC 1.5.3.5 must not be inherited by RHEA:46976 | README states Case 1 `ec: null` | PASS |
| RHEA:11880 does not automatically establish RHEA:46976 known-positive identity | stated explicitly | PASS |
| both retained strict Case 1 positives require independent direct evidence | README states reviewed UniProt RHEA:46976 plus experimental-literature evidence | PASS |

Thus the homepage preserves the fair C=15/2 retrieval outcome without using
RHEA:11880 as query identity, EC identity or known-positive identity.

## 7. Stale Draft Exclusion

The following pre-clarification teacher-facing draft still contains the now
resolved `M3-R1` question and the older provisional RHEA:11880 explanation:

```text
15_Teacher_Formal_Training_Final_Report_2026-07-13/
ENZYMECAGE_M3_CASE1_RHEA46976_REBOUND_DELIVERY_AND_EXECUTION_HANDOFF_2026-07-22.md
```

Classification for final aggregation:

```text
STALE_PRE_CLARIFICATION_DRAFT
EXCLUDE_FROM_FINAL_TEACHER_DELIVERY
DO_NOT_TREAT_M3-R1_AS_OPEN
```

The draft was deliberately not edited during Task 2. A later consolidated
teacher report must use the saved 2026-07-22 clarification and the audited
active files instead.

## 8. Change Isolation And File Identities

Only the existing README was functionally modified for Task 2. The only other
Task 2 filesystem addition is this dedicated local audit. No registry or case
JSON content was changed.

Fresh post-task identities:

```text
M3_CASE_REGISTRY.json
  6aece13eb798db2e9b6025bbddf4b4e64ffe573bd836234a1a112a4ec23176b4

case_1_rhea_40543.json
  8596a089ac4f3a4fc6164079fb359ddfdde9fd25a45e903fe8bdf9e3ed67b8e2

case_1_rhea_46976.json
  916ce5eaec767a46e7f9f8512f727deafbe79e13ae6dce3725cfbc8e95144e2d

case_2_rhea_11532.json
  cdaf710c1838e976fab284a6275e3b4d57bcee6e6be0f86bd03a474c3314196b

case_3_rhea_24292.json
  3fb4c772abe397a98bfbb34255bb55798d85215105b765912bde80b7a01ef30d
```

These values match the identities established before the Task 2 README edit.
The README changed from the Task 1 recorded identity
`45d982673474c3b48b87b50f0d0442c9f6c5c43e79fab561c0ca767ac91efeb7`
to the Task 2 identity recorded in Section 2.

No Agent code, model, wrapper, checkpoint, Chenyu job, GPU inference, API
implementation, M3-EXT screening, M4b/M4c work or external submission was run
or changed.

## 9. Final Self-Audit

```text
active README exact teacher three-line comparison                   PASS
active-file enumeration equals three                               PASS
strict parse of all three active JSON files                        PASS
B/C array lengths and known-positive intersections recomputed      PASS
README frozen-pool table equals JSON-derived counts                PASS
all six pools <= 100                                               PASS
all six pools free of within-pool UID duplicates                   PASS
obsolete active-README phrase scan                                 PASS
2026-07-22 RHEA:11880 clarification reflected                     PASS
registry and all case JSON SHA256 identities unchanged             PASS
stale pre-clarification draft excluded without editing             PASS
task-external execution or implementation                          NOT RUN
```

Final token:

```text
M3_TASK2_FINAL_SELF_AUDIT_PASS
```

Task 2 is locally complete and ready to be included in the eventual unified
teacher delivery. This audit does not claim teacher acceptance and does not
start Task 5 or any later task.
