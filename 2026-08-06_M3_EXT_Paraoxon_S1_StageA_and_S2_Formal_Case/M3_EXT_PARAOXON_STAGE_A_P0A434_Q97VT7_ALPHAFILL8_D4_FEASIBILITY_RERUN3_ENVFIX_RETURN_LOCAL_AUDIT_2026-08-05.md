# Local audit: M3-EXT Paraoxon Stage A P0A434/Q97VT7 AlphaFill 8Å D4 feasibility rerun3 envfix

Date: 2026-08-05  
Audited archive:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_ext_paraoxon_stage_a_p0a434_q97vt7_alphafill8_d4_feasibility_20260805_rerun3_envfix.tar.gz
```

Archive SHA256:

```text
a0c7724edbbb5aeac0c566e2c393a5b8a5029a515efacc1d0ee721cbb334095a
```

## 1. Verdict

Verdict: **ACCEPT AS M3-EXT Paraoxon S1 Stage A technical PASS, with a minor timing-field caveat.**

The return package satisfies the teacher-authorized S1 scope:

```text
only P0A434 and Q97VT7 were processed;
both UIDs used fresh UniProt + AlphaFill live raw inputs;
both UIDs passed AlphaFill 8Å pocket extraction;
both UIDs generated corrected ESM-2 3B staged features;
both UIDs generated GVP staged assets;
both UIDs had matching GVP node count and pocket-node ESM rows;
both UIDs passed actual isolated load_geometric_dataset(...) loader feasibility;
formal production assets were not mutated;
production pool was not mutated;
no EnzymeCAGE model inference/ranking/scoring was performed;
no Paraoxon validation claim was made.
```

Final status in package:

```text
M3_EXT_PARAOXON_STAGE_A_PASS_BOTH_UIDS_ALPHAFILL8_STAGED_D4_LOADER
```

Important boundary: this is a **staged protein-side D4 constructability PASS**, not a biological proof that EnzymeCAGE validated Paraoxon, and not a production D4 merge.

## 2. Manifest and archive integrity

Local checks:

```text
tar readable: PASS
MANIFEST.sha256 check: PASS for all listed files
file count under unpacked return directory: 65
```

Key report files present:

```text
FINAL_STATUS.txt
S1_STAGE_A_EXECUTION_REPORT.md/json
PER_UID_STATUS_TABLE.csv
PER_UID_TIMING_RESOURCE_TABLE.csv
FORMAL_ASSET_MUTATION_CHECK.json
STAGED_ASSET_MANIFEST.csv
ENVIRONMENT_AND_SOURCE_IDENTITY.md/json
per_uid/P0A434/*
per_uid/Q97VT7/*
scripts/run_paraoxon_stage_a_alphafill8_d4_feasibility.py
```

## 3. Teacher S1 requirement audit

| Teacher S1 requirement | Audit result | Evidence |
|---|---|---|
| Only `P0A434` / `Q97VT7` | PASS | `target_uids=["P0A434","Q97VT7"]`; per-UID dirs only for these two |
| D4 constructability check | PASS | ESM3B/GVP/pocket-node/loader reports for both UIDs |
| AlphaFill 8Å pocket | PASS | AlphaFill CIF/JSON 200 for both; `pocket_radius_angstrom=8.0` |
| ESM-2 3B | PASS | `model_name=esm2_t36_3B_UR50D`, `repr_layer=36`, `embedding_dim=2560` |
| GVP | PASS | GVP status PASS and staged `gvp_protein_feature_flat.pt` for both |
| Staged assets report | PASS | `STAGED_ASSET_MANIFEST.csv` and per-UID staged asset dirs |
| Do not modify pool | PASS | `production_pool_mutated=false` |
| Do not modify production D4 | PASS | formal mutation check `mutated=false` |
| Do not run model | PASS | `model_run_performed=false`; loader report says no inference/ranking/scoring |
| Do not claim validated case | PASS | `validation_claim_made=false`; forbidden claims explicitly avoided |

## 4. Per-UID technical result

| UID | UniProt status | AlphaFill | Pocket | ESM-2 3B | GVP | Loader | Final status |
|---|---|---|---:|---|---:|---|---|
| `P0A434` | reviewed Swiss-Prot | 200/200, 27 hits, 43 transplants | 24 residues, chain A | `[367,2560]`, seq `[2560]`, pocket `[24,2560]` | 24 nodes | dataset len 1, item0 constructed | `PASS_ALPHAFILL8_STAGED_D4_LOADER` |
| `Q97VT7` | reviewed Swiss-Prot | 200/200, 34 hits, 51 transplants | 39 residues, chain A | `[316,2560]`, seq `[2560]`, pocket `[39,2560]` | 39 nodes | dataset len 1, item0 constructed | `PASS_ALPHAFILL8_STAGED_D4_LOADER` |

The node shapes are consistent with the formal ESM-2 3B contract:

```text
P0A434 sequence length 365 -> node feature [365+2, 2560] = [367,2560]
Q97VT7 sequence length 314 -> node feature [314+2, 2560] = [316,2560]
```

Independent local checks without torch:

```text
P0A434 node npz: node_feature (367,2560), float32
Q97VT7 node npz: node_feature (316,2560), float32
P0A434 seq2feature: one canonical-sequence key, value (2560,), float32
Q97VT7 seq2feature: one canonical-sequence key, value (2560,), float32
P0A434 pocket PDB: chain A only, 24 standard residues, 0 HETATM
Q97VT7 pocket PDB: chain A only, 39 standard residues, 0 HETATM
```

Local torch was unavailable, so this audit did not independently reload `.torch.pt` / `.pt` tensors. The package-internal loader validation did call `load_geometric_dataset(...)` and constructed `dataset[0]` for both UIDs.

## 5. Fresh-run / non-reuse audit

The package contains fresh raw inputs:

```text
P0A434 raw UniProt JSON SHA256: 7a1fbe9244ba97ca2c25aace154a287703a298e1370d7b940fdacf4596d8824f
P0A434 raw AlphaFill CIF SHA256: 055d4b17d4d38f0eb15eed3beae2eaeea6b680f37624e2a459272dc1c7597733
P0A434 raw AlphaFill JSON SHA256: 2b2ce3e5917e8af4c6bcb62fada2df81a7aaacac00de3f14388f033f2d196214

Q97VT7 raw UniProt JSON SHA256: bd70dd6f59c550d3d70c04b433cd05b5827639a5fd735beae4ab6f8083bbe76e
Q97VT7 raw AlphaFill CIF SHA256: b20760e5501147f80f68bb348d93c4f1b5d284b802aec9ab0e5be66b33b6cd96
Q97VT7 raw AlphaFill JSON SHA256: 2799641772e6a0e895fc866c9a983d382444bfce9527b3f87d3ff9c2425d856f
```

The runner script uses `curl` to fetch UniProt/AlphaFill and then stages new assets under this rerun return directory. Grep review found no copying from previous P0A434/Q97VT7 staged asset directories.

Selected new-vs-old SHA256 comparison also supports that old staged assets were not directly copied:

| Asset | New rerun3 SHA256 | Old 2026-07-31 SHA256 | Same? |
|---|---|---|---|
| P0A434 ESM node npz | `bc89fe76d56da7425879bbd3ee09b8ec507bde0fad41b226c15d2894a5baf4e7` | `2507c0391d257a785040cc9094616b800d4affb936942479ec439e5cfd1709f0` | No |
| P0A434 pocket PDB | `05a5b16ad79f8b4baa4001e5353477f02d522229eb768dad217c2b4073065efb` | `24509cae07c6866f7a236d842927d0b5d6965c93203d491a96b31cb913d1e2f5` | No |
| Q97VT7 ESM node npz | `1b4458f859568fe7cca5630303ecc75117abc5cd9665cf51ddb0c9d9a61d835e` | `471c1b17188531923fae83c4792d6a576325dee6fe4a809fa898b43d771f62f0` | No |
| Q97VT7 pocket PDB | `7237c1d618146cb7f923bcdc8679b92307543434c5fe3ddbf78529d6e1a4c9e9` | `dbe55d420bffecc733fdf95dbbf6e2edcaa51a4db0751aa0ccd64e253f783ab4` | No |

## 6. Formal asset mutation audit

`FORMAL_ASSET_MUTATION_CHECK.json` reports:

```text
mutated=false
mutation_diffs={}
```

Before/after snapshots match for:

```text
FORMAL_SPLIT_TRAIN
FORMAL_SPLIT_VALID
FORMAL_SPLIT_TEST
FORMAL_RXN_FP
FORMAL_REACTION_CENTER
FORMAL_MOL_CONFORMATION
FORMAL_MOL2ID
FORMAL_GVP
FORMAL_SEQ2FEATURE
FORMAL_POCKET_ESM
```

This satisfies the no-production-mutation requirement.

## 7. Loader validation boundary

Both loader validations used a technical carrier reaction selected from `FORMAL_SPLIT_VALID` with source UID `F2K079`.

The package explicitly states:

```text
The carrier reaction is not a Paraoxon model scoring run.
No model inference/ranking/scoring is performed.
```

This is acceptable for S1 because the teacher asked for D4 constructability / staged assets, not a Paraoxon EnzymeCAGE ranking run.

## 8. Timing and resource audit

Reported per-UID wall times:

| UID | total wall sec | ESM3B sec | GVP sec | loader sec | peak GPU allocated |
|---|---:|---:|---:|---:|---:|
| `P0A434` | 65.08 | 31.41 | 3.18 | 1.51 | 11058 MB |
| `Q97VT7` | 37.44 | 30.65 | 0.018 | 1.01 | 11048 MB |

Caveat:

```text
PER_UID_TIMING_RESOURCE_TABLE.csv records pocket_node_sec equal to esm3b_compute_sec for both UIDs.
This appears to be a duplicated/ambiguous timing field rather than an independent extra stage.
Do not add esm3b_compute_sec + pocket_node_sec when summarizing runtime.
Use per_uid_total_wall_sec or the explicit ESM/GVP/loader fields.
```

This caveat does not invalidate constructability PASS.

## 9. Accepted teacher-facing wording

Safe wording:

```text
Paraoxon S1 Stage A staged D4 constructability passed for both authorized direct-evidence UIDs, P0A434 and Q97VT7.
Both were freshly processed through UniProt/AlphaFill live raw input, AlphaFill 8Å pocket extraction, corrected ESM-2 3B, GVP, pocket-node ESM, and isolated EnzymeCAGE loader feasibility.
No production pool or production D4 assets were modified, no model scoring was run, and this is not a Paraoxon validation claim.
```

Do not write:

```text
Paraoxon has been validated.
P0A434/Q97VT7 have been merged into production D4.
Route-B or Route-C pool has been updated.
EnzymeCAGE scored Paraoxon.
Stage A proves biological correctness.
```

## 10. Next recommended action

Proceed to S2 only after recording this S1 audit:

```text
S2 Paraoxon formal case draft should cite this S1 PASS,
but must still state Paraoxon B pool=0 and that the formal running surface will require C pool / prediction fallback as teacher specified.
```

Recommended next status:

```text
S1_ACCEPTED_TECHNICAL_PASS_BOTH_UIDS_READY_FOR_S2_DRAFT
```
