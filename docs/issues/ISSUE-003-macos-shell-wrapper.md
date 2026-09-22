# ISSUE-003 — macOS Bash empty-array failure

- Discovered: 2026-09-22 UTC during demo/reproduction checks.
- Status: Resolved.
- Symptom: `scripts/docker_run.sh: credentials[@]: unbound variable` prevented the demo and final suite from starting.
- Reproduction: `./scripts/run_demo.sh --scripted` on the system Bash 3.2 with `set -u`.
- Cause: Bash 3.2 treats expansion of an empty array as unbound under nounset.
- Impact: shell entry points failed before Docker invocation; direct Docker EDA tests already passed.
- Resolution: use one always-nonempty options array and append optional credentials/network flags. Also propagate explicitly exported provider settings for live mode.
- Verification: rerun scripted demo and complete suite using the corrected wrapper; results in PROGRESS.md.
