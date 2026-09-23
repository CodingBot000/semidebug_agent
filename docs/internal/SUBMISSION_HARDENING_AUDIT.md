# Final submission hardening audit

Observed 2026-09-23 before hardening edits. The user-supplied `docs/update/v2/` instruction was the only untracked path; no tracked file had local changes. Work moved from `main` to new local branch `submission-hardening` at `0143a378b6dba5da1189134cdaef25e2dd963b30`. `main` was four commits ahead of `origin/main`. No remote push or visibility change is part of this work.

## Frozen history and source evidence

| Role | Git commit |
|---|---|
| V1 tag `semidebug-v1-baseline` (peeled commit) | `afc0582e08ba5463a0d4e35630dbebc7432028d4` |
| ChipBench selection manifest introduced | `9e0bc2b3190ba2f1db0ffd391081240730b5f89d` |
| V2 internal evaluation source | `099188fa0b5dee64fe9ec3306ff559101ad728d3` |
| V2 external evaluation source | `a332e03a261f62b569ed86d3039e426bdd58185f` |
| Pre-hardening V2 submission HEAD | `0143a378b6dba5da1189134cdaef25e2dd963b30` |

`git merge-base --is-ancestor` returned exit 0 for V1 → pre-hardening HEAD, selection → external evaluation source, internal evaluation source → pre-hardening HEAD, and external evaluation source → pre-hardening HEAD. The selection manifest SHA256 is `827371795f7def7709c74f58ae0358e4476f46326227e3cfc88adf04fd4b6874` both at introduction commit and in the working tree.

## Raw-result preservation baseline

The committed Git tree object IDs at pre-hardening HEAD are:

- `results/live_codex/`: `a72334b98cb01c2494c5c33a68aefafcd09c98ab`
- `results/v2/internal/`: `737212e5b9663af0edcd4cf68c8fdc88a3849297`
- `results/v2/external/`: `97513240fedc9be459810bc61e44a79444d57c8e`

Critical file SHA256 before work:

| File | SHA256 |
|---|---|
| `results/live_codex/summary.md` | `8682b2a4c85c61eb3c67eb8286f59038cd5390a769db50780d9a3220e0aa05e7` |
| `results/v2/internal/comparison.json` | `77c3073d4e42e427797ae5e1431ac43445bd9c0c7e3b243fcfa710e8d42cf2a8` |
| `results/v2/external/chipbench/evaluation.json` | `0767744b74dc555d5f9a0d7cfbab308460374b2e7a6158d498db23234e5897aa` |
| `results/v2/internal/full_loop_public/results.json` | `1055385306ee09363d7ece5a72580e06f569ca99add034da5c2df051d2812308` |
| `results/v2/internal/full_loop_hidden/results.json` | `e4e69fdc964d3fcd8513ec5296980d7cac44a4ca32c2e480d9c060ab673f364b` |
| `results/v2/external/chipbench/live/results.json` | `d1fb684ebe17ab2fc176446292ed73b19433eaf4cd19fcc7af52e849b2031a75` |

## Current gaps

1. `scripts/run_demo.sh` defaults to `examples/fifo_off_by_one`, whose target and regression share `tb/fifo_tb.v`. Scripted mode uses the same V1 fixture. Replay uses V1 `results/sample_run/result.json`.
2. The submission ZIP has no Git-derived `PROVENANCE.json`.
3. Local lint/106-test/ZIP claims were made in prose but no V2 verification log bundle or machine-readable summary was included.
4. `scripts/package_v2_submission.py` is the active `make package` target; the older `scripts/package_submission.py` remains a historical V1 packager. The active packager currently excludes provenance and verification files.

## Implementation decision

Copy a V2 FIFO case into an independent `examples/` fixture, with explicit `prompt_visible` and separate target plus two evaluator-only regression source files. Keep the core validation gates unchanged. Use a source commit followed by a provenance/package commit: the tracked provenance records the source commit and explains why a self-referential final commit cannot be embedded in the same file. The final completion report outside the ZIP records the packaging commit and ZIP hash. Package-internal verification logs will be captured before packaging; `package_scan.json` and `clean_extract.log` will be kept outside the ZIP because they describe the finished archive and would otherwise create a hash cycle.

## Resolution

The V2 default demo source commit is `b145999d2540cd955b5f8afdd6382e67fe66a134`; the extracted-package verifier was added in `7e13e28eefa1a3b7dda314e7b5b602ae051f929e`; the final package content commit is `bec245665b08663d025bf1907fe91b607a9af821`. `results/v2/PROVENANCE.json` points to the non-self-referential application source and verifies V1, selection and evaluation ancestry. The final ZIP is 708,248 bytes, 643 files, SHA256 `2d74ff57f241cdda7b755839724d30461cef63d36d9bcff672dddbcc9e57d61d`. Package scan and clean extraction evidence are generated after ZIP creation and remain outside it; the included `SUBMISSION_GUIDE.md` tells reviewers how to reproduce extraction checks with the included verifier.

The final scripted V2 demo, lint and 109-test suite passed. The ZIP scanner and clean extraction also passed. The first test run after adding two required evidence files failed because its synthetic ZIP fixture lacked those files; the failed log was preserved, then the test and full suite passed. The first clean-extraction harness used Python `zipfile.extractall`, which dropped script execute bits; the documented `unzip` workflow passed. A later summary parser expected a different PASS label and initially marked a successful verifier run as FAIL; the saved raw log was parsed again and the summary now records PASS. `results/v2/verification/final_audit.json` programmatically confirms the protected V1/V2 raw hashes and Git tree IDs did not change.
