#!/usr/bin/env python3
"""Build the final self-contained submission ZIP from an explicit allowlist."""

import posixpath
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "SemiDebug_Agent"
LIMIT = 50_000_000
TREES = ("src", "scripts", "benchmark_v2", "evaluator", "examples", "tests")
TOP_FILES = (
    "README.md",
    "PORTFOLIO_EVIDENCE.md",
    "VERIFICATION_REPORT.md",
    "QUICKSTART.md",
    "SUBMISSION_GUIDE.md",
    "LICENSE",
    "Dockerfile",
    "Makefile",
    "pyproject.toml",
    "uv.lock",
    "requirements.lock",
    ".python-version",
    ".env.example",
    ".dockerignore",
    "run_demo.sh",
)
DOC_FILES = (
    "docs/ARCHITECTURE.md",
    "docs/architecture.mmd",
    "docs/EVALUATION.md",
    "docs/EXTERNAL_BENCHMARK_PROTOCOL.md",
    "docs/LIMITATIONS.md",
    "docs/THIRD_PARTY.md",
    "docs/OPENAI_API.md",
    "docs/SECURITY.md",
)
RESULT_FILES = (
    "results/README.md",
    "results/final/README.md",
    "results/final/verification/environment.json",
    "results/final/verification/lint.log",
    "results/final/verification/test_all.log",
    "results/final/verification/scripted_demo.log",
    "results/final/verification/scripted_demo_result.json",
    "results/final/verification/scripted_demo_report.md",
    "results/final/verification/verification_summary.json",
    "results/final/dataset_audit.json",
    "results/final/pipeline_validation_summary.json",
    "results/final/internal/comparison.json",
    "results/final/internal/comparison.csv",
    "results/final/internal/comparison.md",
    "results/final/external/chipbench/qualification.json",
    "results/final/external/chipbench/live/summary.json",
    "results/final/external/chipbench/live/summary.md",
    "results/final/external/chipbench/live/results.json",
    "results/final/external/chipbench/live/results.csv",
    "results/final/external/chipbench/evaluation.json",
    "results/final/external/chipbench/evaluation.csv",
    "results/final/external/chipbench/evaluation.md",
    "external/chipbench/selection_manifest.json",
)
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".build", "obj_dir"}
EXCLUDED_FILES = {
    "evaluator/build_dataset.py",
    "evaluator/build_v2_dataset.py",
    "evaluator/record_examples.py",
    "examples/scripted_fifo_responses.json",
}
EXCLUDED_TREES = {"examples/fifo_off_by_one"}
SECRETS = (
    re.compile(rb"(?:sk-(?:proj-)?|gh[pousr]_)[A-Za-z0-9_-]{20,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
)
LOCAL_PATH = re.compile(rb"(?<![A-Za-z0-9:])/(?:Users|home)/[A-Za-z0-9._-]+")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def entries(root: Path) -> dict[str, Path]:
    selected = {}
    for name in (*TOP_FILES, *DOC_FILES, *RESULT_FILES):
        selected[name] = root / name
    for base in TREES:
        for path in sorted((root / base).rglob("*")):
            relative = path.relative_to(root)
            if path.is_file() and not any(part in EXCLUDED_PARTS for part in relative.parts):
                if relative.as_posix() in EXCLUDED_FILES:
                    continue
                if any(
                    relative.as_posix() == prefix or relative.as_posix().startswith(prefix + "/")
                    for prefix in EXCLUDED_TREES
                ):
                    continue
                if (
                    path.name != ".DS_Store"
                    and not path.name.startswith(".env")
                    and path.suffix not in {".pyc", ".vvp"}
                ):
                    selected[relative.as_posix()] = path
    for condition in (
        "full_loop_public",
        "full_loop_hidden",
        "single_shot_public",
        "single_shot_hidden",
    ):
        for filename in ("summary.json", "summary.md", "results.json", "results.csv"):
            name = f"results/final/internal/{condition}/{filename}"
            selected[name] = root / name
    for path in sorted((root / "results/final/evidence").rglob("*")):
        if path.is_file():
            selected[path.relative_to(root).as_posix()] = path
    for name, path in selected.items():
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Required submission file missing or symlinked: {name}")
    return selected


def verify(selected: dict[str, Path]) -> None:
    verify_bytes({name: path.read_bytes() for name, path in selected.items()})


def verify_bytes(selected: dict[str, bytes]) -> None:
    names = set(selected)
    for name, data in selected.items():
        if any(pattern.search(data) for pattern in SECRETS):
            raise ValueError(f"Potential secret in {name}; value withheld")
        if LOCAL_PATH.search(data):
            raise ValueError(f"Local absolute path in {name}; value withheld")
        if name.endswith(".md"):
            for target in LINK.findall(data.decode("utf-8")):
                target = target.strip("<>").split("#", 1)[0]
                if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue
                resolved = posixpath.normpath(
                    posixpath.join(posixpath.dirname(name), unquote(target))
                )
                if resolved not in names and not any(
                    item.startswith(resolved.rstrip("/") + "/") for item in names
                ):
                    raise ValueError(f"Broken relative Markdown link in {name}: {target}")


def scan_archive(output: Path) -> dict:
    with zipfile.ZipFile(output) as archive:
        members = archive.namelist()
        if len(members) != len(set(members)):
            raise ValueError("Duplicate ZIP member")
        if any(not name.startswith(PREFIX + "/") for name in members):
            raise ValueError("ZIP member outside submission root")
        if any(
            not (relative := name.removeprefix(PREFIX + "/"))
            or posixpath.normpath(relative) != relative
            or relative.startswith("/")
            for name in members
        ):
            raise ValueError("Unsafe ZIP member path")
        files = {name.removeprefix(PREFIX + "/"): archive.read(name) for name in members}
    names = set(files)
    required = {
        "README.md",
        "PORTFOLIO_EVIDENCE.md",
        "VERIFICATION_REPORT.md",
        "docs/EVALUATION.md",
        "results/final/verification/verification_summary.json",
        "results/final/verification/lint.log",
        "results/final/verification/test_all.log",
        "results/final/verification/scripted_demo.log",
        "results/final/verification/scripted_demo_result.json",
        "results/final/verification/scripted_demo_report.md",
    }
    if not required <= names:
        raise ValueError(f"Required ZIP members missing: {sorted(required - names)}")
    if any(
        name.startswith("external/chipbench/cases/")
        or name.startswith("benchmark/")
        or name.startswith("results/v2/")
        or name.endswith(("_ref.sv", "_test.sv"))
        or name.endswith("PROVENANCE.json")
        or any(part in {".git", "auth.json", "credentials"} for part in name.split("/"))
        or (Path(name).name.startswith(".env") and Path(name).name != ".env.example")
        for name in names
    ):
        raise ValueError("Forbidden credential, metadata or external reference ZIP member")
    verify_bytes(files)
    size = output.stat().st_size
    if size >= LIMIT:
        raise ValueError(f"Submission size {size} is not below {LIMIT} bytes")
    return {
        "status": "PASS",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "zip_bytes": size,
        "file_count": len(files),
        "under_50mb": True,
        "secret_scan": "PASS",
        "markdown_links": "PASS",
        "absolute_paths": "PASS",
        "self_contained_package": True,
        "credential_files_absent": True,
        "external_reference_solutions_absent": True,
    }


def package(root: Path = ROOT) -> Path:
    selected = entries(root)
    verify(selected)
    output = root / "dist/SemiDebug_Agent_Submission.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, path in sorted(selected.items()):
            info = zipfile.ZipInfo(f"{PREFIX}/{name}", (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if path.suffix == ".sh" else 0o100644) << 16
            archive.writestr(info, path.read_bytes())
    try:
        scan = scan_archive(output)
    except ValueError:
        output.unlink()
        raise
    size = scan["zip_bytes"]
    print(f"ZIP: {output}\nBytes: {size}\nFiles: {len(selected)}")
    return output


if __name__ == "__main__":
    package()
