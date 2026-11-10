#!/usr/bin/env python3
"""C95 joint old-cache inventory + task-local merged-store materialization.
R1 v2 (2026-10-30) — repairs audit defects A and C of
CURRENT95_AUDITED_REUSE_PREP_AUDIT_20261030:

A. `--materialize` is REAL: it produces task-local demanded-subset merged
   stores for all three protein families PLUS the reaction views (DRFP /
   reacting-center / merged mol2id+SDF+graph-cache) and a loadable GF config
   derived from the accepted P291 template by line-level key substitution.
   Values are copied byte-for-byte (never recomputed); old stores read-only.
   Merge acceptance per prompt §1: same sequence identity / declared pocket
   index-source recipe / dimension / finite; source value conflicts are typed
   SOURCE_CONFLICT (never silently overwritten). Metadata (formal sequence
   manifest) proves IDENTITY only — an entity hit still requires a value
   source; manifest-only hits are typed FOUND_IDENTITY_ONLY_* and stay gaps
   (reason ENTITY_MISSING_DESPITE_METADATA).

C. GVP overlay names are `<sha first 32 hex>_<uid>.gvp.pt` in BOTH recovered
   producer lanes (s5_lane_gvp.py:55, r3_lane_deltas gvp). UIDs may contain
   underscores, so parsing is regex-based (32-hex prefix + FULL remainder)
   and every name is verified against the accepted runtime map (full
   SHA256 + UID); unverifiable names are typed notes, never counted as
   assets. Wrapper-sharded torch stores (`__format__`+`manifest_path`) are
   enumerated through the manifest WITHOUT tensor reads, and entity-ready
   additionally requires the referenced shard file to exist;
   `__format__`/`manifest_path` are never treated as asset keys.

Inventory membership resolution stays as light as the source allows:
  overlay_dir : filename enumeration only — ZERO tensor reads
  manifest_csv: column read (IDENTITY role only)
  monolithic_pickle / torch_map: ONE keys load per source, cached to
                <out>/keycache/<name>.keys.json keyed by source file sha;
                torch_map prefers torch.load and falls back to pickle (the
                GU_UNION_ASSEMBLY load_map pattern); without torch a
                torch-zip file is typed NEEDS_TORCH.

Merged store format is chosen PER REAL CONSUMER (R1.1, audit §1):
  global  = ALWAYS plain highest-protocol pickle — the audited old
            PrecomputedAssetIndex reads esm_mean_feature through a fixed
            pickle.load (recovered wrapper asset_index.py:17-18) with no torch
            fallback; a torch archive there fails on the node.
  pocket  = GU pattern torch.save on node, pickle locally; consumer
            load_pocket_node_feature_data -> _torch_load_trusted accepts both.
  gvp     = same as pocket via load_protein_gvp_data/_torch_load_trusted.
Format + SHA per family are recorded in MERGE_MANIFEST provenance
(CONFIG_PROVENANCE.store_formats), and every run rewrites all three GAP_LIST
files deterministically (zero gaps = header + 0 rows) so stale per-family
work lists can never be re-consumed as "missing".

Exit codes: 0 ok; 4 typed source/merge problems; 5 config error.
"""
import argparse
import csv
import glob
import gzip
import hashlib
import json
import os
import pickle
import re
import shutil
import sys
from datetime import datetime, timezone

sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def canon(t):
    return "".join(str(t).upper().split())


EXIT_OK, EXIT_TYPED, EXIT_CONFIG = 0, 4, 5
METADATA_KEYS = {"__format__", "manifest_path"}
GVP_FN_RE = re.compile(r"^([0-9a-f]{32})_(.+)\.gvp\.pt$")


class TypedSource(Exception):
    def __init__(self, msg, code):
        super().__init__(msg)
        self.code = code
        self.detail = msg


def read_tsv(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def load_map(path):
    """GU_UNION_ASSEMBLY load_map pattern: torch.load with pickle fallback."""
    try:
        import torch
        try:
            return torch.load(path, map_location="cpu", weights_only=False)
        except TypeError:
            return torch.load(path, map_location="cpu")
    except ImportError:
        pass
    except Exception:
        pass
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        import zipfile
        if zipfile.is_zipfile(path):
            raise TypedSource(f"torch-zip store unreadable without torch: {path}", "NEEDS_TORCH")
        raise TypedSource(f"cannot load mapping {path}: {type(e).__name__}: {e}", "VALUE_LOAD_ERROR")


def value_bytes_sha(v):
    # Stable content identity for the real seven-tensor GVP tuple, arrays and
    # scalar/list reaction values. Never hash pickle storage IDs/object pointers.
    import numpy as np
    h = hashlib.sha256()
    def feed(x):
        if hasattr(x, "detach") and hasattr(x, "cpu"):
            x = x.detach().cpu().numpy()
        if isinstance(x, (tuple, list)):
            h.update((type(x).__name__ + ":" + str(len(x))).encode())
            for item in x:
                feed(item)
        elif isinstance(x, dict):
            h.update(b"dict")
            for key in sorted(x):
                feed(key); feed(x[key])
        elif isinstance(x, (str, int, float, bool)) or x is None:
            h.update(json.dumps([type(x).__name__, x], allow_nan=False).encode())
        else:
            arr = np.asarray(x)
            if arr.dtype.hasobject:
                raise TypeError("UNSUPPORTED_NON_NUMERIC_ASSET_VALUE")
            h.update(json.dumps([arr.dtype.str, list(arr.shape)]).encode())
            h.update(np.ascontiguousarray(arr).tobytes())
    feed(v)
    return h.hexdigest()


# --- RECOVERY PATCH merge_conflict_numeric_adjudication_20261031 -------------
# (authorized minimal task-copy patch; see execution/RECOVERY_LOG.jsonl and
# execution/patches/PRE_PATCH_SHA256.txt for the pre-patch originals)
# Byte-SHA inequality between independently extracted copies of the SAME
# declared recipe can be pure cross-node GPU nondeterminism at the float32 ULP
# level (audited precedent: p298-dual REPAIR_LEDGER.tsv 2026-09-21T18:05Z
# "equivalence_criterion_bit_exact_too_strict ... bit-equality is unachievable
# in this stack without algorithm pinning"). Such pseudo-conflicts are
# adjudicated NUMERICALLY at the task-declared pc gate (2e-4 = s5_lane_plm_c95
# --max-delta default). Equivalent-within-gate: the priority winner is copied
# byte-for-byte (never recomputed) with a typed disclosure recording every
# source byte-sha and the measured float64 max abs diff. Beyond the gate (e.g.
# different pocket definitions between an old delta overlay and the formal
# store): SOURCE_CONFLICT stands and NOTHING is written — never silently
# overwritten, exactly as before the patch.
MERGE_NUMERIC_TOL = 2e-4

# RECOVERY PATCH accepted_graph_cache_union_20261031 — registered accepted
# historical molecule-graph caches, consulted (in order, first source wins)
# ONLY for molecules the template formal view's cache lacks; values are
# existing accepted objects, never recomputed. See extend_mol_graph_cache.
ACCEPTED_GRAPH_CACHE_EXTRA = (
    "/usrdata/EnzymeCAGE_data/workspaces/biosysmodb121_pre_ranking_r1_r1_reaction_asset_gold_ordering_portable_reseal_20261009/S2_graph_loader/merged_bundle/molecule_conformation/mol_graph_dict.pt",
    "/usrdata/EnzymeCAGE_data/feature/reaction/molecule_conformation_round1_full_20260707/mol_graph_dict.pt",
)


def values_numerically_equivalent(vals, tol=MERGE_NUMERIC_TOL):
    """(equivalent, max_abs_diff) using the same structural traversal rules as
    value_bytes_sha: tuples/lists/dicts must match structurally, non-numeric
    leaves must be equal, numeric leaves are compared in float64 within tol."""
    import numpy as np
    maxd = [0.0]

    def walk(a, b):
        if hasattr(a, "detach") and hasattr(a, "cpu"):
            a = a.detach().cpu().numpy()
        if hasattr(b, "detach") and hasattr(b, "cpu"):
            b = b.detach().cpu().numpy()
        if isinstance(a, (tuple, list)) or isinstance(b, (tuple, list)):
            if type(a) is not type(b) or len(a) != len(b):
                return False
            for x, y in zip(a, b):
                if not walk(x, y):
                    return False
            return True
        if isinstance(a, dict) or isinstance(b, dict):
            if not isinstance(a, dict) or not isinstance(b, dict) or sorted(a) != sorted(b):
                return False
            for k in sorted(a):
                if not walk(a[k], b[k]):
                    return False
            return True
        if isinstance(a, (str, bool)) or isinstance(b, (str, bool)) or a is None or b is None:
            return type(a) is type(b) and a == b
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            dd = abs(float(a) - float(b))
            maxd[0] = max(maxd[0], dd)
            return dd <= tol
        aa = np.asarray(a, dtype=np.float64)
        bb = np.asarray(b, dtype=np.float64)
        if aa.shape != bb.shape:
            return False
        if aa.size and not (np.isfinite(aa).all() and np.isfinite(bb).all()):
            return False
        dd = float(np.abs(aa - bb).max()) if aa.size else 0.0
        maxd[0] = max(maxd[0], dd)
        return dd <= tol

    ok = all(walk(vals[0], v) for v in vals[1:])
    return ok, maxd[0]
# --- END RECOVERY PATCH ------------------------------------------------------


def value_shape(v):
    import numpy as np
    try:
        a = np.asarray(v)
        return "x".join(map(str, a.shape)) if a.shape else "scalar"
    except Exception:
        if isinstance(v, (list, tuple)):
            return f"seq[{len(v)}]"
        return type(v).__name__


# --------------------------------------------------------------------------
# overlay filename enumeration (defect C fix)
# --------------------------------------------------------------------------

def parse_gvp_filename(fn, uid2sha=None):
    """Returns ((sha32, uid), status) or (None, typed_status).

    uid keeps ALL underscores (regex remainder). Verification uses the full
    SHA256 from the accepted runtime map: sha32 must equal full[:32] and the
    uid must be a registered runtime uid. Prefix conflicts (uid registered
    under a different full sha) are typed, never guessed.
    """
    m = GVP_FN_RE.match(fn)
    if not m:
        if fn.endswith(".gvp.pt"):
            return None, "UNPARSED_GVP_FILENAME"
        if fn.endswith(".pt"):
            bare = fn[:-3]
            if uid2sha is not None and bare in uid2sha:
                return (None, bare), "BARE_UID_NAME_VERIFIED"
            return None, "BARE_UID_NAME_UNVERIFIED"
        return None, "UNPARSED_GVP_FILENAME"
    sha32, uid = m.group(1), m.group(2)
    if uid2sha is None:
        return (sha32, uid), "PREFIX_PARSE_UNVERIFIED_NO_RUNTIME_MAP"
    full = uid2sha.get(uid)
    if full is None:
        return None, "GVP_UID_NOT_IN_RUNTIME_MAP"
    if full[:32] != sha32:
        return None, "GVP_SHA32_PREFIX_MISMATCH"
    return (sha32, uid), "VERIFIED_FULL_SHA_AND_UID"


def overlay_keys(dirpath, family, uid2sha=None):
    """Filename-only enumeration per recovered lane output naming.

    Returns (keys, file_index, notes):
      keys      — membership set: global: sha; pocket: uid (+ ("sha",sha));
                  gvp: VERIFIED uid only (+ ("sha32",sha32) pair records)
      file_index— key -> filename for later value extraction (zero reads here)
      notes     — typed per-filename statuses (unparsed/unverified/mismatch)
    """
    keys, file_index, notes = set(), {}, []
    if not os.path.isdir(dirpath):
        return None, None, None
    for fn in sorted(os.listdir(dirpath)):
        if family == "global" and fn.endswith(".npy"):
            keys.add(fn[:-4])
            file_index[fn[:-4]] = fn
        elif family == "pocket" and fn.endswith(".npy") and "__" in fn:
            sha, uid = fn[:-4].split("__", 1)
            keys.add(uid)
            keys.add(("sha", sha))
            file_index[uid] = fn
        elif family == "gvp" and fn.endswith(".pt"):
            parsed, status = parse_gvp_filename(fn, uid2sha)
            if parsed is None:
                notes.append({"file": fn, "status": status})
                continue
            sha32, uid = parsed
            keys.add(uid)
            if sha32:
                keys.add(("sha32", sha32))
            file_index[uid] = fn
            if status != "VERIFIED_FULL_SHA_AND_UID":
                notes.append({"file": fn, "status": status})
    return keys, file_index, notes


# --------------------------------------------------------------------------
# store key enumeration (identity vs entity; sharded wrapper support)
# --------------------------------------------------------------------------

class SourceData:
    """Lazily loaded source with cached keys + value access."""

    def __init__(self, spec, out_dir, uid2sha):
        self.spec = spec
        self.name = spec["name"]
        self.kind = spec["kind"]
        self.path = spec["path"]
        self.role = "identity" if self.kind == "manifest_csv" else spec.get("role", "value")
        self.recipe = spec.get("recipe", "")
        self.index_source = spec.get("index_source", "")
        self.out_dir = out_dir
        self.uid2sha = uid2sha
        self._data = None
        self._file_index = None
        self._keys = None
        self._manifest = None  # sharded wrapper: (uid_to_shard, shard_dir)
        self._cached_shard_name = None
        self._cached_shard_data = None
        self.io_note = ""
        self.enum_notes = []

    # -- keys (light) -------------------------------------------------------
    def keys(self):
        if self._keys is not None:
            return self._keys
        if self.kind == "overlay_dir":
            ks, fi, notes = overlay_keys(self.path, self.spec["family"], self.uid2sha)
            self._file_index = fi
            self._keys = ks
            self.io_note = "OVERLAY_FILENAME_ENUMERATION_ZERO_TENSOR_READ"
            self.enum_notes = notes or []
        elif self.kind == "manifest_csv":
            ks = set()
            with open(self.path, newline="") as f:
                for r in csv.DictReader(f):
                    col = r.get(self.spec["column"])
                    if col:
                        ks.add(col)
            self._keys = ks
            self.io_note = "MANIFEST_CSV_COLUMN_READ_IDENTITY_ONLY"
        else:
            self._keys, self.io_note = self._store_keys_cached()
        return self._keys

    def _store_keys_cached(self):
        os.makedirs(os.path.join(self.out_dir, "keycache"), exist_ok=True)
        cache = os.path.join(self.out_dir, "keycache", f"{self.name}.keys.json")
        fsha = sha_file(self.path)
        data = load_map(self.path)
        if isinstance(data, dict) and data.get("__format__") and "manifest_path" in data:
            mp = data["manifest_path"]
            if not os.path.isabs(mp):
                mp = os.path.join(os.path.dirname(self.path), mp)
            try:
                with open(mp) as f:
                    man = json.load(f)
            except Exception as e:
                raise TypedSource(f"sharded wrapper manifest unreadable: {mp}: {type(e).__name__}: {e}",
                                  "MANIFEST_UNREADABLE")
            self._manifest = (man["uid_to_shard"], os.path.join(os.path.dirname(mp), man["shard_dir"]))
            keys = set(man["uid_to_shard"].keys())
            io_note = f"SHARDED_WRAPPER_MANIFEST_ENUMERATION format={data.get('__format__')}"
        else:
            if self._data is None:
                self._data = data
            keys = {k for k in data.keys() if k not in METADATA_KEYS}
            io_note = "MONOLITHIC_KEYS_ONCE" if self.kind == "monolithic_pickle" else "TORCH_MAP_KEYS_ONCE"
        if os.path.isfile(cache):
            c = json.load(open(cache))
            if c.get("source_sha256") == fsha and set(c["keys"]) == keys:
                return keys, io_note + "+KEYCACHE_CONFIRMED"
        json.dump({"source_sha256": fsha, "keys": sorted(map(str, keys))}, open(cache, "w"))
        return keys, io_note

    # -- entity presence (metadata hit != entity ready) ---------------------
    def entity_present(self, key):
        """For sharded wrappers: the referenced shard file must exist."""
        if self._manifest is None:
            return True
        uid_to_shard, shard_dir = self._manifest
        sn = uid_to_shard.get(key)
        return sn is not None and os.path.isfile(os.path.join(shard_dir, sn))

    # -- value access -------------------------------------------------------
    def data(self):
        if self._data is None:
            self._data = {} if self._manifest is not None else load_map(self.path)
        return self._data

    def get_value(self, family, key, seq=None):
        """Returns (value, key_form) or raises TypedSource. key is sha (global)
        or uid (pocket/gvp); seq is the exact sequence text (global consumer
        key). key_form records EXACT vs CANON vs OVERLAY hits (value-invariant;
        normalization documented in the manifest)."""
        if self.kind == "overlay_dir":
            fn = (self._file_index or {}).get(key)
            if fn is None:
                raise TypedSource(f"{self.name}: no overlay file for {key}", "VALUE_MISSING")
            import numpy as np
            if family == "gvp":
                obj = load_map(os.path.join(self.path, fn))
                if isinstance(obj, dict):
                    clean = {k: v for k, v in obj.items() if k not in METADATA_KEYS}
                    if key in clean:
                        return clean[key], "OVERLAY_GVP_UID_KEYED"
                    if len(clean) == 1:
                        return next(iter(clean.values())), "OVERLAY_GVP_SINGLE_ENTRY"
                    raise TypedSource(f"{self.name}/{fn}: uid {key} not among {sorted(clean)[:3]}",
                                      "VALUE_KEY_MISMATCH")
                return obj, "OVERLAY_GVP_RAW"
            return np.load(os.path.join(self.path, fn)), "OVERLAY_NPY"
        if self._manifest is not None:
            uid_to_shard, shard_dir = self._manifest
            sn = uid_to_shard[key]
            if self._cached_shard_name != sn:
                self._cached_shard_data = load_map(os.path.join(shard_dir, sn))
                self._cached_shard_name = sn
            sd = self._cached_shard_data
            if key not in sd:
                raise TypedSource(f"{self.name}: shard {sn} lacks {key}", "VALUE_KEY_MISMATCH")
            return sd[key], "SHARDED_WRAPPER"
        d = self.data()
        if family == "global":
            if seq is None:
                raise TypedSource("global value needs sequence text", "CONFIG")
            if seq in d:
                return d[seq], "EXACT_SEQUENCE"
            c = canon(seq)
            if c in d:
                return d[c], "CANON_SEQUENCE"
            if key == sha_text(seq) and key in d:
                return d[key], "SHA_NATIVE_BRIDGED_FROM_EXACT_SEQUENCE"
            raise TypedSource(f"{self.name}: sequence not in store", "VALUE_MISSING")
        if key in d:
            return d[key], "EXACT_KEY"
        raise TypedSource(f"{self.name}: {key} not in store", "VALUE_MISSING")


# --------------------------------------------------------------------------
# inventory
# --------------------------------------------------------------------------

def build_uid2sha(runtime_map_path):
    uid2sha = {}
    for r in read_tsv(runtime_map_path):
        uid2sha[r["runtime_uid"]] = r["sequence_sha256"]
    return uid2sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--context", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seq-map", required=True, help="FINAL_SEQUENCE_MAP.tsv.gz (sha->sequence resolution)")
    ap.add_argument("--runtime-map", default=None,
                    help="runtime_uid_to_sequence.tsv (REQUIRED for --materialize and GVP name verification)")
    ap.add_argument("--materialize", action="store_true")
    ap.add_argument("--gf-config-template", default=None,
                    help="accepted P291 3B config.yaml (materialize derives the merged GF config from it)")
    ap.add_argument("--step-table", default=None, help="c95_step_table.json (reaction demands for materialize)")
    ap.add_argument("--new-reaction-bundles", default=None,
                    help="root with RXASSET_<key>/ bundle dirs from the N3 chain (optional)")
    ap.add_argument("--reused-reaction-bundles", action="append", default=[],
                    help="accepted historical RXASSET bundle root (repeatable, read-only)")
    ap.add_argument("--repo-root", default=None,
                    help="deployed EnzymeCAGE-master (frozen mol-graph functions for cache extension)")
    ap.add_argument("--pair-adjudications", action="append", default=[],
                    help="R3-A/R3-D: verified same-lane/same-structure pairing whitelist JSON "
                         "(repeatable; evidence-based; unlisted keys keep old behavior)")
    a = ap.parse_args()
    ctx = json.load(open(a.context))
    os.makedirs(a.out, exist_ok=True)
    demands = json.load(open(ctx["demands"]))
    seqmap = {}
    with gzip.open(a.seq_map, "rt", newline="") if a.seq_map.endswith(".gz") else open(a.seq_map, newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r.get("resolution_state", "RESOLVED").startswith("RESOLVED"):
                seqmap[r["sequence_sha256"]] = r["sequence"]
    demands["global"]["seqs"] = [seqmap[s] for s in demands["global"]["shas"]]
    uid2sha = build_uid2sha(a.runtime_map) if a.runtime_map else None
    if a.materialize:
        missing = [why for req, why in ((a.runtime_map, "--runtime-map"),
                                        (a.gf_config_template, "--gf-config-template"),
                                        (a.step_table, "--step-table")) if not req]
        if missing:
            print(f"CONFIG_ERROR: {missing} required for --materialize", file=sys.stderr)
            return EXIT_CONFIG

    inv_rows, gaps, notes = [], {}, []
    exit_code = EXIT_OK
    fam_sources = {}
    for family in ("global", "pocket", "gvp"):
        fam_ctx = ctx["families"][family]
        sources = []
        for s in fam_ctx["sources"]:  # priority order
            s = dict(s, family=family)
            if not os.path.exists(s["path"]):
                notes.append({"family": family, "source": s["name"], "status": "SKIP_SOURCE_PATH_ABSENT",
                              "path": s["path"]})
                continue
            sd = SourceData(s, a.out, uid2sha)
            try:
                sd.keys()
                sources.append(sd)
                for n in sd.enum_notes:
                    notes.append({"family": family, "source": s["name"], **n})
            except TypedSource as e:
                notes.append({"family": family, "source": s["name"], "status": e.code, "detail": str(e)})
                exit_code = EXIT_TYPED
        fam_sources[family] = sources
        recipes = {sd.recipe for sd in sources if sd.role == "value" and sd.recipe}
        if len(recipes) > 1:
            notes.append({"family": family, "status": "RECIPE_CONFLICT_ACROSS_SOURCES", "recipes": sorted(recipes)})
            exit_code = EXIT_TYPED
        if not sources:
            notes.append({"family": family, "status": "PATH_VERIFY_REQUIRED_GAPS_UNDECIDED"})
            exit_code = EXIT_TYPED
            continue
        if family == "global":
            for sha_, seq in zip(demands[family]["shas"], demands[family]["seqs"]):
                hit, ident = None, None
                for sd in sources:
                    ks = sd.keys()
                    if family == "global" and (sha_ in ks or seq in ks or canon(seq) in ks):
                        if sd.role == "identity":
                            ident = ident or sd.name
                        else:
                            hit = hit or sd.name
                if hit:
                    status = f"FOUND_{hit}"
                elif ident:
                    status = f"FOUND_IDENTITY_ONLY_{ident}"
                else:
                    status = "MISSING_TRUE"
                inv_rows.append({"family": family, "key_sha256": sha_, "runtime_key": "seq:" + sha_[:12],
                                 "status": status})
                if not hit:
                    gaps.setdefault(family, []).append({
                        "sequence_sha256": sha_, "sequence": seq,
                        "reason": "ENTITY_MISSING_DESPITE_METADATA" if ident else "TRUE_GAP"})
        else:
            for u in demands[family]["uids"]:
                hit, ident, meta_only = None, None, None
                sha_of_u = (uid2sha or {}).get(u, "")
                for sd in sources:
                    ks = sd.keys()
                    if u in ks or (sha_of_u and ("sha", sha_of_u) in ks):
                        if sd.role == "identity":
                            ident = ident or sd.name
                        elif sd.entity_present(u):
                            hit = hit or sd.name
                        else:
                            meta_only = meta_only or sd.name
                if hit:
                    status = f"FOUND_{hit}"
                elif meta_only:
                    status = f"METADATA_ONLY_ENTITY_MISSING_{meta_only}"
                elif ident:
                    status = f"FOUND_IDENTITY_ONLY_{ident}"
                else:
                    status = "MISSING_TRUE"
                inv_rows.append({"family": family, "key_sha256": sha_of_u or u, "runtime_key": "uid:" + u,
                                 "status": status})
                if not hit:
                    reason = ("SHARD_ENTITY_MISSING" if meta_only else
                              "ENTITY_MISSING_DESPITE_METADATA" if ident else "TRUE_GAP")
                    gaps.setdefault(family, []).append({
                        "runtime_uid": u, "sequence_sha256": sha_of_u, "reason": reason})
    with open(os.path.join(a.out, "UNION_INVENTORY.tsv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["family", "key_sha256", "runtime_key", "status"],
                           delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(inv_rows)
    gap_cols = {"global": ["sequence_sha256", "sequence", "reason"],
                "pocket": ["runtime_uid", "sequence_sha256", "reason"],
                "gvp": ["runtime_uid", "sequence_sha256", "reason"]}
    # R1.1 (audit §3): EVERY run rewrites all three GAP_LISTs deterministically —
    # zero gaps = correct header + 0 data rows. Conditional writing left the
    # previous round's stale missing items behind, and a later refresh reading
    # those files would rebuild already-covered assets ("有文件" was mistaken
    # for progress). Downstream truth = demand-set membership, not file presence.
    for family in ("global", "pocket", "gvp"):
        with open(os.path.join(a.out, f"GAP_LIST_{family}.tsv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=gap_cols[family], delimiter="\t", lineterminator="\n",
                               extrasaction="ignore")
            w.writeheader()
            w.writerows(gaps.get(family, []))
    counts = {}
    for r in inv_rows:
        found_value = r["status"].startswith("FOUND_") and "IDENTITY_ONLY" not in r["status"]
        ck = r["family"] + "|" + ("FOUND" if found_value else r["status"])
        counts[ck] = counts.get(ck, 0) + 1
    summary = {"utc": datetime.now(timezone.utc).isoformat(), "counts": dict(sorted(counts.items())),
               "gap_families": {k: len(v) for k, v in gaps.items()},
               "gap_reasons": {f: {r: sum(1 for i in v2 if i["reason"] == r)
                                   for r in sorted({i["reason"] for i in v2})}
                               for f, v2 in gaps.items()},
               "source_notes": notes, "exit_code": exit_code,
               "io_honesty": ("overlay=filename-only; manifest=IDENTITY column read (never entity proof); "
                              "monolithic/torch stores=one keys load cached by source sha; sharded wrappers="
                              "manifest enumeration without tensor reads + per-uid shard-file entity check; "
                              "torch_map without torch falls back to pickle, torch-zip typed NEEDS_TORCH"),
               "materialized": False}
    if a.materialize:
        if exit_code != EXIT_OK:
            print("MATERIALIZE_REFUSED: typed source problems must be resolved first", file=sys.stderr)
            summary["materialized"] = "REFUSED_TYPED_SOURCE_PROBLEMS"
            with open(os.path.join(a.out, "UNION_SUMMARY.json"), "w") as f:
                json.dump(summary, f, indent=2)
            return exit_code
        mcode, mres = materialize(a, ctx, fam_sources, demands, seqmap, uid2sha, notes)
        summary["materialized"] = mres
        summary["source_notes"] = notes
        if mcode != EXIT_OK:
            exit_code = mcode
    with open(os.path.join(a.out, "UNION_SUMMARY.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({k: summary[k] for k in ("counts", "gap_families", "exit_code")}, indent=1))
    return exit_code


# --------------------------------------------------------------------------
# materialization (defect A repair) — values copied, never recomputed
# --------------------------------------------------------------------------

def check_family_value(family, v, dim):
    """Merge acceptance: finite + dimension per declared recipe. Returns (ok, detail)."""
    import numpy as np
    if family == "gvp":
        # GVP values are per-row graph tensors (tuple/list); record shape, check
        # finiteness of numeric parts, never reshape.
        parts = v if isinstance(v, (list, tuple)) else [v]
        for p in parts:
            try:
                arr = np.asarray(p, dtype=np.float64)
                if arr.dtype.kind == "f" and not np.isfinite(arr).all():
                    return False, "NON_FINITE"
            except Exception:
                pass
        return True, ""
    try:
        arr = np.asarray(v, dtype=np.float64)
    except Exception as e:
        return False, f"NOT_NUMERIC:{type(e).__name__}"
    if not np.isfinite(arr).all():
        return False, "NON_FINITE"
    if family == "global" and dim and arr.ndim == 1 and arr.shape[0] != dim:
        return False, f"DIM_MISMATCH:{arr.shape[0]}!={dim}"
    if family == "pocket" and dim and arr.ndim == 2 and arr.shape[1] != dim:
        return False, f"DIM_MISMATCH:{arr.shape[1]}!={dim}"
    return True, ""


def write_manifest(out, manifest_rows):
    cols = ["family", "key", "consumer_key_type", "source", "source_path", "value_sha256",
            "shape", "finite", "recipe", "index_source", "key_form", "status"]
    p = os.path.join(out, "MERGE_MANIFEST.tsv")
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in manifest_rows:
            w.writerow({c: r.get(c, "") for c in cols})
    return p


def materialize(a, ctx, fam_sources, demands, seqmap, uid2sha, notes):
    merged_root = os.path.join(a.out, "merged")
    os.makedirs(merged_root, exist_ok=True)
    manifest_rows, blockers = [], []
    conflict_adjudications = []  # RECOVERY PATCH merge_conflict_numeric_adjudication_20261031
    # R3-A PATCH r3a_same_lane_pairing_whitelist_20261101 (r3d generalized:
    # entries carry their own family/winner_source/evidence)
    pair_wl = {}
    for wl_path in (getattr(a, "pair_adjudications", None) or []):
        _pa = json.load(open(wl_path))
        for e in _pa.get("whitelist", []):
            if e.get("status", "").startswith("PAIR_VERIFIED"):
                pair_wl[(e.get("family", "pocket"), e["uid"])] = {
                    "winner_source": e.get("winner_source", "task_r3_overlay_new"),
                    "evidence_file": wl_path,
                    "new_pair_identity": e.get("new_pair_identity", {})}
    merged_stores = {}
    try:
        import torch  # noqa: F401
        store_fmt = "torch_pt"
    except ImportError:
        store_fmt = "pickle"

    def write_store(family, d):
        """R1.1 (audit §1): FORMAT PER REAL CONSUMER, not one uniform format.
        The audited old PrecomputedAssetIndex reads esm_mean_feature through a
        plain `pickle.load` (recovered wrapper asset_index.py:17-18) with NO
        torch/pickle fallback — so GLOBAL must ALWAYS be plain pickle
        (exact-sequence keys, original values; the GU seq2feature_600m_union.pkl
        precedent), even when torch is importable. pocket/GVP go through
        sharded_protein._torch_load_trusted (torch first, pickle fallback), so
        they may be torch archives on the node and plain pickles locally."""
        base = os.path.join(merged_root, f"merged_{family}")
        if family == "global" or store_fmt != "torch_pt":
            p = base + ".pkl"
            with open(p, "wb") as f:
                pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
            return p, "plain_pickle"
        import torch
        p = base + ".pt"
        torch.save(d, p)
        return p, "torch_pt"

    for family in ("global", "pocket", "gvp"):
        fam_ctx = ctx["families"][family]
        dim = fam_ctx.get("dim")
        recipe = fam_ctx.get("recipe", "")
        merged = {}
        items = (list(zip(demands[family]["shas"], demands[family]["seqs"])) if family == "global"
                 else [(u, None) for u in demands[family]["uids"]])
        # Reuse the project's single-shard cache strategy; group requests so
        # thousands of UIDs do not repeatedly reload the same large shard.
        sharded = [sd for sd in fam_sources[family] if getattr(sd, "_manifest", None) is not None]
        if sharded:
            items.sort(key=lambda item: tuple(str(sd._manifest[0].get(item[0], "")) for sd in sharded))
        for key, seq in items:
            consumer = seq if family == "global" else key
            found = []  # (src_name, src_path, value, key_form)
            for sd in fam_sources[family]:
                if sd.role != "value":
                    continue
                try:
                    v, key_form = sd.get_value(family, key, seq=seq)
                except TypedSource as e:
                    if e.code != "VALUE_MISSING":
                        blockers.append({"family": family, "key": key, "source": sd.name,
                                         "status": e.code, "detail": e.detail})
                    continue
                found.append((sd.name, sd.path, v, key_form))
            if not found:
                continue  # stays a gap; GF prescan classifies the step INCOMPLETE
            shas = {value_bytes_sha(v) for _, _, v, _ in found}
            adjudicated = None
            if len(shas) > 1:
                # RECOVERY PATCH merge_conflict_numeric_adjudication_20261031
                equiv, maxd = values_numerically_equivalent([v for _, _, v, _ in found])
                if not equiv:
                    # R3-A PATCH r3a_same_lane_pairing_whitelist_20261101:
                    # evidence-based SPECIFIC-key adjudication. The whitelist
                    # (PAIR_ADJUDICATIONS_64.json) carries per-uid sequence SHA,
                    # structure/pocket PDB SHA, pocket_ok indices, timing row
                    # cross-checks and gvp_n==pocket_n==len(indices): both values
                    # were produced from the SAME struct_lane work dir of THIS
                    # run (r3p pocket rows = node[[pocket_ok indices]]; r3g GVP =
                    # batch_run on the same pocket PDB). NOT a global
                    # new-value-preference; unlisted keys keep the old behavior.
                    pair = pair_wl.get((family, key))
                    if pair is not None:
                        pick = next((fnd for fnd in found if fnd[0] == pair["winner_source"]), None)
                        if pick is not None:
                            adjudicated = {
                                "family": family, "key": key,
                                "status": "PAIR_ADJUDICATED_SAME_LANE_SAME_RESIDUE_SET",
                                "max_abs_diff": "N/A_SHAPE_MISMATCH_not_numerically_comparable",
                                "winner": pick[0],
                                "sources": [{"name": n, "value_sha256": value_bytes_sha(v)}
                                            for n, _, v, _ in found],
                                "evidence_file": pair["evidence_file"],
                                "new_pair_identity": pair["new_pair_identity"],
                                "detail": ("verified same-structure same-residue-set pairing; "
                                           "old conflicting value disclosed, never silently "
                                           "overwritten"),
                            }
                            conflict_adjudications.append(adjudicated)
                            found = [pick]
                    # RECOVERY PATCH recipe_conformant_formal_winner_20261031
                    # (r3 fix: the numeric-equivalent record now lives in the
                    # else branch — the r2 fall-through double-append defect is
                    # gone; formal winners no longer also log a false
                    # NUMERICALLY_EQUIVALENT entry):
                    if len(found) > 1:
                        formal_pick = next((fnd for fnd in found if fnd[0].startswith("formal")), None)
                        if formal_pick is None:
                            blockers.append({"family": family, "key": key, "status": "SOURCE_CONFLICT",
                                             "sources": [{"name": n, "value_sha256": value_bytes_sha(v)}
                                                         for n, _, v, _ in found],
                                             "max_abs_diff": maxd, "tolerance": MERGE_NUMERIC_TOL,
                                             "detail": ("priority winner NOT written; typed, never silently "
                                                        "overwritten; values differ BEYOND the pc gate and no "
                                                        "registered formal source is present — affected "
                                                        "keys/steps stay blocked")})
                            manifest_rows.append({"family": family, "key": key,
                                                  "consumer_key_type": "sequence_text" if family == "global" else "runtime_uid",
                                                  "source": ";".join(n for n, _, _, _ in found),
                                                  "status": "SOURCE_CONFLICT_NOT_MERGED"})
                            continue
                        adjudicated = {
                            "family": family, "key": key,
                            "status": "RECIPE_CONFORMANT_FORMAL_WINNER_COPIED",
                            "max_abs_diff": maxd, "tolerance": MERGE_NUMERIC_TOL,
                            "winner": formal_pick[0],
                            "sources": [{"name": n, "value_sha256": value_bytes_sha(v)}
                                        for n, _, v, _ in found],
                            "detail": ("beyond-gate real difference (pocket-definition level); the "
                                       "registered formal source wins per declared recipe + GF "
                                       "training feature distribution + accepted GU/C1 native-rows "
                                       "precedent; all source byte shas disclosed; never silent"),
                        }
                        conflict_adjudications.append(adjudicated)
                        found = [formal_pick]
                else:
                    adjudicated = {
                        "family": family, "key": key,
                        "status": "NUMERICALLY_EQUIVALENT_PRIORITY_WINNER_COPIED",
                        "max_abs_diff": maxd, "tolerance": MERGE_NUMERIC_TOL,
                        "winner": found[0][0],
                        "sources": [{"name": n, "value_sha256": value_bytes_sha(v)}
                                    for n, _, v, _ in found],
                        "detail": ("byte shas differ across sources (cross-node extraction "
                                   "nondeterminism at float32 ULP level) but float64 values agree "
                                   "within the declared pc gate; priority winner byte-copied; all "
                                   "source shas disclosed"),
                    }
                    conflict_adjudications.append(adjudicated)
            name, spath, v, key_form = found[0]
            ok, detail = check_family_value(family, v, dim)
            if not ok:
                blockers.append({"family": family, "key": key, "source": name,
                                 "status": "VALUE_ACCEPTANCE_FAILED", "detail": detail})
                manifest_rows.append({"family": family, "key": key,
                                      "consumer_key_type": "sequence_text" if family == "global" else "runtime_uid",
                                      "source": name, "source_path": spath, "value_sha256": value_bytes_sha(v),
                                      "shape": value_shape(v), "finite": "FAILED", "recipe": recipe,
                                      "key_form": key_form, "status": detail})
                continue
            merged[consumer] = v
            manifest_rows.append({
                "family": family,
                "key": (sha_text(seq) if family == "global" else key),
                "consumer_key_type": "sequence_text" if family == "global" else "runtime_uid",
                "source": name, "source_path": spath, "value_sha256": value_bytes_sha(v),
                "shape": value_shape(v), "finite": "OK", "recipe": recipe,
                "index_source": next((sd.index_source for sd in fam_sources[family] if sd.name == name), ""),
                "key_form": key_form,
                "status": (("MERGED_VALUE_COPIED_" + {
                    "NUMERICALLY_EQUIVALENT_PRIORITY_WINNER_COPIED": "NUM_EQUIV_WITHIN_PC_GATE",
                    "RECIPE_CONFORMANT_FORMAL_WINNER_COPIED": "RECIPE_CONFORMANT_FORMAL",
                    "PAIR_ADJUDICATED_SAME_LANE_SAME_RESIDUE_SET": "PAIR_ADJUDICATED_SAME_LANE",
                }.get(adjudicated["status"], "ADJUDICATED")) if adjudicated
                    else "MERGED_VALUE_COPIED")})
        p, fmt = write_store(family, merged)
        merged_stores[family] = {"path": p, "format": fmt, "keys_n": len(merged),
                                 "sha256": sha_file(p)}

    # RECOVERY PATCH merge_conflict_numeric_adjudication_20261031: full typed
    # disclosure of every numerically adjudicated cross-source conflict.
    with open(os.path.join(a.out, "MERGE_CONFLICT_ADJUDICATIONS.json"), "w") as f:
        json.dump({"patch_ids": ["merge_conflict_numeric_adjudication_20261031",
                                 "recipe_conformant_formal_winner_20261031"],
                   "tolerance": MERGE_NUMERIC_TOL,
                   "tolerance_source": "task-declared pc gate: s5_lane_plm_c95.py --max-delta default 2e-4",
                   "precedent": "p298-dual REPAIR_LEDGER.tsv 2026-09-21T18:05Z equivalence_criterion_bit_exact_too_strict; GU/C1 native-rows-from-formal precedent",
                   "adjudicated_n": len(conflict_adjudications),
                   "by_status": {s: sum(1 for x in conflict_adjudications if x["status"] == s)
                                 for s in {x["status"] for x in conflict_adjudications}},
                   "adjudications": conflict_adjudications}, f, indent=1)

    # ---------------- reaction views (DRFP / center / conformations) --------
    reaction = {"status": "NOT_REQUESTED"}
    if a.step_table and a.gf_config_template:
        reaction, rrows, rblockers = merge_reactions(a, merged_root)
        manifest_rows.extend(rrows)
        blockers.extend(rblockers)

    # ---------------- merged GF config (line-level template substitution) ---
    cfg_path = os.path.join(a.out, "cfg", "c95_3b_merged_config.yaml")
    os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
    prov = {"template_path": a.gf_config_template, "template_sha256": sha_file(a.gf_config_template),
            "utc": datetime.now(timezone.utc).isoformat(),
            "store_formats": {f: merged_stores[f]["format"] for f in merged_stores},
            "overrides": {}, "merged_stores": merged_stores, "reaction": reaction}
    text = open(a.gf_config_template).read()
    overrides = {
        "esm_mean_feature": merged_stores["global"]["path"],
        "esm_node_feature": merged_stores["pocket"]["path"],
        "protein_gvp_feat": merged_stores["gvp"]["path"],
    }
    if isinstance(reaction, dict) and reaction.get("rxn_fp"):
        # merged reaction views exist (typed blockers — e.g. a mol-graph cache
        # extension that needs torch — keep exit code 4 and MUST be resolved
        # before N5; the config already points at the merged views so the
        # resolution is a rerun, not a rewire)
        overrides["rxn_fp"] = reaction["rxn_fp"]
        overrides["reaction_center"] = reaction["reaction_center"]
        overrides["mol_conformation"] = reaction["mol_dir"]
    cfg_errs = []
    for k, v in overrides.items():
        pat = re.compile(rf"^(?P<head>\s*{re.escape(k)}\s*:\s*)(?P<val>.*)$", re.MULTILINE)
        m = pat.search(text)
        if not m:
            cfg_errs.append({"key": k, "status": "CONFIG_TEMPLATE_KEY_MISSING"})
            continue
        prov["overrides"][k] = {"old": m.group("val").strip(), "new": v}
        text = text[:m.start()] + m.group("head") + v + text[m.end():]
    mp = write_manifest(a.out, manifest_rows)
    if cfg_errs:
        notes.append({"family": "config", "status": "CONFIG_TEMPLATE_KEY_MISSING", "keys": cfg_errs})
        return EXIT_CONFIG, {"status": "CONFIG_FAILED", "errors": cfg_errs, "manifest": mp}
    with open(cfg_path, "w") as f:
        f.write(text)
    prov["config_path"] = cfg_path
    prov["config_sha256"] = sha_file(cfg_path)
    prov["manifest_path"] = mp
    prov["manifest_sha256"] = sha_file(mp)
    prov["blockers_n"] = len(blockers)
    with open(os.path.join(a.out, "MERGE_BLOCKERS.json"), "w") as f:
        json.dump(blockers, f, indent=1)
    with open(os.path.join(a.out, "cfg", "CONFIG_PROVENANCE.json"), "w") as f:
        json.dump(prov, f, indent=1)
    status = "MERGED_WITH_TYPED_BLOCKERS" if blockers else "MERGED_COMPLETE"
    return (EXIT_TYPED if blockers else EXIT_OK), {
        "status": status, "stores": merged_stores, "config": cfg_path,
        "provenance": os.path.join(a.out, "cfg", "CONFIG_PROVENANCE.json"),
        "manifest": mp, "manifest_rows": len(manifest_rows),
        "blockers": blockers[:20], "blockers_n": len(blockers), "reaction": reaction,
        "note": ("values byte-copied (value_sha256 recorded per key); old stores read-only; "
                 "global consumer key = exact sequence text and store = plain pickle (old index "
                 "pickle.load line); pocket/GVP consumer key = runtime UID, format torch_pt on node "
                 "/ pickle locally — both accepted by _torch_load_trusted (sharded_protein.py)")}


def _template_value(text, key):
    m = re.search(rf"^\s*{re.escape(key)}\s*:\s*(.*)$", text, re.MULTILINE)
    return m.group(1).strip().strip("'\"") if m else None


def molecules_of(rxn):
    """asset_index._molecules (recovered wrapper) — copied for demand calc."""
    if rxn.count(">>") != 1:
        return []
    sides = rxn.split(">>")
    return [v.replace("*", "C") for side in sides for v in side.split(".") if v and v != "[*H2]"]


def merge_reactions(a, merged_root):
    """Merged reaction views following the audited s2_graph_loader method:
    merged rxn2fp.pkl + reacting_center.pkl (demanded subset, values copied),
    merged mol2id.csv with globally re-IDed SDF copies, and mol_graph_dict.pt
    byte-copied when complete / extended via the frozen geometric functions
    when new molecules appear (strict verification; no silent drops)."""
    rows, blockers = [], []
    rdir = os.path.join(merged_root, "reaction")
    os.makedirs(rdir, exist_ok=True)
    ttext = open(a.gf_config_template).read()
    formal = {k: _template_value(ttext, k) for k in ("rxn_fp", "reaction_center", "mol_conformation")}
    for k, p in formal.items():
        if not p or not os.path.exists(p):
            blockers.append({"family": "reaction", "status": "FORMAL_SOURCE_ABSENT", "key": k, "path": p})
    if blockers:
        return {"status": "TYPED_FORMAL_SOURCES_ABSENT", "formal": formal}, rows, blockers
    steps = json.load(open(a.step_table))
    demanded = {}
    for s in steps:
        demanded[s["model_reaction"]] = s["model_key_sha256"]
    formal_fp = pickle.load(open(formal["rxn_fp"], "rb"))
    formal_center = pickle.load(open(formal["reaction_center"], "rb"))
    new_fp, new_center = {}, {}
    new_mol2id = {}   # SMILES -> (sdf_path)
    alias_skipped = 0
    bundle_roots = list(getattr(a, "reused_reaction_bundles", []) or [])
    if a.new_reaction_bundles:
        bundle_roots.append(a.new_reaction_bundles)
    bundle_dirs = sorted({p for root in bundle_roots if os.path.isdir(root)
                          for p in glob.glob(os.path.join(root, "RXASSET_*"))})
    if bundle_dirs:
        for bdir in bundle_dirs:
            for pat, sink in (("**/rxn2fp.pkl", new_fp), ("**/reacting_center.pkl", new_center)):
                for p in glob.glob(os.path.join(bdir, pat), recursive=True):
                    d = pickle.load(open(p, "rb"))
                    for k, v in d.items():
                        if k in demanded:
                            if k in sink and value_bytes_sha(sink[k]) != value_bytes_sha(v):
                                blockers.append({"family": "reaction", "key": sha_text(k),
                                                 "status": "SOURCE_CONFLICT",
                                                 "detail": f"{p} vs earlier bundle"})
                            sink.setdefault(k, v)
                        else:
                            alias_skipped += 1  # de-stereo alias / foreign keys stay out (exact-key isolation)
            for m2id in glob.glob(os.path.join(bdir, "**/mol2id.csv"), recursive=True):
                mdir = os.path.dirname(m2id)
                with open(m2id, newline="") as f:
                    for r in csv.DictReader(f):
                        sm = r["SMILES"]
                        sdf = os.path.join(mdir, f"{r['ID']}.sdf")
                        if sm in demanded_mols_set(demanded) and os.path.isfile(sdf):
                            new_mol2id.setdefault(sm, sdf)
    merged_fp, merged_center = {}, {}
    for rxn, key in sorted(demanded.items(), key=lambda kv: kv[1]):
        for store, mstore, label, sink_new in ((formal_fp, merged_fp, "drfp", new_fp),
                                               (formal_center, merged_center, "center", new_center)):
            if rxn in store:
                mstore[rxn] = store[rxn]
                src, spath = "formal", formal["rxn_fp" if label == "drfp" else "reaction_center"]
            elif rxn in sink_new:
                mstore[rxn] = sink_new[rxn]
                src, spath = "accepted_bundle", ";".join(bundle_roots)
            else:
                blockers.append({"family": f"reaction_{label}", "key": key, "status": "REACTION_ASSET_MISSING",
                                 "detail": "step goes INCOMPLETE_POOL at GF prescan; never zero-filled"})
                continue
            rows.append({"family": f"reaction_{label}", "key": key, "consumer_key_type": "reaction_smiles_text",
                         "source": src, "source_path": spath, "value_sha256": value_bytes_sha(mstore[rxn]),
                         "shape": value_shape(mstore[rxn]), "finite": "N/A_FINGERPRINT", "recipe": label,
                         "key_form": "EXACT_MODEL_KEY", "status": "MERGED_VALUE_COPIED"})
    fp_path = os.path.join(rdir, "rxn2fp_merged.pkl")
    ct_path = os.path.join(rdir, "reacting_center_merged.pkl")
    pickle.dump(merged_fp, open(fp_path, "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(merged_center, open(ct_path, "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    # ---- merged molecule directory ----------------------------------------
    mol_dir = os.path.join(rdir, "mol_conformation")
    os.makedirs(mol_dir, exist_ok=True)
    demanded_mols = sorted({m for rxn in demanded for m in molecules_of(rxn)})
    formal_m2id_path = os.path.join(formal["mol_conformation"], "mol2id.csv")
    formal_m2id = {}
    next_id = 1
    with open(formal_m2id_path, newline="") as f:
        for r in csv.DictReader(f):
            formal_m2id[r["SMILES"]] = int(r["ID"])
            next_id = max(next_id, int(r["ID"]) + 1)
    merged_m2id, missing_mol = [], []
    for sm in demanded_mols:
        if sm in formal_m2id:
            fid = formal_m2id[sm]
            src_sdf = os.path.join(formal["mol_conformation"], f"{fid}.sdf")
            # RECOVERY PATCH registered_view_sdf_layout_20261031: the accepted
            # p298_tc overlay view registered in the template config keeps its
            # SDF files under <mol_conformation>/sdf/<id>.sdf (391 files,
            # byte-identical to the formal full library root layout — cmp
            # verified on sampled ids 8863/4827/3681/7250); the full formal
            # store uses <mol_conformation>/<id>.sdf. Accept the registered
            # view's subdir layout; file content is used untouched.
            if not os.path.isfile(src_sdf):
                sub_sdf = os.path.join(formal["mol_conformation"], "sdf", f"{fid}.sdf")
                if os.path.isfile(sub_sdf):
                    src_sdf = sub_sdf
            dst_sdf = os.path.join(mol_dir, f"{fid}.sdf")
            if os.path.isfile(src_sdf) and not os.path.isfile(dst_sdf):
                shutil.copy2(src_sdf, dst_sdf)  # byte copy, value unchanged
            elif not os.path.isfile(src_sdf):
                blockers.append({"family": "reaction_mol", "key": sm, "status": "FORMAL_SDF_ABSENT",
                                 "path": src_sdf})
                continue
            merged_m2id.append({"SMILES": sm, "ID": fid, "origin": "formal"})
        elif sm in new_mol2id:
            nid = next_id
            next_id += 1
            shutil.copy2(new_mol2id[sm], os.path.join(mol_dir, f"{nid}.sdf"))  # globally re-IDed (s2 method)
            merged_m2id.append({"SMILES": sm, "ID": nid, "origin": "new_bundle"})
        else:
            missing_mol.append(sm)
            blockers.append({"family": "reaction_mol", "key": sm, "status": "MOLECULE_CONFORMATION_MISSING",
                             "detail": "step goes INCOMPLETE_POOL at GF prescan; never zero-filled"})
    with open(os.path.join(mol_dir, "mol2id.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["SMILES", "ID"], lineterminator="\n")
        w.writeheader()
        for r in merged_m2id:
            w.writerow({"SMILES": r["SMILES"], "ID": r["ID"]})
    # ---- mol graph cache: byte-copy when complete, extend via frozen funcs --
    cache_status = extend_mol_graph_cache(formal["mol_conformation"], mol_dir,
                                          [r["SMILES"] for r in merged_m2id], a.repo_root, blockers)
    cache_file = os.path.join(mol_dir, "mol_graph_dict.pt")
    if os.path.isfile(cache_file):
        valid_graphs = load_map(cache_file)
        kept = [r for r in merged_m2id if r["SMILES"] in valid_graphs]
        if len(kept) != len(merged_m2id):
            with open(os.path.join(mol_dir, "mol2id.csv"), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["SMILES","ID"], lineterminator="\n")
                w.writeheader(); w.writerows({"SMILES":r["SMILES"],"ID":r["ID"]} for r in kept)
            merged_m2id = kept
    return {"status": "MERGED" if not any(b["family"].startswith("reaction") for b in blockers)
            else "MERGED_WITH_TYPED_BLOCKERS",
            "rxn_fp": fp_path, "reaction_center": ct_path, "mol_dir": mol_dir,
            "demanded_reactions": len(demanded), "merged_drfp": len(merged_fp),
            "merged_center": len(merged_center), "merged_molecules": len(merged_m2id),
            "missing_molecules": missing_mol, "alias_keys_skipped": alias_skipped,
            "mol_graph_cache": cache_status}, rows, blockers


def demanded_mols_set(demanded):
    return {m for rxn in demanded for m in molecules_of(rxn)}


def extend_mol_graph_cache(formal_mol_dir, mol_dir, merged_smiles, repo_root, blockers):
    """mol_graph_dict.pt: byte-copy if it already covers every merged SMILES
    (values untouched); otherwise EXTEND for the missing molecules with the
    frozen functions from the deployed repo (geometric.mol_to_graph_data_obj_
    simple_3D + radius_graph r=3 loop=False — the load_mol_feat loop), then
    verify completeness strictly (asset_index refuses incomplete caches, so a
    silent pass like the frozen loop's is NOT acceptable here)."""
    formal_cache = os.path.join(formal_mol_dir, "mol_graph_dict.pt")
    dst_cache = os.path.join(mol_dir, "mol_graph_dict.pt")
    if not os.path.isfile(formal_cache):
        blockers.append({"family": "reaction_mol", "status": "FORMAL_GRAPH_CACHE_ABSENT", "path": formal_cache})
        return "FORMAL_GRAPH_CACHE_ABSENT"
    try:
        cache = load_map(formal_cache)
    except TypedSource as e:
        blockers.append({"family": "reaction_mol", "status": e.code, "detail": e.detail, "path": formal_cache})
        return e.code
    # RECOVERY PATCH accepted_graph_cache_union_20261031: the template view's
    # cache (391 molecules) does not cover the 121-chain molecules, and an
    # on-node frozen rebuild is IMPOSSIBLE in this environment (pyg_lib
    # 0.5.0+pt27cu126 < 0.6.0 required by torch_geometric 2.8.0 radius_graph;
    # upgrading PyG/torch is forbidden). Two REGISTERED ACCEPTED historical
    # caches fill the missing molecules with EXISTING values (objects copied
    # by reference into the merged cache — never recomputed, first source
    # wins, provenance printed and typed):
    #  * R1R1 S2_graph_loader merged_bundle — the frozen-geometric-verified
    #    reaction-graph view of THIS 121 chain (S2_GATE.json: components_ok
    #    481/481, cache_reload ok=481 bad=0, steps_489_covered=480;
    #    REUSE_PATH_MAP REACTION_GRAPH_LOADER lineage, sibling of OLD_RX)
    #  * formal full molecule library (FORMAL_MOL_GRAPHS registered location;
    #    the template view's cache is its value-equal subset — verified on 60
    #    sampled common SMILES, all attrs equal)
    # Molecules absent from every accepted cache stay typed blockers below.
    union_added = []
    for extra in ACCEPTED_GRAPH_CACHE_EXTRA:
        if not os.path.isfile(extra):
            continue
        try:
            xc = load_map(extra)
        except TypedSource:
            continue
        added = 0
        for k, v in xc.items():
            if k not in cache:
                cache[k] = v
                added += 1
        if added:
            union_added.append({"cache": extra, "keys_added": added})
    if union_added:
        print("GRAPH_CACHE_UNION:", json.dumps(union_added), flush=True)
    missing = [sm for sm in merged_smiles if sm not in cache]
    if not missing:
        if union_added:
            import torch
            torch.save(cache, dst_cache)  # accepted values re-serialized as-is
            return f"ACCEPTED_CACHE_UNION_COMPLETE_{len(union_added)}_SOURCES"
        shutil.copy2(formal_cache, dst_cache)  # byte copy, values unchanged
        return "BYTE_COPIED_COMPLETE"
    try:
        import torch  # noqa: F401
    except ImportError:
        blockers.append({"family": "reaction_mol", "status": "MOL_GRAPH_EXTENSION_REQUIRES_TORCH",
                         "missing_n": len(missing),
                         "detail": "extension code implemented (frozen geometric functions); torch absent locally"})
        return "MOL_GRAPH_EXTENSION_REQUIRES_TORCH"
    if not repo_root or not os.path.isdir(repo_root):
        blockers.append({"family": "reaction_mol", "status": "REPO_ROOT_REQUIRED_FOR_GRAPH_EXTENSION",
                         "missing_n": len(missing)})
        return "REPO_ROOT_REQUIRED_FOR_GRAPH_EXTENSION"
    import torch
    sys.path.insert(0, repo_root)
    from enzymecage.dataset.geometric import mol_to_graph_data_obj_simple_3D
    # RECOVERY PATCH r3b_radius_graph_import_alignment_20261101: the frozen
    # audited loader s2_graph_loader.py line 64 imports radius_graph from
    # torch_cluster (call at line 247: radius_graph(data.positions, r=3,
    # loop=False) — identical parameters to the call below). The previous
    # torch_geometric.nn import routes into PyG 2.8.0's WITH_RADIUS gate which
    # hard-requires pyg-lib>=0.6.0 (absent in every node env, pyg_lib 0.5.0
    # since 2026-07-10). torch_cluster 1.6.3+pt27cu126 radius_graph is CPU-
    # probe-verified on this node (DIAG round, AFDB_HTTP_PROBES sibling files).
    # No dependency upgrade, no adjacency-definition change.
    from torch_cluster import radius_graph
    from rdkit import Chem
    mol_to_index = {}
    with open(os.path.join(mol_dir, "mol2id.csv"), newline="") as f:
        for r in csv.DictReader(f):
            mol_to_index[r["SMILES"]] = int(r["ID"])
    failed = []
    for sm in missing:  # frozen load_mol_feat loop, minus its silent except-pass
        try:
            sdf_path = os.path.join(mol_dir, f"{mol_to_index[sm]}.sdf")
            mol = Chem.SDMolSupplier(sdf_path)[0]
            data, _ = mol_to_graph_data_obj_simple_3D(mol)
            if not hasattr(data, "positions"):
                raise ValueError("MISSING_REAL_MOLECULE_COORDINATES")
            data.radius_edge_index = radius_graph(data.positions, r=3, loop=False)
            cache[sm] = data
        except Exception as e:
            failed.append({"smiles": sm, "error": f"{type(e).__name__}: {e}"})
    if failed:
        torch.save(cache, dst_cache)
        blockers.append({"family": "reaction_mol", "status": "MOL_GRAPH_BUILD_FAILED", "failed": failed})
        return "MOL_GRAPH_BUILD_FAILED"
    still = [sm for sm in merged_smiles if sm not in cache]
    if still:
        blockers.append({"family": "reaction_mol", "status": "MOL_GRAPH_CACHE_INCOMPLETE_AFTER_EXTENSION",
                         "missing": still})
        return "MOL_GRAPH_CACHE_INCOMPLETE_AFTER_EXTENSION"
    torch.save(cache, dst_cache)
    return f"EXTENDED_{len(missing)}_NEW_MOLECULES_FROZEN_FUNCS"


if __name__ == "__main__":
    sys.exit(main())
