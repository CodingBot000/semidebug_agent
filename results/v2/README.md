# Final evaluation evidence

This directory contains the evaluation evidence used in the submission.

- `dataset_audit.json`: real EDA qualification of six gold designs and 30 buggy cases; no model.
- `pipeline_validation_summary.json`: known-fix scripted pipeline check, 30/30; no model.
- `internal/full_loop_*` and `internal/single_shot_*`: actual Codex CLI runs on the final internal corpus. `internal/comparison.*` compares the fixed case sets.
- `external/chipbench/qualification.json`: pre-model gold/baseline compatibility of the 12 selected ChipBench cases.
- `external/chipbench/live/`: actual Codex CLI runs. `evaluation.*` retains all selected successes and failures.
- `evidence/`: representative first-shot, format-retry, semantic-retry, one-shot-failure and final-failure traces.
- `verification/`: executed source checks and their logs.

All live runs used ChatGPT-authenticated Codex CLI `gpt-6-sol` with low reasoning effort. They consumed subscription allowance; API cost is `null`. Timing is observed local end-to-end time, not an isolated performance benchmark. An external case is external to this project's self-authored corpus; absence from model pretraining is not established.
