#!/usr/bin/env bash
source "${C8P_PAYLOAD_DIR:?}/worker_common.sh"
load_target genomespot_indices.txt
[[ "${RUN_GENOMESPOT}" == true ]]
sha_gate "${PROTEIN_PATH}" "${PROTEIN_SHA256}"
[[ -s "${GENOME_PATH}" ]]
SCRATCH=/tmp/${USER}/c8p_prod_genomespot_${SLURM_JOB_ID}_${ASSEMBLY_ACCESSION}
RESULT=${RUN_ROOT}/stages/genomespot/${ASSEMBLY_ACCESSION}
PARTIAL=${RUN_ROOT}/failed_partials/genomespot/${ASSEMBLY_ACCESSION}_${SLURM_JOB_ID}
mkdir -p "${SCRATCH}" "$(dirname "${RESULT}")" "$(dirname "${PARTIAL}")"
trap 'rc=$?; if (( rc != 0 )); then cp -a "${SCRATCH}" "${PARTIAL}"; fi; rm -rf "${SCRATCH}"; exit "${rc}"' EXIT
[[ ! -e "${RESULT}" ]]
run_container "${GENOMESPOT_SIF}" python -m genome_spot.genome_spot \
    --models "${GENOMESPOT_MODELS}" --contigs "${GENOME_PATH}" --proteins "${PROTEIN_PATH}" \
    --output "${SCRATCH}/${GENOME_ID}.genomespot"
[[ -s "${SCRATCH}/${GENOME_ID}.genomespot.predictions.tsv" ]]
mv "${SCRATCH}" "${RESULT}"
trap - EXIT

