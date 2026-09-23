# ISSUE-010 — Live model produced malformed unified diff

- Discovered: 2026-09-23, frozen public and holdout Codex benchmark.
- Status: Resolved within the bounded repair loop; model limitation retained in metrics.
- Symptoms: case_013_arbiter_reset, case_014_arbiter_combinational, case_024_alu_combinational and case_027_pulse_combinational first proposals failed with `Hunk truncated or invalid`.
- Reproduction: inspect their first patch_attempts in results/live_codex/public_v1/results.json and hidden_v1/results.json.
- Cause: generated unified diff hunk structure/count did not satisfy strict patch parsing.
- Impact: one additional model inference for each affected case; no invalid patch was accepted.
- Action: existing guard rejected the patch and fed the recorded error into the next attempt. No tests, gold RTL, prompt or parser limits were changed during evaluation.
- Verification: all seven cases passed actual EDA, full regression and immutable integrity checks on attempt two.

- Holdout follow-up: case_010_fifo_boundary, case_015_arbiter_combinational and case_020_controller_fsm had the same first-attempt guard error and passed on attempt two. Total: 7 rejected proposals out of 37 (18.9%).
