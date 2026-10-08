#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""package_g9_closure.py -- build the small G9 closure tar (no giant raws),
its MANIFEST.tsv, SOURCE_AND_SCORER_IDENTITIES.json, and the .identity.txt /
.validation.txt sidecars. Verifies package hygiene (single root, no links/
devices/duplicates/escapes, MANIFEST covers every member) by re-extraction.
"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.abspath(os.path.join(HERE, os.pardir))
EX = os.path.abspath(os.path.join(G9, os.pardir))
BASE = os.path.abspath(os.path.join(EX, os.pardir))
OUTDIR = os.path.join(BASE, "03_HPC_Returned_Result_Summaries")
ROOT = "biosysmodb150_four_model_121_g9_offline_evaluation_20261008"
TAR_NAME = ROOT + ".tar.gz"
TASK_ID = "biosysmodb150_g9_four_model_121_formal_offline_score_20261008"
FINAL_STATUS = "G9_SCORED_PENDING_LOCAL_HUMAN_SHAPE_REVIEW"

CODE_FILES = [
    "build_formal_484_slot_index.py", "score_formal_484.py", "run_sensitivity.py",
    "compute_usage_costs.py", "make_shape_review_sample.py", "export_shape_review.py",
    "validate_g9_formal_scoring.py", "run_mutation_tests.py", "package_g9_closure.py",
]
TOP_FILES = [
    "BIOSYSMODB150_FOUR_MODEL_121_FINAL_EVALUATION_REPORT_20261008.md",
    "FORMAL_484_SLOT_INDEX.tsv", "FORMAL_MERGE_MANIFEST.json",
    "FINAL_VALIDATION.json", "COMMANDS.log",
]
GATE_EVIDENCE = {
    "gate_evidence/G3_VALIDATION_REPORT.json": "work/gate/G3_VALIDATION_REPORT.json",
    "gate_evidence/mock_all_correct.json": "work/gate/mock_all_correct.json",
    "gate_evidence/mock_all_wrong.json": "work/gate/mock_all_wrong.json",
    "gate_evidence/mock_partial.json": "work/gate/mock_partial.json",
    "gate_evidence/mutation_results.json": "work/mutation_results.json",
    "gate_evidence/staged_first3_per_model.json": "work/staged_first3_per_model.json",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # ---- gate hard preconditions ----
    fv = load_json(os.path.join(G9, "FINAL_VALIDATION.json"))
    assert fv["overall"] == "PASS" and fv["total_failures"] == 0, "FINAL_VALIDATION not PASS"
    mut = load_json(os.path.join(G9, "work", "mutation_results.json"))
    assert mut["all_mutations_detected"] is True, "mutation battery not all detected"
    srm = load_json(os.path.join(G9, "scores", "SCORING_RUN_MANIFEST.json"))
    assert srm["failures"] == 0 and srm["counts"]["rows_scored"] == 484

    # ---- gate_evidence assembly (copies of small work artifacts) ----
    for dst, src in GATE_EVIDENCE.items():
        d = os.path.join(G9, dst)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(os.path.join(G9, src), d)

    # ---- SOURCE_AND_SCORER_IDENTITIES.json ----
    ident = {
        "task_id": TASK_ID,
        "generated_utc": now,
        "api_calls": 0,
        "final_status": FINAL_STATUS,
        "source_packages": {
            "three_model": {
                "tar_name": "biosysmodb150_g6r3_glm_low_then_g8p1_three_model_return_20261007T015420Z.tar.gz",
                "locator": os.path.join(BASE, "03_HPC_Returned_Result_Summaries",
                    "biosysmodb150_g6r3_glm_low_then_g8p1_three_model_return_20261007T015420Z.tar.gz"),
                "bytes": 95804898,
                "sha256": "76a45fac8b54a3e5b6be549245cd7927233f4adbd9082766a886bf6bdf68b8ec",
                "local_audit": {
                    "locator": os.path.join(BASE, "04_Local_Review_Audits",
                        "BIOSYSMODB150_G6R3_GLM_LOW_G8P1_THREE_MODEL_FORMAL_RETURN_LOCAL_AUDIT_20261007.md"),
                    "sha256": "4ede4adafe84901d322151e2500a246e0cb99a49f30c9f784658e5741305e3a6"},
                "extracted_under": "G9/source/three_model (NOT included in this closure tar)",
                "internal_sha256sums": "top 4458/4458 PASS + audit 521/521 PASS",
            },
            "kimi": {
                "tar_name": "biosysmodb150_g8p2_kimi_k3_121_formal_return_20261007T141621Z.tar.gz",
                "locator": os.path.join(BASE, "03_HPC_Returned_Result_Summaries",
                    "biosysmodb150_g8p2_kimi_k3_121_formal_return_20261007T141621Z.tar.gz"),
                "bytes": 117802093,
                "sha256": "e17504af6c2927e9ba37c9f31eb0ec75aa346bfdc1ac28badd213fbcdf31e34c",
                "local_audit": {
                    "locator": os.path.join(BASE, "04_Local_Review_Audits",
                        "BIOSYSMODB150_G8P2_KIMI_K3_121_FORMAL_RETURN_LOCAL_AUDIT_20261008.md"),
                    "sha256": "4fbc0a029d551689c4e4d6c8986f785492d4fe85a40b1b366cac5915c758544e"},
                "extracted_under": "G9/source/kimi (NOT included in this closure tar)",
                "internal_sha256sums": "top 1638/1638 PASS + audit 268/268 PASS",
            },
        },
        "authority_closure": {
            "locator": os.path.join(BASE, "00_Authority_Teacher_Plan",
                "BIOSYSMODB150_FOUR_MODEL_121_FORMAL_API_COLLECTION_CLOSURE_20261008.md"),
            "sha256": "73314ebc41af42225f32aab2b2d7bb69b85c8b7d8a6efaed124e66b176da42bd",
        },
        "embedded_input_package_sha256":
            "48a7e6835fe65994c14b293f4d4ead36aa616835c8727a82abc3f84c559fb222",
        "frozen_scorer": {
            "g1_gold_manifest": "c424763cd4c38fcaac1b178979efb3f18f2b77039369ab6b8c709eab42dce06e",
            "g2_questions_manifest": "ae5780e546bb259d0133ba63157ecfe2f3d3071fc37fc2c0050629f7fe575520",
            "g3_gate": "32c155201a360db8de229e40a9d9cb14bd152993fd0356fd8b0eb8c9001ccaa2",
            "g3_manifest": "24f1004cab0afca4707bbbd34f26f4b7ead074da723651af73f1fe95ad562e8a",
            "scorer_py": "a326eee63258cd0a2706bfd8a1dc6907d6f9fc6aa24b101a7192312c6ed39c61",
            "score_recipe_md": "8b79daf906f04e31589ad77bd93998f9a12649575bd4d476447c43028c338392",
            "validators_py": "c302164433e37127854eefdf25c44a5939201375873833d51846c3c127083899",
            "teacher_approval": {
                "locator": os.path.join(BASE, "00_Authority_Teacher_Plan",
                    "TEACHER_REPLY_BIOSYSMODB150_G2_G3_SIGNOFF_2026-09-28(1).md"),
                "sha256": "1fa908f5ff1caad1f0cb475e820309f0b6431be4e613d51a8548088399c1a5d0"},
            "rdkit": "2026.03.5",
            "gate_rerun": "validator 162/162 PASS; mocks science 100.0/0.0/77.36 (gate_evidence/)",
        },
        "ledgers_authoritative": {
            "global_calls.json": {
                "sha256": sha256_file(os.path.join(G9, "source", "three_model",
                                                   "ledger", "global_calls.json")),
                "total_committed": 377, "spent_cny_est": 184.780276},
            "kimi_calls.json": {
                "sha256": sha256_file(os.path.join(G9, "source", "kimi",
                                                   "ledger", "kimi_calls.json")),
                "total_committed": 121, "spent_cny_est": 435.86014},
            "ignored": [".tmp", ".lock", ".runner.lock runtime files"],
        },
        "formal_cost_recomputed_cny": load_json(os.path.join(
            G9, "scores", "usage_cost_summary.json"))["formal_grand_total_cny"],
        "validation": {
            "FINAL_VALIDATION": {"overall": fv["overall"],
                                 "total_checks": fv["total_checks"],
                                 "total_failures": fv["total_failures"]},
            "mutation_battery": "7/7 detected + control PASS",
        },
        "code": {f: sha256_file(os.path.join(HERE, f)) for f in CODE_FILES},
    }

    # ---- staging tree (regular files only) ----
    stage = os.path.join(G9, "work", "_package_stage")
    if os.path.exists(stage):
        shutil.rmtree(stage)
    rootdir = os.path.join(stage, ROOT)
    os.makedirs(rootdir)

    def add(rel, src):
        dst = os.path.join(rootdir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)

    for f in TOP_FILES:
        add(f, os.path.join(G9, f))
    for f in sorted(os.listdir(os.path.join(G9, "scores"))):
        add("scores/" + f, os.path.join(G9, "scores", f))
    for f in ("sampling_manifest.json", "checklist.tsv", "SHA256SUMS",
              "README.md", "AI_PRE_REVIEW.md"):
        add("shape_review/" + f, os.path.join(G9, "shape_review", f))
    for f in sorted(os.listdir(os.path.join(G9, "shape_review", "samples"))):
        add("shape_review/samples/" + f,
            os.path.join(G9, "shape_review", "samples", f))
    for f in CODE_FILES:
        add("code/" + f, os.path.join(HERE, f))
    for dst in sorted(GATE_EVIDENCE):
        add(dst, os.path.join(G9, dst))

    # identities file written into both stage and G9
    ident_text = json.dumps(ident, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    for p in (os.path.join(rootdir, "SOURCE_AND_SCORER_IDENTITIES.json"),
              os.path.join(G9, "SOURCE_AND_SCORER_IDENTITIES.json")):
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(ident_text)

    # ---- MANIFEST.tsv over all members except itself ----
    members = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, rootdir).replace(os.sep, "/")
            members.append((rel, full))
    members.sort()
    manifest_lines = ["sha256\tbytes\tpath"]
    for rel, full in members:
        manifest_lines.append("%s\t%d\t%s" % (sha256_file(full),
                                              os.path.getsize(full), rel))
    manifest_text = "\n".join(manifest_lines) + "\n"
    with open(os.path.join(rootdir, "MANIFEST.tsv"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(manifest_text)
    with open(os.path.join(G9, "MANIFEST.tsv"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(manifest_text)

    # ---- tar ----
    tar_path = os.path.join(OUTDIR, TAR_NAME)
    for p in (tar_path, tar_path.replace(".tar.gz", ".identity.txt"),
              tar_path.replace(".tar.gz", ".validation.txt")):
        assert not os.path.exists(p), "refusing to overwrite %s" % p
    env = dict(os.environ, LC_ALL="C")
    subprocess.run(
        ["tar", "--create", "--gzip", "--file", tar_path,
         "--owner=0", "--group=0", "--numeric-owner",
         "--mtime=2026-10-08 00:00:00 UTC",
         "--sort=name", "--format=gnu",
         "-C", stage, ROOT], check=True, env=env)
    nbytes = os.path.getsize(tar_path)
    digest = sha256_file(tar_path)

    # ---- hygiene + coverage verification by re-extraction ----
    with tarfile.open(tar_path, "r:gz") as tf:
        infos = tf.getmembers()
        names = [i.name for i in infos]
        assert len(names) == len(set(names)), "duplicate members"
        for i in infos:
            assert not i.name.startswith("/"), "absolute path member"
            assert ".." not in i.name.split("/"), "dotdot member"
            assert i.name == ROOT or i.name.startswith(ROOT + "/"), "root escape"
            assert i.isreg() or i.isdir(), "non-regular member %s" % i.name
            assert not (i.islnk() or i.issym()), "link member"
        roots = {n.split("/")[0] for n in names}
        assert roots == {ROOT}, "multiple roots %s" % roots
        extract_to = os.path.join(G9, "work", "_package_verify")
        if os.path.exists(extract_to):
            shutil.rmtree(extract_to)
        os.makedirs(extract_to)
        tf.extractall(extract_to)
    man = {}
    with open(os.path.join(extract_to, ROOT, "MANIFEST.tsv"), encoding="utf-8",
              newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            man[row["path"]] = (row["sha256"], int(row["bytes"]))
    extracted = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(extract_to, ROOT)):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, os.path.join(extract_to, ROOT)).replace(os.sep, "/")
            extracted.append(rel)
    missing = sorted(set(man) - set(extracted))
    uncovered = sorted(set(extracted) - set(man) - {"MANIFEST.tsv"})
    assert not missing, "manifest lists missing members %s" % missing[:5]
    assert not uncovered, "members not covered by manifest %s" % uncovered[:5]
    for rel, (sha, sz) in man.items():
        full = os.path.join(extract_to, ROOT, rel)
        assert os.path.getsize(full) == sz, rel
        assert sha256_file(full) == sha, rel
    n_members = len(extracted)
    shutil.rmtree(extract_to, ignore_errors=True)
    shutil.rmtree(stage, ignore_errors=True)

    # ---- sidecars ----
    with open(tar_path.replace(".tar.gz", ".identity.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write("file=%s\n" % TAR_NAME)
        fh.write("locator=%s\n" % tar_path)
        fh.write("bytes=%d\n" % nbytes)
        fh.write("sha256=%s\n" % digest)
        fh.write("root=%s\n" % ROOT)
        fh.write("members=%d\n" % n_members)
        fh.write("created_utc=%s\n" % now)
        fh.write("task_id=%s\n" % TASK_ID)
        fh.write("api_calls=0\n")
        fh.write("contains=merge index + scores + sensitivity + usage/cost + "
                 "shape review materials + code + report + gate evidence + "
                 "identities + manifest (NO giant source raws)\n")
        fh.write("source_three_model_sha256=%s\n"
                 % ident["source_packages"]["three_model"]["sha256"])
        fh.write("source_kimi_sha256=%s\n"
                 % ident["source_packages"]["kimi"]["sha256"])
    with open(tar_path.replace(".tar.gz", ".validation.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write("FINAL_STATUS=%s\n" % FINAL_STATUS)
        fh.write("API_CALLS=0\n")
        fh.write("SLOTS=484 committed / 482 terminal / 469 usable / "
                 "13 content failures / 2 held / 0 not-dispatched / 0 retries\n")
        fh.write("FINAL_VALIDATION=PASS (%d checks, 0 failures)\n"
                 % fv["total_checks"])
        fh.write("MUTATION_BATTERY=7/7 detected + control PASS\n")
        fh.write("G3_FROZEN_GATE=162/162 PASS; mocks 100.0/0.0/77.36\n")
        fh.write("SENSITIVITY=STABLE_ALL_10_VARIANTS (0/40 rank changes)\n")
        fh.write("PRIMARY_SCIENCE_MACRO_121=kimi/kimi-k3 17.9131 > "
                 "deepseek-v4.1-flash 12.2099 > qwen3.8-max 11.9753 > "
                 "ZHIPU/GLM-5.3 8.7215\n")
        fh.write("FORMAL_COST_RECOMPUTED_CNY=%.4f\n"
                 % ident["formal_cost_recomputed_cny"])
        fh.write("HUMAN_SHAPE_REVIEW=PENDING_LOCAL_HUMAN_REVIEW (8 samples)\n")
        fh.write("package_hygiene=single root; %d members; no absolute/../"
                 "link/device/duplicate; MANIFEST covers all members except "
                 "itself; re-extraction byte-verified\n" % n_members)
        fh.write("generated_utc=%s\n" % now)

    print("PACKAGE OK: %s" % tar_path)
    print("bytes=%d sha256=%s members=%d" % (nbytes, digest, n_members))
    return 0


if __name__ == "__main__":
    sys.exit(main())
