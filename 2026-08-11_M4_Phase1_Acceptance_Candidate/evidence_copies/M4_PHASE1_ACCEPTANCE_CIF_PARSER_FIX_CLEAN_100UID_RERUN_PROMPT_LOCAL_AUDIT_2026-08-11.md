# Local audit: M4 Phase 1 CIF parser fix clean 100-UID rerun prompt

Date: 2026-08-11

Audited prompt:

```text
07_HPC_Prompts/
HPC_ENZYMECAGE_M4_PHASE1_ACCEPTANCE_CIF_PARSER_FIX_CLEAN_100UID_RERUN_EXECUTOR_ONLY_PROMPT_2026-08-11.md
```

Preceding return audit:

```text
04_Local_Review_Audits/
M4_PHASE1_ACCEPTANCE_100UID_AFDB_P2RANK_RETURN_LOCAL_AUDIT_2026-08-11.md
```

## 1. Verdict

Verdict:

```text
ACCEPT_CIF_PARSER_FIX_CLEAN_100UID_RERUN_PROMPT_FOR_USER_REVIEW
```

The prompt is scoped to one corrective rerun:

```text
fix the CIF-to-PDB normalization verification bug;
rerun the same frozen 100 UIDs;
preserve AFDB-only + P2Rank predicted-pocket route;
preserve ESM-2 3B/GVP/loader staged-only validation;
require a new archive plus external identity file.
```

It does not authorize full 4,681 UID backfill or production merge.

## 2. Identity

Prompt SHA256:

```text
17c0953e9c7f28af7112a684d742df9e128b9b781966b55d2f7863a3d681f5ff
```

Payload required by prompt:

```text
enzymecage_m4_phase1_acceptance_payload_20260811.tar.gz
sha256=0c451d8babcce408ec6816d2f7284abaf3be7d061b95e46b5459b59427cd604a
bytes=80112134
```

New task id:

```text
enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811
```

## 3. Bugfix scope audit

The prompt requires the exact audited fix:

```text
Source CIF is parsed with MMCIFParser.
Normalized output is written as PDB.
The normalized PDB verification pass must use PDBParser.
```

The prompt requires `CIF_PARSER_FIX_PROOF.json` before processing all 100 UIDs.
This proof must show a previously false-blocked CIF UID normalizes into a PDB
with ATOM records.

Affected UIDs from the prior audit:

```text
C5B8H7,Q9BZG8,Q29451,A0A0U3S9Q3,P0DJN3,A6SUD8,Q8UFS9
```

## 4. Route boundary audit

The prompt preserves:

```text
AlphaFoldDB structure only;
P2Rank 2.5.1;
prank predict -threads 4 -c alphafold -visualizations 0 ...;
per-UID .ds files;
top predicted pocket only;
ESM-2 3B, not ESM-C/600M;
same predicted-pocket PDB for GVP and ESM pocket-node features;
staged outputs only.
```

It explicitly forbids rescue via:

```text
AlphaFill;
old-pool pocket assets;
PDB-REDO;
SMR;
experimental PDB;
other non-AFDB structure sources.
```

## 5. P2Rank no-pocket wording audit

The prompt includes the important interpretation:

```text
P2Rank no-pocket means AFDB structure was available and P2Rank ran, but no
usable top predicted pocket was produced under the approved command contract.
It does not mean the structure download failed.
```

This should prevent confusing `BLOCKED_AFDB_P2RANK_NO_POCKET` with AFDB 404 or
network failure.

## 6. Required output discipline

The prompt requires:

```text
F3 rerun from payload source snapshot before UID processing;
same frozen 100 UID checks;
PER_UID_STATUS_TABLE.csv;
PER_UID_TIMING_RESOURCE_TABLE.csv;
STRUCTURE_SOURCE_TABLE.csv;
STAGED_ASSET_MANIFEST.csv;
FORMAL_ASSET_MUTATION_CHECK.json;
PHASE1_ACCEPTANCE_REPORT.md/json;
MANIFEST.sha256;
archive;
external .tar.gz.identity.txt.
```

The identity file must include pass/blocker counts, parse-failed count,
P2Rank no-pocket count, payload SHA, P2Rank SHA, archive SHA and mutation flags.

## 7. Red-line audit

Local literal search found no teacher-forbidden success labels in the prompt.

The prompt does not support claiming:

```text
full missing-UID backfill has been authorized or completed;
production D4 assets were merged;
P2Rank predicted pockets are strict AlphaFill pockets;
the prior 7 CIF parse-failed UIDs were real blockers.
```

## 8. Next action

Next action:

```text
User can run the audited executor-only prompt on Chenyu/HPC.
After the corrected archive and identity file return, perform local return
audit before any teacher-facing upload.
```
