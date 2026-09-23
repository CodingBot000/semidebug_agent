# ISSUE-001 — Live LLM credentials unavailable

- Discovered: 2026-09-22 UTC, Phase 0 environment inspection.
- Status: Resolved (2026-09-23, official Codex CLI authentication).
- Symptom: OPENAI_API_KEY and ANTHROPIC_API_KEY are absent from the process environment.
- Reproduction: check only boolean presence of credential environment variables; never print values.
- Impact: live API demo and AI repair benchmark cannot run. Deterministic tests, dataset validation and packaging can proceed.
- Cause: no project API configuration supplied.
- Attempts: requested user configuration through asynchronous input. Do not reuse Codex login tokens or other application secrets.
- Original proposed resolution: API configuration; superseded by the CLI route below.
- Verification: actual CLI inference and independently validated demo; see resolution below.

## Resolution

The original API-key route was unavailable. At the user’s request, implemented a host Codex CLI adapter using its normal ChatGPT login; no tokens are extracted or repurposed. CLI 0.156.1 and gpt-6-sol / low completed the live FIFO demo with actual EDA, regression and integrity checks. The CLI route removes the live-inference blocker; separate API endpoint compatibility remains unmeasured. See CODEX_CLI.md and the live benchmark evidence.
