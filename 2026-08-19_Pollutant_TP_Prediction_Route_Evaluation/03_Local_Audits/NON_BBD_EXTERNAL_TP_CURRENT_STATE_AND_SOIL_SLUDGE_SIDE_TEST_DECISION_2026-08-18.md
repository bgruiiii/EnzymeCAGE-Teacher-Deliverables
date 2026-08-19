# NON-BBD external TP current state and soil/sludge side-test decision

Date: 2026-08-18  
Purpose: record the current state before switching to a chenyu-side soil/sludge test.

## 1. Current state

We are trying to build a non-BBD external transformation-product validation set for comparing:

```text
BioTransformer ENVMICRO
chem-eclipse BBD-finetuned PREDEC parent-filtered
enviPath prediction / lookup route
```

The immediate motivation is that the BBD83 benchmark is useful but not enough for a generalization claim, because it is BBD/enviPath-lineage.

## 2. What V1 has achieved

The latest returned V1 folder is:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/NON_BBD_EXTERNAL_TP_CLEAN_POOL_V1_20260818
```

Local audit:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/NON_BBD_EXTERNAL_TP_CLEAN_POOL_V1_RETURN_LOCAL_AUDIT_2026-08-18.md
```

V1 did not produce a final benchmark. It produced a cleaned candidate-pool draft:

| Pool | Rows | Unique parent canonical SMILES | Current use |
|---|---:|---:|---|
| clean_primary_pool | 5 | 3 | Very clean but too small |
| clean_reserve_pool | 478 | 245 | Useful mining pool, not directly ready |
| manual_review_pool | 40 | 24 | Needs DOI/source review |
| reject_pool | 58 | 29 | Not usable |

Main V1 blockers:

1. Summary files and executor audit have stale / inconsistent post-demotion counts.
2. Chenyu-side full enviPath soil/sludge overlap has not been completed.
3. Clean pools still contain duplicate parent-product pairs.
4. Clean primary is too small and narrow for a 10–20 case external benchmark by itself.

## 3. Decision: run a soil/sludge side test first

It is reasonable to run a separate chenyu-side soil/sludge test now, before finishing the stricter non-BBD external benchmark.

Reason:

- The chem-eclipse model we currently evaluated was BBD-finetuned.
- Soil and sludge datasets were not used in that BBD-only fine-tuning step, based on our current understanding.
- Therefore, soil/sludge can test whether the BBD-finetuned model transfers beyond BBD-style training data.

This test answers a practical question:

```text
Does the BBD-finetuned ECLIPSE model generalize to soil/sludge transformation-product cases?
```

## 4. Important boundary

This soil/sludge test should not be described as the final “strict non-BBD external benchmark”.

Why:

- Soil/sludge data may still be enviPath-lineage data.
- enviPath prediction / lookup routes may have source-side advantage on enviPath-derived soil/sludge cases.
- The test is most cleanly interpreted as cross-dataset evaluation for the BBD-finetuned ECLIPSE model, plus a useful comparison against BioTransformer and enviPath.

Suggested wording:

```text
soil/sludge side test = BBD-finetuned model cross-dataset transfer check
non-BBD external TP benchmark = still under construction
```

## 5. Recommended chenyu task

Ask chenyu to use the full soil/sludge transformation-product datasets already available there and produce a light audit result package.

Minimum requirements:

1. Identify the exact soil/sludge dataset files used.
2. Confirm whether these files were excluded from the BBD-only fine-tuning run.
3. Build a prediction/evaluation table from soil/sludge cases:
   - parent SMILES;
   - accepted product SMILES;
   - source dataset;
   - source row/reaction ID;
   - whether parent/product canonicalization succeeded;
   - whether parent appears in BBD83 or BBD fine-tune substrates.
4. Run the same compared routes if available:
   - BioTransformer ENVMICRO;
   - chem-eclipse BBD-finetuned PREDEC parent-filtered;
   - enviPath prediction / lookup, if available.
5. Report:
   - number of input rows;
   - number of valid canonicalized cases;
   - number after deduplicating exact parent-product pairs;
   - unique parent count;
   - Top-1 / Top-5 exact canonical product hit rate;
   - coverage / blocker counts per tool;
   - parent-copy or invalid-output counts;
   - a per-case result CSV.

## 6. Interpretation rule

If ECLIPSE performs well on soil/sludge:

- This supports that BBD fine-tuning learned transferable chemical transformation patterns.
- It does not by itself prove performance on a fully independent non-BBD literature benchmark.

If ECLIPSE performs poorly on soil/sludge:

- This suggests BBD-only fine-tuning may be too narrow.
- It motivates multi-source fine-tuning later, e.g. BBD + soil + sludge, followed by a separate held-out external set.

If BioTransformer outperforms ECLIPSE:

- That becomes an important baseline result.
- We should keep BioTransformer as the practical benchmark until ECLIPSE improves.

If enviPath performs best:

- Interpret carefully, because soil/sludge may be close to enviPath’s native data domain.

## 7. Current next step

Proceed with a chenyu soil/sludge side test, but keep it separate from the V1 non-BBD external benchmark construction.

Do not send V1 clean reserve wholesale to prediction yet.

Expected return location on chenyu:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
```

Expected local return location after copying back:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/
```
