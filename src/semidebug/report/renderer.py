from pathlib import Path

from semidebug.models import RunState


def render_run(state: RunState) -> str:
    lines = [
        f"# Evidence: {state.case_id}",
        "",
        f"**{state.final_status}** — provider `{state.provider}`, model `{state.model}`.",
        "",
        f"Category: {state.category}. Immutable integrity: {state.integrity_pass}.",
        f"Reasoning: {state.reasoning_effort or 'unspecified'}; billing: {state.billing_mode or 'unspecified'}.",
        f"Failure reason: {state.failure_reason or 'none'}",
        "",
        "| Check | Baseline | "
        + " | ".join(f"Attempt {a.iteration}" for a in state.patch_attempts)
        + " |",
        "|---|---|" + "---|" * len(state.patch_attempts),
    ]
    for check in ["compile", "simulation", "lint", "synthesis"]:
        bundles = [state.baseline, *[a.validation for a in state.patch_attempts]]
        cells = [
            b.results[check].status.upper() if b and check in b.results else "NOT RUN"
            for b in bundles
        ]
        lines.append(f"| {check} | " + " | ".join(cells) + " |")
    for attempt in state.patch_attempts:
        lines += [
            "",
            f"## Attempt {attempt.iteration}",
            "",
            attempt.hypothesis.summary if attempt.hypothesis else "No hypothesis returned.",
        ]
        if attempt.guard_error:
            lines += ["", f"Rejected: {attempt.guard_error}"]
        if attempt.proposal:
            lines += [
                "",
                attempt.proposal.explanation,
                "",
                "```diff",
                attempt.proposal.unified_diff.rstrip(),
                "```",
            ]
        if attempt.regression:
            lines += ["", "Regression: " + ("PASS" if attempt.regression.passed else "FAIL")]
    lines += [
        "",
        f"Duration: {state.duration_ms} ms; Provider calls: {state.llm_calls}; tokens in/out: {state.input_tokens}/{state.output_tokens}.",
        f"Estimated cost: {state.estimated_cost if state.estimated_cost is not None else 'unknown/unconfigured'}.",
        "",
        "Scripted providers and replay output are not live AI benchmark results.",
    ]
    return "\n".join(lines) + "\n"


def save_report(state: RunState, directory: Path):
    (directory / "report.md").write_text(render_run(state))
