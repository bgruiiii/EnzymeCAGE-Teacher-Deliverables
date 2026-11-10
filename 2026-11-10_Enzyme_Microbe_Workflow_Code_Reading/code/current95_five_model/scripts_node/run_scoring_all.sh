#!/usr/bin/env bash
# R4 scoring driver: STRICTLY SERIAL five-arm forward + evaluation.
# Prereq: runtime/pc_genimpact/ADMISSION_DECISION.json exists (gate + NC review done).
# Usage: run_scoring_all.sh [arm ...]   (default: all five, in order)
set -u
NEWROOT="/usrdata/EnzymeCAGE_data/workspaces/current95_ngpu32g_20261031/five_model_complete_20261103"
PKG="$NEWROOT/current95_five_model_complete_prep_20261103"
GF=/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python
LOGS="$NEWROOT/logs"
POOL="$NEWROOT/runtime/pool"

[ -f "$NEWROOT/runtime/pc_genimpact/ADMISSION_DECISION.json" ] || { echo "ADMISSION_DECISION MISSING — scoring forbidden"; exit 2; }

ARMS_DEFAULT="legacy_esm2_3b legacy_esmc600m new_esmc600m current_e0_enzgfm650m new_enzgfm650m"
ARMS="${*:-$ARMS_DEFAULT}"

for ARM in $ARMS; do
  echo "===== [$(date -u +%FT%TZ)] SCORING $ARM ====="
  case "$ARM" in
    legacy_esm2_3b|legacy_esmc600m|new_esmc600m)
      ( cd "$PKG/sources" && $GF -B -X faulthandler r3_gf_unified.py --arm "$ARM" ) >> "$LOGS/gf_${ARM}.log" 2>&1
      RC=$? ;;
    current_e0_enzgfm650m|new_enzgfm650m)
      ( cd "$NEWROOT/scripts_node" && $GF -B -X faulthandler r4_gf_enzgfm.py --arm "$ARM" ) >> "$LOGS/gf_${ARM}.log" 2>&1
      RC=$? ;;
    *) echo "unknown arm $ARM"; exit 2 ;;
  esac
  echo "gf rc=$RC ($ARM)"
  [ $RC -ne 0 ] && { echo "GF FAILED for $ARM — stopping chain"; exit $RC; }
  for CTX in main delta15; do
    $GF -B "$PKG/sources/r2_ensemble_eval.py" --arm "$ARM" \
      --raw-logits-dir "$NEWROOT/gf_out/$ARM/$CTX/raw_logits_$ARM" \
      --step-table "$POOL/UNIFIED_STEP_TABLE_$CTX.json" \
      --runtime-map "$PKG/inputs/$CTX/RUNTIME_SEQUENCE_PARENT.tsv" \
      --eval-labels "$POOL/EVAL_LABELS_UNIFIED_$CTX.tsv" \
      --seeds 40,41,42,43,44 \
      --expected-context "$NEWROOT/gf_out/$ARM/$CTX/COMMON_CONTEXT.json" \
      --out-dir "$NEWROOT/eval/$ARM/$CTX" \
      --locked-shas-json "$NEWROOT/runtime/locked_shas_$ARM.json" >> "$LOGS/eval_${ARM}_${CTX}.log" 2>&1
    RC=$?
    echo "eval $ARM/$CTX rc=$RC"
    [ $RC -ne 0 ] && { echo "EVAL FAILED (rc=$RC) $ARM/$CTX — stopping chain"; exit $RC; }
  done
done
echo "===== [$(date -u +%FT%TZ)] ALL SCORING+EVAL DONE ====="
