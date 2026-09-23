#!/usr/bin/env python3
"""Compare final OpenAI API full-loop and independent one-shot results."""

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMANTIC = {
    "COMPILE_RETRY",
    "SIMULATION_RETRY",
    "LINT_RETRY",
    "SYNTHESIS_RETRY",
    "REGRESSION_RETRY",
}
FORMAT = {"PATCH_PARSE_RETRY", "PATCH_GUARD_RETRY"}


def load_runs(base: Path, condition: str) -> dict:
    runs = {}
    for split in ("public", "hidden"):
        path = base / f"{condition}_{split}" / "results.json"
        for run in json.loads(path.read_text()):
            if run["case_id"] in runs:
                raise ValueError(f"Duplicate case: {run['case_id']}")
            runs[run["case_id"]] = run
    return runs


def analyze(base: Path) -> tuple[dict, list[dict]]:
    full = load_runs(base, "full_loop")
    single = load_runs(base, "single_shot")
    if set(full) != set(single) or len(full) != 30:
        raise ValueError("Full-loop and single-shot case sets must match all 30 final cases")
    rows = []
    for case_id in sorted(full):
        loop = full[case_id]
        one = single[case_id]
        if loop["model"] != one["model"] or loop["reasoning_effort"] != one["reasoning_effort"]:
            raise ValueError(f"Model configuration differs: {case_id}")
        if loop["max_iterations"] != 3 or one["max_iterations"] != 1:
            raise ValueError(f"Iteration limit differs from protocol: {case_id}")
        previous = [a.get("retry_reason") for a in loop["patch_attempts"][:-1]]
        first_accepted = bool(loop["success"] and loop["iteration"] == 1)
        semantic_rescue = bool(loop["success"] and any(r in SEMANTIC for r in previous))
        format_rescue = bool(
            loop["success"] and not semantic_rescue and any(r in FORMAT for r in previous)
        )
        rows.append(
            {
                "case_id": case_id,
                "category": loop["category"],
                "full_first_proposal_accepted": first_accepted,
                "full_loop_fixed": bool(loop["success"]),
                "single_shot_fixed": bool(one["success"]),
                "semantic_retry_rescue": semantic_rescue,
                "format_retry_rescue": format_rescue,
                "full_attempts": loop["iteration"],
                "full_retry_reasons": ";".join(r for r in previous if r),
                "single_status": one["final_status"],
                "full_duration_ms": loop["duration_ms"],
                "single_duration_ms": one["duration_ms"],
            }
        )
    summary = {
        "measurement": "final-internal-openai-api-ablation",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "total": len(rows),
        "paired_full_first_proposal_accepted": sum(r["full_first_proposal_accepted"] for r in rows),
        "paired_full_final_fixed": sum(r["full_loop_fixed"] for r in rows),
        "paired_retry_rescued": sum(
            r["full_loop_fixed"] and not r["full_first_proposal_accepted"] for r in rows
        ),
        "paired_semantic_retry_rescued": sum(r["semantic_retry_rescue"] for r in rows),
        "paired_format_retry_rescued": sum(r["format_retry_rescue"] for r in rows),
        "independent_single_shot_fixed": sum(r["single_shot_fixed"] for r in rows),
        "independent_full_loop_fixed": sum(r["full_loop_fixed"] for r in rows),
        "independent_absolute_delta": sum(r["full_loop_fixed"] for r in rows)
        - sum(r["single_shot_fixed"] for r in rows),
        "interpretation": "The paired first-proposal comparison uses the same full-loop trajectories. The separately executed one-shot condition is non-deterministic and is not the same sampled proposal as each full-loop first attempt.",
    }
    return summary, rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=ROOT / "results/final/internal")
    args = parser.parse_args()
    summary, rows = analyze(args.base)
    args.base.mkdir(parents=True, exist_ok=True)
    (args.base / "comparison.json").write_text(
        json.dumps({"summary": summary, "cases": rows}, indent=2) + "\n"
    )
    with (args.base / "comparison.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.base / "comparison.md").write_text(
        "# OpenAI API internal ablation\n\n"
        f"Paired full-loop first proposal: {summary['paired_full_first_proposal_accepted']}/30. "
        f"Final: {summary['paired_full_final_fixed']}/30. "
        f"Rescued: {summary['paired_retry_rescued']} "
        f"(semantic {summary['paired_semantic_retry_rescued']}, "
        f"format {summary['paired_format_retry_rescued']}).\n\n"
        f"Independent single-shot: {summary['independent_single_shot_fixed']}/30; "
        f"full loop: {summary['independent_full_loop_fixed']}/30.\n\n"
        + summary["interpretation"]
        + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
