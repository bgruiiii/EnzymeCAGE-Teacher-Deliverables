#!/usr/bin/env python3
"""Build EnzymeCAGE-training-compatible reaction inputs for Pollutant298.

This reproduces the reaction transformation chain in scripts/rhea_data_cleaning.py
without changing the frozen source reaction or candidate identities.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tarfile
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

from rdkit import Chem, DataStructs, rdBase
from rdkit.Chem import AllChem


SOURCE_MEMBER = (
    "pollutant298_three_model_reaction_benchmark_freeze_r5_20260921/"
    "restricted/POLLUTANT298_REACTION_PROVENANCE.tsv"
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def get_rdkit_mol(mol):
    if isinstance(mol, str):
        mol = Chem.MolFromSmiles(mol)
    return mol


def cano_smiles(smiles: str, remain_isomer: bool = True):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return None
    return Chem.MolToSmiles(mol, isomericSmiles=remain_isomer)


def calc_similarity(mol1, mol2) -> float:
    mol1 = get_rdkit_mol(mol1)
    mol2 = get_rdkit_mol(mol2)
    fp1 = AllChem.GetMorganFingerprint(mol1, 2)
    fp2 = AllChem.GetMorganFingerprint(mol2, 2)
    return DataStructs.TanimotoSimilarity(fp1, fp2)


def remove_duplicate_mols(mols1: list[str], mols2: list[str]):
    tmp1 = deepcopy(mols1)
    for mol1 in tmp1:
        for mol2 in mols2:
            if calc_similarity(mol1, mol2) == 1:
                mols1.remove(mol1)
                mols2.remove(mol2)
                break
    return mols1, mols2


def neutralize_atoms(smi: str) -> str:
    try:
        mol = get_rdkit_mol(smi)
        pattern = Chem.MolFromSmarts(
            "[+1!h0!$([*]~[-1,-2,-3,-4]),-1!$([*]~[+1,+2,+3,+4])]"
        )
        matches = [match[0] for match in mol.GetSubstructMatches(pattern)]
        for atom_index in matches:
            atom = mol.GetAtomWithIdx(atom_index)
            charge = atom.GetFormalCharge()
            hydrogen_count = atom.GetTotalNumHs()
            atom.SetFormalCharge(0)
            atom.SetNumExplicitHs(hydrogen_count - charge)
            atom.UpdatePropertyCache()
        neutral = Chem.MolToSmiles(mol)
        if not get_rdkit_mol(neutral):
            neutral = smi
        return neutral
    except Exception:
        return smi


def neutralize_rxn(rxn: str):
    if not rxn:
        return None
    reactants = [neutralize_atoms(smi) for smi in rxn.split(">>")[0].split(".")]
    products = [neutralize_atoms(smi) for smi in rxn.split(">>")[1].split(".")]
    return ".".join(reactants) + ">>" + ".".join(products)


def remove_redundent_from_rxn(rxn: str, items_to_remove=None):
    if not rxn:
        return None
    if not items_to_remove:
        items_to_remove = ["*", "[H+]", "[H]*[H]"]
    reactants = [
        smi for smi in rxn.split(">>")[0].split(".") if smi not in items_to_remove
    ]
    products = [
        smi for smi in rxn.split(">>")[1].split(".") if smi not in items_to_remove
    ]
    reactants, products = remove_duplicate_mols(reactants, products)
    if not reactants or not products:
        return None
    return ".".join(reactants) + ">>" + ".".join(products)


def count_carbon_atoms(smiles: str) -> int:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return 0
    return sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == "C")


def filter_unwanted_rxn(rxn: str):
    if not rxn:
        return None
    reactant_side, product_side = rxn.split(">>")
    reactant_mol = get_rdkit_mol(reactant_side)
    product_mol = get_rdkit_mol(product_side)
    if reactant_mol is None or product_mol is None:
        return None
    if len(reactant_mol.GetAtoms()) > 150 or len(product_mol.GetAtoms()) > 150:
        return None
    reactants = reactant_side.split(".")
    products = product_side.split(".")
    reactant_carbon_components = sum(count_carbon_atoms(x) > 0 for x in reactants)
    product_carbon_components = sum(count_carbon_atoms(x) > 0 for x in products)
    if reactant_carbon_components > 3 or product_carbon_components > 3:
        return None
    if reactant_carbon_components == 0 or product_carbon_components == 0:
        return None
    return rxn


def cano_rxn(rxn: str, exchange_pos: bool = False, remain_isomer: bool = True):
    if not rxn:
        return None
    fields = rxn.split(">")
    reactants = [cano_smiles(x, remain_isomer) for x in fields[0].split(".")]
    products = [cano_smiles(x, remain_isomer) for x in fields[-1].split(".")]
    if any(x is None for x in reactants + products):
        return None
    reactants = sorted(reactants)
    products = sorted(products)
    if not products or not reactants:
        return None
    if exchange_pos:
        return f"{'.'.join(products)}>>{'.'.join(reactants)}"
    return f"{'.'.join(reactants)}>>{'.'.join(products)}"


def clean_reaction(raw: str):
    if raw.count(">>") != 1:
        return None, "MALFORMED_REACTION"
    try:
        reduced = remove_redundent_from_rxn(raw)
    except Exception as exc:
        return None, f"REMOVE_REDUNDANT_EXCEPTION:{type(exc).__name__}"
    if reduced is None:
        return None, "EMPTY_AFTER_REDUNDANT_REMOVAL"
    filtered = filter_unwanted_rxn(reduced)
    if filtered is None:
        return None, "REJECTED_BY_ORIGINAL_SIZE_OR_CARBON_COMPONENT_GATE"
    neutral = neutralize_rxn(filtered)
    canonical = cano_rxn(neutral)
    if canonical is None:
        return None, "CANONICALIZATION_FAILED"
    return canonical, "PASS"


def read_source_rows(archive: Path):
    with tarfile.open(archive, "r:gz") as bundle:
        members = {member.name: member for member in bundle.getmembers()}
        if SOURCE_MEMBER not in members:
            raise RuntimeError(f"missing required member: {SOURCE_MEMBER}")
        handle = bundle.extractfile(members[SOURCE_MEMBER])
        if handle is None:
            raise RuntimeError("could not read provenance member")
        raw = handle.read()
    text = raw.decode("utf-8")
    rows = list(csv.DictReader(text.splitlines(), delimiter="\t"))
    return rows, sha256_bytes(raw)


def write_tsv(path: Path, rows: list[dict], columns: list[str]):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=False)
    rows, member_sha = read_source_rows(args.freeze)
    if len(rows) != 298 or len({x["case_id"] for x in rows}) != 298:
        raise RuntimeError("expected exactly 298 unique cases")

    audit_rows = []
    model_rows = []
    hold_rows = []
    for row in rows:
        raw = row["canonical_directional"]
        cleaned, reason = clean_reaction(raw)
        status = "HOLD" if cleaned is None else ("UNCHANGED" if cleaned == raw else "CHANGED")
        out = {
            "case_id": row["case_id"],
            "global_reaction_id": row["global_reaction_id"],
            "parent_smiles": row["parent_smiles"],
            "source_canonical_directional": raw,
            "source_reaction_sha256": sha256_text(raw),
            "model_cano_rxn_smiles": cleaned or "",
            "model_reaction_sha256": sha256_text(cleaned) if cleaned else "",
            "cleaning_status": status,
            "cleaning_reason": reason,
            "gold_accessions": row["gold_accessions"],
            "source_databases": row["source_databases"],
            "source_record_ids": row["source_record_ids"],
        }
        audit_rows.append(out)
        (hold_rows if cleaned is None else model_rows).append(out)

    columns = list(audit_rows[0])
    write_tsv(args.output_dir / "POLLUTANT298_REACTION_CLEANING_AUDIT.tsv", audit_rows, columns)
    write_tsv(args.output_dir / "POLLUTANT291_MODEL_REACTIONS.tsv", model_rows, columns)
    write_tsv(args.output_dir / "POLLUTANT7_REACTION_CLEANING_HOLD.tsv", hold_rows, columns)

    by_model_reaction = defaultdict(list)
    for row in model_rows:
        by_model_reaction[row["model_reaction_sha256"]].append(row)
    collision_rows = []
    collision_group_count = 0
    for model_sha, grouped_rows in sorted(by_model_reaction.items()):
        if len(grouped_rows) < 2:
            continue
        collision_group_count += 1
        case_ids = "|".join(sorted(row["case_id"] for row in grouped_rows))
        global_ids = "|".join(sorted(row["global_reaction_id"] for row in grouped_rows))
        for row in sorted(grouped_rows, key=lambda item: item["case_id"]):
            collision_rows.append(
                {
                    "model_reaction_sha256": model_sha,
                    "model_cano_rxn_smiles": row["model_cano_rxn_smiles"],
                    "group_size": len(grouped_rows),
                    "all_case_ids": case_ids,
                    "all_global_reaction_ids": global_ids,
                    "case_id": row["case_id"],
                    "global_reaction_id": row["global_reaction_id"],
                    "source_databases": row["source_databases"],
                }
            )
    collision_columns = [
        "model_reaction_sha256",
        "model_cano_rxn_smiles",
        "group_size",
        "all_case_ids",
        "all_global_reaction_ids",
        "case_id",
        "global_reaction_id",
        "source_databases",
    ]
    write_tsv(
        args.output_dir / "POLLUTANT291_COLLAPSED_MODEL_REACTION_GROUPS.tsv",
        collision_rows,
        collision_columns,
    )

    counts = Counter(x["cleaning_status"] for x in audit_rows)
    summary = {
        "status": "PASS_POLLUTANT298_TRAINING_COMPATIBLE_REACTION_CLEANING",
        "source_archive": str(args.freeze.resolve()),
        "source_archive_bytes": args.freeze.stat().st_size,
        "source_archive_sha256": file_sha256(args.freeze),
        "source_member": SOURCE_MEMBER,
        "source_member_sha256": member_sha,
        "official_cleaning_source": str(
            Path(__file__).resolve().parents[2] / "scripts" / "rhea_data_cleaning.py"
        ),
        "official_cleaning_source_sha256": file_sha256(
            Path(__file__).resolve().parents[2] / "scripts" / "rhea_data_cleaning.py"
        ),
        "rdkit_version": rdBase.rdkitVersion,
        "cases": len(audit_rows),
        "status_counts": dict(sorted(counts.items())),
        "model_ready_cases": len(model_rows),
        "hold_cases": len(hold_rows),
        "unique_source_reactions": len({x["source_reaction_sha256"] for x in audit_rows}),
        "unique_model_reactions": len({x["model_reaction_sha256"] for x in model_rows}),
        "collapsed_model_reaction_groups": collision_group_count,
        "cases_in_collapsed_groups": len(collision_rows),
    }
    (args.output_dir / "CLEANING_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )

    manifest_rows = []
    for path in sorted(args.output_dir.iterdir()):
        if path.name == "MANIFEST.tsv" or not path.is_file():
            continue
        manifest_rows.append(
            {"relative_path": path.name, "bytes": path.stat().st_size, "sha256": file_sha256(path)}
        )
    write_tsv(args.output_dir / "MANIFEST.tsv", manifest_rows, ["relative_path", "bytes", "sha256"])
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
