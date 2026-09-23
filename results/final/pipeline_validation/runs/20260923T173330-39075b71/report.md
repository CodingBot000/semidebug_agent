# Evidence: case_015_arbiter_combinational

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: combinational. Immutable integrity: True.
Reasoning: unspecified; billing: unspecified.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -6,7 +6,7 @@
         2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
         2'b11: grant = priority_bit ? 2'b10 : 2'b01;
-        default: grant = 2'b01;
+        default: grant = 2'b00;
     endcase
 end
 always @(posedge clk) begin
```

Regression: PASS

Duration: 1006 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
