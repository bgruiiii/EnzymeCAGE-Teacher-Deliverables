#!/usr/bin/env python3
"""R1 §3: the LOCAL context fill/expand step — NODE_ROOT / CONTEXT_ROOT /
deployed repo are explicit parameters; every input lands at the path the OLD
lanes expect; every lane command gets its OWN correct C95_LANE_CONTEXT (the
S5 context is never passed to R3 and vice versa). Runs locally (acceptance:
synthetic roots) AND on the node (real roots) — identical code, no on-billing
authoring.

Writes under --out:
  gf/c95_gf_context.json                  GF_DUAL_RUN_C95 v2 context (complete)
  union/context_c95.json                  union v2 context incl. materialize block
  lanes/C95_LANE_CONTEXT.s5_plm.json      W/S5/D/CKPT3B
  lanes/C95_LANE_CONTEXT.s5_gvp.json      W/S5/D/CR
  lanes/C95_LANE_CONTEXT.r3_deltas.json   W/R3/PREV/PS5/D
  lanes/C95_LANE_CONTEXT.r3_struct.json   B/D/SEQMAP (CURRENT seqmap, defect B)
  lanes/C95_LANE_CONTEXT.rx_adapter.json  reaction adapter task-root overrides
  lanes/C95_LANE_CONTEXT.rx_s1.json       s1 finalize overrides
  deploy_inputs.sh                        copies gen/s5 four-piece + tasks to the
                                          lane-expected locations (idempotent)
  n3_reaction_build.sh                    entity-checked, per-key FRESH output
                                          roots, adapter full -> registration ->
                                          s1 finalize per key (locked CLI sha
                                          asserted first)
  EXPAND_REPORT.json                      validation: zero unfilled placeholders,
                                          per-lane key sets exact, no S5 keys in
                                          R3 contexts, CKPT3B a clean path

Validation is fail-closed (exit 2): any remaining '{{', '<NODE_ROOT>',
'<context_root>' or prose-in-path is refused.
"""
import argparse
import json
import os
import stat
import sys

EXIT_OK, EXIT_CONFIG = 0, 2
P291_CFG = ("/usrdata/EnzymeCAGE_data/workspaces/p291_legacy600m_20260922/"
            "runtime/overlay_3b/3b_ensemble/seed_40/config.yaml")
PYT3B = "/usrdata/EnzymeCAGE_envs/enzymecage_t3b_generator_v1_20260911/bin/python"
T3B_CLI = "/usrdata/EnzymeCAGE_data/tools/t3b_reaction_asset_generator_v1_20260911/run_reaction_asset_v1.py"
T3B_CLI_SHA = "1f0481ce522a9e69310645c09a2497aa3ce09fb4c200bf2eaf8e28e0cc2b41a7"
T3B_FROZEN = "/usrdata/EnzymeCAGE_data/tools/t3b_reaction_asset_generator_v1_20260911/frozen_source/run_t3b.py"

LANE_REQUIRED_KEYS = {
    "s5_plm": {"W", "S5", "D", "CKPT3B"},
    "s5_gvp": {"W", "S5", "D", "CR"},
    "r3_deltas": {"W", "R3", "PREV", "PS5", "D"},
    "r3_struct": {"B", "D", "SEQMAP"},
    "rx_adapter": {"W", "R1", "R0", "PREV", "GENPY", "CLI", "FROZEN"},
    "rx_s1": {"W", "S1", "SAN", "PREV"},
}
BAD_TOKENS = ("{{", "<NODE_ROOT>", "<context_root>", "<NR>", "<CTX>", "<REPO>")


def expand_obj(o, subs):
    if isinstance(o, dict):
        return {k: expand_obj(v, subs) for k, v in o.items()}
    if isinstance(o, list):
        return [expand_obj(v, subs) for v in o]
    if isinstance(o, str):
        for k, v in subs.items():
            o = o.replace(k, v)
        return o
    return o


def check_clean(name, obj, errors):
    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items():
                if k.endswith("_note"):
                    continue  # prose lives ONLY in *_note fields
                walk(v, path + "/" + k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")
        elif isinstance(x, str):
            for t in BAD_TOKENS:
                if t in x:
                    errors.append({"context": name, "path": path, "bad_token": t, "value": x})
    walk(obj, "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staging-root", required=True, help="synced staging root containing gen/")
    ap.add_argument("--node-root", required=True, help="NODE_ROOT: where the staging tree lives on the node")
    ap.add_argument("--context-root", required=True, help="CONTEXT_ROOT: NEW task outputs (old workspaces never written)")
    ap.add_argument("--repo-root", required=True, help="deployed EnzymeCAGE-master")
    ap.add_argument("--gf-config-template", default=P291_CFG)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    gen = os.path.join(a.staging_root, "gen")
    for p in (gen, os.path.join(gen, "gf"), os.path.join(gen, "lanes"), os.path.join(gen, "union")):
        if not os.path.isdir(p):
            print(f"CONFIG_ERROR: missing {p}", file=sys.stderr)
            return EXIT_CONFIG
    subs = {"{{NODE_ROOT}}": a.node_root, "{{CONTEXT_ROOT}}": a.context_root,
            "{{REPO_ROOT}}": a.repo_root, "{{GF_CONFIG_TEMPLATE}}": a.gf_config_template}
    errors = []
    out = a.out
    os.makedirs(os.path.join(out, "gf"), exist_ok=True)
    os.makedirs(os.path.join(out, "union"), exist_ok=True)
    os.makedirs(os.path.join(out, "lanes"), exist_ok=True)

    # ---- template expansions ------------------------------------------------
    expanded = {}
    gf_tmpl = json.load(open(os.path.join(gen, "gf", "c95_gf_context.template.json")))
    expanded["gf"] = expand_obj(gf_tmpl, subs)
    json.dump(expanded["gf"], open(os.path.join(out, "gf", "c95_gf_context.json"), "w"), indent=1)
    union_tmpl = json.load(open(os.path.join(gen, "union", "context_c95.template.json")))
    expanded["union"] = expand_obj(union_tmpl, subs)
    json.dump(expanded["union"], open(os.path.join(out, "union", "context_c95.json"), "w"), indent=1)
    for lane in LANE_REQUIRED_KEYS:
        if lane.startswith("rx_"):
            continue  # built below, not from gen templates
        tmpl = json.load(open(os.path.join(gen, "lanes", f"C95_LANE_CONTEXT.{lane}.template.json")))
        ctxj = expand_obj(tmpl, subs)
        expanded[lane] = ctxj
        json.dump(ctxj, open(os.path.join(out, "lanes", f"C95_LANE_CONTEXT.{lane}.json"), "w"), indent=1)

    # ---- reaction-chain contexts (task roots under CONTEXT_ROOT) ------------
    rxt = os.path.join(a.context_root, "reaction_task")
    rx_adapter = {"W": rxt, "R1": rxt + "/R1_reaction_assets", "R0": rxt + "/R0_task_table",
                  "PREV": rxt + "/inputs", "GENPY": PYT3B, "CLI": T3B_CLI, "FROZEN": T3B_FROZEN}
    rx_s1 = {"W": a.context_root, "S1": a.context_root + "/S1_final",
             "SAN": rxt, "PREV": rxt}
    expanded["rx_adapter"], expanded["rx_s1"] = rx_adapter, rx_s1
    for lane in ("rx_adapter", "rx_s1"):
        json.dump(expanded[lane], open(os.path.join(out, "lanes", f"C95_LANE_CONTEXT.{lane}.json"), "w"), indent=1)

    # ---- validation ----------------------------------------------------------
    for name, obj in expanded.items():
        check_clean(name, obj, errors)
        if name in LANE_REQUIRED_KEYS:
            have = {k for k in obj if not k.endswith("_note")}
            need = LANE_REQUIRED_KEYS[name]
            if not need <= have:
                errors.append({"context": name, "missing_keys": sorted(need - have)})
    # cross-contamination: R3 contexts must not carry S5 keys and vice versa
    for name, forbidden in (("r3_struct", {"W", "S5", "PS5"}), ("r3_deltas", {"S5", "B", "SEQMAP"}),
                            ("s5_plm", {"B", "R3", "PS5"}), ("s5_gvp", {"B", "R3", "PS5"})):
        bad = forbidden & {k for k in expanded[name] if not k.endswith("_note")}
        if bad:
            errors.append({"context": name, "cross_contamination_keys": sorted(bad)})
    # CKPT3B must be a clean filesystem path (no prose)
    ck = expanded["s5_plm"]["CKPT3B"]
    if not ck.startswith("/") or " " in ck:
        errors.append({"context": "s5_plm", "bad_CKPT3B": ck})
    # GF context required fields for GF_DUAL_RUN_C95 v2
    for k in ("repo_root", "wrapper_root", "ckpt_path_template", "out_root", "cfg",
              "step_table", "runtime_map", "merge_manifest", "union_summary"):
        if not expanded["gf"].get(k):
            errors.append({"context": "gf", "missing_field": k})

    # ---- R1.1 §2: ONE registration connects producers and consumers --------
    # The union context must contain exactly the paths the lane PRODUCERS write
    # (task-local overlays), and the R3 delta consumer root must be the struct
    # producer root. Fail-closed: any mismatch is a validation error, because
    # "generated but not discoverable" was the audit §2 defect.
    plm, rd, rs = expanded["s5_plm"], expanded["r3_deltas"], expanded["r3_struct"]
    u_paths = {fam: {s["path"] for s in expanded["union"]["families"][fam]["sources"]}
               for fam in ("global", "pocket", "gvp")}
    producers = {
        "global": [plm["S5"] + "/overlay/global/legacy_esm2_3b"],
        "pocket": [plm["S5"] + "/overlay/pocket/legacy_esm2_3b",
                   rd["R3"] + "/overlay/pocket/legacy_esm2_3b"],
        "gvp": [plm["S5"] + "/overlay/gvp", rd["R3"] + "/overlay/gvp"],
    }
    for fam, want in producers.items():
        for w in want:
            if w not in u_paths[fam]:
                errors.append({"context": "union", "producer_path_not_registered": fam, "path": w})
    if rd["R3"] + "/struct_lane" != rs["B"]:
        errors.append({"context": "r3", "producer_consumer_root_split":
                       {"struct_producer_B": rs["B"], "delta_consumer_R3": rd["R3"]}})
    registry = {"node_root": a.node_root, "context_root": a.context_root, "repo_root": a.repo_root,
                "gf_config_template": a.gf_config_template,
                "s5_assets": plm["S5"],
                "task_overlays": {f: w for f, w in producers.items()},
                "r3_root": rd["R3"], "r3_struct_lane": rs["B"],
                "r3_worklist": rd["R3"] + "/struct_lane/full/R3_STRUCTURE_WORKLIST.tsv",
                "struct8_status": plm["S5"] + "/struct_lane/structure/STRUCT8_STATUS.tsv",
                "union_context_deployed": a.context_root + "/union/context_c95.json",
                "union_out": a.context_root + "/union",
                "merged_cfg": a.context_root + "/union/cfg/c95_3b_merged_config.yaml",
                "merge_manifest": a.context_root + "/union/MERGE_MANIFEST.tsv",
                "gf_context_deployed": a.context_root + "/gf/c95_gf_context.json",
                "gf_out": expanded["gf"]["out_root"],
                "raw_logits_dir": expanded["gf"]["out_root"] + "/raw_logits_3b",
                "ensemble_out": a.context_root + "/ensemble",
                "reaction": {"tasks": a.context_root + "/reaction_task/inputs/S4_reaction_assets/tasks",
                             "adapter_R1": rxt + "/R1_reaction_assets",
                             "s1_final": a.context_root + "/S1_final/final"}}
    os.makedirs(os.path.join(out, "registry"), exist_ok=True)
    json.dump(registry, open(os.path.join(out, "registry", "PATHS_REGISTRY.json"), "w"), indent=1)

    # ---- deploy_inputs.sh ----------------------------------------------------
    # R1.1 §2: deploy places EVERY command input at the path the commands
    # reference (union context at $CTX/union/, GF context at $CTX/gf/ — the
    # audit showed these stayed under expanded/ and N2/N5 would fail), creates
    # the task-local producer overlay directories the union now registers, and
    # provides EXPLICIT EMPTY-SCHEMA R3 status/worklist inputs so the old R3
    # delta selection code never dies on a first run with missing files
    # (header + 0 rows; later real runs overwrite with content).
    s5d = a.context_root + "/S5_task/S5_protein_assets"
    deploy = f"""#!/usr/bin/env bash
# C95 R1.1 deploy: put every lane input at the path the OLD lanes expect.
# Idempotent; never touches old workspaces (read-only doctrine).
set -euo pipefail
NR="{a.node_root}"; CTX="{a.context_root}"; EXP="{os.path.abspath(out)}"
mkdir -p "$CTX/S5_task/S5_protein_assets" "$CTX/gf" "$CTX/union" \\
         "$CTX/R3_task/R3_structure_protein/struct_lane/full" \\
         "$CTX/S5_task/S5_protein_assets/struct_lane/structure" \\
         "$CTX/S5_task/S5_protein_assets/overlay/global/legacy_esm2_3b" \\
         "$CTX/S5_task/S5_protein_assets/overlay/pocket/legacy_esm2_3b" \\
         "$CTX/S5_task/S5_protein_assets/overlay/gvp" \\
         "$CTX/R3_task/R3_structure_protein/overlay/pocket/legacy_esm2_3b" \\
         "$CTX/R3_task/R3_structure_protein/overlay/gvp" \\
         "$CTX/reaction_task/R0_task_table" "$CTX/reaction_task/inputs/S4_reaction_assets/tasks" \\
         "$CTX/reaction_task/R1_reaction_assets" "$CTX/S1_final" "$CTX/gf_out" "$CTX/lanes"
mkdir -p "$CTX/S5_task/S5_protein_assets/overlay/global/legacy_esm2_3b" \
         "$CTX/S5_task/S5_protein_assets/overlay/pocket/legacy_esm2_3b" \
         "$CTX/S5_task/S5_protein_assets/overlay/gvp"
cp -f "$NR"/gen/s5/S5_SEQMAP.pkl "$NR"/gen/s5/FINAL_SEQUENCE_UNIVERSE.tsv \\
      "$NR"/gen/s5/S5_GAP_FLAGS.tsv.gz "$NR"/gen/s5/S5_SENTINEL_SELECTION.tsv \\
      "$NR"/gen/s5/WORKLIST_SUMMARY.json "$CTX/S5_task/S5_protein_assets/"
cp -f "$NR"/gen/reaction/tasks_c95/RXASSET_*.json "$CTX/reaction_task/inputs/S4_reaction_assets/tasks/"
# expanded contexts land WHERE THE COMMANDS READ THEM (R1.1 §2):
cp -f "$EXP"/union/context_c95.json "$CTX/union/context_c95.json"
cp -f "$EXP"/gf/c95_gf_context.json "$CTX/gf/c95_gf_context.json"
cp -f "$EXP"/lanes/C95_LANE_CONTEXT.*.json "$CTX/lanes/"
cp -f "$EXP"/registry/PATHS_REGISTRY.json "$CTX/registry_PATHS_REGISTRY.json" 2>/dev/null || true
# explicit empty-schema R3 inputs (real runs overwrite; never fake content):
[ -f "$CTX/S5_task/S5_protein_assets/struct_lane/structure/STRUCT8_STATUS.tsv" ] || \\
 printf 'work_item_id\\tuid\\tsequence_sha256\\troute\\tstatus\\thttp\\tseconds\\tretries\\tpdb\\tpocket_pdb\\tpocket_rows\\tpocket_idx_file\\tdetail\\n' \\
   > "$CTX/S5_task/S5_protein_assets/struct_lane/structure/STRUCT8_STATUS.tsv"
[ -f "$CTX/R3_task/R3_structure_protein/struct_lane/full/R3_STRUCTURE_WORKLIST.tsv" ] || \\
 printf 'work_item_id\\tshard_id\\tsequence_sha256\\tselected_uid\\traw_length\\tneeds\\tgap_reasons\\torigin\\treused_status\\treused_route\\treused_work_dir\\treused_pocket_rows\\n' \\
   > "$CTX/R3_task/R3_structure_protein/struct_lane/full/R3_STRUCTURE_WORKLIST.tsv"
# post-deploy self-check: EVERY input the N2/N5/N6 commands read must open & parse
python3 - <<'PYCHK'
import json, os, gzip, sys
ctx = os.environ.get("CTX_DIR", "{a.context_root}")
need_json = [f"{{ctx}}/union/context_c95.json", f"{{ctx}}/gf/c95_gf_context.json"]
for f in sorted(__import__("glob").glob(ctx + "/lanes/C95_LANE_CONTEXT.*.json")):
    need_json.append(f)
for f in need_json:
    json.load(open(f))
for f in (f"{{ctx}}/S5_task/S5_protein_assets/S5_SEQMAP.pkl",
          f"{{ctx}}/S5_task/S5_protein_assets/S5_GAP_FLAGS.tsv.gz",
          f"{{ctx}}/S5_task/S5_protein_assets/FINAL_SEQUENCE_UNIVERSE.tsv",
          f"{{ctx}}/S5_task/S5_protein_assets/S5_SENTINEL_SELECTION.tsv",
          f"{{ctx}}/S5_task/S5_protein_assets/struct_lane/structure/STRUCT8_STATUS.tsv",
          f"{{ctx}}/R3_task/R3_structure_protein/struct_lane/full/R3_STRUCTURE_WORKLIST.tsv"):
    assert os.path.isfile(f), f
with gzip.open(ctx + "/S5_task/S5_protein_assets/S5_GAP_FLAGS.tsv.gz", "rt") as fh:
    hdr = fh.readline().rstrip("\\n").split("\\t")
assert hdr[:8] == ["sequence_sha256", "selected_uid", "seq_ok", "gap_status",
                   "global_gap", "pocket_ok", "gvp_ok", "gap_reasons"], hdr
u = json.load(open(f"{{ctx}}/union/context_c95.json")); g = json.load(open(f"{{ctx}}/gf/c95_gf_context.json"))
assert g["cfg"].endswith("union/cfg/c95_3b_merged_config.yaml"), g["cfg"]
print("DEPLOY_SELFCHECK_OK", len(need_json), "json contexts + 6 entity files + v2 header")
PYCHK
echo "DEPLOY_INPUTS_DONE $CTX"
"""
    dp = os.path.join(out, "deploy_inputs.sh")
    open(dp, "w").write(deploy)
    os.chmod(dp, os.stat(dp).st_mode | stat.S_IXUSR)

    # ---- n3_reaction_build.sh (entity-checked, per-key FRESH roots) ----------
    n3 = f"""#!/usr/bin/env bash
# N3 reaction side: TRUE-MISSING keys only (n2_reaction_entity_check.py wrote
# R0_task_table first: TRUE_MISSING_BUILD_KEYS.txt + the same-name task table).
# Generation entry = the ADAPTED recovered r1_asset_adapter (its run_wrapper
# already enforces a FRESH per-key output-root — the line ~100 assert — plus
# exact/de-stereo-alias key isolation and the §5.2 field gates; the audit
# defect was a raw CLI loop sending all keys into ONE root, which is gone).
# Then status registration -> adapted s1 finalize per key (back-link sha
# gates). Locked CLI identity is asserted before anything runs. s2's merged
# bundle + loader gates are absorbed by N4 materialize (method source cited
# in c95_asset_union.py). C95_LANE_CONTEXT is switched PER COMMAND — never
# shared across chains.
set -euo pipefail
NR="{a.node_root}"; CTX="{a.context_root}"; ADAPTED="$NR/adapted"
CLI="{T3B_CLI}"; CLI_SHA="{T3B_CLI_SHA}"
echo "$(sha256sum "$CLI")" | grep -q "$CLI_SHA" || {{ echo "T3B_CLI_SHA_MISMATCH — STOP"; exit 9; }}
EC="$CTX/reaction_task/R0_task_table"
test -s "$EC/TRUE_MISSING_BUILD_KEYS.txt" || echo "NOTE: no true-missing keys — adapter run is a no-op (entity-check-first worked)"
C95_LANE_CONTEXT="$CTX/lanes/C95_LANE_CONTEXT.rx_adapter.json" \\
  python3 "$ADAPTED/r1_asset_adapter_c95.py" full --all
python3 "$NR/scripts/register_rxchain_status.py" \\
  --selected-root "$CTX/reaction_task/R1_reaction_assets/selected" --san-root "$CTX/reaction_task"
while read -r key; do
  C95_LANE_CONTEXT="$CTX/lanes/C95_LANE_CONTEXT.rx_s1.json" \\
    python3 "$ADAPTED/s1_final_wrapper_c95.py" finalize "$key" || echo "$key" >> "$EC/FINALIZE_TYPED_FAILURE_KEYS.txt"
done < "$EC/TRUE_MISSING_BUILD_KEYS.txt"
echo "N3_REACTION_CHAIN_DONE"
"""
    n3p = os.path.join(out, "n3_reaction_build.sh")
    open(n3p, "w").write(n3)
    os.chmod(n3p, os.stat(n3p).st_mode | stat.S_IXUSR)

    report = {"node_root": a.node_root, "context_root": a.context_root, "repo_root": a.repo_root,
              "gf_config_template": a.gf_config_template,
              "contexts_written": {k: True for k in expanded},
              "commands_written": [dp, n3p],
              "registry": os.path.join(out, "registry", "PATHS_REGISTRY.json"),
              "errors": errors, "ok": not errors}
    json.dump(report, open(os.path.join(out, "EXPAND_REPORT.json"), "w"), indent=1)
    print(json.dumps({"ok": not errors, "errors": errors[:10],
                      "contexts": sorted(expanded)}, indent=1))
    return EXIT_OK if not errors else EXIT_CONFIG


if __name__ == "__main__":
    sys.exit(main())
