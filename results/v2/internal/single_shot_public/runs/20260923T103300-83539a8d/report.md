# Evidence: case_011_arbiter_connectivity

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: connectivity. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The single-request case for req=2'b01 grants requester 1 instead of requester 0.

Correct the grant for the req=01 case while leaving arbitration and priority updates unchanged.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -3,7 +3,7 @@
 always @* begin
     grant = 2'b00;
     case (req)
-        2'b01: grant = 2'b10;
+        2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
         2'b11: grant = priority_bit ? 2'b10 : 2'b01;
         default: grant = 2'b00;
```

Regression: PASS

Duration: 11147 ms; Provider calls: 1; tokens in/out: 6257/335.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
