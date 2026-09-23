# Evidence: case_015_arbiter_combinational

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

The no-request case incorrectly grants requester 0.

Rejected: Hunk truncated or invalid

Make the unmatched no-request case produce no grant.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -6,7 +6,7 @@
         2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
         2'b11: grant = priority_bit ? 2'b10 : 2'b01;
-        default: grant = 2'b01;
+        default: grant = 2'b00;
     endcase
```

## Attempt 2

The no-request case falls through to a grant of requester 0.

Add an explicit no-request case while preserving the existing default behavior for unknown-valued requests.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -6,5 +6,6 @@
         2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
         2'b11: grant = priority_bit ? 2'b10 : 2'b01;
+        2'b00: grant = 2'b00;
         default: grant = 2'b01;
     endcase
```

Regression: PASS

Duration: 25782 ms; Provider calls: 2; tokens in/out: 12873/753.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
