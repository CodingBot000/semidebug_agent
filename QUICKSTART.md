# Quickstart

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Docker, and start the Docker daemon. A source clone additionally needs Git; the extracted submission ZIP is self-contained:

```bash
./scripts/bootstrap.sh
./scripts/run_demo.sh --replay
./scripts/run_demo.sh --scripted
```

Replay reads the saved semantic-retry evidence. Scripted mode uses a FIFO fixture with separate visible target and evaluator-only regression sources. It supplies a known fix while running Icarus, VVP, Verilator, Yosys and hidden regression tests for real. Neither command measures AI repair performance. `make test-all` and `make lint` verify the included source; `make package` creates the final ZIP under `dist/`.

For live inference, set `OPENAI_API_KEY` and `OPENAI_MODEL=gpt-6-sol` in the ignored local `.env`, then run:

```bash
./scripts/doctor.sh
./scripts/run_demo.sh
```

The recorded configuration is `gpt-6-sol / low` through the OpenAI API. Calls are billed to the configured API project. The host process makes model requests; network-disabled Docker containers run EDA without the API key. See [OpenAI API setup](docs/OPENAI_API.md). Final internal benchmark commands are:

```bash
./scripts/run_benchmark.sh benchmark_v2/public --max-iterations 3
./scripts/run_benchmark.sh benchmark_v2/hidden --max-iterations 3
./scripts/run_benchmark.sh benchmark_v2/public --max-iterations 1
./scripts/run_benchmark.sh benchmark_v2/hidden --max-iterations 1
```

Each benchmark creates a new timestamped directory under `artifacts/benchmark/` unless you provide a new `--output` path. The final corpus is under `benchmark_v2/`. Read the saved [evaluation results](docs/EVALUATION.md) before spending API usage on a rerun.

For external reproduction, obtain [ChipBench](https://github.com/zhongkaiyu/ChipBench), check out commit `b4ba3a06759804ec88c26c3cf15b28b9a90b3443`, then run `uv run python scripts/import_chipbench.py <checkout>`. The importer verifies the frozen [selection manifest](external/chipbench/selection_manifest.json) and writes local cases under `external/chipbench/cases/` (excluded from Git/ZIP). Run `./scripts/docker_run.sh python evaluator/qualify_chipbench.py` before `./scripts/run_benchmark.sh external/chipbench/cases`. The selected 12 cases and all failures must remain in the result denominator.

The canonical environment is Docker with Python 3.12, Icarus 11.0, Verilator 5.006 and Yosys 0.23. Native macOS tools are possible with `brew install icarus-verilog verilator yosys`, `uv sync --frozen` and `uv run semidebug doctor`, but versions may differ from recorded results. If using Colima, place the checkout under a shared home-directory mount. Command exit codes are 0 for a completed operation, 1 for an unrepaired case and 2 for a configuration or infrastructure error. A benchmark can exit 0 while containing failed cases; inspect its `summary.json`.
