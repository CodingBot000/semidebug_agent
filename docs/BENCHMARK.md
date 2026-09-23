# Benchmark methodology and measured results

## Dataset

Six original designs, each with five distinct mutations: counter/timer, four-entry synchronous FIFO, two-input round-robin arbiter, three-state controller, eight-operation ALU and enabled rising-edge pulse detector. Category coverage includes syntax, width/signedness, reset, sequential logic, boundary, FSM, combinational and connectivity faults. There are 24 public and 6 holdout cases. Only 2/30 are syntax faults; most require functional correction.

`evaluator/build_dataset.py` first constructs each gold RTL and testbench, then runs the target plus two longer regression seeds through real EDA. Only after all six gold designs pass does it emit mutations. Each mutation is validated and must reproduce a failure; infrastructure errors are not accepted as a detected bug. Testbenches use reference state/scoreboards, directed boundary vectors and seeded pseudorandom cases. Target seed is 7; regression seeds are 17 and 103.

Gold and exact mutation definitions remain in evaluator/. Runtime loading copies only manifest-listed RTL, tests, metadata and the manifest. Prompt context includes only selected RTL and read-only testbench source, never gold, mutation definitions or split labels. Holdout means different mutations of the same design families, not secret data or unseen designs.

## Actual measurements

- Dataset qualification: **6/6 gold designs passed all target and regression checks**.
- Broken qualification: **30/30 mutations reproduce an EDA failure**.
- Known-fix pipeline acceptance: **30/30 fixed on first supplied patch**, full regression and immutable integrity passed. Median measured wall time was **360.5 ms** in the first run; two scripted provider calls per case, no API tokens. This tests the implementation against known fixes and does **not** measure AI repair success.
- Live Codex CLI public benchmark: **24/24 repaired**, 20/24 first attempt, median 14,507.5 ms. Model gpt-6-sol, low effort, CLI 0.156.1, ChatGPT subscription. Full records: `results/live_codex/public_v1/`.

Raw dataset records: `results/dataset_audit.json`. Pipeline summary/rows: `results/benchmark_summary.json`, `results/benchmark_results.json`, `results/benchmark_results.csv`. Each row includes before/after validation, proposals, statuses and hashes. Example full traces are under sample_run/, retry_run/, failed_run/.

## Metrics

Repair success and first-attempt rates divide accepted fixes by all cases. Invalid patch rate divides guard rejections by generated proposals. Retry count is max(iteration-1, 0); median time includes validation and provider time. Regression integrity rate is conditional on accepted fixes and is expected to be 100% because regression/integrity are acceptance gates; it is not a general correctness guarantee. Missing cost rates/source yield null cost, not zero. Scripted token counts are zero because no API call occurs.

## Improvement protocol

`benchmark_v1.json` and `benchmark_v2.json` are historical *known-fix pipeline* reproducibility runs, not AI improvements. The new CLI path performed one FIFO prompt-overhead pilot: input tokens 16,854 → 6,520, both first-attempt fixes. This single-case comparison does not establish a general repair-quality improvement. The optimized inference configuration was frozen before the 24 public and 6 holdout evaluation; holdout results did not drive tuning. Gold, tests and assertions were not modified.

Codex usage is charged against the ChatGPT plan allowance; API cost remains null. Input tokens include cached input tokens. End-to-end timing includes CLI startup, inference and Docker EDA execution on this local machine; this is not an isolated latency experiment. Four public proposals had malformed diff hunks and were rejected, then corrected through feedback; see ISSUE-010. A successful final score does not hide these rejected proposals.

## Completed live evaluation (2026-09-23)

| Split | Fixed | First attempt | Median time | CLI calls |
|---|---:|---:|---:|---:|
| Public | 24/24 | 20/24 | 14.51s | 28 |
| Holdout | 6/6 | 3/6 | 21.39s | 9 |
| Combined | 30/30 | 23/30 | 14.68s | 37 |

Input tokens 234,948 (including 78,848 cached), output tokens 12,223. Seven of 37 proposals (18.9%) were invalid unified diffs, all resolved on the second attempt. Every accepted fix passed real EDA, full regression and integrity checks. Full summary and per-case raw records: [live evidence](../results/live_codex/summary.md). These numbers cover benchmark runs only; setup probes and two demo pilots consumed additional usage.
