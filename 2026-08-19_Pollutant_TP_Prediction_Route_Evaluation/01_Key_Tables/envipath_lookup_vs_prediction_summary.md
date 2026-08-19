# Lookup vs Prediction Summary

## Headline Numbers (n=1788)

| Route | Type | Hit/Recover Count | Rate |
|-------|------|-------------------|------|
| enviPath local lookup | Oracle/known-pathway retrieval | 1788 found, 1788 all recovered | 100.0% found, 100.0% all recovered |
| ECLIPSE NoEC | Prediction (Hit@10) | 414 | 23.2% |
| ECLIPSE PREDEC | Prediction (Hit@10) | 474 | 26.5% |
| BioTransformer ENVMICRO | Prediction (Hit@10) | 553 | 30.9% |

## Interpretation

- enviPath local lookup is a **known-pathway oracle**, not a fair blind predictor.
- It can recover known Soil/Sludge records when the parent exists in the enviPath package.
- Prediction models (ECLIPSE, BioTransformer) are evaluated on blind prediction and should not be compared directly with lookup recall.
- This supports using enviPath as a known-pathway retrieval layer, not as a fair blind predictor on the same Soil/Sludge-derived evaluation set.
