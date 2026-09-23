# Submission guide

Start with [README](README.md), then [portfolio evidence](PORTFOLIO_EVIDENCE.md), [architecture](docs/ARCHITECTURE.md), [evaluation](docs/EVALUATION.md) and the [verification report](VERIFICATION_REPORT.md). Together they show the problem, the model/evaluator boundary, actual repair results, retained failures and executed source checks.

The ZIP contains one final project state. It includes the implementation, final internal corpus, aggregate internal and external results, representative success/retry/failure traces, and lint/test/demo logs. Historical evaluation material and repository history are not part of the submission.

The saved logs are sufficient for document review. To rerun the checks optionally, install [uv](https://docs.astral.sh/uv/getting-started/installation/), start Docker, and run from the extracted directory:

```bash
./scripts/verify_submission.sh
```

This runs bootstrap, a recorded semantic-retry replay, the scripted real-EDA pipeline demo, lint and the complete test suite. Scripted mode supplies a known patch and verifies the acceptance pipeline; it is not a live AI performance measurement.

To try live AI, add `OPENAI_API_KEY` and `OPENAI_MODEL` to a local `.env` and run `./scripts/run_demo.sh`. This consumes OpenAI API usage. The saved internal and external results are actual API model measurements; rerunning them can produce different proposals.

ChipBench's original prompt, test and reference files are not bundled. The [selection manifest](external/chipbench/selection_manifest.json) identifies the exact upstream inputs and their hashes. External reference solutions and official tests remain evaluator-only.

The scope and known limits are stated in [LIMITATIONS.md](docs/LIMITATIONS.md), and external software and data are listed in [THIRD_PARTY.md](docs/THIRD_PARTY.md).
