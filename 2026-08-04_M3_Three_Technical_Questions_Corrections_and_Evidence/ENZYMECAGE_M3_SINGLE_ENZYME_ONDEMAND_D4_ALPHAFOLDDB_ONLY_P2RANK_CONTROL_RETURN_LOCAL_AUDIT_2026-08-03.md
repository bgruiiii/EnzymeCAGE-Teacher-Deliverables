# Local audit: AlphaFoldDB-only P2Rank control return

Date: 2026-08-03

Audited archive:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_single_enzyme_ondemand_d4_alphafolddb_only_p2rank_control_20260803.tar.gz
```

Identity file:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_single_enzyme_ondemand_d4_alphafolddb_only_p2rank_control_20260803.tar.gz.identity.txt
```

## 1. Verdict

Verdict: ACCEPT AS A COMPLETED ALPHAFOLDDB-ONLY P2RANK PREDICTED-POCKET CONTROL, with interpretation caveats.

The package supports:

```text
On the same 100-UID missing-D4/missing-pocket sample, forcing AlphaFoldDB protein structures followed by P2Rank predicted-pocket staging produced 45 / 100 isolated loader-valid staged D4 assets, including 29 UIDs that had failed the strict AlphaFill-transplant route.
```

It does not support:

```text
claiming AlphaFoldDB-only P2Rank assets are strict AlphaFill-transplant PASS_FULL_D4_LOADER;
production asset merge;
biological correctness of any UID for any target reaction;
claiming P2Rank predicted pockets are semantically identical to strict AlphaFill ligand-neighbor pockets.
```

Recommended PASS label:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER
```

not:

```text
PASS_FULL_D4_LOADER
```

## 2. Package integrity

Local archive SHA256:

```text
cf689b2429b40788da77daf6fe08d66a331f432c7a4f40fd7e48f22b733ab6ea
```

Identity file reports the same SHA256:

```text
archive_sha256=cf689b2429b40788da77daf6fe08d66a331f432c7a4f40fd7e48f22b733ab6ea
```

Archive size:

```text
archive_bytes=29169582
```

Final status:

```text
M3_SINGLE_ENZYME_D4_AFDB_ONLY_P2RANK_CONTROL_COMPLETE_WITH_PASS_AND_BLOCKER_COUNTS
```

Internal manifest check:

```text
sha256sum -c MANIFEST.sha256: all listed files OK
```

## 3. Required file coverage

The required evidence files are present:

```text
AFDB_ONLY_P2RANK_CONTROL_REPORT.md
AFDB_ONLY_P2RANK_CONTROL_REPORT.json
AFDB_ONLY_P2RANK_STATUS_TABLE.csv
AFDB_ONLY_P2RANK_TIMING_RESOURCE_TABLE.csv
STRICT_VS_AFDB_ONLY_P2RANK_COMPARISON_TABLE.csv
MIXED_P2RANK_VS_AFDB_ONLY_P2RANK_COMPARISON_TABLE.csv
AFDB_STRUCTURE_SOURCE_TABLE.csv
AFDB_ONLY_PASS_CONTROL_POCKET_OVERLAP_TABLE.csv
P2RANK_VERSION_AND_INSTALL_REPORT.txt
ENVIRONMENT_REPORT.txt
ENVIRONMENT_REMEDIATION_AUDIT.md/json
FINAL_STATUS.txt
MANIFEST.sha256
```

Table row counts:

| File | Rows |
|---|---:|
| `AFDB_ONLY_P2RANK_STATUS_TABLE.csv` | 100 |
| `AFDB_ONLY_P2RANK_TIMING_RESOURCE_TABLE.csv` | 100 |
| `STRICT_VS_AFDB_ONLY_P2RANK_COMPARISON_TABLE.csv` | 100 |
| `MIXED_P2RANK_VS_AFDB_ONLY_P2RANK_COMPARISON_TABLE.csv` | 100 |
| `AFDB_STRUCTURE_SOURCE_TABLE.csv` | 100 |
| `AFDB_ONLY_PASS_CONTROL_POCKET_OVERLAP_TABLE.csv` | 16 |

The 45 PASS UIDs each have the expected isolated files:

```text
pockets/pocket/<UID>.pdb
pockets/pocket_info.csv
esm3b/pocket_node_feature/esm_node_feature.torch.pt
esm3b/protein_level/seq2feature.pkl
gvp/gvp_protein_feature_flat.pt
validation_input.csv
```

No missing required isolated asset file was found among the 45 PASS UIDs.

## 4. Main result

Reported and independently re-counted status distribution:

| Final status | Count |
|---|---:|
| `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 45 |
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | 43 |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | 12 |

Structure acquisition:

| AlphaFoldDB structure status | Count |
|---|---:|
| `PASS` | 88 |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | 12 |

All 88 successful structure URLs point to AlphaFoldDB:

```text
non-AlphaFoldDB URL count=0
```

Version/source distribution among successful AFDB URLs:

| AFDB model URL version | Count |
|---|---:|
| `v6` | 85 |
| `v1` | 3 |

## 5. Comparison with strict AlphaFill route

Strict baseline:

```text
PASS_FULL_D4_LOADER = 16 / 100
```

AlphaFoldDB-only P2Rank:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER = 45 / 100
```

Strict-failure recovery:

```text
n_recovered_from_strict_failure = 29 / 100
```

PASS by strict baseline status:

| Strict AlphaFill baseline status | AFDB-only P2Rank PASS |
|---|---:|
| `PASS_FULL_D4_LOADER` | 16 |
| `BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY` | 10 |
| `BLOCKED_POCKET_EXTRACTION_EMPTY_OR_INVALID` | 10 |
| `BLOCKED_ALPHAFILL_404` | 9 |
| `BLOCKED_SEQUENCE_MISSING` | 0 |

Blocked by strict baseline status:

| AFDB-only blocker | Strict AlphaFill baseline status | Count |
|---|---|---:|
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | `BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY` | 33 |
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | `BLOCKED_POCKET_EXTRACTION_EMPTY_OR_INVALID` | 7 |
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | `BLOCKED_SEQUENCE_MISSING` | 3 |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | `BLOCKED_ALPHAFILL_404` | 11 |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | `BLOCKED_SEQUENCE_MISSING` | 1 |

Interpretation:

```text
AlphaFoldDB-only P2Rank improves coverage over strict AlphaFill. It recovers UIDs from all three major strict blockers: AlphaFill hits/transplants missing, strict pocket extraction failure, and AlphaFill 404.
```

## 6. Comparison with previous mixed-structure P2Rank fallback

Previous mixed-structure P2Rank fallback:

```text
PASS_PREDICTED_POCKET_D4_LOADER = 42 / 100
recovered_from_strict_failure = 26 / 100
```

AlphaFoldDB-only P2Rank:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER = 45 / 100
recovered_from_strict_failure = 29 / 100
```

Delta:

```text
AFDB-only rescued 5 previous mixed-P2Rank failures.
AFDB-only lost 2 previous mixed-P2Rank PASS UIDs.
Net PASS gain = +3.
```

AFDB-only rescued previous mixed failures:

| UID | Mixed result | AFDB-only result | AFDB-only pocket residues |
|---|---|---|---:|
| `Q21882` | `BLOCKED_P2RANK_NO_POCKET` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 7 |
| `Q31YI2` | `BLOCKED_P2RANK_NO_POCKET` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 6 |
| `A9P2J1` | `BLOCKED_P2RANK_NO_POCKET` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 3 |
| `P41476` | `BLOCKED_STRUCTURE_FETCH_FAILED` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 31 |
| `P49328` | `BLOCKED_P2RANK_NO_POCKET` | `PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER` | 67 |

AFDB-only lost previous mixed PASS:

| UID | Mixed result | AFDB-only result | Mixed structure source |
|---|---|---|---|
| `Q55842` | `PASS_PREDICTED_POCKET_D4_LOADER` | `BLOCKED_AFDB_P2RANK_NO_POCKET` | `baseline_alphafill_cif` |
| `Q74ES0` | `PASS_PREDICTED_POCKET_D4_LOADER` | `BLOCKED_AFDB_P2RANK_NO_POCKET` | `baseline_alphafill_cif` |

Interpretation:

```text
AFDB-only is slightly better on this 100-UID sample, but not strictly dominant per UID. A future agent should probably support both: prefer a clean AlphaFoldDB+P2Rank route for reproducible predicted-pocket fallback, while retaining the option to use other trusted structure sources when AFDB-only fails or gives no pocket.
```

## 7. Recovery by stratum

PASS by baseline stratum:

| Baseline stratum | AFDB-only PASS | Total |
|---|---:|---:|
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 25 | 25 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 12 | 40 |
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 8 | 35 |

Blocked by stratum:

| Blocker | Stratum | Count |
|---|---|---:|
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 27 |
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 16 |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 12 |

Interpretation:

```text
The old-pool-with-pocket stratum is fully recovered by AFDB-only P2Rank in this sample. The remaining hard cases are concentrated in AlphaFill-success-no-pocket and old-pool-without-pocket strata.
```

## 8. Failure causes

Remaining failures:

| Failure class | Count | Meaning |
|---|---:|---|
| `BLOCKED_AFDB_P2RANK_NO_POCKET` | 43 | AlphaFoldDB structure was obtained and parsed, but P2Rank did not produce a top pocket with usable mapped residues |
| `BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` | 12 | AlphaFoldDB API and conventional v6/v5/v4 PDB/mmCIF attempts failed |

AFDB structure failure UIDs:

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

Representative structure-failure example:

```text
Q9Z0D5: AlphaFoldDB API returned 404, and conventional v6/v5/v4 PDB/mmCIF URLs all returned 404.
```

Representative no-pocket example:

```text
Q55842: AlphaFoldDB v6 PDB downloaded and parsed, P2Rank ran successfully, but it produced no filtered top pocket with mapped residues. This UID had passed in the previous mixed-structure run using baseline_alphafill_cif, so pocket prediction can be structure-source sensitive.
```

## 9. P2Rank and loader evidence

P2Rank environment:

```text
P2Rank 2.5.1
OpenJDK 17.0.19
P2Rank reused from the previous P2Rank fallback pilot
```

No new apt install was reported in this control:

```text
reused_openjdk_17_from_previous_p2rank_pilot
reused_p2rank_2_5_1_from_previous_p2rank_pilot
used_per_uid_ds_dataset_file_invocation
```

Representative PASS UID `P41476`:

```text
afdb_structure_url=https://alphafold.ebi.ac.uk/files/AF-0000000365760670-model_v1.pdb
p2rank_status=PASS
p2rank_pocket_residue_count=31
model_name=esm2_t36_3B_UR50D
feature_dim=2560
node_feature_shape=[696, 2560]
pocket_node_feature_shape=[31, 2560]
gvp_node_count=31
load_geometric_dataset_called=True
dataset_len=1
dataset0_constructed=True
loader_validation_status=PASS
final_status=PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER
```

This supports isolated predicted-pocket D4 loader eligibility.

## 10. Pocket semantic drift

For the 16 strict AlphaFill PASS controls, AFDB-only P2Rank pocket overlap with strict AlphaFill pockets:

| Metric | Value |
|---|---:|
| rows | 16 |
| mean Jaccard | 0.340 |
| median Jaccard | 0.365 |
| min | 0.037 |
| max | 0.662 |

Comparison:

```text
previous mixed P2Rank mean Jaccard against strict controls ≈ 0.451
AFDB-only P2Rank mean Jaccard against strict controls ≈ 0.340
```

Interpretation:

```text
AFDB-only P2Rank gives slightly better coverage than mixed-structure P2Rank in this sample, but its pockets drift further from strict AlphaFill ligand-neighbor pockets. This strengthens the need to keep predicted-pocket D4 as a separate evidence tier.
```

## 11. Timing and resource summary

All 100 UIDs:

| Stage | Mean sec | Median sec | Max sec |
|---|---:|---:|---:|
| total wall | 13.76 | 9.49 | 89.58 |
| AFDB structure fetch | 8.81 | 4.26 | 83.52 |
| P2Rank | 3.51 | 3.82 | 5.14 |
| ESM-2 3B | 0.45 | 0.00 | 37.03 |
| GVP | 0.26 | 0.00 | 3.57 |
| loader validation | 0.54 | 0.00 | 1.94 |

For the 45 PASS UIDs:

| Stage | Mean sec | Median sec | Max sec |
|---|---:|---:|---:|
| total wall | 16.34 | 11.07 | 89.58 |
| AFDB structure fetch | 9.11 | 4.57 | 83.52 |
| P2Rank | 4.28 | 4.22 | 5.14 |
| ESM-2 3B | 1.01 | 0.18 | 37.03 |
| GVP | 0.58 | 0.49 | 3.57 |
| loader validation | 1.20 | 1.23 | 1.94 |

Resource observations:

```text
gpu_name=NVIDIA GeForce RTX 4090 D
gpu_peak_allocated_mb_max=11244
gpu_peak_reserved_mb_max=11760
process_max_rss_mb_max=16723.3359375
```

Caveat:

```text
GPU and process RSS values are practical run-level observations, not clean cold-start per-UID resource measurements.
```

## 12. Asset mutation and safety

The package reports:

```text
formal_assets_mutated=false
```

Formal asset snapshots before/after show unchanged tracked size and mtime for the formal EnzymeCAGE assets.

Interpretation:

```text
No formal EnzymeCAGE asset mutation is evidenced.
```

Environment note:

```text
This control reused OpenJDK 17 and P2Rank from the previous pilot. It did not report a new apt installation.
```

## 13. Recommended teacher-facing conclusion

Suggested wording:

```text
We ran a strict AlphaFoldDB-only + P2Rank control on the same 100 missing-D4 UIDs. Compared with the strict AlphaFill-transplant route, which recovered 16/100 UIDs, AlphaFoldDB-only P2Rank produced 45/100 isolated loader-valid predicted-pocket D4 assets and recovered 29 strict-failure UIDs. It also slightly exceeded the previous mixed-structure P2Rank fallback, which recovered 42/100. However, predicted pockets are not identical to strict AlphaFill ligand-neighbor pockets: for 16 strict-PASS controls, AFDB-only P2Rank pocket Jaccard overlap had mean 0.340 and median 0.365. Therefore the recommended agent-side route is to keep strict AlphaFill as the highest-evidence path, and add AlphaFoldDB + P2Rank as a lower-evidence predicted-pocket fallback tier with explicit provenance and evidence labels.
```

Recommended next technical follow-up:

```text
Inspect a small number of remaining failures:
1. AFDB structure 404 cases, to decide whether they are obsolete/viral/special UniProt entries or require a different structure source.
2. AFDB_P2RANK_NO_POCKET cases, to determine whether they are very short proteins, low-confidence/disordered AFDB models, non-enzyme-like entries, or P2Rank threshold/model limitations.
```

