"""Step pipeline orchestration (R2) with hard step isolation.

- replay binding (arm/step_id/model_key) flows to retrieval AND scoring replay
  adapters; the wrapper scoring path receives no new parameter (it ignores
  the keyword by signature default).
- pool cap: exceeding configured max_size BLOCKS the whole step (backend is
  never called); no subset scoring. Invalid cap values are rejected.
- full order per wrapper rule; Top-K is a display slice; executed-but-
  undisclosed candidates land in scores_not_disclosed with per-UID identity.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .config import ToolConfig
from .pool import build_pool, scoring_pairs, all_display_uids
from .retrieval_backends import make_retrieval, ReplayBinding
from .schemas import (PathwayResult, RecallGroup, StepResult, NotEvaluated, HostSource)
from .scoring_backends import make_scoring
from .sources_backends import make_sources, authoritative_sig
from .traits_backends import make_traits, collect_traits


def _binding_for(cfg, step_id: str, model_key_sha256: str) -> Optional[ReplayBinding]:
    if cfg.retrieval.backend != "cache_replay_c2":
        return None
    return ReplayBinding(arm=cfg.retrieval.replay_arm,
                         step_id=step_id or cfg.retrieval.replay_step_id,
                         model_key_sha256=model_key_sha256 or cfg.retrieval.replay_model_key_sha256,
                         source_file=cfg.retrieval.c2_export_dir)


def predict_reaction(reaction_smiles: str, step_id: str = "S01", pathway_id: str = "single",
                     config: Optional[ToolConfig] = None, model_reaction: Optional[str] = None,
                     recall_topk: int = 10, injected: Optional[Dict[str, Any]] = None,
                     runtime_factory=None, backend_notes: Optional[List[str]] = None,
                     model_key_sha256: str = "") -> StepResult:
    cfg = config or ToolConfig()
    inj = injected or {}
    query_reaction = model_reaction or reaction_smiles
    rep_source = "caller_model_reaction" if model_reaction else "caller_passthrough"
    out = StepResult(step_id=step_id, pathway_id=pathway_id,
                     reaction_smiles_original=reaction_smiles,
                     model_query_reaction=query_reaction,
                     query_representation_source=rep_source,
                     retrieval_status="", retrieval_mode="", recall_repr_used="")
    out.backend_kinds = {
        "retrieval": "TEST_DOUBLE" if inj.get("retrieval") else cfg.retrieval.backend,
        "scoring": ("TEST_DOUBLE" if inj.get("scoring")
                    else f"{cfg.scoring.backend}+TEST_RUNTIME_BOUNDARY" if runtime_factory
                    else cfg.scoring.backend),
        "sources": "TEST_DOUBLE" if inj.get("sources") else cfg.sources.backend,
        "traits": "TEST_DOUBLE" if inj.get("traits") else
                  ("c8+dehp" if cfg.traits.c8_lookup_index and cfg.traits.dehp_package_root
                   else "c8" if cfg.traits.c8_lookup_index else "dehp" if cfg.traits.dehp_package_root else "none")}

    binding = _binding_for(cfg, step_id, model_key_sha256)

    retrieval = make_retrieval(cfg.retrieval, injected=inj.get("retrieval"))
    pairs_ctx = {}
    if retrieval is None:
        out.retrieval_status = "RETRIEVAL_NOT_CONFIGURED"
    else:
        res = retrieval.retrieve(query_reaction, topk=recall_topk, binding=binding)
        out.retrieval_status = res.status
        out.retrieval_mode = res.mode
        out.recall_repr_used = res.recall_repr
        if res.status in ("OK", "OK_CACHE_REPLAY"):
            out.groups = [RecallGroup(rank=i + 1, reaction_cd=g.reaction_cd, similarity=g.similarity,
                                      exact_same_direction_retrieval_repr=g.exact_same_direction_retrieval_repr,
                                      undirected_key=g.undirected_key, group_cds=list(g.group_cds),
                                      associated_pairs=g.associated_pairs)
                          for i, g in enumerate(res.groups)]
            cands, rows = build_pool(res.groups, retrieval)
            out.pool_candidates = cands
            out.pool_status = "OK" if cands else "EMPTY_NO_ASSOCIATED_ENZYMES"

    # ---- pool cap: whole-step blocking, never a subset ----
    cands = out.pool_candidates
    blocked = None
    if cfg.pool.max_size is not None:
        if type(cfg.pool.max_size) is not int or cfg.pool.max_size <= 0:
            blocked = ("POOL_CAP_INVALID", f"max_size={cfg.pool.max_size!r} must be a positive integer; "
                                           "scoring not attempted")
        elif len(cands) > cfg.pool.max_size:
            blocked = ("POOL_LIMIT_EXCEEDED",
                       f"configured max_size={cfg.pool.max_size} < {len(cands)} candidates; whole step blocked; "
                       "backend NOT called; subset selection by any key is forbidden")
    pairs = scoring_pairs(cands)

    scoring = make_scoring(cfg.scoring, runtime_factory=runtime_factory, injected=inj.get("scoring"))
    if blocked is not None:
        out.scoring_status = blocked[0]
        out.not_evaluated = [NotEvaluated(u, s, blocked[0], blocked[1]) for u, s in pairs]
        return _finish(out, cfg, inj, scoring_pairs, cands, retrieval, blocked_note=blocked[1])
    if not pairs:
        out.scoring_status = "EMPTY_POOL_NO_CANDIDATES"
        return _finish(out, cfg, inj, scoring_pairs, cands, retrieval)
    if scoring is None:
        out.scoring_status = "BACKEND_NOT_CONFIGURED"
        out.not_evaluated = [NotEvaluated(u, s, "BACKEND_NOT_CONFIGURED",
                                          "no scoring backend configured; refusing mock scores")
                             for u, s in pairs]
        return _finish(out, cfg, inj, scoring_pairs, cands, retrieval)

    if getattr(scoring, "accepts_binding", False):
        outcome = scoring.score(query_reaction, pairs, binding=binding)
    else:
        outcome = scoring.score(query_reaction, pairs)
    out.scoring_status = outcome.status
    out.all_candidate_scores = outcome.all_scored
    k = cfg.scoring.top_k
    out.ranked = [c for c in out.all_candidate_scores if c.display_rank is not None][:k]
    out.not_evaluated = outcome.not_evaluated
    out.scores_not_disclosed = outcome.not_disclosed
    out.replay_coverage = outcome.coverage or None
    out.model_version = outcome.model_version
    out.evidence_hash = outcome.evidence_hash
    out.batch_shape = outcome.batch_shape
    return _finish(out, cfg, inj, scoring_pairs, cands, retrieval)


def _finish(out: StepResult, cfg, inj, _sp, cands, retrieval, blocked_note: str = "") -> StepResult:
    sources = make_sources(cfg.sources, injected=inj.get("sources"))
    for uid in all_display_uids(cands):
        hs = sources.lookup(uid) if sources is not None else \
            HostSource(uid=uid, status="SOURCES_TABLE_NOT_CONFIGURED")
        out.hosts.append(hs)
    c8, dehp = make_traits(cfg.traits)
    if inj.get("traits") is not None:
        c8, dehp = inj["traits"], None
    seen = set()
    for hs in out.hosts:
        sig = authoritative_sig(hs)
        key = sig or f"NOSIG::{hs.uid}"
        if key in seen:
            continue
        seen.add(key)
        out.traits.append(collect_traits(c8, dehp, sig))
    return out


def predict_steps(steps: List[Dict[str, Any]], pathway_id: str = "pathway",
                  config: Optional[ToolConfig] = None, recall_topk: int = 10,
                  injected: Optional[Dict[str, Any]] = None, runtime_factory=None) -> PathwayResult:
    res = PathwayResult(pathway_id=pathway_id, n_steps=len(steps))
    for st in steps:
        sid = str(st.get("step_id", ""))
        rxn = str(st.get("reaction_smiles", ""))
        try:
            sr = predict_reaction(rxn, step_id=sid, pathway_id=pathway_id, config=config,
                                  model_reaction=st.get("model_reaction") or None,
                                  recall_topk=recall_topk, injected=injected,
                                  runtime_factory=runtime_factory,
                                  model_key_sha256=str(st.get("model_key_sha256", "")))
        except Exception as exc:
            from .schemas import StepResult as _SR
            sr = _SR(step_id=sid, pathway_id=pathway_id,
                     reaction_smiles_original=rxn, model_query_reaction=rxn,
                     query_representation_source="caller_passthrough",
                     retrieval_status="FAILED_TYPED", retrieval_mode="", recall_repr_used="",
                     step_error=f"{type(exc).__name__}: {str(exc)[:300]}")
        res.steps.append(sr)
    return res
