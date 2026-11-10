# src/utils/organism_aggregator.py
# OrganismAggregator（无状态函数，框架 §3.3）
#
# 职责：把「酶排序（RankedEnzyme）+ 酶→多源原始证据（EnzymeSourceProvenance）」
#       按 reviewed 宿主的 NCBI taxon 聚合成「菌 → 支持酶集合」的 OrganismCandidate 列表。
#
# 属 M4a 授权范围（酶→菌聚合），不涉及 metaTraits 性状（M4b，未立项，见 trait_filter_node）。
#
# 【严格对齐学生权威实现】microbe_crew/tools/organism_aggregator.py（15 tests passed），
#   规则源 = TEACHER_REPLY_MTD5_ACCEPTED_AND_MTD1_D8_DECISIONS_2026-07-16.md
#   + 学生 07-27 最终回应稿（DECIDED_AND_IMPLEMENTED FOR V1）：
#   - MT-D3：排序主键 = supporting-enzyme count 降序 + NCBI taxon ID 数字升序 tie-break。
#     （已裁定：TEACHER_REPLY_M3_P1_UNLOCK_...2026-07-21.md §MT-TQ-01 明确采纳 NCBI taxon ID
#      数字升序、不切换为 enzyme UID 升序——理由：taxon ID 是聚合后唯一生产主键，UID tie-break
#      存在"用哪条 UID 代表 taxon 组"的二义性。早期 07-16 裁定文的 "UID 升序" 表述已被 §MT-TQ-01
#      supersede；文档—代码口径一致，无遗留冲突。）
#   - 输入酶排序按 uid 首见去重；组内成员按 (rank, uid) 排序；排序后赋 1-based default_order_rank。
#   - 仅按 reviewed 宿主的 ncbi_taxon_id 分组；无 reviewed 映射的酶直接丢弃（无 organism_name 回退）。
#     宿主 identity signature/resolution 只作为每酶 provenance 保留。
#   - MT-D2：不输出 confidence float；原始证据维度经 per_enzyme_source_provenance 透传、不坠缩为分数。

import logging
from typing import Dict, List, Optional, Tuple

from src.schemas.evidence import (
    EnzymeSourceProvenance,
    OrganismCandidate,
    RankedEnzyme,
    SupportingEnzyme,
    host_signature_is_enzyme_uid_shaped,
)

logger = logging.getLogger(__name__)


def _host_identity_of(prov: EnzymeSourceProvenance) -> Optional[Tuple[str, Optional[str], int, str]]:
    """R2A 最小宿主键：返回 (host_identity_source_signature, host_resolution, taxon, name)。

    两条合法来源（teacher 授权）：
    - live reviewed UniProt：taxon/name 取 UniProtReviewedHostEvidence 真实字段；
    - 冻结 reviewed UID map fallback：taxon/name 取 map 行字段（uniprot_reviewed 必须为 None）。
    两者皆无 → None（MT-D1：无 reviewed 宿主映射不纳入，与 R2A 之前一致）。

    签名缺失时按 §5 的确定性构造规则补齐（``taxon:<id>|organism:<normalized name>``），
    且绝不允许用该酶自己的 UID 充当宿主签名。本函数纯本地计算：不访问网络、不读 map。
    """
    up = prov.uniprot_reviewed
    if up is not None:
        taxon, name = up.ncbi_taxon_id, up.scientific_organism_name
    elif prov.resolution_route == "FROZEN_REVIEWED_UID_MAP_FALLBACK":
        taxon, name = prov.host_taxid, prov.host_name
    else:
        return None
    if taxon is None or not name:
        return None
    sig = prov.host_identity_source_signature
    if not sig or host_signature_is_enzyme_uid_shaped(prov.enzyme_uid, sig):
        normalized = " ".join(str(name).split()).casefold()
        sig = f"taxon:{int(taxon)}|organism:{normalized}"
    return sig, prov.host_resolution, int(taxon), name


def aggregate_organisms(
    ranked_enzymes: List[RankedEnzyme],
    provenance_map: Dict[str, EnzymeSourceProvenance],
) -> List[OrganismCandidate]:
    """按 reviewed 宿主的 NCBI taxon 聚合酶排序 → OrganismCandidate（对齐学生 aggregate_organisms）。

    Args:
        ranked_enzymes: EnzymeCAGE 真实排序（RankedEnzyme{uid,score,rank,ensemble_ci}），
                        提供组内 (rank, uid) 排序键及支持酶的原始 score/rank/CI（不折算）。
        provenance_map: {enzyme_uid: EnzymeSourceProvenance}，来自 microbe_recommender.map_enzyme_hosts；
                        含 reviewed UniProt 宿主 + KEGG multiplicity + source_errors 原始维度。

    Returns:
        List[OrganismCandidate]，按 MT-D3：supporting-enzyme count 降序 + ncbi_taxon_id 升序。
        无 reviewed 宿主映射的酶不纳入任何候选（无 name 回退）。
    """
    if not ranked_enzymes:
        return []

    # 酶 uid 首见去重（对齐学生 first_ranked 语义）
    first_ranked: Dict[str, RankedEnzyme] = {}
    for ranked in ranked_enzymes:
        if ranked.uid not in first_ranked:
            first_ranked[ranked.uid] = ranked

    # 老师合同：microbe 候选只按 positive NCBI TaxID 分组。
    grouped: Dict[int, List[Tuple[RankedEnzyme, EnzymeSourceProvenance, int]]] = {}
    dropped_no_reviewed = 0
    for uid, ranked in first_ranked.items():
        prov = provenance_map.get(uid)
        identity = _host_identity_of(prov) if prov is not None else None
        if identity is None:
            # 无 reviewed 宿主映射（live 与冻结 map fallback 都没有）→ 不纳入（MT-D1）
            dropped_no_reviewed += 1
            continue
        _sig, _resolution, taxon_id, _name = identity
        if taxon_id <= 0:
            dropped_no_reviewed += 1
            continue
        grouped.setdefault(taxon_id, []).append((ranked, prov, taxon_id))

    candidates: List[OrganismCandidate] = []
    conflict_details: List[str] = []
    for taxon_id, members in grouped.items():
        # 组内成员排序：(rank, uid)
        members.sort(key=lambda item: (item[0].rank, item[0].uid))
        identity_pairs = [
            (ranked.uid, _host_identity_of(prov)[0], _host_identity_of(prov)[1])
            for ranked, prov, _taxon in members
        ]
        common_identity = {(sig, resolution) for _uid, sig, resolution in identity_pairs}
        host_sig = next(iter(common_identity))[0] if len(common_identity) == 1 else None
        if len(common_identity) > 1:
            conflict_details.append(", ".join(
                f"{uid}(signature={sig!r}, resolution={resolution!r})"
                for uid, sig, resolution in identity_pairs
            ))

        name_variants: List[str] = []
        for _, prov, _taxon in members:
            identity = _host_identity_of(prov)
            name = identity[3] if identity else prov.uniprot_reviewed.scientific_organism_name
            if name not in name_variants:
                name_variants.append(name)

        supporting = [
            SupportingEnzyme(
                uid=ranked.uid,
                score=ranked.score,
                rank=ranked.rank,
                ensemble_ci=ranked.ensemble_ci,
            )
            for ranked, _, _taxon in members
        ]
        per_enzyme_provenance = [
            EnzymeSourceProvenance(
                enzyme_uid=ranked.uid,
                uniprot_reviewed=prov.uniprot_reviewed,
                kegg=prov.kegg,
                source_errors=prov.source_errors,
                # G4-R2A：宿主 identity 与冻结 map 行 identity 逐字段随传（无损承载）
                resolution_route=prov.resolution_route,
                host_identity_source=prov.host_identity_source,
                host_identity_source_signature=prov.host_identity_source_signature,
                host_resolution=prov.host_resolution,
                host_taxid=prov.host_taxid,
                host_name=prov.host_name,
                frozen_map_file=prov.frozen_map_file,
                frozen_map_line=prov.frozen_map_line,
                frozen_map_row_sha256=prov.frozen_map_row_sha256,
                frozen_map_table_sha256=prov.frozen_map_table_sha256,
                frozen_map_error=prov.frozen_map_error,
                mapping_confidence_raw=prov.mapping_confidence_raw,
                warnings=list(prov.warnings),
            )
            for ranked, prov, _taxon in members
        ]

        candidates.append(
            OrganismCandidate(
                organism_uid=str(taxon_id),
                taxonomy_namespace="NCBI_taxon",
                ncbi_taxon_id=taxon_id,
                organism_name=name_variants[0],
                organism_name_variants=name_variants,
                supporting_enzymes=supporting,
                supporting_enzyme_count=len(supporting),
                per_enzyme_source_provenance=per_enzyme_provenance,
                default_order_rank=0,
                host_identity_source_signature=host_sig,
            )
        )

    # MT-D3：supporting-enzyme count 降序（主）→ ncbi_taxon_id 数字升序（tie-break）
    candidates.sort(key=lambda c: (-c.supporting_enzyme_count, c.ncbi_taxon_id))
    for order_rank, cand in enumerate(candidates, start=1):
        cand.default_order_rank = order_rank

    # 聚合说明（导师侧可观测性附加，不影响排序/语义；学生 schema 无此项）
    notes_parts = [
        "MT-D3：supporting-enzyme count 降序 + ncbi_taxon_id 升序 tie-break",
        "MT-D2：不产出 confidence float，原始证据维度经 per_enzyme_source_provenance 透传",
        "microbe 候选生产分组主键=positive NCBI TaxID；signature/resolution 仅作为每酶 provenance",
    ]
    if conflict_details:
        notes_parts.append(
            "宿主 identity 冲突（同 TaxID 已合并，聚合级 signature=null）: "
            + " | ".join(conflict_details)
        )
    if dropped_no_reviewed:
        notes_parts.append(
            f"丢弃无 reviewed 宿主映射的酶 {dropped_no_reviewed} 个（无 organism_name 回退）"
        )
    agg_notes = "；".join(notes_parts)
    for cand in candidates:
        cand.aggregation_notes = agg_notes

    logger.info(
        f"[organism_aggregator] 聚合 {len(first_ranked)} 个去重酶 "
        f"→ {len(candidates)} 个候选菌（positive NCBI TaxID 分组；MT-D3 排序；"
        f"丢弃无 reviewed {dropped_no_reviewed} 个）"
    )
    return candidates
