# Codex review audit — BBD full-route v0.3/v3.1 MG-Structural@K supplement

Date: 2026-08-26  
Reviewer: Codex  
Reviewed folder:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/22_BBD_Full_Route_Tool_Comparison_2026-08-26/07_enviformer_style_mg_structural_at_k
```

## 1. Verdict

```text
CONDITIONAL_PASS_NEEDS_SMALL_REPORTING_SUPPLEMENT_BEFORE_TEACHER_FACING_USE
```

The implementation is broadly valid and much more scientifically appropriate than the earlier loose graph-coverage diagnostic because it adds:

- fixed per-step branch budget (`K = 1 / 3 / 5`, optional `10`);
- root exclusion;
- non-isomeric RDKit canonical matching;
- depth weighting (`1 / 2^depth`);
- FP penalty through weighted Precision / Recall / Jaccard;
- toy tests before real scoring;
- clear statement that this is not official probability-threshold enviFormer MG/AUPRC.

However, before this becomes the main teacher-facing table, it needs one small reporting supplement:

```text
Add all-92 inclusive macro/micro summaries where NO_PREDICTION cases remain in the denominator as zero-score cases.
```

Reason: the current `MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv` reports macro/micro over `SCORED` cases only. This is stated, but it is optimistic for tools with no-prediction cases and less ideal for cross-tool ranking.

## 2. File / boundary checks

Expected output files are present:

```text
README.md
MG_STRUCTURAL_AT_K_METHOD_NOTE_2026-08-26.md
MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv
MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv
MG_STRUCTURAL_AT_K_QC_SUMMARY_2026-08-26.csv
MG_STRUCTURAL_AT_K_TOP_BOTTOM_CASES_2026-08-26.csv
MG_STRUCTURAL_AT_K_INTERMEDIATE_NODES_2026-08-26.csv
MG_STRUCTURAL_AT_K_VALIDATION_REPORT.json
MANIFEST.sha256
scripts/score_mg_structural_at_k.py
```

Manifest check:

```text
sha256sum -c MANIFEST.sha256 = all OK
```

Restricted answer leakage check:

```text
No restricted answer CSV/jsonl files are copied into the teacher-facing folder.
```

The method note and script mention restricted local paths/file names for provenance and reproducibility, but do not include raw restricted answer content. This is acceptable if the teacher-facing package is meant to include reproducible local-scoring code; if a public/minimal package is later desired, the script can be moved to an audit-only folder and the README can keep only aggregate results.

## 3. Scope checks

Case-level row count:

```text
1472 = 92 evaluable cases × 4 tools × 4 K values
```

Status counts:

```text
biotransformer_envmicro: 84 SCORED / 8 NO_PREDICTION for each K
envipath_prediction:     87 SCORED / 5 NO_PREDICTION for each K
eclipse_predec:          92 SCORED / 0 NO_PREDICTION for each K
eclipse_noec optional:   92 SCORED / 0 NO_PREDICTION for each K
```

The original 93rd case, `FR-BBD3-CAND-c0105` Chlorobenzene, is excluded as the known zero-route-edge case, matching previous audits.

## 4. Method checks

Passed:

- uses `K = 1, 3, 5`, plus optional `10`;
- uses `max_depth = 6`;
- removes self-loop / parent-copy predictions;
- root is not scored;
- CO2 is excluded from main node scoring;
- prediction ranking is primarily based on rank fields, not incompatible cross-tool probabilities;
- FP is included in Precision and Jaccard denominators;
- intermediate handling is implemented in a limited/basic form and the lack of downstream depth correction is stated.

Important limitation to state more visibly:

```text
This is a bounded depth≤6 route-graph score, not full-depth BBD terminal-route scoring for every case.
```

Reason: 15 evaluable BBD parent cases have `max_depth_from_parent > 6` in the restricted parent summary. The scoring script builds true graphs with `MAX_DEPTH = 6`, so true nodes beyond depth 6 are outside this evaluation window.

Cases with BBD route depth greater than 6:

```text
FR-BBD3-PARENT-c0006  Gallate                         depth 9
FR-BBD3-PARENT-c0121  Benzoate                        depth 13
FR-BBD3-PARENT-c0288  2,4-Dichlorophenoxyacetic acid  depth 8
FR-BBD3-PARENT-c0375  p-Cymene                        depth 8
FR-BBD3-PARENT-c0388  Fluorene                        depth 7
FR-BBD3-PARENT-c0480  Bromoxynil                      depth 7
FR-BBD3-PARENT-c0626  Limonene                        depth 7
FR-BBD3-PARENT-c0865  2,4-Dichlorotoluene             depth 7
FR-BBD3-PARENT-c0941  Cyclohexane                     depth 10
FR-BBD3-PARENT-c1013  Citronellol                     depth 12
FR-BBD3-PARENT-c1078  Isooctane                       depth 13
FR-BBD3-PARENT-c1161  Isoniazid                       depth 7
FR-BBD3-PARENT-c1263  Asulam                          depth 7
FR-BBD3-PARENT-c1457  Malathion                       depth 7
FR-BBD3-CAND-c0141    gamma-Hexachlorocyclohexane     depth 7
```

This does not invalidate the result because prediction generation was also bounded to depth 6, but it must be described as bounded-depth structural evaluation.

## 5. Current reported summary and corrected all-92 view

The current README main table uses `macro = mean over SCORED cases`.

For cross-tool comparison, the stricter recommended teacher-facing view should also report `macro_all92 = mean over all 92 evaluable cases`, where `NO_PREDICTION` cases keep their zero Precision / Recall / Jaccard from the case-level file.

All-92 inclusive macro values recomputed from `MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv`:

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

All-92 interpretation:

- BioTransformer remains highest in macro Jaccard at K=1/3/5.
- ECLIPSE PREDEC remains highest in Recall, especially at K=5.
- ECLIPSE PREDEC Precision collapses as K increases because many FP branches are produced.
- enviPath is lower than BioTransformer but can exceed ECLIPSE PREDEC in Jaccard at K=3/5 because it produces fewer false positives.

Therefore, the main scientific conclusion is stable, but the teacher-facing table should include or switch to all-92 inclusive macro values to avoid optimistic scored-only reporting.

## 6. Additional reproducibility note

The scoring script uses:

```python
td = '/tmp/mg_struct_extract'
if os.path.isdir(td):
    return td
```

This can reuse stale extracted archive contents if the same temp directory already exists from a previous run. It should be repaired before final reproducibility handoff:

```text
Use tempfile.mkdtemp(...) or clear and recreate a run-specific extraction directory after validating the archive path/sha256.
```

This is not a numerical blocker for the current reviewed output, but it is a reproducibility hygiene issue.

## 7. Recommended required supplement / fix

Before using this in a final teacher-facing README, ask the local executor to add:

```text
MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv
```

and update `README.md` / `MG_STRUCTURAL_AT_K_METHOD_NOTE_2026-08-26.md` to state clearly:

```text
Main cross-tool comparison uses all 92 evaluable cases; no-prediction cases are counted as zero.
The existing scored-only table is retained as a coverage-conditional supplement.
The evaluation is bounded to depth≤6 because the prediction graph was generated to depth 6.
15 BBD answer routes extend beyond depth 6 and are not fully terminal-scored in this supplement.
```

Also repair the temp extraction behavior in `scripts/score_mg_structural_at_k.py`.

## 8. Bottom-line conclusion

```text
Core implementation: usable.
Current teacher-facing wording/table: needs small supplement.
Scientific conclusion after stricter all-92 check: still stable.
```

Plain-language summary:

这版已经把“撒大网碰到答案”的问题压下来了。现在不是只看有没有碰到真实节点，而是看预测图和真实路线图整体有多像，并惩罚乱分支。结果显示：BioTransformer 路线更保守但整体 Jaccard 最好；ECLIPSE PREDEC 找到真实节点最多，但错误分支太多，Precision 和 Jaccard 被明显拉低。下一步只需要补一个 all-92 主表和小的脚本复现修复，就可以进入最终报告整合。

