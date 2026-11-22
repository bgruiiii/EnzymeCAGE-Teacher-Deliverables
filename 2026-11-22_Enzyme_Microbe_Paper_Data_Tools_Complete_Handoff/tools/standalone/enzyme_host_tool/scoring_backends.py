"""Scoring backends (R2).

Wrapper path: the ORIGINAL wrapper ordering rule is preserved — aggregation
comes from wrapper.utils.aggregate_seed_scores (sort key (-score, uid)) and is
NEVER re-sorted here; Top-K is a display slice of that single ordering. The
trace is validated (forward flag, UID set+order vs forwarded valid list, five
finite vectors of equal length); if disclosure fails, executed-but-undisclosed
candidates are listed per UID in a separate structure — never mislabelled
"not evaluated", never zero-filled.

Replay path (C2CacheReplayScoring): rows are resolved by strict binding
(arm+step_id+model_key_sha256+query), scores/sequence SHAs re-verified
per-row against the candidate set, coverage differences disclosed; ensemble_ci
is the wrapper's 2.5%/97.5% LINEAR-INTERPOLATION QUANTILES recomputed from the
five cached seed probabilities (labelled cache-derived), NOT min/max.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import math
import sys
from pathlib import Path

from .schemas import NotEvaluated, ScoredCandidate
from .retrieval_backends import replay_context_mismatch

ENV = "BACKEND_ENVIRONMENT_UNAVAILABLE"


class ScoreOutcome:
    def __init__(self, status, all_scored=None, not_evaluated=None, not_disclosed=None,
                 model_version="", evidence_hash="", batch_shape=None, coverage=None):
        self.status = status
        self.all_scored = all_scored or []
        self.not_evaluated = not_evaluated or []
        self.not_disclosed = not_disclosed or []
        self.model_version = model_version
        self.evidence_hash = evidence_hash
        self.batch_shape = batch_shape
        self.coverage = coverage or {}


class _Binding:
    """Replay-only context object; wrapper ignores its argument."""
    def __init__(self, arm="", step_id="", model_key_sha256="", source_file=""):
        self.arm = arm
        self.step_id = step_id
        self.model_key_sha256 = model_key_sha256
        self.source_file = source_file


def _linear_quantile(sorted_vals, q):
    """torch.quantile(interpolation='linear') equivalent for finite vectors."""
    n = len(sorted_vals)
    pos = q * (n - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return sorted_vals[int(pos)]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


class EnzymeCAGEWrapperBackend:
    kind = "enzyme_cage_wrapper"

    def __init__(self, cfg, runtime_factory=None):
        self.cfg = cfg
        self._runtime_factory = runtime_factory
        self._rt = None
        self._preflight_error = None

    def preflight(self):
        if self._preflight_error or self._rt is not None:
            return
        c = self.cfg
        for label, p in (("wrapper_code_root", c.wrapper_code_root),
                         ("enzymecage_source_root", c.enzymecage_source_root),
                         ("weights_package_root", c.weights_package_root)):
            if not p or not Path(p).is_dir():
                self._preflight_error = f"BACKEND_MISSING_DEPENDENCY:{label} path not set/exists"
                return
        try:
            import torch  # noqa: F401
        except Exception:
            self._preflight_error = "BACKEND_MISSING_DEPENDENCY:torch not importable"
            return

    def _runtime(self):
        if self._rt is not None:
            return self._rt
        if self._runtime_factory is not None:
            self._rt = self._runtime_factory()
            return self._rt
        self.preflight()
        if self._preflight_error:
            return None
        for root in (self.cfg.wrapper_code_root, self.cfg.enzymecage_source_root):
            if root not in sys.path:
                sys.path.insert(0, root)
        try:
            from wrapper import predictor
            self._rt = predictor.initialize_runtime(self.cfg.weights_package_root)
            return self._rt
        except Exception as exc:
            self._preflight_error = f"{ENV}: initialize_runtime: {type(exc).__name__}: {str(exc)[:200]}"
            return None

    def score(self, query_reaction: str, candidates, binding=None):
        rt = self._runtime()
        if rt is None:
            return ScoreOutcome(ENV, not_evaluated=[
                NotEvaluated(u, s, ENV, self._preflight_error or "runtime unavailable")
                for u, s in candidates])
        from wrapper.schema import EnzymeCAGERequest
        from wrapper.utils import aggregate_seed_scores
        uniq, seen = [], set()
        for u, s in candidates:
            if u not in seen:
                seen.add(u)
                uniq.append((u, s))
        valid, ne = [], []
        for uid, sha in uniq:
            if not rt.asset_index.has_enzyme(uid):
                ne.append(NotEvaluated(uid, sha, "ENZYME_ASSET_MISSING"))
                continue
            asset_sha = hashlib.sha256(str(rt.asset_index.sequence_for(uid)).encode()).hexdigest()
            if asset_sha != sha:
                ne.append(NotEvaluated(uid, sha, "SEQUENCE_IDENTITY_CONFLICT",
                                       f"asset_sha256={asset_sha[:16]}.. candidate_sha256={sha[:16]}.."))
                continue
            valid.append(uid)
        if not valid:
            return ScoreOutcome("ENZYME_ASSETS_EMPTY", not_evaluated=ne)
        try:
            req = EnzymeCAGERequest(reaction_smiles=query_reaction, enzyme_pool_uids=valid,
                                    top_k=min(self.cfg.top_k, 100), return_ci=self.cfg.return_ci)
            resp = rt.predict(req)
        except Exception as exc:
            name = type(exc).__name__
            if name == "MissingReactionAssetError":
                return ScoreOutcome("REACTION_ASSET_MISSING", not_evaluated=ne + [
                    NotEvaluated(u, s, "REACTION_ASSET_MISSING", str(exc)[:200]) for u, s in uniq])
            return ScoreOutcome("FORWARD_FAILED_TYPED", not_evaluated=ne + [
                NotEvaluated(u, s, "FORWARD_FAILED_TYPED", f"{name}: {str(exc)[:200]}") for u, s in uniq])

        trace = getattr(rt, "last_trace", None) or {}
        per_seed = trace.get("per_seed_scores") or []
        trace_valid = list(trace.get("valid_uids") or [])
        sha_of = dict(uniq)
        try:
            trace_ok = (trace.get("forward_executed") is True
                        and len(per_seed) == 5
                        and trace_valid == valid
                        and all(len(vec) == len(valid) for vec in per_seed)
                        and all(isinstance(x, (int, float)) and math.isfinite(float(x))
                                for vec in per_seed for x in vec))
        except (TypeError, ValueError, OverflowError):
            trace_ok = False
        if not trace_ok:
            # An invalid trace must not let invalid/foreign response rows
            # re-enter via the Top-K fallback. Keep only finite scores for
            # this request and disclose every remaining UID separately.
            response_rows = []
            disclosed = set()
            for r in resp.ranked_enzymes:
                try:
                    row_ok = (r.uid in valid and r.uid not in disclosed
                              and math.isfinite(float(r.score))
                              and (r.ensemble_ci is None or
                                   (len(r.ensemble_ci) == 2 and
                                    all(math.isfinite(float(x)) for x in r.ensemble_ci))))
                except (TypeError, ValueError, OverflowError):
                    row_ok = False
                if row_ok:
                    response_rows.append(r)
                    disclosed.add(r.uid)
            not_disclosed = [{"uid": u, "sequence_sha256": sha_of.get(u, ""),
                              "state": "EXECUTED_SCORE_NOT_DISCLOSED",
                              "detail": "last_trace contract unmet; no valid finite response score disclosed for this UID"}
                             for u in valid if u not in disclosed]
            all_scored = []
            for r in response_rows:
                all_scored.append(ScoredCandidate(uid=r.uid, sequence_sha256=sha_of.get(r.uid, ""),
                                                  score=r.score, rank=r.rank, display_rank=r.rank,
                                                  ensemble_ci=list(r.ensemble_ci) if r.ensemble_ci else None))
            return ScoreOutcome("SCORES_PARTIALLY_DISCLOSED_TRACE_MISMATCH",
                                all_scored=all_scored, not_evaluated=ne, not_disclosed=not_disclosed,
                                model_version=resp.model_version, evidence_hash=resp.evidence_hash,
                                batch_shape={"forwarded": len(valid), "batch_count": trace.get("batch_count")})
        aggregated = aggregate_seed_scores(valid, per_seed, self.cfg.return_ci)
        # ORIGINAL (-score, uid) ordering from the wrapper aggregate; no re-sort
        all_scored = []
        for i, (uid, mean, ci) in enumerate(aggregated, start=1):
            all_scored.append(ScoredCandidate(uid=uid, sequence_sha256=sha_of.get(uid, ""),
                                              score=mean, rank=i,
                                              ensemble_ci=list(ci) if ci else None))
        k = min(self.cfg.top_k, len(all_scored))
        for i, c in enumerate(all_scored[:k], start=1):
            c.display_rank = i
        return ScoreOutcome("OK", all_scored=all_scored, not_evaluated=ne,
                            model_version=resp.model_version, evidence_hash=resp.evidence_hash,
                            batch_shape={"forwarded": len(valid), "batch_count": trace.get("batch_count"),
                                         "forward_executed": True})


class C2CacheReplayScoring:
    kind = "CACHE_REPLAY_c2_bound_rows"
    accepts_binding = True

    def __init__(self, cfg):
        self.cfg = cfg
        self._by_step = {}
        self._traces = {}
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
        t = Path(cfg.c2_export_dir or "") / "ENSEMBLE_PROBABILITY_TRACE.tsv.gz"
        if t.is_file() and cfg.replay_trace:
            with gzip.open(t, "rt", encoding="utf-8") as f:
                for r in csv.DictReader(f, delimiter="\t"):
                    if r["arm"] == cfg.replay_arm:
                        self._traces.setdefault(r["step_id"], {})[r["scientific_uid"]] = r

    def score(self, query_reaction: str, candidates, binding=None):
        if self._error:
            return ScoreOutcome(self._error, not_evaluated=[
                NotEvaluated(u, s, "CACHE_REPLAY_ASSET_MISSING") for u, s in candidates])
        if binding is None:
            binding = _Binding(arm=self.cfg.replay_arm,
                               step_id=self.cfg.replay_step_id,
                               model_key_sha256=self.cfg.replay_model_key_sha256)
        mismatch = replay_context_mismatch(self.cfg, binding, self._file)
        if mismatch:
            return ScoreOutcome(mismatch, not_evaluated=[
                NotEvaluated(u, s, "CACHE_REPLAY_BINDING_MISMATCH", mismatch)
                for u, s in candidates])
        step_id = binding.step_id
        if not step_id:
            hits = {sid for sid, rs in self._by_step.items() if rs and rs[0]["model_reaction"] == query_reaction}
            if len(hits) > 1:
                return ScoreOutcome(
                    f"CACHE_REPLAY_AMBIGUOUS_STEP:query matches {len(hits)} steps; step binding required; "
                    "first/last never guessed",
                    not_evaluated=[NotEvaluated(u, s, "CACHE_REPLAY_BINDING_REQUIRED") for u, s in candidates])
            if len(hits) == 0:
                return ScoreOutcome("CACHE_REPLAY_STEP_NOT_IN_FROZEN_EXPORT",
                                    not_evaluated=[NotEvaluated(u, s, "CACHE_REPLAY_STEP_NOT_IN_FROZEN_EXPORT")
                                                   for u, s in candidates])
            step_id = next(iter(hits))
        rows = self._by_step.get(step_id)
        if not rows:
            return ScoreOutcome("CACHE_REPLAY_STEP_NOT_IN_FROZEN_EXPORT",
                                not_evaluated=[NotEvaluated(u, s, "CACHE_REPLAY_STEP_NOT_IN_FROZEN_EXPORT")
                                               for u, s in candidates])
        r0 = rows[0]
        if r0["model_reaction"] != query_reaction:
            return ScoreOutcome("CACHE_REPLAY_BINDING_MISMATCH:query!=frozen model_reaction",
                                not_evaluated=[NotEvaluated(u, s, "CACHE_REPLAY_BINDING_MISMATCH")
                                               for u, s in candidates])
        if binding.model_key_sha256 and binding.model_key_sha256 != r0["model_key_sha256"]:
            return ScoreOutcome("CACHE_REPLAY_BINDING_MISMATCH:model_key_sha256",
                                not_evaluated=[NotEvaluated(u, s, "CACHE_REPLAY_BINDING_MISMATCH")
                                               for u, s in candidates])
        by_uid = {r["scientific_uid"]: r for r in rows}
        sha_of = dict(candidates)
        all_scored, ne = [], []
        for uid in sha_of:
            r = by_uid.get(uid)
            if r is None:
                ne.append(NotEvaluated(uid, sha_of[uid], "CACHE_REPLAY_UID_NOT_IN_BOUND_STEP",
                                       f"step={step_id} arm={self.cfg.replay_arm}"))
                continue
            row_sha = r.get("sequence_sha256", "")
            if not row_sha or not sha_of[uid] or row_sha != sha_of[uid]:
                ne.append(NotEvaluated(uid, sha_of[uid], "CACHE_REPLAY_SEQUENCE_SHA_MISMATCH",
                                       f"row_sha256={row_sha[:16]}.. declared={sha_of[uid][:16]}.."))
                continue
            ci = None
            tr = self._traces.get(step_id, {}).get(uid)
            if tr and self.cfg.return_ci:
                probs = sorted(float(tr[f"prob_seed{s}"]) for s in (40, 41, 42, 43, 44))
                ci = [_linear_quantile(probs, 0.025), _linear_quantile(probs, 0.975)]
            all_scored.append(ScoredCandidate(
                uid=uid, sequence_sha256=row_sha or sha_of[uid],
                score=float(r["ensemble_prob_float64"]), rank=int(r["rank"]),
                display_rank=int(r["rank"]) if int(r["rank"]) <= self.cfg.top_k else None,
                ensemble_ci=ci))
        all_scored.sort(key=lambda c: c.rank)
        bound_uids = set(by_uid)
        requested = set(sha_of)
        coverage = {"bound_step": step_id, "bound_model_key": r0["model_key_sha256"],
                    "bound_arm": self.cfg.replay_arm,
                    "source_file": self._file, "source_file_sha256": self._file_sha256,
                    "row_uids": len(bound_uids), "requested_uids": len(requested),
                    "set_equal": requested == bound_uids,
                    "extra_requested": sorted(requested - bound_uids),
                    "missing_requested": sorted(bound_uids - requested),
                    "ci_semantics": ("wrapper 2.5%/97.5% linear-interpolation quantiles recomputed from "
                                     "five cached per-seed probabilities (cache-derived, same rule as "
                                     "wrapper.utils.aggregate_seed_scores); NOT min/max")}
        return ScoreOutcome("OK_CACHE_REPLAY", all_scored=all_scored, not_evaluated=ne,
                            model_version=f"CACHE_REPLAY arm={self.cfg.replay_arm} step={step_id} "
                                          f"key={r0['model_key_sha256'][:16]}.. source={self._file}",
                            evidence_hash=r0["source_sha256"],
                            batch_shape={"forwarded": 0, "batch_count": 0, "forward_executed": False},
                            coverage=coverage)


class EnzymeCAGEWrapperNativeC95Backend(EnzymeCAGEWrapperBackend):
    """R4: wrapper scoring on the audited native C95 asset chain.

    Same score()/ordering/trace contract as the wrapper backend; only runtime
    construction differs (native_c95_assets.make_native_runtime). cfg.
    native_binding = {"paths": {...}, "ctx": "main"|"delta15"}.
    """
    kind = "enzyme_cage_wrapper_native_c95"

    def __init__(self, cfg, runtime_factory=None):
        super().__init__(cfg, runtime_factory=runtime_factory)
        if runtime_factory is None:
            from . import native_c95_assets as NC
            nb = dict((cfg.native_binding or {}).get("paths") or {})
            ctx = (cfg.native_binding or {}).get("ctx") or "main"
            def _factory():
                return NC.make_native_runtime(cfg, nb, ctx)
            self._runtime_factory = _factory

    def preflight(self):
        super().preflight()
        if self._preflight_error:
            return
        from . import native_c95_assets as NC
        try:
            NC.check_binding(dict((self.cfg.native_binding or {}).get("paths") or {}),
                             (self.cfg.native_binding or {}).get("ctx") or "main")
        except NC.NativeBindingError as exc:
            self._preflight_error = f"BACKEND_MISSING_DEPENDENCY:{exc}"


def make_scoring(cfg, runtime_factory=None, injected=None):
    if injected is not None:
        return injected
    if cfg.backend == "enzyme_cage_wrapper":
        return EnzymeCAGEWrapperBackend(cfg, runtime_factory=runtime_factory)
    if cfg.backend == "enzyme_cage_wrapper_native_c95":
        return EnzymeCAGEWrapperNativeC95Backend(cfg, runtime_factory=runtime_factory)
    if cfg.backend == "cache_replay_c2":
        return C2CacheReplayScoring(cfg)
    return None
