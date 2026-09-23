#!/usr/bin/env python3
"""Record Git-verified evaluation ancestry and artifact hashes without self-reference."""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results/v2/PROVENANCE.json"
SELECTION = "external/chipbench/selection_manifest.json"
EXPECTED_V1 = "afc0582e08ba5463a0d4e35630dbebc7432028d4"
ARTIFACTS = (
    SELECTION,
    "results/v2/internal/comparison.json",
    "results/v2/external/chipbench/evaluation.json",
    "docs/V2_EVALUATION.md",
    "PORTFOLIO_EVIDENCE.md",
    "README.md",
    "results/live_codex/summary.md",
)
RAW_TREES = (
    "results/live_codex",
    "results/v2/internal",
    "results/v2/external",
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def commit_metadata(commit: str) -> dict:
    resolved = git("rev-parse", f"{commit}^{{commit}}")
    lines = git("show", "--no-patch", "--format=%H%n%cI%n%s", resolved).splitlines()
    if len(lines) != 3 or lines[0] != resolved:
        raise ValueError(f"Cannot read commit metadata: {commit}")
    return {"commit": resolved, "committed_at": lines[1], "subject": lines[2]}


def ancestry(ancestor: str, descendant: str) -> dict:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT, check=False
    )
    if result.returncode not in (0, 1):
        raise ValueError(f"Git ancestry check failed: {ancestor} -> {descendant}")
    return {"is_ancestor": result.returncode == 0, "exit_code": result.returncode}


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def generate() -> dict:
    v1 = git("rev-parse", "semidebug-v1-baseline^{commit}")
    selection_history = git("log", "--follow", "--format=%H", "--", SELECTION).splitlines()
    if not selection_history:
        raise ValueError("Selection manifest has no Git history")
    selection = git("rev-parse", f"{selection_history[-1]}^{{commit}}")
    internal_candidate = json.loads((ROOT / "results/v2/environment.json").read_text())[
        "source_commit"
    ]
    external_candidate = json.loads(
        (ROOT / "results/v2/external/chipbench/environment.json").read_text()
    )["source_commit"]
    internal = git("rev-parse", f"{internal_candidate}^{{commit}}")
    external = git("rev-parse", f"{external_candidate}^{{commit}}")
    source = git("rev-parse", "HEAD")
    at_selection = sha256(git_bytes("show", f"{selection}:{SELECTION}"))
    current_manifest = sha256((ROOT / SELECTION).read_bytes())
    checks = {
        "v1_to_submission_source": ancestry(v1, source),
        "selection_to_external_evaluation": ancestry(selection, external),
        "internal_evaluation_to_submission_source": ancestry(internal, source),
        "external_evaluation_to_submission_source": ancestry(external, source),
    }
    result = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": "SemiDebug Agent",
        "method": "Tracked source commit precedes this provenance/package commit; a file cannot contain its own final commit hash. The package source commit is recorded in the completion report outside the ZIP.",
        "v1": {
            "tag": "semidebug-v1-baseline",
            "commit": commit_metadata(v1),
            "tag_resolves_to_expected_commit": v1 == EXPECTED_V1,
        },
        "chipbench_selection": {
            "commit": commit_metadata(selection),
            "manifest_sha256_at_commit": at_selection,
            "working_tree_manifest_sha256": current_manifest,
            "manifest_unchanged_since_selection": at_selection == current_manifest,
        },
        "evaluations": {
            "internal_source": commit_metadata(internal),
            "external_source": commit_metadata(external),
        },
        "submission": {"source_commit": commit_metadata(source), "packaging_commit": None},
        "ancestry": checks,
        "raw_result_tree_oids": {path: git("rev-parse", f"HEAD:{path}") for path in RAW_TREES},
        "artifacts": {path: sha256((ROOT / path).read_bytes()) for path in ARTIFACTS},
    }
    if not result["v1"]["tag_resolves_to_expected_commit"]:
        raise ValueError("V1 tag target differs from frozen baseline")
    if not result["chipbench_selection"]["manifest_unchanged_since_selection"]:
        raise ValueError("ChipBench selection manifest changed after selection")
    if not all(item["is_ancestor"] for item in checks.values()):
        raise ValueError("Evaluation ancestry check failed")
    return result


def main() -> None:
    if OUTPUT.exists():
        raise ValueError(f"Provenance already exists: {OUTPUT}")
    result = generate()
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} from verified Git history")


if __name__ == "__main__":
    main()
