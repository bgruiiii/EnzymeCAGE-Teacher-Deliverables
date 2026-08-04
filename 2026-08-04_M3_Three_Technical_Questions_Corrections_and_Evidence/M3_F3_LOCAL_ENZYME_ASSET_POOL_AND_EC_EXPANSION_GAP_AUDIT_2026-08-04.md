# M3 F3 local enzyme asset pool and EC-expansion gap audit

Date: 2026-08-04  
Scope: local-only read audit under `/home/a/EnzymeCAGE`; no Chenyu filesystem
inspection; no asset modification.

## Question being answered

This audit separates two different questions that should not be merged:

1. What enzyme assets are actually available locally now, before any new
   Chenyu transfer?
2. If M4 expands enzyme candidates by complete EC number beyond the current
   model/training UID domain, how large is the likely missing-asset gap?

This is not a model-performance audit and does not claim any biological
candidate is correct.

## Two gap classes

For teacher-facing communication, the missing-asset problem should be split
into two classes.

### Gap class 1: local Rhea-derived enzyme-pool asset gap

This means the gap between enzymes already present in the local Rhea-derived
tables and the features needed by the current EnzymeCAGE model stack.

This class includes:

- strict cleaned 2026 enzyme UID already in `all_enzymes.csv`, but lacking
  valid pocket;
- strict cleaned 2026 enzyme UID with sequence/pocket evidence but lacking
  current ESM2-3B corrected features;
- historical ESM-C 600M assets that were built for an earlier feature choice
  but are not a substitute for the current ESM2-3B model input;
- GVP assets recorded historically but not currently materialized as readable
  local shard files in this workspace.

This class asks: should M4 proactively rebuild/repackage the missing full
feature chain for the local strict Rhea enzyme pool, or only backfill individual
UIDs when candidate generation needs them?

### Gap class 2: complete-EC candidate-expansion asset gap

This means the additional gap introduced if M4 uses complete EC numbers to
expand candidate enzymes beyond the current model/training UID domain.

Important boundary: the 218,010 UID figure in this audit is **not** from a live
UniProt all-EC web query. It is a local, release-pinned Rhea 140 calculation:

1. take complete EC rows from local `rhea2ec.tsv`;
2. join by Rhea master ID to local `rhea2uniprot_sprot.tsv`;
3. union the reviewed UniProt UIDs attached to Rhea reactions sharing those ECs.

Thus this is a reproducible Rhea-official / Swiss-Prot-linked EC expansion
baseline, not the maximum possible EC universe from BRENDA, KEGG, UniProt live,
TrEMBL, or literature mining. A broader live/external EC source would need a
separate teacher-approved source contract.

Prior teacher-contract context:

- 2026-07-16 teacher planning introduced `EnzymePoolAgent` and described route
  B as: Reaction Agent emits 1--3 EC numbers, then the EnzymeCAGE side uses the
  EC class to retrieve enzyme UIDs as the candidate pool.
- 2026-07-17 teacher adjudication adopted M3 v1 as B-primary / C-fallback with
  `pool >100 fail closed`, while explicitly keeping D4 assets frozen for M3.
- The accepted P0 evidence measured release-pinned EC-to-reviewed-UID pools and
  D4-valid intersections from the local Rhea 140 raw reviewed-UniProt join.
- The same adjudication left open the later choices of external complete-EC UID
  source, source release, reviewed/unreviewed policy and asset-completion
  procedure.

Therefore, the local Rhea 140 EC baseline is the currently evidenced contract
baseline. A live UniProt full-EC sweep would be a useful M4 source-selection
experiment, but it is a broader and temporally unstable data-source decision,
not something already fixed by the prior M3 contract.

## What source was used in the earlier same-EC enzyme tests?

The earlier work used two different evidence layers, and they must be kept
separate.

### Formal M3-P0 / EnzymePoolAgent baseline

For the formal B-primary EC pool evidence, the tested source was the local
release-pinned Rhea 140 baseline, not a live UniProt full-EC sweep.

Specifically:

- route B was defined as exact frozen Rhea complete EC to query-excluded
  formal Label=1 EC-to-UID to D4;
- EC rows came from frozen/local Rhea files such as `rhea2ec.tsv`;
- enzyme UID mappings came from the local Rhea reviewed-UniProt mapping
  `rhea2uniprot_sprot.tsv`;
- accepted P0 statistics included all 6,151 complete EC numbers, including
  978 complete EC numbers with zero source reviewed UID in that pinned Rhea
  baseline.

Therefore, when we answer the current F3 question about the **already evidenced
EC index baseline**, it is correct to count local missing assets against the
local Rhea complete-EC reviewed-UniProt baseline first.

### M3-EXT pollutant shortlist / external evidence examples

The later Paraoxon/Carbaryl M3-EXT shortlist did use external read-only sources
for evidence discovery and proposal fields. For example:

- Paraoxon EC 3.1.8.1 was checked through a UniProt `ec:3.1.8.1` TSV response,
  which returned 250 UIDs, separated into 15 reviewed and 235 unreviewed;
- Carbaryl used external IUBMB/ExPASy and BRENDA EC 3.5.1.137 evidence, while
  explicitly disclosing that frozen Rhea 140 had no EC row for RHEA:62380;
- those external results were labeled as staged proposals and did not mutate
  the frozen Rhea route-B pool, D4 assets or model-scored candidate pool.

Therefore, the evidence says:

1. The formal M3-tested same-EC pool was Rhea-snapshot based.
2. We have proof that live/external EC sources can reveal biologically relevant
   UIDs outside the current D4 domain.
3. But live UniProt/BRENDA/TrEMBL as the general M4 EC source has not yet been
   frozen by teacher contract and should be presented as a decision/pilot item,
   not as an already completed baseline.

## Evidence sources

- Database construction log:
  `/home/a/EnzymeCAGE/custom/docs/DATABASE_PROGRESS.md`
- Raw Rhea 140 mappings:
  - `data/raw/rhea/RHEA-140_2026-01-21/tsv/rhea2uniprot_sprot.tsv`
  - `data/raw/rhea/RHEA-140_2026-01-21/tsv/rhea2ec.tsv`
  - `data/raw/rhea/RHEA-140_2026-01-21/uid2seq.pkl`
- Strict 2026 cleaned enzyme table:
  `data/processed/rhea/2026-01-21/all_enzymes.csv`
- Strict pocket metadata:
  `data/processed/rhea/2026-01-21/pockets/pocket_info.csv`
- Materialized local pocket package:
  `data/processed/rhea/2026-01-21/cloud_transfer/pocket_node_rerun_2026-04-22/`
  and
  `data/processed/rhea/2026-01-21/cloud_transfer/pocket_node_rerun_2026-04-22.tar.gz`
- Training clean local package:
  `custom/github_upload/reaction_enzyme_microbe_training_clean_2026-06-01/`
- Local ESM2-3B extraction return:
  `custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/t3_1_full_esm2_3b_extraction/`
- Accepted P0 EC-pool evidence:
  `custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/m3_p0a1a_decision_matrix_distribution_final_package_correction_20260717/outputs/`

Fixed-file identities used in the current local recount:

| File | Bytes | SHA256 |
|---|---:|---|
| `data/raw/rhea/RHEA-140_2026-01-21/tsv/rhea2ec.tsv` | 193,357 | `5a90d95d4aab686b4a0c46db6495b89c6431696f4bb351a5a63e4c84a3187d44` |
| `data/raw/rhea/RHEA-140_2026-01-21/tsv/rhea2uniprot_sprot.tsv` | 8,622,649 | `89efa346087108e8b0abbeb3d8739a15d1979951bcfa9b42fa01d8786c5d827e` |
| `data/processed/rhea/2026-01-21/all_enzymes.csv` | 73,842,465 | `a99965d91101c3415e222736ebc6ceaa151310be9be70c32a95fe2ee81d7cf30` |
| `data/processed/rhea/2026-01-21/pockets/pocket_info.csv` | 28,757,164 | `7c8904c4fe9858d641dd155d70465d5e6e5e46ca95780ec20207b1f8d927f391` |
| `t3_1_full_esm2_3b_extraction/outputs/final_feature_counts.csv` | 2,900,355 | `5df73708481699b96a70b7ed4aa91bca74a0358e2be4de39ffe1772f9018d366` |
| `m3_p0a1a.../outputs/ec_uid_pool_statistics.csv` | 445,117 | `4cc90c9b59e71505ec93abdf716b3e629f98e5c284c1262f16c40fb7a0dd8246` |

## Local UID universes

| UID universe | Count | Local evidence |
|---|---:|---|
| Raw Rhea-linked UniProt UID | 236,103 | `rhea2uniprot_sprot.tsv`; `uid2seq.pkl` |
| Raw UID with local sequence in `uid2seq.pkl` | 236,103 | `uid2seq.pkl` |
| Strict cleaned 2026 main-table UID | 195,743 | `all_enzymes.csv` |
| Broad auxiliary sequence table UID | 238,984 | `broad_protein_asset_pool/all_enzymes.csv` |
| Taxonomy-filtered bacteria/fungi/archaea UID | 168,335 | taxonomy-filtered main table |
| Training-clean selected UID | 107,731 | `selected_training_uids.csv` |
| Rhea official complete-EC source UID | 218,010 | recomputed from complete EC in `rhea2ec.tsv` plus `rhea2uniprot_sprot.tsv` |

Interpretation: the user’s concern is valid. The final training-clean UID count
is not the same as the pre-filter strict enzyme asset universe. Asset coverage
must therefore be reported at multiple levels.

## Raw-to-strict filtering reasons

The transition from raw Rhea-linked UIDs to the strict cleaned 2026 enzyme pool
is documented in `DATABASE_PROGRESS.md` and should be teacher-facing because the
counts are otherwise easy to misread.

Raw pair-level cleaning:

| Step | Count / effect | Reason |
|---|---:|---|
| raw Rhea reaction-enzyme rows | 391,027 rows | source table `rhea2uniprot_sprot.tsv` |
| raw unique UniProt UID | 236,103 UID | all raw Rhea-linked reviewed UniProt accessions |
| polymer reactions without usable SMILES | 336 reactions | not usable for the reaction-SMILES feature path |
| rows missing SMILES after Rhea mapping | 18,626 rows | Rhea reaction could not be mapped to usable SMILES |
| rows remaining after SMILES mapping | 372,401 rows | candidate rows after requiring usable reaction SMILES |
| unique raw reaction SMILES before cleaning | 13,619 reactions | pre-canonicalization reaction universe |
| unique reactions failed canonicalization/filtering | 1,747 reactions | failed reaction cleaning / canonicalization rules |
| pair rows removed by reaction cleaning | 41,888 rows | reaction-level cleaning removed associated pairs |
| pair rows missing sequence | 0 rows | no sequence-missing loss after UID-to-sequence mapping |
| pair rows removed by sequence length > 1000 | 12,188 rows | EnzymeCAGE feature/model boundary excludes long sequences |
| final cleaned positive pairs | 320,043 rows | strict cleaned main table |

Raw UID-to-strict UID flow:

| UID stage | Count |
|---|---:|
| raw Rhea-linked UID | 236,103 |
| after requiring non-null reaction SMILES | 222,104 |
| final cleaned main-table UID / strict `all_enzymes.csv` | 195,743 |
| missing from strict relative to raw Rhea-linked UID | 40,360 |

Documented UID removal reasons:

| Removal reason | UID count |
|---|---:|
| no usable reaction SMILES | 13,999 |
| fail canonical reaction cleaning only | 21,403 |
| fail sequence length >1000 only | 4,285 |
| fail both canonicalization and sequence-length filter | 673 |
| missing sequence after mapping | 0 |

Interpretation: the strict 195,743 UID pool is not an arbitrary biological
filter. It is the result of reaction-SMILES usability, canonical reaction
cleaning and model-compatible sequence-length filtering.

The later bacteria/fungi/archaea filter is separate:

| Later taxonomy-filtered stage | Count |
|---|---:|
| unfiltered source UID rows | 195,743 |
| kept UID rows | 168,335 |
| excluded UID rows | 27,408 |
| filtered enzyme-reaction pairs | 227,056 |
| removed enzyme-reaction pairs | 92,987 |

Keep rule: UniProt lineage must be bacteria, fungi or archaea. Excluded UID
groups include animal/metazoa, plant/viridiplantae, other eukaryota and virus.
This was motivated by the microorganism-side branch and should not be confused
with the earlier raw-to-strict reaction-feature cleaning.

## Locally available assets

### Sequence

Local sequence coverage is broad:

- `uid2seq.pkl`: 236,103 UID
- Covers all strict 195,743 UID.
- Covers all 218,010 Rhea official complete-EC source UID.

Conclusion: sequence itself is not the main local bottleneck for Rhea-derived
EC expansion.

### Pocket PDB / pocket metadata

Strict pocket metadata:

- `pocket_info.csv`: 191,290 UID
- Valid non-empty pocket residue rows: 191,062 UID
- Empty/placeholder pocket rows: 228 UID
- Strict 195,743 UID missing valid pocket rows: 4,681 UID

Important local path distinction:

- Primary path `data/processed/rhea/2026-01-21/pockets/pocket/` currently has
  191,290 `.pdb` symlink entries, but only 2,545 resolve as existing local
  files; 188,745 are broken links in this local workspace.
- Materialized local transfer path
  `data/processed/rhea/2026-01-21/cloud_transfer/pocket_node_rerun_2026-04-22/pocket/`
  contains 191,290 real `.pdb` files.
- Its archive
  `data/processed/rhea/2026-01-21/cloud_transfer/pocket_node_rerun_2026-04-22.tar.gz`
  is present locally, size 951,858,580 bytes, with 191,290 PDB members.
- `data/processed/rhea/2026-01-21/pockets/pocket.tar` is an empty 0-byte file
  and must not be used as evidence.

Conclusion: local full strict pocket PDB assets are available through the
materialized cloud-transfer directory/archive, not through the primary symlink
directory.

### GVP

Historical log evidence says strict GVP was built at about 191,060 usable
entries. However, in the current local filesystem:

- canonical GVP path
  `data/processed/rhea/2026-01-21/feature/protein/gvp_feature/`
  is not materialized with shards/manifest.
- training clean package contains only:
  - `features/enzyme/gvp_sharded_pool/selected_training_uids.csv` with 107,731 UID
  - `features/enzyme/gvp_sharded_pool/gvp_full_pool_upload_manifest.json`
    describing a 194-file / 29,634,575,395-byte official GVP pool
- the actual large GVP shard files are not present at their canonical local
  paths in this workspace.

Conclusion: for local-only transfer, full GVP assets are not currently available
as readable local files, even though historical logs record that they were built
and expected under the canonical path.

### ESM-C

Historical log evidence says strict ESM-C sequence-level features were completed
for 195,743 UID and pocket-node features for 191,062 valid pocket targets.
However, in the current local filesystem:

- `data/processed/rhea/2026-01-21/feature/protein/ESM-C_600M/node_level/`
  contains 0 strict `.npz` files.
- `protein_level/seq2feature.pkl` is absent at the canonical strict path.
- full ESM-C pocket-node sharded output is absent at the canonical strict path.
- the training clean package has 107,731 ESM-C request rows, but
  `esm_c_feature_status.csv` records `esm_c_included_locally=False`.
- local complete example ESM-C files are limited to small/demo sets, e.g. 260
  UID in the 300-example package.

Conclusion: full strict ESM-C assets are not locally materialized in the current
workspace; the local training package has request manifests, not the full
feature payload.

### ESM2-3B corrected features

Local return directory
`t3_1_full_esm2_3b_extraction` contains a completed ESM2-3B extraction result
for the current training/D4 subdomain:

- `outputs/final_feature_counts.csv`: 107,705 UID
- `outputs/final_validation_failures.csv`: 0 rows
- 20 `seq2feature_part_*.pkl` files, total 398,196,736 bytes
- 20 `pocket_node_feature_part_*.pt` files, total 398,983,168 bytes
- shard summary totals:
  - UID/pass count: 107,705
  - unique sequence count: 105,099
  - pocket feature count: 107,705
  - fail count: 0

Coverage:

- ESM2-3B local UID in strict 195,743: 107,705
- ESM2-3B local UID in training selected 107,731: 107,705
- training selected UID missing local ESM2-3B: 26
- strict UID missing local ESM2-3B: 88,038

Conclusion: local ESM2-3B assets are available for the current 107,705-UID
training/D4 subdomain, not for the full pre-filter strict 195,743-UID pool.

## EC-expansion gap from Rhea official complete EC mappings

Rhea official complete-EC source UID set was recomputed locally from:

- complete EC regex: `^[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+$`
- `rhea2ec.tsv`
- `rhea2uniprot_sprot.tsv`

Result:

- complete EC count: 6,151
- unique complete-EC source UID: 218,010

Coverage of these 218,010 UID:

| Asset / UID set | EC-source UID covered | EC-source UID missing |
|---|---:|---:|
| raw `uid2seq.pkl` sequence | 218,010 | 0 |
| strict cleaned `all_enzymes.csv` | 186,909 | 31,101 |
| broad auxiliary sequence table | 202,907 | 15,103 |
| strict pocket metadata | 182,998 | 35,012 |
| strict valid pocket rows | 182,770 | 35,240 |
| local ESM2-3B 107,705 subdomain | 103,206 | 114,804 |
| training-clean selected 107,731 UID | 103,231 | 114,779 |

Interpretation:

- If M4 uses complete EC to expand enzyme candidates beyond the current
  training/D4 domain, sequence lookup is likely not the primary bottleneck for
  Rhea-derived UIDs.
- The main bottleneck is full model-ready D4 coverage: pocket/GVP/ESM2-3B/ESM
  registration for expanded UIDs.
- The current local ESM2-3B model subdomain covers only 103,206 / 218,010
  complete-EC source UID.

## Relation to the earlier M3-EXT examples

The earlier Paraoxon/Carbaryl M3-EXT audit already showed the same type of
problem in concrete form:

- EC/evidence can identify biologically meaningful candidate UIDs outside the
  current model-ready D4 domain.
- Those UIDs cannot be honestly ranked by EnzymeCAGE until their D4 assets are
  constructed and validated.

This supports the need for an on-demand D4 backfill tool in M4, but does not
authorize silently injecting hand-picked positives into M3.

## Bottom-line local answer

Local assets currently available enough to transfer/use immediately:

1. Raw sequence for 236,103 Rhea-linked UID.
2. Strict materialized pocket PDB package for 191,290 UID via
   `cloud_transfer/pocket_node_rerun_2026-04-22`.
3. ESM2-3B corrected features for 107,705 UID in the current training/D4
   subdomain.
4. Training-clean manifests/request tables for 107,731 UID.

Local assets not currently materialized as full readable local files:

1. Full strict GVP shard pool.
2. Full strict ESM-C sequence/protein features.
3. Full strict ESM-C pocket-node sharded features.
4. Full ESM2-3B coverage for the pre-filter strict 195,743 UID pool.

Therefore, for F3 the correct answer should not be “we have no assets” and
also should not be “we already have full assets.” The correct local position is:

> We have broad local sequence coverage and a materialized strict pocket PDB
> package, and we have model-subdomain ESM2-3B features for 107,705 UID. However,
> local full model-ready D4 coverage is currently limited to the training/D4
> subdomain. Complete-EC expansion would introduce many additional UIDs, so M4
> needs a formal on-demand D4 backfill path or a rebuilt full-coverage asset
> package before those expanded candidates can be ranked.
