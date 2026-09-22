# ISSUE-004 — Final integrity error could mask the recorded provider failure

- Discovered: 2026-09-22 UTC during robustness review.
- Status: Resolved.
- Symptom: if a source/test file disappeared while the provider failed, the finally-block fingerprint calculation could raise and prevent the final report from being saved.
- Reproduction: temporary project + provider double that removes a testbench and raises ProviderError.
- Impact: incomplete failure evidence; never an accepted fix.
- Cause: unguarded filesystem reads during final integrity handling.
- Resolution: catch missing/invalid paths in final fingerprint validation, report INTEGRITY_ERROR, clear success flags, and persist final run/result/report. Also stop on baseline regression infrastructure errors.
- Verification: dedicated E2E regression test `test_removed_original_records_integrity_error`; full final suite evidence recorded in PROGRESS.md.
