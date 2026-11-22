#!/usr/bin/env python3
"""Reusable T3B reaction-asset generator CLI (recovery build).

Contract:
  --reaction-task-json <file>  JSON with reaction_task_id, reaction_smiles, depth,
                               evidence_hash, source_record_id
  --output-root      <dir>     fresh task-local directory; refuses a non-empty one
  --mode             full|aam_center

This file is a thin parameterising wrapper. It imports the SHA-verified frozen
run_t3b.py, sets RETURN_DIR/THREE_REACTIONS/command_log/timing, and calls the
frozen scientific functions. It never reimplements, edits or bypasses them, and
it never invokes the frozen module's main().
"""
import argparse, hashlib, importlib.util, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

FROZEN = Path(__file__).resolve().parent / "frozen_source" / "run_t3b.py"
FROZEN_SHA = "bfb293456016868ca34ae7ff3cb84c69f416b7326dc9c9c5930ae770804e8e05"
SKIP = None


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_frozen():
    if sha(FROZEN) != FROZEN_SHA:
        raise SystemExit("BLOCKED_SOURCE_IDENTITY: frozen run_t3b.py SHA mismatch")
    spec = importlib.util.spec_from_file_location("t3b_frozen_runtime", FROZEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # module level is path/sys.path setup only
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reaction-task-json", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--mode", choices=("full", "aam_center"), default="full")
    a = ap.parse_args()

    task = json.loads(Path(a.reaction_task_json).read_text())
    for k in ("reaction_task_id", "reaction_smiles", "depth", "evidence_hash", "source_record_id"):
        if k not in task:
            raise SystemExit("input JSON missing required key: " + k)
    out = Path(a.output_root)
    if out.exists() and any(out.iterdir()):
        raise SystemExit("REFUSING non-empty output root (fresh task-local directory required): " + str(out))
    out.mkdir(parents=True, exist_ok=True)

    mod = load_frozen()
    mod.RETURN_DIR = out
    mod.THREE_REACTIONS = [{
        "reaction_task_id": task["reaction_task_id"],
        "reaction_smiles": task["reaction_smiles"],
        "depth": task["depth"],
        "evidence_hash": task["evidence_hash"],
        "source_record_id": task["source_record_id"],
    }]
    mod.command_log = []
    mod.timing = {}

    import rdkit
    rt = {"run_utc": now(), "cli": str(Path(__file__).resolve()),
          "cli_sha256": sha(Path(__file__).resolve()), "frozen_source_sha256": sha(FROZEN),
          "mode": a.mode, "input_task": task, "output_root": str(out),
          "python_executable": sys.executable, "sys_prefix": sys.prefix,
          "versions": {"python": sys.version.split()[0], "rdkit": rdkit.__version__}}
    try:
        import numpy, pandas, drfp, torch
        rt["versions"].update({"numpy": numpy.__version__, "pandas": pandas.__version__,
                               "drfp": drfp.__version__, "torch": torch.__version__})
    except Exception as e:
        rt["versions"]["package_error"] = repr(e)[:200]
    rt["versions"]["transformers"] = __import__("importlib").import_module(
        "transformers").__version__
    rt["frozen_functions_called"] = []

    if a.mode == "full":
        asset_gen = mod.generate_all_assets()
        rt["frozen_functions_called"].append("generate_all_assets")
        staged = mod.build_staged_index(asset_gen)
        rt["frozen_functions_called"].append("build_staged_index")
        rec = asset_gen["reaction_records"][0]
        rt["substage_statuses"] = {"drfp": rec.get("drfp_status"), "aam": rec.get("aam_status"),
                                   "center": rec.get("center_status"),
                                   "reaction_asset_status": rec.get("reaction_asset_status")}
        rt["per_reaction_record"] = rec
        dd = dict(asset_gen["drfp_results"].get(task["reaction_task_id"], {}))
        fp = dd.pop("fingerprint", None)
        if fp is not None:
            import numpy as _np
            dd.update({"shape": list(fp.shape), "dtype": str(fp.dtype),
                       "nonzero_count": int((fp != 0).sum()),
                       "all_finite": bool(_np.isfinite(fp).all())})
        rt["drfp_detail"] = dd
        rt["aam_detail"] = asset_gen["aam_results"].get(task["reaction_task_id"], {})
        rt["center_detail"] = {k: v for k, v in asset_gen["center_results"].get(
            task["reaction_task_id"], {}).items() if k != "center"}
        rt["center_detail"]["center"] = asset_gen["center_results"].get(
            task["reaction_task_id"], {}).get("center")
        rt["molecules"] = []
        import pandas as _pd
        from rdkit import Chem
        mc = Path(asset_gen["mol_conf_dir"])
        for _, row in _pd.read_csv(mc / "mol2id.csv").iterrows():
            smi, idx = row["SMILES"], int(row["ID"])
            sdf = mc / ("%d.sdf" % idx)
            m = Chem.SDMolSupplier(str(sdf), removeHs=False)[0] if sdf.exists() else None
            rt["molecules"].append({
                "smiles": smi, "sdf_id": idx, "sdf_exists": sdf.exists(),
                "canonical_matches_input": bool(m) and Chem.MolToSmiles(Chem.MolFromSmiles(smi)) == smi,
                "atoms": int(m.GetNumAtoms()) if m else None,
                "has_conformer": bool(m and m.GetNumConformers()),
                "coordinates_finite": bool(m and m.GetNumConformers() and __import__("numpy").isfinite(
                    m.GetConformer().GetPositions()).all())})
        rt["staged_index"] = staged
        rt["outputs_expected"] = ["staged_assets/drfp/rxn2fp.pkl", "staged_assets/aam/rxn2aam.pkl",
                                  "staged_assets/reacting_center/reacting_center.pkl",
                                  "staged_assets/molecule_conformation/mol2id.csv",
                                  "staged_assets/molecule_conformation/<ID>.sdf",
                                  "STAGED_REACTION_ASSET_INDEX.csv",
                                  "STAGED_REACTION_ASSET_MANIFEST.csv"]
        # key/identity validation
        import pickle as pkl
        staged_dir = out / "staged_assets"
        keys = {}
        for lab, rel in (("drfp", "drfp/rxn2fp.pkl"), ("aam", "aam/rxn2aam.pkl"),
                         ("center", "reacting_center/reacting_center.pkl")):
            p = staged_dir / rel
            keys[lab] = {"file": str(p), "exists": p.exists(),
                         "keys": sorted(pkl.load(open(p, "rb"))) if p.exists() else []}
        keys["sole_key_is_exact_reaction"] = all(
            keys[l]["keys"] == [task["reaction_smiles"]] for l in ("drfp", "aam", "center"))
        rt["asset_key_validation"] = keys
        rt["command_log"] = list(mod.command_log)
        rt["timing"] = dict(mod.timing)
        ok = (rt["substage_statuses"]["drfp"] == "OK" and rt["substage_statuses"]["aam"] == "OK"
              and rt["substage_statuses"]["center"] == "OK" and keys["sole_key_is_exact_reaction"])
        rt["status"] = "OK" if ok else "FAILED"
    else:
        aam = mod.generate_aam(task["reaction_smiles"])
        rt["frozen_functions_called"].append("generate_aam")
        res = {"aam": aam}
        if aam.get("status") == "OK":
            res["center"] = mod.extract_reacting_center(task["reaction_smiles"],
                                                       {task["reaction_smiles"]: aam["mapped_rxn"]})
            rt["frozen_functions_called"].append("extract_reacting_center")
        rt["aam_center_result"] = res
        rt["command_log"] = list(mod.command_log)
        rt["status"] = "OK" if res["aam"].get("status") == "OK" and res.get("center", {}).get("status") == "OK" else "FAILED"

    (out / ("FULL_ASSET_RESULT.json" if a.mode == "full" else "AAM_CENTER_RESULT.json")).write_text(
        json.dumps(rt, indent=2, default=str))
    print(json.dumps({"status": rt["status"], "mode": a.mode,
                      "substage_statuses": rt.get("substage_statuses"),
                      "sole_key_is_exact_reaction": rt.get("asset_key_validation", {}).get("sole_key_is_exact_reaction"),
                      "result_file": str(out / ("FULL_ASSET_RESULT.json" if a.mode == "full" else "AAM_CENTER_RESULT.json"))},
                     indent=2, default=str))
    return 0 if rt["status"] == "OK" else 3


if __name__ == "__main__":
    sys.exit(main())
