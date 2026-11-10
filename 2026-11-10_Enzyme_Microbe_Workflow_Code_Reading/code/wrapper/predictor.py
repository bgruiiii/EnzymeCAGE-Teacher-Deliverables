import importlib
import os
import threading
from pathlib import Path
from typing import Optional

import torch

from .asset_index import PrecomputedAssetIndex
from .schema import EnzymeCAGERequest, EnzymeCAGEResponse, RankedEnzyme
from .utils import MODEL_VERSION, aggregate_seed_scores, compute_evidence_hash, deduplicate_first


SEEDS = (40, 41, 42, 43, 44)
FOLLOW_BATCH = ["protein", "reaction_feature", "esm_feature", "substrates", "products"]
MODEL_FIELDS = (
    "model", "esm_model", "use_esm", "use_structure", "use_drfp", "use_prods_info",
    "interaction_method", "rxn_inner_interaction", "pocket_inner_interaction",
)


class MissingReactionAssetError(RuntimeError):
    pass


class _Runtime:
    def __init__(self, package_root: Path):
        self.package_root = package_root.resolve()
        yaml = importlib.import_module("yaml")
        configs = []
        for seed in SEEDS:
            with (self.package_root / f"3b_ensemble/seed_{seed}/config.yaml").open(encoding="utf-8") as stream:
                configs.append(yaml.safe_load(stream))
        self.config = configs[0]
        baseline = {field: self.config[field] for field in MODEL_FIELDS}
        if any({field: conf[field] for field in MODEL_FIELDS} != baseline for conf in configs[1:]):
            raise RuntimeError("model-relevant configuration differs across the five package seeds")
        if baseline != {
            "model": "EnzymeCAGE", "esm_model": "esm2_t36_3B_UR50D", "use_esm": True,
            "use_structure": True, "use_drfp": True, "use_prods_info": False,
            "interaction_method": "geo-enhanced-interaction", "rxn_inner_interaction": True,
            "pocket_inner_interaction": True,
        }:
            raise RuntimeError("package is not the accepted corrected-pocket 3B architecture")
        self.asset_index = PrecomputedAssetIndex(self.config)
        if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
            raise RuntimeError("runtime requires exactly one visible CUDA device")
        self.device = torch.device("cuda:0")
        model_module = importlib.import_module("enzymecage.model")
        self.models = []
        for seed in SEEDS:
            checkpoint = self.package_root / f"3b_ensemble/seed_{seed}/best_model.pth"
            model = model_module.EnzymeCAGE(
                use_esm=self.config["use_esm"], use_structure=self.config["use_structure"],
                use_drfp=self.config["use_drfp"], use_prods_info=self.config["use_prods_info"],
                esm_model=self.config["esm_model"], interaction_method=self.config["interaction_method"],
                rxn_inner_interaction=self.config["rxn_inner_interaction"],
                pocket_inner_interaction=self.config["pocket_inner_interaction"], device=str(self.device),
            )
            state = torch.load(checkpoint, map_location="cpu", weights_only=False)
            model.load_state_dict(state, strict=True)
            self.models.append(model.to(self.device).eval())
        torch.cuda.synchronize(self.device)
        self.forward_call_count = 0
        self.last_trace = None

    def _dataset(self, reaction: str, uids: list[str]):
        geometric = importlib.import_module("enzymecage.dataset.geometric")
        pyg_data = importlib.import_module("torch_geometric.data")
        frame = geometric.pd.DataFrame({
            "UniprotID": uids,
            "CANO_RXN_SMILES": [reaction] * len(uids),
            "sequence": [self.asset_index.sequence_for(uid) for uid in uids],
            "Label": [0] * len(uids),
        })
        dataset = geometric.GeometricDataset.__new__(geometric.GeometricDataset)
        pyg_data.Dataset.__init__(dataset)
        dataset.df_data = frame
        dataset.pocket_node_feature = self.asset_index.pocket_node
        dataset.esm_dim = next(iter(self.asset_index.pocket_node.values())).shape[1]
        dataset.protein_dict = self.asset_index.gvp
        dataset.esm_feat_dict = self.asset_index.sequence_esm
        dataset.rxn_feat_dict = self.asset_index.rxn_fp
        dataset.uniprot_ids = list(uids)
        dataset.rxns = [reaction] * len(uids)
        dataset.targets = [0] * len(uids)
        dataset.seqs = [self.asset_index.sequence_for(uid) for uid in uids]
        dataset.weights = torch.ones(len(uids))
        dataset.mol_to_index = {key: index for index, key in enumerate(self.asset_index.molecule_index)}
        dataset.mol_to_data = self.asset_index.molecule_graphs
        dataset.reacting_center_map = self.asset_index.reaction_centers
        return dataset

    def predict(self, request: EnzymeCAGERequest) -> EnzymeCAGEResponse:
        original_uids = list(request.enzyme_pool_uids)
        digest = compute_evidence_hash(request.reaction_smiles, original_uids, MODEL_VERSION)
        missing = self.asset_index.missing_assets(request.reaction_smiles)
        if missing:
            self.last_trace = {"forward_executed": False, "missing_reaction_assets": missing}
            raise MissingReactionAssetError("missing reaction assets: " + "; ".join(missing))
        unique_uids = deduplicate_first(original_uids)
        valid_uids = [uid for uid in unique_uids if self.asset_index.has_enzyme(uid)]
        if not valid_uids:
            self.last_trace = {
                "original_uids": original_uids, "unique_uids": unique_uids, "valid_uids": [],
                "forward_executed": False, "batch_count": 0, "per_seed_scores": [],
            }
            return EnzymeCAGEResponse(ranked_enzymes=[], evidence_hash=digest)
        loader_type = importlib.import_module("torch_geometric.loader").DataLoader
        loader = loader_type(
            self._dataset(request.reaction_smiles, valid_uids), batch_size=len(valid_uids),
            shuffle=False, follow_batch=FOLLOW_BATCH,
        )
        per_seed = []
        with torch.no_grad():
            for model in self.models:
                values, _ = model.evaluate(loader, show_progress=False)
                per_seed.append([float(value) for value in values.detach().cpu().to(torch.float64).tolist()])
        torch.cuda.synchronize(self.device)
        self.forward_call_count += 1
        aggregated = aggregate_seed_scores(valid_uids, per_seed, request.return_ci)
        ranked = [
            RankedEnzyme(uid=uid, score=score, rank=rank, ensemble_ci=ci)
            for rank, (uid, score, ci) in enumerate(aggregated[:request.top_k], 1)
        ]
        self.last_trace = {
            "original_uids": original_uids, "unique_uids": unique_uids, "valid_uids": valid_uids,
            "forward_executed": True, "batch_count": 1, "batch_size": len(valid_uids),
            "per_seed_scores": per_seed, "returned_uids": [row.uid for row in ranked],
        }
        return EnzymeCAGEResponse(ranked_enzymes=ranked, evidence_hash=digest)


_RUNTIME: Optional[_Runtime] = None
_LOCK = threading.Lock()


def initialize_runtime(package_root: str | Path | None = None) -> _Runtime:
    global _RUNTIME
    root = Path(package_root or os.environ.get("ENZYMECAGE_V1_PACKAGE_ROOT", ""))
    if not str(root) or str(root) == ".":
        raise RuntimeError("ENZYMECAGE_V1_PACKAGE_ROOT is required")
    with _LOCK:
        if _RUNTIME is None:
            _RUNTIME = _Runtime(root)
        elif _RUNTIME.package_root != root.resolve():
            raise RuntimeError("runtime is already initialized for a different package root")
    return _RUNTIME


def predict(request: EnzymeCAGERequest) -> EnzymeCAGEResponse:
    return initialize_runtime().predict(request)


def _runtime_for_audit() -> Optional[_Runtime]:
    return _RUNTIME
