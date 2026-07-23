# M3 RHEA:11880 Clarification Original-Byte Resubmission Audit

Date: 2026-07-24

## 1. Verdict

```text
RHEA11880_CLARIFICATION_ORIGINAL_BYTE_RETURN_PASS
EXACT_REQUIRED_FILENAME_PASS
EXACT_REQUIRED_SHA256_PASS
SOURCE_TO_DELIVERY_CMP_PASS
CASE1_PROVENANCE_FILENAME_MATCH_PASS
CASE1_PROVENANCE_SHA256_MATCH_PASS
AUTHORITY_TEXT_UNCHANGED_PASS
TASK1_ACCEPTANCE_UNCHANGED_PASS
NO_RETRIEVAL_OR_MODEL_RERUN_PASS
```

## 2. Teacher Requirement

The 2026-07-23 acceptance document and its 2026-07-24 supplement require:

```text
return the original 2026-07-22 clarification
required SHA256 =
80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0
purpose = replace the teacher-side reconstruction and align audit bytes
effect on Task 1 PASS = none
channel = GitHub teacher-deliverables
```

## 3. Original And Returned Identities

Original local path:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
```

Returned root path:

```text
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
```

Observed identities:

| Check | Original | Returned | Result |
|---|---:|---:|---|
| bytes | 1,652 | 1,652 | PASS |
| physical lines | 9 | 9 | PASS |
| SHA256 | `80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0` | same | PASS |
| direct byte comparison | — | `cmp` exit 0 | PASS |

No Markdown normalization, whitespace cleanup, line wrapping or newline
conversion was applied to the returned authority file.

## 4. Case 1 Provenance Cross-Check

Strict parsing of the already accepted root `case_1_rhea_46976.json` gives:

```text
teacher_clarification.file =
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md

teacher_clarification.sha256 =
80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0
```

The basename equals the returned root filename, and the recorded SHA256 equals
the returned file hash.

The existing Case 1 JSON identity remains:

```text
SHA256 916ce5eaec767a46e7f9f8512f727deafbe79e13ae6dce3725cfbc8e95144e2d
```

It was inspected read-only and not changed by this task.

## 5. Authority Semantics Retained

The returned original preserves all material boundaries:

```text
RHEA:11880 may naturally contribute candidates in fair Top-K retrieval
manual exclusion would contaminate Route-C fairness
RHEA:46976 remains ec=null
RHEA:11880 is not an equivalent RHEA:46976 query
RHEA:11880 does not automatically establish RHEA:46976 known positives
each retained known-positive UID requires evidence level a, b or c disclosure
c-only evidence cannot remain a strict known positive
```

This audit verifies preservation of the authority bytes. It does not
reinterpret or modify the ruling.

## 6. Forbidden-Action Check

```text
authority reconstruction or editing                   not performed
case JSON modification                                not performed
candidate-pool or known-positive mutation             not performed
retrieval, wrapper, model, GPU or Chenyu execution    not performed
Task 1 re-adjudication                                not claimed
```
