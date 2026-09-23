# Evidence provenance

These files are actual tool outputs or summaries of executed commands. The root-level dataset and known-fix pipeline records below are not live AI repair results. `live_codex/` contains V1 live Codex CLI measurements; `v2/internal/` and `v2/external/` contain separately measured V2 runs.

- environment.json / docker_environment.json: actual canonical toolchain versions and image/base IDs.
- dataset_audit.json: each gold target/regression and all 30 broken baseline tool results.
- benchmark_results.json / .csv / benchmark_summary.*: known-fix scripted provider through the full real EDA repair loop; **not AI performance**.
- benchmark_v1.json / benchmark_v2.json / benchmark_comparison.json: repeatability of that same pipeline, no model tuning.
- sample_run/, retry_run/, failed_run/: full recorded traces/diffs/logs. Provider mode is explicitly scripted.
- live_demo_attempt.log / live_benchmark_status.json: historical missing-credential attempt before the Codex CLI integration. Later successful live results are under `live_codex/`.

Durations and random run IDs vary. Test seeds, corpus and dependency versions are fixed. Runtime provider call counts in scripted runs count invocations of the test double, not network API calls. Source/code snippets in reports are trusted local dataset material.
