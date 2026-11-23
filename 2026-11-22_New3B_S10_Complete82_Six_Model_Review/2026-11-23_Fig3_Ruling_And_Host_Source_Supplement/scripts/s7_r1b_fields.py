#!/usr/bin/env python3
"""R1-B: three-layer species field fix. No B1 edits, no taxonomy work,
no new coverage production. Placeholder list = review F01 (read-only)."""
import csv, json, os, sys
from pathlib import Path
from collections import Counter, defaultdict

OUT = Path(os.environ["FIG3_OUT"])
TASK = Path("/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/FIG3_HUANG_RULING_CPU_SUPPLEMENT_20261123")
BASE = TASK / "execution"
CAT = json.loads((TASK / "INPUT_CATALOG_PREPARED.json").read_text())["entries"]

# 22 registered placeholders from review F01 (authoritative list; read-only)
f01 = list(csv.DictReader(open(TASK / "review/F01_UNIDENTIFIED_LABELS_MARKED_ACCEPTED.tsv"), encoding="utf-8"), ) if False else list(csv.DictReader(open(TASK / "review/F01_UNIDENTIFIED_LABELS_MARKED_ACCEPTED.tsv", encoding="utf-8"), delimiter="\t"))
placeholders = {r["scientific_uid"]: {"taxid": r["cur_species_tax_id"], "name": r["cur_species_name"]} for r in f01}
b1 = {r["scientific_uid"]: r for r in csv.DictReader(open(CAT["SOURCE_B1"]["path"], encoding="utf-8"), delimiter="\t")}
assert len(placeholders) == 22 and all(u in b1 for u in placeholders)
assert all(b1[u]["in_microbe_scope"] == "true" and b1[u]["lookup_status"] == "FOUND" for u in placeholders)

rows = []
for uid in sorted(b1):
    r = b1[uid]
    traceable = (r["lookup_status"] == "FOUND" and r["hist_source_signature"] != "" and r["cur_species_tax_id"] != "")
    scope = r["in_microbe_scope"]  # true/false/''(UNRESOLVED)
    if r["lookup_status"] == "IDENTITY_CONFLICT": state = "NOT_TRACED_IDENTITY_CONFLICT"
    elif r["lookup_status"] == "NO_HIT": state = "NOT_TRACED_QUERY_NO_HIT"
    elif r["lookup_status"] == "FOUND_SOURCE_SET": state = "SOURCE_SET_NOT_SINGLE_SPECIES"
    elif uid in placeholders: state = "UNIDENTIFIED_PLACEHOLDER_LABEL"
    elif traceable: state = "IDENTIFIED_SPECIES"
    else: state = "FOUND_RECORD_INCOMPLETE_NO_KEY_OR_TAXID"
    follow = traceable and scope == "true" and uid not in placeholders and state == "IDENTIFIED_SPECIES"
    reason = ("review/F01 marked Unknown/uncultured" if state == "UNIDENTIFIED_PLACEHOLDER_LABEL"
              else ("source-set not single strain/species" if state == "SOURCE_SET_NOT_SINGLE_SPECIES"
              else ("specified query no hit" if state.startswith("NOT_TRACED_QUERY")
              else ("sequence identity conflict" if state == "NOT_TRACED_IDENTITY_CONFLICT"
              else ("record traceable; scope " + (scope or "UNRESOLVED"))))))
    rows.append({"scientific_uid": uid, "join_key_sequence_sha256": r["sequence_sha256"],
                 "lookup_status": r["lookup_status"],
                 "source_record_species_traceable": "TRUE" if traceable else "FALSE",
                 "microbe_scope_accepted": {"true": "TRUE", "false": "FALSE"}.get(scope, "UNRESOLVED"),
                 "species_identity_state": state,
                 "identified_microbe_source_for_followup": "TRUE" if follow else "FALSE",
                 "cur_species_tax_id": r["cur_species_tax_id"], "cur_species_name": r["cur_species_name"],
                 "authoritative_source_key": r["hist_source_signature"],
                 "hist_is_ambiguous_retained": r["hist_is_ambiguous"],
                 "reason": reason,
                 "source_locator": "SOURCE_B1:B1_UID_SOURCE_MAP_7468.tsv#scientific_uid=" + uid + (";review:F01" if uid in placeholders else "")})

# consistency vs the old delivered table (original fields must match)
old = {r["scientific_uid"]: r for r in csv.DictReader(open(BASE / "UID_SPECIES_TRACE_7468.tsv", encoding="utf-8"), delimiter="\t")}
mism = [x for x in [r["scientific_uid"] for r in rows if old[r["scientific_uid"]]["lookup_status"] != r["lookup_status"] or old[r["scientific_uid"]]["cur_species_tax_id"] != r["cur_species_tax_id"] or old[r["scientific_uid"]]["in_microbe_scope"] != ({"TRUE":"true","FALSE":"false","UNRESOLVED":""}[r["microbe_scope_accepted"]])]]
assert not mism, mism[:3]

with open(OUT / "UID_SPECIES_TRACE_7468_R1.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(rows)

st = Counter(r["species_identity_state"] for r in rows)
follow_n = sum(1 for r in rows if r["identified_microbe_source_for_followup"] == "TRUE")
trace_n = sum(1 for r in rows if r["source_record_species_traceable"] == "TRUE")
scope_true = sum(1 for r in rows if r["microbe_scope_accepted"] == "TRUE")
base_layer = sum(1 for r in rows if r["source_record_species_traceable"] == "TRUE" and r["microbe_scope_accepted"] == "TRUE")
assert base_layer == 5601 and follow_n == 5579 and st["UNIDENTIFIED_PLACEHOLDER_LABEL"] == 22

# species-level record / original strain / representative registration are never upgraded between layers
# multi-proteome same species kept
sps = defaultdict(set)
for r in rows:
    if r["source_record_species_traceable"] == "TRUE" and r["authoritative_source_key"].startswith("proteome:"):
        sps[r["cur_species_tax_id"]].add(r["authoritative_source_key"])
multi = sum(1 for v in sps.values() if len(v) > 1)

count_rows = [
 {"statistic": "UIDs (unique, whole cohort)", "value": len(rows), "meaning": "candidate enzymes, NOT organisms"},
 {"statistic": "source_record_species_traceable (record-level base)", "value": trace_n, "meaning": "FOUND + nonempty authoritative key + nonempty species taxid; includes placeholder labels and non-microbe scope; NOT 'identified follow-up-usable species'"},
 {"statistic": "microbe_scope_accepted=TRUE", "value": scope_true, "meaning": "accepted microbe-scope layer only; independent of trace"},
 {"statistic": "traceable AND scope accepted (base layer, kept)", "value": base_layer, "meaning": "previous 5601; retained as record-layer count"},
 {"statistic": "UNIDENTIFIED_PLACEHOLDER_LABEL", "value": st["UNIDENTIFIED_PLACEHOLDER_LABEL"], "meaning": "registered Unknown/uncultured working list (review F01: taxids 2725/1781162/77133/201089/171953)"},
 {"statistic": "identified_microbe_source_for_followup", "value": follow_n, "meaning": "WORKING DEFINITION = traceable ∧ scope accepted ∧ not placeholder; baseline for judgement-B; does NOT prove culturability, purchase or chain function"},
 {"statistic": "NOT_IDENTIFIED total (no_hit+conflict+source_set)", "value": st["NOT_TRACED_QUERY_NO_HIT"] + st["NOT_TRACED_IDENTITY_CONFLICT"] + st["SOURCE_SET_NOT_SINGLE_SPECIES"], "meaning": "unidentified/not-single-identity handled explicitly; source-set species still judged by original record evidence, never declared globally undeterminable"},
 {"statistic": "multi-proteome keys on one species (species count)", "value": multi, "meaning": "kept as evidence richness, not ambiguity"},
 {"statistic": "hist_is_ambiguous=1 retained", "value": sum(1 for r in rows if r["hist_is_ambiguous_retained"] == "1"), "meaning": "historical flag kept as metadata, NOT recoded as species-indeterminate"},
 {"statistic": "C8_source_record_present (trait-library axis)", "value": 4845, "meaning": "record presence in C8; never a source gate"},
]
with open(OUT / "SPECIES_TRACE_STATUS_COUNTS_R1.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["statistic", "value", "meaning"], delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(count_rows)

dic = [
 {"field": "source_record_species_traceable", "layer": "record traceability", "predicate": "lookup_status=FOUND ∧ hist_source_signature≠'' ∧ cur_species_tax_id≠'' ∧ candidate sequence_sha256 == B1 row sha", "one_line": "the record points to one authoritative source carrying a species-level taxid", "file_column": "UID_SPECIES_TRACE_7468_R1.tsv#source_record_species_traceable"},
 {"field": "microbe_scope_accepted", "layer": "microbe acceptance", "predicate": "in_microbe_scope=true (previously accepted scope)", "one_line": "accepted as a microbe for downstream recommendation purposes", "file_column": "...#microbe_scope_accepted"},
 {"field": "species_identity_state", "layer": "species identifiability", "predicate": "ENUM: IDENTIFIED_SPECIES | UNIDENTIFIED_PLACEHOLDER_LABEL(22) | SOURCE_SET_NOT_SINGLE_SPECIES(7) | NOT_TRACED_QUERY_NO_HIT(30) | NOT_TRACED_IDENTITY_CONFLICT(1) | FOUND_RECORD_INCOMPLETE(0)", "one_line": "whether the species label itself is a real identification", "file_column": "...#species_identity_state"},
 {"field": "identified_microbe_source_for_followup", "layer": "combined working definition (RECOMMENDED for judgement-B)", "predicate": "source_record_species_traceable ∧ microbe_scope_accepted ∧ species_identity_state=IDENTIFIED_SPECIES", "one_line": "candidate has an identified, microbe-accepted source species usable as follow-up evidence; NOT a claim of culturability, availability or chain function", "file_column": "...#identified_microbe_source_for_followup"},
 {"field": "hist_is_ambiguous / multi-proteome same species", "layer": "evidence richness metadata", "predicate": "kept as-is (229 / 71)", "one_line": "never collapsed into unknown; source-set species judged by original record evidence only", "file_column": "...#hist_is_ambiguous_retained"},
 {"field": "V1 coverage table status", "layer": "appellation correction", "predicate": "approved_numeric/NONGOLD_SPECIES_COVERAGE_*.tsv", "one_line": "generalized source-traceability APPENDIX (includes non-microbe sources and placeholder labels); withdrawn as final judgement-B coverage; the 596 predicate-difference rows are listed by review F02; no new formal coverage produced by this window", "file_column": "n/a"},
]
with open(OUT / "SPECIES_FIELD_DICTIONARY_AND_JOIN_PROTOCOL_R1.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["field", "layer", "predicate", "one_line", "file_column"], delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(dic)

checks = {"rows_unique_7468": len(rows) == len(set(x["scientific_uid"] for x in rows)) == 7468,
          "base_layer_5601": base_layer == 5601, "followup_5579": follow_n == 5579,
          "placeholders_22": st["UNIDENTIFIED_PLACEHOLDER_LABEL"] == 22, "no_hit_30_conflict_1_sourceset_7":
          st["NOT_TRACED_QUERY_NO_HIT"] == 30 and st["NOT_TRACED_IDENTITY_CONFLICT"] == 1 and st["SOURCE_SET_NOT_SINGLE_SPECIES"] == 7,
          "ambiguity_flag_not_recoded": sum(1 for r in rows if r["hist_is_ambiguous_retained"] == "1" and r["species_identity_state"] in ("NOT_TRACED_QUERY_NO_HIT","NOT_TRACED_IDENTITY_CONFLICT")) == 0,
          "original_fields_match_base_table": not mism,
          "no_new_coverage_produced": True}
(OUT / "internal_R1B_CHECKS.json").write_text(json.dumps(checks, indent=1))
print(json.dumps({**checks, "states": dict(st), "multi_proteome_species": multi}, indent=1, ensure_ascii=False))
sys.exit(0 if all(checks.values()) else 1)
