import pytest

from semidebug.models import Case
from semidebug.models import TestSpec as CaseTestSpec
from semidebug.tools.validation import simulate

pytestmark = pytest.mark.integration


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        ("Mismatches: 0 in 5 samples", "pass"),
        ("Mismatches: 2 in 5 samples", "fail"),
        ("Mismatches: 0 in 0 samples", "fail"),
        ("TIMEOUT\nMismatches: 0 in 5 samples", "fail"),
    ],
)
def test_official_mismatch_result_is_checked(tmp_path, output, expected):
    (tmp_path / "rtl").mkdir()
    (tmp_path / "tb").mkdir()
    (tmp_path / "rtl/TopModule.sv").write_text("module TopModule; endmodule\n")
    escaped = output.replace("\n", "\\n")
    (tmp_path / "tb/test.sv").write_text(
        f'module tb; initial begin $display("{escaped}"); $finish; end endmodule\n'
    )
    official = CaseTestSpec(
        name="official",
        top="tb",
        sources=["tb/test.sv"],
        success_mode="chipbench_mismatches",
    )
    case = Case(
        id="chipbench_sample",
        category="test",
        design_top="TopModule",
        mutable=["rtl/TopModule.sv"],
        immutable=["tb/test.sv"],
        target=official,
        regression=[official.model_copy(update={"name": "regression"})],
    )
    assert simulate(tmp_path, case, official).results["simulation"].status == expected
