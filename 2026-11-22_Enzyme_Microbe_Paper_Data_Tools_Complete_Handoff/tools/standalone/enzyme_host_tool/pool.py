"""Candidate pool (R2): retain everything; no subset selection. max_size if
configured and exceeded BLOCKS the whole step (handled in predict) — the pool
itself never slices."""
from __future__ import annotations

from .schemas import PoolCandidate


def _uid_tokens(pair):
    ids = []
    cpid = str(pair.get("canonical_protein_id", "")).strip()
    if cpid:
        ids.append(cpid)
    for tok in str(pair.get("accessions", "")).split(";"):
        tok = tok.strip()
        if tok and tok not in ids:
            ids.append(tok)
    return ids


def build_pool(groups, retrieval_backend):
    by_sha = {}
    rows = 0
    for g in groups:
        rows_src = getattr(g, "pair_rows", None)
        if rows_src is None:
            rows_src = retrieval_backend.expand_pairs(list(g.group_cds))
        for pair in rows_src:
            rows += 1
            sha = str(pair.get("sequence_sha256", ""))
            if not sha:
                continue
            c = by_sha.get(sha)
            if c is None:
                c = PoolCandidate(sequence_sha256=sha, canonical_protein_id="", associated_uids=[],
                                  provenance_records=[])
                by_sha[sha] = c
            if not c.canonical_protein_id:
                c.canonical_protein_id = str(pair.get("canonical_protein_id", ""))
            for uid in _uid_tokens(pair):
                if uid not in c.associated_uids:
                    c.associated_uids.append(uid)
            c.provenance_records.append(dict(pair))
            for tok in str(pair.get("source_datasets", "")).split(";"):
                if tok.strip() and tok.strip() not in c.sources:
                    c.sources.append(tok.strip())
            for tok in str(pair.get("evidence_tiers", "")).split(";"):
                if tok.strip() and tok.strip() not in c.evidence_tiers:
                    c.evidence_tiers.append(tok.strip())
    # Preserve the first-return/R1 scoring batch order by sequence SHA.
    cands = [by_sha[s] for s in sorted(by_sha)]
    return cands, rows


def scoring_pairs(cands):
    """Scoring representative = the candidate's canonical protein id
    (asset carrier role recorded separately in provenance rows)."""
    return [(c.canonical_protein_id, c.sequence_sha256) for c in cands if c.canonical_protein_id]


def all_display_uids(cands):
    seen, out = set(), []
    for c in cands:
        for u in c.associated_uids:
            if u not in seen:
                seen.add(u)
                out.append(u)
    return out
