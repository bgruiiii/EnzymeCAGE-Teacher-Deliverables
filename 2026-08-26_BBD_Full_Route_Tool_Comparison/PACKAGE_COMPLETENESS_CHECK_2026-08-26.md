# Package completeness check — BBD full-route tool comparison

Date: 2026-08-26  
Package:

```text
22_BBD_Full_Route_Tool_Comparison_2026-08-26
```

## 1. Verdict

```text
LOCAL_PACKAGE_READY_FOR_GITHUB_UPLOAD_REVIEW
```

This package now contains the full local evidence chain for the BBD full-route v0.3/v3.1 tool comparison:

- strict blind input;
- HPC return identities;
- local audits;
- one-step prediction summary;
- bounded multistep graph coverage summary;
- simple-path v2 cleanup summary;
- stricter all-92 MG-Structural@K route-structure scoring;
- Chinese readable discussion report for senior/student discussion.

No raw restricted answer key files are included in this package.

## 2. Main files for teacher / reviewer

Recommended reading order:

```text
README.md
SISTER_READABLE_BBD_FULL_ROUTE_MULTISTEP_PREDICTION_REPORT_2026-08-26.md
03_summary_tables/ONE_STEP_GENERATION1_SCORE_SUMMARY_2026-08-26.csv
03_summary_tables/MULTISTEP_GRAPH_LOCAL_SCORE_SUMMARY_2026-08-26.csv
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_MG_STRUCTURAL_AT_K_ALL92_SUPPLEMENT_CODEX_FINAL_AUDIT_2026-08-26.md
```

## 3. Result layers included

### 3.1 One-step product prediction

Primary table:

```text
03_summary_tables/ONE_STEP_GENERATION1_SCORE_SUMMARY_2026-08-26.csv
```

Main result:

```text
ECLIPSE PREDEC Hit@10 = 74/92 = 80.4%
BioTransformer Hit@10 = 52/92 = 56.5%
ECLIPSE NoEC Hit@10 = 52/92 = 56.5%
enviPath BBD Rules Hit@10 = 45/92 = 48.9%
```

### 3.2 Bounded multistep graph coverage

Primary table:

```text
03_summary_tables/MULTISTEP_GRAPH_LOCAL_SCORE_SUMMARY_2026-08-26.csv
```

Main result:

```text
ECLIPSE PREDEC any downstream node case hit = 89/92 = 96.7%
ECLIPSE PREDEC BBD-local terminal node case hit = 67/92 = 72.8%
ECLIPSE PREDEC exact-edge case hit = 80/92 = 87.0%
```

Interpretation:

```text
This layer measures coverage ability. It is useful, but too permissive if used alone because large predicted graphs can inflate hit rates.
```

### 3.3 Stricter route-structure scoring

Primary table:

```text
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv
```

Main all-92 macro Jaccard:

| tool | K=1 | K=3 | K=5 |
|---|---:|---:|---:|
| BioTransformer ENVMICRO | 0.197 | 0.154 | 0.152 |
| enviPath BBD Rules | 0.116 | 0.136 | 0.140 |
| ECLIPSE PREDEC | 0.178 | 0.106 | 0.070 |
| ECLIPSE NoEC optional | 0.155 | 0.100 | 0.065 |

Interpretation:

```text
BioTransformer has the best all-92 structural Jaccard at K=1/3/5.
ECLIPSE PREDEC has the highest recall but many false-positive branches, so precision/Jaccard drop as K increases.
```

## 4. Audit coverage

The package-internal audit folder now includes:

```text
02_local_audits/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_1_STRICT_BLIND_FIX_LOCAL_AUDIT_2026-08-21.md
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_THREE_TOOL_BLIND_PREDICTIONS_RETURN_LOCAL_AUDIT_2026-08-25.md
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_BOUNDED_MULTISTEP_ROUTE_EXPANSION_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-26.md
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_MULTISTEP_SIMPLE_PATH_REPAIR_V2_CLEANUP_SUPPLEMENT_RETURN_LOCAL_AUDIT_2026-08-26.md
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_ENVIFORMER_STYLE_MG_STRUCTURAL_AT_K_LOCAL_AUDIT_2026-08-26.md
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_ENVIFORMER_STYLE_MG_STRUCTURAL_AT_K_CODEX_REVIEW_AUDIT_2026-08-26.md
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_MG_STRUCTURAL_AT_K_ALL92_REPORTING_SUPPLEMENT_LOCAL_AUDIT_2026-08-26.md
02_local_audits/BBD_FULL_ROUTE_V0_3_V3_1_MG_STRUCTURAL_AT_K_ALL92_SUPPLEMENT_CODEX_FINAL_AUDIT_2026-08-26.md
```

## 5. Boundary statement

This package should be described as:

```text
BBD-local known-route, bounded depth≤6, blind-input tool comparison.
```

It should not be described as:

```text
complete mineralization prediction
full environmental degradation proof
CO2/H2O endpoint prediction
official enviFormer probability-MG/AUPRC reproduction
```

## 6. Suggested next action

If uploading to GitHub, update the target repository README/homepage to link directly to this package folder and point readers first to:

```text
README.md
SISTER_READABLE_BBD_FULL_ROUTE_MULTISTEP_PREDICTION_REPORT_2026-08-26.md
07_enviformer_style_mg_structural_at_k/MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv
```

