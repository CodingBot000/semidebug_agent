from pathlib import Path

from semidebug.patch.parser import FilePatch, PatchError
from semidebug.tools.workspace import safe_path


def apply_patches(root: Path, patches: list[FilePatch]) -> None:
    prepared = {}
    for patch in patches:
        path = safe_path(root, patch.path)
        lines = path.read_text().splitlines(keepends=True)
        output = []
        cursor = 0
        for hunk in patch.hunks:
            start = hunk.old_start - (1 if hunk.old_count else 0)
            if start < cursor or start > len(lines):
                raise PatchError("Overlapping or out-of-range hunk")
            output.extend(lines[cursor:start])
            expected_new_start = len(output) + (1 if hunk.new_count else 0)
            if expected_new_start != hunk.new_start:
                raise PatchError("New hunk position mismatch")
            cursor = start
            for line in hunk.lines:
                if line[0] in " -":
                    if cursor >= len(lines) or lines[cursor] != line[1:]:
                        raise PatchError("Exact baseline context mismatch; fuzzy apply forbidden")
                    cursor += 1
                if line[0] in " +":
                    output.append(line[1:])
        output.extend(lines[cursor:])
        content = "".join(output)
        if content == "".join(lines):
            raise PatchError("No-op patch")
        prepared[path] = content
    # Compute all contents before writing anything, making validation failures atomic.
    for path, content in prepared.items():
        path.write_text(content)
