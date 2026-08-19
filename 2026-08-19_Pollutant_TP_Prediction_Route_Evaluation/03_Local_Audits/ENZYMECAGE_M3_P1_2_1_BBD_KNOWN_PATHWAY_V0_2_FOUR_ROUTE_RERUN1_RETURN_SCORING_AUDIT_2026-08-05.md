# EnzymeCAGE M3 P1.2.1 BBD known-pathway v0.2 four-route blind rerun1 return scoring audit

Date: 2026-08-05  
Auditor: Codex local review  
Status: **PASS for returned-run integrity and local provisional scoring; not a final frozen benchmark claim**

## 1. Audited package

Returned archive:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_bbd_known_pathway_v0_2_four_route_blind_rerun1_20260805.tar.gz
```

Extracted directory:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_bbd_known_pathway_v0_2_four_route_blind_rerun1_20260805/
```

Archive SHA256:

```text
43b9de73788be0fb795dee732f11fcf2eb202c7362ee2611e4d6ce69d5a8b2c2
```

Returned status:

```text
FINAL_STATUS = M3_P1_2_1_BBD_KNOWN_PATHWAY_V0_2_FOUR_ROUTE_RERUN1_PASS
RUN_STATUS   = M3_P1_2_1_BBD_KNOWN_PATHWAY_V0_2_FOUR_ROUTE_RERUN1_PASS
```

HPC forbidden-source audit:

```text
restricted_answer_key_read=false
scoring_performed=false
only_blind_parent_inputs_used_for_cases=true
secret_fields_written=false
merged_from_original_local_routes_and_envipath_rerun1=true
```

Interpretation: Chenyu/HPC side only used blind parent inputs and did not read the restricted answer key. Therefore, local scoring against the restricted answer key is valid.

## 2. Benchmark and scoring boundary

Local answer package used for scoring:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_bbd_known_pathway_benchmark_v0_2_local_build_20260805/
```

Key files:

```text
blind/KNOWN_PATHWAY_POLLUTANT_BLIND_PARENT_INPUTS_V0_2.csv
restricted/KNOWN_PATHWAY_POLLUTANT_ACCEPTED_PRODUCTS_V0_2.csv
restricted/KNOWN_PATHWAY_POLLUTANT_RESTRICTED_ANSWER_KEY_V0_2.jsonl
BUILD_REPORT.json
VALIDATION_REPORT.json
```

Benchmark size:

- 83 parent-level blind cases
- 148 accepted first-generation product labels
- Source: EAWAG-BBD legacy pathway / compound / reaction pages
- Input to tools: parent compound SMILES only

Important boundary: this v0.2 set is a **provisional / canary known-pathway benchmark**, not a final teacher-facing frozen benchmark. The parent-selection audit has already found recoverable missing cases, so the present score is useful for route comparison and debugging, but final claims should wait for v0.2.1 or another audited freeze.

Parent-selection audit note:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/00_Authority_Teacher_Plan/ENZYMECAGE_M3_P1_2_1_BBD_KNOWN_PATHWAY_V0_2_PARENT_SELECTION_AUDIT_2026-08-05.md
```

## 3. Routes audited

Prediction routes:

1. BioTransformer ENVMICRO one-step prediction
2. enviFormer latest-current one-step prediction
3. enviPath Global Setting - BBD Rules one-step prediction

Separate non-prediction route:

4. enviPath database lookup / direct search

The returned merged report explicitly marks:

```text
prediction_accuracy_includes_database_lookup = false
```

Therefore, database lookup is reported as known-pathway retrieval coverage, not mixed into prediction Hit@K accuracy.

## 4. Local scoring method

Scoring was performed locally with RDKit 2026.03.5 in:

```text
/tmp/enzymecage_rdkitcheck_20260805
```

Matching rule:

- normalize accepted product SMILES and predicted product SMILES with RDKit;
- match by full InChIKey or canonical isomeric SMILES;
- for a parent case with multiple accepted first-generation products, count the case as Hit@K if any accepted product appears in the top K predictions;
- also compute product-level recovery to show whether multi-answer cases are only partially recovered.

Evidence outputs:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/evidence/m3_p1_2_1_bbd_known_pathway_v0_2_four_route_rerun1_scoring_20260805/
```

Main evidence files:

```text
prediction_route_scoring_summary.csv
prediction_route_case_level_scoring.csv
prediction_route_category_breakdown.csv
envipath_database_lookup_coverage_summary.csv
SCORING_METHOD.json
```

## 5. Main prediction-route results

| Route | Cases with any prediction | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product labels recovered @10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 76 / 83 | 28 / 83 = 33.7% | 40 / 83 = 48.2% | 50 / 83 = 60.2% | 50 / 83 = 60.2% | 0.428 | 60 / 148 = 40.5% |
| enviPath BBD Rules prediction | 79 / 83 | 20 / 83 = 24.1% | 35 / 83 = 42.2% | 42 / 83 = 50.6% | 43 / 83 = 51.8% | 0.343 | 60 / 148 = 40.5% |
| enviFormer latest-current | 82 / 83 | 1 / 83 = 1.2% | 1 / 83 = 1.2% | 2 / 83 = 2.4% | 3 / 83 = 3.6% | 0.016 | 4 / 148 = 2.7% |

Conclusion for prediction: **BioTransformer ENVMICRO is the best route in this provisional 83-case v0.2 BBD known-pathway test.** enviPath BBD Rules prediction is second and has some complementary hits. enviFormer latest-current is not suitable as the main route under this one-step pollutant known-pathway setting.

## 6. BioTransformer vs enviPath prediction complementarity

At Hit@10:

- BioTransformer and enviPath both hit: 36 cases
- BioTransformer only: 14 cases
- enviPath prediction only: 7 cases
- neither prediction route hit: 26 cases

Examples of BioTransformer-only Hit@10 cases:

- Glyphosate
- beta-1,2,3,4,5,6-Hexachlorocyclohexane
- 2,4-Dichlorophenoxyacetic acid
- cis-1,3-Dichloropropene
- Furfural

Examples of enviPath-prediction-only Hit@10 cases:

- Gallate
- Ethylbenzene
- p-Cymene
- Dibenzo-p-dioxin
- Acetylene
- Limonene
- Bisphenol F

Interpretation: BioTransformer is still the stronger default prediction route, but enviPath rule prediction is not useless; it may provide a useful secondary candidate source or fallback/rerank evidence.

## 7. Category-level pattern

BioTransformer was strongest overall and led most categories by Hit@10:

- halogenated compounds: 12 / 17 Hit@10 = 70.6%
- triazine herbicides: 2 / 2 Hit@10 = 100%
- plasticizer / flame retardant / endocrine-related cases: 2 / 3 Hit@10 = 66.7%
- other EAWAG-BBD xenobiotic cases: 27 / 51 Hit@10 = 52.9%

enviPath BBD Rules prediction was competitive in some aromatic / rule-covered cases:

- aromatic xenobiotic cases: 2 / 3 Hit@10 = 66.7%
- organophosphorus pesticide: 1 / 1 Hit@10 = 100%
- nitroaromatic: 1 / 1 Hit@10 = 100%

enviFormer produced many predictions but almost no exact known-pathway first-generation product recovery:

- 769 normalized prediction rows
- only 3 / 83 Hit@10
- 4 / 148 accepted product labels recovered @10

This suggests the issue is not simply “no output”; the generated products are mostly not the BBD-observed first-generation products.

## 8. enviPath database lookup route

Database lookup is not prediction, but it is important for system design.

Lookup result:

- 83 / 83 cases returned database lookup status `ok`
- 83 / 83 had matched compound count > 0
- 83 / 83 had matched pathway count > 0
- 83 / 83 had matched reaction count > 0
- total matched reactions: 189

Matched-reaction count distribution:

```text
1 reaction: 37 cases
2 reactions: 17 cases
3 reactions: 14 cases
4 reactions: 7 cases
5 reactions: 4 cases
6 reactions: 3 cases
10 reactions: 1 case
```

Interpretation: for this EAWAG-BBD-derived known-pathway set, direct enviPath/BBD database lookup can recover database connectivity for all tested parents. This supports the design idea:

1. first query known pathway databases when the pollutant is already represented;
2. use prediction tools for missing / novel / not-yet-curated compounds;
3. keep prediction scores separate from database evidence, because “known database retrieval” and “blind product prediction” answer different questions.

## 9. Recommendation after this audit

For the current provisional v0.2 result:

1. **Prediction winner:** BioTransformer ENVMICRO.
2. **Useful secondary prediction evidence:** enviPath BBD Rules prediction, because it recovers 7 Hit@10 cases that BioTransformer missed.
3. **Not recommended as main predictor:** enviFormer latest-current in the current one-step pollutant setting.
4. **Potential system architecture:** database lookup first, prediction second. This should be discussed with the teachers because it changes the product from “pure prediction” to “known-pathway retrieval + prediction fallback.”
5. **Next benchmark step:** fix v0.2 parent-selection incompleteness and make a v0.2.1/v0.3 freeze before making teacher-facing final performance claims.

## 10. Residual risks / not yet claimed

- This score does not prove performance on unseen pollutants. EAWAG-BBD/enviPath/BioTransformer may have training or rule-source overlap.
- The v0.2 benchmark needs correction because the parent-selection audit found recoverable missing cases.
- The database lookup result should not be presented as prediction accuracy.
- Matching used exact RDKit structure identity. It does not credit near-misses, downstream second-generation products, or mechanistically plausible but non-BBD-listed products.

