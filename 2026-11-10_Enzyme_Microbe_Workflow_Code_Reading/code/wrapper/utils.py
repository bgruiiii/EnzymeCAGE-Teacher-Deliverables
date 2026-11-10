import hashlib
import math
from typing import Iterable, List, Sequence, Tuple

import torch


MODEL_VERSION = "v1_20260714"


def evidence_hash_payload(reaction_smiles: str, enzyme_pool_uids: Sequence[str], model_version: str = MODEL_VERSION) -> str:
    return reaction_smiles + "\n" + "\n".join(sorted(enzyme_pool_uids)) + "\n" + model_version


def compute_evidence_hash(reaction_smiles: str, enzyme_pool_uids: Sequence[str], model_version: str = MODEL_VERSION) -> str:
    return hashlib.sha256(evidence_hash_payload(reaction_smiles, enzyme_pool_uids, model_version).encode("utf-8")).hexdigest()


def deduplicate_first(values: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def aggregate_seed_scores(uids: Sequence[str], per_seed: Sequence[Sequence[float]], return_ci: bool) -> List[Tuple[str, float, Tuple[float, float] | None]]:
    if len(per_seed) != 5 or any(len(row) != len(uids) for row in per_seed):
        raise ValueError("exactly five equally sized seed-score vectors are required")
    rows = []
    for index, uid in enumerate(uids):
        values = torch.tensor([float(seed[index]) for seed in per_seed], dtype=torch.float64)
        if not bool(torch.isfinite(values).all()):
            raise RuntimeError(f"non-finite live score for UID {uid}")
        mean = float(values.mean().item())
        ci = None
        if return_ci:
            quantiles = torch.quantile(
                values,
                torch.tensor([0.025, 0.975], dtype=torch.float64),
                interpolation="linear",
            )
            ci = (float(quantiles[0].item()), float(quantiles[1].item()))
        rows.append((uid, mean, ci))
    return sorted(rows, key=lambda row: (-row[1], row[0]))


def require_probability(value: float, label: str) -> None:
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise RuntimeError(f"{label} is not a finite probability")
