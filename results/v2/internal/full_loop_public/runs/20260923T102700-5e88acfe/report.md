# Evidence: case_021_alu_combinational

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

Opcode 0 incorrectly subtracts instead of adding.

Change only opcode 0 to perform 8-bit addition, leaving opcode 1 as subtraction.

```diff
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -2,7 +2,7 @@
 always @* begin
     result = 8'd0;
     case (op)
-        3'd0: result = a - b;
+        3'd0: result = a + b;
         3'd1: result = a - b;
         3'd2: result = a & b;
         3'd3: result = a | b;
```

Regression: PASS

Duration: 13720 ms; Provider calls: 1; tokens in/out: 6223/311.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
