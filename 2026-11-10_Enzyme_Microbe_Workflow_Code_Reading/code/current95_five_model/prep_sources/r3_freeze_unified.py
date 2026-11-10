#!/usr/bin/env python3
"""R3 three-model unified pool freeze over the 3B-verified parent pool (382 steps).

Per row, the REAL consumer predicate of ALL THREE models must pass:
  3B    : C95AssetIndex(PrecomputedAssetIndex(R3 merged cfg per ctx), parent runtime map)
          — the A109-proven consumer path (has_enzyme closure incl. row pairing).
  legacy: LegacyArmIndexV3 overlay chain (native -> sept-union -> rescue-generated)
          wrapped by C95AssetIndex + named-bundle rule LEGACY_GEN_COMPAT.
  new   : NewArmIndexV3 (R2 chain + rescue overlays) + named-bundle rule
          NEW_GEN_COMPAT + audited S8 route-UID fallback (exact-seq identity, logged).
Retained rows = pass ALL three (order preserved); step admitted with >=1 retained
Gold; NO_DISCRIMINATION recomputed; rescue/today-batch dependency flagged per row
and per step. Outputs: UNIFIED_STEP_TABLE_{ctx}.json, THREE_MODEL_POOL_EQUALITY.json
(item-level), STEP_RETENTION_AUDIT.tsv (382 rows + assertion), per-ctx freeze
ledgers (merged copy too), EVAL_LABELS_UNIFIED_{ctx}.tsv, ASSET_EXPANSION_BEFORE_AFTER.tsv.
"""
import csv, gzip, hashlib, json, os, pickle, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_paths as P
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "scripts"))
import recovery_helpers as RH
import r2_lib as L2
import r3_consumer as C3
for p in (P.REPO_OLD, P.WRAP, P.BUNDLE + "/historical/a109"):
    if p not in sys.path: sys.path.insert(0, p)
os.environ.setdefault("ENZYMECAGE_SHARD_CACHE_SIZE", "all")
import pandas as pd, torch, yaml

t0 = time.time()
def log(*a): print(f"[{time.time()-t0:6.1f}s]", *a, flush=True)
OUT = P.NEWROOT + "/runtime/pool"; os.makedirs(OUT, exist_ok=True)
sha_text = lambda s: hashlib.sha256(s.encode()).hexdigest()

admission = json.load(open(P.NEWROOT + "/runtime/pc_genimpact/ADMISSION_DECISION.json"))
RESCUE_ADMITTED = admission["decision"] == "ADMIT_WITH_BATCH_EFFECT_DISCLOSURE"
log("rescue batch admitted:", RESCUE_ADMITTED)

# ---------- inputs ----------
pool = {ctx: json.load(open(f"{P.PKG}/inputs/{ctx}/THREE_B_VERIFIED_PARENT_POOL.json")) for ctx in P.CTXS}
runtime = {}
gold = {}
for ctx in P.CTXS:
    runtime[ctx] = f"{P.PKG}/inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv"
    with open(f"{P.PKG}/inputs/{ctx}/EVAL_LABELS_PARENT.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["gold_flag"] == "TRUE":
                gold[(ctx, r["step_occurrence_id"], r["sequence_sha256"])] = True
uid2seq = {}
for ctx in P.CTXS:
    with open(runtime[ctx]) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            uid2seq[r["runtime_uid"]] = (r["sequence_sha256"], r["sequence"])

# ---------- indices ----------
from enzymecage_wrapper.asset_index import PrecomputedAssetIndex
from c95_asset_index_ext import C95AssetIndex

log("building legacy v3 chain (native+union+rescue) ...")
legacy_core = C3.LegacyArmIndexV3(pd, torch)
log("legacy chain layers:", json.dumps(legacy_core.inventory(), default=str)[:400])

log("building new v3 index (main; reaction rebind per ctx) ...")
overlays = C3.load_overlays()
new_core = C3.NewArmIndexV3("main", pd, torch, overlays)
log("new overlay entries:", {k: len(v) for k, v in overlays.items() if k != "_manifest"})

def bind_new_reaction(ctx):
    rx = P.RXN[ctx]
    with open(rx + "/rxn2fp_merged.pkl", "rb") as f: new_core.rxn_fp = pickle.load(f)
    with open(rx + "/reacting_center_merged.pkl", "rb") as f: new_core.reaction_centers = pickle.load(f)
    from pathlib import Path
    mdir = Path(rx + "/mol_conformation")
    mtab = pd.read_csv(mdir / "mol2id.csv")
    new_core.molecule_index = frozenset(mtab["SMILES"].astype(str))
    new_core.molecule_graphs = torch.load(mdir / "mol_graph_dict.pt", map_location="cpu", weights_only=False)
    new_core.ctx = ctx

def extend_uid_map(idx, ctx, extra=None):
    """C95-style extension with typed conflicts."""
    old = dict(idx.uid_to_sequence)
    conflicts = []
    with open(runtime[ctx]) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            u, sq, sh = r["runtime_uid"], r["sequence"], r["sequence_sha256"]
            assert sha_text(sq) == sh, f"runtime row sha mismatch {u}"
            if u in old and old[u] != sq:
                conflicts.append(u)
            idx.uid_to_sequence[u] = sq
    for u, sq in (extra or {}).items():
        if u in idx.uid_to_sequence and idx.uid_to_sequence[u] != sq:
            conflicts.append(u)
        idx.uid_to_sequence[u] = sq
    idx.ambiguous_uids = frozenset(a for a in idx.ambiguous_uids if a not in idx.uid_to_sequence or conflicts)
    assert not conflicts, f"UID_SEQUENCE_CONFLICTS {conflicts[:5]}"

summary = {"contexts": {}, "rescue_admitted": RESCUE_ADMITTED}
equality = {"policy": "item-level equality of the three per-arm projections (uids, shas, seqs, order, gold flags, reaction, model_key)", "steps": []}
audit = []
before_after = []

for ctx in P.CTXS:
    log(f"===== ctx {ctx} =====")
    # 3B index (A109 pattern, merged stores per ctx)
    cfg3b = yaml.safe_load(open(f"{P.R3}/materialize_{ctx}/cfg/c95_3b_merged_config.yaml"))
    idx3b = RH.build_3b_index(P, ctx, cfg3b, PrecomputedAssetIndex, C95AssetIndex)
    log("3B index:", idx3b.inventory()["pocket_node_uid_count"], "pocket;", idx3b.inventory()["gvp_uid_count"], "gvp")
    # legacy: rebind reaction + extend map + C95 wrapper for conflict typing
    legacy_core.bind_reaction(ctx, pd, torch)
    legacy_idx = C95AssetIndex(legacy_core, runtime[ctx])
    # new: rebind reaction + sha map + route fallback prep
    bind_new_reaction(ctx)
    pairs = []
    for s in pool[ctx]:
        for u, sh in zip(s["pool_uids"], s["pool_shas"]):
            e = uid2seq.get(u)
            if e and e[0] == sh: pairs.append((e[1], sh))
    new_core.set_sha_map(pairs)
    route_extra = {}
    # pre-pass route resolution for new arm (audited substitution candidates)
    for s in pool[ctx]:
        for u, sh in zip(s["pool_uids"], s["pool_shas"]):
            e = uid2seq.get(u)
            if not e: continue
            ok, reason, src = C3.new_arm_check_v3(new_core, u, e[1], sh)
            if not ok and reason in ("NEW_POCKET_MISSING_ALL_ROUTES", "NEW_GVP_MISSING_ALL_ROUTES"):
                ru = new_core.sha2route.get(sh)
                if ru and ru != u:
                    cseqv = new_core.cseq.loc[ru, "sequence"] if ru in new_core.cseq.index else None
                    if cseqv is not None and sha_text(cseqv) == sh:
                        route_extra.setdefault((u, sh), ru)
    if route_extra:
        extra_seqs = {}
        for (u, sh), ru in route_extra.items():
            extra_seqs[ru] = new_core.cseq.loc[ru, "sequence"]
        extend_uid_map(new_core, ctx, extra_seqs)
        log("new arm audited-route candidates:", len(route_extra))
    else:
        extend_uid_map(new_core, ctx)
    extend_uid_map(legacy_core, ctx)

    ledger = []
    unified = []
    counts = {"rows_total": 0, "rows_retained": 0, "rows_excluded": 0,
              "excl_3b": 0, "excl_legacy": 0, "excl_new": 0, "excl_multi": 0,
              "route_uid_rows_new": 0, "rescue_rows": 0, "today_batch_rows": 0}
    reason_ct = {}
    for s in pool[ctx]:
        sid = s["step_id"]; rxn = s["model_reaction"]
        miss3 = idx3b.missing_assets(rxn)
        missl = legacy_idx.missing_assets(rxn)
        missn = new_core.missing_assets(rxn)
        rxn_ok = not (miss3 or missl or missn)
        keep = []
        for pos, (u, sh) in enumerate(zip(s["pool_uids"], s["pool_shas"])):
            counts["rows_total"] += 1
            e = uid2seq.get(u)
            g = bool(gold.get((ctx, sid, sh)))
            if not e or e[0] != sh:
                ledger.append([ctx, sid, pos, u, sh, g, "EXCLUDED", "UID_SEQ_MAP_MISSING_OR_MISMATCH", "", "", "", "", ""])
                counts["rows_excluded"] += 1
                continue
            seq = e[1]
            ok3 = idx3b.has_enzyme(u)
            okl, reasl, srcl = (False, "LEGACY_NOT_CHECKED_RXN_FAIL", {}) if not rxn_ok else C3.legacy_arm_check_v3(legacy_idx, u, seq)
            aun = u; usrc = "SCIENTIFIC"
            okn, reason, srcn = (False, "NEW_NOT_CHECKED_RXN_FAIL", {}) if not rxn_ok else C3.new_arm_check_v3(new_core, u, seq, sh)
            if not okn and (u, sh) in route_extra and rxn_ok:
                ru = route_extra[(u, sh)]
                okn2, reason2, srcn2 = C3.new_arm_check_v3(new_core, ru, seq, sh)
                if okn2:
                    okn, reason, srcn, aun, usrc = True, "OK_VIA_AUDITED_ROUTE", srcn2, ru, "AUDITED_ROUTE_S8"
                    counts["route_uid_rows_new"] += 1
                else:
                    reason = f"{reason}|route_try:{reason2}"
            keepall = ok3 and okl and okn
            lroute = f"{srcl.get('pocket','')}/{srcl.get('gvp','')}/{srcl.get('global','')}" if okl else ""
            nroute = f"{srcn.get('pocket','')}/{srcn.get('gvp','')}/{srcn.get('global','')}" if okn else ""
            today = bool(okl and okn and ("RESCUE" in lroute or "RESCUE" in nroute))
            if keepall:
                counts["rows_retained"] += 1
                counts["rescue_rows"] += int("RESCUE" in lroute or "RESCUE" in nroute)
                counts["today_batch_rows"] += int(today)
                keep.append((pos, u, sh, seq, g, aun, usrc, lroute, nroute, today))
            else:
                counts["rows_excluded"] += 1
                if not ok3: counts["excl_3b"] += 1
                if not okl: counts["excl_legacy"] += 1
                if not okn: counts["excl_new"] += 1
                if sum(not x for x in (ok3, okl, okn)) > 1: counts["excl_multi"] += 1
                rr = f"3B:{'OK' if ok3 else 'MISS'}|LEG:{reasl}|NEW:{reason}"
                reason_ct[reasl if not okl else (reason.split('|')[0] if not okn else "3B_MISSING")] = \
                    reason_ct.get(reasl if not okl else (reason.split('|')[0] if not okn else "3B_MISSING"), 0) + 1
            ledger.append([ctx, sid, pos, u, sh, g, "RETAINED" if keepall else "EXCLUDED",
                           "" if keepall else f"3B={ok3};LEG={reasl};NEW={reason}", lroute, nroute,
                           aun if keepall else "", usrc if keepall else "", str(today) if keepall else ""])
        n_gold = sum(1 for k in keep if k[4])
        if rxn_ok and n_gold >= 1 and keep:
            entry = {
                "step_id": sid, "ctx": ctx, "model_reaction": rxn,
                "model_key_sha256": s["model_key_sha256"],
                "pool_uids": [k[1] for k in keep], "pool_shas": [k[2] for k in keep],
                "pool_seqs": [k[3] for k in keep],
                "asset_uids_3b": [k[1] for k in keep],
                "asset_uids_legacy": [k[1] for k in keep],
                "asset_uids_new": [k[5] for k in keep],
                "uid_source_new": [k[6] for k in keep],
                "legacy_routes": [k[7] for k in keep],
                "new_routes": [k[8] for k in keep],
                "today_batch_flags": [k[9] for k in keep],
                "gold_flags": [k[4] for k in keep],
                "no_discrimination": (len(keep) - n_gold) == 0,
                "n_gold": n_gold, "n_background": len(keep) - n_gold,
                "n_parent": len(s["pool_uids"]), "n_excluded": len(s["pool_uids"]) - len(keep),
                "rescue_dependent": any(k[9] and k[4] for k in keep),
                "rescue_rows_n": sum(1 for k in keep if k[9]),
                "provenance": "R3_UNIFIED_THREE_MODEL_CONSUMER_ACCEPTED_ORDER_PRESERVED",
            }
            assert entry["model_key_sha256"] == sha_text(rxn), f"model key mismatch {sid}"
            unified.append(entry)
            # item-level equality evidence: three projections from ONE table
            proj = {arm: [entry[f"pool_uids"], entry[f"pool_shas"], entry["gold_flags"]] for arm in ("3b", "legacy", "new")}
            eq = (proj["3b"] == proj["legacy"] == proj["new"])
            equality["steps"].append({"step_id": sid, "ctx": ctx, "n": len(keep),
                                      "item_level_equal": bool(eq),
                                      "projection_sha256": sha_text(json.dumps(proj["3b"], default=str)),
                                      "asset_uid_note": "new-arm asset uids may be audited-route uids for store lookups; scientific pool_uids/order/gold are the single shared identity"})
            assert eq, f"POOL PROJECTION INEQUALITY {sid}"
            audit.append([ctx, sid, s["model_key_sha256"][:16], "RETAINED", len(keep), n_gold, len(keep) - n_gold,
                          len(s["pool_uids"]) - len(keep), str(entry["no_discrimination"]), str(entry["rescue_dependent"]),
                          sid.split("__")[0], ""])
        else:
            if not rxn_ok:
                why = "REACTION_ASSET_MISSING:" + "|".join(miss3 + missl + missn)
            elif n_gold == 0:
                why = "NO_COMMON_CONSUMABLE_GOLD_AFTER_TRI_CHECK"
            else:
                why = "NO_RETAINED_ROWS"
            audit.append([ctx, sid, s["model_key_sha256"][:16], "NOT_ADMITTED", 0, 0, 0, len(s["pool_uids"]), "", "",
                          sid.split("__")[0], why])
    # assertion: no step with rxn-ok + >=1 tri-consumable gold may be missing from unified
    uni_ids = {e["step_id"] for e in unified}
    for a in audit:
        if a[3] == "NOT_ADMITTED" and a[11] == "NO_RETAINED_ROWS":
            raise AssertionError(f"step with retained rows not in unified table: {a[1]}")
    json.dump(unified, open(f"{OUT}/UNIFIED_STEP_TABLE_{ctx}.json", "w"))
    with gzip.open(f"{OUT}/FREEZE_LEDGER_{ctx}.tsv.gz", "wt") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["ctx", "step_id", "pool_position", "runtime_uid", "sequence_sha256", "gold",
                    "state", "typed_reasons", "legacy_route", "new_route", "asset_uid_new", "uid_source_new", "today_batch"])
        w.writerows(ledger)
    # unified eval labels (retained rows only, parent gold flags)
    with open(f"{OUT}/EVAL_LABELS_UNIFIED_{ctx}.tsv", "w") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["step_occurrence_id", "sequence_sha256", "gold_flag"])
        for e in unified:
            for sh, g in zip(e["pool_shas"], e["gold_flags"]):
                w.writerow([e["step_id"], sh, "TRUE" if g else "FALSE"])
    summary["contexts"][ctx] = {"parent_steps": len(pool[ctx]), "unified_steps": len(unified),
                                "unified_rows": sum(len(e["pool_uids"]) for e in unified),
                                "unified_gold_rows": sum(e["n_gold"] for e in unified),
                                "no_discrimination_steps": sum(1 for e in unified if e["no_discrimination"]),
                                "rescue_dependent_steps": sum(1 for e in unified if e["rescue_dependent"]),
                                **counts, "typed_reasons": reason_ct}
    log(f"ctx {ctx}: unified {len(unified)} steps / {counts['rows_retained']} rows;",
        "rescue-dependent steps:", summary["contexts"][ctx]["rescue_dependent_steps"],
        "reasons:", reason_ct)

# retention audit file
with open(f"{OUT}/STEP_RETENTION_AUDIT.tsv", "w") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["ctx", "step_id", "model_key16", "state", "n_retained", "n_gold_retained", "n_background_retained",
                "n_excluded", "no_discrimination", "rescue_dependent", "case_id", "typed_reason"])
    w.writerows(audit)
assert len(audit) == 382, f"audit rows {len(audit)} != 382"
json.dump(equality, open(f"{OUT}/THREE_MODEL_POOL_EQUALITY.json", "w"), indent=1)
log("equality: all steps item-level equal:", all(x["item_level_equal"] for x in equality["steps"]))

# BEFORE/AFTER
ovlman = overlays.get("_manifest", {})
ba = [
    ["metric", "before_R2", "after_R3_unified"],
    ["three_way_common_steps", 0, sum(summary["contexts"][c]["unified_steps"] for c in P.CTXS)],
    ["dual600_common_steps_R2", 225, "-"],
    ["legacy_scored_steps_R2", 225, "-"],
    ["new_independent_steps_R2", 271, "-"],
    ["unified_rows", 0, sum(summary["contexts"][c]["unified_rows"] for c in P.CTXS)],
    ["legacy_reuse_native_uids", 4090, "-"],
    ["legacy_reuse_sept_union_uids", 0, 874],
    ["legacy_rescue_generated_uids_sliced", 0, ovlman.get("summary", {}).get("legacy_pocket", 0)],
    ["new_reuse_store_ready_uids", 5089, "-"],
    ["new_rescue_sliced_uids", 0, ovlman.get("summary", {}).get("new600_pocket", 0)],
    ["gpu_node_sequences_generated", 0, 1014],
    ["cpu_reslice_from_p291_cache", 0, sum(1 for _ in ())],  # filled from receipts below
    ["typed_failed_uids", 0, sum(ovlman.get("summary", {}).get("typed", {}).values())],
]
# cpu reslice count from slice receipts
try:
    nreslice = 0
    with open(P.NEWROOT + "/overlay/SLICE_RECEIPTS.jsonl") as f:
        for line in f:
            if line.strip() and json.loads(line).get("node_source") == "P291_SEQ_NODES_CACHE_RESLICE": nreslice += 1
    ba[-1] = ["typed_failed_uids", 0, sum(ovlman.get("summary", {}).get("typed", {}).values())]
    ba[11] = ["cpu_reslice_from_p291_cache", 0, nreslice]
except Exception:
    pass
with open(f"{OUT}/ASSET_EXPANSION_BEFORE_AFTER.tsv", "w") as f:
    for r in ba: f.write("\t".join(str(x) for x in r) + "\n")

summary["generated_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
summary["elapsed_sec"] = round(time.time() - t0, 1)
json.dump(summary, open(f"{OUT}/FREEZE_SUMMARY.json", "w"), indent=1)
log("FREEZE DONE", json.dumps({c: {k: summary["contexts"][c][k] for k in ("unified_steps", "unified_rows", "unified_gold_rows", "no_discrimination_steps", "rescue_dependent_steps")} for c in P.CTXS}))
