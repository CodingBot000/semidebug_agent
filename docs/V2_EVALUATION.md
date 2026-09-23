# V2 evaluation — 2026-09-23 UTC

SemiDebug V2 asks whether an RTL repair survives tests the model did not receive, whether retry feedback changes outcomes, and whether the system works outside its original fixtures. The numbers below come from saved per-run JSON, not copied from the V1 headline. [Raw evidence index](../results/v2/README.md) · [environment](../results/v2/environment.json).

## Protocol and visibility

V1 remains frozen at tag `semidebug-v1-baseline`. V2 generated a separate `benchmark_v2/` from the same 30 buggy RTL cases. Each visible target test uses the shorter seed-7 sequence. Each evaluator-only regression has its own source, a longer sequence, seeds 17/103 and additional directed vectors. The provider context includes mutable RTL and visible target source; hidden source, hidden file paths and detailed hidden mismatch output stay in evaluator artifacts. A real EDA end-to-end test checks that a hidden source marker never reaches the provider request.

Before model evaluation, all six reference designs passed target and hidden regression, and all 30 buggy cases reproduced a failure in the pinned Docker toolchain. A separate **known-fix scripted** pipeline check accepted 30/30; this is a system qualification, not model accuracy. [Dataset audit](../results/v2/dataset_audit.json) · [pipeline summary](../results/v2/pipeline_validation_summary.json).

The internal model runs used Codex CLI `0.156.1`, `gpt-6-sol`, reasoning effort `low`, ChatGPT login and the same Docker Icarus 11.0, Verilator 5.006 and Yosys 0.23 gates. A one-shot run allows one patch; a full-loop run allows three. Timing includes host inference and Docker checks. Subscription usage is recorded as tokens; dollar cost is not inferred. Internal source commit: `099188fa0b5dee64fe9ec3306ff559101ad728d3`.

## Internal results and ablation

| Condition | Fixed | First proposal accepted | Calls | Median end-to-end | Input / output tokens |
|---|---:|---:|---:|---:|---:|
| Full loop, public + holdout | 30/30 | 23/30 | 37 | 11.66 s | 235,559 / 12,409 |
| Independently rerun one-shot | 24/30 | 24/30 | 30 | 11.01 s | 187,940 / 9,591 |

Within the **same full-loop trajectories**, seven cases were rescued after the first proposal. All seven first proposals failed strict diff parsing; none was a semantic RTL candidate rejected by EDA. The separate one-shot run produced six fewer final fixes than the full-loop run. It samples new, non-deterministic model outputs, so its 24/30 result is not the exact first proposal from each full-loop trajectory. The paired 23/30 to 30/30 result establishes format recovery in this corpus, not a semantic feedback gain. [Per-case comparison](../results/v2/internal/comparison.md) · [raw comparison](../results/v2/internal/comparison.json).

## Frozen external ChipBench evaluation

The [selection protocol](EXTERNAL_BENCHMARK_PROTOCOL.md) and [12-case manifest](../external/chipbench/selection_manifest.json) were committed before any external model call. It takes the first three lexicographically sorted zero-shot prompts in each of timing, assignment, arithmetic and state-machine categories from upstream commit `b4ba3a06759804ec88c26c3cf15b28b9a90b3443`. Source hashes are recorded. The importer provides the problem description and buggy `TopModule` to the model; upstream `RefModule` and `_test.sv` are evaluator-only. The upstream mismatch test, parsed as `Mismatches: 0 in N samples`, is the acceptance gate after compile, lint and synthesis checks.

Pre-model qualification found all 12 compatible: each reference passed the gates and each buggy baseline failed the official test. No case was replaced or dropped. External evaluation used the same `gpt-6-sol / low` model and Docker toolchain, with source commit `a332e03a261f62b569ed86d3039e426bdd58185f` and [recorded environment](../results/v2/external/chipbench/environment.json).

| Measure | Result |
|---|---:|
| Selected / compatible / attempted | 12 / 12 / 12 |
| Final fixed | 5/12 |
| First-attempt fixed | 2/12 |
| Rescued after a semantically failing candidate | 3 |
| Final failures | 7: five `MAX_RETRY`, two `PATCH_REJECTED` |
| Median end-to-end time | 48.94 s |
| Model calls; input / output tokens | 28; 201,834 / 20,934 |

By category, arithmetic fixed 1/3, assignment 2/3, state machine 2/3 and timing 0/3. There were 11 official regression rejections and 12 invalid patch attempts across all attempts. These are attempt counts, not case counts. [All selected outcomes](../results/v2/external/chipbench/evaluation.md) · [per-case data](../results/v2/external/chipbench/evaluation.json) · [raw live results](../results/v2/external/chipbench/live/results.json).

## Representative evidence

- [First-shot success](../results/v2/evidence/first_shot/report.md): an internal syntax case passed target, independent checks and hidden regression on attempt one.
- [Format retry](../results/v2/evidence/format_retry/report.md): an internal ALU proposal failed diff parsing; the second proposal passed all gates.
- [Semantic retry](../results/v2/evidence/semantic_retry/report.md): external arithmetic case `Prob001` passed target compile/lint/synthesis on attempt one but failed the official regression; a different second patch passed. Its detailed evaluator mismatch output stayed out of the provider request.
- [Final failure](../results/v2/evidence/final_failure/report.md): external arithmetic case `Prob002` failed the official regression on attempts one and three, with a diff parse failure between them, then stopped at the iteration limit.
- [One-shot failure](../results/v2/evidence/one_shot_failure/report.md): the independent internal one-shot condition stopped after an invalid first diff.

## Interpretation and limits

The external result is more informative than the internal 30/30 headline: 5/12 selected external repairs passed, and both successful semantic retries and final failures are visible. ChipBench is external to this project's self-made corpus; the model's possible pretraining exposure is unknown. The 12 selected cases are a small sample. Internal holdout cases use different mutations of the same six designs, not independent design families. Finite simulation, lint and synthesis sanity do not establish formal equivalence or production silicon correctness. HWE-bench was researched but not executed; see [feasibility](HWE_BENCH_FEASIBILITY.md) and [limitations](LIMITATIONS.md).
