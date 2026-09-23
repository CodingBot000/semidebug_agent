# V2 evidence

V1 evidence remains under `results/live_codex/` and the original root-level `results/` files. This directory contains new, separately measured V2 evidence.

- `dataset_audit.json`: real EDA qualification of six gold designs and 30 buggy cases; no model.
- `pipeline_validation_summary.json`: known-fix scripted pipeline check, 30/30; no model.
- `internal/full_loop_*` and `internal/single_shot_*`: actual Codex CLI runs on the V2 internal corpus. Each `results.json` and run directory holds raw outcomes. `internal/comparison.*` compares the fixed case sets.
- `external/chipbench/qualification.json`: pre-model gold/baseline compatibility of the 12 frozen ChipBench cases.
- `external/chipbench/live/`: actual Codex CLI runs. `evaluation.*` preserves the full selected denominator and separate compatibility/failure counts.
- `evidence/`: copies of representative first-shot, format-retry, semantic-retry, one-shot-failure and final-failure traces. Each `provenance.json` points to the original run.

All live runs used ChatGPT-authenticated Codex CLI `gpt-6-sol` with low reasoning effort. They consumed subscription allowance; API cost is `null`. Timing is observed local end-to-end time, not an isolated performance benchmark. An external case is external to this project's self-made corpus; absence from model pretraining is not established.
