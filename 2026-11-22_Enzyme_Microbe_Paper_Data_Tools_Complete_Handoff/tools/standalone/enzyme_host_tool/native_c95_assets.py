"""Native CURRENT95 asset binding for the standalone tool (R4).

Thin IN-PROCESS composition only. It builds the exact audited C95 asset-index
chain that `r3_gf_unified.py::bind_ctx` registers for the legacy_esm2_3b lane
(`recovery_helpers.build_3b_index(paths, ctx, merged_cfg,
PrecomputedAssetIndex, C95AssetIndex)`), and injects it as the wrapper
runtime's asset_index. Files on disk are never modified:

  * wrapper package files (predictor.py b9877649.. reviewed 2026-11-21) are the
    SAME bytes; only the in-process symbol `PrecomputedAssetIndex` is rebound
    for the duration of `_Runtime.__init__`, then restored;
  * scoring, ordering and trace semantics stay in wrapper.predictor /
    wrapper.utils.aggregate_seed_scores: per-seed PROBABILITIES from
    model.evaluate(), averaged ONCE — no second sigmoid anywhere;
  * candidates are never dropped or reordered: frozen pool order is passed
    through; typed ENZYME_ASSET_MISSING / reaction-missing disclosures are
    preserved per UID.

Import-safe without torch: heavy modules load only inside the functions,
on the node.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(8 << 20), b""):
            h.update(blk)
    return h.hexdigest()


class NativeBindingError(RuntimeError):
    pass


def check_binding(nb: dict, ctx: str) -> dict:
    """CPU-only preflight: every registered path exists and module SHAs match
    the ledger. Raises typed errors; never falls back to a guessed path."""
    problems = []
    keys = ("pkg", "a109", "wrap_pkg_root", "rh_dir", "enzymecage_source_root")
    for k in keys:
        p = nb.get(k, "")
        if not p or not Path(p).is_dir():
            problems.append(f"NATIVE_PATH_MISSING:{k}:{p}")
    mc = (nb.get("merged_cfg") or {}).get(ctx, "")
    if not mc or not Path(mc).is_file():
        problems.append(f"NATIVE_MERGED_CFG_MISSING:{ctx}:{mc}")
    rm = f"{nb.get('pkg','')}/inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv"
    if not Path(rm).is_file():
        problems.append(f"NATIVE_RUNTIME_MAP_MISSING:{rm}")
    for label, spec in (nb.get("module_shas") or {}).items():
        p, want = spec.get("path", ""), spec.get("sha256", "")
        if not p or not Path(p).is_file():
            problems.append(f"NATIVE_MODULE_MISSING:{label}:{p}")
        elif want and sha_file(p) != want:
            problems.append(f"NATIVE_MODULE_SHA_DRIFT:{label}")
    if problems:
        raise NativeBindingError("; ".join(problems))
    return {"runtime_map": rm, "merged_cfg": mc}


def build_native_c95_index(nb: dict, ctx: str):
    """Exactly the r3 bind_ctx construction for legacy_esm2_3b."""
    check_binding(nb, ctx)
    sys.path.insert(0, nb["wrap_pkg_root"])      # provides enzymecage_wrapper
    sys.path.insert(0, nb.get("c95_dir") or nb["a109"])  # provides c95_asset_index_ext
    sys.path.insert(0, nb["rh_dir"])             # provides recovery_helpers
    if nb.get("enzymecage_source_root") and nb["enzymecage_source_root"] not in sys.path:
        sys.path.insert(0, nb["enzymecage_source_root"])  # enzymecage package (base imports it)
    import yaml                                   # noqa: deferred (node only)
    import recovery_helpers as RH
    from c95_asset_index_ext import C95AssetIndex
    from enzymecage_wrapper.asset_index import PrecomputedAssetIndex

    class _Paths:
        A109 = nb["a109"]
        PKG = nb["pkg"]

    merged = yaml.safe_load(open(nb["merged_cfg"][ctx], encoding="utf-8"))
    idx = RH.build_3b_index(_Paths(), ctx, merged, PrecomputedAssetIndex, C95AssetIndex)
    return idx


class _ViewWithValues:
    """Read-only accessor shim: exposes the .values() probe used by the live
    wrapper `_dataset` (esm_dim = next(iter(pocket_node.values())).shape[1]).
    Underlying bodies come from the audited overlay view UNCHANGED (overlay
    first, base canonical); no data is fabricated."""
    def __init__(self, view):
        object.__setattr__(self, "_v", view)
    def values(self):
        v = self._v
        keys = []
        base = getattr(v, "base", None)
        if base is not None:
            try:
                keys = list(base.keys())[:1]
            except AttributeError:
                keys = []
        if not keys:
            keys = list(getattr(v, "_reg", {}) or {})[:1]
        return iter([v[k] for k in keys])
    def __getitem__(self, u):
        return self._v[u]
    def __contains__(self, u):
        return u in self._v
    def __len__(self):
        return len(self._v)
    def __iter__(self):
        return iter(self._v)
    def __getattr__(self, n):
        return getattr(object.__getattribute__(self, "_v"), n)


class _IndexWithValues:
    """Proxy of the audited C95 index exposing .values() on the store views
    consumed by the live wrapper's dataset builder. All predicates delegate to
    the original index object; nothing is copied or rewritten."""
    def __init__(self, idx):
        object.__setattr__(self, "_idx", idx)
    @property
    def pocket_node(self):
        return _ViewWithValues(self._idx.pocket_node)
    @property
    def gvp(self):
        return _ViewWithValues(self._idx.gvp)
    def __getattr__(self, n):
        return getattr(object.__getattribute__(self, "_idx"), n)


def make_native_runtime(scoring_cfg, ledger_nb: dict, ctx: str, prebuilt_idx=None):
    """Wrapper runtime with the native C95 index injected.

    Reuses wrapper.predictor._Runtime UNCHANGED (arch gate over the five seed
    configs, single-visible-device check, strict checkpoint load, predict/
    _dataset/trace). The only seam: the class symbol used inside __init__ for
    the asset index is bound to a factory returning the merged-store C95
    chain; the real wrapper module is not edited and the patch is restored.
    """
    nb = dict(ledger_nb)
    nb.setdefault("pkg", None)
    for p in (scoring_cfg.wrapper_code_root, scoring_cfg.enzymecage_source_root):
        if p and p not in sys.path:
            sys.path.insert(0, p)
    from wrapper import predictor as wp
    idx = prebuilt_idx if prebuilt_idx is not None else build_native_c95_index(nb, ctx)
    orig = wp.PrecomputedAssetIndex
    wp.PrecomputedAssetIndex = lambda _cfg: idx
    try:
        rt = wp._Runtime(Path(scoring_cfg.weights_package_root))
    finally:
        wp.PrecomputedAssetIndex = orig
    if rt.asset_index is not idx:
        raise NativeBindingError("NATIVE_INJECTION_LOST: runtime kept a different asset_index")
    rt.asset_index = _IndexWithValues(idx)
    return rt
