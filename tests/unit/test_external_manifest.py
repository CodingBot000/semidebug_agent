import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from semidebug.benchmark.loader import load_case
from semidebug.context.selector import select_context

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "import_chipbench", ROOT / "scripts/import_chipbench.py"
)
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)


def fixture(tmp_path):
    checkout = tmp_path / "upstream"
    directory = checkout / "Verilog Debugging/dataset_debug_zero_shot_timing"
    directory.mkdir(parents=True)
    content = {
        "prompt": b"Repair the stated behavior.\n```\nmodule TopModule; endmodule\n```\n",
        "ref": b"module RefModule; endmodule\n",
        "test": b"module tb; endmodule\n",
    }
    files = {}
    for kind, data in content.items():
        suffix = "txt" if kind == "prompt" else "sv"
        path = directory / f"Prob001_{kind}.{suffix}"
        path.write_bytes(data)
        files[kind] = {
            "path": path.relative_to(checkout).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    manifest = tmp_path / "selection.json"
    manifest.write_text(
        json.dumps(
            {
                "commit": "pinned",
                "selected": [{"category": "timing", "case_id": "timing_Prob001", "files": files}],
            }
        )
    )
    return checkout, manifest, directory


def test_import_preserves_private_reference_and_hashes(tmp_path, monkeypatch):
    checkout, manifest, directory = fixture(tmp_path)
    monkeypatch.setattr(importer.subprocess, "check_output", lambda *args, **kwargs: "pinned\n")
    output = tmp_path / "cases"
    assert len(importer.import_cases(checkout, manifest, output)) == 1
    case = json.loads((output / "timing_Prob001/case.json").read_text())
    assert case["prompt_visible"] == ["rtl/TopModule.sv", "problem.txt"]
    assert "RefModule" not in (output / "timing_Prob001/problem.txt").read_text()
    assert (output / "timing_Prob001/tb/ref.sv").read_bytes() == b"module RefModule; endmodule\n"
    loaded = load_case(output / "timing_Prob001")
    request = json.dumps(select_context(output / "timing_Prob001", loaded, []))
    assert "RefModule" not in request and "tb/ref.sv" not in request

    case["prompt_visible"].append("tb/ref.sv")
    (output / "timing_Prob001/case.json").write_text(json.dumps(case))
    with pytest.raises(ValueError, match="evaluator-only"):
        load_case(output / "timing_Prob001")

    (directory / "Prob001_ref.sv").write_text("tampered")
    with pytest.raises(ValueError, match="hash mismatch"):
        importer.import_cases(checkout, manifest, tmp_path / "second")
