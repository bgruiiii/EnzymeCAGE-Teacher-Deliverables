# -*- coding: utf-8 -*-
"""B2 part C: asset demand inventory (READ-ONLY; no feature generation).
For every planned candidate sequence SHA and every strict gold sequence SHA,
check presence in each of the three model arms' existing frozen stores.
Key sets are extracted once and cached under B2/asset_keys/.
"""
import glob, hashlib, json, os, pickle, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b121_common as C
import pandas as pd
import torch

W = C.WORK
RUN = "/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922"
R1 = os.path.join(RUN, "s11_r1_self_included_four_model_20260927")
F = "/usrdata/EnzymeCAGE_data/feature/protein"
B2 = os.path.join(W, "B2")
AK = os.path.join(B2, "asset_keys")
os.makedirs(AK, exist_ok=True)
HEX64 = set("0123456789abcdef")


def is_sha(k):
    return isinstance(k, str) and len(k) == 64 and all(ch in HEX64 for ch in k)


def load_keys(name, opener):
    cache = os.path.join(AK, name + ".txt")
    if os.path.isfile(cache):
        return set(open(cache).read().split())
    ks = opener()
    with open(cache, "w") as f:
        f.write("\n".join(sorted(ks)) + "\n")
    return ks


def sha_of(k, key_is_seq):
    return k if is_sha(k) else (hashlib.sha256(k.encode()).hexdigest() if key_is_seq else k)


def dict_keys_union(paths, tag):
    def op():
        s = set()
        for p in paths:
            if not os.path.isfile(p):
                continue
            d = pickle.load(open(p, "rb"))
            s.update(sha_of(k, False) for k in d.keys())
        return s
    return load_keys(tag, op)


def pt_uid_keys(paths, tag):
    def op():
        s = set()
        for p in paths:
            if not os.path.isfile(p):
                continue
            d = None
            try:
                d = torch.load(p, map_location="cpu", weights_only=False)
            except Exception:
                try:
                    d = pickle.load(open(p, "rb"))
                except Exception:
                    continue
            if not isinstance(d, dict):
                continue
            if "__format__" in d and "manifest_path" in d:
                mp = d["manifest_path"]
                if not os.path.isabs(mp):
                    mp = os.path.join(os.path.dirname(p), mp)
                if os.path.isfile(mp):
                    m = json.load(open(mp))
                    s.update(str(k) for k in (m.get("uid_to_shard") or m.get("keys") or {}))
                continue
            s.update(str(k) for k in d.keys())
        return s
    return load_keys(tag, op)


def main():
    if os.environ.get("CUDA_VISIBLE_DEVICES", None) != "":
        C.die("CUDA_VISIBLE_DEVICES must be ''")
    pool = pd.read_parquet(os.path.join(B2, "PLANNED_POOL_BASE.parquet"))
    uni = pool.groupby("sequence_sha256")["case_id"].count()
    log = {}

    # ---- global PLM stores keyed by sequence or sha ----
    def gl(paths, tag):
        def op():
            s = set()
            for p in paths:
                if not os.path.isfile(p):
                    continue
                d = pickle.load(open(p, "rb"))
                for k in d.keys():
                    s.add(k if is_sha(k) else hashlib.sha256(k.encode()).hexdigest())
            return s
        return load_keys(tag, op)

    eg_paths = [os.path.join(RUN, "04_plm_assets", "enzgfm", "merged", "protein_level", "seq2feature.pkl"),
                os.path.join(R1, "assets", "enzgfm", "merged_main", "protein_level", "seq2feature.pkl"),
                os.path.join(R1, "assets", "enzgfm", "merged_supp", "protein_level", "seq2feature.pkl"),
                os.path.join(R1, "assets", "enzgfm", "merged_supp2", "protein_level", "seq2feature.pkl")]
    enzgfm_g = gl(eg_paths, "enzgfm_global_sha")
    b3_paths = [os.path.join(F, "ESM2_3B_corrected_107705", "protein_level", "seq2feature.pkl")]
    b3_paths += glob.glob(os.path.join(F, "ESM2_3B_corrected_107705", "protein_level", "*.pkl"))
    b3_g = gl(sorted(set(b3_paths)), "legacy3b_global_sha")
    e6_paths = [os.path.join(F, "ESM-C_600M_baseline_1152_round1_20260708", "protein_level", "seq2feature.pkl")]
    e6_paths += glob.glob(os.path.join(F, "ESM-C_600M_baseline_1152_round1_20260708", "protein_level", "*.pkl"))
    e6_g = gl(sorted(set(e6_paths)), "legacy600m_global_sha")

    # ---- pocket/uid-keyed stores ----
    b3_p = pt_uid_keys(glob.glob(os.path.join(F, "ESM2_3B_corrected_107705", "pocket_node_feature", "*.pt")),
                       "legacy3b_pocket_uid")
    # legacy 600M = 1152 baseline compact-pocket store (NOT the corrected
    # store, which belongs to the new 600M arm per contract §4.1)
    e6_p = pt_uid_keys(glob.glob(os.path.join(
        F, "ESM-C_600M_baseline_1152_round1_20260708", "pocket_node_feature", "*.pt")),
        "legacy600m_pocket_uid")
    eg_p = pt_uid_keys([os.path.join(RUN, "04_plm_assets", "enzgfm", "merged", "pocket_node_feature", "enzgfm_node_feature.torch.pt")] +
                       [os.path.join(R1, "assets", "enzgfm", f"merged_{x}", "pocket_node_feature", "enzgfm_node_feature.torch.pt")
                        for x in ("main", "supp", "supp2")],
                       "enzgfm_pocket_uid")
    gvp = pt_uid_keys([os.path.join(F, "gvp", "gvp_protein_feature_flat.pt")], "gvp_uid")

    # ---- structure bundle dirs ----
    def dir_names(base):
        return set(os.listdir(base)) if os.path.isdir(base) else set()
    struct = dir_names("/usrdata/EnzymeCAGE_data/workspaces/p291_alphafill_20260922/bundles") | \
        dir_names("/usrdata/EnzymeCAGE_data/pollutant298_original_only_dual_3b_600m_4gpu_20260921/protein/staged_assets")

    # ---- accession map for planned shas ----
    acc_by_sha = {}
    for row in pool[["sequence_sha256", "canonical_protein_id"]].drop_duplicates().itertuples():
        acc_by_sha.setdefault(row.sequence_sha256, row.canonical_protein_id)

    rows = []
    tot = {"planned": 0}
    arms = ["enzgfm_global", "enzgfm_pocket", "legacy3b_global", "legacy3b_pocket",
            "legacy600m_global", "legacy600m_pocket", "gvp", "structure"]
    cov = {a: 0 for a in arms}
    any_all = 0
    for sha, nsteps in uni.items():
        acc = acc_by_sha.get(sha, "")
        inb = {"enzgfm_global": sha in enzgfm_g, "enzgfm_pocket": acc in eg_p,
               "legacy3b_global": sha in b3_g, "legacy3b_pocket": acc in b3_p,
               "legacy600m_global": sha in e6_g, "legacy600m_pocket": acc in e6_p,
               "gvp": acc in gvp, "structure": acc in struct}
        if all(inb[a] for a in arms):
            any_all += 1
        for a in arms:
            if inb[a]:
                cov[a] += 1
        tot["planned"] += 1
        rows.append(dict(sequence_sha256=sha, canonical_protein_id=acc,
                         steps_using=int(nsteps), **{("has_" + a): str(inb[a]).upper() for a in arms}))
    C.write_tsv(os.path.join(B2, "ASSET_DEMAND.tsv"),
                ["sequence_sha256", "canonical_protein_id", "steps_using"] +
                ["has_" + a for a in arms], rows)

    # gold sequences inventory
    gseq = C.read_json(os.path.join(B1 := os.path.join(W, "B1"),
                                    "resolved_strict_sequences.json"))["sequences"]
    gold_rows, gcov = [], {a: 0 for a in arms}
    for acc, seq in gseq.items():
        sha = hashlib.sha256(seq.encode()).hexdigest()
        inb = {"enzgfm_global": sha in enzgfm_g, "enzgfm_pocket": acc in eg_p,
               "legacy3b_global": sha in b3_g, "legacy3b_pocket": acc in b3_p,
               "legacy600m_global": sha in e6_g, "legacy600m_pocket": acc in e6_p,
               "gvp": acc in gvp, "structure": acc in struct}
        for a in arms:
            if inb[a]:
                gcov[a] += 1
        gold_rows.append(dict(accession=acc, sequence_sha256=sha,
                              **{("has_" + a): str(inb[a]).upper() for a in arms}))
    C.write_tsv(os.path.join(B2, "ASSET_DEMAND_GOLD.tsv"),
                ["accession", "sequence_sha256"] + ["has_" + a for a in arms], gold_rows)

    plan = {
        "planned_unique_sequences": tot["planned"],
        "planned_cross_all_8_flags": any_all,
        "planned_coverage_by_asset": cov,
        "gold_unique_accessions": len(gseq),
        "gold_coverage_by_asset": gcov,
        "max_pool": int(uni.max()) if len(uni) else 0,
        "note": "coverage judged against existing frozen stores read-only; "
                "pocket/gvp/structure keyed by canonical protein id; global PLM by sequence sha",
    }
    C.write_json(os.path.join(B2, "ASSET_INVENTORY_SUMMARY.json"), plan)
    print("ASSET DEMAND:", json.dumps(plan, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
