#!/usr/bin/env bash
set -euo pipefail
HERE=${C8P_PAYLOAD_DIR:?payload directory required}
source "${HERE}/config.sh"
set +u
source /etc/profile || true
set -u
module purge || true
module load apps/apptainer/1.3.4

run_container() {
    local image=$1
    shift
    apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
        "${image}" /bin/bash -c 'export PATH="$PATH:$1"; shift; exec "$@"' \
        bash "${SOURCE_ROOT}/bin" "$@"
}

load_target() {
    local stage_indices=$1
    local target_index
    target_index=$(apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
        "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/stage_index.py" \
        "${HERE}/${stage_indices}" "${SLURM_ARRAY_TASK_ID}")
    eval "$(apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
        "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/get_target.py" \
        "${HERE}/targets.tsv" "${target_index}")"
    GENOME_ID=${ASSEMBLY_ACCESSION}_genomic
}

sha_gate() {
    local path=$1 expected=$2
    [[ -f "${path}" && $(sha256sum "${path}" | awk '{print $1}') == "${expected}" ]]
}

