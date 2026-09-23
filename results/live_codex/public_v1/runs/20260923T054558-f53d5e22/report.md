# Evidence: case_022_alu_connectivity

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

The subtraction operands are reversed for op 1.

Change op 1 to subtract b from a, matching the specified behavior exercised by the testbench.

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

Duration: 12894 ms; Provider calls: 1; tokens in/out: 6241/328.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
