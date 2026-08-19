# EnzymeCAGE Teacher Deliverables

## 老师当前优先审阅入口 — 2026-08-18

请优先打开：

- [`00_CURRENT_TEACHER_REVIEW_ENTRYPOINT/`](00_CURRENT_TEACHER_REVIEW_ENTRYPOINT/)

该文件夹汇总了当前最新 M4 E2 第二里程碑、1,650 fetch-failed accession
二次复核、P18173/P80550 accession 存疑项补充澄清、BBD83 209a4b4
status-clean 审计状态、已完成证据路径，以及仍需老师后续裁定的问题。
根目录中保留历史文件是为了
不破坏此前已经发给老师的旧 GitHub 链接；当前审阅请以本入口和下方
最新回应为准。

## Supplementary 2026-08-19 pollutant transformation-product route evaluation

- [`2026-08-19_Pollutant_TP_Prediction_Route_Evaluation/`](2026-08-19_Pollutant_TP_Prediction_Route_Evaluation/)

This supplementary package summarizes the current pollutant transformation
product prediction / known-pathway lookup route evaluation. It includes BBD83
results, Soil/Sludge transfer results, enviPath known-pathway lookup checks,
tool comparison tables, local audits, returned archives and directly browsable
detail tables.

Core conclusion:

```text
known parent/pathway records → use enviPath local snapshot lookup first
unknown-parent blind prediction → BioTransformer ENVMICRO remains current baseline
BBD-finetuned ECLIPSE PREDEC → useful complementary candidate generator
current available enviFormer checkpoint → not a main route
```

Boundary: this is an exploratory reaction/product-prediction route evidence
package. It does not replace the current M4 E2 / accession-ambiguity review
items above, does not claim production D4/pool mutation, and does not claim
that enviPath Soil/Sludge lookup is 100% blind prediction accuracy.

## Current 2026-08-18 M4 E2 accession ambiguity clarification

- [`2026-08-18_M4_E2_Accession_Ambiguity_Clarification_P18173_P80550/`](2026-08-18_M4_E2_Accession_Ambiguity_Clarification_P18173_P80550/)

This package answers the two teacher-requested unresolved accession questions
from the accepted 1,650 table-only review:

```text
P18173: Q8SXV0 was selected by deterministic accession probe order, not by
        biological preference; original 625aa is not sequence-identical to
        current canonical or either AFDB candidate structure.
P80550: original 38aa is traced to the frozen 2026-01-21 processed enzyme
        snapshot; it is not sequence-identical to current canonical or AFDB
        F1RSB4.
```

Boundary: both cases remain record-only and unresolved; no UID replacement, no
asset generation, no formal/production mutation and no candidate closure are
claimed.

## Current 2026-08-16 M4 E2 1,650 fetch-failed accession secondary review

- [`2026-08-16_M4_E2_Fetch_Failed_1650_Accession_Secondary_Review/`](2026-08-16_M4_E2_Fetch_Failed_1650_Accession_Secondary_Review/)

This package contains the table-only secondary accession review for the 1,650
`BLOCKED_AFDB_STRUCTURE_FETCH_FAILED` rows from the accepted M4 E2 full 4,681
package.

Core result:

```text
1650 reviewed
5 accession candidates recorded for teacher review only
1645 no available AFDB v6 accession candidate
0 API retry exhausted
no UID replacement
no asset generation
no formal / production mutation
```

Boundary: this is an accession review table only. It is not rescued assets,
production backfill, UID replacement, D4/pool merge, or full asset completion.

## Current 2026-08-14 M4 E2 full 4,681 staged status table

- [`2026-08-14_M4_E2_Full_4681_Staged_Status_Table/`](2026-08-14_M4_E2_Full_4681_Staged_Status_Table/)

This package contains the reviewable GitHub-side tables, reports, identity
sidecar copy and local audit for the completed Chenyu full 4,681 staged status
table return.

The original 658M Chenyu archive is not committed to GitHub. It is available on
Chenyu at:

```text
/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/enzymecage_m4_e2_full_4681_4gpu_sharded_continuation_final_20260814.tar.gz
```

Core result:

```text
1704 staged PASS
1324 P2Rank no-pocket blockers
1650 AFDB structure fetch blockers
3 ESM-2 3B extraction blockers
```

Boundary: this is a staged-only lower-evidence AFDB + P2Rank predicted-pocket
return. It is not a production D4 merge, production pool mutation, or claim that
all 4,681 UIDs were backfilled.

## Current 2026-08-13 M4 E2 and BBD83 status package with 2026-08-14 transport supplement

- [`2026-08-13_M4_E2_Second_Milestone_and_BBD83_Status/`](2026-08-13_M4_E2_Second_Milestone_and_BBD83_Status/)

This package contains the Chen Haoran-side response to the 2026-08-13 guidance:
the M4 second-milestone E2 authorization request, A3CST9 cache-miss smoke
evidence, the BBD83 209a4b4 2026-08-13 P1 re-check audit, and the 2026-08-14
recovered `.tar.gz` + identity transport sidecar audit.

Boundary: production D4/pool was not modified, and BBD83 is status-clean but
still low-coverage rather than final scientific closure. The BBD83 formal
transport sidecar is now present and locally audited, with the known
MANIFEST.sha256 self-hash caveat retained. The full 4,681 final return is not
part of this BBD83 transport supplement.

## Current M4 Phase 1 acceptance candidate — 2026-08-11

The corrected Phase 1 100-UID frozen acceptance candidate package is placed in
a dedicated folder:

- [`2026-08-11_M4_Phase1_Acceptance_Candidate/`](2026-08-11_M4_Phase1_Acceptance_Candidate/)

Main teacher-facing summary:

- [`2026-08-11_M4_Phase1_Acceptance_Candidate/M4_PHASE1_ACCEPTANCE_RESULT_SUMMARY_TO_HUANG_2026-08-11.md`](2026-08-11_M4_Phase1_Acceptance_Candidate/M4_PHASE1_ACCEPTANCE_RESULT_SUMMARY_TO_HUANG_2026-08-11.md)

Current local-audit result: 41/100 staged AFDB-only P2Rank predicted-pocket D4
assets passed ESM-2 3B, same-pocket GVP and isolated loader validation;
44/100 are P2Rank no-pocket blockers; 15/100 are AFDB structure fetch blockers;
the previous CIF parser false-blocker class is cleared; F3 numeric
reproduction passed on Chenyu with `strict_uid_missing_valid_pocket=4681`.

Boundary: this package is not a full 4,681 UID backfill, not a production
D4/pool merge, and not teacher adjudication of Phase 1 acceptance.

## Current M4 OnDemand D4 direction response — 2026-08-09

The 2026-08-07 teacher feedback requested an M4 direction response before
formal M4 authorization. The response is placed in a dedicated package:

- [`2026-08-09_M4_OnDemand_D4_Backfill_Direction_Response/`](2026-08-09_M4_OnDemand_D4_Backfill_Direction_Response/)

Current status: toolization design, workload/timeline estimate, and Phase 1
acceptance UID subset policy have been written for teacher adjudication. This
does not claim M4 implementation authorization, generated staged assets,
production D4 merge, full 4,681 UID processing, or 340-host GVP recovery.

## Current M3-EXT Paraoxon S1/S2 package — 2026-08-06

The 2026-08-04 teacher-authorized Paraoxon follow-up now has a dedicated
teacher-facing package:

- [`2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/`](2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/)

Current status: S1 Stage A technical D4 constructability passed for the two
authorized UIDs `P0A434` and `Q97VT7`; S2 Paraoxon formal case draft has been
written. This package explicitly states that no model scoring, no production
D4 merge, no pool mutation and no Paraoxon validation claim have been made.

## Current final response to 2026-08-03 / 2026-08-04 teacher requirements — 2026-08-04

The latest teacher-facing response and evidence packages have been pushed and
are placed at repository root so the current status is visible from the GitHub
homepage:

- [`M3_2026_08_03_TEACHER_REQUIREMENTS_FINAL_RESPONSE_2026-08-04.md`](M3_2026_08_03_TEACHER_REQUIREMENTS_FINAL_RESPONSE_2026-08-04.md)
- [`M3_THREE_TECHNICAL_QUESTIONS_CORRECTION_AND_EVIDENCE_INDEX_2026-08-04.md`](M3_THREE_TECHNICAL_QUESTIONS_CORRECTION_AND_EVIDENCE_INDEX_2026-08-04.md)
- [`2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/`](2026-08-04_M3_Three_Technical_Questions_Corrections_and_Evidence/)

Status: F1--F5 and the associated evidence-index corrections are complete and
pushed. F6 remains pending only because Gong's model output has not returned.
The 2026-08-04 M3-EXT Paraoxon/Carbaryl follow-up requirements are newer
teacher instructions and are not claimed as completed in this 2026-08-04
response.

## Final 07-23/07-24 response and biological decision — 2026-07-27

The complete item-by-item response is placed directly at repository root so
earlier completed work is not missed:

- [`M3_2026_07_23_24_TEACHER_TASK_LIST_FINAL_RESPONSE_2026-07-27.md`](M3_2026_07_23_24_TEACHER_TASK_LIST_FINAL_RESPONSE_2026-07-27.md)
- [`M3_NEXT_ROUND_HUANG_TEACHER_ADJUDICATION_REQUEST_AFTER_BIOLOGICAL_DECISIONS_2026-07-27.md`](M3_NEXT_ROUND_HUANG_TEACHER_ADJUDICATION_REQUEST_AFTER_BIOLOGICAL_DECISIONS_2026-07-27.md)

The biological meeting selected an A-first comparison of the internal model,
BioTransformer 3.0–ENVMICRO and enviFormer. No tool has been declared the
winner. enviFormer validation is still in progress, the internal model awaits
handoff, and the existing BioTransformer result remains product-only. C becomes
a research fallback only if all three tools fail the minimum contract.

- decision record, audit and hashes:
  [`2026-07-27_M3_P1_2_1_Reaction_Predictor_A_First_Three_Tool_Benchmark_Decision/`](2026-07-27_M3_P1_2_1_Reaction_Predictor_A_First_Three_Tool_Benchmark_Decision/)

The cross-side response is duplicated byte-for-byte in the MetaTraits
teacher-deliverables repository. Enzyme and microbe evidence assets remain
separated by repository.

## Historical pre-decision biological route material — 2026-07-27

The detailed A/B/C biological selection card, visual meeting version and
independent audits are retained as the evidence reviewed before the
2026-07-27 meeting:

- [`2026-07-27_M3_P1_2_1_Reaction_Predictor_Biological_Route_Selection_Pending/`](2026-07-27_M3_P1_2_1_Reaction_Predictor_Biological_Route_Selection_Pending/)

Status at the time of that package: unified pilot and scoring complete; route
selection was pending. The current decision is recorded in the newer package
above. Production `reaction_prediction_node` remains unchanged, and a formal
new benchmark still requires Huang-laoshi scope confirmation.

## Current route adjudication request — 2026-07-26

The three-route reaction-predictor pilot has passed answer-key unlock,
deterministic scoring and independent recomputation. No final route or live
implementation is claimed.

- teacher-facing decision request:
  [`M3_P1_2_1_REACTION_PREDICTOR_ROUTE_ADJUDICATION_REQUEST_2026-07-26.md`](M3_P1_2_1_REACTION_PREDICTOR_ROUTE_ADJUDICATION_REQUEST_2026-07-26.md)
- self-contained evidence package, route audits, machine reports and hashes:
  [`2026-07-26_M3_P1_2_1_Reaction_Predictor_Route_Adjudication/`](2026-07-26_M3_P1_2_1_Reaction_Predictor_Route_Adjudication/)

Current boundary: Route A is contract-incompatible, Route B is product-only,
Route C-exact is a known-Rhea lookup baseline and C-generic is not ready.
`reaction_prediction_node` remains unchanged pending biological/teacher
adjudication.

## Current hard prerequisite return — 2026-07-24

The original 2026-07-22 RHEA:11880 fairness clarification requested for
teacher-side byte alignment is placed directly in the repository root:

- [`TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md`](TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md)
- required SHA256:
  `80a3be0c8507a6cbf4f318de0c4735aa04d7c5106c2cc759fb5af7ee9ea356c0`
- path index, independent audit and delivery hashes:
  [`2026-07-24_M3_RHEA11880_Clarification_Original_Byte_Resubmission/`](2026-07-24_M3_RHEA11880_Clarification_Original_Byte_Resubmission/)

The returned authority file is byte-identical to the original referenced by
`case_1_rhea_46976.json`. It was not reconstructed, edited or reformatted.

## Current submission — 2026-07-23

Teacher-requested files are placed directly in the repository root:

- P0 Task 1: [`case_1_rhea_46976.json`](case_1_rhea_46976.json)
- P1 Task 2: [`THREE_CASE_HOMEPAGE.md`](THREE_CASE_HOMEPAGE.md)
- P2 Task 3: [`M3_CASE_REGISTRY.json`](M3_CASE_REGISTRY.json)
- Retained deprecated evidence: [`case_1_rhea_40543.json`](case_1_rhea_40543.json)
- Active companion cases: [`case_2_rhea_11532.json`](case_2_rhea_11532.json) and [`case_3_rhea_24292.json`](case_3_rhea_24292.json)
- P2 Task 5: [`M3_EXT_CANDIDATE_SHORTLIST_v0.md`](M3_EXT_CANDIDATE_SHORTLIST_v0.md)
- Delivery status and teacher decisions requested:
  [`ENZYME_TASKS_1_2_3_5_FINAL_TEACHER_DELIVERY_2026-07-23.md`](ENZYME_TASKS_1_2_3_5_FINAL_TEACHER_DELIVERY_2026-07-23.md)

Individual task audits and the final pre-submission audit are under
[`2026-07-23_Enzyme_Tasks_1_2_3_5_Submission/audits/`](2026-07-23_Enzyme_Tasks_1_2_3_5_Submission/audits/).
The submission hash manifest is
[`2026-07-23_Enzyme_Tasks_1_2_3_5_Submission/DELIVERABLE_SHA256SUMS.txt`](2026-07-23_Enzyme_Tasks_1_2_3_5_Submission/DELIVERABLE_SHA256SUMS.txt).

Tasks 1–6 were subsequently accepted by the teacher on 2026-07-23. Task 5
remains within candidate-screening scope and still needs separate promotion
and asset adjudication. This repository does not claim official challenge-case
promotion, D4 completion, Route-B/Route-C mutation or a student-side model run.

Earlier dated folders and commits are retained unchanged as historical
submissions.
