# Verification report

**Status: PASS** · recorded 2026-09-23 UTC

This report records checks executed against the final SemiDebug Agent source included in the submission. The saved logs allow review without rerunning the project; `./scripts/verify_submission.sh` is provided for an optional independent rerun.

| Check | Recorded result | Evidence |
|---|---|---|
| Lint and format | PASS, exit 0 | `results/final/verification/lint.log` |
| Full Docker test suite | **104 passed**, exit 0 | `results/final/verification/test_all.log` |
| Scripted pipeline demo | PASS, exit 0 | `results/final/verification/scripted_demo.log` |
| Patch acceptance gates | Compile, simulation, lint, synthesis, two evaluator-only regression seeds and integrity all passed | `results/final/verification/scripted_demo_result.json` |

The scripted demo supplies a known patch and verifies the complete acceptance pipeline; it is not an AI repair-accuracy measurement. Actual OpenAI API measurements are reported separately in [the evaluation](docs/EVALUATION.md): the internal feedback loop fixed 29/30 cases, an independent one-shot run fixed 23/30, and the selected external ChipBench evaluation fixed 6/12 with all six final failures retained.

SemiDebug is a research and portfolio prototype for small RTL repairs. Passing the configured checks does not establish formal equivalence or production silicon readiness.
