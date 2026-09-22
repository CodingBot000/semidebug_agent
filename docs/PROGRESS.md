# Development progress

All timestamps use UTC unless specified. Test and benchmark numbers come from executed commands.

## 2026-09-22 / Phase 0 — research (completed)
- Read the complete development plan, including recording and GitHub publishing instructions.
- Host: macOS 14-era Darwin 23.6 x86_64; Python 3.13.1; uv 0.12.5; Docker client 29.7.2/server 29.5.2; Git 2.46.0.
- GitHub CLI authenticated as CodingBot000. No local Git metadata, native EDA tools, or LLM API environment credentials.
- Verified official Icarus, Verilator, Yosys documentation and current Homebrew formula metadata.
- Decision: canonical EDA runtime is Docker; explicit Python state machine; strict structured provider boundary.
- ISSUE-001: live LLM credentials unavailable; requested user setup asynchronously, continue independent implementation.

## Phase 1 — bootstrap (in progress)
- Create package, CLI, locked dependencies, Docker toolchain and progress/issue records.
- Next: actual compile/simulation/lint/synthesis validation before LLM integration.

## Phases 1–7 — implementation milestones
- Bootstrap: Git main initialized, Python package installed with uv; Docker EDA image built successfully.
- Phase 2: six gold designs passed compile, target simulation, lint, synthesis and two regression seeds. Raw results: `results/dataset_audit.json`.
- Phase 3: strict unified-diff parser/application, path allowlist, immutable fingerprints, bypass guard and isolated baseline copies implemented.
- Phase 4: structured OpenAI-compatible HTTP provider with timeout, bounded retries, output validation, token counters and scripted test double implemented. Live access remains blocked by ISSUE-001.
- Phase 5: explicit repair state machine with rollback, repeated-patch/failure termination and JSONL evidence implemented.
- Phase 6: 30 original mutations across six RTL designs; public 24, holdout 6. All 30 reproduce an actual EDA failure. Gold is held in evaluator/ and never selected for runtime prompts.
- Phase 7: CLI benchmark discovery, CSV/JSON/Markdown export and metric aggregation implemented.
- First unit test run: `uv run pytest tests/unit -q` — 36 passed in 1.62s. Ruff formatting resolved initial style findings; `uv run ruff check src tests evaluator` passes.
- Integration/E2E run is in progress. Actual image versions: Python 3.12.14, Icarus 11.0, Verilator 5.006, Yosys 0.23 (distribution packages, deliberately distinct from latest upstream).

## Phases 8–13 — validation and evidence
- Initial real-EDA integration and E2E: 44 passed in 7.18s; unit: 36 passed. No benchmark testbench/expected output was relaxed.
- Known-fix pipeline benchmark v1: 30/30 accepted, median 360.5 ms, all immutable fingerprints preserved. Explicitly a scripted evaluator self-test, not AI repair performance.
- Captured first-shot, retry-success and repeated-patch-failure examples with real tool logs.
- Phase 8 live model improvement is blocked by ISSUE-001. Do not invent before/after AI results. A second known-fix pipeline run will check reproducibility only.
- ISSUE-003 found by running the shipped demo wrapper on macOS: Bash 3.2 empty-array expansion failed under nounset. Corrected the wrapper and reran it successfully.
- Full suite through the corrected Docker wrapper: **84 passed in 8.50s**. Added packaging/CSV export/regression failure gate tests.
- Docker base digest and exact EDA package versions pinned. Python dependencies locked. Added CI, README, QUICKSTART, architecture, security, licensing and portfolio evidence.
- Live demo entry point was attempted and returned exit 2 with a clear missing API configuration message, recorded in `results/live_demo_attempt.log`. No API call occurred.
- Additional robustness review corrected final trace persistence and integrity handling when original files disappear during a provider error, and baseline regression infrastructure error termination. Added a regression test for that failure path.

## Phase 14 — packaging and final checks
- Known-fix pipeline repeat: 30/30 again; median 363.5 ms versus 360.5 ms. No model improvement claimed; same corpus, no model used.
- Initial package passed whitelist/secret scanning and ZIP integrity checks: 352 files, 321,368 bytes (<50 MB). Final package will be refreshed after delivery records.
- Post-review Docker suite: 85 passed; then added malformed provider JSON-envelope coverage (ISSUE-005). Targeted provider suite passed; final fresh-clone suite follows.
- Actual source/API raw credentials are absent from staging; staged content scan passed.
- First clean clone under host /tmp: uv install, Docker build, lint and ZIP generation succeeded; runtime EDA tests/demo failed because Colima does not share that host path (ISSUE-007). This attempt is not counted as a successful reproduction.
- Added a project-mount preflight and moved the clean-clone verification to a shared directory under the user home. Raw runtime logs are retained outside the repository during the repeat.
- Successful fresh clone under Colima's shared home path: `uv sync --frozen`, clean Docker build, scripted FIFO demo, lint/format, and ZIP generation all passed.
- Final fresh-clone suite: **86 passed in 8.93s**. Full stdout and corpus fingerprint are committed under `results/verification/`.
- The unshared-directory wrapper now returns a clear diagnostic and exit 2, verified against the original /tmp reproduction directory.
- Fresh-clone ZIP: 356 files, 324,726 bytes; final delivery archive is regenerated after publication records. No secrets or excluded environment/cache/build files were found.
- GitHub namespace/repository lookup confirmed CodingBot000/semidebug_agent did not exist. Live credentials remain unavailable; implementation and deterministic verification are delivered, AI measurements remain explicitly blocked.
