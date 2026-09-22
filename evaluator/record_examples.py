#!/usr/bin/env python3
"""Produce clearly labelled real-EDA/scripted-provider example evidence."""

import json
import shutil
from pathlib import Path

from run_pipeline_benchmark import response

from semidebug.agent.orchestrator import repair
from semidebug.llm.fake import ScriptedProvider

ROOT = Path(__file__).resolve().parents[1]


def record(label, root, responses, expected):
    result = repair(root, ScriptedProvider(responses), ROOT / "artifacts/evidence")
    if result.final_status != expected:
        raise SystemExit(f"{label}: {result.final_status}")
    source = ROOT / "artifacts/evidence" / result.run_id
    destination = ROOT / "results" / label
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    return result


def main():
    fifo = ROOT / "examples/fifo_off_by_one"
    scripted = response(fifo)
    (ROOT / "examples/scripted_fifo_responses.json").write_text(
        json.dumps(scripted, indent=2) + "\n"
    )
    record("sample_run", fifo, scripted, "FIXED")
    counter = ROOT / "benchmark/public/case_003_counter_boundary"
    old = (counter / "rtl/counter.v").read_text()
    record(
        "retry_run",
        counter,
        response(counter, old.replace("4'd8", "4'd7")) + response(counter),
        "FIXED",
    )
    repeated = response(counter, old.replace("4'd8", "4'd7"))
    record("failed_run", counter, repeated + repeated, "REPEATED_PATCH")


if __name__ == "__main__":
    main()
