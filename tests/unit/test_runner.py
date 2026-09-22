import json

from semidebug.benchmark.runner import run_benchmark
from semidebug.config import Settings
from semidebug.models import RunState


def test_benchmark_exports(tmp_path, monkeypatch):
    root = tmp_path / "cases"
    (root / "one").mkdir(parents=True)
    (root / "one/case.json").write_text("{}")
    result = RunState(
        run_id="r",
        case_id="c",
        category="syntax",
        provider="scripted-test-double",
        model="test",
        max_iterations=3,
        project_root="c",
        mutable_files=[],
        immutable_files=[],
        final_status="MAX_RETRY",
    )
    monkeypatch.setattr("semidebug.benchmark.runner.repair", lambda *args: result)
    output = tmp_path / "output"
    summary = run_benchmark(root, object(), output, Settings())
    assert summary["total"] == 1 and summary["fixed"] == 0
    assert json.loads((output / "results.json").read_text())[0]["final_status"] == "MAX_RETRY"
    assert "compile_pass" in (output / "results.csv").read_text()
