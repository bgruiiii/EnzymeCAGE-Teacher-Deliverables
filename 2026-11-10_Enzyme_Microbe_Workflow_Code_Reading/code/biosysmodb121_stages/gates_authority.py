# -*- coding: utf-8 -*-
"""Contract-frozen authority constants for BIOSYSMOdb121 (master contract
B121_STEP_RANK_V1, sections 2/3/4/5.3/7). Transcribed verbatim from the
staged instruction files; the B0-B2 validators compare live recomputation
against these constants. Editing this file is equivalent to editing the
contract and is detected by the stage validators.
"""

# ---- section 2: frozen semantic counts (independently recomputable) ----
COUNTS = {
    "formal_cases": 121,
    "quarantine": 29,
    "reaction_gold_participant_rows": 2473,
    "unique_case_step": 533,
    "unique_source_reaction_id": 460,
    "unique_reaction_id_orientation": 460,
    "enzyme_gold_rows": 1355,
    "unique_enzyme_step_links": 1349,
    "unique_enzyme_ids": 880,
    "sequence_availability_TRUE": 687,
    "sequence_availability_FALSE": 668,
    "organism_rows": 2215,
    "organism_STEP_rows": 1869,
    "organism_PATHWAY_COMPLETE_rows": 346,
    "fasta_records": 42053,
    "fasta_unique_headers": 42053,
    "fasta_unique_sequences": 29627,
    "fasta_duplicate_records": 12426,
}
# normalized EC kinds (373 includes incomplete/missing; gate is informational
# only in B0 because the normalization function is ours; must recompute ==373
# with str.strip() over non-empty ec_number_normalized values)
EC_KINDS = 373

# ---- section 3: G1 file SHA gates, relative to package G1_gold/ ----
G1_GATES = {
    "G1_gold/G1_gold.manifest.json":
        "c424763cd4c38fcaac1b178979efb3f18f2b77039369ab6b8c709eab42dce06e",
    "G1_gold/formal_cases.tsv":
        "1749f9a5c272220dfae201d1945526b0f1e35b8e66b2e8a9e31ccee177e29296",
    "G1_gold/reaction_gold.tsv":
        "16e5946c713fb95f3bc6c68957613f6b7ef4e563ee805b4148e3ba454e44bd61",
    "G1_gold/enzyme_gold.tsv":
        "4a62f1cddd632fa9a4c6b504055bbc1ba746f88c9407f28049b67bdd19475c94",
    "G1_gold/organism_gold.tsv":
        "39baf51041a9169f79a588465e6c00cf3f64bd5920a7f838483f139106a3ff6a",
    "G1_gold/case_root_identity.tsv":
        "48622d86861bd1f7a121462d18eb126d7fc6b659ff9b93ea141ed0f0c05d32f9",
    "G1_gold/counts.json":
        "3045a07ef0c2fca7478870c5c19c941e19ecc07d496e09f6534a77e887b603b9",
    "gates/G1_gold.stage_gate.json":
        "36ec60ffe1285d57adaad161455aa6f75010e9e4a726b5d49cc3a1399add4c1a",
    "approval/TEACHER_REPLY_BIOSYSMODB150_G1_APPROVAL_2026-09-27.md":
        "39e08c219aa155d21e687db0976b1fd4df06d1c3d2b8c738ca847bafa47657dd",
}

RAW_GATES = {
    "raw/BIOSYSMOdb_Enzymes_v1.0.csv":
        "dda287d19d2e9f0130da0acb4f63928515c69a5267687fa851bd399ff44b65af",
    "raw/BIOSYSMOdb_ProteinDegradativespace-Annot_v1.0.csv":
        "3fd3aabbef8c9d9930ec4132966f2adf362d94e031255c0fb8c848f2214a20b7",
    "raw/BIOSYSMOdb_ProteinDegradativespace_v1.0.fasta":
        "905135b2c634ad2ed079ab70331d0cd024461cc0342ecc71ca93aff445d3e7d5",
    "raw/BIOSYSMOdb_Reactions_v1.0.csv":
        "43394879e02a6d4987baddce34b8c7879490fb26c30210a1c590bef0a817a847",
    "raw/BIOSYSMOdb_Compounds_chemical_iden_v1.0.csv":
        "3875ad3e74afa69cff31d2fa0bc1f26529c4cc82983f5c9a8c4b6b7549ec2ab0",
    "raw/BIOSYSMOdb_Compounds_chemical_info_v1.0.csv":
        "2586ad50343bfe3c3a776e8390c791bb376801630f1d320dbc7f70b15b76d189",
    "raw/BIOSYSMOdb_Organisms_v1.0.csv":
        "15410b327e87f636baa4806d66283d97cf498e273b15e40ea3a60d8137172f22",
    "raw/LICENSE.txt":
        "7225703a3676167e10522449ad3edda17f30e2234c10f38e1f64ada5ea0786f3",
}

# ---- section 4: historical archives by basename -> sha ----
ARCHIVE_GATES = {
    "enzymecage_pollutant_biodegradation_category_capacity_census_r0_20260920.tar.gz":
        "04d593bdb07488534f569dd7c6521794fda559057faa9ec7019407ad9c2ee7a2",
    "expanded_reaction_enzyme_phase1_r3_retrieval_dbp_20260914.tar.gz":
        "e7dca93e4507ff7437fc9cd19f89cde8a582e3f4f2923bafab62a5af72746efc",
    "enzymecage_v6_s11_r1_self_included_four_model_ensemble_ranking_20260927.tar.gz":
        "12bf22b2db9db818578af41bdc6c96dd6ac28ab2bc5dcd88f4e4d1e49103845a",
    "pollutant291_p2rank_legacy600m_model_matched_dual5seed_rerun_20260922.tar.gz":
        "de3f889bc95f4fe7efa4dc0ec7a1e421cf63ef972dc355ffe5a1a262e2e6a6d4",
    "pollutant298_training_compatible_reactions_local_payload_20260922.tar.gz":
        "cba5771c165120773e1b1c81a323e371718a3d0095ce1c7fa49fa27059936a41",
}

CLEANING_SCRIPT_SHA = ("77e3f770ab73052a837e5708ecad608c1a8f2956eef93f2"
                       "940b2f87fbddf2d14")

# ---- section 4: checkpoint SHA gates ----
CKPT_GATES = {
    ("legacy_esm2_3b", 40): "a95d4687e2cadad1c12f7c1defd21dbdf43db3cce96aa9caace39dbcc226586d",
    ("legacy_esm2_3b", 41): "c429a98bc265e20d415c3d6f479e0f0d6c47d81c13135c589e2a5e173978dbef",
    ("legacy_esm2_3b", 42): "cc54be33a23b78fb89c183f0bca6f87b442a5be4dad9666428d05a72a9b7f7a3",
    ("legacy_esm2_3b", 43): "3eb80be83cb41574204239c80f11008f728029dd9e4ba14c639749d8176b5220",
    ("legacy_esm2_3b", 44): "b9547d3ba17725a5910cf243d33af9367abb12b3215f4b526405f8bdb14acd16",
    ("legacy_esmc600m", 40): "7ca5a6f7d549fedb16a6a410e4afe4f890cfe26b51c17cb64b1acb026aee6c1d",
    ("legacy_esmc600m", 41): "2d163728ec1381694ba20f9816c8e17c744bee15b083461bfca9ae72342dc98f",
    ("legacy_esmc600m", 42): "34ffb52daf66219e482c474f2d2f75614e49c16bca497cd13b226ab84f74934e",
    ("legacy_esmc600m", 43): "f8a9e883fa09e94b4e75d830610be761e1a0efabd25eac5f23f11a0660e6498a",
    ("legacy_esmc600m", 44): "b236ea99317743c265f7402e6c602faa28b926550cac43a83f8d0eb7969003a5",
    ("new_enzgfm650m", 40): "d185923cffc863e4e363ba00c00433dfa8808c91b2ea4474de15ecd69b235cdf",
    ("new_enzgfm650m", 41): "a0a7be616d2aa3251fcc494c558265b394b2d6df303e0da9933fa81be01fa1d1",
    ("new_enzgfm650m", 42): "2f7c5462d1e0e4b67dcb73a7ba448d9e92ab92fa0826f9f74acf4f3d8d1b2542",
    ("new_enzgfm650m", 43): "3e3485c49f0cb3dd8199acbf05e7f7785e4fe495b3c6d974a135c4201eb72c46",
    ("new_enzgfm650m", 44): "a8005c535ebfdd3713cd208ce61b5ccdebe32c7c6ebe8ca901aef288da1d4eec",
}

# ---- section 5.3: cleaning order and parity expectation ----
CLEANING_ORDER = [
    "remove_redundent_from_rxn",
    "filter_unwanted_rxn",
    "neutralize_rxn",
    "cano_rxn",
]
CANO_KWARGS = {"remain_isomer": True, "exchange_pos": False}
PARITY_EXPECT = {"CHANGED": 151, "UNCHANGED": 140, "HOLD": 7, "TOTAL": 298}

# ---- section 7: R0 library identities (recomputed in B2) ----
R0 = {
    "reactions": 29061,
    "pairs": 292582,
    "master_rel": "01_funnel/REACTION_MASTER_POOL.parquet",
    "pairs_rel": "01_funnel/ALL_SCIENTIFIC_PAIRS.parquet",
    "top_k": 10,
    "morgan_radius": 8,
    "greedy": "getRSim",
    "direction": "max(same,reverse)",
    "pythonhashseed": "0",
}

# ---- stage task ids (this batch) ----
TASK_IDS = {
    "B0": "biosysmodb121_b0_input_authority_verification_20260928",
    "B1": "biosysmodb121_b1_step_gold_freeze_20260928",
    "B2": "biosysmodb121_b2_base_recall_audit_20260928",
}
