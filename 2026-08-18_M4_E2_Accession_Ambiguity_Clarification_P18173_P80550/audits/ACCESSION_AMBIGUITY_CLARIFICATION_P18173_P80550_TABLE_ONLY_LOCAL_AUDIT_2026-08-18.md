# Local audit: P18173 / P80550 accession ambiguity clarification

Date: 2026-08-18

Verdict: PASS as record-only clarification package.

## Authority alignment

Teacher file `TEACHER_REPLY_C7_2_FREEZE_AND_1650_ACCESSION_REVIEW_2026-08-17.md` asked for two clarifications:

1. `P18173`: explain the `Q8SXV0` versus `U3PT72` selection rule and sequence consistency against original 625aa.
2. `P80550`: trace the source of original 38aa sequence.

The generated package answers only those two questions and keeps both cases unresolved.

## Package audited

`01_Path_Contract_Objective/ChenHaoran_2026_08_18_Accession_Ambiguity_Clarification/ACCESSION_AMBIGUITY_CLARIFICATION_P18173_P80550_TABLE_ONLY_2026-08-18/`

Files:

- `ACCESSION_AMBIGUITY_CLARIFICATION_TABLE.csv`
- `P18173_P80550_ACCESSION_CLARIFICATION_REPORT.md`
- `NO_MUTATION_CHECK.json`
- `FINAL_STATUS.txt`

## Evidence checks

### P18173

- Frozen source sequence exists in `data/processed/rhea/2026-01-21/all_enzymes.csv`.
- Frozen source length = 625aa.
- Frozen source SHA256 = `d11ccd80851a3c77b9f0c3f92b9d1aba032640a94bd89be57cfb25819c06d077`.
- Current UniProt REST JSON reports primary `P18173` and secondary accessions in order `A0A2U8U0K3`, `Q8SXV0`, `Q9VI87`, `U3PT72`.
- Current UniProt FASTA length = 612aa, SHA256 = `a72a6f819114b51a601f8a991fd74d6a294707ccbcbea36767047c3124e117e1`.
- Prior 1,650 table shows AFDB v6 available for `Q8SXV0` and `U3PT72`, with `Q8SXV0` recorded.
- The selection is explained by deterministic probe order: primary first, then secondary accessions in UniProt-returned order, first HTTP 200 recorded.
- Sequence comparison confirms non-identity to original 625aa, so no closure is authorized or implied.

### P80550

- Frozen source sequence exists in `data/processed/rhea/2026-01-21/all_enzymes.csv`.
- Frozen source sequence also appears in `rhea_rxn2uids.csv`, `enzyme_feature_backfill_input.csv`, and `enzyme_pocket_backfill_input.csv`.
- Frozen source length = 38aa.
- Frozen source SHA256 = `84fd983f3da8dc6ae5918033f3c7e2cb6fd1f38ed02d5ed2ae97a1793d528197`.
- Current UniProt FASTA length = 704aa, SHA256 = `1f228bfcdcfa220e038cbbb18e2d32246347749432275e8d0e4ca571912d5404`.
- AFDB `F1RSB4` v6 exists but is not sequence-identical to the original 38aa source sequence.
- The package correctly treats the 38aa sequence as a frozen-snapshot short-fragment/anomalous source sequence and keeps `P80550` unresolved.

## Boundary checks

PASS:

- No UID replacement claimed.
- No asset generation claimed.
- No formal asset mutation claimed.
- No production pool mutation claimed.
- No production D4 mutation claimed.
- No candidate closure claimed for `P18173` or `P80550`.

Residual risk:

- Current UniProt/AFDB live endpoints were used for read-only evidence. If teacher requires fully frozen endpoint snapshots, the exact HTTP response payloads can be packaged separately, but this package does not depend on them for any production mutation.
