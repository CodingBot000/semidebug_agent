#!/usr/bin/env python3
"""Import only frozen ChipBench cases into a local, untracked evaluator workspace."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_BLOCK = re.compile(r"```(?:verilog|systemverilog)?\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
SMOKE = 'module smoke_tb; initial begin $display("SEMIDEBUG_PASS"); $finish; end endmodule\n'


def import_cases(checkout: Path, manifest_path: Path, output: Path) -> list[Path]:
    manifest = json.loads(manifest_path.read_text())
    revision = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    if revision != manifest["commit"]:
        raise ValueError(f"ChipBench revision mismatch: {revision}")
    if output.exists():
        raise ValueError(f"Output already exists: {output}")
    result = []
    for row in manifest["selected"]:
        files = {}
        for kind, record in row["files"].items():
            path = checkout / record["path"]
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != record["sha256"]:
                raise ValueError(f"Selected {kind} hash mismatch: {row['case_id']}")
            files[kind] = data
        prompt = files["prompt"].decode()
        blocks = CODE_BLOCK.findall(prompt)
        if len(blocks) != 1 or len(re.findall(r"\bmodule\s+TopModule\b", blocks[0])) != 1:
            raise ValueError(f"Cannot extract one buggy TopModule: {row['case_id']}")
        case_root = output / row["case_id"]
        (case_root / "rtl").mkdir(parents=True)
        (case_root / "tb").mkdir()
        (case_root / "rtl/TopModule.sv").write_text(blocks[0].strip() + "\n")
        (case_root / "problem.txt").write_text(prompt[: prompt.index("```")].strip() + "\n")
        (case_root / "tb/ref.sv").write_bytes(files["ref"])
        (case_root / "tb/test.sv").write_bytes(files["test"])
        (case_root / "tb/smoke.sv").write_text(SMOKE)
        (case_root / "upstream.json").write_text(
            json.dumps({"commit": revision, "selected": row}, indent=2) + "\n"
        )
        case = {
            "id": "chipbench_" + row["case_id"],
            "category": row["category"],
            "design_top": "TopModule",
            "mutable": ["rtl/TopModule.sv"],
            "immutable": [
                "problem.txt",
                "tb/ref.sv",
                "tb/test.sv",
                "tb/smoke.sv",
                "upstream.json",
            ],
            "prompt_visible": ["rtl/TopModule.sv", "problem.txt"],
            "target": {
                "name": "target",
                "top": "smoke_tb",
                "sources": ["tb/smoke.sv"],
            },
            "regression": [
                {
                    "name": "official",
                    "top": "tb",
                    "sources": ["tb/ref.sv", "tb/test.sv"],
                    "success_mode": "chipbench_mismatches",
                }
            ],
            "timeout_sec": 30,
        }
        (case_root / "case.json").write_text(json.dumps(case, indent=2) + "\n")
        result.append(case_root)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument(
        "--manifest", type=Path, default=ROOT / "external/chipbench/selection_manifest.json"
    )
    parser.add_argument("--output", type=Path, default=ROOT / "external/chipbench/cases")
    args = parser.parse_args()
    cases = import_cases(args.checkout, args.manifest, args.output)
    print(f"Imported {len(cases)} pinned cases under {args.output}")


if __name__ == "__main__":
    main()
