from semidebug.agent.orchestrator import validation_retry_reason
from semidebug.benchmark.metrics import aggregate
from semidebug.models import PatchAttempt, RunState, ValidationBundle, ValidationResult


def result(status):
    return ValidationResult(tool="eda", command=[], exit_code=1, status=status)


def run(case_id, reasons, *, success=True):
    attempts = [
        PatchAttempt(iteration=i + 1, retry_reason=reason) for i, reason in enumerate(reasons)
    ]
    attempts.append(PatchAttempt(iteration=len(attempts) + 1))
    return RunState(
        run_id=case_id,
        case_id=case_id,
        category="boundary",
        provider="live-openai-api",
        model="test",
        max_iterations=3,
        project_root=case_id,
        mutable_files=[],
        immutable_files=[],
        patch_attempts=attempts,
        iteration=len(attempts),
        success=success,
        regression_pass=success,
        integrity_pass=True,
        final_status="FIXED" if success else "MAX_RETRY",
    )


def test_validation_reason_uses_first_failed_gate():
    bundle = ValidationBundle(
        results={
            "compile": result("pass"),
            "simulation": result("fail"),
            "lint": result("fail"),
            "synthesis": result("pass"),
        }
    )
    assert validation_retry_reason(bundle) == "SIMULATION_RETRY"


def test_semantic_and_format_rescues_are_distinct():
    metrics = aggregate(
        [
            run("first", []),
            run("format", ["PATCH_PARSE_RETRY"]),
            run("semantic", ["REGRESSION_RETRY"]),
            run("failed", ["SIMULATION_RETRY"], success=False),
        ]
    )
    assert metrics["first_attempt_success_rate"] == 0.25
    assert metrics["final_success_rate"] == 0.75
    assert metrics["retry_rescue_count"] == 2
    assert metrics["format_retry_rescue_count"] == 1
    assert metrics["semantic_retry_rescue_count"] == 1
    assert metrics["regression_rejection_count"] == 1
