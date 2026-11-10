# src/utils/route_step_organism_aggregator.py
# T5C-R1 staged: supporting enzymes (all unique UIDs per step), route-order rank key (no inner sorted),
# order-independent trait merge with complete conflict provenance.
#
# 真实多步路线仍需上游 T2/T3；本工具只按冻结输入合同聚合。输入顺序不赋予生物学意义，
# 路线顺序只由 ordered_reaction_task_ids 定义（§3，合同输入顺序≠生物学顺序）。

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from src.schemas.evidence import RouteAggregationInput, RouteStepHostAnnotation, TraitEvidence
from src.tools.trait_query import F_TRAITS

RT_RE = re.compile(r"^RT-[A-Za-z0-9._-]+$")
ROUTE_RE = re.compile(r"^R-[A-Za-z0-9._-]+$")
RESOLVED_HOSTS = ("EXACT_STRAIN", "SPECIES", "REPRESENTATIVE_STRAIN")
LEGAL_HOST_SOURCES = ("UNIPROT_REVIEWED", "KEGG_SUPPLEMENT", "BACDIVE_OBSERVED")

TRAIT_PRECEDENCE = "OBSERVED_OVER_PREDICTED"


class RouteAggregationError(ValueError):
    """输入合同违反（fail-closed）。"""


def _normalize_host_name(name: Optional[str]) -> str:
    if not name or not name.strip():
        return ""
    return " ".join(name.strip().lower().split())


@dataclass
class _StepEnzyme:
    reaction_task_id: str
    enzyme_uid: str
    enzyme_rank: int


@dataclass
class _AggBucket:
    source_signature: str
    host_resolution: str
    host_taxid: int
    host_name: str
    host_name_norm: str
    host_evidence_sources: List[str]
    # task_id -> enzyme_uid -> best occurrence (lowest rank, first-seen tie)
    step_enzymes: Dict[str, Dict[str, _StepEnzyme]] = field(default_factory=dict)
    trait_slots: Dict[str, List[TraitEvidence]] = field(default_factory=dict)
    is_fungi: bool = False
    warnings: List[str] = field(default_factory=list)


def _validate_input(inp: RouteAggregationInput) -> None:
    if not ROUTE_RE.fullmatch(inp.route_id or ""):
        raise RouteAggregationError("route_id must match R-[A-Za-z0-9._-]+")
    tasks = inp.ordered_reaction_task_ids
    if not tasks:
        raise RouteAggregationError("ordered_reaction_task_ids must be non-empty")
    if len(tasks) != len(set(tasks)):
        raise RouteAggregationError("ordered_reaction_task_ids must be unique")
    for tid in tasks:
        if not RT_RE.fullmatch(tid or ""):
            raise RouteAggregationError(f"reaction_task_id must match RT-...: {tid!r}")
    task_set = set(tasks)
    for ann in inp.step_host_annotations:
        if ann.reaction_task_id not in task_set:
            raise RouteAggregationError(
                f"annotation references task {ann.reaction_task_id!r} not in this route")
        if ann.enzyme_rank < 1:
            raise RouteAggregationError("enzyme_rank must be >= 1")
        if not ann.source_signature or not ann.source_signature.strip():
            raise RouteAggregationError("annotation must carry a non-empty source_signature")


def _value_key(value) -> str:
    """stable canonical key for trait values (order independent, dedup-safe)."""
    if isinstance(value, list):
        return json_dump(value)
    return repr(value)


def json_dump(v):
    import json as _json
    return _json.dumps(v, sort_keys=True, ensure_ascii=False)


def _merge_trait_slot_final(slot: List[TraitEvidence], bucket: "_AggBucket") -> Tuple[TraitEvidence, List[str]]:
    """Order-independent merge over ALL evidence of one trait slot."""
    warnings: List[str] = []
    tid = slot[0].trait_id

    # F5 gate: PREDICTED input for F5 fail-closed
    if tid == "F5" and any(e.trait_evidence_class == "PREDICTED" for e in slot):
        raise RouteAggregationError("F5 must not be PREDICTED (fail-closed)")

    observed = [e for e in slot if e.trait_evidence_class == "OBSERVED"]
    predicted = [e for e in slot if e.trait_evidence_class == "PREDICTED"]
    identity = [e for e in slot if e.trait_evidence_class == "IDENTITY_ONLY"]
    missing = [e for e in slot if e.trait_evidence_class == "MISSING"]
    conflicts = [e for e in slot if e.trait_evidence_class == "CONFLICT"]

    if bucket.is_fungi:
        # 严格 fail-closed：任何非 IDENTITY_ONLY 输入立即抛错（不得 warning 后继续）
        for e in slot:
            if e.trait_evidence_class != "IDENTITY_ONLY":
                raise RouteAggregationError(
                    f"{tid}:fungal slot has non-IDENTITY_ONLY input ({e.trait_evidence_class})")
            if e.trait_value is not None:
                raise RouteAggregationError(f"{tid}:fungal slot has non-null trait_value")
            if e.trait_resolution != "IDENTITY_ONLY":
                raise RouteAggregationError(
                    f"{tid}:fungal slot has resolution {e.trait_resolution} (must be IDENTITY_ONLY)")
            if e.used_for_hard_filtering or e.used_for_ranking or e.direct_target_degradation_claim:
                raise RouteAggregationError(f"{tid}:fungal slot has forbidden claim/ranking flag")
        # 全部合格：稳定代表 = 规范化 key 最小的该项（确定性）；合并唯一 source_record_id/warnings
        slot.sort(key=lambda e: e.model_dump_json())
        merged_prov = []
        for e in slot:
            merged_prov.append(e.source_record_id or "unknown")
        merged_prov = list(dict.fromkeys(merged_prov))
        merged_warn = []
        for e in slot:
            merged_warn.extend(e.trait_warning or [])
        merged_warn = list(dict.fromkeys(merged_warn))
        base = slot[0].model_copy(deep=True)
        base.source_record_id = "|".join(merged_prov)
        base.trait_warning = merged_warn
        return base, warnings

    # non-fungi with IDENTITY_ONLY mixed in -> conservative fixed choice: fail-closed
    # (alternative CONFLICT+warning rejected in favour of the more conservative deterministic gate)
    if identity and (observed or predicted or missing or conflicts):
        raise RouteAggregationError(f"{tid}:IDENTITY_ONLY mixed with non-identity evidence in non-fungal bucket (fail-closed)")

    unique_obs: Dict[str, Tuple[TraitEvidence, List[str]]] = {}
    for e in observed:
        k = _value_key(e.trait_value)
        if k not in unique_obs:
            unique_obs[k] = (e, [e.source_record_id or "unknown"])
        else:
            unique_obs[k][1].append(e.source_record_id or "unknown")

    if len(unique_obs) > 1:
        values = list(unique_obs.values())
        values.sort(key=lambda v: (_value_key(v[0].trait_value), sorted(set(v[1]))[0]))
        first = values[0][0]
        merged_value = [v[0].trait_value for v in values]
        merged_prov = []
        for _ev, provs in values:
            merged_prov.extend(sorted(set(provs)))
        merged_prov = list(dict.fromkeys(merged_prov))
        out = first.model_copy(deep=True)
        out.trait_evidence_class = "CONFLICT"
        out.trait_value = merged_value
        out.source_record_id = "|".join(merged_prov)
        out.trait_warning = list(dict.fromkeys(first.trait_warning
                                               + [f"conflict:{len(values)}_distinct_observed_values"]))
        warnings.append(f"{tid}:conflict with {len(values)} distinct observed values preserved")
        return out, warnings

    if len(unique_obs) == 1:
        ev, provs = next(iter(unique_obs.values()))
        out = ev.model_copy(deep=True)
        out.source_record_id = "|".join(sorted(set(provs)))
        return out, warnings

    # no observed
    unique_pred: Dict[str, Tuple[TraitEvidence, List[str]]] = {}
    for e in predicted:
        k = _value_key(e.trait_value)
        if k not in unique_pred:
            unique_pred[k] = (e, [e.source_record_id or "unknown"])
        else:
            unique_pred[k][1].append(e.source_record_id or "unknown")
    if len(unique_pred) > 1:
        values = list(unique_pred.values())
        values.sort(key=lambda v: (_value_key(v[0].trait_value), sorted(set(v[1]))[0]))
        first = values[0][0]
        out = first.model_copy(deep=True)
        out.trait_evidence_class = "CONFLICT"
        out.trait_value = [v[0].trait_value for v in values]
        merged_prov = []
        for _ev, provs in values:
            merged_prov.extend(sorted(set(provs)))
        out.source_record_id = "|".join(list(dict.fromkeys(merged_prov)))
        warnings.append(f"{tid}:multi_predicted_conflict_preserved")
        return out, warnings
    if len(unique_pred) == 1:
        ev, provs = next(iter(unique_pred.values()))
        out = ev.model_copy(deep=True)
        out.source_record_id = "|".join(sorted(set(provs)))
        return out, warnings

    if conflicts:
        # 多个预先 CONFLICT：规范化合并全部唯一 values/provenance/warnings（order-independent）
        all_values: List = []
        all_prov: List[str] = []
        all_warn: List[str] = []
        for e in conflicts:
            v = e.trait_value
            if isinstance(v, list):
                all_values.extend(v)
            else:
                all_values.append(v)
            all_prov.extend((e.source_record_id or "unknown").split("|"))
            all_warn.extend(e.trait_warning or [])
        seen_v: Dict[str, object] = {}
        for v in all_values:
            seen_v.setdefault(_value_key(v), v)
        unique_values = list(seen_v.values())
        unique_values.sort(key=_value_key)
        unique_prov = list(dict.fromkeys(sorted(set(p for p in all_prov if p))))
        unique_warn = list(dict.fromkeys(all_warn))
        first = conflicts[0].model_copy(deep=True)
        first.trait_evidence_class = "CONFLICT"
        first.trait_value = unique_values
        first.source_record_id = "|".join(unique_prov)
        first.trait_warning = unique_warn
        return first, warnings

    if missing:
        # 多个 MISSING：规范化完整对象 key 排序稳定代表；合并全部唯一 source_record_id/warnings
        missing_sorted = sorted(missing, key=lambda e: e.model_dump_json())
        merged_prov = []
        merged_warn: List[str] = []
        for e in missing_sorted:
            merged_prov.append(e.source_record_id or "unknown")
            merged_warn.extend(e.trait_warning or [])
        merged_prov = list(dict.fromkeys(merged_prov))
        merged_warn = list(dict.fromkeys(merged_warn))
        out = missing_sorted[0].model_copy(deep=True)
        out.source_record_id = "|".join(merged_prov)
        out.trait_warning = merged_warn
        return out, warnings

    # only IDENTITY_ONLY (non-fungal): stable representative
    identity_sorted = sorted(identity, key=lambda e: e.model_dump_json())
    base = identity_sorted[0].model_copy(deep=True)
    return base, warnings


def _merge_traits(bucket: _AggBucket) -> Tuple[List[TraitEvidence], List[str]]:
    out: List[TraitEvidence] = []
    warnings: List[str] = []
    for tid in F_TRAITS:
        evs = bucket.trait_slots.get(tid, [])
        if not evs:
            raise RouteAggregationError(f"aggregate missing trait {tid} (F1-F15 completeness violated)")
        merged, ws = _merge_trait_slot_final(evs, bucket)
        out.append(merged)
        warnings.extend(ws)
    return out, warnings


def _key(ann: RouteStepHostAnnotation) -> Tuple[str, str, int, str]:
    return (ann.source_signature.strip(),
            ann.host_resolution,
            ann.host_taxid if ann.host_taxid is not None else -1,
            _normalize_host_name(ann.host_name))


def aggregate_route(inp: RouteAggregationInput) -> dict:
    """返回 {"route_id", "aggregates", "unresolved_ledger", "dedup_notes", "rank_key_audit"}。

    排序：covered desc -> route-order rank tuple asc（严格按 route 步骤顺序，禁止内部 sorted）
          -> source_signature asc -> (host_taxid, host_name_norm) 稳定 tie-break。
    """
    _validate_input(inp)
    order_index = {tid: i for i, tid in enumerate(inp.ordered_reaction_task_ids)}
    buckets: Dict[Tuple, _AggBucket] = {}
    unresolved: List[dict] = []
    dedup_notes: List[str] = []

    for ann in inp.step_host_annotations:
        if ann.host_resolution == "UNRESOLVED" or not ann.source_signature.strip() \
                or not ann.host_taxid or ann.host_taxid < 1 or not _normalize_host_name(ann.host_name):
            unresolved.append({
                "reaction_task_id": ann.reaction_task_id,
                "enzyme_uid": ann.enzyme_uid,
                "source_signature": ann.source_signature,
                "reason": "unresolved_host_or_missing_identity_fields",
            })
            continue
        if ann.host_resolution not in RESOLVED_HOSTS:
            raise RouteAggregationError(f"illegal host_resolution for aggregation: {ann.host_resolution}")
        host_sources_ok = all(s in LEGAL_HOST_SOURCES for s in ann.host_evidence_sources) \
            and len(ann.host_evidence_sources) == len(set(ann.host_evidence_sources)) \
            and len(ann.host_evidence_sources) >= 1
        if not host_sources_ok:
            unresolved.append({
                "reaction_task_id": ann.reaction_task_id,
                "enzyme_uid": ann.enzyme_uid,
                "source_signature": ann.source_signature,
                "reason": "no_legal_host_evidence_sources",
            })
            continue
        k = _key(ann)
        b = buckets.get(k)
        if b is None:
            b = _AggBucket(
                source_signature=ann.source_signature.strip(),
                host_resolution=ann.host_resolution,
                host_taxid=ann.host_taxid,
                host_name=ann.host_name or "",
                host_name_norm=_normalize_host_name(ann.host_name),
                host_evidence_sources=list(dict.fromkeys(ann.host_evidence_sources)),
                is_fungi=(ann.host_taxonomy_group == "target_fungi"),
            )
            buckets[k] = b
        else:
            b.host_evidence_sources = list(dict.fromkeys(b.host_evidence_sources + ann.host_evidence_sources))
            if ann.host_taxonomy_group == "target_fungi":
                b.is_fungi = True
        # task -> uid -> best occurrence: dedup ONLY same (task, uid); different UIDs all kept
        step_map = b.step_enzymes.setdefault(ann.reaction_task_id, {})
        cur = step_map.get(ann.enzyme_uid)
        if cur is None:
            step_map[ann.enzyme_uid] = _StepEnzyme(ann.reaction_task_id, ann.enzyme_uid, ann.enzyme_rank)
        else:
            if (ann.enzyme_rank, ann.source_record_id if hasattr(ann, "source_record_id") else "") \
                    < (cur.enzyme_rank, ""):
                dedup_notes.append(
                    f"task {ann.reaction_task_id} uid {ann.enzyme_uid}: kept rank {ann.enzyme_rank} over {cur.enzyme_rank}")
                step_map[ann.enzyme_uid] = _StepEnzyme(ann.reaction_task_id, ann.enzyme_uid, ann.enzyme_rank)
            else:
                dedup_notes.append(
                    f"task {ann.reaction_task_id} uid {ann.enzyme_uid}: duplicate downgraded (kept rank {cur.enzyme_rank})")
        for tid in F_TRAITS:
            if tid not in ann.traits:
                raise RouteAggregationError(f"annotation missing trait {tid}")
            b.trait_slots.setdefault(tid, []).append(ann.traits[tid])

    aggregates: List[dict] = []
    rank_audit: List[dict] = []
    for b in buckets.values():
        # supported order strictly by route order; per-step UIDs sorted by (rank, uid)
        supported = [t for t in inp.ordered_reaction_task_ids if t in b.step_enzymes]
        enzymes_out: List[dict] = []
        best_rank_per_step: Dict[str, int] = {}
        for t in supported:
            uids_sorted = sorted(b.step_enzymes[t].values(), key=lambda e: (e.enzyme_rank, e.enzyme_uid))
            best_rank_per_step[t] = uids_sorted[0].enzyme_rank
            for e in uids_sorted:
                enzymes_out.append({
                    "reaction_task_id": e.reaction_task_id,
                    "enzyme_uid": e.enzyme_uid,
                    "enzyme_rank": e.enzyme_rank,
                })
        # route-order rank key: position i = best rank at step i, INF for unmatched steps (order preserved)
        rank_key = tuple(
            best_rank_per_step[t] if t in best_rank_per_step else float("inf")
            for t in inp.ordered_reaction_task_ids
        )
        merged_traits, trait_warnings = _merge_traits(b)
        unmatched = [t for t in inp.ordered_reaction_task_ids if t not in b.step_enzymes]
        warnings = list(dict.fromkeys(b.warnings + trait_warnings))
        aggregate = {
            "route_id": inp.route_id,
            "source_signature": b.source_signature,
            "host_taxid": b.host_taxid,
            "host_name": b.host_name,
            "host_resolution": b.host_resolution,
            "host_evidence_source": b.host_evidence_sources,
            "supported_reaction_task_ids": supported,
            "covered_step_count": len(supported),
            "total_route_step_count": len(inp.ordered_reaction_task_ids),
            "unmatched_steps": unmatched,
            "supporting_enzymes": enzymes_out,
            "trait_evidence_precedence": TRAIT_PRECEDENCE,
            "traits": [ev.model_dump() for ev in merged_traits],
            "default_order_rank": 0,
            "warnings": warnings,
        }
        rank_audit.append({
            "source_signature": b.source_signature,
            "host_taxid": b.host_taxid,
            "host_resolution": b.host_resolution,
            "route_order_rank_key": [None if v == float("inf") else v for v in rank_key],
            "covered_step_count": len(supported),
            "supporting_enzyme_count": len(enzymes_out),
        })
        aggregates.append((aggregate, b, rank_key))

    def tie_break(ab):
        b = ab[1]
        return (b.host_taxid, b.host_name_norm)
    aggregates.sort(key=lambda ab: (
        -ab[0]["covered_step_count"],
        ab[2],                    # route-order rank tuple comparison (no sorted inside)
        ab[0]["source_signature"],
        tie_break(ab),
    ))
    for rank, (ag, _b, _rk) in enumerate(aggregates, 1):
        ag["default_order_rank"] = rank
    rank_audit.sort(key=lambda r: (
        -r["covered_step_count"],
        tuple(float("inf") if v is None else v for v in r["route_order_rank_key"]),
        r["source_signature"],
    ))

    return {
        "route_id": inp.route_id,
        "aggregates": [ag for ag, _b, _rk in aggregates],
        "unresolved_ledger": unresolved,
        "dedup_notes": dedup_notes,
        "rank_key_audit": rank_audit,
    }
