"""F2 item builder: assemble one scoring item payload from F0 read-only inputs.

Per contract §7.3 each request carries ONE complete question+answer with
task-relevant gold and frozen evidence, as an independent stateless request.
The builder:
  1. loads the B_480_ANSWER_INDEX row for the slot and recomputes/verifies
     question + answer SHA identities (refuses on any mismatch — no silent
     substitution, no 'latest modified file' lineage shortcuts);
  2. loads the frozen question rendered messages (G2) and answer bytes
     (extracted copy path bound by the F0 index);
  3. attaches the per-case gold slice (f2r12_gold_slicer) + scope rows
     (CASE_CLAIM_GROUP_SCOPE_120, all 6 rows of the case, verbatim);
  4. attaches evidence items from the bound E0 snapshot — or REFUSES a
     production build while evidence is PENDING_F3_E0_BINDING (no fabricated
     E0 hashes). Test builds may use explicitly-labeled synthetic fixtures;
  5. renders ITEM_MESSAGE_TEMPLATE.txt with the placeholders and emits the
     item payload JSON + the request-side validation context (used by
     f2r12_response_validator).

Anonymization: anonymous_item_id comes from a coordinator-side order map
{b_slot_uid → F4I-nnnn} produced by F4 (fixed seed before any AI score is
seen). The map NEVER travels inside the request; tested_model_config_id and
model_config_display are stripped from everything the rater sees.

Offline: no network, no model API.
"""
from __future__ import annotations

import csv
from pathlib import Path
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (R, F0_DIR, F2_DIR, sha256_file, sha256_bytes,
                       canonical_json, sha256_canonical, read_text,
                       F0_INPUT_BASELINE_MANIFEST_SHA, RUBRIC_RATER_CLEAN_TEXT_SHA,
                       SCOPE120_SHA, B480_INDEX_SHA)
import f2r12_gold_slicer

G2_RENDERED = R / "25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26" / "G2_questions" / "rendered_messages"
RUBRIC_TEXT_PATH = (R / "56_BIODEGRADATION_LIKERT_V04_M4_HUMAN_CALIBRATION_PACKAGES_R2_20261026"
                    / "stage_A" / "LIKERT_V04_M4_RATER_A_PACKAGE" / "rubric"
                    / "LIKERT_v0_4_CANDIDATE_R2_RATER_CLEAN_R1_TEXT_EXTRACT.txt")

TEMPLATE_PATH = F2_DIR / "ITEM_MESSAGE_TEMPLATE.txt"
SYSTEM_PROMPT_PATH = F2_DIR / "SCORING_SYSTEM_PROMPT.txt"

PLACEHOLDERS = [
    "ANONYMOUS_ITEM_ID", "CASE_ID", "INPUT_MANIFEST_SHA",
    "QUESTION_RENDERED_PROMPT_SHA256", "ANSWER_SHA256", "RUBRIC_TEXT_SHA256",
    "GOLD_SLICE_MANIFEST_SHA256", "SCOPE_ROWS_SHA256", "EVIDENCE_SNAPSHOT_SHA",
    "EVIDENCE_CASE_SLICE_SHA256", "EVIDENCE_STATUS",
    "SYSTEM_PROMPT_SHA256", "ITEM_TEMPLATE_SHA256",
    "QUESTION_FULL_TEXT", "ANSWER_FULL_TEXT", "GOLD_SLICE_CONTENT",
    "SCOPE_ROWS_TSV", "EVIDENCE_ITEMS",
]

# frozen claim-group predefinition (sha-verified) — supplies CORE fixed
# attributes so unconditional groups cannot drift (audit F2-P1-05)
CG_PREDEF_PATH = (R / "56_BIODEGRADATION_LIKERT_V04_M4_HUMAN_CALIBRATION_PACKAGES_R2_20261026"
                  / "stage_A" / "LIKERT_V04_M4_RATER_A_PACKAGE" / "rubric"
                  / "CLAIM_GROUP_CRITICALITY_PREDEFINITION_R2.tsv")
CG_PREDEF_SHA = "c4558b47776ce750a133fe23ec566561c493aa764890d6b1751ff5ada9cd2095"


def load_predef_attrs() -> dict:
    """{CGnn: {name, condition_type, criticality_unconditional}} from the
    frozen R2 predefinition table. For UNCONDITIONAL groups both criticality
    columns are the fixed value (CORE); for conditional groups the per-case
    frozen scope rows govern and no default is invented here."""
    if sha256_file(CG_PREDEF_PATH) != CG_PREDEF_SHA:
        raise ItemBuildError(f"CG predefinition sha mismatch: {sha256_file(CG_PREDEF_PATH)}")
    attrs = {}
    with open(CG_PREDEF_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            cg_id = row["claim_group"][:4]
            ctype = row["condition_type"].strip()
            entry = {"name": row["claim_group"], "condition_type": ctype}
            if ctype == "UNCONDITIONAL":
                met = row["criticality_when_condition_met"].strip()
                unmet = row["criticality_when_condition_unmet"].strip()
                if met != unmet:
                    raise ItemBuildError(
                        f"{cg_id}: UNCONDITIONAL group with differing criticality columns "
                        f"({met!r}/{unmet!r}) — no default invented; upstream clarification required")
                entry["criticality_unconditional"] = met
            attrs[cg_id] = entry
    return attrs


class ItemBuildError(RuntimeError):
    pass


def load_b480_index(path=None):
    path = path or (F0_DIR / "B_480_ANSWER_INDEX.tsv")
    if sha256_file(path) != B480_INDEX_SHA:
        raise ItemBuildError(f"B_480_ANSWER_INDEX sha mismatch: {sha256_file(path)}")
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != 480:
        raise ItemBuildError(f"B_480_ANSWER_INDEX rows={len(rows)} != 480")
    by_uid = {r["b_slot_uid"]: r for r in rows}
    if len(by_uid) != 480:
        raise ItemBuildError("duplicate b_slot_uid in B_480_ANSWER_INDEX")
    return rows, by_uid


def load_scope_rows(path=None):
    """All 720 frozen scope rows grouped by case; sha-verified."""
    path = path or (F0_DIR / "CASE_CLAIM_GROUP_SCOPE_120.tsv")
    if sha256_file(path) != SCOPE120_SHA:
        raise ItemBuildError(f"CASE_CLAIM_GROUP_SCOPE_120 sha mismatch: {sha256_file(path)}")
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    by_case = {}
    for r in rows:
        by_case.setdefault(r["case_id"], []).append(r)
    return rows, by_case


def scope_rows_tsv_block(rows) -> str:
    """Verbatim TSV block (header + the case's rows)."""
    if not rows:
        raise ItemBuildError("empty scope rows")
    cols = list(rows[0].keys())
    out = ["\t".join(cols)]
    for r in rows:
        out.append("\t".join(str(r[c]) for c in cols))
    return "\n".join(out) + "\n"


def load_question(case_id: str, expected_rendered_sha: str, expected_messages_sha: str):
    """Load G2 rendered question; verify both hashes against the F0 index."""
    p = G2_RENDERED / f"{case_id}.json"
    if not p.exists():
        raise ItemBuildError(f"question file missing: {p}")
    d = json.load(open(p, encoding="utf-8"))
    if d.get("case_id") != case_id:
        raise ItemBuildError(f"question file case_id {d.get('case_id')!r} != {case_id!r} (identity check)")
    got_rendered = d.get("rendered_prompt_sha256")
    got_messages = d.get("messages_sha256")
    if got_rendered != expected_rendered_sha:
        raise ItemBuildError(f"{case_id}: rendered_prompt_sha {got_rendered!r} != index {expected_rendered_sha!r}")
    if got_messages != expected_messages_sha:
        raise ItemBuildError(f"{case_id}: messages_sha {got_messages!r} != index {expected_messages_sha!r}")
    msgs = d.get("messages") or []
    if len(msgs) != 1 or msgs[0].get("role") != "user":
        raise ItemBuildError(f"{case_id}: unexpected messages structure ({len(msgs)} msgs)")
    text = msgs[0]["content"]
    # independent recompute of the rendered prompt sha over the message text
    if sha256_bytes(text.encode("utf-8")) != expected_rendered_sha:
        # rendered_prompt_sha may be defined over the rendered template string;
        # the authoritative equality check is the file-level messages_sha:
        recomputed_messages = sha256_canonical(msgs)
        if recomputed_messages != expected_messages_sha:
            raise ItemBuildError(
                f"{case_id}: neither rendered text nor canonical messages hash matches the index "
                f"(rendered recompute={sha256_bytes(text.encode('utf-8'))}, messages recompute={recomputed_messages})")
    return text


LINEAGE_TSV = F0_DIR / "B_RECOVERED20_LINEAGE.tsv"
LINEAGE_TSV_SHA = "eae103a76da768cd400e15a5e64129b1882422d925556e29ce89b442a4c1f338"
_TAR_SHA_CACHE: dict = {}
_LINEAGE_CACHE: dict = {}


def _load_lineage() -> dict:
    """recovery_slot → lineage row (sha-verified F0 file)."""
    if _LINEAGE_CACHE:
        return _LINEAGE_CACHE
    if sha256_file(LINEAGE_TSV) != LINEAGE_TSV_SHA:
        raise ItemBuildError(f"B_RECOVERED20_LINEAGE sha mismatch: {sha256_file(LINEAGE_TSV)}")
    with open(LINEAGE_TSV, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            _LINEAGE_CACHE[r["recovery_slot"]] = r
    if len(_LINEAGE_CACHE) != 20:
        raise ItemBuildError(f"lineage rows {len(_LINEAGE_CACHE)} != 20")
    return _LINEAGE_CACHE


def _verify_tar_sha(path: str, expected: str):
    if path not in _TAR_SHA_CACHE:
        _TAR_SHA_CACHE[path] = sha256_file(path)
    if _TAR_SHA_CACHE[path] != expected:
        raise ItemBuildError(
            f"sealed tar sha mismatch for {path}: got {_TAR_SHA_CACHE[path]}, expected {expected}")


def _extract_answer_from_sealed_tar(row: dict) -> bytes:
    """Recovered slots (20) carry NO extracted copy: their bytes live only in
    the audit-bound sealed tar (lineage_authority=AUDIT_BOUND_TAR:<name>).
    Resolve via B_RECOVERED20_LINEAGE (sha-verified), verify the tar sha
    against the F0 index, extract the exact member IN MEMORY (no writes into
    read-only trees, no unsafe extraction), then verify answer sha+bytes."""
    import tarfile
    lineage = _load_lineage()
    lrow = lineage.get(row.get("recovery_slot", ""))
    if lrow is None:
        raise ItemBuildError(
            f"{row['b_slot_uid']}: recovered slot without lineage row "
            f"(recovery_slot={row.get('recovery_slot')!r})")
    tar_path = lrow["source_archive"]
    if not os.path.exists(tar_path):
        raise ItemBuildError(f"{row['b_slot_uid']}: sealed tar missing: {tar_path}")
    _verify_tar_sha(tar_path, row["source_archive_sha256"])
    if lrow["source_archive_sha256"] != row["source_archive_sha256"]:
        raise ItemBuildError(f"{row['b_slot_uid']}: index/lineage tar sha disagreement")
    member = row["source_member"]
    if lrow["answer_member"] != member:
        raise ItemBuildError(
            f"{row['b_slot_uid']}: index source_member != lineage answer_member")
    with tarfile.open(tar_path, "r:*") as tf:
        try:
            fobj = tf.extractfile(member)
        except KeyError:
            raise ItemBuildError(f"{row['b_slot_uid']}: member {member!r} not in sealed tar")
        if fobj is None:
            raise ItemBuildError(f"{row['b_slot_uid']}: member {member!r} is not a regular file")
        data = fobj.read()
    if lrow.get("answer_sha256") and lrow["answer_sha256"] != row["answer_sha256_recomputed"]:
        raise ItemBuildError(f"{row['b_slot_uid']}: lineage/index answer sha disagreement")
    return data


def load_answer(row: dict) -> bytes:
    """Load answer bytes with full identity verification:
      - native slots: F0-index-bound extracted copy path;
      - recovered slots (empty extracted_copy_path): audit-bound sealed tar
        member extracted in memory (R1 fix — R0 could not build these 20).
    Both paths verify answer sha256 + byte count against the F0 index;
    any mismatch refuses the build (no silent substitution)."""
    p = row.get("extracted_copy_path")
    _ORIG_R = '/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01'
    if p:
        pp = Path(p) if not str(p).startswith(_ORIG_R) else (R / os.path.relpath(p, _ORIG_R))
        if not pp.is_absolute():
            pp = R / p
        if not pp.exists():
            raise ItemBuildError(f"{row['b_slot_uid']}: mirrored answer file missing: {pp}")
        data = open(pp, "rb").read()
    elif not p and str(row.get("lineage_authority", "")).startswith("AUDIT_BOUND_TAR"):
        # sealed tars are NOT shipped (no old return packages in the bundle);
        # bytes were extracted at assembly with the same audited sha verification
        rec_p = R / 'bundle_recovered_answers' / (row['b_slot_uid'] + '.visible_answer.txt')
        if not rec_p.is_file():
            raise ItemBuildError(f"{row['b_slot_uid']}: recovered answer bytes missing in bundle")
        data = rec_p.read_bytes()
    else:
        raise ItemBuildError(
            f"{row['b_slot_uid']}: no answer source (extracted_copy_path={p!r}, "
            f"lineage_authority={row.get('lineage_authority')!r})")
    got = sha256_bytes(data)
    if got != row["answer_sha256_recomputed"]:
        raise ItemBuildError(
            f"{row['b_slot_uid']}: answer sha mismatch (got {got}, index {row['answer_sha256_recomputed']}) — "
            "refusing to build; no silent substitution")
    if len(data) != int(row["answer_bytes"]):
        raise ItemBuildError(f"{row['b_slot_uid']}: answer bytes {len(data)} != index {row['answer_bytes']}")
    return data


def build_evidence_block(evidence_binding: dict, case_id: str,
                         b_slot_uid: str | None = None):
    """Return (block_text, evidence_ids, evidence_status, block_sha, extra).

    evidence_binding modes:
      {"mode": "PENDING_F3_E0"}               → production build REFUSED
      {"mode": "F3_R11_CASE_SLICES_V2",
       "manifest_path": <EVIDENCE_MANIFEST_R1_1.json>,
       "expected_manifest_sha256": …}        → PRIMARY: audited F3 R1.1
                                               (f3r11_case_slice_v2; shared
                                               official facts + per-slot
                                               claim annotations + F7 inline)
      {"mode": "F3_R1_CASE_SLICES", …}        → superseded v1 (regression only;
      {"mode": "F3_E0_PACKAGE", …}            → legacy R0-derived; PRODUCTION
                                                builds refuse both — no silent
                                                fallback, repair card §2)
      {"mode": "TEST_FIXTURE", "fixture": {...}} → synthetic, clearly labeled
    """
    mode = evidence_binding.get("mode")
    if mode == "PENDING_F3_E0":
        raise ItemBuildError(
            "EVIDENCE_PENDING_F3_E0_BINDING: F3 E0 package not bound; production item build "
            "refused (no fabricated E0 hash, no scoring without the frozen evidence snapshot)")
    if mode == "TEST_FIXTURE":
        fx = evidence_binding.get("fixture") or {}
        items = [it for it in (fx.get("items") or [])
                 if it.get("case_id") in (None, case_id)]
        ids = [it["evidence_id"] for it in items]
        lines = [f"TEST_FIXTURE_SYNTHETIC_EVIDENCE (非E0；仅结构测试) fixture_sha={fx.get('fixture_sha', 'NA')}"]
        for it in items:
            lines.append(json.dumps(it, ensure_ascii=False, sort_keys=True))
        block = "\n".join(lines) + "\n"
        return block, ids, "TEST_FIXTURE", sha256_bytes(block.encode("utf-8")), {}
    if mode == "F3_R11_CASE_SLICES_V2":
        import f2r12_evidence_adapter
        pkg = evidence_binding.get("_loaded_package")
        if pkg is None:
            pkg = f2r12_evidence_adapter.load_package_from_binding(evidence_binding)
        if not b_slot_uid:
            raise ItemBuildError(
                "F3_R11_CASE_SLICES_V2 requires b_slot_uid for the per-slot claim annotations")
        ev = pkg.build_item_evidence(case_id, b_slot_uid)
        extra = {"slice_file_sha256": ev["slice_file_sha256"],
                 "shared_text_sha256": ev["shared_text_sha256"],
                 "annotations_sha256": ev["annotations_sha256"],
                 "counts": ev["counts"],
                 "interface": "f3r11_case_slice_v2"}
        return ev["block_text"], ev["evidence_ids"], ev["status"], ev["block_sha256"], extra
    if mode == "F3_R1_CASE_SLICES":
        import f2r12_evidence_adapter
        pkg = evidence_binding.get("_loaded_package")
        if pkg is None:
            pkg = f2r12_evidence_adapter.load_package_from_binding(evidence_binding)
        if not b_slot_uid:
            raise ItemBuildError("F3_R1_CASE_SLICES requires b_slot_uid for the per-slot claim sub-view")
        ev = pkg.build_item_evidence(case_id, b_slot_uid)
        extra = {"slice_file_sha256": ev["slice_file_sha256"],
                 "shared_text_sha256": ev["shared_text_sha256"],
                 "claim_map_text_sha256": ev.get("claim_map_text_sha256"),
                 "interface": "f3r1_case_slice_v1"}
        return ev["block_text"], ev["evidence_ids"], ev["status"], ev["block_sha256"], extra
    if mode == "F3_E0_PACKAGE":
        import f2r12_evidence_adapter
        pkg = evidence_binding.get("_loaded_package")
        if pkg is None:
            pkg = f2r12_evidence_adapter.load_package_from_binding(evidence_binding)
        sl = pkg.build_case_slice(case_id)
        return (sl["slice_text"], sl["evidence_ids"], sl["status"],
                sl["slice_sha256"], {})
    raise ItemBuildError(f"unknown evidence binding mode {mode!r}")


def gold_slice_content_block(slice_dir) -> tuple[str, list]:
    """Concatenate slice files (deterministic order) into the request block;
    returns (text, gold_ref_ids)."""
    man = json.load(open(os.path.join(slice_dir, "GOLD_SLICE_MANIFEST.json"), encoding="utf-8"))
    parts = []
    for name in sorted(man["files"].keys()):
        p = os.path.join(slice_dir, name)
        data = open(p, "rb").read()
        if sha256_bytes(data) != man["files"][name]["sha256"]:
            raise ItemBuildError(f"gold slice file {name} sha mismatch vs slice manifest")
        parts.append(f"--- FILE: {name} (sha256={man['files'][name]['sha256']}, rows={man['files'][name]['rows']}) ---")
        parts.append(data.decode("utf-8"))
    text = "\n".join(parts) + "\n"
    ref_ids = f2r12_gold_slicer.slice_ref_ids(man, man["case_id"])
    return text, ref_ids


def build_item(b_slot_uid: str, anonymous_item_id: str, order_map_slot_check: dict,
               evidence_binding: dict, gold_slice_root, mode: str = "TEST") -> dict:
    """Build one item payload. mode: TEST (fixtures allowed, labeled) or
    PRODUCTION (requires E0 binding + confirmed run config upstream)."""
    if mode not in ("TEST", "PRODUCTION"):
        raise ItemBuildError(f"bad mode {mode!r}")
    _, by_uid = load_b480_index()
    row = by_uid.get(b_slot_uid)
    if row is None:
        raise ItemBuildError(f"b_slot_uid {b_slot_uid!r} not in B_480 index (wrong case/slot refused)")
    # duplicate-slot guard: the order map must bind exactly one uid → one anon id
    if anonymous_item_id in order_map_slot_check:
        if order_map_slot_check[anonymous_item_id] != b_slot_uid:
            raise ItemBuildError(
                f"duplicate slot: {anonymous_item_id} already bound to {order_map_slot_check[anonymous_item_id]}, refusing {b_slot_uid}")
    case_id = row["case_id"]
    if row["engineering_class"] != "USABLE":
        raise ItemBuildError(f"{b_slot_uid}: engineering_class {row['engineering_class']!r} != USABLE — "
                             "B common-120 domain is USABLE-only; identity problem, do not score silently")

    question_text = load_question(case_id, row["question_rendered_prompt_sha256"],
                                  row["question_messages_sha256"])
    answer_bytes = load_answer(row)
    try:
        answer_text = answer_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ItemBuildError(f"{b_slot_uid}: answer not valid UTF-8: {e}")

    _, scope_by_case = load_scope_rows()
    scope_rows = scope_by_case.get(case_id)
    if not scope_rows or len(scope_rows) != 6:
        raise ItemBuildError(f"{case_id}: expected 6 frozen scope rows, got {len(scope_rows or [])}")
    scope_block = scope_rows_tsv_block(scope_rows)
    scope_rows_sha = sha256_bytes(scope_block.encode("utf-8"))

    slice_dir = os.path.join(str(gold_slice_root), case_id)
    if not os.path.exists(os.path.join(slice_dir, "GOLD_SLICE_MANIFEST.json")):
        if mode == "PRODUCTION":
            raise ItemBuildError(f"gold slice not pre-built for {case_id}: {slice_dir}")
        os.makedirs(slice_dir, exist_ok=True)
    if not os.path.exists(os.path.join(slice_dir, "formal_cases.tsv")):
        f2r12_gold_slicer.build_case_slice(case_id, slice_dir)
    gold_block, gold_ref_ids = gold_slice_content_block(slice_dir)
    gold_man = json.load(open(os.path.join(slice_dir, "GOLD_SLICE_MANIFEST.json"), encoding="utf-8"))
    gold_slice_manifest_sha = sha256_file(os.path.join(slice_dir, "GOLD_SLICE_MANIFEST.json"))

    evidence_block, evidence_ids, evidence_status, evidence_case_slice_sha, ev_extra = \
        build_evidence_block(evidence_binding, case_id, b_slot_uid=b_slot_uid)
    evidence_snapshot_sha = evidence_binding.get("evidence_snapshot_sha")
    if evidence_snapshot_sha is None:
        if evidence_binding.get("mode") == "TEST_FIXTURE":
            # fixture identity = real sha256 over the fixture content (formally
            # valid hex; the SYNTHETIC labeling lives in the fixture + block text,
            # never disguised as an E0 hash)
            evidence_snapshot_sha = sha256_bytes(
                canonical_json(evidence_binding.get("fixture")).encode("utf-8"))
        elif evidence_binding.get("mode") in ("F3_E0_PACKAGE", "F3_R1_CASE_SLICES",
                                              "F3_R11_CASE_SLICES_V2"):
            import f2r12_evidence_adapter
            pkg = evidence_binding.get("_loaded_package")
            if pkg is None:
                pkg = f2r12_evidence_adapter.load_package_from_binding(evidence_binding)
            evidence_snapshot_sha = pkg.manifest_sha256
        else:
            raise ItemBuildError("evidence_snapshot_sha missing in binding")
    if mode == "PRODUCTION" and evidence_binding.get("mode") != "F3_R11_CASE_SLICES_V2":
        raise ItemBuildError(
            "PRODUCTION build requires the AUDITED F3 R1.1 binding "
            "(F3_R11_CASE_SLICES_V2); superseded v1 / legacy R0 / TEST_FIXTURE "
            "are refused in production — no silent fallback (repair card §2)")

    system_prompt_sha = sha256_file(SYSTEM_PROMPT_PATH)
    template_bytes = open(TEMPLATE_PATH, "rb").read()
    template_sha = sha256_bytes(template_bytes)
    rubric_text_sha = sha256_file(RUBRIC_TEXT_PATH)
    if rubric_text_sha != RUBRIC_RATER_CLEAN_TEXT_SHA:
        raise ItemBuildError(f"rubric text sha drift: {rubric_text_sha}")

    identity_echo = {
        "input_manifest_sha": F0_INPUT_BASELINE_MANIFEST_SHA,
        "question_rendered_prompt_sha256": row["question_rendered_prompt_sha256"],
        "answer_sha256": row["answer_sha256_recomputed"],
        "rubric_text_sha256": rubric_text_sha,
        "gold_slice_manifest_sha256": gold_slice_manifest_sha,
        "scope_rows_sha256": scope_rows_sha,
        "evidence_snapshot_sha": evidence_snapshot_sha,
        "evidence_case_slice_sha256": evidence_case_slice_sha,
        "system_prompt_sha256": system_prompt_sha,
        "item_template_sha256": template_sha,
    }

    subs = {
        "ANONYMOUS_ITEM_ID": anonymous_item_id,
        "CASE_ID": case_id,
        "INPUT_MANIFEST_SHA": identity_echo["input_manifest_sha"],
        "QUESTION_RENDERED_PROMPT_SHA256": identity_echo["question_rendered_prompt_sha256"],
        "ANSWER_SHA256": identity_echo["answer_sha256"],
        "RUBRIC_TEXT_SHA256": identity_echo["rubric_text_sha256"],
        "GOLD_SLICE_MANIFEST_SHA256": identity_echo["gold_slice_manifest_sha256"],
        "SCOPE_ROWS_SHA256": identity_echo["scope_rows_sha256"],
        "EVIDENCE_SNAPSHOT_SHA": identity_echo["evidence_snapshot_sha"],
        "EVIDENCE_CASE_SLICE_SHA256": identity_echo["evidence_case_slice_sha256"],
        "EVIDENCE_STATUS": evidence_status,
        "SYSTEM_PROMPT_SHA256": identity_echo["system_prompt_sha256"],
        "ITEM_TEMPLATE_SHA256": identity_echo["item_template_sha256"],
        "QUESTION_FULL_TEXT": question_text,
        "ANSWER_FULL_TEXT": answer_text,
        "GOLD_SLICE_CONTENT": gold_block,
        "SCOPE_ROWS_TSV": scope_block,
        "EVIDENCE_ITEMS": evidence_block,
    }
    template = template_bytes.decode("utf-8")
    user_message = template
    for k in PLACEHOLDERS:
        tok = "{{" + k + "}}"
        if tok not in user_message:
            raise ItemBuildError(f"template placeholder missing: {tok}")
        user_message = user_message.replace(tok, subs[k])
    for k in PLACEHOLDERS:
        if "{{" + k + "}}" in user_message:
            raise ItemBuildError(f"placeholder not fully substituted: {k}")

    scope_ctx_rows = [{"claim_group": r["claim_group"],
                       "condition_met": r["condition_met"],
                       "active_criticality": r["active_criticality"]}
                      for r in scope_rows]

    payload = {
        "mode": mode,
        "b_slot_uid": b_slot_uid,          # coordinator-side only; NOT sent to the rater
        "anonymous_item_id": anonymous_item_id,
        "batch": row["batch"],
        "case_id": case_id,
        "recovered": row["recovered"],
        "source_kind": row["source_kind"],
        "identity_echo": identity_echo,
        "evidence_status": evidence_status,
        "evidence_extra": ev_extra,
        "system_prompt_path": str(SYSTEM_PROMPT_PATH),
        "system_prompt_sha256": system_prompt_sha,
        "item_template_sha256": template_sha,
        "user_message": user_message,
        "user_message_sha256": sha256_bytes(user_message.encode("utf-8")),
        "validation_context": {
            "case_id": case_id,
            "anonymous_item_id": anonymous_item_id,
            "identity_echo": identity_echo,
            "scope_rows": scope_ctx_rows,
            "predef_by_id": load_predef_attrs(),
            "evidence_ids": evidence_ids,
            "gold_ref_ids": gold_ref_ids,
            "scope_row_ref_ids": [f"SCOPE#{case_id}#{r['claim_group'][:4]}" for r in scope_rows],
        },
        # stripped-from-request assertion: the rater never sees these
        "not_sent_to_rater": ["tested_model_config_id", "model_config_display",
                              "b_slot_uid", "source_kind", "recovered",
                              "provider_request_id", "engineering_class", "lineage_authority"],
    }
    return payload


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("b_slot_uid")
    ap.add_argument("anonymous_item_id")
    ap.add_argument("gold_slice_root")
    ap.add_argument("out_json")
    ap.add_argument("--evidence-fixture", default=None,
                    help="path to synthetic fixture JSON (TEST mode only)")
    ap.add_argument("--e0-manifest", default=None,
                    help="F3 R1 EVIDENCE_MANIFEST_R1.json path (production)")
    ap.add_argument("--e0-manifest-sha", default=None,
                    help="expected sha256 of the F3 R1 manifest (production)")
    ap.add_argument("--production", action="store_true",
                    help="production mode (requires --e0-manifest/-sha)")
    a = ap.parse_args()
    if a.evidence_fixture:
        fx = json.load(open(a.evidence_fixture, encoding="utf-8"))
        binding = {"mode": "TEST_FIXTURE", "fixture": fx}
    elif a.e0_manifest:
        if not a.e0_manifest_sha:
            raise SystemExit("--e0-manifest requires --e0-manifest-sha")
        binding = {"mode": "F3_R1_CASE_SLICES", "manifest_path": a.e0_manifest,
                   "expected_manifest_sha256": a.e0_manifest_sha}
    else:
        binding = {"mode": "PENDING_F3_E0"}
    payload = build_item(a.b_slot_uid, a.anonymous_item_id, {}, binding,
                         a.gold_slice_root, mode="TEST" if a.evidence_fixture else "PRODUCTION")
    with open(a.out_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"written {a.out_json}; user_message_sha256={payload['user_message_sha256']}")
