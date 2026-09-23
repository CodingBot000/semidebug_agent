# Evidence: case_024_alu_combinational

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

Opcode 5 shifts right instead of left.

Change opcode 5 to perform the left shift expected by the testbench.

```diff
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -7,7 +7,7 @@
         3'd2: result = a & b;
         3'd3: result = a | b;
         3'd4: result = a ^ b;
-        3'd5: result = a >> b[2:0];
+        3'd5: result = a << b[2:0];
         3'd6: result = {7'd0, ($signed(a) < $signed(b))};
         default: result = a;
     endcase
```

Regression: PASS

Duration: 10664 ms; Provider calls: 1; tokens in/out: 6221/342.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
