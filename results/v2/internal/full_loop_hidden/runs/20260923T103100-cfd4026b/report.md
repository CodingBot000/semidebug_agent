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

The RTL tracks the previous value of enable instead of signal_in, causing an extra pulse when signal_in remains high.

Track the prior signal_in value so the pulse condition detects a rising signal while enable is asserted.

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

Duration: 10747 ms; Provider calls: 1; tokens in/out: 6037/324.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
