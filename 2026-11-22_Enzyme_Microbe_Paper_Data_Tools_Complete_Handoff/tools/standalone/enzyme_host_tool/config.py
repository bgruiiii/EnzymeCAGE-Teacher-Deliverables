"""Tool configuration (R2). Replay-only binding fields are separate from the
real wrapper scoring semantics (the wrapper path ignores them entirely)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class RetrievalCfg:
    backend: str = "none"              # fixed_r3 | cache_replay_c2 | none
    master_parquet: str = ""
    pairs_parquet: str = ""
    mode: str = "PRODUCTION_INCLUDE_EXACT"
    # evidence_tiers: NOT supported by this wrapper. A non-empty value is
    # rejected as RETRIEVAL_PARAM_UNSUPPORTED; no new filtering is invented.
    evidence_tiers: list = field(default_factory=list)
    c2_export_dir: str = ""
    replay_arm: str = "legacy_esm2_3b"
    # REPLAY-ONLY binding defaults (per-step values may override via steps input)
    replay_step_id: str = ""
    replay_model_key_sha256: str = ""


@dataclass
class PoolCfg:
    max_size: Optional[int] = None     # None = keep all. If set and exceeded: WHOLE-STEP
                                       # blocking (backend not called), never a subset.


@dataclass
class ScoringCfg:
    backend: str = "none"              # enzyme_cage_wrapper | enzyme_cage_wrapper_native_c95 | cache_replay_c2 | none
    wrapper_code_root: str = ""
    enzymecage_source_root: str = ""
    weights_package_root: str = ""
    top_k: int = 10                    # DISPLAY view only; full ordering preserved for all evaluated
    return_ci: bool = True
    c2_export_dir: str = ""
    replay_arm: str = "legacy_esm2_3b"
    replay_trace: bool = True
    replay_step_id: str = ""           # replay-only
    replay_model_key_sha256: str = ""  # replay-only
    native_binding: dict = field(default_factory=dict)  # R4 native C95 binding paths/ctx


@dataclass
class SourcesCfg:
    backend: str = "b1_revision1_table"
    b1_table: str = ""


@dataclass
class TraitsCfg:
    dehp_package_root: str = ""
    c8_lookup_index: str = ""


@dataclass
class ToolConfig:
    retrieval: RetrievalCfg = field(default_factory=RetrievalCfg)
    pool: PoolCfg = field(default_factory=PoolCfg)
    scoring: ScoringCfg = field(default_factory=ScoringCfg)
    sources: SourcesCfg = field(default_factory=SourcesCfg)
    traits: TraitsCfg = field(default_factory=TraitsCfg)

    @staticmethod
    def from_json(path: str) -> "ToolConfig":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return ToolConfig(
            retrieval=RetrievalCfg(**raw.get("retrieval", {})),
            pool=PoolCfg(**raw.get("pool", {})),
            scoring=ScoringCfg(**raw.get("scoring", {})),
            sources=SourcesCfg(**raw.get("sources", {})),
            traits=TraitsCfg(**raw.get("traits", {})),
        )

    def validation_notes(self) -> list:
        notes = []
        rc = self.retrieval
        if rc.backend == "fixed_r3":
            if rc.evidence_tiers:
                notes.append("retrieval.evidence_tiers non-empty -> RETRIEVAL_PARAM_UNSUPPORTED (not implemented; nothing silently filtered)")
            for label, p in (("master_parquet", rc.master_parquet), ("pairs_parquet", rc.pairs_parquet)):
                if not p or not Path(p).is_file():
                    notes.append(f"retrieval.{label} missing/empty -> RETRIEVAL_ASSET_MISSING")
        elif rc.backend == "cache_replay_c2":
            if not rc.c2_export_dir or not Path(rc.c2_export_dir).is_dir():
                notes.append("retrieval.c2_export_dir missing -> CACHE_REPLAY_ASSET_MISSING")
        sc = self.scoring
        if sc.backend == "enzyme_cage_wrapper":
            for label, p in (("wrapper_code_root", sc.wrapper_code_root),
                             ("enzymecage_source_root", sc.enzymecage_source_root),
                             ("weights_package_root", sc.weights_package_root)):
                if not p or not Path(p).is_dir():
                    notes.append(f"scoring.{label} missing/empty -> BACKEND_MISSING_DEPENDENCY (preflight)")
        elif sc.backend == "cache_replay_c2":
            if not sc.c2_export_dir or not Path(sc.c2_export_dir).is_dir():
                notes.append("scoring.c2_export_dir missing -> CACHE_REPLAY_ASSET_MISSING")
        if self.pool.max_size is not None and (type(self.pool.max_size) is not int or self.pool.max_size <= 0):
            notes.append("pool.max_size must be a positive integer -> POOL_CAP_INVALID")
        if self.sources.backend == "b1_revision1_table" and not self.sources.b1_table:
            notes.append("sources.b1_table empty -> SOURCES_TABLE_NOT_CONFIGURED")
        if self.traits.c8_lookup_index and not Path(self.traits.c8_lookup_index).is_file():
            notes.append("traits.c8_lookup_index set but file missing -> C8 backend error visible (does not hide SCNET)")
        return notes
