#!/usr/bin/env python3
import csv
import shlex
import sys


with open(sys.argv[1], newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
index = int(sys.argv[2])
if index < 0 or index >= len(rows):
    raise SystemExit("target index out of range")
for key, value in rows[index].items():
    print("%s=%s" % (key.upper(), shlex.quote(value)))

