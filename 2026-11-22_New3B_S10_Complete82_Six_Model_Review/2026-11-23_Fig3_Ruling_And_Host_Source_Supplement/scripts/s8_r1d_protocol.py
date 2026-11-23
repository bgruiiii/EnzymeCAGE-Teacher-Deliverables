#!/usr/bin/env python3
"""R1-D: three evidence axes separated + honest availability mapping.
No new case runs, no schema invention; all paths cross-checked against
R3/R4 tool source (read-only) and the two approved RAW receipts."""
import csv, json, os, sys
from pathlib import Path

OUT = Path(os.environ["FIG3_OUT"])
R = Path("/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01")
TASK = R / "FIG3_HUANG_RULING_CPU_SUPPLEMENT_20261123"
R3TOOL = R / "ENZYME_HOST_STANDALONE_TOOL_HANDOFF_20261119/revision3_native_cpu_verified_20261121/tool"
RAW = [str(p) for p in (R / "ENZYME_HOST_STANDALONE_TOOL_HANDOFF_20261119/revision4_existing_assets_handoff_20261122/native_results_20261122/attempt_6_20261122T051601Z").glob("RAW_*.json")]

P = "PERSISTED_IN_R4_RAW"          # verifiably in attempt6 RAW files
S = "AVAILABLE_IN_TOOL_ON_RUN"    # real nested fields in tool schemas; appear when a run exports them
N = "REQUIRES_C_WIRING"           # not produced by current tool; contract defined here
axes = [
 # axis A: how candidate was recalled
 ("A_recall_basis", "StepResult.retrieval_status/retrieval_mode/recall_repr_used", S, "schemas.py StepResult; predict.py fills from retrieval backend"),
 ("A_recall_basis", "StepResult.groups[]: rank, reaction_cd, similarity, exact_same_direction_retrieval_repr, undirected_key, group_cds, associated_pairs", S, "schemas.py RecallGroup; retrieval_backends FixedR3"),
 ("A_recall_basis", "PoolCandidate.provenance_records[]: source pair rows incl. source_datasets / accessions / evidence_tiers (R0 pair table columns)", S, "pool.py:36-49; retrieval_backends.py:125,176"),
 ("A_recall_basis", "PoolCandidate.sources[] / evidence_tiers[] tokens (e.g. 'replay_only' on cache-replay rows)", S, "pool.py:45-49; examples/pathway_example_output_cache_replay.json"),
 ("A_recall_basis", "recall family for R4 GPU verification calls", "NOT_AVAILABLE_IN_R4_VERIFICATION", "R4 calls took the FROZEN pool order from UNIFIED_STEP_TABLE (pool not re-recalled); provenance_records empty for those steps; families absent in a run are NOT_AVAILABLE, never backfilled from B1/T2 and no forced four-way choice"),
 # axis B: biological source binding
 ("B_source_binding", "HostSource.source_status/authoritative_source_signature/source_key_status/lookup_route/source_resolution/source_stage/source_binding_kind", S, "schemas.py HostSource; sources_backends from B1 row"),
 ("B_source_binding", "HostSource.cur_species_tax_id/cur_species_name/in_microbe_scope + R1 fields (species_identity_state, identified_microbe_source_for_followup)", S, "B1 columns + UID_SPECIES_TRACE_7468_R1.tsv join by scientific_uid/sequence_sha256"),
 ("B_source_binding", "HostSource.original_strains/proteome_linked_strains/representative_registration_coverage/reviewed", S, "schemas.py HostSource — strain/species/representative layers kept distinct"),
 ("B_source_binding", "HostSource.evidence_ids/evidence_source_file/evidence_row_key", S, "B1 evidence pointers preserved per row"),
 # axis C: was the candidate actually scored
 ("C_scoring_state", "execution mode: REAL_FORWARD (wrapper/native wrapper, scoring_status OK + forward_executed), CACHE_REPLAY (OK_CACHE_REPLAY), TEST_ONLY (backend_kinds TEST_DOUBLE / injected), BACKEND_NOT_CONFIGURED/EMPTY_POOL/blocked", S, "predict.py:48-53,68,93-118; scoring_backends outcome.status"),
 ("C_scoring_state", "StepResult.model_version/evidence_hash/batch_shape(forward_executed,batch_count)/replay_coverage", S, "schemas.py StepResult"),
 ("C_scoring_state", "all_candidate_scores[] full ScoredCandidate (rank in FULL ordering, ensemble_ci, display_rank) + ranked top-k slice kept SEPARATE", S, "schemas.py ScoredCandidate; predict.py"),
 ("C_scoring_state", "not_evaluated[] typed reasons + scores_not_disclosed[] per-UID", S, "schemas.py NotEvaluated; scoring_backends disclosure separation"),
 ("C_scoring_state", "GOLD handling: hit/miss when gold known; steps without any registered reference export GOLD_NOT_AVAILABLE (never 'all candidates proven wrong')", S, "C2 columns n_gold/best_gold_rank/gold_flag; contract for absent reference"),
 ("C_scoring_state", "R4 verification evidence present in RAW: query, model_key, pool order, 5 per-seed vectors, all scores, CI, typed ne", P, "attempt6 RAW_BIOPATH150_001__S02__BSY-r00595.json / RAW_...S03...json (different pathways; not one chain)"),
 # run identity & traits
 ("run_identity", "run_id, started_utc, five-seed identities, executed config SHA set", S, "tool StepResult has evidence_hash/model_version; run_id must be added by the export layer (contract below)"),
 ("run_identity", "pathway/step order + RT-{16hex} stable reaction-task id from bridge module", N, "depends on C wiring; bridge component exists in main snapshot, not driven step-by-step"),
 ("traits", "TraitEvidence per-slot OBSERVED/PREDICTED/MISSING/IDENTITY_ONLY + per-backend status (OK/OK_WITH_BACKEND_ERRORS/NO_RECORD_FOR_KEY/NOT_CONFIGURED/BACKEND_ERROR)", S, "schemas.py TraitEvidence; traits_backends.py status vocabulary"),
 ("traits", "observed and predicted may coexist; registry (BacDive) reported in its own column; predictions never relabeled measured", S, "traits_backends.py semantics"),
]
with open(OUT / "CASE_EXPORT_PROTOCOL_FIELDS_R1.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["axis", "field_path", "availability", "basis_or_note"])
    for a in axes: w.writerow(a)

# run-level export contract (what the C-wired run must additionally write)
contract = {"run_id": "<export-layer generated uuid>", "started_utc": "...", "ended_utc": "...",
 "mode_evidence": {"scoring_status": "OK -> REAL_FORWARD if backend_kinds.scoring in {enzyme_cage_wrapper, enzyme_cage_wrapper_native_c95}; OK_CACHE_REPLAY -> CACHE_REPLAY; TEST_DOUBLE -> TEST_ONLY",
   "forward_executed": "batch_shape.forward_executed true/false", "api_successful_requests": "runtime.forward_call_count", "model_evaluate_calls": "source-derived 5 per request (wrapper loops five seed models)"},
 "step_fields": ["step_order", "direction", "rt_id(REQUIRES_C_WIRING)", "reaction_smiles_original", "model_query_reaction", "query_representation_source", "model_key_sha256",
   "pool_status", "pool_candidates[]", "all_candidate_scores[]", "ranked_topk[] (separate slice)", "not_evaluated[]", "scores_not_disclosed[]",
   "gold_state: {PRESENT|ABSENT_GOLD_NOT_AVAILABLE}", "hosts[] (axis B)", "traits[] (backend statuses)", "provenance{source_member,sha256,run_utc}"],
 "honesty_notes": ["R4 RAW = fixed-pool scoring evidence of TWO steps from DIFFERENT pathways; not one pollutant chain",
   "cache example outputs keep synthetic labels; never relabeled as real",
   "unmatched/unscored steps preserved; no zero-fill; no candidate deletion/refill after Gold"]}
(OUT / "CASE_EXPORT_RUN_CONTRACT_R1.json").write_text(json.dumps(contract, indent=1, ensure_ascii=False))

# corrected SCHEMA_ONLY example
example = json.loads((TASK / "execution/CASE_EXPORT_EXAMPLE_SCHEMA_ONLY.json").read_text())
ex_step = example["case"]["steps"][0]
ex_step.update({
 "axis_A_recall_basis": {"retrieval_status": "OK", "retrieval_mode": "fixed_r3", "recall_repr_used": "<...>",
   "groups_top10": [{"rank": 1, "reaction_cd": "<>", "similarity": "<float>", "exact_same_direction_retrieval_repr": "<true|false>", "undirected_key": "<>", "group_cds": ["<>"], "associated_pairs": "<int>"}],
   "candidate_provenance": {"provenance_records": [{"source_datasets": "<pair-table column>", "accessions": "<...>", "evidence_tiers": "<pair-table column, e.g. replay_only>"}],
     "sources": ["<tokens>"], "evidence_tiers": ["<tokens>"]},
   "availability_note": "IN_TOOL_ON_RUN; for frozen-pool verification runs mark NOT_AVAILABLE_IN_R4_VERIFICATION"},
 "axis_B_source_binding": {"source_status": "<FOUND|FOUND_SOURCE_SET|NO_HIT|IDENTITY_CONFLICT>", "authoritative_source_signature": "<>", "source_resolution": "<>",
   "species_identity_state": "<IDENTIFIED_SPECIES|UNIDENTIFIED_PLACEHOLDER_LABEL|...>", "identified_microbe_source_for_followup": "<TRUE|FALSE>",
   "strain_layers": {"original_strains": "<as-is>", "proteome_linked_strains": "<as-is>", "representative_registration_coverage": "<separate>"},
   "evidence_ids": ["<>"], "evidence_source_file": "<B1 file identity>", "evidence_row_key": "<file+uid>"},
 "axis_C_scoring_state": {"execution_mode": "REAL_FORWARD|CACHE_REPLAY|TEST_ONLY", "scoring_status": "<outcome.status>", "forward_executed": "<bool>", "api_successful_requests": "<int>",
   "all_candidate_scores_full": ["<ScoredCandidate with FULL rank + ci>"], "ranked_topk_prefix": ["<display slice>"],
   "not_evaluated": ["<typed>"], "scores_not_disclosed": ["<typed>"],
   "gold_state": {"kind": "PRESENT|ABSENT", "n_gold": "<int>", "best_gold_rank": "<int, only when PRESENT>", "note_absent": "GOLD_NOT_AVAILABLE — no registered reference; NOT a claim that candidates are wrong"}},
})
example["export_mode_note"] = "run_id/RT-ID are export-layer contract fields; RT-ID requires C wiring"
example["R4_raw_coverage_note"] = "axis-C full scores/provenance exist in the two attempt6 RAW files; axes A/B come from tool runs with retrieval+sources+traits attached, NOT from those RAW files alone"
example["SCHEMA_ONLY"] = True
(OUT / "CASE_EXPORT_EXAMPLE_SCHEMA_ONLY_R1.json").write_text(json.dumps(example, indent=1, ensure_ascii=False))

# ---- E: real predicates (replace tautology) ----
rd = json.loads((R / "04_Local_Review_Audits/NEW3B_CURRENT95_RETURN_REVIEW_20261121/returned/NEW3B_S10_CURRENT95_SIX_MODEL_COMPARISON_20261120/release_inputs/NEW3B_CURRENT95_RELEASE_DECISION.json").read_text())
e = rd["scientific_identity_exception"]
es = {"Q66Q78_single_uid": e["uid"] == "Q66Q78", "acceptance": e["acceptance"] == "ACCEPT_FIXED_S10_REPLICATION_ONLY",
      "cause_unverified": e["cause"] == "UNVERIFIED", "rows": [e["train_rows"], e["valid_rows"], e["test_rows"]] == [22, 4, 3],
      "enzgfm_split_original_wording": "E0概率最大差0.011003837339090355、10步/140候选名次变化；新臂0.0657176754251293、19步/411候选名次变化，2步Top1改变、1步Hit@5改变（11/21复审原句；名次变化不都等于Top1变化）",
      "no_new_numeric_supplements": True}
(OUT / "LIMITATIONS_CONFIRMATION_Q66Q78_R1.json").write_text(json.dumps(es, indent=1, ensure_ascii=False))

checks = {"axes_count": len(axes), "three_axes": {"A_recall_basis", "B_source_binding", "C_scoring_state", "run_identity", "traits"} >= {"A_recall_basis", "B_source_binding", "C_scoring_state"},
          "E_all_true": all(v is True for k, v in es.items() if isinstance(v, bool)),
          "no_new_case_run": True}
(OUT / "internal_R1D_CHECKS.json").write_text(json.dumps(checks, indent=1))
print(json.dumps(checks, indent=1)); sys.exit(0 if all(checks.values()) else 1)
