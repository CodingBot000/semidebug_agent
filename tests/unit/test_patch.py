import difflib
import shutil

import pytest

from semidebug.benchmark.loader import load_case
from semidebug.patch.apply import apply_patches
from semidebug.patch.guard import guard_patch
from semidebug.patch.parser import PatchError, parse_diff
from semidebug.tools.workspace import safe_path


def test_patch_exact_apply_and_original_preserved(counter, tmp_path, make_responses):
    work = tmp_path / "project"
    shutil.copytree(counter, work)
    case = load_case(work)
    original = (counter / case.mutable[0]).read_bytes()
    diff = make_responses(work)[1]["unified_diff"]
    apply_patches(work, guard_patch(diff, work, case))
    assert (work / case.mutable[0]).read_bytes() != original
    assert (counter / case.mutable[0]).read_bytes() == original
    with pytest.raises(PatchError, match="context mismatch"):
        apply_patches(work, parse_diff(diff))


@pytest.mark.parametrize(
    "path",
    [
        "../outside.v",
        "/tmp/out.v",
        "rtl/../../x",
        "rtl/a;exec.v",
        "rtl/a b.v",
        "rtl//a.v",
        "rtl/./a.v",
        "-rtl/a.v",
        "rtl/-a.v",
    ],
)
def test_path_rejection(tmp_path, path):
    with pytest.raises(ValueError):
        safe_path(tmp_path, path)


def test_symlink_rejection(tmp_path):
    outside = tmp_path / "outside"
    outside.write_text("x")
    root = tmp_path / "root"
    root.mkdir()
    (root / "rtl").symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(ValueError):
        safe_path(root, "rtl/outside")


@pytest.mark.parametrize(
    "path", ["tb/counter_tb.v", "expected/metadata.json", "case.json", "../other.v"]
)
def test_immutable_rejected(counter, make_responses, path):
    diff = make_responses(counter)[1]["unified_diff"].replace("rtl/counter.v", path)
    with pytest.raises(PatchError):
        guard_patch(diff, counter, load_case(counter))


@pytest.mark.parametrize(
    "line",
    [
        "initial $finish;",
        '`include "external.v"',
        "force dut.count=0;",
        "// verilator lint_off WIDTH",
        "assert (1);",
        '$system("touch x");',
    ],
)
def test_bypass_rejected(counter, line):
    original = (counter / "rtl/counter.v").read_text()
    diff = "".join(
        difflib.unified_diff(
            original.splitlines(True),
            (original + line + "\n").splitlines(True),
            fromfile="a/rtl/counter.v",
            tofile="b/rtl/counter.v",
        )
    )
    with pytest.raises(PatchError):
        guard_patch(diff, counter, load_case(counter))


def test_hunk_lies_and_oversize(counter, make_responses):
    diff = make_responses(counter)[1]["unified_diff"]
    with pytest.raises(PatchError):
        parse_diff(diff[:-1])
    with pytest.raises(PatchError):
        parse_diff("garbage\n")
    big = "".join(
        difflib.unified_diff(
            (counter / "rtl/counter.v").read_text().splitlines(True),
            ["wire x;\n"] * 60,
            fromfile="a/rtl/counter.v",
            tofile="b/rtl/counter.v",
        )
    )
    with pytest.raises(PatchError, match="changed lines"):
        guard_patch(big, counter, load_case(counter))


def test_addition_and_multiple_hunks(tmp_path):
    (tmp_path / "a.v").write_text("a\nb\nc\nd\ne\nf\ng\nh\n")
    new = "z\na\nb\nc\nd\ne\nf\ng\nh\ni\n"
    diff = "".join(
        difflib.unified_diff(
            (tmp_path / "a.v").read_text().splitlines(True),
            new.splitlines(True),
            fromfile="a/a.v",
            tofile="b/a.v",
            n=0,
        )
    )
    apply_patches(tmp_path, parse_diff(diff))
    assert (tmp_path / "a.v").read_text() == new
