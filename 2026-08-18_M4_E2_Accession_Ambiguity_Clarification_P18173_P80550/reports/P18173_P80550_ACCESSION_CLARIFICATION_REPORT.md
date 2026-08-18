# P18173 / P80550 accession clarification report

Date: 2026-08-18

Authority: `TEACHER_REPLY_C7_2_FREEZE_AND_1650_ACCESSION_REVIEW_2026-08-17.md`

Scope: table-only clarification for the two teacher-flagged uncertain accession candidates from the 1,650 fetch-failed accession secondary review. This package does not replace UID, generate assets, mutate formal assets, mutate production pool, or mutate production D4.

## Teacher request addressed

Teacher accepted the 1,650 accession review as table-only closed, but marked two candidate cases as unresolved:

- `P18173`: explain why `Q8SXV0` was selected instead of `U3PT72`, and compare against the original 625aa sequence.
- `P80550`: trace the source of the original 38aa sequence.

## Inputs checked

Local frozen source snapshot:

- `data/processed/rhea/2026-01-21/all_enzymes.csv`
- `custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/07_HPC_Prompts/enzymecage_m4_phase1_acceptance_payload_20260811/f3_source_snapshot/data/processed/rhea/2026-01-21/all_enzymes.csv`
- `data/processed/rhea/2026-01-21/rhea_rxn2uids.csv`
- `data/processed/rhea/2026-01-21/asset_reuse/enzyme_feature_backfill_input.csv`
- `data/processed/rhea/2026-01-21/asset_reuse/enzyme_pocket_backfill_input.csv`
- `data/processed/rhea/2026-01-21/asset_reuse/alphafill_resume/run/remaining_status.csv`

Prior accession-review return package:

- `enzymecage_m4_e2_fetch_failed_1650_accession_secondary_review_manifest_fix_20260816.tar.gz`
- `FULL_1650_ACCESSION_SECONDARY_REVIEW_TABLE.csv`
- `ACCESSION_CANDIDATE_ONLY_TABLE.csv`

Official live endpoints checked only for read-only evidence:

- UniProt REST FASTA/JSON for `P18173`, `Q8SXV0`, `U3PT72`, `P80550`, `F1RSB4`
- AlphaFold DB v6 PDB HEAD/SEQRES for `P18173`, `Q8SXV0`, `U3PT72`, `P80550`, `F1RSB4`

## Result summary

| UID | Teacher issue | Clarification | Status |
| --- | --- | --- | --- |
| `P18173` | Why `Q8SXV0`, not `U3PT72`; compare to original 625aa | The previous script selected `Q8SXV0` because it probes primary accession first, then UniProt secondary accessions in returned order. UniProt returned secondary accessions as `A0A2U8U0K3`, `Q8SXV0`, `Q9VI87`, `U3PT72`; `Q8SXV0` is the first AFDB v6 HTTP 200 hit. This is a deterministic table rule, not a biological preference. Original 625aa differs from current UniProt canonical 612aa by an extra terminal `URVDATWTLHRVI`; AFDB `Q8SXV0` and `U3PT72` are both 612aa, so neither matches the original 625aa sequence exactly. | Keep unresolved; record-only; do not use for closure without teacher authorization. |
| `P80550` | Source of original 38aa | The 38aa sequence `GDKYRXIXGRXNNVDXEKTXAQLPPXFPIKIPPNDXRI` is already present in the frozen 2026-01-21 processed Rhea/UniProt enzyme snapshot and propagated into downstream backfill manifests. It is not introduced by the 1,650 review script. Current UniProt `P80550` canonical is 704aa, while AFDB `F1RSB4` PDB has 705 residues. The original 38aa should therefore be treated as a legacy short-fragment/anomalous source sequence for this pipeline snapshot. | Keep unresolved; record-only; do not use for closure without teacher authorization. |

## P18173 details

Original sequence evidence:

- Source row: `all_enzymes.csv`
- Length: 625aa
- SHA256: `d11ccd80851a3c77b9f0c3f92b9d1aba032640a94bd89be57cfb25819c06d077`

Current UniProt evidence:

- Primary accession: `P18173`
- Current FASTA length: 612aa
- Current FASTA SHA256: `a72a6f819114b51a601f8a991fd74d6a294707ccbcbea36767047c3124e117e1`
- Secondary accession order returned by UniProt JSON: `A0A2U8U0K3`, `Q8SXV0`, `Q9VI87`, `U3PT72`

Prior 1,650 review probe evidence:

- `P18173`: AFDB v6 404
- `A0A2U8U0K3`: AFDB v6 404
- `Q8SXV0`: AFDB v6 200
- `Q9VI87`: AFDB v6 404
- `U3PT72`: AFDB v6 200

The prior script recorded `Q8SXV0` because it was the first HTTP 200 candidate in the deterministic probe list. That rule is sufficient to explain the table entry, but it is not sufficient to justify asset use.

Sequence comparison:

- Original 625aa versus current UniProt canonical 612aa: original has an extra terminal `URVDATWTLHRVI`.
- AFDB `Q8SXV0` PDB SEQRES: 612 residues; differs from original by the missing terminal 13aa plus two residue differences.
- AFDB `U3PT72` PDB SEQRES: 612 residues; matches current UniProt canonical SHA256, but still lacks the original terminal 13aa.

Conclusion for `P18173`: `Q8SXV0` selection was a deterministic accession-order artifact. Because the original 625aa sequence does not exactly match the current canonical sequence or either AFDB candidate structure sequence, `P18173` remains unresolved and should not enter any closure path without a separate teacher decision.

## P80550 details

Original sequence evidence:

- Source row: `all_enzymes.csv`
- Length: 38aa
- SHA256: `84fd983f3da8dc6ae5918033f3c7e2cb6fd1f38ed02d5ed2ae97a1793d528197`
- Sequence: `GDKYRXIXGRXNNVDXEKTXAQLPPXFPIKIPPNDXRI`

Local propagation evidence:

- `rhea_rxn2uids.csv` also carries `P80550` with the same 38aa sequence.
- `enzyme_feature_backfill_input.csv` carries `P80550` with length 38.
- `enzyme_pocket_backfill_input.csv` carries `P80550` with length 38.
- `alphafill_resume/run/remaining_status.csv` records AlphaFill 404 for `P80550`.

Current UniProt / AFDB evidence:

- Current UniProt primary accession: `P80550`
- Current UniProt secondary accessions: `F1RSB4`
- Current UniProt canonical length: 704aa
- Current UniProt canonical SHA256: `1f228bfcdcfa220e038cbbb18e2d32246347749432275e8d0e4ca571912d5404`
- AFDB `P80550` v6: 404
- AFDB `F1RSB4` v6: 200, PDB SEQRES has 705 residues

Conclusion for `P80550`: the 38aa sequence comes from the frozen 2026-01-21 processed enzyme snapshot and was propagated before the accession secondary review. It is a legacy short-fragment/anomalous source sequence relative to current UniProt, not a valid sequence-identical basis for using `F1RSB4`.

## Boundary statement

This clarification is record-only. It does not change any of the following:

- `replacement_performed = False`
- `asset_generation_started = False`
- `formal_assets_mutated = False`
- `production_pool_mutated = False`
- `production_d4_mutated = False`

Both teacher-flagged uncertain cases remain blocked from closure until a separate teacher authorization.
