# M3-EXT Paraoxon formal case draft after S1 Stage A PASS

Date: 2026-08-06  
Status: `FORMAL_CASE_DRAFT_AFTER_TEACHER_CONDITIONAL_PROMOTION_AND_S1_TECHNICAL_PASS`  
Scope: M3-EXT Paraoxon official challenge case draft. This file records the case definition, evidence layering, Stage A D4 constructability result, and formal running surface.

## 1. Executive conclusion

Paraoxon now satisfies the teacher-defined conditional promotion gate for an M3-EXT official challenge case draft:

```text
Teacher 2026-08-04 ruling:
Paraoxon is conditionally promoted if Stage A passes.

S1 Stage A local audit 2026-08-05:
P0A434 and Q97VT7 both passed staged protein-side D4 constructability
with AlphaFill 8 Å pocket, ESM-2 3B, GVP, pocket-node ESM and isolated
EnzymeCAGE loader feasibility.
```

Therefore this draft treats Paraoxon hydrolysis as the current M3-EXT official challenge case draft subject to be documented and reviewed.

The important boundary is:

```text
This is not a Paraoxon EnzymeCAGE validation result.
No Paraoxon model score, ranking, prediction, or production D4 merge has been produced.
The formal running surface remains C pool / prediction fallback because Paraoxon B pool = 0.
```

## 2. Authority and source chain

This draft is based on the following local evidence chain.

| Evidence layer | Local source | What it supports |
|---|---|---|
| Teacher ruling | `00_Authority_Teacher_Plan/TEACHER_REPLY_M3_COMBINED_THREE_QUESTIONS_AND_NEXT_STEPS_2026-08-04.md` | Paraoxon conditional promotion; Stage A authorization; B pool = 0 running-surface disclosure; S2 deliverable requirements |
| Candidate shortlist | `M3_EXT_CANDIDATE_SHORTLIST_v0.md` | Paraoxon Rhea/EC/reaction definition, preliminary B/C pool sizes, evidence UID boundary, split-exclusion checks |
| Second adjudication reaudit | Teacher-facing package context; see `M3_EXT_CANDIDATE_SHORTLIST_v0.md` and the accepted 2026-08-07 teacher audit | Rechecked Paraoxon/Carbaryl/Nitrobenzene status and overclaim boundaries before teacher ruling |
| S1 Stage A audit | `M3_EXT_PARAOXON_STAGE_A_P0A434_Q97VT7_ALPHAFILL8_D4_FEASIBILITY_RERUN3_ENVFIX_RETURN_LOCAL_AUDIT_2026-08-05.md` | P0A434/Q97VT7 staged D4 constructability PASS and no-production-mutation boundary |
| S1 return package | `enzymecage_m3_ext_paraoxon_stage_a_p0a434_q97vt7_alphafill8_d4_feasibility_20260805_rerun3_envfix.tar.gz` internal path `enzymecage_m3_ext_paraoxon_stage_a_p0a434_q97vt7_alphafill8_d4_feasibility_20260805_rerun3_envfix/S1_STAGE_A_EXECUTION_REPORT.md` | Raw/staged S1 evidence package; archive SHA256 listed in the audit |

## 3. Formal case identity

| Field | Value |
|---|---|
| Case name | Paraoxon hydrolysis |
| Pollutant category | Organophosphate insecticide; hydrolytic detoxification challenge |
| Rhea master | `RHEA:18053` |
| Rhea left-to-right / forward | `RHEA:18054` |
| Rhea 140 EC | `3.1.8.1` |
| Rhea definition | `paraoxon + H2O = diethylphosphate + 4-nitrophenol + 2 H(+)` |
| Preliminary B pool size | `0` |
| Preliminary C pool size | `13` |
| Current challenge status | Teacher condition met by S1 Stage A PASS; ready for formal case review |

Forward reaction SMILES recorded in the shortlist:

```text
CCOP(=O)(OCC)OC1=CC=C([N+](=O)[O-])C=C1.[H]O[H]>>CCOP(=O)([O-])OCC.O=[N+]([O-])C1=CC=C([O-])C=C1.[H+].[H+]
```

The target pollutant used for molecule-exclusion checking was RDKit-canonicalized as:

```text
CCOP(=O)(OCC)Oc1ccc([N+](=O)[O-])cc1
```

## 4. Why B pool = 0 must be explicitly disclosed

The Paraoxon case has `B pool = 0` in the current M3-EXT candidate materials.

This means the current frozen B-route evidence path does not naturally produce a runnable B pool for Paraoxon. The shortlist records that frozen Rhea 140 has no reviewed Rhea-to-UniProt cross-reference for `RHEA:18053`. The evidence chain is therefore split deliberately:

```text
Rhea supports the exact reaction chemistry.
UniProt and primary papers support selected enzyme activities.
They are not currently a direct frozen Rhea-to-UID mapping.
```

Teacher already acknowledged this in the 2026-08-04 ruling:

```text
Paraoxon B pool = 0.
After promotion, the formal case running surface must use C pool / prediction fallback.
This property must be marked in the case file.
```

Therefore the formal case must not be described as a normal B-route case. It should be described as:

```text
M3-EXT challenge case with exact Rhea chemistry,
direct enzyme evidence for selected UIDs,
and C pool / prediction fallback as the current formal running surface.
```

## 5. Evidence layering for Paraoxon

### 5.1 Reaction chemistry evidence

Rhea provides the exact chemistry:

```text
RHEA:18053 / RHEA:18054
paraoxon + H2O = diethylphosphate + 4-nitrophenol + 2 H(+)
EC 3.1.8.1 in frozen Rhea 140
```

This supports the reaction identity, not a direct model-positive UID by itself.

### 5.2 Direct enzyme activity evidence

Two reviewed UniProt accessions were authorized by the teacher for S1 Stage A.

| UID | Evidence status | Role in this case | Boundary |
|---|---|---|---|
| `P0A434` | UniProtKB reviewed / Swiss-Prot; direct purified-enzyme paraoxon evidence in the shortlist | Strong direct positive evidence UID for Stage A constructability | Not currently merged into production D4; not model-scored for Paraoxon |
| `Q97VT7` | UniProtKB reviewed / Swiss-Prot; purified recombinant SsoPox showed low paraoxonase activity | Auxiliary direct biochemical positive; lower/promiscuous activity evidence | Not evidence for a natural paraoxon mineralization pathway; not model-scored for Paraoxon |

The shortlist cites the following direct evidence records:

```text
P0A434:
PMID 2548585; DOI 10.1021/bi00437a021
PMID 1649628; DOI 10.1021/bi00244a010

Q97VT7:
PMID 15909078; DOI 10.1007/s00792-005-0445-4
```

### 5.3 Auxiliary / excluded UID evidence

`P0A433` is not treated as a UID-specific direct Paraoxon positive in this formal case draft. Its Paraoxon annotation was marked in the shortlist as `By similarity`, so it remains auxiliary provenance only.

No UID should be manually inserted into a candidate pool merely because it is known-positive evidence. Doing so would inject the answer key into the ranking problem.

## 6. Split-exclusion and leakage checks

The shortlist records the following exclusion checks for Paraoxon across formal train, valid and test splits.

| Check | train | valid | test | Result |
|---|---:|---:|---:|---|
| rows resolving to Rhea master `18053` | 0 | 0 | 0 | PASS |
| exact forward or reverse reaction SMILES | 0 | 0 | 0 | PASS |
| Paraoxon molecule in either reaction side | 0 | 0 | 0 | PASS |
| `P0A434`, `P0A433` or `Q97VT7` UID rows | 0 | 0 | 0 | PASS |
| exact EC `3.1.8.1` rows | 0 | 0 | 0 | PASS |

Interpretation:

```text
The Paraoxon query chemistry, target molecule, direct evidence UIDs and EC
were not found in the frozen formal train/valid/test splits by these checks.
```

This supports the challenge-case screening boundary. It does not prove downstream model success.

## 7. S1 Stage A result

S1 Stage A was authorized only for `P0A434` and `Q97VT7`.

The audited S1 return package final status was:

```text
M3_EXT_PARAOXON_STAGE_A_PASS_BOTH_UIDS_ALPHAFILL8_STAGED_D4_LOADER
```

Per-UID result:

| UID | UniProt status | AlphaFill | 8 Å pocket | ESM-2 3B | GVP | isolated loader | Final S1 status |
|---|---|---|---:|---|---:|---|---|
| `P0A434` | reviewed Swiss-Prot | 200/200, 27 hits, 43 transplants | 24 residues | `[367,2560]` node, `[24,2560]` pocket-node | 24 nodes | dataset length 1, item constructed | PASS |
| `Q97VT7` | reviewed Swiss-Prot | 200/200, 34 hits, 51 transplants | 39 residues | `[316,2560]` node, `[39,2560]` pocket-node | 39 nodes | dataset length 1, item constructed | PASS |

The S1 audit also records:

```text
formal production assets mutated: false
production pool mutated: false
model run performed: false
validation claim made: false
```

Runtime/resource note:

| UID | total wall sec | ESM-2 3B sec | GVP sec | loader sec | peak GPU allocated |
|---|---:|---:|---:|---:|---:|
| `P0A434` | 65.08 | 31.41 | 3.18 | 1.51 | 11058 MB |
| `Q97VT7` | 37.44 | 30.65 | 0.018 | 1.01 | 11048 MB |

Timing caveat: the S1 timing table records `pocket_node_sec` equal to `esm3b_compute_sec`; this appears to be a duplicated or ambiguous timing field. Runtime summaries should use `per_uid_total_wall_sec` or explicit ESM/GVP/loader fields, not add `esm3b_compute_sec + pocket_node_sec`.

## 8. Formal running surface

Because `B pool = 0`, the current formal running surface is:

```text
Primary runnable surface for this case:
C pool / prediction fallback

Not currently runnable as:
normal B-route exact reviewed Rhea-to-UID pool
```

Current C pool size recorded in the shortlist is:

```text
C preliminary pool size = 13
```

Important interpretation:

```text
C pool size is not an EnzymeCAGE rank.
C pool size is not proof that the known positive UIDs are recoverable.
C pool size is not a model score.
```

Before any formal Paraoxon model run, a separate execution contract should freeze:

1. the exact input reaction representation;
2. the C pool / prediction fallback construction rule;
3. whether staged S1 assets may be merged into an isolated evaluation asset bundle;
4. the prohibition against manually adding known positives to the pool;
5. the scoring and reporting fields;
6. the no-production-mutation boundary unless separately authorized.

## 9. What this case draft supports and does not support

This draft records that Paraoxon is ready for formal case review after S1 technical passage.

It supports the following documentation statement:

```text
Use Paraoxon hydrolysis as the S2 formal case draft subject.
Report B pool = 0 and C pool / prediction fallback as the running surface.
Use P0A434 and Q97VT7 as evidence-layered Stage A UIDs whose staged D4 constructability passed.
```

It does not support the following actions or claims:

```text
production D4 merge;
production pool mutation;
Route-B or Route-C pool update;
manual insertion of P0A434 or Q97VT7 into any scoring pool;
EnzymeCAGE Paraoxon model scoring;
claim that Paraoxon has been validated by EnzymeCAGE;
claim that Stage A proves biological correctness or environmental degradation performance.
```

## 10. Recommended next step after this draft

If the teacher accepts this S2 case file draft, the next technical step should be a separate, explicit Paraoxon execution contract rather than an implicit model run.

Recommended contract title:

```text
M3-EXT Paraoxon C-pool / prediction-fallback formal execution contract
```

Minimum contents:

| Required item | Why |
|---|---|
| Freeze C pool / fallback construction rule | Avoid manual positive insertion and keep ranking fair |
| Freeze input reaction representation | Avoid changing model input after seeing outcomes |
| Define staged asset use | Decide whether S1 assets remain isolated or enter a case-specific evaluation bundle |
| Define output metrics | Separate pool membership, model rank, score, and evidence UID recovery |
| Define failure gates | Stop if assets, pool construction, or loader compatibility fail |
| Define no-production-mutation rule | Preserve current formal D4 and pools unless teacher explicitly authorizes a merge |

## 11. Short teacher-facing wording

Safe summary:

```text
Paraoxon has met the teacher-defined conditional promotion gate for an M3-EXT formal case draft:
S1 Stage A passed for P0A434 and Q97VT7 at the staged D4 constructability level.
The case file explicitly marks B pool = 0, evidence is layered rather than treated as a direct Rhea-to-UID mapping,
and the formal running surface remains C pool / prediction fallback.
No model scoring, production D4 merge, pool mutation, or Paraoxon validation claim has been made.
```

Unsafe wording to avoid:

```text
Paraoxon has been validated.
EnzymeCAGE has scored Paraoxon.
P0A434/Q97VT7 are now in production D4.
Paraoxon can run as a normal B-pool case.
Stage A proves the biology is correct.
```
