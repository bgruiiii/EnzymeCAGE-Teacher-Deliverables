"""03E release common (derived from accepted 03D-R1-PATCH common_03a).

Same names/API so the reviewed chain modules (rules_03a / registry_03d /
proofs_03a_r1) run byte-identically. The only change: every path is resolved
under an explicit run root. RUN_ROOT defaults to <bundle>/data (source-bytes
mirror, original bytes/SHAs preserved) and can be overridden with the
LIKERT_V05_RUN_ROOT environment variable — nothing assumes /home/a/EnzymeCAGE.
Deploy paths never impersonate scientific identity: identity() keeps the same
path_rel_R strings as the reviewed sources because data/ mirrors those subtrees.
"""
import csv, hashlib, io, json, os, sys
from pathlib import Path
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent          # bundle/runtime/v05_release
BUNDLE = HERE.parent.parent                      # bundle root
RUN_ROOT = Path(os.environ.get("LIKERT_V05_RUN_ROOT", str(BUNDLE / "data")))
R = RUN_ROOT  # reviewed chain modules import this name; resolves to the bundle data mirror
OUT = Path(os.environ.get("LIKERT_V05_RELEASE_DIR", str(BUNDLE / "release")))  # release tree (== PATCH OUT file names)
W = RUN_ROOT / "LIKERT_V05_RELEASE_20261108"
B = W / "S1_BIO_REVIEW"
S0 = W / "S0_INTEGRATION"
PATCH = W / "S0_INTEGRATION_R2_PATCH"
F2 = HERE.parent / "f2"                          # derived f2r12 code (same APIs)
PIPELINE = HERE.parent / "pipeline"
SCHEMA_PATH = OUT / "schema/RATING_OUTPUT_SCHEMA_RELEASE.json"
VERSION = "LIKERT_V05_20261110_R1"
RELEASE_STATUS_FILE = OUT / "FREEZE_RECORD.json"
DIMS = ["D1", "D2", "D3a", "D3b", "D4", "D5", "D6"]
BRANCH_MAP = OUT / "mapping/BRANCH_PATH_MAPPING_03E.tsv"
csv.field_size_limit(1 << 27)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def jsha(obj):
    return sha(canonical(obj).encode())


def load(p):
    return json.loads(Path(p).read_text())


def put(rel, text):
    p = OUT / rel
    assert p.resolve().is_relative_to(OUT.resolve())
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text if isinstance(text, bytes) else text.encode())


def js(rel, obj):
    put(rel, json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def rows(p):
    with Path(p).open(newline="") as f:
        rr = list(csv.reader(f, delimiter="\t", strict=True))
    assert rr and all(len(x) == len(rr[0]) for x in rr[1:])
    return [dict(zip(rr[0], x)) for x in rr[1:]]


def tsv(rel, rr):
    s = io.StringIO(newline="")
    wtr = csv.DictWriter(s, list(rr[0]), delimiter="\t", lineterminator="\n")
    wtr.writeheader()
    wtr.writerows(rr)
    put(rel, s.getvalue())


def identity(p):
    p = Path(p)
    return {"path_rel_R": str(p.relative_to(RUN_ROOT)), "sha256": sha(p.read_bytes()),
            "bytes": p.stat().st_size}
