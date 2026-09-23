# Evaluation — 2026-09-23 UTC

The final SemiDebug evaluation asks whether an RTL repair survives tests the model did not receive, whether retry feedback changes outcomes, and whether the system works outside its original fixtures. The numbers below come from saved OpenAI API per-run JSON. [Raw evidence index](../results/final/README.md) · [verification report](../VERIFICATION_REPORT.md).

## Protocol and visibility

The final internal corpus under `benchmark_v2/` contains 30 buggy RTL cases. Each visible target test uses the shorter seed-7 sequence. Each evaluator-only regression has its own source, a longer sequence, seeds 17/103 and additional directed vectors. The provider context includes mutable RTL and visible target source; hidden source, hidden file paths and detailed hidden mismatch output stay in evaluator artifacts. A real EDA end-to-end test checks that a hidden source marker never reaches the provider request.

Before model evaluation, all six reference designs passed target and hidden regression, and all 30 buggy cases reproduced a failure in the pinned Docker toolchain. A separate **known-fix scripted** pipeline check accepted 30/30; this is a system qualification, not model accuracy. [Dataset audit](../results/final/dataset_audit.json) · [pipeline summary](../results/final/pipeline_validation_summary.json).

The internal model runs used the OpenAI Chat Completions API with `gpt-6-sol`, reasoning effort `low`, Structured Outputs and the same Docker Icarus 11.0, Verilator 5.006 and Yosys 0.23 gates. Each attempt requests one combined diagnosis and patch. A one-shot run allows one patch; a full-loop run allows three. Timing includes API inference and Docker checks. Estimated USD uses the [official model prices](https://developers.openai.com/api/docs/models/gpt-6-sol) recorded on 2026-09-24: $2/M uncached input, $0.20/M cached input and $10/M output.

## Internal results and ablation

| Condition | Fixed | First proposal accepted | Calls | Median end-to-end | Input / cached / output tokens | Estimated USD |
|---|---:|---:|---:|---:|---:|---:|
| Full loop, public + holdout | 29/30 | 22/30 | 38 | 7.43 s | 138,552 / 41,496 / 13,621 | $0.339 |
| Independently rerun one-shot | 23/30 | 23/30 | 30 | 6.25 s | 104,206 / 104,116 / 10,377 | $0.125 |

Within the **same full-loop trajectories**, seven cases were rescued after the first proposal. All seven first proposals failed strict diff parsing; none was a semantic RTL candidate rejected by EDA. One additional case ended at `PATCH_REJECTED`. The separate one-shot run produced six fewer final fixes than the full-loop run. It samples new, non-deterministic model outputs, so its 23/30 result is not the exact first proposal from each full-loop trajectory. The paired 22/30 to 29/30 result establishes format recovery in this corpus, not a semantic feedback gain. [Per-case comparison](../results/final/internal/comparison.md) · [raw comparison](../results/final/internal/comparison.json).

## Frozen external ChipBench evaluation

The [selection protocol](EXTERNAL_BENCHMARK_PROTOCOL.md) and [12-case manifest](../external/chipbench/selection_manifest.json) were frozen before any external model call. It takes the first three lexicographically sorted zero-shot prompts in each of timing, assignment, arithmetic and state-machine categories from the pinned upstream ChipBench revision `b4ba3a06759804ec88c26c3cf15b28b9a90b3443`. Source hashes are recorded. The importer provides the problem description and buggy `TopModule` to the model; upstream `RefModule` and `_test.sv` are evaluator-only. The upstream mismatch test, parsed as `Mismatches: 0 in N samples`, is the acceptance gate after compile, lint and synthesis checks.

Pre-model qualification found all 12 compatible: each reference passed the gates and each buggy baseline failed the official test. No case was replaced or dropped. External evaluation used the same OpenAI API `gpt-6-sol / low` configuration and Docker toolchain. The [verification report](../VERIFICATION_REPORT.md) records the executed source checks.

| Measure | Result |
|---|---:|
| Selected / compatible / attempted | 12 / 12 / 12 |
| Final fixed | 6/12 |
| First-attempt fixed | 1/12 |
| Rescued after a semantically failing candidate | 3 |
| Final failures | 6: two `MAX_RETRY`, four `PATCH_REJECTED` |
| Median end-to-end time | 21.56 s |
| Model calls | 26 |
| Input / cached / output tokens | 131,937 / 28,392 / 16,695 |
| Estimated USD | $0.380 |

By category, arithmetic fixed 2/3, assignment 2/3, state machine 2/3 and timing 0/3. There were five official regression rejections and 15 invalid patch attempts across all attempts. These are attempt counts, not case counts. [All selected outcomes](../results/final/external/chipbench/evaluation.md) · [per-case data](../results/final/external/chipbench/evaluation.json) · [raw API results](../results/final/external/chipbench/live/results.json).

## Representative evidence

- [First-shot success](../results/final/evidence/first_shot/report.md): an internal syntax case passed target, independent checks and hidden regression on attempt one.
- [Format retry](../results/final/evidence/format_retry/report.md): an internal FIFO proposal failed diff parsing; the second proposal passed all gates.
- [Semantic retry](../results/final/evidence/semantic_retry/report.md): external arithmetic case `Prob001` first recovered from a diff parse failure, then had a candidate rejected by the official regression before a third patch passed. Detailed evaluator mismatch output stayed out of the API request.
- [Final failure](../results/final/evidence/final_failure/report.md): external timing case `Prob002` had one official-regression failure between two diff parse failures, then stopped at the iteration limit.
- [One-shot failure](../results/final/evidence/one_shot_failure/report.md): the independent internal one-shot condition stopped after an invalid first diff.

## Interpretation and limits

The external result is more informative than the internal 29/30 result: 6/12 selected external repairs passed, and both successful semantic retries and final failures are visible. ChipBench is external to this project's self-made corpus; the model's possible pretraining exposure is unknown. The 12 selected cases are a small sample. Internal holdout cases use different mutations of the same six designs, not independent design families. Finite simulation, lint and synthesis sanity do not establish formal equivalence or production silicon correctness. HWE-bench was not executed. See [limitations](LIMITATIONS.md).
