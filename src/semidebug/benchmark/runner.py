import csv
import json
from pathlib import Path

from semidebug.agent.orchestrator import repair
from semidebug.benchmark.metrics import aggregate


def run_benchmark(root: Path, provider, output: Path, settings):
    cases = sorted(p.parent for p in root.rglob("case.json"))
    if not cases:
        raise ValueError("No case.json files found")
    output.mkdir(parents=True, exist_ok=False)
    runs = []
    for case in cases:
        result = repair(case, provider, output / "runs", settings)
        runs.append(result)
        (output / "checkpoint.json").write_text(
            json.dumps(
                {
                    "completed": len(runs),
                    "total": len(cases),
                    "last_case": result.case_id,
                    "results": [r.model_dump() for r in runs],
                },
                indent=2,
            )
            + "\n"
        )
        print(f"{result.case_id}: {result.final_status} ({result.iteration} attempts)", flush=True)
    summary = aggregate(runs)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output / "results.json").write_text(
        json.dumps([r.model_dump() for r in runs], indent=2) + "\n"
    )
    rows = []
    for r in runs:
        row = {
            "case_id": r.case_id,
            "bug_category": r.category,
            "success": r.success,
            "status": r.final_status,
            "iterations": r.iteration,
            "llm_calls": r.llm_calls,
            "regression_pass": r.regression_pass,
            "integrity_pass": r.integrity_pass,
            "invalid_patch_attempts": sum(a.guard_error is not None for a in r.patch_attempts),
            "retry_reasons": ";".join(a.retry_reason or "" for a in r.patch_attempts),
            "duration_ms": r.duration_ms,
            "input_tokens": r.input_tokens,
            "output_tokens": r.output_tokens,
            "estimated_cost": r.estimated_cost,
        }
        for check in ["compile", "simulation", "lint", "synthesis"]:
            v = r.current_validation
            row[check + "_pass"] = bool(
                v and check in v.results and v.results[check].status == "pass"
            )
        rows.append(row)
    with (output / "results.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output / "summary.md").write_text(
        "# Benchmark\n\n"
        + f"Measurement: **{summary['measurement']}**\n\n"
        + f"Fixed {summary['fixed']}/{summary['total']} cases.\n\n"
        + "```json\n"
        + json.dumps(summary, indent=2)
        + "\n```\n"
    )
    return summary
