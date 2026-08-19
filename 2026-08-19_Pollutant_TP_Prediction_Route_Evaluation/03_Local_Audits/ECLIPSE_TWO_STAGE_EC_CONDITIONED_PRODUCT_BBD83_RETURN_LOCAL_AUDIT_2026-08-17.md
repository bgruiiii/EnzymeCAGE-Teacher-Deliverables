# ECLIPSE Two-Stage EC-Conditioned Product Prediction BBD83 Return Local Audit

Date: 2026-08-17  
Archive:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m3_p1_2_1_bbd83_eclipse_two_stage_ec_conditioned_product_pilot_20260817.tar.gz
```

Archive SHA256:

```text
f59e1a221d91bd472e9e9f09784414c8714143741a783267ec3c2916bd765c5e
```

## 1. Verdict

Verdict:

```text
TECHNICAL_RUN_COMPLETE_BUT_PRODUCT_ACCURACY_LOW
```

The returned package is useful and contains real blind prediction outputs:

- EC-only predictions were produced for all 83 cases;
- No-EC product predictions were produced for 80/83 cases, with 3 empty/encoding failures;
- PredEC-conditioned product predictions were produced for all 83 cases;
- restricted answer files were not read on Chenyu/HPC according to the executor summary.

However, local scoring against the restricted v0.2 answer key shows that the
ECLIPSE two-stage PredEC route is much worse than the previous BioTransformer
ENVMICRO baseline on this BBD83 task.

## 2. Executor status

Final status:

```text
ECLIPSE_BBD83_TWO_STAGE_PRODUCT_PILOT_COMPLETE
```

Executor summary:

```text
restricted_answer_key_read = false
total_cases = 83
ec_completed_case_count = 83
no_ec_completed_case_count = 80
pred_ec_completed_case_count = 83
runtime_failure_count = 0
typed_blocker_count = 0
```

Model/assets reported:

```text
chem-eclipse v0.1.0
EC predictor = H-ECLIPSE, trained from Zenodo ecmap.csv
ECMap training reactions = 124,705
EC predictor training time = 138.1 sec CPU
Product Transformer = USPTO-pretrained TransformerModel
checkpoint = epoch=124-step=880875.ckpt
checkpoint_sha256 = a7b1d6d592078268f421d53d3a0710be5452b6ee42a3f040cee0c8ce7ae3e305
```

Important asset boundary:

```text
No official BBD-refined product model checkpoint was available in this run.
The product model used for scoring was the USPTO-pretrained Transformer, not a BBD/environment fine-tuned model.
```

## 3. Prediction coverage

Executor-reported candidate coverage:

| Route | Valid cases | Mean candidates | Median candidates | Notes |
|---|---:|---:|---:|---|
| EC-only | 83 / 83 | 1.13 ECs/case | - | 94 EC predictions total |
| No-EC product | 80 / 83 | 2.77 | 3.0 | 3 empty rows: c0367, c0526, c0939 |
| PredEC product | 83 / 83 | 2.84 | 3.0 | 236 product rows total |

No-EC empty cases:

```text
SPD-BBD2-PARENT-c0367  Benzonitrile
SPD-BBD2-PARENT-c0526  Acetylene
SPD-BBD2-PARENT-c0939  Hypophosphite
```

## 4. Local strict product scoring

Local scoring used the restricted BBD83 answer table after the blind executor
run returned:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m3_p1_2_1_bbd_known_pathway_benchmark_v0_2_local_build_20260805/
restricted/KNOWN_PATHWAY_POLLUTANT_ACCEPTED_PRODUCTS_V0_2.csv
```

Scoring rule:

```text
RDKit canonical exact product match
match by full InChIKey or canonical isomeric SMILES
case-level Hit@K = any accepted first-generation product appears in Top-K
product-level recovery = accepted product labels recovered among 148 labels
```

Strict scoring result:

| Route | Valid prediction cases | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product labels recovered @10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ECLIPSE No-EC Product Transformer | 80 / 83 | 3 / 83 = 3.6% | 4 / 83 = 4.8% | 4 / 83 = 4.8% | 4 / 83 = 4.8% | 0.0422 | 5 / 148 = 3.4% |
| ECLIPSE PredEC-conditioned Product Transformer | 83 / 83 | 2 / 83 = 2.4% | 2 / 83 = 2.4% | 2 / 83 = 2.4% | 2 / 83 = 2.4% | 0.0241 | 3 / 148 = 2.0% |

PredEC did not improve over No-EC. It reduced strict case-level hits from 4 to
2 and reduced product recovery from 5/148 to 3/148.

## 5. Comparison to BioTransformer baseline

Previous BioTransformer ENVMICRO baseline on the same BBD83 benchmark:

| Route | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product labels recovered @10 |
|---|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 28 / 83 = 33.7% | 40 / 83 = 48.2% | 50 / 83 = 60.2% | 50 / 83 = 60.2% | 0.428 | 60 / 148 = 40.5% |
| ECLIPSE PredEC product | 2 / 83 = 2.4% | 2 / 83 = 2.4% | 2 / 83 = 2.4% | 2 / 83 = 2.4% | 0.0241 | 3 / 148 = 2.0% |

Conclusion:

```text
ECLIPSE PredEC product is not competitive with BioTransformer ENVMICRO under the current ECMap + USPTO-pretrained configuration.
```

## 6. Paired NoEC vs PredEC product result

Strict hit cases:

```text
No-EC hits:
SPD-BBD2-PARENT-c1019
SPD-BBD2-PARENT-c1094
SPD-BBD2-PARENT-c1182
SPD-BBD2-PARENT-c1313

PredEC hits:
SPD-BBD2-PARENT-c1019
SPD-BBD2-PARENT-c1313
```

Paired strict classification:

| Category | Count |
|---|---:|
| both NoEC and PredEC hit | 2 |
| NoEC-only hit | 2 |
| PredEC-only hit | 0 |
| neither hit | 79 |

Interpretation:

- adding predicted EC did not rescue any case that No-EC missed;
- adding predicted EC removed two No-EC hits;
- this is a classic error-propagation pattern rather than an improvement.

## 7. EC prediction diagnostic

Using restricted answers locally after return, the predicted ECs were compared
against answer-table EC numbers at the EC-3 level.

Denominator:

```text
cases with answer EC information = 82 / 83
unique answer EC labels across cases = 116
```

ECLIPSE EC-3 result:

| Metric | Result |
|---|---:|
| EC3 Hit@1 | 9 / 82 = 11.0% |
| EC3 Hit@3 | 9 / 82 = 11.0% |
| EC3 Hit@10 | 9 / 82 = 11.0% |

EC3 hit cases:

```text
SPD-BBD2-PARENT-c0002
SPD-BBD2-PARENT-c0006
SPD-BBD2-PARENT-c0116
SPD-BBD2-PARENT-c0148
SPD-BBD2-PARENT-c0367
SPD-BBD2-PARENT-c0480
SPD-BBD2-PARENT-c1066
SPD-BBD2-PARENT-c1266
SPD-BBD2-PARENT-c1586
```

Interpretation:

- the predicted EC context is usually not aligned with the BBD answer EC family;
- therefore PredEC-conditioned product generation is likely being conditioned
  on the wrong enzyme class for most cases;
- this explains why PredEC product prediction did not improve over No-EC.

## 8. Training-overlap diagnostic

Executor-reported overlap against ECMap training data:

```text
total blind cases = 83
exact substrate overlap = 7 / 83 = 8.43%
overlap status categories in overlap_by_case.csv:
UNSEEN = 59
SEEN_IN_TRAINING = 24
```

Strict product scoring by overlap group:

| Route | Subset | Hit@1 | Hit@3/5/10 | MRR@10 | Product labels @10 |
|---|---|---:|---:|---:|---:|
| No-EC | ALL 83 | 3 / 83 | 4 / 83 | 0.0422 | 5 |
| No-EC | UNSEEN 59 | 2 / 59 | 2 / 59 | 0.0339 | 3 |
| No-EC | SEEN 24 | 1 / 24 | 2 / 24 | 0.0625 | 2 |
| PredEC | ALL 83 | 2 / 83 | 2 / 83 | 0.0241 | 3 |
| PredEC | UNSEEN 59 | 2 / 59 | 2 / 59 | 0.0339 | 3 |
| PredEC | SEEN 24 | 0 / 24 | 0 / 24 | 0.0000 | 0 |

Interpretation:

- the low PredEC score is not inflated by ECMap overlap;
- the seen/training-overlap subset did not produce PredEC hits;
- the current failure is primarily product/EC-domain mismatch, not a hidden
  success masked by strict unseen filtering.

## 9. Final interpretation

The experiment was worth running because it answered the real question:

```text
Does predicted EC context improve one-step product prediction on BBD83?
```

Current answer:

```text
No, not under the returned ECMap H-ECLIPSE + USPTO-pretrained Transformer configuration.
```

Main reasons:

1. The two-stage route technically runs and produces ranked product candidates.
2. The product model is only USPTO-pretrained, not BBD/environment fine-tuned.
3. EC prediction at the answer EC-3 level is low: 9/82.
4. PredEC conditioning causes error propagation and is worse than No-EC.
5. Both ECLIPSE routes are far below BioTransformer ENVMICRO on BBD83.

Recommended next step:

```text
Do not continue this exact configuration as a production or main reranker candidate.
```

Only consider further ECLIPSE work if one of the following becomes available:

- an official or reproducible BBD/environment-fine-tuned Product Transformer;
- a much better EC predictor for environmental degradation EC classes;
- a TrueEC oracle diagnostic showing that correct EC conditioning substantially
  improves product prediction, which would justify fixing the EC predictor;
- a controlled training setup that does not leak the BBD83 evaluation cases.

