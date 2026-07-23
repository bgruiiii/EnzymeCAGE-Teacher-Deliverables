# EnzymeCAGE M3 Task 1 RHEA:46976 Case JSON Local Audit

Date: 2026-07-22

Task scope: latest teacher Section 6.2.1 item 1 plus the 2026-07-22 explicit
RHEA:11880 fairness and per-UID evidence clarification only.

Latest authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
SHA256 80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0
```

Pre-implementation clarification audit:

```text
04_Local_Review_Audits/
ENZYMECAGE_M3_CASE1_RHEA11880_FAIRNESS_TEACHER_CLARIFICATION_LOCAL_AUDIT_2026-07-22.md
```

## 1. Verdict

```text
TASK1_LOCAL_AUDIT_PASS
RHEA46976_EXACT_QUERY_IDENTITY_PASS
EC_JSON_NULL_PASS
FAIR_TOPK_C15_MEMBERSHIP_PASS
RHEA11880_NATURAL_CONTRIBUTION_RETAINED_PASS
RHEA11880_NO_EC_QUERY_OR_KNOWN_POSITIVE_IDENTITY_INHERITANCE_PASS
Q93NH4_DIRECT_EVIDENCE_LEVEL_A_AND_B_PASS
A0A075BSX9_DIRECT_EVIDENCE_LEVEL_A_AND_B_PASS
STRICT_KNOWN_POSITIVE_UIDS_RETAINED_PASS
CASE1_JSON_READY_FOR_FINAL_TEACHER_DELIVERY
MODEL_AND_CHENYU_NOT_RUN
TEACHER_ACCEPTANCE_NOT_YET_CLAIMED
```

The new Case 1 JSON now contains the teacher-required per-UID evidence layers.
Both UIDs have direct reviewed UniProt catalytic-activity records for exact
RHEA:46976 plus experimental literature citations. They are not classified as
similarity-only evidence and may remain in `known_positive_uids`.

## 2. Audited Deliverable

```text
19_M3_Frozen_Case_Configs_2026-07-21/case_1_rhea_46976.json
SHA256 916ce5eaec767a46e7f9f8512f727deafbe79e13ae6dce3725cfbc8e95144e2d
```

Machine-readable core state:

```text
rhea_master_id = 46976
ec = null
reaction_sha256 = 9737dd8c994296811f87278e33cc7c8b1743112ddf9ecb745ba6de1e1dc2971a
difficulty_tier = STRONG_TOP_5
route_used = C-fallback
B pool = 0
C pool = 15
strict known positives = Q93NH4, A0A075BSX9
historical ranks = Q93NH4:2, A0A075BSX9:3
```

The canonical reaction SHA256 was freshly recomputed. The complete C-pool UID
list and order exactly match the accepted compressed B1 route-membership body.

## 3. Latest Teacher Requirement Matrix

| Teacher requirement | JSON implementation | Audit |
|---|---|---|
| RHEA:11880 may naturally contribute in fair Top-K retrieval | both UID evidence blocks record neighbor RHEA:11880 rank 3 and `candidate_contribution_allowed=true` | PASS |
| no manual removal of that contribution | full accepted C=15 pool retained | PASS |
| exact RHEA:46976 EC must be null | top-level `ec` is JSON null | PASS |
| RHEA:11880 is not an equivalent query | query remains master 46976 / LR 46977; provenance marks `used_as_query_or_ec_identity=false` | PASS |
| no automatic known-positive inheritance from 11880 | each UID has independent reviewed UniProt RHEA:46976 evidence; provenance marks 11880 identity evidence false | PASS |
| every UID must disclose evidence level a, b or c | both UID blocks explicitly record levels `a` and `b` | PASS |
| condition-c-only UID must be removed from strict positives | not triggered; neither UID relies only on condition c | NOT APPLICABLE |

## 4. Per-UID Evidence Audit

### 4.1 Q93NH4

Official source checked 2026-07-22:

```text
UniProtKB reviewed (Swiss-Prot), entry version 125
https://rest.uniprot.org/uniprotkb/Q93NH4.txt
text SHA256 59e1b1060bc50b7141ffcd5c380fe87e28d041bf82319f40c6ca50ce809a189c
https://rest.uniprot.org/uniprotkb/Q93NH4.json
JSON SHA256 be56367c8b5f3aea5d8dd0d2e204abb36cb02648b68bee09d0763deb59415b41
```

Direct curated reaction:

```text
(S)-6-hydroxynicotine + O2 = 6-hydroxy-N-methylmyosmine + H2O2
RHEA:46976 / physiological LR RHEA:46977
ECO:0000269
PubMed:21383134, 26744768, 28080034, 4965794
```

Result:

```text
condition (a) direct UniProt exact reaction: PASS
condition (b) direct experimental literature: PASS
strict known-positive eligibility: PASS
```

### 4.2 A0A075BSX9

Official source checked 2026-07-22:

```text
UniProtKB reviewed (Swiss-Prot), entry version 58
https://rest.uniprot.org/uniprotkb/A0A075BSX9.txt
text SHA256 7d930cfe0daaa1cf8d7cd6e92a9785af997f97798b50e8486e5f579522199a26
https://rest.uniprot.org/uniprotkb/A0A075BSX9.json
JSON SHA256 2c1359d6f4b388a4753d960aa57d9c9e3bd50ae32ad868b5a338b15b535337a8
```

Direct curated reaction:

```text
(S)-6-hydroxynicotine + O2 = 6-hydroxy-N-methylmyosmine + H2O2
RHEA:46976 / physiological LR RHEA:46977
ECO:0000269
PubMed:25002425
DOI:10.1128/AEM.01312-14
```

Result:

```text
condition (a) direct UniProt exact reaction: PASS
condition (b) direct experimental literature: PASS
strict known-positive eligibility: PASS
```

## 5. Evidence Dimensions Kept Separate

The JSON now makes three separate facts machine-readable:

```text
exact-query identity:
  RHEA:46976, ec=null

strict known-positive identity:
  direct reviewed UniProt RHEA:46976 plus experimental literature

candidate retrieval provenance:
  RHEA:11880 naturally appears at similarity-neighbor rank 3 and may
  contribute candidates, but supplies no query EC or known-positive identity
```

Although both UniProt protein records also annotate EC 1.5.3.5 for the related
overall reaction RHEA:11880, this enzyme annotation is not copied into the
top-level exact RHEA:46976 `ec` field.

## 6. Registry Identity Synchronization

The local registry contained a SHA256 identity for the active Case 1 file.
After the authorized JSON evidence update, only that one derived hash field was
mechanically changed:

```text
M3_CASE_REGISTRY.json
new SHA256 6aece13eb798db2e9b6025bbddf4b4e64ffe573bd836234a1a112a4ec23176b4
active Case 1 file SHA256 916ce5eaec767a46e7f9f8512f727deafbe79e13ae6dce3725cfbc8e95144e2d
```

The previously audited Task 3 deprecation record remains unchanged:

```text
deprecated = true
reason = business_direction_mismatch
superseded_by = RHEA:46976
old Case 1 SHA256 = 8596a089ac4f3a4fc6164079fb359ddfdde9fd25a45e903fe8bdf9e3ed67b8e2
```

## 7. Isolation And Self-Review

Fresh automated validation checked:

```text
strict JSON parse and reaction hash                              PASS
exact B1 C-pool membership/order                                PASS
known-positive/evidence/rank key equality                       PASS
both live UniProt text and JSON response SHA256 values          PASS
both UniProt entry types and versions                           PASS
exact RHEA:46976 catalytic activity in both structured records  PASS
experimental PubMed sets in both structured records             PASS
RHEA:11880 B1 neighbor rank 3                                   PASS
teacher clarification identity                                  PASS
registry active Case 1 SHA256 synchronization                   PASS
```

Unchanged task-external case files:

```text
README.md
  45d982673474c3b48b87b50f0d0442c9f6c5c43e79fab561c0ca767ac91efeb7
case_1_rhea_40543.json
  8596a089ac4f3a4fc6164079fb359ddfdde9fd25a45e903fe8bdf9e3ed67b8e2
case_2_rhea_11532.json
  cdaf710c1838e976fab284a6275e3b4d57bcee6e6be0f86bd03a474c3314196b
case_3_rhea_24292.json
  3fb4c772abe397a98bfbb34255bb55798d85215105b765912bde80b7a01ef30d
```

No Agent code, model, wrapper, checkpoint, Chenyu job, GPU inference, API
implementation, M3-EXT screening or later MetaTraits task was run or changed.

## 8. Task State

```text
Task 1: LOCALLY AUDITED PASS; ready for final teacher delivery
Task 2: NOT STARTED as a separately accepted task
Task 3: LOCALLY AUDITED PASS
Task 4: LOCALLY AUDITED PASS
Task 5 and later: NOT STARTED
```

This audit supersedes the pre-clarification Case 1 audit for the active JSON
identity. It does not submit the file externally or claim teacher acceptance.

