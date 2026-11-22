"""Host provenance backend (R2): B1 revision1 cohort table.
Row-presence vs resolved-source stay separate; each row additionally carries
its own evidence_ids pointers plus the file identity + uid row key so any
claim remains locatable."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .schemas import HostSource


class B1Revision1Table:
    kind = "b1_revision1_exact_uid_table"

    def __init__(self, path):
        self.path = str(path)
        self.rows = {}
        p = Path(path)
        if not p.is_file():
            self.error = "SOURCES_TABLE_MISSING"
            return
        self.error = None
        with p.open(encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                self.rows[row["scientific_uid"]] = row

    def lookup(self, uid: str) -> HostSource:
        if self.error:
            return HostSource(uid=uid, status=self.error,
                              evidence_source_file=self.path)
        r = self.rows.get(uid)
        if r is None:
            return HostSource(uid=uid, status="UID_NOT_IN_B1_COHORT", row_present=False,
                              evidence_source_file=self.path,
                              note="B1 revision1 covers the fixed 7468 ranking cohort; hand to an external resolver")
        ls = r.get("lookup_status", "")
        src_status = ls if ls in ("FOUND", "FOUND_SOURCE_SET", "NO_HIT", "IDENTITY_CONFLICT", "QUERY_ERROR") else "UNKNOWN_STATUS"
        auth = (r.get("hist_source_signature") or "").strip()
        try:
            eids = json.loads(r.get("evidence_ids_json") or "[]")
            eids = [str(x) for x in eids if isinstance(x, list) or isinstance(x, str)] if isinstance(eids, list) else []
        except Exception:
            eids = []
        return HostSource(
            uid=uid, status="ROW_PRESENT", row_present=True,
            source_status=src_status,
            authoritative_source_signature=auth,
            source_key_status=("AUTHORITATIVE_KEY_PRESENT" if auth else "AUTHORITATIVE_KEY_UNRESOLVED"),
            lookup_route=r.get("lookup_route", ""),
            source_resolution=r.get("source_resolution", ""),
            orig_taxid=r.get("orig_taxid", ""), orig_organism_name=r.get("orig_organism_name", ""),
            cur_tax_id=r.get("cur_tax_id", ""),
            cur_species_tax_id=r.get("cur_species_tax_id", ""), cur_species_name=r.get("cur_species_name", ""),
            current_taxonomy_group=r.get("current_taxonomy_group", ""),
            in_microbe_scope=(None if r.get("in_microbe_scope", "") in ("", "UNKNOWN")
                              else r["in_microbe_scope"] == "true"),
            microbe_scope_stage=r.get("microbe_scope_stage", ""),
            original_strains=_jlist(r.get("original_strains_json")),
            proteome_linked_strains=[{"proteome_id": p.get("proteome_id"), "strain": p.get("strain") or "",
                                      "organism": p.get("proteome_organism") or ""}
                                     for p in _jlist(r.get("proteome_linked_strains_json")) if isinstance(p, dict)],
            representative_registration_coverage=r.get("representative_registration_coverage", ""),
            representative_validation=r.get("representative_validation", ""),
            reviewed=r.get("cur_reviewed", "") or r.get("hist_reviewed", ""),
            protein_existence_raw=r.get("protein_existence_raw", ""),
            protein_existence=r.get("protein_existence", ""),
            source_stage=r.get("source_stage", ""), source_binding_kind=r.get("source_binding_kind", ""),
            note=r.get("source_resolution_reason", ""),
            evidence_ids=eids,
            evidence_source_file=self.path,
            evidence_row_key=f"{self.path}::{uid}")


def _jlist(v):
    try:
        out = json.loads(v or "[]")
        return out if isinstance(out, list) else []
    except Exception:
        return []


def make_sources(cfg, injected=None):
    if injected is not None:
        return injected  # TEST_DOUBLE (harness only)
    if cfg.backend == "b1_revision1_table" and cfg.b1_table:
        return B1Revision1Table(cfg.b1_table)
    return None


def authoritative_sig(host: HostSource) -> str:
    return host.authoritative_source_signature if host.status == "ROW_PRESENT" else ""
