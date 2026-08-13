# Local audit: M4 E2 cache-miss one-UID smoke bounded fallback return

Date: 2026-08-13

Audited archive:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_cache_miss_one_uid_smoke_bounded_fallback_20260813.tar.gz
```

External identity:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_cache_miss_one_uid_smoke_bounded_fallback_20260813.tar.gz.identity.txt
```

Prompt:

```text
07_HPC_Prompts/
HPC_ENZYMECAGE_M4_E2_CACHE_MISS_ONE_UID_SMOKE_BOUNDED_FALLBACK_EXECUTOR_ONLY_PROMPT_2026-08-13.md
```

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_PROJECT_NEXT_STEPS_GUIDANCE_2026-08-13.md
```

Input candidate preflight:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_e2_cache_miss_smoke_candidate_preflight_20260813.tar.gz
```

## 1. Verdict

Verdict:

```text
LOCAL_AUDIT_PASS_AS_M4_E2_ONE_UID_CACHE_MISS_STAGED_ONLY_SMOKE
```

The return supports the narrow claim that one cache-miss UID smoke completed:

```text
A3CST9
```

The accurate plain-language interpretation is:

```text
Chenyu tried the first candidate in the audited fallback queue, A3CST9. It
passed the AFDB -> P2Rank predicted pocket -> ESM-2 3B staged feature -> same
pocket GVP staged feature -> isolated D4 loader validation path. Because
stop_after_first_pass=true, the other fallback candidates were not attempted.
```

This audit does not claim:

```text
full 4,681 backfill was run;
production D4 assets were merged or mutated;
production pool assets were mutated;
model inference, ranking, or scoring was performed;
P2Rank predicted pockets are equivalent to strict AlphaFill pockets.
```

## 2. Archive identity and integrity

Local archive SHA256:

```text
8573bd4524934f795dea035204ffb06815e0f937b7f2df6c2345319bd88d62ff
```

External identity reported archive SHA256:

```text
8573bd4524934f795dea035204ffb06815e0f937b7f2df6c2345319bd88d62ff
```

Local archive bytes:

```text
1379633
```

External identity reported archive bytes:

```text
1379633
```

Internal manifest check:

```text
sha256sum -c MANIFEST.sha256:
  all listed files OK
```

Compared with the earlier candidate-preflight package, this returned package
does not have the manifest self-inclusion failure.

## 3. Final status recount

Identity final status:

```text
M4_E2_CACHE_MISS_ONE_UID_SMOKE_COMPLETE_WITH_ONE_PASS_AND_ATTEMPT_LOG
```

`FINAL_STATUS.txt`:

```text
M4_E2_CACHE_MISS_ONE_UID_SMOKE_COMPLETE_WITH_ONE_PASS_AND_ATTEMPT_LOG
```

Identity summary:

| Field | Value |
|---|---:|
| `attempt_queue` | `A3CST9,B8GGQ9,A7I9P9,A0A0H2V760,P0DXZ0` |
| `attempted_uids` | `A3CST9` |
| `pass_uid` | `A3CST9` |
| `n_attempted` | 1 |
| `n_pass` | 1 |
| `n_blocked` | 0 |
| `n_skipped` | 0 |
| `stop_after_first_pass` | true |
| `staged_smoke_assets_generated` | true |
| `formal_assets_mutated` | false |
| `production_pool_mutated` | false |
| `full_4681_backfill_run` | false |
| `production_d4_mutated` | false |

`ATTEMPT_STATUS_TABLE.csv` recount:

| UID | Final status |
|---|---|
| `A3CST9` | `PASS_CACHE_MISS_AFDB_P2RANK_PREDICTED_POCKET_STAGED_D4_LOADER_SMOKE` |
| `B8GGQ9` | `NOT_ATTEMPTED_STOP_AFTER_PRIOR_PASS` |
| `A7I9P9` | `NOT_ATTEMPTED_STOP_AFTER_PRIOR_PASS` |
| `A0A0H2V760` | `NOT_ATTEMPTED_STOP_AFTER_PRIOR_PASS` |
| `P0DXZ0` | `NOT_ATTEMPTED_STOP_AFTER_PRIOR_PASS` |

Interpretation:

```text
The user observation "第一次就找到了那个酶" is supported if phrased as:
"the first attempted candidate A3CST9 produced the requested one-UID smoke PASS."
It should not be phrased as all candidates were tested or that all are usable.
```

## 4. A3CST9 pass evidence

Per-UID report:

```text
per_uid/A3CST9/REPORT.json
```

Key facts:

| Check | Evidence |
|---|---|
| Local sequence present | `True` |
| Sequence length | `398` |
| Pre-attempt ESM-2 3B cache status | `cache_miss` |
| Pre-attempt pocket-node cache status | `cache_miss` |
| Pre-attempt GVP cache status | `cache_miss` |
| AFDB URL | `https://alphafold.ebi.ac.uk/files/AF-A3CST9-F1-model_v6.pdb` |
| AFDB HTTP status | `200` |
| AFDB model version | `v6` |
| AFDB parser status | `PASS` |
| Selected chain | `A` |
| P2Rank status | `PASS_TOP_POCKET_MAPPED` |
| P2Rank version | `P2Rank 2.5.1` |
| P2Rank top pocket rank | `1` |
| P2Rank top pocket score | `118.99` |
| Final mapped pocket residue count | `85` |
| ESM-2 3B status | `PASS` |
| ESM node feature shape | `[85, 2560]` |
| GVP status | `PASS` |
| Same pocket for ESM node and GVP | `True` |
| Loader validation called | `True` |
| Loader validation status | `PASS` |
| Loader dataset length | `1` |
| Loader `dataset[0]` constructed | `True` |

P2Rank command:

```text
/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1/prank predict -threads 4 -c alphafold -visualizations 0 ...
```

Important count note:

```text
The earlier candidate preflight table reported predicted_residues=302 for
A3CST9. In this final smoke package, the mapped top-pocket residue count used
for staged feature generation is 85, and the ESM node feature shape is
[85, 2560]. Use 85 as the final smoke evidence count.
```

## 5. Staged smoke assets

`STAGED_SMOKE_ASSET_MANIFEST.csv` lists the required A3CST9 staged smoke assets,
all with `exists=True`:

```text
staged_smoke_assets/A3CST9/pockets/pocket/A3CST9.pdb
staged_smoke_assets/A3CST9/pockets/pocket_info.csv
staged_smoke_assets/A3CST9/esm3b/protein_level/seq2feature.pkl
staged_smoke_assets/A3CST9/esm3b/pocket_node_feature/esm_node_feature.torch.pt
staged_smoke_assets/A3CST9/gvp/gvp_protein_feature_flat.pt
staged_smoke_assets/A3CST9/validation_input.csv
```

The package also includes GVP intermediate evidence:

```text
staged_smoke_assets/A3CST9/gvp/input/A3CST9.pdb
staged_smoke_assets/A3CST9/gvp/tmp/A3CST9.pt
```

These are staged smoke assets only. They are not evidence of production D4
merge.

## 6. Loader validation boundary

`LOADER_VALIDATION_REPORT.json` confirms:

| Field | Value |
|---|---:|
| `loader_validation_called` | true |
| `loader_validation_pass` | true |
| `pass_uid` | `A3CST9` |
| `dataset_len` for A3CST9 | 1 |
| `dataset0_constructed` for A3CST9 | true |
| `protein_level_feature_loaded_from_staged_smoke` | true |
| `pocket_node_feature_loaded_from_staged_smoke` | true |
| `gvp_feature_loaded_from_staged_smoke` | true |

The script validates the staged smoke feature route by calling
`load_geometric_dataset` with:

```text
data_path=staged_smoke_assets/A3CST9/validation_input.csv
protein_gvp_feat=<loaded staged GVP feature>
esm_node_feature=<loaded staged pocket-node feature>
esm_mean_feature_path=staged_smoke_assets/A3CST9/esm3b/protein_level/seq2feature.pkl
formal reaction feature paths read from existing formal assets
```

Boundary note from the report:

```text
Technical EnzymeCAGE loader feasibility check. No model inference/ranking/scoring
is performed.
```

## 7. Safety and mutation audit

`FORMAL_ASSET_MUTATION_CHECK.json` reports:

| Field | Value |
|---|---:|
| `formal_feature_root_mutated` | false |
| `formal_split_root_mutated` | false |
| `formal_model_root_mutated` | false |
| `production_data_root_mutated` | false |
| `production_dataset_root_mutated` | false |

Script-path inspection supports the same boundary:

```text
Generated protein/pocket/GVP outputs are written under RETURN_DIR/staged_smoke_assets/A3CST9.
Formal split/reaction assets are opened for loader validation input only.
The report flags production ESM and GVP cache mutation as false.
```

## 8. Runtime and environment

Environment:

| Item | Evidence |
|---|---|
| Python | `3.12.3` |
| Torch | `2.7.1+cu126` |
| CUDA available | `True` |
| GPU | `NVIDIA GeForce RTX 4090 D` |
| Java | `17.0.19` |
| P2Rank | `2.5.1` |
| ESM import | `OK` |
| Bio.PDB import | `OK` |

Timing/resource for A3CST9:

| Stage | Seconds |
|---|---:|
| cache check | 0.093 |
| sequence fetch | 0.155 |
| AFDB structure fetch | 3.824 |
| P2Rank | 4.248 |
| ESM-2 3B | 33.805 |
| GVP | 3.347 |
| loader validation | 2.029 |
| total wall time | 47.573 |

Peak GPU allocated:

```text
11065 MB
```

## 9. Residual risks and wording constraints

Allowed wording:

```text
One cache-miss UID smoke passed on A3CST9 using staged-only generated assets.
The first candidate in the audited queue passed, so fallbacks were not attempted.
This demonstrates the technical route for one missing-asset UID under the
bounded M4 E2 smoke scope.
```

Do not say:

```text
M4 production D4 backfill is complete.
All 4,681 missing-pocket UIDs are backfilled.
The production D4 loader passed for the full dataset.
P2Rank proves a ligand/AlphaFill pocket.
The remaining fallback candidates were tested.
```

Residual risk:

```text
The PASS is a technical smoke validation on one UID, not a biological
performance result. The pocket is P2Rank-predicted and lower-evidence than a
strict AlphaFill pocket. Full-scale backfill and production merge still require
separate authorization.
```
