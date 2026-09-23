#!/usr/bin/env python3
"""Copy fixed representative V2 traces to stable reviewer-facing paths."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results/v2/evidence"
CHOICES = {
    "first_shot": (
        "results/v2/internal/full_loop_public",
        "case_001_counter_syntax",
        "FIXED",
    ),
    "format_retry": (
        "results/v2/internal/full_loop_public",
        "case_023_alu_width_signedness",
        "FIXED",
    ),
    "one_shot_failure": (
        "results/v2/internal/single_shot_public",
        "case_014_arbiter_combinational",
        "MAX_RETRY",
    ),
    "semantic_retry": (
        "results/v2/external/chipbench/live",
        "chipbench_arithmetic_Prob001_continuous_input_sequence_detect",
        "FIXED",
    ),
    "final_failure": (
        "results/v2/external/chipbench/live",
        "chipbench_arithmetic_Prob002_extraneous_items_sequence_detect",
        "MAX_RETRY",
    ),
}


def select(root: Path = ROOT, output: Path = OUTPUT) -> None:
    if output.exists():
        raise ValueError(f"Evidence output already exists: {output}")
    for label, (relative, case_id, status) in CHOICES.items():
        base = root / relative
        matching = [
            row
            for row in json.loads((base / "results.json").read_text())
            if row["case_id"] == case_id
        ]
        if len(matching) != 1 or matching[0]["final_status"] != status:
            raise ValueError(f"Missing or changed representative case: {case_id}")
        run = matching[0]
        source = base / "runs" / run["run_id"]
        destination = output / label
        shutil.copytree(source, destination)
        (destination / "provenance.json").write_text(
            json.dumps(
                {
                    "measurement": "live-ai-repair",
                    "source_run": f"{relative}/runs/{run['run_id']}",
                    "case_id": case_id,
                    "final_status": status,
                    "model": run["model"],
                    "retry_reasons": [a.get("retry_reason") for a in run["patch_attempts"]],
                },
                indent=2,
            )
            + "\n"
        )
    print(f"Selected {len(CHOICES)} representative traces under {output}")


if __name__ == "__main__":
    select()
