# Architecture decisions

1. Canonical runtime: Python 3.12 in Debian bookworm Docker; native Python >=3.11 supported. Pin the resolved image digest/tool versions after building. Debian EDA packages favor reproducibility over newest upstream releases.
2. Package manager: uv, committed uv.lock. argparse CLI, Pydantic models, httpx provider, pytest/ruff development tools.
3. Primary simulation: Icarus compile + VVP. Independent lint: Verilator. Structural synthesis sanity: Yosys.
4. Orchestrator: explicit states with append-only JSONL trace; each proposal applies to a fresh copy of baseline, not cumulatively. Failed candidates never alter user sources.
5. Patches: strict unified diff, existing mutable RTL only, no fuzzy application, max 2 files/40 changed lines. Immutable hashes verified around every tool stage and before success.
6. Dataset: six original design families, 30 mutations, 24 public/6 holdout. Gold sources and mutation definitions stay in evaluator/ and are excluded from prompts/workspaces.
7. Initial pre-CLI milestone: API credentials were unavailable, so the live benchmark was then recorded as unavailable. Scripted E2E tests and dataset integrity checks are real EDA executions, explicitly not measurements of AI repair ability. The later Codex CLI integration and live results are recorded below.
8. Default remote: private GitHub repository CodingBot000/semidebug_agent, per the approved plan.
9. Native runtime supports trusted projects only. Docker offline execution is recommended; adversarial HDL needs a dedicated disposable VM/container boundary beyond lexical patch guards.

## 2026-09-23 — Local Codex inference

Use official host Codex CLI ChatGPT authentication at the user’s request. One structured call returns diagnosis and patch per attempt. A short dedicated instruction file and successful-log compaction reduced input tokens from 16,854 to 6,520 in one FIFO pilot; both proposals passed independent verification. Use the optimized prompt unchanged for the 24 public and 6 holdout cases. Record subscription usage as tokens with null API cost; do not equate this pilot with a general repair-quality improvement. EDA remains in credential-free, network-disabled Docker containers.

## 2026-09-23 — V2 evaluation hardening

Preserve V1 raw files and tag `semidebug-v1-baseline`. Derive `benchmark_v2/` without changing V1 mutations. A separate hidden regression source, longer vectors and two seeds replace the V1 shared-testbench protocol. Filter provider context to visible files and redact detailed evaluator-only failures, while saving full logs locally. This strengthens the evaluation boundary without pretending the internal six design families are independent.

Classify each attempt's retry reason before aggregating results. Keep paired first-proposal versus final-loop counts distinct from independently rerun one-shot measurements because Codex output is stochastic. The V2 internal seven rescues are format repairs, so do not claim they show semantic reasoning improvement.

Freeze ChipBench's zero-shot 12-case selection and SHA256 hashes before inference. Use the official mismatch test as the hidden acceptance criterion, along with existing compile/lint/synthesis/integrity checks. Keep upstream reference/test files in the local evaluator workspace and outside provider requests and the submission ZIP. Preserve all seven final failures in the selected denominator. Defer repository-scale HWE-bench execution after recording its setup and resource uncertainty; no HWE performance claim is made.
