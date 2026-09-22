import hashlib
import re
import shutil
from pathlib import Path, PurePosixPath

SAFE_PATH = re.compile(r"^[A-Za-z0-9_./-]+$")


def safe_path(root: Path, value: str) -> Path:
    parts = PurePosixPath(value).parts
    if (
        not SAFE_PATH.fullmatch(value)
        or not parts
        or value.startswith(("/", "-"))
        or any(p in ("..", ".") or p.startswith("-") for p in parts)
        or str(PurePosixPath(value)) != value
    ):
        raise ValueError(f"Unsafe relative path: {value!r}")
    path = root / value
    for parent in [path, *path.parents]:
        if parent == root.parent:
            break
        if parent.is_symlink():
            raise ValueError("Symlinks are not supported")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Path escapes project root")
    return path


def hashes(root: Path, files: list[str]) -> dict[str, str]:
    return {
        name: hashlib.sha256(safe_path(root, name).read_bytes()).hexdigest()
        for name in sorted(files)
    }


def copy_project(root: Path, destination: Path, files: list[str]) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for name in files:
        source = safe_path(root, name)
        if source.stat().st_size > 1_000_000:
            raise ValueError("Project file exceeds 1 MB limit")
        target = safe_path(destination, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
