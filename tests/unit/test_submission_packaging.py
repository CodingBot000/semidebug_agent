import importlib.util
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "package_submission", ROOT / "scripts/package_submission.py"
)
package_submission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package_submission)


def test_final_selection_excludes_historical_submission_material():
    configured = {
        *package_submission.TOP_FILES,
        *package_submission.DOC_FILES,
        *package_submission.RESULT_FILES,
    }
    assert "VERIFICATION_REPORT.md" in configured
    assert "benchmark" not in package_submission.TREES
    assert not any(name.startswith("results/v2/") for name in configured)


def test_package_rejects_missing_link_local_path_and_secret(tmp_path):
    source = tmp_path / "README.md"
    source.write_text("[missing](missing.md)\n")
    with pytest.raises(ValueError, match="Broken relative"):
        package_submission.verify({"README.md": source})

    source.write_text("Local workspace: /" + "Users/example/project\n")
    with pytest.raises(ValueError, match="Local absolute path"):
        package_submission.verify({"README.md": source})

    source.write_text("sk-" + "a" * 30)
    with pytest.raises(ValueError, match="Potential secret"):
        package_submission.verify({"README.md": source})


def test_package_scan_rejects_external_reference(tmp_path):
    archive = tmp_path / "submission.zip"
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
    with zipfile.ZipFile(archive, "w") as stream:
        for name in required:
            stream.writestr(f"{package_submission.PREFIX}/{name}", "ok")
        stream.writestr(f"{package_submission.PREFIX}/external/chipbench/cases/item_ref.sv", "ref")
    with pytest.raises(ValueError, match="Forbidden"):
        package_submission.scan_archive(archive)


def test_package_scan_rejects_legacy_benchmark_tree(tmp_path):
    archive = tmp_path / "submission.zip"
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
    with zipfile.ZipFile(archive, "w") as stream:
        for name in required:
            stream.writestr(f"{package_submission.PREFIX}/{name}", "ok")
        stream.writestr(f"{package_submission.PREFIX}/benchmark/old/case.json", "history")
    with pytest.raises(ValueError, match="Forbidden"):
        package_submission.scan_archive(archive)
