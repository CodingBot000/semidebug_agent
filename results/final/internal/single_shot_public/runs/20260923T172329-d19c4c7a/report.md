# Evidence: case_024_alu_combinational

**MAX_RETRY** — provider `live-openai-api`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

Opcode 5 shifts in the wrong direction.

Rejected: Hunk truncated or invalid

Change opcode 5 from right shift to left shift at rtl/alu.v:10.

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
```

Duration: 5175 ms; Provider calls: 1; tokens in/out: 3160/361.
Estimated cost: 0.004247399999999999.

Scripted providers and replay output are not live AI benchmark results.
