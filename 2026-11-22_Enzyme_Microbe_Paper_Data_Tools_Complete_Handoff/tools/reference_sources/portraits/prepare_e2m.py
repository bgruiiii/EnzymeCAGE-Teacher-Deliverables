#!/usr/bin/env python3
import argparse
import csv
import gzip
import json
import os
import shutil
from pathlib import Path


def normalize(path, accession):
    with gzip.open(path, "rt", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    if len(rows) != 2 or len(rows[0]) != len(rows[1]) or not rows[0]:
        raise RuntimeError("invalid one-sample matrix: %s" % path)
    allowed = {accession, accession.rsplit(".", 1)[0], accession + "_genomic"}
    if rows[1][0] not in allowed:
        raise RuntimeError("unexpected sample ID in %s: %s" % (path, rows[1][0]))
    rows[1][0] = accession
    temporary = Path(str(path) + ".tmp")
    with gzip.open(temporary, "wt", newline="") as handle:
        csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)
    os.replace(temporary, path)
    return len(rows[0]) - 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--accession", required=True)
    parser.add_argument("--source-ko")
    parser.add_argument("--source-pfam")
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    root = Path(args.directory)
    root.mkdir(parents=True, exist_ok=True)
    if args.source_ko and args.source_pfam:
        shutil.copy2(args.source_ko, root / "emapper.KEGG_ko.tsv.gz")
        shutil.copy2(args.source_pfam, root / "emapper.PFAMs.tsv.gz")
    files = sorted(root.glob("*.tsv.gz"))
    if not files:
        raise RuntimeError("no e2m matrices")
    counts = {path.name: normalize(path, args.accession) for path in files}
    genome = args.accession + "_genomic"
    for basename in ("emapper.KEGG_ko.tsv.gz", "emapper.PFAMs.tsv.gz"):
        source = root / basename
        if not source.is_file():
            raise RuntimeError("missing required matrix: %s" % basename)
        shutil.copy2(source, root / (genome + "." + basename))
    report = {"accession": args.accession, "matrix_files": len(files),
              "feature_counts": counts, "all_pass": True}
    Path(args.report).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
