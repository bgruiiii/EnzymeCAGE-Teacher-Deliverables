#!/usr/bin/env python3
import sys


lines = [line.strip() for line in open(sys.argv[1], encoding="ascii") if line.strip()]
position = int(sys.argv[2])
if position < 0 or position >= len(lines):
    raise SystemExit("stage position out of range")
print(lines[position])

