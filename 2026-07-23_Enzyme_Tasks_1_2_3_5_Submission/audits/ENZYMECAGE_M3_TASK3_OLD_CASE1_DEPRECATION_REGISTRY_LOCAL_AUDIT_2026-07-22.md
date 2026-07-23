# EnzymeCAGE M3 Task 3 Old Case 1 Deprecation Registry Local Audit

Date: 2026-07-22

Task scope: latest teacher reply Section 3.4 and Section 6.2.1 item 3 only.

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_P1_UNLOCK_CASE1_REBOUND_AND_METATRAITS_M4A_ADJUDICATION_2026-07-21.md
SHA256 57699b8a92ba6b555c96c0216c3961af0e80299d150b21979cb4fa7a19a18d57
```

## 1. Objective And Boundaries

Objective:

```text
Record old Case 1 RHEA:40543 as deprecated with the exact teacher-required
reason and replacement identity while retaining its configuration and evidence.
```

Allowed review target:

```text
19_M3_Frozen_Case_Configs_2026-07-21/M3_CASE_REGISTRY.json
19_M3_Frozen_Case_Configs_2026-07-21/case_1_rhea_40543.json
the old case's already referenced A1A, B1 and Rhea 140 evidence
```

Forbidden in this task:

```text
finalize or accept the new RHEA:46976 Case 1 JSON
resolve the RHEA:11880 candidate-source question
update or accept the three-case README
modify Case 1, Case 2 or Case 3 JSON bytes
start any later M3, M3-EXT, MetaTraits, M4 or Chenyu task
```

## 2. Verdict

```text
TASK3_LOCAL_AUDIT_PASS
OLD_CASE1_DEPRECATED_TRUE_PASS
DEPRECATION_REASON_EXACT_PASS
SUPERSEDED_BY_RHEA46976_PASS
OLD_CASE1_BYTES_RETAINED_PASS
OLD_CASE1_REFERENCED_EVIDENCE_RETAINED_PASS
NO_REGISTRY_REWRITE_REQUIRED
REGISTRY_FIELDS_OUTSIDE_TASK3_NOT_ACCEPTED_BY_THIS_AUDIT
```

The exact Task 3 record already existed in the local registry draft. Rewriting
the file would add no evidence, so this task performed a read-only audit and
created only this independent audit report.

This verdict accepts only the old-case deprecation record. It does not accept
the registry's new-Case-1 fields, the RHEA:46976 configuration, its candidate
pool, or the updated README. Those belong to separate tasks and remain subject
to the pending RHEA:11880 clarification.

## 3. Teacher Requirement-To-Evidence Check

| Teacher requirement | Observed evidence | Result |
|---|---|---|
| mark old RHEA:40543 deprecated | `deprecated: true` | PASS |
| use exact reason | `reason: business_direction_mismatch` | PASS |
| identify replacement | `superseded_by: RHEA:46976` | PASS |
| do not physically delete old evidence | old JSON exists and all referenced A1A/B1/Rhea 140 files exist | PASS |
| retain audit trace | old JSON SHA256 matches the registry and its previously accepted identity | PASS |
| old case must not remain active | RHEA:40543 is absent from `active_cases` | PASS |

## 4. Audited Identities

Registry inspected:

```text
M3_CASE_REGISTRY.json
SHA256 e355dfe2c7cae224760d5d35f9a79a3568c0ab8f7c99e035d80ca00fff9a4b4d
```

Retained old Case 1:

```text
case_1_rhea_40543.json
SHA256 8596a089ac4f3a4fc6164079fb359ddfdde9fd25a45e903fe8bdf9e3ed67b8e2
rhea_master_id 40543
ec 1.14.15.33
known positive O87605
```

The old JSON SHA256 is unchanged from its earlier locally accepted identity.
All four Rhea 140 source files and every A1A/B1 file referenced by that JSON
were found and independently matched their recorded SHA256 values.

## 5. Isolation Check

The following task-external files were not edited during Task 3:

```text
README.md
case_1_rhea_40543.json
case_1_rhea_46976.json
case_2_rhea_11532.json
case_3_rhea_24292.json
```

No code, model, wrapper, candidate pool, GPU job, API query, MetaTraits source
or teacher-facing consolidated report was created or changed by this task.

## 6. Task State

```text
Task 1: BLOCKED pending teacher clarification on RHEA:11880 versus C=15/2
Task 2: NOT STARTED as a separately accepted task
Task 3: LOCALLY AUDITED PASS
Task 4 and later: NOT STARTED in the one-task-at-a-time workflow
```

Task 3 is ready to be included in the final consolidated teacher delivery only
after the remaining tasks are handled one at a time. It is not being submitted
or reported as teacher accepted now.

