# Evidence: case_022_alu_connectivity

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
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -3,7 +3,7 @@
     result = 8'd0;
     case (op)
         3'd0: result = a + b;
-        3'd1: result = b - a;
+        3'd1: result = a - b;
         3'd2: result = a & b;
         3'd3: result = a | b;
         3'd4: result = a ^ b;
```

Regression: PASS

Duration: 1063 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
