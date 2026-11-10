from typing import List, Optional, Tuple

from pydantic import BaseModel, Field


class EnzymeCAGERequest(BaseModel):
    reaction_smiles: str = Field(
        ..., description="目标反应的 SMILES 字符串"
    )
    enzyme_pool_uids: List[str] = Field(
        ..., min_length=1, description="候选酶 UID 列表（来源由上游 Agent 提供）"
    )
    top_k: int = Field(
        default=10, ge=1, le=100, description="返回排序前 K 个结果"
    )
    return_ci: bool = Field(
        default=True, description="是否返回 5-seed ensemble 置信区间"
    )


class RankedEnzyme(BaseModel):
    uid: str
    score: float = Field(..., description="5-seed ensemble 平均分")
    rank: int = Field(..., ge=1, description="从 1 开始连续编号")
    ensemble_ci: Optional[Tuple[float, float]] = Field(
        default=None,
        description="5-seed 打分的 [lower, upper] 95% 分位 CI；return_ci=False 时为 None"
    )


class EnzymeCAGEResponse(BaseModel):
    ranked_enzymes: List[RankedEnzyme] = Field(
        ..., description="按 score 降序排列，长度 = min(top_k, 有效候选数)"
    )
    model_version: str = Field(default="v1_20260714")
    evidence_hash: str = Field(
        ..., description="本次推理输入的 SHA256 摘要，用于复现追溯"
    )
