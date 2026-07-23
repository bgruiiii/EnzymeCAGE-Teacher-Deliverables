# EnzymeCAGE M3 Task 5 M3-EXT Candidate Shortlist Local Audit

Date: 2026-07-22

Last revised: 2026-07-23 (EC-null, staged-D4 and agent-assisted discovery
proposal audit)

Task scope: teacher reply Section 4, candidate-screening phase only.

## 1. Authority And Audited Deliverable

Latest authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_P1_UNLOCK_CASE1_REBOUND_AND_METATRAITS_M4A_ADJUDICATION_2026-07-21.md
SHA256 57699b8a92ba6b555c96c0216c3961af0e80299d150b21979cb4fa7a19a18d57
```

Audited Task 5 deliverable:

```text
M3_EXT_CANDIDATE_SHORTLIST_v0.md
lines 452
SHA256 cebe6756ecbf1d98d67b1c16b789d7ad6324784d3f8578747a9dbe5d42657447
status SHORTLIST_ONLY_PENDING_TEACHER_ADJUDICATION
retained candidate count 2
materially excluded candidate count 1
```

The two GPT-generated evidence documents under `00_Authority_Teacher_Plan`
were treated as untrusted source leads, not teacher authority. Every adopted
claim was checked against frozen local sources, UniProt or original
literature.

## 2. Verdict

```text
TASK5_LOCAL_AUDIT_PASS
TEACHER_REQUIRED_MINIMUM_FIELDS_PASS
PARAOXON_RETAIN_PASS
CARBARYL_RETAIN_WITH_UNREVIEWED_UID_DISCLOSURE_PASS
NITROBENZENE_MOLECULE_LEAK_EXCLUSION_PASS
B_C_READ_ONLY_RECOMPUTATION_PASS
TRAIN_VALID_TEST_EXCLUSION_CHECK_PASS
D4_ABSENCE_DISCLOSURE_PASS
EC_NULL_MINIMUM_EVIDENCE_CHAIN_PASS
STAGED_D4_AND_FAIR_FULL_POOL_PROPOSAL_PASS
AGENT_ASSISTED_DISCOVERY_PROPOSAL_BOUNDARY_PASS
NO_MODEL_NO_GPU_NO_ASSET_COMPLETION_PASS
CURRENT_THREE_CASES_UNCHANGED_PASS
SHORTLIST_ONLY_NOT_SYSTEM_VALIDATION_PASS
TASK6_NOT_STARTED_PASS
```

Task 5 is locally complete. The result is a screening shortlist for teacher
adjudication, not an official-case freeze and not permission to complete
assets or run EnzymeCAGE.

## 3. Source Identity

Frozen Rhea 140 sources:

| Source | SHA256 |
|---|---|
| `rhea-reactions.txt.gz` | `e5b470ee1a2c3781d37776dcf567a1d998ca69db73d37162d25945c02efaa852` |
| `rhea-directions.tsv` | `a10e61027681de822fd2ad91d0c2a7b66c92a55ee770974c1816b4c335ef771b` |
| `rhea2ec.tsv` | `5a90d95d4aab686b4a0c46db6495b89c6431696f4bb351a5a63e4c84a3187d44` |
| `rhea-reaction-smiles.tsv` | `34f7fb5eff7d230c2d0243b2a669b236b075a35ffda76ebe0137b0f5dd374e02` |
| `rhea2uniprot_sprot.tsv` | `89efa346087108e8b0abbeb3d8739a15d1979951bcfa9b42fa01d8786c5d827e` |

Frozen formal split files:

| Split | SHA256 |
|---|---|
| train | `99edc55621eff856464963e60e9fb94b94d5b23f356fe944653d482cde73c155` |
| valid | `d22e8663d0132c7e3088ac44340b366120db826511fa213e04d8a6552b7ca010` |
| test | `541eb88a345a7c8c772713abfa745cf9c89c37ebc3a289e7c8a0cf2461c883b8` |

Frozen candidate-pool assets and method:

| Input | SHA256 |
|---|---|
| query-excluded Route-B EC-to-UID export | `0b1063941d120ee27faa426e8fc8dbe767f68ccd1f614dd965e57b2fefd9f2c2` |
| 4,051-reference Route-C reaction index | `d57d326ffdc9d738e65d9d5400a76c470f1aa4dd7598ad7f64676e330ec7bba9` |
| frozen D4 availability export | `28a1f88165c47e80d1774c9f6fe6a259c1e1a59b70ac343bdd4baf8b8f19e829` |
| accepted M3-P0B B/C benchmark script | `c0d7a88e7e17028bd8e6594b525e81e0532160632af1c4c44f13364c1fb8a968` |

RDKit `2026.03.3` was loaded from the temporary
`/tmp/m3ext_rdkit_2026033_site` installation. It was not installed into or
written under the project repository.

## 4. Requirement-To-Field Audit

| Teacher-required field | Paraoxon | Carbaryl | Result |
|---|---|---|---|
| Rhea ID and direction | 18053 / 18054 | 62380 / 62381 | PASS |
| EC | frozen Rhea 3.1.8.1 | frozen Rhea `null`; external 3.5.1.137 segregated | PASS |
| exact Rhea 140 SMILES | present | present | PASS |
| pollutant category | organophosphate insecticide detoxification | N-methylcarbamate insecticide degradation | PASS |
| candidate basis | reviewed P0A434 direct activity; Q97VT7 low auxiliary activity | Q8RR61 and Q8GRB9 experimental papers; both unreviewed | PASS |
| B/C preliminary size | 0 / 13 | 0 / 72 | PASS |
| train/test overlap evidence | stricter train/valid/test table present | stricter train/valid/test table present | PASS |
| query UID / EC / molecule exclusions | all zero | all zero | PASS |
| asset-state boundary | evidence UIDs absent from D4; staged proposal only | evidence UIDs absent from D4; staged proposal only | PASS |

The document does not present C pool size as rank, recall or model quality. It
does not claim that the current C pools contain the evidence UIDs.

## 5. Independent B/C Recalculation

The accepted M3-P0B similarity implementation was imported byte-for-byte. The
calculation loaded the frozen query-excluded Route-C index and Route-B mapping
and read the query SMILES directly from frozen Rhea 140 rather than copying a
hand-transcribed string.

Method:

```text
Route B = exact frozen Rhea complete EC -> query-excluded formal Label=1 EC-to-UID -> D4
Route C = Morgan radius 8 / Tanimoto / greedy molecule matching /
          max(same, reverse) / Top-K=10 / UID union
model calls = 0
network calls = 0
GPU calls = 0
```

Observed rerun:

| Candidate | B pool | C pool | C top-10 nearest master IDs in rank order |
|---|---:|---:|---|
| paraoxon RHEA:18053 | 0 | 13 | 21664, 12568, 58888, 47384, 22916, 58884, 28166, 80199, 58824, 15141 |
| carbaryl RHEA:62380 | 0 | 72 | 83911, 72823, 84023, 10432, 75351, 21768, 72827, 42620, 21372, 33915 |

Carbaryl B is zero because frozen Rhea 140 has no EC for RHEA:62380. The
external IUBMB/BRENDA EC 3.5.1.137 was not injected into frozen Route B.

## 6. Independent Leakage Audit

The audit resolved every formal-row Rhea ID through frozen
`rhea-directions.tsv`, compared exact forward and reverse reaction strings,
checked every evidence UID and EC, and canonicalized individual molecules with
RDKit before target-pollutant comparison. The last operation prevents aromatic
case or alternative valid SMILES spelling from hiding a molecule overlap.

### 6.1 Retained candidates

| Candidate and check | train | valid | test | Result |
|---|---:|---:|---:|---|
| paraoxon master 18053 | 0 | 0 | 0 | PASS |
| paraoxon exact/reverse reaction | 0 | 0 | 0 | PASS |
| canonical paraoxon molecule | 0 | 0 | 0 | PASS |
| P0A434/P0A433/Q97VT7 | 0 | 0 | 0 | PASS |
| EC 3.1.8.1 | 0 | 0 | 0 | PASS |
| carbaryl master 62380 | 0 | 0 | 0 | PASS |
| carbaryl exact/reverse reaction | 0 | 0 | 0 | PASS |
| canonical carbaryl molecule | 0 | 0 | 0 | PASS |
| Q8GRB9/Q8RR61 | 0 | 0 | 0 | PASS |
| external EC 3.5.1.137 | 0 | 0 | 0 | PASS |

### 6.2 Nitrobenzene correction and exclusion

The initial preliminary note had incorrectly treated nitrobenzene molecule
overlap as zero. That result came from an insufficient exact-string view. The
strict RDKit-canonicalized check found:

```text
canonical target molecule: O=[N+]([O-])c1ccccc1
train molecule rows: 52
valid molecule rows: 0
test molecule rows: 0
all 52 train rows resolve to master RHEA:52884
```

RHEA:52884 is the already trained nitrobenzene nitroreductase reaction. Thus
the distinct RHEA:46508 dioxygenase chemistry still shares the target query
molecule with formal training data and fails the teacher's molecule exclusion
gate. The final shortlist correctly removes it.

The exclusion is independently strengthened by the system contract mismatch:
P95561, Q8RTL5, Q8RTL4 and Q8RTL3 are four complementary NBDO components; no
one UID performs the complete NADH-dependent RHEA:46509 reaction.

## 7. External Evidence Audit And Corrections

### 7.1 Paraoxon

```text
P0A434: direct purified-enzyme paraoxon evidence; reviewed
Q97VT7: direct but low promiscuous paraoxonase activity; reviewed auxiliary evidence
P0A433: paraoxon annotation By similarity; not a UID-specific direct positive
Rhea-to-evidence-UID direct cross-reference: absent
complete mineralization or real-water occurrence claim: not made
```

### 7.2 Carbaryl

The GPT evidence document incorrectly reported that Q8GRB9 could not be
identified. Official UniProt and PMID 16781470 establish Q8GRB9 as submitted
CahA from *Arthrobacter* sp. RC100, with cloning, overexpression and purified
enzyme evidence. The shortlist restores it and labels it unreviewed.

Q8RR61 is also unreviewed, but PMID 11872471 directly connects purified CehA,
the cloned gene and carbaryl hydrolysis to 1-naphthol and methylamine. CO2 is
kept as part of the curated net reaction after spontaneous decomposition of
the unstable N-methylcarbamate; it is not described as a separately measured
paper product.

Frozen Rhea EC `null`, external EC 3.5.1.137 and the absence of a frozen
Rhea-to-UID mapping are all separately disclosed.

## 8. EC-Null And Staged-D4 Proposal Audit

### 8.1 Minimum carbaryl EC chain

Read-only checks on 2026-07-23 confirmed every boundary used in shortlist
Section 6.1:

```text
frozen Rhea 140 RHEA:62380 definition present                  PASS
frozen Rhea 140 RHEA:62380 EC row absent                      PASS
current Rhea RHEA:62380 EC row still absent                   PASS
IUBMB/ExPASy EC 3.5.1.137 accepted name N-methylcarbamate
  hydrolase, alternative name carbaryl hydrolase and carbaryl
  substrate-scope statement present                           PASS
current Rhea EC 3.5.1.137 mappings are generic RHEA:74171
  and carbofuran RHEA:74191, not exact RHEA:62380              PASS
BRENDA EC 3.5.1.137 sequence result includes Q8RR61            PASS
Q8RR61 direct carbaryl paper PMID 11872471                     PASS
Q8GRB9 direct carbaryl paper PMID 16781470                     PASS
Q8GRB9 current official UID-level EC absent                    PASS
```

Accordingly, `external_ec_candidate=3.5.1.137` is a defensible proposal field,
while frozen `rhea_ec` must remain `null`. The shortlist asks for teacher
adjudication rather than silently promoting the external class assignment.

External response identities used only for this proposal:

| Read-only source | Observed identity |
|---|---|
| UniProt `ec:3.1.8.1` TSV | 250 rows: 15 reviewed, 235 unreviewed; SHA256 `3091688bf9c1e360565bae36bead6551d7b6ab4d18befe477d022d5088e18c90` |
| SIB ENZYME/ExPASy EC 3.5.1.137 HTML | SHA256 `7c880ad6b7f28219d1de5ccfcb3fc122447f28450765e37cfd82fcec2aaf9dd5` |
| BRENDA EC 3.5.1.137 sequence-search HTML | SHA256 `5987d5c036c9e4a3049272efc19b335e519f8dd40d235d6c208be1c7603d971c` |
| current Rhea `rhea2ec.tsv` | SHA256 `2b449ac148ab155880fd0c751ba5a76b0448f05e42a5079e1877392304a7055a` |

These files were downloaded only under `/tmp`; no live source replaced a
pinned project input.

### 8.2 Pool-size and D4 feasibility checks

The UniProt EC 3.1.8.1 set contains P0A434, Q97VT7 and P0A433 as reviewed
entries. Intersection with the frozen D4 export found:

```text
UniProt EC 3.1.8.1 UIDs                         250
reviewed / unreviewed                           15 / 235
UIDs with current complete D4                    1
additional D4 required for all-250 contract    249
additional D4 required for reviewed-only set    14
```

The current BRENDA EC 3.5.1.137 page displays seven sequence accessions; none
has a current D4 row. Q8RR61 is present in that EC sequence result. Q8GRB9 is
not, so the shortlist correctly makes its Route-B treatment a separate teacher
question rather than inferring an official UID-level EC.

### 8.3 Fairness of the staged proposal

The proposed stages are correctly separated:

```text
Stage A: teacher-authorized D4 constructability for direct evidence UIDs only;
         no pool mutation, recall claim or model run
Stage B: pin the objective external source and inclusion rule, select every
         qualifying UID, complete full-pool D4, rebuild and validate Route B
Stage C: model call only after Stage B passes independent audit
```

This prevents a targeted known-positive D4 fill from becoming manual
ground-truth injection. The shortlist also forbids manually unioning known
positives into Route C.

The first requested paraoxon feasibility pair is P0A434 and Q97VT7. P0A433 is
excluded because its exact paraoxon statement is `By similarity`. The
Q8RR61/Q8GRB9 carbaryl pair is conditional on teacher acceptance of carbaryl
and the EC-null policy.

### 8.4 Agent-assisted EC-null discovery proposal boundary

The proposed internet-enabled agent workflow is correctly limited to source
discovery and structured evidence-packet assembly. It does not treat an agent,
model agreement or a search-result snippet as an EC authority.

The proposal explicitly requires:

```text
same source hierarchy and output schema across runs                  PASS
official-database or original-paper reproducibility                  PASS
source identity, access date, evidence and non-proof boundary        PASS
different-model performance treated as unknown                      PASS
conflicting or unsupported results remain unresolved                 PASS
human/teacher adjudication before project adoption                   PASS
no automatic Rhea/UID/pool/D4/model mutation                         PASS
```

No multi-agent comparison was run and no claim is made about which model is
more reliable. The shortlist asks the teacher whether to authorize a limited
pilot and which comparison design to use.

## 9. D4 And Forbidden-Action Audit

The following evidence UIDs are absent from the frozen D4 availability export:

```text
P0A434
P0A433
Q97VT7
Q8GRB9
Q8RR61
```

This is an asset-state disclosure, not authorization to fill assets. The audit
found no D4, Rhea 140, Route-B or Route-C asset writes. No current case JSON,
case registry or three-case homepage file was changed by Task 5.

Forbidden-action review:

```text
asset completion                                      not performed  PASS
Case 1/2/3 mutation                                   not performed  PASS
EnzymeCAGE wrapper/model/checkpoint call              not performed  PASS
GPU or Chenyu resource use                            not performed  PASS
claim of official case or system validation           absent         PASS
Task 6 start                                           absent         PASS
external publication or teacher submission            not performed  PASS
```

Network access was used only to read official UniProt and literature evidence.
It did not change any external state.

## 10. Final Self-Review

```text
exact teacher delivery filename present                         PASS
two retained candidates satisfy every exclusion gate            PASS
failed third candidate removed rather than caveated into pass    PASS
all required per-candidate fields present                        PASS
frozen versus external EC semantics separated                    PASS
reviewed versus unreviewed UID status separated                  PASS
direct experiment versus similarity annotation separated        PASS
B/C counts independently reproduced                              PASS
all D4 absences disclosed                                       PASS
EC-null source hierarchy and non-overwrite rule present         PASS
targeted D4 feasibility separated from fair full-pool build      PASS
explicit teacher questions cover EC bridge and pool rule         PASS
agent-assisted discovery is proposal-only with model uncertainty PASS
shortlist-only and second-adjudication boundary explicit         PASS
no unsupported completeness or validation claim                 PASS
```

## 11. Task State

```text
Task 1: LOCALLY AUDITED PASS
Task 2: LOCALLY AUDITED PASS
Task 3: LOCALLY AUDITED PASS
Task 4: LOCALLY AUDITED PASS
Task 5: LOCALLY AUDITED PASS; shortlist ready for final consolidated teacher delivery
Task 6 and later: NOT STARTED
```
