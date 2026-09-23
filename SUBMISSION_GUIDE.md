# Submission guide

Start with [README](README.md), then [portfolio evidence](PORTFOLIO_EVIDENCE.md), [architecture](docs/ARCHITECTURE.md) and the [V2 evaluation](docs/V2_EVALUATION.md). The project demonstrates that AI proposes RTL repairs while independent tools and evaluator-only tests decide acceptance. The ZIP is self-contained for the included demos and internal benchmark; access to the private GitHub repository is not required.

From the extracted project directory, install [uv](https://docs.astral.sh/uv/getting-started/installation/), start Docker, then run:

```bash
./scripts/bootstrap.sh
./scripts/run_demo.sh --replay
./scripts/run_demo.sh --scripted
```

`--replay` prints a recorded run without executing tools. `--scripted` supplies a known patch but actually runs EDA and regression; neither is a live AI performance measurement. `make test-all` and `make lint` check the included code and fixtures.

To try live AI, install the Codex CLI and sign in with ChatGPT, then run `./scripts/run_demo.sh`. It consumes Codex subscription allowance. New internal benchmarks use `./scripts/run_benchmark.sh benchmark_v2/public` and `benchmark_v2/hidden`; pass `--max-iterations 1` for a new one-shot run. Choose a new `--output` directory for each run. [CLI setup](docs/CODEX_CLI.md).

The included [internal comparison](results/v2/internal/comparison.md) and [external ChipBench evaluation](results/v2/external/chipbench/evaluation.md) are actual model measurements. The [known-fix pipeline result](results/v2/pipeline_validation_summary.json) is scripted and labeled separately. Representative [semantic retry](results/v2/evidence/semantic_retry/report.md) and [final failure](results/v2/evidence/final_failure/report.md) include the validation trail.

ChipBench's original prompt, test and reference files are **not** bundled. The [selection manifest](external/chipbench/selection_manifest.json) pins the upstream commit and hashes. To reproduce that evaluation, clone [ChipBench](https://github.com/zhongkaiyu/ChipBench) at the pinned commit, run `uv run python scripts/import_chipbench.py <checkout>`, then qualify the 12 selected cases with `./scripts/docker_run.sh python evaluator/qualify_chipbench.py` before a live run. The importer refuses changed files. HWE-bench was researched but not run; see [feasibility](docs/HWE_BENCH_FEASIBILITY.md).

The scope, failed cases and security limits are stated in [LIMITATIONS.md](docs/LIMITATIONS.md). The internal evaluator gold is included so the bundled dataset-generation and tests remain inspectable; the runtime model request never receives those files. External reference solutions are omitted. [Third-party attribution](docs/THIRD_PARTY.md).
