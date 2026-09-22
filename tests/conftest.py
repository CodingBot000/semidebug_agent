import difflib
from pathlib import Path

import pytest

from semidebug.benchmark.loader import load_case

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def counter():
    return ROOT / "benchmark/public/case_003_counter_boundary"


@pytest.fixture
def fifo():
    return ROOT / "examples/fifo_off_by_one"


@pytest.fixture
def make_responses():
    def make(root, replacement=None, path=None):
        case = load_case(root)
        name = path or case.mutable[0]
        old = (root / name).read_text()
        gold = (
            (ROOT / "evaluator/gold" / case.design_top / name).read_text()
            if replacement is None
            else replacement
        )
        diff = "".join(
            difflib.unified_diff(
                old.splitlines(True),
                gold.splitlines(True),
                fromfile="a/" + name,
                tofile="b/" + name,
            )
        )
        return [
            {
                "hypotheses": [
                    {
                        "summary": "Scripted fixture hypothesis",
                        "likely_files": [name],
                        "likely_lines": [1],
                        "reasoning": "Test double; external tools determine success",
                        "confidence": 0.8,
                        "evidence_ids": ["baseline:simulation"],
                    }
                ]
            },
            {
                "explanation": "Scripted test candidate, not AI-generated",
                "unified_diff": diff,
                "expected_effect": "Exercise validation loop",
                "risks": [],
            },
        ]

    return make
