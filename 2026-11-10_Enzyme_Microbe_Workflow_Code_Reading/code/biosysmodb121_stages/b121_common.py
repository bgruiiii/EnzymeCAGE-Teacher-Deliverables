# -*- coding: utf-8 -*-
"""Shared helpers for BIOSYSMOdb121 B0-B2 stage scripts (CPU-only)."""
import csv, gzip, hashlib, io, json, os, sys, time

WORK = "/usrdata/EnzymeCAGE_data/workspaces/biosysmodb121_step_enzyme_ranking_20260928"
INPUTS = os.path.join(WORK, "inputs", "biosysmodb121_step_enzyme_ranking_inputs_20260928")
DATA_ROOT = "/usrdata/EnzymeCAGE_data"
CODE_ROOT = os.path.join(DATA_ROOT, "EnzymeCAGE-master")
RET = os.path.join(CODE_ROOT, "HPC_Returned_Result_Summaries")
HPC_INPUTS = os.path.join(CODE_ROOT, "HPC_Inputs")
PY = "/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python"

INPUT_TAR = os.path.join(
    HPC_INPUTS, "biosysmodb121_step_enzyme_ranking_inputs_20260928.tar.gz")
INPUT_TAR_BYTES = 28476186
INPUT_TAR_SHA256 = ("f7ff8653bfd9e4be1ce4831a0f4308628719a02a4f8c27bfad59e"
                    "7ef388b569e")


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def file_stat(path):
    st = os.stat(path)
    return st.st_size


def read_tsv(path):
    """utf-8-sig tolerant TSV reader -> list of dict rows (keeps blank cols)."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def read_tsv_header(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f, delimiter="\t")
        return next(r)


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.reader(f))


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")


def write_tsv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([r.get(k, "") for k in header])


def assert_cpu_only():
    if os.environ.get("CUDA_VISIBLE_DEVICES", None) != "":
        die("CUDA_VISIBLE_DEVICES must be set to '' (CPU-only contract)")


def die(msg):
    print("BLOCKED: " + msg, file=sys.stderr)
    sys.exit(3)


def snapshot_tree(root_dirs):
    """path -> [bytes, sha256] for all regular files under given roots."""
    out = {}
    for root in root_dirs:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames.sort()
            for fn in sorted(filenames):
                p = os.path.join(dirpath, fn)
                if os.path.islink(p):
                    out["LINK:" + p] = [0, "SYMLINK"]
                    continue
                out[p] = [os.path.getsize(p), sha256_file(p)]
    return out


def manifest_lines(exclude_paths):
    """MANIFEST.sha256 body lines for a tree rooted at cwd (relative names)."""
    rows = []
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames.sort()
        for fn in sorted(filenames):
            p = os.path.relpath(os.path.join(dirpath, fn), ".")
            if p in exclude_paths or ("./" + p) in exclude_paths:
                continue
            rows.append((p, sha256_file(os.path.join(dirpath, fn))))
    return rows
