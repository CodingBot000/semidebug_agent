# External benchmark protocol (frozen before model evaluation)

Frozen on 2026-09-23. No ChipBench model call was made before this selection and protocol were written. The selection manifest is `external/chipbench/selection_manifest.json`.

## Source and selection

- Upstream: [ChipBench](https://github.com/zhongkaiyu/ChipBench), commit `b4ba3a06759804ec88c26c3cf15b28b9a90b3443`, MIT [license](https://github.com/zhongkaiyu/ChipBench/blob/main/LICENSE).
- Task: `Verilog Debugging/dataset_debug_zero_shot_*`. Select the first three prompt filenames in lexicographic order in each of `timing`, `assignment`, `arithmetic`, `state_machine`: 12 cases total.
- Each selected prompt must have matching `_ref.sv` and `_test.sv`; a missing file aborts selection. The manifest records SHA256 for every selected file.
- Keep all 12 selected cases in the denominator. Do not substitute another case after seeing compatibility, baseline or model results. Report selected, compatible, attempted, fixed, first-attempt fixed, semantic retry rescued, unsupported, baseline-pass, model failure and infrastructure error separately.

## Visibility and acceptance

- The model may see the problem statement, buggy `TopModule` source and non-answer-bearing baseline diagnostics. It must not see `RefModule`, `_ref.sv`, `_test.sv`, the reference solution, official mismatch details or upstream development history that could reveal a solution.
- The adapter must extract the buggy `TopModule` from the prompt into a mutable RTL file without changing its content. The prompt, source and evaluator file hashes must match the frozen manifest.
- An independent validator compiles the candidate with the selected upstream `_ref.sv` and `_test.sv` using Icarus `-g2012`, runs VVP, and parses the upstream test's `Mismatches: N in S samples` result. Acceptance requires compilation and simulation exit zero, exactly one result line, `N=0`, `S>0`, no timeout marker, an allowed exact RTL patch and unchanged evaluator files. Local lint/synthesis checks are additional where the selected design supports them; report any skipped check.
- Qualification occurs before inference. A selected triplet whose reference cannot pass the pinned simulator is `unsupported`; a buggy baseline that already passes is `baseline_pass`. Neither is quietly removed or replaced.
- Every retry starts from the original buggy RTL. A failed candidate's official diagnostics remain in local evidence; model feedback may contain only a bounded, answer-free failure summary. Gold RTL and evaluator test source are never sent to the provider.

## Reproduction and redistribution

Clone ChipBench at the exact commit, rerun `scripts/freeze_chipbench_selection.py`, and compare all 36 SHA256 values with the manifest before importing. The submission ZIP ships this manifest and adapter, not the full external dataset or reference files. The upstream license and commit must appear in `docs/THIRD_PARTY.md`.
