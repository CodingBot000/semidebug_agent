# ISSUE-008 — Installed Codex CLI too old for requested GPT-6 models

- Discovered: 2026-09-23 during live provider setup.
- Status: Resolved.
- Initial CLI: 0.147.0, ChatGPT authenticated. Local cache listed GPT-6, but actual Sol request returned HTTP 400 unsupported; Astra explicitly required a newer CLI.
- Impact: initial live demo attempts ended LLM_ERROR with zero inference tokens for rejected requests.
- Resolution: verified npm's official @openai/codex package latest version and updated to 0.156.1; authentication retained. The user also permitted any working model.
- Verification: GPT-6 Sol / low completed a real FIFO diagnosis/patch call after update; full EDA and regression passed on its first candidate.
- No tokens were extracted, copied or repurposed; the CLI manages ChatGPT authentication.
