"""Small strict unified-diff parser: no fuzzy offsets, rename, create or delete."""

import re
from dataclasses import dataclass


class PatchError(ValueError):
    pass


@dataclass
class Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[str]


@dataclass
class FilePatch:
    path: str
    hunks: list[Hunk]


HEADER = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?:.*)$")


def parse_diff(diff: str) -> list[FilePatch]:
    if len(diff) > 50000 or not diff.endswith("\n"):
        raise PatchError("Diff must be <= 50 KB and end with newline")
    lines = diff.splitlines(keepends=True)
    patches = []
    index = 0
    while index < len(lines):
        if lines[index].startswith("diff --git "):
            index += 1
            if index < len(lines) and lines[index].startswith("index "):
                index += 1
        if (
            index + 1 >= len(lines)
            or not lines[index].startswith("--- a/")
            or not lines[index + 1].startswith("+++ b/")
        ):
            raise PatchError("Expected --- a/path and +++ b/path")
        old = lines[index][6:].rstrip("\n")
        new = lines[index + 1][6:].rstrip("\n")
        if old != new or old in {p.path for p in patches}:
            raise PatchError("Renames and duplicate file sections forbidden")
        index += 2
        hunks = []
        while index < len(lines) and lines[index].startswith("@@"):
            match = HEADER.fullmatch(lines[index].rstrip("\n"))
            if not match:
                raise PatchError("Malformed hunk header")
            a, b, c, d = match.groups()
            hunk = Hunk(int(a), int(b or 1), int(c), int(d or 1), [])
            index += 1
            old_count = new_count = 0
            while old_count < hunk.old_count or new_count < hunk.new_count:
                if index >= len(lines) or lines[index][0] not in " +-":
                    raise PatchError("Hunk truncated or invalid")
                line = lines[index]
                hunk.lines.append(line)
                old_count += line[0] in " -"
                new_count += line[0] in " +"
                index += 1
                if old_count > hunk.old_count or new_count > hunk.new_count:
                    raise PatchError("Hunk count mismatch")
            hunks.append(hunk)
        if not hunks:
            raise PatchError("File patch has no hunks")
        patches.append(FilePatch(old, hunks))
    if not patches:
        raise PatchError("Empty diff")
    return patches
