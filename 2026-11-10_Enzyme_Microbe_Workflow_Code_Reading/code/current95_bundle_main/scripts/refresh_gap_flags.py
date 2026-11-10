#!/usr/bin/env python3
"""Node-side gap refresh (R1.1 §3): the LIGHT, staging-only consumer of union
outputs — NEVER the full local generator. The full `make_reuse_inputs.py`
re-reads local preparation archives (FIN/R1D/REPP under /home/a...) that are
NOT uploaded to the node; the audit probe executed the real generator entry
under a staging-only boundary and it died on its first dependency. This module
holds the canonical gap-flags construction (imported by make_reuse_inputs too,
so local pre-staging and node refresh can never diverge) and its CLI takes
ONLY explicitly passed staged inputs:

  --universe   FINAL_SEQUENCE_UNIVERSE.tsv (accepted sha -> selected_uid)
  --union-out  dir with GAP_LIST_{global,pocket,gvp}.tsv (this run's truth)
  --out-dir    where S5_GAP_FLAGS.tsv.gz + WORKLIST_SUMMARY.json are written
  (no --union-out: skeleton mode, every flag False — lanes select nothing)

Zero gaps: correct header + 0 data rows (deterministic rewrite; the union now
also always rewrites its three GAP_LISTs, so no stale per-family list can be
re-consumed). Validation is against the CONTEXT DEMAND SET: every gap sha must
be in the universe, every gap uid must be the universe's selected_uid for its
sha (same SHA keeps the frozen UID, routing never silently changes). File
existence is not completion; a gap row that cannot be mapped to the accepted
universe is a typed error. Old-schema flags keep failing closed in the lanes.
"""
import argparse
import csv
import gzip
import json
import os
import sys

GAP_COLS = ["sequence_sha256", "selected_uid", "seq_ok", "gap_status",
            "global_gap", "pocket_ok", "gvp_ok", "gap_reasons"]


def read_tsv(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def build_gap_rows(universe_rows, union_out=None):
    """universe_rows: [{'sequence_sha256','selected_uid'}]; returns (rows, worklist, problems)."""
    uid_of = {r["sequence_sha256"]: r["selected_uid"] for r in universe_rows}
    sha_of = {v: k for k, v in uid_of.items()}
    problems = []
    if union_out is None:
        rows = [{"sequence_sha256": sh, "selected_uid": uid_of.get(sh, ""), "seq_ok": "True",
                 "gap_status": "PENDING_UNION_INVENTORY", "global_gap": "False",
                 "pocket_ok": "False", "gvp_ok": "False", "gap_reasons": ""}
                for sh in sorted(uid_of)]
        wl = {"mode": "PENDING_UNION_INVENTORY", "global_forward_items": 0,
              "pocket_forward_items": 0, "gvp_forward_items": 0, "rows": len(rows)}
        return rows, wl, problems

    def gaps(fname):
        p = os.path.join(union_out, f"GAP_LIST_{fname}.tsv")
        return read_tsv(p) if os.path.isfile(p) else []
    g_global = {r["sequence_sha256"]: r.get("reason", "TRUE_GAP") for r in gaps("global")}
    g_pocket = {r["runtime_uid"]: r.get("reason", "TRUE_GAP") for r in gaps("pocket")}
    g_gvp = {r["runtime_uid"]: r.get("reason", "TRUE_GAP") for r in gaps("gvp")}
    # demand-set validation (not file-existence): every claimed gap must map into THIS context
    for sh in g_global:
        if sh not in uid_of:
            problems.append({"kind": "global_gap_sha_not_in_universe", "value": sh})
    for fam, gm in (("pocket", g_pocket), ("gvp", g_gvp)):
        for u in gm:
            sh = sha_of.get(u)
            if sh is None:
                problems.append({"kind": f"{fam}_gap_uid_not_in_universe", "value": u})
            elif u != uid_of[sh]:
                problems.append({"kind": f"{fam}_gap_uid_route_conflict", "value": u,
                                 "detail": f"universe selected_uid for its sha is {uid_of[sh]} "
                                           "(same SHA keeps the frozen UID; routing never silently changes)"})
    if problems:
        return None, None, problems
    row_shas = sorted(set(g_global) | {sha_of[u] for u in set(g_pocket) | set(g_gvp)})
    rows = []
    for sh in row_shas:
        u = uid_of.get(sh, "")
        reasons = []
        if sh in g_global:
            reasons.append(f"global:{g_global[sh]}")
        if u in g_pocket:
            reasons.append(f"pocket:{g_pocket[u]}")
        if u in g_gvp:
            reasons.append(f"gvp:{g_gvp[u]}")
        rows.append({"sequence_sha256": sh, "selected_uid": u, "seq_ok": "True",
                     "gap_status": "TRUE_GAP_PER_UNION",
                     "global_gap": "True" if sh in g_global else "False",
                     "pocket_ok": "True" if u in g_pocket else "False",
                     "gvp_ok": "True" if u in g_gvp else "False",
                     "gap_reasons": "|".join(reasons)})
    wl = {"mode": "FROM_UNION", "union_out": union_out,
          "global_forward_items": sum(1 for r in rows if r["global_gap"] == "True"),
          "pocket_forward_items": sum(1 for r in rows if r["pocket_ok"] == "True"),
          "gvp_forward_items": sum(1 for r in rows if r["gvp_ok"] == "True"),
          "rows": len(rows)}
    for fam in ("global", "pocket", "gvp"):
        wl[f"{fam}_NO_WORK"] = (wl[f"{fam}_forward_items"] == 0)
    return rows, wl, []


def write_flags(out_dir, rows, worklist):
    os.makedirs(out_dir, exist_ok=True)
    with gzip.open(os.path.join(out_dir, "S5_GAP_FLAGS.tsv.gz"), "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=GAP_COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)   # zero rows still writes the correct header
    json.dump(worklist, open(os.path.join(out_dir, "WORKLIST_SUMMARY.json"), "w"), indent=1)
    return os.path.join(out_dir, "S5_GAP_FLAGS.tsv.gz")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", required=True)
    ap.add_argument("--union-out", default=None)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    rows, wl, problems = build_gap_rows(read_tsv(a.universe), a.union_out)
    if problems:
        json.dump(problems, open(os.path.join(a.out_dir, "REFRESH_PROBLEMS.json"), "w"), indent=1) \
            if os.path.isdir(a.out_dir) else None
        raise SystemExit("REFRESH_TYPED_ERROR: gap rows not in the accepted universe — "
                         f"{len(problems)} problems (first: {problems[0]})")
    p = write_flags(a.out_dir, rows, wl)
    print(json.dumps({"flags": p, **wl}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
