"""bundle path resolver for the reviewed pipeline chain (derived; explicit run root)."""
import os
from pathlib import Path
PIPELINE = Path(__file__).resolve().parent
BUNDLE = PIPELINE.parent.parent
RUN_ROOT = str(Path(os.environ.get("LIKERT_V05_RUN_ROOT", str(BUNDLE / "data"))))
F2 = str(PIPELINE.parent / "f2")
