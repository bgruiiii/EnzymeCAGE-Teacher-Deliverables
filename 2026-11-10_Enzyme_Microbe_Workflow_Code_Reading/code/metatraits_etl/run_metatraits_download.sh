#!/usr/bin/env bash
# =============================================================================
# run_metatraits_download.sh
# MetaTraits bulk TSV land on Chenyu — executor-only, READ/DOWNLOAD/REPORT ONLY.
#
# Mission : download the 12 required MetaTraits bulk summary TSV gzip files
#           plus 2 companion crosswalk files from the official source, validate
#           them (gzip -t + SHA256), and emit a metadata-only report package.
#
# Hard boundaries : no API calls, no predictions, no production mutation,
#                   no large TSV data inside the returned archive.
#
# Run style        : nohup bash run_metatraits_download.sh \
#                     > /tmp/metatraits_bulk_tsv_download_20260818.log 2>&1 &
# =============================================================================
set -uo pipefail

# ------------------------------------------------------------------ paths ----
TASK_ID="metatraits_bulk_tsv_landed_chenyu_20260818"
PROJECT_ROOT="/root/projects/EnzymeCAGE-master"
DATA_DIR="${PROJECT_ROOT}/data/metatraits/metatraits_bulk_tsv_snapshot_20260818"
RETURN_ROOT="${PROJECT_ROOT}/HPC_Returned_Result_Summaries"
RETURN_DIR="${RETURN_ROOT}/${TASK_ID}"
ARCHIVE="${RETURN_ROOT}/${TASK_ID}.tar.gz"
IDENTITY="${RETURN_ROOT}/${TASK_ID}.tar.gz.identity.txt"

BASE_URL="https://www.bork.embl.de/~robbani/metatraits"
WORK_DIR="/tmp/metatraits_work_20260818"

log() { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $*"; }

# --------------------------------------------------------- conflict guard ----
if [[ -f "${ARCHIVE}" || -f "${IDENTITY}" ]]; then
  log "ABORT: ARCHIVE or IDENTITY already exists -> ${ARCHIVE} / ${IDENTITY}"
  log "Remove them manually if a full rerun is intended."
  exit 2
fi

mkdir -p "${DATA_DIR}" "${RETURN_DIR}" "${WORK_DIR}/headers"

# ----------------------------------------------- file metadata (14 rows) -----
# fields: file_name|role|required_summary_12|taxonomy_namespace|taxonomic_rank|prediction_scope
META_FILE="${WORK_DIR}/file_metadata.tsv"
cat > "${META_FILE}" <<'EOF'
gtdb_family_summary_all.tsv.gz|bulk_summary|true|gtdb|family|all
gtdb_family_summary_no_predictions.tsv.gz|bulk_summary|true|gtdb|family|no_predictions
gtdb_genus_summary_all.tsv.gz|bulk_summary|true|gtdb|genus|all
gtdb_genus_summary_no_predictions.tsv.gz|bulk_summary|true|gtdb|genus|no_predictions
gtdb_species_summary_all.tsv.gz|bulk_summary|true|gtdb|species|all
gtdb_species_summary_no_predictions.tsv.gz|bulk_summary|true|gtdb|species|no_predictions
ncbi_family_summary_all.tsv.gz|bulk_summary|true|ncbi|family|all
ncbi_family_summary_no_predictions.tsv.gz|bulk_summary|true|ncbi|family|no_predictions
ncbi_genus_summary_all.tsv.gz|bulk_summary|true|ncbi|genus|all
ncbi_genus_summary_no_predictions.tsv.gz|bulk_summary|true|ncbi|genus|no_predictions
ncbi_species_summary_all.tsv.gz|bulk_summary|true|ncbi|species|all
ncbi_species_summary_no_predictions.tsv.gz|bulk_summary|true|ncbi|species|no_predictions
GTDB2NCBI.tsv.gz|companion_crosswalk|false|crosswalk|mapping|mapping
NCBI2GTDB.tsv.gz|companion_crosswalk|false|crosswalk|mapping|mapping
EOF

# --------------------------------------------------- fetch official index ---
INDEX_HTML="${RETURN_DIR}/OFFICIAL_SOURCE_INDEX.html"
log "Fetching official index -> ${INDEX_HTML}"
curl -sL --fail --retry 5 --retry-delay 10 --connect-timeout 30 \
  -o "${INDEX_HTML}.part" "${BASE_URL}/" && mv "${INDEX_HTML}.part" "${INDEX_HTML}"
INDEX_FETCH_RC=$?
if [[ ${INDEX_FETCH_RC} -ne 0 ]]; then
  log "WARN: official index fetch failed (rc=${INDEX_FETCH_RC}); continuing with downloads anyway."
fi

# ------------------------------------------------------ download + validate -
CMD_LOG="${RETURN_DIR}/DOWNLOAD_COMMAND_LOG.txt"
RESULTS_TSV="${WORK_DIR}/results.tsv"
: > "${RESULTS_TSV}"
: > "${CMD_LOG}"

log "Starting download+validate loop for 14 files"

while IFS='|' read -r fname role req12 taxo rank scope; do
  [[ -z "${fname}" ]] && continue
  url="${BASE_URL}/${fname}"
  target="${DATA_DIR}/${fname}"
  part="${target}.part"
  hdrfile="${WORK_DIR}/headers/${fname}.header"

  log "=== ${fname} (role=${role}, taxo=${taxo}, rank=${rank}, scope=${scope}) ==="

  download_status="FAIL"
  notes=""
  need_download=1

  # skip if already present & valid
  if [[ -f "${target}" ]]; then
    if gzip -t "${target}" 2>/dev/null; then
      log "  already present + gzip -t OK -> skip download"
      download_status="PASS"
      need_download=0
      notes="skipped_download_already_validated"
    else
      log "  present but gzip -t FAIL -> redownload"
      rm -f "${target}"
      notes="redownload_due_to_gzip_test_fail"
    fi
  fi

  if [[ ${need_download} -eq 1 ]]; then
    max_outer=8
    for attempt in $(seq 1 ${max_outer}); do
      log "  download attempt ${attempt}/${max_outer}"
      {
        echo "# $(date -u +"%Y-%m-%dT%H:%M:%SZ") ${fname} attempt ${attempt}"
        if [[ -f "${part}" ]]; then
          echo "curl -L --fail --retry 3 --retry-delay 10 --connect-timeout 30 -C - -o \"${part}\" \"${url}\""
        else
          echo "curl -L --fail --retry 3 --retry-delay 10 --connect-timeout 30 -o \"${part}\" \"${url}\""
        fi
      } >> "${CMD_LOG}"
      if [[ -f "${part}" ]]; then
        curl -L --fail --retry 3 --retry-delay 10 --connect-timeout 30 \
             -C - -o "${part}" "${url}" 2>&1 | tail -n 2 | sed 's/^/    curl: /'
      else
        curl -L --fail --retry 3 --retry-delay 10 --connect-timeout 30 \
             -o "${part}" "${url}" 2>&1 | tail -n 2 | sed 's/^/    curl: /'
      fi
      rc=${PIPESTATUS[0]}
      if [[ ${rc} -eq 0 && -f "${part}" && -s "${part}" ]]; then
        download_status="PASS"
        break
      fi
      log "  attempt ${attempt} rc=${rc}, sleep 5 then retry"
      sleep 5
    done

    if [[ "${download_status}" == "PASS" ]]; then
      mv "${part}" "${target}"
    else
      rm -f "${part}"
      notes="${notes};download_failed_after_${max_outer}_attempts"
    fi
  fi

  # gzip -t
  gzip_status="FAIL"
  if [[ -f "${target}" ]] && gzip -t "${target}" 2>/dev/null; then
    gzip_status="PASS"
  elif [[ -f "${target}" ]]; then
    notes="${notes};gzip_test_fail"
  fi

  # size + sha256
  size_bytes=""
  sha256=""
  if [[ -f "${target}" ]]; then
    size_bytes=$(stat -c%s "${target}" 2>/dev/null || echo "")
    sha256=$(sha256sum "${target}" 2>/dev/null | awk '{print $1}')
  fi

  # header
  header_col_count=0
  : > "${hdrfile}"
  if [[ "${gzip_status}" == "PASS" ]]; then
    gzip -dc "${target}" 2>/dev/null | head -n 1 > "${hdrfile}"
    if [[ -s "${hdrfile}" ]]; then
      # count tab-separated columns
      header_col_count=$(awk -F'\t' '{print NF}' "${hdrfile}" | head -n 1)
    fi
  fi

  # data row count (with timeout)
  data_row_count=""
  row_count_status="SKIPPED_RUNTIME_BOUND"
  if [[ "${gzip_status}" == "PASS" ]]; then
    rc_timeout=0
    cnt=$(timeout 1800 bash -c "gzip -dc \"${target}\" 2>/dev/null | tail -n +2 | wc -l" 2>/dev/null) || rc_timeout=$?
    if [[ ${rc_timeout} -eq 0 ]]; then
      data_row_count="${cnt}"
      row_count_status="COUNTED"
    else
      row_count_status="SKIPPED_RUNTIME_BOUND"
      notes="${notes};rowcount_timeout_or_fail"
    fi
  fi

  validation_status="FAIL"
  if [[ "${download_status}" == "PASS" && "${gzip_status}" == "PASS" && -n "${sha256}" ]]; then
    validation_status="PASS"
  fi

  log "  result: download=${download_status} gzip=${gzip_status} validation=${validation_status} size=${size_bytes} cols=${header_col_count} rows=${data_row_count}(${row_count_status})"

  # results row (pipe-separated; header kept separately)
  printf '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n' \
    "${fname}" "${role}" "${req12}" "${taxo}" "${rank}" "${scope}" \
    "${url}" "${target}" "${size_bytes}" "${sha256}" "${gzip_status}" \
    "${header_col_count}" "${data_row_count}" "${row_count_status}" \
    "${download_status}" "${validation_status}" "${notes}" >> "${RESULTS_TSV}"
done < "${META_FILE}"

log "Download+validate loop finished."

# ----------------------------------------------------------- reports (py) ---
log "Generating report package via python3"
python3 - "${DATA_DIR}" "${RETURN_DIR}" "${WORK_DIR}" "${BASE_URL}" "${TASK_ID}" \
  "${ARCHIVE}" "${IDENTITY}" "${INDEX_HTML}" "${META_FILE}" "${RESULTS_TSV}" <<'PYEOF'
import csv, json, os, re, sys, datetime

DATA_DIR      = sys.argv[1]
RETURN_DIR    = sys.argv[2]
WORK_DIR      = sys.argv[3]
BASE_URL      = sys.argv[4]
TASK_ID       = sys.argv[5]
ARCHIVE       = sys.argv[6]
IDENTITY      = sys.argv[7]
INDEX_HTML    = sys.argv[8]
META_FILE     = sys.argv[9]
RESULTS_TSV   = sys.argv[10]

def now_utc():  return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def now_local(): return datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

# ---- load metadata ----
meta = {}  # fname -> dict
with open(META_FILE) as f:
    for line in f:
        line = line.rstrip("\n")
        if not line: continue
        p = line.split("|")
        meta[p[0]] = dict(role=p[1], required_summary_12=p[2], taxonomy_namespace=p[3],
                          taxonomic_rank=p[4], prediction_scope=p[5])

# ---- load results ----
res = {}  # fname -> dict
res_cols = ["file_name","role","required_summary_12","taxonomy_namespace","taxonomic_rank",
            "prediction_scope","official_url","chenyu_path","size_bytes","sha256",
            "gzip_test_status","header_column_count","data_row_count","row_count_status",
            "download_status","validation_status","notes"]
with open(RESULTS_TSV) as f:
    for line in f:
        line = line.rstrip("\n")
        if not line: continue
        p = line.split("|")
        d = dict(zip(res_cols, p))
        # load header line
        hdrfile = os.path.join(WORK_DIR, "headers", d["file_name"] + ".header")
        header_line = ""
        if os.path.exists(hdrfile):
            with open(hdrfile) as hf:
                header_line = hf.readline().rstrip("\n")
        d["header_line"] = header_line
        res[d["file_name"]] = d

# ---- parse official index HTML ----
index_rows = []
try:
    with open(INDEX_HTML, encoding="utf-8", errors="replace") as f:
        html = f.read()
    # each file row: <a href="X">X</a></td><td align="right">DATE  </td><td align="right">SIZE</td>
    pat = re.compile(r'<a href="([^"]+)">[^<]+</a></td>\s*<td align="right">([^<]*?)</td>\s*<td align="right">\s*([^<]*?)\s*</td>', re.S)
    for m in pat.finditer(html):
        name, lastmod, size = m.group(1), m.group(2).strip(), m.group(3).strip()
        if name in ("Parent Directory",) or name.endswith("/"):
            continue
        if not name.endswith(".tsv.gz"):
            continue
        role = "bulk_summary" if name in meta and meta[name]["role"] == "bulk_summary" \
               else ("companion_crosswalk" if name in meta and meta[name]["role"] == "companion_crosswalk"
                     else "other_upstream_file")
        index_rows.append({
            "file_name": name,
            "official_url": f"{BASE_URL}/{name}",
            "last_modified": lastmod,
            "size_from_index": size,
            "role": role,
            "required_summary_12": "true" if (name in meta and meta[name]["required_summary_12"]=="true") else "false",
        })
except Exception as e:
    pass  # index fetch may have failed

# ---- OFFICIAL_SOURCE_INDEX_PARSED.csv ----
idx_cols = ["file_name","official_url","last_modified","size_from_index","role","required_summary_12"]
with open(os.path.join(RETURN_DIR, "OFFICIAL_SOURCE_INDEX_PARSED.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=idx_cols)
    w.writeheader()
    for r in index_rows:
        w.writerow({k: r.get(k,"") for k in idx_cols})

idx_lookup = {r["file_name"]: r for r in index_rows}

# ---- METATRAITS_BULK_TSV_FILE_MANIFEST.csv ----
man_cols = ["file_name","role","required_summary_12","taxonomy_namespace","taxonomic_rank",
            "prediction_scope","official_url","official_last_modified_from_index",
            "official_size_from_index","chenyu_path","size_bytes","sha256","gzip_test_status",
            "header_column_count","data_row_count","row_count_status","download_status",
            "validation_status","notes"]
# order: 12 summary first (by meta order), then 2 crosswalks
ordered = list(meta.keys())
with open(os.path.join(RETURN_DIR, "METATRAITS_BULK_TSV_FILE_MANIFEST.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=man_cols)
    w.writeheader()
    for fname in ordered:
        m = meta[fname]
        r = res.get(fname, {})
        ix = idx_lookup.get(fname, {})
        row = {
            "file_name": fname,
            "role": m["role"],
            "required_summary_12": m["required_summary_12"],
            "taxonomy_namespace": m["taxonomy_namespace"],
            "taxonomic_rank": m["taxonomic_rank"],
            "prediction_scope": m["prediction_scope"],
            "official_url": r.get("official_url", f"{BASE_URL}/{fname}"),
            "official_last_modified_from_index": ix.get("last_modified", ""),
            "official_size_from_index": ix.get("size_from_index", ""),
            "chenyu_path": r.get("chenyu_path", os.path.join(DATA_DIR, fname)),
            "size_bytes": r.get("size_bytes", ""),
            "sha256": r.get("sha256", ""),
            "gzip_test_status": r.get("gzip_test_status", "FAIL"),
            "header_column_count": r.get("header_column_count", ""),
            "data_row_count": r.get("data_row_count", ""),
            "row_count_status": r.get("row_count_status", "SKIPPED_RUNTIME_BOUND"),
            "download_status": r.get("download_status", "FAIL"),
            "validation_status": r.get("validation_status", "FAIL"),
            "notes": r.get("notes", ""),
        }
        w.writerow(row)

# ---- SHA256SUMS.txt ----
with open(os.path.join(RETURN_DIR, "SHA256SUMS.txt"), "w") as f:
    for fname in ordered:
        r = res.get(fname, {})
        if r.get("sha256"):
            f.write(f"{r['sha256']}  {r.get('chenyu_path', os.path.join(DATA_DIR, fname))}\n")

# ---- GZIP_TEST_REPORT.csv ----
with open(os.path.join(RETURN_DIR, "GZIP_TEST_REPORT.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["file_name","chenyu_path","gzip_test_status","size_bytes"])
    for fname in ordered:
        r = res.get(fname, {})
        w.writerow([fname, r.get("chenyu_path",""), r.get("gzip_test_status","FAIL"), r.get("size_bytes","")])

# ---- HEADER_COLUMNS_LONG.csv ----
hdr_cols = ["file_name","column_index_1based","column_name","role","taxonomy_namespace","taxonomic_rank","prediction_scope"]
with open(os.path.join(RETURN_DIR, "HEADER_COLUMNS_LONG.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=hdr_cols)
    w.writeheader()
    for fname in ordered:
        m = meta[fname]
        r = res.get(fname, {})
        header_line = r.get("header_line","")
        if header_line:
            cols = header_line.split("\t")
            for i, c in enumerate(cols, start=1):
                w.writerow({
                    "file_name": fname,
                    "column_index_1based": i,
                    "column_name": c,
                    "role": m["role"],
                    "taxonomy_namespace": m["taxonomy_namespace"],
                    "taxonomic_rank": m["taxonomic_rank"],
                    "prediction_scope": m["prediction_scope"],
                })

# ---- C7_1_TRAIT_PANEL_FIELD_MAPPING_DRAFT.csv ----
# collect all column names observed (lowercased) -> set of files where seen
col_index = {}  # col_lower -> list of (fname, col_original)
for fname in ordered:
    r = res.get(fname, {})
    hl = r.get("header_line","")
    if hl:
        for c in hl.split("\t"):
            cl = c.strip().lower()
            if cl == "": continue
            col_index.setdefault(cl, []).append((fname, c))

def find_cols(keywords):
    hits = []
    for cl, occ in col_index.items():
        for kw in keywords:
            if kw in cl:
                for (fn, orig) in occ:
                    hits.append(f"{orig}@{fn}")
                break
    # dedupe preserving order
    seen=set(); out=[]
    for h in hits:
        if h not in seen:
            seen.add(h); out.append(h)
    return ", ".join(out)

trait_rules = [
    ("F1","oxygen_tolerance",["oxygen","aerobic","anaerobic","o2","microaerophil"," facultative"]),
    ("F2","temperature",["temperature","temp_","_temp","temp_range"]),
    ("F3","pH",["ph_opt","ph_range","ph_min","ph_max","_ph_","ph ","acidity"]),
    ("F4","salinity",["salinity","salin","nacl","salt"]),
    ("F5","bacdive_availability",[]),  # BacDive/local closure, not MetaTraits TSV
    ("F6","respiration_electron_acceptor",["electron_acceptor","acceptor","respiration","terminal_acceptor"]),
    ("F7","carbon_and_substrate_utilization",["carbon","substrate","utilization","c_source","sugar","carbohydrate","ferment"]),
    ("F8","degradation_capacity_broad",["degrad","hydrolysis","hydrolase","catabol","lipase","protease"]),
    ("F9","enzyme_activity",["enzyme","catalase","oxidase","urease"]),
    ("F10","motility",["motility","motile","flagell"]),
    ("F11","cell_morphology",["morphology","cell_shape","shape","rod","coccus"]),
    ("F12","cell_envelope_gram",["gram","envelope","cell_wall","peptidoglycan","stain"]),
    ("F13","sporulation",["sporulation","spore","endospore"]),
    ("F14","genome_basic",["genome","_gc","gc_","contig","cram","completeness","size"]),
    ("F15","habitat_generalism",["habitat","ecolog","environment","biotope"]),
]
policy = {
    "F1":"observed first; predicted soft-fill allowed when explicitly labelled",
    "F2":"observed first; predicted soft-fill allowed when explicitly labelled",
    "F3":"observed first; predicted soft-fill allowed when explicitly labelled",
    "F4":"observed first; predicted soft-fill allowed when explicitly labelled",
    "F5":"BacDive availability / culture collection; observed only; must not be predicted",
    "F6":"observed first; predicted soft-fill allowed when explicitly labelled",
    "F7":"observed first; predicted soft-fill allowed when explicitly labelled",
    "F8":"broad degradation context only; never claim exact pollutant degradation from it",
    "F9":"source-labelled context only; no hard rejection",
    "F10":"source-labelled context only; no hard rejection",
    "F11":"source-labelled context only; no hard rejection",
    "F12":"source-labelled context only; no hard rejection",
    "F13":"source-labelled context only; no hard rejection",
    "F14":"source-labelled context only; no hard rejection",
    "F15":"low-coverage ecological background only; must not participate in ranking",
}
# screens (first_screen) — best-effort label
screen = {
    "F1":"observed_trait","F2":"observed_trait","F3":"observed_trait","F4":"observed_trait",
    "F5":"observed_evidence_only","F6":"observed_trait","F7":"observed_trait",
    "F8":"broad_context_only","F9":"source_labelled","F10":"source_labelled",
    "F11":"source_labelled","F12":"source_labelled","F13":"source_labelled",
    "F14":"source_labelled","F15":"ecological_background",
}
summary_files_to_check = ", ".join([f for f in ordered if meta[f]["role"]=="bulk_summary"])

c7_cols = ["trait_id","trait_name","first_screen","teacher_policy",
           "metatraits_summary_files_to_check","candidate_tsv_columns_or_patterns",
           "mapping_status","notes"]
with open(os.path.join(RETURN_DIR, "C7_1_TRAIT_PANEL_FIELD_MAPPING_DRAFT.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=c7_cols)
    w.writeheader()
    for tid, tname, kws in trait_rules:
        if tid == "F5":
            cand = ""
            mstatus = "NOT_MAPPED_FROM_METATRAITS_TSV"
            notes = "F5 is BacDive/local culture-collection closure evidence, not MetaTraits TSV; must not be predicted."
            files_to_check = "(BacDive / local closure, not MetaTraits TSV)"
        else:
            cand = find_cols(kws)
            if cand:
                mstatus = "MAPPED_DRAFT"
                notes = "Draft keyword match against MetaTraits TSV headers; not a production mapping."
            else:
                mstatus = "NOT_MAPPED_FROM_METATRAITS_TSV"
                notes = "No matching MetaTraits TSV column found by draft keyword match."
            files_to_check = summary_files_to_check
        w.writerow({
            "trait_id": tid,
            "trait_name": tname,
            "first_screen": screen[tid],
            "teacher_policy": policy[tid],
            "metatraits_summary_files_to_check": files_to_check,
            "candidate_tsv_columns_or_patterns": cand,
            "mapping_status": mstatus,
            "notes": notes,
        })

# ---- counts + final status ----
req_total = 12
comp_total = 2
req_validated = sum(1 for fn in ordered if meta[fn]["role"]=="bulk_summary"
                    and res.get(fn,{}).get("validation_status")=="PASS")
comp_validated = sum(1 for fn in ordered if meta[fn]["role"]=="companion_crosswalk"
                     and res.get(fn,{}).get("validation_status")=="PASS")

req_downloaded = sum(1 for fn in ordered if meta[fn]["role"]=="bulk_summary"
                     and res.get(fn,{}).get("download_status")=="PASS")
comp_downloaded = sum(1 for fn in ordered if meta[fn]["role"]=="companion_crosswalk"
                      and res.get(fn,{}).get("download_status")=="PASS")

all_req_present = (req_downloaded == req_total)
all_req_gzip = all(res.get(fn,{}).get("gzip_test_status")=="PASS"
                   for fn in ordered if meta[fn]["role"]=="bulk_summary")
all_req_sha = all(bool(res.get(fn,{}).get("sha256"))
                  for fn in ordered if meta[fn]["role"]=="bulk_summary")
all_comp_present = (comp_downloaded == comp_total)
all_comp_gzip = all(res.get(fn,{}).get("gzip_test_status")=="PASS"
                    for fn in ordered if meta[fn]["role"]=="companion_crosswalk")

if (req_validated == req_total and comp_validated == comp_total):
    final_status = "METATRAITS_BULK_TSV_LANDED_CHENYU_COMPLETE"
else:
    final_status = "BLOCKED_METATRAITS_BULK_TSV_DOWNLOAD_OR_VALIDATION_FAILED"

# ---- VALIDATION_REPORT.json ----
vr = {
    "task_id": TASK_ID,
    "official_base_url": BASE_URL,
    "data_dir": DATA_DIR,
    "return_dir": RETURN_DIR,
    "required_summary_expected_count": req_total,
    "required_summary_downloaded_count": req_downloaded,
    "required_summary_validated_count": req_validated,
    "companion_crosswalk_expected_count": comp_total,
    "companion_crosswalk_downloaded_count": comp_downloaded,
    "companion_crosswalk_validated_count": comp_validated,
    "all_required_summary_present": all_req_present,
    "all_required_summary_gzip_test_pass": all_req_gzip,
    "all_required_summary_sha256_present": all_req_sha,
    "all_companion_crosswalk_present": all_comp_present,
    "all_companion_crosswalk_gzip_test_pass": all_comp_gzip,
    "final_status": final_status,
    "boundary_no_api_call": True,
    "boundary_no_prediction_run": True,
    "boundary_no_production_mutation": True,
    "generated_at_utc": now_utc(),
}
with open(os.path.join(RETURN_DIR, "VALIDATION_REPORT.json"), "w") as f:
    json.dump(vr, f, indent=2, sort_keys=False)
    f.write("\n")

# ---- VALIDATION_REPORT.md ----
def tf(b): return "true" if b else "false"
with open(os.path.join(RETURN_DIR, "VALIDATION_REPORT.md"), "w") as f:
    f.write(f"# MetaTraits bulk TSV validation report\n\n")
    f.write(f"- task_id: `{TASK_ID}`\n")
    f.write(f"- official_base_url: {BASE_URL}\n")
    f.write(f"- data_dir: `{DATA_DIR}`\n")
    f.write(f"- return_dir: `{RETURN_DIR}`\n\n")
    f.write(f"| metric | value |\n|---|---|\n")
    f.write(f"| required_summary_expected_count | {req_total} |\n")
    f.write(f"| required_summary_downloaded_count | {req_downloaded} |\n")
    f.write(f"| required_summary_validated_count | {req_validated} |\n")
    f.write(f"| companion_crosswalk_expected_count | {comp_total} |\n")
    f.write(f"| companion_crosswalk_downloaded_count | {comp_downloaded} |\n")
    f.write(f"| companion_crosswalk_validated_count | {comp_validated} |\n")
    f.write(f"| all_required_summary_present | {tf(all_req_present)} |\n")
    f.write(f"| all_required_summary_gzip_test_pass | {tf(all_req_gzip)} |\n")
    f.write(f"| all_required_summary_sha256_present | {tf(all_req_sha)} |\n")
    f.write(f"| all_companion_crosswalk_present | {tf(all_comp_present)} |\n")
    f.write(f"| all_companion_crosswalk_gzip_test_pass | {tf(all_comp_gzip)} |\n\n")
    f.write(f"## Final status\n\n")
    f.write(f"```\n{final_status}\n```\n\n")
    f.write(f"## Boundaries\n\n")
    f.write(f"- boundary_no_api_call: {tf(vr['boundary_no_api_call'])}\n")
    f.write(f"- boundary_no_prediction_run: {tf(vr['boundary_no_prediction_run'])}\n")
    f.write(f"- boundary_no_production_mutation: {tf(vr['boundary_no_production_mutation'])}\n\n")
    f.write(f"## Per-file outcome\n\n")
    f.write(f"| file | role | download | gzip | validation | size | sha256 (8) |\n")
    f.write(f"|---|---|---|---|---|---|---|\n")
    for fn in ordered:
        r = res.get(fn,{})
        sha8 = (r.get("sha256","")[:8]) if r.get("sha256") else ""
        f.write(f"| {fn} | {meta[fn]['role']} | {r.get('download_status','FAIL')} | "
                f"{r.get('gzip_test_status','FAIL')} | {r.get('validation_status','FAIL')} | "
                f"{r.get('size_bytes','')} | {sha8} |\n")

# ---- FINAL_STATUS.txt ----
with open(os.path.join(RETURN_DIR, "FINAL_STATUS.txt"), "w") as f:
    f.write(f"final_status={final_status}\n")
    f.write(f"DATA_DIR={DATA_DIR}\n")
    f.write(f"RETURN_DIR={RETURN_DIR}\n")
    f.write(f"ARCHIVE={ARCHIVE}\n")
    f.write(f"IDENTITY={IDENTITY}\n")
    f.write(f"required_summary_validated_count={req_validated}/{req_total}\n")
    f.write(f"companion_crosswalk_validated_count={comp_validated}/{comp_total}\n")
    f.write(f"generated_at_utc={now_utc()}\n")

# expose summary to bash
with open(os.path.join(WORK_DIR, "summary.env"), "w") as f:
    f.write(f"REQ_VALIDATED={req_validated}\n")
    f.write(f"COMP_VALIDATED={comp_validated}\n")
    f.write(f"FINAL_STATUS={final_status}\n")
PYEOF
PY_RC=$?
log "python report generation rc=${PY_RC}"
if [[ ${PY_RC} -ne 0 ]]; then
  log "ERROR: python report generation failed; aborting before archive."
  exit 3
fi
source "${WORK_DIR}/summary.env"

# ---------------------------------------------------- MANIFEST + archive -----
log "Building MANIFEST.files / MANIFEST.sha256"
pushd "${RETURN_DIR}" >/dev/null
find . -type f ! -name MANIFEST.files ! -name MANIFEST.sha256 | sort | sed 's|^\./||' > MANIFEST.files
: > MANIFEST.sha256
while IFS= read -r mf; do
  [[ -z "${mf}" ]] && continue
  sha=$(sha256sum "${mf}" | awk '{print $1}')
  printf '%s  %s\n' "${sha}" "${mf}" >> MANIFEST.sha256
done < MANIFEST.files
popd >/dev/null

log "Creating metadata-only archive -> ${ARCHIVE}"
tar -czf "${ARCHIVE}" -C "${RETURN_ROOT}" "${TASK_ID}"
ARCHIVE_SIZE=$(stat -c%s "${ARCHIVE}")
ARCHIVE_SHA=$(sha256sum "${ARCHIVE}" | awk '{print $1}')
CREATED_UTC=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CREATED_LOCAL=$(date +"%Y-%m-%dT%H:%M:%S%z")

log "Writing identity sidecar -> ${IDENTITY}"
cat > "${IDENTITY}" <<EOF
task_id=${TASK_ID}
archive_path=${ARCHIVE}
archive_size_bytes=${ARCHIVE_SIZE}
archive_sha256=${ARCHIVE_SHA}
single_root_dir=${TASK_ID}
data_dir=${DATA_DIR}
required_summary_expected_count=12
required_summary_validated_count=${REQ_VALIDATED}
companion_crosswalk_expected_count=2
companion_crosswalk_validated_count=${COMP_VALIDATED}
final_status=${FINAL_STATUS}
created_at_utc=${CREATED_UTC}
created_at_local=${CREATED_LOCAL}
EOF

log "============================================================"
log "FINAL_STATUS=${FINAL_STATUS}"
log "DATA_DIR=${DATA_DIR}"
log "RETURN_DIR=${RETURN_DIR}"
log "ARCHIVE=${ARCHIVE}"
log "IDENTITY=${IDENTITY}"
log "required_summary_validated_count=${REQ_VALIDATED}/12"
log "companion_crosswalk_validated_count=${COMP_VALIDATED}/2"
log "archive_sha256=${ARCHIVE_SHA}"
log "DONE."
