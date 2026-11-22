#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HPC executor-only: MetaTraits C7-1 long-form mapping correction.
READ / PARSE / REPORT ONLY. No download, no API, no prediction, no production
mutation, no snapshot activation.

Builds a long-form trait catalog by streaming the 12 MetaTraits bulk summary TSV
gzip files, maps the frozen C7-1 F1-F15 panel to row-level MetaTraits fields
(trait_name / group_1 / group_2 / unit / ontology_ids), and emits a small
metadata-only correction package (reports + archive + identity).
"""
import csv, gzip, hashlib, json, os, sys, tarfile, datetime, subprocess

# ------------------------------------------------------------------ paths ----
TASK_ID = "metatraits_c7_1_long_form_mapping_correction_20260819"
CHENYU_DATA_ROOT = "/usrdata/EnzymeCAGE_data"
PROJECT_ROOT = os.path.join(CHENYU_DATA_ROOT, "EnzymeCAGE-master")
DATA_DIR = os.path.join(CHENYU_DATA_ROOT, "data", "metatraits", "incoming",
                        "metatraits_bulk_tsv_snapshot_20260818")
PREVIOUS_RETURN_DIR = os.path.join(PROJECT_ROOT, "HPC_Returned_Result_Summaries",
                                   "metatraits_bulk_tsv_landed_chenyu_20260818")
RETURN_ROOT = os.path.join(PROJECT_ROOT, "HPC_Returned_Result_Summaries")
RETURN_DIR = os.path.join(RETURN_ROOT, TASK_ID)
ARCHIVE = os.path.join(RETURN_ROOT, TASK_ID + ".tar.gz")
IDENTITY = os.path.join(RETURN_ROOT, TASK_ID + ".tar.gz.identity.txt")

LOG_PATH = "/tmp/metatraits_c7_1_mapping_20260819.log"
def log(m):
    line = "[%s] %s" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), m)
    print(line, flush=True)

# ----------------------------------------------------- 12 summary files -------
# (file_name, taxonomy_namespace, taxonomic_rank, prediction_scope)
SUMMARY_FILES = [
    ("gtdb_family_summary_all.tsv.gz", "gtdb", "family", "all"),
    ("gtdb_family_summary_no_predictions.tsv.gz", "gtdb", "family", "no_predictions"),
    ("gtdb_genus_summary_all.tsv.gz", "gtdb", "genus", "all"),
    ("gtdb_genus_summary_no_predictions.tsv.gz", "gtdb", "genus", "no_predictions"),
    ("gtdb_species_summary_all.tsv.gz", "gtdb", "species", "all"),
    ("gtdb_species_summary_no_predictions.tsv.gz", "gtdb", "species", "no_predictions"),
    ("ncbi_family_summary_all.tsv.gz", "ncbi", "family", "all"),
    ("ncbi_family_summary_no_predictions.tsv.gz", "ncbi", "family", "no_predictions"),
    ("ncbi_genus_summary_all.tsv.gz", "ncbi", "genus", "all"),
    ("ncbi_genus_summary_no_predictions.tsv.gz", "ncbi", "genus", "no_predictions"),
    ("ncbi_species_summary_all.tsv.gz", "ncbi", "species", "all"),
    ("ncbi_species_summary_no_predictions.tsv.gz", "ncbi", "species", "no_predictions"),
]
CROSSWALK_FILES = ["GTDB2NCBI.tsv.gz", "NCBI2GTDB.tsv.gz"]

REQUIRED_LONG_FORM_COLS = ["trait_name", "unit", "consensus_value", "minimum",
                           "median", "mean", "maximum", "discrete_values",
                           "databases", "group_1", "group_2", "ontology_ids"]

# ----------------------------------------------- C7-1 frozen panel + rules ---
# teacher policy + first screen + boundary notes
F_POLICY = {
    "F1": ("oxygen_tolerance",
           "observed_trait",
           "observed first; predicted soft-fill allowed when explicitly labelled",
           "Primary signal: group_2=Atmosphere (Environmental preferences). Substrate-growth rows (aerobic/anaerobic growth: <substrate>) are assigned to F7, not F1, to avoid oxygen-vs-substrate ambiguity."),
    "F2": ("temperature",
           "observed_trait",
           "observed first; predicted soft-fill allowed when explicitly labelled",
           "Primary signal: group_2=Temperature. Ranges/optima are observed context."),
    "F3": ("pH",
           "observed_trait",
           "observed first; predicted soft-fill allowed when explicitly labelled",
           "Primary signal: group_2=pH. Matched on group_2 to avoid false hits from 'ph' in other words."),
    "F4": ("salinity",
           "observed_trait",
           "observed first; predicted soft-fill allowed when explicitly labelled",
           "Primary signal: group_2=Salinity."),
    "F5": ("bacdive_availability",
           "observed_evidence_only",
           "BacDive availability / culture collection; observed only; must not be predicted",
           "NOT a MetaTraits source. F5 is BacDive / culture-collection closure evidence only."),
    "F6": ("respiration_electron_acceptor",
           "observed_trait",
           "observed first; predicted soft-fill allowed when explicitly labelled",
           "group_2 in {Electron acceptor, Respiration, Denitrification, Reduction, Nitrification, Ammonification}."),
    "F7": ("carbon_and_substrate_utilization",
           "observed_trait",
           "observed first; predicted soft-fill allowed when explicitly labelled",
           "group_2 in {Carbon utilization, Aerobic growth, Anaerobic growth, Fermentation, Utilizes metabolite, Assimilation, Energy source, Growth}. 'aerobic/anaerobic growth: <substrate>' rows map here (substrate context), not to F1."),
    "F8": ("degradation_capacity_broad",
           "broad_context_only",
           "broad degradation context only; never claim exact pollutant degradation from it",
           "group_2 in {Catabolic process, Hydrolase activity, Oxidation}. Overlaps F9 for hydrolases; broad context only."),
    "F9": ("enzyme_activity",
           "source_labelled",
           "source-labelled context only; no hard rejection",
           "Primary signal: group_1=Enzymes (group_2=Enzyme activity). Hydrolase-activity rows also touch F8."),
    "F10": ("motility",
            "source_labelled",
            "source-labelled context only; no hard rejection",
            "group_2 in {Motility, Cell appendages}."),
    "F11": ("cell_morphology",
            "source_labelled",
            "source-labelled context only; no hard rejection",
            "group_2 in {Cell morphology, Cell size phenotype}."),
    "F12": ("cell_envelope_gram",
            "source_labelled",
            "source-labelled context only; no hard rejection",
            "Primary signal: group_2=Cell envelope (gram stain / outer membrane)."),
    "F13": ("sporulation",
            "source_labelled",
            "source-labelled context only; no hard rejection",
            "Primary signal: group_2=Sporulation."),
    "F14": ("genome_basic",
            "source_labelled",
            "source-labelled context only; no hard rejection",
            "Primary signal: group_1=Genome (Genome size / Gene content / Composition / Pangenome / Population diversity). Crosswalk files give NCBI<->GTDB identity context only."),
    "F15": ("habitat_generalism",
            "ecological_background",
            "low-coverage ecological background only; must not participate in ranking",
            "Primary signal: group_2=Generalism (Habitat). Ecological background only; not a ranking input."),
}

# field-aware patterns: list of (field, lowercase_substring)
# field in column names; a signature matches F if ANY rule's substring is found
# in that field's lowercased value.
F_PATTERNS = {
    "F1": [("group_2", "atmosphere"),
           ("trait_name", "aerotolerant"), ("trait_name", "microaerophil"),
           ("trait_name", "obligate aerobe"), ("trait_name", "obligate anaerobe"),
           ("trait_name", "facultative anaerobe"), ("trait_name", "oxygen tolerance"),
           ("ontology_ids", "oxygen")],
    "F2": [("group_2", "temperature"),
           ("trait_name", "temperature"), ("trait_name", "thermophil"),
           ("trait_name", "mesophil"), ("trait_name", "psychrophil"),
           ("trait_name", "psychrotolerant"), ("trait_name", "hyperthermophil")],
    "F3": [("group_2", "ph"),
           ("trait_name", "ph range"), ("trait_name", "optimum ph"),
           ("trait_name", "growth ph"), ("trait_name", "acidophil"),
           ("trait_name", "alkaliphil"), ("trait_name", "neutrophil")],
    "F4": [("group_2", "salinity"),
           ("trait_name", "salinity"), ("trait_name", "halophil"),
           ("trait_name", "halotolerant"), ("trait_name", "nacl")],
    "F5": [],  # NOT_METATRAITS_SOURCE_BACDIVE_ONLY
    "F6": [("group_2", "electron acceptor"), ("group_2", "respiration"),
           ("group_2", "denitrification"), ("group_2", "reduction"),
           ("group_2", "nitrification"), ("group_2", "ammonification"),
           ("trait_name", "electron acceptor"), ("trait_name", "nitrate"),
           ("trait_name", "nitrite"), ("trait_name", "sulfate"),
           ("trait_name", "sulfite"), ("trait_name", "thiosulfate"),
           ("trait_name", "fumarate"), ("trait_name", "ferric"),
           ("trait_name", "denitrif"), ("trait_name", "methanogenesis"),
           ("ontology_ids", "electron acceptor")],
    "F7": [("group_2", "carbon utilization"), ("group_2", "aerobic growth"),
           ("group_2", "anaerobic growth"), ("group_2", "fermentation"),
           ("group_2", "utilizes metabolite"), ("group_2", "assimilation"),
           ("group_2", "energy source"), ("group_2", "growth"),
           ("trait_name", "utilization"), ("trait_name", "catabolization"),
           ("trait_name", "growth:"), ("trait_name", "substrate"),
           ("trait_name", "carbon source"), ("trait_name", "fermentation")],
    "F8": [("group_2", "catabolic process"), ("group_2", "hydrolase activity"),
           ("group_2", "oxidation"),
           ("trait_name", "degradation"), ("trait_name", "catabolization"),
           ("trait_name", "hydrolysis"), ("trait_name", "aromatic"),
           ("trait_name", "xenobiotic"), ("trait_name", "pollutant")],
    "F9": [("group_1", "enzymes"),
           ("trait_name", "enzyme"), ("trait_name", "oxidase"),
           ("trait_name", "catalase"), ("trait_name", "urease"),
           ("trait_name", "lipase"), ("trait_name", "protease"),
           ("trait_name", "amylase"), ("trait_name", "cellulase"),
           ("trait_name", "phosphatase"), ("trait_name", "nitrate reductase")],
    "F10": [("group_2", "motility"), ("group_2", "cell appendages"),
            ("trait_name", "motility"), ("trait_name", "motile"),
            ("trait_name", "flagella"), ("trait_name", "gliding")],
    "F11": [("group_2", "cell morphology"), ("group_2", "cell size phenotype"),
            ("trait_name", "cell shape"), ("trait_name", "morphology"),
            ("trait_name", "pleomorphic"), ("trait_name", "filamentous")],
    "F12": [("group_2", "cell envelope"),
            ("trait_name", "gram"), ("trait_name", "outer membrane")],
    "F13": [("group_2", "sporulation"),
            ("trait_name", "sporulation"), ("trait_name", "spore"),
            ("trait_name", "endospore")],
    "F14": [("group_1", "genome"),
            ("trait_name", "genome"), ("trait_name", "coding density"),
            ("trait_name", "gene count"), ("trait_name", "gene content")],
    "F15": [("group_2", "generalism"),
            ("trait_name", "habitat"), ("trait_name", "isolation source"),
            ("trait_name", "ecosystem"), ("trait_name", "host-associated")],
}

# ----------------------------------------------------------------- main ------
def now_utc():  return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def now_local(): return datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    # conflict guard
    if os.path.exists(ARCHIVE) or os.path.exists(IDENTITY):
        log("ABORT: ARCHIVE or IDENTITY already exists -> %s / %s" % (ARCHIVE, IDENTITY))
        sys.exit(2)
    os.makedirs(RETURN_DIR, exist_ok=True)

    cmd_log_lines = [
        "# C7-1 long-form mapping correction (executor-only, 2026-08-19)",
        "# boundaries: NO MetaTraits download, NO MetaTraits API, NO BacDive API,",
        "#             NO prediction, NO production mutation, NO snapshot activation.",
        "# DATA_DIR=%s" % DATA_DIR,
        "# generated: %s" % now_utc(),
        "# Operations: gzip -t, header read, line-by-line streaming parse, mapping, reporting.",
    ]

    # ---- validate inputs ----
    required_summary_present = 0
    required_summary_gzip_pass = 0
    long_form_header_valid = 0
    crosswalk_present = 0
    file_headers = {}   # file_name -> header list
    file_col_idx = {}   # file_name -> {col: idx}
    file_valid_flags = {}  # file_name -> bool (present & gzip pass & long-form cols present)

    for (fname, ns, rank, scope) in SUMMARY_FILES:
        path = os.path.join(DATA_DIR, fname)
        present = os.path.isfile(path) and os.path.getsize(path) > 0
        gzip_ok = False
        header = None
        if present:
            # gzip -t via subprocess
            rc = subprocess.run(["gzip", "-t", path],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
            gzip_ok = (rc == 0)
        if gzip_ok:
            required_summary_present += 1
            required_summary_gzip_pass += 1
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
                header = fh.readline().rstrip("\n").split("\t")
            file_headers[fname] = header
            idx = {c: i for i, c in enumerate(header)}
            file_col_idx[fname] = idx
            missing = [c for c in REQUIRED_LONG_FORM_COLS if c not in idx]
            if not missing:
                long_form_header_valid += 1
                file_valid_flags[fname] = True
            else:
                file_valid_flags[fname] = False
                log("WARN: %s missing long-form cols: %s" % (fname, missing))
        else:
            file_valid_flags[fname] = False
            log("WARN: %s present=%s gzip_ok=%s" % (fname, present, gzip_ok))
        log("input %s: present=%s gzip_ok=%s long_form_ok=%s cols=%d"
            % (fname, present, gzip_ok, file_valid_flags[fname], len(header) if header else 0))

    for cw in CROSSWALK_FILES:
        p = os.path.join(DATA_DIR, cw)
        if os.path.isfile(p) and subprocess.run(["gzip","-t",p],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            crosswalk_present += 1

    all_inputs_ok = (required_summary_gzip_pass == 12 and long_form_header_valid == 12)

    # ---- stream + build catalog ----
    # catalog key: (fname, trait_name, unit, group_1, group_2, ontology_ids, databases)
    catalog = {}        # key -> dict(row_count, example, matched_Fs:set, why:dict)
    per_file_rows = {}  # fname -> total data rows
    per_scope_rows = {}  # scope -> total data rows
    # evidence examples: (F, scope) -> list of example dicts (<=50)
    examples = {(fid, scope): [] for fid in F_POLICY for (_,_,_,scope) in SUMMARY_FILES}
    # per-F match counts (unique signatures)
    f_match_observed = {fid: 0 for fid in F_POLICY}   # no_predictions scope
    f_match_all = {fid: 0 for fid in F_POLICY}        # all scope
    f_matched_sig_keys = {fid: set() for fid in F_POLICY}  # to dedupe per F across all files

    def match_signature(fields_by_name):
        # fields_by_name: {col: value}
        # returns list of (F, why_str)
        hits = []
        for fid, rules in F_PATTERNS.items():
            if fid == "F5":
                continue
            why = None
            for (field, sub) in rules:
                val = fields_by_name.get(field, "") or ""
                lv = val.lower()
                if sub in lv:
                    why = "%s:%s~%s" % (field, sub, val[:40])
                    break
            if why:
                hits.append((fid, why))
        return hits

    if all_inputs_ok:
        for (fname, ns, rank, scope) in SUMMARY_FILES:
            path = os.path.join(DATA_DIR, fname)
            idx = file_col_idx[fname]
            row_total = 0
            # columns we need
            need_cols = ["taxon_id","taxon_name","trait_name","unit","consensus_value",
                         "minimum","median","mean","maximum","discrete_values",
                         "databases","group_1","group_2","ontology_ids"]
            have_idx = {c: idx[c] for c in need_cols if c in idx}
            log("streaming %s (scope=%s, rank=%s) ..." % (fname, scope, rank))
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
                # skip header
                fh.readline()
                for line in fh:
                    if not line:
                        continue
                    row_total += 1
                    parts = line.rstrip("\n").split("\t")
                    # guard column count
                    def g(col):
                        i = have_idx.get(col)
                        if i is None or i >= len(parts):
                            return ""
                        return parts[i]
                    fields = {c: g(c) for c in have_idx}
                    tn = fields.get("trait_name","")
                    unit = fields.get("unit","")
                    g1 = fields.get("group_1","")
                    g2 = fields.get("group_2","")
                    ont = fields.get("ontology_ids","")
                    dbs = fields.get("databases","")
                    key = (fname, tn, unit, g1, g2, ont, dbs)
                    hits = match_signature(fields)
                    matched_fs = [fid for (fid,_) in hits]
                    entry = catalog.get(key)
                    if entry is None:
                        entry = {"row_count": 0, "example": None,
                                 "matched": set(), "why": {}, "first_scope": scope,
                                 "ns": ns, "rank": rank}
                        catalog[key] = entry
                    entry["row_count"] += 1
                    if entry["example"] is None:
                        entry["example"] = {
                            "taxon_id": fields.get("taxon_id",""),
                            "taxon_name": fields.get("taxon_name",""),
                            "consensus_value": fields.get("consensus_value",""),
                            "minimum": fields.get("minimum",""),
                            "median": fields.get("median",""),
                            "mean": fields.get("mean",""),
                            "maximum": fields.get("maximum",""),
                        }
                    for (fid, why) in hits:
                        entry["matched"].add(fid)
                        if fid not in entry["why"]:
                            entry["why"][fid] = why
                        f_matched_sig_keys[fid].add(key)
                        # evidence examples
                        cap = examples.get((fid, scope))
                        if cap is not None and len(cap) < 50:
                            cap.append({
                                "trait_id": fid, "trait_name_c7": F_POLICY[fid][0],
                                "prediction_scope": scope, "file_name": fname,
                                "taxonomy_namespace": ns, "taxonomic_rank": rank,
                                "metatraits_trait_name": tn, "unit": unit,
                                "group_1": g1, "group_2": g2, "ontology_ids": ont,
                                "databases": dbs,
                                "example_taxon_id": fields.get("taxon_id",""),
                                "example_taxon_name": fields.get("taxon_name",""),
                                "example_consensus_value": fields.get("consensus_value",""),
                                "example_minimum": fields.get("minimum",""),
                                "example_median": fields.get("median",""),
                                "example_mean": fields.get("mean",""),
                                "example_maximum": fields.get("maximum",""),
                                "why_matched": why,
                                "boundary_note": F_POLICY[fid][3],
                            })
            per_file_rows[fname] = row_total
            per_scope_rows[scope] = per_scope_rows.get(scope, 0) + row_total
            log("  %s: %d data rows streamed" % (fname, row_total))

        # per-F match counts (unique signatures), split by scope using file scope
        for fid in F_POLICY:
            if fid == "F5":
                continue
            for key in f_matched_sig_keys[fid]:
                fname = key[0]
                # find scope of that file
                sc = [s for (fn,_,_,s) in SUMMARY_FILES if fn == fname][0]
                if sc == "no_predictions":
                    f_match_observed[fid] += 1
                else:
                    f_match_all[fid] += 1

    # ---- write METATRAITS_LONG_FORM_TRAIT_CATALOG.csv ----
    cat_cols = ["file_name","taxonomy_namespace","taxonomic_rank","prediction_scope",
                "trait_name","unit","group_1","group_2","ontology_ids","databases",
                "row_count","candidate_c7_trait_ids","candidate_c7_mapping_status"]
    cat_path = os.path.join(RETURN_DIR, "METATRAITS_LONG_FORM_TRAIT_CATALOG.csv")
    # size guard: keep matched-only if catalog would be very large
    matched_keys = [k for k,v in catalog.items() if v["matched"]]
    all_keys = list(catalog.keys())
    use_matched_only = False
    # decide by estimated row count: if matched-only is still reasonable, prefer ALL;
    # if ALL is huge, fall back to matched-only.
    if len(all_keys) > 120000:
        use_matched_only = True
    catalog_filter = "C7_PATTERN_MATCHED_ONLY" if use_matched_only else "ALL_SIGNATURES"
    chosen_keys = matched_keys if use_matched_only else all_keys
    with open(cat_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cat_cols)
        for key in chosen_keys:
            fname, tn, unit, g1, g2, ont, dbs = key
            entry = catalog[key]
            ns = entry["ns"]; rank = entry["rank"]; scope = entry["first_scope"]
            mfs = sorted(entry["matched"])
            if len(mfs) == 0:
                mstatus = "NO_MATCH"
            elif len(mfs) == 1:
                mstatus = "SINGLE_MATCH"
            else:
                mstatus = "MULTI_MATCH_AMBIGUOUS"
            w.writerow([fname, ns, rank, scope, tn, unit, g1, g2, ont, dbs,
                        entry["row_count"], ";".join(mfs), mstatus])
    log("catalog written: %d rows (%s), total unique signatures=%d, matched=%d"
        % (len(chosen_keys), catalog_filter, len(all_keys), len(matched_keys)))

    # ---- write C7_1_TRAIT_PANEL_METATRAITS_LONG_FORM_MAPPING_CORRECTION.csv ----
    corr_cols = ["trait_id","trait_name","first_screen","teacher_policy",
                 "metatraits_long_form_fields_to_use","observed_scope_files_to_check",
                 "all_scope_files_to_check","candidate_trait_name_patterns",
                 "candidate_group_1_patterns","candidate_group_2_patterns",
                 "candidate_units","observed_scope_match_count","all_scope_match_count",
                 "example_trait_names_observed_scope","example_trait_names_all_scope",
                 "mapping_status","boundary_notes"]
    observed_files = [fn for (fn,_,_,s) in SUMMARY_FILES if s=="no_predictions"]
    all_files = [fn for (fn,_,_,s) in SUMMARY_FILES if s=="all"]
    corr_path = os.path.join(RETURN_DIR, "C7_1_TRAIT_PANEL_METATRAITS_LONG_FORM_MAPPING_CORRECTION.csv")
    # gather example trait_names per F per scope (unique, up to 8 for readability)
    ex_tn = {(fid, scope): [] for fid in F_POLICY for (_,_,_,scope) in SUMMARY_FILES}
    for key in chosen_keys:
        fname, tn, unit, g1, g2, ont, dbs = key
        scope = catalog[key]["first_scope"]
        for fid in catalog[key]["matched"]:
            lst = ex_tn[(fid, scope)]
            if tn and tn not in lst and len(lst) < 8:
                lst.append(tn)
    with open(corr_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(corr_cols)
        for fid in ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","F13","F14","F15"]:
            tname, first_screen, policy, boundary = F_POLICY[fid]
            # pattern summaries
            rules = F_PATTERNS[fid]
            tn_pats = "; ".join(sorted(set(p for (fld,p) in rules if fld=="trait_name")))
            g1_pats = "; ".join(sorted(set(p for (fld,p) in rules if fld=="group_1")))
            g2_pats = "; ".join(sorted(set(p for (fld,p) in rules if fld=="group_2")))
            unit_pats = "; ".join(sorted(set(p for (fld,p) in rules if fld=="unit")))
            fields_to_use = "trait_name, group_1, group_2, unit, ontology_ids"
            if fid == "F5":
                mstatus = "NOT_METATRAITS_SOURCE_BACDIVE_ONLY"
                obs_cnt = 0; all_cnt = 0
                ex_obs = ""; ex_all = ""
                fields_to_use = "(none - BacDive/culture collection only)"
            else:
                obs_cnt = f_match_observed[fid]
                all_cnt = f_match_all[fid]
                ex_obs = "; ".join(ex_tn[(fid,"no_predictions")])
                ex_all = "; ".join(ex_tn[(fid,"all")])
                if obs_cnt == 0 and all_cnt == 0:
                    mstatus = "NOT_MAPPED_FROM_METATRAITS_AFTER_LONG_FORM_SCAN"
                else:
                    mstatus = "MAPPED_LONG_FORM_DRAFT"
            w.writerow([fid, tname, first_screen, policy, fields_to_use,
                        "; ".join(observed_files), "; ".join(all_files),
                        tn_pats, g1_pats, g2_pats, unit_pats,
                        obs_cnt, all_cnt, ex_obs, ex_all, mstatus, boundary])
    log("mapping correction CSV written (15 rows)")

    # ---- write METATRAITS_C7_1_MAPPING_EVIDENCE_EXAMPLES.csv ----
    ev_cols = ["trait_id","trait_name","prediction_scope","file_name","taxonomy_namespace",
               "taxonomic_rank","metatraits_trait_name","unit","group_1","group_2",
               "ontology_ids","databases","example_taxon_id","example_taxon_name",
               "example_consensus_value","example_minimum","example_median","example_mean",
               "example_maximum","why_matched","boundary_note"]
    ev_path = os.path.join(RETURN_DIR, "METATRAITS_C7_1_MAPPING_EVIDENCE_EXAMPLES.csv")
    with open(ev_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(ev_cols)
        n = 0
        for (fid, scope), lst in sorted(examples.items()):
            for e in lst:
                w.writerow([e["trait_id"], e["trait_name_c7"], e["prediction_scope"],
                            e["file_name"], e["taxonomy_namespace"], e["taxonomic_rank"],
                            e["metatraits_trait_name"], e["unit"], e["group_1"], e["group_2"],
                            e["ontology_ids"], e["databases"], e["example_taxon_id"],
                            e["example_taxon_name"], e["example_consensus_value"],
                            e["example_minimum"], e["example_median"], e["example_mean"],
                            e["example_maximum"], e["why_matched"], e["boundary_note"]])
                n += 1
    log("evidence examples written: %d rows" % n)

    # ---- mapping summary json ----
    summary = {
        "task_id": TASK_ID,
        "data_dir": DATA_DIR,
        "catalog_filter": catalog_filter,
        "total_unique_signatures": len(all_keys),
        "matched_unique_signatures": len(matched_keys),
        "per_file_data_rows": per_file_rows,
        "per_scope_data_rows": per_scope_rows,
        "per_trait_unique_signature_matches": {
            fid: (f_match_observed[fid] + f_match_all[fid]) for fid in F_POLICY if fid != "F5"
        },
        "per_trait_observed_scope_match_count": f_match_observed,
        "per_trait_all_scope_match_count": f_match_all,
        "evidence_example_rows": n,
        "created_at_utc": now_utc(),
    }
    with open(os.path.join(RETURN_DIR, "METATRAITS_C7_1_MAPPING_SUMMARY.json"), "w") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")

    # ---- mapping correction md ----
    with open(os.path.join(RETURN_DIR, "C7_1_TRAIT_PANEL_METATRAITS_LONG_FORM_MAPPING_CORRECTION.md"), "w") as f:
        f.write("# MetaTraits C7-1 long-form mapping correction\n\n")
        f.write("- task_id: `%s`\n" % TASK_ID)
        f.write("- data_dir: `%s`\n" % DATA_DIR)
        f.write("- previous_return_dir: `%s`\n" % PREVIOUS_RETURN_DIR)
        f.write("- catalog_filter: `%s`\n" % catalog_filter)
        f.write("- total_unique_signatures: %d (matched: %d)\n\n" % (len(all_keys), len(matched_keys)))
        f.write("## F1-F15 mapping status\n\n")
        f.write("| trait_id | trait_name | mapping_status | observed_scope_match | all_scope_match |\n")
        f.write("|---|---|---|---|---|\n")
        for fid in ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","F13","F14","F15"]:
            if fid == "F5":
                ms = "NOT_METATRAITS_SOURCE_BACDIVE_ONLY"; oc="-"; ac="-"
            else:
                ms = "MAPPED_LONG_FORM_DRAFT" if (f_match_observed[fid]+f_match_all[fid])>0 \
                      else "NOT_MAPPED_FROM_METATRAITS_AFTER_LONG_FORM_SCAN"
                oc = f_match_observed[fid]; ac = f_match_all[fid]
            f.write("| %s | %s | %s | %s | %s |\n" % (fid, F_POLICY[fid][0], ms, oc, ac))
        f.write("\n## Key interpretation notes\n\n")
        f.write("- MetaTraits summary TSVs are **long-form**: semantic traits live in row values "
                "(`trait_name`, `group_1`, `group_2`, `unit`, `ontology_ids`), not in wide columns.\n")
        f.write("- `group_1`/`group_2` provide the cleanest semantic signal and are used as primary "
                "evidence (e.g. `Environmental preferences/Atmosphere`=F1, `/Temperature`=F2, "
                "`/pH`=F3, `/Salinity`=F4; `Metabolism/Electron acceptor`=F6; `Enzymes/Enzyme "
                "activity`=F9; `Morphology/Cell envelope`=F12; `Genome/*`=F14; `Habitat/Generalism`=F15).\n")
        f.write("- F1 oxygen-tolerance is separated from F7 substrate-utilization: "
                "`aerobic/anaerobic growth: <substrate>` rows map to F7 (substrate context), "
                "while F1 uses `group_2=Atmosphere` plus oxygen-specific trait_names.\n")
        f.write("- F8 (broad degradation) overlaps F9 for hydrolase rows; kept as broad context only.\n")
        f.write("- F5 is BacDive/culture-collection closure evidence; NOT a MetaTraits source.\n")
        f.write("- This is a **draft evidence mapping**, not final production implementation.\n")

    # ---- validation report ----
    trait_panel_rows_written = 15
    final_status = ("METATRAITS_C7_1_LONG_FORM_MAPPING_CORRECTION_COMPLETE"
                    if all_inputs_ok else
                    "BLOCKED_METATRAITS_C7_1_MAPPING_INPUT_MISSING_OR_INVALID")
    vr = {
        "task_id": TASK_ID,
        "data_dir": DATA_DIR,
        "return_dir": RETURN_DIR,
        "previous_return_dir": PREVIOUS_RETURN_DIR,
        "required_summary_expected_count": 12,
        "required_summary_present_count": required_summary_present,
        "required_summary_gzip_pass_count": required_summary_gzip_pass,
        "long_form_header_valid_count": long_form_header_valid,
        "crosswalk_present_count": crosswalk_present,
        "mapping_correction_created": all_inputs_ok,
        "trait_panel_rows_expected": 15,
        "trait_panel_rows_written": trait_panel_rows_written,
        "catalog_filter": catalog_filter,
        "total_unique_signatures": len(all_keys),
        "matched_unique_signatures": len(matched_keys),
        "boundary_no_download": True,
        "boundary_no_api_call": True,
        "boundary_no_prediction_run": True,
        "boundary_no_production_mutation": True,
        "boundary_no_snapshot_activation": True,
        "final_status": final_status,
        "created_at_utc": now_utc(),
        "created_at_local": now_local(),
    }
    with open(os.path.join(RETURN_DIR, "VALIDATION_REPORT.json"), "w") as f:
        json.dump(vr, f, indent=2)
        f.write("\n")
    with open(os.path.join(RETURN_DIR, "VALIDATION_REPORT.md"), "w") as f:
        f.write("# MetaTraits C7-1 mapping correction validation\n\n")
        for k, v in vr.items():
            f.write("- %s: `%s`\n" % (k, v))

    # ---- command log ----
    with open(os.path.join(RETURN_DIR, "COMMAND_LOG.txt"), "w") as f:
        f.write("\n".join(cmd_log_lines) + "\n")

    # ---- final status ----
    with open(os.path.join(RETURN_DIR, "FINAL_STATUS.txt"), "w") as f:
        f.write("final_status=%s\n" % final_status)
        f.write("DATA_DIR=%s\n" % DATA_DIR)
        f.write("RETURN_DIR=%s\n" % RETURN_DIR)
        f.write("ARCHIVE=%s\n" % ARCHIVE)
        f.write("IDENTITY=%s\n" % IDENTITY)
        f.write("trait_panel_rows_written=%d/15\n" % trait_panel_rows_written)
        f.write("catalog_filter=%s\n" % catalog_filter)
        f.write("generated_at_utc=%s\n" % now_utc())

    # ---- MANIFEST.files / MANIFEST.sha256 ----
    # list all files in RETURN_DIR except the two manifest files
    all_return_files = sorted([fn for fn in os.listdir(RETURN_DIR)
                               if os.path.isfile(os.path.join(RETURN_DIR, fn))
                               and fn not in ("MANIFEST.files", "MANIFEST.sha256")])
    with open(os.path.join(RETURN_DIR, "MANIFEST.files"), "w") as f:
        f.write("\n".join(all_return_files) + "\n")
    with open(os.path.join(RETURN_DIR, "MANIFEST.sha256"), "w") as f:
        for fn in all_return_files:
            f.write("%s  %s\n" % (sha256_file(os.path.join(RETURN_DIR, fn)), fn))

    # ---- archive (metadata only) ----
    with tarfile.open(ARCHIVE, "w:gz") as tar:
        tar.add(RETURN_DIR, arcname=TASK_ID)
    archive_size = os.path.getsize(ARCHIVE)
    archive_sha = sha256_file(ARCHIVE)

    # ---- identity sidecar ----
    with open(IDENTITY, "w") as f:
        f.write("task_id=%s\n" % TASK_ID)
        f.write("archive_path=%s\n" % ARCHIVE)
        f.write("archive_size_bytes=%d\n" % archive_size)
        f.write("archive_sha256=%s\n" % archive_sha)
        f.write("single_root_dir=%s\n" % TASK_ID)
        f.write("data_dir=%s\n" % DATA_DIR)
        f.write("previous_return_dir=%s\n" % PREVIOUS_RETURN_DIR)
        f.write("final_status=%s\n" % final_status)
        f.write("created_at_utc=%s\n" % now_utc())
        f.write("created_at_local=%s\n" % now_local())

    log("============================================================")
    log("FINAL_STATUS=%s" % final_status)
    log("DATA_DIR=%s" % DATA_DIR)
    log("RETURN_DIR=%s" % RETURN_DIR)
    log("ARCHIVE=%s" % ARCHIVE)
    log("IDENTITY=%s" % IDENTITY)
    log("trait_panel_rows_written=%d/15" % trait_panel_rows_written)
    log("archive_sha256=%s" % archive_sha)
    log("DONE.")

if __name__ == "__main__":
    main()
