# Evidence: case_023_alu_width_signedness

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: width_signedness. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Opcode 6 compares unsigned operands instead of signed operands.

Cast both operands to signed values for the opcode-6 comparison at rtl/alu.v:11.

```diff
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -8,7 +8,7 @@
         3'd3: result = a | b;
         3'd4: result = a ^ b;
         3'd5: result = a << b[2:0];
-        3'd6: result = {7'd0, (a < b)};
+        3'd6: result = {7'd0, ($signed(a) < $signed(b))};
         default: result = a;
     endcase
 end
```

Regression: PASS

Duration: 6840 ms; Provider calls: 1; tokens in/out: 3155/430.
Estimated cost: 0.0049364.

Scripted providers and replay output are not live AI benchmark results.
