#!/usr/bin/env bash
source "${C8P_PAYLOAD_DIR:?}/worker_common.sh"
load_target "${1:?batch index file required}"
SCRATCH=/tmp/${USER}/c8p_prod_downstream_${SLURM_JOB_ID}_${ASSEMBLY_ACCESSION}
RESULT=${RUN_ROOT}/results/${ASSEMBLY_ACCESSION}
PARTIAL=${RUN_ROOT}/failed_partials/downstream/${ASSEMBLY_ACCESSION}_${SLURM_JOB_ID}
ROOT=${SCRATCH}/${GENOME_ID}
mkdir -p "${ROOT}/e2m" "$(dirname "${RESULT}")" "$(dirname "${PARTIAL}")"
trap 'rc=$?; if (( rc != 0 )); then cp -a "${SCRATCH}" "${PARTIAL}"; fi; rm -rf "${SCRATCH}"; exit "${rc}"' EXIT
[[ ! -e "${RESULT}" ]]
E2M=${RUN_ROOT}/stages/e2m/${ASSEMBLY_ACCESSION}/e2m
cp "${E2M}/${GENOME_ID}.emapper.KEGG_ko.tsv.gz" "${ROOT}/e2m/"
cp "${E2M}/${GENOME_ID}.emapper.PFAMs.tsv.gz" "${ROOT}/e2m/"
KO=${ROOT}/e2m/${GENOME_ID}.emapper.KEGG_ko.tsv.gz
PFAM=${ROOT}/e2m/${GENOME_ID}.emapper.PFAMs.tsv.gz

if [[ "${REUSE_DOWNSTREAM}" == true ]]; then
    apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
        "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/copy_keep_files.py" \
        --table "${HERE}/keep_downstream_files.tsv" --accession "${ASSEMBLY_ACCESSION}" \
        --output "${ROOT}" --exclude-e2m
else
    [[ "${RUN_NATIVE_DOWNSTREAM}" == true ]]
    mkdir -p "${ROOT}/micropherret" "${ROOT}/bacdive_ai" "${ROOT}/traitar"
    micro_rc=0
    run_container "${MICRO_SIF}" KO2MICROPHERRET.py --ko-matrix "${KO}" \
        --model-dir "${MICRO_MODELS}" --outdir "${ROOT}/micropherret" || micro_rc=$?
    printf '%s\n' "${micro_rc}" > "${ROOT}/micropherret/tool_exit_code.txt"
    [[ -s "${ROOT}/micropherret/MICROPHERRET.prob.tsv.gz" && -s "${ROOT}/micropherret/MICROPHERRET.binary.tsv.gz" ]]
    run_container "${TRAIT_SIF}" PFAM2BacDive-AI.py --pfam-matrix "${PFAM}" \
        --model-dir "${BACDIVE_MODELS}" --outdir "${ROOT}/bacdive_ai"
    run_container "${TRAIT_SIF}" PFAM2Traitar.py --pfam-matrix "${PFAM}" \
        --model-dir "${TRAITAR_MODELS}" --outdir "${ROOT}/traitar" --voters 5
fi

apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
    "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/finalize_downstream.py" \
    --root "${ROOT}" --accession "${ASSEMBLY_ACCESSION}" --model-root "${MICRO_MODELS}" \
    --report "${SCRATCH}/DOWNSTREAM_VALIDATION.json"
apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
    "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/make_complete.py" \
    --root "${SCRATCH}" --accession "${ASSEMBLY_ACCESSION}" \
    --report "${SCRATCH}/DOWNSTREAM_VALIDATION.json"
mv "${SCRATCH}" "${RESULT}"
trap - EXIT
