import json
from pathlib import Path

from semidebug.benchmark.loader import load_case
from semidebug.context.selector import select_context

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples/fifo_off_by_one_v2"


def test_default_demo_hides_separate_regression_sources():
    case = load_case(DEMO)
    target = set(case.target.sources)
    regression = [source for test in case.regression for source in test.sources]
    assert len(regression) == len(set(regression)) == 2
    assert target.isdisjoint(regression)
    assert case.prompt_visible == ["rtl/fifo.v", "tb/fifo_target_tb.v"]
    assert not set(regression) & set(case.prompt_visible)

    context = select_context(DEMO, case, [])
    serialized = json.dumps(context)
    assert "tb/fifo_target_tb.v" in context["sources_with_line_numbers"]
    for source in regression:
        assert source not in serialized
        assert (DEMO / source).read_text().splitlines()[0] not in serialized
