"""Retrieval backends (R2).

FixedR3Retrieval: mirrors b2a frozen index semantics; unsupported non-empty
evidence_tiers is rejected at construction (no new filtering invented);
missing columns/deps/assets give typed statuses.

C2CacheReplayRetrieval: STRICT final-object binding. The replay identity is
(arm, step_id, model_key_sha256, model_reaction, scientific_uid, sequence_sha256).
Rows are selected by step_id ONLY (never by searching the query string first —
42 queries appear in multiple steps). Missing step context while the query
matches several steps -> CACHE_REPLAY_AMBIGUOUS_STEP; any supplied field that
disagrees with the frozen row -> CACHE_REPLAY_BINDING_MISMATCH. expand_pairs
carries per-row sequence_sha256 + asset_uid + source file identity so the
scoring side can re-verify.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path

_VENDORED = Path(__file__).resolve().parent.parent / "vendored"
MODES = ("PRODUCTION_INCLUDE_EXACT", "BENCHMARK_QUERY_EXCLUDED")


@dataclass
class ReplayBinding:
    """Replay-only context passed from the orchestrator. The wrapper path never
    receives or uses it (no intrusion into real wrapper scoring semantics)."""
    arm: str = ""
    step_id: str = ""
    model_key_sha256: str = ""
    source_file: str = ""


def replay_context_mismatch(cfg, binding, source_file):
    """Reject an explicit context from another arm or export location."""
    if binding.arm and binding.arm != cfg.replay_arm:
        return "CACHE_REPLAY_BINDING_MISMATCH:arm"
    if binding.source_file:
        supplied = Path(binding.source_file).resolve()
        actual = Path(source_file).resolve()
        if supplied not in (actual, actual.parent):
            return "CACHE_REPLAY_BINDING_MISMATCH:source_file"
    return ""


class RetrievalOutcome:
    def __init__(self, status, groups=None, mode="", recall_repr="", detail="", freeze=None):
        self.status = status
        self.groups = groups or []
        self.mode = mode
        self.recall_repr = recall_repr
        self.detail = detail
        self.freeze = freeze or {}


class _Group:
    def __init__(self, reaction_cd, score, exact_repr, uk, members, n_pairs, pair_rows=None):
        self.reaction_cd = reaction_cd
        self.similarity = score
        self.exact_same_direction_retrieval_repr = exact_repr
        self.undirected_key = uk
        self.group_cds = members
        self.associated_pairs = n_pairs
        # None means native expansion is required; [] means an explicitly
        # supplied empty set. Do not collapse those distinct states.
        self.pair_rows = pair_rows


class FixedR3Retrieval:
    kind = "fixed_r3_frozen"

    def __init__(self, cfg):
        self.cfg = cfg
        self._load_error = None
        self._index = None
        self._fre = None
        self._uk_of = {}
        self._uk_members = {}
        self._repr_members = {}
        self._repr_of = {}
        self._uk_by_repr = {}
        self._pairs_by_cd = {}
        self.freeze_info = {}
        if cfg.evidence_tiers:
            # parameter path executes for real: reject, do not silently ignore
            self._load_error = ("RETRIEVAL_PARAM_UNSUPPORTED:evidence_tiers is not implemented by this wrapper; "
                                "no filtering was invented (frozen recall unchanged)")

    def _load(self):
        if self._index is not None or self._load_error:
            return
        for label, p in (("master_parquet", self.cfg.master_parquet), ("pairs_parquet", self.cfg.pairs_parquet)):
            if not p or not Path(p).is_file():
                self._load_error = f"RETRIEVAL_ASSET_MISSING:{label}"
                return
        if self.cfg.mode not in MODES:
            self._load_error = f"RETRIEVAL_PARAM_UNSUPPORTED:mode={self.cfg.mode!r}; allowed={MODES}"
            return
        if os.environ.get("PYTHONHASHSEED", None) != "0":
            self._load_error = "RETRIEVAL_ENVIRONMENT_UNAVAILABLE:PYTHONHASHSEED!=0"
            return
        try:
            if str(_VENDORED) not in sys.path:
                sys.path.insert(0, str(_VENDORED))
            import pandas as pd
            import fixed_retrieval_engine as FRE
        except Exception as exc:
            self._load_error = f"RETRIEVAL_ENVIRONMENT_UNAVAILABLE:{type(exc).__name__}: {str(exc)[:200]}"
            return
        try:
            mp = pd.read_parquet(self.cfg.master_parquet)
            ps = pd.read_parquet(self.cfg.pairs_parquet)
        except Exception as exc:
            self._load_error = f"RETRIEVAL_ASSET_MISSING:unreadable:{type(exc).__name__}: {str(exc)[:160]}"
            return
        master_need = {"canonical_directional", "chemistry_equivalence_undirected_key"}
        pairs_need = {"canonical_directional", "retrieval_repr",
                      "scientific_pair_ok", "canonical_protein_id", "sequence_sha256",
                      "accessions", "source_datasets", "evidence_tiers"}
        miss = sorted(c for c in master_need if c not in mp.columns)
        if miss:
            self._load_error = f"RETRIEVAL_SCHEMA_MISMATCH:master_columns_missing={miss}"
            return
        miss = sorted(c for c in pairs_need if c not in ps.columns)
        if miss:
            self._load_error = f"RETRIEVAL_SCHEMA_MISMATCH:pairs_columns_missing={miss}"
            return
        self._fre = FRE
        pr = ps[["canonical_directional", "retrieval_repr"]].dropna(subset=["retrieval_repr"])
        first, multi = {}, set()
        for cd, rep in zip(pr.canonical_directional, pr.retrieval_repr):
            if cd not in first:
                first[cd] = rep
            elif first[cd] != rep:
                multi.add(cd)
        uk = dict(zip(mp.canonical_directional, mp.chemistry_equivalence_undirected_key))
        qrepr = FRE.query_retrieval_repr
        reactions = []
        fix_up = 0
        for cd in mp.canonical_directional:
            rep = first.get(cd)
            if rep is None or cd in multi or ">>" not in (rep or ""):
                got = qrepr(cd)
                rep = got if got else cd
                fix_up += 1
            u = uk.get(cd)
            reactions.append({"canonical_directional": cd, "retrieval_repr": rep,
                              "undirected_key": u if isinstance(u, str) else None})
        self._uk_of = uk
        members = {}
        for r in reactions:
            if r["undirected_key"]:
                members.setdefault(r["undirected_key"], set()).add(r["canonical_directional"])
        self._uk_members = members
        # The audited b2a grouping includes BOTH undirected members and
        # members sharing the frozen retrieval representation.
        for r in reactions:
            cd, rep = r["canonical_directional"], r["retrieval_repr"]
            self._repr_of[cd] = rep
            self._repr_members.setdefault(rep, set()).add(cd)
            self._uk_by_repr.setdefault(rep, r["undirected_key"])
        for row in ps.itertuples():
            if not bool(getattr(row, "scientific_pair_ok", True)):
                continue
            cd = row.canonical_directional
            self._pairs_by_cd.setdefault(cd, []).append({
                "cd": cd, "pair_id": str(getattr(row, "pair_id", "")),
                "canonical_protein_id": str(row.canonical_protein_id),
                "accessions": str(row.accessions), "sequence_sha256": str(row.sequence_sha256),
                "source_datasets": str(row.source_datasets), "evidence_tiers": str(row.evidence_tiers),
                "record_ids": str(getattr(row, "record_ids", ""))})
        r2e = {cd: {(p["canonical_protein_id"], p["sequence_sha256"]) for p in rows_}
               for cd, rows_ in self._pairs_by_cd.items()}
        self._index = FRE.FixedIndex("standalone_r2", reactions, r2e)
        self.freeze_info = {"library_reactions": len(reactions),
                            "repr_from_pairs_frozen": len(reactions) - fix_up,
                            "repr_recomputed_or_fallback": fix_up,
                            "multi_repr_collisions": len(multi)}

    def retrieve(self, target_reaction_smiles, topk=10, binding=None):
        self._load()
        if self._load_error:
            return RetrievalOutcome(self._load_error, mode=self.cfg.mode)
        FRE = self._fre
        q_repr = FRE.query_retrieval_repr(target_reaction_smiles)
        if not q_repr:
            return RetrievalOutcome("RETRIEVAL_QUERY_REPRESENTATION_FAILED", mode=self.cfg.mode)
        exact_cd = set(self._index.by_repr.get(q_repr, []))
        ranked = FRE.retrieve(self._index, q_repr, self.cfg.mode,
                              q_uk=self._uk_by_repr.get(q_repr), topk=None)
        groups, used = [], set()
        for cd, score in ranked:
            uk = self._uk_of.get(cd)
            if uk and uk in used:
                continue
            if uk:
                used.add(uk)
            mem = sorted({cd} | self._uk_members.get(uk, set()) |
                         self._repr_members.get(self._repr_of.get(cd), set()))
            n = sum(len(self._pairs_by_cd.get(m, [])) for m in mem)
            groups.append(_Group(cd, score, cd in exact_cd, uk or "", mem, n))
            if len(groups) >= topk:
                break
        return RetrievalOutcome("OK", groups=groups, mode=self.cfg.mode,
                                recall_repr=q_repr, freeze=self.freeze_info)

    def expand_pairs(self, cds):
        out = []
        for cd in cds:
            for p in self._pairs_by_cd.get(cd, []):
                q = dict(p)
                q["reference_cd"] = cd
                out.append(q)
        return out


class C2CacheReplayRetrieval:
    kind = "CACHE_REPLAY_c2_bound_rows"

    def __init__(self, cfg):
        self.cfg = cfg
        self._by_step = {}
        self._file = ""
        self._error = None
        p = Path(cfg.c2_export_dir or "") / "STEP_CANDIDATE_RANKINGS.tsv.gz"
        self._file = str(p)
        if not p.is_file():
            self._error = f"CACHE_REPLAY_ASSET_MISSING:{p}"
            return
        self._file_sha256 = hashlib.sha256(p.read_bytes()).hexdigest()
        with gzip.open(p, "rt", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r["arm"] == cfg.replay_arm:
                    self._by_step.setdefault(r["step_id"], []).append(r)

    def _resolve_rows(self, query, binding):
        if binding is None:
            binding = ReplayBinding(arm=self.cfg.replay_arm,
                                    step_id=self.cfg.replay_step_id,
                                    model_key_sha256=self.cfg.replay_model_key_sha256)
        mismatch = replay_context_mismatch(self.cfg, binding, self._file)
        if mismatch:
            return None, mismatch
        step_id = binding.step_id
        if step_id:
            rows = self._by_step.get(step_id)
            if not rows:
                return None, "CACHE_REPLAY_STEP_NOT_IN_FROZEN_EXPORT"
        else:
            hits = {sid: rs for sid, rs in self._by_step.items() if rs and rs[0]["model_reaction"] == query}
            if not hits:
                return None, "CACHE_REPLAY_STEP_NOT_IN_FROZEN_EXPORT"
            if len(hits) > 1:
                return None, (f"CACHE_REPLAY_AMBIGUOUS_STEP:query matches {len(hits)} steps {sorted(hits)}; "
                              "step_id binding required; first/last never guessed")
            rows = next(iter(hits.values()))
        r0 = rows[0]
        if r0["model_reaction"] != query:
            return None, "CACHE_REPLAY_BINDING_MISMATCH:query!=frozen model_reaction for this step"
        if binding.model_key_sha256 and binding.model_key_sha256 != r0["model_key_sha256"]:
            return None, "CACHE_REPLAY_BINDING_MISMATCH:model_key_sha256"
        return rows, "OK"

    def retrieve(self, query, topk=10, binding=None):
        if self._error:
            return RetrievalOutcome(self._error, mode="CACHE_REPLAY")
        rows, status = self._resolve_rows(query, binding)
        if rows is None:
            return RetrievalOutcome(status, mode="CACHE_REPLAY")
        r0 = rows[0]
        cd = f"REPLAY::{r0['step_id']}::{r0['model_key_sha256']}"
        pair_rows = [{
            "cd": cd, "reference_cd": cd,
            "pair_id": f"C2::{r0['arm']}::{r0['step_id']}::{r['scientific_uid']}",
            "canonical_protein_id": r["scientific_uid"],
            "asset_uid": r.get("asset_uid", ""),
            "accessions": r.get("scientific_uid", ""),
            "sequence_sha256": r.get("sequence_sha256", ""),
            "source_datasets": "C2_export_frozen_pool",
            "evidence_tiers": "replay_only",
            "record_ids": (f"rank={r['rank']}|model_key={r['model_key_sha256']}|ctx={r['ctx']}"
                           f"|source_member={r.get('source_member','')}|source_sha256={r.get('source_sha256','')}"),
            "source_file": self._file,
            "source_file_sha256": self._file_sha256,
        } for r in rows]
        grp = _Group(cd, "frozen_pool_replay_not_similarity", False, "", [cd], len(rows), pair_rows)
        self._last_rows = rows
        self._last_step = r0["step_id"]
        return RetrievalOutcome("OK_CACHE_REPLAY", groups=[grp], mode="CACHE_REPLAY",
                                recall_repr=query,
                                detail=f"arm={self.cfg.replay_arm} step={r0['step_id']} "
                                       f"key={r0['model_key_sha256'][:16]}.. rows={len(rows)}")

    def expand_pairs(self, cds):
        # replay groups carry pair_rows directly (bound rows); nothing else is expanded
        return []


def make_retrieval(cfg, injected=None):
    if injected is not None:
        return injected
    if cfg.backend == "fixed_r3":
        return FixedR3Retrieval(cfg)
    if cfg.backend == "cache_replay_c2":
        return C2CacheReplayRetrieval(cfg)
    return None
