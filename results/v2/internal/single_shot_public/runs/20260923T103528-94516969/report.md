# Evidence: case_027_pulse_combinational

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The pulse condition detects a sustained high level instead of a rising edge.

Invert the prior-sample condition to detect a rising edge.

```diff
--- a/rtl/pulse.v
+++ b/rtl/pulse.v
@@ -4,7 +4,7 @@
     if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
     else begin
         previous <= signal_in;
-        pulse_out <= enable && signal_in && previous;
+        pulse_out <= enable && signal_in && !previous;
     end
 end
 endmodule
```

Regression: PASS

Duration: 10019 ms; Provider calls: 1; tokens in/out: 6039/285.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
