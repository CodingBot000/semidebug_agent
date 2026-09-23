# Evidence: case_029_pulse_reset

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: reset. Immutable integrity: True.
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
--- a/rtl/pulse.v
+++ b/rtl/pulse.v
@@ -1,7 +1,7 @@
 module pulse(input wire clk, rst, signal_in, enable, output reg pulse_out);
 reg previous;
 always @(posedge clk) begin
-    if (rst) begin previous <= 1'b0; pulse_out <= 1'b1; end
+    if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
     else begin
         previous <= signal_in;
         pulse_out <= enable && signal_in && !previous;
```

Regression: PASS

Duration: 1131 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
