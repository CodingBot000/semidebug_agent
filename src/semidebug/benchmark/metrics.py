import statistics
from collections import Counter

from semidebug.models import RunState


def aggregate(runs: list[RunState]) -> dict:
    total = len(runs)
    fixed = [r for r in runs if r.success and r.regression_pass and r.integrity_pass]
    rescued = [r for r in fixed if r.iteration > 1]
    semantic_reasons = {
        "COMPILE_RETRY",
        "SIMULATION_RETRY",
        "LINT_RETRY",
        "SYNTHESIS_RETRY",
        "REGRESSION_RETRY",
    }
    format_reasons = {"PATCH_PARSE_RETRY", "PATCH_GUARD_RETRY"}
    semantic_rescued = [
        r for r in rescued if any(a.retry_reason in semantic_reasons for a in r.patch_attempts[:-1])
    ]
    format_only_rescued = [
        r
        for r in rescued
        if r not in semantic_rescued
        and any(a.retry_reason in format_reasons for a in r.patch_attempts[:-1])
    ]
    attempts = sum(sum(a.proposal is not None for a in r.patch_attempts) for r in runs)
    rejected = sum(sum(a.guard_error is not None for a in r.patch_attempts) for r in runs)
    categories = sorted({r.category for r in runs})
    return {
        "measurement": "live-ai-repair"
        if runs and all(r.provider.startswith("live-") for r in runs)
        else "scripted-test-not-ai-performance",
        "total": total,
        "fixed": len(fixed),
        "repair_success_rate": len(fixed) / total if total else 0,
        "first_attempt_fix_rate": sum(r.iteration == 1 for r in fixed) / total if total else 0,
        "first_attempt_success_rate": sum(r.iteration == 1 for r in fixed) / total if total else 0,
        "final_success_rate": len(fixed) / total if total else 0,
        "retry_rescue_count": len(rescued),
        "semantic_retry_rescue_count": len(semantic_rescued),
        "format_retry_rescue_count": len(format_only_rescued),
        "regression_rejection_count": sum(
            a.retry_reason == "REGRESSION_RETRY" for r in runs for a in r.patch_attempts
        ),
        "retry_reason_counts": dict(
            Counter(a.retry_reason for r in runs for a in r.patch_attempts if a.retry_reason)
        ),
        "average_attempts": statistics.mean(r.iteration for r in runs) if runs else 0,
        "median_attempts": statistics.median(r.iteration for r in runs) if runs else 0,
        "regression_integrity_rate": sum(r.regression_pass and r.integrity_pass for r in fixed)
        / len(fixed)
        if fixed
        else None,
        "patch_attempts": attempts,
        "invalid_patch_attempts": rejected,
        "invalid_patch_rate": rejected / attempts if attempts else 0,
        "average_retry_count": statistics.mean(max(0, r.iteration - 1) for r in runs)
        if runs
        else 0,
        "median_repair_time_ms": statistics.median(r.duration_ms for r in runs) if runs else 0,
        "median_latency_ms": statistics.median(r.duration_ms for r in runs) if runs else 0,
        "average_llm_calls": statistics.mean(r.llm_calls for r in runs) if runs else 0,
        "input_tokens": sum(r.input_tokens for r in runs),
        "cached_input_tokens": sum(r.cached_input_tokens for r in runs),
        "models": sorted({r.model for r in runs}),
        "reasoning_efforts": sorted({r.reasoning_effort for r in runs if r.reasoning_effort}),
        "billing_modes": sorted({r.billing_mode for r in runs if r.billing_mode}),
        "output_tokens": sum(r.output_tokens for r in runs),
        "estimated_cost": sum(r.estimated_cost for r in runs)
        if runs and all(r.estimated_cost is not None for r in runs)
        else None,
        "failure_breakdown": dict(Counter(r.final_status for r in runs if r not in fixed)),
        "categories": {
            c: {
                "total": sum(r.category == c for r in runs),
                "fixed": sum(r.category == c for r in fixed),
            }
            for c in categories
        },
        "retry_distribution": dict(Counter(str(max(0, r.iteration - 1)) for r in runs)),
    }
