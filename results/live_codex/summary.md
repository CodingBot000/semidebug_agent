# Actual Codex CLI benchmark

Model: **gpt-6-sol / low**; CLI 0.156.1; ChatGPT authentication.

| Split | Fixed | First attempt | Median time | Calls | Input tokens | Cached input | Output tokens |
|---|---:|---:|---:|---:|---:|---:|---:|
| Public | 24/24 | 20/24 | 14.51s | 28 | 176,008 | 53,760 | 9,134 |
| Holdout | 6/6 | 3/6 | 21.39s | 9 | 58,940 | 25,088 | 3,089 |
| Overall | 30/30 | 23/30 | 14.68s | 37 | 234,948 | 78,848 | 12,223 |

All accepted fixes passed real Icarus/VVP, Verilator, Yosys, regression and integrity gates. Seven malformed first diffs were rejected and repaired on the second attempt. No final failures; this does not imply correctness for untested inputs. Holdout uses different mutations of the same six design families. Input tokens include the cached subset. Subscription allowance is consumed; API cost is null. Timing includes host CLI and Docker validation and is an observational local measurement.

Full per-case evidence: [public](public_v1/summary.md), [holdout](hidden_v1/summary.md). The model never received evaluator gold. Configuration was fixed before these runs.
