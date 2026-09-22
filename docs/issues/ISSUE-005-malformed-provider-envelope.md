# ISSUE-005 — Non-object provider response envelope

- Discovered: 2026-09-22 UTC during provider boundary review.
- Status: Resolved.
- Symptom: a successful HTTP response containing a JSON array instead of the required response object could raise AttributeError before schema validation.
- Impact: malformed provider output could escape the structured ProviderError path.
- Cause: JSON decoding accepts non-object values while the adapter expected mapping methods.
- Resolution: normalize this malformed envelope into ProviderError; never apply a patch from it.
- Verification: added array response to the invalid-output parametrized test; targeted provider tests pass. No test expectations were weakened.
