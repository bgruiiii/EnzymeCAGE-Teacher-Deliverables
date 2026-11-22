"""Trait evidence backends (R2).

C8 native rows: one row per source_signature x trait_id with
observed_available / matched_observed_examples / value_status_preview /
fungi_identity_only / predicted_soft_fill_candidate_available /
prediction_allowed_for_trait / taxonomy_group / source_type_preview ...
Slot classification reuses the audited t6_prod conservative rules
(code/depending_t6_prod/src/tools/trait_query.py::_trait_evidence/
_conservative_structured_value):
  - target_fungi -> IDENTITY_ONLY first;
  - observed_available true but matched content parses to empty (semicolon
    split, trim, drop empty, first-seen dedup; comma NOT a separator)
    -> MISSING + warning 'observed_available_flag_set_but_no_parseable_content';
  - predicted_soft_fill_candidate_available -> warning only (never OBSERVED);
  - otherwise MISSING.
Per-backend status/detail stay visible after merge: a missing or broken C8
never disappears behind SCNET success, and SCNET results still return.
SCNET long-table rows keep every original column verbatim.
"""
from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path

from .schemas import TraitEvidence

SCNET_REF = ("existing SCNET prediction flow (GenomeSPOT/MICROPHERRET/BacDiveAI/Traitar; audited DEHP returns "
             "2026-11-14). Submission NOT performed by this tool; prediction-required list only.")


def conservative_examples(matched: str):
    """t6_prod _conservative_structured_value semantics: ';' only, trim,
    drop-empty, first-seen dedup; comma not a separator."""
    if not matched:
        return []
    parts = [p.strip() for p in matched.split(";") if p.strip()]
    return list(dict.fromkeys(parts))


class C8Index:
    kind = "C8_native_slot_rows"

    def __init__(self, path: str):
        self.by_sig = {}
        self.n_rows = 0
        if not path or not Path(path).is_file():
            self.error = "C8_ASSET_MISSING_OR_NOT_CONFIGURED"
            return
        self.error = None
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except Exception as exc:
                    self.error = f"C8_PARSE_ERROR_row_{self.n_rows}: {type(exc).__name__}"
                    return
                if "source_signature" not in row or "trait_id" not in row:
                    self.error = f"C8_SCHEMA_UNEXPECTED_row_{self.n_rows}: missing source_signature/trait_id"
                    return
                self.by_sig.setdefault(row["source_signature"], []).append(row)
                self.n_rows += 1

    def traits(self, sig: str) -> TraitEvidence:
        if self.error:
            return TraitEvidence(source_signature=sig, backend="C8", status="BACKEND_ERROR",
                                 backend_statuses=[{"backend": "C8", "status": "BACKEND_ERROR", "detail": self.error}],
                                 note=self.error)
        rows = self.by_sig.get(sig)
        if rows is None:
            return TraitEvidence(source_signature=sig, backend="C8", status="NO_RECORD_FOR_KEY",
                                 backend_statuses=[{"backend": "C8", "status": "NO_RECORD_FOR_KEY",
                                                   "detail": "authoritative key absent from C8 index"}],
                                 note="no C8 rows for this exact authoritative key (not a claim of no data elsewhere)")
        slots = []
        n_obs = n_miss = n_id = 0
        pred_req = []
        for r in rows:
            tid = str(r.get("trait_id", ""))
            taxonomy = str(r.get("taxonomy_group", ""))
            observed = bool(r.get("observed_available"))
            matched = str(r.get("matched_observed_examples") or "").strip()
            warnings = []
            if r.get("predicted_soft_fill_candidate_available"):
                warnings.append("predicted_candidate_present_but_not_activated")
            if taxonomy == "target_fungi":
                cls = "IDENTITY_ONLY"
                n_id += 1
            elif observed:
                parsed = conservative_examples(matched)
                if not parsed:
                    cls = "MISSING"
                    n_miss += 1
                    warnings.append("observed_available_flag_set_but_no_parseable_content")
                    if r.get("prediction_allowed_for_trait") is True:
                        pred_req.append(tid)
                else:
                    cls = "OBSERVED"
                    n_obs += 1
            else:
                cls = "MISSING"
                n_miss += 1
                if r.get("prediction_allowed_for_trait") is True:
                    pred_req.append(tid)
            slots.append({"trait_id": tid, "trait_name": str(r.get("trait_name", "")), "class": cls,
                          "observed_available": observed,
                          "matched_observed_examples": matched,
                          "parsed_examples": conservative_examples(matched),
                          "value_status_preview": str(r.get("value_status_preview") or ""),
                          "prediction_allowed_for_trait": bool(r.get("prediction_allowed_for_trait")),
                          "taxonomy_group": taxonomy,
                          "source_resolution_level": str(r.get("source_resolution_level") or ""),
                          "source_type_preview": str(r.get("source_type_preview") or ""),
                          "mapping_contract_id": str(r.get("mapping_contract_id") or ""),
                          "source_record_id": f"{sig}|{tid}",
                          "warnings": warnings})
        return TraitEvidence(source_signature=sig, backend="C8", status="OK", slots=slots,
                             backend_statuses=[{"backend": "C8", "status": "OK",
                                                "detail": f"{len(rows)} slot rows parsed from {self.n_rows}-row index"}],
                             n_slots=len(slots), n_observed=n_obs, n_identity_only=n_id, n_missing=n_miss,
                             all_slots_present=(n_miss == 0 and n_id == 0),
                             prediction_required_slots=pred_req,
                             note="slot classes/conservative parse per t6_prod rules; one OBSERVED does not mean "
                                  "the whole source is complete")


class DehpPackage:
    kind = "SCNET_DEHP_audited_long_table"

    def __init__(self, root: str):
        self.by_sig = {}
        self.reps = {}
        data = Path(root or "") / "data"
        lg = data / "ALL_SIX_SOURCES_PREDICTED_TRAITS_LONG.tsv.gz"
        repsf = data / "BACDIVE_SPECIES_REPRESENTATIVES_ONLY.tsv"
        if not lg.is_file():
            self.error = "SCNET_PACKAGE_ASSET_MISSING"
            return
        self.error = None
        with gzip.open(lg, "rt", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                self.by_sig.setdefault(row["source_signature"], []).append(dict(row))
        if repsf.is_file():
            with repsf.open(encoding="utf-8") as f:
                for row in csv.DictReader(f, delimiter="\t"):
                    self.reps.setdefault(row["source_signature"], []).append(dict(row))

    def traits(self, sig: str) -> TraitEvidence:
        if self.error:
            return TraitEvidence(source_signature=sig, backend="SCNET", status="BACKEND_ERROR",
                                 backend_statuses=[{"backend": "SCNET", "status": "BACKEND_ERROR",
                                                   "detail": self.error}], note=self.error)
        rows = self.by_sig.get(sig, [])
        reps = self.reps.get(sig, [])
        if not rows and not reps:
            return TraitEvidence(source_signature=sig, backend="SCNET", status="NO_RECORD_FOR_KEY",
                                 backend_statuses=[{"backend": "SCNET", "status": "NO_RECORD_FOR_KEY",
                                                   "detail": "exact key not in audited SCNET package; "
                                                             "no same-name forced join"}],
                                 note="no SCNET record for this authoritative key")
        return TraitEvidence(source_signature=sig, backend="SCNET", status="OK",
                             backend_statuses=[{"backend": "SCNET", "status": "OK",
                                                "detail": f"{len(rows)} predicted rows + {len(reps)} "
                                                          f"representative rows, all original columns verbatim"}],
                             predicted_records=[dict(r) for r in rows],
                             representative_records=[dict(r) for r in reps],
                             note=(f"SCNET model output {len(rows)} PREDICTED rows (tool/version/units/NA/"
                                   f"genome_input_sha256/protein_input_sha256/batch/archive sha kept) + {len(reps)} "
                                   f"REPRESENTATIVE registration rows kept in their own scope; predicted values "
                                   f"are not wet-lab observations; representative scope not transferred to target strain"))


def make_traits(cfg):
    c8 = C8Index(cfg.c8_lookup_index) if cfg.c8_lookup_index else None
    dehp = DehpPackage(cfg.dehp_package_root) if cfg.dehp_package_root else None
    return c8, dehp


def collect_traits(c8, dehp, sig: str) -> TraitEvidence:
    """Merge with per-backend visibility: every backend contributes a
    backend_statuses entry; overall status OK only when none errored."""
    if sig == "":
        return TraitEvidence(source_signature="", backend="NONE", status="NO_AUTHORITATIVE_KEY",
                             note="no authoritative source_signature; traits not attached honestly")
    parts = []
    for b in (c8, dehp):
        if b is None:
            parts.append(TraitEvidence(source_signature=sig, backend=b_kind(b) if b else "NONE",
                                       status="NOT_CONFIGURED",
                                       backend_statuses=[{"backend": b_kind(b) if b else "NONE",
                                                         "status": "NOT_CONFIGURED", "detail": "backend not configured"}],
                                       note="backend not configured"))
            continue
        parts.append(b.traits(sig))
    merged = TraitEvidence(source_signature=sig, status="NOT_CONFIGURED",
                           backend="+".join(p.backend for p in parts),
                           backend_statuses=[st for p in parts for st in (p.backend_statuses or
                                       [{"backend": p.backend, "status": p.status, "detail": p.note}])])
    for p in parts:
        merged.slots.extend(p.slots)
        merged.predicted_records.extend(p.predicted_records)
        merged.representative_records.extend(p.representative_records)
        merged.n_slots += p.n_slots
        merged.n_observed += p.n_observed
        merged.n_identity_only += p.n_identity_only
        merged.n_missing += p.n_missing
        merged.prediction_required_slots.extend(p.prediction_required_slots)
    merged.all_slots_present = (merged.n_slots > 0 and merged.n_missing == 0 and merged.n_identity_only == 0)
    statuses = [e["status"] for e in merged.backend_statuses]
    ok_any = any(p.status == "OK" for p in parts)
    err_any = any(p.status in ("BACKEND_ERROR", "C8_ASSET_MISSING_OR_NOT_CONFIGURED") for p in parts)
    if ok_any and err_any:
        merged.status = "OK_WITH_BACKEND_ERRORS"
    elif ok_any:
        merged.status = "OK"
    elif all(p.status == "NO_RECORD_FOR_KEY" for p in parts):
        merged.status = "NO_RECORD_FOR_KEY"
    elif all(p.status == "NOT_CONFIGURED" for p in parts):
        merged.status = "NOT_CONFIGURED"
    else:
        merged.status = parts[0].status
    merged.note = "; ".join(f"{p.backend}: {p.status}" for p in parts)
    if merged.prediction_required_slots or any(p.backend == "SCNET" for p in parts if p.status != "OK"):
        merged.note += f" | prediction-required list scope: {SCNET_REF}"
    return merged


def b_kind(b):
    return getattr(b, "kind", "UNKNOWN") if b is not None else "NONE"
