# Failure case analysis: AlphaFoldDB-only P2Rank on-demand D4 control

Date: 2026-08-03

Source package:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_single_enzyme_ondemand_d4_alphafolddb_only_p2rank_control_20260803.tar.gz
```

Parent local audit:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_SINGLE_ENZYME_ONDEMAND_D4_ALPHAFOLDDB_ONLY_P2RANK_CONTROL_RETURN_LOCAL_AUDIT_2026-08-03.md
```

## 1. What `BLOCKED_AFDB_P2RANK_NO_POCKET` means

`BLOCKED_AFDB_P2RANK_NO_POCKET` does **not** mean:

```text
P2Rank checked a pocket database and did not find this UID.
```

P2Rank is not being used as a pocket database lookup.

In this control, P2Rank was used as an online/local predictor:

```text
UniProt UID
→ AlphaFoldDB protein 3D structure
→ P2Rank 2.5.1 `prank predict -c alphafold`
→ P2Rank prediction/residue CSV
→ top-ranked predicted pocket residue mapping
→ EnzymeCAGE-style pocket PDB + pocket_info.csv
→ ESM-2 3B pocket-node features + GVP
→ isolated EnzymeCAGE loader validation
```

Therefore:

```text
BLOCKED_AFDB_P2RANK_NO_POCKET
= AlphaFoldDB structure was obtained and parsed, and P2Rank ran, but P2Rank did not provide a top predicted pocket with usable mapped residues.
```

This is a predicted-pocket failure, not a missing-structure failure.

## 2. Difference from AlphaFill

The strict AlphaFill route and P2Rank route define pockets differently.

| Route | Input 3D structure | Pocket evidence | How pocket is defined | Main failure mode |
|---|---|---|---|---|
| Strict AlphaFill | AlphaFill transplant CIF/JSON, ultimately based on AlphaFold/PDB-REDO context | transplanted ligand/cofactor/homologous structure context | residues within 8 Å of transplanted ligand/cofactor | no AlphaFill entry; no usable hits/transplants; ligand-neighbor extraction invalid |
| AlphaFoldDB + P2Rank | AlphaFoldDB protein-only structure | predicted surface pocket from structure geometry/chemistry | P2Rank predicted pocket residues | no AFDB structure; P2Rank predicts no usable pocket |

Important interpretation:

```text
AlphaFill asks: can we define a pocket from transferred ligand/cofactor evidence?
P2Rank asks: given a protein 3D structure, does the surface look like it contains a ligandable pocket?
```

So P2Rank can rescue cases where AlphaFill has no transplant metadata, but P2Rank evidence is lower-tier and should not be reported as strict AlphaFill ligand-neighbor evidence.

## 3. Failure summary in AFDB-only control

Total:

```text
n_input_uids = 100
n_pass = 45
n_failed = 55
```

Failure classes:

| Failure class | Count | Meaning |
|---|---:|---|
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | 43 | AlphaFoldDB structure was obtained; P2Rank ran; no usable top pocket residues were produced |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | 12 | AlphaFoldDB API and conventional v6/v5/v4 PDB/mmCIF attempts did not provide a usable structure |

There were:

```text
0 feature-stage failures
0 GVP-stage failures
0 loader-validation failures among generated predicted-pocket assets
```

So once the pipeline obtains a usable structure and a usable P2Rank pocket, the downstream D4 staging/loader chain is technically stable in this pilot.

## 4. Analysis of `BLOCKED_AFDB_P2RANK_NO_POCKET`

### 4.1 Size/length pattern

The 43 no-pocket UIDs have:

```text
min sequence length = 16 aa
median sequence length = 95 aa
mean sequence length = 97.7 aa
max sequence length = 228 aa
```

Length bins:

| Length bin | Count |
|---|---:|
| `<=120 aa` | 37 |
| `121-250 aa` | 6 |
| `>250 aa` | 0 |

For comparison, the 45 PASS UIDs have:

```text
mean sequence length ≈ 390.3 aa
median sequence length = 377 aa
```

Interpretation:

```text
The no-pocket failures are overwhelmingly short/small proteins or peptide-like entries. This is consistent with P2Rank not finding a sufficiently large or well-formed ligandable surface pocket.
```

### 4.2 AlphaFold confidence pattern

Mean pLDDT estimated from AlphaFoldDB PDB B-factor field:

| Group | n | mean pLDDT | median pLDDT |
|---|---:|---:|---:|
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | 43 | 92.2 | 93.9 |
| `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 45 | 89.7 | 92.2 |

Interpretation:

```text
No-pocket failures are not mainly caused by low-confidence AlphaFoldDB structures. Many no-pocket cases have high-confidence structures, but the proteins are too small or lack a P2Rank-filtered pocket.
```

### 4.3 P2Rank log pattern

For the 43 no-pocket UIDs:

| P2Rank log metric | Count |
|---|---:|
| `LIGANDABLE POINTS = 0` | 21 |
| `LIGANDABLE POINTS > 0` | 22 |
| `FILTERED CLUSTERS = 0` | 43 |

Interpretation:

```text
In roughly half the cases P2Rank found no ligandable surface points at all. In the other half it found a few candidate points/clusters, but none survived filtering into a usable predicted pocket.
```

Representative no-pocket examples:

| UID | Length | Organism | P2Rank evidence |
|---|---:|---|---|
| `P27067` | 16 | Vigna unguiculata subsp. unguiculata | `LIGANDABLE POINTS=0`, `FILTERED CLUSTERS=0` |
| `P0DJM7` | 23 | Protobothrops tokarensis | `LIGANDABLE POINTS=0`, `FILTERED CLUSTERS=0` |
| `B2GKN0` | 98 | Kocuria rhizophila | `LIGANDABLE POINTS=0`, `FILTERED CLUSTERS=0` |
| `Q55842` | 100 | Synechocystis sp. PCC 6803 | `LIGANDABLE POINTS=1`, `CLUSTERS=1`, `FILTERED CLUSTERS=0` |
| `Q9RYJ3` | 228 | Deinococcus radiodurans R1 | `LIGANDABLE POINTS=1`, `CLUSTERS=1`, `FILTERED CLUSTERS=0` |

Conclusion:

```text
These are real P2Rank no-pocket calls under the selected top-pocket rule, not evidence that the workflow forgot to query a pocket database.
```

## 5. Analysis of `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED`

These 12 UIDs did not yield an AlphaFoldDB structure under the tested route:

```text
Q72CF1
Q73FB9
P89436
P11156
P82679
Q70KP1
P59709
P39915
P20304
O64174
Q9Z0D5
Q9EVI6
```

The executor tried:

```text
AlphaFoldDB API
conventional AF-<UID>-F1-model_v6.pdb/cif
conventional AF-<UID>-F1-model_v5.pdb/cif
conventional AF-<UID>-F1-model_v4.pdb/cif
```

Representative example:

```text
Q9Z0D5:
AlphaFoldDB API = 404
AF-Q9Z0D5-F1-model_v6.pdb/cif = 404
AF-Q9Z0D5-F1-model_v5.pdb/cif = 404
AF-Q9Z0D5-F1-model_v4.pdb/cif = 404
```

Organism/source pattern:

| UID | Length | Organism/source type |
|---|---:|---|
| `P89436` | 518 | Human herpesvirus 2 |
| `P11156` | 388 | Enterobacteria phage T4 |
| `Q70KP1` | 430 | Porcine torovirus |
| `P59709` | 424 | Bovine coronavirus |
| `O64174` | 329 | Bacillus phage SPbeta |
| `Q9Z0D5` | 281 | Milk vetch dwarf C1 alphasatellite |
| `P82679` | 31 | short bacterial protein |
| `P20304` | 13 | very short Sus scrofa entry |
| `Q72CF1` | 351 | bacterial |
| `Q73FB9` | 485 | bacterial |
| `P39915` | 463 | bacterial |
| `Q9EVI6` | 443 | bacterial endosymbiont |

Interpretation:

```text
These are external structure-source coverage failures for the AlphaFoldDB-only route. Some are viral/phage/satellite entries; some are very short entries; some are bacterial entries not reachable through the tested AlphaFoldDB endpoints.
```

This is not a downstream EnzymeCAGE loader problem.

## 6. What these failures imply for the on-demand asset tool

The current technical evidence supports an agent tool with explicit tiers:

```text
Tier 1: strict AlphaFill transplant 8 Å pocket
Tier 2: AlphaFoldDB + P2Rank predicted pocket
Tier 3: optional other trusted structure sources / old-pocket revalidation, if authorized
```

For failures:

```text
If no structure is available from the allowed source, return BLOCKED_STRUCTURE_FETCH_FAILED.
If structure is available but P2Rank finds no usable pocket, return BLOCKED_PREDICTED_POCKET_NOT_FOUND.
Do not fabricate pocket residues.
Do not use whole-protein or arbitrary fixed-residue fallbacks as if they were valid D4 pocket assets.
```

This fits the project goal:

```text
The agent can automate asset supplementation from UID alone, but it should fail closed when external structure/pocket evidence is absent.
```

## 7. Teacher-facing wording

Suggested wording:

```text
For the remaining failures, the blockers are mostly outside the EnzymeCAGE feature-generation code itself. In the AlphaFoldDB-only + P2Rank control, 12/100 UIDs had no reachable AlphaFoldDB structure after API and v6/v5/v4 URL attempts. Another 43/100 had an AlphaFoldDB structure and P2Rank was executed, but P2Rank did not produce a usable predicted pocket. These no-pocket cases were overwhelmingly short/small proteins: 37/43 were ≤120 aa, with median length 95 aa, and their mean pLDDT was high rather than low. Therefore the failure mode is mainly absence of an acceptable structure/pocket evidence source, not a failure of ESM-2 3B, GVP, or EnzymeCAGE loader construction. The proposed tool should return explicit blocker states for these cases rather than inventing assets.
```

