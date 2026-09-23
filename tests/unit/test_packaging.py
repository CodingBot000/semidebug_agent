import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "package_submission", ROOT / "scripts/package_submission.py"
)
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


def test_secret_detected_without_value_echo():
    secret = ("sk-" + "a" * 30).encode()
    with pytest.raises(ValueError) as error:
        pack.verify_bytes({"test.txt": secret})
    assert secret.decode() not in str(error.value)


def test_selection_excludes_env_files_and_caches(tmp_path, monkeypatch):
    monkeypatch.setattr(pack, "TOP_FILES", ("README.md", ".env.example"))
    monkeypatch.setattr(pack, "DOC_FILES", ())
    monkeypatch.setattr(pack, "RESULT_FILES", ())
    monkeypatch.setattr(pack, "TREES", ("src",))
    monkeypatch.setattr(pack, "EXCLUDED_TREES", set())
    (tmp_path / "docs").mkdir()
    (tmp_path / "src").mkdir()
    for name in [
        "src/ok.py",
        "src/.env",
        "src/.env.production",
        "private.txt",
        "README.md",
        ".env.example",
        "PORTFOLIO_EVIDENCE.md",
        "docs/ARCHITECTURE.md",
        "docs/architecture.mmd",
        "SUBMISSION_GUIDE.md",
        "docs/SECURITY.md",
    ]:
        (tmp_path / name).write_text("x")
    (tmp_path / "src/__pycache__").mkdir()
    (tmp_path / "src/__pycache__/x.pyc").write_bytes(b"x")
    for condition in (
        "full_loop_public",
        "full_loop_hidden",
        "single_shot_public",
        "single_shot_hidden",
    ):
        directory = tmp_path / "results/final/internal" / condition
        directory.mkdir(parents=True, exist_ok=True)
        for name in ("summary.json", "summary.md", "results.json", "results.csv"):
            (directory / name).write_text("x")
    (tmp_path / "results/final/evidence").mkdir(parents=True)
    selected = pack.entries(tmp_path)
    assert "src/ok.py" in selected
    assert "src/.env" not in selected and "src/.env.production" not in selected
    assert ".env.example" in selected and ".git" not in selected
    assert all("__pycache__" not in name for name in selected)
