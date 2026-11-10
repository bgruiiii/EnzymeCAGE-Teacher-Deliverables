"""R3 max-coverage round: registered path constants (read-only sources + NEWROOT writes)."""
WS = "/usrdata/EnzymeCAGE_data/workspaces/current95_ngpu32g_20261031"
NEWROOT = WS + "/five_model_complete_20261103"
PREVROOT = WS + "/max_coverage_three_model_20261103"
from pathlib import Path
PKG = str(Path(__file__).resolve().parents[1])
R1 = WS + "/current95_dual600m_fasttrack_r1_20261102"
BUNDLE = R1 + "/current95_600m_dual_fasttrack_r1_20261102"
R2 = WS + "/current95_dual600m_r2_scoring_20261102"
A109 = WS + "/a109_admission_resume_20261102_run"
R3 = WS + "/asset_repair_r3_20261101/output"
S5 = "/usrdata/EnzymeCAGE_data/workspaces/biosysmodb121_final_reaction_rescue_pre_enzyme_ranking_asset_closure_20261006/S5_protein_assets"
OLDR3 = "/usrdata/EnzymeCAGE_data/workspaces/biosysmodb121_pre_ranking_r1_reaction_protein_asset_gold_closure_20261008/R3_structure_protein"
P291 = "/usrdata/EnzymeCAGE_data/workspaces/p291_legacy600m_20260922"
P291_ASSETS = P291 + "/runtime/assets"
TRAIN = "/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922"
S10 = TRAIN + "/10_full_training_enzgfm_then_esmc_continuation_r1_20260926"
S8CODE = TRAIN + "/08_loader_code_smoke_20260924/code"
WR = TRAIN + "/s11_r1_self_included_four_model_20260927"
FEAT = "/usrdata/EnzymeCAGE_data/feature/protein"
REPO_OLD = "/usrdata/EnzymeCAGE_data/EnzymeCAGE-master"
WRAP = REPO_OLD + "/HPC_Returned_Result_Summaries/d4b1a_wrapper_hash_relative_path_final_package_correction_20260716"
CARRIER_PARQUET = TRAIN + "/02_carrier_uid_and_pocket/SEQUENCE_TO_CARRIER_UID_ALL.parquet"
CORR_JSONL = FEAT + "/esmc600m_corrected_pocket_107705_20260713/metadata/final_corrected_pocket_indices.jsonl"
ESM_ROOT = "/usrdata/EnzymeCAGE_data/models/esmc_600m"
ESMC_WEIGHTS_SHA = "8ef856e1a237ee3f995442df997a962e70057faadecf38fc0c8561bd3c2f4324"
GF_PY = "/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python"
ESMC_PY = "/usrdata/EnzymeCAGE_envs/esm_extraction_py312/bin/python"
CTXS = ("main", "delta15")
RXN = {ctx: R3 + f"/materialize_{ctx}/merged/reaction" for ctx in CTXS}
STORES = {
    "legacy_global_formal": FEAT + "/ESM-C_600M_baseline_1152_round1_20260708/protein_level/seq2feature.pkl",
    "legacy_pocket_native": FEAT + "/ESM-C_600M_baseline_1152_round1_20260708/pocket_node_feature/esm_node_feature.torch.pt",
    "gvp_flat": FEAT + "/gvp/gvp_protein_feature_flat.pt",
    "corrected_pocket": FEAT + "/esmc600m_corrected_pocket_107705_20260713/pocket_node_feature/esm_node_feature.torch.pt",
    "gvp_s3_new": TRAIN + "/03_gvp_assets/gvp_protein_feature_s3_new.pt",
    "gvp_r1_overlay": WR + "/assets/gvp_r1_overlay.pt",
    "s10_out": TRAIN + "/04_plm_assets/esmc/out",
    "s11_gen2_out": WR + "/assets/esmc_gen2/out",
}
CKPT = {
    "legacy_esm2_3b": REPO_OLD + "/HPC_Returned_Result_Summaries/enzymecage_v1_20260714/3b_ensemble/seed_{seed}/best_model.pth",
    "legacy_esmc600m": REPO_OLD + "/HPC_Returned_Result_Summaries/enzymecage_v1_20260714/600m_ensemble/seed_{seed}/best_model.pth",
    "new_esmc600m": S10 + "/esmc600m/seed_{seed}/best_model.pth",
}
SEEDS = [40, 41, 42, 43, 44]
ARMS3 = ("legacy_esm2_3b", "legacy_esmc600m", "new_esmc600m")
