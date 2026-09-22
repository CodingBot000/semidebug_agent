# ISSUE-006 — Git whitespace warnings on generated evidence

- Discovered: 2026-09-22 UTC while reviewing staged artifacts.
- Status: Resolved.
- Symptom: `git diff --cached --check` flagged standard CSV CRLF separators and blank trailing lines in captured EDA logs.
- Impact: noisy diff review, not a code/test failure.
- Cause: generic source whitespace rules applied to generated evidence formats.
- Resolution: `.gitattributes` permits CSV CRLF and preserves whitespace in captured log files. Raw tool content remains intact; source lint and format rules are unchanged.
- Verification: rerun staged whitespace check before final publication.
