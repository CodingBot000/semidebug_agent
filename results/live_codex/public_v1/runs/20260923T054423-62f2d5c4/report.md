# Evidence: case_014_arbiter_combinational

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

The both-request grant selection is reversed.

Rejected: Hunk truncated or invalid

Swap the grants selected by priority_bit when both requesters assert req.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -5,7 +5,7 @@
     case (req)
         2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
-        2'b11: grant = priority_bit ? 2'b01 : 2'b10;
+        2'b11: grant = priority_bit ? 2'b10 : 2'b01;
         default: grant = 2'b00;
     endcase
```

## Attempt 2

The grant choices for simultaneous requests are reversed; the previous proposal was rejected for an invalid diff hunk, not by RTL validation.

Correct the simultaneous-request selection using a valid one-line unified diff hunk.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -8,1 +8,1 @@
-        2'b11: grant = priority_bit ? 2'b01 : 2'b10;
+        2'b11: grant = priority_bit ? 2'b10 : 2'b01;
```

Regression: PASS

Duration: 30827 ms; Provider calls: 2; tokens in/out: 12942/738.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
