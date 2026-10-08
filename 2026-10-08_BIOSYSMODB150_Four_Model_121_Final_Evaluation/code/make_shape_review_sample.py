#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_shape_review_sample.py -- frozen-seed shape-review sampler.

Reads ONLY the sorted 121 case IDs (from frozen G2 main_cases.jsonl); reads NO
answer content whatsoever before the sample is fixed. Algorithm (per execution
card section 6):
    rng = random.Random(20261006)
    for model in [qwen3.8-max, deepseek-v4.1-flash, ZHIPU/GLM-5.3, kimi/kimi-k3]:
        picks[model] = rng.sample(sorted_case_ids, 2)   # without replacement
A single rng instance is used sequentially across the four models. If a picked
slot is a failed/held slot the sample is NOT replaced.
Writes shape_review/sampling_manifest.json (python version, algorithm, seed,
model order, picked cases, manifest SHA).
"""
import hashlib
import json
import os
import platform
import random
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.abspath(os.path.join(HERE, os.pardir))
EX = os.path.abspath(os.path.join(G9, os.pardir))

SEED = 20261006
MODEL_ORDER = ["qwen3.8-max", "deepseek-v4.1-flash", "ZHIPU/GLM-5.3", "kimi/kimi-k3"]
ALGORITHM = ("random.Random(20261006); for each model in fixed order: "
             "rng.sample(sorted_121_case_ids, 2) without replacement; "
             "single rng instance sequentially across models; sampled "
             "failed/held slots are never replaced")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    cases = []
    g2 = os.path.join(EX, "G2_questions", "main_cases.jsonl")
    with open(g2, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                cases.append(json.loads(line)["case_id"])
    assert len(cases) == 121 == len(set(cases))
    sorted_cases = sorted(cases)

    rng = random.Random(SEED)
    picks = {}
    for m in MODEL_ORDER:
        picks[m] = rng.sample(sorted_cases, 2)

    out_dir = os.path.join(G9, "shape_review")
    os.makedirs(out_dir, exist_ok=True)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "seed": SEED,
        "algorithm": ALGORITHM,
        "model_order": MODEL_ORDER,
        "case_id_source": {"path": "G2_questions/main_cases.jsonl",
                           "sha256": sha256_file(g2),
                           "n_cases": 121},
        "sampling_input_note": "only sorted case IDs were read before sampling; no answer content",
        "sampled": picks,
        "sample_flat_order": [
            {"model_exact_id": m, "case_id": c, "draw_index": i}
            for m in MODEL_ORDER for i, c in enumerate(picks[m])],
        "replacement_policy": "NONE - sampled failed/held slots are kept and exported as status notes",
        "api_calls": 0,
    }
    path = os.path.join(out_dir, "sampling_manifest.json")
    text = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    manifest["manifest_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print("SAMPLE FIXED (seed=%d):" % SEED)
    for m in MODEL_ORDER:
        print("  %-24s %s" % (m, picks[m]))
    print("manifest sha256 =", manifest["manifest_sha256"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
