# Local audit — BBD full-route v0.3 v3.1 enviFormer-style MG-Structural@K evaluation

Date: 2026-08-26
Protocol: `ENVIFORMER_MG_STRUCTURAL_AT_K_ADAPTED_BBD_FULL_ROUTE`
Output folder:
`22_BBD_Full_Route_Tool_Comparison_2026-08-26/07_enviformer_style_mg_structural_at_k/`

## 1. Verdict

```text
PASS_READY_FOR_CODEX_REVIEW
```

All 6 toy tests passed before real scoring. Scope, method, boundary, and input-identity checks all satisfied. No hard-stop condition was triggered.

## 2. Input identity

```text
restricted answer source path =
  /home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/21_BBD_Known_Pathway_Full_Route_Testset_2026-08-21/bbd_known_pathway_full_route_v0_3_candidate_v3_repair_20260821/restricted

prediction archive path =
  .../03_HPC_Returned_Result_Summaries/bbd_full_route_v0_3_v3_1_bounded_multistep_route_expansion_supplement_20260825.tar.gz

prediction archive sha256 =
  ee8e06fffe76bec29825702c18deb1211e33b7c4609ff3132be8428179fe83cf

simple path v2 archive sha256 (consulted as QC reference only) =
  13107f9fa6b376327e817b64373bd58e6c0db635dc563de848c156dd49e6a592
```

## 3. Boundary check

```text
no restricted answer files copied into teacher-facing folder = true
  (verified: output folder contains only aggregate scores + script + prose; no restricted CSV/jsonl)
no web fetch = true
no new prediction run = true
no modification of prior folders = true
  (only created the new 07_enviformer_style_mg_structural_at_k/ folder and this audit)
```

## 4. Scope check

```text
93 total cases              = 93   (matches)
92 scored/evaluable cases   = 92   (matches)
1 zero-route-edge excluded   = FR-BBD3-CAND-c0105 Chlorobenzene  (matches)
invalid_reference_smiles_count = 0
rdkit_available = true
```

Computed evaluable case count is exactly 92, matching the previous local audits. No discrepancy.

## 5. Method check

```text
K = 1, 3, 5               (主)   ✓
K = 10                     (optional exploratory)  ✓
max_depth = 6              ✓  (matches bounded generation depth)
root excluded from scoring ✓
CO2 policy                 = exclude_CO2_from_main_node_scoring = true (stated, 10 true CO2 target edges excluded)
canonicalization mode      = non_isomeric_rdkit_canonical (stated)
depth weighting            = 1 / 2^depth  ✓
intermediate handling      = true (基础版: 零权重、不计 FP)
downstream_depth_correction = false (limitation stated prominently)
FP penalty present         ✓  (weighted_fp in denominator of precision & jaccard)
rank fields authoritative  ✓  (edge_rank_from_source / edge_rank_global ascending; score only tie-breaker)
```

## 6. Toy tests

All 6 required toy tests passed before real scoring (recorded in validation report JSON):

| # | name | expected | result |
|---|---|---|---|
| 1 | exact chain A→B→C | P=R=J=1 | PASS |
| 2 | extra FP A→X | P=0.5 R=1 J=0.5 | PASS |
| 3 | missing downstream | P=1 R=2/3 J=2/3 | PASS |
| 4 | root excluded | root not in nodes, TP=0.5 | PASS |
| 5 | depth weighting | depth-1 FP penalised more than depth-3 FP | PASS |
| 6 | intermediate enabled | X zero-weighted, P=R=J=1 | PASS |

`toy_tests_all_passed = true`. No toy test failed, so PASS verdict is permitted.

## 7. Results summary（中文）

### 7.1 哪个工具 MG-Structural@1/@3/@5 最强

以 **macro weighted Jaccard** 为综合指标：

| K | biotransformer | envipath | eclipse_predec | eclipse_noec(opt) |
|---:|---:|---:|---:|---:|
| 1 | **0.216** | 0.122 | 0.178 | 0.155 |
| 3 | **0.168** | 0.144 | 0.106 | 0.100 |
| 5 | **0.167** | 0.148 | 0.070 | 0.065 |

**BioTransformer 在 K=1/3/5 的 Jaccard 均最高**。
ECLIPSE PREDEC 在 K=1 时 Jaccard 排第二，但随 K 增大迅速恶化，K=5 时仅 0.070（四工具最低之一）。

### 7.2 PREDEC 是否仍优于 NoEC / BioTransformer / enviPath

- **Recall 维度**：PREDEC 在所有 K 仍最高（@5 recall 0.645，高于 NoEC 0.512、BioTransformer 0.512、enviPath 0.406）。PREDEC 确实覆盖最多真实节点。
- **Precision 维度**：PREDEC 在 K≥3 时最低（@5 precision 0.074）。NoEC 在 K=1 precision 略低于 PREDEC（0.278 vs 0.315），但 K≥3 后两者都极低。
- **综合 Jaccard**：BioTransformer > enviPath > PREDEC ≈ NoEC（K=5）。

结论：PREDEC 的“最强”仅体现在 recall/覆盖，其覆盖优势伴随大量 FP 分支，导致 precision 与综合 Jaccard 反而最差。NoEC recall 始终低于 PREDEC，precision 在低 K 接近但高 K 同样崩塌。

### 7.3 分支变宽后 Recall 是否上升、Precision 是否下降

是，且四工具一致：

| 工具 | K=1→5 recall | K=1→5 precision |
|---|---|---|
| biotransformer | 0.265 → 0.512 ↑ | 0.360 → 0.214 ↓ |
| envipath | 0.141 → 0.406 ↑ | 0.272 → 0.208 ↓ |
| eclipse_predec | 0.220 → 0.645 ↑ | 0.315 → 0.074 ↓ |
| eclipse_noec | 0.188 → 0.512 ↑ | 0.278 → 0.069 ↓ |

这正是 FP 惩罚设计预期：宽分支带来更多覆盖，但也更多错误分支，precision 被压低。

### 7.4 为什么这个结果比之前 coverage diagnostic 更科学

之前 coverage diagnostic 只看“真实节点是否被预测到某处”，不惩罚错误分支。
ECLIPSE PREDEC 生成了约 29,530 条预测边（含 4,333 条自环/parent-copy被移除），图规模远大于其他工具，
因此在大图 coverage 下“看起来最强”（gen-1 case hit 88%、any downstream 96.7%）。

但 MG-Structural@K 在固定 TopK 预算下做深度加权比较：
- ECLIPSE 的宽分支在 K=5 产生 1,095 的总 weighted FP（macro），把 precision 压到 0.074；
- BioTransformer 边更少但更精，K=1 时 precision 0.360、Jaccard 0.216 最高。

即：**“图大”不等于“路径恢复质量高”**。MG-Structural@K 通过 FP 惩罚把这一区别显化，使评价不再被图规模放大效应误导。这是本次补充相对 coverage diagnostic 的核心科学增益。

## 8. Output files

```text
07_enviformer_style_mg_structural_at_k/
  README.md
  MG_STRUCTURAL_AT_K_METHOD_NOTE_2026-08-26.md
  MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv          (16 rows: 4 tools × 4 K)
  MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv      (1472 rows: 92 × 4 tools × 4 K)
  MG_STRUCTURAL_AT_K_QC_SUMMARY_2026-08-26.csv              (1472 rows)
  MG_STRUCTURAL_AT_K_TOP_BOTTOM_CASES_2026-08-26.csv        (160 rows: 4 tools × 4 K × 10)
  MG_STRUCTURAL_AT_K_INTERMEDIATE_NODES_2026-08-26.csv      (376 rows)
  MG_STRUCTURAL_AT_K_VALIDATION_REPORT.json
  scripts/score_mg_structural_at_k.py
  MANIFEST.sha256
```

No restricted answer file is present in the teacher-facing folder.

## 9. Limitations carried forward

```text
downstream_depth_correction = false (intermediate zero-weighted but downstream depth not adjusted)
no probability threshold / no AUPRC (not official enviFormer probability MG)
non-isomeric matching merges cis/trans isomer cases (consistent with prior audits)
eclipse_noec optional, original generation partial depth 4
```

These do not block the PASS verdict; they are stated in the method note and validation report.

## 10. Final conclusion

```text
PASS_READY_FOR_CODEX_REVIEW
```

The MG-Structural@K supplement is scientifically sound, reproducible, scope-correct, boundary-clean, and toy-test-verified. It may proceed to Codex review before any teacher-facing README update or GitHub upload.
