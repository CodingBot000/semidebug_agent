# OpenAI API setup

## Configuration

Create an ignored local `.env` file with an OpenAI API key and model ID:

```env
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-6-sol
OPENAI_BASE_URL=https://api.openai.com/v1
SEMIDEBUG_REASONING_EFFORT=low
SEMIDEBUG_API_TIMEOUT=180
```

The key must remain local. `.env` is excluded from the Docker build context and submission ZIP.

## Run

Install dependencies, build the EDA image, and check the environment:

```bash
./scripts/bootstrap.sh
./scripts/doctor.sh
```

Run the live API demo or the final internal benchmark:

```bash
./scripts/run_demo.sh
./scripts/run_benchmark.sh benchmark_v2/public
./scripts/run_benchmark.sh benchmark_v2/hidden
```

`gpt-6-sol` with low reasoning effort is the recorded evaluation configuration. `--model` and `--reasoning-effort` can override these values for a new run. Model output is non-deterministic, so new measurements must use a new output directory.

## Isolation

The OpenAI API request runs in the trusted host process. RTL compilation, simulation, lint, synthesis and evaluator-only regression run in separate network-disabled Docker containers. The API key is not forwarded to those EDA containers, and evaluator-only source is not included in the model request.

The API provider uses Chat Completions Structured Outputs to request one combined diagnosis and patch per attempt. Only the independent validators can approve a patch.

## Usage and cost

Every run records the model, reasoning effort, API call count, input tokens, cached input tokens, output tokens and local end-to-end time. Optional per-million-token prices may be supplied with `SEMIDEBUG_INPUT_PRICE`, `SEMIDEBUG_CACHED_INPUT_PRICE`, `SEMIDEBUG_OUTPUT_PRICE` and `SEMIDEBUG_PRICE_SOURCE`; recorded cost remains `null` when any of these are absent.
