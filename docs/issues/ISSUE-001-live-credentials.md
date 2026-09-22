# ISSUE-001 — Live LLM credentials unavailable

- Discovered: 2026-09-22 UTC, Phase 0 environment inspection.
- Status: Blocked.
- Symptom: OPENAI_API_KEY and ANTHROPIC_API_KEY are absent from the process environment.
- Reproduction: check only boolean presence of credential environment variables; never print values.
- Impact: live API demo and AI repair benchmark cannot run. Deterministic tests, dataset validation and packaging can proceed.
- Cause: no project API configuration supplied.
- Attempts: requested user configuration through asynchronous input. Do not reuse Codex login tokens or other application secrets.
- Resolution: pending `.env` configuration with OPENAI_API_KEY, OPENAI_MODEL and optional OPENAI_BASE_URL.
- Verification: not yet performed; do not claim live AI repair results.
