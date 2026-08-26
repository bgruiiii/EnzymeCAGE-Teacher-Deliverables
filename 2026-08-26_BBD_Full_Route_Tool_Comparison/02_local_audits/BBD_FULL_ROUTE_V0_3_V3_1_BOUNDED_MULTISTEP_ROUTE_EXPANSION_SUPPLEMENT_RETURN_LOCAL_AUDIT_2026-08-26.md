# Local audit — BBD full-route v0.3 v3.1 bounded multistep route-expansion supplement

Date: 2026-08-26  
Audited archive:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz
```

Local restricted scoring reference used only during this local audit:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/21_BBD_Known_Pathway_Full_Route_Testset_2026-08-21/bbd_known_pathway_full_route_v0_3_candidate_v3_repair_20260821/restricted
```

## 1. Bottom-line verdict

Executor / blind-boundary compliance:

```text
PASS_WITH_MINOR_PACKAGING_ISSUE
```

Bounded multistep route graph execution:

```text
PASS_FOR_EDGE_AND_NODE_LEVEL_MULTISTEP_EXPANSION
```

Path-file / full route reconstruction readiness:

```text
PARTIAL
```

Plain-language conclusion:

```text
This return did move beyond one-step prediction. It contains bounded multistep expansion graphs for BioTransformer ENVMICRO, enviPath BBD Rules, ECLIPSE PREDEC, and optional ECLIPSE NoEC.

However, it should be described as "bounded multistep route-graph prediction to depth <= 6", not as complete mineralization and not as fully validated end-to-end degradation routes. The PREDICTED_ROUTE_PATHS files, especially for ECLIPSE, contain many repeated-node / repeated-edge paths, so path-level scoring should not rely on those files directly. Local scoring should use PREDICTED_ROUTE_EDGES + PREDICTED_ROUTE_NODES and reconstruct clean graph paths if needed.
```

Therefore this package is usable for:

```text
multi-step predicted node recovery
multi-step predicted edge recovery
terminal-node recovery as a graph-node diagnostic
tool comparison at bounded depth <= 6
```

But it is not yet sufficient for:

```text
claiming complete degradation to harmless/mineralized products
claiming all returned PREDICTED_ROUTE_PATHS are chemically valid simple routes
using path_depth directly as true biological route length without cleanup
```

## 2. Archive identity and manifest check

Archive SHA256:

```text
ee8e06fffe76bec29825702c18deb1211e33b7c4609ff3132be8428179fe83cf
```

Executor final status:

```text
COMPLETE_BOUNDED_MULTISTEP_ROUTE_EXPANSION_READY_FOR_LOCAL_SCORING
```

Manifest check result:

```text
sha256sum -c MANIFEST.sha256
```

All major result files passed, but one log file failed:

```text
logs/packaging.log: FAILED
```

Expected / actual hashes:

```text
MANIFEST.sha256: 7e9ba5e697deaa51c1bb04fe4d624808406703818a7d3471b9fdb6b079b3e513  logs/packaging.log
Actual:          2b026be1345f0939672b886250e212e331a2209fdbb833d41762c626a871b286
```

Interpretation:

```text
This looks like a packaging-log append-after-manifest issue. It does not invalidate the prediction result files, but it is a package-integrity hygiene issue and should be fixed in future returns.
```

## 3. Input and blind-boundary audit

Strict blind input identity reported by executor:

```text
strict_blind_rows=93
archive_sha256_match=true
blind_csv_sha256_match=true
blind_csv_sha256=be11658b0ede11093bb8bb833281994cb2f507629eaf7b3524de74a4e46acb66
restricted_answer_key_read=false
input_audit_pass=true
```

Previous one-step package was reused only as unscored depth-1 prediction output:

```text
previous_s1_archive_sha256_match=true
treated_as_unscored_prediction_output=true
restricted_answer_key_read=false
```

Local text search found no restricted answer data, no `hit@`, no `target_product`, and no local correctness fields in the returned package. Only compliance statements such as `restricted_answer_key_read=false` were found.

## 4. Returned route files

The package contains the requested multistep route-expansion files:

```text
03_ROUTE_EXPANSION/biotransformer_envmicro_multistep/PREDICTED_ROUTE_EDGES.jsonl
03_ROUTE_EXPANSION/biotransformer_envmicro_multistep/PREDICTED_ROUTE_NODES.csv
03_ROUTE_EXPANSION/biotransformer_envmicro_multistep/PREDICTED_ROUTE_PATHS.jsonl

03_ROUTE_EXPANSION/envipath_bbd_rules_multistep/PREDICTED_ROUTE_EDGES.jsonl
03_ROUTE_EXPANSION/envipath_bbd_rules_multistep/PREDICTED_ROUTE_NODES.csv
03_ROUTE_EXPANSION/envipath_bbd_rules_multistep/PREDICTED_ROUTE_PATHS.jsonl

03_ROUTE_EXPANSION/eclipse_predec_bbd_finetuned_10fold_multistep/PREDICTED_ROUTE_EDGES.jsonl
03_ROUTE_EXPANSION/eclipse_predec_bbd_finetuned_10fold_multistep/PREDICTED_ROUTE_NODES.csv
03_ROUTE_EXPANSION/eclipse_predec_bbd_finetuned_10fold_multistep/PREDICTED_ROUTE_PATHS.jsonl

03_ROUTE_EXPANSION/eclipse_noec_bbd_finetuned_10fold_multistep_optional/PREDICTED_ROUTE_EDGES.jsonl
03_ROUTE_EXPANSION/eclipse_noec_bbd_finetuned_10fold_multistep_optional/PREDICTED_ROUTE_NODES.csv
03_ROUTE_EXPANSION/eclipse_noec_bbd_finetuned_10fold_multistep_optional/PREDICTED_ROUTE_PATHS.jsonl
```

Required routes:

| Route | Executor status | Max depth requested | Max depth reached | Returned edge rows | Returned node rows | Returned path rows |
|---|---|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | ok | 6 | 6 | 8,069 | 6,791 | 786 |
| enviPath BBD Rules | ok | 6 | 6 | 2,932 | 2,693 | 745 |
| ECLIPSE PREDEC BBD-finetuned 10-fold | ok | 6 | 6 | 29,530 | 20,715 | 930 |

Optional route:

| Route | Executor status | Max depth requested | Max depth reached | Returned edge rows | Returned node rows | Returned path rows |
|---|---|---:|---:|---:|---:|---:|
| ECLIPSE NoEC BBD-finetuned 10-fold optional | completed_with_partial_depth | 6 | 4 | 15,197 | 11,232 | 930 |

Typed blocker for optional NoEC:

```text
eclipse_noec_multistep_status=completed_with_partial_depth_runtime_cap_reached
```

This is acceptable because NoEC was optional, but it must be marked as partial-depth.

## 5. Independent depth audit

The executor summary reports `parents_with_depth_k`, but this field is not always equivalent to “cases with actual newly materialized nodes at depth k.” Therefore this audit recomputed actual node depths from `PREDICTED_ROUTE_NODES.csv`.

Actual cases with nodes first seen at each depth:

| Route | depth0 parent | depth1 | depth2 | depth3 | depth4 | depth5 | depth6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 93 | 85 | 84 | 81 | 81 | 80 | 80 |
| enviPath BBD Rules | 93 | 88 | 83 | 71 | 59 | 41 | 26 |
| ECLIPSE PREDEC | 93 | 93 | 93 | 93 | 93 | 93 | 93 |
| ECLIPSE NoEC optional | 93 | 93 | 93 | 93 | 93 | 0 | 0 |

Important discrepancy:

```text
enviPath summary says parents reaching depth6 = 41, but actual node table has depth6 nodes for only 26 cases.
```

Likely explanation:

```text
The executor's "parents reaching depth k" field appears to reflect expansion/frontier attempt rounds rather than actual new-node materialization. For scientific interpretation, use actual node and edge files, not this summary field alone.
```

## 6. Path-file audit

`PREDICTED_ROUTE_PATHS.jsonl` files are present and internally have matching path-length arrays, but many paths are not simple paths. They contain repeated nodes, repeated SMILES, and sometimes repeated edge IDs.

Repeated path counts:

| Route | Path rows | Repeated-node paths | Repeated-edge paths | Interpretation |
|---|---:|---:|---:|---|
| BioTransformer ENVMICRO | 786 | 49 | 21 | Mostly usable but still needs cleanup |
| enviPath BBD Rules | 745 | 0 | 0 | Cleanest path file |
| ECLIPSE PREDEC | 930 | 917 | 828 | Not reliable for path-level scoring as-is |
| ECLIPSE NoEC optional | 930 | 921 | 834 | Not reliable for path-level scoring as-is |

Example issue:

```text
ECLIPSE PREDEC path example repeats the same compound node and same edge many times:
Clc1ccccc1 -> Oc1ccc(Cl)cc1 -> Oc1ccc(Cl)cc1 -> Oc1ccc(Cl)cc1 -> ...
```

Therefore:

```text
Do not score full route paths directly from PREDICTED_ROUTE_PATHS for ECLIPSE/NoEC. Reconstruct clean acyclic paths from PREDICTED_ROUTE_EDGES and PREDICTED_ROUTE_NODES, or ask executor to regenerate path files with simple-path constraints.
```

## 7. Local scoring setup

The local restricted answer set has:

```text
93 parent cases
92 evaluable route cases
1 zero-route-edge case: FR-BBD3-CAND-c0105 Chlorobenzene
```

Primary denominator:

```text
92 evaluable cases
```

Scoring policy used here:

```text
1. HPC package itself was not scored and did not read restricted answers.
2. Local audit loaded restricted answers only after return.
3. For tool predictions, use valid normalized predicted edges/nodes.
4. Exclude parent-copy and direct self-loop predictions from the main clean score.
5. Use non-isomeric RDKit canonical SMILES as the main structure-matching key, because BBD answers often do not specify stereochemistry while ECLIPSE may output stereospecific products.
6. Report node recovery and edge recovery separately.
```

Answer label totals under this non-isomeric scoring key:

| Answer set | Total labels / edges |
|---|---:|
| generation-1 product labels | 179 |
| any downstream product labels | 619 |
| terminal product labels | 223 |
| exact answer edges | 690 |

## 8. Local scoring — clean non-isomeric graph score

Case-level recovery:

| Route | Generation-1 case hit | Any downstream case hit | Terminal-node case hit | Exact-edge case hit |
|---|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 59/92 = 64.1% | 71/92 = 77.2% | 44/92 = 47.8% | 60/92 = 65.2% |
| enviPath BBD Rules | 53/92 = 57.6% | 62/92 = 67.4% | 30/92 = 32.6% | 52/92 = 56.5% |
| ECLIPSE PREDEC | 81/92 = 88.0% | 89/92 = 96.7% | 67/92 = 72.8% | 80/92 = 87.0% |
| ECLIPSE NoEC optional | 70/92 = 76.1% | 80/92 = 87.0% | 52/92 = 56.5% | 62/92 = 67.4% |

Label / edge recovery:

| Route | Generation-1 labels | Any downstream labels | Terminal labels | Exact answer edges |
|---|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 87/179 = 48.6% | 207/619 = 33.4% | 70/223 = 31.4% | 154/690 = 22.3% |
| enviPath BBD Rules | 85/179 = 47.5% | 169/619 = 27.3% | 48/223 = 21.5% | 136/690 = 19.7% |
| ECLIPSE PREDEC | 127/179 = 70.9% | 324/619 = 52.3% | 109/223 = 48.9% | 213/690 = 30.9% |
| ECLIPSE NoEC optional | 103/179 = 57.5% | 233/619 = 37.6% | 81/223 = 36.3% | 133/690 = 19.3% |

Interpretation:

```text
ECLIPSE PREDEC is clearly strongest in this bounded multistep graph setting.

Compared with the previous one-step package, multistep expansion substantially increases downstream and terminal-node recovery. However, exact edge recovery is still much lower than case-level node recovery, meaning the tools often generate some correct compounds somewhere in the graph but do not reliably reconstruct the exact BBD route topology.
```

## 9. QC observations

Executor QC summary:

```text
invalid_or_unparseable_prediction_rows=565
parent_copy_or_self_loop_rows=5498
cycle_or_seen_before_rows=14104
restricted_answer_key_read=false
scoring_performed=false
```

Route-level edge QC from local parsing:

| Route | Edge rows | Valid normalized rows | Invalid rows | Self/source-copy rows | Parent-copy rows | Cycle/seen-before rows |
|---|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 8,069 | 7,504 | 565 | 32 | 0 | 806 |
| enviPath BBD Rules | 2,932 | 2,932 | 0 | 1 | 0 | 332 |
| ECLIPSE PREDEC | 29,530 | 29,530 | 0 | 3,345 | 105 | 8,908 |
| ECLIPSE NoEC optional | 15,197 | 15,197 | 0 | 1,979 | 165 | 4,058 |

The high self-loop / seen-before burden is the main reason path-level output needs cleanup.

## 10. What can be said to Huang-laoshi / Shijie

Recommended wording:

```text
We have now completed a bounded multistep route-expansion supplement on the 93-case BBD full-route v0.3/v3.1 blind input. This is no longer only one-step prediction: BioTransformer, enviPath BBD Rules, and ECLIPSE PREDEC all returned multistep edge/node graphs up to requested depth 6; optional ECLIPSE NoEC stopped at depth 4 due to runtime cap.

Local restricted scoring shows ECLIPSE PREDEC has the best bounded-route graph recovery: generation-1 case hit 81/92, any downstream node hit 89/92, terminal-node hit 67/92, and exact-edge case hit 80/92 under non-isomeric structure matching.

However, this should not be described as complete mineralization. It is bounded prediction against BBD-local known pathway endpoints. Also, returned PREDICTED_ROUTE_PATHS for ECLIPSE contain many repeated-node/repeated-edge paths, so final path-level claims require graph cleanup or a regenerated simple-path supplement.
```

## 11. Recommended next action

If we want a teacher-facing final report now:

```text
Use this package for bounded multistep edge/node graph scoring, with the caveats above.
```

If we want a cleaner final route-path deliverable:

```text
Ask chenyu to produce a small repair supplement:
1. Do not rerun all predictions.
2. Reuse existing PREDICTED_ROUTE_EDGES and PREDICTED_ROUTE_NODES.
3. Regenerate PREDICTED_ROUTE_PATHS as simple acyclic paths only.
4. Do not repeat node IDs, SMILES, or edge IDs inside one path.
5. Make path_depth consistent with actual node depth.
6. Recompute route summaries from actual materialized nodes, not frontier attempts.
7. Regenerate MANIFEST.sha256 after all logs are finalized.
```

This would make the route-path layer defensible without spending another full prediction run.
