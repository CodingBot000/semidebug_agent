# Delivery checklist

## Implemented and exercised
- [x] Validated project manifests; input RTL is never overwritten.
- [x] Actual baseline compile/simulation/lint/synthesis failure evidence.
- [x] Provider abstraction, JSON schema hypotheses/diffs, malformed/API error handling and usage capture (HTTP mocked tests).
- [x] Strict patches, path allowlist, immutable fingerprints, isolated candidate workspaces.
- [x] Independent EDA tools, target plus full regression gate, retry and bounded safe termination.
- [x] JSON/JSONL trace, tool logs, hypotheses, diffs, final artifacts and human-readable reports.
- [x] 30 benchmark cases, 24 public/6 holdout, six verified gold designs and 30 reproducible failures.
- [x] Actual known-fix pipeline benchmark and repeat; explicit non-AI labels; raw CSV/JSON preserved.
- [x] Successful first attempt, retry success and failed-run examples with real EDA.
- [x] README, QUICKSTART, portfolio, research/decisions, architecture, benchmark, security, third-party docs.
- [x] Unit/integration/scripted E2E tests and lint passed during development; final clean clone check recorded separately.
- [x] Docker base digest, exact EDA versions, locked Python dependencies and CI.
- [x] Package allowlist, secret scan, SHA256 and 50 MB limit implemented.

## Live inference follow-up
- [x] Actual ChatGPT-authenticated Codex CLI inference and demo; ISSUE-001 resolved via CLI. Separate API endpoint remains unmeasured.
- [x] Token overhead reduced in one real demo comparison; fixed prompt used for public/holdout measurement. This is not a controlled repair-quality improvement experiment.

Packaging, clean-clone reproduction and GitHub publication execution results are appended to PROGRESS.md. This checklist does not claim unexecuted live AI work is complete.

## Final executed reproduction
- [x] Fresh clone, locked installation and Docker image build.
- [x] Complete suite: 86 passed in 8.93 seconds; lint and format pass.
- [x] Shipped scripted demo passes with real EDA; unshared-mount error is actionable.
- [x] Whitelist/secret scan, ZIP integrity and size below 50 MB.
- [x] Test output and dataset fingerprint preserved in results/verification/.
- [x] GitHub private repository created and main pushed with upstream tracking.
- [x] GitHub Actions image build, lint/format and complete test suite passed on the published source commit.

## CLI integration validation (2026-09-23)

- Complete suite: **95 passed in 10.19 seconds**. Ruff check and format passed.
- Host Codex login stays outside credential-free EDA containers.
- Live evaluation complete: public 24/24, holdout 6/6; first attempt 23/30; 37 actual CLI calls. Raw results preserved.
- GitHub Actions run 35824003905 passed for source commit c024c43859128190a8e6afe26f54e1a0a53e6d45.
