# Evidence: case_011_arbiter_connectivity

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: connectivity. Immutable integrity: True.
Reasoning: unspecified; billing: unspecified.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

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

Duration: 1099 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
