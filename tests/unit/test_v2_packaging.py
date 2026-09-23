import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "package_v2_submission", ROOT / "scripts/package_v2_submission.py"
)
package_v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package_v2)


def test_v2_package_rejects_missing_link_local_path_and_secret(tmp_path):
    source = tmp_path / "README.md"
    source.write_text("[missing](missing.md)\n")
    with pytest.raises(ValueError, match="Broken relative"):
        package_v2.verify({"README.md": source})

    source.write_text("Local workspace: /" + "Users/example/project\n")
    with pytest.raises(ValueError, match="Local absolute path"):
        package_v2.verify({"README.md": source})

    source.write_text("sk-" + "a" * 30)
    with pytest.raises(ValueError, match="Potential secret"):
        package_v2.verify({"README.md": source})
