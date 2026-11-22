#!/usr/bin/env bash
source "${C8P_PAYLOAD_DIR:?}/worker_common.sh"
load_target all_indices.txt
SCRATCH=/tmp/${USER}/c8p_prod_e2m_${SLURM_JOB_ID}_${ASSEMBLY_ACCESSION}
RESULT=${RUN_ROOT}/stages/e2m/${ASSEMBLY_ACCESSION}
PARTIAL=${RUN_ROOT}/failed_partials/e2m/${ASSEMBLY_ACCESSION}_${SLURM_JOB_ID}
mkdir -p "${SCRATCH}/e2m" "$(dirname "${RESULT}")" "$(dirname "${PARTIAL}")"
trap 'rc=$?; if (( rc != 0 )); then cp -a "${SCRATCH}" "${PARTIAL}"; fi; rm -rf "${SCRATCH}"; exit "${rc}"' EXIT
[[ ! -e "${RESULT}" ]]
if [[ "${RUN_E2M}" == true ]]; then
    if [[ "${RUN_EGGNOG}" == true ]]; then
        ANNOTATION=${RUN_ROOT}/stages/eggnog/${ASSEMBLY_ACCESSION}/${GENOME_ID}.emapper.annotations
        (cd "${RUN_ROOT}/stages/eggnog/${ASSEMBLY_ACCESSION}" && sha256sum -c STAGE.sha256 >/dev/null)
    else
        ANNOTATION=${ANNOTATION_PATH}
        sha_gate "${ANNOTATION}" "${ANNOTATION_SHA256}"
    fi
    run_container "${MICRO_SIF}" emapper2matrix.py --input-file "${ANNOTATION}" \
        --pfam-map-file "${PFAM_MAP}" --outdir "${SCRATCH}/e2m"
    apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
        "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/prepare_e2m.py" \
        --directory "${SCRATCH}/e2m" --accession "${ASSEMBLY_ACCESSION}" \
        --report "${SCRATCH}/E2M_COMPLETE.json"
else
    sha_gate "${KO_PATH}" "${KO_SHA256}"
    sha_gate "${PFAM_PATH}" "${PFAM_SHA256}"
    apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
        "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/prepare_e2m.py" \
        --directory "${SCRATCH}/e2m" --accession "${ASSEMBLY_ACCESSION}" \
        --source-ko "${KO_PATH}" --source-pfam "${PFAM_PATH}" \
        --report "${SCRATCH}/E2M_COMPLETE.json"
fi
mv "${SCRATCH}" "${RESULT}"
trap - EXIT
