# Detailed result tables

Date: 2026-08-19

This folder contains extracted, directly browsable result tables from the returned archives. The original returned packages remain preserved under `../02_Return_Packages/`.

## BBD83

| File | Meaning |
|---|---|
| `BBD83/bbd83_biotransformer_envmicro_predictions_normalized.jsonl` | BioTransformer ENVMICRO normalized predictions for the 83-parent BBD known-pathway set. |
| `BBD83/bbd83_envipath_bbd_rules_predictions_normalized.jsonl` | enviPath BBD Rules one-step prediction results for the same 83 parents. |
| `BBD83/bbd83_enviformer_latest_predictions_normalized.jsonl` | current available enviFormer checkpoint predictions for the same 83 parents. |
| `BBD83/bbd83_envipath_database_lookup_summary.csv` | BBD83 enviPath database lookup summary; lookup is separate from prediction scoring. |
| `BBD83/bbd83_eclipse_initial_noec_predictions_normalized.csv` | initial USPTO-pretrained ECLIPSE NoEC product predictions before BBD fine-tuning. |
| `BBD83/bbd83_eclipse_initial_predec_predictions_normalized.csv` | initial ECMap/PREDEC-conditioned ECLIPSE predictions before BBD fine-tuning. |
| `BBD83/bbd83_eclipse_finetuned_noec_oof_parent_filtered_aggregated.csv` | BBD-finetuned ECLIPSE NoEC conservative OOF parent-filtered aggregated table. |
| `BBD83/bbd83_eclipse_finetuned_predec_oof_parent_filtered_aggregated.csv` | BBD-finetuned ECLIPSE PREDEC conservative OOF parent-filtered aggregated table. |
| `BBD83/bbd83_eclipse_finetuned_predec_allfold_parent_filtered_aggregated.csv` | BBD-finetuned ECLIPSE PREDEC all-fold parent-filtered aggregated table; useful but optimistic. |

## Soil/Sludge

| File | Meaning |
|---|---|
| `Soil_Sludge/soil_sludge_metrics_summary_v2_extracted.csv` | final cleaned Soil/Sludge metric summary extracted from the v2 return package. |
| `Soil_Sludge/soil_sludge_per_parent_scoring_table_with_biotransformer.csv` | per-parent Soil/Sludge scoring table covering ECLIPSE NoEC, ECLIPSE PREDEC and BioTransformer. |
| `Soil_Sludge/envipath_local_snapshot_parent_lookup_results.csv` | parent-level enviPath local snapshot lookup results. |
| `Soil_Sludge/envipath_local_snapshot_product_recall_by_parent.csv` | per-parent known-product recall for enviPath local snapshot lookup. |
| `Soil_Sludge/envipath_lookup_vs_prediction_parent_level_join.csv` | joined parent-level comparison between lookup and prediction routes. |

## Interpretation boundary

`enviPath local snapshot lookup` is known-pathway retrieval, not blind prediction. It should not be reported as 100% prediction accuracy.
