#!/usr/bin/env python3
"""Qualify pinned ChipBench cases before any model invocation."""

import argparse
import json
import re
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from semidebug.benchmark.loader import load_case
from semidebug.tools.validation import regress, validate
from semidebug.tools.workspace import copy_project

ROOT = Path(__file__).resolve().parents[1]


def summarize(bundle):
    return {
        name: {
            "status": result.status,
            "stderr_tail": result.stderr[-1000:] if result.status != "pass" else "",
        }
        for name, result in bundle.results.items()
    }


def qualify(root: Path) -> dict:
    manifests = sorted(root.glob("*/case.json"))
    if len(manifests) != 12:
        raise ValueError(f"Expected 12 frozen ChipBench cases, found {len(manifests)}")
    rows = []
    with tempfile.TemporaryDirectory(prefix="semidebug-chipbench-audit-") as temporary:
        work = Path(temporary)
        for index, manifest in enumerate(manifests):
            source = manifest.parent
            case = load_case(source)
            files = sorted(set(case.mutable + case.immutable + ["case.json"]))
            baseline = work / f"baseline-{index:02d}"
            copy_project(source, baseline, files)
            baseline_official = regress(baseline, case)

            gold = work / f"gold-{index:02d}"
            copy_project(source, gold, files)
            reference = (gold / "tb/ref.sv").read_text()
            corrected, count = re.subn(
                r"\bmodule\s+RefModule\b", "module TopModule", reference, count=1
            )
            if count != 1:
                raise ValueError(f"Cannot normalize reference module: {case.id}")
            (gold / "rtl/TopModule.sv").write_text(corrected)
            gold_target = validate(gold, case)
            gold_official = regress(gold, case)

            if any(
                bundle.infrastructure_error
                for bundle in (baseline_official, gold_target, gold_official)
            ):
                status = "infra_error"
            elif not gold_target.passed or not gold_official.passed:
                status = "unsupported"
            elif baseline_official.passed:
                status = "baseline_pass"
            else:
                status = "compatible"
            rows.append(
                {
                    "case_id": case.id,
                    "category": case.category,
                    "status": status,
                    "baseline_official": summarize(baseline_official),
                    "gold_target": summarize(gold_target),
                    "gold_official": summarize(gold_official),
                }
            )
    counts = Counter(row["status"] for row in rows)
    return {
        "measurement": "chipbench-qualification-no-model",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "selected": len(rows),
        "status_counts": dict(counts),
        "cases": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT / "external/chipbench/cases")
    args = parser.parse_args()
    print(json.dumps(qualify(args.root), indent=2))


if __name__ == "__main__":
    main()
