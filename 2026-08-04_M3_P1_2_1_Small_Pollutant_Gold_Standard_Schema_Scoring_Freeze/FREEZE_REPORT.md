# Freeze Report

Final status: `M3_P1_2_1_GOLD_SCHEMA_SCORING_FREEZE_PASS`

## Source Paths Used

- Uploaded benchmark package: `/root/projects/EnzymeCAGE-master/HPC_Inputs/enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728.tar.gz`
- Equivalent gold source: `/tmp/enzymecage_m3_p1_2_1_gold_rerun1_xmv1ej44/enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728/restricted/POLLUTANT_DEGRADATION_STRICT_SINGLE_PARENT_RESTRICTED_ANSWER_KEY_V0_1.jsonl` and `/tmp/enzymecage_m3_p1_2_1_gold_rerun1_xmv1ej44/enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728/restricted/POLLUTANT_DEGRADATION_STRICT_SINGLE_PARENT_ACCEPTED_PRODUCTS_V0_1.csv` from extracted package
- Blind input source: `/tmp/enzymecage_m3_p1_2_1_gold_rerun1_xmv1ej44/enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728/benchmark/POLLUTANT_DEGRADATION_STRICT_SINGLE_PARENT_BLIND_INPUTS_V0_1.csv` from extracted package
- BioTransformer replay package: `/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_small_pollutant_strict_v0_1_biotransformer_envmicro_prediction_20260728.tar.gz`
- enviFormer replay package: `/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_small_pollutant_strict_v0_1_enviformer_latest_prediction_20260728.tar.gz`

The original fixed output path was already occupied by `/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_20260804` and was not overwritten. SHA256 and byte size identities are recorded in `inputs/SOURCE_FILE_IDENTITIES.tsv`.

## Counts

- case_count: 18
- reaction_row_count: 39
- product_row_count: 39

## Replay Status

- BioTransformer ENVMICRO: scored
- enviFormer latest: scored

## Replay Summary

| tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | product recall@10 | recovered products@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 0.500000 | 0.722222 | 0.888889 | 0.888889 | 0.619444 | 0.652778 | 20 |
| enviFormer latest | 0.000000 | 0.055556 | 0.055556 | 0.055556 | 0.027778 | 0.018519 | 1 |

## Limitations

- These 18 cases are a small curated benchmark, not the full pollutant universe.
- EAWAG-BBD/enviPath-known products do not guarantee prediction tools will recover them.
- This package does not choose the final reaction predictor until Gong model results are scored with the same script.
