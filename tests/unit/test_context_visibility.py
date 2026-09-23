import importlib.util
import json
from pathlib import Path

from semidebug.agent.orchestrator import provider_history
from semidebug.benchmark.loader import load_case
from semidebug.context.selector import evidence_from, select_context
from semidebug.models import PatchAttempt, ValidationBundle, ValidationResult

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "build_v2_dataset", ROOT / "evaluator/build_v2_dataset.py"
)
dataset_builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dataset_builder)


def test_v2_cases_keep_regression_source_out_of_prompt(tmp_path):
    output = tmp_path / "benchmark_v2"
    assert dataset_builder.build(ROOT / "benchmark", output) == 30
    for manifest in sorted(output.glob("*/case_*/case.json")):
        root = manifest.parent
        case = load_case(root)
        assert set(case.target.sources).isdisjoint(
            source for test in case.regression for source in test.sources
        )
        assert all(test.top != case.target.top for test in case.regression)
        assert "REGRESSION" not in (root / case.target.sources[0]).read_text()
        hidden = root / case.regression[0].sources[0]
        hidden.write_text(hidden.read_text() + "\n// HIDDEN_SENTINEL\n")
        serialized = json.dumps(select_context(root, case, []))
        assert "HIDDEN_SENTINEL" not in serialized
        assert case.regression[0].sources[0] not in serialized


def test_regression_feedback_never_serializes_private_details():
    bundle = ValidationBundle(
        results={
            "regression_17.simulation": ValidationResult(
                tool="vvp",
                command=["vvp", "tb/hidden_secret.v"],
                exit_code=1,
                status="fail",
                stderr="HIDDEN_EXPECTED=42",
            )
        }
    )
    attempt = PatchAttempt(iteration=1, regression=bundle)
    context = {
        "evidence": [
            e.model_dump() for e in evidence_from(bundle, "regression-1", evaluator_only=True)
        ],
        "previous_attempts": provider_history([attempt]),
    }
    serialized = json.dumps(context)
    assert "HIDDEN_EXPECTED" not in serialized
    assert "tb/hidden_secret.v" not in serialized
    assert "regression_17" not in serialized
    assert "fail" in serialized
