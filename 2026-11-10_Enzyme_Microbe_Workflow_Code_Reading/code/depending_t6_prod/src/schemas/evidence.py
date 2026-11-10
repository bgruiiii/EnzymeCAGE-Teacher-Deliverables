# src/schemas/evidence.py
# 证据链与子模型（M3 + M5 全量）

import hashlib
import re
from typing import Dict, List, Optional, Literal, Any
from pydantic import BaseModel, Field, field_validator, model_validator


# ═══════════════════════════════════════════════════════════════
# M3 核心模型
# ═══════════════════════════════════════════════════════════════

class SubstrateInfo(BaseModel):
    """底物解析结果"""
    substrate_smiles: str
    # 原输入 SMILES token（规范化前）——T6-R3 裁定 6：保留原文便于来源可追踪，
    # canonical lowercase aromatic 直接接受时不丢失原始表示。
    raw_substrate_smiles: Optional[str] = None
    substrate_name: Optional[str] = None
    # 取值：
    #   user_smiles     — 用户直接供 SMILES
    #   user_inchi      — 用户直接供 InChI
    #   pubchem_lookup  — LLM 提取名字 → PubChem 官方查表得到 SMILES（2026-07-22 引入）
    #   llm_parsed      — LLM 直接生成 SMILES（已知不可靠，仅作兼容/兼内部回退）
    source: Literal["user_smiles", "user_inchi", "pubchem_lookup", "llm_parsed"]
    provenance: str


class SourceContribution(BaseModel):
    """Typed provenance for one retrieved or predicted reaction contribution."""
    source: Literal["retrieved", "predicted"]
    source_tag: Optional[str] = None
    source_tool: Optional[str] = None
    model_version: Optional[str] = None
    provenance: Optional[str] = None
    source_record_id: Optional[str] = None
    evidence_hash: Optional[str] = None
    similarity_score: Optional[float] = None
    raw_score: Optional[float] = None
    score_semantics: Optional[str] = None


class CandidateReaction(BaseModel):
    """候选反应

    source_tag/source_tool 强制非空（T6-R3 裁定 3）：任何构造点必须显式标注来源，
    未知来源显式写 unknown/unavailable，禁止缺省或默认 enviPath（避免零调用时来源误归因）。

    G5（黄老师 2026-09-09 裁定 1）字段成对契约：每条 retrieved 证据必须同时携带
    reaction_smiles 与 reaction_sha256（对 UTF-8 原字符串、无追加换行求 SHA256）。
    二者由模型层 validator 强制成对一致：缺任一字段、SHA 不匹配或非 64 位小写
    hex 一律拒绝。
    """
    reaction_smiles: str
    reaction_sha256: str
    similarity_score: Optional[float] = None
    source: Literal["retrieved", "predicted"] = "retrieved"
    source_tag: str        # 来源细粒度标签：similarity_retrieval_route_c / biotransformer_envmicro / depending_v32 / mock_dry_run / unknown
    source_tool: str       # 来源工具名：reaction_retriever / reaction_predictor / unknown
    rhea_id: Optional[str] = None
    ec_numbers: Optional[List[str]] = None
    prediction_rank: Optional[int] = None
    raw_score: Optional[float] = None
    score_semantics: Optional[str] = None
    is_calibrated_probability: Optional[bool] = None
    model_version: Optional[str] = None
    provenance: Optional[str] = None
    source_record_id: Optional[str] = None
    evidence_hash: Optional[str] = None
    depth: Optional[int] = None
    parent_node_smiles: Optional[str] = None
    parent_node_depth: Optional[int] = None
    warnings: List[str] = Field(default_factory=list)
    source_contributions: List[SourceContribution] = Field(default_factory=list)

    @field_validator("reaction_sha256")
    @classmethod
    def _pair_with_reaction_smiles(cls, v: str, info) -> str:
        reaction_smiles = info.data.get("reaction_smiles")
        if not reaction_smiles:
            raise ValueError("reaction_sha256 requires the paired reaction_smiles")
        expected = hashlib.sha256(reaction_smiles.encode("utf-8")).hexdigest()
        if v != expected:
            raise ValueError(
                "reaction_sha256 does not match reaction_smiles: "
                f"expected {expected}, got {v!r}; SHA256 must be computed over "
                "the UTF-8 reaction_smiles string without trailing newline"
            )
        return v

    @field_validator("source_tag", "source_tool")
    @classmethod
    def _reject_blank_source(cls, v: str) -> str:
        # T6-R3 裁定 3：强制非空 + 拒绝空串/纯空白（"" / "   "）
        if not isinstance(v, str) or not v.strip():
            raise ValueError("source_tag/source_tool 必须为非空字符串（禁止空串或纯空白）")
        return v


class RankedEnzyme(BaseModel):
    """EnzymeCAGE 排序结果"""
    uid: str
    score: float
    rank: int
    ensemble_ci: Optional[tuple[float, float]] = None


class EvidenceRecord(BaseModel):
    """证据链记录"""
    stage: str          # "substrate" / "reaction" / "pool" / "ranking" / "reranking" / "microbe" / "trait" / "synthesis"
    action: str         # 具体动作描述
    data: dict[str, Any]
    timestamp: str


# ═══════════════════════════════════════════════════════════════
# M5 扩展模型
# ═══════════════════════════════════════════════════════════════

# ─── G4-R2A: 宿主 identity 与证据 record identity 必须分开（T6-R3A-R2A §5—§6）───
# 三件互相独立的事实：
#   1. host_identity_source_signature —— 宿主身份签名；冻结 G-SCHEMA organismAggregate 的
#      合并主键就是 source_signature，因此它绝不能用 enzyme UID 冒充（根因 C）。
#   2. evidence record identity —— UniProt accession / URL / response SHA，或冻结 map 行
#      identity；留在 source_record_id / evidence_hash，不混入宿主签名。
#   3. resolution_route —— LIVE_UNIPROT_REVIEWED 与 FROZEN_REVIEWED_UID_MAP_FALLBACK 必须
#      可无损区分，且互不冒充：fallback 绝不写入 UniProtReviewedHostEvidence（§6 禁伪造 live）。
# 枚举定义位置上移（同一对象，非重复定义）：MicrobeCandidate / EnzymeSourceProvenance 的
# 类注解在导入时即求值，必须早于这些模型。

HOST_RESOLUTION_LITERALS = (
    "EXACT_STRAIN",
    "SPECIES",
    "REPRESENTATIVE_STRAIN",
    "UNRESOLVED",
)
HostResolution = Literal["EXACT_STRAIN", "SPECIES", "REPRESENTATIVE_STRAIN", "UNRESOLVED"]

HOST_RESOLUTION_ROUTE_LITERALS = (
    "LIVE_UNIPROT_REVIEWED",
    "FROZEN_REVIEWED_UID_MAP_FALLBACK",
)
HostResolutionRoute = Literal["LIVE_UNIPROT_REVIEWED", "FROZEN_REVIEWED_UID_MAP_FALLBACK"]

# 宿主 identity 签名的来源：冻结已审计 map 行，或 §5 允许的确定性 taxon|organism 构造。
# REPRESENTATIVE_STRAIN 在 R2A 保留不启用：无 map 级菌株权威时不声称菌株分辨率。
HOST_IDENTITY_SOURCE_LITERALS = (
    "FROZEN_REVIEWED_UID_MAP",
    "CONSTRUCTED_TAXON_ORGANISM",
)
HostIdentitySource = Literal["FROZEN_REVIEWED_UID_MAP", "CONSTRUCTED_TAXON_ORGANISM"]

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def validate_host_resolution(value: str) -> str:
    """校验 host identity-resolution 字面量（与 host source 枚举相互独立，不得混用）。"""
    if isinstance(value, str) and value in HOST_RESOLUTION_LITERALS:
        return value
    raise ValueError(
        f"illegal host resolution literal: {value!r}; "
        f"allowed: {', '.join(HOST_RESOLUTION_LITERALS)}"
    )


def validate_host_resolution_route(value: str) -> str:
    """校验宿主证据解析路由字面量。"""
    if isinstance(value, str) and value in HOST_RESOLUTION_ROUTE_LITERALS:
        return value
    raise ValueError(
        f"illegal host resolution route: {value!r}; "
        f"allowed: {', '.join(HOST_RESOLUTION_ROUTE_LITERALS)}"
    )


def host_signature_is_enzyme_uid_shaped(enzyme_uid: str, signature) -> bool:
    """判定宿主签名是否其实就是该酶自己的 UID（根因 C 的模型级防线）。

    命中：signature == enzyme_uid，或末尾 identity token 恰为该 UID（如
    ``uniprotkb_reviewed:Q7X2D3``）。真实宿主 identity（``taxon:37930|organism:...``、
    ``proteome:UP000019804``）不因含数字/子串而被误判。
    """
    if not isinstance(signature, str) or not isinstance(enzyme_uid, str):
        return False
    sig, uid = signature.strip(), enzyme_uid.strip()
    if not sig or not uid:
        return False
    if sig == uid:
        return True
    return sig.rsplit(":", 1)[-1].strip() == uid


class RerankedEnzyme(BaseModel):
    """LLM 重排序后的酶（M5: LLMRerankingNode 输出）"""
    uid: str
    original_rank: int
    reranked_rank: int
    original_score: float
    rerank_rationale: str       # LLM 给出的排序理由
    confidence: Optional[float] = None


class MicrobeCandidate(BaseModel):
    """推荐微生物（M5: MicrobeSelectionNode 输出）——单酶→菌事实映射"""
    organism_name: str
    tax_id: Optional[int] = None
    enzyme_uid: str             # 该微生物携带的目标酶
    habitat_match: Optional[str] = None   # 与污水环境的匹配度描述
    growth_conditions: Optional[str] = None
    source_db: Optional[str] = None       # UniProt / KEGG / 文献
    # M4a 证据分级（框架 §3.2 OrganismHit 契约：UniProt SwissProt=reviewed / TrEMBL=unreviewed）
    # MT-D2（2026-07-18 裁定）：v1 不输出 organism_confidence float，
    #   禁止把 reviewed/unreviewed 映射成 0-1 confidence；evidence_level 作为原始维度保留。
    evidence_level: Optional[Literal["reviewed", "unreviewed", "predicted"]] = None
    rationale: Optional[str] = None
    # G4-R2A（§4/§7）：候选层直接携带解析路由与宿主 identity 签名，使下游转换只读节点
    # 输出即可区分 live reviewed 与冻结 map fallback。不新增公共 state 键——本模型已在
    # EnzymeCrewState.microbe_candidates 的现有承载路径上。
    resolution_route: Optional[HostResolutionRoute] = None
    host_identity_source_signature: Optional[str] = None


class SupportingEnzyme(BaseModel):
    """支持某候选菌的单酶记录（镜像学生权威实现 microbe_crew.tools.organism_aggregator.SupportingEnzyme）。

    保留原始 EnzymeCAGE 分 / rank / CI，不折算、不合成 confidence（MT-D2）。
    """
    uid: str
    score: float
    rank: int
    ensemble_ci: Optional[tuple[float, float]] = None


# ─── M4a 酶→菌原始证据维度（严格镜像学生 microbe_crew.tools.enzyme2organism_tool）───
# MT-D2：确定性代码透传原始证据维度（reviewed 状态 / annotation score / protein existence /
#   KEGG multiplicity），不合成 confidence float；LLM 不得创造数值。
# MT-D1：v1 仅纳入 UniProt reviewed (Swiss-Prot) 宿主；KEGG 作独立交叉证据（保留 multiplicity）。

class UniProtReviewedHostEvidence(BaseModel):
    """UniProt reviewed 宿主证据（与学生同名字段）。"""
    source_database: Literal["UniProtKB"] = "UniProtKB"
    source_url: str
    response_sha256: str
    primary_accession: str
    entry_type: Literal["UniProtKB reviewed (Swiss-Prot)"]
    reviewed: Literal[True] = True
    scientific_organism_name: str
    ncbi_taxon_id: int = Field(gt=0)
    lineage: List[str] = Field(default_factory=list)
    annotation_score: float
    protein_existence: str


class KEGGSupplementEvidence(BaseModel):
    """KEGG 独立补充证据：基因映射 multiplicity 原样保留（不折叠为单一宿主）。"""
    source_database: Literal["KEGG"] = "KEGG"
    source_url: str
    response_sha256: str
    gene_ids: List[str] = Field(default_factory=list)
    multiplicity: int = Field(ge=0)
    state: Literal["missing", "single", "multiple"]


class SourceError(BaseModel):
    """单个数据源查询失败 / 排除的结构化留痕（包括 unreviewed 排除）。"""
    source_database: Literal["UniProtKB", "KEGG"]
    source_url: str
    error_type: str
    message: str


class EnzymeSourceProvenance(BaseModel):
    """单酶的多源原始证据（镜像学生 EnzymeHostMapping / EnzymeSourceProvenance）。

    G4-R2A：该对象经 OrganismCandidate.per_enzyme_source_provenance 整体进入公共 state
    （现有承载键，见 §4 审计），因此在**本现有对象**上补齐宿主 identity 字段即可无损
    到达下游转换，无需新增老师未定义的公共 state 字段。
    """
    enzyme_uid: str
    uniprot_reviewed: Optional[UniProtReviewedHostEvidence] = None
    kegg: Optional[KEGGSupplementEvidence] = None
    source_errors: List[SourceError] = Field(default_factory=list)

    # ── G4-R2A: 宿主 identity（live / frozen-map fallback 共用同一套字段）──
    resolution_route: Optional[HostResolutionRoute] = None
    host_identity_source: Optional[HostIdentitySource] = None
    host_identity_source_signature: Optional[str] = None
    host_resolution: Optional[HostResolution] = None
    host_taxid: Optional[int] = Field(default=None, ge=1)
    host_name: Optional[str] = None
    # 冻结 map 行 identity（fallback 必备；live 分支若借 map 取审计签名也如实记录行号）
    frozen_map_file: Optional[str] = None
    frozen_map_line: Optional[int] = Field(default=None, ge=1)
    frozen_map_row_sha256: Optional[str] = None
    frozen_map_table_sha256: Optional[str] = None
    frozen_map_error: Optional[str] = None        # map 不可用/身份错的显式留痕（不静默）
    mapping_confidence_raw: Optional[str] = None  # 原始元数据，绝不折算 confidence/score
    warnings: List[str] = Field(default_factory=list)

    @field_validator("frozen_map_row_sha256", "frozen_map_table_sha256")
    @classmethod
    def _map_hashes_are_sha256(cls, v):
        if v is not None and not _SHA256_PATTERN.fullmatch(v):
            raise ValueError(
                "frozen map hashes must be 64-char lowercase hex SHA256 digests"
            )
        return v

    @model_validator(mode="after")
    def _host_identity_route_contract(self):
        sig = self.host_identity_source_signature
        if sig is not None and host_signature_is_enzyme_uid_shaped(self.enzyme_uid, sig):
            raise ValueError(
                "host_identity_source_signature must express the HOST, not the enzyme UID: "
                f"got {sig!r} for enzyme_uid {self.enzyme_uid!r} (T6-R3A-R2A §5 root cause C)"
            )
        if self.resolution_route is None:
            # 未做宿主 identity 判定（R1 既有 bare provenance 构造仍合法）：不得半填 identity 字段
            if (sig is not None or self.host_identity_source is not None
                    or self.frozen_map_line is not None):
                raise ValueError(
                    "host identity fields require an explicit resolution_route "
                    "(LIVE_UNIPROT_REVIEWED / FROZEN_REVIEWED_UID_MAP_FALLBACK)"
                )
            return self
        route = validate_host_resolution_route(self.resolution_route)
        if route == "LIVE_UNIPROT_REVIEWED":
            if self.uniprot_reviewed is None:
                raise ValueError(
                    "resolution_route=LIVE_UNIPROT_REVIEWED requires real reviewed UniProt "
                    "evidence; a frozen-map row must use FROZEN_REVIEWED_UID_MAP_FALLBACK"
                )
        else:  # FROZEN_REVIEWED_UID_MAP_FALLBACK
            if self.uniprot_reviewed is not None:
                raise ValueError(
                    "resolution_route=FROZEN_REVIEWED_UID_MAP_FALLBACK must NOT carry "
                    "UniProtReviewedHostEvidence: the frozen map row is mapping evidence, "
                    "not a live UniProt response (task section 6)"
                )
            missing = [n for n in ("frozen_map_file", "frozen_map_line",
                                   "frozen_map_row_sha256", "frozen_map_table_sha256")
                       if getattr(self, n) is None]
            if missing:
                raise ValueError(
                    "frozen-map fallback requires complete row identity fields: "
                    + ", ".join(missing)
                )
            if self.host_identity_source != "FROZEN_REVIEWED_UID_MAP":
                raise ValueError(
                    "frozen-map fallback must declare "
                    "host_identity_source=FROZEN_REVIEWED_UID_MAP"
                )
        if self.host_resolution is not None and self.host_resolution != "UNRESOLVED":
            if not (sig and self.host_taxid and self.host_name):
                raise ValueError(
                    "resolved host_resolution requires host identity "
                    "signature/host_taxid/host_name"
                )
        return self


class OrganismCandidate(BaseModel):
    """聚合后的候选菌（M5: OrganismAggregator 输出，框架 §3.3）

    严格对齐学生权威实现（microbe_crew/tools/organism_aggregator.py，15 tests passed）：
    - MT-D3（2026-07-16 裁定 B / 学生 07-27 DECIDED_AND_IMPLEMENTED）排序主键 =
      supporting-enzyme count 降序 + NCBI taxon ID 数字升序 tie-break。
    - MT-D2：v1 不输出 organism_confidence float；原始证据维度经 per_enzyme_source_provenance 透传。
    - MT-D1：仅按 reviewed 宿主的 NCBI taxon 分组；无 reviewed 映射的酶不纳入。
    - aggregation_notes 为导师侧可观测性附加字段（学生 schema 无此项，不影响排序/语义）。
    """
    organism_uid: str                     # = str(ncbi_taxon_id)
    taxonomy_namespace: Literal["NCBI_taxon"] = "NCBI_taxon"
    ncbi_taxon_id: int
    organism_name: str                    # 组内首个（按 rank,uid 排序）scientific name
    organism_name_variants: List[str] = Field(default_factory=list)  # 同 taxon 下去重名称
    supporting_enzymes: List[SupportingEnzyme] = Field(default_factory=list)
    supporting_enzyme_count: int          # MT-D3 排序主键（降序）
    per_enzyme_source_provenance: List[EnzymeSourceProvenance] = Field(default_factory=list)  # MT-D2 原始维度透传
    default_order_rank: int = 0           # 排序后 1-based 名次
    aggregation_notes: Optional[str] = None
    # G4-R2A（§9）：聚合后的候选菌必须显式携带其宿主 identity 签名——合并主键从
    # “仅 ncbi_taxon_id”改为“宿主 identity 签名（taxon 仍为生产主键与 MT-D3 tie-break）”。
    host_identity_source_signature: Optional[str] = None


class OrganismRecommendation(BaseModel):
    """选菌层（MicrobeSelectionAgent）有界推荐——D6 约束下的 LLM 理由层。

    授权边界（学生 07-27 §4.6 / D6）：M4b TraitFilterLayer 与 M4c 完整决策层 NOT AUTHORIZED，
    当前仅允许「按既有聚合主键（MT-D3）呈现 Top-K + 生成有界理由」。因此本模型：
    - 不含 trait_score / total_score（依赖 M4b，锁定）。
    - default_order_rank 直接沿用 OrganismCandidate 的 MT-D3 确定性名次，LLM 不得覆盖。
    - 候选池成员由确定性聚合决定，LLM 不得增删。

    D6 硬约束：每条 recommended 至少引用 2 条可追溯 evidence；证据不足置
    insufficient_evidence/unknown；冲突 / no_robust_majority 进 uncertainty_flags；
    禁止把 soft evidence 改写成 hard exclusion。
    """
    organism_uid: str
    organism_name: str
    ncbi_taxon_id: int
    default_order_rank: int                       # 沿用 MT-D3 确定性名次（LLM 不覆盖）
    supporting_enzyme_count: int
    recommendation_status: Literal["recommended", "insufficient_evidence", "unknown"]
    cited_evidence: List[str] = Field(default_factory=list)  # D6：recommended 需 ≥2 条可追溯 evidence
    rationale: str                                # LLM 有界理由（仅解释既有证据，不创造数值）
    uncertainty_flags: List[str] = Field(default_factory=list)


class TraitRecord(BaseModel):
    """性状记录（M5: TraitFilterNode，集成 metaTraits）"""
    trait_name: str
    value: Any
    is_ai: bool                    # 独立布尔
    majority_label: Optional[str] = None  # 独立聚合标签
    source_database: Optional[str] = None
    source_url: Optional[str] = None
    tax_id: Optional[int] = None


# T5B/T6: C8 read-only trait objects. These are evidence objects, not new public state keys.
GSCHEMA_TRAIT_RESOLUTIONS = (
    "EXACT_STRAIN", "SPECIES", "REPRESENTATIVE_STRAIN", "IDENTITY_ONLY", "UNRESOLVED"
)


class TraitEvidence(BaseModel):
    trait_id: Literal["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15"]
    trait_value: Optional[Any] = None
    trait_evidence_class: Literal["OBSERVED", "PREDICTED", "MISSING", "IDENTITY_ONLY", "CONFLICT"]
    trait_resolution: Literal["EXACT_STRAIN", "SPECIES", "REPRESENTATIVE_STRAIN", "IDENTITY_ONLY", "UNRESOLVED"]
    trait_source: Optional[str] = None
    source_record_id: Optional[str] = None
    source_tool: str = "c8_trait_annotation_readonly"
    model_version: Optional[str] = None
    evidence_hash: Optional[str] = None
    used_for_hard_filtering: Literal[False] = False
    used_for_ranking: Literal[False] = False
    direct_target_degradation_claim: Literal[False] = False
    trait_warning: List[str] = Field(default_factory=list)


class HostTraitAnnotation(BaseModel):
    enzyme_uid: str
    source_signature: str
    host_taxid: Optional[int] = None
    host_name: Optional[str] = None
    host_resolution: Literal["EXACT_STRAIN", "SPECIES", "REPRESENTATIVE_STRAIN", "UNRESOLVED"] = "UNRESOLVED"
    host_taxonomy_group: Optional[str] = None
    host_evidence_sources: List[Literal["UNIPROT_REVIEWED", "KEGG_SUPPLEMENT", "BACDIVE_OBSERVED", "UNRESOLVED"]] = Field(
        default_factory=lambda: ["UNRESOLVED"], min_length=1
    )
    traits: Dict[str, TraitEvidence] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _check_trait_warning_array(self):
        for evidence in self.traits.values():
            if not isinstance(evidence.trait_warning, list):
                raise ValueError("trait_warning must always be an array")
        return self

    @model_validator(mode="after")
    def _check_host_evidence_sources(self):
        if not self.host_evidence_sources:
            raise ValueError("host_evidence_sources must be non-empty")
        if len(self.host_evidence_sources) != len(set(self.host_evidence_sources)):
            raise ValueError("host_evidence_sources must be unique")
        return self


# ─── G2: 唯一 T2B v3.2 PredictedReaction（黄老师 2026-09-09 裁定 3）───
# 定义取自 T2B v3.2 累计 SOURCE_PATCH（SHA256=3b592f744feec2f5d2dcc6508a87e457a0bd35aa199a34780dec7d95d974bd10）。
# 决策红线：禁用 confidence；不恢复旧强制 prediction_method；全仓仅此一个定义。

class PredictionScore(BaseModel):
    """预测分数：raw_score 语义严格（无 confidence，无校准概率声明）。"""
    raw_score: float
    score_semantics: str = "ns_score_max_per_source_probability_over_3"
    is_calibrated_probability: bool = False


class PredictedReaction(BaseModel):
    """T2B 单 SMILES v3.2 预测反应（staged adapter 输出）。

    禁用字段（决策红线）: confidence。
    规则引擎（如 BioTransformer ENVMICRO）无概率输出时，必须显式给出非概率
    score_semantics 并置 is_calibrated_probability=False、raw_score=0.0，
    在 warnings 中注明语义缺席，不得伪造概率。
    """
    reaction_smiles: str  # canonical_parent>>canonical_product
    prediction_rank: int = Field(..., ge=1)
    prediction_score: PredictionScore
    source_tag: str
    source_tool: str = "depending_bbd_v3.2"
    model_version: str = "depending_bbd_v3.2"
    provenance: str
    source_record_id: Optional[str] = None
    evidence_hash: Optional[str] = None
    depth: int = Field(..., ge=1)
    parent_node_smiles: Optional[str] = None
    parent_node_depth: Optional[int] = None
    warnings: List[str] = Field(default_factory=list)


# ─── G4: host 证据来源合法枚举（黄老师 2026-09-09 裁定 4）───
# 未解析 host 一律大写 UNRESOLVED；N/A、空串、小写 unresolved 等一律非法。

HOST_SOURCE_LITERALS = (
    "UNIPROT_REVIEWED",
    "KEGG_SUPPLEMENT",
    "BACDIVE_OBSERVED",
    "UNRESOLVED",
)
HostSource = Literal["UNIPROT_REVIEWED", "KEGG_SUPPLEMENT", "BACDIVE_OBSERVED", "UNRESOLVED"]


def validate_host_source(value: str) -> str:
    """校验 host 来源字面量：仅接受四个合法大写枚举，非法值直接拒绝。"""
    if isinstance(value, str) and value in HOST_SOURCE_LITERALS:
        return value
    raise ValueError(
        f"illegal host source literal: {value!r}; "
        f"allowed: {', '.join(HOST_SOURCE_LITERALS)}"
    )


# ─── G4-R1: host 证据真实字段模型（T6-R3A-R1，黄老师 2026-09-09 纠错裁定）───
# 将上方 G4 四项 source 常量实际用于 production host evidence 字段（不再是无生产消费的孤儿 helper）。
# 字段名与冻结 G-SCHEMA（THREE_MODULE_EVIDENCE_CHAIN_SCHEMA V0.1 2026-09-05）hostEvidence $defs 一致：
# host_evidence_source 为单数形态的非空唯一列表；host_resolution 独立使用四项 identity-resolution 枚举。
# 八条最小修正映射（T6-R3A-R1 §7）：
#   1. HOST_SOURCE_LITERALS/HostSource/validate_host_source 直接作为 host_evidence_source 的类型与校验器；
#   2. host_evidence_source 非空、唯一、合法列表；
#   3. host_resolution 单独使用四项枚举；
#   4. UNRESOLVED source 若出现必须独占；
#   5. resolution=UNRESOLVED 时不得伪造 source_signature/host_taxid/host_name；
#   6. resolved resolution 必须有 source_signature、正整数 taxonId、非空 host name；
#   7. reviewed 证据由 producer 显式传入真实字段，模型层无默认值可覆盖；
#   8. 不修改冻结 G-SCHEMA；本模型输出可直接映射为 schema hostEvidence 子对象。

# G4-R2A 注：HOST_RESOLUTION_LITERALS / HostResolution 定义已上移至 M5 扩展模型段首
# （供 EnzymeSourceProvenance / MicrobeCandidate 注解引用），此处不再重复定义。
_EVIDENCE_SHA256_PATTERN = _SHA256_PATTERN


class HostEvidenceRecord(BaseModel):
    """单酶宿主证据记录（production host evidence 字段，对齐冻结 G-SCHEMA hostEvidence $defs）。

    producer：src/tools/microbe_recommender.build_host_evidence_record（reviewed 分支取
    UniProtReviewedHostEvidence 真实字段；无 reviewed 分支强制 UNRESOLVED 且身份字段全 None）。
    """

    enzyme_uid: str
    # 宿主 identity 签名（来自 identity resolver/map 行或 §5 确定性构造）；
    # UniProt accession 属于 evidence record identity，留在 source_record_id。
    source_signature: Optional[str] = None
    host_taxid: Optional[int] = Field(default=None, ge=1)
    host_name: Optional[str] = None
    host_resolution: HostResolution
    host_evidence_source: List[HostSource]
    source_record_id: str
    evidence_hash: str
    warnings: List[str] = Field(default_factory=list)
    # G4-R2A：解析路由与 identity 来源是生产侧可读元数据。冻结 G-SCHEMA hostEvidence 是
    # additionalProperties=false 的 9 字段契约，故二者标为 exclude（投影时自动不出现），
    # 并由 producer 在 warnings 内以 "resolution_route=<ROUTE>" 显式留痕（schema 合法且必读）。
    resolution_route: Optional[HostResolutionRoute] = Field(default=None, exclude=True)
    host_identity_source: Optional[HostIdentitySource] = Field(default=None, exclude=True)

    @field_validator("host_evidence_source")
    @classmethod
    def _host_evidence_source_contract(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("host_evidence_source must be a non-empty list")
        for item in v:
            validate_host_source(item)
        if len(set(v)) != len(v):
            raise ValueError("host_evidence_source entries must be unique")
        if "UNRESOLVED" in v and len(v) != 1:
            raise ValueError(
                "UNRESOLVED host source must appear alone, never alongside "
                "UNIPROT_REVIEWED/KEGG_SUPPLEMENT/BACDIVE_OBSERVED"
            )
        return v

    @field_validator("evidence_hash")
    @classmethod
    def _evidence_hash_is_sha256(cls, v: str) -> str:
        if not _EVIDENCE_SHA256_PATTERN.fullmatch(v):
            raise ValueError(
                "evidence_hash must be a 64-char lowercase hex SHA256 digest"
            )
        return v

    @model_validator(mode="after")
    def _resolution_identity_contract(self):
        if self.host_resolution == "UNRESOLVED":
            if self.host_evidence_source != ["UNRESOLVED"]:
                raise ValueError(
                    "host_resolution=UNRESOLVED requires host_evidence_source==['UNRESOLVED']"
                )
            if (
                self.source_signature is not None
                or self.host_taxid is not None
                or self.host_name is not None
            ):
                raise ValueError(
                    "host_resolution=UNRESOLVED forbids fabricated "
                    "source_signature/host_taxid/host_name"
                )
        else:
            if "UNRESOLVED" in self.host_evidence_source:
                raise ValueError(
                    "resolved host_resolution forbids UNRESOLVED in host_evidence_source"
                )
            if not (self.source_signature and self.source_signature.strip()):
                raise ValueError(
                    "resolved host_resolution requires a non-empty source_signature"
                )
            if self.host_taxid is None or self.host_taxid < 1:
                raise ValueError(
                    "resolved host_resolution requires a positive integer host_taxid"
                )
            if not (self.host_name and self.host_name.strip()):
                raise ValueError(
                    "resolved host_resolution requires a non-empty host_name"
                )
            # G4-R2A 根因 C：宿主签名不得就是该酶自己的 UID
            if host_signature_is_enzyme_uid_shaped(self.enzyme_uid, self.source_signature):
                raise ValueError(
                    "resolved host record requires a HOST identity source_signature; got an "
                    f"enzyme-UID-shaped value {self.source_signature!r} for enzyme_uid "
                    f"{self.enzyme_uid!r} (T6-R3A-R2A §5: uniprotkb_reviewed:<enzyme_uid> "
                    "must no longer be generated as a host source_signature)"
                )
        return self


class IntentClassification(BaseModel):
    """用户意图分类（M5: OrchestratorNode LLM 输出）"""
    intent: Literal[
        "enzyme_recommendation",     # 标准底物→反应→酶流程
        "microbe_recommendation",    # 进一步推荐微生物
        "trait_query",               # 查询微生物性状
        "reaction_exploration",      # 探索反应路径
        "general_question",          # 一般问题
    ]
    confidence: float
    extracted_entities: dict[str, Any] = Field(default_factory=dict)


class RouteStepHostAnnotation(BaseModel):
    reaction_task_id: str
    enzyme_uid: str
    enzyme_rank: int = Field(..., ge=1)
    source_signature: str
    host_taxid: Optional[int] = None
    host_name: Optional[str] = None
    host_resolution: Literal["EXACT_STRAIN", "SPECIES", "REPRESENTATIVE_STRAIN", "UNRESOLVED"]
    host_taxonomy_group: Optional[str] = None
    host_evidence_sources: List[Literal["UNIPROT_REVIEWED", "KEGG_SUPPLEMENT", "BACDIVE_OBSERVED", "UNRESOLVED"]] = Field(default_factory=list)
    traits: Dict[str, TraitEvidence] = Field(default_factory=dict)


class RouteAggregationInput(BaseModel):
    route_id: str
    ordered_reaction_task_ids: List[str]
    step_host_annotations: List[RouteStepHostAnnotation] = Field(default_factory=list)
