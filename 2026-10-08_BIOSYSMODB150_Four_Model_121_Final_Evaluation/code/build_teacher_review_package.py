#!/usr/bin/env python3
"""Build and validate the versioned BIOSYSMOdb150 teacher-review package."""
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
RUN_ROOT = os.path.abspath(os.path.join(ROOT, os.pardir, os.pardir))
OUT = os.path.join(RUN_ROOT, "03_HPC_Returned_Result_Summaries")
NAME = "biosysmodb150_four_model_121_teacher_review_20261008"
TAR = os.path.join(OUT, NAME + ".tar.gz")
IDENTITY = os.path.join(OUT, NAME + ".identity.txt")
VALIDATION = os.path.join(OUT, NAME + ".validation.txt")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def files_under(root):
    out = []
    for dp, dns, fns in os.walk(root):
        dns[:] = sorted(d for d in dns if d != "__pycache__")
        for fn in sorted(fns):
            if fn.endswith(".pyc"):
                continue
            out.append(os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, "/"))
    return out


def require(rel):
    p = os.path.join(ROOT, rel)
    assert os.path.isfile(p), "missing required file: " + rel
    return p


def main():
    required = [
        "README.md", "PACKAGE_STATUS.txt",
        "BIOSYSMODB150_FOUR_MODEL_121_FINAL_FEEDBACK_TO_HUANG_20261008.md",
        "PROTOCOL_DEVIATIONS_AND_TEACHER_ADJUDICATION_REQUEST_20261008.md",
        "HUANG_TEACHER_REQUIREMENT_COMPLIANCE_MATRIX_20261008.md",
        "reports/BIOSYSMODB150_FOUR_MODEL_121_FINAL_EVALUATION_REPORT_20261008.md",
        "reports/BIOSYSMODB150_G9_FOUR_MODEL_121_OFFLINE_EVALUATION_LOCAL_AUDIT_20261008.md",
        "shape_review/HUMAN_SHAPE_REVIEW_RECORD_20261008.md",
        "tables/per_model_summary.tsv", "tables/per_case_scores.tsv",
        "tables/failure_registry.tsv", "tables/sensitivity_results.tsv",
        "tables/FORMAL_484_SLOT_INDEX.tsv", "validation/FINAL_VALIDATION.json",
    ]
    for rel in required:
        require(rel)

    status = open(require("PACKAGE_STATUS.txt"), encoding="utf-8").read()
    assert "HUMAN_SHAPE_REVIEW=PASS_8_OF_8" in status
    assert "TEACHER_ADJUDICATION_REQUIRED=true" in status
    report = open(require("reports/BIOSYSMODB150_FOUR_MODEL_121_FINAL_EVALUATION_REPORT_20261008.md"),
                  encoding="utf-8").read()
    assert "G9_FINAL_READY_FOR_TEACHER_REVIEW" in report
    assert "PARTIAL_WITH_DISCLOSED_DEVIATIONS" in report
    assert "抽样在全量评分后执行" in report
    assert "PENDING_LOCAL_HUMAN_SHAPE_REVIEW" not in report

    fv = json.load(open(require("validation/FINAL_VALIDATION.json"), encoding="utf-8"))
    assert fv["overall"] == "PASS" and fv["total_checks"] == 8974
    rows = list(csv.DictReader(open(require("tables/per_case_scores.tsv"), encoding="utf-8"), delimiter="\t"))
    assert len(rows) == 484
    assert len({(r["case_id"], r["model_exact_id"]) for r in rows}) == 484
    assert sum(r["engineering_class"] == "USABLE" for r in rows) == 469

    # Refresh shape hashes after correcting provenance wording and adding human record.
    shape_members = [
        "shape_review/sampling_manifest.json", "shape_review/checklist.tsv",
        "shape_review/AI_PRE_REVIEW.md", "shape_review/HUMAN_SHAPE_REVIEW_RECORD_20261008.md",
    ] + [r for r in files_under(ROOT) if r.startswith("shape_review/samples/")]
    shape_lines = ["%s  %s" % (sha(os.path.join(ROOT, r)), r.split("shape_review/", 1)[1])
                   for r in sorted(shape_members)]
    with open(os.path.join(ROOT, "shape_review", "SHA256SUMS"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(shape_lines) + "\n")

    # No giant raw/source extracts, credentials, secrets, or accidental git metadata.
    all_files = files_under(ROOT)
    assert not any(r.startswith("source/") for r in all_files)
    assert not any("/.git/" in ("/" + r + "/") or r.startswith(".git/") for r in all_files)
    assert max(os.path.getsize(os.path.join(ROOT, r)) for r in all_files) < 5 * 1024 * 1024
    secret = re.compile(rb"(?:sk-[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9_.-]{16,}|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY)")
    hits = []
    for rel in all_files:
        data = open(os.path.join(ROOT, rel), "rb").read()
        if secret.search(data):
            hits.append(rel)
    assert not hits, "secret-like content: %r" % hits

    validation = {
        "status": "PASS_READY_FOR_TEACHER_REVIEW_WITH_DISCLOSED_PROTOCOL_DEVIATIONS",
        "api_calls": 0,
        "files": len(all_files),
        "formal_slots": 484,
        "usable": 469,
        "content_failures": 13,
        "held": 2,
        "human_shape_review": "PASS_8_OF_8",
        "numeric_validation": "8974/8974_PASS",
        "mutation_battery": "7/7_DETECTED_PLUS_CONTROL_PASS",
        "teacher_adjudication_required": True,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(os.path.join(ROOT, "TEACHER_PACKAGE_VALIDATION.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(validation, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")

    excluded = {"PACKAGE_FILE_MANIFEST.tsv", "PACKAGE_SHA256SUMS.txt"}
    payload = [r for r in files_under(ROOT) if r not in excluded]
    manifest = ["sha256\tbytes\tpath"]
    sums = []
    for rel in payload:
        p = os.path.join(ROOT, rel)
        dg = sha(p)
        manifest.append("%s\t%d\t%s" % (dg, os.path.getsize(p), rel))
        sums.append("%s  %s" % (dg, rel))
    with open(os.path.join(ROOT, "PACKAGE_FILE_MANIFEST.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(manifest) + "\n")
    with open(os.path.join(ROOT, "PACKAGE_SHA256SUMS.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(sums) + "\n")

    for p in (TAR, IDENTITY, VALIDATION):
        assert not os.path.exists(p), "refusing overwrite: " + p
    os.makedirs(OUT, exist_ok=True)
    stage = tempfile.mkdtemp(prefix="biosysmodb150_teacher_pkg_")
    staged = os.path.join(stage, NAME)
    shutil.copytree(ROOT, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    with tarfile.open(TAR, "w:gz", format=tarfile.GNU_FORMAT) as tf:
        for rel in [""] + files_under(staged):
            p = staged if not rel else os.path.join(staged, rel)
            arc = NAME if not rel else NAME + "/" + rel
            info = tf.gettarinfo(p, arc)
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 1791417600  # 2026-10-08T00:00:00Z
            if info.isfile():
                with open(p, "rb") as fh:
                    tf.addfile(info, fh)
            else:
                tf.addfile(info)

    with tarfile.open(TAR, "r:gz") as tf:
        infos = tf.getmembers()
        names = [i.name for i in infos]
        assert len(names) == len(set(names))
        assert {n.split("/")[0] for n in names} == {NAME}
        for i in infos:
            assert not i.name.startswith("/") and ".." not in i.name.split("/")
            assert i.isfile() or i.isdir()
            assert not (i.issym() or i.islnk() or i.isdev())
        regular = sum(i.isfile() for i in infos)
        total = len(infos)

    tar_sha = sha(TAR)
    with open(IDENTITY, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("file=%s\nbytes=%d\nsha256=%s\nroot=%s\nregular_files=%d\ntar_members=%d\n"
                 "status=READY_FOR_TEACHER_REVIEW_WITH_DISCLOSED_PROTOCOL_DEVIATIONS\napi_calls=0\n"
                 % (os.path.basename(TAR), os.path.getsize(TAR), tar_sha, NAME, regular, total))
    with open(VALIDATION, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("FINAL_STATUS=READY_FOR_TEACHER_REVIEW_WITH_DISCLOSED_PROTOCOL_DEVIATIONS\n"
                 "API_CALLS=0\nFORMAL=484/482/469/13/2\nHUMAN_SHAPE_REVIEW=PASS_8_OF_8\n"
                 "NUMERIC_VALIDATION=8974/8974_PASS\nMUTATIONS=7/7_DETECTED_PLUS_CONTROL_PASS\n"
                 "TEACHER_ADJUDICATION_REQUIRED=true\nregular_files=%d\ntar_members=%d\n"
                 "package_hygiene=single_root,no_links,no_devices,no_duplicates,no_escape\n"
                 % (regular, total))
    shutil.rmtree(stage)
    print("PACKAGE", TAR)
    print("BYTES", os.path.getsize(TAR))
    print("SHA256", tar_sha)
    print("REGULAR_FILES", regular, "TAR_MEMBERS", total)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("BLOCKED_TEACHER_PACKAGE:", exc, file=sys.stderr)
        raise
