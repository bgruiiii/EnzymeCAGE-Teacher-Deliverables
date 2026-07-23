# Enzyme Tasks 1, 2, 3 And 5 Final Pre-Submission Audit

Date: 2026-07-23

## 1. Verdict

```text
FINAL_ENZYME_PRE_SUBMISSION_AUDIT_PASS
TASK1_CURRENT_BYTES_AND_EVIDENCE_PASS
TASK2_CURRENT_HOMEPAGE_AND_COUNTS_PASS
TASK3_CURRENT_REGISTRY_AND_RETENTION_PASS
TASK5_CURRENT_SHORTLIST_AND_PROPOSAL_PASS
ROOT_DISCOVERABILITY_PASS
HISTORICAL_COMMITS_PRESERVED_PASS
TEACHER_ACCEPTANCE_NOT_YET_CLAIMED
```

## 2. Authority And Scope

The final check used:

```text
TEACHER_REPLY_M3_P1_UNLOCK_CASE1_REBOUND_AND_METATRAITS_M4A_ADJUDICATION_2026-07-21.md
SHA256 57699b8a92ba6b555c96c0216c3961af0e80299d150b21979cb4fa7a19a18d57
```

It also applied the 2026-07-22 teacher clarification that RHEA:11880 may
naturally contribute candidates in fair Top-K retrieval but must not supply
the RHEA:46976 query identity, EC identity or known-positive identity.

The four individual audit files were produced sequentially. Any old
task-progress sentence inside an earlier audit, such as "Task 1 blocked" or
"Task 2 not started", records the state at that audit's creation time. It is
superseded by this final audit and does not reopen a resolved question.

## 3. Fresh Task 1–3 Recalculation

All four case JSON files and the registry parsed as strict JSON.

Fresh array-length and set-intersection results:

| Case | B pool / known-positive intersection | C pool / known-positive intersection |
|---|---:|---:|
| RHEA:46976 | 0 / 0 | 15 / 2 |
| RHEA:11532 | 10 / 3 | 17 / 3 |
| RHEA:24292 | 0 / 0 | 79 / 0 |

No within-pool duplicate was found, and every B/C pool remains within the
teacher's `<=100` gate.

Task 1 exact checks:

```text
rhea_master_id = 46976
ec = JSON null
route_used = C-fallback
known_positive_uids = Q93NH4, A0A075BSX9
known-positive evidence keys = known-positive UID keys
historical-rank keys = known-positive UID keys
```

Fresh UniProt retrieval on 2026-07-23 reproduced the JSON identities:

| UID | Entry type/version | Direct exact activity | Text SHA256 | JSON SHA256 |
|---|---|---|---|---|
| Q93NH4 | reviewed / 125 | RHEA:46976 and physiological RHEA:46977 | `59e1b1060bc50b7141ffcd5c380fe87e28d041bf82319f40c6ca50ce809a189c` | `be56367c8b5f3aea5d8dd0d2e204abb36cb02648b68bee09d0763deb59415b41` |
| A0A075BSX9 | reviewed / 58 | RHEA:46976 and physiological RHEA:46977 | `7d930cfe0daaa1cf8d7cd6e92a9785af997f97798b50e8486e5f579522199a26` | `2c1359d6f4b388a4753d960aa57d9c9e3bd50ae32ad868b5a338b15b535337a8` |

Both per-UID evidence blocks satisfy teacher levels `a` and `b`. Their
RHEA:11880 provenance permits natural candidate contribution and forbids
manual exclusion, while explicitly setting query/EC identity use and
known-positive identity use to false.

Task 2 exact three-line comparison passed once for each required line.
Negative scans found no active-homepage occurrence of `抗生素降解`,
`最小 pipeline`, `pool=1` or `pool = 1`.

Task 3 registry checks passed:

```text
active_case_count = 3
RHEA:40543 absent from active_cases
deprecated = true
reason = business_direction_mismatch
superseded_by = RHEA:46976
old evidence retention = RETAIN_DO_NOT_DELETE
```

Every registry file hash matches the current root file bytes.

## 4. Fresh Task 5 Recalculation

The current shortlist has:

```text
status = SHORTLIST_ONLY_PENDING_TEACHER_ADJUDICATION
retained candidates = 2
materially excluded candidates = 1
```

Using frozen query-excluded assets and RDKit 2026.03.3, the accepted original
similarity implementation was rerun without model inference:

| Candidate | B | C | Top-10 nearest Rhea masters |
|---|---:|---:|---|
| Paraoxon RHEA:18053 | 0 | 13 | 21664, 12568, 58888, 47384, 22916, 58884, 28166, 80199, 58824, 15141 |
| Carbaryl RHEA:62380 | 0 | 72 | 83911, 72823, 84023, 10432, 75351, 21768, 72827, 42620, 21372, 33915 |

The rerun independently matched the individual Task 5 audit. Frozen
RHEA:62380 remains EC-null; external EC 3.5.1.137 was not injected into Route
B.

The final shortlist contains all six teacher decision requests and the staged
proposal:

```text
Paraoxon remains priority 1
Stage A = targeted D4 constructability only, no pool/recall/model claim
Stage B = teacher-pinned objective complete pool and full D4 expansion
Stage C = model call only after independent fair-pool audit
EC-null external evidence remains separate from frozen Rhea
agent-assisted discovery remains a source-discovery pilot with unknown
model reliability and mandatory reproducibility/human adjudication
```

Nitrobenzene remains materially excluded because the target molecule occurs
in 52 formal training rows.

## 5. Root Delivery Identities

| File | SHA256 |
|---|---|
| `case_1_rhea_46976.json` | `916ce5eaec767a46e7f9f8512f727deafbe79e13ae6dce3725cfbc8e95144e2d` |
| `case_1_rhea_40543.json` | `8596a089ac4f3a4fc6164079fb359ddfdde9fd25a45e903fe8bdf9e3ed67b8e2` |
| `case_2_rhea_11532.json` | `cdaf710c1838e976fab284a6275e3b4d57bcee6e6be0f86bd03a474c3314196b` |
| `case_3_rhea_24292.json` | `3fb4c772abe397a98bfbb34255bb55798d85215105b765912bde80b7a01ef30d` |
| `M3_CASE_REGISTRY.json` | `6aece13eb798db2e9b6025bbddf4b4e64ffe573bd836234a1a112a4ec23176b4` |
| `THREE_CASE_HOMEPAGE.md` | `21c337c91808d32774c03edb137e5a01f455af6f2f96a68fe85cc0bb900a152d` |
| `M3_EXT_CANDIDATE_SHORTLIST_v0.md` | `cebe6756ecbf1d98d67b1c16b789d7ad6324784d3f8578747a9dbe5d42657447` |

The repository root README links every current teacher-facing file on its
first screen. No historical folder or commit was deleted, rebased or
overwritten.

## 6. Forbidden-Action Check

```text
D4/Rhea/Route-B/Route-C asset mutation       not performed
Case 1/2/3 runtime inference                  not performed
wrapper/checkpoint/GPU/Chenyu call            not performed
fourth active case                            not created
Task 5 official-case promotion                not claimed
teacher acceptance                            not claimed
```

