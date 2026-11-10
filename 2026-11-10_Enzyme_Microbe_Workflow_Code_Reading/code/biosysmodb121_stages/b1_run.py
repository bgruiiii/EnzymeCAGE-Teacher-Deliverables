# -*- coding: utf-8 -*-
"""B1 part 1: step split (533), participant closure (2473), gold links
(1355/1349), organisms (STEP vs PATHWAY_COMPLETE), three reaction views,
frozen-cleaning parity on 298, REACTION_VIEW_AUDIT, complex flag scan.
Part 2 (crosswalk) is b1x_crosswalk.py; part 3 (coverage assembly) is at the
end of this file, executed only when the crosswalk file exists.
"""
import csv, importlib.util, json, os, re, sys, time
csv.field_size_limit(10 ** 9)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b121_common as C
import gates_authority as G

W = C.WORK
IN = C.INPUTS
OUT = None
CLEAN_SCRIPT = os.path.join(
    W, "tools/cleaning_payload/pollutant298_training_compatible_reactions_local_payload_20260922",
    "scripts/build_pollutant298_training_compatible_reactions.py")


def load_cleaning():
    spec = importlib.util.spec_from_file_location("p298_clean", CLEAN_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # module-level import only; main() is guarded
    return mod


def valid_smiles(s, Chem):
    if not s or not s.strip():
        return None
    try:
        m = Chem.MolFromSmiles(s)
    except Exception:
        return None
    return m is not None


def step1(cfg, out):
    global OUT
    OUT = out
    os.makedirs(out, exist_ok=True)
    cl = load_cleaning()
    Chem = cl.Chem
    sha_text = cl.sha256_text

    formal = C.read_tsv(os.path.join(IN, "G1_gold/formal_cases.tsv"))
    fset = {r["case_id"] for r in formal}
    rg = C.read_tsv(os.path.join(IN, "G1_gold/reaction_gold.tsv"))
    assert all(r["case_id"] in fset for r in rg)
    assert len(rg) == 2473
    # ---- participants (original rows + step index) ----
    steps = {}
    for i, r in enumerate(rg):
        k = (r["case_id"], r["step_occurrence_id"])
        steps.setdefault(k, []).append(i)
    assert len(steps) == 533
    with open(os.path.join(out, "step_participants.tsv"), "w", newline="",
              encoding="utf-8") as f:
        hdr = list(rg[0].keys()) + ["participant_ordinal_in_step"]
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(hdr)
        for k, idxs in steps.items():
            for o, i in enumerate(idxs):
                w.writerow([rg[i][c] for c in rg[0].keys()] + [o])

    # ---- raw compound structure recovery map ----
    rec = {}
    with open(os.path.join(IN, "raw/BIOSYSMOdb_Compounds_chemical_info_v1.0.csv"),
              newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        for row in rd:
            bid = row.get("BIOSYSMO ID", "").strip()
            iso = (row.get("isosmiles") or "").strip()
            can = (row.get("canonicalsmiles") or "").strip()
            if bid and bid not in rec:
                rec[bid] = (iso, can)

    # ---- lumped source reactions (multi-arrow Complete Name) ----
    lumped_r = set()
    rows_csv = list(csv.DictReader(open(os.path.join(
        IN, "raw/BIOSYSMOdb_Reactions_v1.0.csv"), newline="", encoding="utf-8-sig")))
    rrow_by_id = {}
    for row in rows_csv:
        rid = row.get("Reaction unique ID", "").strip()
        rrow_by_id[rid] = row
        nm = (row.get("Complete Name") or "") + " | " + (row.get("title") or "")
        if nm.count("->") >= 2:
            lumped_r.add(rid)

    # ---- per-step views ----
    def pick(r):
        """returns (smiles_used, stereo_note, source_marker) or (None, reason, None)"""
        iso = r["isosmiles"].strip()
        can = r["canonicalsmiles"].strip()
        if iso and valid_smiles(iso, Chem):
            return iso, "STEREO_AS_RECORDED", "G1_ISO"
        if can and valid_smiles(can, Chem):
            return can, "STEREO_MAYBE_LOST_CANONICAL_ONLY", "G1_CANONICAL"
        # try raw recovery by compound id
        got = rec.get(r["compound_id"].strip())
        if got:
            giso, gcan = got
            if giso and valid_smiles(giso, Chem):
                return giso, "STEREO_AS_RECORDED_RAW", "RAW_COMPOUNDS_INFO"
            if gcan and valid_smiles(gcan, Chem):
                return gcan, "STEREO_CANONICAL_RAW", "RAW_COMPOUNDS_INFO"
        if iso or can:
            return None, "UNPARSEABLE_STRUCTURE_RECORD", (iso or can)
        return None, "EMPTY_STRUCTURE_BOTH_FIELDS", ""

    audit_rows, uniq = [], {"raw_full": set(), "full_can": set(), "main": set(), "model": set()}
    collisions = {"full_can": {}, "model": {}}
    for k, idxs in sorted(steps.items()):
        case, step = k
        subs, prods, empty_ids, incomplete = [], [], [], []
        main_s, main_p = [], []
        roles = []
        for i in idxs:
            r = rg[i]
            sm, note, src = pick(r)
            side = "S" if r["participant_side"] == "SUBSTRATE" else "P"
            main_ok = (r["is_main_chain_candidate"] == "TRUE" and
                       r["s4r2_occurrence_mask"] == "FALSE")
            roles.append((r["compound_id"], r["role_label"], r["participant_side"],
                          sm is not None))
            if sm is None:
                empty_ids.append(f"{r['compound_id']}:{note}:{src}")
                incomplete.append((side, note))
                continue
            if side == "S":
                subs.append(sm)
                if main_ok:
                    main_s.append(sm)
            else:
                prods.append(sm)
                if main_ok:
                    main_p.append(sm)
        full_raw = ".".join(subs) + ">>" + ".".join(prods)
        uniq["raw_full"].add(full_raw)
        full_can = None
        if subs and prods and not incomplete:
            full_can = (".".join(sorted(Chem.MolToSmiles(Chem.MolFromSmiles(x))
                                        for x in subs)) + ">>" +
                        ".".join(sorted(Chem.MolToSmiles(Chem.MolFromSmiles(x))
                                        for x in prods)))
            uniq["full_can"].add(full_can)
            collisions["full_can"].setdefault(full_can, []).append(k)
        main_key = None
        if main_s and main_p:
            main_key = (".".join(main_s) + ">>" + ".".join(main_p))
            uniq["main"].add(main_key)
        model_key, status, reason = (None, "FULL_INCOMPLETE",
                                     ";".join(f"{s}:{n}" for s, n in incomplete))
        if incomplete and all(n == "EMPTY_STRUCTURE_BOTH_FIELDS" for _, n in incomplete):
            status = "FULL_EMPTY_STRUCTURE"
        if not subs or not prods:
            status = "NO_DIRECTIONAL_FULL"
        if full_can is not None:
            mk, st = cl.clean_reaction(full_raw)
            if mk is None:
                status = "HOLD"
                reason = st
            else:
                status = "CLEANED_MODEL_OK" if mk != full_raw else "CLEANED_MODEL_UNCHANGED"
                model_key = mk
                uniq["model"].add(model_key)
                collisions["model"].setdefault(model_key, []).append(k)
        rid = rg[idxs[0]]["reaction_id"]
        src = rrow_by_id.get(rid, {})
        audit_rows.append({
            "case_id": case, "step_occurrence_id": step,
            "reaction_id": rid,
            "gold_orientation": rg[idxs[0]]["gold_orientation"],
            "arrow_class": rg[idxs[0]]["arrow_class"],
            "n_participants": len(idxs),
            "full_raw": full_raw, "full_raw_sha256": sha_text(full_raw),
            "full_canonical": full_can or "", "full_canonical_sha256": sha_text(full_can) if full_can else "",
            "main_chain_view": main_key or "", "main_chain_sha256": sha_text(main_key) if main_key else "",
            "model_cleaned_full": model_key or "", "model_cleaned_sha256": sha_text(model_key) if model_key else "",
            "cleaning_status": status, "cleaning_or_incomplete_reason": reason,
            "missing_structure_participants": ";".join(empty_ids),
            "stereo_note_per_participant": "|".join(
                f"{rg[i]['compound_id']}:{pick(rg[i])[1] if pick(rg[i])[0] else 'NA'}" for i in idxs),
            "lumped_source_step": "TRUE" if rid in lumped_r else "FALSE",
            "source_reaction_complete_name": (src.get("Complete Name") or "")[:200],
            "source_kegg_id": src.get("KEGG-ID", ""), "source_eawag_id": src.get("EAWAG-ID", ""),
            "source_metacyc_id": src.get("MetaCyC-ID", ""),
            "structure_recovery_used": ";".join(
                f"{rg[i]['compound_id']}:{pick(rg[i])[2]}" for i in idxs if pick(rg[i])[2] == "RAW_COMPOUNDS_INFO"),
        })
    C.write_tsv(os.path.join(out, "REACTION_VIEW_AUDIT.tsv"), list(audit_rows[0].keys()), audit_rows)

    # ---- step_queries ----
    qcols = ["case_id", "pathway_id", "step_occurrence_id", "reaction_id",
             "linear_display_order", "topological_level", "branch_id",
             "predecessor_step_ids", "successor_step_ids", "gold_orientation",
             "arrow_class", "participant_count", "n_substrates", "n_products",
             "directed_reaction_smiles_full", "directed_reaction_smiles_main",
             "model_cleaned_full", "cleaning_status", "lumped_source_step"]
    qrows = []
    for a in audit_rows:
        first = rg[steps[(a["case_id"], a["step_occurrence_id"])][0]]
        nS = sum(1 for i in steps[(a["case_id"], a["step_occurrence_id"])]
                 if rg[i]["participant_side"] == "SUBSTRATE")
        qrows.append(dict(a, pathway_id=first["pathway_id"],
                          linear_display_order=first["linear_display_order"],
                          topological_level=first["topological_level"],
                          branch_id=first["branch_id"],
                          predecessor_step_ids=first["predecessor_step_ids"],
                          successor_step_ids=first["successor_step_ids"],
                          participant_count=a["n_participants"],
                          n_substrates=nS,
                          n_products=int(a["n_participants"]) - nS,
                          directed_reaction_smiles_full=a["full_raw"],
                          directed_reaction_smiles_main=a["main_chain_view"],
                          model_cleaned_full=a["model_cleaned_full"]))
    C.write_tsv(os.path.join(out, "step_queries.tsv"), qcols, qrows)

    # ---- gold enzyme links ----
    eg = C.read_tsv(os.path.join(IN, "G1_gold/enzyme_gold.tsv"))
    assert len(eg) == 1355
    links = {}
    for i, r in enumerate(eg):
        links.setdefault((r["case_id"], r["step_occurrence_id"], r["enzyme_id"]), []).append(i)
    dups = [{"case_id": k[0], "step_occurrence_id": k[1], "enzyme_id": k[2],
             "row_numbers_in_enzyme_gold": ";".join(str(i + 2) for i in v),
             "ec_raw": eg[v[0]]["ec_number_raw"], "rule": eg[v[0]]["rule"],
             "source_row_number": ";".join(eg[i]["source_row_number"] for i in v)}
            for k, v in links.items() if len(v) > 1]
    C.write_tsv(os.path.join(out, "STEP_GOLD_LINK_DUPLICATES.tsv"),
                list(dups[0].keys()) if dups else ["case_id", "step_occurrence_id", "enzyme_id"], dups)
    C.write_tsv(os.path.join(out, "step_gold_enzymes.tsv"),
                ["case_id", "pathway_id", "step_occurrence_id", "reaction_id", "enzyme_id",
                 "enzyme_name", "ec_number_raw", "ec_number_normalized", "eawag_enzyme_id",
                 "metacyc_enzyme_id", "mibpop_enzyme_id", "kegg_enzyme_id",
                 "sequence_availability", "rule", "license", "source_row_number"], eg)
    assert len(links) == 1349

    # ---- organisms ----
    og = C.read_tsv(os.path.join(IN, "G1_gold/organism_gold.tsv"))
    step_rows = [r for r in og if r["scope"] == "STEP"]
    pcw_rows = [r for r in og if r["scope"] == "PATHWAY_COMPLETE"]
    assert len(step_rows) == 1869 and len(pcw_rows) == 346
    C.write_tsv(os.path.join(out, "step_gold_organisms.tsv"),
                ["case_id", "pathway_id", "step_occurrence_id", "reaction_id", "enzyme_id",
                 "enzyme_name", "organism_name_raw", "organism_name_normalized",
                 "organism_match_status", "matched_organism_name", "taxid", "genome_id",
                 "kingdom", "download_available", "license", "source_row_number"], step_rows)
    C.write_json(os.path.join(out, "PATHWAY_COMPLETE_ORGANISMS.json"),
                 {"note": "kept separate; must not substitute STEP enzyme species",
                  "rows": pcw_rows})

    # ---- complex flag scan (438 = // or CPLX, audit-candidate flag only) ----
    flagged = [r for r in eg if "//" in r["enzyme_name"] or "CPLX" in r["metacyc_enzyme_id"]]
    C.write_json(os.path.join(out, "COMPLEX_FLAG_SCAN.json"),
                 {"flagged_rows": len(flagged),
                  "note": "flag only; per-source classification in COMPLEX_ROLE_AUDIT (crosswalk step)",
                  "cases": [{"enzyme_id": r["enzyme_id"], "name": r["enzyme_name"],
                             "metacyc": r["metacyc_enzyme_id"]} for r in flagged]})

    # ---- 298 cleaning parity ----
    audit298 = C.read_tsv(os.path.join(W, "tools/cleaning_payload/"
                "pollutant298_training_compatible_reactions_local_payload_20260922/outputs/"
                "POLLUTANT298_REACTION_CLEANING_AUDIT.tsv"))
    assert len(audit298) == 298
    mism, dist = [], {"CHANGED": 0, "UNCHANGED": 0, "HOLD": 0}
    for r in audit298:
        raw = r["source_canonical_directional"]
        exp = r["model_cano_rxn_smiles"]
        outp, st = cl.clean_reaction(raw)
        got = outp if outp is not None else None
        if r["cleaning_status"] == "HOLD":
            cls = "HOLD"
            ok = got is None
        elif raw == exp:
            cls = "UNCHANGED"
            ok = got == exp
        else:
            cls = "CHANGED"
            ok = got == exp
        dist[cls] += 1
        if not ok:
            mism.append(r["case_id"])
    parity = {"rows": len(audit298), "status_distribution": dist,
              "expected": G.PARITY_EXPECT, "mismatch_rows": mism,
              "rdkit_version": cl.rdBase.rdkitVersion,
              "cleaning_source_sha256": C.sha256_file(CLEAN_SCRIPT),
              "pass": (dist == {k: v for k, v in G.PARITY_EXPECT.items() if k != "TOTAL"}
                       and not mism)}
    C.write_json(os.path.join(out, "CLEANING_PARITY.json"), parity)

    # ---- uniques & collisions ----
    coll = {kk: {key: [f"{c}/{s}" for c, s in v] for key, v in d.items() if len(v) > 1}
            for kk, d in collisions.items()}
    C.write_json(os.path.join(out, "REACTION_UNIQUE_COUNTS.json"), {
        "source_reaction_ids_unique": len({r["reaction_id"] for r in rg}),
        "source_id_orientation_unique": len({(r["reaction_id"], r["gold_orientation"]) for r in rg}),
        "raw_full_directed_unique": len(uniq["raw_full"]),
        "full_canonical_unique": len(uniq["full_can"]),
        "main_chain_unique": len(uniq["main"]),
        "model_cleaned_unique": len(uniq["model"]),
        "steps_by_cleaning_status": {s: sum(1 for a in audit_rows if a["cleaning_status"] == s)
                                     for s in {a["cleaning_status"] for a in audit_rows}},
        "collision_groups_full_canonical": coll["full_can"],
        "collision_groups_model_cleaned": coll["model"],
        "lumped_source_steps": sum(1 for a in audit_rows if a["lumped_source_step"] == "TRUE"),
    })
    print("B1 part1 done: parity pass =", parity["pass"], "dist =", dist)
    return 0 if parity["pass"] else 3


def run(cfg, task_id, out, allow_nonempty=False):
    if os.environ.get("CUDA_VISIBLE_DEVICES", None) != "":
        C.die("CUDA_VISIBLE_DEVICES must be '' (CPU-only)")
    return step1(cfg, out)
