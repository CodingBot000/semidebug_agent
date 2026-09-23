# Evidence: case_014_arbiter_combinational

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The simultaneous-request grant selection has reversed priority polarity.

Reverse the two grant choices for simultaneous requests to match the reference priority behavior.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -8 +8 @@
-        2'b11: grant = priority_bit ? 2'b01 : 2'b10;
+        2'b11: grant = priority_bit ? 2'b10 : 2'b01;
```

Regression: PASS

Duration: 10383 ms; Provider calls: 1; tokens in/out: 6257/311.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
