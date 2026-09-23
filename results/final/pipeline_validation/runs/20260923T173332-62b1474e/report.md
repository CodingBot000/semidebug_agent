# Evidence: case_025_alu_syntax

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: syntax. Immutable integrity: True.
Reasoning: unspecified; billing: unspecified.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | FAIL | PASS |
| simulation | NOT RUN | PASS |
| lint | FAIL | PASS |
| synthesis | FAIL | PASS |

## Attempt 1

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

```diff
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -6,7 +6,7 @@
         3'd1: result = a - b;
         3'd2: result = a & b;
         3'd3: result = a | b;
-        3'd4: result = a ^ nonexistent;
+        3'd4: result = a ^ b;
         3'd5: result = a << b[2:0];
         3'd6: result = {7'd0, ($signed(a) < $signed(b))};
         default: result = a;
```

Regression: PASS

Duration: 1000 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
