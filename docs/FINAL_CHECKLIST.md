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

## External dependency
- [ ] Live API/model compatibility and actual AI repair benchmark: blocked by missing OPENAI_API_KEY / OPENAI_MODEL (ISSUE-001).
- [ ] Evidence-based live model improvement and public/holdout comparison: requires the live baseline above. Scripted pipeline repeat is not a substitute.

Packaging, clean-clone reproduction and GitHub publication execution results are appended to PROGRESS.md. This checklist does not claim unexecuted live AI work is complete.
