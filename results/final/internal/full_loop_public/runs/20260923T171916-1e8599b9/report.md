# Evidence: case_022_alu_connectivity

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: connectivity. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Subtraction operands are reversed for op 1.

Change only the op-1 subtraction in rtl/alu.v:6 to match the checked operand order.

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

Duration: 6341 ms; Provider calls: 1; tokens in/out: 3160/312.
Estimated cost: 0.0074744.

Scripted providers and replay output are not live AI benchmark results.
