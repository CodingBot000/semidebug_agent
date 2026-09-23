# Evidence: case_029_pulse_reset

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Reset assigns pulse_out high, but the reference expects it low.

Set the registered pulse output to zero during reset, matching the reference behavior.

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

Duration: 11501 ms; Provider calls: 1; tokens in/out: 6036/307.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
