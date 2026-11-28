"""Read-only, standard-library verification of this portable evidence package."""

from collections import defaultdict
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]


def read_json(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def read_table(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(value, label):
    if not value:
        raise ValueError(label)


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-12, abs_tol=1e-15)


def main():
    expected = {}
    for line in (ROOT / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        path = (ROOT / name).resolve()
        require(path.is_relative_to(ROOT) and name not in expected, "manifest path/duplicate")
        require(sha(path) == digest, "checksum: " + name)
        expected[name] = digest
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p.name != "SHA256SUMS"}
    require(set(expected) == actual, "manifest coverage")
    sources = read_table("provenance/SOURCE_FILES.tsv")
    copies = 0
    for row in sources:
        if row["package_path"]:
            path = ROOT / row["package_path"]
            require(sha(path) == row["sha256"] and path.stat().st_size == int(row["bytes"]), "copied source identity")
            copies += 1

    pools = read_table("F02B_POOL_DISTRIBUTION/POOL_SIZE_PER_STEP_382.tsv")
    require(len(pools) == len({r["step_id"] for r in pools}) == 382, "unique step count")
    by_step = {r["step_id"]: r for r in pools}
    cross = read_table("F02A_RANDOM_BASELINE/CROSS_ARM_POOL_CONSISTENCY_382.tsv")
    require(len(cross) == 382 and {r["step_id"] for r in cross} == set(by_step), "cross-arm step identities")
    for row in cross:
        pool = by_step[row["step_id"]]
        require(row["n_arms"] == "6" and row["distinct_N"] == row["distinct_G"] == "1", "six shared arms")
        require(row["N"] == pool["N_step_candidate_associations"] == row["r4_n_retained"], "N match")
        require(row["G"] == pool["G_step_Gold_associations"] == row["r4_n_gold_retained"], "G match")

    distributions = read_table("F02B_POOL_DISTRIBUTION/POOL_SIZE_DISTRIBUTION_BY_VIEW.tsv")
    bins = read_table("F02B_POOL_DISTRIBUTION/POOL_SIZE_BINS_BY_VIEW.tsv")
    frozen = read_json("F02A_RANDOM_BASELINE/FROZEN_VIEWS.json")["views"]
    summary = read_table("F02A_RANDOM_BASELINE/RANDOM_BASELINE_BY_VIEW.tsv")
    probabilities = {}
    for step, pool in by_step.items():
        n, g = int(pool["N_step_candidate_associations"]), int(pool["G_step_Gold_associations"])
        require(0 <= g <= n and n > 0, "valid N/G")
        p = {}
        for k in (1, 10):
            miss = Fraction(1)
            for i in range(min(k, n)):
                miss *= Fraction(max(n - g - i, 0), n - i)
            p[k] = 1 - miss
        probabilities[step] = p
    detail = read_table("F02A_RANDOM_BASELINE/RANDOM_BASELINE_PER_STEP_382.tsv")
    require(len(detail) == 382 and {r["step_id"] for r in detail} == set(by_step), "probability step identities")
    for row in detail:
        step = row["step_id"]
        pool = by_step[step]
        require(row["N"] == pool["N_step_candidate_associations"] and row["G"] == pool["G_step_Gold_associations"], "per-step N/G")
        for k in (1, 10):
            require(int(row[f"k{k}_eff"]) == min(k, int(row["N"])), "effective k")
            require(Fraction(int(row[f"rand_hit{k}_num"]), int(row[f"rand_hit{k}_den"])) == probabilities[step][k], "per-step exact probability")
            require(close(row[f"rand_hit{k}_prop"], probabilities[step][k]), "per-step probability value")
        for view in frozen:
            require(row["in_" + view.lower()] == pool["in_" + view.lower()], "per-step view flags")
    for row in summary:
        view = row["view_id"]
        members = [p for p in pools if p["in_" + view.lower()] == "True"]
        require(len(members) == int(row["n_steps"]), "view step count")
        require(len({p["case_id"] for p in members}) == int(row["n_paths"]), "view path count")
        require({p["step_id"] for p in members} == set(frozen[view]["step_ids"]), "frozen view membership")
        for k in (1, 10):
            value = sum((probabilities[p["step_id"]][k] for p in members), Fraction()) / len(members)
            require(value == Fraction(row[f"rand_hit{k}_exact_frac"]), "exact random expectation")
            require(close(value, row[f"rand_hit{k}_macro_prop"]), "random proportion")
            require(close(float(value) * 100, row[f"rand_hit{k}_macro_pct"]), "random percentage")
        for dist in (d for d in distributions if d["view_id"] == view):
            values = [int(p[dist["measure"]]) for p in members]
            quantiles = statistics.quantiles(values, n=100, method="inclusive")
            for key, value in {
                "count": len(values), "min": min(values), "max": max(values), "sum": sum(values),
                "mean": statistics.mean(values), "median": statistics.median(values),
                "population_sd": statistics.pstdev(values), "q05": quantiles[4], "q25": quantiles[24],
                "q75": quantiles[74], "q95": quantiles[94],
            }.items():
                require(close(dist[key], value), "distribution: " + key)
            if dist["steps_N_le10"]:
                small = sum(v <= 10 for v in values)
                require(int(dist["steps_N_le10"]) == small and close(dist["share_N_le10"], small / len(values)), "small pools")
        view_bins = [b for b in bins if b["view_id"] == view]
        require(len(view_bins) == 5, "five pool bins")
        for bucket in view_bins:
            lower, upper = int(bucket["lower"]), int(bucket["upper"]) if bucket["upper"] else math.inf
            count = sum(lower <= int(p["N_step_candidate_associations"]) <= upper for p in members)
            require(int(bucket["n_steps"]) == count and close(bucket["ratio_of_steps"], count / len(members)), "pool bin count")

    coverage = {r["item_id"]: int(r["value"]) for r in read_table("E03_SOURCE_COVERAGE/COVERAGE_AND_MISSINGNESS_EXPLANATION.tsv")}
    wanted = [7468, 7430, 7, 30, 1, 5579, 31, 38, 5607, 5601, 22]
    require([coverage[f"E03-{i:02d}"] for i in range(1, 12)] == wanted, "source counts")
    require(7430 + 7 + 30 + 1 == 7468 and 5601 - 22 == 5579, "source layers")

    positions = read_json("E06_REAL_TOOL_CASE/COMPLETE167_POSITIONS.json")
    require(len(positions) == 167, "167 positions")
    missing = [r for r in positions if r["score"] is None]
    require({r["uid"] for r in missing} == {"A5YV19", "P19733", "Q84AQ1", "Q84AQ3"} and len(missing) == 4, "four explicit gaps")
    require(all(r["rank"] is r["ensemble_ci"] is r["per_seed_probability"] is None and r["status"] == "TYPED_UNSCORED" for r in missing), "nulls kept")
    groups = defaultdict(list)
    for row in positions:
        groups[row["step_id"]].append(row)
    require({k: len(v) for k, v in groups.items()} == {"RT-755cab4942170d85": 91, "RT-bb8e451c4bff6bb6": 76}, "two step pools")
    for step, group in groups.items():
        require([r["candidate_position"] for r in group] == list(range(len(group))), "position order")
        scored = sorted((r for r in group if r["score"] is not None), key=lambda r: (-r["score"], r["uid"]))
        raw = read_json("E06_REAL_TOOL_CASE/RAW/" + step + "_RAW.json")
        require(len(raw["outcome"]["all_scored"]) == len(scored), "raw scored count")
        for rank, (row, original) in enumerate(zip(scored, raw["outcome"]["all_scored"]), 1):
            require(row["rank"] == rank and row["uid"] == original["uid"] and row["score"] == original["score"], "raw rank/score")
            values = list(row["per_seed_probability"].values())
            require(len(values) == 5 and close(statistics.mean(values), row["score"]), "five-seed mean")
            quantiles = statistics.quantiles(values, n=1000, method="inclusive")
            require(close(quantiles[24], row["ensemble_ci"][0]) and close(quantiles[974], row["ensemble_ci"][1]), "seed quantile interval")
    top = read_table("E06_REAL_TOOL_CASE/TOP10.tsv")
    require(len(top) == 20, "20 top positions")
    lookup = {(r["step_id"], r["rank"]): r for r in positions if r["score"] is not None}
    require(len({(r["step_id"], int(r["rank"])) for r in top}) == 20, "unique Top10")
    for row in top:
        original = lookup[row["step_id"], int(row["rank"])]
        require(1 <= int(row["rank"]) <= 10 and row["uid"] == original["uid"] and close(row["score"], original["score"]), "Top10 projection")
    receipt = read_json("E06_REAL_TOOL_CASE/PROCESS_RECEIPT.json")
    journal = read_json("E06_REAL_TOOL_CASE/FORWARD_JOURNAL.json")
    require(receipt["worker_exit_code"] == 0 and journal["wrapper_calls_completed"] == 2 and journal["model_evaluate_calls_completed"] == 10, "completed real run receipts")

    approval = read_json("R02_OLD_V05_FREEZE/RELEASE_APPROVAL.json")
    release = ROOT / "R02_OLD_V05_FREEZE"
    require(approval["scope"] == "OLD_SPECIFIED_ROUTE_ONLY", "old scope only")
    require(sha(release / approval["manifest_path"]) == approval["manifest_sha"], "approval manifest binding")
    require(sha(release / "rubric/SCORE_RULES_RELEASE.json") == approval["release_subject"]["rules_json_sha256_final"], "approval rule binding")
    statuses = {r["item_id"]: r["status"] for r in read_table("DELIVERY_STATUS.tsv")}
    require(statuses["F02e"] == "DEFERRED_TO_SISTER_BY_USER", "no fake figure confirmation")
    require(statuses["L03"] == "NOT_PROVIDED_NO_HUMAN_VALIDATION_CLAIM", "no fake human scores")
    links = 0
    for path in ROOT.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            destination = (path.parent / unquote(target.split("#", 1)[0])).resolve()
            require(destination.is_relative_to(ROOT) and destination.exists(), "local link: " + target)
            links += 1
    print(json.dumps({
        "pass": True, "manifest_entries": len(expected), "source_copies": copies,
        "random_step_probabilities": 764, "frozen_views": 4, "source_layers_checked": True,
        "case_positions": 167, "case_scored": 163, "case_unscored": 4,
        "release_binding_verified": True, "relative_links_checked": links,
        "figure_confirmation": "DEFERRED_NOT_CONFIRMED", "human_validation": "NOT_CLAIMED",
        "model_or_network_calls": 0,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
