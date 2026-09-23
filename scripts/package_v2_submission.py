#!/usr/bin/env python3
"""Build a self-contained V2 submission ZIP with selected, inspectable evidence."""

import hashlib
import posixpath
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "SemiDebug_Agent_V2"
LIMIT = 50_000_000
TREES = ("src", "scripts", "benchmark", "benchmark_v2", "evaluator", "examples", "tests")
TOP_FILES = (
    "README.md",
    "PORTFOLIO_EVIDENCE.md",
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
    "docs/BENCHMARK.md",
    "docs/V2_EVALUATION.md",
    "docs/EXTERNAL_BENCHMARK_PROTOCOL.md",
    "docs/LIMITATIONS.md",
    "docs/THIRD_PARTY.md",
    "docs/CODEX_CLI.md",
    "docs/SECURITY.md",
    "docs/DECISIONS.md",
    "docs/RESEARCH.md",
    "docs/HWE_BENCH_FEASIBILITY.md",
)
RESULT_FILES = (
    "results/README.md",
    "results/v2/README.md",
    "results/dataset_audit.json",
    "results/benchmark_results.json",
    "results/benchmark_results.csv",
    "results/benchmark_summary.json",
    "results/benchmark_summary.md",
    "results/sample_run/result.json",
    "results/sample_run/report.md",
    "results/retry_run/report.md",
    "results/failed_run/report.md",
    "results/live_codex/summary.json",
    "results/live_codex/summary.md",
    "results/live_codex/public_v1/summary.json",
    "results/live_codex/public_v1/summary.md",
    "results/live_codex/hidden_v1/summary.json",
    "results/live_codex/hidden_v1/summary.md",
    "results/v2/environment.json",
    "results/v2/dataset_audit.json",
    "results/v2/pipeline_validation_summary.json",
    "results/v2/internal/comparison.json",
    "results/v2/internal/comparison.csv",
    "results/v2/internal/comparison.md",
    "results/v2/external/chipbench/qualification.json",
    "results/v2/external/chipbench/environment.json",
    "results/v2/external/chipbench/live/summary.json",
    "results/v2/external/chipbench/live/summary.md",
    "results/v2/external/chipbench/live/results.json",
    "results/v2/external/chipbench/live/results.csv",
    "results/v2/external/chipbench/evaluation.json",
    "results/v2/external/chipbench/evaluation.csv",
    "results/v2/external/chipbench/evaluation.md",
    "external/chipbench/selection_manifest.json",
)
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".build", "obj_dir"}
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
            name = f"results/v2/internal/{condition}/{filename}"
            selected[name] = root / name
    for path in sorted((root / "results/v2/evidence").rglob("*")):
        if path.is_file():
            selected[path.relative_to(root).as_posix()] = path
    aliases = {
        "00_README.md": "README.md",
        "01_PORTFOLIO_EVIDENCE.md": "PORTFOLIO_EVIDENCE.md",
        "02_ARCHITECTURE.md": "docs/ARCHITECTURE.md",
        "03_SUBMISSION_GUIDE.md": "SUBMISSION_GUIDE.md",
        "architecture.mmd": "docs/architecture.mmd",
        "SECURITY.md": "docs/SECURITY.md",
    }
    selected.update({alias: root / source for alias, source in aliases.items()})
    for name, path in selected.items():
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Required submission file missing or symlinked: {name}")
    return selected


def verify(selected: dict[str, Path]) -> None:
    names = set(selected)
    for name, path in selected.items():
        data = path.read_bytes()
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


def package(root: Path = ROOT) -> Path:
    selected = entries(root)
    verify(selected)
    output = root / "dist/SemiDebug_Agent_V2_Submission.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, path in sorted(selected.items()):
            info = zipfile.ZipInfo(f"{PREFIX}/{name}", (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if path.suffix == ".sh" else 0o100644) << 16
            archive.writestr(info, path.read_bytes())
    size = output.stat().st_size
    if size >= LIMIT:
        output.unlink()
        raise ValueError(f"Submission size {size} is not below {LIMIT} bytes")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".sha256").write_text(f"{digest}  {output.name}\n")
    print(f"ZIP: {output}\nBytes: {size}\nSHA256: {digest}\nFiles: {len(selected)}")
    return output


if __name__ == "__main__":
    package()
