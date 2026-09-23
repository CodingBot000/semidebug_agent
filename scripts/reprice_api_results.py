#!/usr/bin/env python3
"""Recompute derived API cost fields from recorded token counts."""

import argparse
import csv
import json
from pathlib import Path

from semidebug.benchmark.metrics import aggregate
from semidebug.models import RunState
from semidebug.report.renderer import render_run


def price(state: RunState, input_price: float, cached_price: float, output_price: float) -> None:
    if state.billing_mode != "openai-api":
        return
    uncached = max(0, state.input_tokens - state.cached_input_tokens)
    state.estimated_cost = (
        uncached * input_price
        + state.cached_input_tokens * cached_price
        + state.output_tokens * output_price
    ) / 1_000_000


def update_condition(
    directory: Path,
    input_price: float,
    cached_price: float,
    output_price: float,
    source: str,
) -> None:
    results_path = directory / "results.json"
    states = [RunState.model_validate(row) for row in json.loads(results_path.read_text())]
    for state in states:
        price(state, input_price, cached_price, output_price)
        state.price_source = source
        run = directory / "runs" / state.run_id
        for name in ("run.json", "result.json", "final/metrics.json"):
            path = run / name
            if path.is_file():
                path.write_text(state.model_dump_json(indent=2) + "\n")
        if run.is_dir():
            (run / "report.md").write_text(render_run(state))

    rows = [state.model_dump() for state in states]
    results_path.write_text(json.dumps(rows, indent=2) + "\n")
    checkpoint = directory / "checkpoint.json"
    if checkpoint.is_file():
        data = json.loads(checkpoint.read_text())
        data["results"] = rows
        checkpoint.write_text(json.dumps(data, indent=2) + "\n")

    csv_path = directory / "results.csv"
    if csv_path.is_file():
        with csv_path.open(newline="") as stream:
            csv_rows = list(csv.DictReader(stream))
        costs = {state.case_id: state.estimated_cost for state in states}
        for row in csv_rows:
            row["estimated_cost"] = str(costs[row["case_id"]])
        with csv_path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(csv_rows[0]))
            writer.writeheader()
            writer.writerows(csv_rows)

    summary = aggregate(states)
    (directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (directory / "summary.md").write_text(
        "# Benchmark\n\n"
        + f"Measurement: **{summary['measurement']}**\n\n"
        + f"Fixed {summary['fixed']}/{summary['total']} cases.\n\n"
        + "```json\n"
        + json.dumps(summary, indent=2)
        + "\n```\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--input-price", type=float, required=True)
    parser.add_argument("--cached-input-price", type=float, required=True)
    parser.add_argument("--output-price", type=float, required=True)
    parser.add_argument("--source", required=True)
    args = parser.parse_args()
    conditions = sorted(path.parent for path in args.root.rglob("results.json"))
    if not conditions:
        raise SystemExit("No benchmark results.json files found")
    for directory in conditions:
        update_condition(
            directory,
            args.input_price,
            args.cached_input_price,
            args.output_price,
            args.source,
        )
        print(directory)


if __name__ == "__main__":
    main()
