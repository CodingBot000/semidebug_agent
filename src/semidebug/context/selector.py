import re
from pathlib import Path

from semidebug.models import Case, EvidenceItem, ValidationBundle
from semidebug.tools.workspace import safe_path


def evidence_from(bundle: ValidationBundle, prefix: str) -> list[EvidenceItem]:
    return [
        EvidenceItem(
            id=f"{prefix}:{name}",
            tool=r.tool,
            status=r.status,
            message=(r.stdout + "\n" + r.stderr)[-8000:],
        )
        for name, r in bundle.results.items()
    ]


def select_context(
    root: Path, case: Case, evidence: list[EvidenceItem], limit: int = 40000
) -> dict:
    # No directory walk: only manifest mutable RTL and immutable testbench sources are eligible.
    logs = "\n".join(e.message for e in evidence)
    sources = {}
    files = list(case.mutable) + list(
        dict.fromkeys(s for t in [case.target, *case.regression] for s in t.sources)
    )
    files.sort(key=lambda name: (name not in logs, name not in case.mutable))
    remaining = limit
    for name in files:
        if remaining <= 0:
            break
        lines = safe_path(root, name).read_text().splitlines()
        numbered = "\n".join(f"{i}: {line}" for i, line in enumerate(lines, 1))
        if len(numbered) > min(remaining, 14000):
            match = re.search(re.escape(name) + r":(\d+)", logs)
            center = int(match.group(1)) - 1 if match else 0
            begin = max(0, center - 40)
            numbered = "\n".join(
                f"{i + 1}: {lines[i]}" for i in range(begin, min(len(lines), begin + 100))
            )
        sources[name] = numbered[:remaining]
        remaining -= len(sources[name])
    return {
        "mutable": case.mutable,
        "immutable": case.immutable,
        "sources_with_line_numbers": sources,
        "evidence": [e.model_dump() for e in evidence],
    }
