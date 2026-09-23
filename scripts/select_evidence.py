#!/usr/bin/env python3
"""Copy final OpenAI API traces into stable reviewer-facing paths."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results/final/evidence"
CHOICES = {
    "first_shot": (
        "results/final/internal/full_loop_public",
        "case_001_counter_syntax",
        "FIXED",
    ),
    "format_retry": (
        "results/final/internal/full_loop_public",
        "case_008_fifo_sequential",
        "FIXED",
    ),
    "one_shot_failure": (
        "results/final/internal/single_shot_public",
        "case_006_fifo_boundary",
        "MAX_RETRY",
    ),
    "semantic_retry": (
        "results/final/external/chipbench/live",
        "chipbench_arithmetic_Prob001_continuous_input_sequence_detect",
        "FIXED",
    ),
    "final_failure": (
        "results/final/external/chipbench/live",
        "chipbench_timing_Prob002_extraneous_items_sequence_detect",
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
        (destination / "origin.json").write_text(
            json.dumps(
                {
                    "record_type": "representative_evidence_origin",
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
