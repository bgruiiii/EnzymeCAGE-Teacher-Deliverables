# HPC executor-only prompt: M4 Phase 1 acceptance CIF parser fix and clean 100-UID rerun

You are running on Chenyu/HPC as an executor. Your job is to produce a corrected M4 Phase 1 acceptance package by fixing one audited script bug and rerunning the same frozen 100-UID acceptance set. Do not modify production EnzymeCAGE assets or pools.

## 0. Why this rerun is needed

The previous return package:

```text
enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_20260811.tar.gz
```

produced useful evidence, but local audit found 7 likely false blockers:

```text
C5B8H7,Q9BZG8,Q29451,A0A0U3S9Q3,P0DJN3,A6SUD8,Q8UFS9
```

They were reported as:

```text
BLOCKED_AFDB_STRUCTURE_PARSE_FAILED
ValueError("The input mmCIF file must begin with a 'data_' directive.")
```

Audit interpretation:

```text
The raw downloaded .cif files are valid and begin with data_AF-...
The script converted CIF to normalized PDB, then incorrectly reused MMCIFParser
to parse the newly written PDB verification file.
```

Fix only this parser verification bug. Do not change the approved route.

## 1. Task identity

```text
TASK_ID=enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811
RUN_TYPE=phase1_acceptance_frozen_100uid_afdb_only_p2rank_predicted_pocket_staged_cif_parser_fix_clean_rerun
PRIMARY_ROUTE=AlphaFoldDB structure -> P2Rank predicted pocket -> ESM-2 3B on-demand/cache -> same-pocket GVP -> isolated loader validation
EVIDENCE_TIER=P2Rank predicted pocket lower-evidence tier
```

Allowed successful final package status:

```text
M4_ONDEMAND_D4_PHASE1_ACCEPTANCE_CIF_PARSER_FIX_RERUN_COMPLETE_WITH_PASS_AND_BLOCKER_COUNTS
```

This is not a full 4,681-UID backfill and not a production merge.

## 2. Required payload

Use the same payload archive:

```text
payload_archive_name=enzymecage_m4_phase1_acceptance_payload_20260811.tar.gz
payload_archive_sha256=0c451d8babcce408ec6816d2f7284abaf3be7d061b95e46b5459b59427cd604a
payload_archive_bytes=80112134
```

Locate it at one of:

```text
/root/projects/EnzymeCAGE-master/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/07_HPC_Prompts/enzymecage_m4_phase1_acceptance_payload_20260811.tar.gz
/root/projects/EnzymeCAGE-master/07_HPC_Prompts/enzymecage_m4_phase1_acceptance_payload_20260811.tar.gz
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_phase1_acceptance_payload_20260811.tar.gz
/usrdata/EnzymeCAGE_data/EnzymeCAGE-master/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/07_HPC_Prompts/enzymecage_m4_phase1_acceptance_payload_20260811.tar.gz
```

Do not download this payload from the internet. Verify SHA256 before extraction.

Extract to:

```text
PAYLOAD_STAGE=/tmp/enzymecage_m4_phase1_acceptance_payload_stage_cif_fix_20260811
```

Then verify:

```text
cd ${PAYLOAD_STAGE}/enzymecage_m4_phase1_acceptance_payload_20260811
sha256sum -c MANIFEST.sha256
```

If payload or internal manifest verification fails, stop with:

```text
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_PAYLOAD_MISSING_OR_SHA256_FAIL
```

## 3. Fresh output locations

Use fresh paths only:

```text
PROJECT_REPO=/root/projects/EnzymeCAGE-master
RETURN_ROOT=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries
RETURN_DIR=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811
ARCHIVE=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811.tar.gz
IDENTITY=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811.tar.gz.identity.txt
WORK_ROOT=/tmp/enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811
```

If any of `RETURN_DIR`, `ARCHIVE`, `IDENTITY`, `WORK_ROOT`, or `PAYLOAD_STAGE` already exists, do not overwrite, delete, reuse, or repair it. Return a minimal uniquely suffixed fail-closed package with:

```text
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_OUTPUT_OR_PAYLOAD_STAGE_EXISTS
```

## 4. Hard safety boundaries

Read-only inspection is allowed. Do not write to or mutate:

```text
/usrdata/EnzymeCAGE_data/feature
/usrdata/EnzymeCAGE_data/formal_splits
/usrdata/EnzymeCAGE_data/models
/root/projects/EnzymeCAGE-master/data
/root/projects/EnzymeCAGE-master/dataset
```

All generated files must stay under:

```text
WORK_ROOT
RETURN_DIR
```

Do not run apt, conda install, pip install, or write to `/usr`, `/usr/local`, or `/opt`.

## 5. P2Rank identity and route

Use the already audited stable P2Rank directory:

```text
P2RANK_DIR=/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1
PRANK=/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1/prank
EXPECTED_P2RANK_ARCHIVE_SHA256=d243f2d9036ac053fefb9407b5fe1c85f4fe077c519fd975ac585e995feab274
EXPECTED_PRANK_VERSION=P2Rank 2.5.1
```

Required command contract:

```text
prank predict -threads 4 -c alphafold -visualizations 0 ...
```

Use per-UID `.ds` dataset files for P2Rank input.

Do not rescue any UID using AlphaFill, old-pool pocket assets, PDB-REDO, SMR, experimental PDB, or any non-AFDB structure source.

## 6. Required script fix

Create a new run script under:

```text
${RETURN_DIR}/scripts/run_m4_phase1_acceptance_cif_parser_fix.py
```

You may base it on the previous returned `scripts/run_m4_phase1_acceptance.py`, but the new script must include this normalization fix:

```python
def normalize_structure(src, out):
    from Bio.PDB import MMCIFParser, PDBParser, PDBIO
    source_parser = MMCIFParser(QUIET=True) if src.suffix.lower() in [".cif", ".mmcif"] else PDBParser(QUIET=True)
    st = source_parser.get_structure(src.stem, str(src))
    ...
    io = PDBIO()
    io.set_structure(st)
    io.save(str(out), ChainResidueSelect("A"))

    # The normalized output is PDB regardless of whether the source was CIF.
    check_parser = PDBParser(QUIET=True)
    st2 = check_parser.get_structure("chk", str(out))
    n = sum(1 for r in st2.get_residues() if r.id[0] == " " and r.resname in STD_AA and "CA" in r)
    return {"parse_ok": True, "selected_chain": "A", "residue_count": n}
```

Do not count a UID as `BLOCKED_AFDB_STRUCTURE_PARSE_FAILED` if the raw CIF parsed, the normalized PDB was written, and the normalized PDB has ATOM records.

Keep the PyTorch 2.7 ESM `torch.load(..., weights_only=False)` compatibility patch from the previous run.

## 7. Pre-rerun bugfix proof

Before processing all 100 UIDs, run a small normalization proof on at least one of the previously false-blocked CIF UIDs, preferably:

```text
C5B8H7
```

Required proof output:

```text
CIF_PARSER_FIX_PROOF.json
```

It must record:

```text
test_uid
raw_cif_url
raw_cif_sha256
raw_cif_first_line
normalized_pdb_exists
normalized_pdb_atom_line_count
normalize_structure_status
```

If the proof does not show a valid normalized PDB with ATOM records, stop with:

```text
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_BUGFIX_PROOF_FAILED
```

## 8. Required F3 rerun

Run F3 reproduction from the payload source snapshot before UID processing:

```text
F3_SOURCE_ROOT=${PAYLOAD_STAGE}/enzymecage_m4_phase1_acceptance_payload_20260811/f3_source_snapshot
F3_REPRO_DIR=${PAYLOAD_STAGE}/enzymecage_m4_phase1_acceptance_payload_20260811/f3_numeric_reproduction
```

Copy `F3_REPRO_DIR` into:

```text
${RETURN_DIR}/F3_Numeric_Reproduction_Path_2026-08-11/
```

Then run:

```text
python3 ${RETURN_DIR}/F3_Numeric_Reproduction_Path_2026-08-11/F3_REPRODUCE_COUNTS.py --project-root ${F3_SOURCE_ROOT} --output-dir ${RETURN_DIR}/F3_Numeric_Reproduction_Path_2026-08-11/rerun_on_chenyu
```

Require:

```text
F3_REPRODUCTION_PASS
expected_count_mismatches={}
strict_uid_missing_valid_pocket=4681
strict_cleaned_2026_main_table_uid=195743
```

If this fails, stop before UID processing with:

```text
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_F3_PAYLOAD_REPRODUCTION_FAILED
```

## 9. Frozen UID checks

Use only:

```text
SAMPLED_UIDS=${PAYLOAD_STAGE}/enzymecage_m4_phase1_acceptance_payload_20260811/uid_freeze/SAMPLED_UIDS.csv
```

Verify before UID processing:

```text
100 rows;
100 unique UniprotID values;
35 ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING;
25 OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING;
40 OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING;
strict_2026_uid=true for all rows;
local_sequence_present=true for all rows;
f3_missing_valid_pocket_member=true for all rows;
final_missing_pocket_uid_member=true for all rows;
appeared_in_previous_2026_08_03_pilots=false for all rows;
main_acceptance_denominator=true for all rows.
```

Do not resample, substitute strata, add UIDs, or remove UIDs.

## 10. Clean 100-UID rerun

Run all 100 frozen UIDs again with the same approved workflow:

```text
AlphaFoldDB structure only;
P2Rank top predicted pocket only;
ESM-2 3B model_name=esm2_t36_3B_UR50D, repr_layer=36, embedding_dim=2560;
same predicted-pocket PDB for GVP and ESM pocket-node features;
isolated load_geometric_dataset validation;
staged assets only.
```

Use PASS token:

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER
```

Do not use the strict AlphaFill full-loader PASS token.

The only allowed PASS token for this predicted-pocket route is the one listed above.

Every input UID must have exactly one final status.

For P2Rank no-pocket cases, the status means:

```text
AFDB structure was available and P2Rank ran, but no usable top predicted pocket
was produced under the approved command contract.
```

It does not mean the structure download failed.

## 11. Required output files

At minimum, `RETURN_DIR` must contain:

```text
CIF_PARSER_FIX_PROOF.json
ENVIRONMENT_REPORT.txt
F3_Numeric_Reproduction_Path_2026-08-11/
FINAL_STATUS.txt
FORMAL_ASSET_MUTATION_CHECK.json
MANIFEST.sha256
P2RANK_VERSION_AND_INSTALL_REPORT.txt
PER_UID_STATUS_TABLE.csv
PER_UID_TIMING_RESOURCE_TABLE.csv
PHASE1_ACCEPTANCE_REPORT.md
PHASE1_ACCEPTANCE_REPORT.json
SAMPLED_UIDS.csv
SAMPLE_DESIGN_REPORT.md
SAMPLE_DESIGN_REPORT.json
STAGED_ASSET_MANIFEST.csv
STRUCTURE_SOURCE_TABLE.csv
scripts/run_m4_phase1_acceptance_cif_parser_fix.py
per_uid/<UID>/REPORT.md
per_uid/<UID>/REPORT.json
```

For each PASS UID, `STAGED_ASSET_MANIFEST.csv` must include:

```text
staged_assets/<UID>/pockets/pocket/<UID>.pdb
staged_assets/<UID>/pockets/pocket_info.csv
staged_assets/<UID>/esm3b/protein_level/seq2feature.pkl
staged_assets/<UID>/esm3b/pocket_node_feature/esm_node_feature.torch.pt
staged_assets/<UID>/gvp/gvp_protein_feature_flat.pt
staged_assets/<UID>/validation_input.csv
```

## 12. Required summary fields

`PHASE1_ACCEPTANCE_REPORT.md/json` must report:

```text
n_input_uids
n_unique_input_uids
n_main_acceptance_denominator
stratum_counts
n_afdb_structure_pass
n_afdb_structure_blocked
n_afdb_structure_parse_failed
n_p2rank_no_pocket
n_pass_afdb_p2rank_predicted_pocket_d4_loader
n_blocked_by_final_status
n_esm2_3b_cache_hit
n_esm2_3b_cache_miss
n_loader_validation_called
n_loader_validation_pass
status_counts
status_counts_by_stratum
list_of_afdb_404_uids
list_of_p2rank_no_pocket_uids
list_of_parse_failed_uids
cif_parser_fix_proof_status
F3 rerun status
formal asset mutation booleans
```

If any `BLOCKED_AFDB_STRUCTURE_PARSE_FAILED` remains, include the raw file first line, file type, parser error, and whether normalized PDB/ATOM lines exist.

## 13. Manifest, archive, and identity

Before archiving:

```text
cd ${RETURN_DIR}
find . -type f -print0 | sort -z | xargs -0 sha256sum > MANIFEST.sha256
```

Create both:

```text
${ARCHIVE}
${IDENTITY}
```

The identity file must be present beside the archive and include:

```text
task_id
final_status
n_input_uids
n_unique_input_uids
n_pass_afdb_p2rank_predicted_pocket_d4_loader
n_blocked_total
n_afdb_structure_parse_failed
n_p2rank_no_pocket
n_esm2_3b_cache_hit
n_esm2_3b_cache_miss
payload_archive_sha256
p2rank_archive_sha256
p2rank_version
archive_sha256
archive_bytes
created_utc
formal_assets_mutated=false
production_pool_mutated=false
```

Do not report success without both archive and identity file.

## 14. Final status tokens

If completed:

```text
M4_ONDEMAND_D4_PHASE1_ACCEPTANCE_CIF_PARSER_FIX_RERUN_COMPLETE_WITH_PASS_AND_BLOCKER_COUNTS
```

If blocked before UID processing:

```text
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_PAYLOAD_MISSING_OR_SHA256_FAIL
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_OUTPUT_OR_PAYLOAD_STAGE_EXISTS
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_BUGFIX_PROOF_FAILED
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_F3_PAYLOAD_REPRODUCTION_FAILED
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_FROZEN_UID_MANIFEST_INVALID
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_JAVA_OR_P2RANK_MISSING
M4_PHASE1_ACCEPTANCE_CIF_FIX_BLOCKED_ENVIRONMENT_MISSING
```

If blocked after some UID attempts, still write all required status/timing tables for all 100 UIDs and create the archive plus identity file.
