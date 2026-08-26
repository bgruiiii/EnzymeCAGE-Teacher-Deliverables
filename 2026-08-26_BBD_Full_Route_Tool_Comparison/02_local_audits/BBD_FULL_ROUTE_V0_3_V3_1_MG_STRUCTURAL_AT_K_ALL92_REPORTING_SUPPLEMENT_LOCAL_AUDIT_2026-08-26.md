# Local audit — BBD full-route v0.3 v3.1 MG-Structural@K all-92 reporting supplement

Date: 2026-08-26
Protocol: `ENVIFORMER_MG_STRUCTURAL_AT_K_ADAPTED_BBD_FULL_ROUTE`
Supplement prompt: `LOCAL_BBD_FULL_ROUTE_MG_STRUCTURAL_AT_K_ALL92_REPORTING_SUPPLEMENT_PROMPT_2026-08-26.md`
Codex review audit: `BBD_FULL_ROUTE_V0_3_V3_1_ENVIFORMER_STYLE_MG_STRUCTURAL_AT_K_CODEX_REVIEW_AUDIT_2026-08-26.md`

## 1. Verdict

```text
PASS_READY_FOR_CODEX_REVIEW
```

The all-92 inclusive reporting supplement has been added. All cross-check values match. The stale tmp extraction fix is applied. The bounded depth≤6 limitation is stated. No hard-stop condition was triggered.

## 2. files_created

```text
MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv          (16 rows: 4 tools × 4 K)
MG_STRUCTURAL_AT_K_REPORTING_SUPPLEMENT_2026-08-26.md
```

## 3. files_updated

```text
README.md                                    (主表改用 all-92 inclusive macro)
MG_STRUCTURAL_AT_K_METHOD_NOTE_2026-08-26.md (新增 §12b all-92 vs scored-only；§13 加 bounded depth≤6 限制)
MG_STRUCTURAL_AT_K_VALIDATION_REPORT.json    (新增 reporting_supplement / bounded_depth / stale_tmp 字段)
MANIFEST.sha256                               (重新生成，含全部 12 个文件)
scripts/score_mg_structural_at_k.py           (修复 stale tmp extract + 加入 all-92 生成逻辑)
```

## 4. all-92 row count check

```text
case-level CSV rows = 1472 = 92 × 4 tools × 4 K   ✓
each tool × K group = 92 rows                     ✓
NO_PREDICTION rows retained in all-92 denominator  ✓
NO_PREDICTION rows all have zero tp/fp/precision/recall/jaccard (fn>0)  ✓
```

## 5. tool × K status counts

| tool | K | total | scored | no_prediction |
|---|---:|---:|---:|---:|
| biotransformer_envmicro | all | 92 | 84 | 8 |
| envipath_prediction | all | 92 | 87 | 5 |
| eclipse_predec | all | 92 | 92 | 0 |
| eclipse_noec | all | 92 | 92 | 0 |

## 6. all-92 macro values

| tool | K | macro_all92_P | macro_all92_R | macro_all92_J |
|---|---:|---:|---:|---:|
| biotransformer_envmicro | 1 | 0.329 | 0.242 | **0.197** |
| biotransformer_envmicro | 3 | 0.203 | 0.396 | **0.154** |
| biotransformer_envmicro | 5 | 0.195 | 0.467 | **0.152** |
| biotransformer_envmicro | 10 | 0.191 | 0.474 | 0.149 |
| envipath_prediction | 1 | 0.257 | 0.133 | 0.116 |
| envipath_prediction | 3 | 0.208 | 0.327 | 0.136 |
| envipath_prediction | 5 | 0.197 | 0.384 | 0.140 |
| envipath_prediction | 10 | 0.184 | 0.398 | 0.133 |
| eclipse_predec | 1 | 0.315 | 0.220 | 0.178 |
| eclipse_predec | 3 | 0.122 | 0.510 | 0.106 |
| eclipse_predec | 5 | 0.074 | 0.645 | 0.070 |
| eclipse_predec | 10 | 0.050 | 0.706 | 0.049 |
| eclipse_noec | 1 | 0.278 | 0.188 | 0.155 |
| eclipse_noec | 3 | 0.115 | 0.429 | 0.100 |
| eclipse_noec | 5 | 0.069 | 0.512 | 0.065 |
| eclipse_noec | 10 | 0.051 | 0.548 | 0.049 |

All values match the expected cross-check table in the supplement prompt §5 (3 decimal places).

## 7. all-92 micro values

| tool | K | micro_all92_P | micro_all92_R | micro_all92_J |
|---|---:|---:|---:|---:|
| biotransformer_envmicro | 1 | 0.352 | 0.192 | 0.142 |
| biotransformer_envmicro | 5 | 0.125 | 0.441 | 0.108 |
| eclipse_predec | 5 | 0.072 | 0.586 | 0.068 |
| envipath_prediction | 5 | 0.143 | 0.386 | 0.116 |

(Full 16-row micro values in the all-92 CSV.)

## 8. Checklist

```text
README updated = true                    (主表改为 all-92 inclusive macro)
method note updated = true               (§12b all-92 vs scored-only；§13 bounded depth≤6)
validation report updated = true         (reporting_supplement_added, bounded_depth_scoring, stale_tmp_extract_fix_applied 等)
manifest check result = PASS             (sha256sum -c all OK)
restricted answer leakage check = CLEAN  (teacher-facing 文件夹无 restricted answer 数据)
bounded depth≤6 limitation stated = true  (README §6, 方法说明 §13, validation report)
stale tmp extraction fix applied = true   (tempfile.mkdtemp 替代固定 /tmp 路径)
```

## 9. Manifest check

```text
sha256sum -c MANIFEST.sha256 = all OK
```

## 10. Restricted answer leakage check

```text
teacher-facing folder contains no restricted answer CSV/jsonl files = true
grep for restricted SMILES/compound IDs/edge IDs in output = 0 matches
only descriptive references (filenames, path constants) present = acceptable
```

## 11. Final conclusion

```text
PASS_READY_FOR_CODEX_REVIEW
```

The all-92 inclusive reporting supplement is complete, cross-checked, and reproducible. The main scientific conclusion is stable under the stricter all-92 view: BioTransformer has the highest MG-Structural Jaccard at K=1/3/5; ECLIPSE PREDEC has the highest recall but lowest precision. This supplement may proceed to Codex final review before teacher-facing integration.
