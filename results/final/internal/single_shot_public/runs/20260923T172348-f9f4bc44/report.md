# Evidence: case_028_pulse_sequential

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The enable condition is inverted in the pulse-generation expression.

Use the active-high enable condition in the registered rising-edge pulse expression at rtl/pulse.v:7.

```diff
--- a/rtl/pulse.v
+++ b/rtl/pulse.v
@@ -4,7 +4,7 @@
     if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
     else begin
         previous <= signal_in;
-        pulse_out <= !enable && signal_in && !previous;
+        pulse_out <= enable && signal_in && !previous;
     end
 end
 endmodule
```

Regression: PASS

Duration: 6054 ms; Provider calls: 1; tokens in/out: 3122/315.
Estimated cost: 0.0037798000000000003.

Scripted providers and replay output are not live AI benchmark results.
