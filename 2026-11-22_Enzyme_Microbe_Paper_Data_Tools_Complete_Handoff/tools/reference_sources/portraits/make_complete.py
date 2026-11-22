#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.add_argument("--accession", required=True)
parser.add_argument("--report", required=True)
args = parser.parse_args()
root = Path(args.root)
validation = json.loads(Path(args.report).read_text())
files = sorted(path for path in root.rglob("*") if path.is_file() and path.name != "COMPLETE.json")
complete = {"accession": args.accession, "all_pass": validation.get("all_pass") is True,
            "validation": validation, "file_count": len(files),
            "files": [{"path": str(path.relative_to(root)), "bytes": path.stat().st_size,
                       "sha256": sha(path)} for path in files]}
(root / "COMPLETE.json").write_text(json.dumps(complete, indent=2, sort_keys=True) + "\n")
raise SystemExit(0 if complete["all_pass"] else 1)

