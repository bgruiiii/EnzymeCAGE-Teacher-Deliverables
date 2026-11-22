#!/usr/bin/env bash
ASSET_ROOT=/public/home/aclhl3hbth/c8p_portraits_assets_20260826/portraits/v0.2.1
EXTRACT_ROOT=${ASSET_ROOT}/extracted_assets/c8_p4c_20260823
SIF_ROOT=${ASSET_ROOT}/containers/sif
SOURCE_ROOT=${ASSET_ROOT}/source/porTraits_945795b5a6577f881c451f292eb3a60d94d33eed
P7C_ROOT=/public/home/aclhl3hbth/HPC_Work/scnet_c8p_p7c_direct_recognise_markers_validate_install_resume_smoke_then_412_20260828
SOURCE_RUN_ROOT=/public/home/aclhl3hbth/HPC_Work/scnet_c8p_stage_targeted_production_20260908
RUN_ROOT=/public/home/aclhl3hbth/HPC_Work/scnet_c8p_stage_targeted_production_resume1_20260910
RETURN_ROOT=/public/home/aclhl3hbth/HPC_Returned_Result_Summaries
RETURN_ARCHIVE=${RETURN_ROOT}/scnet_c8p_stage_targeted_production_resume1_result_20260910.tar.gz

GENOMESPOT_SIF=${SIF_ROOT}/genomespot_docker_v1.0.1plus.sif
EGGNOG_SIF=${SIF_ROOT}/eggnog_mapper_2.1.12_pyhdfd78af_2.sif
MICRO_SIF=${SIF_ROOT}/portrait_sklearn_v1.2.2_micropherret.sif
TRAIT_SIF=${SIF_ROOT}/portrait_sklearn_v1.4.0_traitar_bacdive.sif
COLLATE_SIF=${SIF_ROOT}/portraits_metatraits_with_pandas.sif

GENOMESPOT_MODELS=${EXTRACT_ROOT}/portraits_db/GenomeSPOT/models
EGGNOG_DB=${EXTRACT_ROOT}/eggnog/emapperdb-5.0.2
PFAM_MAP=${EGGNOG_DB}/pfam/Pfam-A.clans.tsv.gz
MICRO_MODELS=${EXTRACT_ROOT}/portraits_db/MICROPHERRET
BACDIVE_MODELS=${EXTRACT_ROOT}/portraits_db/BacDive-AI/models
TRAITAR_MODELS=${EXTRACT_ROOT}/portraits_db/Traitar
TRAITS_INFO=${SOURCE_ROOT}/assets/traits_info.json
TRAITS_HARMONIZED=${SOURCE_ROOT}/assets/traits_harmonized.json
VERSIONS_JSON=${SOURCE_ROOT}/assets/versions.json
