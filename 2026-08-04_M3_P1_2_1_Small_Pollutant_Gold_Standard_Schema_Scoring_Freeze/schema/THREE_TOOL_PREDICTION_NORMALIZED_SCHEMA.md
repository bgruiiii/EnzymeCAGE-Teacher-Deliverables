# Three-Tool Prediction Normalized Schema

One JSON object per predicted product. Required fields:

- `tool_name`
- `tool_version`
- `run_id`
- `case_id`
- `parent_smiles`
- `prediction_rank`
- `predicted_product_smiles_original`
- `predicted_product_smiles_canonical`
- `predicted_product_inchikey`
- `raw_score`
- `raw_confidence`
- `provenance`
- `raw_output_ref`
- `normalization_status`
- `normalization_note`

Rules:

- `prediction_rank` is 1-based per case.
- `raw_score` and `raw_confidence` may be blank when absent.
- BioTransformer score, enviFormer beam order, and Gong-model score are not calibrated against each other by this contract.
- Ranking metrics use `prediction_rank`, not raw score.
- Invalid predicted product SMILES must be retained with `normalization_status=invalid_smiles` and cannot count as hits.
