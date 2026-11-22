#!/usr/bin/env bash
source "${C8P_PAYLOAD_DIR:?}/worker_common.sh"
SHARD=${SLURM_ARRAY_TASK_ID:?array task required}
SHARD_FILE=${HERE}/eggnog_shard_${SHARD}.txt
[[ -s "${SHARD_FILE}" ]]
SCRATCH=/tmp/${USER}/c8p_prod_eggnog_shard_${SLURM_ARRAY_JOB_ID}_${SHARD}
LOCAL_DB=${SCRATCH}/db
AVAILABLE=$(df --output=avail -B1 /tmp | tail -1 | tr -d ' ')
(( AVAILABLE >= 70*1024*1024*1024 ))
mkdir -p "${LOCAL_DB}"
trap 'rm -rf "${SCRATCH}"' EXIT
cp -a "${EGGNOG_DB}/." "${LOCAL_DB}/"
[[ $(stat -c %s "${LOCAL_DB}/eggnog.db") == 41370988544 ]]
[[ $(stat -c %s "${LOCAL_DB}/eggnog_proteins.dmnd") == 9285439161 ]]
[[ $(sha256sum "${LOCAL_DB}/eggnog.db" | awk '{print $1}') == 4d6857c129423889edcd607995b28d97944787a588224f31dd7f745fe9ef1e4f ]]
[[ $(sha256sum "${LOCAL_DB}/eggnog_proteins.dmnd" | awk '{print $1}') == f4b63db0313021e4a2ca1d47a6b3f7862a3c8c2016abf3b51ef5865e653642a7 ]]
failures=0
while IFS= read -r target_index; do
    [[ -n "${target_index}" ]] || continue
    if ! bash "${HERE}/run_eggnog_one.sh" "${target_index}" "${LOCAL_DB}"; then
        failures=$((failures + 1))
    fi
done < "${SHARD_FILE}"
(( failures == 0 ))
