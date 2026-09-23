# Quickstart

Install Git, [uv](https://docs.astral.sh/uv/getting-started/installation/) and Docker, and start the Docker daemon. From a checkout or the extracted submission ZIP:

```bash
./scripts/bootstrap.sh
./scripts/run_demo.sh --replay
./scripts/run_demo.sh --scripted
```

Replay reads the saved V2 semantic-retry evidence only (`--replay-v1` shows the historical V1 sample). Scripted mode uses the new V2 FIFO fixture with separate visible target and evaluator-only regression sources. It supplies a known fix while running Icarus, VVP, Verilator, Yosys and hidden regression tests for real. Neither command measures AI repair performance. `make test-all` and `make lint` verify the included source; `make package` creates the V2 ZIP under `dist/`.

For live inference, install/update the Codex CLI, sign in with ChatGPT and run the demo:

```bash
npm install -g @openai/codex@latest
codex login
codex login status
./scripts/doctor.sh
./scripts/run_demo.sh
```

The default is `gpt-6-sol / low` through normal ChatGPT authentication; no API key is required. It consumes Codex subscription allowance. See [provider setup](docs/CODEX_CLI.md). V2 internal benchmark commands are:

```bash
./scripts/run_benchmark.sh benchmark_v2/public --max-iterations 3
./scripts/run_benchmark.sh benchmark_v2/hidden --max-iterations 3
./scripts/run_benchmark.sh benchmark_v2/public --max-iterations 1
./scripts/run_benchmark.sh benchmark_v2/hidden --max-iterations 1
```

Each benchmark creates a new timestamped directory under `artifacts/benchmark/` unless you provide a new `--output` path. The historical V1 corpus remains under `benchmark/`; the V2 corpus is under `benchmark_v2/`. Saved [V2 results](docs/V2_EVALUATION.md) should be read before rerunning paid/subscription inference.

For external reproduction, obtain [ChipBench](https://github.com/zhongkaiyu/ChipBench), check out commit `b4ba3a06759804ec88c26c3cf15b28b9a90b3443`, then run `uv run python scripts/import_chipbench.py <checkout>`. The importer verifies the frozen [selection manifest](external/chipbench/selection_manifest.json) and writes local cases under `external/chipbench/cases/` (excluded from Git/ZIP). Run `./scripts/docker_run.sh python evaluator/qualify_chipbench.py` before `./scripts/run_benchmark.sh external/chipbench/cases`. The selected 12 cases and all failures must remain in the result denominator.

The canonical environment is Docker with Python 3.12, Icarus 11.0, Verilator 5.006 and Yosys 0.23. Native macOS tools are possible with `brew install icarus-verilog verilator yosys`, `uv sync --frozen` and `uv run semidebug doctor`, but versions may differ from recorded results. If using Colima, place the checkout under a shared home-directory mount. CLI exit codes: 0 completed operation, 1 unrepaired case, 2 configuration or infrastructure error. A benchmark can exit 0 while containing failed cases; inspect its `summary.json`.
