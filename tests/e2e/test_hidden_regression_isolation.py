import json
import shutil
from pathlib import Path

import pytest

from semidebug.agent.orchestrator import repair
from semidebug.benchmark.loader import load_case
from semidebug.llm.fake import ScriptedProvider

pytestmark = pytest.mark.e2e
ROOT = Path(__file__).resolve().parents[2]


def test_hidden_regression_runs_without_entering_provider_request(tmp_path, make_responses):
    source = ROOT / "benchmark_v2/public/case_006_fifo_boundary"
    case_root = tmp_path / "case"
    shutil.copytree(source, case_root)
    case = load_case(case_root)
    hidden_path = case.regression[0].sources[0]
    hidden = case_root / hidden_path
    hidden.write_text(hidden.read_text() + "\n// HIDDEN_SENTINEL\n")

    provider = ScriptedProvider(make_responses(case_root))
    result = repair(case_root, provider, tmp_path / "runs")

    assert result.final_status == "FIXED"
    assert result.regression_pass and result.integrity_pass
    request = json.dumps(provider.requests)
    assert "HIDDEN_SENTINEL" not in request
    assert hidden_path not in request
