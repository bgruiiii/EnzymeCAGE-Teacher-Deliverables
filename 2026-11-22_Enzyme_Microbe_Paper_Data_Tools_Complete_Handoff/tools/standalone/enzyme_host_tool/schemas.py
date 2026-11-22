"""Typed outputs (R2: disclosure separation + per-backend statuses + evidence pointers)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RecallGroup:
    rank: int
    reaction_cd: str
    similarity: Any
    exact_same_direction_retrieval_repr: bool
    undirected_key: str
    group_cds: List[str]
    associated_pairs: int


@dataclass
class PoolCandidate:
    sequence_sha256: str
    canonical_protein_id: str
    associated_uids: List[str]
    provenance_records: List[Dict[str, Any]] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    evidence_tiers: List[str] = field(default_factory=list)


@dataclass
class ScoredCandidate:
    uid: str
    sequence_sha256: str
    score: float
    rank: int                                  # position in the FULL ordering (wrapper rule)
    ensemble_ci: Optional[List[float]] = None
    display_rank: Optional[int] = None         # within Top-K display view only


@dataclass
class NotEvaluated:
    uid: str
    sequence_sha256: str
    reason: str   # BACKEND_NOT_CONFIGURED | BACKEND_ENVIRONMENT_UNAVAILABLE | ENZYME_ASSET_MISSING |
                  # REACTION_ASSET_MISSING | SEQUENCE_IDENTITY_CONFLICT | FORWARD_FAILED_TYPED |
                  # POOL_LIMIT_EXCEEDED | CACHE_REPLAY_UID_NOT_IN_BOUND_STEP |
                  # CACHE_REPLAY_SEQUENCE_SHA_MISMATCH
    detail: str = ""


@dataclass
class HostSource:
    uid: str
    status: str                    # ROW_PRESENT | UID_NOT_IN_B1_COHORT | SOURCES_TABLE_* ...
    row_present: bool = False
    source_status: str = ""
    authoritative_source_signature: str = ""
    source_key_status: str = ""
    lookup_route: str = ""
    source_resolution: str = ""
    orig_taxid: str = ""
    orig_organism_name: str = ""
    cur_tax_id: str = ""
    cur_species_tax_id: str = ""
    cur_species_name: str = ""
    current_taxonomy_group: str = ""
    in_microbe_scope: Optional[bool] = None
    microbe_scope_stage: str = ""
    original_strains: List[str] = field(default_factory=list)
    proteome_linked_strains: List[Dict[str, str]] = field(default_factory=list)
    representative_registration_coverage: str = ""
    representative_validation: str = ""
    reviewed: str = ""
    protein_existence_raw: str = ""
    protein_existence: str = ""
    source_stage: str = ""
    source_binding_kind: str = ""
    note: str = ""
    evidence_ids: List[str] = field(default_factory=list)      # B1 table's own evidence pointers
    evidence_source_file: str = ""                              # the B1 file identity used
    evidence_row_key: str = ""                                   # file + scientific_uid locator


@dataclass
class TraitEvidence:
    source_signature: str
    backend: str
    status: str            # OK | OK_WITH_BACKEND_ERRORS | NO_RECORD_FOR_KEY | NOT_CONFIGURED | BACKEND_ERROR
    slots: List[Dict[str, Any]] = field(default_factory=list)
    predicted_records: List[Dict[str, Any]] = field(default_factory=list)
    representative_records: List[Dict[str, Any]] = field(default_factory=list)
    backend_statuses: List[Dict[str, Any]] = field(default_factory=list)  # per-backend status/detail
    n_slots: int = 0
    n_observed: int = 0
    n_identity_only: int = 0
    n_missing: int = 0
    all_slots_present: bool = False
    prediction_required_slots: List[str] = field(default_factory=list)
    note: str = ""


@dataclass
class StepResult:
    step_id: str
    pathway_id: str
    reaction_smiles_original: str
    model_query_reaction: str
    query_representation_source: str
    retrieval_status: str
    retrieval_mode: str
    recall_repr_used: str
    groups: List[RecallGroup] = field(default_factory=list)
    pool_status: str = ""
    pool_candidates: List[PoolCandidate] = field(default_factory=list)
    scoring_status: str = ""
    model_version: str = ""
    evidence_hash: str = ""
    batch_shape: Optional[Dict[str, Any]] = None
    all_candidate_scores: List[ScoredCandidate] = field(default_factory=list)
    ranked: List[ScoredCandidate] = field(default_factory=list)
    scores_not_disclosed: List[Dict[str, str]] = field(default_factory=list)  # executed, score unknown
    not_evaluated: List[NotEvaluated] = field(default_factory=list)           # truly unevaluated
    replay_coverage: Optional[Dict[str, Any]] = None                          # bound-step uid/sha set diff
    hosts: List[HostSource] = field(default_factory=list)
    traits: List[TraitEvidence] = field(default_factory=list)
    step_error: str = ""
    backend_kinds: Dict[str, str] = field(default_factory=dict)


@dataclass
class PathwayResult:
    pathway_id: str
    n_steps: int
    steps: List[StepResult] = field(default_factory=list)
