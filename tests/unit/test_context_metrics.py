import json

from semidebug.benchmark.loader import load_case
from semidebug.benchmark.metrics import aggregate
from semidebug.context.selector import select_context
from semidebug.models import RunState


def test_no_gold_or_hidden_metadata(counter):
    context = select_context(counter, load_case(counter), [])
    text = json.dumps(context)
    assert "evaluator" not in text and "ground_truth" not in text and "hidden" not in text
    assert set(context["sources_with_line_numbers"]) == {"rtl/counter.v", "tb/counter_tb.v"}
    assert "metadata.json" not in context["sources_with_line_numbers"]


def test_metrics_denominators():
    def run(**kwargs):
        return RunState(
            run_id="id",
            case_id="c",
            category="boundary",
            provider="scripted-test-double",
            model="test",
            max_iterations=3,
            project_root="c",
            mutable_files=[],
            immutable_files=[],
            **kwargs,
        )

    runs = [
        run(
            success=True,
            regression_pass=True,
            integrity_pass=True,
            iteration=1,
            final_status="FIXED",
        ),
        run(iteration=3, final_status="MAX_RETRY"),
    ]
    metrics = aggregate(runs)
    assert metrics["repair_success_rate"] == 0.5
    assert metrics["first_attempt_fix_rate"] == 0.5
    assert metrics["average_retry_count"] == 1
    assert metrics["estimated_cost"] is None
    assert aggregate([])["regression_integrity_rate"] is None
