import json
from pathlib import Path

import pytest

from semidebug.benchmark.loader import load_case
from semidebug.tools.validation import regress, validate
from semidebug.tools.workspace import copy_project, hashes

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.integration


@pytest.mark.parametrize("design", ["counter", "fifo", "arbiter", "controller", "alu", "pulse"])
def test_gold(design, tmp_path):
    source = ROOT / "evaluator/gold" / design
    case = load_case(source)
    root = tmp_path / "project"
    copy_project(source, root, case.mutable + case.immutable + ["case.json"])
    assert validate(root, case).passed
    assert regress(root, case).passed


@pytest.mark.parametrize(
    "entry", json.loads((ROOT / "benchmark/manifest.json").read_text()), ids=lambda e: e["id"]
)
def test_mutation_reproduced(entry, tmp_path):
    source = ROOT / "benchmark" / entry["path"]
    case = load_case(source)
    root = tmp_path / "project"
    copy_project(source, root, case.mutable + case.immutable + ["case.json"])
    before = hashes(root, case.immutable)
    bundle = validate(root, case)
    assert not bundle.passed
    assert not bundle.infrastructure_error
    assert hashes(root, case.immutable) == before
