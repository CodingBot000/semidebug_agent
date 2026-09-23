from pathlib import Path

from semidebug.models import Case
from semidebug.tools.workspace import safe_path


def load_case(root: Path) -> Case:
    root = root.resolve()
    manifest = safe_path(root, "case.json")
    if manifest.stat().st_size > 100000:
        raise ValueError("Case manifest too large")
    case = Case.model_validate_json(manifest.read_text())
    mutable = set(case.mutable)
    immutable = set(case.immutable)
    if len(mutable) != len(case.mutable) or len(immutable) != len(case.immutable):
        raise ValueError("Duplicate manifest paths")
    if mutable & immutable or "case.json" in mutable:
        raise ValueError("Mutable/immutable paths overlap")
    for name in mutable:
        if not name.startswith("rtl/") or not name.endswith((".v", ".sv")):
            raise ValueError("Only explicit rtl/*.v or rtl/*.sv files can be mutable")
    for name in mutable | immutable:
        p = safe_path(root, name)
        if not p.is_file() or p.stat().st_size > 1_000_000:
            raise ValueError(f"Missing/oversize source: {name}")
    if case.prompt_visible is not None:
        visible = set(case.prompt_visible)
        hidden_regression = {source for test in case.regression for source in test.sources} - set(
            case.target.sources
        )
        if not visible or not visible <= mutable | immutable or visible & hidden_regression:
            raise ValueError("Prompt visibility includes missing or evaluator-only files")
        if not mutable <= visible:
            raise ValueError("Prompt visibility must include mutable RTL")
    names = [t.name for t in [case.target, *case.regression]]
    if len(names) != len(set(names)):
        raise ValueError("Test names must be unique")
    for test in [case.target, *case.regression]:
        if not set(test.sources) <= immutable or not all(
            s.endswith((".v", ".sv")) for s in test.sources
        ):
            raise ValueError("Every testbench must be immutable HDL")
        if any(
            not a.startswith("+") or len(a) > 100 or any(c.isspace() for c in a)
            for a in test.plusargs
        ):
            raise ValueError("Only bounded simulation plusargs are supported")
    return case
