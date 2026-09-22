# Quickstart

1. Install Git, uv and Docker; start the Docker daemon.
2. From the project directory run `./scripts/bootstrap.sh` (network needed only to build/install).
3. Run `./scripts/run_demo.sh --scripted` for real EDA validation with an explicitly scripted patch.
4. Run `./scripts/run_demo.sh --replay` to read recorded evidence without EDA execution.
5. Run `make test-all` and `make lint`.
6. For live AI: copy `.env.example` to `.env`, set OPENAI_API_KEY and OPENAI_MODEL, then run `./scripts/run_demo.sh`.
7. Run `./scripts/run_benchmark.sh benchmark/public`; after deciding improvements, repeat the same split and separately evaluate `benchmark/hidden`.
8. Run `make package`. The ZIP and SHA256 file are written under `dist/`.

The repository is private by default; GitHub authentication with access is required to clone it. An extracted submission ZIP can be used without GitHub access.

Canonical tools: Docker, Python 3.12, Icarus 11.0, Verilator 5.006, Yosys 0.23. Native alternative on macOS: `brew install icarus-verilog verilator yosys`, `uv sync --frozen`, then `uv run semidebug doctor`. Native tool versions may differ from canonical results.

A successful fix saves the diff, logs, fingerprint maps and corrected RTL under `artifacts/runs/<run-id>/`; it does not overwrite the input project. CLI exit codes: 0 successful operation, 1 unrepaired case/failed validation, 2 configuration or infrastructure error. A benchmark can finish successfully with unfixed cases; inspect summary.json for actual repair rates.

No API key is necessary for scripted tests or replay. Recorded/scripted examples must never be presented as live AI inference.
