"""CLI (R2). Steps input may carry replay-only binding fields
(step_id/model_key_sha256); the wrapper path ignores them."""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict

from .config import ToolConfig
from .predict import predict_reaction, predict_steps


def _load_config(args) -> ToolConfig:
    path = args.config or os.environ.get("ENZYME_HOST_TOOL_CONFIG", "")
    if path:
        return ToolConfig.from_json(path)
    return ToolConfig()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="enzyme_host_tool")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("predict", help="single step target reaction")
    p1.add_argument("--reaction", required=True)
    p1.add_argument("--model-reaction", default="")
    p1.add_argument("--step-id", default="S01")
    p1.add_argument("--model-key-sha256", default="", help="replay binding (cache_replay_c2 only)")
    p1.add_argument("--pathway-id", default="single")
    p1.add_argument("--recall-topk", type=int, default=10)
    p1.add_argument("--config", default="")
    p1.add_argument("-o", "--out", default="")
    p2 = sub.add_parser("predict-steps", help="list of already-split steps with replay binding fields")
    p2.add_argument("--in", dest="infile", required=True)
    p2.add_argument("--recall-topk", type=int, default=10)
    p2.add_argument("--config", default="")
    p2.add_argument("-o", "--out", default="")
    args = ap.parse_args(argv)
    try:
        cfg = _load_config(args)
    except Exception as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2
    notes: list = []
    if args.cmd == "predict":
        res = predict_reaction(args.reaction, step_id=args.step_id, pathway_id=args.pathway_id,
                               config=cfg, model_reaction=args.model_reaction or None,
                               recall_topk=args.recall_topk, backend_notes=notes,
                               model_key_sha256=args.model_key_sha256)
        payload = asdict(res)
    else:
        try:
            raw = json.loads(open(args.infile, encoding="utf-8").read())
        except Exception as exc:
            print(f"input error: {exc}", file=sys.stderr)
            return 2
        res = predict_steps(raw.get("steps", []), pathway_id=raw.get("pathway_id", "pathway"),
                            config=cfg, recall_topk=args.recall_topk)
        payload = {"pathway_id": res.pathway_id, "n_steps": res.n_steps,
                   "steps": [asdict(s) for s in res.steps]}
    payload["environment_notes"] = notes
    out = json.dumps(payload, ensure_ascii=False, indent=1)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out + "\n")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
