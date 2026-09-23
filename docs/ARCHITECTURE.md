# Architecture

SemiDebug owns the control flow. The LLM returns hypotheses and candidate diffs through a typed provider boundary; it cannot invoke arbitrary commands or declare validation success.

`benchmark/loader.py` validates the explicit project manifest and path boundaries. `tools/workspace.py` copies only mutable RTL, immutable testbench/expected files and the manifest into an isolated temporary directory. Gold and mutation definitions are evaluator-only. `tools/validation.py` runs Icarus/VVP, independent Verilator lint, and Yosys structural sanity. The runner uses argv lists, a credential-free environment, bounded output and process-group timeouts.

`agent/orchestrator.py` collects actual baseline evidence, selects bounded context, asks for a structured analysis and patch, guards the diff, and applies it with exact context matching. Each failed attempt is discarded. Every next attempt starts from the original baseline and includes prior diffs, commands, exit codes and failure logs. Two consecutive invalid patches, repeated diffs, repeated hypotheses/failures, exhausted budget and infrastructure/provider errors terminate the run.

A candidate must pass compile, target simulation, critical lint policy, synthesis, two longer regression seeds and immutable integrity before `FIXED`. Original user files remain untouched; accepted RTL and the exact diff are saved under `final/`. Exit zero without a trusted testbench completion marker is failure. Even after success, the original project's complete selected-file fingerprints are checked.

Artifact schema: run.json/result.json, events.jsonl, baseline tool logs, attempts/NN/hypothesis.json + patch.diff + validation.json, final/patch.diff + RTL + regression.json + metrics.json, report.md. Reports show actual checks and explicitly mark unexecuted stages. Provider errors do not dump raw API bodies or credentials.

See [Mermaid source](architecture.mmd). The design is single-process and sequential to keep retries and evidence understandable. Native subprocesses are not a security sandbox; see SECURITY.md.

## Local CLI inference adapter

The default provider is `live-codex-cli`. Host `codex exec` uses normal ChatGPT authentication and returns one structured diagnosis/patch pair per attempt. The orchestrator consumes that pair through its existing analysis/patch interface. The next failed attempt gets new evidence and a new call; the adapter does not reuse a proposal across changed contexts. The CLI cannot execute model tools. Host orchestration dispatches manifest-limited temporary workspaces to credential-free, network-disabled EDA Docker workers. CLI usage and version are attached to each run; subscription cost stays null.
