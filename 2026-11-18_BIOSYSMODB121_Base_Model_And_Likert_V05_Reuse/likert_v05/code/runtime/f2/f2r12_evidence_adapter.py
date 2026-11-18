"""F2 R1 evidence adapter: consume an F3 E0 evidence package through an
explicit, version-bound interface contract (audit F2-P1-02).

Replaces the R0 loose `man.get("items", [])` consumption that silently
delivered an EMPTY evidence block against the real F3 manifest. Rules:

  1. The package is bound by manifest path + expected manifest sha256; every
     consumed file is verified against the manifest's own outputs entries
     (sha256 + bytes). Missing file / sha mismatch / unknown schema →
     E0InterfaceError (NEVER a silent empty block).
  2. Per-case slice derivation is deterministic:
       case → claims (CLAIM_REGISTRY.case_ids, split on [,;])
            → official_record_ids (VERIFICATION_RESULTS, split on [,;])
            → NORMALIZED_RECORDS entries (rater-facing sanitized layer).
     Refs that resolve to records = evidence; refs shaped 'f3e0:*' that do
     NOT resolve = dangling → REJECT (illegal citation, not a gap); other
     refs (e.g. CASE_CLAIM_GROUP_SCOPE_120.tsv#…/CGnn locators) are scope
     locators, listed separately, never presented as evidence records.
  3. A case with zero linked records yields status EVIDENCE_GAP with an
     explicit disclosure block (kept 待核), never an empty section.
  4. Leak defense: record keys are scanned against F3_FORBIDDEN_RECORD_KEYS;
     the slice never contains another model's answer text, historical scores,
     KE verdicts or model identity (the same case-level record union is used
     for all four slots of a case — contract §8.10).
  5. Version binding: package identity (manifest sha, baseline id, per-file
     shas) flows into the item payload, cache key and canonical record; an
     F3 R1 package rebinds by sha — no cross-version reuse.

Interface contract document: E0_INTERFACE_CONTRACT_R1.md (this directory).
Offline: pure local file reads; no network, no model API.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (sha256_file, sha256_bytes, canonical_json,
                         sha256_canonical, F3_REQUIRED_FILES,
                         F3_RECORD_REQUIRED_KEYS, F3_FORBIDDEN_RECORD_KEYS,
                         F3_RECORD_DISCLOSED_OPTIONAL_KEYS)

SPLIT_RE = re.compile(r"[;,]")
RECORD_ID_PATTERN = re.compile(r"^f3e0:")


class E0InterfaceError(RuntimeError):
    pass


def _split_multi(value: str) -> list:
    return [t.strip() for t in SPLIT_RE.split(value or "") if t.strip()]


class E0Package:
    """A verified F3 evidence package bound by manifest identity."""

    def __init__(self, manifest_path: str, expected_manifest_sha256: str,
                 package_label: str = "F3_E0"):
        self.manifest_path = os.path.abspath(manifest_path)
        if not os.path.exists(self.manifest_path):
            raise E0InterfaceError(f"E0 manifest missing: {manifest_path}")
        actual_sha = sha256_file(self.manifest_path)
        if expected_manifest_sha256 and actual_sha != expected_manifest_sha256:
            raise E0InterfaceError(
                f"E0 manifest sha mismatch: actual {actual_sha} != bound {expected_manifest_sha256}")
        self.manifest_sha256 = actual_sha
        with open(self.manifest_path, encoding="utf-8") as f:
            self.manifest = json.load(f)
        self.baseline_id = self.manifest.get("evidence_baseline_id")
        if not self.baseline_id:
            raise E0InterfaceError("E0 manifest lacks evidence_baseline_id — schema incompatible")
        outputs = self.manifest.get("outputs")
        if not isinstance(outputs, dict):
            raise E0InterfaceError("E0 manifest lacks outputs{} — schema incompatible")
        self.package_label = package_label
        self.files = {}       # name → {path, sha256, bytes}
        self._verify_and_load_files()
        self._load_data()
        self._build_case_index()

    # -- verification -------------------------------------------------------
    def _verify_and_load_files(self):
        outputs = self.manifest["outputs"]
        for name, required_cols in F3_REQUIRED_FILES.items():
            entry = outputs.get(name)
            if not isinstance(entry, dict) or "sha256" not in entry:
                raise E0InterfaceError(
                    f"E0 manifest outputs lacks binding for required file {name} — refuse (no silent empty)")
            path = entry.get("path")
            if not path:
                # allow manifest-relative resolution
                path = os.path.join(os.path.dirname(self.manifest_path), name)
            if not os.path.exists(path):
                raise E0InterfaceError(f"E0 required file missing: {name} at {path}")
            actual_sha = sha256_file(path)
            if actual_sha != entry["sha256"]:
                raise E0InterfaceError(
                    f"E0 file {name} sha mismatch: actual {actual_sha} != manifest {entry['sha256']}")
            actual_bytes = os.path.getsize(path)
            if entry.get("bytes") is not None and actual_bytes != entry["bytes"]:
                raise E0InterfaceError(
                    f"E0 file {name} bytes mismatch: actual {actual_bytes} != manifest {entry['bytes']}")
            if name.endswith(".tsv") and required_cols:
                with open(path, encoding="utf-8") as f:
                    header = f.readline().rstrip("\n").split("\t")
                missing = [c for c in required_cols if c not in header]
                if missing:
                    raise E0InterfaceError(
                        f"E0 file {name} schema incompatible: missing columns {missing}")
            self.files[name] = {"path": path, "sha256": actual_sha, "bytes": actual_bytes}

    def _load_data(self):
        # normalized records (rater-facing fact layer)
        self.records = {}
        rec_path = self.files["NORMALIZED_RECORDS.jsonl"]["path"]
        with open(rec_path, encoding="utf-8") as f:
            for ln, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError as e:
                    raise E0InterfaceError(f"NORMALIZED_RECORDS.jsonl line {ln} invalid JSON: {e}")
                rid = rec.get("record_id")
                if not rid:
                    raise E0InterfaceError(f"NORMALIZED_RECORDS.jsonl line {ln} lacks record_id")
                missing = [k for k in F3_RECORD_REQUIRED_KEYS if k not in rec]
                if missing:
                    raise E0InterfaceError(
                        f"record {rid} schema incompatible: missing keys {missing}")
                bad = F3_FORBIDDEN_RECORD_KEYS.intersection(rec.keys())
                if bad:
                    raise E0InterfaceError(
                        f"record {rid} contains forbidden rater-facing keys {sorted(bad)} — leak defense")
                if rid in self.records:
                    raise E0InterfaceError(f"duplicate record_id {rid}")
                self.records[rid] = rec
        # claim registry (coordination layer; used ONLY for case association)
        self.claims_by_case = {}
        with open(self.files["CLAIM_REGISTRY.tsv"]["path"], encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                for cid in _split_multi(row.get("case_ids", "")):
                    self.claims_by_case.setdefault(cid, []).append(row["claim_id"])
        # verification results (claim → record refs)
        self.ver_by_claim = {}
        with open(self.files["VERIFICATION_RESULTS.tsv"]["path"], encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                self.ver_by_claim[row["claim_id"]] = row

    def _build_case_index(self):
        self.case_records = {}     # case → set(record_id)
        self.case_locators = {}    # case → set(non-record locator refs)
        dangling = set()
        for cid, claim_ids in self.claims_by_case.items():
            recs, locs = set(), set()
            for cl in claim_ids:
                v = self.ver_by_claim.get(cl)
                if not v:
                    continue
                for ref in _split_multi(v.get("official_record_ids", "")):
                    if ref in self.records:
                        recs.add(ref)
                    elif RECORD_ID_PATTERN.match(ref):
                        dangling.add(ref)
                    else:
                        locs.add(ref)
            self.case_records[cid] = recs
            self.case_locators[cid] = locs
        if dangling:
            raise E0InterfaceError(
                f"E0 package has dangling record refs (f3e0:* not in NORMALIZED_RECORDS): "
                f"{sorted(dangling)[:5]}… ({len(dangling)} total) — illegal citation, refuse")

    # -- identity -----------------------------------------------------------
    def identity(self) -> dict:
        return {"package_label": self.package_label,
                "manifest_path": self.manifest_path,
                "manifest_sha256": self.manifest_sha256,
                "evidence_baseline_id": self.baseline_id,
                "files": {n: {"sha256": i["sha256"], "bytes": i["bytes"]}
                          for n, i in sorted(self.files.items())},
                "records_total": len(self.records),
                "cases_with_records": sum(1 for v in self.case_records.values() if v),
                "identity_sha256": sha256_canonical(
                    {"m": self.manifest_sha256, "b": self.baseline_id,
                     "f": {n: i["sha256"] for n, i in sorted(self.files.items())}})}

    # -- per-case slice -------------------------------------------------------
    def build_case_slice(self, case_id: str) -> dict:
        """Deterministic per-case evidence slice for the rater request.

        Returns dict: status (E0_RECORDS|EVIDENCE_GAP), records (list of full
        sanitized records sorted by record_id), evidence_ids, locator_refs,
        slice_text (request block), slice_sha256 (over canonical slice JSON).
        """
        if case_id not in self.claims_by_case:
            # case absent from the claim registry entirely: explicit gap,
            # never silent empty (the four slots of the case share this status)
            recs = set()
        else:
            recs = self.case_records.get(case_id, set())
        records = [self.records[rid] for rid in sorted(recs)]
        locator_refs = sorted(self.case_locators.get(case_id, set()))
        if records:
            status = "E0_RECORDS"
            header = (f"E0_FROZEN_SNAPSHOT status=E0_RECORDS baseline_id={self.baseline_id} "
                      f"manifest_sha256={self.manifest_sha256} case={case_id} "
                      f"records={len(records)}")
        else:
            status = "EVIDENCE_GAP"
            header = (f"E0_FROZEN_SNAPSHOT status=EVIDENCE_GAP baseline_id={self.baseline_id} "
                      f"manifest_sha256={self.manifest_sha256} case={case_id}\n"
                      "EVIDENCE_GAP披露：本案在冻结E0基线中没有经claim关联的机器核验事实记录。"
                      "相关声称保持UNRESOLVED待核（未核≠虚构≠CONTRADICTED）；不得凭数据库记忆放行编号类声称；"
                      "该缺口由F3联网查询卡（另行冻结与派发）后续补充，不在本评分请求内解决。")
        lines = [header]
        # explicit per-record disclosure of missing optional annotations
        # (records stay verbatim; nothing silently rewritten or dropped)
        for opt_key in F3_RECORD_DISCLOSED_OPTIONAL_KEYS:
            lacking = [r["record_id"] for r in records
                       if not r.get(opt_key)]
            if lacking:
                lines.append(
                    f"DISCLOSURE_{opt_key.upper()}_ABSENT: {','.join(lacking)} "
                    f"—— 上述记录未随附{opt_key}；评价者不得因此扩展其支持范围，"
                    "相关声称按UNRESOLVED待核处理（缺口属F3层，不在评分请求内解决）。")
        for rec in records:
            lines.append(json.dumps(rec, ensure_ascii=False, sort_keys=True))
        if locator_refs:
            lines.append("SCOPE_LOCATOR_REFS(非证据记录,仅定位参照): " + ";".join(locator_refs))
        slice_text = "\n".join(lines) + "\n"
        slice_obj = {"status": status, "case_id": case_id,
                     "evidence_baseline_id": self.baseline_id,
                     "manifest_sha256": self.manifest_sha256,
                     "evidence_ids": sorted(r["record_id"] for r in records),
                     "locator_refs": locator_refs,
                     "records": records}
        return {"status": status, "records": records,
                "evidence_ids": sorted(r["record_id"] for r in records),
                "locator_refs": locator_refs,
                "slice_text": slice_text,
                "slice_sha256": sha256_canonical(slice_obj),
                "slice_bytes": len(slice_text.encode("utf-8"))}


def load_package_from_binding(binding: dict):
    """binding modes:
      {"mode":"F3_R11_CASE_SLICES_V2",
       "manifest_path":<EVIDENCE_MANIFEST_R1_1.json>,
       "expected_manifest_sha256":…}          → PRIMARY: audited F3 R1.1
                                                 (f3r11_case_slice_v2)
      {"mode":"F3_R1_CASE_SLICES", …}         → superseded R1 v1 path — kept
      {"mode":"F3_E0_PACKAGE", …}             → legacy R0-derived path — kept
      for regression continuity ONLY; production item builds refuse both
      (no silent fallback, repair card §2).
    """
    mode = binding.get("mode")
    mp = binding.get("manifest_path")
    es = binding.get("expected_manifest_sha256")
    if mode in ("F3_R11_CASE_SLICES_V2", "F3_R1_CASE_SLICES",
                "F3_E0_PACKAGE") and (not mp or not es):
        raise E0InterfaceError(
            f"{mode} binding requires manifest_path AND expected_manifest_sha256")
    if mode == "F3_R11_CASE_SLICES_V2":
        return F3R11CaseSlicesV2(mp, es,
                                 package_label=binding.get("package_label", "F3_E0_R1_1"))
    if mode == "F3_R1_CASE_SLICES":
        return F3R1CaseSlices(mp, es,
                              package_label=binding.get("package_label", "F3_E0_R1"))
    if mode == "F3_E0_PACKAGE":
        return E0Package(mp, es,
                         package_label=binding.get("package_label", "F3_E0"))
    raise E0InterfaceError(f"unknown evidence package mode: {mode!r}")


# ==========================================================================
# PRIMARY adapter: the real F3 R1 case-slice interface
# (F3_EVIDENCE_R1/F3_TO_F2_INTERFACE.md, schema f3r1_case_slice_v1)
# ==========================================================================

SLICE_REQUIRED_KEYS = ("case_id", "evidence_baseline_id", "schema_version",
                       "shared_evidence_policy", "entries", "gaps", "counts")
ENTRY_REQUIRED_KEYS = ("evidence_id", "record_class", "canonical_identifier",
                       "evidence_layer", "fact_excerpt", "source",
                       "support_scope", "non_support_scope", "limitations",
                       "related_claims")
RELATED_CLAIM_ALLOWED_KEYS = {"claim_id", "claim_type", "claim_group",
                              "verification_status", "verification_basis",
                              "unresolved_reason"}
GAP_REQUIRED_KEYS = ("gap_id", "kind", "detail", "in_query_plan")


class F3R1CaseSlices:
    """Consumes the F3 R1 package exactly per F3_TO_F2_INTERFACE.md:

      - binds EVIDENCE_MANIFEST_R1.json by sha; verifies CASE_EVIDENCE_MANIFEST,
        NORMALIZED_RECORDS.jsonl and CLAIM_OCCURRENCES.tsv against its outputs;
      - per-case slice file sha re-computed at consumption vs BOTH the case
        manifest row and the package manifest outputs (disagreement → refuse);
      - slice schema check (required keys/types) → refuse on incompatibility,
        never a silent empty block;
      - rater-visible material = SHARED_EVIDENCE section (entries verbatim,
        BYTE-IDENTICAL for the four slots of a case, related_claims stripped)
        + ITEM_CLAIM_MAP section (per-slot filtered claim→evidence mapping via
        CLAIM_OCCURRENCES; claim metadata only — never answer text);
      - gaps/interpretation_layers/pending_external_review are shared and
        delivered verbatim (EVIDENCE_GAP explicit, unverified ≠ fabricated);
      - leak defense: related_claims key whitelist; forbidden record keys scan.
    """

    def __init__(self, manifest_path: str, expected_manifest_sha256: str | None,
                 package_label: str = "F3_E0_R1"):
        self.manifest_path = os.path.abspath(manifest_path)
        if not os.path.exists(self.manifest_path):
            raise E0InterfaceError(f"F3 R1 manifest missing: {manifest_path}")
        actual = sha256_file(self.manifest_path)
        if expected_manifest_sha256 and actual != expected_manifest_sha256:
            raise E0InterfaceError(
                f"F3 R1 manifest sha mismatch: actual {actual} != bound {expected_manifest_sha256}")
        self.manifest_sha256 = actual
        with open(self.manifest_path, encoding="utf-8") as f:
            self.manifest = json.load(f)
        self.baseline_id = self.manifest.get("evidence_baseline_id")
        outputs = self.manifest.get("outputs")
        if not self.baseline_id or not isinstance(outputs, dict):
            raise E0InterfaceError("F3 R1 manifest schema incompatible (baseline_id/outputs)")
        self.package_label = package_label
        self.root = os.path.dirname(self.manifest_path)
        self.outputs = outputs
        self._verify_output("CASE_EVIDENCE_MANIFEST.json")
        self._verify_output("NORMALIZED_RECORDS.jsonl")
        self._verify_output("CLAIM_OCCURRENCES.tsv")
        cm_path = self._out_path("CASE_EVIDENCE_MANIFEST.json")
        with open(cm_path, encoding="utf-8") as f:
            cm = json.load(f)
        self.case_bindings = {c["case_id"]: c for c in cm["cases"]}
        if len(self.case_bindings) != cm.get("cases_total", len(self.case_bindings)):
            raise E0InterfaceError("CASE_EVIDENCE_MANIFEST cases/cases_total inconsistent")
        # occurrences: claim_id → set(b_slot_uid); slot → claim ids
        self.slot_claims = {}
        occ_path = self._out_path("CLAIM_OCCURRENCES.tsv")
        with open(occ_path, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                self.slot_claims.setdefault(row["b_slot_uid"], set()).add(row["claim_id"])
        # record ids (for closure checks)
        self.record_ids = set()
        rec_path = self._out_path("NORMALIZED_RECORDS.jsonl")
        with open(rec_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.record_ids.add(json.loads(line)["record_id"])
        self._slice_cache = {}

    def _out_path(self, name):
        entry = self.outputs.get(name)
        if not isinstance(entry, dict) or "sha256" not in entry:
            raise E0InterfaceError(f"F3 R1 manifest lacks output binding for {name}")
        p = entry.get("path") or os.path.join(self.root, name)
        if not os.path.exists(p):
            raise E0InterfaceError(f"F3 R1 output file missing: {name} at {p}")
        return p

    def _verify_output(self, name):
        p = self._out_path(name)
        entry = self.outputs[name]
        got = sha256_file(p)
        if got != entry["sha256"]:
            raise E0InterfaceError(
                f"F3 R1 output {name} sha mismatch: actual {got} != manifest {entry['sha256']}")
        if entry.get("bytes") is not None and os.path.getsize(p) != entry["bytes"]:
            raise E0InterfaceError(f"F3 R1 output {name} bytes mismatch")

    def _load_slice(self, case_id: str) -> dict:
        if case_id in self._slice_cache:
            return self._slice_cache[case_id]
        cb = self.case_bindings.get(case_id)
        if cb is None:
            raise E0InterfaceError(f"case {case_id} absent from CASE_EVIDENCE_MANIFEST — refuse (not a silent gap)")
        rel = cb["slice_path"]
        p = os.path.join(self.root, rel)
        if not os.path.exists(p):
            raise E0InterfaceError(f"slice file missing: {rel}")
        got = sha256_file(p)
        if got != cb["sha256"]:
            raise E0InterfaceError(f"slice {rel} sha mismatch vs CASE_EVIDENCE_MANIFEST: {got}")
        out_entry = self.outputs.get(rel)
        if out_entry and out_entry.get("sha256") != got:
            raise E0InterfaceError(f"slice {rel} sha disagreement between case manifest and package manifest")
        with open(p, encoding="utf-8") as f:
            s = json.load(f)
        self._check_slice_schema(s, case_id)
        s["_file_sha256"] = got
        s["_file_bytes"] = os.path.getsize(p)
        self._slice_cache[case_id] = s
        return s

    def _check_slice_schema(self, s: dict, case_id: str):
        for k in SLICE_REQUIRED_KEYS:
            if k not in s:
                raise E0InterfaceError(f"slice {case_id} schema incompatible: missing {k}")
        if s["case_id"] != case_id:
            raise E0InterfaceError(f"slice case_id {s['case_id']!r} != requested {case_id!r}")
        if s.get("schema_version") != "f3r1_case_slice_v1":
            raise E0InterfaceError(f"slice {case_id} unknown schema_version {s.get('schema_version')!r}")
        for e in s["entries"]:
            for k in ENTRY_REQUIRED_KEYS:
                if k not in e:
                    raise E0InterfaceError(f"slice {case_id} entry missing key {k}")
            if F3_FORBIDDEN_RECORD_KEYS.intersection(e.keys()):
                raise E0InterfaceError(f"slice {case_id} entry {e.get('evidence_id')} has forbidden keys")
            for rc in e["related_claims"]:
                extra = set(rc.keys()) - RELATED_CLAIM_ALLOWED_KEYS
                if extra:
                    raise E0InterfaceError(
                        f"slice {case_id} related_claim has non-whitelisted keys {sorted(extra)} "
                        "(answer text must never ride along)")
        for g in s["gaps"]:
            for k in GAP_REQUIRED_KEYS:
                if k not in g:
                    raise E0InterfaceError(f"slice {case_id} gap missing key {k}")

    # -- identity --
    def identity(self) -> dict:
        return {"package_label": self.package_label,
                "interface": "f3r1_case_slice_v1",
                "manifest_path": self.manifest_path,
                "manifest_sha256": self.manifest_sha256,
                "evidence_baseline_id": self.baseline_id,
                "cases_bound": len(self.case_bindings),
                "records_total": len(self.record_ids),
                "identity_sha256": sha256_canonical(
                    {"m": self.manifest_sha256, "b": self.baseline_id,
                     "i": "f3r1_case_slice_v1",
                     "cm": self.outputs["CASE_EVIDENCE_MANIFEST.json"]["sha256"]})}

    # -- shared (byte-identical across the four slots) --
    def shared_evidence_section(self, case_id: str) -> tuple[str, str, list]:
        """Returns (shared_text, slice_file_sha, evidence_ids). Entries are
        serialized verbatim minus related_claims (claim mapping is per-item)."""
        s = self._load_slice(case_id)
        entries_shared = []
        for e in s["entries"]:
            e2 = {k: v for k, v in e.items() if k != "related_claims"}
            entries_shared.append(e2)
        obj = {"section": "SHARED_EVIDENCE", "case_id": case_id,
               "evidence_baseline_id": s["evidence_baseline_id"],
               "schema_version": s["schema_version"],
               "shared_evidence_policy": s["shared_evidence_policy"],
               "entries": entries_shared,
               "gaps": s["gaps"],
               "interpretation_layers": s.get("interpretation_layers") or [],
               "pending_external_review": s.get("pending_external_review") or [],
               "counts": s["counts"]}
        text = json.dumps(obj, ensure_ascii=False, sort_keys=True)
        ids = [e["evidence_id"] for e in s["entries"]]
        return text, s["_file_sha256"], ids

    # -- per-item claim sub-view (filtered by slot occurrences) --
    def item_claim_map(self, case_id: str, b_slot_uid: str) -> str:
        s = self._load_slice(case_id)
        slot_claims = self.slot_claims.get(b_slot_uid, set())
        mapping = []
        for e in s["entries"]:
            mine = [rc for rc in e["related_claims"] if rc["claim_id"] in slot_claims]
            if mine:
                mapping.append({"evidence_id": e["evidence_id"],
                                "claims": sorted(mine, key=lambda x: x["claim_id"])})
        obj = {"section": "ITEM_CLAIM_MAP", "case_id": case_id,
               "note": ("本答案声称与证据记录的关联子视图（协调侧按CLAIM_OCCURRENCES以槽位过滤后生成；"
                        "仅claim元数据，不含任何答案原文、槽位ID、其他槽内容或模型身份）。"
                        "未列入的声称≠虚构，按UNRESOLVED待核处理。"),
               "claim_to_evidence": mapping}
        return json.dumps(obj, ensure_ascii=False, sort_keys=True)

    # -- combined per-item block --
    def build_item_evidence(self, case_id: str, b_slot_uid: str) -> dict:
        shared_text, slice_sha, ids = self.shared_evidence_section(case_id)
        claim_map_text = self.item_claim_map(case_id, b_slot_uid)
        s = self._slice_cache[case_id]
        status = "E0_RECORDS" if s["entries"] else "EVIDENCE_GAP"
        header = (f"E0R1_FROZEN_SNAPSHOT status={status} interface=f3r1_case_slice_v1 "
                  f"baseline_id={self.baseline_id} manifest_sha256={self.manifest_sha256} "
                  f"case={case_id} slice_file_sha256={slice_sha} entries={len(s['entries'])} "
                  f"gaps={len(s['gaps'])}")
        if status == "EVIDENCE_GAP":
            header += ("\nEVIDENCE_GAP披露：本案切片无证据记录（见gaps逐条显式登记，含in_query_plan标记）。"
                       "相关声称保持UNRESOLVED待核；未核≠虚构≠CONTRADICTED；不得凭数据库记忆放行编号类声称。")
        block = "\n".join([header, shared_text, claim_map_text]) + "\n"
        block_obj_sha = sha256_canonical({"shared_sha256": sha256_bytes(shared_text.encode()),
                                          "claim_map_sha256": sha256_bytes(claim_map_text.encode()),
                                          "slice_file_sha256": slice_sha})
        return {"status": status, "evidence_ids": ids,
                "block_text": block, "block_sha256": block_obj_sha,
                "shared_text_sha256": sha256_bytes(shared_text.encode("utf-8")),
                "claim_map_text_sha256": sha256_bytes(claim_map_text.encode("utf-8")),
                "slice_file_sha256": slice_sha,
                "slice_bytes": s["_file_bytes"],
                "block_bytes": len(block.encode("utf-8"))}

    # compatibility shim so both adapters present one face to the item builder
    def build_case_slice(self, case_id: str) -> dict:
        shared_text, slice_sha, ids = self.shared_evidence_section(case_id)
        s = self._slice_cache[case_id]
        status = "E0_RECORDS" if s["entries"] else "EVIDENCE_GAP"
        return {"status": status, "evidence_ids": ids,
                "slice_text": shared_text, "slice_sha256": slice_sha,
                "slice_bytes": s["_file_bytes"], "records": s["entries"]}


# ==========================================================================
# PRIMARY adapter (R1.1): the AUDITED F3 R1.1 package
# (F3_EVIDENCE_R1_1/F3_TO_F2_INTERFACE.md, schema f3r11_case_slice_v2,
#  baseline E0R11_20261029_SAME_FACTS_AS_R1)
#
# v2 policy (vs v1): the OFFICIAL FACT SET (entries' fact fields +
# interpretation layers) is shared byte-identically by all four items of a
# case; only related_claims annotations and item-level gaps are filtered per
# slot via the FULL CLAIM_OCCURRENCES mapping; entries without current-slot
# claims are KEPT with related_claims=[] (facts never removed by slot
# filtering); case-level EVIDENCE_GAP_CASE_NO_RECORDS is always visible with
# its full claim list. F7 interpretation layers (notes_text/panel_content)
# are sha-verified locally and delivered INLINE in the request (the remote
# rater cannot open local paths).
#
# The audited parent manifest carries NO top-level evidence_baseline_id:
# baseline/schema identity is read from the bound CASE_EVIDENCE_MANIFEST and
# re-verified in every slice (exact VALUES, not key presence).
# ==========================================================================

F3R11_SCHEMA_VERSION = "f3r11_case_slice_v2"
F3R11_BASELINE = "E0R11_20261029_SAME_FACTS_AS_R1"
V2_SLICE_REQUIRED_KEYS = ("case_id", "evidence_baseline_id", "schema_version",
                          "shared_evidence_policy", "entries", "gaps",
                          "interpretation_layers", "pending_external_review",
                          "counts")
V2_ENTRY_REQUIRED_KEYS = ("evidence_id", "record_class", "canonical_identifier",
                          "evidence_layer", "record_status", "fact_excerpt",
                          "source", "support_scope", "non_support_scope",
                          "limitations", "related_claims")
V2_GAP_REQUIRED_KEYS = ("gap_id", "kind", "detail", "in_query_plan")
V2_CASE_GAP_KIND = "EVIDENCE_GAP_CASE_NO_RECORDS"
V2_RELATED_CLAIM_ALLOWED_KEYS = {"claim_id", "claim_type", "claim_group",
                                 "verification_status", "verification_basis",
                                 "unresolved_reason"}
V2_LAYER_REQUIRED_KEYS = ("layer_id", "applies_to", "note", "notes_text",
                          "notes_sha256", "panel_content", "panel_sha256")


class F3R11CaseSlicesV2:
    """Audited F3 R1.1 consumer. Strict rejection paths (never silent empty):
    parent manifest sha; CASE_EVIDENCE_MANIFEST/CLAIM_OCCURRENCES/
    NORMALIZED_RECORDS per-file sha+bytes from parent outputs; per-slice sha
    +bytes at consumption; slice schema (keys, TYPES, and exact case_id/
    schema_version/baseline VALUES); F7 notes/panel text sha; slot/case pair
    via occurrences (SLOT_NOT_IN_OCCURRENCES); missing occurrences table;
    forbidden keys / non-whitelisted related_claim keys (answer-text riders).
    """

    def __init__(self, manifest_path: str, expected_manifest_sha256: str | None,
                 package_label: str = "F3_E0_R1_1"):
        self.manifest_path = os.path.abspath(manifest_path)
        if not os.path.exists(self.manifest_path):
            raise E0InterfaceError(f"F3 R1.1 manifest missing: {manifest_path}")
        actual = sha256_file(self.manifest_path)
        if expected_manifest_sha256 and actual != expected_manifest_sha256:
            raise E0InterfaceError(
                f"F3 R1.1 manifest sha mismatch: actual {actual} != bound {expected_manifest_sha256}")
        self.manifest_sha256 = actual
        with open(self.manifest_path, encoding="utf-8") as f:
            self.manifest = json.load(f)
        outputs = self.manifest.get("outputs")
        if not isinstance(outputs, dict):
            raise E0InterfaceError("F3 R1.1 manifest schema incompatible (no outputs{})")
        self.outputs = outputs
        self.root = os.path.dirname(self.manifest_path)
        self.package_label = package_label
        # --- bound case manifest: source of baseline/schema identity ---
        self._verify_output("CASE_EVIDENCE_MANIFEST.json")
        self._verify_output("CLAIM_OCCURRENCES.tsv")
        self._verify_output("NORMALIZED_RECORDS.jsonl")
        with open(self._out_path("CASE_EVIDENCE_MANIFEST.json"), encoding="utf-8") as f:
            cm = json.load(f)
        self.baseline_id = cm.get("evidence_baseline_id")
        self.schema_version = cm.get("slice_schema_version")
        if self.baseline_id != F3R11_BASELINE:
            raise E0InterfaceError(
                f"case manifest baseline {self.baseline_id!r} != audited {F3R11_BASELINE!r}")
        if self.schema_version != F3R11_SCHEMA_VERSION:
            raise E0InterfaceError(
                f"case manifest slice_schema_version {self.schema_version!r} != {F3R11_SCHEMA_VERSION!r}")
        cases = cm.get("cases")
        if not isinstance(cases, list) or not cases:
            raise E0InterfaceError("case manifest schema incompatible (cases list)")
        self.case_bindings = {c["case_id"]: c for c in cases}
        if len(self.case_bindings) != cm.get("cases_total", len(self.case_bindings)):
            raise E0InterfaceError("case manifest cases/cases_total inconsistent")
        self.case_manifest_sha256 = sha256_file(self._out_path("CASE_EVIDENCE_MANIFEST.json"))
        # --- occurrences: (case_id, slot) → claim ids; slot → claim ids ---
        self.slot_case_claims = {}
        occ_path = self._out_path("CLAIM_OCCURRENCES.tsv")
        with open(occ_path, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                key = (row["case_id"], row["b_slot_uid"])
                self.slot_case_claims.setdefault(key, set()).add(row["claim_id"])
        if not self.slot_case_claims:
            raise E0InterfaceError("CLAIM_OCCURRENCES empty — item filtering cannot proceed safely")
        # --- record ids (closure checks) ---
        self.record_ids = set()
        with open(self._out_path("NORMALIZED_RECORDS.jsonl"), encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.record_ids.add(json.loads(line)["record_id"])
        self._slice_cache = {}

    # -- infrastructure --
    def _out_path(self, name):
        entry = self.outputs.get(name)
        if not isinstance(entry, dict) or "sha256" not in entry:
            raise E0InterfaceError(f"F3 R1.1 manifest lacks output binding for {name}")
        p = entry.get("path") or os.path.join(self.root, name)
        if not os.path.exists(p):
            raise E0InterfaceError(f"F3 R1.1 output file missing: {name} at {p}")
        return p

    def _verify_output(self, name):
        p = self._out_path(name)
        entry = self.outputs[name]
        got = sha256_file(p)
        if got != entry["sha256"]:
            raise E0InterfaceError(
                f"F3 R1.1 output {name} sha mismatch: actual {got} != manifest {entry['sha256']}")
        if entry.get("bytes") is not None and os.path.getsize(p) != entry["bytes"]:
            raise E0InterfaceError(f"F3 R1.1 output {name} bytes mismatch")

    def _load_slice(self, case_id: str) -> dict:
        if case_id in self._slice_cache:
            return self._slice_cache[case_id]
        cb = self.case_bindings.get(case_id)
        if cb is None:
            raise E0InterfaceError(
                f"case {case_id} absent from CASE_EVIDENCE_MANIFEST — refuse (not a silent gap)")
        rel = cb.get("slice_path")
        p = os.path.join(self.root, rel) if rel else None
        if not p or not os.path.exists(p):
            raise E0InterfaceError(f"slice file missing for {case_id}: {rel!r}")
        got = sha256_file(p)
        if got != cb.get("sha256"):
            raise E0InterfaceError(
                f"slice {rel} sha mismatch vs case manifest: actual {got} != bound {cb.get('sha256')} "
                "(tamper or version drift — external binding refuses)")
        if cb.get("bytes") is not None and os.path.getsize(p) != cb["bytes"]:
            raise E0InterfaceError(f"slice {rel} bytes mismatch vs case manifest")
        out_entry = self.outputs.get(rel)
        if out_entry and out_entry.get("sha256") != got:
            raise E0InterfaceError(
                f"slice {rel} sha disagreement between case manifest and parent manifest outputs")
        with open(p, encoding="utf-8") as f:
            s = json.load(f)
        self._check_slice_schema(s, case_id)
        s["_file_sha256"] = got
        s["_file_bytes"] = os.path.getsize(p)
        self._slice_cache[case_id] = s
        return s

    def _check_slice_schema(self, s: dict, case_id: str):
        for k in V2_SLICE_REQUIRED_KEYS:
            if k not in s:
                raise E0InterfaceError(f"slice {case_id} schema incompatible: missing key {k}")
        if s["case_id"] != case_id:
            raise E0InterfaceError(f"slice case_id {s['case_id']!r} != requested {case_id!r}")
        if s["schema_version"] != F3R11_SCHEMA_VERSION:
            raise E0InterfaceError(
                f"slice {case_id} schema_version {s['schema_version']!r} != {F3R11_SCHEMA_VERSION!r} (no v1 downgrade)")
        if s["evidence_baseline_id"] != F3R11_BASELINE:
            raise E0InterfaceError(
                f"slice {case_id} baseline {s['evidence_baseline_id']!r} != case-manifest baseline {F3R11_BASELINE!r}")
        if not isinstance(s["entries"], list) or not isinstance(s["gaps"], list) \
                or not isinstance(s["interpretation_layers"], list):
            raise E0InterfaceError(f"slice {case_id} schema type error (entries/gaps/layers)")
        for e in s["entries"]:
            for k in V2_ENTRY_REQUIRED_KEYS:
                if k not in e:
                    raise E0InterfaceError(f"slice {case_id} entry missing key {k}")
            if F3_FORBIDDEN_RECORD_KEYS.intersection(e.keys()):
                raise E0InterfaceError(
                    f"slice {case_id} entry {e.get('evidence_id')} has forbidden keys (leak defense)")
            for rc in e["related_claims"]:
                extra = set(rc.keys()) - V2_RELATED_CLAIM_ALLOWED_KEYS
                if extra:
                    raise E0InterfaceError(
                        f"slice {case_id} related_claim has non-whitelisted keys {sorted(extra)} "
                        "(answer text must never ride along)")
        for g in s["gaps"]:
            for k in V2_GAP_REQUIRED_KEYS:
                if k not in g:
                    raise E0InterfaceError(f"slice {case_id} gap missing key {k}")
            if not isinstance(g.get("claim_ids", []), list):
                raise E0InterfaceError(f"slice {case_id} gap claim_ids type error")
        for layer in s["interpretation_layers"]:
            for k in V2_LAYER_REQUIRED_KEYS:
                if k not in layer:
                    raise E0InterfaceError(f"slice {case_id} interpretation layer missing key {k}")
            if sha256_bytes(layer["notes_text"].encode("utf-8")) != layer["notes_sha256"]:
                raise E0InterfaceError(
                    f"slice {case_id} F7 notes_text sha mismatch vs notes_sha256 (content integrity)")
            if sha256_bytes(layer["panel_content"].encode("utf-8")) != layer["panel_sha256"]:
                raise E0InterfaceError(
                    f"slice {case_id} F7 panel_content sha mismatch vs panel_sha256 (content integrity)")

    # -- identity --
    def identity(self) -> dict:
        return {"package_label": self.package_label,
                "interface": F3R11_SCHEMA_VERSION,
                "manifest_path": self.manifest_path,
                "manifest_sha256": self.manifest_sha256,
                "case_manifest_sha256": self.case_manifest_sha256,
                "evidence_baseline_id": self.baseline_id,
                "cases_bound": len(self.case_bindings),
                "records_total": len(self.record_ids),
                "occurrence_pairs": len(self.slot_case_claims),
                "identity_sha256": sha256_canonical(
                    {"m": self.manifest_sha256, "cm": self.case_manifest_sha256,
                     "b": self.baseline_id, "i": F3R11_SCHEMA_VERSION})}

    # -- views --
    def case_facts(self, case_id: str) -> dict:
        """Fact-only view (coordination/acceptance): the full shared slice,
        never sent wholesale to the remote rater (item builder assembles the
        rater block from shared facts + item annotations)."""
        return self._load_slice(case_id)

    def slot_claim_set(self, case_id: str, b_slot_uid: str) -> set:
        claims = self.slot_case_claims.get((case_id, b_slot_uid))
        if not claims:
            raise E0InterfaceError(
                f"SLOT_NOT_IN_OCCURRENCES case={case_id} slot={b_slot_uid} "
                "(wrong slot/case pair rejected; occurrences are the authority)")
        return claims

    def build_item_evidence(self, case_id: str, b_slot_uid: str) -> dict:
        """Rater-visible evidence for ONE item:
          SHARED_OFFICIAL_FACTS  — entries' fact fields (related_claims
                                   stripped) + interpretation layers with F7
                                   notes/panel FULL TEXT inline + case-level
                                   gap (full claim list): byte-identical for
                                   all four slots of the case;
          ITEM_CLAIM_ANNOTATIONS — per-entry related_claims filtered to this
                                   slot's claims (entries kept even when empty)
                                   + item-level gaps filtered by the full
                                   occurrence mapping. No other-slot claims,
                                   no answer text, no slot uid, no model id.
        """
        s = self._load_slice(case_id)
        my_claims = self.slot_claim_set(case_id, b_slot_uid)

        shared_entries = [{k: v for k, v in e.items() if k != "related_claims"}
                          for e in s["entries"]]
        case_gap = next((g for g in s["gaps"]
                         if g["kind"] == V2_CASE_GAP_KIND), None)
        shared_obj = {"section": "SHARED_OFFICIAL_FACTS", "case_id": case_id,
                      "evidence_baseline_id": s["evidence_baseline_id"],
                      "schema_version": s["schema_version"],
                      "shared_evidence_policy": s["shared_evidence_policy"],
                      "entries": shared_entries,
                      "interpretation_layers": s["interpretation_layers"],
                      "case_level_gap": case_gap,
                      "pending_external_review": s["pending_external_review"]}
        shared_text = json.dumps(shared_obj, ensure_ascii=False, sort_keys=True)

        annotations = []
        for e in s["entries"]:
            mine = [rc for rc in e["related_claims"] if rc["claim_id"] in my_claims]
            annotations.append({"evidence_id": e["evidence_id"],
                                "related_claims": sorted(mine, key=lambda x: x["claim_id"])})
        item_gaps = [g for g in s["gaps"]
                     if g["kind"] != V2_CASE_GAP_KIND
                     and any(cid in my_claims for cid in g.get("claim_ids", []))]
        ann_obj = {"section": "ITEM_CLAIM_ANNOTATIONS", "case_id": case_id,
                   "note": ("本答案声称与官方事实记录的关联注释及item级证据缺口（协调侧按完整"
                            "CLAIM_OCCURRENCES以槽过滤生成；仅claim元数据与缺口登记，不含任何答案原文、"
                            "槽位ID、模型身份或其他槽内容）。未列入的声称≠虚构，按UNRESOLVED待核处理；"
                            "送达记录不升级claim：核验状态原样（UNRESOLVED保持UNRESOLVED）。"),
                   "claim_annotations": annotations,
                   "item_gaps": item_gaps}
        ann_text = json.dumps(ann_obj, ensure_ascii=False, sort_keys=True)

        status = "E0_RECORDS" if s["entries"] else "EVIDENCE_GAP"
        header = (f"E0R11_FROZEN_SNAPSHOT status={status} interface={F3R11_SCHEMA_VERSION} "
                  f"baseline_id={self.baseline_id} manifest_sha256={self.manifest_sha256} "
                  f"case={case_id} slice_file_sha256={s['_file_sha256']} entries={len(s['entries'])} "
                  f"gaps_total={len(s['gaps'])} interpretation_layers={len(s['interpretation_layers'])}")
        if status == "EVIDENCE_GAP":
            header += ("\nEVIDENCE_GAP披露：本案切片无官方事实记录（整题GAP见case_level_gap逐条登记，含in_query_plan标记）。"
                       "相关声称保持UNRESOLVED待核；未核≠虚构≠CONTRADICTED；不得凭数据库记忆放行编号类声称；"
                       "不得因无证据静默剔题或猜分。")
        if s["interpretation_layers"]:
            header += ("\nF7解释层提示：以下interpretation_layers含BacDive 153432/12880底物面板的测量符号(+/-)与测试类型恢复全文"
                       "（notes_text与panel_content已按SHA核验并全文装入本请求）。F7判定前必读NOTES：裸名称列表≠阳性碳源清单；"
                       "培养温度记录≠最适温度；不得越级外推。")
        block = "\n".join([header, shared_text, ann_text]) + "\n"
        block_sha = sha256_canonical({
            "shared_sha256": sha256_bytes(shared_text.encode("utf-8")),
            "annotations_sha256": sha256_bytes(ann_text.encode("utf-8")),
            "slice_file_sha256": s["_file_sha256"]})
        return {"status": status,
                "evidence_ids": [e["evidence_id"] for e in s["entries"]],
                "block_text": block,
                "block_sha256": block_sha,
                "shared_text": shared_text,
                "shared_text_sha256": sha256_bytes(shared_text.encode("utf-8")),
                "annotations_text": ann_text,
                "annotations_sha256": sha256_bytes(ann_text.encode("utf-8")),
                "slice_file_sha256": s["_file_sha256"],
                "slice_bytes": s["_file_bytes"],
                "block_bytes": len(block.encode("utf-8")),
                "counts": {"slot_claims_total": len(my_claims),
                           "entries_total": len(s["entries"]),
                           "entries_with_slot_claims": sum(1 for a in annotations if a["related_claims"]),
                           "item_gaps": len(item_gaps),
                           "case_level_gap": case_gap is not None,
                           "interpretation_layers": len(s["interpretation_layers"])}}

    # compatibility shim (measurement/acceptance helpers)
    def build_case_slice(self, case_id: str) -> dict:
        s = self._load_slice(case_id)
        shared_entries = [{k: v for k, v in e.items() if k != "related_claims"}
                          for e in s["entries"]]
        text = json.dumps({"entries": shared_entries,
                           "interpretation_layers": s["interpretation_layers"],
                           "gaps": s["gaps"]}, ensure_ascii=False, sort_keys=True)
        return {"status": "E0_RECORDS" if s["entries"] else "EVIDENCE_GAP",
                "evidence_ids": [e["evidence_id"] for e in s["entries"]],
                "slice_text": text,
                "slice_sha256": sha256_bytes(text.encode("utf-8")),
                "slice_bytes": s["_file_bytes"], "records": s["entries"]}
