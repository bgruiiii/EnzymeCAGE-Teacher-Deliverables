#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
route_checker_r1.py -- LIKERT V0.5 确定性路线对齐检查器（R1窄修版）

R0→R1修复（对应审计F01/F02/F07/F08，反例见
04_Local_Review_Audits/LIKERT_V05_REVISION_20261105/R0_RETURN_REVIEW/review_reproductions.py）：

F01 反转证明：
  * 禁止平均反向亲和≥t即升级确定反转。确定反转仅限严格层（G3冻结键）双侧反向重合≥t且
    正向<t（DIRECTION_FLIPPED_STRICT）。
  * 松弛层（stereo_blind/charge_blind/both_blind/tautomer）反向双侧命中=REVERSAL_CANDIDATE_*
    （UNKNOWN边界）——与正向同层政策对称（F08）：正向松弛等价不升MATCH，反向松弛等价也不升确认。
  * 单端点重合=ONE_SIDED_REVERSAL_CLUE，仅入候选线索表，不绑定目标步、不改步骤状态。
  * 整链反转CONFIRMED需：≥max(2,ceil(n_req/2))个严格层确定反转步 + 预测图连通 +
    （端点流交换证据 或 反转步=全部绑定关系）。整链反转CANDIDATE_STRONG需：matched=0 +
    （≥2双侧候选(任意层) 或 ≥1双侧候选+端点流交换）+ 连通 → BOUNDARY_REVIEW优先复核旗。
F02 跨题与绑定：
  * 跨题签名命中=检索线索（OTHER_ROUTE_SIGNATURE_CLUE），只按预测步记录一次，不广播为多个
    目标步的独占配对，不单独作为偏离证据。
  * 确认替换仅两种：ENTRY_DIVERGENCE（预测入口步与gold入口步底物双侧≥t而产物双侧<t，
    同一污染物投喂不同转化）与POSITIONAL（预测步已绑定邻域=gold步已绑定邻域）。一对一独占。
  * 额外步分类顺序：背景步匹配 → 终点后下游（先于跨题检索，DOWNSTREAM修复）→ 跨题线索 → 未匹配。
F07 任务条件层（与化学对齐层分离输出）：
  * 氧条件独立核对：scope氧(题面)非null且答案非null且不同→TASK_VIOLATION_OXYGEN_MISMATCH；
    scope氧null→NO_INFERENCE不猜值；答案null→记录不判违背。
  * 路线名照抄核对→TASK_ROUTE_NAME_*（D1消费；照抄正确不等于内容正确）。
  * task_conformance_status与route_status(化学层)分开；组合列task_and_route_status。
F08 表示差异正交分层（多标签）：
  * 立体识别用RDKit真实手性标签+双键立体（E/Z），不再用'@'字符串。
  * stereo_blind(保电荷) / charge_blind(保立体) / both_blind / tautomer 四层分别判等；
    仅both_blind相等=MIXED_CHARGE_AND_STEREO，绝不叫"纯电荷差异"。
  * 双侧显式立体不同（含E/Z）=STEREO_CONFLICT_SPECIFIED（确认NONMATCH，真实化学差异）；
    单侧未标=STEREO_UNSPECIFIED/ADDED_ONE_SIDE（UNKNOWN）。
  * 名称命名空间：路线对齐只用化合物名（gold identity_name/db_cmpdname/aligned_token vs
    答案底物/产物name）；酶名同义词属P2 accepted集合层，绝不混入。
确定性：无随机、排序稳定、RDKit 2026.03.5、重复运行逐字节一致。阈值0.5=G3历史判据仅初查，
正式阈值待DR-01；输出全部标DRAFT_DIAGNOSTIC。
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict

from rdkit import Chem as _C
from rdkit.Chem.MolStandardize import rdMolStandardize
import rdkit as _rdkit

RDKIT_VERSION = _rdkit.__version__
_UNCHARGER = rdMolStandardize.Uncharger()
_TAUT = rdMolStandardize.TautomerEnumerator()

_CACHE = {}
_TAUT_CACHE = {}
_STEREO_CACHE = {}


def canon(smiles, achiral=False, uncharged=False):
    if not smiles or not isinstance(smiles, str):
        return None
    key = (smiles.strip(), bool(achiral), bool(uncharged))
    if key in _CACHE:
        return _CACHE[key]
    out = None
    try:
        mol = _C.MolFromSmiles(smiles.strip())
        if mol is not None:
            if uncharged:
                try:
                    mol = _UNCHARGER.uncharge(mol)
                except Exception:
                    pass
            if achiral:
                mol = _C.MolFromSmiles(_C.MolToSmiles(mol))
                if mol is not None:
                    _C.RemoveStereochemistry(mol)
            out = _C.MolToSmiles(mol) if mol is not None else None
    except Exception:
        out = None
    _CACHE[key] = out
    return out


def stereo_specified(smiles):
    """RDKit真实立体识别：手性原子标签+双键立体(E/Z)，非'@'字符串。"""
    if not smiles or not isinstance(smiles, str):
        return False
    s = smiles.strip()
    if s in _STEREO_CACHE:
        return _STEREO_CACHE[s]
    out = False
    try:
        mol = _C.MolFromSmiles(s)
        if mol is not None:
            for a in mol.GetAtoms():
                tag = a.GetChiralTag()
                if tag != _C.ChiralType.CHI_UNSPECIFIED:
                    out = True
                    break
            if not out:
                for b in mol.GetBonds():
                    st = b.GetStereo()
                    if st != _C.BondStereo.STEREONONE:
                        out = True
                        break
    except Exception:
        out = False
    _STEREO_CACHE[s] = out
    return out


def tautomer_canon(smiles):
    if not smiles or not isinstance(smiles, str):
        return None
    s = smiles.strip()
    if s in _TAUT_CACHE:
        return _TAUT_CACHE[s]
    out = None
    try:
        mol = _C.MolFromSmiles(s)
        if mol is not None:
            try:
                mol = _UNCHARGER.uncharge(mol)
            except Exception:
                pass
            _C.RemoveStereochemistry(mol)
            out = _C.MolToSmiles(_TAUT.Canonicalize(mol))
    except Exception:
        out = None
    _TAUT_CACHE[s] = out
    return out


def norm(text):
    if text is None:
        return ""
    if not isinstance(text, str):
        text = json.dumps(text, sort_keys=True) if isinstance(text, (dict, list)) else str(text)
    return " ".join(text.strip().lower().split())


def jac(a, b):
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / float(len(a | b))


def containment(a, b):
    """|a∩b|/|b|（b为参照侧）；b空→0。"""
    if not b:
        return 0.0
    return len(set(a) & set(b)) / float(len(set(b)))


LAYER_ATTRS = ("iso", "stereo_blind", "charge_blind", "both_blind", "taut")


class GoldCompound:
    __slots__ = ("compound_id", "names", "iso", "stereo_blind", "charge_blind",
                 "both_blind", "taut", "stereo_specified", "key")

    def __init__(self, compound_id, names, isosmiles):
        self.compound_id = compound_id
        self.names = {n for n in (norm(x) for x in names) if n}
        self.iso = canon(isosmiles)
        self.stereo_blind = canon(isosmiles, achiral=True) if self.iso else None
        self.charge_blind = canon(isosmiles, uncharged=True) if self.iso else None
        self.both_blind = canon(isosmiles, achiral=True, uncharged=True) if self.iso else None
        self.taut = tautomer_canon(isosmiles) if self.iso else None
        self.stereo_specified = stereo_specified(isosmiles) if self.iso else False
        self.key = self.iso or ("NAME:" + max(self.names) if self.names else None)


class PredCompound:
    __slots__ = ("name", "raw_smiles", "iso", "stereo_blind", "charge_blind",
                 "both_blind", "taut", "stereo_specified", "key", "parseable")

    def __init__(self, name, smiles):
        self.name = norm(name)
        self.raw_smiles = (smiles or "").strip() if isinstance(smiles, str) else ""
        self.iso = canon(self.raw_smiles)
        self.parseable = bool(self.raw_smiles) and self.iso is not None
        self.stereo_blind = canon(self.raw_smiles, achiral=True) if self.raw_smiles else None
        self.charge_blind = canon(self.raw_smiles, uncharged=True) if self.raw_smiles else None
        self.both_blind = canon(self.raw_smiles, achiral=True, uncharged=True) if self.raw_smiles else None
        self.taut = tautomer_canon(self.raw_smiles) if self.raw_smiles else None
        self.stereo_specified = stereo_specified(self.raw_smiles) if self.raw_smiles else False
        self.key = self.iso or ("NAME:" + self.name if self.name else None)


class GoldStep:
    def __init__(self, sid, reaction_id, order, branch, preds, succs, orientation,
                 arrow_class, subs, prods):
        self.sid = sid
        self.reaction_id = reaction_id
        self.order = order
        self.branch = branch
        self.preds = preds
        self.succs = succs
        self.orientation = orientation
        self.arrow_class = arrow_class
        self.subs = subs
        self.prods = prods

    @property
    def ref_gap(self):
        return any(c.iso is None for c in self.subs + self.prods)

    def sig(self):
        sk = frozenset(c.key for c in self.subs if c.key)
        pk = frozenset(c.key for c in self.prods if c.key)
        return (sk, pk) if (sk or pk) else None


class PredStep:
    def __init__(self, index, step_id, order, preds, subs, prods, raw):
        self.index = index
        self.step_id = step_id
        self.order = order
        self.preds = preds
        self.subs = subs
        self.prods = prods
        self.raw = raw

    def sig(self):
        sk = frozenset(c.key for c in self.subs if c.key)
        pk = frozenset(c.key for c in self.prods if c.key)
        return (sk, pk) if (sk or pk) else None

    @property
    def has_any_structure(self):
        return any(c.parseable for c in self.subs + self.prods)


def parse_pred_steps(answer):
    out = []
    steps = answer.get("steps")
    if not isinstance(steps, list):
        return out, "NO_STEPS_KEY"
    dicts = [s for s in steps if isinstance(s, dict)]
    if not dicts:
        return out, "EMPTY_STEPS"
    for i, s in enumerate(dicts):
        subs, prods = [], []
        for field, bucket in (("substrates", subs), ("products", prods)):
            for comp in (s.get(field) or []):
                if not isinstance(comp, dict):
                    continue
                role = norm(comp.get("role"))
                if role and role not in ("main",):
                    continue
                bucket.append(PredCompound(comp.get("name"), comp.get("smiles")))
        preds = [str(x) for x in (s.get("predecessor_step_ids") or []) if str(x).strip()]
        try:
            order = int(s.get("order"))
        except (TypeError, ValueError):
            order = None
        out.append(PredStep(i, str(s.get("step_id") or "IDX%d" % i), order, preds,
                            subs, prods, s))
    return out, "OK"


# ------------------------------------------------------------ side keys ----

def gold_side(gstep, side, controlled):
    comps = gstep.subs if side == "subs" else gstep.prods
    keys = {c.key for c in comps if c.key}
    all_ctrl = bool(comps) and bool(controlled) and all(
        (c.names & controlled) for c in comps)
    return keys, all_ctrl


def pred_side_keys(pstep, side, controlled, stats):
    comps = pstep.subs if side == "subs" else pstep.prods
    keys = set()
    for c in comps:
        if c.name and c.name in controlled:
            stats["repetitions"] += 1
            if not c.parseable:
                stats["excluded"] += 1
                continue
        if c.key:
            keys.add(c.key)
    return keys


def side_keys_layer(gstep, pstep, side, layer):
    gcomps = gstep.subs if side == "subs" else gstep.prods
    pcomps = pstep.subs if side == "subs" else pstep.prods
    gk, pk = set(), set()
    for c in gcomps:
        v = getattr(c, layer)
        gk.add(v if v else ("NAME:" + (max(c.names) if c.names else "GAP:%s" % c.compound_id)))
    for c in pcomps:
        v = getattr(c, layer)
        pk.add(v if v else ("NAME:" + (c.name or "PRED_NULL")))
    return {x for x in gk if x}, {x for x in pk if x}


def layer_jacs(gstep, pstep, layer, threshold, controlled):
    """返回(fwd_ok, s_jac, p_jac, flip_ok)——同一层正向/反向对称评估。"""
    stats = {"repetitions": 0, "excluded": 0}
    if layer == "iso":
        g_subs, sub_ctrl = gold_side(gstep, "subs", controlled)
        g_prods, prod_ctrl = gold_side(gstep, "prods", controlled)
        p_subs = pred_side_keys(pstep, "subs", controlled, stats)
        p_prods = pred_side_keys(pstep, "prods", controlled, stats)
    else:
        gs, ps = side_keys_layer(gstep, pstep, "subs", layer)
        gp, pp = side_keys_layer(gstep, pstep, "prods", layer)
        g_subs0, sub_ctrl = gold_side(gstep, "subs", controlled)
        g_prods0, prod_ctrl = gold_side(gstep, "prods", controlled)
        g_subs = {k for k in g_subs0 if k.startswith("NAME:")} | gs
        g_prods = {k for k in g_prods0 if k.startswith("NAME:")} | gp
        p_subs0 = pred_side_keys(pstep, "subs", controlled, stats)
        p_prods0 = pred_side_keys(pstep, "prods", controlled, stats)
        p_subs = {k for k in p_subs0 if k.startswith("NAME:")} | ps
        p_prods = {k for k in p_prods0 if k.startswith("NAME:")} | pp
    s_j = 1.0 if (sub_ctrl and not p_subs) else jac(p_subs, g_subs)
    p_j = 1.0 if (prod_ctrl and not p_prods) else jac(p_prods, g_prods)
    s_neutral = sub_ctrl and not p_subs
    p_neutral = prod_ctrl and not p_prods
    evid = [v for v, ne in ((s_j, s_neutral), (p_j, p_neutral)) if not ne]
    fwd_ok = bool(evid) and all(v >= threshold for v in evid) and \
        (sum(evid) / float(len(evid))) >= threshold
    r1 = jac(p_prods, g_subs)
    r2 = jac(p_subs, g_prods)
    flip_ok = (s_j < threshold and p_j < threshold
               and r1 >= threshold and r2 >= threshold)
    return fwd_ok, s_j, p_j, flip_ok, (r1, r2)


def _pair_side(gc_list, pc_list):
    """同侧稳定配对（R2-02）：键优先级 iso>charge_blind>stereo_blind>both_blind；
    同层多成员无法唯一配对→AMBIGUOUS。"""
    labels = set()
    used_g = set()
    for pc in pc_list:
        matches = []
        for gi, gc in enumerate(gc_list):
            if gi in used_g:
                continue
            if gc.iso and pc.iso and gc.iso == pc.iso:
                matches.append((0, gi, gc))
            elif gc.charge_blind and pc.charge_blind and gc.charge_blind == pc.charge_blind:
                matches.append((1, gi, gc))
            elif gc.stereo_blind and pc.stereo_blind and gc.stereo_blind == pc.stereo_blind:
                matches.append((2, gi, gc))
            elif gc.both_blind and pc.both_blind and gc.both_blind == pc.both_blind:
                matches.append((3, gi, gc))
        if not matches:
            continue
        best = min(m[0] for m in matches)
        bestm = [m for m in matches if m[0] == best]
        if len(bestm) > 1:
            labels.add("AMBIGUOUS_IDENTITY_PAIRING")
            continue
        _, gi, gc = bestm[0]
        used_g.add(gi)
        if best == 0:
            continue
        g_st, p_st = gc.stereo_specified, pc.stereo_specified
        # same_stereo_layer（去立体后相等）→差异只在立体；same_charge_layer（去电荷后
        # 相等）→差异只在电荷。
        same_charge_layer = (gc.charge_blind == pc.charge_blind)
        same_stereo_layer = (gc.stereo_blind == pc.stereo_blind)
        if same_stereo_layer and not same_charge_layer:
            labels.add("STEREO_CONFLICT_SPECIFIED" if (g_st and p_st)
                       else ("STEREO_UNSPECIFIED_ONE_SIDE" if (g_st and not p_st)
                             else "STEREO_ADDED_ONE_SIDE" if (p_st and not g_st)
                             else "STEREO_LAYER_DIFF_UNCHARACTERIZED"))
        elif same_charge_layer and not same_stereo_layer:
            labels.add("CHARGE_NOTATION_ONLY")
        elif not same_stereo_layer and not same_charge_layer:
            labels.add("REPRESENTATION_MIXED_CHARGE_AND_STEREO")
            if g_st and p_st:
                labels.add("STEREO_CONFLICT_SPECIFIED")
            elif g_st and not p_st:
                labels.add("STEREO_UNSPECIFIED_ONE_SIDE")
            elif p_st and not g_st:
                labels.add("STEREO_ADDED_ONE_SIDE")
        else:
            if gc.taut is not None and pc.taut is not None and gc.taut == pc.taut:
                labels.add("TAUTOMER_CANDIDATE")
            else:
                labels.add("CONSTITUTIONAL_REMAINS_UNEXPLAINED")
    return labels


def representation_labels(gstep, pstep):
    """同侧、同身份稳定配对后的差异多标签（R2-02：禁止跨底物/产物侧笛卡尔积比较）。"""
    return (_pair_side(gstep.subs, pstep.subs) | _pair_side(gstep.prods, pstep.prods)) \
        or {"NO_COMPOUND_PAIR_ANALYZABLE"}


RELATION_CLASS = {  # 关系→(状态, 类别秩, 确认性)
    "DIRECTION_FLIPPED_STRICT": ("NONMATCH", 0, "CONFIRMED"),
    "SUBSTITUTED_ENTRY_DIVERGENCE": ("NONMATCH", 1, "CONFIRMED"),
    "SUBSTITUTED_MIDROUTE_FOREIGN": ("NONMATCH", 1, "CONFIRMED"),
    "SUBSTITUTION_SUSPECTED_IDENTITY_UNRESOLVED": ("UNKNOWN", 2, "CANDIDATE_TWO_SIDED"),
    "SUBSTITUTION_SUSPECTED_POSITIONAL": ("UNKNOWN", 2, "CANDIDATE_TWO_SIDED"),
    "MERGE_OR_SHORTCUT_SUSPECTED": ("UNKNOWN", 2, "CANDIDATE_TWO_SIDED"),
    "STEREO_CONFLICT_SPECIFIED": ("NONMATCH", 0, "CONFIRMED"),
    "REVERSAL_CANDIDATE_STEREO_BLIND": ("UNKNOWN", 2, "CANDIDATE_TWO_SIDED"),
    "REVERSAL_CANDIDATE_CHARGE_BLIND": ("UNKNOWN", 2, "CANDIDATE_TWO_SIDED"),
    "REVERSAL_CANDIDATE_BOTH_BLIND": ("UNKNOWN", 2, "CANDIDATE_TWO_SIDED"),
    "REVERSAL_CANDIDATE_TAUT": ("UNKNOWN", 2, "CANDIDATE_TWO_SIDED"),
    "REPRESENTATION_EQ_STEREO_BLIND": ("UNKNOWN", 3, "CANDIDATE"),
    "REPRESENTATION_EQ_CHARGE_BLIND": ("UNKNOWN", 3, "CANDIDATE"),
    "REPRESENTATION_EQ_BOTH_BLIND": ("UNKNOWN", 3, "CANDIDATE"),
    "REPRESENTATION_EQ_TAUT": ("UNKNOWN", 3, "CANDIDATE"),
    "REFERENCE_LIMITED": ("UNKNOWN", 4, "CANDIDATE"),
    "NAME_ONLY_UNRESOLVED": ("UNKNOWN", 4, "CANDIDATE"),
}
LAYER_ORDER = (("stereo_blind", "STEREO_BLIND"), ("charge_blind", "CHARGE_BLIND"),
               ("both_blind", "BOTH_BLIND"), ("taut", "TAUT"))


def diagnose_pair(gstep, pstep, threshold, controlled):
    """(relation, state, s_jac, p_jac, labels, reversal_two_sided) —— 单对诊断，不做绑定。"""
    fwd0, s0, p0, flip0, rev0 = layer_jacs(gstep, pstep, "iso", threshold, controlled)
    if fwd0:
        return "STRICT_MATCH", "MATCH", s0, p0, set(), False
    if flip0:
        return "DIRECTION_FLIPPED_STRICT", "NONMATCH", s0, p0, set(), False
    for attr, tag in LAYER_ORDER:
        fwd, s_j, p_j, flip, rev = layer_jacs(gstep, pstep, attr, threshold, controlled)
        if fwd:
            labels = representation_labels(gstep, pstep)
            if "STEREO_CONFLICT_SPECIFIED" in labels:
                return ("STEREO_CONFLICT_SPECIFIED", "NONMATCH", s_j, p_j, labels, False)
            return "REPRESENTATION_EQ_%s" % tag, "UNKNOWN", s_j, p_j, labels, False
        if flip:
            return ("REVERSAL_CANDIDATE_%s" % tag, "UNKNOWN", s_j, p_j,
                    representation_labels(gstep, pstep), True)
    # 单侧反向亲和（F01：只作线索）
    weak_rev = False
    for attr, tag in (("iso", "STRICT"),) + LAYER_ORDER:
        _, s_j, p_j, _, (r1, r2) = layer_jacs(gstep, pstep, attr, threshold, controlled)
        if (r1 >= threshold) != (r2 >= threshold):
            weak_rev = True
            break
    if gstep.ref_gap:
        return "REFERENCE_LIMITED", "UNKNOWN", s0, p0, {"GOLD_MAIN_COMPOUND_MISSING_SMILES"}, False
    if not pstep.has_any_structure:
        return "NAME_ONLY_UNRESOLVED", "UNKNOWN", s0, p0, set(), False
    if weak_rev:
        return "_CLUE_ONE_SIDED_REVERSAL", "CLUE", s0, p0, set(), False
    return "NO_RELATION", "NONE", s0, p0, set(), False


# ------------------------------------------------------------ alignment ----

def _oxygen_token(text):
    t = norm(text)
    if not t:
        return "NULL"
    if "anaerobic" in t or "厌氧" in t:
        return "ANAEROBIC"
    if "aerobic" in t or "好氧" in t:
        return "AEROBIC"
    return "OTHER:%s" % t[:30]


def _case_product_universe(gold_steps):
    """本案全部gold步（必答+背景）主产物both_blind键+NAME键集合——
    "内容对参考路线外来"判定用（F02双要件：位置证据+化学外来性）。"""
    uni = set()
    for g in gold_steps.values():
        for c in g.prods:
            if c.both_blind:
                uni.add(c.both_blind)
            uni |= {"NAME:" + n for n in c.names}
    return uni


def _gold_product_keys(g):
    keys = set()
    for c in g.prods:
        if c.both_blind:
            keys.add(c.both_blind)
        keys |= {"NAME:" + n for n in c.names}
    return keys


def _pred_sub_keys_bb(p):
    keys = set()
    for c in p.subs:
        if c.both_blind:
            keys.add(c.both_blind)
        elif c.name:
            keys.add("NAME:" + c.name)
    return keys


def _pred_product_keys(p):
    keys = set()
    for c in p.prods:
        if c.both_blind:
            keys.add(c.both_blind)
        elif c.name:
            keys.add("NAME:" + c.name)
    return keys


def _build_product_identity(gold_steps):
    """本案全部gold步主产物的分层身份宇宙（R2-01）。"""
    uni = {"iso": set(), "charge_blind": set(), "stereo_blind": set(),
           "both_blind": set(), "taut": set(), "names": set()}
    for g in gold_steps.values():
        for c in g.prods:
            for k in ("iso", "charge_blind", "stereo_blind", "both_blind", "taut"):
                v = getattr(c, k)
                if v:
                    uni[k].add(v)
            uni["names"] |= c.names
    return uni


def product_identity_verdicts(p, uni):
    out = []
    for c in p.prods:
        if c.parseable or c.iso:
            hit = any(getattr(c, k) and getattr(c, k) in uni[k]
                      for k in ("iso", "charge_blind", "stereo_blind", "both_blind", "taut"))
            if hit:
                out.append("SAME_OR_RELAXED_MATCH")
            elif c.name and c.name in uni["names"]:
                out.append("NAME_STRUCTURE_CONFLICT")
            else:
                out.append("OUT_PROVEN_STRUCTURAL")
        elif c.name and c.name in uni["names"]:
            out.append("SAME_BY_NAME")
        else:
            out.append("UNRESOLVED_IDENTITY")
    return out


def substitution_confirmable(verdicts):
    """确认替换门槛（R2-01）：≥1个结构证明外来且无名/结构矛盾项。
    缺结构或名未命中只构成身份未定→嫌疑边界，不得判确认外来。"""
    if not verdicts or "NAME_STRUCTURE_CONFLICT" in verdicts:
        return False
    return "OUT_PROVEN_STRUCTURAL" in verdicts


def unresolved_identity_flag(verdicts):
    return ("UNRESOLVED_IDENTITY" in verdicts or "SAME_BY_NAME" in verdicts
            or "NAME_STRUCTURE_CONFLICT" in verdicts)


def align_case(scope, gold_steps, answer_obj, controlled, cross_index,
               threshold=0.5, case_id=None):
    case_id = case_id or scope["case_id"]
    required = [s for s in scope["required_step_ids"].split("|") if s]
    background = [s for s in scope["background_step_ids"].split("|") if s]
    human_review_case = scope.get("content_deviation_requires_human_review") == "TRUE"
    ref_insufficient = scope.get("reference_insufficient") == "TRUE"
    req_set = set(required)

    res = {
        "case_id": case_id, "threshold": threshold,
        "answer_state": "OK", "route_status": None, "route_flags": [],
        "task_conformance_status": "OK", "task_violations": [],
        "task_and_route_status": None,
        "step_rows": [], "extra_rows": [], "boundary_rows": [], "clue_rows": [],
        "n_required": len(required), "n_background": len(background),
        "matched": 0, "flipped_strict": 0, "flipped_strict_nonrev": 0,
        "flipped_strict_rev": 0, "reversal_candidates_two_sided": 0,
        "substituted_confirmed": 0, "stereo_conflict": 0,
        "boundary_unknown": 0, "nonmatch_confirmed": 0, "missing": 0,
        "extra_unmatched": 0, "extra_background": 0, "extra_other_route_clue": 0,
        "extra_downstream": 0,
        "edge_total": 0, "edge_concordant": 0, "edge_discordant_hard": 0,
        "edge_discordant_soft": 0, "endpoint_reached": "",
        "endpoint_token_check": "", "coverage": "",
        "controlled_repetitions": 0, "controlled_excluded": 0,
        "split_merge_suspected": 0,
        "chain_reversal_confirmed": False, "chain_reversal_candidate_strong": False,
        "endpoint_flow_swap": "",
    }

    # ---------- 答案失败态 ----------
    if not isinstance(answer_obj, dict):
        return _fail_out(res, required, gold_steps, "NOT_OBJECT_OR_PARSE_FAILURE")
    pred_steps, pstate = parse_pred_steps(answer_obj)
    if pstate != "OK":
        return _fail_out(res, required, gold_steps, pstate)

    # ---------- 任务条件层（F07，独立于化学层） ----------
    rs = answer_obj.get("route_scope") if isinstance(answer_obj.get("route_scope"), dict) else {}
    chosen = norm(rs.get("chosen_route_name"))
    q_route = norm(scope.get("route_name_question"))
    if chosen and q_route:
        if chosen == q_route:
            res["route_flags"].append("TASK_ROUTE_NAME_VERBATIM_OK")
        else:
            res["task_violations"].append("ROUTE_NAME_NOT_VERBATIM")
            res["route_flags"].append("TASK_VIOLATION_ROUTE_NAME_NOT_VERBATIM")
    scope_oxy = _oxygen_token(scope.get("oxygen"))
    ans_oxy = _oxygen_token(rs.get("oxygen_condition"))
    if scope_oxy in ("AEROBIC", "ANAEROBIC"):
        if ans_oxy in ("AEROBIC", "ANAEROBIC") and ans_oxy != scope_oxy:
            res["task_violations"].append("OXYGEN_MISMATCH:%s_vs_%s" % (scope_oxy, ans_oxy))
            res["route_flags"].append("TASK_VIOLATION_OXYGEN_MISMATCH")
        elif ans_oxy == "NULL":
            res["route_flags"].append("TASK_OXYGEN_ANSWER_NULL")
    else:
        res["route_flags"].append("TASK_OXYGEN_SCOPE_NULL_NO_INFERENCE")
    res["n_alt_branches_declared"] = len(
        [x for x in (answer_obj.get("alternative_branches") or []) if isinstance(x, dict)])
    res["n_downstream_continuation"] = len(
        [x for x in (answer_obj.get("downstream_continuation") or []) if isinstance(x, dict)])

    # ---------- 第一轮：G3冻结口径 strict 一对一贪心（必答+背景） ----------
    stats = {"repetitions": 0, "excluded": 0}
    pviews = []
    for p in pred_steps:
        pviews.append((pred_side_keys(p, "subs", controlled, stats),
                       pred_side_keys(p, "prods", controlled, stats)))
    res["controlled_repetitions"] = stats["repetitions"]
    res["controlled_excluded"] = stats["excluded"]
    all_gold_ids = required + background
    pairs = []
    for gsid in sorted(all_gold_ids):
        g = gold_steps[gsid]
        g_subs, sub_ctrl = gold_side(g, "subs", controlled)
        g_prods, prod_ctrl = gold_side(g, "prods", controlled)
        for idx, (p_subs, p_prods) in enumerate(pviews):
            s_jac = 1.0 if (sub_ctrl and not p_subs) else jac(p_subs, g_subs)
            p_jac = 1.0 if (prod_ctrl and not p_prods) else jac(p_prods, g_prods)
            s_neutral = sub_ctrl and not p_subs
            p_neutral = prod_ctrl and not p_prods
            evid = [v for v, ne in ((s_jac, s_neutral), (p_jac, p_neutral)) if not ne]
            score = 0.0 if not evid else sum(evid) / float(len(evid))
            if evid and score >= threshold and all(v >= threshold for v in evid):
                pairs.append((score, gsid, idx, s_jac, p_jac))
    pairs.sort(key=lambda tt: (-tt[0], tt[1], tt[2]))
    used_g, used_p, match_of_gold, gold_of_pred, jac_of = set(), set(), {}, {}, {}
    for score, gsid, idx, s_jac, p_jac in pairs:
        if gsid in used_g or idx in used_p:
            continue
        used_g.add(gsid)
        used_p.add(idx)
        match_of_gold[gsid] = idx
        gold_of_pred[idx] = gsid
        jac_of[gsid] = (s_jac, p_jac)

    unmatched_pred = [p for p in pred_steps if p.index not in used_p]

    # ---------- 第二轮：未绑定必答步逐对诊断（候选，不直接绑定） ----------
    diag = {}   # (gsid, pidx) -> diagnose tuple
    for gsid in required:
        if gsid in match_of_gold:
            continue
        g = gold_steps[gsid]
        for p in unmatched_pred:
            diag[(gsid, p.index)] = diagnose_pair(g, p, threshold, controlled)

    # ---------- 确认替换（F02：仅ENTRY_DIVERGENCE与POSITIONAL，独占） ----------
    pred_by_id = {p.step_id: p for p in pred_steps}
    succ_map_pred = defaultdict(set)
    for p in pred_steps:
        for pre in p.preds:
            if pre in pred_by_id:
                succ_map_pred[pre].add(p.step_id)
    gold_flow_entry = [s for s in required
                       if not ({x for x in gold_steps[s].preds} & req_set)]

    bound = {}          # gsid -> (relation, pidx, s_j, p_j, labels, two_sided)
    bound_pred = set()
    product_universe = _build_product_identity(gold_steps)

    # ENTRY_DIVERGENCE（F02双要件）：同底物投喂（严格层底物侧≥t）+产物对全路线外来。
    # 产物命中本案gold产物universe→疑似拆并/抄近路→边界嫌疑，不确认替换。
    for gsid in sorted(gold_flow_entry):
        if gsid in match_of_gold:
            continue
        g = gold_steps[gsid]
        for p in unmatched_pred:
            if p.index in bound_pred or p.preds:
                continue
            _, s0, p0, _, _ = layer_jacs(g, p, "iso", threshold, controlled)
            if s0 >= threshold and p0 < threshold:
                rel0 = diag.get((gsid, p.index))
                if rel0 and rel0[0] not in ("NO_RELATION", "_CLUE_ONE_SIDED_REVERSAL"):
                    continue  # 已有真实关系→正常绑定优先，不算替换
                verdicts = product_identity_verdicts(p, product_universe)
                if substitution_confirmable(verdicts):
                    bound[gsid] = ("SUBSTITUTED_ENTRY_DIVERGENCE", p.index, s0, p0,
                                   {"SAME_ENTRY_SUBSTRATE_DIFFERENT_TRANSFORMATION",
                                    "PRODUCT_FOREIGN_TO_ROUTE",
                                    "PRODUCT_IDENTITY_VERDICTS:" + ",".join(sorted(verdicts))},
                                   False)
                    bound_pred.add(p.index)
                elif "SAME_OR_RELAXED_MATCH" in verdicts:
                    res["split_merge_suspected"] += 1
                    res["boundary_rows"].append({
                        "case_id": case_id, "b_slot_uid": "",
                        "kind": "MERGE_OR_SHORTCUT_SUSPECTED",
                        "gold_step_ids": gsid, "pred_step_id": p.step_id,
                        "threshold": threshold,
                        "note": "入口底物相同、产物命中本案其他gold步产物：疑似拆并/抄近路，交边界复核"})
                elif unresolved_identity_flag(verdicts):
                    bound[gsid] = ("SUBSTITUTION_SUSPECTED_IDENTITY_UNRESOLVED",
                                   p.index, s0, p0,
                                   {"PRODUCT_IDENTITY_VERDICTS:" + ",".join(sorted(verdicts)),
                                    "IDENTITY_UNPROVEN_NOT_FOREIGN_PROOF"}, False)
                    bound_pred.add(p.index)
                break

    # ---------- 关系绑定（确认类先于UNKNOWN类，独占、稳定tie-break） ----------
    cand = []
    for (gsid, pidx), d in diag.items():
        rel, state, s_j, p_j, labels, two_sided = d
        if gsid in bound or pidx in bound_pred:
            continue
        if rel.startswith("_CLUE") or rel == "NO_RELATION":
            continue
        cls = RELATION_CLASS[rel][1]
        cand.append((cls, -((s_j + p_j) / 2.0), gsid, pidx, rel, s_j, p_j, labels, two_sided))
    cand.sort(key=lambda tt: (tt[0], tt[1], tt[2], tt[3]))
    for cls, negj, gsid, pidx, rel, s_j, p_j, labels, two_sided in cand:
        if gsid in bound or pidx in bound_pred:
            continue
        bound[gsid] = (rel, pidx, s_j, p_j, labels, two_sided)
        bound_pred.add(pidx)

    # POSITIONAL替换（F02三要件：位置邻域等值 + 物质流连续性 + 产物外来性；独占）
    rev_bound = {v[1]: k for k, v in bound.items()}
    for gsid in required:
        if gsid in match_of_gold or gsid in bound:
            continue
        g = gold_steps[gsid]
        g_pre_bound = {x for x in g.preds if x in req_set and
                       (x in match_of_gold or x in bound)}
        g_suc_bound = {x for x in g.succs if x in req_set and
                       (x in match_of_gold or x in bound)}
        if not (g_pre_bound or g_suc_bound):
            continue
        best = None
        for p in unmatched_pred:
            if p.index in bound_pred:
                continue
            d = diag.get((gsid, p.index))
            if d and d[0] not in ("NO_RELATION", "_CLUE_ONE_SIDED_REVERSAL"):
                continue  # 有化学关系（含表示类）的配对走正常绑定，不作位置替换
            p_pre_g = set()
            for x in p.preds:
                if x in pred_by_id:
                    xi = pred_by_id[x].index
                    if xi in gold_of_pred:
                        p_pre_g.add(gold_of_pred[xi])
                    elif xi in rev_bound:
                        p_pre_g.add(rev_bound[xi])
            p_suc_g = set()
            for x in succ_map_pred.get(p.step_id, ()):
                if x in pred_by_id:
                    xi = pred_by_id[x].index
                    if xi in gold_of_pred:
                        p_suc_g.add(gold_of_pred[xi])
                    elif xi in rev_bound:
                        p_suc_g.add(rev_bound[xi])
            hit = ((g_pre_bound and p_pre_g == g_pre_bound) or
                   (g_suc_bound and p_suc_g == g_suc_bound))
            if not hit:
                continue
            # 物质流连续性：p的底物须实际承接已绑定上游的产物
            # （gold前驱产物 或 已绑定/已匹配pred前驱的产物）
            cont_universe = set()
            for gg in g_pre_bound:
                cont_universe |= _gold_product_keys(gold_steps[gg])
            for x in p.preds:
                if x in pred_by_id:
                    xi = pred_by_id[x].index
                    if xi in gold_of_pred:
                        cont_universe |= _gold_product_keys(gold_steps[gold_of_pred[xi]])
                    elif xi in rev_bound:
                        cont_universe |= _pred_product_keys(pred_steps[xi])
            continuity = bool(_pred_sub_keys_bb(p) & cont_universe)
            sjp = d[2] if d else 0.0
            pjp = d[3] if d else 0.0
            key = (not continuity, -(sjp + pjp), p.index)
            if best is None or key < best[0]:
                best = (key, p.index, sjp, pjp, continuity)
        if best:
            _, pidx, sjp, pjp, continuity = best
            p = pred_steps[pidx]
            verdicts = product_identity_verdicts(p, product_universe)
            foreign = substitution_confirmable(verdicts)
            if continuity and not foreign and unresolved_identity_flag(verdicts):
                bound[gsid] = ("SUBSTITUTION_SUSPECTED_IDENTITY_UNRESOLVED", pidx,
                               sjp, pjp,
                               {"NEIGHBORHOOD_MATCH", "MATERIAL_FLOW_CONTINUITY",
                                "IDENTITY_UNPROVEN_NOT_FOREIGN_PROOF",
                                "PRODUCT_IDENTITY_VERDICTS:" + ",".join(sorted(verdicts))},
                               False)
                bound_pred.add(pidx)
            elif continuity and foreign:
                bound[gsid] = ("SUBSTITUTED_MIDROUTE_FOREIGN", pidx, sjp, pjp,
                               {"NEIGHBORHOOD_MATCH", "MATERIAL_FLOW_CONTINUITY",
                                "PRODUCT_FOREIGN_TO_ROUTE",
                                "PRODUCT_IDENTITY_VERDICTS:" + ",".join(sorted(verdicts))},
                               False)
                bound_pred.add(pidx)
            elif continuity and not foreign:
                # 位置+连续性成立但产物不外来的：疑似拆并/表示问题→边界嫌疑
                bound[gsid] = ("SUBSTITUTION_SUSPECTED_POSITIONAL", pidx, sjp, pjp,
                               {"NEIGHBORHOOD_MATCH", "MATERIAL_FLOW_CONTINUITY",
                                "PRODUCT_NOT_FOREIGN_TO_ROUTE"}, False)
                bound_pred.add(pidx)
            else:
                # 无物质流连续性：无关预测不得充当替换证据（F02），仅记线索
                res["clue_rows"].append({
                    "case_id": case_id, "b_slot_uid": "", "gold_step_id": gsid,
                    "pred_step_id": p.step_id,
                    "clue_type": "POSITIONAL_NO_MATERIAL_CONTINUITY",
                    "layer": "", "jac_sub": round(sjp, 4), "jac_prod": round(pjp, 4),
                    "final_target_binding": "NO",
                    "note": "位置邻域命中但底物不承接上游产物：不确认替换，gold步按缺步处理"})

    # ---------- 候选线索表（非独占；F02） ----------
    for gsid in required:
        if gsid in match_of_gold or gsid in bound:
            continue
        for p in unmatched_pred:
            if p.index in bound_pred:
                continue
            d = diag.get((gsid, p.index))
            if not d:
                continue
            rel, state, s_j, p_j, labels, two_sided = d
            if rel == "_CLUE_ONE_SIDED_REVERSAL":
                res["clue_rows"].append({
                    "case_id": case_id, "b_slot_uid": "", "gold_step_id": gsid,
                    "pred_step_id": p.step_id, "clue_type": "ONE_SIDED_REVERSAL",
                    "layer": "", "jac_sub": round(s_j, 4), "jac_prod": round(p_j, 4),
                    "final_target_binding": "NO",
                    "note": "单端点反向重合：仅候选，不构成反转证明(F01)"})
    for p in unmatched_pred:
        sig = p.sig()
        if sig:
            hits = [h for h in cross_index.get(sig, []) if h[0] != case_id]
            if hits:
                res["clue_rows"].append({
                    "case_id": case_id, "b_slot_uid": "", "gold_step_id": "",
                    "pred_step_id": p.step_id, "clue_type": "OTHER_ROUTE_SIGNATURE",
                    "layer": "strict_signature", "jac_sub": "", "jac_prod": "",
                    "final_target_binding": ("YES" if p.index in bound_pred else "NO"),
                    "note": "hits=%s;跨题命中=检索线索不广播(F02)" %
                            ";".join("%s:%s" % h for h in sorted(hits)[:4])})
        # 名称匹配本案其他gold步化合物（命名空间=化合物名，非酶名）
        if not p.has_any_structure:
            pnames = {c.name for c in p.subs + p.prods if c.name}
            for gsid2 in sorted(set(required) | set(background)):
                if gsid2 in match_of_gold or gsid2 in bound:
                    continue
                gnames = set()
                for c in gold_steps[gsid2].subs + gold_steps[gsid2].prods:
                    gnames |= c.names
                if pnames & gnames:
                    res["clue_rows"].append({
                        "case_id": case_id, "b_slot_uid": "", "gold_step_id": gsid2,
                        "pred_step_id": p.step_id, "clue_type": "NAME_MATCH_OTHER_STEP",
                        "layer": "compound_name_only", "jac_sub": "", "jac_prod": "",
                        "final_target_binding": "NO",
                        "note": "化合物名命中其他gold步（酶名同义词不入此层，A.5命名空间纪律）"})

    # ---------- 拆并嫌疑（保持R0：仅边界诊断，不赦免一对一） ----------
    req_unbound = [g for g in required if g not in match_of_gold and g not in bound]
    unbound_pred = [p for p in unmatched_pred if p.index not in bound_pred]
    for i, g1 in enumerate(req_unbound):
        for g2 in req_unbound[i + 1:]:
            if g2 not in gold_steps[g1].succs and g1 not in gold_steps[g2].succs:
                continue
            a, b = (g1, g2) if g2 in gold_steps[g1].succs else (g2, g1)
            ga, gb = gold_steps[a], gold_steps[b]
            shared = ({c.key for c in ga.prods if c.key} & {c.key for c in gb.subs if c.key})
            m_subs = ({c.key for c in ga.subs if c.key} | {c.key for c in gb.subs if c.key}) - shared
            m_prods = ({c.key for c in ga.prods if c.key} | {c.key for c in gb.prods if c.key}) - shared
            for p in unbound_pred:
                ps = {c.key for c in p.subs if c.key}
                pp = {c.key for c in p.prods if c.key}
                if m_subs and m_prods and jac(ps, m_subs) >= threshold and \
                        jac(pp, m_prods) >= threshold:
                    res["split_merge_suspected"] += 1
                    res["boundary_rows"].append({
                        "case_id": case_id, "b_slot_uid": "", "kind": "MERGE_SUSPECTED",
                        "gold_step_ids": "%s+%s" % (a, b), "pred_step_id": p.step_id,
                        "threshold": threshold,
                        "note": "两连续gold步并集≈一预测步；一对一不赦免(G3 D3)，交边界复核"})

    # ---------- 逐步行 ----------
    cls_count = defaultdict(int)
    for gsid in required:
        g = gold_steps[gsid]
        if gsid in match_of_gold:
            pidx = match_of_gold[gsid]
            p = pred_steps[pidx]
            sj, pj = jac_of[gsid]
            res["step_rows"].append(_step_row(case_id, gsid, p.step_id, "MATCH",
                                              "STRICT_MATCH", round(sj, 4), round(pj, 4),
                                              "", threshold, "FINAL_BOUND",
                                              pred_order=p.order, gold_order=g.order,
                                              gold_reaction=g.reaction_id,
                                              gold_arrow=g.arrow_class))
            cls_count["MATCHED"] += 1
            continue
        if gsid in bound:
            rel, pidx, s_j, p_j, labels, two_sided = bound[gsid]
            p = pred_steps[pidx]
            state = RELATION_CLASS[rel][0]
            note = ",".join(sorted(labels))
            res["step_rows"].append(_step_row(case_id, gsid, p.step_id, state, rel,
                                              round(s_j, 4), round(p_j, 4), note,
                                              threshold, "FINAL_BOUND",
                                              pred_order=p.order, gold_order=g.order,
                                              gold_reaction=g.reaction_id,
                                              gold_arrow=g.arrow_class))
            cls_count["MATCHED" if state == "MATCH" else
                      "NONMATCH" if state == "NONMATCH" else "BOUNDARY"] += 1
            continue
        # 未绑定：MISSING（缺步），线索见clue表
        clue_kinds = sorted({c["clue_type"] for c in res["clue_rows"]
                             if c["gold_step_id"] == gsid})
        res["step_rows"].append(_step_row(case_id, gsid, "", "MISSING",
                                          "NO_BOUND_RELATION", "", "",
                                          "clues=%s" % ",".join(clue_kinds) if clue_kinds else "",
                                          threshold, "UNBOUND",
                                          gold_order=g.order,
                                          gold_reaction=g.reaction_id,
                                          gold_arrow=g.arrow_class))
        cls_count["MISSING"] += 1

    res["matched"] = cls_count["MATCHED"]
    res["missing"] = cls_count["MISSING"]
    res["boundary_unknown"] = cls_count["BOUNDARY"]
    reasons = [r["reason_code"] for r in res["step_rows"]]
    res["flipped_strict"] = reasons.count("DIRECTION_FLIPPED_STRICT")
    flip_sids = [r["gold_step_id"] for r in res["step_rows"]
                 if r["reason_code"] == "DIRECTION_FLIPPED_STRICT"]
    res["flipped_strict_nonrev"] = sum(
        1 for s in flip_sids if gold_steps[s].arrow_class != "reversible")
    res["flipped_strict_rev"] = res["flipped_strict"] - res["flipped_strict_nonrev"]
    res["reversal_candidates_two_sided"] = sum(
        1 for r in res["step_rows"] if r["reason_code"].startswith("REVERSAL_CANDIDATE"))
    res["substituted_confirmed"] = sum(
        1 for r in res["step_rows"] if r["reason_code"].startswith("SUBSTITUTED"))
    res["stereo_conflict"] = reasons.count("STEREO_CONFLICT_SPECIFIED")
    res["nonmatch_confirmed"] = sum(1 for r in res["step_rows"]
                                    if r["step_state"] == "NONMATCH")
    res["coverage"] = round(cls_count["MATCHED"] / float(len(required)), 4) if required else ""

    # ---------- 链级反转（F01严格版） ----------
    endpoints = _endpoint_flow_swap(scope, gold_steps, pred_steps, match_of_gold,
                                    bound, threshold)
    res["endpoint_flow_swap"] = endpoints
    flip_or_cand_sids = [r["gold_step_id"] for r in res["step_rows"]
                         if r["reason_code"] == "DIRECTION_FLIPPED_STRICT" or
                         r["reason_code"].startswith("REVERSAL_CANDIDATE")]
    involved_pred = []
    for r in res["step_rows"]:
        if r["gold_step_id"] in flip_or_cand_sids and r["pred_step_id"]:
            pid = next((p.index for p in pred_steps if p.step_id == r["pred_step_id"]), None)
            if pid is not None:
                involved_pred.append(pid)
    connected = _pred_connected(involved_pred, pred_steps, pred_by_id, succ_map_pred)
    n_two_sided = res["flipped_strict"] + res["reversal_candidates_two_sided"]
    need = max(2, -(-len(required) // 2))
    if (res["matched"] == 0 and res["flipped_strict"] >= need and connected):
        # F01确定反转：每个反转步本身已是严格层双侧身份证明+方向+稳定一对一配对；
        # 连通性给"实际连接依据"；matched==0保证是整链而非局部
        res["chain_reversal_confirmed"] = True
        res["route_flags"].append("CHAIN_REVERSAL_CONFIRMED_STRICT")
    elif (res["matched"] == 0 and connected and
          (n_two_sided >= need or
           (n_two_sided >= 1 and endpoints == "SWAP_SUPPORTED"))):
        res["chain_reversal_candidate_strong"] = True
        res["route_flags"].append("CHAIN_REVERSAL_CANDIDATE_STRONG")

    # ---------- 额外步分类（F02顺序：背景→下游→跨题线索→未匹配） ----------
    term_keys = set()
    for t in [s for s in scope["gold_terminal_step_ids"].split("|") if s]:
        if t in gold_steps:
            term_keys |= {c.key for c in gold_steps[t].prods if c.key}
            term_keys |= {c.charge_blind for c in gold_steps[t].prods if c.charge_blind}
    bg_matched = {gsid for gsid in match_of_gold if gsid in set(background)}
    for p in pred_steps:
        if p.index in used_p:
            gsid = gold_of_pred[p.index]
            if gsid in bg_matched:
                res["extra_background"] += 1
                res["extra_rows"].append(_extra_row(case_id, p, "EXTRA_BACKGROUND_MATCH",
                                                    "matched_background_gold_step=%s;范围附录不罚" % gsid))
            continue
        if p.index in bound_pred:
            continue
        p_sub_keys = {c.key for c in p.subs if c.key} | \
                     {c.charge_blind for c in p.subs if c.charge_blind}
        if term_keys and p_sub_keys and (p_sub_keys & term_keys):
            res["extra_downstream"] += 1
            res["extra_rows"].append(_extra_row(case_id, p, "EXTRA_DOWNSTREAM_OF_ENDPOINT",
                                                "底物含金终点主产物；先于跨题检索分类(F02)；记录不判偏离"))
            continue
        sig = p.sig()
        hits = [h for h in cross_index.get(sig, []) if h[0] != case_id] if sig else []
        if hits:
            res["extra_other_route_clue"] += 1
            res["extra_rows"].append(_extra_row(case_id, p, "EXTRA_OTHER_ROUTE_CLUE",
                                                "线索=%s;不单独作偏离证据(F02)" %
                                                ";".join("%s:%s" % h for h in sorted(hits)[:4])))
            continue
        res["extra_unmatched"] += 1
        res["extra_rows"].append(_extra_row(case_id, p, "EXTRA_UNMATCHED", ""))

    # ---------- 连接一致性（沿gold真实边；分支不按S编号强判线性） ----------
    matched_pairs = {g: match_of_gold[g] for g in required if g in match_of_gold}
    pred_edges_present = any(p.preds for p in pred_steps)
    order_of_pred = {p.index: (p.order if p.order is not None else p.index)
                     for p in pred_steps}
    for gu in sorted(matched_pairs):
        for gv in gold_steps[gu].succs:
            if gv not in req_set or gv not in matched_pairs:
                continue
            res["edge_total"] += 1
            pu, pv = pred_steps[matched_pairs[gu]], pred_steps[matched_pairs[gv]]
            pu_before_pv = pu.step_id in _pred_closure_before(pv, pred_by_id)
            pv_before_pu = pv.step_id in _pred_closure_before(pu, pred_by_id)
            soft_ok = order_of_pred[pu.index] < order_of_pred[pv.index]
            if pv_before_pu:
                res["edge_discordant_hard"] += 1
                kind = "PRED_EDGE_CYCLE" if pu_before_pv else "ORDER_CONNECTIVITY_VIOLATION"
                res["route_flags"].append("%s:%s->%s" % (kind, gu.split("__")[1],
                                                         gv.split("__")[1]))
            elif pu_before_pv or soft_ok:
                res["edge_concordant"] += 1
            else:
                res["edge_discordant_soft"] += 1
                res["route_flags"].append("ORDER_SOFT_DISCORDANT:%s->%s"
                                          % (gu.split("__")[1], gv.split("__")[1]))

    # ---------- 终点 ----------
    terminals = [s for s in scope["gold_terminal_step_ids"].split("|") if s]
    t_matched = [t for t in terminals if t in matched_pairs]
    res["endpoint_reached"] = ("ALL" if t_matched and len(t_matched) == len(terminals)
                               else "PARTIAL" if t_matched else "NO")
    tok = norm(scope.get("question_endpoint_token"))
    if tok:
        term_names = set()
        for t in terminals:
            for c in gold_steps[t].prods:
                term_names |= c.names
        res["endpoint_token_check"] = ("TOKEN_MATCHES_GOLD_TERMINAL"
                                       if any(tok in n or n in tok for n in term_names)
                                       else "REFERENCE_SIDE_TOKEN_NAMING_QA")

    # ---------- 整题状态（化学层）+任务层组合 ----------
    status, flags = _case_status(res, human_review_case, ref_insufficient, required)
    res["route_status"] = status
    res["route_flags"] = sorted(set(res["route_flags"] + flags))
    if res["split_merge_suspected"]:
        res["route_flags"].append("SPLIT_MERGE_SUSPECTED")
    res["task_conformance_status"] = ("VIOLATED" if res["task_violations"] else "OK")
    res["task_and_route_status"] = "%s|%s" % (status, res["task_conformance_status"])
    return res


def _fail_out(res, required, gold_steps, state):
    res["answer_state"] = state
    res["route_status"] = "INCOMPLETE"
    res["task_and_route_status"] = "INCOMPLETE|%s" % (
        "OK" if state != "EMPTY_STEPS" else "HONEST_NULL")
    flag = "HONEST_NULL_ANSWER" if state == "EMPTY_STEPS" else "ANSWER_FAILURE:%s" % state
    res["route_flags"].append(flag)
    for sid in required:
        res["step_rows"].append(_step_row(res["case_id"], sid, "", "MISSING", state,
                                          "", "", "", res["threshold"], "UNBOUND",
                                          gold_order=gold_steps[sid].order,
                                          gold_reaction=gold_steps[sid].reaction_id,
                                          gold_arrow=gold_steps[sid].arrow_class))
    res["missing"] = len(required)
    res["coverage"] = 0.0
    res["endpoint_reached"] = "NO"
    return res


def _endpoint_flow_swap(scope, gold_steps, pred_steps, match_of_gold, bound, threshold):
    """端点流交换证据：预测入口步底物≈gold流终点产物 且 预测终点步产物≈gold流入口底物。"""
    required = [s for s in scope["required_step_ids"].split("|") if s]
    req_set = set(required)
    if not required or not pred_steps:
        return "NOT_APPLICABLE"
    gold_entry = [s for s in required if not ({x for x in gold_steps[s].preds} & req_set)]
    gold_term = [s for s in required if not ({x for x in gold_steps[s].succs} & req_set)]
    pred_entry = [p for p in pred_steps if not p.preds] or \
                 [min(pred_steps, key=lambda p: (p.order if p.order is not None else p.index))]
    pred_term = [p for p in pred_steps
                 if not any(p.step_id in q.preds for q in pred_steps)] or \
                [max(pred_steps, key=lambda p: (p.order if p.order is not None else p.index))]

    def bb_keys(comps):
        return {c.both_blind or c.key for c in comps if (c.both_blind or c.key)}

    gold_term_prods = set()
    for t in gold_term:
        gold_term_prods |= bb_keys(gold_steps[t].prods)
    gold_entry_subs = set()
    for t in gold_entry:
        gold_entry_subs |= bb_keys(gold_steps[t].subs)
    pe_subs = set()
    for p in pred_entry:
        pe_subs |= bb_keys(p.subs)
    pt_prods = set()
    for p in pred_term:
        pt_prods |= bb_keys(p.prods)
    c1 = containment(pe_subs, gold_term_prods) >= threshold or \
        jac(pe_subs, gold_term_prods) >= threshold
    c2 = containment(pt_prods, gold_entry_subs) >= threshold or \
        jac(pt_prods, gold_entry_subs) >= threshold
    return "SWAP_SUPPORTED" if (c1 and c2) else ("PARTIAL" if (c1 or c2) else "NO")


def _pred_connected(pidxs, pred_steps, pred_by_id, succ_map_pred):
    """涉及的预测步在其自声明图（或order邻接）中是否连通。"""
    if len(pidxs) <= 1:
        return bool(pidxs)
    idxset = set(pidxs)
    byidx = {p.index: p for p in pred_steps}
    adj = defaultdict(set)
    for i in idxset:
        p = byidx[i]
        for pre in p.preds:
            if pre in pred_by_id and pred_by_id[pre].index in idxset:
                adj[i].add(pred_by_id[pre].index)
                adj[pred_by_id[pre].index].add(i)
        for suc in succ_map_pred.get(p.step_id, ()):
            if suc in pred_by_id and pred_by_id[suc].index in idxset:
                adj[i].add(pred_by_id[suc].index)
                adj[pred_by_id[suc].index].add(i)
    if not any(adj.values()):
        # 无边声明时退化为order连续块：涉及步在全体pred顺序中构成无间断区间
        srt_all = sorted((p.index for p in pred_steps),
                         key=lambda i: (byidx[i].order if byidx[i].order is not None
                                        else byidx[i].index))
        pos = sorted(srt_all.index(i) for i in idxset)
        return pos == list(range(pos[0], pos[0] + len(pos)))
    seen, stack = set(), [pidxs[0]]
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(adj[x])
    return seen == idxset


def _pred_closure_before(pv, pred_by_id):
    seen, stack = set(), list(pv.preds)
    while stack:
        x = stack.pop()
        if x in seen or x not in pred_by_id:
            continue
        seen.add(x)
        stack.extend(pred_by_id[x].preds)
    return seen


def _case_status(res, human_review_case, ref_insufficient, required):
    flags = []
    if ref_insufficient:
        return "REFERENCE_HOLD", ["REFERENCE_INSUFFICIENT_PER_SCOPE"]
    if res["answer_state"] != "OK":
        return "INCOMPLETE", []
    if res["chain_reversal_confirmed"]:
        if human_review_case:
            flags.append("HUMAN_REVIEW_006_DISCLOSURE_APPLIES")
        return "DEVIATES", flags
    if res["flipped_strict_nonrev"]:
        # 非可逆步严格反转=结构事实；006亦判但挂披露复核旗
        if human_review_case:
            flags.append("HUMAN_REVIEW_006_DISCLOSURE_APPLIES")
        return "DEVIATES", flags
    if res["substituted_confirmed"] or res["stereo_conflict"]:
        if human_review_case:
            flags.append("CONTENT_DEVIATION_DOWNGRADED_PER_DR03_ROUTE_UNIQUENESS_NOT_ESTABLISHED")
            return "BOUNDARY_REVIEW", flags
        return "DEVIATES", flags
    if res["edge_discordant_hard"]:
        return "DEVIATES", flags
    if res["flipped_strict_rev"]:
        flags.append("REVERSIBLE_STEP_FLIPPED_STRICT_X%d" % res["flipped_strict_rev"])
        return "BOUNDARY_REVIEW", flags
    boundary_triggers = []
    if res["chain_reversal_candidate_strong"]:
        boundary_triggers.append("CHAIN_REVERSAL_CANDIDATE_STRONG_PRIORITY_REVIEW")
    if res["boundary_unknown"]:
        boundary_triggers.append("STEP_UNKNOWN_X%d" % res["boundary_unknown"])
    if res["split_merge_suspected"]:
        boundary_triggers.append("SPLIT_MERGE_SUSPECTED")
    if res["edge_discordant_soft"]:
        boundary_triggers.append("ORDER_SOFT_DISCORDANT")
    if human_review_case and (res["missing"] or res["boundary_unknown"]):
        boundary_triggers.append("CASE_006_AMBIGUITY_REVIEW")
    if boundary_triggers:
        return "BOUNDARY_REVIEW", flags + boundary_triggers
    if res["missing"]:
        return "INCOMPLETE", flags + ["MISSING_REQUIRED_STEPS_X%d" % res["missing"]]
    return "CONFORMS", flags


def _step_row(case_id, gsid, pred_step_id, state, reason, s_jac, p_jac, note,
              threshold, binding, pred_order="", gold_order="", gold_reaction="",
              gold_arrow=""):
    return {
        "case_id": case_id, "b_slot_uid": "",
        "gold_step_id": gsid,
        "gold_short": gsid.split("__")[1] if "__" in gsid else gsid,
        "gold_reaction_id": gold_reaction or (gsid.split("__")[2] if gsid.count("__") == 2 else ""),
        "gold_order": gold_order,
        "gold_arrow_class": gold_arrow,
        "pred_step_id": pred_step_id, "pred_order": pred_order,
        "step_state": state, "reason_code": reason,
        "binding_status": binding,
        "jac_sub": s_jac, "jac_prod": p_jac,
        "threshold": threshold, "note": note,
    }


def _extra_row(case_id, p, klass, note):
    names = ",".join(sorted({c.name for c in p.subs + p.prods if c.name})[:4])
    return {
        "case_id": case_id, "b_slot_uid": "",
        "pred_step_id": p.step_id, "pred_order": p.order,
        "extra_class": klass,
        "pred_main_names": names,
        "pred_sub_keys": "|".join(sorted({c.key for c in p.subs if c.key})[:3]),
        "pred_prod_keys": "|".join(sorted({c.key for c in p.prods if c.key})[:3]),
        "penalty_policy": ("NOT_PENALIZED_SCOPE_BACKGROUND" if klass == "EXTRA_BACKGROUND_MATCH"
                           else "NOT_PENALIZED_DOWNSTREAM_RECORD_ONLY"
                           if klass == "EXTRA_DOWNSTREAM_OF_ENDPOINT"
                           else "CLUE_ONLY_RECORDED" if klass == "EXTRA_OTHER_ROUTE_CLUE"
                           else "RECORDED_FOR_REVIEW"),
        "note": note,
    }


# ------------------------------------------------------------ gold load ----

def load_gold_steps(reaction_gold_path, cases=None):
    tmp = defaultdict(lambda: defaultdict(lambda: {"subs": [], "prods": [], "meta": None}))
    with open(reaction_gold_path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            case, sid = row["case_id"], row["step_occurrence_id"]
            if cases is not None and case not in cases:
                continue
            ent = tmp[case][sid]
            if ent["meta"] is None:
                ent["meta"] = (row["reaction_id"], int(row["linear_display_order"] or 0),
                               row.get("branch_id", ""),
                               sorted(p for p in (row.get("predecessor_step_ids") or "").split("|") if p),
                               sorted(p for p in (row.get("successor_step_ids") or "").split("|") if p),
                               row.get("gold_orientation", ""), row.get("arrow_class", ""))
            role = row["role_label"]
            if role in ("MAIN_SUBSTRATE", "MAIN_PRODUCT"):
                comp = GoldCompound(row["compound_id"],
                                    [row.get("identity_name"), row.get("db_cmpdname"),
                                     row.get("aligned_token")],
                                    (row.get("isosmiles") or "").strip())
                ent["subs" if role == "MAIN_SUBSTRATE" else "prods"].append(comp)
    out = {}
    for case, sids in tmp.items():
        out[case] = {}
        for sid, ent in sids.items():
            m = ent["meta"]
            out[case][sid] = GoldStep(sid, m[0], m[1], m[2], m[3], m[4], m[5], m[6],
                                      ent["subs"], ent["prods"])
    return out


def build_cross_route_index(gold_by_case):
    index = defaultdict(list)
    for case in sorted(gold_by_case):
        for sid in sorted(gold_by_case[case]):
            sig = gold_by_case[case][sid].sig()
            if sig:
                index[sig].append((case, sid))
    return dict(index)


def load_controlled_mask(path):
    ctrl = defaultdict(set)
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            cid = row["case_id"].strip()
            tok = norm(row.get("controlled_token"))
            if cid and tok:
                ctrl[cid].add(tok)
    return dict(ctrl)


def load_scope(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return {r["case_id"]: r for r in csv.DictReader(fh, delimiter="\t")}
