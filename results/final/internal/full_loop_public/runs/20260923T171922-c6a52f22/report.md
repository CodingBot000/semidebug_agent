# Evidence: case_023_alu_width_signedness

**PATCH_REJECTED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: width_signedness. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: Two consecutive invalid patches

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | NOT RUN |
| simulation | FAIL | NOT RUN | NOT RUN |
| lint | PASS | NOT RUN | NOT RUN |
| synthesis | PASS | NOT RUN | NOT RUN |

## Attempt 1

Opcode 6 compares unsigned operands instead of signed 8-bit values.

Rejected: Hunk truncated or invalid

Cast both 8-bit operands to signed values for opcode 6 while preserving the one-bit comparison result and zero extension.

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

Opcode 6 uses an unsigned comparison where signed 8-bit comparison is expected.

Rejected: Expected --- a/path and +++ b/path

For opcode 6, compare sign bits first. When the signs match, the existing unsigned comparison gives the same ordering as a signed comparison.

```diff
--- a/rtl/alu.v
+++ b/rtl/alu.v
@@ -8,6 +8,6 @@
         3'd3: result = a | b;
         3'd4: result = a ^ b;
         3'd5: result = a << b[2:0];
-        3'd6: result = {7'd0, (a < b)};
+        3'd6: result = {7'd0, ((a[7] != b[7]) ? a[7] : (a < b))};
         default: result = a;
     endcase
 end
```

Duration: 14216 ms; Provider calls: 2; tokens in/out: 6743/874.
Estimated cost: 0.0182948.

Scripted providers and replay output are not live AI benchmark results.
