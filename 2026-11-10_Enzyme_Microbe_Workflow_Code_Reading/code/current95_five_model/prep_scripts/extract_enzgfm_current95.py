#!/usr/bin/env python3
"""Extract frozen EnzGFM-650M global and pocket-node features in shards.

This script deliberately consumes an already audited structure-to-FASTA mapping.
It does not infer pockets or align structures.  The input CSV must contain one
frozen carrier UID per original sequence and 1-based FASTA pocket indices.

Each worker owns one deterministic sequence-SHA shard, loads EnzGFM once, and
writes atomic chunk files.  A later merge step creates the exact files consumed
by EnzymeCAGE: an exact-sequence keyed global pickle and a UID-keyed pocket
mapping.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Iterable


REQUIRED_COLUMNS = {
    "UniprotID",
    "sequence",
    "sequence_sha256",
    "pocket_indices_1based",
    "pocket_hash",
    "pocket_source",
}
UZOB_RE = re.compile(r"[UZOB]")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_sequence(sequence: str) -> str:
    return UZOB_RE.sub("X", sequence)


def parse_indices(raw: str, length: int) -> list[int]:
    tokens = [part.strip() for part in str(raw).replace(";", ",").split(",")]
    try:
        indices = [int(part) for part in tokens if part]
    except ValueError as exc:
        raise ValueError(f"non-integer pocket index: {raw!r}") from exc
    if not indices:
        raise ValueError("empty pocket index list")
    # TASK-LOCAL ADAPTATION (P1_r1, contract §5.3): the OLD frozen corrected
    # pocket indices are stored in lexicographic (string-sorted) row order,
    # which the preimage rejected via the numeric-ascending guard. Here the
    # frozen ROW ORDER is honored verbatim for slicing; the guard is replaced
    # by explicit duplicate + range validation (both previously present).
    if len(indices) != len(set(indices)):
        raise ValueError("duplicate pocket indices")
    if min(indices) < 1 or max(indices) > length:
        raise ValueError(f"pocket index outside 1..{length}")
    return indices


def assigned_shard(sequence_sha256: str, num_shards: int) -> int:
    return int(sequence_sha256[:16], 16) % num_shards


def read_carriers(path: Path, shard_index: int, num_shards: int, max_sequence_length: int = 1000) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    uid_to_sha: dict[str, str] = {}
    uid_to_ph: dict[str, str] = {}
    sequence_to_uid: dict[str, str] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"carrier CSV missing columns: {sorted(missing)}")
        added: set[tuple[str, str]] = set()
        for line_number, row in enumerate(reader, start=2):
            uid = str(row["UniprotID"]).strip().lstrip(">")
            sequence = str(row["sequence"]).strip().upper()
            declared_sha = str(row["sequence_sha256"]).strip().lower()
            if not uid or not sequence:
                raise ValueError(f"line {line_number}: empty UID or sequence")
            observed_sha = sha256_text(sequence)
            if observed_sha != declared_sha:
                raise ValueError(
                    f"line {line_number}: sequence SHA mismatch for {uid}: "
                    f"{observed_sha} != {declared_sha}"
                )
            if not 1 <= len(sequence) <= max_sequence_length:
                raise ValueError(f"line {line_number}: sequence length outside 1..{max_sequence_length}")
            if uid in uid_to_sha and uid_to_sha[uid] != declared_sha:
                raise ValueError(f"UID {uid} maps to multiple sequence SHAs")
            # TASK-LOCAL ADAPTATION (P1_r1, contract §5): the preimage rejected
            # one sequence with multiple carrier UIDs. Here multiple UIDs per
            # sequence are ALLOWED (§5 requires one forward per unique
            # sequence with per-UID slicing); identity of UID->sequence stays
            # 1:1 and an identical duplicate row (uid+sha+pocket+hash) is
            # deduplicated, while a UID reused with a different pocket
            # definition is still rejected below via pocket_hash.
            indices = parse_indices(row["pocket_indices_1based"], len(sequence))
            pocket_hash = str(row["pocket_hash"]).strip()
            if uid in uid_to_ph and uid_to_ph[uid] != pocket_hash:
                raise ValueError(
                    f"line {line_number}: UID {uid} reused with a different "
                    f"pocket definition ({uid_to_ph[uid]} vs {pocket_hash})")
            uid_to_ph[uid] = pocket_hash
            row_key = (uid, pocket_hash)
            if row_key in added:
                continue
            added.add(row_key)
            uid_to_sha[uid] = declared_sha
            normalized = normalize_sequence(sequence)
            record = {
                "uid": uid,
                "sequence": sequence,
                "sequence_sha256": declared_sha,
                "normalized_sequence": normalized,
                "normalized_sequence_sha256": sha256_text(normalized),
                "uzob_replacement_count": sum(sequence.count(aa) for aa in "UZOB"),
                "sequence_length": len(sequence),
                "pocket_indices_1based": indices,
                "pocket_hash": pocket_hash,
                "pocket_source": str(row["pocket_source"]).strip(),
            }
            if assigned_shard(declared_sha, num_shards) == shard_index:
                rows.append(record)
    # deterministic order; rows sharing a normalized sequence end up adjacent,
    # infer_batch additionally groups by exact normalized sequence
    rows_sorted = sorted(rows, key=lambda item: (item["sequence_length"], item["sequence_sha256"], item["uid"]))
    _ = sequence_to_uid  # preimage global-uniqueness map intentionally unused
    return rows_sorted


def torch_load_trusted(path: Path, torch: Any) -> Any:
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


def existing_uids(chunk_dir: Path, torch: Any) -> tuple[set[str], int]:
    seen: set[str] = set()
    max_index = -1
    for path in sorted(chunk_dir.glob("chunk_*.pt")):
        try:
            max_index = max(max_index, int(path.stem.split("_")[-1]))
        except ValueError:
            raise ValueError(f"unexpected chunk filename: {path.name}")
        obj = torch_load_trusted(path, torch)
        if obj.get("__format__") != "enzgfm650m_feature_chunk_v1":
            raise ValueError(f"unexpected chunk format in {path}")
        overlap = seen.intersection(obj["entries"])
        if overlap:
            raise ValueError(f"duplicate UID across existing chunks: {sorted(overlap)[:5]}")
        seen.update(obj["entries"])
    return seen, max_index + 1


def make_batches(
    rows: list[dict[str, Any]], max_batch_size: int, max_batch_tokens: int
) -> Iterable[list[dict[str, Any]]]:
    # TASK-LOCAL ADAPTATION (P1_r1): batching operates on GROUPS of rows that
    # share one normalized sequence, so a sequence is never split across
    # batches (contract §5.2: exactly one forward per unique sequence, and all
    # its UIDs see bit-identical hidden states inside one batch). Batch limits
    # count unique sequences (forward slots), matching infer_batch's grouping.
    groups: dict[str, list[dict[str, Any]]] = {}
    order: list[str] = []
    for row in rows:
        if row["normalized_sequence"] not in groups:
            groups[row["normalized_sequence"]] = []
            order.append(row["normalized_sequence"])
        groups[row["normalized_sequence"]].append(row)
    batch: list[dict[str, Any]] = []
    max_len = 0
    for key in order:
        group = groups[key]
        row_tokens = group[0]["sequence_length"] + 2
        proposed_max = max(max_len, row_tokens)
        proposed_size = len(batch) + 1
        if batch and (
            proposed_size > max_batch_size
            or proposed_max * proposed_size > max_batch_tokens
        ):
            yield batch
            batch = []
            max_len = 0
        batch.extend(group)
        max_len = max(max_len, row_tokens)
    if batch:
        yield batch


def verify_token_alignment(tokenizer: Any, ids: Any, mask: Any, row: dict[str, Any]) -> None:
    valid_len = int(mask.sum().item())
    expected_len = row["sequence_length"] + 2
    if valid_len != expected_len:
        raise ValueError(f"token length {valid_len} != L+2={expected_len}")
    tokens = tokenizer.convert_ids_to_tokens(ids[:valid_len].tolist())
    if tokens[0] != "<cls>" or tokens[-1] != "<eos>":
        raise ValueError(f"unexpected special-token boundary: {tokens[:1]} ... {tokens[-1:]}")
    if tokens[1:-1] != list(row["normalized_sequence"]):
        raise ValueError("token/residue identity mismatch")


def infer_batch(
    rows: list[dict[str, Any]], tokenizer: Any, model: Any, device: Any, torch: Any,
    max_width: int = 1022
) -> dict[str, dict[str, Any]]:
    # TASK-LOCAL ADAPTATION (P1_r1, contract §5.2): forward runs once per UNIQUE
    # normalized sequence inside the batch; every UID sharing that sequence is
    # sliced from the same hidden state with its own frozen 1-based pocket
    # indices. All preimage per-row validations are retained.
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(row["normalized_sequence"], []).append(row)
    keys = list(groups)
    encoded = tokenizer.batch_encode_plus(
        keys,
        add_special_tokens=True,
        padding=True,
        truncation=False,
        return_tensors="pt",
    )
    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device)
    if input_ids.shape[1] > max_width:
        raise ValueError(f"encoded batch width {input_ids.shape[1]} exceeds model capacity {max_width}")
    with torch.no_grad():
        output = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            ec_numbers=[""] * len(keys),
        )
    hidden = output.last_hidden_state
    if hidden.ndim != 3 or hidden.shape[0] != len(keys):
        raise ValueError(f"unexpected hidden shape: {tuple(hidden.shape)}")
    hidden_size = int(model.config.hidden_size)
    if hidden_size != 2048 or hidden.shape[2] != hidden_size:
        raise ValueError(f"unexpected EnzGFM hidden size: config={hidden_size}, tensor={hidden.shape[2]}")

    result: dict[str, dict[str, Any]] = {}
    for key_index, key in enumerate(keys):
        group = groups[key]
        row0 = group[0]
        verify_token_alignment(tokenizer, input_ids[key_index],
                               attention_mask[key_index], row0)
        length = row0["sequence_length"]
        for row in group:
            if row["sequence_length"] != length:
                raise ValueError(f"{row['uid']}: shared group length mismatch")
        residue_feature = hidden[key_index, 1 : length + 1].float()
        global_feature = residue_feature.mean(dim=0).cpu().contiguous()
        if tuple(global_feature.shape) != (2048,):
            raise ValueError(f"{row0['uid']}: bad global shape {tuple(global_feature.shape)}")
        if not torch.isfinite(global_feature).all():
            raise ValueError(f"{row0['uid']}: NaN/Inf global feature")
        if int(torch.count_nonzero(global_feature)) == 0:
            raise ValueError(f"{row0['uid']}: all-zero global feature")
        for row in group:
            token_indices = torch.tensor(row["pocket_indices_1based"],
                                         device=device, dtype=torch.long)
            pocket_feature = hidden[key_index].index_select(0, token_indices).float().cpu().contiguous()
            if tuple(pocket_feature.shape) != (len(row["pocket_indices_1based"]), 2048):
                raise ValueError(f"{row['uid']}: bad pocket shape {tuple(pocket_feature.shape)}")
            if not torch.isfinite(pocket_feature).all():
                raise ValueError(f"{row['uid']}: NaN/Inf pocket feature")
            if int(torch.count_nonzero(pocket_feature)) == 0:
                raise ValueError(f"{row['uid']}: all-zero pocket feature")
            result[row["uid"]] = {
                "sequence": row["sequence"],
                "sequence_sha256": row["sequence_sha256"],
                "normalized_sequence_sha256": row["normalized_sequence_sha256"],
                "uzob_replacement_count": row["uzob_replacement_count"],
                "sequence_length": length,
                "pocket_indices_1based": row["pocket_indices_1based"],
                "pocket_hash": row["pocket_hash"],
                "pocket_source": row["pocket_source"],
                "global_feature": global_feature,
                "pocket_feature": pocket_feature,
            }
    return result


def atomic_torch_save(obj: Any, destination: Path, torch: Any) -> None:
    temporary = destination.with_name(destination.name + ".tmp")
    torch.save(obj, temporary)
    os.replace(temporary, destination)


def write_failures(path: Path, failures: list[dict[str, str]]) -> None:
    fields = ["UniprotID", "sequence_sha256", "stage", "error_type", "error"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(failures)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--carrier-csv", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--tokenizer-dir", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--num-shards", type=int, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--max-sequence-length", type=int, default=1000)
    parser.add_argument("--max-batch-size", type=int, default=4)
    parser.add_argument("--max-batch-tokens", type=int, default=2048)
    parser.add_argument("--chunk-entries", type=int, default=128)
    parser.add_argument("--repo-commit", default="")
    parser.add_argument("--weight-sha256", default="")
    args = parser.parse_args()

    if not 0 <= args.shard_index < args.num_shards:
        raise ValueError("shard-index must be in [0, num-shards)")
    if min(args.max_batch_size, args.max_batch_tokens, args.chunk_entries) <= 0:
        raise ValueError("batch and chunk limits must be positive")

    import torch
    from transformers import EsmTokenizer

    sys.path.insert(0, str(args.repo_root))
    from models import EnzGFM_Model

    shard_root = args.output_root / f"shard_{args.shard_index:03d}_of_{args.num_shards:03d}"
    chunk_dir = shard_root / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=False if not shard_root.exists() else True)

    all_rows = read_carriers(args.carrier_csv, args.shard_index, args.num_shards, args.max_sequence_length)
    _cfg = json.loads((args.model_dir / "config.json").read_text())
    _cap = _cfg.get("max_position_embeddings")
    _pos = _cfg.get("position_embedding_type", "absolute")
    if _cap and _pos != "rotary" and any(r["sequence_length"] + 2 > int(_cap) for r in all_rows):
        raise ValueError("MODEL_POSITION_CAPACITY_REQUIRES_EXACT_FULL_LENGTH_ROUTE_NO_TRUNCATION")
    # R4 adaptation (WIDTH_GUARD_20261103): the literal 1022 batch-width bound
    # was inherited from the old 1000-aa CSV guard; the REAL capacity comes
    # from the frozen model config (jamba hybrid: n_ctx=65536, no absolute
    # max_position_embeddings; a 1189-token GPU forward is verified finite in
    # ENZGFM_ENCODER_CPU_WIRING.json). The guard stays — bound to the config
    # capacity instead of the legacy literal. No truncation, no numeric change.
    _max_width = int(_cap) if (_cap and _pos != "rotary") else int(_cfg.get("n_ctx") or 1022)
    completed, next_chunk_index = existing_uids(chunk_dir, torch)
    rows = [row for row in all_rows if row["uid"] not in completed]

    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    tokenizer = EsmTokenizer.from_pretrained(str(args.tokenizer_dir))
    model = EnzGFM_Model.from_pretrained(str(args.model_dir)).to(device).eval()
    if int(model.config.hidden_size) != 2048:
        raise ValueError(f"checkpoint hidden_size={model.config.hidden_size}, expected 2048")

    start = time.time()
    failures: list[dict[str, str]] = []
    chunk_entries: dict[str, dict[str, Any]] = {}

    def flush() -> None:
        nonlocal chunk_entries, next_chunk_index
        if not chunk_entries:
            return
        destination = chunk_dir / f"chunk_{next_chunk_index:06d}.pt"
        payload = {
            "__format__": "enzgfm650m_feature_chunk_v1",
            "hidden_size": 2048,
            "entries": chunk_entries,
        }
        atomic_torch_save(payload, destination, torch)
        chunk_entries = {}
        next_chunk_index += 1

    for batch in make_batches(rows, args.max_batch_size, args.max_batch_tokens):
        try:
            inferred = infer_batch(batch, tokenizer, model, device, torch, _max_width)
            chunk_entries.update(inferred)
        except Exception as batch_error:
            if device.type == "cuda":
                torch.cuda.empty_cache()
            for row in batch:
                try:
                    inferred = infer_batch([row], tokenizer, model, device, torch, _max_width)
                    chunk_entries.update(inferred)
                except Exception as single_error:
                    failures.append(
                        {
                            "UniprotID": row["uid"],
                            "sequence_sha256": row["sequence_sha256"],
                            "stage": "single_retry_after_batch_failure",
                            "error_type": type(single_error).__name__,
                            "error": str(single_error),
                        }
                    )
            print(
                f"batch fallback: {type(batch_error).__name__}: {batch_error}",
                file=sys.stderr,
                flush=True,
            )
        if len(chunk_entries) >= args.chunk_entries:
            flush()
    flush()
    write_failures(shard_root / "failures.csv", failures)

    final_completed, _ = existing_uids(chunk_dir, torch)
    expected_uids = {row["uid"] for row in all_rows}
    unexpected = final_completed - expected_uids
    missing = expected_uids - final_completed - {row["UniprotID"] for row in failures}
    if unexpected or missing:
        raise RuntimeError(
            f"shard closure failed: unexpected={len(unexpected)} missing_untyped={len(missing)}"
        )
    run_manifest = {
        "format": "enzgfm650m_extraction_shard_v1",
        "shard_index": args.shard_index,
        "num_shards": args.num_shards,
        "expected": len(expected_uids),
        "success": len(final_completed),
        "failed": len(failures),
        "hidden_size": 2048,
        "repo_root": str(args.repo_root.resolve()),
        "repo_commit": args.repo_commit,
        "model_dir": str(args.model_dir.resolve()),
        "tokenizer_dir": str(args.tokenizer_dir.resolve()),
        "weight_sha256": args.weight_sha256,
        "global_pooling": "mean_real_residue_tokens_only",
        "special_tokens_in_global": False,
        "pocket_index_contract": "1-based FASTA index equals token index with CLS at zero",
        "truncation": False,
        "task_local_adaptation": "P1_r1: one forward per unique normalized sequence; multiple carrier UIDs per sequence allowed with per-UID slicing (preimage rejected it)",
        "elapsed_seconds": round(time.time() - start, 3),
    }
    (shard_root / "RUN_MANIFEST.json").write_text(
        json.dumps(run_manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(run_manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

