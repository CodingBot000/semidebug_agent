#!/usr/bin/env python3
"""Normalize frozen ChipBench qualification and live results without dropping cases."""

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/v2/external/chipbench"
MANIFEST = ROOT / "external/chipbench/selection_manifest.json"
SEMANTIC = {
    "COMPILE_RETRY",
    "SIMULATION_RETRY",
    "LINT_RETRY",
    "SYNTHESIS_RETRY",
    "REGRESSION_RETRY",
}


def analyze(base: Path = BASE, manifest_path: Path = MANIFEST) -> tuple[dict, list[dict]]:
    manifest = json.loads(manifest_path.read_text())
    qualification = json.loads((base / "qualification.json").read_text())
    runs = json.loads((base / "live/results.json").read_text())
    selected = {"chipbench_" + row["case_id"] for row in manifest["selected"]}
    qualified = {row["case_id"]: row["status"] for row in qualification["cases"]}
    by_case = {run["case_id"]: run for run in runs}
    if len(selected) != 12 or set(qualified) != selected:
        raise ValueError("Qualification does not match all 12 frozen selections")
    compatible = {case_id for case_id, status in qualified.items() if status == "compatible"}
    if set(by_case) != compatible:
        raise ValueError("Live result set differs from prequalified compatible cases")
    rows = []
    for case_id in sorted(selected):
        run = by_case.get(case_id)
        prior = [a.get("retry_reason") for a in run["patch_attempts"][:-1]] if run else []
        rows.append(
            {
                "case_id": case_id,
                "qualification": qualified[case_id],
                "attempted": bool(run),
                "fixed": bool(run and run["success"]),
                "first_attempt_fixed": bool(run and run["success"] and run["iteration"] == 1),
                "semantic_retry_rescued": bool(
                    run and run["success"] and any(reason in SEMANTIC for reason in prior)
                ),
                "status": run["final_status"] if run else qualified[case_id],
                "attempts": run["iteration"] if run else 0,
                "retry_reasons": ";".join(reason for reason in prior if reason),
                "duration_ms": run["duration_ms"] if run else 0,
            }
        )
    summary = {
        "measurement": "v2-chipbench-live-ai-repair",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "upstream_commit": manifest["commit"],
        "selected": len(selected),
        "compatible": len(compatible),
        "attempted": sum(row["attempted"] for row in rows),
        "fixed": sum(row["fixed"] for row in rows),
        "first_attempt_fixed": sum(row["first_attempt_fixed"] for row in rows),
        "semantic_retry_rescued": sum(row["semantic_retry_rescued"] for row in rows),
        "unsupported": sum(row["qualification"] == "unsupported" for row in rows),
        "baseline_pass": sum(row["qualification"] == "baseline_pass" for row in rows),
        "infra_error": sum(row["qualification"] == "infra_error" for row in rows),
        "final_failure": sum(row["attempted"] and not row["fixed"] for row in rows),
        "failure_statuses": dict(
            Counter(row["status"] for row in rows if row["attempted"] and not row["fixed"])
        ),
        "scope_note": "External to the project's self-made RTL benchmark; absence from model pretraining is not established.",
    }
    return summary, rows


def main() -> None:
    summary, rows = analyze()
    (BASE / "evaluation.json").write_text(
        json.dumps({"summary": summary, "cases": rows}, indent=2) + "\n"
    )
    with (BASE / "evaluation.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "evaluation.md").write_text(
        "# V2 ChipBench evaluation\n\n"
        f"Selected {summary['selected']}; compatible {summary['compatible']}; "
        f"attempted {summary['attempted']}; fixed {summary['fixed']}; "
        f"first attempt {summary['first_attempt_fixed']}; "
        f"semantic retry rescue {summary['semantic_retry_rescued']}; "
        f"final failure {summary['final_failure']}.\n\n" + summary["scope_note"] + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
