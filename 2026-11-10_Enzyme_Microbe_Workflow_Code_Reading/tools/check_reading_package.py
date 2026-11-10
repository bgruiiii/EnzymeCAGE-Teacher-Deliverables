"""Check reading-package integrity with the standard library; no business imports."""
import argparse
import ast
import csv
import hashlib
import io
import json
import re
from pathlib import Path, PurePosixPath


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def validate(root):
    root = Path(root).resolve()
    paths = list(root.rglob("*"))
    assert not any(p.is_symlink() for p in paths), "Symlinks are not reading-package members"
    files = {str(p.relative_to(root)): p.read_bytes() for p in paths if p.is_file()}
    suffixes = {".py", ".sh", ".md", ".tsv", ".json", ".yaml", ".txt"}
    assert all(Path(n).suffix in suffixes or Path(n).name in {"LICENSE", ".gitignore", "SHA256SUMS"} for n in files)
    assert not any(set(PurePosixPath(n).parts) & {".git", "__pycache__", ".venv"} for n in files)
    assert all(len(raw) < 10 * 1024 * 1024 for raw in files.values())
    assert sum(map(len, files.values())) < 50 * 1024 * 1024
    expected = {}
    for line in files["SHA256SUMS"].decode().splitlines():
        digest, name = line.split("  ", 1)
        p = PurePosixPath(name)
        assert not p.is_absolute() and ".." not in p.parts and "\\" not in name
        assert re.fullmatch(r"[0-9a-f]{64}", digest) and name not in expected
        expected[name] = digest
    assert set(expected) == set(files) - {"SHA256SUMS"}, "Missing or unexpected package member"
    assert all(sha(files[name]) == digest for name, digest in expected.items()), "Checksum mismatch"
    sources = list(csv.DictReader(io.StringIO(files["provenance/SOURCE_MANIFEST.tsv"].decode()), delimiter="\t"))
    assert len(sources) == len({r["file"] for r in sources})
    for row in sources:
        raw = files[row["file"]]
        assert sha(raw) == row["published_sha256"]
        if row["transformation"] == "NONE_BYTE_IDENTICAL":
            assert row["published_sha256"] == row["original_sha256"]
        else:
            assert row["file"] == "schemas/pathway_input_reaction_gold.schema.tsv"
            assert row["transformation"].startswith("SCHEMA_COMMENTS_ONLY_NORMALIZED")
        assert len(raw) == int(row["bytes"])
    checkpoints = list(csv.DictReader(io.StringIO(files["assets/CHECKPOINTS_25.tsv"].decode()), delimiter="\t"))
    assert len(checkpoints) == 25
    assert len({(r["arm"], r["seed"]) for r in checkpoints}) == 25
    assert len({r["arm"] for r in checkpoints}) == 5
    assert all({r["seed"] for r in checkpoints if r["arm"] == arm} == {"40", "41", "42", "43", "44"}
               for arm in {r["arm"] for r in checkpoints})
    index = list(csv.DictReader(io.StringIO(files["provenance/CODE_INDEX.tsv"].decode()), delimiter="\t"))
    for row in index:
        assert row["file"] in files and sha(files[row["file"]]) == row["sha256"]
    python_count = json_count = link_count = 0
    for name, raw in files.items():
        text = raw.decode("utf-8-sig")
        if name.endswith(".py"):
            ast.parse(text, filename=name)
            python_count += 1
        if name.endswith(".json"):
            json.loads(text)
            json_count += 1
        if name.endswith(".md") and not name.startswith("code/"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                path = (root / name).parent / target.split("#", 1)[0]
                assert path.resolve().is_relative_to(root), "Link escapes package"
                assert path.is_file(), f"Missing documentation link: {name}: {target}"
                link_count += 1
        assert not re.search(r"BIOPATH150_\d{3}(?:__S\d+)?", text), "Real evaluation case literal"
        assert not re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", text)
        assert not re.search(r"\b(?:sk-(?:proj-)?|oc_sk_)[A-Za-z0-9_-]{24,}", text)
        assert not re.search(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{25,}", text)
    for name in ("examples/given_path.synthetic.json", "examples/host_trait.synthetic.json"):
        assert "SYNTHETIC" in json.loads(files[name])["example_kind"]
    assert "SYNTHETIC" in files["examples/rankings.synthetic.tsv"].decode()
    return {"status": "PASS_STATIC_READING_PACKAGE_ONLY", "files": len(files),
            "source_schema_rows": len(sources), "python_ast": python_count,
            "json": json_count, "documentation_links": link_count, "checkpoint_identities": len(checkpoints),
            "business_code_imports": 0, "network_gpu_api_calls": 0,
            "limitations": "Not a deployment, biological correctness, absolute secret absence, or license clearance test."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(validate(args.root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
