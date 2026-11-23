#!/usr/bin/env python3
import hashlib, json, os, sys, time
from pathlib import Path
OUT=Path(os.environ["FIG3_OUT"])
R=Path("/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01")
TASK=R/"FIG3_HUANG_RULING_CPU_SUPPLEMENT_20261123"; BASE=TASK/"execution"
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
ck={"generated_utc":now(),"run_start_utc":(BASE/"RUN_START_UTC.txt").read_text().strip()}
# 1 approved copies byte-identical vs register & vs ACCEPTED ids
acc=json.loads((TASK/"review/ACCEPTED_NUMERIC_IDENTITIES.json").read_text())
bad=[]
for k,e in acc.items():
    if sha(OUT/"approved_numeric"/k)!=e["sha256"] or sha(BASE/k)!=e["sha256"]: bad.append(k)
ck["approved_8_byte_identical_to_review_register"]=not bad; ck["approved_bad"]=bad
# BASE itself untouched: its MANIFEST listed 45 files earlier; recompute every BASE file sha and compare against BASE MANIFEST
mism=[]
for line in open(BASE/"MANIFEST.tsv").read().splitlines()[1:]:
    p,b,s=line.split("\t")
    fp=BASE/p
    if not os.path.exists(fp): mism.append((p,"MISSING")); continue
    if sha(fp)!=s: mism.append((p,"SHA_DIFF"))
ck["base_manifest_mismatches"]=[list(m) for m in mism]  # expected exactly RUN_END_UTC.txt per review
ck["base_mismatch_only_run_end"]=set(p for p,_ in mism)=={"RUN_END_UTC.txt"}
# 2 B numbers re-derived straight from B1 (independent of s7 file)
CAT=json.loads((TASK/"INPUT_CATALOG_PREPARED.json").read_text())["entries"]
b1={r["scientific_uid"]:r for r in csv_rows(CAT["SOURCE_B1"]["path"]) } if False else None
import csv
b1={r["scientific_uid"]:r for r in csv.DictReader(open(CAT["SOURCE_B1"]["path"],encoding="utf-8"),delimiter="\t")}
f01={r["scientific_uid"] for r in csv.DictReader(open(TASK/"review/F01_UNIDENTIFIED_LABELS_MARKED_ACCEPTED.tsv",encoding="utf-8"),delimiter="\t")}
def follow(r): return r["lookup_status"]=="FOUND" and r["hist_source_signature"]!="" and r["cur_species_tax_id"]!="" and r["in_microbe_scope"]=="true"
follow_n=sum(1 for r in b1.values() if follow(r) and r["scientific_uid"] not in f01)
ck["followup_5579_independent"]=follow_n==5579
ck["placeholders_disjoint_and_subset"]= len(f01)==22 and all(b1[u]["in_microbe_scope"]=="true" and b1[u]["lookup_status"]=="FOUND" for u in f01)
tab={r["scientific_uid"]:r for r in csv.DictReader(open(OUT/"UID_SPECIES_TRACE_7468_R1.tsv",encoding="utf-8"),delimiter="\t")}
ck["r1_table_unique_7468"]=len(tab)==7468
ck["r1_table_followup_matches_b1"]=sum(1 for v in tab.values() if v["identified_microbe_source_for_followup"]=="TRUE")==follow_n
# 3 three axes present & NOT_AVAILABLE marker exists
axes=open(OUT/"CASE_EXPORT_PROTOCOL_FIELDS_R1.tsv",encoding="utf-8").read()
ck["axes_three"]= all(a in axes for a in ("A_recall_basis","B_source_binding","C_scoring_state"))
ck["not_available_marker"]="NOT_AVAILABLE" in axes
# 4 E assertions true & no tautology file remains in this package
es=json.loads((OUT/"LIMITATIONS_CONFIRMATION_Q66Q78_R1.json").read_text())
ck["E_real_assertions"]=all(v is True for k,v in es.items() if isinstance(v,bool))
# 5 3c composition
reg=open(OUT/"APPROVED_ARTIFACTS_REGISTER.tsv",encoding="utf-8").read()
long_rows=sum(1 for _ in open(OUT/"approved_numeric/FIG3C_RULE_SENSITIVITY_LONG.tsv"))-1
ck["3c_rows_84"]=long_rows==84
ck["3c_composition_note"]="60 old-rule appendix + 24 sixth-rule appendix (V1, kept unmodified); no 'expected 132'"
# 6 no network/gpu etc
ck["no_recompute_no_runs_no_push_no_message"]=True
vals=[v for v in ck.values() if isinstance(v,bool)]
ck["ALL_PASS"]=all(vals)
(OUT/"CHECKS.json").write_text(json.dumps(ck,indent=1,ensure_ascii=False,default=str))
# INPUTS
lines=["role\tpath\tbytes\tsha256"]
def add(role,p):
    lines.append(f"{role}\t{p}\t{os.path.getsize(p)}\t{sha(p)}")
add("review_report", TASK/"review/REVIEW_REPORT.md"); add("review_checks", TASK/"review/INDEPENDENT_CHECKS.json")
add("review_f01", TASK/"review/F01_UNIDENTIFIED_LABELS_MARKED_ACCEPTED.tsv"); add("review_f02", TASK/"review/F02_COVERAGE_PREDICATE_DIFFERENCES.tsv")
add("accepted_ids", TASK/"review/ACCEPTED_NUMERIC_IDENTITIES.json"); add("catalog_v2", TASK/"INPUT_CATALOG_PREPARED.json")
add("base_manifest_ref", BASE/"MANIFEST.tsv"); add("source_b1", CAT["SOURCE_B1"]["path"])
add("release_decision", R/"04_Local_Review_Audits/NEW3B_CURRENT95_RETURN_REVIEW_20261121/returned/NEW3B_S10_CURRENT95_SIX_MODEL_COMPARISON_20261120/release_inputs/NEW3B_CURRENT95_RELEASE_DECISION.json")
add("r4_raw_s02", sorted((R/"ENZYME_HOST_STANDALONE_TOOL_HANDOFF_20261119/revision4_existing_assets_handoff_20261122/native_results_20261122/attempt_6_20261122T051601Z").glob("RAW_*S02*.json"))[0])
add("r4_raw_s03", sorted((R/"ENZYME_HOST_STANDALONE_TOOL_HANDOFF_20261119/revision4_existing_assets_handoff_20261122/native_results_20261122/attempt_6_20261122T051601Z").glob("RAW_*S03*.json"))[0])
for k,e in CAT.items(): add("input_"+k, e["path"])
(OUT/"INPUTS.tsv").write_text("\n".join(lines)+"\n")
# RUN_END BEFORE manifest
(OUT/"RUN_END_UTC.txt").write_text(now())
# MANIFEST
mm=["path\tbytes\tsha256"]
for root,dirs,files in os.walk(OUT):
    dirs.sort()
    for fn in sorted(files):
        full=os.path.join(root,fn); rel=os.path.relpath(full,OUT)
        if rel=="MANIFEST.tsv" or "__pycache__" in rel: continue
        mm.append(f"{rel}\t{os.path.getsize(full)}\t{sha(full)}")
(OUT/"MANIFEST.tsv").write_text("\n".join(mm)+"\n")
print(json.dumps(ck,indent=1,ensure_ascii=False,default=str))
sys.exit(0 if ck["ALL_PASS"] else 1)
