"""Internal JSON worker invoked inside the credential-free EDA image."""

import sys
from pathlib import Path

from semidebug.benchmark.loader import load_case
from semidebug.tools.validation import regress, validate


def main():
    root = Path.cwd()
    case = load_case(root)
    mode = sys.argv[1]
    if mode not in {"target", "regression"}:
        raise SystemExit("Invalid EDA mode")
    result = (regress if mode == "regression" else validate)(root, case)
    print(result.model_dump_json())


if __name__ == "__main__":
    main()
