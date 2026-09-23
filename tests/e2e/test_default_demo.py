import json
from pathlib import Path

import pytest

from semidebug.agent.orchestrator import repair
from semidebug.llm.fake import ScriptedProvider

pytestmark = pytest.mark.e2e
ROOT = Path(__file__).resolve().parents[2]


def test_scripted_default_demo_runs_real_hidden_regression(tmp_path):
    case = ROOT / "examples/fifo_off_by_one_v2"
    responses = json.loads((ROOT / "examples/scripted_fifo_v2_responses.json").read_text())
    provider = ScriptedProvider(responses)
    run = repair(case, provider, tmp_path)

    assert run.final_status == "FIXED"
    assert run.integrity_pass and run.regression_pass
    assert run.baseline and not run.baseline.passed
    assert run.patch_attempts[0].guard_error is None
    assert run.patch_attempts[0].validation
    assert set(run.patch_attempts[0].validation.results) == {
        "compile",
        "simulation",
        "lint",
        "synthesis",
    }
    assert run.patch_attempts[0].validation.passed
    assert run.patch_attempts[0].regression
    assert run.patch_attempts[0].regression.passed
    assert len(run.patch_attempts[0].regression.results) == 4

    requests = json.dumps(provider.requests)
    assert "fifo_target_tb.v" in requests
    assert "fifo_hidden_regression" not in requests
    assert "SEMIDEBUG_HIDDEN_REGRESSION" not in requests
