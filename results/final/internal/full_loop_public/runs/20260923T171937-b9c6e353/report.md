# Evidence: case_024_alu_combinational

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

Opcode 5 shifts in the wrong direction.

Rejected: Hunk truncated or invalid

Change only the opcode-5 shift direction at rtl/alu.v:10.

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

Opcode 5 shifts in the wrong direction.

Change opcode 5 at rtl/alu.v:10 to shift left. The diff uses the correct six-line hunk count against the original baseline.

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

Duration: 13567 ms; Provider calls: 2; tokens in/out: 6734/725.
Estimated cost: 0.016786799999999998.

Scripted providers and replay output are not live AI benchmark results.
