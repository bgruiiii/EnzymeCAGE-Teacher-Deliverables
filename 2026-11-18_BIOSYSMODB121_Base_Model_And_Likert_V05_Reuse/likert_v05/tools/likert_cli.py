#!/usr/bin/env python3
"""Offline commands are default; live scoring requires explicit confirmation."""
import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
from likert_eval.common import load,totals_contract
from likert_eval.pipeline import prepare,validate_return,merge


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('prepare');p.add_argument('--item',required=True);p.add_argument('--out',required=True);p.add_argument('--dimensions')
    p=sub.add_parser('validate');p.add_argument('--request',required=True);p.add_argument('--response',required=True);p.add_argument('--out')
    p=sub.add_parser('merge');p.add_argument('--request',required=True);p.add_argument('--response',required=True);p.add_argument('--baseline');p.add_argument('--out',required=True)
    p=sub.add_parser('totals');p.add_argument('--rating',required=True)
    p=sub.add_parser('run');p.add_argument('--request',required=True);p.add_argument('--config',required=True);p.add_argument('--work',required=True);p.add_argument('--i-confirm-live-paid-calls',action='store_true')
    a=parser.parse_args()
    if a.command=='prepare':result=prepare(load(a.item),a.dimensions.split(',')if a.dimensions else None)
    elif a.command=='validate':result=validate_return(load(a.response),load(a.request))
    elif a.command=='merge':result=merge(load(a.response),load(a.request),load(a.baseline)if a.baseline else None)
    elif a.command=='totals':
        x=load(a.rating);result=totals_contract(x.get('dimensions',x))
    else:
        from likert_eval.runner import run
        result=run(load(a.request),load(a.config),a.work,a.i_confirm_live_paid_calls)
    if getattr(a,'out',None):
        target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    else:print(json.dumps(result,ensure_ascii=False,indent=2))
    if a.command=='validate'and not result['valid']:raise SystemExit(1)


if __name__=='__main__':main()
