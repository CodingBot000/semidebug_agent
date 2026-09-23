# Evidence: case_026_pulse_sequential

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | FAIL | PASS |
| synthesis | PASS | PASS |

## Attempt 1

A blocking update overwrites the prior sampled input before the rising-edge test.

Use a nonblocking assignment for the sequential previous-input register.

```diff
--- a/rtl/pulse.v
+++ b/rtl/pulse.v
@@ -3,7 +3,7 @@
 always @(posedge clk) begin
     if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
     else begin
-        previous = signal_in;
+        previous <= signal_in;
         pulse_out <= enable && signal_in && !previous;
     end
 end
```

Regression: PASS

Duration: 10909 ms; Provider calls: 1; tokens in/out: 6282/286.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
