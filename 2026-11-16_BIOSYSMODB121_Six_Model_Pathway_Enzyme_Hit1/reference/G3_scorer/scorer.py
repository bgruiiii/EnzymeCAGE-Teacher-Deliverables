#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scorer.py -- BIOSYSMOdb150 offline scorer (G3 FROZEN 2026-09-28).

TEACHER-FROZEN implementation of the five science layers
(Pathway 45 / SMILES 10 / Enzyme 20 / Microbial identity 15 / Traits 10)
plus the independent evidence / engineering / abstention axes.
Frozen adjudications (teacher reply 2026-09-28, sha 1fa908f5...):
  D1 trait numeric accuracy over mask-declared numeric cells only; F2/F3/F4
     item-level cells out of the numeric denominator (sub-field mask is
     authoritative); preference/category WORDS reported as text_coverage;
     1161 pending range/multi-value cells stay out; completeness separate.
  D2 independent equal-weight sub-indicators; enzyme-microbe pair on accepted
     species/strain name; active wrong TaxID -> IDENTITY_CONFLICT and pair
     wrong; TaxID=null -> name-only pair credit, TaxID sub-field = recall miss.
  D3 Jaccard threshold 0.5; A->B != B->A; stable-id tie-break; split/merge no
     manual forgiveness; one-to-many matches at most one gold step.
  D4 overclaims are independent reporting + evidence-axis stats only, never a
     science deduction; null is a recall miss and never an overclaim.
  D5 formal genome accession ONLY from traits.F14.value.genome_accession;
     disagreeing profile-level compatibility field -> CONFLICT, no second truth.
  D6 primary SMILES score is always canonical isomeric; achiral goes to the
     appendix/sensitivity reference only.

Frozen boundaries:
  * reads ONLY G1 gold, G2 cases and the G1 lookup manifest; never writes
    anywhere except its own report output on stdout/--out;
  * gold is canonicalized with the SAME RDKit version and options as
    predictions -- one-sided cleaning is not possible by construction;
  * null values are recall misses and never overclaims;
  * extra JSON fields produce warnings only and never fail the schema axis;
  * within-layer subindicator weights and the trait composition are
    CANDIDATE values flagged PENDING_TEACHER (see score_recipe.md);
  * no real model answers are ever read: only local mock files under
    G3_scorer/mocks/ are scored in this phase.
"""

import argparse
import collections
import csv
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.abspath(os.path.join(HERE, os.pardir))
G1 = os.path.join(STAGE, "G1_gold")
G2 = os.path.join(STAGE, "G2_questions")
SOURCE_CSV = os.path.join(STAGE, os.pardir, "00_Authority_Teacher_Plan", "BIOSYSMOdb v2")

LAYERS = {"pathway": 0.45, "smiles": 0.10, "enzyme": 0.20,
          "microbial_identity": 0.15, "traits": 0.10}
TRAITS = ["F%d" % i for i in range(1, 16)]
SUBFIELD_MASK_TRAITS = {"F2": ("minimum_c", "optimum_c", "maximum_c"),
                        "F3": ("minimum", "optimum", "maximum"),
                        "F4": ("minimum", "optimum", "maximum", "unit", "category")}


def norm(text):
    if text is None:
        return ""
    if not isinstance(text, str):
        text = json.dumps(text, sort_keys=True) if isinstance(text, (dict, list)) else str(text)
    return " ".join(text.strip().lower().split())


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


# --------------------------------------------------------------------------
# RDKit normalization (identical path for gold and prediction)
# --------------------------------------------------------------------------

class Chem:
    def __init__(self):
        self._rdkit = None
        try:
            from rdkit import Chem as _C
            from rdkit.Chem.MolStandardize import rdMolStandardize  # noqa
            self._rdkit = _C
            self.version = __import__("rdkit").__version__
        except Exception:
            self.version = "UNAVAILABLE"

    def canon(self, smiles, achiral=False):
        if not smiles or self._rdkit is None:
            return None
        try:
            mol = self._rdkit.MolFromSmiles(smiles)
            if mol is None:
                return None
            if achiral:
                mol = self._rdkit.MolFromSmiles(self._rdkit.MolToSmiles(mol))
                mt = self._rdkit.MolOps.RemoveStereochemistry if hasattr(
                    self._rdkit.MolOps, "RemoveStereochemistry") else None
                if mt:
                    mt(mol)
                return self._rdkit.MolToSmiles(mol)
            return self._rdkit.MolToSmiles(mol)
        except Exception:
            return None


CHEM = Chem()


# --------------------------------------------------------------------------
# gold index
# --------------------------------------------------------------------------

class GoldIndex:
    def __init__(self):
        self.steps = collections.defaultdict(dict)       # case -> step_id -> step
        self.enzymes = collections.defaultdict(lambda: collections.defaultdict(set))
        self.enzyme_ec = collections.defaultdict(lambda: collections.defaultdict(set))
        self.step_organisms = collections.defaultdict(lambda: collections.defaultdict(set))
        self.profiles = collections.defaultdict(dict)    # case -> taxid -> profile
        self.item_values = collections.defaultdict(lambda: collections.defaultdict(set))
        self.subfield_values = collections.defaultdict(lambda: collections.defaultdict(dict))
        self.scoreable_items = collections.defaultdict(set)
        self.scoreable_subfields = collections.defaultdict(set)
        self._load()

    def _load(self):
        for row in read_tsv(os.path.join(G1, "reaction_gold.tsv")):
            case, sid = row["case_id"], row["step_occurrence_id"]
            step = self.steps[case].setdefault(sid, {
                "step_id": sid, "order": int(row["linear_display_order"] or 0),
                "branch": row.get("branch_id", ""),
                "preds": set(p for p in (row.get("predecessor_step_ids") or "").split("|") if p),
                "subs": [], "prods": [],
            })
            role = row["role_label"]
            if role in ("MAIN_SUBSTRATE", "MAIN_PRODUCT"):
                comp = {
                    "compound_id": row["compound_id"],
                    "names": {n for n in (norm(row.get("identity_name")),
                                          norm(row.get("db_cmpdname"))) if n},
                    "iso": CHEM.canon(row.get("isosmiles")),
                    "achiral": CHEM.canon(row.get("isosmiles"), achiral=True),
                }
                step["subs" if role == "MAIN_SUBSTRATE" else "prods"].append(comp)
        for row in read_tsv(os.path.join(G1, "enzyme_gold.tsv")):
            case = row["case_id"]
            sid = row["step_occurrence_id"]
            self.enzymes[case][sid].add(norm(row.get("enzyme_name")))
            ec = norm(row.get("ec_number_normalized"))
            self.enzyme_ec[case][sid].add(None if ec in ("", "not_observed") else ec)
        for row in read_tsv(os.path.join(G1, "organism_gold.tsv")):
            if row.get("scope") != "STEP":
                continue
            case = row["case_id"]
            self.step_organisms[case][row["step_occurrence_id"]].add(
                norm(row.get("matched_organism_name")))
            taxid = row.get("taxid", "").strip()
            if taxid:
                self.step_organisms[case][row["step_occurrence_id"]].add(taxid)
            prof = self.profiles[case].setdefault(taxid or row.get("matched_organism_name", ""), {
                "taxid": taxid, "name": norm(row.get("matched_organism_name")),
                "genome": row.get("genome_id", "").strip(),
            })
            prof["name"] = prof["name"] or norm(row.get("matched_organism_name"))
        for row in read_tsv(os.path.join(G1, "trait_scoreability_mask.tsv")):
            key = (row["ncbi_taxid"], row["trait_id"])
            if row["scoreable"] == "TRUE":
                self.scoreable_items[row["case_id"]].add(key)
        for row in read_tsv(os.path.join(G1, "trait_gold.tsv")):
            if row["value_status"] == "OBSERVED" and (row.get("value") or "").strip():
                v = norm(row["value"])
                if v not in ("na", "n/a", "no robust majority"):
                    # multi-valued gold strings ("DSM x|ATCC y") are split into
                    # their members for membership comparison
                    for part in v.split("|"):
                        part = part.strip()
                        if part:
                            self.item_values[row["case_id"]][
                                (row["ncbi_taxid"], row["trait_id"])].add(part)
        for row in read_tsv(os.path.join(G1, "trait_subfield_scoreability_mask.tsv")):
            key = (row["ncbi_taxid"], row["trait_id"], row["target_subfield"])
            if row["scoreable"] == "TRUE" and (row.get("accepted_gold_values") or "").strip():
                self.scoreable_subfields[row["case_id"]].add(key)
                self.subfield_values[row["case_id"]][key] = {
                    norm(v) for v in row["accepted_gold_values"].split("|") if norm(v)}


_ACCESSION_RE = re.compile(r"^(gca|gcf)_\d{6}(\.\d+)?$")


def _numeric(v):
    try:
        float(str(v))
        return True
    except (TypeError, ValueError):
        return False


def _get_cell(traits_dict, trait):
    """tolerant trait-cell lookup: short ids (F2) and schema keys (F2_temperature)."""
    cell = traits_dict.get(trait)
    if cell is None:
        for k in traits_dict:
            if isinstance(k, str) and k.split("_")[0] == trait:
                cell = traits_dict[k]
                break
    return cell if isinstance(cell, dict) else {}


def _pred_parts(raw):
    """normalized scalar set of a predicted (sub)field value container."""
    vals = []
    if isinstance(raw, dict):
        vals = [v for v in raw.values()
                if v not in (None, "") and not isinstance(v, (dict, list))]
    elif raw is not None:
        vals = [raw]
    out = set()
    for v in vals:
        if isinstance(v, str):
            out.add(norm(v))
        elif isinstance(v, bool):
            out.add("true" if v else "false")
        elif isinstance(v, (int, float)):
            out.add("%g" % v)
        else:
            out.add(norm(v))
    return out


def value_matches(answer_value, gold_values):
    """Exact string match OR numeric equality (no tolerance: same number)."""
    for g in gold_values:
        if answer_value == g:
            return True
        try:
            if float(answer_value) == float(g):
                return True
        except (TypeError, ValueError):
            pass
    return False


GOLD = GoldIndex()

# --------------------------------------------------------------------------
# CONTROLLED_INPUT mask (teacher G2 signoff 1fa908f5, 2026-09-28):
# names disclosed in the rendered question are controlled input. Repeating a
# controlled name earns NO autonomous recall; it must never act as a global
# exemption and never masks structural/directional errors.
# --------------------------------------------------------------------------
CONTROLLED_MASK_PATH = os.path.join(G2, "controlled_input_scoring_mask.tsv")
CONTROLLED = {}          # case_id -> set of normalized controlled tokens
CONTROLLED_META = {"rows": 0, "cases": 0, "path": None}


def load_controlled_mask(path=None):
    global CONTROLLED
    path = path or CONTROLLED_MASK_PATH
    CONTROLLED = {}
    rows = 0
    with open(path, encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        for row in rd:
            cid = row["case_id"].strip()
            tok = norm(row["controlled_token"])
            if not cid or not tok:
                continue
            CONTROLLED.setdefault(cid, set()).add(tok)
            rows += 1
    CONTROLLED_META.update({"rows": rows, "cases": len(CONTROLLED), "path": path})
    return CONTROLLED


CONTROLLED = load_controlled_mask()

# strain-level gold organisms: matched name differs from the raw row name
# (e.g. "Arthrobacter protophormiae RKJ100") or the taxid is absent
_GOLD_STRAIN_TAXIDS = {}
for _row in read_tsv(os.path.join(G1, "organism_gold.tsv")):
    _matched = norm(_row.get("matched_organism_name"))
    _raw = norm(_row.get("organism_name_raw"))
    if _row.get("scope") != "STEP" or not _matched:
        continue
    _key = (_row["case_id"], _row.get("taxid", "").strip())
    _extra = _raw[len(_matched):].strip() if _raw.startswith(_matched) and _raw != _matched else ""
    if _extra or not _row.get("taxid", "").strip():
        _GOLD_STRAIN_TAXIDS.setdefault(_key, set())
        if _extra:
            _GOLD_STRAIN_TAXIDS[_key].add(_extra)

# evidence lookup: frozen local record ids
LOOKUP = set()


def build_lookup():
    import csv as _csv
    _csv.field_size_limit(1 << 27)
    tables = [
        ("BIOSYSMOdb_Reactions_v1.0.csv", "Reaction unique ID", "utf-8-sig"),
        ("BIOSYSMOdb_Enzymes_v1.0.csv", "Enzyme-ID", "utf-8-sig"),
        ("BIOSYSMOdb_Compounds_chemical_info_v1.0.csv", "BIOSYSMO ID", "utf-8-sig"),
        ("BIOSYSMOdb_Pathways_v1.0.csv", "Unique Pathway ID", "utf-8-sig"),
        ("BIOSYSMOdb_Organisms_v1.0.csv", "Organism Name", "utf-8-sig"),
    ]
    for fname, col, enc in tables:
        path = os.path.join(SOURCE_CSV, fname)
        if not os.path.isfile(path):
            continue
        with open(path, encoding=enc, newline="") as fh:
            for row in _csv.DictReader(fh):
                value = norm(row.get(col))
                if value:
                    LOOKUP.add(value)
    for row in read_tsv(os.path.join(G1, "trait_gold.tsv")):
        if row["value_status"] == "OBSERVED":
            for v in (norm(row.get("source_record")), norm(row.get("value"))):
                if v:
                    LOOKUP.add(v)


build_lookup()


# --------------------------------------------------------------------------
# validation (independent of the D0 collector, same rules)
# --------------------------------------------------------------------------

def answer_form_status(answer):
    if answer is None:
        return "INVALID_OR_NULL"
    if isinstance(answer, dict):
        return "OBJECT"
    return "NON_OBJECT"


def extra_field_warnings(answer):
    """Extra keys at any nesting level: warnings only, text preserved."""
    warnings = []

    def walk(node, spec, path):
        if isinstance(node, dict) and isinstance(spec, dict):
            props = spec.get("properties") or {}
            for key in node:
                if props and key not in props:
                    warnings.append({"path": path, "unexpected_key": key})
                elif key in props:
                    walk(node[key], props[key].get("items")
                         if props[key].get("type") == "array" else props[key],
                         "%s/%s" % (path, key))
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, spec, "%s/%d" % (path, i))
    return warnings


# --------------------------------------------------------------------------
# alignment
# --------------------------------------------------------------------------

def comp_key(comp):
    return comp["iso"] or ("NAME:" + max(comp["names"]))


def side_set(step, side):
    return {comp_key(c) for c in step[side]}


def jac(a, b):
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / float(len(a | b))


def _gold_side(gcomps, controlled):
    """(gold key set, all-controlled?) for one side of a gold step."""
    keys = {comp_key(c) for c in gcomps}
    all_ctrl = bool(gcomps) and bool(controlled) and all(
        (c["names"] & controlled) for c in gcomps)
    return keys, all_ctrl


def _pred_side(pred_step, field, controlled, stats):
    """identity keys a prediction side provides for AUTONOMOUS matching.
    A controlled name without valid structure is counted and dropped from the
    key set (mere repetition is not autonomous evidence); any valid canonical
    SMILES always keys normally (structure is scored as usual)."""
    keys = set()
    for comp in (pred_step.get(field) or []):
        if not isinstance(comp, dict):
            continue
        role = norm(comp.get("role"))
        if role and role not in ("main",):
            continue
        iso = CHEM.canon(comp.get("smiles"))
        name = norm(comp.get("name"))
        if name and name in controlled:
            stats["repetitions"] += 1
            if not iso:
                stats["excluded"] += 1
                continue          # name-only repetition: no autonomous key
        if iso:
            keys.add(iso)
        elif name:
            keys.add("NAME:" + name)
    return keys


def align_steps(gold_steps, pred_steps, controlled=frozenset(), threshold=0.5):
    """Greedy max-Jaccard one-to-one matching; direction checked per side.

    CONTROLLED_INPUT math (teacher G2 signoff 1fa908f5):
      * a side whose gold entities are ALL disclosed controlled names and whose
        prediction carries no valid structure on that side is NEUTRAL:
        overlap = 1.0 by definition, and the side is excluded from the
        step's autonomous-evidence mean;
      * if BOTH sides are neutral the pair has zero autonomous evidence:
        score = 0.0 and can never MATCH (a mere name repetition of the whole
        step does not create a correct step);
      * a MATCH requires EVERY non-neutral side to overlap >= threshold and the
        mean of non-neutral sides >= threshold;
      * wrong or missing structure on a controlled entity's side is never
        exempted: prediction structure keeps full authority (neutral applies
        only when the prediction offers no structure at all)."""
    stats = {"repetitions": 0, "excluded": 0}
    pviews = []
    for p in pred_steps:
        pviews.append((_pred_side(p, "substrates", controlled, stats),
                       _pred_side(p, "products", controlled, stats)))
    pairs = []
    for gsid, g in sorted(gold_steps.items()):
        gsubs, gs_sub_ctrl = _gold_side(g["subs"], controlled)
        gprods, gs_prod_ctrl = _gold_side(g["prods"], controlled)
        for idx, (psubs, pprods) in enumerate(pviews):
            s_jac = 1.0 if (gs_sub_ctrl and not psubs) else jac(psubs, gsubs)
            p_jac = 1.0 if (gs_prod_ctrl and not pprods) else jac(pprods, gprods)
            s_neutral = gs_sub_ctrl and not psubs
            p_neutral = gs_prod_ctrl and not pprods
            evid = [v for v, ne in ((s_jac, s_neutral), (p_jac, p_neutral)) if not ne]
            if not evid:
                score = 0.0
            else:
                score = sum(evid) / float(len(evid))
            direction_flipped = ((not s_neutral) and (not p_neutral)
                                 and s_jac < threshold and p_jac < threshold
                                 and jac(pprods, gsubs) >= threshold
                                 and jac(psubs, gprods) >= threshold)
            if evid and score >= threshold and all(v >= threshold for v in evid):
                pairs.append((score, gsid, idx, "MATCH"))
            elif direction_flipped:
                pairs.append((0.0, gsid, idx, "DIRECTION_FLIPPED"))
    pairs.sort(key=lambda tt: (-tt[0], tt[1], tt[2]))
    used_g, used_p, matches = set(), set(), []
    for score, gsid, idx, kind in pairs:
        if kind != "MATCH" or gsid in used_g or idx in used_p:
            continue
        used_g.add(gsid)
        used_p.add(idx)
        matches.append({"gold_step": gsid, "pred_index": idx})
    flipped = [tt for tt in pairs if tt[3] == "DIRECTION_FLIPPED"
               and tt[1] not in used_g and tt[2] not in used_p]
    extras = [i for i in range(len(pred_steps)) if i not in used_p]
    missing = [g for g in gold_steps if g not in used_g]
    return {"matches": matches, "extra_pred_steps": extras,
            "missing_gold_steps": missing, "direction_flipped": len(flipped),
            "controlled_stats": stats}


def side_set_from_pred(pred_step, field):
    keys = set()
    for comp in (pred_step.get(field) or []):
        if not isinstance(comp, dict):
            continue
        role = norm(comp.get("role"))
        if role and role not in ("main",):
            continue
        iso = CHEM.canon(comp.get("smiles"))
        if iso:
            keys.add(iso)
        else:
            name = norm(comp.get("name"))
            if name:
                keys.add("NAME:" + name)
    return keys


def gold_step_identity_keys(gstep, side):
    keys = set()
    for comp in gstep[side]:
        keys.add(comp_key(comp))
    return keys


def pred_comp_names(pred_step, field):
    out = set()
    for comp in (pred_step.get(field) or []):
        if isinstance(comp, dict):
            role = norm(comp.get("role"))
            if role and role != "main":
                continue
            name = norm(comp.get("name"))
            if name:
                out.add(name)
    return out


def pred_comp_smiles(pred_step, field):
    out = []
    for comp in (pred_step.get(field) or []):
        if isinstance(comp, dict):
            role = norm(comp.get("role"))
            if role and role != "main":
                continue
            out.append((norm(comp.get("name")), CHEM.canon(comp.get("smiles")),
                        CHEM.canon(comp.get("smiles"), achiral=True)))
    return out


# --------------------------------------------------------------------------
# profile / trait helpers
# --------------------------------------------------------------------------

def pred_profiles(answer):
    out = {}
    for prof in (answer.get("organism_profiles") or []):
        if not isinstance(prof, dict):
            continue
        taxid = str(prof.get("ncbi_taxid") or "").strip()
        name = norm(prof.get("organism_name"))
        key = taxid or name
        out[key] = {"taxid": taxid, "name": name, "raw": prof}
    return out


def score_traits(case, answer, matched_taxids=None):
    profiles = GOLD.profiles[case]
    if matched_taxids is not None:
        profiles = {k: v for k, v in profiles.items()
                    if (v.get("taxid") or k) in matched_taxids}
    pred = pred_profiles(answer)
    item_scores, completeness, subfield_scores = [], [], []
    text_total = text_correct = 0
    for key, prof in sorted(profiles.items()):
        taxid = prof["taxid"] or key
        p = pred.get(taxid) or pred.get(prof["name"])
        traits = (p or {}).get("raw", {}).get("traits") or {}
        gold_vals = GOLD.item_values[case]
        score_keys = [k for k in GOLD.scoreable_items[case] if k[0] == taxid]
        answered = 0
        correct_cells = 0
        scoreable_present = 0
        # Teacher D1 (FROZEN 2026-09-28, approval 1fa908f5): numeric accuracy
        # contains only cells explicitly scoreable in the numeric/sub-field
        # mask. For F2/F3/F4 the sub-field mask below is the authoritative
        # denominator; item-level cells of these traits are excluded from the
        # numeric accuracy, and their observed preference/category WORDS are
        # reported separately as text_coverage (option B: excluded, not reweighted).
        # Teacher D5: F14 genome accuracy compares ONLY against genome accessions
        # via the single formal source traits.F14.value.genome_accession; profile
        # identity tokens in the gold item values are not genome claims.
        for tax, trait in score_keys:
            cell = _get_cell(traits, trait)
            raw = cell.get("value") if isinstance(cell, dict) else None
            gold_set = set(gold_vals.get((tax, trait), set()))
            parts = _pred_parts(raw)
            if parts:
                answered += 1
            if trait in ("F2", "F3", "F4"):
                word_gold = {v for v in gold_set if not _numeric(v)}
                if word_gold:
                    text_total += 1
                    if parts & word_gold:
                        text_correct += 1
                continue
            if trait == "F14":
                acc_gold = {v for v in gold_set if _ACCESSION_RE.match(v)}
                if not acc_gold:
                    continue
                formal = ""
                if isinstance(raw, dict):
                    formal = norm(raw.get("genome_accession") or "")
                parts = {formal} if formal else set()
                gold_set = acc_gold
            if not gold_set:
                continue
            scoreable_present += 1
            if parts and any(value_matches(x, gold_set) for x in parts):
                correct_cells += 1
        def cell_answered(t):
            cell = traits.get(t) if isinstance(traits.get(t), dict) else {}
            raw = cell.get("value")
            if isinstance(raw, dict):
                return any(v not in (None, "") for v in raw.values())
            if isinstance(raw, list):
                return bool(raw)
            return bool(norm(raw)) and norm(raw).lower() not in ("na", "n/a", "no robust majority")
        all_traits = sum(1 for t in TRAITS if cell_answered(t))
        completeness.append(all_traits / float(len(TRAITS)))
        if scoreable_present:
            item_scores.append(correct_cells / float(scoreable_present))
        for trait in ("F2", "F3", "F4"):
            sf_keys = [k for k in GOLD.scoreable_subfields[case]
                       if k[0] == taxid and k[1] == trait]
            if not sf_keys:
                continue
            ok = 0
            for tax, tr, target in sf_keys:
                cell = traits.get(tr) if isinstance(traits.get(tr), dict) else {}
                raw_val = cell.get("value")
                if isinstance(raw_val, dict):
                    value = norm(raw_val.get(target))
                elif isinstance(raw_val, str):
                    value = norm(raw_val)
                else:
                    value = ""
                if value and value_matches(value,
                                           GOLD.subfield_values[case].get(
                                               (tax, tr, target), set())):
                    ok += 1
            subfield_scores.append(ok / float(len(sf_keys)))
    item = sum(item_scores) / len(item_scores) if item_scores else None
    subf = sum(subfield_scores) / len(subfield_scores) if subfield_scores else None
    comp = sum(completeness) / len(completeness) if completeness else None
    return {"item_accuracy": item, "subfield_accuracy": subf,
            "completeness": comp,
            "text_coverage": (text_correct / float(text_total)) if text_total else None,
            "text_coverage_cells": text_total,
            "profiles_scored": len(profiles)}


def score_layers(case, answer):
    gold_steps = GOLD.steps[case]
    pred_steps = [s for s in (answer.get("steps") or []) if isinstance(s, dict)]
    # extra steps placed in downstream_continuation are not penalized
    controlled = frozenset(CONTROLLED.get(case, set()))
    align = align_steps(gold_steps, pred_steps, controlled)
    n_gold = len(gold_steps) or 1
    n_pred = len(pred_steps)
    recall = len(align["matches"]) / float(n_gold)
    precision = (len(align["matches"]) / float(len(align["matches"]) + len(align["extra_pred_steps"]))
                 if (align["matches"] or align["extra_pred_steps"]) else 1.0)
    if not align["matches"]:
        order = 0.0
        matched_orders_g = []
    else:
        pass
    matched_orders_g = [gold_steps[m["gold_step"]]["order"] for m in align["matches"]]
    matched_orders_p = [pred_steps[m["pred_index"]].get("order") for m in align["matches"]]
    if align["matches"]:
        order = 1.0
        pairs = list(zip(matched_orders_g, matched_orders_p))
        if len(pairs) > 1:
            concordant = sum(1 for i in range(len(pairs)) for j in range(i + 1, len(pairs))
                             if (pairs[i][0] < pairs[j][0]) == (
                                 (pairs[i][1] or 0) < (pairs[j][1] or 0)))
            total = len(pairs) * (len(pairs) - 1) / 2.0
            order = concordant / total if total else 1.0
    pathway = 100.0 * (recall + precision + order) / 3.0

    # SMILES layer: per matched step, main compound structure equality
    iso_ok = iso_total = ach_ok = 0
    for m in align["matches"]:
        g = gold_steps[m["gold_step"]]
        p = pred_steps[m["pred_index"]]
        for side, gkey, pkey in (("substrates", "subs", "substrates"),
                                 ("products", "prods", "products")):
            gcomps = g[gkey]
            for comp in gcomps:
                for pname, piso, pach in pred_comp_smiles(p, pkey):
                    names_hit = pname in comp["names"] or (
                        comp_key(comp) == (piso or ("NAME:" + pname)))
                    if names_hit or (piso and piso == comp["iso"]):
                        iso_total += 1
                        ach_total = iso_total  # counted below
                        if piso and piso == comp["iso"]:
                            iso_ok += 1
                            if comp.get("achiral") and pach and comp["achiral"] == pach:
                                ach_ok += 1
                        break
    smiles_score = 100.0 * iso_ok / iso_total if iso_total else 0.0
    smiles_achiral = 100.0 * ach_ok / iso_total if iso_total else 0.0

    # Enzyme layer
    e_scores = []
    identity_conflicts = 0
    for sid in sorted(gold_steps):
        matched = next((m for m in align["matches"] if m["gold_step"] == sid), None)
        names_ok = ec_ok = pair_ok = 0.0
        if matched:
            p = pred_steps[matched["pred_index"]]
            enz = p.get("enzyme") or {}
            org = p.get("microorganism") or {}
            pred_name = norm(enz.get("name")) if isinstance(enz, dict) else ""
            names_ok = 1.0 if pred_name and pred_name in GOLD.enzymes[case].get(sid, set()) else 0.0
            ec = norm(enz.get("ec_number")) if isinstance(enz, dict) else ""
            gold_ecs = GOLD.enzyme_ec[case].get(sid, set())
            ec_ok = 1.0 if ((None if not ec else ec) in gold_ecs) else 0.0
            org_taxid = str(org.get("ncbi_taxid") or "").strip() if isinstance(org, dict) else ""
            org_name = norm(org.get("organism_name") if isinstance(org, dict) else "") or \
                (norm((GOLD.profiles[case].get(org_taxid) or {}).get("name", ""))
                 if org_taxid and org_taxid in GOLD.profiles[case] else "")
            accepted_org = GOLD.step_organisms[case].get(sid, set())
            tax_match = bool(org_taxid) and org_taxid in accepted_org
            name_match = bool(org_name) and org_name in accepted_org
            # Teacher D2 (FROZEN): pair credit on accepted species/strain NAME
            # match; an ACTIVE WRONG TaxID makes the pair wrong and raises
            # IDENTITY_CONFLICT even when the name matches; TaxID=null is a
            # recall miss only and the pair may still earn name credit.
            if org_taxid:
                pair_ok = 1.0 if (tax_match and (not org_name or name_match)) else 0.0
                if (not tax_match) and name_match:
                    identity_conflicts += 1
            else:
                pair_ok = 1.0 if name_match else 0.0
        e_scores.append((names_ok, ec_ok, pair_ok))
    enzyme = 100.0 * sum(sum(t) for t in e_scores) / (3.0 * len(e_scores)) if e_scores else 0.0

    # Microbial identity layer: scored over the organisms the answer was asked
    # to prefer -- one per matched gold step (gold keeps alternatives; the
    # model returns one preferred pairing). Not a demand to list every
    # accepted organism of the pathway.
    profiles = GOLD.profiles[case]
    pred = pred_profiles(answer)
    accepted_by_step = {}
    for sid in gold_steps:
        names = {norm(o) for o in
                 [c for c in GOLD.step_organisms[case].get(sid, set())]}
        accepted_by_step[sid] = names
    sub_vals = []
    genome_conflicts = 0
    for m in align["matches"]:
        sid = m["gold_step"]
        p_step = pred_steps[m["pred_index"]]
        org = p_step.get("microorganism") or {}
        accepted = GOLD.step_organisms[case].get(sid, set())
        pred_taxid = str(org.get("ncbi_taxid") or "").strip() if isinstance(org, dict) else ""
        pred_name = norm(org.get("organism_name")) if isinstance(org, dict) else ""
        gold_prof = None
        for key, prof in profiles.items():
            if (prof["taxid"] and prof["taxid"] == pred_taxid) \
                    or norm(prof["name"]) == pred_name:
                if norm(prof["name"]) in accepted or prof["taxid"] in accepted:
                    gold_prof = prof
                    break
        name_ok = 1.0 if gold_prof and pred_name == norm(gold_prof["name"]) else 0.0
        tax_ok = 1.0 if gold_prof and pred_taxid and pred_taxid == gold_prof["taxid"] else 0.0
        prof = gold_prof or {"genome": "", "name": pred_name, "taxid": ""}
        p = pred.get(prof["taxid"]) or pred.get(prof["name"])
        raw = (p or {}).get("raw") or {}
        gen_ok = None
        if prof["genome"]:
            # Teacher D5 (FROZEN): the ONLY formal genome source is
            # traits.F14.value.genome_accession. A profile-level compatibility
            # field must agree with it or it is a CONFLICT; it can never act as
            # a second source of truth and can never earn credit by itself.
            f14 = _get_cell(raw.get("traits") or {}, "F14")
            formal = ""
            if isinstance(f14.get("value"), dict):
                formal = norm(f14["value"].get("genome_accession") or "")
            compat = norm(raw.get("genome_accession") or raw.get("ncbi_genome_accession") or "")
            if compat and (not formal or compat != formal):
                genome_conflicts += 1
                gen_ok = 0.0
            else:
                gen_ok = 1.0 if formal and formal == norm(prof["genome"]) else 0.0
        strain = norm(raw.get("strain")) if p else ""
        strain_tokens = _GOLD_STRAIN_TAXIDS.get((case, prof.get("taxid", "")), set())
        if not strain_tokens:
            strain_ok = None
        elif p and strain and any(tok in strain for strain_tok in [strain]
                                  for tok in strain_tokens
                                  if tok in strain or strain == tok):
            strain_ok = 1.0
        else:
            strain_ok = 0.0
        sub_vals.append([v for v in (name_ok, tax_ok, gen_ok, strain_ok) if v is not None])
    total_sub = sum(len(v) for v in sub_vals)
    microbial = 100.0 * sum(sum(v) for v in sub_vals) / total_sub if total_sub else 0.0

    matched_taxids = set()
    for m in align["matches"]:
        sid = m["gold_step"]
        p_step = pred_steps[m["pred_index"]]
        org = p_step.get("microorganism") or {}
        if isinstance(org, dict) and org.get("ncbi_taxid"):
            matched_taxids.add(str(org["ncbi_taxid"]).strip())
    traits = score_traits(case, answer, matched_taxids)
    # Teacher D1 (FROZEN): the 10% trait layer is the numeric accuracy over the
    # mask-defined numeric cells only -- mean(item_accuracy[non F2/F3/F4],
    # subfield_accuracy[F2/F3/F4 min/max consensus scalars]), equal-weighted
    # where present. completeness and text_coverage are reported separately and
    # never mixed into the numeric layer (no reweighting).
    parts = [v for v in (traits["item_accuracy"], traits["subfield_accuracy"])
             if v is not None]
    traits_score = 100.0 * (sum(parts) / len(parts) if parts else 0.0)

    science = (LAYERS["pathway"] * pathway + LAYERS["smiles"] * smiles_score +
               LAYERS["enzyme"] * enzyme + LAYERS["microbial_identity"] * microbial +
               LAYERS["traits"] * traits_score)
    return {
        "layers": {"pathway": round(pathway, 2), "smiles": round(smiles_score, 2),
                   "enzyme": round(enzyme, 2),
                   "microbial_identity": round(microbial, 2),
                   "traits": round(traits_score, 2)},
        "science_100": round(science, 2),
        "alignment": align,
        "smiles_achiral_reference": round(smiles_achiral, 2),
        "identity_conflicts": identity_conflicts,
        "genome_conflicts": genome_conflicts,
        "controlled_input": {
            "mask_rows_total": CONTROLLED_META["rows"],
            "mask_cases_total": CONTROLLED_META["cases"],
            "disclosed_atoms_in_case": len(controlled),
            "controlled_name_repetitions": align["controlled_stats"]["repetitions"],
            "controlled_name_recall_excluded": align["controlled_stats"]["excluded"]},
        "traits_detail": traits,
    }


# --------------------------------------------------------------------------
# evidence + abstention axes
# --------------------------------------------------------------------------

def record_resolves(rec_id):
    return norm(rec_id) in LOOKUP


def score_evidence(case, answer, gold_result):
    """Evidence axis over the WHOLE answer, not only matched steps: a fake
    DATABASE_DIRECT record_id is a hallucination wherever it appears."""
    registry = {e.get("evidence_id"): e for e in (answer.get("evidence_registry") or [])
                if isinstance(e, dict)}
    stats = {"verified_correct": 0, "unverified_correct": 0,
             "evidence_hallucination": 0, "ref_missing": 0,
             "model_inference": 0, "internal_knowledge": 0}
    step_ids = {s.get("step_id") for s in (answer.get("steps") or [])
                if isinstance(s, dict)}
    profile_ids = {p.get("organism_profile_id") for p in (answer.get("organism_profiles") or [])
                   if isinstance(p, dict)}
    for evid, entry in sorted(registry.items(), key=lambda kv: str(kv[0])):
        stype = norm(entry.get("source_type"))
        if stype == "model_inference":
            stats["model_inference"] += 1
            continue
        if stype == "internal_knowledge_only":
            stats["internal_knowledge"] += 1
            continue
        if stype == "database_direct":
            resolves = record_resolves(entry.get("record_id"))
            scopes = entry.get("claim_scope") or []
            claim_ok = True
            gold_sid_norms = {norm(s) for s in GOLD.steps[case]}
            answer_sid_norms = {norm(s) for s in step_ids if s}
            for scope in scopes:
                token = norm(scope)
                if token.startswith("step:"):
                    remainder = token[len("step:"):]
                    sid_part = remainder.split(".")[0]
                    if sid_part and sid_part not in gold_sid_norms \
                            and sid_part not in answer_sid_norms:
                        claim_ok = False
            if resolves and claim_ok:
                stats["verified_correct"] += 1
            else:
                stats["evidence_hallucination"] += 1
            continue
        stats["unverified_correct"] += 1
    # dangling references inside the answer
    known_ids = set(registry)
    for s in (answer.get("steps") or []):
        if not isinstance(s, dict):
            continue
        refs = [s.get("reaction_evidence_id")]
        for part in (s.get("enzyme"), s.get("microorganism")):
            if isinstance(part, dict):
                refs.append(part.get("evidence_id"))
        for ref in refs:
            if ref and ref not in known_ids:
                stats["ref_missing"] += 1
    return stats


def score_abstention(case, answer, gold_result):
    """null = recall miss only; a WRONG non-null value answered with high
    confidence and without resolvable evidence = overclaim."""
    nulls = 0
    overclaims = 0
    matched_map = {m["gold_step"]: m["pred_index"]
                   for m in gold_result["alignment"]["matches"]}
    matched_pred = set(matched_map.values())
    pred_steps = [s for s in (answer.get("steps") or []) if isinstance(s, dict)]
    registry = {e.get("evidence_id"): e for e in (answer.get("evidence_registry") or [])
                if isinstance(e, dict)}

    def evidence_verifiable(ref):
        entry = registry.get(ref)
        if not entry:
            return False
        if norm(entry.get("source_type")) != "database_direct":
            return False
        return record_resolves(entry.get("record_id"))

    def fact(value, confidence, ref, correct):
        nonlocal nulls, overclaims
        if value in (None, ""):
            nulls += 1
            return
        if not correct and norm(confidence) == "high" and not evidence_verifiable(ref):
            overclaims += 1

    for idx, p in enumerate(pred_steps):
        sid = None
        for gsid, pi in matched_map.items():
            if pi == idx:
                sid = gsid
                break
        enz = p.get("enzyme") or {}
        if isinstance(enz, dict):
            pred_name = norm(enz.get("name"))
            correct = bool(sid) and pred_name in GOLD.enzymes[case].get(sid, set())
            fact(enz.get("name"), enz.get("confidence"), enz.get("evidence_id"), correct)
        org = p.get("microorganism") or {}
        if isinstance(org, dict):
            org_taxid = str(org.get("ncbi_taxid") or "").strip()
            org_name = norm(org.get("organism_name"))
            accepted = GOLD.step_organisms[case].get(sid, set()) if sid else set()
            correct = bool(sid) and (org_taxid in accepted or org_name in accepted)
            fact(org.get("ncbi_taxid") or org.get("organism_name"),
                 org.get("confidence"), org.get("evidence_id"), correct)
    missing = len(GOLD.steps[case]) - len(matched_map)
    return {"null_abstentions": nulls, "overclaims": overclaims,
            "gold_steps_recall_missed": max(0, missing)}


def score_answer(case_id, answer, parse_status="VALID"):
    result = {
        "case_id": case_id,
        "engineering": {"json_parse_status": parse_status,
                        "answer_form": answer_form_status(answer),
                        "extra_field_warnings": 0},
    }
    if not isinstance(answer, dict):
        result["layers"] = {k: 0.0 for k in
                            ("pathway", "smiles", "enzyme", "microbial_identity", "traits")}
        result["science_100"] = 0.0
        result["alignment"] = {"matches": [], "extra_pred_steps": [],
                               "missing_gold_steps": sorted(GOLD.steps[case_id]),
                               "direction_flipped": 0}
        return result
    layers = score_layers(case_id, answer)
    layers["evidence_axis"] = score_evidence(case_id, answer, layers)
    layers["abstention_axis"] = score_abstention(case_id, answer, layers)
    result.update(layers)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", required=True, help="mock answer JSON file")
    parser.add_argument("--case", required=True)
    parser.add_argument("--controlled-mask", default=None,
                        help="override controlled_input_scoring_mask.tsv path (validator probes)")
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)
    if args.controlled_mask:
        load_controlled_mask(args.controlled_mask)
    with open(args.mock, encoding="utf-8") as fh:
        answer = json.load(fh)
    result = score_answer(args.case, answer)
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
