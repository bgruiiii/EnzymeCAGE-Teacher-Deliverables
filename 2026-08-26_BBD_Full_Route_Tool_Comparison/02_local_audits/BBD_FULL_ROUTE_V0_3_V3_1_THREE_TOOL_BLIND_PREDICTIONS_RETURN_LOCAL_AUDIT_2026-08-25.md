# Local audit — BBD full-route v0.3 v3.1 three-tool blind prediction return

Date: 2026-08-25  
Audited archive:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz
```

Identity sidecar:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_three_tool_blind_predictions_20260821.tar.gz.identity.txt
```

Local restricted scoring reference used for this audit:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/21_BBD_Known_Pathway_Full_Route_Testset_2026-08-21/bbd_known_pathway_full_route_v0_3_candidate_v3_repair_20260821/restricted/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_RESTRICTED_ROUTE_ANSWER_KEY.jsonl
```

## 1. Verdict

Executor package integrity and blind-boundary compliance:

```text
PASS
```

Scientific / task-scope verdict:

```text
PARTIAL_FOR_FULL_ROUTE_GOAL
```

Reason:

```text
The package successfully returns first-step (prediction_depth=1) blind product candidates for BioTransformer, enviPath BBD Rules, ECLIPSE PREDEC, and ECLIPSE NoEC. However, it does not contain multi-step / route-expansion outputs. The directory 04_OPTIONAL_ROUTE_EXPANSION is empty.
```

Therefore this return is valid for:

```text
parent -> first-generation product scoring
parent -> any known downstream node direct-recovery diagnostic
parent -> terminal node direct-recovery diagnostic
```

But it is not yet sufficient for:

```text
tool-predicted full degradation route reconstruction
multi-step route graph scoring
path-to-terminal scoring
mineralization or terminal-closure scoring
```

## 2. Archive and manifest

Local archive SHA256:

```text
5eee73713a3034c75e44e149874758146f69f3d6ee83f91bfc2536a5170e6f5f
```

Sidecar reports:

```text
archive_sha256=5eee73713a3034c75e44e149874758146f69f3d6ee83f91bfc2536a5170e6f5f
final_status=COMPLETE_THREE_TOOL_BLIND_PREDICTIONS_READY_FOR_LOCAL_SCORING
restricted_answer_key_read=false
strict_blind_rows=93
```

Manifest check:

```text
sha256sum -c MANIFEST.sha256
```

Result:

```text
all files OK
```

## 3. Input audit

Strict blind identity reported by executor:

```text
archive_sha256_match=true
blind_csv_sha256_match=true
blind_csv_rows=93
blind_csv_rows_expected=93
blind_csv_rows_match=true
blind_csv_sha256=be11658b0ede11093bb8bb833281994cb2f507629eaf7b3524de74a4e46acb66
restricted_answer_key_read=false
input_audit_pass=true
```

Strict blind columns:

```text
full_route_case_id
scope
pollutant_name
pollutant_category
parent_smiles
parent_canonical_smiles
input_note
```

No restricted answer files were found in the return package. Text search found only compliance statements such as `restricted answer key read: false`.

## 4. Executor route status

Executor final status:

```text
COMPLETE_THREE_TOOL_BLIND_PREDICTIONS_READY_FOR_LOCAL_SCORING
```

Route summary:

| Route | Status | Input parents | Parents with predictions | Normalized predictions | Raw outputs | Notes |
|---|---|---:|---:|---:|---:|---|
| BioTransformer ENVMICRO s1 | ok | 93 | 85 | 259 | 85 | success=85, error=8 |
| enviPath BBD Rules s1 | ok | 93 | 89 | 353 | 89 | prediction ok, lookup ok |
| ECLIPSE PREDEC BBD-finetuned 10-fold s1 | ok | 93 | 93 | 740 | 10 | CPU, 10 folds |
| ECLIPSE NoEC BBD-finetuned 10-fold s1 | ok | 93 | 93 | 671 | 10 | CPU, 10 folds |

The package also contains enviPath database lookup for all 93 parents:

```text
05_ENVIPATH_DATABASE_LOOKUP_SEPARATE/ENVIPATH_DATABASE_LOOKUP_SUMMARY.csv
rows=93
```

This lookup layer must remain separate from prediction metrics.

## 5. Prediction-depth audit

All normalized prediction rows are first-step predictions:

| Route | prediction_depth values |
|---|---|
| BioTransformer ENVMICRO | 1 only |
| enviPath BBD Rules | 1 only |
| ECLIPSE PREDEC | 1 only |
| ECLIPSE NoEC | 1 only |

No multi-step route expansion files were produced:

```text
04_OPTIONAL_ROUTE_EXPANSION file count = 0
```

This is the central limitation of the current return.

## 6. Missing prediction cases

BioTransformer ENVMICRO had no normalized prediction rows for 8 cases:

| Case | Pollutant |
|---|---|
| FR-BBD3-CAND-c0347 | Methanesulfonate |
| FR-BBD3-PARENT-c0039 | Dibenzofuran |
| FR-BBD3-PARENT-c0352 | 1-Aminocyclopropane-1-carboxylate |
| FR-BBD3-PARENT-c0426 | Dibenzo-p-dioxin |
| FR-BBD3-PARENT-c0444 | Carbazole |
| FR-BBD3-PARENT-c0526 | Acetylene |
| FR-BBD3-PARENT-c0939 | Hypophosphite |
| FR-BBD3-PARENT-c1039 | 4-Fluorobenzoate |

BioTransformer log example for Acetylene:

```text
For the prediction of environmental microbial metabolism, the compound must:
1) be organic; 2) not be a mixture; 3) not be a cofactor or dead end compound;
and 4) have a molecular mass of 1000 Da or less.
```

enviPath BBD Rules had no normalized prediction rows for 4 cases:

| Case | Pollutant |
|---|---|
| FR-BBD3-PARENT-c0039 | Dibenzofuran |
| FR-BBD3-PARENT-c0444 | Carbazole |
| FR-BBD3-PARENT-c0939 | Hypophosphite |
| FR-BBD3-PARENT-c1201 | 4-Hydroxypyridine |

ECLIPSE PREDEC and ECLIPSE NoEC both produced normalized rows for all 93 cases.

## 7. Local scoring setup

The local restricted answer key has 93 case records. One case has no scoreable downstream answer because the current v3 benchmark build marks it as zero-route-edge:

```text
FR-BBD3-CAND-c0105 Chlorobenzene
```

Therefore the primary denominator below is:

```text
92 evaluable cases
```

Three local answer sets were computed:

| Answer set | Meaning | Total accepted labels | Cases with no labels |
|---|---|---:|---:|
| generation_1 | immediate products from parent in BBD route graph | 181 | 1 |
| downstream | any downstream product node in the BBD route graph | 627 | 1 |
| terminal | terminal nodes from parent-to-terminal paths | 224 | 1 |

Important interpretation:

```text
generation_1 is the fair direct score for one-step predictions.
downstream and terminal are diagnostic direct-recovery checks only, because the returned predictions are still prediction_depth=1.
```

## 8. Local scoring — generation-1 products

This is the main fair score for the returned first-step predictions.

| Route | Filter mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Labels recovered@10 |
|---|---|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | raw | 31/92 = 33.7% | 43/92 = 46.7% | 52/92 = 56.5% | 52/92 = 56.5% | 0.416 | 77/181 |
| BioTransformer ENVMICRO | parent-filtered | 31/92 = 33.7% | 43/92 = 46.7% | 52/92 = 56.5% | 52/92 = 56.5% | 0.416 | 77/181 |
| enviPath BBD Rules | raw | 24/92 = 26.1% | 42/92 = 45.7% | 45/92 = 48.9% | 45/92 = 48.9% | 0.353 | 73/181 |
| enviPath BBD Rules | parent-filtered | 24/92 = 26.1% | 42/92 = 45.7% | 45/92 = 48.9% | 45/92 = 48.9% | 0.353 | 73/181 |
| ECLIPSE PREDEC | raw | 28/92 = 30.4% | 59/92 = 64.1% | 69/92 = 75.0% | 74/92 = 80.4% | 0.492 | 101/181 |
| ECLIPSE PREDEC | parent-filtered | 33/92 = 35.9% | 62/92 = 67.4% | 70/92 = 76.1% | 74/92 = 80.4% | 0.528 | 101/181 |
| ECLIPSE NoEC | raw | 19/92 = 20.7% | 41/92 = 44.6% | 50/92 = 54.3% | 52/92 = 56.5% | 0.344 | 67/181 |
| ECLIPSE NoEC | parent-filtered | 29/92 = 31.5% | 47/92 = 51.1% | 50/92 = 54.3% | 52/92 = 56.5% | 0.410 | 67/181 |

Main generation-1 result:

```text
ECLIPSE PREDEC is strongest on Hit@3/5/10 and recovered-label count.
BioTransformer is competitive and tied with ECLIPSE NoEC at Hit@10.
enviPath BBD Rules is useful but weaker on this 93-parent v0.3 first-step score.
```

## 9. Local scoring — any downstream node diagnostic

Because all predictions are one-step outputs, this is not full-route reconstruction scoring. It only asks whether a predicted one-step product directly equals any known downstream node in the route graph.

| Route | Filter mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Labels recovered@10 |
|---|---|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | raw / parent-filtered | 38/92 = 41.3% | 56/92 = 60.9% | 63/92 = 68.5% | 63/92 = 68.5% | 0.517 | 95/627 |
| enviPath BBD Rules | raw / parent-filtered | 27/92 = 29.3% | 46/92 = 50.0% | 52/92 = 56.5% | 53/92 = 57.6% | 0.401 | 88/627 |
| ECLIPSE PREDEC | raw | 36/92 = 39.1% | 64/92 = 69.6% | 73/92 = 79.3% | 77/92 = 83.7% | 0.555 | 140/627 |
| ECLIPSE PREDEC | parent-filtered | 41/92 = 44.6% | 67/92 = 72.8% | 74/92 = 80.4% | 77/92 = 83.7% | 0.593 | 140/627 |
| ECLIPSE NoEC | raw | 25/92 = 27.2% | 47/92 = 51.1% | 56/92 = 60.9% | 60/92 = 65.2% | 0.410 | 89/627 |
| ECLIPSE NoEC | parent-filtered | 36/92 = 39.1% | 53/92 = 57.6% | 56/92 = 60.9% | 60/92 = 65.2% | 0.483 | 88/627 |

Diagnostic result:

```text
ECLIPSE PREDEC again gives the strongest direct recovery of known downstream nodes.
```

## 10. Local scoring — terminal node diagnostic

Again, this is not route-to-terminal scoring. It only asks whether one-step predictions directly equal a terminal node.

| Route | Filter mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Labels recovered@10 |
|---|---|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | raw / parent-filtered | 4/92 = 4.3% | 9/92 = 9.8% | 13/92 = 14.1% | 15/92 = 16.3% | 0.080 | 18/224 |
| enviPath BBD Rules | raw / parent-filtered | 2/92 = 2.2% | 8/92 = 8.7% | 12/92 = 13.0% | 14/92 = 15.2% | 0.063 | 18/224 |
| ECLIPSE PREDEC | raw | 5/92 = 5.4% | 13/92 = 14.1% | 18/92 = 19.6% | 24/92 = 26.1% | 0.113 | 28/224 |
| ECLIPSE PREDEC | parent-filtered | 6/92 = 6.5% | 14/92 = 15.2% | 19/92 = 20.7% | 24/92 = 26.1% | 0.122 | 28/224 |
| ECLIPSE NoEC | raw | 6/92 = 6.5% | 11/92 = 12.0% | 14/92 = 15.2% | 18/92 = 19.6% | 0.102 | 18/224 |
| ECLIPSE NoEC | parent-filtered | 8/92 = 8.7% | 12/92 = 13.0% | 15/92 = 16.3% | 17/92 = 18.5% | 0.118 | 17/224 |

Interpretation:

```text
Terminal direct hits are low, as expected, because the current returned outputs are one-step predictions rather than iterative route predictions.
```

## 11. Parent-copy behavior

Parent-copy rows:

| Route | Parent-copy rows |
|---|---:|
| BioTransformer ENVMICRO | 0 |
| enviPath BBD Rules | 0 |
| ECLIPSE PREDEC | 53 |
| ECLIPSE NoEC | 76 |

Parent filtering improves ECLIPSE early-rank metrics, especially NoEC and PREDEC Hit@1. Raw and parent-filtered results should both be reported, but parent-filtered is more meaningful for degradation product prediction.

## 12. Caveats

1. The returned package is a valid blind prediction package, but not a completed full-route expansion result.
2. All route predictions are first-step only.
3. enviPath database lookup is present for all 93 parents, but it is known-pathway retrieval and must not be mixed with prediction accuracy.
4. ECLIPSE used CPU mode; all 10 folds loaded and ran successfully.
5. BioTransformer used a `/tmp/.../Biotransformer` jar path with Java 17. The package records the actual jar SHA256. This is acceptable for this executor run, but the jar identity should be preserved in any teacher-facing evidence package.
6. The benchmark itself remains v0.3 candidate. It tests BBD known downstream routes, not complete environmental mineralization.

## 13. Recommended next step

If the immediate goal is a three-tool first-step comparison against the expanded full-route answer graph:

```text
Use this package for local scoring/reporting.
```

If the immediate goal is truly complete degradation-route prediction:

```text
Send a supplement request to chenyu for bounded multi-step route expansion.
```

Suggested supplement scope:

```text
Use the same 93 strict blind parents.
Run iterative/official multistep expansion where feasible.
max_depth=3
top10 frontier per depth
deduplicate by RDKit canonical SMILES
preserve raw outputs and predicted route edges
do not read restricted answers
return PREDICTED_ROUTE_EDGES.jsonl and PREDICTED_ROUTE_NODES.csv per route
```

Only after such a supplement can we score path-level / route-to-terminal behavior.

