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
        pack.scan(secret, "test.txt")
    assert secret.decode() not in str(error.value)


def test_whitelist_excludes_credentials_cache_and_outside(tmp_path):
    (tmp_path / "src").mkdir()
    for name in ["src/ok.py", "src/.env", "src/.env.production", "private.txt", "README.md"]:
        (tmp_path / name).write_text("x")
    (tmp_path / "src/__pycache__").mkdir()
    (tmp_path / "src/__pycache__/x.pyc").write_bytes(b"x")
    assert {str(r) for _, r in pack.candidates(tmp_path)} == {"src/ok.py", "README.md"}
