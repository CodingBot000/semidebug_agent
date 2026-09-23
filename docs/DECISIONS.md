# Architecture decisions

1. Canonical runtime: Python 3.12 in Debian bookworm Docker; native Python >=3.11 supported. Pin the resolved image digest/tool versions after building. Debian EDA packages favor reproducibility over newest upstream releases.
2. Package manager: uv, committed uv.lock. argparse CLI, Pydantic models, httpx provider, pytest/ruff development tools.
3. Primary simulation: Icarus compile + VVP. Independent lint: Verilator. Structural synthesis sanity: Yosys.
4. Orchestrator: explicit states with append-only JSONL trace; each proposal applies to a fresh copy of baseline, not cumulatively. Failed candidates never alter user sources.
5. Patches: strict unified diff, existing mutable RTL only, no fuzzy application, max 2 files/40 changed lines. Immutable hashes verified around every tool stage and before success.
6. Dataset: six original design families, 30 mutations, 24 public/6 holdout. Gold sources and mutation definitions stay in evaluator/ and are excluded from prompts/workspaces.
7. No API credentials: record live benchmark as unavailable. Scripted E2E tests and dataset integrity checks are real EDA executions, explicitly not measurements of AI repair ability.
8. Default remote: private GitHub repository CodingBot000/semidebug_agent, per the approved plan.
9. Native runtime supports trusted projects only. Docker offline execution is recommended; adversarial HDL needs a dedicated disposable VM/container boundary beyond lexical patch guards.

## 2026-09-23 — Local Codex inference

Use official host Codex CLI ChatGPT authentication at the user’s request. One structured call returns diagnosis and patch per attempt. A short dedicated instruction file and successful-log compaction reduced input tokens from 16,854 to 6,520 in one FIFO pilot; both proposals passed independent verification. Use the optimized prompt unchanged for the 24 public and 6 holdout cases. Record subscription usage as tokens with null API cost; do not equate this pilot with a general repair-quality improvement. EDA remains in credential-free, network-disabled Docker containers.
