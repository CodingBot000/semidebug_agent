# Evidence: case_024_alu_combinational

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

Opcode 5 shifts right, but the expected ALU operation shifts left.

Rejected: Hunk truncated or invalid

Change opcode 5 to perform a left shift, matching the expected behavior.

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

## Attempt 2

Opcode 5 shifts right instead of left.

Correct the opcode 5 shift direction and use a valid unified-diff hunk count.

```diff
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -7,6 +7,6 @@
         3'd2: result = a & b;
         3'd3: result = a | b;
         3'd4: result = a ^ b;
-        3'd5: result = a >> b[2:0];
+        3'd5: result = a << b[2:0];
         3'd6: result = {7'd0, ($signed(a) < $signed(b))};
         default: result = a;
```

Regression: PASS

Duration: 28381 ms; Provider calls: 2; tokens in/out: 12875/743.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
