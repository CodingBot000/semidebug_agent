# Evidence: case_029_pulse_reset

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Reset drives pulse_out high instead of low.

Change the synchronous reset value of pulse_out at rtl/pulse.v:4 to zero, matching the expected reset behavior.

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

Duration: 5357 ms; Provider calls: 1; tokens in/out: 3121/331.
Estimated cost: 0.0039396.

Scripted providers and replay output are not live AI benchmark results.
