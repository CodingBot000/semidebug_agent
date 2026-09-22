import statistics
from collections import Counter

from semidebug.models import RunState


def aggregate(runs: list[RunState]) -> dict:
    total = len(runs)
    fixed = [r for r in runs if r.success and r.regression_pass and r.integrity_pass]
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
        "average_llm_calls": statistics.mean(r.llm_calls for r in runs) if runs else 0,
        "input_tokens": sum(r.input_tokens for r in runs),
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
