# Codex final audit — MG-Structural@K all-92 reporting supplement

Date: 2026-08-26  
Reviewer: Codex  
Reviewed folder:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/22_BBD_Full_Route_Tool_Comparison_2026-08-26/07_enviformer_style_mg_structural_at_k
```

Local executor audit:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/BBD_FULL_ROUTE_V0_3_V3_1_MG_STRUCTURAL_AT_K_ALL92_REPORTING_SUPPLEMENT_LOCAL_AUDIT_2026-08-26.md
```

Prior Codex review:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/BBD_FULL_ROUTE_V0_3_V3_1_ENVIFORMER_STYLE_MG_STRUCTURAL_AT_K_CODEX_REVIEW_AUDIT_2026-08-26.md
```

## 1. Verdict

```text
PASS_READY_FOR_TEACHER_FACING_INTEGRATION
```

The previously identified reporting limitation has been fixed. The supplement now includes an all-92 inclusive summary where all 92 evaluable cases are retained in the denominator and `NO_PREDICTION` cases contribute zero scores. This is the correct teacher-facing cross-tool summary.

## 2. Files checked

The folder contains the expected files:

```text
README.md
MG_STRUCTURAL_AT_K_METHOD_NOTE_2026-08-26.md
MG_STRUCTURAL_AT_K_REPORTING_SUPPLEMENT_2026-08-26.md
MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv
MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv
MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv
MG_STRUCTURAL_AT_K_QC_SUMMARY_2026-08-26.csv
MG_STRUCTURAL_AT_K_TOP_BOTTOM_CASES_2026-08-26.csv
MG_STRUCTURAL_AT_K_INTERMEDIATE_NODES_2026-08-26.csv
MG_STRUCTURAL_AT_K_VALIDATION_REPORT.json
scripts/score_mg_structural_at_k.py
MANIFEST.sha256
```

Manifest verification:

```text
sha256sum -c MANIFEST.sha256 = all OK
```

Note: `MANIFEST.sha256` records 11 content files; including the manifest itself, the folder has 12 top-level/relevant deliverable files. This is only a wording distinction and not a validation issue.

## 3. Recomputed all-92 check

Recomputed from:

```text
MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv
```

Case-level rows:

```text
1472 = 92 evaluable cases × 4 tools × 4 K values
```

All tool × K groups contain exactly 92 rows.

Status counts:

```text
biotransformer_envmicro: 84 SCORED / 8 NO_PREDICTION
envipath_prediction:     87 SCORED / 5 NO_PREDICTION
eclipse_predec:          92 SCORED / 0 NO_PREDICTION
eclipse_noec optional:   92 SCORED / 0 NO_PREDICTION
```

The all-92 table retains `NO_PREDICTION` cases in the denominator. Recomputed values exactly match `MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv`.

Main all-92 macro values:

| tool | K | all-92 macro P | all-92 macro R | all-92 macro J |
|---|---:|---:|---:|---:|
| biotransformer_envmicro | 1 | 0.329 | 0.242 | **0.197** |
| biotransformer_envmicro | 3 | 0.203 | 0.396 | **0.154** |
| biotransformer_envmicro | 5 | 0.195 | 0.467 | **0.152** |
| envipath_prediction | 1 | 0.257 | 0.133 | 0.116 |
| envipath_prediction | 3 | 0.208 | 0.327 | 0.136 |
| envipath_prediction | 5 | 0.197 | 0.384 | 0.140 |
| eclipse_predec | 1 | 0.315 | 0.220 | 0.178 |
| eclipse_predec | 3 | 0.122 | 0.510 | 0.106 |
| eclipse_predec | 5 | 0.074 | 0.645 | 0.070 |
| eclipse_noec optional | 1 | 0.278 | 0.188 | 0.155 |
| eclipse_noec optional | 3 | 0.115 | 0.429 | 0.100 |
| eclipse_noec optional | 5 | 0.069 | 0.512 | 0.065 |

K=10 is present in the CSV as a wider exploratory supplement and should not be used as the primary conclusion.

## 4. Documentation check

README now correctly states:

```text
main teacher-facing table = all-92 inclusive macro
NO_PREDICTION cases are retained as zero-score cases
scored-only table is retained only as a coverage-conditional supplement
K=10 is supplemental
the evaluation is bounded to depth≤6
```

Method note now clearly separates:

```text
all-92 inclusive macro/micro = main table
scored-only macro/micro = supplement
```

The bounded-depth limitation is visible:

```text
15 evaluable BBD routes extend beyond depth 6;
because the returned prediction graph is bounded to depth 6,
this supplement evaluates depth≤6 structural recovery,
not full-depth terminal-route recovery for every case.
```

## 5. Script / reproducibility check

`scripts/score_mg_structural_at_k.py` now uses:

```text
tempfile.mkdtemp(prefix='mg_struct_extract_')
```

instead of reusing a fixed `/tmp/mg_struct_extract` directory.

Syntax check:

```text
python compile(...) = syntax_ok
```

Validation report flags are present and correct:

```text
reporting_supplement_added = true
main_teacher_facing_summary = all92_inclusive_macro
scored_only_summary_retained = true
bounded_depth_scoring = true
true_routes_with_max_depth_gt_6 = 15
stale_tmp_extract_fix_applied = true
final_status = PASS_READY_FOR_CODEX_REVIEW
```

## 6. Restricted answer leakage check

No restricted answer CSV/jsonl files are present in the teacher-facing MG supplement folder.

Checked:

```text
no __pycache__ files
no restricted/answer-like filenames
manifest clean
```

The method note and script contain descriptive local path/file references for reproducibility, but not raw restricted answer tables. This is acceptable for the current local/teacher-facing evidence folder.

## 7. Scientific interpretation

The corrected all-92 summary supports the following cautious conclusion:

```text
BioTransformer has the best overall MG-Structural@1/@3/@5 Jaccard.
ECLIPSE PREDEC has the highest recall, meaning it covers more true route nodes.
ECLIPSE PREDEC also produces many more false-positive branches, so its precision and Jaccard drop sharply as K increases.
enviPath is lower than BioTransformer overall but can exceed ECLIPSE PREDEC in Jaccard at wider K because it is less branch-explosive.
```

Plain-language conclusion:

这版补充已经把之前“撒大网碰到答案”的问题控制住了。现在主表不是只看有没有碰到真实节点，而是把 92 个可评分 case 都放进分母，同时惩罚错误分支。结果可以给老师看，但必须按“bounded depth≤6 的结构化多步评价”表述，不要说成完整矿化或全深度终点路线预测。

