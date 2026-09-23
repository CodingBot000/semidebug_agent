import re
from pathlib import Path

from semidebug.models import Case, TestSpec, ValidationBundle
from semidebug.tools.process import run_process

CRITICAL_WARNINGS = {
    "WIDTH",
    "WIDTHTRUNC",
    "WIDTHEXPAND",
    "LATCH",
    "MULTIDRIVEN",
    "UNDRIVEN",
    "PINMISSING",
    "IMPLICIT",
    "CASEINCOMPLETE",
    "UNOPTFLAT",
}


def simulate(root: Path, case: Case, test: TestSpec) -> ValidationBundle:
    build = root / ".build"
    build.mkdir(exist_ok=True)
    output = f".build/{test.name}.vvp"
    compile_result = run_process(
        ["iverilog", "-g2012", "-Wall", "-s", test.top, "-o", output, *case.mutable, *test.sources],
        root,
        case.timeout_sec,
        "iverilog",
    )
    results = {"compile": compile_result}
    if compile_result.status == "pass":
        sim = run_process(["vvp", "-N", output, *test.plusargs], root, case.timeout_sec, "vvp")
        if sim.status == "pass" and test.success_mode == "semidebug_pass":
            if "SEMIDEBUG_PASS" not in sim.stdout.splitlines():
                sim.status = "fail"
                sim.stderr += "\nMissing trusted testbench completion marker."
        if sim.status == "pass" and test.success_mode == "chipbench_mismatches":
            matches = re.findall(r"^Mismatches: (\d+) in (\d+) samples$", sim.stdout, re.MULTILINE)
            if (
                len(matches) != 1
                or int(matches[0][0]) != 0
                or int(matches[0][1]) <= 0
                or "TIMEOUT" in sim.stdout
            ):
                sim.status = "fail"
                sim.stderr += "\nChipBench official mismatch result did not pass."
        results["simulation"] = sim
    return ValidationBundle(results=results)


def validate(root: Path, case: Case) -> ValidationBundle:
    bundle = simulate(root, case, case.target)
    lint = run_process(
        [
            "verilator",
            "--lint-only",
            "-Wall",
            "-Wno-fatal",
            "--top-module",
            case.design_top,
            *case.mutable,
        ],
        root,
        case.timeout_sec,
        "verilator",
    )
    warning_codes = set(re.findall(r"%Warning-([A-Z0-9_]+):", lint.stderr + lint.stdout))
    if lint.status == "pass" and warning_codes & CRITICAL_WARNINGS:
        lint.status = "fail"
        lint.stderr += "\nCritical lint policy: " + ", ".join(
            sorted(warning_codes & CRITICAL_WARNINGS)
        )
    bundle.results["lint"] = lint
    # Manifest path validation prevents Yosys command/script injection.
    script = (
        "read_verilog -sv "
        + " ".join(case.mutable)
        + "; hierarchy -check -top "
        + case.design_top
        + "; proc; opt; check -assert"
    )
    bundle.results["synthesis"] = run_process(
        ["yosys", "-Q", "-T", "-p", script], root, case.timeout_sec, "yosys"
    )
    return bundle


def regress(root: Path, case: Case) -> ValidationBundle:
    result = ValidationBundle()
    for test in case.regression:
        bundle = simulate(root, case, test)
        result.results.update({f"{test.name}.{name}": r for name, r in bundle.results.items()})
    return result
