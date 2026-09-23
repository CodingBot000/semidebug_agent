#!/usr/bin/env python3
"""Measure pipeline acceptance with known fixes, NEVER claim AI performance.
Only this offline evaluator reads gold; provider requests cannot access it.
"""

import argparse
import difflib
import json
from pathlib import Path

from semidebug.benchmark.loader import load_case
from semidebug.benchmark.runner import run_benchmark
from semidebug.config import Settings
from semidebug.llm.fake import ScriptedProvider

ROOT = Path(__file__).resolve().parents[1]


def response(root, replacement=None):
    case = load_case(root)
    path = case.mutable[0]
    old = (root / path).read_text()
    new = (
        (ROOT / "evaluator/gold" / case.design_top / path).read_text()
        if replacement is None
        else replacement
    )
    diff = "".join(
        difflib.unified_diff(
            old.splitlines(True), new.splitlines(True), fromfile="a/" + path, tofile="b/" + path
        )
    )
    return [
        {
            "hypotheses": [
                {
                    "summary": "Scripted evaluator proposal (known fix)",
                    "likely_files": [path],
                    "likely_lines": [1],
                    "reasoning": "Pipeline acceptance check, not AI inference",
                    "confidence": 1.0,
                    "evidence_ids": ["baseline:simulation"],
                }
            ]
        },
        {
            "explanation": "Known fix supplied by evaluator to test pipeline only",
            "unified_diff": diff,
            "expected_effect": "Restore reference behavior",
            "risks": [],
        },
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--benchmark-root", type=Path, default=ROOT / "benchmark")
    parser.add_argument("--expected-count", type=int, default=30)
    args = parser.parse_args()
    responses = []
    for manifest in sorted(args.benchmark_root.rglob("case.json")):
        responses += response(manifest.parent)
    summary = run_benchmark(
        args.benchmark_root, ScriptedProvider(responses), args.output, Settings()
    )
    if summary["fixed"] != args.expected_count or summary["total"] != args.expected_count:
        raise SystemExit("Pipeline acceptance failed; inspect individual evidence")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
