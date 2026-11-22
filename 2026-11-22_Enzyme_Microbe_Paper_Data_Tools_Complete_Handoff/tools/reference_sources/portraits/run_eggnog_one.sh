#!/usr/bin/env bash
source "${C8P_PAYLOAD_DIR:?}/worker_common.sh"
TARGET_INDEX=${1:?target index required}
LOCAL_DB=${2:?local database required}
eval "$(apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
    "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/get_target.py" "${HERE}/targets.tsv" "${TARGET_INDEX}")"
GENOME_ID=${ASSEMBLY_ACCESSION}_genomic
[[ "${RUN_EGGNOG}" == true ]]
sha_gate "${PROTEIN_PATH}" "${PROTEIN_SHA256}"
SCRATCH=/tmp/${USER}/c8p_prod_eggnog_${SLURM_JOB_ID}_${ASSEMBLY_ACCESSION}
RESULT=${RUN_ROOT}/stages/eggnog/${ASSEMBLY_ACCESSION}
PARTIAL=${RUN_ROOT}/failed_partials/eggnog/${ASSEMBLY_ACCESSION}_${SLURM_JOB_ID}
mkdir -p "${SCRATCH}" "$(dirname "${RESULT}")" "$(dirname "${PARTIAL}")"
trap 'rc=$?; if (( rc != 0 )); then cp -a "${SCRATCH}" "${PARTIAL}"; fi; rm -rf "${SCRATCH}"; exit "${rc}"' EXIT
[[ ! -e "${RESULT}" ]]
run_container "${EGGNOG_SIF}" emapper.py -i "${PROTEIN_PATH}" --data_dir "${LOCAL_DB}" \
    --output "${SCRATCH}/${GENOME_ID}" -m diamond --cpu "${SLURM_CPUS_PER_TASK:-32}" --dmnd_algo 0
for suffix in .emapper.annotations .emapper.hits .emapper.seed_orthologs; do
    [[ -s "${SCRATCH}/${GENOME_ID}${suffix}" ]]
done
(cd "${SCRATCH}" && sha256sum "${GENOME_ID}.emapper.annotations" \
    "${GENOME_ID}.emapper.hits" "${GENOME_ID}.emapper.seed_orthologs" > STAGE.sha256)
mv "${SCRATCH}" "${RESULT}"
trap - EXIT
