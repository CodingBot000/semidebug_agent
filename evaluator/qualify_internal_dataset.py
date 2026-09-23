#!/usr/bin/env python3
"""Verify final gold designs and broken cases with real EDA before model evaluation."""

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from semidebug.benchmark.loader import load_case
from semidebug.tools.validation import regress, validate
from semidebug.tools.workspace import copy_project

ROOT = Path(__file__).resolve().parents[1]


def statuses(bundle):
    return {name: result.status for name, result in bundle.results.items()}


def qualify(root: Path, gold_root: Path) -> dict:
    cases = sorted(root.glob("*/case_*/case.json"))
    if len(cases) != 30:
        raise ValueError(f"Expected 30 final cases; found {len(cases)}")
    gold = {}
    broken = []
    with tempfile.TemporaryDirectory(prefix="semidebug-v2-audit-") as temporary:
        work = Path(temporary)
        for index, manifest in enumerate(cases):
            source = manifest.parent
            case = load_case(source)
            files = sorted(set(case.mutable + case.immutable + ["case.json"]))
            candidate = work / f"case-{index:02d}"
            copy_project(source, candidate, files)
            target = validate(candidate, case)
            regression = regress(candidate, case) if target.passed else None
            if target.infrastructure_error or (regression and regression.infrastructure_error):
                raise RuntimeError(f"EDA infrastructure error: {case.id}")
            failed = not (target.passed and regression and regression.passed)
            broken.append(
                {
                    "case_id": case.id,
                    "target": statuses(target),
                    "regression": statuses(regression) if regression else None,
                    "failure_reproduced": bool(failed),
                }
            )
            if case.design_top not in gold:
                for mutable in case.mutable:
                    (candidate / mutable).write_bytes(
                        (gold_root / case.design_top / mutable).read_bytes()
                    )
                gold_target = validate(candidate, case)
                gold_regression = regress(candidate, case) if gold_target.passed else None
                gold[case.design_top] = {
                    "target": statuses(gold_target),
                    "regression": statuses(gold_regression) if gold_regression else None,
                    "passed": bool(
                        gold_target.passed and gold_regression and gold_regression.passed
                    ),
                }
    return {
        "measurement": "final-dataset-qualification-no-model",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_cases": len(broken),
        "broken_reproduced": sum(row["failure_reproduced"] for row in broken),
        "gold_passed": sum(row["passed"] for row in gold.values()),
        "gold_total": len(gold),
        "gold": gold,
        "cases": broken,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT / "benchmark_v2")
    parser.add_argument("--gold", type=Path, default=ROOT / "evaluator/gold")
    args = parser.parse_args()
    report = qualify(args.root, args.gold)
    print(json.dumps(report, indent=2))
    if report["broken_reproduced"] != 30 or report["gold_passed"] != report["gold_total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
