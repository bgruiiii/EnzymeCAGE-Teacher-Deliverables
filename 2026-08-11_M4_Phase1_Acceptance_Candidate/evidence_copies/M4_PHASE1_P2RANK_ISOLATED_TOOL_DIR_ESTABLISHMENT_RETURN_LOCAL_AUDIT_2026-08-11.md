# Local audit: M4 Phase 1 P2Rank isolated tool-directory establishment return

Date: 2026-08-11

Audited archive:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_phase1_p2rank_isolated_tool_dir_establishment_20260811.tar.gz
```

Identity file:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m4_phase1_p2rank_isolated_tool_dir_establishment_20260811.tar.gz.identity.txt
```

Executor prompt:

```text
07_HPC_Prompts/
HPC_ENZYMECAGE_M4_PHASE1_P2RANK_ISOLATED_TOOL_DIR_ESTABLISHMENT_EXECUTOR_ONLY_PROMPT_2026-08-11.md
```

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M4_PHASE1_CONDITIONAL_APPROVAL_2026-08-11.md
```

## 1. Verdict

Verdict:

```text
ACCEPT_ISOLATED_TOOL_DIR_ESTABLISHMENT_RETURN
```

The return package supports this narrow conclusion:

```text
The previously audited P2Rank 2.5.1 release has been copied from the verified
2026-08-03 runtime archive and established under a stable isolated Chenyu/HPC
tool directory:

/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1
```

This return does not start or authorize the Phase 1 >=100 UID acceptance run.
The next step remains F3 reproduction-path packaging.

## 2. Archive and manifest integrity

Archive identity:

| Item | Value |
|---|---|
| local archive SHA256 | `a78f4cb963b639861c2eb05a40a2b26646c8de9b94fed81f4cdd8c189e17a87d` |
| identity SHA256 | `a78f4cb963b639861c2eb05a40a2b26646c8de9b94fed81f4cdd8c189e17a87d` |
| archive bytes | `34983` |
| created UTC | `2026-08-11T02:47:27Z` |

Package files present:

```text
COMMAND_TRANSCRIPT.txt
ENVIRONMENT_REPORT.txt
FINAL_STATUS.txt
FORMAL_ASSET_READONLY_SNAPSHOT.json
JAVA_RUNTIME_REPORT.txt
MANIFEST.sha256
P2RANK_ISOLATED_TOOL_DIR_REPORT.json
P2RANK_ISOLATED_TOOL_DIR_REPORT.md
P2RANK_TOOL_DIR_MANIFEST.tsv
P2RANK_TOOL_DIR_SHA256SUMS.txt
```

Local manifest check:

```text
COMMAND_TRANSCRIPT.txt: OK
ENVIRONMENT_REPORT.txt: OK
FINAL_STATUS.txt: OK
FORMAL_ASSET_READONLY_SNAPSHOT.json: OK
JAVA_RUNTIME_REPORT.txt: OK
P2RANK_ISOLATED_TOOL_DIR_REPORT.json: OK
P2RANK_ISOLATED_TOOL_DIR_REPORT.md: OK
P2RANK_TOOL_DIR_MANIFEST.tsv: OK
P2RANK_TOOL_DIR_SHA256SUMS.txt: OK
```

No internal transcript manifest inconsistency was observed in this package.

## 3. Required-file audit

| Required by prompt | Present | Result |
|---|---|---|
| `P2RANK_ISOLATED_TOOL_DIR_REPORT.md` | yes | PASS |
| `P2RANK_ISOLATED_TOOL_DIR_REPORT.json` | yes | PASS |
| `P2RANK_TOOL_DIR_MANIFEST.tsv` | yes | PASS |
| `P2RANK_TOOL_DIR_SHA256SUMS.txt` | yes; 599 files listed | PASS |
| `JAVA_RUNTIME_REPORT.txt` | yes | PASS |
| `ENVIRONMENT_REPORT.txt` | yes | PASS |
| `FORMAL_ASSET_READONLY_SNAPSHOT.json` | yes | PASS |
| `COMMAND_TRANSCRIPT.txt` | yes | PASS |
| `FINAL_STATUS.txt` | yes | PASS |
| `MANIFEST.sha256` | yes | PASS |

## 4. Main result

Final status:

```text
M4_PHASE1_P2RANK_ISOLATED_TOOL_DIR_READY
```

Structured report fields:

| Field | Value |
|---|---|
| `method_changed` | `false` |
| `readonly_except_tool_dir` | `true` |
| `production_assets_mutated` | `false` |
| `uid_backfill_run` | `false` |
| `forbidden_actions_performed` | `none` |
| `tool_dir_status` | `PASS_ISOLATED_P2RANK_TOOL_DIR_READY` |
| `next_action_recommendation` | `PROCEED_TO_LOCAL_AUDIT_THEN_F3_REPRODUCTION_STEP` |

Stable tool directory:

```text
stable_p2rank_dir=/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1
stable_prank_path=/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1/prank
stable_archive_path=/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1.tar.gz
```

Tool identity:

| Check | Result |
|---|---|
| stable archive SHA256 | `d243f2d9036ac053fefb9407b5fe1c85f4fe077c519fd975ac585e995feab274` |
| expected archive SHA256 | same |
| stable `prank --version` | `P2Rank 2.5.1` |
| `prank` launcher SHA256 | `ad7bedfcb833b639aebe171c005920017e68acb071cb5508e8147726ad5d115c` |
| `bin/p2rank.jar` SHA256 | `4d73a85b796bd5ec5563d840abb5b1005f37b4651fd7f8aaad4b01a936ea1ece` |
| `config/alphafold.groovy` SHA256 | `bc3be625000100ccf3d57907b67c726159c797b9bb421d07fc4a7b6fca0aaa9f` |

## 5. Prior-method preservation audit

The return correctly preserves the previously audited method:

| Required method element | Evidence in return | Result |
|---|---|---|
| P2Rank version `2.5.1` | `stable_prank_version=P2Rank 2.5.1` | PASS |
| prior archive SHA256 | exact match to `d243f2d9...b274` | PASS |
| prior release archive reused | source archive verified and copied; no replacement download | PASS |
| `-c alphafold` config exists | `config/alphafold.groovy` present and hashed | PASS |
| command contract preserved | expected command recorded | PASS |
| per-UID `.ds` input contract preserved | expected input mode recorded | PASS |
| no new pocket route | `method_changed=false` | PASS |

Commit caveat:

```text
commit_255a05e_locally_evidenced=false
commit_255a05e_status=TEACHER_EXPECTED_COMMIT_NOT_PRESENT_IN_RELEASE_TARBALL_GIT_METADATA
```

Audit interpretation:

```text
The teacher-required commit field is preserved as an expected identity field,
but the release tarball still does not contain `.git` metadata. Therefore we
can claim archive SHA256 identity and P2Rank 2.5.1 version, but we cannot claim
commit 255a05e was locally proven from git metadata.
```

## 6. Boundary / no-mutation audit

The prompt allowed writes only to:

```text
/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1
/usrdata/EnzymeCAGE_data/tools/p2rank_2.5.1.tar.gz
WORK_ROOT
RETURN_DIR / ARCHIVE / IDENTITY
```

The return reports and transcript support:

| Forbidden action | Evidence | Result |
|---|---|---|
| apt install | no install command evidenced | PASS |
| conda/pip install | no install command evidenced | PASS |
| download | no `curl`/`wget` download evidenced; copied old verified archive | PASS |
| system install under `/usr`, `/usr/local`, `/opt` | no such write evidenced | PASS |
| PATH modification | not evidenced | PASS |
| UID sampling/backfill | report says false | PASS |
| AlphaFoldDB fetch | not evidenced | PASS |
| `prank predict` | not evidenced; only `--version`, `--help`, `-h` probes | PASS |
| ESM-2 3B extraction | not evidenced | PASS |
| GVP generation | not evidenced | PASS |
| loader validation | not evidenced | PASS |
| production D4/pool mutation | report says false; protected roots only snapshotted read-only | PASS |

Formal protected root snapshot was limited to one-level stat summaries for:

```text
/usrdata/EnzymeCAGE_data/feature
/usrdata/EnzymeCAGE_data/formal_splits
/usrdata/EnzymeCAGE_data/models
/root/projects/EnzymeCAGE-master/data
/root/projects/EnzymeCAGE-master/dataset
```

This supports boundary discipline for the prompt, but it is not a full
before/after mutation proof of every file under those roots.

## 7. Environment observations

Current Chenyu/HPC environment from return:

| Item | Value |
|---|---|
| host | `674db4f51184` |
| user | `root` |
| working dir | `/usrdata/EnzymeCAGE_data/EnzymeCAGE-master` |
| Python | `/usr/bin/python`, Python `3.12.3` |
| GPU | NVIDIA GeForce RTX 4090 D, driver `570.144` |
| Java | OpenJDK `17.0.19` |
| Java realpath | `/usr/lib/jvm/java-17-openjdk-amd64/bin/java` |

## 8. What this return does not support

This return does not support claiming:

```text
Phase 1 >=100 UID acceptance run has started;
any UID was sampled or processed;
any staged D4 asset was generated by this tool-directory step;
F3 reproduction path has been completed;
full 4,681 UID status table is authorized or complete;
production D4 or production pool was modified;
P2Rank predicted pockets are strict AlphaFill pockets;
commit 255a05e was locally evidenced from git metadata.
```

## 9. Next action

The next action is not a UID run. It is:

```text
F3 reproduction path packaging
```

This is required by Huang-laoshi's 2026-08-11 condition:

```text
F3 verification path = reproduction script + Rhea/UniProt snapshot versions,
to be delivered with the Phase 1 acceptance package.
```

After F3 reproduction is written and locally audited, the project can proceed to
sample-freeze planning for the >=100 UID acceptance subset.

Final local audit status:

```text
ARCHIVE_IDENTITY_PASS
MANIFEST_PASS
REQUIRED_FILES_PASS
ISOLATED_P2RANK_TOOL_DIR_READY_PASS
PRIOR_P2RANK_METHOD_PRESERVED_PASS
NO_NEW_POCKET_ROUTE_PASS
NO_INSTALL_OR_DOWNLOAD_PASS
NO_UID_RUN_PASS
NO_PRODUCTION_MUTATION_EVIDENCED_PASS
COMMIT_255A05E_NOT_LOCALLY_EVIDENCED_CAVEAT
NEXT_STEP_F3_REPRODUCTION_PATH
```

