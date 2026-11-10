import importlib
import pickle
from collections import defaultdict
from pathlib import Path
from typing import List

import torch


class PrecomputedAssetIndex:
    def __init__(self, config: dict):
        geometric = importlib.import_module("enzymecage.dataset.geometric")
        sharded = importlib.import_module("enzymecage.dataset.sharded_protein")
        self.config = dict(config)
        self.gvp = sharded.load_protein_gvp_data(config["protein_gvp_feat"])
        self.pocket_node = sharded.load_pocket_node_feature_data(config["esm_node_feature"])
        with open(config["esm_mean_feature"], "rb") as stream:
            self.sequence_esm = pickle.load(stream)
        with open(config["rxn_fp"], "rb") as stream:
            self.rxn_fp = pickle.load(stream)
        molecule_dir = Path(config["mol_conformation"])
        molecule_table = geometric.pd.read_csv(molecule_dir / "mol2id.csv")
        self.molecule_index = frozenset(molecule_table["SMILES"].astype(str))
        self.molecule_graphs = torch.load(molecule_dir / "mol_graph_dict.pt", map_location="cpu", weights_only=False)
        if not self.molecule_index.issubset(self.molecule_graphs.keys()):
            raise RuntimeError("molecule graph cache is incomplete; refusing any asset repair")
        with open(config["reaction_center"], "rb") as stream:
            self.reaction_centers = pickle.load(stream)

        uid_sequences = defaultdict(set)
        uid_row_counts = defaultdict(int)
        split_rows = 0
        for key in ("train_path", "valid_path", "test_path"):
            frame = geometric.pd.read_csv(config[key], usecols=["UniprotID", "sequence"], dtype=str, keep_default_na=False)
            split_rows += len(frame)
            for uid, sequence in frame.itertuples(index=False, name=None):
                uid_sequences[uid].add(sequence)
                uid_row_counts[uid] += 1
        self.ambiguous_uids = frozenset(uid for uid, sequences in uid_sequences.items() if len(sequences) != 1)
        self.uid_to_sequence = {
            uid: next(iter(sequences)) for uid, sequences in uid_sequences.items() if len(sequences) == 1
        }
        self.duplicate_uid_mappings = tuple(
            {
                "uid": uid,
                "row_count": uid_row_counts[uid],
                "distinct_sequence_count": len(uid_sequences[uid]),
            }
            for uid in sorted(uid_sequences)
            if uid_row_counts[uid] > 1 and len(uid_sequences[uid]) == 1
        )
        self.duplicate_uid_mapping_count = len(self.duplicate_uid_mappings)
        self.duplicate_uid_mapping_row_count = sum(row["row_count"] for row in self.duplicate_uid_mappings)
        self.split_row_count = split_rows

    @staticmethod
    def _molecules(reaction_smiles: str) -> List[str]:
        if reaction_smiles.count(">>") != 1:
            return []
        sides = reaction_smiles.split(">>")
        return [
            value.replace("*", "C")
            for side in sides
            for value in side.split(".")
            if value and value != "[*H2]"
        ]

    def has_reaction(self, reaction_smiles: str) -> bool:
        return not self.missing_assets(reaction_smiles)

    def has_enzyme(self, uid: str) -> bool:
        sequence = self.uid_to_sequence.get(uid)
        return bool(
            sequence
            and uid not in self.ambiguous_uids
            and uid in self.gvp
            and uid in self.pocket_node
            and sequence in self.sequence_esm
        )

    def missing_assets(self, reaction_smiles: str) -> List[str]:
        missing = []
        if reaction_smiles not in self.rxn_fp:
            missing.append("DRFP reaction fingerprint")
        molecules = self._molecules(reaction_smiles)
        if not molecules or any(molecule not in self.molecule_index or molecule not in self.molecule_graphs for molecule in molecules):
            missing.append("molecule-conformation graph")
        return missing

    def sequence_for(self, uid: str) -> str:
        if not self.has_enzyme(uid):
            raise KeyError(uid)
        return self.uid_to_sequence[uid]

    def inventory(self) -> dict:
        return {
            "split_row_count": self.split_row_count,
            "unambiguous_uid_count": len(self.uid_to_sequence),
            "ambiguous_uid_count": len(self.ambiguous_uids),
            "ambiguous_uids": sorted(self.ambiguous_uids),
            "duplicate_uid_mapping_count": self.duplicate_uid_mapping_count,
            "duplicate_uid_mapping_row_count": self.duplicate_uid_mapping_row_count,
            "duplicate_uid_mappings": list(self.duplicate_uid_mappings),
            "gvp_uid_count": len(self.gvp),
            "pocket_node_uid_count": len(self.pocket_node),
            "sequence_esm_count": len(self.sequence_esm),
            "drfp_reaction_count": len(self.rxn_fp),
            "molecule_index_count": len(self.molecule_index),
            "molecule_graph_count": len(self.molecule_graphs),
            "query_methods_read_only": True,
        }
