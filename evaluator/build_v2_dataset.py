#!/usr/bin/env python3
"""Derive V2 fixtures without changing the frozen V1 benchmark."""

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGRESSION_SWITCH = re.compile(
    r'^\s*if\s*\(\s*\$test\$plusargs\("REGRESSION"\)\s*\)\s*cycles\s*=\s*(\d+)\s*;\s*$',
    re.MULTILINE,
)
PASS_MARKER = '    $display("SEMIDEBUG_PASS"); $finish;'

# These sequences run only in the evaluator copy. The random run is also longer
# and receives seeds 17/103, while the visible target keeps its shorter seed 7.
HIDDEN_VECTORS = {
    "counter": """    rst=1; en=0; step; rst=0; en=1;
    for(i=0;i<35;i=i+1) step;
    en=0; for(i=0;i<5;i=i+1) step;
""",
    "fifo": """    rst=1; wr_en=0; rd_en=0; step; rst=0;
    for(i=0;i<16;i=i+1) begin
        wr_en=1; rd_en=0; data_in=i; step;
        wr_en=0; rd_en=1; step;
    end
""",
    "arbiter": """    rst=1; req=0; step; rst=0;
    for(i=0;i<24;i=i+1) begin
        req=3; step; req=1; step; req=2; step;
    end
""",
    "controller": """    rst=1; start=1; finish=1; step; rst=0;
    for(i=0;i<20;i=i+1) begin
        start=1; finish=1; step;
        start=0; finish=1; step;
        start=0; finish=0; step;
    end
""",
    "alu": """    for(i=0;i<8;i=i+1) begin
        a=(i%2) ? 8'h80 : 8'h7f; b=8'hff-i;
        for(j=0;j<8;j=j+1) begin op=j; check; end
    end
""",
    "pulse": """    rst=1; signal_in=0; enable=0; step; rst=0;
    for(i=0;i<20;i=i+1) begin
        signal_in=1; enable=1; step;
        enable=0; step; signal_in=0; step;
    end
""",
}


def transform_case(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".yosys_history", ".build", "*.vvp"),
    )
    manifest_path = destination / "case.json"
    case = json.loads(manifest_path.read_text())
    visible = case["target"]["sources"]
    if len(visible) != 1 or any(test["sources"] != visible for test in case["regression"]):
        raise ValueError(f"Unexpected V1 testbench layout: {source}")
    visible_path = destination / visible[0]
    original = visible_path.read_text()
    visible_text, count = REGRESSION_SWITCH.subn("", original)
    if count != 1:
        raise ValueError(f"Missing unique regression switch: {source}")
    visible_path.write_text(visible_text)

    top = case["target"]["top"]
    design = case["design_top"]
    if not top.endswith("_tb") or design not in HIDDEN_VECTORS:
        raise ValueError(f"Unexpected testbench top or design: {source}")
    hidden_top = top.removesuffix("_tb") + "_hidden_tb"
    hidden_name = visible[0].removesuffix(".v") + "_hidden.v"
    hidden_text, count = REGRESSION_SWITCH.subn(lambda m: f"    cycles={m.group(1)};", original)
    if count != 1:
        raise ValueError(f"Missing hidden regression switch: {source}")
    hidden_text = hidden_text.replace(f"module {top};", f"module {hidden_top};", 1)
    if hidden_text == original or hidden_text.count(PASS_MARKER) != 1:
        raise ValueError(f"Unexpected testbench structure: {source}")
    hidden_text = hidden_text.replace(PASS_MARKER, HIDDEN_VECTORS[design] + PASS_MARKER)
    (destination / hidden_name).write_text(hidden_text)

    case["immutable"].append(hidden_name)
    for test in case["regression"]:
        test["top"] = hidden_top
        test["sources"] = [hidden_name]
        test["plusargs"] = [arg for arg in test["plusargs"] if arg != "+REGRESSION"]
    manifest_path.write_text(json.dumps(case, indent=2) + "\n")


def build(source_root: Path, output_root: Path) -> int:
    if output_root.exists():
        raise ValueError(f"Output already exists: {output_root}")
    manifests = sorted(source_root.glob("*/case_*/case.json"))
    if len(manifests) != 30:
        raise ValueError(f"Expected 30 V1 cases, found {len(manifests)}")
    count = 0
    for manifest in manifests:
        relative = manifest.parent.relative_to(source_root)
        transform_case(manifest.parent, output_root / relative)
        count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "benchmark")
    parser.add_argument("--output", type=Path, default=ROOT / "benchmark_v2")
    args = parser.parse_args()
    count = build(args.source, args.output)
    print(f"Generated {count} V2 cases under {args.output}")


if __name__ == "__main__":
    main()
