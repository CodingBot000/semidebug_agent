# Evidence: case_023_alu_width_signedness

**MAX_RETRY** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: width_signedness. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

Opcode 6 uses an unsigned comparison, but the expected behavior is signed comparison.

Rejected: Hunk truncated or invalid

Cast both operands to signed 8-bit values for opcode 6 while retaining the one-bit result formatting.

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
```

Duration: 10338 ms; Provider calls: 1; tokens in/out: 6218/334.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
