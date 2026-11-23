#!/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python
"""S7 reaction-group split (task-local from the 2026-07-01 step5 authority,
SHA 7622a8cb...). Algorithm skeleton preserved: seed=42 shuffle of sorted
entities, int(n*0.8)/int(n*0.1) prefix split, remaining to test, UID overlap
allowed but disclosed. Scientific adaptation per contract §3:
 - entity = INTERNAL_SPLIT_GROUP over frozen directed reactions:
     reverse_R = right>>left; a,b = sorted([R,reverse_R])
     ISG = "ISG_" + sha256((a + "\\n" + b)).hexdigest()
 - sequence scientific keys carried; row schema §3.3; ordering §3.3;
 - V6 same-direction gate; empty values normalized to "" (no literal nan).
"""
import hashlib
import os
import random
import sys

import pandas as pd
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s7cfg as cfg

SEED = 42


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(8 << 20), b""):
            h.update(b)
    return h.hexdigest()


def isg(rxn):
    left, _, right = rxn.partition(">>")
    a, b = sorted([rxn, right + ">>" + left])
    return "ISG_" + hashlib.sha256((a + "\n" + b).encode("utf-8")).hexdigest()


def dirkey(c):
    out = []
    for side in c.split(">>"):
        cs = [Chem.MolToSmiles(Chem.MolFromSmiles(x), isomericSmiles=True) for x in side.split(".")]
        out.append(tuple(sorted(cs)))
    return (out[0], out[1])


def main():
    fail = []
    fz = pd.read_parquet(cfg.FROZEN_PARQUET).fillna("").astype(str)
    assert len(fz) == 755828, len(fz)
    pos_n = int((fz.Label == "1").sum()); neg_n = int((fz.Label == "0").sum())
    assert pos_n == 112245 and neg_n == 643583
    rxns = sorted(fz.CANO_RXN_SMILES.unique())
    assert len(rxns) == 5770
    # input hard gates
    assert int(fz.duplicated(["CANO_RXN_SMILES", "sequence_sha256", "Label"]).sum()) == 0
    pk = set(zip(fz[fz.Label == "1"].CANO_RXN_SMILES, fz[fz.Label == "1"].sequence_sha256))
    nk = set(zip(fz[fz.Label == "0"].CANO_RXN_SMILES, fz[fz.Label == "0"].sequence_sha256))
    assert len(pk & nk) == 0
    lab = fz.groupby("CANO_RXN_SMILES").Label.agg(set)
    assert all(s >= {"0", "1"} for s in lab.values)

    groups = {r: isg(r) for r in rxns}
    uniq = sorted(set(groups.values()))
    rng = random.Random(SEED)
    rng.shuffle(uniq)
    n_tr = int(len(uniq) * 0.8); n_va = int(len(uniq) * 0.1)
    assign = {}
    for g in uniq[:n_tr]:
        assign[g] = "train"
    for g in uniq[n_tr:n_tr + n_va]:
        assign[g] = "valid"
    for g in uniq[n_tr + n_va:]:
        assign[g] = "test"

    fz["INTERNAL_SPLIT_GROUP"] = fz.CANO_RXN_SMILES.map(groups)
    fz["split"] = fz.INTERNAL_SPLIT_GROUP.map(assign)
    fz["UniprotID"] = fz.training_carrier_uid
    fz["negative_source"] = fz.apply(lambda r: "POSITIVE" if r.Label == "1" else r.negative_source, axis=1)
    REQ = ["UniprotID", "sequence", "sequence_sha256", "CANO_RXN_SMILES",
           "directed_training_reaction_id", "INTERNAL_SPLIT_GROUP", "Label", "negative_source"]
    EXTRA = ["example_id", "ec_numbers", "training_carrier_uid", "negative_id",
             "source_reaction", "source_rank", "source_similarity", "target_neg", "n_pos",
             "negative_rank", "random_seed", "target_ec3", "candidate_ec3"]
    cols = []
    for c in REQ + EXTRA:
        if c not in cols:
            cols.append(c)
    # V6 same-direction gate (S6 audited semantics: per-side isomeric canonical
    # sorted components, side order preserved; reverse counted separately)
    v6 = pd.read_csv(cfg.V6_CSV, dtype=str).fillna("")
    vk = {dirkey(c) for c in v6.canonical_directional if ">>" in c}
    vk.discard(None)
    rev_keys = {(b, a) for a, b in vk}
    v6_hits = [r for r in rxns if dirkey(r) in vk]
    v6_rev_only = [r for r in rxns if dirkey(r) not in vk and dirkey(r) in rev_keys]
    if v6_hits:
        fail.append(f"V6_SAME_DIRECTION_OVERLAP={len(v6_hits)}")

    audit = {"same_direction_overlaps": len(v6_hits), "first_hits": v6_hits[:5],
             "reverse_only_counterparts_counted": len(v6_rev_only),
             "note": "V6 never enters the internal split and never selects S8 configs"}

    counts = {}
    for split in ("train", "valid", "test"):
        sub = fz[fz.split == split][cols].copy()
        sub = sub.sort_values(["INTERNAL_SPLIT_GROUP", "CANO_RXN_SMILES", "Label",
                               "sequence_sha256"],
                              ascending=[True, True, False, True], kind="stable")
        sub = sub[cols].fillna("").astype("string")
        csv_p = cfg.S7_ROOT + f"/{split}.csv"
        pq_p = cfg.S7_ROOT + f"/{split}.parquet"
        sub.to_csv(csv_p, index=False, lineterminator="\n")
        sub.to_parquet(pq_p, index=False)
        # CSV/parquet row identity
        c1 = pd.read_csv(csv_p, dtype=str).fillna("")
        c2 = pd.read_parquet(pq_p).fillna("").astype(str)
        assert c1.reset_index(drop=True).equals(c2[list(c1.columns)].reset_index(drop=True))
        counts[split] = {
            "rows": int(len(sub)),
            "reactions": int(sub.CANO_RXN_SMILES.nunique()),
            "groups": int(sub.INTERNAL_SPLIT_GROUP.nunique()),
            "positive_rows": int((sub.Label == "1").sum()),
            "negative_rows": int((sub.Label == "0").sum()),
            "unique_uids": int(sub.UniprotID.nunique()),
            "unique_sequence_sha256": int(sub.sequence_sha256.nunique()),
            "csv_sha256": sha(csv_p), "parquet_sha256": sha(pq_p),
            "csv_rows_eq_parquet_rows": True,
        }

    # cross-split overlap audits
    def sets_for(split, col):
        return set(fz[fz.split == split][col])
    ovs = {}
    for a, b in [("train", "valid"), ("train", "test"), ("valid", "test")]:
        ovs[f"reaction_{a}_{b}"] = len(sets_for(a, "CANO_RXN_SMILES") & sets_for(b, "CANO_RXN_SMILES"))
        ovs[f"group_{a}_{b}"] = len(sets_for(a, "INTERNAL_SPLIT_GROUP") & sets_for(b, "INTERNAL_SPLIT_GROUP"))
        ovs[f"pair_{a}_{b}"] = len(set(zip(fz[fz.split == a].CANO_RXN_SMILES, fz[fz.split == a].sequence_sha256))
                                   & set(zip(fz[fz.split == b].CANO_RXN_SMILES, fz[fz.split == b].sequence_sha256)))
        ovs[f"uid_{a}_{b}"] = len(sets_for(a, "UniprotID") & sets_for(b, "UniprotID"))
        # exact reverse counterpart across splits: rxn in A whose reverse is in B
        ra = sets_for(a, "CANO_RXN_SMILES"); rb = sets_for(b, "CANO_RXN_SMILES")
        rev = 0
        for r in ra:
            l, _, rt = r.partition(">>")
            if rt + ">>" + l in rb:
                rev += 1
        ovs[f"reverse_counterpart_{a}_{b}"] = rev
    zero_keys = [k for k in ovs if not k.startswith("uid_")]
    bad = {k: ovs[k] for k in zero_keys if ovs[k] != 0}
    if bad:
        fail.append("SPLIT_OVERLAP=" + str(sorted(bad)))
    # union equals input, each row exactly once
    u = pd.concat([fz[fz.split == s][cols] for s in ("train", "valid", "test")])
    if len(u) != len(fz) or u.duplicated(list(cols)).sum() != 0:
        fail.append("SPLIT_UNION_MISMATCH")
    if fz.split.isna().any():
        fail.append("UNASSIGNED_SPLIT")

    fz[["CANO_RXN_SMILES", "INTERNAL_SPLIT_GROUP", "split"]].drop_duplicates()\
        .sort_values("CANO_RXN_SMILES").to_parquet(cfg.S7_ROOT + "/SPLIT_ASSIGNMENT.parquet", index=False)
    cfg.save_json({"groups_total": len(uniq), "train_groups": n_tr, "valid_groups": n_va,
                   "test_groups": len(uniq) - n_tr - n_va, "seed": SEED,
                   "ratio": "int(0.8)/int(0.1)/remainder by GROUP count",
                   "splits": counts, "failures_seen_by_producer": fail}, cfg.S7_ROOT + "/SPLIT_COUNTS.json")
    cfg.save_json({"cross_split_overlaps": ovs, "v6_gate": audit},
                  cfg.S7_ROOT + "/SPLIT_OVERLAP_AUDIT.json")
    cfg.save_json({"frozen_parquet": {"path": cfg.FROZEN_PARQUET, "sha256": sha(cfg.FROZEN_PARQUET)},
                   "frozen_csv": {"path": cfg.FROZEN_CSV, "sha256": sha(cfg.FROZEN_CSV)},
                   "v6_csv": {"path": cfg.V6_CSV, "sha256": sha(cfg.V6_CSV)},
                   "authority_script": {"path": cfg.AUTH_SCRIPT, "sha256": sha(cfg.AUTH_SCRIPT)},
                   "rows": len(fz)}, cfg.S7_ROOT + "/INPUT_IDENTITIES.json")
    if fail:
        print("PRODUCER_FAILURES:", fail)
        sys.exit(2)
    print("S7 producer OK: groups", len(uniq), "| rows", {s: counts[s]["rows"] for s in counts})


if __name__ == "__main__":
    main()
