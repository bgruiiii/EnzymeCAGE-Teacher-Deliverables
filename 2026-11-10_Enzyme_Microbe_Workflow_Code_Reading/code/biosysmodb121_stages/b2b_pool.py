# -*- coding: utf-8 -*-
"""B2 part B: candidate pool freeze (from retrieval results + library direct
pairs ONLY), step funnel (all 533 typed), recall (before/after asset filter),
frozen case masks, train/valid/test overlap, asset demand inventory.
Gold connects only AFTER the pool freeze. CPU-only."""
import csv, glob, hashlib, json, os, pickle, subprocess, sys, time

csv.field_size_limit(10 ** 9)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b121_common as C
import pandas as pd

W = C.WORK
RUN = "/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922"
R1 = os.path.join(RUN, "s11_r1_self_included_four_model_20260927")
R0 = os.path.join(W, "tools/r0_census/enzymecage_pollutant_biodegradation_category_capacity_census_r0_20260920")
B1 = os.path.join(W, "B1")
B2 = os.path.join(W, "B2")
PHASE = sys.argv[1] if len(sys.argv) > 1 else "freeze"
LOG = []


def log(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    LOG.append(line)


def sha256s(x):
    return hashlib.sha256(x.encode()).hexdigest()


def load_retrieval():
    import gzip
    res = {}
    for fn in glob.glob(os.path.join(B2, "retrieval", "*.json.gz")):
        rec = json.load(gzip.open(fn, "rt", encoding="utf-8"))
        res[rec["model_key"]] = rec
    return res


def rev_key(s):
    p = s.split(">>")
    if len(p) != 2:
        return None
    return ".".join(sorted(p[1].split("."))) + ">>" + ".".join(sorted(p[0].split(".")))


def main():
    if os.environ.get("CUDA_VISIBLE_DEVICES", None) != "":
        C.die("CUDA_VISIBLE_DEVICES must be ''")
    os.makedirs(B2, exist_ok=True)
    mp = pd.read_parquet(os.path.join(R0, "01_funnel", "REACTION_MASTER_POOL.parquet"))
    ps = pd.read_parquet(os.path.join(R0, "01_funnel", "ALL_SCIENTIFIC_PAIRS.parquet"))
    # index: reaction cd -> direct pairs (all members of library)
    cd2pairs = {}
    for row in ps[["global_reaction_id", "canonical_directional", "sequence_sha256",
                   "canonical_protein_id", "accessions", "source_datasets",
                   "evidence_tiers", "record_ids", "scientific_pair_ok"]].itertuples():
        cd2pairs.setdefault(row.canonical_directional, []).append(
            (row.sequence_sha256, row.canonical_protein_id, row.accessions,
             row.source_datasets, row.evidence_tiers, str(row.record_ids),
            bool(row.scientific_pair_ok)))
    uk_of = dict(zip(mp.canonical_directional,
                     mp.chemistry_equivalence_undirected_key))
    # group members map (same reaction dup + reverse equivalence)
    uk_members = {}
    for cd, u in uk_of.items():
        if isinstance(u, str):
            uk_members.setdefault(u, set()).add(cd)

    retr = load_retrieval()
    sq = C.read_tsv(os.path.join(B1, "step_queries.tsv"))
    audit = {r["case_id"] + "/" + r["step_occurrence_id"]: r
             for r in C.read_tsv(os.path.join(B1, "REACTION_VIEW_AUDIT.tsv"))}
    log("retrieval shards:", len(retr), "steps:", len(sq))
    C.write_json(os.path.join(B2, "R0_IDENTITIES.json"), {
        "archive": C.sha256_file(os.path.join(C.RET,
            "enzymecage_pollutant_biodegradation_category_capacity_census_r0_20260920.tar.gz")) +
            " @ " + os.path.join(C.RET,
            "enzymecage_pollutant_biodegradation_category_capacity_census_r0_20260920.tar.gz"),
        "master_parquet": [os.path.join(R0, "01_funnel", "REACTION_MASTER_POOL.parquet"),
                           len(mp), C.sha256_file(os.path.join(R0, "01_funnel", "REACTION_MASTER_POOL.parquet"))],
        "pairs_parquet": [os.path.join(R0, "01_funnel", "ALL_SCIENTIFIC_PAIRS.parquet"),
                          len(ps), C.sha256_file(os.path.join(R0, "01_funnel", "ALL_SCIENTIFIC_PAIRS.parquet"))],
        "frozen_counts_match": (len(mp) == 29061 and len(ps) == 292582),
    })

    top_rows, pool_rows, prov_rows = [], [], []
    step_pool_size = {}
    pool_by_step = {}
    for q in sq:
        key = (q["case_id"], q["step_occurrence_id"])
        mk = q["model_cleaned_full"]
        rec = retr.get(mk) if mk else None
        status = q["cleaning_status"]
        if rec is None:
            top_rows.append({"case_id": key[0], "step_occurrence_id": key[1], "rank": "",
                             "reference_cd": "", "similarity": "", "exact_same_direction": "",
                             "undirected_key": "", "group_size": 0, "group_cds": "",
                             "pool_seq_count": 0,
                             "reason": ("NO_MODEL_KEY:" + status if not mk
                                        else "QUERY_REPRESENTATION_FAILED")})
            step_pool_size[key] = 0
            continue
        pool_shas = set()
        pool_by_step[key] = pool_shas
        for i, ref in enumerate(rec["references"]):
            grp = set(ref["group_cds"])
            members = sorted((grp | uk_members.get(ref["uk"], set())) if ref["uk"] else grp)
            for cd in members:
                for tup in cd2pairs.get(cd, []):
                    if not tup[6]:
                        continue
                    pool_shas.add(tup[0])
                    pool_rows.append({"case_id": key[0], "step_occurrence_id": key[1],
                                      "rank": i + 1, "reference_cd": ref["cd"],
                                      "group_cd": cd, "sequence_sha256": tup[0],
                                      "canonical_protein_id": tup[1], "accessions": tup[2],
                                      "source_datasets": tup[3], "evidence_tiers": tup[4],
                                      "exact_same_direction": ref["exact_same_direction"]})
            top_rows.append({"case_id": key[0], "step_occurrence_id": key[1], "rank": i + 1,
                             "reference_cd": ref["cd"], "similarity": ref["score"],
                             "exact_same_direction": ref["exact_same_direction"],
                             "undirected_key": ref["uk"], "group_size": len(members),
                             "group_cds": ";".join(members),
                             "pool_seq_count": len(pool_shas), "reason": ""})
        step_pool_size[key] = len(pool_shas)
        prov_rows.append({"case_id": key[0], "step_occurrence_id": key[1],
                          "planned_seqs": len(pool_shas),
                          "exact_rank1": "TRUE" if rec["references"] and rec["references"][0]["exact_same_direction"] else "FALSE"})
    C.write_tsv(os.path.join(B2, "TOP10_BASE.tsv"),
                ["case_id", "step_occurrence_id", "rank", "reference_cd", "similarity",
                 "exact_same_direction", "undirected_key", "group_size", "group_cds",
                 "pool_seq_count", "reason"],
                top_rows)
    df_pool = pd.DataFrame(pool_rows)
    df_pool.to_parquet(os.path.join(B2, "PLANNED_POOL_BASE.parquet"), index=False)
    C.write_tsv(os.path.join(B2, "CANDIDATE_PROVENANCE_BASE.tsv"),
                ["case_id", "step_occurrence_id", "planned_seqs", "exact_rank1"], prov_rows)
    log("pool rows", len(df_pool), "unique shas", df_pool.sequence_sha256.nunique() if len(df_pool) else 0)

    # ---------- gold (connect after freeze) ----------
    cw = C.read_tsv(os.path.join(B1, "enzyme_sequence_crosswalk.tsv"))
    STRICT = {"RESOLVED_SINGLE", "RESOLVED_MULTIPLE_DIRECT"}
    seqs_map = C.read_json(os.path.join(B1, "resolved_strict_sequences.json"))["sequences"]
    gold_shas = {}
    step_gold_status = {}
    for r in cw:
        k = (r["case_id"], r["step_occurrence_id"])
        if r["mapping_status"] in STRICT:
            shas = set()
            accs = r["source_accession_or_isoform"]
            if accs.startswith("MULTI:"):
                for a in accs[6:].split(";"):
                    if a in seqs_map:
                        shas.add(sha256s(seqs_map[a]))
            elif r["sequence_sha256"]:
                shas.add(r["sequence_sha256"])
            gold_shas.setdefault(k, set()).update(shas)
        d = step_gold_status.setdefault(k, [0, 0])
        d[0] += 1
        if r["mapping_status"] in STRICT:
            d[1] += 1

    pair_shas_all = set(ps.sequence_sha256)
    funnel, recall = [], {
        "steps_total": 533, "gold_resolved_steps": 0, "gold_complete_steps": 0,
        "gold_partial_steps": 0, "query_exact_in_R0_steps": 0, "query_not_in_R0_steps": 0,
        "assessable_resolved_steps": 0, "any_gold_in_planned_pool": 0,
        "resolved_gold_micro": 0, "gold_seq_in_pool_micro": 0,
        "gold_sequence_has_any_R0_pair": 0, "gold_present_in_top10_pool": 0,
        "gold_seq_library_absent_steps": 0, "gold_seq_library_present_not_retrieved_steps": 0,
        "any_gold_after_common_asset_filter": 0}
    exact_rank1_keys = set()
    for r in prov_rows:
        if r["exact_rank1"] == "TRUE":
            exact_rank1_keys.add((r["case_id"], r["step_occurrence_id"]))
    for q in sq:
        k = (q["case_id"], q["step_occurrence_id"])
        gst = step_gold_status.get(k, [0, 0])
        g = gold_shas.get(k, set())
        pool = pool_by_step.get(k, set())
        has_pool = step_pool_size.get(k, 0) > 0
        row = {"case_id": k[0], "step_occurrence_id": k[1],
               "cleaning_status": q["cleaning_status"],
               "model_key_present": "TRUE" if q["model_cleaned_full"] else "FALSE",
               "query_exact_in_R0": "TRUE" if k in exact_rank1_keys else "FALSE",
               "gold_records": gst[0], "gold_strict_records": gst[1],
               "gold_seq_shas": ";".join(sorted(g))[:400],
               "planned_pool_seqs": step_pool_size.get(k, 0),
               "gold_in_pool": "-", "gold_lib_has_any_pair": "-",
               "gold_after_asset_filter": "-", "status": ""}
        if q["cleaning_status"] in ("FULL_EMPTY_STRUCTURE", "HOLD", "FULL_INCOMPLETE",
                                    "NO_DIRECTIONAL_FULL") or not q["model_cleaned_full"]:
            row["status"] = "NO_QUERY_REPRESENTATION"
        elif not gst[1]:
            row["status"] = "GOLD_NOT_RESOLVED"
        elif not has_pool:
            row["status"] = "EMPTY_POOL"
            if g:
                row["gold_in_pool"] = "FALSE"
                row["gold_lib_has_any_pair"] = str(bool(g & pair_shas_all)).upper()
            recall["assessable_resolved_steps"] += 1
        else:
            row["status"] = "POOL_READY"
        if g and has_pool:
            row["gold_in_pool"] = "TRUE" if g & pool else "FALSE"
            row["gold_lib_has_any_pair"] = str(bool(g & pair_shas_all)).upper()
            if k not in exact_rank1_keys:
                pass
        funnel.append(row)
    # aggregate
    for q in sq:
        k = (q["case_id"], q["step_occurrence_id"])
        f = next(x for x in funnel if (x["case_id"], x["step_occurrence_id"]) == k)
        g = gold_shas.get(k, set())
        if g:
            recall["gold_resolved_steps"] += 1
        if f["gold_records"] and f["gold_strict_records"] == f["gold_records"]:
            recall["gold_complete_steps"] += 1
        elif g:
            recall["gold_partial_steps"] += 1
        if f["query_exact_in_R0"] == "TRUE":
            recall["query_exact_in_R0_steps"] += 1
        elif f["model_key_present"] == "TRUE":
            recall["query_not_in_R0_steps"] += 1
    for f in funnel:
        k = (f["case_id"], f["step_occurrence_id"])
        g = gold_shas.get(k, set())
        if not g:
            continue
        recall["assessable_resolved_steps"] += 1
        recall["resolved_gold_micro"] += len(g)
        pool = pool_by_step.get(k, set())
        in_pool = g & pool
        recall["gold_seq_in_pool_micro"] += len(in_pool)
        if in_pool:
            recall["any_gold_in_planned_pool"] += 1
        recall["gold_sequence_has_any_R0_pair"] += len(g & pair_shas_all)
        recall["gold_present_in_top10_pool"] += len(in_pool)
        if g and not (g & pair_shas_all):
            recall["gold_seq_library_absent_steps"] += 1
        elif g and (g & pair_shas_all) and not in_pool:
            recall["gold_seq_library_present_not_retrieved_steps"] += 1
    recall["macro_any_gold_in_pool"] = (recall["any_gold_in_planned_pool"] /
                                        recall["assessable_resolved_steps"]) if recall["assessable_resolved_steps"] else 0
    recall["micro_gold_seq_coverage"] = (recall["gold_seq_in_pool_micro"] /
                                         recall["resolved_gold_micro"]) if recall["resolved_gold_micro"] else 0
    C.write_json(os.path.join(B2, "RECALL_BASE.json"), recall)
    C.write_tsv(os.path.join(B2, "STEP_FUNNEL_ALL533.tsv"), list(funnel[0].keys()), funnel)

    # ---------- training overlap + masks ----------
    log("loading splits…")
    splits = {}
    for gen, files in [("old", {"train": "/usrdata/EnzymeCAGE_data/formal_splits/formal_filtered_train.csv",
                               "valid": "/usrdata/EnzymeCAGE_data/formal_splits/formal_filtered_valid.csv",
                               "test": "/usrdata/EnzymeCAGE_data/formal_splits/formal_filtered_test.csv"}),
                      ("new", {"train": RUN + "/07_splits_reaction_group_20260924/train.csv",
                              "valid": RUN + "/07_splits_reaction_group_20260924/valid.csv",
                              "test": RUN + "/07_splits_reaction_group_20260924/test.csv"})]:
        for part, p in files.items():
            df = pd.read_csv(p, usecols=["CANO_RXN_SMILES", "sequence_sha256", "Label"]
                             if gen == "new" else ["CANO_RXN_SMILES", "sequence", "Label"])
            if gen == "new":
                d = {"cano": df["CANO_RXN_SMILES"], "seqsha": df["sequence_sha256"],
                     "label": df["Label"]}
            else:
                d = {"cano": df["CANO_RXN_SMILES"],
                     "seqsha": df["sequence"].map(sha256s), "label": df["Label"]}
            key2rows = {}
            for i, cn in enumerate(d["cano"]):
                key2rows.setdefault(cn, []).append(i + 2)
            pos_pairs = set(zip(d["cano"], d["seqsha"])) if False else None
            pos1 = set()
            pos_rows = d["label"] == 1
            for cn, sh in zip(d["cano"][pos_rows], d["seqsha"][pos_rows]):
                pos1.add((cn, sh))
            seqs_in = set(d["seqsha"])
            rev2rows = {}
            for cn in key2rows:
                rv = rev_key(cn)
                if rv:
                    rev2rows.setdefault(rv, []).extend(key2rows[cn])
            splits[f"{gen}_{part}"] = {"key2rows": key2rows, "rev2rows": rev2rows,
                                       "pos_pairs": pos1, "seqs": seqs_in, "rows": len(df)}
            log(gen, part, len(df))

    # full canonical & model key per step (from audit)
    overlap_rows = []
    masks = {"ALL533": [], "NO_RAW_SAME_TRAIN": [], "NO_MODEL_SAME_OR_REVERSE_TRAIN": [],
             "NO_MODEL_SAME_OR_REVERSE_TRAIN_VALID": []}
    for q in sq:
        k = (q["case_id"], q["step_occurrence_id"])
        a = audit[f"{k[0]}/{k[1]}"]
        fc = a["full_canonical"]; mk = a["model_cleaned_full"]
        rfc = rev_key(fc) if fc else None
        rmk = rev_key(mk) if mk else None
        rec = {"case_id": k[0], "step_occurrence_id": k[1],
               "raw_same": "", "raw_reverse": "", "model_same": "", "model_reverse": "",
               "raw_row_ids": "", "model_row_ids": "", "gold_seq_in_train_pair": "",
               "candidate_seq_train_pair_hits": ""}
        g = gold_shas.get(k, set())
        gp = set()
        cp = pool_by_step.get(k, set())
        cp2 = set()
        raw_same_tr = raw_any = mdl_tr = mdl_tv = False
        for name, sp in sorted(splits.items()):
            gen, part = name.split("_")
            for s, field in ((fc, "raw_same"), (rfc, "raw_reverse"),
                             (mk, "model_same"), (rmk, "model_reverse")):
                if not s:
                    continue
                tbl = sp["rev2rows"] if field.endswith("reverse") else sp["key2rows"]
                if s in tbl:
                    rids = tbl[s][:3]
                    rec[field] += (";" if rec[field] else "") + name
                    idf = "raw_row_ids" if field.startswith("raw") else "model_row_ids"
                    rec[idf] += (name + "#" + ",".join(map(str, rids)) + " ")
                    if field == "raw_same" and part == "train":
                        raw_same_tr = True
                    if field.startswith("raw"):
                        raw_any = True
                    if field.startswith("model") and part == "train":
                        mdl_tr = True
                    if field.startswith("model") and part in ("train", "valid"):
                        mdl_tv = True
            if mk:
                gp |= {sh for sh in g if (mk, sh) in sp["pos_pairs"] and part == "train"}
                cp2 |= {sh for sh in cp if (mk, sh) in sp["pos_pairs"] and part == "train"}
        rec["gold_seq_in_train_pair"] = "TRUE" if gp else ("FALSE" if g else "-")
        rec["candidate_seq_train_pair_hits"] = len(cp2)
        overlap_rows.append(rec)
        masks["ALL533"].append(k)
        if not raw_same_tr:
            masks["NO_RAW_SAME_TRAIN"].append(k)
        if not mdl_tr:
            masks["NO_MODEL_SAME_OR_REVERSE_TRAIN"].append(k)
        if not mdl_tv:
            masks["NO_MODEL_SAME_OR_REVERSE_TRAIN_VALID"].append(k)
    C.write_tsv(os.path.join(B2, "TRAIN_OVERLAP.tsv"), list(overlap_rows[0].keys()), overlap_rows)
    C.write_tsv(os.path.join(B2, "FROZEN_CASE_MASKS.tsv"),
                ["mask", "case_id", "step_occurrence_id"],
                [{"mask": m, "case_id": c, "step_occurrence_id": s}
                 for m, lst in masks.items() for c, s in lst])
    C.write_json(os.path.join(B2, "MASK_COUNTS.json"),
                 {m: len(v) for m, v in masks.items()})

    C.write_json(os.path.join(B2, "SPLIT_STATS.json"),
                 {k: {"rows": v["rows"], "keys": len(v["key2rows"]),
                      "pos_pairs": len(v["pos_pairs"]), "seqs": len(v["seqs"])}
                  for k, v in splits.items()})
    with open(os.path.join(B2, "b2b_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")
    log("B2 part B done")


if __name__ == "__main__":
    main()
