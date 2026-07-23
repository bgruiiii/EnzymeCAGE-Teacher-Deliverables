# M3-EXT Candidate Shortlist v0

Date: 2026-07-22

Last revised: 2026-07-23 (EC-null evidence chain, staged-D4 proposal and
agent-assisted discovery question)

Status: `SHORTLIST_ONLY_PENDING_TEACHER_ADJUDICATION`

## 1. Scope And Authority

This document is the candidate-screening-only delivery authorized by Section
4.2 of:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_P1_UNLOCK_CASE1_REBOUND_AND_METATRAITS_M4A_ADJUDICATION_2026-07-21.md
SHA256 57699b8a92ba6b555c96c0216c3961af0e80299d150b21979cb4fa7a19a18d57
```

It is a targeted shortlist, not an exhaustive ranking of every pollutant
reaction in Rhea. The two retained entries passed the required preliminary
checks against the frozen formal train, valid and test splits. They have not
been promoted to official challenge cases.

This phase did not:

```text
complete or change D4, Rhea 140, route-B or route-C assets
change Case 1, Case 2 or Case 3
call the EnzymeCAGE model or wrapper
use a checkpoint, GPU or Chenyu resources
claim system validation, ranking quality or environmental effectiveness
start M3-EXT implementation, Task 6 or any later teacher task
```

## 2. Shortlist Summary

| Priority | Pollutant and reaction | Rhea master / forward | EC disclosed for this shortlist | B pool | C pool | train/valid/test exclusion result | Recommendation |
|---:|---|---|---|---:|---:|---|---|
| 1 | paraoxon hydrolysis | 18053 / 18054 | Rhea 140 `3.1.8.1` | 0 | 13 | PASS: exact master, reaction, target molecule, evidence UID and EC counts all `0/0/0` | retain; priority candidate for teacher review |
| 2 | carbaryl hydrolysis | 62380 / 62381 | Rhea 140 `null`; external IUBMB/BRENDA `3.5.1.137` | 0 | 72 | PASS: exact master, reaction, target molecule, evidence UID and external EC counts all `0/0/0` | retain; review candidate with unreviewed-UID disclosure |

`B pool` and `C pool` are preliminary candidate-pool sizes, not EnzymeCAGE
ranks and not evidence that the correct enzymes are recoverable with current
assets.

## 3. Candidate 1: Paraoxon Hydrolysis

### 3.1 Required fields

```text
pollutant category: organophosphate insecticide; hydrolytic detoxification
Rhea master: RHEA:18053
Rhea left-to-right: RHEA:18054
Rhea 140 EC: 3.1.8.1
Rhea definition: paraoxon + H2O = diethylphosphate + 4-nitrophenol + 2 H(+)
B preliminary pool size: 0
C original Top-K=10 preliminary UID-union size: 13
```

Rhea 140 forward reaction SMILES:

```text
CCOP(=O)(OCC)OC1=CC=C([N+](=O)[O-])C=C1.[H]O[H]>>CCOP(=O)([O-])OCC.O=[N+]([O-])C1=CC=C([O-])C=C1.[H+].[H+]
```

### 3.2 Candidate basis and evidence boundary

P0A434 is a reviewed UniProtKB/Swiss-Prot parathion hydrolase. Purified-enzyme
kinetic studies directly used paraoxon as substrate and support its paraoxon
hydrolysis activity:

```text
PMID 2548585; DOI 10.1021/bi00437a021
PMID 1649628; DOI 10.1021/bi00244a010
```

Q97VT7 is a reviewed auxiliary biochemical positive: purified recombinant
SsoPox showed low paraoxonase activity (PMID 15909078; DOI
10.1007/s00792-005-0445-4). Its activity is low and promiscuous, so it is not
evidence for a natural paraoxon mineralization pathway.

P0A433 is not treated as a UID-specific direct paraoxon positive. Its UniProt
paraoxon statement is explicitly `By similarity`; it remains auxiliary
provenance only.

Frozen Rhea 140 has no reviewed Rhea-to-UniProt cross-reference for
RHEA:18053. The evidence chain is therefore deliberately split: Rhea supports
the exact chemistry, while UniProt and the papers independently support the
enzyme activities. This shortlist does not claim a direct Rhea-to-P0A434 or
Rhea-to-Q97VT7 mapping.

The supported biological description is paraoxon hydrolytic inactivation. It
does not establish complete microbial assimilation or mineralization, and it
does not establish stable or widespread paraoxon detection in real wastewater,
groundwater or surface water.

### 3.3 Exclusion evidence

The target pollutant used for the molecule check was canonicalized with RDKit
to:

```text
CCOP(=O)(OCC)Oc1ccc([N+](=O)[O-])cc1
```

| Check | train | valid | test | Result |
|---|---:|---:|---:|---|
| rows resolving to Rhea master 18053 | 0 | 0 | 0 | PASS |
| exact forward or reverse reaction SMILES | 0 | 0 | 0 | PASS |
| paraoxon molecule in either reaction side | 0 | 0 | 0 | PASS |
| P0A434, P0A433 or Q97VT7 UID rows | 0 | 0 | 0 | PASS |
| exact EC 3.1.8.1 rows | 0 | 0 | 0 | PASS |

P0A434, P0A433 and Q97VT7 are absent from the frozen D4 availability export.
No asset completion was attempted. A later official-case decision would
therefore require separate teacher adjudication before any model call.

## 4. Candidate 2: Carbaryl Hydrolysis

### 4.1 Required fields

```text
pollutant category: N-methylcarbamate insecticide; initial hydrolytic degradation step
Rhea master: RHEA:62380
Rhea left-to-right: RHEA:62381
Rhea 140 EC: null
external nomenclature only: IUBMB/BRENDA EC 3.5.1.137
Rhea definition: carbaryl + H2O + H(+) = 1-naphthol + methylamine + CO2
B preliminary pool size: 0
C original Top-K=10 preliminary UID-union size: 72
```

Rhea 140 forward reaction SMILES:

```text
CNC(=O)OC1=C2C=CC=CC2=CC=C1.[H]O[H].[H+]>>OC1=CC=CC2=CC=CC=C12.C[NH3+].O=C=O
```

### 4.2 Candidate basis and evidence boundary

Q8RR61 is the unreviewed UniProtKB/TrEMBL sequence submitted for CehA from
*Rhizobium* sp. AC100. The original study purified carbaryl hydrolase, directly
reported carbaryl hydrolysis to 1-naphthol and methylamine, and connected the
N-terminal protein sequence to the cloned `cehA` gene:

```text
PMID 11872471; DOI 10.1128/AEM.68.3.1220-1227.2002
```

Q8GRB9 is the unreviewed UniProtKB/TrEMBL sequence submitted for CahA from
*Arthrobacter* sp. RC100. The original study cloned `cahA`, overexpressed it,
purified the enzyme to homogeneity and demonstrated hydrolase activity toward
N-methylcarbamate pesticides:

```text
PMID 16781470; DOI 10.1263/jbb.101.410
```

Q8RR61 provides the stronger exact product-level evidence. Both UID entries
are unreviewed and must not be described as Swiss-Prot. Frozen Rhea 140 has no
reviewed Rhea-to-UniProt mapping for RHEA:62380.

The paper directly reports 1-naphthol and methylamine. In the IUBMB net
reaction, the enzyme first releases an unstable N-methylcarbamate that
spontaneously decomposes to methylamine and CO2. CO2 is therefore retained as
part of the curated Rhea/IUBMB net equation, not claimed as a separately
measured product in the cited Q8RR61 paper.

Frozen Rhea 140 supplies no EC for RHEA:62380, so the official shortlist EC
field is `null`. EC 3.5.1.137 is disclosed separately as current external
IUBMB/BRENDA nomenclature and was not inherited into the frozen Rhea mapping.

### 4.3 Exclusion evidence

The target pollutant used for the molecule check was canonicalized with RDKit
to:

```text
CNC(=O)Oc1cccc2ccccc12
```

| Check | train | valid | test | Result |
|---|---:|---:|---:|---|
| rows resolving to Rhea master 62380 | 0 | 0 | 0 | PASS |
| exact forward or reverse reaction SMILES | 0 | 0 | 0 | PASS |
| carbaryl molecule in either reaction side | 0 | 0 | 0 | PASS |
| Q8GRB9 or Q8RR61 UID rows | 0 | 0 | 0 | PASS |
| external EC 3.5.1.137 rows | 0 | 0 | 0 | PASS |

Q8GRB9 and Q8RR61 are absent from the frozen D4 availability export. No asset
completion was attempted.

## 5. Preliminary B/C Method

The preliminary pool counts reproduce the already accepted M3-P0B method over
the frozen, query-excluded assets:

```text
Route B:
  exact Rhea master -> complete frozen Rhea 140 EC -> query-excluded formal
  Label=1 EC-to-UID index -> D4-valid UID set

Route C:
  original EnzymeCAGE Morgan radius 8 / Tanimoto similarity
  greedy molecule pairing
  max(same direction, reverse direction)
  Top-K=10 over 4,051 query-excluded formal positive reference reactions
  union the D4-valid UIDs attached to those ten reactions
```

The Route-C tie-break is similarity descending and then SHA256 of canonical
reference reaction ascending. Exact query masters are excluded. The operation
was read-only and CPU-only.

Interpretation boundaries:

```text
B=0 does not prove the EC is biologically wrong.
C pool size does not prove a known positive was recovered.
Neither number is an EnzymeCAGE rank or model result.
The evidence UIDs are currently outside D4, so no present hit/recall claim is made.
```

## 6. EC-Null Resolution And Staged D4 Proposal For Teacher Adjudication

This section is a proposal only. It does not modify the pinned Rhea 140 EC
field, complete any D4 asset, rebuild Route B or authorize a model run.

### 6.1 Minimum auditable EC-resolution chain for RHEA:62380

The carbaryl candidate exposes a general boundary: an exact Rhea reaction can
exist while its pinned Rhea release has no reaction-to-EC row. The minimum
chain below separates the facts from the proposed bridge.

| Step | Source and observed fact | What it proves | What it does not prove |
|---:|---|---|---|
| 1 | frozen Rhea 140 defines RHEA:62380 as `carbaryl + H2O + H(+) = 1-naphthol + methylamine + CO2`, with no `rhea2ec.tsv` row | exact chemistry and `rhea_ec=null` | no official frozen EC |
| 2 | current IUBMB/ExPASy ENZYME defines EC 3.5.1.137 as `N-methylcarbamate hydrolase`, gives `carbaryl hydrolase` as an alternative name and explicitly includes carbaryl in the substrate scope | EC 3.5.1.137 is the nomenclature class matching carbaryl hydrolysis | it does not retroactively alter frozen Rhea 140 |
| 3 | current Rhea maps EC 3.5.1.137 to generic N-methylcarbamate RHEA:74171 and carbofuran RHEA:74191, but still not to exact carbaryl RHEA:62380 | Rhea and IUBMB agree on the generic EC chemistry | there is still no direct RHEA:62380-to-EC mapping |
| 4 | BRENDA lists Q8RR61 under EC 3.5.1.137; PMID 11872471 directly connects Q8RR61/CehA to carbaryl hydrolysis | Q8RR61 has an external database EC link plus direct substrate evidence | Q8GRB9 is not established by this step |
| 5 | PMID 16781470 directly supports Q8GRB9/CahA carbaryl-hydrolase activity, but current UniProt does not assign it an EC and the BRENDA EC sequence result does not list Q8GRB9 | Q8GRB9 remains a direct literature positive | it cannot enter a strict database-EC Route B without a separately approved literature-to-EC rule |

The defensible machine-readable representation before teacher approval is:

```text
rhea_master = 62380
rhea_ec = null
external_ec_candidate = 3.5.1.137
external_ec_source = IUBMB/ExPASy ENZYME + BRENDA
external_ec_evidence_strength = nomenclature_scope_plus_Q8RR61_direct_experiment
external_ec_status = pending_teacher_adjudication
```

The project must not silently copy `3.5.1.137` into frozen `rhea2ec.tsv`.
If the teacher accepts the bridge, a separate external-EC field and provenance
record should drive an explicitly versioned Route-B extension.

### 6.2 Proposed search order when an exact Rhea reaction has EC null

```text
1. Preserve the exact Rhea master, direction, chemistry and rhea_ec=null.
2. Query IUBMB Enzyme Nomenclature or its SIB ENZYME/ExPASy mirror for an
   accepted EC whose reaction class and named substrate scope cover the query.
3. Check current Rhea generic/specific reaction cross-references for that EC;
   record whether the exact master is directly linked or only class-related.
4. Use BRENDA to connect the EC to organisms, accessions, substrate records and
   literature; do not infer missing accessions from an organism name alone.
5. Use UniProt and the original paper to verify each proposed UID, exact
   substrate, product evidence, reviewed state and whether the activity is
   direct, promiscuous or inferred.
6. Store the result as external_ec_candidate pending teacher approval; never
   rewrite the pinned Rhea field in place.
```

This order gives IUBMB authority over EC nomenclature, Rhea authority over the
exact reaction, BRENDA authority over enzyme-specific EC evidence and UniProt /
the paper authority over accession identity and direct activity.

### 6.3 Staged D4 and Route-B plan

The suggested sequence separates asset feasibility from a fair model test.

#### Stage A: targeted evidence-UID D4 feasibility only

After teacher authorization, first complete D4 for the two direct paraoxon
positives:

```text
P0A434  strong direct paraoxon activity; EC 3.1.8.1
Q97VT7  direct but low/promiscuous paraoxon activity; EC 3.1.8.1
```

P0A433 is not included in this first pair because its paraoxon annotation is
`By similarity`.

If the teacher selects carbaryl and accepts the EC-null bridge, the analogous
case-specific feasibility pair is:

```text
Q8RR61  direct carbaryl product evidence; BRENDA EC 3.5.1.137
Q8GRB9  direct carbaryl-hydrolase evidence; no current official UID-level EC
```

Stage A may verify sequence, GVP, pocket-node and sequence-ESM asset
constructability. It must not modify the formal candidate pool, report recall
or run EnzymeCAGE. Adding only known positives to a runnable pool would inject
ground-truth labels.

#### Stage B: objective full-pool freeze and D4 expansion

For paraoxon, a read-only UniProt query on 2026-07-23 returned 250 accessions
under EC 3.1.8.1: 15 reviewed and 235 unreviewed. Only one of the 250 currently
has complete frozen D4 assets. The teacher must choose and pin the fair pool
contract, for example reviewed-only or all accessions, before bulk completion.
Whichever rule is selected must be applied to every qualifying UID, not only
P0A434 and Q97VT7.

For carbaryl, the current BRENDA EC 3.5.1.137 page displays seven sequence
accessions, none present in the frozen D4 export. Q8RR61 is the accession with
the direct BRENDA EC link used here; Q8GRB9 needs an explicit teacher decision
because its direct paper evidence is not accompanied by an official UID-level
EC annotation.

Stage B would require a separate authorization to:

```text
pin the external database release/retrieval identity and exact inclusion rule
freeze the complete EC-to-UID candidate universe
complete D4 for every UID selected by that rule
rebuild Route B from the frozen rule without manual positive insertion
validate membership, asset completeness, query exclusion and provenance
```

#### Stage C: model call only after the fair pool is complete

Only after Stage B passes an independent audit may the correct evidence UIDs
be tested for natural Route-B membership and ranked by EnzymeCAGE. Route C
must remain unchanged unless a separately approved, globally applied Route-C
contract is adopted. P0A434, Q97VT7, Q8RR61 or Q8GRB9 must not be manually
unioned into C merely because they are known positives.

### 6.4 External lookup identity used for this proposal

Access date: 2026-07-23.

```text
UniProt query ec:3.1.8.1 TSV
  rows 250; reviewed 15; unreviewed 235
  SHA256 3091688bf9c1e360565bae36bead6551d7b6ab4d18befe477d022d5088e18c90

SIB ENZYME/ExPASy EC 3.5.1.137 HTML
  SHA256 7c880ad6b7f28219d1de5ccfcb3fc122447f28450765e37cfd82fcec2aaf9dd5

BRENDA EC 3.5.1.137 sequence-search HTML
  SHA256 5987d5c036c9e4a3049272efc19b335e519f8dd40d235d6c208be1c7603d971c

current Rhea rhea2ec.tsv
  SHA256 2b449ac148ab155880fd0c751ba5a76b0448f05e42a5079e1877392304a7055a
```

These live lookups are proposal evidence only and do not replace the pinned
Rhea 140 or formal split identities used for the shortlist.

### 6.5 Proposed agent-assisted EC-null evidence-discovery pilot

For future exact Rhea reactions with `rhea_ec=null`, an internet-enabled agent
could perform the source discovery and evidence-packet assembly described in
Section 6.2. This would be a retrieval aid, not an EC authority or an automatic
data-curation step.

Each agent run should be constrained to the same source hierarchy and output
schema:

```text
inputs:
  exact Rhea master, balanced reaction, ChEBI identities and substrate synonyms
preferred sources:
  Rhea; IUBMB/ExplorEnz or SIB ENZYME/ExPASy; BRENDA; UniProt; PubMed/DOI paper
required output per claim:
  source URL/identifier, access date, exact quoted or structured evidence,
  reaction/EC/UID linkage, evidence strength and explicit non-proof boundary
mandatory terminal state:
  supported_external_candidate | conflicting | unresolved
```

The reliability of different agents or foundation models for this task is not
yet established. They may differ in retrieval coverage, synonym resolution,
paywalled-paper access, citation accuracy and willingness to distinguish a
generic EC class from an exact Rhea mapping. A small controlled pilot should
therefore give the same EC-null cases and schema to independently configured
agents, then compare:

```text
official-source retrieval coverage
verifiable-citation precision
reaction-to-EC conclusion agreement
UID-level evidence agreement
unsupported-claim and missed-evidence rates
```

Agreement between models would not itself validate an EC. Every retained claim
must still be reproducible from the cited official database or original paper.
Any unsupported or conflicting result remains `unresolved` for human/teacher
adjudication. No agent output may automatically overwrite `rhea_ec=null`, alter
`known_positive_uids`, expand Route B/C, trigger D4 completion or authorize a
model run.

## 7. Materially Excluded Candidate

Nitrobenzene dioxygenation RHEA:46508/RHEA:46509 was considered and then
excluded from this shortlist.

Its exact Rhea master, exact reaction, EC 1.14.12.23 and four evidence UIDs
(P95561, Q8RTL5, Q8RTL4 and Q8RTL3) have zero exact train/valid/test overlap.
However, RDKit-canonicalized nitrobenzene itself occurs in 52 formal train
rows, all associated with the already trained RHEA:52884 nitrobenzene
nitroreductase reaction. This violates the teacher-required molecule exclusion
gate.

It also has a separate structural mismatch: the complete NADH-dependent
reaction requires reductase NbzAa, ferredoxin NbzAb and the NbzAc/NbzAd
oxygenase complex. No one UID completes the reaction. These facts make it
ineligible for this shortlist even though the four-component biochemical
evidence is genuine.

## 8. Teacher Decision Requested

This shortlist requests only the next teacher adjudication described in
Section 4.3 of the authority document:

1. whether paraoxon and/or carbaryl should advance to an official challenge
   case freeze;
2. whether Stage A may first complete D4 feasibility assets for the two direct
   paraoxon positives P0A434 and Q97VT7 without modifying any pool or running
   the model;
3. if carbaryl advances, whether `external_ec_candidate=3.5.1.137` may be used
   under the provenance chain in Section 6.1 while preserving frozen
   `rhea_ec=null`, and whether Q8GRB9 may remain a literature positive despite
   lacking an official UID-level EC;
4. which objective full-pool rule should govern the later Stage-B D4 expansion
   and Route-B rebuild (for example, reviewed-only versus all accessions from a
   pinned database snapshot);
5. confirmation that no EnzymeCAGE call should occur until the complete
   teacher-approved pool, D4 assets and rebuilt Route B pass independent audit.
6. whether a limited EC-null agent-assisted evidence-discovery pilot may be
   authorized under Section 6.5, and whether the teacher wants a single-agent
   reproducibility check or a controlled comparison across different agents /
   foundation models before adopting any such workflow.

Until that decision, both entries remain candidate-screening evidence only.
