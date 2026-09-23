# Evidence: case_030_pulse_connectivity

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: connectivity. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The history register tracks enable instead of signal_in.

Track the prior value of signal_in so the existing pulse expression detects its rising edge while enable gates the output.

```diff
--- a/rtl/pulse.v
+++ b/rtl/pulse.v
@@ -3,7 +3,7 @@
 always @(posedge clk) begin
     if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
     else begin
-        previous <= enable;
+        previous <= signal_in;
         pulse_out <= enable && signal_in && !previous;
     end
 end
```

Regression: PASS

Duration: 7921 ms; Provider calls: 1; tokens in/out: 3119/380.
Estimated cost: 0.0080724.

Scripted providers and replay output are not live AI benchmark results.
