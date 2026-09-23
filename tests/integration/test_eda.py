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


FINAL_CASES = sorted((ROOT / "benchmark_v2/public").glob("case_*/case.json")) + sorted(
    (ROOT / "benchmark_v2/hidden").glob("case_*/case.json")
)


@pytest.mark.parametrize("manifest", FINAL_CASES, ids=lambda path: path.parent.name)
def test_mutation_reproduced(manifest, tmp_path):
    source = manifest.parent
    case = load_case(source)
    root = tmp_path / "project"
    copy_project(source, root, case.mutable + case.immutable + ["case.json"])
    before = hashes(root, case.immutable)
    bundle = validate(root, case)
    assert not bundle.passed
    assert not bundle.infrastructure_error
    assert hashes(root, case.immutable) == before
