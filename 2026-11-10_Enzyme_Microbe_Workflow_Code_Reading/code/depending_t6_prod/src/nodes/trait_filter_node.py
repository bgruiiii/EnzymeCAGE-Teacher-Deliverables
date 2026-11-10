# src/nodes/trait_filter_node.py
# T5B: C8 只读性状注释节点（替换旧 M4b soft-passthrough 占位）。
#
# 语义: annotation_complete_no_hard_filter —— 只注释、不筛选、不排序、不评分。

import logging
from datetime import datetime, timezone

from src.state import EnzymeCrewState
from src.schemas.evidence import EvidenceRecord
from src.tools.trait_query import C8AssetError, build_trait_annotations, trait_records_from_annotations

logger = logging.getLogger(__name__)

NODE_ACTION = "c8_trait_annotation_readonly"


def trait_filter_node(state: EnzymeCrewState) -> dict:
    """T5B Trait 节点：从 organism_candidates 的 supporting_enzymes UID 构建 C8 注释。

    输出: existing public state keys trait_records + trait_filter_passed。
    不改变 candidate 成员/顺序/rank；不做 hard filtering。
    """
    candidates = state.organism_candidates

    # 无候选 → 诚实空输出，不报成功筛选
    if not candidates:
        evidence = EvidenceRecord(
            stage="trait", action=NODE_ACTION,
            data={"input_organism_candidates": 0, "annotations": 0, "note": "no organism_candidates"},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return {
            "trait_records": [],
            "trait_filter_passed": None,
            "uncertainty_flags": state.uncertainty_flags,
            "evidence_chain": state.evidence_chain + [evidence],
        }

    # 有候选 → 必须完成查询；资产身份失败则 fail-closed
    try:
        annotations, meta = build_trait_annotations(candidates)
    except C8AssetError as exc:
        uncertainty = list(state.uncertainty_flags)
        uncertainty.append(f"c8_asset_error:{exc}")
        evidence = EvidenceRecord(
            stage="trait", action=NODE_ACTION,
            data={"input_organism_candidates": len(candidates), "error": str(exc)},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return {
            "trait_records": [],
            "trait_filter_passed": None,
            "error": f"c8_trait_annotation asset identity failed: {exc}",
            "fail_closed": True,
            "uncertainty_flags": uncertainty,
            "evidence_chain": state.evidence_chain + [evidence],
        }

    records = trait_records_from_annotations(annotations)
    observed = sum(1 for a in annotations for ev in a.traits.values() if ev.trait_evidence_class == "OBSERVED")
    missing = sum(1 for a in annotations for ev in a.traits.values() if ev.trait_evidence_class == "MISSING")
    identity = sum(1 for a in annotations for ev in a.traits.values() if ev.trait_evidence_class == "IDENTITY_ONLY")
    not_mapped = meta.get("not_mapped_uids", [])
    uncertainty = list(state.uncertainty_flags)
    if not_mapped:
        uncertainty.append(f"NOT_MAPPED_uids={len(not_mapped)}")
    uncertainty.append("predicted_candidates_not_activated: see per-trait warnings")

    evidence = EvidenceRecord(
        stage="trait", action=NODE_ACTION,
        data={
            "input_organism_candidates": len(candidates),
            "unique_enzyme_uids": meta["unique_enzyme_uids"],
            "mapped_uids": meta["mapped_uids"],
            "not_mapped_uids": not_mapped,
            "unique_source_signatures": meta["unique_source_signatures"],
            "observed_trait_count": observed,
            "missing_trait_count": missing,
            "identity_only_trait_count": identity,
            "f1_f15_complete_per_mapped_source": True,
            "annotation_semantics": "annotation_complete_no_hard_filter",
            "asset_hashes": meta["asset_hashes"],
        },
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    return {
        "trait_records": records,
        "trait_filter_passed": True,  # 语义 = annotation_complete_no_hard_filter
        "uncertainty_flags": uncertainty,
        "evidence_chain": state.evidence_chain + [evidence],
    }
