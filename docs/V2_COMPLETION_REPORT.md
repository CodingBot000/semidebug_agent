# SemiDebug Agent V2 completion report

Completed locally on 2026-09-23. This report is outside the submission ZIP so its recorded ZIP hash does not change the archive being hashed.

## Implemented changes

- Froze V1 at `afc0582e08ba5463a0d4e35630dbebc7432028d4` with local tag `semidebug-v1-baseline`; the checked V1 result hashes remain unchanged.
- Added `benchmark_v2/` without altering V1 mutations. Visible target and evaluator-only regression now use separate testbench sources; the regression runs longer vectors under seeds 17 and 103.
- Limited provider context to explicitly visible files and reduced hidden regression feedback to gate/status. Detailed evaluator output remains in local run artifacts. Added end-to-end leakage isolation coverage.
- Recorded stable parse/guard/EDA/regression retry reasons and separate format versus semantic rescue metrics.
- Frozen 12 ChipBench cases and 36 upstream file hashes in commit `9e0bc2b` before model execution. Added a hash-checking importer and an adapter that uses the official mismatch test without exposing reference/test source to the model.
- Added internal and external result analysis scripts, selected representative raw traces, V2 documentation and a curated submission packager.
- Submission hardening changed the default live and scripted demo to an independent V2 FIFO fixture with one visible target source and two distinct evaluator-only regression sources. Default replay now shows a V2 semantic retry; `--replay-v1` keeps the historical sample accessible.
- Added Git-derived [PROVENANCE.json](../results/v2/PROVENANCE.json), captured command logs and a machine-readable [verification summary](../results/v2/verification/verification_summary.json). Source commit `b145999d2540cd955b5f8afdd6382e67fe66a134` precedes provenance; packaging source commit is `fdd135b56cd9449c188e8be842f969e2cba6b08b`. The final commit cannot be embedded in a tracked file that belongs to itself.

## Evaluation protocol and actual results

The V2 internal corpus passed pre-model qualification: gold 6/6, broken baseline failures 30/30. Known-fix **scripted** pipeline validation passed 30/30 and is not counted as AI repair.

| Actual model run | Fixed | First attempt | Retry detail |
|---|---:|---:|---|
| V2 internal full loop, 30 cases | 30/30 | 23/30 | Seven rescued after malformed diffs; zero semantic rescues |
| V2 internal independent one-shot | 24/30 | 24/30 | Six final failures |
| Preselected external ChipBench, 12 compatible cases | 5/12 | 2/12 | Three semantic rescues; seven final failures |

External failures: `arithmetic_Prob002`, `arithmetic_Prob006`, `assignment_Prob003`, `state_machine_Prob012`, and all three selected timing cases. Five stopped at `MAX_RETRY`; two at `PATCH_REJECTED`. None was removed from the 12-case denominator. The successful external [semantic retry](../results/v2/evidence/semantic_retry/report.md) and [final failure](../results/v2/evidence/final_failure/report.md) preserve the attempted diffs and EDA outcome. Full methodology, tokens, timing and all case results are in [V2_EVALUATION.md](V2_EVALUATION.md).

## Verification

- Source `make lint` passed; source Docker `make test-all` passed **109 tests**. Actual exit codes and logs are saved in `results/v2/verification/`.
- Docker dataset qualification: gold 6/6; broken 30/30. Known-fix pipeline: 30/30.
- ChipBench reference and official test qualification: 12/12 compatible, all 12 buggy baselines failed.
- The V2 scripted demo recorded a failing baseline, accepted patch, compile/simulation/lint/synthesis passes, hidden regression passes, integrity pass and final `FIXED`. The model request visibility test found no hidden source path or marker.
- Submission ZIP was extracted with `unzip` into a clean local directory. Its `bootstrap.sh`, V2 replay, V2 scripted real-EDA demo, lint and all **109 tests** passed. [Clean extraction log](../results/v2/verification/clean_extract.log) is outside the ZIP to avoid changing the ZIP hash after verification.
- [Package scan](../results/v2/verification/package_scan.json) checked ZIP members, common secret patterns, local absolute paths, Markdown relative links and size. External source/reference files, credentials, `.env`, Git metadata, internal journal and duplicate full run directories are excluded. This scan is outside the ZIP for the same hash-cycle reason.
- One intermediate full-suite run failed because the package-scan unit test had not yet listed two new required demo evidence files. The test was corrected and the failed [log](../results/v2/verification/test_all_pre_fix_failure.log) was preserved; the final full suite passed. An initial Python `zipfile.extractall` check did not restore shell execute bits, so clean extraction was repeated with the documented `unzip` command and passed.

## Document changes

`README.md`, `PORTFOLIO_EVIDENCE.md` and `QUICKSTART.md` now lead with the problem, measured V2 outcomes and reproduction. `docs/ARCHITECTURE.md` explains model, patch, credential and evaluator boundaries. `docs/BENCHMARK.md` keeps V1 historical methodology; `docs/V2_EVALUATION.md` owns V2 measurements; `docs/EXTERNAL_BENCHMARK_PROTOCOL.md` owns preselection; `docs/LIMITATIONS.md` and `docs/THIRD_PARTY.md` own caveats and attribution. Development audits remain in `docs/internal/`. The repository was confirmed private; ZIP guidance does not require GitHub access.

## Submission package

- Path: `dist/SemiDebug_Agent_V2_Submission.zip`
- Size: **707,252 bytes** (642 files; below 50 MB)
- SHA256: `f15c1602ec46e1afc9d6e3804c95d4d812ce735d3eefc46d6225f2e9f4bcb5b2`
- Checksum file: `dist/SemiDebug_Agent_V2_Submission.sha256`
- Included evidence: V1 summaries, V2 qualification and per-case result JSON/CSV, the 12-case external manifest, five representative full traces, Git provenance, and final lint/test/V2 scripted-demo logs and summary. Full external datasets and reference solutions are not included. Package scan and clean extraction evidence remain alongside the repository's verification artifacts, outside this immutable ZIP.

## Remaining limits

HWE-bench was researched but not executed; its repository-level harness, separate dataset and per-PR images require another integration and resource assessment. No HWE success number is claimed. The external 12 cases are a small sample, model pretraining exposure is unknown, and finite EDA tests are not formal equivalence or production verification. The OpenAI-compatible API provider remains tested with mock HTTP, not measured live. No remote release, visibility change or push was performed; V2 commits and the ZIP are local.

The [final hardening audit](../results/v2/verification/final_audit.json) checked V1/V2 raw-file SHA256 and committed raw-tree IDs before and after this work, Git ancestry, the frozen ChipBench manifest, demo source separation, package scan and clean extraction. Every check passed. No existing benchmark raw result was changed.
