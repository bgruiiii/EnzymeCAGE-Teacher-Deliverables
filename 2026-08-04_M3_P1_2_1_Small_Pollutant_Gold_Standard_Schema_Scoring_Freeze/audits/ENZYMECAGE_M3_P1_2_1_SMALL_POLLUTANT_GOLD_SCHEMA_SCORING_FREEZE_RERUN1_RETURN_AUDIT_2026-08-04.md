# Local audit: small-pollutant gold standard / schema / scoring freeze rerun1 return

Date: 2026-08-04  
Audited return archive:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_rerun1_20260804.tar.gz
```

Identity file:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_rerun1_20260804.tar.gz.identity.txt
```

## Verdict

```text
AUDIT_VERDICT = PASS_WITH_DISCLOSED_LOCAL_RDKIT_LIMITATION
FINAL_STATUS = M3_P1_2_1_GOLD_SCHEMA_SCORING_FREEZE_PASS
TASK_SUCCESS = TRUE
```

The rerun1 return completes the requested F6-preparation asset:

- 18-case small-pollutant gold standard;
- blind parent input table;
- normalized three-tool prediction schema;
- reusable RDKit-based scoring script;
- validation script;
- replay scoring for BioTransformer ENVMICRO and enviFormer latest.

Local limitation: this workstation does not have RDKit installed, so the RDKit
canonicalization/scoring scripts were not rerun locally. The Chenyu validation
inside the package reports `rdkit_available=true`, `rdkit_version=2026.03.4`,
and `synthetic_scoring_runs=true`. Local audit independently checked archive
identity, file presence, counts, blind-column leakage, source identity, and
case-level summary consistency without RDKit.

## Archive identity

Local SHA256:

```text
archive_sha256 = 58feccb30056847acee41d2436263d770eea35a44d5d2d5a78e0ad20a06a3d3e
identity_sha256 = 64de3ec55d9b589adc1f154523ee261ef64c2c2b508b847a344b5a8e0eb7307c
```

Identity file records:

```text
archive_path   /root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_rerun1_20260804.tar.gz
archive_sha256 58feccb30056847acee41d2436263d770eea35a44d5d2d5a78e0ad20a06a3d3e
archive_bytes  26359
final_status   M3_P1_2_1_GOLD_SCHEMA_SCORING_FREEZE_PASS
created_utc    2026-08-04T08:14:12Z
```

The identity file hash matches the local archive hash.

## Required output presence

Required gold standard outputs are present:

```text
gold_standard/SMALL_POLLUTANT_STRICT_V0_1_GOLD_STANDARD_REACTIONS.csv
gold_standard/SMALL_POLLUTANT_STRICT_V0_1_GOLD_STANDARD_PRODUCTS.jsonl
gold_standard/SMALL_POLLUTANT_STRICT_V0_1_CASES.csv
gold_standard/SMALL_POLLUTANT_STRICT_V0_1_BLIND_PARENT_INPUTS.csv
```

Required schema outputs are present:

```text
schema/THREE_TOOL_PREDICTION_NORMALIZED_SCHEMA.md
schema/THREE_TOOL_PREDICTION_NORMALIZED_SCHEMA.json
```

Required scripts are present:

```text
scripts/score_three_tool_predictions.py        156 lines
scripts/validate_gold_schema_scoring_freeze.py  93 lines
```

Replay scoring outputs are present for both tools:

```text
replay/biotransformer_envmicro/CASE_LEVEL_SCORING.csv
replay/biotransformer_envmicro/PRODUCT_LEVEL_SCORING.csv
replay/biotransformer_envmicro/SCORING_SUMMARY.json
replay/biotransformer_envmicro/NORMALIZED_PREDICTIONS.jsonl

replay/enviformer_latest/CASE_LEVEL_SCORING.csv
replay/enviformer_latest/PRODUCT_LEVEL_SCORING.csv
replay/enviformer_latest/SCORING_SUMMARY.json
replay/enviformer_latest/NORMALIZED_PREDICTIONS.jsonl
```

## Source identity check

The rerun used the uploaded complete benchmark package:

```text
/root/projects/EnzymeCAGE-master/HPC_Inputs/
enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728.tar.gz
```

Chenyu source SHA256:

```text
94637b47f7f0f3c755e7bda2c023b45c8b4f178409d3c39c75573b4b118603e4
```

Local source package SHA256 independently matches:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/
ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/
03_HPC_Returned_Result_Summaries/
enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728.tar.gz
= 94637b47f7f0f3c755e7bda2c023b45c8b4f178409d3c39c75573b4b118603e4
```

Thus the gold-standard freeze used the intended local benchmark archive.

## Independent local count and leakage checks

Local non-RDKit CSV/JSONL checks found:

```text
gold reactions rows = 39
gold product rows   = 39
case rows           = 18
blind input rows    = 18
case ID sets match across reactions/cases/blind/products = true
```

Blind input columns:

```text
case_id
pollutant_name
parent_smiles
parent_inchikey
input_policy
```

No blind input column contains answer-like terms:

```text
product
reaction
answer
evidence
url
```

Therefore the blind input table is appropriate for Gong-model prediction and
does not leak product/reaction/evidence answers.

Gold product distribution by case:

```text
SPD-BBD-2,4-d  1
SPD-BBD-ala    1
SPD-BBD-atr    3
SPD-BBD-bpa    2
SPD-BBD-caf    3
SPD-BBD-cbf    3
SPD-BBD-dce    1
SPD-BBD-dmta   2
SPD-BBD-gly    1
SPD-BBD-mal    2
SPD-BBD-naph   2
SPD-BBD-nb     2
SPD-BBD-pha    4
SPD-BBD-pthn   2
SPD-BBD-pyr    3
SPD-BBD-tbp2   1
SPD-BBD-tce2   1
SPD-BBD-tol    5
```

## Replay scoring results

BioTransformer ENVMICRO:

```text
case_count                    18
prediction_count              72
accepted_product_count        39
Hit@1                         9/18  = 0.500000
Hit@3                         13/18 = 0.722222
Hit@5                         16/18 = 0.888889
Hit@10                        16/18 = 0.888889
MRR@10                        0.619444
recovered products @10        20/39
mean product recall @10       0.652778
```

enviFormer latest:

```text
case_count                    18
prediction_count              163
accepted_product_count        39
Hit@1                         0/18  = 0.000000
Hit@3                         1/18  = 0.055556
Hit@5                         1/18  = 0.055556
Hit@10                        1/18  = 0.055556
MRR@10                        0.027778
recovered products @10        1/39
mean product recall @10       0.018519
```

Local recomputation from `CASE_LEVEL_SCORING.csv` sums matches both
`SCORING_SUMMARY.json` files:

```text
BioTransformer: case_count=18, prediction_count=72,
hit_at_1_count=9, hit_at_3_count=13, hit_at_5_count=16,
hit_at_10_count=16, recovered_product_count_at_10=20

enviFormer: case_count=18, prediction_count=163,
hit_at_1_count=0, hit_at_3_count=1, hit_at_5_count=1,
hit_at_10_count=1, recovered_product_count_at_10=1
```

Interpretation: BioTransformer ENVMICRO substantially outperforms enviFormer
latest on this 18-case strict single-parent small-pollutant benchmark. This
does not yet choose the final fallback engine because Gong-model results still
need to be scored with the same script.

## Validation report

Chenyu validation reports:

```text
status = PASS
case_count = 18
reaction_row_count = 39
product_jsonl_count = 39
schema_json_parseable = true
synthetic_scoring_runs = true
biotransformer_envmicro_replay_case_count = 18
enviformer_latest_replay_case_count = 18
```

No validation errors are recorded.

## Boundary and limitations

1. The 18-case benchmark is curated and small; it is not a complete pollutant
   universe.
2. Database-known products do not imply prediction tools will recover them.
3. BioTransformer and enviFormer scores/beam ranks are not calibrated against
   each other; this package uses rank-based Hit@K/MRR/product recall.
4. Gong-model scoring is not included yet; this package is the reusable
   benchmark/scoring substrate for that later F6 closeout.
5. Local RDKit rerun was not possible because local Python lacks RDKit; the
   RDKit-dependent validation was performed on Chenyu.

## Audit conclusion

This rerun closes the “18 条污染物 gold standard 固化 / 统一评估脚本 /
三工具输出 schema 归一化定义” preparation step. It should be included in the
final teacher-deliverables evidence index after all remaining teacher-list
items are ready for unified GitHub synchronization.
