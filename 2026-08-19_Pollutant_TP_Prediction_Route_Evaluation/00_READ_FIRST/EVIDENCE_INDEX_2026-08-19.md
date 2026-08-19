# Evidence index — pollutant TP prediction route evaluation

Date: 2026-08-19

## 1. Read order

1. `POLLUTANT_TP_PREDICTION_ROUTE_STAGE_REPORT_2026-08-19.md`  
   Main report, written for teacher review.
2. `TEST_SET_CONSTRUCTION_NOTE_2026-08-19.md`  
   Explains how BBD83 and Soil/Sludge evaluation sets were constructed and what they can/cannot prove.
3. `PACKAGE_LOCAL_AUDIT_2026-08-19.md`  
   Local audit for this assembled evidence package.
4. `../01_Key_Tables/tool_capability_comparison_2026-08-19.md`  
   Human-readable comparison of BioTransformer, enviPath and ECLIPSE.
5. `../01_Key_Tables/soil_sludge_metrics_summary_v2.csv`  
   Final cleaned Soil/Sludge prediction metrics.
6. `../01_Key_Tables/envipath_lookup_summary_metrics.csv`  
   enviPath local lookup summary.
7. `../06_Detailed_Result_Tables/README_DETAILED_RESULT_TABLES_2026-08-19.md`  
   Directly browsable per-route and per-parent result tables extracted from the returned archives.

## 2. Key return packages

| File | Meaning |
|---|---|
| `../02_Return_Packages/chem_eclipse_bbd_finetune_soil_sludge_transfer_eval_clean_supplement_v2_20260819.tar.gz` | Final cleaned Soil/Sludge transfer evaluation supplement. |
| `../02_Return_Packages/envipath_soil_sludge_known_pathway_lookup_supplement_20260819.tar.gz` | enviPath Soil/Sludge known-pathway lookup supplement. |
| `../02_Return_Packages/chem_eclipse_bbd_fullfold_bbd83_oof_parentfilter_supplement_20260817.tar.gz` | BBD-finetuned ECLIPSE BBD83 all-fold / OOF parent-filtered supplement. |
| `../02_Return_Packages/enzymecage_m3_p1_2_1_bbd83_eclipse_two_stage_ec_conditioned_product_pilot_20260817.tar.gz` | Initial ECMap/USPTO ECLIPSE two-stage BBD83 pilot. |
| `../02_Return_Packages/enzymecage_m3_p1_2_1_bbd_known_pathway_v0_2_four_route_blind_rerun1_20260805.tar.gz` | BBD83 four-route BioTransformer / enviPath / enviFormer comparison. |

## 3. Key local audits

| Audit | Use |
|---|---|
| `../03_Local_Audits/CHEM_ECLIPSE_BBD_FINETUNE_SOIL_SLUDGE_TRANSFER_EVAL_CLEAN_SUPPLEMENT_V2_RETURN_LOCAL_AUDIT_2026-08-19.md` | Final PASS audit for Soil/Sludge transfer clean supplement v2. |
| `../03_Local_Audits/ENVIPATH_SOIL_SLUDGE_KNOWN_PATHWAY_LOOKUP_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-19.md` | Validates enviPath known-pathway lookup, with retrieval/prediction caveat. |
| `../03_Local_Audits/CHEM_ECLIPSE_BBD83_OOF_PARENTFILTER_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-18.md` | Conservative OOF reading of BBD-finetuned ECLIPSE. |
| `../03_Local_Audits/ECLIPSE_TWO_STAGE_EC_CONDITIONED_PRODUCT_BBD83_RETURN_LOCAL_AUDIT_2026-08-17.md` | Initial ECLIPSE ECMap/USPTO pilot showing PredEC did not help before BBD fine-tuning. |
| `../03_Local_Audits/ENZYMECAGE_M3_P1_2_1_BBD_KNOWN_PATHWAY_V0_2_FOUR_ROUTE_RERUN1_RETURN_SCORING_AUDIT_2026-08-05.md` | BBD83 BioTransformer / enviPath / enviFormer baseline comparison. |
| `../03_Local_Audits/NON_BBD_EXTERNAL_TP_CURRENT_STATE_AND_SOIL_SLUDGE_SIDE_TEST_DECISION_2026-08-18.md` | Explains why Soil/Sludge transfer was used before finishing strict non-BBD external benchmark. |

## 4. Key table files

| File | Description |
|---|---|
| `../01_Key_Tables/tool_capability_comparison_2026-08-19.md` | Teacher-readable route comparison and recommended system use. |
| `../01_Key_Tables/route_metric_summary_2026-08-19.csv` | Compact metric table across BBD83 and Soil/Sludge. |
| `../01_Key_Tables/soil_sludge_metrics_summary_v2.csv` | Full cleaned prediction metric summary from v2 supplement. |
| `../01_Key_Tables/soil_sludge_route_status_corrected.csv` | Route status table separating completed / skipped / lookup-only routes. |
| `../01_Key_Tables/soil_sludge_biotransformer_empty_or_error_parent_list.csv` | 109 BioTransformer empty/error parent rows. |
| `../01_Key_Tables/envipath_lookup_summary_metrics.csv` | Full local enviPath lookup summary metrics. |
| `../01_Key_Tables/envipath_lookup_vs_prediction_summary.md` | Returned comparison note, with lookup vs prediction boundary. |

## 5. Detailed result tables

| Folder | Description |
|---|---|
| `../06_Detailed_Result_Tables/BBD83/` | Direct BBD83 prediction/detail tables for BioTransformer, enviPath BBD Rules, enviFormer and ECLIPSE. |
| `../06_Detailed_Result_Tables/Soil_Sludge/` | Soil/Sludge per-parent scoring and enviPath lookup detail tables. |

## 6. What is safe to say

```text
BioTransformer ENVMICRO remains the strongest current blind-prediction baseline.
BBD-finetuned ECLIPSE PREDEC improves over ECLIPSE NoEC but should remain a complementary candidate generator for now.
enviPath local snapshot lookup is complete for the Soil/Sludge-derived known-pathway set and should be used as a known-pathway retrieval layer.
```

## 7. What not to say

```text
Do not say enviPath has 100% prediction accuracy on Soil/Sludge.
Do not say ECLIPSE has replaced BioTransformer.
Do not say this is a strict non-BBD external benchmark.
```
