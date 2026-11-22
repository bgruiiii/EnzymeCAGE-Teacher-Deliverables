#!/usr/bin/env python3
"""C95AssetIndex: thin extension of the AUDITED enzymecage_wrapper
PrecomputedAssetIndex (source sha256 recorded in ADAPTED_SOURCES_MANIFEST; the
original file is NEVER modified — this wrapper delegates to it).

Extension semantics (prompt §5):
  * the original index builds UID->sequence ONLY from the old train/valid/test
    splits; current unseen UIDs are added from the ACCEPTED runtime map
    (RUNTIME_UID_TO_SEQUENCE, generated from the accepted R1 runtime input +
    FINAL_SEQUENCE_MAP, sha-recomputed per row)
  * a UID present in BOTH old splits and the runtime map with DIFFERENT
    sequence -> typed C95IndexConflict listing every conflicting UID (the pool
    is never smuggled in as training data, and old mappings are never silently
    overwritten)
  * a UID whose old mapping was AMBIGUOUS but the runtime map provides one
    exact sequence becomes resolvable (recorded, count exposed)
  * has_enzyme/sequence_for reproduce the original predicate EXACTLY
    (uid->seq known, not ambiguous, uid in gvp, uid in pocket_node, sequence
    in sequence_esm) evaluated on the extended mapping and the merged stores
    held by the inner index (merged by c95_asset_union.py; same SHA/UID/recipe)
  * everything else (missing_assets/_molecules/rxn_fp/molecule stores/reaction
    centers/inventory) delegates untouched; inventory() gains extension counts
"""
import csv
import gzip
import hashlib
import os

sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()


class C95IndexConflict(Exception):
    def __init__(self, conflicts):
        super().__init__(f"{len(conflicts)} UID(s) map to different sequences in old splits vs accepted runtime map")
        self.conflicts = conflicts


def load_runtime_map(path):
    """TSV(.gz): runtime_uid, sequence_sha256, sequence. Verifies sha per row;
    a uid bound to two different sequences is a typed conflict (R1 audit proved
    zero such cases; re-verified here at load)."""
    op = gzip.open if str(path).endswith(".gz") else open
    m, by_uid = {}, {}
    with op(path, "rt", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            uid, seq, sh = r["runtime_uid"], r["sequence"], r["sequence_sha256"]
            if sha_text(seq) != sh:
                raise ValueError(f"runtime map row sha mismatch for uid {uid}")
            if uid in by_uid and by_uid[uid] != seq:
                raise C95IndexConflict([{"uid": uid, "reason": "RUNTIME_MAP_INTERNAL_UID_TO_TWO_SEQUENCES"}])
            by_uid[uid] = seq
            m[uid] = seq
    return m


# ---- c95_asset_index_ext R2_1 fork (assemble_R2_1). The accepted original is
# preserved verbatim except edits E1-E3 (see c95_asset_index_ext.r2_1.diff and
# c95_asset_index_ext.accepted_original).
import json
import os
import numpy as np


class _RegistryOverlayView:
    """Overlay-first mapping over a base mapping with identity gating.

    An overlay body is exposed for a uid ONLY when the uid is present in the
    identity registry AND the body passes verification (shape/rows/finite)
    against the registered rows count. Unregistered or invalid files never
    override the base (no first-wins). Quarantined uids are absent."""

    def __init__(self, base, overlay_dir, registry, quarantine, kind):
        self.base = base
        self.overlay_dir = overlay_dir
        self.kind = kind
        self._reg = registry
        self._q = quarantine
        self._cache = {}
        self.typed_log = []

    def _overlay_path(self, uid):
        reg = self._reg.get(uid)
        if not reg or not os.path.isdir(self.overlay_dir):
            return None
        expected = reg.get("overlay_gvp_name") if self.kind == "gvp" else reg.get("pocket_name")
        if not expected:
            return None
        p = os.path.join(self.overlay_dir, expected)
        if os.path.basename(expected) != expected or not os.path.isfile(p):
            return None
        if self.kind == "pocket":
            if not expected == reg.get("seq_sha") + "__" + uid + ".npy":
                return None
        else:
            if not expected == reg.get("seq_sha", "")[:32] + "_" + uid + ".gvp.pt":
                return None
        want = reg.get("gvp_body_sha" if self.kind == "gvp" else "pocket_body_sha") or ""
        if want:
            import hashlib
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for blk in iter(lambda: f.read(1 << 22), b""): h.update(blk)
            if h.hexdigest() != want:
                self.typed_log.append({"uid": uid, "reason": "OVERLAY_BODY_SHA_DRIFT"})
                return None
        return p

    def _load(self, uid):
        if uid in self._cache:
            return self._cache[uid]
        val = None
        p = self._overlay_path(uid)
        if p and os.path.isfile(p):
            try:
                if self.kind == "pocket":
                    arr = np.load(p)
                    assert arr.dtype == np.float32 and arr.ndim == 2 and int(arr.shape[0]) == int(self._reg[uid]["rows"])                         and int(arr.shape[1]) == 2560 and np.isfinite(arr).all()
                    val = arr
                else:
                    import torch
                    v = torch.load(p, map_location="cpu", weights_only=False)
                    v = v[uid] if isinstance(v, dict) and uid in v else v
                    assert isinstance(v, (tuple, list)) and len(v) == 7
                    assert int(v[0].shape[0]) == int(self._reg[uid]["rows"])
                    assert all(torch.isfinite(t).all() for t in v)
                    val = tuple(v)
            except Exception as exc:
                self.typed_log.append({"uid": uid, "reason": "OVERLAY_BODY_INVALID_OR_UNREGISTERED",
                                       "error": type(exc).__name__})
                val = None
        self._cache[uid] = val
        return val

    def __contains__(self, uid):
        if uid in self._q:
            return False
        return self._load(uid) is not None or (uid in self.base)

    def __getitem__(self, uid):
        if uid in self._q:
            raise KeyError(uid)
        v = self._load(uid)
        if v is not None:
            return v
        return self.base[uid]

    def get(self, uid, default=None):
        try:
            return self[uid]
        except KeyError:
            return default



class C95AssetIndex:
    def __init__(self, inner, runtime_map_path):
        self._inner = inner
        self.runtime_map = load_runtime_map(runtime_map_path)
        old = dict(inner.uid_to_sequence)
        amb = set(inner.ambiguous_uids)
        conflicts = []
        for uid, seq in self.runtime_map.items():
            if uid in old and old[uid] != seq:
                conflicts.append({"uid": uid, "reason": "OLD_SPLIT_VS_RUNTIME_SEQUENCE_DIFFER"})
        if conflicts:
            raise C95IndexConflict(conflicts)
        # extended mapping: old unambiguous + runtime additions (incl. uids the
        # old splits found ambiguous but the runtime map resolves exactly)
        self.uid_to_sequence = dict(old)
        self.ambiguous_uids = frozenset(a for a in amb if a not in self.runtime_map)
        self.uid_to_sequence.update(self.runtime_map)
        self.extension_stats = {
            "runtime_map_uids": len(self.runtime_map),
            "added_new_uids": sum(1 for u in self.runtime_map if u not in old and u not in amb),
            "resolved_previously_ambiguous": sum(1 for u in self.runtime_map if u in amb),
            "same_sequence_overlap": sum(1 for u in self.runtime_map if u in old and old[u] == self.runtime_map[u]),
            "conflicts_typed": len(conflicts),
        }
        # R2_1 E2: env-configured registry-gated overlays + quarantine
        ctxp = os.environ.get("C95_R2_1_CONTEXT")
        self.r2_1_stats = {"enabled": False, "registry_n": 0, "quarantine_n": 0}
        self._r2_pocket_view = self._r2_gvp_view = None
        if ctxp:
            rc = json.load(open(ctxp))
            reg = json.load(open(rc["registry"])).get("entities", {}) if os.path.isfile(rc["registry"]) else {}
            qf = rc.get("quarantine")
            q = set(json.load(open(qf)).get("uids", [])) if qf and os.path.isfile(qf) else set()
            self.r2_1_stats.update({"enabled": True, "registry_n": len(reg), "quarantine_n": len(q)})
            self._r2_pocket_view = _RegistryOverlayView(inner.pocket_node, rc["pocket_overlay_dir"], reg, q, "pocket")
            self._r2_gvp_view = _RegistryOverlayView(inner.gvp, rc["gvp_overlay_dir"], reg, q, "gvp")

    # R2_1 E3: effective views (registered overlay first, base canonical)
    @property
    def gvp(self):
        return self._r2_gvp_view if self._r2_gvp_view is not None else self._inner.gvp

    @property
    def pocket_node(self):
        return self._r2_pocket_view if self._r2_pocket_view is not None else self._inner.pocket_node

    # original predicate evaluated on the EFFECTIVE chained state: same closure
    # math (rows == pocket rows <= len(sequence)); quarantined uids absent, so
    # the whole step is typed INCOMPLETE_POOL upstream; candidates never removed.
    def has_enzyme(self, uid):
        sequence = self.uid_to_sequence.get(uid)
        gvpv, pocketv = self.gvp, self.pocket_node
        present = bool(
            sequence
            and uid not in self.ambiguous_uids
            and uid in gvpv
            and uid in pocketv
            and sequence in self._inner.sequence_esm
        )
        if not present:
            return False
        try:
            n = int(gvpv[uid][0].shape[0])
            p = int(pocketv[uid].shape[0])
            return 0 < n == p <= len(sequence)
        except (AttributeError, IndexError, TypeError):
            return False

    def sequence_for(self, uid):
        if not self.has_enzyme(uid):
            raise KeyError(uid)
        return self.uid_to_sequence[uid]

    def has_reaction(self, reaction_smiles):
        return not self.missing_assets(reaction_smiles)

    def inventory(self):
        inv = self._inner.inventory()
        inv["c95_extension"] = dict(self.extension_stats)
        inv["c95_unambiguous_uid_count"] = len(self.uid_to_sequence)
        inv["c95_ambiguous_uid_count"] = len(self.ambiguous_uids)
        import hashlib as _h
        ident = {}
        for uid, reg in sorted((self._r2_pocket_view._reg if self._r2_pocket_view else {}).items()):
            ident[uid] = {k: reg.get(k, "") for k in ("seq_sha", "rows", "pdb_sha", "indices_sha",
                                                       "gvp_value_sha", "snapshot_sha", "pocket_source", "layer", "recipe", "weight_sha")}
        inv["r2_1"] = dict(self.r2_1_stats,
                           identities_sha256=_h.sha256(json.dumps(ident, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                           identities=ident,
                           pocket_typed=list(self._r2_pocket_view.typed_log) if self._r2_pocket_view else [],
                           gvp_typed=list(self._r2_gvp_view.typed_log) if self._r2_gvp_view else [])
        return inv

    def missing_assets(self, reaction_smiles):
        missing = list(self._inner.missing_assets(reaction_smiles))
        center = self._inner.reaction_centers.get(reaction_smiles)
        if not isinstance(center, (tuple, list)) or len(center) != 2:
            missing.append("reacting-center exact key")
        elif len(center[0]) == 0 or len(center[1]) == 0:
            missing.append("reacting-center typed empty side")
        return missing

    def __getattr__(self, name):
        # pass-through for gvp / pocket_node / sequence_esm / rxn_fp /
        # molecule_index / molecule_graphs / reaction_centers / config ...
        return getattr(self._inner, name)
