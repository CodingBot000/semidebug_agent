# Benchmark methodology and measured results

## Dataset

Six original designs, each with five distinct mutations: counter/timer, four-entry synchronous FIFO, two-input round-robin arbiter, three-state controller, eight-operation ALU and enabled rising-edge pulse detector. Category coverage includes syntax, width/signedness, reset, sequential logic, boundary, FSM, combinational and connectivity faults. There are 24 public and 6 holdout cases. Only 2/30 are syntax faults; most require functional correction.

`evaluator/build_dataset.py` first constructs each gold RTL and testbench, then runs the target plus two longer regression seeds through real EDA. Only after all six gold designs pass does it emit mutations. Each mutation is validated and must reproduce a failure; infrastructure errors are not accepted as a detected bug. Testbenches use reference state/scoreboards, directed boundary vectors and seeded pseudorandom cases. Target seed is 7; regression seeds are 17 and 103.

Gold and exact mutation definitions remain in evaluator/. Runtime loading copies only manifest-listed RTL, tests, metadata and the manifest. Prompt context includes only selected RTL and read-only testbench source, never gold, mutation definitions or split labels. Holdout means different mutations of the same design families, not secret data or unseen designs.

## Actual measurements

- Dataset qualification: **6/6 gold designs passed all target and regression checks**.
- Broken qualification: **30/30 mutations reproduce an EDA failure**.
- Known-fix pipeline acceptance: **30/30 fixed on first supplied patch**, full regression and immutable integrity passed. Median measured wall time was **360.5 ms** in the first run; two scripted provider calls per case, no API tokens. This tests the implementation against known fixes and does **not** measure AI repair success.
- Live AI benchmark: **not run**, missing API credentials. AI success rate, failure distribution, live latency, token use and cost are unknown.

Raw dataset records: `results/dataset_audit.json`. Pipeline summary/rows: `results/benchmark_summary.json`, `results/benchmark_results.json`, `results/benchmark_results.csv`. Each row includes before/after validation, proposals, statuses and hashes. Example full traces are under sample_run/, retry_run/, failed_run/.

## Metrics

Repair success and first-attempt rates divide accepted fixes by all cases. Invalid patch rate divides guard rejections by generated proposals. Retry count is max(iteration-1, 0); median time includes validation and provider time. Regression integrity rate is conditional on accepted fixes and is expected to be 100% because regression/integrity are acceptance gates; it is not a general correctness guarantee. Missing cost rates/source yield null cost, not zero. Scripted token counts are zero because no API call occurs.

## Improvement protocol

No model/prompt tuning or claimed AI improvement was performed without live results. Phase 8 live before/after comparison remains blocked by ISSUE-001. `benchmark_v1.json` and `benchmark_v2.json` record a repeat of the *known-fix pipeline*, explicitly labelled as reproducibility checks. Do not interpret them as improved AI performance.

When credentials are supplied, run public benchmark, analyze actual failures, record one justified change in DECISIONS.md, rerun the same cases/model/limits, and finally run holdout once. Preserve both raw outputs and failed cases. Never tune tests, assertions or expected results to make a patch pass.
