#!/usr/bin/env python3
"""Freeze a reproducible 12-case ChipBench selection before any model calls."""

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

UPSTREAM = "https://github.com/zhongkaiyu/ChipBench.git"
REVISION = "b4ba3a06759804ec88c26c3cf15b28b9a90b3443"
CATEGORIES = ("timing", "assignment", "arithmetic", "state_machine")
ROOT = Path(__file__).resolve().parents[1]


def freeze(checkout: Path) -> dict:
    commit = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    if commit != REVISION:
        raise ValueError(f"Expected pinned ChipBench revision {REVISION}, got {commit}")
    dataset = checkout / "Verilog Debugging"
    selected = []
    for category in CATEGORIES:
        directory = dataset / f"dataset_debug_zero_shot_{category}"
        prompts = sorted(directory.glob("*_prompt.txt"), key=lambda path: path.name)
        if len(prompts) < 3:
            raise ValueError(f"Too few {category} prompts")
        for prompt in prompts[:3]:
            base = prompt.name.removesuffix("_prompt.txt")
            files = {
                kind: directory / f"{base}_{kind}.{suffix}"
                for kind, suffix in (("prompt", "txt"), ("ref", "sv"), ("test", "sv"))
            }
            if any(not path.is_file() for path in files.values()):
                raise ValueError(f"Incomplete selected triplet: {base}")
            selected.append(
                {
                    "category": category,
                    "case_id": f"{category}_{base}",
                    "files": {
                        kind: {
                            "path": path.relative_to(checkout).as_posix(),
                            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        }
                        for kind, path in files.items()
                    },
                }
            )
    return {
        "benchmark": "ChipBench Verilog Debugging zero-shot",
        "upstream": UPSTREAM,
        "commit": REVISION,
        "license": "MIT; retain upstream license if redistributing files",
        "selected_at_utc": datetime.now(timezone.utc).isoformat(),
        "selection_rule": "For each timing, assignment, arithmetic and state_machine zero-shot directory, take the first three *_prompt.txt filenames in bytewise lexicographic order. Require matching *_ref.sv and *_test.sv; abort if any selected triplet is incomplete. No result-based substitution or post-selection exclusion.",
        "selected_count": len(selected),
        "selected": selected,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "external/chipbench/selection_manifest.json"
    )
    args = parser.parse_args()
    manifest = freeze(args.checkout)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Frozen {manifest['selected_count']} cases at {manifest['commit']}")


if __name__ == "__main__":
    main()
