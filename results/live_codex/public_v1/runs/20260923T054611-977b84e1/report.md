# Evidence: case_023_alu_width_signedness

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: width_signedness. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Opcode 6 compares unsigned operands, but the expected behavior is signed comparison.

Cast both operands to signed values for opcode 6.

```diff
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -11,1 +11,1 @@
-        3'd6: result = {7'd0, (a < b)};
+        3'd6: result = {7'd0, ($signed(a) < $signed(b))};
```

Regression: PASS

Duration: 12673 ms; Provider calls: 1; tokens in/out: 6238/296.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
