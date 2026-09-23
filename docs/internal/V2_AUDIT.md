# V2 repository audit

Observed 2026-09-23 before V2 implementation. This is an audit of the checked-out repository, not a V2 benchmark result.

## Frozen V1 baseline

- Branch: `main`; commit: `afc0582e08ba5463a0d4e35630dbebc7432028d4`.
- Local annotated tag: `semidebug-v1-baseline`. No tag or commit was pushed.
- Before changes, the only untracked path was `docs/update/`.
- V1 live summary `results/live_codex/summary.json`: SHA256 `dd19aed0f5ac2d0ee869d692f301c0381cf3dd6a96f883e0da4223607ea9496c`.
- V1 public/holdout summaries: SHA256 `8893398b55e55bd90b4992b83641c0ef24dc71b79f18d91bf4feadb45505fbf8` / `bcfecb23ef43b5c88a8b5a6c30cf64c135303f7122745ac0e34f11bf6d50a8b6`.
- Known-fix results JSON/CSV: SHA256 `0f7041ed97ce39e7d934567c249395d89ab4c3fcea8994b63af4f34f561e117c` / `a8b9084b581824ac318dcdd54585d84c3bc66f2c18a14994d3b561cf175ed648`.
- Dataset audit: SHA256 `d664bebfecc5c0ad6e5a24eaf1820c817076b639bf741fce2a799a92732f4ddd`.
- Raw V1 live records show 30/30 fixed, 23/30 first attempt, 37 calls. All seven retries followed rejected malformed unified diffs; none was a validated semantic failure rescued by feedback. V1 therefore cannot establish a semantic retry benefit.

## Current execution path and boundaries

1. `scripts/run_demo.sh` and `scripts/run_benchmark.sh` call `uv run semidebug`; default provider is host `codex exec` with ChatGPT authentication. Scripted demo uses the Docker wrapper.
2. `cli.py` loads `case.json`, sets provider, iteration limit and EDA runtime, then calls `agent/orchestrator.py`. `--max-iterations 1` already supports a single-proposal run.
3. `benchmark/loader.py` validates paths and requires every target/regression source to be immutable. `tools/workspace.py` copies only mutable RTL, immutable files and the manifest into isolated candidate directories. `evaluator/gold/` and mutation definitions are outside this copy.
4. `context/selector.py` serializes mutable RTL **and sources from both target and regression tests** into the model context. It also serializes every immutable path. The orchestrator adds baseline evidence and previous attempt results, including regression logs. The provider receives this context.
5. Patch guard limits edits to the manifest's mutable RTL. Icarus/VVP, Verilator and Yosys validate a fresh candidate; regression and SHA256 integrity gate `FIXED`. Failed candidates do not change the input project.
6. `benchmark/runner.py` saves per-run JSON/logs plus aggregate JSON/CSV/Markdown. V1 `PatchAttempt` records guard errors and tool bundles but has no explicit retry reason. Current aggregate lacks semantic/format rescue counts.

## Answers to the ten required questions

1. **V1 route:** host Codex CLI inference, Docker EDA validation, bounded repair loop, then saved evidence. API and scripted providers also exist but are different measurements.
2. **Prompt visibility:** mutable RTL, target and regression test source selected by `select_context`, immutable path names, EDA evidence and previous attempt summaries. The exact provider request is assembled in `llm/codex.py`.
3. **Regression source visible?** Yes. `select_context` explicitly iterates over `case.regression`. The FIFO manifest uses the same `tb/fifo_tb.v` for target and regressions, with `+REGRESSION` and different seeds. Filtering regression paths alone would not hide regression logic in this case.
4. **Gold/mutation isolation:** Gold and mutation source are not copied to the runtime workspace. This protects those files, but it does not establish hidden regression isolation.
5. **Single-shot possible?** Yes, CLI `--max-iterations 1`. A separate V2 output directory and fixed case/model protocol are still needed for a fair comparison.
6. **Retry taxonomy today:** Guard error and tool result details permit retrospective classification, but no stable per-attempt reason field or semantic rescue metric exists. Seven V1 retries are format/guard failures.
7. **Least invasive external adapter:** add an importer/protocol beside `src/semidebug/benchmark/`, preserve the internal manifest loader, and use a separate validator when the external benchmark's official acceptance check does not fit the internal Icarus/Verilator/Yosys contract.
8. **Document issues:** V1 counts in README/portfolio/benchmark match the saved summary, but first-attempt improvement can be misread as semantic feedback value; the seven V1 retries were format repairs. README/benchmark/security text describes testbench visibility without stating regression source exposure. The V2 plan names root `ARCHITECTURE.md`, while the current file is `docs/ARCHITECTURE.md`; it also names a nonexistent `CODEX_SUBMISSION_DOC_REVIEW.md` instead of the supplied review instruction filename.
9. **ZIP exclusions:** `.env`, credentials, Codex auth, `.git`, `.venv`, caches, full external datasets, Docker images, unnecessary gold/reference answers, duplicate raw logs and local absolute paths. Current package allowlist includes all of `evaluator/` and `results/`; V2 packaging must narrow this deliberately.
10. **External licenses:** upstream ChipBench is MIT ([license](https://github.com/zhongkaiyu/ChipBench/blob/main/LICENSE)); the RTL repair [HWE-bench](https://github.com/pku-liang/hwe-bench) repository is Apache-2.0 ([license](https://github.com/pku-liang/hwe-bench/blob/main/LICENSE)). Dataset and subject-project assets can carry additional provenance; pin exact commits and inspect selected files before redistribution. Prefer shipping selection manifests, hashes and download instructions rather than full external data.

## Priority and acceptance gate

First separate prompt-visible target tests from evaluator-only regression tests and prove the boundary with serialization/integration checks. A shared testbench with a hidden plusarg does not meet this gate. Keep V1 raw files untouched and store all V2 runs under new paths. Before any external model evaluation, freeze the upstream revision, case selection and unsupported-case criteria. Re-measure the internal benchmark after the evaluation protocol changes; V1 results remain historical.
