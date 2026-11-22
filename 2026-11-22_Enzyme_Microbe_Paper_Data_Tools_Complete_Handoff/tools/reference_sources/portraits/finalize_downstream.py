#!/usr/bin/env python3
import argparse
import csv
import gzip
import json
import math
import os
import pickle
from pathlib import Path


KERAS_TRAITS = (
    "anoxygenic_photoautotrophy_Fe_oxidizing",
    "anoxygenic_photoautotrophy_S_oxidizing",
    "dark_sulfite_oxidation", "dark_sulfur_oxidation",
    "dark_thiosulfate_oxidation", "intracellular_parasites",
    "oil_bioremediation", "predatory_or_exoparasitic",
)


def read_table(path):
    with gzip.open(path, "rt", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    if len(rows) != 2 or not rows[0] or len(rows[0]) != len(rows[1]):
        raise RuntimeError("invalid one-sample table: %s" % path)
    return rows


def normalize_file(path, accession):
    rows = read_table(path)
    allowed = {accession, accession.rsplit(".", 1)[0], accession + "_genomic"}
    if rows[1][0] not in allowed:
        raise RuntimeError("unexpected sample ID in %s" % path)
    values = rows[1][1:]
    rows[1][0] = accession
    temporary = Path(str(path) + ".tmp")
    with gzip.open(temporary, "wt", newline="") as handle:
        csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)
    os.replace(temporary, path)
    if read_table(path)[1][1:] != values:
        raise RuntimeError("normalization changed values in %s" % path)


def canonicalize(directory, genome, accession):
    for path in sorted(directory.glob("*.tsv.gz")):
        normalize_file(path, accession)
        if not path.name.startswith(genome + "."):
            destination = directory / (genome + "." + path.name)
            if destination.exists():
                raise RuntimeError("canonical name collision: %s" % destination)
            path.rename(destination)


def recover_keras(ko_path, micro_dir, genome, model_root):
    import numpy as np
    import pandas as pd
    from keras.models import load_model

    training_columns = list(pd.read_csv(
        model_root / "matrix" / "genome_ko_all.csv", nrows=0).columns)
    training_columns = [name for name in training_columns if name not in ("Genome", "Species")]
    values = pd.read_csv(ko_path, sep="\t", index_col=0, compression="infer")
    values.columns = values.columns.str.replace(r"^ko:", "", regex=True)
    values = values.reindex(columns=training_columns, fill_value=0)
    probability_path = micro_dir / (genome + ".MICROPHERRET.prob.tsv.gz")
    binary_path = micro_dir / (genome + ".MICROPHERRET.binary.tsv.gz")
    merged = pd.read_csv(probability_path, sep="\t", index_col=0, compression="gzip")
    if list(values.index) != list(merged.index) or len(values.index) != 1:
        raise RuntimeError("KO/MICROPHERRET sample mismatch")
    if len(merged.columns) not in (66, 74):
        raise RuntimeError("unexpected native MICROPHERRET trait count")
    keras_columns = {trait + "_prob" for trait in KERAS_TRAITS}
    if len(merged.columns) == 74 and not keras_columns.issubset(set(merged.columns)):
        raise RuntimeError("74-trait table lacks the accepted Keras trait set")
    recovered = []
    for trait in KERAS_TRAITS:
        column = trait + "_prob"
        if column in merged.columns:
            continue
        model_path = model_root / "saved_models" / (trait + ".mdl_wts.hdf5")
        scaler_path = model_root / "saved_models" / ("scaler_" + trait + ".sav")
        if not model_path.is_file() or not scaler_path.is_file():
            raise RuntimeError("missing approved model/scaler for %s" % trait)
        model = load_model(model_path, compile=False)
        with open(scaler_path, "rb") as handle:
            scaler = pickle.load(handle)
        probability = model.predict(scaler.transform(values), verbose=0).reshape(-1)
        if len(probability) != 1 or not np.isfinite(probability).all():
            raise RuntimeError("invalid prediction for %s" % trait)
        merged[column] = probability
        one = pd.DataFrame(probability, index=values.index, columns=[column])
        one.to_csv(micro_dir / (genome + "." + trait + ".tsv.gz"),
                   sep="\t", compression="gzip")
        recovered.append(trait)
    if (len(merged.columns) != 74 or not keras_columns.issubset(set(merged.columns)) or
            set(recovered) not in (set(), set(KERAS_TRAITS))):
        raise RuntimeError("MICROPHERRET compatibility closure failed")
    merged.to_csv(probability_path, sep="\t", compression="gzip")
    binary = (merged > 0.5).astype(int)
    binary.columns = [name.removesuffix("_prob") for name in binary.columns]
    binary.to_csv(binary_path, sep="\t", compression="gzip")
    return recovered


def numeric_gate(path, accession, traits, binary=False):
    rows = read_table(path)
    if rows[1][0] != accession or len(rows[0]) != traits + 1:
        return False
    try:
        values = [float(value) for value in rows[1][1:]]
    except ValueError:
        return False
    if not all(math.isfinite(value) for value in values):
        return False
    return all(value in (0, 1) for value in values) if binary else all(0 <= value <= 1 for value in values)


def micro_pair_gate(probability_path, binary_path, accession):
    probability = read_table(probability_path)
    binary = read_table(binary_path)
    if probability[1][0] != accession or binary[1][0] != accession:
        return False
    if [name.removesuffix("_prob") for name in probability[0][1:]] != binary[0][1:]:
        return False
    try:
        probabilities = [float(value) for value in probability[1][1:]]
        binaries = [int(value) for value in binary[1][1:]]
    except ValueError:
        return False
    return binaries == [int(value > 0.5) for value in probabilities]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--accession", required=True)
    parser.add_argument("--model-root", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    root = Path(args.root)
    accession = args.accession
    genome = accession + "_genomic"
    for name in ("e2m", "micropherret", "bacdive_ai", "traitar"):
        directory = root / name
        if not directory.is_dir():
            raise RuntimeError("missing stage directory: %s" % directory)
        canonicalize(directory, genome, accession)
    recovered = recover_keras(
        root / "e2m" / (genome + ".emapper.KEGG_ko.tsv.gz"),
        root / "micropherret", genome, Path(args.model_root))
    gates = {
        "micro_prob_74": numeric_gate(root / "micropherret" / (genome + ".MICROPHERRET.prob.tsv.gz"), accession, 74),
        "micro_binary_74": numeric_gate(root / "micropherret" / (genome + ".MICROPHERRET.binary.tsv.gz"), accession, 74, True),
        "micro_pair_columns_and_threshold": micro_pair_gate(
            root / "micropherret" / (genome + ".MICROPHERRET.prob.tsv.gz"),
            root / "micropherret" / (genome + ".MICROPHERRET.binary.tsv.gz"), accession),
        "bac_prob_8": numeric_gate(root / "bacdive_ai" / (genome + ".BacDiveAI.prob.tsv.gz"), accession, 8),
        "bac_binary_8": numeric_gate(root / "bacdive_ai" / (genome + ".BacDiveAI.binary.tsv.gz"), accession, 8, True),
        "traitar_prob_67": numeric_gate(root / "traitar" / (genome + ".Traitar.prob.tsv.gz"), accession, 67),
        "traitar_binary_67": numeric_gate(root / "traitar" / (genome + ".Traitar.binary.tsv.gz"), accession, 67, True),
    }
    report = {"accession": accession, "recovered_keras_traits": recovered,
              "gates": gates, "all_pass": all(gates.values())}
    Path(args.report).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    raise SystemExit(0 if report["all_pass"] else 1)


if __name__ == "__main__":
    main()
