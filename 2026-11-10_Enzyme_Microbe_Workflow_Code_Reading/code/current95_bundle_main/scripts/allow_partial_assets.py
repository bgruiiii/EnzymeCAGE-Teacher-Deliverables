"""A missing asset may block a step, never hide conflicts/loader failures."""
import argparse
import json
from pathlib import Path
import sys

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--union-out',required=True);a=ap.parse_args()
    p=Path(a.union_out)/'MERGE_BLOCKERS.json'
    missing={'REACTION_ASSET_MISSING','MOLECULE_CONFORMATION_MISSING','FORMAL_SDF_ABSENT','MOL_GRAPH_BUILD_FAILED'}
    rows=json.loads(p.read_text()) if p.exists() else []
    hard=[r for r in rows if r.get('status') not in missing]
    if hard:
        print(json.dumps({'HARD_ASSET_BLOCKERS':hard},indent=2));return 4
    cfg=Path(a.union_out)/'cfg/c95_3b_merged_config.yaml'
    if not cfg.exists():return 5
    print(json.dumps({'typed_missing_asset_entries':len(rows),'policy':'GF prescan retains whole-step INCOMPLETE; no candidate dropped'}))
    return 0
if __name__=='__main__':sys.exit(main())
