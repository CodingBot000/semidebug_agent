# Final OpenAI API evaluation evidence

This directory contains the final submission evidence measured with the OpenAI API using `gpt-6-sol` and low reasoning effort.

- `dataset_audit.json`: model-independent EDA qualification of six gold designs and 30 buggy cases.
- `pipeline_validation_summary.json`: known-fix scripted pipeline check, 30/30; not AI performance.
- `internal/full_loop_*`: maximum three-attempt API runs, 29/30 fixed and 22/30 accepted on the first proposal.
- `internal/single_shot_*`: independent one-attempt API runs, 23/30 fixed.
- `internal/comparison.*`: paired first-proposal/final-loop and independent one-shot comparison.
- `external/chipbench/qualification.json`: pre-model compatibility of all 12 selected ChipBench cases.
- `external/chipbench/live/`: OpenAI API runs, 6/12 fixed with all six final failures retained.
- `evidence/`: representative first-shot, format-retry, semantic-retry, one-shot-failure and final-failure traces.
- `verification/`: final lint, complete test-suite and scripted pipeline-demo logs.

The API measurements used one combined Structured Output containing diagnosis and patch per attempt. API calls ran on the host while all RTL validation ran in network-disabled Docker containers without API credentials. Token counts, cached tokens, timing and estimated cost are recorded in each result.
