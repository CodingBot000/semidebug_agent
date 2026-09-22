import re
from pathlib import Path

from semidebug.models import Case
from semidebug.patch.parser import FilePatch, PatchError, parse_diff
from semidebug.tools.workspace import safe_path

SENSITIVE = re.compile(
    r"\b(assert|assume|cover|force|release|bind|disable|initial|import|export)\b|`|\$|translate_off|lint_off",
    re.I,
)
ALLOWED_FUNCTIONS = re.compile(r"\$(signed|unsigned|clog2|bits)\b")


def guard_patch(diff: str, root: Path, case: Case) -> list[FilePatch]:
    patches = parse_diff(diff)
    if len(patches) > 2:
        raise PatchError("More than two files changed")
    changed = 0
    for patch in patches:
        if patch.path not in case.mutable or patch.path in case.immutable:
            raise PatchError("Only manifest mutable RTL may change")
        try:
            path = safe_path(root, patch.path)
        except ValueError as exc:
            raise PatchError(str(exc)) from exc
        if not path.is_file():
            raise PatchError("New files are forbidden")
        for hunk in patch.hunks:
            for line in hunk.lines:
                if line[0] in "+-":
                    changed += 1
                    if SENSITIVE.search(ALLOWED_FUNCTIONS.sub("", line[1:])) or re.search(
                        r"\b[A-Za-z_]\w*\s*\.\s*[A-Za-z_]\w*", line[1:]
                    ):
                        raise PatchError(
                            "Verification bypass, directive or dependency-sensitive change"
                        )
    if not 0 < changed <= 40:
        raise PatchError("Expected 1..40 changed lines")
    return patches
