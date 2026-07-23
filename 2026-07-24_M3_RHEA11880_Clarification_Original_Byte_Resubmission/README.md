# M3 RHEA:11880 Clarification Original-Byte Resubmission

Date of resubmission: 2026-07-24

Original authority date: 2026-07-22

Status:

```text
ORIGINAL_AUTHORITY_BYTE_RETURN_COMPLETE
NOT_RECONSTRUCTED
NOT_EDITED
NOT_REFORMATTED
```

## 1. Teacher Entry Point

The original file is placed directly in the repository root:

```text
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
```

Required and observed identity:

```text
bytes  1652
lines  9
SHA256 80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0
```

The file has nine physical lines because the complete ruling is one long final
paragraph. It is not truncated.

## 2. Why This File Is Returned

The 2026-07-23 teacher acceptance document states that the teacher-side
workspace contained a reconstructed copy whose bytes did not equal
`80a3be0c…`. It asks the student to return the original so that the teacher can
replace the reconstruction and align both sides of the audit chain.

The 2026-07-24 supplement repeats this as a P0 hard requirement and states that
the repair does not affect the existing Task 1 PASS decision.

This return satisfies only that byte-alignment requirement.

## 3. Original Student-Side Source

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
```

The root GitHub file was copied directly from this source. Direct `cmp`
comparison and SHA256 verification are recorded in the audit.

## 4. Existing Case 1 Reference

The already accepted root file `case_1_rhea_46976.json` contains:

```json
{
  "file": "00_Authority_Teacher_Plan/TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md",
  "sha256": "80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0"
}
```

Thus the returned filename and hash exactly match the provenance identity
already frozen in Case 1.

## 5. Audit Files

Current return audit:

```text
audits/
M3_RHEA11880_CLARIFICATION_ORIGINAL_BYTE_RESUBMISSION_AUDIT_2026-07-24.md
```

Delivery identity list:

```text
DELIVERABLE_SHA256SUMS.txt
```

## 6. Boundary

This task:

```text
does not change the authority text
does not change case_1_rhea_46976.json
does not change any candidate pool or known-positive identity
does not rerun retrieval, wrapper inference or a three-case workflow
does not alter the already accepted Task 1 conclusion
```

The teacher can use the root file bytes to replace the reconstructed
teacher-side copy.
