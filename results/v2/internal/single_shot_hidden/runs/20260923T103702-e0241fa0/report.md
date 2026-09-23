# Evidence: case_030_pulse_connectivity

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: connectivity. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The edge-history register samples enable rather than signal_in, causing an extra pulse while signal_in remains high.

Track the prior signal_in value, matching the reference edge detector, while leaving pulse gating unchanged.

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

Duration: 12490 ms; Provider calls: 1; tokens in/out: 6037/328.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
