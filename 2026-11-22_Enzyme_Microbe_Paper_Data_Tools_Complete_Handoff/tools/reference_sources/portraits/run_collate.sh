#!/usr/bin/env bash
source "${C8P_PAYLOAD_DIR:?}/worker_common.sh"
WORK=${RUN_ROOT}/collate_work
[[ ! -e "${WORK}" ]]
[[ $(find "${RUN_ROOT}/results" -mindepth 2 -maxdepth 2 -name COMPLETE.json -type f | wc -l) == 412 ]]
apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
    "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/build_collate_input.py" \
    --targets "${HERE}/targets.tsv" --run-root "${RUN_ROOT}" --source-run-root "${SOURCE_RUN_ROOT}" --output "${WORK}" \
    --traits-info "${TRAITS_INFO}" --traits-harmonized "${TRAITS_HARMONIZED}" --versions "${VERSIONS_JSON}"
apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
    "${COLLATE_SIF}" /bin/bash -ue -c \
    "export PATH=\"\$PATH:${SOURCE_ROOT}/bin\"; cd '${WORK}'; mkdir collated; collate_results.py -i . -o collated/ --traits_info traits_info.json --traits_harmonized traits_harmonized.json --versions versions.json"
apptainer exec --no-home --pid --cleanenv --bind /public/home/aclhl3hbth,/tmp \
    "${MICRO_SIF}" /opt/conda/bin/python "${HERE}/validate_collate.py" \
    --file "${WORK}/collated/portraits_results.tsv.gz" --targets "${HERE}/targets.tsv" \
    --json "${WORK}/PRODUCTION_COLLATE_COMPLETE.json"
mkdir "${RUN_ROOT}/collate_result"
cp "${WORK}/collated/portraits_results.tsv.gz" "${RUN_ROOT}/collate_result/"
cp "${WORK}/PRODUCTION_COLLATE_COMPLETE.json" "${RUN_ROOT}/collate_result/"
