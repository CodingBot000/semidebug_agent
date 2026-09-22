import json

import pytest

from semidebug.agent.orchestrator import repair
from semidebug.config import Settings
from semidebug.llm.fake import ScriptedProvider
from semidebug.tools.workspace import hashes

pytestmark = pytest.mark.e2e


def test_first_shot(fifo, tmp_path, make_responses):
    p = ScriptedProvider(make_responses(fifo))
    result = repair(fifo, p, tmp_path)
    assert result.final_status == "FIXED"
    assert result.integrity_pass and result.regression_pass
    assert result.llm_calls == 2
    saved = json.loads((tmp_path / result.run_id / "result.json").read_text())
    assert saved["success"] is True
    events = [
        json.loads(line)["event_type"]
        for line in (tmp_path / result.run_id / "events.jsonl").read_text().splitlines()
    ]
    assert "VALIDATE_REGRESSION" in events and "SUCCESS" in events
    assert all("evaluator" not in json.dumps(r) for r in p.requests)


def test_retry(counter, tmp_path, make_responses):
    source = (counter / "rtl/counter.v").read_text()
    wrong = make_responses(counter, source.replace("4'd8", "4'd7"))
    result = repair(counter, ScriptedProvider(wrong + make_responses(counter)), tmp_path)
    assert result.final_status == "FIXED" and result.iteration == 2
    assert not result.patch_attempts[0].validation.passed


def test_exhausted(counter, tmp_path, make_responses):
    source = (counter / "rtl/counter.v").read_text()
    responses = []
    for value in [7, 6, 5]:
        responses += make_responses(counter, source.replace("4'd8", f"4'd{value}"))
    result = repair(counter, ScriptedProvider(responses), tmp_path)
    assert result.final_status == "MAX_RETRY"
    assert result.integrity_pass and not result.success


def test_testbench_attack_then_recover(counter, tmp_path, make_responses):
    bad = make_responses(counter)
    bad[1]["unified_diff"] = bad[1]["unified_diff"].replace("rtl/counter.v", "tb/counter_tb.v")
    result = repair(counter, ScriptedProvider(bad + make_responses(counter)), tmp_path)
    assert result.success and result.iteration == 2
    assert result.patch_attempts[0].guard_error


def test_repeated_patch(counter, tmp_path, make_responses):
    original = (counter / "rtl/counter.v").read_text()
    wrong = make_responses(counter, original.replace("4'd8", "4'd7"))
    result = repair(counter, ScriptedProvider(wrong + wrong), tmp_path)
    assert result.final_status == "REPEATED_PATCH"


def test_provider_error(counter, tmp_path):
    result = repair(counter, ScriptedProvider([]), tmp_path)
    assert result.final_status == "LLM_ERROR" and result.integrity_pass


def test_integrity_tamper_is_invalid(counter, tmp_path, make_responses, monkeypatch):
    import semidebug.agent.orchestrator as module

    actual = module.validate

    def tamper(root, case):
        result = actual(root, case)
        (root / case.immutable[0]).write_text("// corrupted\n")
        return result

    monkeypatch.setattr(module, "validate", tamper)
    before = hashes(counter, ["tb/counter_tb.v"])
    result = repair(counter, ScriptedProvider(make_responses(counter)), tmp_path)
    assert result.final_status == "INTEGRITY_ERROR" and not result.success
    assert hashes(counter, ["tb/counter_tb.v"]) == before


def test_one_iteration_failure(counter, tmp_path, make_responses):
    original = (counter / "rtl/counter.v").read_text()
    wrong = make_responses(counter, original.replace("4'd8", "4'd7"))
    result = repair(counter, ScriptedProvider(wrong), tmp_path, Settings(max_iterations=1))
    assert result.final_status == "MAX_RETRY" and result.iteration == 1


def test_regression_failure_cannot_be_accepted(counter, tmp_path, make_responses, monkeypatch):
    import semidebug.agent.orchestrator as module
    from semidebug.models import ValidationBundle, ValidationResult

    # Inject an independent validator failure; neither benchmark source nor test expectations change.
    monkeypatch.setattr(
        module,
        "regress",
        lambda *args: ValidationBundle(
            results={
                "regression.simulation": ValidationResult(
                    tool="vvp",
                    command=["vvp", "fixture"],
                    exit_code=1,
                    status="fail",
                    stderr="independent regression failure",
                )
            }
        ),
    )
    result = repair(
        counter, ScriptedProvider(make_responses(counter)), tmp_path, Settings(max_iterations=1)
    )
    assert result.patch_attempts[0].validation.passed
    assert result.final_status == "MAX_RETRY" and not result.success and not result.regression_pass


def test_removed_original_records_integrity_error(counter, tmp_path, monkeypatch):
    import shutil

    import semidebug.agent.orchestrator as module

    root = tmp_path / "project"
    shutil.copytree(counter, root)

    class UnavailableProvider(ScriptedProvider):
        def generate_structured(self, request, schema):
            from semidebug.llm.base import ProviderError

            (root / "tb/counter_tb.v").unlink()
            raise ProviderError("Fixture provider failed")

    result = module.repair(root, UnavailableProvider([]), tmp_path / "runs")
    assert result.final_status == "INTEGRITY_ERROR" and not result.success
    assert (tmp_path / "runs" / result.run_id / "result.json").exists()
