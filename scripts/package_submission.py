#!/usr/bin/env python3
"""Allowlisted reproducible portfolio ZIP with secret/size gates."""

import hashlib
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP_FILES = {
    "README.md",
    "LICENSE",
    "PORTFOLIO_EVIDENCE.md",
    "QUICKSTART.md",
    "pyproject.toml",
    "uv.lock",
    "requirements.lock",
    ".python-version",
    ".env.example",
    ".gitignore",
    ".gitattributes",
    ".dockerignore",
    "Dockerfile",
    "Makefile",
    "run_demo.sh",
}
TOP_DIRS = {
    "src",
    "tests",
    "examples",
    "benchmark",
    "evaluator",
    "scripts",
    "results",
    "docs",
    ".github",
}
EXCLUDED = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    ".build",
    "obj_dir",
}
SECRETS = [
    re.compile(rb"(?:sk-(?:proj-)?|gh[pousr]_)[A-Za-z0-9_-]{20,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
]
REQUIRED = {
    "README.md",
    "PORTFOLIO_EVIDENCE.md",
    "QUICKSTART.md",
    "src/semidebug/cli.py",
    "results/benchmark_results.json",
    "results/benchmark_results.csv",
    "results/benchmark_summary.md",
    "results/sample_run/result.json",
    "scripts/run_demo.sh",
    "uv.lock",
}


def scan(data: bytes, label: str):
    if any(pattern.search(data) for pattern in SECRETS):
        raise ValueError(f"Potential secret in {label}; value withheld")


def candidates(root: Path):
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if relative.parts[0] not in TOP_DIRS and str(relative) not in TOP_FILES:
            continue
        if any(part in EXCLUDED for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Symlink excluded: {relative}")
        if not path.is_file() or path.name == ".DS_Store" or path.suffix in {".pyc", ".vvp"}:
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            continue
        yield path, relative


def package(root=ROOT):
    files = list(candidates(root))
    included = {str(relative) for _, relative in files}
    missing = REQUIRED - included
    if missing:
        raise ValueError(f"Required submission files missing: {sorted(missing)}")
    for path, relative in files:
        scan(path.read_bytes(), str(relative))
    output = root / "dist/SemiDebug_Agent_SKHynix_Portfolio.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, relative in files:
            info = zipfile.ZipInfo(
                "SemiDebug_Agent_SKHynix_Portfolio/" + str(relative), (2026, 1, 1, 0, 0, 0)
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if path.suffix == ".sh" else 0o100644) << 16
            archive.writestr(info, path.read_bytes())
    size = output.stat().st_size
    if size > 50_000_000:
        output.unlink()
        raise ValueError("Submission exceeds 50 MB")
    checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"ZIP: {output}\nBytes: {size}\nSHA256: {checksum}\nFiles: {len(files)}")
    output.with_suffix(".sha256").write_text(f"{checksum}  {output.name}\n")
    return output


if __name__ == "__main__":
    package()
