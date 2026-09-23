# Evidence: case_023_alu_width_signedness

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: width_signedness. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

Opcode 6 uses an unsigned comparison, but the expected result is a signed comparison.

Rejected: Hunk truncated or invalid

Cast both operands to signed values for opcode 6 while retaining the one-bit comparison result.

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

## Attempt 2

Opcode 6 compares unsigned operands, but the expected comparison is signed.

Compare both operands as signed 8-bit values for opcode 6. The diff is against the original source and uses a corrected five-line hunk.

```diff
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -8,5 +8,5 @@
         3'd3: result = a | b;
         3'd4: result = a ^ b;
         3'd5: result = a << b[2:0];
-        3'd6: result = {7'd0, (a < b)};
+        3'd6: result = {7'd0, ($signed(a) < $signed(b))};
         default: result = a;
```

Regression: PASS

Duration: 22890 ms; Provider calls: 2; tokens in/out: 12838/721.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
