# Evidence: case_026_pulse_sequential

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | FAIL | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Blocking update overwrites the prior sample before edge detection

Change the sampled-input register update at rtl/pulse.v:6 to nonblocking so rtl/pulse.v:7 reads its value from the preceding clock edge.

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

Duration: 7023 ms; Provider calls: 1; tokens in/out: 3369/325.
Estimated cost: 0.0039292.

Scripted providers and replay output are not live AI benchmark results.
