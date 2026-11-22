#!/usr/bin/env python3
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True)
parser.add_argument("--targets", required=True)
parser.add_argument("--json", required=True)
args = parser.parse_args()
with open(args.targets, newline="", encoding="utf-8") as handle:
    expected_genomes = {row["assembly_accession"] for row in csv.DictReader(handle, delimiter="\t")}
path = Path(args.file)
with gzip.open(path, "rt", newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
expected = {"genomespot": 10, "MICROPHERRET": 74, "BacDiveAI": 9, "Traitar": 68}
pairs = Counter((row.get("genome"), row.get("tool")) for row in rows)
gates = {
    "rows_66332": len(rows) == 66332,
    "genomes_412_exact": {row.get("genome") for row in rows} == expected_genomes,
    "tools_four_exact": {row.get("tool") for row in rows} == set(expected),
    "pair_counts": all(pairs[(genome, tool)] == count for genome in expected_genomes for tool, count in expected.items()),
    "features_nonempty": bool(rows) and all(row.get("feature") for row in rows),
}
report = {"rows": len(rows), "genomes": len({row.get("genome") for row in rows}),
          "tool_totals": dict(Counter(row.get("tool") for row in rows)),
          "gates": gates, "all_pass": all(gates.values()),
          "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
Path(args.json).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
raise SystemExit(0 if report["all_pass"] else 1)

