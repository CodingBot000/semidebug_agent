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

## GitHub publication
- Created **private** repository https://github.com/CodingBot000/semidebug_agent.
- Initial publication succeeded: branch `main`, commit `297a0d4376df0f71a41f8313fc9ed121c2bb3679`, upstream `origin/main`.
- GitHub Actions validation started for that commit. Its final outcome is recorded below after completion.
- Live API evaluation remains the only externally blocked work; see ISSUE-001. No live-AI success rate or improvement is claimed.
- GitHub Actions [validation run 35782805742](https://github.com/CodingBot000/semidebug_agent/actions/runs/35782805742) completed successfully: image build, lint/format and the complete test suite passed on GitHub's runner. Machine-readable status: `results/verification/github_ci.json`.
- Final publication record is a documentation/evidence-only follow-up commit; application/test sources are unchanged from the successful CI commit. The follow-up uses `[skip ci]` to avoid rerunning identical source checks.
- Final submission ZIP and its SHA256 sidecar are generated in `dist/` after this record; the archive excludes .git, .env, caches and build outputs and remains below 50 MB.

## Codex CLI provider — 2026-09-23
- User requested ChatGPT-authenticated local Codex CLI instead of a separately billed API key, with GPT-6 Astra low or Sol.
- Verified installed CLI 0.147.0 and `codex login status`: logged in using ChatGPT. Local model catalog lists `gpt-6-sol` with low reasoning supported.
- Selected `gpt-6-sol`, low reasoning. Keep authentication managed by the CLI; do not extract tokens or mount credentials into EDA containers.
- Implement a host CLI provider plus network-disabled Docker EDA execution. Combine hypothesis and patch in one structured CLI response to reduce model calls per attempt.
- Existing scripted measurements remain preserved; new live measurements will be recorded separately.
- Initial CLI requests exposed outdated-version/model-catalog mismatch (ISSUE-008). Updated official Codex CLI from 0.147.0 to 0.156.1 while preserving ChatGPT login.
- Corrected CLI event classification (ISSUE-009); diagnostic metadata warnings are distinct from actual tool calls.
- First real GPT-6 Sol / low FIFO demo: FIXED on first candidate, all independent EDA + regression + immutable checks passed; one CLI invocation, 16,854 input / 251 output tokens. This is a pilot, separate from benchmark measurements.
- Applying usage reduction before the fixed benchmark protocol: short stateless model instructions, minimal unused skill catalog, and omission of verbose successful-validator logs from prompts only. Full validation artifacts remain preserved.
- Optimized real FIFO demo: FIXED on the first candidate, one CLI call, 6,520 input / 322 output tokens, zero model tool calls. The previous successful pilot used 16,854 input tokens: a 61.3% input reduction on this one example, not a general cost guarantee.
- Freeze the optimized provider/prompt for the live benchmark: GPT-6 Sol, low, max 3 attempts, public 24 then holdout 6, one structured CLI request per attempt, same original immutable corpus.
- Local Codex integration verification: Docker full suite 95 passed in 10.19s; Ruff check/format pass. Host doctor confirms CLI ChatGPT login and Docker EDA versions. Raw verification saved under results/verification/codex_*.
- Frozen live public benchmark: 24/24 fixed, first attempt 20/24, median 14,507.5ms, 28 inference calls. Four malformed proposals were rejected and corrected on retry; ISSUE-010 records them.
- Source implementation committed and pushed as c024c43859128190a8e6afe26f54e1a0a53e6d45. GitHub Actions run 35824003905 started; final result will be recorded below.
- Frozen holdout completed 6/6; first attempt 3/6. Overall 30/30, first attempt 23/30, 37 actual CLI calls, median 14,679.5ms. Input 234,948 including cached 78,848; output 12,223. Seven malformed diff proposals safely rejected then corrected. All raw runs, CSV/JSON summaries, optimized demo and pilot usage comparison exported under results/.
- GitHub Actions run 35824003905 completed successfully for c024c43859128190a8e6afe26f54e1a0a53e6d45. Local 95-test suite and cloud CI both pass. API costs stay null because ChatGPT subscription authentication was used.
- 2026-09-23: 사용자가 요청한 완료된 개발 계획 문서 `docs/SemiDebug_Agent_Codex_Development_Plan.md`를 저장소에서 삭제. 코드·가이드 문서 참조가 없는 것을 확인했으며, 제출 ZIP도 삭제 내용을 반영해 다시 생성함.
- 2026-09-23: 신규 작업자가 `git pull` 후 목적·폴더·실행·설계 및 평가 문서를 빠르게 찾도록 README 저장소 구조와 문서 읽기 순서를 보강. BENCHMARK의 이전 public-only/재시도 요약을 전체 30건 집계와 일치시킴.
