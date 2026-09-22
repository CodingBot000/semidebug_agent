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
