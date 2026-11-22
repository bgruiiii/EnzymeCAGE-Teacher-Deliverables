#!/usr/bin/env python3
import argparse
import csv
import hashlib
import os
from pathlib import Path


def sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def link(source, destination, expected=None, allow_empty=False):
    if not source.is_file() or (not allow_empty and source.stat().st_size == 0):
        raise RuntimeError("missing collate input: %s" % source)
    if expected and sha(source) != expected:
        raise RuntimeError("collate source hash mismatch: %s" % source)
    if destination.exists() or destination.is_symlink():
        raise RuntimeError("duplicate collate destination: %s" % destination)
    destination.symlink_to(source.resolve())


parser = argparse.ArgumentParser()
parser.add_argument("--targets", required=True)
parser.add_argument("--run-root", required=True)
parser.add_argument("--source-run-root", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--traits-info", required=True)
parser.add_argument("--traits-harmonized", required=True)
parser.add_argument("--versions", required=True)
args = parser.parse_args()
with open(args.targets, newline="", encoding="utf-8") as handle:
    targets = list(csv.DictReader(handle, delimiter="\t"))
if len(targets) != 412:
    raise SystemExit("expected 412 targets")
run_root = Path(args.run_root)
source_run_root = Path(args.source_run_root)
output = Path(args.output)
output.mkdir(parents=True, exist_ok=False)
for row in targets:
    acc = row["assembly_accession"]
    genome = acc + "_genomic"
    result = run_root / "results" / acc / genome
    link(Path(row["gtdb_path"]), output / Path(row["gtdb_path"]).name.replace("_genomic", ""), row["gtdb_sha256"])
    if row["speci_path"] != "NA" and row["speci_bytes"] != "0":
        link(Path(row["speci_path"]), output / Path(row["speci_path"]).name.replace("_genomic", ""),
             row["speci_sha256"])
    if row["run_genomespot"] == "true":
        source = source_run_root / "stages" / "genomespot" / acc / (genome + ".genomespot.predictions.tsv")
        link(source, output / (acc + ".genomespot.predictions.tsv"))
    else:
        source = Path(row["genomespot_path"])
        link(source, output / source.name.replace("_genomic", ""), row["genomespot_sha256"])
    for suffix in (".emapper.KEGG_ko.tsv.gz", ".emapper.PFAMs.tsv.gz"):
        link(result / "e2m" / (genome + suffix), output / (acc + suffix))
    for directory, suffixes in (
        ("micropherret", (".MICROPHERRET.binary.tsv.gz", ".MICROPHERRET.prob.tsv.gz")),
        ("bacdive_ai", (".BacDiveAI.binary.tsv.gz", ".BacDiveAI.prob.tsv.gz")),
    ):
        for suffix in suffixes:
            link(result / directory / (genome + suffix), output / (acc + suffix))
    for source in sorted((result / "traitar").glob("*.tsv.gz")):
        link(source, output / source.name.replace("_genomic", ""))
for path in (Path(args.traits_info), Path(args.traits_harmonized), Path(args.versions)):
    link(path, output / path.name)
