# Local audit: P2Rank fallback coverage pilot return

Date: 2026-08-03

Audited archive:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_single_enzyme_ondemand_d4_p2rank_fallback_coverage_pilot_20260803.tar.gz
```

Identity file:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_single_enzyme_ondemand_d4_p2rank_fallback_coverage_pilot_20260803.tar.gz.identity.txt
```

## 1. Verdict

Verdict: ACCEPT AS A TECHNICAL P2Rank PREDICTED-POCKET FALLBACK PILOT, with two interpretation caveats.

The package supports:

```text
On the same 100-UID missing-D4/missing-pocket sample used for the strict AlphaFill-transplant probe, the P2Rank predicted-pocket fallback produced 42 / 100 isolated loader-valid staged D4 assets, including 26 UIDs that had failed the strict AlphaFill route.
```

It does not support:

```text
claiming these assets are strict AlphaFill-transplant PASS_FULL_D4_LOADER;
production asset merge;
biological correctness of any UID for any target reaction;
claiming a pure AlphaFoldDB-only P2Rank route, because most structures were reused from baseline AlphaFill CIF files;
claiming no environment mutation at all, because the executor installed OpenJDK 17 via apt, although formal EnzymeCAGE assets were not mutated.
```

Recommended label:

```text
PASS_PREDICTED_POCKET_D4_LOADER
```

not:

```text
PASS_FULL_D4_LOADER
```

## 2. Package integrity

Local archive SHA256:

```text
ee522d2caccebd646210e3144e390d328a1796d92e3210c355d289b5146a7790
```

Identity file reports the same SHA256:

```text
archive_sha256=ee522d2caccebd646210e3144e390d328a1796d92e3210c355d289b5146a7790
```

Archive size:

```text
archive_bytes=28274973
```

Final status:

```text
M3_SINGLE_ENZYME_D4_P2RANK_FALLBACK_PILOT_COMPLETE_WITH_PASS_AND_BLOCKER_COUNTS
```

Internal manifest check:

```text
sha256sum -c MANIFEST.sha256: all listed files OK
```

## 3. Required file coverage

The required top-level evidence files are present:

```text
P2RANK_FALLBACK_PILOT_REPORT.md
P2RANK_FALLBACK_PILOT_REPORT.json
PER_UID_P2RANK_STATUS_TABLE.csv
PER_UID_P2RANK_TIMING_RESOURCE_TABLE.csv
STRICT_VS_P2RANK_COMPARISON_TABLE.csv
PASS_CONTROL_POCKET_OVERLAP_TABLE.csv
STRUCTURE_SOURCE_TABLE.csv
P2RANK_VERSION_AND_INSTALL_REPORT.txt
ENVIRONMENT_REPORT.txt
ENVIRONMENT_REMEDIATION_AUDIT.md/json
FINAL_STATUS.txt
MANIFEST.sha256
```

Table row counts:

| File | Rows |
|---|---:|
| `PER_UID_P2RANK_STATUS_TABLE.csv` | 100 |
| `PER_UID_P2RANK_TIMING_RESOURCE_TABLE.csv` | 100 |
| `STRICT_VS_P2RANK_COMPARISON_TABLE.csv` | 100 |
| `STRUCTURE_SOURCE_TABLE.csv` | 100 |
| `PASS_CONTROL_POCKET_OVERLAP_TABLE.csv` | 16 |

The 42 PASS UIDs each have the expected isolated asset files:

```text
pockets/pocket/<UID>.pdb
pockets/pocket_info.csv
esm3b/pocket_node_feature/esm_node_feature.torch.pt
esm3b/protein_level/seq2feature.pkl
gvp/gvp_protein_feature_flat.pt
validation_input.csv
```

No missing required isolated asset file was found among the 42 PASS UIDs.

## 4. Main result

Reported and independently re-counted status distribution:

| Final status | Count |
|---|---:|
| `PASS_PREDICTED_POCKET_D4_LOADER` | 42 |
| `BLOCKED_P2RANK_NO_POCKET` | 45 |
| `BLOCKED_STRUCTURE_FETCH_FAILED` | 12 |
| `BLOCKED_SEQUENCE_FETCH_TIMEOUT` | 1 |

Strict baseline distribution from the comparison table:

| Strict baseline status | Count |
|---|---:|
| `BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY` | 43 |
| `BLOCKED_ALPHAFILL_404` | 20 |
| `BLOCKED_POCKET_EXTRACTION_EMPTY_OR_INVALID` | 17 |
| `PASS_FULL_D4_LOADER` | 16 |
| `BLOCKED_SEQUENCE_MISSING` | 4 |

P2Rank PASS by strict baseline status:

| Strict baseline status | P2Rank PASS |
|---|---:|
| `PASS_FULL_D4_LOADER` | 16 |
| `BLOCKED_POCKET_EXTRACTION_EMPTY_OR_INVALID` | 10 |
| `BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY` | 8 |
| `BLOCKED_ALPHAFILL_404` | 8 |

Therefore:

```text
strict route PASS = 16 / 100
P2Rank predicted-pocket route PASS = 42 / 100
net additional rescue from strict failures = 26 / 100
```

## 5. Recovery by stratum

Recovered-from-strict-failure counts:

| Baseline stratum | Recovered by P2Rank |
|---|---:|
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 10 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 9 |
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 7 |

Interpretation:

```text
P2Rank materially improves coverage, especially for UIDs where strict AlphaFill either lacked usable transplant metadata, had 404 under the strict endpoint, or had transplant metadata but failed the original pocket extractor.
```

The old-pool-with-pocket stratum is especially informative because the previous strict 100-UID audit had 10 failures in that stratum; this run recovered 10 UIDs from that stratum.

## 6. Structure-source interpretation

Structure source distribution:

| Structure source | Count |
|---|---:|
| `baseline_alphafill_cif` | 76 |
| `alphafolddb_api_pdb` | 8 |
| `live_alphafill_cif` | 3 |
| blank / unavailable | 13 |

P2Rank status by structure source:

| Structure source | Status | Count |
|---|---|---:|
| `baseline_alphafill_cif` | `PASS_PREDICTED_POCKET_D4_LOADER` | 34 |
| `baseline_alphafill_cif` | `BLOCKED_P2RANK_NO_POCKET` | 42 |
| `alphafolddb_api_pdb` | `PASS_PREDICTED_POCKET_D4_LOADER` | 8 |
| `live_alphafill_cif` | `BLOCKED_P2RANK_NO_POCKET` | 3 |
| blank | `BLOCKED_STRUCTURE_FETCH_FAILED` | 12 |
| blank | `BLOCKED_SEQUENCE_FETCH_TIMEOUT` | 1 |

Important caveat:

```text
This is not a pure "AlphaFoldDB download for all UIDs + P2Rank" experiment.
```

The executor reused baseline AlphaFill CIF protein coordinates when available and only used AlphaFoldDB API PDB for 8 UIDs. This is acceptable for testing an agent-side "use available 3D structure + P2Rank" fallback, but a strict author-style AF2-only comparison would require a separate rerun that forces AlphaFoldDB structure acquisition first.

## 7. P2Rank execution evidence

P2Rank version:

```text
P2Rank 2.5.1
```

Package source:

```text
https://github.com/rdk/p2rank/releases/download/2.5.1/p2rank_2.5.1.tar.gz
```

Archive SHA256:

```text
d243f2d9036ac053fefb9407b5fe1c85f4fe077c519fd975ac585e995feab274
```

P2Rank ran with the AlphaFold config:

```text
prank predict -threads 4 -c alphafold -visualizations 0 ...
```

The package records that a previous incorrect direct-PDB invocation was corrected to per-UID `.ds` dataset files before full 100-UID execution.

Blocked example check:

```text
B2GKN0: structure parsed, P2Rank ran, but LIGANDABLE POINTS: 0 and no residues were assigned to top-ranked pocket.
```

This supports that `BLOCKED_P2RANK_NO_POCKET` is a real fail-closed pocket prediction/mapping blocker, not simply "P2Rank was not run".

## 8. Loader and feature evidence

For a representative recovered UID, `B9SIL7`, the per-UID report records:

```text
structure_source=alphafolddb_api_pdb
p2rank_status=PASS
p2rank_pocket_residue_count=35
model_name=esm2_t36_3B_UR50D
feature_dim=2560
node_feature_shape=[780, 2560]
pocket_node_feature_shape=[35, 2560]
gvp_node_count=35
load_geometric_dataset_called=True
dataset_len=1
dataset0_constructed=True
loader_validation_status=PASS
final_status=PASS_PREDICTED_POCKET_D4_LOADER
```

This is credible isolated loader eligibility evidence for predicted-pocket assets.

## 9. Pocket semantic drift

The package includes 16 strict-PASS controls comparing strict AlphaFill pockets against P2Rank pockets.

Jaccard overlap summary:

| Metric | Value |
|---|---:|
| rows | 16 |
| mean Jaccard | 0.451 |
| median Jaccard | 0.414 |
| min | 0.350 |
| max | 0.621 |

Interpretation:

```text
P2Rank predicted pockets often overlap with strict AlphaFill pockets, but they are not identical and should not be silently treated as the same pocket evidence class.
```

This supports keeping P2Rank as a separate lower-evidence fallback tier unless the teacher explicitly authorizes merging predicted-pocket semantics into formal D4.

## 10. Timing and resource summary

All 100 UIDs:

| Stage | Mean sec | Median sec | Max sec |
|---|---:|---:|---:|
| total wall | 7.78 | 6.16 | 60.10 |
| structure fetch | 2.08 | 0.20 | 27.04 |
| P2Rank | 3.74 | 3.95 | 13.11 |
| ESM-2 3B | 0.44 | 0.00 | 37.02 |
| GVP | 0.24 | 0.00 | 3.64 |
| loader validation | 0.53 | 0.00 | 1.77 |

For the 42 PASS UIDs:

| Stage | Mean sec | Median sec | Max sec |
|---|---:|---:|---:|
| total wall | 9.13 | 6.70 | 48.38 |
| structure fetch | 1.60 | 0.32 | 10.43 |
| P2Rank | 4.49 | 4.37 | 6.01 |
| ESM-2 3B | 1.05 | 0.17 | 37.02 |
| GVP | 0.58 | 0.47 | 3.64 |
| loader validation | 1.26 | 1.25 | 1.77 |

Resource caveat:

```text
process_max_rss_mb and GPU peak values are process/run-level observations and can be influenced by previous per-UID work in the same process. They should be treated as practical execution footprint indicators, not clean per-UID cold-start measurements.
```

## 11. Environment and scope caveats

The package reports:

```text
formal_assets_mutated=false
```

Formal asset snapshots before/after show unchanged size and mtime for the tracked formal EnzymeCAGE assets.

However, the executor also reports environment remediations:

```text
installed_openjdk_17_jre_headless_via_apt
downloaded_p2rank_2_5_1_to_work_root_tools
corrected_p2rank_invocation_to_dataset_file
cleaned_current_run_partial_per_uid_outputs_after_failed_smoke
```

Audit interpretation:

```text
No formal EnzymeCAGE asset mutation is evidenced.
But the run did modify the execution environment by installing Java 17 via apt.
Future toolization should either preinstall Java/P2Rank in the chenyu environment or use an isolated JRE under WORK_ROOT, so the tool does not need system-level package installation.
```

The cleanup note appears limited to current-task generated `per_uid/isolated_assets` after a failed smoke invocation. It does not evidence production asset deletion, but future prompts should define this more explicitly.

## 12. Recommended teacher-facing conclusion

Suggested wording:

```text
We reran the same 100-UID missing-D4 sample with a P2Rank predicted-pocket fallback. The strict AlphaFill-transplant route had recovered 16/100 UIDs. The P2Rank fallback produced 42/100 isolated loader-valid staged D4 assets, including 26 UIDs that strict AlphaFill had failed to recover. This strongly suggests that a UID-only on-demand D4 tool should not rely only on AlphaFill transplant pockets. However, the strict AlphaFill and P2Rank pockets are not semantically identical: among 16 strict-PASS controls, pocket-residue Jaccard overlap had mean 0.451 and median 0.414. Therefore P2Rank should be reported as a predicted-pocket fallback tier, not merged with strict AlphaFill PASS unless authorized.
```

Recommended next action:

```text
Keep the result as evidence for adding a P2Rank fallback branch to the on-demand D4 backfill tool. If the teacher wants exact alignment with the inferred original mix-af-p2rank pipeline, run one additional forced AlphaFoldDB-only + P2Rank control, because this run mostly reused baseline AlphaFill CIF structures as available protein 3D sources.
```

